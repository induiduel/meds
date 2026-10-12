/**
 * Kullanıcı notları yedeği (sunucu). Notlar tarayıcıda tutulur; bu uçlar cihazlar arası eşitleme ve
 * kayıp önleme içindir. Kimlik:
 * - Oturum açık: `Authorization: Bearer <Firebase ID token>` → defter hesaba bağlıdır (kod `acct:<uid>`,
 *   yalnız sunucuda türetilir). Hangi cihazdan girilirse girilsin aynı defter gelir.
 * - Girişsiz: eşitleme kodu (x-user-id; cihaz belirteci ya da kullanıcının başka cihaza taşıdığı kod).
 * Dosya adı kodun SHA-256 özetidir → kod diskte açık durmaz.
 * Birleştirme: not başına son güncellenen kazanır; silinenler "mezar taşı" ile yayılır (90 gün).
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import type express from 'express';
import { requestUser, accountNotesCode } from './firebaseIdentity';

export interface Note { id: string; updatedAt: string; [k: string]: unknown }
export interface Store { notes: Note[]; deleted: Record<string, string>; updatedAt: string }

const MAX_NOTES = 1000;
const MAX_BODY = 60_000;
const TOMBSTONE_DAYS = 90;

export function mergeNotes(a: Store, incoming: { notes?: unknown; deleted?: unknown }): Store {
  const deleted: Record<string, string> = { ...(a.deleted || {}) };
  const inDel = incoming.deleted && typeof incoming.deleted === 'object' ? (incoming.deleted as Record<string, string>) : {};
  for (const [id, at] of Object.entries(inDel)) if (!deleted[id] || deleted[id] < at) deleted[id] = String(at);
  const byId = new Map<string, Note>();
  for (const n of a.notes || []) byId.set(n.id, n);
  for (const raw of Array.isArray(incoming.notes) ? incoming.notes : []) {
    const n = raw as Note;
    if (!n || typeof n.id !== 'string' || !n.id || typeof n.updatedAt !== 'string') continue;
    if (typeof n.body === 'string' && n.body.length > MAX_BODY) continue;
    const cur = byId.get(n.id);
    if (!cur || cur.updatedAt < n.updatedAt) byId.set(n.id, n);
  }
  // Silinme notun son düzenlemesinden yeniyse not düşer; daha sonra düzenlenmişse geri gelir
  for (const [id, at] of Object.entries(deleted)) {
    const n = byId.get(id);
    if (n && n.updatedAt <= at) byId.delete(id);
  }
  const cutoff = new Date(Date.now() - TOMBSTONE_DAYS * 864e5).toISOString();
  for (const [id, at] of Object.entries(deleted)) if (at < cutoff) delete deleted[id];
  const notes = Array.from(byId.values()).sort((x, y) => y.updatedAt.localeCompare(x.updatedAt)).slice(0, MAX_NOTES);
  return { notes, deleted, updatedAt: new Date().toISOString() };
}

/** Not defteri deposu: hem /api/notes hem hesap yedeği (/api/user-data/backup) aynı depoyu kullanır. */
export function createNotesStore(dataDir: string, onNotesUpdated?: (codeHash: string, store: Store) => void) {
  const dir = path.join(dataDir, 'user_notes');
  const fileFor = (code: string) => path.join(dir, crypto.createHash('sha256').update(code).digest('hex').slice(0, 40) + '.json');
  const read = (code: string): Store => {
    try { return JSON.parse(fs.readFileSync(fileFor(code), 'utf8')); } catch { return { notes: [], deleted: {}, updatedAt: '' }; }
  };
  const merge = (code: string, incoming: { notes?: unknown; deleted?: unknown }): Store => {
    fs.mkdirSync(dir, { recursive: true });
    const f = fileFor(code);
    const merged = mergeNotes(read(code), incoming || {});
    const tmp = `${f}.${process.pid}.${Date.now()}.tmp`;
    fs.writeFileSync(tmp, JSON.stringify(merged), 'utf8');
    fs.renameSync(tmp, f);
    if (onNotesUpdated) {
      try {
        onNotesUpdated(crypto.createHash('sha256').update(code).digest('hex').slice(0, 16), merged);
      } catch (_) {}
    }
    return merged;
  };
  return { read, merge };
}
export type NotesStore = ReturnType<typeof createNotesStore>;

