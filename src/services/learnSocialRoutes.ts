/**
 * Öğren ekranı ortak katmanı (server-only, meds-pg):
 *  - Herkese açık slayt notları: SPOT / ÖNEMLİ / VURGU (isteğe bağlı seçili metne bağlı).
 *  - Metin bildirimi + tartışma: öğrenci seçtiği metni "Bildir"ir → herkes metnin yanında kırmızı "!" görür,
 *    dokununca o metin hakkındaki sohbet açılır. Bildirim yöneticiye de gider (triggerAdminNotification).
 *
 * Tablolar: deploy/pg/sql/learn_social.sql (learn_notes, learn_threads, learn_thread_messages).
 * Canlı yayın: her yazımdan sonra SSE `learn_social` olayı ({ deckId, type, op, item | id }).
 *
 * Uçlar (hepsi /api/learn/social altında; yazma parolası istemez, kendi sınırlarını uygular):
 *   GET    /api/learn/social?deckId=…                     → { notes, threads }
 *   POST   /api/learn/social/notes                        → { item }
 *   DELETE /api/learn/social/notes/:id?uid=…              (yazar ya da yönetici)
 *   POST   /api/learn/social/threads                      → { item, message }  (ilk mesajla birlikte)
 *   GET    /api/learn/social/threads/:id                  → { item, messages }
 *   POST   /api/learn/social/threads/:id/messages         → { message, item }
 *   DELETE /api/learn/social/messages/:id?uid=…           (yazar ya da yönetici)
 *   POST   /api/learn/social/threads/:id/status           { status: open|resolved } (yönetici ya da bildiren)
 *   DELETE /api/learn/social/threads/:id                  (yönetici)
 *
 * Kimlik: istemcinin `whoAmI()` kimliği (Firebase uid ya da cihaz kimliği) — öğren geri bildirimiyle aynı güven
 * modeli. Silme yalnız aynı kimlikle (ya da yönetici) yapılabilir.
 */
import type express from 'express';
import crypto from 'crypto';
import { pgPool } from './pgDb';

export type LearnNoteKind = 'spot' | 'onemli' | 'vurgu';
const KINDS = new Set<LearnNoteKind>(['spot', 'onemli', 'vurgu']);

const ID_RE = /^[\p{L}\p{N}._:-]{1,160}$/u;
const LIMITS = { note: 600, anchor: 300, quote: 400, ctx: 80, message: 1000, name: 60 };

