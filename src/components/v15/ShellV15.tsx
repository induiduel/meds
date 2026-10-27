import React, { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  Bell,
  ChevronLeft,
  ChevronRight,
  CloudUpload,
  Database,
  FileDown,
  Maximize2,
  Minimize2,
  PanelLeftClose,
  PanelLeftOpen,
  Search,
  Settings2,
  ShieldCheck,
  Smartphone,
  Stethoscope,
  Trophy,
  UserRound,
} from 'lucide-react';
import { linkClick, navigateTo, pathFor, ROUTE_TITLES, type AppRoute } from '../../router';
import { icKonum } from '../../siteHaritasi';
import type { AppUser } from '../../services/auth';
import { pwaService } from '../../services/pwaService';
import { offlineDatabaseService } from '../../services/offlineDatabaseService';
import { userNotificationService } from '../../services/userNotificationService';
import { aktifKurul, sinavaKalanGun } from '../../services/kurulTakvimi';
import { prefetchRoute } from '../../routePrefetch';
import { useReviewCounts } from '../../hooks/useReviewCounts';
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
import { NAV_ITEMS, initialsOf, openSearch } from '../shell/navModel';
import { usePhone, useSearchShortcut, useSideCollapse } from '../shell/shellHooks';
import { TOP_SLOT_ID } from '../v12/ShellV12';
import { V15_SECTIONS, sectionOf, type V15Section } from './navV15';
import { useV15BaslikOku } from './baslik';
import '../../styles/v15/tokens.css';
import '../../styles/v15/shell.css';

/**
 * v15 kabuğu (tasarım sistemi v15 › Kabuk). Kesme noktaları: <600 alt sekme çubuğu, 600–1023 76 px ikonlu ray,
 * ≥1024 236 px yan menü (kurul kartı, arama, bölümler, etkin bölümün alt sayfaları, profil, kullanıcı kartı).
 * Üst bar sade: başlık + alt satır; tablette üstünde konum satırı ve kurul çipi, PC'de ⌘K arama alanı.
 * Etkin öge yalnız vurgu rengiyle belirtilir; dokunma hedefi ≥44 px. Renkler yalnız palet token'ı (utils/palettes.ts).
 * Sayfalar kendi araçlarını #s12-top-slot yuvasına koyar (TopBarSlotV12).
 */

/** v15 yazı tipleri (Plus Jakarta Sans, Newsreader) yalnız v15 seçiliyken bir kez yüklenir */
const FONT_HREF =
  'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Newsreader:opsz,wght@6..72,400;6..72,600&display=swap';
const useV15Fonts = () => {
  useEffect(() => {
    if (document.getElementById('v15-fonts')) return;
    const l = document.createElement('link');
    l.id = 'v15-fonts';
    l.rel = 'stylesheet';
    l.href = FONT_HREF;
    document.head.appendChild(l);
  }, []);
};

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

/** Bölüm rozetleri: Ders çalış'ta vadesi gelen tekrar (Öğren hata defteri) */
const useBadges = (): Partial<Record<V15Section['id'], number>> => {
  const review = useReviewCounts();
  return { dersler: review.total.due > 0 ? review.total.due : undefined };
};

/** Takvimdeki aktif kurul ve sınava kalan gün (gün değişince yenilenir) */
const useKurul = () => {
  const [k, setK] = useState(() => ({ kurul: aktifKurul(), kalan: sinavaKalanGun() }));
  useEffect(() => {
    const t = window.setInterval(() => setK({ kurul: aktifKurul(), kalan: sinavaKalanGun() }), 30 * 60_000);
    return () => window.clearInterval(t);
  }, []);
  return k;
};
const kalanYazi = (n: number) => (n > 0 ? `sınava ${n} gün` : n === 0 ? 'sınav bugün' : 'sınav bitti');

const Avatar: React.FC<{ user: AppUser | null; size?: number }> = ({ user, size = 32 }) => (
  <span className="v15-av" style={{ '--v15-av': `${size}px` } as React.CSSProperties} aria-hidden="true">
    {user?.photoURL ? <img src={user.photoURL} alt="" /> : user ? initialsOf(user) : <UserRound />}
  </span>
);

