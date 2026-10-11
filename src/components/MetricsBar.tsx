import React from 'react';
import { Search, Check, CircleDashed, UserRound, X, CircleDot } from 'lucide-react';
import { useUiVersion } from '../utils/uiVersion';
import { Segmented } from './ui/kit';

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
  const { isV7 } = useUiVersion();
  const pct = (n: number) => `${Math.min(100, (n / Math.max(totalTarget, 1)) * 100)}%`;
  const segBtn = (active: boolean) =>
    `h-8 px-3 rounded-lg text-sm cursor-pointer whitespace-nowrap ${
      active ? 'bg-white font-semibold shadow-xs text-ink' : 'text-ink-2'
    }`;

  if (isV7) {
    // v8: özet kartı (halka + üç durum) ve yapışkan kontrol yuvası (arama, durum, sorularım, branş)
    const done = Math.min(1, completedCount / Math.max(totalTarget, 1));
    const draft = Math.min(1 - done, gatheringCount / Math.max(totalTarget, 1));
    const C = 2 * Math.PI * 26;
    return (
      <>
        <section className="pl-sum" aria-label="Havuz durumu">
          <svg className="pl-ring" viewBox="0 0 64 64" aria-hidden="true">
            <circle cx="32" cy="32" r="26" className="pl-ring-bg" />
            <circle cx="32" cy="32" r="26" className="pl-ring-draft" strokeDasharray={`${(done + draft) * C} ${C}`} />
            <circle cx="32" cy="32" r="26" className="pl-ring-done" strokeDasharray={`${done * C} ${C}`} />
          </svg>
          <div className="pl-sum-main">
            <p className="pl-sum-big"><b className="hk-num">{completedCount}</b> <span>/ {totalTarget} soru kuruldu</span></p>
            <ul className="pl-sum-legend">
              <li><i className="is-done" />Doğrulandı <b className="hk-num">{completedCount}</b></li>
              <li><i className="is-draft" />Taslak <b className="hk-num">{gatheringCount}</b></li>
              <li><i />Boş yuva <b className="hk-num">{emptyCount}</b></li>
            </ul>
          </div>
          {isAdmin && emptyCount > 0 && (
            <button type="button" onClick={onGenerateSlots} disabled={isGeneratingSlots} className={`ui-btn is-tonal is-sm ${isGeneratingSlots ? 'is-loading' : ''}`} title="Yönetici: soru yuvalarını aç">
              1–{totalTarget} yuvalarını aç
            </button>
          )}
        </section>

        <div className="cx-dock pl-dock">
          <div className="pl-dock-row">
            <label className="cx-search pl-search">
              <Search aria-hidden />
              <span className="sr-only">Soru havuzunda ara</span>
              <input type="search" placeholder="Soru no, hastalık, ilaç ya da anahtar kelime" value={searchQuery} onChange={(e) => onSearchChange(e.target.value)} />
              {searchQuery && (
                <button type="button" className="cx-search-x" aria-label="Aramayı temizle" onClick={() => onSearchChange('')}><X /></button>
              )}
            </label>
            <Segmented<string>
              className="pl-status"
              label="Durum"
              value={selectedStatus}
              onChange={onSelectStatus}
              options={[
                { value: 'Tümü', label: 'Tümü' },
                { value: 'completed', label: <span className="inline-flex items-center gap-1"><Check className="w-3.5 h-3.5" strokeWidth={3} />Doğrulanan</span> },
                { value: 'gathering', label: <span className="inline-flex items-center gap-1"><CircleDashed className="w-3.5 h-3.5" />Taslak</span> },
              ]}
            />
            {myQuestionsCount !== undefined && onToggleMyQuestionsOnly && (
              <button type="button" onClick={onToggleMyQuestionsOnly} aria-pressed={filterMyQuestionsOnly} className="pl-mine">
                {filterMyQuestionsOnly ? <CircleDot /> : <UserRound />}
                Sorularım <b className="hk-num">{myQuestionsCount}</b>
              </button>
            )}
          </div>
          <nav className="cx-tabs" aria-label="Branş">
            {DISCIPLINES.map((d) => (
              <button key={d} type="button" aria-pressed={selectedDiscipline === d} onClick={() => onSelectDiscipline(d)} className={`cx-tab ${selectedDiscipline === d ? 'is-on' : ''}`}>
                {d}
              </button>
            ))}
          </nav>
        </div>
      </>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-line overflow-hidden">
      {/* Pool status strip */}
      <div className="px-4 sm:px-6 py-3 sm:py-5 flex flex-col gap-2.5 sm:gap-3 border-b border-line">
        <div className="flex flex-wrap items-baseline gap-x-4 sm:gap-x-6 gap-y-1.5">
          <span className="flex items-baseline gap-2">
            <span className="font-display text-3xl sm:text-4xl font-bold leading-none tracking-[-0.03em]">{completedCount}</span>
            <span className="text-base text-ink-2">/ {totalTarget} soru kuruldu</span>
          </span>
          <span className="flex flex-wrap gap-x-3 sm:gap-x-4 gap-y-1 text-xs sm:text-sm text-ink-2">
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
              className="ml-auto h-9 px-3.5 rounded-[10px] border border-line-2 bg-white text-sm font-semibold cursor-pointer disabled:opacity-50"
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
          {gatheringCount > 0 && <span className="bg-warn" style={{ width: pct(gatheringCount) }} />}
        </div>
      </div>

      {/* Search & filters */}
      <div className="px-4 sm:px-6 py-3 sm:py-4 flex flex-col gap-2.5 sm:gap-3.5">
        <div className="flex flex-col md:flex-row md:items-center gap-2.5 sm:gap-3">
          <label className="cx-search flex-1 md:max-w-[440px]">
            <Search aria-hidden />
            <span className="sr-only">Soru havuzunda ara</span>
            <input
              type="search"
              placeholder="Soru no, hastalık, ilaç ya da anahtar kelime"
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
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
                className={`shrink-0 h-[38px] px-3 rounded-[10px] text-sm inline-flex items-center gap-1.5 cursor-pointer ${
                  filterMyQuestionsOnly ? 'border-[1.5px] border-accent bg-accent-soft text-accent font-semibold' : 'border border-line bg-white text-ink'
                }`}
              >
                <UserRound className="w-3.5 h-3.5" />
                Sorularım <span className="font-mono">{myQuestionsCount}</span>
              </button>
            )}
          </div>
        </div>

        <nav className="cx-tabs" aria-label="Branş">
          {DISCIPLINES.map((d) => (
            <button key={d} type="button" aria-pressed={selectedDiscipline === d} onClick={() => onSelectDiscipline(d)} className={`cx-tab ${selectedDiscipline === d ? 'is-on' : ''}`}>
              {d}
            </button>
          ))}
        </nav>
      </div>
    </div>
  );
};
