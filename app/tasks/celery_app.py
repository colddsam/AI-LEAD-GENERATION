import os
from celery import Celery
from celery.schedules import crontab
from app.config import settings

redis_url = settings.REDIS_URL
if redis_url.startswith("rediss://") and "?" not in redis_url:
    redis_url += "?ssl_cert_reqs=CERT_NONE"

# Initialize Celery app
celery_app = Celery(
    "lead_gen_worker",
    broker=redis_url,
    backend=redis_url,
    include=["app.tasks.daily_pipeline"]
)

# Optional configuration, see Celery docs
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",  # Update to target user's locale
    enable_utc=True,
    task_track_started=False,  # Saves Redis writes
    task_time_limit=3600,
    
    # --- REDIS/UPSTASH FREE TIER OPTIMIZATIONS ---
    # Greatly reduce aggressive polling
    broker_transport_options={
        'visibility_timeout': 3600,
        'max_connections': 2,
    },
    redis_max_connections=2,
    
    # Disable unneeded background chatter (huge usage savers!)
    worker_send_task_events=False,
    worker_enable_remote_control=False,
    worker_disable_rate_limits=True,
    
    # Turn off celery sync logs
    worker_cancel_long_running_tasks_on_connection_loss=True
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
