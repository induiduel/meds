/// <reference lib="webworker" />
/**
 * Canlı ders · video işçisi (Dedicated Worker): kare çizimi + video/ses kodlama ana iş parçacığından ayrı yürür.
 * Sekme arka plandayken ana iş parçacığının zamanlayıcıları kısılır; işçi bundan etkilenmez, arayüz de takılmaz.
 * Slayt görüntüleri (pdf.js) ana iş parçacığında çizilip ImageBitmap olarak aktarılır ('sayfa' mesajı).
 * Ses: soru çözücü kapalı + MP4 ise dersin MP3'ü yeniden kodlanmadan kopyalanır; değilse çözülüp AAC/Opus'a kodlanır
 * (ders sesi + sessizlik + soru klipleri tek iz).
 */
import {
  ALL_FORMATS, AudioSample, BufferSource, AudioSampleSink, AudioSampleSource, BufferTarget, CanvasSource, EncodedAudioPacketSource,
  EncodedPacketSink, Input, Mp4OutputFormat, Output, StreamTarget, UrlSource, WebMOutputFormat, getFirstEncodableAudioCodec,
  type InputAudioTrack,
} from 'mediabunny';
import type { CdDetay, CdVaryant } from './canliDersStore';
import {
  CD_VIDEO_BICIM, CD_VIDEO_BOYUT, anAnahtari, anBul, cdVideoBitHizi, ciz, cizelge, sayfaCizelgesi, slaytKutusu, soruCizelgesi,
  type CdVideoAyar, type CdVideoSoru,
} from './cdVideoCiz';

declare const self: DedicatedWorkerGlobalScope;

export interface IsciBasla {
  tur: 'basla';
  detay: CdDetay; varyant: CdVaryant; ayar: CdVideoAyar; etiket: string;
  sesUrl: string; sayilar: number[]; sorular: CdVideoSoru[];
  dosya?: FileSystemFileHandle;
  /** sınama: ders bölümü en çok bu kadar saniye */
  enCokSn?: number;
}
export type IsciGelen = IsciBasla | { tur: 'iptal' } | { tur: 'sayfa'; id: number; bmp: ImageBitmap | null };
export type IsciGiden =
  | { tur: 'ilerleme'; asama: 'hazirlik' | 'kodlama' | 'bitiriliyor'; oran: number; t: number; sure: number; kalanSn?: number }
  | { tur: 'sayfa'; id: number; d: number; s: number; sonraki?: [number, number] }
  | { tur: 'bitti'; blob?: Blob; diskte: boolean; dersSure: number }
  | { tur: 'iptal' }
  | { tur: 'hata'; mesaj: string };

const gonder = (m: IsciGiden, aktar?: Transferable[]) => self.postMessage(m, aktar || []);
let iptal = false;
const bekleyen = new Map<number, (b: ImageBitmap | null) => void>();
let sayac = 0;
const sayfaIste = (d: number, s: number, sonraki?: [number, number]) => new Promise<ImageBitmap | null>((r) => {
  const id = ++sayac;
  bekleyen.set(id, r);
  gonder({ tur: 'sayfa', id, d, s, sonraki });
});

self.onmessage = (e: MessageEvent<IsciGelen>) => {
  const m = e.data;
  if (m.tur === 'iptal') iptal = true;
  else if (m.tur === 'sayfa') { bekleyen.get(m.id)?.(m.bmp); bekleyen.delete(m.id); }
  else if (m.tur === 'basla') {
    uret(m).then(
      (r) => gonder({ tur: 'bitti', blob: r.blob, diskte: !r.blob, dersSure: r.dersSure }),
      (err) => gonder(err?.name === 'AbortError' ? { tur: 'iptal' } : { tur: 'hata', mesaj: err?.message || 'Video oluşturulamadı.' }),
    );
  }
};

