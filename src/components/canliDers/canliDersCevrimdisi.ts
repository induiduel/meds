/**
 * Canlı ders · çevrimdışı paket. Bir dersin seçili sesi (MP3), konuşma metni + zamanlama + PDF hizalaması (ayrıntı
 * JSON'u), ders PDF'leri ve PDF.js yardımcı dosyaları cihazdaki `medsoru-canli-ders-offline` önbelleğine yazılır.
 *  - Ses: sw.js bu önbellekteki MP3'ü Range/206 ile verir (aynı adres; internet yokken de sarma/atlama çalışır).
 *  - Ayrıntı/liste/PDF eşlemesi: istek sw.js'te ağdan alınamazsa tüm önbelleklerde aranır; ayrıca store ağ hatasında
 *    buradaki kopyaya düşer (SW yoksa da). Ders PDF'i aynı akış adresiyle saklanır (pdf.js tam yanıtı okur).
 *  - Saklama: kurul boyunca kalır; kurul sınavından 3 gün sonra silinebilir — kendiliğinden SİLİNMEZ, bildirim düşülür
 *    ve kullanıcıya sorulur (CanliDersCevrimdisiSoru). Kayıt defteri localStorage'da (`KAYIT_KEY`).
 */
import { useSyncExternalStore } from 'react';
import { getCustomApiUrl } from '../../services/api';
import { resolveDeckPdf } from '../../services/deckPdfService';
import { OFFICIAL_CURRICULUM_COMMITTEES } from '../../data/curriculumData';
import { cdDetayGetir, cdSesUrl, type CdDetay, type CdListeDers, type CdVaryant } from './canliDersStore';
import { CD_CEVRIMDISI_DEGISTI, cdCevrimdisiKayitlari, cdCevrimdisiYaz, type CdCevrimdisiKayit } from './canliDersCevrimdisiKayit';

export const CD_OFFLINE_CACHE = 'medsoru-canli-ders-offline';
const VARYANT_KEY = 'medsoru_canli_ders_ses';
const SILME_GECIKME_GUN = 3;

const mutlak = (p: string) => new URL(`${(getCustomApiUrl(p) || '').replace(/\/$/, '')}${p}`, location.href).href;
/** SW'nin ses isteğini tanıdığı anahtar: sürüm sorgusu olmadan yol */
const sesAnahtari = (key: string, vid: string) => mutlak(`/api/canli-ders/ses/${encodeURIComponent(key)}/${encodeURIComponent(vid)}.mp3`);
const detayAdresi = (key: string) => mutlak(`/api/canli-ders/${encodeURIComponent(key)}`);
const listeAdresi = () => mutlak('/api/canli-ders');
const deckAdresi = (deckId: string) => mutlak(`/api/lecture-pdf/deck/${encodeURIComponent(deckId)}`);
/** SW'den bağımsız yedek kopyalar (store ağ hatasında okur) */
const yedekDetay = (key: string) => mutlak(`/__cd-cevrimdisi/detay/${encodeURIComponent(key)}`);
const yedekListe = (key: string) => mutlak(`/__cd-cevrimdisi/liste/${encodeURIComponent(key)}`);

export const cdCevrimdisiDestek = () => typeof caches !== 'undefined' && typeof fetch !== 'undefined';

/* ---------------- kurul süresi ---------------- */
const AYLAR = ['ocak', 'şubat', 'mart', 'nisan', 'mayıs', 'haziran', 'temmuz', 'ağustos', 'eylül', 'ekim', 'kasım', 'aralık'];
function trTarih(s: string): Date | null {
  const m = s.trim().toLocaleLowerCase('tr').match(/^(\d{1,2})\s+(\S+)\s+(\d{4})$/);
  if (!m) return null;
  const ay = AYLAR.indexOf(m[2]);
  return ay < 0 ? null : new Date(Number(m[3]), ay, Number(m[1]));
}
/** Dersin kurulu (anahtar `k<n>-…`) ve kurul sınavından 3 gün sonrası (ms). Tarih bilinmiyorsa null: hiç sorulmaz. */
export function cdKurulBilgisi(key: string): { kurul: number; sinav: string; silinebilir: number } | null {
  const n = Number(key.match(/^k(\d+)-/)?.[1]);
  const c = OFFICIAL_CURRICULUM_COMMITTEES.find((x) => x.id === `donem3-kurul${n}`);
  const d = c && trTarih(c.examDate);
  if (!d) return null;
  return { kurul: n, sinav: c!.examDate, silinebilir: d.getTime() + SILME_GECIKME_GUN * 86_400_000 };
}

