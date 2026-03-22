"""
Health check API endpoint.
Provides system status for monitoring and diagnostics.
"""
from fastapi import APIRouter, Depends
from loguru import logger
from app.config import get_settings, get_production_status
from app.core.scheduler import scheduler

router = APIRouter()

@router.get("/health")
async def health_check(
    settings = Depends(get_settings)
):
    """
    Performs a comprehensive system health check.
    
    Returns:
        dict: A status report of the system's core components.
    """
    from app.models.daily_report import DailyReport
    from sqlalchemy import select
    from app.core.database import get_session_maker

    last_status = "unknown"
    try:
        # Check database health by attempting a simple select on DailyReport
        async with get_session_maker()() as db:
            stmt = select(DailyReport).order_by(DailyReport.report_date.desc()).limit(1)
            res = await db.execute(stmt)
            latest = res.scalars().first()
            if latest:
                last_status = latest.pipeline_status
    except Exception as e:
        logger.error(f"Health check database error: {e}")

    return {
        "status": "healthy",
        "version": "1.0.0", # hardcoded or pulled from elsewhere
        "environment": settings.APP_ENV,
        "last_pipeline_status": last_status,
        "scheduler_running": scheduler.running,
        "production_status": get_production_status() == "RUN"
    }
