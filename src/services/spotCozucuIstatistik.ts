import { useSyncExternalStore } from 'react';
import { BRANSLAR, type Brans } from '../components/spots/brans';
import { ILERLEME_KEY as COZUCU_ILERLEME_KEY, type DersIlerleme } from '../components/spots/cozucu/cozucuVeri';
import { ANAHTAR as SPOT_OGRENDIM_KEY } from '../components/spots/spotsShared';

/**
 * Sınav Spotları ve Sesli Soru Çözücü — Kaldığın Yer, İlerleme & İstatistik Servisi.
 *
 * Kullanıcının:
 *  - Spot bilgilerde en son hangi derste ve hangi spotta kaldığını,
 *  - Soru çözücülerde en son hangi branşta, hangi derste ve kaçıncı soruda kaldığını,
 *  - Spotlarda kaç dakika çalıştığını ve kaç spot öğrendiğini,
 *  - Soru çözücülerde kaç dakika çözdüğünü, doğru ilerleyişini (% doğruluk, ilk denemede doğru, yardımlı, yanlış),
 *  - Soru başına ortalama çözüm süresini
 * kayıt altına alır ve kullanıcıya özel tasarımla sunar.
 */

export const SPOT_ILERLEME_KEY = 'medsoru_spot_ilerleme_v1';
export const COZUCU_ISTATISTIK_KEY = 'medsoru_cozucu_istatistik_v1';
const STATS_OLAY = 'medsor:spot-cozucu-stats';

// Soru çözücü dizinlerini derleme zamanında hazır yükle (7 branşın tüm soruları)
const COZUCU_DIZINLER = import.meta.glob('../data/*_cozucu/index.json', { eager: true }) as Record<
  string,
  { default: { dersler: Array<{ kod: string; no: number; baslik: string; soru: number; cikmis?: number; set?: number; setSay?: number; sure?: number }> } }
>;

export interface LastSpotInfo {
  id: string;
  ders: number;
  baslik: string;
  kategori?: string;
  at: string;
}

export interface LastCozucuInfo {
  brans: Brans;
  kod: string;
  dersNo: number;
  baslik: string;
  soruNo: number;
  toplamSoru: number;
  at: string;
}

export interface SpotStoreData {
  lastSpot?: LastSpotInfo;
  sureSn: number;
  sonZiyaret?: string;
}

export interface CozucuStoreData {
  lastCozucu?: LastCozucuInfo;
  sureSn: number;
  sonZiyaret?: string;
}

export interface BransCozucuIstatistik {
  brans: Brans;
  ad: string;
  tamAd: string;
  toplamSoru: number;
  cozulenSoru: number;
  dogruIlk: number;
  dogruYardimli: number;
  yanlis: number;
  dogrulukOrani: number;
  tamamlananDers: number;
  toplamDers: number;
}

export interface SpotCozucuStats {
  // Spotlar
  toplamSpot: number;
  ogrenilenSpot: number;
  spotOgrenmeOrani: number;
  spotSureSn: number;
  spotSureDk: number;
  lastSpot: LastSpotInfo | null;

  // Soru Çözücü
  toplamSoru: number;
  cozulenSoru: number;
  cozulmeOrani: number;
  dogruIlk: number;
  dogruYardimli: number;
  yanlis: number;
  dogrulukOrani: number;
  basariOrani: number;
  cozucuSureSn: number;
  cozucuSureDk: number;
  ortalamaSoruSuresiSn: number;
  tamamlananDers: number;
  toplamDers: number;
  lastCozucu: LastCozucuInfo | null;
  branslar: BransCozucuIstatistik[];

  // Toplam
  toplamSureSn: number;
  toplamSureDk: number;
}

const safeJsonParse = <T>(val: string | null, fallback: T): T => {
  if (!val) return fallback;
  try {
    const parsed = JSON.parse(val);
    return (parsed && typeof parsed === 'object') ? parsed : fallback;
  } catch {
    return fallback;
  }
};

export const getSpotData = (): SpotStoreData => {
  try {
    return safeJsonParse<SpotStoreData>(localStorage.getItem(SPOT_ILERLEME_KEY), { sureSn: 0 });
  } catch {
    return { sureSn: 0 };
  }
};

export const getCozucuData = (): CozucuStoreData => {
  try {
    return safeJsonParse<CozucuStoreData>(localStorage.getItem(COZUCU_ISTATISTIK_KEY), { sureSn: 0 });
  } catch {
    return { sureSn: 0 };
  }
};

const notifyChange = () => {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new Event(STATS_OLAY));
  }
};

/**
 * Kullanıcı bir spotu incelediğinde veya tıkladığında kaldığı yeri kaydeder.
 */
