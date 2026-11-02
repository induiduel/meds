import { useSyncExternalStore } from 'react';

/** Hocanın ders kaydında vurguladığı yerler (scripts/hoca_vurgu/yayinla.py → src/data/hoca_vurgu/<ders>.json). */
export type HvKategori = 'sorulur' | 'cikmis' | 'onemli' | 'bilin' | 'dikkat';
export interface HvVurgu {
  id: string;
  kategori: HvKategori;
  /** hocanın tetikleyici sözü ("bunu sınavda sorarım") */
  ifade: string;
  /** hocanın cümlesi, terimleri slayta göre düzeltilmiş */
  alinti: string;
  /** vurgulanan bilginin slayttaki karşılığı */
  konu: string;
  s: number | null;
  /** ders kaydındaki zaman (dk:sn) */
  dk: string;
  /** sesli derste bilginin anlatıldığı paragraf / Öğren adımı */
  p: number | null;
  adim: number | null;
}
export interface HvDers { ders: string; key: string; vurgular: HvVurgu[] }

export const HV_KATEGORI: { id: HvKategori; ad: string }[] = [
  { id: 'sorulur', ad: 'Sınavda sorulur' }, { id: 'cikmis', ad: 'Çıkmıştı' }, { id: 'onemli', ad: 'Önemli' },
  { id: 'bilin', ad: 'Bilin' }, { id: 'dikkat', ad: 'Dikkat' },
];

const VERI = import.meta.glob('../../data/hoca_vurgu/k*.json', { import: 'default' }) as Record<string, () => Promise<HvDers>>;
const ders = (key: string) => key.replace(/-v\d+$/, '').split('-').slice(0, 2).join('-');
const bul = (key: string) => Object.entries(VERI).find(([p]) => p.endsWith(`/${ders(key)}.json`))?.[1];
export const hocaVurguVar = (key: string) => !!bul(key);
export const hocaVurguGetir = async (key: string): Promise<HvDers | null> => (await bul(key)?.()) || null;

// Öğrencinin işaretledikleri (profil eşitlemesi: userKvSync SYNC_PATTERNS medsoru_hoca_vurgu_isaret_v1)
const ANAHTAR = 'medsoru_hoca_vurgu_isaret_v1';
type Isaret = Record<string, number>;
let onbellek: Isaret | null = null;
const dinleyici = new Set<() => void>();
const oku = (): Isaret => {
  if (onbellek) return onbellek;
  try { onbellek = JSON.parse(localStorage.getItem(ANAHTAR) || '{}') || {}; } catch { onbellek = {}; }
  return onbellek!;
};
if (typeof window !== 'undefined')
  window.addEventListener('storage', (e) => { if (e.key === ANAHTAR || e.key == null) { onbellek = null; dinleyici.forEach((f) => f()); } });
export const hvIsaretli = (m: Isaret, id: string) => !!m[id];
export function hvIsaretle(id: string, on: boolean) {
  const m = { ...oku() };
  if (on) m[id] = Date.now(); else delete m[id];
  onbellek = m;
  try { localStorage.setItem(ANAHTAR, JSON.stringify(m)); } catch { /* depolama kapalı: oturumda kalır */ }
  dinleyici.forEach((f) => f());
}
export const useHvIsaret = () => useSyncExternalStore((f) => { dinleyici.add(f); return () => { dinleyici.delete(f); }; }, oku, oku);
