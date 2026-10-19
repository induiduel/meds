/**
 * Cihaz ve tarayıcı algılama — tek kaynak.
 *
 * Neden ayrı dosya: iOS algısı daha önce `fullscreen.ts` ve `pwaService.ts` içinde ayrı ayrı
 * `CSS.supports('-webkit-touch-callout', 'none')` ile yapılıyordu. Bu koşul macOS Safari'de de
 * doğru döndüğü için masaüstü Safari yanlışlıkla "iOS" sayılıyor, tam ekran/zoom kuralları
 * bozuluyordu. Burada yalnız kullanıcı aracısı ve dokunma noktası sayısı kullanılır.
 *
 * iPadOS 13+ kendini "MacIntel" olarak tanıttığı için `maxTouchPoints > 1` kontrolü korunur.
 */

export type IosBrowserType = 'safari' | 'crios' | 'fxios' | 'edgios' | 'other';

export function isIosDevice(): boolean {
  if (typeof navigator === 'undefined') return false;
  const ua = navigator.userAgent || '';
  if (/iPad|iPhone|iPod/.test(ua)) return true;
  // iPadOS 13+ masaüstü modu: platform MacIntel ama dokunmatik ekran var.
  if (navigator.platform === 'MacIntel' && (navigator.maxTouchPoints || 0) > 1) return true;
  return false;
}

export function isIpadDevice(): boolean {
  if (typeof navigator === 'undefined') return false;
  const ua = navigator.userAgent || '';
  if (/iPad/.test(ua)) return true;
  if (navigator.platform === 'MacIntel' && (navigator.maxTouchPoints || 0) > 1) return true;
  if (isIosDevice() && typeof window !== 'undefined' && window.screen) {
    return Math.min(window.screen.width, window.screen.height) >= 700;
  }
  return false;
}

export function getIosBrowser(): IosBrowserType {
  if (typeof navigator === 'undefined') return 'other';
  const ua = navigator.userAgent || '';
  if (/CriOS/i.test(ua)) return 'crios';
  if (/FxiOS/i.test(ua)) return 'fxios';
  if (/EdgiOS/i.test(ua)) return 'edgios';
  if (/Safari/i.test(ua) && !/CriOS|FxiOS|EdgiOS|OPiOS/i.test(ua)) return 'safari';
  return 'other';
}

/** Kurulu uygulama (Ana Ekrana Ekle) mı? Tarayıcı sekmesinde miyiz? */
export function isStandaloneApp(): boolean {
  if (typeof window === 'undefined') return false;
  try {
    if (window.matchMedia?.('(display-mode: standalone)').matches) return true;
    if (window.matchMedia?.('(display-mode: fullscreen)').matches) return true;
  } catch {
    /* matchMedia yok */
  }
  if ((navigator as Navigator & { standalone?: boolean }).standalone === true) return true;
  return /android-app:\/\//.test(document.referrer || '');
}

/**
 * iOS'ta tarayıcı sekmesindeyiz: adres çubuğu/tarayıcı altlığı gizlenemez.
 * Gerçek tam ekran yalnız kurulu PWA'da mümkündür; arayüz bunu dürüstçe söyler.
 */
export function isIosBrowserTab(): boolean {
  return isIosDevice() && !isStandaloneApp();
}

/**
 * Dokunmatik ekranlı cihazlarda (iPhone, iPad, Android telefon/tablet, dokunmatik ekranlı bilgisayar)
 * tarayıcının native `requestFullscreen` / `webkitRequestFullscreen` API'si çağrıldığında:
 * - Chrome "Tam ekrandan çıkmak için kaydır" kipine girip sayfa içi kaydırma, bölünmüş ekran ayracı ve
 *   kart kaydırma hareketlerini yakalayarak sitenin işlevselliğini bozar,
 * - iOS/iPadOS WebKit bölünmüş ekranda metin/PDF kaydırırken tam ekrandan kendiliğinden çıkar.
 * Bu cihazlarda native Fullscreen API yerine doğrudan uygulama içi tam ekran katmanı kullanılır.
 */
export function shouldAvoidNativeFullscreen(): boolean {
  if (typeof window === 'undefined' || typeof navigator === 'undefined') return true;
  if (isIosDevice()) return true;
  const ua = navigator.userAgent || '';
  if (/Android|CriOS|FxiOS|EdgiOS|Mobile|Tablet/i.test(ua)) return true;
  if ((navigator.maxTouchPoints || 0) > 0) return true;
  try {
    if (window.matchMedia?.('(pointer: coarse), (hover: none)').matches) return true;
  } catch {
    /* matchMedia yok */
  }
  return false;
}

/**
 * CSS'in kullanacağı cihaz sınıflarını kök öğeye yazar. `main.tsx` açılışta bir kez çağırır.
 * `uiZoom.ts` ve `v12.css` iOS kuralları bu sınıflara bağlıdır.
 */
export function markDeviceClasses(): void {
  if (typeof document === 'undefined') return;
  const root = document.documentElement;
  const ios = isIosDevice();
  root.classList.toggle('is-ios', ios);
  root.classList.toggle('is-ipados', isIpadDevice());
  root.classList.toggle('is-ios-browser-tab', isIosBrowserTab());
}

