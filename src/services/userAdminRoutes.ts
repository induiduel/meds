/**
 * Yönetim › Kullanıcılar: rol değiştirme ve hesap askıya alma.
 *
 * Veri modeli (data/users.json kaydı; meds-pg `users` yansıması isteğe bağlı):
 *   role: 'student' | 'moderator' | 'admin'
 *   suspension?: { active: boolean; reason: string; until: string | null; by: string; at: string; liftedAt?: string; liftedBy?: string }
 *   accessHistory?: { at; by; kind: 'role' | 'suspend' | 'unsuspend'; from?; to?; reason?; until? }[]  (yalnız eklenir)
 *
 * Rol anlamı: 'admin' ve 'moderator' bu dosyada yalnız kayıt + gösterim içindir; güçlü yönetici yetkisi hâlâ yalnız
 * ana yöneticidedir (isStrongAdmin). Moderatör hiçbir yönetici ucuna erişim kazanmaz (ileride dar izinler eklenebilir).
 *
 * Askı uygulaması: aynı dosyadaki ara katman, askıdaki uid/e-postadan gelen tüm öğrenci yazma isteklerini (GET dışı
 * /api/*) 403 + code 'ACCOUNT_SUSPENDED' ile reddeder. Ana yönetici rolü değiştirilemez, askıya alınamaz.
 * Hiçbir kullanıcı verisi silinmez.
 */
import express from 'express';
import { isLoopback, isStrongAdmin } from './peopleInsights';
import { requestUser } from './firebaseIdentity';

type Any = Record<string, any>;
export type UserRole = 'student' | 'moderator' | 'admin';
const ROLES: UserRole[] = ['student', 'moderator', 'admin'];

export interface UserAdminDeps {
  adminEmail: string;
  loadUsers: () => Any[];
  saveUsers: (users: Any[]) => void;
  /** meds-pg users tablosuna yansıtma (isteğe bağlı) */
  mirrorUser?: (user: Any) => Promise<unknown> | unknown;
  broadcastAdmin?: (event: string, data: Any) => void;
  oracleApiUrl?: string;
}

const lc = (v: unknown) => String(v ?? '').trim().toLowerCase();
const clip = (v: unknown, n: number) => String(v ?? '').replace(/\s+/g, ' ').trim().slice(0, n);

export const SUSPENDED_CODE = 'ACCOUNT_SUSPENDED';

/** Askı hâlâ geçerli mi (bitiş tarihi geçtiyse geçersiz; kayıt silinmez) */
export function suspensionActive(s: Any | undefined | null, now = Date.now()): boolean {
  if (!s || !s.active) return false;
  if (s.until) {
    const t = Date.parse(s.until);
    if (Number.isFinite(t) && t <= now) return false;
  }
  return true;
}

