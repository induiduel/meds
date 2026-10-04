import React from 'react';
import { Search, Check, CircleDashed, UserRound } from 'lucide-react';

interface MetricsBarProps {
  totalTarget: number;
  totalGathered: number;
  completedCount: number;
  gatheringCount: number;
  emptyCount: number;
  selectedDiscipline: string;
  onSelectDiscipline: (discipline: string) => void;
  selectedStatus: string;
  onSelectStatus: (status: string) => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
  onGenerateSlots: () => void;
  isGeneratingSlots: boolean;
  isAdmin?: boolean;
  myQuestionsCount?: number;
  filterMyQuestionsOnly?: boolean;
  onToggleMyQuestionsOnly?: () => void;
}

const DISCIPLINES = [
  'Tümü',
  'Patoloji',
  'Farmakoloji',
  'Tıbbi Mikrobiyoloji',
  'Dahiliye',
  'Göğüs Hastalıkları',
  'Kardiyoloji',
  'Pediatri',
  'Anatomi',
  'Fizyoloji',
  'Tıbbi Biyokimya',
];

export const MetricsBar: React.FC<MetricsBarProps> = ({
  totalTarget,
  totalGathered,
  completedCount,
  gatheringCount,
  emptyCount,
  selectedDiscipline,
  onSelectDiscipline,
  selectedStatus,
  onSelectStatus,
  searchQuery,
  onSearchChange,
  onGenerateSlots,
  isGeneratingSlots,
  isAdmin = false,
  myQuestionsCount,
  filterMyQuestionsOnly = false,
  onToggleMyQuestionsOnly,
}) => {
  const pct = (n: number) => `${Math.min(100, (n / Math.max(totalTarget, 1)) * 100)}%`;
  const segBtn = (active: boolean) =>
    `h-8 px-3 rounded-lg text-[13px] cursor-pointer whitespace-nowrap ${
      active ? 'bg-white font-semibold shadow-xs text-ink' : 'text-ink-2'
    }`;

  return (
    <div className="bg-white rounded-2xl border border-line overflow-hidden">
      {/* Pool status strip */}
      <div className="px-4 sm:px-6 py-3 sm:py-5 flex flex-col gap-2.5 sm:gap-3 border-b border-line">
        <div className="flex flex-wrap items-baseline gap-x-4 sm:gap-x-6 gap-y-1.5">
          <span className="flex items-baseline gap-2">
            <span className="font-display text-[26px] sm:text-[32px] font-bold leading-none tracking-[-0.03em]">{completedCount}</span>
            <span className="text-[14px] text-ink-2">/ {totalTarget} soru kuruldu</span>
          </span>
          <span className="flex flex-wrap gap-x-3 sm:gap-x-4 gap-y-1 text-[12px] sm:text-[13px] text-ink-2">
            <span className="inline-flex items-center gap-1.5">
              <Check className="w-3.5 h-3.5 text-ok" strokeWidth={3} />
              Doğrulandı <span className="font-mono text-ink">{completedCount}</span>
            </span>
            <span className="inline-flex items-center gap-1.5">
              <CircleDashed className="w-3.5 h-3.5 text-warn" />
              Taslak <span className="font-mono text-ink">{gatheringCount}</span>
            </span>
            <span className="inline-flex items-center gap-1.5">
              Boş yuva <span className="font-mono text-ink">{emptyCount}</span>
            </span>
          </span>
          {isAdmin && emptyCount > 0 && (
            <button
              type="button"
              onClick={onGenerateSlots}
              disabled={isGeneratingSlots}
              className="ml-auto h-9 px-3.5 rounded-[10px] border border-line-2 bg-white text-[13px] font-semibold cursor-pointer disabled:opacity-50"
              title="Yönetici: soru yuvalarını aç"
            >
              {isGeneratingSlots ? 'Oluşturuluyor…' : `1–${totalTarget} yuvalarını aç`}
            </button>
          )}
        </div>
        <div
          role="img"
          aria-label={`${completedCount} doğrulandı, ${gatheringCount} taslak`}
          className="flex h-2 rounded-full overflow-hidden gap-[3px] bg-line-soft"
        >
          {completedCount > 0 && <span className="bg-ok-bright" style={{ width: pct(completedCount) }} />}
          {gatheringCount > 0 && <span className="bg-amber-600" style={{ width: pct(gatheringCount) }} />}
        </div>
      </div>

      {/* Search & filters */}
      <div className="px-4 sm:px-6 py-3 sm:py-4 flex flex-col gap-2.5 sm:gap-3.5">
        <div className="flex flex-col md:flex-row md:items-center gap-2.5 sm:gap-3">
          <label className="flex items-center gap-2 h-10 sm:h-11 px-3 border border-line-2 rounded-[10px] bg-field flex-1 md:max-w-[440px] focus-within:border-accent">
            <Search className="w-4 h-4 text-ink-2 shrink-0" />
            <span className="sr-only">Soru havuzunda ara</span>
            <input
              type="search"
              placeholder="Soru no, hastalık, ilaç ya da anahtar kelime"
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
              className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[15px] placeholder:text-slate-600"
            />
          </label>

          <div className="flex items-center gap-2 md:ml-auto overflow-x-auto no-scrollbar">
            <div role="group" aria-label="Durum" className="flex gap-1 bg-canvas rounded-[10px] p-[3px]">
              <button type="button" aria-pressed={selectedStatus === 'Tümü'} onClick={() => onSelectStatus('Tümü')} className={segBtn(selectedStatus === 'Tümü')}>
                Tümü
              </button>
              <button type="button" aria-pressed={selectedStatus === 'completed'} onClick={() => onSelectStatus('completed')} className={segBtn(selectedStatus === 'completed')}>
                Doğrulanan
              </button>
              <button type="button" aria-pressed={selectedStatus === 'gathering'} onClick={() => onSelectStatus('gathering')} className={segBtn(selectedStatus === 'gathering')}>
                Taslak
              </button>
            </div>

            {myQuestionsCount !== undefined && onToggleMyQuestionsOnly && (
              <button
                type="button"
                onClick={onToggleMyQuestionsOnly}
                aria-pressed={filterMyQuestionsOnly}
                className={`shrink-0 h-[38px] px-3 rounded-[10px] text-[13px] inline-flex items-center gap-1.5 cursor-pointer ${
                  filterMyQuestionsOnly ? 'border-[1.5px] border-accent bg-accent-soft text-accent font-semibold' : 'border border-line bg-white text-ink'
                }`}
              >
                <UserRound className="w-3.5 h-3.5" />
                Sorularım <span className="font-mono">{myQuestionsCount}</span>
              </button>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2 overflow-x-auto no-scrollbar -mx-4 px-4 sm:mx-0 sm:px-0">
          {DISCIPLINES.map((d) => {
            const on = selectedDiscipline === d;
            return (
              <button
                key={d}
                type="button"
                aria-pressed={on}
                onClick={() => onSelectDiscipline(d)}
                className={`shrink-0 h-8 sm:h-9 px-3 sm:px-3.5 rounded-full text-[13px] sm:text-[14px] cursor-pointer whitespace-nowrap ${
                  on ? 'bg-accent-soft text-accent font-semibold ring-1 ring-inset ring-accent/40' : 'bg-white border border-line text-ink hover:border-line-2'
                }`}
              >
                {d}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
