/**
 * Bitirdiklerim — dört modülün ders → konu listesi. Her konu: takip kimliği, ad, beklenen süre (tahmin için),
 * içerikten türetilen tamamlanma, aç / tekrar et eylemleri.
 *
 * Konu kimlikleri (services/calismaTakip): sesli `<ders anahtarı>`, ogren `<versionGroup || deste id>`,
 * cozucu `<branş>/<set kodu>`, onem `<branş>/<ders kodu>`. Sayfalardaki sayaçlar aynı kimlikleri kullanır.
 */
import { navigateTo, pathFor } from '../../router';
import type { TakipModul } from '../../services/calismaTakip';
import { cdListeGetir, cdOynat, cdTercihVaryant } from '../canliDers/canliDersStore';
import { CD_SPOT_BRANS, cdKategoriGrupla, cdParca } from '../canliDers/canliDersKategori';
import { BRANSLAR, type Brans } from '../spots/brans';
import { cozucuDizinYukle, ilerlemeOku, ilerlemeYaz, ozet, setAdi, type CDizin } from '../spots/cozucu/cozucuVeri';
import { dizinYukle as onemDizinYukle, ogrenilenler, type Dizin as OnemDizin } from '../spots/onem/onemVeri';
import { getAsistanSureGruplari } from '../spots/sure/spotsSureVeri';
import { cozucuyaGit, onemeGit } from '../spots/spotsYol';
import { DECK_CATALOG, type DeckCatalogEntry, loadDeckCatalog } from '../../data/deckStore';
import { branchOf, isPublished, stateOf, type Progress } from '../learn/LearnLibrary';
import { ogrenBasaAl, onemAsistanBasaAl } from './basaAl';
import { KURULLAR } from '../../services/kurulTakvimi';
import { bransAdi, kurulKampYollari, type Kamp } from '../kamp/kampVeri';
import { kampAnahtar, kampKaydi, kampOzeti, kampSifirla } from '../kamp/kampIlerleme';
// Katalog tembel yüklenir; bu modül eşzamanlı okuduğundan yüklenirken hazır olmasını bekle.
await loadDeckCatalog().catch(() => undefined);

export interface BdKonu {
  id: string;
  no?: string | number;
  ad: string;
  alt?: string;
  /** içeriğin beklenen süresi (sn) */
  beklenen: number;
  turetilen: boolean;
  /** başka modülden gelen ilgili soru sayısı (sesli derste aynı konunun soru çözücüsü) */
  ekSoru?: number;
  ac: () => void;
  tekrar: () => void;
}
export interface BdDers { id: string; ad: string; konular: BdKonu[] }

/** Soru çözücüde ortalama soru süresi (ses dizininde süre yoksa) */
const SORU_SN = 75;
/** En önemlilerde asistan süresi yoksa madde başına okuma süresi */
const MADDE_SN = 40;
/** Etkileşimli derste adım başına (anlatım + 4–6 etkileşim) */
const ADIM_SN = 75;

const tumBranslar = <T,>(yukle: (b: Brans) => Promise<T>) =>
  Promise.all(BRANSLAR.map((b) => yukle(b.id).then((x) => [b, x] as const).catch(() => [b, null] as const)));

const cozucuDizinleri = () => tumBranslar<CDizin>(cozucuDizinYukle);

/** Sesli ders konusuna bağlı soru çözücü sorularından çözülenler (branş + branş içi numara) */
const ilgiliCozulenler = async (): Promise<Map<string, number>> => {
  const il = ilerlemeOku();
  const m = new Map<string, number>();
  for (const [b, dz] of await cozucuDizinleri()) {
    for (const d of dz?.dersler || []) {
      const k = `${b.id}|${Number(d.no)}`;
      m.set(k, (m.get(k) || 0) + ozet(il[d.kod], d.soru).cozulen);
    }
  }
  return m;
};

/** Son Prova partı (k1-81-son-prova-patoloji-1) → /son-prova/patoloji/1 (CanliDersView.sonProvaYolu ile aynı) */
const sonProvaYolu = (key: string) => {
  const m = /^k\d+-\d+-son-prova-([a-z-]+?)(?:-(\d+))?$/.exec(key);
  return m ? `/son-prova/${m[1].replace(/-/g, '')}/${m[2] || 1}` : null;
};

async function sesliYukle(): Promise<BdDers[]> {
  const [ds, ilgili] = await Promise.all([cdListeGetir(), ilgiliCozulenler().catch(() => new Map<string, number>())]);
  return cdKategoriGrupla(ds).map(({ kat, dersler }) => ({
    id: kat.id,
    ad: kat.ad,
    konular: dersler.map((d) => {
      const v = cdTercihVaryant(d.varyantlar) || d.varsayilan;
      const sb = d.brans ? CD_SPOT_BRANS[d.brans] : undefined;
      // Part 1/2 aynı konunun iki parçası: ilgili sorular yalnız ilk parçada sayılır
      const ek = sb && (d.parca || 1) === 1 ? ilgili.get(`${sb}|${Number(d.no)}`) || 0 : 0;
      const sp = sonProvaYolu(d.key);
      const ac = () => navigateTo(sp || pathFor('canli_ders', d.key));
      return {
        id: d.key,
        no: d.no,
        ad: d.baslik,
        alt: cdParca(d) || undefined,
        beklenen: v?.sureSn || 0,
        turetilen: false,
        ekSoru: ek,
        ac,
        tekrar: () => { if (v) cdOynat(d, v.id, { t: 0 }); ac(); },
      };
    }),
  }));
}

