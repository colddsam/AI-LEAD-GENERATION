import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';

import Shell from './components/layout/Shell';
import Login from './pages/Login';
import Overview from './pages/Overview';
import Pipeline from './pages/Pipeline';
import Scheduler from './pages/Scheduler';
import Leads from './pages/Leads';
import LeadDetail from './pages/LeadDetail';
import Campaigns from './pages/Campaigns';
import Inbox from './pages/Inbox';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';
import { AuthProvider } from './hooks/useAuth';
import ProtectedRoute from './components/auth/ProtectedRoute';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 30_000,
      refetchOnWindowFocus: false,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            {/* Public */}
            <Route path="/login" element={<Login />} />

            {/* Dashboard (inside ProtectedRoute + Shell layout) */}
            <Route element={<ProtectedRoute />}>
              <Route element={<Shell />}>
                <Route path="/overview" element={<Overview />} />
                <Route path="/pipeline" element={<Pipeline />} />
                <Route path="/scheduler" element={<Scheduler />} />
                <Route path="/leads" element={<Leads />} />
                <Route path="/leads/:id" element={<LeadDetail />} />
                <Route path="/campaigns" element={<Campaigns />} />
                <Route path="/inbox" element={<Inbox />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/settings" element={<Settings />} />
              </Route>
            </Route>

            {/* Redirects + 404 */}
            <Route path="/" element={<Navigate to="/overview" replace />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>

      <Toaster
        position="bottom-right"
        toastOptions={{
          style: {
            background: '#101829',
            color: '#e2e8f0',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: '10px',
            fontSize: '13px',
            fontFamily: '"JetBrains Mono", monospace',
          },
          success: {
            iconTheme: { primary: '#00e5be', secondary: '#0a0f1e' },
          },
          error: {
            iconTheme: { primary: '#ff3b5c', secondary: '#0a0f1e' },
          },
        }}
      />
    </QueryClientProvider>
  );
}
