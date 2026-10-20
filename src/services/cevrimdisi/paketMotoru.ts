/**
 * Çevrimdışı merkezi — paket motoru.
 *
 * Paket = cihaza birlikte inen dosyalar (bir dersin soru çözücü seti, önem listesi + sesli asistan, alternatif çözücü, Öğren destesi
 * + sesleri + PDF'i, başvuru verileri, uygulama kodu). Katalog sunucudan gelir (`/api/cevrimdisi/katalog`, src/services/cevrimdisiKatalog.ts);
 * iki özel tür istemcide eklenir: sesli dersler (`sesli:<key>`, canliDersCevrimdisi.ts) ve çıkmış/soru havuzu veritabanı (`db:sorular`,
 * offlineDatabaseService → IndexedDB).
 *
 * Saklama: dosyalar `medsor-paket-v1` önbelleğinde (sw.js sürüm temizliğinde silmez, yalnız kullanıcı siler). Ses klipleri sorgusuz adresle
 * anahtarlanır, sürüm `X-Paket-Surum` başlığında; sw.js bu önbellekteki sesi Range/206 ile verir, derleme parçalarını ve API JSON'larını
 * önbellekten sunar. Kayıt defteri IndexedDB `medsor_cevrimdisi` › `paketler` (paket başına dosya listesi; paylaşılan dosyalar —
 * dizinler, ortak klipler — yalnız hiçbir paket kullanmıyorsa silinir).
 *
 * İndirme: kalıcı kuyruk (localStorage), dosya düzeyinde devam (yarıda kalan paket yeniden başlayınca inmiş dosyaları atlar), yavaş
 * ağda 2, hızlıda 4 paralel istek, dosya başına 4 deneme (2/4/8/16 sn), bağlantı gidince durur ve gelince sürer. "Yalnız Wi-Fi"
 * açıksa hücresel ağda beklenir. Güncelleme: katalogdaki paket sürümü cihazdakinden farklıysa yalnız değişen dosyalar iner.
 */
import { useSyncExternalStore } from 'react';
import { getCustomApiUrl } from '../api';

export const PAKET_CACHE = 'medsor-paket-v1';
const DB_ADI = 'medsor_cevrimdisi';
const AYAR_KEY = 'medsoru_cevrimdisi_v1';
const KUYRUK_KEY = 'medsoru_cevrimdisi_kuyruk_v1';
const SECIM_KEY = 'medsoru_cevrimdisi_secim_v1';
const KATALOG_KEY = '/__cevrimdisi/katalog';

export type Modul = 'uygulama' | 'sesli' | 'cozucu' | 'onem' | 'alt' | 'ogren' | 'veri' | 'db';
export interface PDosya { u: string; v?: string; b: number }
export interface Paket {
  id: string;
  modul: Modul;
  grup: string;
  baslik: string;
  alt?: string;
  sira: number;
  bayt: number;
  n: number;
  surum: string;
  zorunlu?: boolean;
  /** İsteğe bağlı ağır parçalar (ses klipleri, ders PDF'leri) */
  ek?: { ses?: { b: number; n: number }; pdf?: { b: number; n: number } };
  surumT?: { veri: string; ses?: string; pdf?: string };
  /** Birlikte inmesi gereken paketler (sunucu kataloğu) */
  bagimli?: string[];
}
/** Paket başına içerik seçimi: sesler ve PDF'ler inecek mi */
export interface Secim { ses: boolean; pdf: boolean }
export type DosyaTuru = 'ses' | 'pdf' | 'veri';
export interface Kayit {
  id: string;
  surum: string;
  bayt: number;
  dosyalar: PDosya[];
  at: number;
  baslik: string;
  modul: Modul;
  grup: string;
  /** İndirme sürüyor/yarıda kaldı: dosyalar planlanan listedir */
  yarim?: boolean;
  /** İndirilirken geçerli içerik seçimi ve tür başına sürümler */
  secim?: Secim;
  surumT?: Paket['surumT'];
}
export type Durum = 'yok' | 'kuyrukta' | 'iniyor' | 'tamam' | 'guncelleme' | 'hata';
export interface Ayar {
  /** Çevrimdışı mod açık: uygulama dosyaları cihazda tutulur, güncellemeler kendiliğinden iner */
  acik: boolean;
  /** Yalnız Wi-Fi / kablolu ağda indir */
  wifi: boolean;
  /** Güncellemeleri kendiliğinden indir */
  otoGuncelle: boolean;
  /** Yeni indirmelerde varsayılan: ses klipleri de insin (kapalı = sessiz, çok daha az yer) */
  ses: boolean;
  /** Yeni indirmelerde varsayılan: ders PDF'leri de insin */
  pdf: boolean;
  /** Cihazda bırakılacak en az boş alan (bayt); indirme bunun altına düşürmez */
  pay: number;
}
export interface Aktif { id: string; alinan: number; toplam: number; hiz: number; dosya: number; dosyaSay: number; bekliyor?: string }

