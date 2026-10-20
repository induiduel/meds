/**
 * Kurul kampı ilerlemesi — tek nesne `medsoru_kamp_v1` (userKvSync ile hesaba eşitlenir):
 *   { "k2/farmakoloji": { dinlenen: { <anlatım id>: zaman }, cevap: { <soru id>: { s: "B", d: true } }, bildim: { <kalıp satır id>: zaman } } }
 * Kamp aynı zamanda çalışma takibinde `kamp:k<N>/<brans>` konusudur (services/calismaTakip, /bitirdiklerim?m=kamp).
 */
import { useSyncExternalStore } from 'react';
import type { Kamp } from './kampVeri';

export const KAMP_KEY = 'medsoru_kamp_v1';
const OLAY = 'medsor:kamp-ilerleme';

export interface KampCevap { s: string; d: boolean }
export interface KampKayit { dinlenen: Record<string, number>; cevap: Record<string, KampCevap>; bildim: Record<string, number> }
type Veri = Record<string, KampKayit>;

export const kampAnahtar = (kurul: number, brans: string) => `k${kurul}/${brans}`;
const BOS: KampKayit = { dinlenen: {}, cevap: {}, bildim: {} };

let onbellek: { ham: string | null; v: Veri } = { ham: null, v: {} };
const oku = (): Veri => {
  let ham: string | null = null;
  try { ham = localStorage.getItem(KAMP_KEY); } catch { /* özel pencere */ }
  if (ham !== onbellek.ham) {
    let v: Veri = {};
    try { const x = JSON.parse(ham || '{}'); if (x && typeof x === 'object' && !Array.isArray(x)) v = x; } catch { /* bozuk */ }
    onbellek = { ham, v };
  }
  return onbellek.v;
};

export const kampKaydi = (anahtar: string, v: Veri = oku()): KampKayit => {
  const k = v[anahtar];
  return { dinlenen: k?.dinlenen || {}, cevap: k?.cevap || {}, bildim: k?.bildim || {} };
};

const degistir = (anahtar: string, f: (k: KampKayit) => KampKayit) => {
  const v = oku();
  const yeni = { ...v, [anahtar]: f(kampKaydi(anahtar, v)) };
  try {
    const ham = JSON.stringify(yeni);
    localStorage.setItem(KAMP_KEY, ham);
    onbellek = { ham, v: yeni };
  } catch { /* kota */ }
  window.dispatchEvent(new Event(OLAY));
};

export const dinlendi = (a: string, id: string) =>
  degistir(a, (k) => (k.dinlenen[id] ? k : { ...k, dinlenen: { ...k.dinlenen, [id]: Date.now() } }));
export const cevapla = (a: string, id: string, c: KampCevap) => degistir(a, (k) => ({ ...k, cevap: { ...k.cevap, [id]: c } }));
export const cevapSil = (a: string, ids: string[]) =>
  degistir(a, (k) => { const c = { ...k.cevap }; ids.forEach((i) => delete c[i]); return { ...k, cevap: c }; });
export const bildimDegistir = (a: string, id: string) =>
  degistir(a, (k) => { const b = { ...k.bildim }; if (b[id]) delete b[id]; else b[id] = Date.now(); return { ...k, bildim: b }; });

const abone = (f: () => void) => {
  const g = (e: Event) => { if (e.type === OLAY || (e as StorageEvent).key == null || (e as StorageEvent).key === KAMP_KEY) f(); };
  window.addEventListener('storage', g);
  window.addEventListener(OLAY, g);
  return () => { window.removeEventListener('storage', g); window.removeEventListener(OLAY, g); };
};
const sunucu = (): Veri => ({});
export const useKampVeri = () => useSyncExternalStore(abone, oku, sunucu);
export const useKampKaydi = (anahtar: string): KampKayit => {
  const v = useKampVeri();
  return v[anahtar] ? kampKaydi(anahtar, v) : BOS;
};

/** "Tekrar et": kampın dinleme, deneme ve bildim işaretlerini siler */
export const kampSifirla = (a: string) => degistir(a, () => ({ dinlenen: {}, cevap: {}, bildim: {} }));

export const kalipSatirId = (kalipId: string, i: number) => `${kalipId}-${i}`;

/** Kampın ilerleme özeti (yalnız kampta hâlâ bulunan öğeler sayılır) */
export function kampOzeti(kamp: Kamp, k: KampKayit) {
  const anlatim = kamp.anlatim.filter((m) => k.dinlenen[m.id]).length;
  const cevaplanan = kamp.deneme.filter((s) => k.cevap[s.id]);
  const dogru = cevaplanan.filter((s) => k.cevap[s.id].s === s.dogru).length;
  const satirToplam = kamp.kalipler.reduce((n, x) => n + x.satir.length, 0);
  const bildim = kamp.kalipler.reduce((n, x) => n + x.satir.filter((_, i) => k.bildim[kalipSatirId(x.id, i)]).length, 0);
  const toplam = kamp.anlatim.length + kamp.deneme.length + satirToplam;
  const yapilan = anlatim + cevaplanan.length + bildim;
  return {
    anlatim, cevaplanan: cevaplanan.length, dogru, yanlis: cevaplanan.length - dogru, bildim, satirToplam,
    toplam, yapilan, yuzde: toplam ? Math.round((yapilan / toplam) * 100) : 0, tamam: toplam > 0 && yapilan >= toplam,
  };
}
