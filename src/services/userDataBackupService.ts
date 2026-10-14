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
import { requestUser, accountNotesCode } from './firebaseIdentity';
import { mergeNotes, type NotesStore } from './userNotesService';

export interface UserDataBackupDeps {
  dataDir: string;
  loadUsers: () => any[];
  saveUsers: (users: any[]) => void;
  mirrorUserToDb: (user: any) => Promise<void>;
  getPastQuestions: () => any[];
  /** Hesaba bağlı not defteri (/api/notes ile aynı depo). */
  notesStore: NotesStore;
  /** Kayıttan sonra: meds-pg `user_data` yansısı + kullanıcının diğer cihazlarına SSE (`user_data_changed`). */
  onSaved?: (info: { uid: string; email: string; verified: boolean; bundle: any; origin: string }) => void;
}

/** Kullanıcının SSE olay anahtarı: olay tüm ziyaretçilere gider, yalnız bu özeti kendi uid'sinden üreten cihaz çeker. */
export const userEventHash = (uid: string): string => crypto.createHash('sha256').update(`ud:${uid}`).digest('hex').slice(0, 16);

type Identity = { uid: string; email: string; verified: boolean };

// Cihaz jetonu: src/utils/voterId.ts → `dev-<uuid>` (ya da eski tarayıcılarda `dev-<zaman>-<rastgele>`)
const DEVICE_TOKEN_RE = /^dev-[a-z0-9-]{16,64}$/i;

// ---------------- Sunucu tarafı birleştirme ----------------
// Yedek artık üzerine yazılmaz: gelen paket mevcut yedekle birleştirilir ve sonuç istemciye döner. Böylece yeni/
// sıfırlanmış bir cihazın boş paketi hesabın verisini silemez; cihazlar her yedekte birbirine yakınsar.
// Not: favori/tekrar listesi gibi kümelerde birleşim kullanılır (bir cihazda kaldırılan öğe diğerinden geri gelebilir).

const arr = (v: unknown): any[] => (Array.isArray(v) ? v : []);
const obj = (v: unknown): Record<string, any> => (v && typeof v === 'object' && !Array.isArray(v) ? (v as Record<string, any>) : {});
const itemKey = (x: any): string => (x && typeof x === 'object' ? String(x.id ?? x.at ?? x.date ?? x.timestamp ?? JSON.stringify(x)) : String(x));

/** Kimliğe göre birleşim; aynı kimlikte `pick(eski, yeni)` kazanır (varsayılan: gelen). */
function unionBy<T>(a: T[], b: T[], pick: (oldV: T, newV: T) => T = (_o, n) => n, keyOf: (x: T) => string = itemKey): T[] {
  const m = new Map<string, T>();
  for (const x of a) if (x != null) m.set(keyOf(x), x);
  for (const x of b) {
    if (x == null) continue;
    const k = keyOf(x);
    const cur = m.get(k);
    m.set(k, cur === undefined ? x : pick(cur, x));
  }
  return Array.from(m.values());
}
const newerAt = (o: any, n: any) => (String(n?.at || n?.updatedAt || '') >= String(o?.at || o?.updatedAt || '') ? n : o);

