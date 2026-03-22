import { cn } from '../../lib/utils';

interface StatusDotProps {
  status: 'live' | 'hold' | 'error' | 'unknown';
  className?: string;
}

const dotStyles: Record<string, string> = {
  live: 'bg-green-400',
  hold: 'bg-amber-500',
  error: 'bg-red-500',
  unknown: 'bg-gray-500',
};

export default function StatusDot({ status, className }: StatusDotProps) {
  return (
    <span className={cn('relative inline-flex h-2.5 w-2.5', className)}>
      {status === 'live' && (
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
      )}
      <span className={cn('relative inline-flex rounded-full h-2.5 w-2.5', dotStyles[status])} />
    </span>
  );
}
