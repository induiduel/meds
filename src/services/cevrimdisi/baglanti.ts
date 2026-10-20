/**
 * Gerçek bağlantı denetimi. `navigator.onLine` yalnız ağ arayüzünü söyler: Wi-Fi'ye bağlı ama internetsiz (ya da sunucuya
 * ulaşılamayan) cihazda da true döner. Parça yüklenemediğinde "yeni sürüm geldi, yenile" kararı yalnız sunucu gerçekten
 * yanıt veriyorsa verilir; yoksa internetsiz ekranı gösterilir (yenileme döngüsü ve önbellek silme yok).
 * /api/surum SW'den geçmez (sw.js), yanıt her zaman ağdandır.
 */
import { getNetState } from '../net';

let son: { at: number; ok: boolean } | null = null;
let suren: Promise<boolean> | null = null;

export function sunucuyaUlasilir(ms = 3500): Promise<boolean> {
  if (typeof navigator !== 'undefined' && !navigator.onLine) return Promise.resolve(false);
  if (son && Date.now() - son.at < 10_000) return Promise.resolve(son.ok);
  if (suren) return suren;
  const ctl = typeof AbortController !== 'undefined' ? new AbortController() : null;
  const t = setTimeout(() => ctl?.abort(), ms);
  suren = fetch(`/api/surum?t=${Date.now()}`, { cache: 'no-store', signal: ctl?.signal })
    .then((r) => r.ok)
    .catch(() => false)
    .then((ok) => { clearTimeout(t); son = { at: Date.now(), ok }; suren = null; return ok; });
  return suren;
}

/** Arayüz kapalıysa, son denetim sunucuya ulaşılamadığını söylediyse ya da SW internetsiz yanıt verdiyse (net.ts) true */
export const cevrimdisiGibi = () =>
  (typeof navigator !== 'undefined' && !navigator.onLine) || (!!son && !son.ok && Date.now() - son.at < 60_000) || getNetState() === 'offline';
