/**
 * WhatsApp Meta Cloud API (Graph API) Servisi ve Günlük Tekrar Dağıtıcısı
 *
 * Öğrencinin yıldızladığı (beğendiği) paragrafları, favori bilgi kartlarını ve
 * favori sorularını Meta WhatsApp Cloud API üzerinden kullanıcının belirttiği
 * telefon numarasına günlük olarak gönderir.
 */

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import type express from 'express';
import { requestUser } from './firebaseIdentity';

export interface WhatsAppPrefs {
  enabled: boolean;
  phone: string; // e.g. "905321234567"
  hour: number; // 0..23, default 21
  includeStarredParagraphs: boolean; // default true
  includeFavoriteCards: boolean; // default true
  includeFavoriteQuestions: boolean; // default false
  paragraphCount: number; // 1..3, default 1
  cardCount: number; // 1..3, default 1
  lastSentDate?: string; // "YYYY-MM-DD"
  lastStatus?: {
    at: string;
    success: boolean;
    message?: string;
  };
}

export const WHATSAPP_PREFS_KEY = 'medsoru_whatsapp_prefs_v1';

export interface WhatsAppConfig {
  phoneNumberId?: string;
  accessToken?: string;
  businessAccountId?: string;
  templateName?: string;
  apiVersion: string;
}

export function getWhatsAppConfig(): WhatsAppConfig {
  return {
    phoneNumberId: process.env.WHATSAPP_PHONE_NUMBER_ID?.trim() || undefined,
    accessToken: process.env.WHATSAPP_ACCESS_TOKEN?.trim() || undefined,
    businessAccountId: process.env.WHATSAPP_BUSINESS_ACCOUNT_ID?.trim() || undefined,
    templateName: process.env.WHATSAPP_TEMPLATE_NAME?.trim() || undefined,
    apiVersion: process.env.WHATSAPP_API_VERSION?.trim() || 'v21.0',
  };
}

export function isWhatsAppConfigured(): boolean {
  const cfg = getWhatsAppConfig();
  return Boolean(cfg.phoneNumberId && cfg.accessToken);
}

/**
 * Telefon numarasını E.164 uluslararası biçime (başında + olmadan Meta formatına) dönüştürür.
 * Örnekler:
 * "0532 123 45 67" -> "905321234567"
 * "5321234567"     -> "905321234567"
 * "+905321234567"  -> "905321234567"
 */
export function normalizePhoneNumber(raw: string): string | null {
  if (!raw) return null;
  const digits = raw.replace(/\D/g, '');
  if (!digits) return null;

  // Türkiye için 05xx... (11 hane)
  if (digits.length === 11 && digits.startsWith('0')) {
    return `90${digits.slice(1)}`;
  }
  // Türkiye için 5xx... (10 hane)
  if (digits.length === 10 && digits.startsWith('5')) {
    return `90${digits}`;
  }
  // Zaten 905xx... (12 hane)
  if (digits.length === 12 && digits.startsWith('90')) {
    return digits;
  }
  // Diğer ülke kodları (10 - 15 hane arası)
  if (digits.length >= 10 && digits.length <= 15) {
    return digits;
  }

  return null;
}

/**
 * Meta WhatsApp Cloud API ile metin mesajı gönderir.
 */
export async function sendMetaTextMessage(
  to: string,
  bodyText: string
): Promise<{ success: boolean; messageId?: string; error?: string; raw?: any }> {
  const cfg = getWhatsAppConfig();
  if (!cfg.phoneNumberId || !cfg.accessToken) {
    return {
      success: false,
      error: 'WhatsApp Meta Cloud API yapılandırılmamış. WHATSAPP_PHONE_NUMBER_ID ve WHATSAPP_ACCESS_TOKEN ortam değişkenlerini tanımlayın.',
    };
  }

  const cleanPhone = normalizePhoneNumber(to);
  if (!cleanPhone) {
    return {
      success: false,
      error: `Geçersiz telefon numarası: "${to}". Lütfen geçerli bir cep telefonu numarası girin.`,
    };
  }

  const url = `https://graph.facebook.com/${cfg.apiVersion}/${cfg.phoneNumberId}/messages`;

  const payload = {
    messaging_product: 'whatsapp',
    recipient_type: 'individual',
    to: cleanPhone,
    type: 'text',
    text: {
      preview_url: true,
      body: bodyText,
    },
  };

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${cfg.accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data: any = await res.json().catch(() => null);

    if (!res.ok) {
      const errMsg =
        data?.error?.message ||
        `WhatsApp API hatası (${res.status} ${res.statusText})`;
      const errCode = data?.error?.code;

      let detail = errMsg;
      if (errCode === 131047) {
        detail +=
          ' (24 saatlik müşteri yanıt penceresi dışındaki gönderimler için Meta panelinde onaylı bir şablon gerekir veya kullanıcı son 24 saatte numaranıza mesaj göndermiş olmalıdır.)';
      }

      return {
        success: false,
        error: detail,
        raw: data,
      };
    }

    const messageId = data?.messages?.[0]?.id;
    return {
      success: true,
      messageId,
      raw: data,
    };
  } catch (err: any) {
    return {
      success: false,
      error: err?.message || 'Ağ hatası: WhatsApp API sunucusuna erişilemedi.',
    };
  }
}

