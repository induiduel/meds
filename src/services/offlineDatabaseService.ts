/**
 * src/services/offlineDatabaseService.ts
 *
 * Tam Çevrimdışı Tıp Veritabanı ve Senkronizasyon Yöneticisi:
 * - Çıkmış sorular (5.695 soru), havuz soruları, komiteler, interaktif öğrenme desteleri,
 *   tıbbi sözlük (1.000+ terim) ve akıl kartlarını (flashcards) kullanıcının cihazına
 *   (IndexedDB + CacheStorage) tek tıkla indirir.
 * - İnternet bağlantısı sıfır olsa dahi uygulamanın %100 işlevsel çalışmasını sağlar.
 * - Çevrimdışıyken yapılan soru katkısı / oylamaları çevrimdışı işlem kuyruğunda saklar,
 *   bağlantı sağlandığında arka planda sunucuyla eşitler (Background Sync).
 */

import { QuestionItem, Committee } from '../types';
import { pastQuestionsCache } from './pastQuestionsCache';
import { loadDeck, DECK_CATALOG } from '../data/deckStore';
import { pwaService } from './pwaService';

const OFFLINE_DB_NAME = 'medsoru_offline_db';
const OFFLINE_DB_VERSION = 2;

const STORE_QUESTIONS = 'questions';
const STORE_COMMITTEES = 'committees';
const STORE_DECKS = 'decks';
const STORE_SUMMARIES = 'summaries';
const STORE_GLOSSARY = 'glossary';
const STORE_FLASHCARDS = 'flashcards';
const STORE_QUEUE = 'offline_queue';
const STORE_META = 'metadata';

const KEY_IS_DOWNLOADED = 'is_database_downloaded';
const KEY_DOWNLOAD_DATE = 'database_downloaded_at';
const KEY_STATS = 'database_stats';

export interface OfflineDbStats {
  pastQuestionsCount: number;
  poolQuestionsCount: number;
  committeesCount: number;
  decksCount: number;
  summariesCount: number;
  glossaryCount: number;
  flashcardsCount: number;
  totalItems: number;
  estimatedSizeMb: number;
  downloadedAt: string | null;
}

export interface OfflineProgress {
  stage: string;
  percent: number;
  currentCount?: number;
  totalCount?: number;
}

export interface OfflineAction {
  id?: number;
  type: 'contribute' | 'vote' | 'note' | 'feedback';
  endpoint: string;
  method: 'POST' | 'PUT' | 'DELETE';
  payload: any;
  timestamp: string;
}

export interface OfflineState {
  isOnline: boolean;
  isDatabaseDownloaded: boolean;
  isDownloading: boolean;
  progress: OfflineProgress;
  stats: OfflineDbStats;
  queuedActionsCount: number;
}

export type OfflineListener = (state: OfflineState) => void;

class OfflineDatabaseService {
  private dbPromise: Promise<IDBDatabase | null> | null = null;
  private listeners: Set<OfflineListener> = new Set();
  private isDownloading = false;

  private state: OfflineState = {
    isOnline: typeof navigator !== 'undefined' ? navigator.onLine : true,
    isDatabaseDownloaded: false,
    isDownloading: false,
    progress: { stage: 'Hazır', percent: 0 },
    stats: {
      pastQuestionsCount: 0,
      poolQuestionsCount: 0,
      committeesCount: 0,
      decksCount: 0,
      summariesCount: 0,
      glossaryCount: 0,
      flashcardsCount: 0,
      totalItems: 0,
      estimatedSizeMb: 0,
      downloadedAt: null,
    },
    queuedActionsCount: 0,
  };

  constructor() {
    if (typeof window !== 'undefined') {
      this.initListeners();
      this.initDb()
        .then(() => this.loadStats())
        .catch((e) => console.warn('[OfflineDb] Başlatma uyarısı:', e));
    }
  }

