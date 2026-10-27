/** Dersin sesli soru çözücüsü: ders başlığı ↔ src/data/k<N>*_cozucu/index.json eşlemesi → /soru-cozucu?brans=&ders=&coz=1 */
const IZ = import.meta.glob('../../data/k*_cozucu/index.json', { eager: true, import: 'default' }) as Record<string, { dersler?: { kod: string; baslik: string; soru?: number; madde?: number }[] }>;
const nz = (s: string) => (s || '').toLocaleLowerCase('tr').replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
export interface DersCozucu { url: string; soru: number }
export const dersCozucu = (baslik?: string): DersCozucu | null => {
  const b = nz(baslik || '');
  if (!b) return null;
  for (const [yol, d] of Object.entries(IZ)) {
    const brans = yol.match(/data\/(k[^/]*)_cozucu\//)?.[1];
    const x = d.dersler?.find((y) => nz(y.baslik) === b);
    if (brans && x) return { url: `/soru-cozucu?brans=${brans}&ders=${x.kod}&coz=1`, soru: x.soru ?? x.madde ?? 0 };
  }
  return null;
};
