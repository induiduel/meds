/**
 * Yönetim v16 — yönetici denetim kaydı (server-only, 2026-10-28).
 *
 * Ara katman (`denetimAraKatmani`) şunları meds-pg `yonetici_denetim` tablosuna yazar:
 *  - TÜM yönetici yazma istekleri: POST/PUT/PATCH/DELETE `/api/admin/*` (+ YAZMA_EK_ONEKLER)
 *  - kişisel veri okumaları: KISISEL_OKUMA desenlerine uyan GET istekleri (profil verisi, sohbet mesajı…)
 * Yanıt bittiğinde (`res.on('finish')`) kim, ne zaman, hangi uç, hedef kimlik, durum kodu, süre ve gövde özeti kaydedilir.
 *
 * Uç yazarları için:
 *  - `denetimHedef(res, 'ders:k2-07')`     → hedef kimliği açıkça bildir (yoksa adresin son parçası / body.id kullanılır)
 *  - `denetimFark(res, onceki, sonraki)`  → değişen alanların özet farkını kayda ekle
 *  - `denetimKaydet(req, {...})`          → ara katmanın görmediği bir olayı elle yaz (ör. toplu iş sonucu)
 *
 * meds-pg kapalıysa satır `data/yonetici_denetim.jsonl` dosyasına düşer (kayıp olmaz). Şema: deploy/pg/sql/yonetim16.sql.
 */
import type express from 'express';
import fs from 'fs';
import path from 'path';
import { pgDb } from '../pgDb.ts';
import { verifiedEmail } from '../adminAuth.ts';
import { listeSorgusu } from './sayfalama.ts';

export type DenetimTur = 'yazma' | 'okuma';
export type DenetimSatiri = {
  id?: number;
  at: string;
  tur: DenetimTur;
  kim: string;
  via: string;
  ip: string;
  yontem: string;
  uc: string;
  hedef: string;
  durum: number;
  sure_ms: number;
  ozet: Record<string, unknown>;
};

/** /api/admin dışında yazma olarak denetlenen yönetici önekleri */
const YAZMA_EK_ONEKLER = ['/api/notebooklm/manage', '/api/sesli-anlatim/yerel', '/api/canli-ders/video-is', '/api/system/services'];
/** Kişisel veri okuması sayılan GET uçları (yeni kişisel veri ucu eklerken buraya desen ekleyin) */
const KISISEL_OKUMA: RegExp[] = [
  /^\/api\/admin\/people\/[^/]+$/,
  /^\/api\/admin\/people\/[^/]+\/(etkinlik|events|cihaz|devices|calisma|study|veri)/,
  /^\/api\/admin\/user-data\//,
  // Kullanıcılar (v16): olay zaman çizelgesi, sosyal/erişim, tüm-kullanıcı etkinlik günlüğü, başarım kişisi, erişim listesi
  /^\/api\/admin\/people\/[^/]+\/(olaylar|sosyal|birlestir)$/,
  /^\/api\/admin\/events$/,
  /^\/api\/admin\/basarim\/kisi\/[^/]+$/,
  /^\/api\/admin\/people-access$/,
  /^\/api\/admin\/topluluk\/(mesajlar|odalar\/[^/]+\/mesajlar)/,
  /^\/api\/admin\/sohbet\//,
  /^\/api\/admin\/topluluk\/(sikayetler|odalar\/[^/]+$|arkadaslik|notlar)/,
  /^\/api\/admin\/pg\/(rows|row)$/,
];
/** Gürültü: kaydı gereksiz yazma uçları */
const ATLA: RegExp[] = [
  /^\/api\/admin\/denetim/,
  /^\/api\/admin\/console-logs\/?$/,
  // XTTS ses işçisinin iş alma / kalp atışı / parça yükleme uçları (yönetici işlemi değil, dakikada bir gelir)
  /^\/api\/sesli-anlatim\/yerel\/(al|kalp|is\/)/,
];

const GIZLI_ANAHTAR = /(pass|parola|sifre|şifre|secret|token|apikey|api_key|authorization|cookie|smtp_pass|privatekey)/i;

