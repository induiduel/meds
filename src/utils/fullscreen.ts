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
let scrollGuardInstalled = false;

function isAnyFullscreenActive(): boolean {
  if (typeof document === 'undefined') return false;
  const d = document as WebkitDocument;
  const root = document.documentElement;
  return Boolean(
    d.fullscreenElement ||
    d.webkitFullscreenElement ||
    root.classList.contains(APP_FS_CLASS) ||
    root.classList.contains('cd-tam-ekran')
  );
}

function isScrollableY(el: HTMLElement): boolean {
  if (el === document.documentElement || el === document.body) return false;
  if (el.scrollHeight <= el.clientHeight + 1) return false;
  const oy = window.getComputedStyle(el).overflowY;
  return oy === 'auto' || oy === 'scroll' || oy === 'overlay';
}

/**
 * iOS / iPadOS WebKit'te native tam ekranda (`webkitRequestFullscreen`) bölünmüş ekran bölmelerini
 * (`.ls-split-l`, `.pdv`, `.cd-metin` vb.) kaydırırken `scrollTop === 0` veya alt sınırda oluşan
 * overscroll hareketinin WebKit tarafından "tam ekrandan çıkma hareketi" olarak algılanmasını engeller.
 */
export function installFullscreenScrollGuard(): void {
  if (typeof window === 'undefined' || scrollGuardInstalled) return;
  scrollGuardInstalled = true;

  let startX = 0;
  let startY = 0;

  const markTouch = () => {
    lastTouchOrScrollAt = Date.now();
  };

  const onTouchStart = (e: TouchEvent) => {
    markTouch();
    if (e.touches.length !== 1) return;
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;

    if (!isAnyFullscreenActive()) return;

    // 1px sınır yastığı: scrollTop tam 0 iken başlayan dokunuşlarda WebKit UIScrollView hareketi
    // kendi üstüne almak yerine tam ekrandan çıkış hareketine devreder. 1px içeride başlatmak bunu önler.
    let node = e.target as HTMLElement | null;
    while (node && node !== document.body && node !== document.documentElement) {
      if (isScrollableY(node)) {
        if (node.scrollTop <= 0) {
          node.scrollTop = 1;
        } else if (node.scrollTop + node.clientHeight >= node.scrollHeight) {
          node.scrollTop = Math.max(1, node.scrollHeight - node.clientHeight - 1);
        }
      }
      node = node.parentElement;
    }
  };

  const onTouchMove = (e: TouchEvent) => {
    markTouch();
    if (e.touches.length !== 1 || !isAnyFullscreenActive()) return;

    const target = e.target as HTMLElement | null;
    if (!target) return;
    if (target.closest('input[type="range"], .cd-ayrac, .ls-split-handle, .cd-cubuk, [data-allow-touchmove]')) {
      return;
    }

    const dx = e.touches[0].clientX - startX;
    const dy = e.touches[0].clientY - startY;
    // Yatay kaydırmalara veya çok küçük hareketlere dokunma
    if (Math.abs(dy) <= Math.abs(dx) || Math.abs(dy) < 4) return;

    let node: HTMLElement | null = target;
    let canScrollInDirection = false;
    while (node && node !== document.body && node !== document.documentElement) {
      if (isScrollableY(node)) {
        if (dy > 0 && node.scrollTop > 0) {
          canScrollInDirection = true;
          break;
        }
        if (dy < 0 && node.scrollTop + node.clientHeight < node.scrollHeight - 1) {
          canScrollInDirection = true;
          break;
        }
      }
      node = node.parentElement;
    }

    // Hiçbir alt bölme bu yönde kayamıyorsa (üst/alt sınıra dayandıysa veya kaymayan bir alandaysa)
    // hareketin belge köküne sıçrayıp native tam ekranı kapatmasını engelle
    if (!canScrollInDirection && e.cancelable) {
      e.preventDefault();
    }
  };

  window.addEventListener('touchstart', onTouchStart, { passive: true, capture: true });
  window.addEventListener('touchmove', onTouchMove, { passive: false, capture: false });
  window.addEventListener('scroll', markTouch, { passive: true, capture: true });
}

installFullscreenScrollGuard();

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

export function wasRecentlyScrollingOrTouching(thresholdMs = 1200): boolean {
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
  const target = (el || document.documentElement) as WebkitElement;
  return (
    typeof target.requestFullscreen === 'function' ||
    typeof target.webkitRequestFullscreen === 'function' ||
    typeof target.webkitRequestFullScreen === 'function'
  );
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
 * Her platformda (iPhone, iPad, Android, Masaüstü) çalışan tam ekran açıcı.
 * Hem native Fullscreen API (`requestFullscreen` / `webkitRequestFullscreen`) çağrılır,
 * hem de `html.is-app-fullscreen` sınıfı etkinleştirilir.
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
    try {
      const res2 = req.call(target);
      if (res2 && typeof (res2 as Promise<void>).then === 'function') {
        await (res2 as Promise<void>);
      }
    } catch {
      /* tarayıcı desteklemiyorsa CSS tam ekran (is-app-fullscreen) devrede kalır */
    }
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
      if (!isNativeFullscreen() && document.documentElement.classList.contains(APP_FS_CLASS)) {
        if (!wasRecentlyScrollingOrTouching()) {
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
