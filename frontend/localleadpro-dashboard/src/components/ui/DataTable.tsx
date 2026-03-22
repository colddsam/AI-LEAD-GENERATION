import { cn } from '../../lib/utils';
import type { ReactNode } from 'react';

export interface Column<T> {
  key: string;
  label: string;
  render?: (value: unknown, row: T) => ReactNode;
  sortable?: boolean;
  width?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  onRowClick?: (row: T) => void;
  loading?: boolean;
  emptyMessage?: string;
  className?: string;
}

function SkeletonRow({ cols }: { cols: number }) {
  return (
    <tr className="border-b border-white/5">
      {Array.from({ length: cols }).map((_, i) => (
        <td key={i} className="px-4 py-3">
          <div className="h-4 bg-navy-700 rounded animate-pulse" style={{ width: `${60 + ((i * 17) % 40)}%` }} />
        </td>
      ))}
    </tr>
  );
}

/**
 * Generic, type-safe data table component with support for custom column rendering,
 * loading skeletons, and interactive row clicks.
 * 
 * @template T - The shape of the data record being displayed.
 */
export default function DataTable<T extends Record<string, unknown>>({
  columns,
  data,
  onRowClick,
  loading = false,
  emptyMessage = 'No data available',
  className,
}: DataTableProps<T>) {
  if (loading) {
    return (
      <div className={cn('overflow-x-auto', className)}>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-white/10">
              {columns.map((col) => (
                <th key={col.key} className="px-4 py-3 text-left text-xs font-mono uppercase tracking-wider text-gray-400" style={{ width: col.width }}>
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: 8 }).map((_, i) => (
              <SkeletonRow key={i} cols={columns.length} />
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  if (!data.length) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-gray-500">
        <p className="font-mono text-sm">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className={cn('overflow-x-auto', className)}>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-white/10">
            {columns.map((col) => (
              <th key={col.key} className="px-4 py-3 text-left text-xs font-mono uppercase tracking-wider text-gray-400" style={{ width: col.width }}>
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr
              key={i}
              onClick={() => onRowClick?.(row)}
              className={cn(
                'border-b border-white/5 transition-colors',
                onRowClick && 'cursor-pointer hover:bg-navy-700/50',
              )}
            >
              {columns.map((col) => (
                <td key={col.key} className="px-4 py-3 text-gray-300">
                  {col.render
                    ? col.render(row[col.key], row)
                    : String(row[col.key] ?? '—')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
