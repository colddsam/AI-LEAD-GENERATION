from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

class CampaignBase(BaseModel):
    name: str
    campaign_date: date
    status: str

class CampaignResponse(CampaignBase):
    id: UUID
    total_leads: int
    emails_sent: int
    emails_opened: int
    links_clicked: int
    replies_received: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
    
class CampaignStatsResponse(BaseModel):
    total_discovered: int
    total_qualified: int
    emails_sent: int
    emails_opened: int
    links_clicked: int
    replies_received: int
    
class EmailOutreachResponse(BaseModel):
    id: UUID
    to_email: str
    subject: str
    status: str
    sent_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class CampaignDetailResponse(CampaignResponse):
    outreach: List[EmailOutreachResponse] = []
