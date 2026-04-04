"""
Cold Scout OSS — Self-Hosted Lead Generation Server
No auth. No threads. User-provided API keys.
"""
import asyncio
import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import get_settings
from app.database import init_db, SessionLocal
from app.pipeline import (
    run_discovery_stage,
    run_qualification_stage,
    run_personalization_stage,
    run_outreach_stage,
    generate_daily_report,
    run_full_pipeline,
)

settings = get_settings()
scheduler = AsyncIOScheduler()

# Track pipeline state for the dashboard
pipeline_state = {
    "status": "idle",
    "last_run": None,
    "last_result": None,
    "scheduler_running": False,
}


def _schedule_jobs():
    """Register pipeline stages on the APScheduler."""
    scheduler.add_job(
        lambda: asyncio.ensure_future(run_discovery_stage()),
        "cron", hour=settings.DISCOVERY_HOUR, minute=0, id="discovery",
        replace_existing=True,
    )
    scheduler.add_job(
        lambda: asyncio.ensure_future(run_qualification_stage()),
        "cron", hour=settings.QUALIFICATION_HOUR, minute=0, id="qualification",
        replace_existing=True,
    )
    scheduler.add_job(
        lambda: asyncio.ensure_future(run_personalization_stage()),
        "cron", hour=settings.PERSONALIZATION_HOUR, minute=0, id="personalization",
        replace_existing=True,
    )
    scheduler.add_job(
        lambda: asyncio.ensure_future(run_outreach_stage()),
        "cron", hour=settings.OUTREACH_HOUR, minute=0, id="outreach",
        replace_existing=True,
    )
    scheduler.add_job(
        lambda: asyncio.ensure_future(generate_daily_report()),
        "cron", hour=settings.REPORT_HOUR, minute=settings.REPORT_MINUTE, id="daily_report",
        replace_existing=True,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Cold Scout OSS starting up...")
    await init_db()
    _schedule_jobs()
    scheduler.start()
    pipeline_state["scheduler_running"] = True
    logger.info("Scheduler started with pipeline jobs.")
    yield
    scheduler.shutdown()
    pipeline_state["scheduler_running"] = False
    logger.info("Cold Scout OSS shutting down.")


app = FastAPI(
    title="Cold Scout OSS",
    description="Self-hosted lead generation pipeline — free tier",
    version="1.0.0",
    lifespan=lifespan,
)


# ── API Endpoints ────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/status")
async def status():
    jobs = []
    if scheduler.running:
        for job in scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
            })

    from sqlalchemy import select, func
    from app.models.lead import Lead
    from app.models.campaign import EmailOutreach

    async with SessionLocal() as db:
        total_leads = await db.scalar(select(func.count(Lead.id))) or 0
        qualified = await db.scalar(select(func.count(Lead.id)).where(Lead.status.in_(["qualified", "phone_qualified"]))) or 0
        sent = await db.scalar(select(func.count(EmailOutreach.id)).where(EmailOutreach.status == "sent")) or 0

    return {
        "pipeline": pipeline_state,
        "scheduler_running": scheduler.running,
        "jobs": jobs,
        "stats": {"total_leads": total_leads, "qualified": qualified, "emails_sent": sent},
    }


@app.post("/api/pipeline/trigger/{stage}")
async def trigger_stage(stage: str):
    valid = {
        "all": run_full_pipeline,
        "discovery": run_discovery_stage,
        "qualification": run_qualification_stage,
        "personalization": run_personalization_stage,
        "outreach": run_outreach_stage,
        "report": generate_daily_report,
    }
    if stage not in valid:
        return JSONResponse({"error": f"Invalid stage. Choose: {list(valid.keys())}"}, 400)

    pipeline_state["status"] = f"running:{stage}"

    async def _run():
        try:
            result = await valid[stage]()
            pipeline_state["status"] = "idle"
            pipeline_state["last_run"] = datetime.utcnow().isoformat()
            pipeline_state["last_result"] = result
        except Exception as e:
            pipeline_state["status"] = f"error:{stage}"
            pipeline_state["last_result"] = {"error": str(e)}
            logger.exception(f"Pipeline stage {stage} failed")

    asyncio.create_task(_run())
    return {"status": "triggered", "stage": stage, "triggered_at": datetime.utcnow().isoformat()}


