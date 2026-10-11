import React, { useEffect, useMemo, useState } from 'react';
import {
  Bell,
  BellOff,
  Sparkles,
  MessageSquare,
  AlertTriangle,
  CheckCircle2,
  CheckCheck,
  Trash2,
  MoreHorizontal,
  Circle,
  PenLine,
  Users,
  ChevronRight,
} from 'lucide-react';
import { userNotificationService, UserNotification } from '../../services/userNotificationService';
import { executeDeepLinkFocus } from '../../services/universalRedirectService';
import { Sheet } from '../ui/Sheet';
import { Segmented, Switch } from '../ui/kit';
import { confirmDialog } from '../ui/ConfirmDialog';
import { toast } from '../ui/Toast';

/**
 * Bildirimler — ortak Sheet üzerinde (Escape, odak tuzağı, telefonda alttan sayfa).
 *  - Süzgeç: Tümü / Okunmamış; gün gruplu liste (Bugün, Dün, tarih); göreli zaman.
 *  - Satır: tür ikon karosu · başlık · ileti · zaman; tıklayınca okundu + uygulama içinde hedefe gider (sayfa yenilenmez).
 *  - Satır menüsü: okundu/okunmadı, sil. Toplu: tümünü okundu say, geçmişi temizle (onaylı).
 *  - Ayar: anlık (tarayıcı) bildirim; izin reddedilirse nasıl açılacağı yazılır.
 */
interface NotificationHistoryModalProps {
  isOpen: boolean;
  onClose: () => void;
}

type Filter = 'all' | 'unread';

const TYPE_META: Record<UserNotification['type'], { icon: React.ElementType; tone: string; label: string }> = {
  ai_reconstruction_complete: { icon: Sparkles, tone: 'ai', label: 'Yapay zekâ' },
  ai_queued: { icon: Sparkles, tone: 'ai', label: 'Yapay zekâ' },
  comment_added: { icon: MessageSquare, tone: 'accent', label: 'Yorum' },
  comment_deleted: { icon: MessageSquare, tone: 'muted', label: 'Yorum' },
  contribution_added: { icon: Users, tone: 'clinic', label: 'Katkı' },
  report_filed: { icon: AlertTriangle, tone: 'warn', label: 'Bildirim' },
  report_resolved: { icon: CheckCircle2, tone: 'ok', label: 'Çözüldü' },
  question_revised: { icon: PenLine, tone: 'ok', label: 'Revizyon' },
};

const startOfDay = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime();

function dayLabel(iso: string) {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return 'Tarihsiz';
  const today = startOfDay(new Date());
  const day = startOfDay(d);
  if (day === today) return 'Bugün';
  if (day === today - 86_400_000) return 'Dün';
  return d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: d.getFullYear() === new Date().getFullYear() ? undefined : 'numeric' });
}

function relTime(iso: string) {
  const t = new Date(iso).getTime();
  if (Number.isNaN(t)) return '';
  const s = Math.max(0, (Date.now() - t) / 1000);
  if (s < 60) return 'şimdi';
  if (s < 3600) return `${Math.floor(s / 60)} dk önce`;
  if (s < 86_400) return `${Math.floor(s / 3600)} sa önce`;
  return new Date(t).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' });
}

/** Uygulama içi gezinme: adres değişir, App popstate ile rotayı kurar, ardından hedef öğeye odaklanılır. */
function openDeepLink(url: string) {
  if (!url) return;
  try {
    const u = new URL(url, window.location.origin);
    if (u.origin !== window.location.origin) {
      window.open(u.href, '_blank', 'noopener');
      return;
    }
    window.history.pushState({}, '', u.pathname + u.search + u.hash);
    window.dispatchEvent(new PopStateEvent('popstate'));
    const anchor = u.hash ? decodeURIComponent(u.hash.slice(1)) : '';
    // Hedef ekran ve liste yüklenene kadar birkaç kez dene.
    let n = 0;
    const tick = () => {
      if (executeDeepLinkFocus(anchor || undefined) || ++n > 8) return;
      window.setTimeout(tick, 350);
    };
    window.setTimeout(tick, 250);
  } catch {
    executeDeepLinkFocus(url);
  }
}

