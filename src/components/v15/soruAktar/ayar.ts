/**
 * Soru dışa aktarıcı · belge ayarları. Tek ayar nesnesi üç biçimi (PDF, DOCX, PPTX) aynı anda yönetir; tasarım modu
 * bir ayar demetidir (seçince alanlar doldurulur, sonra her alan elle değiştirilebilir). Ölçüler: kâğıt ve boşluk mm,
 * yazı pt. Kayıt: localStorage `medsoru_soru_aktar_v1` (yalnız bu cihaz) + adlandırılmış şablonlar.
 */
import type { KaynakId } from './kaynak';

export type Bicim = 'pdf' | 'docx' | 'pptx';
export type Kagit = 'a4' | 'a5' | 'a3' | 'b5' | 'letter';
export type Duzen = 'akis' | 1 | 2 | 4 | 8;
export type TasarimId = 'sinav' | 'modern' | 'sade' | 'kart' | 'defter' | 'kompakt';
export type YaziId = 'sans' | 'serif' | 'kitap' | 'modern' | 'mono';
export type CizgiStil = 'solid' | 'dashed' | 'dotted' | 'double';
export type RenkAlan = 'yok' | 'ders' | 'konu' | 'yil' | 'kaynak' | 'kurul' | 'tur';
export type CozumYeri = 'yok' | 'altinda' | 'sayfaAlti' | 'arkada' | 'sonda';
export type Grupla = 'yok' | 'ders' | 'konu' | 'yil' | 'kaynak' | 'kurul';
export type Sirala = 'kaynak' | 'ders' | 'konu' | 'yil' | 'zorluk' | 'rastgele';

export interface Ayar {
  tasarim: TasarimId;
  bicim: Bicim;
  /* sayfa */
  kagit: Kagit;
  yatay: boolean;
  /** PPTX slayt boyutu: kâğıt oranı ya da ekran oranları */
  slayt: 'genis' | 'standart' | 'kagit';
  duzen: Duzen;
  /** akış düzeninde sütun */
  sutun: 1 | 2;
  kenar: [number, number, number, number];
  kenarKilit: boolean;
  cerceve: boolean;
  cerceveStil: CizgiStil;
  cerceveKalin: number;
  cerceveRenk: string;
  cerceveYaricap: number;
  cerceveIc: number;
  hucreCerceve: boolean;
  hucreAralik: number;
  sutunCizgi: boolean;
  baslikAcik: boolean;
  baslik: string;
  altBaslik: string;
  adSoyad: boolean;
  tarih: boolean;
  baslikHerSayfa: boolean;
  sayfaNo: boolean;
  altMetin: string;
  kapak: boolean;
  filigran: string;
  /* metin */
  yazi: YaziId;
  punto: number;
  satir: number;
  paragraf: number;
  soruArasi: number;
  iki: boolean;
  kokKalin: boolean;
  secenekDuzen: 'alt' | 'iki' | 'yan';
  numara: '1.' | '1)' | 'S1.' | 'Soru 1';
  harf: 'A)' | 'A.' | '(A)' | 'a)';
  metinRenk: string;
  vurgu: string;
  ayirici: 'yok' | CizgiStil;
  yazmaSatiri: number;
  /* renklendirme ve etiketler */
  renkAlan: RenkAlan;
  renkStil: 'serit' | 'etiket' | 'zemin' | 'numara';
  palet: 'canli' | 'pastel' | 'koyu' | 'gri';
  renkOzel: Record<string, string>;
  etiket: { ders: boolean; konu: boolean; yil: boolean; kaynak: boolean; kurul: boolean; zorluk: boolean; tur: boolean };
  etiketYeri: 'ust' | 'alt';
  grupRenkli: boolean;
  /* çözüm */
  dogruIsaret: boolean;
  isaretStil: 'kalin' | 'zemin' | 'tik' | 'daire';
  cozumYeri: CozumYeri;
  cozumIcerik: { harf: boolean; aciklama: boolean; siklar: boolean; kaynak: boolean };
  cevapAnahtari: boolean;
  optik: boolean;
  /** "arkada" çözümde ızgara satırlarını aynalar (çift yüz baskıda kartın arkası önüne denk gelir) */
  arkaAyna: boolean;
  /* sıra */
  grupla: Grupla;
  grupYeniSayfa: boolean;
  sirala: Sirala;
  sikKaristir: boolean;
  numaraBas: number;
  grupNumara: boolean;
  tohum: number;
}

