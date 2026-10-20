/** Sesli sınav asistanı içerik dosyaları (ders başına tembel). Sayfa yalnız varlığını sorar; içerik asistan açılınca iner.
 *  Branş klasörleri src/data/<brans>_asistan/; ders kodları branşlar arasında tekil (patoloji "07", enfeksiyon "e07", üroloji "u03"). */
import type { Brans } from '../brans';
import branslarVeri from '../../../data/dersler/branslar.json';

const DOSYA = import.meta.glob('../../../data/*_asistan/[0-9eughkf]*.json');
const DIZIN = import.meta.glob('../../../data/*_asistan/index.json');
const ONEK_BRANS: Record<string, Brans> = {
  e: 'enfeksiyon', u: 'uroloji', g: 'genetik', h: 'halksagligi', k: 'kadindogum', f: 'farmakoloji',
};
const HARF_SLUG: Record<string, string> = Object.fromEntries(
  (branslarVeri as any).branslar.map((b: any) => [b.harf, b.slug]),
);
/** Kurul 1: önek harfi (e07) ya da rakam (07 = patoloji). Kurul 2+: <kurul><harf><no> (2n03) → k2noroloji (sunucu
 *  services/patolojiAsistan.ts bransKlasor ile aynı kural). */
export const kodBrans = (kod: string): Brans => {
  const m = /^(\d)([a-z])\d{2}/.exec(kod);
  if (m && HARF_SLUG[m[2]]) return `k${m[1]}${HARF_SLUG[m[2]]}` as Brans;
  return ONEK_BRANS[kod[0]] || 'patoloji';
};
export const asistanYolu = (kod: string) => `../../../data/${kodBrans(kod)}_asistan/${kod}.json`;
export const asistanDersVar = (kod: string) => !!DOSYA[asistanYolu(kod)];
export const asistanDosyasi = (kod: string) => DOSYA[asistanYolu(kod)] as (() => Promise<{ default: unknown }>) | undefined;
export const asistanDersleri = (brans: Brans) =>
  Object.keys(DOSYA).filter((k) => k.includes(`/${brans}_asistan/`)).map((k) => k.replace(/^.*\/(\w+)\.json$/, '$1'));
export const asistanDizinDosyasi = (brans: Brans) => DIZIN[`../../../data/${brans}_asistan/index.json`] as (() => Promise<{ default: any }>) | undefined;
