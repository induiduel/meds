/**
 * Canlı ders · video dışa aktarım (tamamen kullanıcının cihazında: WebCodecs + mediabunny, sunucuya iş düşmez).
 * Görüntü: o an okunan paragrafın PDF slaytı (pdf_isaret.py kutuları varsa okunan satır/kelime işaretli) + altta okunan
 * cümle, kelime kelime vurgulu. Ses: dersin MP3'ü yeniden kodlanmadan MP4'e aktarılır (paket kopyası).
 * Zamanlama sözleşmesi canlı dersle aynı: varyant.zamanlama (paragraf), kelimeZaman (kelime), detay.isaret (slayt kutusu).
 * Çıktı: Chrome/Edge masaüstünde doğrudan diske akış (showSaveFilePicker), diğerlerinde bellekte toplanıp indirilir.
 */
import * as pdfjs from 'pdfjs-dist';
import workerUrl from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import {
  ALL_FORMATS, BufferTarget, CanvasSource, EncodedAudioPacketSource, EncodedPacketSink, Input, Mp4OutputFormat, Output,
  QUALITY_HIGH, StreamTarget, UrlSource, canEncodeVideo,
} from 'mediabunny';
import { getCustomApiUrl } from '../../services/api';
import { resolveDeckPdf } from '../../services/deckPdfService';
import { cdSesUrl, type CdDetay, type CdIsaret, type CdVaryant } from './canliDersStore';

pdfjs.GlobalWorkerOptions.workerSrc = workerUrl;

export type CdVideoCozunurluk = '720p' | '1080p' | '2k' | '4k';
export const CD_VIDEO_BOYUT: Record<CdVideoCozunurluk, { w: number; h: number; etiket: string; bitHizi: number }> = {
  '720p': { w: 1280, h: 720, etiket: '720p HD', bitHizi: 4_000_000 },
  '1080p': { w: 1920, h: 1080, etiket: '1080p Full HD', bitHizi: 8_000_000 },
  '2k': { w: 2560, h: 1440, etiket: '2K (1440p)', bitHizi: 14_000_000 },
  '4k': { w: 3840, h: 2160, etiket: '4K (2160p)', bitHizi: 28_000_000 },
};
export const CD_VIDEO_FPS = 60;

export const cdVideoDestek = () => typeof window !== 'undefined' && 'VideoEncoder' in window && 'OffscreenCanvas' in window;

/** Cihaz bu çözünürlüğü 60 fps H.264 (yoksa VP9) kodlayabiliyor mu */
export async function cdVideoKodlanabilir(c: CdVideoCozunurluk): Promise<'avc' | 'vp9' | null> {
  if (!cdVideoDestek()) return null;
  const b = CD_VIDEO_BOYUT[c];
  for (const kod of ['avc', 'vp9'] as const) {
    try { if (await canEncodeVideo(kod, { width: b.w, height: b.h, bitrate: b.bitHizi })) return kod; } catch { /* sonraki */ }
  }
  return null;
}

export interface CdVideoIlerleme { asama: 'hazirlik' | 'kodlama' | 'bitiriliyor'; oran: number; t: number; sure: number; kalanSn?: number }
export interface CdVideoSecenek {
  detay: CdDetay;
  varyant: CdVaryant;
  cozunurluk: CdVideoCozunurluk;
  etiket: string;
  /** Diske akış (Chrome/Edge); verilmezse bellekte toplanıp Blob döner */
  dosya?: FileSystemWritableFileStream;
  /** Deneme/önizleme: yalnız ilk n saniye */
  enCokSn?: number;
  sinyal?: AbortSignal;
  onIlerleme?: (p: CdVideoIlerleme) => void;
}

// ---------- zaman çizelgesi
interface Kelime { b: number; e: number; t: number }
interface Para { i: number; metin: string; bas: number; son: number; kelimeler: Kelime[]; cumle: number[]; bolum: string }

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

