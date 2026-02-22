# app/modules/discovery/deduplication.py
# ✅ ACTIVE — uses existing leads table, no Redis needed

from datetime import datetime, timedelta
from sqlalchemy import select
from app.models.lead import Lead

# ============================================================
# 🔴 REDIS APPROACH — PRESERVED FOR FUTURE SCALE
# This approach is faster at high volume (100k+ leads)
# because it avoids DB round trips. Reactivate when needed.
#
# import redis.asyncio as redis
# from app.core.redis_client import get_redis
#
# async def is_recently_discovered_redis(place_id: str, hours: int = 24) -> bool:
#     r = await get_redis()
#     key = f"place:{place_id}"
#     exists = await r.exists(key)
#     return bool(exists)
#
# async def mark_as_discovered_redis(place_id: str, hours: int = 24):
#     r = await get_redis()
#     key = f"place:{place_id}"
#     await r.setex(key, hours * 3600, "1")   # Auto-expires after 24hrs
# ============================================================

async def is_recently_discovered(db, place_id: str, hours: int = 24) -> bool:
    """
    Check if a place was already discovered within the last `hours` hours.
    Uses the leads table — place_id has a unique index so this is fast.
    No Redis needed at current scale (~100 places/day).
    """
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    result = await db.execute(
        select(Lead.id)
        .where(Lead.place_id == place_id)
        .where(Lead.discovered_at >= cutoff)
        .limit(1)
    )
    return result.scalar_one_or_none() is not None


async def save_new_leads(db, raw_places: list) -> int:
    """Filter out already-seen places, insert the rest. Returns count of new leads."""
    new_count = 0
    for place in raw_places:
        if await is_recently_discovered(db, place["place_id"]):
            continue
        await db.execute(
            Lead.__table__.insert().values(
                place_id=place["place_id"],
                business_name=place["name"],
                address=place.get("address"),
                phone=place.get("phone"),
                website_url=place.get("website"),
                rating=place.get("rating"),
                google_maps_url=place.get("maps_url"),
                raw_places_data=place,
                status="discovered"
            )
        )
        new_count += 1
    await db.commit()
    return new_count
