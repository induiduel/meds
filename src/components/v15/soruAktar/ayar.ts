/**
 * Soru dışa aktarıcı · belge ayarları. Tek ayar nesnesi üç biçimi (PDF, DOCX, PPTX) aynı anda yönetir; tasarım modu
 * bir ayar demetidir (seçince alanlar doldurulur, sonra her alan elle değiştirilebilir). Ölçüler: kâğıt ve boşluk mm,
 * yazı pt. Kayıt: localStorage `medsoru_soru_aktar_v1` (yalnız bu cihaz) + adlandırılmış şablonlar.
 */
import type { KaynakId } from './kaynak';
import { disciplineKey, type DisciplineKey } from '../../../utils/discipline';

export type Bicim = 'pdf' | 'docx' | 'pptx';
export type Kagit = 'a4' | 'a5' | 'a3' | 'b5' | 'letter';
export type Duzen = 'akis' | 1 | 2 | 4 | 8;
export type TasarimId = 'sinav' | 'modern' | 'sade' | 'kart' | 'defter' | 'kompakt' | 'akademik' | 'kesilir';
export type YaziId =
  | 'sans' | 'serif' | 'kitap' | 'modern' | 'mono'
  | 'inter' | 'roboto' | 'opensans' | 'lato' | 'montserrat' | 'poppins' | 'nunito' | 'firasans' | 'notosans' | 'sourcesans' | 'plexsans' | 'lexend' | 'atkinson' | 'dmsans' | 'manrope' | 'raleway' | 'ubuntu' | 'ptsans'
  | 'sourceserif' | 'merriweather' | 'lora' | 'literata' | 'ebgaramond' | 'crimson' | 'playfair' | 'spectral' | 'librebask' | 'ptserif' | 'notoserif' | 'plexserif' | 'newsreader' | 'vollkorn' | 'alegreya' | 'cormorant'
  | 'plexmono' | 'jetbrains' | 'firamono' | 'sourcecode';
/** Yazı stili: kalınlık, harf aralığı ve başlık yazısı için ayrı seçimler */
export type Agirlik = 300 | 400 | 500 | 600 | 700 | 800;
export type BaslikYazi = 'ayni' | YaziId;
export type MetinStil = 'normal' | 'kalin' | 'italik' | 'kalinItalik';
export type HarfBuyuk = 'normal' | 'buyuk' | 'kucukBuyuk';
export type NumaraStil = 'duz' | 'kalin' | 'kutu' | 'daire' | 'altCizgi';
export type SikHarfStil = 'kalin' | 'normal' | 'daire' | 'kutu';
/** Belgenin öge renkleri (renk teması tek seferde doldurur, her biri elle değiştirilebilir) */
export type RenkOge =
  | 'sayfaZemin' | 'baslik' | 'baslikCizgi' | 'altBilgi' | 'bant' | 'grup'
  | 'numara' | 'kok' | 'sik' | 'sikHarf' | 'dogru' | 'dogruZemin'
  | 'cozumZemin' | 'cozumKenar' | 'cozumMetin' | 'cevapHarfi' | 'kaynak'
  | 'ayirici' | 'sutunCizgi' | 'hucreKenar' | 'yazmaCizgi' | 'anahtarKenar' | 'filigran' | 'kapakBaslik'
  | 'baslikZemin' | 'kutuKenar' | 'kutuZemin' | 'desen' | 'notCizgi' | 'kesim'
  /* 2026-11-13: ayrı ayrı değiştirilebilen eksik ögeler (başlık alt yazısı, kapak parçaları, etiket, anahtar zemini, optik) */
  | 'baslikAlt' | 'grupSayi' | 'kapakUst' | 'kapakSayi' | 'kapakAlt' | 'kapakNot' | 'kapakZemin'
  | 'etiket' | 'anahtarZemin' | 'optik';
