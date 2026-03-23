/**
 * Semantic Badge/Tag Component.
 * 
 * Primarily used for status indicators and categorical tagging.
 * Supports automated coloring based on the standard `LeadStatus`.
 */
import { cn } from '../../lib/utils';
import type { LeadStatus } from '../../lib/api';
import { STATUS_COLORS } from '../../lib/constants';

interface BadgeProps {
  /** Text content to be displayed in the badge */
  label: string;
  /** Semantic color theme matching the application's design system */
  variant?: 'green' | 'teal' | 'amber' | 'red' | 'muted';
  /** Additional CSS classes for custom positioning or sizing */
  className?: string;
}

const variantStyles: Record<string, string> = {
  green: 'bg-success-subtle text-green-700 border-green-200',
  teal: 'bg-teal-50 text-teal-700 border-teal-200',
  amber: 'bg-warning-subtle text-amber-700 border-amber-200',
  red: 'bg-danger-subtle text-red-700 border-red-200',
  muted: 'bg-accents-1 text-secondary border-accents-2',
};

const dotColors: Record<string, string> = {
  green: 'bg-success',
  teal: 'bg-teal-300',
  amber: 'bg-warning',
  red: 'bg-danger',
  muted: 'bg-accents-3',
};

/**
 * A highly customizable badge component used for displaying status, tags, and labels.
 * Supports multiple semantic variants and includes a status indicator dot.
 */
export default function Badge({ label, variant = 'muted', className }: BadgeProps) {
  return (
    <span className={cn(
      'inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-semibold border uppercase tracking-wider',
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
