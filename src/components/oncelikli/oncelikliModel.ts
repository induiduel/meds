/**
 * Öncelikli dersler — puanlama algoritması (ekran tarafı).
 *
 * Ham ölçümler `scripts/oncelikli_dersler/analiz.py` ile ders metninden ve dersin çıkmışlarından çıkarılır
 * (`src/data/oncelikli_dersler/k<N>.json`). Her ders altı boyutta 0–100 puan alır (yüksek = öğrenci lehine):
 *
 *   azEzber      farklı yabancı/Latince terim, ilaç ve hastalık adı, sayı yükü az   (yüzdelik, ters)
 *   mantik       metinde neden-sonuç bağlacı yoğun, "şunlardır / türleri" kalıbı az
 *   kolayCikmis  çıkmışlarda yabancı terim yoğunluğu ve isim soran soru oranı düşük (çıkmışı yoksa bilinmiyor)
 *   kisa         anlatım kısa (kelime sayısı)
 *   getiri       beklenen sınav sorusu / anlatım uzunluğu (branş soru sayısı × dersin çıkmış payı)
 *   sikCikmis    çıkmış sayısı ve kaç farklı yılda sorulduğu
 *
 * Öncelik puanı = Σ ağırlık·boyut / Σ ağırlık. Öğrenci ağırlıkları hazır profilden seçer ya da kendisi ayarlar;
 * eşik süzgeçleri (ör. "az ezberli" = azEzber ≥ 60) sıralamadan önce uygulanır.
 */

export type Boyut = 'azEzber' | 'mantik' | 'kolayCikmis' | 'kisa' | 'getiri' | 'sikCikmis';
export type DersTuru = 'mantik' | 'karma' | 'ezber';

export interface OncelikliDers {
  key: string;
  baslik: string;
  brans: string;
  no: number;
  sureSn: number | null;
  kelime: number;
  terim: number;
  ilac: number;
  hastalik: number;
  gen: number;
  sayi: number;
  terim1000: number;
  mantik1000: number;
  cikmis: number;
  yil: number;
  cikmisIsim: number | null;
  cikmisTerim: number | null;
  cikmisNegatif: number | null;
  beklenen: number;
  boyut: Record<Boyut, number | null>;
  puan: number;
  tur: DersTuru;
  ornekTerim: string[];
  /** YZ yargısı (Claude, ders metni + çıkmışlar okunarak): scripts/oncelikli_dersler/yz/k<N>.json */
  yz?: {
    tur?: DersTuru;
    gerekce?: string;
    ezberCekirdegi?: string[];
    konular?: { baslik: string; tur: DersTuru; cikmis?: boolean }[];
    cikmisNot?: string;
  };
}
export interface OncelikliVeri { kurul: number; varsayilanAgirlik: Record<Boyut, number>; dersler: OncelikliDers[] }

export const BOYUTLAR: { id: Boyut; ad: string; kisa: string; ne: string }[] = [
  { id: 'azEzber', ad: 'Az ezber', kisa: 'Ezber', ne: 'Ezberlenecek yabancı terim, ilaç, hastalık adı ve sayı az' },
  { id: 'mantik', ad: 'Mantıkla çözülür', kisa: 'Mantık', ne: 'Anlatım neden-sonuç zinciriyle ilerliyor; çıkarımla cevaplanır' },
  { id: 'kolayCikmis', ad: 'Çıkmışı kolay', kisa: 'Çıkmış', ne: 'Çıkmış sorular az terimli, isim sormaktan çok anlamayı ölçüyor' },
  { id: 'kisa', ad: 'Kısa', kisa: 'Kısa', ne: 'Dinlemesi kısa sürüyor' },
  { id: 'getiri', ad: 'Puan getirisi', kisa: 'Getiri', ne: 'Çalışma süresine göre sınavda beklenen soru çok' },
  { id: 'sikCikmis', ad: 'Sık çıkıyor', kisa: 'Sıklık', ne: 'Geçmiş sınavlarda çok ve her yıl soruluyor' },
];

export const TUR_AD: Record<DersTuru, string> = { mantik: 'Mantık ağırlıklı', karma: 'Karma', ezber: 'Ezber ağırlıklı' };

export type Agirlik = Record<Boyut, number>;
export interface Profil { id: string; ad: string; ne: string; agirlik: Agirlik }
export const PROFILLER: Profil[] = [
  { id: 'kolay', ad: 'Az ezber, kolay puan', ne: 'Önerilen: ezberi az, mantıkla çözülen, çıkmışı kolay dersler önce',
    agirlik: { azEzber: 3, mantik: 2.5, kolayCikmis: 1.5, kisa: 1.5, getiri: 1.5, sikCikmis: 1 } },
  { id: 'hizli', ad: 'En hızlı puan', ne: 'Kısa sürede en çok beklenen soruyu getirenler',
    agirlik: { azEzber: 1.5, mantik: 1, kolayCikmis: 1, kisa: 2.5, getiri: 3, sikCikmis: 1 } },
  { id: 'sik', ad: 'Sık çıkanlar', ne: 'Geçmiş sınavlarda en çok ve her yıl sorulanlar',
    agirlik: { azEzber: 1, mantik: 0.5, kolayCikmis: 1, kisa: 0.5, getiri: 2, sikCikmis: 3 } },
  { id: 'mantik', ad: 'Yalnız mantık', ne: 'Neredeyse hiç ezber gerektirmeyen, akıl yürütmeyle çözülenler',
    agirlik: { azEzber: 3, mantik: 3, kolayCikmis: 2, kisa: 0.5, getiri: 0.5, sikCikmis: 0.5 } },
];

/** Çıkmışı olmayan derste "çıkmışı kolay" bilinmiyor: hafif ceza (analiz.py ile aynı) */
const BILINMIYOR = 40;

export function oncelikPuani(d: OncelikliDers, a: Agirlik): number {
  let top = 0;
  let w = 0;
  for (const { id } of BOYUTLAR) {
    const k = a[id] || 0;
    if (!k) continue;
    top += (d.boyut[id] ?? BILINMIYOR) * k;
    w += k;
  }
  return w ? Math.round(top / w) : 0;
}

/** Eşik süzgeci: seçili her boyut ≥ ESIK olmalı */
export const ESIK = 60;
export const esikGecer = (d: OncelikliDers, secili: Boyut[]) => secili.every((b) => (d.boyut[b] ?? 0) >= ESIK);

export const veriYukle = (kurul = 1): Promise<OncelikliVeri> =>
  kurul === 1
    ? import('../../data/oncelikli_dersler/k1.json').then((m) => m.default as unknown as OncelikliVeri)
    : Promise.reject(new Error('kurul analizi yok'));
