// MeDSor Service Worker - PWA v8: Yüksek Hızlı Açılış, Optimize Edilmiş Bellek & Modül Parçalama
const CACHE_VERSION = 'medsoru-pwa-v14';
const STATIC_CACHE = `medsoru-static-${CACHE_VERSION}`;
const RUNTIME_CACHE = `medsoru-runtime-${CACHE_VERSION}`;
const DATA_CACHE = `medsoru-data-${CACHE_VERSION}`;
// Canlı ders çevrimdışı paketleri (canliDersCevrimdisi.ts): sürüm temizliğinde silinmez, yalnız kullanıcı siler
const CD_OFFLINE_CACHE = 'medsoru-canli-ders-offline';
/** Arka planda (Background Fetch) inen ders dosyaları; uygulama açılınca kaydedilir (canliDersCevrimdisi.ts) */
const CD_BEKLEYEN_CACHE = 'medsoru-cd-bekleyen';

// Cihazdaki canlı ders sesleri: yol → sürüm (X-Cd-Surum). İstemci değiştirince CD_OFFLINE_CHANGED gönderir.
let cdSesler = null;
let cdSesYukle = null;
function cdSesleriYukle() {
  cdSesYukle = caches
    .open(CD_OFFLINE_CACHE)
    .then(async (c) => {
      const m = new Map();
      for (const r of await c.keys()) {
        const u = new URL(r.url);
        if (!u.pathname.startsWith('/api/canli-ders/ses/')) continue;
        const res = await c.match(r);
        m.set(u.pathname, res ? res.headers.get('X-Cd-Surum') || '' : '');
      }
      cdSesler = m;
    })
    .catch(() => { cdSesler = new Map(); });
  return cdSesYukle;
}
cdSesleriYukle();

/** Önbellekteki tam MP3'ten Range isteğine 206 (yoksa 200) yanıt */
async function cdSesYanit(req, url) {
  const c = await caches.open(CD_OFFLINE_CACHE);
  const hit = await c.match(url.origin + url.pathname);
  if (!hit) return null;
  const blob = await hit.blob();
  const size = blob.size;
  const range = req.headers.get('range');
  const m = range && /bytes=(\d*)-(\d*)/.exec(range);
  if (!m) {
    return new Response(blob, { status: 200, headers: { 'Content-Type': 'audio/mpeg', 'Content-Length': String(size), 'Accept-Ranges': 'bytes' } });
  }
  let start = m[1] === '' ? Math.max(0, size - Number(m[2])) : Number(m[1]);
  let end = m[1] !== '' && m[2] !== '' ? Math.min(size - 1, Number(m[2])) : size - 1;
  if (start >= size || start > end) {
    return new Response(null, { status: 416, headers: { 'Content-Range': `bytes */${size}` } });
  }
  return new Response(blob.slice(start, end + 1), {
    status: 206,
    headers: {
      'Content-Type': 'audio/mpeg',
      'Content-Length': String(end - start + 1),
      'Content-Range': `bytes ${start}-${end}/${size}`,
      'Accept-Ranges': 'bytes',
    },
  });
}

const PRECACHE_ASSETS = [
  '/index.html',
  '/manifest.json',
  '/favicon.ico',
  '/favicon.png',
  '/apple-touch-icon.png',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  '/icons/maskable-icon-192x192.png',
  '/icons/maskable-icon-512x512.png',
];

// Varsayılan komiteler (çevrimdışıyken sunucuya hiç ulaşılamasa dahi arayüzün boş kalmasını önler)
const DEFAULT_OFFLINE_COMMITTEES = [
  { id: 'donem3-kurul1', name: 'Dönem 3 Kurul 1', targetCount: 100 },
  { id: 'donem3-kurul2', name: 'Dönem 3 Kurul 2', targetCount: 100 },
  { id: 'donem3-kurul3', name: 'Dönem 3 Kurul 3', targetCount: 100 },
  { id: 'donem3-kurul4', name: 'Dönem 3 Kurul 4', targetCount: 100 },
  { id: 'donem3-kurul5', name: 'Dönem 3 Kurul 5', targetCount: 100 },
  { id: 'donem3-kurul6', name: 'Dönem 3 Kurul 6', targetCount: 100 }
];

