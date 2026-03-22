"""
Optional Redis Client Connectivity Module.

NOTE: This is currently a PASSIVE module reserved for future horizontal scaling.
The system currently uses APScheduler's in-memory / persistent JobManager 
strategy which is sufficient for single-instance deployments.

Scale-Up Path:
1. Install requirements: `pip install redis==5.2.0`
2. Configure: Set `REDIS_URL` in your environment.
3. Integration: Import `get_redis()` for distributed caching or Celery brokerage.
"""

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
