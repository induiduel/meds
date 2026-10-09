import React, { useEffect, useId, useRef, useState } from 'react';
import { X } from 'lucide-react';

interface DialogProps {
  title: React.ReactNode;
  subtitle?: React.ReactNode;
  onClose: () => void;
  footer?: React.ReactNode;
  /** Tailwind max-w sınıfı (varsayılan max-w-xl) */
  width?: string;
  children: React.ReactNode;
  /** Gövde kendi içinde kaymasın (içerik kendi kaydırmasını yönetiyorsa) */
  bareBody?: boolean;
}

/**
 * Ortak pencere: sade beyaz başlık, kendi içinde kayan gövde, isteğe bağlı alt eylem şeridi.
 * Masaüstünde ortada, telefonda alttan açılan sayfa. Esc ve dış tıklama kapatır; açılınca odak pencereye geçer.
 */
export const Dialog: React.FC<DialogProps> = ({ title, subtitle, onClose, footer, width = 'max-w-xl', children, bareBody }) => {
  const id = useId();
  const panelRef = useRef<HTMLDivElement>(null);
  // Kapanış animasyonlu: Esc, dış tıklama ve kapat düğmesi önce çıkış animasyonunu oynatır
  const [closing, setClosing] = useState(false);
  const closingRef = useRef(false);
  const requestClose = () => {
    if (closingRef.current) return;
    closingRef.current = true;
    setClosing(true);
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    window.setTimeout(() => onClose(), reduce ? 0 : 190);
  };
  const closeRef = useRef(requestClose);
  closeRef.current = requestClose;

  useEffect(() => {
    const prevFocus = document.activeElement as HTMLElement | null;
    panelRef.current?.focus();
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && closeRef.current();
    document.addEventListener('keydown', onKey);
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = prevOverflow;
      prevFocus?.focus?.();
    };
  }, []);

  return (
    <div className={`ms-overlay fixed inset-0 z-[70] flex items-center justify-center p-4 ${closing ? 'is-closing' : ''}`} onMouseDown={(e) => e.target === e.currentTarget && requestClose()}>
      <div
        ref={panelRef}
        tabIndex={-1}
        role="dialog"
        aria-modal="true"
        aria-labelledby={`${id}-t`}
        className={`ms-modal-panel bg-white w-full ${width} flex flex-col overflow-hidden outline-none`}
      >
        <header className="flex items-start gap-2 px-5 pt-4 pb-3 border-b border-line-soft shrink-0">
          <div className="flex-1 min-w-0">
            <h2 id={`${id}-t`} className="m-0 font-display text-[17px] font-semibold leading-snug text-ink">{title}</h2>
            {subtitle && <p className="m-0 mt-0.5 text-[12.5px] text-ink-3">{subtitle}</p>}
          </div>
          <button type="button" onClick={requestClose} aria-label="Kapat" className="ms-btn is-ghost is-icon -mr-2 -mt-1">
            <X />
          </button>
        </header>
        <div className={bareBody ? 'flex-1 min-h-0 flex flex-col' : 'flex-1 min-h-0 overflow-y-auto overscroll-contain px-5 py-4 flex flex-col gap-4'}>{children}</div>
        {footer && (
          <footer className="flex flex-wrap items-center justify-end gap-2 px-5 py-3 border-t border-line-soft shrink-0" style={{ paddingBottom: 'max(0.75rem, env(safe-area-inset-bottom))' }}>
            {footer}
          </footer>
        )}
      </div>
    </div>
  );
};