export const KAGIT: Record<Kagit, { ad: string; w: number; h: number }> = {
  a4: { ad: 'A4', w: 210, h: 297 },
  a5: { ad: 'A5', w: 148, h: 210 },
  a3: { ad: 'A3', w: 297, h: 420 },
  b5: { ad: 'B5', w: 176, h: 250 },
  letter: { ad: 'Letter', w: 215.9, h: 279.4 },
};
export const SLAYT: Record<'genis' | 'standart', { ad: string; w: number; h: number }> = {
  genis: { ad: '16:9', w: 338.67, h: 190.5 },
  standart: { ad: '4:3', w: 254, h: 190.5 },
};

/** Yazı tipleri: ekranda/PDF'te yığın, DOCX/PPTX'te ad */
export const YAZI: Record<YaziId, { ad: string; css: string; ofis: string }> = {
  sans: { ad: 'Sans (Arial)', css: "Arial, 'Liberation Sans', Helvetica, 'DejaVu Sans', sans-serif", ofis: 'Arial' },
  serif: { ad: 'Serif (Times)', css: "'Times New Roman', 'Liberation Serif', Times, 'DejaVu Serif', serif", ofis: 'Times New Roman' },
  kitap: { ad: 'Kitap (Georgia)', css: "Georgia, 'Gelasio', 'DejaVu Serif', serif", ofis: 'Georgia' },
  modern: { ad: 'Modern (Calibri)', css: "Calibri, Carlito, 'Segoe UI', 'Noto Sans', 'DejaVu Sans', sans-serif", ofis: 'Calibri' },
  mono: { ad: 'Daktilo (Courier)', css: "'Courier New', 'Liberation Mono', Courier, 'DejaVu Sans Mono', monospace", ofis: 'Courier New' },
};

export const PALETLER: Record<Ayar['palet'], { ad: string; renk: string[] }> = {
  canli: { ad: 'Canlı', renk: ['#2563eb', '#dc2626', '#059669', '#d97706', '#7c3aed', '#db2777', '#0891b2', '#65a30d', '#ea580c', '#4f46e5', '#0d9488', '#be123c'] },
  pastel: { ad: 'Pastel', renk: ['#7aa2e3', '#e88f8f', '#7cc6a4', '#e8b86d', '#b39ddb', '#f0a1c2', '#7ec8d8', '#a9cf76', '#f2a87a', '#9fa8da', '#80cbc4', '#e6a0b0'] },
  koyu: { ad: 'Koyu', renk: ['#1e3a8a', '#7f1d1d', '#064e3b', '#78350f', '#4c1d95', '#831843', '#164e63', '#365314', '#7c2d12', '#312e81', '#134e4a', '#881337'] },
  gri: { ad: 'Gri tonlar', renk: ['#111827', '#4b5563', '#6b7280', '#374151', '#9ca3af', '#1f2937'] },
};

const ORTAK: Ayar = {
  tasarim: 'sinav', bicim: 'pdf', kagit: 'a4', yatay: false, slayt: 'genis', duzen: 'akis', sutun: 2,
  kenar: [15, 14, 15, 14], kenarKilit: false, cerceve: false, cerceveStil: 'solid', cerceveKalin: 0.8, cerceveRenk: '#111827',
  cerceveYaricap: 0, cerceveIc: 4, hucreCerceve: false, hucreAralik: 6, sutunCizgi: true,
  baslikAcik: true, baslik: 'Soru kitapçığı', altBaslik: '', adSoyad: true, tarih: true, baslikHerSayfa: false,
  sayfaNo: true, altMetin: 'MeDSor', kapak: false, filigran: '',
  yazi: 'serif', punto: 10.5, satir: 1.3, paragraf: 2, soruArasi: 6, iki: false, kokKalin: true, secenekDuzen: 'alt',
  numara: '1.', harf: 'A)', metinRenk: '#111827', vurgu: '#1d4ed8', ayirici: 'yok', yazmaSatiri: 0,
  renkAlan: 'yok', renkStil: 'serit', palet: 'canli', renkOzel: {},
  etiket: { ders: false, konu: false, yil: false, kaynak: false, kurul: false, zorluk: false, tur: false }, etiketYeri: 'ust', grupRenkli: true,
  dogruIsaret: false, isaretStil: 'kalin', cozumYeri: 'sonda', cozumIcerik: { harf: true, aciklama: true, siklar: false, kaynak: false },
  cevapAnahtari: true, optik: false, arkaAyna: true,
  grupla: 'yok', grupYeniSayfa: false, sirala: 'kaynak', sikKaristir: false, numaraBas: 1, grupNumara: false, tohum: 1,
};

