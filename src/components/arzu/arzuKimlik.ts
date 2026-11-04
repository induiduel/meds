/**
 * Arzu'ya özel katmanın kimlik kapısı. Yalnız bu hesaplar (ve yönetici) görür; başka hiçbir kullanıcı için parça yüklenmez
 * (ArzuKatmani tembel çağrılır). Güncelleme notlarında anılmaz: sürpriz.
 *
 * Önizleme (yalnız geliştirici): localStorage `medsoru_arzu_onizleme` = '1' → katman açılır.
 */
import { useEffect, useState } from 'react';
import { ADMIN_EMAIL, type AppUser } from '../../services/auth';

// Yönetici de görür (kullanıcı kararı 2026-11-03)
const EPOSTALAR = new Set(['arzuturk361@gmail.com', 'drarzuturk@gmail.com', 'arzuturk@gmail.com', ADMIN_EMAIL.toLowerCase()]);
const UIDLER = new Set(['q7YHMBOsJdekIe6HLMaJ8NxMQfm1', 'std-gcdo0r-muvm9owv']);

export const ARZU_ONIZLEME_KEY = 'medsoru_arzu_onizleme';
/** Ayarlar › "Küçük sürprizler" kapatıldıysa '1' (cihaza özel). */
export const ARZU_KAPALI_KEY = 'medsoru_arzu_kapali';
export const ARZU_AYAR_OLAYI = 'medsoru:arzu-ayar';

const depoOku = (k: string) => { try { return typeof window !== 'undefined' ? window.localStorage.getItem(k) : null; } catch { return null; } };

/** Hesap bu katmanı görebilecek hesaplardan mı (kapatma ayarına bakılmaz). */
export function arzuHesabiMi(user: AppUser | null | undefined): boolean {
  if (depoOku(ARZU_ONIZLEME_KEY) === '1') return true;
  if (!user) return false;
  if (user.uid && UIDLER.has(user.uid)) return true;
  const e = (user.email || '').trim().toLowerCase();
  return !!e && EPOSTALAR.has(e);
}

export const arzuKapaliMi = (): boolean => depoOku(ARZU_KAPALI_KEY) === '1';

/** Katmanı aç/kapat; App ve ayar satırı olayla yenilenir. */
export function arzuKatmaniAyarla(acik: boolean): void {
  try {
    if (acik) window.localStorage.removeItem(ARZU_KAPALI_KEY);
    else window.localStorage.setItem(ARZU_KAPALI_KEY, '1');
  } catch { /* depolama kapalı */ }
  try { window.dispatchEvent(new CustomEvent(ARZU_AYAR_OLAYI, { detail: { acik } })); } catch { /* yok */ }
}

/** Katman gösterilsin mi: hesap uygun ve kullanıcı kapatmamış. */
export function arzuMu(user: AppUser | null | undefined): boolean {
  return arzuHesabiMi(user) && !arzuKapaliMi();
}

/** Ayar değişince yeniden okuyan kanca. */
export function useArzuAcik(): boolean {
  const [acik, setAcik] = useState(() => !arzuKapaliMi());
  useEffect(() => {
    const d = () => setAcik(!arzuKapaliMi());
    window.addEventListener(ARZU_AYAR_OLAYI, d);
    window.addEventListener('storage', d);
    return () => { window.removeEventListener(ARZU_AYAR_OLAYI, d); window.removeEventListener('storage', d); };
  }, []);
  return acik;
}
