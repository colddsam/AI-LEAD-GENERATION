"""
Cold Scout OSS — Pipeline Orchestrator
5 stages: Discovery, Qualification, Personalization, Outreach, Reporting.
No threads. No auth. Legacy logic only.
"""
import asyncio
import hashlib
import base64
import os
from datetime import date, datetime, timedelta
from loguru import logger

from sqlalchemy import select, func
from app.database import SessionLocal
from app.models.lead import Lead, SearchHistory
from app.models.campaign import Campaign, EmailOutreach
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
from app.modules.reporting.excel_builder import generate_daily_report_excel


# ── Stage 1: Discovery ──────────────────────────────────────────────────────

async def run_discovery_stage():
    logger.info("Starting Discovery Stage")
    discovered_count = 0
    client = GooglePlacesClient()
    groq_client = GroqClient()
    seen_place_ids: set = set()
    today = date.today()

    async with SessionLocal() as db:
        try:
            # Ensure daily report exists
            report_res = await db.execute(select(DailyReport).where(DailyReport.report_date == today))
            db_report = report_res.scalars().first()
            if not db_report:
                db_report = DailyReport(report_date=today, pipeline_status="running", pipeline_started_at=datetime.utcnow())
                db.add(db_report)
            else:
                db_report.pipeline_status = "running"
                db_report.pipeline_started_at = datetime.utcnow()
            await db.flush()

            # Get recent search history to avoid duplicates
            sixty_days_ago = datetime.utcnow() - timedelta(days=60)
            hist_res = await db.execute(select(SearchHistory).where(SearchHistory.created_at >= sixty_days_ago))
            recent = hist_res.scalars().all()
            exclude_cities = list({h.city for h in recent})
            exclude_categories = list({h.category for h in recent})

            targets = await groq_client.generate_daily_targets(exclude_cities, exclude_categories)
            logger.info(f"Targets: {targets}")

            for target in targets:
                city = target.get("city")
                category = target.get("category")
                if not city or not category:
                    continue

                places = await client.search_places(city, category, 5000)
                db.add(SearchHistory(city=city, category=category))

                if not places:
                    continue

                batch_ids = [p["id"] for p in places]
                existing_res = await db.execute(select(Lead.place_id).where(Lead.place_id.in_(batch_ids)))
                existing_ids = set(existing_res.scalars().all())

                for place in places:
                    place_id = place["id"]
                    if place_id in seen_place_ids or place_id in existing_ids:
                        continue
                    seen_place_ids.add(place_id)

                    website_url = place.get("websiteUri")
                    email = None
                    if website_url:
                        email = await scrape_contact_email(website_url)

                    if email:
                        dup = await db.execute(select(Lead).where(Lead.email == email))
                        if dup.scalars().first():
                            continue

                    lead = Lead(
                        place_id=place["id"],
                        business_name=place.get("displayName", {}).get("text", "Unknown"),
                        category=category, address=place.get("formattedAddress"),
                        city=city, phone=place.get("nationalPhoneNumber"),
                        website_url=website_url, google_maps_url=place.get("googleMapsUri"),
                        rating=place.get("rating"), review_count=place.get("userRatingCount"),
                        email=email, status="discovered", raw_places_data=place,
                    )
                    db.add(lead)
                    discovered_count += 1

            db_report.pipeline_status = "completed"
            db_report.pipeline_ended_at = datetime.utcnow()
            await db.commit()

            if discovered_count > 0:
                await send_telegram_alert(f"Discovery: {discovered_count} new leads found (Targets: {targets})")

        except Exception as e:
            logger.exception("Discovery stage failed")
            await db.rollback()
            try:
                db_report.pipeline_status = "failed"
                db_report.error_log = str(e)
                await db.commit()
            except Exception:
                pass
            raise

    return {"discovered": discovered_count}


# ── Stage 2: Qualification ───────────────────────────────────────────────────

