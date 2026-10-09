/**
 * Kalem (stylus) algılama: telefonda/tablette bir kez gerçek kalem dokunuşu (pointerType "pen") görülünce
 * cihaz "kalemli" sayılır. O andan sonra işaretleme araçlarında yalnız kalem yazar, parmak sayfayı kaydırır.
 * Kalem hiç görülmezse parmakla yazma eskisi gibi çalışır. Oturum boyunca (sessionStorage) hatırlanır.
 */
import { useSyncExternalStore } from 'react';

const KEY = 'medsoru_pen_device';
let penDevice = (() => {
  try {
    return sessionStorage.getItem(KEY) === '1';
  } catch {
    return false;
  }
})();
const listeners = new Set<() => void>();

const setPenDevice = (v: boolean) => {
  if (penDevice === v) return;
  penDevice = v;
  try {
    if (v) sessionStorage.setItem(KEY, '1');
    else sessionStorage.removeItem(KEY);
  } catch {
    /* ignore */
  }
  listeners.forEach((l) => l());
};

/** Her işaretçi olayında çağrılabilir; kalem görülürse cihazı kalemli işaretler. */
export const notePointer = (e: { pointerType?: string }) => {
  if (e.pointerType === 'pen') setPenDevice(true);
};

export const isPenDevice = () => penDevice;

/** Kalem algılamasını sıfırla (ör. kullanıcı "parmakla yaz"ı seçerse). */
export const resetPenDevice = () => setPenDevice(false);

export const usePenDevice = () =>
  useSyncExternalStore(
    (cb) => {
      listeners.add(cb);
      return () => listeners.delete(cb);
    },
    () => penDevice,
    () => penDevice
  );

// Uygulama genelinde ilk kalem dokunuşunu yakala (araç açık olmasa da)
if (typeof window !== 'undefined') {
  window.addEventListener('pointerdown', notePointer, { capture: true, passive: true });
}

/**
 * Kalemli cihazda parmakla kaydırma: dokunma eylemi kapalı (touch-action: none) bir yüzeyde
 * parmak hareketini en yakın kayan kapsayıcıya aktarır; bırakınca kısa bir eylemsizlikle durur.
 */
export const startFingerPan = (e: { pointerId: number; clientY: number; target: EventTarget | null }, from: Element) => {
  let el: HTMLElement | null = from.parentElement;
  while (el && !(el.scrollHeight > el.clientHeight + 2 && /(auto|scroll)/.test(getComputedStyle(el).overflowY))) el = el.parentElement;
  const scroller = el || (document.scrollingElement as HTMLElement | null);
  if (!scroller) return;
  const id = e.pointerId;
  let lastY = e.clientY;
  let lastT = performance.now();
  let v = 0;
  const target = (e.target as Element) || from;
  try {
    (target as any).setPointerCapture?.(id);
  } catch {
    /* ignore */
  }
  const move = (ev: PointerEvent) => {
    if (ev.pointerId !== id) return;
    const now = performance.now();
    const dy = ev.clientY - lastY;
    scroller.scrollTop -= dy;
    v = dy / Math.max(1, now - lastT);
    lastY = ev.clientY;
    lastT = now;
  };
  const end = (ev: PointerEvent) => {
    if (ev.pointerId !== id) return;
    window.removeEventListener('pointermove', move);
    window.removeEventListener('pointerup', end);
    window.removeEventListener('pointercancel', end);
    let vel = v * 16;
    const glide = () => {
      if (Math.abs(vel) < 0.5) return;
      scroller.scrollTop -= vel;
      vel *= 0.94;
      requestAnimationFrame(glide);
    };
    requestAnimationFrame(glide);
  };
  window.addEventListener('pointermove', move);
  window.addEventListener('pointerup', end);
  window.addEventListener('pointercancel', end);
};
