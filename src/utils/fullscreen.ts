import { useEffect, useState } from 'react';

type WebkitDocument = Document & {
  webkitFullscreenElement?: Element | null;
  webkitExitFullscreen?: () => Promise<void> | void;
  webkitCancelFullScreen?: () => Promise<void> | void;
};

type WebkitElement = HTMLElement & {
  webkitRequestFullscreen?: () => Promise<void> | void;
  webkitRequestFullScreen?: () => Promise<void> | void;
  webkitEnterFullscreen?: () => void;
};

const APP_FS_CLASS = 'is-app-fullscreen';
const FS_EVENT = 'medsor:fullscreenchange';

let lastTouchOrScrollAt = 0;
if (typeof window !== 'undefined') {
  const markTouch = () => {
    lastTouchOrScrollAt = Date.now();
  };
  window.addEventListener('touchstart', markTouch, { passive: true, capture: true });
  window.addEventListener('touchmove', markTouch, { passive: true, capture: true });
  window.addEventListener('scroll', markTouch, { passive: true, capture: true });
}

export function isIosWebKit(): boolean {
  if (typeof navigator === 'undefined') return false;
  const ua = navigator.userAgent || '';
  if (/iPad|iPhone|iPod/.test(ua)) return true;
  if (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1) return true;
  if (typeof CSS !== 'undefined' && typeof CSS.supports === 'function' && CSS.supports('-webkit-touch-callout', 'none')) {
    return true;
  }
  return false;
}

export function wasRecentlyScrollingOrTouching( thresholdMs = 1200 ): boolean {
  return Date.now() - lastTouchOrScrollAt < thresholdMs;
}

export function getNativeFullscreenElement(): Element | null {
  if (typeof document === 'undefined') return null;
  const d = document as WebkitDocument;
  return d.fullscreenElement || d.webkitFullscreenElement || null;
}

export function isNativeFullscreen(): boolean {
  return !!getNativeFullscreenElement();
}

export function isNativeFullscreenSupported(el?: HTMLElement | null): boolean {
  if (typeof document === 'undefined') return false;
  if (isIosWebKit()) return false;
  const target = (el || document.documentElement) as WebkitElement;
  return typeof target.requestFullscreen === 'function' || typeof target.webkitRequestFullscreen === 'function' || typeof target.webkitRequestFullScreen === 'function';
}

export function isAppFullscreen(): boolean {
  if (typeof document === 'undefined') return false;
  return isNativeFullscreen() || document.documentElement.classList.contains(APP_FS_CLASS);
}

function notifyFullscreenChange() {
  if (typeof window === 'undefined') return;
  window.dispatchEvent(new Event(FS_EVENT));
}

/**
 * Her platformda (iPhone Safari, iPhone Chrome, iPad, Android, Masaüstü) çalışan tam ekran açıcı.
 * - iOS / iPadOS WebKit'te native `webkitRequestFullscreen` dikey kaydırma hareketini (özellikle bölünmüş
 *   ekranda metin/PDF kaydırırken) "tam ekrandan çıkma hareketi" sanıp tam ekranı otomatik kapattığı için
 *   iOS/iPadOS cihazlarda doğrudan kilitli CSS Tam Ekran katmanı (`html.is-app-fullscreen`) kullanılır.
 * - Masaüstü ve Android'de hem `html.is-app-fullscreen` hem native Fullscreen API etkinleştirilir.
 */
export async function enterFullscreen(el?: HTMLElement | null): Promise<boolean> {
  if (typeof document === 'undefined') return false;
  const root = document.documentElement;
  root.classList.add(APP_FS_CLASS);
  try {
    window.scrollTo({ top: 0, left: 0, behavior: 'instant' as ScrollBehavior });
  } catch {
    window.scrollTo(0, 0);
  }
  notifyFullscreenChange();

  // iOS ve iPadOS'ta WebKit native fullscreen kaydırma sırasında kendiliğinden kapandığı için çağrılmaz
  if (isIosWebKit()) {
    return true;
  }

  const target = (el || root) as WebkitElement;
  const req = target.requestFullscreen || target.webkitRequestFullscreen || target.webkitRequestFullScreen;
  if (!req) {
    return true;
  }

  try {
    const res = req.call(target, { navigationUI: 'hide' } as FullscreenOptions);
    if (res && typeof (res as Promise<void>).then === 'function') {
      await (res as Promise<void>);
    }
    notifyFullscreenChange();
    return true;
  } catch {
    notifyFullscreenChange();
    return true;
  }
}

export async function exitFullscreen(): Promise<void> {
  if (typeof document === 'undefined') return;
  const root = document.documentElement;
  root.classList.remove(APP_FS_CLASS);
  const d = document as WebkitDocument;
  if (d.fullscreenElement || d.webkitFullscreenElement) {
    const exit = d.exitFullscreen || d.webkitExitFullscreen || d.webkitCancelFullScreen;
    try {
      const res = exit?.call(d);
      if (res && typeof (res as Promise<void>).catch === 'function') {
        await (res as Promise<void>).catch(() => {});
      }
    } catch {
      /* ignore */
    }
  }
  notifyFullscreenChange();
}

export async function toggleFullscreen(el?: HTMLElement | null): Promise<boolean> {
  if (isAppFullscreen()) {
    await exitFullscreen();
    return false;
  }
  return enterFullscreen(el);
}

export function useAppFullscreen(): [boolean, (el?: HTMLElement | null) => void, () => void] {
  const [active, setActive] = useState<boolean>(() => isAppFullscreen());

  useEffect(() => {
    const sync = () => {
      setActive(isAppFullscreen());
    };
    const onNativeChange = () => {
      // Dokunmatik cihazda kaydırma sırasında tarayıcı native tam ekrandan çıksa bile uygulama tam ekranını koru
      if (!isNativeFullscreen() && document.documentElement.classList.contains(APP_FS_CLASS)) {
        if (!isIosWebKit() && !wasRecentlyScrollingOrTouching()) {
          document.documentElement.classList.remove(APP_FS_CLASS);
        }
      }
      sync();
    };
    document.addEventListener('fullscreenchange', onNativeChange);
    document.addEventListener('webkitfullscreenchange', onNativeChange);
    window.addEventListener(FS_EVENT, sync);
    return () => {
      document.removeEventListener('fullscreenchange', onNativeChange);
      document.removeEventListener('webkitfullscreenchange', onNativeChange);
      window.removeEventListener(FS_EVENT, sync);
    };
  }, []);

  const toggle = (el?: HTMLElement | null) => {
    void toggleFullscreen(el);
  };

  const exit = () => {
    void exitFullscreen();
  };

  return [active, toggle, exit];
}
