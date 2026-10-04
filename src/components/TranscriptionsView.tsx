import React, { useState, useEffect, useMemo } from 'react';
import { PageHeader } from './ui/PageHeader';
import {
  Mic,
  Headphones,
  Search,
  Filter,
  FileText,
  Clock,
  BookOpen,
  Sparkles,
  Copy,
  Check,
  ChevronRight,
  ExternalLink,
  Volume2,
  Calendar,
  Layers,
  GraduationCap,
  MessageSquare
} from 'lucide-react';

export interface TranscriptionMeta {
  id: string;
  fileName: string;
  title: string;
  discipline: string;
  committeeId: string;
  charCount: number;
  wordCount: number;
  estimatedMinutes: number;
  sectionsCount: number;
  firstSnippet: string;
}

export interface TranscriptionDetail extends TranscriptionMeta {
  content: string;
  sections: Array<{
    title: string;
    level: number;
    content: string;
  }>;
}

interface TranscriptionsViewProps {
  onAskAiWithContext?: (contextText: string, title: string) => void;
}

const DISCIPLINE_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  'Halk Sağlığı': { bg: 'bg-sky-50', text: 'text-sky-800', border: 'border-sky-200' },
  'Tıbbi Genetik': { bg: 'bg-indigo-50', text: 'text-indigo-800', border: 'border-indigo-200' },
  'Enfeksiyon Hastalıkları': { bg: 'bg-amber-50', text: 'text-amber-800', border: 'border-amber-200' },
  'Tıbbi Patoloji': { bg: 'bg-rose-50', text: 'text-rose-800', border: 'border-rose-200' },
  'İç Hastalıkları / Üroloji': { bg: 'bg-emerald-50', text: 'text-emerald-800', border: 'border-emerald-200' },
};

