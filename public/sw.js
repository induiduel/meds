// MedSoru Service Worker - PWA v8: Yüksek Hızlı Açılış, Optimize Edilmiş Bellek & Modül Parçalama
const CACHE_VERSION = 'medsoru-pwa-v10';
const STATIC_CACHE = `medsoru-static-${CACHE_VERSION}`;
const RUNTIME_CACHE = `medsoru-runtime-${CACHE_VERSION}`;
const DATA_CACHE = `medsoru-data-${CACHE_VERSION}`;

const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.ico',
  '/favicon.png',
  '/apple-touch-icon.png',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  '/icons/maskable-icon-192x192.png',
  '/icons/maskable-icon-512x512.png',
  '/cikmis',
  '/ogren',
  '/kartlar',
  '/hastaliklar',
  '/sozluk',
  '/calis',
  '/ozetler',
  '/kazanimlar',
  '/test',
  '/istatistik',
  '/ayarlar',
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

// 1. Kurulum (Install) - Statik çekirdek dosyaları önbelleğe al
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(STATIC_CACHE)
      .then((cache) => {
        return Promise.all(
          PRECACHE_ASSETS.map((url) =>
            fetch(url, { cache: 'no-cache' })
              .then((res) => {
                if (res.ok) {
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
            if (key !== STATIC_CACHE && key !== RUNTIME_CACHE && key !== DATA_CACHE && key !== 'medsoru-pdf-offline') {
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
        const matchDirect = await caches.match(req, { ignoreSearch: true });
        if (matchDirect) return matchDirect;

        const matchHtml =
          (await caches.match('/index.html', { ignoreSearch: true })) ||
          (await caches.match('/', { ignoreSearch: true }));
        if (matchHtml) return matchHtml;

        const allKeys = await caches.keys();
        for (const k of allKeys) {
          const c = await caches.open(k);
          const found =
            (await c.match('/index.html', { ignoreSearch: true })) ||
            (await c.match('/', { ignoreSearch: true }));
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

  // B. Statik Varlıklar (JS, CSS, Fontlar, İkonlar, Resimler)
  // Stale-While-Revalidate / Cache-First stratejisi (ASLA undefined dönmez)
  if (
    url.pathname.startsWith('/assets/') ||
    url.pathname.startsWith('/icons/') ||
    url.pathname.startsWith('/fonts/') ||
    /\.(js|css|woff2?|ttf|png|jpe?g|gif|svg|ico)$/i.test(url.pathname)
  ) {
    event.respondWith(
      (async () => {
        // Önce tam eşleşen veya arama parametresi yok sayılan önbellek kaydına bak
        const cached =
          (await caches.match(req, { ignoreSearch: true })) ||
          (await caches.match(url.pathname, { ignoreSearch: true }));

        // Arka planda güncelleme (network)
        const fetchPromise = fetch(req)
          .then((networkRes) => {
            if (networkRes && networkRes.status === 200) {
              const clone = networkRes.clone();
              caches.open(RUNTIME_CACHE).then((cache) => {
                cache.put(req, clone.clone());
                cache.put(url.pathname, clone);
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
    if (
      url.pathname.includes('/sse') ||
      url.pathname.includes('/heartbeat') ||
      url.pathname.includes('/ai/') ||
      url.pathname.includes('/backup')
    ) {
      return;
    }

    // Büyük tam listeler IndexedDB'de tutulur; SW önbelleğine ikinci kopya yazılmaz
    const cacheable = !/\/api\/past-exams(\/?$|\/sync)/.test(url.pathname) && !url.pathname.includes('/admin/');

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
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync tetiklendi:', event.tag);
  if (event.tag === 'sync-offline-actions' || event.tag === 'medsoru-sync') {
    event.waitUntil(notifyClientsToSync());
  }
});

// 5. Periyodik Arka Plan Senkronizasyonu (Periodic Background Sync)
self.addEventListener('periodicsync', (event) => {
  console.log('[SW] Periodic background sync tetiklendi:', event.tag);
  if (event.tag === 'update-database' || event.tag === 'medsoru-daily-sync') {
    event.waitUntil(notifyClientsToSync());
  }
});

async function notifyClientsToSync() {
  const clientList = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
  for (const client of clientList) {
    client.postMessage({ type: 'MEDSORU_BACKGROUND_SYNC' });
  }
}

// 6. İstemciden Gelen Mesajlar (postMessage)
self.addEventListener('message', (event) => {
  const data = event.data;
  if (!data) return;

  if (data.type === 'SKIP_WAITING') {
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
    const title = payload.title || '🚨 MedSoru Bildirimi';
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
      requireInteraction: true,
      vibrate: [300, 100, 300, 100, 300],
      data,
      actions: [
        { action: 'open', title: '🔍 Görüntüle' },
        { action: 'close', title: 'Kapat' },
      ],
    };

    event.waitUntil(self.registration.showNotification(title, options));
  } catch (err) {
    console.error('[SW] Push ayrıştırma hatası:', err);
    event.waitUntil(
      self.registration.showNotification('🚨 MedSoru Bildirimi', {
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
