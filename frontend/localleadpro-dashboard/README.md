# 🖥️ LocalLeadPro Admin Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/React-18-blue.svg?style=for-the-badge&logo=react" alt="React" />
  <img src="https://img.shields.io/badge/Vite-5-purple.svg?style=for-the-badge&logo=vite" alt="Vite" />
  <img src="https://img.shields.io/badge/TailwindCSS-3-38B2AC.svg?style=for-the-badge&logo=tailwind-css" alt="Tailwind" />
  <img src="https://img.shields.io/badge/TypeScript-5-blue.svg?style=for-the-badge&logo=typescript" alt="TypeScript" />
</p>

The **LocalLeadPro Dashboard** is a high-performance CRM and control interface for an AI-driven lead generation ecosystem. It bridges the gap between raw data scraping and meaningful business outreach by providing real-time pipeline monitoring, AI-powered lead qualification, and a centralized communication hub.

---

## ✨ System Features

- **🔐 Enterprise Authentication**: JWT-based security with persistent sessions, route protection, and OAuth2 compatibility.
- **📊 Real-time Dashboard**: Live overview of pipeline health, campaign performance, and system-wide metrics.
- **🕵️ Lead Management CRM**: Advanced lead tracking with AI-scored qualification, detailed enrichment data, and outreach history.
- **⚙️ Integrated Job Scheduler**: Direct control over background automation tasks (Discovery, Scraping, Outreach) via `jobs_config.json`.
- **🛠️ Pipeline Control**: Manual trigger overrides for individual pipeline stages with live output logging.
- **📥 AI Inbox**: Centralized reply management with automated intent classification (Interested, Not Interested, Out of Office).
- **🎨 Premium UI/UX**: Professional glassmorphic design utilizing Tailwind CSS, Lucide icons, and sleek micro-animations.

---

## 🏗️ Architecture & Security

To ensure high security and seamless local development, the system uses a **Development Proxy Server**:

- **Location**: `server/index.ts`
- **Purpose**: Acts as a bridge between the Frontend (Vite) and the Backend API (FastAPI).
- **Security**: Injects sensitive `API_KEY` headers on the server-side, preventing them from being exposed to the client browser.
- **CORS Management**: Handles cross-origin requests and forwards Authorization headers (JWT) automatically.

---

## 📂 Project Structure

```text
frontend/localleadpro-dashboard/
├── server/           # 🛡️ Development Proxy Server (Node.js + TypeScript)
├── src/
│   ├── components/   # Reusable Atomic UI and Layout components
│   ├── hooks/        # 🪝 Logic-heavy React hooks for API interaction & Auth
│   ├── lib/          # Core utilities, API clients, and constants
│   ├── pages/        # Main route views (Dashboard, CRM, Settings, etc.)
│   ├── App.tsx       # Main Router and Page Layout definition
│   └── main.tsx      # Application entry point with React Query Provider
├── .env              # 🔑 Local environment secrets
└── vite.config.ts    # Build and dev server configuration
```

---

## 🚀 Step-by-Step Setup

### 1. Installation
Ensure you have Node.js 18+ installed.

```bash
# Install frontend and proxy dependencies
npm install
```

### 2. Environment Configuration
Create a `.env` file in the `frontend/localleadpro-dashboard` directory:

```env
# Backend API Location (External or Local)
API_BASE_URL=http://localhost:8000

# Global API Key (Injected by Proxy)
API_KEY=your_secret_api_key_here

# Frontend Proxy Access
VITE_PROXY_URL=http://localhost:3000
VITE_API_KEY=your_secret_api_key_here
```

### 3. Local Development Start
Run both the frontend and the proxy server simultaneously:

```bash
# Starts proxy on :3000 and Vite on :5173
npm run dev
```

---

## 🚢 Building for Production

Generate the optimized static bundle for deployment:

```bash
npm run build
```

The resulting `dist/` directory can be deployed to any static host (Vercel, Netlify, AWS S3). Note that in production, you should point your environment variables directly to your live API or configure an equivalent production proxy.

---

<div align="center">
  <em>LocalLeadPro — Automating the Future of Outreach</em>
</div>
