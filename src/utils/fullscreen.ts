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
 * - Tarayıcı Fullscreen API destekliyorsa (Masaüstü, Android, iPad) doğrudan tam ekrana geçer.
 * - Desteklemiyorsa veya reddederse (iPhone Safari / iPhone Chrome) uygulama kabuğunu gizleyen
 *   gerçek tam ekran görünüm katmanını (`html.is-app-fullscreen`) etkinleştirir ve adres çubuğunu
 *   küçültmek için sayfayı en üste kaydırır.
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
    // iPhone / iOS WebKit veya gömülü görünümde Fullscreen API reddedilirse CSS tam ekran kipi aktif kalır
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
      // Eğer kullanıcı tarayıcının kendi Esc / küçült düğmesiyle native tam ekrandan çıktıysa sınıfı da temizle
      setActive(isAppFullscreen());
    };
    const onNativeChange = () => {
      if (!isNativeFullscreen() && document.documentElement.classList.contains(APP_FS_CLASS)) {
        // Native fullscreen kapandıysa uygulama tam ekran sınıfını da kapat
        document.documentElement.classList.remove(APP_FS_CLASS);
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