export function mergeUserBundle(existing: any, incoming: any): any {
  const e = obj(existing);
  const i = obj(incoming);
  const es = { ...obj(e.stats) };
  const is = { ...obj(i.stats) };

  // İlerleme sıfırlaması (kapsam → ISO): daha yeni sıfırlamayı taşıyan taraf o kapsamda tek başına geçerlidir;
  // eski taraftan yalnız sıfırlamadan sonra yapılmış (zamanı olan) çözümler alınır.
  const eReset = obj(e.progressReset);
  const iReset = obj(i.progressReset);
  const progressReset: Record<string, string> = {};
  for (const scope of ['soru', 'kart']) {
    const at = [String(eReset[scope] || ''), String(iReset[scope] || '')].sort().pop() || '';
    if (!at) continue;
    progressReset[scope] = at;
    const after = (x: any) => String(x?.at || '') > at;
    for (const [side, stamp] of [[es, String(eReset[scope] || '')], [is, String(iReset[scope] || '')]] as const) {
      if (stamp >= at) continue;
      if (scope === 'soru') {
        side.selftestHistory = arr(side.selftestHistory).filter(after);
        side.studyProgress = Object.fromEntries(Object.entries(obj(side.studyProgress)).filter(([, r]) => after(r)));
        side.studyReview = [];
      } else side.flashcards = {};
    }
  }

  const studySeconds: Record<string, number> = { ...obj(es.studySeconds) };
  for (const [day, sec] of Object.entries(obj(is.studySeconds))) studySeconds[day] = Math.max(Number(studySeconds[day]) || 0, Number(sec) || 0);

  const studyProgress: Record<string, any> = { ...obj(es.studyProgress) };
  for (const [id, rec] of Object.entries(obj(is.studyProgress))) studyProgress[id] = studyProgress[id] ? newerAt(studyProgress[id], rec) : rec;

  // Kart kutusu: daha çok tekrar edilmiş (seen) durum güncel kabul edilir
  const flashcards: Record<string, any> = { ...obj(es.flashcards) };
  for (const [id, st] of Object.entries(obj(is.flashcards))) {
    const cur = flashcards[id];
    flashcards[id] = !cur || (Number(st?.seen) || 0) > (Number(cur?.seen) || 0) || ((Number(st?.seen) || 0) === (Number(cur?.seen) || 0) && (Number(st?.due) || 0) > (Number(cur?.due) || 0)) ? st : cur;
  }

  const activityKey = (a: any) => `${a?.at}|${a?.kind}|${a?.text}`;
  const stats = {
    activityLog: unionBy(arr(es.activityLog), arr(is.activityLog), undefined, activityKey)
      .sort((x: any, y: any) => String(x?.at).localeCompare(String(y?.at)))
      .slice(-600),
    studySeconds,
    selftestHistory: unionBy(arr(es.selftestHistory), arr(is.selftestHistory))
      .sort((x: any, y: any) => String(x?.at || '').localeCompare(String(y?.at || '')))
      .slice(-500),
    studyProgress,
    studyReview: unionBy(arr(es.studyReview), arr(is.studyReview)),
    flashcards,
    favorites: unionBy(arr(es.favorites), arr(is.favorites)),
    cardFavorites: unionBy(arr(es.cardFavorites), arr(is.cardFavorites), newerAt),
    bookmarkedEncyclopedia: unionBy(arr(es.bookmarkedEncyclopedia), arr(is.bookmarkedEncyclopedia)),
  };

  // Silinen bildirimler (mezar taşı) ve "geçmişi temizle" zamanı: birleşim silineni geri getirmesin
  const eTomb = obj(e.notificationsDeleted);
  const iTomb = obj(i.notificationsDeleted);
  const deletedIds: Record<string, string> = { ...obj(eTomb.ids) };
  for (const [id, at] of Object.entries(obj(iTomb.ids))) if (!deletedIds[id] || String(at) > deletedIds[id]) deletedIds[id] = String(at);
  const clearedAt = [String(eTomb.clearedAt || ''), String(iTomb.clearedAt || '')].sort().pop() || '';
  // En eski mezar taşları budanır (bildirim listesi zaten 300 ile sınırlı)
  const tombIds = Object.fromEntries(Object.entries(deletedIds).sort((a, b) => b[1].localeCompare(a[1])).slice(0, 600));

  // Bildirim bir cihazda okunduysa okunmuş sayılır
  const notifications = unionBy(arr(e.notifications), arr(i.notifications), (o: any, n: any) => ({ ...o, ...n, read: Boolean(o?.read || n?.read) }))
    .filter((n: any) => n && !tombIds[n.id] && !(clearedAt && String(n.createdAt || '') <= clearedAt))
    .sort((x: any, y: any) => String(y?.createdAt || '').localeCompare(String(x?.createdAt || '')))
    .slice(0, 300);

  return {
    ...e,
    ...i,
    displayName: i.displayName || e.displayName || null,
    studentNumber: i.studentNumber || e.studentNumber || null,
    stats,
    notifications,
    notificationsDeleted: { ids: tombIds, clearedAt },
    notificationPrefs: { ...obj(e.notificationPrefs), ...obj(i.notificationPrefs) },
    kv: mergeKv(e.kv, i.kv),
    progressReset,
  };
}