// 1. Kurulum (Install) - Statik çekirdek dosyaları önbelleğe al (SPA rotaları için index.html tek kez çekilir)
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(STATIC_CACHE)
      .then((cache) => {
        return Promise.all(
          PRECACHE_ASSETS.map((url) =>
            fetch(url)
              .then(async (res) => {
                if (res.ok) {
                  if (url === '/index.html') {
                    await cache.put('/', res.clone());
                  }
                  return cache.put(url, res);
                }
              })
              .catch((err) => {
                console.warn('[SW] Precache atlandı:', url, err);
              })
          )
        );
      })
      .then(() => self.skipWaiting())
  );
});

// 2. Aktivasyon (Activate) - Eski önbellekleri temizle ve istemcileri hemen devral
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => {
        return Promise.all(
          keys.map((key) => {
            if (key !== STATIC_CACHE && key !== RUNTIME_CACHE && key !== DATA_CACHE && key !== 'medsoru-pdf-offline' && key !== CD_OFFLINE_CACHE && key !== CD_BEKLEYEN_CACHE) {
              console.log('[SW] Eski önbellek temizleniyor:', key);
              return caches.delete(key);
            }
          })
        );
      })
      .then(() => self.clients.claim())
  );
});

// 3. İstek Yönetimi (Fetch)
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Sadece GET isteklerini önbellekle
  if (req.method !== 'GET') {
    return;
  }

  // Tarayıcı içi / eklenti protokollerini atla
  if (!url.protocol.startsWith('http')) {
    return;
  }

  // A. Sayfa Gezinme İstekleri (SPA HTML - Navigate)
  // Çevrimdışıyken veya zayıf ağda 1.2 saniyeden uzun bekletme: doğrudan önbellekteki index.html'i ver!
  if (req.mode === 'navigate') {
    event.respondWith(
      (async () => {
        // Ağ isteği ile önbellek yedeklemesini yarıştır
        const fetchPromise = fetch(req)
          .then((networkRes) => {
            if (networkRes && networkRes.status === 200) {
              const clone = networkRes.clone();
              caches.open(STATIC_CACHE).then((cache) => {
                cache.put(req, clone.clone());
                cache.put('/index.html', clone.clone());
                cache.put('/', clone);
              });
            }
            return networkRes;
          })
          .catch(() => null);

        // Ağ 400ms içinde yanıt verirse ağı kullan, gecikirse beklemeden anında önbellekteki App Shell'i ver (arka planda güncellenir)
        const timeoutPromise = new Promise((resolve) => setTimeout(() => resolve(null), 400));
        const fastNetworkRes = await Promise.race([fetchPromise, timeoutPromise]);

        if (fastNetworkRes) {
          return fastNetworkRes;
        }

        // Ağ gecikti veya başarısız oldu: Önce önbelleklerde index.html ara
        // (ignoreVary: kayıtlı yanıt 'Vary: Accept-Encoding' taşır; başlıksız '/index.html' isteğiyle eşleşmiyordu)
        const matchDirect = await caches.match(req, { ignoreSearch: true, ignoreVary: true });
        if (matchDirect) return matchDirect;

        const matchHtml =
          (await caches.match('/index.html', { ignoreSearch: true, ignoreVary: true })) ||
          (await caches.match('/', { ignoreSearch: true, ignoreVary: true }));
        if (matchHtml) return matchHtml;

        const allKeys = await caches.keys();
        for (const k of allKeys) {
          const c = await caches.open(k);
          const found =
            (await c.match('/index.html', { ignoreSearch: true, ignoreVary: true })) ||
            (await c.match('/', { ignoreSearch: true, ignoreVary: true }));
          if (found) return found;
        }

        // Ağ isteği arka planda tamamlanırsa son çare bekle
        const slowRes = await fetchPromise;
        if (slowRes) return slowRes;

        // Son çare: Temel SPA HTML iskeleti dönerek sayfanın takılmasını önle
        return new Response(
          `<!doctype html>
          <html lang="tr">
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
              <title>MeDSor · Çevrimdışı Mod</title>
              <link rel="stylesheet" href="/assets/asset-index.css">
            </head>
            <body class="bg-slate-900 text-white flex items-center justify-center min-h-screen p-4 text-center font-sans">
              <div class="max-w-md w-full p-6 bg-slate-800 rounded-2xl border border-slate-700 shadow-xl space-y-4">
                <div class="text-3xl">⚡</div>
                <h1 class="text-xl font-bold">MeDSor Çevrimdışı Mod</h1>
                <p class="text-sm text-slate-300">İnternet bağlantısı algılanamadı. Uygulama veritabanınız cihazınızda kuruluysa lütfen ana sayfaya dönünüz.</p>
                <a href="/" class="inline-block px-5 py-2.5 bg-teal-600 hover:bg-teal-500 text-white font-semibold rounded-xl text-sm transition-colors">
                  Ana Sayfaya Dön
                </a>
              </div>
            </body>
          </html>`,
          { headers: { 'Content-Type': 'text/html; charset=utf-8' } }
        );
      })()
    );
    return;
  }

  // Canlı ders sesi cihazdaysa: aynı sürümse doğrudan cihazdan (Range/206), değilse önce ağ, ağ yoksa cihazdaki kopya.
  // Cihazda olmayan ses SW'den hiç geçmez (aşağıdaki API dalında atlanır).
  if (url.pathname.startsWith('/api/canli-ders/ses/') && !url.searchParams.has('indir')) {
    const karar = (m) => {
      if (!m.has(url.pathname)) return null;
      const surum = m.get(url.pathname);
      const istenen = url.searchParams.get('v');
      if (!istenen || !surum || istenen === surum) return cdSesYanit(req, url).then((r) => r || fetch(req));
      return fetch(req).catch(() => cdSesYanit(req, url).then((r) => r || Response.error()));
    };
    if (cdSesler) {
      const p = karar(cdSesler);
      if (p) {
        event.respondWith(p);
        return;
      }
    } else {
      event.respondWith((cdSesYukle || cdSesleriYukle()).then(() => karar(cdSesler) || fetch(req)));
      return;
    }
  }

  // PDF.js yardımcı dosyaları (yazı tipi, wasm, ICC, CMap): sürüme bağlı, değişmez → önbellek önce
  if (url.pathname.startsWith('/vendor/pdfjs/')) {
    event.respondWith(
      (async () => {
        const cached = await caches.match(req, { ignoreSearch: true, ignoreVary: true });
        if (cached) return cached;
        const res = await fetch(req);
        if (res && res.status === 200) {
          const clone = res.clone();
          caches.open(RUNTIME_CACHE).then((cache) => cache.put(req, clone)).catch(() => {});
        }
        return res;
      })()
    );
    return;
  }

  // B. Statik Varlıklar (JS, CSS, Fontlar, İkonlar, Resimler)
  // İçerik özetli (/assets/) dosyalar değişmez (immutable) olduğundan tam Cache-First uygulanır (gereksiz arka plan ağ trafiği sıfırlanır)
  if (
    url.pathname.startsWith('/assets/') ||
    url.pathname.startsWith('/icons/') ||
    url.pathname.startsWith('/fonts/') ||
    /\.(js|css|woff2?|ttf|png|jpe?g|gif|svg|ico)$/i.test(url.pathname)
  ) {
    const isImmutableAsset = url.pathname.startsWith('/assets/');
    event.respondWith(
      (async () => {
        const cached = await caches.match(req, { ignoreSearch: true, ignoreVary: true });
        if (cached && isImmutableAsset) {
          return cached;
        }

        const fetchPromise = fetch(req)
          .then((networkRes) => {
            if (networkRes && networkRes.status === 200) {
              const clone = networkRes.clone();
              caches.open(RUNTIME_CACHE).then((cache) => {
                cache.put(req, clone);
              });
            }
            return networkRes;
          })
          .catch(() => null);

        if (cached) {
          return cached;
        }

        const networkRes = await fetchPromise;
        if (networkRes) return networkRes;

        // Önbellekte de yoksa ve ağ kapalıysa: 503 döndürerek React.lazy / wrapLazy catch mekanizmasının güvenle devreye girmesini sağla
        if (url.pathname.endsWith('.js') || url.pathname.includes('.js?')) {
          return new Response('/* Offline fallback: Module not cached */', {
            status: 503,
            statusText: 'Service Unavailable (Offline)',
            headers: { 'Content-Type': 'text/plain; charset=utf-8' },
          });
        }
        if (url.pathname.endsWith('.css') || url.pathname.includes('.css?')) {
          return new Response('/* Offline fallback stylesheet */', {
            headers: { 'Content-Type': 'text/css; charset=utf-8' },
          });
        }

        return new Response('', { status: 404 });
      })()
    );
    return;
  }

  // C. API İstekleri (/api/...)
  // Network-First, bağlantı hatasında güvenli veri mock'una veya veri önbelleğine düş
  if (url.pathname.startsWith('/api/')) {
    // Akış (SSE) ve canlı uçlar SW'den GEÇMEZ: yakalanan sonsuz akış (önbellek kopyası da okunuyordu) sayfa yenilense de
    // kapanmıyor, her açılışta bir bağlantı daha birikiyor; HTTP/1.1'in 6 bağlantı sınırı dolunca sayfalar "Yükleniyor"da kalıyordu
    if (
      (req.headers.get('accept') || '').includes('text/event-stream') ||
      url.pathname.startsWith('/api/realtime/') ||
      url.pathname.startsWith('/api/live/') ||
      url.pathname.startsWith('/api/presence') ||
      url.pathname.startsWith('/api/canli-ders/ses/') || // ses akışı (Range/206): tarayıcı doğrudan alır, önbelleğe yazılmaz
      url.pathname.startsWith('/api/patoloji-asistan/ses/') || // sınav asistanı EMA klipleri (Range/206)
      url.pathname.startsWith('/api/patoloji-cozucu/ses/') || // soru çözücü EMA klipleri (Range/206)
      url.pathname.includes('/events') ||
      url.pathname.includes('/stream') ||
      url.pathname.includes('/sse') ||
      url.pathname.includes('/heartbeat') ||
      url.pathname.includes('/ai/') ||
      url.pathname.includes('/backup')
    ) {
      return;
    }

    // Büyük tam listeler IndexedDB'de tutulur; SW önbelleğine ikinci kopya yazılmaz
    // Kişiye özel yanıtlar (notlar, profil, kullanıcı verisi, kimlik başlıklı istekler) asla önbelleğe alınmaz:
    // anahtar yalnız URL olduğundan aynı cihazdaki sonraki öğrenciye verilirdi.
    const personal =
      /^\/api\/(notes|user-data|users|profile|me|my-|people|presence|learn\/social|ornek)/.test(url.pathname) ||
      req.headers.has('authorization') || req.headers.has('x-user-id') || req.headers.has('x-user-uid');
    const cacheable = !personal && !/\/api\/past-exams(\/?$|\/sync)/.test(url.pathname) && !url.pathname.includes('/admin/');

    event.respondWith(
      (async () => {
        const network = fetch(req).then((networkRes) => {
          if (cacheable && networkRes && networkRes.status === 200) {
            const clone = networkRes.clone();
            // Anahtar TAM URL'dir (sorgu dizesi dahil): ?committee=k1 ile ?committee=k2 birbirini ezmez
            caches.open(DATA_CACHE).then((cache) => cache.put(req.url, clone)).catch(() => {});
          }
          return networkRes;
        });
        // Zayıf ağ: 4 sn içinde yanıt yoksa önbellekteki kopya hemen verilir (ağ arka planda önbelleği tazeler)
        const cached = cacheable ? await caches.match(req.url) : undefined;
        if (cached) {
          const slow = new Promise((resolve) => setTimeout(() => resolve(null), 4000));
          const winner = await Promise.race([network.catch(() => null), slow]);
          if (winner) return winner;
          const headers = new Headers(cached.headers);
          headers.set('X-From-Cache', '1');
          return new Response(await cached.clone().blob(), { status: cached.status, statusText: cached.statusText, headers });
        }
        try {
          return await network;
        } catch (err) {
          // Önbellekte yok ve ağ yok: komite listesi gerçek varsayılanlarla, diğerleri dürüst 503 ile döner
          // (eskiden boş liste 200 dönüyordu → istemci "veri yok" sanıp boş ekran gösteriyordu)
          if (url.pathname.includes('/api/committees')) {
            return new Response(JSON.stringify({ offline: true, committees: DEFAULT_OFFLINE_COMMITTEES }), {
              headers: { 'Content-Type': 'application/json', 'X-From-Cache': '1' },
              status: 200,
            });
          }
          return new Response(JSON.stringify({ offline: true, error: 'Ağ bağlantısı yok (çevrimdışı)' }), {
            headers: { 'Content-Type': 'application/json' },
            status: 503,
          });
        }
      })()
    );
    return;
  }
});

