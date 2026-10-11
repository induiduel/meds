import React, { useEffect, useId, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { X } from 'lucide-react';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';

/**
 * Ortak alt sayfa (v8). Telefonda alttan açılır ve tutamaçtan/başlıktan sürüklenir; geniş ekranda
 * (≥640px) aynı içerik ortada pencere olur. Kurallar (tasarım sistemi · Hareket):
 *  - Arka sayfa ortak sayaçlı kilitle (utils/scrollLock) kilitlenir; kaydırma konumu yerinde kalır.
 *  - Gövde kendi kayar (overscroll-behavior: contain) → kaydırma arka sayfaya zincirlenmez.
 *  - Sürükleme başlıktan başlar; gövde en üstteyken aşağı çekiş de sayfayı sürükler (iOS tarzı devir).
 *  - Sürükleme React durumu değil doğrudan transform yazar (kare başına bir kez, rAF) → takılma olmaz.
 *  - Bırakınca: %35'ten fazla çekildiyse ya da hız > 0.5 px/ms ise kapanır, yoksa yayla geri döner.
 *  - Yükseklik görsel alana (--vvh) göre: klavye açılınca sayfa zıplamaz.
 *  - Esc kapatır, açılınca odak pencereye geçer, kapanınca önceki öğeye döner; Tab pencerede kalır.
 */
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
  const backRef = useRef<HTMLDivElement>(null);
  const bodyRef = useRef<HTMLDivElement>(null);
  const drag = useRef<{ y: number; lastY: number; lastT: number; v: number; dy: number } | null>(null);
  const raf = useRef(0);
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

  // Sürükleme konumunu doğrudan DOM'a yaz (kare başına bir kez)
  const paint = () => {
    raf.current = 0;
    const d = drag.current;
    const panel = panelRef.current;
    if (!panel) return;
    const dy = d ? d.dy : 0;
    panel.style.transform = dy ? `translate3d(0, ${Math.max(dy, -24)}px, 0)` : '';
    if (backRef.current) backRef.current.style.opacity = dy > 0 ? String(Math.max(0.15, 1 - dy / 400)) : '';
  };
  const schedule = () => {
    if (!raf.current) raf.current = requestAnimationFrame(paint);
  };
  const begin = (y: number) => {
    const now = performance.now();
    drag.current = { y, lastY: y, lastT: now, v: 0, dy: 0 };
    // Sürüklerken yay geçişi kapalı (parmağı birebir izlesin); bırakınca CSS geçişi geri gelir
    if (panelRef.current) panelRef.current.style.transition = 'none';
    if (backRef.current) backRef.current.style.transition = 'none';
  };
  const move = (y: number) => {
    const d = drag.current;
    if (!d) return;
    const now = performance.now();
    d.v = (y - d.lastY) / Math.max(1, now - d.lastT);
    d.lastY = y;
    d.lastT = now;
    const raw = y - d.y;
    // Yukarı çekişte direnç: sayfa yerinden kopmaz
    d.dy = raw > 0 ? raw : -Math.min(24, Math.sqrt(-raw) * 3);
    schedule();
  };
  const end = () => {
    const d = drag.current;
    drag.current = null;
    if (panelRef.current) panelRef.current.style.transition = '';
    if (backRef.current) backRef.current.style.transition = '';
    if (!d) return;
    const h = panelRef.current?.offsetHeight || 1;
    if (d.dy > h * 0.35 || d.v > 0.5) {
      closeRef.current();
    } else {
      schedule();
    }
  };

  const onDown = (e: React.PointerEvent) => {
    if (!isSheet() || (e.target as HTMLElement).closest('button,a,input,select,textarea')) return;
    try {
      (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    } catch {
      /* sentetik olay */
    }
    begin(e.clientY);
  };

  // Gövde en üstteyken aşağı çekiş → sayfayı sürükle (dokunmatik; kaydırmayla çakışmasın diye yalnız tepe noktada)
  useEffect(() => {
    const body = bodyRef.current;
    if (!body) return;
    let startY = 0;
    let startX = 0;
    let armed = false;
    const onStart = (e: TouchEvent) => {
      if (!isSheet() || e.touches.length !== 1) return;
      startY = e.touches[0].clientY;
      startX = e.touches[0].clientX;
      armed = body.scrollTop <= 0;
    };
    const onMoveT = (e: TouchEvent) => {
      if (!armed) return;
      const y = e.touches[0].clientY;
      const dy = y - startY;
      const dx = Math.abs(e.touches[0].clientX - startX);
      if (!drag.current) {
        if (dy > 8 && dy > dx && body.scrollTop <= 0) begin(startY);
        else if (dy < -4 || dx > 12) { armed = false; return; }
        else return;
      }
      e.preventDefault();
      move(y);
    };
    const onEnd = () => {
      armed = false;
      if (drag.current) end();
    };
    body.addEventListener('touchstart', onStart, { passive: true });
    body.addEventListener('touchmove', onMoveT, { passive: false });
    body.addEventListener('touchend', onEnd, { passive: true });
    body.addEventListener('touchcancel', onEnd, { passive: true });
    return () => {
      body.removeEventListener('touchstart', onStart);
      body.removeEventListener('touchmove', onMoveT);
      body.removeEventListener('touchend', onEnd);
      body.removeEventListener('touchcancel', onEnd);
      if (raf.current) cancelAnimationFrame(raf.current);
    };
  }, []);

  const style = { '--sheet-w': `${width}px` } as React.CSSProperties;

  return (
    <div className={`sh-sheet-root ${closing ? 'is-closing' : ''}`}>
      <div ref={backRef} className="sh-sheet-backdrop" aria-hidden="true" onClick={onClose} />
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
        <div className="sh-sheet-head" onPointerDown={onDown} onPointerMove={(e) => move(e.clientY)} onPointerUp={end} onPointerCancel={end}>
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
        <div ref={bodyRef} className={`sh-sheet-body ${bare ? 'is-bare' : ''}`}>{children}</div>
        {footer && <div className="sh-sheet-foot">{footer}</div>}
      </div>
    </div>
  );
};