let deps: { rootDir: string; dataDir: string; isPgOnline: () => boolean; broadcastAdmin?: (ev: string, d: any) => void } | null = null;
let semaHazir = false;
let yedekDosya = '';

/** Gövdeyi kayda uygun küçük özete indirger: gizli alanlar maskelenir, uzun metin/dizi kırpılır, en fazla ~4 KB */
export function ozetle(v: unknown, derinlik = 0): unknown {
  if (v == null) return v;
  if (typeof v === 'string') return v.length > 200 ? `${v.slice(0, 200)}… (${v.length} karakter)` : v;
  if (typeof v !== 'object') return v;
  if (derinlik >= 3) return Array.isArray(v) ? `[${v.length} öge]` : '{…}';
  if (Array.isArray(v)) {
    const ilk = v.slice(0, 10).map((x) => ozetle(x, derinlik + 1));
    return v.length > 10 ? [...ilk, `… +${v.length - 10} öge`] : ilk;
  }
  const out: Record<string, unknown> = {};
  const keys = Object.keys(v as object);
  for (const k of keys.slice(0, 30)) out[k] = GIZLI_ANAHTAR.test(k) ? '***' : ozetle((v as any)[k], derinlik + 1);
  if (keys.length > 30) out['…'] = `+${keys.length - 30} alan`;
  return out;
}

function sinirla(o: Record<string, unknown>): Record<string, unknown> {
  const s = JSON.stringify(o);
  if (s.length <= 4096) return o;
  return { kirpildi: true, alanlar: Object.keys(o), ham: s.slice(0, 3800) };
}

/** İki nesne arasındaki değişen üst düzey alanlar ({alan: {once, sonra}}), en fazla 40 alan */
export function farkHesapla(onceki: any, sonraki: any): Record<string, { once: unknown; sonra: unknown }> {
  const out: Record<string, { once: unknown; sonra: unknown }> = {};
  const a = onceki && typeof onceki === 'object' ? onceki : {};
  const b = sonraki && typeof sonraki === 'object' ? sonraki : {};
  for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) {
    if (JSON.stringify(a[k]) === JSON.stringify(b[k])) continue;
    out[k] = { once: GIZLI_ANAHTAR.test(k) ? '***' : ozetle(a[k], 1), sonra: GIZLI_ANAHTAR.test(k) ? '***' : ozetle(b[k], 1) };
    if (Object.keys(out).length >= 40) break;
  }
  return out;
}

/** Uç içinden hedef kimliği bildir (ör. 'site-ayar', 'ders:k2-07', 'kisi:<uid>') */
export function denetimHedef(res: express.Response, hedef: string) {
  res.locals.denetim = { ...(res.locals.denetim || {}), hedef: String(hedef).slice(0, 300) };
}

/** Uç içinden özet fark ekle (önceki ve sonraki kayıt) */
export function denetimFark(res: express.Response, onceki: unknown, sonraki: unknown) {
  res.locals.denetim = { ...(res.locals.denetim || {}), fark: farkHesapla(onceki, sonraki) };
}

/** Ek bilgi (ör. {silinen: 12}) */
export function denetimNot(res: express.Response, not: Record<string, unknown>) {
  res.locals.denetim = { ...(res.locals.denetim || {}), not: ozetle(not) };
}

function kimOf(req: express.Request): { kim: string; via: string } {
  const via = String((req as any).adminAuth?.via || '');
  const email = verifiedEmail(req);
  const iddia = String(req.headers['x-admin-email'] || '');
  const kim = email || (via === 'secret' ? 'panel-anahtarı' : via === 'loopback' ? 'yerel' : iddia ? `iddia:${iddia}` : 'bilinmiyor');
  return { kim: kim.slice(0, 200), via: via || (iddia ? 'iddia' : '') };
}

function ipOf(req: express.Request): string {
  return String(req.headers['cf-connecting-ip'] || req.headers['x-real-ip'] || req.socket?.remoteAddress || '').slice(0, 80);
}

function hedefTahmin(req: express.Request): string {
  const b: any = req.body;
  const fromBody = b && typeof b === 'object' && !Array.isArray(b) ? (b.id ?? b.uid ?? b.key ?? b.questionId ?? '') : '';
  if (fromBody) return String(fromBody).slice(0, 300);
  const parts = req.path.split('/').filter(Boolean);
  // /api/admin/<grup>[/<id>...] → grup dışındaki son parça
  return parts.length > 3 ? decodeURIComponent(parts[parts.length - 1]).slice(0, 300) : '';
}