export interface TasarimTanim { id: TasarimId; ad: string; alt: string; ayar: Partial<Ayar> }
export const TASARIMLAR: TasarimTanim[] = [
  {
    id: 'sinav', ad: 'Sınav kitapçığı', alt: 'İki sütun, serif, ad-soyad alanı, cevap anahtarı sonda',
    ayar: { yazi: 'serif', punto: 10.5, satir: 1.3, duzen: 'akis', sutun: 2, sutunCizgi: true, cerceve: false, hucreCerceve: false, baslikAcik: true, adSoyad: true, tarih: true, numara: '1.', harf: 'A)', kokKalin: true, renkAlan: 'yok', etiket: { ...ORTAK.etiket }, dogruIsaret: false, cozumYeri: 'sonda', cevapAnahtari: true, optik: true, ayirici: 'yok', secenekDuzen: 'alt', vurgu: '#111827', metinRenk: '#111827', yazmaSatiri: 0, kapak: true },
  },
  {
    id: 'modern', ad: 'Modern renkli', alt: 'Derse göre renk şeridi, etiketler, ferah aralık',
    ayar: { yazi: 'modern', punto: 10.5, satir: 1.4, duzen: 'akis', sutun: 1, sutunCizgi: false, cerceve: false, hucreCerceve: false, numara: 'Soru 1', harf: 'A)', kokKalin: true, renkAlan: 'ders', renkStil: 'serit', palet: 'canli', etiket: { ...ORTAK.etiket, ders: true, konu: true, yil: true, tur: true }, ayirici: 'yok', vurgu: '#2563eb', metinRenk: '#1f2937', soruArasi: 7, dogruIsaret: false, cozumYeri: 'sonda', optik: false, kapak: false, yazmaSatiri: 0 },
  },
  {
    id: 'sade', ad: 'Sade (mürekkep dostu)', alt: 'Siyah-beyaz, tek sütun, ince ayraç çizgisi',
    ayar: { yazi: 'sans', punto: 10.5, satir: 1.35, duzen: 'akis', sutun: 1, sutunCizgi: false, cerceve: false, hucreCerceve: false, numara: '1)', harf: 'A)', kokKalin: false, renkAlan: 'yok', etiket: { ...ORTAK.etiket }, ayirici: 'solid', vurgu: '#111827', metinRenk: '#111827', dogruIsaret: false, cozumYeri: 'sonda', optik: false, kapak: false, yazmaSatiri: 0 },
  },
  {
    id: 'kart', ad: 'Kart / tekrar', alt: 'Sayfa başına 4 kutulu kart, çözüm arka sayfada',
    ayar: { yazi: 'modern', punto: 11, satir: 1.35, duzen: 4, cerceve: false, hucreCerceve: true, hucreAralik: 6, numara: 'S1.', harf: 'A)', kokKalin: true, renkAlan: 'konu', renkStil: 'etiket', palet: 'pastel', etiket: { ...ORTAK.etiket, ders: true, konu: true }, ayirici: 'yok', vurgu: '#7c3aed', metinRenk: '#1f2937', dogruIsaret: false, cozumYeri: 'arkada', cozumIcerik: { harf: true, aciklama: true, siklar: true, kaynak: false }, cevapAnahtari: false, optik: false, kapak: false, baslikAcik: false, yazmaSatiri: 0 },
  },
  {
    id: 'defter', ad: 'Çalışma kâğıdı', alt: 'Her sorunun altında not satırları, sayfa çerçevesi',
    ayar: { yazi: 'kitap', punto: 11, satir: 1.45, duzen: 2, cerceve: true, cerceveStil: 'solid', cerceveKalin: 0.8, cerceveYaricap: 3, hucreCerceve: false, numara: 'Soru 1', harf: 'A)', kokKalin: true, renkAlan: 'yok', etiket: { ...ORTAK.etiket, konu: true }, ayirici: 'dashed', vurgu: '#0f766e', metinRenk: '#111827', yazmaSatiri: 4, dogruIsaret: false, cozumYeri: 'sonda', optik: false, kapak: false, baslikAcik: true, adSoyad: true },
  },
  {
    id: 'kompakt', ad: 'Kompakt tekrar', alt: 'Küçük punto, iki sütun, doğru şık işaretli, şıklar yan yana',
    ayar: { yazi: 'sans', punto: 8.5, satir: 1.2, paragraf: 1, soruArasi: 3, duzen: 'akis', sutun: 2, sutunCizgi: true, cerceve: false, hucreCerceve: false, numara: '1.', harf: 'A)', kokKalin: true, secenekDuzen: 'iki', renkAlan: 'ders', renkStil: 'numara', palet: 'koyu', etiket: { ...ORTAK.etiket, yil: true }, ayirici: 'dotted', vurgu: '#b91c1c', metinRenk: '#111827', dogruIsaret: true, isaretStil: 'zemin', cozumYeri: 'yok', cevapAnahtari: false, optik: false, kapak: false, kenar: [10, 10, 10, 10], yazmaSatiri: 0 },
  },
];
export const tasarimUygula = (a: Ayar, id: TasarimId): Ayar => ({ ...a, ...(TASARIMLAR.find((t) => t.id === id)?.ayar || {}), tasarim: id });
export const VARSAYILAN: Ayar = tasarimUygula(ORTAK, 'sinav');

