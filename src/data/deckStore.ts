/**
 * Öğrenme desteleri: liste anında açılsın diye hafif katalog paketle gelir; bir destenin
 * slaytları yalnızca o deste açılınca ayrı bir parça olarak yüklenir.
 * Dosyalar derlemede scripts/vite/splitLearningDecks.ts ile üretilir.
 */

export interface DeckCatalogEntry {
  id: string;
  deckId?: string;
  title: string;
  shortTitle?: string;
  discipline: string;
  committee?: string;
  instructor?: string;
  overview?: string;
  highYieldPearls?: string[];
  themeColor?: string;
  category?: string;
  slideCount: number;
  questionCount: number;
  cardCount: number;
  firstSlideNumber: number;
  [key: string]: any;
}

// Katalog derlemede üretilir; glob kullanımı dosya henüz yokken de tür denetiminin geçmesini sağlar
// Başarım (2026-10-20): katalog (~575 KB) ilk paketten çıkarıldı; ayrı parça olarak tembel yüklenir.
// DECK_CATALOG aynı dizi nesnesidir, yüklenince yerinde doldurulur. Katalogu eşzamanlı okuyan modüller
// en üstte `await loadDeckCatalog()` yapar (hepsi tembel parçalarda), diğerleri kullanmadan önce bekler.
const catalogModules = import.meta.glob('./decks/catalog.json', { import: 'default' }) as Record<string, () => Promise<unknown>>;
export const DECK_CATALOG: DeckCatalogEntry[] = [];
let catalogPromise: Promise<DeckCatalogEntry[]> | null = null;
let catalogLoaded = false;
export const isDeckCatalogLoaded = () => catalogLoaded;
export function loadDeckCatalog(): Promise<DeckCatalogEntry[]> {
  if (!catalogPromise) {
    const fn = Object.values(catalogModules)[0];
    catalogPromise = (fn ? fn() : Promise.resolve([]))
      .then((list) => {
        // patchCatalog yüklemeden önce eklediyse onları koru (aynı kimlik: canlı sürüm kazanır)
        const early = new Map(DECK_CATALOG.map((d) => [d.id, d]));
        DECK_CATALOG.length = 0;
        for (const d of (Array.isArray(list) ? list : []) as DeckCatalogEntry[]) {
          DECK_CATALOG.push(early.get(d.id) || d);
          early.delete(d.id);
        }
        for (const d of early.values()) DECK_CATALOG.push(d);
        catalogLoaded = true;
        return DECK_CATALOG;
      })
      .catch((err) => { catalogPromise = null; throw err; });
  }
  return catalogPromise;
}

const loaders = import.meta.glob('./decks/items/*.json', { import: 'default' }) as Record<string, () => Promise<any>>;
const flashcardModules = import.meta.glob('./decks/flashcards.json', { import: 'default' }) as Record<string, () => Promise<any>>;
const safe = (id: string) => id.replace(/[^a-zA-Z0-9_-]+/g, '_');
const cache = new Map<string, Promise<any>>();
const MAX_CACHED_DECKS = 8;

function touchDeckCache(id: string, p: Promise<any>) {
  if (cache.has(id)) cache.delete(id);
  else if (cache.size >= MAX_CACHED_DECKS) {
    const oldest = cache.keys().next().value;
    if (oldest) cache.delete(oldest);
  }
  cache.set(id, p);
}

async function loadFromIndexedDb(id: string): Promise<any> {
  if (typeof window === 'undefined' || !('indexedDB' in window)) return null;
  return new Promise((resolve) => {
    try {
      const req = window.indexedDB.open('medsoru_offline_db', 2);
      req.onblocked = () => resolve(null);
      req.onsuccess = () => {
        const db = req.result;
        db.onversionchange = () => db.close();
        if (!db.objectStoreNames.contains('decks')) {
          db.close();
          return resolve(null);
        }
        const tx = db.transaction('decks', 'readonly');
        const store = tx.objectStore('decks');
        const getReq = store.get(id);
        getReq.onsuccess = () => {
          const res = getReq.result || null;
          db.close();
          resolve(res);
        };
        getReq.onerror = () => {
          db.close();
          resolve(null);
        };
      };
      req.onerror = () => resolve(null);
    } catch {
      resolve(null);
    }
  });
}

import { defaultApiBaseForThisHost } from '../config/deployment';
import { contentReady, isContentChanged, changedIds, onContentChanged } from '../services/contentLive';
import { cevrimdisiGibi } from '../services/cevrimdisi/baglanti';

/** Canlı API tabanı: Ayarlar'daki özel URL, yoksa bulunulan hostun varsayılanı (Oracle tüneli). */
function apiBase(): string {
  try {
    if (typeof localStorage !== 'undefined') {
      const custom = (localStorage.getItem('medsoru_custom_api_url') || '').trim().replace(/\/$/, '');
      if (custom) return custom;
    }
  } catch {}
  try {
    return defaultApiBaseForThisHost().replace(/\/$/, '');
  } catch {
    return '';
  }
}

/** Sunucudan tek deste (derlenmiş parça eksikse yedek yol; ?format=json ham JSON döndürür). */
async function loadFromApi<T>(id: string): Promise<T | null> {
  try {
    // Zayıf bağlantıda sonsuza dek beklemesin: 20 sn sonra IndexedDB yedeğine düşülür
    const res = await fetch(`${apiBase()}/api/decks/${encodeURIComponent(id)}?format=json`, {
      headers: { Accept: 'application/json' },
      signal: typeof AbortSignal !== 'undefined' && 'timeout' in AbortSignal ? AbortSignal.timeout(20000) : undefined,
    });
    if (!res.ok) return null;
    const data = await res.json();
    const deck = data?.deck;
    if (deck && Array.isArray(deck.slides) && deck.slides.length > 0) return deck as T;
  } catch (err) {
    console.warn(`[DeckStore] API yedeği başarısız (${id}):`, err);
  }
  return null;
}

