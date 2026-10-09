import fs from 'fs';
import path from 'path';
import webpush from 'web-push';
import type { Transporter } from 'nodemailer';

export const ADMIN_EMAIL = 'nofrostlife@gmail.com';

export interface AdminPushSubscription {
  endpoint: string;
  keys: {
    p256dh: string;
    auth: string;
  };
  userAgent?: string;
  createdAt: string;
}

export interface AdminNotificationItem {
  id: string;
  type: 'report' | 'comment' | 'test';
  title: string;
  message: string;
  questionId?: string;
  author?: string;
  reason?: string;
  details?: string;
  text?: string;
  discipline?: string;
  topic?: string;
  url?: string;
  timestamp: string;
  read: boolean;
}

export class ServerNotificationService {
  private dataDir: string;
  private keysFile: string;
  private subsFile: string;
  private notifsFile: string;
  private vapidKeys: { publicKey: string; privateKey: string } | null = null;
  private recentEventKeys: Map<string, number> = new Map();

  constructor(dataDir: string) {
    this.dataDir = dataDir;
    this.keysFile = path.resolve(this.dataDir, 'web_push_keys.json');
    this.subsFile = path.resolve(this.dataDir, 'admin_push_subscriptions.json');
    this.notifsFile = path.resolve(this.dataDir, 'admin_notifications.json');
    this.ensureDirsAndKeys();
  }

  private ensureDirsAndKeys() {
    try {
      if (!fs.existsSync(this.dataDir)) {
        fs.mkdirSync(this.dataDir, { recursive: true });
      }

      // VAPID anahtarlarını kontrol et veya üret
      if (fs.existsSync(this.keysFile)) {
        try {
          this.vapidKeys = JSON.parse(fs.readFileSync(this.keysFile, 'utf-8'));
        } catch {
          this.vapidKeys = null;
        }
      }

      if (!this.vapidKeys || !this.vapidKeys.publicKey || !this.vapidKeys.privateKey) {
        this.vapidKeys = webpush.generateVAPIDKeys();
        fs.writeFileSync(this.keysFile, JSON.stringify(this.vapidKeys, null, 2), 'utf-8');
        console.log('[NotificationService] Yeni VAPID anahtarları üretildi ve kaydedildi.');
      }

      webpush.setVapidDetails(
        `mailto:${ADMIN_EMAIL}`,
        this.vapidKeys.publicKey,
        this.vapidKeys.privateKey
      );
    } catch (err: any) {
      console.error('[NotificationService] VAPID kurulum hatası:', err.message);
    }
  }

  public getVapidPublicKey(): string | null {
    return this.vapidKeys?.publicKey || null;
  }

  public getSubscriptions(): AdminPushSubscription[] {
    try {
      if (!fs.existsSync(this.subsFile)) return [];
      const content = fs.readFileSync(this.subsFile, 'utf-8');
      const list = JSON.parse(content);
      return Array.isArray(list) ? list : [];
    } catch {
      return [];
    }
  }

  public saveSubscriptions(subs: AdminPushSubscription[]) {
    try {
      fs.writeFileSync(this.subsFile, JSON.stringify(subs, null, 2), 'utf-8');
    } catch (err: any) {
      console.error('[NotificationService] Abonelikler kaydedilemedi:', err.message);
    }
  }

  public addSubscription(sub: { endpoint: string; keys: { p256dh: string; auth: string } }, userAgent?: string): boolean {
    if (!sub || !sub.endpoint || !sub.keys) return false;
    const subs = this.getSubscriptions();
    const existingIndex = subs.findIndex(s => s.endpoint === sub.endpoint);
    const item: AdminPushSubscription = {
      endpoint: sub.endpoint,
      keys: sub.keys,
      userAgent: userAgent || 'Mobil/Tarayıcı',
      createdAt: new Date().toISOString(),
    };

    if (existingIndex >= 0) {
      subs[existingIndex] = item;
    } else {
      subs.push(item);
    }
    this.saveSubscriptions(subs);
    return true;
  }

  public removeSubscription(endpoint: string): boolean {
    if (!endpoint) return false;
    const subs = this.getSubscriptions();
    const filtered = subs.filter(s => s.endpoint !== endpoint);
    if (filtered.length !== subs.length) {
      this.saveSubscriptions(filtered);
      return true;
    }
    return false;
  }

