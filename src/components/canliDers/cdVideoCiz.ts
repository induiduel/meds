/**
 * Canlı ders · video: ayarlar, zaman çizelgesi ve kare çizimi. DOM ve pdf.js kullanmaz; hem video işçisinde
 * (cdVideoIsci.ts, asıl üretim) hem ana iş parçacığında (pencere önizlemesi, altyazı dosyası) aynı kodla çalışır.
 * Zamanlama sözleşmesi canlı dersle aynı: varyant.zamanlama (paragraf), kelimeZaman (kelime), detay.isaret (slayt kutusu).
 */
import type { CdDetay, CdIsaret, CdVaryant } from './canliDersStore';

// ---------- ayarlar
export type CdVideoCozunurluk = '720p' | '1080p' | '2k' | '4k';
export type CdVideoBicim = 'mp4-avc' | 'mp4-hevc' | 'webm-vp9';
export type CdVideoKalite = 'dengeli' | 'yuksek' | 'en-yuksek';
export type CdVideoFps = 24 | 30 | 60;
/** alt: slayt + altta metin paneli · yan: slayt + sağda metin · altyazi: tam slayt + bindirmeli altyazı · slayt: yalnız slayt · metin: yalnız metin */
export type CdVideoDuzen = 'alt' | 'yan' | 'altyazi' | 'slayt' | 'metin';
export interface CdAltyaziAyar {
  boyut: 'k' | 'o' | 'b' | 'cb';
  satir: 1 | 2 | 3;
  zemin: 'kutu' | 'yari' | 'kontur';
  vurgu: 'kelime' | 'cumle';
  renk: 'sari' | 'turkuaz' | 'yesil' | 'pembe';
  konum: 'alt' | 'ust';
}
export interface CdCozucuAyar { acik: boolean; tur: 'hepsi' | 'ornek' | 'cikmis'; dusunSn: number }
export interface CdVideoAyar {
  bicim: CdVideoBicim;
  cozunurluk: CdVideoCozunurluk;
  fps: CdVideoFps;
  kalite: CdVideoKalite;
  duzen: CdVideoDuzen;
  tema: 'koyu' | 'acik';
  baslikSerit: boolean;
  ilerleme: boolean;
  slaytIsaret: boolean;
  ogrenciNot: boolean;
  altyazi: CdAltyaziAyar;
  /** ayrıca .vtt altyazı dosyası indirilsin */
  vtt: boolean;
  cozucu: CdCozucuAyar;
  /** bitince tarayıcı bildirimi */
  bildirim: boolean;
}
export const CD_VIDEO_VARSAYILAN: CdVideoAyar = {
  bicim: 'mp4-avc', cozunurluk: '1080p', fps: 30, kalite: 'yuksek', duzen: 'alt', tema: 'koyu',
  baslikSerit: true, ilerleme: true, slaytIsaret: true, ogrenciNot: true,
  altyazi: { boyut: 'o', satir: 2, zemin: 'yari', vurgu: 'kelime', renk: 'sari', konum: 'alt' },
  vtt: false, cozucu: { acik: false, tur: 'hepsi', dusunSn: 5 }, bildirim: true,
};

export const CD_VIDEO_BOYUT: Record<CdVideoCozunurluk, { w: number; h: number; etiket: string; bitHizi: number }> = {
  // bitHizi: 30 fps H.264 "yüksek" kalite tabanı
  '720p': { w: 1280, h: 720, etiket: '720p', bitHizi: 3_000_000 },
  '1080p': { w: 1920, h: 1080, etiket: '1080p', bitHizi: 6_000_000 },
  '2k': { w: 2560, h: 1440, etiket: '2K', bitHizi: 10_000_000 },
  '4k': { w: 3840, h: 2160, etiket: '4K', bitHizi: 20_000_000 },
};
export const CD_VIDEO_BICIM: Record<CdVideoBicim, { etiket: string; aciklama: string; kod: 'avc' | 'hevc' | 'vp9'; kap: 'mp4' | 'webm'; carpan: number }> = {
  'mp4-avc': { etiket: 'MP4 · H.264', aciklama: 'Her cihazda açılır', kod: 'avc', kap: 'mp4', carpan: 1 },
  'mp4-hevc': { etiket: 'MP4 · H.265', aciklama: 'Daha küçük dosya', kod: 'hevc', kap: 'mp4', carpan: 0.65 },
  'webm-vp9': { etiket: 'WebM · VP9', aciklama: 'Açık biçim, küçük dosya', kod: 'vp9', kap: 'webm', carpan: 0.7 },
};
const KALITE_CARPAN: Record<CdVideoKalite, number> = { dengeli: 0.6, yuksek: 1, 'en-yuksek': 1.7 };
const FPS_CARPAN: Record<CdVideoFps, number> = { 24: 0.85, 30: 1, 60: 1.4 };
export const cdVideoBitHizi = (a: Pick<CdVideoAyar, 'bicim' | 'cozunurluk' | 'fps' | 'kalite'>) =>
  Math.round(CD_VIDEO_BOYUT[a.cozunurluk].bitHizi * KALITE_CARPAN[a.kalite] * FPS_CARPAN[a.fps] * CD_VIDEO_BICIM[a.bicim].carpan);
