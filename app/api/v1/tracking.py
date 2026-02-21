"""
Engagement tracking API endpoints.
Provides publicly accessible routes to process email pixel loads and hyperlink clicks,
facilitating closed-loop metrics on outreach effectiveness.
"""
from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import RedirectResponse
import base64
from app.core.database import get_db
from app.modules.tracking.pixel_tracker import TrackingService

router = APIRouter()

PIXEL_GIF = base64.b64decode("R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==")

@router.get("/track/open/{token}")
async def track_email_open(token: str, request: Request, db=Depends(get_db)):
    """
    HTTP GET endpoint corresponding to the embedded 1x1 tracking pixel.
    Synchronously registers an 'open' event and returns a transparent GIF to the client.
    
    Args:
        token (str): The cryptographic tracking identifier.
        request (Request): Client request context.
        db (AsyncSession): The injected database session dependency.
        
    Returns:
        Response: A binary image/gif response.
    """
    await TrackingService.log_event(db, token, "open", request)
    return Response(content=PIXEL_GIF, media_type="image/gif")

@router.get("/track/click/{token}")
async def track_email_click(token: str, url: str, request: Request, db=Depends(get_db)):
    """
    HTTP GET endpoint for wrapped hyperlink direction.
    Registers a 'click' event against the provided token before issuing 
    an HTTP 307 Temporary Redirect to the intended destination URL.
    
    Args:
        token (str): The cryptographic tracking identifier.
        url (str): The underlying destination URL.
        request (Request): Client request context.
        db (AsyncSession): The injected database session dependency.
        
    Returns:
        RedirectResponse: Standard redirection to the target URL.
    """
    await TrackingService.log_event(db, token, "click", request, url_clicked=url)
    return RedirectResponse(url=url)