  private initListeners() {
    window.addEventListener('online', () => {
      this.state.isOnline = true;
      this.notify();
      this.syncOfflineQueue();
    });

    window.addEventListener('offline', () => {
      this.state.isOnline = false;
      this.notify();
    });

    // Service Worker'dan gelen background sync sinyallerini dinle
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data?.type === 'MEDSORU_BACKGROUND_SYNC') {
          console.log('[OfflineDb] SW Background sync sinyali alındı.');
          this.syncOfflineQueue();
        }
      });
    }
  }

  private dbInstance: IDBDatabase | null = null;

  private async initDb(): Promise<IDBDatabase | null> {
    if (typeof window === 'undefined' || !('indexedDB' in window)) return null;
    if (this.dbInstance) {
      try {
        if (this.dbInstance.objectStoreNames.length > 0) {
          return this.dbInstance;
        }
      } catch {
        this.dbInstance = null;
        this.dbPromise = null;
      }
    }
    if (this.dbPromise) return this.dbPromise;

    this.dbPromise = new Promise((resolve) => {
      let isDone = false;
      const finish = (db: IDBDatabase | null) => {
        if (!isDone) {
          isDone = true;
          this.dbInstance = db;
          resolve(db);
        }
      };

      const timer = setTimeout(() => {
        console.warn('[OfflineDb] initDb zaman aşımına uğradı');
        finish(null);
      }, 5000);

      try {
        const req = window.indexedDB.open(OFFLINE_DB_NAME, OFFLINE_DB_VERSION);

        req.onblocked = () => {
          console.warn('[OfflineDb] DB open blocked. Açık bağlantılar kapatılıyor...');
        };

        req.onupgradeneeded = (e: IDBVersionChangeEvent) => {
          const db = (e.target as IDBOpenDBRequest).result;
          if (!db.objectStoreNames.contains(STORE_QUESTIONS)) {
            const q = db.createObjectStore(STORE_QUESTIONS, { keyPath: 'id' });
            q.createIndex('by_committee', 'committeeId', { unique: false });
          }
          if (!db.objectStoreNames.contains(STORE_COMMITTEES)) {
            db.createObjectStore(STORE_COMMITTEES, { keyPath: 'id' });
          }
          if (!db.objectStoreNames.contains(STORE_DECKS)) {
            db.createObjectStore(STORE_DECKS, { keyPath: 'id' });
          }
          if (!db.objectStoreNames.contains(STORE_SUMMARIES)) {
            db.createObjectStore(STORE_SUMMARIES, { keyPath: 'id' });
          }
          if (!db.objectStoreNames.contains(STORE_GLOSSARY)) {
            db.createObjectStore(STORE_GLOSSARY, { keyPath: 'term' });
          }
          if (!db.objectStoreNames.contains(STORE_FLASHCARDS)) {
            db.createObjectStore(STORE_FLASHCARDS, { keyPath: 'id' });
          }
          if (!db.objectStoreNames.contains(STORE_QUEUE)) {
            db.createObjectStore(STORE_QUEUE, { keyPath: 'id', autoIncrement: true });
          }
          if (!db.objectStoreNames.contains(STORE_META)) {
            db.createObjectStore(STORE_META, { keyPath: 'key' });
          }
        };

        req.onsuccess = (e) => {
          clearTimeout(timer);
          const db = (e.target as IDBOpenDBRequest).result;
          db.onversionchange = () => {
            console.log('[OfflineDb] DB version change, closing connection');
            db.close();
            this.dbInstance = null;
            this.dbPromise = null;
          };
          finish(db);
        };

        req.onerror = () => {
          clearTimeout(timer);
          finish(null);
        };
      } catch {
        clearTimeout(timer);
        finish(null);
      }
    });

    return this.dbPromise;
  }

  public getState(): OfflineState {
    return { ...this.state };
  }

  public subscribe(listener: OfflineListener): () => void {
    this.listeners.add(listener);
    listener(this.getState());
    return () => this.listeners.delete(listener);
  }

  private notify() {
    const s = this.getState();
    for (const listener of this.listeners) {
      try {
        listener(s);
      } catch (err) {
        console.warn('[OfflineDb] Listener error:', err);
      }
    }
  }

  private async getMeta<T>(key: string): Promise<T | null> {
    const db = await this.initDb();
    if (!db) return null;
    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_META, 'readonly');
        const store = tx.objectStore(STORE_META);
        const req = store.get(key);
        req.onsuccess = () => resolve(req.result ? req.result.value : null);
        req.onerror = () => resolve(null);
      } catch {
        resolve(null);
      }
    });
  }

  private async setMeta<T>(key: string, value: T): Promise<void> {
    const db = await this.initDb();
    if (!db) return;
    return new Promise((resolve) => {
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

  public async loadStats(): Promise<OfflineDbStats> {
    const isDownloaded = (await this.getMeta<boolean>(KEY_IS_DOWNLOADED)) || false;
    const downloadedAt = (await this.getMeta<string>(KEY_DOWNLOAD_DATE)) || null;
    const savedStats = await this.getMeta<OfflineDbStats>(KEY_STATS);

    // IndexedDB'deki çıkmış soruları oku
    const pq = await pastQuestionsCache.getCachedQuestions();
    const pqCount = pq.length;

    // Diğer store sayılarını oku
    const db = await this.initDb();
    let poolCount = 0;
    let commCount = 0;
    let decksCount = 0;
    let glossaryCount = 0;
    let flashcardsCount = 0;
    let queueCount = 0;

    if (db) {
      poolCount = await this.countStore(db, STORE_QUESTIONS);
      commCount = await this.countStore(db, STORE_COMMITTEES);
      decksCount = await this.countStore(db, STORE_DECKS);
      glossaryCount = await this.countStore(db, STORE_GLOSSARY);
      flashcardsCount = await this.countStore(db, STORE_FLASHCARDS);
      queueCount = await this.countStore(db, STORE_QUEUE);
    }

    const total = pqCount + poolCount + commCount + decksCount + glossaryCount + flashcardsCount;
    const stats: OfflineDbStats = {
      pastQuestionsCount: pqCount,
      poolQuestionsCount: poolCount,
      committeesCount: commCount,
      decksCount: decksCount || DECK_CATALOG.length,
      summariesCount: savedStats?.summariesCount || 66,
      glossaryCount: glossaryCount || (savedStats?.glossaryCount || 0),
      flashcardsCount: flashcardsCount || (savedStats?.flashcardsCount || 0),
      totalItems: total,
      estimatedSizeMb: Math.round(((total * 3.5 + 20000) / 1024) * 10) / 10,
      downloadedAt,
    };

    this.state.isDatabaseDownloaded = isDownloaded || pqCount > 1000;
    this.state.stats = stats;
    this.state.queuedActionsCount = queueCount;
    this.notify();
    return stats;
  }

  private countStore(db: IDBDatabase, storeName: string): Promise<number> {
    return new Promise((resolve) => {
      try {
        if (!db.objectStoreNames.contains(storeName)) return resolve(0);
        const tx = db.transaction(storeName, 'readonly');
        const req = tx.objectStore(storeName).count();
        req.onsuccess = () => resolve(req.result || 0);
        req.onerror = () => resolve(0);
      } catch {
        resolve(0);
      }
    });
  }

  public async getDeck<T = any>(id: string): Promise<T | null> {
    const db = await this.initDb();
    if (!db || !db.objectStoreNames.contains(STORE_DECKS)) return null;
    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_DECKS, 'readonly');
        const store = tx.objectStore(STORE_DECKS);
        const req = store.get(id);
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => resolve(null);
      } catch {
        resolve(null);
      }
    });
  }

  /**
   * TÜM VERİTABANINI CİHAZA İNDİR (TEK TIKLA %100 ÇEVRİMDIŞI)
   */
  public async downloadEntireDatabase(
    onProgressCallback?: (p: OfflineProgress) => void
  ): Promise<boolean> {
    if (this.isDownloading) return false;
    this.isDownloading = true;
    this.state.isDownloading = true;

    const report = (stage: string, percent: number, current?: number, total?: number) => {
      this.state.progress = { stage, percent, currentCount: current, totalCount: total };
      onProgressCallback?.(this.state.progress);
      this.notify();
    };

    try {
      const db = await this.initDb();
      if (!db) throw new Error('IndexedDB başlatılamadı. Lütfen tarayıcı izinlerini kontrol edin.');

      // 1. AŞAMA: Komiteleri Çek ve Kaydet (%0 - %10)
      report('Komiteler ve sınav takvimi alınıyor...', 5);
      let committees: Committee[] = [];
      try {
        const res = await fetch('/api/committees');
        if (res.ok) {
          const data = await res.json();
          committees = data.committees || [];
        }
      } catch (e) {
        console.warn('[OfflineDb] Komite API uyarısı:', e);
      }

      if (committees.length > 0) {
        await this.putBatch(db, STORE_COMMITTEES, committees);
      }
      report('Komiteler kaydedildi.', 10);

      // 2. AŞAMA: Çıkmış Soruları (5.600+ soru) İndir (%10 - %35)
      report('Çıkmış sorular veritabanı indiriliyor...', 15);
      try {
        await pastQuestionsCache.syncWithRemote({
          forceFull: true,
          onUpdate: (updated) => {
            report(`Çıkmış sorular işleniyor (${updated.length} soru)...`, 28);
          },
        });
      } catch (err) {
        console.warn('[OfflineDb] syncWithRemote uyarısı:', err);
      }

      let cachedPast = await pastQuestionsCache.getCachedQuestions();
      // Eğer soru sayısı 0 ise doğrudan sunucudan almayı dene
      if (cachedPast.length === 0) {
        try {
          report('Çıkmış sorular sunucudan doğrudan alınıyor...', 20);
          const res = await fetch('/api/past-exams');
          if (res.ok) {
            const data = await res.json();
            const questions = data.questions || [];
            if (questions.length > 0) {
              await pastQuestionsCache.saveBatch(questions);
              cachedPast = questions;
            }
          }
        } catch (e) {
          console.warn('[OfflineDb] Doğrudan past-exams indirme hatası:', e);
        }
      }
      report(`${cachedPast.length} çıkmış sınav sorusu cihaza kaydedildi.`, 35);

      // 3. AŞAMA: Komite Havuz Sorularını İndir (%35 - %50)
      report('Komite havuz soruları indiriliyor...', 40);
      let poolQuestions: QuestionItem[] = [];
      try {
        const res = await fetch('/api/questions');
        if (res.ok) {
          const data = await res.json();
          poolQuestions = data.questions || [];
        }
      } catch (e) {
        console.warn('[OfflineDb] Havuz soruları API uyarısı:', e);
      }

      if (poolQuestions.length > 0) {
        await this.putBatch(db, STORE_QUESTIONS, poolQuestions);
      }
      report(`${poolQuestions.length} havuz sorusu kaydedildi.`, 50);

      // 4. AŞAMA: Öğrenme Destelerini Cihaza Yükle (%50 - %70)
      report('İnteraktif ders öğrenme desteleri önbelleğe alınıyor...', 52);
      const loadedDecks: any[] = [];
      try {
        const total = DECK_CATALOG.length;
        let count = 0;
        for (const d of DECK_CATALOG) {
          try {
            const full = await loadDeck(d.id);
            if (full) {
              loadedDecks.push(full);
              await this.putBatch(db, STORE_DECKS, [full]);
            }
          } catch (e) {
            console.warn(`[OfflineDb] Deste yüklenemedi (${d.id}):`, e);
          }
          count++;
          if (count % 8 === 0 || count === total) {
            const pct = Math.round(52 + (count / total) * 18);
            report(`Desteler kaydediliyor (${count}/${total})...`, pct, count, total);
            await new Promise((r) => setTimeout(r, 0));
          }
        }
        report(`${loadedDecks.length} ders destesi tam içerikle kaydedildi.`, 70);
      } catch (e) {
        console.warn('[OfflineDb] Deste yükleme uyarısı:', e);
      }

      // 5. AŞAMA: Tıbbi Sözlük ve Ansiklopedi Terimlerini İndir (%70 - %82)
      report('Tıbbi terimler sözlüğü ve ansiklopedi indiriliyor...', 72);
      try {
        const { GLOSSARY } = await import('../data/glossary');
        if (GLOSSARY && GLOSSARY.length > 0) {
          await this.putBatch(db, STORE_GLOSSARY, GLOSSARY);
        }
        report(`${GLOSSARY.length} tıbbi terim ve ansiklopedi maddesi kaydedildi.`, 82);
      } catch (e) {
        console.warn('[OfflineDb] Sözlük indirme uyarısı:', e);
      }

      // 6. AŞAMA: Akıl Kartları (Flashcards) İndir (%82 - %90)
      report('Akıl kartları (flashcards) derleniyor ve kaydediliyor...', 84);
      try {
        const flashcardsList: any[] = [];
        // Sözlük kartları
        const { GLOSSARY } = await import('../data/glossary');
        GLOSSARY.forEach((g) => {
          flashcardsList.push({
            id: `g:${g.term}`,
            group: g.category || 'Tıbbi Sözlük',
            front: g.term,
            back: g.definition,
            sub: g.pronunciation,
            pearl: g.clinicalPearls,
          });
        });

        // Deste kartları
        loadedDecks.forEach((d) => {
          (d.slides || []).forEach((s: any) => {
            (s.flashcards || []).forEach((c: any, i: number) => {
              const front = c.front || c.question;
              const back = c.back || c.answer;
              if (front && back) {
                flashcardsList.push({
                  id: `d:${d.id}:${s.slideNumber}:${c.id || i}`,
                  group: d.shortTitle || d.title,
                  front,
                  back,
                });
              }
            });
          });
        });

        if (flashcardsList.length > 0) {
          await this.putBatch(db, STORE_FLASHCARDS, flashcardsList);
        }
        report(`${flashcardsList.length} akıl kartı hazırlandı ve kaydedildi.`, 90);
      } catch (e) {
        console.warn('[OfflineDb] Kartlar indirme uyarısı:', e);
      }

      // 7. AŞAMA: Çevrimdışı Sayfa Modüllerini Önceden Yükle (Preload Chunks) (%90 - %96)
      report('Çevrimdışı sayfaların modülleri önbelleğe alınıyor...', 92);
      try {
        await Promise.allSettled([
          import('../components/encyclopedia/MedicalEncyclopediaView'),
          import('../components/flashcards/FlashcardsView'),
          import('../components/PastExamsView'),
          import('../components/PracticeMode'),
          import('../components/study/StudyHub'),
          import('../components/KazanimlarView'),
          import('../components/LectureNotesView'),
          import('../components/QuestionMatrix'),
          import('../components/BookletView'),
          import('../components/LeaderboardView'),
          import('../components/learn/InteractiveDeckView'),
        ]);
      } catch (e) {
        console.warn('[OfflineDb] Modül preload uyarısı:', e);
      }
      report('Tüm sayfa modülleri cihaza mühürlendi.', 96);

      // 8. AŞAMA: URL'leri Service Worker Cache'ine Yaz (%96 - %100)
      report('Uygulama çekirdeği senkronize ediliyor...', 97);
      const urlsToPrecache = [
        '/',
        '/index.html',
        '/manifest.json',
        '/cikmis',
        '/sozluk',
        '/kartlar',
        '/ogren',
        '/calis',
        '/sorular',
        '/kazanimlar',
        '/api/committees',
        '/api/questions',
        '/api/past-exams/sync',
      ];
      pwaService.precacheUrls(urlsToPrecache);

      const now = new Date().toISOString();
      await this.setMeta(KEY_IS_DOWNLOADED, true);
      await this.setMeta(KEY_DOWNLOAD_DATE, now);

      await this.loadStats();
      report('✓ Tüm veritabanı (sorular, desteler, sözlük, kartlar) başarıyla indirildi.', 100);

      this.isDownloading = false;
      this.state.isDownloading = false;
      this.notify();
      return true;
    } catch (err: any) {
      console.error('[OfflineDb] İndirme başarısız:', err);
      report(`İndirme sırasında hata: ${err.message || 'Bilinmeyen hata'}`, 0);
      this.isDownloading = false;
      this.state.isDownloading = false;
      this.notify();
      return false;
    }
  }

  /**
   * Toplu veri yazma (Transaction)
   */
  private putBatch(db: IDBDatabase, storeName: string, items: any[]): Promise<void> {
    return new Promise((resolve) => {
      try {
        if (!db.objectStoreNames.contains(storeName) || !items || items.length === 0) return resolve();
        const tx = db.transaction(storeName, 'readwrite');
        const store = tx.objectStore(storeName);
        for (let i = 0; i < items.length; i++) {
          const item = items[i];
          if (!item) continue;
          try {
            if (store.keyPath === 'id' && !item.id) {
              item.id = `item_${Date.now()}_${i}`;
            } else if (store.keyPath === 'term' && !item.term) {
              item.term = `term_${Date.now()}_${i}`;
            }
            store.put(item);
          } catch (e) {
            console.warn(`[OfflineDb] put error in ${storeName}:`, e);
          }
        }
        tx.oncomplete = () => resolve();
        tx.onerror = (e) => {
          console.warn(`[OfflineDb] tx error in ${storeName}:`, e);
          resolve();
        };
      } catch (e) {
        console.warn(`[OfflineDb] putBatch exception in ${storeName}:`, e);
        resolve();
      }
    });
  }

  /**
   * Çevrimdışı Eylem Kuyruğu: Kullanıcı internetsizken katkı yaparsa sakla
   */
  public async queueAction(action: Omit<OfflineAction, 'timestamp'>): Promise<void> {
    const db = await this.initDb();
    if (!db) return;

    const fullAction: OfflineAction = {
      ...action,
      timestamp: new Date().toISOString(),
    };

    await new Promise<void>((resolve) => {
      try {
        const tx = db.transaction(STORE_QUEUE, 'readwrite');
        tx.objectStore(STORE_QUEUE).add(fullAction);
        tx.oncomplete = () => resolve();
        tx.onerror = () => resolve();
      } catch {
        resolve();
      }
    });

    this.state.queuedActionsCount += 1;
    this.notify();
    pwaService.registerBackgroundSync();
  }

  /**
   * Kuyruktaki çevrimdışı eylemleri sunucuya gönder
   */
  public async syncOfflineQueue(): Promise<{ synced: number; failed: number }> {
    if (!this.state.isOnline) return { synced: 0, failed: 0 };
    const db = await this.initDb();
    if (!db) return { synced: 0, failed: 0 };

    const actions: (OfflineAction & { id: number })[] = await new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_QUEUE, 'readonly');
        const req = tx.objectStore(STORE_QUEUE).getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => resolve([]);
      } catch {
        resolve([]);
      }
    });

    if (actions.length === 0) return { synced: 0, failed: 0 };

    let synced = 0;
    let failed = 0;

    for (const act of actions) {
      try {
        const res = await fetch(act.endpoint, {
          method: act.method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(act.payload),
        });

        if (res.ok) {
          synced += 1;
          await new Promise<void>((resDel) => {
            const txDel = db.transaction(STORE_QUEUE, 'readwrite');
            txDel.objectStore(STORE_QUEUE).delete(act.id);
            txDel.oncomplete = () => resDel();
            txDel.onerror = () => resDel();
          });
        } else {
          failed += 1;
        }
      } catch {
        failed += 1;
      }
    }

    this.state.queuedActionsCount = Math.max(0, actions.length - synced);
    this.notify();
    return { synced, failed };
  }

  /**
   * Çevrimdışı veritabanını temizle
   */
  public async clearDatabase(): Promise<void> {
    const db = await this.initDb();
    if (db) {
      await new Promise<void>((resolve) => {
        try {
          const stores = [
            STORE_QUESTIONS,
            STORE_COMMITTEES,
            STORE_DECKS,
            STORE_SUMMARIES,
            STORE_GLOSSARY,
            STORE_FLASHCARDS,
            STORE_META,
          ].filter((s) => db.objectStoreNames.contains(s));

          const tx = db.transaction(stores, 'readwrite');
          stores.forEach((s) => tx.objectStore(s).clear());
          tx.oncomplete = () => resolve();
          tx.onerror = () => resolve();
        } catch {
          resolve();
        }
      });
    }

    await pastQuestionsCache.clearCache();
    await this.loadStats();
    this.state.isDatabaseDownloaded = false;
    this.notify();
  }
}

export const offlineDatabaseService = new OfflineDatabaseService();
