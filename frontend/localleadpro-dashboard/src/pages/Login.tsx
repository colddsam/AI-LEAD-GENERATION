import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { LogIn, Zap } from 'lucide-react';

/**
 * The authentication entry point to the system dashboard.
 *
 * It provides a secure login form that calls out to the backend API (`/api/v1/login/access-token`).
 * Upon successful authentication, it acquires a JWT token and immediately redirects
 * the user back to their securely requested destination (or the Overview page by default).
 *
 * State bounds: Once a JWT is successfully saved via the `useAuth` hook, the user
 * is effectively bound to the session across all browser windows.
 */
export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // The 'from' object retains the URL path the user tried to visit before being intercepted
  const from = location.state?.from?.pathname || '/';

  useEffect(() => {
    if (isAuthenticated) {
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, from]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      // Authenticates the user by acquiring a JWT access token via the OAuth2 compatible endpoint.
      // In local dev, VITE_PROXY_URL hits the proxy. In production, it hits the live backend directly.
      const res = await fetch(`${import.meta.env.VITE_PROXY_URL || ''}/api/v1/login/access-token`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-API-Key': import.meta.env.VITE_API_KEY || ''
        },
        body: formData,
      });

      if (!res.ok) {
        throw new Error('Invalid credentials');
      }

      const data = await res.json();
      login(data.access_token, data.user);
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  if (isAuthenticated) return null; // Prevent flash of login while redirecting

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-navy-950 px-4 sm:px-0">
      <div className="absolute inset-0 z-0 opacity-20 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-coldscout-teal/30 via-transparent to-transparent"></div>
      
      <Card className="w-full max-w-md z-10 relative overflow-hidden ring-1 ring-white/10 shadow-2xl backdrop-blur-sm" padding={false}>
        <div className="p-8">
          <div className="flex justify-center mb-8">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-coldscout-teal to-blue-500 flex items-center justify-center shadow-lg shadow-coldscout-teal/20">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
                {import.meta.env.VITE_SITE_NAME || 'LocalLeadPro'}
              </span>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Admin Email</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-navy-900/50 border border-white/10 rounded-lg px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:ring-1 focus:ring-coldscout-teal/50 focus:border-coldscout-teal/50 transition-colors"
                placeholder="admin@example.com"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-300">Master Password</label>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-navy-900/50 border border-white/10 rounded-lg px-4 py-3 text-white placeholder:text-gray-600 focus:outline-none focus:ring-1 focus:ring-coldscout-teal/50 focus:border-coldscout-teal/50 transition-colors"
                placeholder="••••••••"
              />
            </div>

            <Button
              type="submit"
              className="w-full justify-center h-12 text-sm font-semibold tracking-wide"
              loading={loading}
              icon={<LogIn className="w-4 h-4" />}
            >
              Authenticate System
            </Button>
          </form>
        </div>
        
        <div className="border-t border-white/5 bg-white/[0.02] p-4 text-center">
          <p className="text-xs text-gray-500">Authorized Personnel Only. Core Engine Node Alpha.</p>
        </div>
      </Card>
    </div>
  );
}
