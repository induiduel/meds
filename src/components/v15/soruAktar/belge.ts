/**
 * Soru dışa aktarıcı · belge motoru. Akış:
 *   hazirla()  seçili soruları sıralar, gruplar, numaralar, istenirse şıkları karıştırır, renk anahtarını kurar
 *   sayfala()  her bloğu gizli bir çerçevede ölçer ve sayfalara yerleştirir (1/2/4/8 ızgara ya da 1–2 sütun akış);
 *              ızgara hücresine sığmayan soru yazı ölçeği (--k) küçültülerek sığdırılır
 *   belgeHtml() sayfa modelinden önizleme/PDF HTML'i üretir (sunucu Chrome'u aynı HTML'i basar)
 * DOCX ve PPTX yazıcıları aynı sayfa modelini (Sayfa[]) ve aynı ölçekleri kullanır; böylece üç çıktı aynı düzendedir.
 */
import type { PdfOption } from '../../pdf/pdfSources';
import { kaynakAdi, type AQ } from './kaynak';
import {
  ALAN_RENK, ALT_MM, BASLIK_MM, GRUP_MM, KAGIT, NOT_PAY_MM, PX_MM, SERIT_MM, YAZI, altBilgiVar, baslikYazi, buyukCss, cozumZeminCss, dersRengi, dogruZeminCss, govde, izgara, karistir,
  kaynakSirasi, ogeRenk, paletRenkleri, sayfaAraligi, sayfaOlcu, stilCss, yaprakOlcu, yaziBaglantilari,
  type Alan, type Ayar, type Govde, type RenkAlan,
} from './ayar';

/* ---------------------------------------------------------------------------
 * Hazırlık
 * ------------------------------------------------------------------------- */
export interface HS {
  q: AQ;
  no: number;
  /** grup yolu: katman değerleri " › " ile (ızgara bandı, sayfa kırılımı); gruplama yoksa '' */
  grup: string;
  /** katman başına grup değeri (a.gruplar sırasıyla) */
  gruplar: string[];
  /** katman başına başlık rengi (grupRenkli kapalıysa null) */
  grupRenk: (string | null)[];
  /** renk anahtarı rengi (renkAlan) */
  renk: string | null;
  /** dersin sabit rengi (etiket "ders" kipi, başlıklar) */
  dersRenk: string;
  secenek: PdfOption[];
  dogru?: string;
}

const s = (v: unknown) => String(v ?? '').trim();
const ZOR = ['kolay', 'orta', 'zor'];
const hash = (t: string) => { let h = 2166136261; for (let i = 0; i < t.length; i++) h = Math.imul(h ^ t.charCodeAt(i), 16777619); return h >>> 0; };
const buyuk = (t: string) => (t ? t[0].toLocaleUpperCase('tr') + t.slice(1) : t);

/** Listedeki etiket sıklığı: bir sorunun birden çok etiketi varsa gruplamada en yaygını temsil eder */
export function etiketSikligi(list: AQ[]): Map<string, number> {
  const m = new Map<string, number>();
  for (const q of list) for (const t of q.etiketler) m.set(t, (m.get(t) || 0) + 1);
  return m;
}
export function deger(q: AQ, alan: RenkAlan | '', sik?: Map<string, number>): string {
  switch (alan) {
    case 'ders': return q.ders || 'Diğer';
    case 'konu': return q.konu || 'Konusuz';
    case 'yil': return q.year || 'Yılsız';
    case 'kaynak': return kaynakAdi(q.kaynak);
    case 'kurul': return q.kurul ? `Kurul ${q.kurul}` : 'Kurul belirsiz';
    case 'tur': return q.tur;
    case 'zorluk': return q.difficulty ? buyuk(q.difficulty) : 'Zorluk belirsiz';
    case 'etiket': {
      if (!q.etiketler.length) return 'Etiketsiz';
      if (!sik) return q.etiketler[0];
      return [...q.etiketler].sort((x, y) => (sik.get(y) || 0) - (sik.get(x) || 0))[0];
    }
    default: return '';
  }
}

/** Renk anahtarı: değer → renk (derste sitedeki sabit ders rengi; başka alanda ilk görünüş sırasına göre palet; elle seçilen renk önce gelir) */
export function renkHaritasi(list: AQ[], a: Ayar): { v: string; renk: string; n: number }[] {
  if (a.renkAlan === 'yok') return [];
  const sik = a.renkAlan === 'etiket' ? etiketSikligi(list) : undefined;
  const m = new Map<string, number>();
  for (const q of list) { const v = deger(q, a.renkAlan, sik); m.set(v, (m.get(v) || 0) + 1); }
  const pal = paletRenkleri(a);
  const sabit = a.renkAlan === 'ders' && a.dersRenkleri;
  return [...m].map(([v, n], i) => ({ v, n, renk: a.renkOzel[`${a.renkAlan}:${v}`] || (sabit ? dersRengi(v) : pal[i % pal.length]) }));
}

const sirala = (list: AQ[], a: Ayar): AQ[] => {
  const idx = new Map(list.map((q, i) => [q.key, i]));
  const ilk = (x: AQ, y: AQ) => (idx.get(x.key)! - idx.get(y.key)!);
  const tr = (x: string, y: string) => x.localeCompare(y, 'tr', { numeric: true });
  const no = (x: AQ, y: AQ) => (x.number || 0) - (y.number || 0);
  const zor = (x: AQ) => { const i = ZOR.indexOf(x.difficulty || ''); return i < 0 ? ZOR.length : i; };
  const uz = (x: AQ) => x.stem.length + x.options.reduce((t, o) => t + o.text.length, 0);
  switch (a.sirala) {
    case 'rastgele': return karistir(list, a.tohum);
    case 'ders': return [...list].sort((x, y) => tr(x.ders, y.ders) || tr(x.konu, y.konu) || no(x, y) || ilk(x, y));
    case 'konu': return [...list].sort((x, y) => tr(x.konu, y.konu) || no(x, y) || ilk(x, y));
    case 'yil': return [...list].sort((x, y) => tr(y.year || '', x.year || '') || tr(x.ders, y.ders) || no(x, y) || ilk(x, y));
    case 'yilEski': return [...list].sort((x, y) => tr(x.year || '9999', y.year || '9999') || tr(x.ders, y.ders) || no(x, y) || ilk(x, y));
    case 'zorluk': return [...list].sort((x, y) => zor(x) - zor(y) || ilk(x, y));
    case 'zorlukZor': return [...list].sort((x, y) => (zor(y) === ZOR.length ? -1 : zor(y)) - (zor(x) === ZOR.length ? -1 : zor(x)) || ilk(x, y));
    case 'numara': return [...list].sort((x, y) => no(x, y) || ilk(x, y));
    case 'kisa': return [...list].sort((x, y) => uz(x) - uz(y) || ilk(x, y));
    case 'uzun': return [...list].sort((x, y) => uz(y) - uz(x) || ilk(x, y));
    case 'alfabetik': return [...list].sort((x, y) => tr(x.stem, y.stem) || ilk(x, y));
    default: return [...list].sort((x, y) => kaynakSirasi.indexOf(x.kaynak) - kaynakSirasi.indexOf(y.kaynak) || ilk(x, y));
  }
};

/** Bir katmandaki grup adlarının olağan sırası: yıl yeni önce, kurul numarası, zorluk kolaydan, kaynak kaynak sırası, etiket sıklık, ad A→Z */
function grupSirasi(alan: Alan, gruplar: Map<string, AQ[]>, a: Ayar, sik: Map<string, number>): string[] {
  const adlar = [...gruplar.keys()];
  if (a.sirala === 'rastgele' && a.grupSirasi === 'olagan') return adlar;
  const tr = (x: string, y: string) => x.localeCompare(y, 'tr', { numeric: true });
  const olagan = (x: string, y: string): number => {
    switch (alan) {
      case 'yil': { // sayısal yıllar yeni önce; "Yılı belirsiz", "Kategorisiz", "Yılsız" gibi metinler sona
        const m = (v: string) => (/^\d/.test(v) ? 0 : 1);
        return m(x) - m(y) || (m(x) ? tr(x, y) : tr(y, x));
      }
      case 'kurul': return tr(x, y);
      case 'zorluk': { const o = ['Kolay', 'Orta', 'Zor', 'Zorluk belirsiz']; return o.indexOf(x) - o.indexOf(y); }
      case 'kaynak': return kaynakSirasi.findIndex((k) => kaynakAdi(k) === x) - kaynakSirasi.findIndex((k) => kaynakAdi(k) === y);
      case 'etiket': return (x === 'Etiketsiz' ? 1 : 0) - (y === 'Etiketsiz' ? 1 : 0) || (sik.get(y) || 0) - (sik.get(x) || 0) || tr(x, y);
      default: return tr(x, y);
    }
  };
  const n = (x: string) => gruplar.get(x)!.length;
  if (a.grupSirasi === 'sayiAzalan') return adlar.sort((x, y) => n(y) - n(x) || olagan(x, y));
  if (a.grupSirasi === 'sayiArtan') return adlar.sort((x, y) => n(x) - n(y) || olagan(x, y));
  return adlar.sort(olagan);
}

/** Katmanlı gruplama: her katmanda gruplar sıralanır, grup içi sıra korunur (kararlı) */
function katmanla(list: AQ[], a: Ayar, seviye: number, sik: Map<string, number>): AQ[] {
  const alan = a.gruplar[seviye];
  if (!alan) return list;
  const gruplar = new Map<string, AQ[]>();
  for (const q of list) {
    const v = deger(q, alan, sik);
    const l = gruplar.get(v);
    if (l) l.push(q); else gruplar.set(v, [q]);
  }
  return grupSirasi(alan, gruplar, a, sik).flatMap((ad) => katmanla(gruplar.get(ad)!, a, seviye + 1, sik));
}

/** Başlık rengi: katmanın alanı ders ise dersin sabit rengi; renk anahtarının alanıysa o renk; yoksa bir üst katmandan miras */
function grupRenkleri(q: AQ, a: Ayar, renk: string | null): (string | null)[] {
  const out: (string | null)[] = [];
  let miras: string | null = null;
  for (const alan of a.gruplar) {
    let r: string | null = null;
    if (!a.grupRenkli) r = null;
    else if (alan === 'ders' && a.dersRenkleri) r = dersRengi(q.ders || 'Diğer');
    else if (alan === a.renkAlan) r = renk;
    else r = miras;
    out.push(r);
    if (r) miras = r;
  }
  return out;
}

