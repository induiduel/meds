import { useSyncExternalStore } from 'react';

/**
 * Patoloji · Sesli soru çözücü — veri ve ilerleme deposu.
 * İçerik: src/data/patoloji_cozucu/{index,<kod>}.json (scripts/patoloji_cozucu/cozucu_birlestir.py). Her soru 2026-27 örnek
 * sorularından; ipucu, her şıkkın neden doğru/yanlış olduğu ve çözüm ders sunumuna dayanır. Ses: EMA klipleri
 * /api/patoloji-cozucu/ses/<kod>/<klip>.mp3?v=<özet> (q-n kök+şıklar · i-n ipucu · s-n-H şık · c-n çözüm · d-n "Doğru!").
 */

export type Harf = 'A' | 'B' | 'C' | 'D' | 'E';
export const HARFLER: Harf[] = ['A', 'B', 'C', 'D', 'E'];
export interface Klip { v: string; sure: number; zaman: [number, number][] }
export interface CSoru { no: number; soru: string; secenekler: Record<Harf, string>; dogru: Harf; ipucu: string; siklar: Record<Harf, string>; cozum: string; sayfa: number[] }
export interface CDers { kod: string; no: number; baslik: string; sorular: CSoru[]; klip: Record<string, Klip> }
export interface CDizinDers { kod: string; no: number; baslik: string; soru: number; ses: boolean }
export interface CDizin { surum: string; ortak: Record<string, { v: string; sure: number }>; dersler: CDizinDers[] }

const DOSYA = import.meta.glob('../../../data/patoloji_cozucu/[0-9]*.json') as Record<string, () => Promise<{ default: CDers }>>;
const DIZIN = import.meta.glob('../../../data/patoloji_cozucu/index.json') as Record<string, () => Promise<{ default: CDizin }>>;
const yol = (kod: string) => `../../../data/patoloji_cozucu/${kod}.json`;
const bellek = new Map<string, Promise<CDers>>();
export const cozucuVar = () => Object.keys(DIZIN).length > 0;
export const cozucuDersYukle = (kod: string): Promise<CDers> => {
  let p = bellek.get(kod);
  if (!p) {
    const f = DOSYA[yol(kod)];
    if (!f) return Promise.reject(new Error(`ders yok: ${kod}`));
    p = f().then((m) => m.default);
    p.catch(() => bellek.delete(kod));
    bellek.set(kod, p);
  }
  return p;
};
let dizinP: Promise<CDizin> | null = null;
export const cozucuDizinYukle = (): Promise<CDizin> => {
  if (!dizinP) {
    const f = Object.values(DIZIN)[0];
    dizinP = f ? f().then((m) => m.default) : Promise.resolve({ surum: '', ortak: {}, dersler: [] });
    dizinP.catch(() => { dizinP = null; });
  }
  return dizinP;
};

/** d: ilk denemede yardımsız doğru · d2: yardımla ya da ikinci denemede doğru · y: çözümü dinledi / bilemedi */
export type Sonuc = 'd' | 'd2' | 'y';
export interface DersIlerleme { s: Record<string, Sonuc>; i: number; at: string }
export const ILERLEME_KEY = 'medsoru_cozucu_ilerleme_v1';
export const TERCIH_KEY = 'medsoru_cozucu_tercih_v1';
const OLAY = 'medsor:cozucu-ilerleme';

let onbellek: { ham: string | null; v: Record<string, DersIlerleme> } = { ham: null, v: {} };
const oku = (): Record<string, DersIlerleme> => {
  let ham: string | null = null;
  try { ham = localStorage.getItem(ILERLEME_KEY); } catch { /* özel pencere */ }
  if (ham !== onbellek.ham) {
    let v: Record<string, DersIlerleme> = {};
    try { const x = JSON.parse(ham || '{}'); if (x && typeof x === 'object') v = x; } catch { /* bozuk kayıt */ }
    onbellek = { ham, v };
  }
  return onbellek.v;
};
export const ilerlemeOku = oku;
export const ilerlemeYaz = (kod: string, p: Partial<DersIlerleme> | null) => {
  const t = { ...oku() };
  if (p === null) delete t[kod];
  else t[kod] = { ...{ s: {}, i: 0 }, ...t[kod], ...p, at: new Date().toISOString() };
  try { localStorage.setItem(ILERLEME_KEY, JSON.stringify(t)); } catch { /* özel pencere */ }
  window.dispatchEvent(new Event(OLAY));
};
const abone = (f: () => void) => {
  const g = (e: Event) => { if (e.type === OLAY || (e as StorageEvent).key == null || (e as StorageEvent).key === ILERLEME_KEY) f(); };
  window.addEventListener('storage', g);
  window.addEventListener(OLAY, g);
  return () => { window.removeEventListener('storage', g); window.removeEventListener(OLAY, g); };
};
export const useIlerleme = () => useSyncExternalStore(abone, oku, oku);

/** Ekranda/ilerlemede gösterilen ders numarası (ör. 26b → 27) dizinden gelir; burada yalnız sayım yardımcıları. */
export const ozet = (p: DersIlerleme | undefined, toplam: number) => {
  const s = Object.values(p?.s || {});
  const d = s.filter((x) => x === 'd').length;
  const d2 = s.filter((x) => x === 'd2').length;
  const y = s.filter((x) => x === 'y').length;
  return { d, d2, y, cozulen: s.length, toplam, tamam: s.length >= toplam && toplam > 0 };
};
