// Gerçek kullanıcı başarım ölçümü (web-vitals eşdeğeri, bağımlılıksız): LCP, CLS, INP, TTFB, uzun görev sayısı.
// Oturumların %25'inde, boşta (idle) kurulur; sayfa gizlenince TEK kayıt navigator.sendBeacon ile /api/olcum/vitals'a gider.
// Kişisel veri yok: rota siteHaritasi iç adresine çevrilir, sorgu dizgisi ve kimlik benzeri parçalar atılır.
import { icYol } from '../siteHaritasi';

declare const __MEDS_SURUM__: string;

const UC = '/api/olcum/vitals';
const ORNEK_ORANI = 0.25;
const ORNEK_ANAHTARI = 'medsoru_vitals_ornek';

export type VitalsKaydi = {
  rota: string;
  lcp: number | null;   // ms
  cls: number;          // birimsiz, oturum penceresi en büyüğü
  inp: number | null;   // ms, en yavaş etkileşimlerin üst yüzdeliği (yaklaşık p98)
  ttfb: number | null;  // ms
  uzunGorev: number;    // ≥50 ms görev sayısı
  surum: string;
  cihaz: 'telefon' | 'tablet' | 'masaustu';
};

/** Oturum başına bir kez zar atılır; aynı sekmede yenilemeler aynı kararı paylaşır. */
function orneklendi(): boolean {
  try {
    const v = sessionStorage.getItem(ORNEK_ANAHTARI);
    if (v === '1' || v === '0') return v === '1';
    const secildi = Math.random() < ORNEK_ORANI;
    sessionStorage.setItem(ORNEK_ANAHTARI, secildi ? '1' : '0');
    return secildi;
  } catch {
    return Math.random() < ORNEK_ORANI;
  }
}

/** Görünen adres → iç rota; kimlik/sayı parçaları ':id' olur, sorgu ve hash atılır. */
function rotaNormalize(): string {
  let yol = location.pathname;
  try { yol = icYol(location.pathname).split(/[?#]/)[0] || yol; } catch { /* sade yol kalır */ }
  const parca = yol.split('/').filter(Boolean).slice(0, 4)
    .map((s) => (/\d{2,}|^[0-9a-f-]{16,}$|^[A-Za-z0-9_-]{20,}$/i.test(s) ? ':id' : s.slice(0, 40)));
  return '/' + parca.join('/');
}

function cihazSinifi(): VitalsKaydi['cihaz'] {
  const w = window.innerWidth || 0;
  return w < 768 ? 'telefon' : w < 1200 ? 'tablet' : 'masaustu';
}

function gozle(tur: string, cb: (girdiler: PerformanceEntryList) => void, ek: Record<string, unknown> = {}): void {
  try {
    if (!PerformanceObserver.supportedEntryTypes?.includes(tur)) return;
    new PerformanceObserver((l) => cb(l.getEntries())).observe({ type: tur, buffered: true, ...ek } as PerformanceObserverInit);
  } catch { /* tarayıcı desteklemiyor: o ölçü boş kalır */ }
}

function kur(): void {
  let lcp: number | null = null;
  let cls = 0, oturumCls = 0, oturumBas = 0, oturumSon = 0;
  let uzunGorev = 0;
  const etkilesim = new Map<number, number>(); // interactionId → en uzun süre

  gozle('largest-contentful-paint', (g) => { const s = g[g.length - 1]; if (s) lcp = Math.round(s.startTime); });
  gozle('layout-shift', (g) => {
    for (const e of g as Array<PerformanceEntry & { value: number; hadRecentInput: boolean }>) {
      if (e.hadRecentInput) continue;
      // web-vitals oturum penceresi: 1 sn boşluk ya da 5 sn toplam yeni pencere açar
      if (oturumCls && e.startTime - oturumSon < 1000 && e.startTime - oturumBas < 5000) oturumCls += e.value;
      else { oturumCls = e.value; oturumBas = e.startTime; }
      oturumSon = e.startTime;
      if (oturumCls > cls) cls = oturumCls;
    }
  });
  gozle('longtask', (g) => { uzunGorev += g.length; });
  gozle('event', (g) => {
    for (const e of g as Array<PerformanceEntry & { interactionId?: number }>) {
      const id = e.interactionId;
      if (!id) continue;
      if ((etkilesim.get(id) || 0) < e.duration) etkilesim.set(id, e.duration);
      if (etkilesim.size > 400) etkilesim.delete(etkilesim.keys().next().value as number);
    }
  }, { durationThreshold: 40 });

  let gonderildi = false;
  const gonder = () => {
    if (gonderildi || document.visibilityState !== 'hidden') return;
    if (!navigator.onLine || typeof navigator.sendBeacon !== 'function') return;
    gonderildi = true;
    const sureler = [...etkilesim.values()].sort((a, b) => b - a);
    // INP ≈ her 50 etkileşimde bir en yavaşı atla (web-vitals yaklaşımı)
    const inp = sureler.length ? Math.round(sureler[Math.min(sureler.length - 1, Math.floor(sureler.length / 50))]) : null;
    const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming | undefined;
    const kayit: VitalsKaydi = {
      rota: rotaNormalize(),
      lcp,
      cls: Math.round(cls * 1000) / 1000,
      inp,
      ttfb: nav && nav.responseStart > 0 ? Math.round(nav.responseStart) : null,
      uzunGorev,
      surum: typeof __MEDS_SURUM__ === 'string' ? __MEDS_SURUM__ : '',
      cihaz: cihazSinifi(),
    };
    try { navigator.sendBeacon(UC, new Blob([JSON.stringify(kayit)], { type: 'application/json' })); } catch { /* ölçüm kaybı önemsiz */ }
  };
  document.addEventListener('visibilitychange', gonder);
  window.addEventListener('pagehide', gonder);
}

/** main.tsx'ten bir kez çağrılır; ana iş parçacığını yormamak için boşta kurulur. */
export function installWebVitals(): void {
  if (typeof window === 'undefined' || typeof PerformanceObserver === 'undefined') return;
  if (!orneklendi()) return;
  const w = window as Window & { requestIdleCallback?: (cb: () => void, o?: { timeout: number }) => number };
  if (w.requestIdleCallback) w.requestIdleCallback(kur, { timeout: 5000 });
  else window.setTimeout(kur, 1500);
}
