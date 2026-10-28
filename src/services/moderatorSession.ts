/**
 * Moderatör oturumu (istemci): GET /api/me/access ile rol öğrenilir. Moderatör kipinde /api isteklerine
 * Firebase kimlik jetonu (Authorization: Bearer) eklenir; sunucu moderatörü yalnız bu jetondan tanır.
 * Bu modül yetki vermez; yalnız gösterim ve jeton ekleme içindir. Asıl denetim sunucudadır (moderatorAccess.ts).
 */
import { auth, logout } from './auth';

export type AccessRole = 'student' | 'moderator' | 'admin';
export interface MyAccess {
  role: AccessRole;
  suspended: boolean;
}

let moderatorMode = false;
export const isModeratorMode = () => moderatorMode;
export const setModeratorMode = (on: boolean) => {
  moderatorMode = on;
};

/** Moderatörün açabildiği yönetim bölümleri (sunucuda izinli uçlarla eşleşir) */
export const MODERATOR_SECTIONS = ['overview', 'inbox', 'moderation', 'drafts', 'pending'] as const;

export async function fetchMyAccess(): Promise<MyAccess | null> {
  const user = auth.currentUser;
  if (!user) return null;
  try {
    const token = await user.getIdToken();
    const res = await fetch('/api/me/access', { headers: { Authorization: `Bearer ${token}`, Accept: 'application/json' }, cache: 'no-store' });
    if (!res.ok) return null;
    const d = await res.json();
    // Yönetici bu cihazdaki oturumu sonlandırdı (Kullanıcılar › Erişim): çıkış yap, giriş ekranına dön
    if (d?.oturumSonlandirildi) {
      try { await logout(); } catch { /* */ }
      window.location.reload();
      return null;
    }
    const role: AccessRole = d?.role === 'admin' || d?.role === 'moderator' ? d.role : 'student';
    return { role, suspended: !!d?.suspended };
  } catch {
    return null;
  }
}

/** Moderatör kipinde: kendi API'mize giden isteğe jeton ekler (başka adreslere asla) */
export async function attachModeratorToken(url: string, headers: Headers): Promise<void> {
  if (!moderatorMode || headers.has('Authorization')) return;
  let ours = url.startsWith('/api/');
  if (!ours && typeof window !== 'undefined') {
    try {
      const u = new URL(url, window.location.href);
      ours = u.origin === window.location.origin && u.pathname.startsWith('/api/');
    } catch {
      ours = false;
    }
  }
  if (!ours) return;
  const user = auth.currentUser;
  if (!user) return;
  try {
    headers.set('Authorization', `Bearer ${await user.getIdToken()}`);
  } catch {
    /* jeton alınamadı: sunucu 403 döner */
  }
}
