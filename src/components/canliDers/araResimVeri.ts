// Sesli ders "ara resim" (mekanizma resmi) katmanı — veri (kullanıcı kararı 2026-11-04; kurallar docs/ARA_RESIM_KURALLARI.md).
// Veri: src/data/ara_resim/<ders key>.json (küçük, derlemeye gömülür); SVG'ler statik: public/ara_resim/<key>/<svg>.
// Gösterim CdAraResim.tsx, dışa aktarım canliDersDisaAktar.ts (resim bağlı paragraf aralığının sonuna), çevrimdışı canliDersCevrimdisi.ts.
export interface AraResim {
  id: string; baslik: string; aciklama: string; adimlar?: string[];
  svg: string;
  /** isteğe bağlı Lottie animasyonu (public/ara_resim/<key>/<ad>.json); svg her zaman durağan yedek + dışa aktarım */
  lottie?: string;
  paragraf: number; bitis?: number; kaynak?: number[];
  /** yükleyicinin eklediği: verinin ders anahtarı (SVG klasörü) */
  dersKey?: string;
}
export interface AraResimDers { key: string; resimler: AraResim[] }

const VERI = import.meta.glob('../../data/ara_resim/*.json', { eager: true, import: 'default' }) as Record<string, AraResimDers>;
const kisaKey = (k: string) => /^k\d-\d{2}/.exec(k)?.[0] || k;
const BOS: AraResim[] = [];

/** Dersin ara resimleri, paragraf sırasıyla (yoksa boş dizi) */
const bellek = new Map<string, AraResim[]>();
export function araResimleri(key: string | null | undefined): AraResim[] {
  if (!key) return BOS;
  const b = bellek.get(key);
  if (b) return b;
  const tum = Object.values(VERI);
  const d = tum.find((x) => x?.key === key) || tum.find((x) => x?.key && kisaKey(x.key) === kisaKey(key) && kisaKey(key) !== key);
  const l = d?.resimler?.length ? d.resimler.map((r) => ({ ...r, dersKey: d.key })).sort((a, b) => a.paragraf - b.paragraf) : BOS;
  bellek.set(key, l);
  return l;
}
export const araResimBitis = (r: AraResim) => r.bitis ?? r.paragraf;
/** SVG'nin site içi yolu (kök göreli) */
export const araResimYolu = (r: AraResim) => `/ara_resim/${encodeURIComponent(r.dersKey || '')}/${encodeURIComponent(r.svg)}`;
/** Etkin paragrafın resmi */
export const araResimBul = (liste: AraResim[], aktif: number) => liste.find((r) => aktif >= r.paragraf && aktif <= araResimBitis(r)) || null;
export const araResimLottieYolu = (r: AraResim) => r.lottie ? `/ara_resim/${encodeURIComponent(r.dersKey || '')}/${encodeURIComponent(r.lottie)}` : null;