/** Kayıttan gelen ayarı doğrular (eksik alan varsayılandan, bozuk değer atılır) */
export function ayarNormal(raw: any): Ayar {
  const a: any = { ...VARSAYILAN };
  if (raw && typeof raw === 'object') {
    for (const k of Object.keys(VARSAYILAN) as (keyof Ayar)[]) {
      const v = raw[k];
      const d: any = VARSAYILAN[k];
      if (v == null) continue;
      if (Array.isArray(d)) { if (Array.isArray(v) && v.length === d.length && v.every((x: any) => typeof x === 'number')) a[k] = v; }
      else if (typeof d === 'object') { if (typeof v === 'object' && !Array.isArray(v)) a[k] = { ...d, ...v }; }
      else if (typeof v === typeof d || (k === 'duzen' && (v === 'akis' || [1, 2, 4, 8].includes(v)))) a[k] = v;
    }
  }
  a.punto = Math.min(16, Math.max(6, Number(a.punto) || 10.5));
  a.satir = Math.min(2.4, Math.max(1, Number(a.satir) || 1.3));
  a.kenar = a.kenar.map((x: number) => Math.min(40, Math.max(0, x)));
  if (![1, 2].includes(a.sutun)) a.sutun = 1;
  return a as Ayar;
}

/* ---------------------------------------------------------------------------
 * Geometri: sayfa ölçüsü, gövde alanı, ızgara
 * ------------------------------------------------------------------------- */
export const PX_MM = 96 / 25.4;
export const BASLIK_MM = 16;
export const ALT_MM = 7;
export const SERIT_MM = 11;
export const GRUP_MM = 9;

export function sayfaOlcu(a: Ayar): { w: number; h: number } {
  if (a.bicim === 'pptx' && a.slayt !== 'kagit') return { ...SLAYT[a.slayt] };
  const k = KAGIT[a.kagit] || KAGIT.a4;
  return a.yatay ? { w: k.h, h: k.w } : { w: k.w, h: k.h };
}

/** Izgara: hücre sayısı → sütun × satır (yatay sayfada sütun önceliği) */
export function izgara(a: Ayar, n: 1 | 2 | 4 | 8): { sut: number; sat: number } {
  const { w, h } = sayfaOlcu(a);
  const genis = w > h;
  if (n === 1) return { sut: 1, sat: 1 };
  if (n === 2) return genis ? { sut: 2, sat: 1 } : { sut: 1, sat: 2 };
  if (n === 4) return { sut: 2, sat: 2 };
  return genis ? { sut: 4, sat: 2 } : { sut: 2, sat: 4 };
}

export interface Govde {
  w: number; h: number;
  /** sayfa başlığı bu sayfada var mı */
  baslik: boolean;
}
/** Sayfanın içerik alanı (mm): kenar − çerçeve iç boşluğu − başlık − alt bilgi − cevap şeridi − grup bandı */
export function govde(a: Ayar, o: { ilk: boolean; serit: boolean; grup: boolean }): Govde {
  const { w, h } = sayfaOlcu(a);
  const ic = a.cerceve ? a.cerceveIc + a.cerceveKalin * 0.35 : 0;
  const baslik = a.baslikAcik && (o.ilk || a.baslikHerSayfa);
  const altVar = a.sayfaNo || !!a.altMetin.trim();
  const gw = w - a.kenar[1] - a.kenar[3] - ic * 2;
  const gh = h - a.kenar[0] - a.kenar[2] - ic * 2 - (baslik ? BASLIK_MM : 0) - (altVar ? ALT_MM : 0) - (o.serit ? SERIT_MM : 0) - (o.grup ? GRUP_MM : 0);
  return { w: Math.max(20, gw), h: Math.max(20, gh), baslik };
}

/** Kararlı karıştırma (tohumlu): aynı tohum aynı sırayı verir, önizleme ile indirilen belge eşleşir */
export function karistir<T>(arr: T[], tohum: number): T[] {
  let x = (tohum * 2654435761) >>> 0 || 1;
  const r = () => ((x ^= x << 13), (x ^= x >>> 17), (x ^= x << 5), (x >>> 0) / 4294967296);
  const out = [...arr];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(r() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}
export const kaynakSirasi: KaynakId[] = ['cikmis', 'ornek', 'cozucu', 'hoca', 'hocaara', 'calisma', 'mini', 'havuz'];
