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
import { icerikDurumu, kapaliAnahtarVar, type IcerikTur } from '../icerikGorunurlukKural.ts';

export type SayfaDurumu = 'acik' | 'gizli' | 'kapali' | 'yalniz-yonetici';
export type GorunurlukDurumu = 'acik' | 'gizli' | 'yalniz-yonetici';
export type Duyuru = { acik: boolean; metin: string; ton: 'bilgi' | 'uyari' | 'hata'; baglanti?: string; baslangic?: string; bitis?: string; kurul?: number[]; kapatilabilir?: boolean };
export type SiteAyar = {
  surum: number;
  guncellendi: string;
  guncelleyen?: string;
  /** Rota kimliği (AppRoute) → durum. Yoksa derleme sabitleri (GIZLI_SAYFALAR/KAPALI_SAYFALAR) geçerli */
  sayfalar: Record<string, SayfaDurumu>;
  /** Rota → menüde görünsün mü (false: menü ve merkez kartlarından kalkar, adresle açılır). Yapı/sıra kodda (kural 16) */
  menu: Record<string, boolean>;
  /** Özellik bayrakları (ad → açık/kapalı). İstemci: bayrak('ad', varsayilan) */
  bayraklar: Record<string, boolean>;
  /** İçerik görünürlüğü: '<tür>:<kimlik>' (ör. 'kurul:2', 'ders:k2-07', 'varlik:spot:k1-03') → durum */
  gorunurluk: Record<string, GorunurlukDurumu>;
  duyuru: Duyuru | null;
  bakim: { acik: boolean; sure?: string; mesaj?: string };
};

const BOS: SiteAyar = { surum: 0, guncellendi: '', sayfalar: {}, menu: {}, bayraklar: {}, gorunurluk: {}, duyuru: null, bakim: { acik: false } };
const SAYFA_D = new Set(['acik', 'gizli', 'kapali', 'yalniz-yonetici']);
const GOR_D = new Set(['acik', 'gizli', 'yalniz-yonetici']);

let dosya = '';
let onbellek: { ayar: SiteAyar; genel: string; etag: string } | null = null;

function oku(): SiteAyar {
  try {
    const d = JSON.parse(fs.readFileSync(resolveContent(dosya), 'utf8'));
    return { ...BOS, ...d, sayfalar: d.sayfalar || {}, menu: d.menu || {}, bayraklar: d.bayraklar || {}, gorunurluk: d.gorunurluk || {}, bakim: d.bakim || { acik: false } };
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
    ...(d.baslangic ? { baslangic: String(d.baslangic).slice(0, 40) } : {}),
    ...(d.bitis ? { bitis: String(d.bitis).slice(0, 40) } : {}),
    ...(Array.isArray(d.kurul) && d.kurul.length ? { kurul: d.kurul.map(Number).filter((n: number) => Number.isInteger(n) && n >= 1 && n <= 12).slice(0, 12) } : {}),
    ...(d.kapatilabilir === false ? { kapatilabilir: false } : {}),
  };
}

/**
 * Dış ajan içeriği (AGENTS kural 24): yeni anahtarları `yalniz-yonetici` yapar. Yalnız KAPATIR, açmaz; yönetici onayı
 * (panel › Site › Görünürlük) `acik`'a çevirir. Açılmış bir anahtara dokunmaz.
 */
