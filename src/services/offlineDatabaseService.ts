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
import { toast } from '../components/ui/Toast';
import { defaultApiBaseForThisHost } from '../config/deployment';
import { onNetChange, getNetState } from './net';

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
  type: 'contribute' | 'vote' | 'note' | 'feedback' | 'report' | 'comment';
  endpoint: string;
  method: 'POST' | 'PUT' | 'DELETE';
  payload: any;
  timestamp: string;
  /** Kuyruk denemesi: kaç kez gönderilmeye çalışıldı, bir sonraki deneme zamanı (ms) */
  attempts?: number;
  nextAt?: number;
}

/** Göreli /api yolunu canlı API tabanına çevirir (Ayarlar'daki özel adres > hostun varsayılanı). */
function resolveApiUrl(endpoint: string) {
  if (!endpoint.startsWith('/')) return endpoint;
  let base = '';
  try {
    base = (localStorage.getItem('medsoru_custom_api_url') || '').trim();
  } catch { /* yok */ }
  if (!base) base = defaultApiBaseForThisHost();
  return `${base.replace(/\/$/, '')}${endpoint}`;
}
const MAX_ATTEMPTS = 8;

export interface OfflineState {
  isOnline: boolean;
  isDatabaseDownloaded: boolean;
  isDownloading: boolean;
  progress: OfflineProgress;
  stats: OfflineDbStats;
  queuedActionsCount: number;
}

