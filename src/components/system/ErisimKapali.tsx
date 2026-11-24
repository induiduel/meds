import React from 'react';
import { LockKeyhole, LogOut, Mail } from 'lucide-react';
import type { AppUser } from '../../services/auth';
import { ERISIM_KAPALI_MESAJI } from '../../services/erisimSiniri';
import { navigateTo } from '../../router';
import '../../styles/v15/ek15.css';

/**
 * Erişim kapalı ekranı (2026-11-23, kullanıcı kararı): site yalnız Arzu Türk ve yönetici hesabına açıktır.
 * İzinli listede olmayan bir hesapla giriş yapılınca uygulama kabuğu/veritabanı hiç kurulmaz, bu ekran kalır.
 * Kapatılamaz; tek çıkış "Çıkış yap". Liste: services/erisimSiniri.ts (sunucu kapısıyla AYNI kaynak).
 */
export default function ErisimKapali({ currentUser, onLogout }: { currentUser: AppUser | null; onLogout: () => void }) {
  // Cihazda önceki oturumdan kalan veri olabilir (önbellek/IndexedDB): engelli hesap okumasın diye bir kez boşaltılır.
  React.useEffect(() => {
    const temizle = async () => {
      try { void import('../../services/offlineDatabaseService').then((m) => m.offlineDatabaseService.clearDatabase()).catch(() => {}); } catch { /* yok */ }
      try {
        if (typeof caches !== 'undefined') {
          for (const ad of await caches.keys()) {
            // Kullanıcının indirdiği çevrimdışı ders/ses paketleri dahil hepsi: bu hesap içeriği görmemeli
            if (/data|api|paket|canli|pdf|soru|ders/i.test(ad)) await caches.delete(ad).catch(() => false);
          }
        }
      } catch { /* önbellek erişimi yok */ }
    };
    void temizle();
  }, []);
  return (
    <div className="min-h-dvh w-full bg-canvas text-ink flex items-center justify-center p-4 font-sans antialiased" role="main">
      <div className="max-w-[460px] w-full bg-white border border-line rounded-2xl p-6 sm:p-8 flex flex-col items-center text-center gap-3">
        <span className="w-12 h-12 rounded-2xl bg-ink text-white flex items-center justify-center">
          <LockKeyhole className="w-6 h-6" aria-hidden />
        </span>
        <h1 className="m-0 font-display font-bold text-2xl tracking-[-0.02em]">Bu hesaba site kapalı</h1>
        <p className="m-0 text-md text-ink-2">{ERISIM_KAPALI_MESAJI}</p>
        {currentUser?.email && (
          <p className="m-0 text-sm text-ink-2 inline-flex items-center gap-2">
            <Mail className="w-4 h-4" aria-hidden />
            <b>{currentUser.email}</b>
          </p>
        )}
        <p className="m-0 text-sm text-ink-2">
          Hesabının açılması için site yöneticisine başvurabilirsin.
        </p>
        <div className="flex flex-wrap justify-center gap-2 pt-2">
          <button
            type="button"
            onClick={onLogout}
            className="h-11 px-5 rounded-xl bg-accent hover:bg-accent-hover text-white font-semibold text-md cursor-pointer inline-flex items-center gap-2"
          >
            <LogOut className="w-4 h-4" aria-hidden />
            Çıkış yap
          </button>
          <button
            type="button"
            onClick={() => navigateTo('/')}
            className="h-11 px-4 rounded-xl border border-line-2 bg-white font-semibold text-md cursor-pointer"
          >
            Giriş ekranına dön
          </button>
        </div>
      </div>
    </div>
  );
}
