import React from 'react';
import { House, Library, Plus, ListChecks, BookOpenText } from 'lucide-react';
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
        className={`flex flex-col items-center justify-center gap-1 min-h-12 text-[11px] leading-none cursor-pointer ${
          active ? 'text-accent font-semibold' : 'text-ink-2'
        }`}
      >
        <span className={`h-7 w-12 rounded-full flex items-center justify-center transition-colors ${active ? 'bg-accent-soft' : ''}`}>
          <Icon className="w-5 h-5" strokeWidth={active ? 2.3 : 2} />
        </span>
        {label}
      </button>
    );
  };

  return (
    <nav
      aria-label="Alt menü"
      className="sm:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur border-t border-line px-1 pt-1.5 pb-[max(env(safe-area-inset-bottom),8px)] grid grid-cols-5 items-end print:hidden"
    >
      <Item id="quick_add" label="Ana sayfa" icon={House} />
      <Item id="questions" label="Havuz" icon={Library} />
      <button type="button" onClick={onOpenContributeModal} aria-label="Soru ekle" className="flex justify-center items-center min-h-12 cursor-pointer">
        <span className="w-12 h-12 rounded-2xl bg-accent flex items-center justify-center shadow-[0_6px_16px_rgba(30,79,216,0.32)]">
          <Plus className="w-6 h-6 text-white" strokeWidth={2.4} />
        </span>
      </button>
      <Item id="study" label="Çalış" icon={ListChecks} />
      <Item id="notes" label="Notlar" icon={BookOpenText} />
    </nav>
  );
};
