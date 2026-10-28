import { useEffect, useMemo, useState } from 'react';
import { pathFor } from '../../router';
import { cdKonumListesi, cdListeGetir, type CdListeDers } from '../canliDers/canliDersStore';
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
  const konum = useMemo(() => new Map(cdKonumListesi().map((k) => [k.key, k])), []);
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

export const dersAdi = (d: Pick<CdListeDers, 'no' | 'baslik' | 'parca'>) => `${d.no}. ${d.baslik}${d.parca ? ` · Part ${d.parca}` : ''}`;

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
export const dersSirala = (ds: CdListeDers[]) => ds.slice().sort((a, b) => noSayi(a) - noSayi(b) || (a.parca ?? 0) - (b.parca ?? 0) || (a.sira ?? 0) - (b.sira ?? 0));
