from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import get_api_key
from app.core.database import get_db
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignResponse, CampaignDetailResponse, CampaignStatsResponse
from typing import List

router = APIRouter(prefix="/campaigns", dependencies=[Depends(get_api_key)])

@router.get("", response_model=List[CampaignResponse])
async def list_campaigns(db: AsyncSession = Depends(get_db)):
    stmt = select(Campaign).order_by(Campaign.campaign_date.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{campaign_id}", response_model=CampaignDetailResponse)
async def get_campaign(campaign_id: str, db: AsyncSession = Depends(get_db)):
    from sqlalchemy.orm import selectinload
    stmt = select(Campaign).options(selectinload(Campaign.outreach)).where(Campaign.id == campaign_id)
    result = await db.execute(stmt)
    campaign = result.scalars().first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.get("/{campaign_id}/stats", response_model=CampaignStatsResponse)
async def get_campaign_stats(campaign_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Campaign).where(Campaign.id == campaign_id)
    result = await db.execute(stmt)
    campaign = result.scalars().first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    from app.models.lead import Lead
    from sqlalchemy import func
    
    discovered = await db.scalar(select(func.count(Lead.id)).where(func.date(Lead.discovered_at) == campaign.campaign_date))
    qualified = await db.scalar(select(func.count(Lead.id)).where(func.date(Lead.qualified_at) == campaign.campaign_date))
    
    return {
        "total_discovered": discovered or 0,
        "total_qualified": qualified or 0,
        "emails_sent": campaign.emails_sent,
        "emails_opened": campaign.emails_opened,
        "links_clicked": campaign.links_clicked,
        "replies_received": campaign.replies_received
    }
