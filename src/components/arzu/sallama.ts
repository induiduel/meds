/**
 * Telefonu sallayınca tilki geçidi: devicemotion ivme farkı eşiği aşınca (8 sn soğuma) `arzu:tilki` olayı yayılır.
 * iOS 13+ izin ister; izin yalnız bir kullanıcı dokunuşu içinden istenebilir (KalpAskisi ilk dokunuşta çağırır).
 */
let kurulu = false;
let izinDenendi = false;

export async function hareketIzniIste(): Promise<void> {
  if (izinDenendi) return;
  izinDenendi = true;
  const DME = (window as any).DeviceMotionEvent;
  if (DME && typeof DME.requestPermission === 'function') {
    try {
      const r = await DME.requestPermission();
      if (r === 'granted') sallamaDinle();
    } catch { /* izin verilmedi */ }
  }
}

export function sallamaDinle(): () => void {
  if (kurulu || typeof window === 'undefined' || !('DeviceMotionEvent' in window)) return () => {};
  kurulu = true;
  let onceki: { x: number; y: number; z: number } | null = null;
  let sonTetik = 0;
  let sayac = 0;
  const onMotion = (e: DeviceMotionEvent) => {
    const a = e.accelerationIncludingGravity;
    if (!a || a.x == null || a.y == null || a.z == null) return;
    if (onceki) {
      const fark = Math.abs(a.x - onceki.x) + Math.abs(a.y - onceki.y) + Math.abs(a.z - onceki.z);
      if (fark > 28) sayac++;
      else sayac = Math.max(0, sayac - 1);
      if (sayac >= 3 && Date.now() - sonTetik > 8000) {
        sonTetik = Date.now();
        sayac = 0;
        window.dispatchEvent(new CustomEvent('arzu:tilki', { detail: { adet: 5 } }));
        window.dispatchEvent(new CustomEvent('arzu:fisilti', { detail: { metin: 'Salladın, geldiler.' } }));
      }
    }
    onceki = { x: a.x, y: a.y, z: a.z };
  };
  window.addEventListener('devicemotion', onMotion);
  return () => { window.removeEventListener('devicemotion', onMotion); kurulu = false; };
}