// 4. Arka Plan Senkronizasyonu (Background Sync)
// Açık pencere varsa boşaltmayı o yapar (aynı kuyruğu iki taraf birden göndermesin); yoksa SW kuyruğu kendisi gönderir.
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-offline-actions' || event.tag === 'medsoru-sync') {
    event.waitUntil(arkaPlanEsitle());
  }
});

// 5. Periyodik Arka Plan Senkronizasyonu (Periodic Background Sync): kuyruk + önbellekteki herkese açık verileri tazele
self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'update-database' || event.tag === 'medsoru-daily-sync') {
    event.waitUntil(arkaPlanEsitle().then(veriOnbelleginiTazele));
  }
});

async function notifyClientsToSync() {
  const clientList = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
  for (const client of clientList) {
    client.postMessage({ type: 'MEDSORU_BACKGROUND_SYNC' });
  }
  return clientList.length;
}

async function arkaPlanEsitle() {
  if (await notifyClientsToSync()) return;
  await kuyruguBosalt();
}

/** offlineDatabaseService ile aynı IndexedDB kuyruğu (medsoru_offline_db › offline_queue). Sürüm verilmez: şema yükseltmesi uygulamanındır. */
function kuyrukDb() {
  return new Promise((resolve) => {
    try {
      const req = indexedDB.open('medsoru_offline_db');
      req.onsuccess = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains('offline_queue')) { db.close(); resolve(null); } else resolve(db);
      };
      req.onupgradeneeded = () => { try { req.transaction.abort(); } catch (_) {} };
      req.onerror = () => resolve(null);
    } catch (_) { resolve(null); }
  });
}
const idbIstek = (r) => new Promise((ok, hata) => { r.onsuccess = () => ok(r.result); r.onerror = () => hata(r.error); });

