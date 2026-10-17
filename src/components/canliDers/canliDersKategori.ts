/**
 * Canlı ders listesi · ders (branş) kategorileri. Branş ve branş içi numara sunucudan gelir
 * (canliDers.ts › bransBilgisi: slayt PDF'inin Drive klasörü + dosya numarası). Her grup kendi numarasına göre sıralı.
 */
import type { CdListeDers } from './canliDersStore';

export interface CdKategori { id: string; ad: string; kisa: string; alt: string }

const KISA: Record<string, string> = {
  'Tıbbi Patoloji': 'Patoloji',
  'Tıbbi Genetik': 'Genetik',
  'Tıbbi Farmakoloji': 'Farmakoloji',
  'Enfeksiyon Hastalıkları': 'Enfeksiyon',
  'Kadın Hastalıkları ve Doğum': 'Kadın Doğum',
};
export const cdBransKisa = (brans: string) => KISA[brans] || brans.replace(/^Tıbbi\s+/, '');
const bransAdi = (d: CdListeDers) => d.brans || 'Diğer';
const noSayi = (d: CdListeDers) => Number(d.no) || 9999;

/** Liste satırı dışında (oynatıcı, devam kartı, listem) gösterilecek ad: "Patoloji 16 · Başlık" */
export const cdDersEtiketi = (d: { no?: string | number; brans?: string }) =>
  d.brans && d.brans !== 'Diğer' ? `${cdBransKisa(d.brans)} ${d.no}` : d.no ? String(d.no) : '';

/** Boş gruplar düşer; branşlar ders sayısına göre (çoktan aza), her grupta branş içi numaraya göre sıralı.
 *  Birden çok kurul varsa her kurulun branşı ayrı grup olur. */
export function cdKategoriGrupla(ds: CdListeDers[]): { kat: CdKategori; dersler: CdListeDers[] }[] {
  const cokKurul = new Set(ds.map((d) => d.kurul || 0)).size > 1;
  const m = new Map<string, { kat: CdKategori; dersler: CdListeDers[] }>();
  for (const d of ds) {
    const ad = bransAdi(d);
    const id = `${cokKurul ? `k${d.kurul || 0}-` : ''}${ad}`;
    let g = m.get(id);
    if (!g) m.set(id, (g = { kat: { id, ad, kisa: cdBransKisa(ad), alt: cokKurul && d.kurul ? `Kurul ${d.kurul}` : '' }, dersler: [] }));
    g.dersler.push(d);
  }
  const diger = (g: { kat: CdKategori }) => (g.kat.ad === 'Diğer' ? 1 : 0);
  return [...m.values()]
    .map((g) => ({ ...g, dersler: g.dersler.sort((a, b) => noSayi(a) - noSayi(b) || (a.sira ?? 0) - (b.sira ?? 0)) }))
    .sort((a, b) => diger(a) - diger(b) || (a.kat.alt || '').localeCompare(b.kat.alt || '', 'tr')
      || b.dersler.length - a.dersler.length || a.kat.ad.localeCompare(b.kat.ad, 'tr'));
}
