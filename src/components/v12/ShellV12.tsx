import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  Activity,
  Bell,
  ChevronDown,
  ChevronRight,
  CloudUpload,
  Database,
  FileDown,
  MoreHorizontal,
  Moon,
  PanelLeftClose,
  PanelLeftOpen,
  Plus,
  Search,
  ShieldCheck,
  Sun,
  SunMedium,
  UserRound,
} from 'lucide-react';
import { linkClick, pathFor, ROUTE_TITLES, type AppRoute } from '../../router';
import type { AppUser } from '../../services/auth';
import { pwaService } from '../../services/pwaService';
import { offlineDatabaseService } from '../../services/offlineDatabaseService';
import { userNotificationService } from '../../services/userNotificationService';
import { prefetchRoute } from '../../routePrefetch';
import { useReviewCounts } from '../../hooks/useReviewCounts';
import { MODE_LABELS, type ThemeMode, useAppearance } from '../../utils/appearance';
import { useTheme } from '../../utils/theme';
import { OfflineStatusBadge } from '../pwa/OfflineStatusBadge';
import { NotificationHistoryModal } from '../notifications/NotificationHistoryModal';
import { SearchPalette } from '../search/SearchPalette';
import { Segmented } from '../ui/kit';
import { Sheet } from '../ui/Sheet';
import { AccountMenu } from '../shell/AccountMenu';
import type { SideNavProps } from '../shell/SideNav';
import type { TopBarProps } from '../shell/TopBar';
import type { TabBarProps } from '../shell/TabBar';
import { BrandWord } from '../shell/BrandWord';
import { NAV_ITEMS, V12_MORE_TREE, V12_RAIL, V12_RAIL_MORE, V12_TABS, initialsOf, openSearch, type NavItem } from '../shell/navModel';
import { usePhone, useSearchShortcut, useSideCollapse } from '../shell/shellHooks';
import '../../styles/v12/shell.css';

/**
 * v12 "Net" uygulama kabuğu — canvas panoları Shell.dc.html (masaüstü ray + üst çubuk + komut paleti) ve
 * Mobile.dc.html (telefon üst/alt çubuğu, tablet). Klasik kabukla (shell/SideNav, TopBar, TabBar) aynı props ve
 * işlevler; yalnız html[data-design='v12'] iken o bileşenlerin içinden çağrılır. Stiller: styles/v12/shell.css (s12-*).
 *
 * Sayfa üst çubuğa kendi bağlamsal denetimini (kurul seçimi, sayaç, "Test oluştur"…) koymak isterse
 * <TopBarSlotV12> ile koyar; çubuk yoksa (v10/v11) hiçbir şey çizilmez.
 */

/** Dokunuşta çok kısa titreşim (destekleyen telefonlarda) */
const buzz = () => {
  try {
    navigator.vibrate?.(6);
  } catch {
    /* yok */
  }
};

/** Vadesi gelen ezber kartları (TodayView ile aynı depo, aynı ölçüt) */
const readDueCards = () => {
  try {
    const store = JSON.parse(localStorage.getItem('medsoru_flashcards_v1') || '{}') as Record<string, { due?: number } | null>;
    const now = Date.now();
    let n = 0;
    for (const s of Object.values(store)) if (s && typeof s.due === 'number' && s.due <= now) n++;
    return n;
  } catch {
    return 0;
  }
};

/** Menüdeki sayaçlar: yalnız gerçek, cihazdaki veriden (hata defteri vadesi + vadesi gelen kartlar) */
const useNavCounts = (active: AppRoute): Partial<Record<AppRoute, { n: number; hint: string }>> => {
  const review = useReviewCounts();
  const [cards, setCards] = useState(0);
  useEffect(() => {
    // Sayfa değişiminde boşta okunur: ilk boyamayı geciktirmez
    const w = window as Window & { requestIdleCallback?: (cb: () => void) => number; cancelIdleCallback?: (id: number) => void };
    if (w.requestIdleCallback) {
      const id = w.requestIdleCallback(() => setCards(readDueCards()));
      return () => w.cancelIdleCallback?.(id);
    }
    const t = window.setTimeout(() => setCards(readDueCards()), 200);
    return () => window.clearTimeout(t);
  }, [active]);
  return {
    learn: review.total.due > 0 ? { n: review.total.due, hint: 'hata defterinde vadesi gelen öge' } : undefined,
    flashcards: cards > 0 ? { n: cards, hint: 'vadesi gelen kart' } : undefined,
  };
};

