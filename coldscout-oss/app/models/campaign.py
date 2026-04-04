"""Campaign and email outreach models for Cold Scout OSS."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Date, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base


def _uuid():
    return str(uuid.uuid4())


class Campaign(Base):
    __tablename__ = "campaigns"

    id            = Column(String(36), primary_key=True, default=_uuid)
    name          = Column(String(255), nullable=False)
    campaign_date = Column(Date, nullable=False)
    status        = Column(String(50), default="pending")

    total_leads      = Column(Integer, default=0)
    emails_sent      = Column(Integer, default=0)
    emails_opened    = Column(Integer, default=0)
    links_clicked    = Column(Integer, default=0)
    replies_received = Column(Integer, default=0)

    started_at   = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at   = Column(DateTime, default=datetime.utcnow)

    outreach = relationship("EmailOutreach", back_populates="campaign", cascade="all, delete-orphan")


class EmailOutreach(Base):
    __tablename__ = "email_outreach"

    id          = Column(String(36), primary_key=True, default=_uuid)
    lead_id     = Column(String(36), ForeignKey("leads.id", ondelete="CASCADE"), index=True)
    campaign_id = Column(String(36), ForeignKey("campaigns.id"))

    to_email       = Column(String(255), nullable=False)
    subject        = Column(Text, nullable=False)
    body_html      = Column(Text, nullable=True)
    tracking_token = Column(String(255), unique=True, index=True, nullable=False)

    ai_generated    = Column(Boolean, default=True)
    has_attachment  = Column(Boolean, default=False)
    attachment_names = Column(JSON, nullable=True)

    status = Column(String(50), default="queued")

    sent_at    = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    lead     = relationship("Lead", back_populates="outreach")
    campaign = relationship("Campaign", back_populates="outreach")
