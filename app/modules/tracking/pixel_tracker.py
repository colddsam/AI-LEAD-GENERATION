from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import Request
import logging
from datetime import datetime

from app.models.email_event import EmailEvent
from app.models.campaign import EmailOutreach
from app.models.lead import Lead

logger = logging.getLogger(__name__)

class TrackingService:
    @staticmethod
    async def log_event(db: AsyncSession, token: str, event_type: str, request: Request, url_clicked: str = None) -> Lead:
        """
        Logs an email event (open, click) using the tracking token.
        Updates the lead and outreach status accordingly.
        Returns the associated Lead object.
        """
        try:
            # 1. Find the outreach record
            stmt = select(EmailOutreach).where(EmailOutreach.tracking_token == token)
            result = await db.execute(stmt)
            outreach = result.scalars().first()
            
            if not outreach:
                return None
                
            # 2. Find the lead
            lead_stmt = select(Lead).where(Lead.id == outreach.lead_id)
            lead_result = await db.execute(lead_stmt)
            lead = lead_result.scalars().first()
            
            if not lead:
                return None
                
            # 3. Create Event
            client_ip = request.client.host if request.client else None
            user_agent = request.headers.get("user-agent", "")
            
            event = EmailEvent(
                lead_id=outreach.lead_id,
                outreach_id=outreach.id,
                tracking_token=token,
                event_type=event_type,
                url_clicked=url_clicked,
                ip_address=client_ip,
                user_agent=user_agent
            )
            db.add(event)
            
            # 4. Update Lead & Outreach Status
            if event_type == "open":
                if lead.status == "email_sent":
                    lead.status = "opened"
                    lead.first_opened_at = datetime.utcnow()
                if outreach.status == "sent":
                    outreach.status = "delivered"
                    outreach.delivered_at = datetime.utcnow()
            
            elif event_type == "click":
                if lead.status in ["email_sent", "opened"]:
                    lead.status = "clicked"
                    lead.first_clicked_at = datetime.utcnow()
                    
            await db.commit()
            return lead
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error logging {event_type} event: {e}")
            return None
