import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowLeft, Search, RefreshCw, Moon, Sun, ChevronDown, AlignJustify, Menu, X } from 'lucide-react';
import type { Committee } from '../../types';
import type { ManageSection } from '../manage/ManageConsole';
import type { RealtimeConnectionStatus } from '../../services/realtimeEvents';
import type { M12NavGroup } from '../v12/ManageV12';
import '../../styles/v14/manage.css';

/**
 * Yönetim konsolu — v14 kabuğu (canvas: "MeDSor Yönetim Paneli v14", Main/Nav/Bilesenler.dc.html).
 * - Her bölüm kendi sayfası; sol menü gruplu ve içinde arama var, dar ekranda içerik üstüne katlanır (çekmece yok).
 * - Ayrıntı/düzenleme alanları (consoleUi Drawer) bu kabukta içerik alanının tamamına yerleşir: html.m14-on.
 * - Veri ve işlevler ManageConsole'da kalır; bu bileşen yalnız düzen ve gezinmedir. Önek: m14-.
 */

const LIVE_TEXT: Record<RealtimeConnectionStatus, string> = { connected: 'Bağlı', connecting: 'Bağlanıyor', disconnected: 'Bağlantı yok' };
const fold = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '');

export const ManageShellV14: React.FC<{
  groups: M12NavGroup[];
  section: ManageSection;
  currentLabel: string;
  currentGroup: string;
  currentHint: React.ReactNode;
  headCount?: { n: number; alert?: boolean };
  onPick: (id: ManageSection) => void;
  onOpenPalette: () => void;
  onExit: () => void;
  adminEmail: string;
  sourceLive: boolean;
  canSwitchSource: boolean;
  onChooseSource: (t: 'oracle' | 'yerel') => void;
  liveStatus: RealtimeConnectionStatus;
  syncLabel: string;
  dense: boolean;
  onToggleDense: () => void;
  committees: Committee[];
  selectedCommitteeId: string;
  onSelectCommittee: (id: string) => void;
  loading: boolean;
  onRefresh: () => void;
  theme: string;
  onToggleTheme: () => void;
  bodyDensity: string;
  wide?: boolean;
  fullscreen: boolean;
  children: React.ReactNode;
}> = (p) => {
  const [q, setQ] = useState('');
  const [navOpen, setNavOpen] = useState(false);
  const navRef = useRef<HTMLElement>(null);
  const mainRef = useRef<HTMLElement>(null);

  // Tam alan çalışma alanları (Drawer) bu bayrağa bakar
  useEffect(() => {
    const el = document.documentElement;
    el.classList.add('m14-on');
    return () => el.classList.remove('m14-on');
  }, []);
  useEffect(() => {
    setNavOpen(false);
    mainRef.current?.scrollTo({ top: 0 });
    navRef.current?.querySelector('.m14-nav-i.on')?.scrollIntoView({ block: 'nearest' });
  }, [p.section]);

  const groups = useMemo(() => {
    const f = fold(q.trim());
    if (!f) return p.groups;
    return p.groups
      .map((g) => ({ ...g, items: g.items.filter((it) => fold(`${it.label} ${it.hint}`).includes(f)) }))
      .filter((g) => g.items.length > 0);
  }, [p.groups, q]);
  const flat = groups.flatMap((g) => g.items);
  const liveText = LIVE_TEXT[p.liveStatus] || 'Bağlantı yok';

  const navButton = (it: M12NavGroup['items'][number]) => {
    const on = it.id === p.section;
    const Icon = it.icon;
    return (
      <button key={it.id} type="button" className={`m14-nav-i ${on ? 'on' : ''}`} aria-current={on ? 'page' : undefined} onClick={() => p.onPick(it.id)} title={it.hint}>
        <Icon aria-hidden="true" />
        <span className="l">{it.label}</span>
        {it.badge && it.badge.n > 0 && (
          <span className={`c ${it.badge.alert && !on ? 'hot' : ''}`} aria-label={`${it.badge.n} bekleyen`}>{it.badge.n.toLocaleString('tr-TR')}</span>
        )}
      </button>
    );
  };

  return (
    <div className={`ms-console m14-app ${p.fullscreen ? 'is-full' : 'is-inline'}`} data-m14-dense={p.dense ? 'tight' : 'cozy'}>
      <aside className={`m14-side ${navOpen ? 'is-open' : ''}`} aria-label="Yönetim menüsü">
        <div className="m14-brand-row">
          <button type="button" className="m14-brand" onClick={p.onExit} title="Öğrenci sitesine dön">
            <i aria-hidden="true">M</i>
            <span className="w">MeDSor<small>Yönetim</small></span>
          </button>
          <button type="button" className="m14-btn ghost icon m14-navtoggle" onClick={() => setNavOpen((v) => !v)} aria-expanded={navOpen} aria-label={navOpen ? 'Menüyü kapat' : 'Menüyü aç'}>
            {navOpen ? <X aria-hidden="true" /> : <Menu aria-hidden="true" />}
          </button>
        </div>
        <div className="m14-side-body">
          <label className="m14-navsearch">
            <Search aria-hidden="true" />
            <input
              type="search"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && flat[0]) { p.onPick(flat[0].id); setQ(''); }
                if (e.key === 'Escape') setQ('');
              }}
              placeholder="Sayfa ara"
              aria-label="Yönetim sayfası ara"
            />
            <button type="button" className="m14-kbd" onClick={p.onOpenPalette} title="Tüm işler (Ctrl+K)">Ctrl K</button>
          </label>
          <nav className="m14-nav" aria-label="Yönetim bölümleri" ref={navRef}>
            {groups.map((g, gi) =>
              !g.label ? (
                <React.Fragment key={`g${gi}`}>{g.items.map(navButton)}</React.Fragment>
              ) : (
                <div key={g.label} className="m14-grp" role="group" aria-labelledby={`m14-g-${gi}`}>
                  <div className="m14-grp-h" id={`m14-g-${gi}`}>{g.label}</div>
                  {g.items.map(navButton)}
                </div>
              ),
            )}
            {groups.length === 0 && <p className="m14-empty">“{q}” ile eşleşen sayfa yok.</p>}
          </nav>
          <button type="button" className="m14-nav-i m14-exit" onClick={p.onExit}>
            <ArrowLeft aria-hidden="true" />
            <span className="l">Öğrenci sitesine dön</span>
          </button>
        </div>
      </aside>

      <div className="m14-main">
        <header className={`m14-top ${p.sourceLive ? 'is-live' : ''}`}>
          <div className="m14-title">
            <span className="g">{p.currentGroup}</span>
            <h1>
              {p.currentLabel}
              {p.headCount && p.headCount.n > 0 && <span className={`m14-pill ${p.headCount.alert ? 'bad' : 'acc'}`}>{p.headCount.n.toLocaleString('tr-TR')}</span>}
            </h1>
          </div>
          <div className="m14-tools">
            {p.canSwitchSource ? (
              <div className="m14-seg" role="group" aria-label="Veri kaynağı">
                <button type="button" className={p.sourceLive ? 'on' : ''} aria-pressed={p.sourceLive} onClick={() => !p.sourceLive && p.onChooseSource('oracle')} title="Değişiklikler doğrudan canlı siteye (Oracle) yazılır">Canlı</button>
                <button type="button" className={!p.sourceLive ? 'on' : ''} aria-pressed={!p.sourceLive} onClick={() => p.sourceLive && p.onChooseSource('yerel')} title="Bu bilgisayardaki sunucu (deneme)">Yerel</button>
              </div>
            ) : (
              <span className={`m14-pill ${p.sourceLive ? 'warn' : ''}`}>{p.sourceLive ? 'Canlı' : 'Yerel'}</span>
            )}
            <label className="m14-select" title={p.committees.find((c) => c.id === p.selectedCommitteeId)?.name}>
              <span className="sr-only">Kurul</span>
              <select value={p.selectedCommitteeId} onChange={(e) => p.onSelectCommittee(e.target.value)}>
                {p.committees.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
              <ChevronDown aria-hidden="true" />
            </label>
            <span className={`m14-live is-${p.liveStatus}`} role="status" title={p.syncLabel ? `Son eşitleme ${p.syncLabel}` : undefined}>
              <i aria-hidden="true" />{liveText}
            </span>
            <button type="button" className="m14-btn ghost icon" onClick={p.onToggleDense} aria-pressed={p.dense} aria-label={`Yoğunluk: ${p.dense ? 'Sıkı' : 'Rahat'}`} title="Yoğunluk">
              <AlignJustify aria-hidden="true" />
            </button>
            <button type="button" className="m14-btn ghost icon" onClick={p.onRefresh} disabled={p.loading} aria-label="Verileri yenile" title="Verileri yenile">
              <RefreshCw className={p.loading ? 'm14-spin' : ''} aria-hidden="true" />
            </button>
            <button type="button" className="m14-btn ghost icon" onClick={p.onToggleTheme} aria-label={p.theme === 'dark' ? 'Açık temaya geç' : 'Koyu temaya geç'}>
              {p.theme === 'dark' ? <Sun aria-hidden="true" /> : <Moon aria-hidden="true" />}
            </button>
            <span className="m14-me" role="img" aria-label={`Yönetici: ${p.adminEmail || 'Yönetici'}`} title={p.adminEmail}>
              {(p.adminEmail || 'Y').charAt(0).toLocaleUpperCase('tr-TR')}
            </span>
          </div>
        </header>
        {p.sourceLive && p.canSwitchSource && <div className="m14-livebar" role="note">Canlı veriye bağlısınız: yaptığınız değişiklikler doğrudan siteye yazılır.</div>}
        <main ref={mainRef} key={p.section} className="ms-console-body m14-body" data-density={p.bodyDensity} aria-label={p.currentLabel}>
          <div className={`ms-cinner m14-inner ${p.wide ? 'is-wide' : ''}`}>
            {p.currentHint && <p className="m14-hint">{p.currentHint}</p>}
            {p.children}
          </div>
        </main>
      </div>
    </div>
  );
};
