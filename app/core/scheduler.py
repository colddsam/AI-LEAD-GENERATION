# app/core/scheduler.py
# ✅ ACTIVE — APScheduler async approach (no Redis required)

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from app.config import get_settings
settings = get_settings()

# ============================================================
# 🔴 CELERY APPROACH — PRESERVED FOR FUTURE SCALE
# When you need distributed workers, import and use celery_app
# instead of this scheduler. Add these back to requirements.txt:
#   celery[redis]==5.4.0
#   redis==5.2.0
# And run separate worker + beat processes in docker-compose.yml
# ============================================================
# from app.tasks.celery_app import celery_app
# from celery.schedules import crontab
# celery_app.conf.beat_schedule = {
#     "run-discovery": {"task": "discovery", "schedule": crontab(hour=6, minute=0)},
#     "run-qualification": {"task": "qualification", "schedule": crontab(hour=7, minute=0)},
#     ...
# }
# ============================================================

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")


def setup_scheduler():
    """
    Register all pipeline stages as cron jobs.
    APScheduler runs in the FastAPI process — no external broker required.
    """

    # Import here to avoid circular imports
    from app.tasks.daily_pipeline import (
        run_discovery_stage,
        run_qualification_stage,
        run_personalization_stage,
        run_outreach_stage,
        poll_replies,
        generate_daily_report,
    )

    scheduler.add_job(
        run_discovery_stage,
        CronTrigger(hour=settings.DISCOVERY_HOUR, minute=0),
        id="discovery",
        replace_existing=True,
        misfire_grace_time=600,       # Allow up to 10min late start (handles Render cold boot)
    )

    scheduler.add_job(
        run_qualification_stage,
        CronTrigger(hour=settings.QUALIFICATION_HOUR, minute=0),
        id="qualification",
        replace_existing=True,
        misfire_grace_time=600,
    )

    scheduler.add_job(
        run_personalization_stage,
        CronTrigger(hour=settings.PERSONALIZATION_HOUR, minute=0),
        id="personalization",
        replace_existing=True,
        misfire_grace_time=600,
    )

    scheduler.add_job(
        run_outreach_stage,
        CronTrigger(hour=settings.OUTREACH_HOUR, minute=0),
        id="outreach",
        replace_existing=True,
        misfire_grace_time=600,
    )

    scheduler.add_job(
        poll_replies,
        "interval",
        minutes=30,
        id="reply_poll",
        replace_existing=True,
    )

    scheduler.add_job(
        generate_daily_report,
        CronTrigger(hour=settings.REPORT_HOUR, minute=settings.REPORT_MINUTE),
        id="daily_report",
        replace_existing=True,
        misfire_grace_time=600,
    )

    scheduler.start()
    logger.info("✅ APScheduler started — all pipeline stages registered")
    logger.info(f"   Discovery:      {settings.DISCOVERY_HOUR}:00 IST")
    logger.info(f"   Qualification:  {settings.QUALIFICATION_HOUR}:00 IST")
    logger.info(f"   Personalization:{settings.PERSONALIZATION_HOUR}:00 IST")
    logger.info(f"   Outreach:       {settings.OUTREACH_HOUR}:00 IST")
    logger.info(f"   Daily Report:   {settings.REPORT_HOUR}:{settings.REPORT_MINUTE} IST")