export function hazirla(list: AQ[], a: Ayar): HS[] {
  const sik = etiketSikligi(list);
  const sirali = a.gruplar.length ? katmanla(sirala(list, a), a, 0, sik) : sirala(list, a);
  const renk = new Map(renkHaritasi(sirali, a).map((r) => [r.v, r.renk]));
  let no = a.numaraBas - 1;
  let onceki = '';
  return sirali.map((q) => {
    const gruplar = a.gruplar.map((alan) => deger(q, alan, sik));
    const grup = gruplar.join(' › ');
    if (a.grupNumara && grup !== onceki) no = a.numaraBas - 1;
    onceki = grup;
    no++;
    let secenek = q.options;
    let dogru = q.answer;
    if (a.sikKaristir && secenek.length > 2) {
      const k = karistir(secenek, a.tohum + hash(q.key));
      const harfler = secenek.map((o) => o.key);
      secenek = k.map((o, i) => ({ ...o, key: harfler[i] }));
      const yeni = k.findIndex((o) => o.key === q.answer);
      dogru = yeni >= 0 ? harfler[yeni] : q.answer;
    }
    const r = a.renkAlan === 'yok' ? null : renk.get(deger(q, a.renkAlan, sik)) || null;
    return { q, no, grup, gruplar, grupRenk: grupRenkleri(q, a, r), renk: r, dersRenk: dersRengi(q.ders || 'Diğer'), secenek, dogru };
  });
}

/* ---------------------------------------------------------------------------
 * Metin yardımcıları (HTML + Office yazıcıları ortak)
 * ------------------------------------------------------------------------- */
export const esc = (t: string) => t.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]!));
/** "**kalın**" ve satır sonları: parça listesi (Office) */
export interface Parca { t: string; b?: boolean; br?: boolean }
export function parcala(t: string): Parca[] {
  const out: Parca[] = [];
  s(t).replace(/\r/g, '').split('\n').forEach((satir, i) => {
    if (i) out.push({ t: '', br: true });
    satir.split(/(\*\*[^*]+\*\*)/).forEach((p) => {
      if (!p) return;
      const m = /^\*\*([^*]+)\*\*$/.exec(p);
      out.push(m ? { t: m[1], b: true } : { t: p });
    });
  });
  return out;
}
const zengin = (t: string) => parcala(t).map((p) => (p.br ? '<br>' : p.b ? `<b>${esc(p.t)}</b>` : esc(p.t))).join('');

export const numaraMetni = (no: number, a: Ayar) =>
  a.numara === '1)' ? `${no})` : a.numara === 'S1.' ? `S${no}.` : a.numara === 'Soru 1' ? `Soru ${no}` : `${no}.`;
export const harfMetni = (k: string, a: Ayar) =>
  a.harf === 'A.' ? `${k}.` : a.harf === '(A)' ? `(${k})` : a.harf === 'a)' ? `${k.toLowerCase()})` : `${k})`;

export interface Etiket { ad: string; alan: Alan; /** renk anahtarının alanı (rengi taşır) */ renkli: boolean; /** etiket kipine göre hesaplanan renk (HTML/DOCX/PPTX ortak) */ renk: string }
/** Etiketin rengi: gri · alan (etiket türü başına sabit) · ders (dersin rengi) · özel (metin rengi, zemin ayrı) · renk anahtarı alanı her kipte kendi rengini taşır */
function etiketRengi(h: HS, alan: Alan, a: Ayar): string {
  if (a.renkAlan === alan && h.renk) return h.renk;
  switch (a.etiketRenk) {
    case 'alan': return alan === 'ders' && a.dersRenkleri ? h.dersRenk : ALAN_RENK[alan];
    case 'ders': return h.dersRenk;
    case 'ozel': return a.etiketMetin;
    default: return '#64748b';
  }
}
export function etiketler(h: HS, a: Ayar): Etiket[] {
  const q = h.q;
  const e = a.etiket;
  const out: Etiket[] = [];
  const ekle = (on: boolean, alan: Alan, v: string | undefined) => { if (on && v) out.push({ ad: v, alan, renkli: a.renkAlan === alan, renk: etiketRengi(h, alan, a) }); };
  ekle(e.kurul, 'kurul', q.kurul ? `Kurul ${q.kurul}` : '');
  ekle(e.ders, 'ders', q.ders);
  ekle(e.konu, 'konu', q.konu);
  ekle(e.yil, 'yil', q.year);
  ekle(e.kaynak, 'kaynak', kaynakAdi(q.kaynak));
  ekle(e.tur, 'tur', q.tur);
  ekle(e.zorluk, 'zorluk', q.difficulty ? buyuk(q.difficulty) : '');
  if (e.etiket) for (const t of q.etiketler.slice(0, 6)) ekle(true, 'etiket', t);
  // renk anahtarı etiketi kapalı olsa da "etiket" renk stilinde rengin anlamı görünsün
  if (a.renkAlan !== 'yok' && a.renkStil === 'etiket' && !out.some((x) => x.renkli)) out.unshift({ ad: deger(q, a.renkAlan), alan: a.renkAlan, renkli: true, renk: h.renk || etiketRengi(h, a.renkAlan, a) });
  return out;
}

/** Çözüm metni parçaları (HTML/DOCX/PPTX ortak). "Yalnız doğru şık": yalnız doğru seçeneğin gerekçesi, çeldirici çözümlemesi yok */
export interface CozumIcerik { harf?: string; aciklama?: string; siklar: { k: string; t: string; dogru: boolean }[]; kaynak?: string }
export function cozumIcerik(h: HS, a: Ayar): CozumIcerik {
  const c = a.cozumIcerik;
  const q = h.q;
  const dogruWhy = h.secenek.find((o) => o.key === h.dogru)?.why;
  const siklar = c.siklar && !c.yalnizDogru ? h.secenek.filter((o) => o.why).map((o) => ({ k: o.key, t: o.why!, dogru: o.key === h.dogru })) : [];
  return {
    harf: c.harf ? h.dogru || '—' : undefined,
    aciklama: c.aciklama ? (c.yalnizDogru ? dogruWhy || q.explanation : q.explanation || (!c.siklar ? dogruWhy : undefined)) : undefined,
    siklar,
    kaynak: c.kaynak ? [...(q.refs || []), q.kazanim?.text ? `Kazanım: ${q.kazanim.text}` : ''].filter(Boolean).join(' · ') || undefined : undefined,
  };
}
export const cozumBos = (c: CozumIcerik) => !c.harf && !c.aciklama && !c.siklar.length && !c.kaynak;

/* ---------------------------------------------------------------------------
 * Sayfa modeli
 * ------------------------------------------------------------------------- */
export interface GrupBlok { t: 'grup'; ad: string; renk: string | null; /** katman: 0 en üst */ seviye: number; /** gruptaki soru sayısı */ sayi: number; k: number }
export type Blok =
  | { t: 'soru'; h: HS; k: number; tasma?: boolean; /** ızgara hücresinde sorunun üstüne yazılan alt katman başlıkları */ basliklar?: GrupBlok[] }
  | { t: 'cozum'; h: HS; k: number; tasma?: boolean }
  | GrupBlok;

export interface Sayfa {
  tur: 'kapak' | 'soru' | 'cozum' | 'anahtar' | 'optik';
  g: Govde;
  izgara?: { sut: number; sat: number; cw: number; ch: number };
  hucre?: (Blok | null)[];
  kolon?: Blok[][];
  kolonW?: number;
  /** sayfa başındaki bant (ızgara grubu ya da bölüm adı) */
  bant?: { ad: string; renk: string | null };
  serit?: { no: number; harf: string }[];
  anahtar?: { no: number; harf: string; renk: string | null }[];
  anahtarSut?: number;
  optik?: number[];
  optikSut?: number;
  /** gövdenin doluluk oranı 0–1 (sayfaya sığdır ölçütü) */
  dolu?: number;
  /** zorunlu kırılımla (yeni grup) başlayan sayfa: önceki sayfa bölümün sonudur */
  yeniBolum?: boolean;
}
export interface Belge {
  sayfalar: Sayfa[];
  hs: HS[];
  /** ızgaraya sığmayıp kırpılan soru sayısı */
  tasan: number;
  /** önizlemede yalnız ilk sorular sayfalandıysa tahmini toplam sayfa */
  tahmini?: number;
  /** sayfaya sığdırın seçtiği genel yazı ölçeği (1 = ayarlanan punto) */
  olcek: number;
  /** sayfaya sığdır hedefe ulaşamadıysa açıklama */
  sigdirNot?: string;
}

export const KOLON_ARA = 8;
const HUCRE_IC = 3;
export const ANAHTAR_W = 19;
export const ANAHTAR_H = 7;
export const OPTIK_W = 44;
export const OPTIK_H = 6.2;
export const MIN_K = 0.55;
/** sayfaya sığdır aralığı: genel ölçek bu sınırların dışına çıkmaz */
export const SIGDIR_MIN = 0.6;
export const SIGDIR_MAX = 1.35;
/** gövdesinin bu orandan azı dolu olan bölüm sonu sayfası "seyrek" sayılır (kendiliğinden hedef = bir sayfa az) */
const SEYREK = 0.45;

/* ---------------------------------------------------------------------------
 * CSS (önizleme, ölçüm ve PDF aynı kuralları kullanır)
 * ------------------------------------------------------------------------- */
