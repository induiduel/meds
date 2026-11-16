// H588: Tembel bileşenler için TEK güvenli yükleyici. Depoda `React.lazy(` yalnız burada geçer
// (kapı: scripts/kapilar/lazy_denetim.py).
//
// Kök neden: `vite:preloadError` dinleyicisi (index.html / main.tsx / manage-main.tsx) preventDefault() çağırınca
// Vite'ın `__vitePreload` sarıcısı başarısız parça içe aktarımını REDDETMEK yerine `undefined` ile ÇÖZER;
// çıplak React.lazy o zaman `e._result.default` / React #306 ile çöker. Burada boş modül ve `default`'suz modül
// yükleme hatası sayılır; `.then(m => ({ default: m.X }))` biçimindeki adlı dışa aktarımda `m` undefined ise
// oluşan TypeError da aynı yola düşer.
import React from 'react';
import CevrimdisiYok from '../components/cevrimdisi/CevrimdisiYok';
import { sunucuyaUlasilir } from '../services/cevrimdisi/baglanti';

type Modul<T> = { default: T };

const YenidenDeneKarti: React.FC = () => (
  <div className="p-8 text-center text-ink-3 max-w-md mx-auto my-12 bg-white rounded-2xl border border-line shadow-sm">
    <div className="text-3xl mb-3">📶</div>
    <p className="font-semibold text-ink text-base">Bileşen yüklenirken bir sorun oluştu.</p>
    <p className="text-sm mt-1.5 text-ink-2">Lütfen sayfayı yenileyiniz veya bağlantınızı kontrol ediniz.</p>
    <div className="mt-5 flex items-center justify-center gap-2.5">
      <button type="button" onClick={() => window.location.reload()}
        className="px-4 py-2 bg-accent text-white rounded-xl text-sm font-semibold hover:bg-accent-hover cursor-pointer transition-colors">
        Yeniden Dene
      </button>
    </div>
  </div>
);

const CevrimdisiBilgi: React.FC = () => <CevrimdisiYok />;

/** Yükleme sözünü sarar: boş modül/`default` yok → hata; hata → (çevrimiçi) kısıtlı tek yenileme, aksi hâlde bilgi bileşeni. */
export function guvenliYukle<T extends React.ComponentType<any>>(soz: Promise<Modul<T>>): Promise<Modul<T>> {
  return soz.then((m) => {
    if (!m || !(m as Partial<Modul<T>>).default) throw new Error('chunk default export missing (parça yüklenemedi)');
    return m;
  }).catch(async (err: unknown) => {
    const e = err as { message?: string } | undefined;
    console.warn('[SafeLazy] Failed to load component:', e?.message || err);
    // navigator.onLine Wi-Fi'ye bağlı ama internetsiz cihazda da true: yenileme kararı yalnız sunucu gerçekten yanıt verirse
    const cevrimici = typeof window !== 'undefined' && navigator.onLine && (await sunucuyaUlasilir());
    if (cevrimici) {
      const msg = String(e?.message || err || '');
      if (
        msg.includes('dynamically imported module') ||
        msg.includes('Failed to fetch') ||
        msg.includes('default') ||
        // adlı dışa aktarım: import() undefined çözünce `.then(m => m.X)` TypeError verir
        err instanceof TypeError
      ) {
        const son = sessionStorage.getItem('medsoru_chunk_reload');
        if (!son || Date.now() - Number(son) > 8000) {
          sessionStorage.setItem('medsoru_chunk_reload', String(Date.now()));
          window.location.reload();
        }
      }
      return { default: YenidenDeneKarti as unknown as T };
    }
    // İnternetsiz ve parça cihazda yok: bilgi ekranı (bağlantı gelince kendiliğinden yenilenir)
    return { default: CevrimdisiBilgi as unknown as T };
  });
}

/** `React.lazy` yerine kullanılır: `guvenliLazy(() => import('./X'))` ya da `.then(m => ({ default: m.X }))`. */
export function guvenliLazy<T extends React.ComponentType<any>>(
  yukleyici: () => Promise<Modul<T>>,
): React.LazyExoticComponent<T> {
  return React.lazy(() => {
    let soz: Promise<Modul<T>>;
    try { soz = yukleyici(); } catch (err) { soz = Promise.reject(err); }
    return guvenliYukle(soz);
  });
}
