/**
 * Persistent Header / Topbar Component.
 * 
 * Displays context-aware page titles, real-time system health metrics,
 * and the administrative "System Hold" safety toggle.
 * Integrates with the application state to show data freshness timestamps.
 */
import { useLocation } from 'react-router-dom';
import { useHealth, useSystemToggle } from '../../hooks/useConfig';
import Badge from '../ui/Badge';
import { useState } from 'react';
import Modal from '../ui/Modal';
import Button from '../ui/Button';
import { NAV_ITEMS } from '../../lib/constants';
import { timeAgo } from '../../lib/utils';

import { Menu } from 'lucide-react';

interface TopbarProps {
  /** Callback triggered to reveal the mobile navigation sidebar */
  onMenuClick: () => void;
}

export default function Topbar({ onMenuClick }: TopbarProps) {
  const location = useLocation();
  const { data: health, dataUpdatedAt } = useHealth();
  const systemToggle = useSystemToggle();
  const [showConfirm, setShowConfirm] = useState(false);

  const currentNav = NAV_ITEMS.find((n) => location.pathname.startsWith(n.path));
  const pageTitle = currentNav?.label || 'Dashboard';
  const isRunning = health?.production_status === true;

  const handleToggle = () => {
    setShowConfirm(true);
  };

  const confirmToggle = () => {
    systemToggle.mutate(isRunning ? 'hold' : 'resume');
    setShowConfirm(false);
  };

  return (
    <>
      <header className="flex items-center justify-between h-14 px-4 md:px-6 bg-white border-b border-gray-200">
        <div className="flex items-center gap-4">
          <button
            onClick={onMenuClick}
            className="lg:hidden p-1.5 text-secondary hover:text-black transition-colors"
          >
            <Menu className="w-6 h-6" />
          </button>
          <h1 className="text-base md:text-lg font-semibold text-black tracking-tight whitespace-nowrap">{pageTitle}</h1>
        </div>

        <div className="flex items-center gap-3 md:gap-4">
          {/* Last updated */}
          <span className="hidden sm:inline text-[10px] md:text-xs font-mono text-subtle">
            Updated {dataUpdatedAt ? timeAgo(new Date(dataUpdatedAt).toISOString()) : '—'}
          </span>

          {/* Health */}
          {health && (
            <Badge
              label={health.status === 'healthy' ? 'Healthy' : 'Error'}
              variant={health.status === 'healthy' ? 'green' : 'red'}
              className="hidden xs:flex"
            />
          )}

          {/* System Toggle */}
          <Button
            variant={isRunning ? 'danger' : 'primary'}
            size="sm"
            onClick={handleToggle}
            loading={systemToggle.isPending}
            className="px-2 md:px-4 text-[10px] md:text-xs"
          >
            <span className="hidden xs:inline">{isRunning ? '⏸ HOLD SYSTEM' : '▶ RESUME SYSTEM'}</span>
            <span className="xs:hidden">{isRunning ? '⏸' : '▶'}</span>
          </Button>
        </div>
      </header>

      <Modal open={showConfirm} onClose={() => setShowConfirm(false)} title="Confirm System Toggle">
        <p className="text-secondary text-sm mb-4">
          {isRunning
            ? 'This will pause ALL automated pipeline operations. Are you sure?'
            : 'This will resume all automated pipeline operations. Are you sure?'}
        </p>
        <div className="flex gap-3 justify-end">
          <Button variant="ghost" onClick={() => setShowConfirm(false)}>Cancel</Button>
          <Button variant={isRunning ? 'danger' : 'primary'} onClick={confirmToggle}>
            {isRunning ? 'Hold System' : 'Resume System'}
          </Button>
        </div>
      </Modal>
    </>
  );
}
