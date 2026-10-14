import React, { useState, useEffect, useMemo } from 'react';
import { PageHeader } from './ui/PageHeader';
import { PageToolbar, QuickOptions } from './ui/PageToolbar';
import { useAppearance } from '../utils/appearance';
import { TranscriptionsV12 } from './v12/TranscriptionsV12';
import {
  Mic,
  Search,
  FileText,
  Clock,
  Sparkles,
  Copy,
  Check,
  ChevronRight,
} from 'lucide-react';

import {
  useTranscriptionsQuery,
  useTranscriptionDetailQuery,
  TranscriptionMeta,
  TranscriptionDetail,
} from '../hooks/useMedicalQueries';

export type { TranscriptionMeta, TranscriptionDetail };

interface TranscriptionsViewProps {
  onAskAiWithContext?: (contextText: string, title: string) => void;
}

const DISCIPLINE_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  'Halk Sağlığı': { bg: 'bg-accent-soft', text: 'text-accent', border: 'border-accent/30' },
  'Tıbbi Genetik': { bg: 'bg-accent-soft', text: 'text-accent', border: 'border-accent/30' },
  'Enfeksiyon Hastalıkları': { bg: 'bg-warn-soft', text: 'text-warn', border: 'border-warn/30' },
  'Tıbbi Patoloji': { bg: 'bg-bad-soft', text: 'text-bad-text', border: 'border-bad/30' },
  'İç Hastalıkları / Üroloji': { bg: 'bg-ok-soft', text: 'text-ok', border: 'border-ok/30' },
};

