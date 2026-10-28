/**
 * Yönetim v16 — çalışma anı site ayarı (server-only, 2026-10-28).
 *
 * Dosya: src/data/site_ayar.json (paket varsayılanı) → panel yazımı data/content/site_ayar.json (canlı katman,
 * contentOverlay). Dağıtım [0b] (deploy/oracle/content-overlay-sync.sh) data/content altındaki her .json'u yerel
 * src/data'ya geri çeker; çekilen site_ayar.json commit'lenir.
 *
 * Uçlar:
 *  - GET  /api/site-ayar            herkese açık (bellek önbelleği + ETag/304; SW önbelleğine alınmaz)
 *  - GET  /api/admin/site-ayar      tam ayar (guncelleyen dahil)
 *  - PUT  /api/admin/site-ayar      kısmi birleştirme: {sayfalar?, bayraklar?, gorunurluk?, duyuru?, bakim?}
 *                                   haritalarda değer null → anahtar silinir (derleme varsayılanına döner)
 *  - SSE  site_ayar_changed         herkese, gövde = genel ayar
 * Bakım: bakimHataRoutes denetleyicisine bağlıdır (açılışta kalıcı durum uygulanır, POST /api/admin/bakim kalıcı yazılır).
 */
import type express from 'express';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { resolveContent, writableContent } from '../contentOverlay.ts';
import { atomikJsonGuncelle } from './atomikJson.ts';
import { denetimFark, denetimHedef } from './denetim.ts';
import type { BakimDenetleyici } from '../bakimHataRoutes.ts';

export type SayfaDurumu = 'acik' | 'gizli' | 'kapali';
export type GorunurlukDurumu = 'acik' | 'gizli' | 'yalniz-yonetici';
export type Duyuru = { acik: boolean; metin: string; ton: 'bilgi' | 'uyari' | 'hata'; baglanti?: string; bitis?: string };
export type SiteAyar = {
  surum: number;
  guncellendi: string;
  guncelleyen?: string;
  /** Rota kimliği (AppRoute) → durum. Yoksa derleme sabitleri (GIZLI_SAYFALAR/KAPALI_SAYFALAR) geçerli */
  sayfalar: Record<string, SayfaDurumu>;
  /** Özellik bayrakları (ad → açık/kapalı). İstemci: bayrak('ad', varsayilan) */
  bayraklar: Record<string, boolean>;
  /** İçerik görünürlüğü: '<tür>:<kimlik>' (ör. 'kurul:2', 'ders:k2-07', 'varlik:spot:k1-03') → durum */
  gorunurluk: Record<string, GorunurlukDurumu>;
  duyuru: Duyuru | null;
  bakim: { acik: boolean; sure?: string };
};

const BOS: SiteAyar = { surum: 0, guncellendi: '', sayfalar: {}, bayraklar: {}, gorunurluk: {}, duyuru: null, bakim: { acik: false } };
const SAYFA_D = new Set(['acik', 'gizli', 'kapali']);
const GOR_D = new Set(['acik', 'gizli', 'yalniz-yonetici']);

let dosya = '';
let onbellek: { ayar: SiteAyar; genel: string; etag: string } | null = null;

function oku(): SiteAyar {
  try {
    const d = JSON.parse(fs.readFileSync(resolveContent(dosya), 'utf8'));
    return { ...BOS, ...d, sayfalar: d.sayfalar || {}, bayraklar: d.bayraklar || {}, gorunurluk: d.gorunurluk || {}, bakim: d.bakim || { acik: false } };
  } catch {
    return { ...BOS };
  }
}

export function genelAyar(a: SiteAyar) {
  const { guncelleyen: _g, ...rest } = a;
  // Süresi geçmiş duyuru gösterilmez
  if (rest.duyuru?.bitis && Date.parse(rest.duyuru.bitis) < Date.now()) rest.duyuru = { ...rest.duyuru, acik: false };
  return rest;
}

function yenile(a?: SiteAyar) {
  const ayar = a || oku();
  const genel = JSON.stringify(genelAyar(ayar));
  onbellek = { ayar, genel, etag: `"${crypto.createHash('md5').update(genel).digest('hex').slice(0, 16)}"` };
  return onbellek;
}

/** Sunucu içinden okuma (ör. başka bir uç bayrağa bakacaksa) */
export function siteAyarOku(): SiteAyar {
  return (onbellek || yenile()).ayar;
}

function haritaBirlestir<T extends string | boolean>(eski: Record<string, T>, yeni: unknown, gecerli: (v: unknown) => boolean): Record<string, T> {
  if (!yeni || typeof yeni !== 'object') return eski;
  const out = { ...eski };
  for (const [k, v] of Object.entries(yeni as Record<string, unknown>)) {
    const key = String(k).slice(0, 120);
    if (v === null) delete out[key];
    else if (gecerli(v)) out[key] = v as T;
    else throw new Error(`Geçersiz değer: ${key}=${JSON.stringify(v)}`);
  }
  return out;
}

