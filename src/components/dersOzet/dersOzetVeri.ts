/**
 * Ders özeti — veri (src/data/ders_ozet/k<N>/{index.json, <ders>.json}; üretim scripts/uretim/ders_ozet/, belge docs/DERS_OZETI_MODULU.md).
 * Ses: EMA klipleri /api/cozucu-ses/k<N>ozet/ema/<kod>/<klip>.mp3 (g giriş · b-i bölüm · a akılda kalması gerekenler);
 * her klipte öğe (madde id / 'baslik' / 'giris' / 'akilda-i') → [başlangıç, bitiş] saniye.
 */
import { useSyncExternalStore } from 'react';
import { getCustomApiUrl } from '../../services/api';

export type MaddeTur = 'bilgi' | 'spot' | 'ayirici' | 'klinik';
export interface OzMadde { id: string; tur: MaddeTur; metin: string; s: number[]; cikmis?: string[] }
export interface OzBolum { id: string; baslik: string; maddeler: OzMadde[] }
export interface OzKlip { v: string; sure: number; oge: Record<string, [number, number]> }
export interface OzDers {
  ders: string; key: string; kod: string; kurul: number; brans?: string; baslik: string; ogretim_uyesi?: string;
  giris: string; bolumler: OzBolum[]; akilda: { metin: string; s: number[]; cikmis?: string[] }[];
  cikmis: { id: string; kok: string; cevap: string; yil?: string; s?: number }[];
  cozucu: { brans: string; kod: string; kodlar?: string[]; soru: number; cikmis: number } | null;
  ses: { brans: string; kod: string; klipler: Record<string, OzKlip> } | null;
  sure: number; kelime?: number;
}
export interface OzDizinDers { ders: string; key: string; kod: string; brans?: string; baslik: string; madde: number; cikmis: number; sure: number; ses: boolean; soru: number }
export interface OzDizin { kurul: number; dersler: OzDizinDers[] }

const DIZIN = import.meta.glob('../../data/ders_ozet/k*/index.json') as Record<string, () => Promise<{ default: OzDizin }>>;
const DERS = import.meta.glob('../../data/ders_ozet/k*/k*-*.json') as Record<string, () => Promise<{ default: OzDers }>>;

export const ozKurullar = (): number[] =>
  Object.keys(DIZIN).map((k) => Number(/\/k(\d+)\/index/.exec(k)?.[1])).filter(Boolean).sort((a, b) => a - b);
export const ozDizinYukle = (kurul: number): Promise<OzDizin | null> => {
  const f = DIZIN[`../../data/ders_ozet/k${kurul}/index.json`];
  return f ? f().then((m) => m.default) : Promise.resolve(null);
};
export const ozDersYukle = (ders: string): Promise<OzDers | null> => {
  const k = /^k(\d)/.exec(ders)?.[1];
  const f = DERS[`../../data/ders_ozet/k${k}/${ders}.json`];
  return f ? f().then((m) => m.default) : Promise.resolve(null);
};
/** Okuma sırası: giriş → bölümler → akılda kalması gerekenler */
export const klipSirasi = (d: OzDers): string[] => ['g', ...d.bolumler.map((_, i) => `b-${i + 1}`), 'a'].filter((k) => d.ses?.klipler[k]);
export const klipAdres = (d: OzDers, klip: string) =>
  d.ses ? `${getCustomApiUrl() || ''}/api/cozucu-ses/${d.ses.brans}/ema/${encodeURIComponent(d.ses.kod)}/${klip}.mp3?v=${d.ses.klipler[klip]?.v || ''}` : '';
/** Öğe kimliğinin bulunduğu klip */
export const ogeKlibi = (d: OzDers, oge: string): string | null => {
  for (const [k, x] of Object.entries(d.ses?.klipler || {})) if (x.oge[oge]) return k;
  return null;
};
export const TUR_AD: Record<MaddeTur, string> = { bilgi: '', spot: 'Spot', ayirici: 'Ayırıcı', klinik: 'Klinik' };
export const dk = (sn: number) => `${Math.max(1, Math.round(sn / 60))} dk`;

/** İlerleme (yalnız bu cihaz): ders → son klip/saniye, bitti zamanı */
export interface OzIlerleme { klip?: string; t?: number; bitti?: string; at: string }
const ILERLEME_KEY = 'medsoru_ders_ozet_v1';
let onbellek: Record<string, OzIlerleme> | null = null;
const abone = new Set<() => void>();
function oku(): Record<string, OzIlerleme> {
  if (onbellek) return onbellek;
  try { onbellek = JSON.parse(localStorage.getItem(ILERLEME_KEY) || '{}') || {}; } catch { onbellek = {}; }
  return onbellek!;
}
export function ozIlerlemeYaz(ders: string, p: Partial<OzIlerleme> | null) {
  const t = { ...oku() };
  if (p === null) delete t[ders]; else t[ders] = { ...t[ders], ...p, at: new Date().toISOString() };
  onbellek = t;
  try { localStorage.setItem(ILERLEME_KEY, JSON.stringify(t)); } catch { /* özel pencere: yalnız bellekte */ }
  abone.forEach((f) => f());
}
// Hesaptan gelen güncelleme (userKvSync storage olayı) ya da başka sekme: önbelleği boşalt, ekranı yenile
if (typeof window !== 'undefined') window.addEventListener('storage', (e) => {
  if (e.key === ILERLEME_KEY || e.key === null) { onbellek = null; abone.forEach((f) => f()); }
});
export const useOzIlerleme = () => useSyncExternalStore((f) => { abone.add(f); return () => abone.delete(f); }, oku, oku);
