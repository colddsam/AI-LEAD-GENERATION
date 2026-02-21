from fastapi import FastAPI, Depends, Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.config import settings

app = FastAPI(
    title="AI Lead Generation System",
    description="Automated system to discover, qualify, and outreach to local businesses.",
    version="1.0.0"
)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate API KEY"
        )
    return api_key_header

@app.get("/api/v1/health")
async def health_check():
    """System health check endpoint"""
    return {
        "status": "healthy",
        "version": app.version,
        "environment": settings.APP_ENV
    }

from app.api.router import api_router
app.include_router(api_router, prefix="/api/v1")
