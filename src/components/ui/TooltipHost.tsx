import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

/**
 * Uygulama geneli Material tarzı ipucu. Ayrı ayrı bileşen sarmalamak yerine belge düzeyinde
 * dinler: title ya da aria-label taşıyan her düğme/bağlantı/sekme için çalışır. Tarayıcının
 * kendi title ipucu çift görünmesin diye gezinme süresince title geçici olarak saklanır.
 * Dokunmatikte gösterilmez (Material: uzun basma davranışı tarayıcıya bırakılır).
 */
const TARGET = 'button, a[href], [role="button"], [role="tab"], [role="radio"], [role="switch"], label[title], summary[title]';
const SHOW_DELAY = 450;

interface TipState { text: string; x: number; y: number; place: 'top' | 'bottom' }

const labelOf = (el: HTMLElement): string => {
  const t = el.getAttribute('data-ms-title') || el.getAttribute('title') || el.getAttribute('aria-label') || '';
  const text = t.trim();
  if (!text) return '';
  // Görünür yazısı ipucuyla aynıysa tekrar etme
  const visible = (el.innerText || '').replace(/\s+/g, ' ').trim();
  if (visible && visible.toLocaleLowerCase('tr') === text.toLocaleLowerCase('tr')) return '';
  return text.length > 140 ? text.slice(0, 137) + '…' : text;
};

export const TooltipHost: React.FC = () => {
  const [tip, setTip] = useState<TipState | null>(null);
  const timer = useRef<number | null>(null);
  const current = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const restoreTitle = (el: HTMLElement | null) => {
      if (!el) return;
      const saved = el.getAttribute('data-ms-title');
      if (saved !== null) {
        el.setAttribute('title', saved);
        el.removeAttribute('data-ms-title');
      }
    };
    const hide = () => {
      if (timer.current) window.clearTimeout(timer.current);
      timer.current = null;
      restoreTitle(current.current);
      current.current = null;
      setTip(null);
    };
    const showFor = (el: HTMLElement, delay: number) => {
      const text = labelOf(el);
      if (!text) return;
      if (el.hasAttribute('title')) {
        el.setAttribute('data-ms-title', el.getAttribute('title') || '');
        el.removeAttribute('title');
      }
      current.current = el;
      timer.current = window.setTimeout(() => {
        if (current.current !== el || !el.isConnected) return;
        const r = el.getBoundingClientRect();
        const place = r.top > 44 ? 'top' : 'bottom';
        setTip({ text, x: r.left + r.width / 2, y: place === 'top' ? r.top - 8 : r.bottom + 8, place });
      }, delay);
    };

    const onOver = (e: PointerEvent) => {
      if (e.pointerType === 'touch') return;
      const el = (e.target as HTMLElement | null)?.closest?.(TARGET) as HTMLElement | null;
      if (el === current.current) return;
      hide();
      if (el && !el.closest('[data-no-tip]')) showFor(el, SHOW_DELAY);
    };
    const onFocus = (e: FocusEvent) => {
      const el = (e.target as HTMLElement | null)?.closest?.(TARGET) as HTMLElement | null;
      hide();
      if (el && el.matches(':focus-visible') && !el.closest('[data-no-tip]')) showFor(el, 120);
    };

    document.addEventListener('pointerover', onOver, true);
    document.addEventListener('focusin', onFocus, true);
    document.addEventListener('focusout', hide, true);
    document.addEventListener('pointerdown', hide, true);
    document.addEventListener('keydown', hide, true);
    window.addEventListener('scroll', hide, true);
    window.addEventListener('blur', hide);
    return () => {
      hide();
      document.removeEventListener('pointerover', onOver, true);
      document.removeEventListener('focusin', onFocus, true);
      document.removeEventListener('focusout', hide, true);
      document.removeEventListener('pointerdown', hide, true);
      document.removeEventListener('keydown', hide, true);
      window.removeEventListener('scroll', hide, true);
      window.removeEventListener('blur', hide);
    };
  }, []);

  if (!tip) return null;
  // Ekran kenarında kesilmesin: merkez, kenarlardan yarım ipucu genişliği kadar içeride tutulur
  const maxW = 260;
  const half = Math.min(maxW, tip.text.length * 7 + 18) / 2;
  const left = Math.min(Math.max(tip.x, 8 + half), window.innerWidth - 8 - half);
  return createPortal(
    <div
      role="tooltip"
      className={`ms-tooltip ${tip.place === 'top' ? 'is-top' : 'is-bottom'}`}
      style={{ left, top: tip.y, maxWidth: maxW }}
    >
      {tip.text}
    </div>,
    document.body
  );
};