/* ------------------------------------------------------------------ depo ------------------------------------------------------------------ */
interface Durumlar {
  katalog: Paket[];
  katalogAt: number;
  katalogHata?: string;
  kayitlar: Record<string, Kayit>;
  kuyruk: string[];
  aktif: Aktif | null;
  hatalar: Record<string, string>;
  ayar: Ayar;
  duraklat: boolean;
  hazir: boolean;
  /** Paket başına içerik seçimi (yoksa ayardaki varsayılan) */
  secimler: Record<string, Secim>;
}
const oku = <T,>(k: string, d: T): T => {
  try {
    const v = JSON.parse(localStorage.getItem(k) || 'null');
    return v ?? d;
  } catch {
    return d;
  }
};
const yazLS = (k: string, v: unknown) => {
  try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* kota */ }
};
let S: Durumlar = {
  katalog: [],
  katalogAt: 0,
  kayitlar: {},
  kuyruk: typeof localStorage !== 'undefined' ? oku<string[]>(KUYRUK_KEY, []) : [],
  aktif: null,
  hatalar: {},
  ayar: { acik: false, wifi: false, otoGuncelle: true, ses: true, pdf: true, pay: 300 * 1024 * 1024, ...(typeof localStorage !== 'undefined' ? oku<Partial<Ayar>>(AYAR_KEY, {}) : {}) },
  duraklat: false,
  hazir: false,
  secimler: typeof localStorage !== 'undefined' ? oku<Record<string, Secim>>(SECIM_KEY, {}) : {},
};
const subs = new Set<() => void>();
let yayZaman = 0;
let yayBekleyen: number | null = null;
function yay(hemen = true) {
  if (!hemen) {
    // İlerleme güncellemeleri en çok 5/sn
    const t = Date.now();
    if (t - yayZaman < 200) {
      if (yayBekleyen == null) yayBekleyen = window.setTimeout(() => { yayBekleyen = null; yay(); }, 200);
      return;
    }
  }
  yayZaman = Date.now();
  subs.forEach((f) => f());
}
const guncelle = (p: Partial<Durumlar>, hemen = true) => {
  S = { ...S, ...p };
  if (p.kuyruk) yazLS(KUYRUK_KEY, p.kuyruk);
  if (p.ayar) yazLS(AYAR_KEY, p.ayar);
  if (p.secimler) yazLS(SECIM_KEY, p.secimler);
  yay(hemen);
};
export const abone = (f: () => void) => {
  subs.add(f);
  return () => { subs.delete(f); };
};
export const durumAl = () => S;
export function useCevrimdisi(): Durumlar {
  return useSyncExternalStore(abone, durumAl, durumAl);
}

/* ------------------------------------------------------------------ yardımcılar ------------------------------------------------------------------ */
export const destek = () => typeof caches !== 'undefined' && typeof indexedDB !== 'undefined';
const SES_RE = /^\/api\/(cozucu-ses|patoloji-asistan\/ses|patoloji-cozucu\/ses|patoloji-cozucu-alt\/ses|ogren-ses|kamp\/ses)\//;
/** Dosya türü (sunucu cevrimdisiKatalog.dosyaTuru ile aynı kural) */
export const dosyaTuru = (u: string): DosyaTuru =>
  /\.mp3($|\?)/i.test(u) || SES_RE.test(u) ? 'ses' : u.startsWith('/api/lecture-pdf/') || u.startsWith('/vendor/pdfjs/') ? 'pdf' : 'veri';
const tabanFor = (u: string) => (u.startsWith('/api/') ? (getCustomApiUrl(u) || '').replace(/\/$/, '') : '');
/** Önbellek anahtarı (sw.js ile aynı kural): ses klipleri sorgusuz, diğerleri tam adres */
export function anahtar(d: PDosya | string): string {
  const u = typeof d === 'string' ? d : d.u;
  const abs = new URL(tabanFor(u) + u, location.href);
  if (SES_RE.test(abs.pathname)) return abs.origin + abs.pathname;
  return abs.href;
}
/** İndirme adresi (ses klibine sürüm sorgusu eklenir: sunucu/CDN önbelleği bayatlamasın) */
const indirmeAdresi = (d: PDosya) => {
  const abs = new URL(tabanFor(d.u) + d.u, location.href);
  if (d.v && SES_RE.test(abs.pathname)) abs.searchParams.set('v', d.v);
  return abs.href;
};
const swBildir = () => {
  try { navigator.serviceWorker?.controller?.postMessage({ type: 'PAKET_CHANGED' }); } catch { /* yok */ }
};
const bekle = (ms: number) => new Promise((r) => setTimeout(r, ms));

export function agTuru(): { cevrimici: boolean; yavas: boolean; hucresel: boolean; veriTasarrufu: boolean } {
  const c = (navigator as any).connection;
  const et = String(c?.effectiveType || '');
  return {
    cevrimici: navigator.onLine,
    yavas: /(^|-)2g|3g/.test(et) || (typeof c?.downlink === 'number' && c.downlink > 0 && c.downlink < 1.5),
    hucresel: c?.type === 'cellular',
    veriTasarrufu: !!c?.saveData,
  };
}

