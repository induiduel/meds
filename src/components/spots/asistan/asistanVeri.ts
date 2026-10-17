/** Sesli sınav asistanı içerik dosyaları (ders başına tembel). Sayfa yalnız varlığını sorar; içerik asistan açılınca iner.
 *  Branş klasörleri src/data/<brans>_asistan/; ders kodları branşlar arasında tekil (patoloji "07", enfeksiyon "e07", üroloji "u03"). */
import type { Brans } from '../brans';

const DOSYA = import.meta.glob('../../../data/*_asistan/[0-9eu]*.json');
const DIZIN = import.meta.glob('../../../data/*_asistan/index.json');
export const kodBrans = (kod: string): Brans => (kod.startsWith('e') ? 'enfeksiyon' : kod.startsWith('u') ? 'uroloji' : 'patoloji');
export const asistanYolu = (kod: string) => `../../../data/${kodBrans(kod)}_asistan/${kod}.json`;
export const asistanDersVar = (kod: string) => !!DOSYA[asistanYolu(kod)];
export const asistanDosyasi = (kod: string) => DOSYA[asistanYolu(kod)] as (() => Promise<{ default: unknown }>) | undefined;
export const asistanDersleri = (brans: Brans) =>
  Object.keys(DOSYA).filter((k) => k.includes(`/${brans}_asistan/`)).map((k) => k.replace(/^.*\/(\w+)\.json$/, '$1'));
export const asistanDizinDosyasi = (brans: Brans) => DIZIN[`../../../data/${brans}_asistan/index.json`] as (() => Promise<{ default: any }>) | undefined;