const clip = (v: unknown, n: number) => String(v ?? '').replace(/\s+/g, ' ').trim().slice(0, n);
/** Mesaj gövdesi: satır sonları korunur, fazla boş satır sıkıştırılır */
const clipBody = (v: unknown, n: number) =>
  String(v ?? '')
    .replace(/\r\n?/g, '\n')
    .replace(/[^\S\n]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
    .slice(0, n);
const newId = (p: string) => `${p}-${Date.now().toString(36)}-${crypto.randomBytes(4).toString('hex')}`;

/* ---------------- hız sınırı (bellekte, kayan pencere) ---------------- */
const hits = new Map<string, number[]>();
function limited(key: string, max: number, windowMs: number): boolean {
  const now = Date.now();
  const arr = (hits.get(key) || []).filter((t) => now - t < windowMs);
  if (arr.length >= max) {
    hits.set(key, arr);
    return true;
  }
  arr.push(now);
  hits.set(key, arr);
  return false;
}
setInterval(() => {
  const now = Date.now();
  for (const [k, arr] of hits) if (!arr.some((t) => now - t < 3_600_000)) hits.delete(k);
}, 600_000).unref?.();

const clientIp = (req: express.Request) => String(req.headers['x-forwarded-for'] || req.ip || req.socket?.remoteAddress || '').split(',')[0].trim();

/* ---------------- satır → istemci biçimi ---------------- */
const noteView = (r: any, uid: string, admin: boolean) => ({
  id: r.id,
  deckId: r.deck_id,
  stepNumber: r.step_number,
  kind: r.kind as LearnNoteKind,
  body: r.body,
  anchor: r.anchor || '',
  author: { id: r.author_id, name: r.author_name },
  createdAt: new Date(r.created_at).toISOString(),
  mine: !!uid && r.author_id === uid,
  canDelete: admin || (!!uid && r.author_id === uid),
});
const threadView = (r: any, uid: string, admin: boolean) => ({
  id: r.id,
  deckId: r.deck_id,
  stepNumber: r.step_number,
  quote: r.quote,
  prefix: r.prefix || '',
  suffix: r.suffix || '',
  status: r.status as 'open' | 'resolved',
  reporter: { id: r.reporter_id, name: r.reporter_name },
  messageCount: r.message_count,
  createdAt: new Date(r.created_at).toISOString(),
  lastMessageAt: new Date(r.last_message_at).toISOString(),
  mine: !!uid && r.reporter_id === uid,
  canResolve: admin || (!!uid && r.reporter_id === uid),
});
const messageView = (r: any, uid: string, admin: boolean) => ({
  id: r.id,
  threadId: r.thread_id,
  body: r.body,
  author: { id: r.author_id, name: r.author_name },
  isAdmin: !!r.is_admin,
  createdAt: new Date(r.created_at).toISOString(),
  mine: !!uid && r.author_id === uid,
  canDelete: admin || (!!uid && r.author_id === uid),
});
/** Yayında herkes aynı yükü alır: kişiye özel alanlar (mine/canDelete) istemcide yeniden hesaplanır. */
const publicView = <T extends Record<string, any>>(v: T) => {
  const { mine, canDelete, canResolve, ...rest } = v as any;
  return rest;
};

export interface LearnSocialDeps {
  isAdmin: (req: express.Request) => boolean;
  broadcast: (event: string, data: any) => void;
  notifyAdmin: (p: { questionId: string; reason: string; details: string; author: string; topic?: string; link: string }) => void;
  censor?: (s: string) => string;
}

export function learnThreadLink(deckId: string, stepNumber: number, threadId: string) {
  return `/ogren/${encodeURIComponent(deckId)}?adim=${stepNumber}&tartisma=${encodeURIComponent(threadId)}`;
}

export function registerLearnSocialRoutes(app: express.Express, deps: LearnSocialDeps) {
  const censor = deps.censor || ((s: string) => s);
  const uidOf = (req: express.Request) => clip(req.body?.author?.id || req.body?.uid || req.query?.uid || req.headers['x-user-uid'], 120);
  const nameOf = (req: express.Request) => clip(req.body?.author?.name, LIMITS.name) || 'Anonim öğrenci';
  const emit = (deckId: string, type: 'note' | 'thread' | 'message', op: 'insert' | 'update' | 'delete', payload: Record<string, any>) =>
    deps.broadcast('learn_social', { deckId, type, op, ...payload, time: Date.now() });
  const fail = (res: express.Response, status: number, error: string) => res.status(status).json({ error });
  const dbFail = (res: express.Response, e: any) => {
    console.warn('[learnSocial] veritabanı hatası:', e?.message || e);
    return fail(res, 503, 'Ortak notlar şu an kullanılamıyor. Biraz sonra yeniden deneyin.');
  };
  /** Yazma sınırı: IP + kimlik; aşılırsa 429 */
  const rate = (req: express.Request, res: express.Response, kind: string, perMin: number, perHour: number) => {
    // Yönetici (ya da loopback) daha geniş sınır alır ama sınırsız değildir: tünel trafiği de loopback görünür
    const f = deps.isAdmin(req) ? 5 : 1;
    const keys = [`ip:${clientIp(req)}`, `u:${uidOf(req)}`];
    for (const k of keys) {
      if (limited(`${kind}:m:${k}`, perMin * f, 60_000) || limited(`${kind}:h:${k}`, perHour * f, 3_600_000)) {
        fail(res, 429, 'Çok hızlı gönderiyorsun; biraz bekleyip yeniden dene.');
        return true;
      }
    }
    return false;
  };

  app.get('/api/learn/social', async (req, res) => {
    const deckId = clip(req.query.deckId, 160);
    if (!ID_RE.test(deckId)) return fail(res, 400, 'Ders belirtilmedi.');
    const uid = clip(req.query.uid, 120);
    const admin = deps.isAdmin(req);
    try {
      const [notes, threads] = await Promise.all([
        pgPool.query('select * from learn_notes where deck_id = $1 order by step_number, created_at limit 2000', [deckId]),
        pgPool.query('select * from learn_threads where deck_id = $1 order by step_number, created_at limit 1000', [deckId]),
      ]);
      res.setHeader('Cache-Control', 'no-store');
      res.json({
        notes: notes.rows.map((r) => noteView(r, uid, admin)),
        threads: threads.rows.map((r) => threadView(r, uid, admin)),
        isAdmin: admin,
      });
    } catch (e) {
      dbFail(res, e);
    }
  });

  /* ---------------- notlar ---------------- */
  app.post('/api/learn/social/notes', async (req, res) => {
    const deckId = clip(req.body?.deckId, 160);
    const stepNumber = Math.trunc(Number(req.body?.stepNumber));
    const kind = String(req.body?.kind || '') as LearnNoteKind;
    const uid = uidOf(req);
    if (!ID_RE.test(deckId) || !Number.isFinite(stepNumber) || stepNumber < 0 || stepNumber > 10000) return fail(res, 400, 'Geçersiz ders ya da adım.');
    if (!KINDS.has(kind)) return fail(res, 400, 'Not türü SPOT, ÖNEMLİ ya da VURGU olmalı.');
    if (!uid) return fail(res, 400, 'Yazar belirsiz.');
    const body = censor(clipBody(req.body?.body, LIMITS.note));
    if (body.length < 3) return fail(res, 400, 'Not en az 3 karakter olmalı.');
    if (String(req.body?.body || '').trim().length > LIMITS.note) return fail(res, 400, `Not en çok ${LIMITS.note} karakter olabilir.`);
    if (rate(req, res, 'note', 6, 60)) return;
    const anchor = clip(req.body?.anchor, LIMITS.anchor) || null;
    const admin = deps.isAdmin(req);
    try {
      const { rows } = await pgPool.query(
        `insert into learn_notes (id, deck_id, step_number, kind, body, anchor, author_id, author_name)
         values ($1,$2,$3,$4,$5,$6,$7,$8) returning *`,
        [newId('ln'), deckId, stepNumber, kind, body, anchor, uid, nameOf(req)]
      );
      const item = noteView(rows[0], uid, admin);
      emit(deckId, 'note', 'insert', { item: publicView(item) });
      res.json({ success: true, item });
    } catch (e) {
      dbFail(res, e);
    }
  });

  app.delete('/api/learn/social/notes/:id', async (req, res) => {
    const id = clip(req.params.id, 80);
    const uid = uidOf(req);
    const admin = deps.isAdmin(req);
    try {
      const { rows } = await pgPool.query('select id, deck_id, author_id from learn_notes where id = $1', [id]);
      if (!rows[0]) return fail(res, 404, 'Not bulunamadı.');
      if (!admin && (!uid || rows[0].author_id !== uid)) return fail(res, 403, 'Yalnız kendi notunu silebilirsin.');
      await pgPool.query('delete from learn_notes where id = $1', [id]);
      emit(rows[0].deck_id, 'note', 'delete', { id });
      res.json({ success: true });
    } catch (e) {
      dbFail(res, e);
    }
  });

  /* ---------------- bildirim + tartışma ---------------- */
  app.post('/api/learn/social/threads', async (req, res) => {
    const deckId = clip(req.body?.deckId, 160);
    const stepNumber = Math.trunc(Number(req.body?.stepNumber));
    const uid = uidOf(req);
    if (!ID_RE.test(deckId) || !Number.isFinite(stepNumber) || stepNumber < 0 || stepNumber > 10000) return fail(res, 400, 'Geçersiz ders ya da adım.');
    if (!uid) return fail(res, 400, 'Bildiren belirsiz.');
    const quote = clip(req.body?.quote, LIMITS.quote);
    if (quote.length < 4) return fail(res, 400, 'Bildirmek için en az birkaç kelimelik bir metin seç.');
    const body = censor(clipBody(req.body?.body, LIMITS.message));
    if (body.length < 5) return fail(res, 400, 'Metinde neyin yanlış ya da belirsiz olduğunu kısaca yaz (en az 5 karakter).');
    if (rate(req, res, 'thread', 3, 20)) return;
    const admin = deps.isAdmin(req);
    const name = nameOf(req);
    const deckTitle = clip(req.body?.deckTitle, 160) || deckId;
    const client = await pgPool.connect().catch((e) => {
      dbFail(res, e);
      return null;
    });
    if (!client) return;
    try {
      // Aynı adımda aynı metin zaten açık bir tartışmadaysa yeni kayıt açma, mesajı oraya ekle
      await client.query('begin');
      const dup = await client.query(
        `select * from learn_threads where deck_id = $1 and step_number = $2 and quote = $3 and status = 'open' limit 1 for update`,
        [deckId, stepNumber, quote]
      );
      let thread = dup.rows[0];
      const created = !thread;
      if (!thread) {
        const ins = await client.query(
          `insert into learn_threads (id, deck_id, deck_title, step_number, quote, prefix, suffix, reporter_id, reporter_name)
           values ($1,$2,$3,$4,$5,$6,$7,$8,$9) returning *`,
          [newId('lt'), deckId, deckTitle, stepNumber, quote, clip(req.body?.prefix, LIMITS.ctx), clip(req.body?.suffix, LIMITS.ctx), uid, name]
        );
        thread = ins.rows[0];
      }
      const msg = await client.query(
        `insert into learn_thread_messages (id, thread_id, body, author_id, author_name, is_admin) values ($1,$2,$3,$4,$5,$6) returning *`,
        [newId('lm'), thread.id, body, uid, name, admin]
      );
      const upd = await client.query(
        `update learn_threads set message_count = message_count + 1, last_message_at = now() where id = $1 returning *`,
        [thread.id]
      );
      await client.query('commit');
      const item = threadView(upd.rows[0], uid, admin);
      const message = messageView(msg.rows[0], uid, admin);
      emit(deckId, 'thread', created ? 'insert' : 'update', { item: publicView(item) });
      emit(deckId, 'message', 'insert', { threadId: item.id, item: publicView(message) });
      if (created) {
        deps.notifyAdmin({
          questionId: `${deckTitle} · Adım ${stepNumber}`,
          reason: 'Öğren: metin bildirildi',
          details: `Bildirilen metin: “${quote}”\n\n${body}`,
          author: name,
          topic: 'Öğren › Metin bildirimi',
          link: learnThreadLink(deckId, stepNumber, item.id),
        });
      }
      res.json({ success: true, item, message, created });
    } catch (e) {
      await client.query('rollback').catch(() => {});
      dbFail(res, e);
    } finally {
      client.release();
    }
  });

  app.get('/api/learn/social/threads/:id', async (req, res) => {
    const id = clip(req.params.id, 80);
    const uid = clip(req.query.uid, 120);
    const admin = deps.isAdmin(req);
    try {
      const t = await pgPool.query('select * from learn_threads where id = $1', [id]);
      if (!t.rows[0]) return fail(res, 404, 'Tartışma bulunamadı.');
      const m = await pgPool.query('select * from learn_thread_messages where thread_id = $1 order by created_at limit 500', [id]);
      res.setHeader('Cache-Control', 'no-store');
      res.json({ item: threadView(t.rows[0], uid, admin), messages: m.rows.map((r) => messageView(r, uid, admin)) });
    } catch (e) {
      dbFail(res, e);
    }
  });

  app.post('/api/learn/social/threads/:id/messages', async (req, res) => {
    const id = clip(req.params.id, 80);
    const uid = uidOf(req);
    if (!uid) return fail(res, 400, 'Yazar belirsiz.');
    const body = censor(clipBody(req.body?.body, LIMITS.message));
    if (body.length < 1) return fail(res, 400, 'Boş mesaj gönderilemez.');
    if (String(req.body?.body || '').trim().length > LIMITS.message) return fail(res, 400, `Mesaj en çok ${LIMITS.message} karakter olabilir.`);
    if (rate(req, res, 'msg', 10, 120)) return;
    const admin = deps.isAdmin(req);
    try {
      const t = await pgPool.query('select id, deck_id from learn_threads where id = $1', [id]);
      if (!t.rows[0]) return fail(res, 404, 'Tartışma bulunamadı.');
      const msg = await pgPool.query(
        `insert into learn_thread_messages (id, thread_id, body, author_id, author_name, is_admin) values ($1,$2,$3,$4,$5,$6) returning *`,
        [newId('lm'), id, body, uid, nameOf(req), admin]
      );
      const upd = await pgPool.query(
        `update learn_threads set message_count = message_count + 1, last_message_at = now() where id = $1 returning *`,
        [id]
      );
      const item = threadView(upd.rows[0], uid, admin);
      const message = messageView(msg.rows[0], uid, admin);
      emit(t.rows[0].deck_id, 'message', 'insert', { threadId: id, item: publicView(message) });
      emit(t.rows[0].deck_id, 'thread', 'update', { item: publicView(item) });
      res.json({ success: true, message, item });
    } catch (e) {
      dbFail(res, e);
    }
  });

  app.delete('/api/learn/social/messages/:id', async (req, res) => {
    const id = clip(req.params.id, 80);
    const uid = uidOf(req);
    const admin = deps.isAdmin(req);
    try {
      const { rows } = await pgPool.query(
        `select m.id, m.author_id, m.thread_id, t.deck_id from learn_thread_messages m join learn_threads t on t.id = m.thread_id where m.id = $1`,
        [id]
      );
      if (!rows[0]) return fail(res, 404, 'Mesaj bulunamadı.');
      if (!admin && (!uid || rows[0].author_id !== uid)) return fail(res, 403, 'Yalnız kendi mesajını silebilirsin.');
      await pgPool.query('delete from learn_thread_messages where id = $1', [id]);
      const upd = await pgPool.query(
        `update learn_threads set message_count = (select count(*) from learn_thread_messages where thread_id = $1) where id = $1 returning *`,
        [rows[0].thread_id]
      );
      emit(rows[0].deck_id, 'message', 'delete', { threadId: rows[0].thread_id, id });
      if (upd.rows[0]) emit(rows[0].deck_id, 'thread', 'update', { item: publicView(threadView(upd.rows[0], '', false)) });
      res.json({ success: true });
    } catch (e) {
      dbFail(res, e);
    }
  });

  app.post('/api/learn/social/threads/:id/status', async (req, res) => {
    const id = clip(req.params.id, 80);
    const status = req.body?.status === 'resolved' ? 'resolved' : req.body?.status === 'open' ? 'open' : '';
    if (!status) return fail(res, 400, 'Durum open ya da resolved olmalı.');
    const uid = uidOf(req);
    const admin = deps.isAdmin(req);
    try {
      const t = await pgPool.query('select id, deck_id, reporter_id from learn_threads where id = $1', [id]);
      if (!t.rows[0]) return fail(res, 404, 'Tartışma bulunamadı.');
      if (!admin && (!uid || t.rows[0].reporter_id !== uid)) return fail(res, 403, 'Bu bildirimi yalnız bildiren ya da yönetici kapatabilir.');
      const upd = await pgPool.query('update learn_threads set status = $2 where id = $1 returning *', [id, status]);
      const item = threadView(upd.rows[0], uid, admin);
      emit(t.rows[0].deck_id, 'thread', 'update', { item: publicView(item) });
      res.json({ success: true, item });
    } catch (e) {
      dbFail(res, e);
    }
  });

  app.delete('/api/learn/social/threads/:id', async (req, res) => {
    if (!deps.isAdmin(req)) return fail(res, 403, 'Tartışmayı yalnız yönetici silebilir.');
    const id = clip(req.params.id, 80);
    try {
      const { rows } = await pgPool.query('delete from learn_threads where id = $1 returning deck_id', [id]);
      if (!rows[0]) return fail(res, 404, 'Tartışma bulunamadı.');
      emit(rows[0].deck_id, 'thread', 'delete', { id });
      res.json({ success: true });
    } catch (e) {
      dbFail(res, e);
    }
  });
}
