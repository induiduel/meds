/**
 * src/services/clientCache.ts
 *
 * Akıllı İstemci Tarafı Önbellekleme, Stale-While-Revalidate (SWR)
 * ve Koşullu Veri Çekme Motoru.
 *
 * Temel Özellikler:
 * 1. L1 In-Memory Cache: 0-1 ms içinde mikrosaniye düzeyinde anında erişim.
 * 2. L2 IndexedDB Persistent Cache: Uygulama veya tarayıcı kapatılıp açılsa bile
 *    verilerin cihazda kalıcı olmasını sağlar.
 * 3. Stale-While-Revalidate (SWR): Taze veri varsa internete hiç gitmez. Bayat veri
 *    varsa anında kullanıcıya sunar, arka planda sessizce revalidate eder.
 * 4. Conditional Request / ETag Tracking: Sunucudan dönen ETag ve son güncelleme
 *    damgalarını saklar; 304 Not Modified durumunda 0 bayt veri aktarımı sağlar.
 * 5. Event-Driven Push Desteği: WebSocket / Supabase Realtime olaylarında doğrudan
 *    bellekteki ve IndexedDB'deki veriyi günceller (in-place update), gereksiz
 *    yeniden çekmeleri (refetch storm) önler.
 */

const DB_NAME = 'medsoru_client_cache_db';
const DB_VERSION = 1;
const STORE_CACHE = 'kv_cache';
const STORE_ETAG = 'etag_meta';

export interface CacheEntry<T = any> {
  key: string;
  data: T;
  timestamp: number;
  etag?: string;
  tag?: string;
}

export interface ETagEntry {
  url: string;
  etag: string;
  timestamp: number;
  cachedResponse?: any;
}

export interface CacheOptions<T = any> {
  /** Verinin taze (fresh) sayıldığı süre (ms). Bu süre içinde internete HİÇBİR istek atılmaz. Varsayılan: 5 dakika (300.000 ms) */
  ttlMs?: number;
  /** Verinin bayat ama anında gösterilebilir kabul edildiği süre (ms). Varsayılan: 24 saat */
  staleMs?: number;
  /** Zorla yenileme (önbelleği yok sayıp doğrudan kaynaktan çek) */
  forceRefresh?: boolean;
  /** Gruplama etiketi (toplu geçersiz kılma için örn. 'questions', 'committees', 'summaries') */
  tag?: string;
  /** Arka planda SWR ile yeni veri geldiğinde tetiklenen geri çağırım */
  onBackgroundUpdate?: (freshData: T) => void;
}

class ClientCacheService {
  private memoryCache = new Map<string, CacheEntry>();
  private etagMemory = new Map<string, ETagEntry>();
  private dbPromise: Promise<IDBDatabase | null> | null = null;
  private pendingFetches = new Map<string, Promise<any>>();
  private realtimeActiveTags = new Set<string>();
  private activeRevalidations = new Set<string>();
  private readonly MAX_MEMORY_ENTRIES = 250;

  private setMemoryEntry(key: string, entry: CacheEntry) {
    if (this.memoryCache.size >= this.MAX_MEMORY_ENTRIES && !this.memoryCache.has(key)) {
      const oldestKey = this.memoryCache.keys().next().value;
      if (oldestKey !== undefined) this.memoryCache.delete(oldestKey);
    }
    this.memoryCache.set(key, entry);
  }

  constructor() {
    if (typeof window !== 'undefined') {
      this.initDb().catch((err) => {
        console.warn('[ClientCache] IndexedDB init warning, using memory cache:', err);
      });
    }
  }

  private async initDb(): Promise<IDBDatabase | null> {
    if (typeof window === 'undefined' || !('indexedDB' in window)) {
      return null;
    }
    if (this.dbPromise) return this.dbPromise;

    this.dbPromise = new Promise((resolve) => {
      try {
        const req = window.indexedDB.open(DB_NAME, DB_VERSION);
        req.onupgradeneeded = (e: IDBVersionChangeEvent) => {
          const db = (e.target as IDBOpenDBRequest).result;
          if (!db.objectStoreNames.contains(STORE_CACHE)) {
            const store = db.createObjectStore(STORE_CACHE, { keyPath: 'key' });
            store.createIndex('by_tag', 'tag', { unique: false });
            store.createIndex('by_timestamp', 'timestamp', { unique: false });
          }
          if (!db.objectStoreNames.contains(STORE_ETAG)) {
            db.createObjectStore(STORE_ETAG, { keyPath: 'url' });
          }
        };

        req.onsuccess = (e) => {
          const db = (e.target as IDBOpenDBRequest).result;
          resolve(db);
        };

        req.onerror = () => {
          console.warn('[ClientCache] IndexedDB error, falling back to memory');
          resolve(null);
        };
      } catch (err) {
        console.warn('[ClientCache] IndexedDB exception:', err);
        resolve(null);
      }
    });

    return this.dbPromise;
  }