export type OfflineStoreKind = 'past' | 'pool' | 'committees' | 'decks' | 'summaries' | 'glossary' | 'flashcards';

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
      void this.syncOfflineQueue();
    });

    window.addEventListener('offline', () => {
      this.state.isOnline = false;
      this.notify();
    });

    // Bağlantı "zayıf"tan "çevrimiçi"ye dönünce ve sekme öne gelince kuyruk boşaltılır
    onNetChange(() => {
      if (getNetState() === 'online') void this.syncOfflineQueue();
    });
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden && this.state.queuedActionsCount > 0) void this.syncOfflineQueue();
    });

    // Service Worker'dan gelen background sync sinyallerini dinle
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data?.type === 'MEDSORU_BACKGROUND_SYNC') void this.syncOfflineQueue();
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
    // Yalnız sayı gerekiyor: getCachedQuestions açılışta ~85 MB'ı belleğe açıyordu (telefonda donma)
    const pqCount = await pastQuestionsCache.getCachedCount();

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
   * Çevrimdışı komiteleri getir
   */
  public async getCommittees(): Promise<Committee[]> {
    const db = await this.initDb();
    if (!db || !db.objectStoreNames.contains(STORE_COMMITTEES)) return [];
    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_COMMITTEES, 'readonly');
        const req = tx.objectStore(STORE_COMMITTEES).getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => resolve([]);
      } catch {
        resolve([]);
      }
    });
  }

  /**
   * Komiteleri cihaza kaydet
   */
  public async saveCommittees(committees: Committee[]): Promise<void> {
    if (!committees || committees.length === 0) return;
    const db = await this.initDb();
    if (!db) return;
    await this.putBatch(db, STORE_COMMITTEES, committees);
  }

  /**
   * Çevrimdışı havuz sorularını getir
   */
  public async getQuestions(committeeId?: string): Promise<QuestionItem[]> {
    const db = await this.initDb();
    if (!db || !db.objectStoreNames.contains(STORE_QUESTIONS)) return [];
    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_QUESTIONS, 'readonly');
        const store = tx.objectStore(STORE_QUESTIONS);
        if (committeeId && store.indexNames.contains('by_committee')) {
          const idx = store.index('by_committee');
          const req = idx.getAll(committeeId);
          req.onsuccess = () => resolve(req.result || []);
          req.onerror = () => resolve([]);
        } else {
          const req = store.getAll();
          req.onsuccess = () => {
            const all: QuestionItem[] = req.result || [];
            if (committeeId) {
              resolve(all.filter((q) => q.committeeId === committeeId));
            } else {
              resolve(all);
            }
          };
          req.onerror = () => resolve([]);
        }
      } catch {
        resolve([]);
      }
    });
  }

  /**
   * Havuz sorularını cihaza kaydet
   */
  public async saveQuestions(questions: QuestionItem[]): Promise<void> {
    if (!questions || questions.length === 0) return;
    const db = await this.initDb();
    if (!db) return;
    await this.putBatch(db, STORE_QUESTIONS, questions);
  }

  /**
   * Çevrimdışı tıbbi sözlüğü getir
   */
  public async getGlossary(): Promise<any[]> {
    const db = await this.initDb();
    if (!db || !db.objectStoreNames.contains(STORE_GLOSSARY)) return [];
    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_GLOSSARY, 'readonly');
        const req = tx.objectStore(STORE_GLOSSARY).getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => resolve([]);
      } catch {
        resolve([]);
      }
    });
  }

  /**
   * Tıbbi sözlük terimlerini cihaza kaydet
   */
  public async saveGlossary(items: any[]): Promise<void> {
    if (!items || items.length === 0) return;
    const db = await this.initDb();
    if (!db) return;
    await this.putBatch(db, STORE_GLOSSARY, items);
  }

  /**
   * Çevrimdışı akıl kartlarını getir
   */
  public async getFlashcards(): Promise<any[]> {
    const db = await this.initDb();
    if (!db || !db.objectStoreNames.contains(STORE_FLASHCARDS)) return [];
    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_FLASHCARDS, 'readonly');
        const req = tx.objectStore(STORE_FLASHCARDS).getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => resolve([]);
      } catch {
        resolve([]);
      }
    });
  }

  /**
   * Akıl kartlarını cihaza kaydet
   */
  public async saveFlashcards(cards: any[]): Promise<void> {
    if (!cards || cards.length === 0) return;
    const db = await this.initDb();
    if (!db) return;
    await this.putBatch(db, STORE_FLASHCARDS, cards);
  }

  /**
   * Çevrimdışı ders özetlerini getir
   */
  public async getSummaries(): Promise<any[]> {
    const db = await this.initDb();
    if (!db || !db.objectStoreNames.contains(STORE_SUMMARIES)) return [];
    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_SUMMARIES, 'readonly');
        const req = tx.objectStore(STORE_SUMMARIES).getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => resolve([]);
      } catch {
        resolve([]);
      }
    });
  }

  /**
   * Ders özetlerini cihaza kaydet
   */
  public async saveSummaries(items: any[]): Promise<void> {
    if (!items || items.length === 0) return;
    const db = await this.initDb();
    if (!db) return;
    await this.putBatch(db, STORE_SUMMARIES, items);
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
        report(`${flashcardsList.length} akıl kartı hazırlandı ve kaydedildi.`, 88);
      } catch (e) {
        console.warn('[OfflineDb] Kartlar indirme uyarısı:', e);
      }

      // 6.5 AŞAMA: Ders Özetlerini (Summaries) Kaydet (%88 - %92)
      report('Ders özetleri önbelleğe alınıyor...', 89);
      try {
        const [k1, k2, k3, k4, k5, k6] = await Promise.all([
          import('../data/summaries/kurul1.json').then((m) => m.default || m).catch(() => []),
          import('../data/summaries/kurul2.json').then((m) => m.default || m).catch(() => []),
          import('../data/summaries/kurul3.json').then((m) => m.default || m).catch(() => []),
          import('../data/summaries/kurul4.json').then((m) => m.default || m).catch(() => []),
          import('../data/summaries/kurul5.json').then((m) => m.default || m).catch(() => []),
          import('../data/summaries/kurul6.json').then((m) => m.default || m).catch(() => []),
        ]);
        const allSummaries = [...k1, ...k2, ...k3, ...k4, ...k5, ...k6];
        if (allSummaries.length > 0) {
          await this.putBatch(db, STORE_SUMMARIES, allSummaries);
        }
        report(`${allSummaries.length} ders özeti cihaza kaydedildi.`, 92);
      } catch (e) {
        console.warn('[OfflineDb] Özet indirme uyarısı:', e);
      }

      // 7. AŞAMA: Çevrimdışı Sayfa Modüllerini Önceden Yükle (Preload Chunks) (%92 - %96)
      report('Çevrimdışı sayfaların modülleri önbelleğe alınıyor...', 93);
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
          import('../components/diseases/DiseasesView'),
          import('../components/LectureSummariesView'),
          import('../components/PracticeQuestionsView'),
          import('../components/stats/StatsView'),
          import('../components/settings/ProfileSettingsView'),
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
        '/hastaliklar',
        '/calis',
        '/ozetler',
        '/ornek-sorular',
        '/sorular',
        '/kazanimlar',
        '/test',
        '/istatistik',
        '/ayarlar',
        '/api/committees',
        '/api/questions',
        '/api/past-exams/sync',
      ];
      pwaService.precacheUrls(urlsToPrecache);

      const now = new Date().toISOString();
      await this.setMeta(KEY_IS_DOWNLOADED, true);
      await this.setMeta(KEY_DOWNLOAD_DATE, now);

      await this.loadStats();
      report('✓ Tüm veritabanı (sorular, desteler, özetler, sözlük, kartlar) başarıyla indirildi.', 100);

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

  private readQueue(db: IDBDatabase): Promise<(OfflineAction & { id: number })[]> {
    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_QUEUE, 'readonly');
        const req = tx.objectStore(STORE_QUEUE).getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => resolve([]);
      } catch {
        resolve([]);
      }
    });
  }

  private writeQueue(db: IDBDatabase, op: (store: IDBObjectStore) => void): Promise<void> {
    return new Promise((resolve) => {
      try {
        const tx = db.transaction(STORE_QUEUE, 'readwrite');
        op(tx.objectStore(STORE_QUEUE));
        tx.oncomplete = () => resolve();
        tx.onerror = () => resolve();
      } catch {
        resolve();
      }
    });
  }

  private syncRegistered = false;
  private queueToastAt = 0;

  /**
   * Çevrimdışı Eylem Kuyruğu: istek ağ hatasıyla düşerse işlem cihazda saklanır.
   * - Oy uçları aç/kapa çalışır: kuyrukta aynı oyun bekleyen bir kopyası varsa ikisi birbirini sıfırlar (iki dokunuş = değişiklik yok).
   * - Aynı uca aynı yükle bekleyen kopya varsa yenisi eklenmez (çift dokunuş yığılmaz).
   */
  public async queueAction(action: Omit<OfflineAction, 'timestamp'>): Promise<void> {
    const db = await this.initDb();
    if (!db) return;
    const existing = await this.readQueue(db);
    const payloadKey = JSON.stringify(action.payload ?? null);
    const twin = existing.find((a) => a.endpoint === action.endpoint && a.method === action.method && JSON.stringify(a.payload ?? null) === payloadKey);

    if (twin && action.type === 'vote') {
      await this.writeQueue(db, (st) => st.delete(twin.id));
    } else if (!twin) {
      const fullAction: OfflineAction = { ...action, timestamp: new Date().toISOString(), attempts: 0, nextAt: 0 };
      await this.writeQueue(db, (st) => st.add(fullAction));
    }

    this.state.queuedActionsCount = (await this.readQueue(db)).length;
    this.notify();
    if (!this.syncRegistered) {
      this.syncRegistered = true;
      void pwaService.registerBackgroundSync();
    }
    // Art arda işlemlerde tek bildirim
    if (Date.now() - this.queueToastAt > 15_000) {
      this.queueToastAt = Date.now();
      toast.info('Bağlantı yok — sıraya alındı', 'İşleminiz cihazda saklandı; bağlantı gelince kendiliğinden gönderilecek.');
    }
  }

  /** Kuyruktaki işlemler (en yeni üstte) — "Gönderim kuyruğu" sayfası için. */
  public async listQueue(): Promise<(OfflineAction & { id: number })[]> {
    const db = await this.initDb();
    if (!db) return [];
    return (await this.readQueue(db)).sort((a, b) => String(b.timestamp).localeCompare(String(a.timestamp)));
  }

  /** Bekleyen işlemleri iptal eder (sunucuya hiç gönderilmez). `ids` verilmezse tümü. */
  public async cancelQueued(ids?: number[]): Promise<number> {
    const db = await this.initDb();
    if (!db) return 0;
    const all = await this.readQueue(db);
    const target = ids ? all.filter((a) => ids.includes(a.id)) : all;
    if (!target.length) return 0;
    await this.writeQueue(db, (st) => target.forEach((a) => st.delete(a.id)));
    this.state.queuedActionsCount = (await this.readQueue(db)).length;
    this.notify();
    return target.length;
  }

  /** İptali geri al: işlemi aynı içerikle (deneme sayacı sıfırlanarak) kuyruğa geri koyar. */
  public async restoreQueued(actions: OfflineAction[]): Promise<void> {
    const db = await this.initDb();
    if (!db || !actions.length) return;
    await this.writeQueue(db, (st) => actions.forEach(({ id: _id, ...a }) => st.add({ ...a, attempts: 0, nextAt: 0 })));
    this.state.queuedActionsCount = (await this.readQueue(db)).length;
    this.notify();
  }

  private draining: Promise<{ synced: number; failed: number }> | null = null;

  /**
   * Kuyruktaki eylemleri sırayla gönderir. Aynı anda tek boşaltma çalışır (online olayı, SW sinyali ve
   * el ile tetikleme üst üste binmez). Başarısız eylem geri çekilmeyle (2^n sn) bekler; 4xx yanıtı (408/429
   * hariç) ya da 8 deneme sonrası kuyruktan düşer — sonsuza dek tekrar edilmez.
   */
  public syncOfflineQueue(): Promise<{ synced: number; failed: number }> {
    if (this.draining) return this.draining;
    this.draining = this.drain().finally(() => {
      this.draining = null;
    });
    return this.draining;
  }

  private async drain(): Promise<{ synced: number; failed: number }> {
    if (!this.state.isOnline || getNetState() === 'offline') return { synced: 0, failed: 0 };
    const db = await this.initDb();
    if (!db) return { synced: 0, failed: 0 };
    const actions = await this.readQueue(db);
    if (actions.length === 0) {
      if (this.state.queuedActionsCount) { this.state.queuedActionsCount = 0; this.notify(); }
      return { synced: 0, failed: 0 };
    }

    let synced = 0;
    let failed = 0;
    let dropped = 0;
    const now = Date.now();
    for (const act of actions) {
      if ((act.nextAt || 0) > now) continue;
      let ok = false;
      let permanent = false;
      try {
        const headers: Record<string, string> = { 'Content-Type': 'application/json' };
        try {
          const pw = sessionStorage.getItem('medsoru_api_write_password');
          if (pw) headers['X-API-Password'] = pw;
        } catch { /* yok */ }
        const res = await fetch(resolveApiUrl(act.endpoint), {
          method: act.method,
          headers,
          body: act.method === 'DELETE' && act.payload == null ? undefined : JSON.stringify(act.payload),
        });
        ok = res.ok;
        permanent = !ok && res.status >= 400 && res.status < 500 && res.status !== 408 && res.status !== 429;
      } catch {
        ok = false;
      }
      const attempts = (act.attempts || 0) + 1;
      if (ok || permanent || attempts >= MAX_ATTEMPTS) {
        if (ok) synced += 1;
        else dropped += 1;
        await this.writeQueue(db, (st) => st.delete(act.id));
      } else {
        failed += 1;
        await this.writeQueue(db, (st) => st.put({ ...act, attempts, nextAt: Date.now() + Math.min(5 * 60_000, 2000 * 2 ** attempts) }));
        // Ağ hâlâ yoksa kalanları bu turda zorlamaya gerek yok
        if (getNetState() !== 'online') break;
      }
    }

    this.state.queuedActionsCount = (await this.readQueue(db)).length;
    this.notify();
    if (synced > 0) toast.success('Gönderildi', `Bekleyen ${synced} işlem sunucuya iletildi.`);
    if (dropped > 0) toast.info('Bazı işlemler gönderilemedi', `${dropped} işlem sunucu tarafından kabul edilmedi ve kuyruktan çıkarıldı.`);
    // Hâlâ bekleyen varsa en yakın deneme zamanına kur
    if (this.state.queuedActionsCount > 0) {
      const rest = await this.readQueue(db);
      const soonest = Math.min(...rest.map((a) => a.nextAt || 0));
      window.setTimeout(() => void this.syncOfflineQueue(), Math.max(1000, soonest - Date.now()));
    }
    return { synced, failed };
  }

  /** Tek bir çevrimdışı depoyu boşaltır (Cihazdaki veriler › tek tek silme). */
  public async clearStore(kind: OfflineStoreKind): Promise<void> {
    if (kind === 'past') {
      await pastQuestionsCache.clearCache();
    } else {
      const name = {
        pool: STORE_QUESTIONS,
        committees: STORE_COMMITTEES,
        decks: STORE_DECKS,
        summaries: STORE_SUMMARIES,
        glossary: STORE_GLOSSARY,
        flashcards: STORE_FLASHCARDS,
      }[kind];
      const db = await this.initDb();
      if (db && db.objectStoreNames.contains(name)) {
        await new Promise<void>((resolve) => {
          try {
            const tx = db.transaction(name, 'readwrite');
            tx.objectStore(name).clear();
            tx.oncomplete = () => resolve();
            tx.onerror = () => resolve();
          } catch {
            resolve();
          }
        });
      }
    }
    await this.loadStats();
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
