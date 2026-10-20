import { useEffect, useState } from 'react';
import { isIosDevice, shouldAvoidNativeFullscreen } from './device';

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
let touchTrackerInstalled = false;

/**
 * Dokunma ve kaydırma zamanını yalnızca pasif olarak izler (hiçbir dokunma/kaydırma
 * hareketine `preventDefault` uygulamaz; sayfa ve bölme kaydırmaları doğal çalışır).
 */
export function installFullscreenScrollGuard(): void {
  if (typeof window === 'undefined' || touchTrackerInstalled) return;
  touchTrackerInstalled = true;
  const mark = () => {
    lastTouchOrScrollAt = Date.now();
  };
  window.addEventListener('touchstart', mark, { passive: true, capture: true });
  window.addEventListener('touchmove', mark, { passive: true, capture: true });
  window.addEventListener('scroll', mark, { passive: true, capture: true });
}

installFullscreenScrollGuard();

/**
 * Sayfa geçişi izi: uygulama içi her adres değişikliği (pushState, yol değiştiren replaceState,
 * geri/ileri = popstate) zamanı tutulur. Geçişte kapanan sayfanın temizliği tam ekranı kapatmasın
 * diye `releasePageFullscreen` buna bakar; kullanıcı tam ekrandan çıkmadan sayfalar arasında gezer.
 */
let lastRouteChangeAt = 0;
let routeTrackerInstalled = false;
function installRouteChangeTracker(): void {
  if (typeof window === 'undefined' || routeTrackerInstalled) return;
  routeTrackerInstalled = true;
  const mark = () => { lastRouteChangeAt = Date.now(); };
  const h = window.history;
  const push = h.pushState.bind(h);
  const replace = h.replaceState.bind(h);
  h.pushState = (...args: Parameters<History['pushState']>) => { mark(); return push(...args); };
  h.replaceState = (...args: Parameters<History['replaceState']>) => {
    const before = window.location.pathname;
    const r = replace(...args);
    if (window.location.pathname !== before) mark();
    return r;
  };
  window.addEventListener('popstate', mark, { capture: true });
}
installRouteChangeTracker();

export function isRouteChanging(thresholdMs = 1500): boolean {
  return Date.now() - lastRouteChangeAt < thresholdMs;
}

/**
 * Tam ekranlı bir sayfa kapanırken (unmount) çağrılır. Sayfa geçişiyse tam ekran (uygulama sınıfı +
 * native katman) korunur ve yeni sayfa tam ekranda açılır; değilse tam ekran tamamen kapanır.
 */
export function releasePageFullscreen(): void {
  if (typeof document === 'undefined') return;
  if (isRouteChanging() && (isAppFullscreen() || isNativeFullscreen())) {
    document.documentElement.classList.add(APP_FS_CLASS);
    notifyFullscreenChange();
    return;
  }
  document.documentElement.classList.remove(APP_FS_CLASS);
  exitNativeFullscreen();
  notifyFullscreenChange();
}

/** Geriye dönük ad: algılama tek kaynakta (`utils/device.ts`). */
export function isIosWebKit(): boolean {
  return isIosDevice();
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
  if (shouldAvoidNativeFullscreen()) return false;
  const target = (el || document.documentElement) as WebkitElement;
  return (
    typeof target.requestFullscreen === 'function' ||
    typeof target.webkitRequestFullscreen === 'function' ||
    typeof target.webkitRequestFullScreen === 'function'
  );
}

/**
 * Uygulama tam ekranı YALNIZ `html.is-app-fullscreen` sınıfıdır. Native fullscreen (ör. bir video
 * veya tarayıcının kendi F11'i) uygulama tam ekranı sayılmaz; aksi hâlde kabuktaki tam ekran
 * düğmesi ilgisiz bir native katmanı kapatmaya çalışıyordu.
 */
export function isAppFullscreen(): boolean {
  if (typeof document === 'undefined') return false;
  return document.documentElement.classList.contains(APP_FS_CLASS);
}

function notifyFullscreenChange() {
  if (typeof window === 'undefined') return;
  window.dispatchEvent(new Event(FS_EVENT));
}

/**
 * Her platformda (iPhone, iPad, Android, Masaüstü) çalışan tam ekran açıcı.
 * - Dokunmatik cihazlarda (iOS, iPadOS, Android, dokunmatik ekran) tarayıcının native
 *   `requestFullscreen` kipi ("Tam ekrandan çıkmak için kaydır") sayfa içi kaydırma ve
 *   bölünmüş ekran hareketlerini bozduğu için çağrılmaz; doğrudan uygulama içi tam ekran
 *   (`html.is-app-fullscreen`) etkinleştirilir.
 * - Masaüstü tarayıcılarda hem `html.is-app-fullscreen` hem native Fullscreen API açılır.
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

  if (shouldAvoidNativeFullscreen()) {
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

/**
 * Native tam ekrandan çıkışın tek yolu. iOS/iPadOS WebKit'te `exitFullscreen` bulunmayabilir;
 * sırayla `webkitExitFullscreen`, ardından eski adı `webkitCancelFullScreen` denenir.
 */
export function exitNativeFullscreen(): void {
  if (typeof document === 'undefined') return;
  const d = document as WebkitDocument;
  if (!d.fullscreenElement && !d.webkitFullscreenElement) return;
  const exit = d.exitFullscreen || d.webkitExitFullscreen || d.webkitCancelFullScreen;
  try {
    const res = exit?.call(d);
    if (res && typeof (res as Promise<void>).catch === 'function') {
      void (res as Promise<void>).catch(() => {});
    }
  } catch {
    /* tarayıcı tam ekranı zaten kapatmış olabilir */
  }
}

export async function exitFullscreen(): Promise<void> {
  if (typeof document === 'undefined') return;
  document.documentElement.classList.remove(APP_FS_CLASS);
  exitNativeFullscreen();
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
        // Sayfa içi bir tam ekran katmanı (ders, okuyucu, asistan, PDF) hâlâ açıksa sınıfı koru:
        // iOS'ta native tam ekran kaydırma sırasında kapanabilir, kullanıcı ise sayfa içinde kalmalı.
        const sayfaIci = document.documentElement.classList.contains('cd-tam-ekran')
          || !!document.querySelector('.pa.is-tam, .sc.is-tam, .dpv.is-max, .ls-root.is-immersive, .r12-root.is-immersive');
        if (!sayfaIci && !wasRecentlyScrollingOrTouching()) {
          document.documentElement.classList.remove(APP_FS_CLASS);
        }
      }
      sync();
    };
    document.addEventListener('fullscreenchange', onNativeChange);
    document.addEventListener('webkitfullscreenchange', onNativeChange);
    window.addEventListener(FS_EVENT, sync);
    // Bazı tam ekran oynatıcılar (ders, çözücü, asistan) sınıfı doğrudan ekler ve olay yollamaz;
    // html sınıfı izlenir ki kabuk (gezinme adası, tam ekran düğmesi) her durumda eşlensin.
    const mo = new MutationObserver(sync);
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    return () => {
      mo.disconnect();
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
