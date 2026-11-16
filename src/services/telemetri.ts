/**
 * Sunucu telemetrisi (2026-11-16): /api/* istek süreleri, yavaş istek kaydı, bellek örnekleyici, web-vitals doğrulayıcısı.
 *
 * - İstek başına O(1): bitişte (res 'finish') rota anahtarı + kova sayacı artırılır; gövde ayrıştırma yok.
 * - Rota anahtarı: `req.baseUrl + req.route.path` (Express eşleştiyse), yoksa yolun kimlik/sayı parçaları `:id`.
 *   En çok ROTA_TAVAN anahtar; dolunca yeni rotalar `(diger)` altında toplanır.
 * - ≥ YAVAS_MS istekler `veriOlayi('uyari','yavas-istek',…)` (dakikada en çok YAVAS_DAKIKA_TAVAN kayıt).
 * - SSE/akış yanıtları (text/event-stream) sayılmaz.
 * - 5 dakikada bir bellek örneği `veriOlayi('bilgi','bellek',…)`; olay döngüsü gecikmesi perf_hooks ile.
 * Kişisel veri (IP, kullanıcı kimliği, sorgu dizesi) tutulmaz/yazılmaz.
 */
import type express from 'express';
import { monitorEventLoopDelay } from 'perf_hooks';
import { veriOlayi, gunlugeEkle } from './veriGunlugu.ts';

export const KOVALAR = [10, 25, 50, 100, 250, 500, 1000, 2500] as const; // son kova: > 2500
const ROTA_TAVAN = 300;
const YAVAS_MS = 1000;
const YAVAS_DAKIKA_TAVAN = 30;
const BELLEK_ORNEK_TAVAN = 48; // 4 saatlik geçmiş (5 dk aralık)

type RotaIstatistik = { sayi: number; toplamMs: number; enCokMs: number; hata: number; kovalar: number[] };
const rotalar = new Map<string, RotaIstatistik>();
const bellekOrnekleri: any[] = [];
let yavasPencere = 0;
let yavasSayac = 0;
let atlananYavas = 0;

/** Yolun değişken parçalarını `:id` yapar (sayı, uuid/hex, uzun kimlik benzeri parçalar). Saf işlev. */
export function rotaNormalize(yol: string): string {
  const temiz = String(yol || '').split('?')[0];
  return temiz
    .split('/')
    .map((p) => {
      if (!p) return p;
      if (/^\d+$/.test(p)) return ':id';
      if (/^[0-9a-f]{8,}(-[0-9a-f]{4,})*$/i.test(p)) return ':id';
      // harf + rakam karışık ve uzun (ör. q_1699…_abc, sse_…) ya da çok uzun parçalar
      if (p.length >= 16 && /\d/.test(p)) return ':id';
      if (p.length > 40) return ':id';
      if (/^[a-z]+[-_]\d+([-_][\w]+)*$/i.test(p) && /\d{3,}/.test(p)) return ':id';
      return p;
    })
    .join('/');
}

/** Süreyi kova indisine çevirir (0..KOVALAR.length). Saf işlev. */
export function kovaIndisi(ms: number): number {
  for (let i = 0; i < KOVALAR.length; i++) if (ms <= KOVALAR[i]) return i;
  return KOVALAR.length;
}

/** Bir isteği kaydeder (sınamada doğrudan çağrılabilir). */
export function istekKaydet(yontem: string, rota: string, ms: number, durum: number): void {
  let anahtar = `${yontem} ${rota}`;
  let st = rotalar.get(anahtar);
  if (!st) {
    if (rotalar.size >= ROTA_TAVAN) {
      anahtar = `${yontem} (diger)`;
      st = rotalar.get(anahtar);
    }
    if (!st) {
      st = { sayi: 0, toplamMs: 0, enCokMs: 0, hata: 0, kovalar: new Array(KOVALAR.length + 1).fill(0) };
      rotalar.set(anahtar, st);
    }
  }
  st.sayi++;
  st.toplamMs += ms;
  if (ms > st.enCokMs) st.enCokMs = ms;
  if (durum >= 500) st.hata++;
  st.kovalar[kovaIndisi(ms)]++;

  if (ms >= YAVAS_MS) {
    const dk = Math.floor(Date.now() / 60_000);
    if (dk !== yavasPencere) { yavasPencere = dk; yavasSayac = 0; }
    if (yavasSayac < YAVAS_DAKIKA_TAVAN) {
      yavasSayac++;
      veriOlayi('uyari', 'yavas-istek', `${yontem} ${rota} ${Math.round(ms)} ms`, { yontem, rota, ms: Math.round(ms), durum });
    } else atlananYavas++;
  }
}

/** Erken `app.use` ara katmanı: yalnız /api/* ölçülür. */
export function telemetriAraKatmani(): express.RequestHandler {
  return (req, res, next) => {
    if (!req.path.startsWith('/api/') && req.path !== '/api') return next();
    const t0 = process.hrtime.bigint();
    res.once('finish', () => {
      try {
        const tur = String(res.getHeader('Content-Type') || '');
        if (tur.includes('text/event-stream')) return;
        const ms = Number(process.hrtime.bigint() - t0) / 1e6;
        const routePath = (req as any).route?.path;
        const rota = typeof routePath === 'string'
          ? `${req.baseUrl || ''}${routePath}`
          : rotaNormalize(req.originalUrl || req.url);
        istekKaydet(req.method, rota, ms, res.statusCode);
      } catch { /* ölçüm hiçbir isteği bozmasın */ }
    });
    next();
  };
}

let dongu: ReturnType<typeof monitorEventLoopDelay> | null = null;
let ornekZamanlayici: ReturnType<typeof setInterval> | null = null;

