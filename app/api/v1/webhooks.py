"""
External webhook listener execution module.
Exposes dedicated POST endpoints for third-party service providers (e.g., SMTP gateways)
to asynchronously push asynchronous delivery and engagement telemetry.
"""
from fastapi import APIRouter, Request, Depends, BackgroundTasks
import logging
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from app.models.campaign import EmailOutreach

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/webhooks/brevo")
async def brevo_webhook(request: Request, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """
    Ingests and parses payload data delivered by the Brevo SMTP gateway webhook service.
    Translates asynchronous 'delivered' and 'bounced' states to local database entities.
    
    Security Note: Production implementations require validation of the `X-Mailin-Custom` 
    header or origin IP whitelists to prevent unauthorized spoofing.
    
    Args:
        request (Request): Unparsed client request to be consumed as JSON.
        background_tasks (BackgroundTasks): Utility for deferring execution.
        db (AsyncSession): The injected database session dependency.
        
    Returns:
        dict: Standardized success or failure acknowledgment.
    """
    
    try:
        payload = await request.json()
        event = payload.get("event")
        email = payload.get("email")
        message_id = payload.get("message-id")
        
        logger.info(f"Received Brevo webhook: {event} for {email}")
        
        if event == "delivered" and message_id:
            stmt = (
                update(EmailOutreach)
                .where(EmailOutreach.brevo_message_id == message_id)
                .values(status="delivered")
            )
            await db.execute(stmt)
            await db.commit()
            
        elif event in ["bounced", "hard_bounce", "soft_bounce", "spam", "blocked"] and message_id:
            stmt = (
                update(EmailOutreach)
                .where(EmailOutreach.brevo_message_id == message_id)
                .values(status="bounced", bounce_reason=payload.get("reason", event))
            )
            await db.execute(stmt)
            await db.commit()
            
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing Brevo webhook: {e}")
        return {"status": "error"}
