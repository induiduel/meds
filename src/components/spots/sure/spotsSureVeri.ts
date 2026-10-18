import { BRANSLAR, type Brans } from '../brans';

const ASISTAN_DIZINLER = import.meta.glob('../../../data/*_asistan/index.json', { eager: true }) as Record<string, { default: { dersler: AsistanHamDers[] } }>;
const COZUCU_DIZINLER = import.meta.glob('../../../data/*_cozucu/index.json', { eager: true }) as Record<string, { default: { dersler: CozucuHamDers[] } }>;

interface AsistanHamDers {
  kod: string;
  no: number;
  baslik: string;
  bolum?: number;
  adim: number;
  soru: number;
  cikmis?: number;
  ses: boolean;
  sure: number;
}

interface CozucuHamDers {
  kod: string;
  no: number;
  baslik: string;
  soru: number;
  ornek?: number;
  benzer?: number;
  cikmis?: number;
  ses: boolean;
  set?: number;
  setSay?: number;
  sure?: number;
}

export interface SpotDersSure {
  kod: string;
  no: number | string;
  baslik: string;
  sure: number; // saniye
  soru?: number;
  adim?: number;
  cikmis?: number;
  set?: number;
  setSay?: number;
  tamamlandi?: boolean;
}

export interface SpotBransSureGrup {
  brans: Brans;
  ad: string;
  kisa: string;
  alt?: string;
  dersler: SpotDersSure[];
  toplamSure: number;
  toplamSoru: number;
  toplamAdim: number;
  dinlenenSure: number;
}

export const dk = (s: number) => Math.round(s / 60);

export const fmtSaat = (s: number) => {
  const m = Math.round(s / 60);
  const h = Math.floor(m / 60);
  return h ? `${h} sa${m % 60 ? ` ${m % 60} dk` : ''}` : `${m} dk`;
};

export const fmtSure = (s: number) => {
  const m = Math.floor(s / 60);
  const sn = Math.floor(s % 60);
  return `${m}:${sn.toString().padStart(2, '0')}`;
};

const ASISTAN_ILERLEME_KEY = 'medsoru_onem_asistan_v1';
const COZUCU_ILERLEME_KEY = 'medsoru_cozucu_ilerleme_v1';

function okuAsistanIlerleme(): Record<string, { nid: string; at?: string }> {
  try {
    return JSON.parse(localStorage.getItem(ASISTAN_ILERLEME_KEY) || '{}');
  } catch {
    return {};
  }
}

function okuCozucuIlerleme(): Record<string, Record<string, number>> {
  try {
    return JSON.parse(localStorage.getItem(COZUCU_ILERLEME_KEY) || '{}');
  } catch {
    return {};
  }
}

export function getAsistanSureGruplari(): SpotBransSureGrup[] {
  const ilerleme = okuAsistanIlerleme();
  const gruplar: SpotBransSureGrup[] = [];

  for (const b of BRANSLAR) {
    if (!b.asistan) continue;
    const yol = `../../../data/${b.id}_asistan/index.json`;
    const veri = ASISTAN_DIZINLER[yol]?.default;
    if (!veri || !veri.dersler?.length) continue;

    const dersler: SpotDersSure[] = veri.dersler.map((d) => {
      const tamamlandi = !!ilerleme[d.kod];
      return {
        kod: d.kod,
        no: d.no,
        baslik: d.baslik,
        sure: d.sure || 0,
        soru: d.soru || 0,
        adim: d.adim || 0,
        cikmis: d.cikmis,
        tamamlandi,
      };
    });

    const toplamSure = dersler.reduce((acc, d) => acc + d.sure, 0);
    const toplamSoru = dersler.reduce((acc, d) => acc + (d.soru || 0), 0);
    const toplamAdim = dersler.reduce((acc, d) => acc + (d.adim || 0), 0);
    const dinlenenSure = dersler.reduce((acc, d) => acc + (d.tamamlandi ? d.sure : 0), 0);

    gruplar.push({
      brans: b.id,
      ad: b.tam || b.ad,
      kisa: b.ad,
      alt: `${dersler.length} ders`,
      dersler,
      toplamSure,
      toplamSoru,
      toplamAdim,
      dinlenenSure,
    });
  }

  return gruplar;
}

export function getCozucuSureGruplari(): SpotBransSureGrup[] {
  const ilerleme = okuCozucuIlerleme();
  const gruplar: SpotBransSureGrup[] = [];

  for (const b of BRANSLAR) {
    const yol = `../../../data/${b.id}_cozucu/index.json`;
    const veri = COZUCU_DIZINLER[yol]?.default;
    if (!veri || !veri.dersler?.length) continue;

    const dersler: SpotDersSure[] = veri.dersler.map((d) => {
      const p = ilerleme[d.kod] || {};
      const cozulen = Object.keys(p).length;
      const soruSayisi = d.soru || 1;
      const oran = Math.min(1, cozulen / soruSayisi);
      const sure = d.sure || (d.soru * 75);
      return {
        kod: d.kod,
        no: d.no,
        baslik: d.baslik,
        sure,
        soru: d.soru || 0,
        cikmis: d.cikmis,
        set: d.set,
        setSay: d.setSay,
        tamamlandi: oran >= 1,
      };
    });

    const toplamSure = dersler.reduce((acc, d) => acc + d.sure, 0);
    const toplamSoru = dersler.reduce((acc, d) => acc + (d.soru || 0), 0);
    const dinlenenSure = dersler.reduce((acc, d) => {
      const p = ilerleme[d.kod] || {};
      const cozulen = Object.keys(p).length;
      const soruSayisi = d.soru || 1;
      const oran = Math.min(1, cozulen / soruSayisi);
      return acc + Math.round(d.sure * oran);
    }, 0);

    gruplar.push({
      brans: b.id,
      ad: b.tam || b.ad,
      kisa: b.ad,
      alt: `${dersler.length} set · ${toplamSoru} soru`,
      dersler,
      toplamSure,
      toplamSoru,
      toplamAdim: 0,
      dinlenenSure,
    });
  }

  return gruplar;
}
