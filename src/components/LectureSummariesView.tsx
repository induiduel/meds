import React, { useState, useEffect, useMemo } from 'react';
import { disciplineClass, disciplineLabel } from '../utils/discipline';
import { PageHeader } from './ui/PageHeader';
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
// Resmi ders programı + kaynak PDF eşleşmesi: scripts/pipeline/10-enrich-summaries.mjs üretir
import summariesEnrichment from '../data/summaries_enrichment.json';
import curriculumDisciplines from '../data/curriculum_disciplines.json';
import { SummaryArtifactReader } from './SummaryArtifactReader';
import { triggerDomHighlightAndScroll } from '../services/universalRedirectService';

export interface SummaryMeta {
  id: string;
  kurul: number;
  committeeId: string;
  discipline: string;
  title: string;
  instructor?: string;
  fileName: string;
  keyPoints: string[];
  charCount: number;
  readingTimeMinutes: number;
  /** Kaynak PDF'in oluşturulma yılı (biliniyorsa) */
  sourceYear?: number;
  sourceDate?: string;
  pdfName?: string;
}

type Enrichment = { lessonTitle?: string; discipline?: string; instructor?: string; sourceYear?: number; sourceDate?: string; pdfName?: string };
const ENRICH = summariesEnrichment as Record<string, Enrichment>;
const KURUL_DISCIPLINES = curriculumDisciplines as Record<string, string[]>;

/** Dosya adından türemiş başlıkları toparlar: baştaki sıra numarası, "D3", alt çizgi vb. */
const cleanTitle = (t: string) =>
  t
    .replace(/^\s*\d+\s*[).\-]?\s*/, '')
    .replace(/\b(d\d+|son|kopya|\(\d+\))\b/gi, ' ')
    .replace(/\s{2,}/g, ' ')
    .trim()
    .replace(/^\p{Ll}/u, (c) => c.toLocaleUpperCase('tr')) || t;

export interface SummaryDetail extends SummaryMeta {
  content?: string;
}

interface LectureSummariesViewProps {
  onOpenPdfModal?: () => void;
  /** Aramadan gelince doğrudan açılacak özet */
  initialSummaryId?: string;
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
  'Tıbbi Farmakoloji': { bg: 'bg-ok-soft', text: 'text-ok', border: 'border-ok/30' },
  'Tıbbi Patoloji': { bg: 'bg-bad-soft', text: 'text-bad-text', border: 'border-bad/30' },
  'Tıbbi Mikrobiyoloji': { bg: 'bg-warn-soft', text: 'text-warn', border: 'border-warn/30' },
  'Tıbbi Genetik': { bg: 'bg-accent-soft', text: 'text-accent', border: 'border-accent/30' },
  'Halk Sağlığı': { bg: 'bg-accent-soft', text: 'text-accent', border: 'border-accent/30' },
  'Tıbbi Biyokimya': { bg: 'bg-ai-soft', text: 'text-ai', border: 'border-ai/30' },
  'İç Hastalıkları': { bg: 'bg-accent-soft', text: 'text-accent', border: 'border-accent/30' },
};

