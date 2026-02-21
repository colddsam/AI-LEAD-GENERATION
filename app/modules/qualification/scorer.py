from app.models.lead import Lead
from app.modules.qualification.website_checker import check_website
from app.modules.qualification.social_checker import check_social_media

async def qualify_lead(lead: Lead) -> tuple[bool, int, str]:
    """
    Qualify a Lead based on their digital presence.
    Returns: (is_qualified, score, notes)
    """
    score = 0
    notes = []

    # 1. No website provided by Google Places
    if not lead.website_url:
        score += 40
        notes.append("No website URL found in Places data.")
        is_dns_valid = False
        is_http_valid = False
    else:
        # 2. Check website availability
        is_dns_valid, is_http_valid, _ = await check_website(lead.website_url)
        
        if not is_dns_valid:
            score += 30
            notes.append("Domain does not resolve (NXDOMAIN).")
        elif not is_http_valid:
            score += 25
            notes.append("Website is unreachable or returns HTTP error.")
            
    # 3. Check Social Media
    if lead.website_url and is_http_valid:
        has_socials, social_notes = await check_social_media(lead.website_url)
        if not has_socials:
            score += 10
            notes.append("No common social media links found.")
        else:
            notes.append(f"Social media: {social_notes}")
            
    # 4. Rating checks
    if lead.rating and lead.rating >= 4.0:
        score += 10
        notes.append(f"High rating ({lead.rating} stars) indicates active business.")
        
    # 5. Reachability check
    if lead.phone:
        score += 5
        notes.append("Phone number is available.")

    is_qualified = score >= 50
    return is_qualified, score, " | ".join(notes)
