"""
Domain validity and HTTP accessibility verification module.
Performs asynchronous DNS resolution and HTTP health checks to ascertain 
the operational status of target lead domains.
"""
import httpx
import dns.resolver
from typing import Tuple
from loguru import logger

async def dns_resolves(domain: str) -> bool:
    """
    Performs an asynchronous DNS query for A records against the provided domain string.
    
    Args:
        domain (str): The fully qualified domain name (FQDN) to test.
        
    Returns:
        bool: True if the domain successfully resolves, False otherwise.
    """
    if not domain:
        return False
        
    try:
        domain = domain.replace('http://', '').replace('https://', '')
        domain = domain.split('/')[0]
        
        resolver = dns.resolver.Resolver()
        resolver.timeout = 3
        resolver.lifetime = 3
        
        resolver.resolve(domain, 'A')
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.LifetimeTimeout):
        return False
    except Exception as e:
        logger.debug(f"DNS Resolution failed for {domain}: {e}")
        return False

async def website_responds(url: str) -> bool:
    """
    Executes an asynchronous HTTP GET request to verify non-error HTTP status codes.
    
    Args:
        url (str): The target URL to establish an HTTP connection with.
        
    Returns:
        bool: True if the web server responds with a sub-400 status code, False otherwise.
    """
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
    Orchestrates sequential validation of a domain via DNS resolution followed by 
    an HTTP accessibility check.
    
    Args:
        url (str): The target URL string associated with the lead.
        
    Returns:
        Tuple[bool, bool, str]: A tuple of booleans indicating DNS validity and HTTP accessibility, plus the evaluated URL.
    """
    if not url:
        return False, False, url
        
    domain = url.replace('http://', '').replace('https://', '').split('/')[0]
    is_dns_valid = await dns_resolves(domain)
    
    if not is_dns_valid:
        return False, False, url
        
    is_http_valid = await website_responds(url)
    return is_dns_valid, is_http_valid, url
