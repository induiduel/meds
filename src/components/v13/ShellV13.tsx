import React, { useEffect, useId, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  Activity,
  Bell,
  ChevronUp,
  CloudUpload,
  Database,
  FileDown,
  LayoutGrid,
  Maximize2,
  Minimize2,
  Moon,
  PanelLeftClose,
  PanelLeftOpen,
  Plus,
  Search,
  ShieldCheck,
  Smartphone,
  Sun,
  SunMedium,
  UserRound,
  X,
} from 'lucide-react';
import { linkClick, pathFor, ROUTE_TITLES, type AppRoute } from '../../router';
import type { AppUser } from '../../services/auth';
import { pwaService } from '../../services/pwaService';
import { offlineDatabaseService } from '../../services/offlineDatabaseService';
import { userNotificationService } from '../../services/userNotificationService';
import { prefetchRoute } from '../../routePrefetch';
import { useReviewCounts } from '../../hooks/useReviewCounts';
import { DESIGN_CHOICES, DESIGN_CHOICE_LABELS, MODE_LABELS, designChoiceOf, type ThemeMode, useAppearance } from '../../utils/appearance';
import { useTheme } from '../../utils/theme';
import { useAppFullscreen } from '../../utils/fullscreen';
import { OfflineStatusBadge } from '../pwa/OfflineStatusBadge';
import { GuncellemeSimgesi } from '../system/UpdatePrompt';
import { NotificationHistoryModal } from '../notifications/NotificationHistoryModal';
import { SearchPalette } from '../search/SearchPalette';
import { Sheet } from '../ui/Sheet';
import { AccountMenu } from '../shell/AccountMenu';
import type { SideNavProps } from '../shell/SideNav';
import type { TopBarProps } from '../shell/TopBar';
import type { TabBarProps } from '../shell/TabBar';
import { BrandWord } from '../shell/BrandWord';
import { NAV_ITEMS, initialsOf, openSearch, type NavItem } from '../shell/navModel';
import { matchPages } from '../shell/phoneNav';
import { usePhone, useSearchShortcut, useSideCollapse } from '../shell/shellHooks';
import { TOP_SLOT_ID } from '../v12/ShellV12';
import { V13_GROUPS, groupOf, lastIn, rememberLast, type V13Group } from './navGroups';
import '../../styles/v13/shell.css';

/**
 * v13 "Ada" uygulama kabuğu. Tam genişlik şerit yoktur: her parça kenarlardan ayrık, yuvarlak bir "ada"dır.
 *  - Kenar adası (≥768 px): omurga (niyet öbekleri) + panel (öbeğin sayfaları). Geniş ekranda panel sabit açık,
 *    tablette ve daraltılınca omurganın yanında açılır kutu. Her sayfa en çok iki tıkta.
 *  - Başlık kapsülü: sayfa sütunuyla aynı genişlikte, yapışkan; sayfa adı · bağlamsal yuva (TopBarSlotV12) · araçlar.
 *  - Alt ada (<768 px): Bugün · Ders · [+] · Çöz · Menü. Öbek düğmesi öbekte son açılan sayfaya götürür; öbekteyken
 *    yeniden dokunulursa öbeğin sayfa listesi açılır. Menü: sayfa arama, tüm öbekler, tema, araçlar, tasarım.
 * Sayfa içerikleri v12 bileşenleridir (design = 'v12'); stiller styles/v13/shell.css (a13-*).
 */

const buzz = () => {
  try {
    navigator.vibrate?.(6);
  } catch {
    /* yok */
  }
};

const useUnread = () => {
  const [unread, setUnread] = useState(0);
  useEffect(() => userNotificationService.subscribe((list) => setUnread(list.filter((n) => !n.read).length)), []);
  return unread;
};

