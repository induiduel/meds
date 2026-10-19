/** Patoloji alternatif sesli soru çözücü — veri yükleyici ve ilerleme deposu.
 * Metin: src/data/patoloji_cozucu_alt/{index,<kod>}.json (scripts/patoloji_cozucu_alt/paketle.py).
 * Ses: /api/patoloji-cozucu-alt/ses/<kod>/<no>.mp3 (src/services/patolojiCozucuAlt.ts).
 */
import { useEffect, useState } from 'react';

export type Harf = 'A' | 'B' | 'C' | 'D' | 'E';
export const HARFLER: Harf[] = ['A', 'B', 'C', 'D', 'E'];

export interface AltSoru {
  no: number;
  tur: 'ornek' | 'cikmis';
  zorluk?: 'kolay' | 'orta' | 'zor';
  sinav?: string;
  soru: string;
  secenekler: Record<Harf, string>;
  dogru: Harf;
  giris: string;
  aciklamalar: Record<Harf, string>;
  ozet: string;
  ipucu?: string;
  sayfa?: number[];
  mp3: string;
  h: string;
  sure: number;
  /** 13 kümülatif bitiş saniyesi: [0]=kök, [1..5]=A..E şık okuma, [6]=giriş, [7..11]=A..E açıklama, [12]=cevap, >[12]=özet */
  zaman?: number[];
}

export interface AltDers {
  kod: string;
  no: number;
  baslik: string;
  sorular: AltSoru[];
}

export interface AltDizinDers {
  kod: string;
  no: number;
  baslik: string;
  soru: number;
  ornek: number;
  cikmis: number;
  sure: number;
}

export interface AltDizin {
  surum: string;
  dersler: AltDizinDers[];
}

const DOSYA = import.meta.glob('../../data/patoloji_cozucu_alt/*.json') as Record<string, () => Promise<{ default: unknown }>>;
const yol = (kod: string) => `../../data/patoloji_cozucu_alt/${kod}.json`;

export const altDizinYukle = async (): Promise<AltDizin> => {
  const f = DOSYA['../../data/patoloji_cozucu_alt/index.json'];
  if (!f) return { surum: '', dersler: [] };
  return (await f()).default as AltDizin;
};

const bellek = new Map<string, Promise<AltDers>>();
export const altDersYukle = (kod: string): Promise<AltDers> => {
  let p = bellek.get(kod);
  if (!p) {
    const f = DOSYA[yol(kod)];
    if (!f) return Promise.reject(new Error(`ders yok: ${kod}`));
    p = f().then((m) => m.default as AltDers);
    p.catch(() => bellek.delete(kod));
    bellek.set(kod, p);
  }
  return p;
};

export const altSesYolu = (kod: string, s: AltSoru) =>
  `/api/patoloji-cozucu-alt/ses/${encodeURIComponent(kod)}/${encodeURIComponent(s.mp3)}${s.h ? `?v=${s.h}` : ''}`;

/** Ders başına kalınan soru, dinlenen/çözülen sorular ve şık seçimleri (tarayıcıda + profil senkronunda) */
export interface AltIlerleme {
  i: number;
  bitti: number[];
  secim?: Record<number, Harf>;
  ilkDogru?: number[];
  incelenen?: number[];
  son?: number;
}

const KEY = 'medsoru_alt_cozucu_v1';
const OLAY = 'medsoru:alt-ilerleme';

export const ilerlemeOku = (): Record<string, AltIlerleme> => {
  try {
    const x = JSON.parse(localStorage.getItem(KEY) || '{}');
    return x && typeof x === 'object' ? x : {};
  } catch {
    return {};
  }
};

export const ilerlemeYaz = (kod: string, p: AltIlerleme) => {
  try {
    const t = ilerlemeOku();
    t[kod] = { ...t[kod], ...p, son: p.son ?? Date.now() };
    localStorage.setItem(KEY, JSON.stringify(t));
    window.dispatchEvent(new Event(OLAY));
  } catch {
    /* özel pencere */
  }
};

export const ilerlemeDersSifirla = (kod: string) => {
  try {
    const t = ilerlemeOku();
    delete t[kod];
    localStorage.setItem(KEY, JSON.stringify(t));
    window.dispatchEvent(new Event(OLAY));
  } catch {
    /* özel pencere */
  }
};