const LEARN_PROGRESS_KEY = 'medsoru_learn_progress_v1';
const learnProgress = (): Progress => {
  try { return JSON.parse(localStorage.getItem(LEARN_PROGRESS_KEY) || '{}') || {}; } catch { return {}; }
};
/** Öğren takip kimliği: sürümlü derste grup kimliği (V1/V2 aynı konu) */
export const ogrenKonuId = (d: { id: string; versionGroup?: string }) => d.versionGroup || d.id;

async function ogrenYukle(): Promise<BdDers[]> {
  const p = learnProgress();
  // Kitaplıktaki gibi: sürüm grubunun en yeni sürümü, yalnız yayımlanmış dersler
  const gruplar = new Map<string, DeckCatalogEntry[]>();
  for (const d of DECK_CATALOG) {
    const g = ogrenKonuId(d);
    gruplar.set(g, [...(gruplar.get(g) || []), d]);
  }
  const dersler = new Map<string, BdKonu[]>();
  for (const [g, l] of gruplar) {
    l.sort((a, b) => String(a.versionLabel || 'V1').localeCompare(String(b.versionLabel || 'V1'), 'tr', { numeric: true }));
    const d = l[l.length - 1];
    if (!isPublished(d) && l.length < 2) continue;
    const ad = branchOf(d);
    const ac = () => navigateTo(`${pathFor('learn')}/${d.id}`);
    const konu: BdKonu = {
      id: g,
      ad: String(d.shortTitle || d.title || '').replace(/^\d+\s*[.)-]\s*/, ''),
      alt: d.instructor ? String(d.instructor) : undefined,
      beklenen: (d.slideCount || 0) * ADIM_SN,
      turetilen: stateOf(d, p).status === 'done',
      ac,
      tekrar: () => { ogrenBasaAl(l.map((x) => x.id)); ac(); },
    };
    dersler.set(ad, [...(dersler.get(ad) || []), konu]);
  }
  return [...dersler.entries()]
    .sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0], 'tr'))
    .map(([ad, konular]) => ({ id: ad, ad, konular }));
}

async function cozucuYukle(): Promise<BdDers[]> {
  const il = ilerlemeOku();
  return (await cozucuDizinleri()).flatMap(([b, dz]) => {
    if (!dz?.dersler.length) return [];
    return [{
      id: b.id,
      ad: b.tam,
      konular: dz.dersler.map((d) => {
        const ac = () => cozucuyaGit({ brans: b.id, ders: d.kod, coz: '1' });
        return {
          id: `${b.id}/${d.kod}`,
          no: d.no,
          ad: d.baslik,
          alt: [setAdi(d), `${d.soru} soru`].filter(Boolean).join(' · '),
          beklenen: d.sure || d.soru * SORU_SN,
          turetilen: ozet(il[d.kod], d.soru).tamam,
          ac,
          tekrar: () => { ilerlemeYaz(d.kod, null); ac(); },
        };
      }),
    }];
  });
}


async function onemYukle(): Promise<BdDers[]> {
  const ogr = ogrenilenler();
  const say = new Map<string, number>();
  ogr.forEach((id) => { const k = id.slice(0, id.lastIndexOf('-')); say.set(k, (say.get(k) || 0) + 1); });
  const asistanSure = new Map<string, number>();
  for (const g of getAsistanSureGruplari()) for (const d of g.dersler) asistanSure.set(`${g.brans}/${d.kod}`, d.sure);
  return (await tumBranslar<OnemDizin>(onemDizinYukle)).flatMap(([b, dz]) => {
    if (!dz?.dersler.length) return [];
    return [{
      id: b.id,
      ad: b.tam,
      konular: dz.dersler.map((d) => {
        const ac = () => onemeGit({ brans: b.id, ders: d.kod });
        return {
          id: `${b.id}/${d.kod}`,
          no: d.no,
          ad: d.baslik,
          alt: `${d.madde} madde · ${say.get(d.kod) || 0} öğrenildi`,
          beklenen: asistanSure.get(`${b.id}/${d.kod}`) || d.madde * MADDE_SN,
          turetilen: d.madde > 0 && (say.get(d.kod) || 0) >= d.madde,
          ac,
          tekrar: () => { onemAsistanBasaAl(d.kod); ac(); },
        };
      }),
    }];
  });
}

/** Kurul kampı: kurul → branş kampı; konu kimliği `k<N>/<brans>` (takipte `kamp:k<N>/<brans>`) */
async function kampYukle(): Promise<BdDers[]> {
  const out: BdDers[] = [];
  for (const { kurul } of KURULLAR) {
    const L = (await Promise.all(kurulKampYollari(kurul).map((x) => x.yukle().catch(() => null)))).filter((x): x is Kamp => !!x);
    if (!L.length) continue;
    out.push({
      id: `k${kurul}`,
      ad: `Kurul ${kurul}`,
      konular: L.sort((a, b) => a.baslik.localeCompare(b.baslik, 'tr')).map((k) => {
        const a = kampAnahtar(k.kurul, k.brans);
        const o = kampOzeti(k, kampKaydi(a));
        const ac = () => navigateTo(`/kamp/${k.kurul}/${k.brans}`);
        return {
          id: a,
          ad: k.baslik,
          alt: `${bransAdi(k.brans)} · %${o.yuzde}`,
          beklenen: k.anlatim.length * MADDE_SN + k.deneme.length * SORU_SN + o.satirToplam * 10,
          turetilen: o.tamam,
          ac,
          tekrar: () => { kampSifirla(a); ac(); },
        };
      }),
    });
  }
  return out;
}

export const MODUL_YUKLE: Record<TakipModul, () => Promise<BdDers[]>> = {
  sesli: sesliYukle,
  ogren: ogrenYukle,
  cozucu: cozucuYukle,
  onem: onemYukle,
  kamp: kampYukle,
};
