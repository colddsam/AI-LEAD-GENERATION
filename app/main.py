"""
Entry point for the AI Lead Generation System API.
Configures the FastAPI application, security dependencies, and core routers.
"""
from fastapi import FastAPI, Security, HTTPException, status, Depends
from fastapi.security.api_key import APIKeyHeader
from app.config import get_settings

app = FastAPI(
    title="AI Lead Generation System",
    description="Automated system to discover, qualify, and outreach to local businesses.",
    version="1.0.0"
)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


def get_current_settings():
    """
    Retrieves the current application settings using a cached provider.
    
    Returns:
        Settings: The current configuration settings instance.
    """
    return get_settings()


async def get_api_key(
    api_key_header: str = Security(api_key_header),
    settings = Depends(get_current_settings),
):
    """
    Validates the API key provided in the request header against the configured secret.

    Args:
        api_key_header (str): The API key extracted from the request headers.
        settings (Settings): The application settings dependency.

    Raises:
        HTTPException: If the provided API key is invalid or missing.

    Returns:
        str: The validated API key.
    """
    if api_key_header != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate API KEY"
        )
    return api_key_header


@app.get("/api/v1/health")
async def health_check(settings = Depends(get_current_settings)):
    """
    System health check endpoint to verify API availability and environment configuration.

    Args:
        settings (Settings): The application settings dependency.

    Returns:
        dict: A dictionary containing the system status, version, and environment context.
    """
    return {
        "status": "healthy",
        "version": app.version,
        "environment": settings.APP_ENV
    }


from app.api.router import api_router
app.include_router(api_router, prefix="/api/v1")