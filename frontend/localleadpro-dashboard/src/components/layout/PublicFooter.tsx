import { Link } from 'react-router-dom';
import { Heart } from 'lucide-react';
import Logo from '../ui/Logo';

export default function PublicFooter() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-gray-200 py-12 bg-white relative z-10">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex flex-col md:flex-row items-start justify-between gap-12 mb-12">
          <div className="flex flex-col gap-4 max-w-sm">
            <Link to="/" className="flex items-center" aria-label="Cold Scout Home">
              <Logo size="sm" />
            </Link>
            <p className="text-sm text-secondary leading-relaxed">
              AI-powered lead generation platform that discovers, qualifies, and engages local business leads at scale.
            </p>
          </div>
          
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-12 md:gap-24">
            <div className="flex flex-col gap-4">
              <h4 className="text-sm font-bold text-black uppercase tracking-wider">Product</h4>
              <nav className="flex flex-col gap-2">
                <a href="/#features" className="text-sm text-secondary hover:text-black transition-colors">Features</a>
                <a href="/#workflow" className="text-sm text-secondary hover:text-black transition-colors">How it works</a>
                <Link to="/pricing" className="text-sm text-secondary hover:text-black transition-colors">Pricing</Link>
                <Link to="/docs" className="text-sm text-secondary hover:text-black transition-colors">Documentation</Link>
              </nav>
            </div>
            
            <div className="flex flex-col gap-4">
              <h4 className="text-sm font-bold text-black uppercase tracking-wider">Legal</h4>
              <nav className="flex flex-col gap-2">
                <Link to="/privacy" className="text-sm text-secondary hover:text-black transition-colors">Privacy Policy</Link>
                <Link to="/terms" className="text-sm text-secondary hover:text-black transition-colors">Terms of Service</Link>
                <Link to="/delete-data" className="text-sm text-secondary hover:text-black transition-colors">Data Deletion</Link>
              </nav>
            </div>

            <div className="flex flex-col gap-4">
              <h4 className="text-sm font-bold text-black uppercase tracking-wider">Community</h4>
              <nav className="flex flex-col gap-2">
                <a 
                  href="https://github.com/colddsam/coldscout.git" 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="text-sm text-secondary hover:text-black transition-colors"
                >
                  GitHub
                </a>
                <a 
                  href="https://github.com/sponsors/colddsam" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-sm text-secondary hover:text-black transition-colors flex items-center gap-1"
                >
                  <Heart className="w-3 h-3 fill-black text-black" /> Sponsor
                </a>
              </nav>
            </div>
          </div>
        </div>
        
        <div className="pt-8 border-t border-gray-100 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-xs text-subtle">
            &copy; {currentYear} Cold Scout. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <span className="text-[10px] text-subtle uppercase tracking-widest font-medium">Built with precision</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