export const cdVideoMetinli = (d: CdVideoDuzen) => d !== 'slayt';

// ---------- çözücü soruları (işçiye giden yalın biçim)
export interface CdVideoKlip { url: string; sure: number }
export interface CdVideoSoru {
  no: number; tur?: string; sinav?: string; soru: string; secenekler: Record<string, string>; dogru: string; cozum: string;
  q: CdVideoKlip; c: CdVideoKlip;
}

// ---------- ders zaman çizelgesi
interface Kelime { b: number; e: number; t: number }
export interface Para { i: number; metin: string; bas: number; son: number; kelimeler: Kelime[]; cumle: number[]; bolum: string }

function cumleSinirlari(metin: string): number[] {
  // canliDersStore.cumleSinirlari ile aynı kural (pdf_isaret.py cümle dizinleri buna göre)
  const out: number[] = [];
  const re = /[.!?…]+["'”’)\]]*(?:\s+|$)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(metin))) {
    if (!m[0]) { re.lastIndex++; continue; }
    const e = m.index + m[0].length;
    const s = metin.charAt(e);
    if (s && s !== s.toLocaleUpperCase('tr') && s === s.toLocaleLowerCase('tr')) continue;
    if (e > (out[out.length - 1] || 0)) out.push(e);
    if (re.lastIndex >= metin.length) break;
  }
  if (!out.length || out[out.length - 1] < metin.length) out.push(metin.length);
  return out;
}

export function cizelge(detay: CdDetay, v: CdVaryant): Para[] {
  const z = v.zamanlama;
  if (!z?.length) throw new Error('Bu sesin paragraf zamanlaması yok; video oluşturulamaz.');
  const out: Para[] = [];
  for (const b of detay.bolumler) for (const p of b.paragraflar) {
    const r = z[p.i];
    if (!r) continue;
    const kelimeler: Kelime[] = [];
    for (const m of p.metin.matchAll(/\S+/g)) kelimeler.push({ b: m.index!, e: m.index! + m[0].length, t: 0 });
    const kz = v.kelimeZaman?.[p.i];
    if (kz && kz.length === kelimeler.length) kelimeler.forEach((w, j) => { w.t = kz[j]; });
    else { // ölçüm yoksa harf oranıyla paylaştır
      const L = Math.max(1, p.metin.length);
      kelimeler.forEach((w) => { w.t = r[0] + (w.b / L) * (r[1] - r[0]); });
    }
    out.push({ i: p.i, metin: p.metin, bas: r[0], son: r[1], kelimeler, cumle: cumleSinirlari(p.metin), bolum: b.baslik });
  }
  return out.sort((a, b) => a.bas - b.bas);
}

export const sonIndeks = <T,>(dizi: T[], t: number, al: (x: T) => number) => {
  let lo = 0, hi = dizi.length - 1, k = -1;
  while (lo <= hi) { const m = (lo + hi) >> 1; if (al(dizi[m]) <= t) { k = m; lo = m + 1; } else hi = m - 1; }
  return k;
};

// ---------- sayfa zaman çizelgesi: PDF'in HER sayfası en az bir kez görünür
type Sayfa = [number, number];
export interface SayfaDilim { t: number; d: number; s: number }
const SAYFA_EN_COK_SN = 4; // anlatımda geçmeyen sayfa en çok bu kadar görünür
const SAYFA_EN_AZ_SN = 1.2;