/* ------------------------------------------------------------------ IndexedDB kayıt defteri ------------------------------------------------------------------ */
let dbP: Promise<IDBDatabase> | null = null;
function db(): Promise<IDBDatabase> {
  if (!dbP) {
    dbP = new Promise((ok, hata) => {
      const r = indexedDB.open(DB_ADI, 1);
      r.onupgradeneeded = () => {
        const d = r.result;
        if (!d.objectStoreNames.contains('paketler')) d.createObjectStore('paketler', { keyPath: 'id' });
      };
      r.onsuccess = () => {
        const d = r.result;
        d.onversionchange = () => { d.close(); dbP = null; };
        ok(d);
      };
      r.onerror = () => { dbP = null; hata(r.error); };
      r.onblocked = () => { dbP = null; hata(new Error('Cihaz deposu meşgul.')); };
    });
  }
  return dbP;
}
const istek = <T,>(r: IDBRequest<T>) => new Promise<T>((ok, hata) => { r.onsuccess = () => ok(r.result); r.onerror = () => hata(r.error); });
async function kayitlariOku(): Promise<Record<string, Kayit>> {
  const d = await db();
  const hepsi = await istek(d.transaction('paketler', 'readonly').objectStore('paketler').getAll() as IDBRequest<Kayit[]>);
  return Object.fromEntries(hepsi.map((k) => [k.id, k]));
}
async function kayitYaz(k: Kayit | null, id?: string) {
  const d = await db();
  const st = d.transaction('paketler', 'readwrite').objectStore('paketler');
  await istek((k ? st.put(k) : st.delete(id!)) as IDBRequest<unknown>);
  const n = { ...S.kayitlar };
  if (k) n[k.id] = k;
  else delete n[id!];
  guncelle({ kayitlar: n });
}

/** Başka ekranlardan (sesli ders, eski veritabanı penceresi) gelen kayıtlar: değiştiyse yazılır */
export async function kayitEkleDisaridan(k: Kayit) {
  const o = S.kayitlar[k.id];
  if (o && o.surum === k.surum && o.bayt === k.bayt && !o.yarim) return;
  await kayitYaz({ ...k, grup: k.grup || o?.grup || '' });
}
export async function kayitSilDisaridan(id: string) {
  if (S.kayitlar[id]) await kayitYaz(null, id);
}

/* ------------------------------------------------------------------ katalog ------------------------------------------------------------------ */
type Ekler = { sesli: () => Promise<Paket[]>; db: () => Promise<Paket[]> };
let ekler: Ekler | null = null;
/** Sesli ders ve veritabanı uyarlayıcıları (uyarlayicilar.ts) kendini kaydeder */
export function ekKaydet(e: Ekler) { ekler = e; }

/** Modüller arasında aynı branşa aynı ad ("Tıbbi Patoloji", "Enfeksiyon Hastalıkları" → "Patoloji", "Enfeksiyon") */
const GRUP_ES: Record<string, string> = {
  'Enfeksiyon Hastalıkları': 'Enfeksiyon', 'Kadın Hastalıkları ve Doğum': 'Kadın Doğum', 'Kadın Hastalıkları Ve Doğum': 'Kadın Doğum',
};
export const grupAdi = (g: string) => {
  const t = String(g || 'Diğer').replace(/^Tıbbi\s+/i, '').trim();
  return GRUP_ES[t] || t;
};

let katalogP: Promise<void> | null = null;
export function katalogYenile(zorla = false): Promise<void> {
  if (katalogP && !zorla) return katalogP;
  katalogP = (async () => {
    let sunucu: Paket[] | null = null;
    const cache = destek() ? await caches.open(PAKET_CACHE) : null;
    try {
      if (!navigator.onLine) throw new Error('çevrimdışı');
      const r = await fetch(`${tabanFor('/api/')}/api/cevrimdisi/katalog`, { cache: 'no-store' });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const j = await r.json();
      sunucu = j.paketler;
      await cache?.put(new URL(KATALOG_KEY, location.href).href, new Response(JSON.stringify(j), { headers: { 'Content-Type': 'application/json' } }));
      guncelle({ katalogHata: undefined });
    } catch (e: any) {
      // Çevrimdışı ya da sunucu yok: son bilinen katalog
      const eski = await cache?.match(new URL(KATALOG_KEY, location.href).href);
      if (eski) sunucu = (await eski.json()).paketler;
      if (!sunucu) guncelle({ katalogHata: navigator.onLine ? 'Paket listesi alınamadı.' : 'Paket listesi için bir kez internete bağlanman gerekiyor.' });
    }
    const ek = ekler ? (await Promise.all([ekler.sesli().catch(() => []), ekler.db().catch(() => [])])).flat() : [];
    const hepsi = [...(sunucu || []), ...ek].map((p) => ({ ...p, grup: grupAdi(p.grup) }));
    guncelle({ katalog: hepsi, katalogAt: Date.now() });
  })().finally(() => { katalogP = null; });
  return katalogP;
}

