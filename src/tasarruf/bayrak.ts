/**
 * Tasarruf kipi (kullanıcı kararı 2026-11-25): yönetici ve moderatör DIŞINDAKİ herkes sade kabuğu görür —
 * yalnız sesli dersler, sesli soru çözücü, çıkmışlar ve ayarlar. Animasyon, diyalog, çevrimdışı, profil,
 * sıralama yok. Kapatmak için TASARRUF_ACIK = false. Yönetici önizlemesi: localStorage medsor_tasarruf_onizleme=1.
 */
import type { AppRoute } from '../router';

export const TASARRUF_ACIK = true;

/** Tasarruf kabuğunun açtığı sayfalar; geri kalanı yokmuş gibi ilk sayfaya döner */
export const TASARRUF_SAYFALAR: { tab: AppRoute; ad: string }[] = [
  { tab: 'canli_ders', ad: 'Sesli dersler' },
  { tab: 'soru_cozucu', ad: 'Soru çözücü' },
  { tab: 'past_exams', ad: 'Çıkmışlar' },
  { tab: 'settings', ad: 'Ayarlar' },
];
export const TASARRUF_ROTALAR = new Set<string>(TASARRUF_SAYFALAR.map((s) => s.tab));

const onizleme = () => { try { return localStorage.getItem('medsor_tasarruf_onizleme') === '1'; } catch { return false; } };

/** rolBilindi: moderatör rolü sunucudan gelmeden öğrenci kabuğu açılmaz (yanıp sönme olmasın) */
export function tasarrufAcik(yonetici: boolean, moderator: boolean, rolBilindi: boolean): boolean {
  if (!TASARRUF_ACIK) return false;
  if (yonetici || moderator) return onizleme();
  return rolBilindi;
}
