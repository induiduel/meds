import React, { useState, useEffect, useMemo } from 'react';
import { 
  BookOpen, 
  Search, 
  Filter, 
  FileText, 
  ExternalLink, 
  Copy, 
  Check, 
  Clock, 
  Sparkles, 
  AlertTriangle, 
  ChevronRight, 
  X, 
  Printer, 
  Download,
  GraduationCap,
  BookMarked,
  Layers
} from 'lucide-react';
import summariesMetaData from '../data/summaries_meta.json';
import { SummaryArtifactReader } from './SummaryArtifactReader';

export interface SummaryMeta {
  id: string;
  kurul: number;
  committeeId: string;
  discipline: string;
  title: string;
  fileName: string;
  keyPoints: string[];
  charCount: number;
  readingTimeMinutes: number;
}

export interface SummaryDetail extends SummaryMeta {
  content?: string;
}

interface LectureSummariesViewProps {
  onOpenPdfModal?: () => void;
}

const KURUL_LABELS: Record<number, string> = {
  1: 'Kurul 1: Ürogenital & Obstetrik',
  2: 'Kurul 2: Nöropsikiyatri',
  3: 'Kurul 3: Gastrointestinal Sistem',
  4: 'Kurul 4: Dolaşım, Solunum & Tümör',
  5: 'Kurul 5: Ortopedi, Travma & Hematopoetik',
  6: 'Kurul 6: Endokrin & Yaşlanma',
};

const DISCIPLINE_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  'Tıbbi Farmakoloji': { bg: 'bg-emerald-50', text: 'text-emerald-800', border: 'border-emerald-200' },
  'Tıbbi Patoloji': { bg: 'bg-rose-50', text: 'text-rose-800', border: 'border-rose-200' },
  'Tıbbi Mikrobiyoloji': { bg: 'bg-amber-50', text: 'text-amber-800', border: 'border-amber-200' },
  'Tıbbi Genetik': { bg: 'bg-indigo-50', text: 'text-indigo-800', border: 'border-indigo-200' },
  'Halk Sağlığı': { bg: 'bg-sky-50', text: 'text-sky-800', border: 'border-sky-200' },
  'Tıbbi Biyokimya': { bg: 'bg-purple-50', text: 'text-purple-800', border: 'border-purple-200' },
  'İç Hastalıkları': { bg: 'bg-blue-50', text: 'text-blue-800', border: 'border-blue-200' },
};