export type Renkler = Record<RenkOge, string>;
export type TemaId = 'klasik' | 'lacivert' | 'bordo' | 'orman' | 'mor' | 'turuncu' | 'okyanus' | 'sepya' | 'gri' | 'pembe' | 'gece' | 'kahve' | 'zeytin' | 'mavi-gri' | 'ozel';
export type CizgiStil = 'solid' | 'dashed' | 'dotted' | 'double';
/** Soruyu sınıflandıran alanlar: gruplama katmanı, renk anahtarı ve etiket aynı listeden seçilir */
export type Alan = 'yil' | 'kurul' | 'ders' | 'konu' | 'kaynak' | 'tur' | 'zorluk' | 'etiket';
export const ALANLAR: { id: Alan; ad: string; alt: string }[] = [
  { id: 'yil', ad: 'Yıl', alt: 'Sınav yılı (yeni önce)' },
  { id: 'kurul', ad: 'Kurul', alt: 'Kurul 1 … 6' },
  { id: 'ders', ad: 'Ders', alt: 'Branş / ders adı' },
  { id: 'konu', ad: 'Konu', alt: 'Ders başlığı / konu' },
  { id: 'kaynak', ad: 'Kaynak', alt: 'Çıkmış, örnek, çözücü …' },
  { id: 'tur', ad: 'Soru türü', alt: 'Çıkmış, benzer, hoca üslubu …' },
  { id: 'zorluk', ad: 'Zorluk', alt: 'Kolay, orta, zor' },
  { id: 'etiket', ad: 'Etiket', alt: 'Sorunun etiketi (birden çoksa en yaygını)' },
];
export const alanAdi = (id: Alan) => ALANLAR.find((x) => x.id === id)?.ad || id;
export type RenkAlan = 'yok' | Alan;
export type CozumYeri = 'yok' | 'altinda' | 'sayfaAlti' | 'arkada' | 'sonda';
export type Sirala = 'kaynak' | 'ders' | 'konu' | 'yil' | 'yilEski' | 'zorluk' | 'zorlukZor' | 'numara' | 'kisa' | 'uzun' | 'alfabetik' | 'rastgele';
export const SIRALAMALAR: { id: Sirala; ad: string }[] = [
  { id: 'kaynak', ad: 'Kaynak sırası' },
  { id: 'ders', ad: 'Derse göre (A→Z)' },
  { id: 'konu', ad: 'Konuya göre (A→Z)' },
  { id: 'yil', ad: 'Yıla göre (yeni önce)' },
  { id: 'yilEski', ad: 'Yıla göre (eski önce)' },
  { id: 'zorluk', ad: 'Zorluğa göre (kolaydan)' },
  { id: 'zorlukZor', ad: 'Zorluğa göre (zordan)' },
  { id: 'numara', ad: 'Kaynaktaki soru numarası' },
  { id: 'kisa', ad: 'Kısadan uzuna' },
  { id: 'uzun', ad: 'Uzundan kısaya' },
  { id: 'alfabetik', ad: 'Soru metni (A→Z)' },
  { id: 'rastgele', ad: 'Rastgele' },
];
/** Grupların kendi aralarındaki sırası: olağan (yıl yeni önce, kurul numarası, zorluk kolaydan, ad) ya da soru sayısı */
export type GrupSirasi = 'olagan' | 'sayiAzalan' | 'sayiArtan';
/** Grup başlığı biçimi */
export type GrupStil = 'cizgi' | 'bant' | 'kutu' | 'sade';
/** Sayfaya sığdır: kapalı · yalnız küçült (seyrek son sayfayı kaldırır) · doldur (küçült ya da büyüt, sayfalar dolsun) */
export type Sigdir = 'yok' | 'kucult' | 'doldur';
export type PaletId = 'canli' | 'pastel' | 'koyu' | 'gri' | 'sicak' | 'soguk' | 'toprak' | 'neon' | 'maviTon' | 'yesilTon' | 'morTon' | 'bordoTon' | 'gokkusagi' | 'ofis' | 'ozel';
export type EtiketSekil = 'hap' | 'kutu' | 'kose' | 'cizgi' | 'duz';
export type EtiketRenk = 'gri' | 'alan' | 'ders' | 'ozel';
export type EtiketDizilim = 'sol' | 'sag' | 'orta' | 'dikey';
/** Yaprak düzeni (PDF/yazdırma): tek sayfa · yaprakta 2 sayfa · katlanır kitapçık (sayfa sırası baskıya göre dizilir) */
export type Yaprak = 'tek' | 'iki' | 'kitapcik';
export type BaslikStil = 'cizgi' | 'bant' | 'kutu' | 'sade';
export type SoruKutu = 'yok' | 'cizgi' | 'zemin' | 'golge';
export type CozumStil = 'bant' | 'kutu' | 'zemin' | 'sade';
export type Desen = 'yok' | 'cizgili' | 'kareli' | 'noktali';
export type SayfaNoBicim = 'bolme' | 'duz' | 'sayfa' | 'tire';
export type KapakStil = 'sade' | 'bant' | 'zemin';
/** Hangi sayfalar dışa aktarılır: hepsi · yalnız soru sayfaları (öğrenci kopyası) · yalnız çözüm + cevap anahtarı (öğretmen kopyası) */
export type Cikti = 'hepsi' | 'sorular' | 'cozumler';
export const EN_COK_GRUP = 4;
/** Logo veri adresi için üst sınır (localStorage'da saklanır) */
export const LOGO_EN_COK = 160 * 1024;

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
  /* sayfa tasarımı (2026-11-09) */
  /** yaprak düzeni: PDF ve yazdırmada; Office belgeleri tek sayfa kipinde kalır */
  yaprak: Yaprak;
  /** çift yüz baskı: sol kenar cilt payı (iç kenar) olur, çift sayfalarda sağa geçer; kapak varsa ardına boş sayfa gelir */
  ciftYuz: boolean;
  /** ızgarada hücreler arası kesik kesim çizgileri (kart kesmek için) */
  kesimCizgi: boolean;
  baslikStil: BaslikStil;
  baslikHiza: 'sol' | 'orta';
  /** logo (data: adresi, PNG/JPEG; yalnız PDF ve yazdırma) */
  logo: string;
  logoYer: 'baslik' | 'kapak' | 'ikisi';
  /** logo yüksekliği (mm) */
  logoYuk: number;
  /** alt bilgi orta ve sağ bölge; `altMetin` sol bölge. Yer tutucular: {sayfa} {toplam} {tarih} {baslik} {altbaslik} {soru} */
  altOrta: string;
  altSag: string;
  sayfaNoYer: 'sol' | 'orta' | 'sag';
  sayfaNoBicim: SayfaNoBicim;
  /** alt bilgi üstünde ince çizgi */
  altCizgi: boolean;
  /** sayfa zemin deseni (çizgili / kareli / noktalı defter kâğıdı) */
  desen: Desen;
  /** her sayfanın altında not alanı (mm; 0 = yok) */
  notAlani: number;
  kapakStil: KapakStil;
  /** kapakta serbest not (yönerge, sınav bilgisi) */
  kapakNot: string;
  /* soru bloğu tasarımı */
  soruKutu: SoruKutu;
  /** kutuların köşe yarıçapı (mm): soru kutusu, çözüm kutusu, hücre çerçevesi */
  kutuYaricap: number;
  /** soru kutusu iç boşluğu (mm) */
  kutuIc: number;
  /** şıklar soru kökünün metin hizasından başlar (numara dışarıda asılı) */
  asiliGirinti: boolean;
  /** şıklar arası boşluk (pt) */
  sikAralik: number;
  /** şık puntosu (gövde puntosuna oran) */
  sikOran: number;
  cozumStil: CozumStil;
  /* dışa aktarım */
  cikti: Cikti;
  /** sayfa aralığı, ör. "1-4, 7" (boş = tümü); kapak 0 sayılır */
  sayfaAralik: string;
  /** belge CSS'ine eklenen özel kurallar (ileri düzey; önizleme ve PDF'te uygulanır) */
  ozelCss: string;
  /* metin */
  yazi: YaziId;
  /** başlık, grup ve kapak yazısı ('ayni' = gövde yazısı) */
  yaziBaslik: BaslikYazi;
  /** gövde kalınlığı (değişken yazı tiplerinde 300–700) */
  agirlik: Agirlik;
  baslikAgirlik: Agirlik;
  /** harf aralığı (em) */
  harfAralik: number;
  kokStil: MetinStil;
  sikStil: MetinStil;
  baslikBuyuk: HarfBuyuk;
  grupBuyuk: HarfBuyuk;
  numaraStil: NumaraStil;
  sikHarfStil: SikHarfStil;
  /** başlık puntosu (gövde puntosuna oran) */
  baslikOran: number;
  /** şıkların girintisi (mm) */
  sikGirinti: number;
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
  /** renk teması ve öge renkleri (kural: ogeRenk(a, 'numara') boşsa vurgu/metin türetir) */
  tema: TemaId;
  renkler: Partial<Renkler>;
  /** renk anahtarı için kullanıcının kendi paleti (palet: 'ozel') */
  paletOzel: string[];
  ayirici: 'yok' | CizgiStil;
  yazmaSatiri: number;
  /* renklendirme ve etiketler */
  renkAlan: RenkAlan;
  renkStil: 'serit' | 'etiket' | 'zemin' | 'numara';
  palet: PaletId;
  renkOzel: Record<string, string>;
  /** Ders renk anahtarında sitedeki sabit ders renkleri (Patoloji pembe, Farmakoloji mor …); kapalıysa palet sırası */
  dersRenkleri: boolean;
  etiket: { ders: boolean; konu: boolean; yil: boolean; kaynak: boolean; kurul: boolean; zorluk: boolean; tur: boolean; etiket: boolean };
  etiketYeri: 'ust' | 'alt';
  /** etiket yazı boyutu (soru puntosuna oran) */
  etiketBoyut: number;
  etiketDizilim: EtiketDizilim;
  etiketSekil: EtiketSekil;
  etiketRenk: EtiketRenk;
  etiketZemin: string;
  etiketMetin: string;
  etiketKalin: boolean;
  grupRenkli: boolean;
  /* çözüm */
  dogruIsaret: boolean;
  isaretStil: 'kalin' | 'zemin' | 'tik' | 'daire';
  cozumYeri: CozumYeri;
  cozumIcerik: { harf: boolean; aciklama: boolean; siklar: boolean; kaynak: boolean; yalnizDogru: boolean };
  cevapAnahtari: boolean;
  optik: boolean;
  /** "arkada" çözümde ızgara satırlarını aynalar (çift yüz baskıda kartın arkası önüne denk gelir) */
  arkaAyna: boolean;
  /* sıra ve gruplama */
  /** iç içe gruplama katmanları: ilk öğe en üst grup (ör. ['yil','kurul','ders','konu']); boşsa gruplama yok */
  gruplar: Alan[];
  grupSirasi: GrupSirasi;
  grupStil: GrupStil;
  /** başlıkta soru sayısı: "Patoloji (12)" */
  grupSayi: boolean;
  grupYeniSayfa: boolean;
  sirala: Sirala;
  sikKaristir: boolean;
  numaraBas: number;
  grupNumara: boolean;
  tohum: number;
  /* sayfaya sığdır */
  sigdir: Sigdir;
  /** hedef sayfa sayısı (0 = kendiliğinden: seyrek son sayfa kaldırılır) */
  sigdirHedef: number;
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

