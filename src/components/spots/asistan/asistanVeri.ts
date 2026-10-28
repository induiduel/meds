/** Sesli sınav asistanı içerik dosyaları (ders başına tembel). Sayfa yalnız varlığını sorar; içerik asistan açılınca iner.
 *  Branş klasörleri src/data/<brans>_asistan/; ders kodları branşlar arasında tekil (patoloji "07", enfeksiyon "e07", üroloji "u03"). */
import type { Brans } from '../brans';
import branslarVeri from '../../../data/dersler/branslar.json';
import { icerikGizli } from '../../../services/siteAyar';

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
/** Panel görünürlüğü (asistan:<dizin>/<kod>, kurul:<n>) */
const kapali = (kod: string) => icerikGizli('asistan', `${kodBrans(kod)}_asistan/${kod}`);
export const asistanDersVar = (kod: string) => !kapali(kod) && !!DOSYA[asistanYolu(kod)];
export const asistanDosyasi = (kod: string) => (kapali(kod) ? undefined : DOSYA[asistanYolu(kod)]) as (() => Promise<{ default: unknown }>) | undefined;
export const asistanDersleri = (brans: Brans) =>
  Object.keys(DOSYA).filter((k) => k.includes(`/${brans}_asistan/`)).map((k) => k.replace(/^.*\/(\w+)\.json$/, '$1')).filter((k) => !kapali(k));
export const asistanDizinDosyasi = (brans: Brans) => {
  const f = DIZIN[`../../../data/${brans}_asistan/index.json`] as (() => Promise<{ default: any }>) | undefined;
  if (!f) return undefined;
  // Panelde kapatılan dersler dizinden süzülür
  return () => f().then((m) => ({ ...m, default: { ...m.default, dersler: (m.default?.dersler || []).filter((x: any) => !kapali(String(x.kod))) } }));
};
