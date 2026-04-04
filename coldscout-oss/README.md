# Cold Scout OSS — Self-Hosted Lead Generation

[![GitHub Release](https://img.shields.io/github/v/release/colddsam/coldscout?filter=oss-v*&label=Latest%20Release&color=black)](https://github.com/colddsam/coldscout/releases?q=oss-v&expanded=true)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](https://opensource.org/licenses/MIT)

> Free, open-source, self-hosted lead generation pipeline. Part of the [Cold Scout](https://coldscout.colddsam.com) platform.

**Zero cost to Cold Scout** — you bring your own API keys.

### [Download Latest Release](https://github.com/colddsam/coldscout/releases/latest)

## What's Included

The full 5-stage automated lead generation pipeline:

| Stage | Description |
|-------|-------------|
| **Discovery** | Finds local businesses via Google Places API |
| **Qualification** | Scores leads by digital presence (website, social, reviews) |
| **Personalization** | AI-generated outreach emails + PDF proposals via Groq |
| **Outreach** | Sends personalized emails via Brevo SMTP |
| **Reporting** | Daily Excel reports emailed to admin |

Plus a **web dashboard** at `http://localhost:8000` for monitoring and manual control.

## What's NOT Included

- **Threads/social media pipeline** (platform-specific, Pro/Enterprise only)
- **Authorization layer** (no login, no JWT — this is your private server)
- **Supabase/PostgreSQL** (uses local SQLite for simplicity)
- **Billing/payments** (it's free!)

## Quick Start

### 1. Download

**Option A: Download release (recommended)**
```bash
# Download from GitHub Releases
# https://github.com/colddsam/coldscout/releases?q=oss-v&expanded=true
# Extract the archive and cd into it
```

**Option B: Clone from source**
```bash
git clone https://github.com/colddsam/coldscout.git
cd coldscout/coldscout-oss
```

### 2. Get Your API Keys (all free tiers available)

| Service | What For | Free Tier | Setup |
|---------|----------|-----------|-------|
| **Google Places** | Business discovery | $200/mo credit | [GCP Console](https://console.cloud.google.com/) → Enable Places API → Credentials → API Key |
| **Groq** | AI email generation | Free tier | [console.groq.com](https://console.groq.com/) → API Keys → Create |
| **Brevo** | Email sending | 300 emails/day | [brevo.com](https://www.brevo.com/) → SMTP & API → Generate Key |
| **Telegram** (optional) | Pipeline alerts | Free | [@BotFather](https://t.me/BotFather) → Create Bot → Get Token |

### 3. Configure

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 4. Run

**Option A: Python (development)**
```bash
pip install -r requirements.txt
python run.py
```

**Option B: Docker (production)**
```bash
docker compose up -d
```

### 5. Open Dashboard

Visit `http://localhost:8000` to:
- View pipeline status and statistics
- Manually trigger any pipeline stage
- See all discovered leads
- Pause/resume the automated scheduler
- Check configuration status

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web dashboard |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/status` | Pipeline status + stats |
| `GET` | `/api/leads` | List leads (query: `?status=qualified&limit=50`) |
| `GET` | `/api/config` | Current configuration |
| `POST` | `/api/pipeline/trigger/{stage}` | Trigger a stage (`all`, `discovery`, `qualification`, `personalization`, `outreach`, `report`) |
| `POST` | `/api/scheduler/pause` | Pause all scheduled jobs |
| `POST` | `/api/scheduler/resume` | Resume all scheduled jobs |

## Default Schedule (24h IST)

| Time | Stage |
|------|-------|
| 06:00 | Discovery |
| 07:00 | Qualification |
| 08:00 | Personalization |
| 09:00 | Outreach |
| 23:30 | Daily Report |

Configure in `.env` via `DISCOVERY_HOUR`, `QUALIFICATION_HOUR`, etc.

## Architecture

```
coldscout-oss/
├── app/
│   ├── main.py              # FastAPI app + dashboard + scheduler
│   ├── config.py             # Environment configuration
│   ├── database.py           # SQLite async engine
│   ├── pipeline.py           # 5-stage pipeline orchestrator
│   ├── models/               # SQLAlchemy models (Lead, Campaign, Report)
│   └── modules/
│       ├── discovery/        # Google Places API + email scraping
│       ├── qualification/    # Website/social/review scoring
│       ├── personalization/  # Groq AI + PDF proposals
│       ├── outreach/         # Brevo SMTP email sender
│       ├── enrichment/       # Competitor analysis
│       ├── reporting/        # Excel report builder
│       └── notifications/    # Optional Telegram alerts
├── run.py                    # Entry point
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## License

MIT — Same as the main Cold Scout project.
