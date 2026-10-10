// MedSoru Service Worker - PWA, Güçlendirilmiş Çevrimdışı Önbellek, Background Sync ve Push
const CACHE_VERSION = 'medsoru-pwa-v3';
const STATIC_CACHE = `medsoru-static-${CACHE_VERSION}`;
const RUNTIME_CACHE = `medsoru-runtime-${CACHE_VERSION}`;
const DATA_CACHE = `medsoru-data-${CACHE_VERSION}`;

const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/favicon.ico',
  '/apple-touch-icon.png',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  '/icons/maskable-icon-192x192.png',
  '/icons/maskable-icon-512x512.png',
];

// 1. Kurulum (Install) - Statik çekirdek dosyaları önbelleğe al
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(STATIC_CACHE)
      .then((cache) => {
        // Her dosyayı bağımsız fetch ile ekle (biri 404 olsa bile diğerleri çöpe gitmez)
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

// 2. Aktivasyon (Activate) - Eski önbellekleri temizle ve istemcileri devral
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => {
        return Promise.all(
          keys.map((key) => {
            if (key !== STATIC_CACHE && key !== RUNTIME_CACHE && key !== DATA_CACHE) {
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
  // Çevrimdışı olunduğunda ASLA düz metin veya hata dönme! Her zaman önbellekteki index.html'i sun!
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
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
        .catch(async () => {
          // 1. Önce tam eşleşen URL veya /index.html'i ara
          const matchDirect = await caches.match(req, { ignoreSearch: true });
          if (matchDirect) return matchDirect;

          const matchHtml =
            (await caches.match('/index.html', { ignoreSearch: true })) ||
            (await caches.match('/', { ignoreSearch: true }));
          if (matchHtml) return matchHtml;

          // 2. Tüm açık önbelleklerde index.html ara
          const allKeys = await caches.keys();
          for (const k of allKeys) {
            const c = await caches.open(k);
            const found =
              (await c.match('/index.html', { ignoreSearch: true })) ||
              (await c.match('/', { ignoreSearch: true }));
            if (found) return found;
          }

          // 3. Son çare: Temel SPA HTML iskeleti dönerek sayfanın takılmasını önle
          return new Response(
            `<!doctype html>
            <html lang="tr">
              <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
        })
    );
    return;
  }

  // B. Statik Varlıklar (JS, CSS, Fontlar, İkonlar, Resimler)
  // Stale-While-Revalidate / Cache-First stratejisi
  if (
    url.pathname.startsWith('/assets/') ||
    url.pathname.startsWith('/icons/') ||
    url.pathname.startsWith('/fonts/') ||
    /\.(js|css|woff2?|ttf|png|jpe?g|gif|svg|ico)$/i.test(url.pathname)
  ) {
    event.respondWith(
      caches.match(req).then((cachedRes) => {
        const fetchPromise = fetch(req)
          .then((networkRes) => {
            if (networkRes && networkRes.status === 200) {
              const clone = networkRes.clone();
              caches.open(RUNTIME_CACHE).then((cache) => cache.put(req, clone));
            }
            return networkRes;
          })
          .catch(() => cachedRes);

        return cachedRes || fetchPromise;
      })
    );
    return;
  }

  // C. API İstekleri (/api/...)
  // Network-First, hata durumunda veri önbelleğine düş
  if (url.pathname.startsWith('/api/')) {
    if (
      url.pathname.includes('/sse') ||
      url.pathname.includes('/heartbeat') ||
      url.pathname.includes('/ai/') ||
      url.pathname.includes('/backup')
    ) {
      return;
    }

    event.respondWith(
      fetch(req)
        .then((networkRes) => {
          if (networkRes && networkRes.status === 200) {
            const clone = networkRes.clone();
            caches.open(DATA_CACHE).then((cache) => cache.put(req, clone));
          }
          return networkRes;
        })
        .catch(async () => {
          const cached = await caches.match(req);
          if (cached) {
            return cached;
          }
          return new Response(
            JSON.stringify({ offline: true, error: 'Ağ bağlantısı yok (Çevrimdışı)' }),
            {
              headers: { 'Content-Type': 'application/json' },
              status: 200, // 503 yerine 200 ile offline JSON dönüyoruz ki istemci çökmesin
            }
          );
        })
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
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'close') {
    return;
  }

  const notificationData = event.notification.data || {};
  let targetUrl = '/cikmis';
  if (notificationData.url) {
    targetUrl = notificationData.url;
  } else if (notificationData.questionId) {
    targetUrl = `/cikmis/${encodeURIComponent(notificationData.questionId)}`;
  }

  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if ('focus' in client) {
          if (client.url && client.url.includes(self.location.origin)) {
            client.navigate(targetUrl);
            return client.focus();
          }
        }
      }
      if (self.clients.openWindow) {
        return self.clients.openWindow(targetUrl);
      }
    })
  );
});