async function kuyruguBosalt() {
  const db = await kuyrukDb();
  if (!db) return;
  try {
    const hepsi = await idbIstek(db.transaction('offline_queue', 'readonly').objectStore('offline_queue').getAll());
    let gonderilen = 0;
    let kalan = 0;
    for (const act of hepsi) {
      if (!act.url) { kalan++; continue; } // eski kayıt: mutlak adresi yok, uygulama açılınca gider
      let ok = false;
      let kalici = false;
      try {
        const res = await fetch(act.url, {
          method: act.method,
          headers: { 'Content-Type': 'application/json' },
          body: act.method === 'DELETE' && act.payload == null ? undefined : JSON.stringify(act.payload),
        });
        ok = res.ok;
        kalici = !ok && res.status >= 400 && res.status < 500 && res.status !== 408 && res.status !== 429 && res.status !== 401 && res.status !== 403;
      } catch (_) {
        // Ağ yok: tarayıcı sync olayını yeniden dener
        throw new Error('ag-yok');
      }
      const st = db.transaction('offline_queue', 'readwrite').objectStore('offline_queue');
      if (ok || kalici) { await idbIstek(st.delete(act.id)); if (ok) gonderilen++; }
      else { await idbIstek(st.put({ ...act, attempts: (act.attempts || 0) + 1 })); kalan++; }
    }
    if (gonderilen && self.registration.showNotification) {
      await self.registration.showNotification('MeDSor', {
        body: `Bekleyen ${gonderilen} işlem arka planda gönderildi.`,
        icon: '/icons/icon-192x192.png', badge: '/icons/icon-96x96.png', tag: 'medsoru-kuyruk', silent: true,
      }).catch(() => {});
    }
    if (kalan) throw new Error('kuyruk-bekliyor'); // sync yeniden zamanlansın
  } finally {
    db.close();
  }
}

