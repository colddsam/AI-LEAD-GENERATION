from pydantic import BaseModel, ConfigDict
from typing import Optional, Any, List
from datetime import datetime
from uuid import UUID

class LeadSocialNetworkBase(BaseModel):
    platform_name: str
    profile_url: str

class LeadSocialNetworkResponse(LeadSocialNetworkBase):
    id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class LeadBase(BaseModel):
    place_id: str
    business_name: str
    category: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website_url: Optional[str] = None
    google_maps_url: Optional[str] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    
    status: Optional[str] = None
    notes: Optional[str] = None

class LeadResponse(LeadBase):
    id: UUID
    qualification_score: int
    has_website: bool
    has_social_media: bool
    web_presence_notes: Optional[str] = None
    discovered_at: Optional[datetime] = None
    qualified_at: Optional[datetime] = None
    email_sent_at: Optional[datetime] = None
    first_opened_at: Optional[datetime] = None
    first_clicked_at: Optional[datetime] = None
    first_replied_at: Optional[datetime] = None
    
    # v2 fields (Optional for now)
    followup_count: Optional[int] = None
    next_followup_at: Optional[datetime] = None
    followup_sequence_active: Optional[bool] = None
    reply_classification: Optional[str] = None
    reply_confidence: Optional[float] = None
    suggested_reply_draft: Optional[str] = None
    reply_key_signal: Optional[str] = None
    lead_tier: Optional[str] = None
    website_title: Optional[str] = None
    website_copyright_year: Optional[int] = None
    is_mobile_responsive: Optional[bool] = None
    has_online_booking: Optional[bool] = None
    has_ecommerce: Optional[bool] = None
    
    model_config = ConfigDict(from_attributes=True)

class LeadDetailResponse(LeadResponse):
    social_networks: List[LeadSocialNetworkResponse] = []

class LeadUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None

class LeadListResponse(BaseModel):
    leads: List[LeadResponse]
    total: int
    page: int
    pages: int
