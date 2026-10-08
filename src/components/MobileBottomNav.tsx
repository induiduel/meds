import React, { useEffect, useState } from 'react';
import {
  SquarePen,
  GraduationCap,
  Archive,
  ListChecks,
  LayoutGrid,
  Library,
  Trophy,
  BookOpen,
  BookOpenText,
  Mic,
  BookCopy,
  FileDown,
  ShieldCheck,
  ChevronRight,
  X,
  Layers,
  Target,
  Compass,
} from 'lucide-react';
import type { AppTab } from './Header';
import { pathFor, linkClick } from '../router';

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

const TABS: { id: AppTab; label: string; icon: React.ElementType }[] = [
  { id: 'quick_add', label: 'Ekle', icon: SquarePen },
  { id: 'learn', label: 'Öğren', icon: GraduationCap },
  { id: 'flashcards', label: 'Kartlar', icon: Layers },
  { id: 'past_exams', label: 'Çıkmış', icon: Archive },
];

// "Daha" sayfası: kenar menüsüyle aynı kategoriler; renk yalnız seçili sayfada
const MORE_GROUPS: { label: string; items: { id: AppTab; label: string; hint: string; icon: React.ElementType }[] }[] = [
  {
    label: 'Sorular',
    items: [
      { id: 'ornek_sorular', label: 'Örnek sorular', hint: 'Kazanım temelli sorular', icon: Target },
      { id: 'questions', label: 'Soru havuzu', hint: 'Kurul sorularını birlikte kur', icon: Library },
      { id: 'study', label: 'Çalış', hint: 'Soru çöz, kendini test et', icon: ListChecks },
      { id: 'matrix', label: 'Soru haritası', hint: '1–100 doluluk', icon: LayoutGrid },
    ],
  },
  {
    label: 'Öğrenme',
    items: [
      { id: 'kazanimlar', label: 'Kazanımlar', hint: 'Müfredat ve kazanım haritası', icon: Compass },
      { id: 'summaries', label: 'Ders özetleri', hint: 'Spot bilgiler', icon: BookOpen },
      { id: 'glossary', label: 'Sözlük', hint: 'Hastalık ve ilaç ansiklopedisi', icon: BookOpenText },
    ],
  },
  {
    label: 'Topluluk',
    items: [{ id: 'leaderboard', label: 'Sıralama', hint: 'En çok katkı verenler', icon: Trophy }],
  },
];

