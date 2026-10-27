import { useEffect, useMemo, useState } from 'react';
import { pathFor } from '../../router';
import { cdKonumListesi, cdListeGetir, type CdListeDers } from '../canliDers/canliDersStore';
import { cdBransKisa, cdBransSlug, cdTekSurum } from '../canliDers/canliDersKategori';
import { bittiMi, sesliKonuId, useTakip } from '../../services/calismaTakip';
import { kurulKimlikten } from '../kurul/KurulSuzgec';

/**
 * v15 Ders çalış sayfalarının (merkez, branş, ders ayrıntısı) ortak verisi: sesli ders listesi (sunucu ya da cihaz),
 * kaldığın yer kayıtları ve "bitti" işaretleri. Uydurma sayı yok: veri yoksa alan boş kalır.
 */
export type DersListeDurum = { dersler: CdListeDers[] | null; hata: string | null };

/** Son Prova partları ve blok özetleri ders değildir; V2/V3 ayrı ders sayılmaz */
export function useDersListesi(): DersListeDurum {
  const [d, setD] = useState<DersListeDurum>({ dersler: null, hata: null });
  useEffect(() => {
    let canli = true;
    cdListeGetir().then(
      (ds) => canli && setD({ dersler: cdTekSurum(ds.filter((x) => !/-son-prova-|-blok-ozet-/.test(x.key))), hata: null }),
      (e) => canli && setD({ dersler: [], hata: e?.message || 'Ders listesi alınamadı.' }),
    );
    return () => {
      canli = false;
    };
  }, []);
  return d;
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
}

/** Ders başına ilerleme: "bitti" işareti %100, yoksa kayıtlı konum / ses süresi */
export function useIlerleme() {
  const takip = useTakip();
  const konum = useMemo(() => new Map(cdKonumListesi().map((k) => [k.key, k])), []);
  return (d: CdListeDers): Ilerleme => {
    const bitti = bittiMi(takip.k[`sesli:${sesliKonuId(d.key)}`]);
    const k = konum.get(d.key);
    const sure = d.varsayilan?.sureSn || 0;
    const t = k ? k.t : null;
    const pct = bitti ? 100 : t != null && sure > 0 ? Math.min(99, Math.round((t / sure) * 100)) : 0;
    return { pct, bitti, t, sure, at: k?.at || 0 };
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