const Badge: React.FC<{ n?: number; label: string }> = ({ n, label }) =>
  n ? (
    <span className="v15-badge">
      <span aria-hidden="true">{n > 99 ? '99+' : n}</span>
      <span className="sr-only">, {n} {label}</span>
    </span>
  ) : null;

const Mark: React.FC = () => (
  <span className="v15-mark" aria-hidden="true">
    <Stethoscope strokeWidth={2.2} />
  </span>
);

/* =============================================================================
 * Yan menü (≥1024) ve ray (600–1023)
 * ============================================================================= */
export const SideNavV15: React.FC<SideNavProps> = ({ active, onGo, isAdmin, user }) => {
  const { collapsed, setCollapsed } = useSideCollapse();
  const wide = useMedia('(min-width: 1024px)');
  const full = wide && !collapsed;
  const here = sectionOf(active);
  const badges = useBadges();
  const { kurul, kalan } = useKurul();

  const link = (id: AppRoute, children: React.ReactNode, cls: string, title?: string) => (
    <a
      key={id}
      href={pathFor(id)}
      onClick={linkClick(() => onGo(id))}
      onPointerEnter={() => prefetchRoute(id)}
      onFocus={() => prefetchRoute(id)}
      aria-current={active === id ? 'page' : undefined}
      className={cls}
      title={title}
    >
      {children}
    </a>
  );

  if (!full) {
    return (
      <nav aria-label="Ana menü" className="v15-side is-rail print:hidden">
        {link('today', <Mark />, 'v15-rail-mark', 'MeDSor · Bugün')}
        <div className="v15-rail-list">
          {V15_SECTIONS.map((s) => {
            const Icon = s.icon;
            const on = here?.id === s.id;
            return (
              <a
                key={s.id}
                href={pathFor(s.hub)}
                onClick={linkClick(() => onGo(s.hub))}
                onPointerEnter={() => prefetchRoute(s.hub)}
                aria-current={on ? 'page' : undefined}
                className="v15-rail-btn"
                title={s.label}
              >
                <span className="v15-rail-ic">
                  <Icon strokeWidth={on ? 2.1 : 1.8} aria-hidden="true" />
                  {badges[s.id] ? <i className="v15-dot" aria-hidden="true" /> : null}
                </span>
                <span className="v15-rail-l">{s.short}</span>
              </a>
            );
          })}
        </div>
        <span className="v15-grow" />
        {isAdmin && link('manage', <><ShieldCheck aria-hidden="true" /><span className="v15-rail-l">Yönetim</span></>, 'v15-rail-btn', 'Yönetim konsolu')}
        {wide && (
          <button type="button" className="v15-rail-btn" onClick={() => setCollapsed(() => false)} aria-label="Menüyü genişlet" title="Menüyü genişlet">
            <PanelLeftOpen aria-hidden="true" />
          </button>
        )}
        {link('settings', <Avatar user={user} size={32} />, 'v15-rail-me', 'Profil ve ayarlar')}
      </nav>
    );
  }

  return (
    <nav aria-label="Ana menü" className="v15-side is-full print:hidden">
      <div className="v15-side-head">
        {link('today', <><Mark /><span className="v15-word">MeDSor</span></>, 'v15-brand', 'Bugün')}
        <button type="button" className="v15-ib" onClick={() => setCollapsed(() => true)} aria-label="Menüyü daralt" title="Menüyü daralt">
          <PanelLeftClose aria-hidden="true" />
        </button>
      </div>

      {link(
        'sinav_plani',
        <>
          <span className="v15-kurul-t">
            <b>Kurul {kurul.kurul}</b>
            <span>{kalanYazi(kalan)}</span>
          </span>
          <ChevronRight className="v15-chev" aria-hidden="true" />
        </>,
        'v15-kurul',
        `${kurul.ad} · sınav planı`,
      )}

      <button type="button" className="v15-find" onClick={openSearch} aria-label="Ara (Ctrl+K)">
        <Search aria-hidden="true" />
        <span>Ara</span>
        <kbd>⌘K</kbd>
      </button>

      <div className="v15-side-scroll">
        <ul className="v15-nav" role="list">
          {V15_SECTIONS.map((s) => {
            const Icon = s.icon;
            const on = here?.id === s.id;
            return (
              <li key={s.id}>
                <a
                  href={pathFor(s.hub)}
                  onClick={linkClick(() => onGo(s.hub))}
                  onPointerEnter={() => prefetchRoute(s.hub)}
                  aria-current={active === s.hub ? 'page' : on ? 'true' : undefined}
                  className="v15-nav-a"
                >
                  <Icon strokeWidth={on ? 2.1 : 1.8} aria-hidden="true" />
                  <span className="v15-nav-t">{s.label}</span>
                  <Badge n={badges[s.id]} label="bekleyen iş" />
                </a>
                {on && s.items.length > 0 && (
                  <ul className="v15-sub" role="list" aria-label={`${s.label} sayfaları`}>
                    {s.items.map((it) => (
                      <li key={it.id}>{link(it.id, <span className="v15-nav-t">{it.label}</span>, 'v15-sub-a', it.hint)}</li>
                    ))}
                  </ul>
                )}
              </li>
            );
          })}
        </ul>
      </div>

      <div className="v15-side-foot">
        {isAdmin && link('manage', <><ShieldCheck aria-hidden="true" /><span className="v15-nav-t">Yönetim</span></>, 'v15-nav-a')}
        {link('basarimlar', <><Trophy aria-hidden="true" /><span className="v15-nav-t">Başarımlar</span></>, 'v15-nav-a')}
        <div className="v15-me">
          <Avatar user={user} size={34} />
          <span className="v15-me-t">
            <b>{user?.displayName || user?.email?.split('@')[0] || 'Misafir'}</b>
            <span>Kurul {kurul.kurul}</span>
          </span>
          {link('settings', <Settings2 aria-hidden="true" />, 'v15-ib', 'Ayarlar')}
        </div>
      </div>
    </nav>
  );
};

