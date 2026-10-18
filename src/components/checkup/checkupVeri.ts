/**
 * Patoloji Hızlı Check Up verisi — src/data/patoloji_checkup/NN-*.json (tek kaynak; doğrulayıcı:
 * scripts/patoloji_checkup/dogrula.py, 0 HATA vermeden yayınlanmaz). Kaynak "kod:slayt" biçimindedir
 * (kod = Kurul 1 patoloji ders PDF'i, slayt = PDF sayfası); ders adları dersler.json'dan gelir.
 */
import dersler from '../../data/patoloji_checkup/dersler.json';

export interface CuTablo {
  id: string;
  baslik: string;
  k: string[];
  sutun: string[];
  satir: string[][];
}
export interface CuNot {
  m: string;
  k: string;
}
export interface CuBolum {
  id: string;
  ad: string;
  kisa: string;
  tablolar: CuTablo[];
  notlar: CuNot[];
}

const DOSYALAR = import.meta.glob('../../data/patoloji_checkup/[0-9][0-9]-*.json', { eager: true, import: 'default' }) as Record<string, CuBolum>;

export const BOLUMLER: CuBolum[] = Object.keys(DOSYALAR).sort().map((k) => DOSYALAR[k]);

const DERS_AD = dersler as Record<string, string>;

/** Drive'daki güncel ders sırası: dosya adı numarası ile gerçek ders sırası farklı olanlar (26b = 27. ders, 39 = 29. ders) */
const SIRA: Record<string, string> = { '26b': '27', '39': '29' };

/** "08" → "Ders 8 · Enflamasyonun Kimyasal Mediyatörleri" */
export const dersAdi = (kod: string) => {
  const ad = (DERS_AD[kod] || '').replace(/^\s*\d+\s*\)\s*/, '').trim();
  const no = SIRA[kod] || String(Number.parseInt(kod, 10));
  return ad ? `Ders ${no} · ${ad}` : `Ders ${no}`;
};

/** ["08:20","08:21","07:33"] → [{kod:"08", ad, slaytlar:[20,21]}, {kod:"07", …}] (ilk geliş sırası korunur) */
export function kaynakGrupla(k: string[]) {
  const m = new Map<string, number[]>();
  for (const x of k) {
    const [kod, s] = x.split(':');
    if (!m.has(kod)) m.set(kod, []);
    const n = Number(s);
    if (!m.get(kod)!.includes(n)) m.get(kod)!.push(n);
  }
  return [...m.entries()].map(([kod, sl]) => ({ kod, ad: dersAdi(kod), slaytlar: sl.sort((a, b) => a - b) }));
}

/** Türkçe büyük/küçük harf ve aksan katlamalı arama anahtarı */
export const katla = (s: string) =>
  s
    .toLocaleLowerCase('tr')
    .replace(/[ıi̇]/g, 'i')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[₀-₉]/g, (c) => String(c.charCodeAt(0) - 0x2080))
    .replace(/[⁺⁻]/g, '');

export const TOPLAM = BOLUMLER.reduce(
  (a, b) => ({ tablo: a.tablo + b.tablolar.length, satir: a.satir + b.tablolar.reduce((x, t) => x + t.satir.length, 0), not: a.not + b.notlar.length }),
  { tablo: 0, satir: 0, not: 0 },
);
