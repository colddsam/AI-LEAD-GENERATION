from sqlalchemy.orm import declarative_base

# Shared Base Model for Alembic to detect
Base = declarative_base()

# Import all models here so they get registered with Base
from app.models.lead import Lead, TargetLocation
from app.models.campaign import Campaign, EmailOutreach
from app.models.email_event import EmailEvent
from app.models.daily_report import DailyReport
