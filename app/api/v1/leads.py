from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import get_api_key
from app.core.database import get_db
from app.models.lead import Lead
from app.schemas.lead import LeadResponse, LeadDetailResponse, LeadUpdate, LeadListResponse
from fastapi.responses import StreamingResponse
import csv
import io
from datetime import date

router = APIRouter(prefix="/leads", dependencies=[Depends(get_api_key)])

@router.get("", response_model=LeadListResponse)
async def list_leads(
    status: Optional[str] = None,
    city: Optional[str] = None,
    category: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Lead)
    if status:
        stmt = stmt.where(Lead.status == status)
    if city:
        stmt = stmt.where(Lead.city.ilike(f"%{city}%"))
    if category:
        stmt = stmt.where(Lead.category.ilike(f"%{category}%"))
    if date_from:
        stmt = stmt.where(func.date(Lead.created_at) >= date_from)
    if date_to:
        stmt = stmt.where(func.date(Lead.created_at) <= date_to)
        
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = await db.scalar(count_stmt)
    if total is None:
        total = 0
    
    stmt = stmt.offset((page - 1) * limit).limit(limit).order_by(Lead.created_at.desc())
    result = await db.execute(stmt)
    leads = result.scalars().all()
    
    pages = (total + limit - 1) // limit if total > 0 else 1
    
    return {
        "leads": leads,
        "total": total,
        "page": page,
        "pages": pages
    }

@router.get("/export/csv")
async def export_leads_csv(
    status: Optional[str] = None,
    city: Optional[str] = None,
    category: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Lead)
    if status:
        stmt = stmt.where(Lead.status == status)
    if city:
        stmt = stmt.where(Lead.city.ilike(f"%{city}%"))
    if category:
        stmt = stmt.where(Lead.category.ilike(f"%{category}%"))
    if date_from:
        stmt = stmt.where(func.date(Lead.created_at) >= date_from)
    if date_to:
        stmt = stmt.where(func.date(Lead.created_at) <= date_to)
        
    result = await db.execute(stmt)
    leads = result.scalars().all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Business Name", "Email", "Phone", "City", "Category", "Status", "Created At"])
    for lead in leads:
        writer.writerow([
            str(lead.id), lead.business_name, lead.email or "", lead.phone or "", 
            lead.city or "", lead.category or "", lead.status, str(lead.created_at)
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]), 
        media_type="text/csv", 
        headers={"Content-Disposition": f"attachment; filename=leads_{date.today()}.csv"}
    )

@router.get("/{lead_id}", response_model=LeadDetailResponse)
async def get_lead(lead_id: str, db: AsyncSession = Depends(get_db)):
    from sqlalchemy.orm import selectinload
    stmt = select(Lead).options(selectinload(Lead.social_networks)).where(Lead.id == lead_id)
    result = await db.execute(stmt)
    lead = result.scalars().first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(lead_id: str, update_data: LeadUpdate, db: AsyncSession = Depends(get_db)):
    stmt = select(Lead).where(Lead.id == lead_id)
    result = await db.execute(stmt)
    lead = result.scalars().first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    if update_data.status is not None:
        lead.status = update_data.status
    if update_data.notes is not None:
        lead.notes = update_data.notes
        
    await db.commit()
    await db.refresh(lead)
    return lead
