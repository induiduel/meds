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

/** Aynı dersin V2/V3'ü (`…-v2`, `…-v3`) V1'i varsa ayrı ders sayılmaz (Bitirdiklerim, sınav planı) */
export const cdTekSurum = <T extends { key: string }>(ds: T[]): T[] => {
  const ks = new Set(ds.map((d) => d.key));
  return ds.filter((d) => !(/-v[23]$/.test(d.key) && ks.has(d.key.slice(0, -3))));
};

/** Grup başlığındaki sayı: Part 1/2 tek konu (PDF) sayılır */
export const cdKonuSayisi = (ds: CdListeDers[]) => new Set(ds.map((d) => `${d.brans}|${d.no}`)).size;

export const cdParca = (d: { parca?: number }) => (d.parca ? `Part ${d.parca}` : '');
/** Liste satırı dışında (oynatıcı, devam kartı, listem) gösterilecek ad: "Patoloji 30 · Part 2" */
export const cdDersEtiketi = (d: { key?: string; no?: string | number; brans?: string; parca?: number }) =>
  (d.brans && d.brans !== 'Diğer' ? `${cdBransKisa(d.brans)} ${cdNo(d)}` : d.no ? String(cdNo(d)) : '') + (d.parca ? ` · ${cdParca(d)}` : '');

const noSayi = (d: CdListeDers) => d.listeNo ?? (Number(d.no) || 9999);
/** Liste sırası: drive = branş içi numara (Drive dosya adı / ders defteri kodu), program = ders programındaki sıra
 *  (anahtar numarası k2-NN), eklenme = siteye eklenme anı (ilk ses). Numara sabit değil, seçilen sıradan türetilir. */
export type DersSiraTur = 'drive' | 'program' | 'eklenme';
const programNo = (d: CdListeDers) => Number(/^(?:y25-)?k\d+-(\d+)/.exec(d.key)?.[1]) || 9999;
/** Modül/Son Prova/Blok özet gibi numarasız dersler sona düşer ve numara almaz */
const numarasiz = (d: CdListeDers) => !Number.isFinite(Number(d.no));
const surumsuz = (key: string) => key.replace(/-v\d+$/, '');
export const dersSirala = (ds: CdListeDers[], tur: DersSiraTur = 'drive') => ds.slice().sort((a, b) =>
  Number(numarasiz(a)) - Number(numarasiz(b))
  || (tur === 'program' ? programNo(a) - programNo(b) : tur === 'eklenme' ? (a.eklendi ?? 9e15) - (b.eklendi ?? 9e15) : 0)
  || noSayi(a) - noSayi(b) || (a.parca ?? 0) - (b.parca ?? 0) || (a.sira ?? 0) - (b.sira ?? 0));
/** Seçilen sıraya göre boşluksuz 1..N numara. V2/V3 V1'le, Part 1/2 ve aynı PDF'e hizalı dersler aynı numarayı paylaşır. */
export function dersNumaralari(ds: CdListeDers[], tur: DersSiraTur = 'drive'): Map<string, number> {
  const m = new Map<string, number>();
  const grup = new Map<string, number>();
  for (const d of dersSirala(ds, tur)) {
    if (numarasiz(d)) continue;
    // Drive sırasında aynı PDF numarası tek numara (asıl dersi gizli V2/V3 de kaydırmasın); diğerlerinde ders (sürümsüz anahtar)
    const g = tur === 'drive' || d.parca ? `pdf:${d.no}` : surumsuz(d.key);
    if (!grup.has(g)) grup.set(g, grup.size + 1);
    m.set(d.key, grup.get(g)!);
  }
  return m;
}

/* ---- Dinamik numara: listede seçilen sıra her yerde (oynatıcı, branş sayfası, devam kartı) aynı numarayı verir ---- */
const SIRA_ANAHTAR = 'sl15-sira';
const TURLER: DersSiraTur[] = ['drive', 'program', 'eklenme'];
/** Liste sıralama seçimi (son/kısa gibi yalnız yeniden dizen seçimler de saklanır; numara için drive'a düşer) */
export function cdSiraSecimi(): string | null {
  try { return localStorage.getItem(SIRA_ANAHTAR); } catch { return null; }
}
export function cdSiraKaydet(v: string) {
  try { localStorage.setItem(SIRA_ANAHTAR, v); } catch { /* depolama kapalı */ }
  numaraHesapla();
}
export const cdSiraTur = (): DersSiraTur => {
  const v = cdSiraSecimi();
  return TURLER.includes(v as DersSiraTur) ? (v as DersSiraTur) : 'drive';
};
let sonListe: CdListeDers[] = [];
let numara = new Map<string, number>();
let numaraSurum = 0;
const dinleyiciler = new Set<() => void>();
/** Numaralar değişince (liste yüklendi / sıra seçildi) yeniden çizim için: useSyncExternalStore(cdNumaraAbone, cdNumaraSurum) */
export const cdNumaraAbone = (f: () => void) => { dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; };
export const cdNumaraSurum = () => numaraSurum;
/** Numara grupları sesli ders listesindeki gruplarla aynı: kurul + branş; Son Prova/Blok özet dışarıda */
function numaraHesapla() {
  const gruplar = new Map<string, CdListeDers[]>();
  for (const d of sonListe) {
    if (/-son-prova-|-blok-ozet-/.test(d.key)) continue;
    const g = `${d.donem || ''}|${d.kurul || 0}|${d.brans || 'Diğer'}`;
    (gruplar.get(g) || gruplar.set(g, []).get(g)!).push(d);
  }
  const tur = cdSiraTur();
  const m = new Map<string, number>();
  for (const ds of gruplar.values()) for (const [k, n] of dersNumaralari(cdTekSurum(ds), tur)) m.set(k, n);
  numara = m;
  numaraSurum++;
  dinleyiciler.forEach((f) => f());
}
/** Liste yüklenince çağrılır (canliDersStore › cdListeGetir) */
export function cdNumaraKaydet(ds: CdListeDers[]) {
  const ks = new Set(ds.map((d) => d.key));
  sonListe = [...sonListe.filter((d) => !ks.has(d.key)), ...ds];
  numaraHesapla();
}
/** Gösterilecek numara: seçilen sıradaki konum; liste henüz yoksa ya da ders numarasızsa sunucu numarası */
export const cdNo = (d: { key?: string; no?: string | number }) =>
  (d.key ? numara.get(d.key) ?? numara.get(surumsuz(d.key)) : undefined) ?? d.no ?? '';

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
