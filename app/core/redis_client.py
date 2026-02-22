# app/core/redis_client.py
# ============================================================
# 🔴 PRESERVED FOR FUTURE USE — NOT IMPORTED IN ACTIVE CODE
#
# This file is intentionally not imported by any active module.
# When scaling up:
#   1. pip install redis==5.2.0
#   2. Set REDIS_URL in .env
#   3. Import get_redis() wherever caching is needed
#   4. Re-enable Celery (see celery_app.py)
# ============================================================

import redis.asyncio as redis
from app.config import get_settings

_redis_client = None

async def get_redis() -> redis.Redis:
    global _redis_client
    if _redis_client is None:
        settings = get_settings()
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    return _redis_client

async def close_redis():
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