export function bellekOrnegiAl(sseIstemci: () => number): any {
  const m = process.memoryUsage();
  const mb = (n: number) => Math.round(n / 1048576);
  const ornek = {
    zaman: new Date().toISOString(),
    rss: mb(m.rss),
    heapUsed: mb(m.heapUsed),
    heapTotal: mb(m.heapTotal),
    external: mb(m.external),
    sseIstemci: (() => { try { return sseIstemci(); } catch { return -1; } })(),
    olayDongusuGecikmeMs: dongu ? Math.round((dongu.percentile(99) / 1e6) * 10) / 10 : null,
    olayDongusuOrtMs: dongu ? Math.round((dongu.mean / 1e6) * 10) / 10 : null,
  };
  if (dongu) dongu.reset();
  bellekOrnekleri.push(ornek);
  if (bellekOrnekleri.length > BELLEK_ORNEK_TAVAN) bellekOrnekleri.shift();
  return ornek;
}

/** 5 dakikada bir bellek örneği (birim MB). Zamanlayıcı süreci açık tutmaz. */
export function bellekOrnekleyiciBaslat(sseIstemci: () => number, aralikMs = 5 * 60_000): void {
  if (ornekZamanlayici) return;
  try { dongu = monitorEventLoopDelay({ resolution: 20 }); dongu.enable(); } catch { dongu = null; }
  ornekZamanlayici = setInterval(() => {
    try {
      const o = bellekOrnegiAl(sseIstemci);
      const { zaman: _z, ...ek } = o;
      veriOlayi('bilgi', 'bellek', `rss ${o.rss} MB, heap ${o.heapUsed}/${o.heapTotal} MB`, ek);
    } catch { /* yok */ }
  }, aralikMs);
  ornekZamanlayici.unref();
}

/** Yönetici özeti: kova tablosu + en yavaş 20 rota + son bellek örnekleri. */
export function telemetriOzeti(): any {
  const tablo = Array.from(rotalar.entries()).map(([rota, st]) => ({
    rota,
    sayi: st.sayi,
    ortMs: st.sayi ? Math.round((st.toplamMs / st.sayi) * 10) / 10 : 0,
    enCokMs: Math.round(st.enCokMs),
    hata5xx: st.hata,
    kovalar: Object.fromEntries(st.kovalar.map((n, i) => [i < KOVALAR.length ? `<=${KOVALAR[i]}` : `>${KOVALAR[KOVALAR.length - 1]}`, n])),
  }));
  tablo.sort((a, b) => b.sayi - a.sayi);
  const enYavas = [...tablo].sort((a, b) => b.ortMs - a.ortMs).slice(0, 20);
  return {
    baslangic: new Date(Date.now() - process.uptime() * 1000).toISOString(),
    rotaSayisi: rotalar.size,
    rotaTavan: ROTA_TAVAN,
    kovaSinirlariMs: KOVALAR,
    atlananYavasKayit: atlananYavas,
    enYavas20: enYavas,
    tablo,
    bellek: bellekOrnekleri.slice(-12),
  };
}

/* ---------------- web-vitals ---------------- */

const VITALS_SAYI_ALANLARI = ['lcp', 'cls', 'inp', 'ttfb', 'uzunGorev'] as const;
const VITALS_DIZE_ALANLARI: Record<string, number> = { rota: 120, surum: 40, cihaz: 24 };

/**
 * Gelen vitals gövdesini (JSON nesnesi ya da sendBeacon'ın text/plain dizesi) doğrular. Saf işlev.
 * Dönüş: temiz kayıt ya da null (geçersiz). Bilinmeyen alanlar atılır; kişisel veri alanı kabul edilmez.
 */
export function vitalsDogrula(govde: unknown): Record<string, any> | null {
  let o: any = govde;
  if (typeof o === 'string') {
    if (o.length > 2048) return null;
    try { o = JSON.parse(o); } catch { return null; }
  }
  if (!o || typeof o !== 'object' || Array.isArray(o)) return null;
  const kayit: Record<string, any> = {};
  for (const k of VITALS_SAYI_ALANLARI) {
    const v = o[k];
    if (v === undefined || v === null || v === '') continue;
    const n = typeof v === 'number' ? v : Number(v);
    if (!Number.isFinite(n) || n < 0 || n > 600_000) return null;
    kayit[k] = k === 'cls' ? Math.round(n * 10000) / 10000 : Math.round(n);
  }
  for (const [k, tavan] of Object.entries(VITALS_DIZE_ALANLARI)) {
    const v = o[k];
    if (v === undefined || v === null) continue;
    if (typeof v !== 'string' && typeof v !== 'number') return null;
    // rota: yalnız yol; sorgu/parça atılır, kimlik benzeri parçalar normalize (kişisel veri sızmasın)
    let s = String(v).replace(/[\u0000-\u001f]/g, '').trim();
    if (k === 'rota') s = rotaNormalize(s.split('#')[0]);
    kayit[k] = s.slice(0, tavan);
  }
  if (!VITALS_SAYI_ALANLARI.some((k) => k in kayit)) return null;
  return kayit;
}

const vitalsIp = new Map<string, { dk: number; n: number }>();
/** IP başına dakikada `tavan` istek; IP yalnız bellekte tutulur. */
export function vitalsHizSiniri(ip: string, tavan = 10): boolean {
  const dk = Math.floor(Date.now() / 60_000);
  const k = vitalsIp.get(ip);
  if (!k || k.dk !== dk) {
    if (vitalsIp.size > 5000) vitalsIp.clear();
    vitalsIp.set(ip, { dk, n: 1 });
    return true;
  }
  if (k.n >= tavan) return false;
  k.n++;
  return true;
}

export function vitalsKaydet(kayit: Record<string, any>): void {
  gunlugeEkle('vitals', { zaman: new Date().toISOString(), ...kayit });
}
