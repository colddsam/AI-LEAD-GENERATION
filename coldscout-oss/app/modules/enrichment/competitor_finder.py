"""Competitor discovery for Cold Scout OSS."""
from sqlalchemy import select
from app.models.lead import Lead


async def find_top_competitor(category: str, city: str, db) -> dict | None:
    if not category or not city:
        return None
    stmt = select(Lead).where(
        Lead.category == category,
        Lead.city == city,
        Lead.has_website == True,
        Lead.rating >= 4.0,
    ).order_by(Lead.rating.desc(), Lead.review_count.desc()).limit(1)

    res = await db.execute(stmt)
    competitor = res.scalars().first()
    if competitor:
        return {"name": competitor.business_name, "website": competitor.website_url}
    return None