/* =============================================================================
 * Üst bar
 * ============================================================================= */
export const TopBarV15: React.FC<TopBarProps> = ({ active, onGo, user, isAdmin, searchQuery = '', onSearch, onOpenOffline, actions }) => {
  const phone = usePhone();
  const [appFs, toggleAppFs, exitAppFs] = useAppFullscreen();
  const [menu, setMenu] = useState(false);
  const [search, setSearch] = useState(false);
  const [canInstall, setCanInstall] = useState(pwaService.getState().canInstall);
  const [showNotifModal, setShowNotifModal] = useState(false);
  const unread = useUnread();
  const { kurul, kalan } = useKurul();
  useV15Fonts();

  useEffect(() => pwaService.subscribe((s) => setCanInstall(s.canInstall)), []);
  useEffect(() => setMenu(false), [active]);
  useSearchShortcut(() => setSearch(true));

  const sec = sectionOf(active);
  const sayfa = useV15BaslikOku();
  // Odak ekranı: sesli ders açıkken kendi üst barını kullanır (tasarım sistemi v15 › Kabuk)
  const odak = active === 'canli_ders' && icKonum().pathname.startsWith('/canliders/');
  const title = sayfa?.baslik || (active === 'today' ? greeting(user) : ROUTE_TITLES[active]);
  const sub =
    sayfa?.alt ??
    (active === 'today'
      ? `${new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', weekday: 'long' })} · Kurul ${kurul.kurul} ${kalanYazi(kalan)}`
      : undefined);
  const crumb = sec && sec.id !== 'bugun' && active !== sec.hub ? sec : undefined;

  if (odak) {
    return search ? (
      <SearchPalette initialQuery={searchQuery} onClose={() => setSearch(false)} onOpenResults={(q, focusId, hit) => onSearch?.(q, focusId, hit)} onGo={onGo} />
    ) : null;
  }

  return (
    <header className="v15-top print:hidden">
      {sayfa?.geri && (
        <a className="v15-ib v15-back" href={sayfa.geri} onClick={linkClick(() => navigateTo(sayfa.geri!))} aria-label="Geri" title="Geri">
          <ChevronLeft aria-hidden="true" />
        </a>
      )}
      <button type="button" className={`v15-top-av${sayfa?.geri ? ' is-hidden' : ''}`} onClick={() => setMenu((v) => !v)} aria-haspopup="dialog" aria-expanded={menu} aria-label="Hesap ve araçlar">
        <Avatar user={user} size={32} />
        {unread > 0 && <i className="v15-dot" aria-hidden="true" />}
      </button>
      <div className="v15-top-t">
        {crumb && (
          <a className="v15-crumb" href={pathFor(crumb.hub)} onClick={linkClick(() => onGo(crumb.hub))}>
            {crumb.label}
            <ChevronRight aria-hidden="true" />
          </a>
        )}
        <p className="v15-top-h">{title}</p>
        {sub && <p className="v15-top-sub">{sub}</p>}
      </div>
      <div id={TOP_SLOT_ID} className="v15-top-slot" />
      <div className="v15-top-tools">
        <OfflineStatusBadge onClick={() => onOpenOffline?.()} isAdmin={isAdmin} className="v15-ofb" />
        <GuncellemeSimgesi className="v15-ib" />
        <button type="button" className="v15-search" onClick={() => setSearch(true)} aria-label="Ara ( / ya da Ctrl+K )">
          <Search aria-hidden="true" />
          <span className="v15-search-l">Ders, soru, terim ara</span>
          <kbd className="v15-search-k">⌘K</kbd>
        </button>
        <a className="v15-chip v15-only-tab" href={pathFor('sinav_plani')} onClick={linkClick(() => onGo('sinav_plani'))} title={`${kurul.ad} · ${kalanYazi(kalan)}`}>
          Kurul {kurul.kurul}
          <ChevronRight aria-hidden="true" />
        </a>
        {canInstall && (
          <button type="button" className="v15-ib v15-not-phone" onClick={() => pwaService.promptInstall()} aria-label="Uygulamayı cihaza yükle" title="Uygulamayı cihaza yükle">
            <Smartphone aria-hidden="true" />
          </button>
        )}
        <button
          type="button"
          className="v15-ib v15-not-phone"
          onClick={() => toggleAppFs()}
          aria-label={appFs ? 'Tam ekrandan çık' : 'Tam ekran'}
          title={appFs ? 'Tam ekrandan çık' : 'Tam ekran: menüleri gizle'}
        >
          {appFs ? <Minimize2 aria-hidden="true" /> : <Maximize2 aria-hidden="true" />}
        </button>
        <button type="button" className="v15-ib" onClick={() => setShowNotifModal(true)} aria-label={unread ? `Bildirimler, ${unread} okunmamış` : 'Bildirimler'} title="Bildirimler">
          <Bell aria-hidden="true" />
          {unread > 0 && <i className="v15-dot" aria-hidden="true" />}
        </button>
        <div className="v15-acct">
          <button type="button" className="v15-acct-btn v15-not-phone" onClick={() => setMenu((v) => !v)} aria-haspopup="dialog" aria-expanded={menu} aria-label="Hesap ve araçlar">
            <Avatar user={user} size={32} />
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
          <button type="button" className="s12-fs-exit v15-fs-exit print:hidden" onClick={exitAppFs} aria-label="Tam ekrandan çık" title="Tam ekrandan çık (Esc)">
            <Minimize2 aria-hidden="true" />
            <span>Tam ekrandan çık</span>
          </button>,
          document.body,
        )}
    </header>
  );
};

