/**
 * Ağ katmanı — zayıf bağlantıda donma ve istek yığılmasını önler.
 *
 * installFetchGuard() tarayıcının fetch'ini bir kez sarar; böylece projedeki tüm istekler (ham fetch, safeJsonFetch,
 * Supabase istemcisi) aynı kurallara uyar:
 *  1. Zaman aşımı: yanıt BAŞLIKLARI gelene kadar süre tutulur (gövde indirmesi sınırsız). GET 15 sn, yazma 20 sn,
 *     yapay zekâ / uzun işler 120 sn. Çağıranın kendi AbortSignal'ı korunur ve zaman aşımıyla birleşir.
 *     Zaman aşımında AbortError değil ağ hatası (TypeError) atılır → mevcut çevrimdışı/önbellek yedekleri devreye girer.
 *  2. Birleştirme: aynı anda uçuşan özdeş GET istekleri (aynı URL + kimlik başlıkları) tek ağ isteği paylaşır.
 *  3. Bağlantı durumu: ardışık hata/zaman aşımı → "slow", navigator.onLine=false → "offline"; ilk başarılı yanıtta "online".
 *     useNetState() ve onNetChange() ile okunur; NetworkBanner ve usePoll bunu kullanır.
 */
import { useEffect, useRef, useSyncExternalStore } from 'react';

export type NetState = 'online' | 'slow' | 'offline';

const LONG_RE = /\/api\/(ai|studio|rag|admin\/scripts|admin\/phases\/question\/[^/]+\/(rereview|test)|notebooklm|past-question-reviews|phase14|transcri|upload|import|backup|drive|automation|v2\/cluster|learn\/ask)|reconstruct|optimize|\/generate|\/chat|\/stream|\/audit\/|\/master\//i;
const GET_TIMEOUT = 15_000;
const WRITE_TIMEOUT = 20_000;
const LONG_TIMEOUT = 120_000;
const ID_HEADERS = ['authorization', 'x-user-id', 'x-voter-uid', 'x-admin-email', 'apikey', 'range', 'accept'];

let state: NetState = typeof navigator !== 'undefined' && navigator.onLine === false ? 'offline' : 'online';
const listeners = new Set<() => void>();
let failTimes: number[] = [];

function setState(next: NetState) {
  if (next === state) return;
  state = next;
  listeners.forEach((l) => l());
}

