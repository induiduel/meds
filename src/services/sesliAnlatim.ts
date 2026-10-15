// Sesli anlatım: ders konuşma metinlerini MP3'e çeviren kuyruk + yönetim uçları.
//
// Veri: data/sesli_anlatim/
//   dersler.json   — ders listesi (sıra, başlık, varsayılan sağlayıcı)   [repo]
//   metin/<key>.md — konuşma metni (# başlık, @@ bölüm, paragraflar)      [repo]
//   kayit.json     — üretilmiş sesler (varyantlar)                        [çalışma durumu]
//   kuyruk.json    — işler                                                [çalışma durumu]
//   butce.json     — ücretli anahtar harcama defteri                       [çalışma durumu]
//   ayar.json      — işçi açık/kapalı
//   ses/<key>/<vid>.mp3, ses/<key>/.parca/<isId>/NNN.mp3 (yarım işin parçaları; kaldığı yerden sürer)
//
// Sağlayıcılar: Microsoft Edge Emel (ücretsiz), Gemini TTS ücretsiz anahtar havuzu (GEMINI_API_KEY + GEMINI_FREE_KEY_N),
// Gemini TTS ücretli anahtar (TTS_PAID_GEMINI_KEY; yalnız panelden elle, bütçe kilidi 850 TL / tavan 900 TL).
import type { Express, Request, Response, NextFunction } from 'express';
import fs from 'fs';
import path from 'path';
import { MsEdgeTTS, OUTPUT_FORMAT } from 'msedge-tts';
import { Mp3Encoder } from '@breezystack/lamejs';
import { freeGeminiKeyNames } from './aiProvider';
import { isStrongAdmin } from './peopleInsights';

type Saglayici = 'edge-emel' | 'gemini-ucretsiz' | 'gemini-ucretli';
type IsDurum = 'bekliyor' | 'calisiyor' | 'kota-bekliyor' | 'bitti' | 'hata' | 'iptal' | 'butce-durdu';

interface Varyant {
  id: string;
  saglayici: Saglayici;
  ses: string;
  model?: string;
  etiket: string;
  ucretli: boolean;
  sureSn: number;
  bayt: number;
  parca: number;
  metinHash: string;
  olusturuldu: string;
  maliyetTL?: number;
  dogrulama?: { parca: number; toplam: number; ortalama: number | null };
  /** Paragraf zamanları [baş, son] sn; dizin = metindeki global paragraf sırası. Aralıklar bitişiktir (son = sonrakinin başı). */
  zamanlama?: [number, number][];
  /** olcum: üretimde ölçüldü · tahmini: parça içi karakter oranı · sessizlik / karakter: zamanlama_cikar.py */
  zamanlamaKaynak?: string;
}
interface Is {
  id: string;
  key: string;
  saglayici: Saglayici;
  ses: string;
  durum: IsDurum;
  varsayilanYap: boolean;
  ilerleme: { bitti: number; toplam: number };
  olusturuldu: string;
  basladi?: string;
  bitti?: string;
  sonrakiDeneme?: string;
  hata?: string;
  notlar?: string[];
  maliyetTL?: number;
  isteyen?: string;
}
interface Ders { key: string; no: number; baslik: string; sira: number; ses: 'emel' | 'aoede' }

const KOK = path.join(process.cwd(), 'data', 'sesli_anlatim');
const P = {
  dersler: path.join(KOK, 'dersler.json'),
  kayit: path.join(KOK, 'kayit.json'),
  kuyruk: path.join(KOK, 'kuyruk.json'),
  butce: path.join(KOK, 'butce.json'),
  ayar: path.join(KOK, 'ayar.json'),
  metin: (k: string) => path.join(KOK, 'metin', `${k}.md`),
  sesDir: (k: string) => path.join(KOK, 'ses', k),
  ses: (k: string, v: string) => path.join(KOK, 'ses', k, `${v}.mp3`),
  parcaDir: (k: string, isId: string) => path.join(KOK, 'ses', k, '.parca', isId),
};

// Ücretli bütçe: Google'ın 2026 fiyatı 9 $/1M ses tokenı; defter temkinli olsun diye 2 katı ve yüksek kurla hesaplar.
const BUTCE = { tavanTL: 900, kilitTL: 850, sesUsdMilyon: 18, metinUsdMilyon: 2, usdTry: 50 };
const GEMINI_MODEL = 'gemini-3.8-flash-tts';
const GEMINI_SESLER = ['Aoede', 'Kore', 'Leda', 'Despina', 'Sulafat', 'Achernar', 'Callirrhoe', 'Vindemiatrix'];
const EDGE_HIZ = '+12%';
const KELIME_DK = 112; // Emel %12 hızda ölçüldü
const EDGE_PARCA = 2400;
const GEMINI_PARCA = 3000;
const STIL =
  'Aşağıdaki Türkçe tıp dersi anlatımını, deneyimli bir kadın patoloji hocası gibi sıcak, net ve öğretici bir tonda, ' +
  'normalden yüzde on kadar hızlı ve akıcı bir tempoda, tıbbi terimleri özenle ve doğru telaffuz ederek oku. ' +
  'Metni değiştirme, hiçbir şey ekleme ya da atlama, bu yönergeyi okuma:\n\n';

const SAGLAYICILAR: Record<Saglayici, { etiket: string; ucretli: boolean; sesler: string[]; varsayilanSes: string }> = {
  'edge-emel': { etiket: 'Microsoft Edge · Emel', ucretli: false, sesler: ['Emel'], varsayilanSes: 'Emel' },
  'gemini-ucretsiz': { etiket: 'Google Gemini TTS · ücretsiz anahtarlar', ucretli: false, sesler: GEMINI_SESLER, varsayilanSes: 'Aoede' },
  'gemini-ucretli': { etiket: 'Google Gemini TTS · ücretli anahtar', ucretli: true, sesler: GEMINI_SESLER, varsayilanSes: 'Aoede' },
};

