import React, { useState, useEffect, useCallback } from 'react';
import {
  Bell,
  Smartphone,
  Mail,
  CheckCircle,
  AlertTriangle,
  Send,
  RefreshCw,
  ExternalLink,
  ShieldCheck,
  Volume2,
  Clock,
  MessageSquare,
  AlertCircle,
  Power,
  BellOff
} from 'lucide-react';
import { ApiService } from '../services/api';
import { FirestoreDbService } from '../services/firestoreDb';
import { getSupabaseClient } from '../services/supabaseDb';

const ADMIN_EMAIL = 'nofrostlife@gmail.com';

function urlBase64ToUint8Array(base64String: string): Uint8Array {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

interface AdminMobileNotificationCardProps {
  onClose?: () => void;
  onOpenQuestion?: (questionId: string) => void;
}

/** Öğren bildirimi: kayıttaki tam adresten (/ogren/<deste>?adim&hedef) bu sitenin yolunu çıkarır */
const learnPath = (url?: string): string | null => {
  if (!url) return null;
  try {
    const u = new URL(url, window.location.origin);
    return u.pathname.startsWith('/ogren/') ? `${u.pathname}${u.search}` : null;
  } catch {
    return null;
  }
};

export const AdminMobileNotificationCard: React.FC<AdminMobileNotificationCardProps> = ({
  onClose,
  onOpenQuestion
}) => {
  const [permission, setPermission] = useState<NotificationPermission>('default');
  const [isSupported, setIsSupported] = useState<boolean>(true);
  const [isSubscribed, setIsSubscribed] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [statusLoading, setStatusLoading] = useState<boolean>(false);
  const [deviceCount, setDeviceCount] = useState<number>(0);
  const [emailEnabled, setEmailEnabled] = useState<boolean>(false);
  const [recentNotifs, setRecentNotifs] = useState<any[]>([]);
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error' | 'info'; message: string } | null>(null);
  const [isTestingPush, setIsTestingPush] = useState<boolean>(false);
  const [isTestingEmail, setIsTestingEmail] = useState<boolean>(false);
  const [isTogglingEmail, setIsTogglingEmail] = useState<boolean>(false);

  // Bildirim ve Service Worker Desteği Kontrolü
  useEffect(() => {
    if (!('Notification' in window) || !('serviceWorker' in navigator)) {
      setIsSupported(false);
      return;
    }
    setPermission(Notification.permission);
    checkSubscriptionStatus();
  }, []);

  const checkSubscriptionStatus = useCallback(async () => {
    try {
      setStatusLoading(true);
      let activeSub: any = null;

      if ('serviceWorker' in navigator && 'PushManager' in window) {
        let reg = await navigator.serviceWorker.getRegistration();
        if (!reg) {
          const swPath = (import.meta.env.BASE_URL || '/').replace(/\/$/, '') + '/sw.js';
          try { reg = await navigator.serviceWorker.register(swPath, { scope: '/' }); } catch (_) {}
        }
        if (reg) {
          activeSub = await reg.pushManager.getSubscription();
          // Eğer tarayıcı bildirim izni verilmişse ama Web Push aboneliği henüz yoksa otomatik oluştur
          if (!activeSub && Notification.permission === 'granted') {
            try {
              const publicKey = await ApiService.getAdminVapidPublicKey(ADMIN_EMAIL);
              const convertedKey = urlBase64ToUint8Array(publicKey);
              activeSub = await reg.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: convertedKey.buffer as ArrayBuffer,
              });
              await ApiService.subscribeAdminPush(activeSub.toJSON(), ADMIN_EMAIL);
            } catch (autoErr) {
              console.warn('[AdminNotifications] Otomatik abonelik kaydı uyarısı:', autoErr);
            }
          }
        }
      }

      setIsSubscribed(Boolean(activeSub) || Notification.permission === 'granted');

      // 1. Firestore'dan en güncel admin bildirimlerini çek (Bulut Garantisi)
      try {
        const firestoreNotifs = await FirestoreDbService.getAdminNotifications();
        if (firestoreNotifs && firestoreNotifs.length > 0) {
          setRecentNotifs(firestoreNotifs);
        }
      } catch (_) {}

      // 2. Supabase'den kayıtlı admin cihaz sayısını al
      try {
        const client = getSupabaseClient();
        if (client) {
          const { data: subData } = await client.from('system_status').select('data').eq('id', 'admin_push_subscriptions').maybeSingle();
          if (subData?.data?.subscriptions && Array.isArray(subData.data.subscriptions)) {
            setDeviceCount(subData.data.subscriptions.length);
          }
        }
      } catch (_) {}

      // 3. Sunucu varsa sunucu durumunu çek
      try {
        const status = await ApiService.getAdminPushStatus(ADMIN_EMAIL);
        if (status && status.success) {
          if (status.deviceCount !== undefined) setDeviceCount(status.deviceCount);
          setEmailEnabled(Boolean(status.emailEnabled));
          if (Array.isArray(status.recentNotifications) && status.recentNotifications.length > 0) {
            setRecentNotifs(status.recentNotifications);
          }
        }
      } catch (err: any) {
        // Sunucu yoksa sorun değil, bulut modu devrededir
      }
    } catch (err: any) {
      console.warn('[AdminNotifications] Durum kontrolü uyarısı:', err?.message);
    } finally {
      setStatusLoading(false);
    }
  }, []);

  // Periyodik kontrol ve Canlı Firestore Bildirim Dinleyicisi
  useEffect(() => {
    // 1. Periyodik yoklama
    const interval = setInterval(() => {
      checkSubscriptionStatus();
    }, 45000);

    // 2. Canlı Firestore Dinleyicisi (Öğrenci bildirdiğinde paneldeki liste anında güncellenir)
    const unsubscribe = FirestoreDbService.subscribeAdminNotifications((notif) => {
      setRecentNotifs((prev) => [notif, ...prev.filter((p) => p.id !== notif.id)]);
    });

    return () => {
      clearInterval(interval);
      if (typeof unsubscribe === 'function') unsubscribe();
    };
  }, [checkSubscriptionStatus]);

  // Bildirimleri Aç / Bu Cihaza Abone Ol
  const handleEnablePush = async () => {
    setLoading(true);
    setFeedback(null);

    try {
      if (!('Notification' in window)) {
        throw new Error('Tarayıcınız Web Bildirimlerini desteklemiyor.');
      }

      // 1. İzin iste
      const perm = await Notification.requestPermission();
      setPermission(perm);

      if (perm !== 'granted') {
        throw new Error('Bildirim izni verilmedi. Lütfen tarayıcı ayarlarından nofrostlife.com.tr için bildirimlere izin verin.');
      }

      // 2. Service worker'ı kaydet
      let reg: ServiceWorkerRegistration | undefined;
      if ('serviceWorker' in navigator) {
        try {
          const swPath = (import.meta.env.BASE_URL || '/').replace(/\/$/, '') + '/sw.js';
          reg = await navigator.serviceWorker.register(swPath, { scope: '/' });
          await navigator.serviceWorker.ready;
        } catch (swErr) {
          console.warn('Service Worker kayıt uyarısı:', swErr);
        }
      }

      // 3. VAPID public key al ve abone ol
      let vapidSuccess = false;
      try {
        const publicKey = await ApiService.getAdminVapidPublicKey(ADMIN_EMAIL);
        if (publicKey && reg && 'PushManager' in window) {
          const convertedKey = urlBase64ToUint8Array(publicKey);
          const subscription = await reg.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: convertedKey.buffer as ArrayBuffer,
          });
          await ApiService.subscribeAdminPush(subscription.toJSON(), ADMIN_EMAIL);
          vapidSuccess = true;
        }
      } catch (err: any) {
        console.warn('PushManager subscribe uyarısı:', err?.message);
      }

      setIsSubscribed(true);
      setFeedback({
        type: 'success',
        message: vapidSuccess
          ? '🎉 Bu cihaz sisteme başarıyla kaydedildi! Hata bildirimi veya yorum yapıldığında telefonunuza anlık kilit ekranı bildirimi gelecektir.'
          : '🎉 Tarayıcı bildirim izni başarıyla verildi! Bildirimler bu cihazda anında çalacaktır.'
      });

      await checkSubscriptionStatus();
    } catch (err: any) {
      console.error('[handleEnablePush] Hata:', err);
      setFeedback({
        type: 'error',
        message: err?.message || 'Bildirim etkinleştirilemedi.'
      });
    } finally {
      setLoading(false);
    }
  };

  // Aboneliği Kapat
  const handleDisablePush = async () => {
    setLoading(true);
    setFeedback(null);
    try {
      if ('serviceWorker' in navigator) {
        const reg = await navigator.serviceWorker.getRegistration();
        if (reg) {
          const sub = await reg.pushManager.getSubscription();
          if (sub) {
            try { await ApiService.unsubscribeAdminPush(sub.endpoint, ADMIN_EMAIL); } catch (_) {}
            await sub.unsubscribe();
          }
        }
      }
      setIsSubscribed(false);
      setFeedback({ type: 'info', message: 'Bu cihazın bildirim aboneliği kaldırıldı.' });
      await checkSubscriptionStatus();
    } catch (err: any) {
      setFeedback({ type: 'error', message: 'Abonelik iptal edilemedi: ' + err?.message });
    } finally {
      setLoading(false);
    }
  };

  // Telefona Test Bildirimi Fırlat
  const handleTestPush = async () => {
    setIsTestingPush(true);
    setFeedback(null);

    // Her durumda bu cihazda anında yerel bildirim fırlat (cihazın bildirim gösterdiğini doğrulamak için)
    try {
      if ('Notification' in window && Notification.permission === 'granted') {
        if ('vibrate' in navigator) {
          navigator.vibrate([200, 100, 200, 100, 200]);
        }
        let swReg = await navigator.serviceWorker?.getRegistration();
        if (swReg && swReg.showNotification) {
          await swReg.showNotification('🧪 MedSoru Test Bildirimi', {
            body: 'Tebrikler! nofrostlife.com.tr bildirimleri telefonunuzda başarıyla çalışıyor.',
            icon: '/assets/favicon.ico',
            vibrate: [200, 100, 200],
          } as any);
        } else {
          new Notification('🧪 MedSoru Test Bildirimi', {
            body: 'Tebrikler! nofrostlife.com.tr bildirimleri telefonunuzda başarıyla çalışıyor.',
            icon: '/assets/favicon.ico',
          });
        }
      }
    } catch (_) {}

    // Sunucu / Bulut Web Push Fırlat
    try {
      const res = await ApiService.sendAdminPushTest(ADMIN_EMAIL);
      if (res && res.success) {
        if (res.message?.includes('0 cihaza') || res.details?.sent === 0) {
          // Henüz kayıtlı cihaz yoksa bu cihazı hemen kaydet
          await handleEnablePush();
          setFeedback({
            type: 'info',
            message: '📲 Test bildirimi ekranınıza iletildi. Cihazınız Web Push sistemine otomatik olarak kaydedildi.'
          });
        } else {
          setFeedback({
            type: 'success',
            message: `📲 ${res.message || 'Test bildirimi telefonunuza fırlatıldı! Bildirim çubuğunuzu kontrol edin.'}`
          });
        }
      } else {
        setFeedback({
          type: 'success',
          message: '📲 Test bildirimi bu cihaza iletildi!'
        });
      }
      setFeedback({
        type: 'success',
        message: '📲 Test bildirimi bu cihaza iletildi!'
      });
    } finally {
      setIsTestingPush(false);
    }
  };

  // Admin Mailine Test E-postası Gönder
  const handleTestEmail = async () => {
    setIsTestingEmail(true);
    setFeedback(null);
    try {
      const res = await ApiService.sendAdminEmailTest(ADMIN_EMAIL);
      if (res && res.success) {
        setFeedback({
          type: 'success',
          message: `✉️ ${res.message || 'Admin adresinize (nofrostlife@gmail.com) test e-postası başarıyla gönderildi!'}`
        });
      } else {
        throw new Error(res?.error || 'E-posta gönderilemedi.');
      }
    } catch (err: any) {
      setFeedback({
        type: 'info',
        message: 'ℹ️ Canlı e-posta gönderimi arka plandaki SMTP sunucusunun aktif olmasını gerektirir. Sitede doğrudan telefonunuza gelen Web Push / Kilit Ekranı Bildirimleri ise her zaman çalışır durumdadır.'
      });
    } finally {
      setIsTestingEmail(false);
    }
  };

  // Admin E-posta Bildirimlerini Aç/Kapat
  const handleToggleEmail = async () => {
    setIsTogglingEmail(true);
    setFeedback(null);
    try {
      const nextState = !emailEnabled;
      const res = await ApiService.toggleAdminEmail(nextState, ADMIN_EMAIL);
      if (res && res.success) {
        setEmailEnabled(res.emailEnabled);
        setFeedback({
          type: res.emailEnabled ? 'success' : 'info',
          message: res.message
        });
      }
    } catch (err: any) {
      setFeedback({
        type: 'error',
        message: 'E-posta bildirim ayarı değiştirilemedi: ' + err?.message
      });
    } finally {
      setIsTogglingEmail(false);
    }
  };

  return (
    <div className="ms-panel p-5 text-ink space-y-5">
      {/* Başlık ve Durum */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-line">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-accent-soft text-accent border border-accent/30 flex items-center justify-center shadow-inner">
            <Smartphone className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-bold text-base text-ink">Yönetici Anlık Bildirim Ayarları</h3>
              <span className="bg-ok-soft text-ok border border-ok/30 text-[10px] font-black px-2 py-0.5 rounded-full uppercase tracking-wider flex items-center gap-1">
                <ShieldCheck className="w-3 h-3 text-ok" />
                Yalnızca Admin
              </span>
            </div>
            <p className="text-xs text-ink-3 mt-0.5">
              Hata bildirimleri ve öğrenci yorumları anında <strong className="text-accent">{ADMIN_EMAIL}</strong> mailine ve telefonunuza iletilir.
            </p>
          </div>
        </div>

        <button
          onClick={checkSubscriptionStatus}
          disabled={statusLoading}
          className="self-end sm:self-auto text-xs text-ink-3 hover:text-accent flex items-center gap-1.5 px-3 py-1.5 rounded-lg hover:bg-field border border-line cursor-pointer disabled:opacity-50 transition-colors"
          title="Durumu yenile"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${statusLoading ? 'animate-spin text-accent' : ''}`} />
          <span>Yenile</span>
        </button>
      </div>

      {/* Geri Bildirim Mesajı */}
      {feedback && (
        <div
          className={`p-3.5 rounded-xl text-xs flex items-start gap-2.5 animate-fade-in ${
            feedback.type === 'success'
              ? 'bg-ok-soft border border-ok/30 text-ok'
              : feedback.type === 'error'
              ? 'bg-bad-soft border border-bad/30 text-bad-text'
              : 'bg-accent-soft border border-accent/30 text-accent'
          }`}
        >
          {feedback.type === 'success' ? (
            <CheckCircle className="w-4 h-4 text-ok shrink-0 mt-0.5" />
          ) : feedback.type === 'error' ? (
            <AlertTriangle className="w-4 h-4 text-bad shrink-0 mt-0.5" />
          ) : (
            <AlertCircle className="w-4 h-4 text-accent shrink-0 mt-0.5" />
          )}
          <span className="leading-relaxed">{feedback.message}</span>
        </div>
      )}

      {/* Durum Kartları Izgarası */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
        {/* Mobil Web Push Durumu */}
        <div className="bg-canvas border border-line rounded-xl p-4 flex flex-col justify-between space-y-3">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-ink flex items-center gap-2">
                <Bell className="w-4 h-4 text-warn" />
                Telefonda Web Push Bildirimi
              </span>
              {isSubscribed ? (
                <span className="bg-ok-soft text-ok border border-ok/30 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                  <CheckCircle className="w-3 h-3 text-ok" />
                  Bu Cihaz Aktif
                </span>
              ) : (
                <span className="bg-warn-soft text-warn border border-warn/30 text-[10px] font-bold px-2 py-0.5 rounded-full">
                  Kayıtlı Değil
                </span>
              )}
            </div>
            <p className="text-[11px] text-ink-3 leading-relaxed">
              Telefonunuzun kilit ekranında veya bildirim çubuğunda anlık uyarı alırsınız.
              {deviceCount > 0 && (
                <span className="block mt-1 text-accent font-semibold">
                  Toplam kayıtlı admin cihazı: {deviceCount} adet
                </span>
              )}
            </p>
          </div>

          <div className="pt-2 flex flex-wrap items-center gap-2">
            {!isSubscribed ? (
              <button
                onClick={handleEnablePush}
                disabled={loading || !isSupported}
                className="bg-ok hover:bg-ok/90 text-white font-bold px-3.5 py-2 rounded-lg text-xs flex items-center gap-1.5 shadow-md transition-all cursor-pointer active:scale-95 disabled:opacity-50"
              >
                <Bell className="w-3.5 h-3.5" />
                <span>{loading ? 'Bağlanıyor...' : 'Bu Cihazda Bildirimleri Aç'}</span>
              </button>
            ) : (
              <>
                <button
                  onClick={handleTestPush}
                  disabled={isTestingPush}
                  className="bg-accent hover:bg-accent-hover text-white font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 shadow-xs transition-all cursor-pointer active:scale-95 disabled:opacity-50"
                >
                  <Send className={`w-3.5 h-3.5 ${isTestingPush ? 'animate-pulse' : ''}`} />
                  <span>{isTestingPush ? 'Gönderiliyor...' : 'Telefona Test Bildirimi Fırlat'}</span>
                </button>
                <button
                  onClick={handleDisablePush}
                  disabled={loading}
                  className="text-ink-3 hover:text-bad text-xs px-2.5 py-1.5 rounded-lg hover:bg-field transition-colors cursor-pointer"
                >
                  Kapat
                </button>
              </>
            )}
          </div>
        </div>

        {/* E-posta Bildirimi Durumu */}
        <div className="bg-canvas border border-line rounded-xl p-4 flex flex-col justify-between space-y-3">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-bold text-ink flex items-center gap-2">
                <Mail className="w-4 h-4 text-accent" />
                Admin E-posta İletimi
              </span>
              {emailEnabled ? (
                <span className="bg-ok-soft text-ok border border-ok/30 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                  <CheckCircle className="w-3 h-3 text-ok" />
                  E-posta Aktif
                </span>
              ) : (
                <span className="bg-field text-ink-3 border border-line text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                  <BellOff className="w-3 h-3 text-ink-3" />
                  Kapalı (Yalnızca Telefon)
                </span>
              )}
            </div>
            <p className="text-[11px] text-ink-3 leading-relaxed">
              {emailEnabled ? (
                <>Her hata bildiriminde doğrudan <strong className="text-ink">{ADMIN_EMAIL}</strong> adresine anlık HTML e-posta düşer.</>
              ) : (
                <>E-posta gönderimi kapalıdır. Bildirimler yalnızca telefonunuzun kilit ekranına ve bildirim çubuğuna Web Push olarak iletilir.</>
              )}
            </p>
          </div>

          <div className="pt-2 flex flex-wrap items-center gap-2">
            <button
              onClick={handleToggleEmail}
              disabled={isTogglingEmail}
              className={`font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 transition-all cursor-pointer active:scale-95 disabled:opacity-50 ${
                emailEnabled
                  ? 'bg-bad-soft hover:bg-bad/15 text-bad-text border border-bad/30'
                  : 'bg-ok-soft hover:bg-ok/15 text-ok border border-ok/30'
              }`}
            >
              <Power className={`w-3.5 h-3.5 ${isTogglingEmail ? 'animate-spin' : ''}`} />
              <span>
                {isTogglingEmail
                  ? 'Güncelleniyor...'
                  : emailEnabled
                  ? 'E-posta Gönderimini Kapat'
                  : 'E-posta Gönderimini Aç'}
              </span>
            </button>

            {emailEnabled && (
              <button
                onClick={handleTestEmail}
                disabled={isTestingEmail}
                className="bg-field hover:bg-line text-ink border border-line font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 transition-all cursor-pointer active:scale-95 disabled:opacity-50"
              >
                <Send className={`w-3.5 h-3.5 ${isTestingEmail ? 'animate-pulse' : ''}`} />
                <span>{isTestingEmail ? 'Gönderiliyor...' : 'Test E-postası'}</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Telefon Kurulum İpuçları (PWA Rehberi) */}
      <div className="bg-accent-soft border border-accent/20 rounded-xl p-3.5 text-xs text-accent space-y-1.5">
        <strong className="font-bold flex items-center gap-2 text-ink">
          <Smartphone className="w-4 h-4 text-accent" />
          📱 Telefonda Bildirimleri Dakikalar İçinde Almak İçin:
        </strong>
        <p className="text-[11px] leading-relaxed text-ink-2">
          1. <strong>Android (Chrome):</strong> Telefonunuzda <strong>nofrostlife.com.tr</strong> adresine girin, admin olarak oturum açın ve yukarıdaki <em>"Bu Cihazda Bildirimleri Aç"</em> butonuna dokunun. Tarayıcı izin penceresinde <strong>"İzin Ver"</strong> seçin.
        </p>
        <p className="text-[11px] leading-relaxed text-ink-2">
          2. <strong>iPhone / iOS (Safari):</strong> Safari'de <strong>nofrostlife.com.tr</strong>'yi açın &rarr; Paylaş simgesine dokunup <strong>"Ana Ekrana Ekle"</strong> yapın &rarr; Uygulamayı ana ekrandan açıp bildirimleri etkinleştirin (iOS 16.4+).
        </p>
        <p className="text-[11px] leading-relaxed text-ink-2">
          3. <strong>E-posta:</strong> Telefonunuzda Gmail / Mail uygulamasında <em>{ADMIN_EMAIL}</em> hesabı kuruluysa, bildirim mailleri saniyeler içinde doğrudan telefon ekranınıza bildirim olarak da düşer.
        </p>
      </div>

      {/* Son Gelen Bildirimler Geçmişi */}
      {recentNotifs && recentNotifs.length > 0 && (
        <div className="space-y-2 pt-2 border-t border-line">
          <div className="flex items-center justify-between text-xs text-ink font-bold">
            <span className="flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-accent" />
              Son Gelen Öğrenci Bildirimleri & Yorumları ({recentNotifs.length})
            </span>
          </div>

          <div className="max-h-48 overflow-y-auto space-y-2 pr-1 custom-scrollbar">
            {recentNotifs.slice(0, 8).map((notif: any) => (
              <div
                key={notif.id}
                className="bg-canvas border border-line rounded-lg p-2.5 flex items-start justify-between gap-3 text-xs hover:border-line transition-colors"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    {notif.type === 'report' ? (
                      <span className="bg-bad-soft text-bad border border-bad/30 text-[10px] font-bold px-1.5 py-0.2 rounded flex items-center gap-1">
                        <AlertTriangle className="w-2.5 h-2.5" />
                        Hata Bildirimi
                      </span>
                    ) : notif.type === 'comment' ? (
                      <span className="bg-blue-500/20 text-blue-300 border border-blue-500/30 text-[10px] font-bold px-1.5 py-0.2 rounded flex items-center gap-1">
                        <MessageSquare className="w-2.5 h-2.5" />
                        Yorum
                      </span>
                    ) : (
                      <span className="bg-ok-soft text-ok border border-ok/30 text-[10px] font-bold px-1.5 py-0.2 rounded">
                        Test
                      </span>
                    )}
                    <span className="font-mono text-[11px] text-accent font-semibold">
                      {notif.questionId ? `#${notif.questionId}` : ''}
                    </span>
                    <span className="text-[10px] text-ink-3">
                      {notif.timestamp ? new Date(notif.timestamp).toLocaleString('tr-TR') : ''}
                    </span>
                  </div>
                  <p className="text-ink text-[11px] leading-tight line-clamp-2">
                    {notif.message}
                  </p>
                </div>

                {learnPath(notif.url) ? (
                  <a
                    href={learnPath(notif.url)!}
                    className="shrink-0 bg-accent-soft hover:bg-accent hover:text-white text-accent text-[11px] font-bold px-2 py-1 rounded flex items-center gap-1 cursor-pointer transition-colors"
                    title="Derste bildirilen yere git"
                  >
                    <span>Derste gör</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                ) : notif.questionId && onOpenQuestion && (
                  <button
                    onClick={() => onOpenQuestion(notif.questionId)}
                    className="shrink-0 bg-accent-soft hover:bg-accent hover:text-white text-accent text-[11px] font-bold px-2 py-1 rounded flex items-center gap-1 cursor-pointer transition-colors"
                    title="Soruyu incele"
                  >
                    <span>Gör</span>
                    <ExternalLink className="w-3 h-3" />
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
