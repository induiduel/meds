/**
 * src/services/pastQuestionsCache.ts
 *
 * Yüksek Performanslı İstemci Tarafı Soru Önbelleği (Client-Side Storage)
 * ve Artımlı/Soru Bazında Senkronizasyon Motoru (Incremental Delta Sync).
 *
 * Neden Çerezler (Cookies) Yerine IndexedDB?
 * - Çerezlerin domain başına en fazla 4 KB limiti vardır. 1937 soru ~7.1 MB tutmaktadır
 *   (çerez sınırının 1700 katından fazla).
 * - Çerezler her HTTP isteğinde sunucuya tekrar tekrar gönderilir ve bant genişliğini tüketir.
 * - IndexedDB ise tarayıcının yerel, asenkron ve yüksek kapasiteli (yüzlerce MB) veritabanıdır;
 *   ana iş parçacığını (UI thread) dondurmaz ve sıfır ağ gecikmesi ile 10-20 ms içinde açılır.
 *
 * Çalışma Prensibi:
 * 1. Site Açılışı (< 20ms): Sorular doğrudan cihazın IndexedDB hafızasından okunur ve
 *    kullanıcıya anında sunulur. Sunucu / veritabanı beklenmez, bekleme süresi sıfırdır.
 * 2. Arka Planda Delta Senkronizasyon (Ekonomik Kontrol):
 *    - Veritabanına yalnızca son güncelleme zamanı ve toplam sayı sorulur (~100 bayt).
 *    - Eğer değişiklik yoksa 0 soru indirilir, kota harcanmaz.
 *    - Eğer 1 veya birkaç soru güncellenmişse, YALNIZCA güncellenen o soru(lar) çekilir
 *      ve yerel IndexedDB güncellenir. Tüm sorular baştan çekilmez.
 */

import { QuestionItem } from '../types';
import { SupabaseDbService } from './supabaseDb';

function getCustomApiUrl(): string {
  if (typeof window === 'undefined' || !window.localStorage) return '';
  const url = localStorage.getItem('medsoru_custom_api_url') || '';
  if (url && (url.includes('github.io') || url.includes('github.com'))) return '';
  return url.trim().replace(/\/$/, '');
}

const DB_NAME = 'medsoru_past_questions_db';
const DB_VERSION = 1;
const STORE_QUESTIONS = 'past_questions';
const STORE_META = 'metadata';

const KEY_LAST_SYNC = 'last_sync_timestamp';
const KEY_TOTAL_COUNT = 'last_sync_count';
const KEY_SYNC_SOURCE = 'last_sync_source';

export interface CacheSyncStatus {
  isSyncing: boolean;
  totalCached: number;
  lastSyncTime: string | null;
  lastSyncDeltaCount: number;
  source: 'indexeddb' | 'memory' | 'unsupported';
  isUpToDate: boolean;
  statusMessage: string;
}

export type CacheListener = (status: CacheSyncStatus, updatedQuestions?: QuestionItem[]) => void;

class PastQuestionsCacheService {
  private dbPromise: Promise<IDBDatabase | null> | null = null;
  private memoryMap = new Map<string, QuestionItem>();
  private memoryMeta = new Map<string, any>();
  private isMemoryInitialized = false;
  private listeners: Set<CacheListener> = new Set();
  private syncInProgress = false;

  private currentStatus: CacheSyncStatus = {
    isSyncing: false,
    totalCached: 0,
    lastSyncTime: null,
    lastSyncDeltaCount: 0,
    source: 'indexeddb',
    isUpToDate: false,
    statusMessage: 'Önbellek başlatılıyor...',
  };

  constructor() {
    if (typeof window !== 'undefined') {
      // Lazy init on browser start
      this.initDb().catch((err) => {
        console.warn('[PastQuestionsCache] IndexedDB init warning, using memory fallback:', err);
      });
    }
  }

