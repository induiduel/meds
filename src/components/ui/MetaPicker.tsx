import React, { useEffect, useId, useRef, useState } from 'react';
import { ChevronDown, Sparkles, X } from 'lucide-react';

/**
 * Künye seçicisi: etiket + değer gösteren düğme; tıklayınca seçenek panelini açar.
 * Masaüstünde düğmenin altında açılır kutu, telefonda alttan açılan panel. Esc ve dışarı tıklama kapatır.
 */
export const MetaPicker: React.FC<{
  label: string;
  value: React.ReactNode;
  icon?: React.ElementType;
  /** Değer otomatik dolduruldu (ör. eşleşen taslaktan) */
  auto?: boolean;
  empty?: boolean;
  width?: number;
  title?: string;
  children: (close: () => void) => React.ReactNode;
}> = ({ label, value, icon: Icon, auto, empty, width = 280, title, children }) => {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const id = useId();
  useEffect(() => {
    if (!open) return;
    const onDown = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setOpen(false);
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDown);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);
  const close = () => setOpen(false);
  return (
    <div className={`qa-pick ${open ? 'is-open' : ''}`} ref={ref}>
      <button
        type="button"
        className={`qa-tok ${auto ? 'is-auto' : ''} ${empty ? 'is-empty' : ''}`}
        onClick={() => setOpen((v) => !v)}
        aria-haspopup="dialog"
        aria-expanded={open}
        aria-controls={open ? id : undefined}
        title={title}
      >
        {Icon && <Icon className="qa-tok-i" aria-hidden />}
        <span className="qa-tok-l">{label}</span>
        <span className="qa-tok-v">{value}</span>
        {auto && <Sparkles className="qa-tok-auto" aria-label="otomatik dolduruldu" />}
        <ChevronDown className="qa-tok-c" aria-hidden />
      </button>
      {open && (
        <>
          <button type="button" className="qa-pop-scrim" aria-label="Kapat" onClick={close} />
          <div className="qa-pop" id={id} role="dialog" aria-label={label} style={{ ['--w' as string]: `${width}px` }}>
            <div className="qa-pop-head">
              <b>{label}</b>
              <button type="button" onClick={close} aria-label="Kapat"><X /></button>
            </div>
            {children(close)}
          </div>
        </>
      )}
    </div>
  );
};
