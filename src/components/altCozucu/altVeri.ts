/** Patoloji alternatif sesli soru çözücü — veri yükleyici.
 * Metin: src/data/patoloji_cozucu_alt/{index,<kod>}.json (scripts/patoloji_cozucu_alt/paketle.py).
 * Ses: /api/patoloji-cozucu-alt/ses/<kod>/<no>.mp3 (src/services/patolojiCozucuAlt.ts).
 */
export type Harf = 'A' | 'B' | 'C' | 'D' | 'E';
export const HARFLER: Harf[] = ['A', 'B', 'C', 'D', 'E'];
export interface AltSoru {
  no: number;
  tur: 'ornek' | 'cikmis';
  soru: string;
  secenekler: Record<Harf, string>;
  dogru: Harf;
  giris: string;
  aciklamalar: Record<Harf, string>;
  ozet: string;
  mp3: string;
  h: string;
  sure: number;
}
export interface AltDers { kod: string; no: number; baslik: string; sorular: AltSoru[] }
export interface AltDizinDers { kod: string; no: number; baslik: string; soru: number; ornek: number; cikmis: number; sure: number }
export interface AltDizin { surum: string; dersler: AltDizinDers[] }

const DOSYA = import.meta.glob('../../data/patoloji_cozucu_alt/*.json') as Record<string, () => Promise<{ default: unknown }>>;
const yol = (kod: string) => `../../data/patoloji_cozucu_alt/${kod}.json`;

export const altDizinYukle = async (): Promise<AltDizin> => {
  const f = DOSYA['../../data/patoloji_cozucu_alt/index.json'];
  if (!f) return { surum: '', dersler: [] };
  return (await f()).default as AltDizin;
};

const bellek = new Map<string, Promise<AltDers>>();
export const altDersYukle = (kod: string): Promise<AltDers> => {
  let p = bellek.get(kod);
  if (!p) {
    const f = DOSYA[yol(kod)];
    if (!f) return Promise.reject(new Error(`ders yok: ${kod}`));
    p = f().then((m) => m.default as AltDers);
    p.catch(() => bellek.delete(kod));
    bellek.set(kod, p);
  }
  return p;
};

export const altSesYolu = (kod: string, s: AltSoru) =>
  `/api/patoloji-cozucu-alt/ses/${encodeURIComponent(kod)}/${encodeURIComponent(s.mp3)}${s.h ? `?v=${s.h}` : ''}`;

/** Ders başına kalınan soru + dinlenen sorular (tarayıcıda) */
export interface AltIlerleme { i: number; bitti: number[] }
const KEY = 'medsoru_alt_cozucu_v1';
export const ilerlemeOku = (): Record<string, AltIlerleme> => {
  try {
    const x = JSON.parse(localStorage.getItem(KEY) || '{}');
    return x && typeof x === 'object' ? x : {};
  } catch { return {}; }
};
export const ilerlemeYaz = (kod: string, p: AltIlerleme) => {
  try {
    const t = ilerlemeOku();
    t[kod] = p;
    localStorage.setItem(KEY, JSON.stringify(t));
  } catch { /* özel pencere */ }
};

export const dk = (sn: number) => `${Math.max(1, Math.round(sn / 60))} dk`;
export const sureYazi = (sn: number) => {
  if (!sn || !isFinite(sn)) return '0:00';
  const d = Math.floor(sn / 60);
  const s = Math.floor(sn % 60);
  return `${d}:${String(s).padStart(2, '0')}`;
};
