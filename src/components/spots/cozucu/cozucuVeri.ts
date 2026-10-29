import { useSyncExternalStore } from 'react';
import type { Brans } from '../brans';
import { icerikGizli } from '../../../services/siteAyar';

/**
 * Sesli soru çözücü — veri ve ilerleme deposu (branş geneli: patoloji, enfeksiyon, üroloji).
 * İçerik: src/data/<brans>_cozucu/{index,<kod>}.json (patoloji: scripts/patoloji_cozucu/cozucu_birlestir.py; diğerleri:
 * scripts/spot_cozucu/birlestir.py). Patoloji soruları: 2026-27 örnek (ornek), benzer, çıkmış; diğer branşlar: çıkmış + çıkmışların
 * üslubunda örnek sorular (zorluk kolay/orta/zor), 40'tan çok sorulu ders setlere bölünür (kod "e04-1", klip klasörü `klasor` "e04").
 * Ses: /api/cozucu-ses/<brans>/<ses>/<klasor>/<klip>.mp3?v=<özet> (q-n kök+şıklar · i-n ipucu · s-n-H şık · c-n çözüm · d-n "Doğru!").
 * Varsayılan ses `klip` alanında (EMA); başka sesler `klipSes[<ses>]` + dizinde `sesler` / `ortakSes` (altyapı; şimdilik yalnız EMA).
 */

export type Harf = 'A' | 'B' | 'C' | 'D' | 'E';
export const HARFLER: Harf[] = ['A', 'B', 'C', 'D', 'E'];
export interface Klip { v: string; sure: number; zaman: [number, number][] }
export type SoruTur = 'ornek' | 'benzer' | 'cikmis';
export type Zorluk = 'kolay' | 'orta' | 'zor';
export interface CSoru { no: number; tur?: SoruTur; sinav?: string; zorluk?: Zorluk; soru: string; secenekler: Record<Harf, string>; dogru: Harf; ipucu: string; siklar: Record<Harf, string>; cozum: string; sayfa: number[]
  /** paket sorusu: ses klasörü + klip numarası (asıl derste no) ve kaynak ders (Öğren paneli, etiket) */
  klasor?: string; kn?: number; kaynak?: { kod: string; no: number; baslik: string; dersNo: number };
  /** kısa not (spot bilgisi, slayttan): klasor "@a/<asistan kodu>" + klip ise EMA ile okunur */
  not?: { baslik: string; cumleler: string[]; kaynak: string; klasor?: string; klip?: string };
  /** ders içi ara soru (k<N>hocaara): açıldığı slayt + çözümü önceki slaytlardan anlatan metin (klip a-n) */
  ara?: { dosya: number; sayfa: number; paragraf: number | null }; anlatim?: string;
}
export interface CDers {
  kod: string; no: number; baslik: string; sorular: CSoru[]; klip: Record<string, Klip>;
  /** ses klasörü (setlere bölünen derste ders kodu; yoksa kod) */
  klasor?: string; set?: number; setSay?: number;
  /** varsayılan dışındaki seslerin klipleri */
  klipSes?: Record<string, Record<string, Klip>>;
}
export interface CDizinDers { kod: string; key?: string; no: number; baslik: string; soru: number; ornek?: number; benzer?: number; cikmis?: number; ses: boolean; set?: number; setSay?: number; sayfa?: [number, number]; sure?: number }
export interface SesTanim { id: string; ad: string; varsayilan?: boolean }
export interface CDizin {
  surum: string; ortak: Record<string, { v: string; sure: number }>; dersler: CDizinDers[];
  /** üretilmiş sesler (ilk/varsayilan = klip alanı); yoksa yalnız EMA */
  sesler?: SesTanim[]; ortakSes?: Record<string, Record<string, { v: string; sure: number }>>;
}
export const VARSAYILAN_SES = 'ema';
export const sesListesi = (d: CDizin | null): SesTanim[] => (d?.sesler?.length ? d.sesler : [{ id: VARSAYILAN_SES, ad: 'EMA', varsayilan: true }]);

const DOSYA = import.meta.glob('../../../data/*_cozucu/*.json') as Record<string, () => Promise<{ default: CDers | CDizin }>>;
const yol = (brans: Brans, kod: string) => `../../../data/${brans}_cozucu/${kod}.json`;
const bellek = new Map<string, Promise<CDers>>();
/** Panel görünürlüğü (cozucu:<dizin>/<kod>, kurul:<n>) */
const kapali = (brans: Brans, kod: string) => icerikGizli('cozucu', `${brans}_cozucu/${kod}`);
export const cozucuVar = (brans: Brans = 'patoloji') => !!DOSYA[yol(brans, 'index')];
export const cozucuDersYukle = (kod: string, brans: Brans = 'patoloji'): Promise<CDers> => {
  const a = `${brans}/${kod}`;
  let p = bellek.get(a);
  if (!p) {
    const f = DOSYA[yol(brans, kod)];
    if (!f || kod === 'index') return Promise.reject(new Error(`ders yok: ${kod}`));
    if (kapali(brans, kod)) return Promise.reject(new Error('Bu içerik şu an kapalı'));
    p = f().then((m) => m.default as CDers);
    p.catch(() => bellek.delete(a));
    bellek.set(a, p);
  }
  return p;
};
const dizinP = new Map<Brans, Promise<CDizin>>();
export const cozucuDizinYukle = (brans: Brans = 'patoloji'): Promise<CDizin> => {
  let p = dizinP.get(brans);
  if (!p) {
    const f = DOSYA[yol(brans, 'index')];
    p = f ? f().then((m) => m.default as CDizin) : Promise.resolve({ surum: '', ortak: {}, dersler: [] });
    p.catch(() => dizinP.delete(brans));
    dizinP.set(brans, p);
  }
  // Panel görünürlüğü her çağrıda uygulanır (önbellekteki dizin değişmez)
  return p.then((d) => ({ ...d, dersler: (d.dersler || []).filter((x: any) => !kapali(brans, String(x.kod))) }));
};
/** Ses klibinin adresi (sunucu: src/services/cozucuSes.ts) */
export const klipYolu = (brans: Brans, ses: string, klasor: string, klip: string) =>
  `/api/cozucu-ses/${brans}/${encodeURIComponent(ses)}/${encodeURIComponent(klasor)}/${encodeURIComponent(klip)}.mp3`;
/** Ders listesinde set adı: "Set 1/2 · s. 1–30" */
export const setAdi = (d: { set?: number; setSay?: number; sayfa?: [number, number] }) =>
  d.set && d.setSay && d.setSay > 1 ? `Set ${d.set}/${d.setSay}${d.sayfa ? ` · s. ${d.sayfa[0]}–${d.sayfa[1]}` : ''}` : '';

/** d: ilk denemede yardımsız doğru · d2: yardımla ya da ikinci denemede doğru · y: çözümü dinledi / bilemedi */
export type Sonuc = 'd' | 'd2' | 'y';
/** s: soru no → sonuç · i: listedeki konum (eski kayıt) · q: kalınan sorunun no'su (sıra değişse de doğru yere döner) */
export interface DersIlerleme { s: Record<string, Sonuc>; i: number; q?: number; at: string }
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
