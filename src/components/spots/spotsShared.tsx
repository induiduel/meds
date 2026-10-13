import React from 'react';

/**
 * Sınav spotları ortak tipleri ve küçük yardımcılar (ExamSpotsView + SpotCard).
 * Veri biçimi: src/data/exam_spots_k1.json (scripts/sinav_spotlari/birlestir.py üretir).
 */

export type Kategori = 'en_sik' | 'karakteristik' | 'sayi' | 'eslesme' | 'tani_tedavi' | 'mekanizma' | 'tuzak' | 'siniflama';

export interface Spot {
  id: string;
  ders: number;
  kategori: Kategori;
  onem: 1 | 2 | 3;
  baslik: string;
  spot: string;
  maddeler?: string[];
  soru?: string;
  cevap?: string;
  tuzak?: string;
  karsilastir?: { basliklar: string[]; satirlar: string[][] } | null;
  etiketler?: string[];
  kaynak: { satir?: number; alinti: string }[];
}
export interface Ders { no: number; id: string; baslik: string; disiplin: string; hoca?: string; tarih?: string; sayi: number }
export interface Veri { kurul?: number; dersler: Ders[]; spotlar: Spot[] }

export const KATEGORILER: { id: Kategori; ad: string; kisa: string; aciklama: string }[] = [
  { id: 'en_sik', ad: 'En sık · en az · tek', kisa: 'En sık', aciklama: 'En sık, en az, en çok, tek, ilk ifadeleri' },
  { id: 'karakteristik', ad: 'Karakteristik bulgu', kisa: 'Karakteristik', aciklama: 'Patognomonik, tipik görünüm, triad' },
  { id: 'tuzak', ad: 'Tuzak & çeldirici', kisa: 'Tuzak', aciklama: 'Karıştırılan kavramlar, klasik çeldiriciler' },
  { id: 'eslesme', ad: 'Eşleştir', kisa: 'Eşleştir', aciklama: 'Etken → hastalık, gen → sendrom, belirteç → tümör' },
  { id: 'sayi', ad: 'Sayı & oran', kisa: 'Sayı', aciklama: 'Yüzde, eşik, süre, doz' },
  { id: 'tani_tedavi', ad: 'Tanı & tedavi', kisa: 'Tanı/Tedavi', aciklama: 'İlk tercih, altın standart, tanı testi' },
  { id: 'mekanizma', ad: 'Mekanizma', kisa: 'Mekanizma', aciklama: 'Sınavda sorulan neden–sonuç' },
  { id: 'siniflama', ad: 'Sınıflama', kisa: 'Sınıflama', aciklama: 'Tip, evre, derece ayrımı' },
];
export const KAT = Object.fromEntries(KATEGORILER.map((k) => [k.id, k])) as Record<Kategori, (typeof KATEGORILER)[number]>;

/** "Öğrendim" işaretleri tarayıcıda; anahtar eski sürümle aynı (kullanıcı ilerlemesi korunur). */
export const ANAHTAR = 'medsoru_spot_ogrendim';
export const okuOgrenilen = (): Set<string> => {
  try { return new Set(JSON.parse(localStorage.getItem(ANAHTAR) || '[]')); } catch { return new Set(); }
};
export const yazOgrenilen = (s: Set<string>) => {
  try { localStorage.setItem(ANAHTAR, JSON.stringify([...s])); } catch { /* özel pencere */ }
};

export const kucuk = (s: string) => s.toLocaleLowerCase('tr-TR');

/** Hareket azaltma tercihi: kaydırmalar anlık olur. */
export const azHareket = () =>
  typeof window !== 'undefined' && !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

/** **kalın** → <strong>; başka biçim yok */
export const Zengin: React.FC<{ metin: string }> = ({ metin }) => (
  <>
    {metin.split(/(\*\*[^*]+\*\*)/g).map((p, i) =>
      p.startsWith('**') && p.endsWith('**') ? <strong key={i}>{p.slice(2, -2)}</strong> : <React.Fragment key={i}>{p}</React.Fragment>
    )}
  </>
);