/** Veri önbelleğindeki herkese açık GET yanıtlarını (en çok 40) arka planda yeniler. */
async function veriOnbelleginiTazele() {
  const cache = await caches.open(DATA_CACHE);
  const keys = (await cache.keys()).slice(0, 40);
  await Promise.all(keys.map(async (req) => {
    try {
      const res = await fetch(req.url, { cache: 'no-store' });
      if (res.ok) await cache.put(req.url, res);
    } catch (_) { /* sonraki tur */ }
  }));
}

// 4b. Arka plan indirme (Background Fetch): canlı ders ses + PDF'leri. Kimlik `cd|<ders>|<vid,vid>`.
// Sayfa açıksa sonucu kendisi okur; burada dosyalar yine de bekleme önbelleğine yazılır ki sayfa kapandıysa kaybolmasın.
self.addEventListener('backgroundfetchsuccess', (event) => {
  const reg = event.registration;
  event.waitUntil((async () => {
    if (!reg.id.startsWith('cd|')) return;
    const [, key, vidler] = reg.id.split('|');
    const bekleyen = await caches.open(CD_BEKLEYEN_CACHE);
    for (const r of await reg.matchAll()) {
      const res = await r.responseReady.catch(() => null);
      if (res && res.ok) await bekleyen.put(r.request.url, res);
    }
    const acik = (await self.clients.matchAll({ type: 'window' })).length > 0;
    if (!acik) {
      await bekleyen.put(`/__cd-bekleyen/${encodeURIComponent(key)}`, new Response(JSON.stringify({ key, vidler: vidler ? vidler.split(',') : null }), { headers: { 'Content-Type': 'application/json' } }));
    }
    try { await event.updateUI({ title: acik ? 'Canlı ders indirildi' : 'Canlı ders indirildi — açınca cihaza kaydedilecek' }); } catch (_) {}
  })());
});
self.addEventListener('backgroundfetchfail', (event) => {
  event.waitUntil((async () => { try { await event.updateUI({ title: 'Canlı ders indirilemedi' }); } catch (_) {} })());
});
self.addEventListener('backgroundfetchclick', (event) => {
  event.waitUntil(self.clients.openWindow ? self.clients.openWindow('/canli-ders') : Promise.resolve());
});

