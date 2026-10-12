/**
 * Canlı veri eşitleme: sunucunun SSE akışına (/api/realtime/events) her ziyaretçiyi bağlar.
 * Oracle yerel Supabase'teki değişiklik → sunucu hub'ı → SSE → bu modül → ilgili önbellek tazelenir.
 * Eskiden akışa yalnız yönetim ekranı abone olmaya niyetliydi (connect hiç çağrılmıyordu); istemci
 * 5–30 dk'lık önbellek süreleri dolana kadar değişiklikleri görmüyordu.
 */
import { realtimeEventService } from './realtimeEvents';
import { pastQuestionsCache } from './pastQuestionsCache';
import { clientCache } from './clientCache';
import { startContentLive } from './contentLive';

let started = false;
let pastTimer: ReturnType<typeof setTimeout> | null = null;

function schedulePastSync(delay = 800) {
  if (pastTimer) clearTimeout(pastTimer);
  pastTimer = setTimeout(() => {
    pastTimer = null;
    pastQuestionsCache.syncWithRemote().catch(() => {});
  }, delay);
}

/** SW veri önbelleğindeki eşleşen API yanıtlarını düşür (ağ hatasında eski kopya sunulmasın) */
async function purgeSwCache(pathPrefix: string) {
  if (typeof caches === 'undefined') return;
  try {
    for (const name of await caches.keys()) {
      const cache = await caches.open(name);
      for (const req of await cache.keys()) {
        if (new URL(req.url).pathname.startsWith(pathPrefix)) await cache.delete(req);
      }
    }
  } catch (_) {}
}

export function startLiveDataSync() {
  if (started || typeof window === 'undefined') return;
  started = true;
  realtimeEventService.connect();
  startContentLive();

  window.addEventListener('medsoru:past-questions-changed', () => schedulePastSync());

  window.addEventListener('medsoru:database-sync', (e: Event) => {
    const table = (e as CustomEvent).detail?.table;
    if (table === 'committees') {
      void clientCache.invalidate('committees').then(() => purgeSwCache('/api/committees')).then(() => {
        window.dispatchEvent(new CustomEvent('medsoru:committees-changed'));
      });
    } else if (table === 'lecture_notes') {
      void purgeSwCache('/api/lecture-notes').then(() => {
        window.dispatchEvent(new CustomEvent('medsoru:lecture-notes-changed'));
      });
    }
  });

  // Bağlantı koptuğu sırada kaçan değişiklikleri yakala
  realtimeEventService.onStatusChange((s) => {
    if (s === 'connected') schedulePastSync(2000);
  });
}
