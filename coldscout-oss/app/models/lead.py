"""
Lead and search history models for Cold Scout OSS.
SQLite-compatible — no PostgreSQL-specific types.
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Float,
    Integer, JSON, String, Text,
)
from sqlalchemy.orm import relationship
from app.database import Base


def _uuid():
    return str(uuid.uuid4())


class SearchHistory(Base):
    __tablename__ = "search_history"

    id         = Column(String(36), primary_key=True, default=_uuid)
    city       = Column(String(100), nullable=False, index=True)
    category   = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class Lead(Base):
    __tablename__ = "leads"

    id             = Column(String(36), primary_key=True, default=_uuid)
    place_id       = Column(String(255), unique=True, index=True, nullable=False)
    business_name  = Column(String(255), nullable=False)
    category       = Column(String(100), nullable=True)
    address        = Column(String, nullable=True)
    city           = Column(String(100), nullable=True)
    phone          = Column(String(50), nullable=True)
    email          = Column(String(255), nullable=True)
    website_url    = Column(String, nullable=True)
    google_maps_url = Column(String, nullable=True)
    rating         = Column(Float, nullable=True)
    review_count   = Column(Integer, nullable=True)

    # Qualification
    ai_score            = Column(Integer, default=0)
    has_website         = Column(Boolean, default=False)
    has_social_media    = Column(Boolean, default=False)
    qualification_notes = Column(String, nullable=True)
    lead_tier           = Column(String(2), nullable=True)

    # Website quality
    website_title         = Column(String(255), nullable=True)
    website_copyright_year = Column(Integer, nullable=True)
    is_mobile_responsive  = Column(Boolean, nullable=True)
    has_online_booking    = Column(Boolean, nullable=True)
    has_ecommerce         = Column(Boolean, nullable=True)

    # Status lifecycle
    status = Column(String(50), default="discovered", index=True)

    # Timestamps
    discovered_at   = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    qualified_at    = Column(DateTime, nullable=True)
    email_sent_at   = Column(DateTime, nullable=True)
    first_opened_at = Column(DateTime, nullable=True)
    first_clicked_at = Column(DateTime, nullable=True)
    first_replied_at = Column(DateTime, nullable=True)

    # Follow-up
    followup_count           = Column(Integer, default=0)
    follow_up_stage          = Column(Integer, default=0)
    next_followup_at         = Column(DateTime, nullable=True)
    followup_sequence_active = Column(Boolean, default=True)

    # Reply intelligence
    reply_classification  = Column(String(50), nullable=True)
    reply_confidence      = Column(Float, nullable=True)
    reply_key_signal      = Column(Text, nullable=True)
    suggested_reply_draft = Column(Text, nullable=True)

    # Metadata
    raw_places_data = Column(JSON, nullable=True)
    notes           = Column(Text, nullable=True)
    created_at      = Column(DateTime, default=datetime.utcnow)
    updated_at      = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    outreach = relationship("EmailOutreach", back_populates="lead", cascade="all, delete-orphan")
