/**
 * AB06 · Bildirim tercihleri. Yalnız sitede gerçekten üretilen bildirim türleri (BildirimlerV15 türetilenleri +
 * userNotificationService hesap bildirimleri). Profil anahtarı `medsoru_bildirim_tercih_v1` (userKvSync SYNC_PATTERNS:
 * cihazlar arası eşitlenir). Uygulama noktaları:
 *  - BildirimlerV15: kapalı türün satırı listelenmez.
 *  - userNotificationService.addNotification: kapalı türse kaydedilmez; sessiz saatte sistem (anlık) bildirimi gösterilmez.
 */
import { useEffect, useState } from 'react';
import type { UserNotification } from './userNotificationService';

export type BildirimTur = 'yeni_ders' | 'sinav' | 'pratik' | 'yanlis' | 'yorum' | 'katki' | 'hata_bildirimi' | 'revizyon' | 'yapay_zeka' | 'sistem';

export const BILDIRIM_TURLERI: { id: BildirimTur; ad: string; alt: string; grup: 'Ders' | 'Soru' | 'Sistem' }[] = [
  { id: 'yeni_ders', ad: 'Yeni sesli ders', alt: 'Listeye yeni bir sesli ders eklendiğinde', grup: 'Ders' },
  { id: 'sinav', ad: 'Sınav yaklaşıyor', alt: 'Kurul sınavına 14 gün ve daha az kaldığında', grup: 'Ders' },
  { id: 'pratik', ad: 'Sınav öncesi pratik', alt: 'Sınavdan 5, 3 ve 1 gün önce (Sınav takviminde açtıysan)', grup: 'Soru' },
  { id: 'yanlis', ad: 'Yanlış tekrarı', alt: 'Yanlış yaptığın soruların tekrar zamanı geldiğinde', grup: 'Soru' },
  { id: 'yorum', ad: 'Yorumlar', alt: 'Sorularına yorum eklendiğinde ya da silindiğinde', grup: 'Soru' },
  { id: 'katki', ad: 'Katkılar', alt: 'Sorularına katkı geldiğinde', grup: 'Soru' },
  { id: 'hata_bildirimi', ad: 'Hata bildirimleri', alt: 'Bildirdiğin hata alındığında ve çözüldüğünde', grup: 'Soru' },
  { id: 'revizyon', ad: 'Soru düzeltmeleri', alt: 'Bir soru düzeltildiğinde', grup: 'Soru' },
  { id: 'yapay_zeka', ad: 'Yapay zekâ işleri', alt: 'Soru yeniden kurma sıraya alındığında ve bittiğinde', grup: 'Soru' },
  { id: 'sistem', ad: 'Site bildirimleri', alt: 'İşlem sonuçları ve uyarılar', grup: 'Sistem' },
];

export const BILDIRIM_TERCIH_KEY = 'medsoru_bildirim_tercih_v1';
export interface BildirimTercih { kapali: Partial<Record<BildirimTur, 1>>; sessiz: { acik: boolean; bas: string; bit: string } }
const VARSAYILAN: BildirimTercih = { kapali: {}, sessiz: { acik: false, bas: '23:00', bit: '08:00' } };

export function tercihOku(): BildirimTercih {
  try {
    const j = JSON.parse(localStorage.getItem(BILDIRIM_TERCIH_KEY) || 'null');
    if (j && typeof j === 'object') return { kapali: { ...(j.kapali || {}) }, sessiz: { ...VARSAYILAN.sessiz, ...(j.sessiz || {}) } };
  } catch { /* bozuk */ }
  return { kapali: {}, sessiz: { ...VARSAYILAN.sessiz } };
}
export function tercihYaz(t: BildirimTercih) {
  try { localStorage.setItem(BILDIRIM_TERCIH_KEY, JSON.stringify(t)); } catch { /* yok */ }
  try { window.dispatchEvent(new Event('medsoru:bildirim-tercih')); } catch { /* sunucu */ }
}
export function useBildirimTercih(): [BildirimTercih, (t: BildirimTercih) => void] {
  const [t, setT] = useState(tercihOku);
  useEffect(() => {
    const f = () => setT(tercihOku());
    const st = (e: StorageEvent) => { if (e.key === BILDIRIM_TERCIH_KEY) f(); };
    window.addEventListener('medsoru:bildirim-tercih', f);
    window.addEventListener('storage', st);
    window.addEventListener('medsoru:user-data-synced', f);
    return () => { window.removeEventListener('medsoru:bildirim-tercih', f); window.removeEventListener('storage', st); window.removeEventListener('medsoru:user-data-synced', f); };
  }, []);
  return [t, (n) => { tercihYaz(n); setT(n); }];
}

export const turAcik = (tur: BildirimTur, t: BildirimTercih = tercihOku()) => !t.kapali[tur];

/** Hesap bildirim tipini tercih türüne çevirir */
export function hesapTuru(type: UserNotification['type']): BildirimTur {
  if (type.startsWith('comment_')) return 'yorum';
  if (type === 'contribution_added') return 'katki';
  if (type.startsWith('report_')) return 'hata_bildirimi';
  if (type === 'question_revised') return 'revizyon';
  if (type.startsWith('ai_')) return 'yapay_zeka';
  return 'sistem';
}

const dk = (s: string) => { const m = /^(\d{1,2}):(\d{2})$/.exec(s); return m ? Number(m[1]) * 60 + Number(m[2]) : null; };
/** Şu an sessiz saatlerde mi (gece yarısını aşan aralık desteklenir) */
export function sessizSaatte(t: BildirimTercih = tercihOku(), simdi = new Date()): boolean {
  if (!t.sessiz.acik) return false;
  const a = dk(t.sessiz.bas), b = dk(t.sessiz.bit);
  if (a == null || b == null || a === b) return false;
  const n = simdi.getHours() * 60 + simdi.getMinutes();
  return a < b ? n >= a && n < b : n >= a || n < b;
}