const useMedia = (q: string) => {
  const [m, setM] = useState(() => typeof window !== 'undefined' && window.matchMedia(q).matches);
  useEffect(() => {
    const mq = window.matchMedia(q);
    const on = () => setM(mq.matches);
    on();
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, [q]);
  return m;
};

/** Menü sayaçları: hata defterinde vadesi gelenler (Öğren) */
const useCounts = (): Partial<Record<AppRoute, number>> => {
  const review = useReviewCounts();
  return { learn: review.total.due > 0 ? review.total.due : undefined } as Partial<Record<AppRoute, number>>;
};

const Avatar: React.FC<{ user: AppUser | null; size: number }> = ({ user, size }) => (
  <span className="a13-av" style={{ '--a13-av': `${size}px` } as React.CSSProperties} aria-hidden="true">
    {user?.photoURL ? <img src={user.photoURL} alt="" /> : user ? initialsOf(user) : <UserRound />}
  </span>
);

/** Rota değişince öbeğin son sayfası hatırlanır */
const useRememberRoute = (active: AppRoute) => {
  useEffect(() => rememberLast(active), [active]);
};

/** Bir öbeğin sayfa listesi (kenar paneli, açılır kutu ve alt ada açılırı aynı listeyi kullanır) */
const PageList: React.FC<{ group: V13Group; active: AppRoute; onPick: (r: AppRoute) => void; counts?: Partial<Record<AppRoute, number>> }> = ({
  group,
  active,
  onPick,
  counts = {},
}) => (
  <ul className="a13-plist" role="list">
    {group.items.map((it) => {
      const on = it.id === active;
      const Icon = it.icon;
      const n = counts[it.id];
      return (
        <li key={it.id}>
          <a
            href={pathFor(it.id)}
            onClick={linkClick(() => onPick(it.id))}
            onPointerEnter={() => prefetchRoute(it.id)}
            onFocus={() => prefetchRoute(it.id)}
            aria-current={on ? 'page' : undefined}
            className="a13-plink"
            title={it.hint}
          >
            <Icon className="a13-ico" strokeWidth={on ? 2.1 : 1.8} aria-hidden="true" />
            <span className="a13-plink-t">{it.label}</span>
            {n ? (
              <span className="a13-count">
                <span aria-hidden="true">{n > 99 ? '99+' : n}</span>
                <span className="sr-only">, {n} vadesi gelen öge</span>
              </span>
            ) : null}
          </a>
        </li>
      );
    })}
  </ul>
);

/* =============================================================================
 * Kenar adası (≥768 px)
 * ============================================================================= */
export const SideNavV13: React.FC<SideNavProps> = ({ active, onGo, isAdmin, user }) => {
  useRememberRoute(active);
  const { collapsed, setCollapsed } = useSideCollapse();
  const wideScreen = useMedia('(min-width: 1180px)');
  const docked = wideScreen && !collapsed;
  const counts = useCounts();
  const activeGroup = groupOf(active);
  const [view, setView] = useState<V13Group['id']>(activeGroup?.id && activeGroup.id !== 'bugun' ? activeGroup.id : 'ders');
  const [fly, setFly] = useState(false);
  // Panel öbeği kullanıcı seçti mi (seçmediyse yalnız açık sayfanın öbeği vurgulanır)
  const [picked, setPicked] = useState(false);
  const rootRef = useRef<HTMLElement>(null);
  const panelId = useId();

  // Sayfa değişince panel etkin öbeğe döner, açılır kutu kapanır
  useEffect(() => {
    const g = groupOf(active);
    if (g && g.id !== 'bugun') setView(g.id);
    setFly(false);
    setPicked(false);
  }, [active]);

  // Açılır kutu: dışarı tıklama ve Escape kapatır
  useEffect(() => {
    if (!fly) return;
    const down = (e: PointerEvent) => {
      if (!rootRef.current?.contains(e.target as Node)) setFly(false);
    };
    const key = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setFly(false);
        rootRef.current?.querySelector<HTMLElement>(`[data-g="${view}"]`)?.focus();
      }
    };
    document.addEventListener('pointerdown', down);
    document.addEventListener('keydown', key);
    return () => {
      document.removeEventListener('pointerdown', down);
      document.removeEventListener('keydown', key);
    };
  }, [fly, view]);

  const go = (r: AppRoute) => {
    setFly(false);
    onGo(r);
  };
  const viewGroup = V13_GROUPS.find((g) => g.id === view) || V13_GROUPS[1];
  const panelShown = docked || fly;

  return (
    <nav ref={rootRef} aria-label="Ana menü" className="a13-side print:hidden" data-docked={docked ? 'true' : undefined}>
      <div className="a13-spine">
        <a href={pathFor('quick_add')} onClick={linkClick(() => go('quick_add'))} className="a13-mark" aria-label="MeDSor ana sayfa" title="MeDSor">
          <Activity strokeWidth={2.4} aria-hidden="true" />
        </a>
        <button type="button" className="a13-sbtn" onClick={openSearch} aria-label="Ara ya da git (Ctrl+K)" title="Ara ya da git ( / ya da Ctrl+K )">
          <Search aria-hidden="true" />
          <span className="a13-sbtn-l">Ara</span>
        </button>
        <a
          href={pathFor('quick_add')}
          onClick={linkClick(() => go('quick_add'))}
          aria-current={active === 'quick_add' ? 'page' : undefined}
          className="a13-sbtn a13-add"
          title="Soru ekle"
        >
          <Plus aria-hidden="true" />
          <span className="a13-sbtn-l">Ekle</span>
        </a>
        <span className="a13-sep" aria-hidden="true" />
        <div className="a13-groups" role="group" aria-label="Bölümler">
          {V13_GROUPS.map((g) => {
            const Icon = g.icon;
            const here = activeGroup?.id === g.id;
            if (g.id === 'bugun') {
              return (
                <a
                  key={g.id}
                  href={pathFor('today')}
                  onClick={linkClick(() => go('today'))}
                  aria-current={active === 'today' ? 'page' : undefined}
                  className="a13-sbtn"
                  data-g={g.id}
                  title="Bugün"
                >
                  <Icon aria-hidden="true" />
                  <span className="a13-sbtn-l">{g.short}</span>
                </a>
              );
            }
            const viewing = panelShown && view === g.id && (here || picked || fly);
            return (
              <button
                key={g.id}
                type="button"
                data-g={g.id}
                className={`a13-sbtn ${here ? 'is-here' : ''} ${viewing ? 'is-view' : ''}`}
                aria-expanded={docked ? undefined : fly && view === g.id}
                aria-pressed={docked ? view === g.id : undefined}
                aria-controls={panelShown ? panelId : undefined}
                title={g.label}
                onClick={() => {
                  if (docked) {
                    setView(g.id);
                    setPicked(true);
                    return;
                  }
                  if (fly && view === g.id) setFly(false);
                  else {
                    setView(g.id);
                    setFly(true);
                  }
                }}
              >
                <Icon aria-hidden="true" />
                <span className="a13-sbtn-l">{g.short}</span>
                {here && <span className="sr-only"> (açık sayfa bu bölümde)</span>}
              </button>
            );
          })}
        </div>
        <span className="a13-grow" />
        {isAdmin && (
          <a
            href={pathFor('manage')}
            onClick={linkClick(() => go('manage'))}
            aria-current={active === 'manage' ? 'page' : undefined}
            className="a13-sbtn"
            title="Yönetim konsolu"
          >
            <ShieldCheck aria-hidden="true" />
            <span className="a13-sbtn-l">Yönetim</span>
          </a>
        )}
        {wideScreen && (
          <button
            type="button"
            className="a13-sbtn a13-toggle"
            onClick={() => setCollapsed((c) => !c)}
            aria-label={collapsed ? 'Sayfa panelini aç' : 'Sayfa panelini kapat'}
            aria-expanded={!collapsed}
            title={collapsed ? 'Sayfa panelini aç' : 'Sayfa panelini kapat'}
          >
            {collapsed ? <PanelLeftOpen aria-hidden="true" /> : <PanelLeftClose aria-hidden="true" />}
          </button>
        )}
        <a
          href={pathFor('settings')}
          onClick={linkClick(() => go('settings'))}
          aria-current={active === 'settings' ? 'page' : undefined}
          className="a13-sbtn a13-me"
          title={user ? `${user.displayName || user.email || ''} · Profil ve ayarlar` : 'Profil ve ayarlar'}
          aria-label="Profil ve ayarlar"
        >
          <Avatar user={user} size={28} />
        </a>
      </div>

      {panelShown && (
        <div id={panelId} className={`a13-panel ${docked ? '' : 'is-fly'}`} role={docked ? undefined : 'dialog'} aria-label={viewGroup.label}>
          <div className="a13-panel-h">
            {docked ? <BrandWord className="a13-brandword" /> : <b>{viewGroup.label}</b>}
            {!docked && (
              <button type="button" className="a13-x" onClick={() => setFly(false)} aria-label="Kapat">
                <X aria-hidden="true" />
              </button>
            )}
          </div>
          {docked && <p className="a13-panel-g">{viewGroup.label}</p>}
          <div className="a13-panel-body">
            <PageList group={viewGroup} active={active} onPick={go} counts={counts} />
          </div>
        </div>
      )}
    </nav>
  );
};

