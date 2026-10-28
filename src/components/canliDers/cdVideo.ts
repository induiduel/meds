/**
 * Canlı ders · video dışa aktarım (tamamen kullanıcının cihazında: WebCodecs + mediabunny, sunucuya iş düşmez).
 * Ana iş parçacığı: PDF slaytlarını pdf.js ile çizer (sayfa başına bir kez), cihaz yeteneklerini sınar, pencere
 * önizlemesini çizer, dersin soru çözücü sorularını bulur. Kare çizimi + kodlama video işçisinde (cdVideoIsci.ts) yürür.
 * Çizim ve zaman çizelgesi: cdVideoCiz.ts (ikisi de aynı kodu kullanır).
 * Çıktı: Chrome/Edge masaüstünde doğrudan diske akış (showSaveFilePicker), diğerlerinde bellekte toplanıp indirilir.
 */
import * as pdfjs from 'pdfjs-dist';
import workerUrl from 'pdfjs-dist/build/pdf.worker.min.mjs?url';
import { canEncodeVideo, getFirstEncodableAudioCodec } from 'mediabunny';
import { getCustomApiUrl } from '../../services/api';
import { resolveDeckPdf } from '../../services/deckPdfService';
import { cdSesUrl, type CdDetay, type CdVaryant } from './canliDersStore';
import { CD_SPOT_BRANS } from './canliDersKategori';
import { cozucuDersYukle, cozucuDizinYukle, klipYolu, VARSAYILAN_SES, type CSoru } from '../spots/cozucu/cozucuVeri';
import type { Brans } from '../spots/brans';
import {
  CD_VIDEO_BICIM, CD_VIDEO_BOYUT, anBul, cdVideoBitHizi, cdVideoVtt, ciz, cizelge, slaytKutusu, soruCizelgesi,
  type CdVideoAyar, type CdVideoBicim, type CdVideoCozunurluk, type CdVideoSoru,
} from './cdVideoCiz';
import type { IsciBasla, IsciGelen, IsciGiden } from './cdVideoIsci';

pdfjs.GlobalWorkerOptions.workerSrc = workerUrl;

export const cdVideoDestek = () => typeof window !== 'undefined' && 'VideoEncoder' in window && 'OffscreenCanvas' in window && 'Worker' in window;

/** Cihaz bu biçim + çözünürlük + fps'i kodlayabiliyor mu */
export async function cdVideoKodlanabilir(a: Pick<CdVideoAyar, 'bicim' | 'cozunurluk' | 'fps' | 'kalite'>): Promise<boolean> {
  if (!cdVideoDestek()) return false;
  const b = CD_VIDEO_BOYUT[a.cozunurluk];
  try { return await canEncodeVideo(CD_VIDEO_BICIM[a.bicim].kod, { width: b.w, height: b.h, bitrate: cdVideoBitHizi(a) }); } catch { return false; }
}
/** Ses yeniden kodlanabiliyor mu (soru çözücü ve WebM için gerekli) */
export async function cdSesKodlanabilir(bicim: CdVideoBicim): Promise<boolean> {
  if (!cdVideoDestek()) return false;
  try {
    const ad = CD_VIDEO_BICIM[bicim].kap === 'webm' ? ['opus' as const] : ['aac' as const, 'opus' as const];
    return !!(await getFirstEncodableAudioCodec(ad, { numberOfChannels: 1, sampleRate: 48_000, bitrate: 128_000 }));
  } catch { return false; }
}

