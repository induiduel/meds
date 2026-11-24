import { useCdKonumSurum } from '../canliDers/CdIlerlemeTemizle';
import { useEffect, useMemo, useState } from 'react';
import { pathFor } from '../../router';
import { cdKonumListesi, cdListeGetir, cdSurumler, type CdListeDers, type CdSurum } from '../canliDers/canliDersStore';
import { cdBransKisa, cdBransSlug, cdTekSurum } from '../canliDers/canliDersKategori';
import { bittiMi, sesliKonuId, useTakip } from '../../services/calismaTakip';
import { kurulKimlikten } from '../kurul/KurulSuzgec';
import { icerikGizli, useSiteAyar } from '../../services/siteAyar';

/**
 * v15 Ders çalış sayfalarının (merkez, branş, ders ayrıntısı) ortak verisi: sesli ders listesi (sunucu ya da cihaz),
 * kaldığın yer kayıtları ve "bitti" işaretleri. Uydurma sayı yok: veri yoksa alan boş kalır.
 */
export type DersListeDurum = { dersler: CdListeDers[] | null; hata: string | null; /** sürümler dahil (V2 ayrıntı sayfası için) */ hepsi?: CdListeDers[] };

/** Son Prova partları ve blok özetleri ders değildir; V2/V3 ayrı ders sayılmaz */
export function useDersListesi(donem: '2026-2027' | '2025-2026' = '2026-2027'): DersListeDurum {
  const [d, setD] = useState<DersListeDurum>({ dersler: null, hata: null });
  useEffect(() => {
    let canli = true;
    setD({ dersler: null, hata: null });
    cdListeGetir(false, donem).then(
      (ds) => {
        if (!canli) return;
        const temiz = ds.filter((x) => !/-son-prova-|-blok-ozet-/.test(x.key));
        const ek = new Map<string, string[]>();
        for (const x of temiz) if (/-v[23]$/.test(x.key)) ek.set(x.key.slice(0, -3), [...(ek.get(x.key.slice(0, -3)) || []), x.key].sort());
        setD({ dersler: cdTekSurum(temiz).map((x) => (ek.has(x.key) ? { ...x, surumlar: ek.get(x.key) } : x)), hata: null, hepsi: temiz });
      },
      (e) => canli && setD({ dersler: [], hata: e?.message || 'Ders listesi alınamadı.' }),
    );
    return () => {
      canli = false;
    };
  }, [donem]);
  // Panel görünürlüğü (sesli:<key>, ders:<id>, kurul:<n>): kapalı dersler öğrencinin listesinden kalkar; yönetici hepsini görür
  const ayar = useSiteAyar();
  return useMemo(() => (d.dersler ? { ...d, dersler: d.dersler.filter((x) => !icerikGizli('sesli', x.key)), hepsi: d.hepsi?.filter((x) => !icerikGizli('sesli', x.key)) } : d), [d, ayar]);
}

export const dersKurulu = (d: Pick<CdListeDers, 'kurul' | 'key'>) => d.kurul ?? kurulKimlikten(d.key) ?? 1;
export const dersBransi = (d: Pick<CdListeDers, 'brans'>) => d.brans || 'Diğer';

export interface Ilerleme {
  pct: number;
  bitti: boolean;
  /** kaldığın yer (sn); yoksa null */
  t: number | null;
  sure: number;
  at: number;
  /** bitmiş derse yeniden başlandı (bitişten sonra kaldığın yer kaydı var) */
  tekrar: boolean;
  /** tamamlanan tekrar turu sayısı */
  tur: number;
}

/** Ders başına ilerleme: "bitti" işareti %100, yoksa kayıtlı konum / ses süresi */
export function useIlerleme() {
  const takip = useTakip();
  const konumSurum = useCdKonumSurum();
  const konum = useMemo(() => new Map(cdKonumListesi().map((k) => [k.key, k])), [konumSurum]);
  return (d: CdListeDers): Ilerleme => {
    const kayit = takip.k[`sesli:${sesliKonuId(d.key)}`];
    const bitti = bittiMi(kayit);
    const k = konum.get(d.key);
    const sure = d.varsayilan?.sureSn || 0;
    const t = k ? k.t : null;
    const bittiAt = kayit?.bittiAt ? Date.parse(kayit.bittiAt) || 0 : 0;
    // bitişte konum silinir; bitmiş derste konum varsa (bitişten sonra kaydedildiyse) tekrar sürüyor
    const tekrar = bitti && k != null && k.at > bittiAt;
    const kismi = t != null && sure > 0 ? Math.min(99, Math.round((t / sure) * 100)) : 0;
    const pct = bitti && !tekrar ? 100 : kismi;
    return { pct, bitti, t, sure, at: k?.at || 0, tekrar, tur: kayit?.tur || 0 };
  };
}

export const sureDk = (sn: number) => (sn > 0 ? `${Math.max(1, Math.round(sn / 60))} dk` : '');
export const saatYaz = (sn: number) => {
  const s = Math.max(0, Math.floor(sn));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const ss = String(s % 60).padStart(2, '0');
  return h ? `${h}:${String(m).padStart(2, '0')}:${ss}` : `${String(m).padStart(2, '0')}:${ss}`;
};

/** "PROF. DR. HİKMET KELEŞ" → "Prof. Dr. Hikmet Keleş" */
export const hocaYaz = (h?: string) =>
  (h || '')
    .trim()
    .toLocaleLowerCase('tr-TR')
    .split(/\s+/)
    .map((w) => w.charAt(0).toLocaleUpperCase('tr-TR') + w.slice(1))
    .join(' ');

export const dersAdi = (d: Pick<CdListeDers, 'no' | 'baslik' | 'parca'>, no?: number) => `${no ?? d.no}. ${d.baslik}${d.parca ? ` · Part ${d.parca}` : ''}`;

/** Görünen adresler */
export const bransYolu = (kurul: number, brans: string) => `/dersler/canliders/kurul${kurul}/${cdBransSlug(brans)}`;
export const dersYolu = (key: string) => pathFor('ders_detay', key);
export const merkezYolu = (kurul: number) => `/dersler/kurul${kurul}`;

/** Kuruldaki branşlar: ders sayısına göre (çoktan aza) */
export function kurulBranslari(ds: CdListeDers[], kurul: number) {
  const m = new Map<string, CdListeDers[]>();
  for (const d of ds) {
    if (dersKurulu(d) !== kurul) continue;
    const b = dersBransi(d);
    (m.get(b) || m.set(b, []).get(b)!).push(d);
  }
  return [...m.entries()]
    .map(([ad, dersler]) => ({ ad, kisa: cdBransKisa(ad), slug: cdBransSlug(ad), dersler }))
    .sort((a, b) => (a.ad === 'Diğer' ? 1 : 0) - (b.ad === 'Diğer' ? 1 : 0) || b.dersler.length - a.dersler.length || a.ad.localeCompare(b.ad, 'tr'));
}

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

/** Dersin V1/V2/V3 sürümleri (ders sürümü …-v2 + adlandırılmış ses sürümleri); ana ders ya da sürüm anahtarından çağrılabilir */
export function dersSurumleri(key: string, d: DersListeDurum): CdSurum[] {
  const ana = key.replace(/-v[23]$/, '');
  const hepsi = d.hepsi || d.dersler || [];
  const bas = (d.dersler || []).find((x) => x.key === ana) || hepsi.find((x) => x.key === ana);
  if (!bas) return [];
  const dersler = [bas, ...(bas.surumlar || []).map((k) => hepsi.find((x) => x.key === k)).filter((x): x is CdListeDers => !!x)];
  return cdSurumler(dersler);
}