// 6. İstemciden Gelen Mesajlar (postMessage)
self.addEventListener('message', (event) => {
  const data = event.data;
  if (!data) return;

  if (data.type === 'CD_OFFLINE_CHANGED') {
    event.waitUntil(cdSesleriYukle());
  } else if (data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  } else if (data.type === 'CACHE_URLS' && Array.isArray(data.urls)) {
    event.waitUntil(
      caches.open(DATA_CACHE).then((cache) => {
        return Promise.all(
          data.urls.map((u) =>
            fetch(u)
              .then((res) => {
                if (res.ok) return cache.put(u, res);
              })
              .catch((e) => console.warn('[SW] Toplu url önbellekleme uyarısı:', u, e))
          )
        );
      })
    );
  }
});

// 7. Sunucudan Web Push bildirimi geldiğinde
self.addEventListener('push', (event) => {
  if (!event.data) return;

  try {
    const payload = event.data.json();
    const title = payload.title || (payload.student ? 'MeDSor' : '🚨 MeDSor Bildirimi');
    const body = payload.body || 'Yeni bir işlem gerçekleşti.';
    const icon = payload.icon || '/icons/icon-192x192.png';
    const badge = payload.badge || '/icons/icon-96x96.png';
    const tag = payload.tag || `medsoru-${Date.now()}`;
    const data = payload.data || {};

    const options = {
      body,
      icon,
      badge,
      tag,
      renotify: true,
      // Öğrenci bildirimi sessizce düşer; yönetici bildirimi kalıcıdır
      requireInteraction: !payload.student,
      vibrate: payload.student ? [120, 60, 120] : [300, 100, 300, 100, 300],
      data,
      actions: [
        { action: 'open', title: payload.student ? 'Aç' : '🔍 Görüntüle' },
        { action: 'close', title: 'Kapat' },
      ],
    };

    event.waitUntil(self.registration.showNotification(title, options));
  } catch (err) {
    console.error('[SW] Push ayrıştırma hatası:', err);
    event.waitUntil(
      self.registration.showNotification('🚨 MeDSor Bildirimi', {
        body: event.data.text() || 'Yeni bir güncelleme alındı.',
        icon: '/icons/icon-192x192.png',
        vibrate: [200, 100, 200],
      })
    );
  }
});