/* =============================================================================
 * Başlık kapsülü
 * ============================================================================= */
export const TopBarV13: React.FC<TopBarProps> = ({ active, onGo, user, isAdmin, searchQuery = '', onSearch, onOpenOffline, actions }) => {
  const phone = usePhone();
  const { theme, toggle } = useTheme();
  const [appFs, toggleAppFs, exitAppFs] = useAppFullscreen();
  const [menu, setMenu] = useState(false);
  const [search, setSearch] = useState(false);
  const [canInstall, setCanInstall] = useState(pwaService.getState().canInstall);
  const [showNotifModal, setShowNotifModal] = useState(false);
  const unread = useUnread();

  useEffect(() => pwaService.subscribe((s) => setCanInstall(s.canInstall)), []);
  useEffect(() => setMenu(false), [active]);
  useSearchShortcut(() => setSearch(true));

  const title = ROUTE_TITLES[active];
  const group = groupOf(active);
  const dark = theme === 'dark';

  return (
    <header className="a13-top print:hidden">
      <div className="a13-cap">
        <div className="a13-title">
          {group && group.id !== 'bugun' && <span className="a13-crumb">{group.label}</span>}
          <p className="a13-h">{title}</p>
        </div>
        <div id={TOP_SLOT_ID} className="a13-ctx" />
        <div className="a13-tools">
          <OfflineStatusBadge onClick={() => onOpenOffline?.()} isAdmin={isAdmin} className="a13-ofb" />
          <GuncellemeSimgesi className="a13-ib" />
          <button type="button" className="a13-ib a13-find" onClick={() => setSearch(true)} aria-label="Ara" title="Ara ( / ya da Ctrl+K )">
            <Search aria-hidden="true" />
            <span className="a13-find-l" aria-hidden="true">Ara</span>
          </button>
          {canInstall && (
            <button type="button" className="a13-ib a13-hide-phone" onClick={() => pwaService.promptInstall()} aria-label="Uygulamayı cihaza yükle" title="Uygulamayı cihaza yükle">
              <Smartphone aria-hidden="true" />
            </button>
          )}
          <button
            type="button"
            className="a13-ib a13-hide-phone"
            onClick={() => toggleAppFs()}
            aria-label={appFs ? 'Tam ekrandan çık' : 'Tam ekran'}
            title={appFs ? 'Tam ekrandan çık' : 'Tam ekran: menüleri gizle'}
          >
            {appFs ? <Minimize2 aria-hidden="true" /> : <Maximize2 aria-hidden="true" />}
          </button>
          <button
            type="button"
            className="a13-ib a13-hide-phone"
            onClick={toggle}
            aria-label={dark ? 'Açık temaya geç' : 'Koyu temaya geç'}
            title={dark ? 'Açık tema' : 'Koyu tema'}
          >
            {dark ? <Sun aria-hidden="true" /> : <Moon aria-hidden="true" />}
          </button>
          <button
            type="button"
            className="a13-ib a13-hide-phone"
            onClick={() => setShowNotifModal(true)}
            aria-label={unread ? `Bildirimler, ${unread} okunmamış` : 'Bildirimler'}
            title="Bildirimler"
          >
            <Bell aria-hidden="true" />
            {unread > 0 && <span className="a13-dotn" aria-hidden="true">{unread > 9 ? '9+' : unread}</span>}
          </button>
          <div className="a13-acct-anchor">
            <button
              type="button"
              className={`a13-acct ${menu ? 'is-open' : ''}`}
              onClick={() => setMenu((v) => !v)}
              aria-haspopup="dialog"
              aria-expanded={menu}
              aria-label={unread ? `Hesap ve araçlar, ${unread} okunmamış bildirim` : 'Hesap ve araçlar'}
            >
              <Avatar user={user} size={28} />
              {unread > 0 && <i className="a13-acct-dot" aria-hidden="true" />}
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
      {appFs &&
        createPortal(
          <button type="button" className="s12-fs-exit a13-fs-exit print:hidden" onClick={exitAppFs} aria-label="Tam ekrandan çık" title="Tam ekrandan çık (Esc)">
            <Minimize2 aria-hidden="true" />
            <span>Tam ekrandan çık</span>
          </button>,
          document.body,
        )}
    </header>
  );
};

