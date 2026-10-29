import { installKabukBayraklari } from './services/kabukBayraklari';
import './services/netInstall';
import { adresKatmaniniKur } from './siteHaritasi';
import { installAdminFetchAuth } from './services/adminFetchAuth';
import { Component, ErrorInfo, ReactNode } from 'react';
import CevrimdisiYok from './components/cevrimdisi/CevrimdisiYok';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import './styles/health.css';
import './styles/appearance.css';
import './styles/shell.css';
import './styles/motifler.css';
import './styles/screens.css';
import './styles/rebuild.css';
import './styles/toolbar.css';
// summary.css (özet/not okuyucu) ve spots.css (sınav spotları) kendi tembel ekranlarıyla yüklenir (başarım turu 2026-10-20).
import './styles/layout-modes.css';
import './styles/bento.css';
import './styles/motion.css';
import './styles/mobile.css';
import './styles/v11.css';
import './styles/v12.css';
import './styles/v13/base.css';
import './styles/v13/shell.css';
import './styles/v13/components.css';
import './styles/v13/fullscreen.css';
import './styles/v13/pages.css';
import './styles/v13/wide.css';
import { installToastBridge } from './components/ui/Toast';
import { installNetworkBanner } from './components/system/NetworkBanner';
import { installUpdatePrompt } from './components/system/UpdatePrompt';
import { installBakimEkrani } from './components/system/BakimEkrani';
import { getLocalAdminSession, isAdminUser } from './services/auth';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import './styles/v15/ek15.css';
declare const __MEDS_SURUM__: string;
import { installPullToRefresh } from './components/system/PullToRefresh';
import { installNotesSync } from './services/notesSync';
import { installUserDataAutoBackup } from './services/userDataSyncService';
import { installPresence } from './services/presence';
import { installEtkinlikGunlugu } from './services/etkinlikGunlugu';
import { prefetchIdle } from './routePrefetch';
import { installAutoReveal } from './utils/autoReveal';
import { installSelectionShare } from './utils/selectionShare';
import { installStudyTimer } from './services/activityLog';
import { applyTheme, readTheme } from './utils/theme';
import { applyUiVersion } from './utils/uiVersion';
import { markDeviceClasses } from './utils/device';
import { pwaService } from './services/pwaService';
import { offlineDatabaseService } from './services/offlineDatabaseService';
import { arkaPlanPushKur } from './services/arkaPlanPush';
import { cevrimdisiGibi, sunucuyaUlasilir } from './services/cevrimdisi/baglanti';
import { hizliMod, hizliModuKur } from './services/hizliMod';
import { prefetchRoute } from './routePrefetch';
import './styles/hizli.css';

// Yönetici oturumundaki API isteklerine Firebase jetonu (sunucu x-admin-email'e güvenmez; src/services/adminAuth.ts)
installAdminFetchAuth();
// Görünen adres katmanı (siteHaritasi): eski biçimli adresler ve history yazımları iç içe adrese çevrilir
// TV / performans modu: <html> sınıfları, TV'de ana sayfa → sesli dersler (adres katmanından önce)
hizliModuKur();
adresKatmaniniKur();
applyTheme(readTheme());
applyUiVersion();
// iOS/iPadOS sınıfları: zoom ve tam ekran CSS kuralları bu sınıflara bağlı (macOS Safari'yi etkilemez).
markDeviceClasses();

// PWA & Çevrimdışı Servis Başlatıcı
if (typeof window !== 'undefined') {
  pwaService.initServiceWorker().catch(() => {});
  offlineDatabaseService.loadStats().catch(() => {});
  arkaPlanPushKur();
  // Sayfa kapalıyken biten canlı ders indirmeleri (sw.js bekleme önbelleği) açılışta kaydedilir
  if ('caches' in window) {
    void caches.has('medsoru-cd-bekleyen').then((v) => { if (v) return import('./components/canliDers/canliDersCevrimdisi').then((m) => m.cdBekleyenleriTamamla()); }).catch(() => {});
  }
  // Çevrimdışı merkezi: yarım kalan indirmeler sürer, çevrimdışı moddaysa uygulama ve ders güncellemeleri iner (services/cevrimdisi)
  if (!hizliMod()) window.setTimeout(() => { void import('./services/cevrimdisi/paketMotoru').then((m) => m.cevrimdisiBaslat()).catch(() => {}); }, 2500);
}