export const useAltIlerleme = (): Record<string, AltIlerleme> => {
  const [veri, setVeri] = useState<Record<string, AltIlerleme>>(() => ilerlemeOku());
  useEffect(() => {
    const yenile = () => setVeri(ilerlemeOku());
    const depolama = (e: StorageEvent) => {
      if (!e.key || e.key === KEY) yenile();
    };
    window.addEventListener(OLAY, yenile);
    window.addEventListener('storage', depolama);
    window.addEventListener('medsoru:profile-kv-applied', yenile);
    return () => {
      window.removeEventListener(OLAY, yenile);
      window.removeEventListener('storage', depolama);
      window.removeEventListener('medsoru:profile-kv-applied', yenile);
    };
  }, []);
  return veri;
};

export interface AltTercih {
  hiz: number;
  otoGec: boolean;
  cevabiGizle: boolean;
  cozumdenBasla: boolean;
  olcek: number;
}

const TERCIH_KEY = 'medsoru_alt_cozucu_tercih_v1';
const VARSAYILAN_TERCIH: AltTercih = {
  hiz: 1,
  otoGec: true,
  cevabiGizle: false,
  cozumdenBasla: false,
  olcek: 100,
};

export const tercihOku = (): AltTercih => {
  try {
    const x = JSON.parse(localStorage.getItem(TERCIH_KEY) || '{}');
    if (!x || typeof x !== 'object') return VARSAYILAN_TERCIH;
    return {
      hiz: typeof x.hiz === 'number' && x.hiz >= 0.5 && x.hiz <= 3 ? x.hiz : 1,
      otoGec: typeof x.otoGec === 'boolean' ? x.otoGec : true,
      cevabiGizle: typeof x.cevabiGizle === 'boolean' ? x.cevabiGizle : false,
      cozumdenBasla: typeof x.cozumdenBasla === 'boolean' ? x.cozumdenBasla : false,
      olcek: typeof x.olcek === 'number' ? Math.min(130, Math.max(85, x.olcek)) : 100,
    };
  } catch {
    return VARSAYILAN_TERCIH;
  }
};

export const tercihYaz = (parca: Partial<AltTercih>): AltTercih => {
  const yeni = { ...tercihOku(), ...parca };
  try {
    localStorage.setItem(TERCIH_KEY, JSON.stringify(yeni));
  } catch {
    /* özel pencere */
  }
  return yeni;
};

export type AltSesBolumu =
  | { asama: 'bekle' }
  | { asama: 'kok' }
  | { asama: 'sik'; harf: Harf }
  | { asama: 'giris' }
  | { asama: 'acik'; harf: Harf }
  | { asama: 'cevap' }
  | { asama: 'ozet' };

/** Anlık ses saniyesine göre hangi bölümün okunduğunu ve o ana kadar elenmiş şıkları hesaplar */
export const altSesDurumuHesapla = (
  soru: AltSoru,
  anlik: number,
  caliyor: boolean,
): {
  bolum: AltSesBolumu;
  elenenler: Set<Harf>;
  cozumeUlasti: boolean;
} => {
  const elenenler = new Set<Harf>();
  const z = soru.zaman;
  if (!z || z.length < 13 || (anlik <= 0.05 && !caliyor)) {
    return { bolum: { asama: 'bekle' }, elenenler, cozumeUlasti: false };
  }

  // Açıklaması tamamlanmış yanlış şıkları işaretle
  for (let k = 0; k < 5; k++) {
    const h = HARFLER[k];
    const acikBitis = z[7 + k];
    if (anlik >= acikBitis - 0.15 && h !== soru.dogru) {
      elenenler.add(h);
    }
  }

  const cozumeUlasti = anlik >= z[11] - 0.15;

  if (anlik < z[0]) return { bolum: { asama: 'kok' }, elenenler, cozumeUlasti };
  for (let k = 0; k < 5; k++) {
    if (anlik < z[1 + k]) return { bolum: { asama: 'sik', harf: HARFLER[k] }, elenenler, cozumeUlasti };
  }
  if (anlik < z[6]) return { bolum: { asama: 'giris' }, elenenler, cozumeUlasti };
  for (let k = 0; k < 5; k++) {
    if (anlik < z[7 + k]) return { bolum: { asama: 'acik', harf: HARFLER[k] }, elenenler, cozumeUlasti };
  }
  if (anlik < z[12]) return { bolum: { asama: 'cevap' }, elenenler, cozumeUlasti };
  return { bolum: { asama: 'ozet' }, elenenler, cozumeUlasti };
};

export const dk = (sn: number) => `${Math.max(1, Math.round(sn / 60))} dk`;
export const sureYazi = (sn: number) => {
  if (!sn || !isFinite(sn)) return '0:00';
  const d = Math.floor(sn / 60);
  const s = Math.floor(sn % 60);
  return `${d}:${String(s).padStart(2, '0')}`;
};
