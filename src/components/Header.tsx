import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
import {
  Plus,
  Search,
  ShieldCheck,
  CloudUpload,
  LogOut,
  FileDown,
  FileUp,
  LogIn,
  NotebookPen,
  Activity,
  FolderPlus,
  LayoutGrid,
  BookCopy,
  UserRound,
  IdCard,
  ChevronDown,
  House,
  Library,
  Archive,
  ListChecks,
  BookOpenText,
  BookOpen,
  Trophy,
  SquarePen,
  GraduationCap,
  MoreHorizontal,
  Mic,
  Music,
  Layers,
  Sparkles,
  Compass,
  Target,
  Moon,
  Sun,
  Palette,
} from 'lucide-react';
import { useTheme } from '../utils/theme';
import { useUiVersion } from '../utils/uiVersion';
import { Committee } from '../types';
import { AppUser } from '../services/auth';
import { SearchPalette } from './search/SearchPalette';
import { AppRoute, pathFor, linkClick } from '../router';

export type AppTab = AppRoute;

interface HeaderProps {
  committees: Committee[];
  selectedCommitteeId: string;
  onSelectCommittee: (id: string) => void;
  activeTab: AppTab;
  setActiveTab: (tab: AppTab) => void;
  onOpenContributeModal: () => void;
  onOpenNewCommitteeModal: () => void;
  onOpenAdminPanel: () => void;
  onOpenPastExamModal?: () => void;
  onOpenNotebookLMModal?: () => void;
  onOpenSubagentMonitor?: () => void;
  onOpenProfileModal?: () => void;
  onOpenAuthModal?: (mode: 'login' | 'register' | 'admin') => void;
  completedCount: number;
  totalCount: number;
  targetCount: number;
  // Search
  searchQuery?: string;
  onSearch?: (query: string, focusId?: string) => void;
  // Auth & Drive Props
  currentUser: AppUser | null;
  isAdmin: boolean;
  onLogin: () => void;
  onLogout: () => void;
  isLoggingIn: boolean;
  onUploadToDrive: () => void;
  isUploadingToDrive: boolean;
  driveLastUploadedLink: string | null;
  onOpenPdfModal: () => void;
  onOpenDiagnostics?: () => void;
}

/** Primary pages, in priority order: the desktop nav shows as many as fit, the rest go under "Daha". */
export const NAV: { id: AppTab; label: string; icon: React.ElementType }[] = [
  { id: 'quick_add', label: 'Soru ekle', icon: SquarePen },
  { id: 'past_exams', label: 'Çıkmış sorular', icon: Archive },
  { id: 'ornek_sorular', label: 'Örnek sorular', icon: Target },
  { id: 'questions', label: 'Soru havuzu', icon: Library },
  { id: 'study', label: 'Çalış', icon: ListChecks },
  { id: 'kazanimlar', label: 'Kazanımlar', icon: Compass },
  { id: 'learn', label: 'Öğren', icon: GraduationCap },
  { id: 'glossary', label: 'Sözlük', icon: BookOpenText },
  { id: 'flashcards', label: 'Kartlar', icon: Layers },
  { id: 'leaderboard', label: 'Sıralama', icon: Trophy },
  { id: 'music', label: 'Müzik', icon: Music },
  { id: 'summaries', label: 'Ders özetleri', icon: BookOpen },
  { id: 'matrix', label: 'Soru haritası', icon: LayoutGrid },
];

/** How many NAV entries the desktop bar may show before folding the rest into "Daha". */
const NAV_PRIMARY = 9;
/** v3: dört ana yer önde, gerisi "Daha" menüsünde. */
const V3_ORDER: AppTab[] = ['quick_add', 'past_exams', 'ornek_sorular', 'learn', 'kazanimlar', 'study', 'questions', 'glossary', 'flashcards', 'summaries', 'leaderboard', 'music', 'matrix'];

export const BrandMark: React.FC<{ size?: number }> = ({ size = 34 }) => (
  <span
    className="rounded-lg bg-accent flex items-center justify-center shrink-0"
    style={{ width: size, height: size }}
  >
    <Plus className="text-white" style={{ width: size * 0.53, height: size * 0.53 }} strokeWidth={2.6} />
  </span>
);

