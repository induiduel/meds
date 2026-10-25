/**
 * src/services/pwaService.ts
 *
 * PWA (Progressive Web App) Yaşam Döngüsü ve Arka Plan Servis Yöneticisi:
 * - Service Worker kaydı ve güncellemelerin otomatik yönetimi
 * - Masaüstü, Android ve iOS (Safari & Chrome) yükleme istemi / rehberi
 * - Standalone (kurulu uygulama) algılama
 * - Arka Plan Eşitlemesi (Background Sync & Periodic Background Sync)
 * - Push Bildirim yetkilendirmesi ve entegrasyonu
 */

import {
  getIosBrowser,
  isIosDevice,
  isIpadDevice,
  isStandaloneApp,
  type IosBrowserType,
} from '../utils/device';

export type { IosBrowserType } from '../utils/device';

export interface PwaState {
  isSupported: boolean;
  isInstalled: boolean;
  /** Uygulama henüz kurulu değilse true (hem native prompt hem iOS Safari/Chrome rehberi için) */
  canInstall: boolean;
  /** Tarayıcı doğrudan beforeinstallprompt sunduysa true */
  hasNativePrompt: boolean;
  isIos: boolean;
  isIpad: boolean;
  iosBrowser: IosBrowserType;
  isRegistered: boolean;
  hasUpdate: boolean;
  backgroundSyncSupported: boolean;
  periodicSyncSupported: boolean;
}

export type PwaListener = (state: PwaState) => void;

/**
 * Sürüm sorgusu Cloudflare önbelleğini atlatır: /sw.js eskiden "immutable, 1 yıl" başlığıyla CDN'de takılı
 * kalmıştı (yeni SW hiç inmiyordu). public/sw.js değişince (CACHE_VERSION ile birlikte) bunu da artır.
 * Tüm kayıtlar bu adresi kullanır; sorgusuz /sw.js kaydı CDN'deki eski sürüme dönebilir.
 */
export const SW_URL = '/sw.js?v=13';

export const PWA_WELCOME_STORAGE_KEY = 'medsoru_pwa_welcome_dismissed_v1';
export const PWA_GUIDE_OPEN_EVENT = 'medsor:open-pwa-install-guide';

/**
 * Geriye dönük uyumluluk: algılama artık `utils/device.ts` içinde tek yerde.
 * Burada yalnız yeniden dışa aktarılır (mevcut çağrılar değişmeden çalışır).
 */
export const detectIosDevice = isIosDevice;
export const detectIpadDevice = isIpadDevice;
export const detectIosBrowser = getIosBrowser;

class PwaService {
  private deferredPrompt: any = null;
  private listeners: Set<PwaListener> = new Set();
  private registration: ServiceWorkerRegistration | null = null;

  private state: PwaState = {
    isSupported: typeof window !== 'undefined' && 'serviceWorker' in navigator,
    isInstalled: false,
    canInstall: true,
    hasNativePrompt: false,
    isIos: detectIosDevice(),
    isIpad: detectIpadDevice(),
    iosBrowser: detectIosBrowser(),
    isRegistered: false,
    hasUpdate: false,
    backgroundSyncSupported: false,
    periodicSyncSupported: false,
  };

  constructor() {
    if (typeof window !== 'undefined') {
      this.checkInstalled();
      this.initServiceWorker();
      this.listenInstallPrompt();
      try {
        const mq = window.matchMedia('(display-mode: standalone)');
        mq.addEventListener?.('change', () => this.checkInstalled());
      } catch {
        /* ignore */
      }
    }
  }

  public getState(): PwaState {
    return { ...this.state };
  }

  public subscribe(listener: PwaListener): () => void {
    this.listeners.add(listener);
    listener(this.getState());
    return () => this.listeners.delete(listener);
  }

  private notify() {
    const s = this.getState();
    for (const listener of this.listeners) {
      try {
        listener(s);
      } catch (err) {
        console.warn('[PWA] Listener error:', err);
      }
    }
  }

  public isStandalone(): boolean {
    return isStandaloneApp();
  }

  private checkInstalled() {
    const installed = this.isStandalone();
    this.state.isInstalled = installed;
    this.state.canInstall = !installed;
    if (installed) {
      document.documentElement.classList.add('is-pwa-standalone');
    } else {
      document.documentElement.classList.remove('is-pwa-standalone');
    }
    this.notify();
  }

  private listenInstallPrompt() {
    window.addEventListener('beforeinstallprompt', (e: Event) => {
      // Varsayılan mini-infobar'ı engelle ve kendi özel butonumuz için sakla
      e.preventDefault();
      this.deferredPrompt = e;
      this.state.hasNativePrompt = true;
      this.state.canInstall = !this.state.isInstalled;
      this.notify();
      console.log('[PWA] beforeinstallprompt yakalandı. Uygulama kurulabilir.');
    });

    window.addEventListener('appinstalled', () => {
      this.deferredPrompt = null;
      this.state.hasNativePrompt = false;
      this.state.canInstall = false;
      this.state.isInstalled = true;
      document.documentElement.classList.add('is-pwa-standalone');
      this.notify();
      console.log('[PWA] MeDSor başarıyla kuruldu.');
    });
  }