// ---------------- Profil anahtar deposu (kv) ----------------
// İstemcideki her kullanıcı verisi anahtarı (Öğren ilerlemesi, vurgular, çizimler, kart notları, tercihler…)
// `{ v: localStorage değeri | null (silindi), at: ISO }` olarak taşınır; anahtar başına son yazan kazanır.
const KV_MAX_KEYS = 600;
const KV_MAX_VALUE = 2_000_000;
const KV_KEY_RE = /^[A-Za-z0-9_.:\-]{1,160}$/;

export function mergeKv(existing: unknown, incoming: unknown): Record<string, { v: string | null; at: string }> {
  const out: Record<string, { v: string | null; at: string }> = {};
  for (const src of [obj(existing), obj(incoming)]) {
    for (const [k, rec] of Object.entries(src)) {
      if (!KV_KEY_RE.test(k) || !rec || typeof rec !== 'object') continue;
      const v = (rec as any).v;
      const at = String((rec as any).at || '');
      if (v !== null && typeof v !== 'string') continue;
      if (typeof v === 'string' && v.length > KV_MAX_VALUE) continue;
      const cur = out[k];
      if (!cur || at > cur.at) out[k] = { v, at };
    }
  }
  const keys = Object.keys(out);
  if (keys.length <= KV_MAX_KEYS) return out;
  // Sınır aşılırsa önce eski silinmiş kayıtlar, sonra en eskiler düşer
  keys.sort((a, b) => Number(out[a].v === null) - Number(out[b].v === null) || out[b].at.localeCompare(out[a].at));
  return Object.fromEntries(keys.slice(0, KV_MAX_KEYS).map((k) => [k, out[k]]));
}

/** Yanıtta yalnız istemcinin henüz görmediği kv kayıtları gider (her kayıtta tüm çizim/vurgu verisi dönmesin). */
function withKvSince(bundle: any, since: unknown): any {
  const s = typeof since === 'string' ? since : '';
  const kv = obj(bundle?.kv);
  const sent = s ? Object.fromEntries(Object.entries(kv).filter(([, r]: any) => String(r?.at || '') > s)) : kv;
  const kvRev = Object.values(kv).reduce((m: string, r: any) => (String(r?.at || '') > m ? String(r.at) : m), '');
  return { ...bundle, kv: sent, kvRev };
}

export interface ServerUserNotification {
  type: string;
  title: string;
  message: string;
  deepLinkUrl?: string;
  targetType?: string;
  targetId?: string;
  /** Aynı olay iki kez bildirilmesin (ör. `report_resolved:<raporId>`). */
  dedupeKey?: string;
}