/* =============================================================================
 * Alt ada (<768 px)
 * ============================================================================= */
const MODE_ICONS: Record<ThemeMode, React.ElementType> = { light: Sun, sepia: SunMedium, dark: Moon };
const ISLAND: V13Group['id'][] = ['bugun', 'ders', 'coz'];

export const TabBarV13: React.FC<TabBarProps> = ({ active, onGo, isAdmin, onPdf, onOffline }) => {
  useRememberRoute(active);
  const look = useAppearance();
  const counts = useCounts();
  const [menu, setMenu] = useState(false);
  const [pop, setPop] = useState<V13Group['id'] | null>(null);
  const [query, setQuery] = useState('');
  const [showNotifModal, setShowNotifModal] = useState(false);
  const unread = useUnread();
  const [appFs, toggleAppFs] = useAppFullscreen();
  const [canInstall, setCanInstall] = useState(pwaService.getState().canInstall);
  useEffect(() => pwaService.subscribe((s) => setCanInstall(s.canInstall)), []);
  const [queued, setQueued] = useState(() => offlineDatabaseService.getState().queuedActionsCount);
  useEffect(() => offlineDatabaseService.subscribe((st) => setQueued(st.queuedActionsCount)), []);
  const islandRef = useRef<HTMLDivElement>(null);
  const activeGroup = groupOf(active);

  useEffect(() => {
    setMenu(false);
    setPop(null);
  }, [active]);
  useEffect(() => {
    if (!menu) setQuery('');
  }, [menu]);
  // Tanıtım turu "Daha" sayfasını açıp kapatır (WelcomeTour → medsoru:more)
  useEffect(() => {
    const on = (e: Event) => setMenu(Boolean((e as CustomEvent<{ open?: boolean }>).detail?.open));
    window.addEventListener('medsoru:more', on);
    return () => window.removeEventListener('medsoru:more', on);
  }, []);
  useEffect(() => {
    if (!pop) return;
    const down = (e: PointerEvent) => {
      if (!islandRef.current?.contains(e.target as Node)) setPop(null);
    };
    const key = (e: KeyboardEvent) => e.key === 'Escape' && setPop(null);
    document.addEventListener('pointerdown', down);
    document.addEventListener('keydown', key);
    return () => {
      document.removeEventListener('pointerdown', down);
      document.removeEventListener('keydown', key);
    };
  }, [pop]);

  const go = (r: AppRoute) => {
    setMenu(false);
    setPop(null);
    onGo(r);
  };

  const groupTab = (id: V13Group['id']) => {
    const g = V13_GROUPS.find((x) => x.id === id)!;
    const here = activeGroup?.id === id;
    const cur = here ? g.items.find((it) => it.id === active) : undefined;
    const Icon = cur?.icon || g.icon;
    const label = cur ? cur.short || cur.label : g.short;
    if (g.items.length === 1) {
      const it = g.items[0];
      return (
        <a
          key={id}
          href={pathFor(it.id)}
          onClick={linkClick(() => {
            if (!here) buzz();
            go(it.id);
          })}
          aria-current={here ? 'page' : undefined}
          className="a13-tab"
        >
          <Icon strokeWidth={here ? 2.1 : 1.8} aria-hidden="true" />
          <span className="a13-tab-l">{label}</span>
        </a>
      );
    }
    return (
      <button
        key={id}
        type="button"
        className={`a13-tab ${here ? 'is-here' : ''}`}
        aria-current={here ? 'page' : undefined}
        aria-expanded={pop === id}
        aria-haspopup="menu"
        aria-label={`${g.label}${cur ? `, şu an: ${cur.label}` : ''}. ${here ? 'Sayfa listesi için dokun' : 'Son açtığın sayfaya git; listeyi görmek için basılı tut'}`}
        onClick={() => {
          buzz();
          if (here || pop === id) setPop((p) => (p === id ? null : id));
          else go(lastIn(g));
        }}
        onContextMenu={(e) => {
          e.preventDefault();
          setPop(id);
        }}
      >
        <Icon strokeWidth={here ? 2.1 : 1.8} aria-hidden="true" />
        <span className="a13-tab-l">
          {label}
          <ChevronUp className="a13-tab-chev" aria-hidden="true" />
        </span>
      </button>
    );
  };

  const popGroup = pop ? V13_GROUPS.find((g) => g.id === pop) : undefined;
  const pool: NavItem[] = [NAV_ITEMS.quick_add, ...V13_GROUPS.flatMap((g) => g.items), NAV_ITEMS.settings];
  const hits = matchPages(query, pool);
  const choice = designChoiceOf(look);

  const toolRow = (key: string, Icon: React.ElementType, label: string, end: React.ReactNode, onClick: () => void) => (
    <button key={key} type="button" className="a13-trow" onClick={onClick}>
      <Icon className="a13-ico" aria-hidden="true" />
      <span className="a13-trow-t">{label}</span>
      {end}
    </button>
  );

  return (
    <>
      <div className="a13-island-wrap ms-hide-on-kb print:hidden" ref={islandRef}>
        {popGroup && (
          <div className="a13-pop" role="menu" aria-label={popGroup.label}>
            <p className="a13-pop-h">{popGroup.label}</p>
            <PageList group={popGroup} active={active} onPick={go} counts={counts} />
          </div>
        )}
        <nav aria-label="Alt gezinme" className="a13-island">
          {groupTab(ISLAND[0])}
          {groupTab(ISLAND[1])}
          <a
            href={pathFor('quick_add')}
            onClick={linkClick(() => {
              buzz();
              go('quick_add');
            })}
            aria-current={active === 'quick_add' ? 'page' : undefined}
            className="a13-tab a13-tab-add"
            aria-label="Soru ekle"
          >
            <span className="a13-plus"><Plus strokeWidth={2.4} aria-hidden="true" /></span>
          </a>
          {groupTab(ISLAND[2])}
          <button
            type="button"
            className="a13-tab"
            onClick={() => {
              buzz();
              setPop(null);
              setMenu(true);
            }}
            aria-haspopup="dialog"
            aria-expanded={menu}
            aria-current={activeGroup && !ISLAND.includes(activeGroup.id) ? 'page' : active === 'settings' ? 'page' : undefined}
            aria-label={`Menü: tüm sayfalar ve araçlar${unread || queued ? ', yeni bildirim ya da bekleyen işlem var' : ''}`}
          >
            <span className="a13-tab-ic">
              <LayoutGrid strokeWidth={1.8} aria-hidden="true" />
              {(unread > 0 || queued > 0) && <i className="a13-tab-dot" aria-hidden="true" />}
            </span>
            <span className="a13-tab-l" aria-hidden="true">Menü</span>
          </button>
        </nav>
      </div>

      <Sheet open={menu} onClose={() => setMenu(false)} title="Menü" size="full">
        <div className="a13-menu">
          <div className="a13-msearch">
            <Search aria-hidden="true" />
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && hits[0]) {
                  e.preventDefault();
                  go(hits[0].id);
                }
              }}
              placeholder="Sayfa bul (kart, sözlük, test…)"
              aria-label="Sayfa bul"
              enterKeyHint="go"
              autoComplete="off"
            />
          </div>

          {query.trim() ? (
            <ul className="a13-plist" role="list" aria-label="Bulunan sayfalar">
              {hits.map((it) => {
                const Icon = it.icon;
                return (
                  <li key={it.id}>
                    <a href={pathFor(it.id)} onClick={linkClick(() => go(it.id))} aria-current={it.id === active ? 'page' : undefined} className="a13-plink">
                      <Icon className="a13-ico" aria-hidden="true" />
                      <span className="a13-plink-t">{it.label}</span>
                    </a>
                  </li>
                );
              })}
              <li>
                <button
                  type="button"
                  className="a13-plink"
                  onClick={() => {
                    setMenu(false);
                    openSearch();
                  }}
                >
                  <Search className="a13-ico" aria-hidden="true" />
                  <span className="a13-plink-t">“{query.trim()}” için sorularda, notlarda ve sözlükte ara</span>
                </button>
              </li>
            </ul>
          ) : (
            <>
              {V13_GROUPS.filter((g) => g.id !== 'bugun').map((g) => (
                <section key={g.id} className="a13-msec" aria-label={g.label}>
                  <h2 className="a13-msec-h">{g.label}</h2>
                  <div className="a13-chips">
                    {g.items.map((it) => {
                      const Icon = it.icon;
                      return (
                        <a
                          key={it.id}
                          href={pathFor(it.id)}
                          onClick={linkClick(() => go(it.id))}
                          aria-current={it.id === active ? 'page' : undefined}
                          className="a13-chip"
                        >
                          <Icon aria-hidden="true" />
                          <span>{it.tile || it.label}</span>
                        </a>
                      );
                    })}
                  </div>
                </section>
              ))}

              <section className="a13-msec" aria-label="Görünüm">
                <h2 className="a13-msec-h">Görünüm</h2>
                <div className="a13-seg" role="radiogroup" aria-label="Tema">
                  {(['light', 'sepia', 'dark'] as ThemeMode[]).map((m) => {
                    const Icon = MODE_ICONS[m];
                    return (
                      <button key={m} type="button" role="radio" aria-checked={look.mode === m} onClick={() => look.set({ mode: m })}>
                        <Icon aria-hidden="true" />
                        {MODE_LABELS[m]}
                      </button>
                    );
                  })}
                </div>
                <div className="a13-seg" role="radiogroup" aria-label="Tasarım">
                  {DESIGN_CHOICES.map((c) => (
                    <button key={c} type="button" role="radio" aria-checked={choice === c} onClick={() => look.set({ choice: c })} title={DESIGN_CHOICE_LABELS[c]}>
                      {c}
                    </button>
                  ))}
                </div>
              </section>

              <section className="a13-msec" aria-label="Araçlar">
                <h2 className="a13-msec-h">Araçlar</h2>
                <div className="a13-tools-list">
                  {canInstall && toolRow('install', Smartphone, 'Uygulamayı cihaza yükle', null, () => {
                    setMenu(false);
                    void pwaService.promptInstall();
                  })}
                  {toolRow('fs', appFs ? Minimize2 : Maximize2, appFs ? 'Tam ekrandan çık' : 'Tam ekran', null, () => {
                    setMenu(false);
                    toggleAppFs();
                  })}
                  {toolRow('notif', Bell, 'Bildirimler', unread > 0 ? <span className="a13-count">{unread}</span> : null, () => {
                    setMenu(false);
                    setShowNotifModal(true);
                  })}
                  {toolRow('queue', CloudUpload, queued ? 'Gönderim kuyruğu' : 'Gönderim kuyruğu (boş)', queued > 0 ? <span className="a13-count is-warn">{queued}</span> : null, () => {
                    setMenu(false);
                    window.dispatchEvent(new Event('medsoru:pending'));
                  })}
                  {onOffline && toolRow('offline', Database, 'Çevrimdışı veritabanı', null, () => {
                    setMenu(false);
                    onOffline();
                  })}
                  {toolRow('pdf', FileDown, 'PDF indir', null, () => {
                    setMenu(false);
                    onPdf();
                  })}
                  <a href={pathFor('settings')} onClick={linkClick(() => go('settings'))} className="a13-trow" aria-current={active === 'settings' ? 'page' : undefined}>
                    <NAV_ITEMS.settings.icon className="a13-ico" aria-hidden="true" />
                    <span className="a13-trow-t">Profil ve ayarlar</span>
                  </a>
                  {isAdmin && (
                    <a href={pathFor('manage')} onClick={linkClick(() => go('manage'))} className="a13-trow" aria-current={active === 'manage' ? 'page' : undefined}>
                      <ShieldCheck className="a13-ico" aria-hidden="true" />
                      <span className="a13-trow-t">Yönetim konsolu</span>
                    </a>
                  )}
                </div>
              </section>
            </>
          )}
        </div>
      </Sheet>

      <NotificationHistoryModal isOpen={showNotifModal} onClose={() => setShowNotifModal(false)} />
    </>
  );
};