export const LectureSummariesView: React.FC<LectureSummariesViewProps> = ({ onOpenPdfModal }) => {
  const [selectedKurul, setSelectedKurul] = useState<number | 'all'>('all');
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Active reading modal
  const [activeSummary, setActiveSummary] = useState<SummaryDetail | null>(null);
  const [isLoadingContent, setIsLoadingContent] = useState(false);
  const [copied, setCopied] = useState(false);

  // All metadata list
  const summaries: SummaryMeta[] = summariesMetaData as SummaryMeta[];

  // Unique disciplines
  const disciplines = useMemo(() => {
    const set = new Set<string>();
    summaries.forEach((s) => s.discipline && set.add(s.discipline));
    return Array.from(set).sort();
  }, [summaries]);

  // Filtered summaries
  const filteredSummaries = useMemo(() => {
    return summaries.filter((s) => {
      if (selectedKurul !== 'all' && s.kurul !== selectedKurul) return false;
      if (selectedDiscipline !== 'all' && s.discipline !== selectedDiscipline) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const inTitle = s.title.toLowerCase().includes(q);
        const inDiscipline = s.discipline.toLowerCase().includes(q);
        const inPoints = s.keyPoints.some((p) => p.toLowerCase().includes(q));
        if (!inTitle && !inDiscipline && !inPoints) return false;
      }
      return true;
    });
  }, [summaries, selectedKurul, selectedDiscipline, searchQuery]);

  // Load full summary content when opened
  const handleOpenSummary = async (meta: SummaryMeta) => {
    setActiveSummary(meta);
    setIsLoadingContent(true);
    try {
      // 1. Try server API
      const res = await fetch(`/api/summaries/${meta.id}`);
      if (res.ok && res.headers.get('content-type')?.includes('application/json')) {
        const data = await res.json();
        if (data.success && data.summary?.content) {
          setActiveSummary(data.summary);
          setIsLoadingContent(false);
          return;
        }
      }
    } catch (_) {}

    // 2. Fallback to dynamic full import for GitHub Pages / offline
    try {
      const fullMod = await import('../data/lectureSummariesCatalog.json');
      const found = (fullMod.default || fullMod).find((s: any) => s.id === meta.id);
      if (found && found.content) {
        setActiveSummary(found);
      }
    } catch (e) {
      console.warn('Could not load full summary content:', e);
    } finally {
      setIsLoadingContent(false);
    }
  };

  const handleCopyMarkdown = () => {
    if (!activeSummary?.content) return;
    navigator.clipboard.writeText(activeSummary.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="max-w-[1280px] mx-auto px-4 sm:px-8 py-6 space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-teal-900 via-teal-800 to-slate-900 rounded-2xl p-6 sm:p-8 text-white shadow-lg relative overflow-hidden">
        <div className="relative z-10 max-w-2xl space-y-2">
          <div className="inline-flex items-center gap-2 bg-teal-500/20 border border-teal-400/30 px-3 py-1 rounded-full text-xs font-semibold text-teal-200">
            <Sparkles className="w-3.5 h-3.5" />
            <span>347 Amfi Ders Sunumu & Spot Bilgi Kataloğu</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold font-display tracking-tight text-white">
            Ders Özetleri & Yüksek Verimli Tıp Notları
          </h1>
          <p className="text-sm text-teal-100/90 leading-relaxed">
            Dönem 3 kurul sınavlarında hocaların en çok üzerinde durduğu klinik ipuçları, patofizyolojik mekanizmalar, sınav tuzakları ve farmakolojik tablolar.
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs space-y-3">
        {/* Kurul pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar text-xs font-semibold">
          <button
            type="button"
            onClick={() => setSelectedKurul('all')}
            className={`px-3 py-1.5 rounded-lg shrink-0 cursor-pointer transition-colors ${
              selectedKurul === 'all'
                ? 'bg-teal-700 text-white shadow-xs'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            Tüm Kurullar ({summaries.length})
          </button>
          {[1, 2, 3, 4, 5, 6].map((kNum) => {
            const count = summaries.filter((s) => s.kurul === kNum).length;
            const isSel = selectedKurul === kNum;
            return (
              <button
                key={kNum}
                type="button"
                onClick={() => setSelectedKurul(kNum)}
                className={`px-3 py-1.5 rounded-lg shrink-0 cursor-pointer transition-colors ${
                  isSel
                    ? 'bg-teal-700 text-white shadow-xs'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                Kurul {kNum} ({count})
              </button>
            );
          })}
        </div>

        {/* Search & Discipline Filter */}
        <div className="flex flex-col sm:flex-row gap-3 items-center">
          <div className="relative flex-1 w-full">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Ders başlığı, konu veya klinik terim ara (örn: İmmunofarmakoloji, Aort, Diyabet)..."
              className="w-full pl-9 pr-4 py-2 text-sm border border-slate-200 rounded-lg bg-slate-50 focus:bg-white focus:outline-hidden focus:border-teal-600 transition-colors"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-2.5 text-slate-400 hover:text-slate-600 cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          <div className="w-full sm:w-auto shrink-0 flex items-center gap-2">
            <Filter className="w-4 h-4 text-slate-400" />
            <select
              value={selectedDiscipline}
              onChange={(e) => setSelectedDiscipline(e.target.value)}
              className="w-full sm:w-48 py-2 px-3 text-xs font-medium border border-slate-200 rounded-lg bg-white focus:outline-hidden focus:border-teal-600 cursor-pointer"
            >
              <option value="all">Tüm Branşlar ({disciplines.length})</option>
              {disciplines.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Summaries Grid */}
      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs text-slate-500 px-1">
          <span>
            Toplam <strong>{filteredSummaries.length}</strong> ders özeti listeleniyor
          </span>
          {onOpenPdfModal && (
            <button
              type="button"
              onClick={onOpenPdfModal}
              className="text-teal-700 hover:text-teal-900 font-bold flex items-center gap-1 cursor-pointer"
            >
              <Download className="w-3.5 h-3.5" />
              <span>PDF İndirme Merkezine Git</span>
            </button>
          )}
        </div>

        {filteredSummaries.length === 0 ? (
          <div className="bg-white rounded-xl border border-slate-200 p-12 text-center space-y-3">
            <BookOpen className="w-10 h-10 text-slate-300 mx-auto" />
            <h3 className="font-bold text-slate-800 text-sm">Aranan kriterlere uygun ders özeti bulunamadı</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Arama filtrenizi temizleyerek veya farklı bir kurul seçerek tekrar deneyebilirsiniz.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredSummaries.map((s) => {
              const discColor = DISCIPLINE_COLORS[s.discipline] || {
                bg: 'bg-slate-50',
                text: 'text-slate-800',
                border: 'border-slate-200',
              };

              return (
                <div
                  key={s.id}
                  onClick={() => handleOpenSummary(s)}
                  className="bg-white rounded-xl border border-slate-200 hover:border-teal-500/80 p-5 shadow-2xs hover:shadow-md transition-all flex flex-col justify-between cursor-pointer group"
                >
                  <div className="space-y-2.5">
                    {/* Tags */}
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-[11px] font-bold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                        Kurul {s.kurul}
                      </span>
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded border ${discColor.bg} ${discColor.text} ${discColor.border}`}
                      >
                        {s.discipline}
                      </span>
                    </div>

                    {/* Title */}
                    <h3 className="font-bold text-sm text-slate-900 group-hover:text-teal-700 transition-colors line-clamp-2">
                      {s.title}
                    </h3>

                    {/* Key takeaway bullets */}
                    {s.keyPoints && s.keyPoints.length > 0 && (
                      <ul className="space-y-1 text-xs text-slate-600 pt-1">
                        {s.keyPoints.slice(0, 3).map((pt, idx) => (
                          <li key={idx} className="flex items-start gap-1.5 line-clamp-1">
                            <span className="text-teal-600 font-bold shrink-0">•</span>
                            <span className="truncate">{pt}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>

                  {/* Footer */}
                  <div className="pt-4 mt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
                    <span className="flex items-center gap-1 font-mono text-[11px]">
                      <Clock className="w-3.5 h-3.5 text-slate-400" />
                      ~{s.readingTimeMinutes} dk okuma
                    </span>
                    <span className="font-bold text-teal-700 group-hover:translate-x-0.5 transition-transform flex items-center gap-0.5">
                      <span>Özeti Oku</span>
                      <ChevronRight className="w-4 h-4" />
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* State-of-the-Art Artifact Reader View */}
      {activeSummary && (
        <SummaryArtifactReader
          summary={activeSummary}
          onClose={() => setActiveSummary(null)}
          onOpenPdfModal={onOpenPdfModal}
        />
      )}
    </div>
  );
};