async function yaz(s: DenetimSatiri) {
  if (deps?.isPgOnline() && semaHazir) {
    try {
      await pgDb.query(
        `insert into public.yonetici_denetim (at, tur, kim, via, ip, yontem, uc, hedef, durum, sure_ms, ozet)
         values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)`,
        [s.at, s.tur, s.kim, s.via, s.ip, s.yontem, s.uc, s.hedef, s.durum, s.sure_ms, JSON.stringify(s.ozet)],
      );
      deps.broadcastAdmin?.('denetim_eklendi', { uc: s.uc, tur: s.tur, at: s.at });
      return;
    } catch (e: any) {
      console.warn('[denetim] pg yazılamadı, dosyaya düşüldü:', e?.message);
    }
  }
  if (yedekDosya) fs.promises.appendFile(yedekDosya, JSON.stringify(s) + '\n').catch(() => {});
}

/** Ara katmanın görmediği bir olayı elle kaydet */
export function denetimKaydet(req: express.Request, o: { tur?: DenetimTur; uc?: string; hedef?: string; durum?: number; ozet?: Record<string, unknown> }) {
  const { kim, via } = kimOf(req);
  void yaz({
    at: new Date().toISOString(),
    tur: o.tur || 'yazma',
    kim,
    via,
    ip: ipOf(req),
    yontem: req.method,
    uc: (o.uc || req.path).slice(0, 300),
    hedef: (o.hedef || '').slice(0, 300),
    durum: o.durum ?? 200,
    sure_ms: 0,
    ozet: sinirla((ozetle(o.ozet || {}) as Record<string, unknown>) || {}),
  });
}

function denetlenirMi(req: express.Request): DenetimTur | null {
  const p = req.path;
  if (ATLA.some((r) => r.test(p))) return null;
  const yazma = req.method === 'POST' || req.method === 'PUT' || req.method === 'PATCH' || req.method === 'DELETE';
  if (yazma && (p.startsWith('/api/admin/') || YAZMA_EK_ONEKLER.some((o) => p.startsWith(o)))) return 'yazma';
  if (req.method === 'GET' && KISISEL_OKUMA.some((r) => r.test(p))) return 'okuma';
  return null;
}

/** server.ts: express.json + adminAuthMiddleware'den SONRA, rotalardan ÖNCE app.use(denetimAraKatmani()) */
export function denetimAraKatmani(): express.RequestHandler {
  return (req, res, next) => {
    const tur = denetlenirMi(req);
    if (!tur) return next();
    const t0 = Date.now();
    const govde = tur === 'yazma' && req.body && typeof req.body === 'object' ? ozetle(req.body) : undefined;
    const sorgu = Object.keys(req.query || {}).length ? ozetle(req.query) : undefined;
    res.on('finish', () => {
      // Yetkisiz denemeler de kaydedilir (403), ama durum kodundan ayırt edilir
      const { kim, via } = kimOf(req);
      const ek = res.locals.denetim || {};
      const ozet: Record<string, unknown> = {};
      if (govde !== undefined) ozet.govde = govde;
      if (sorgu !== undefined) ozet.sorgu = sorgu;
      if (ek.fark) ozet.fark = ek.fark;
      if (ek.not) ozet.not = ek.not;
      void yaz({
        at: new Date(t0).toISOString(),
        tur,
        kim,
        via,
        ip: ipOf(req),
        yontem: req.method,
        uc: req.path.slice(0, 300),
        hedef: String(ek.hedef || hedefTahmin(req)).slice(0, 300),
        durum: res.statusCode,
        sure_ms: Date.now() - t0,
        ozet: sinirla(ozet),
      });
    });
    next();
  };
}

