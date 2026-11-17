/** Dersin sesli soru çözücüsü: ders başlığı ↔ src/data/k<N>*_cozucu/index.json eşlemesi → /soru-cozucu?brans=&ders=&coz=1 */
const IZ = import.meta.glob('../../data/k*_cozucu/index.json', { eager: true, import: 'default' }) as Record<string, { dersler?: { kod: string; baslik: string; soru?: number; madde?: number }[] }>;
// Ders kayıt defteri (kimlik → kod). Çözücü kodu defter koduyla aynıdır (2r01, 2f05…); başlıklar ise sık farklıdır
// ("Opoid…" ≠ "Opioid…") — yalnız başlıkla eşleme 15 Kurul 2 dersinde çözücü bağlantısını düşürüyordu (H608, 2026-11-17).
const DEFTER = import.meta.glob('../../data/dersler/k*.json', { eager: true, import: 'default' }) as Record<string, { dersler?: { id: string; kod?: string }[] }>;
const KOD = new Map<string, string>();
for (const d of Object.values(DEFTER)) for (const x of d.dersler || []) if (x.id && x.kod) KOD.set(x.id, x.kod);
const kisaKey = (k: string) => /^k\d-\d{2}/.exec(k)?.[0] || k;
const nz = (s: string) => (s || '').toLocaleLowerCase('tr').replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
export interface DersCozucu { url: string; soru: number }
/** hoca: 'ara' → ders içi "hocanın sorabileceği" sorular (k<N>hocaara) · true → hocanın üslubunda sorular çözücüsü (branş adı "…hoca" ile biter; k2patolojihoca), false → normal çözücü */
const bul = (baslik: string | undefined, hoca: boolean | 'ara', key?: string): DersCozucu | null => {
  const b = nz(baslik || '');
  const kod = key ? KOD.get(kisaKey(key)) : undefined;
  if (!b && !kod) return null;
  // 1) defter koduyla (kesin; bölünmüş çözücüde ilk parça: 2b01 → 2b01-1), 2) başlıkla (eski davranış)
  for (const tur of ['kod', 'baslik'] as const) {
    if (tur === 'kod' ? !kod : !b) continue;
    for (const [yol, d] of Object.entries(IZ)) {
      const brans = yol.match(/data\/(k[^/]*)_cozucu\//)?.[1];
      // k<N>hocaara: ders içi ara sorular (dersAraCozucu), normal/hoca çözücüsüne karışmaz
      if (!brans || brans.endsWith('hocaara') !== (hoca === 'ara') || (hoca !== 'ara' && brans.endsWith('hoca') !== hoca)) continue;
      const x = tur === 'kod'
        ? d.dersler?.find((y) => y.kod === kod) || d.dersler?.find((y) => y.kod.startsWith(`${kod}-`))
        : d.dersler?.find((y) => nz(y.baslik) === b);
      if (x) return { url: `/soru-cozucu?brans=${brans}&ders=${x.kod}&coz=1`, soru: x.soru ?? x.madde ?? 0 };
    }
  }
  return null;
};
export const dersCozucu = (baslik?: string, key?: string): DersCozucu | null => bul(baslik, false, key);
export const dersHocaCozucu = (baslik?: string, key?: string): DersCozucu | null => bul(baslik, true, key);
export const dersAraCozucu = (baslik?: string, key?: string): DersCozucu | null => bul(baslik, 'ara', key);