export const NotificationHistoryModal: React.FC<NotificationHistoryModalProps> = ({ isOpen, onClose }) => {
  const [notifications, setNotifications] = useState<UserNotification[]>(() => userNotificationService.getAll());
  const [filter, setFilter] = useState<Filter>('all');
  const [pushEnabled, setPushEnabled] = useState(userNotificationService.isPushEnabled());
  const [menuFor, setMenuFor] = useState<string | null>(null);
  const [, tick] = useState(0);

  useEffect(() => {
    if (!isOpen) return;
    const unsub = userNotificationService.subscribe(setNotifications);
    setPushEnabled(userNotificationService.isPushEnabled());
    // Göreli zamanlar ("3 dk önce") açıkken tazelenir.
    const t = window.setInterval(() => tick((x) => x + 1), 30_000);
    return () => {
      unsub();
      window.clearInterval(t);
    };
  }, [isOpen]);

  useEffect(() => {
    if (!menuFor) return;
    const close = (e: MouseEvent) => {
      if (!(e.target as HTMLElement).closest('.nf-menu, .nf-more')) setMenuFor(null);
    };
    document.addEventListener('mousedown', close);
    return () => document.removeEventListener('mousedown', close);
  }, [menuFor]);

  const unread = notifications.filter((n) => !n.read).length;
  const shown = filter === 'unread' ? notifications.filter((n) => !n.read) : notifications;

  const groups = useMemo(() => {
    const out: { label: string; items: UserNotification[] }[] = [];
    [...shown]
      .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
      .forEach((n) => {
        const label = dayLabel(n.createdAt);
        const last = out[out.length - 1];
        if (last && last.label === label) last.items.push(n);
        else out.push({ label, items: [n] });
      });
    return out;
  }, [shown]);

  const handleTogglePush = async (next: boolean) => {
    if (next) {
      if (typeof window === 'undefined' || !('Notification' in window)) {
        toast.error('Desteklenmiyor', 'Bu tarayıcı anlık bildirimleri desteklemiyor.');
        return;
      }
      const granted = await userNotificationService.requestPushPermission();
      setPushEnabled(granted);
      if (!granted) {
        toast.error(
          'İzin verilmedi',
          Notification.permission === 'denied'
            ? 'Tarayıcı bu site için bildirimleri engelliyor. Adres çubuğundaki site ayarlarından "Bildirimler"i aç.'
            : 'Anlık bildirim izni verilmedi.'
        );
      } else {
        toast.success('Anlık bildirim açık', 'Yeni bildirimler bu cihazda da görünecek.');
      }
    } else {
      userNotificationService.setPushEnabled(false);
      setPushEnabled(false);
    }
  };

  const open = (n: UserNotification) => {
    userNotificationService.markAsRead(n.id);
    if (!n.deepLinkUrl) return;
    onClose();
    openDeepLink(n.deepLinkUrl);
  };

  const clearAll = async () => {
    const ok = await confirmDialog({
      title: 'Bildirim geçmişi silinsin mi?',
      message: `${notifications.length} bildirim bu cihazdan kalıcı olarak silinecek.`,
      confirmLabel: 'Hepsini sil',
      tone: 'danger',
    });
    if (ok) userNotificationService.clearAll();
  };

  return (
    <Sheet
      open={isOpen}
      onClose={onClose}
      title="Bildirimler"
      subtitle={unread ? `${unread} okunmamış` : notifications.length ? 'Hepsi okundu' : undefined}
      width={520}
      size="full"
      actions={
        unread > 0 ? (
          <button type="button" className="ui-btn is-ghost is-sm" onClick={() => userNotificationService.markAllAsRead()} title="Tümünü okundu say">
            <CheckCheck aria-hidden /> <span className="nf-hide-sm">Tümü okundu</span>
          </button>
        ) : null
      }
    >
      <div className="nf">
        <div className="nf-bar">
          <Segmented<Filter>
            className="nf-seg"
            label="Bildirim süzgeci"
            value={filter}
            onChange={setFilter}
            options={[
              { value: 'all', label: <>Tümü <span className="nf-n">{notifications.length}</span></> },
              { value: 'unread', label: <>Okunmamış <span className="nf-n">{unread}</span></> },
            ]}
          />
        </div>

        {shown.length === 0 ? (
          <div className="nf-empty">
            <span className="nf-empty-ic" aria-hidden>{filter === 'unread' ? <CheckCheck /> : <Bell />}</span>
            <b>{filter === 'unread' ? 'Okunmamış bildirim yok' : 'Henüz bildirim yok'}</b>
            <p>
              {filter === 'unread'
                ? 'Hepsini gördün.'
                : 'Sorun yapay zekâyla yeniden kurulduğunda, bildirdiğin hata çözüldüğünde ya da sorulara yorum geldiğinde burada görünür.'}
            </p>
          </div>
        ) : (
          groups.map((g) => (
            <section key={g.label} className="nf-group" aria-label={g.label}>
              <h4 className="nf-day">{g.label}</h4>
              <ul className="nf-list">
                {g.items.map((n) => {
                  const meta = TYPE_META[n.type] || { icon: Bell, tone: 'muted', label: 'Bildirim' };
                  const Icon = meta.icon;
                  return (
                    <li key={n.id} className={`nf-row ${n.read ? '' : 'is-unread'}`}>
                      <button type="button" className="nf-main" onClick={() => open(n)}>
                        <span className={`nf-ic is-${meta.tone}`} aria-hidden><Icon /></span>
                        <span className="nf-body">
                          <span className="nf-top">
                            <b>{n.title.replace(/^✓\s*/, '')}</b>
                            <time dateTime={n.createdAt}>{relTime(n.createdAt)}</time>
                          </span>
                          {n.message && <span className="nf-msg">{n.message}</span>}
                          <span className="nf-kind">{meta.label}{n.deepLinkUrl && <><i aria-hidden>·</i>Aç <ChevronRight aria-hidden /></>}</span>
                        </span>
                        {!n.read && <span className="nf-dot" aria-label="Okunmamış" />}
                      </button>
                      <button
                        type="button"
                        className="nf-more qk-ib"
                        aria-haspopup="menu"
                        aria-expanded={menuFor === n.id}
                        aria-label="Bildirim seçenekleri"
                        onClick={() => setMenuFor(menuFor === n.id ? null : n.id)}
                      >
                        <MoreHorizontal aria-hidden />
                      </button>
                      {menuFor === n.id && (
                        <div className="nf-menu" role="menu">
                          <button
                            type="button"
                            role="menuitem"
                            onClick={() => {
                              n.read ? userNotificationService.markAsUnread(n.id) : userNotificationService.markAsRead(n.id);
                              setMenuFor(null);
                            }}
                          >
                            {n.read ? <><Circle aria-hidden /> Okunmadı yap</> : <><CheckCheck aria-hidden /> Okundu say</>}
                          </button>
                          <button
                            type="button"
                            role="menuitem"
                            className="is-bad"
                            onClick={() => {
                              userNotificationService.remove(n.id);
                              setMenuFor(null);
                            }}
                          >
                            <Trash2 aria-hidden /> Sil
                          </button>
                        </div>
                      )}
                    </li>
                  );
                })}
              </ul>
            </section>
          ))
        )}

        <section className="nf-settings" aria-label="Bildirim ayarları">
          <div className="nf-set-row">
            <span className="nf-ic is-accent" aria-hidden>{pushEnabled ? <Bell /> : <BellOff />}</span>
            <span className="nf-body">
              <b>Anlık bildirim</b>
              <span className="nf-msg">Uygulama kapalıyken bu cihazda tarayıcı bildirimi göster.</span>
            </span>
            <Switch checked={pushEnabled} onChange={handleTogglePush} label="Anlık bildirim" />
          </div>
          <p className="nf-note">Hata bildirimlerinin sonucu ayrıca hesabındaki e-posta adresine gönderilir.</p>
          {notifications.length > 0 && (
            <button type="button" className="ui-btn is-danger is-sm nf-clear" onClick={clearAll}>
              <Trash2 aria-hidden /> Geçmişi temizle
            </button>
          )}
        </section>
      </div>
    </Sheet>
  );
};
