from datetime import datetime
import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, DateTime, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models import Base

class TargetLocation(Base):
    __tablename__ = "target_locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    country = Column(String(100), default="India")
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    categories = Column(JSON)
    radius_meters = Column(Integer, default=5000)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    place_id = Column(String(255), unique=True, index=True, nullable=False)
    business_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)
    address = Column(String, nullable=True)
    city = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    website_url = Column(String, nullable=True)
    google_maps_url = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    review_count = Column(Integer, nullable=True)

    # Qualification
    qualification_score = Column(Integer, default=0)
    has_website = Column(Boolean, default=False)
    has_social_media = Column(Boolean, default=False)
    web_presence_notes = Column(String, nullable=True)

    # Lifecycle Status
    status = Column(String(50), default="discovered", index=True)

    # Timestamps
    discovered_at = Column(DateTime(timezone=True), default=func.now(), index=True)
    qualified_at = Column(DateTime(timezone=True), nullable=True)
    email_sent_at = Column(DateTime(timezone=True), nullable=True)
    first_opened_at = Column(DateTime(timezone=True), nullable=True)
    first_clicked_at = Column(DateTime(timezone=True), nullable=True)
    first_replied_at = Column(DateTime(timezone=True), nullable=True)

    # Metadata
    raw_places_data = Column(JSON, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    outreach = relationship("EmailOutreach", back_populates="lead", cascade="all, delete-orphan")
    events = relationship("EmailEvent", back_populates="lead", cascade="all, delete-orphan")
