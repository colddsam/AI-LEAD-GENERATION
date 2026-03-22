import type { ReactNode } from 'react';

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
}

export default function PageHeader({ title, subtitle, actions }: PageHeaderProps) {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h2 className="text-xl md:text-2xl font-display font-bold text-white">{title}</h2>
        {subtitle && <p className="text-xs md:text-sm text-gray-400 mt-1">{subtitle}</p>}
      </div>
      {actions && <div className="flex flex-wrap gap-2 md:gap-3">{actions}</div>}
    </div>
  );
}