  public getNotifications(limit = 50): AdminNotificationItem[] {
    try {
      if (!fs.existsSync(this.notifsFile)) return [];
      const content = fs.readFileSync(this.notifsFile, 'utf-8');
      const list = JSON.parse(content);
      return (Array.isArray(list) ? list : []).slice(0, limit);
    } catch {
      return [];
    }
  }

  public recordNotification(item: AdminNotificationItem) {
    try {
      const list = this.getNotifications(200);
      list.unshift(item);
      fs.writeFileSync(this.notifsFile, JSON.stringify(list.slice(0, 100), null, 2), 'utf-8');
    } catch (err: any) {
      console.warn('[NotificationService] Bildirim geçmişe yazılamadı:', err.message);
    }
  }

  public markAsRead(id?: string) {
    try {
      const list = this.getNotifications(200);
      for (const item of list) {
        if (!id || item.id === id) {
          item.read = true;
        }
      }
      fs.writeFileSync(this.notifsFile, JSON.stringify(list, null, 2), 'utf-8');
    } catch {}
  }

  /**
   * Admin telefonlarına Web Push fırlatır
   */
  public async sendAdminWebPush(payload: {
    title: string;
    body: string;
    icon?: string;
    badge?: string;
    url?: string;
    data?: any;
  }): Promise<{ sent: number; failed: number; total: number }> {
    const subs = this.getSubscriptions();
    if (!subs.length) {
      return { sent: 0, failed: 0, total: 0 };
    }

    const jsonPayload = JSON.stringify({
      title: payload.title,
      body: payload.body,
      icon: payload.icon || 'https://nofrostlife.com.tr/assets/favicon.ico',
      badge: payload.badge || 'https://nofrostlife.com.tr/assets/favicon.ico',
      tag: payload.data?.tag || `medsoru-${payload.data?.type || 'item'}-${payload.data?.questionId || 'general'}`,
      data: {
        url: payload.url || 'https://nofrostlife.com.tr',
        ...(payload.data || {}),
      },
    });

    let sent = 0;
    let failed = 0;
    const remainingSubs: AdminPushSubscription[] = [];

    for (const sub of subs) {
      try {
        await webpush.sendNotification(
          {
            endpoint: sub.endpoint,
            keys: sub.keys,
          },
          jsonPayload,
          {
            TTL: 60 * 60 * 24, // 24 saat sakla
            urgency: 'high',
          }
        );
        sent++;
        remainingSubs.push(sub);
      } catch (err: any) {
        failed++;
        console.warn(`[NotificationService] Push gönderim hatası (${sub.endpoint.slice(0, 30)}...):`, err.statusCode || err.message);
        // 404 veya 410 aboneliğin süresi dolmuş veya iptal edilmiş demektir
        if (err.statusCode === 404 || err.statusCode === 410) {
          console.log('[NotificationService] Süresi dolmuş abonelik silindi.');
        } else {
          remainingSubs.push(sub);
        }
      }
    }

    if (remainingSubs.length !== subs.length) {
      this.saveSubscriptions(remainingSubs);
    }

    return { sent, failed, total: subs.length };
  }