  public async initServiceWorker(): Promise<ServiceWorkerRegistration | null> {
    if (!('serviceWorker' in navigator)) {
      this.state.isSupported = false;
      this.notify();
      return null;
    }

    // Vite geliştirme sunucusunda SW kaynak modülleri (/src/*.css, *.tsx) önbelleğe alıp
    // düzenlemeleri gizliyordu: geliştirmede kaydedilmez, eski kayıt varsa kaldırılır.
    if (import.meta.env.DEV) {
      navigator.serviceWorker.getRegistrations().then((regs) => regs.forEach((r) => r.unregister())).catch(() => {});
      return null;
    }

    try {
      const reg = await navigator.serviceWorker.register(SW_URL, { scope: '/' });
      this.registration = reg;
      this.state.isRegistered = true;

      // Arka plan yeteneklerini denetle
      this.state.backgroundSyncSupported = 'sync' in reg;
      this.state.periodicSyncSupported = 'periodicSync' in reg;

      // Güncelleme kontrolü
      reg.addEventListener('updatefound', () => {
        const newWorker = reg.installing;
        if (!newWorker) return;
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            this.state.hasUpdate = true;
            this.notify();
            console.log('[PWA] Yeni bir sürüm hazır!');
          }
        });
      });

      // Arka plan senkronizasyonunu kaydet
      await this.registerBackgroundSync();

      // Çevrimdışı çekirdek rotaları Service Worker'a mühürle
      if (typeof window !== 'undefined' && 'requestIdleCallback' in window) {
        (window as any).requestIdleCallback(() => {
          this.precacheUrls([
            '/',
            '/index.html',
            '/manifest.json',
            '/cikmis',
            '/ogren',
            '/kartlar',
            '/hastaliklar',
            '/sozluk',
            '/calis',
            '/ozetler',
            '/kazanimlar',
            '/test',
            '/istatistik',
            '/ayarlar',
            '/api/committees',
          ]);
        }, { timeout: 6000 });
      } else {
        setTimeout(() => {
          this.precacheUrls([
            '/',
            '/index.html',
            '/manifest.json',
            '/cikmis',
            '/ogren',
            '/kartlar',
            '/hastaliklar',
            '/sozluk',
            '/calis',
            '/ozetler',
            '/kazanimlar',
            '/test',
            '/istatistik',
            '/ayarlar',
            '/api/committees',
          ]);
        }, 4000);
      }

      this.notify();
      return reg;
    } catch (err) {
      console.warn('[PWA] Service Worker kayıt hatası:', err);
      return null;
    }
  }

  /**
   * Arka plan senkronizasyonunu işletim sistemine kaydet
   */
  public async registerBackgroundSync(): Promise<boolean> {
    if (!this.registration) return false;

    // 1. One-shot Background Sync (Ağ gelince çevrimdışı işlemleri kuyruktan yürütme)
    if ('sync' in this.registration) {
      try {
        await (this.registration as any).sync.register('sync-offline-actions');
        console.log('[PWA] Background Sync (sync-offline-actions) kaydedildi.');
      } catch (e) {
        console.warn('[PWA] Sync register uyarısı:', e);
      }
    }

    // 2. Periodic Background Sync (Günde 1 kez arka planda veritabanı denetimi)
    if ('periodicSync' in this.registration) {
      try {
        const status = await (navigator as any).permissions.query({
          name: 'periodic-background-sync',
        });
        if (status.state === 'granted') {
          await (this.registration as any).periodicSync.register('update-database', {
            minInterval: 12 * 60 * 60 * 1000, // 12 saatte bir
          });
          console.log('[PWA] Periodic Background Sync (update-database) kaydedildi.');
        }
      } catch (e) {
        // İzin yoksa sessizce geç
      }
    }

    return true;
  }

  /**
   * Görsel kurulum rehberi modalını aç (iOS Safari, iOS Chrome ve manuel kurulum için)
   */
  public openInstallGuide() {
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent(PWA_GUIDE_OPEN_EVENT));
    }
  }

  /**
   * Kullanıcıya PWA Kurulum Penceresini Göster.
   * Native prompt varsa doğrudan açar; yoksa (iOS Safari, iOS Chrome vb.) görsel kurulum rehberini açar.
   */
  public async promptInstall(opts?: { silentIfUnsupported?: boolean }): Promise<'accepted' | 'dismissed' | 'unsupported'> {
    if (!this.deferredPrompt) {
      if (!opts?.silentIfUnsupported) {
        this.openInstallGuide();
      }
      return 'unsupported';
    }

    try {
      this.deferredPrompt.prompt();
      const choiceResult = await this.deferredPrompt.userChoice;
      this.deferredPrompt = null;
      this.state.hasNativePrompt = false;
      this.state.canInstall = !this.state.isInstalled;
      this.notify();
      return choiceResult.outcome;
    } catch (e) {
      console.warn('[PWA] Prompt hatası:', e);
      if (!opts?.silentIfUnsupported) {
        this.openInstallGuide();
      }
      return 'dismissed';
    }
  }

  /**
   * Yeni sürüm varsa beklemedeki Service Worker'ı anında aktif et
   */
  public applyUpdate() {
    if (this.registration && this.registration.waiting) {
      this.registration.waiting.postMessage({ type: 'SKIP_WAITING' });
      window.location.reload();
    }
  }

  /**
   * Service Worker'a önbelleğe alınacak URL'leri ilet
   */
  public precacheUrls(urls: string[]) {
    if (navigator.serviceWorker.controller) {
      navigator.serviceWorker.controller.postMessage({
        type: 'CACHE_URLS',
        urls,
      });
    }
  }
}

export const pwaService = new PwaService();

export function openPwaInstallGuide(): void {
  pwaService.openInstallGuide();
}

