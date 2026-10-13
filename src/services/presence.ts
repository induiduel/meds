/**
 * Cihaz varlığı ve kullanım süresi (yönetim paneli › Kişiler).
 *
 * - Herkese açık cihaz kimliği: gizli cihaz jetonundan (medsoru_device_token) SHA-256 ile türetilir; jetonun kendisi
 *   asla gönderilmez. Sunucu aynı türetmeyle girişsiz profil yedeğini bu cihaza bağlar (peopleInsights.publicDeviceId).
 * - Yazma isteklerine `x-device-id` eklenir (net.ts): eylem günlüğü doğru cihaza/kişiye düşer. GET'lere eklenmez
 *   (çapraz köken ön-kontrolü her GET'e binmesin).
 * - sendBeacon başlık taşıyamaz ve çapraz kökende yalnız text/plain gönderebilir; sunucu bu ucu text/plain JSON olarak da okur.
 * - Kalp atışı: sekme görünür ve son 5 dakikada etkileşim varken her 60 sn'de bir etkin saniye gönderilir;
 *   sekme gizlenince kalan süre sendBeacon ile yollanır. Giriş yapılmışsa Firebase jetonu eklenir (cihaz hesaba bağlanır).
 */
import { auth } from './auth';
import { getCustomApiUrl } from './api';
import { getDeviceToken } from '../utils/voterId';

const PUB_KEY = 'medsoru_device_pub';
const BEAT_MS = 60_000;
const IDLE_MS = 5 * 60_000;

let pubId = '';
try {
  pubId = localStorage.getItem(PUB_KEY) || '';
} catch {
  /* gizli pencere */
}

export const getPublicDeviceId = () => pubId;

async function derivePublicId(): Promise<string> {
  if (pubId) return pubId;
  try {
    const data = new TextEncoder().encode(`pub:${getDeviceToken()}`);
    const buf = await crypto.subtle.digest('SHA-256', data);
    const hex = Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, '0')).join('');
    pubId = `p${hex.slice(0, 23)}`;
    try {
      localStorage.setItem(PUB_KEY, pubId);
    } catch {
      /* yoksay */
    }
  } catch {
    /* crypto.subtle yalnız güvenli kökende; yoksa varlık bildirilmez */
  }
  return pubId;
}

async function deviceHint() {
  const nav: any = navigator;
  const hint: Record<string, any> = {
    standalone: window.matchMedia?.('(display-mode: standalone)').matches || nav.standalone === true,
  };
  try {
    const uad = nav.userAgentData;
    if (uad?.getHighEntropyValues) {
      const v = await uad.getHighEntropyValues(['model', 'platform']);
      if (v.model) hint.model = String(v.model).slice(0, 60);
      if (v.platform) hint.platform = String(v.platform).slice(0, 40);
    }
  } catch {
    /* desteklenmiyor */
  }
  return hint;
}

let installed = false;

export function installPresence() {
  if (installed || typeof window === 'undefined') return;
  installed = true;
  let lastInput = Date.now();
  let visibleSince = document.hidden ? 0 : Date.now();
  let pending = 0; // gönderilmemiş etkin ms
  let hint: Record<string, any> = {};
  let started = false;

  const onInput = () => {
    lastInput = Date.now();
  };
  for (const ev of ['pointerdown', 'keydown', 'wheel', 'touchstart', 'scroll']) window.addEventListener(ev, onInput, { passive: true, capture: true });

  const accrue = () => {
    const now = Date.now();
    if (visibleSince && now - lastInput < IDLE_MS) pending += now - visibleSince;
    visibleSince = document.hidden ? 0 : now;
  };

  const payload = (activeSec: number) => ({
    deviceId: pubId,
    activeSec,
    path: location.pathname.slice(0, 200),
    device: hint,
    start: !started,
    displayName: auth.currentUser?.displayName || undefined,
  });

  const send = async (beacon = false) => {
    if (!pubId) return;
    accrue();
    const activeSec = Math.min(120, Math.round(pending / 1000));
    const body = payload(activeSec);
    const url = `${(getCustomApiUrl() || '').replace(/\/$/, '')}/api/presence`;
    try {
      if (beacon && navigator.sendBeacon) {
        if (navigator.sendBeacon(url, new Blob([JSON.stringify(body)], { type: 'text/plain' }))) pending = Math.max(0, pending - activeSec * 1000);
        return;
      }
      const headers: Record<string, string> = { 'Content-Type': 'application/json', 'x-device-id': pubId };
      const user = auth.currentUser;
      if (user) {
        try {
          headers.Authorization = `Bearer ${await user.getIdToken()}`;
        } catch {
          /* jetonsuz gönder */
        }
      }
      const res = await fetch(url, { method: 'POST', headers, body: JSON.stringify(body), keepalive: true });
      if (res.ok) {
        pending = Math.max(0, pending - activeSec * 1000);
        started = true;
      }
    } catch {
      /* çevrimdışı: süre birikir, sonraki atışta gider */
    }
  };

  void (async () => {
    await derivePublicId();
    hint = await deviceHint();
    await send();
  })();

  window.setInterval(() => {
    if (!document.hidden) void send();
  }, BEAT_MS);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      accrue();
      void send(true);
    } else {
      visibleSince = Date.now();
      lastInput = Date.now();
    }
  });
  window.addEventListener('pagehide', () => void send(true));
  // Giriş/çıkış: cihazın hesabı hemen güncellensin
  auth.onAuthStateChanged?.(() => void send());
}
