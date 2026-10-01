import React, { useEffect, useRef, useState } from 'react';
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
  Trophy,
  SquarePen,
} from 'lucide-react';
import { Committee } from '../types';
import { AppUser, ADMIN_EMAIL, setLocalAdminSession } from '../services/auth';

export type AppTab = 'quick_add' | 'questions' | 'past_exams' | 'matrix' | 'leaderboard' | 'notes' | 'practice' | 'booklet';

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
  onSearch?: (query: string) => void;
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
}

export const NAV: { id: AppTab; label: string; icon: React.ElementType }[] = [
  { id: 'quick_add', label: 'Ana sayfa', icon: House },
  { id: 'questions', label: 'Soru havuzu', icon: Library },
  { id: 'past_exams', label: 'Çıkmış sorular', icon: Archive },
  { id: 'practice', label: 'Test çöz', icon: ListChecks },
  { id: 'notes', label: 'Ders notları', icon: BookOpenText },
  { id: 'leaderboard', label: 'Sıralama', icon: Trophy },
];

export const BrandMark: React.FC<{ size?: number }> = ({ size = 34 }) => (
  <span
    className="rounded-[9px] bg-accent flex items-center justify-center shrink-0"
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
}) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [mobileSearchOpen, setMobileSearchOpen] = useState(false);
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
      if (e.key !== '/' || ['INPUT', 'TEXTAREA', 'SELECT'].includes(t.tagName) || t.isContentEditable) return;
      e.preventDefault();
      searchRef.current?.focus();
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
    if (!isAdmin) setLocalAdminSession(ADMIN_EMAIL);
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
    <header className="bg-white border-b border-line sticky top-0 z-30 print:hidden">
      <div className="max-w-[1280px] mx-auto px-4 sm:px-8 h-14 sm:h-[68px] flex items-center gap-3 lg:gap-4 xl:gap-6">
        <button
          type="button"
          onClick={() => setActiveTab('quick_add')}
          className="flex items-center gap-2.5 cursor-pointer shrink-0"
          aria-label="MedSoru ana sayfa"
        >
          <BrandMark size={30} />
          <span className="font-display font-bold text-[18px] sm:text-[20px] tracking-[-0.02em] text-ink">MedSoru</span>
          <span className="hidden 2xl:inline font-mono text-[11px] px-[7px] py-[3px] border border-line rounded-md text-ink-2">
            DÖNEM {currentCommittee?.year || 3}
          </span>
        </button>

        <nav aria-label="Ana menü" className="hidden lg:flex items-center gap-0.5 flex-1 min-w-0">
          {NAV.map((item) => {
            const active = activeTab === item.id;
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => setActiveTab(item.id)}
                aria-current={active ? 'page' : undefined}
                className={`h-10 px-2 xl:px-2.5 rounded-lg text-[14px] xl:text-[15px] whitespace-nowrap cursor-pointer transition-colors inline-flex items-center gap-2 ${
                  active ? 'bg-accent-soft text-accent font-semibold' : 'text-ink-2 hover:text-ink hover:bg-canvas'
                }`}
              >
                <Icon className="w-4 h-4 shrink-0" strokeWidth={active ? 2.3 : 2} />
                {item.label}
              </button>
            );
          })}
        </nav>

        <span className="flex-1 lg:hidden" />

        <form
          onSubmit={submitSearch}
          role="search"
          className="hidden md:flex items-center gap-2 w-[200px] xl:w-[220px] h-10 px-3 border border-line rounded-[10px] bg-[#F7F8FA] focus-within:border-accent"
        >
          <Search className="w-4 h-4 text-ink-2 shrink-0" />
          <input
            ref={searchRef}
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Soru, konu, ders ara"
            aria-label="Ara"
            className="border-0 outline-0 bg-transparent text-[14px] flex-1 min-w-0 placeholder:text-[#6B7785]"
          />
          <kbd className="font-mono text-[11px] text-ink-2 border border-line rounded-[5px] px-[5px] leading-[18px]">/</kbd>
        </form>

        <button
          type="button"
          onClick={() => setMobileSearchOpen((v) => !v)}
          aria-label="Ara"
          aria-expanded={mobileSearchOpen}
          className="md:hidden w-10 h-10 rounded-xl bg-canvas flex items-center justify-center cursor-pointer"
        >
          <Search className="w-[18px] h-[18px] text-ink" />
        </button>

        <div className="relative shrink-0" ref={menuRef}>
          <button
            type="button"
            onClick={() => setMenuOpen((v) => !v)}
            aria-haspopup="menu"
            aria-expanded={menuOpen}
            aria-label="Hesap ve araçlar"
            className={`h-10 pl-1 pr-2 rounded-full border bg-white flex items-center gap-1 cursor-pointer ${
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
            <ChevronDown className={`w-3.5 h-3.5 text-ink-2 transition-transform ${menuOpen ? 'rotate-180' : ''}`} />
          </button>

          {menuOpen && (
            <div
              role="menu"
              className="fixed sm:absolute left-3 right-3 sm:left-auto sm:right-0 top-[60px] sm:top-12 sm:w-[300px] max-h-[calc(100dvh-140px)] sm:max-h-[calc(100vh-96px)] overflow-y-auto bg-white border border-line rounded-2xl shadow-[0_12px_40px_rgba(14,26,38,0.16)] p-2 z-50"
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

              <MenuLabel>Çalış</MenuLabel>
              <MenuItem icon={Archive} label="Çıkmış sorular" className="lg:hidden" onClick={() => setActiveTab('past_exams')} />
              <MenuItem icon={Trophy} label="Sıralama" className="lg:hidden" onClick={() => setActiveTab('leaderboard')} />
              <MenuItem icon={LayoutGrid} label="Soru haritası" onClick={() => setActiveTab('matrix')} />
              <MenuItem icon={BookCopy} label="A4 kitapçık" onClick={() => setActiveTab('booklet')} />
              <MenuItem icon={FileDown} label="PDF indir" onClick={onOpenPdfModal} />

              <MenuLabel>Yönetim</MenuLabel>
              <MenuItem icon={ShieldCheck} label="Yönetim paneli" onClick={openAdmin} />
              {isAdmin && (
                <>
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
                </>
              )}
              {onOpenSubagentMonitor && <MenuItem icon={Activity} label="AI subagent izleme" onClick={onOpenSubagentMonitor} />}

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
        <form onSubmit={submitSearch} role="search" className="md:hidden px-4 pb-3">
          <div className="flex items-center gap-2 h-11 px-3 border border-line-2 rounded-xl bg-field">
            <Search className="w-4 h-4 text-ink-2" />
            <input
              autoFocus
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Soru, konu, ders ara"
              aria-label="Ara"
              className="border-0 outline-0 bg-transparent text-[16px] flex-1 min-w-0"
            />
          </div>
        </form>
      )}
    </header>
  );
};
