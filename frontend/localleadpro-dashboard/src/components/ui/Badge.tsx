import { cn } from '../../lib/utils';
import type { LeadStatus } from '../../lib/api';
import { STATUS_COLORS } from '../../lib/constants';

interface BadgeProps {
  label: string;
  variant?: 'green' | 'teal' | 'amber' | 'red' | 'muted';
  className?: string;
}

const variantStyles: Record<string, string> = {
  green: 'bg-green-400/10 text-green-400 border-green-400/30',
  teal: 'bg-coldscout-teal/10 text-coldscout-teal border-coldscout-teal/30',
  amber: 'bg-amber-500/10 text-amber-500 border-amber-500/30',
  red: 'bg-red-500/10 text-red-500 border-red-500/30',
  muted: 'bg-navy-700/50 text-gray-400 border-gray-600/30',
};

const dotColors: Record<string, string> = {
  green: 'bg-green-400',
  teal: 'bg-coldscout-teal',
  amber: 'bg-amber-500',
  red: 'bg-red-500',
  muted: 'bg-gray-500',
};

/**
 * A highly customizable badge component used for displaying status, tags, and labels.
 * Supports multiple semantic variants and includes a status indicator dot.
 */
export default function Badge({ label, variant = 'muted', className }: BadgeProps) {
  return (
    <span className={cn(
      'inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border font-mono',
      variantStyles[variant],
      className,
    )}>
      <span className={cn('w-1.5 h-1.5 rounded-full', dotColors[variant])} />
      {label}
    </span>
  );
}

/**
 * Higher-order utility to render a themed badge based on a Lead's status.
 * Automatically maps status keys to the correct color variant and label.
 */
// eslint-disable-next-line react-refresh/only-export-components
export function statusBadge(status: LeadStatus | string) {
  const variant = (STATUS_COLORS[status] || 'muted') as BadgeProps['variant'];
  const label = status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ');
  return <Badge label={label} variant={variant} />;
}
