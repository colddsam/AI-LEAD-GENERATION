import { Link } from 'react-router-dom';
import { Heart, Github, Mail } from 'lucide-react';
import Logo from '../ui/Logo';

export default function PublicFooter() {
  const currentYear = new Date().getFullYear();

  return (
    <footer
      className="border-t border-gray-200 py-12 bg-white relative z-10"
      role="contentinfo"
      aria-label="Site footer"
      itemScope
      itemType="https://schema.org/WPFooter"
    >
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex flex-col md:flex-row items-start justify-between gap-12 mb-12">
          {/* Brand */}
          <div
            className="flex flex-col gap-4 max-w-sm"
            itemScope
            itemType="https://schema.org/Organization"
          >
            <meta itemProp="name" content="Cold Scout" />
            <meta itemProp="url" content="https://coldscout.colddsam.com/" />
            <Link to="/" className="flex items-center" aria-label="Cold Scout Home" itemProp="url">
              <Logo size="sm" />
            </Link>
            <p className="text-sm text-secondary leading-relaxed" itemProp="description">
              AI-powered lead generation platform that discovers, qualifies, and engages local business leads at scale.
            </p>
            <div className="flex items-center gap-4">
              <a
                href="https://github.com/colddsam/coldscout"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="Cold Scout on GitHub"
                className="text-secondary hover:text-black transition-colors"
                itemProp="sameAs"
              >
                <Github className="w-4 h-4" />
              </a>
              <a
                href="mailto:admin@colddsam.com"
                aria-label="Email Cold Scout support"
                className="text-secondary hover:text-black transition-colors"
                itemProp="email"
              >
                <Mail className="w-4 h-4" />
              </a>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-12 md:gap-24">
            {/* Product */}
            <div className="flex flex-col gap-4">
              <h2 className="text-sm font-bold text-black uppercase tracking-wider">Product</h2>
              <nav className="flex flex-col gap-2" aria-label="Product navigation">
                <a href="/#features" className="text-sm text-secondary hover:text-black transition-colors">Features</a>
                <a href="/#workflow" className="text-sm text-secondary hover:text-black transition-colors">How it works</a>
                <a href="/#faq" className="text-sm text-secondary hover:text-black transition-colors">FAQ</a>
                <Link to="/pricing" className="text-sm text-secondary hover:text-black transition-colors">Pricing</Link>
                <Link to="/docs" className="text-sm text-secondary hover:text-black transition-colors">Documentation</Link>
                <Link to="/support" className="text-sm text-secondary hover:text-black transition-colors">Support</Link>
              </nav>
            </div>

            {/* Legal */}
            <div className="flex flex-col gap-4">
              <h2 className="text-sm font-bold text-black uppercase tracking-wider">Legal</h2>
              <nav className="flex flex-col gap-2" aria-label="Legal navigation">
                <Link to="/privacy" className="text-sm text-secondary hover:text-black transition-colors">Privacy Policy</Link>
                <Link to="/terms" className="text-sm text-secondary hover:text-black transition-colors">Terms of Service</Link>
                <Link to="/refund-policy" className="text-sm text-secondary hover:text-black transition-colors">Refund Policy</Link>
                <Link to="/delete-data" className="text-sm text-secondary hover:text-black transition-colors">Data Deletion</Link>
              </nav>
            </div>

            {/* Community */}
            <div className="flex flex-col gap-4">
              <h2 className="text-sm font-bold text-black uppercase tracking-wider">Community</h2>
              <nav className="flex flex-col gap-2" aria-label="Community navigation">
                <a
                  href="https://github.com/colddsam/coldscout"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-secondary hover:text-black transition-colors"
                >
                  GitHub Repository
                </a>
                <a
                  href="https://github.com/colddsam/coldscout/issues"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-secondary hover:text-black transition-colors"
                >
                  Report an Issue
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
            <a href="/sitemap.xml" className="text-[10px] text-subtle hover:text-black transition-colors uppercase tracking-widest font-medium" aria-label="XML Sitemap">
              Sitemap
            </a>
            <a href="/robots.txt" className="text-[10px] text-subtle hover:text-black transition-colors uppercase tracking-widest font-medium" aria-label="Robots.txt">
              Robots
            </a>
            <span className="text-[10px] text-subtle uppercase tracking-widest font-medium">Built with precision</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