const useUnread = () => {
  const [unread, setUnread] = useState(0);
  useEffect(() => userNotificationService.subscribe((list) => setUnread(list.filter((n) => !n.read).length)), []);
  return unread;
};

const Avatar: React.FC<{ user: AppUser | null; size: number }> = ({ user, size }) => (
  <span className="s12-av" style={{ '--s12-av': `${size}px` } as React.CSSProperties} aria-hidden="true">
    {user?.photoURL ? <img src={user.photoURL} alt="" /> : user ? initialsOf(user) : <UserRound />}
  </span>
);

/* =============================================================================
 * Kenar rayı (≥768px). Tablette 64px simge rayı; masaüstünde 224px, daraltılabilir.
 * ============================================================================= */
export const SideNavV12: React.FC<SideNavProps> = ({
  active,
  onGo,
  isAdmin,
  user,
}) => {
  const { collapsed, setCollapsed } = useSideCollapse();
  const counts = useNavCounts(active);
  const inMore = V12_RAIL_MORE.some((g) => g.items.some((it) => it.id === active));
  const [moreOpen, setMoreOpen] = useState(inMore);
  // Etkin sayfa "Daha fazla" içindeyse açılır kendiliğinden açılır (seçili satır hep görünür)
  useEffect(() => {
    if (inMore) setMoreOpen(true);
  }, [inMore]);
  // Etkin satır listenin görünmeyen kısmında kalmasın (uzun "Daha fazla" listesi kısa ekranda kayar)
  const listRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const box = listRef.current;
    const el = box?.querySelector<HTMLElement>('[aria-current="page"]');
    if (!box || !el) return;
    const top = el.offsetTop - box.offsetTop;
    if (top < box.scrollTop || top + el.offsetHeight > box.scrollTop + box.clientHeight) box.scrollTop = Math.max(0, top - box.clientHeight / 3);
  }, [active, moreOpen]);

  const link = (it: Pick<NavItem, 'id' | 'label' | 'icon'>) => {
    const on = active === it.id;
    const c = counts[it.id];
    const Icon = it.icon;
    return (
      <a
        key={it.id}
        href={pathFor(it.id)}
        onClick={linkClick(() => onGo(it.id))}
        onPointerEnter={() => prefetchRoute(it.id)}
        aria-current={on ? 'page' : undefined}
        className="s12-nav"
        title={c ? `${it.label} · ${c.n} ${c.hint}` : it.label}
      >
        <Icon className="s12-ico" strokeWidth={on ? 2.1 : 1.8} aria-hidden="true" />
        <span className="s12-l">{it.label}</span>
        {c && (
          <span className="s12-c">
            <span aria-hidden="true">{c.n > 99 ? '99+' : c.n}</span>
            <span className="sr-only">, {c.n} {c.hint}</span>
          </span>
        )}
      </a>
    );
  };

  return (
    <nav aria-label="Ana menü" className="s12-rail print:hidden" data-collapsed={collapsed ? 'true' : undefined}>
      <div className="s12-rail-top">
        <a href={pathFor('quick_add')} onClick={linkClick(() => onGo('quick_add'))} className="s12-brand" aria-label="MeDSor ana sayfa">
          <span className="s12-brand-mark" aria-hidden="true"><Activity strokeWidth={2.4} /></span>
          <BrandWord className="s12-brand-word" />
        </a>
        <button
          type="button"
          className="s12-rail-toggle"
          onClick={() => setCollapsed((c) => !c)}
          aria-label={collapsed ? 'Menüyü genişlet' : 'Menüyü daralt'}
          aria-expanded={!collapsed}
          title={collapsed ? 'Menüyü genişlet' : 'Menüyü daralt'}
        >
          {collapsed ? <PanelLeftOpen aria-hidden="true" /> : <PanelLeftClose aria-hidden="true" />}
        </button>
      </div>

      <button type="button" className="s12-rail-search" onClick={openSearch} aria-label="Ara ya da git" title="Ara ya da git ( / ya da Ctrl+K )">
        <Search className="s12-ico" aria-hidden="true" />
        <span className="s12-l">Ara ya da git</span>
        <kbd className="s12-kbd s12-l" aria-hidden="true">⌘K</kbd>
      </button>

      <div className="s12-rail-list" ref={listRef}>
        {V12_RAIL.map((g, gi) => (
          <div key={g.label || gi} className="s12-rail-grp" role="group" aria-label={g.label || 'Sayfalar'}>
            {g.label && <span className="s12-grp" aria-hidden="true">{g.label}</span>}
            {g.items.map(link)}
          </div>
        ))}

        <button
          type="button"
          className="s12-nav s12-more-btn"
          onClick={() => setMoreOpen((v) => !v)}
          aria-expanded={moreOpen}
          aria-controls="s12-rail-more"
          title="Daha fazla"
        >
          <MoreHorizontal className="s12-ico" strokeWidth={1.8} aria-hidden="true" />
          <span className="s12-l">Daha fazla</span>
          <ChevronDown className="s12-chev s12-l" aria-hidden="true" />
        </button>
        {moreOpen && (
          <div id="s12-rail-more" className="s12-rail-more">
            {V12_RAIL_MORE.map((g) => (
              <div key={g.label} className="s12-rail-grp" role="group" aria-label={g.label || undefined}>
                {g.label && <span className="s12-grp" aria-hidden="true">{g.label}</span>}
                {g.items.map(link)}
              </div>
            ))}
          </div>
        )}

        {isAdmin && (
          <div className="s12-rail-grp s12-rail-admin" role="group" aria-label="Yönetim">
            {link({ id: 'manage', label: 'Yönetim konsolu', icon: ShieldCheck })}
          </div>
        )}
      </div>

      <a
        href={pathFor('settings')}
        onClick={linkClick(() => onGo('settings'))}
        aria-current={active === 'settings' ? 'page' : undefined}
        className="s12-nav s12-me"
        title="Profil ve ayarlar"
      >
        <Avatar user={user} size={24} />
        <span className="s12-l s12-me-t">
          <b>{user ? user.displayName || user.email?.split('@')[0] : 'Giriş yapmadın'}</b>
          <span>Profil ve ayarlar</span>
        </span>
      </a>
    </nav>
  );
};