// ---------- PDF sayfaları (önbellek: aynı anda en çok birkaç sayfa bellekte)
const SAYFA_SURE_MS = 30_000;
class Sayfalar {
  private belgeler = new Map<number, Promise<pdfjs.PDFDocumentProxy | null>>();
  private onbellek = new Map<string, Promise<ImageBitmap | null>>();
  private deneme = new Map<string, number>();
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
  /** Sayfanın görüntüsü; döndürülen bitmap çağırana aittir (kopya: işçiye aktarılınca önbellektekisi bozulmaz) */
  async kopya(d: number, s: number): Promise<ImageBitmap | null> {
    const b = (await this.sayfa(d, s)) || (await this.sayfa(d, s));
    if (!b) return null;
    try { return await createImageBitmap(b); } catch { return null; }
  }
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
      while (this.onbellek.size > 6) {
        const ilk = this.onbellek.keys().next().value!;
        const eski = this.onbellek.get(ilk);
        this.onbellek.delete(ilk);
        eski?.then((b) => b?.close()); // işçiye hep kopya gider: güvenle kapatılır
      }
    }
    return p;
  }
  async sayfaSayisi(d: number): Promise<number> { return (await this.belge(d))?.numPages || 0; }
  hazirla(d: number, s: number) { void this.sayfa(d, s); }
  kapat() {
    this.onbellek.forEach((p) => p.then((b) => b?.close()));
    this.belgeler.forEach((p) => p.then((d) => d?.destroy()));
  }
}
const sayfaSayilari = (detay: CdDetay, sf: Sayfalar) =>
  Promise.all((detay.pdf?.dosyalar || []).map(async (f, d) => (await sf.sayfaSayisi(d)) || f.pages || 0));

// ---------- dersin soru çözücü soruları
const nz = (s: string) => (s || '').toLocaleLowerCase('tr').replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
const IZ = import.meta.glob('../../data/*_cozucu/index.json', { eager: false, import: 'default' }) as Record<string, () => Promise<{ dersler?: { kod: string; baslik: string; no?: number }[] }>>;
export interface CdSoruKaynak { brans: Brans; kodlar: string[] }