export const getNetState = () => state;
/** Tarayıcı ya da sunucu yoklaması çevrimdışı diyorsa doğru (arka plan istekleri atlansın) */
export const cevrimdisiMi = () => state === 'offline' || (typeof navigator !== 'undefined' && navigator.onLine === false);
/** Çevrimdışıyken hiç atılmayan arka plan uçları (varlık, profil yedeği, müzik listesi eşitlemesi) */
const BG_RE = /\/api\/(presence|user-data\/backup|music\/playlist)(?:[/?#]|$)/;
export function onNetChange(cb: () => void) {
  listeners.add(cb);
  return () => listeners.delete(cb);
}
export function useNetState(): NetState {
  return useSyncExternalStore(onNetChange, getNetState, () => 'online');
}

function reportOk() {
  failTimes = [];
  if (state !== 'online' && (typeof navigator === 'undefined' || navigator.onLine !== false)) setState('online');
}
// Tek istek hatası (CORS, üçüncü taraf servis, sunucuda yavaş bir uç, SW'nin "ağ yok" yanıtı) bağlantı durumunu
// doğrudan değiştirmez: önce sunucu ayrıca yoklanır (/api/surum, SW'den geçmez). Yalnız yoklama da başarısızsa
// "offline", yoklama yavaşsa "slow" olur; yoklama hızlı yanıt verirse uyarı çıkmaz (2026-10-21: internet varken
// "Çevrimdışısın / Bağlantı geri geldi" uyarıları).
let nativeFetchRef: typeof fetch | null = null;
let probing: Promise<void> | null = null;
let lastProbe = 0;
function probe(suspect: 'offline' | 'slow') {
  if (probing || Date.now() - lastProbe < 5_000) return;
  const f = nativeFetchRef || (typeof fetch === 'function' ? fetch : null);
  if (!f) return setState(suspect);
  const ctl = new AbortController();
  const started = Date.now();
  const t = setTimeout(() => ctl.abort(), 6_000);
  probing = f(`/api/surum?t=${started}`, { cache: 'no-store', signal: ctl.signal })
    .then((r) => {
      if (!r.ok) throw new Error(String(r.status));
      if (Date.now() - started > 4_000) setState('slow');
      else reportOk();
    })
    .catch(() => setState(navigator.onLine === false ? 'offline' : suspect === 'offline' ? 'offline' : 'slow'))
    .finally(() => { clearTimeout(t); lastProbe = Date.now(); probing = null; });
}
/** SW ağa ulaşamadığını bildirdi (X-Cevrimdisi): sunucu yoklaması da başarısızsa "çevrimdışı" (Wi-Fi bağlı ama internetsiz) */
function reportOffline() {
  failTimes = [];
  if (typeof navigator !== 'undefined' && navigator.onLine === false) return setState('offline');
  probe('offline');
}
function reportFail() {
  if (typeof navigator !== 'undefined' && navigator.onLine === false) return setState('offline');
  const now = Date.now();
  failTimes = failTimes.filter((t) => now - t < 30_000);
  failTimes.push(now);
  if (failTimes.length >= 2) probe('slow');
}

/** Zaman aşımı: isteğin türüne göre ms. */
export function timeoutFor(url: string, method: string) {
  if (LONG_RE.test(url)) return LONG_TIMEOUT;
  return method === 'GET' || method === 'HEAD' ? GET_TIMEOUT : WRITE_TIMEOUT;
}

function anySignal(signals: AbortSignal[]): AbortSignal {
  const ctrl = new AbortController();
  for (const s of signals) {
    if (s.aborted) {
      ctrl.abort(s.reason);
      break;
    }
    s.addEventListener('abort', () => ctrl.abort(s.reason), { once: true });
  }
  return ctrl.signal;
}

let installed = false;
/** Ön plandaki (sayfanın beklediği) isteklerden yanıt başlığı henüz gelmemiş olanların sayısı */
let onUcus = 0;

/**
 * Arka plan indirmesi (çevrimdışı paketleri vb.): fetch korumasından geçmez, düşük öncelikle gider ve ön plan isteği
 * uçuşurken (ya da son 1,5 sn'de istek başladıysa) başlamadan bekler. Böylece Wi-Fi'de bile büyük ses/PDF indirmeleri
 * sayfa geçişlerini sıraya sokmaz.
 */
export async function arkaPlanFetch(url: string, init: RequestInit = {}): Promise<Response> {
  await onPlanBosalinca(init.signal || undefined);
  const f = nativeFetchRef || fetch;
  return f(url, { ...init, priority: 'low' } as RequestInit);
}
export async function onPlanBosalinca(signal?: AbortSignal) {
  const bas = Date.now();
  // Yalnız uçuşan ön plan isteği varsa ve en çok 2 sn bekler. (Eskiden "son 1,5 sn'de istek" de bekletiyor ve sınır 20 sn idi:
  // saniyede yoklayan ekranlarda her dosya 20 sn bekliyor, yüzlerce dosyalı paket "sırada" takılı görünüyordu.)
  while (onUcus > 0 && Date.now() - bas < 2_000 && !signal?.aborted) {
    await new Promise((r) => setTimeout(r, 300));
  }
}

export function installFetchGuard() {
  if (installed || typeof window === 'undefined' || typeof window.fetch !== 'function') return;
  installed = true;
  const nativeFetch = window.fetch.bind(window);
  nativeFetchRef = nativeFetch;
  type Waiter = [(r: Response) => void, (e: unknown) => void];
  const inflight = new Map<string, Waiter[]>();

  const guarded = async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
    const req = input instanceof Request ? input : null;
    const url = typeof input === 'string' ? input : input instanceof URL ? input.href : req!.url;
    if (!/^(https?:|\/)/i.test(url) || url.includes('/@vite') || url.includes('/node_modules/')) return nativeFetch(input, init);
    const method = String(init?.method || req?.method || 'GET').toUpperCase();
    // Çevrimdışıyken arka plan istekleri ağa hiç çıkmaz (2026-10-28): bunlar yalnız durum/eşitleme içindir, başarısızlıkları
    // yeniden denenir; boşuna atılınca SW 503'ü + zaman aşımı + reportFail gürültüsü üretiyordu. /api/surum burada değil:
    // bağlantı yoklaması (baglanti.ts) onu kullanır; sürüm denetimi UpdatePrompt'ta ayrıca atlanır.
    if (BG_RE.test(url) && cevrimdisiMi()) throw new TypeError('Çevrimdışı: arka plan isteği atlandı');
    const headers = new Headers(init?.headers || req?.headers || undefined);
    // Yazma isteklerinde herkese açık cihaz kimliği (yönetim › Kişiler eylem günlüğü). GET'e eklenmez: çapraz kökende
    // her GET'e ön-kontrol binmesin. Kimlik presence.ts'te türetilir; henüz yoksa eklenmez.
    let sendInit = init;
    if (method !== 'GET' && method !== 'HEAD' && url.includes('/api/') && !headers.has('x-device-id')) {
      let pub = '';
      try { pub = localStorage.getItem('medsoru_device_pub') || ''; } catch { /* gizli pencere */ }
      if (pub) {
        headers.set('x-device-id', pub);
        sendInit = { ...init, headers };
      }
    }

    const run = async () => {
      onUcus++;
      const timer = new AbortController();
      const ms = timeoutFor(url, method);
      let timedOut = false;
      const t = window.setTimeout(() => {
        timedOut = true;
        timer.abort();
      }, ms);
      const callerSignal = init?.signal || req?.signal || null;
      const signal = callerSignal ? anySignal([callerSignal, timer.signal]) : timer.signal;
      try {
        const res = await nativeFetch(input, { ...sendInit, signal });
        // SW'nin internetsiz yanıtları (cihazdaki kopya / "ağ yok" 503'ü) bağlantı geldi sayılmaz
        if (res.headers.get('X-Cevrimdisi')) reportOffline();
        else if (res.headers.get('X-From-Cache') !== '1') reportOk();
        return res;
      } catch (err: any) {
        if (timedOut) {
          reportFail();
          throw new TypeError(`Bağlantı zaman aşımına uğradı (${Math.round(ms / 1000)} sn)`);
        }
        if (err?.name !== 'AbortError') reportFail();
        throw err;
      } finally {
        window.clearTimeout(t);
        onUcus--;
      }
    };

    // Özdeş GET'leri birleştir: ilk çağıran özgün yanıtı alır; bekleyenlere yanıt gelir gelmez (ilk çağıran
    // gövdeyi okumadan önce) kopya verilir. Bekleyen yoksa kopya yapılmaz → büyük gövdeler iki kez tutulmaz.
    // Kendi iptal sinyali olan istekler birleştirilmez (bir çağıranın iptali ötekini düşürmesin)
    if (method === 'GET' && !init?.body && !init?.signal && !req?.signal) {
      const key = url + '|' + ID_HEADERS.map((h) => headers.get(h) || '').join('|');
      const waiting = inflight.get(key);
      if (waiting) return new Promise<Response>((resolve, reject) => waiting.push([resolve, reject]));
      const waiters: Waiter[] = [];
      inflight.set(key, waiters);
      const p = run();
      p.then(
        (r) => {
          inflight.delete(key);
          for (const [resolve, reject] of waiters) {
            try { resolve(r.clone()); } catch (e) { reject(e); }
          }
        },
        (e) => {
          inflight.delete(key);
          for (const [, reject] of waiters) reject(e);
        }
      );
      return p;
    }
    return run();
  };

  window.fetch = guarded as typeof window.fetch;
  window.addEventListener('online', () => {
    failTimes = [];
    setState('online');
  });
  window.addEventListener('offline', () => setState('offline'));
}

/**
 * Yoklama kancası: önceki çağrı bitmeden yenisini başlatmaz, sekme gizliyken ve çevrimdışıyken durur,
 * hatada aralığı ikiye katlar (en çok 8×). `fn` güncel kalır (ref).
 */
export function usePoll(fn: () => Promise<unknown> | unknown, ms: number, enabled = true) {
  const fnRef = useRef(fn);
  fnRef.current = fn;
  useEffect(() => {
    if (!enabled) return;
    let stopped = false;
    let busy = false;
    let factor = 1;
    let timer: number | undefined;
    const schedule = () => {
      if (!stopped) timer = window.setTimeout(tick, ms * factor);
    };
    const tick = async () => {
      if (stopped) return;
      if (busy || document.hidden || getNetState() === 'offline') return schedule();
      busy = true;
      try {
        await fnRef.current();
        factor = 1;
      } catch {
        factor = Math.min(8, factor * 2);
      } finally {
        busy = false;
        schedule();
      }
    };
    schedule();
    const onVis = () => {
      if (!document.hidden && !busy) {
        window.clearTimeout(timer);
        void tick();
      }
    };
    document.addEventListener('visibilitychange', onVis);
    return () => {
      stopped = true;
      window.clearTimeout(timer);
      document.removeEventListener('visibilitychange', onVis);
    };
  }, [ms, enabled]);
}

/**
 * Tek uçuş kilidi: aynı anahtarla bir işlem sürerken yeni çağrı onu bekler, ikinci istek atılmaz.
 * Düğmelerde çift dokunuşla yığılan yazmaları önler.
 */
const locks = new Map<string, Promise<unknown>>();
export function singleFlight<T>(key: string, fn: () => Promise<T>): Promise<T> {
  const cur = locks.get(key) as Promise<T> | undefined;
  if (cur) return cur;
  const p = fn().finally(() => locks.delete(key));
  locks.set(key, p);
  return p;
}

/**
 * setInterval yerine: önceki çağrı bitmeden yenisini başlatmaz (yavaş ağda istekler üst üste yığılmaz),
 * sekme gizliyken ve çevrimdışıyken atlar. Dönen işlev aralığı durdurur.
 */
export function guardedInterval(fn: () => unknown, ms: number): () => void {
  let busy = false;
  const id = window.setInterval(async () => {
    if (busy || document.hidden || getNetState() === 'offline') return;
    busy = true;
    try {
      await fn();
    } catch {
      /* çağıran kendi hatasını gösterir */
    } finally {
      busy = false;
    }
  }, ms);
  return () => window.clearInterval(id);
}