export function registerUserDataBackupRoutes(app: express.Express, deps: UserDataBackupDeps) {
  const backupsDir = path.join(deps.dataDir, 'user_backups');
  if (!fs.existsSync(backupsDir)) {
    fs.mkdirSync(backupsDir, { recursive: true });
  }

  /** İstek sahibinin kimliği; geçersizse hata iletisi. */
  async function resolveIdentity(req: express.Request, claimedUid: string): Promise<{ id?: Identity; error?: string; status?: number }> {
    const who = await requestUser(req);
    if (who.invalid) return { error: 'Oturum doğrulanamadı; lütfen yeniden giriş yapın.', status: 401 };
    if (who.user) return { id: { uid: who.user.uid, email: who.user.email, verified: true } };
    if (DEVICE_TOKEN_RE.test(claimedUid)) return { id: { uid: claimedUid, email: '', verified: false } };
    return { error: 'Bu hesabın yedeği için giriş yapılmalıdır.', status: 401 };
  }

  /** Notlar: hesapta hesap defteri (/api/notes ile ortak), cihazda yedeğin kendi içinde mezar taşlı birleşim. */
  function mergeBundleNotes(id: Identity, existing: any, incoming: any): { notes: any[]; notesDeleted: Record<string, string> } {
    const inc = { notes: arr(incoming?.notes), deleted: obj(incoming?.notesDeleted) };
    if (id.verified) {
      const st = deps.notesStore.merge(accountNotesCode(id.uid), inc);
      return { notes: st.notes, notesDeleted: st.deleted };
    }
    const st = mergeNotes({ notes: arr(existing?.notes), deleted: obj(existing?.notesDeleted), updatedAt: '' }, inc);
    return { notes: st.notes, notesDeleted: st.deleted };
  }

  // Hız sınırı: profil artık her değişiklikte birkaç saniye içinde eşitlenir. IP başına dakikada 240 (yurt/okul ağında
  // pek çok öğrenci aynı IP'yi paylaşır), kimlik başına dakikada 40 yazma.
  const writeRate = new Map<string, { n: number; at: number }>();
  const overLimit = (key: string, max: number) => {
    const now = Date.now();
    const r = writeRate.get(key);
    if (!r || now - r.at > 60_000) {
      if (writeRate.size > 10_000) writeRate.clear();
      writeRate.set(key, { n: 1, at: now });
      return false;
    }
    return ++r.n > max;
  };
  const rateLimited = (req: express.Request) => overLimit(`ip:${String(req.headers['cf-connecting-ip'] || req.ip || '')}`, 240);

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

  /** Atomik dosya yazımı (girintisiz: kv içinde çizim/vurgu verisi büyüyebilir). */
  const writeBackup = (file: string, bundle: any) => {
    const tmpFile = `${file}.${process.pid}.${Date.now()}.tmp`;
    fs.writeFileSync(tmpFile, JSON.stringify(bundle), 'utf8');
    fs.renameSync(tmpFile, file);
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
      if (overLimit(`id:${uid}`, 40)) return res.status(429).json({ error: 'Çok sık yedekleme isteği; biraz sonra tekrar deneyin.' });

      const primaryId = uid;
      const backupFile = getBackupFilePath(primaryId);
      // Doğrulanmış hesaba ait yedek, jetonsuz istekle asla ezilmez
      if (!verified && readBackup(backupFile)?.verified) {
        return res.status(401).json({ error: 'Bu hesabın yedeği için giriş yapılmalıdır.' });
      }

      // Hesabın ilk uid'li yedeği yoksa eski e-posta kopyası taban alınır (eski kayıtlar kaybolmasın)
      let existing = readBackup(backupFile);
      if (!existing && verified && email) existing = readBackup(getBackupFilePath(email));

      const savedAt = new Date().toISOString();
      const { kvSince: _kvSince, origin: _origin, ...incoming } = body;
      const bundleToSave = {
        ...mergeUserBundle(existing, incoming),
        ...mergeBundleNotes(who.id, existing, body),
        uid,
        email: email || undefined,
        verified,
        serverSavedAt: savedAt,
      };

      writeBackup(backupFile, bundleToSave);
      try {
        deps.onSaved?.({ uid, email, verified, bundle: bundleToSave, origin: String(body.origin || '').slice(0, 64) });
      } catch (e: any) {
        console.warn('[UserDataBackup] onSaved uyarısı:', e?.message || e);
      }

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
          selftestCount: Array.isArray(bundleToSave.stats?.selftestHistory) ? bundleToSave.stats.selftestHistory.length : 0,
          notesCount: Array.isArray(bundleToSave.notes) ? bundleToSave.notes.length : 0,
          notificationsCount: Array.isArray(bundleToSave.notifications) ? bundleToSave.notifications.length : 0,
          favoritesCount: Array.isArray(bundleToSave.stats?.favorites) ? bundleToSave.stats.favorites.length : 0,
          activityCount: Array.isArray(bundleToSave.stats?.activityLog) ? bundleToSave.stats.activityLog.length : 0,
          studySecondsTotal: Object.values(bundleToSave.stats?.studySeconds || {}).reduce(
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

      const selftestCount = Array.isArray(bundleToSave.stats?.selftestHistory) ? bundleToSave.stats.selftestHistory.length : 0;
      const notesCount = Array.isArray(bundleToSave.notes) ? bundleToSave.notes.length : 0;
      const notificationsCount = Array.isArray(bundleToSave.notifications) ? bundleToSave.notifications.length : 0;
      const favoritesCount = Array.isArray(bundleToSave.stats?.favorites) ? bundleToSave.stats.favorites.length : 0;

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
        // Birleştirilmiş paket: istemci bunu yerel verisine uygular (cihazlar yakınsar); kv yalnız yeni kayıtlar
        data: withKvSince(bundleToSave, body.kvSince),
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
          // Hesapta notların güncel hâli hesap defterindedir (başka cihazdan /api/notes ile eklenmiş olabilir)
          if (verified) {
            const st = deps.notesStore.read(accountNotesCode(uid));
            if (st.updatedAt) {
              data.notes = st.notes;
              data.notesDeleted = st.deleted;
            }
          }
          return res.json({
            success: true,
            found: true,
            backedUpAt: data.serverSavedAt || data.clientUpdatedAt,
            data: withKvSince(data, req.query.kvSince),
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
  app.get('/api/user-data/my-comments', async (req, res) => {
    try {
      // Kimlik sorgudan alınmaz (başkasının yorumları/e-postası okunabiliyordu): doğrulanmış oturum ya da cihaz jetonu.
      const ident = await resolveIdentity(req, String(req.headers['x-user-id'] || '').trim());
      if (!ident.id) return res.status(ident.status || 401).json({ error: ident.error });
      const uid = ident.id.uid;
      const email = ident.id.verified ? String(ident.id.email || '').toLowerCase() : '';
      const author = '';

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

  /**
   * Sunucu olayını (raporun çözüldü, yorumuna yanıt…) öğrencinin profil bildirimlerine yazar ve cihazlarına SSE ile
   * duyurur. Kullanıcı uid ya da e-postayla bulunur; hiç yedeği yoksa yeni profil dosyası açılır.
   */
  function pushUserNotification(target: { uid?: string | null; email?: string | null }, n: ServerUserNotification): boolean {
    try {
      let uid = String(target.uid || '').trim();
      const email = String(target.email || '').trim().toLowerCase();
      if (!uid && email) {
        const u = deps.loadUsers().find((x: any) => x?.email && String(x.email).toLowerCase() === email);
        uid = String(u?.uid || '').trim();
      }
      if (!uid || uid.length > 128) return false;
      const file = getBackupFilePath(uid);
      const existing = readBackup(file) || { uid, email: email || undefined, verified: !DEVICE_TOKEN_RE.test(uid), stats: {}, notifications: [] };
      const list = arr(existing.notifications);
      const id = `srv-${crypto.createHash('sha1').update(n.dedupeKey || `${n.type}|${n.targetId}|${Date.now()}`).digest('hex').slice(0, 16)}`;
      if (list.some((x: any) => x?.id === id) || obj(obj(existing.notificationsDeleted).ids)[id]) return false;
      const item = {
        id,
        type: n.type,
        title: n.title.slice(0, 160),
        message: n.message.slice(0, 600),
        deepLinkUrl: n.deepLinkUrl,
        targetType: n.targetType,
        targetId: n.targetId,
        read: false,
        createdAt: new Date().toISOString(),
        source: 'server',
      };
      const bundle = { ...existing, notifications: [item, ...list].slice(0, 300), serverSavedAt: item.createdAt };
      writeBackup(file, bundle);
      deps.onSaved?.({ uid, email: String(bundle.email || email || ''), verified: Boolean(bundle.verified), bundle, origin: 'server' });
      return true;
    } catch (e: any) {
      console.warn('[UserDataBackup] Kullanıcı bildirimi yazılamadı:', e?.message || e);
      return false;
    }
  }

  return { pushUserNotification };
}
