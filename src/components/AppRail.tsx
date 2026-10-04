import React from 'react';
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
} from 'lucide-react';
import type { AppTab } from './Header';
import { pathFor, linkClick } from '../router';

/** v3 rail: every page one tap away on tablet and desktop. Phones use MobileBottomNav. */
export const RAIL: { id: AppTab; label: string; icon: React.ElementType }[] = [
  { id: 'quick_add', label: 'Ekle', icon: SquarePen },
  { id: 'learn', label: 'Öğren', icon: GraduationCap },
  { id: 'glossary', label: 'Sözlük', icon: BookOpenText },
  { id: 'flashcards', label: 'Kartlar', icon: Layers },
  { id: 'past_exams', label: 'Çıkmış', icon: Archive },
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

export const AppRail: React.FC<AppRailProps> = ({ activeTab, setActiveTab, isAdmin }) => {
  const item = (id: AppTab, label: string, Icon: React.ElementType) => {
    const on = activeTab === id;
    return (
      <a
        key={id}
        href={pathFor(id)}
        onClick={linkClick(() => setActiveTab(id))}
        aria-current={on ? 'page' : undefined}
        title={label}
        className={`w-[62px] shrink-0 py-[7px] rounded-[12px] flex flex-col items-center gap-[3px] text-[11px] leading-none transition-colors ${
          on ? 'bg-accent-soft text-accent font-semibold' : 'text-ink-3 hover:text-ink hover:bg-canvas font-medium'
        }`}
      >
        <Icon className="w-[21px] h-[21px]" strokeWidth={on ? 2.3 : 2} />
        {label}
      </a>
    );
  };

  return (
    <nav
      aria-label="Ana menü"
      className="hidden md:flex lg:hidden fixed left-0 top-0 bottom-0 z-40 w-[76px] flex-col items-center gap-0.5 bg-white border-r border-line pt-3.5 pb-3 overflow-y-auto no-scrollbar print:hidden"
    >
      <a
        href={pathFor('quick_add')}
        onClick={linkClick(() => setActiveTab('quick_add'))}
        aria-label="MedSoru ana sayfa"
        className="w-[34px] h-[34px] shrink-0 rounded-[10px] bg-accent text-white flex items-center justify-center mb-3"
      >
        <Plus className="w-[18px] h-[18px]" strokeWidth={2.8} />
      </a>
      {RAIL.map((r) => item(r.id, r.label, r.icon))}
      <span className="flex-1 min-h-3" aria-hidden="true" />
      {isAdmin && item('manage', 'Yönetim', ShieldCheck)}
    </nav>
  );
};
