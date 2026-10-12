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
}

export function registerUserDataBackupRoutes(app: express.Express, deps: UserDataBackupDeps) {
  const backupsDir = path.join(deps.dataDir, 'user_backups');
  if (!fs.existsSync(backupsDir)) {
    fs.mkdirSync(backupsDir, { recursive: true });
  }

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
      const body = req.body || {};
      const headerUid = String(req.headers['x-user-id'] || '').trim();
      const uid = String(body.uid || headerUid || '').trim();
      const email = String(body.email || '').trim().toLowerCase();

      if (!uid && !email) {
        return res.status(400).json({ error: 'uid veya email zorunludur.' });
      }

      const primaryId = uid || email;
      const backupFile = getBackupFilePath(primaryId);

      const savedAt = new Date().toISOString();
      const bundleToSave = {
        ...body,
        uid: uid || primaryId,
        email: email || undefined,
        serverSavedAt: savedAt,
      };

      // Atomik dosya yazımı
      const tmpFile = `${backupFile}.${process.pid}.${Date.now()}.tmp`;
      fs.writeFileSync(tmpFile, JSON.stringify(bundleToSave, null, 2), 'utf8');
      fs.renameSync(tmpFile, backupFile);

      // Email üzerinden de erişilebilmesi için ikincil hash dosyası (eğer uid ile farklıysa)
      if (email && email !== primaryId) {
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
        } else {
          const newUser = {
            uid: uid || 'user-' + Date.now().toString(36),
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
  app.get('/api/user-data/backup', (req, res) => {
    try {
      const uid = String(req.query.uid || req.headers['x-user-id'] || '').trim();
      const email = String(req.query.email || '').trim().toLowerCase();

      if (!uid && !email) {
        return res.status(400).json({ error: 'uid veya email zorunludur.' });
      }

      // Öncelik: uid ile dosya ara, yoksa email ile ara
      let backupFile = uid ? getBackupFilePath(uid) : '';
      if (!backupFile || !fs.existsSync(backupFile)) {
        if (email) {
          backupFile = getBackupFilePath(email);
        }
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
