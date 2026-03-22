"""
AI Lead Generation System - Database Foundation

This module defines the SQLAlchemy declarative base used by all models in the system.
It includes specific logic for schema handling to ensure compatibility across different
database backends (PostgreSQL for production/Supabase vs. SQLite for local testing).
"""
import os
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

# Shared Base Model for Alembic to detect
# Force 'public' schema to prevent Supabase from defaulting to 'extensions', except for sqlite tests.
# This ensures that our tables are created in the standard PostgreSQL location.
db_url = os.environ.get("DATABASE_URL", "")
schema = None if "sqlite" in db_url else "public"

metadata_obj = MetaData(schema=schema)
Base = declarative_base(metadata=metadata_obj)
