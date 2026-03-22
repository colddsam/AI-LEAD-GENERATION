# 🌍 Continuous Deployment Guide (Production)

This guide provides an exact, step-by-step approach to deploying the **AI Lead Generation System** into a professional production environment from scratch. 

We utilize a robust modern stack:
1. **[Supabase](https://supabase.com/)** (Managed PostgreSQL Database)
2. **[Render](https://render.com/)** (Containerized FastAPI Backend)
3. **[Vercel](https://vercel.com/)** (Static React Dashboard)

---

## 🔑 Mastering API Keys & Secrets (100% Free Way)

Before deploying, you need to collect several API keys. Follow these exact steps to get them for free.

### 🧩 1. Groq AI (Llama 3 Brain)
*Used for Lead Qualification & Email Generation.*

```mermaid
graph LR
    A[Groq Cloud Console] --> B[Sign up with Email/GitHub]
    B --> C[Navigate to API Keys]
    C --> D[Create API Key]
    D --> E[GSK_...]
```

1. Visit [Groq Cloud](https://console.groq.com/keys).
2. Sign up for a free account (Google/GitHub supported).
3. Click "Create API Key". 
4. **Copy the key** (starts with `gsk_`). This is your `GROQ_API_KEY`.

---

### 📍 2. Google Places API (Target Discovery)
*Used to find local businesses.*

```mermaid
graph LR
    A[Google Cloud Console] --> B[Create Project]
    B --> C[Enable Places API]
    C --> D[Credentials -> API Key]
    D --> E[AIza...]
```

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. **Create a New Project** (e.g., "AI-Lead-Gen").
3. Search for **"Places API"** and click **Enable**.
4. Go to **APIs & Services > Credentials**.
5. Click **+ CREATE CREDENTIALS > API Key**.
6. **Free-tier Note**: Google offers $200 free monthly credit, which easily covers thousands of searches daily at no cost to you.

---

### 🗄️ 3. Supabase (PostgreSQL Database)
*Used to store leads, jobs, and history.*

```mermaid
graph LR
    A[Supabase.com] --> B[New Project]
    B --> C[Settings -> Database]
    C --> D[Copy Connection String]
    62 --> E[Copy URL & Anon Key]
```

1. Go to [Supabase](https://supabase.com/).
2. Create a project on the **Free Tier**.
3. Go to **Settings > Database**.
4. Copy the **URI** connection string.
5. **Format it for FastAPI**: Add `+asyncpg` after `postgresql`.
   *Result: `postgresql+asyncpg://postgres.[ref]:[pass]@aws-..`*
6. Go to **Settings > API** to copy `SUPABASE_URL` and `SUPABASE_ANON_KEY`.

---

### ✉️ 4. Brevo (SMTP Outreach)
*Used to send outreach emails.*

```mermaid
graph TD
    A[Brevo.com] --> B[Sign up Free]
    B --> C[Click Profile -> SMTP & API]
    C --> D[Generate New SMTP Key]
    D --> E[Copy Key to SMTP_PASSWORD]
    E --> F[Verify Sender Domain/Email]
```

1. Sign up for free at [Brevo](https://www.brevo.com/).
2. Click your **Profile Name** (top right) > **SMTP & API**.
3. Select the **SMTP** tab.
4. Click **Generate a New SMTP Key**.
5. **Set the following in `.env`**:
   - `BREVO_SMTP_HOST`: `smtp-relay.brevo.com`
   - `BREVO_SMTP_PORT`: `587`
   - `BREVO_SMTP_USER`: Your login email.
   - `BREVO_SMTP_PASSWORD`: The key you just generated.
   - `FROM_EMAIL`: Your verified sender address from Brevo settings.
   - `FROM_NAME`: Your business or personal name.

---

### 📤 5. Gmail IMAP (Inbound Tracking)
*Used for tracking email replies.*

```mermaid
graph LR
    A[Google Account Settings] --> B[2-Step Verification ON]
    B --> C[Search: App Passwords]
    C --> D[Create: 'ColdScout']
    D --> E[Copy 16-Char Code]
```

1. Open your Google Account settings.
2. Ensure **2-Step Verification** is enabled.
3. Search for **"App Passwords"** in the top search bar.
4. Create a new app password named "ColdScout".
5. Copy the **16-character code**. This is your `IMAP_PASSWORD`.

---

### 🤖 6. Telegram Bot (Real-time Alerts)
*Used for instant notifications on system health and lead status.*

```mermaid
graph TD
    A[Search @BotFather] --> B[/newbot command]
    B --> C[Set Name & Username]
    C --> D[Copy HTTP API Token]
    D --> E[Search @userinfobot]
    E --> F[Copy Your User ID]
```

1. **Step 1: Create the Bot**
   - Search for **@BotFather** on Telegram and click **Start**.
   - Send `/newbot`.
   - Follow prompts to set a name and a unique username (ending in `_bot`).
   - **Save the Token**: `TELEGRAM_BOT_TOKEN`.
2. **Step 2: Get Your Chat ID**
   - Search for **@userinfobot** on Telegram.
   - Click **Start**.
   - It will reply with your `User ID`. This is your `TELEGRAM_CHAT_ID`.
3. **Step 3: Start the Bot**
   - Open your new bot and click **Start** or send a message so it can send you alerts.

---

### ⏰ 7. CRON Job & Keep-Alive (cron-job.org)
*Ensures the system never sleeps (Render Free Tier) and schedules remain active.*

```mermaid
graph TD
    A[cron-job.org] --> B[Create Free Account]
    B --> C[API Keys -> Create New]
    C --> D[Copy Key to CRON_JOB_API_KEY]
    D --> E[Run setup_cronjob.py Script]
```

1. Sign up at [cron-job.org](https://cron-job.org).
2. Go to **Settings > API Keys** and generate a new key.
3. **Automated Setup**:
   Once your backend is live on Render, run this locally:
   ```bash
   python scripts/setup_cronjob.py
   ```
4. This script automatically registers a "Keep-Alive" ping every 10 minutes to `https://your-app.onrender.com/health`.

---

### 🚀 8. GitHub Actions & CI/CD
*Automates tests and deployment sync on every push.*

```mermaid
graph LR
    A[Local Code] --> B[git push main]
    B --> C[GitHub Actions runs Tests]
    C --> D[On Success: Render Deploy Hook]
    D --> E[Live Production Update]
```

1. **Repository Secrets**:
   Go to your GitHub Repo **Settings > Secrets and variables > Actions** and add:
   - `GROQ_API_KEY`, `GOOGLE_PLACES_API_KEY`, `DATABASE_URL`, etc.
   - `RENDER_DEPLOY_HOOK`: Get this from Render Dashboard > Service > Settings > Deploy Hook.
2. **Alerts**:
   - `TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHAT_ID`: To receive build failure/success notifications.

---

### 🛡️ 9. Core Secrets (Security)
*Used to encrypt sessions and secure the API.*

To generate secure `APP_SECRET_KEY`, `API_KEY`, and `SECURITY_SALT` automatically, run this command in your terminal:
```bash
python scripts/generate_secrets.py
```
This script will generate cryptographically secure hex strings and offer to append them directly to your `.env` file.

---

## ⚙️ Master Environment Variable Reference (42 Tokens)

Ensure all variables are consistently mirrored across your production environment (Render/Vercel).

| Category | Key | Description |
| :--- | :--- | :--- |
| **Security** | `APP_ENV` | `production` or `development` |
| | `APP_SECRET_KEY` | Hex string for session salt |
| | `API_KEY` | Public access key for API |
| | `SECURITY_SALT` | Random string for hashing |
| | `BACKEND_CORS_ORIGINS` | Comma-separated allowed domains |
| | `APP_URL` | Your Render Service URL |
| | `IMAGE_BASE_URL` | CDN link for branding assets |
| | `VITE_API_KEY` | (Frontend) Matches Backend `API_KEY` |
| **Database** | `DATABASE_URL` | Supabase URI (`postgresql+asyncpg://...`) |
| | `SUPABASE_URL` | Your Supabase project URL |
| | `SUPABASE_ANON_KEY` | Your Supabase anon/public key |
| | `REDIS_URL` | (Optional) Upstash Redis Link |
| **AI Brain** | `GROQ_API_KEY` | Groq Llama 3 key |
| | `GROQ_MODEL` | Default: `llama-3.1-8b-instant` |
| | `GOOGLE_PLACES_API_KEY` | Google Maps API key |
| **Outreach** | `BREVO_SMTP_HOST` | `smtp-relay.brevo.com` |
| | `BREVO_SMTP_PORT` | `587` |
| | `BREVO_SMTP_USER` | Your Brevo login email |
| | `BREVO_SMTP_PASSWORD` | Your Brevo SMTP key |
| | `FROM_EMAIL` | Verified sender address |
| | `FROM_NAME` | Display name in inbox |
| | `REPLY_TO_EMAIL` | Direct client reply address |
| **Tracking** | `IMAP_HOST` | `imap.gmail.com` |
| | `IMAP_USER` | Your Gmail address |
| | `IMAP_PASSWORD` | 16-char App Password |
| **Alerts** | `ADMIN_EMAIL` | Dashboard login email |
| | `TELEGRAM_BOT_TOKEN` | Token from @BotFather |
| | `TELEGRAM_CHAT_ID` | User ID from @userinfobot |
| | `WHATSAPP_NUMBER` | Contact for WhatsApp alerts |
| | `CALLMEBOT_API_KEY` | CallMeBot integration key |
| **Automation** | `PRODUCTION_STATUS` | `RUN` to enable pipeline |
| | `CRON_JOB_API_KEY` | cron-job.org portal key |
| | `RENDER_DEPLOY_HOOK` | Auto-deployment URL |
| **Scheduling** | `DISCOVERY_HOUR` | IST Hour for search (0-23) |
| | `QUALIFICATION_HOUR` | IST Hour for qualification |
| | `PERSONALIZATION_HOUR`| IST Hour for personalization |
| | `OUTREACH_HOUR` | IST Hour for email sending |
| | `REPORT_HOUR` | IST Hour for daily report |
| | `REPORT_MINUTE` | Minute for daily report |
| | `EMAIL_SEND_INTERVAL_SECONDS` | Delay between emails |
| **Branding** | `VITE_SITE_NAME` | (Frontend) Custom brand title |
| | `BOOKING_LINK` | Meeting URL (Calendly) |
| | `SENDER_ADDRESS` | Physical address for footer |

---

## 🚀 Step 1: Database Setup (Supabase)

1. Create a project on [Supabase.com](https://supabase.com/).
2. Get the **URI** from **Project Settings > Database**.
3. **CRITICAL**: Change `postgresql://` to `postgresql+asyncpg://`.

## ⚙️ Step 2: Backend Deployment (Render)

1. **Connect Repo**: New -> Web Service.
2. **Environment**: Select **Docker**.
3. **Variables**: Mirror the **Master Reference Table** above.
4. **Deploy**: Once live, copy your URL for the frontend.

## 🎨 Step 3: Frontend Deployment (Vercel)

1. **Connect Repo**: New -> Project.
2. **Root Directory**: Select `frontend/localleadpro-dashboard`.
3. **Environment Variables**:
   - `VITE_PROXY_URL`: Your Render Backend URL.
   - `VITE_API_KEY`: Matching your backend API_KEY.
   - `VITE_SITE_NAME`: Your desired brand name.
4. **Deploy**: Your dashboard is now live!

🎉 **Congratulations! Your system is now running 24/7 in the cloud.**

## 🌐 Cross-Platform Architecture (Vercel + Render)

To ensure high availability and performance, we use a decentralized architecture:

```mermaid
graph LR
    User((User)) --> Vercel[Vercel Frontend]
    Vercel -- "X-API-Key: Header" --> Render[Render API]
    Render --> Supabase[(Supabase DB)]
    Render --> Groq[Groq AI]
    Render --> Brevo[Brevo SMTP]
```

### 🔐 No Proxy Needed in Production
In this production architecture, the React app communicates **directly** with the Render API. The `server/index.ts` proxy is primarily for **local development** to bypass browser CORS constraints during testing. For production, simply point `VITE_PROXY_URL` to your Render URL (no `server/` process required on Vercel).
