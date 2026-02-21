import httpx
from bs4 import BeautifulSoup
import re
from typing import Optional, List
from loguru import logger

async def scrape_contact_email(url: str) -> Optional[str]:
    """
    Attempts to scrape a website to find generic email addresses.
    """
    if not url.startswith("http"):
        url = "http://" + url
        
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, timeout=10.0, follow_redirects=True)
            if response.status_code != 200:
                return None
            
            # Use regex to find email patterns
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            emails = re.findall(email_pattern, response.text)
            
            # Filter out common false positives like example@sentry.io or png/jpg
            valid_emails = []
            for e in emails:
                e_lower = e.lower()
                if "wixpress" in e_lower or "sentry" in e_lower or e_lower.endswith(('.png', '.jpg', '.gif', '.jpeg')):
                    continue
                valid_emails.append(e_lower)
                
            return valid_emails[0] if valid_emails else None
            
    except Exception as e:
        logger.warning(f"Failed to scrape email for {url}")
        return None
