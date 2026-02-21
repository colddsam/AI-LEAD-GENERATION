from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from functools import lru_cache

from app.config import get_settings

Base = declarative_base()

_engine = None
_async_session_maker = None


def get_engine():
    global _engine

    if _engine is None:
        settings = get_settings()

        engine_args = {
            "echo": False,
            "future": True,
        }

        if not settings.DATABASE_URL.startswith("sqlite"):
            engine_args["pool_size"] = 10
            engine_args["max_overflow"] = 20

        _engine = create_async_engine(
            settings.DATABASE_URL,
            **engine_args
        )

    return _engine


def get_session_maker():
    global _async_session_maker

    if _async_session_maker is None:
        _async_session_maker = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    return _async_session_maker


async def get_db():
    async_session = get_session_maker()
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()