/**
 * Öğrenci Web Push (site kapalıyken bildirim).
 *  - VAPID anahtarı yönetici push'uyla ortak (`web_push_keys.json`; webpush.setVapidDetails ServerNotificationService'te).
 *  - Abonelikler `user_push_subscriptions.json`: { uid → [{endpoint, keys, ua, at}] }; cihaz başına tek kayıt (endpoint).
 *  - Kimlik: Firebase ID jetonu (requestUser) ya da gizli cihaz jetonu (`dev-…`), profil yedeğiyle aynı kural.
 *  - notifyStudent → pushToUser: profil bildirimine yazılan her olay ayrıca telefona düşer. 404/410 abonelik silinir.
 */
import fs from 'fs';
import path from 'path';
import type express from 'express';
import webpush from 'web-push';
import { requestUser } from './firebaseIdentity';

const DEVICE_TOKEN_RE = /^dev-[a-z0-9-]{16,64}$/i;
const MAX_PER_USER = 8;

interface Sub { endpoint: string; keys: { p256dh: string; auth: string }; ua?: string; at: string }

export function registerUserPushRoutes(app: express.Express, deps: { dataDir: string; getPublicKey: () => string | null }) {
  const file = path.join(deps.dataDir, 'user_push_subscriptions.json');
  let cache: Record<string, Sub[]> | null = null;
  const load = (): Record<string, Sub[]> => {
    if (cache) return cache;
    try { cache = fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) || {} : {}; } catch { cache = {}; }
    return cache!;
  };
  const save = () => {
    const tmp = `${file}.${process.pid}.tmp`;
    fs.writeFileSync(tmp, JSON.stringify(cache || {}));
    fs.renameSync(tmp, file);
  };

  async function who(req: express.Request): Promise<string | null> {
    const u = await requestUser(req);
    if (u.user) return u.user.uid;
    if (u.invalid) return null;
    const dev = String(req.body?.deviceId || req.headers['x-user-id'] || '');
    return DEVICE_TOKEN_RE.test(dev) ? dev : null;
  }

  app.get('/api/push/vapid-public-key', (_req, res) => {
    const key = deps.getPublicKey();
    if (!key) return res.status(503).json({ error: 'Bildirim anahtarı hazır değil.' });
    res.set('Cache-Control', 'public, max-age=3600').json({ publicKey: key });
  });

  app.post('/api/push/subscribe', async (req, res) => {
    const uid = await who(req);
    if (!uid) return res.status(401).json({ error: 'Bildirim için oturum gerekli.' });
    const s = req.body?.subscription;
    if (!s?.endpoint || !s?.keys?.p256dh || !s?.keys?.auth || !/^https:\/\//.test(s.endpoint) || s.endpoint.length > 1000) {
      return res.status(400).json({ error: 'Geçersiz abonelik.' });
    }
    const all = load();
    // Aynı cihaz başka hesapta kayıtlıysa oradan düşer (hesap değişimi)
    for (const k of Object.keys(all)) {
      all[k] = all[k].filter((x) => x.endpoint !== s.endpoint);
      if (!all[k].length) delete all[k];
    }
    const list = all[uid] || [];
    list.unshift({ endpoint: s.endpoint, keys: { p256dh: s.keys.p256dh, auth: s.keys.auth }, ua: String(req.headers['user-agent'] || '').slice(0, 160), at: new Date().toISOString() });
    all[uid] = list.slice(0, MAX_PER_USER);
    save();
    res.json({ ok: true });
  });

  app.post('/api/push/unsubscribe', (req, res) => {
    const endpoint = String(req.body?.endpoint || '');
    if (!endpoint) return res.status(400).json({ error: 'endpoint gerekli' });
    const all = load();
    let n = 0;
    for (const k of Object.keys(all)) {
      const before = all[k].length;
      all[k] = all[k].filter((x) => x.endpoint !== endpoint);
      n += before - all[k].length;
      if (!all[k].length) delete all[k];
    }
    if (n) save();
    res.json({ ok: true, removed: n });
  });

  /** Kullanıcının tüm cihazlarına push. Abonelik yoksa sessizce 0. */
  async function pushToUser(uid: string, p: { title: string; body: string; url?: string; tag?: string }): Promise<number> {
    const all = load();
    const list = all[uid];
    if (!uid || !list?.length || !deps.getPublicKey()) return 0;
    const payload = JSON.stringify({
      title: p.title.slice(0, 120),
      body: p.body.slice(0, 300),
      tag: p.tag || `medsor-${Date.now()}`,
      student: true,
      data: { url: p.url || '/' },
    });
    let sent = 0;
    const keep: Sub[] = [];
    for (const s of list) {
      try {
        await webpush.sendNotification({ endpoint: s.endpoint, keys: s.keys }, payload, { TTL: 60 * 60 * 24 * 3, urgency: 'normal' });
        sent++;
        keep.push(s);
      } catch (e: any) {
        if (e?.statusCode !== 404 && e?.statusCode !== 410) keep.push(s);
      }
    }
    if (keep.length !== list.length) {
      if (keep.length) all[uid] = keep; else delete all[uid];
      save();
    }
    return sent;
  }

  return { pushToUser };
}
