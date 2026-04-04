"""
Lead qualification scoring for Cold Scout OSS.
Higher score = weaker digital presence = better prospect.
"""
import asyncio
from loguru import logger
from app.models.lead import Lead
from app.modules.qualification.website_checker import check_website, get_website_quality
from app.modules.qualification.social_checker import check_social_media


def _score_digital_need(website_url, is_dns_valid, is_http_valid, quality, has_socials):
    score = 0
    notes = []

    if not website_url:
        score += 50
        notes.append("No website — maximum digital need.")
        score += 10
        notes.append("Social media presence unverifiable (no website).")
        return score, notes

    if not is_dns_valid:
        score += 35
        notes.append("Domain does not resolve — site completely broken.")
    elif not is_http_valid:
        score += 40
        notes.append("Website unreachable — site is down.")
    else:
        notes.append("Website is live and reachable.")
        if quality.get("is_free_builder"):
            score += 15
            notes.append("Site on free builder — needs professional rebuild.")
        if not quality.get("has_ssl"):
            score += 10
            notes.append("No SSL — outdated.")
        if not quality.get("is_mobile_friendly"):
            score += 10
            notes.append("Not mobile-responsive.")
        copyright_year = quality.get("copyright_year")
        if copyright_year and copyright_year < 2020:
            score += 10
            notes.append(f"Copyright year {copyright_year} — outdated.")
        if not has_socials:
            score += 10
            notes.append("No social media profiles found.")
        else:
            notes.append("Social media profiles found.")

    return score, notes


def _score_viability(lead):
    score = 0
    notes = []
    count = lead.review_count or 0
    if count > 50:
        score += 15
        notes.append(f"High review count ({count}).")
    elif count >= 20:
        score += 10
        notes.append(f"Good reviews ({count}).")
    elif count >= 5:
        score += 5
        notes.append(f"Some reviews ({count}).")
    elif count >= 1:
        score += 2
        notes.append(f"Few reviews ({count}).")

    rating = lead.rating
    if rating is not None and rating >= 4.0:
        score += 15
        notes.append(f"Strong rating ({rating}).")
    elif rating is not None and rating >= 3.0:
        score += 8
        notes.append(f"Average rating ({rating}).")
    elif rating is not None:
        score += 2
        notes.append(f"Low rating ({rating}).")

    if lead.phone:
        score += 10
        notes.append("Phone available.")

    return score, notes


def _assign_tier(score, has_email, has_phone):
    if not (has_email or has_phone):
        return "D"
    if score >= 75:
        return "A"
    if score >= 50:
        return "B"
    if score >= 30:
        return "C"
    return "D"


async def qualify_lead(lead, db=None):
    is_dns_valid = False
    is_http_valid = False
    has_socials = False
    quality = {}

    if lead.website_url:
        (is_dns_valid, is_http_valid, _), quality = await asyncio.gather(
            check_website(lead.website_url),
            get_website_quality(lead.website_url),
        )

    if lead.website_url and is_http_valid:
        has_socials, _ = await check_social_media(lead.website_url)

    need_score, need_notes = _score_digital_need(
        lead.website_url, is_dns_valid, is_http_valid, quality, has_socials
    )
    viability_score, viability_notes = _score_viability(lead)

    total_score = min(need_score + viability_score, 100)

    lead.has_website = is_http_valid
    lead.has_social_media = has_socials
    lead.lead_tier = _assign_tier(total_score, bool(lead.email), bool(lead.phone))

    if quality:
        lead.is_mobile_responsive = quality.get("is_mobile_friendly")
        lead.website_copyright_year = quality.get("copyright_year")

    is_qualified = total_score >= 50 and bool(lead.email or lead.phone)
    all_notes = need_notes + viability_notes

    logger.debug(f"Scored '{lead.business_name}': {total_score}/100 | tier={lead.lead_tier}")

    return is_qualified, total_score, " | ".join(all_notes)
