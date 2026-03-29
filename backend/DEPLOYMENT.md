# Backend Deployment Guide

This document specifices production deployment steps for the Python FastAPI application and task workers.

## Deploying to Render

We recommend Render for hosting the web service alongside background workers.

### 1. Connect GitHub Repository
Link this repository branch to Render and set the root directory to `backend`.

### 2. Configure Environment Properties
Create a **Web Service** with the following parameters:
- **Build Command**: `pip install -r requirements.txt && playwright install chromium --with-deps`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000` (alternatively use Docker build).
- **Environment Variables**: Populate exactly as laid out in `.env.example`. Make sure `APP_ENV` is `production`.

### 3. Database Updates
If your deployment utilizes `alembic` migrations, you may execute them via jobs or via `entrypoint.sh` scripts depending on containerization usage.