/** Bir destenin tam içeriğini (slaytlarla) yükler; ağ hatasında IndexedDB çevrimdışı yedeğine düşer. */
export function loadDeck<T = any>(id: string): Promise<T | null> {
  let p = cache.get(id);
  if (p) {
    touchDeckCache(id, p);
    return p as Promise<T | null>;
  }
  const loader = loaders[`./decks/items/${safe(id)}.json`];
  p = (async () => {
    // 0. Panelden değiştirilen deste paketteki kopyadan yenidir: önce sunucudan
    await contentReady();
    if (isContentChanged('decks', id) && (typeof navigator === 'undefined' || navigator.onLine) && !cevrimdisiGibi()) {
      const fresh = await loadFromApi<T>(id);
      if (fresh) return fresh;
    }

    // 1. Önce Vite derlenmiş modülünü dene (RAM / hızlı chunk)
    if (loader) {
      try {
        const res = await loader();
        if (res) return res;
      } catch (_) {}
    }

    // 2. Cihaz hafızasındaki (IndexedDB) tam desteye bak (< 5ms - sıfır ağ gecikmesi)
    try {
      const fromDb = await loadFromIndexedDb(id);
      if (fromDb) return fromDb;
    } catch (_) {}

    // 3. Cihazda yoksa ve internete bağlıysak sunucudan dene (Wi-Fi bağlı ama internetsizse beklemeden geç)
    if ((typeof navigator === 'undefined' || navigator.onLine) && !cevrimdisiGibi()) {
      try {
        const viaApi = await loadFromApi<T>(id);
        if (viaApi) return viaApi;
      } catch (_) {}
    }

    return null;
  })();
  touchDeckCache(id, p);
  // Başarısız yükleme önbellekte kalmasın: bağlantı dönünce aynı deste yeniden denenebilsin
  p.then((v) => { if (!v) cache.delete(id); }, () => cache.delete(id));
  return p as Promise<T | null>;
}

/** Derlemede ayrıştırılmış hafif ders kartları listesini (~300 KB) tek parçada yükler (118 desteyi indirmeden). */
export async function loadDeckFlashcards(): Promise<any[] | null> {
  const fn = Object.values(flashcardModules)[0];
  if (!fn) return null;
  try {
    const list = await fn();
    return Array.isArray(list) ? list : null;
  } catch {
    return null;
  }
}

/** Tüm desteleri sırayla yükler; her desteden sonra ana iş parçacığına nefes aldırır. */
export async function loadAllDecks<T = any>(): Promise<T[]> {
  await loadDeckCatalog();
  // 4'erli gruplar (sıra korunur): internetsizken cihazda olmayan desteler hızlıca boş döner, yalnız inmiş olanlar gelir
  const out: T[] = [];
  for (let i = 0; i < DECK_CATALOG.length; i += 4) {
    const grup = await Promise.all(DECK_CATALOG.slice(i, i + 4).map((d) => loadDeck<T>(d.id).catch(() => null)));
    for (const full of grup) if (full) out.push(full);
    await new Promise((r) => setTimeout(r, 0));
  }
  return out;
}

/** Ekranda gösterilecek ders adı: iç etiketler ("(Yeni Mikro-Ders)") ayıklanır. */
export const deckName = (d: { title?: string; shortTitle?: string }, short = true) =>
  String((short && d.shortTitle) || d.title || '')
    .replace(/\s*\((?:yeni\s*)?mikro[-\s]?ders\)\s*/gi, ' ')
    .replace(/\s{2,}/g, ' ')
    .trim();

/** Değişen destelerin liste bilgisini (başlık, ders…) sunucudan alıp DECK_CATALOG'u yerinde günceller. */
async function patchCatalog(ids: string[]) {
  if (!ids.length) return;
  try {
    await loadDeckCatalog();
    const res = await fetch(`${apiBase()}/api/content/deck-catalog?ids=${encodeURIComponent(ids.join(','))}`, { cache: 'no-store' });
    if (!res.ok) return;
    const { decks } = (await res.json()) as { decks: DeckCatalogEntry[] };
    for (const d of decks || []) {
      const i = DECK_CATALOG.findIndex((x) => x.id === d.id);
      if (i >= 0) DECK_CATALOG[i] = d;
      else DECK_CATALOG.push(d);
    }
  } catch { /* çevrimdışı: paketteki liste kalır */ }
}

/** Panel değişikliği: önbellek düşer, liste güncellenir, açık ekranlar `medsoru:decks-changed` ile tazelenir. */
function announce(ids: string[]) {
  ids.forEach((id) => cache.delete(id));
  void patchCatalog(ids).then(() => {
    if (typeof window !== 'undefined') window.dispatchEvent(new CustomEvent('medsoru:decks-changed', { detail: { ids } }));
  });
}
// Modül grafiği (contentLive ↔ api ↔ deckStore döngüsü) yüklenince kaydol
if (typeof window !== 'undefined') setTimeout(() => {
  void contentReady(8000).then(() => { const ids = changedIds('decks'); if (ids.length) announce(ids); });
  onContentChanged('decks', (ids) => announce(ids.length ? ids : changedIds('decks')));
}, 0);
