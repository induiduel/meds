import React, { useEffect, useId, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { ChevronDown, Sparkles, X } from 'lucide-react';

/**
 * Künye seçicisi (kurul, ders, sene…): etiket + değer gösteren düğme; tıklayınca seçenek panelini açar.
 * Panel her zaman belgenin üst katmanına çizilir (kaydırılan pencere ya da sayfa animasyonu kırpmaz/kaydırmaz):
 * masaüstünde düğmeye göre konumlanan kutu (altta yer yoksa yukarı açılır), telefonda alttan açılan panel.
 * Esc ve dışarı tıklama kapatır; kapanış da animasyonludur.
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
  /** "token": yazma alanının altındaki küçük etiket görünümü (ms-meta-token) */
  variant?: 'field' | 'token';
  children: (close: () => void) => React.ReactNode;
}> = ({ label, value, icon: Icon, auto, empty, width = 280, title, variant = 'field', children }) => {
  const [open, setOpen] = useState(false);
  const [closing, setClosing] = useState(false);
  const [phone, setPhone] = useState(false);
  const [pos, setPos] = useState<{ top?: number; bottom?: number; left: number; maxH: number } | null>(null);
  const ref = useRef<HTMLDivElement>(null);
  const popRef = useRef<HTMLDivElement>(null);
  const id = useId();

  const close = () => {
    if (!open || closing) return;
    setClosing(true);
    window.setTimeout(() => {
      setOpen(false);
      setClosing(false);
    }, 160);
  };

  useEffect(() => {
    if (!open) return;
    const onDown = (e: MouseEvent) => {
      const t = e.target as Node;
      if (ref.current?.contains(t) || popRef.current?.contains(t)) return;
      close();
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.stopPropagation();
        close();
      }
    };
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey, true);
    return () => {
      document.removeEventListener('mousedown', onDown);
      document.removeEventListener('keydown', onKey, true);
    };
  }); // eslint-disable-line react-hooks/exhaustive-deps

  // Masaüstü konumu: düğmenin altı (yer yoksa üstü), ekrana sığacak kadar
  const place = () => {
    const btn = ref.current?.querySelector('button');
    if (!btn) return;
    const r = btn.getBoundingClientRect();
    const vh = window.innerHeight;
    const vw = window.innerWidth;
    const w = Math.min(Math.max(width, r.width), vw - 16);
    const left = Math.min(Math.max(8, r.left), vw - w - 8);
    const below = vh - r.bottom - 14;
    const above = r.top - 14;
    const want = Math.min(popRef.current?.scrollHeight || 360, 420);
    if (below >= Math.min(want, 260) || below >= above) setPos({ top: r.bottom + 6, left, maxH: Math.max(160, Math.min(420, below)) });
    else setPos({ bottom: vh - r.top + 6, left, maxH: Math.max(160, Math.min(420, above)) });
  };
  useLayoutEffect(() => {
    if (!open || phone) return;
    place();
    const raf = requestAnimationFrame(place);
    window.addEventListener('resize', place);
    window.addEventListener('scroll', place, true);
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener('resize', place);
      window.removeEventListener('scroll', place, true);
    };
  }, [open, phone]); // eslint-disable-line react-hooks/exhaustive-deps

  const toggle = () => {
    if (open) return close();
    setPhone(window.matchMedia('(max-width: 767px)').matches);
    setPos(null);
    setOpen(true);
  };

  return (
    <div className={`qa-pick ${open && !closing ? 'is-open' : ''}`} ref={ref}>
      <button
        type="button"
        className={variant === 'token' ? `ms-meta-token qa-mtok ${auto ? 'is-auto' : ''} ${empty ? 'is-empty' : ''}` : `qa-tok ${auto ? 'is-auto' : ''} ${empty ? 'is-empty' : ''}`}
        onClick={toggle}
        aria-haspopup="dialog"
        aria-expanded={open && !closing}
        aria-controls={open ? id : undefined}
        title={title}
      >
        {variant === 'token' ? (
          <>
            {Icon && <Icon className="w-3.5 h-3.5 shrink-0" aria-hidden />}
            <span className="sr-only">{label}: </span>
            <span className="truncate">{value}</span>
            {auto && <Sparkles className="ms-meta-auto w-3 h-3 shrink-0" aria-label="otomatik dolduruldu" />}
            <ChevronDown className="qa-mtok-c w-3.5 h-3.5 shrink-0 opacity-60" aria-hidden />
          </>
        ) : (
          <>
            {Icon && <Icon className="qa-tok-i" aria-hidden />}
            <span className="qa-tok-l">{label}</span>
            <span className="qa-tok-v">{value}</span>
            {auto && <Sparkles className="qa-tok-auto" aria-label="otomatik dolduruldu" />}
            <ChevronDown className="qa-tok-c" aria-hidden />
          </>
        )}
      </button>
      {open &&
        createPortal(
          <>
            {phone && <button type="button" className={`qa-pop-scrim ${closing ? 'is-closing' : ''}`} aria-label="Kapat" onClick={close} />}
            <div
              ref={popRef}
              className={`qa-pop ${phone ? 'is-sheet' : 'is-float'} ${closing ? 'is-closing' : ''}`}
              id={id}
              role="dialog"
              aria-label={label}
              style={
                phone
                  ? undefined
                  : { top: pos?.top, bottom: pos?.bottom, left: pos?.left ?? 8, width, maxHeight: pos?.maxH, visibility: pos ? 'visible' : 'hidden' }
              }
            >
              <div className="qa-pop-head">
                <b>{label}</b>
                <button type="button" onClick={close} aria-label="Kapat"><X /></button>
              </div>
              {children(close)}
            </div>
          </>,
          document.body
        )}
    </div>
  );
};
