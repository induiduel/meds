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
const catalogModules = import.meta.glob('./decks/catalog.json', { eager: true, import: 'default' }) as Record<string, unknown>;
export const DECK_CATALOG = ((Object.values(catalogModules)[0] as DeckCatalogEntry[] | undefined) || []);

const loaders = import.meta.glob('./decks/items/*.json', { import: 'default' }) as Record<string, () => Promise<any>>;
const safe = (id: string) => id.replace(/[^a-zA-Z0-9_-]+/g, '_');
const cache = new Map<string, Promise<any>>();

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

/** Bir destenin tam içeriğini (slaytlarla) yükler; ağ hatasında IndexedDB çevrimdışı yedeğine düşer. */
export function loadDeck<T = any>(id: string): Promise<T | null> {
  let p = cache.get(id);
  if (!p) {
    const loader = loaders[`./decks/items/${safe(id)}.json`];
    p = (async () => {
      try {
        if (loader) {
          const res = await loader();
          if (res) return res;
        }
      } catch (err) {
        console.warn(`[DeckStore] Modül yüklenemedi (${id}), çevrimdışı veritabanı deneniyor:`, err);
      }
      return await loadFromIndexedDb(id);
    })();
    cache.set(id, p);
  }
  return p as Promise<T | null>;
}

/** Tüm desteleri sırayla yükler; her desteden sonra ana iş parçacığına nefes aldırır. */
export async function loadAllDecks<T = any>(): Promise<T[]> {
  const out: T[] = [];
  for (const d of DECK_CATALOG) {
    const full = await loadDeck<T>(d.id);
    if (full) out.push(full);
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