function duyuruDogrula(v: unknown): Duyuru | null {
  if (v === null) return null;
  const d = v as any;
  if (!d || typeof d !== 'object') throw new Error('duyuru nesne olmalı');
  return {
    acik: d.acik === true,
    metin: String(d.metin || '').slice(0, 500),
    ton: d.ton === 'uyari' || d.ton === 'hata' ? d.ton : 'bilgi',
    ...(d.baglanti ? { baglanti: String(d.baglanti).slice(0, 300) } : {}),
    ...(d.bitis ? { bitis: String(d.bitis).slice(0, 40) } : {}),
  };
}

export function registerSiteAyarRoutes(app: express.Express, d: {
  rootDir: string;
  requireAdmin: express.RequestHandler;
  broadcast: (ev: string, data: any) => void;
  bakim?: BakimDenetleyici;
  kimOf?: (req: express.Request) => string;
}) {
  dosya = path.join(d.rootDir, 'src', 'data', 'site_ayar.json');
  const ilk = yenile();
  const yedekKlasoru = path.join(d.rootDir, 'data', '_yedek', 'site_ayar');

  // Bakım kalıcılığı: açılışta kalıcı durum uygulanır (ortam MEDS_BAKIM=1 açıkken kalıcı "kapalı" onu kapatmaz)
  if (d.bakim) {
    if (ilk.ayar.bakim?.acik) d.bakim.ayarla(true, ilk.ayar.bakim.sure);
    d.bakim.onDegisti = (b) => {
      void yaz({ bakim: { acik: b.bakim, ...(b.sure ? { sure: b.sure } : {}) } }, 'bakim-ucu').catch((e) => console.warn('[site-ayar] bakım yazılamadı:', e?.message));
    };
  }

  async function yaz(parca: any, kim: string): Promise<{ once: SiteAyar; sonra: SiteAyar }> {
    let once: SiteAyar = siteAyarOku();
    const hedef = writableContent(dosya);
    // Katmanda kopya yoksa paket varsayılanından başla
    if (!fs.existsSync(hedef)) fs.writeFileSync(hedef, JSON.stringify(once, null, 2));
    const sonra = await atomikJsonGuncelle<SiteAyar>(hedef, (eskiHam) => {
      const eski = { ...BOS, ...(eskiHam || {}) } as SiteAyar;
      once = eski;
      const y: SiteAyar = {
        ...eski,
        sayfalar: haritaBirlestir(eski.sayfalar || {}, parca.sayfalar, (v) => SAYFA_D.has(String(v))),
        bayraklar: haritaBirlestir(eski.bayraklar || {}, parca.bayraklar, (v) => typeof v === 'boolean'),
        gorunurluk: haritaBirlestir(eski.gorunurluk || {}, parca.gorunurluk, (v) => GOR_D.has(String(v))),
        duyuru: 'duyuru' in parca ? duyuruDogrula(parca.duyuru) : eski.duyuru ?? null,
        bakim: parca.bakim && typeof parca.bakim === 'object'
          ? { acik: parca.bakim.acik === true, ...(parca.bakim.sure ? { sure: String(parca.bakim.sure).slice(0, 40) } : {}) }
          : eski.bakim || { acik: false },
        surum: (eski.surum || 0) + 1,
        guncellendi: new Date().toISOString(),
        guncelleyen: kim,
      };
      return y;
    }, { yedek: 5, yedekKlasoru });
    const c = yenile(sonra);
    d.broadcast('site_ayar_changed', JSON.parse(c.genel));
    return { once, sonra };
  }

  app.get('/api/site-ayar', (req, res) => {
    const c = onbellek || yenile();
    res.set('Cache-Control', 'no-cache');
    res.set('ETag', c.etag);
    if (req.headers['if-none-match'] === c.etag) return res.status(304).end();
    res.type('application/json').send(c.genel);
  });

  app.get('/api/admin/site-ayar', d.requireAdmin, (_req, res) => {
    res.json(siteAyarOku());
  });

  app.put('/api/admin/site-ayar', d.requireAdmin, async (req, res) => {
    const parca = req.body || {};
    try {
      const kim = d.kimOf?.(req) || 'yönetici';
      const { once, sonra } = await yaz(parca, kim);
      if (d.bakim && parca.bakim && typeof parca.bakim === 'object') d.bakim.ayarla(sonra.bakim.acik, sonra.bakim.sure);
      denetimHedef(res, 'site-ayar');
      const { surum: _a, guncellendi: _b, guncelleyen: _c, ...o } = once;
      const { surum: _d, guncellendi: _e, guncelleyen: _f, ...s } = sonra;
      denetimFark(res, o, s);
      res.json(sonra);
    } catch (e: any) {
      res.status(400).json({ error: e?.message || 'site ayarı yazılamadı' });
    }
  });
}