/**
 * Şablon destekli Meta WhatsApp mesajı gönderir (eğer onaylı şablon varsa).
 */
export async function sendMetaTemplateMessage(
  to: string,
  templateName: string,
  languageCode = 'tr',
  parameters: string[] = []
): Promise<{ success: boolean; messageId?: string; error?: string; raw?: any }> {
  const cfg = getWhatsAppConfig();
  if (!cfg.phoneNumberId || !cfg.accessToken) {
    return {
      success: false,
      error: 'WhatsApp Meta Cloud API yapılandırılmamış.',
    };
  }

  const cleanPhone = normalizePhoneNumber(to);
  if (!cleanPhone) {
    return {
      success: false,
      error: `Geçersiz telefon numarası: "${to}".`,
    };
  }

  const url = `https://graph.facebook.com/${cfg.apiVersion}/${cfg.phoneNumberId}/messages`;

  const components: any[] = [];
  if (parameters.length > 0) {
    components.push({
      type: 'body',
      parameters: parameters.map((p) => ({ type: 'text', text: p })),
    });
  }

  const payload = {
    messaging_product: 'whatsapp',
    recipient_type: 'individual',
    to: cleanPhone,
    type: 'template',
    template: {
      name: templateName,
      language: {
        code: languageCode,
      },
      components: components.length ? components : undefined,
    },
  };

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${cfg.accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data: any = await res.json().catch(() => null);

    if (!res.ok) {
      return {
        success: false,
        error: data?.error?.message || `WhatsApp şablon hatası (${res.status})`,
        raw: data,
      };
    }

    return {
      success: true,
      messageId: data?.messages?.[0]?.id,
      raw: data,
    };
  } catch (err: any) {
    return {
      success: false,
      error: err?.message || 'Ağ hatası: WhatsApp şablonu gönderilemedi.',
    };
  }
}

/**
 * Kullanıcı verisinden (yıldızlı paragraflar, kartlar, sorular) günlük WhatsApp tekrar mesajı üretir.
 */
