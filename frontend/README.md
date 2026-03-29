# Cold Scout Dashboard

<p align="center">
  <img src="https://img.shields.io/badge/React-18-black.svg?style=for-the-badge&logo=react" alt="React" />
  <img src="https://img.shields.io/badge/Vite-5-black.svg?style=for-the-badge&logo=vite" alt="Vite" />
  <img src="https://img.shields.io/badge/TailwindCSS-3-black.svg?style=for-the-badge&logo=tailwind-css" alt="Tailwind" />
  <img src="https://img.shields.io/badge/TypeScript-5-black.svg?style=for-the-badge&logo=typescript" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Supabase-Auth-black.svg?style=for-the-badge&logo=supabase" alt="Supabase" />
</p>

The **Cold Scout Dashboard** is the centralized command center for the AI-driven lead generation pipeline. It provides real-time pipeline monitoring, campaign management, lead tracking, and role-based access for both **freelancers** and **clients**.

---

## Features

- **Role-Based Access Control**: Two distinct user roles — `freelancer` (full pipeline access) and `client` (welcome/reporting view). Roles are fixed at account creation and enforced on both the frontend and backend.
- **Supabase Auth**: Email/password and OAuth (Google, GitHub, Facebook, LinkedIn) sign-in via Supabase Auth with PKCE flow. JWT tokens are verified on the backend using the Supabase JWKS endpoint (ES256).
- **Plan Gating**: Freelancers on the free plan see a skeleton dashboard and an upgrade prompt. Pro/Enterprise freelancers and all clients see live data.
- **Real-time Pipeline Monitoring**: Live observation of discovery, qualification, and outreach stages.
- **Lead State Management**: Full lead lifecycle tracking with AI qualification scores.
- **Scheduler Control**: Override and manually trigger individual pipeline stages.
- **Inbox Processing**: Categorises inbound email replies by intent (positive, negative, out-of-office).

---

## Architecture

```
src/
├── components/
│   ├── auth/           # ProtectedRoute, ClientRoute, FreelancerRoute, SessionExpiredModal
│   ├── dashboard/      # DashboardSkeleton, UpgradeModal, stat cards, pipeline widgets
│   ├── layout/         # Shell, Sidebar, Topbar, PublicNavbar, PublicFooter
│   └── ui/             # Atomic design-system components (Button, Card, Badge, etc.)
├── hooks/
│   ├── useAuth.tsx     # AuthProvider + useAuth — central auth state, session sync
│   └── useSEO.ts       # Page-level SEO / meta tag management
├── lib/
│   ├── api.ts          # Axios client with JWT interceptor and session-expiry handling
│   └── supabase.ts     # Supabase client, signIn/signUp/signOut helpers, getUserRole
├── pages/              # Route-level view components (Login, SignUp, AuthCallback, Welcome, …)
└── App.tsx             # React Router v6 route tree
server/
└── index.ts            # Development-only Node.js proxy (injects X-API-Key server-side)
```

### Authentication Flow

1. **Email/Password**: `signInWithPassword` → Supabase session established → `onAuthStateChange` fires → auto-sync to backend (`/api/v1/auth/sync`) → role and plan loaded → redirect.
2. **OAuth**: `signInWithOAuth` → Supabase OAuth redirect → `/auth/callback` page → sync to backend → redirect based on backend role.
3. **Role authority**: `user.role` from the backend database is always the authoritative value. Supabase `user_metadata.role` is only used as a creation-time hint for brand-new accounts.

---

## Local Development Setup

### Prerequisites

- Node.js 18+
- The FastAPI backend running on `http://localhost:8000`

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Create a `.env.local` file inside `frontend/localleadpro-dashboard/`:

```env
# Supabase project credentials (Settings → API in your Supabase dashboard)
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key

# Development proxy target (the running FastAPI backend)
VITE_PROXY_URL=http://localhost:8000

# API key injected by the dev proxy into every backend request
VITE_API_KEY=your_api_key_matching_backend_API_KEY
```

> **Note:** `.env.local` is listed in `.gitignore` and is never committed to version control. Do not commit real credentials.

### 3. Start the Development Server

```bash
npm run dev
```

The dashboard is available at `http://localhost:5173`. The proxy server (`server/index.ts`) runs alongside Vite and injects `X-API-Key` into every forwarded request so the key is never exposed to the browser.

---

## Production Build

```bash
npm run build
```

The compiled `dist/` output is a fully static bundle deployable to any edge CDN (Vercel, Cloudflare Pages, AWS S3).

In production, set the following environment variables in your hosting platform:

| Variable | Description |
| --- | --- |
| `VITE_SUPABASE_URL` | Your Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | Your Supabase anonymous/public key |
| `VITE_PROXY_URL` | The deployed FastAPI backend URL |
| `VITE_API_KEY` | The API key (must match backend `API_KEY`) |

---

## Security Notes

- The `X-API-Key` header is injected **server-side** by the Node.js proxy in development. In production it is injected by the Vite build-time environment. It is **never** stored in `localStorage` or exposed in the browser's network tab as a static string.
- Supabase sessions are persisted in `localStorage` by the Supabase client SDK. The backend validates every request against the Supabase JWKS endpoint (ES256) or the legacy JWT secret (HS256).
- Role values stored in `localStorage` (`llp_user`) are treated as a display-only cache. The backend role is re-verified on every sync call and is never overwritten during login — only during initial account creation.
