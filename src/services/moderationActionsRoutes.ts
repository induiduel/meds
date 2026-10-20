/**
 * Moderasyon eylemleri (yönetim): kişiye ata, etiket, reddet, öğrenciye yanıt, ertele, moderasyona aktar.
 *
 * Veri, bildirimlerin/yorumların kendisine dokunmadan yan kayıtta tutulur: data/moderation_actions.json
 * ({ items: { [kimlik]: ModerationMeta } }). Kimlik; hata bildirimi, yorum ya da otomatik onarım kaydının
 * kimliğidir. Tüm alanlar isteğe bağlıdır; eski kayıtlar olduğu gibi çalışır. Dosya boş/okunamaz ise
 * üzerine boş liste yazılmaz (yazma reddedilir).
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import type express from 'express';

export interface ModerationReply {
  text: string;
  at: string;
  by: string;
  delivered: boolean;
}

export interface ModerationMeta {
  id: string;
  kind?: string;
  assignee?: string;
  tags?: string[];
  rejected?: { reason: string; at: string; by: string } | null;
  snoozedUntil?: string | null;
  escalated?: { at: string; by: string } | null;
  replies?: ModerationReply[];
  updatedAt?: string;
}

export interface ModerationTarget {
  uid?: string | null;
  email?: string | null;
  name?: string | null;
  questionId?: string | null;
}

export interface ModerationActionDeps {
  dataDir: string;
  requireAdmin: express.RequestHandler;
  /** Yönetici kimliği (atama "Bana", kayıtta "by") */
  actorOf: (req: express.Request) => string;
  /** Bildirim/yorum/onarım kimliğinden öğrenci hedefini bulur (yanıt için) */
  findTarget: (id: string) => ModerationTarget | null;
  notifyStudent: (
    target: { uid?: string | null; email?: string | null },
    n: { type: string; title: string; message: string; deepLinkUrl?: string; targetType?: string; targetId?: string; dedupeKey?: string },
  ) => boolean;
  broadcastAdmin: (event: string, data: any) => void;
}

type Store = { items: Record<string, ModerationMeta> };

const ACTIONS = new Set(['assign', 'tags', 'add_tags', 'remove_tags', 'reject', 'reopen', 'reply', 'snooze', 'unsnooze', 'escalate', 'unescalate']);
const MAX_IDS = 500;

