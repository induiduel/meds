import React, { useEffect, useState } from 'react';
import { ChevronRight, Database, FileDown, LayoutGrid, Moon, ShieldCheck, Sun, SunMedium, Bell, Plus, CloudUpload } from 'lucide-react';
import { offlineDatabaseService } from '../../services/offlineDatabaseService';
import { prefetchRoute } from '../../routePrefetch';

/** Dokunuşta çok kısa titreşim (destekleyen telefonlarda) — uygulama hissi */
const buzz = () => {
  try { navigator.vibrate?.(6); } catch { /* yok */ }
};
import { linkClick, pathFor, type AppRoute } from '../../router';
import { MODE_LABELS, type ThemeMode, useAppearance } from '../../utils/appearance';
import { Segmented } from '../ui/kit';
import { Sheet } from '../ui/Sheet';
import { MORE_TREE, NAV_ITEMS, TAB_ITEMS } from './navModel';
import { userNotificationService } from '../../services/userNotificationService';
import { NotificationHistoryModal } from '../notifications/NotificationHistoryModal';

const MODE_ICONS: Record<ThemeMode, React.ElementType> = { light: Sun, sepia: SunMedium, dark: Moon };

/**
 * v9 alt gezinme (<768px): ekranın altında yüzen "ada". Öğren · Havuz · [+ Ekle] · Çıkmış · Daha.
 * Etkin sekmenin simgesi kendi renginde bir hapa oturur (yaylanarak), ortada yükseltilmiş ekle düğmesi.
 * Dokunuşta kısa titreşim, basılı tutunca sayfanın kodu önden yüklenir. Klavye açıkken gizlenir (html.kb-open).
 * "Daha" ortak Sheet'te: gruplu liste, hızlı tema, araçlar.
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

  const [queued, setQueued] = useState(() => offlineDatabaseService.getState().queuedActionsCount);
  useEffect(() => offlineDatabaseService.subscribe((st) => setQueued(st.queuedActionsCount)), []);
  const look = useAppearance();
  const inMore = !TAB_ITEMS.some((t) => t.id === active) && active !== 'practice';
  useEffect(() => setMore(false), [active]);

  const go = (r: AppRoute) => {
    setMore(false);
    onGo(r);
  };
  const [addTab, learnTab, poolTab, pastTab] = TAB_ITEMS;
  const tabLink = ({ id, short, label, icon: Icon, tint }: (typeof TAB_ITEMS)[number]) => {
    const on = active === id;
    return (
      <a
        key={id}
        href={pathFor(id)}
        onClick={linkClick(() => { if (!on) buzz(); go(id); })}
        onPointerDown={() => prefetchRoute(id)}
        aria-current={on ? 'page' : undefined}
        className="sh-tab"
        style={{ ['--tab-c' as string]: tint }}
      >
        <span className="sh-tab-pill"><Icon strokeWidth={on ? 2.3 : 1.9} /></span>
        <span className="sh-tab-l">{short || label}</span>
      </a>
    );
  };

  return (
    <>
      <nav aria-label="Alt gezinme" className="sh-tabs ms-hide-on-kb print:hidden">
        <div className="sh-tabs-in">
          {[learnTab, poolTab].map((t) => tabLink(t))}
          {/* Ortadaki birincil eylem: soru ekle (yükseltilmiş yuvarlak düğme) */}
          <a
            href={pathFor(addTab.id)}
            onClick={linkClick(() => { buzz(); go(addTab.id); })}
            aria-current={active === addTab.id ? 'page' : undefined}
            className="sh-tab-fab"
            aria-label={addTab.label}
          >
            <span className="sh-tab-fab-in"><Plus strokeWidth={2.6} /></span>
            <span className="sh-tab-fab-l">{addTab.short || addTab.label}</span>
          </a>
          {tabLink(pastTab)}
          <button
            type="button"
            className="sh-tab"
            onClick={() => { buzz(); setMore(true); }}
            aria-haspopup="dialog"
            aria-expanded={more}
            aria-current={inMore ? 'page' : undefined}
            style={{ ['--tab-c' as string]: 'var(--color-ink-2)' }}
          >
            <span className="sh-tab-pill"><LayoutGrid strokeWidth={inMore ? 2.3 : 1.9} />{(unreadNotifs > 0 || queued > 0) && <i className="sh-tab-dot" aria-hidden />}</span>
            <span className="sh-tab-l">Daha</span>
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
              <button
                type="button"
                className="ui-row has-icon sh-more-row"
                onClick={() => {
                  setMore(false);
                  window.dispatchEvent(new Event('medsoru:pending'));
                }}
              >
                <span className="ui-ico" style={{ '--ico-bg': queued ? 'var(--color-warn)' : '#34C759', '--ico-fg': '#fff' } as React.CSSProperties}>
                  <CloudUpload strokeWidth={2.1} />
                </span>
                <span className="ui-row-main">
                  <b>Gönderim kuyruğu</b>
                  <span>{queued ? 'Bağlantı bekleyen işlemler · gör, iptal et' : 'Bekleyen işlem yok'}</span>
                </span>
                {queued > 0 ? <span className="ui-tag is-warn">{queued}</span> : <ChevronRight className="w-4 h-4 shrink-0" style={{ color: 'var(--color-line-2)' }} />}
              </button>
              <a href={pathFor('settings')} onClick={linkClick(() => go('settings'))} className="ui-row has-icon sh-more-row" aria-current={active === 'settings' ? 'page' : undefined}>
                <span className="ui-ico" style={{ '--ico-bg': NAV_ITEMS.settings.tint, '--ico-fg': '#fff' } as React.CSSProperties}><NAV_ITEMS.settings.icon strokeWidth={2.1} /></span>
                <span className="ui-row-main"><b>Profil ve ayarlar</b><span>Palet, yoğunluk, fotoğraf</span></span>
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
