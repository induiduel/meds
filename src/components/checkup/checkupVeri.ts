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
// Kurul 2+: src/data/patoloji_checkup/k<N>/NN-*.json (otomasyon/checkup_zinciri.py üretir; Kurul 1 dosyaları kökte kalır)
const KURUL_DOSYALAR = import.meta.glob('../../data/patoloji_checkup/k[2-6]/[0-9][0-9]-*.json', { eager: true, import: 'default' }) as Record<string, CuBolum>;
const DEFTER = import.meta.glob('../../data/dersler/k[2-6].json', { eager: true, import: 'default' }) as Record<string, { dersler: { id: string; kod: string; konu: string }[] }>;

/** ?kurul=N ve o kurulun Check Up verisi varsa o kurul; yoksa Kurul 1 (varsayılan davranış değişmez) */
const istenen = (() => {
  try { return Number(new URLSearchParams(window.location.search).get('kurul')) || 1; } catch { return 1; }
})();
const kurulDosyalari = Object.keys(KURUL_DOSYALAR).filter((k) => k.includes(`/patoloji_checkup/k${istenen}/`));
export const CHECKUP_KURUL: number = istenen >= 2 && kurulDosyalari.length ? istenen : 1;

export const BOLUMLER: CuBolum[] = CHECKUP_KURUL === 1
  ? Object.keys(DOSYALAR).sort().map((k) => DOSYALAR[k])
  : kurulDosyalari.sort().map((k) => KURUL_DOSYALAR[k]);

const DEFTER_KOD: Record<string, { no: string; konu: string }> = Object.fromEntries(
  Object.values(DEFTER).flatMap((d) => d.dersler.map((x) => [x.kod, { no: String(Number(x.id.split('-')[1])), konu: x.konu }])),
);

const DERS_AD = dersler as Record<string, string>;

/** Drive'daki güncel ders sırası: dosya adı numarası ile gerçek ders sırası farklı olanlar (26b = 27. ders, 39 = 29. ders) */
const SIRA: Record<string, string> = { '26b': '27', '39': '29' };

/** "08" → "Ders 8 · Enflamasyonun Kimyasal Mediyatörleri" */
export const dersAdi = (kod: string) => {
  const k2 = DEFTER_KOD[kod]; // Kurul 2+ kodu (2p03) → ders kayıt defteri
  if (k2) return `Ders ${k2.no} · ${k2.konu}`;
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
