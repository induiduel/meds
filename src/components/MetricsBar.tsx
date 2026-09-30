import React from 'react';
import { 
  Search, 
  Filter, 
  CheckCircle, 
  Clock, 
  Sparkles, 
  AlertCircle,
  Hash,
  Database
} from 'lucide-react';

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
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs space-y-4">
      {/* Top Stat Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-slate-50 border border-slate-200/80 rounded-lg p-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-500">Hedef Kurul Sorusu</span>
            <Hash className="w-4 h-4 text-slate-400" />
          </div>
          <div className="mt-1 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-slate-900">{totalTarget}</span>
            <span className="text-xs text-slate-500">soruluk sınav</span>
          </div>
        </div>

        <div className="bg-emerald-50/80 border border-emerald-200/80 rounded-lg p-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-emerald-700">AI Rekonstrükte (%90+)</span>
            <Sparkles className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="mt-1 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-emerald-800">{completedCount}</span>
            <span className="text-xs text-emerald-600 font-medium">soru hazır</span>
          </div>
        </div>

        <div className="bg-amber-50/80 border border-amber-200/80 rounded-lg p-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-amber-700">Taslak & Şık Bekleyen</span>
            <Clock className="w-4 h-4 text-amber-600" />
          </div>
          <div className="mt-1 flex items-baseline gap-2">
            <span className="text-2xl font-bold text-amber-800">{gatheringCount}</span>
            <span className="text-xs text-amber-600 font-medium">aktif toplanıyor</span>
          </div>
        </div>

        <div className="bg-sky-50/80 border border-sky-200/80 rounded-lg p-3 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-sky-700">1-{totalTarget} Yuva Şablonu</span>
            <Database className="w-4 h-4 text-sky-600" />
          </div>
          <div className="mt-1 flex items-center justify-between gap-1">
            <span className="text-sm font-semibold text-sky-900">
              {emptyCount > 0 ? `${emptyCount} boş yuva` : 'Tüm yuvalar hazır'}
            </span>
            {isAdmin ? (
              <button
                onClick={onGenerateSlots}
                disabled={isGeneratingSlots}
                className="text-xs bg-sky-600 hover:bg-sky-700 text-white font-medium px-2 py-1 rounded transition-colors disabled:opacity-50 cursor-pointer"
                title="Yönetici: 1-100 soru yuvalarını aç"
              >
                {isGeneratingSlots ? 'Oluşturuluyor...' : `1-${totalTarget} Aç`}
              </button>
            ) : (
              <span className="text-[11px] text-slate-500 font-medium">
                {emptyCount > 0 ? `${emptyCount} Boş` : 'Dolu'}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pt-2 border-t border-slate-100">
        {/* Search Input */}
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Soru no, hastalık, ilaç, etken veya anahtar kelime ara..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full bg-slate-50 border border-slate-200 rounded-lg pl-9 pr-4 py-2 text-sm text-slate-800 placeholder:text-slate-400 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-teal-500/20 focus:border-teal-500 transition-all"
          />
        </div>

        {/* My Questions Only Toggle (if logged in / has questions) */}
        {myQuestionsCount !== undefined && onToggleMyQuestionsOnly && (
          <button
            onClick={onToggleMyQuestionsOnly}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer ${
              filterMyQuestionsOnly
                ? 'bg-amber-400 text-slate-950 shadow-xs'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
            }`}
            title="Sadece benim eklediğim veya katkıda bulunduğum soruları listele"
          >
            <span>👤 Sorularım ({myQuestionsCount})</span>
          </button>
        )}

        {/* Status Filter */}
        <div className="flex items-center gap-2">
          <span className="text-xs font-medium text-slate-500 flex items-center gap-1">
            <Filter className="w-3.5 h-3.5" /> Durum:
          </span>
          <div className="inline-flex rounded-lg border border-slate-200 bg-slate-50 p-0.5 text-xs">
            <button
              onClick={() => onSelectStatus('Tümü')}
              className={`px-2.5 py-1 rounded-md font-medium transition-colors cursor-pointer ${
                selectedStatus === 'Tümü'
                  ? 'bg-white text-slate-900 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Tümü
            </button>
            <button
              onClick={() => onSelectStatus('completed')}
              className={`px-2.5 py-1 rounded-md font-medium transition-colors cursor-pointer ${
                selectedStatus === 'completed'
                  ? 'bg-emerald-600 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Tamamlanan (%100)
            </button>
            <button
              onClick={() => onSelectStatus('gathering')}
              className={`px-2.5 py-1 rounded-md font-medium transition-colors cursor-pointer ${
                selectedStatus === 'gathering'
                  ? 'bg-amber-500 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Taslak / Katkı Bekleyen
            </button>
          </div>
        </div>
      </div>

      {/* Discipline Chips Filter */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs no-scrollbar">
        <span className="text-slate-400 shrink-0 font-medium mr-1">Dersler:</span>
        {DISCIPLINES.map((d) => (
          <button
            key={d}
            onClick={() => onSelectDiscipline(d)}
            className={`px-2.5 py-1 rounded-md transition-colors font-medium whitespace-nowrap cursor-pointer ${
              selectedDiscipline === d
                ? 'bg-teal-700 text-white font-semibold shadow-xs'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            {d}
          </button>
        ))}
      </div>
    </div>
  );
};
