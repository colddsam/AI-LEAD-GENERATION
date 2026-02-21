from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import RedirectResponse
import base64
from app.core.database import get_db
from app.modules.tracking.pixel_tracker import TrackingService

router = APIRouter()

# 1x1 transparent GIF base64 encoded
PIXEL_GIF = base64.b64decode("R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==")

@router.get("/track/open/{token}")
async def track_email_open(token: str, request: Request, db=Depends(get_db)):
    """
    Tracking pixel endpoint.
    Returns a 1x1 invisible GIF and logs the open event.
    """
    await TrackingService.log_event(db, token, "open", request)
    return Response(content=PIXEL_GIF, media_type="image/gif")

@router.get("/track/click/{token}")
async def track_email_click(token: str, url: str, request: Request, db=Depends(get_db)):
    """
    Click tracking endpoint.
    Logs the click event and redirects the user to the actual URL.
    """
    await TrackingService.log_event(db, token, "click", request, url_clicked=url)
    return RedirectResponse(url=url)
