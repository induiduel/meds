/**
 * Dil ve bölge tercihleri (cihaza özgü; userKvSync DEVICE_PREFS'te — profile eşitlenmez).
 * Site yalnız Türkçedir; burada yalnız gerçekten uygulanan biçim tercihleri durur:
 *  - tarih: 'uzun' (29 Ekim Perşembe) | 'kisa' (29.10.2026 Perşembe) — ders programı ve program kartı
 *  - saat: '24' (13:30) | '12' (1:30 ÖS) — ders programı, program kartı, arka plan işleri
 *  - haftaBas: 1 Pazartesi | 0 Pazar — ders programı ay ızgarası
 */
import { useSyncExternalStore } from 'react';

export interface BolgeTercih { tarih: 'uzun' | 'kisa'; saat: '24' | '12'; haftaBas: 0 | 1 }
export const BOLGE_KEY = 'medsoru_bolge_v1';
const OLAY = 'medsor:bolge';
const VARSAYILAN: BolgeTercih = { tarih: 'uzun', saat: '24', haftaBas: 1 };

let ham: string | null | undefined;
let onb: BolgeTercih = VARSAYILAN;
export const bolgeOku = (): BolgeTercih => {
  let h: string | null = null;
  try { h = localStorage.getItem(BOLGE_KEY); } catch { /* yok */ }
  if (h !== ham) {
    ham = h;
    try { onb = { ...VARSAYILAN, ...(h ? JSON.parse(h) : {}) }; } catch { onb = VARSAYILAN; }
  }
  return onb;
};
export const bolgeYaz = (p: Partial<BolgeTercih>) => {
  try { localStorage.setItem(BOLGE_KEY, JSON.stringify({ ...bolgeOku(), ...p })); } catch { /* dolu */ }
  window.dispatchEvent(new Event(OLAY));
};
const abone = (f: () => void) => {
  const g = (e: Event) => { if (!(e instanceof StorageEvent) || e.key === BOLGE_KEY) f(); };
  window.addEventListener(OLAY, g); window.addEventListener('storage', g);
  return () => { window.removeEventListener(OLAY, g); window.removeEventListener('storage', g); };
};
export const useBolge = () => useSyncExternalStore(abone, bolgeOku, bolgeOku);

/** "08:50" → tercihe göre "08:50" ya da "8:50 ÖÖ" */
export function saatYaz(hhmm: string | undefined, t: BolgeTercih = bolgeOku()): string {
  if (!hhmm) return '';
  const m = /^(\d{1,2}):(\d{2})/.exec(hhmm);
  if (!m || t.saat === '24') return hhmm;
  const s = Number(m[1]);
  return `${s % 12 || 12}:${m[2]} ${s < 12 ? 'ÖÖ' : 'ÖS'}`;
}
/** Date → saat:dakika (tercihli) */
export const saatDate = (d: Date, t: BolgeTercih = bolgeOku()) =>
  saatYaz(`${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`, t);

/** ISO gün (YYYY-AA-GG) → tercihli tarih; haftaGunu ile gün adı da eklenir */
export function tarihYaz(gun: string, t: BolgeTercih = bolgeOku(), o: { gunAdi?: boolean; kisaAd?: boolean } = { gunAdi: true }): string {
  const d = new Date(`${gun}T12:00:00`);
  if (t.tarih === 'kisa') {
    const s = d.toLocaleDateString('tr-TR', { day: '2-digit', month: '2-digit', year: 'numeric' });
    return o.gunAdi ? `${s} ${d.toLocaleDateString('tr-TR', { weekday: o.kisaAd ? 'short' : 'long' })}` : s;
  }
  return d.toLocaleDateString('tr-TR', o.gunAdi ? { weekday: o.kisaAd ? 'short' : 'long', day: 'numeric', month: o.kisaAd ? undefined : 'long' } : { day: 'numeric', month: 'long', year: 'numeric' });
}

/** Cihazın saat dilimi ve Türkiye saatinden farkı (dakika) */
export function saatDilimi(): { ad: string; farkDk: number } {
  let ad = '';
  try { ad = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch { /* yok */ }
  // Türkiye UTC+3 (yaz saati yok); cihaz ofseti getTimezoneOffset dakika cinsinden ters işaretli
  const farkDk = -new Date().getTimezoneOffset() - 180;
  return { ad, farkDk };
}
