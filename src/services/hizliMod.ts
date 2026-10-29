/**
 * Hızlı mod: TV modu + Performans modu (tek kaynak).
 *
 * - TV modu: TV tarayıcısı (CanliDersTv TV_UA) ya da ?tv=1 ile kendiliğinden açılır; ?tv=0 kapatır.
 * - Performans modu: Ayarlar › Görünüm › "Performans modu" ya da ?perf=1 / ?perf=0.
 *
 * İkisi de siteyi sesli ders, soru çözücü ve PDF'e odaklar: açılıştaki yan kurulumlar (varlık, kaydırma,
 * seçim paylaşımı, çekerek yenileme, boşta sayfa ön yüklemesi) kurulmaz, ağır CSS (bulanıklık, gölge,
 * geçiş) kapanır, PDF tek seferde indirilip cihazda (Cache Storage) tutulur ve sonraki açılışta ağsız açılır.
 * TV modu ayrıca tuval çözünürlüğünü 1×'e indirir ve ana sayfa yerine sesli dersler listesini açar.
 */
import { cdTvMi } from '../components/canliDers/CanliDersTv';

const PERF_KEY = 'medsor_performans_modu';
const PDF_CACHE = 'medsor-hizli-pdf-v1';
const PDF_TAVAN = 16; // cihazda tutulan en çok PDF (en eski silinir)

let perf: boolean | null = null;
function perfMi(): boolean {
  if (perf != null) return perf;
  try {
    const q = new URLSearchParams(location.search).get('perf');
    if (q === '1' || q === '0') localStorage.setItem(PERF_KEY, q);
    perf = localStorage.getItem(PERF_KEY) === '1';
  } catch { perf = false; }
  return perf;
}

export const tvModu = (): boolean => cdTvMi();
export const performansModu = (): boolean => perfMi();
/** TV ya da performans modu açık mı */
export const hizliMod = (): boolean => tvModu() || perfMi();

export function performansModuAyarla(on: boolean) {
  try { localStorage.setItem(PERF_KEY, on ? '1' : '0'); } catch { /* yok */ }
  location.reload(); // açılış kurulumları yalnız yeniden yüklemede değişir
}
export function tvModuAyarla(on: boolean) {
  try { localStorage.setItem('medsoru_canli_ders_tv', on ? '1' : '0'); } catch { /* yok */ }
  location.reload();
}

/** <html> sınıfları + kalıcı depolama isteği + TV'de ana sayfa → sesli dersler. main.tsx'te render'dan önce. */
export function hizliModuKur() {
  if (typeof document === 'undefined' || !hizliMod()) return;
  const kok = document.documentElement;
  kok.classList.add('hm-hizli');
  if (tvModu()) kok.classList.add('hm-tv');
  // Tarayıcı önbelleği boşaltmasın: PDF ve ses kopyaları açılışlar arasında kalsın
  void navigator.storage?.persist?.().catch(() => {});
  if (tvModu() && (location.pathname === '/' || location.pathname === '')) {
    history.replaceState(history.state, '', '/canliders' + location.search + location.hash);
  }
}

/* ---------------- PDF: tek indirme, cihazda kalır ---------------- */

const bellek = new Map<string, Promise<Uint8Array | null>>();

async function onbellektenYaDaAgdan(url: string): Promise<Uint8Array | null> {
  if (!('caches' in window)) return null;
  const c = await caches.open(PDF_CACHE);
  const var_ = await c.match(url);
  if (var_) {
    void c.put(url, var_.clone()); // erişim sırası: en son açılan en sona (aşağıdaki tavan en eskiyi siler)
    return new Uint8Array(await var_.arrayBuffer());
  }
  const r = await fetch(url, { credentials: 'include' });
  if (!r.ok) return null;
  const buf = await r.arrayBuffer();
  try {
    await c.put(url, new Response(buf.slice(0), { headers: { 'Content-Type': 'application/pdf' } }));
    const anahtarlar = await c.keys();
    for (const k of anahtarlar.slice(0, Math.max(0, anahtarlar.length - PDF_TAVAN))) await c.delete(k);
  } catch { /* kota dolu: yine açılır */ }
  return new Uint8Array(buf);
}

/**
 * Hızlı modda PDF'in tam içeriği (cihazdan ya da tek istekle). null → normal Range akışına dön.
 * pdf.js `data` aldığı ArrayBuffer'ı işçiye aktarır: her çağrıda kopya verilir, bellek kopyası korunur.
 */
export async function hizliPdfVerisi(url: string): Promise<Uint8Array | null> {
  if (!hizliMod() || !url || url.startsWith('blob:') || url.startsWith('data:')) return null;
  let p = bellek.get(url);
  if (!p) {
    p = onbellektenYaDaAgdan(url).catch(() => null);
    bellek.set(url, p);
    if (bellek.size > 3) bellek.delete(bellek.keys().next().value as string);
  }
  const d = await p;
  if (!d) { bellek.delete(url); return null; }
  return d.slice();
}

/** Ders açılmadan PDF'i arka planda cihaza al (liste ekranında ders kartına odaklanınca vb.) */
export function hizliPdfOnYukle(url: string) {
  if (hizliMod()) void hizliPdfVerisi(url);
}
