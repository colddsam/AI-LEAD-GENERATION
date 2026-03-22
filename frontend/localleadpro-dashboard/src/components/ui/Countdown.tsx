import { useState, useEffect } from 'react';
import { differenceInSeconds, parseISO } from 'date-fns';

interface CountdownProps {
  to: string | null;
}

export default function Countdown({ to }: CountdownProps) {
  const [display, setDisplay] = useState('—');

  useEffect(() => {
    if (!to) {
      return;
    }

    const update = () => {
      const target = parseISO(to);
      const now = new Date();
      const diff = differenceInSeconds(target, now);

      if (diff <= 0) {
        setDisplay('now');
        return;
      }

      const h = Math.floor(diff / 3600);
      const m = Math.floor((diff % 3600) / 60);
      const s = diff % 60;

      if (h > 0) {
        setDisplay(`${h}h ${m}m ${s}s`);
      } else if (m > 0) {
        setDisplay(`${m}m ${s}s`);
      } else {
        setDisplay(`${s}s`);
      }
    };

    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, [to]);

  if (!to) {
    return <span className="font-mono text-coldscout-teal tabular-nums">—</span>;
  }

  return (
    <span className="font-mono text-coldscout-teal tabular-nums">
      {display !== '—' && display !== 'now' ? `in ${display}` : display}
    </span>
  );
}
