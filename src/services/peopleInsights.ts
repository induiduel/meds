/**
 * Kişiler (yönetim paneli) — her kullanıcının tek ekranda tüm izi:
 *   hesap bilgisi, cihazlar (ad, platform, ilk/son görülme), kullanım süresi (cihaz × gün), skorlar (test geçmişi),
 *   etkinlik günlüğü, yorumlar, notlar (kişisel defter + Öğren ortak notları), yazdığı sorular, şık / ipucu katkıları,
 *   beğeniler, hata bildirimleri ve öneriler.
 *
 * Veri yolu (canlı, veritabanı aracılı):
 *   tarayıcı → POST /api/presence (60 sn'de bir, yalnız sekme görünürken) → meds-pg user_devices + user_usage_daily
 *   öğrenci yazma uçları → trackActivity ara katmanı → meds-pg user_events
 *   tablo tetikleyicisi pg_notify('meds_changes') → server.ts hub → yalnız yöneticilere SSE `people_changed`
 *   panel olayı alınca açık listeyi/kişiyi yeniden çeker (debounce).
 * Veritabanı kapalıysa yazımlar bellekte kuyrukta bekler, bağlantı gelince boşaltılır (kayıp yok).
 *
 * Erişim: kişisel veri olduğu için bu uçlar başlıktaki e-postaya güvenmez (bkz. isStrongAdmin):
 * yalnız cihazdaki sunucuya loopback, Firebase'in doğruladığı yönetici jetonu ya da iki sunucunun .env'indeki
 * MEDS_PANEL_SECRET. Yerel panel Oracle'daki kişilere yerel sunucu üzerinden (vekil) ulaşır.
 */
import express from 'express';
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import { pgDb } from './pgDb';
import { requestUser } from './firebaseIdentity';
import { notificationLinkFor } from './notificationLinks';

type Any = Record<string, any>;

export interface PeopleDeps {
  rootDir: string;
  dataDir: string;
  adminEmail: string;
  isPgOnline: () => boolean;
  loadUsers: () => Any[];
  getPastQuestions: () => Any[];
  getPoolQuestions: () => Any[];
  /** Yalnız yöneticilere SSE (veritabanı kapalıyken doğrudan yayın için) */
  broadcastAdmin: (event: string, data: any) => void;
  oracleApiUrl: string;
}

const clip = (v: unknown, n: number) => String(v ?? '').replace(/\s+/g, ' ').trim().slice(0, n);
const lc = (v: unknown) => String(v ?? '').trim().toLowerCase();
const hash16 = (s: string) => crypto.createHash('sha256').update(s).digest('hex').slice(0, 16);
/** Gizli cihaz jetonundan (dev-…) herkese açık cihaz kimliği; istemci aynısını üretir (src/services/presence.ts) */
export const publicDeviceId = (token: string) => `p${crypto.createHash('sha256').update(`pub:${token}`).digest('hex').slice(0, 23)}`;
const DEVICE_RE = /^[a-z0-9-]{8,64}$/i;
/** Ad eşleşmesi bu genel adlarda yapılmaz (herkes "Öğrenci" olabilir) */
const GENERIC_NAMES = new Set(['', 'öğrenci', 'anonim', 'anonim öğrenci', 'tıp öğrencisi', 'misafir', 'kullanıcı', 'sistem', 'yönetici']);

/* ------------------------------------------------------------------ */
/* Erişim                                                              */
/* ------------------------------------------------------------------ */

function isLoopback(req: express.Request) {
  const ip = String(req.socket?.remoteAddress || '');
  // Tünel/Caddy arkasındaki istekler de loopback'ten gelir: vekil başlığı varsa dış istek sayılır
  if (req.headers['cf-connecting-ip'] || req.headers['x-forwarded-for']) return false;
  return ip === '127.0.0.1' || ip === '::1' || ip === '::ffff:127.0.0.1';
}

function panelSecret(): string {
  return String(process.env.MEDS_PANEL_SECRET || '').trim();
}

function secretOk(req: express.Request) {
  const expected = panelSecret();
  const supplied = String(req.headers['x-panel-secret'] || '');
  if (expected.length < 24 || supplied.length !== expected.length) return false;
  return crypto.timingSafeEqual(Buffer.from(supplied), Buffer.from(expected));
}

export async function isStrongAdmin(req: express.Request, adminEmail: string): Promise<boolean> {
  if (isLoopback(req) || secretOk(req)) return true;
  const who = await requestUser(req);
  return !!who.user && lc(who.user.email) === lc(adminEmail);
}

/* ------------------------------------------------------------------ */
/* Yazım kuyruğu (veritabanı kapalıyken kayıp olmasın)                 */
/* ------------------------------------------------------------------ */

type Job = { sql: string; values: any[] };
const queue: Job[] = [];
let draining = false;
let schemaReady = false;

async function drain(deps: PeopleDeps) {
  if (draining || !schemaReady || !deps.isPgOnline()) return;
  draining = true;
  try {
    while (queue.length) {
      const job = queue[0];
      try {
        await pgDb.query(job.sql, job.values);
        queue.shift();
      } catch (e: any) {
        // Bağlantı hatası: sonra yeniden denenir. Veri hatası (ör. çok uzun alan): iş atılır.
        if (/ECONNREFUSED|terminat|Connection|timeout/i.test(String(e?.message))) break;
        console.warn('[Kişiler] yazım atlandı:', e?.message);
        queue.shift();
      }
    }
  } finally {
    draining = false;
  }
}

function enqueue(deps: PeopleDeps, sql: string, values: any[]) {
  if (queue.length > 20_000) queue.splice(0, queue.length - 20_000);
  queue.push({ sql, values });
  void drain(deps);
}

/* ------------------------------------------------------------------ */
/* Kimlik: istek → (uid, e-posta, ad, cihaz)                            */
/* ------------------------------------------------------------------ */

export interface Actor {
  uid: string | null;
  email: string | null;
  name: string | null;
  deviceId: string | null;
  verified: boolean;
}

/** Cihaz → son doğrulanmış hesap (giriş yapmış cihazın jetonsuz isteklerini de doğru kişiye bağlamak için) */
const deviceOwner = new Map<string, { uid: string; email: string | null; name: string | null }>();

async function actorOf(req: express.Request): Promise<Actor> {
  const b: Any = req.body && typeof req.body === 'object' ? req.body : {};
  const deviceId = DEVICE_RE.test(String(req.headers['x-device-id'] || b.deviceId || '')) ? String(req.headers['x-device-id'] || b.deviceId) : null;
  let uid: string | null = null;
  let email: string | null = null;
  let verified = false;
  try {
    const who = await requestUser(req);
    if (who.user) {
      uid = who.user.uid;
      email = who.user.email || null;
      verified = true;
    }
  } catch {
    /* jeton doğrulanamadı */
  }
  const name =
    clip(b.author?.name || b.author || b.reportedBy || b.suggestedBy || b.authorName || b.contributedByName || b.displayName || '', 80) || null;
  if (!uid) {
    const claimed = clip(b.authorUid || b.reporterUid || b.uid || b.userId || b.voterId || b.author?.id || req.headers['x-user-id'] || req.headers['x-voter-uid'] || '', 128);
    // Cihaz jetonu (dev-…) gizlidir: kimlik olarak saklanmaz, yalnız özeti tutulur
    if (claimed && !claimed.startsWith('dev-')) uid = claimed;
    email = clip(b.authorEmail || b.reporterEmail || '', 160).toLowerCase() || null;
  }
  if (!uid && deviceId) {
    const own = deviceOwner.get(deviceId);
    if (own) {
      uid = own.uid;
      email = email || own.email;
    }
  }
  return { uid, email, name, deviceId, verified };
}

