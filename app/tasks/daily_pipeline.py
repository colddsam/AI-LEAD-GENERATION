import asyncio
import logging
from datetime import date
from celery import shared_task

from app.core.database import AsyncSessionLocal
from app.models.lead import Lead, TargetLocation
from app.config import settings
from sqlalchemy import select

from app.modules.notifications.telegram_bot import send_telegram_alert

logger = logging.getLogger(__name__)

def run_async(coro):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)

async def _mock_pipeline_step(step_name: str):
    await send_telegram_alert(f"🚀 Running Pipeline Step: {step_name}")
    logger.info(f"Executed {step_name}")

@shared_task(name="app.tasks.daily_pipeline.run_discovery_task")
def run_discovery_task():
    logger.info("Starting Daily Discovery Task")
    run_async(_mock_pipeline_step("Discovery"))

@shared_task(name="app.tasks.daily_pipeline.run_qualification_task")
def run_qualification_task():
    logger.info("Starting Daily Qualification Task")
    run_async(_mock_pipeline_step("Qualification"))

@shared_task(name="app.tasks.daily_pipeline.run_personalization_task")
def run_personalization_task():
    logger.info("Starting Daily Personalization Task")
    run_async(_mock_pipeline_step("Personalization"))

@shared_task(name="app.tasks.daily_pipeline.run_outreach_send_task")
def run_outreach_send_task():
    logger.info("Starting Daily Outreach Send Task")
    run_async(_mock_pipeline_step("Outreach & Sending"))

@shared_task(name="app.tasks.daily_pipeline.run_reply_polling_task")
def run_reply_polling_task():
    logger.info("Starting Reply Polling Task")
    run_async(_mock_pipeline_step("Reply Polling"))

@shared_task(name="app.tasks.daily_pipeline.run_daily_report_task")
def run_daily_report_task():
    logger.info("Starting Daily Report Task")
    run_async(_mock_pipeline_step("Daily Report Generation"))

@shared_task(name="app.tasks.daily_pipeline.run_manual_full_pipeline")
def run_manual_full_pipeline():
    """Manually run all steps sequentially (for testing)"""
    logger.info("Running full manual pipeline...")
    run_discovery_task()
    run_qualification_task()
    run_personalization_task()
    run_outreach_send_task()
    run_daily_report_task()
