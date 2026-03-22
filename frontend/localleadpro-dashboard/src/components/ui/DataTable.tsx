/**
 * Generic Data Table Component.
 * 
 * Provides a standardized, type-safe way to display tabular data.
 * Supports:
 * - Custom column rendering via a `render` function.
 * - Loading states with animated skeleton rows.
 * - Interactive row clicks for navigation or selection.
 * - Responsive horizontal scrolling for large data sets.
 */
import { cn } from '../../lib/utils';
import type { ReactNode } from 'react';

export interface Column<T> {
  /** Unique key identifying the data property for this column */
  key: string;
  /** Display label shown in the table header */
  label: string;
  /** Optional function to customize the cell content rendering */
  render?: (value: unknown, row: T) => ReactNode;
  /** Enables visual sorting indicators (future support) */
  sortable?: boolean;
  /** CSS width constraint for the column */
  width?: string;
}

interface DataTableProps<T> {
  /** Array of column configurations */
  columns: Column<T>[];
  /** The raw data array to display */
  data: T[];
  /** Callback triggered when a row is clicked */
  onRowClick?: (row: T) => void;
  /** Visibility toggle for the loading skeleton state */
  loading?: boolean;
  /** Message displayed when the data array is empty */
  emptyMessage?: string;
  /** Additional CSS classes for the container */
  className?: string;
}

function SkeletonRow({ cols }: { cols: number }) {
  return (
    <tr className="border-b border-gray-100">
      {Array.from({ length: cols }).map((_, i) => (
        <td key={i} className="px-6 py-3">
          <div className="h-4 bg-gray-100 rounded animate-pulse" style={{ width: `${60 + ((i * 17) % 40)}%` }} />
        </td>
      ))}
    </tr>
  );
}

/**
 * Generic, type-safe data table component with support for custom column rendering,
 * loading skeletons, and interactive row clicks.
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
            <tr className="border-b border-gray-200">
              {columns.map((col) => (
                <th key={col.key} className="px-6 py-3 text-left text-[10px] font-semibold uppercase tracking-widest text-secondary" style={{ width: col.width }}>
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
      <div className="flex flex-col items-center justify-center py-16 text-secondary">
        <p className="font-mono text-sm">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className={cn('overflow-x-auto', className)}>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-200">
            {columns.map((col) => (
              <th key={col.key} className="px-6 py-3 text-left text-[10px] font-semibold uppercase tracking-widest text-secondary" style={{ width: col.width }}>
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
                'border-b border-gray-100 transition-colors',
                onRowClick && 'cursor-pointer hover:bg-gray-50',
              )}
            >
              {columns.map((col) => (
                <td key={col.key} className="px-6 py-4 text-secondary">
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
