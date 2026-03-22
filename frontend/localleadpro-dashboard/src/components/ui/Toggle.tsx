/**
 * Accessible Binary Switch Component.
 * 
 * Primarily used for administrative system toggles (e.g., Hold/Run).
 * Features animated transitions and customizable labels for each state.
 */
import { cn } from '../../lib/utils';

interface ToggleProps {
  /** The current Boolean state of the toggle */
  value: boolean;
  /** Callback triggered when the switch position is toggled */
  onChange: (v: boolean) => void;
  /** Label text shown in the 'true' state */
  labelOn?: string;
  /** Label text shown in the 'false' state */
  labelOff?: string;
  /** Background color class for the 'true' state */
  colorOn?: string;
  /** Background color class for the 'false' state */
  colorOff?: string;
  /** Interaction lock for the toggle */
  disabled?: boolean;
}

export default function Toggle({
  value,
  onChange,
  labelOn = 'RUN',
  labelOff = 'HOLD',
  colorOn = 'bg-black',
  colorOff = 'bg-gray-300',
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
        value ? 'left-2.5 text-white' : 'right-2 text-gray-600',
      )}>
        {value ? labelOn : labelOff}
      </span>
    </button>
  );
}
