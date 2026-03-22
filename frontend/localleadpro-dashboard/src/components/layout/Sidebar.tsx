import { NavLink } from 'react-router-dom';
import { cn } from '../../lib/utils';
import { NAV_ITEMS } from '../../lib/constants';
import { useHealth } from '../../hooks/useConfig';
import StatusDot from '../ui/StatusDot';
import {
  LayoutDashboard, GitBranch, Clock, Users, Send, Inbox,
  BarChart2, Settings, ChevronLeft, ChevronRight, Radar, LogOut
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

const ICON_MAP: Record<string, React.ElementType> = {
  LayoutDashboard, GitBranch, Clock, Users, Send, Inbox, BarChart2, Settings,
};

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
  mobileOpen?: boolean;
  onMobileClose?: () => void;
}

export default function Sidebar({ collapsed, onToggle, mobileOpen, onMobileClose }: SidebarProps) {
  const { data: health } = useHealth();
  const { logout } = useAuth();
  const isRunning = health?.production_status === true;

  return (
    <>
      {/* Mobile Overlay */}
      <div 
        className={cn(
          "fixed inset-0 bg-navy-950/80 backdrop-blur-sm z-40 transition-opacity lg:hidden",
          mobileOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        )}
        onClick={onMobileClose}
      />

      <aside className={cn(
        'flex flex-col bg-navy-900 border-r border-white/5 transition-all duration-300 z-50',
        'fixed inset-y-0 left-0 lg:static', // Responsive positioning
        collapsed ? 'w-16' : 'w-60',
        !mobileOpen && '-translate-x-full lg:translate-x-0', // Hide on mobile unless open
      )}>
        {/* Logo */}
        <div className="flex items-center justify-between px-4 h-14 border-b border-white/5">
          <div className="flex items-center gap-3">
            <div className="flex-shrink-0">
              <Radar className="w-7 h-7 text-coldscout-teal" fill="rgba(164,219,217,0.15)" />
            </div>
            {(!collapsed || mobileOpen) && (
              <span className="font-premium font-bold text-lg text-white tracking-tight">
                {(() => {
                  const name = import.meta.env.VITE_SITE_NAME || 'Cold Scout';
                  const parts = name.split(' ');
                  if (parts.length === 1) return name;
                  return (
                    <>
                      {parts[0]}
                      <span className="text-coldscout-teal ml-1">
                        {parts.slice(1).join(' ')}
                      </span>
                    </>
                  );
                })()}
              </span>
            )}
          </div>
          
          {/* Mobile Close Button */}
          {mobileOpen && (
            <button 
              onClick={onMobileClose}
              className="lg:hidden p-1 text-gray-500 hover:text-white"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Nav Items */}
        <nav className="flex-1 py-3 space-y-1 px-2 overflow-y-auto">
          {NAV_ITEMS.map((item) => {
            const Icon = ICON_MAP[item.icon];
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onMobileClose}
                className={({ isActive }) => cn(
                  'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200 group',
                  isActive
                    ? 'bg-coldscout-teal/10 text-coldscout-teal border-l-2 border-coldscout-teal'
                    : 'text-gray-400 hover:text-gray-200 hover:bg-navy-800',
                  collapsed && !mobileOpen && 'justify-center px-0',
                )}
              >
                {Icon && <Icon className="w-5 h-5 flex-shrink-0" />}
                {(!collapsed || mobileOpen) && <span className="font-body">{item.label}</span>}
              </NavLink>
            );
          })}
        </nav>

        {/* Bottom Area */}
        <div className="border-t border-white/5 p-3 space-y-2">
          {/* Logout Button */}
          <button
            onClick={() => {
              logout();
              onMobileClose?.();
            }}
            className={cn(
              "flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm transition-all duration-200",
              "text-red-400 hover:text-red-300 hover:bg-red-400/10",
              collapsed && !mobileOpen && "justify-center px-0"
            )}
            title="Logout"
          >
            <LogOut className="w-5 h-5 flex-shrink-0" />
            {(!collapsed || mobileOpen) && <span className="font-body">Logout</span>}
          </button>

          {/* System Status */}
          <div className={cn(
            'flex items-center gap-2 px-3 py-2 rounded-lg bg-navy-800/50',
            collapsed && !mobileOpen && 'justify-center px-0',
          )}>
            <StatusDot status={isRunning ? 'live' : 'hold'} />
            {(!collapsed || mobileOpen) && (
              <span className="text-xs font-mono text-gray-400">
                {isRunning ? 'SYSTEM RUN' : 'SYSTEM HOLD'}
              </span>
            )}
          </div>

          {/* Collapse Toggle (hide on mobile) */}
          <button
            onClick={onToggle}
            className="hidden lg:flex items-center justify-center w-full p-2 rounded-lg text-gray-500 hover:text-gray-300 hover:bg-navy-700/50 transition-colors"
          >
            {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        </div>
      </aside>
    </>
  );
}
