// MedSoru Service Worker - Web Push ve Arka Plan Bildirim Yöneticisi
const CACHE_NAME = 'medsoru-sw-v1';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

// Sunucudan Web Push bildirimi geldiğinde
self.addEventListener('push', (event) => {
  if (!event.data) return;

  try {
    const payload = event.data.json();
    const title = payload.title || '🚨 MedSoru Admin Bildirimi';
    const body = payload.body || 'Yeni bir işlem gerçekleşti.';
    const icon = payload.icon || '/assets/favicon.ico';
    const badge = payload.badge || '/assets/favicon.ico';
    const tag = payload.tag || `medsoru-${Date.now()}`;
    const data = payload.data || {};

    const options = {
      body,
      icon,
      badge,
      tag,
      renotify: true,
      requireInteraction: true, // Kullanıcı tıklayana kadar ekranda tut
      vibrate: [300, 100, 300, 100, 300],
      data,
      actions: [
        { action: 'open', title: '🔍 Soruyu Aç' },
        { action: 'close', title: 'Kapat' }
      ]
    };

    event.waitUntil(self.registration.showNotification(title, options));
  } catch (err) {
    console.error('[SW] Push ayrıştırma hatası:', err);
    event.waitUntil(
      self.registration.showNotification('🚨 MedSoru Bildirimi', {
        body: event.data.text() || 'Yeni bir öğrenci bildirimi alındı.',
        icon: '/assets/favicon.ico',
        vibrate: [200, 100, 200]
      })
    );
  }
});

// Bildirime tıklandığında ilgili sayfayı/soruyu aç
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'close') {
    return;
  }

  const notificationData = event.notification.data || {};
  let targetUrl = 'https://nofrostlife.com.tr/cikmis';
  // Sunucu bağlantıyı hazırladıysa (ör. Öğren hata bildirimi → /ogren/<deste>?adim=&hedef=) doğrudan oraya git
  const hasDeepLink = notificationData.url && /\/(ogren|cikmis)\b/.test(notificationData.url);
  if (hasDeepLink) {
    targetUrl = notificationData.url;
  } else if (notificationData.questionId) {
    targetUrl = `https://nofrostlife.com.tr/cikmis/${encodeURIComponent(notificationData.questionId)}`;
  } else if (notificationData.url) {
    targetUrl = notificationData.url;
  }

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clientList) => {
      // Açık bir sekme varsa oraya odaklan ve URL'i yükle
      for (const client of clientList) {
        if ('focus' in client) {
          if (client.url && client.url.includes('nofrostlife.com.tr')) {
            client.navigate(targetUrl);
            return client.focus();
          }
        }
      }
      // Açık sekme yoksa yeni pencere aç
      if (clients.openWindow) {
        return clients.openWindow(targetUrl);
      }
    })
  );
});