export function paketDurumu(id: string, s: Durumlar = S): Durum {
  if (S.aktif?.id === id) return 'iniyor';
  if (s.kuyruk.includes(id)) return 'kuyrukta';
  if (s.hatalar[id]) return 'hata';
  const k = s.kayitlar[id];
  if (!k || k.yarim) return 'yok';
  const p = s.katalog.find((x) => x.id === id);
  if (p && guncelMi(p, k) === false) return 'guncelleme';
  return 'tamam';
}

/** Paket için geçerli içerik seçimi: kullanıcının paket seçimi > cihazdaki kayıt > ayardaki varsayılan */
export function secimAl(id: string, s: Durumlar = S): Secim {
  return s.secimler[id] || s.kayitlar[id]?.secim || { ses: s.ayar.ses, pdf: s.ayar.pdf };
}
/** Seçime göre inecek bayt (ek parçası olmayan paketlerde tamamı) */
export function secimliBayt(p: Paket, secim: Secim): number {
  let b = p.bayt;
  if (!secim.ses) b -= p.ek?.ses?.b || 0;
  if (!secim.pdf) b -= p.ek?.pdf?.b || 0;
  return Math.max(0, b);
}
/** Cihazdaki kopya katalogdakiyle aynı mı (yalnız inen türlerin sürümü karşılaştırılır) */
function guncelMi(p: Paket, k: Kayit): boolean {
  if (!p.surum) return true;
  if (p.surumT && k.surumT && k.secim) {
    if (p.surumT.veri !== k.surumT.veri) return false;
    if (k.secim.ses && (p.surumT.ses || '') !== (k.surumT.ses || '')) return false;
    if (k.secim.pdf && (p.surumT.pdf || '') !== (k.surumT.pdf || '')) return false;
    return true;
  }
  return k.surum === p.surum;
}

/* ------------------------------------------------------------------ özel türler ------------------------------------------------------------------ */
export interface OzelTur {
  indir(id: string, ilerle: (alinan: number, toplam: number) => void, signal: AbortSignal): Promise<{ surum: string; bayt: number }>;
  sil(id: string): Promise<void>;
}
const ozel: Partial<Record<Modul, OzelTur>> = {};
export function ozelKaydet(m: Modul, t: OzelTur) { ozel[m] = t; }

/* ------------------------------------------------------------------ indirme ------------------------------------------------------------------ */
let calisiyor = false;
let iptal: AbortController | null = null;

export function kuyrugaEkle(ids: string[], basa = false, secim?: Secim) {
  // Bağımlı paketler (katalogdaki `bagimli`): cihazda olmayanlar da birlikte kuyruğa girer (iç içe olabilir)
  const tum = new Set(ids);
  for (let i = 0; i < 3; i++) {
    for (const id of [...tum]) for (const b of S.katalog.find((p) => p.id === id)?.bagimli || []) if (paketDurumu(b) === 'yok') tum.add(b);
  }
  ids = [...tum];
  // İçerik inerken uygulama kodu da cihazda olmalı (yoksa ekranlar internetsiz açılmaz; PDF görüntüleyici, çizim işçisi vb.)
  // Güncel olmalı da: içerik parçalarının adları yeni derlemeye aittir, eski kabuk onları bulamaz
  if (ids.some((x) => x !== 'uygulama') && !ids.includes('uygulama') && ['yok', 'guncelleme', 'hata'].includes(paketDurumu('uygulama'))) ids = ['uygulama', ...ids];
  if (secim) {
    const sm = { ...S.secimler };
    ids.forEach((id) => { sm[id] = secim; });
    guncelle({ secimler: sm });
  }
  const yeni = ids.filter((id) => !S.kuyruk.includes(id) && S.aktif?.id !== id);
  if (!yeni.length) return;
  const h = { ...S.hatalar };
  yeni.forEach((id) => delete h[id]);
  guncelle({ kuyruk: basa ? [...yeni, ...S.kuyruk] : [...S.kuyruk, ...yeni], hatalar: h });
  // Listeden indirildiyse (merkez hiç açılmadan) boyut/ilerleme için katalog da gelsin
  if (!S.katalog.length) void katalogYenile().then(() => calistir());
  else void calistir();
}
export function kuyruktanCikar(ids: string[]) {
  guncelle({ kuyruk: S.kuyruk.filter((x) => !ids.includes(x)) });
  if (S.aktif && ids.includes(S.aktif.id)) iptal?.abort();
}
export function duraklat(d: boolean) {
  guncelle({ duraklat: d });
  if (d) iptal?.abort();
  else void calistir();
}
export function ayarYaz(p: Partial<Ayar>) {
  guncelle({ ayar: { ...S.ayar, ...p } });
  if (p.wifi === false) void calistir();
}

/** Ağ izin veriyor mu (yoksa bekleme nedeni) */
function agEngeli(): string | null {
  const a = agTuru();
  if (!a.cevrimici) return 'İnternet bağlantısı bekleniyor';
  if (S.ayar.wifi && a.hucresel) return 'Wi-Fi bekleniyor (yalnız Wi-Fi açık)';
  return null;
}

