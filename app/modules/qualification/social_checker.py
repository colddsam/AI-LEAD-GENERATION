import httpx
from bs4 import BeautifulSoup
from typing import Tuple

async def check_social_media(url: str) -> Tuple[bool, str]:
    """
    Checks if the website contains links to an active Facebook or Instagram page.
    Returns (has_socials, notes).
    """
    if not url:
        return False, "No website to check."
        
    if not url.startswith("http"):
        url = "http://" + url
        
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, timeout=10.0, follow_redirects=True)
            if response.status_code != 200:
                return False, f"HTTP {response.status_code}"
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            social_found = False
            notes = []
            
            for link in links:
                href = link['href'].lower()
                if 'facebook.com' in href or 'fb.com' in href:
                    notes.append("Facebook found.")
                    social_found = True
                if 'instagram.com' in href:
                    notes.append("Instagram found.")
                    social_found = True
                    
            if not social_found:
                notes.append("No common social media links found on homepage.")
                
            return social_found, " ".join(set(notes))
            
    except Exception as e:
        return False, f"Error checking social media: {str(e)}"
