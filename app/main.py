"""
AI Lead Generation System - Core API Entry Point

This module serves as the central orchestration layer for the FastAPI application.
It handles application lifecycle (startup/shutdown), security middleware configuration,
and serves as the mounting point for all versioned API routers.

Key Responsibilities:
1. Lifespan Management: Initializes database connections and the task scheduler on startup.
2. Security: Implements API key validation and CORS policies for authorized frontend access.
3. Routing: Aggregates modular routers into a single cohesive API surface.
"""

import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Security, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

# Internal imports ensure the application context is correctly initialized
from app.config import get_settings, get_production_status
from app.core.scheduler import scheduler, setup_scheduler
from app.core.database import verify_tables_exist
from app.api.deps import get_api_key
from app.api.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's lifecycle events.
    
    Startup logic ensures the database is ready and the background scheduler is initialized.
    Shutdown logic ensures a clean exit by stopping the scheduler without waiting for 
    non-critical background tasks to complete, preventing hanging processes.
    """
    # ── Startup ──────────────────────────────────────────────
    logger.info("Initializing Lead Generation Automation API...")
    
    # Ensure database schema is present before accepting requests
    await verify_tables_exist()
    
    # Setup background task scheduling (Discovery, Qualification, Outreach)
    setup_scheduler()

    # NOTE: The system is designed to be extensible. While we currently use 
    # APScheduler for simplicity, the codebase retains structure compatible 
    # with Celery/Redis for future horizontal scaling requirements.

    yield

    # ── Shutdown ─────────────────────────────────────────────
    # Gracefully stop the scheduler to prevent orphaned tasks
    scheduler.shutdown(wait=False)
    logger.info("Application shutdown complete. Scheduler stopped.")

# Initialize FastAPI application with optimized metadata for OpenAPI/Swagger documentation
app = FastAPI(
    title="AI Lead Generation System",
    description=(
        "An autonomous pipeline designed to discover local business leads, "
        "qualify them using AI, and manage personalized outreach campaigns."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Configure Cross-Origin Resource Sharing (CORS)
# This is critical for allowing the Vite-based frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


from app.api.router import api_router
app.include_router(api_router, prefix="/api/v1")