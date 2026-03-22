import { cn } from '../../lib/utils';
import { Loader2 } from 'lucide-react';
import type { ButtonHTMLAttributes, ReactNode } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'danger' | 'ghost' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: ReactNode;
}

const variants: Record<string, string> = {
  primary: 'bg-coldscout-teal text-navy-900 hover:bg-[#b8e5e3] font-bold shadow-lg shadow-coldscout-teal/10 hover:shadow-coldscout-teal/20',
  danger: 'bg-red-500 text-white hover:bg-red-400 font-semibold shadow-lg shadow-red-500/20',
  ghost: 'bg-transparent text-gray-400 hover:text-coldscout-teal hover:bg-navy-700/50',
  outline: 'bg-transparent text-coldscout-teal border border-coldscout-teal/30 hover:bg-coldscout-teal/10',
};

const sizes: Record<string, string> = {
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base',
};

/**
 * Core button component with multiple stylistic variants (primary, danger, ghost, outline)
 * and an integrated loading state with a spinner.
 */
export default function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  icon,
  children,
  className,
  disabled,
  ...rest
}: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-lg font-body transition-all duration-200',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        variants[variant],
        sizes[size],
        className,
      )}
      disabled={disabled || loading}
      {...rest}
    >
      {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : icon}
      {children}
    </button>
  );
}
