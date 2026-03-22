import { cn } from '../../lib/utils';
import type { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  glow?: boolean;
  padding?: boolean;
}

/**
 * Foundational container component with consistent corner rounding and background styling.
 * Optionally supports a subtle "glassmorphism" glow effect and internal padding.
 */
export default function Card({ children, className, glow = true, padding = true }: CardProps) {
  return (
    <div
      className={cn(
        'rounded-xl bg-navy-800',
        glow && 'card-glow',
        padding && 'p-5',
        className,
      )}
    >
      {children}
    </div>
  );
}

interface StatCardProps {
  label: string;
  value: string | number;
  icon?: ReactNode;
  trend?: string;
  className?: string;
}

/**
 * Specialized card designed for high-level dashboard metrics.
 * Displays a label, a primary value, and an optional icon or trend indicator.
 */
export function StatCard({ label, value, icon, trend, className }: StatCardProps) {
  return (
    <Card className={cn('grid-bg relative overflow-hidden', className)}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs text-gray-400 uppercase tracking-wider mb-1 font-mono">{label}</p>
          <p className="text-3xl font-mono font-semibold text-white">{value}</p>
          {trend && (
            <p className="text-xs text-coldscout-teal mt-1 font-mono">{trend}</p>
          )}
        </div>
        {icon && (
          <div className="text-coldscout-teal/30 mt-1">{icon}</div>
        )}
      </div>
    </Card>
  );
}
