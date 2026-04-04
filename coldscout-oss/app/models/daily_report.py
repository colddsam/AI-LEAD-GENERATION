"""Daily report model for Cold Scout OSS."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, DateTime
from app.database import Base


def _uuid():
    return str(uuid.uuid4())


class DailyReport(Base):
    __tablename__ = "daily_reports"

    id           = Column(String(36), primary_key=True, default=_uuid)
    report_date  = Column(Date, unique=True, nullable=False)

    leads_discovered = Column(Integer, default=0)
    leads_qualified  = Column(Integer, default=0)
    emails_sent      = Column(Integer, default=0)
    emails_opened    = Column(Integer, default=0)
    links_clicked    = Column(Integer, default=0)
    replies_received = Column(Integer, default=0)

    pipeline_started_at = Column(DateTime, nullable=True)
    pipeline_ended_at   = Column(DateTime, nullable=True)
    pipeline_status     = Column(String(50), default="pending")
    error_log           = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
