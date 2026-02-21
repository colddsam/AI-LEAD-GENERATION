"""
Main API router aggregation module.
Consolidates discrete API sub-routers (e.g., tracking, webhooks) into a singular 
application-level routing construct for FastAPI initialization.
"""
from fastapi import APIRouter
from app.api.v1 import tracking, webhooks

api_router = APIRouter()
api_router.include_router(tracking.router, tags=["tracking"])
api_router.include_router(webhooks.router, tags=["webhooks"])
