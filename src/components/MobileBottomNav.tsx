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
  { id: 'quick_add', label: 'Soru ekle', icon: SquarePen },
  { id: 'learn', label: 'Öğren', icon: GraduationCap },
  { id: 'past_exams', label: 'Çıkmış', icon: Archive },
  { id: 'study', label: 'Çalış', icon: ListChecks },
];

const MORE: { id: AppTab; label: string; hint: string; icon: React.ElementType; tint: string }[] = [
  { id: 'questions', label: 'Soru havuzu', hint: 'Kurul sorularını birlikte kur', icon: Library, tint: '#1E4FD8' },
  { id: 'leaderboard', label: 'Sıralama', hint: 'En çok katkı verenler', icon: Trophy, tint: '#B7791F' },
  { id: 'summaries', label: 'Ders özetleri', hint: 'Spot bilgiler', icon: BookOpen, tint: '#6D28D9' },
  { id: 'notes', label: 'Ders notları', hint: 'Slaytlar ve PDF notlar', icon: BookOpenText, tint: '#0F7A5F' },
  { id: 'transcripts', label: 'Ses kayıtları', hint: 'Amfi transkriptleri', icon: Mic, tint: '#C2410C' },
  { id: 'matrix', label: 'Soru haritası', hint: '1–100 doluluk', icon: LayoutGrid, tint: '#0E1A26' },
  { id: 'booklet', label: 'A4 kitapçık', hint: 'Yazdırılabilir görünüm', icon: BookCopy, tint: '#4A5868' },
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
        className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur border-t border-line pt-1.5 pb-[max(env(safe-area-inset-bottom),8px)] print:hidden"
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
        <div className="lg:hidden fixed inset-0 z-50 print:hidden" role="dialog" aria-modal="true" aria-label="Diğer sayfalar">
          <button type="button" aria-label="Kapat" onClick={() => setSheetOpen(false)} className="absolute inset-0 bg-[rgba(14,26,38,0.4)] cursor-default" />
          <div className="absolute left-0 right-0 bottom-0 max-h-[85dvh] overflow-y-auto bg-white rounded-t-[24px] shadow-[0_-10px_40px_rgba(14,26,38,0.18)] px-4 pt-2 pb-[max(env(safe-area-inset-bottom),20px)]">
            <div className="max-w-[640px] mx-auto flex flex-col gap-3">
              <span className="self-center w-10 h-[5px] rounded-full bg-line-2" aria-hidden="true" />
              <div className="flex items-center">
                <h2 className="m-0 flex-1 font-display text-[22px] font-bold tracking-[-0.02em]">Daha fazla</h2>
                <button type="button" onClick={() => setSheetOpen(false)} aria-label="Kapat" className="w-10 h-10 -mr-2 rounded-full flex items-center justify-center text-ink-2 cursor-pointer">
                  <X className="w-5 h-5" />
                </button>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {MORE.map(({ id, label, hint, icon: Icon, tint }) => {
                  const on = activeTab === id;
                  return (
                    <a
                      key={id}
                      href={pathFor(id)}
                      onClick={linkClick(() => go(id))}
                      aria-current={on ? 'page' : undefined}
                      className={`min-h-[60px] px-3 rounded-2xl flex items-center gap-3 ${on ? 'bg-accent-soft' : 'bg-canvas'}`}
                    >
                      <span className="w-10 h-10 rounded-xl bg-white flex items-center justify-center shrink-0" style={{ color: tint }}>
                        <Icon className="w-5 h-5" />
                      </span>
                      <span className="flex-1 min-w-0">
                        <span className={`block text-[15px] font-semibold ${on ? 'text-accent' : 'text-ink'}`}>{label}</span>
                        <span className="block text-[13px] text-ink-3 truncate">{hint}</span>
                      </span>
                      <ChevronRight className="w-4 h-4 text-ink-3 shrink-0" />
                    </a>
                  );
                })}
              </div>
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
