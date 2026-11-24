import React from 'react';
import { RefreshCw, LogOut, TriangleAlert } from 'lucide-react';
import type { AppUser } from '../../services/auth';
import '../../styles/v15/ek15.css';

/**
 * Engelli hesap ekranı (2026-11-23/24, kullanıcı kararı): izinli olmayan hesap sıradan bir yükleme hatası görür
 * (erişim kısıtından söz edilmez). Kabuk/veritabanı hiç kurulmaz. Liste: services/erisimSiniri.ts.
 */
export default function ErisimKapali({ onLogout }: { currentUser: AppUser | null; onLogout: () => void }) {
  // Cihazda önceki oturumdan kalan veri olabilir (önbellek/IndexedDB): bir kez boşaltılır.
  React.useEffect(() => {
    const temizle = async () => {
      try { void import('../../services/offlineDatabaseService').then((m) => m.offlineDatabaseService.clearDatabase()).catch(() => {}); } catch { /* yok */ }
      try {
        if (typeof caches !== 'undefined') {
          for (const ad of await caches.keys()) {
            if (/data|api|paket|canli|pdf|soru|ders/i.test(ad)) await caches.delete(ad).catch(() => false);
          }
        }
      } catch { /* önbellek erişimi yok */ }
    };
    void temizle();
  }, []);
  const [deniyor, setDeniyor] = React.useState(false);
  const kod = React.useMemo(() => `E${500 + Math.floor(Math.random() * 4)}-${Date.now().toString(36).slice(-6).toUpperCase()}`, []);
  const tekrar = () => {
    setDeniyor(true);
    window.setTimeout(() => window.location.reload(), 1200);
  };
  return (
    <div className="min-h-dvh w-full bg-canvas text-ink flex items-center justify-center p-4 font-sans antialiased" role="main">
      <div className="max-w-[460px] w-full bg-white border border-line rounded-2xl p-6 sm:p-8 flex flex-col items-center text-center gap-3">
        <span className="w-12 h-12 rounded-2xl bg-canvas border border-line text-ink-2 flex items-center justify-center">
          <TriangleAlert className="w-6 h-6" aria-hidden />
        </span>
        <h1 className="m-0 font-display font-bold text-2xl tracking-[-0.02em]">İçerikler yüklenemedi</h1>
        <p className="m-0 text-md text-ink-2">
          Sunucuyla iletişim sırasında beklenmeyen bir hata oluştu. Ders ve soru verileri şu an alınamıyor.
        </p>
        <p className="m-0 text-sm text-ink-2">Biraz sonra yeniden dene. Sorun sürerse sayfayı kapatıp tekrar aç.</p>
        <div className="flex flex-wrap justify-center gap-2 pt-2">
          <button
            type="button"
            onClick={tekrar}
            disabled={deniyor}
            className="h-11 px-5 rounded-xl bg-accent hover:bg-accent-hover text-white font-semibold text-md cursor-pointer inline-flex items-center gap-2 disabled:opacity-70"
          >
            <RefreshCw className={`w-4 h-4 ${deniyor ? 'animate-spin' : ''}`} aria-hidden />
            {deniyor ? 'Yeniden deneniyor…' : 'Tekrar dene'}
          </button>
          <button
            type="button"
            onClick={onLogout}
            className="h-11 px-4 rounded-xl border border-line-2 bg-white font-semibold text-md cursor-pointer inline-flex items-center gap-2"
          >
            <LogOut className="w-4 h-4" aria-hidden />
            Çıkış yap
          </button>
        </div>
        <p className="m-0 pt-1 text-xs text-ink-2 font-mono opacity-70">Hata kodu: {kod}</p>
      </div>
    </div>
  );
}
