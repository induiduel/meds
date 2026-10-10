/**
 * src/services/pwaService.ts
 *
 * PWA (Progressive Web App) Yaşam Döngüsü ve Arka Plan Servis Yöneticisi:
 * - Service Worker kaydı ve güncellemelerin otomatik yönetimi
 * - Masaüstü ve mobil yükleme istemi (beforeinstallprompt, promptInstall)
 * - Standalone (kurulu uygulama) algılama
 * - Arka Plan Eşitlemesi (Background Sync & Periodic Background Sync)
 * - Push Bildirim yetkilendirmesi ve entegrasyonu
 */

export interface PwaState {
  isSupported: boolean;
  isInstalled: boolean;
  canInstall: boolean;
  isRegistered: boolean;
  hasUpdate: boolean;
  backgroundSyncSupported: boolean;
  periodicSyncSupported: boolean;
}

export type PwaListener = (state: PwaState) => void;

class PwaService {
  private deferredPrompt: any = null;
  private listeners: Set<PwaListener> = new Set();
  private registration: ServiceWorkerRegistration | null = null;

  private state: PwaState = {
    isSupported: typeof window !== 'undefined' && 'serviceWorker' in navigator,
    isInstalled: false,
    canInstall: false,
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
    if (typeof window === 'undefined') return false;
    return (
      window.matchMedia('(display-mode: standalone)').matches ||
      (window.navigator as any).standalone === true ||
      document.referrer.includes('android-app://')
    );
  }

  private checkInstalled() {
    this.state.isInstalled = this.isStandalone();
    this.notify();
  }

  private listenInstallPrompt() {
    window.addEventListener('beforeinstallprompt', (e: Event) => {
      // Varsayılan mini-infobar'ı engelle ve kendi özel butonumuz için sakla
      e.preventDefault();
      this.deferredPrompt = e;
      this.state.canInstall = true;
      this.notify();
      console.log('[PWA] beforeinstallprompt yakalandı. Uygulama kurulabilir.');
    });

    window.addEventListener('appinstalled', () => {
      this.deferredPrompt = null;
      this.state.canInstall = false;
      this.state.isInstalled = true;
      this.notify();
      console.log('[PWA] MedSoru başarıyla kuruldu.');
    });
  }

  public async initServiceWorker(): Promise<ServiceWorkerRegistration | null> {
    if (!('serviceWorker' in navigator)) {
      this.state.isSupported = false;
      this.notify();
      return null;
    }

    try {
      const swUrl = '/sw.js';
      const reg = await navigator.serviceWorker.register(swUrl, { scope: '/' });
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
   * Kullanıcıya PWA Kurulum Penceresini Göster
   */
  public async promptInstall(): Promise<'accepted' | 'dismissed' | 'unsupported'> {
    if (!this.deferredPrompt) {
      // iOS Safari için manuel rehber gerekebilir
      return 'unsupported';
    }

    try {
      this.deferredPrompt.prompt();
      const choiceResult = await this.deferredPrompt.userChoice;
      this.deferredPrompt = null;
      this.state.canInstall = false;
      this.notify();
      return choiceResult.outcome;
    } catch (e) {
      console.warn('[PWA] Prompt hatası:', e);
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