export function registerUserNotesRoutes(app: express.Express, store: NotesStore) {
  const deviceCode = (req: express.Request) => {
    const c = String(req.headers['x-user-id'] || '').trim();
    // `acct:` öneki yalnız sunucunun doğrulanmış jetondan türettiği hesap defterine aittir; elle yazılamaz
    // (uid'ler yorumlarda açık görünür; önek serbest olsaydı jetonsuz hesap defterine ulaşılırdı).
    if (c.toLowerCase().startsWith('acct:')) return '';
    return c.length >= 12 && c.length <= 200 ? c : '';
  };
  /** Oturum açıksa hesap defteri, değilse eşitleme kodu. Geçersiz jeton → 401 (sessizce cihaza düşülmez). */
  const codeOf = async (req: express.Request, res: express.Response): Promise<string | null> => {
    const who = await requestUser(req);
    if (who.invalid) {
      res.status(401).json({ error: 'Oturum doğrulanamadı; lütfen yeniden giriş yapın.' });
      return null;
    }
    if (who.user) return accountNotesCode(who.user.uid);
    const c = deviceCode(req);
    if (!c) {
      res.status(400).json({ error: 'Eşitleme kodu (x-user-id) gerekli' });
      return null;
    }
    return c;
  };

  app.get('/api/notes', async (req, res) => {
    const code = await codeOf(req, res);
    if (!code) return;
    const notesStore = store.read(code);
    const since = typeof req.query.since === 'string' ? req.query.since.trim() : '';

    // Incremental Delta Sync (1. Madde: Değişiklik Senkronizasyonu)
    if (since) {
      if (notesStore.updatedAt && since >= notesStore.updatedAt) {
        return res.json({
          upToDate: true,
          count: notesStore.notes.length,
          updatedAt: notesStore.updatedAt,
          notes: [],
          deleted: {}
        });
      }

      const deltaNotes = notesStore.notes.filter((n) => n.updatedAt && n.updatedAt > since);
      const deltaDeleted: Record<string, string> = {};
      for (const [id, at] of Object.entries(notesStore.deleted || {})) {
        if (at > since) deltaDeleted[id] = at;
      }

      return res.json({
        upToDate: deltaNotes.length === 0 && Object.keys(deltaDeleted).length === 0,
        count: notesStore.notes.length,
        updatedAt: notesStore.updatedAt,
        notes: deltaNotes,
        deleted: deltaDeleted
      });
    }

    res.json(notesStore);
  });

  // Yazma parolası gerekmez (kimlik = gizli kod); kötüye kullanıma karşı IP başına dakikada 60 yazma.
  const writeRate = new Map<string, { n: number; at: number }>();
  app.put('/api/notes', async (req, res) => {
    const ip = String(req.headers['cf-connecting-ip'] || req.ip || '');
    const now = Date.now();
    const r = writeRate.get(ip);
    if (!r || now - r.at > 60_000) {
      if (writeRate.size > 5000) writeRate.clear();
      writeRate.set(ip, { n: 1, at: now });
    } else if (++r.n > 60) {
      return res.status(429).json({ error: 'Çok sık eşitleme isteği; biraz sonra tekrar denenecek.' });
    }
    const code = await codeOf(req, res);
    if (!code) return;
    try {
      res.json(store.merge(code, req.body || {}));
    } catch (err: any) {
      res.status(500).json({ error: 'Notlar kaydedilemedi: ' + err.message });
    }
  });
}