async def run_qualification_stage():
    logger.info("Starting Qualification Stage")
    qualified_count = 0
    phone_qualified_count = 0

    async with SessionLocal() as db:
        result = await db.execute(select(Lead).where(Lead.status == "discovered"))
        leads = result.scalars().all()

        for lead in leads:
            try:
                is_qualified, score, notes = await qualify_lead(lead, db)
                lead.ai_score = score
                lead.qualification_notes = notes

                if is_qualified and lead.email:
                    lead.status = "qualified"
                    lead.qualified_at = datetime.utcnow()
                    qualified_count += 1
                elif is_qualified and lead.phone and not lead.email:
                    lead.status = "phone_qualified"
                    lead.qualified_at = datetime.utcnow()
                    phone_qualified_count += 1
                else:
                    lead.status = "rejected"
            except Exception as e:
                logger.error(f"Qualification failed for {lead.business_name}: {e}")
                lead.status = "rejected"

        if leads:
            await db.commit()

        if qualified_count > 0 or phone_qualified_count > 0:
            await send_telegram_alert(f"Qualification: {qualified_count} email, {phone_qualified_count} phone qualified")

    return {"qualified": qualified_count, "phone_qualified": phone_qualified_count}


# ── Stage 3: Personalization ─────────────────────────────────────────────────

def _generate_tracking_token(lead_id, campaign_id) -> str:
    payload = f"{lead_id}_{campaign_id}"
    sig = hashlib.sha256(payload.encode()).digest()
    b64_payload = base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")
    b64_sig = base64.urlsafe_b64encode(sig).decode().rstrip("=")
    return f"{b64_payload}.{b64_sig}"


async def run_personalization_stage():
    logger.info("Starting Personalization Stage")
    pers_count = 0
    groq_client = GroqClient()

    async with SessionLocal() as db:
        today = date.today()
        camp_res = await db.execute(select(Campaign).where(Campaign.campaign_date == today).limit(1))
        campaign = camp_res.scalars().first()
        if not campaign:
            campaign = Campaign(name=f"Daily Outreach {today}", campaign_date=today)
            db.add(campaign)
            await db.flush()

        result = await db.execute(select(Lead).where(Lead.status == "qualified"))
        leads = result.scalars().all()

        for lead in leads:
            try:
                # AI email generation
                ai_data = await groq_client.generate_email_content({
                    "business_name": lead.business_name,
                    "category": lead.category,
                    "location": lead.city,
                    "rating": lead.rating,
                    "review_count": lead.review_count,
                    "qualification_notes": lead.qualification_notes,
                })

                # PDF proposal
                pdf_path = generate_proposal_pdf(
                    business_name=lead.business_name, category=lead.category,
                    benefits=ai_data.get('benefits', []),
                    output_filename=f"Proposal_{lead.id}.pdf",
                    rating=lead.rating, review_count=lead.review_count,
                    city=lead.city, qualification_notes=lead.qualification_notes,
                )

                # Email HTML
                tracking_token = _generate_tracking_token(lead.id, campaign.id)
                html_body = render_email_html(
                    {"business_name": lead.business_name},
                    ai_data.get('body_html', ''),
                    tracking_token,
                )

                attachments = [pdf_path] if pdf_path else []
                outreach = EmailOutreach(
                    lead_id=lead.id, campaign_id=campaign.id,
                    to_email=lead.email, subject=ai_data.get('subject', f"Digital Growth for {lead.business_name}"),
                    body_html=html_body, tracking_token=tracking_token,
                    ai_generated=True, has_attachment=bool(attachments),
                    attachment_names=attachments, status="queued",
                )
                db.add(outreach)
                campaign.total_leads += 1
                lead.status = "queued_for_send"
                pers_count += 1

            except Exception as e:
                logger.error(f"Personalization failed for {lead.business_name}: {e}")

        if leads:
            await db.commit()
            if pers_count > 0:
                await send_telegram_alert(f"Personalization: {pers_count} proposals queued")

    return {"personalized": pers_count}


# ── Stage 4: Outreach ────────────────────────────────────────────────────────