// 8. Bildirime tıklandığında ilgili sayfayı aç
// Hedef her zaman bu kökenin yoluna çevrilir (bildirim nofrostlife.com.tr adresini taşısa da abone olunan
// uygulamada açılsın). Açık bir pencere varsa içine MEDSORU_NAVIGATE mesajı gider: uygulama sayfayı
// yenilemeden rotayı kurar ve hedef öğeye odaklanır. Pencere mesajı almazsa navigate(), o da olmazsa yeni pencere.
const APP_HOST_RE = /(^|\.)nofrostlife\.com\.tr$/i;

function notificationTargetPath(data) {
  let raw = data.url || data.link || '';
  if (!raw && data.questionId) raw = `/cikmis/${encodeURIComponent(data.questionId)}`;
  if (!raw) return { path: '/', external: false };
  try {
    const u = new URL(raw, self.location.origin);
    if (u.origin === self.location.origin || APP_HOST_RE.test(u.hostname)) {
      return { path: u.pathname + u.search + u.hash, external: false };
    }
    return { path: u.href, external: true };
  } catch (_) {
    return { path: '/', external: false };
  }
}

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  if (event.action === 'close') return;

  const target = notificationTargetPath(event.notification.data || {});
  const path = target.path;
  const absolute = new URL(path, self.location.origin).href;

  event.waitUntil((async () => {
    if (target.external) {
      if (self.clients.openWindow) await self.clients.openWindow(absolute);
      return;
    }
    const list = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    const same = list.filter((c) => c.url && new URL(c.url).origin === self.location.origin);
    // Odaktaki / görünür pencere önce
    same.sort((a, b) => Number(b.focused) - Number(a.focused) || Number(b.visibilityState === 'visible') - Number(a.visibilityState === 'visible'));
    const client = same[0];
    if (client) {
      try { await client.focus(); } catch (_) { /* odak izni yoksa da gezinme denensin */ }
      // Uygulama mesajı alınca yanıt verir; eski bir sürüm (dinleyicisiz) açıksa 1,5 sn sonra tam gezinme yapılır.
      const handled = await new Promise((resolve) => {
        try {
          const ch = new MessageChannel();
          const timer = setTimeout(() => resolve(false), 1500);
          ch.port1.onmessage = () => { clearTimeout(timer); resolve(true); };
          client.postMessage({ type: 'MEDSORU_NAVIGATE', url: path }, [ch.port2]);
        } catch (_) {
          resolve(false);
        }
      });
      if (handled) return;
      try {
        if (client.navigate) {
          await client.navigate(absolute);
          return;
        }
      } catch (_) { /* denetlenmeyen pencere: yeni pencere aç */ }
    }
    if (self.clients.openWindow) await self.clients.openWindow(absolute);
  })());
});

// Oturum değişince istemci kişisel önbelleği boşaltır (auth.ts purgePersonalCaches).
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'PURGE_DATA_CACHE') {
    event.waitUntil(caches.delete(DATA_CACHE));
  }
});
