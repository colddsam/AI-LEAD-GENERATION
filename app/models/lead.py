"""
Core lead and geographic targeting database models.
Defines schemas for discovered local businesses, search constraints,
and the full lead lifecycle footprint.
"""
import uuid
from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Float,
    ForeignKey, Integer, JSON, String, Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models import Base


class SearchHistory(Base):
    """
    Archives discovery parameters to enforce deduplication
    and prevent redundant API queries within cooling periods.
    """
    __tablename__ = "search_history"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city       = Column(String(100), nullable=False, index=True)
    category   = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


class Lead(Base):
    """
    Primary model for a discovered local business prospect.
    Tracks profile properties, qualification metrics, and lifecycle timestamps.

    ── Status lifecycle ──────────────────────────────────────────────────────
    discovered
      → qualified        score >= 50, has email  → automated email sequence
      → phone_qualified  score >= 50, phone only → manual call / WhatsApp alert
      → rejected         score < 50 or no contact
    qualified / phone_qualified
      → queued_for_send  (personalization complete, email queued)
    queued_for_send
      → email_sent
    email_sent
      → opened → clicked → replied
    (any active stage can become bounced or unsubscribed)
    """
    __tablename__ = "leads"

    # ── Identity ──────────────────────────────────────────────────────────────
    id             = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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

    # ── Qualification ─────────────────────────────────────────────────────────
    qualification_score = Column(Integer, default=0)
    has_website         = Column(Boolean, default=False)
    has_social_media    = Column(Boolean, default=False)
    web_presence_notes  = Column(String, nullable=True)

    # Lead tier: A / B / C / D  (VARCHAR(2), 1-character values only)
    lead_tier = Column(String(2), nullable=True)

    # ── Website quality signals (populated during qualification) ──────────────
    website_title        = Column(String(255), nullable=True)
    website_copyright_year = Column(Integer, nullable=True)
    is_mobile_responsive = Column(Boolean, nullable=True)
    has_online_booking   = Column(Boolean, nullable=True)
    has_ecommerce        = Column(Boolean, nullable=True)

    # ── Status lifecycle ──────────────────────────────────────────────────────
    # Valid values:
    #   discovered | qualified | phone_qualified | rejected
    #   queued_for_send | email_sent
    #   opened | clicked | replied | bounced | unsubscribed
    status = Column(String(50), default="discovered", index=True)

    # ── Lifecycle timestamps ──────────────────────────────────────────────────
    # discovered_at must NEVER be overwritten after the initial insert.
    # The check_stmt guard in run_discovery_stage skips existing place_ids,
    # so re-runs will never touch this value.
    discovered_at  = Column(
        DateTime(timezone=True), default=func.now(), nullable=False, index=True
    )
    qualified_at   = Column(DateTime(timezone=True), nullable=True)
    email_sent_at  = Column(DateTime(timezone=True), nullable=True)
    first_opened_at = Column(
        DateTime(timezone=True), nullable=True,
        comment="Timestamp of first email open pixel hit."
    )
    first_clicked_at = Column(
        DateTime(timezone=True), nullable=True,
        comment="Timestamp of first tracked link click."
    )
    first_replied_at = Column(DateTime(timezone=True), nullable=True)

    # ── Follow-up sequence ────────────────────────────────────────────────────
    followup_count           = Column(Integer, default=0)
    next_followup_at         = Column(DateTime(timezone=True), nullable=True)
    followup_sequence_active = Column(Boolean, default=True)

    # ── Reply intelligence ────────────────────────────────────────────────────
    # classification: interested | not_interested | auto_reply |
    #                 wrong_person | question | pricing_inquiry
    reply_classification  = Column(String(50), nullable=True)
    reply_confidence      = Column(Float, nullable=True)
    reply_key_signal      = Column(Text, nullable=True)
    suggested_reply_draft = Column(Text, nullable=True)

    # ── Metadata ──────────────────────────────────────────────────────────────
    raw_places_data = Column(
        JSON, nullable=True,
        comment="Raw Google Places API payload for discovery fallback."
    )
    notes = Column(
        Text, nullable=True,
        comment="Custom context or manual remarks about the lead."
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    outreach = relationship(
        "EmailOutreach", back_populates="lead", cascade="all, delete-orphan"
    )
    events = relationship(
        "EmailEvent", back_populates="lead", cascade="all, delete-orphan"
    )
    social_networks = relationship(
        "LeadSocialNetwork", back_populates="lead", cascade="all, delete-orphan"
    )


class LeadSocialNetwork(Base):
    """
    Stores individual social media profiles found during qualification.
    At most one entry per platform per lead (enforced in social_checker.py).
    """
    __tablename__ = "lead_social_networks"

    id          = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id     = Column(
        UUID(as_uuid=True),
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    # platform_name values: facebook | instagram | linkedin | twitter |
    #                        youtube | tiktok | pinterest
    platform_name = Column(String(50), nullable=False, index=True)
    profile_url   = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    lead = relationship("Lead", back_populates="social_networks")