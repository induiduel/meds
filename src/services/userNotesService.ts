/**
 * Kullanıcı notları yedeği (sunucu). Notlar tarayıcıda tutulur; bu uçlar cihazlar arası eşitleme ve
 * kayıp önleme içindir. Kimlik = eşitleme kodu (x-user-id; cihaz belirteci ya da kullanıcının başka
 * cihaza taşıdığı kod). Dosya adı kodun SHA-256 özetidir → kod diskte açık durmaz.
 * Birleştirme: not başına son güncellenen kazanır; silinenler "mezar taşı" ile yayılır (90 gün).
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import type express from 'express';

interface Note { id: string; updatedAt: string; [k: string]: unknown }
interface Store { notes: Note[]; deleted: Record<string, string>; updatedAt: string }

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

export function registerUserNotesRoutes(app: express.Express, dataDir: string) {
  const dir = path.join(dataDir, 'user_notes');
  const fileFor = (code: string) => path.join(dir, crypto.createHash('sha256').update(code).digest('hex').slice(0, 40) + '.json');
  const codeOf = (req: express.Request) => {
    const c = String(req.headers['x-user-id'] || '').trim();
    return c.length >= 12 && c.length <= 200 ? c : '';
  };
  const read = (f: string): Store => {
    try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return { notes: [], deleted: {}, updatedAt: '' }; }
  };

  app.get('/api/notes', (req, res) => {
    const code = codeOf(req);
    if (!code) return res.status(400).json({ error: 'Eşitleme kodu (x-user-id) gerekli' });
    res.json(read(fileFor(code)));
  });

  app.put('/api/notes', (req, res) => {
    const code = codeOf(req);
    if (!code) return res.status(400).json({ error: 'Eşitleme kodu (x-user-id) gerekli' });
    try {
      fs.mkdirSync(dir, { recursive: true });
      const f = fileFor(code);
      const merged = mergeNotes(read(f), req.body || {});
      const tmp = `${f}.${process.pid}.tmp`;
      fs.writeFileSync(tmp, JSON.stringify(merged), 'utf8');
      fs.renameSync(tmp, f);
      res.json(merged);
    } catch (err: any) {
      res.status(500).json({ error: 'Notlar kaydedilemedi: ' + err.message });
    }
  });
}
