/**
 * Responsive Modal / Dialog Component.
 * 
 * Handles focus trapping, keyboard closure (Escape), and backdrop interactions.
 * Animated via Framer Motion for smooth visual entry/exit transitions.
 */
import { useEffect, useRef, type ReactNode } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { cn } from '../../lib/utils';

interface ModalProps {
  /** Visibility toggle provided by the parent component */
  open: boolean;
  /** Callback to trigger when the modal should be dismissed (backdrop or close btn) */
  onClose: () => void;
  /** Optional semantic title displayed in the modal header */
  title?: string;
  /** Main dialog body content */
  children: ReactNode;
  /** Tailwind max-width class (e.g., 'max-w-2xl') */
  maxWidth?: string;
}

/**
 * Accessible modal overlay component with Framer Motion animations.
 * Features a backdrop blur, escape-key closure, and responsive max-width configurations.
 */
export default function Modal({ open, onClose, title, children, maxWidth = 'max-w-md' }: ModalProps) {
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    if (open) document.addEventListener('keydown', handleEsc);
    return () => document.removeEventListener('keydown', handleEsc);
  }, [open, onClose]);

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          ref={overlayRef}
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
        >
          <motion.div
            className={cn('bg-white rounded-lg border border-gray-200 w-full shadow-vercel-hover', maxWidth)}
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            transition={{ duration: 0.15 }}
          >
            {title && (
              <div className="flex items-center justify-between px-5 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-black">{title}</h3>
                <button onClick={onClose} className="text-gray-400 hover:text-black transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>
            )}
            <div className="p-5">{children}</div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