  /**
   * IndexedDB Bağlantısını Başlat
   */
  private async initDb(): Promise<IDBDatabase | null> {
    if (typeof window === 'undefined' || !('indexedDB' in window)) {
      this.currentStatus.source = 'memory';
      return null;
    }

    if (this.dbPromise) return this.dbPromise;

    this.dbPromise = new Promise((resolve) => {
      try {
        const req = window.indexedDB.open(DB_NAME, DB_VERSION);

        req.onupgradeneeded = (e: IDBVersionChangeEvent) => {
          const db = (e.target as IDBOpenDBRequest).result;
          if (!db.objectStoreNames.contains(STORE_QUESTIONS)) {
            const qStore = db.createObjectStore(STORE_QUESTIONS, { keyPath: 'id' });
            qStore.createIndex('by_committee', 'committeeId', { unique: false });
            qStore.createIndex('by_discipline', 'discipline', { unique: false });
            qStore.createIndex('by_updatedAt', 'updatedAt', { unique: false });
          }
          if (!db.objectStoreNames.contains(STORE_META)) {
            db.createObjectStore(STORE_META, { keyPath: 'key' });
          }
        };

        req.onsuccess = (e) => {
          const db = (e.target as IDBOpenDBRequest).result;
          this.currentStatus.source = 'indexeddb';
          resolve(db);
        };

        req.onerror = (e) => {
          console.warn('[PastQuestionsCache] IndexedDB error, falling back to memory:', e);
          this.currentStatus.source = 'memory';
          resolve(null);
        };
      } catch (err) {
        console.warn('[PastQuestionsCache] IndexedDB exception, falling back to memory:', err);
        this.currentStatus.source = 'memory';
        resolve(null);
      }
    });

    return this.dbPromise;
  }

  /**
   * Dinleyici ekle (UI bileşenleri anlık bildirim için)
   */
  public subscribe(listener: CacheListener): () => void {
    this.listeners.add(listener);
    listener(this.currentStatus);
    return () => this.listeners.delete(listener);
  }

  private notifyListeners(updatedQuestions?: QuestionItem[]) {
    this.currentStatus.totalCached = this.memoryMap.size;
    for (const listener of this.listeners) {
      try {
        listener({ ...this.currentStatus }, updatedQuestions);
      } catch (e) {
        console.warn('[PastQuestionsCache] Listener error:', e);
      }
    }
  }

  /**
   * Cihaz hafızasındaki (IndexedDB) tüm çıkmış soruları getirir (< 20ms)
   */
  public async getCachedQuestions(): Promise<QuestionItem[]> {
    if (this.isMemoryInitialized && this.memoryMap.size > 0) {
      return Array.from(this.memoryMap.values());
    }

    const db = await this.initDb();
    if (!db) {
      return Array.from(this.memoryMap.values());
    }

    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_QUESTIONS, 'readonly');
        const store = tx.objectStore(STORE_QUESTIONS);
        const req = store.getAll();

        req.onsuccess = () => {
          const items: QuestionItem[] = req.result || [];
          this.memoryMap.clear();
          for (const item of items) {
            if (item && item.id) {
              this.memoryMap.set(item.id, item);
            }
          }
          this.isMemoryInitialized = true;
          this.currentStatus.totalCached = this.memoryMap.size;
          resolve(items);
        };