/* ---------------- süren indirmeler ---------------- */
export interface CdIndirme { oran: number; hata?: string }
let isler: Record<string, CdIndirme> = {};
const iptaller = new Map<string, AbortController>();
const subs = new Set<() => void>();
const yay = () => subs.forEach((f) => f());
const isYaz = (key: string, v: CdIndirme | null) => {
  const n = { ...isler };
  if (v) n[key] = v;
  else delete n[key];
  isler = n;
  yay();
};
let kayitAnlik = cdCevrimdisiKayitlari();
if (typeof window !== 'undefined') {
  window.addEventListener(CD_CEVRIMDISI_DEGISTI, () => { kayitAnlik = cdCevrimdisiKayitlari(); yay(); });
}
const abone = (f: () => void) => { subs.add(f); return () => subs.delete(f); };
export function useCdCevrimdisi(key: string): { kayit: CdCevrimdisiKayit | null; is: CdIndirme | null } {
  const kayit = useSyncExternalStore(abone, () => kayitAnlik[key] || null, () => null);
  const is = useSyncExternalStore(abone, () => isler[key] || null, () => null);
  return { kayit, is };
}
export const useCdCevrimdisiSayi = () => useSyncExternalStore(abone, () => Object.keys(kayitAnlik).length, () => 0);

/* ---------------- indirme ---------------- */
function swBildir() {
  try { navigator.serviceWorker?.controller?.postMessage({ type: 'CD_OFFLINE_CHANGED' }); } catch { /* yok */ }
}

/** Yanıt gövdesini ilerlemeyle okur */
async function govdeOku(res: Response, ilerle: (n: number) => void): Promise<Blob> {
  if (!res.body) {
    const b = await res.blob();
    ilerle(b.size);
    return b;
  }
  const r = res.body.getReader();
  const parcalar: BlobPart[] = [];
  for (;;) {
    const { done, value } = await r.read();
    if (done) break;
    parcalar.push(value as Uint8Array<ArrayBuffer>);
    ilerle(value.byteLength);
  }
  return new Blob(parcalar);
}

const tercihVid = (vs: CdVaryant[], caliyor?: string | null) => {
  if (caliyor && vs.some((v) => v.id === caliyor)) return caliyor;
  try {
    const want = localStorage.getItem(VARYANT_KEY);
    const v = want && vs.find((x) => x.etiket === want || x.id === want);
    if (v) return v.id;
  } catch { /* yok */ }
  return vs[0]?.id;
};

let yardimciP: Promise<void> | null = null;
/**
 * PDF.js yardımcı dosyaları (çevrimdışı önbelleğe) + canlı ders ekranının kod parçaları (SW çalışma önbelleğine).
 * Uygulama güncellenince parça adları değişir: kapı (CanliDersDockGate) cihazda ders varsa her çevrimiçi açılışta çağırır.
 */
export function cdCevrimdisiOnIsit(): Promise<void> {
  if (!cdCevrimdisiDestek()) return Promise.resolve();
  if (!yardimciP) {
    const base = `${(getCustomApiUrl() || '').replace(/\/$/, '')}/vendor/pdfjs/`;
    const dosyalar = [
      ...['FoxitDingbats.pfb', 'FoxitFixed.pfb', 'FoxitFixedBold.pfb', 'FoxitFixedBoldItalic.pfb', 'FoxitFixedItalic.pfb', 'FoxitSerif.pfb',
        'FoxitSerifBold.pfb', 'FoxitSerifBoldItalic.pfb', 'FoxitSerifItalic.pfb', 'FoxitSymbol.pfb', 'LiberationSans-Bold.ttf',
        'LiberationSans-BoldItalic.ttf', 'LiberationSans-Italic.ttf', 'LiberationSans-Regular.ttf'].map((f) => `standard_fonts/${f}`),
      'wasm/openjpeg.wasm', 'wasm/openjpeg_nowasm_fallback.js', 'wasm/qcms_bg.wasm', 'iccs/CGATS001Compat-v2-micro.icc',
    ];
    yardimciP = caches.open(CD_OFFLINE_CACHE).then((cache) => Promise.all([
      ...dosyalar.map(async (f) => {
        const u = new URL(base + f, location.href).href;
        if (await cache.match(u)) return;
        const r = await fetch(u);
        if (r.ok) await cache.put(u, r);
      }),
      // Liste/ders ekranı, oynatıcı, tanıtım ve PDF görüntüleyici parçaları (içerik özetli /assets/ dosyaları SW önbelleğine girer)
      import('./CanliDersView'),
      import('./CanliDersDock'),
      import('./CanliDersTur'),
      import('../learn/pdf/PdfDocView'),
      import('pdfjs-dist/build/pdf.worker.min.mjs?url').then((m) => fetch((m as any).default)),
    ])).then(() => undefined, () => { yardimciP = null; });
  }
  return yardimciP;
}

