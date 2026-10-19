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
import { defaultApiBaseForThisHost, panelApiBase } from '../config/deployment';

function getCustomApiUrl(): string {
  if (typeof window === 'undefined' || !window.localStorage) return '';
  const url = localStorage.getItem('medsoru_custom_api_url') || '';
  if (url && (url.includes('github.io') || url.includes('github.com'))) return '';
  if (url.trim()) return url.trim().replace(/\/$/, '');
  try {
    // Yerel yönetim paneli Oracle'a bağlıysa çıkmış sorular da oradan
    return panelApiBase('/api/past-exams') || defaultApiBaseForThisHost();
  } catch (_) {
    return '';
  }
}

const DB_NAME = 'medsoru_past_questions_db';
const DB_VERSION = 1;
const CACHE_FORMAT_KEY = 'medsoru_pq_cache_format';
const CACHE_FORMAT = '2026-10-07';
const STORE_QUESTIONS = 'past_questions';
const STORE_META = 'metadata';

const KEY_LAST_SYNC = 'last_sync_timestamp';
const KEY_TOTAL_COUNT = 'last_sync_count';

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
  /** Son başarılı ağ eşitlemesinin zamanı (aynı açılışta art arda tetiklemeleri birleştirmek için) */
  private lastSyncAt = 0;
  /** Bellek doldurulmadan bilinen soru kimlikleri (IndexedDB anahtarları). Eşitleme tüm soruları
   * (~85 MB) belleğe açmadan sayı ve fazlalık denetimini bununla yapar; ekranlar getCachedQuestions ister. */
  private cachedIds: Set<string> | null = null;

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

  /** Cihazdaki soru sayısı (bellek henüz doldurulmadıysa anahtar kümesinden) */
  private cachedCount(): number {
    if (this.isMemoryInitialized || !this.cachedIds) return this.memoryMap.size;
    return this.cachedIds.size;
  }

  /** Tüm soruları açmadan cihazdaki kimlikler (IndexedDB getAllKeys: yapılandırılmış kopya yok, ucuz) */
  private async getCachedIdSet(): Promise<Set<string>> {
    if (this.isMemoryInitialized) return new Set(this.memoryMap.keys());
    if (this.cachedIds) return this.cachedIds;
    const db = await this.initDb();
    if (!db) return new Set(this.memoryMap.keys());
    const keys = await new Promise<string[]>((resolve) => {
      try {
        const req = db.transaction(STORE_QUESTIONS, 'readonly').objectStore(STORE_QUESTIONS).getAllKeys();
        req.onsuccess = () => resolve((req.result || []).map(String));
        req.onerror = () => resolve([]);
      } catch {
        resolve([]);
      }
    });
    // Bu arada belleğe tam yükleme yapıldıysa o yetkilidir
    if (this.isMemoryInitialized) return new Set(this.memoryMap.keys());
    this.cachedIds = new Set(keys);
    return this.cachedIds;
  }

  /** Cihazdaki soru sayısı — soruları belleğe açmadan (istatistik/durum ekranları için) */
  public async getCachedCount(): Promise<number> {
    return (await this.getCachedIdSet()).size;
  }

  private notifyListeners(updatedQuestions?: QuestionItem[]) {
    this.currentStatus.totalCached = this.cachedCount();
    for (const listener of this.listeners) {
      try {
        listener({ ...this.currentStatus }, updatedQuestions);
      } catch (e) {
        console.warn('[PastQuestionsCache] Listener error:', e);
      }
    }
  }

  /**
   * İstemci arayüzünde hiç kullanılmayan sunucu/pipeline alanlarını (checkSolveOriginal, ragChunk,
   * embeddingText, grounding, yinelenen denetleyiciSurumu/reconstruction açıklamaları) bellekten ve
   * IndexedDB'den arındırarak RAM kullanımını %50+ düşürür.
   */
  /** Kayıt sadeleştirilmemiş alan taşıyor mu (okumada her soruyu yeniden kopyalamamak için ucuz denetim) */
  private needsSlim(raw: any): boolean {
    if (!raw || typeof raw !== 'object') return false;
    if (raw.checkSolveOriginal || raw.ragChunk || raw.embeddingText || raw.grounding) return true;
    if (raw.explanation && raw.tibbi_aciklama) return true;
    const cs = raw.checkSolve;
    if (cs && typeof cs === 'object' && ('version' in cs || 'parti' in cs || 'degisiklikler' in cs || 'guven' in cs)) return true;
    const ds = raw.denetleyiciSurumu;
    if (ds && typeof ds === 'object' && ('explanation' in ds || 'correctAnswer' in ds || 'topic' in ds)) return true;
    const rc = raw.reconstruction;
    if (rc && typeof rc === 'object' && ((raw.explanation && rc.explanation === raw.explanation) || (raw.stem && rc.stem === raw.stem))) return true;
    return false;
  }

  private slimQuestion(raw: QuestionItem): QuestionItem {
    if (!raw || typeof raw !== 'object') return raw;
    const q: any = { ...raw };
    delete q.checkSolveOriginal;
    delete q.ragChunk;
    delete q.embeddingText;
    delete q.grounding;
    if (q.explanation && q.tibbi_aciklama) {
      delete q.tibbi_aciklama;
    }
    if (q.checkSolve && typeof q.checkSolve === 'object') {
      const cs = q.checkSolve;
      q.checkSolve = {
        status: cs.status,
        ...(cs.cevapDegisti ? { cevapDegisti: cs.cevapDegisti } : {}),
        ...(cs.cevapGerekcesi ? { cevapGerekcesi: cs.cevapGerekcesi } : {}),
        ...(cs.eklenenSiklar ? { eklenenSiklar: cs.eklenenSiklar } : {}),
        ...(cs.mufredat ? { mufredat: cs.mufredat } : {}),
        ...(cs.at ? { at: cs.at } : {}),
      };
    }
    if (q.denetleyiciSurumu && typeof q.denetleyiciSurumu === 'object') {
      const ds = q.denetleyiciSurumu;
      q.denetleyiciSurumu = {
        ...(ds.stem ? { stem: ds.stem } : {}),
        ...(ds.options ? { options: ds.options } : {}),
        ...(ds.onayTarihi ? { onayTarihi: ds.onayTarihi } : {}),
        ...(!q.sik_analizi && ds.sik_analizi ? { sik_analizi: ds.sik_analizi } : {}),
        ...(!q.referans_kaynaklar && ds.referans_kaynaklar ? { referans_kaynaklar: ds.referans_kaynaklar } : {}),
      };
    }
    if (q.reconstruction && typeof q.reconstruction === 'object') {
      const rc = { ...q.reconstruction };
      if (q.explanation && rc.explanation === q.explanation) delete rc.explanation;
      if (q.stem && rc.stem === q.stem) delete rc.stem;
      if (Array.isArray(q.options) && Array.isArray(rc.options) && rc.options.length === q.options.length) {
        let same = true;
        for (let i = 0; i < q.options.length; i++) {
          if (q.options[i] !== rc.options[i]) { same = false; break; }
        }
        if (same) delete rc.options;
      }
      q.reconstruction = rc;
    }
    return q as QuestionItem;
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
          const rawItems: QuestionItem[] = req.result || [];
          this.memoryMap.clear();
          const slimmed: QuestionItem[] = [];
          for (const item of rawItems) {
            if (item && item.id) {
              // saveBatch/saveQuestion zaten sadeleştirip yazar; yalnız eski biçimde kalmış kaydı yeniden kopyala
              const s = this.needsSlim(item) ? this.slimQuestion(item) : item;
              this.memoryMap.set(s.id, s);
              slimmed.push(s);
            }
          }
          this.isMemoryInitialized = true;
          this.cachedIds = null;
          this.currentStatus.totalCached = this.memoryMap.size;
          resolve(slimmed);
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
        req.onsuccess = () => resolve(req.result ? this.slimQuestion(req.result) : null);
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
    const slim = this.slimQuestion(question);
    if (this.isMemoryInitialized) {
      this.memoryMap.set(slim.id, slim);
    }
    this.cachedIds?.add(slim.id);

    const db = await this.initDb();
    if (db) {
      await new Promise<void>((resolve) => {
        try {
          const tx = db.transaction([STORE_QUESTIONS, STORE_META], 'readwrite');
          const qStore = tx.objectStore(STORE_QUESTIONS);
          qStore.put(slim);

          tx.oncomplete = () => resolve();
          tx.onerror = () => resolve();
        } catch {
          resolve();
        }
      });
    }

    this.notifyListeners([slim]);
  }

  /**
   * Çoklu soruları toplu şekilde IndexedDB'ye yaz (Batch Transaction)
   */
  public async saveBatch(questions: QuestionItem[]): Promise<void> {
    if (!questions || questions.length === 0) return;

    const slimList: QuestionItem[] = new Array(questions.length);
    for (let i = 0; i < questions.length; i++) {
      slimList[i] = this.slimQuestion(questions[i]);
    }

    // Bellek yalnızca getCachedQuestions() çağrılmışsa (isMemoryInitialized === true) doldurulur.
    // Arka plan eşitlemesinde 5.400 soruyu JS yığınına (RAM) açmayız; yalnız kimlik kümesi güncellenir.
    if (!this.isMemoryInitialized && !this.cachedIds) {
      this.cachedIds = new Set();
    }
    for (const q of slimList) {
      if (q && q.id) {
        if (this.isMemoryInitialized) this.memoryMap.set(q.id, q);
        else this.memoryMap.delete(q.id);
        this.cachedIds?.add(q.id);
      }
    }

    const db = await this.initDb();
    if (!db) {
      // IndexedDB desteklenmeyen ortamda mecburi bellek yedeği
      for (const q of slimList) {
        if (q && q.id) this.memoryMap.set(q.id, q);
      }
      this.isMemoryInitialized = true;
      this.notifyListeners(slimList);
      return;
    }

    // Parça parça yazılır: put() kaydı ana iş parçacığında kopyalar; 500'lük parça ilk yüklemede
    // 1,5–2 sn'lik donma yapıyordu. 200'lük parçalar ve aralarında bir kare boşluk arayüzü akıcı tutar.
    const CHUNK_SIZE = 200;
    for (let i = 0; i < slimList.length; i += CHUNK_SIZE) {
      if (i > 0) await new Promise<void>((r) => setTimeout(r, 0));
      const chunk = slimList.slice(i, i + CHUNK_SIZE);
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

    this.notifyListeners(slimList);
  }

  /**
   * Silinen soruları cihaz hafızasından kaldır
   */
  public async removeQuestions(ids: string[]): Promise<void> {
    if (!ids || ids.length === 0) return;

    for (const id of ids) {
      this.memoryMap.delete(id);
      this.cachedIds?.delete(id);
    }
    this.currentStatus.totalCached = this.cachedCount();

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
    // Önbellek biçimi değişince (ör. Faz 14 / cevap anketi alanları) cihaz bir kez tam yükleme yapar
    try {
      if (typeof window !== 'undefined' && window.localStorage.getItem(CACHE_FORMAT_KEY) !== CACHE_FORMAT) return null;
    } catch { /* depolama kapalı */ }
    return this.getMeta<string>(KEY_LAST_SYNC);
  }

  public async setLastSyncTime(time: string, count?: number): Promise<void> {
    await this.setMeta(KEY_LAST_SYNC, time);
    // Eşitleme zamanı yalnız güncel biçimde tam/artımlı yazılmış önbellek için kaydedilir; biçim işareti
    // konmazsa getLastSyncTime null döner ve bir sonraki eşitleme tüm listeyi (~85 MB) ikinci kez indirirdi
    // (ilk açılışı multiDbManager/api.ts doldurduğunda böyle oluyordu).
    try { if (typeof window !== 'undefined') window.localStorage.setItem(CACHE_FORMAT_KEY, CACHE_FORMAT); } catch { /* depolama kapalı */ }
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
    this.cachedIds = new Set();

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
    onlyIfCached?: boolean;
    onUpdate?: (updated: QuestionItem[]) => void;
  } = {}): Promise<{
    success: boolean;
    updatedCount: number;
    isUpToDate: boolean;
    totalCount: number;
  }> {
    if (this.syncInProgress) {
      if (options.forceFull) {
        let waitCount = 0;
        while (this.syncInProgress && waitCount < 20) {
          await new Promise((r) => setTimeout(r, 200));
          waitCount++;
        }
        if (this.syncInProgress) {
          this.syncInProgress = false;
        }
      } else {
        return {
          success: true,
          updatedCount: 0,
          isUpToDate: this.currentStatus.isUpToDate,
          totalCount: this.cachedCount(),
        };
      }
    }

    // Açılışta getPastQuestions, SSE bağlanması ve sayfa geçişleri eşitlemeyi saniyeler içinde birkaç kez
    // tetikliyor; zorunlu olmayanlar 20 sn içinde tekrar ağa çıkmaz.
    if (!options.forceFull && this.lastSyncAt > 0 && Date.now() - this.lastSyncAt < 20_000) {
      return { success: true, updatedCount: 0, isUpToDate: this.currentStatus.isUpToDate, totalCount: this.cachedCount() };
    }

    this.syncInProgress = true;
    this.currentStatus.isSyncing = true;
    this.currentStatus.statusMessage = 'Güncellemeler kontrol ediliyor...';
    this.notifyListeners();

    try {
      // 1. Mevcut yerel soruları ve son senkronizasyon zamanını oku
      const localIds = await this.getCachedIdSet();
      const localCount = localIds.size;
      let lastSyncTime = await this.getLastSyncTime();

      // Arka plan SSE tetiklemesi: Kullanıcı henüz Çıkmış Sorular'ı açmamışsa ve yerel önbellek boşsa
      // tam veritabanını arka planda indirip ağ ve RAM'i meşgul etme
      if (options.onlyIfCached && (localCount === 0 || !lastSyncTime) && !this.isMemoryInitialized) {
        this.syncInProgress = false;
        this.currentStatus.isSyncing = false;
        this.notifyListeners();
        return {
          success: true,
          updatedCount: 0,
          isUpToDate: false,
          totalCount: localCount,
        };
      }

      // Çevrimdışı Kontrolü: Cihaz internetsizse doğrudan cihaz hafızasını sun, ağı bekleme
      if (typeof navigator !== 'undefined' && !navigator.onLine) {
        this.syncInProgress = false;
        this.currentStatus.isSyncing = false;
        this.currentStatus.isUpToDate = true;
        this.currentStatus.statusMessage = 'Çevrimdışı mod: Cihaz hafızasındaki sorular hazır.';
        this.notifyListeners();
        return {
          success: true,
          updatedCount: 0,
          isUpToDate: true,
          totalCount: localCount,
        };
      }

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
      {
        try {
          const apiBase = customUrl || '';
          const syncUrl = `${apiBase}/api/past-exams/sync?since=${encodeURIComponent(lastSyncTime)}&count=${localCount}`;
          
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 4000);
          const res = await fetch(syncUrl, { signal: controller.signal });
          clearTimeout(timeoutId);

          if (res.ok) {
            const data = await res.json();
            this.lastSyncAt = Date.now();
            // Sunucuda silinmiş soruları doğrudan yerel önbellekten kaldır
            if (Array.isArray(data.deletedIds) && data.deletedIds.length > 0) {
              const toRemove = data.deletedIds.filter((id: string) => localIds.has(String(id)) || this.memoryMap.has(id));
              if (toRemove.length) await this.removeQuestions(toRemove);
            }
            // Sunucuda artık olmayan (ör. karantinaya alınan) soruları cihaz önbelleğinden kaldır
            // Tam liste geldiyse o liste yetkilidir (eski sunucu allIds göndermiyordu → fazlalık hiç silinmiyordu)
            const authoritativeIds: any[] | null = Array.isArray(data.allIds) && data.allIds.length > 0
              ? data.allIds
              : (Array.isArray(data.questions) && data.questions.length > 0 ? data.questions.map((q: any) => q?.id).filter(Boolean) : null);
            if (authoritativeIds) {
              const keep = new Set<string>(authoritativeIds.map(String));
              const stale = Array.from(this.isMemoryInitialized ? this.memoryMap.keys() : localIds).filter((id) => !keep.has(String(id)));
              if (stale.length) await this.removeQuestions(stale);
            }
            if (data.upToDate) {
              this.syncInProgress = false;
              this.currentStatus.isSyncing = false;
              this.currentStatus.isUpToDate = true;
              this.currentStatus.lastSyncDeltaCount = 0;
              this.currentStatus.statusMessage = 'Cihazınız tamamen güncel (0 Bayt indirme yapıldı).';
              this.notifyListeners();
              return { success: true, updatedCount: 0, isUpToDate: true, totalCount: localCount };
            }

            const incomingQuestions = (Array.isArray(data.updatedQuestions) && data.updatedQuestions.length > 0)
              ? data.updatedQuestions
              : (Array.isArray(data.questions) && data.questions.length > 0 ? data.questions : null);

            if (incomingQuestions && incomingQuestions.length > 0) {
              await this.saveBatch(incomingQuestions);
              if (data.lastModified) {
                await this.setLastSyncTime(data.lastModified, this.cachedCount() || data.count || incomingQuestions.length);
                this.currentStatus.lastSyncTime = data.lastModified;
              }
              options.onUpdate?.(incomingQuestions);

              this.syncInProgress = false;
              this.currentStatus.isSyncing = false;
              this.currentStatus.isUpToDate = true;
              this.currentStatus.lastSyncDeltaCount = incomingQuestions.length;
              this.currentStatus.statusMessage = `${incomingQuestions.length} adet soru cihazınızda güncellendi.`;
              this.notifyListeners(incomingQuestions);
              return {
                success: true,
                updatedCount: incomingQuestions.length,
                isUpToDate: true,
                totalCount: this.cachedCount(),
              };
            }

            // Yerel sunucu yanıt verdi, silinenler kaldırıldı; güncellenecek yeni soru yok
            if (data.lastModified) {
              await this.setLastSyncTime(data.lastModified, data.count || this.cachedCount());
              this.currentStatus.lastSyncTime = data.lastModified;
            }
            this.syncInProgress = false;
            this.currentStatus.isSyncing = false;
            this.currentStatus.isUpToDate = true;
            this.currentStatus.lastSyncDeltaCount = 0;
            this.currentStatus.statusMessage = 'Cihazınız güncel.';
            this.notifyListeners();
            return {
              success: true,
              updatedCount: 0,
              isUpToDate: true,
              totalCount: this.cachedCount(),
            };
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
              totalCount: this.cachedCount(),
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
      return { success: false, updatedCount: 0, isUpToDate: false, totalCount: this.cachedCount() };
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
      try { window.localStorage.setItem(CACHE_FORMAT_KEY, CACHE_FORMAT); } catch { /* depolama kapalı */ }
      this.currentStatus.lastSyncTime = maxTime;
      this.currentStatus.totalCached = fetched.length;
    }

    return fetched;
  }

  public getStatus(): CacheSyncStatus {
    return { ...this.currentStatus, totalCached: this.cachedCount() };
  }
}

export const pastQuestionsCache = new PastQuestionsCacheService();
