"""
External Webhook Listener Module.

Exposes POST endpoints for delivery telemetry from third-party SMTP gateways.
Currently handles Brevo (formerly Sendinblue) event notifications.

Security:
  When BREVO_WEBHOOK_SECRET is configured in the environment, every inbound
  request must carry a matching 'X-Brevo-Secret' header.  Requests that fail
  this check are rejected with HTTP 403 before any database work is performed.
  Without a configured secret, the endpoint operates in open mode (acceptable
  for local development; not recommended in production).
"""

import hmac
import logging

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, Request, status
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.database import get_db
from app.models.campaign import EmailOutreach

logger = logging.getLogger(__name__)
router = APIRouter()


def _verify_brevo_secret(provided: str | None) -> None:
    """
    Validates the shared secret sent by Brevo against the configured value.

    Uses ``hmac.compare_digest`` for a constant-time comparison to prevent
    timing-based secret enumeration attacks.

    Args:
        provided: The value of the ``X-Brevo-Secret`` request header, or None
                  if the header was absent.

    Raises:
        HTTPException 403: If BREVO_WEBHOOK_SECRET is configured and the
                           provided header is absent or does not match.
    """
    expected = get_settings().BREVO_WEBHOOK_SECRET
    if not expected:
        # No secret configured — webhook runs in open mode (dev/local use only).
        return

    if not provided or not hmac.compare_digest(provided, expected):
        logger.warning(
            "Brevo webhook request rejected: missing or invalid X-Brevo-Secret header."
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid webhook secret.",
        )


@router.post("/webhooks/brevo")
async def brevo_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    x_brevo_secret: str | None = Header(default=None),
) -> dict:
    """
    Parses delivery telemetry from the Brevo SMTP gateway webhook.

    Translates ``delivered``, ``bounced``, and related event types into local
    ``EmailOutreach`` status updates so the dashboard reflects accurate delivery
    state without polling the Brevo API.

    Request Headers:
        X-Brevo-Secret: Shared secret for request authentication (see BREVO_WEBHOOK_SECRET).

    Request Body (JSON):
        event (str):       Brevo event type (e.g. "delivered", "hard_bounce").
        email (str):       Recipient email address.
        message-id (str):  Brevo message identifier used to locate the local record.
        reason (str):      Optional bounce reason string.

    Returns:
        {"status": "ok"} on successful processing.
    """
    # Authenticate the request before touching the database.
    _verify_brevo_secret(x_brevo_secret)

    try:
        payload = await request.json()
        event = payload.get("event")
        email = payload.get("email")
        message_id = payload.get("message-id")

        logger.info("Received Brevo webhook: event=%s for email=%s", event, email)

        if event == "delivered" and message_id:
            stmt = (
                update(EmailOutreach)
                .where(EmailOutreach.brevo_message_id == message_id)
                .values(status="delivered")
            )
            await db.execute(stmt)
            await db.commit()

        elif (
            event in ["bounced", "hard_bounce", "soft_bounce", "spam", "blocked"]
            and message_id
        ):
            stmt = (
                update(EmailOutreach)
                .where(EmailOutreach.brevo_message_id == message_id)
                .values(status="bounced", bounce_reason=payload.get("reason", event))
            )
            await db.execute(stmt)
            await db.commit()

        return {"status": "ok"}

    except HTTPException:
        raise  # Re-raise auth errors unchanged
    except Exception as e:
        logger.error("Error processing Brevo webhook: %s", e)
        return {"status": "error"}
