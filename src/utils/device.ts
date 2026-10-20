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
 * Native `requestFullscreen` YALNIZ iOS/iPadOS WebKit'te atlanır (kurulu PWA dahil diğer her yerde açılır): iPhone'da sayfa öğeleri için hiç desteklenmez,
 * iPad'de bölünmüş ekranda kaydırırken kendiliğinden kapanır. Oradaki çözüm uygulama içi tam ekran + "Ana ekrana
 * ekle" ipucudur (ana ekrandan açılan uygulama zaten tarayıcı çubuksuzdur).
 * 2026-10-20: eskiden tüm dokunmatik cihazlarda (Android, dokunmatik dizüstü, Chromebook) da atlanıyordu; bu
 * cihazlarda adres çubuğu kaldığı için "tam ekran açılmıyor" bildirildi ve sayfalar arasında tutarsızlık vardı.
 * Artık bu cihazlarda gerçek tam ekran açılır; kaydırma sayfanın kendi kaydırma kabında sürer, native tam ekran
 * kaydırma/geri hareketiyle kapanırsa uygulama içi tam ekran korunur (utils/fullscreen.ts onNativeChange).
 */
export function shouldAvoidNativeFullscreen(): boolean {
  if (typeof window === 'undefined' || typeof navigator === 'undefined') return true;
  // Kurulu uygulamada (masaüstü PWA penceresi, Android ana ekran) da gerçek tam ekran açılır: pencere başlığı,
  // Android durum/gezinme çubukları ancak böyle gizlenir (2026-10-20: "masaüstü uygulamasında tam ekran olmuyor").
  return isIosDevice();
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

