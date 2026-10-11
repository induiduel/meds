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

  constructor(
    batchFn: (keys: K[]) => Promise<Map<K, V> | Array<V | null>>,
    options: { delayMs?: number; enableCache?: boolean } = {}
  ) {
    this.batchFn = batchFn;
    this.delayMs = options.delayMs ?? 50;
    this.enableCache = options.enableCache ?? true;
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
    if (this.enableCache) {
      this.cache.set(key, value);
    }
  }

  private async dispatchBatch() {
    this.timer = null;
    const currentQueue = new Map(this.queue);
    this.queue.clear();

    const keys = Array.from(currentQueue.keys());
    if (keys.length === 0) return;

    try {
      const result = await this.batchFn(keys);
      if (result instanceof Map) {
        for (const [key, waiters] of currentQueue.entries()) {
          const val = result.get(key);
          if (this.enableCache && val !== undefined) this.cache.set(key, val);
          waiters.forEach((w) => w.resolve(val as V));
        }
      } else if (Array.isArray(result)) {
        keys.forEach((key, idx) => {
          const val = result[idx];
          const waiters = currentQueue.get(key) || [];
          if (this.enableCache && val !== undefined && val !== null) this.cache.set(key, val as V);
          waiters.forEach((w) => w.resolve(val as V));
        });
      }
    } catch (err) {
      for (const waiters of currentQueue.values()) {
        waiters.forEach((w) => w.reject(err));
      }
    }
  }
}

/**
 * HTTP İstek Paketleyicisi (Request Batcher)
 * 50ms içindeki istekleri POST /api/batch altında birleştirir.
 */
class RequestBatcherService {
  private queue: {
    req: BatchRequestItem;
    resolve: (res: BatchResponseItem) => void;
    reject: (err: any) => void;
  }[] = [];
  private timer: any = null;
  private readonly WINDOW_MS = 50;

  /**
   * Bir URL isteğini paket havuzuna ekler.
   */
  public async fetchBatched<T = any>(
    url: string,
    options: {
      method?: 'GET' | 'POST' | 'PATCH' | 'DELETE';
      headers?: Record<string, string>;
      body?: any;
    } = {}
  ): Promise<T> {
    const id = `req_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    const reqItem: BatchRequestItem = {
      id,
      method: options.method || 'GET',
      url,
      headers: options.headers,
      body: options.body,
    };

    return new Promise<T>((resolve, reject) => {
      this.queue.push({
        req: reqItem,
        resolve: (resItem) => {
          if (resItem.status >= 200 && resItem.status < 300) {
            resolve(resItem.body as T);
          } else {
            reject(new Error(resItem.error || `HTTP ${resItem.status} error in batch request`));
          }
        },
        reject,
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

    if (batch.length === 0) return;

    // Eğer havuzda tek bir istek varsa doğrudan sunucuya gönderebilir veya batch uç noktasına iletebilir
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
        single.resolve({ status: res.status, body });
      } catch (err) {
        single.reject(err);
      }
      return;
    }

    // Birden fazla istek varsa tek bir POST /api/batch ile gönder
    try {
      const res = await fetch('/api/batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ requests: batch.map((b) => b.req) }),
      });

      if (!res.ok) {
        throw new Error(`Batch request failed with HTTP ${res.status}`);
      }

      const payload: BatchResponsePayload = await res.json();
      for (const item of batch) {
        const subRes = payload.responses?.[item.req.id];
        if (subRes) {
          item.resolve(subRes);
        } else {
          item.reject(new Error(`No sub-response received for batch request ${item.req.id}`));
        }
      }
    } catch (err) {
      for (const item of batch) {
        item.reject(err);
      }
    }
  }
}

export const requestBatcher = new RequestBatcherService();
