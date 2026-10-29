import React, { useLayoutEffect, useRef, useState } from 'react';
import { Activity, PanelLeftClose, PanelLeftOpen, Search, ShieldCheck } from 'lucide-react';
import { linkClick, pathFor, type AppRoute } from '../../router';
import type { AppUser } from '../../services/auth';
import { NAV_ITEMS, NAV_TREE, initialsOf, openSearch } from './navModel';
import { BrandWord } from './BrandWord';
import { useSideCollapse } from './shellHooks';
import { useAppearance } from '../../utils/appearance';
import { SideNavV12 } from '../v12/ShellV12';
import { SideNavV13 } from '../v13/ShellV13';
import { SideNavV15 } from '../v15/ShellV15';

export type SideNavProps = { active: AppRoute; onGo: (r: AppRoute) => void; isAdmin: boolean; user: AppUser | null };

/** v12 "Net" tasarımında kendi rayı (components/v12/ShellV12); v10/v11 aşağıdaki klasik menü. */
export const SideNav: React.FC<SideNavProps> = (props) => {
  const a = useAppearance();
  if (a.design !== 'v12') return <SideNavClassic {...props} />;
  if (a.v15) return <SideNavV15 {...props} />;
  return a.v13 ? <SideNavV13 {...props} /> : <SideNavV12 {...props} />;
};

/**
 * v8 kenar menüsü (≥768px). Tablette 72px simge rayı (kısa etiketli), masaüstünde 236px gruplu menü;
 * masaüstünde daraltılabilir. Etkin sayfayı tek bir kayan vurgu izler (yayla).
 * Altta: yönetim (yöneticiye) ve kullanıcı kartı → Profil ve ayarlar.
 */
const SideNavClassic: React.FC<SideNavProps> = ({ active, onGo, isAdmin, user }) => {
  const { collapsed, setCollapsed } = useSideCollapse();

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
          <BrandWord />
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