/** Yazı tipleri: ekranda/PDF'te yığın, DOCX/PPTX'te ad; `g` Google Fonts ailesi (önizleme + sunucu PDF'i yükler), `tur` gruplama */
export interface YaziTanim { ad: string; css: string; ofis: string; g?: string; tur: 'sans' | 'serif' | 'mono'; alt?: string }
export const YAZI: Record<YaziId, YaziTanim> = {
  sans: { ad: 'Arial', alt: 'Sistem · her yerde var', css: "Arial, 'Liberation Sans', Helvetica, 'DejaVu Sans', sans-serif", ofis: 'Arial', tur: 'sans' },
  modern: { ad: 'Calibri', alt: 'Sistem · Office varsayılanı', css: "Calibri, Carlito, 'Segoe UI', 'Noto Sans', 'DejaVu Sans', sans-serif", ofis: 'Calibri', tur: 'sans' },
  inter: { ad: 'Inter', alt: 'Nötr, ekran', css: "Inter, system-ui, sans-serif", ofis: 'Inter', g: 'Inter:wght@300;400;500;600;700;800', tur: 'sans' },
  roboto: { ad: 'Roboto', alt: 'Android · okunaklı', css: "Roboto, 'Noto Sans', sans-serif", ofis: 'Roboto', g: 'Roboto:wght@300;400;500;700;900', tur: 'sans' },
  opensans: { ad: 'Open Sans', alt: 'Geniş, dost', css: "'Open Sans', sans-serif", ofis: 'Open Sans', g: 'Open+Sans:wght@300;400;500;600;700;800', tur: 'sans' },
  lato: { ad: 'Lato', alt: 'Yumuşak, sıcak', css: "Lato, sans-serif", ofis: 'Lato', g: 'Lato:wght@300;400;700;900', tur: 'sans' },
  montserrat: { ad: 'Montserrat', alt: 'Geometrik başlıklar', css: "Montserrat, sans-serif", ofis: 'Montserrat', g: 'Montserrat:wght@300;400;500;600;700;800', tur: 'sans' },
  poppins: { ad: 'Poppins', alt: 'Yuvarlak, modern', css: "Poppins, sans-serif", ofis: 'Poppins', g: 'Poppins:wght@300;400;500;600;700;800', tur: 'sans' },
  nunito: { ad: 'Nunito', alt: 'Yuvarlak, sıcak', css: "Nunito, sans-serif", ofis: 'Nunito', g: 'Nunito:wght@300;400;500;600;700;800', tur: 'sans' },
  firasans: { ad: 'Fira Sans', alt: 'Hümanist, teknik', css: "'Fira Sans', sans-serif", ofis: 'Fira Sans', g: 'Fira+Sans:wght@300;400;500;600;700;800', tur: 'sans' },
  notosans: { ad: 'Noto Sans', alt: 'Tüm harfler, Türkçe tam', css: "'Noto Sans', sans-serif", ofis: 'Noto Sans', g: 'Noto+Sans:wght@300;400;500;600;700;800', tur: 'sans' },
  sourcesans: { ad: 'Source Sans 3', alt: 'Sade, dar', css: "'Source Sans 3', sans-serif", ofis: 'Source Sans 3', g: 'Source+Sans+3:wght@300;400;500;600;700;800', tur: 'sans' },
  plexsans: { ad: 'IBM Plex Sans', alt: 'Teknik, tablolar', css: "'IBM Plex Sans', sans-serif", ofis: 'IBM Plex Sans', g: 'IBM+Plex+Sans:wght@300;400;500;600;700', tur: 'sans' },
  lexend: { ad: 'Lexend', alt: 'Okuma güçlüğüne uygun', css: "Lexend, sans-serif", ofis: 'Lexend', g: 'Lexend:wght@300;400;500;600;700;800', tur: 'sans' },
  atkinson: { ad: 'Atkinson Hyperlegible', alt: 'Az görme · ayırt edici', css: "'Atkinson Hyperlegible', sans-serif", ofis: 'Atkinson Hyperlegible', g: 'Atkinson+Hyperlegible:wght@400;700', tur: 'sans' },
  dmsans: { ad: 'DM Sans', alt: 'Düşük kontrast, ferah', css: "'DM Sans', sans-serif", ofis: 'DM Sans', g: 'DM+Sans:wght@300;400;500;600;700;800', tur: 'sans' },
  manrope: { ad: 'Manrope', alt: 'Modern, net', css: "Manrope, sans-serif", ofis: 'Manrope', g: 'Manrope:wght@300;400;500;600;700;800', tur: 'sans' },
  raleway: { ad: 'Raleway', alt: 'Zarif, ince', css: "Raleway, sans-serif", ofis: 'Raleway', g: 'Raleway:wght@300;400;500;600;700;800', tur: 'sans' },
  ubuntu: { ad: 'Ubuntu', alt: 'Yuvarlak, teknik', css: "Ubuntu, sans-serif", ofis: 'Ubuntu', g: 'Ubuntu:wght@300;400;500;700', tur: 'sans' },
  ptsans: { ad: 'PT Sans', alt: 'Dar, çok metin', css: "'PT Sans', sans-serif", ofis: 'PT Sans', g: 'PT+Sans:wght@400;700', tur: 'sans' },
  serif: { ad: 'Times New Roman', alt: 'Sistem · klasik sınav', css: "'Times New Roman', 'Liberation Serif', Times, 'DejaVu Serif', serif", ofis: 'Times New Roman', tur: 'serif' },
  kitap: { ad: 'Georgia', alt: 'Sistem · kitap', css: "Georgia, 'Gelasio', 'DejaVu Serif', serif", ofis: 'Georgia', tur: 'serif' },
  sourceserif: { ad: 'Source Serif 4', alt: 'Uzun metin', css: "'Source Serif 4', Georgia, serif", ofis: 'Source Serif 4', g: 'Source+Serif+4:opsz,wght@8..60,300;8..60,400;8..60,500;8..60,600;8..60,700', tur: 'serif' },
  merriweather: { ad: 'Merriweather', alt: 'Küçük punto, rahat', css: "Merriweather, Georgia, serif", ofis: 'Merriweather', g: 'Merriweather:wght@300;400;700;900', tur: 'serif' },
  lora: { ad: 'Lora', alt: 'Notlar, yumuşak', css: "Lora, Georgia, serif", ofis: 'Lora', g: 'Lora:wght@400;500;600;700', tur: 'serif' },
  literata: { ad: 'Literata', alt: 'E-kitap', css: "Literata, Georgia, serif", ofis: 'Literata', g: 'Literata:opsz,wght@7..72,300;7..72,400;7..72,500;7..72,600;7..72,700', tur: 'serif' },
  ebgaramond: { ad: 'EB Garamond', alt: 'Klasik kitap', css: "'EB Garamond', Garamond, Georgia, serif", ofis: 'EB Garamond', g: 'EB+Garamond:wght@400;500;600;700;800', tur: 'serif' },
  crimson: { ad: 'Crimson Pro', alt: 'Akademik', css: "'Crimson Pro', Georgia, serif", ofis: 'Crimson Pro', g: 'Crimson+Pro:wght@300;400;500;600;700;800', tur: 'serif' },
  playfair: { ad: 'Playfair Display', alt: 'Şık başlıklar', css: "'Playfair Display', Georgia, serif", ofis: 'Playfair Display', g: 'Playfair+Display:wght@400;500;600;700;800', tur: 'serif' },
  spectral: { ad: 'Spectral', alt: 'Ekran serifi', css: "Spectral, Georgia, serif", ofis: 'Spectral', g: 'Spectral:wght@300;400;500;600;700;800', tur: 'serif' },
  librebask: { ad: 'Libre Baskerville', alt: 'Geleneksel', css: "'Libre Baskerville', Georgia, serif", ofis: 'Libre Baskerville', g: 'Libre+Baskerville:wght@400;700', tur: 'serif' },
  ptserif: { ad: 'PT Serif', alt: 'Dar, çok metin', css: "'PT Serif', Georgia, serif", ofis: 'PT Serif', g: 'PT+Serif:wght@400;700', tur: 'serif' },
  notoserif: { ad: 'Noto Serif', alt: 'Tüm harfler, Türkçe tam', css: "'Noto Serif', Georgia, serif", ofis: 'Noto Serif', g: 'Noto+Serif:wght@300;400;500;600;700;800', tur: 'serif' },
  plexserif: { ad: 'IBM Plex Serif', alt: 'Teknik serif', css: "'IBM Plex Serif', Georgia, serif", ofis: 'IBM Plex Serif', g: 'IBM+Plex+Serif:wght@300;400;500;600;700', tur: 'serif' },
  newsreader: { ad: 'Newsreader', alt: 'Gazete, okuma', css: "Newsreader, Georgia, serif", ofis: 'Newsreader', g: 'Newsreader:opsz,wght@6..72,300;6..72,400;6..72,500;6..72,600;6..72,700;6..72,800', tur: 'serif' },
  vollkorn: { ad: 'Vollkorn', alt: 'Kalın, koyu', css: "Vollkorn, Georgia, serif", ofis: 'Vollkorn', g: 'Vollkorn:wght@400;500;600;700;800', tur: 'serif' },
  alegreya: { ad: 'Alegreya', alt: 'Edebî, canlı', css: "Alegreya, Georgia, serif", ofis: 'Alegreya', g: 'Alegreya:wght@400;500;600;700;800', tur: 'serif' },
  cormorant: { ad: 'Cormorant Garamond', alt: 'Çok zarif, büyük punto', css: "'Cormorant Garamond', Garamond, serif", ofis: 'Cormorant Garamond', g: 'Cormorant+Garamond:wght@300;400;500;600;700', tur: 'serif' },
  mono: { ad: 'Courier New', alt: 'Sistem · daktilo', css: "'Courier New', 'Liberation Mono', Courier, 'DejaVu Sans Mono', monospace", ofis: 'Courier New', tur: 'mono' },
  plexmono: { ad: 'IBM Plex Mono', alt: 'Kod, değer', css: "'IBM Plex Mono', monospace", ofis: 'IBM Plex Mono', g: 'IBM+Plex+Mono:wght@300;400;500;600;700', tur: 'mono' },
  jetbrains: { ad: 'JetBrains Mono', alt: 'Kod, net', css: "'JetBrains Mono', monospace", ofis: 'JetBrains Mono', g: 'JetBrains+Mono:wght@300;400;500;600;700;800', tur: 'mono' },
  firamono: { ad: 'Fira Mono', alt: 'Kod, yumuşak', css: "'Fira Mono', monospace", ofis: 'Fira Mono', g: 'Fira+Mono:wght@400;500;700', tur: 'mono' },
  sourcecode: { ad: 'Source Code Pro', alt: 'Kod, dar', css: "'Source Code Pro', monospace", ofis: 'Source Code Pro', g: 'Source+Code+Pro:wght@300;400;500;600;700;800', tur: 'mono' },
};
export const YAZI_TUR_AD: Record<YaziTanim['tur'], string> = { sans: 'Düz (sans)', serif: 'Tırnaklı (serif)', mono: 'Eş aralıklı' };
export const yaziTanim = (id: YaziId | BaslikYazi, a?: Ayar): YaziTanim => YAZI[(id === 'ayni' ? (a?.yazi || 'sans') : id) as YaziId] || YAZI.sans;
export const baslikYazi = (a: Ayar): YaziTanim => yaziTanim(a.yaziBaslik === 'ayni' ? a.yazi : a.yaziBaslik);
/** Belgede kullanılan Google Fonts bağlantıları (önizleme, ölçüm çerçevesi ve sunucu PDF'i aynı adresleri yükler) */
export function yaziBaglantilari(a: Ayar): string[] {
  const ids = new Set<YaziId>([a.yazi, ...(a.yaziBaslik !== 'ayni' ? [a.yaziBaslik] : [])]);
  return [...ids].map((id) => YAZI[id]?.g).filter((g): g is string => !!g).map((g) => `https://fonts.googleapis.com/css2?family=${g}&display=swap`);
}
export const AGIRLIKLAR: { v: Agirlik; ad: string }[] = [{ v: 300, ad: 'İnce' }, { v: 400, ad: 'Normal' }, { v: 500, ad: 'Orta' }, { v: 600, ad: 'Yarı kalın' }, { v: 700, ad: 'Kalın' }, { v: 800, ad: 'Çok kalın' }];
export const stilCss = (st: MetinStil) => `${st === 'kalin' || st === 'kalinItalik' ? 'font-weight:700;' : ''}${st === 'italik' || st === 'kalinItalik' ? 'font-style:italic;' : ''}`;
export const buyukCss = (b: HarfBuyuk) => (b === 'buyuk' ? 'text-transform:uppercase;letter-spacing:.06em;' : b === 'kucukBuyuk' ? 'font-variant-caps:small-caps;letter-spacing:.03em;' : '');