export const TranscriptionsView: React.FC<TranscriptionsViewProps> = ({ onAskAiWithContext }) => {
  const { data: transcriptions = [], isLoading } = useTranscriptionsQuery();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('all');
  
  // Selected detail modal / reader (TanStack Query ile önbellekli)
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const { data: selectedItem, isLoading: isLoadingDetail } = useTranscriptionDetailQuery(selectedId);
  const [copied, setCopied] = useState(false);
  const v12 = useAppearance().design === 'v12';

  const handleOpenDetail = (meta: TranscriptionMeta) => {
    setSelectedId(meta.id);
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

  if (v12) {
    const countOf = (d: string) => transcriptions.filter((t) => t.discipline === d).length;
    return (
      <TranscriptionsV12
        toolbar={
          <PageToolbar
            title="Ses kayıtları"
            count={filteredTranscriptions.length === transcriptions.length ? `${transcriptions.length} kayıt` : `${filteredTranscriptions.length} / ${transcriptions.length}`}
            search={{ value: searchQuery, onChange: setSearchQuery, placeholder: 'Transkript ya da konu ara' }}
            quick={
              disciplines.length > 0
                ? [
                    {
                      id: 'brans',
                      label: 'Branş',
                      value: selectedDiscipline !== 'all' ? selectedDiscipline : undefined,
                      onClear: () => setSelectedDiscipline('all'),
                      content: (close) => (
                        <QuickOptions
                          options={[{ id: 'all', label: 'Tüm branşlar', count: transcriptions.length }, ...disciplines.map((d) => ({ id: d, label: d, count: countOf(d) }))]}
                          value={selectedDiscipline}
                          onPick={setSelectedDiscipline}
                          close={close}
                        />
                      ),
                    },
                  ]
                : undefined
            }
          />
        }
        isLoading={isLoading}
        items={filteredTranscriptions}
        hasAny={transcriptions.length > 0}
        onOpen={handleOpenDetail}
        selectedId={selectedId}
        detail={selectedItem}
        isLoadingDetail={isLoadingDetail}
        onClose={() => setSelectedId(null)}
        onCopy={handleCopy}
        onAskAiWithContext={onAskAiWithContext}
      />
    );
  }

  return (
    <div className="w-full min-w-0 flex flex-col gap-4 sm:gap-5 pb-8">
      <PageHeader
        eyebrow="Amfi ses kayıtları"
        title="Ses kayıtları"
        description="Hocaların amfide anlattığı derslerin kelimesi kelimesine çözümlenmiş, tıbbi terimleri düzeltilmiş metinleri."
        stats={[{ label: 'Çözümlenen kayıt', value: transcriptions.length }]}
      />

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-xl border border-line p-4 shadow-xs flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-ink-3 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Transkript veya konu ara..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-2 text-sm bg-field border border-line rounded-lg focus:outline-none focus:ring-2 focus:ring-accent/20 focus:border-accent transition-colors"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
          <button
            onClick={() => setSelectedDiscipline('all')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
              selectedDiscipline === 'all'
                ? 'bg-accent text-white shadow-xs'
                : 'bg-field text-ink-2 hover:bg-line'
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
                  ? 'bg-accent text-white shadow-xs'
                  : 'bg-field text-ink-2 hover:bg-line'
              }`}
            >
              {d}
            </button>
          ))}
        </div>
      </div>

      {/* Grid of Transcriptions */}
      {isLoading ? (
        <div className="py-20 text-center text-ink-3 space-y-3">
          <div className="w-8 h-8 border-3 border-accent border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-sm font-medium">Ses kaydı transkriptleri yükleniyor...</p>
        </div>
      ) : filteredTranscriptions.length === 0 ? (
        <div className="py-16 text-center text-ink-3 bg-white rounded-xl border border-line p-8 space-y-2">
          <Mic className="w-10 h-10 text-ink-3 mx-auto" />
          <h3 className="font-semibold text-ink-2">Aramanıza uygun transkript bulunamadı</h3>
          <p className="text-xs text-ink-3">Arama kelimelerini veya branş filtresini değiştirmeyi deneyebilirsiniz.</p>
        </div>
      ) : (
        <div className="bento bento-host is-rhythm is-list">
          {filteredTranscriptions.map(item => {
            const color = DISCIPLINE_COLORS[item.discipline] || { bg: 'bg-field', text: 'text-ink-2', border: 'border-line' };
            return (
              <div
                key={item.id}
                onClick={() => handleOpenDetail(item)}
                className="bg-white rounded-xl border border-line p-5 shadow-xs hover:shadow-md hover:border-accent/30 transition-all cursor-pointer flex flex-col justify-between group"
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between gap-2">
                    <span className={`px-2.5 py-0.5 rounded-md text-2xs font-semibold border ${color.bg} ${color.text} ${color.border}`}>
                      {item.discipline}
                    </span>
                    <span className="flex items-center gap-1 text-2xs text-ink-3 font-medium">
                      <Clock className="w-3.5 h-3.5 text-ink-3" />
                      ~{item.estimatedMinutes} dk dinleme
                    </span>
                  </div>

                  <h3 className="font-bold text-ink group-hover:text-accent transition-colors line-clamp-2 leading-snug">
                    {item.title}
                  </h3>

                  <p className="text-xs text-ink-3 line-clamp-3 leading-relaxed">
                    {item.firstSnippet}
                  </p>
                </div>

                <div className="pt-4 mt-4 border-t border-line flex items-center justify-between text-xs text-ink-3">
                  <span className="flex items-center gap-1">
                    <FileText className="w-3.5 h-3.5 text-ink-3" />
                    {item.wordCount.toLocaleString('tr-TR')} kelime · {item.sectionsCount} bölüm
                  </span>
                  <span className="inline-flex items-center gap-1 font-semibold text-accent group-hover:translate-x-0.5 transition-transform">
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
        <div className="ms-overlay fixed inset-0 z-50 bg-[var(--color-scrim)] flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90dvh] shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-150">
            {/* Modal Header */}
            <div className="p-5 border-b border-line bg-field flex items-start justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-md text-2xs font-semibold bg-accent-soft text-accent border border-accent/30">
                    {selectedItem.discipline}
                  </span>
                  <span className="text-xs text-ink-3">
                    ~{selectedItem.estimatedMinutes} dk · {selectedItem.wordCount.toLocaleString('tr-TR')} kelime
                  </span>
                </div>
                <h2 className="text-lg sm:text-xl font-bold text-ink leading-snug">
                  {selectedItem.title}
                </h2>
              </div>

              <div className="flex items-center gap-2 shrink-0">
                <button
                  onClick={() => handleCopy(selectedItem.content)}
                  className="px-3 py-1.5 rounded-lg border border-line bg-white hover:bg-field text-ink-2 text-xs font-semibold flex items-center gap-1.5 transition-colors"
                  title="Metni Kopyala"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-ok" /> : <Copy className="w-3.5 h-3.5" />}
                  {copied ? 'Kopyalandı' : 'Kopyala'}
                </button>
                <button
                  onClick={() => setSelectedId(null)}
                  className="p-1.5 rounded-lg text-ink-3 hover:text-ink-2 hover:bg-line transition-colors"
                >
                                  </button>
              </div>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto space-y-6 text-ink leading-relaxed text-sm sm:text-base">
              {selectedItem.sections.map((sec, idx) => (
                <div key={idx} className="space-y-2 border-b border-line pb-5 last:border-0">
                  <h4 className="font-bold text-accent text-base sm:text-lg flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-accent" />
                    {sec.title}
                  </h4>
                  <div className="whitespace-pre-line text-ink-2 leading-relaxed text-sm pl-4 border-l-2 border-line">
                    {sec.content}
                  </div>
                </div>
              ))}
            </div>

            {/* Modal Footer */}
            <div className="p-4 border-t border-line bg-field flex items-center justify-between text-xs text-ink-3">
              <span className="flex items-center gap-1.5">
                <Sparkles className="w-4 h-4 text-ok" />
                Bu transkript RAG vektör sisteminde aramalara açıktır.
              </span>
              <button
                onClick={() => setSelectedId(null)}
                className="px-4 py-2 bg-ink text-white rounded-lg font-semibold hover:bg-ink transition-colors"
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
