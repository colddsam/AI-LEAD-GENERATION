"""
Database connection and session management module.
Provides async connection pooling and session makers for PostgreSQL.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from functools import lru_cache

from app.config import get_settings
from sqlalchemy import text
from loguru import logger

Base = declarative_base()

_engine = None
_async_session_maker = None


def get_engine():
    """
    Initializes and retrieves the global async SQLAlchemy engine.
    Establishes connection pool settings.
    """
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
    """
    Initializes and retrieves the global async session maker factory.
    """
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
    """
    Async dependency to acquire and release isolated database sessions.
    """
    async_session = get_session_maker()
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def verify_tables_exist():
    """
    Verifies that required core application tables exist in the database.
    Raises SystemExit if uninitialized.
    """
    engine = get_engine()
    async with engine.begin() as conn:
        try:
            # Try to query two of the most foundational tables explicitly in public schema
            await conn.execute(text("SELECT id FROM public.leads LIMIT 1"))
            await conn.execute(text("SELECT id FROM public.search_history LIMIT 1"))
        except Exception as e:
            # Check for Postgres ('does not exist') or SQLite ('no such table') errors
            error_str = str(e).lower()
            if "does not exist" in error_str or "no such table" in error_str:
                error_msg = (
                    "Database tables are missing or uninitialized! 🛑\n"
                    "Please run: 'python create_tables.py' to set up the database schema."
                )
                logger.error(error_msg)
                import sys
                sys.exit(error_msg)
            # If it's a different exception (e.g. auth failed), surface it
            raise