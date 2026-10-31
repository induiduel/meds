/** KMB ders verisi türleri ve ortak yardımcılar (src/data/kmb/<kod>.json; şema docs/KMB_GORSEL_ASISTAN.md §3) */
import type { Eylem } from './eylem';

export type Adim = { id: string; baslik: string; sahne: string; ek?: string[]; cumleler: { metin: string; eylem?: Eylem[] }[]; puf?: string[]; dikkat?: string[] };
/** Sınav ögelerindeki `adim`: ilgili öğretim adımı (hata istatistiği "bu adımı yeniden çalış" yolu) */
export type Senaryo = { id: string; baslik: string; sahne: string; adim?: string; eylem?: Eylem[]; soru: string; secenekler: { metin: string; dogru: boolean; aciklama: string }[]; puf?: string };
/** Dallanan OSCE akışı: dal yalnız listenin son basamağında; her yol kendi basamak listesini taşır (iç içe dal olabilir) */
export type Basamak = { id: string; metin: string; aciklama: string; adim?: string; dal?: { soru: string; yollar: { id: string; etiket: string; basamaklar: Basamak[] }[] } };
export type Akis = { id: string; ad: string; yonerge: string; basamaklar: Basamak[] };
export type Bul = { id: string; sahne: string; yonerge: string; hedef: string; aciklama: string; adim?: string };
/** Hedefler filmi vuruşu (cümle başına): sahne değişimi (durum sıfırlanır), biriken eylemler, kameranın yaklaştığı öge ve yakınlaşma */
export type FilmVurus = { sahne?: string; eylem?: Eylem[]; odak?: string; zoom?: number; /** 3B kamera açısı sapması [yaw, pitch] derece */ aci?: [number, number] };
export type HedefKart = { no: number; sahne: string; eylem?: Eylem[]; lottie?: string; ne: string; nasil: string[]; neden: string; hata: string; hoca: string; dogrulanacak?: string; film?: FilmVurus[] };
export type Ders = {
  kod: string; slug: string; ad: string; belgeKodu: string; amac: string;
  hedefler: { no: number; metin: string; adimlar: string[] }[];
  hedefCalisma?: HedefKart[];
  adimlar: Adim[];
  sinav: { akislar: Akis[]; senaryolar: Senaryo[]; bul: Bul[] };
};
export type SesKayit = Record<string, { h: string; sure: number; zaman: [number, number][] }>;

export function karistir<T>(a: T[], tohum: number): T[] {
  const r = [...a];
  let s = tohum;
  for (let i = r.length - 1; i > 0; i--) { s = (s * 9301 + 49297) % 233280; const j = Math.floor((s / 233280) * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; }
  return r;
}

export type Yol = { ad: string; basamaklar: Basamak[]; kararlar: { sonra: number; soru: string; etiket: string }[] };

/** Ağacı uçtan uca yollara aç: her yol düz basamak listesi + hangi basamaktan sonra hangi kararın geldiği */
export function yollar(L: Basamak[], on: Yol = { ad: '', basamaklar: [], kararlar: [] }): Yol[] {
  const tum = { ...on, basamaklar: [...on.basamaklar, ...L] };
  const son = L[L.length - 1];
  if (!son?.dal) return [tum];
  return son.dal.yollar.flatMap((y) => yollar(y.basamaklar, {
    ad: on.ad ? `${on.ad} → ${y.etiket}` : y.etiket,
    basamaklar: tum.basamaklar,
    kararlar: [...tum.kararlar, { sonra: tum.basamaklar.length, soru: son.dal!.soru, etiket: y.etiket }],
  }));
}

/** Basamağın kavram anahtarı: aynı metinli dal basamakları (ör. üç yolda "kaydet") tek kavramdır */
export const basamakAnahtar = (akis: string, b: Basamak) => `b:${akis}:${b.metin}`;

/** Öğrenme ilerlemesi (yerel + hesap eşitlemesi) */
export const IL = 'kmb-ilerleme';
export function ilOku<T>(k: string, varsayilan: T): T { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : varsayilan; } catch { return varsayilan; } }
export function ilYaz(k: string, v: unknown) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* özel pencere: yalnız oturumda */ } window.dispatchEvent(new Event(IL)); }
export const ilAnahtar = (kod: string, ne: string) => `medsoru_kmb_${ne}_${kod}`;
