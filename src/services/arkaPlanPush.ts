/**
 * Öğrenci Web Push aboneliği (site kapalıyken bildirim).
 *  - Tercih `medsoru_push_acik_v1` ('1' açık). Açıkken hesap değişince ve açılışta abonelik sunucuya yeniden yazılır
 *    (cihaz başka hesaba geçerse sunucu eski hesaptan düşürür).
 *  - Kimlik profil yedeğiyle aynı (`backupIdentity`: Firebase jetonu ya da cihaz jetonu).
 *  - Gösterim sw.js `push` olayında; tıklama hedef yola gider (notificationclick).
 */
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from './auth';
import { safeJsonFetch } from './api';
import { backupIdentity } from './userDataSyncService';

const PREF = 'medsoru_push_acik_v1';

export type PushDurum = 'desteklenmiyor' | 'engelli' | 'kapali' | 'acik';

export const pushDestek = () =>
  typeof window !== 'undefined' && 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window;

const tercih = () => { try { return localStorage.getItem(PREF) === '1'; } catch { return false; } };
const tercihYaz = (v: boolean) => { try { v ? localStorage.setItem(PREF, '1') : localStorage.removeItem(PREF); } catch { /* yok */ } };

function b64ToU8(b64: string) {
  const pad = '='.repeat((4 - (b64.length % 4)) % 4);
  const raw = atob((b64 + pad).replace(/-/g, '+').replace(/_/g, '/'));
  return Uint8Array.from(raw, (c) => c.charCodeAt(0));
}

export async function pushDurum(): Promise<PushDurum> {
  if (!pushDestek()) return 'desteklenmiyor';
  if (Notification.permission === 'denied') return 'engelli';
  if (!tercih() || Notification.permission !== 'granted') return 'kapali';
  const reg = await navigator.serviceWorker.getRegistration();
  return (await reg?.pushManager.getSubscription()) ? 'acik' : 'kapali';
}

async function sunucuyaYaz(sub: PushSubscription) {
  const id = await backupIdentity();
  const r = await safeJsonFetch('/api/push/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...id.headers },
    body: JSON.stringify({ subscription: sub.toJSON(), deviceId: id.uid }),
  });
  if (!r.ok) throw new Error(r.error || 'Abonelik kaydedilemedi.');
}

/** İzin ister, abone olur, sunucuya yazar. */
export async function pushAc(): Promise<PushDurum> {
  if (!pushDestek()) return 'desteklenmiyor';
  const izin = await Notification.requestPermission();
  if (izin !== 'granted') return izin === 'denied' ? 'engelli' : 'kapali';
  const reg = await navigator.serviceWorker.ready;
  let sub = await reg.pushManager.getSubscription();
  if (!sub) {
    const k = await safeJsonFetch<{ publicKey: string }>('/api/push/vapid-public-key');
    const publicKey = k.data?.publicKey;
    if (!k.ok || !publicKey) throw new Error(k.error || 'Bildirim anahtarı alınamadı.');
    sub = await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64ToU8(publicKey) });
  }
  await sunucuyaYaz(sub);
  tercihYaz(true);
  return 'acik';
}

export async function pushKapat(): Promise<PushDurum> {
  tercihYaz(false);
  if (!pushDestek()) return 'desteklenmiyor';
  const reg = await navigator.serviceWorker.getRegistration();
  const sub = await reg?.pushManager.getSubscription();
  if (sub) {
    await safeJsonFetch('/api/push/unsubscribe', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ endpoint: sub.endpoint }),
    }).catch(() => null);
    await sub.unsubscribe().catch(() => false);
  }
  return 'kapali';
}

let kuruldu = false;
/** Açılışta bir kez: tercih açıksa aboneliği tazeler; oturum değişince yeniden bağlar. */
export function arkaPlanPushKur() {
  if (kuruldu || !pushDestek()) return;
  kuruldu = true;
  let son = '';
  onAuthStateChanged(auth, (u) => {
    const k = u?.uid || 'cihaz';
    if (k === son) return;
    son = k;
    if (!tercih() || Notification.permission !== 'granted') return;
    void (async () => {
      const reg = await navigator.serviceWorker.ready;
      const sub = await reg.pushManager.getSubscription();
      if (sub) await sunucuyaYaz(sub); else await pushAc();
    })().catch(() => {});
  });
}