@app.post("/api/scheduler/pause")
async def pause_scheduler():
    for job in scheduler.get_jobs():
        scheduler.pause_job(job.id)
    pipeline_state["status"] = "paused"
    return {"status": "paused"}


@app.post("/api/scheduler/resume")
async def resume_scheduler():
    for job in scheduler.get_jobs():
        scheduler.resume_job(job.id)
    pipeline_state["status"] = "idle"
    return {"status": "resumed"}


@app.get("/api/leads")
async def list_leads(status: str = None, limit: int = 50, offset: int = 0):
    from sqlalchemy import select
    from app.models.lead import Lead

    async with SessionLocal() as db:
        query = select(Lead).order_by(Lead.created_at.desc()).limit(limit).offset(offset)
        if status:
            query = query.where(Lead.status == status)
        result = await db.execute(query)
        leads = result.scalars().all()

    return [
        {
            "id": l.id, "business_name": l.business_name, "category": l.category,
            "city": l.city, "email": l.email, "phone": l.phone,
            "rating": l.rating, "review_count": l.review_count,
            "ai_score": l.ai_score, "lead_tier": l.lead_tier,
            "status": l.status, "website_url": l.website_url,
            "google_maps_url": l.google_maps_url,
            "discovered_at": l.discovered_at.isoformat() if l.discovered_at else None,
        }
        for l in leads
    ]


@app.get("/api/config")
async def get_config():
    """Show current schedule config (no secrets exposed)."""
    return {
        "discovery_hour": settings.DISCOVERY_HOUR,
        "qualification_hour": settings.QUALIFICATION_HOUR,
        "personalization_hour": settings.PERSONALIZATION_HOUR,
        "outreach_hour": settings.OUTREACH_HOUR,
        "report_hour": settings.REPORT_HOUR,
        "report_minute": settings.REPORT_MINUTE,
        "groq_model": settings.GROQ_MODEL,
        "has_google_key": bool(settings.GOOGLE_PLACES_API_KEY),
        "has_groq_key": bool(settings.GROQ_API_KEY),
        "has_smtp": bool(settings.BREVO_SMTP_USER),
        "has_telegram": bool(settings.TELEGRAM_BOT_TOKEN),
    }


# ── Status Dashboard (HTML) ─────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return DASHBOARD_HTML


DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cold Scout OSS — Dashboard</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #fafafa; color: #000; }
    .header { background: #000; color: #fff; padding: 24px 32px; }
    .header h1 { font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }
    .header p { font-size: 12px; color: #888; margin-top: 4px; letter-spacing: 1px; text-transform: uppercase; }
    .container { max-width: 900px; margin: 0 auto; padding: 24px 16px; }
    .card { background: #fff; border: 1px solid #eaeaea; border-radius: 12px; padding: 24px; margin-bottom: 16px; }
    .card h2 { font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #666; margin-bottom: 16px; }
    .stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; }
    .stat { background: #f5f5f5; border-radius: 8px; padding: 16px; text-align: center; }
    .stat .value { font-size: 28px; font-weight: 800; letter-spacing: -1px; }
    .stat .label { font-size: 11px; color: #666; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
    .status-badge { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
    .status-idle { background: #e8f5e9; color: #2e7d32; }
    .status-running { background: #fff3e0; color: #e65100; }
    .status-error { background: #ffebee; color: #c62828; }
    .status-paused { background: #f3e5f5; color: #6a1b9a; }
    .btn-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
    .btn { padding: 8px 16px; border: 1px solid #000; border-radius: 8px; background: #fff; color: #000; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.15s; }
    .btn:hover { background: #000; color: #fff; }
    .btn.primary { background: #000; color: #fff; }
    .btn.primary:hover { background: #333; }
    .btn.danger { border-color: #c62828; color: #c62828; }
    .btn.danger:hover { background: #c62828; color: #fff; }
    .jobs-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 12px; }
    .jobs-table th { text-align: left; padding: 8px 12px; background: #000; color: #fff; font-weight: 600; font-size: 11px; letter-spacing: 0.5px; }
    .jobs-table td { padding: 8px 12px; border-bottom: 1px solid #eaeaea; }
    .jobs-table tr:nth-child(even) { background: #fafafa; }
    .leads-table { width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 12px; }
    .leads-table th { text-align: left; padding: 6px 10px; background: #000; color: #fff; font-size: 10px; letter-spacing: 0.5px; text-transform: uppercase; }
    .leads-table td { padding: 6px 10px; border-bottom: 1px solid #f0f0f0; }
    .leads-table tr:nth-child(even) { background: #fafafa; }
    .tier-A { color: #2e7d32; font-weight: 700; }
    .tier-B { color: #1565c0; font-weight: 700; }
    .tier-C { color: #e65100; font-weight: 600; }
    .tier-D { color: #999; }
    .config-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 13px; }
    .config-item { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #f0f0f0; }
    .config-item .key { color: #666; }
    .config-item .val { font-weight: 600; }
    .check { color: #2e7d32; }
    .cross { color: #c62828; }
    .log { background: #111; color: #0f0; font-family: monospace; font-size: 12px; padding: 16px; border-radius: 8px; max-height: 200px; overflow-y: auto; margin-top: 12px; }
    #toast { position: fixed; bottom: 24px; right: 24px; background: #000; color: #fff; padding: 12px 20px; border-radius: 8px; font-size: 13px; display: none; z-index: 999; }
  </style>
</head>
<body>
  <div class="header">
    <h1>Cold Scout OSS</h1>
    <p>Self-Hosted Lead Generation Dashboard</p>
  </div>

  <div class="container">
    <!-- Status Card -->
    <div class="card">
      <h2>Pipeline Status</h2>
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
        <span id="statusBadge" class="status-badge status-idle">idle</span>
        <span id="lastRun" style="font-size:12px;color:#666;"></span>
      </div>
      <div class="stat-grid" id="stats">
        <div class="stat"><div class="value" id="statLeads">-</div><div class="label">Total Leads</div></div>
        <div class="stat"><div class="value" id="statQualified">-</div><div class="label">Qualified</div></div>
        <div class="stat"><div class="value" id="statSent">-</div><div class="label">Emails Sent</div></div>
      </div>
    </div>

    <!-- Controls -->
    <div class="card">
      <h2>Manual Controls</h2>
      <div class="btn-grid">
        <button class="btn primary" onclick="trigger('all')">Run Full Pipeline</button>
        <button class="btn" onclick="trigger('discovery')">Discovery</button>
        <button class="btn" onclick="trigger('qualification')">Qualification</button>
        <button class="btn" onclick="trigger('personalization')">Personalization</button>
        <button class="btn" onclick="trigger('outreach')">Outreach</button>
        <button class="btn" onclick="trigger('report')">Generate Report</button>
      </div>
      <div class="btn-grid" style="margin-top:8px;">
        <button class="btn danger" onclick="pauseScheduler()">Pause Scheduler</button>
        <button class="btn" onclick="resumeScheduler()">Resume Scheduler</button>
      </div>
    </div>

    <!-- Scheduled Jobs -->
    <div class="card">
      <h2>Scheduled Jobs</h2>
      <table class="jobs-table">
        <thead><tr><th>Job</th><th>Next Run</th></tr></thead>
        <tbody id="jobsBody"><tr><td colspan="2">Loading...</td></tr></tbody>
      </table>
    </div>

    <!-- Configuration -->
    <div class="card">
      <h2>Configuration</h2>
      <div class="config-grid" id="configGrid">Loading...</div>
    </div>

    <!-- Recent Leads -->
    <div class="card">
      <h2>Recent Leads</h2>
      <table class="leads-table">
        <thead><tr><th>Business</th><th>Category</th><th>City</th><th>Score</th><th>Tier</th><th>Status</th><th>Email</th></tr></thead>
        <tbody id="leadsBody"><tr><td colspan="7">Loading...</td></tr></tbody>
      </table>
    </div>
  </div>

  <div id="toast"></div>

  <script>
    function toast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.style.display = 'block';
      setTimeout(() => t.style.display = 'none', 3000);
    }

    async function fetchStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();

        // Status badge
        const badge = document.getElementById('statusBadge');
        const st = data.pipeline.status || 'idle';
        badge.textContent = st;
        badge.className = 'status-badge ' + (st.startsWith('running') ? 'status-running' : st.startsWith('error') ? 'status-error' : st === 'paused' ? 'status-paused' : 'status-idle');

        if (data.pipeline.last_run) {
          document.getElementById('lastRun').textContent = 'Last run: ' + new Date(data.pipeline.last_run).toLocaleString();
        }

        // Stats
        document.getElementById('statLeads').textContent = data.stats.total_leads;
        document.getElementById('statQualified').textContent = data.stats.qualified;
        document.getElementById('statSent').textContent = data.stats.emails_sent;

        // Jobs
        const tbody = document.getElementById('jobsBody');
        if (data.jobs.length === 0) {
          tbody.innerHTML = '<tr><td colspan="2" style="color:#999;">No scheduled jobs</td></tr>';
        } else {
          tbody.innerHTML = data.jobs.map(j =>
            `<tr><td>${j.id}</td><td>${j.next_run ? new Date(j.next_run).toLocaleString() : 'Paused'}</td></tr>`
          ).join('');
        }
      } catch (e) {
        console.error('Status fetch error:', e);
      }
    }

    async function fetchConfig() {
      try {
        const res = await fetch('/api/config');
        const cfg = await res.json();
        const grid = document.getElementById('configGrid');
        const items = [
          ['Discovery Hour', cfg.discovery_hour + ':00'],
          ['Qualification Hour', cfg.qualification_hour + ':00'],
          ['Personalization Hour', cfg.personalization_hour + ':00'],
          ['Outreach Hour', cfg.outreach_hour + ':00'],
          ['Report Time', cfg.report_hour + ':' + String(cfg.report_minute).padStart(2, '0')],
          ['Groq Model', cfg.groq_model],
          ['Google API Key', cfg.has_google_key ? '<span class="check">Configured</span>' : '<span class="cross">Missing</span>'],
          ['Groq API Key', cfg.has_groq_key ? '<span class="check">Configured</span>' : '<span class="cross">Missing</span>'],
          ['SMTP', cfg.has_smtp ? '<span class="check">Configured</span>' : '<span class="cross">Missing</span>'],
          ['Telegram', cfg.has_telegram ? '<span class="check">Configured</span>' : '<span class="cross">Optional</span>'],
        ];
        grid.innerHTML = items.map(([k, v]) => `<div class="config-item"><span class="key">${k}</span><span class="val">${v}</span></div>`).join('');
      } catch (e) {
        console.error('Config fetch error:', e);
      }
    }

    async function fetchLeads() {
      try {
        const res = await fetch('/api/leads?limit=20');
        const leads = await res.json();
        const tbody = document.getElementById('leadsBody');
        if (leads.length === 0) {
          tbody.innerHTML = '<tr><td colspan="7" style="color:#999;">No leads yet — run discovery first</td></tr>';
        } else {
          tbody.innerHTML = leads.map(l =>
            `<tr>
              <td><b>${l.business_name || '-'}</b></td>
              <td>${l.category || '-'}</td>
              <td>${l.city || '-'}</td>
              <td>${l.ai_score || 0}</td>
              <td class="tier-${l.lead_tier || 'D'}">${l.lead_tier || '-'}</td>
              <td>${l.status}</td>
              <td>${l.email || '-'}</td>
            </tr>`
          ).join('');
        }
      } catch (e) {
        console.error('Leads fetch error:', e);
      }
    }

    async function trigger(stage) {
      toast('Triggering ' + stage + '...');
      try {
        const res = await fetch('/api/pipeline/trigger/' + stage, { method: 'POST' });
        const data = await res.json();
        toast(data.error || 'Stage ' + stage + ' triggered!');
        setTimeout(fetchStatus, 2000);
      } catch (e) {
        toast('Error triggering ' + stage);
      }
    }

    async function pauseScheduler() {
      await fetch('/api/scheduler/pause', { method: 'POST' });
      toast('Scheduler paused');
      fetchStatus();
    }

    async function resumeScheduler() {
      await fetch('/api/scheduler/resume', { method: 'POST' });
      toast('Scheduler resumed');
      fetchStatus();
    }

    // Initial load
    fetchStatus();
    fetchConfig();
    fetchLeads();

    // Auto-refresh every 15s
    setInterval(() => { fetchStatus(); fetchLeads(); }, 15000);
  </script>
</body>
</html>"""