/* =============================================================================
 * Üst çubuk: sayfa adı · bağlamsal yuva · araçlar (çevrimdışı, ara, tema, bildirim, soru ekle, hesap)
 * ============================================================================= */
export const TOP_SLOT_ID = 's12-top-slot';

/** Sayfanın üst çubuğa bağlamsal denetim koyması için (yalnız v12'de görünür) */
export const TopBarSlotV12: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [el, setEl] = useState<HTMLElement | null>(null);
  useLayoutEffect(() => setEl(document.getElementById(TOP_SLOT_ID)), []);
  return el ? createPortal(children, el) : null;
};

export const TopBarV12: React.FC<TopBarProps> = ({ active, onGo, user, isAdmin, searchQuery = '', onSearch, onOpenOffline, actions }) => {
  const phone = usePhone();
  const { theme, toggle } = useTheme();
  const [menu, setMenu] = useState(false);
  const [search, setSearch] = useState(false);
  const [canInstall, setCanInstall] = useState(pwaService.getState().canInstall);
  const [showNotifModal, setShowNotifModal] = useState(false);
  const unread = useUnread();

  useEffect(() => pwaService.subscribe((s) => setCanInstall(s.canInstall)), []);
  useEffect(() => setMenu(false), [active]);
  useSearchShortcut(() => setSearch(true));

  const title = ROUTE_TITLES[active];
  const dark = theme === 'dark';

  return (
    <header className="s12-top print:hidden">
      <div className="s12-top-in">
        <span className="s12-top-t">{title}</span>
        <div id={TOP_SLOT_ID} className="s12-top-ctx" />

        <div className="s12-top-tools">
          <OfflineStatusBadge onClick={() => onOpenOffline?.()} isAdmin={isAdmin} className="s12-ofb" />
          <button type="button" className="s12-ib s12-only-phone" onClick={() => setSearch(true)} aria-label="Ara">
            <Search aria-hidden="true" />
          </button>
          <button
            type="button"
            className="s12-ib s12-hide-phone"
            onClick={toggle}
            aria-label={dark ? 'Aydınlık temaya geç' : 'Koyu temaya geç'}
            title={dark ? 'Aydınlık tema' : 'Koyu tema'}
          >
            {dark ? <Sun aria-hidden="true" /> : <Moon aria-hidden="true" />}
          </button>
          <button
            type="button"
            className="s12-ib s12-hide-phone s12-bell"
            onClick={() => setShowNotifModal(true)}
            aria-label={unread ? `Bildirimler, ${unread} okunmamış` : 'Bildirimler'}
            title="Bildirimler"
          >
            <Bell aria-hidden="true" />
            {unread > 0 && <span className="s12-dotn" aria-hidden="true">{unread > 9 ? '9+' : unread}</span>}
          </button>
          <a
            href={pathFor('quick_add')}
            onClick={linkClick(() => onGo('quick_add'))}
            aria-current={active === 'quick_add' ? 'page' : undefined}
            className="s12-add s12-hide-phone"
            aria-label="Soru ekle"
            title="Soru ekle"
          >
            <Plus aria-hidden="true" />
            <span aria-hidden="true">Soru ekle</span>
          </a>
          <div className="s12-acct-anchor">
            <button
              type="button"
              className={`s12-acct ${menu ? 'is-open' : ''}`}
              onClick={() => setMenu((v) => !v)}
              aria-haspopup="dialog"
              aria-expanded={menu}
              aria-label={unread ? `Hesap ve araçlar, ${unread} okunmamış bildirim` : 'Hesap ve araçlar'}
            >
              <Avatar user={user} size={30} />
              {unread > 0 && <i className="s12-acct-dot s12-only-phone" aria-hidden="true" />}
            </button>
            <AccountMenu
              open={menu}
              onClose={() => setMenu(false)}
              user={user}
              phone={phone}
              actions={{
                ...actions,
                onNotifications: () => setShowNotifModal(true),
                onInstall: canInstall ? () => pwaService.promptInstall() : undefined,
              }}
            />
          </div>
        </div>
      </div>

      {search && (
        <SearchPalette
          initialQuery={searchQuery}
          onClose={() => setSearch(false)}
          onOpenResults={(q, focusId, hit) => onSearch?.(q, focusId, hit)}
          onGo={onGo}
        />
      )}

      <NotificationHistoryModal isOpen={showNotifModal} onClose={() => setShowNotifModal(false)} />
    </header>
  );
};

