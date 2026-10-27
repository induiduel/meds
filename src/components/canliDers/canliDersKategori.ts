/**
 * Canlı ders listesi · ders (branş) kategorileri. Branş ve branş içi numara sunucudan gelir
 * (canliDers.ts › bransBilgisi: slayt PDF'inin Drive klasörü + dosya numarası). Her grup kendi numarasına göre sıralı.
 */
import type { CdListeDers } from './canliDersStore';
import type { Brans } from '../spots/brans';
import { bransAdresi } from '../../siteHaritasi';

export interface CdKategori { id: string; ad: string; kisa: string; alt: string }

const KISA: Record<string, string> = {
  'Tıbbi Patoloji': 'Patoloji',
  'Tıbbi Genetik': 'Genetik',
  'Tıbbi Farmakoloji': 'Farmakoloji',
  'Enfeksiyon Hastalıkları': 'Enfeksiyon',
  'Kadın Hastalıkları ve Doğum': 'Kadın Doğum',
};
/** Sesli ders branş adı → soru çözücü / en önemliler branşı (ilgili konu eşlemesi: branş + branş içi numara) */
export const CD_SPOT_BRANS: Record<string, Brans> = {
  'Tıbbi Patoloji': 'patoloji',
  'Enfeksiyon Hastalıkları': 'enfeksiyon',
  'Üroloji': 'uroloji',
  'Tıbbi Genetik': 'genetik',
  'Halk Sağlığı': 'halksagligi',
  'Kadın Hastalıkları ve Doğum': 'kadindogum',
  'Tıbbi Farmakoloji': 'farmakoloji',
};
const katla = (s: string) => s.toLocaleLowerCase('tr-TR').replace(/ı/g, 'i').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
/** Sesli ders branş adının adres adı (Tıbbi Genetik → tbg; Kurul 2+ branşları adından: Nöroloji → noroloji) */
export const cdBransSlug = (ad: string) => {
  const b = CD_SPOT_BRANS[ad];
  return b ? bransAdresi(b).slug : katla(ad).replace(/^tibbi /, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
};
export const cdBransKisa = (brans: string) => KISA[brans] || brans.replace(/^Tıbbi\s+/, '');
const bransAdi = (d: CdListeDers) => d.brans || 'Diğer';
const noSayi = (d: CdListeDers) => Number(d.no) || 9999;

/** Aynı dersin V2/V3'ü (`…-v2`, `…-v3`) V1'i varsa ayrı ders sayılmaz (Bitirdiklerim, sınav planı) */
export const cdTekSurum = <T extends { key: string }>(ds: T[]): T[] => {
  const ks = new Set(ds.map((d) => d.key));
  return ds.filter((d) => !(/-v[23]$/.test(d.key) && ks.has(d.key.slice(0, -3))));
};

/** Grup başlığındaki sayı: Part 1/2 tek konu (PDF) sayılır */
export const cdKonuSayisi = (ds: CdListeDers[]) => new Set(ds.map((d) => `${d.brans}|${d.no}`)).size;

export const cdParca = (d: { parca?: number }) => (d.parca ? `Part ${d.parca}` : '');
/** Liste satırı dışında (oynatıcı, devam kartı, listem) gösterilecek ad: "Patoloji 30 · Part 2" */
export const cdDersEtiketi = (d: { no?: string | number; brans?: string; parca?: number }) =>
  (d.brans && d.brans !== 'Diğer' ? `${cdBransKisa(d.brans)} ${d.no}` : d.no ? String(d.no) : '') + (d.parca ? ` · ${cdParca(d)}` : '');

/** Boş gruplar düşer; branşlar ders sayısına göre (çoktan aza), her grupta branş içi numaraya göre sıralı.
 *  Birden çok kurul varsa her kurulun branşı ayrı grup olur. */
export function cdKategoriGrupla(ds: CdListeDers[]): { kat: CdKategori; dersler: CdListeDers[] }[] {
  const cokKurul = new Set(ds.map((d) => d.kurul || 0)).size > 1;
  const m = new Map<string, { kat: CdKategori; dersler: CdListeDers[] }>();
  for (const d of ds) {
    // Son Prova partları normal ders değil: branşlarına karışmaz, kendi kategorisinde (en sonda) durur
    const ad = /-son-prova-/.test(d.key) ? 'Son Prova' : bransAdi(d);
    const id = `${cokKurul ? `k${d.kurul || 0}-` : ''}${ad}`;
    let g = m.get(id);
    if (!g) m.set(id, (g = { kat: { id, ad, kisa: cdBransKisa(ad), alt: cokKurul && d.kurul ? `Kurul ${d.kurul}` : '' }, dersler: [] }));
    g.dersler.push(d);
  }
  const diger = (g: { kat: CdKategori }) => (g.kat.ad === 'Son Prova' ? 2 : g.kat.ad === 'Diğer' ? 1 : 0);
  return [...m.values()]
    .map((g) => ({ ...g, dersler: g.dersler.sort((a, b) => (a.listeNo ?? noSayi(a)) - (b.listeNo ?? noSayi(b)) || (a.parca ?? 0) - (b.parca ?? 0) || (a.sira ?? 0) - (b.sira ?? 0)) }))
    .sort((a, b) => diger(a) - diger(b) || (a.kat.alt || '').localeCompare(b.kat.alt || '', 'tr')
      || b.dersler.length - a.dersler.length || a.kat.ad.localeCompare(b.kat.ad, 'tr'));
}
