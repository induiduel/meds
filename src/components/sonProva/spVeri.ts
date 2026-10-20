/**
 * Son Prova — veri ve ilerleme deposu.
 * İçerik: src/data/son_prova/k<N>/index.json (kurul, sınav dağılımı, dersler → partlar → aşamalar, genel check-up, denemeler)
 * ve sorular/<brans>.json (soru çözücü havuzundan seçilen sorular; meds_temp/son_prova/soru_dagit.py üretir).
 * Partın anlatımı sesli ders altyapısındadır (anahtar = part key, ör. k1-81-son-prova-patoloji-1; kırpılmış özet PDF'i
 * deste k1p-<key>). Soru sesleri soru çözücü klipleridir: /api/cozucu-ses/<brans>/ema/<klasör>/<q|i|c|d|s>-<no>.mp3.
 * İlerleme: localStorage medsoru_son_prova_v1 (userKvSync ile hesaba eşitlenir).
 */
import { useSyncExternalStore } from 'react';
import { getCustomApiUrl } from '../../services/api';

export type Harf = 'A' | 'B' | 'C' | 'D' | 'E';
export interface SpAsama { no: number; baslik: string; ders: string; dersAd: string; dersNo: string; p: [number, number]; sorular: string[]; checkup: string[] }
export interface SpPart { key: string; no: number; baslik: string; kelime: number; tahminiDk: number; sayfa: number; dersler: { kod: string; no: string; ad: string }[]; asamalar: SpAsama[] }
export interface SpDers { brans: string; ad: string; soru: number; genel: string[]; partlar: SpPart[] }
export interface SpDeneme { no: number; sure: number; sorular: string[] }
export interface SpIndex { kurul: number; ad: string; surum: string; sinav: Record<string, { ad: string; soru: number }>; dersler: SpDers[]; denemeler: SpDeneme[] }
export interface SpSoru {
  soru: string; secenekler: Partial<Record<Harf, string>>; dogru: Harf; ipucu: string; siklar: Partial<Record<Harf, string>>; cozum: string;
  tur?: 'cikmis' | 'ornek' | 'benzer' | 'yeni'; sinav?: string; zorluk?: 'kolay' | 'orta' | 'zor';
  kaynak: { kod: string; s: number[] }; asama: [string, number]; kl: string; klip: Record<string, string>;
}

const INDEX = import.meta.glob('../../data/son_prova/k*/index.json') as Record<string, () => Promise<{ default: SpIndex }>>;
const SORU = import.meta.glob('../../data/son_prova/k*/sorular/*.json') as Record<string, () => Promise<{ default: Record<string, SpSoru> }>>;

