# AI Lead Generation - Backend Service

This repository section contains the core FastAPI application handling API requests, scheduling cron tasks for lead discovery and qualification using Groq Llama 3, and automated email generation mechanisms.

## System Prerequisites
- **Python**: 3.11+
- **Database**: PostgreSQL 14+

## Local Execution

### 1. Setup Virtual Environment
```bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Environment Variables
Copy `.env.example` to `.env` and fill in necessary fields (`GROQ_API_KEY`, `SUPABASE_URL`, etc.).

### 4. Database Setup & Run
Ensure your local or remote DB is accessible via `DATABASE_URL`.
```bash
python scripts/create_tables.py
python scripts/seed_admin.py
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
API Documentation will be available at: http://localhost:8000/docs
