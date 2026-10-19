/**
 * Etkinlik günlüğü: öğrencinin girdiği her sayfa, sayfada etkin geçirdiği süre ve kaldığı yer (kaydırma konumu).
 *
 * - `medsoru_etkinlik_v1`: ziyaret listesi (en yeni sonda; en çok 600 kayıt, 90 gün).
 * - `medsoru_son_konum_v1`: sayfa (yol + sorgu) başına son ziyaret, toplam süre, ziyaret sayısı, kaydırma oranı;
 *   `son` alanı en son açık sayfadır (kaldığı yerden devam için).
 *
 * İkisi de userKvSync profil anahtarıdır (QUIET_PROFILE): her yazımda damgalanır, dönemsel gönderimle, sekme arka
 * plana geçerken ve sayfa kapanırken sunucuya (meds-pg user_data) gider; diğer cihazlar SSE ile çeker.
 * Ekranların kendi adım/ilerleme anahtarları (Öğren, çözücü, sesli ders konumu…) ayrıca eşitlenir.
 */

const GUNLUK_KEY = 'medsoru_etkinlik_v1';
const KONUM_KEY = 'medsoru_son_konum_v1';
const MAX_ZIYARET = 600;
const MAX_KONUM = 400;
const SAKLA_MS = 90 * 86_400_000;
const BOS_MS = 60_000; // son etkileşimden bu kadar sonra süre saymayı bırak
const TIK_MS = 5_000;

export type Ziyaret = { p: string; t: string; g: number; c: number; s: number; k: number };
export type SonKonum = { at: number; t: string; s: number; n: number; k: number; y: number };
type KonumDeposu = { son?: string; sayfalar: Record<string, SonKonum> };

const oku = <T,>(key: string, bos: T): T => {
  try {
    const v = JSON.parse(localStorage.getItem(key) || 'null');
    return v && typeof v === 'object' ? v : bos;
  } catch {
    return bos;
  }
};
const yaz = (key: string, v: unknown) => {
  try {
    localStorage.setItem(key, JSON.stringify(v));
  } catch {
    /* kota / gizli pencere */
  }
};

const yolAl = () => (location.pathname + location.search).slice(0, 240);

export function sonKonumlar(): KonumDeposu {
  const d = oku<KonumDeposu>(KONUM_KEY, { sayfalar: {} });
  return { son: d.son, sayfalar: d.sayfalar && typeof d.sayfalar === 'object' ? d.sayfalar : {} };
}
export const sonKonum = (yol: string): SonKonum | undefined => sonKonumlar().sayfalar[yol];
export const ziyaretler = (): Ziyaret[] => {
  const v = oku<Ziyaret[]>(GUNLUK_KEY, []);
  return Array.isArray(v) ? v : [];
};

let kuruldu = false;

export function installEtkinlikGunlugu(): void {
  if (kuruldu || typeof window === 'undefined') return;
  kuruldu = true;

  let yol = yolAl();
  let giris = Date.now();
  let etkinMs = 0;
  let sonGirdi = Date.now();
  let sonTik = Date.now();
  let kaydirma = { k: 0, y: 0 };
  let kaydedilen = { etkinMs: -1, k: -1 };

  const tik = () => {
    const simdi = Date.now();
    if (!document.hidden && simdi - sonGirdi < BOS_MS) etkinMs += Math.min(simdi - sonTik, TIK_MS * 3);
    sonTik = simdi;
  };

  /** Bu ziyareti günlüğe ve son konuma yazar (aynı ziyaret güncellenir, yeni kayıt açılmaz). */
  const kaydet = () => {
    tik();
    const s = Math.round(etkinMs / 1000);
    if (s === kaydedilen.etkinMs && kaydirma.k === kaydedilen.k) return;
    const onceki = kaydedilen.etkinMs < 0 ? 0 : kaydedilen.etkinMs;
    kaydedilen = { etkinMs: s, k: kaydirma.k };
    const t = (document.title || '').slice(0, 120);
    const simdi = Date.now();

    const liste = ziyaretler().filter((z) => simdi - z.g < SAKLA_MS);
    const son = liste[liste.length - 1];
    const kayit: Ziyaret = { p: yol, t, g: giris, c: simdi, s, k: kaydirma.k };
    if (son && son.p === yol && son.g === giris) liste[liste.length - 1] = kayit;
    else liste.push(kayit);
    yaz(GUNLUK_KEY, liste.slice(-MAX_ZIYARET));

    const depo = sonKonumlar();
    const eski = depo.sayfalar[yol];
    const yeniZiyaret = !eski || eski.at < giris;
    depo.sayfalar[yol] = {
      at: simdi,
      t,
      s: (eski?.s || 0) + Math.max(0, s - (yeniZiyaret ? 0 : onceki)),
      n: (eski?.n || 0) + (yeniZiyaret ? 1 : 0),
      k: kaydirma.k,
      y: kaydirma.y,
    };
    const anahtarlar = Object.keys(depo.sayfalar);
    if (anahtarlar.length > MAX_KONUM) {
      anahtarlar
        .sort((a, b) => depo.sayfalar[a].at - depo.sayfalar[b].at)
        .slice(0, anahtarlar.length - MAX_KONUM)
        .forEach((a) => delete depo.sayfalar[a]);
    }
    depo.son = yol;
    yaz(KONUM_KEY, depo);
  };

  const sayfaDegisti = () => {
    const yeni = yolAl();
    if (yeni === yol) return;
    kaydet();
    yol = yeni;
    giris = Date.now();
    etkinMs = 0;
    sonTik = giris;
    kaydirma = { k: 0, y: 0 };
    kaydedilen = { etkinMs: -1, k: -1 };
    // Başlık yeni ekranda birkaç yüz ms sonra kurulur; ziyareti o zaman aç
    window.setTimeout(kaydet, 800);
  };

  for (const ad of ['pushState', 'replaceState'] as const) {
    const asil = history[ad].bind(history);
    history[ad] = ((...a: Parameters<History['pushState']>) => {
      const r = asil(...a);
      try {
        sayfaDegisti();
      } catch {
        /* günlük asla gezinmeyi bozmaz */
      }
      return r;
    }) as History['pushState'];
  }
  window.addEventListener('popstate', sayfaDegisti);
  window.addEventListener('hashchange', sayfaDegisti);

  const girdi = () => {
    tik();
    sonGirdi = Date.now();
  };
  for (const ev of ['pointerdown', 'keydown', 'wheel', 'touchstart']) window.addEventListener(ev, girdi, { passive: true, capture: true });

  // Kaydırma: sayfa ya da iç kaydırma kabı (v12 kabuğu) — en son kaydırılan büyük kabın oranı
  let kaydirmaZamani = 0;
  window.addEventListener(
    'scroll',
    (e) => {
      girdi();
      const simdi = Date.now();
      if (simdi - kaydirmaZamani < 250) return;
      kaydirmaZamani = simdi;
      const hedef = e.target instanceof Element ? e.target : document.scrollingElement;
      if (!hedef) return;
      const el = hedef as Element;
      const aralik = el.scrollHeight - el.clientHeight;
      if (aralik < 40 || el.clientHeight < window.innerHeight * 0.4) return;
      kaydirma = { k: Math.round((el.scrollTop / aralik) * 1000) / 1000, y: Math.round(el.scrollTop) };
    },
    { passive: true, capture: true },
  );

  window.setInterval(() => {
    tik();
    if (!document.hidden) kaydet();
  }, TIK_MS * 6);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) kaydet();
    else sonTik = sonGirdi = Date.now();
  });
  window.addEventListener('pagehide', kaydet);
  window.setTimeout(kaydet, 1500);
}
