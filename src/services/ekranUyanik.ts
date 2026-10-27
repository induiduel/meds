/**
 * "Ekran kararmasın" (tasarım O10 Tam ekran ve kip): sesli ders çalarken Screen Wake Lock ister, duraklayınca bırakır.
 * Tercih cihazda (`medsoru_ekran_uyanik_v1`, varsayılan açık). Desteklemeyen tarayıcıda sessizce hiçbir şey yapmaz;
 * sekme gizlenince tarayıcı kilidi düşürür, görünür olunca çalma sürüyorsa yeniden istenir.
 */
export const EKRAN_UYANIK_KEY = 'medsoru_ekran_uyanik_v1';
export const ekranUyanikAcik = () => { try { return localStorage.getItem(EKRAN_UYANIK_KEY) !== '0'; } catch { return true; } };
export const ekranUyanikYaz = (v: boolean) => { try { localStorage.setItem(EKRAN_UYANIK_KEY, v ? '1' : '0'); } catch { /* yok */ } };

type Kilit = { release: () => Promise<void> };
let kilit: Kilit | null = null;
let istek = false;
async function al() {
  const wl = (navigator as unknown as { wakeLock?: { request: (t: 'screen') => Promise<Kilit> } }).wakeLock;
  if (!wl || kilit || !ekranUyanikAcik() || document.visibilityState !== 'visible') return;
  try { kilit = await wl.request('screen'); } catch { kilit = null; }
}
export function ekranUyanik(ac: boolean) {
  istek = ac;
  if (ac) void al();
  else if (kilit) { const k = kilit; kilit = null; void k.release().catch(() => {}); }
}
if (typeof document !== 'undefined') {
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') { kilit = null; if (istek) void al(); }
  });
}
