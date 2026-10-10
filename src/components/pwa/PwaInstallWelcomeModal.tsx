import React, { useState, useEffect } from 'react';
import {
  Smartphone,
  DownloadCloud,
  WifiOff,
  Zap,
  RefreshCw,
  X,
  Share2,
  CheckCircle2,
  Database,
  ArrowRight,
  ShieldCheck,
} from 'lucide-react';
import { pwaService, PwaState } from '../../services/pwaService';
import { offlineDatabaseService, OfflineState } from '../../services/offlineDatabaseService';

interface PwaInstallWelcomeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenOfflineDatabase: () => void;
}

export const PWA_WELCOME_STORAGE_KEY = 'medsoru_pwa_welcome_dismissed_v1';

export const PwaInstallWelcomeModal: React.FC<PwaInstallWelcomeModalProps> = ({
  isOpen,
  onClose,
  onOpenOfflineDatabase,
}) => {
  const [pwaState, setPwaState] = useState<PwaState>(pwaService.getState());
  const [offlineState, setOfflineState] = useState<OfflineState>(offlineDatabaseService.getState());
  const [isIos, setIsIos] = useState(false);
  const [showIosGuide, setShowIosGuide] = useState(false);
  const [dontShowAgain, setDontShowAgain] = useState(false);

  useEffect(() => {
    const unsubPwa = pwaService.subscribe(setPwaState);
    const unsubOffline = offlineDatabaseService.subscribe(setOfflineState);

    if (typeof window !== 'undefined') {
      const ua = window.navigator.userAgent.toLowerCase();
      setIsIos(/iphone|ipad|ipod/.test(ua));
    }

    return () => {
      unsubPwa();
      unsubOffline();
    };
  }, []);

  if (!isOpen) return null;

  const handleDismiss = (permanent: boolean = false) => {
    if (typeof window !== 'undefined') {
      try {
        const val = permanent || dontShowAgain ? 'permanent' : String(Date.now());
        localStorage.setItem(PWA_WELCOME_STORAGE_KEY, val);
      } catch {}
    }
    onClose();
  };

  const handleInstallAndDownload = async () => {
    handleDismiss(true);

    if (pwaState.canInstall) {
      await pwaService.promptInstall();
    } else if (isIos) {
      setShowIosGuide(true);
      return;
    }

    // Doğrudan veritabanı modalını aç ve indirmeyi başlat
    onOpenOfflineDatabase();
    setTimeout(() => {
      offlineDatabaseService.downloadEntireDatabase();
    }, 400);
  };

  const handleOnlyDatabase = () => {
    handleDismiss(true);
    onOpenOfflineDatabase();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3.5 sm:p-4 bg-slate-950/75 backdrop-blur-md animate-in fade-in duration-200">
      <div
        className="w-full max-w-lg bg-surface border border-line rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh] animate-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Başlık ve Kapat */}
        <div className="relative p-5 pb-4 border-b border-line bg-gradient-to-br from-accent/10 via-surface to-surface flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-accent text-white flex items-center justify-center shadow-lg shadow-accent/25 shrink-0">
              <Smartphone className="w-6 h-6" />
            </div>
            <div>
              <div className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-accent-soft text-accent text-[11px] font-bold uppercase tracking-wider mb-1">
                <ShieldCheck className="w-3.5 h-3.5" />
                PWA & Çevrimdışı Mod
              </div>
              <h2 className="text-lg sm:text-xl font-bold text-ink leading-tight">
                MeDSor'u Cihazınıza Yükleyin
              </h2>
            </div>
          </div>

          <button
            type="button"
            onClick={() => handleDismiss(false)}
            className="w-8 h-8 rounded-full hover:bg-surface-hover flex items-center justify-center text-ink-3 hover:text-ink transition-colors cursor-pointer"
            aria-label="Kapat"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* İçerik */}
        <div className="p-5 overflow-y-auto space-y-4 text-sm">
          <p className="text-ink-2 leading-relaxed">
            MeDSor uygulamasını telefonunuza veya bilgisayarınıza bağımsız uygulama olarak yükleyebilir,
            tüm tıp veritabanını tek tıkla indirerek <strong>internetsiz (%100 çevrimdışı)</strong> çalışabilirsiniz.
          </p>

          {/* Avantajlar Kartı */}
          <div className="space-y-2.5">
            <div className="p-3.5 rounded-2xl bg-canvas border border-line flex items-start gap-3">
              <div className="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center shrink-0 mt-0.5">
                <WifiOff className="w-4 h-4" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-ink">Tam Çevrimdışı Tıp Veritabanı</h4>
                <p className="text-xs text-ink-3 mt-0.5 leading-snug">
                  5.600+ çıkmış soru, 114 interaktif deste, tıbbi sözlük ve akıl kartları cihazınıza kaydedilir. Metroda veya nöbette internetsiz çözün.
                </p>
              </div>
            </div>

            <div className="p-3.5 rounded-2xl bg-canvas border border-line flex items-start gap-3">
              <div className="w-8 h-8 rounded-xl bg-indigo-500/10 text-indigo-600 flex items-center justify-center shrink-0 mt-0.5">
                <Zap className="w-4 h-4" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-ink">Hızlı & Tam Ekran Uygulama Deneyimi</h4>
                <p className="text-xs text-ink-3 mt-0.5 leading-snug">
                  Tarayıcı çubuğu olmadan tam ekran çalışır. Ana ekranınızdan tek dokunuşla anında açılır.
                </p>
              </div>
            </div>

            <div className="p-3.5 rounded-2xl bg-canvas border border-line flex items-start gap-3">
              <div className="w-8 h-8 rounded-xl bg-teal-500/10 text-teal-600 flex items-center justify-center shrink-0 mt-0.5">
                <RefreshCw className="w-4 h-4" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-ink">Arka Planda Akıllı Senkronizasyon</h4>
                <p className="text-xs text-ink-3 mt-0.5 leading-snug">
                  Çevrimdışıyken işaretlediğiniz veya katkıda bulunduğunuz sorular ağ bağlantısı sağlandığında otomatik senkronize edilir.
                </p>
              </div>
            </div>
          </div>

          {/* iOS Kullanıcıları için özel rehber */}
          {showIosGuide && (
            <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/25 space-y-2 animate-in fade-in duration-150">
              <div className="flex items-center gap-2 text-amber-700 dark:text-amber-300 font-bold text-xs">
                <Share2 className="w-4 h-4" />
                iOS (iPhone / iPad) Kurulum Adımları
              </div>
              <ol className="text-xs text-ink-2 space-y-1.5 list-decimal list-inside pl-1">
                <li>Safari tarayıcısının altındaki <strong>Paylaş</strong> simgesine dokunun.</li>
                <li>Açılan menüyü aşağı kaydırıp <strong>"Ana Ekrana Ekle"</strong> seçeneğini seçin.</li>
                <li>Sağ üstteki <strong>"Ekle"</strong> butonuna dokunarak kurulumu tamamlayın.</li>
              </ol>
            </div>
          )}

          {/* Bir daha gösterme seçeneği */}
          <label className="flex items-center gap-2 pt-1 text-xs text-ink-3 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={dontShowAgain}
              onChange={(e) => setDontShowAgain(e.target.checked)}
              className="rounded border-line text-accent focus:ring-accent cursor-pointer"
            />
            <span>Bu öneriyi bir daha açılışta gösterme</span>
          </label>
        </div>

        {/* Alt Eylem Butonları */}
        <div className="p-4 border-t border-line bg-surface-hover/20 flex flex-col gap-2">
          <button
            type="button"
            onClick={handleInstallAndDownload}
            className="w-full py-3.5 px-4 rounded-2xl bg-accent text-white font-bold text-sm flex items-center justify-center gap-2 hover:bg-accent-hover active:scale-[0.99] transition-all shadow-lg shadow-accent/20 cursor-pointer"
          >
            <DownloadCloud className="w-4 h-4" />
            Uygulamayı ve Veritabanını Kur
            <ArrowRight className="w-4 h-4" />
          </button>

          <div className="grid grid-cols-2 gap-2 pt-0.5">
            <button
              type="button"
              onClick={handleOnlyDatabase}
              className="py-2.5 px-3 rounded-xl bg-canvas border border-line hover:bg-surface-hover text-ink text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors cursor-pointer"
            >
              <Database className="w-3.5 h-3.5 text-accent" />
              Sadece Veritabanını İndir
            </button>

            <button
              type="button"
              onClick={() => handleDismiss(dontShowAgain)}
              className="py-2.5 px-3 rounded-xl hover:bg-surface-hover text-ink-3 hover:text-ink text-xs font-medium flex items-center justify-center transition-colors cursor-pointer"
            >
              Daha Sonra
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
