"""
Lead qualification and scoring module.
Evaluates discovered leads based on digital footprint heuristics to determine 
viability for personalized outreach sequences.
"""
from app.models.lead import Lead
from app.modules.qualification.website_checker import check_website
from app.modules.qualification.social_checker import check_social_media

async def qualify_lead(lead: Lead) -> tuple[bool, int, str]:
    """
    Computes a comprehensive qualification score for a given lead by analyzing 
    website availability, social media presence, and public rating metrics.
    
    Args:
        lead (Lead): The instantiated Lead model to evaluate.
        
    Returns:
        tuple[bool, int, str]: A boolean indicating qualification status, the derived score, and consolidated evaluator notes.
    """
    score = 0
    notes = []

    if not lead.website_url:
        score += 40
        notes.append("No website URL found in Places data.")
        is_dns_valid = False
        is_http_valid = False
    else:
        is_dns_valid, is_http_valid, _ = await check_website(lead.website_url)
        
        if not is_dns_valid:
            score += 30
            notes.append("Domain does not resolve (NXDOMAIN).")
        elif not is_http_valid:
            score += 25
            notes.append("Website is unreachable or returns HTTP error.")
            
    if lead.website_url and is_http_valid:
        has_socials, social_notes = await check_social_media(lead.website_url)
        if not has_socials:
            score += 10
            notes.append("No common social media links found.")
        else:
            notes.append(f"Social media: {social_notes}")
            
    if lead.rating and lead.rating >= 4.0:
        score += 10
        notes.append(f"High rating ({lead.rating} stars) indicates active business.")
        
    if lead.phone:
        score += 5
        notes.append("Phone number is available.")

    is_qualified = score >= 50
    return is_qualified, score, " | ".join(notes)