async def run_outreach_stage():
    logger.info("Starting Outreach Stage")
    sent_count = 0

    async with SessionLocal() as db:
        result = await db.execute(select(EmailOutreach).where(EmailOutreach.status == "queued"))
        queued = result.scalars().all()

        for email_task in queued:
            attachments = email_task.attachment_names if email_task.has_attachment else []
            try:
                success = await send_email(
                    to_email=email_task.to_email,
                    subject=email_task.subject,
                    html_content=email_task.body_html,
                    attachment_paths=attachments,
                )
                if success:
                    email_task.status = "sent"
                    email_task.sent_at = datetime.utcnow()
                    sent_count += 1

                    lead_res = await db.execute(select(Lead).where(Lead.id == email_task.lead_id))
                    lead = lead_res.scalars().first()
                    if lead:
                        lead.status = "email_sent"
                        lead.email_sent_at = datetime.utcnow()

                    camp_res = await db.execute(select(Campaign).where(Campaign.id == email_task.campaign_id))
                    camp = camp_res.scalars().first()
                    if camp:
                        camp.emails_sent += 1
                        if camp.status == "pending":
                            camp.status = "active"
                            camp.started_at = datetime.utcnow()

                    await db.commit()
                else:
                    email_task.status = "failed"
            except Exception as e:
                logger.error(f"Outreach failed for {email_task.to_email}: {e}")
                email_task.status = "failed"
            finally:
                if attachments:
                    for att in attachments:
                        if os.path.exists(att):
                            try:
                                os.remove(att)
                            except Exception:
                                pass
            await asyncio.sleep(2)

        if queued:
            await db.commit()
            if sent_count > 0:
                await send_telegram_alert(f"Outreach: {sent_count} emails sent")

    return {"sent": sent_count}


# ── Stage 5: Daily Report ────────────────────────────────────────────────────

async def generate_daily_report():
    logger.info("Generating Daily Report")
    today = date.today()

    async with SessionLocal() as db:
        leads_discovered = await db.scalar(
            select(func.count(Lead.id)).where(func.date(Lead.discovered_at) == today)
        ) or 0
        leads_qualified = await db.scalar(
            select(func.count(Lead.id)).where(
                (func.date(Lead.qualified_at) == today) &
                Lead.status.in_(["qualified", "phone_qualified"])
            )
        ) or 0
        emails_sent = await db.scalar(
            select(func.count(EmailOutreach.id)).where(
                (func.date(EmailOutreach.sent_at) == today) &
                (EmailOutreach.status == "sent")
            )
        ) or 0

        leads_res = await db.execute(
            select(Lead).where(
                (func.date(Lead.discovered_at) == today) |
                (func.date(Lead.email_sent_at) == today)
            )
        )
        report_leads = leads_res.scalars().all()

        report_data = {
            "leads_discovered": leads_discovered,
            "leads_qualified": leads_qualified,
            "emails_sent": emails_sent,
            "emails_opened": 0,
            "links_clicked": 0,
            "replies_received": 0,
        }

        lead_dicts = [
            {
                "business_name": l.business_name, "category": l.category,
                "city": l.city, "status": l.status, "phone": l.phone,
                "email_sent_at": l.email_sent_at, "google_maps_url": l.google_maps_url,
            }
            for l in report_leads
        ]

        excel_path = generate_daily_report_excel(report_data, lead_dicts, today)

        # Email report to admin
        if settings.ADMIN_EMAIL and settings.BREVO_SMTP_USER:
            try:
                from app.modules.outreach.email_sender import send_email as send_report
                html = f"""
                <html><body style="font-family:sans-serif;background:#f5f5f5;margin:0;padding:0;">
                <div style="max-width:560px;margin:32px auto;background:#fff;border:1px solid #eaeaea;border-radius:12px;overflow:hidden;">
                <div style="background:#000;padding:24px 32px;"><h1 style="color:#fff;margin:0;font-size:20px;">Cold Scout Report — {today}</h1></div>
                <div style="padding:24px 32px;">
                <p>Discovered: <b>{leads_discovered}</b> | Qualified: <b>{leads_qualified}</b> | Sent: <b>{emails_sent}</b></p>
                <p style="color:#666;font-size:13px;">Excel report attached.</p>
                </div></div></body></html>"""
                await send_report(settings.ADMIN_EMAIL, f"[Cold Scout] Daily Report — {today}", html, [excel_path])
            except Exception as e:
                logger.error(f"Failed to email report: {e}")

        await db.commit()

    return {"report_date": str(today), "excel": excel_path, **report_data}


# ── Full Pipeline ────────────────────────────────────────────────────────────

async def run_full_pipeline():
    logger.info("Running full pipeline")
    results = {}
    results["discovery"] = await run_discovery_stage()
    results["qualification"] = await run_qualification_stage()
    results["personalization"] = await run_personalization_stage()
    results["outreach"] = await run_outreach_stage()
    results["report"] = await generate_daily_report()
    return results