export function registerModerationActionRoutes(app: express.Express, deps: ModerationActionDeps) {
  const file = path.join(deps.dataDir, 'moderation_actions.json');

  const read = (): Store | null => {
    try {
      if (!fs.existsSync(file)) return { items: {} };
      const raw = fs.readFileSync(file, 'utf-8');
      if (!raw.trim()) return null;
      const parsed = JSON.parse(raw);
      if (!parsed || typeof parsed !== 'object' || typeof parsed.items !== 'object') return null;
      return parsed as Store;
    } catch {
      return null;
    }
  };

  const write = (store: Store) => {
    const tmp = `${file}.${process.pid}.tmp`;
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(tmp, JSON.stringify(store, null, 2));
    fs.renameSync(tmp, file);
  };

  const cleanTags = (v: unknown): string[] =>
    (Array.isArray(v) ? v : String(v || '').split(','))
      .map((t) => String(t || '').trim().slice(0, 40))
      .filter(Boolean)
      .slice(0, 20);

  app.get('/api/admin/moderation/meta', deps.requireAdmin, (_req, res) => {
    const store = read();
    if (!store) return res.status(500).json({ error: 'Moderasyon kaydı okunamadı.' });
    res.json({ items: store.items });
  });

  app.post('/api/admin/moderation/actions', deps.requireAdmin, (req, res) => {
    const body = req.body || {};
    const action = String(body.action || '');
    if (!ACTIONS.has(action)) return res.status(400).json({ error: 'Bilinmeyen eylem.' });
    const ids: string[] = (Array.isArray(body.ids) ? body.ids : [body.id])
      .map((x: unknown) => String(x || '').trim())
      .filter((x: string) => x && x.length <= 200);
    if (!ids.length) return res.status(400).json({ error: 'En az bir kayıt seçilmeli.' });
    if (ids.length > MAX_IDS) return res.status(400).json({ error: `Tek seferde en çok ${MAX_IDS} kayıt işlenir.` });

    const text = String(body.text ?? body.reason ?? '').trim().slice(0, 2000);
    if (action === 'reply' && !text) {
      return res.status(400).json({ error: 'Yanıt metni boş olamaz.' });
    }
    if (action === 'reject' && !text) return res.status(400).json({ error: 'Ret gerekçesi yazılmalı.' });
    let snoozeIso = '';
    if (action === 'snooze') {
      const d = new Date(String(body.until || ''));
      if (Number.isNaN(d.getTime()) || d.getTime() <= Date.now()) return res.status(400).json({ error: 'Erteleme tarihi ileri bir zaman olmalı.' });
      snoozeIso = d.toISOString();
    }

    const store = read();
    if (!store) return res.status(500).json({ error: 'Moderasyon kaydı okunamadı; veri korunması için yazılmadı.' });

    const by = deps.actorOf(req);
    const now = new Date().toISOString();
    const kind = body.kind ? String(body.kind).slice(0, 30) : undefined;
    const results: { id: string; ok: boolean; error?: string }[] = [];

    for (const id of ids) {
      const m: ModerationMeta = { ...(store.items[id] || { id }), id };
      if (kind && !m.kind) m.kind = kind;
      let ok = true;
      let error: string | undefined;
      switch (action) {
        case 'assign': {
          const who = String(body.assignee || '').trim().slice(0, 120);
          if (who) m.assignee = who;
          else delete m.assignee;
          break;
        }
        case 'tags':
          m.tags = cleanTags(body.tags);
          break;
        case 'add_tags':
          m.tags = Array.from(new Set([...(m.tags || []), ...cleanTags(body.tags)])).slice(0, 20);
          break;
        case 'remove_tags': {
          const drop = new Set(cleanTags(body.tags).map((t) => t.toLocaleLowerCase('tr-TR')));
          m.tags = (m.tags || []).filter((t) => !drop.has(t.toLocaleLowerCase('tr-TR')));
          break;
        }
        case 'reject': {
          m.rejected = { reason: text, at: now, by };
          if (body.notify) {
            const t = deps.findTarget(id);
            const delivered = !!t && (t.uid || t.email)
              ? deps.notifyStudent(
                  { uid: t.uid || null, email: t.email || null },
                  {
                    type: 'report_rejected',
                    title: 'Bildiriminiz incelendi',
                    message: `Bildiriminiz incelendi ve değişiklik gerekmediğine karar verildi. Gerekçe: ${text}`,
                    targetType: 'report',
                    targetId: id,
                    dedupeKey: `report_rejected:${id}`,
                  },
                )
              : false;
            m.replies = [...(m.replies || []), { text: `Ret gerekçesi: ${text}`, at: now, by, delivered }];
            if (!delivered) error = 'Reddedildi; öğrenci profili bulunamadığı için bildirim gitmedi.';
          }
          break;
        }
        case 'reopen':
          m.rejected = null;
          break;
        case 'reply': {
          const t = deps.findTarget(id);
          const delivered = !!t && !!(t.uid || t.email)
            ? deps.notifyStudent(
                { uid: t.uid || null, email: t.email || null },
                {
                  type: 'report_reply',
                  title: 'Bildiriminize yanıt var',
                  message: text,
                  targetType: 'report',
                  targetId: id,
                  dedupeKey: `report_reply:${id}:${crypto.createHash('sha1').update(text + now).digest('hex').slice(0, 10)}`,
                },
              )
            : false;
          m.replies = [...(m.replies || []), { text, at: now, by, delivered }].slice(-50);
          if (!delivered) { ok = false; error = 'Öğrenci profili bulunamadı; yanıt kayda alındı ama iletilemedi.'; }
          break;
        }
        case 'snooze':
          m.snoozedUntil = snoozeIso;
          break;
        case 'unsnooze':
          m.snoozedUntil = null;
          break;
        case 'escalate':
          m.escalated = { at: now, by };
          break;
        case 'unescalate':
          m.escalated = null;
          break;
      }
      m.updatedAt = now;
      store.items[id] = m;
      results.push({ id, ok, ...(error ? { error } : {}) });
    }

    try {
      write(store);
    } catch (e: any) {
      return res.status(500).json({ error: 'Moderasyon kaydı yazılamadı: ' + (e?.message || e) });
    }
    const updated: Record<string, ModerationMeta> = {};
    for (const id of ids) updated[id] = store.items[id];
    deps.broadcastAdmin('moderation_meta_changed', { ids, action, time: Date.now() });
    deps.broadcastAdmin('inbox_update', { type: 'moderation_action', action, time: Date.now() });
    res.json({ success: true, items: updated, results });
  });
}
