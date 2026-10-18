/**
 * Sınav Çalışması — veri ve ilerleme deposu.
 * İçerik: src/data/sinav_calisma/k1/{index,<ders>-<konu>}.json (scripts/sinav_calisma_bol.py, kaynak sinav_calisma_k1.json).
 * Dizin küçüktür (~140 KB) ve sayfa açılınca gelir; bir konunun soruları ancak o konudan kazanım açılınca yüklenir.
 * İlerleme profilde eşitlenir (userKvSync: medsoru_sinav_calisma_v2) — kazanım → soru → 'd' (ilk denemede doğru) | 'y'.
 */
import type { CSoru, Harf } from '../spots/cozucu/cozucuVeri';

export type Zorluk = 'kolay' | 'orta' | 'zor';
export interface KzOzet { id: string; no: number; metin: string; soru: number; cikmis: number; zorluk: Record<Zorluk, number> }
export interface KonuOzet { ad: string; dosya: string; kazanimlar: KzOzet[] }
export interface DersOzet { ad: string; konular: KonuOzet[] }
export interface SinavDizin { kurul: number; ad: string; kod: string; dersler: DersOzet[]; toplam: { kazanim: number; soru: number } }

export interface SSoru {
  id: string;
  tur?: 'cikmis';
  yil?: string;
  zorluk: Zorluk;
  soru: string;
  secenekler: Partial<Record<Harf, string>>;
  dogru: Harf;
  aciklama: string;
  siklar?: Partial<Record<Harf, string>>;
  ipucu?: string;
}
export interface KzAyrinti {
  id: string;
  sorular: SSoru[];
  ozet?: string;
  bilinmesi_gerekenler?: string[];
  anlatim?: string[];
  slaytlar?: { sayfa: number; baslik: string; deck: string }[];
}

const DOSYA = import.meta.glob('../../data/sinav_calisma/k1/*.json') as Record<string, () => Promise<{ default: unknown }>>;
const yol = (ad: string) => `../../data/sinav_calisma/k1/${ad}.json`;

let dizinP: Promise<SinavDizin> | null = null;
export const dizinYukle = (): Promise<SinavDizin> => {
  if (!dizinP) {
    const f = DOSYA[yol('index')];
    dizinP = f ? f().then((m) => m.default as SinavDizin) : Promise.reject(new Error('Sınav çalışması verisi yok'));
    dizinP.catch(() => { dizinP = null; });
  }
  return dizinP;
};

const konuP = new Map<string, Promise<Map<string, KzAyrinti>>>();
export const konuYukle = (dosya: string): Promise<Map<string, KzAyrinti>> => {
  let p = konuP.get(dosya);
  if (!p) {
    const f = DOSYA[yol(dosya)];
    p = f
      ? f().then((m) => new Map((m.default as { kazanimlar: KzAyrinti[] }).kazanimlar.map((k) => [k.id, k])))
      : Promise.reject(new Error(`konu yok: ${dosya}`));
    p.catch(() => konuP.delete(dosya));
    konuP.set(dosya, p);
  }
  return p;
};

/* ── İlerleme ─────────────────────────────────────────────────────────── */
export type Sonuc = 'd' | 'y';
export type Ilerleme = Record<string, Record<string, Sonuc>>;
export const ILERLEME_KEY = 'medsoru_sinav_calisma_v2';

export const ilerlemeOku = (): Ilerleme => {
  try {
    const v = JSON.parse(localStorage.getItem(ILERLEME_KEY) || '{}');
    return v && typeof v === 'object' ? v : {};
  } catch {
    return {};
  }
};
export const ilerlemeYaz = (v: Ilerleme) => {
  try { localStorage.setItem(ILERLEME_KEY, JSON.stringify(v)); } catch { /* depolama kapalı: bu oturumda bellekte kalır */ }
};

/* ── Sesli çözücüye dönüştürme ────────────────────────────────────────── */
const VARSAYILAN_IPUCU = 'Kazanımın temel mekanizmasını ve ayırıcı noktalarını düşün.';
export const cozucuSorulari = (sorular: SSoru[]): CSoru[] =>
  sorular.map((s, i) => ({
    no: i + 1,
    tur: s.tur === 'cikmis' ? 'cikmis' : 'ornek',
    sinav: s.yil,
    zorluk: s.zorluk,
    soru: s.soru,
    secenekler: s.secenekler as Record<Harf, string>,
    dogru: s.dogru,
    ipucu: s.ipucu || VARSAYILAN_IPUCU,
    siklar: (s.siklar || {}) as Record<Harf, string>,
    cozum: s.aciklama,
    sayfa: [],
  }));

/** Arama için Türkçe katlama: büyük/küçük harf + aksan duyarsız */
export const katla = (s: string) =>
  s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');
