/**
 * Kullanıcı Veri Yedekleme ve Senkronizasyon Sunucu Servisi
 * (User Data Backup & Database Synchronization Server Service)
 *
 * Görevleri:
 * 1. POST /api/user-data/backup:
 *    - İstemciden gelen istatistikler, deneme sınavları, çalışma süreleri, bildirimler, notlar,
 *      favoriler ve profil verilerini alır.
 *    - data/user_backups/<sha256(id)>.json dosyasına atomik olarak yazar.
 *    - data/users.json içindeki ilgili kullanıcı kaydını günceller (lastBackupAt, backupStats).
 *    - mirrorUserToDb aracılığıyla meds-pg (Postgres) veritabanındaki `users` tablosuna
 *      (JSONB `data` sütunu) tam yedeği ve özetleri yansıtır.
 * 2. GET /api/user-data/backup:
 *    - Belirtilen kullanıcı (uid, email veya x-user-id) için diskteki ve veritabanındaki en güncel yedeği çeker.
 * Kimlik: giriş yapmış kullanıcı `Authorization: Bearer <Firebase ID token>` gönderir; sunucu jetonu Firebase'e
 * doğrulatır ve uid/e-postayı oradan alır (gövdedeki uid/email'e güvenilmez). Girişsiz kullanıcı yalnız kendi gizli
 * cihaz jetonuyla (`dev-<uuid>`) yedekler. Böylece başkasının uid'si ya da e-postası yazılarak yedeği ezilemez/okunamaz.
 * 3. GET /api/user-data/my-comments:
 *    - Soru veritabanında (pastQuestions.json) kullanıcının (uid, email veya rumuz/author)
 *      yaptığı tüm yorumları tarar ve soru başlıkları/detaylarıyla listeler.
 */

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import type express from 'express';

export interface UserDataBackupDeps {
  dataDir: string;
  loadUsers: () => any[];
  saveUsers: (users: any[]) => void;
  mirrorUserToDb: (user: any) => Promise<void>;
  getPastQuestions: () => any[];
  /** Firebase web API anahtarı (herkese açık); ID jetonunu accounts:lookup ile doğrulamak için. */
  firebaseApiKey?: string;
}

type Identity = { uid: string; email: string; verified: boolean };

// Cihaz jetonu: src/utils/voterId.ts → `dev-<uuid>` (ya da eski tarayıcılarda `dev-<zaman>-<rastgele>`)
const DEVICE_TOKEN_RE = /^dev-[a-z0-9-]{16,64}$/i;