const initialsOf = (user: AppUser | null) => {
  const src = (user?.displayName || user?.email || 'Ö').trim();
  const parts = src.split(/[^\p{L}]+/u).filter(Boolean);
  return ((parts[0]?.[0] || 'Ö') + (parts[1]?.[0] || '')).toLocaleUpperCase('tr-TR');
};

/**
 * Desktop nav that never overflows: every tab is measured off-screen, as many as
 * fit are shown, and the rest move into a "Daha" menu. Re-measures on resize,
 * breakpoint changes (icons/padding) and font load.
 */
const PriorityNav: React.FC<{
  items: { id: AppTab; label: string; icon: React.ElementType }[];
  active: AppTab;
  onSelect: (id: AppTab) => void;
  max?: number;
}> = ({ items, active, onSelect, max = NAV_PRIMARY }) => {
  const navRef = useRef<HTMLElement>(null);
  const measureRef = useRef<HTMLDivElement>(null);
  const moreRef = useRef<HTMLDivElement>(null);
  const [count, setCount] = useState(items.length);
  const [open, setOpen] = useState(false);

  useLayoutEffect(() => {
    const nav = navRef.current;
    const measure = measureRef.current;
    if (!nav || !measure) return;
    const GAP = 2;
    const compute = () => {
      const avail = nav.clientWidth;
      if (!avail) return;
      const kids = Array.from(measure.children) as HTMLElement[];
      const widths = kids.slice(0, items.length).map((k) => k.offsetWidth);
      const moreW = (kids[items.length]?.offsetWidth || 80) + GAP;
      const all = widths.reduce((a, b) => a + b, 0) + GAP * (widths.length - 1);
      if (all <= avail) return setCount(items.length);
      let used = 0;
      let c = 0;
      for (const w of widths) {
        if (used + w + moreW > avail) break;
        used += w + GAP;
        c++;
      }
      setCount(c);
    };
    compute();
    const ro = new ResizeObserver(compute);
    ro.observe(nav);
    ro.observe(measure);
    (document as any).fonts?.ready?.then(compute);
    return () => ro.disconnect();
  }, [items]);

  useEffect(() => {
    if (!open) return;
    const onDown = (e: MouseEvent) => moreRef.current && !moreRef.current.contains(e.target as Node) && setOpen(false);
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setOpen(false);
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDown);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);

  const itemCls = (on: boolean) =>
    `h-9 px-3 rounded-lg text-[13px] font-medium whitespace-nowrap cursor-pointer transition-colors inline-flex items-center gap-2 shrink-0 ${
      on ? 'bg-accent-soft text-accent font-semibold' : 'text-ink-2 hover:text-ink hover:bg-canvas'
    }`;
  const shown = items.slice(0, Math.min(count, max));
  const hidden = items.slice(Math.min(count, max));
  const activeHidden = hidden.some((i) => i.id === active);

  return (
    <nav ref={navRef} aria-label="Ana menü" className="hidden lg:flex items-center gap-0.5 flex-1 min-w-0 relative">
      {/* off-screen measuring row (same classes, never visible) */}
      <div ref={measureRef} aria-hidden="true" className="absolute left-0 top-0 flex gap-0.5 invisible pointer-events-none h-0 overflow-hidden">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <span key={item.id} className={itemCls(item.id === active)}>
              <Icon className="hidden w-4 h-4 shrink-0" />
              {item.label}
            </span>
          );
        })}
        <span className={itemCls(false)}>
          <MoreHorizontal className="w-4 h-4" />
          Daha
        </span>
      </div>

      {shown.map((item) => {
        const on = active === item.id;
        const Icon = item.icon;
        return (
          <a key={item.id} href={pathFor(item.id)} onClick={linkClick(() => onSelect(item.id))} aria-current={on ? 'page' : undefined} className={itemCls(on)}>
            <Icon className="hidden w-4 h-4 shrink-0" strokeWidth={on ? 2.3 : 2} />
            {item.label}
          </a>
        );
      })}

      {hidden.length > 0 && (
        <div className="relative shrink-0" ref={moreRef}>
          <button
            type="button"
            onClick={() => setOpen((v) => !v)}
            aria-haspopup="menu"
            aria-expanded={open}
            className={itemCls(activeHidden)}
          >
            <MoreHorizontal className="w-4 h-4" />
            {activeHidden ? hidden.find((i) => i.id === active)?.label : 'Daha'}
            <ChevronDown className={`w-3.5 h-3.5 transition-transform ${open ? 'rotate-180' : ''}`} />
          </button>
          {open && (
            <div role="menu" className="absolute left-0 top-11 min-w-[220px] bg-white border border-line rounded-2xl shadow-lg p-1.5 z-50">
              {hidden.map((item) => {
                const Icon = item.icon;
                const on = active === item.id;
                return (
                  <a
                    key={item.id}
                    href={pathFor(item.id)}
                    role="menuitem"
                    onClick={linkClick(() => {
                      setOpen(false);
                      onSelect(item.id);
                    })}
                    className={`w-full min-h-10 px-2.5 rounded-[10px] flex items-center gap-2.5 text-left text-[14px] cursor-pointer ${
                      on ? 'bg-accent-soft text-accent font-semibold' : 'text-ink hover:bg-canvas'
                    }`}
                  >
                    <Icon className="w-4 h-4 shrink-0" />
                    {item.label}
                  </a>
                );
              })}
            </div>
          )}
        </div>
      )}
    </nav>
  );
};