export function buildDailyDigestMessage(
  userBundle: any,
  prefs: WhatsAppPrefs,
  allPastQuestions?: any[]
): { text: string; hasContent: boolean } {
  const name = userBundle?.displayName || 'Öğrencimiz';
  const appUrl = (process.env.APP_URL || 'https://medsor.app').replace(/\/+$/, '');

  // 1. Yıldızlı Paragraflar
  let starredParagraphs: any[] = [];
  try {
    const rawKv = userBundle?.kv?.medsoru_yildizli_paragraflar_v1?.v || userBundle?.kv?.medsoru_yildizli_paragraflar?.v;
    if (rawKv) {
      const parsed = typeof rawKv === 'string' ? JSON.parse(rawKv) : rawKv;
      if (Array.isArray(parsed)) starredParagraphs = parsed.filter((p: any) => p && !p.silindi);
    }
  } catch {}

  // 2. Favori Bilgi Kartları
  const cardFavorites: any[] = Array.isArray(userBundle?.stats?.cardFavorites)
    ? userBundle.stats.cardFavorites
    : [];

  // 3. Favori Sorular
  const favoriteQIds: string[] = Array.isArray(userBundle?.stats?.favorites)
    ? userBundle.stats.favorites
    : [];

  const sections: string[] = [];

  // Paragraf ekleme
  if (prefs.includeStarredParagraphs && starredParagraphs.length > 0) {
    const pCount = Math.max(1, Math.min(3, prefs.paragraphCount || 1));
    // Rastgele veya dönüşümlü seçim
    const shuffled = [...starredParagraphs].sort(() => 0.5 - Math.random()).slice(0, pCount);

    shuffled.forEach((p, idx) => {
      const numLabel = pCount > 1 ? ` #${idx + 1}` : '';
      let sec = `📌 *YILDIZLI PARAGRAF${numLabel}*\n`;
      if (p.baslik) sec += `*${p.baslik}*${p.altBaslik ? ` — ${p.altBaslik}` : ''}\n`;
      sec += `> "${(p.metin || '').trim()}"\n`;
      if (p.deeplink) {
        const link = p.deeplink.startsWith('http') ? p.deeplink : `${appUrl}${p.deeplink.startsWith('/') ? '' : '/'}${p.deeplink}`;
        sec += `🔗 _Uygulamada git:_ ${link}`;
      }
      sections.push(sec);
    });
  }

  // Bilgi Kartı ekleme
  if (prefs.includeFavoriteCards && cardFavorites.length > 0) {
    const cCount = Math.max(1, Math.min(3, prefs.cardCount || 1));
    const shuffled = [...cardFavorites].sort(() => 0.5 - Math.random()).slice(0, cCount);

    shuffled.forEach((c, idx) => {
      const numLabel = cCount > 1 ? ` #${idx + 1}` : '';
      let sec = `💡 *FAVORİ BİLGİ KARTI${numLabel}*\n`;
      if (c.group) sec += `_${c.group}_\n`;
      sec += `❓ *Soru:* ${c.front}\n`;
      sec += `👉 *Cevap:* ${c.back}`;
      sections.push(sec);
    });
  }

  // Soru ekleme
  if (prefs.includeFavoriteQuestions && favoriteQIds.length > 0 && Array.isArray(allPastQuestions)) {
    const match = allPastQuestions.find((q) => favoriteQIds.includes(String(q.id)));
    if (match) {
      let sec = `📝 *FAVORİ ÇIKMIŞ SORU*\n`;
      sec += `_${[match.discipline, match.year].filter(Boolean).join(' · ')}_\n`;
      sec += `*Soru:* ${(match.stem || match.question || '').slice(0, 300)}\n`;
      if (match.correct_answer || match.correctAnswer) {
        sec += `✅ *Doğru Cevap:* ${match.correct_answer || match.correctAnswer}\n`;
      }
      if (match.explanation) {
        sec += `💡 *Açıklama:* ${match.explanation.slice(0, 300)}`;
      }
      sections.push(sec);
    }
  }

  const todayStr = new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' });

  if (sections.length === 0) {
    const emptyText =
      `📚 *MeDSor Günlük Tekrar Bildirimi*\n` +
      `📅 ${todayStr}\n\n` +
      `Merhaba *${name}*! 👋\n\n` +
      `Bugün için kayıtlı yıldızlı paragrafın veya favori kartın bulunmuyor.\n\n` +
      `💡 *İpucu:* Sesli Ders, Sınav Asistanı veya Soru Çözücü ekranlarında önemli gördüğün yerleri ⭐ yıldıza dokunarak kaydedebilirsin. Yıldızladığın notlar her gün bu saatte tekrar olarak sana gelecektir!\n\n` +
      `🔗 *Çalışmaya Başla:* ${appUrl}`;
    return { text: emptyText, hasContent: false };
  }

  const messageText =
    `🩺 *MeDSor Günlük Tekrarınız* 📚\n` +
    `📅 ${todayStr}\n\n` +
    `Merhaba *${name}*, bugün tekrar etmen için favorilerinden seçtiğimiz notlar:\n\n` +
    sections.join('\n\n───────────────\n\n') +
    `\n\n───────────────\n` +
    `✨ _İyi çalışmalar dileriz!_\n` +
    `🌐 MeDSor — ${appUrl}`;

  return { text: messageText, hasContent: true };
}

/**
 * Tek bir kullanıcı için günlük tekrarı gönderir.
 */
export async function sendDailyDigestForUser(
  userBundle: any,
  prefs: WhatsAppPrefs,
  allPastQuestions?: any[]
): Promise<{ success: boolean; error?: string; messageId?: string }> {
  if (!prefs.enabled) {
    return { success: false, error: 'Kullanıcının WhatsApp bildirimleri kapalı.' };
  }

  const phone = normalizePhoneNumber(prefs.phone);
  if (!phone) {
    return { success: false, error: 'Geçerli bir telefon numarası bulunamadı.' };
  }

  const { text } = buildDailyDigestMessage(userBundle, prefs, allPastQuestions);

  const res = await sendMetaTextMessage(phone, text);
  return res;
}