function cizelge(detay: CdDetay, v: CdVaryant): Para[] {
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

const sonIndeks = <T,>(dizi: T[], t: number, al: (x: T) => number) => {
  let lo = 0, hi = dizi.length - 1, k = -1;
  while (lo <= hi) { const m = (lo + hi) >> 1; if (al(dizi[m]) <= t) { k = m; lo = m + 1; } else hi = m - 1; }
  return k;
};

const SAYFA_SURE_MS = 30_000;

// ---------- PDF sayfaları (önbellek: aynı anda en çok birkaç sayfa bellekte)
class Sayfalar {
  private belgeler = new Map<number, Promise<pdfjs.PDFDocumentProxy | null>>();
  private onbellek = new Map<string, Promise<ImageBitmap | null>>();
  constructor(private detay: CdDetay, private enX: number, private enY: number) {}
  private belge(d: number) {
    let p = this.belgeler.get(d);
    if (!p) {
      p = (async () => {
        const pdf = this.detay.pdf;
        if (!pdf?.deckId) return null;
        const url = (await resolveDeckPdf(pdf.deckId)).files[d]?.url;
        if (!url) return null;
        const base = `${getCustomApiUrl() || ''}/vendor/pdfjs/`;
        return pdfjs.getDocument({
          url, rangeChunkSize: 512 * 1024, disableStream: true, isEvalSupported: false,
          standardFontDataUrl: `${base}standard_fonts/`, cMapUrl: `${base}cmaps/`, cMapPacked: true,
        }).promise;
      })().catch(() => null);
      this.belgeler.set(d, p);
    }
    return p;
  }
  private deneme = new Map<string, number>();
  sayfa(d: number, s: number): Promise<ImageBitmap | null> {
    const k = `${d}:${s}`;
    let p = this.onbellek.get(k);
    if (!p) {
      p = (async () => {
        const doc = await this.belge(d);
        if (!doc || s < 1 || s > doc.numPages) return null;
        const pg = await doc.getPage(s);
        const v1 = pg.getViewport({ scale: 1 });
        const vp = pg.getViewport({ scale: Math.min(this.enX / v1.width, this.enY / v1.height) });
        // slayt görüntüleyicisiyle (PdfDocView) aynı yol: DOM canvas'ı
        const c = document.createElement('canvas');
        c.width = Math.ceil(vp.width); c.height = Math.ceil(vp.height);
        // takılan sayfa (ağır görsel/yazı tipi) işi durdurmasın: süre aşılırsa iptal, önceki slayt kalır
        // intent 'print': pdf.js requestAnimationFrame kullanmaz (sekme/pencere gizliyken rAF durur, çizim hiç bitmezdi)
        const is = pg.render({ canvas: c, viewport: vp, intent: 'print' });
        let zaman: ReturnType<typeof setTimeout> | undefined;
        const tamam = await Promise.race([
          is.promise.then(() => true),
          new Promise<boolean>((r) => { zaman = setTimeout(() => r(false), SAYFA_SURE_MS); }),
        ]).finally(() => clearTimeout(zaman));
        if (!tamam) { is.cancel(); c.width = 0; console.warn('video: slayt çizilemedi', d, s); return null; }
        pg.cleanup();
        const bmp = await createImageBitmap(c);
        c.width = 0;
        return bmp;
      })().catch(() => null);
      // sayfa getirme (aralık isteği) de takılabilir: üst süre
      p = Promise.race([p, new Promise<null>((r) => setTimeout(() => r(null), SAYFA_SURE_MS + 5_000))]);
      this.onbellek.set(k, p);
      // çizilemeyen sayfa bir kez daha denenir (geçici ağ/çizim hatası)
      p.then((b) => { if (!b && (this.deneme.get(k) || 0) < 1) { this.deneme.set(k, 1); this.onbellek.delete(k); } });
      // en eski sayfaları bırak
      while (this.onbellek.size > 6) {
        const ilk = this.onbellek.keys().next().value!;
        this.onbellek.delete(ilk); // kapatılmaz: çizimde hâlâ kullanılıyor olabilir (GC toplar)
      }
    }
    return p;
  }
  async sayfaSayisi(d: number): Promise<number> { return (await this.belge(d))?.numPages || 0; }
  /** sonraki sayfayı önceden hazırla */
  hazirla(d: number, s: number) { void this.sayfa(d, s); }
  kapat() {
    this.onbellek.forEach((p) => p.then((b) => b?.close()));
    this.belgeler.forEach((p) => p.then((d) => d?.destroy()));
  }
}

// ---------- sayfa zaman çizelgesi: PDF'in HER sayfası en az bir kez görünür
type Sayfa = [number, number];
interface SayfaDilim { t: number; d: number; s: number }
const SAYFA_EN_COK_SN = 4; // anlatımda geçmeyen sayfa en çok bu kadar görünür
const SAYFA_EN_AZ_SN = 1.2;

function sayfaCizelgesi(paras: Para[], detay: CdDetay, sure: number, sayilar: number[]): SayfaDilim[] {
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

// ---------- çizim
const RENK = { zemin: '#0f1419', kart: '#1a2129', yazi: '#e8edf2', soluk: '#7d8a97', okunan: '#ffd25c', vurgu: 'rgba(255, 196, 0, .28)', cizgi: '#ffb300' };
const FONT = '"Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif';

interface An { p: Para | null; w: number; c: number; isaret: CdIsaret | null; sayfa: [number, number] | null }

function anBul(paras: Para[], detay: CdDetay, t: number, cizelge: SayfaDilim[]): An {
  const sd = cizelge[Math.max(0, sonIndeks(cizelge, t, (x) => x.t))];
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

function satirlaraBol(ctx: OffscreenCanvasRenderingContext2D, kelimeler: { s: string; j: number }[], gen: number) {
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

function ciz(ctx: OffscreenCanvasRenderingContext2D, W: number, H: number, an: An, bmp: ImageBitmap | null, o: { baslik: string; etiket: string; t: number; sure: number }) {
  const k = H / 720;
  ctx.fillStyle = RENK.zemin; ctx.fillRect(0, 0, W, H);
  // üst şerit
  ctx.textBaseline = 'middle';
  ctx.font = `600 ${17 * k}px ${FONT}`; ctx.fillStyle = RENK.yazi;
  const ust = 30 * k;
  ctx.fillText(`${o.etiket} · ${o.baslik}`.slice(0, 110), 28 * k, ust);
  if (an.p?.bolum) {
    ctx.font = `500 ${15 * k}px ${FONT}`; ctx.fillStyle = RENK.soluk; ctx.textAlign = 'right';
    ctx.fillText(an.p.bolum.slice(0, 60), W - 28 * k, ust); ctx.textAlign = 'left';
  }
  // slayt alanı
  const metinY = H - 196 * k;
  const ax = 28 * k, ay = 58 * k, aw = W - 56 * k, ah = metinY - ay - 14 * k;
  if (bmp) {
    const s = Math.min(aw / bmp.width, ah / bmp.height);
    const w = bmp.width * s, h = bmp.height * s, x = ax + (aw - w) / 2, y = ay + (ah - h) / 2;
    ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.45)'; ctx.shadowBlur = 24 * k; ctx.fillStyle = '#fff'; ctx.fillRect(x, y, w, h); ctx.restore();
    ctx.drawImage(bmp, x, y, w, h);
    const is = an.isaret;
    if (is && an.sayfa && is.d === an.sayfa[0] && is.s === an.sayfa[1] && an.p) {
      ctx.fillStyle = RENK.vurgu;
      for (const [x0, y0, x1, y1] of is.l || []) ctx.fillRect(x + x0 * w, y + y0 * h, (x1 - x0) * w, (y1 - y0) * h);
      // okunan kelimenin slayttaki kutusu
      const cb = an.c ? an.p.cumle[an.c - 1] : 0;
      const kc = (an.p.kelimeler[an.w]?.b ?? 0) - cb;
      const wk = (is.w || []).find((q) => kc >= q[0] && kc < q[1]);
      if (wk) {
        ctx.strokeStyle = RENK.cizgi; ctx.lineWidth = 2.5 * k;
        ctx.strokeRect(x + wk[2] * w - 2 * k, y + wk[3] * h - 2 * k, (wk[4] - wk[2]) * w + 4 * k, (wk[5] - wk[3]) * h + 4 * k);
      }
    }
  } else {
    ctx.fillStyle = RENK.kart; ctx.fillRect(ax, ay, aw, ah);
    ctx.font = `700 ${34 * k}px ${FONT}`; ctx.fillStyle = RENK.yazi; ctx.textAlign = 'center';
    ctx.fillText((an.p?.bolum || o.baslik).slice(0, 60), ax + aw / 2, ay + ah / 2); ctx.textAlign = 'left';
  }
  // okunan cümle (en çok 3 satır; uzun cümlede okunan satırı içeren pencere)
  ctx.fillStyle = RENK.kart; ctx.fillRect(0, metinY, W, H - metinY);
  if (an.p) {
    const p = an.p;
    const cb = an.c ? p.cumle[an.c - 1] : 0, ce = p.cumle[an.c];
    const ks = p.kelimeler.map((w, j) => ({ w, j })).filter(({ w }) => w.b >= cb && w.b < ce).map(({ w, j }) => ({ s: p.metin.slice(w.b, w.e), j }));
    const fs = 30 * k;
    ctx.font = `500 ${fs}px ${FONT}`;
    const satir = satirlaraBol(ctx, ks, W - 120 * k);
    const okunanSatir = Math.max(0, satir.findIndex((s) => s.some((q) => q.j === an.w)));
    const bas = Math.min(Math.max(0, okunanSatir - 1), Math.max(0, satir.length - 3));
    const gor = satir.slice(bas, bas + 3);
    const lh = fs * 1.45;
    let y = metinY + (H - metinY - 6 * k) / 2 - ((gor.length - 1) * lh) / 2;
    for (const s of gor) {
      for (const q of s) {
        const xx = 60 * k + q.x;
        if (q.j === an.w) {
          const g = ctx.measureText(q.s).width;
          ctx.fillStyle = 'rgba(255, 210, 92, .18)';
          ctx.beginPath(); ctx.roundRect(xx - 6 * k, y - fs * 0.68, g + 12 * k, fs * 1.36, 8 * k); ctx.fill();
          ctx.fillStyle = RENK.okunan; // aynı kalınlık: satır ölçüsü bozulmasın
        } else ctx.fillStyle = q.j < an.w ? RENK.yazi : RENK.soluk;
        ctx.fillText(q.s, xx, y);
      }
      y += lh;
    }
  }
  // ilerleme çubuğu
  ctx.fillStyle = 'rgba(255,255,255,.08)'; ctx.fillRect(0, H - 6 * k, W, 6 * k);
  ctx.fillStyle = RENK.okunan; ctx.fillRect(0, H - 6 * k, W * Math.min(1, o.t / Math.max(1, o.sure)), 6 * k);
}

// ---------- ana iş
export async function cdVideoOlustur(o: CdVideoSecenek): Promise<Blob | null> {
  const b = CD_VIDEO_BOYUT[o.cozunurluk];
  const kod = await cdVideoKodlanabilir(o.cozunurluk);
  if (!kod) throw new Error(`Bu cihaz ${b.etiket} videoyu kodlayamıyor; daha düşük bir çözünürlük seç.`);
  o.onIlerleme?.({ asama: 'hazirlik', oran: 0, t: 0, sure: 0 });
  const paras = cizelge(o.detay, o.varyant);

  // ses: MP3 paketleri yeniden kodlanmadan
  const giris = new Input({ source: new UrlSource(cdSesUrl(o.detay.key, o.varyant.id)), formats: ALL_FORMATS });
  const sesIz = await giris.getPrimaryAudioTrack();
  if (!sesIz) throw new Error('Ders sesi okunamadı.');
  const sesKod = sesIz.codec;
  if (!sesKod) throw new Error('Ses biçimi tanınmadı.');
  const tamSure = Math.max(await giris.computeDuration(), paras.length ? paras[paras.length - 1].son : 0);
  const sure = o.enCokSn ? Math.min(tamSure, o.enCokSn) : tamSure;

  const hedef = o.dosya ? new StreamTarget(o.dosya as unknown as WritableStream, { chunked: true }) : new BufferTarget();
  const cikis = new Output({ format: new Mp4OutputFormat({ fastStart: o.dosya ? false : 'in-memory' }), target: hedef });
  const tuval = new OffscreenCanvas(b.w, b.h);
  const ctx = tuval.getContext('2d', { alpha: false })!;
  const video = new CanvasSource(tuval, { codec: kod, bitrate: b.bitHizi || QUALITY_HIGH, keyFrameInterval: 2, latencyMode: 'quality' });
  const ses = new EncodedAudioPacketSource(sesKod);
  cikis.addVideoTrack(video, { frameRate: CD_VIDEO_FPS });
  cikis.addAudioTrack(ses);
  await cikis.start();

  const sayfalar = new Sayfalar(o.detay, b.w - 56 * (b.h / 720), b.h - 268 * (b.h / 720));
  const sayilar = await Promise.all((o.detay.pdf?.dosyalar || []).map(async (f, d) => (await sayfalar.sayfaSayisi(d)) || f.pages || 0));
  const sCizelge = sayfaCizelgesi(paras, o.detay, sure, sayilar);
  const sIndeks = (d: number, s: number) => sCizelge.findIndex((x) => x.d === d && x.s === s);
  const kapsam = new Set(sCizelge.map((x) => `${x.d}:${x.s}`)).size;
  console.info(`video: ${sayilar.reduce((a, n) => a + n, 0)} sayfadan ${kapsam} sayfa zaman çizelgesinde`, sCizelge);
  const paketler = new EncodedPacketSink(sesIz).packets();
  const sesYapi = await sesIz.getDecoderConfig();
  let ilkPaket = true;
  let sesBitti = false;
  let bekleyen: Awaited<ReturnType<typeof paketler.next>>['value'] | null = null;
  const sesiItle = async (t: number) => {
    while (!sesBitti) {
      if (!bekleyen) {
        const r = await paketler.next();
        if (r.done) { sesBitti = true; break; }
        bekleyen = r.value;
      }
      const pk = bekleyen!;
      if (pk.timestamp > t || pk.timestamp >= sure) { if (pk.timestamp >= sure) sesBitti = true; break; }
      await ses.add(pk, ilkPaket && sesYapi ? { decoderConfig: sesYapi } : undefined);
      ilkPaket = false; bekleyen = null;
    }
  };

  const kare = Math.ceil(sure * CD_VIDEO_FPS);
  const dt = 1 / CD_VIDEO_FPS;
  let sonAnahtar = '';
  let sonSayfa: [number, number] | null = null;
  let bmp: ImageBitmap | null = null;
  const t0 = performance.now();
  let sonBildirim = 0;
  try {
    for (let f = 0; f < kare; f++) {
      if (o.sinyal?.aborted) throw new DOMException('İptal edildi', 'AbortError');
      const t = f * dt;
      const an = anBul(paras, o.detay, t, sCizelge);
      if (an.sayfa && (!sonSayfa || an.sayfa[0] !== sonSayfa[0] || an.sayfa[1] !== sonSayfa[1])) {
        bmp = (await sayfalar.sayfa(an.sayfa[0], an.sayfa[1])) || (await sayfalar.sayfa(an.sayfa[0], an.sayfa[1])) || bmp;
        const sonraki = sCizelge[sIndeks(an.sayfa[0], an.sayfa[1]) + 1];
        if (sonraki) sayfalar.hazirla(sonraki.d, sonraki.s);
        sonSayfa = an.sayfa;
      }
      // görüntü yalnız okunan kelime/sayfa ya da ilerleme çubuğu pikseli değişince yeniden çizilir
      const anahtar = `${an.p?.i}|${an.w}|${sonSayfa?.join(':')}|${Math.floor((t / sure) * b.w)}`;
      if (anahtar !== sonAnahtar) {
        ciz(ctx, b.w, b.h, an, bmp, { baslik: o.detay.baslik, etiket: o.etiket, t, sure });
        sonAnahtar = anahtar;
      }
      await video.add(t, dt);
      await sesiItle(t + 0.5);
      const simdi = performance.now();
      if (simdi - sonBildirim > 250) {
        sonBildirim = simdi;
        const oran = (f + 1) / kare;
        const gecen = (simdi - t0) / 1000;
        o.onIlerleme?.({ asama: 'kodlama', oran, t, sure, kalanSn: oran > 0.01 ? gecen / oran - gecen : undefined });
      }
    }
    await sesiItle(sure);
    o.onIlerleme?.({ asama: 'bitiriliyor', oran: 1, t: sure, sure });
    await cikis.finalize();
  } catch (e) {
    await cikis.cancel().catch(() => undefined);
    throw e;
  } finally {
    sayfalar.kapat();
    bmp = null;
    giris.dispose?.();
  }
  if (hedef instanceof BufferTarget) return new Blob([hedef.buffer!], { type: 'video/mp4' });
  return null;
}
