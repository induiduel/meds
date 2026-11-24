/**
 * Erişim kapısı (2026-11-23, kullanıcı kararı): /api/* uçları yalnız Arzu Türk ve yönetici hesabına açıktır.
 *
 * Belirti (neden gerekli): site yalnız bu iki hesaba açılacak; diğer hesaplar hata sayfası görecek ve
 * "veritabanı yüklenmeyecek, içeriklere erişemeyecek". Yalnız istemci ekranı kapamak yetmez: jetonu olan
 * herhangi biri /api/committees, /api/questions, /api/past-exams çağırıp veriyi indirebilirdi.
 *
 * Kural: giriş yapmış ama izinli listede olmayan kullanıcı → 403 { code: 'ERISIM_KAPALI' }.
 *  - Yönetici (MEDS_PANEL_SECRET / loopback / yönetici jetonu) her zaman geçer.
 *  - İzinli e-posta listesi TEK kaynaktan gelir: src/services/erisimSiniri.ts (istemci de aynı listeyi okur).
 *  - Yapay zekâ test çerezi (imzalı, panel anahtarıyla alınır) geçer: site sınama ajanları kapanmasın.
 *  - Açık bırakılan uçlar: kimlik (giriş/kayıt/çıkış — kayıt açık kalacak), bakım durumu, sağlık, sürüm,
 *    istemci hata bildirimi ve yönetici uçları (requireAdmin kendi kapısını uygular).
 */
import type express from 'express';
import { isRequestAdminVerified } from './adminAuth';
import { requestUser } from './kimlikDogrulama';
import { erisimEpostasiIzinli, ERISIM_KAPALI_KODU, ERISIM_KAPALI_MESAJI } from './erisimSiniri';

/** Kapıdan muaf yollar (kimlik ve tanı uçları; veri döndürmezler) */
const MUAF = [
  /^\/api\/kimlik\//,
  /^\/api\/bakim$/,
  /^\/api\/health(\/|$)/,
  /^\/api\/surum(\/|$)/,
  /^\/api\/site-ayar(\/|$)/, // herkese açık çalışma anı ayarı (gizli sayfa/bayrak); veri döndürmez
  /^\/api\/istemci-hata(\/|$)/,
  /^\/api\/olcum(\/|$)/,
  /^\/api\/ai-test(\/|$)/,
  /^\/api\/me\/access$/, // yalnız kendi rolünü döndürür; istemci moderatörü buradan tanır (2026-11-24)
];

/** Yönetici uçları kendi kimlik kapısını uygular; burada erken 403 ile paneli kilitlemeyiz */
const YONETICI = /^\/api\/admin(\/|$)/;

export function erisimKapisi(opts: {
  aiTestGecerli?: (req: express.Request) => boolean;
  /** 2026-11-24: kullanıcı kaydında rolü moderatör/yönetici olan (askıda değil) hesap da geçer */
  rolIzinli?: (uid: string, email: string) => boolean;
} = {}): express.RequestHandler {
  const izinli = (u: { uid?: string; email?: string | null } | null | undefined): boolean => {
    if (!u) return false;
    if (erisimEpostasiIzinli(u.email)) return true;
    try { return !!(u.uid && opts.rolIzinli?.(u.uid, String(u.email || '').trim().toLowerCase())); } catch { return false; }
  };
  /**
   * İstek kimliğini bir kez çözeriz; express.json'dan SONRA kayıtlıdır ki gövde kullanılabilsin.
   * Jeton kimlikDogrulama'da yerel HMAC ile doğrulanır (dış servise gidilmez).
   */
  return (req, res, next) => {
    if (!req.path.startsWith('/api/')) return next();
    if (MUAF.some((r) => r.test(req.path))) return next();
    if (YONETICI.test(req.path)) return next();
    if (isRequestAdminVerified(req, 'nofrostlife@gmail.com')) return next();
    try { if (opts.aiTestGecerli?.(req)) return next(); } catch { /* çerez bozuksa kapı normal işler */ }

    // adminAuthMiddleware zaten çözdüyse onu kullan; çözmediyse burada doğrula (ör. jeton sonradan eklendi)
    const bilinen = (req as any).verifiedUser;
    if (bilinen && izinli(bilinen)) return next();

    requestUser(req)
      .then((who) => {
        if (who.user && izinli(who.user)) return next();
        // Jeton geçersiz/iptal: istemci yeniden giriş yapmalı (invalid) — gövdede ayrıca söylenir
        return res.status(403).json({
          success: false,
          error: ERISIM_KAPALI_MESAJI,
          code: ERISIM_KAPALI_KODU,
          ...(who.invalid ? { invalid: true } : {}),
        });
      })
      .catch(() => res.status(403).json({ success: false, error: ERISIM_KAPALI_MESAJI, code: ERISIM_KAPALI_KODU }));
  };
}