/* ---------------------------------------------------------------------------
 * Renk temaları: belgenin öge renkleri bir demet; seçince renkler dolar, her biri elle değiştirilebilir
 * ------------------------------------------------------------------------- */
export const RENK_OGELERI: { id: RenkOge; ad: string; grup: 'sayfa' | 'metin' | 'cevap' | 'cizgi' }[] = [
  { id: 'sayfaZemin', ad: 'Sayfa zemini', grup: 'sayfa' },
  { id: 'baslik', ad: 'Sayfa başlığı', grup: 'sayfa' },
  { id: 'baslikCizgi', ad: 'Başlık çizgisi', grup: 'sayfa' },
  { id: 'baslikAlt', ad: 'Başlık alt yazısı', grup: 'sayfa' },
  { id: 'altBilgi', ad: 'Alt bilgi', grup: 'sayfa' },
  { id: 'bant', ad: 'Bölüm bandı', grup: 'sayfa' },
  { id: 'grup', ad: 'Grup başlıkları', grup: 'sayfa' },
  { id: 'grupSayi', ad: 'Grup soru sayısı', grup: 'sayfa' },
  { id: 'etiket', ad: 'Etiket rengi', grup: 'sayfa' },
  { id: 'kapakBaslik', ad: 'Kapak başlığı', grup: 'sayfa' },
  { id: 'kapakAlt', ad: 'Kapak alt başlığı', grup: 'sayfa' },
  { id: 'kapakUst', ad: 'Kapak üst yazısı', grup: 'sayfa' },
  { id: 'kapakSayi', ad: 'Kapak sayıları', grup: 'sayfa' },
  { id: 'kapakNot', ad: 'Kapak notu', grup: 'sayfa' },
  { id: 'kapakZemin', ad: 'Kapak zemini / yan bandı', grup: 'sayfa' },
  { id: 'baslikZemin', ad: 'Başlık bandı zemini', grup: 'sayfa' },
  { id: 'filigran', ad: 'Filigran', grup: 'sayfa' },
  { id: 'desen', ad: 'Zemin deseni', grup: 'sayfa' },
  { id: 'anahtarZemin', ad: 'Cevap anahtarı zemini', grup: 'sayfa' },
  { id: 'optik', ad: 'Optik form (daire ve çizgi)', grup: 'sayfa' },
  { id: 'numara', ad: 'Soru numarası', grup: 'metin' },
  { id: 'kok', ad: 'Soru kökü', grup: 'metin' },
  { id: 'sik', ad: 'Şık metni', grup: 'metin' },
  { id: 'sikHarf', ad: 'Şık harfi', grup: 'metin' },
  { id: 'kaynak', ad: 'Kaynak satırı', grup: 'metin' },
  { id: 'dogru', ad: 'Doğru şık', grup: 'cevap' },
  { id: 'dogruZemin', ad: 'Doğru şık zemini', grup: 'cevap' },
  { id: 'cevapHarfi', ad: '"Cevap: A" yazısı', grup: 'cevap' },
  { id: 'cozumZemin', ad: 'Çözüm kutusu zemini', grup: 'cevap' },
  { id: 'cozumKenar', ad: 'Çözüm kutusu kenarı', grup: 'cevap' },
  { id: 'cozumMetin', ad: 'Çözüm metni', grup: 'cevap' },
  { id: 'anahtarKenar', ad: 'Cevap anahtarı kenarı', grup: 'cevap' },
  { id: 'ayirici', ad: 'Sorular arası çizgi', grup: 'cizgi' },
  { id: 'sutunCizgi', ad: 'Sütun çizgisi', grup: 'cizgi' },
  { id: 'hucreKenar', ad: 'Hücre kenarı', grup: 'cizgi' },
  { id: 'yazmaCizgi', ad: 'Yazma satırı', grup: 'cizgi' },
  { id: 'kutuKenar', ad: 'Soru kutusu kenarı', grup: 'cizgi' },
  { id: 'kutuZemin', ad: 'Soru kutusu zemini', grup: 'cizgi' },
  { id: 'notCizgi', ad: 'Not alanı çizgisi', grup: 'cizgi' },
  { id: 'kesim', ad: 'Kesim çizgisi', grup: 'cizgi' },
];
export const RENK_GRUP_AD: Record<'sayfa' | 'metin' | 'cevap' | 'cizgi', string> = { sayfa: 'Sayfa ve başlıklar', metin: 'Soru metni', cevap: 'Cevap ve çözüm', cizgi: 'Çizgiler ve kenarlar' };