async function calistir() {
  if (calisiyor || !destek()) return;
  calisiyor = true;
  try {
    while (S.kuyruk.length && !S.duraklat) {
      const engel = agEngeli();
      if (engel) {
        guncelle({ aktif: { id: S.kuyruk[0], alinan: 0, toplam: 0, hiz: 0, dosya: 0, dosyaSay: 0, bekliyor: engel } });
        break; // 'online' / bağlantı değişimi yeniden başlatır
      }
      const id = S.kuyruk[0];
      iptal = new AbortController();
      try {
        await paketIndir(id, iptal.signal);
        guncelle({ kuyruk: S.kuyruk.filter((x) => x !== id) });
      } catch (e: any) {
        if (iptal.signal.aborted || e?.name === 'AbortError') {
          // Duraklatma ya da kuyruktan çıkarma: paket kuyrukta kalır (çıkarıldıysa zaten yok)
          if (S.duraklat) break;
          continue;
        }
        if (!navigator.onLine) continue; // döngü başında bağlantı beklenir
        guncelle({ kuyruk: S.kuyruk.filter((x) => x !== id), hatalar: { ...S.hatalar, [id]: e?.message || 'İndirilemedi' } });
      }
    }
  } finally {
    calisiyor = false;
    iptal = null;
    if (!S.aktif?.bekliyor || !S.kuyruk.length) guncelle({ aktif: null });
    void depolamaYenile();
  }
}