export function kaydetSpotZiyaret(spot: { id: string; ders: number; baslik: string; kategori?: string }) {
  if (typeof window === 'undefined') return;
  try {
    const cur = getSpotData();
    const guncel: SpotStoreData = {
      ...cur,
      lastSpot: {
        id: spot.id,
        ders: spot.ders,
        baslik: spot.baslik,
        kategori: spot.kategori,
        at: new Date().toISOString(),
      },
      sonZiyaret: new Date().toISOString(),
    };
    localStorage.setItem(SPOT_ILERLEME_KEY, JSON.stringify(guncel));
    notifyChange();
  } catch {
    // Özel pencere / kota
  }
}

/**
 * Kullanıcı soru çözücüde bir soruya geldiğinde veya çözdüğünde kaldığı yeri kaydeder.
 */
export function kaydetCozucuZiyaret(bilgi: {
  brans: Brans;
  kod: string;
  dersNo: number;
  baslik: string;
  soruNo: number;
  toplamSoru: number;
}) {
  if (typeof window === 'undefined') return;
  try {
    const cur = getCozucuData();
    const guncel: CozucuStoreData = {
      ...cur,
      lastCozucu: {
        ...bilgi,
        at: new Date().toISOString(),
      },
      sonZiyaret: new Date().toISOString(),
    };
    localStorage.setItem(COZUCU_ISTATISTIK_KEY, JSON.stringify(guncel));
    notifyChange();
  } catch {
    // Özel pencere / kota
  }
}

/**
 * Spot çalışma süresine saniye ekler.
 */
export function ekleSpotSure(saniye: number) {
  if (typeof window === 'undefined' || saniye <= 0) return;
  try {
    const cur = getSpotData();
    const guncel: SpotStoreData = {
      ...cur,
      sureSn: (cur.sureSn || 0) + saniye,
      sonZiyaret: new Date().toISOString(),
    };
    localStorage.setItem(SPOT_ILERLEME_KEY, JSON.stringify(guncel));
    notifyChange();
  } catch {
    // kota
  }
}

/**
 * Soru çözücü çalışma süresine saniye ekler.
 */
export function ekleCozucuSure(saniye: number) {
  if (typeof window === 'undefined' || saniye <= 0) return;
  try {
    const cur = getCozucuData();
    const guncel: CozucuStoreData = {
      ...cur,
      sureSn: (cur.sureSn || 0) + saniye,
      sonZiyaret: new Date().toISOString(),
    };
    localStorage.setItem(COZUCU_ISTATISTIK_KEY, JSON.stringify(guncel));
    notifyChange();
  } catch {
    // kota
  }
}

/**
 * Anlık tüm istatistikleri, doğruluk oranlarını ve kalınan yerleri hesaplar.
 */
