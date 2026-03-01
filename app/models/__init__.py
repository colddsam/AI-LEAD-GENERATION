from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

# Shared Base Model for Alembic to detect
# Force 'public' schema to prevent Supabase from defaulting to 'extensions'
metadata_obj = MetaData(schema="public")
Base = declarative_base(metadata=metadata_obj)

# Import all models here so they get registered with Base
from app.models.lead import Lead
from app.models.campaign import Campaign, EmailOutreach
from app.models.email_event import EmailEvent
from app.models.daily_report import DailyReport
