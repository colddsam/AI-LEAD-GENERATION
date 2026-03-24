import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ArrowRight, Heart, Menu, X } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import Logo from '../ui/Logo';

export default function PublicNavbar() {
  const { isAuthenticated } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();
  const isHomePage = location.pathname === '/';

  // Prevent scroll when menu is open
  useEffect(() => {
    if (isMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
  }, [isMenuOpen]);

  // Handle link click to close menu
  const handleLinkClick = () => {
    setIsMenuOpen(false);
  };

  const navLinks = [
    { name: 'Features', href: isHomePage ? '#features' : '/#features' },
    { name: 'How it works', href: isHomePage ? '#workflow' : '/#workflow' },
    { name: 'Pricing', href: '/pricing' },
    { name: 'Docs', href: '/docs' },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass-panel">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center" aria-label="Cold Scout Home" onClick={handleLinkClick}>
          <Logo size="md" />
        </Link>
        
        {/* Desktop Links */}
        <div className="hidden md:flex items-center gap-6">
          {navLinks.map((link) => (
            <a 
              key={link.name}
              href={link.href} 
              className={`text-sm transition-colors ${
                location.pathname === link.href ? 'text-black font-medium' : 'text-secondary hover:text-black'
              }`}
            >
              {link.name}
            </a>
          ))}
          <a 
            href="https://github.com/sponsors/colddsam" 
            target="_blank" 
            rel="noopener noreferrer"
            className="text-sm text-secondary hover:text-black transition-colors flex items-center gap-1"
          >
            <Heart className="w-3.5 h-3.5 fill-black text-black" /> Sponsor
          </a>
          <Link
            to={isAuthenticated ? '/overview' : '/login'}
            className="inline-flex items-center gap-2 bg-black text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-800 transition-colors"
          >
            {isAuthenticated ? 'Go to Dashboard' : 'Sign In'} <ArrowRight className="w-4 h-4 ml-1" />
          </Link>
        </div>

        {/* Mobile Toggle */}
        <button 
          className="md:hidden p-2 text-secondary hover:text-black transition-colors"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-label="Toggle Menu"
        >
          {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Menu Overlay */}
      {isMenuOpen && (
        <div className="md:hidden fixed inset-0 top-16 bg-white z-40 animate-fade-in">
          <div className="flex flex-col p-6 gap-6 h-full bg-white">
            {navLinks.map((link) => (
              <a 
                key={link.name}
                href={link.href} 
                className="text-lg font-medium text-black border-b border-gray-100 pb-4"
                onClick={handleLinkClick}
              >
                {link.name}
              </a>
            ))}
            <a 
              href="https://github.com/sponsors/colddsam" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-lg font-medium text-black border-b border-gray-100 pb-4 flex items-center gap-2"
              onClick={handleLinkClick}
            >
              <Heart className="w-5 h-5 fill-black text-black" /> Sponsor
            </a>
            <Link
              to={isAuthenticated ? '/overview' : '/login'}
              className="mt-4 inline-flex items-center justify-center gap-2 bg-black text-white px-6 py-4 rounded-md text-base font-medium hover:bg-gray-800 transition-colors"
              onClick={handleLinkClick}
            >
              {isAuthenticated ? 'Go to Dashboard' : 'Sign In'} <ArrowRight className="w-5 h-5 ml-1" />
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}
