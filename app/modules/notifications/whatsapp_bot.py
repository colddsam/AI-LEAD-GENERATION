"""
WhatsApp notification integration module.
Dispatches critical, real-time alerts to the administrator's WhatsApp number
when high-intent prospects execute key engagement events.
"""
import httpx
import logging
from app.config import get_settings

logger = logging.getLogger(__name__)

# Basic in-memory counter to respect the 20 msgs/day rate limit.
# Note: In a multi-worker setup, this won't be synchronized perfectly.
whatsapp_msg_count: int = 0 

async def send_whatsapp_alert(message: str) -> bool:
    """
    Transmits an asynchronous alert payload via the CallMeBot API.
    Used selectively for "hot-lead" engagements to preserve strict daily provider limits.
    
    Args:
        message (str): The alert payload to send.
        
    Returns:
        bool: True if transmission succeeded, False otherwise.
    """
    global whatsapp_msg_count
    
    settings = get_settings()
    phone = settings.WHATSAPP_NUMBER
    apikey = settings.CALLMEBOT_API_KEY
    
    if not phone or not apikey:
        logger.warning("WhatsApp API credentials missing. Skipping alert.")
        return False
        
    if whatsapp_msg_count >= 20:
        logger.warning("WhatsApp daily limit (20) reached. Skipping alert.")
        return False
        
    try:
        url = "https://api.callmebot.com/whatsapp.php"
        params = {
            "phone": phone,
            "text": message,
            "apikey": apikey
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            
        whatsapp_msg_count += 1
        return True
    except Exception as e:
        logger.warning(f"Failed to send WhatsApp alert: {e}")
        return False