/** Dersin çözücü seti: önce başlıkla (Kurul 2+), yoksa Kurul 1 branşı + ders numarasıyla */
export async function cdCozucuBul(detay: CdDetay): Promise<CdSoruKaynak | null> {
  const b = nz(detay.baslik);
  for (const [yol, yukle] of Object.entries(IZ)) {
    const brans = yol.match(/data\/([^/]*)_cozucu\//)?.[1];
    if (!brans || brans === 'cozucu_ogren' || brans.endsWith('_alt')) continue;
    if (!/^k\d/.test(brans)) continue;
    try {
      const d = await yukle();
      const ks = (d.dersler || []).filter((x) => nz(x.baslik) === b).map((x) => x.kod);
      if (ks.length) return { brans: brans as Brans, kodlar: ks };
    } catch { /* sonraki */ }
  }
  const brans = detay.brans ? CD_SPOT_BRANS[detay.brans] : undefined;
  const no = Number(detay.no);
  if (brans && Number.isFinite(no)) {
    try {
      const dz = await cozucuDizinYukle(brans);
      const ks = dz.dersler.filter((x) => Number(x.no) === no).map((x) => x.kod);
      if (ks.length) return { brans, kodlar: ks };
    } catch { /* yok */ }
  }
  return null;
}

const mutlak = (u: string) => new URL(u, location.href).href;

/** Video için sorular: soru (kök + şıklar) ve çözüm (doğru cevap + açıklama) klibi olanlar */
export async function cdVideoSorulari(k: CdSoruKaynak, tur: CdVideoAyar['cozucu']['tur']): Promise<CdVideoSoru[]> {
  const out: CdVideoSoru[] = [];
  const goruldu = new Set<string>();
  for (const kod of k.kodlar) {
    let ders;
    try { ders = await cozucuDersYukle(kod, k.brans); } catch { continue; }
    const klasorAdi = ders.klasor || ders.kod || kod;
    for (const q of ders.sorular as CSoru[]) {
      if (tur !== 'hepsi' && (tur === 'cikmis' ? q.tur !== 'cikmis' : q.tur === 'cikmis')) continue;
      const klasor = q.klasor || klasorAdi;
      const n = q.kn ?? q.no;
      const al = (on: string) => {
        const kl = ders!.klip[`${klasor}/${on}-${n}`] || ders!.klip[`${on}-${n}`];
        return kl ? { url: mutlak(`${getCustomApiUrl() || ''}${klipYolu(k.brans, VARSAYILAN_SES, klasor, `${on}-${n}`)}?v=${kl.v}`), sure: kl.sure } : null;
      };
      const qk = al('q'), ck = al('c');
      const anahtar = `${klasor}/${n}`;
      if (!qk || !ck || goruldu.has(anahtar) || !q.secenekler?.[q.dogru]) continue;
      goruldu.add(anahtar);
      out.push({ no: Number(q.no), tur: q.tur, sinav: q.sinav, soru: q.soru, secenekler: { ...q.secenekler }, dogru: q.dogru, cozum: q.cozum, q: qk, c: ck });
    }
  }
  return out;
}

// ---------- pencere önizlemesi (aynı çizim kodu, küçük boyut)
export interface CdOnizleyici { ciz: (ayar: CdVideoAyar, kip: 'ders' | 'soru', sorular: CdVideoSoru[]) => Promise<void>; kapat: () => void }
export function cdVideoOnizleyici(canvas: HTMLCanvasElement, detay: CdDetay, varyant: CdVaryant, etiket: string): CdOnizleyici {
  const W = canvas.width, H = canvas.height;
  let sf: Sayfalar | null = null, sfAnahtar = '';
  let paras: ReturnType<typeof cizelge> = [];
  try { paras = cizelge(detay, varyant); } catch { /* zamanlama yok */ }
  // örnek an: derste ilk sözü olan paragrafın birkaç kelime sonrası (sayfa işareti olan cümle tercih edilir)
  const ornek = paras.find((p) => detay.isaret?.[p.i]?.some((x) => x?.s)) || paras[Math.min(1, paras.length - 1)];
  return {
    async ciz(ayar, kip, sorular) {
      const ctx = canvas.getContext('2d');
      if (!ctx) return;
      const baglam = { W, H, ayar, baslik: detay.baslik, etiket, t: 0, sure: 1, not: detay.ogrenciNot, soruSay: sorular.length };
      if (kip === 'soru' && sorular.length) {
        const sc = soruCizelgesi(0, sorular.slice(0, 1), ayar.cozucu.dusunSn)!;
        const d = sc.dilimler[0];
        baglam.t = 0.8; baglam.sure = 1;
        ciz(ctx, { p: null, w: -1, c: -1, isaret: null, sayfa: null, soru: { evre: 'cevap', d } }, null, baglam);
        return;
      }
      const t = ornek ? ornek.kelimeler[Math.min(3, ornek.kelimeler.length - 1)]?.t ?? ornek.bas : 0;
      const sure = Math.max(1, paras.length ? paras[paras.length - 1].son : 1);
      baglam.t = t; baglam.sure = sure;
      const kutu = slaytKutusu(ayar, W, H);
      let bmp: ImageBitmap | null = null;
      const an = anBul(paras, detay, t, [], null);
      // slayt: önce o cümlenin işaretli sayfası, yoksa paragrafın sayfası, o da yoksa ilk sayfa
      const e = an.p ? detay.pdf?.paragraflar?.[an.p.i] : undefined;
      const sayfa: [number, number] = an.isaret?.s ? [an.isaret.d, an.isaret.s] : e ? [e.dosya, e.sayfa] : [0, 1];
      an.sayfa = sayfa;
      if (kutu.w > 0 && detay.pdf) {
        const a = `${Math.round(kutu.w)}x${Math.round(kutu.h)}`;
        if (a !== sfAnahtar) { sf?.kapat(); sf = new Sayfalar(detay, kutu.w * 1.5, kutu.h * 1.5); sfAnahtar = a; }
        bmp = await sf!.sayfa(sayfa[0], sayfa[1]);
      }
      ciz(ctx, an, bmp, baglam);
    },
    kapat() { sf?.kapat(); sf = null; },
  };
}

// ---------- üretim
export interface CdVideoIlerleme { asama: 'hazirlik' | 'kodlama' | 'bitiriliyor'; oran: number; t: number; sure: number; kalanSn?: number }
export interface CdVideoSecenek {
  detay: CdDetay;
  varyant: CdVaryant;
  ayar: CdVideoAyar;
  etiket: string;
  sorular: CdVideoSoru[];
  /** Diske akış (Chrome/Edge); verilmezse bellekte toplanıp Blob döner */
  dosya?: FileSystemFileHandle;
  /** sınama: ders bölümü en çok bu kadar saniye */
  enCokSn?: number;
  sinyal?: AbortSignal;
  onIlerleme?: (p: CdVideoIlerleme) => void;
}

/** Videoyu üretir. Döner: blob (bellekte üretildiyse) + istenirse VTT altyazı metni */
export async function cdVideoOlustur(o: CdVideoSecenek): Promise<{ blob: Blob | null; vtt: string | null }> {
  if (!(await cdVideoKodlanabilir(o.ayar))) throw new Error('Bu cihaz seçilen biçim ve çözünürlükte videoyu kodlayamıyor; daha düşük bir çözünürlük ya da MP4 · H.264 seç.');
  if (o.sinyal?.aborted) throw new DOMException('İptal edildi', 'AbortError');
  o.onIlerleme?.({ asama: 'hazirlik', oran: 0, t: 0, sure: 0 });
  const B = CD_VIDEO_BOYUT[o.ayar.cozunurluk];
  const kutu = slaytKutusu(o.ayar, B.w, B.h);
  const sf = new Sayfalar(o.detay, Math.max(1, kutu.w), Math.max(1, kutu.h));
  const sayilar = await sayfaSayilari(o.detay, sf);
  const isci = new Worker(new URL('./cdVideoIsci.ts', import.meta.url), { type: 'module', name: 'medsor-video' });
  const sesUrl = mutlak(cdSesUrl(o.detay.key, o.varyant.id));
  try {
    const sonuc = await new Promise<{ blob?: Blob; diskte: boolean; dersSure: number }>((coz, red) => {
      const iptalEt = () => isci.postMessage({ tur: 'iptal' } satisfies IsciGelen);
      o.sinyal?.addEventListener('abort', iptalEt, { once: true });
      isci.onerror = (e) => { e.preventDefault(); red(new Error(e.message || 'Video işçisi başlatılamadı.')); };
      isci.onmessage = async (e: MessageEvent<IsciGiden>) => {
        const m = e.data;
        if (m.tur === 'ilerleme') o.onIlerleme?.(m);
        else if (m.tur === 'sayfa') {
          const bmp = await sf.kopya(m.d, m.s);
          isci.postMessage({ tur: 'sayfa', id: m.id, bmp } satisfies IsciGelen, bmp ? [bmp] : []);
          if (m.sonraki) sf.hazirla(m.sonraki[0], m.sonraki[1]);
        } else if (m.tur === 'bitti') coz(m);
        else if (m.tur === 'iptal') red(new DOMException('İptal edildi', 'AbortError'));
        else if (m.tur === 'hata') red(new Error(m.mesaj));
      };
      const basla: IsciBasla = {
        tur: 'basla', detay: o.detay, varyant: o.varyant, ayar: o.ayar, etiket: o.etiket, sesUrl, sayilar,
        sorular: o.ayar.cozucu.acik ? o.sorular : [], dosya: o.dosya, enCokSn: o.enCokSn,
      };
      isci.postMessage(basla satisfies IsciGelen);
    });
    let vtt: string | null = null;
    if (o.ayar.vtt) {
      const paras = cizelge(o.detay, o.varyant);
      const dersSure = sonuc.dersSure;
      vtt = cdVideoVtt(paras, dersSure, o.ayar.cozucu.acik ? soruCizelgesi(dersSure, o.sorular, o.ayar.cozucu.dusunSn) : null);
    }
    if (!sonuc.diskte && !sonuc.blob) throw new Error('Video dosyası oluşturulamadı.');
    return { blob: sonuc.blob || null, vtt };
  } finally {
    isci.terminate();
    sf.kapat();
  }
}