        req.onerror = () => {
          resolve(Array.from(this.memoryMap.values()));
        };
      } catch (err) {
        resolve(Array.from(this.memoryMap.values()));
      }
    });
  }

  /**
   * Tek bir soruyu ID ile önbellekten çek
   */
  public async getCachedQuestionById(id: string): Promise<QuestionItem | null> {
    if (this.memoryMap.has(id)) {
      return this.memoryMap.get(id) || null;
    }
    const db = await this.initDb();
    if (!db) return null;

    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_QUESTIONS, 'readonly');
        const store = tx.objectStore(STORE_QUESTIONS);
        const req = store.get(id);
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => resolve(null);
      } catch {
        resolve(null);
      }
    });
  }

  /**
   * Tek bir soruyu cihaz hafızasına kaydet veya güncelle
   */
  public async saveQuestion(question: QuestionItem): Promise<void> {
    if (!question || !question.id) return;
    this.memoryMap.set(question.id, question);

    const db = await this.initDb();
    if (db) {
      await new Promise<void>((resolve) => {
        try {
          const tx = db.transaction([STORE_QUESTIONS, STORE_META], 'readwrite');
          const qStore = tx.objectStore(STORE_QUESTIONS);
          qStore.put(question);

          tx.oncomplete = () => resolve();
          tx.onerror = () => resolve();
        } catch {
          resolve();
        }
      });
    }

    this.notifyListeners([question]);
  }

  /**
   * Çoklu soruları toplu şekilde IndexedDB'ye yaz (Batch Transaction)
   */
  public async saveBatch(questions: QuestionItem[]): Promise<void> {
    if (!questions || questions.length === 0) return;

    for (const q of questions) {
      if (q && q.id) {
        this.memoryMap.set(q.id, q);
      }
    }
    this.isMemoryInitialized = true;

    const db = await this.initDb();
    if (!db) {
      this.notifyListeners(questions);
      return;
    }

    // Parça parça (500'lük gruplar halinde) yazarak tarayıcı transaction zaman aşımını önle
    const CHUNK_SIZE = 500;
    for (let i = 0; i < questions.length; i += CHUNK_SIZE) {
      const chunk = questions.slice(i, i + CHUNK_SIZE);
      await new Promise<void>((resolve) => {
        try {
          const tx = db.transaction(STORE_QUESTIONS, 'readwrite');
          const store = tx.objectStore(STORE_QUESTIONS);
          for (const item of chunk) {
            store.put(item);
          }
          tx.oncomplete = () => resolve();
          tx.onerror = () => resolve();
        } catch {
          resolve();
        }
      });
    }

    this.notifyListeners(questions);
  }

  /**
   * Silinen soruları cihaz hafızasından kaldır
   */
  public async removeQuestions(ids: string[]): Promise<void> {
    if (!ids || ids.length === 0) return;

    for (const id of ids) {
      this.memoryMap.delete(id);
    }

    const db = await this.initDb();
    if (db) {
      await new Promise<void>((resolve) => {
        try {
          const tx = db.transaction(STORE_QUESTIONS, 'readwrite');
          const store = tx.objectStore(STORE_QUESTIONS);
          for (const id of ids) {
            store.delete(id);
          }
          tx.oncomplete = () => resolve();
          tx.onerror = () => resolve();
        } catch {
          resolve();
        }
      });
    }

    this.notifyListeners();
  }

  /**
   * Meta veri oku
   */
  public async getMeta<T>(key: string): Promise<T | null> {
    if (this.memoryMeta.has(key)) {
      return this.memoryMeta.get(key) as T;
    }

    // Fallback to localStorage for quick sync check
    if (typeof window !== 'undefined' && window.localStorage) {
      const lsVal = localStorage.getItem(`medsoru_meta_${key}`);
      if (lsVal) {
        try {
          const parsed = JSON.parse(lsVal);
          this.memoryMeta.set(key, parsed);
          return parsed;
        } catch {}
      }
    }

    const db = await this.initDb();
    if (!db) return null;

    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_META, 'readonly');
        const store = tx.objectStore(STORE_META);
        const req = store.get(key);
        req.onsuccess = () => {
          const val = req.result ? req.result.value : null;
          if (val !== null) this.memoryMeta.set(key, val);
          resolve(val);
        };
        req.onerror = () => resolve(null);
      } catch {
        resolve(null);
      }
    });
  }

  /**
   * Meta veri kaydet
   */
  public async setMeta<T>(key: string, value: T): Promise<void> {
    this.memoryMeta.set(key, value);

    if (typeof window !== 'undefined' && window.localStorage) {
      try {
        localStorage.setItem(`medsoru_meta_${key}`, JSON.stringify(value));
      } catch {}
    }

    const db = await this.initDb();
    if (!db) return;

    await new Promise<void>((resolve) => {
      try {
        const tx = db.transaction(STORE_META, 'readwrite');
        const store = tx.objectStore(STORE_META);
        store.put({ key, value });
        tx.oncomplete = () => resolve();
        tx.onerror = () => resolve();
      } catch {
        resolve();
      }
    });
  }

  public async getLastSyncTime(): Promise<string | null> {
    return this.getMeta<string>(KEY_LAST_SYNC);
  }

  public async setLastSyncTime(time: string, count?: number): Promise<void> {
    await this.setMeta(KEY_LAST_SYNC, time);
    if (count !== undefined) {
      await this.setMeta(KEY_TOTAL_COUNT, count);
    }
  }

  /**
   * Önbelleği tamamen temizle
   */
  public async clearCache(): Promise<void> {
    this.memoryMap.clear();
    this.memoryMeta.clear();
    this.isMemoryInitialized = false;

    if (typeof window !== 'undefined' && window.localStorage) {
      try {
        localStorage.removeItem(`medsoru_meta_${KEY_LAST_SYNC}`);
        localStorage.removeItem(`medsoru_meta_${KEY_TOTAL_COUNT}`);
      } catch {}
    }

    const db = await this.initDb();
    if (db) {
      await new Promise<void>((resolve) => {
        try {
          const tx = db.transaction([STORE_QUESTIONS, STORE_META], 'readwrite');
          tx.objectStore(STORE_QUESTIONS).clear();
          tx.objectStore(STORE_META).clear();
          tx.oncomplete = () => resolve();
          tx.onerror = () => resolve();
        } catch {
          resolve();
        }
      });
    }

    this.currentStatus.totalCached = 0;
    this.currentStatus.lastSyncTime = null;
    this.currentStatus.lastSyncDeltaCount = 0;
    this.currentStatus.isUpToDate = false;
    this.currentStatus.statusMessage = 'Önbellek temizlendi';
    this.notifyListeners();
  }

  /**
   * ARTIK VE EN KRİTİK FONKSİYON:
   * Soru Bazında Delta Senkronizasyon (Incremental Sync)
   *
   * 1. Veritabanına sadece `max(updated_at)` ve soru sayısını sorar (~100 Bayt).
   * 2. Değişiklik yoksa TEK BİR SORU BİLE indirmez (Sıfır veritabanı maliyeti).
   * 3. Soru bazında değişiklik varsa, YALNIZCA değişen soruları çeker ve IndexedDB'ye yazar.
   * 4. Tüm soruları asla baştan indirmez!
   */
  public async syncWithRemote(options: {
    forceFull?: boolean;
    onUpdate?: (updated: QuestionItem[]) => void;
  } = {}): Promise<{
    success: boolean;
    updatedCount: number;
    isUpToDate: boolean;
    totalCount: number;
  }> {
    if (this.syncInProgress) {
      return {
        success: true,
        updatedCount: 0,
        isUpToDate: this.currentStatus.isUpToDate,
        totalCount: this.memoryMap.size,
      };
    }

    this.syncInProgress = true;
    this.currentStatus.isSyncing = true;
    this.currentStatus.statusMessage = 'Güncellemeler kontrol ediliyor...';
    this.notifyListeners();

    try {
      // 1. Mevcut yerel soruları ve son senkronizasyon zamanını oku
      const localQuestions = await this.getCachedQuestions();
      const localCount = localQuestions.length;
      let lastSyncTime = await this.getLastSyncTime();

      // Eğer hiç soru yoksa veya zorunlu tam çekim istenmişse tam yükleme yap
      if (localCount === 0 || options.forceFull || !lastSyncTime) {
        const fullResult = await this.performInitialLoad();
        this.syncInProgress = false;
        this.currentStatus.isSyncing = false;
        this.currentStatus.isUpToDate = true;
        this.currentStatus.lastSyncDeltaCount = fullResult.length;
        this.currentStatus.statusMessage = `İlk yükleme tamamlandı: ${fullResult.length} soru cihazınıza kaydedildi.`;
        this.notifyListeners(fullResult);
        return {
          success: true,
          updatedCount: fullResult.length,
          isUpToDate: true,
          totalCount: fullResult.length,
        };
      }

      // 2. YÖNTEM A: Yerel Node.js / Express Sunucusu Kontrolü (Hızlı ve Yerel)
      const customUrl = getCustomApiUrl();
      const isGitHubPages = typeof window !== 'undefined' && window.location.hostname.includes('github.io');
      const canTryLocalServer = !isGitHubPages || Boolean(customUrl);

      if (canTryLocalServer) {
        try {
          const apiBase = customUrl || '';
          const syncUrl = `${apiBase}/api/past-exams/sync?since=${encodeURIComponent(lastSyncTime)}&count=${localCount}`;
          
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 4000);
          const res = await fetch(syncUrl, { signal: controller.signal });
          clearTimeout(timeoutId);

          if (res.ok) {
            const data = await res.json();
            if (data.upToDate) {
              this.syncInProgress = false;
              this.currentStatus.isSyncing = false;
              this.currentStatus.isUpToDate = true;
              this.currentStatus.lastSyncDeltaCount = 0;
              this.currentStatus.statusMessage = 'Cihazınız tamamen güncel (0 Bayt indirme yapıldı).';
              this.notifyListeners();
              return { success: true, updatedCount: 0, isUpToDate: true, totalCount: localCount };
            }

            if (data.updatedQuestions && Array.isArray(data.updatedQuestions) && data.updatedQuestions.length > 0) {
              await this.saveBatch(data.updatedQuestions);
              if (data.lastModified) {
                await this.setLastSyncTime(data.lastModified, data.count);
                this.currentStatus.lastSyncTime = data.lastModified;
              }
              options.onUpdate?.(data.updatedQuestions);

              this.syncInProgress = false;
              this.currentStatus.isSyncing = false;
              this.currentStatus.isUpToDate = true;
              this.currentStatus.lastSyncDeltaCount = data.updatedQuestions.length;
              this.currentStatus.statusMessage = `${data.updatedQuestions.length} adet soru cihazınızda güncellendi.`;
              this.notifyListeners(data.updatedQuestions);
              return {
                success: true,
                updatedCount: data.updatedQuestions.length,
                isUpToDate: true,
                totalCount: this.memoryMap.size,
              };
            }
          }
        } catch {
          // Yerel sunucu yanıt vermezse doğrudan Supabase delta sorgusuna geç
        }
      }

      // 3. YÖNTEM B: Supabase PostgreSQL Soru Bazında Delta Kontrolü
      try {
        const meta = await SupabaseDbService.getPastQuestionsMeta();
        if (meta && meta.count > 0) {
          const remoteLatest = meta.latestUpdatedAt;
          const remoteCount = meta.count;

          // Kontrol: Veritabanında daha yeni bir kayıt var mı?
          const isUpToDate = Boolean(
            remoteLatest &&
            lastSyncTime &&
            new Date(remoteLatest).getTime() <= new Date(lastSyncTime).getTime() &&
            remoteCount === localCount
          );

          if (isUpToDate) {
            this.syncInProgress = false;
            this.currentStatus.isSyncing = false;
            this.currentStatus.isUpToDate = true;
            this.currentStatus.lastSyncDeltaCount = 0;
            this.currentStatus.statusMessage = 'Veritabanı güncel (Yeni değişiklik yok - 0 Bayt aktarım).';
            this.notifyListeners();
            return { success: true, updatedCount: 0, isUpToDate: true, totalCount: localCount };
          }

          // Soru bazında delta: YALNIZCA son senkronizasyon tarihinden sonra güncellenenleri çek
          const deltaQuestions = await SupabaseDbService.getPastQuestionsDelta(lastSyncTime);
          
          if (deltaQuestions && deltaQuestions.length > 0) {
            await this.saveBatch(deltaQuestions);
            if (remoteLatest) {
              await this.setLastSyncTime(remoteLatest, remoteCount);
              this.currentStatus.lastSyncTime = remoteLatest;
            }
            options.onUpdate?.(deltaQuestions);

            // Silinen soru kontrolü: Yerel önbellekteki soruların Supabase senkronizasyonu eksikse
            // kazara silinmesini önlemek için doğrudan toplu silme yapmıyoruz.
            // Yerel doğrulanmış soru tabanı korunur.

            this.syncInProgress = false;
            this.currentStatus.isSyncing = false;
            this.currentStatus.isUpToDate = true;
            this.currentStatus.lastSyncDeltaCount = deltaQuestions.length;
            this.currentStatus.statusMessage = `${deltaQuestions.length} soru veritabanından çekilip güncellendi.`;
            this.notifyListeners(deltaQuestions);
            return {
              success: true,
              updatedCount: deltaQuestions.length,
              isUpToDate: true,
              totalCount: this.memoryMap.size,
            };
          } else {
            // Zaman damgası hafif ileride olsa bile delta boş ise zamanı güncelle
            if (remoteLatest) {
              await this.setLastSyncTime(remoteLatest, remoteCount);
              this.currentStatus.lastSyncTime = remoteLatest;
            }
            this.syncInProgress = false;
            this.currentStatus.isSyncing = false;
            this.currentStatus.isUpToDate = true;
            this.currentStatus.lastSyncDeltaCount = 0;
            this.currentStatus.statusMessage = 'Sorular güncel.';
            this.notifyListeners();
            return { success: true, updatedCount: 0, isUpToDate: true, totalCount: localCount };
          }
        }
      } catch (err: any) {
        console.warn('[PastQuestionsCache] Supabase delta sync error:', err);
      }

      this.syncInProgress = false;
      this.currentStatus.isSyncing = false;
      this.currentStatus.statusMessage = 'Çevrimdışı mod: Cihazınızdaki sorular gösteriliyor.';
      this.notifyListeners();
      return { success: true, updatedCount: 0, isUpToDate: false, totalCount: localCount };
    } catch (err: any) {
      this.syncInProgress = false;
      this.currentStatus.isSyncing = false;
      this.currentStatus.statusMessage = 'Senkronizasyon hatası: ' + (err.message || '');
      this.notifyListeners();
      return { success: false, updatedCount: 0, isUpToDate: false, totalCount: this.memoryMap.size };
    }
  }

  /**
   * İlk Ziyaret: Cihazda henüz soru yokken soruları çek ve IndexedDB'ye aktar
   */
  private async performInitialLoad(): Promise<QuestionItem[]> {
    this.currentStatus.statusMessage = 'Sorular ilk kez cihazınıza indiriliyor...';
    this.notifyListeners();

    let fetched: QuestionItem[] = [];

    // 1. Önce yerel Express REST API'yi dene
    try {
      const customUrl = getCustomApiUrl();
      const apiBase = customUrl || '';
      const res = await fetch(`${apiBase}/api/past-exams`);
      if (res.ok) {
        const json = await res.json();
        if (json.questions && Array.isArray(json.questions) && json.questions.length > 0) {
          fetched = json.questions;
        }
      }
    } catch {}

    // 2. Olmazsa Supabase'den çek
    if (fetched.length === 0) {
      try {
        fetched = await SupabaseDbService.getAllPastQuestions();
      } catch (err) {
        console.warn('[PastQuestionsCache] Supabase initial load error:', err);
      }
    }

    if (fetched.length > 0) {
      await this.saveBatch(fetched);

      // En yeni güncellenme tarihini tespit et
      let maxTime = new Date(0).toISOString();
      for (const q of fetched) {
        if (q.updatedAt && q.updatedAt > maxTime) {
          maxTime = q.updatedAt;
        }
      }
      if (maxTime === new Date(0).toISOString()) {
        maxTime = new Date().toISOString();
      }

      await this.setLastSyncTime(maxTime, fetched.length);
      this.currentStatus.lastSyncTime = maxTime;
      this.currentStatus.totalCached = fetched.length;
    }

    return fetched;
  }

  public getStatus(): CacheSyncStatus {
    return { ...this.currentStatus, totalCached: this.memoryMap.size };
  }
}

export const pastQuestionsCache = new PastQuestionsCacheService();