export const LectureSummariesView: React.FC<LectureSummariesViewProps> = ({ onOpenPdfModal, initialSummaryId }) => {
  const [selectedKurul, setSelectedKurul] = useState<number | 'all'>('all');
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Active reading modal
  const [activeSummary, setActiveSummary] = useState<SummaryDetail | null>(null);
  const [isLoadingContent, setIsLoadingContent] = useState(false);
  const [copied, setCopied] = useState(false);

  // All metadata list
  // Ders programından gelen gerçek ders adı, branş ve öğretim üyesi; kaynak PDF yılı
  const summaries: SummaryMeta[] = useMemo(
    () =>
      (summariesMetaData as SummaryMeta[]).map((s) => {
        const e = ENRICH[s.id] || {};
        return {
          ...s,
          title: e.lessonTitle || cleanTitle(s.title),
          discipline: e.discipline || s.discipline,
          instructor: e.instructor || s.instructor,
          sourceYear: e.sourceYear,
          sourceDate: e.sourceDate,
          pdfName: e.pdfName,
        };
      }),
    []
  );

  // Kurul seçiliyse yalnızca o kurulda verilen dersler (resmi programdan; özeti olanlar)
  const disciplines = useMemo(() => {
    const have = new Set(summaries.filter((s) => selectedKurul === 'all' || s.kurul === selectedKurul).map((s) => s.discipline).filter(Boolean));
    const program = selectedKurul === 'all' ? null : KURUL_DISCIPLINES[String(selectedKurul)];
    const list = program ? program.filter((d) => have.has(d)) : Array.from(have);
    return list.sort((a, b) => a.localeCompare(b, 'tr'));
  }, [summaries, selectedKurul]);

  useEffect(() => {
    if (selectedDiscipline !== 'all' && !disciplines.includes(selectedDiscipline)) setSelectedDiscipline('all');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [disciplines]);

  // Filtered summaries
  const filteredSummaries = useMemo(() => {
    return summaries.filter((s) => {
      if (selectedKurul !== 'all' && s.kurul !== selectedKurul) return false;
      if (selectedDiscipline !== 'all' && s.discipline !== selectedDiscipline) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const inTitle = s.title.toLowerCase().includes(q);
        const inDiscipline = s.discipline.toLowerCase().includes(q);
        const inInstructor = s.instructor ? s.instructor.toLowerCase().includes(q) : false;
        const inPoints = s.keyPoints.some((p) => p.toLowerCase().includes(q));
        if (!inTitle && !inDiscipline && !inInstructor && !inPoints) return false;
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
        if (typeof window !== 'undefined') {
          const urlParams = new URLSearchParams(window.location.search);
          const highlight = urlParams.get('highlight');
          if (highlight) {
            setTimeout(() => triggerDomHighlightAndScroll(highlight), 400);
          }
        }
      }
    } catch (e) {
      console.warn('Could not load summary content from committee chunk:', e);
    } finally {
      setIsLoadingContent(false);
    }
  };

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const urlParams = new URLSearchParams(window.location.search);
    const targetId = initialSummaryId || urlParams.get('id') || urlParams.get('summaryId') || urlParams.get('noteId');
    const highlight = urlParams.get('highlight');

    if (targetId) {
      const meta = summaries.find((x) => x.id === targetId);
      if (meta) {
        handleOpenSummary(meta);
        if (highlight) {
          setTimeout(() => triggerDomHighlightAndScroll(highlight), 700);
        }
      }
    } else if (highlight) {
      setTimeout(() => triggerDomHighlightAndScroll(highlight), 500);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialSummaryId, summaries]);


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
      <PageHeader
        eyebrow="Amfi notları"
        title="Ders özetleri"
        description="Klinik ipuçları, mekanizmalar, sınav tuzakları ve tablolar; ders ders, okunur biçimde."
        stats={[{ label: 'özet', value: filteredSummaries.length }]}
        actions={
          onOpenPdfModal && (
            <button
              type="button"
              onClick={onOpenPdfModal}
              aria-label="PDF indir"
              className="shrink-0 h-10 px-3 rounded-[10px] border border-line bg-white text-base font-semibold inline-flex items-center gap-2 cursor-pointer hover:border-line-2"
            >
              <Download className="w-4 h-4" />
              <span className="hidden sm:inline">PDF indir</span>
            </button>
          )
        }
      />

      {/* Arama + branş tek satır; kurullar altı çizili sekme (Çıkmış dili) */}
      <div className="flex flex-col sm:flex-row gap-2 min-w-0">
        <label className="cx-search flex-1 min-w-0">
          <Search aria-hidden />
          <span className="sr-only">Özetlerde ara</span>
          <input type="search" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} placeholder="Ders, konu ya da terim ara" />
          {searchQuery && (
            <button type="button" className="cx-search-x" onClick={() => setSearchQuery('')} aria-label="Aramayı temizle"><X /></button>
          )}
        </label>
        <label className="sr-only" htmlFor="summ-discipline">Branş</label>
        <select
          id="summ-discipline"
          value={selectedDiscipline}
          onChange={(e) => setSelectedDiscipline(e.target.value)}
          className="ms-select h-11 sm:w-[230px] min-w-0"
        >
          <option value="all">{selectedKurul === 'all' ? 'Tüm dersler' : `Kurul ${selectedKurul} dersleri`} ({disciplines.length})</option>
          {disciplines.map((d) => (
            <option key={d} value={d}>{d}</option>
          ))}
        </select>
      </div>
      <nav className="cx-tabs" aria-label="Kurul" role="radiogroup">
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
              className={`cx-tab ${on ? 'is-on' : ''} ${count === 0 ? 'is-zero' : ''}`}
            >
              {k === 'all' ? 'Tümü' : `K${k}`} <small>{count}</small>
            </button>
          );
        })}
      </nav>

      {selectedKurul !== 'all' && <p className="m-0 -mt-1 text-sm text-ink-3">{KURUL_LABELS[selectedKurul]}</p>}

      {filteredSummaries.length === 0 ? (
        <div className="ui-card text-center flex flex-col items-center gap-2" style={{ paddingBlock: 36 }}>
          <h3 className="m-0 font-display text-xl font-bold tracking-[-0.02em]">Bu süzgeçte özet yok</h3>
          <p className="m-0 text-base text-ink-2">Aramayı temizle ya da başka bir kurul seç.</p>
        </div>
      ) : (
        <ul className="list-none m-0 p-0 ui-grid">
          {filteredSummaries.map((s) => (
            <li key={s.id} className={`min-w-0 ${disciplineClass(s.discipline)}`}>
              <button
                type="button"
                onClick={() => handleOpenSummary(s)}
                className="ks-lesson group"
              >
                <span className="ks-lesson-top">
                  <span className="hk-eyebrow"><i className="hk-dot" aria-hidden /><span>{disciplineLabel(s.discipline) || s.discipline}</span></span>
                  <span className="ks-lesson-no">K{s.kurul}</span>
                  {s.sourceYear && (
                    <span className="ml-auto shrink-0 text-xs text-ink-3 tabular-nums" title={s.pdfName ? `${s.pdfName} · ${s.sourceDate}` : s.sourceDate}>
                      {s.sourceYear}
                    </span>
                  )}
                </span>
                <span className="ks-lesson-t line-clamp-2">{s.title}</span>
                {s.instructor && (
                  <span className="text-sm text-ink-2 font-medium flex items-center gap-1.5 truncate">
                    <GraduationCap className="w-3.5 h-3.5 text-accent shrink-0" />
                    <span className="truncate">{s.instructor}</span>
                  </span>
                )}
                {s.keyPoints?.length > 0 && (
                  <span className="flex flex-col gap-0.5 text-sm text-ink-2">
                    {s.keyPoints.slice(0, 3).map((pt, idx) => (
                      <span key={idx} className="truncate">
                        · {pt}
                      </span>
                    ))}
                  </span>
                )}
                <span className="mt-auto pt-2 border-t border-line-soft flex items-center justify-between text-xs text-ink-3">
                  <span className="inline-flex items-center gap-1 font-mono">
                    <Clock className="w-3.5 h-3.5" /> ~{s.readingTimeMinutes} dk
                  </span>
                  <span className="inline-flex items-center gap-0.5 text-sm font-semibold text-accent">
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
