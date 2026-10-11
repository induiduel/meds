import React, { useEffect, useState } from 'react';
import { ChevronRight, Database, FileDown, LayoutGrid, Moon, ShieldCheck, Sun, SunMedium, Bell } from 'lucide-react';
import { linkClick, pathFor, type AppRoute } from '../../router';
import { MODE_LABELS, type ThemeMode, useAppearance } from '../../utils/appearance';
import { Segmented } from '../ui/kit';
import { Sheet } from '../ui/Sheet';
import { MORE_TREE, NAV_ITEMS, TAB_ITEMS } from './navModel';
import { userNotificationService } from '../../services/userNotificationService';
import { NotificationHistoryModal } from '../notifications/NotificationHistoryModal';

const MODE_ICONS: Record<ThemeMode, React.ElementType> = { light: Sun, sepia: SunMedium, dark: Moon };

/**
 * v8 alt gezinme (<768px): dört sayfa + "Daha". Etkin sekmenin arkasında tek bir hap kayar.
 * Klavye açıkken gizlenir (html.kb-open). "Daha" ortak Sheet'te: gruplu liste, hızlı tema, araçlar.
 */
export const TabBar: React.FC<{
  active: AppRoute;
  onGo: (r: AppRoute) => void;
  isAdmin: boolean;
  onPdf: () => void;
  onOffline?: () => void;
}> = ({ active, onGo, isAdmin, onPdf, onOffline }) => {
  const [more, setMore] = useState(false);
  const [unreadNotifs, setUnreadNotifs] = useState(0);
  const [showNotifModal, setShowNotifModal] = useState(false);

  useEffect(() => {
    return userNotificationService.subscribe((list) => {
      setUnreadNotifs(list.filter((n) => !n.read).length);
    });
  }, []);

  const look = useAppearance();
  const idx = TAB_ITEMS.findIndex((t) => t.id === active);
  const at = idx >= 0 ? idx : active === 'practice' ? -1 : 4;
  useEffect(() => setMore(false), [active]);

  const go = (r: AppRoute) => {
    setMore(false);
    onGo(r);
  };

  return (
    <>
      <nav aria-label="Alt gezinme" className="sh-tabs ms-hide-on-kb print:hidden">
        <div className="sh-tabs-in">
          <span className="sh-tabs-ind" aria-hidden="true" style={{ transform: `translateX(${Math.max(0, at) * 100}%)`, opacity: at < 0 ? 0 : 1 }} />
          {TAB_ITEMS.map(({ id, short, label, icon: Icon }) => {
            const on = active === id;
            return (
              <a key={id} href={pathFor(id)} onClick={linkClick(() => go(id))} aria-current={on ? 'page' : undefined} className="sh-tab">
                <Icon strokeWidth={on ? 2.3 : 1.9} />
                <span>{short || label}</span>
              </a>
            );
          })}
          <button type="button" className="sh-tab" onClick={() => setMore(true)} aria-haspopup="dialog" aria-expanded={more} aria-current={at === 4 ? 'page' : undefined}>
            <LayoutGrid strokeWidth={at === 4 ? 2.3 : 1.9} />
            <span>Daha</span>
          </button>
        </div>
      </nav>

      <Sheet open={more} onClose={() => setMore(false)} title="Daha fazla" size="auto">
        <div className="sh-more">
          {MORE_TREE.map((g) => (
            <section key={g.label} className="ui-section">
              <div className="ui-section-h"><h2>{g.label}</h2></div>
              <div className="ui-group">
                {g.items.map(({ id, label, hint, icon: Icon, tint }) => (
                  <a
                    key={id}
                    href={pathFor(id)}
                    onClick={linkClick(() => go(id))}
                    aria-current={active === id ? 'page' : undefined}
                    className="ui-row has-icon sh-more-row"
                  >
                    <span className="ui-ico" style={{ '--ico-bg': tint, '--ico-fg': '#fff' } as React.CSSProperties}><Icon strokeWidth={2.1} /></span>
                    <span className="ui-row-main"><b>{label}</b><span>{hint}</span></span>
                    <ChevronRight className="w-4 h-4 shrink-0" style={{ color: 'var(--color-line-2)' }} />
                  </a>
                ))}
              </div>
            </section>
          ))}

          <section className="ui-section">
            <div className="ui-section-h"><h2>Görünüm ve hesap</h2></div>
            <div className="ui-group">
              <div className="ui-row">
                <Segmented<ThemeMode>
                  className="flex-1"
                  label="Tema"
                  value={look.mode}
                  onChange={(m) => look.set({ mode: m })}
                  options={(['light', 'sepia', 'dark'] as ThemeMode[]).map((m) => {
                    const Icon = MODE_ICONS[m];
                    return { value: m, label: <span className="inline-flex items-center gap-1.5"><Icon className="w-4 h-4" />{MODE_LABELS[m]}</span> };
                  })}
                />
              </div>
              <button
                type="button"
                className="ui-row has-icon sh-more-row"
                onClick={() => {
                  setMore(false);
                  setShowNotifModal(true);
                }}
              >
                <span className="ui-ico" style={{ '--ico-bg': '#FF9500', '--ico-fg': '#fff' } as React.CSSProperties}>
                  <Bell strokeWidth={2.1} />
                </span>
                <span className="ui-row-main">
                  <b>Bildirim geçmişi</b>
                  <span>AI redaksiyonları ve bildirimler</span>
                </span>
                {unreadNotifs > 0 ? (
                  <span className="ui-tag is-accent">{unreadNotifs}</span>
                ) : (
                  <ChevronRight className="w-4 h-4 shrink-0" style={{ color: 'var(--color-line-2)' }} />
                )}
              </button>
              <a href={pathFor('settings')} onClick={linkClick(() => go('settings'))} className="ui-row has-icon sh-more-row" aria-current={active === 'settings' ? 'page' : undefined}>
                <span className="ui-ico" style={{ '--ico-bg': NAV_ITEMS.settings.tint, '--ico-fg': '#fff' } as React.CSSProperties}><NAV_ITEMS.settings.icon strokeWidth={2.1} /></span>
                <span className="ui-row-main"><b>Profil ve ayarlar</b><span>Palet, yoğunluk, fotoğraf, klasik tasarım</span></span>
                <ChevronRight className="w-4 h-4 shrink-0" style={{ color: 'var(--color-line-2)' }} />
              </a>
              {onOffline && (
                <button type="button" className="ui-row has-icon" onClick={() => { setMore(false); onOffline(); }}>
                  <span className="ui-ico" style={{ '--ico-bg': '#30B0C7', '--ico-fg': '#fff' } as React.CSSProperties}><Database strokeWidth={2.1} /></span>
                  <span className="ui-row-main"><b>Çevrimdışı veritabanı</b><span>Soruları cihaza indir</span></span>
                </button>
              )}
              <button type="button" className="ui-row has-icon" onClick={() => { setMore(false); onPdf(); }}>
                <span className="ui-ico" style={{ '--ico-bg': '#5856D6', '--ico-fg': '#fff' } as React.CSSProperties}><FileDown strokeWidth={2.1} /></span>
                <span className="ui-row-main"><b>PDF indir</b><span>Kurul soruları A4 kitapçık</span></span>
              </button>
              {isAdmin && (
                <a href={pathFor('manage')} onClick={linkClick(() => go('manage'))} className="ui-row has-icon sh-more-row">
                  <span className="ui-ico" style={{ '--ico-bg': '#FF9500', '--ico-fg': '#fff' } as React.CSSProperties}><ShieldCheck strokeWidth={2.1} /></span>
                  <span className="ui-row-main"><b>Yönetim konsolu</b></span>
                  <ChevronRight className="w-4 h-4 shrink-0" style={{ color: 'var(--color-line-2)' }} />
                </a>
              )}
            </div>
          </section>
        </div>
      </Sheet>

      <NotificationHistoryModal isOpen={showNotifModal} onClose={() => setShowNotifModal(false)} />
    </>
  );
};
