"""
Main API router aggregation module.
Consolidates API sub-routers into a single app routing construct.
"""
from fastapi import APIRouter
from app.api.v1 import tracking, webhooks

api_router = APIRouter()
api_router.include_router(tracking.router, tags=["tracking"])
api_router.include_router(webhooks.router, tags=["webhooks"])
