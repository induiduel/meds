/**
 * Moderatör erişimi: yalnız içerik moderasyonu uçlarına dar izin.
 *
 * Kural: istek doğrulanmış bir Firebase kimlik jetonu (Authorization: Bearer) taşımalı; jetonun kullanıcısı
 * data/users.json'da role 'moderator' (ya da 'admin') kaydına sahip olmalı ve hesabı askıda olmamalı.
 * x-admin-email başlığına ya da gövdedeki e-postaya asla güvenilmez.
 *
 * `requireModeratorOrAdmin` YALNIZ moderasyon rotalarına konur (bildirim/yorum çözme, sorudan düzeltme, taslak
 * yayın/birleştirme, /api/admin/moderation/*, otomatik onarım okuma/geri alma). Kullanıcılar, Kişiler, roller,
 * veritabanı gezgini, servis, hat, betik, otomasyon, yedek, ayarlar ve veri kataloğu toplu silmeleri moderatöre
 * hiçbir zaman açılmaz: o rotalar `requireAdmin`/`isStrongAdmin` ile kalır.
 *
 * Her moderatör yazması (GET dışı) data/moderator_audit.jsonl dosyasına eklenir (kim, ne, ne zaman, sonuç kodu).
 */
import fs from 'fs';
import path from 'path';
import type express from 'express';
import { requestUser } from './firebaseIdentity';
import { suspensionActive } from './userAdminRoutes';

type Any = Record<string, any>;
const lc = (v: unknown) => String(v ?? '').trim().toLowerCase();

export interface ModeratorIdentity {
  uid: string;
  email: string;
  role: 'moderator' | 'admin';
}

export interface ModeratorAccessDeps {
  dataDir: string;
  adminEmail: string;
  loadUsers: () => Any[];
  /** Mevcut yönetici denetimi (değiştirilmeden önce geçer) */
  isAdmin: (req: express.Request) => boolean;
}

const MOD_KEY = '__medsModerator';

/** Rota içinde: isteği moderatör yaptıysa kimliği (yönetici isteklerinde null) */
export function moderatorOf(req: express.Request): ModeratorIdentity | null {
  return ((req as any)[MOD_KEY] as ModeratorIdentity | undefined) || null;
}

export function createModeratorAccess(deps: ModeratorAccessDeps) {
  const owner = lc(deps.adminEmail);
  const auditFile = path.join(deps.dataDir, 'moderator_audit.jsonl');

  /** Doğrulanmış jeton + kayıtta moderatör/yönetici rolü + askıda değil */
  async function isModerator(req: express.Request): Promise<ModeratorIdentity | null> {
    let who;
    try {
      who = await requestUser(req);
    } catch {
      return null;
    }
    const user = who?.user;
    if (!user?.uid) return null;
    const email = lc(user.email);
    if (email && email === owner) return { uid: user.uid, email, role: 'admin' };
    let rec: Any | undefined;
    try {
      rec = (deps.loadUsers() || []).find((u) => u && (u.uid === user.uid || (email && lc(u.email) === email)));
    } catch {
      return null;
    }
    if (!rec) return null;
    if (rec.role !== 'moderator' && rec.role !== 'admin') return null;
    if (suspensionActive(rec.suspension)) return null;
    return { uid: user.uid, email, role: rec.role };
  }

  function audit(entry: Any) {
    try {
      fs.mkdirSync(path.dirname(auditFile), { recursive: true });
      fs.appendFileSync(auditFile, JSON.stringify(entry) + '\n');
    } catch (e: any) {
      console.warn('[Moderatör denetim kaydı] yazılamadı:', e?.message || e);
    }
  }

  const bodySummary = (b: unknown) => {
    if (!b || typeof b !== 'object') return undefined;
    const o = b as Any;
    return {
      keys: Object.keys(o).slice(0, 40),
      ...(Array.isArray(o.ids) ? { ids: o.ids.slice(0, 50).map(String) } : {}),
      ...(typeof o.action === 'string' ? { action: o.action.slice(0, 40) } : {}),
      ...(o.questionId ? { questionId: String(o.questionId).slice(0, 120) } : {}),
      ...(Array.isArray(o.mergedIds) ? { mergedIds: o.mergedIds.slice(0, 50).map(String) } : {}),
      ...(o.status ? { status: String(o.status).slice(0, 40) } : {}),
    };
  };

  /** Yöneticiye her zamanki gibi açık; ek olarak doğrulanmış moderatöre. Moderatör yazmaları denetim kaydına gider. */
  const requireModeratorOrAdmin: express.RequestHandler = (req, res, next) => {
    if (deps.isAdmin(req)) return next();
    void isModerator(req).then((mod) => {
      if (!mod) {
        return res.status(403).json({
          success: false,
          error: 'Bu işlem için yetkiniz yok. Moderatör ya da yönetici hesabıyla giriş yapmalısınız.',
          code: 'MODERATOR_REQUIRED',
        });
      }
      (req as any)[MOD_KEY] = mod;
      if (req.method !== 'GET' && req.method !== 'HEAD' && req.method !== 'OPTIONS') {
        const at = new Date().toISOString();
        res.on('finish', () =>
          audit({
            at,
            uid: mod.uid,
            email: mod.email,
            role: mod.role,
            method: req.method,
            path: String(req.originalUrl || req.url || '').split('?')[0].slice(0, 300),
            params: req.params,
            body: bodySummary(req.body),
            status: res.statusCode,
          }),
        );
      }
      next();
    }, () => res.status(403).json({ success: false, error: 'Kimlik doğrulanamadı.', code: 'MODERATOR_REQUIRED' }));
  };

  return { isModerator, requireModeratorOrAdmin, moderatorOf };
}
