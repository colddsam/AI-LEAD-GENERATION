import httpx
import dns.resolver
from typing import Tuple
from loguru import logger

async def dns_resolves(domain: str) -> bool:
    """Check if the given domain resolves to any A or CNAME record."""
    if not domain:
        return False
        
    try:
        # Remove http/https protocol if present
        domain = domain.replace('http://', '').replace('https://', '')
        # Remove paths
        domain = domain.split('/')[0]
        
        resolver = dns.resolver.Resolver()
        resolver.timeout = 3
        resolver.lifetime = 3
        
        # Try finding A records
        resolver.resolve(domain, 'A')
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.LifetimeTimeout):
        return False
    except Exception as e:
        logger.debug(f"DNS Resolution failed for {domain}: {e}")
        return False

async def website_responds(url: str) -> bool:
    """Check if the website returns a valid 2xx HTTP status."""
    if not url:
        return False
        
    if not url.startswith('http'):
        url = 'http://' + url
        
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, timeout=5.0, follow_redirects=True)
            return response.status_code < 400
    except Exception as e:
        logger.debug(f"HTTP Check failed for {url}")
        return False

async def check_website(url: str) -> Tuple[bool, bool, str]:
    """
    Combines DNS and HTTP checks.
    Returns: (is_dns_valid, is_http_valid, updated_url)
    """
    if not url:
        return False, False, url
        
    domain = url.replace('http://', '').replace('https://', '').split('/')[0]
    is_dns_valid = await dns_resolves(domain)
    
    if not is_dns_valid:
        return False, False, url
        
    is_http_valid = await website_responds(url)
    return is_dns_valid, is_http_valid, url