export const Header: React.FC<HeaderProps> = ({
  committees,
  selectedCommitteeId,
  activeTab,
  setActiveTab,
  onOpenContributeModal,
  onOpenNewCommitteeModal,
  onOpenAdminPanel,
  onOpenPastExamModal,
  onOpenNotebookLMModal,
  onOpenSubagentMonitor,
  onOpenProfileModal,
  onOpenAuthModal,
  searchQuery = '',
  onSearch,
  currentUser,
  isAdmin,
  onLogin,
  onLogout,
  isLoggingIn,
  onUploadToDrive,
  isUploadingToDrive,
  driveLastUploadedLink,
  onOpenPdfModal,
  onOpenDiagnostics,
}) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [mobileSearchOpen, setMobileSearchOpen] = useState(false);
  const { theme, toggle: toggleTheme } = useTheme();
  const { ui, isV3, toggleUi } = useUiVersion();
  const [query, setQuery] = useState(searchQuery);
  const menuRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLInputElement>(null);

  useEffect(() => setQuery(searchQuery), [searchQuery]);

  // Close the account menu on outside click / Escape
  useEffect(() => {
    if (!menuOpen) return;
    const onDown = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) setMenuOpen(false);
    };
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setMenuOpen(false);
    document.addEventListener('mousedown', onDown);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', onDown);
      document.removeEventListener('keydown', onKey);
    };
  }, [menuOpen]);

  // "/" focuses the search field
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      const isK = (e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k';
      if (!isK && (e.key !== '/' || ['INPUT', 'TEXTAREA', 'SELECT'].includes(t.tagName) || t.isContentEditable)) return;
      e.preventDefault();
      setMobileSearchOpen(true);
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, []);

  const submitSearch = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch?.(query.trim());
    setMobileSearchOpen(false);
  };

  const run = (fn?: () => void) => () => {
    setMenuOpen(false);
    fn?.();
  };

  const openAdmin = () => {
    if (!isAdmin) return;
    onOpenAdminPanel();
  };

  const currentCommittee = committees.find((c) => c.id === selectedCommitteeId);

  const MenuItem: React.FC<{
    icon: React.ElementType;
    label: string;
    onClick: () => void;
    hint?: string;
    disabled?: boolean;
    className?: string;
    tone?: 'default' | 'accent';
  }> = ({ icon: Icon, label, onClick, hint, disabled, className = '', tone = 'default' }) => (
    <button
      type="button"
      role="menuitem"
      disabled={disabled}
      onClick={run(onClick)}
      className={`w-full min-h-11 px-2 rounded-[10px] flex items-center gap-3 text-left text-[14px] text-ink hover:bg-canvas disabled:opacity-50 cursor-pointer ${className}`}
    >
      <span
        className={`w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${
          tone === 'accent' ? 'bg-accent text-white' : 'bg-canvas text-ink-2'
        }`}
      >
        <Icon className="w-4 h-4" strokeWidth={2} />
      </span>
      <span className={`flex-1 ${tone === 'accent' ? 'font-semibold' : ''}`}>{label}</span>
      {hint && <span className="text-[12px] text-ok font-semibold">{hint}</span>}
    </button>
  );

  const MenuLabel: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <div className="px-2 pt-3 pb-1 text-[11px] font-semibold uppercase tracking-[0.08em] text-ink-3">{children}</div>
  );

  return (
    <header className="bg-white md:bg-canvas border-b border-line sticky top-0 z-30 print:hidden">
      <div className="px-4 sm:px-6 lg:px-8 h-14 flex items-center gap-2 sm:gap-3">
        {/* Telefon: logo. Tablet/masaüstü: logo ve menü kenar çubuğunda; burada sayfa başlığı */}
        <a
          href={pathFor('quick_add')}
          onClick={linkClick(() => setActiveTab('quick_add'))}
          className="md:hidden flex items-center gap-2 cursor-pointer shrink-0"
          aria-label="MeDSor ana sayfa"
        >
          <BrandMark size={28} />
          <span className="font-display font-bold text-[18px] tracking-[-0.02em] text-ink">Me<span className="text-accent">DS</span>or</span>
        </a>
        <span className="flex-1" aria-hidden="true" />

        <button
          type="button"
          onClick={toggleTheme}
          aria-label={theme === 'dark' ? 'Açık temaya geç' : 'Koyu temaya geç'}
          title={theme === 'dark' ? 'Açık tema' : 'Koyu tema'}
          className="w-10 h-10 rounded-xl flex items-center justify-center cursor-pointer shrink-0 bg-canvas text-ink hover:bg-line-soft transition-colors"
        >
          {theme === 'dark' ? <Sun className="w-[18px] h-[18px]" /> : <Moon className="w-[18px] h-[18px]" />}
        </button>

        <button
          type="button"
          onClick={() => setMobileSearchOpen((v) => !v)}
          aria-label="Ara"
          aria-expanded={mobileSearchOpen}
          title="Ara  ( / ya da Ctrl+K )"
          className={`w-10 h-10 rounded-xl flex items-center justify-center cursor-pointer shrink-0 transition-colors ${
            mobileSearchOpen ? 'bg-accent-soft text-accent' : 'bg-canvas text-ink hover:bg-line-soft'
          }`}
        >
          <Search className="w-[18px] h-[18px]" />
        </button>

        <div className="relative shrink-0" ref={menuRef}>
          <button
            type="button"
            onClick={() => setMenuOpen((v) => !v)}
            aria-haspopup="menu"
            aria-expanded={menuOpen}
            aria-label="Hesap ve araçlar"
            className={`h-10 pl-1 pr-1 sm:pr-2 rounded-full border bg-white flex items-center gap-1 cursor-pointer ${
              menuOpen ? 'border-accent' : 'border-line hover:border-line-2'
            }`}
          >
            {currentUser?.photoURL ? (
              <img src={currentUser.photoURL} alt="" className="w-8 h-8 rounded-full" />
            ) : (
              <span className="w-8 h-8 rounded-full bg-ink text-white flex items-center justify-center text-[12px] font-semibold">
                {currentUser ? initialsOf(currentUser) : <UserRound className="w-4 h-4" />}
              </span>
            )}
            <ChevronDown className={`hidden sm:block w-3.5 h-3.5 text-ink-2 transition-transform ${menuOpen ? 'rotate-180' : ''}`} />
          </button>

          {menuOpen && (
            <div
              role="menu"
              className="fixed sm:absolute left-3 right-3 sm:left-auto sm:right-0 top-[60px] sm:top-12 sm:w-[300px] max-h-[calc(100dvh-140px)] sm:max-h-[calc(100vh-96px)] overflow-y-auto bg-white border border-line rounded-2xl shadow-lg p-2 z-50"
            >
              <div className="flex items-center gap-3 px-2 py-2.5">
                <span className="w-10 h-10 rounded-full bg-ink text-white flex items-center justify-center text-[13px] font-semibold shrink-0">
                  {currentUser ? initialsOf(currentUser) : <UserRound className="w-4 h-4" />}
                </span>
                <div className="min-w-0">
                  {currentUser ? (
                    <>
                      <div className="font-semibold text-[15px] text-ink truncate">
                        {currentUser.displayName || currentUser.email?.split('@')[0]}
                      </div>
                      <div className="text-[13px] text-ink-3 truncate">
                        {currentUser.studentNumber ? `No: ${currentUser.studentNumber}` : currentUser.email}
                        {isAdmin ? ' · Yönetici' : ''}
                      </div>
                    </>
                  ) : (
                    <div className="text-[14px] text-ink-2">Giriş yapmadın. Katkı için isim gerekmez.</div>
                  )}
                </div>
              </div>

              <MenuItem icon={SquarePen} label="Soru katkısı yap" tone="accent" onClick={onOpenContributeModal} />

              <MenuItem icon={FileDown} label="PDF indir" onClick={onOpenPdfModal} />


              {isAdmin && (
                <>
                  <MenuLabel>Yönetim</MenuLabel>
                  <MenuItem icon={ShieldCheck} label="Yönetim" onClick={openAdmin} />
                  <MenuItem icon={Activity} label="Test Edilen Çıkmışlar (Faz 14)" onClick={() => setActiveTab('test_cikmis')} />
                  {onOpenDiagnostics && <MenuItem icon={Activity} label="Veritabanı & limit takibi" onClick={onOpenDiagnostics} />}
                  {onOpenPastExamModal && <MenuItem icon={FileUp} label="Çıkmış soru yükle" onClick={onOpenPastExamModal} />}
                  {onOpenNotebookLMModal && <MenuItem icon={NotebookPen} label="NotebookLM / Gemini" onClick={onOpenNotebookLMModal} />}
                  <MenuItem
                    icon={CloudUpload}
                    label={isUploadingToDrive ? "Drive'a yükleniyor…" : "Drive'a kaydet"}
                    hint={driveLastUploadedLink ? 'Güncel' : undefined}
                    disabled={isUploadingToDrive}
                    onClick={onUploadToDrive}
                  />
                  <MenuItem icon={FolderPlus} label="Yeni kurul ekle" onClick={onOpenNewCommitteeModal} />
                  {onOpenSubagentMonitor && <MenuItem icon={Activity} label="AI subagent izleme" onClick={onOpenSubagentMonitor} />}
                </>
              )}

              <MenuLabel>Hesap</MenuLabel>
              {currentUser ? (
                <>
                  {onOpenProfileModal && <MenuItem icon={IdCard} label="Profil ve öğrenci no" onClick={onOpenProfileModal} />}
                  <MenuItem icon={LogOut} label="Çıkış yap" onClick={onLogout} />
                </>
              ) : (
                <>
                  <MenuItem icon={LogIn} label="Öğrenci girişi" onClick={() => (onOpenAuthModal ? onOpenAuthModal('login') : onLogin())} />
                  <MenuItem
                    icon={ShieldCheck}
                    label={isLoggingIn ? 'Giriş yapılıyor…' : 'Yönetici girişi'}
                    disabled={isLoggingIn}
                    onClick={() => (onOpenAuthModal ? onOpenAuthModal('admin') : onLogin())}
                  />
                </>
              )}
            </div>
          )}
        </div>
      </div>

      {mobileSearchOpen && (
        <SearchPalette
          initialQuery={query}
          onClose={() => setMobileSearchOpen(false)}
          onOpenResults={(q, focusId) => { setQuery(q); onSearch?.(q, focusId); }}
        />
      )}
    </header>
  );
};