/* =============================================================================
 * Telefon alt çubuğu (<768px): kenara oturan düz çubuk. Bugün · Öğren · [+] · Çıkmış · Daha
 * ============================================================================= */
const MODE_ICONS: Record<ThemeMode, React.ElementType> = { light: Sun, sepia: SunMedium, dark: Moon };

export const TabBarV12: React.FC<TabBarProps> = ({ active, onGo, isAdmin, onPdf, onOffline }) => {
  const [more, setMore] = useState(false);
  const [showNotifModal, setShowNotifModal] = useState(false);
  const unread = useUnread();
  const [queued, setQueued] = useState(() => offlineDatabaseService.getState().queuedActionsCount);
  useEffect(() => offlineDatabaseService.subscribe((st) => setQueued(st.queuedActionsCount)), []);
  const look = useAppearance();
  const inMore = !V12_TABS.some((t) => t.id === active);
  useEffect(() => setMore(false), [active]);
  // Tanıtım turu "Daha" sayfasını açıp kapatır (WelcomeTour → medsoru:more)
  useEffect(() => {
    const on = (e: Event) => setMore(Boolean((e as CustomEvent<{ open?: boolean }>).detail?.open));
    window.addEventListener('medsoru:more', on);
    return () => window.removeEventListener('medsoru:more', on);
  }, []);

  const go = (r: AppRoute) => {
    setMore(false);
    onGo(r);
  };
  const [todayTab, learnTab, addTab, pastTab] = V12_TABS;
  const tab = ({ id, short, label, icon: Icon }: NavItem) => {
    const on = active === id;
    return (
      <a
        key={id}
        href={pathFor(id)}
        onClick={linkClick(() => {
          if (!on) buzz();
          go(id);
        })}
        onPointerDown={() => prefetchRoute(id)}
        aria-current={on ? 'page' : undefined}
        className="s12-tab"
      >
        <span className="s12-tab-ic"><Icon strokeWidth={on ? 2.1 : 1.8} aria-hidden="true" /></span>
        <span className="s12-tab-l">{short || label}</span>
      </a>
    );
  };

  const row = (key: string, Icon: React.ElementType, label: string, hint: string | undefined, end: React.ReactNode, props: { href?: string; onClick: () => void; current?: boolean }) => {
    const body = (
      <>
        <Icon className="s12-ico" strokeWidth={1.8} aria-hidden="true" />
        <span className="s12-mrow-t">
          <b>{label}</b>
          {hint && <span>{hint}</span>}
        </span>
        {end ?? <ChevronRight className="s12-mrow-chev" aria-hidden="true" />}
      </>
    );
    return props.href ? (
      <a key={key} href={props.href} onClick={linkClick(props.onClick)} aria-current={props.current ? 'page' : undefined} className="s12-mrow">
        {body}
      </a>
    ) : (
      <button key={key} type="button" onClick={props.onClick} className="s12-mrow">
        {body}
      </button>
    );
  };

  return (
    <>
      <nav aria-label="Alt gezinme" className="s12-tabs ms-hide-on-kb print:hidden">
        {tab(todayTab)}
        {tab(learnTab)}
        <a
          href={pathFor(addTab.id)}
          onClick={linkClick(() => {
            buzz();
            go(addTab.id);
          })}
          aria-current={active === addTab.id ? 'page' : undefined}
          className="s12-tab s12-tab-add"
          aria-label={addTab.label}
        >
          <span className="s12-tab-plus"><Plus strokeWidth={2.2} aria-hidden="true" /></span>
        </a>
        {tab(pastTab)}
        <button
          type="button"
          className="s12-tab"
          onClick={() => {
            buzz();
            setMore(true);
          }}
          aria-haspopup="dialog"
          aria-expanded={more}
          aria-current={inMore ? 'page' : undefined}
          aria-label={unread || queued ? 'Daha fazla, yeni bildirim ya da bekleyen işlem var' : 'Daha fazla'}
        >
          <span className="s12-tab-ic">
            <MoreHorizontal strokeWidth={inMore ? 2.1 : 1.8} aria-hidden="true" />
            {(unread > 0 || queued > 0) && <i className="s12-tab-dot" aria-hidden="true" />}
          </span>
          <span className="s12-tab-l" aria-hidden="true">Daha</span>
        </button>
      </nav>

      <Sheet open={more} onClose={() => setMore(false)} title="Daha fazla" size="auto">
        <div className="s12-more">
          {V12_MORE_TREE.map((g) => (
            <section key={g.label} className="s12-msec" aria-label={g.label || undefined}>
              {g.label && <h2 className="s12-msec-h">{g.label}</h2>}
              <div className="s12-mlist">
                {g.items.map(({ id, label, hint, icon }) => row(id, icon, label, hint, undefined, { href: pathFor(id), onClick: () => go(id), current: active === id }))}
              </div>
            </section>
          ))}

          <section className="s12-msec" aria-label="Görünüm ve hesap">
            <h2 className="s12-msec-h">Görünüm ve hesap</h2>
            <div className="s12-mtheme">
              <Segmented<ThemeMode>
                className="flex-1"
                label="Tema"
                value={look.mode}
                onChange={(m) => look.set({ mode: m })}
                options={(['light', 'sepia', 'dark'] as ThemeMode[]).map((m) => {
                  const Icon = MODE_ICONS[m];
                  return { value: m, label: <span className="inline-flex items-center gap-1.5"><Icon className="w-4 h-4" aria-hidden="true" />{MODE_LABELS[m]}</span> };
                })}
              />
            </div>
            <div className="s12-mlist">
              {row('notif', Bell, 'Bildirim geçmişi', 'Yapay zekâ düzeltmeleri ve bildirimler', unread > 0 ? <span className="s12-badge is-acc">{unread}</span> : undefined, {
                onClick: () => {
                  setMore(false);
                  setShowNotifModal(true);
                },
              })}
              {row('queue', CloudUpload, 'Gönderim kuyruğu', queued ? 'Bağlantı bekleyen işlemler · gör, iptal et' : 'Bekleyen işlem yok', queued > 0 ? <span className="s12-badge is-warn">{queued}</span> : undefined, {
                onClick: () => {
                  setMore(false);
                  window.dispatchEvent(new Event('medsoru:pending'));
                },
              })}
              {row('settings', NAV_ITEMS.settings.icon, 'Profil ve ayarlar', 'Palet, yoğunluk, fotoğraf', undefined, { href: pathFor('settings'), onClick: () => go('settings'), current: active === 'settings' })}
              {onOffline &&
                row('offline', Database, 'Çevrimdışı veritabanı', 'Soruları cihaza indir', undefined, {
                  onClick: () => {
                    setMore(false);
                    onOffline();
                  },
                })}
              {row('pdf', FileDown, 'PDF indir', 'Kurul soruları A4 kitapçık', undefined, {
                onClick: () => {
                  setMore(false);
                  onPdf();
                },
              })}
              {isAdmin && row('manage', ShieldCheck, 'Yönetim konsolu', undefined, undefined, { href: pathFor('manage'), onClick: () => go('manage'), current: active === 'manage' })}
            </div>
          </section>
        </div>
      </Sheet>

      <NotificationHistoryModal isOpen={showNotifModal} onClose={() => setShowNotifModal(false)} />
    </>
  );
};
