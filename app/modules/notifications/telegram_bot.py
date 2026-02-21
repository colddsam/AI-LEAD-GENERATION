"""
Telegram Bot notification module.
Facilitates system-wide alerting capabilities by interfacing with the 
Telegram Bot API for administrative tracking.
"""
import httpx
from app.config import get_settings
settings = get_settings()
import logging

logger = logging.getLogger(__name__)

async def send_telegram_alert(message: str) -> bool:
    """
    Transmits an arbitrary textual payload to the securely configured Telegram administrative channel.
    
    Args:
        message (str): The structured alert message to dispatch.
        
    Returns:
        bool: True if the dispatch was successfully processed, False otherwise.
    """
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.warning("Telegram credentials not set. Alert skipped.")
        return False
        
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=5.0)
            if response.status_code == 200:
                return True
            else:
                logger.error(f"Failed to send Telegram alert: {response.text}")
                return False
    except Exception as e:
        logger.error(f"Telegram API Exception: {e}")
        return False
