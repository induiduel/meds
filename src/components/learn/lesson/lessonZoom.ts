import { useEffect, useSyncExternalStore } from 'react';

/**
 * Ders içeriği yakınlaştırması (yalnız ders sütunu/kartı; üst çubuk ve paneller sabit kalır).
 *  - scale: 0.8–1.8 (%10 adım). CSS `zoom` ile uygulanır → metin ve görseller birlikte büyür, sütun görsel
 *    genişliği aynı kalır (genişlik scale'e bölünür), yatay kaydırma oluşmaz.
 *  - gestures: açıkken iki parmak / trackpad sıkıştırma ve Ctrl(+/−/0) dersi yakınlaştırır; kapalıyken
 *    tarayıcının kendi davranışı geçerlidir. İkisi de cihazda saklanır.
 */
export interface LessonZoom {
  scale: number;
  gestures: boolean;
}

const KEY = 'medsoru_learn_zoom';
export const ZOOM_MIN = 0.8;
export const ZOOM_MAX = 1.8;
const listeners = new Set<() => void>();
// read() başlangıçta çağırdığı için state'ten ÖNCE tanımlı olmalı (aksi hâlde TDZ → kayıtlı ölçek yok sayılıyordu)
export const clamp = (v: number) => Math.round(Math.min(ZOOM_MAX, Math.max(ZOOM_MIN, v)) * 100) / 100;

function read(): LessonZoom {
  try {
    const raw = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (raw && typeof raw.scale === 'number') return { scale: clamp(raw.scale), gestures: raw.gestures !== false };
  } catch { /* yok */ }
  return { scale: 1, gestures: true };
}
let state: LessonZoom = typeof window === 'undefined' ? { scale: 1, gestures: true } : read();


export function setLessonZoom(patch: Partial<LessonZoom>) {
  const next = { ...state, ...patch, scale: clamp(patch.scale ?? state.scale) };
  if (next.scale === state.scale && next.gestures === state.gestures) return;
  state = next;
  try { localStorage.setItem(KEY, JSON.stringify(state)); } catch { /* yok */ }
  listeners.forEach((l) => l());
}
export const stepZoom = (dir: 1 | -1) => setLessonZoom({ scale: Math.round((state.scale + dir * 0.1) * 10) / 10 });

export function useLessonZoom(): LessonZoom {
  return useSyncExternalStore(
    (cb) => { listeners.add(cb); return () => listeners.delete(cb); },
    () => state,
    () => state
  );
}

/**
 * Hareketler: Ctrl/Cmd + (=, +, −, 0) klavye; Ctrl + tekerlek (trackpad sıkıştırma); iki parmak sıkıştırma.
 * `onChange` her değişimde kısa bir ölçek rozeti göstermek için çağrılır.
 */
export function useLessonZoomGestures(target: React.RefObject<HTMLElement | null>, enabled: boolean, onChange: () => void) {
  useEffect(() => {
    if (!enabled) return;
    const onKey = (e: KeyboardEvent) => {
      if (!(e.ctrlKey || e.metaKey) || e.altKey) return;
      if (e.key === '=' || e.key === '+') { e.preventDefault(); stepZoom(1); onChange(); }
      else if (e.key === '-' || e.key === '_') { e.preventDefault(); stepZoom(-1); onChange(); }
      else if (e.key === '0') { e.preventDefault(); setLessonZoom({ scale: 1 }); onChange(); }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [enabled, onChange]);

  useEffect(() => {
    const el = target.current;
    if (!el || !enabled) return;
    let wheelAcc = 0;
    const onWheel = (e: WheelEvent) => {
      if (!e.ctrlKey) return;
      e.preventDefault();
      wheelAcc += -e.deltaY;
      if (Math.abs(wheelAcc) >= 40) {
        stepZoom(wheelAcc > 0 ? 1 : -1);
        wheelAcc = 0;
        onChange();
      }
    };
    let start = 0;
    let base = 1;
    let raf = 0;
    let pending = 0;
    const dist = (t: TouchList) => Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY);
    const onStart = (e: TouchEvent) => {
      if (e.touches.length === 2) { start = dist(e.touches); base = state.scale; }
    };
    const onMove = (e: TouchEvent) => {
      if (e.touches.length !== 2 || !start) return;
      e.preventDefault();
      pending = base * (dist(e.touches) / start);
      if (!raf) raf = requestAnimationFrame(() => { raf = 0; setLessonZoom({ scale: pending }); onChange(); });
    };
    const onEnd = (e: TouchEvent) => { if (e.touches.length < 2) start = 0; };
    el.addEventListener('wheel', onWheel, { passive: false });
    el.addEventListener('touchstart', onStart, { passive: true });
    el.addEventListener('touchmove', onMove, { passive: false });
    el.addEventListener('touchend', onEnd, { passive: true });
    el.addEventListener('touchcancel', onEnd, { passive: true });
    return () => {
      el.removeEventListener('wheel', onWheel);
      el.removeEventListener('touchstart', onStart);
      el.removeEventListener('touchmove', onMove);
      el.removeEventListener('touchend', onEnd);
      el.removeEventListener('touchcancel', onEnd);
      if (raf) cancelAnimationFrame(raf);
    };
  }, [target, enabled, onChange]);
}
