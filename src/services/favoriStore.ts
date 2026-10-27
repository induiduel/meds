/**
 * Favoriler (medsoru_favoriler_v1): ders içerik sayfalarında (terim, hastalık, bilgi, spot, tablo, liste) ★ ile kaydedilen
 * ya da "tekrar et" işaretlenen kayıtlar. Bugün sayfasında listelenir, PDF'e aktarılır, profille eşitlenir (userKvSync).
 * Her kayıt kaynağını taşır: ders, kurul, bölüm, slayt/PDF sayfası, Öğren adımı — eksik kaynak bilgisi yazılmaz.
 */
import { useEffect, useState } from 'react';

export type FavoriTur = 'terim' | 'hastalik' | 'bilgi' | 'onemli' | 'spot' | 'tablo' | 'liste';
export interface Favori {
  id: string; // <dersKey>|<tur>|<başlık>
  tur: FavoriTur;
  baslik: string;
  metin: string; // satır sonlu düz metin ('- ' ile maddeler)
  dersKey: string;
  ders: string;
  kurul: number;
  bolum: string; // ?b= değeri
  slayt?: number[]; // PDF/slayt sayfaları
  adim?: number; // Öğren adımı
  yildiz: boolean;
  tekrar: boolean;
  tarih: number;
}
export const FAVORI_KEY = 'medsoru_favoriler_v1';
const OLAY = 'medsor:favoriler_degisti';

export const favoriOku = (): Favori[] => {
  try { const v = JSON.parse(localStorage.getItem(FAVORI_KEY) || '[]'); return Array.isArray(v) ? v : []; } catch { return []; }
};
const yaz = (l: Favori[]) => {
  try { localStorage.setItem(FAVORI_KEY, JSON.stringify(l)); window.dispatchEvent(new CustomEvent(OLAY)); } catch { /* gizli pencere */ }
};
export const favoriId = (dersKey: string, tur: FavoriTur, baslik: string) => `${dersKey}|${tur}|${baslik}`;

/** Bayrağı çevirir; ikisi de kapanınca kayıt silinir. */
export function favoriCevir(k: Omit<Favori, 'yildiz' | 'tekrar' | 'tarih'>, bayrak: 'yildiz' | 'tekrar') {
  const l = favoriOku(); const i = l.findIndex((x) => x.id === k.id);
  if (i < 0) { yaz([{ ...k, yildiz: bayrak === 'yildiz', tekrar: bayrak === 'tekrar', tarih: Date.now() }, ...l]); return; }
  const y = { ...l[i], [bayrak]: !l[i][bayrak] };
  if (!y.yildiz && !y.tekrar) l.splice(i, 1); else l[i] = y;
  yaz(l);
}
export const favoriSil = (id: string) => yaz(favoriOku().filter((x) => x.id !== id));

export function useFavoriler(): Favori[] {
  const [l, setL] = useState(favoriOku);
  useEffect(() => {
    const f = () => setL(favoriOku());
    window.addEventListener(OLAY, f); window.addEventListener('storage', f);
    return () => { window.removeEventListener(OLAY, f); window.removeEventListener('storage', f); };
  }, []);
  return l;
}
