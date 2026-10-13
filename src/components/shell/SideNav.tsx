import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { Activity, PanelLeftClose, PanelLeftOpen, Search, ShieldCheck } from 'lucide-react';
import { linkClick, pathFor, type AppRoute } from '../../router';
import type { AppUser } from '../../services/auth';
import { NAV_ITEMS, NAV_TREE, initialsOf, openSearch } from './navModel';

const COLLAPSE_KEY = 'medsoru_rail_collapsed';

/**
 * v8 kenar menüsü (≥768px). Tablette 72px simge rayı (kısa etiketli), masaüstünde 236px gruplu menü;
 * masaüstünde daraltılabilir. Etkin sayfayı tek bir kayan vurgu izler (yayla).
 * Altta: yönetim (yöneticiye) ve kullanıcı kartı → Profil ve ayarlar.
 */
export const SideNav: React.FC<{ active: AppRoute; onGo: (r: AppRoute) => void; isAdmin: boolean; user: AppUser | null }> = ({ active, onGo, isAdmin, user }) => {
  // Kullanıcının seçimi (null: seçim yok). Seçim yoksa Akış/Odak düzeninde menü daralmış başlar; düzen
  // değişince seçim sıfırlanır. Eskiden bu düzenlerde CSS menüyü zorla daraltıyordu ve düğme işe yaramıyordu.
  const [pref, setPref] = useState<boolean | null>(() => {
    try {
      const v = localStorage.getItem(COLLAPSE_KEY);
      return v === '1' ? true : v === '0' ? false : null;
    } catch {
      return null;
    }
  });
  const [compactLayout, setCompactLayout] = useState(() => /^(akis|odak)$/.test(document.documentElement.dataset.layout || ''));
  useEffect(() => {
    const el = document.documentElement;
    let last = el.dataset.layout;
    const mo = new MutationObserver(() => {
      if (el.dataset.layout === last) return;
      last = el.dataset.layout;
      setCompactLayout(/^(akis|odak)$/.test(last || ''));
      setPref(null);
      try {
        localStorage.removeItem(COLLAPSE_KEY);
      } catch {
        /* ignore */
      }
    });
    mo.observe(el, { attributes: true, attributeFilter: ['data-layout'] });
    return () => mo.disconnect();
  }, []);
  const collapsed = pref ?? compactLayout;
  const setCollapsed = (f: (c: boolean) => boolean) => {
    const next = f(collapsed);
    setPref(next);
    try {
      localStorage.setItem(COLLAPSE_KEY, next ? '1' : '0');
    } catch {
      /* ignore */
    }
  };
  useEffect(() => {
    document.documentElement.dataset.side = collapsed ? 'collapsed' : 'open';
  }, [collapsed]);
  useEffect(() => () => void delete document.documentElement.dataset.side, []);

  // Kayan vurgu: etkin bağlantının konumunu izler
  const listRef = useRef<HTMLDivElement>(null);
  const [ind, setInd] = useState<{ top: number; h: number; on: boolean }>({ top: 0, h: 0, on: false });
  useLayoutEffect(() => {
    const measure = () => {
      const el = listRef.current?.querySelector<HTMLElement>('[aria-current="page"]');
      setInd(el ? { top: el.offsetTop, h: el.offsetHeight, on: true } : (p) => ({ ...p, on: false }));
    };
    measure();
    const ro = new ResizeObserver(measure);
    if (listRef.current) ro.observe(listRef.current);
    return () => ro.disconnect();
  }, [active, collapsed, isAdmin]);

  const link = (id: AppRoute, label: string, short: string | undefined, Icon: React.ElementType) => {
    const on = active === id;
    return (
      <a
        key={id}
        href={pathFor(id)}
        onClick={linkClick(() => onGo(id))}
        aria-current={on ? 'page' : undefined}
        className="sh-side-link"
        title={label}
      >
        <span className="sh-side-ic" aria-hidden="true"><Icon strokeWidth={on ? 2.3 : 2} /></span>
        <span className="sh-side-label">{label}</span>
        <span className="sh-side-short" aria-hidden="true">{short || label}</span>
      </a>
    );
  };

  return (
    <nav aria-label="Ana menü" className="sh-side print:hidden">
      <div className="sh-side-top">
        <a href={pathFor('quick_add')} onClick={linkClick(() => onGo('quick_add'))} className="sh-brand" aria-label="MeDSor ana sayfa">
          <span className="sh-brand-mark"><Activity strokeWidth={2.4} /></span>
          <span className="sh-brand-word">Me<b>DS</b>or</span>
        </a>
        <button
          type="button"
          className="sh-side-collapse"
          onClick={() => setCollapsed((c) => !c)}
          aria-label={collapsed ? 'Menüyü genişlet' : 'Menüyü daralt'}
          title={collapsed ? 'Menüyü genişlet' : 'Menüyü daralt'}
        >
          {collapsed ? <PanelLeftOpen /> : <PanelLeftClose />}
        </button>
      </div>

      <button type="button" className="sh-side-search" onClick={openSearch} aria-label="Ara" title="Ara ( / ya da Ctrl+K )">
        <Search />
        <span className="sh-side-label">Ara</span>
        <kbd className="sh-side-label">⌘K</kbd>
      </button>

      <a
        href={pathFor('quick_add')}
        onClick={linkClick(() => onGo('quick_add'))}
        aria-current={active === 'quick_add' ? 'page' : undefined}
        className="sh-side-add"
        title="Soru ekle"
      >
        <NAV_ITEMS.quick_add.icon strokeWidth={2.3} aria-hidden="true" />
        <span className="sh-side-label">Soru ekle</span>
      </a>

      <div className="sh-side-list" ref={listRef}>
        <span
          className="sh-side-ind"
          aria-hidden="true"
          style={{ transform: `translateY(${ind.top}px)`, height: ind.h, opacity: ind.on ? 1 : 0 }}
        />
        {NAV_TREE.map((g, gi) => (
          <div key={g.label || gi} className="sh-side-group" role="group" aria-label={g.label || undefined}>
            {g.label && <span className="sh-side-gl" aria-hidden="true">{g.label}</span>}
            {g.items.map((it) => link(it.id, it.label, it.short, it.icon))}
          </div>
        ))}
        <span className="flex-1" aria-hidden="true" />
        {isAdmin && (
          <div className="sh-side-group">{link('manage', 'Yönetim konsolu', 'Yönetim', ShieldCheck)}</div>
        )}
      </div>

      <a
        href={pathFor('settings')}
        onClick={linkClick(() => onGo('settings'))}
        aria-current={active === 'settings' ? 'page' : undefined}
        className="sh-side-user"
        title="Profil ve ayarlar"
      >
        <span className="ui-avatar" style={{ '--av': '32px' } as React.CSSProperties}>
          {user?.photoURL ? <img src={user.photoURL} alt="" /> : user ? initialsOf(user) : <NAV_ITEMS.settings.icon className="w-4 h-4" />}
        </span>
        <span className="sh-side-label sh-side-user-t">
          <b>{user ? user.displayName || user.email?.split('@')[0] : 'Giriş yapmadın'}</b>
          <span>Profil ve ayarlar</span>
        </span>
      </a>
    </nav>
  );
};
