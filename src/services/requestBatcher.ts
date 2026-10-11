/**
 * src/services/requestBatcher.ts
 *
 * İstekleri Tekilleştirme ve Paketleme (Request Deduplication & Batching)
 *
 * 1. Deduplication (Tekilleştirme): Aynı anda veya aynı zaman penceresinde tetiklenen
 *    özdeş istekler yakalanır; sunucuya tek bir HTTP isteği gönderilir ve yanıt
 *    tüm dinleyicilere dağıtılır.
 * 2. Batching (Paketleme / DataLoader Mantığı): 50 ms zaman penceresi içinde çıkan
 *    farklı tekil istekler (GET /questions/1, GET /questions/2 vb.) birleştirilerek
 *    sunucuya tek bir POST /api/batch çağrısı ile topluca iletilir.
 */

export interface BatchRequestItem {
  id: string;
  method?: 'GET' | 'POST' | 'PATCH' | 'DELETE';
  url: string;
  headers?: Record<string, string>;
  body?: any;
}

export interface BatchResponseItem {
  status: number;
  headers?: Record<string, string>;
  body: any;
  error?: string;
}

export interface BatchResponsePayload {
  responses: Record<string, BatchResponseItem>;
}

/**
 * DataLoader Deseni: Tekil nesne getirme isteklerini 50ms'lik bir havuzda toplar
 * ve tek bir toplu işlemle sunucudan çeker.
 */
export class DataLoader<K, V> {
  private batchFn: (keys: K[]) => Promise<Map<K, V> | Array<V | null>>;
  private queue = new Map<K, { resolve: (val: V) => void; reject: (err: any) => void }[]>();
  private timer: any = null;
  private delayMs: number;
  private cache = new Map<K, V>();
  private enableCache: boolean;
  private maxCacheSize: number;
  private maxBatchSize: number;

  constructor(
    batchFn: (keys: K[]) => Promise<Map<K, V> | Array<V | null>>,
    options: { delayMs?: number; enableCache?: boolean; maxCacheSize?: number; maxBatchSize?: number } = {}
  ) {
    this.batchFn = batchFn;
    this.delayMs = options.delayMs ?? 50;
    this.enableCache = options.enableCache ?? true;
    this.maxCacheSize = options.maxCacheSize ?? 1000;
    this.maxBatchSize = options.maxBatchSize ?? 50;
  }

  private setCache(key: K, val: V) {
    if (!this.enableCache) return;
    if (this.cache.size >= this.maxCacheSize) {
      const oldestKey = this.cache.keys().next().value;
      if (oldestKey !== undefined) this.cache.delete(oldestKey);
    }
    this.cache.set(key, val);
  }

  public async load(key: K): Promise<V> {
    if (this.enableCache && this.cache.has(key)) {
      return this.cache.get(key)!;
    }

    return new Promise<V>((resolve, reject) => {
      const waiters = this.queue.get(key) || [];
      waiters.push({ resolve, reject });
      this.queue.set(key, waiters);

      if (!this.timer) {
        this.timer = setTimeout(() => this.dispatchBatch(), this.delayMs);
      }
    });
  }

  public async loadMany(keys: K[]): Promise<V[]> {
    return Promise.all(keys.map((k) => this.load(k)));
  }

  public clear(key?: K) {
    if (key !== undefined) {
      this.cache.delete(key);
    } else {
      this.cache.clear();
    }
  }

  public prime(key: K, value: V) {
    this.setCache(key, value);
  }

  private async dispatchBatch() {
    this.timer = null;
    const currentQueue = new Map(this.queue);
    this.queue.clear();

    const allKeys = Array.from(currentQueue.keys());
    if (allKeys.length === 0) return;

    // maxBatchSize dilimleriyle parçala
    for (let i = 0; i < allKeys.length; i += this.maxBatchSize) {
      const keys = allKeys.slice(i, i + this.maxBatchSize);
      try {
        const result = await this.batchFn(keys);
        if (result instanceof Map) {
          for (const key of keys) {
            const waiters = currentQueue.get(key) || [];
            const val = result.get(key);
            if (val !== undefined) this.setCache(key, val);
            waiters.forEach((w) => w.resolve(val as V));
          }
        } else if (Array.isArray(result)) {
          keys.forEach((key, idx) => {
            const val = result[idx];
            const waiters = currentQueue.get(key) || [];
            if (val !== undefined && val !== null) this.setCache(key, val as V);
            waiters.forEach((w) => w.resolve(val as V));
          });
        }
      } catch (err) {
        for (const key of keys) {
          const waiters = currentQueue.get(key) || [];
          waiters.forEach((w) => w.reject(err));
        }
      }
    }
  }
}

