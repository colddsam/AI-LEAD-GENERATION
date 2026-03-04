from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import get_api_key
from app.core.database import get_db
from app.models.daily_report import DailyReport
from app.schemas.report import ReportResponse
from typing import List
from fastapi.responses import FileResponse
import os
import datetime

router = APIRouter(prefix="/reports", dependencies=[Depends(get_api_key)])

@router.get("", response_model=List[ReportResponse])
async def list_reports(db: AsyncSession = Depends(get_db)):
    stmt = select(DailyReport).order_by(DailyReport.report_date.desc())
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{date}", response_model=ReportResponse)
async def get_report_by_date(date: datetime.date, db: AsyncSession = Depends(get_db)):
    stmt = select(DailyReport).where(DailyReport.report_date == date)
    result = await db.execute(stmt)
    report = result.scalars().first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.get("/{date}/download")
async def download_report(date: datetime.date, db: AsyncSession = Depends(get_db)):
    stmt = select(DailyReport).where(DailyReport.report_date == date)
    result = await db.execute(stmt)
    report = result.scalars().first()
    if not report or not report.report_file_path or not os.path.exists(report.report_file_path):
        raise HTTPException(status_code=404, detail="Report file not found")
        
    return FileResponse(
        path=report.report_file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=os.path.basename(report.report_file_path)
    )
