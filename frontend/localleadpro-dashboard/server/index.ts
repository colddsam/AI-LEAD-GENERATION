/**
 * Local Development Proxy Server.
 * 
 * Provides a CORS-compliant bridge between the Vite frontend and the Python backend.
 * Features:
 * - Automatic injection of the system API Key into all proxied requests.
 * - Forwarding of Authorization headers for authenticated sessions.
 * - Detailed request logging for debugging local integration issues.
 */
import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import cors from 'cors';
import dotenv from 'dotenv';
import path from 'path';

// Load environmental configuration from the root directory
dotenv.config({ path: path.join(__dirname, '../.env.local') });

const app = express();
/** Port used by the proxy; must match the proxy URL in frontend constants */
const PORT = process.env.PORT || 3001;
/** Target backend API URL (resolved from .env.local) */
const API_BASE_URL = process.env.API_BASE_URL;
/** Global secret key used for administrative authentication */
const API_KEY = process.env.API_KEY;

if (!API_BASE_URL || !API_KEY) {
  console.error('❌ Missing Critical Configuration: API_BASE_URL or API_KEY in .env.local');
  process.exit(1);
}

// Allow local Vite dev servers to communicate with this proxy securely
app.use(cors({ origin: ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:4173'] }));

// HTTP Proxy Middleware
// This routes local frontend requests (from 5173) through this proxy (3001) to the actual backend API.
// It bypasses browser CORS constraints during local development.
// Note: In production (Vercel + Render), this proxy is completely skipped, and the frontend connects to the backend directly.
app.use(createProxyMiddleware({
  target: API_BASE_URL,
  changeOrigin: true,
  pathFilter: '/api',
  on: {
    proxyReq: (proxyReq, req) => {
      // Automatically attach the global API Key to every outgoing request for local development
      proxyReq.setHeader('X-API-Key', API_KEY);
      // Forward Authorization header from the frontend (JWT Bearer token)
      const authHeader = req.headers['authorization'];
      if (authHeader) {
        proxyReq.setHeader('Authorization', authHeader);
      }
      console.log(`[PROXY] ${req.method} ${req.url} | Auth: ${authHeader ? 'Bearer ...' + (authHeader as string).slice(-8) : 'NONE'}`);
    },
    proxyRes: (proxyRes, req, _res) => {
      console.log(`[PROXY] ${req.method} ${req.url} -> ${proxyRes.statusCode}`);
    },
    error: (err, req, res) => {
      console.error(`[PROXY ERROR] ${req.method} ${req.url}: ${err.message}`);
      (res as express.Response).status(502).json({ detail: 'Proxy error: ' + err.message });
    },
  },
}));

const server = app.listen(PORT, () => console.log(`✅ Proxy running on http://localhost:${PORT}`));

// Explicit error handling for the server listener
server.on('error', (err: any) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`\n❌ Error: Port ${PORT} is already in use.`);
    console.error(`   A process is already running on this port. Please stop it or use a different port.\n`);
  } else {
    console.error(`\n❌ Server error:`, err.message);
  }
  process.exit(1);
});

// Capture unhandled rejections and exceptions
process.on('unhandledRejection', (reason) => {
  console.error('Unhandled Rejection:', reason);
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err.message);
  process.exit(1);
});