/**
 * HTTP İstek Paketleyicisi (Request Batcher)
 * 50ms içindeki istekleri POST /api/batch altında birleştirir.
 * Özdeş GET isteklerini tekilleştirir, 50 üstü istekleri güvenli paketler halinde böler.
 */
class RequestBatcherService {
  private queue: {
    req: BatchRequestItem;
    waiters: {
      resolve: (res: BatchResponseItem) => void;
      reject: (err: any) => void;
    }[];
  }[] = [];
  private getDedupeMap = new Map<string, BatchRequestItem>();
  private timer: any = null;
  private readonly WINDOW_MS = 50;
  private readonly MAX_BATCH_SIZE = 50;

  /**
   * Bir URL isteğini paket havuzuna ekler. Özdeş GET istekleri havuz içinde tekilleştirilir.
   */
  public async fetchBatched<T = any>(
    url: string,
    options: {
      method?: 'GET' | 'POST' | 'PATCH' | 'DELETE';
      headers?: Record<string, string>;
      body?: any;
    } = {}
  ): Promise<T> {
    const method = options.method || 'GET';
    const isGet = method === 'GET';
    const dedupeKey = isGet ? `${url}|${JSON.stringify(options.headers || {})}` : null;

    return new Promise<T>((resolve, reject) => {
      const waiter = {
        resolve: (resItem: BatchResponseItem) => {
          if (resItem.status >= 200 && resItem.status < 300) {
            resolve(resItem.body as T);
          } else {
            reject(new Error(resItem.error || `HTTP ${resItem.status} error in batch request`));
          }
        },
        reject,
      };

      // Özdeş GET isteği pencere içinde zaten varsa yeni bir HTTP kaydı açma, garsonu ona bağla
      if (dedupeKey && this.getDedupeMap.has(dedupeKey)) {
        const existingReq = this.getDedupeMap.get(dedupeKey)!;
        const entry = this.queue.find((q) => q.req.id === existingReq.id);
        if (entry) {
          entry.waiters.push(waiter);
          return;
        }
      }

      const id = `req_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
      const reqItem: BatchRequestItem = {
        id,
        method,
        url,
        headers: options.headers,
        body: options.body,
      };

      if (dedupeKey) {
        this.getDedupeMap.set(dedupeKey, reqItem);
      }

      this.queue.push({
        req: reqItem,
        waiters: [waiter],
      });

      if (!this.timer) {
        this.timer = setTimeout(() => this.flush(), this.WINDOW_MS);
      }
    });
  }

  private async flush() {
    this.timer = null;
    const batch = [...this.queue];
    this.queue = [];
    this.getDedupeMap.clear();

    if (batch.length === 0) return;

    // Eğer havuzda tek bir istek varsa doğrudan sunucuya gönderebilir
    if (batch.length === 1) {
      const single = batch[0];
      try {
        const res = await fetch(single.req.url, {
          method: single.req.method,
          headers: single.req.headers,
          body: single.req.body ? JSON.stringify(single.req.body) : undefined,
        });
        const contentType = res.headers.get('content-type') || '';
        const body = contentType.includes('application/json') ? await res.json() : await res.text();
        single.waiters.forEach((w) => w.resolve({ status: res.status, body }));
      } catch (err) {
        single.waiters.forEach((w) => w.reject(err));
      }
      return;
    }

    // 50'den fazla istek varsa MAX_BATCH_SIZE (50) dilimlerine bölerek sunucu limitini aşma
    const chunks: typeof batch[] = [];
    for (let i = 0; i < batch.length; i += this.MAX_BATCH_SIZE) {
      chunks.push(batch.slice(i, i + this.MAX_BATCH_SIZE));
    }

    await Promise.all(
      chunks.map(async (chunk) => {
        try {
          const res = await fetch('/api/batch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ requests: chunk.map((b) => b.req) }),
          });

          if (!res.ok) {
            throw new Error(`Batch request failed with HTTP ${res.status}`);
          }

          const payload: BatchResponsePayload = await res.json();
          for (const item of chunk) {
            const subRes = payload.responses?.[item.req.id];
            if (subRes) {
              item.waiters.forEach((w) => w.resolve(subRes));
            } else {
              const err = new Error(`No sub-response received for batch request ${item.req.id}`);
              item.waiters.forEach((w) => w.reject(err));
            }
          }
        } catch (err) {
          for (const item of chunk) {
            item.waiters.forEach((w) => w.reject(err));
          }
        }
      })
    );
  }
}

export const requestBatcher = new RequestBatcherService();
