# Frontend Deployment Guide

This document specifices production deployment steps for the React Vite Admin Dashboard.

## Deploying to Vercel

Vercel provides native Vite and React support.

### 1. Link Project to Vercel
In the Vercel dashboard, attach this repository and set the **Root Directory** to `frontend`.

### 2. Configure Build
Vercel should automatically detect Vite. 
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### 3. Environment Variables
Add necessary environment parameters to your Vercel project:
- `VITE_PROXY_URL`: Point this to your Render backend URL (e.g. `https://your-backend.onrender.com`).
- `VITE_API_KEY`: API authentication key.

### 4. Deploy
Vercel will manage SSL certificates and CDN edge caching automatically.
