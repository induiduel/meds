import React, { useEffect, useId, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { X } from 'lucide-react';

/**
 * Ortak alt sayfa (v8). Telefonda alttan açılır ve tutamaçtan/başlıktan sürüklenir; geniş ekranda
 * (≥640px) aynı içerik ortada pencere olur. Kurallar (tasarım sistemi · Hareket):
 *  - Arka sayfa kilitlenir, kaydırma konumu korunur; iç içe sayfalarda kilit sayılır.
 *  - Gövde kendi kayar (overscroll-behavior: contain) → kaydırma arka sayfaya zincirlenmez.
 *  - Sürükleme yalnız başlık bölgesinde başlar → gövde kaydırmasıyla çakışmaz.
 *  - Bırakınca: %35'ten fazla çekildiyse ya da hız > 0.5 px/ms ise kapanır, yoksa yayla geri döner.
 *  - Yükseklik görsel alana (--vvh) göre: klavye açılınca sayfa zıplamaz.
 *  - Esc kapatır, açılınca odak pencereye geçer, kapanınca önceki öğeye döner; Tab pencerede kalır.
 */
let lockCount = 0;
let savedY = 0;
function lockScroll() {
  if (lockCount++ > 0) return;
  savedY = window.scrollY;
  const b = document.body.style;
  b.position = 'fixed';
  b.top = `-${savedY}px`;
  b.left = '0';
  b.right = '0';
  b.width = '100%';
}
function unlockScroll() {
  if (--lockCount > 0) return;
  const b = document.body.style;
  b.position = b.top = b.left = b.right = b.width = '';
  window.scrollTo(0, savedY);
}

export interface SheetProps {
  open: boolean;
  onClose: () => void;
  title?: React.ReactNode;
  subtitle?: React.ReactNode;
  /** Başlığın sağında ek araçlar */
  actions?: React.ReactNode;
  footer?: React.ReactNode;
  /** 'auto': içerik kadar (en çok %92) · 'full': her zaman %92 */
  size?: 'auto' | 'full';
  /** Geniş ekranda pencere genişliği (px) */
  width?: number;
  /** Erişilebilir ad (title metin değilse) */
  label?: string;
  hideClose?: boolean;
  /** Gövde iç boşluğu olmasın (içerik kendi başlık/gövdesini getiriyorsa) */
  bare?: boolean;
  children: React.ReactNode;
}

export const Sheet: React.FC<SheetProps> = (props) => {
  // Kapanış animasyonu bitene kadar DOM'da kal
  const [mounted, setMounted] = useState(props.open);
  const [closing, setClosing] = useState(false);
  useEffect(() => {
    if (props.open) {
      setMounted(true);
      setClosing(false);
    } else if (mounted) {
      setClosing(true);
      const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const t = window.setTimeout(() => {
        setMounted(false);
        setClosing(false);
      }, reduce ? 0 : 240);
      return () => window.clearTimeout(t);
    }
  }, [props.open]);
  if (!mounted) return null;
  return createPortal(<SheetPanel {...props} closing={closing} />, document.body);
};

const SheetPanel: React.FC<SheetProps & { closing: boolean }> = ({ onClose, title, subtitle, actions, footer, size = 'auto', width = 520, label, hideClose, bare, children, closing }) => {
  const id = useId();
  const panelRef = useRef<HTMLDivElement>(null);
  const [dy, setDy] = useState(0);
  const [dragging, setDragging] = useState(false);
  const drag = useRef<{ y: number; t: number; lastY: number; lastT: number; v: number } | null>(null);
  const closeRef = useRef(onClose);
  closeRef.current = onClose;

  useLayoutEffect(() => {
    lockScroll();
    return unlockScroll;
  }, []);

  useEffect(() => {
    const prev = document.activeElement as HTMLElement | null;
    panelRef.current?.focus({ preventScroll: true });
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.stopPropagation();
        closeRef.current();
      }
      if (e.key === 'Tab' && panelRef.current) {
        const f = panelRef.current.querySelectorAll<HTMLElement>('a[href],button:not([disabled]),input:not([disabled]),select,textarea,[tabindex]:not([tabindex="-1"])');
        if (!f.length) return;
        const first = f[0];
        const last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    };
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('keydown', onKey);
      prev?.focus?.({ preventScroll: true });
    };
  }, []);

  const isSheet = () => window.matchMedia('(max-width: 639px)').matches;
  const onDown = (e: React.PointerEvent) => {
    if (!isSheet() || (e.target as HTMLElement).closest('button,a,input,select,textarea')) return;
    try {
      (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    } catch {
      /* sentetik olay */
    }
    const now = performance.now();
    drag.current = { y: e.clientY, t: now, lastY: e.clientY, lastT: now, v: 0 };
    setDragging(true);
  };
  const onMove = (e: React.PointerEvent) => {
    const d = drag.current;
    if (!d) return;
    const now = performance.now();
    d.v = (e.clientY - d.lastY) / Math.max(1, now - d.lastT);
    d.lastY = e.clientY;
    d.lastT = now;
    const raw = e.clientY - d.y;
    // Yukarı çekişte direnç: sayfa yerinden kopmaz
    setDy(raw > 0 ? raw : -Math.min(24, Math.sqrt(-raw) * 3));
  };
  const onUp = () => {
    const d = drag.current;
    drag.current = null;
    setDragging(false);
    if (!d) return;
    const h = panelRef.current?.offsetHeight || 1;
    if (dy > h * 0.35 || d.v > 0.5) onClose();
    else setDy(0);
  };

  const style = {
    '--sheet-w': `${width}px`,
    transform: dy ? `translate3d(0, ${Math.max(dy, -24)}px, 0)` : undefined,
    transition: dragging ? 'none' : undefined,
  } as React.CSSProperties;

  return (
    <div className={`sh-sheet-root ${closing ? 'is-closing' : ''}`}>
      <div
        className="sh-sheet-backdrop"
        aria-hidden="true"
        onClick={onClose}
        style={dy > 0 ? { opacity: Math.max(0.15, 1 - dy / 400) } : undefined}
      />
      <div
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-label={label}
        aria-labelledby={title && !label ? `${id}-t` : undefined}
        tabIndex={-1}
        className={`sh-sheet ${size === 'full' ? 'is-full' : ''}`}
        style={style}
      >
        <div className="sh-sheet-head" onPointerDown={onDown} onPointerMove={onMove} onPointerUp={onUp} onPointerCancel={onUp}>
          <span className="sh-sheet-grab" aria-hidden="true" />
          {(title || actions || !hideClose) && !bare && (
            <div className="sh-sheet-bar">
              <div className="min-w-0 flex-1">
                {title && <h2 id={`${id}-t`} className="sh-sheet-title">{title}</h2>}
                {subtitle && <p className="sh-sheet-sub">{subtitle}</p>}
              </div>
              {actions}
              {!hideClose && (
                <button type="button" className="sh-sheet-x" aria-label="Kapat" onClick={onClose}>
                  <X />
                </button>
              )}
            </div>
          )}
        </div>
        <div className={`sh-sheet-body ${bare ? 'is-bare' : ''}`}>{children}</div>
        {footer && <div className="sh-sheet-foot">{footer}</div>}
      </div>
    </div>
  );
};