export function belgeCss(a: Ayar, onizleme = false): string {
  const { w, h } = sayfaOlcu(a);
  const [kt, ks, ka, kl] = a.kenar;
  const ic = a.cerceve ? a.cerceveIc : 0;
  const vurgu = a.vurgu;
  const R = (k: Parameters<typeof ogeRenk>[1]) => ogeRenk(a, k);
  const zemin = R('sayfaZemin');
  const cizgi = (st: string, renk: string) => (st === 'yok' ? 'none' : `${st === 'double' ? 1.6 : 0.6}pt ${st} ${renk}`);
  const dogru = R('dogru');
  const isaret =
    a.isaretStil === 'zemin' ? `background:${dogruZeminCss(a)};box-shadow:0 0 0 .25em ${dogruZeminCss(a)};border-radius:.2em;font-weight:700;color:${dogru};`
      : a.isaretStil === 'daire' ? `font-weight:700;color:${dogru};`
        : a.isaretStil === 'tik' ? `font-weight:700;color:${dogru};`
          : `font-weight:700;color:${dogru};`;
  const basF = baslikYazi(a).css;
  const numara =
    a.numaraStil === 'kutu' ? `display:inline-block;background:${R('numara')};color:${zemin};border-radius:.3em;padding:0 .4em;min-width:1.6em;text-align:center;font-weight:800;`
      : a.numaraStil === 'daire' ? `display:inline-block;border:.13em solid ${R('numara')};color:${R('numara')};border-radius:99px;padding:0 .35em;min-width:1.7em;text-align:center;font-weight:700;`
        : a.numaraStil === 'altCizgi' ? `color:${R('numara')};font-weight:700;text-decoration:underline;text-underline-offset:.15em;`
          : a.numaraStil === 'duz' ? `color:${R('numara')};font-weight:400;`
            : `color:${R('numara')};font-weight:800;`;
  const sikHarf =
    a.sikHarfStil === 'daire' ? `color:${R('sikHarf')};font-weight:700;border:.11em solid currentColor;border-radius:99px;min-width:1.55em;text-align:center;padding:0 .15em;line-height:1.35;`
      : a.sikHarfStil === 'kutu' ? `color:${zemin};background:${R('sikHarf')};font-weight:700;border-radius:.25em;min-width:1.55em;text-align:center;padding:0 .2em;line-height:1.35;`
        : a.sikHarfStil === 'normal' ? `color:${R('sikHarf')};font-weight:400;`
          : `color:${R('sikHarf')};font-weight:700;`;
  const kokStil = stilCss(a.kokStil) || (a.kokKalin ? 'font-weight:600;' : '');
  const yp = yaprakOlcu(a);
  const yr = `${a.kutuYaricap}mm`;
  const desenR = R('desen');
  const desen =
    a.desen === 'cizgili' ? `background-image:repeating-linear-gradient(to bottom,transparent 0 ${(a.punto * a.satir * 0.3528 * 1.35).toFixed(2)}mm,${desenR} 0 calc(${(a.punto * a.satir * 0.3528 * 1.35).toFixed(2)}mm + .25pt));`
      : a.desen === 'kareli' ? `background-image:linear-gradient(${desenR} .25pt,transparent .25pt),linear-gradient(90deg,${desenR} .25pt,transparent .25pt);background-size:5mm 5mm;`
        : a.desen === 'noktali' ? `background-image:radial-gradient(${desenR} .35pt,transparent .5pt);background-size:5mm 5mm;`
          : '';
  const soruKutu =
    a.soruKutu === 'cizgi' ? `border:.6pt solid ${R('kutuKenar')};border-radius:${yr};padding:${a.kutuIc}mm;background:${R('kutuZemin') || 'transparent'};`
      : a.soruKutu === 'zemin' ? `border-radius:${yr};padding:${a.kutuIc}mm;background:${R('kutuZemin') || `color-mix(in srgb,${vurgu} 5%,${zemin})`};`
        : a.soruKutu === 'golge' ? `border-radius:${yr};padding:${a.kutuIc}mm;background:${R('kutuZemin') || zemin};box-shadow:0 .5mm 1.6mm rgb(0 0 0 / .2),0 0 0 .45pt ${R('kutuKenar')};`
          : '';
  const cozumKutu =
    a.cozumStil === 'kutu' ? `border:.6pt solid ${R('cozumKenar')};border-radius:${yr};background:${cozumZeminCss(a)};padding:1.8mm 2.4mm;`
      : a.cozumStil === 'zemin' ? `border-radius:${yr};background:${cozumZeminCss(a)};padding:1.8mm 2.4mm;`
        : a.cozumStil === 'sade' ? `border-top:.5pt solid ${R('cozumKenar')};padding:1.4mm 0 0;background:none;border-radius:0;`
          : `padding:1.6mm 2.2mm;border-radius:${Math.max(0.8, a.kutuYaricap)}mm;background:${cozumZeminCss(a)};border-left:.8mm solid ${R('cozumKenar')};`;
  const baslikKutu =
    a.baslikStil === 'bant' ? `background:${R('baslikZemin')};color:${zemin};padding:0 3mm 2.2mm;margin:0 -${a.cerceve ? a.cerceveIc : 0}mm;border-bottom:0;border-radius:${a.cerceve ? `${Math.max(0, a.cerceveYaricap - 0.5)}mm ${Math.max(0, a.cerceveYaricap - 0.5)}mm` : '0 0'} 0 0;`
      : a.baslikStil === 'kutu' ? `border:.7pt solid ${R('baslikCizgi')};border-radius:${yr};padding:0 3mm 2.2mm;`
        : a.baslikStil === 'sade' ? `border-bottom:0;`
          : '';
  const baslikRenk = a.baslikStil === 'bant' ? zemin : R('baslik');
  const baslikAlt = a.baslikStil === 'bant' ? `color-mix(in srgb,${zemin} 82%,${R('baslikZemin')})` : R('altBilgi');
  return `
@page{size:${yp.w}mm ${yp.h}mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:${YAZI[a.yazi].css};font-weight:${a.agirlik};color:${a.metinRenk};-webkit-print-color-adjust:exact;print-color-adjust:exact;font-size:${a.punto}pt;line-height:${a.satir};letter-spacing:${a.harfAralik}em;text-rendering:geometricPrecision;font-kerning:normal}
${onizleme ? `html{background:#d4d7dd}body{padding:14px 0}.pg,.yp{margin:0 auto 14px;box-shadow:0 2px 10px rgb(0 0 0 / .18)}.yp .pg{margin:0;box-shadow:none}` : ''}
.pg{width:${w}mm;height:${h}mm;padding:${kt}mm ${ks}mm ${ka}mm ${kl}mm;position:relative;overflow:hidden;background:${zemin};break-after:page;page-break-after:always}
.pg.cift{padding:${kt}mm ${kl}mm ${ka}mm ${ks}mm}
.pg:last-child{break-after:auto;page-break-after:auto}
.yp{width:${yp.w}mm;height:${yp.h}mm;display:flex;justify-content:center;align-items:center;overflow:hidden;background:${zemin};break-after:page;page-break-after:always;position:relative}
.yp:last-child{break-after:auto;page-break-after:auto}
.yp>div{width:${(w * yp.olcek).toFixed(3)}mm;height:${(h * yp.olcek).toFixed(3)}mm;overflow:hidden;flex:none;position:relative}
.yp>div>.pg{transform:scale(${yp.olcek.toFixed(5)});transform-origin:0 0;break-after:auto;page-break-after:auto}
${a.yaprak === 'kitapcik' && !onizleme ? '' : a.yaprak !== 'tek' ? `.yp>div+div::before{content:'';position:absolute;left:-.3pt;top:0;bottom:0;border-left:.3pt dashed ${R('kesim')};opacity:.6}` : ''}
.pg-in{height:100%;position:relative;${a.cerceve ? `border:${a.cerceveKalin}pt ${a.cerceveStil} ${a.cerceveRenk};border-radius:${a.cerceveYaricap}mm;padding:${ic}mm;` : ''}${desen}}
.pg-logo{height:${a.logoYuk}mm;width:auto;max-width:60mm;object-fit:contain;flex:none;display:block}
.pg-not{height:${a.notAlani + NOT_PAY_MM}mm;padding-top:${NOT_PAY_MM - 1.5}mm;position:relative;z-index:1;overflow:hidden}
.pg-not b{display:block;font-size:${Math.max(6.5, a.punto * 0.72)}pt;color:${R('altBilgi')};line-height:1.2;margin-bottom:.6mm;font-weight:600}
.pg-not i{display:block;height:${(a.punto * a.satir * 1.35).toFixed(2)}pt;border-bottom:.5pt solid ${R('notCizgi')}}
.fil{position:absolute;inset:0;display:grid;place-items:center;pointer-events:none;z-index:0}
.fil span{transform:rotate(-32deg);font-size:${Math.min(w, h) / 7}mm;font-weight:800;font-family:${basF};color:${R('filigran')};opacity:.06;white-space:nowrap;letter-spacing:.04em}
.pg-bas{height:${BASLIK_MM}mm;display:flex;align-items:flex-end;justify-content:space-between;gap:6mm;padding-bottom:2.2mm;border-bottom:1.1pt solid ${R('baslikCizgi')};position:relative;z-index:1;${baslikKutu}}
.pg-bas.orta{justify-content:center;text-align:center}
.pg-bas.orta .bl{flex:1}
.pg-bas h1{margin:0;font-family:${basF};font-size:${Math.min(16, a.punto * a.baslikOran)}pt;line-height:1.15;color:${baslikRenk};font-weight:${a.baslikAgirlik};${buyukCss(a.baslikBuyuk)}white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pg-bas p{margin:.6mm 0 0;font-size:${Math.max(7, a.punto * 0.8)}pt;line-height:1.2;color:${baslikAlt};white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pg-bas .bl{min-width:0;display:flex;align-items:flex-end;gap:3mm}
.pg-bas .bl>div{min-width:0}
.pg-bas .br{flex:none;display:grid;gap:1.6mm;font-size:${Math.max(7, a.punto * 0.78)}pt;color:${baslikAlt};text-align:left}
.pg-bas .br span{display:flex;gap:2mm;align-items:flex-end}
.pg-bas .br i{display:inline-block;width:42mm;border-bottom:.6pt solid ${baslikAlt};height:1em}
.pg-bant{height:${GRUP_MM}mm;display:flex;align-items:center;gap:2.5mm;font-family:${basF};font-weight:${a.baslikAgirlik};font-size:${Math.max(8, a.punto * 1.05)}pt;color:${R('bant')};${buyukCss(a.grupBuyuk)}border-bottom:.6pt solid ${R('anahtarKenar')};position:relative;z-index:1;white-space:nowrap;overflow:hidden}
.pg-bant::before{content:'';width:2.6mm;height:2.6mm;border-radius:1mm;background:var(--bk,${R('bant')});flex:none}
.pg-gv{position:relative;z-index:1;overflow:hidden}
.pg-serit{height:${SERIT_MM}mm;border-top:.6pt dashed ${R('ayirici')};padding-top:1.4mm;font-size:${Math.max(6.5, a.punto * 0.72)}pt;line-height:1.35;color:${R('cozumMetin')};overflow:hidden;position:relative;z-index:1}
.pg-serit b{color:${R('cevapHarfi')}}
.pg-alt{height:${ALT_MM}mm;display:flex;align-items:flex-end;justify-content:space-between;gap:3mm;font-size:${Math.max(6.5, a.punto * 0.72)}pt;color:${R('altBilgi')};position:relative;z-index:1;${a.altCizgi ? `border-top:.5pt solid ${R('anahtarKenar')};` : ''}}
.pg-alt>span{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.pg-alt>span:nth-child(2){text-align:center}.pg-alt>span:nth-child(3){text-align:right}
.izg{display:grid;height:100%}
.hc{overflow:hidden;position:relative;min-width:0}
.hc.cer{border:.7pt solid ${R('hucreKenar')};border-radius:${Math.max(0.5, a.kutuYaricap)}mm;padding:${HUCRE_IC}mm}
${a.kesimCizgi ? `.izg.kes{position:relative}.izg.kes .hc{outline:.35pt dashed ${R('kesim')};outline-offset:${(a.hucreAralik / 2).toFixed(2)}mm}` : ''}
.akis{display:flex;height:100%;gap:${KOLON_ARA}mm}
.kol{position:relative;min-width:0}
${a.sutunCizgi ? `.kol+.kol::before{content:'';position:absolute;left:-${KOLON_ARA / 2}mm;top:0;bottom:0;border-left:.6pt solid ${R('sutunCizgi')}}` : ''}
.sb,.cb,.gb{font-size:calc(${a.punto}pt * var(--k,1));line-height:${a.satir};padding-bottom:calc(${a.soruArasi}mm * var(--k,1));break-inside:avoid;position:relative}
.sb{${a.iki ? 'text-align:justify;hyphens:auto;' : ''}}
${soruKutu ? `.sb.kt{${soruKutu}padding-bottom:${a.kutuIc}mm;margin-bottom:calc(${a.soruArasi}mm * var(--k,1))}.hc>.sb.kt{margin-bottom:0;min-height:100%}.sb.kt.ay{border-bottom:${cizgi(a.ayirici, R('ayirici'))}}` : ''}
${a.asiliGirinti ? `.sb .kok{display:flex;gap:.35em;align-items:baseline}.sb .kok .no{margin-right:0;flex:0 0 auto;white-space:nowrap;min-width:var(--nw,1.6em)}.sb .kok .km{flex:1 1 0;min-width:0}.sb .sk{padding-left:calc(var(--nw,1.6em) + .35em + ${a.sikGirinti}mm)}` : ''}
.sb.ay{border-bottom:${cizgi(a.ayirici, R('ayirici'))};margin-bottom:calc(${a.soruArasi * 0.5}mm * var(--k,1))}
.hc>.sb,.hc>.cb{padding-bottom:0;border-bottom:0;margin-bottom:0}
.sb.r-serit,.cb.r-serit{border-left:1.2mm solid var(--rk);padding-left:2.6mm}
.sb.r-zemin,.cb.r-zemin{background:color-mix(in srgb,var(--rk) 9%,${zemin});border-radius:1.6mm;padding:2mm 2.4mm calc(2mm + ${a.soruArasi * 0.4}mm * var(--k,1));margin-bottom:calc(${a.soruArasi * 0.5}mm * var(--k,1))}
.hc>.sb.r-zemin,.hc>.cb.r-zemin{min-height:100%;margin-bottom:0}
.et{display:flex;flex-wrap:wrap;gap:1.2mm;margin:0 0 calc(${a.paragraf}pt * var(--k,1));align-items:flex-start}
.et.alt{margin:calc(${a.paragraf}pt * var(--k,1)) 0 0}
.et.d-sag{justify-content:flex-end}.et.d-orta{justify-content:center}.et.d-dikey{flex-direction:column;gap:.6mm}
.et span{--ek:#64748b;font-size:${a.etiketBoyut}em;line-height:1.3;padding:.15em .55em;border-radius:99px;background:color-mix(in srgb,var(--ek) 13%,${zemin});color:color-mix(in srgb,var(--ek) 78%,${a.metinRenk});font-weight:${a.etiketKalin ? 600 : 400};letter-spacing:0;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.et.s-kutu span{border-radius:.3em}.et.s-kose span{border-radius:0}
.et.s-cizgi span{background:none;border:.5pt solid color-mix(in srgb,var(--ek) 55%,${zemin});color:color-mix(in srgb,var(--ek) 85%,${a.metinRenk})}
.et.s-duz{gap:.2em}.et.s-duz span{background:none;padding:0;color:color-mix(in srgb,var(--ek) 85%,${a.metinRenk})}
.et.s-duz span+span::before{content:'·';margin-right:.45em;color:${R('ayirici')}}
${a.etiketRenk === 'ozel' ? `.et span:not(.rk){background:${a.etiketZemin};color:${a.etiketMetin}}.et.s-cizgi span:not(.rk){background:none;border-color:${a.etiketMetin}}.et.s-duz span:not(.rk){background:none}` : ''}
.kok{margin:0 0 calc(${a.paragraf}pt * var(--k,1));color:${R('kok')};${kokStil}overflow-wrap:anywhere}
.no{margin-right:.35em;font-style:normal;${numara}}
.sb.r-numara .no{display:inline-block;background:var(--rk);color:${zemin};border:0;border-radius:.3em;padding:0 .35em;min-width:1.6em;text-align:center;text-decoration:none}
.sk{list-style:none;margin:0;padding:0 0 0 ${a.sikGirinti}mm;display:grid;gap:calc(${a.sikAralik}pt * var(--k,1)) 4mm;color:${R('sik')};font-size:${a.sikOran}em;${stilCss(a.sikStil)}}
.sk.iki{grid-template-columns:1fr 1fr}
.sk.yan{display:flex;flex-wrap:wrap;gap:.2em 1.4em}
.sk li{display:flex;gap:.35em;min-width:0;overflow-wrap:anywhere;align-items:baseline}
.sk .hf{flex:none;font-style:normal;${sikHarf}}
.sk li.dg>span{${isaret}}
${a.isaretStil === 'daire' ? `.sk li.dg .hf{border:.13em solid ${dogru};border-radius:99px;padding:0 .2em;color:${dogru};background:none}` : ''}
${a.isaretStil === 'tik' ? `.sk li.dg>span::after{content:' ✓';color:${dogru}}` : ''}
.yz{margin-top:calc(${a.paragraf}pt * var(--k,1))}
.yz i{display:block;height:${(a.punto * a.satir * 1.35).toFixed(2)}pt;border-bottom:.5pt solid ${R('yazmaCizgi')}}
.cz{margin-top:calc(${a.paragraf * 1.5}pt * var(--k,1));${cozumKutu}color:${R('cozumMetin')};font-size:.9em}
.cb{color:${R('cozumMetin')}}
.cz p,.cb p{margin:0 0 .35em}
.cz ul,.cb ul{margin:0;padding:0;list-style:none;display:grid;gap:.2em}
.cz li,.cb li{display:flex;gap:.35em}
.cz li b,.cb li b{flex:none}
.cz li.dg,.cb li.dg{color:${dogru}}
.cvp{font-weight:800;color:${R('cevapHarfi')}}
.kay{color:${R('kaynak')};font-size:.88em}
.cb .cb-bas{display:flex;align-items:baseline;gap:.5em;margin-bottom:.3em}
.gb{font-family:${basF};font-weight:${a.baslikAgirlik};color:var(--rk,${R('grup')});${buyukCss(a.grupBuyuk)}font-size:calc(${a.punto * 1.12}pt * var(--k,1));padding:.2em 0 .25em;margin-bottom:calc(${a.soruArasi * 0.5}mm * var(--k,1));display:flex;align-items:baseline;gap:.5em;min-width:0}
.gb>span{min-width:0;overflow:hidden;text-overflow:ellipsis}
.gb em{font-style:normal;font-weight:600;font-size:.78em;color:${R('altBilgi')};flex:none;text-transform:none;font-variant-caps:normal;letter-spacing:0}
.gb.s0{font-size:calc(${a.punto * 1.28}pt * var(--k,1))}.gb.s1{font-size:calc(${a.punto * 1.12}pt * var(--k,1))}.gb.s2{font-size:calc(${a.punto * 1.0}pt * var(--k,1));font-weight:700}.gb.s3{font-size:calc(${a.punto * 0.92}pt * var(--k,1));font-weight:700}
.gb.s1{margin-left:1.5mm}.gb.s2{margin-left:3mm}.gb.s3{margin-left:4.5mm}
.gb.ic{margin-left:0;font-size:calc(${a.punto * 0.95}pt * var(--k,1));padding:.1em 0 .15em;margin-bottom:calc(${a.paragraf}pt * var(--k,1))}.gb.ic.s2,.gb.ic.s3{font-size:calc(${a.punto * 0.86}pt * var(--k,1))}
${a.grupStil === 'cizgi' ? `.gb{border-bottom:.8pt solid color-mix(in srgb,var(--rk,${R('grup')}) 55%,${zemin})}.gb.s2,.gb.s3{border-bottom-width:.5pt}` : ''}
${a.grupStil === 'bant' ? `.gb{background:color-mix(in srgb,var(--rk,${R('grup')}) 10%,${zemin});border-left:1.2mm solid var(--rk,${R('grup')});padding:.3em .7em;border-radius:0 .3em .3em 0}.gb.s2,.gb.s3{background:color-mix(in srgb,var(--rk,${R('grup')}) 5%,${zemin})}` : ''}
${a.grupStil === 'kutu' ? `.gb{border:.6pt solid color-mix(in srgb,var(--rk,${R('grup')}) 55%,${zemin});padding:.25em .7em;border-radius:.35em}` : ''}
${a.grupStil === 'sade' ? `.gb{padding:.1em 0}` : ''}
.ank{display:grid;gap:1.2mm}
.ank div{height:${ANAHTAR_H - 1.2}mm;display:flex;align-items:center;justify-content:space-between;padding:0 2mm;border:.6pt solid ${R('anahtarKenar')};border-radius:1.2mm;font-size:${Math.max(8, a.punto * 0.92)}pt;border-left:1.1mm solid var(--rk,${R('anahtarKenar')})}
.ank b{font-weight:800}
.ank i{font-style:normal;font-weight:800;color:${R('cevapHarfi')}}
.opt{display:grid;column-gap:5mm}
.opt div{height:${OPTIK_H}mm;display:flex;align-items:center;gap:1.6mm;font-size:8pt;border-bottom:.4pt solid color-mix(in srgb,${R('anahtarKenar')} 50%,${zemin})}
.opt b{width:8mm;text-align:right;font-weight:700}
.opt i{width:4.6mm;height:4.6mm;border-radius:50%;border:.6pt solid ${R('altBilgi')};display:grid;place-items:center;font-style:normal;font-size:6pt;color:${R('altBilgi')}}
.kp{height:100%;display:flex;flex-direction:column;justify-content:center;gap:7mm;padding:0 6mm;position:relative;z-index:1}
${a.kapakStil === 'bant' ? `.kp{border-left:4mm solid ${vurgu};padding-left:8mm}` : ''}
${a.kapakStil === 'zemin' ? `.pg.kpk{background:${vurgu}}.pg.kpk .pg-in{border-color:color-mix(in srgb,${zemin} 50%,${vurgu})}.kp{color:${zemin}}.kp .ust,.kp h1,.kp h2,.kp .sy b,.kp .sy span,.kp .not,.kp .alan,.kp .lj{color:${zemin}}.kp .sy div{border-color:color-mix(in srgb,${zemin} 55%,${vurgu})}.kp .yon{background:color-mix(in srgb,${zemin} 14%,${vurgu});border-color:${zemin};color:${zemin}}.kp .alan i{border-color:${zemin}}.kp .kpn{color:${zemin}}` : ''}
.kp .kpn{margin:0;font-size:10pt;line-height:1.5;white-space:pre-wrap;color:${R('cozumMetin')}}
.kp .pg-logo{height:${Math.max(a.logoYuk, 14)}mm;max-width:80mm}
.kp .ust{font-size:9pt;letter-spacing:.18em;text-transform:uppercase;color:${vurgu};font-weight:800}
.kp h1{margin:0;font-family:${basF};font-size:30pt;line-height:1.08;color:${R('kapakBaslik')};font-weight:${a.baslikAgirlik};${buyukCss(a.baslikBuyuk)}}
.kp h2{margin:0;font-size:13pt;font-weight:500;color:${R('altBilgi')}}
.kp .sy{display:flex;flex-wrap:wrap;gap:3mm}
.kp .sy div{border:.7pt solid ${R('anahtarKenar')};border-radius:2mm;padding:3mm 4mm;min-width:32mm}
.kp .sy b{display:block;font-size:17pt;color:${vurgu}}
.kp .sy span{font-size:8.5pt;color:${R('altBilgi')}}
.kp .yon{border-left:1.2mm solid ${R('cozumKenar')};background:${cozumZeminCss(a)};padding:3mm 4mm;font-size:9pt;line-height:1.5;color:${R('cozumMetin')}}
.kp .alan{display:grid;gap:5mm;font-size:10pt}
.kp .alan span{display:flex;gap:3mm;align-items:flex-end}
.kp .alan i{flex:1;border-bottom:.7pt solid ${R('altBilgi')};height:1.2em}
.kp .not{color:${R('altBilgi')}}
.lj{display:flex;flex-wrap:wrap;gap:2mm 4mm;font-size:8.5pt}
.lj span{display:flex;align-items:center;gap:1.4mm}
.lj i{width:3mm;height:3mm;border-radius:.8mm;background:var(--rk)}
${a.ozelCss ? `\n/* özel */\n${a.ozelCss.replace(/<\/style/gi, '')}` : ''}
`;
}
/** Google Fonts bağlantıları (önizleme, ölçüm ve sunucu PDF'i) */
export const yaziLinkHtml = (a: Ayar) => {
  const l = yaziBaglantilari(a);
  return l.length ? `<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>${l.map((h) => `<link rel="stylesheet" href="${h}">`).join('')}` : '';
};

/* ---------------------------------------------------------------------------
 * Blok HTML
 * ------------------------------------------------------------------------- */
const renkSinif = (h: HS, a: Ayar) => (h.renk ? ` r-${a.renkStil}` : '');
const renkStil = (h: HS) => (h.renk ? `--rk:${h.renk};` : '');

function etiketHtml(h: HS, a: Ayar, yer: 'ust' | 'alt'): string {
  if (a.etiketYeri !== yer) return '';
  const e = etiketler(h, a);
  if (!e.length) return '';
  const sinif = `et${yer === 'alt' ? ' alt' : ''} d-${a.etiketDizilim} s-${a.etiketSekil}`;
  return `<div class="${sinif}">${e.map((x) => `<span${x.renkli ? ' class="rk"' : ''} style="--ek:${x.renk}">${esc(x.ad)}</span>`).join('')}</div>`;
}

export function cozumGovdeHtml(c: CozumIcerik, a: Ayar): string {
  return [
    c.harf ? `<p><span class="cvp">Cevap: ${esc(c.harf)}</span></p>` : '',
    c.aciklama ? `<p>${zengin(c.aciklama)}</p>` : '',
    c.siklar.length ? `<ul>${c.siklar.map((x) => `<li${x.dogru ? ' class="dg"' : ''}><b>${esc(harfMetni(x.k, a))}</b><span>${zengin(x.t)}</span></li>`).join('')}</ul>` : '',
    c.kaynak ? `<p class="kay">${esc(c.kaynak)}</p>` : '',
  ].join('');
}

export function soruHtml(h: HS, a: Ayar, k = 1, o: { isaret?: boolean; satir?: boolean; ayirici?: boolean; basliklar?: GrupBlok[] } = {}): string {
  const isaret = o.isaret ?? a.dogruIsaret;
  const altinda = a.cozumYeri === 'altinda' ? cozumIcerik(h, a) : null;
  const sk = a.secenekDuzen === 'iki' ? ' iki' : a.secenekDuzen === 'yan' ? ' yan' : '';
  const ay = (o.ayirici ?? true) && a.ayirici !== 'yok' ? ' ay' : '';
  const kt = a.soruKutu !== 'yok' ? ' kt' : '';
  const nw = a.asiliGirinti ? `--nw:${(numaraMetni(h.no, a).length * 0.62 + 0.3).toFixed(2)}em;` : '';
  return `<div class="sb${renkSinif(h, a)}${ay}${kt}" style="${renkStil(h)}${nw}--k:${k}">`
    + (o.basliklar || []).map((b) => grupHtml(b, a, k, true)).join('')
    + etiketHtml(h, a, 'ust')
    + `<div class="kok"><span class="no">${esc(numaraMetni(h.no, a))}</span><span class="km">${zengin(h.q.stem)}</span></div>`
    + `<ol class="sk${sk}">${h.secenek.map((x) => `<li${isaret && x.key === h.dogru ? ' class="dg"' : ''}><b class="hf">${esc(harfMetni(x.key, a))}</b><span>${zengin(x.text)}</span></li>`).join('')}</ol>`
    + etiketHtml(h, a, 'alt')
    + ((o.satir ?? true) && a.yazmaSatiri > 0 ? `<div class="yz">${'<i></i>'.repeat(a.yazmaSatiri)}</div>` : '')
    + (altinda && !cozumBos(altinda) ? `<div class="cz">${cozumGovdeHtml(altinda, a)}</div>` : '')
    + `</div>`;
}

export function cozumHtml(h: HS, a: Ayar, k = 1): string {
  const c = cozumIcerik(h, a);
  if (!c.harf) c.harf = h.dogru || '—';
  return `<div class="cb${renkSinif(h, a)}" style="${renkStil(h)}--k:${k}"><div class="cb-bas"><span class="no">${esc(numaraMetni(h.no, a))}</span></div>${cozumGovdeHtml(c, a)}</div>`;
}
/** ic: ızgara hücresinin içinde (küçük, girintisiz) */
const grupHtml = (b: GrupBlok, a: Ayar, k = b.k, ic = false) =>
  `<div class="gb s${Math.min(3, b.seviye)}${ic ? ' ic' : ''}" style="${b.renk ? `--rk:${b.renk};` : ''}--k:${k}"><span>${esc(b.ad)}</span>${a.grupSayi ? `<em>${b.sayi} soru</em>` : ''}</div>`;

const blokHtml = (b: Blok, a: Ayar) =>
  b.t === 'soru' ? soruHtml(b.h, a, b.k, { ayirici: !b.basliklar, basliklar: b.basliklar }) : b.t === 'cozum' ? cozumHtml(b.h, a, b.k) : grupHtml(b, a);

/* ---------------------------------------------------------------------------
 * Ölçüm: gizli çerçevede aynı CSS ile blok yükseklikleri (px)
 * ------------------------------------------------------------------------- */
export class Olcer {
  private f: HTMLIFrameElement;
  private d!: Document;
  private kap!: HTMLElement;
  constructor(private a: Ayar) {
    this.f = document.createElement('iframe');
    this.f.setAttribute('aria-hidden', 'true');
    this.f.tabIndex = -1;
    Object.assign(this.f.style, { position: 'fixed', left: '-12000px', top: '0', width: '4000px', height: '400px', visibility: 'hidden', border: '0' });
    document.body.appendChild(this.f);
  }
  async hazir() {
    const d = this.f.contentDocument!;
    d.open();
    d.write(`<!doctype html><html><head><meta charset="utf-8">${yaziLinkHtml(this.a)}<style>${belgeCss(this.a)}</style></head><body><div id="k"></div></body></html>`);
    d.close();
    this.d = d;
    this.kap = d.getElementById('k')!;
    try { await (d as any).fonts?.ready; } catch { /* yazı tipi beklenemedi */ }
    return this;
  }
  /** Çok sayıda bloğu tek düzen geçişinde ölçer */
  toplu(list: { html: string; w: number }[]): number[] {
    this.kap.innerHTML = list.map((x) => `<div style="width:${x.w}mm;display:flow-root">${x.html}</div>`).join('');
    const out = Array.from(this.kap.children).map((c) => (c as HTMLElement).getBoundingClientRect().height);
    this.kap.innerHTML = '';
    return out;
  }
  tek(html: string, w: number): number { return this.toplu([{ html, w }])[0]; }
  /** Yükseklik sınırına sığana dek yazı ölçeğini küçültür (k0: başlangıç/genel ölçek, ilkH: k0'daki ölçülmüş yükseklik) */
  sigdir(html: (k: number) => string, w: number, hMax: number, ilkH?: number, k0 = 1): { k: number; tasma?: boolean } {
    let h = ilkH ?? this.tek(html(k0), w);
    if (h <= hMax) return { k: k0 };
    let k = Math.max(MIN_K, Math.min(0.98 * k0, k0 * Math.sqrt(hMax / h) * 0.99));
    for (let i = 0; i < 8; i++) {
      h = this.tek(html(k), w);
      if (h <= hMax) return { k: Math.round(k * 1000) / 1000 };
      if (k <= MIN_K) break;
      k = Math.max(MIN_K, k * Math.min(0.97, Math.sqrt(hMax / h) * 0.995));
    }
    return { k: MIN_K, tasma: true };
  }
  /** Sığan en büyük ölçek: [k0, kMax] aralığında büyütür; k0'da bile sığmıyorsa küçültür */
  enBuyuk(html: (k: number) => string, w: number, hMax: number, k0: number, kMax: number, ilkH?: number): { k: number; tasma?: boolean } {
    const h = ilkH ?? this.tek(html(k0), w);
    if (h > hMax) return this.sigdir(html, w, hMax, h, k0);
    if (kMax <= k0) return { k: k0 };
    if (this.tek(html(kMax), w) <= hMax) return { k: kMax };
    let lo = k0;
    let hi = kMax;
    for (let i = 0; i < 6 && hi - lo > 0.02; i++) {
      const k = (lo + hi) / 2;
      if (this.tek(html(k), w) <= hMax) lo = k; else hi = k;
    }
    return { k: Math.round(lo * 1000) / 1000 };
  }
  kapat() { this.f.remove(); }
}

/* ---------------------------------------------------------------------------
 * Sayfalama
 * ------------------------------------------------------------------------- */
const pxMm = (mm: number) => mm * PX_MM;

/**
 * Sayfalar. `sigdir` açıksa genel yazı ölçeğini (k0) arar: hedef sayfa sayısı verilmişse ona, verilmemişse seyrek
 * (gövdesinin %45'inden azı dolu) bölüm sonu sayfalarını kaldıracak sayfa sayısına sığan EN BÜYÜK ölçek seçilir.
 * "kucult" yalnız küçültür (k0 ≤ 1); "doldur" sayfalar dolsun diye büyütür de (k0 ≤ SIGDIR_MAX). Izgarada sayfa
 * sayısı hücre sayısından gelir; orada "doldur" her sayfada hücrelere sığan ortak en büyük ölçeği uygular.
 */
export async function sayfala(hs: HS[], a: Ayar, o: { olcer?: Olcer; tahminToplam?: number } = {}): Promise<Belge> {
  const olcer = o.olcer || (await new Olcer(a).hazir());
  try {
    if (a.sigdir === 'yok' || !hs.length || a.duzen !== 'akis') return sayfalaEs(hs, a, olcer, o.tahminToplam, 1);
    return sigdirarak(hs, a, olcer, o.tahminToplam);
  } finally {
    if (!o.olcer) olcer.kapat();
  }
}

/** İçerik sayfası sayısı (kapak/anahtar/optik dışı; "arkada" çözüm sayfaları soru sayfasını aynalar, sayılmaz) ve seyrek bölüm sonu sayısı */
export function sigdirOlcut(b: Belge, a: Ayar): { n: number; seyrek: number } {
  const icerik = b.sayfalar.filter((p) => (p.tur === 'soru' || p.tur === 'cozum') && !(a.cozumYeri === 'arkada' && p.tur === 'cozum'));
  let seyrek = 0;
  icerik.forEach((p, i) => {
    const son = i === icerik.length - 1 || icerik[i + 1].yeniBolum || icerik[i + 1].tur !== p.tur;
    const ilk = i === 0 || icerik[i].yeniBolum || icerik[i - 1].tur !== p.tur;
    // tek sayfalık bölüm seyrek sayılmaz (kaldırılacak sayfa yok)
    if (son && !ilk && (p.dolu ?? 1) < SEYREK) seyrek++;
  });
  return { n: icerik.length, seyrek };
}

function sigdirarak(hs: HS[], a: Ayar, olcer: Olcer, tahminToplam?: number): Belge {
  const dene = (k: number) => { const b = sayfalaEs(hs, a, olcer, tahminToplam, k); return { b, ...sigdirOlcut(b, a) }; };
  const ilk = dene(1);
  const hedef = a.sigdirHedef > 0 ? a.sigdirHedef : Math.max(1, ilk.n - ilk.seyrek);
  const ust = a.sigdir === 'doldur' ? SIGDIR_MAX : 1;
  const sigar = (r: { n: number }) => r.n <= hedef;
  let iyi: { k: number; b: Belge } | null = sigar(ilk) ? { k: 1, b: ilk.b } : null;
  if (iyi && ust <= 1) return iyi.b;
  let lo: number;
  let hi: number;
  if (iyi) {
    const enUst = dene(ust);
    if (sigar(enUst)) return enUst.b;
    lo = 1;
    hi = ust;
  } else {
    const enAlt = dene(SIGDIR_MIN);
    if (!sigar(enAlt)) {
      // hedefe en küçük ölçekte de ulaşılamıyor: elle verilen hedefte en küçük ölçek, kendiliğinde doğal ölçek
      return a.sigdirHedef > 0
        ? { ...enAlt.b, sigdirNot: `${a.sigdirHedef} sayfaya en küçük ölçekte de sığmadı (${enAlt.n} sayfa oldu).` }
        : { ...ilk.b, sigdirNot: 'Seyrek son sayfa en küçük ölçekte de kaldırılamadı; doğal ölçek kullanıldı.' };
    }
    iyi = { k: SIGDIR_MIN, b: enAlt.b };
    lo = SIGDIR_MIN;
    hi = 1;
  }
  // ikili arama: sığan en büyük ölçek (hassasiyet ≈ %1)
  for (let i = 0; i < 7 && hi - lo > 0.01; i++) {
    const k = Math.round(((lo + hi) / 2) * 1000) / 1000;
    const r = dene(k);
    if (sigar(r)) { iyi = { k, b: r.b }; lo = k; } else hi = k;
  }
  return iyi.b;
}

/**
 * Her sorunun önüne gelecek katman başlıkları: grubun ilk sorusunda, değişen katmandan itibaren (alt katmanlar dahil).
 * `alt`: bu katmandan küçük seviyeler atlanır (ızgarada en üst katman sayfa bandıdır, hücreye yalnız alt katmanlar yazılır).
 */
function katmanBasliklari(hs: HS[], a: Ayar, k0: number, alt = 0): GrupBlok[][] {
  const n = a.gruplar.length;
  let onceki: string[] | null = null;
  return hs.map((h, i) => {
    const out: GrupBlok[] = [];
    if (n) {
      let d = 0;
      if (onceki) while (d < n && onceki[d] === h.gruplar[d]) d++;
      for (let sv = Math.max(d, alt); sv < n; sv++) {
        let j = i;
        while (j < hs.length && h.gruplar.slice(0, sv + 1).every((v, t) => hs[j].gruplar[t] === v)) j++;
        out.push({ t: 'grup', ad: h.gruplar[sv], renk: h.grupRenk[sv], seviye: sv, sayi: j - i, k: k0 });
      }
      onceki = h.gruplar;
    }
    return out;
  });
}
/** Akış: başlık blokları + soru/çözüm blokları sırayla */
function grupBloklari(hs: HS[], a: Ayar, k0: number, yap: (h: HS) => Blok): Blok[] {
  const basliklar = katmanBasliklari(hs, a, k0);
  return hs.flatMap((h, i) => [...basliklar[i], yap(h)]);
}
/** En iç katmanın rengi (ızgara bandı için) */
const bantRenk = (h: HS): string | null => { for (let i = h.grupRenk.length - 1; i >= 0; i--) if (h.grupRenk[i]) return h.grupRenk[i]; return null; };

function sayfalaEs(hs: HS[], a: Ayar, olcer: Olcer, tahminToplam: number | undefined, k0: number): Belge {
  const sayfalar: Sayfa[] = [];
  let tasan = 0;
  let ilkSoru = true;
  const serit = a.cozumYeri === 'sayfaAlti';
  const ilkMi = () => { const v = ilkSoru; ilkSoru = false; return v; };
  const grupVar = a.gruplar.length > 0;
  const html = (b: Blok, k = k0) => (b.t === 'soru' ? soruHtml(b.h, a, k) : b.t === 'cozum' ? cozumHtml(b.h, a, k) : grupHtml(b, a, k));

  if (a.kapak) sayfalar.push({ tur: 'kapak', g: govde({ ...a, baslikAcik: false, sayfaNo: false, altMetin: '' }, { ilk: false, serit: false, grup: false }) });

  /* ---- ızgara: en üst katman sayfa bandı + sayfa kırılımı; alt katmanlar hücre içinde küçük başlık ---- */
  if (a.duzen !== 'akis') {
    const n = a.duzen;
    const { sut, sat } = izgara(a, n);
    const buyut = a.sigdir === 'doldur';
    const basliklar = katmanBasliklari(hs, a, k0, 1);
    let i = 0;
    while (i < hs.length) {
      const g = govde(a, { ilk: ilkMi(), serit, grup: grupVar });
      const cw = (g.w - (sut - 1) * a.hucreAralik) / sut;
      const ch = (g.h - (sat - 1) * a.hucreAralik) / sat;
      const icW = a.hucreCerceve ? cw - HUCRE_IC * 2 - 0.5 : cw;
      const icH = pxMm(a.hucreCerceve ? ch - HUCRE_IC * 2 - 0.5 : ch);
      const grup = hs[i].gruplar[0] ?? '';
      const bas = i;
      const parca: HS[] = [];
      while (i < hs.length && parca.length < n && (!grupVar || hs[i].gruplar[0] === grup)) parca.push(hs[i++]);
      const html = (h: HS, j: number, k: number) => soruHtml(h, a, k, { ayirici: false, basliklar: basliklar[bas + j] });
      const olc = olcer.toplu(parca.map((h, j) => ({ html: html(h, j, k0), w: icW })));
      const sig = parca.map((h, j) => (buyut
        ? olcer.enBuyuk((k) => html(h, j, k), icW, icH, k0, SIGDIR_MAX, olc[j])
        : olcer.sigdir((k) => html(h, j, k), icW, icH, olc[j], k0)));
      // "doldur": sayfadaki hücreler ortak ölçek alır (küçülmek zorunda kalan hücre kendi ölçeğinde kalır)
      const ortak = buyut ? Math.min(...sig.map((f) => Math.max(f.k, k0))) : k0;
      const hucre: (Blok | null)[] = parca.map((h, j) => {
        const f = sig[j];
        if (f.tasma) tasan++;
        return { t: 'soru', h, k: buyut && f.k >= k0 ? ortak : f.k, tasma: f.tasma, basliklar: basliklar[bas + j].length ? basliklar[bas + j] : undefined };
      });
      while (hucre.length < n) hucre.push(null);
      const bant = grupVar ? { ad: grup, renk: parca[0].grupRenk[0] ?? bantRenk(parca[0]) } : undefined;
      sayfalar.push({ tur: 'soru', g, izgara: { sut, sat, cw, ch }, hucre, bant, dolu: parca.length / n, serit: serit ? parca.map((h) => ({ no: h.no, harf: h.dogru || '—' })) : undefined });
      if (a.cozumYeri === 'arkada') {
        const g2 = govde(a, { ilk: false, serit: false, grup: grupVar });
        const ch2 = (g2.h - (sat - 1) * a.hucreAralik) / sat;
        const icH2 = pxMm(a.hucreCerceve ? ch2 - HUCRE_IC * 2 - 0.5 : ch2);
        let arka: (Blok | null)[] = parca.map((h) => {
          const f = olcer.sigdir((k) => cozumHtml(h, a, k), icW, icH2, undefined, k0);
          return { t: 'cozum', h, k: f.k, tasma: f.tasma };
        });
        while (arka.length < n) arka.push(null);
        if (a.arkaAyna && sut > 1) {
          const satirlar: (Blok | null)[] = [];
          for (let r = 0; r < sat; r++) satirlar.push(...arka.slice(r * sut, r * sut + sut).reverse());
          arka = satirlar;
        }
        sayfalar.push({ tur: 'cozum', g: g2, izgara: { sut, sat, cw, ch: ch2 }, hucre: arka, dolu: parca.length / n, bant: { ad: `Çözümler${bant ? ` · ${bant.ad}` : ''}`, renk: bant?.renk || null } });
      }
    }
  }

  /* ---- akış ---- */
  function akisYerlestir(bloklar: Blok[], tur: 'soru' | 'cozum', bolum?: string) {
    const sut = a.sutun;
    const yeni = (yeniBolum = false) => {
      const g = govde(a, { ilk: tur === 'soru' ? ilkMi() : false, serit: tur === 'soru' && serit, grup: !!bolum });
      const kw = (g.w - (sut - 1) * KOLON_ARA) / sut;
      const p: Sayfa = { tur, g, kolon: Array.from({ length: sut }, () => []), kolonW: kw, bant: bolum ? { ad: bolum, renk: null } : undefined, serit: tur === 'soru' && serit ? [] : undefined, dolu: 0, yeniBolum };
      sayfalar.push(p);
      return p;
    };
    if (!bloklar.length) return;
    let p = yeni();
    const yuk = olcer.toplu(bloklar.map((b) => ({ html: html(b), w: p.kolonW! })));
    let kol = 0;
    let kalan = pxMm(p.g.h);
    const kullan = (h: number) => { kalan -= h; p.dolu = (p.dolu || 0) + h / (sut * pxMm(p.g.h)); };
    const sonraki = (zorla = false) => {
      if (!zorla && kol < a.sutun - 1) { kol++; kalan = pxMm(p.g.h); return; }
      // ızgaradaki "arkada" çözümü akışta: soru sayfası bitince çözümleri ayrı sayfada
      if (tur === 'soru' && a.cozumYeri === 'arkada') bekleyen();
      p = yeni(zorla);
      kol = 0;
      kalan = pxMm(p.g.h);
    };
    let sayfaHs: HS[] = [];
    const bekleyen = () => {
      const l = sayfaHs;
      sayfaHs = [];
      if (l.length) akisCoz(l);
    };
    let oncekiGrup: string | null = null;
    for (let i = 0; i < bloklar.length; i++) {
      const b = bloklar[i];
      let h = yuk[i];
      if (b.t === 'grup') {
        if (a.grupYeniSayfa && b.seviye === 0 && oncekiGrup !== null && p.kolon!.some((c) => c.length)) sonraki(true);
        if (b.seviye === 0) oncekiGrup = b.ad;
        // başlık dizisi (ardışık katmanlar) bir sonraki blokla birlikte kalır
        if (i === 0 || bloklar[i - 1].t !== 'grup') {
          let j = i;
          let birlikte = 0;
          while (j < bloklar.length && bloklar[j].t === 'grup') birlikte += yuk[j++];
          birlikte += Math.min(yuk[j] ?? 0, pxMm(p.g.h) * 0.5);
          if (birlikte > kalan && p.kolon![kol].length) sonraki();
        }
        p.kolon![kol].push(b);
        kullan(h);
        continue;
      }
      if (h > kalan && p.kolon![kol].length) sonraki();
      let k = k0;
      let tasma = false;
      if (h > kalan) {
        const f = olcer.sigdir((kk) => html(b, kk), p.kolonW!, kalan, h, k0);
        k = f.k;
        tasma = !!f.tasma;
        if (tasma) tasan++;
        h = olcer.tek(html(b, k), p.kolonW!);
      }
      p.kolon![kol].push({ ...b, k, tasma });
      sayfaHs.push(b.h);
      p.serit?.push({ no: b.h.no, harf: b.h.dogru || '—' });
      kullan(h);
    }
    if (tur === 'soru' && a.cozumYeri === 'arkada') bekleyen();
  }
  function akisCoz(l: HS[]) { akisYerlestir(l.map((h) => ({ t: 'cozum', h, k: k0 }) as Blok), 'cozum', 'Çözümler'); }

  if (a.duzen === 'akis') akisYerlestir(grupBloklari(hs, a, k0, (h) => ({ t: 'soru', h, k: k0 })), 'soru');

  /* ---- sonda: cevap anahtarı + çözümler ---- */
  if (a.cevapAnahtari && hs.length) {
    const g = govde(a, { ilk: false, serit: false, grup: true });
    const sut = Math.max(1, Math.floor((g.w + 1.2) / (ANAHTAR_W + 1.2)));
    const sat = Math.max(1, Math.floor((g.h + 1.2) / ANAHTAR_H));
    const kap = sut * sat;
    for (let i = 0; i < hs.length; i += kap) {
      sayfalar.push({
        tur: 'anahtar', g, bant: { ad: 'Cevap anahtarı', renk: null }, anahtarSut: sut,
        anahtar: hs.slice(i, i + kap).map((h) => ({ no: h.no, harf: h.dogru || '—', renk: h.renk })),
      });
    }
  }
  if (a.cozumYeri === 'sonda' && hs.length) akisYerlestir(grupBloklari(hs, a, k0, (h) => ({ t: 'cozum', h, k: k0 })), 'cozum', 'Çözümler');
  if (a.optik && hs.length) {
    const g = govde(a, { ilk: false, serit: false, grup: true });
    const sut = Math.max(1, Math.floor((g.w + 5) / (OPTIK_W + 5)));
    const sat = Math.max(1, Math.floor(g.h / OPTIK_H));
    const kap = sut * sat;
    for (let i = 0; i < hs.length; i += kap) {
      sayfalar.push({ tur: 'optik', g, bant: { ad: 'Cevap kâğıdı', renk: null }, optikSut: sut, optik: hs.slice(i, i + kap).map((h) => h.no) });
    }
  }
  return { sayfalar, hs, tasan, tahmini: tahminToplam, olcek: k0 };
}

/* ---------------------------------------------------------------------------
 * Belge HTML
 * ------------------------------------------------------------------------- */
export interface BelgeBilgi { toplam: number; dersler: string[]; kaynaklar: string[]; tarih: string }

export function bilgi(hs: HS[]): BelgeBilgi {
  return {
    toplam: hs.length,
    dersler: [...new Set(hs.map((h) => h.q.ders))],
    kaynaklar: [...new Set(hs.map((h) => kaynakAdi(h.q.kaynak)))],
    tarih: new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }),
  };
}

/** Alt bilgi / kapak yer tutucuları: {sayfa} {toplam} {tarih} {baslik} {altbaslik} {soru} */
export function yerTutucu(t: string, v: { sayfa: number; toplam: number; tarih: string; baslik: string; altbaslik: string; soru: number }): string {
  return String(t || '').replace(/\{(sayfa|toplam|tarih|baslik|altbaslik|soru)\}/g, (_, k: keyof typeof v) => String(v[k] ?? ''));
}
export const sayfaNoMetni = (no: number, toplam: number, a: Ayar) =>
  a.sayfaNoBicim === 'duz' ? `${no}` : a.sayfaNoBicim === 'sayfa' ? `Sayfa ${no}` : a.sayfaNoBicim === 'tire' ? `– ${no} –` : `${no} / ${toplam}`;
/** Alt bilginin üç bölgesi (sol, orta, sağ); sayfa numarası seçilen bölgeye eklenir (bölgede {sayfa} yoksa) */
export function altBolgeler(a: Ayar, no: number, toplam: number, b: BelgeBilgi): [string, string, string] {
  const v = { sayfa: no, toplam, tarih: b.tarih, baslik: a.baslik, altbaslik: a.altBaslik, soru: b.toplam };
  const ham: [string, string, string] = [a.altMetin || '', a.altOrta || '', a.altSag || ''];
  const out = ham.map((t) => yerTutucu(t, v)) as [string, string, string];
  if (a.sayfaNo) {
    const i = a.sayfaNoYer === 'sol' ? 0 : a.sayfaNoYer === 'orta' ? 1 : 2;
    if (!/\{sayfa\}/.test(ham[i])) out[i] = out[i] ? `${out[i]} · ${sayfaNoMetni(no, toplam, a)}` : sayfaNoMetni(no, toplam, a);
  }
  return out;
}
const logoHtml = (a: Ayar, yer: 'baslik' | 'kapak') => (a.logo && (a.logoYer === yer || a.logoYer === 'ikisi') ? `<img class="pg-logo" src="${a.logo}" alt="">` : '');

function sayfaHtml(p: Sayfa, a: Ayar, no: number, toplam: number, b: BelgeBilgi, lejant: { v: string; renk: string }[]): string {
  const fil = a.filigran.trim() ? `<div class="fil"><span>${esc(a.filigran.trim())}</span></div>` : '';
  const cift = a.ciftYuz && no % 2 === 0 ? ' cift' : '';
  if (p.tur === 'kapak') {
    const v = { sayfa: 0, toplam, tarih: b.tarih, baslik: a.baslik, altbaslik: a.altBaslik, soru: b.toplam };
    return `<section class="pg kpk"><div class="pg-in">${fil}<div class="kp">`
      + logoHtml(a, 'kapak')
      + `<div class="ust">${esc(b.kaynaklar.join(' · '))}</div>`
      + `<h1>${esc(a.baslik || 'Soru kitapçığı')}</h1>${a.altBaslik ? `<h2>${esc(a.altBaslik)}</h2>` : ''}`
      + (a.kapakNot.trim() ? `<p class="kpn">${esc(yerTutucu(a.kapakNot, v))}</p>` : '')
      + `<div class="sy"><div><b>${b.toplam}</b><span>soru</span></div><div><b>${b.dersler.length}</b><span>ders</span></div><div><b>${toplam}</b><span>sayfa</span></div></div>`
      + (b.dersler.length ? `<p class="not" style="margin:0;font-size:9.5pt">${esc(b.dersler.slice(0, 14).join(' · '))}${b.dersler.length > 14 ? ' …' : ''}</p>` : '')
      + (lejant.length ? `<div class="lj">${lejant.slice(0, 24).map((l) => `<span style="--rk:${l.renk}"><i></i>${esc(l.v)}</span>`).join('')}</div>` : '')
      + `<div class="yon">Her sorunun yalnız bir doğru cevabı vardır.${a.optik ? ' Cevaplarını sondaki cevap kâğıdına işaretle.' : ''}${a.cevapAnahtari ? ' Cevap anahtarı belgenin sonundadır.' : ''}</div>`
      + (a.adSoyad || a.tarih ? `<div class="alan">${a.adSoyad ? '<span>Ad Soyad <i></i></span><span>Numara <i></i></span>' : ''}${a.tarih ? '<span>Tarih <i></i></span>' : ''}</div>` : '')
      + `<p class="not" style="margin:0;font-size:8.5pt;opacity:.8">${esc(b.tarih)}${a.altMetin ? ` · ${esc(yerTutucu(a.altMetin, v))}` : ''}</p>`
      + `</div></div></section>`;
  }
  const g = p.g;
  const bas = g.baslik
    ? `<header class="pg-bas${a.baslikHiza === 'orta' ? ' orta' : ''}"><div class="bl">${logoHtml(a, 'baslik')}<div><h1>${esc(a.baslik)}</h1>${a.altBaslik ? `<p>${esc(a.altBaslik)}</p>` : ''}</div></div>${a.adSoyad || a.tarih ? `<div class="br">${a.adSoyad ? '<span>Ad Soyad:<i></i></span>' : ''}${a.tarih ? `<span>Tarih:<i style="width:${a.adSoyad ? 42 : 30}mm"></i></span>` : ''}</div>` : ''}</header>`
    : '';
  const bant = p.bant ? `<div class="pg-bant" style="${p.bant.renk ? `--bk:${p.bant.renk}` : ''}">${esc(p.bant.ad)}</div>` : '';
  let gv = '';
  if (p.izgara && p.hucre) {
    const { sut, sat, cw, ch } = p.izgara;
    gv = `<div class="izg${a.kesimCizgi ? ' kes' : ''}" style="grid-template-columns:repeat(${sut},${cw}mm);grid-template-rows:repeat(${sat},${ch}mm);gap:${a.hucreAralik}mm">`
      + p.hucre.map((h) => `<div class="hc${a.hucreCerceve ? ' cer' : ''}">${h ? blokHtml(h, a) : ''}</div>`).join('') + `</div>`;
  } else if (p.kolon) {
    gv = `<div class="akis">${p.kolon.map((c) => `<div class="kol" style="width:${p.kolonW}mm">${c.map((x) => blokHtml(x, a)).join('')}</div>`).join('')}</div>`;
  } else if (p.anahtar) {
    gv = `<div class="ank" style="grid-template-columns:repeat(${p.anahtarSut},minmax(0,1fr))">${p.anahtar.map((x) => `<div style="${x.renk ? `--rk:${x.renk}` : ''}"><b>${x.no}</b><i>${esc(x.harf)}</i></div>`).join('')}</div>`;
  } else if (p.optik) {
    const sat = Math.ceil(p.optik.length / p.optikSut!);
    gv = `<div class="opt" style="grid-template-columns:repeat(${p.optikSut},${OPTIK_W}mm);grid-auto-flow:column;grid-template-rows:repeat(${sat},${OPTIK_H}mm)">${p.optik.map((n) => `<div><b>${n}</b>${['A', 'B', 'C', 'D', 'E'].map((h) => `<i>${h}</i>`).join('')}</div>`).join('')}</div>`;
  }
  const seritHtml = p.serit ? `<div class="pg-serit"><b>Cevaplar</b> · ${p.serit.map((x) => `${x.no}-${esc(x.harf)}`).join('  ')}</div>` : '';
  const alt = altBilgiVar(a) ? `<footer class="pg-alt">${altBolgeler(a, no, toplam, b).map((t) => `<span>${esc(t)}</span>`).join('')}</footer>` : '';
  const satirYuk = a.punto * a.satir * 1.35 * 0.3528; // mm
  const notHtml = a.notAlani > 0 ? `<div class="pg-not"><b>Notlar</b>${'<i></i>'.repeat(Math.max(1, Math.floor(a.notAlani / satirYuk)))}</div>` : '';
  return `<section class="pg${cift}"><div class="pg-in">${fil}${bas}${bant}<div class="pg-gv" style="height:${g.h}mm">${gv}</div>${seritHtml}${notHtml}${alt}</div></section>`;
}

/** Çıktı süzgeci: "yalnız sorular" (kapak, soru, cevap kâğıdı) · "yalnız çözümler" (çözüm, cevap anahtarı) · sayfa aralığı. Belge modeli değişmez, sayfalar seçilir */
export function ciktiSuz(belge: Belge, a: Ayar): Belge {
  let sayfalar = belge.sayfalar;
  if (a.cikti === 'sorular') sayfalar = sayfalar.filter((p) => p.tur === 'kapak' || p.tur === 'soru' || p.tur === 'optik');
  else if (a.cikti === 'cozumler') sayfalar = sayfalar.filter((p) => p.tur === 'cozum' || p.tur === 'anahtar');
  const aralik = sayfaAraligi(a.sayfaAralik);
  if (aralik) {
    const kapakVar = sayfalar[0]?.tur === 'kapak';
    sayfalar = sayfalar.filter((p, i) => aralik.has(kapakVar ? i : i + 1));
  }
  return sayfalar === belge.sayfalar ? belge : { ...belge, sayfalar };
}

/** Yaprak sayısı: 2'li ve kitapçıkta iki sayfa bir yaprakta; kitapçık 4'ün katına tamamlanır (çift yüzde kapak ardı boş sayfa dahil) */
export function yaprakSayisi(n: number, a: Ayar, kapakVar = false): number {
  const m = n + (a.ciftYuz && kapakVar ? 1 : 0);
  if (a.yaprak === 'tek' || a.bicim !== 'pdf') return m;
  if (a.yaprak === 'kitapcik') return Math.ceil(m / 4) * 2;
  return Math.ceil(m / 2);
}

/** tum/toplamSayfa: önizleme yalnız ilk soruları sayfaladığında kapak, renk anahtarı ve sayfa numaraları tüm seçimi göstersin */
/**
 * `ilk`: önizlemede gösterilecek yaprak sayısı (tek kipte sayfa). Çift yüzde kapağın ardına boş sayfa girer (içerik sağ
 * sayfadan başlar); 2'li yaprakta sayfalar sırayla ikişer, kitapçıkta katlama sırasıyla (ön: son–ilk, arka: 2–sondan bir önce) dizilir.
 */
export function belgeHtml(belge: Belge, a: Ayar, o: { onizleme?: boolean; ilk?: number; baslik?: string; tum?: HS[]; toplamSayfa?: number } = {}): string {
  const b = bilgi(o.tum || belge.hs);
  const kapakVar = belge.sayfalar[0]?.tur === 'kapak';
  const toplam = o.toplamSayfa || belge.sayfalar.length;
  const lejant = renkHaritasi((o.tum || belge.hs).map((h) => h.q), a);
  // sayfa HTML'leri (null = boş sayfa)
  const html: (string | null)[] = belge.sayfalar.map((p, i) => sayfaHtml(p, a, kapakVar ? i : i + 1, kapakVar ? toplam - 1 : toplam, b, lejant));
  if (a.ciftYuz && kapakVar) html.splice(1, 0, null);
  const bos = `<section class="pg"><div class="pg-in"></div></section>`;
  const yp = yaprakOlcu(a);
  let govdeHtml: string;
  if (yp.sayfa === 1) {
    govdeHtml = (o.ilk ? html.slice(0, o.ilk) : html).map((h) => h ?? bos).join('');
  } else {
    let sira: (number | null)[][];
    if (a.yaprak === 'kitapcik') {
      const n = Math.ceil(html.length / 4) * 4;
      const s = (i: number) => (i < html.length ? i : null);
      sira = [];
      for (let i = 0; i < n / 2; i += 1) {
        // ön yüz: son–ilk; arka yüz: ikinci–sondan ikinci (katlanınca sıra doğru)
        sira.push(i % 2 === 0 ? [s(n - 1 - i), s(i)] : [s(i), s(n - 1 - i)]);
      }
    } else {
      sira = [];
      for (let i = 0; i < html.length; i += 2) sira.push([i, i + 1 < html.length ? i + 1 : null]);
    }
    if (o.ilk) sira = sira.slice(0, o.ilk);
    govdeHtml = sira.map((y) => `<div class="yp">${y.map((i) => `<div>${i == null ? bos : (html[i] ?? bos)}</div>`).join('')}</div>`).join('');
  }
  return `<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>${esc(o.baslik || a.baslik || 'Sorular')}</title>${yaziLinkHtml(a)}<style>${belgeCss(a, o.onizleme)}</style></head><body>${govdeHtml}</body></html>`;
}

export const kagitAdi = (a: Ayar) => {
  if (a.bicim === 'pptx' && a.slayt !== 'kagit') return a.slayt === 'genis' ? 'Slayt 16:9' : 'Slayt 4:3';
  return `${KAGIT[a.kagit].ad} ${a.yatay ? 'yatay' : 'dikey'}`;
};