export async function gorunurlukKilitle(anahtarlar: string[], kim: string): Promise<void> {
  if (!dosya || !anahtarlar.length) return;
  const hedef = writableContent(dosya);
  if (!fs.existsSync(hedef)) fs.writeFileSync(hedef, JSON.stringify(siteAyarOku(), null, 2));
  const sonra = await atomikJsonGuncelle<SiteAyar>(hedef, (eskiHam) => {
    const eski = { ...BOS, ...(eskiHam || {}) } as SiteAyar;
    const g = { ...(eski.gorunurluk || {}) };
    for (const a of anahtarlar) if (!g[a]) g[a] = 'yalniz-yonetici';
    return { ...eski, gorunurluk: g, surum: (eski.surum || 0) + 1, guncellendi: new Date().toISOString(), guncelleyen: kim };
  }, { yedek: 5, yedekKlasoru: path.join(path.dirname(path.dirname(dosya)), '..', 'data', '_yedek', 'site_ayar') });
  yenile(sonra);
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
    if (ilk.ayar.bakim?.acik) d.bakim.ayarla(true, ilk.ayar.bakim.sure, ilk.ayar.bakim.mesaj);
    d.bakim.onDegisti = (b) => {
      void yaz({ bakim: { acik: b.bakim, ...(b.sure ? { sure: b.sure } : {}), ...(b.mesaj ? { mesaj: b.mesaj } : {}) } }, 'bakim-ucu').catch((e) => console.warn('[site-ayar] bakım yazılamadı:', e?.message));
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
        menu: haritaBirlestir(eski.menu || {}, parca.menu, (v) => typeof v === 'boolean'),
        bayraklar: haritaBirlestir(eski.bayraklar || {}, parca.bayraklar, (v) => typeof v === 'boolean'),
        gorunurluk: haritaBirlestir(eski.gorunurluk || {}, parca.gorunurluk, (v) => GOR_D.has(String(v))),
        duyuru: 'duyuru' in parca ? duyuruDogrula(parca.duyuru) : eski.duyuru ?? null,
        bakim: parca.bakim && typeof parca.bakim === 'object'
          ? { acik: parca.bakim.acik === true, ...(parca.bakim.sure ? { sure: String(parca.bakim.sure).slice(0, 40) } : {}), ...(parca.bakim.mesaj ? { mesaj: String(parca.bakim.mesaj).slice(0, 300) } : {}) }
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
    // Bitiş saati olan duyuru: süresi dolunca genel ayar yeniden üretilsin (önbellek yazım anında kurulur)
    const c = onbellek && !onbellek.ayar.duyuru?.bitis ? onbellek : yenile(onbellek?.ayar);
    res.set('Cache-Control', 'no-cache');
    res.set('ETag', c.etag);
    if (req.headers['if-none-match'] === c.etag) return res.status(304).end();
    res.type('application/json').send(c.genel);
  });

  app.get('/api/admin/site-ayar/bayraklar', d.requireAdmin, (_req, res) => {
    const b = siteAyarOku().bayraklar || {};
    res.json({ ogeler: BAYRAKLAR.map((x) => ({ ...x, acik: b[x.ad] !== false, ayarli: x.ad in b })) });
  });

  app.get('/api/admin/site-ayar', d.requireAdmin, (_req, res) => {
    res.json(siteAyarOku());
  });

  app.put('/api/admin/site-ayar', d.requireAdmin, async (req, res) => {
    const parca = req.body || {};
    try {
      const kim = d.kimOf?.(req) || 'yönetici';
      const { once, sonra } = await yaz(parca, kim);
      if (d.bakim && parca.bakim && typeof parca.bakim === 'object') d.bakim.ayarla(sonra.bakim.acik, sonra.bakim.sure, sonra.bakim.mesaj);
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

/**
 * Özellik bayrakları — sunucu kapısı. Bayrak yoksa AÇIK sayılır (varsayılan davranış korunur).
 * Panel: Yönetim › Site › Özellik bayrakları. İstemci karşılığı services/siteAyar.ts BAYRAK_SAYFA (menü/rota gizleme).
 */
export const BAYRAKLAR: { ad: string; etiket: string; aciklama: string }[] = [
  { ad: 'oyunlar', etiket: 'Oyunlar', aciklama: 'Kapalıyken Oyunlar sayfası öğrenciye gizlenir, /api/oyun/* ve canlı oda (WebSocket) katılımı reddedilir.' },
  { ad: 'topluluk_sohbet', etiket: 'Topluluk sohbet odaları', aciklama: 'Kapalıyken sohbet odası listesi, katılma ve mesaj gönderme uçları 403 döner (kanal mesajları etkilenmez).' },
  { ad: 'topluluk_mesaj', etiket: 'Topluluk kanal mesajları', aciklama: 'Kapalıyken topluluk kanallarına yeni mesaj yazılamaz (okuma sürer).' },
  { ad: 'arkadaslik', etiket: 'Arkadaşlık', aciklama: 'Kapalıyken Arkadaşlar sayfası gizlenir, /api/arkadas/* uçları 403 döner.' },
  { ad: 'siralama_herkese', etiket: 'Sıralama herkese açık', aciklama: 'Kapalıyken Sıralama sayfası öğrenciye gizlenir; sıralama uçlarını yalnız yönetici okur.' },
  { ad: 'kayit_acik', etiket: 'Yeni kayıt açık', aciklama: 'Kapalıyken daha önce hiç girmemiş hesap profil oluşturamaz (mevcut kullanıcılar girer).' },
  { ad: 'not_paylas', etiket: 'Not paylaşımı', aciklama: 'Kapalıyken öğrenciler yeni not paylaşamaz.' },
];

/** bayrak → [yöntem desen, yol deseni]; eşleşen istek bayrak kapalıyken (yönetici değilse) 403 alır */
const BAYRAK_UC: Record<string, [RegExp, RegExp][]> = {
  oyunlar: [[/./, /^\/api\/oyun\//]],
  topluluk_sohbet: [[/./, /^\/api\/topluluk\/sohbet(ler)?(\/|$)/]],
  topluluk_mesaj: [[/^POST$/, /^\/api\/topluluk\/mesaj$/]],
  arkadaslik: [[/./, /^\/api\/arkadas(\/|$)/]],
  siralama_herkese: [[/^GET$/, /^\/api\/(kisi\/siralama|basarim\/(hucre-)?siralama)$/]],
  not_paylas: [[/^POST$/, /^\/api\/not-paylas$/]],
};

export function bayrakAcik(ad: string): boolean {
  return siteAyarOku().bayraklar?.[ad] !== false;
}

/** Erken (rotalardan önce) app.use ile takılır. kayit_acik: yeni kullanıcı denetimi için kullaniciVar verilir. */
export function bayrakKapisi(d: { isAdmin: (req: express.Request) => boolean; kullaniciVar?: (uid: string, email: string) => boolean }): express.RequestHandler {
  return (req, res, next) => {
    if (!req.path.startsWith('/api/') || req.path.startsWith('/api/admin/')) return next();
    const b = siteAyarOku().bayraklar || {};
    if (!Object.values(b).some((v) => v === false)) return next();
    for (const [ad, desenler] of Object.entries(BAYRAK_UC)) {
      if (b[ad] !== false) continue;
      if (desenler.some(([y, p]) => y.test(req.method) && p.test(req.path))) {
        if (d.isAdmin(req)) return next();
        return res.status(403).json({ error: 'Bu özellik şu an kapalı.', ozellikKapali: ad });
      }
    }
    if (b.kayit_acik === false && req.method === 'POST' && req.path === '/api/users/sync' && d.kullaniciVar) {
      const uid = String(req.body?.uid || '');
      const email = String(req.body?.email || '').trim().toLowerCase();
      if (!d.kullaniciVar(uid, email) && !d.isAdmin(req)) return res.status(403).json({ error: 'Yeni kayıtlar şu an kapalı.', ozellikKapali: 'kayit_acik' });
    }
    next();
  };
}

/* ================= İçerik görünürlüğü sunucu kapısı (2026-10-28) ================= */

/**
 * Öğrenciye kapalı içeriği (site ayarı `gorunurluk`: ders/kurul/deste/sesli/paket) sunucuda da vermez. Kural istemciyle ortak:
 * `icerikGorunurlukKural.ts`. Yönetici her şeyi alır. Erken (rotalardan önce) app.use ile takılır.
 * - Tekil uç: `/api/canli-ders/:key[/…]`, `/api/canli-ders/ses/:key/…`, `/api/decks|ogren|interactive-decks/:id` → 403 { icerikKapali }.
 * - Liste: `/api/canli-ders` (dersler[].key), `/api/canli-ders/ara` (sonuc[].k), `/api/decks` (dizi ya da {decks}) — yanıt süzülür, ETag/304 kapatılır, önbellek `private`.
 * Önem/asistan/çözücü ve ders içerik paketi ön yüz paketindedir (sunucu ucu yok): süzme istemcide (services/siteAyar.ts::icerikGizli).
 */
export function icerikKapisi(d: { isAdmin: (req: express.Request) => boolean }): express.RequestHandler {
  const TEK_CANLI = /^\/api\/canli-ders\/(?:ses\/)?([^/]+)(?:\/|$)/;
  const TEK_DESTE = /^\/api\/(?:decks|ogren|interactive-decks)\/([^/]+)\/?$/;
  const LISTE_CANLI = /^\/api\/canli-ders\/?$/;
  const LISTE_DESTE = /^\/api\/(?:decks|ogren|interactive-decks)\/?$/;
  const ARA_CANLI = /^\/api\/canli-ders\/ara\/?$/; // sesli ders arama sonuçları (sonuc[].k = sesli anahtarı)
  const OZEL = new Set(['ara', 'cikmis-dizin', 'video-is']);
  return (req, res, next) => {
    if (req.method !== 'GET' || !req.path.startsWith('/api/')) return next();
    const g = (siteAyarOku().gorunurluk || {}) as Record<string, string>;
    if (!kapaliAnahtarVar(g)) return next();
    let m = req.path.match(TEK_CANLI);
    const tekil = (tur: IcerikTur, id: string) => {
      if (icerikDurumu(g, tur, id) === 'acik' || d.isAdmin(req)) return next();
      res.setHeader('Cache-Control', 'no-store');
      return res.status(403).json({ error: 'Bu içerik şu an kapalı.', icerikKapali: true });
    };
    if (m && !OZEL.has(decodeURIComponent(m[1]))) return tekil('sesli', decodeURIComponent(m[1]));
    m = req.path.match(TEK_DESTE);
    if (m) return tekil('deste', decodeURIComponent(m[1]));
    const canliListe = LISTE_CANLI.test(req.path) || ARA_CANLI.test(req.path);
    if (!canliListe && !LISTE_DESTE.test(req.path)) return next();
    if (d.isAdmin(req)) { res.setHeader('Vary', 'Authorization, x-panel-secret'); return next(); }
    const tur: IcerikTur = canliListe ? 'sesli' : 'deste';
    const acik = (x: any) => !x || typeof x !== 'object' || (() => { const id = String(x.key ?? x.id ?? x.k ?? ''); return !id || icerikDurumu(g, tur, id) === 'acik'; })();
    const suz = (body: any) => {
      if (Array.isArray(body)) return body.filter(acik);
      if (body && typeof body === 'object') {
        const out = { ...body };
        for (const k of ['dersler', 'decks', 'items', 'sonuc']) if (Array.isArray(out[k])) out[k] = out[k].filter(acik);
        return out;
      }
      return body;
    };
    // Paylaşılan ETag (yönetici/öğrenci aynı) 304 ile süzülmemiş gövdeyi tarayıcıda bırakmasın
    delete req.headers['if-none-match'];
    const ozelOnbellek = () => { res.removeHeader('ETag'); res.setHeader('Cache-Control', 'private, no-cache'); };
    const json0 = res.json.bind(res);
    const send0 = res.send.bind(res);
    let jsonIcinde = false;
    res.json = ((body: any) => { ozelOnbellek(); jsonIcinde = true; try { return json0(suz(body)); } finally { jsonIcinde = false; } }) as any;
    res.send = ((body: any) => {
      if (!jsonIcinde && typeof body === 'string' && /json/.test(String(res.getHeader('Content-Type') || ''))) {
        try { ozelOnbellek(); return send0(JSON.stringify(suz(JSON.parse(body)))); } catch { /* JSON değil */ }
      }
      return send0(body);
    }) as any;
    next();
  };
}