/** Tema: vurgu + metin + ögeler. Boş bırakılan öge `ogeRenk` ile türetilir */
export interface TemaTanim { id: TemaId; ad: string; alt: string; vurgu: string; metin: string; renkler: Partial<Renkler> }
const temaKur = (id: TemaId, ad: string, alt: string, vurgu: string, metin: string, r: Partial<Renkler> = {}): TemaTanim => ({ id, ad, alt, vurgu, metin, renkler: r });
export const TEMALAR: TemaTanim[] = [
  temaKur('klasik', 'Klasik', 'Siyah metin, lacivert vurgu', '#1d4ed8', '#111827'),
  temaKur('lacivert', 'Lacivert', 'Koyu mavi başlık ve numaralar', '#1e3a8a', '#0f172a', { numara: '#1e40af', dogru: '#1d4ed8', cozumZemin: '#eef2ff', cozumKenar: '#3730a3' }),
  temaKur('bordo', 'Bordo', 'Sıcak kırmızı vurgu', '#9f1239', '#1c1917', { numara: '#be123c', dogru: '#be123c', cozumZemin: '#fff1f2', cozumKenar: '#9f1239', baslikCizgi: '#9f1239' }),
  temaKur('orman', 'Orman', 'Yeşil tonları', '#166534', '#14532d', { numara: '#15803d', dogru: '#15803d', cozumZemin: '#f0fdf4', cozumKenar: '#166534', altBilgi: '#4d7c0f' }),
  temaKur('mor', 'Mor', 'Menekşe vurgu', '#6d28d9', '#1e1b4b', { numara: '#7c3aed', dogru: '#7c3aed', cozumZemin: '#f5f3ff', cozumKenar: '#6d28d9' }),
  temaKur('turuncu', 'Turuncu', 'Enerjik turuncu, koyu kahve metin', '#c2410c', '#292524', { numara: '#ea580c', dogru: '#c2410c', cozumZemin: '#fff7ed', cozumKenar: '#ea580c' }),
  temaKur('okyanus', 'Okyanus', 'Turkuaz ve petrol', '#0e7490', '#0f172a', { numara: '#0891b2', dogru: '#0e7490', cozumZemin: '#ecfeff', cozumKenar: '#0e7490', bant: '#155e75' }),
  temaKur('sepya', 'Sepya', 'Krem sayfa, kahve metin', '#78350f', '#3f2a14', { sayfaZemin: '#fbf6ec', numara: '#92400e', dogru: '#92400e', cozumZemin: '#f5ecd9', cozumKenar: '#a16207', altBilgi: '#8b6b3a', ayirici: '#d6c5a3' }),
  temaKur('gri', 'Gri tonlar', 'Mürekkep dostu, renksiz', '#1f2937', '#111827', { numara: '#374151', dogru: '#111827', dogruZemin: '#e5e7eb', cozumZemin: '#f3f4f6', cozumKenar: '#6b7280', baslikCizgi: '#374151' }),
  temaKur('pembe', 'Pembe', 'Fuşya vurgu', '#be185d', '#1f2937', { numara: '#db2777', dogru: '#be185d', cozumZemin: '#fdf2f8', cozumKenar: '#be185d' }),
  temaKur('gece', 'Gece', 'Koyu sayfa, açık metin (ekran)', '#60a5fa', '#e5e7eb', { sayfaZemin: '#0f172a', baslik: '#93c5fd', baslikCizgi: '#334155', altBilgi: '#94a3b8', bant: '#93c5fd', grup: '#93c5fd', numara: '#60a5fa', kok: '#f1f5f9', sik: '#cbd5e1', sikHarf: '#e2e8f0', dogru: '#4ade80', dogruZemin: '#14532d', cevapHarfi: '#4ade80', cozumZemin: '#1e293b', cozumKenar: '#60a5fa', cozumMetin: '#e2e8f0', kaynak: '#94a3b8', ayirici: '#334155', sutunCizgi: '#334155', hucreKenar: '#334155', yazmaCizgi: '#334155', anahtarKenar: '#334155', filigran: '#e5e7eb', kapakBaslik: '#f8fafc' }),
  temaKur('kahve', 'Kahve', 'Koyu kahve, bej çözüm', '#5c3d2e', '#2b1d16', { numara: '#7c4a2d', dogru: '#7c4a2d', cozumZemin: '#f7efe6', cozumKenar: '#8b5e3c', altBilgi: '#8b6b57' }),
  temaKur('zeytin', 'Zeytin', 'Zeytin yeşili, toprak', '#4d7c0f', '#1a2e05', { numara: '#65a30d', dogru: '#4d7c0f', cozumZemin: '#f7fee7', cozumKenar: '#65a30d' }),
  temaKur('mavi-gri', 'Mavi gri', 'Sakin, kurumsal', '#334155', '#0f172a', { numara: '#475569', dogru: '#0369a1', cozumZemin: '#f1f5f9', cozumKenar: '#64748b', baslikCizgi: '#475569' }),
  temaKur('ozel', 'Özel', 'Her rengi kendin seç', '#1d4ed8', '#111827'),
];
export const temaTanim = (id: TemaId) => TEMALAR.find((t) => t.id === id) || TEMALAR[0];
/** Temayı uygular: vurgu, metin ve öge renkleri temadan gelir; özel seçimler sıfırlanır */
export const temaUygula = (a: Ayar, id: TemaId): Ayar => {
  const t = temaTanim(id);
  return { ...a, tema: id, vurgu: t.vurgu, metinRenk: t.metin, renkler: { ...t.renkler } };
};
/** Öge rengi: elle/temadan seçilmişse o, yoksa vurgu/metin renginden türetilen varsayılan */
export function ogeRenk(a: Ayar, k: RenkOge): string {
  const v = a.renkler?.[k];
  if (v) return v;
  switch (k) {
    case 'sayfaZemin': return '#ffffff';
    case 'baslik': case 'baslikCizgi': case 'bant': case 'grup': case 'numara': case 'dogru': case 'cevapHarfi': case 'cozumKenar': return a.vurgu;
    case 'kapakBaslik': case 'kok': case 'sik': case 'sikHarf': case 'filigran': return a.metinRenk;
    case 'dogruZemin': return `${a.vurgu}22`;
    case 'cozumZemin': return '';
    case 'cozumMetin': return a.metinRenk;
    case 'altBilgi': return '#6b7280';
    case 'kaynak': return '#6b7280';
    case 'ayirici': case 'sutunCizgi': return '#9ca3af';
    case 'hucreKenar': return '#cbd5e1';
    case 'yazmaCizgi': case 'notCizgi': return '#c7cbd1';
    case 'anahtarKenar': return '#d1d5db';
    case 'baslikZemin': return a.vurgu;
    case 'kutuKenar': return '#cbd5e1';
    case 'kutuZemin': return '';
    case 'desen': return '#d1d5db';
    case 'kesim': return '#9ca3af';
    /* 2026-11-13: yeni ayrı ögeler; boş bırakılırsa eski davranışla aynı yere bağlanır */
    case 'baslikAlt': case 'grupSayi': case 'kapakAlt': case 'optik': return '#6b7280';
    case 'kapakUst': case 'kapakSayi': case 'kapakZemin': return a.vurgu;
    case 'kapakNot': return a.metinRenk;
    case 'etiket': return '#64748b';
    case 'anahtarZemin': return '';
    default: return a.vurgu;
  }
}
/** Çözüm kutusu zemini: seçilmemişse vurgunun %7 açık tonu (CSS color-mix) */
export const cozumZeminCss = (a: Ayar) => ogeRenk(a, 'cozumZemin') || `color-mix(in srgb,${a.vurgu} 7%,${ogeRenk(a, 'sayfaZemin')})`;
/** Doğru şık zemini CSS değeri (tema vermediyse vurgunun saydam tonu) */
export const dogruZeminCss = (a: Ayar) => ogeRenk(a, 'dogruZemin');

