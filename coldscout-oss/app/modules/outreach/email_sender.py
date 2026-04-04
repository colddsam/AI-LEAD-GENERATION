"""
Email dispatch via SMTP for Cold Scout OSS.
Uses user-provided Brevo credentials.
"""
import os
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

import aiosmtplib
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import get_settings

settings = get_settings()

_ALLOWED_EXTENSIONS = {".pdf", ".xlsx", ".xls", ".csv", ".txt"}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    attachment_paths: list[str] = None,
) -> bool:
    message = EmailMessage()
    message["From"] = formataddr((settings.FROM_NAME, settings.FROM_EMAIL))
    message["To"] = to_email
    message["Subject"] = subject
    if settings.REPLY_TO_EMAIL:
        message["Reply-To"] = settings.REPLY_TO_EMAIL

    message.set_content("Please enable HTML to view this message.")
    message.add_alternative(html_content, subtype="html")

    if attachment_paths:
        for filepath in attachment_paths:
            path = Path(filepath)
            if not path.exists() or path.suffix.lower() not in _ALLOWED_EXTENSIONS:
                logger.warning(f"Skipping attachment: {filepath}")
                continue

            with open(path, "rb") as f:
                file_data = f.read()

            subtype_map = {
                ".xlsx": "vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ".xls": "vnd.ms-excel",
                ".csv": "csv",
                ".txt": "plain",
            }
            subtype = subtype_map.get(path.suffix.lower(), "pdf")
            message.add_attachment(file_data, maintype="application", subtype=subtype, filename=path.name)

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.BREVO_SMTP_HOST,
            port=settings.BREVO_SMTP_PORT,
            username=settings.BREVO_SMTP_USER,
            password=settings.BREVO_SMTP_PASSWORD,
            use_tls=settings.BREVO_SMTP_PORT == 465,
            start_tls=settings.BREVO_SMTP_PORT == 587,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        raise e