const greeting = (user: AppUser | null) => {
  const h = new Date().getHours();
  const w = h < 5 ? 'İyi geceler' : h < 12 ? 'Günaydın' : h < 18 ? 'İyi günler' : 'İyi akşamlar';
  const ad = (user?.displayName || '').trim().split(/\s+/)[0];
  return ad ? `${w}, ${ad}` : w;
};

/* =============================================================================
 * Alt sekme çubuğu (<600)
 * ============================================================================= */
export const TabBarV15: React.FC<TabBarProps> = ({ active, onGo, isAdmin, onPdf, onOffline }) => {
  const here = sectionOf(active);
  const badges = useBadges();
  const [sheet, setSheet] = useState<V15Section | null>(null);
  const [appFs, toggleAppFs] = useAppFullscreen();
  const [queued, setQueued] = useState(() => offlineDatabaseService.getState().queuedActionsCount);
  useEffect(() => offlineDatabaseService.subscribe((st) => setQueued(st.queuedActionsCount)), []);
  useEffect(() => setSheet(null), [active]);
  // Tanıtım turu "Daha" sayfasını açıp kapatır (WelcomeTour → medsoru:more): v15'te bölüm listesi
  useEffect(() => {
    const on = (e: Event) => setSheet((e as CustomEvent<{ open?: boolean }>).detail?.open ? V15_SECTIONS[1] : null);
    window.addEventListener('medsoru:more', on);
    return () => window.removeEventListener('medsoru:more', on);
  }, []);

  const go = (r: AppRoute) => {
    setSheet(null);
    onGo(r);
  };
  // Odak ekranı (sesli ders): alt sekme yerine oynatıcı durur
  if (active === 'canli_ders' && icKonum().pathname.startsWith('/canliders/')) return null;

  return (
    <>
      <nav aria-label="Alt gezinme" className="v15-tabs ms-hide-on-kb print:hidden">
        {V15_SECTIONS.map((s) => {
          const Icon = s.icon;
          const on = here?.id === s.id;
          return (
            <a
              key={s.id}
              href={pathFor(s.hub)}
              onClick={(e) => {
                if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
                e.preventDefault();
                buzz();
                // Bölümün içindeyken yeniden dokunmak sayfa listesini açar
                if (on && s.items.length && active !== s.hub) setSheet(s);
                else go(s.hub);
              }}
              onContextMenu={(e) => {
                if (!s.items.length) return;
                e.preventDefault();
                setSheet(s);
              }}
              aria-current={on ? 'page' : undefined}
              className="v15-tab"
            >
              <span className="v15-tab-pill">
                <Icon strokeWidth={on ? 2.1 : 1.8} aria-hidden="true" />
                {badges[s.id] ? <i className="v15-dot" aria-hidden="true" /> : null}
              </span>
              <span className="v15-tab-l">{s.short}</span>
            </a>
          );
        })}
      </nav>

      <Sheet open={!!sheet} onClose={() => setSheet(null)} title={sheet?.label || ''}>
        {sheet && (
          <div className="v15-sheet">
            <ul className="v15-sheet-list" role="list">
              <li>
                <a href={pathFor(sheet.hub)} onClick={linkClick(() => go(sheet.hub))} aria-current={active === sheet.hub ? 'page' : undefined} className="v15-sheet-a">
                  <sheet.icon aria-hidden="true" />
                  <span>{sheet.label} merkezi</span>
                  <ChevronRight className="v15-chev" aria-hidden="true" />
                </a>
              </li>
              {sheet.items.map((it) => (
                <li key={it.id}>
                  <a href={pathFor(it.id)} onClick={linkClick(() => go(it.id))} aria-current={active === it.id ? 'page' : undefined} className="v15-sheet-a">
                    <it.icon aria-hidden="true" />
                    <span>
                      {it.label}
                      <small>{it.hint}</small>
                    </span>
                    <ChevronRight className="v15-chev" aria-hidden="true" />
                  </a>
                </li>
              ))}
            </ul>
            <div className="v15-sheet-tools" role="group" aria-label="Araçlar">
              <button type="button" onClick={() => { setSheet(null); onPdf(); }}><FileDown aria-hidden="true" />PDF</button>
              {onOffline && <button type="button" onClick={() => { setSheet(null); onOffline(); }}><Database aria-hidden="true" />Çevrimdışı</button>}
              <button type="button" onClick={() => { setSheet(null); window.dispatchEvent(new Event('medsoru:pending')); }}>
                <CloudUpload aria-hidden="true" />Kuyruk{queued > 0 ? ` · ${queued}` : ''}
              </button>
              <button type="button" onClick={() => { setSheet(null); toggleAppFs(); }}>{appFs ? <Minimize2 aria-hidden="true" /> : <Maximize2 aria-hidden="true" />}Tam ekran</button>
              {isAdmin && <a href={pathFor('manage')} onClick={linkClick(() => go('manage'))}><ShieldCheck aria-hidden="true" />Yönetim</a>}
              <a href={pathFor('settings')} onClick={linkClick(() => go('settings'))}><NAV_ITEMS.settings.icon aria-hidden="true" />Ayarlar</a>
            </div>
          </div>
        )}
      </Sheet>
    </>
  );
};