const SES_HZ = 48_000;
/** Geçici ağ hatasında (502, bağlantı kopması) artan bekleme ile yeniden dene; 6 denemeden sonra vazgeç */
const yenidenDene = (n: number) => (n < 6 ? Math.min(8, 0.5 * 2 ** n) : null);
async function klipGetir(url: string): Promise<ArrayBuffer> {
  for (let n = 0; ; n++) {
    try {
      const r = await fetch(url, { credentials: 'include' });
      if (r.ok) return await r.arrayBuffer();
      if (r.status < 500 && r.status !== 429) throw new Error(`HTTP ${r.status}`);
    } catch (e) { if (n >= 4) throw e; }
    if (n >= 4) throw new Error('klip alınamadı');
    await new Promise((r) => setTimeout(r, 500 * 2 ** n));
  }
}
const PARCA_SN = 0.5;
const sessiz = (ts: number, sn: number) => new AudioSample({
  data: new Float32Array(Math.max(1, Math.round(sn * SES_HZ))), format: 'f32', numberOfChannels: 1, sampleRate: SES_HZ, timestamp: ts,
});

/** Kodlayıcı tek biçim ister (ders sesi ve klipler farklı hızda olabilir): mono'ya indirip doğrusal olarak SES_HZ'ye örnekler */
function tekBicim(s: AudioSample, ts: number): AudioSample {
  const n = s.numberOfFrames, ch = s.numberOfChannels, sr = s.sampleRate;
  const mono = new Float32Array(n);
  const kanal = new Float32Array(n);
  for (let c = 0; c < ch; c++) {
    s.copyTo(kanal, { planeIndex: c, format: 'f32-planar' });
    for (let i = 0; i < n; i++) mono[i] += kanal[i] / ch;
  }
  let veri = mono;
  if (sr !== SES_HZ) {
    const m = Math.max(1, Math.round((n * SES_HZ) / sr));
    veri = new Float32Array(m);
    const oran = sr / SES_HZ;
    for (let i = 0; i < m; i++) {
      const x = i * oran, a = Math.floor(x), f = x - a;
      const v0 = mono[Math.min(a, n - 1)], v1 = mono[Math.min(a + 1, n - 1)];
      veri[i] = v0 + (v1 - v0) * f;
    }
  }
  return new AudioSample({ data: veri, format: 'f32', numberOfChannels: 1, sampleRate: SES_HZ, timestamp: ts });
}

/** Zaman sırasıyla ses örnekleri: [bas, son) aralığını doldurur (kısa kalan klip sessizlikle tamamlanır) */
async function* izOrnekleri(iz: InputAudioTrack | null, bas: number, son: number): AsyncGenerator<AudioSample> {
  let t = bas;
  if (iz) {
    for await (const s of new AudioSampleSink(iz).samples(0, son - bas)) {
      const ts = bas + s.timestamp;
      if (ts >= son) { s.close(); break; }
      if (ts + s.duration <= t + 1e-4) { s.close(); continue; } // örtüşen (öncekiyle aynı aralık) örnek
      if (ts > t + 0.02) yield* sessizlik(t, ts);
      const k = ts + s.duration > son ? s.trim(0, Math.max(1, Math.floor((son - ts) * s.sampleRate))) : null;
      if (k) s.close();
      const o = tekBicim(k || s, Math.max(ts, t));
      (k || s).close();
      t = o.timestamp + o.duration;
      yield o;
    }
  }
  if (t < son - 0.01) yield* sessizlik(t, son);
}
async function* sessizlik(bas: number, son: number): AsyncGenerator<AudioSample> {
  for (let t = bas; t < son - 1e-4; t += PARCA_SN) yield sessiz(t, Math.min(PARCA_SN, son - t));
}

