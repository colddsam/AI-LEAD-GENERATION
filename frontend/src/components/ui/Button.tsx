/**
 * Interactive Button Component.
 * 
 * Highly configurable action element supporting various semantic styles, sizes,
 * and an integrated 'loading' state for async operations.
 */
import { cn } from '../../lib/utils';
import { Loader2 } from 'lucide-react';
import type { ButtonHTMLAttributes, ReactNode } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual variant affecting the button's color and background */
  variant?: 'primary' | 'danger' | 'ghost' | 'outline';
  /** Size multiplier for padding and font dimensions */
  size?: 'sm' | 'md' | 'lg';
  /** Indicates if a background process is active; disables interaction and shows a spinner */
  loading?: boolean;
  /** Optional Lucide icon to display before the label */
  icon?: ReactNode;
}

const variants: Record<string, string> = {
  primary: 'bg-black text-white hover:bg-gray-800 font-medium border border-black',
  danger: 'bg-white text-black border-2 border-black hover:bg-black hover:text-white font-bold',
  ghost: 'bg-transparent text-secondary hover:text-black hover:bg-gray-50',
  outline: 'bg-white text-black border border-gray-200 hover:border-black hover:shadow-vercel font-medium',
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
        'inline-flex items-center justify-center gap-2 rounded-md font-sans transition-all duration-200',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        variants[variant],
        sizes[size],
        className,
      )}
      disabled={disabled || loading}
      {...rest}
    >
      {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : (
        icon && <span className={cn(
          size === 'sm' ? 'w-3.5 h-3.5' : size === 'lg' ? 'w-5 h-5' : 'w-4 h-4',
          'flex items-center justify-center -ml-0.5'
        )}>{icon}</span>
      )}
      {children}
    </button>
  );
}