export const spKurullar = (): number[] =>
  Object.keys(INDEX).map((k) => Number(/\/k(\d+)\//.exec(k)?.[1])).filter(Boolean).sort((a, b) => a - b);

const indexP = new Map<number, Promise<SpIndex>>();
export function spIndexYukle(kurul: number): Promise<SpIndex> {
  let p = indexP.get(kurul);
  if (!p) {
    const f = INDEX[`../../data/son_prova/k${kurul}/index.json`];
    p = f ? f().then((m) => m.default) : Promise.reject(new Error('Bu kurulun Son Prova içeriği yok'));
    p.catch(() => indexP.delete(kurul));
    indexP.set(kurul, p);
  }
  return p;
}
const soruP = new Map<string, Promise<Record<string, SpSoru>>>();
function bransSorulari(kurul: number, brans: string) {
  const a = `${kurul}/${brans}`;
  let p = soruP.get(a);
  if (!p) {
    const f = SORU[`../../data/son_prova/k${kurul}/sorular/${brans}.json`];
    p = f ? f().then((m) => m.default) : Promise.resolve({});
    p.catch(() => soruP.delete(a));
    soruP.set(a, p);
  }
  return p;
}
/** ref listesindeki soruları (sırayla) yükler: "patoloji/07#12" */
export async function spSorulariYukle(kurul: number, refs: string[]): Promise<(SpSoru & { ref: string })[]> {
  const branslar = [...new Set(refs.map((r) => r.split('/')[0]))];
  const tum = Object.assign({}, ...(await Promise.all(branslar.map((b) => bransSorulari(kurul, b)))));
  return refs.filter((r) => tum[r]).map((r) => ({ ...tum[r], ref: r }));
}
export const spBrans = (ref: string) => ref.split('/')[0];
const soruNo = (ref: string) => ref.split('#')[1];
/** Soru klibi adresi; klip yoksa null (tarayıcı sesiyle okunmaz — sessiz geçilir) */
export function spKlip(ref: string, q: SpSoru, tur: 'q' | 'i' | 'c' | 'd' | 's', harf?: Harf): string | null {
  const v = q.klip[tur === 's' ? `s${harf}` : tur];
  if (!v) return null;
  const ad = tur === 's' ? `s-${soruNo(ref)}-${harf}` : `${tur}-${soruNo(ref)}`;
  return `${getCustomApiUrl() || ''}/api/cozucu-ses/${spBrans(ref)}/ema/${encodeURIComponent(q.kl)}/${ad}.mp3?v=${v}`;
}
/** Tüm partlar: anahtar → [ders, part] */
export const spPartBul = (ix: SpIndex, key: string): { ders: SpDers; part: SpPart } | null => {
  for (const d of ix.dersler) for (const p of d.partlar) if (p.key === key) return { ders: d, part: p };
  return null;
};
export const BRANS_KISA: Record<string, string> = {
  patoloji: 'Patoloji', enfeksiyon: 'Enfeksiyon', genetik: 'Genetik', uroloji: 'Üroloji', halksagligi: 'Halk Sağlığı',
  kadindogum: 'Kadın Doğum', farmakoloji: 'Farmakoloji',
};
export const BRANS_RENK: Record<string, string> = {
  patoloji: '#E11D48', enfeksiyon: '#0EA5E9', genetik: '#10B981', uroloji: '#F59E0B', halksagligi: '#8B5CF6',
  kadindogum: '#EC4899', farmakoloji: '#14B8A6',
};

/* ---------------- ilerleme ---------------- */
export interface TestSonuc { d: number; n: number; at: number; yanlis: string[] }
export interface SpKayit {
  /** "<partKey>:<aşama>" → aşama sonu soruları sonucu */
  asama: Record<string, TestSonuc>;
  /** partKey → part check-up */
  checkup: Record<string, TestSonuc>;
  /** "k<kurul>:<brans>" → genel check-up */
  genel: Record<string, TestSonuc>;
  /** "k<kurul>:<no>" → deneme (cevaplar sürer; bitince sonuç) */
  deneme: Record<string, { cevap: Record<string, Harf>; bas: number; bitti?: number; sonuc?: TestSonuc }>;
}
export const SP_KEY = 'medsoru_son_prova_v1';
const BOS: SpKayit = { asama: {}, checkup: {}, genel: {}, deneme: {} };
let ham: string | null = null;
let kayit: SpKayit = BOS;
const oku = (): SpKayit => {
  let h: string | null = null;
  try { h = localStorage.getItem(SP_KEY); } catch { /* özel pencere */ }
  if (h !== ham) {
    ham = h;
    try { kayit = { ...BOS, ...(h ? JSON.parse(h) : {}) }; } catch { kayit = BOS; }
  }
  return kayit;
};
const subs = new Set<() => void>();
export function spYaz(f: (k: SpKayit) => SpKayit) {
  const n = f(oku());
  try { localStorage.setItem(SP_KEY, JSON.stringify(n)); } catch { /* yer yok */ }
  ham = null;
  subs.forEach((x) => x());
}
if (typeof window !== 'undefined') window.addEventListener('storage', (e) => { if (e.key === SP_KEY) { ham = null; subs.forEach((x) => x()); } });
export const useSpKayit = (): SpKayit => useSyncExternalStore((f) => { subs.add(f); return () => { subs.delete(f); }; }, oku, () => BOS);

/** Bir partın ilerlemesi: biten aşama sayısı + check-up */
export function partIlerleme(k: SpKayit, p: SpPart) {
  const biten = p.asamalar.filter((a) => k.asama[`${p.key}:${a.no}`]).length;
  return { biten, toplam: p.asamalar.length, checkup: k.checkup[p.key] || null };
}
/** Yanlış sorulardan zayıf aşamalar: [partKey, aşama] → yanlış sayısı (çoktan aza) */
export function zayifAsamalar(yanlislar: (SpSoru & { ref: string })[]) {
  const m = new Map<string, { part: string; no: number; n: number }>();
  for (const q of yanlislar) {
    const a = `${q.asama[0]}:${q.asama[1]}`;
    const x = m.get(a) || { part: q.asama[0], no: q.asama[1], n: 0 };
    x.n++;
    m.set(a, x);
  }
  return [...m.values()].sort((a, b) => b.n - a.n);
}
export const yuzde = (d: number, n: number) => (n ? Math.round((100 * d) / n) : 0);