/**
 * Sunucuda çalışan periyodik günlük kontrol (Cron / Interval).
 * Her saat başında çalışarak saati gelen kullanıcıların günlük tekrarını yollar.
 */
export async function runScheduledWhatsAppDigests(deps: {
  dataDir: string;
  getPastQuestions: () => any[];
}): Promise<{ checked: number; sent: number; errors: number }> {
  if (!isWhatsAppConfigured()) {
    return { checked: 0, sent: 0, errors: 0 };
  }

  const userBackupsDir = path.join(deps.dataDir, 'user_backups');
  if (!fs.existsSync(userBackupsDir)) {
    return { checked: 0, sent: 0, errors: 0 };
  }

  // Türkiye saatine göre gün ve saat (UTC+3)
  const now = new Date();
  const trHour = parseInt(
    new Intl.DateTimeFormat('tr-TR', { hour: 'numeric', hour12: false, timeZone: 'Europe/Istanbul' }).format(now),
    10
  );
  const todayStr = new Intl.DateTimeFormat('tr-TR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    timeZone: 'Europe/Istanbul',
  })
    .format(now)
    .split('.')
    .reverse()
    .join('-'); // YYYY-MM-DD

  let checked = 0;
  let sent = 0;
  let errors = 0;

  try {
    const files = fs.readdirSync(userBackupsDir).filter((f) => f.endsWith('.json'));

    for (const f of files) {
      checked++;
      const filePath = path.join(userBackupsDir, f);
      try {
        const raw = fs.readFileSync(filePath, 'utf-8');
        const bundle = JSON.parse(raw);

        // WhatsApp tercihini oku
        let prefs: WhatsAppPrefs | null = null;
        const kvVal = bundle?.kv?.[WHATSAPP_PREFS_KEY]?.v;
        if (kvVal) {
          prefs = typeof kvVal === 'string' ? JSON.parse(kvVal) : kvVal;
        }

        if (!prefs || !prefs.enabled || !prefs.phone) {
          continue;
        }

        // Gönderim saati eşleşiyor mu? (Varsayılan: 21:00)
        const targetHour = typeof prefs.hour === 'number' ? prefs.hour : 21;
        if (targetHour !== trHour) {
          continue;
        }

        // Bugün zaten gönderildi mi?
        if (prefs.lastSentDate === todayStr) {
          continue;
        }

        // Gönder
        const result = await sendDailyDigestForUser(bundle, prefs, deps.getPastQuestions());

        // Durumu kaydet
        prefs.lastSentDate = todayStr;
        prefs.lastStatus = {
          at: new Date().toISOString(),
          success: result.success,
          message: result.error || 'Başarıyla gönderildi',
        };

        if (result.success) {
          sent++;
          console.log(`[WhatsApp] Günlük tekrar gönderildi: ${prefs.phone} (${bundle.displayName || 'İsimsiz'})`);
        } else {
          errors++;
          console.warn(`[WhatsApp] Gönderim başarısız: ${prefs.phone} - ${result.error}`);
        }

        // Paketi güncelle
        if (!bundle.kv) bundle.kv = {};
        bundle.kv[WHATSAPP_PREFS_KEY] = {
          v: JSON.stringify(prefs),
          at: new Date().toISOString(),
        };

        fs.writeFileSync(filePath, JSON.stringify(bundle, null, 2), 'utf-8');
      } catch (err: any) {
        console.error(`[WhatsApp] Kullanıcı yedek işleme hatası (${f}):`, err?.message || err);
      }
    }
  } catch (err: any) {
    console.error('[WhatsApp] Zamanlanmış görev taranırken hata:', err?.message || err);
  }

  return { checked, sent, errors };
}

/**
 * Express HTTP rotalarını kaydeder.
 */
