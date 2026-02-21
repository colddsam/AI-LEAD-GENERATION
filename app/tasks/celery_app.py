import os
from celery import Celery
from celery.schedules import crontab
from app.config import settings

# Initialize Celery app
celery_app = Celery(
    "lead_gen_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.daily_pipeline"]
)

# Optional configuration, see Celery docs
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",  # Update to target user's locale
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
)

# Scheduled tasks via Celery Beat (alternative to APScheduler if running as worker)
celery_app.conf.beat_schedule = {
    # 6:00 AM - Discovery
    "run-discovery-morning": {
        "task": "app.tasks.daily_pipeline.run_discovery_task",
        "schedule": crontab(hour=settings.DISCOVERY_HOUR, minute=0),
    },
    # 7:00 AM - Qualification
    "run-qualification-morning": {
        "task": "app.tasks.daily_pipeline.run_qualification_task",
        "schedule": crontab(hour=settings.QUALIFICATION_HOUR, minute=0),
    },
    # 8:00 AM - Personalization
    "run-personalize-morning": {
        "task": "app.tasks.daily_pipeline.run_personalization_task",
        "schedule": crontab(hour=settings.PERSONALIZATION_HOUR, minute=0),
    },
    # 9:00 AM - Outreach Sending
    "run-outreach-morning": {
        "task": "app.tasks.daily_pipeline.run_outreach_send_task",
        "schedule": crontab(hour=settings.OUTREACH_HOUR, minute=0),
    },
    # Every 30 minutes - Reply Tracking
    "run-reply-tracking-poll": {
        "task": "app.tasks.daily_pipeline.run_reply_polling_task",
        "schedule": crontab(minute="*/30"),
    },
    # 11:30 PM - Daily Report
    "run-daily-report-night": {
        "task": "app.tasks.daily_pipeline.run_daily_report_task",
        "schedule": crontab(hour=settings.REPORT_HOUR, minute=settings.REPORT_MINUTE),
    },
}