export function sayfaCizelgesi(paras: Para[], detay: CdDetay, sure: number, sayilar: number[]): SayfaDilim[] {
  // 1) anlatımın gösterdiği sayfalar (cümle başına: pdf_isaret kutusu > hizalamanın cümle sayfası > paragraf sayfası)
  const cap: SayfaDilim[] = [];
  for (const p of paras) {
    const e = detay.pdf?.paragraflar?.[p.i];
    if (!e) continue;
    for (let c = 0; c < p.cumle.length; c++) {
      const cb = c ? p.cumle[c - 1] : 0;
      const w = p.kelimeler.find((k) => k.b >= cb);
      const t = c === 0 ? p.bas : w ? w.t : p.bas;
      const is = detay.isaret?.[p.i]?.[c];
      const sf: Sayfa = is && is.s ? [is.d, is.s]
        : e.sayfalar?.[c] ? [e.dosyalar?.[c] ?? e.dosya, e.sayfalar[c]] : [e.dosya, e.sayfa];
      const son = cap[cap.length - 1];
      if (!son || son.d !== sf[0] || son.s !== sf[1]) cap.push({ t: Math.max(t, son ? son.t : 0), d: sf[0], s: sf[1] });
    }
  }
  const gecerli = (d: number, s: number) => d >= 0 && d < sayilar.length && s >= 1 && s <= sayilar[d];
  const dilim = cap.filter((x) => gecerli(x.d, x.s));
  // global sıra: dosya sırası, sonra sayfa
  const ofs: number[] = []; let top = 0;
  sayilar.forEach((n, d) => { ofs[d] = top; top += n; });
  const g = (d: number, s: number) => ofs[d] + s - 1;
  if (!top) return dilim;
  if (!dilim.length) { // hizalama yoksa: sayfalar süreye eşit paylaştırılır
    const pay = sure / top;
    const out: SayfaDilim[] = [];
    sayilar.forEach((n, d) => { for (let s = 1; s <= n; s++) out.push({ t: g(d, s) * pay, d, s }); });
    return out;
  }
  dilim[0].t = 0;
  // 2) hiç gösterilmeyen sayfalar: global sırada kendinden önceki en yakın gösterilen sayfanın (son kez göründüğü) diliminin
  //    sonuna eklenir; önünde gösterilen sayfa yoksa (kapak vb.) ilk dilimin başına
  const gorulen = new Set(dilim.map((x) => g(x.d, x.s)));
  const sonDilim = new Map<number, number>(); // global sayfa → son göründüğü dilim dizini
  dilim.forEach((x, i) => sonDilim.set(g(x.d, x.s), i));
  const ek = new Map<number, Sayfa[]>(); // dilim dizini → arkasına eklenecekler (-1: en baş)
  sayilar.forEach((n, d) => {
    for (let s = 1; s <= n; s++) {
      const k = g(d, s);
      if (gorulen.has(k)) continue;
      let sahip = -1;
      for (let j = k - 1; j >= 0; j--) if (sonDilim.has(j)) { sahip = sonDilim.get(j)!; break; }
      (ek.get(sahip) ?? ek.set(sahip, []).get(sahip)!).push([d, s]);
    }
  });
  const out: SayfaDilim[] = [];
  const bitis = (i: number) => (i + 1 < dilim.length ? dilim[i + 1].t : sure);
  const pay = (uzun: number, n: number) => Math.max(SAYFA_EN_AZ_SN, Math.min(SAYFA_EN_COK_SN, (uzun * 0.6) / n));
  const bas = ek.get(-1) || [];
  dilim.forEach((x, i) => {
    let t0 = x.t;
    if (i === 0 && bas.length) { // kapak/giriş sayfaları ilk dilimin başında
      const p = pay(bitis(0) - x.t, bas.length);
      bas.forEach(([d, s], j) => out.push({ t: x.t + j * p, d, s }));
      t0 = x.t + bas.length * p;
    }
    out.push({ t: t0, d: x.d, s: x.s });
    const ekler = ek.get(i);
    if (ekler?.length) {
      const son = bitis(i);
      const p = pay(son - t0, ekler.length);
      const ilk = Math.max(t0 + 0.5, son - ekler.length * p);
      const adim = (son - ilk) / ekler.length;
      ekler.forEach(([d, s], j) => out.push({ t: ilk + j * adim, d, s }));
    }
  });
  return out.sort((a, b) => a.t - b.t);
}

// ---------- soru çözücü zaman çizelgesi (ders bitince, sorular art arda)
export interface SoruDilim { soru: CdVideoSoru; n: number; t0: number; qBas: number; qSon: number; cBas: number; cSon: number; t1: number }
export interface SoruCizelge { bas: number; girisSon: number; dilimler: SoruDilim[]; son: number }
const SORU_GIRIS_SN = 3;
const SORU_ON_SN = 0.8;
const SORU_SON_SN = 1.6;

export function soruCizelgesi(dersSon: number, sorular: CdVideoSoru[], dusunSn: number): SoruCizelge | null {
  if (!sorular.length) return null;
  let t = dersSon + SORU_GIRIS_SN;
  const dilimler = sorular.map((soru, n) => {
    const t0 = t;
    const qBas = t0 + SORU_ON_SN, qSon = qBas + soru.q.sure;
    const cBas = qSon + Math.max(0, dusunSn), cSon = cBas + soru.c.sure;
    t = cSon + SORU_SON_SN;
    return { soru, n, t0, qBas, qSon, cBas, cSon, t1: t };
  });
  return { bas: dersSon, girisSon: dersSon + SORU_GIRIS_SN, dilimler, son: t };
}

// ---------- an (bir zamandaki durum)
export interface An {
  p: Para | null; w: number; c: number; isaret: CdIsaret | null; sayfa: [number, number] | null;
  /** soru bölümü: giris | soru (kök+şıklar okunuyor) | dusun | cevap */
  soru?: { evre: 'giris' | 'soru' | 'dusun' | 'cevap'; d?: SoruDilim; kalan?: number };
}

export function anBul(paras: Para[], detay: CdDetay, t: number, sc: SayfaDilim[], soruC: SoruCizelge | null): An {
  if (soruC && t >= soruC.bas) {
    if (t < soruC.girisSon) return { p: null, w: -1, c: -1, isaret: null, sayfa: null, soru: { evre: 'giris' } };
    const d = soruC.dilimler[Math.max(0, sonIndeks(soruC.dilimler, t, (x) => x.t0))];
    const evre = t < d.qSon ? 'soru' : t < d.cBas ? 'dusun' : 'cevap';
    return { p: null, w: -1, c: -1, isaret: null, sayfa: null, soru: { evre, d, kalan: evre === 'dusun' ? Math.ceil(d.cBas - t) : undefined } };
  }
  const sd = sc[Math.max(0, sonIndeks(sc, t, (x) => x.t))];
  const sayfa: [number, number] | null = sd ? [sd.d, sd.s] : null;
  const k = sonIndeks(paras, t, (p) => p.bas);
  if (k < 0) return { p: null, w: -1, c: -1, isaret: null, sayfa };
  const p = paras[k];
  const w = Math.max(0, sonIndeks(p.kelimeler, t, (x) => x.t));
  const kb = p.kelimeler[w]?.b ?? 0;
  let c = p.cumle.findIndex((e) => kb < e);
  if (c < 0) c = p.cumle.length - 1;
  const is = detay.isaret?.[p.i]?.[c] || null;
  return { p, w, c, isaret: is, sayfa };
}