/** Şema + okuma ucu: GET /api/admin/denetim?sayfa=&boyut=&hedef=&uc=&kim=&tur=&q=&durum=hata */
export function registerDenetimRoutes(app: express.Express, d: { rootDir: string; dataDir: string; requireAdmin: express.RequestHandler; isPgOnline: () => boolean; broadcastAdmin?: (ev: string, d: any) => void }) {
  deps = d;
  yedekDosya = path.join(d.dataDir, 'yonetici_denetim.jsonl');
  const sqlFile = path.join(d.rootDir, 'deploy', 'pg', 'sql', 'yonetim16.sql');
  const ensure = async () => {
    if (semaHazir || !d.isPgOnline()) return;
    try {
      await pgDb.query(fs.readFileSync(sqlFile, 'utf8'));
      semaHazir = true;
      console.log('🧾 [Denetim] yonetici_denetim şeması hazır.');
    } catch (e: any) {
      console.warn('[Denetim] şema uygulanamadı:', e?.message);
    }
  };
  setTimeout(ensure, 3000);
  const t = setInterval(() => { if (semaHazir) clearInterval(t); else void ensure(); }, 30_000);
  t.unref?.();

  app.get('/api/admin/denetim', d.requireAdmin, async (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50, enFazla: 200 });
    const where: string[] = [];
    const vals: unknown[] = [];
    const add = (sql: string, v: unknown) => { vals.push(v); where.push(sql.replace('?', `$${vals.length}`)); };
    // Süzgeç hem düz (?tur=) hem çip biçiminde (?s.tur=, VeriTablosu) gelebilir
    const qv = (k: string) => String((req.query as any)[k] || s.suzgec[k] || '').trim();
    if (qv('baslangic')) add('at >= ?', qv('baslangic'));
    if (qv('bitis')) add('at <= ?', qv('bitis'));
    if (qv('hedef')) add('hedef = ?', qv('hedef'));
    if (qv('uc')) add('uc like ?', `${qv('uc')}%`);
    if (qv('kim')) add('kim ilike ?', `%${qv('kim')}%`);
    if (qv('tur') === 'yazma' || qv('tur') === 'okuma') add('tur = ?', qv('tur'));
    if (qv('durum') === 'hata') where.push('durum >= 400');
    if (qv('yontem')) add('yontem = ?', qv('yontem').toUpperCase());
    if (s.q) add(`(uc ilike ? or hedef ilike $X or kim ilike $X)`.replace(/\$X/g, `$${vals.length + 1}`), `%${s.q}%`);
    const w = where.length ? `where ${where.join(' and ')}` : '';
    if (!d.isPgOnline() || !semaHazir) {
      // Yedek dosyadan son kayıtlar (pg kapalıyken)
      try {
        const satir = fs.existsSync(yedekDosya) ? fs.readFileSync(yedekDosya, 'utf8').trim().split('\n').filter(Boolean) : [];
        const ogeler = satir.slice(-s.boyut).reverse().map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
        return res.json({ ogeler, toplam: ogeler.length, sayfa: 0, boyut: s.boyut, kaynak: 'dosya' });
      } catch (e: any) { return res.status(500).json({ error: e?.message }); }
    }
    try {
      const yon = s.yon === 'artan' ? 'asc' : 'desc';
      const sira = ['at', 'uc', 'kim', 'durum', 'sure_ms'].includes(s.sirala) ? s.sirala : 'at';
      const [{ rows }, c] = await Promise.all([
        pgDb.query(`select * from public.yonetici_denetim ${w} order by ${sira} ${yon}, id desc limit ${s.boyut} offset ${s.sayfa * s.boyut}`, vals),
        pgDb.query(`select count(*)::int n from public.yonetici_denetim ${w}`, vals),
      ]);
      res.json({ ogeler: rows, toplam: c.rows[0]?.n || 0, sayfa: s.sayfa, boyut: s.boyut, kaynak: 'pg' });
    } catch (e: any) {
      res.status(500).json({ error: e?.message });
    }
  });
}

/** Son N denetim satırı (Genel bakış için) */
export async function sonDenetimler(n = 8): Promise<DenetimSatiri[]> {
  if (!deps?.isPgOnline() || !semaHazir) return [];
  try {
    const { rows } = await pgDb.query(`select id, at, tur, kim, yontem, uc, hedef, durum from public.yonetici_denetim order by at desc limit $1`, [n]);
    return rows as DenetimSatiri[];
  } catch { return []; }
}