async function uret(m: IsciBasla): Promise<{ blob?: Blob; dersSure: number }> {
  iptal = false;
  const { ayar, detay } = m;
  const b = CD_VIDEO_BOYUT[ayar.cozunurluk];
  const bicim = CD_VIDEO_BICIM[ayar.bicim];
  const fps = ayar.fps;
  gonder({ tur: 'ilerleme', asama: 'hazirlik', oran: 0, t: 0, sure: 0 });
  const paras = cizelge(detay, m.varyant);

  const giris = new Input({ source: new UrlSource(m.sesUrl, { getRetryDelay: yenidenDene }), formats: ALL_FORMATS });
  const sesIz = await giris.getPrimaryAudioTrack();
  if (!sesIz) throw new Error('Ders sesi okunamadı.');
  const tamSure = Math.max(await giris.computeDuration(), paras.length ? paras[paras.length - 1].son : 0);
  const dersSure = m.enCokSn ? Math.min(tamSure, m.enCokSn) : tamSure;
  const soruC = ayar.cozucu.acik ? soruCizelgesi(dersSure, m.sorular, ayar.cozucu.dusunSn) : null;
  const sure = soruC ? soruC.son : dersSure;

  const kopya = bicim.kap === 'mp4' && !soruC && !!sesIz.codec && ['mp3', 'aac'].includes(sesIz.codec);
  let yazici: FileSystemWritableFileStream | null = null;
  if (m.dosya) { try { yazici = await m.dosya.createWritable(); } catch { yazici = null; } }
  const hedef = yazici ? new StreamTarget(yazici as unknown as WritableStream, { chunked: true }) : new BufferTarget();
  // diske akışta MP4 fastStart kapalı (moov sonda); bellekte başa alınır
  const format = bicim.kap === 'webm' ? new WebMOutputFormat() : new Mp4OutputFormat({ fastStart: yazici ? false : 'in-memory' });
  const cikis = new Output({ format, target: hedef });

  const tuval = new OffscreenCanvas(b.w, b.h);
  const ctx = tuval.getContext('2d', { alpha: false })!;
  const video = new CanvasSource(tuval, { codec: bicim.kod, bitrate: cdVideoBitHizi(ayar), keyFrameInterval: 2, latencyMode: 'quality' });
  cikis.addVideoTrack(video, { frameRate: fps });

  // ses kaynağı
  let sesEkle: (t: number) => Promise<void>;
  if (kopya) {
    const ses = new EncodedAudioPacketSource(sesIz.codec!);
    cikis.addAudioTrack(ses);
    const paketler = new EncodedPacketSink(sesIz).packets();
    const sesYapi = await sesIz.getDecoderConfig();
    let ilk = true, bitti = false;
    let bek: Awaited<ReturnType<typeof paketler.next>>['value'] | null = null;
    sesEkle = async (t: number) => {
      while (!bitti) {
        if (!bek) { const r = await paketler.next(); if (r.done) { bitti = true; break; } bek = r.value; }
        const pk = bek!;
        if (pk.timestamp > t || pk.timestamp >= sure) { if (pk.timestamp >= sure) bitti = true; break; }
        await ses.add(pk, ilk && sesYapi ? { decoderConfig: sesYapi } : undefined);
        ilk = false; bek = null;
      }
    };
  } else {
    const adaylar = (bicim.kap === 'webm' ? ['opus'] : ['aac', 'opus']) as ('aac' | 'opus')[];
    const kod = await getFirstEncodableAudioCodec(adaylar, { numberOfChannels: 1, sampleRate: SES_HZ, bitrate: 128_000 });
    if (!kod) throw new Error('Bu tarayıcı sesi kodlayamıyor; biçim olarak MP4 · H.264 seç ve soru çözücüyü kapat.');
    const ses = new AudioSampleSource({ codec: kod, bitrate: 128_000 });
    cikis.addAudioTrack(ses);
    const klipler: Input[] = [];
    async function* akis(): AsyncGenerator<AudioSample> {
      yield* izOrnekleri(sesIz!, 0, dersSure);
      if (!soruC) return;
      let t = dersSure;
      for (const d of soruC.dilimler) {
        yield* sessizlik(t, d.qBas);
        for (const [k, a, z] of [[d.soru.q, d.qBas, d.qSon], [d.soru.c, d.cBas, d.cSon]] as const) {
          let iz: InputAudioTrack | null = null;
          try {
            const g = new Input({ source: new BufferSource(await klipGetir(k.url)), formats: ALL_FORMATS });
            klipler.push(g);
            iz = await g.getPrimaryAudioTrack();
          } catch (err) { console.warn('video: soru klibi okunamadı', k.url, err); }
          yield* izOrnekleri(iz, a, z);
          if (a === d.qBas) yield* sessizlik(d.qSon, d.cBas);
        }
        t = d.cSon;
      }
      yield* sessizlik(t, soruC.son);
    }
    const it = akis();
    let bek: AudioSample | null = null, bitti = false;
    sesEkle = async (t: number) => {
      while (!bitti) {
        if (!bek) { const r = await it.next(); if (r.done) { bitti = true; break; } bek = r.value; }
        if (bek!.timestamp > t) break;
        await ses.add(bek!); bek!.close(); bek = null;
      }
    };
    void klipler;
  }
  await cikis.start();

  const kutu = slaytKutusu(ayar, b.w, b.h);
  const sCizelge = ayar.duzen === 'metin' ? [] : sayfaCizelgesi(paras, detay, dersSure, m.sayilar);
  const sIndeks = (d: number, s: number) => sCizelge.findIndex((x) => x.d === d && x.s === s);

  const kare = Math.ceil(sure * fps);
  const dt = 1 / fps;
  let sonAnahtar = '';
  let sonSayfa: [number, number] | null = null;
  let bmp: ImageBitmap | null = null;
  const t0 = performance.now();
  let sonBildirim = 0;
  const baglam = { W: b.w, H: b.h, ayar, baslik: detay.baslik, etiket: m.etiket, t: 0, sure, not: detay.ogrenciNot, soruSay: soruC?.dilimler.length };
  try {
    for (let f = 0; f < kare; f++) {
      if (iptal) throw new DOMException('İptal edildi', 'AbortError');
      const t = f * dt;
      const an = anBul(paras, detay, t, sCizelge, soruC);
      if (kutu.w > 0 && an.sayfa && (!sonSayfa || an.sayfa[0] !== sonSayfa[0] || an.sayfa[1] !== sonSayfa[1])) {
        const sn = sCizelge[sIndeks(an.sayfa[0], an.sayfa[1]) + 1];
        const yeni = await sayfaIste(an.sayfa[0], an.sayfa[1], sn ? [sn.d, sn.s] : undefined);
        if (yeni) { bmp?.close(); bmp = yeni; }
        sonSayfa = an.sayfa;
      }
      const anahtar = anAnahtari(an, sonSayfa?.join(':') || '', ayar.ilerleme ? Math.floor((t / sure) * b.w) : 0);
      if (anahtar !== sonAnahtar) {
        baglam.t = t;
        ciz(ctx, an, bmp, baglam);
        sonAnahtar = anahtar;
      }
      await video.add(t, dt);
      await sesEkle(t + 0.5);
      const simdi = performance.now();
      if (simdi - sonBildirim > 250) {
        sonBildirim = simdi;
        const oran = (f + 1) / kare;
        const gecen = (simdi - t0) / 1000;
        gonder({ tur: 'ilerleme', asama: 'kodlama', oran, t, sure, kalanSn: oran > 0.01 ? gecen / oran - gecen : undefined });
      }
    }
    await sesEkle(sure + 1);
    gonder({ tur: 'ilerleme', asama: 'bitiriliyor', oran: 1, t: sure, sure });
    await cikis.finalize();
  } catch (e) {
    await cikis.cancel().catch(() => undefined);
    if (yazici) await yazici.abort().catch(() => undefined);
    throw e;
  } finally {
    bmp?.close();
    giris.dispose?.();
  }
  if (hedef instanceof BufferTarget) return { blob: new Blob([hedef.buffer!], { type: bicim.kap === 'webm' ? 'video/webm' : 'video/mp4' }), dersSure };
  return { dersSure };
}
