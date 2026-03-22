/**
 * Presentational Card Components.
 * 
 * Provides structural containers for dashboard modules and specific 'StatCard'
 * variants for high-level KPI visualization.
 */
import { cn } from '../../lib/utils';
import type { ReactNode } from 'react';

interface CardProps {
  /** Inner content of the card */
  children: ReactNode;
  /** Additional CSS classes */
  className?: string;
  /** Enables the Vercel-style shadow hover effect */
  glow?: boolean;
  /** Automatically applies standard padding */
  padding?: boolean;
}

/**
 * Foundational container component with consistent styling.
 * Uses Vercel-style shadow on hover and clean white background.
 */
export default function Card({ children, className, glow = true, padding = true }: CardProps) {
  return (
    <div
      className={cn(
        'rounded-lg bg-white border border-gray-200',
        glow && 'hover:shadow-vercel transition-shadow duration-300',
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
    <Card className={cn('relative overflow-hidden group hover:shadow-vercel-hover', className)}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-[10px] text-secondary uppercase tracking-widest font-semibold mb-2">{label}</p>
          <p className="text-3xl font-bold text-black tracking-tighter">{value}</p>
          {trend && (
            <p className="text-xs text-coldscout-teal-dark mt-1 font-mono">{trend}</p>
          )}
        </div>
        {icon && (
          <div className="text-gray-200 group-hover:text-gray-300 transition-colors mt-1">{icon}</div>
        )}
      </div>
    </Card>
  );
}
