import React, { Component, ErrorInfo, ReactNode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import './styles/health.css';
import { installToastBridge } from './components/ui/Toast';
import { applyTheme, readTheme } from './utils/theme';
import { applyUiVersion } from './utils/uiVersion';
import { pwaService } from './services/pwaService';
import { offlineDatabaseService } from './services/offlineDatabaseService';

applyTheme(readTheme());
applyUiVersion();

// PWA & Çevrimdışı Servis Başlatıcı
if (typeof window !== 'undefined') {
  pwaService.initServiceWorker().catch(() => {});
  offlineDatabaseService.loadStats().catch(() => {});
}

// Klavye açılıp kapanırken görsel alanı izle: katmanlar --vvh ile kısalır,
// alt menü ve FAB klavye açıkken gizlenir; tasarım sıçramaz.
(function trackVisualViewport() {
  const vv = window.visualViewport;
  const root = document.documentElement;
  const update = () => {
    const h = vv ? vv.height : window.innerHeight;
    root.style.setProperty('--vvh', `${Math.round(h)}px`);
    root.style.setProperty('--vvt', `${Math.round(vv ? vv.offsetTop : 0)}px`);
    const typing = !!(document.activeElement as HTMLElement | null)?.closest?.('input,textarea,select,[contenteditable="true"]');
    root.classList.toggle('kb-open', typing && h < window.innerHeight * 0.8 || (typing && !!vv && vv.height < screen.height * 0.6));
  };
  update();
  vv?.addEventListener('resize', update);
  vv?.addEventListener('scroll', update);
  window.addEventListener('resize', update);
  document.addEventListener('focusin', () => setTimeout(update, 250));
  document.addEventListener('focusout', () => setTimeout(update, 250));
})();

// alert() and unhandled failures become friendly floating toasts
installToastBridge();

// Auto reload on stale Vite chunk after a new deployment
window.addEventListener('vite:preloadError', (event) => {
  if (!navigator.onLine) {
    event.preventDefault();
    return;
  }
  const key = 'medsoru_last_chunk_reload';
  const now = Date.now();
  const last = Number(sessionStorage.getItem(key) || 0);
  if (now - last > 5000) {
    sessionStorage.setItem(key, String(now));
    window.location.reload();
  }
});

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
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
    if (!navigator.onLine) return;
    const msg = error?.message || '';
    if (/Failed to fetch dynamically imported module|Importing a module script failed/i.test(msg)) {
      const key = 'medsoru_last_chunk_reload';
      const now = Date.now();
      const last = Number(sessionStorage.getItem(key) || 0);
      if (now - last > 8000) {
        sessionStorage.setItem(key, String(now));
        window.location.reload();
      }
    }
  }

  handleSoftReload = () => {
    window.location.reload();
  };

  handleHardReset = () => {
    try {
      localStorage.clear();
      sessionStorage.clear();
    } catch (e) {}
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      const msg = this.state.error?.message || 'Bilinmeyen arayüz hatası';
      const isChunkError = /Failed to fetch dynamically imported module|Importing a module script failed/i.test(msg);

      return (
        <div className="min-h-dvh bg-ink text-white flex flex-col items-center justify-center p-4">
          <div className="max-w-md w-full bg-ink border border-line-2 rounded-2xl p-6 shadow-2xl text-center space-y-4">
            <div className="w-12 h-12 bg-bad/20 text-bad-text rounded-full flex items-center justify-center mx-auto text-xl font-bold">
              !
            </div>
            <h2 className="text-lg font-bold text-ink-3">
              {isChunkError ? 'Yeni Sürüm Tespit Edildi' : 'Uygulama Yüklenirken Bir Sorun Oluştu'}
            </h2>
            <p className="text-xs text-ink-3 font-mono bg-ink p-3 rounded-lg text-left overflow-auto max-h-32">
              {msg}
            </p>
            <div className="flex flex-col sm:flex-row gap-2 justify-center pt-2">
              <button
                onClick={this.handleSoftReload}
                className="bg-ok hover:bg-ok text-white text-xs font-bold px-4 py-2.5 rounded-lg cursor-pointer transition-colors"
              >
                Sayfayı Yenile (Güncelle)
              </button>
              <button
                onClick={this.handleHardReset}
                className="bg-ink-2 hover:bg-ink-2 text-ink-3 text-xs font-medium px-3 py-2.5 rounded-lg cursor-pointer transition-colors"
              >
                Önbelleği Sıfırla
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

createRoot(document.getElementById('root')!).render(
  <RootErrorBoundary>
    <App />
  </RootErrorBoundary>
);