export function registerUserDataBackupRoutes(app: express.Express, deps: UserDataBackupDeps) {
  const backupsDir = path.join(deps.dataDir, 'user_backups');
  if (!fs.existsSync(backupsDir)) {
    fs.mkdirSync(backupsDir, { recursive: true });
  }

  // Doğrulanmış jetonlar kısa süre önbellekte (her yedekte Firebase'e gidilmesin)
  const tokenCache = new Map<string, { uid: string; email: string; exp: number }>();
  async function verifyIdToken(token: string): Promise<{ uid: string; email: string } | null> {
    if (!token || !deps.firebaseApiKey) return null;
    const key = crypto.createHash('sha256').update(token).digest('hex');
    const hit = tokenCache.get(key);
    if (hit && hit.exp > Date.now()) return { uid: hit.uid, email: hit.email };
    try {
      const r = await fetch(`https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=${encodeURIComponent(deps.firebaseApiKey)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idToken: token }),
        signal: AbortSignal.timeout(5000),
      });
      if (!r.ok) return null;
      const u = (await r.json())?.users?.[0];
      if (!u?.localId) return null;
      const out = { uid: String(u.localId), email: String(u.email || '').toLowerCase() };
      if (tokenCache.size > 2000) tokenCache.clear();
      tokenCache.set(key, { ...out, exp: Date.now() + 10 * 60 * 1000 });
      return out;
    } catch {
      return null;
    }
  }

  /** İstek sahibinin kimliği; geçersizse null ve hata iletisi. */
  async function resolveIdentity(req: express.Request, claimedUid: string): Promise<{ id?: Identity; error?: string; status?: number }> {
    const auth = String(req.headers.authorization || '');
    const token = auth.toLowerCase().startsWith('bearer ') ? auth.slice(7).trim() : '';
    if (token) {
      const v = await verifyIdToken(token);
      if (!v) return { error: 'Oturum doğrulanamadı; lütfen yeniden giriş yapın.', status: 401 };
      return { id: { uid: v.uid, email: v.email, verified: true } };
    }
    if (DEVICE_TOKEN_RE.test(claimedUid)) return { id: { uid: claimedUid, email: '', verified: false } };
    return { error: 'Bu hesabın yedeği için giriş yapılmalıdır.', status: 401 };
  }

  // Basit hız sınırı (IP başına dakikada 20 yazma)
  const writeRate = new Map<string, { n: number; at: number }>();
  const rateLimited = (req: express.Request) => {
    const ip = String(req.headers['cf-connecting-ip'] || req.ip || '');
    const now = Date.now();
    const r = writeRate.get(ip);
    if (!r || now - r.at > 60_000) {
      if (writeRate.size > 5000) writeRate.clear();
      writeRate.set(ip, { n: 1, at: now });
      return false;
    }
    return ++r.n > 20;
  };

  const readBackup = (file: string): any | null => {
    try {
      return fs.existsSync(file) ? JSON.parse(fs.readFileSync(file, 'utf8')) : null;
    } catch {
      return null;
    }
  };

  const getBackupFilePath = (id: string): string => {
    const hash = crypto.createHash('sha256').update(id.trim().toLowerCase()).digest('hex').slice(0, 40);
    return path.join(backupsDir, `${hash}.json`);
  };

  /**
   * POST /api/user-data/backup
   * Kullanıcının tüm tarayıcı verilerini sunucu ve Supabase veritabanına kaydeder.
   */
  app.post('/api/user-data/backup', async (req, res) => {
    try {
      if (rateLimited(req)) return res.status(429).json({ error: 'Çok sık yedekleme isteği; biraz sonra tekrar deneyin.' });
      const body = req.body || {};
      const claimed = String(body.uid || req.headers['x-user-id'] || '').trim().slice(0, 128);
      const who = await resolveIdentity(req, claimed);
      if (!who.id) return res.status(who.status || 401).json({ error: who.error });
      const { uid, email, verified } = who.id;

      const primaryId = uid;
      const backupFile = getBackupFilePath(primaryId);
      // Doğrulanmış hesaba ait yedek, jetonsuz istekle asla ezilmez
      if (!verified && readBackup(backupFile)?.verified) {
        return res.status(401).json({ error: 'Bu hesabın yedeği için giriş yapılmalıdır.' });
      }

      const savedAt = new Date().toISOString();
      const bundleToSave = {
        ...body,
        uid,
        email: email || undefined,
        verified,
        serverSavedAt: savedAt,
      };

      // Atomik dosya yazımı
      const tmpFile = `${backupFile}.${process.pid}.${Date.now()}.tmp`;
      fs.writeFileSync(tmpFile, JSON.stringify(bundleToSave, null, 2), 'utf8');
      fs.renameSync(tmpFile, backupFile);

      // E-posta üzerinden de erişilebilmesi için ikincil kopya (yalnız Firebase'in doğruladığı e-posta)
      if (verified && email && email !== primaryId) {
        const emailFile = getBackupFilePath(email);
        try {
          fs.copyFileSync(backupFile, emailFile);
        } catch {
          // İkincil kopya hatası kritik değil
        }
      }

      // users.json ve Supabase güncellemesi
      let matchedUser: any = null;
      try {
        const users = deps.loadUsers();
        const existingIdx = users.findIndex(
          (u) => (uid && u.uid === uid) || (email && u.email && u.email.toLowerCase() === email)
        );

        const statsSummary = {
          selftestCount: Array.isArray(body.stats?.selftestHistory) ? body.stats.selftestHistory.length : 0,
          notesCount: Array.isArray(body.notes) ? body.notes.length : 0,
          notificationsCount: Array.isArray(body.notifications) ? body.notifications.length : 0,
          favoritesCount: Array.isArray(body.stats?.favorites) ? body.stats.favorites.length : 0,
          activityCount: Array.isArray(body.stats?.activityLog) ? body.stats.activityLog.length : 0,
          studySecondsTotal: Object.values(body.stats?.studySeconds || {}).reduce(
            (acc: number, val: any) => acc + (Number(val) || 0),
            0
          ),
        };

        if (existingIdx !== -1) {
          const user = users[existingIdx];
          user.lastBackupAt = savedAt;
          user.backupStats = statsSummary;
          if (email && !user.email) user.email = email;
          if (body.displayName && !user.displayName) user.displayName = body.displayName;
          if (body.studentNumber && !user.studentNumber) user.studentNumber = body.studentNumber;
          user.data = {
            ...(user.data || {}),
            lastBackupAt: savedAt,
            backupStats: statsSummary,
          };
          deps.saveUsers(users);
          matchedUser = user;
        } else if (verified) {
          // Yeni kullanıcı kaydı yalnız doğrulanmış hesaplar için (anonim cihaz yedekleri listeyi doldurmasın)
          const newUser = {
            uid,
            email: email || 'ogrenci@medsoru.local',
            displayName: body.displayName || 'Öğrenci',
            studentNumber: body.studentNumber || null,
            role: 'student',
            createdAt: savedAt,
            lastLoginAt: savedAt,
            lastBackupAt: savedAt,
            backupStats: statsSummary,
            data: {
              lastBackupAt: savedAt,
              backupStats: statsSummary,
            },
          };
          users.unshift(newUser);
          deps.saveUsers(users);
          matchedUser = newUser;
        }

        if (matchedUser) {
          deps.mirrorUserToDb(matchedUser).catch((e: any) => {
            console.warn('[UserDataBackup] meds-pg mirror non-fatal warning:', e?.message || e);
          });
        }
      } catch (dbErr) {
        console.warn('[UserDataBackup] users.json sync non-fatal warning:', dbErr);
      }

      const selftestCount = Array.isArray(body.stats?.selftestHistory) ? body.stats.selftestHistory.length : 0;
      const notesCount = Array.isArray(body.notes) ? body.notes.length : 0;
      const notificationsCount = Array.isArray(body.notifications) ? body.notifications.length : 0;
      const favoritesCount = Array.isArray(body.stats?.favorites) ? body.stats.favorites.length : 0;

      res.json({
        success: true,
        backedUpAt: savedAt,
        message: 'Kullanıcı verileri, istatistikler ve bildirimler veritabanına başarıyla kaydedildi.',
        summary: {
          selftestCount,
          notesCount,
          notificationsCount,
          favoritesCount,
        },
      });
    } catch (err: any) {
      console.error('[UserDataBackup] POST /api/user-data/backup error:', err);
      res.status(500).json({ error: err.message || 'Yedekleme sırasında sunucu hatası oluştu.' });
    }
  });

  /**
   * GET /api/user-data/backup
   * Belirtilen kullanıcının veritabanındaki en son yedeğini çeker.
   */
  app.get('/api/user-data/backup', async (req, res) => {
    try {
      const claimed = String(req.query.uid || req.headers['x-user-id'] || '').trim().slice(0, 128);
      const who = await resolveIdentity(req, claimed);
      if (!who.id) return res.status(who.status || 401).json({ error: who.error });
      const { uid, email, verified } = who.id;

      // Öncelik: uid ile dosya ara, yoksa (doğrulanmış) e-posta ile ara
      let backupFile = getBackupFilePath(uid);
      if (!fs.existsSync(backupFile) && verified && email) {
        backupFile = getBackupFilePath(email);
      }
      // Doğrulanmış hesabın yedeği jetonsuz okunamaz
      if (!verified && readBackup(backupFile)?.verified) {
        return res.status(401).json({ error: 'Bu hesabın yedeği için giriş yapılmalıdır.' });
      }

      if (backupFile && fs.existsSync(backupFile)) {
        try {
          const raw = fs.readFileSync(backupFile, 'utf8');
          const data = JSON.parse(raw);
          return res.json({
            success: true,
            found: true,
            backedUpAt: data.serverSavedAt || data.clientUpdatedAt,
            data,
          });
        } catch (readErr: any) {
          console.error('[UserDataBackup] Backup file read error:', readErr);
        }
      }

      return res.json({
        success: true,
        found: false,
        message: 'Kullanıcı için henüz kayıtlı bir veritabanı yedeği bulunmuyor.',
      });
    } catch (err: any) {
      res.status(500).json({ error: err.message || 'Yedek okunurken hata oluştu.' });
    }
  });

  /**
   * GET /api/user-data/my-comments
   * Kullanıcının soru veritabanındaki tüm yorumlarını ve katkılarını listeler.
   */
  app.get('/api/user-data/my-comments', (req, res) => {
    try {
      const uid = String(req.query.uid || req.headers['x-user-id'] || '').trim();
      const email = String(req.query.email || '').trim().toLowerCase();
      const author = String(req.query.author || '').trim().toLowerCase();

      if (!uid && !email && !author) {
        return res.status(400).json({ error: 'uid, email veya author belirtilmelidir.' });
      }

      const pastQuestions = deps.getPastQuestions();
      const userComments: any[] = [];

      for (const q of pastQuestions) {
        if (!Array.isArray(q.comments)) continue;
        for (const c of q.comments) {
          if (!c) continue;
          const matchUid = Boolean(uid && c.authorUid === uid);
          const matchEmail = Boolean(email && c.authorEmail && c.authorEmail.toLowerCase() === email);
          const matchAuthor = Boolean(author && c.author && c.author.toLowerCase() === author);

          if (matchUid || matchEmail || matchAuthor) {
            userComments.push({
              id: c.id,
              questionId: q.id,
              questionYear: q.year,
              faculty: q.faculty,
              term: q.term,
              committee: q.committee,
              discipline: q.discipline,
              topic: q.topic,
              questionSnippet: (q.question || q.text || q.stem || '').slice(0, 160),
              text: c.text,
              createdAt: c.createdAt || c.timestamp,
              author: c.author,
              parentId: c.parentId,
            });
          }
        }
      }

      // En yeni yorumlar en başta
      userComments.sort((a, b) => (b.createdAt || '').localeCompare(a.createdAt || ''));

      res.json({
        success: true,
        count: userComments.length,
        comments: userComments,
      });
    } catch (err: any) {
      res.status(500).json({ error: err.message || 'Yorumlar taranırken hata oluştu.' });
    }
  });
}