/** App-style tab bar for phones and tablets (below lg), with a "Daha" sheet for the remaining pages. */
export const MobileBottomNav: React.FC<MobileBottomNavProps> = ({ activeTab, setActiveTab, isAdmin, onOpenPdfModal }) => {
  const [sheetOpen, setSheetOpen] = useState(false);
  const moreActive = !TABS.some((t) => t.id === activeTab) && activeTab !== 'practice';

  useEffect(() => {
    if (!sheetOpen) return;
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && setSheetOpen(false);
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    document.addEventListener('keydown', onKey);
    return () => {
      document.body.style.overflow = prev;
      document.removeEventListener('keydown', onKey);
    };
  }, [sheetOpen]);

  const go = (id: AppTab) => {
    setSheetOpen(false);
    setActiveTab(id);
  };

  const tabCls = (on: boolean) =>
    `flex flex-col items-center justify-center gap-1 min-h-12 text-[11px] md:text-[12px] leading-none cursor-pointer ${
      on ? 'text-accent font-semibold' : 'text-ink-3'
    }`;

  return (
    <>
      <nav
        aria-label="Alt menü"
        className="ms-hide-on-kb md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur border-t border-line pt-1.5 pb-[max(env(safe-area-inset-bottom),8px)] print:hidden"
      >
        <div className="max-w-[720px] mx-auto grid grid-cols-5 px-1">
          {TABS.map(({ id, label, icon: Icon }) => {
            const on = activeTab === id;
            return (
              <a key={id} href={pathFor(id)} onClick={linkClick(() => go(id))} aria-current={on ? 'page' : undefined} className={tabCls(on)}>
                <span className={`h-7 w-12 rounded-full flex items-center justify-center transition-colors ${on ? 'bg-accent-soft' : ''}`}>
                  <Icon className="w-[21px] h-[21px]" strokeWidth={on ? 2.3 : 2} />
                </span>
                {label}
              </a>
            );
          })}
          <button type="button" onClick={() => setSheetOpen(true)} aria-haspopup="dialog" aria-expanded={sheetOpen} className={tabCls(moreActive)}>
            <span className={`h-7 w-12 rounded-full flex items-center justify-center transition-colors ${moreActive ? 'bg-accent-soft' : ''}`}>
              <LayoutGrid className="w-[21px] h-[21px]" strokeWidth={moreActive ? 2.3 : 2} />
            </span>
            Daha
          </button>
        </div>
      </nav>

      {sheetOpen && (
        <div className="md:hidden fixed inset-0 z-50 print:hidden" role="dialog" aria-modal="true" aria-label="Diğer sayfalar">
          <button type="button" aria-label="Kapat" onClick={() => setSheetOpen(false)} className="ms-fade-in absolute inset-0 bg-[rgba(14,26,38,0.4)] cursor-default" />
          <div className="ms-sheet-up absolute left-0 right-0 bottom-0 max-h-[85dvh] overflow-y-auto overscroll-contain bg-white rounded-t-2xl shadow-lg px-4 pt-2 pb-[max(env(safe-area-inset-bottom),20px)]">
            <div className="max-w-[640px] mx-auto flex flex-col gap-3">
              <span className="self-center w-10 h-[5px] rounded-full bg-line-2" aria-hidden="true" />
              <div className="flex items-center">
                <h2 className="m-0 flex-1 font-display text-[19px] font-semibold tracking-[-0.02em]">Daha fazla</h2>
                <button type="button" onClick={() => setSheetOpen(false)} aria-label="Kapat" className="w-10 h-10 -mr-2 rounded-full flex items-center justify-center text-ink-2 cursor-pointer">
                  <X className="w-5 h-5" />
                </button>
              </div>
              {MORE_GROUPS.map((g) => (
                <section key={g.label} className="flex flex-col gap-0.5">
                  <h3 className="m-0 px-1 pb-1 text-[12px] font-semibold text-ink-3">{g.label}</h3>
                  <div className="flex flex-col bg-canvas rounded-2xl overflow-hidden">
                    {g.items.map(({ id, label, hint, icon: Icon }, i) => {
                      const on = activeTab === id;
                      return (
                        <a
                          key={id}
                          href={pathFor(id)}
                          onClick={linkClick(() => go(id))}
                          aria-current={on ? 'page' : undefined}
                          className={`min-h-[52px] px-3.5 flex items-center gap-3 ${i > 0 ? 'border-t border-line-soft' : ''} ${on ? 'bg-accent-soft' : ''}`}
                        >
                          <Icon className={`w-5 h-5 shrink-0 ${on ? 'text-accent' : 'text-ink-2'}`} />
                          <span className="flex-1 min-w-0">
                            <span className={`block text-[15px] font-semibold leading-tight ${on ? 'text-accent' : 'text-ink'}`}>{label}</span>
                            <span className="block text-[12.5px] text-ink-3 truncate">{hint}</span>
                          </span>
                          <ChevronRight className="w-4 h-4 text-ink-3 shrink-0" />
                        </a>
                      );
                    })}
                  </div>
                </section>
              ))}
              <div className="flex flex-col bg-canvas rounded-2xl overflow-hidden">
                <button
                  type="button"
                  onClick={() => {
                    setSheetOpen(false);
                    onOpenPdfModal();
                  }}
                  className="min-h-[52px] px-4 flex items-center gap-3 text-[15px] text-ink text-left cursor-pointer"
                >
                  <FileDown className="w-5 h-5 text-ink-2" />
                  PDF indir
                </button>
                {isAdmin && (
                  <a
                    href={pathFor('admin')}
                    onClick={linkClick(() => go('admin'))}
                    className="min-h-[52px] px-4 flex items-center gap-3 text-[15px] text-ink border-t border-line"
                  >
                    <ShieldCheck className="w-5 h-5 text-ink-2" />
                    Yönetim
                  </a>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