export const TranscriptionsView: React.FC<TranscriptionsViewProps> = ({ onAskAiWithContext }) => {
  const [transcriptions, setTranscriptions] = useState<TranscriptionMeta[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('all');
  
  // Selected detail modal / reader
  const [selectedItem, setSelectedItem] = useState<TranscriptionDetail | null>(null);
  const [isLoadingDetail, setIsLoadingDetail] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    fetchTranscriptions();
  }, []);

  const fetchTranscriptions = async () => {
    setIsLoading(true);
    try {
      const res = await fetch('/api/transcriptions');
      if (res.ok) {
        const data = await res.json();
        if (data.success && Array.isArray(data.transcriptions)) {
          setTranscriptions(data.transcriptions);
        }
      }
    } catch (e) {
      console.warn('Transkripsiyonlar yüklenemedi:', e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOpenDetail = async (meta: TranscriptionMeta) => {
    setIsLoadingDetail(true);
    try {
      const res = await fetch(`/api/transcriptions/${encodeURIComponent(meta.id)}`);
      if (res.ok) {
        const data = await res.json();
        if (data.success && data.transcription) {
          setSelectedItem(data.transcription);
          return;
        }
      }
    } catch (e) {
      console.warn('Detay yüklenemedi:', e);
    } finally {
      setIsLoadingDetail(false);
    }
  };

  const disciplines = useMemo(() => {
    const set = new Set<string>();
    transcriptions.forEach(t => t.discipline && set.add(t.discipline));
    return Array.from(set).sort();
  }, [transcriptions]);

  const filteredTranscriptions = useMemo(() => {
    return transcriptions.filter(t => {
      if (selectedDiscipline !== 'all' && t.discipline !== selectedDiscipline) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const inTitle = t.title.toLowerCase().includes(q);
        const inDiscipline = t.discipline.toLowerCase().includes(q);
        const inSnippet = t.firstSnippet.toLowerCase().includes(q);
        if (!inTitle && !inDiscipline && !inSnippet) return false;
      }
      return true;
    });
  }, [transcriptions, selectedDiscipline, searchQuery]);

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="w-full min-w-0 flex flex-col gap-4 sm:gap-5 pb-8">
      <PageHeader
        eyebrow="Amfi ses kayıtları"
        title="Ses kayıtları"
        description="Hocaların amfide anlattığı derslerin kelimesi kelimesine çözümlenmiş, tıbbi terimleri düzeltilmiş metinleri."
        stats={[{ label: 'Çözümlenen kayıt', value: transcriptions.length }]}
      />

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Transkript veya konu ara..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500/20 focus:border-sky-500 transition-colors"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
          <button
            onClick={() => setSelectedDiscipline('all')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
              selectedDiscipline === 'all'
                ? 'bg-sky-600 text-white shadow-xs'
                : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
            }`}
          >
            Tüm Branşlar ({transcriptions.length})
          </button>
          {disciplines.map(d => (
            <button
              key={d}
              onClick={() => setSelectedDiscipline(d)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
                selectedDiscipline === d
                  ? 'bg-sky-600 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {d}
            </button>
          ))}
        </div>
      </div>

      {/* Grid of Transcriptions */}
      {isLoading ? (
        <div className="py-20 text-center text-slate-500 space-y-3">
          <div className="w-8 h-8 border-3 border-sky-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-sm font-medium">Ses kaydı transkriptleri yükleniyor...</p>
        </div>
      ) : filteredTranscriptions.length === 0 ? (
        <div className="py-16 text-center text-slate-500 bg-white rounded-xl border border-slate-200 p-8 space-y-2">
          <Mic className="w-10 h-10 text-slate-300 mx-auto" />
          <h3 className="font-semibold text-slate-700">Aramanıza uygun transkript bulunamadı</h3>
          <p className="text-xs text-slate-400">Arama kelimelerini veya branş filtresini değiştirmeyi deneyebilirsiniz.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredTranscriptions.map(item => {
            const color = DISCIPLINE_COLORS[item.discipline] || { bg: 'bg-slate-50', text: 'text-slate-700', border: 'border-slate-200' };
            return (
              <div
                key={item.id}
                onClick={() => handleOpenDetail(item)}
                className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs hover:shadow-md hover:border-sky-300 transition-all cursor-pointer flex flex-col justify-between group"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between gap-2">
                    <span className={`px-2.5 py-0.5 rounded-md text-[11px] font-semibold border ${color.bg} ${color.text} ${color.border}`}>
                      {item.discipline}
                    </span>
                    <span className="flex items-center gap-1 text-[11px] text-slate-500 font-medium">
                      <Clock className="w-3.5 h-3.5 text-slate-400" />
                      ~{item.estimatedMinutes} dk dinleme
                    </span>
                  </div>

                  <h3 className="font-bold text-slate-900 group-hover:text-sky-600 transition-colors line-clamp-2 leading-snug">
                    {item.title}
                  </h3>

                  <p className="text-xs text-slate-500 line-clamp-3 leading-relaxed">
                    {item.firstSnippet}
                  </p>
                </div>

                <div className="pt-4 mt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                  <span className="flex items-center gap-1">
                    <FileText className="w-3.5 h-3.5 text-slate-400" />
                    {item.wordCount.toLocaleString('tr-TR')} kelime · {item.sectionsCount} bölüm
                  </span>
                  <span className="inline-flex items-center gap-1 font-semibold text-sky-600 group-hover:translate-x-0.5 transition-transform">
                    Oku <ChevronRight className="w-3.5 h-3.5" />
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Reader Modal */}
      {selectedItem && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-150">
            {/* Modal Header */}
            <div className="p-5 border-b border-slate-200 bg-slate-50 flex items-start justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-md text-[11px] font-semibold bg-sky-100 text-sky-800 border border-sky-200">
                    {selectedItem.discipline}
                  </span>
                  <span className="text-xs text-slate-500">
                    ~{selectedItem.estimatedMinutes} dk · {selectedItem.wordCount.toLocaleString('tr-TR')} kelime
                  </span>
                </div>
                <h2 className="text-lg sm:text-xl font-bold text-slate-900 leading-snug">
                  {selectedItem.title}
                </h2>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => handleCopy(selectedItem.content)}
                  className="px-3 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-colors"
                  title="Metni Kopyala"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                  {copied ? 'Kopyalandı' : 'Kopyala'}
                </button>
                <button
                  onClick={() => setSelectedItem(null)}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200 transition-colors"
                >
                  ✕
                </button>
              </div>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto space-y-6 text-slate-800 leading-relaxed text-sm sm:text-base">
              {selectedItem.sections.map((sec, idx) => (
                <div key={idx} className="space-y-2 border-b border-slate-100 pb-5 last:border-0">
                  <h4 className="font-bold text-sky-950 text-base sm:text-lg flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-sky-500" />
                    {sec.title}
                  </h4>
                  <div className="whitespace-pre-line text-slate-700 leading-relaxed text-sm pl-4 border-l-2 border-slate-200">
                    {sec.content}
                  </div>
                </div>
              ))}
            </div>

            {/* Modal Footer */}
            <div className="p-4 border-t border-slate-200 bg-slate-50 flex items-center justify-between text-xs text-slate-500">
              <span className="flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-emerald-600" />
                Bu transkript RAG vektör sisteminde aramalara açıktır.
              </span>
              <button
                onClick={() => setSelectedItem(null)}
                className="px-4 py-2 bg-slate-800 text-white rounded-lg font-semibold hover:bg-slate-900 transition-colors"
              >
                Kapat
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
