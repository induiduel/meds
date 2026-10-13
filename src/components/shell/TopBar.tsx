import React, { useEffect, useState, useSyncExternalStore } from 'react';
import { Activity, Moon, Search, Sun, UserRound, Bell } from 'lucide-react';
import { linkClick, pathFor, ROUTE_TITLES, type AppRoute } from '../../router';
import type { AppUser } from '../../services/auth';
import { pwaService } from '../../services/pwaService';
import { useTheme } from '../../utils/theme';
import { OfflineStatusBadge } from '../pwa/OfflineStatusBadge';
import { SearchPalette } from '../search/SearchPalette';
import type { SearchHit } from '../search/searchShared';
import { AccountMenu, type AccountActions } from './AccountMenu';
import { initialsOf } from './navModel';
import { userNotificationService } from '../../services/userNotificationService';
import { NotificationHistoryModal } from '../notifications/NotificationHistoryModal';

const usePhone = () =>
  useSyncExternalStore(
    (cb) => {
      const m = window.matchMedia('(max-width: 639px)');
      m.addEventListener('change', cb);
      return () => m.removeEventListener('change', cb);
    },
    () => window.matchMedia('(max-width: 639px)').matches,
    () => false
  );

/**
 * v8 üst çubuk. Sol: telefonda logo; sayfa aşağı kayınca logo yerine sayfa adı belirir (büyük başlık → çubuk başlığı).
 * Sağ: masaüstünde alan görünümlü arama, çevrimdışı rozeti, hızlı açık/koyu, hesap (telefonda alt sayfa).
 * Arama: "/" ya da Ctrl/⌘+K; kenar menüsü `medsoru:search` olayıyla açar.
 */
export const TopBar: React.FC<{
  active: AppRoute;
  onGo: (r: AppRoute) => void;
  user: AppUser | null;
  isAdmin: boolean;
  searchQuery?: string;
  /** hit verilirse (palette sonucuna tıklandı) doğrudan kaynağı açmak denenir */
  onSearch?: (q: string, focusId?: string, hit?: SearchHit) => void;
  onOpenOffline?: () => void;
  actions: Omit<AccountActions, 'onInstall'>;
}> = ({ active, onGo, user, isAdmin, searchQuery = '', onSearch, onOpenOffline, actions }) => {
  const phone = usePhone();
  const { theme, toggle } = useTheme();
  const [menu, setMenu] = useState(false);
  const [search, setSearch] = useState(false);
  const [scrolled, setScrolled] = useState(0);
  const [canInstall, setCanInstall] = useState(pwaService.getState().canInstall);
  const [unreadNotifs, setUnreadNotifs] = useState(0);
  const [showNotifModal, setShowNotifModal] = useState(false);

  useEffect(() => pwaService.subscribe((s) => setCanInstall(s.canInstall)), []);
  useEffect(() => {
    return userNotificationService.subscribe((list) => {
      setUnreadNotifs(list.filter((n) => !n.read).length);
    });
  }, []);

  useEffect(() => {
    let raf = 0;
    const on = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => setScrolled(window.scrollY > 64 ? 2 : window.scrollY > 4 ? 1 : 0));
    };
    on();
    window.addEventListener('scroll', on, { passive: true });
    return () => {
      window.removeEventListener('scroll', on);
      cancelAnimationFrame(raf);
    };
  }, []);
  useEffect(() => setMenu(false), [active]);

  useEffect(() => {
    const open = () => setSearch(true);
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      const isK = (e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k';
      if (!isK && (e.key !== '/' || ['INPUT', 'TEXTAREA', 'SELECT'].includes(t.tagName) || t.isContentEditable)) return;
      e.preventDefault();
      setSearch(true);
    };
    window.addEventListener('medsoru:search', open);
    document.addEventListener('keydown', onKey);
    return () => {
      window.removeEventListener('medsoru:search', open);
      document.removeEventListener('keydown', onKey);
    };
  }, []);

  const title = ROUTE_TITLES[active];

  return (
    <header className={`sh-top print:hidden ${scrolled ? 'is-scrolled' : ''} ${scrolled === 2 ? 'show-title' : ''}`}>
      <div className="sh-top-in">
        <div className="sh-top-lead">
          <a href={pathFor('quick_add')} onClick={linkClick(() => onGo('quick_add'))} className="sh-brand sh-top-brand" aria-label="MeDSor ana sayfa">
            <span className="sh-brand-mark"><Activity strokeWidth={2.4} /></span>
            <span className="sh-brand-word">Me<b>DS</b>or</span>
          </a>
          <span className="sh-top-title" aria-hidden={scrolled !== 2}>{title}</span>
        </div>

        <button type="button" className="sh-top-search" onClick={() => setSearch(true)} title="Ara ( / ya da Ctrl+K )">
          <Search />
          <span>Soru, ders, terim ara</span>
          <kbd>⌘K</kbd>
        </button>

        <div className="sh-top-tools">
          <OfflineStatusBadge onClick={() => onOpenOffline?.()} isAdmin={isAdmin} />
          <button type="button" className="sh-ibtn sh-top-search-i" onClick={() => setSearch(true)} aria-label="Ara">
            <Search />
          </button>
          <button
            type="button"
            className="sh-ibtn sh-top-theme"
            onClick={toggle}
            aria-label={theme === 'dark' ? 'Aydınlık temaya geç' : 'Koyu temaya geç'}
            title={theme === 'dark' ? 'Aydınlık tema' : 'Koyu tema'}
          >
            <span className="sh-theme-ic" data-dark={theme === 'dark'}>
              <Sun />
              <Moon />
            </span>
          </button>
          <button
            type="button"
            className="sh-ibtn relative sh-top-bell"
            onClick={() => setShowNotifModal(true)}
            aria-label={unreadNotifs ? `Bildirimler, ${unreadNotifs} okunmamış` : 'Bildirimler'}
            title="Bildirimler"
          >
            <Bell className="w-5 h-5" />
            {unreadNotifs > 0 && <span className="sh-badge" aria-hidden>{unreadNotifs > 9 ? '9+' : unreadNotifs}</span>}
          </button>
          <div className="sh-acct-anchor">
            <button
              type="button"
              className={`sh-acct-btn ${menu ? 'is-open' : ''} ${unreadNotifs ? 'has-unread' : ''}`}
              onClick={() => setMenu((v) => !v)}
              aria-haspopup="dialog"
              aria-expanded={menu}
              aria-label="Hesap ve araçlar"
            >
              <span className="ui-avatar" style={{ '--av': '30px' } as React.CSSProperties}>
                {user?.photoURL ? <img src={user.photoURL} alt="" /> : user ? initialsOf(user) : <UserRound className="w-4 h-4" />}
              </span>
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
        />
      )}

      <NotificationHistoryModal isOpen={showNotifModal} onClose={() => setShowNotifModal(false)} />
    </header>
  );
};
