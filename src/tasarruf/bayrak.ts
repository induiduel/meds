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

/**
 * Bot (yapay zekâ test erişimi) geçişi: `?tasarruf=0` normal mod, `?tasarruf=1` tasarruf kipi; seçim cihazda kalır
 * (medsor_tasarruf_bot). Yalnız aiTest oturumunda okunur; gerçek öğrenciyi etkilemez.
 */
const BOT_KEY = 'medsor_tasarruf_bot';
// Parametre modül yüklenirken okunur: yönlendirme/kanonik adres onu aiTest bilinmeden önce silebiliyor
try { const q = new URLSearchParams(location.search).get('tasarruf'); if (q === '0' || q === '1') localStorage.setItem(BOT_KEY, q); } catch { /* yok */ }
export function botTasarrufTercihi(): boolean | null {
  try {
    const v = localStorage.getItem(BOT_KEY);
    return v === '0' ? false : v === '1' ? true : null;
  } catch { return null; }
}
export function botTasarrufAyarla(acik: boolean) { try { localStorage.setItem(BOT_KEY, acik ? '1' : '0'); } catch { /* yok */ } location.reload(); }

/** rolBilindi: moderatör rolü sunucudan gelmeden öğrenci kabuğu açılmaz (yanıp sönme olmasın); bot: aiTest oturumu */
export function tasarrufAcik(yonetici: boolean, moderator: boolean, rolBilindi: boolean, bot = false): boolean {
  if (!TASARRUF_ACIK) return false;
  if (bot) { const t = botTasarrufTercihi(); if (t !== null) return t; }
  if (yonetici || moderator) return onizleme();
  return rolBilindi;
}