/* ------------------------------------------------------------------ */
/* Cihaz adı (User-Agent + istemcinin verdiği model)                   */
/* ------------------------------------------------------------------ */

export function describeDevice(ua: string, hint: Any = {}): { label: string; platform: string; browser: string; model: string } {
  const s = ua || '';
  let platform = clip(hint.platform, 40);
  if (!platform) {
    if (/iPhone/.test(s)) platform = 'iPhone';
    else if (/iPad/.test(s) || (/Macintosh/.test(s) && /Mobile/.test(s))) platform = 'iPad';
    else if (/Android/.test(s)) platform = 'Android';
    else if (/Windows/.test(s)) platform = 'Windows';
    else if (/CrOS/.test(s)) platform = 'ChromeOS';
    else if (/Mac OS X|Macintosh/.test(s)) platform = 'macOS';
    else if (/Linux/.test(s)) platform = 'Linux';
    else platform = 'Bilinmeyen';
  }
  let browser = '';
  if (/Edg\//.test(s)) browser = 'Edge';
  else if (/OPR\/|Opera/.test(s)) browser = 'Opera';
  else if (/SamsungBrowser/.test(s)) browser = 'Samsung Internet';
  else if (/YaBrowser/.test(s)) browser = 'Yandex';
  else if (/Firefox\/|FxiOS/.test(s)) browser = 'Firefox';
  else if (/CriOS|Chrome\//.test(s)) browser = 'Chrome';
  else if (/Safari\//.test(s)) browser = 'Safari';
  else browser = 'Tarayıcı';
  let model = clip(hint.model, 60);
  if (!model) {
    const m = /Android [\d.]+; (?:[a-z]{2}-[a-z]{2}; )?([^;)]+?)(?: Build|\))/i.exec(s);
    if (m && !/^K$/.test(m[1].trim())) model = clip(m[1], 60);
  }
  if (hint.standalone) browser = `${browser} (uygulama)`;
  const label = clip(hint.name, 60) || [model || platform, browser].filter(Boolean).join(' · ');
  return { label, platform, browser, model };
}

/* ------------------------------------------------------------------ */
/* Eylem günlüğü: hangi istek hangi kayıt                              */
/* ------------------------------------------------------------------ */

type Rule = {
  m: string;
  re: RegExp;
  kind: string;
  action?: string;
  label: (p: string[], b: Any) => string;
  link?: (p: string[], b: Any) => string;
  body?: (b: Any) => string;
};
const enc = encodeURIComponent;
const past = (id: string, commentId?: string) => notificationLinkFor({ kind: 'past_question', id, commentId });
const pool = (id: string) => notificationLinkFor({ kind: 'pool_question', id });

const RULES: Rule[] = [
  { m: 'POST', re: /^\/api\/past-exams\/([^/]+)\/comment$/, kind: 'comment', label: () => 'Çıkmış soruya yorum', link: (p) => past(p[0]), body: (b) => b.text },
  { m: 'PUT', re: /^\/api\/past-exams\/([^/]+)\/comments\/([^/]+)$/, kind: 'comment', action: 'edit', label: () => 'Yorumunu düzenledi', link: (p) => past(p[0], p[1]), body: (b) => b.text },
  { m: 'DELETE', re: /^\/api\/past-exams\/([^/]+)\/comments\/([^/]+)$/, kind: 'comment', action: 'delete', label: () => 'Yorumunu sildi', link: (p) => past(p[0]) },
  { m: 'POST', re: /^\/api\/past-exams\/([^/]+)\/report$/, kind: 'report', label: (_p, b) => `Çıkmış soru bildirimi: ${clip(b.reason, 80)}`, link: (p) => past(p[0]), body: (b) => b.details },
  { m: 'POST', re: /^\/api\/past-exams\/([^/]+)\/upvote$/, kind: 'like', label: () => 'Çıkmış soruyu beğendi', link: (p) => past(p[0]) },
  { m: 'POST', re: /^\/api\/past-exams\/([^/]+)\/downvote$/, kind: 'like', action: 'dislike', label: () => 'Çıkmış soruyu beğenmedi', link: (p) => past(p[0]) },
  { m: 'POST', re: /^\/api\/past-question-reviews\/([^/]+)\/answer-votes$/, kind: 'vote', label: (_p, b) => `Cevap oyu: ${clip(b.choice, 2)}`, link: (p) => past(p[0]) },
  { m: 'POST', re: /^\/api\/questions$/, kind: 'question', label: (_p, b) => `Soru yazdı: ${clip(b.topic || b.discipline || b.question?.topic || '', 80)}`, body: (b) => b.stem || b.text || b.question?.stem },
  { m: 'POST', re: /^\/api\/questions\/([^/]+)\/report$/, kind: 'report', label: (_p, b) => `Havuz sorusu bildirimi: ${clip(b.reason, 80)}`, link: (p) => pool(p[0]), body: (b) => b.details },
  { m: 'POST', re: /^\/api\/questions\/([^/]+)\/upvote$/, kind: 'like', label: () => 'Havuz sorusunu beğendi', link: (p) => pool(p[0]) },
  { m: 'POST', re: /^\/api\/questions\/([^/]+)\/fragments$/, kind: 'fragment', label: () => 'Soruya hafıza/ipucu ekledi', link: (p) => pool(p[0]), body: (b) => b.text },
  { m: 'POST', re: /^\/api\/questions\/([^/]+)\/fragments\/([^/]+)\/upvote$/, kind: 'like', label: () => 'Bir katkıyı beğendi', link: (p) => pool(p[0]) },
  { m: 'POST', re: /^\/api\/questions\/([^/]+)\/options$/, kind: 'option', label: (_p, b) => `Şık ekledi (${clip(b.key, 2)})`, link: (p) => pool(p[0]), body: (b) => b.text },
  { m: 'POST', re: /^\/api\/questions\/([^/]+)\/options\/([^/]+)\/upvote$/, kind: 'like', label: (p) => `Şıkkı beğendi (${p[1]})`, link: (p) => pool(p[0]) },
  { m: 'POST', re: /^\/api\/questions\/([^/]+)\/claimed-answer$/, kind: 'answer', label: (_p, b) => `Cevap önerdi: ${clip(b.answer, 2)}`, link: (p) => pool(p[0]) },
  { m: 'POST', re: /^\/api\/terms\/([^/]+)\/report$/, kind: 'report', label: (_p, b) => `Sözlük bildirimi: ${clip(b.reason, 80)}`, link: (p) => notificationLinkFor({ kind: 'term', id: p[0] }), body: (b) => b.details },
  { m: 'POST', re: /^\/api\/cards\/([^/]+)\/report$/, kind: 'report', label: (_p, b) => `Kart bildirimi: ${clip(b.reason, 80)}`, link: (p) => notificationLinkFor({ kind: 'flashcard', id: p[0] }), body: (b) => b.details },
  { m: 'POST', re: /^\/api\/ornek-sorular\/([^/]+)\/report$/, kind: 'report', label: (_p, b) => `Örnek soru bildirimi: ${clip(b.reason, 80)}`, link: (p) => notificationLinkFor({ kind: 'ornek_question', id: p[0] }), body: (b) => b.details },
  { m: 'POST', re: /^\/api\/universal-report$/, kind: 'report', label: (_p, b) => `Bildirim (${clip(b.targetType, 30)}): ${clip(b.reason, 80)}`, link: (_p, b) => (typeof b.link === 'string' && b.link.startsWith('/') ? b.link : ''), body: (b) => b.details },
  { m: 'POST', re: /^\/api\/learn\/feedback$/, kind: 'report', label: (_p, b) => `Öğren bildirimi: ${clip(b.field || b.targetLabel, 80)}`, link: (_p, b) => (b.deckId ? `/ogren/${enc(b.deckId)}?adim=${Number(b.slideNumber) || 1}` : ''), body: (b) => b.reason },
  { m: 'POST', re: /^\/api\/learn\/feedback\/([^/]+)\/vote$/, kind: 'like', label: (_p, b) => (Number(b.vote) < 0 ? 'Öğren bildirimini reddetti' : 'Öğren bildirimini destekledi') },
  { m: 'POST', re: /^\/api\/learn\/social\/notes$/, kind: 'note', label: (_p, b) => `Öğren notu (${clip(b.kind, 10)})`, link: (_p, b) => (b.deckId ? `/ogren/${enc(b.deckId)}?adim=${Number(b.stepNumber) || 1}` : ''), body: (b) => b.body },
  { m: 'POST', re: /^\/api\/learn\/social\/threads$/, kind: 'report', label: () => 'Öğren metin bildirimi', link: (_p, b) => (b.deckId ? `/ogren/${enc(b.deckId)}?adim=${Number(b.stepNumber) || 1}` : ''), body: (b) => `${clip(b.quote, 200)} — ${clip(b.body, 400)}` },
  { m: 'POST', re: /^\/api\/learn\/social\/threads\/([^/]+)\/messages$/, kind: 'comment', label: () => 'Öğren tartışmasına yazdı', body: (b) => b.body },
  { m: 'POST', re: /^\/api\/recall\/feedback$/, kind: 'feedback', label: () => 'Soru havuzu eşleşme geri bildirimi' },
];

/* ------------------------------------------------------------------ */

export function registerPeopleInsights(app: express.Express, deps: PeopleDeps) {
  const backupsDir = path.join(deps.dataDir, 'user_backups');
  const sqlFile = path.join(deps.rootDir, 'deploy', 'pg', 'sql', 'user_activity.sql');

  // Şema: açılışta (ve veritabanı geç gelirse 30 sn'de bir) uygulanır
  const ensureSchema = async () => {
    if (schemaReady || !deps.isPgOnline()) return;
    try {
      await pgDb.query(fs.readFileSync(sqlFile, 'utf8'));
      schemaReady = true;
      const { rows } = await pgDb.query(`select device_id, uid, email, display_name from user_devices where uid is not null and verified`);
      for (const r of rows) deviceOwner.set(r.device_id, { uid: r.uid, email: r.email, name: r.display_name });
      console.log(`👥 [Kişiler] şema hazır (${rows.length} doğrulanmış cihaz).`);
      void drain(deps);
    } catch (e: any) {
      console.warn('[Kişiler] şema uygulanamadı:', e?.message);
    }
  };
  setTimeout(ensureSchema, 2500);
  setInterval(() => {
    void ensureSchema();
    void drain(deps);
  }, 30_000).unref?.();

  const recordEvent = (a: Actor, e: { kind: string; action?: string; ref?: string; label: string; body?: string; link?: string; meta?: Any }) => {
    enqueue(
      deps,
      `insert into user_events (uid, email, display_name, device_id, kind, action, ref, label, body, link, meta)
       values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)`,
      [a.uid, a.email, a.name, a.deviceId, e.kind, e.action || 'create', e.ref || null, clip(e.label, 200), clip(e.body, 2000), clip(e.link, 500), e.meta || {}],
    );
    if (!deps.isPgOnline()) deps.broadcastAdmin('people_changed', { table: 'user_events', uids: [a.uid], kinds: [e.kind], at: Date.now() });
  };

  /* ---------------- Ara katman: öğrenci eylemleri ---------------- */
  app.use((req, res, next) => {
    if (req.method === 'GET' || req.method === 'OPTIONS' || req.method === 'HEAD') return next();
    const p = String(req.path || '');
    if (!p.startsWith('/api/')) return next();
    const rule = RULES.find((r) => r.m === req.method && r.re.test(p));
    if (!rule) return next();
    const params = (rule.re.exec(p) || []).slice(1).map((x) => decodeURIComponent(x));
    const body: Any = req.body && typeof req.body === 'object' ? { ...req.body } : {};
    // Yönetici eylemleri öğrenci günlüğüne yazılmaz
    const adminHeader = lc(req.headers['x-admin-email'] || body.adminEmail);
    res.on('finish', () => {
      if (res.statusCode >= 400 || adminHeader === lc(deps.adminEmail)) return;
      void (async () => {
        try {
          const a = await actorOf(req);
          recordEvent(a, {
            kind: rule.kind,
            action: rule.action,
            ref: params.join('/') || undefined,
            label: rule.label(params, body),
            body: rule.body ? clip(rule.body(body), 2000) : '',
            link: rule.link ? rule.link(params, body) : '',
          });
        } catch (e: any) {
          console.warn('[Kişiler] eylem kaydedilemedi:', e?.message);
        }
      })();
    });
    next();
  });

  /* ---------------- Varlık + kullanım süresi ---------------- */
  const beatAt = new Map<string, number>();
  // sendBeacon gövdesi text/plain gelir
  app.use('/api/presence', express.text({ type: 'text/plain', limit: '8kb' }));
  app.post('/api/presence', async (req, res) => {
    if (typeof req.body === 'string') {
      try {
        req.body = JSON.parse(req.body);
      } catch {
        req.body = {};
      }
    }
    const b: Any = req.body && typeof req.body === 'object' ? req.body : {};
    const deviceId = String(b.deviceId || req.headers['x-device-id'] || '');
    if (!DEVICE_RE.test(deviceId)) return res.status(400).json({ error: 'Cihaz kimliği geçersiz.' });
    const now = Date.now();
    const last = beatAt.get(deviceId) || 0;
    if (now - last < 15_000 && !b.start) return res.json({ ok: true, throttled: true });
    beatAt.set(deviceId, now);
    if (beatAt.size > 50_000) beatAt.clear();

    const a = await actorOf(req);
    // Doğrulanmamış iddia (jetonsuz uid) cihaz kaydını bir hesaba BAĞLAMAZ; yalnız jetonla bağlanır
    const uid = a.verified ? a.uid : deviceOwner.get(deviceId)?.uid || null;
    const email = a.verified ? a.email : deviceOwner.get(deviceId)?.email || null;
    const name = clip(b.displayName, 80) || (a.verified ? a.name : deviceOwner.get(deviceId)?.name) || null;
    if (a.verified && uid) deviceOwner.set(deviceId, { uid, email, name });
    const active = Math.max(0, Math.min(Number(b.activeSec) || 0, 120));
    const d = describeDevice(String(req.headers['user-agent'] || ''), b.device || {});
    const day = new Date().toLocaleDateString('sv-SE', { timeZone: 'Europe/Istanbul' });
    enqueue(
      deps,
      `insert into user_devices (device_id, uid, email, display_name, verified, label, platform, browser, model, user_agent, active_seconds, sessions, last_path)
       values ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,1,$12)
       on conflict (device_id) do update set
         uid = coalesce(excluded.uid, user_devices.uid),
         email = coalesce(excluded.email, user_devices.email),
         display_name = coalesce(excluded.display_name, user_devices.display_name),
         verified = user_devices.verified or excluded.verified,
         label = excluded.label, platform = excluded.platform, browser = excluded.browser,
         model = case when excluded.model <> '' then excluded.model else user_devices.model end,
         user_agent = excluded.user_agent,
         active_seconds = user_devices.active_seconds + excluded.active_seconds,
         sessions = user_devices.sessions + case when now() - user_devices.last_seen > interval '30 minutes' or ($13 and now() - user_devices.last_seen > interval '5 minutes') then 1 else 0 end,
         last_seen = now(), last_path = excluded.last_path`,
      [deviceId, uid, email, name, !!(a.verified && uid), d.label, d.platform, d.browser, d.model, clip(req.headers['user-agent'], 400), active, clip(b.path, 200), !!b.start],
    );
    if (active > 0) {
      enqueue(
        deps,
        `insert into user_usage_daily (device_id, day, uid, active_seconds) values ($1,$2,$3,$4)
         on conflict (device_id, day) do update set active_seconds = user_usage_daily.active_seconds + excluded.active_seconds,
           uid = coalesce(excluded.uid, user_usage_daily.uid)`,
        [deviceId, day, uid, active],
      );
    }
    if (!deps.isPgOnline()) deps.broadcastAdmin('people_changed', { table: 'user_devices', uids: [uid], at: now });
    res.json({ ok: true });
  });

  /* ---------------- Okuma: kaynaklar ---------------- */
  const readJson = <T,>(file: string, fb: T): T => {
    try {
      return JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch {
      return fb;
    }
  };
  const backupFile = (id: string) =>
    path.join(backupsDir, `${crypto.createHash('sha256').update(id.trim().toLowerCase()).digest('hex').slice(0, 40)}.json`);

  /** Tüm profil yedekleri: doğrulanmış hesaplar + girişsiz cihazlar (e-posta kopyaları elenir) */
  const loadBackups = (): Any[] => {
    let files: string[] = [];
    try {
      files = fs.readdirSync(backupsDir).filter((f) => f.endsWith('.json'));
    } catch {
      return [];
    }
    const byUid = new Map<string, Any>();
    for (const f of files) {
      const b = readJson<Any | null>(path.join(backupsDir, f), null);
      if (!b?.uid) continue;
      const prev = byUid.get(b.uid);
      if (!prev || String(b.serverSavedAt || '') > String(prev.serverSavedAt || '')) byUid.set(b.uid, b);
    }
    return [...byUid.values()];
  };

  type Person = {
    key: string;
    kind: 'account' | 'guest';
    uid: string | null;
    email: string | null;
    name: string;
    studentNumber: string | null;
    phone: string | null;
    role: string;
    photoURL: string | null;
    createdAt: string | null;
    lastLoginAt: string | null;
    ids: Set<string>; // eşleşme kimlikleri (uid, e-posta, cihaz jetonu)
    devs: Set<string>; // herkese açık cihaz kimlikleri (girişsiz yedeklerden)
    names: Set<string>;
    backup: Any | null;
  };

  const people = (): Person[] => {
    const users = deps.loadUsers();
    const backups = loadBackups();
    const out: Person[] = [];
    const byId = new Map<string, Person>();
    for (const u of users) {
      // Aynı e-postanın ikinci hesap kaydı (ör. yerel yönetici + Google hesabı) tek kişide birleşir
      const twin = u.email ? byId.get(lc(u.email)) : undefined;
      if (twin) {
        twin.ids.add(u.uid);
        if (u.displayName && !GENERIC_NAMES.has(lc(u.displayName))) twin.names.add(lc(u.displayName));
        if (!twin.studentNumber && u.studentNumber) twin.studentNumber = u.studentNumber;
        if (String(u.lastLoginAt || '') > String(twin.lastLoginAt || '')) twin.lastLoginAt = u.lastLoginAt;
        byId.set(u.uid, twin);
        continue;
      }
      const p: Person = {
        key: `u:${u.uid}`,
        kind: 'account',
        uid: u.uid,
        email: u.email || null,
        name: u.displayName || (u.email || '').split('@')[0] || 'Öğrenci',
        studentNumber: u.studentNumber || null,
        phone: u.phone || u.phoneNumber || null,
        role: u.role || 'student',
        photoURL: u.photoURL || null,
        createdAt: u.createdAt || null,
        lastLoginAt: u.lastLoginAt || null,
        ids: new Set([u.uid, lc(u.email)].filter(Boolean)),
        names: new Set([lc(u.displayName)].filter((n) => !GENERIC_NAMES.has(n))),
        devs: new Set(),
        backup: null,
      };
      out.push(p);
      byId.set(u.uid, p);
      if (u.email) byId.set(lc(u.email), p);
    }
    for (const b of backups) {
      const owner = byId.get(b.uid) || (b.verified && b.email ? byId.get(lc(b.email)) : undefined);
      if (owner) {
        if (!owner.backup || String(b.serverSavedAt || '') > String(owner.backup.serverSavedAt || '')) owner.backup = b;
        owner.ids.add(b.uid);
        if (String(b.uid).startsWith('dev-')) owner.devs.add(publicDeviceId(b.uid));
        continue;
      }
      const p: Person = {
        key: b.verified ? `u:${b.uid}` : `g:${hash16(b.uid)}`,
        kind: b.verified ? 'account' : 'guest',
        uid: b.verified ? b.uid : null,
        email: b.verified ? b.email || null : null,
        name: b.displayName || (b.verified ? (b.email || '').split('@')[0] : 'Misafir cihaz'),
        studentNumber: b.studentNumber || null,
        phone: null,
        role: 'student',
        photoURL: null,
        createdAt: null,
        lastLoginAt: null,
        ids: new Set([b.uid, lc(b.email)].filter(Boolean)),
        names: new Set(),
        devs: new Set(String(b.uid).startsWith('dev-') ? [publicDeviceId(b.uid)] : []),
        backup: b,
      };
      out.push(p);
    }
    return out;
  };

  const sinceIso = (b: Any | null) => String(b?.serverSavedAt || '');

  /** Bir kişinin içerik katkıları (çıkmış + havuz + Öğren bildirimleri + örnek soru bildirimleri) */
  const contributions = (p: Person) => {
    const has = (...ids: unknown[]) => ids.some((x) => x && p.ids.has(String(x)) || (x && p.ids.has(lc(x))));
    const byName = (n: unknown) => p.names.size > 0 && p.names.has(lc(n));
    const items: Any[] = [];
    const push = (x: Any) => items.push(x);

    for (const q of deps.getPastQuestions()) {
      const title = clip(q.topic || q.discipline || q.stem || 'Çıkmış soru', 90);
      for (const c of q.comments || []) {
        const strong = has(c.authorUid, c.authorEmail);
        if (strong || (!c.authorUid && !c.authorEmail && byName(c.author))) {
          push({ kind: 'comment', id: c.id, questionId: q.id, source: 'past', title, body: clip(c.text, 1500), at: c.createdAt || c.timestamp, link: past(q.id, c.id), weak: !strong });
        }
      }
      for (const r of q.reports || []) {
        const strong = has(r.reporterUid, r.reporterEmail);
        if (strong || (!r.reporterUid && !r.reporterEmail && byName(r.reportedBy))) {
          push({ kind: 'report', id: r.id, questionId: q.id, source: 'past', title: `${clip(r.reason, 80)} · ${title}`, body: clip(r.details, 1500), at: r.timestamp || r.createdAt, status: r.status || (r.resolved ? 'resolved' : 'pending'), link: past(q.id), weak: !strong });
        }
      }
      if ((q.likedBy || []).some((v: string) => p.ids.has(v))) push({ kind: 'like', id: `pl-${q.id}`, questionId: q.id, source: 'past', title, at: null, link: past(q.id) });
      if ((q.dislikedBy || []).some((v: string) => p.ids.has(v))) push({ kind: 'like', action: 'dislike', id: `pd-${q.id}`, questionId: q.id, source: 'past', title, at: null, link: past(q.id) });
    }
    for (const q of deps.getPoolQuestions()) {
      const title = clip(q.topic || q.discipline || q.stem || 'Havuz sorusu', 90);
      const link = pool(q.id);
      if (has(q.contributedByUid, q.contributedByEmail) || (!q.contributedByUid && byName(q.contributedByName))) {
        push({ kind: 'question', id: q.id, questionId: q.id, source: 'pool', title, body: clip(q.stem || q.text, 600), at: q.createdAt, status: q.status, link, weak: !q.contributedByUid });
      }
      for (const f of q.fragments || []) {
        if (has(f.authorUid, f.authorEmail) || (!f.authorUid && byName(f.author))) {
          push({ kind: 'fragment', id: f.id, questionId: q.id, source: 'pool', title, body: clip(f.text, 800), at: f.timestamp, link, weak: !f.authorUid });
        }
        if ((f.likedBy || []).some((v: string) => p.ids.has(v))) push({ kind: 'like', id: `fl-${f.id}`, questionId: q.id, source: 'pool', title: `Katkı · ${title}`, at: null, link });
      }
      for (const o of q.options || []) {
        if (has(o.suggestedByUid) || (!o.suggestedByUid && byName(o.suggestedBy))) {
          push({ kind: 'option', id: `${q.id}-${o.key}`, questionId: q.id, source: 'pool', title: `${o.key}) ${title}`, body: clip(o.text, 400), at: o.createdAt || null, link, weak: !o.suggestedByUid });
        }
        if ((o.likedBy || []).some((v: string) => p.ids.has(v))) push({ kind: 'like', id: `ol-${q.id}-${o.key}`, questionId: q.id, source: 'pool', title: `Şık ${o.key} · ${title}`, at: null, link });
      }
      for (const r of q.reports || []) {
        const strong = has(r.reporterUid, r.reporterEmail);
        if (strong || (!r.reporterUid && !r.reporterEmail && byName(r.reportedBy))) {
          push({ kind: 'report', id: r.id, questionId: q.id, source: 'pool', title: `${clip(r.reason, 80)} · ${title}`, body: clip(r.details, 1500), at: r.timestamp, status: r.status || 'pending', link, weak: !strong });
        }
      }
      if ((q.likedBy || []).some((v: string) => p.ids.has(v))) push({ kind: 'like', id: `ql-${q.id}`, questionId: q.id, source: 'pool', title, at: null, link });
    }
    for (const f of readJson<Any[]>(path.join(deps.dataDir, 'learn_feedback.json'), [])) {
      if (has(f.author?.id) || (!f.author?.id && byName(f.author?.name))) {
        push({ kind: 'report', id: f.id, source: 'learn', title: `${clip(f.field || f.targetLabel, 80)} · ${clip(f.deckTitle, 60)}`, body: clip(f.reason, 1500), at: f.createdAt, status: f.status, link: f.link, weak: !f.author?.id });
      }
      if (Object.keys(f.votes || {}).some((v) => p.ids.has(v))) push({ kind: 'like', id: `lf-${f.id}`, source: 'learn', title: `Öğren bildirimi · ${clip(f.deckTitle, 60)}`, at: null, link: f.link });
    }
    try {
      const lines = fs.readFileSync(path.join(deps.dataDir, 'ornek_soru_bildirimleri.jsonl'), 'utf8').split('\n');
      lines.forEach((l, i) => {
        if (!l.trim()) return;
        try {
          const r = JSON.parse(l);
          if (has(r.reporterUid, r.reporterEmail) || (!r.reporterUid && byName(r.reportedBy))) {
            push({ kind: 'report', id: `ornek-${i}`, source: 'ornek', title: `${clip(r.reason, 80)} · ${r.soru_id}`, body: clip(r.details, 1500), at: r.timestamp, link: notificationLinkFor({ kind: 'ornek_question', id: r.soru_id }), weak: !r.reporterUid });
          }
        } catch {
          /* bozuk satır */
        }
      });
    } catch {
      /* dosya yok */
    }
    const polls = readJson<Any>(path.join(deps.dataDir, 'user_answer_polls.json'), {});
    for (const [qid, v] of Object.entries<Any>(polls)) if (p.ids.has(String(v?.by))) push({ kind: 'vote', id: `poll-${qid}`, source: 'past', title: `Cevap anketi açtı · ${qid}`, at: v.at, link: past(qid) });
    return items;
  };

  /** Öğren ortak katmanı + veritabanındaki oylar/cihazlar/olaylar */
  const dbFacts = async (p: Person, deviceIds: string[] = []) => {
    const ids = [...p.ids];
    const empty = { devices: [] as Any[], usage: [] as Any[], events: [] as Any[], learnNotes: [] as Any[], learnMessages: [] as Any[], answerVotes: [] as Any[] };
    if (!deps.isPgOnline() || !schemaReady) return empty;
    const q = async (sql: string, v: any[]) => {
      try {
        return (await pgDb.query(sql, v)).rows;
      } catch (e: any) {
        console.warn('[Kişiler] sorgu:', e?.message);
        return [];
      }
    };
    const emails = ids.filter((x) => x.includes('@'));
    const devices = await q(
      `select device_id, uid, email, display_name, verified, label, platform, browser, model, first_seen, last_seen, active_seconds, sessions, last_path
         from user_devices where uid = any($1) or lower(email) = any($2) or device_id = any($3) order by last_seen desc limit 50`,
      [ids, emails, deviceIds],
    );
    const devIds = [...new Set([...devices.map((d) => d.device_id), ...deviceIds])];
    const [usage, events, learnNotes, learnMessages, answerVotes] = await Promise.all([
      q(`select day::text as day, sum(active_seconds)::int as seconds from user_usage_daily where uid = any($1) or device_id = any($2) group by day order by day desc limit 120`, [ids, devIds]),
      q(`select id, kind, action, ref, label, body, link, device_id, at from user_events where uid = any($1) or lower(email) = any($2) or device_id = any($3) order by at desc limit 500`, [ids, emails, devIds]),
      q(`select id, deck_id, step_number, kind, body, created_at from learn_notes where author_id = any($1) order by created_at desc limit 200`, [ids]),
      q(`select m.id, m.body, m.created_at, t.deck_id, t.deck_title, t.step_number, t.quote, (t.reporter_id = m.author_id) as is_report
           from learn_thread_messages m join learn_threads t on t.id = m.thread_id where m.author_id = any($1) order by m.created_at desc limit 200`, [ids]),
      q(`select question_id, choice, created_at from answer_votes where voter_uid = any($1) order by created_at desc limit 300`, [ids]),
    ]);
    return { devices, usage, events, learnNotes, learnMessages, answerVotes };
  };

  const scoreSummary = (b: Any | null) => {
    const hist: Any[] = Array.isArray(b?.stats?.selftestHistory) ? b.stats.selftestHistory : [];
    let correct = 0;
    let total = 0;
    let wrong = 0;
    const tests = hist
      .map((h) => {
        const c = Number(h.correct ?? h.correctCount ?? h.score ?? 0) || 0;
        const t = Number(h.total ?? h.totalQuestions ?? h.questionCount ?? (Array.isArray(h.answers) ? h.answers.length : 0)) || 0;
        correct += c;
        total += t;
        const w = Number(h.wrong ?? h.wrongCount ?? 0) || 0;
        wrong += w;
        return {
          id: h.id || null,
          at: h.date || h.at || h.finishedAt || h.createdAt || null,
          correct: c,
          total: t,
          wrong: w,
          blank: Number(h.blank ?? Math.max(0, t - c - w)) || 0,
          durationSec: Number(h.durationSec) || 0,
          title: clip(h.title || h.committeeName || h.committeeId || h.mode || 'Test', 80),
          byDiscipline: h.byDiscipline && typeof h.byDiscipline === 'object' ? h.byDiscipline : {},
        };
      })
      .sort((x, y) => String(y.at || '').localeCompare(String(x.at || '')));
    return {
      tests: tests.slice(0, 100),
      testCount: tests.length,
      correct,
      wrong,
      total,
      net: Math.round((correct - wrong / 4) * 100) / 100,
      accuracy: total ? Math.round((correct / total) * 100) : null,
      answeredAccuracy: correct + wrong ? Math.round((correct / (correct + wrong)) * 100) : null,
    };
  };

  const studySeconds = (b: Any | null) => Object.values<any>(b?.stats?.studySeconds || {}).reduce((a, v) => a + (Number(v) || 0), 0);

  // Liste önbelleği: 4 sn içinde gelen istekler aynı hesaplamayı paylaşır; `people_changed` geçersiz kılar
  let listCache: { at: number; data: Any } | null = null;
  const invalidate = () => {
    listCache = null;
  };

  const buildList = async () => {
    if (listCache && Date.now() - listCache.at < 4000) return listCache.data;
    const ps = people();
    let devices: Any[] = [];
    let usage: Any[] = [];
    let eventCounts: Any[] = [];
    if (deps.isPgOnline() && schemaReady) {
      try {
        devices = (await pgDb.query(`select device_id, uid, lower(email) as email, display_name, verified, label, platform, browser, last_seen, active_seconds from user_devices order by last_seen desc limit 5000`)).rows;
        usage = (await pgDb.query(`select uid, device_id, sum(active_seconds)::int as s from user_usage_daily where day >= (now() at time zone 'Europe/Istanbul')::date - 6 group by uid, device_id`)).rows;
        eventCounts = (await pgDb.query(`select coalesce(uid, lower(email), 'd:' || device_id) as who, kind, count(*)::int as n, max(at) as last from user_events group by 1, 2`)).rows;
      } catch (e: any) {
        console.warn('[Kişiler] liste sorgusu:', e?.message);
      }
    }
    const now = Date.now();
    const claimed = new Set<string>();
    const rows = ps.map((p) => {
      const devs = devices.filter((d) => (d.uid && p.ids.has(d.uid)) || (d.email && p.ids.has(d.email)) || p.devs.has(d.device_id));
      devs.forEach((d) => claimed.add(d.device_id));
      const devSet = new Set(devs.map((d) => d.device_id));
      const week = usage.filter((u) => (u.uid && p.ids.has(u.uid)) || devSet.has(u.device_id)).reduce((a, u) => a + u.s, 0);
      const counts: Record<string, number> = {};
      let lastEvent = '';
      for (const e of eventCounts) {
        if (!p.ids.has(e.who) && !devSet.has(String(e.who).replace(/^d:/, ''))) continue;
        counts[e.kind] = (counts[e.kind] || 0) + e.n;
        const l = new Date(e.last).toISOString();
        if (l > lastEvent) lastEvent = l;
      }
      const c = contributions(p);
      const cnt = (k: string) => c.filter((x) => x.kind === k).length;
      const lastSeen = [devs[0]?.last_seen ? new Date(devs[0].last_seen).toISOString() : '', sinceIso(p.backup), p.lastLoginAt || '', lastEvent].sort().pop() || null;
      const score = scoreSummary(p.backup);
      return {
        key: p.key,
        kind: p.kind,
        uid: p.uid,
        email: p.email,
        name: p.name,
        studentNumber: p.studentNumber,
        phone: p.phone,
        role: p.role,
        photoURL: p.photoURL,
        createdAt: p.createdAt,
        lastSeen,
        online: devs.some((d) => now - new Date(d.last_seen).getTime() < 150_000),
        deviceCount: devs.length,
        deviceNames: devs.slice(0, 4).map((d) => d.label),
        totalSeconds: devs.reduce((a, d) => a + Number(d.active_seconds || 0), 0) || studySeconds(p.backup),
        weekSeconds: week,
        accuracy: score.accuracy,
        testCount: score.testCount,
        counts: {
          comment: cnt('comment'),
          report: cnt('report'),
          question: cnt('question'),
          fragment: cnt('fragment'),
          option: cnt('option'),
          like: cnt('like'),
          note: (Array.isArray(p.backup?.notes) ? p.backup.notes.length : 0) + (counts.note || 0),
          events: Object.values(counts).reduce((a, n) => a + n, 0),
        },
      };
    });
    // Hiçbir hesaba/yedeğe bağlanmamış cihazlar: misafir satırı
    for (const d of devices) {
      if (claimed.has(d.device_id) || d.uid) continue;
      const counts: Record<string, number> = {};
      for (const e of eventCounts) if (e.who === `d:${d.device_id}`) counts[e.kind] = (counts[e.kind] || 0) + e.n;
      rows.push({
        key: `d:${d.device_id}`,
        kind: 'guest',
        uid: null,
        email: null,
        name: d.display_name || 'Misafir cihaz',
        studentNumber: null,
        phone: null,
        role: 'guest',
        photoURL: null,
        createdAt: null,
        lastSeen: new Date(d.last_seen).toISOString(),
        online: now - new Date(d.last_seen).getTime() < 150_000,
        deviceCount: 1,
        deviceNames: [d.label],
        totalSeconds: Number(d.active_seconds || 0),
        weekSeconds: usage.filter((u) => u.device_id === d.device_id).reduce((a, u) => a + u.s, 0),
        accuracy: null,
        testCount: 0,
        counts: { comment: counts.comment || 0, report: counts.report || 0, question: counts.question || 0, fragment: counts.fragment || 0, option: counts.option || 0, like: counts.like || 0, note: counts.note || 0, events: Object.values(counts).reduce((a, n) => a + n, 0) },
      });
    }
    // Günlükte olup hiçbir kişiye bağlanamayan kimlikler (kayıtsız uid / cihaz kaydı olmayan istemci) da görünür kalsın
    const known = new Set<string>();
    for (const p of ps) for (const id of p.ids) known.add(id);
    for (const d of devices) known.add(`d:${d.device_id}`);
    const orphan = new Map<string, { counts: Record<string, number>; last: string }>();
    for (const e of eventCounts) {
      const who = String(e.who);
      if (known.has(who) || ps.some((p) => p.devs.has(who.replace(/^d:/, '')))) continue;
      const o = orphan.get(who) || { counts: {}, last: '' };
      o.counts[e.kind] = (o.counts[e.kind] || 0) + e.n;
      const l = new Date(e.last).toISOString();
      if (l > o.last) o.last = l;
      orphan.set(who, o);
    }
    for (const [who, o] of orphan) {
      const c = o.counts;
      rows.push({
        key: `x:${who}`, kind: 'guest', uid: who.startsWith('d:') ? null : who, email: who.includes('@') ? who : null,
        name: who.startsWith('d:') ? 'Kayıtsız cihaz' : 'Kayıtsız kimlik', studentNumber: null, phone: null, role: 'guest', photoURL: null,
        createdAt: null, lastSeen: o.last, online: false, deviceCount: 0, deviceNames: [], totalSeconds: 0, weekSeconds: 0, accuracy: null, testCount: 0,
        counts: { comment: c.comment || 0, report: c.report || 0, question: c.question || 0, fragment: c.fragment || 0, option: c.option || 0, like: c.like || 0, note: c.note || 0, events: Object.values(c).reduce((a, n) => a + n, 0) },
      });
    }
    rows.sort((a, b) => Number(b.online) - Number(a.online) || String(b.lastSeen || '').localeCompare(String(a.lastSeen || '')));
    const data = {
      people: rows,
      totals: {
        people: rows.length,
        accounts: rows.filter((r) => r.kind === 'account').length,
        online: rows.filter((r) => r.online).length,
        devices: devices.length,
        weekSeconds: usage.reduce((a, u) => a + u.s, 0),
        openReports: rows.reduce((a, r) => a + r.counts.report, 0),
      },
      database: deps.isPgOnline() && schemaReady,
      at: new Date().toISOString(),
    };
    listCache = { at: Date.now(), data };
    return data;
  };

  const buildDetail = async (key: string) => {
    const ps = people();
    // Derin bağlantı: anahtar (u:/g:/d:), çıplak uid ya da e-posta
    const bare = lc(key.replace(/^u:/, ''));
    let p = ps.find((x) => x.key === key) || ps.find((x) => x.ids.has(key.replace(/^u:/, '')) || x.ids.has(bare)) || null;
    let deviceIds: string[] = [];
    if (!p && key.startsWith('x:')) {
      const who = key.slice(2);
      const dev = who.startsWith('d:') ? who.slice(2) : '';
      if (dev) deviceIds = [dev];
      p = { key, kind: 'guest', uid: dev ? null : who, email: who.includes('@') ? who : null, name: dev ? 'Kayıtsız cihaz' : 'Kayıtsız kimlik', studentNumber: null, phone: null, role: 'guest', photoURL: null, createdAt: null, lastLoginAt: null, ids: new Set(dev ? [] : [who]), names: new Set(), devs: new Set(dev ? [dev] : []), backup: null };
    }
    if (!p && key.startsWith('d:')) {
      const id = key.slice(2);
      deviceIds = [id];
      p = { key, kind: 'guest', uid: null, email: null, name: 'Misafir cihaz', studentNumber: null, phone: null, role: 'guest', photoURL: null, createdAt: null, lastLoginAt: null, ids: new Set(), names: new Set(), devs: new Set([id]), backup: null };
    }
    if (!p) return null;
    const facts = await dbFacts(p, [...new Set([...deviceIds, ...p.devs])]);
    if (key.startsWith('d:') && facts.devices[0]?.display_name) p.name = facts.devices[0].display_name;
    const b = p.backup;
    const items = contributions(p);
    for (const n of facts.learnNotes) items.push({ kind: 'note', id: n.id, source: 'learn', title: `Öğren notu (${n.kind}) · adım ${n.step_number}`, body: clip(n.body, 1500), at: n.created_at, link: notificationLinkFor({ kind: 'deck', id: n.deck_id, slideNumber: n.step_number }), deckId: n.deck_id });
    for (const m of facts.learnMessages)
      items.push({ kind: m.is_report ? 'report' : 'comment', id: m.id, source: 'learn', title: `${m.is_report ? 'Metin bildirimi' : 'Tartışma'} · ${clip(m.deck_title, 60)} · adım ${m.step_number}`, body: clip(m.is_report ? `“${clip(m.quote, 200)}” — ${m.body}` : m.body, 1500), at: m.created_at, link: notificationLinkFor({ kind: 'deck', id: m.deck_id, slideNumber: m.step_number }), messageId: m.id });
    const pastTitle = new Map<string, string>();
    if (facts.answerVotes.length) for (const q of deps.getPastQuestions()) pastTitle.set(String(q.id), clip(q.topic || q.discipline || q.stem || '', 70));
    for (const v of facts.answerVotes)
      items.push({ kind: 'vote', id: `av-${v.question_id}`, source: 'past', title: `Cevap oyu: ${v.choice} · ${pastTitle.get(v.question_id) || v.question_id}`, at: v.created_at, link: past(v.question_id) });
    for (const n of Array.isArray(b?.notes) ? b.notes : []) {
      items.push({ kind: 'note', id: n.id, source: 'notebook', title: clip(n.title || n.questionTopic || n.contextLabel || 'Kişisel not', 90), body: clip(n.text || n.content || n.body, 1500), at: n.updatedAt || n.createdAt, link: n.questionId ? past(n.questionId) : n.link || '' });
    }
    items.sort((x, y) => String(y.at || '').localeCompare(String(x.at || '')));
    const activityLog = (Array.isArray(b?.stats?.activityLog) ? b.stats.activityLog : []).slice(-200).reverse();
    const kvCount = Object.keys(b?.kv || {}).length;
    const totalSeconds = facts.devices.reduce((a, d) => a + Number(d.active_seconds || 0), 0);
    return {
      person: {
        key: p.key,
        kind: p.kind,
        uid: p.uid,
        email: p.email,
        name: p.name,
        studentNumber: p.studentNumber,
        phone: p.phone,
        role: p.role,
        photoURL: p.photoURL,
        createdAt: p.createdAt,
        lastLoginAt: p.lastLoginAt,
        lastBackupAt: b?.serverSavedAt || null,
        verified: !!b?.verified || p.kind === 'account',
      },
      devices: facts.devices.map((d) => ({ ...d, online: Date.now() - new Date(d.last_seen).getTime() < 150_000 })),
      usage: {
        totalSeconds: totalSeconds || studySeconds(b),
        studySeconds: studySeconds(b),
        daily: facts.usage,
        // Uygulamanın kendi çalışma sayacı (gün → sn); cihaz kaydı öncesi geçmişi de kapsar
        studyDaily: Object.entries<any>(b?.stats?.studySeconds || {})
          .map(([day, sec]) => ({ day, seconds: Number(sec) || 0 }))
          .sort((x, y) => y.day.localeCompare(x.day))
          .slice(0, 120),
        sessions: facts.devices.reduce((a, d) => a + Number(d.sessions || 0), 0),
      },
      score: scoreSummary(b),
      study: {
        progress: Object.keys(b?.stats?.studyProgress || {}).length,
        review: Object.keys(b?.stats?.studyReview || {}).length,
        favorites: (b?.stats?.favorites || []).length,
        flashcards: Array.isArray(b?.stats?.flashcards) ? b.stats.flashcards.length : Object.keys(b?.stats?.flashcards || {}).length,
        kvCount,
      },
      activityLog,
      events: facts.events,
      items,
      notifications: (Array.isArray(b?.notifications) ? b.notifications : []).slice(0, 100),
      at: new Date().toISOString(),
    };
  };

  /* ---------------- Yerel panel → Oracle vekili ---------------- */
  const proxyToOracle = async (req: express.Request, res: express.Response) => {
    const secret = panelSecret();
    if (!secret) return res.status(503).json({ error: 'MEDS_PANEL_SECRET tanımlı değil; canlı kişi verisine yerelden ulaşılamıyor.' });
    try {
      const r = await fetch(`${deps.oracleApiUrl.replace(/\/$/, '')}${req.originalUrl}`, {
        method: req.method,
        headers: { 'content-type': 'application/json', 'x-panel-secret': secret, 'x-admin-email': deps.adminEmail },
        body: req.method === 'GET' ? undefined : JSON.stringify(req.body || {}),
      });
      res.status(r.status).type(r.headers.get('content-type') || 'application/json').send(Buffer.from(await r.arrayBuffer()));
    } catch (e: any) {
      res.status(502).json({ error: `Oracle'a ulaşılamadı: ${e?.message || e}` });
    }
  };

  const guard = async (req: express.Request, res: express.Response): Promise<boolean> => {
    if (!(await isStrongAdmin(req, deps.adminEmail))) {
      res.status(403).json({ error: 'Kişisel verilere yalnız doğrulanmış yönetici oturumu erişebilir. Lütfen yönetici hesabıyla giriş yapın.' });
      return false;
    }
    if (req.headers['x-panel-target'] === 'oracle' && isLoopback(req)) {
      await proxyToOracle(req, res);
      return false;
    }
    return true;
  };

  app.get('/api/admin/people', async (req, res) => {
    if (!(await guard(req, res))) return;
    try {
      res.setHeader('Cache-Control', 'no-store');
      res.json(await buildList());
    } catch (e: any) {
      res.status(500).json({ error: e?.message || String(e) });
    }
  });

  app.get('/api/admin/people/:key', async (req, res) => {
    if (!(await guard(req, res))) return;
    try {
      const d = await buildDetail(String(req.params.key));
      if (!d) return res.status(404).json({ error: 'Kişi bulunamadı.' });
      res.setHeader('Cache-Control', 'no-store');
      res.json(d);
    } catch (e: any) {
      res.status(500).json({ error: e?.message || String(e) });
    }
  });

  // Cihazı unut: cihaz satırı ve günlük kullanımı silinir (olay günlüğü kalır)
  app.delete('/api/admin/people/devices/:deviceId', async (req, res) => {
    if (!(await guard(req, res))) return;
    const id = String(req.params.deviceId);
    if (!DEVICE_RE.test(id)) return res.status(400).json({ error: 'Cihaz kimliği geçersiz.' });
    try {
      await pgDb.query('delete from user_usage_daily where device_id = $1', [id]);
      await pgDb.query('delete from user_devices where device_id = $1', [id]);
      deviceOwner.delete(id);
      invalidate();
      res.json({ success: true });
    } catch (e: any) {
      res.status(500).json({ error: e?.message || String(e) });
    }
  });

  // Olay günlüğünden tek kayıt sil
  app.delete('/api/admin/people/events/:id', async (req, res) => {
    if (!(await guard(req, res))) return;
    try {
      await pgDb.query('delete from user_events where id = $1', [Number(req.params.id) || 0]);
      invalidate();
      res.json({ success: true });
    } catch (e: any) {
      res.status(500).json({ error: e?.message || String(e) });
    }
  });

  return {
    invalidate,
    /** Hub: user_devices / user_events değişikliği → yalnız yöneticilere tek özet olay */
    onDbChanges(table: string, changes: { op: string; id: string | null; c?: string | null; q?: string | null }[]) {
      invalidate();
      deps.broadcastAdmin('people_changed', {
        table,
        uids: [...new Set(changes.map((c) => c.c).filter(Boolean))].slice(0, 50),
        kinds: [...new Set(changes.map((c) => c.q).filter(Boolean))].slice(0, 20),
        count: changes.length,
        at: Date.now(),
      });
    },
    /** Profil yedeği kaydedildi (skor, etkinlik, notlar değişti) */
    onProfileSaved(uid: string) {
      invalidate();
      deps.broadcastAdmin('people_changed', { table: 'user_data', uids: [uid], at: Date.now() });
    },
    backupFile,
  };
}