/** Yeniden çizim anahtarı: yalnız görüntüyü değiştiren durum değişince kare yeniden çizilir */
export const anAnahtari = (an: An, sayfa: string, ilerlemePx: number) =>
  an.soru ? `s|${an.soru.evre}|${an.soru.d?.n}|${an.soru.kalan}|${ilerlemePx}` : `${an.p?.i}|${an.w}|${an.c}|${sayfa}|${ilerlemePx}`;

// ---------- çizim
export type Ctx = OffscreenCanvasRenderingContext2D | CanvasRenderingContext2D;
const FONT = '"Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif';
const TEMA = {
  koyu: { zemin: '#0f1419', kart: '#1a2129', yazi: '#e8edf2', soluk: '#7d8a97', cizgi: 'rgba(255,255,255,.08)' },
  acik: { zemin: '#e9edf2', kart: '#ffffff', yazi: '#15202b', soluk: '#8a96a3', cizgi: 'rgba(0,0,0,.08)' },
};
export const CD_VURGU_RENK: Record<CdAltyaziAyar['renk'], string> = { sari: '#ffd25c', turkuaz: '#3fd8d2', yesil: '#5fe08e', pembe: '#ff86bd' };
const BOYUT: Record<CdAltyaziAyar['boyut'], number> = { k: 0.8, o: 1, b: 1.25, cb: 1.5 };
const DOGRU = '#22a55b';

export interface CizBaglam {
  W: number; H: number; ayar: CdVideoAyar; baslik: string; etiket: string; t: number; sure: number;
  not?: CdDetay['ogrenciNot']; soruSay?: number;
}

/** Slaytın çizileceği kutu (pdf.js bu boyutta çizer: keskin görüntü) */
export function slaytKutusu(a: CdVideoAyar, W: number, H: number) {
  const k = H / 720;
  const ust = a.baslikSerit ? 58 * k : 20 * k;
  const alt = (a.ilerleme ? 6 * k : 0) + 20 * k;
  if (a.duzen === 'alt') {
    const ph = altPanelYuk(a, k);
    return { x: 28 * k, y: ust, w: W - 56 * k, h: H - ph - ust - 14 * k };
  }
  if (a.duzen === 'yan') return { x: 28 * k, y: ust, w: W * 0.64 - 28 * k, h: H - ust - alt };
  if (a.duzen === 'metin') return { x: 0, y: 0, w: 0, h: 0 };
  return { x: 20 * k, y: ust, w: W - 40 * k, h: H - ust - alt };
}
const yaziBoyu = (a: CdVideoAyar, k: number) => 30 * k * BOYUT[a.altyazi.boyut];
const altPanelYuk = (a: CdVideoAyar, k: number) => Math.round(yaziBoyu(a, k) * 1.45 * a.altyazi.satir + 56 * k + (a.ilerleme ? 6 * k : 0));

function satirlaraBol(ctx: Ctx, kelimeler: { s: string; j: number }[], gen: number) {
  const satir: { s: string; j: number; x: number }[][] = [[]];
  let x = 0;
  const bosluk = ctx.measureText(' ').width;
  for (const k of kelimeler) {
    const g = ctx.measureText(k.s).width;
    if (x > 0 && x + g > gen) { satir.push([]); x = 0; }
    satir[satir.length - 1].push({ ...k, x });
    x += g + bosluk;
  }
  return satir;
}

