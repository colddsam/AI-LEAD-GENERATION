import asyncio
import sys
import os
from loguru import logger
import traceback

# Ensure the root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import verify_tables_exist
from app.tasks.daily_pipeline import (
    run_discovery_stage,
    run_qualification_stage,
    run_personalization_stage,
    run_outreach_stage,
    poll_replies,
    generate_daily_report
)

async def test_stage(stage_name, stage_func):
    logger.info(f"========== TESTING STAGE: {stage_name} ==========")
    try:
        await stage_func()
        logger.info(f"✅ STAGE {stage_name} COMPLETED SUCCESSFULLY.")
    except Exception as e:
        logger.error(f"❌ STAGE {stage_name} FAILED: {str(e)}")
        logger.error(traceback.format_exc())
    logger.info("=================================================\n")

async def main():
    """
    Executes the daily lead generation pipeline stages manually for debugging or immediate triggering.
    Bypasses the APScheduler to run the sequence synchronously.
    """
    logger.info("Initiating manual pipeline execution...")
    
    # 1. Establish structural integrity
    logger.info("Verifying database tables...")
    await verify_tables_exist()
    
    # 2. Execute pipeline sequence
    # await test_stage("Discovery", run_discovery_stage)
    # await test_stage("Qualification", run_qualification_stage)
    # await test_stage("Personalization", run_personalization_stage)
    # await test_stage("Outreach", run_outreach_stage)
    
    # # 3. Post-outreach actions
    # await test_stage("Poll Replies", poll_replies)
    await test_stage("Generate Daily Report", generate_daily_report)
    
    logger.info("Manual pipeline execution completed.")

if __name__ == "__main__":
    asyncio.run(main())