export function registerWhatsAppRoutes(
  app: express.Express,
  deps: {
    dataDir: string;
    getPastQuestions: () => any[];
    mirrorUserToDb?: (user: any) => Promise<void>;
  }
) {
  // 1. WhatsApp API Yapılandırma Durumu
  app.get('/api/whatsapp/status', (_req, res) => {
    const cfg = getWhatsAppConfig();
    const isConfigured = Boolean(cfg.phoneNumberId && cfg.accessToken);
    res.json({
      configured: isConfigured,
      phoneNumberIdMasked: cfg.phoneNumberId
        ? `${cfg.phoneNumberId.slice(0, 4)}...${cfg.phoneNumberId.slice(-4)}`
        : null,
      templateConfigured: Boolean(cfg.templateName),
      templateName: cfg.templateName || null,
      apiVersion: cfg.apiVersion,
    });
  });

  // 2. Test Mesajı Gönder (Anında)
  app.post('/api/whatsapp/test', async (req, res) => {
    try {
      const { phone } = req.body;
      const cleanPhone = normalizePhoneNumber(phone);
      if (!cleanPhone) {
        return res.status(400).json({
          success: false,
          error: 'Lütfen geçerli bir telefon numarası girin (örn. 0532 123 45 67).',
        });
      }

      const text =
        `👋 *MeDSor WhatsApp Bağlantı Testi*\n\n` +
        `Tebrikler! WhatsApp bildirim entegrasyonunuz başarıyla çalışıyor. 🩺✨\n\n` +
        `Yıldızladığınız paragraflar ve favori bilgi kartlarınız her gün belirlediğiniz saatte bu numaraya iletilecektir.\n\n` +
        `İyi çalışmalar dileriz! 🚀`;

      const result = await sendMetaTextMessage(cleanPhone, text);

      if (!result.success) {
        return res.status(502).json({
          success: false,
          error: result.error,
          raw: result.raw,
        });
      }

      res.json({
        success: true,
        message: 'Test mesajı WhatsApp üzerinden başarıyla iletildi.',
        messageId: result.messageId,
      });
    } catch (err: any) {
      res.status(500).json({ success: false, error: err?.message || 'Sunucu hatası' });
    }
  });

  // 3. Günün Tekrarını Şimdi Gönder (Önizleme / Anında Tetikleme)
  app.post('/api/whatsapp/send-digest-now', async (req, res) => {
    try {
      const auth = await requestUser(req).catch(() => null);
      const { phone, prefs: customPrefs } = req.body;

      let targetBundle: any = null;

      // Kullanıcının yedeğini bul
      const uid = auth?.user?.uid;
      const email = auth?.user?.email;
      if (uid) {
        const hash = crypto.createHash('sha256').update(uid).digest('hex');
        const backupFile = path.join(deps.dataDir, 'user_backups', `${hash}.json`);
        if (fs.existsSync(backupFile)) {
          try {
            targetBundle = JSON.parse(fs.readFileSync(backupFile, 'utf-8'));
          } catch {}
        }
      }

      // Kullanıcı yedeği yoksa gelen gövdeden veya örnek veriden derle
      if (!targetBundle) {
        targetBundle = {
          displayName: email ? email.split('@')[0] : 'Öğrencimiz',
          kv: req.body.kv || {},
          stats: req.body.stats || {},
        };
      }

      const effectivePrefs: WhatsAppPrefs = {
        enabled: true,
        phone: phone || targetBundle?.kv?.[WHATSAPP_PREFS_KEY]?.v?.phone || '',
        hour: customPrefs?.hour ?? 21,
        includeStarredParagraphs: customPrefs?.includeStarredParagraphs ?? true,
        includeFavoriteCards: customPrefs?.includeFavoriteCards ?? true,
        includeFavoriteQuestions: customPrefs?.includeFavoriteQuestions ?? false,
        paragraphCount: customPrefs?.paragraphCount ?? 1,
        cardCount: customPrefs?.cardCount ?? 1,
      };

      const cleanPhone = normalizePhoneNumber(effectivePrefs.phone);
      if (!cleanPhone) {
        return res.status(400).json({
          success: false,
          error: 'Lütfen geçerli bir telefon numarası belirtin.',
        });
      }

      const result = await sendDailyDigestForUser(
        targetBundle,
        effectivePrefs,
        deps.getPastQuestions()
      );

      if (!result.success) {
        return res.status(502).json({
          success: false,
          error: result.error,
        });
      }

      res.json({
        success: true,
        message: 'Günün tekrarı WhatsApp üzerinden iletildi.',
        messageId: result.messageId,
      });
    } catch (err: any) {
      res.status(500).json({ success: false, error: err?.message || 'Sunucu hatası' });
    }
  });
}