async function paketIndir(id: string, signal: AbortSignal) {
  const p = S.katalog.find((x) => x.id === id);
  const aktif: Aktif = { id, alinan: 0, toplam: p?.bayt || 0, hiz: 0, dosya: 0, dosyaSay: p?.n || 0 };
  guncelle({ aktif });
  try { await navigator.storage?.persist?.(); } catch { /* izin yok */ }
  const t0 = Date.now();
  const ilerle = (alinan: number, toplam: number) => {
    const sn = Math.max(0.5, (Date.now() - t0) / 1000);
    guncelle({ aktif: { ...S.aktif!, alinan, toplam: toplam || S.aktif!.toplam, hiz: alinan / sn } }, false);
  };
  const m = (p?.modul || id.split(':')[0]) as Modul;
  const oz = ozel[m];
  if (oz) {
    const r = await oz.indir(id, ilerle, signal);
    await kayitYaz({ id, surum: r.surum || p?.surum || '', bayt: r.bayt, dosyalar: [], at: Date.now(), baslik: p?.baslik || id, modul: m, grup: p?.grup || '' });
    return;
  }

  const r = await fetch(`${tabanFor('/api/')}/api/cevrimdisi/paket/${encodeURIComponent(id)}`, { cache: 'no-store', signal });
  if (!r.ok) throw new Error(r.status === 404 ? 'Bu paket artık sunucuda yok.' : `Paket bilgisi alınamadı (${r.status}).`);
  const ham: Paket & { dosyalar: PDosya[] } = await r.json();
  const secim = secimAl(id);
  // Uygulama paketi seçimden bağımsız tam iner (sessiz klip, motivasyon klipleri, PDF.js yardımcıları uygulamanın parçası)
  const bilgi = { ...ham, dosyalar: ham.dosyalar.filter((d) => { const t = dosyaTuru(d.u); return id === 'uygulama' || t === 'veri' || secim[t]; }) };
  const cache = await caches.open(PAKET_CACHE);
  const onceki = S.kayitlar[id];
  // Yarım kaldığında silinebilsin diye plan önce kaydedilir (eski dosyalar + yeni dosyalar)
  const plan = new Map<string, PDosya>();
  for (const d of onceki?.dosyalar || []) plan.set(d.u, d);
  for (const d of bilgi.dosyalar) plan.set(d.u, d);
  if (!onceki || onceki.yarim) {
    await kayitYaz({ id, surum: '', bayt: 0, dosyalar: [...plan.values()], at: Date.now(), baslik: bilgi.baslik, modul: bilgi.modul, grup: bilgi.grup, yarim: true });
  } else {
    // Güncelleme: eski sürüm kullanılabilir kalır, yeni dosyalar da defterde (yarıda kalırsa silmede unutulmasın)
    await kayitYaz({ ...onceki, dosyalar: [...plan.values()] });
  }

  // Cihazda aynı sürümüyle olanlar atlanır
  const eksik: PDosya[] = [];
  let hazirBayt = 0;
  for (const d of bilgi.dosyalar) {
    const hit = await cache.match(anahtar(d));
    if (hit && (hit.headers.get('X-Paket-Surum') || '') === (d.v || '')) hazirBayt += d.b;
    else eksik.push(d);
  }
  const toplam = bilgi.dosyalar.reduce((a, d) => a + d.b, 0);
  // Yer denetimi: inecek kısım cihazdaki boş alanı (bırakılacak pay dahil) aşıyorsa hiç başlamadan dur
  try {
    const e = await navigator.storage?.estimate?.();
    if (e?.quota) {
      const bos = e.quota - (e.usage || 0);
      const gerek = toplam - hazirBayt;
      if (gerek > 0 && gerek > bos - S.ayar.pay) {
        throw Object.assign(new Error(`Cihazda yer yetmiyor: ${mb(gerek)} gerekli, ${mb(Math.max(0, bos))} boş. Sesleri kapatarak ya da başka paketleri silerek yer aç.`), { name: 'YerYok' });
      }
    }
  } catch (e: any) { if (e?.name === 'YerYok') throw e; }
  let alinan = hazirBayt;
  let biten = bilgi.dosyalar.length - eksik.length;
  guncelle({ aktif: { ...S.aktif!, toplam, alinan, dosya: biten, dosyaSay: bilgi.dosyalar.length } });

  const paralel = agTuru().yavas ? 2 : 4;
  let sira = 0;
  const isci = async () => {
    while (sira < eksik.length) {
      if (signal.aborted) throw Object.assign(new Error('İptal'), { name: 'AbortError' });
      const d = eksik[sira++];
      let deneme = 0;
      for (;;) {
        let dosyaAlinan = 0;
        try {
          const res = await fetch(indirmeAdresi(d), { signal });
          if (!res.ok) {
            if (res.status === 404) break; // sunucuda yok: paket yine de kullanılabilir (o klip ağdan da gelmez)
            throw new Error(`HTTP ${res.status}`);
          }
          const parcalar: BlobPart[] = [];
          if (res.body) {
            const okuyucu = res.body.getReader();
            for (;;) {
              const { done, value } = await okuyucu.read();
              if (done) break;
              parcalar.push(value as Uint8Array<ArrayBuffer>);
              dosyaAlinan += value.byteLength;
              alinan += value.byteLength;
              ilerle(alinan, toplam);
            }
          } else parcalar.push(await res.blob());
          const blob = new Blob(parcalar, { type: res.headers.get('Content-Type') || '' });
          const basliklar: Record<string, string> = {
            'Content-Type': res.headers.get('Content-Type') || 'application/octet-stream',
            'Content-Length': String(blob.size),
            'X-Paket-Surum': d.v || '',
          };
          if (SES_RE.test(new URL(indirmeAdresi(d)).pathname)) basliklar['Accept-Ranges'] = 'bytes';
          await cache.put(anahtar(d), new Response(blob, { headers: basliklar }));
          break;
        } catch (e: any) {
          alinan -= dosyaAlinan;
          if (signal.aborted || e?.name === 'AbortError') throw Object.assign(new Error('İptal'), { name: 'AbortError' });
          if (e?.name === 'QuotaExceededError' || /quota/i.test(String(e?.message))) throw new Error('Cihazda yer kalmadı. Bazı paketleri silip yeniden dene.');
          if (++deneme > 4) throw new Error('Bağlantı sorunu: dosya inmedi. Yeniden dene.');
          // Bağlantı gittiyse gelene dek bekle
          while (!navigator.onLine && !signal.aborted) await bekle(1500);
          await bekle(2000 * 2 ** (deneme - 1));
        }
      }
      biten++;
      guncelle({ aktif: { ...S.aktif!, dosya: biten } }, false);
    }
  };
  await Promise.all(Array.from({ length: Math.min(paralel, eksik.length) }, isci));
  // Google yazı tipi CSS'i indiyse içindeki Türkçe için gereken (latin, latin-ext) woff2 dosyaları da iner ve pakete yazılır
  for (const d of bilgi.dosyalar.filter((x) => x.u.startsWith('https://fonts.googleapis.com/'))) {
    try {
      const css = await (await cache.match(anahtar(d)))?.text();
      const bloklar = (css || '').split('/*').filter((b) => /^\s*latin(-ext)?\s*\*\//.test(b));
      const adresler = [...new Set(bloklar.flatMap((b) => b.match(/https:\/\/fonts\.gstatic\.com\/[^)'"\s]+/g) || []))];
      for (const u of adresler) {
        if (signal.aborted) break;
        if (!(await cache.match(u))) {
          const r = await fetch(u, { signal, mode: 'cors' });
          if (r.ok) await cache.put(u, new Response(await r.blob(), { headers: { 'Content-Type': r.headers.get('Content-Type') || 'font/woff2', 'X-Paket-Surum': '' } }));
        }
        bilgi.dosyalar.push({ u, b: 0 });
      }
    } catch { /* yazı tipi inmezse sistem yazı tipi kullanılır */ }
  }

  // Artık kullanılmayan eski dosyalar (başka paket kullanmıyorsa) silinir
  const yeni = new Set(bilgi.dosyalar.map((d) => d.u));
  const atilacak = [...plan.values()].filter((d) => !yeni.has(d.u));
  await kayitYaz({ id, surum: bilgi.surum, bayt: toplam, dosyalar: bilgi.dosyalar, at: Date.now(), baslik: bilgi.baslik, modul: bilgi.modul, grup: bilgi.grup,
    secim, surumT: bilgi.surumT });
  await dosyalariBirak(atilacak, id);
  swBildir();
}

const mb = (n: number) => (n >= 1024 ** 3 ? `${(n / 1024 ** 3).toFixed(1)} GB` : `${Math.max(1, Math.round(n / 1024 / 1024))} MB`).replace('.', ',');

/**
 * Paketlerin içerik seçimini değiştir. Bir türü kaldırmak internetsiz, anında yapılır (dosyalar silinir, ders sessiz kullanılır);
 * eklemek için paket yeniden kuyruğa girer ve yalnız eksik dosyalar iner.
 */
export async function secimDegistir(ids: string[], degisim: Partial<Secim>) {
  const sm = { ...S.secimler };
  const indirilecek: string[] = [];
  for (const id of ids) {
    const eski = secimAl(id);
    const yeni = { ...eski, ...degisim };
    sm[id] = yeni;
    const k = S.kayitlar[id];
    if (!k || k.yarim) continue;
    const ekle = (yeni.ses && !eski.ses) || (yeni.pdf && !eski.pdf) || (k.secim && ((yeni.ses && !k.secim.ses) || (yeni.pdf && !k.secim.pdf)));
    // Kaldırılan türler: yerelde düş
    const kalan = k.dosyalar.filter((d) => { const t = dosyaTuru(d.u); return t === 'veri' || yeni[t]; });
    if (kalan.length !== k.dosyalar.length) {
      const atilan = k.dosyalar.filter((d) => !kalan.includes(d));
      await kayitYaz({ ...k, dosyalar: kalan, bayt: kalan.reduce((a, d) => a + d.b, 0), secim: { ses: !!(k.secim || eski).ses && yeni.ses, pdf: !!(k.secim || eski).pdf && yeni.pdf } });
      await dosyalariBirak(atilan, id);
    }
    if (ekle) indirilecek.push(id);
  }
  guncelle({ secimler: sm });
  if (indirilecek.length) kuyrugaEkle(indirilecek);
  swBildir();
  void depolamaYenile();
}

/** Modül başına cihazdaki bayt (yer kullanımı dökümü) */
export function modulDokumu(s: Durumlar = S): { modul: Modul; bayt: number; n: number; ses: number }[] {
  const m = new Map<Modul, { modul: Modul; bayt: number; n: number; ses: number }>();
  for (const k of Object.values(s.kayitlar)) {
    if (k.yarim) continue;
    const x = m.get(k.modul) || { modul: k.modul, bayt: 0, n: 0, ses: 0 };
    x.bayt += k.bayt;
    x.n++;
    x.ses += k.dosyalar.filter((d) => dosyaTuru(d.u) === 'ses').reduce((a, d) => a + d.b, 0);
    m.set(k.modul, x);
  }
  return [...m.values()].sort((a, b) => b.bayt - a.bayt);
}

/** Hiçbir paketin kullanmadığı artık dosyaları (yarıda kalmış eski sürümler vb.) siler; boşalan baytı döndürür */
export async function yerAc(): Promise<number> {
  if (!destek()) return 0;
  const kullanilan = new Set<string>([new URL(KATALOG_KEY, location.href).href]);
  for (const k of Object.values(S.kayitlar)) k.dosyalar.forEach((d) => kullanilan.add(anahtar(d)));
  const cache = await caches.open(PAKET_CACHE);
  let bayt = 0;
  for (const req of await cache.keys()) {
    if (kullanilan.has(req.url)) continue;
    const r = await cache.match(req);
    bayt += Number(r?.headers.get('Content-Length') || 0);
    await cache.delete(req);
  }
  swBildir();
  await depolamaYenile();
  return bayt;
}

/** Diğer paketlerin kullanmadığı dosyaları önbellekten siler */
async function dosyalariBirak(dosyalar: PDosya[], haric: string) {
  if (!dosyalar.length) return;
  const kullanilan = new Set<string>();
  for (const k of Object.values(S.kayitlar)) if (k.id !== haric) k.dosyalar.forEach((d) => kullanilan.add(anahtar(d)));
  const cache = await caches.open(PAKET_CACHE);
  await Promise.all(dosyalar.map((d) => anahtar(d)).filter((a) => !kullanilan.has(a)).map((a) => cache.delete(a)));
}

export async function paketSil(ids: string[]) {
  kuyruktanCikar(ids);
  for (const id of ids) {
    const k = S.kayitlar[id];
    const m = (k?.modul || id.split(':')[0]) as Modul;
    if (ozel[m]) {
      try { await ozel[m]!.sil(id); } catch { /* yine de defterden düşer */ }
      if (k) await kayitYaz(null, id);
      continue;
    }
    if (!k) continue;
    const dosyalar = k.dosyalar;
    await kayitYaz(null, id);
    await dosyalariBirak(dosyalar, id);
  }
  const h = { ...S.hatalar };
  ids.forEach((id) => delete h[id]);
  guncelle({ hatalar: h });
  swBildir();
  void depolamaYenile();
}

/** Güncellemesi olan paketler (otomatik güncelleme ve "Tümünü güncelle") */
export const guncellemeler = (s: Durumlar = S) => Object.keys(s.kayitlar).filter((id) => paketDurumu(id, s) === 'guncelleme');

/* ------------------------------------------------------------------ depolama ------------------------------------------------------------------ */
export interface Depolama { kullanilan: number; kota: number; kalici: boolean }
let depolama: Depolama | null = null;
const depSubs = new Set<() => void>();
export async function depolamaYenile() {
  try {
    const e = await navigator.storage?.estimate?.();
    const kalici = (await navigator.storage?.persisted?.()) || false;
    depolama = e ? { kullanilan: e.usage || 0, kota: e.quota || 0, kalici } : null;
  } catch { depolama = null; }
  depSubs.forEach((f) => f());
}
export const useDepolama = () => useSyncExternalStore((f) => { depSubs.add(f); return () => { depSubs.delete(f); }; }, () => depolama, () => null);

/* ------------------------------------------------------------------ doğrulama ------------------------------------------------------------------ */
/** Kullanıcı site verisini temizlediyse: önbellekte olmayan paketler defterden düşer, yarım paketler kuyruğa döner */
async function dogrula() {
  const cache = await caches.open(PAKET_CACHE);
  for (const k of Object.values(S.kayitlar)) {
    if (!k.dosyalar.length) continue;
    if (k.yarim) {
      if (!S.kuyruk.includes(k.id)) guncelle({ kuyruk: [...S.kuyruk, k.id] });
      continue;
    }
    // İlk ve son dosyaya bakmak yeter (tümü aynı anda silinir)
    const ornek = [k.dosyalar[0], k.dosyalar[k.dosyalar.length - 1]];
    const var_ = await Promise.all(ornek.map((d) => cache.match(anahtar(d))));
    if (var_.some((x) => !x)) await kayitYaz({ ...k, yarim: true });
  }
}

/* ------------------------------------------------------------------ başlatma ------------------------------------------------------------------ */
let basladi = false;
/** Uygulama açılışında bir kez (main/App): defter, katalog, yarım işler, otomatik güncelleme */
export async function cevrimdisiBaslat() {
  if (basladi || !destek()) return;
  basladi = true;
  try {
    guncelle({ kayitlar: await kayitlariOku() });
  } catch { /* IndexedDB kapalı */ }
  await import('./uyarlayicilar').then((m) => m.uyarlayicilariKur()).catch(() => {});
  guncelle({ hazir: true });
  // Otomatik çevrimdışı sınaması (scripts/cevrimdisi_sinama) motoru arayüzsüz sürer
  (window as any).__medsorCevrimdisi = { kuyrugaEkle, durumAl, katalogYenile, paketSil, ayarYaz, paketDurumu, cevrimdisiModuAc };
  void depolamaYenile();
  window.addEventListener('online', () => { void calistir(); void otomatikTur(); });
  (navigator as any).connection?.addEventListener?.('change', () => void calistir());
  // SW arka plan eşitleme mesajı: kuyruk sürsün
  navigator.serviceWorker?.addEventListener?.('message', (e: MessageEvent) => {
    if (e.data?.type === 'MEDSORU_BACKGROUND_SYNC') { void calistir(); }
    if (e.data?.type === 'CEVRIMDISI_SES_YOK') bildir('Bu bölümün sesi cihazda yok; internet gelene dek sessiz devam ediliyor.');
  });
  await dogrula().catch(() => {});
  if (S.kuyruk.length || S.ayar.acik || Object.keys(S.kayitlar).length) {
    await katalogYenile().catch(() => {});
    void calistir();
    void otomatikTur();
  }
}

/** Kısa alt bildirim (React dışı; her ekranda, tam ekran derslerde de görünür). Stil: index.css .cv-toast */
export function bildir(metin: string, ms = 4500) {
  try {
    document.querySelector('.cv-toast')?.remove();
    const el = document.createElement('div');
    el.className = 'cv-toast';
    el.setAttribute('role', 'status');
    el.textContent = metin;
    document.body.appendChild(el);
    window.setTimeout(() => el.remove(), ms);
  } catch { /* DOM yok */ }
}

/** Çevrimdışı mod açıkken: uygulama paketi her zaman güncel, diğer güncellemeler ayara göre */
async function otomatikTur() {
  if (!navigator.onLine) return;
  if (!S.katalog.length) await katalogYenile().catch(() => {});
  // Cihazda herhangi bir paket varsa uygulama paketi de güncel tutulur (çevrimdışı mod kapalı olsa bile)
  if (S.ayar.acik || Object.keys(S.kayitlar).some((id) => id !== 'uygulama')) {
    const u = paketDurumu('uygulama');
    if (u === 'yok' || u === 'guncelleme') kuyrugaEkle(['uygulama'], true);
  }
  if (S.ayar.otoGuncelle) {
    const g = guncellemeler().filter((id) => id !== 'uygulama');
    if (g.length) kuyrugaEkle(g);
  }
}

/** Çevrimdışı modu aç: uygulama + seçilen paketler kuyruğa */
export function cevrimdisiModuAc(ids: string[], secim?: Secim) {
  ayarYaz({ acik: true });
  kuyrugaEkle(['uygulama']);
  kuyrugaEkle(ids.filter((x) => x !== 'uygulama'), false, secim);
}
/** Çevrimdışı modu kapat (silmek isteğe bağlı) */
export async function cevrimdisiModuKapat(sil: boolean) {
  ayarYaz({ acik: false });
  if (sil) await paketSil(Object.keys(S.kayitlar));
  else kuyruktanCikar(['uygulama']);
}