/**
 * Sitedeki sabit ders renkleri (styles/health.css `.d-<anahtar>` --d değerleri): her ders her belgede aynı rengi alır.
 * Eşleşmeyen dersler (Ortopedi, Aile Hekimliği …) ek listeden ad karmasıyla seçilir; böylece birbirinden ayrışır.
 */
export const DERS_RENK: Record<DisciplineKey, string> = {
  pat: '#E8336B', farm: '#AF52DE', enf: '#34A853', mikro: '#2FAE6A', halk: '#00A79D', ic: '#007AFF', gen: '#5856D6', cocuk: '#FF9500',
  kadin: '#D63AAF', acil: '#FF3B30', biyo: '#32ADE6', ana: '#A2845E', fiz: '#E6A800', noro: '#5E5CE6', psik: '#8E6CEF', kardi: '#FF2D55',
  cerr: '#64748B', ftr: '#30B0C7', uro: '#FFB340', onko: '#BF5AF2', diger: '#8E8E93',
};
const EK_DERS_RENK = ['#0D9488', '#B45309', '#4D7C0F', '#9F1239', '#1D4ED8', '#6D28D9', '#0E7490', '#92400E', '#334155', '#7C2D12'];
export function dersRengi(ad: string): string {
  const k = disciplineKey(ad);
  if (k !== 'diger') return DERS_RENK[k];
  let h = 2166136261;
  for (let i = 0; i < ad.length; i++) h = Math.imul(h ^ ad.charCodeAt(i), 16777619);
  return EK_DERS_RENK[(h >>> 0) % EK_DERS_RENK.length];
}
/** Etiket türü başına sabit renk ("Alan rengi" etiket kipi) */
export const ALAN_RENK: Record<Alan, string> = {
  yil: '#0891b2', kurul: '#4f46e5', ders: '#db2777', konu: '#059669', kaynak: '#d97706', tur: '#7c3aed', zorluk: '#dc2626', etiket: '#0d9488',
};

export const PALETLER: Record<PaletId, { ad: string; renk: string[] }> = {
  canli: { ad: 'Canlı', renk: ['#2563eb', '#dc2626', '#059669', '#d97706', '#7c3aed', '#db2777', '#0891b2', '#65a30d', '#ea580c', '#4f46e5', '#0d9488', '#be123c'] },
  pastel: { ad: 'Pastel', renk: ['#7aa2e3', '#e88f8f', '#7cc6a4', '#e8b86d', '#b39ddb', '#f0a1c2', '#7ec8d8', '#a9cf76', '#f2a87a', '#9fa8da', '#80cbc4', '#e6a0b0'] },
  koyu: { ad: 'Koyu', renk: ['#1e3a8a', '#7f1d1d', '#064e3b', '#78350f', '#4c1d95', '#831843', '#164e63', '#365314', '#7c2d12', '#312e81', '#134e4a', '#881337'] },
  gri: { ad: 'Gri tonlar', renk: ['#111827', '#4b5563', '#6b7280', '#374151', '#9ca3af', '#1f2937'] },
  sicak: { ad: 'Sıcak', renk: ['#dc2626', '#ea580c', '#d97706', '#ca8a04', '#be123c', '#c2410c', '#b45309', '#9f1239', '#f59e0b', '#e11d48'] },
  soguk: { ad: 'Soğuk', renk: ['#2563eb', '#0891b2', '#0d9488', '#4f46e5', '#0e7490', '#1d4ed8', '#0f766e', '#6366f1', '#0284c7', '#4338ca'] },
  toprak: { ad: 'Toprak', renk: ['#78350f', '#92400e', '#a16207', '#4d7c0f', '#5c3d2e', '#7c2d12', '#365314', '#854d0e', '#6b4f3a', '#3f6212'] },
  neon: { ad: 'Neon', renk: ['#f43f5e', '#8b5cf6', '#06b6d4', '#22c55e', '#f59e0b', '#ec4899', '#3b82f6', '#84cc16', '#f97316', '#a855f7'] },
  maviTon: { ad: 'Mavi tonları', renk: ['#1e3a8a', '#1d4ed8', '#2563eb', '#3b82f6', '#60a5fa', '#0c4a6e', '#0369a1', '#0284c7', '#0ea5e9', '#38bdf8'] },
  yesilTon: { ad: 'Yeşil tonları', renk: ['#14532d', '#166534', '#15803d', '#16a34a', '#22c55e', '#134e4a', '#0f766e', '#0d9488', '#14b8a6', '#4d7c0f'] },
  morTon: { ad: 'Mor tonları', renk: ['#4c1d95', '#5b21b6', '#6d28d9', '#7c3aed', '#8b5cf6', '#581c87', '#7e22ce', '#9333ea', '#a855f7', '#c026d3'] },
  bordoTon: { ad: 'Bordo tonları', renk: ['#881337', '#9f1239', '#be123c', '#e11d48', '#f43f5e', '#831843', '#9d174d', '#be185d', '#db2777', '#ec4899'] },
  gokkusagi: { ad: 'Gökkuşağı', renk: ['#ef4444', '#f97316', '#eab308', '#22c55e', '#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899', '#14b8a6', '#f59e0b', '#6366f1', '#84cc16'] },
  ofis: { ad: 'Ofis', renk: ['#4472c4', '#ed7d31', '#a5a5a5', '#ffc000', '#5b9bd5', '#70ad47', '#264478', '#9e480e', '#636363', '#997300'] },
  ozel: { ad: 'Kendi paletim', renk: [] },
};
/** Renk anahtarının paleti: 'ozel' kullanıcının kendi listesi (boşsa Canlı) */
export const paletRenkleri = (a: Ayar): string[] => (a.palet === 'ozel' ? (a.paletOzel.length ? a.paletOzel : PALETLER.canli.renk) : PALETLER[a.palet]?.renk || PALETLER.canli.renk);

