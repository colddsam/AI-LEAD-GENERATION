"""
Email engagement event database model module.
Defines the SQLAlchemy schema for tracking discrete lead interactions 
such as email opens and link clicks tied to specific outreach efforts.
"""
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models import Base

class EmailEvent(Base):
    """
    Model representing a granular engagement event triggered by a prospective lead,
    facilitating analytics on campaign performance and individual lead readiness.
    """
    __tablename__ = "email_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"), index=True)
    outreach_id = Column(UUID(as_uuid=True), ForeignKey("email_outreach.id"))
    tracking_token = Column(String(255), nullable=True)

    event_type = Column(String(50), nullable=False, index=True)
    
    url_clicked = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)

    occurred_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    lead = relationship("Lead", back_populates="events")
    outreach = relationship("EmailOutreach", back_populates="events")