const oku = <T,>(p: string, bos: T): T => {
  try {
    return JSON.parse(fs.readFileSync(p, 'utf8'));
  } catch {
    return bos;
  }
};
const yaz = (p: string, v: unknown) => {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  const tmp = `${p}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(v, null, 1));
  fs.renameSync(tmp, p);
};
const simdi = () => new Date().toISOString();
const uyu = (ms: number) => new Promise((r) => setTimeout(r, ms));
const hash = (s: string) => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619);
  return (h >>> 0).toString(16);
};

let yayinla: (olay: string, veri: any) => void = () => {};
const degisti = (neden: string) => yayinla('sesli_anlatim', { neden, at: simdi() });

const kayitlar = () => oku<Record<string, Varyant[]>>(P.kayit, {});
const kuyruk = () => oku<Is[]>(P.kuyruk, []);
const kuyrukYaz = (q: Is[]) => yaz(P.kuyruk, q);
const isGuncelle = (id: string, f: (i: Is) => void) => {
  const q = kuyruk();
  const i = q.find((x) => x.id === id);
  if (i) {
    f(i);
    kuyrukYaz(q);
  }
  return i;
};
const butce = () => oku(P.butce, { tavanTL: BUTCE.tavanTL, kilitTL: BUTCE.kilitTL, harcananTL: 0, kayitlar: [] as any[] });
const ayar = () => ({ isciAktif: true, ucretliAktif: false, ...oku<Record<string, any>>(P.ayar, {}) });

// ---------- metin → parçalar ----------
interface Parca { metin: string; kelime: number; bolumBasi: boolean; ilkParagraf: number }
export interface MetinParagraf { t: string; bolumBasi: boolean; bolumBaslik: string }
/** Konuşma metnini paragraflara ayırır (global sıra = dizin). metniParcala ve canlı ders ucu bunu kullanır. */
export function metinParagraflari(md: string): MetinParagraf[] {
  const satirlar = md.split(/\r?\n/);
  const paragraflar: MetinParagraf[] = [];
  let bolumBasi = true;
  let bolumBaslik = '';
  let tampon: string[] = [];
  const bitir = () => {
    const t = tampon.join(' ').replace(/\s+/g, ' ').trim();
    if (t) {
      paragraflar.push({ t, bolumBasi, bolumBaslik });
      bolumBasi = false;
    }
    tampon = [];
  };
  for (const s of satirlar) {
    if (s.startsWith('# ')) continue;
    if (s.startsWith('@@')) {
      bitir();
      bolumBasi = true;
      bolumBaslik = s.slice(2).trim();
      continue;
    }
    if (!s.trim()) bitir();
    else tampon.push(s.trim());
  }
  bitir();
  return paragraflar;
}
function metniParcala(md: string, sinir: number): Parca[] {
  const paragraflar = metinParagraflari(md);
  const out: Parca[] = [];
  let cur: { t: string[]; bolumBasi: boolean; ilk: number } | null = null;
  const it = (c: { t: string[]; bolumBasi: boolean; ilk: number }) =>
    out.push({ metin: c.t.join('\n'), kelime: c.t.join(' ').split(/\s+/).length, bolumBasi: c.bolumBasi, ilkParagraf: c.ilk });
  for (let idx = 0; idx < paragraflar.length; idx++) {
    const p = paragraflar[idx];
    const uzun = cur ? cur.t.join('\n').length + p.t.length : 0;
    if (!cur || p.bolumBasi || uzun > sinir) {
      if (cur) it(cur);
      cur = { t: [p.t], bolumBasi: p.bolumBasi, ilk: idx };
    } else cur.t.push(p.t);
  }
  if (cur) it(cur);
  // çok küçük bölüm parçalarını bir sonrakiyle birleştirmeden bırak (bölüm araları korunur)
  return out;
}

// ---------- Edge (Emel) ----------
const xml = (s: string) => s.replace(/[<>&"']/g, (c) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&apos;' })[c]!);
async function edgeParagraf(metin: string): Promise<Buffer> {
  // Not: tüketici Edge uç noktası <break> gibi ek SSML etiketlerinde akışı yarıda kesiyor; yalnız düz metin gönderilir.
  const tts = new MsEdgeTTS();
  await tts.setMetadata('tr-TR-EmelNeural', OUTPUT_FORMAT.AUDIO_24KHZ_48KBITRATE_MONO_MP3);
  const { audioStream } = tts.toStream(xml(metin), { rate: EDGE_HIZ });
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    const timer = setTimeout(() => {
      tts.close();
      reject(new Error('Edge zaman aşımı'));
    }, 180000);
    audioStream.on('data', (d: Buffer) => chunks.push(d));
    audioStream.on('end', () => {
      clearTimeout(timer);
      tts.close();
      resolve(Buffer.concat(chunks));
    });
    audioStream.on('error', (e: Error) => {
      clearTimeout(timer);
      tts.close();
      reject(e);
    });
  });
}
const sessizlikCache = new Map<string, Buffer>();
/** Edge çıktısıyla aynı biçimde (24 kHz, 48 kbps, mono) sessiz MP3 kareleri. */
function sessizlik(sn: number, kbps = 48): Buffer {
  const k = `${sn}-${kbps}`;
  if (!sessizlikCache.has(k)) {
    const enc = new Mp3Encoder(1, 24000, kbps);
    const parts = [enc.encodeBuffer(new Int16Array(Math.round(24000 * sn))), enc.flush()];
    sessizlikCache.set(k, Buffer.concat(parts.map((u) => Buffer.from(u))));
  }
  return sessizlikCache.get(k)!;
}
async function edgeParagrafDayanikli(par: string): Promise<Buffer> {
  for (let d = 1; ; d++) {
    try {
      const b = await edgeParagraf(par);
      if (!b.length) throw new Error('Edge boş ses');
      return b;
    } catch (e: any) {
      // 429 (çok istek) ve kopan akışta paragraf düzeyinde bekleyip yeniden dene
      if (d >= 6) throw e;
      await uyu((/429/.test(String(e?.message)) ? 20000 : 4000) * d);
    }
  }
}
const EDGE_ES_ZAMANLI = 3;
/** Parça içi paragraf zamanı: [konuşma başı, konuşma sonu] (sn, parçanın başına göre). */
type ParcaZaman = [number, number][];
async function edgeSentezle(p: Parca): Promise<{ buf: Buffer; zaman: ParcaZaman }> {
  // Paragraflar EDGE_ES_ZAMANLI istekle paralel seslendirilir, sıra korunur.
  const paragraflar = p.metin.split('\n');
  const sonuc: Buffer[] = new Array(paragraflar.length);
  let sira = 0;
  const isci = async () => {
    for (;;) {
      const i = sira++;
      if (i >= paragraflar.length) return;
      sonuc[i] = await edgeParagrafDayanikli(paragraflar[i]);
      await uyu(150);
    }
  };
  await Promise.all(Array.from({ length: Math.min(EDGE_ES_ZAMANLI, paragraflar.length) }, isci));
  const out: Buffer[] = [];
  const zaman: ParcaZaman = [];
  let t = 0; // 48 kbps CBR: süre = bayt*8/48000 (sessizlikler dahil gerçek tampon süreleri)
  if (p.bolumBasi) {
    out.push(sessizlik(0.5));
    t += edgeSure(sessizlik(0.5));
  }
  for (const b of sonuc) {
    const bas = t;
    t += edgeSure(b);
    zaman.push([bas, t]);
    out.push(b, sessizlik(0.7));
    t += edgeSure(sessizlik(0.7));
  }
  return { buf: Buffer.concat(out), zaman };
}
const edgeSure = (b: Buffer) => (b.length * 8) / 48000;

// ---------- Gemini ----------
/** Anahtar geçersiz/yetkisiz (401/403): işten deneme hakkı yemez; anahtar 24 saat devre dışı kalır. */
class AnahtarHatasi extends Error {}
class KotaHatasi extends Error {
  constructor(public bekleMs: number, msg: string) {
    super(msg);
  }
}
const anahtarBekleme = new Map<string, number>(); // ad → bu zamana kadar kullanma
function ucretsizAnahtarlar(): { ad: string; deger: string }[] {
  // Önce seslendirmeye ayrılmış ücretsiz anahtarlar (TTS_FREE_GEMINI_KEY_N), sonra genel ücretsiz havuz
  const ozel = Object.keys(process.env)
    .filter((n) => /^TTS_FREE_GEMINI_KEY_\d+$/.test(n))
    .sort((a, b) => Number(a.slice(20)) - Number(b.slice(20)));
  const adlar = [...ozel, 'GEMINI_API_KEY', ...freeGeminiKeyNames()];
  return adlar.map((ad) => ({ ad, deger: (process.env[ad] || '').trim() })).filter((x) => x.deger);
}
function sonrakiPasifikGeceYarisi(): number {
  // Ücretsiz günlük kota Pasifik gece yarısında yenilenir (07:00/08:00 UTC); 08:10 UTC güvenli.
  const d = new Date();
  const t = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(), 8, 10);
  return t > Date.now() ? t : t + 86400000;
}
function sureOku(s?: string): number {
  const m = /^([\d.]+)s$/.exec(s || '');
  return m ? Math.ceil(parseFloat(m[1]) * 1000) : 0;
}
async function geminiCagir(anahtar: string, sesAdi: string, metin: string): Promise<{ pcm: Buffer; usage: any }> {
  const body = {
    contents: [{ parts: [{ text: STIL + metin }] }],
    generationConfig: {
      responseModalities: ['AUDIO'],
      speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: sesAdi } } },
    },
  };
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 300000);
  try {
    const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': anahtar },
      body: JSON.stringify(body),
      signal: ctrl.signal,
    });
    const j: any = await r.json().catch(() => ({}));
    if (!r.ok) {
      const e = j?.error || {};
      const msg = String(e.message || `HTTP ${r.status}`);
      if (r.status === 429) {
        const det = Array.isArray(e.details) ? e.details : [];
        const gunluk = JSON.stringify(det).includes('PerDay') || /per day|daily|spending cap/i.test(msg);
        const retry = sureOku(det.find((x: any) => x?.retryDelay)?.retryDelay);
        throw new KotaHatasi(gunluk ? sonrakiPasifikGeceYarisi() - Date.now() : Math.max(retry, 20000), msg.slice(0, 200));
      }
      if (r.status >= 500) throw new KotaHatasi(30000, `Gemini ${r.status}: ${msg.slice(0, 160)}`);
      if (r.status === 401 || r.status === 403) throw new AnahtarHatasi(`Gemini ${r.status}: ${msg.slice(0, 160)}`);
      throw new Error(`Gemini ${r.status}: ${msg.slice(0, 200)}`);
    }
    const data = j?.candidates?.[0]?.content?.parts?.find((p: any) => p?.inlineData?.data)?.inlineData?.data;
    if (!data) throw new KotaHatasi(15000, 'Gemini boş ses döndürdü');
    return { pcm: Buffer.from(data, 'base64'), usage: j.usageMetadata || {} };
  } finally {
    clearTimeout(timer);
  }
}
/** Baştaki/sondaki sessizliği kırpar (Gemini kısa parçaların sonuna uzun sessizlik ekleyebiliyor). */
function sessizlikKirp(pcm: Buffer): Buffer {
  const s = new Int16Array(pcm.buffer, pcm.byteOffset, Math.floor(pcm.length / 2));
  const pencere = 480; // 20 ms
  const esik = 600;
  const sesli = (i: number) => {
    let m = 0;
    for (let j = i; j < Math.min(i + pencere, s.length); j++) m = Math.max(m, Math.abs(s[j]));
    return m > esik;
  };
  let bas = 0;
  while (bas < s.length && !sesli(bas)) bas += pencere;
  let son = s.length;
  while (son > bas && !sesli(Math.max(0, son - pencere))) son -= pencere;
  bas = Math.max(0, bas - 3600); // 150 ms pay
  son = Math.min(s.length, son + 4800); // 200 ms pay
  return Buffer.from(pcm.buffer, pcm.byteOffset + bas * 2, (son - bas) * 2);
}
const BIRLER = ['', 'bir', 'iki', 'üç', 'dört', 'beş', 'altı', 'yedi', 'sekiz', 'dokuz'];
const ONLAR = ['', 'on', 'yirmi', 'otuz', 'kırk', 'elli', 'altmış', 'yetmiş', 'seksen', 'doksan'];
/** 0–999.999.999 arası sayıyı Türkçe yazıya çevirir (döküm karşılaştırması için). */
function sayiYazi(n: number): string {
  if (n === 0) return 'sıfır';
  const uc = (x: number) => (x >= 100 ? (x >= 200 ? BIRLER[Math.floor(x / 100)] : '') + 'yüz' : '') + ONLAR[Math.floor((x % 100) / 10)] + BIRLER[x % 10];
  const milyon = Math.floor(n / 1e6), bin = Math.floor((n % 1e6) / 1000), kalan = n % 1000;
  return (milyon ? uc(milyon) + 'milyon' : '') + (bin ? (bin === 1 ? '' : uc(bin)) + 'bin' : '') + uc(kalan);
}
/** Karşılaştırma için katlanmış harf dizisi: yüzde/sayılar yazıya, aksan/boşluk/noktalama atılır.
 *  Böylece "de ne a" ile "DNA", "yüzde otuz" ile "%30" eşleşir. */
const harfDizisi = (t: string) =>
  t
    .replace(/%\s*(\d+)/g, ' yüzde $1 ')
    .replace(/(\d+)[.,](\d+)/g, (_m, a, b) => ` ${a} virgül ${b} `)
    .replace(/\d+/g, (m) => (m.length <= 9 ? ' ' + sayiYazi(Number(m)) + ' ' : ' ' + m + ' '))
    .toLocaleLowerCase('tr-TR')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/ı/g, 'i')
    .replace(/[^a-z]/g, '');
/** Kaynak harflerinin dökümde sırayla bulunma oranı (harf düzeyinde LCS / kaynak uzunluğu). */
function benzerlik(kaynak: string, dokum: string): number {
  const a = harfDizisi(kaynak);
  const b = harfDizisi(dokum);
  if (!a.length) return 1;
  let prev = new Uint16Array(b.length + 1);
  let cur = new Uint16Array(b.length + 1);
  for (let i = 1; i <= a.length; i++) {
    const ca = a.charCodeAt(i - 1);
    for (let j = 1; j <= b.length; j++) cur[j] = ca === b.charCodeAt(j - 1) ? prev[j - 1] + 1 : Math.max(prev[j], cur[j - 1]);
    [prev, cur] = [cur, prev];
  }
  return prev[b.length] / a.length;
}
const DOKUM_MODELLER = ['gemini-3.5-flash-lite', 'gemini-3.1-flash-lite', 'gemini-2.5-flash-lite'];
/** Ücretsiz anahtarla sesi yazıya döker; kota/erişim yoksa null (doğrulanamadı). */
async function dokumAl(pcm: Buffer): Promise<string | null> {
  const wav = Buffer.alloc(44 + pcm.length);
  wav.write('RIFF', 0); wav.writeUInt32LE(36 + pcm.length, 4); wav.write('WAVE', 8); wav.write('fmt ', 12);
  wav.writeUInt32LE(16, 16); wav.writeUInt16LE(1, 20); wav.writeUInt16LE(1, 22); wav.writeUInt32LE(24000, 24);
  wav.writeUInt32LE(48000, 28); wav.writeUInt16LE(2, 32); wav.writeUInt16LE(16, 34); wav.write('data', 36); wav.writeUInt32LE(pcm.length, 40);
  pcm.copy(wav, 44);
  const body = JSON.stringify({
    contents: [{ parts: [{ inlineData: { mimeType: 'audio/wav', data: wav.toString('base64') } }, { text: 'Bu Türkçe ses kaydını baştan sona kelimesi kelimesine yazıya dök. Yalnız dökümü yaz.' }] }],
    generationConfig: { maxOutputTokens: 8000, temperature: 0 },
  });
  for (const model of DOKUM_MODELLER) {
    for (const k of ucretsizAnahtarlar()) {
      const kilit = `dokum:${model}:${k.ad}`;
      if ((anahtarBekleme.get(kilit) || 0) > Date.now()) continue;
      try {
        const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'x-goog-api-key': k.deger },
          body,
          signal: AbortSignal.timeout(120000),
        });
        if (r.status === 429) {
          anahtarBekleme.set(kilit, Date.now() + 10 * 60000);
          continue;
        }
        if (r.status === 404 || r.status === 400) break; // model yok → sonraki model
        if (!r.ok) continue;
        const j: any = await r.json();
        const t = (j?.candidates?.[0]?.content?.parts || []).map((x: any) => x?.text || '').join(' ').trim();
        if (t) return t;
      } catch {
        /* sonraki anahtar */
      }
    }
  }
  return null;
}

function pcmMp3(pcm: Buffer, sessizlikSn: number, onceSessizlikSn: number): Buffer {
  const enc = new Mp3Encoder(1, 24000, 64);
  const out: Uint8Array[] = [];
  const blok = 1152 * 32;
  const isle = (s: Int16Array) => {
    for (let i = 0; i < s.length; i += blok) out.push(enc.encodeBuffer(s.subarray(i, i + blok)));
  };
  if (onceSessizlikSn > 0) isle(new Int16Array(Math.round(24000 * onceSessizlikSn)));
  isle(new Int16Array(pcm.buffer, pcm.byteOffset, Math.floor(pcm.length / 2)));
  if (sessizlikSn > 0) isle(new Int16Array(Math.round(24000 * sessizlikSn)));
  out.push(enc.flush());
  return Buffer.concat(out.map((u) => Buffer.from(u)));
}

// ---------- paragraf zamanlaması ----------
const yuvarla = (x: number, b = 2) => Math.round(x * 10 ** b) / 10 ** b;
/** CBR MP3 süresi (lamejs/Edge çıktısında Xing başlığı yok): bayt*8/(kbps*1000). */
const mp3Sure = (b: Buffer | number, kbps: number) => ((typeof b === 'number' ? b : b.length) * 8) / (kbps * 1000);
interface ParcaMeta { sure?: number; kelime?: number; dogrulama?: number; bayt?: number; paragraf?: number; zaman?: [number, number][] }
/** Konuşma süresini paragraflara karakter uzunluğu oranında dağıtır; [baş, son] parçanın başına göre. */
function karakterOraniyla(paragraflar: string[], bas: number, konusma: number, araSessizlik = 0): ParcaZaman {
  const top = paragraflar.reduce((t, x) => t + x.length, 0) || 1;
  const net = Math.max(0, konusma - araSessizlik * paragraflar.length);
  const out: ParcaZaman = [];
  let t = bas;
  for (const x of paragraflar) {
    const d = (net * x.length) / top;
    out.push([t, t + d]);
    t += d + araSessizlik;
  }
  return out;
}
/** Gemini parçası: [önde sessizlik][pcm: paragraflar karakter oranıyla][sonda sessizlik]; gerçek MP3 süresine ölçeklenir. */
function geminiParcaZamani(paragraflar: string[], once: number, pcmSn: number, sona: number, gercekSn: number): ParcaZaman {
  const nominal = once + pcmSn + sona;
  const k = nominal > 0 && gercekSn > 0 ? gercekSn / nominal : 1;
  return karakterOraniyla(paragraflar, once, pcmSn).map(([a, b]) => [a * k, b * k]);
}
/** Parça metalarından global, bitişik paragraf zamanlaması. Eski (zamansız) metalarda parça süresi karakter oranıyla bölünür. */
function zamanlamaBirlestir(sag: Saglayici, parcalar: Parca[], buflar: Buffer[], metalar: ParcaMeta[]): { zamanlama: [number, number][]; kaynak: string } {
  const kbps = sag === 'edge-emel' ? 48 : 64;
  const baslar: number[] = [];
  let ofset = 0;
  let tahmini = false;
  parcalar.forEach((p, i) => {
    const pars = p.metin.split('\n');
    const dur = mp3Sure(buflar[i], kbps);
    const m = metalar[i] || {};
    let z: ParcaZaman | undefined = Array.isArray(m.zaman) && m.zaman.length === pars.length ? m.zaman : undefined;
    if (!z) {
      tahmini = true;
      z = sag === 'edge-emel'
        ? karakterOraniyla(pars, p.bolumBasi ? 0.5 : 0, dur - (p.bolumBasi ? 0.5 : 0), 0.7)
        : geminiParcaZamani(pars, p.bolumBasi && i > 0 ? 0.6 : 0, Math.max(0, dur - 0.6 - (p.bolumBasi && i > 0 ? 0.6 : 0)), 0.6, dur);
    }
    for (const [a] of z) baslar.push(ofset + a);
    ofset += dur;
  });
  const zamanlama = baslar.map((b, i) => [yuvarla(b), yuvarla(i + 1 < baslar.length ? baslar[i + 1] : ofset)] as [number, number]);
  return { zamanlama, kaynak: tahmini ? 'tahmini' : 'olcum' };
}

// ---------- bütçe ----------
const tlHesapla = (usage: any) => {
  const ses = Number(usage?.candidatesTokenCount || 0);
  const metin = Number(usage?.promptTokenCount || 0);
  return ((ses * BUTCE.sesUsdMilyon + metin * BUTCE.metinUsdMilyon) / 1e6) * BUTCE.usdTry;
};
const parcaTahminiTL = (kelime: number) => tlHesapla({ candidatesTokenCount: (kelime / KELIME_DK) * 60 * 25 * 1.3, promptTokenCount: kelime * 3 });

// ---------- işçi ----------
let calisiyor = false;
const durt = () => [...uyandirilar].forEach((f) => f());

async function isIsle(is: Is) {
  const md = fs.readFileSync(P.metin(is.key), 'utf8');
  const sinir = is.saglayici === 'edge-emel' ? EDGE_PARCA : GEMINI_PARCA;
  const parcalar = metniParcala(md, sinir);
  const dir = P.parcaDir(is.key, is.id);
  fs.mkdirSync(dir, { recursive: true });
  isGuncelle(is.id, (x) => {
    x.durum = 'calisiyor';
    x.basladi = x.basladi || simdi();
    x.ilerleme = { bitti: x.ilerleme?.bitti || 0, toplam: parcalar.length };
    x.sonrakiDeneme = undefined;
  });
  degisti('basladi');
  let sureToplam = 0;
  for (let i = 0; i < parcalar.length; i++) {
    const dosya = path.join(dir, `${String(i).padStart(3, '0')}.mp3`);
    const meta = `${dosya}.json`;
    if (fs.existsSync(dosya) && fs.existsSync(meta)) {
      sureToplam += oku(meta, { sure: 0 }).sure;
      continue;
    }
    const guncel = kuyruk().find((x) => x.id === is.id);
    if (!guncel || guncel.durum === 'iptal') return;
    if (!ayar().isciAktif) throw new KotaHatasi(60000, 'İşçi durduruldu');
    const p = parcalar[i];
    const beklenen = (p.kelime / KELIME_DK) * 60;
    let buf: Buffer | null = null;
    let sure = 0;
    let ucretliYedek = false;
    let dogrulama: number | undefined; // Gemini: döküm benzerliği %, -1 = doğrulanamadı
    let zaman: ParcaZaman | undefined; // parça içi paragraf zamanları (birleştirmede globale çevrilir)
    // Ücretli işte her deneme para yakar: en fazla 2 deneme (yalnız bağlantı/biçim hatasında), ücretsizde 4
    const maxDeneme = is.saglayici === 'gemini-ucretli' ? 2 : 4;
    for (let deneme = 1; deneme <= maxDeneme && !buf; deneme++) {
      try {
        if (is.saglayici === 'edge-emel') {
          const { buf: b, zaman: z } = await edgeSentezle(p);
          sure = edgeSure(b);
          if (sure < beklenen * 0.55 || sure > beklenen * 1.8) throw new Error(`süre tutarsız (${sure.toFixed(0)} sn, beklenen ~${beklenen.toFixed(0)})`);
          buf = b;
          zaman = z;
        } else {
          const ucretli = is.saglayici === 'gemini-ucretli';
          let parcaUcretli = false; // ücretsiz işte tüm ücretsiz anahtarlar doluyken ücretli yedekle üretilen parça
          let anahtar = '';
          let anahtarAdi = '';
          if (ucretli) {
            anahtar = (process.env.TTS_PAID_GEMINI_KEY || '').trim();
            anahtarAdi = 'TTS_PAID_GEMINI_KEY';
            if (!anahtar) throw new Error('TTS_PAID_GEMINI_KEY tanımlı değil');
            if (!ayar().ucretliAktif) throw new KotaHatasi(60000, 'Ücretli üretim panelden kapatıldı; açılınca kaldığı yerden sürer');
            const b0 = butce();
            if (b0.harcananTL + parcaTahminiTL(p.kelime) > BUTCE.kilitTL) {
              isGuncelle(is.id, (x) => {
                x.durum = 'butce-durdu';
                x.hata = `Bütçe kilidi: harcanan ${b0.harcananTL.toFixed(2)} TL, kilit ${BUTCE.kilitTL} TL (tavan ${BUTCE.tavanTL} TL)`;
              });
              degisti('butce');
              return;
            }
          } else {
            const uygun = ucretsizAnahtarlar().filter((k) => (anahtarBekleme.get(k.ad) || 0) <= Date.now());
            if (uygun.length) {
              anahtar = uygun[0].deger;
              anahtarAdi = uygun[0].ad;
            } else {
              // Bütün ücretsiz anahtarlar denendi ve dolu: ücretli üretim açıksa aynı ders ücretli anahtarla sürer, değilse bekler
              const odenen = (process.env.TTS_PAID_GEMINI_KEY || '').trim();
              const b0 = butce();
              if (ayar().ucretliAktif && odenen && b0.harcananTL + parcaTahminiTL(p.kelime) <= BUTCE.kilitTL) {
                anahtar = odenen;
                anahtarAdi = 'TTS_PAID_GEMINI_KEY';
                parcaUcretli = true;
              } else {
                const en = Math.min(...ucretsizAnahtarlar().map((k) => anahtarBekleme.get(k.ad) || Date.now() + 60000));
                throw new KotaHatasi(
                  Math.max(en - Date.now(), 30000),
                  ayar().ucretliAktif ? 'Tüm ücretsiz anahtarlar dolu ve bütçe kilidine ulaşıldı' : 'Tüm ücretsiz anahtarların kotası dolu (ücretli üretim kapalı; kota açılınca aynı ders sürer)',
                );
              }
            }
          }
          try {
            const ham = await geminiCagir(anahtar, is.ses, p.metin);
            const usage = ham.usage;
            const pcm = sessizlikKirp(ham.pcm);
            sure = pcm.length / 48000;
            if (ucretli || parcaUcretli) {
              const tl = tlHesapla(usage);
              const b = butce();
              b.harcananTL = +(b.harcananTL + tl).toFixed(4);
              b.kayitlar.push({ at: simdi(), is: is.id, key: is.key, parca: i, ses: usage?.candidatesTokenCount, metin: usage?.promptTokenCount, tl: +tl.toFixed(4) });
              yaz(P.butce, b);
              isGuncelle(is.id, (x) => (x.maliyetTL = +((x.maliyetTL || 0) + tl).toFixed(4)));
            }
            const parali = ucretli || parcaUcretli;
            // Ücretli parçada yalnız açıkça bozuk çıktı (çok kısa/uzun) yeniden denenir; ücretsizde dar aralık
            if (parali ? sure < beklenen * 0.35 || sure > beklenen * 3 : sure < beklenen * 0.5 || sure > beklenen * 2)
              throw new Error(`süre tutarsız (${sure.toFixed(0)} sn, beklenen ~${beklenen.toFixed(0)})`);
            const dokum = await dokumAl(pcm);
            if (dokum !== null) {
              const oran = benzerlik(p.metin, dokum);
              dogrulama = Math.round(oran * 100);
              // Ücretsizde düşük benzerlik yeniden üretilir; ücretli parçada para yakmamak için ses tutulur, not düşülür
              if (oran < 0.85 && !parali) throw new Error(`döküm uyuşmuyor (%${dogrulama})`);
              if (oran < 0.85) isGuncelle(is.id, (x) => (x.notlar = [...(x.notlar || []).slice(-9), `parça ${i + 1}: döküm benzerliği %${dogrulama} (ücretli; yeniden üretilmedi)`]));
            } else dogrulama = -1;
            const once = p.bolumBasi && i > 0 ? 0.6 : 0;
            buf = pcmMp3(pcm, 0.6, once);
            ucretliYedek = parcaUcretli;
            zaman = geminiParcaZamani(p.metin.split('\n'), once, sure, 0.6, mp3Sure(buf, 64));
            sure += 0.6 + once;
          } catch (e) {
            if (e instanceof AnahtarHatasi && !ucretli && !parcaUcretli) {
              anahtarBekleme.set(anahtarAdi, Date.now() + 24 * 3600000);
              deneme--;
              if (ucretsizAnahtarlar().every((k) => (anahtarBekleme.get(k.ad) || 0) > Date.now()))
                throw new KotaHatasi(30 * 60000, 'Ücretsiz anahtarların hepsi kota bekliyor ya da geçersiz');
              continue;
            }
            if (e instanceof KotaHatasi && !ucretli && !parcaUcretli) {
              anahtarBekleme.set(anahtarAdi, Date.now() + e.bekleMs);
              deneme--; // başka anahtarla aynı denemeyi sürdür
              if (ucretsizAnahtarlar().every((k) => (anahtarBekleme.get(k.ad) || 0) > Date.now())) throw e;
              continue;
            }
            throw e;
          }
        }
      } catch (e: any) {
        if (e instanceof KotaHatasi) throw e;
        if (e instanceof AnahtarHatasi && is.saglayici === 'gemini-ucretli') throw new Error(`Ücretli anahtar reddedildi: ${e.message}`);
        if (deneme >= maxDeneme) throw new Error(`Parça ${i + 1}/${parcalar.length}: ${e?.message || e}`);
        isGuncelle(is.id, (x) => (x.notlar = [...(x.notlar || []).slice(-9), `parça ${i + 1} deneme ${deneme}: ${e?.message || e}`]));
        await uyu(4000 * deneme);
      }
    }
    fs.writeFileSync(dosya, buf!);
    fs.writeFileSync(meta, JSON.stringify({ sure, kelime: p.kelime, dogrulama, ucretliYedek, bayt: buf!.length, paragraf: p.metin.split('\n').length, zaman: zaman?.map(([a, b]) => [yuvarla(a, 3), yuvarla(b, 3)]) }));
    sureToplam += sure;
    isGuncelle(is.id, (x) => (x.ilerleme = { bitti: i + 1, toplam: parcalar.length }));
    degisti('ilerleme');
    if (is.saglayici === 'gemini-ucretsiz') await uyu(2500);
  }
  // birleştir
  const vid = `${is.saglayici}-${is.ses.toLowerCase()}-${Date.now().toString(36)}`;
  const hedef = P.ses(is.key, vid);
  const parts = parcalar.map((_, i) => fs.readFileSync(path.join(dir, `${String(i).padStart(3, '0')}.mp3`)));
  const metalar = parcalar.map((_, i) => oku<{ dogrulama?: number; ucretliYedek?: boolean }>(path.join(dir, `${String(i).padStart(3, '0')}.mp3.json`), {}));
  const yedekParca = metalar.filter((m) => m.ucretliYedek).length;
  const dogrulanan = metalar.filter((m) => typeof m.dogrulama === 'number' && m.dogrulama >= 0);
  const dogrulamaOzet = is.saglayici === 'edge-emel' ? undefined : {
    parca: dogrulanan.length,
    toplam: parcalar.length,
    ortalama: dogrulanan.length ? Math.round(dogrulanan.reduce((t, m) => t + (m.dogrulama || 0), 0) / dogrulanan.length) : null,
  };
  const tum = Buffer.concat(parts);
  fs.writeFileSync(hedef, tum);
  const zz = zamanlamaBirlestir(is.saglayici, parcalar, parts, parcalar.map((_, i) => oku<ParcaMeta>(path.join(dir, `${String(i).padStart(3, '0')}.mp3.json`), {})));
  const s = SAGLAYICILAR[is.saglayici];
  const v: Varyant = {
    id: vid,
    saglayici: is.saglayici,
    ses: is.ses,
    model: is.saglayici === 'edge-emel' ? 'tr-TR-EmelNeural' : GEMINI_MODEL,
    etiket: `${s.etiket}${is.saglayici === 'edge-emel' ? '' : ` · ${is.ses}`}${yedekParca ? ` · ${yedekParca}/${parcalar.length} parça ücretli yedekle` : ''}`,
    ucretli: s.ucretli,
    sureSn: Math.round(sureToplam),
    bayt: tum.length,
    parca: parcalar.length,
    metinHash: hash(md),
    olusturuldu: simdi(),
    maliyetTL: kuyruk().find((x) => x.id === is.id)?.maliyetTL,
    dogrulama: dogrulamaOzet,
    zamanlama: zz.zamanlama,
    zamanlamaKaynak: zz.kaynak,
  };
  const k = kayitlar();
  const liste = (k[is.key] = k[is.key] || []);
  if (is.varsayilanYap || !liste.length) liste.unshift(v);
  else liste.push(v);
  yaz(P.kayit, k);
  fs.rmSync(dir, { recursive: true, force: true });
  isGuncelle(is.id, (x) => {
    x.durum = 'bitti';
    x.bitti = simdi();
    x.hata = undefined;
  });
  degisti('bitti');
}

type Serit = 'edge' | 'gemini' | 'ucretli';
const seritSaglayici = (x: Is): Serit => (x.saglayici === 'edge-emel' ? 'edge' : x.saglayici === 'gemini-ucretli' ? 'ucretli' : 'gemini');
const uyandirilar = new Set<() => void>();

/** Bir şerit: Edge (Emel), ücretsiz Gemini ve ücretli Gemini ayrı servis/anahtar kullandığından üç şerit paralel çalışır;
 *  her şerit kendi içinde tek tek. Ücretli işler hiçbir ücretsiz işi beklemez. */
async function seritDongusu(serit: Serit) {
  for (;;) {
    let bekle = 60000;
    try {
      if (ayar().isciAktif) {
        const q = kuyruk();
        const an = Date.now();
        const sirada = q.filter(
          (x) =>
            seritSaglayici(x) === serit &&
            (x.durum === 'bekliyor' || x.durum === 'kota-bekliyor') &&
            (!x.sonrakiDeneme || Date.parse(x.sonrakiDeneme) <= an) &&
            fs.existsSync(P.metin(x.key)) &&
            (x.saglayici !== 'gemini-ucretli' || ayar().ucretliAktif),
        );
        // Ücretsiz Aoede alternatifleri ders sırasıyla ve TEK TEK: başlamış (kota bekleyen / yarım) bir ücretsiz iş
        // bitmeden sıradaki derse geçilmez.
        let adaylar = sirada;
        if (serit === 'gemini') {
          const yarim = q.find(
            (x) =>
              x.saglayici === 'gemini-ucretsiz' &&
              (x.durum === 'calisiyor' || x.durum === 'kota-bekliyor' || (x.durum === 'bekliyor' && (x.ilerleme?.bitti || 0) > 0)),
          );
          if (yarim) adaylar = sirada.filter((x) => x.id === yarim.id);
        }
        const is = adaylar[0];
        if (is) {
          try {
            await isIsle(is);
          } catch (e: any) {
            if (e instanceof KotaHatasi) {
              isGuncelle(is.id, (x) => {
                x.durum = 'kota-bekliyor';
                x.sonrakiDeneme = new Date(Date.now() + e.bekleMs).toISOString();
                x.hata = e.message;
              });
            } else {
              isGuncelle(is.id, (x) => {
                x.durum = 'hata';
                x.hata = String(e?.message || e).slice(0, 400);
              });
            }
            degisti('hata');
          }
          bekle = 500;
        } else {
          const sonraki = q
            .filter((x) => seritSaglayici(x) === serit && x.durum === 'kota-bekliyor' && x.sonrakiDeneme)
            .map((x) => Date.parse(x.sonrakiDeneme!) - an);
          if (sonraki.length) bekle = Math.max(5000, Math.min(...sonraki, 600000));
        }
      }
    } catch (e) {
      console.error(`[sesli-anlatim] ${serit} şeridi hatası`, e);
    }
    await new Promise<void>((r) => {
      const t = setTimeout(done, bekle);
      function done() {
        clearTimeout(t);
        uyandirilar.delete(done);
        r();
      }
      uyandirilar.add(done);
    });
  }
}

async function isciDongusu() {
  if (calisiyor) return;
  calisiyor = true;
  // yeniden açılışta yarım kalan işler sıraya döner (parçalar diskte durur)
  const q0 = kuyruk();
  q0.forEach((x) => x.durum === 'calisiyor' && (x.durum = 'bekliyor'));
  kuyrukYaz(q0);
  void seritDongusu('edge');
  void seritDongusu('gemini');
  void seritDongusu('ucretli');
}

export function isEkle(key: string, saglayici: Saglayici, ses: string, opts: { varsayilanYap?: boolean; isteyen?: string; one?: boolean } = {}) {
  const q = kuyruk();
  const ayni = q.find((x) => x.key === key && x.saglayici === saglayici && x.ses === ses && ['bekliyor', 'calisiyor', 'kota-bekliyor'].includes(x.durum));
  if (ayni) return ayni;
  const is: Is = {
    id: `is-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`,
    key,
    saglayici,
    ses,
    durum: 'bekliyor',
    varsayilanYap: !!opts.varsayilanYap,
    ilerleme: { bitti: 0, toplam: 0 },
    olusturuldu: simdi(),
    isteyen: opts.isteyen,
  };
  if (opts.one) {
    const ilkBekleyen = q.findIndex((x) => x.durum === 'bekliyor' || x.durum === 'kota-bekliyor');
    q.splice(ilkBekleyen < 0 ? q.length : ilkBekleyen, 0, is);
  } else q.push(is);
  kuyrukYaz(q);
  degisti('ekle');
  durt();
  return is;
}

function durum() {
  const dersler = oku<Ders[]>(P.dersler, []);
  const k = kayitlar();
  const q = kuyruk();
  const b = butce();
  return {
    dersler: dersler.map((d) => {
      const metinVar = fs.existsSync(P.metin(d.key));
      let kelime = 0;
      let bolum = 0;
      let hashNow = '';
      if (metinVar) {
        const md = fs.readFileSync(P.metin(d.key), 'utf8');
        kelime = md.split('\n').filter((l) => !l.startsWith('#') && !l.startsWith('@@')).join(' ').split(/\s+/).filter(Boolean).length;
        bolum = (md.match(/^@@ /gm) || []).length;
        hashNow = hash(md);
      }
      return {
        ...d,
        metin: metinVar,
        kelime,
        bolum,
        tahminiDk: Math.round(kelime / KELIME_DK),
        varyantlar: (k[d.key] || []).map((v) => ({ ...v, metinGuncel: v.metinHash === hashNow })),
        isler: q.filter((x) => x.key === d.key && !['bitti', 'iptal'].includes(x.durum)),
      };
    }),
    kuyruk: q.slice(-400),
    butce: { tavanTL: BUTCE.tavanTL, kilitTL: BUTCE.kilitTL, harcananTL: +b.harcananTL.toFixed(2), kalanTL: +(BUTCE.kilitTL - b.harcananTL).toFixed(2), varsayim: `${BUTCE.sesUsdMilyon} $/1M ses tokenı (gerçek 9 $), 1 $ = ${BUTCE.usdTry} TL — temkinli`, anahtarVar: !!process.env.TTS_PAID_GEMINI_KEY },
    saglayicilar: Object.entries(SAGLAYICILAR).map(([id, s]) => ({ id, ...s })),
    ucretsizAnahtar: ucretsizAnahtarlar().map((x) => ({ ad: x.ad, bekliyorKadar: anahtarBekleme.get(x.ad) && anahtarBekleme.get(x.ad)! > Date.now() ? new Date(anahtarBekleme.get(x.ad)!).toISOString() : null })),
    isci: { aktif: ayar().isciAktif !== false, calisiyor },
    ucretliAktif: !!ayar().ucretliAktif,
  };
}

function guvenliAnahtar(k: string) {
  return /^k1-\d+-[a-z0-9-]+$/.test(k) ? k : null;
}

export function registerSesliAnlatimRoutes(
  app: Express,
  requireAdmin: (req: Request, res: Response, next: NextFunction) => void,
  broadcast: (event: string, data: any) => void,
  adminEmail: string,
) {
  // Okuma uçları genel yönetici denetimiyle; üretim/silme/kuyruk eylemleri (özellikle ücretli anahtar) yalnız
  // doğrulanmış yöneticiyle: loopback, Firebase yönetici jetonu ya da MEDS_PANEL_SECRET (başlık e-postasına güvenilmez).
  const guclu = async (req: Request, res: Response, next: NextFunction) => {
    if (await isStrongAdmin(req, adminEmail)) return next();
    res.status(403).json({ error: 'Bu işlem için yönetici hesabıyla giriş yapmış olmalısın.' });
  };
  yayinla = broadcast;
  fs.mkdirSync(KOK, { recursive: true });

  app.get('/api/sesli-anlatim', requireAdmin, (_req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    res.json(durum());
  });

  app.get('/api/sesli-anlatim/metin/:key', requireAdmin, (req, res) => {
    const k = guvenliAnahtar(req.params.key);
    if (!k || !fs.existsSync(P.metin(k))) return res.status(404).json({ error: 'metin yok' });
    res.json({ metin: fs.readFileSync(P.metin(k), 'utf8') });
  });

  app.get('/api/sesli-anlatim/ses/:key/:vid', requireAdmin, (req, res) => {
    const k = guvenliAnahtar(req.params.key);
    const vid = String(req.params.vid).replace(/\.mp3$/, '');
    if (!k || !/^[a-z0-9-]+$/.test(vid)) return res.status(400).end();
    const f = P.ses(k, vid);
    if (!fs.existsSync(f)) return res.status(404).end();
    const st = fs.statSync(f);
    const d = oku<Ders[]>(P.dersler, []).find((x) => x.key === k);
    const v = (kayitlar()[k] || []).find((x) => x.id === vid);
    if (req.query.indir) {
      const ad = `${String(d?.no ?? '').padStart(2, '0')} - ${d?.baslik || k} - ${v?.etiket || vid}.mp3`.replace(/[\\/:*?"<>|]/g, '-');
      res.setHeader('Content-Disposition', `attachment; filename="${encodeURIComponent(ad)}"; filename*=UTF-8''${encodeURIComponent(ad)}`);
    }
    res.setHeader('Content-Type', 'audio/mpeg');
    res.setHeader('Accept-Ranges', 'bytes');
    res.setHeader('Cache-Control', 'private, max-age=86400');
    const range = /bytes=(\d*)-(\d*)/.exec(String(req.headers.range || ''));
    if (range && !req.query.indir) {
      const bas = range[1] ? parseInt(range[1], 10) : 0;
      const son = range[2] ? Math.min(parseInt(range[2], 10), st.size - 1) : st.size - 1;
      if (bas >= st.size || bas > son) return res.status(416).setHeader('Content-Range', `bytes */${st.size}`).end();
      res.status(206);
      res.setHeader('Content-Range', `bytes ${bas}-${son}/${st.size}`);
      res.setHeader('Content-Length', String(son - bas + 1));
      return fs.createReadStream(f, { start: bas, end: son }).pipe(res);
    }
    res.setHeader('Content-Length', String(st.size));
    fs.createReadStream(f).pipe(res);
  });

  app.post('/api/sesli-anlatim/uret', requireAdmin, guclu, (req, res) => {
    const k = guvenliAnahtar(String(req.body?.key || ''));
    const sag = String(req.body?.saglayici || '') as Saglayici;
    const s = SAGLAYICILAR[sag];
    if (!k || !s) return res.status(400).json({ error: 'ders ya da sağlayıcı geçersiz' });
    if (!fs.existsSync(P.metin(k))) return res.status(400).json({ error: 'Bu dersin konuşma metni henüz yok' });
    const ses = s.sesler.includes(String(req.body?.ses)) ? String(req.body.ses) : s.varsayilanSes;
    if (s.ucretli) {
      if (!ayar().ucretliAktif) return res.status(400).json({ error: 'Ücretli üretim kapalı. Önce panelden "Ücretli üretim" anahtarını aç.' });
      if (!process.env.TTS_PAID_GEMINI_KEY) return res.status(400).json({ error: 'Ücretli anahtar sunucuda tanımlı değil' });
      const md = fs.readFileSync(P.metin(k), 'utf8');
      const tahmin = metniParcala(md, GEMINI_PARCA).reduce((t, p) => t + parcaTahminiTL(p.kelime), 0);
      const b = butce();
      const bekleyen = kuyruk()
        .filter((x) => x.saglayici === 'gemini-ucretli' && ['bekliyor', 'calisiyor', 'kota-bekliyor'].includes(x.durum))
        .reduce((t, x) => t + metniParcala(fs.readFileSync(P.metin(x.key), 'utf8'), GEMINI_PARCA).reduce((a, p) => a + parcaTahminiTL(p.kelime), 0), 0);
      if (b.harcananTL + bekleyen + tahmin > BUTCE.kilitTL)
        return res.status(402).json({ error: `Bütçe yetmez: harcanan ${b.harcananTL.toFixed(2)} TL + sıradaki ${bekleyen.toFixed(2)} TL + bu ders ~${tahmin.toFixed(2)} TL > kilit ${BUTCE.kilitTL} TL` });
    }
    const is = isEkle(k, sag, ses, { isteyen: String(req.headers['x-admin-email'] || 'panel'), one: !!req.body?.one });
    res.json({ ok: true, is });
  });

  app.post('/api/sesli-anlatim/kuyruk/:id/:eylem', requireAdmin, guclu, (req, res) => {
    const { id, eylem } = req.params;
    const q = kuyruk();
    const i = q.findIndex((x) => x.id === id);
    if (i < 0) return res.status(404).json({ error: 'iş yok' });
    const is = q[i];
    if (eylem === 'iptal') {
      if (['bitti'].includes(is.durum)) return res.status(400).json({ error: 'bitmiş iş' });
      is.durum = 'iptal';
      fs.rmSync(P.parcaDir(is.key, is.id), { recursive: true, force: true });
    } else if (eylem === 'yeniden') {
      if (!['hata', 'iptal', 'butce-durdu', 'kota-bekliyor'].includes(is.durum)) return res.status(400).json({ error: 'yeniden denenemez' });
      is.durum = 'bekliyor';
      is.hata = undefined;
      is.sonrakiDeneme = undefined;
    } else if (eylem === 'one-al') {
      q.splice(i, 1);
      const ilk = q.findIndex((x) => x.durum === 'bekliyor' || x.durum === 'kota-bekliyor');
      q.splice(ilk < 0 ? q.length : ilk, 0, is);
    } else return res.status(400).json({ error: 'eylem geçersiz' });
    kuyrukYaz(q);
    degisti(eylem);
    durt();
    res.json({ ok: true });
  });

  app.post('/api/sesli-anlatim/varsayilan', requireAdmin, guclu, (req, res) => {
    const k = guvenliAnahtar(String(req.body?.key || ''));
    const kayit = kayitlar();
    const liste = k ? kayit[k] || [] : [];
    const i = liste.findIndex((v) => v.id === req.body?.vid);
    if (i < 0) return res.status(404).json({ error: 'varyant yok' });
    liste.unshift(...liste.splice(i, 1));
    yaz(P.kayit, kayit);
    degisti('varsayilan');
    res.json({ ok: true });
  });

  app.delete('/api/sesli-anlatim/ses/:key/:vid', requireAdmin, guclu, (req, res) => {
    const k = guvenliAnahtar(req.params.key);
    const kayit = kayitlar();
    const liste = k ? kayit[k] || [] : [];
    const i = liste.findIndex((v) => v.id === req.params.vid);
    if (i < 0) return res.status(404).json({ error: 'varyant yok' });
    if (i === 0 && liste.length > 1) return res.status(400).json({ error: 'Önce başka bir sesi varsayılan yap' });
    const [v] = liste.splice(i, 1);
    fs.rmSync(P.ses(k!, v.id), { force: true });
    yaz(P.kayit, kayit);
    degisti('sil');
    res.json({ ok: true });
  });

  app.post('/api/sesli-anlatim/ucretli', requireAdmin, guclu, (req, res) => {
    yaz(P.ayar, { ...ayar(), ucretliAktif: !!req.body?.aktif });
    if (req.body?.aktif) {
      const q = kuyruk();
      q.forEach((x) => x.saglayici === 'gemini-ucretsiz' && x.durum === 'kota-bekliyor' && delete x.sonrakiDeneme);
      kuyrukYaz(q);
    }
    degisti('ucretli');
    durt();
    res.json({ ok: true });
  });

  app.post('/api/sesli-anlatim/isci', requireAdmin, guclu, (req, res) => {
    yaz(P.ayar, { ...ayar(), isciAktif: !!req.body?.aktif });
    degisti('isci');
    durt();
    res.json({ ok: true });
  });

  setTimeout(() => void isciDongusu(), 15000);
}
