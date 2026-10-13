/**
 * src/services/deviceStorage.ts
 *
 * Cihazdaki önbellek (CacheStorage) kayıtlarını listeler ve tek tek / toplu siler.
 *  - pdf:  /api/lecture-pdf/… (ders PDF'leri; Service Worker 200 yanıtları DATA önbelleğine yazar)
 *  - data: diğer /api/… yanıtları
 *  - app:  uygulama dosyaları (js, css, yazı tipi, ikon, index.html)
 */
import { DECK_CATALOG } from '../data/deckStore';

export type CacheKind = 'pdf' | 'data' | 'app';

export interface CacheItem {
  cache: string;
  url: string;
  kind: CacheKind;
  name: string;
  bytes: number;
}

const kindOf = (u: URL): CacheKind =>
  u.pathname.includes('/api/lecture-pdf/') ? 'pdf' : u.pathname.includes('/api/') ? 'data' : 'app';

function pdfName(u: URL): string {
  const m = u.pathname.match(/\/api\/lecture-pdf\/deck\/([^/]+)\/(\d+)/);
  if (m) {
    const id = decodeURIComponent(m[1]);
    const d = DECK_CATALOG.find((x) => x.id === id);
    const title = d ? d.shortTitle || d.title : id;
    return Number(m[2]) > 0 ? `${title} · ${Number(m[2]) + 1}. dosya` : title;
  }
  const f = u.pathname.split('/').pop() || '';
  try {
    return decodeURIComponent(f).replace(/\.pdf$/i, '');
  } catch {
    return f;
  }
}

async function sizeOf(res: Response | undefined, exact: boolean): Promise<number> {
  if (!res) return 0;
  const len = Number(res.headers.get('content-length'));
  if (len > 0) return len;
  if (!exact) return 0;
  try {
    return (await res.clone().blob()).size;
  } catch {
    return 0;
  }
}

export async function listCacheItems(): Promise<CacheItem[]> {
  if (typeof caches === 'undefined') return [];
  const out: CacheItem[] = [];
  for (const cacheName of await caches.keys()) {
    const cache = await caches.open(cacheName);
    for (const req of await cache.keys()) {
      let u: URL;
      try {
        u = new URL(req.url, location.origin);
      } catch {
        continue;
      }
      const kind = kindOf(u);
      // Boyutu başlıktan; başlık yoksa yalnız PDF'lerde gövdeyi ölç (yüzlerce küçük yanıtı açmamak için)
      const bytes = await sizeOf(await cache.match(req), kind === 'pdf');
      out.push({
        cache: cacheName,
        url: req.url,
        kind,
        name: kind === 'pdf' ? pdfName(u) : u.pathname + u.search,
        bytes,
      });
    }
  }
  return out;
}

/** Aynı URL birden çok önbellekte olabilir; hepsinden silinir. */
export async function deleteCacheItems(items: Pick<CacheItem, 'cache' | 'url'>[]): Promise<void> {
  if (typeof caches === 'undefined') return;
  await Promise.all(items.map(async (it) => {
    const c = await caches.open(it.cache);
    await c.delete(it.url);
  }));
}

export async function storageEstimate(): Promise<{ usage: number; quota: number } | null> {
  try {
    const e = await navigator.storage?.estimate?.();
    return e ? { usage: e.usage || 0, quota: e.quota || 0 } : null;
  } catch {
    return null;
  }
}

export const fmtBytes = (n: number) =>
  n <= 0 ? '—' : n < 1024 * 1024 ? `${Math.max(1, Math.round(n / 1024))} KB` : `${(n / 1024 / 1024).toFixed(1).replace('.', ',')} MB`;

/** Elle indirilen PDF'ler bu önbellekte durur; SW sürüm temizliğinde silinmesin diye ayrı ad (sw.js listesinde korunur). */
export const PDF_CACHE = 'medsoru-pdf-offline';
export const PDF_SAVED_EVENT = 'medsoru:pdf-saved';

export async function isPdfSaved(url: string): Promise<boolean> {
  if (typeof caches === 'undefined') return false;
  return !!(await caches.match(url));
}

/** PDF'i tam (Range'siz) indirip önbelleğe yazar. */
export async function savePdfOffline(url: string): Promise<void> {
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const blob = await res.blob();
  const c = await caches.open(PDF_CACHE);
  await c.put(url, new Response(blob, { headers: { 'Content-Type': 'application/pdf', 'Content-Length': String(blob.size) } }));
  window.dispatchEvent(new Event(PDF_SAVED_EVENT));
}

export async function removeSavedPdf(url: string): Promise<void> {
  if (typeof caches === 'undefined') return;
  for (const k of await caches.keys()) await (await caches.open(k)).delete(url);
  window.dispatchEvent(new Event(PDF_SAVED_EVENT));
}

/** Cihazdaki kopyayı blob adresi olarak verir (internet yokken görüntüleyici bununla açar). */
export async function savedPdfObjectUrl(url: string): Promise<string | null> {
  if (typeof caches === 'undefined') return null;
  const r = await caches.match(url);
  return r ? URL.createObjectURL(await r.blob()) : null;
}
