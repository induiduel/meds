import React, { useEffect, useState } from 'react';
import {
  Plus,
  SquarePen,
  GraduationCap,
  BookOpenText,
  Layers,
  Archive,
  Library,
  ListChecks,
  Trophy,
  BookOpen,
  ShieldCheck,
  BotMessageSquare,
  PanelLeftClose,
  PanelLeftOpen,
} from 'lucide-react';
import type { AppTab } from './Header';
import { pathFor, linkClick } from '../router';

/** v3 rail: every page one tap away on tablet and desktop. Phones use MobileBottomNav. */
export const RAIL: { id: AppTab; label: string; icon: React.ElementType }[] = [
  { id: 'quick_add', label: 'Ekle', icon: SquarePen },
  { id: 'ai_chat', label: 'Asistan', icon: BotMessageSquare },
  { id: 'learn', label: 'Öğren', icon: GraduationCap },
  { id: 'past_exams', label: 'Çıkmış', icon: Archive },
  { id: 'glossary', label: 'Sözlük', icon: BookOpenText },
  { id: 'flashcards', label: 'Kartlar', icon: Layers },
  { id: 'questions', label: 'Havuz', icon: Library },
  { id: 'study', label: 'Çalış', icon: ListChecks },
  { id: 'leaderboard', label: 'Sıralama', icon: Trophy },
  { id: 'summaries', label: 'Özetler', icon: BookOpen },
];

interface AppRailProps {
  activeTab: AppTab;
  setActiveTab: (tab: AppTab) => void;
  isAdmin: boolean;
}

const COLLAPSE_KEY = 'medsoru_rail_collapsed';

export const AppRail: React.FC<AppRailProps> = ({ activeTab, setActiveTab, isAdmin }) => {
  // Masaüstünde kenar çubuğu daraltılabilir (yalnızca simgeler); tercih hatırlanır
  const [collapsed, setCollapsed] = useState(() => {
    try { return localStorage.getItem(COLLAPSE_KEY) === '1'; } catch { return false; }
  });
  useEffect(() => {
    document.documentElement.classList.toggle('rail-collapsed', collapsed);
    try { localStorage.setItem(COLLAPSE_KEY, collapsed ? '1' : '0'); } catch { /* gizli pencere */ }
  }, [collapsed]);

  const item = (id: AppTab, label: string, Icon: React.ElementType) => {
    const on = activeTab === id;
    return (
      <a
        key={id}
        href={pathFor(id)}
        onClick={linkClick(() => setActiveTab(id))}
        aria-current={on ? 'page' : undefined}
        title={label}
        className={`ms-rail-item w-[62px] lg:w-full shrink-0 py-[7px] lg:py-0 lg:h-10 lg:px-3 rounded-xl flex flex-col lg:flex-row items-center gap-[3px] lg:gap-3 text-[11px] lg:text-[14px] leading-none transition-colors ${
          on ? 'bg-accent-soft text-accent font-semibold' : 'text-ink-3 hover:text-ink hover:bg-canvas font-medium'
        }`}
      >
        <Icon className="w-[21px] h-[21px] lg:w-[18px] lg:h-[18px] shrink-0" strokeWidth={on ? 2.3 : 2} />
        <span className="ms-rail-label truncate">{label}</span>
      </a>
    );
  };

  return (
    <nav
      aria-label="Ana menü"
      className="ms-rail hidden md:flex fixed left-0 top-0 bottom-0 z-40 w-[76px] lg:w-[232px] flex-col items-center lg:items-stretch gap-0.5 bg-white border-r border-line pt-3.5 pb-3 lg:px-3 overflow-y-auto no-scrollbar print:hidden"
    >
      <a
        href={pathFor('quick_add')}
        onClick={linkClick(() => setActiveTab('quick_add'))}
        aria-label="MeDSor ana sayfa"
        className="shrink-0 flex items-center gap-2.5 mb-3 lg:mb-5 lg:px-2 lg:h-10"
      >
        <span className="w-[34px] h-[34px] rounded-[10px] bg-accent text-white flex items-center justify-center shrink-0">
          <Plus className="w-[18px] h-[18px]" strokeWidth={2.8} />
        </span>
        <span className="ms-rail-word hidden lg:inline font-display font-bold text-[19px] tracking-[-0.02em] text-ink">
          Me<span className="text-accent">DS</span>or
        </span>
      </a>
      {RAIL.map((r) => item(r.id, r.label, r.icon))}
      <span className="flex-1 min-h-3" aria-hidden="true" />
      {isAdmin && item('manage', 'Yönetim', ShieldCheck)}
      <button
        type="button"
        onClick={() => setCollapsed((c) => !c)}
        aria-label={collapsed ? 'Menüyü genişlet' : 'Menüyü daralt'}
        title={collapsed ? 'Menüyü genişlet' : 'Menüyü daralt'}
        className="ms-rail-item ms-rail-toggle hidden lg:flex w-full h-10 px-3 mt-1 rounded-xl items-center gap-3 text-[14px] text-ink-3 hover:text-ink hover:bg-canvas cursor-pointer"
      >
        {collapsed ? <PanelLeftOpen className="w-[18px] h-[18px] shrink-0" /> : <PanelLeftClose className="w-[18px] h-[18px] shrink-0" />}
        <span className="ms-rail-label">Daralt</span>
      </button>
    </nav>
  );
};
