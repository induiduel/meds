import React from 'react';
import { Home, List, Plus, CircleCheck, BookMarked } from 'lucide-react';
import type { AppTab } from './Header';

interface MobileBottomNavProps {
  activeTab: AppTab;
  setActiveTab: (tab: AppTab) => void;
  questionsCount: number;
  isAdmin: boolean;
  onOpenContributeModal: () => void;
  onOpenPdfModal: () => void;
  onOpenAdminPanel: () => void;
  onUploadToDrive: () => void;
}

export const MobileBottomNav: React.FC<MobileBottomNavProps> = ({ activeTab, setActiveTab, onOpenContributeModal }) => {
  const Item: React.FC<{ id: AppTab; label: string; icon: React.ElementType }> = ({ id, label, icon: Icon }) => {
    const active = activeTab === id;
    return (
      <button
        type="button"
        onClick={() => setActiveTab(id)}
        aria-current={active ? 'page' : undefined}
        className={`flex flex-col items-center justify-center gap-0.5 min-h-12 text-[11px] cursor-pointer ${
          active ? 'text-accent font-semibold' : 'text-ink-2'
        }`}
      >
        <Icon className="w-[22px] h-[22px]" strokeWidth={2} />
        {label}
      </button>
    );
  };

  return (
    <nav
      aria-label="Alt menü"
      className="sm:hidden fixed bottom-0 left-0 right-0 z-40 bg-white border-t border-line px-2 pt-2 pb-[max(env(safe-area-inset-bottom),14px)] grid grid-cols-5 items-end print:hidden"
    >
      <Item id="quick_add" label="Ana sayfa" icon={Home} />
      <Item id="questions" label="Havuz" icon={List} />
      <button type="button" onClick={onOpenContributeModal} aria-label="Soru ekle" className="flex justify-center cursor-pointer">
        <span className="w-[52px] h-[52px] rounded-2xl bg-accent flex items-center justify-center">
          <Plus className="w-6 h-6 text-white" strokeWidth={2.4} />
        </span>
      </button>
      <Item id="practice" label="Test" icon={CircleCheck} />
      <Item id="notes" label="Notlar" icon={BookMarked} />
    </nav>
  );
};
