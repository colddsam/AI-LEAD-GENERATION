"""
Daily reporting database model module.
Defines the SQLAlchemy schema for aggregating and persisting system-wide
performance metrics executed during a standard daily cycle.
"""
import uuid
from sqlalchemy import Column, String, Integer, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.models import Base

class DailyReport(Base):
    """
    Model consolidating metrics across discovery, qualification, and outreach
    activities to facilitate administrative reporting and trend analysis.
    """
    __tablename__ = "daily_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_date = Column(Date, unique=True, nullable=False)

    leads_discovered = Column(Integer, default=0)
    leads_qualified = Column(Integer, default=0)
    emails_sent = Column(Integer, default=0)
    emails_opened = Column(Integer, default=0)
    links_clicked = Column(Integer, default=0)
    replies_received = Column(Integer, default=0)
    new_conversions = Column(Integer, default=0)

    report_file_path = Column(String, nullable=True)
    email_sent_to = Column(String(255), nullable=True)

    pipeline_started_at = Column(DateTime(timezone=True), nullable=True)
    pipeline_ended_at = Column(DateTime(timezone=True), nullable=True)
    pipeline_status = Column(String(50), default="pending")
    error_log = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