  /**
   * Admin e-posta adresine detaylı HTML bildirim maili gönderir
   */
  public async sendAdminEmail(params: {
    transporter: Transporter | null;
    smtpFrom: string;
    type: 'report' | 'comment' | 'test';
    questionId?: string;
    reason?: string;
    details?: string;
    text?: string;
    author?: string;
    discipline?: string;
    topic?: string;
    appUrl?: string;
    /** Uygulama içi yol (ör. Öğren derin bağlantısı); verilirse bağlantı buraya gider */
    link?: string;
  }): Promise<{ success: boolean; messageId?: string; error?: string }> {
    const { transporter, smtpFrom, type, questionId, reason, details, text, author, discipline, topic } = params;
    if (!transporter) {
      return { success: false, error: 'SMTP sunucusu yapılandırılmamış veya devre dışı.' };
    }

    let baseUrl = params.appUrl || 'https://nofrostlife.com.tr';
    if (!baseUrl || baseUrl.includes('localhost') || baseUrl.includes('127.0.0.1')) {
      baseUrl = 'https://nofrostlife.com.tr';
    }
    const cleanBaseUrl = baseUrl.replace(/\/$/, '');
    const questionLink = params.link
      ? `${cleanBaseUrl}${params.link}`
      : questionId
        ? `${cleanBaseUrl}/cikmis/${encodeURIComponent(questionId)}`
        : `${cleanBaseUrl}/cikmis`;

    let subject = '';
    let badgeColor = '#0f766e';
    let badgeText = '';
    let headline = '';
    let mainContentHtml = '';

    const safeAuthor = (author || 'Anonim Tıp Öğrencisi').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const safeReason = (reason || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const safeDetails = (details || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const safeText = (text || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const safeDiscipline = (discipline || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const safeTopic = (topic || '').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    if (type === 'report') {
      subject = params.link?.startsWith('/ogren')
        ? `🚨 [MedSoru Öğren Hata Bildirimi] ${questionId || 'Ders'}: ${safeReason || 'İtiraz/Hata'}`
        : `🚨 [MedSoru Hata Bildirimi] Soru #${questionId || 'Genel'}: ${safeReason || 'İtiraz/Hata'}`;
      badgeColor = '#dc2626';
      badgeText = 'HATA BİLDİRİMİ';
      headline = 'Bir tıp öğrencisi soru hakkında hata/itiraz bildirdi!';
      mainContentHtml = `
        <div style="background-color: #fef2f2; border: 1px solid #fee2e2; border-left: 4px solid #ef4444; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
          <p style="margin: 0 0 8px 0; font-size: 13px; font-weight: 700; color: #991b1b; text-transform: uppercase; letter-spacing: 0.5px;">Bildirilen Sebep:</p>
          <p style="margin: 0 0 12px 0; font-size: 15px; font-weight: 600; color: #111827;">${safeReason}</p>
          ${safeDetails ? `
            <p style="margin: 0 0 6px 0; font-size: 13px; font-weight: 700; color: #991b1b; text-transform: uppercase; letter-spacing: 0.5px;">Öğrenci Detay Açıklaması:</p>
            <p style="margin: 0; font-size: 14px; color: #374151; white-space: pre-wrap; background: #ffffff; padding: 10px 14px; border-radius: 6px; border: 1px solid #fecaca;">${safeDetails}</p>
          ` : ''}
        </div>
      `;
    } else if (type === 'comment') {
      subject = `💬 [MedSoru Yeni Yorum] Soru #${questionId || 'Genel'} - ${safeAuthor}`;
      badgeColor = '#2563eb';
      badgeText = 'ÖĞRENCİ YORUMU';
      headline = 'Soruya yeni bir öğrenci yorumu/katkısı eklendi!';
      mainContentHtml = `
        <div style="background-color: #eff6ff; border: 1px solid #dbeafe; border-left: 4px solid #3b82f6; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
          <p style="margin: 0 0 8px 0; font-size: 13px; font-weight: 700; color: #1e40af; text-transform: uppercase; letter-spacing: 0.5px;">Yorum / Öneri Metni:</p>
          <p style="margin: 0; font-size: 14px; color: #1e293b; white-space: pre-wrap; background: #ffffff; padding: 12px 14px; border-radius: 6px; border: 1px solid #bfdbfe;">${safeText}</p>
        </div>
      `;
    } else {
      subject = `🧪 [MedSoru] Admin Bildirim Sistemi Canlı Testi`;
      badgeColor = '#059669';
      badgeText = 'TEST BİLDİRİMİ';
      headline = 'Bildirim sistemi ve e-posta entegrasyonu başarıyla çalışıyor!';
      mainContentHtml = `
        <div style="background-color: #ecfdf5; border: 1px solid #d1fae5; border-left: 4px solid #10b981; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
          <p style="margin: 0; font-size: 14px; color: #065f46;">Bu e-posta, hata bildirimi ve öğrenci yorumu yapıldığında tarafınıza anında iletilecek bildirimlerin canlı testidir. Sistem çalışır durumdadır.</p>
        </div>
      `;
    }

    const htmlBody = `
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${subject}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
  <div style="max-width: 600px; margin: 24px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05); border: 1px solid #e2e8f0;">
    
    <!-- Üst Başlık -->
    <div style="background: linear-gradient(135deg, #0f766e 0%, #115e59 100%); padding: 24px; color: #ffffff;">
      <div style="display: flex; align-items: center; justify-content: space-between;">
        <span style="font-size: 18px; font-weight: 800; letter-spacing: -0.5px;">🩺 MeDSor · Tıp Kurul Portalı</span>
        <span style="background-color: ${badgeColor}; color: #ffffff; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.5px;">${badgeText}</span>
      </div>
      <h1 style="margin: 16px 0 0 0; font-size: 20px; font-weight: 700; line-height: 1.3;">${headline}</h1>
    </div>

    <!-- Gövde -->
    <div style="padding: 24px;">
      
      <!-- Meta Bilgiler -->
      <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13px;">
        ${questionId ? `
        <tr>
          <td style="padding: 6px 0; color: #64748b; width: 110px;">Soru Kimliği:</td>
          <td style="padding: 6px 0; color: #0f172a; font-weight: 600; font-family: monospace;">#${questionId}</td>
        </tr>
        ` : ''}
        ${(safeDiscipline || safeTopic) ? `
        <tr>
          <td style="padding: 6px 0; color: #64748b;">Ders / Konu:</td>
          <td style="padding: 6px 0; color: #0f172a; font-weight: 500;">${[safeDiscipline, safeTopic].filter(Boolean).join(' • ')}</td>
        </tr>
        ` : ''}
        <tr>
          <td style="padding: 6px 0; color: #64748b;">Gönderen:</td>
          <td style="padding: 6px 0; color: #0f172a; font-weight: 600;">${safeAuthor}</td>
        </tr>
        <tr>
          <td style="padding: 6px 0; color: #64748b;">Tarih & Saat:</td>
          <td style="padding: 6px 0; color: #0f172a;">${new Date().toLocaleString('tr-TR', { timeZone: 'Europe/Istanbul' })}</td>
        </tr>
      </table>

      <!-- Ana İçerik Bloğu -->
      ${mainContentHtml}

      <!-- Doğrudan Buton -->
      <div style="text-align: center; margin: 28px 0 16px 0;">
        <a href="${questionLink}" target="_blank" style="display: inline-block; background-color: #0f766e; color: #ffffff; font-weight: 600; font-size: 15px; padding: 12px 28px; border-radius: 8px; text-decoration: none; box-shadow: 0 2px 4px rgba(15, 118, 110, 0.3);">
          📱 Soruyu nofrostlife.com.tr'de Aç ve İncele &rarr;
        </a>
      </div>

    </div>

    <!-- Alt Bilgi -->
    <div style="background-color: #f1f5f9; padding: 16px 24px; border-top: 1px solid #e2e8f0; font-size: 12px; color: #64748b; line-height: 1.5; text-align: center;">
      <p style="margin: 0 0 4px 0;">Bu bildirim yalnızca yöneticiye (<strong style="color: #334155;">${ADMIN_EMAIL}</strong>) gönderilmektedir.</p>
      <p style="margin: 0;">MedSoru Bildirim Sistemi · <a href="${cleanBaseUrl}" style="color: #0f766e; text-decoration: none;">nofrostlife.com.tr</a></p>
    </div>

  </div>
</body>
</html>
    `;

    try {
      const info = await transporter.sendMail({
        from: smtpFrom,
        to: ADMIN_EMAIL,
        subject,
        html: htmlBody,
        text: `${headline}\n\nSoru: #${questionId || 'Genel'}\nGönderen: ${safeAuthor}\n${safeReason ? `Sebep: ${safeReason}\n` : ''}${safeDetails ? `Detay: ${safeDetails}\n` : ''}${safeText ? `Yorum: ${safeText}\n` : ''}\nBağlantı: ${questionLink}`,
      });
      return { success: true, messageId: info.messageId };
    } catch (err: any) {
      console.error('[NotificationService] E-posta gönderim hatası:', err.message);
      return { success: false, error: err.message };
    }
  }

  /**
   * Olay olduğunda hem e-posta hem Web Push bildirimi tetikler ve arşive kaydeder
   */
  public async notifyAdminOnEvent(params: {
    transporter: Transporter | null;
    smtpFrom: string;
    type: 'report' | 'comment' | 'test';
    questionId: string;
    reason?: string;
    details?: string;
    text?: string;
    author?: string;
    discipline?: string;
    topic?: string;
    appUrl?: string;
    /** Uygulama içi yol (ör. Öğren derin bağlantısı); verilirse bağlantı buraya gider */
    link?: string;
  }) {
    const { type, questionId, reason, details, text, author, discipline, topic, appUrl, transporter, smtpFrom } = params;

    // Mükerrer bildirim koruması (Aynı soru ve tip için 3 dakika içinde mükerrer bildirimleri filtrele)
    const dedupKey = `${type}:${questionId}:${reason || text || details || ''}`;
    const now = Date.now();
    const lastSent = this.recentEventKeys.get(dedupKey);
    if (lastSent && (now - lastSent) < 180000) {
      console.log(`[NotificationService] 🛑 Mükerrer bildirim engellendi (Son 3dk içinde iletildi): ${dedupKey}`);
      return;
    }
    this.recentEventKeys.set(dedupKey, now);

    // Bellek temizliği (10 dakikadan eski anahtarları sil)
    if (this.recentEventKeys.size > 200) {
      for (const [k, t] of this.recentEventKeys.entries()) {
        if (now - t > 600000) this.recentEventKeys.delete(k);
      }
    }

    const authorName = author || 'Anonim Öğrenci';
    let baseUrl = appUrl || 'https://nofrostlife.com.tr';
    if (!baseUrl || baseUrl.includes('localhost') || baseUrl.includes('127.0.0.1')) {
      baseUrl = 'https://nofrostlife.com.tr';
    }
    const cleanBaseUrl = baseUrl.replace(/\/$/, '');
    const questionUrl = params.link
      ? `${cleanBaseUrl}${params.link}`
      : questionId
      ? `${cleanBaseUrl}/cikmis/${encodeURIComponent(questionId)}`
      : `${cleanBaseUrl}/cikmis`;

    const title = type === 'report'
      ? `🚨 MedSoru: Yeni Hata Bildirimi (#${questionId})`
      : type === 'comment'
      ? `💬 MedSoru: Yeni Öğrenci Yorumu (#${questionId})`
      : `🧪 MedSoru: Test Bildirimi`;

    const summaryMessage = type === 'report'
      ? `${authorName}: ${reason || 'Hata bildirildi'}${details ? ' - ' + details : ''}`
      : type === 'comment'
      ? `${authorName}: ${text || 'Yorum eklendi'}`
      : 'Yönetici telefon/tarayıcı test bildirimi.';

    // 1. Bildirim kaydı oluştur
    const notifItem: AdminNotificationItem = {
      id: `ntf-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      type,
      title,
      message: summaryMessage.slice(0, 300),
      questionId,
      author: authorName,
      reason,
      details,
      text,
      discipline,
      topic,
      url: questionUrl,
      timestamp: new Date().toISOString(),
      read: false,
    };
    this.recordNotification(notifItem);

    // 2. Asenkron Web Push Gönderimi (Admin telefonlarına)
    this.sendAdminWebPush({
      title,
      body: summaryMessage.slice(0, 160),
      url: questionUrl,
      data: {
        questionId,
        type,
        notificationId: notifItem.id,
      },
    }).then(res => {
      if (res.total > 0) {
        console.log(`[NotificationService] Web Push iletildi: ${res.sent}/${res.total} cihaza ulaştı.`);
      }
    }).catch(err => {
      console.warn('[NotificationService] Web Push tetikleme hatası:', err.message);
    });

    // 3. Asenkron E-posta Gönderimi (nofrostlife@gmail.com)
    this.sendAdminEmail({
      transporter,
      smtpFrom,
      type,
      questionId,
      reason,
      details,
      text,
      author: authorName,
      discipline,
      topic,
      appUrl: cleanBaseUrl,
      link: params.link,
    }).then(res => {
      if (res.success) {
        console.log(`[NotificationService] Admin bildirim e-postası başarıyla iletildi (${ADMIN_EMAIL})`);
      } else {
        console.log(`[NotificationService] Admin bildirim e-postası gönderilemedi: ${res.error}`);
      }
    }).catch(err => {
      console.warn('[NotificationService] E-posta tetikleme hatası:', err.message);
    });
  }
}