// Klavye açılıp kapanırken görsel alanı izle: katmanlar --vvh ile kısalır,
// alt menü ve FAB klavye açıkken gizlenir; tasarım sıçramaz.
(function trackVisualViewport() {
  const vv = window.visualViewport;
  const root = document.documentElement;
  // Mobilde adres çubuğu kaydırırken sürekli resize/scroll olayı üretir: kare başına en çok bir kez ölç,
  // yalnız DEĞİŞEN değeri yaz (her yazma --vvh kullanan tüm katmanları yeniden yerleştiriyordu → kasma).
  let lastH = -1, lastT = -1, lastKb: boolean | null = null, raf = 0;
  const measure = () => {
    raf = 0;
    const h = Math.round(vv ? vv.height : window.innerHeight);
    const typing = !!(document.activeElement as HTMLElement | null)?.closest?.('input,textarea,select,[contenteditable="true"]');
    const kb = (typing && h < window.innerHeight * 0.8) || (typing && !!vv && vv.height < screen.height * 0.6);
    // offsetTop yalnız klavyede değil, iOS'ta adres çubuğu/kaydırma sırasında da görünür alanı
    // kaydırabilir. Her zaman yaz: tam ekran katmanları `top: var(--vvt)` ile hizalanır.
    const t = vv ? Math.max(0, Math.round(vv.offsetTop)) : 0;
    if (h !== lastH) { lastH = h; root.style.setProperty('--vvh', `${h}px`); }
    if (t !== lastT) { lastT = t; root.style.setProperty('--vvt', `${t}px`); }
    if (kb !== lastKb) { lastKb = kb; root.classList.toggle('kb-open', kb); }
  };
  const update = () => { if (!raf) raf = requestAnimationFrame(measure); };
  measure();
  vv?.addEventListener('resize', update, { passive: true });
  vv?.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update, { passive: true });
  const onFs = () => { update(); setTimeout(update, 120); };
  document.addEventListener('fullscreenchange', onFs, { passive: true });
  document.addEventListener('webkitfullscreenchange', onFs, { passive: true });
  window.addEventListener('medsor:fullscreenchange', onFs, { passive: true });
  document.addEventListener('focusin', () => setTimeout(update, 250));
  document.addEventListener('focusout', () => setTimeout(update, 250));
})();

// alert() and unhandled failures become friendly floating toasts
installToastBridge();
installNetworkBanner();
installUpdatePrompt();
installBakimEkrani();
installNotesSync();
// Günlük önce kurulur: sekme gizlenince önce son ziyaret yazılır, sonra eşitleme gönderir
installEtkinlikGunlugu();
installUserDataAutoBackup();
installStudyTimer();
if (hizliMod()) {
  // TV / performans modu: yan kurulumlar yok; yalnız sesli ders ve çözücü kodu önden iner
  prefetchRoute('canli_ders');
  window.setTimeout(() => { prefetchRoute('soru_cozucu'); prefetchRoute('cikmis_cozucu'); }, 1500);
} else {
  installPullToRefresh();
  installPresence();
  prefetchIdle();
  installAutoReveal();
  installSelectionShare();
}
installKabukBayraklari();

// Auto reload on stale Vite chunk after a new deployment
// (Wi-Fi bağlı ama internetsizken de yenilenmez: önce sunucuya ulaşılıyor mu bakılır)
window.addEventListener('vite:preloadError', (event) => {
  if (!navigator.onLine) {
    event.preventDefault();
    return;
  }
  void sunucuyaUlasilir().then((ok) => {
    if (!ok) return;
    const key = 'medsoru_last_chunk_reload';
    const now = Date.now();
    const last = Number(sessionStorage.getItem(key) || 0);
    if (now - last > 5000) {
      sessionStorage.setItem(key, String(now));
      window.location.reload();
    }
  });
});

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  /** Hata sunucuya (POST /api/istemci-hata) gerçekten ulaştıysa true — "Sorun bize iletildi" yalnız o zaman yazılır */
  iletildi?: boolean;
  yigin?: string;
}

class RootErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('[RootErrorBoundary]:', error, errorInfo);
    this.setState({ yigin: `${error?.stack || ''}\n${errorInfo?.componentStack || ''}`.trim() });
    if (!navigator.onLine) return;
    const msg = error?.message || '';
    if (!/Failed to fetch dynamically imported module|Importing a module script failed/i.test(msg)) {
      void fetch('/api/istemci-hata', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mesaj: msg, yigin: error?.stack || '', bilesen: errorInfo?.componentStack || '', adres: location.pathname + location.search, surum: typeof __MEDS_SURUM__ === 'string' ? __MEDS_SURUM__ : '' }),
      }).then((r) => { if (r.ok) this.setState({ iletildi: true }); }).catch(() => {});
    }
    if (/Failed to fetch dynamically imported module|Importing a module script failed/i.test(msg)) {
      void sunucuyaUlasilir().then((ok) => {
        if (!ok) { this.forceUpdate(); return; } // internetsiz: "cihazında yok" ekranı (render cevrimdisiGibi'ye bakar)
        const key = 'medsoru_last_chunk_reload';
        const now = Date.now();
        const last = Number(sessionStorage.getItem(key) || 0);
        if (now - last > 8000) {
          sessionStorage.setItem(key, String(now));
          window.location.reload();
        }
      });
    }
  }

  handleSoftReload = () => {
    window.location.reload();
  };

  handleHardReset = () => {
    try {
      sessionStorage.clear();
      // Yalnızca geçici chunk/reload ve önbellek anahtarlarını temizle; kullanıcının notlarını,
      // çözdüğü soruları, akıl kartlarını ve favorilerini ASLA silme!
      const volatilePrefixes = ['medsoru_last_chunk_', 'medsoru_chunk_', 'medsoru_db_data_'];
      for (let i = localStorage.length - 1; i >= 0; i--) {
        const k = localStorage.key(i);
        if (k && volatilePrefixes.some((p) => k.startsWith(p))) {
          localStorage.removeItem(k);
        }
      }
      if ('caches' in window) {
        // Kullanıcının elle indirdikleri (çevrimdışı PDF'ler, canlı ders paketleri) korunur
        const korunan = ['medsoru-pdf-offline', 'medsoru-canli-ders-offline', 'medsoru-cd-bekleyen', 'medsor-paket-v1'];
        caches.keys().then((keys) => keys.filter((k) => !korunan.includes(k)).forEach((k) => caches.delete(k))).catch(() => {});
      }
    } catch (e) {}
    window.location.reload();
  };

  handleGoBack = () => {
    this.setState({ hasError: false, error: null });
    if (window.history.length > 1) {
      window.history.back();
    } else {
      window.location.href = '/';
    }
  };

  render() {
    if (this.state.hasError) {
      const msg = this.state.error?.message || 'Bilinmeyen arayüz hatası';
      const isChunkError = /Failed to fetch dynamically imported module|Importing a module script failed/i.test(msg);
      if (isChunkError && cevrimdisiGibi()) return <CevrimdisiYok />;

      const yonetici = isAdminUser(getLocalAdminSession());
      if (isChunkError) {
        return (
          <div className="eh15">
            <div className="eh15-k" role="alert">
              <RefreshCw className="eh15-ik" aria-hidden />
              <h1>Yeni sürüm hazır</h1>
              <p>Sayfayı yenileyince güncel sürüm açılır.</p>
              <div className="eh15-d">
                <button type="button" onClick={this.handleSoftReload} className="v15-btn">Sayfayı yenile</button>
                <button type="button" onClick={this.handleHardReset} className="v15-btn is-ghost">Önbelleği tazele</button>
              </div>
            </div>
          </div>
        );
      }
      // AB17: ham hata metni öğrenciye gösterilmez; yönetici "Ayrıntı"yı açar
      return (
        <div className="eh15">
          <div className="eh15-k" role="alert">
            <AlertTriangle className="eh15-ik" aria-hidden />
            <h1>Bir şeyler ters gitti</h1>
            <p>{this.state.iletildi ? 'Sorun bize iletildi. Sayfayı yenileyerek devam edebilirsin.' : 'Sayfayı yenileyerek devam edebilirsin.'}</p>
            <p className="v15-cap">İnternet yoksa indirdiğin dersler çalışmaya devam eder.</p>
            <div className="eh15-d">
              <button type="button" onClick={this.handleSoftReload} className="v15-btn">Sayfayı yenile</button>
              <button type="button" onClick={this.handleGoBack} className="v15-btn is-ghost">Geri dön</button>
              <a href="/cevrimdisi" className="v15-btn is-ghost">İndirilenler</a>
            </div>
            {yonetici && (
              <details className="eh15-ay">
                <summary>Ayrıntı (yönetici)</summary>
                <pre>{msg}{this.state.yigin ? `\n\n${this.state.yigin}` : ''}</pre>
                <button type="button" onClick={this.handleHardReset} className="v15-btn is-ghost">Önbelleği tazele</button>
              </details>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from './queryClient';
import './styles/erisilebilirlik.css';
import { erisimUygula } from './utils/erisilebilirlik';
erisimUygula();

createRoot(document.getElementById('root')!).render(
  <RootErrorBoundary>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </RootErrorBoundary>
);