/** Yazma isteğinde askı denetimi yapılmayan yollar */
const EXEMPT = [/^\/api\/admin\//, /^\/api\/users\/sync$/, /^\/api\/presence$/, /^\/api\/me\/access$/];

export function registerUserAdminRoutes(app: express.Express, deps: UserAdminDeps) {
  const owner = lc(deps.adminEmail);

  /* ---------- Askı önbelleği (users.json her istekte okunmasın) ---------- */
  let cache: { at: number; byUid: Map<string, Any>; byEmail: Map<string, Any> } | null = null;
  const refresh = () => {
    const byUid = new Map<string, Any>();
    const byEmail = new Map<string, Any>();
    try {
      for (const u of deps.loadUsers() || []) {
        if (!suspensionActive(u?.suspension) || lc(u.email) === owner) continue;
        if (u.uid) byUid.set(String(u.uid), u);
        if (u.email) byEmail.set(lc(u.email), u);
      }
    } catch (e: any) {
      console.warn('[Kullanıcı erişimi] kullanıcılar okunamadı:', e?.message);
    }
    cache = { at: Date.now(), byUid, byEmail };
    return cache;
  };
  const suspended = () => (cache && Date.now() - cache.at < 15_000 ? cache : refresh());
  const invalidate = () => {
    cache = null;
  };

  const suspendedBody = (u: Any) => ({
    error: `Hesabınız askıya alındı${u.suspension?.until ? ` (${new Date(u.suspension.until).toLocaleDateString('tr-TR')} tarihine kadar)` : ''}. Bu süre içinde içerik gönderemez ve değişiklik yapamazsınız. Gerekçe: ${u.suspension?.reason || 'belirtilmedi'}`,
    code: SUSPENDED_CODE,
    reason: u.suspension?.reason || '',
    until: u.suspension?.until || null,
  });

  /* ---------- Ara katman: askıdaki hesabın yazma isteklerini reddet ---------- */
  app.use(async (req, res, next) => {
    try {
      if (req.method === 'GET' || req.method === 'HEAD' || req.method === 'OPTIONS') return next();
      const p = String(req.path || '');
      if (!p.startsWith('/api/') || EXEMPT.some((re) => re.test(p))) return next();
      const c = suspended();
      if (!c.byUid.size && !c.byEmail.size) return next();

      const b: Any = req.body && typeof req.body === 'object' ? req.body : {};
      const uids = new Set<string>();
      const emails = new Set<string>();
      for (const v of [b.uid, b.userId, b.authorUid, b.reporterUid, b.voterId, b.author?.id, req.headers['x-user-id'], req.headers['x-voter-uid']]) {
        const s = clip(v, 128);
        if (s) uids.add(s);
      }
      for (const v of [b.email, b.authorEmail, b.reporterEmail, b.author?.email]) {
        const s = lc(v);
        if (s) emails.add(s);
      }
      if (req.headers.authorization) {
        try {
          const who = await requestUser(req);
          if (who.user) {
            uids.add(who.user.uid);
            if (who.user.email) emails.add(lc(who.user.email));
          }
        } catch {
          /* jeton doğrulanamadı */
        }
      }
      let hit: Any | undefined;
      for (const u of uids) if ((hit = c.byUid.get(u))) break;
      if (!hit) for (const e of emails) if ((hit = c.byEmail.get(e))) break;
      if (!hit) return next();
      // Ana yöneticinin askıdaki kişi adına yaptığı düzeltmeler engellenmez
      if (await isStrongAdmin(req, deps.adminEmail)) return next();
      return res.status(403).json(suspendedBody(hit));
    } catch {
      return next();
    }
  });

  /* ---------- Öğrencinin kendi durumu ---------- */
  app.get('/api/me/access', async (req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    try {
      const who = await requestUser(req);
      if (!who.user) return res.json({ role: 'student', suspended: false });
      const u = (deps.loadUsers() || []).find((x) => x.uid === who.user!.uid || (who.user!.email && lc(x.email) === lc(who.user!.email)));
      const active = !!u && lc(u.email) !== owner && suspensionActive(u.suspension);
      res.json({
        role: lc(who.user.email) === owner ? 'admin' : u?.role || 'student',
        suspended: active,
        ...(active ? { reason: u!.suspension.reason || '', until: u!.suspension.until || null } : {}),
      });
    } catch (e: any) {
      res.status(500).json({ error: e?.message || String(e) });
    }
  });

  /* ---------- Yönetici uçları (yalnız güçlü yönetici; yerel panel → Oracle vekili) ---------- */
  const proxyToOracle = async (req: express.Request, res: express.Response) => {
    const secret = String(process.env.MEDS_PANEL_SECRET || '').trim();
    if (!secret || !deps.oracleApiUrl) return res.status(503).json({ error: 'MEDS_PANEL_SECRET tanımlı değil; canlı sunucuya yerelden ulaşılamıyor.' });
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
      res.status(403).json({ error: 'Rol ve askı işlemlerini yalnız doğrulanmış ana yönetici yapabilir.' });
      return false;
    }
    if (req.headers['x-panel-target'] === 'oracle' && isLoopback(req)) {
      await proxyToOracle(req, res);
      return false;
    }
    res.setHeader('Cache-Control', 'no-store');
    return true;
  };
  const actorEmail = (req: express.Request) => lc(req.headers['x-admin-email']) || owner;
  const view = (u: Any) => ({
    uid: u.uid,
    email: u.email || '',
    displayName: u.displayName || '',
    role: lc(u.email) === owner ? 'admin' : ROLES.includes(u.role) ? u.role : 'student',
    isOwner: lc(u.email) === owner,
    suspended: lc(u.email) !== owner && suspensionActive(u.suspension),
    suspension: u.suspension || null,
    accessHistory: Array.isArray(u.accessHistory) ? u.accessHistory.slice(-20) : [],
  });
  const targetUids = (body: Any): string[] =>
    Array.from(new Set((Array.isArray(body?.uids) ? body.uids : [body?.uid]).map((x: unknown) => clip(x, 128)).filter(Boolean))) as string[];

  /** Ortak güncelleme: seçili kayıtları değiştirir, atlananları gerekçesiyle döndürür */
  const apply = (req: express.Request, res: express.Response, fn: (u: Any, now: string) => string | null) => {
    const uids = targetUids(req.body);
    if (!uids.length) return res.status(400).json({ error: 'En az bir kullanıcı seçin.' });
    if (uids.length > 500) return res.status(400).json({ error: 'Tek seferde en çok 500 kullanıcı güncellenebilir.' });
    const users = deps.loadUsers() || [];
    const now = new Date().toISOString();
    const changed: Any[] = [];
    const skipped: { uid: string; reason: string }[] = [];
    for (const uid of uids) {
      const idx = users.findIndex((u) => u.uid === uid);
      if (idx === -1) {
        skipped.push({ uid, reason: 'Kullanıcı bulunamadı.' });
        continue;
      }
      if (lc(users[idx].email) === owner) {
        skipped.push({ uid, reason: 'Ana yönetici hesabı değiştirilemez.' });
        continue;
      }
      const u = { ...users[idx] };
      const why = fn(u, now);
      if (why) {
        skipped.push({ uid, reason: why });
        continue;
      }
      u.updatedAt = now;
      users[idx] = u;
      changed.push(u);
    }
    if (changed.length) {
      deps.saveUsers(users);
      invalidate();
      for (const u of changed) {
        try {
          void Promise.resolve(deps.mirrorUser?.(u)).catch(() => {});
        } catch {
          /* yansıtma isteğe bağlı */
        }
      }
      deps.broadcastAdmin?.('people_changed', { table: 'users', uids: changed.map((u) => u.uid), at: Date.now() });
    }
    res.json({ success: true, changed: changed.map(view), skipped });
  };
  const pushHistory = (u: Any, entry: Any) => {
    u.accessHistory = [...(Array.isArray(u.accessHistory) ? u.accessHistory : []), entry].slice(-100);
  };

  app.get('/api/admin/people-access', async (req, res) => {
    if (!(await guard(req, res))) return;
    try {
      res.json({ users: (deps.loadUsers() || []).map(view), roles: ROLES });
    } catch (e: any) {
      res.status(500).json({ error: e?.message || String(e) });
    }
  });

  app.post('/api/admin/people-access/role', async (req, res) => {
    if (!(await guard(req, res))) return;
    const role = String(req.body?.role || '') as UserRole;
    if (!ROLES.includes(role)) return res.status(400).json({ error: 'Geçersiz rol. Öğrenci, moderatör ya da yönetici seçin.' });
    const by = actorEmail(req);
    apply(req, res, (u, now) => {
      const from = ROLES.includes(u.role) ? u.role : 'student';
      if (from === role) return 'Rol zaten bu.';
      u.role = role;
      pushHistory(u, { at: now, by, kind: 'role', from, to: role });
      return null;
    });
  });

  app.post('/api/admin/people-access/suspend', async (req, res) => {
    if (!(await guard(req, res))) return;
    const reason = clip(req.body?.reason, 500);
    if (reason.length < 3) return res.status(400).json({ error: 'Askıya alma gerekçesi yazılmalı.' });
    let until: string | null = null;
    if (req.body?.until) {
      const t = Date.parse(String(req.body.until));
      if (!Number.isFinite(t)) return res.status(400).json({ error: 'Bitiş tarihi geçersiz.' });
      if (t <= Date.now()) return res.status(400).json({ error: 'Bitiş tarihi ileri bir tarih olmalı.' });
      until = new Date(t).toISOString();
    }
    const by = actorEmail(req);
    apply(req, res, (u, now) => {
      u.suspension = { active: true, reason, until, by, at: now };
      pushHistory(u, { at: now, by, kind: 'suspend', reason, until });
      return null;
    });
  });

  app.post('/api/admin/people-access/unsuspend', async (req, res) => {
    if (!(await guard(req, res))) return;
    const by = actorEmail(req);
    apply(req, res, (u, now) => {
      if (!u.suspension?.active) return 'Hesap zaten askıda değil.';
      u.suspension = { ...u.suspension, active: false, liftedAt: now, liftedBy: by };
      pushHistory(u, { at: now, by, kind: 'unsuspend' });
      return null;
    });
  });

  return { invalidate, isSuspended: (uid: string) => suspended().byUid.has(uid) };
}
