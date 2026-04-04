"""Social media presence checker for Cold Scout OSS."""
import re
import httpx
from bs4 import BeautifulSoup
from typing import Tuple, List, Dict
from loguru import logger

SOCIAL_PATTERNS: Dict[str, re.Pattern] = {
    "facebook":  re.compile(r"(facebook\.com|fb\.com)/", re.IGNORECASE),
    "instagram": re.compile(r"instagram\.com/", re.IGNORECASE),
    "linkedin":  re.compile(r"linkedin\.com/", re.IGNORECASE),
    "twitter":   re.compile(r"(twitter\.com|(?<![a-z0-9\-])x\.com)/", re.IGNORECASE),
    "youtube":   re.compile(r"(youtube\.com|youtu\.be)/", re.IGNORECASE),
    "tiktok":    re.compile(r"tiktok\.com/", re.IGNORECASE),
    "pinterest": re.compile(r"(pinterest\.com|pin\.it)/", re.IGNORECASE),
}


async def check_social_media(url: str) -> Tuple[bool, List[Dict[str, str]]]:
    if not url:
        return False, []
    if not url.startswith("http"):
        url = "http://" + url

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(
                url, timeout=10.0, follow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            )
            if response.status_code != 200:
                return False, []

            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)

            social_profiles: List[Dict[str, str]] = []
            seen_platforms: set = set()

            for link in links:
                href = link["href"]
                for platform, pattern in SOCIAL_PATTERNS.items():
                    if pattern.search(href.lower()) and platform not in seen_platforms:
                        seen_platforms.add(platform)
                        social_profiles.append({"platform": platform, "url": href})
                        break

            return bool(social_profiles), social_profiles
    except Exception as e:
        logger.debug(f"Social check failed for {url}: {repr(e)}")
        return False, []