/** Düz metni satırlara sarar (uzun kelimeyi de böler) */
function sar(ctx: Ctx, metin: string, gen: number): string[] {
  const out: string[] = [];
  for (const par of metin.split(/\n+/)) {
    let satir = '';
    for (const kelime of par.split(/\s+/).filter(Boolean)) {
      const aday = satir ? `${satir} ${kelime}` : kelime;
      if (ctx.measureText(aday).width <= gen) { satir = aday; continue; }
      if (satir) out.push(satir);
      satir = kelime;
      while (ctx.measureText(satir).width > gen && satir.length > 1) {
        let n = satir.length - 1;
        while (n > 1 && ctx.measureText(satir.slice(0, n)).width > gen) n--;
        out.push(satir.slice(0, n)); satir = satir.slice(n);
      }
    }
    if (satir) out.push(satir);
  }
  return out;
}
export const markdownsuz = (s: string) => (s || '').replace(/\*\*|__|`/g, '').replace(/\s+/g, ' ').trim();

interface MetinStil { fs: number; satir: number; hiza: 'sol' | 'orta'; bindirme: boolean }

/** Okunan cümleyi kelime vurgulu yazar; okunan satırı içeren en çok `satir` satırlık pencere. Kutunun dikey ortasına. */
function cumleYaz(ctx: Ctx, an: An, kutu: { x: number; y: number; w: number; h: number }, st: MetinStil, b: CizBaglam) {
  const p = an.p;
  if (!p) return;
  const k = b.H / 720;
  const tm = TEMA[b.ayar.tema];
  const renk = CD_VURGU_RENK[b.ayar.altyazi.renk];
  const zemin = b.ayar.altyazi.zemin;
  const cb = an.c ? p.cumle[an.c - 1] : 0, ce = p.cumle[an.c];
  const ks = p.kelimeler.map((w, j) => ({ w, j })).filter(({ w }) => w.b >= cb && w.b < ce).map(({ w, j }) => ({ s: p.metin.slice(w.b, w.e), j }));
  ctx.font = `500 ${st.fs}px ${FONT}`;
  ctx.textBaseline = 'middle';
  ctx.textAlign = 'left';
  const satir = satirlaraBol(ctx, ks, kutu.w);
  const okunanSatir = Math.max(0, satir.findIndex((s) => s.some((q) => q.j === an.w)));
  const bas = Math.min(Math.max(0, okunanSatir - (st.satir > 2 ? 1 : 0)), Math.max(0, satir.length - st.satir));
  const gor = satir.slice(bas, bas + st.satir);
  if (!gor.length) return;
  const lh = st.fs * 1.45;
  const genis = (s: typeof gor[number]) => (s.length ? s[s.length - 1].x + ctx.measureText(s[s.length - 1].s).width : 0);
  const blokH = gor.length * lh;
  let y = kutu.y + (kutu.h - blokH) / 2 + lh / 2;
  // bindirme altyazı: zemin kutusu
  if (st.bindirme && zemin !== 'kontur') {
    const enGen = Math.max(...gor.map(genis));
    const px = 22 * k, py = 12 * k;
    const x0 = st.hiza === 'orta' ? kutu.x + (kutu.w - enGen) / 2 : kutu.x;
    ctx.fillStyle = zemin === 'kutu' ? 'rgba(10,12,16,.88)' : 'rgba(10,12,16,.58)';
    ctx.beginPath(); ctx.roundRect(x0 - px, y - lh / 2 - py, enGen + px * 2, blokH + py * 2, 14 * k); ctx.fill();
  }
  const kelimeVurgu = b.ayar.altyazi.vurgu === 'kelime';
  const acikZemin = !st.bindirme && b.ayar.tema === 'acik';
  for (const s of gor) {
    const ox = st.hiza === 'orta' ? kutu.x + (kutu.w - genis(s)) / 2 : kutu.x;
    for (const q of s) {
      const xx = ox + q.x;
      const okunan = kelimeVurgu && q.j === an.w;
      if (okunan) {
        const g = ctx.measureText(q.s).width;
        ctx.fillStyle = acikZemin ? renk : `${renk}2e`;
        ctx.beginPath(); ctx.roundRect(xx - 6 * k, y - st.fs * 0.66, g + 12 * k, st.fs * 1.32, 8 * k); ctx.fill();
      }
      if (st.bindirme) {
        ctx.fillStyle = okunan ? renk : kelimeVurgu && q.j > an.w ? 'rgba(255,255,255,.62)' : '#ffffff';
        if (zemin === 'kontur') { ctx.lineJoin = 'round'; ctx.lineWidth = st.fs * 0.16; ctx.strokeStyle = 'rgba(0,0,0,.9)'; ctx.strokeText(q.s, xx, y); }
      } else if (okunan) ctx.fillStyle = acikZemin ? '#15202b' : renk; // aynı kalınlık: satır ölçüsü bozulmasın
      else ctx.fillStyle = !kelimeVurgu || q.j < an.w ? tm.yazi : tm.soluk;
      ctx.fillText(q.s, xx, y);
    }
    y += lh;
  }
}

function slaytCiz(ctx: Ctx, an: An, bmp: ImageBitmap | null, kutu: { x: number; y: number; w: number; h: number }, b: CizBaglam) {
  const k = b.H / 720;
  const tm = TEMA[b.ayar.tema];
  if (!bmp) {
    ctx.fillStyle = tm.kart; ctx.fillRect(kutu.x, kutu.y, kutu.w, kutu.h);
    ctx.font = `700 ${34 * k}px ${FONT}`; ctx.fillStyle = tm.yazi; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText((an.p?.bolum || b.baslik).slice(0, 60), kutu.x + kutu.w / 2, kutu.y + kutu.h / 2); ctx.textAlign = 'left';
    return;
  }
  const s = Math.min(kutu.w / bmp.width, kutu.h / bmp.height);
  const w = bmp.width * s, h = bmp.height * s, x = kutu.x + (kutu.w - w) / 2, y = kutu.y + (kutu.h - h) / 2;
  ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = 24 * k; ctx.fillStyle = '#fff'; ctx.fillRect(x, y, w, h); ctx.restore();
  ctx.drawImage(bmp, x, y, w, h);
  // öğrenci notunda işaretli yerler: kırmızı marker + pasaj başı yıldızı + sağ üst köşe yıldızı (PdfDocView ile aynı)
  const nt = b.ayar.ogrenciNot && an.sayfa ? b.not?.[String(an.sayfa[0])]?.[String(an.sayfa[1])] : null;
  if (nt) {
    ctx.save();
    ctx.globalCompositeOperation = 'multiply';
    ctx.fillStyle = 'rgba(239,68,68,.32)';
    for (const [x0, y0, x1, y1] of nt.l) ctx.fillRect(x + x0 * w - 2 * k, y + y0 * h - 2 * k, (x1 - x0) * w + 4 * k, (y1 - y0) * h + 4 * k);
    ctx.restore();
    const yildiz = (px: number, py: number, boy: number, sag: boolean) => {
      ctx.font = `700 ${boy}px ${FONT}`; ctx.textBaseline = 'middle'; ctx.textAlign = sag ? 'center' : 'right';
      ctx.lineWidth = 3 * k; ctx.strokeStyle = '#fff'; ctx.strokeText('★', px, py);
      ctx.fillStyle = '#dc2626'; ctx.fillText('★', px, py);
      ctx.textAlign = 'left';
    };
    for (const [bx, by] of nt.b || []) yildiz(x + bx * w - 1 * k, y + by * h, Math.max(10, w * 0.019), false);
    if (nt.y) yildiz(x + nt.y[0] * w, y + nt.y[1] * h, Math.max(14, w * 0.032), true);
  }
  const is = an.isaret;
  if (b.ayar.slaytIsaret && is && an.sayfa && is.d === an.sayfa[0] && is.s === an.sayfa[1] && an.p) {
    const renk = CD_VURGU_RENK[b.ayar.altyazi.renk];
    ctx.save(); ctx.globalAlpha = 0.28; ctx.fillStyle = renk;
    for (const [x0, y0, x1, y1] of is.l || []) ctx.fillRect(x + x0 * w, y + y0 * h, (x1 - x0) * w, (y1 - y0) * h);
    ctx.restore();
    // okunan kelimenin slayttaki kutusu
    const cb = an.c ? an.p.cumle[an.c - 1] : 0;
    const kc = (an.p.kelimeler[an.w]?.b ?? 0) - cb;
    const wk = (is.w || []).find((q) => kc >= q[0] && kc < q[1]);
    if (wk) {
      ctx.strokeStyle = renk; ctx.lineWidth = 2.5 * k;
      ctx.strokeRect(x + wk[2] * w - 2 * k, y + wk[3] * h - 2 * k, (wk[4] - wk[2]) * w + 4 * k, (wk[5] - wk[3]) * h + 4 * k);
    }
  }
}

function ustSerit(ctx: Ctx, b: CizBaglam, sag: string) {
  const k = b.H / 720;
  const tm = TEMA[b.ayar.tema];
  const ust = 30 * k;
  ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
  ctx.font = `600 ${17 * k}px ${FONT}`; ctx.fillStyle = tm.yazi;
  ctx.fillText(`${b.etiket} · ${b.baslik}`.slice(0, 110), 28 * k, ust);
  if (sag) {
    ctx.font = `500 ${15 * k}px ${FONT}`; ctx.fillStyle = tm.soluk; ctx.textAlign = 'right';
    ctx.fillText(sag.slice(0, 60), b.W - 28 * k, ust); ctx.textAlign = 'left';
  }
}

function ilerlemeCubugu(ctx: Ctx, b: CizBaglam) {
  const k = b.H / 720;
  ctx.fillStyle = TEMA[b.ayar.tema].cizgi; ctx.fillRect(0, b.H - 6 * k, b.W, 6 * k);
  ctx.fillStyle = CD_VURGU_RENK[b.ayar.altyazi.renk];
  ctx.fillRect(0, b.H - 6 * k, b.W * Math.min(1, b.t / Math.max(1, b.sure)), 6 * k);
}

/** Bir kareyi çizer */
export function ciz(ctx: Ctx, an: An, bmp: ImageBitmap | null, b: CizBaglam) {
  const { W, H, ayar } = b;
  const k = H / 720;
  const tm = TEMA[ayar.tema];
  ctx.fillStyle = tm.zemin; ctx.fillRect(0, 0, W, H);
  if (an.soru) { soruCiz(ctx, an, b); if (ayar.ilerleme) ilerlemeCubugu(ctx, b); return; }
  if (ayar.baslikSerit) ustSerit(ctx, b, an.p?.bolum || '');
  const fs = yaziBoyu(ayar, k);
  const kutu = slaytKutusu(ayar, W, H);
  if (ayar.duzen !== 'metin') slaytCiz(ctx, an, bmp, kutu, b);
  if (ayar.duzen === 'alt') {
    const ph = altPanelYuk(ayar, k);
    const y0 = H - ph;
    ctx.fillStyle = tm.kart; ctx.fillRect(0, y0, W, ph);
    cumleYaz(ctx, an, { x: 60 * k, y: y0, w: W - 120 * k, h: ph - (ayar.ilerleme ? 6 * k : 0) }, { fs, satir: ayar.altyazi.satir, hiza: 'sol', bindirme: false }, b);
  } else if (ayar.duzen === 'yan') {
    const x0 = kutu.x + kutu.w + 24 * k;
    const r = { x: x0, y: kutu.y, w: W - x0 - 28 * k, h: kutu.h };
    ctx.fillStyle = tm.kart; ctx.beginPath(); ctx.roundRect(r.x, r.y, r.w, r.h, 16 * k); ctx.fill();
    const fsY = fs * 0.9;
    const enCok = Math.max(1, Math.floor((r.h - 48 * k) / (fsY * 1.45)));
    cumleYaz(ctx, an, { x: r.x + 26 * k, y: r.y + 12 * k, w: r.w - 52 * k, h: r.h - 24 * k }, { fs: fsY, satir: Math.min(enCok, ayar.altyazi.satir + 6), hiza: 'sol', bindirme: false }, b);
  } else if (ayar.duzen === 'altyazi') {
    const lh = fs * 1.45;
    const h = lh * ayar.altyazi.satir + 24 * k;
    const y = ayar.altyazi.konum === 'ust' ? kutu.y + 24 * k : kutu.y + kutu.h - h - 18 * k;
    cumleYaz(ctx, an, { x: W * 0.08, y, w: W * 0.84, h }, { fs, satir: ayar.altyazi.satir, hiza: 'orta', bindirme: true }, b);
  } else if (ayar.duzen === 'metin') {
    const ust = ayar.baslikSerit ? 58 * k : 20 * k;
    const fsM = fs * 1.35;
    cumleYaz(ctx, an, { x: W * 0.1, y: ust, w: W * 0.8, h: H - ust - 30 * k }, { fs: fsM, satir: Math.max(3, ayar.altyazi.satir + 2), hiza: 'orta', bindirme: false }, b);
  }
  if (ayar.ilerleme) ilerlemeCubugu(ctx, b);
}

const TUR_AD: Record<string, string> = { ornek: 'Örnek soru', benzer: 'Benzer soru', cikmis: 'Çıkmış soru' };

function soruCiz(ctx: Ctx, an: An, b: CizBaglam) {
  const { W, H } = b;
  const k = H / 720;
  const tm = TEMA[b.ayar.tema];
  const renk = CD_VURGU_RENK[b.ayar.altyazi.renk];
  const s = an.soru!;
  ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
  if (b.ayar.baslikSerit) ustSerit(ctx, b, 'Soru çözücü');
  if (s.evre === 'giris' || !s.d) {
    ctx.textAlign = 'center';
    ctx.font = `700 ${46 * k}px ${FONT}`; ctx.fillStyle = tm.yazi;
    ctx.fillText('Soru çözücü', W / 2, H / 2 - 26 * k);
    ctx.font = `500 ${22 * k}px ${FONT}`; ctx.fillStyle = tm.soluk;
    ctx.fillText(`Bu dersin ${b.soruSay || ''} sorusu: soru, şıklar, doğru cevap ve açıklaması`.replace('  ', ' '), W / 2, H / 2 + 28 * k);
    ctx.fillStyle = renk; ctx.fillRect(W / 2 - 40 * k, H / 2 + 62 * k, 80 * k, 4 * k);
    ctx.textAlign = 'left';
    return;
  }
  const q = s.d.soru;
  const cevap = s.evre === 'cevap';
  const kx = 64 * k, ky = (b.ayar.baslikSerit ? 62 : 28) * k;
  const kw = W - kx * 2, kh = H - ky - 30 * k;
  ctx.fillStyle = tm.kart; ctx.beginPath(); ctx.roundRect(kx, ky, kw, kh, 18 * k); ctx.fill();
  const pad = 32 * k;
  const ix = kx + pad, iw = kw - pad * 2;
  // üst: soru numarası + tür
  ctx.font = `700 ${16 * k}px ${FONT}`; ctx.fillStyle = renk;
  const ust = `SORU ${s.d.n + 1} / ${b.soruSay || ''}`.trim();
  ctx.fillText(ust, ix, ky + pad);
  const tur = [q.tur ? TUR_AD[q.tur] || '' : '', q.sinav || ''].filter(Boolean).join(' · ');
  if (tur) { ctx.font = `500 ${15 * k}px ${FONT}`; ctx.fillStyle = tm.soluk; ctx.textAlign = 'right'; ctx.fillText(tur, ix + iw, ky + pad); ctx.textAlign = 'left'; }
  if (s.evre === 'dusun' && s.kalan != null) {
    ctx.font = `600 ${15 * k}px ${FONT}`; ctx.fillStyle = tm.soluk; ctx.textAlign = 'right';
    ctx.fillText(`Düşün… ${s.kalan}`, ix + iw, ky + pad + 24 * k); ctx.textAlign = 'left';
  }
  // yerleşim: kök + şıklar (+ cevapta açıklama) sığana dek yazı küçülür
  const harfler = Object.keys(q.secenekler).filter((h) => q.secenekler[h]);
  const kok = markdownsuz(q.soru);
  const aciklama = markdownsuz(q.cozum);
  const alanY = ky + pad + 30 * k, alanH = kh - pad * 2 - 30 * k;
  let fs = 28 * k, olcu: { kok: string[]; sik: string[][]; ac: string[] } = { kok: [], sik: [], ac: [] };
  const yukseklik = (f: number) => {
    const lh = f * 1.38;
    ctx.font = `600 ${f}px ${FONT}`;
    const kokS = sar(ctx, kok, iw);
    ctx.font = `500 ${f * 0.92}px ${FONT}`;
    const sikS = harfler.map((h) => sar(ctx, q.secenekler[h], iw - 70 * k));
    const acS = cevap ? (ctx.font = `500 ${f * 0.82}px ${FONT}`, sar(ctx, aciklama, iw - 40 * k)) : [];
    olcu = { kok: kokS, sik: sikS, ac: acS };
    const sikH = sikS.reduce((a, x) => a + x.length * lh * 0.92 + 16 * k, 0);
    return kokS.length * lh + 22 * k + sikH + (cevap ? 26 * k + acS.length * lh * 0.82 + 30 * k : 0);
  };
  while (fs > 12 * k && yukseklik(fs) > alanH) fs -= 1 * k;
  const lh = fs * 1.38;
  let y = alanY + lh / 2;
  ctx.font = `600 ${fs}px ${FONT}`; ctx.fillStyle = tm.yazi;
  for (const l of olcu.kok) { ctx.fillText(l, ix, y); y += lh; }
  y += 22 * k - lh / 2;
  harfler.forEach((h, i) => {
    const sat = olcu.sik[i];
    const sh = sat.length * lh * 0.92 + 8 * k;
    const dogru = cevap && h === q.dogru;
    if (dogru) { ctx.fillStyle = `${DOGRU}2b`; ctx.beginPath(); ctx.roundRect(ix - 10 * k, y, iw + 20 * k, sh, 10 * k); ctx.fill(); }
    const solukSik = cevap && !dogru;
    // harf rozeti
    const r = fs * 0.62;
    const cy = y + 4 * k + lh * 0.46;
    ctx.beginPath(); ctx.arc(ix + r, cy, r, 0, Math.PI * 2);
    ctx.fillStyle = dogru ? DOGRU : 'transparent'; ctx.fill();
    ctx.lineWidth = 1.5 * k; ctx.strokeStyle = dogru ? DOGRU : tm.soluk; ctx.stroke();
    ctx.font = `700 ${fs * 0.72}px ${FONT}`; ctx.textAlign = 'center';
    ctx.fillStyle = dogru ? '#fff' : solukSik ? tm.soluk : tm.yazi;
    ctx.fillText(h, ix + r, cy);
    ctx.textAlign = 'left';
    ctx.font = `${dogru ? 600 : 500} ${fs * 0.92}px ${FONT}`;
    ctx.fillStyle = solukSik ? tm.soluk : tm.yazi;
    let yy = cy;
    for (const l of sat) { ctx.fillText(l, ix + 50 * k, yy); yy += lh * 0.92; }
    y += sh + 8 * k;
  });
  if (cevap) {
    y += 10 * k;
    const ah = olcu.ac.length * lh * 0.82 + 24 * k;
    ctx.fillStyle = `${DOGRU}1a`; ctx.beginPath(); ctx.roundRect(ix - 10 * k, y, iw + 20 * k, ah + 18 * k, 12 * k); ctx.fill();
    ctx.fillStyle = DOGRU; ctx.fillRect(ix - 10 * k, y, 4 * k, ah + 18 * k);
    ctx.font = `700 ${fs * 0.62}px ${FONT}`; ctx.fillStyle = DOGRU;
    ctx.fillText(`DOĞRU CEVAP: ${q.dogru}`, ix + 10 * k, y + 16 * k);
    ctx.font = `500 ${fs * 0.82}px ${FONT}`; ctx.fillStyle = tm.yazi;
    let yy = y + 26 * k + lh * 0.41;
    for (const l of olcu.ac) { ctx.fillText(l, ix + 10 * k, yy); yy += lh * 0.82; }
  }
}

// ---------- WebVTT altyazı dosyası
const vttZaman = (t: number) => {
  const ms = Math.max(0, Math.round(t * 1000));
  const h = Math.floor(ms / 3_600_000), m = Math.floor((ms % 3_600_000) / 60_000), s = Math.floor((ms % 60_000) / 1000);
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}.${String(ms % 1000).padStart(3, '0')}`;
};
export function cdVideoVtt(paras: Para[], dersSure: number, soruC: SoruCizelge | null): string {
  const ip: { a: number; b: number; s: string }[] = [];
  for (const p of paras) {
    if (p.bas >= dersSure) break;
    let cb = 0;
    p.cumle.forEach((ce, c) => {
      const ws = p.kelimeler.filter((w) => w.b >= cb && w.b < ce);
      const a = c === 0 ? p.bas : ws[0]?.t ?? p.bas;
      const sonraki = p.kelimeler.find((w) => w.b >= ce);
      const b = Math.min(sonraki ? sonraki.t : p.son, dersSure);
      const s = p.metin.slice(cb, ce).trim();
      if (s && b > a) ip.push({ a, b, s });
      cb = ce;
    });
  }
  for (const d of soruC?.dilimler || []) {
    ip.push({ a: d.qBas, b: d.qSon, s: markdownsuz(d.soru.soru) });
    ip.push({ a: d.cBas, b: d.cSon, s: `Doğru cevap ${d.soru.dogru}. ${markdownsuz(d.soru.cozum)}` });
  }
  return `WEBVTT\n\n${ip.map((x, i) => `${i + 1}\n${vttZaman(x.a)} --> ${vttZaman(x.b)}\n${x.s}\n`).join('\n')}`;
}
