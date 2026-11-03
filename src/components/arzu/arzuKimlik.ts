/**
 * Arzu'ya özel katmanın kimlik kapısı. Yalnız bu hesaplar (ve yönetici) görür; başka hiçbir kullanıcı için parça yüklenmez
 * (ArzuKatmani tembel çağrılır). Güncelleme notlarında anılmaz: sürpriz.
 *
 * Önizleme (yalnız geliştirici): localStorage `medsoru_arzu_onizleme` = '1' → katman açılır.
 */
import { ADMIN_EMAIL, type AppUser } from '../../services/auth';

// Yönetici de görür (kullanıcı kararı 2026-11-03)
const EPOSTALAR = new Set(['arzuturk361@gmail.com', 'drarzuturk@gmail.com', 'arzuturk@gmail.com', ADMIN_EMAIL.toLowerCase()]);
const UIDLER = new Set(['q7YHMBOsJdekIe6HLMaJ8NxMQfm1', 'std-gcdo0r-muvm9owv']);

export const ARZU_ONIZLEME_KEY = 'medsoru_arzu_onizleme';

export function arzuMu(user: AppUser | null | undefined): boolean {
  try {
    if (typeof window !== 'undefined' && window.localStorage.getItem(ARZU_ONIZLEME_KEY) === '1') return true;
  } catch { /* depolama kapalı */ }
  if (!user) return false;
  if (user.uid && UIDLER.has(user.uid)) return true;
  const e = (user.email || '').trim().toLowerCase();
  return !!e && EPOSTALAR.has(e);
}