  /**
   * Realtime bağlantısı aktif olan bir etiket kaydeder (örn. 'questions').
   * Realtime push bağlıyken verinin bayatlaması önlenir ve gereksiz HTTP istekleri engellenir.
   */
  public setRealtimeActive(tag: string, active: boolean) {
    if (active) {
      this.realtimeActiveTags.add(tag);
    } else {
      this.realtimeActiveTags.delete(tag);
    }
  }

  public isRealtimeActive(tag?: string): boolean {
    if (!tag) return false;
    return this.realtimeActiveTags.has(tag);
  }

  /**
   * Bellekten (L1) veya IndexedDB'den (L2) anında önbellek kaydını getirir.
   */
  public async get<T = any>(key: string): Promise<CacheEntry<T> | null> {
    // 1. L1 Memory Cache (0 ms) - LRU terfisi
    if (this.memoryCache.has(key)) {
      const entry = this.memoryCache.get(key) as CacheEntry<T>;
      this.memoryCache.delete(key);
      this.memoryCache.set(key, entry);
      return entry;
    }

    // 2. L2 IndexedDB Cache
    const db = await this.initDb();
    if (!db) return null;

    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_CACHE, 'readonly');
        const store = tx.objectStore(STORE_CACHE);
        const req = store.get(key);
        req.onsuccess = () => {
          const res = req.result as CacheEntry<T> | undefined;
          if (res) {
            // Memory cache'e terfi ettir
            this.setMemoryEntry(key, res);
            resolve(res);
          } else {
            resolve(null);
          }
        };
        req.onerror = () => resolve(null);
      } catch {
        resolve(null);
      }
    });
  }

  /**
   * Hem L1 (bellek) hem de L2 (IndexedDB) katmanına atomik veri kaydeder.
   */
  public async set<T = any>(key: string, data: T, options: { tag?: string; etag?: string } = {}): Promise<void> {
    const entry: CacheEntry<T> = {
      key,
      data,
      timestamp: Date.now(),
      tag: options.tag,
      etag: options.etag,
    };

    // L1 Memory (LRU korumalı)
    this.setMemoryEntry(key, entry);

    // L2 IndexedDB (Arka planda asenkron)
    this.saveToIndexedDb(entry).catch(() => {});
  }

  private async saveToIndexedDb(entry: CacheEntry): Promise<void> {
    const db = await this.initDb();
    if (!db) return;

    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_CACHE, 'readwrite');
        const store = tx.objectStore(STORE_CACHE);
        store.put(entry);
        tx.oncomplete = () => resolve();
        tx.onerror = () => resolve();
      } catch {
        resolve();
      }
    });
  }

  /**
   * Stale-While-Revalidate Mantığıyla Veri Getirici:
   * - Taze veri varsa (TTL dolmamışsa): 0 ms'de önbellekten döner, sunucuya HİÇBİR İSTEK ATMAZ.
   * - Bayat veri varsa (Stale): Anında bayat veriyi döner, kullanıcıyı bekletmez.
   *   Arka planda sunucuya istek atar, veriyi günceller ve onBackgroundUpdate ile haber verir.
   * - Veri hiç yoksa veya forceRefresh istenmişse: Sunucudan çeker, önbelleğe yazar ve döner.
   */
  public async fetchWithCache<T = any>(
    key: string,
    fetcher: () => Promise<T>,
    options: CacheOptions<T> = {}
  ): Promise<T> {
    const ttlMs = options.ttlMs ?? 5 * 60 * 1000; // 5 dakika varsayılan
    const staleMs = options.staleMs ?? 24 * 60 * 60 * 1000; // 24 saat varsayılan
    const now = Date.now();

    // 1. Önbelleği kontrol et
    if (!options.forceRefresh) {
      const cached = await this.get<T>(key);
      if (cached) {
        const age = now - cached.timestamp;
        const isPushActive = options.tag ? this.isRealtimeActive(options.tag) : false;

        // A) Veri taze mi VEYA Realtime Push açık mı?
        // Realtime açıkken sunucudaki her değişiklik push ile geldiğinden veri her zaman tazedir!
        if (age < ttlMs || isPushActive) {
          return cached.data;
        }

        // B) Veri bayat ama kullanılabilir mi? (Stale-While-Revalidate)
        if (age < staleMs) {
          // Anında bayat veriyi dön, kullanıcı beklemesin!
          // Arka planda sessizce taze veriyi çek
          this.triggerBackgroundRevalidate(key, fetcher, options);
          return cached.data;
        }
      }
    }

    // 2. Önbellekte yoksa veya süre dolmuşsa doğrudan fetch yap
    // Çift istek fırtınasını (duplicate request storm) önlemek için pending fetch birleştirme
    return this.deduplicatedFetch(key, fetcher, options);
  }

  private deduplicatedFetch<T>(key: string, fetcher: () => Promise<T>, options: CacheOptions<T>): Promise<T> {
    if (this.pendingFetches.has(key)) {
      return this.pendingFetches.get(key) as Promise<T>;
    }

    const p = (async () => {
      try {
        const result = await fetcher();
        if (result !== undefined && result !== null) {
          await this.set(key, result, { tag: options.tag });
        }
        return result;
      } finally {
        this.pendingFetches.delete(key);
      }
    })();

    this.pendingFetches.set(key, p);
    return p;
  }

  private triggerBackgroundRevalidate<T>(key: string, fetcher: () => Promise<T>, options: CacheOptions<T>) {
    if (this.pendingFetches.has(key)) return;

    const revalidate = async () => {
      try {
        const fresh = await fetcher();
        if (fresh !== undefined && fresh !== null) {
          await this.set(key, fresh, { tag: options.tag });
          options.onBackgroundUpdate?.(fresh);
        }
      } catch (err) {
        console.warn(`[ClientCache] Arka plan revalidate başarısız (${key}):`, err);
      } finally {
        this.pendingFetches.delete(key);
      }
    };

    // Tarayıcı boşta (idle) olduğunda çalıştır
    if (typeof window !== 'undefined' && 'requestIdleCallback' in window) {
      (window as any).requestIdleCallback(() => {
        this.pendingFetches.set(key, revalidate());
      }, { timeout: 10000 });
    } else {
      setTimeout(() => {
        this.pendingFetches.set(key, revalidate());
      }, 500);
    }
  }

  /**
   * Belirli bir anahtarı veya etikete ait tüm kayıtları bellek ve diskten siler.
   */
  public async invalidate(keyOrTag: string): Promise<void> {
    // 1. Memory'den temizle
    if (this.memoryCache.has(keyOrTag)) {
      this.memoryCache.delete(keyOrTag);
    }
    for (const [k, v] of this.memoryCache.entries()) {
      if (v.tag === keyOrTag) {
        this.memoryCache.delete(k);
      }
    }

    // 2. IndexedDB'den temizle
    const db = await this.initDb();
    if (!db) return;

    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_CACHE, 'readwrite');
        const store = tx.objectStore(STORE_CACHE);
        // Önce doğrudan key olarak dene
        store.delete(keyOrTag);

        // Sonra index üstünden tag olarak ara
        if (store.indexNames.contains('by_tag')) {
          const tagIdx = store.index('by_tag');
          const req = tagIdx.openCursor(IDBKeyRange.only(keyOrTag));
          req.onsuccess = (e) => {
            const cursor = (e.target as IDBRequest).result as IDBCursorWithValue | null;
            if (cursor) {
              cursor.delete();
              cursor.continue();
            }
          };
        }
        tx.oncomplete = () => resolve();
        tx.onerror = () => resolve();
      } catch {
        resolve();
      }
    });
  }

  /**
   * Önbellekteki bir dizi öğesini yerinde günceller (Push/Realtime mutasyonları için).
   */
  public async updateItemInList<T = any>(
    key: string,
    predicate: (item: T) => boolean,
    updater: (item: T) => T,
    insertIfMissing?: T
  ): Promise<void> {
    const entry = await this.get<T[]>(key);
    if (!entry || !Array.isArray(entry.data)) {
      if (insertIfMissing) {
        await this.set(key, [insertIfMissing]);
      }
      return;
    }

    const list = [...entry.data];
    const idx = list.findIndex(predicate);
    if (idx >= 0) {
      list[idx] = updater(list[idx]);
    } else if (insertIfMissing) {
      list.push(insertIfMissing);
    }

    await this.set(key, list, { tag: entry.tag, etag: entry.etag });
  }

  /**
   * Önbellekteki bir listeden öğe siler.
   */
  public async removeItemFromList<T = any>(
    key: string,
    predicate: (item: T) => boolean
  ): Promise<void> {
    const entry = await this.get<T[]>(key);
    if (!entry || !Array.isArray(entry.data)) return;

    const filtered = entry.data.filter((item) => !predicate(item));
    await this.set(key, filtered, { tag: entry.tag, etag: entry.etag });
  }

  // ================= ETag & Koşullu İstek (Conditional HTTP) Yönetimi =================

  public getStoredETag(url: string): ETagEntry | null {
    return this.etagMemory.get(url) || null;
  }

  public setStoredETag(url: string, etag: string, cachedResponse?: any) {
    const entry: ETagEntry = {
      url,
      etag,
      timestamp: Date.now(),
      cachedResponse,
    };
    this.etagMemory.set(url, entry);

    // IndexedDB'ye de yaz
    this.saveETagToIndexedDb(entry).catch(() => {});
  }

  private async saveETagToIndexedDb(entry: ETagEntry): Promise<void> {
    const db = await this.initDb();
    if (!db || !db.objectStoreNames.contains(STORE_ETAG)) return;

    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_ETAG, 'readwrite');
        tx.objectStore(STORE_ETAG).put(entry);
        tx.oncomplete = () => resolve();
        tx.onerror = () => resolve();
      } catch {
        resolve();
      }
    });
  }

  // ================= Cache-Aside ile Versiyon Hash Kontrolü (5. Madde) =================

  private versionHashesPromise: Promise<Record<string, string> | null> | null = null;
  private versionHashesTimestamp = 0;

  /**
   * Sunucudan ~200 baytlık versiyon hash özetini çeker (60 saniye boyunca bellek içi saklar).
   */
  public async fetchServerVersionHashes(): Promise<Record<string, string> | null> {
    const now = Date.now();
    if (this.versionHashesPromise && now - this.versionHashesTimestamp < 60000) {
      return this.versionHashesPromise;
    }

    this.versionHashesTimestamp = now;
    this.versionHashesPromise = (async () => {
      try {
        const res = await fetch('/api/version-hashes');
        if (!res.ok) return null;
        return (await res.json()) as Record<string, string>;
      } catch (err) {
        console.warn('[ClientCache] /api/version-hashes alınamadı:', err);
        return null;
      }
    })();

    return this.versionHashesPromise;
  }

  /**
   * 5. Madde: Kalıcı İstemci Depolama (IndexedDB ile Cache-Aside ve Version Hash)
   * 1. Uygulama açılışta önce IndexedDB kontrolü yapar. Veri yerelde varsa ekrana ANINDA basılır (0ms).
   * 2. Sunucuya yalnızca verinin versiyon kontrolü (version_hash) sorulur (/api/version-hashes).
   * 3. Versiyon aynıysa YENİ VERİ İNDİRİLMEZ (megabaytlarca veri ve ağ bant genişliği tasarrufu).
   * 4. Versiyon değişmişse arka planda yeni veri indirilir, IndexedDB güncellenir ve onBackgroundUpdate tetiklenir.
   */
  public async fetchWithCacheAsideVersion<T = any>(
    key: string,
    entityName: string,
    fetcher: () => Promise<T>,
    options: {
      tag?: string;
      onBackgroundUpdate?: (freshData: T) => void;
    } = {}
  ): Promise<T> {
    // 1. Önce IndexedDB / Memory kontrolü yap
    const cached = await this.get<T>(key);
    if (cached && cached.data !== undefined && cached.data !== null) {
      // Ekrana anında bas!
      // Arka planda versiyon hash kontrolü yap
      this.revalidateWithVersionHash(key, entityName, cached.etag, fetcher, options);
      return cached.data;
    }

    // 2. Önbellekte yoksa ilk yüklemeyi yap
    return this.deduplicatedFetch(key, async () => {
      const data = await fetcher();
      const hashes = await this.fetchServerVersionHashes();
      const currentHash = hashes ? (hashes as any)[entityName] : undefined;
      await this.set(key, data, { tag: options.tag, etag: currentHash });
      return data;
    }, options);
  }

  private revalidateWithVersionHash<T>(
    key: string,
    entityName: string,
    cachedEtag: string | undefined,
    fetcher: () => Promise<T>,
    options: { tag?: string; onBackgroundUpdate?: (freshData: T) => void }
  ) {
    if (this.activeRevalidations.has(key)) return;
    this.activeRevalidations.add(key);

    const check = async () => {
      try {
        const hashes = await this.fetchServerVersionHashes();
        if (!hashes) return;
        const currentHash = (hashes as any)[entityName];
        if (!currentHash) return;

        // Versiyon aynıysa: YENİ VERİ İNDİRME!
        if (cachedEtag && cachedEtag === currentHash) {
          return;
        }

        // Versiyon değişmiş: yeni veriyi çek ve güncelle
        const fresh = await fetcher();
        if (fresh !== undefined && fresh !== null) {
          await this.set(key, fresh, { tag: options.tag, etag: currentHash });
          options.onBackgroundUpdate?.(fresh);
        }
      } catch (err) {
        console.warn(`[ClientCache] revalidateWithVersionHash (${entityName}) hatası:`, err);
      } finally {
        this.activeRevalidations.delete(key);
      }
    };

    if (typeof window !== 'undefined' && 'requestIdleCallback' in window) {
      (window as any).requestIdleCallback(() => void check(), { timeout: 10000 });
    } else {
      setTimeout(() => void check(), 1000);
    }
  }
}

export const clientCache = new ClientCacheService();
