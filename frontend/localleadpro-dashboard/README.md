# 🖥️ LocalLeadPro Admin Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/React-18-blue.svg?style=for-the-badge&logo=react" alt="React" />
  <img src="https://img.shields.io/badge/Vite-5-purple.svg?style=for-the-badge&logo=vite" alt="Vite" />
  <img src="https://img.shields.io/badge/TailwindCSS-3-38B2AC.svg?style=for-the-badge&logo=tailwind-css" alt="Tailwind" />
</p>

The **LocalLeadPro Dashboard** is the centralized CRM and control interface for the AI Lead Generation System. It provides real-time visibility into the automated lead generation pipeline, job statuses, and detailed prospect metrics.

---

## ✨ System Features

- **🔐 Enterprise Authentication**: JWT-based login with persistent sessions and route protection.
- **📊 Unified Analytics**: High-level overview of Lead Volume, Conversion Rates, and AI Status at a glance.
- **🕵️ Lead CRM**: Interactive tables to view, filter, and manage discovered leads and their qualification statuses.
- **⚙️ Job Orchestrator**: Real-time tracking of background automation tasks (Discovery, Scraping, Outreach).
- **🎨 Modern Glassmorphic UI**: A highly premium, scalable design optimized for both desktop and mobile operations.

---

## 📂 Project Structure

```text
frontend/localleadpro-dashboard/
├── src/
│   ├── assets/       # Static assets and icons
│   ├── components/   # Reusable UI components (Sidebar, StatsCard, etc.)
│   ├── context/      # React Context (AuthContext for JWT handling)
│   ├── hooks/        # Custom data hooks (useApi, useAuth)
│   ├── pages/        # Core Views (Dashboard, Leads, Automation, Login)
│   ├── App.jsx       # Root router component
│   └── index.css     # Global Tailwind styles
├── .env.example      # Example frontend variables
└── vite.config.js    # Vite environment configuration
```

---

## 🚀 Step-by-Step Setup

### 1. Installation
Ensure you have Node.js 18+ installed. Navigate to the directory and install dependencies:
```bash
npm install
```

### 2. Environment Configuration
Create a `.env` file in the root of the `frontend/localleadpro-dashboard` directory. The application needs to know where the FastAPI backend is located.

```env
# For Local Development (running FastAPI on port 8000):
VITE_PROXY_URL=http://localhost:8000

# For Production (When your API is live on Render):
VITE_PROXY_URL=https://your-app-namespace.onrender.com
```

### 3. Local Development Start
Spin up the local development server:
```bash
npm run dev
```

The dashboard will be available at **http://localhost:5173**. 
*Note: Make sure your FastAPI backend is running simultaneously for data and login to work.*

---

## 🚢 Building for Production

If you are deploying this manually or via a CI/CD pipeline, run the build command to generate a highly optimized static bundle:

```bash
npm run build
```

This will create a `dist/` directory containing the final, minified HTML/CSS/JS files. These can be served from any static file host like NGINX, AWS S3, or Vercel.

---

<div align="center">
  <em>LocalLeadPro Frontend Architecture</em>
</div>
