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

    // 2. Fallback to dynamic per-committee chunk import for GitHub Pages / offline
    try {
      let kurulMod: any;
      switch (meta.kurul) {
        case 1:
          kurulMod = await import('../data/summaries/kurul1.json');
          break;
        case 2:
          kurulMod = await import('../data/summaries/kurul2.json');
          break;
        case 3:
          kurulMod = await import('../data/summaries/kurul3.json');
          break;
        case 4:
          kurulMod = await import('../data/summaries/kurul4.json');
          break;
        case 5:
          kurulMod = await import('../data/summaries/kurul5.json');
          break;
        case 6:
          kurulMod = await import('../data/summaries/kurul6.json');
          break;
        default:
          kurulMod = await import('../data/summaries/kurul1.json');
          break;
      }
      const list = (kurulMod && (kurulMod.default || kurulMod)) || [];
      const found = list.find((s: any) => s.id === meta.id);
      if (found && found.content) {
        setActiveSummary(found);
      }
    } catch (e) {
      console.warn('Could not load summary content from committee chunk:', e);
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
    <div className="flex flex-col gap-3 sm:gap-5 min-w-0">
      {/* Title */}
      <div className="flex items-end justify-between gap-3">
        <div className="min-w-0">
          <h1 className="m-0 font-display font-bold text-[24px] sm:text-[32px] leading-[1.1] tracking-[-0.03em]">Ders özetleri</h1>
          <p className="m-0 mt-1 text-[14px] text-ink-2">
            {summaries.length} amfi dersinin özeti: klinik ipuçları, mekanizmalar, sınav tuzakları ve tablolar.
          </p>
        </div>
        {onOpenPdfModal && (
          <button
            type="button"
            onClick={onOpenPdfModal}
            aria-label="PDF indir"
            className="shrink-0 h-10 px-3 rounded-[10px] border border-line-2 bg-white text-[14px] font-semibold inline-flex items-center gap-2 cursor-pointer hover:border-ink-3"
          >
            <Download className="w-4 h-4" />
            <span className="hidden sm:inline">PDF indir</span>
          </button>
        )}
      </div>

      {/* Toolbar */}
      <div className="bg-white border border-line rounded-[16px] p-3 sm:p-4 flex flex-col gap-2.5">
        <div role="radiogroup" aria-label="Kurul" className="flex gap-1.5 overflow-x-auto no-scrollbar -mx-3 px-3 sm:mx-0 sm:px-0">
          {(['all', 1, 2, 3, 4, 5, 6] as const).map((k) => {
            const on = selectedKurul === k;
            const count = k === 'all' ? summaries.length : summaries.filter((s) => s.kurul === k).length;
            return (
              <button
                key={String(k)}
                type="button"
                role="radio"
                aria-checked={on}
                title={k === 'all' ? undefined : KURUL_LABELS[k]}
                onClick={() => setSelectedKurul(k)}
                className={`shrink-0 h-8 sm:h-9 px-3 rounded-full text-[13px] sm:text-[14px] cursor-pointer whitespace-nowrap ${
                  on ? 'bg-accent-soft text-accent font-semibold ring-1 ring-inset ring-accent/40' : 'bg-white border border-line text-ink hover:border-line-2'
                }`}
              >
                {k === 'all' ? 'Tümü' : `Kurul ${k}`}
                <span className={`ml-1.5 font-mono text-[12px] ${on ? 'text-accent/70' : 'text-ink-3'}`}>{count}</span>
              </button>
            );
          })}
        </div>
        <div className="flex flex-col sm:flex-row gap-2">
          <label className="flex items-center gap-2 h-10 px-3 border border-line-2 rounded-[10px] bg-field flex-1 min-w-0 focus-within:border-accent">
            <Search className="w-4 h-4 text-ink-2 shrink-0" />
            <span className="sr-only">Özetlerde ara</span>
            <input
              type="search"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Ders, konu ya da terim ara"
              className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[15px] placeholder:text-[#6B7785]"
            />
            {searchQuery && (
              <button type="button" onClick={() => setSearchQuery('')} aria-label="Aramayı temizle" className="w-7 h-7 rounded-md flex items-center justify-center text-ink-2 hover:bg-white cursor-pointer">
                <X className="w-4 h-4" />
              </button>
            )}
          </label>
          <label className="sr-only" htmlFor="summ-discipline">
            Branş
          </label>
          <select
            id="summ-discipline"
            value={selectedDiscipline}
            onChange={(e) => setSelectedDiscipline(e.target.value)}
            className="h-10 border border-line-2 rounded-[10px] px-3 text-[14px] bg-white cursor-pointer sm:w-[220px] min-w-0"
          >
            <option value="all">Tüm branşlar ({disciplines.length})</option>
            {disciplines.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="text-[13px] text-ink-2 px-1" role="status">
        <strong className="text-ink font-semibold">{filteredSummaries.length}</strong> özet
        {selectedKurul !== 'all' && <> · {KURUL_LABELS[selectedKurul]}</>}
      </div>

      {filteredSummaries.length === 0 ? (
        <div className="bg-white border border-line rounded-[16px] px-6 py-12 text-center flex flex-col items-center gap-2">
          <h3 className="m-0 font-display text-[20px] font-bold tracking-[-0.02em]">Bu filtrede özet yok</h3>
          <p className="m-0 text-[14px] text-ink-2">Aramayı temizleyip farklı bir kurul seçebilirsin.</p>
        </div>
      ) : (
        <ul className="list-none m-0 p-0 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-2.5 sm:gap-3">
          {filteredSummaries.map((s) => (
            <li key={s.id} className="min-w-0">
              <button
                type="button"
                onClick={() => handleOpenSummary(s)}
                className="w-full h-full text-left bg-white border border-line rounded-[14px] p-3.5 sm:p-4 flex flex-col gap-2 cursor-pointer hover:border-accent transition-colors group"
              >
                <span className="flex items-center gap-1.5 min-w-0">
                  <span className="shrink-0 h-6 px-2 rounded-full bg-canvas text-ink-2 text-[12px] font-semibold inline-flex items-center">Kurul {s.kurul}</span>
                  <span className="min-w-0 h-6 px-2 rounded-full bg-accent-soft text-accent text-[12px] font-semibold inline-flex items-center truncate">{s.discipline}</span>
                </span>
                <span className="text-[16px] font-semibold leading-snug text-ink group-hover:text-accent line-clamp-2">{s.title}</span>
                {s.keyPoints?.length > 0 && (
                  <span className="flex flex-col gap-0.5 text-[13px] text-ink-2">
                    {s.keyPoints.slice(0, 3).map((pt, idx) => (
                      <span key={idx} className="truncate">
                        · {pt}
                      </span>
                    ))}
                  </span>
                )}
                <span className="mt-auto pt-2 border-t border-line-soft flex items-center justify-between text-[12px] text-ink-3">
                  <span className="inline-flex items-center gap-1 font-mono">
                    <Clock className="w-3.5 h-3.5" /> ~{s.readingTimeMinutes} dk
                  </span>
                  <span className="inline-flex items-center gap-0.5 text-[13px] font-semibold text-accent">
                    Oku <ChevronRight className="w-4 h-4" />
                  </span>
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}

      {activeSummary && (
        <SummaryArtifactReader summary={activeSummary} onClose={() => setActiveSummary(null)} onOpenPdfModal={onOpenPdfModal} />
      )}
    </div>
  );
};
