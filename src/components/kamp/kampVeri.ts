/**
 * Kurul kampı ortak verisi: ders kayıt defteri (data/dersler/kN.json), branşlar (branslar.json), kamp dosyaları
 * (data/kamp/k<N>/<brans>.json, gece otomasyon/kamp_zinciri.py üretir; şema scripts/kamp/TALIMAT_KAMP.md) ve
 * kaynak etiketi ("2f01:12" → "Ders 7 · Genel Anestezik İlaçlar · s.12").
 */
import { getCustomApiUrl } from '../../services/api';
import bransRaw from '../../data/dersler/branslar.json';
import { DECK_CATALOG } from '../../data/deckStore';

export interface KampAnlatim { id: string; baslik: string; metin: string; k?: string[]; puan: number; tuyo?: string | null }
export interface KampKalipSatir { s: string; t: string; k?: string; h?: number }
export interface KampKalip { id: string; baslik: string; soru: string; sutun: [string, string]; satir: KampKalipSatir[] }
export interface KampSoru { id: string; kok: string; secenekler: Record<string, string>; dogru: string; aciklama: Record<string, string>; k?: string[]; tuyo?: string | null }
export interface Kamp {
  surum: number; kurul: number; brans: string; baslik: string; kisa?: string;
  tuyolar: { id: string; metin: string }[]; anlatim: KampAnlatim[]; kalipler: KampKalip[]; deneme: KampSoru[];
  ses?: Record<string, string>;
}
export interface Ders { id: string; kod: string; kurul: number; brans: string; konu: string }
export interface Brans { harf: string; ad: string; slug: string; kisa: string }

const BRANSLAR: Brans[] = (bransRaw as unknown as { branslar: Brans[] }).branslar;
const DERS_DOSYA = import.meta.glob('../../data/dersler/k*.json', { eager: true, import: 'default' }) as Record<string, { dersler?: Ders[] }>;
const KAMP_DOSYA = import.meta.glob('../../data/kamp/k*/*.json', { import: 'default' }) as Record<string, () => Promise<unknown>>;

const DERSLER: Ders[] = Object.values(DERS_DOSYA).flatMap((d) => d.dersler || []);
const KOD_DERS = new Map(DERSLER.map((d) => [d.kod, d]));

/** Branş adı (ders defterindeki yazım) → branş kaydı */
export const bransBul = (adVeyaSlug: string): Brans | undefined =>
  BRANSLAR.find((b) => b.slug === adVeyaSlug || b.ad === adVeyaSlug || b.kisa === adVeyaSlug);
export const bransAdi = (slug: string) => bransBul(slug)?.ad || slug;
export const bransKisa = (slug: string) => bransBul(slug)?.kisa || slug;

export const kurulDersleri = (kurul: number) => DERSLER.filter((d) => d.kurul === kurul);

/** Kurulun ders defterindeki branşlar (ders defteri yoksa bütün branşlar); slug tekil */
export function kurulBranslari(kurul: number): Brans[] {
  const D = kurulDersleri(kurul);
  const liste = D.length ? D.map((d) => bransBul(d.brans)).filter((b): b is Brans => !!b) : BRANSLAR;
  const gor = new Set<string>();
  return liste.filter((b) => (gor.has(b.slug) ? false : (gor.add(b.slug), true)));
}

export const dersNo = (d: Ders) => Number(d.id.split('-')[1]) || 0;

/** "2f01:12" → "Ders 7 · Genel Anestezik İlaçlar · s.12" (bilinmeyen kod olduğu gibi kalır) */
export function kaynakYaz(k: string): string {
  const [kod, sayfa] = String(k || '').split(':');
  const d = KOD_DERS.get(kod);
  const s = sayfa ? ` · s.${sayfa}` : '';
  return d ? `Ders ${dersNo(d)} · ${d.konu}${s}` : `${kod}${s}`;
}

/**
 * Kaynak bağlantısı: "2f01:12" → ders defteri (k2-07) → o dersin Öğren destesi (`k<N>p-<ders_id>-…`, sürümlüyse en
 * yeni sürüm) varsa `/ogren/<deckId>` (uygulama içi), yoksa sunucu kısa bağlantısı `/k/<ders_id>` (tam yükleme).
 * Öğren'de PDF sayfasına giden adres parametresi olmadığından sayfa numarası yalnız etikette kalır.
 * DECK_CATALOG tembel yüklenir (deckStore.loadDeckCatalog); yüklenmeden çağrılırsa kısa bağlantı döner.
 */
export function kaynakHedef(k: string): { url: string; ic: boolean } | null {
  const d = KOD_DERS.get(String(k || '').split(':')[0]);
  if (!d) return null;
  const on = `k${d.kurul}p-${d.id}-`;
  const L = DECK_CATALOG.filter((x) => x.id.startsWith(on));
  if (L.length) {
    // Kitaplıktaki sıra (InteractiveDeckView.versionsOf): versionLabel sayısal artan, son öğe en yeni sürüm
    const en = [...L].sort((a, b) => String(a.versionLabel || 'V1').localeCompare(String(b.versionLabel || 'V1'), 'tr', { numeric: true })).pop()!;
    return { url: `/ogren/${en.id}`, ic: true };
  }
  return { url: `/k/${d.id}`, ic: false };
}

/** Kurulun kamp dosyaları (yalnız yol; içerik tembel yüklenir) */
export function kurulKampYollari(kurul: number): { brans: string; yukle: () => Promise<Kamp> }[] {
  return Object.entries(KAMP_DOSYA)
    .map(([yol, yukle]) => ({ m: /\/k(\d+)\/([a-z0-9]+)\.json$/.exec(yol), yukle }))
    .filter((x) => x.m && Number(x.m[1]) === kurul)
    .map((x) => ({ brans: x.m![2], yukle: x.yukle as () => Promise<Kamp> }));
}

export const kampSesUrl = (kamp: Kamp, anahtar: string): string | null => {
  const d = kamp.ses?.[anahtar];
  return d ? `${getCustomApiUrl()}/api/kamp/ses/${kamp.kurul}/${kamp.brans}/${d}` : null;
};