export function computeSpotCozucuStats(): SpotCozucuStats {
  const spotData = getSpotData();
  const cozucuData = getCozucuData();

  // 1. Spot Öğrenilenler
  let ogrenilenSpotSet = new Set<string>();
  try {
    const raw = localStorage.getItem(SPOT_OGRENDIM_KEY);
    if (raw) ogrenilenSpotSet = new Set(JSON.parse(raw));
  } catch {
    // boş
  }
  const toplamSpot = 1700; // Kurul 1 toplam spot sayısı
  const ogrenilenSpot = ogrenilenSpotSet.size;
  const spotOgrenmeOrani = toplamSpot > 0 ? Math.round((ogrenilenSpot / toplamSpot) * 100) : 0;
  const spotSureSn = Math.max(0, spotData.sureSn || 0);

  // 2. Soru Çözücü İlerlemeleri
  let cozucuIlerlemeMap: Record<string, DersIlerleme> = {};
  try {
    const raw = localStorage.getItem(COZUCU_ILERLEME_KEY);
    if (raw) cozucuIlerlemeMap = JSON.parse(raw);
  } catch {
    // boş
  }

  let toplamSoru = 0;
  let cozulenSoru = 0;
  let dogruIlk = 0;
  let dogruYardimli = 0;
  let yanlis = 0;
  let tamamlananDers = 0;
  let toplamDers = 0;

  const branslar: BransCozucuIstatistik[] = [];

  for (const b of BRANSLAR) {
    const yol = `../data/${b.id}_cozucu/index.json`;
    const dizin = COZUCU_DIZINLER[yol]?.default;
    const dersler = dizin?.dersler || [];

    let bToplamSoru = 0;
    let bCozulen = 0;
    let bDogruIlk = 0;
    let bYardimli = 0;
    let bYanlis = 0;
    let bTamamlananDers = 0;

    for (const d of dersler) {
      toplamDers++;
      bToplamSoru += d.soru || 0;
      toplamSoru += d.soru || 0;

      const p = cozucuIlerlemeMap[d.kod];
      if (p && p.s) {
        const sonuclar = Object.values(p.s);
        const dCount = sonuclar.filter((x) => x === 'd').length;
        const d2Count = sonuclar.filter((x) => x === 'd2').length;
        const yCount = sonuclar.filter((x) => x === 'y').length;
        const cCount = sonuclar.length;

        bCozulen += cCount;
        bDogruIlk += dCount;
        bYardimli += d2Count;
        bYanlis += yCount;

        cozulenSoru += cCount;
        dogruIlk += dCount;
        dogruYardimli += d2Count;
        yanlis += yCount;

        if (cCount >= d.soru && d.soru > 0) {
          bTamamlananDers++;
          tamamlananDers++;
        }
      }
    }

    const bDogruluk = bCozulen > 0 ? Math.round((bDogruIlk / bCozulen) * 100) : 0;

    branslar.push({
      brans: b.id,
      ad: b.ad,
      tamAd: b.tam,
      toplamSoru: bToplamSoru,
      cozulenSoru: bCozulen,
      dogruIlk: bDogruIlk,
      dogruYardimli: bYardimli,
      yanlis: bYanlis,
      dogrulukOrani: bDogruluk,
      tamamlananDers: bTamamlananDers,
      toplamDers: dersler.length,
    });
  }

  const cozucuSureSn = Math.max(0, cozucuData.sureSn || 0);
  const dogrulukOrani = cozulenSoru > 0 ? Math.round((dogruIlk / cozulenSoru) * 100) : 0;
  const basariOrani = cozulenSoru > 0 ? Math.round(((dogruIlk + dogruYardimli * 0.7) / cozulenSoru) * 100) : 0;
  const ortalamaSoruSuresiSn = cozulenSoru > 0 ? Math.round(cozucuSureSn / cozulenSoru) : 0;
  const cozulmeOrani = toplamSoru > 0 ? Math.round((cozulenSoru / toplamSoru) * 100) : 0;

  const toplamSureSn = spotSureSn + cozucuSureSn;

  return {
    toplamSpot,
    ogrenilenSpot,
    spotOgrenmeOrani,
    spotSureSn,
    spotSureDk: Math.round(spotSureSn / 60),
    lastSpot: spotData.lastSpot || null,

    toplamSoru,
    cozulenSoru,
    cozulmeOrani,
    dogruIlk,
    dogruYardimli,
    yanlis,
    dogrulukOrani,
    basariOrani,
    cozucuSureSn,
    cozucuSureDk: Math.round(cozucuSureSn / 60),
    ortalamaSoruSuresiSn,
    tamamlananDers,
    toplamDers,
    lastCozucu: cozucuData.lastCozucu || null,
    branslar,

    toplamSureSn,
    toplamSureDk: Math.round(toplamSureSn / 60),
  };
}

// React Hook
let cachedStats: SpotCozucuStats | null = null;
const getSnapshot = () => (cachedStats ??= computeSpotCozucuStats());

const subscribe = (onStoreChange: () => void) => {
  const handler = (e: Event) => {
    if (
      e.type === STATS_OLAY ||
      (e as StorageEvent).key == null ||
      (e as StorageEvent).key === SPOT_ILERLEME_KEY ||
      (e as StorageEvent).key === COZUCU_ISTATISTIK_KEY ||
      (e as StorageEvent).key === SPOT_OGRENDIM_KEY ||
      (e as StorageEvent).key === COZUCU_ILERLEME_KEY
    ) {
      cachedStats = computeSpotCozucuStats();
      onStoreChange();
    }
  };

  if (typeof window !== 'undefined') {
    window.addEventListener(STATS_OLAY, handler);
    window.addEventListener('storage', handler);
  }

  return () => {
    if (typeof window !== 'undefined') {
      window.removeEventListener(STATS_OLAY, handler);
      window.removeEventListener('storage', handler);
    }
  };
};

export const useSpotCozucuStats = () => useSyncExternalStore(subscribe, getSnapshot, getSnapshot);

/**
 * Süre biçimlendirme yardımcıları
 */
export const fmtSureDk = (saniye: number): string => {
  const m = Math.round(saniye / 60);
  const h = Math.floor(m / 60);
  if (h > 0) {
    const kalanM = m % 60;
    return kalanM > 0 ? `${h} sa ${kalanM} dk` : `${h} sa`;
  }
  return `${m} dk`;
};

export const relZamanTr = (iso: string): string => {
  try {
    const ms = Date.now() - Date.parse(iso);
    if (isNaN(ms) || ms < 0) return 'az önce';
    if (ms < 60_000) return 'az önce';
    if (ms < 3_600_000) return `${Math.floor(ms / 60_000)} dk önce`;
    if (ms < 86_400_000) return `${Math.floor(ms / 3_600_000)} sa önce`;
    if (ms < 7 * 86_400_000) return `${Math.floor(ms / 86_400_000)} gün önce`;
    return new Date(iso).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
  } catch {
    return 'az önce';
  }
};