const ORTAK: Ayar = {
  tasarim: 'sinav', bicim: 'pdf', kagit: 'a4', yatay: false, slayt: 'genis', duzen: 'akis', sutun: 2,
  kenar: [15, 14, 15, 14], kenarKilit: false, cerceve: false, cerceveStil: 'solid', cerceveKalin: 0.8, cerceveRenk: '#111827',
  cerceveYaricap: 0, cerceveIc: 4, hucreCerceve: false, hucreAralik: 6, sutunCizgi: true,
  baslikAcik: true, baslik: 'Soru kitapçığı', altBaslik: '', adSoyad: true, tarih: true, baslikHerSayfa: false,
  sayfaNo: true, altMetin: 'MeDSor', kapak: false, filigran: '',
  yaprak: 'tek', ciftYuz: false, kesimCizgi: false, baslikStil: 'cizgi', baslikHiza: 'sol', logo: '', logoYer: 'ikisi', logoYuk: 10,
  altOrta: '', altSag: '', sayfaNoYer: 'sag', sayfaNoBicim: 'bolme', altCizgi: false, desen: 'yok', notAlani: 0, kapakStil: 'sade', kapakNot: '',
  soruKutu: 'yok', kutuYaricap: 1.6, kutuIc: 2.5, asiliGirinti: false, sikAralik: 1.2, sikOran: 1, cozumStil: 'bant',
  cikti: 'hepsi', sayfaAralik: '', ozelCss: '',
  yazi: 'serif', yaziBaslik: 'ayni', agirlik: 400, baslikAgirlik: 800, harfAralik: 0, kokStil: 'normal', sikStil: 'normal', baslikBuyuk: 'normal', grupBuyuk: 'normal',
  numaraStil: 'kalin', sikHarfStil: 'kalin', baslikOran: 1.45, sikGirinti: 0, punto: 10.5, satir: 1.3, paragraf: 2, soruArasi: 6, iki: false, kokKalin: true, secenekDuzen: 'alt',
  numara: '1.', harf: 'A)', metinRenk: '#111827', vurgu: '#1d4ed8', tema: 'klasik', renkler: {}, paletOzel: [], ayirici: 'yok', yazmaSatiri: 0,
  renkAlan: 'yok', renkStil: 'serit', palet: 'canli', renkOzel: {}, dersRenkleri: true,
  etiket: { ders: false, konu: false, yil: false, kaynak: false, kurul: false, zorluk: false, tur: false, etiket: false }, etiketYeri: 'ust',
  etiketBoyut: 0.72, etiketDizilim: 'sol', etiketSekil: 'hap', etiketRenk: 'gri', etiketZemin: '#e2e8f0', etiketMetin: '#334155', etiketKalin: true,
  grupRenkli: true,
  dogruIsaret: false, isaretStil: 'kalin', cozumYeri: 'sonda', cozumIcerik: { harf: true, aciklama: true, siklar: false, kaynak: false, yalnizDogru: false },
  cevapAnahtari: true, optik: false, arkaAyna: true,
  gruplar: [], grupSirasi: 'olagan', grupStil: 'cizgi', grupSayi: false, grupYeniSayfa: false, sirala: 'kaynak', sikKaristir: false, numaraBas: 1, grupNumara: false, tohum: 1,
  sigdir: 'yok', sigdirHedef: 0,
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
    ayar: { yazi: 'modern', punto: 11, satir: 1.35, duzen: 4, cerceve: false, hucreCerceve: true, hucreAralik: 6, numara: 'S1.', harf: 'A)', kokKalin: true, renkAlan: 'konu', renkStil: 'etiket', palet: 'pastel', etiket: { ...ORTAK.etiket, ders: true, konu: true }, ayirici: 'yok', vurgu: '#7c3aed', metinRenk: '#1f2937', dogruIsaret: false, cozumYeri: 'arkada', cozumIcerik: { harf: true, aciklama: true, siklar: true, kaynak: false, yalnizDogru: false }, cevapAnahtari: false, optik: false, kapak: false, baslikAcik: false, yazmaSatiri: 0 },
  },
  {
    id: 'defter', ad: 'Çalışma kâğıdı', alt: 'Her sorunun altında not satırları, sayfa çerçevesi',
    ayar: { yazi: 'kitap', punto: 11, satir: 1.45, duzen: 2, cerceve: true, cerceveStil: 'solid', cerceveKalin: 0.8, cerceveYaricap: 3, hucreCerceve: false, numara: 'Soru 1', harf: 'A)', kokKalin: true, renkAlan: 'yok', etiket: { ...ORTAK.etiket, konu: true }, ayirici: 'dashed', vurgu: '#0f766e', metinRenk: '#111827', yazmaSatiri: 4, dogruIsaret: false, cozumYeri: 'sonda', optik: false, kapak: false, baslikAcik: true, adSoyad: true },
  },
  {
    id: 'akademik', ad: 'Akademik', alt: 'Serif, asılı girinti, başlık bandı, çift yüz cilt payı, çözüm sonda',
    ayar: { yazi: 'sourceserif', yaziBaslik: 'montserrat', punto: 10.5, satir: 1.38, duzen: 'akis', sutun: 1, sutunCizgi: false, cerceve: false, hucreCerceve: false, numara: '1.', harf: 'A)', kokKalin: false, kokStil: 'normal', asiliGirinti: true, secenekDuzen: 'alt', renkAlan: 'yok', etiket: { ...ORTAK.etiket, konu: true }, etiketSekil: 'duz', ayirici: 'yok', soruArasi: 7, vurgu: '#1e3a8a', metinRenk: '#0f172a', tema: 'lacivert', renkler: { numara: '#1e40af', dogru: '#1d4ed8', cozumZemin: '#eef2ff', cozumKenar: '#3730a3' }, baslikStil: 'bant', baslikHerSayfa: true, baslikBuyuk: 'kucukBuyuk', ciftYuz: true, kenar: [16, 14, 16, 20], sayfaNoYer: 'orta', sayfaNoBicim: 'tire', altCizgi: true, dogruIsaret: false, cozumYeri: 'sonda', cozumStil: 'kutu', cevapAnahtari: true, optik: false, kapak: true, kapakStil: 'bant', yazmaSatiri: 0, soruKutu: 'yok' },
  },
  {
    id: 'kesilir', ad: 'Kesilebilir kartlar', alt: 'Sayfada 8 kart, kesim çizgileri, çözüm kartın arkasında (çift yüz)',
    ayar: { yazi: 'inter', punto: 9.5, satir: 1.3, duzen: 8, hucreCerceve: false, hucreAralik: 0, kesimCizgi: true, cerceve: false, numara: 'S1.', harf: 'A)', kokKalin: true, renkAlan: 'ders', renkStil: 'etiket', etiket: { ...ORTAK.etiket, ders: true, konu: true }, ayirici: 'yok', vurgu: '#0f766e', metinRenk: '#111827', dogruIsaret: false, cozumYeri: 'arkada', arkaAyna: true, cozumIcerik: { harf: true, aciklama: true, siklar: false, kaynak: false, yalnizDogru: true }, cevapAnahtari: false, optik: false, kapak: false, baslikAcik: false, sayfaNo: false, altMetin: '', yazmaSatiri: 0, soruKutu: 'yok', kutuIc: 3, kenar: [10, 10, 10, 10] },
  },
  {
    id: 'kompakt', ad: 'Kompakt tekrar', alt: 'Küçük punto, iki sütun, doğru şık işaretli, şıklar yan yana',
    ayar: { yazi: 'sans', punto: 8.5, satir: 1.2, paragraf: 1, soruArasi: 3, duzen: 'akis', sutun: 2, sutunCizgi: true, cerceve: false, hucreCerceve: false, numara: '1.', harf: 'A)', kokKalin: true, secenekDuzen: 'iki', renkAlan: 'ders', renkStil: 'numara', palet: 'koyu', etiket: { ...ORTAK.etiket, yil: true }, ayirici: 'dotted', vurgu: '#b91c1c', metinRenk: '#111827', dogruIsaret: true, isaretStil: 'zemin', cozumYeri: 'yok', cevapAnahtari: false, optik: false, kapak: false, kenar: [10, 10, 10, 10], yazmaSatiri: 0 },
  },
];
export const tasarimUygula = (a: Ayar, id: TasarimId): Ayar => ({ ...a, ...(TASARIMLAR.find((t) => t.id === id)?.ayar || {}), tasarim: id });
export const VARSAYILAN: Ayar = tasarimUygula(ORTAK, 'sinav');

const ALAN_SET = new Set<string>(ALANLAR.map((x) => x.id));
/** Gruplama katmanları: yalnız geçerli alanlar, tekrarsız, en çok EN_COK_GRUP */
export const gruplarNormal = (v: unknown): Alan[] =>
  (Array.isArray(v) ? v : []).filter((x, i, arr): x is Alan => typeof x === 'string' && ALAN_SET.has(x) && arr.indexOf(x) === i).slice(0, EN_COK_GRUP);

