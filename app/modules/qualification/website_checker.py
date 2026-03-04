"""
Domain validity and HTTP accessibility verification module.
Performs DNS resolution, HTTP health checks, and basic quality
signals on target business domains.
"""
import re
import httpx
import dns.resolver
from typing import Tuple
from loguru import logger

# Free website builder domains — businesses on these still need a real site
FREE_BUILDER_DOMAINS = (
    "wixsite.com", "wix.com", "weebly.com", "blogspot.com",
    "wordpress.com", "site123.me", "godaddysites.com",
    "squarespace.com", "jimdo.com", "webnode.com",
    "strikingly.com", "yolasite.com", "webflow.io",
)

_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.5",
}


async def dns_resolves(domain: str) -> bool:
    """
    Asynchronously queries DNS A records for a domain.

    Args:
        domain (str): Bare domain name (no scheme, no path).

    Returns:
        bool: True if at least one A record exists.
    """
    if not domain:
        return False
    try:
        domain = (
            domain.replace("http://", "")
            .replace("https://", "")
            .split("/")[0]
        )
        resolver = dns.resolver.Resolver()
        resolver.timeout = 3
        resolver.lifetime = 3
        resolver.resolve(domain, "A")
        return True
    except (
        dns.resolver.NXDOMAIN,
        dns.resolver.NoAnswer,
        dns.resolver.LifetimeTimeout,
    ):
        return False
    except Exception as e:
        logger.debug(f"DNS resolution failed for {domain}: {e}")
        return False


async def website_responds(url: str) -> bool:
    """
    Asynchronously executes an HTTP GET to verify a non-error status code.

    Args:
        url (str): Full website URL.

    Returns:
        bool: True if HTTP status < 400.
    """
    if not url:
        return False
    if not url.startswith("http"):
        url = "http://" + url
    try:
        async with httpx.AsyncClient(
            verify=False, headers=_DEFAULT_HEADERS
        ) as client:
            response = await client.get(url, timeout=8.0, follow_redirects=True)
            return response.status_code < 400
    except Exception as e:
        logger.debug(f"HTTP check failed for {url}: {repr(e)}")
        return False


async def get_website_quality(url: str) -> dict:
    """
    Fetches a live website and extracts quality signals used for lead scoring.

    Only call this when the site is already confirmed reachable (is_http_valid=True)
    to avoid a redundant failing request.

    Args:
        url (str): Full website URL.

    Returns:
        dict with keys:
            has_ssl (bool)            — URL uses HTTPS
            is_mobile_friendly (bool) — Has a viewport meta tag
            is_free_builder (bool)    — Hosted on Wix, Weebly, etc.
            copyright_year (int|None) — Most recent year in copyright notice
            responded (bool)          — Site returned 2xx/3xx
    """
    result = {
        "has_ssl": False,
        "is_mobile_friendly": False,
        "is_free_builder": False,
        "copyright_year": None,
        "responded": False,
    }

    if not url:
        return result

    if not url.startswith("http"):
        url = "http://" + url

    result["has_ssl"] = url.lower().startswith("https")
    result["is_free_builder"] = any(b in url.lower() for b in FREE_BUILDER_DOMAINS)

    try:
        async with httpx.AsyncClient(
            verify=False, headers=_DEFAULT_HEADERS
        ) as client:
            response = await client.get(url, timeout=8.0, follow_redirects=True)
            if response.status_code < 400:
                result["responded"] = True
                html = response.text
                result["is_mobile_friendly"] = "viewport" in html.lower()
                years = re.findall(r"©\s*(\d{4})", html)
                if years:
                    result["copyright_year"] = max(int(y) for y in years)
    except Exception as e:
        logger.debug(f"Quality check failed for {url}: {repr(e)}")

    return result


async def check_website(url: str) -> Tuple[bool, bool, str]:
    """
    Orchestrates DNS resolution followed by an HTTP reachability check.

    Args:
        url (str): The website URL to check.

    Returns:
        Tuple[bool, bool, str]:
            - is_dns_valid: Domain resolves in DNS.
            - is_http_valid: Site returns a non-error HTTP response.
            - url: The original URL (unchanged).
    """
    if not url:
        return False, False, url

    domain = url.replace("http://", "").replace("https://", "").split("/")[0]
    is_dns_valid = await dns_resolves(domain)

    if not is_dns_valid:
        return False, False, url

    is_http_valid = await website_responds(url)
    return is_dns_valid, is_http_valid, url