/** Dersi cihaza indirir (ses + metin + PDF). Aynı ders için ikinci çağrı mevcut işi bekletmez, yok sayılır. */
export async function cdCevrimdisiIndir(key: string, opts: { caliyorVid?: string | null } = {}): Promise<void> {
  if (!cdCevrimdisiDestek()) throw new Error('Bu tarayıcı çevrimdışı saklamayı desteklemiyor.');
  if (iptaller.has(key)) return;
  const ac = new AbortController();
  iptaller.set(key, ac);
  isYaz(key, { oran: 0 });
  try {
    // Kurul boyunca tarayıcının alan açmak için silmemesi istenir (izin verilmezse yine de çalışır)
    void navigator.storage?.persist?.().catch(() => false);
    const detay: CdDetay = await cdDetayGetir(key, true);
    const vid = tercihVid(detay.varyantlar, opts.caliyorVid);
    const v = detay.varyantlar.find((x) => x.id === vid);
    if (!v) throw new Error('Bu dersin sesi yok.');
    const cache = await caches.open(CD_OFFLINE_CACHE);

    // PDF dosyaları (sunucuda olanlar)
    const pdfAdres: { url: string; bayt: number }[] = [];
    let deckJson: unknown = null;
    if (detay.pdf?.deckId) {
      const r = await fetch(deckAdresi(detay.pdf.deckId), { cache: 'no-store', signal: ac.signal }).catch(() => null);
      if (r?.ok) deckJson = await r.json();
      const info = await resolveDeckPdf(detay.pdf.deckId);
      for (const f of info.files) if (f.url) pdfAdres.push({ url: new URL(f.url, location.href).href, bayt: f.size || 0 });
    }
    const toplam = Math.max(1, (v.bayt || 0) + pdfAdres.reduce((a, p) => a + p.bayt, 0));
    let alinan = 0;
    let sonYay = 0;
    const ilerle = (n: number) => {
      alinan += n;
      const t = Date.now();
      if (t - sonYay > 150) { sonYay = t; isYaz(key, { oran: Math.min(0.99, alinan / toplam) }); }
    };

    // Ses
    const sr = await fetch(cdSesUrl(key, vid!), { cache: 'no-store', signal: ac.signal });
    if (!sr.ok) throw new Error(`Ses indirilemedi (${sr.status}).`);
    const ses = await govdeOku(sr, ilerle);
    // PDF'ler
    const pdfler: { url: string; blob: Blob }[] = [];
    for (const p of pdfAdres) {
      const r = await fetch(p.url, { cache: 'no-store', signal: ac.signal });
      if (!r.ok) throw new Error(`PDF indirilemedi (${r.status}).`);
      pdfler.push({ url: p.url, blob: await govdeOku(r, ilerle) });
    }
    await cdCevrimdisiOnIsit();

    // Yalnız indirilen ses varyantıyla ayrıntı: internet yokken oynatıcı başka (indirilmemiş) sese geçmesin
    const yerelDetay: CdDetay = { ...detay, varyantlar: [v] };
    const json = (o: unknown) => new Response(JSON.stringify(o), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    await cache.put(sesAnahtari(key, vid!), new Response(ses, {
      headers: { 'Content-Type': 'audio/mpeg', 'Content-Length': String(ses.size), 'Accept-Ranges': 'bytes', 'X-Cd-Surum': String((v as any).surum || v.bayt || '') },
    }));
    for (const p of pdfler) {
      await cache.put(p.url, new Response(p.blob, { headers: { 'Content-Type': 'application/pdf', 'Content-Length': String(p.blob.size) } }));
    }
    await cache.put(detayAdresi(key), json(detay));
    await cache.put(yedekDetay(key), json(yerelDetay));
    if (deckJson && detay.pdf?.deckId) await cache.put(deckAdresi(detay.pdf.deckId), json(deckJson));
    const listeSatiri: CdListeDers = {
      key, no: detay.no, baslik: detay.baslik, sira: Number(detay.no) || 0, varsayilan: v, varyantlar: [v], pdf: !!detay.pdf,
    };
    await cache.put(yedekListe(key), json(listeSatiri));
    // SW'nin ağ yedeği olarak tam liste (ağdan alınabilirse)
    const lr = await fetch(listeAdresi(), { cache: 'no-store' }).catch(() => null);
    if (lr?.ok) await cache.put(listeAdresi(), lr);

    const kb = cdKurulBilgisi(key);
    cdCevrimdisiYaz(key, {
      vid: vid!,
      surum: (v as any).surum || v.bayt || 0,
      etiket: v.etiket,
      baslik: detay.baslik,
      no: String(detay.no),
      bayt: ses.size + pdfler.reduce((a, p) => a + p.blob.size, 0),
      pdfler: pdfler.map((p) => p.url),
      deckId: detay.pdf?.deckId,
      at: Date.now(),
      kurul: kb?.kurul,
      silinebilir: kb?.silinebilir,
    });
    swBildir();
    isYaz(key, null);
  } catch (e: any) {
    const iptal = e?.name === 'AbortError';
    isYaz(key, iptal ? null : { oran: 0, hata: e?.message || 'İndirilemedi.' });
    if (!iptal) throw e;
  } finally {
    iptaller.delete(key);
  }
}

export function cdCevrimdisiIptal(key: string) {
  iptaller.get(key)?.abort();
}
export const cdCevrimdisiHataSil = (key: string) => { if (isler[key]?.hata) isYaz(key, null); };

/** Dersi cihazdan siler. Başka bir indirilmiş dersin de kullandığı PDF kalır. */
export async function cdCevrimdisiSil(keys: string[]): Promise<void> {
  const tum = cdCevrimdisiKayitlari();
  const kalan = Object.entries(tum).filter(([k]) => !keys.includes(k));
  const kullanilan = new Set(kalan.flatMap(([, x]) => x.pdfler || []));
  const deckKullanilan = new Set(kalan.map(([, x]) => x.deckId).filter(Boolean));
  if (cdCevrimdisiDestek()) {
    const cache = await caches.open(CD_OFFLINE_CACHE);
    for (const key of keys) {
      const x = tum[key];
      if (!x) continue;
      await Promise.all([
        cache.delete(sesAnahtari(key, x.vid)),
        cache.delete(detayAdresi(key)),
        cache.delete(yedekDetay(key)),
        cache.delete(yedekListe(key)),
        ...(x.pdfler || []).filter((u) => !kullanilan.has(u)).map((u) => cache.delete(u)),
        ...(x.deckId && !deckKullanilan.has(x.deckId) ? [cache.delete(deckAdresi(x.deckId))] : []),
      ]);
    }
  }
  for (const key of keys) cdCevrimdisiYaz(key, null);
  swBildir();
}

/** Kayıt defterindeki ama önbellekte olmayan dersler (kullanıcı site verisini temizlediyse) defterden düşer. */
export async function cdCevrimdisiDogrula(): Promise<void> {
  if (!cdCevrimdisiDestek()) return;
  const tum = cdCevrimdisiKayitlari();
  const keys = Object.keys(tum);
  if (!keys.length) return;
  const cache = await caches.open(CD_OFFLINE_CACHE);
  for (const key of keys) {
    if (!(await cache.match(sesAnahtari(key, tum[key].vid)))) cdCevrimdisiYaz(key, null);
  }
}

/* ---------------- store yedekleri (ağ yokken) ---------------- */
export async function cdYerelDetay(key: string): Promise<CdDetay | null> {
  if (!cdCevrimdisiDestek() || !cdCevrimdisiKayitlari()[key]) return null;
  const r = await caches.match(yedekDetay(key));
  return r ? r.json() : null;
}
export async function cdYerelListe(): Promise<CdListeDers[]> {
  if (!cdCevrimdisiDestek()) return [];
  const out: CdListeDers[] = [];
  for (const key of Object.keys(cdCevrimdisiKayitlari())) {
    const r = await caches.match(yedekListe(key));
    if (r) out.push(await r.json());
  }
  return out;
}
