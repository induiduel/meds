import React from 'react';
import { Search, Check, CircleDashed, UserRound, X, CircleDot } from 'lucide-react';
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
};
