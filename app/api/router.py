"""
Main API router aggregation module.
Consolidates API sub-routers into a single app routing construct.
"""
from fastapi import APIRouter
from app.api.v1 import tracking, webhooks, pipeline, leads, campaigns, reports, unsubscribe

api_router = APIRouter()
api_router.include_router(tracking.router, tags=["tracking"])
api_router.include_router(webhooks.router, tags=["webhooks"])
api_router.include_router(pipeline.router, tags=["pipeline"])
api_router.include_router(leads.router, tags=["leads"])
api_router.include_router(campaigns.router, tags=["campaigns"])
api_router.include_router(reports.router, tags=["reports"])
api_router.include_router(unsubscribe.router)
