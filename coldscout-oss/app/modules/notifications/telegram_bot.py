"""Optional Telegram alerts for Cold Scout OSS."""
import httpx
from loguru import logger
from app.config import get_settings

settings = get_settings()


async def send_telegram_alert(message: str) -> bool:
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.debug("Telegram not configured — alert skipped.")
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json={
                "chat_id": settings.TELEGRAM_CHAT_ID,
                "text": message,
            }, timeout=5.0)
            return response.status_code == 200
    except Exception as e:
        logger.error(f"Telegram error: {e}")
        return False
