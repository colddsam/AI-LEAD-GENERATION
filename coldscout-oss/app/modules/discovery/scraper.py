"""Contact email scraper for Cold Scout OSS."""
import re
from typing import Optional
import httpx
from loguru import logger


async def scrape_contact_email(url: str) -> Optional[str]:
    if not url.startswith("http"):
        url = "http://" + url

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        async with httpx.AsyncClient(verify=False, headers=headers) as client:
            response = await client.get(url, timeout=10.0, follow_redirects=True)
            if response.status_code != 200:
                return None

            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)
            for e in emails:
                e_lower = e.lower()
                if "wixpress" in e_lower or "sentry" in e_lower or e_lower.endswith(('.png', '.jpg', '.gif', '.jpeg')):
                    continue
                return e_lower
            return None
    except Exception as e:
        logger.debug(f"Email scrape failed for {url}: {repr(e)}")
        return None