/** Kayıttan gelen ayarı doğrular (eksik alan varsayılandan, bozuk değer atılır); eski tek alanlı `grupla` kaydı katmana çevrilir */
export function ayarNormal(raw: any): Ayar {
  const a: any = { ...VARSAYILAN };
  if (raw && typeof raw === 'object') {
    for (const k of Object.keys(VARSAYILAN) as (keyof Ayar)[]) {
      const v = raw[k];
      const d: any = VARSAYILAN[k];
      if (v == null) continue;
      if (k === 'gruplar') { a.gruplar = gruplarNormal(v); continue; }
      if (Array.isArray(d)) { if (Array.isArray(v) && v.length === d.length && v.every((x: any) => typeof x === 'number')) a[k] = v; }
      else if (typeof d === 'object') { if (typeof v === 'object' && !Array.isArray(v)) a[k] = { ...d, ...v }; }
      else if (typeof v === typeof d || (k === 'duzen' && (v === 'akis' || [1, 2, 4, 8].includes(v)))) a[k] = v;
    }
    if (!Array.isArray(raw.gruplar) && typeof raw.grupla === 'string' && raw.grupla !== 'yok') a.gruplar = gruplarNormal([raw.grupla]);
  }
  a.punto = Math.min(16, Math.max(6, Number(a.punto) || 10.5));
  if (!YAZI[a.yazi as YaziId]) a.yazi = 'serif';
  if (a.yaziBaslik !== 'ayni' && !YAZI[a.yaziBaslik as YaziId]) a.yaziBaslik = 'ayni';
  if (![300, 400, 500, 600, 700, 800].includes(a.agirlik)) a.agirlik = 400;
  if (![300, 400, 500, 600, 700, 800].includes(a.baslikAgirlik)) a.baslikAgirlik = 800;
  a.harfAralik = Math.min(0.2, Math.max(-0.05, Number(a.harfAralik) || 0));
  a.baslikOran = Math.min(2.2, Math.max(1, Number(a.baslikOran) || 1.45));
  a.sikGirinti = Math.min(12, Math.max(0, Number(a.sikGirinti) || 0));
  if (!TEMALAR.some((t) => t.id === a.tema)) a.tema = 'klasik';
  if (!PALETLER[a.palet as PaletId]) a.palet = 'canli';
  const hexMi = (v: unknown) => typeof v === 'string' && /^#[0-9a-f]{6}([0-9a-f]{2})?$/i.test(v);
  a.paletOzel = (Array.isArray(a.paletOzel) ? a.paletOzel : []).filter(hexMi).slice(0, 24);
  a.renkler = Object.fromEntries(Object.entries(a.renkler || {}).filter(([k, v]) => RENK_OGELERI.some((o) => o.id === k) && hexMi(v)));
  a.satir = Math.min(2.4, Math.max(1, Number(a.satir) || 1.3));
  a.kenar = a.kenar.map((x: number) => Math.min(40, Math.max(0, x)));
  if (![1, 2].includes(a.sutun)) a.sutun = 1;
  if (a.renkAlan !== 'yok' && !ALAN_SET.has(a.renkAlan)) a.renkAlan = 'yok';
  if (!SIRALAMALAR.some((x) => x.id === a.sirala)) a.sirala = 'kaynak';
  a.etiketBoyut = Math.min(1.1, Math.max(0.5, Number(a.etiketBoyut) || 0.72));
  a.sigdirHedef = Math.min(999, Math.max(0, Math.round(Number(a.sigdirHedef) || 0)));
  if (!['tek', 'iki', 'kitapcik'].includes(a.yaprak)) a.yaprak = 'tek';
  if (!['cizgi', 'bant', 'kutu', 'sade'].includes(a.baslikStil)) a.baslikStil = 'cizgi';
  if (!['sol', 'orta'].includes(a.baslikHiza)) a.baslikHiza = 'sol';
  if (typeof a.logo !== 'string' || !/^data:image\/(png|jpeg|webp|gif);base64,/.test(a.logo) || a.logo.length > LOGO_EN_COK * 1.4) a.logo = '';
  if (!['baslik', 'kapak', 'ikisi'].includes(a.logoYer)) a.logoYer = 'ikisi';
  a.logoYuk = Math.min(24, Math.max(4, Number(a.logoYuk) || 10));
  if (!['sol', 'orta', 'sag'].includes(a.sayfaNoYer)) a.sayfaNoYer = 'sag';
  if (!['bolme', 'duz', 'sayfa', 'tire'].includes(a.sayfaNoBicim)) a.sayfaNoBicim = 'bolme';
  if (!['yok', 'cizgili', 'kareli', 'noktali'].includes(a.desen)) a.desen = 'yok';
  a.notAlani = Math.min(80, Math.max(0, Number(a.notAlani) || 0));
  if (!['sade', 'bant', 'zemin'].includes(a.kapakStil)) a.kapakStil = 'sade';
  if (!['yok', 'cizgi', 'zemin', 'golge'].includes(a.soruKutu)) a.soruKutu = 'yok';
  a.kutuYaricap = Math.min(6, Math.max(0, Number(a.kutuYaricap) || 0));
  a.kutuIc = Math.min(8, Math.max(0, Number(a.kutuIc) || 0));
  a.sikAralik = Math.min(8, Math.max(0, Number(a.sikAralik) || 0));
  a.sikOran = Math.min(1.2, Math.max(0.7, Number(a.sikOran) || 1));
  if (!['bant', 'kutu', 'zemin', 'sade'].includes(a.cozumStil)) a.cozumStil = 'bant';
  if (!['hepsi', 'sorular', 'cozumler'].includes(a.cikti)) a.cikti = 'hepsi';
  a.sayfaAralik = String(a.sayfaAralik || '').replace(/[^\d,\- ]/g, '').slice(0, 60);
  a.ozelCss = String(a.ozelCss || '').slice(0, 4000);
  for (const k of ['altOrta', 'altSag', 'kapakNot'] as const) a[k] = String(a[k] || '').slice(0, 200);
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
/** not alanının başlık + üst boşluk payı (mm) */
export const NOT_PAY_MM = 4;
/** alt bilgi var mı: sayfa numarası ya da üç bölgeden birinde metin */
export const altBilgiVar = (a: Ayar) => a.sayfaNo || !!(a.altMetin || '').trim() || !!(a.altOrta || '').trim() || !!(a.altSag || '').trim();

/** Sayfa aralığı metni ("1-4, 7") → sayfa numarası kümesi; boş/bozuk = null (tümü). Kapak 0 sayılır */
export function sayfaAraligi(t: string): Set<number> | null {
  const out = new Set<number>();
  for (const p of String(t || '').split(',')) {
    const m = /^\s*(\d+)\s*(?:-\s*(\d+))?\s*$/.exec(p);
    if (!m) continue;
    const a = Number(m[1]);
    const b = m[2] ? Number(m[2]) : a;
    for (let i = Math.min(a, b); i <= Math.max(a, b) && i <= 2000; i++) out.add(i);
  }
  return out.size ? out : null;
}
/** Yaprak başına sayfa ve yaprak ölçüsü (mm): 2'li ve kitapçıkta sayfa yatay yaprağa yarım ölçekte yerleşir */
export function yaprakOlcu(a: Ayar): { w: number; h: number; sayfa: 1 | 2; olcek: number } {
  const { w, h } = sayfaOlcu(a);
  if (a.yaprak === 'tek' || a.bicim !== 'pdf') return { w, h, sayfa: 1, olcek: 1 };
  // yaprak: sayfanın uzun kenarı yaprağın kısa kenarı olur (A4 dikey → A4 yatay yaprakta 2 × A5)
  const yw = Math.max(w, h);
  const yh = Math.min(w, h);
  const olcek = Math.min((yw / 2) / w, yh / h);
  return { w: yw, h: yh, sayfa: 2, olcek };
}

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
  const altVar = altBilgiVar(a);
  const gw = w - a.kenar[1] - a.kenar[3] - ic * 2;
  const not = a.notAlani > 0 ? a.notAlani + NOT_PAY_MM : 0;
  const gh = h - a.kenar[0] - a.kenar[2] - ic * 2 - (baslik ? BASLIK_MM : 0) - (altVar ? ALT_MM : 0) - (o.serit ? SERIT_MM : 0) - (o.grup ? GRUP_MM : 0) - not;
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
