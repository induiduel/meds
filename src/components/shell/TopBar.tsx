import React, { useEffect, useState } from 'react';
import { Activity, Moon, Search, Sun, UserRound, Bell, Smartphone, Maximize2, Minimize2 } from 'lucide-react';
import { linkClick, pathFor, ROUTE_TITLES, type AppRoute } from '../../router';
import type { AppUser } from '../../services/auth';
import { pwaService } from '../../services/pwaService';
import { useTheme } from '../../utils/theme';
import { useAppFullscreen } from '../../utils/fullscreen';
import { OfflineStatusBadge } from '../pwa/OfflineStatusBadge';
import { GuncellemeSimgesi } from '../system/UpdatePrompt';
import { SearchPalette } from '../search/SearchPalette';
import type { SearchHit } from '../search/searchShared';
import { AccountMenu, type AccountActions } from './AccountMenu';
import { initialsOf } from './navModel';
import { userNotificationService } from '../../services/userNotificationService';
import { NotificationHistoryModal } from '../notifications/NotificationHistoryModal';
import { BrandWord } from './BrandWord';
import { usePhone, useSearchShortcut } from './shellHooks';
import { useAppearance } from '../../utils/appearance';
import { TopBarV12 } from '../v12/ShellV12';

/**
 * v8 üst çubuk. Sol: telefonda logo; sayfa aşağı kayınca logo yerine sayfa adı belirir (büyük başlık → çubuk başlığı).
 * Sağ: masaüstünde alan görünümlü arama, çevrimdışı rozeti, hızlı açık/koyu, hesap (telefonda alt sayfa).
 * Arama: "/" ya da Ctrl/⌘+K; kenar menüsü `medsoru:search` olayıyla açar.
 */
export type TopBarProps = {
  active: AppRoute;
  onGo: (r: AppRoute) => void;
  user: AppUser | null;
  isAdmin: boolean;
  searchQuery?: string;
  /** hit verilirse (palette sonucuna tıklandı) doğrudan kaynağı açmak denenir */
  onSearch?: (q: string, focusId?: string, hit?: SearchHit) => void;
  onOpenOffline?: () => void;
  actions: Omit<AccountActions, 'onInstall'>;
};

/** v12 "Net" tasarımında kendi üst çubuğu (components/v12/ShellV12); v10/v11 aşağıdaki klasik çubuk. */
export const TopBar: React.FC<TopBarProps> = (props) =>
  useAppearance().design === 'v12' ? <TopBarV12 {...props} /> : <TopBarClassic {...props} />;

const TopBarClassic: React.FC<TopBarProps> = ({ active, onGo, user, isAdmin, searchQuery = '', onSearch, onOpenOffline, actions }) => {
  const phone = usePhone();
  const { theme, toggle } = useTheme();
  const [appFs, toggleAppFs] = useAppFullscreen();
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

  useSearchShortcut(() => setSearch(true));

  const title = ROUTE_TITLES[active];

  return (
    <header className={`sh-top print:hidden ${scrolled ? 'is-scrolled' : ''} ${scrolled === 2 ? 'show-title' : ''}`}>
      <div className="sh-top-in">
        <div className="sh-top-lead">
          <a href={pathFor('quick_add')} onClick={linkClick(() => onGo('quick_add'))} className="sh-brand sh-top-brand" aria-label="MeDSor ana sayfa">
            <span className="sh-brand-mark"><Activity strokeWidth={2.4} /></span>
            <BrandWord />
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
          <GuncellemeSimgesi className="sh-ibtn" />
          {canInstall && (
            <button
              type="button"
              className="sh-ibtn"
              onClick={() => pwaService.promptInstall()}
              aria-label="Uygulamayı cihaza yükle (Ana Ekrana Ekle)"
              title="Uygulamayı cihaza yükle (Tam Ekran PWA)"
            >
              <Smartphone className="w-5 h-5" />
            </button>
          )}
          <button
            type="button"
            className="sh-ibtn"
            onClick={() => toggleAppFs()}
            aria-label={appFs ? 'Tam ekrandan çık' : 'Tam ekran görünümü'}
            title={appFs ? 'Tam ekrandan çık' : 'Tam ekran görünümü'}
          >
            {appFs ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
          </button>
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
