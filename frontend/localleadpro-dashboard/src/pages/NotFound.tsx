import { Link } from 'react-router-dom';
import Button from '../components/ui/Button';
import { ShieldAlert, ArrowLeft } from 'lucide-react';

/**
 * A standard 404 overlay specifically designed to match the application's
 * dark futuristic aesthetic. Displayed automatically by React Router when a
 * user navigates to an invalid/unregistered route.
 */
export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center flex-col text-center space-y-6">
      <div className="w-20 h-20 bg-red-500/10 rounded-full flex items-center justify-center animate-pulse">
        <ShieldAlert className="w-10 h-10 text-red-400" />
      </div>
      <div>
        <h1 className="text-4xl font-bold font-mono text-white mb-2">404</h1>
        <p className="text-gray-400 max-w-md mx-auto">
          The requested system node could not be localized. Please return to the primary sequence.
        </p>
      </div>
      <Link to="/" className="inline-block mt-4">
         <Button icon={<ArrowLeft className="w-4 h-4" />}>Return to Dashboard</Button>
      </Link>
    </div>
  );
}
