import { cn } from '../../lib/utils';

interface ToggleProps {
  value: boolean;
  onChange: (v: boolean) => void;
  labelOn?: string;
  labelOff?: string;
  colorOn?: string;
  colorOff?: string;
  disabled?: boolean;
}

export default function Toggle({
  value,
  onChange,
  labelOn = 'RUN',
  labelOff = 'HOLD',
  colorOn = 'bg-coldscout-teal',
  colorOff = 'bg-red-500',
  disabled = false,
}: ToggleProps) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={() => onChange(!value)}
      className={cn(
        'relative inline-flex h-8 w-20 items-center rounded-full transition-colors duration-300 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed',
        value ? colorOn : colorOff,
      )}
    >
      <span
        className={cn(
          'absolute left-1 flex h-6 w-6 items-center justify-center rounded-full bg-white shadow-md transition-transform duration-300',
          value && 'translate-x-12',
        )}
      />
      <span className={cn(
        'absolute text-xs font-mono font-semibold transition-all',
        value ? 'left-2.5 text-navy-900' : 'right-2 text-white',
      )}>
        {value ? labelOn : labelOff}
      </span>
    </button>
  );
}
