import asyncio
from loguru import logger
from datetime import date, datetime
import uuid
import base64
import os
from celery import shared_task

from sqlalchemy import select, func, update
from app.core.database import get_session_maker
from app.models.lead import Lead, TargetLocation
from app.models.campaign import Campaign, EmailOutreach
from app.models.email_event import EmailEvent
from app.models.daily_report import DailyReport
from app.config import get_settings
settings = get_settings()

from app.modules.notifications.telegram_bot import send_telegram_alert
from app.modules.discovery.google_places import GooglePlacesClient
from app.modules.discovery.scraper import scrape_contact_email
from app.modules.qualification.scorer import qualify_lead
from app.modules.personalization.groq_client import GroqClient
from app.modules.personalization.email_generator import render_email_html
from app.modules.personalization.pdf_generator import generate_proposal_pdf
from app.modules.outreach.email_sender import send_email
from app.modules.tracking.reply_tracker import fetch_recent_replies
from app.modules.reporting.excel_builder import generate_daily_report_excel
from app.modules.reporting.email_reporter import send_daily_report_email

def run_async(coro):
    """Utility to run async functions blockingly inside Celery tasks."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


async def _do_discovery():
    """Fetches places from Google API and saves new valid leads."""
    logger.info("Starting Discovery")
    discovered_count = 0
    client = GooglePlacesClient()
    
    async with get_session_maker()() as db:
        stmt = select(TargetLocation).where(TargetLocation.is_active == True)
        result = await db.execute(stmt)
        locations = result.scalars().all()
        
        for loc in locations:
            for category in loc.categories:
                places = await client.search_places(loc.city, category, loc.radius_meters)
                for place in places:
                    # Check if exists
                    check_stmt = select(Lead).where(Lead.place_id == place["id"])
                    check_result = await db.execute(check_stmt)
                    if check_result.scalars().first():
                        continue
                    
                    # Try to scrape email if website is found
                    website_url = place.get("websiteUri")
                    email = None
                    if website_url:
                        email = await scrape_contact_email(website_url)
                        
                    lead = Lead(
                        place_id=place["id"],
                        business_name=place.get("displayName", {}).get("text", "Unknown"),
                        category=category,
                        address=place.get("formattedAddress"),
                        city=loc.city,
                        phone=place.get("nationalPhoneNumber"),
                        website_url=website_url,
                        google_maps_url=place.get("googleMapsUri"),
                        rating=place.get("rating"),
                        review_count=place.get("userRatingCount"),
                        email=email,
                        status="discovered"
                    )
                    db.add(lead)
                    discovered_count += 1
        
        if discovered_count > 0:
            await db.commit()
            await send_telegram_alert(f"🔍 Discovery found {discovered_count} new local businesses!")


async def _do_qualification():
    """Scores discovered leads and filters those that need digital presence."""
    logger.info("Starting Qualification")
    qualified_count = 0
    
    async with get_session_maker()() as db:
        stmt = select(Lead).where(Lead.status == "discovered")
        result = await db.execute(stmt)
        leads = result.scalars().all()
        
        for lead in leads:
            is_qualified, score, notes = await qualify_lead(lead)
            lead.qualification_score = score
            lead.web_presence_notes = notes
            
            if is_qualified and lead.email: # Must have email to be useful
                lead.status = "qualified"
                lead.qualified_at = datetime.utcnow()
                qualified_count += 1
            else:
                lead.status = "rejected"
        
        if leads:
            await db.commit()
            if qualified_count > 0:
                await send_telegram_alert(f"🎯 Qualified {qualified_count} hot leads ready for outreach!")


def _generate_tracking_token(lead_id, campaign_id):
    """Generates unique base64 tracking token"""
    raw_token = f"{lead_id}_{campaign_id}"
    return base64.urlsafe_b64encode(raw_token.encode()).decode('utf-8')


async def _do_personalization():
    """Generates personalized AI emails and PDFs for qualified leads."""
    logger.info("Starting Personalization")
    pers_count = 0
    groq_client = GroqClient()
    
    async with get_session_maker()() as db:
        # Check active campaign or create new
        today = date.today()
        camp_stmt = select(Campaign).where(Campaign.campaign_date == today).limit(1)
        camp_res = await db.execute(camp_stmt)
        campaign = camp_res.scalars().first()
        
        if not campaign:
            campaign = Campaign(name=f"Daily Outreach {today}", campaign_date=today)
            db.add(campaign)
            await db.flush()
            
        stmt = select(Lead).where(Lead.status == "qualified")
        result = await db.execute(stmt)
        leads = result.scalars().all()
        
        for lead in leads:
            # 1. AI content
            ai_data = await groq_client.generate_email_content({
                "business_name": lead.business_name,
                "category": lead.category,
                "location": lead.city,
                "rating": lead.rating,
                "review_count": lead.review_count,
                "web_presence_notes": lead.web_presence_notes
            })
            
            # 2. PDF Proposal
            pdf_path = generate_proposal_pdf(
                business_name=lead.business_name,
                category=lead.category,
                benefits=ai_data.get('benefits', []),
                output_filename=f"Proposal_{lead.id}.pdf"
            )
            
            # 3. Create Outreach Queue Record
            tracking_token = _generate_tracking_token(lead.id, campaign.id)
            html_body = render_email_html(
                {"business_name": lead.business_name}, 
                ai_data.get('body_html', ''), 
                tracking_token, 
                settings.APP_URL
            )
            
            outreach = EmailOutreach(
                lead_id=lead.id,
                campaign_id=campaign.id,
                to_email=lead.email,
                subject=ai_data.get('subject', f"Digital Growth for {lead.business_name}"),
                body_html=html_body,
                tracking_token=tracking_token,
                ai_generated=True,
                has_attachment=True,
                attachment_names=[pdf_path],
                status="queued"
            )
            db.add(outreach)
            
            campaign.total_leads += 1
            lead.status = "queued_for_send"
            pers_count += 1
            
        if leads:
            await db.commit()
            if pers_count > 0:
                await send_telegram_alert(f"🤖 AI Personalized {pers_count} proposals. Ready to send!")


async def _do_outreach():
    """Dispatches all queued emails."""
    logger.info("Starting Outreach Dispatch")
    sent_count = 0
    
    async with get_session_maker()() as db:
        stmt = select(EmailOutreach).where(EmailOutreach.status == "queued")
        result = await db.execute(stmt)
        queued_emails = result.scalars().all()
        
        for email_task in queued_emails:
            attachments = email_task.attachment_names if email_task.has_attachment else []
            success = await send_email(
                to_email=email_task.to_email,
                subject=email_task.subject,
                html_content=email_task.body_html,
                attachment_paths=attachments
            )
            
            if success:
                email_task.status = "sent"
                email_task.sent_at = datetime.utcnow()
                sent_count += 1
                
                # Update lead
                l_stmt = select(Lead).where(Lead.id == email_task.lead_id)
                l_res = await db.execute(l_stmt)
                lead = l_res.scalars().first()
                if lead:
                    lead.status = "email_sent"
                    lead.email_sent_at = datetime.utcnow()
                    
                # Clean up PDF if needed
                for att in attachments:
                    if os.path.exists(att):
                        os.remove(att)
            else:
                email_task.status = "failed"
                
            # Slow down to avoid spam filters (optional if running synchronously)
            await asyncio.sleep(2)
            
        if queued_emails:
            await db.commit()
            if sent_count > 0:
                await send_telegram_alert(f"✉️ Outreach Complete: Sent {sent_count} emails.")


async def _do_reply_polling():
    """Polls IMAP for direct replies."""
    logger.info("Polling for replies")
    replies = await fetch_recent_replies(since_minutes=30)
    
    async with get_session_maker()() as db:
        for sender_email, subject in replies:
            # Find matching lead
            stmt = select(Lead).where(Lead.email == sender_email).order_by(Lead.created_at.desc()).limit(1)
            res = await db.execute(stmt)
            lead = res.scalars().first()
            
            if lead and lead.status != "replied":
                lead.status = "replied"
                lead.first_replied_at = datetime.utcnow()
                await send_telegram_alert(f"🚨 REPLY RECEIVED!\nBusiness: {lead.business_name}\nEmail: {lead.email}\nSubject: {subject}")
                await db.commit()


async def _do_daily_report():
    """Generates and sends the daily Excel report."""
    logger.info("Generating Daily Report")
    today = date.today()
    
    async with get_session_maker()() as db:
        camp_stmt = select(Campaign).where(Campaign.campaign_date == today).limit(1)
        camp_res = await db.execute(camp_stmt)
        campaign = camp_res.scalars().first()
        
        if not campaign:
            return # Nothing happened today
            
        report_data = {
            "leads_discovered": await db.scalar(select(func.count(Lead.id)).where(func.date(Lead.discovered_at) == today)),
            "leads_qualified": await db.scalar(select(func.count(Lead.id)).where(func.date(Lead.qualified_at) == today)),
            "emails_sent": await db.scalar(select(func.count(EmailOutreach.id)).where(func.date(EmailOutreach.sent_at) == today)),
            "emails_opened": await db.scalar(select(func.count(EmailEvent.id)).where((func.date(EmailEvent.occurred_at) == today) & (EmailEvent.event_type == 'open'))),
            "links_clicked": await db.scalar(select(func.count(EmailEvent.id)).where((func.date(EmailEvent.occurred_at) == today) & (EmailEvent.event_type == 'click'))),
            "replies_received": await db.scalar(select(func.count(Lead.id)).where(func.date(Lead.first_replied_at) == today))
        }
        
        # Save to DB report
        db_report = DailyReport(
            report_date=today,
            total_leads_discovered=report_data["leads_discovered"],
            total_qualified_leads=report_data["leads_qualified"],
            emails_sent=report_data["emails_sent"],
            emails_opened=report_data["emails_opened"],
            links_clicked=report_data["links_clicked"],
            replies_received=report_data["replies_received"]
        )
        db.add(db_report)
        
        # Get active leads for excel
        leads_stmt = select(Lead).where(
            (func.date(Lead.discovered_at) == today) | 
            (Lead.status.in_(["email_sent", "opened", "clicked", "replied"]))
        )
        leads_res = await db.execute(leads_stmt)
        leads = leads_res.scalars().all()
        
        lead_dicts = [{
            "business_name": l.business_name,
            "category": l.category,
            "city": l.city,
            "email_sent_at": l.email_sent_at,
            "first_opened_at": l.first_opened_at,
            "first_clicked_at": l.first_clicked_at,
            "first_replied_at": l.first_replied_at,
            "status": l.status,
            "phone": l.phone,
            "google_maps_url": l.google_maps_url
        } for l in leads]
        
        excel_path = generate_daily_report_excel(report_data, lead_dicts, today)
        
        await send_daily_report_email(report_data, excel_path, today)
        await db.commit()

# Celery Shared Tasks Wrapper

@shared_task(name="app.tasks.daily_pipeline.run_discovery_task")
def run_discovery_task():
    logger.info("Executing Discovery Task via Celery")
    try:
        run_async(_do_discovery())
    except Exception as e:
        logger.error(f"Discovery Failed: {e}")
        run_async(send_telegram_alert(f"❌ Pipeline Error (Discovery): {e}"))

@shared_task(name="app.tasks.daily_pipeline.run_qualification_task")
def run_qualification_task():
    logger.info("Executing Qualification Task via Celery")
    try:
        run_async(_do_qualification())
    except Exception as e:
        logger.error(f"Qualification Failed: {e}")
        run_async(send_telegram_alert(f"❌ Pipeline Error (Qualification): {e}"))

@shared_task(name="app.tasks.daily_pipeline.run_personalization_task")
def run_personalization_task():
    logger.info("Executing Personalization Task via Celery")
    try:
        run_async(_do_personalization())
    except Exception as e:
        logger.error(f"Personalization Failed: {e}")
        run_async(send_telegram_alert(f"❌ Pipeline Error (Personalization): {e}"))

@shared_task(name="app.tasks.daily_pipeline.run_outreach_send_task")
def run_outreach_send_task():
    logger.info("Executing Outreach Task via Celery")
    try:
        run_async(_do_outreach())
    except Exception as e:
        logger.error(f"Outreach Failed: {e}")
        run_async(send_telegram_alert(f"❌ Pipeline Error (Outreach): {e}"))

@shared_task(name="app.tasks.daily_pipeline.run_reply_polling_task")
def run_reply_polling_task():
    logger.info("Executing Reply Polling Task via Celery")
    try:
        run_async(_do_reply_polling())
    except Exception as e:
        logger.error(f"Reply Polling Failed: {e}")
        run_async(send_telegram_alert(f"❌ Pipeline Error (Reply Polling): {e}"))

@shared_task(name="app.tasks.daily_pipeline.run_daily_report_task")
def run_daily_report_task():
    logger.info("Executing Daily Report Task via Celery")
    try:
        run_async(_do_daily_report())
    except Exception as e:
        logger.error(f"Daily Report Failed: {e}")
        run_async(send_telegram_alert(f"❌ Pipeline Error (Daily Report): {e}"))

@shared_task(name="app.tasks.daily_pipeline.run_manual_full_pipeline")
def run_manual_full_pipeline():
    """Manually run all steps sequentially (for testing)"""
    logger.info("Running full manual pipeline...")
    try:
        run_async(_do_discovery())
        run_async(_do_qualification())
        run_async(_do_personalization())
        run_async(_do_outreach())
        run_async(_do_daily_report())
    except Exception as e:
        logger.error(f"Manual Pipeline Failed: {e}")
        run_async(send_telegram_alert(f"❌ Pipeline Error (Manual Run): {e}"))
