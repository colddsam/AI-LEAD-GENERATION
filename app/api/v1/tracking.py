"""
Engagement tracking API endpoints.
Provides routes to process email pixel loads and link clicks.
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
    HTTP GET endpoint for the embedded 1x1 tracking pixel.
    Registers an 'open' event and returns a transparent GIF.
    """
    await TrackingService.log_event(db, token, "open", request)
    return Response(content=PIXEL_GIF, media_type="image/gif")

@router.get("/track/click/{token}")
async def track_email_click(token: str, url: str, request: Request, db=Depends(get_db)):
    """
    HTTP GET endpoint for wrapped hyperlink redirection.
    Registers a 'click' event before issuing an HTTP 307 Redirect.
    """
    await TrackingService.log_event(db, token, "click", request, url_clicked=url)
    return RedirectResponse(url=url)
