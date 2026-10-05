import React, { useState } from 'react';
import { 
  X, 
  BookOpen, 
  ExternalLink, 
  ChevronLeft, 
  ChevronRight, 
  Layers, 
  Search, 
  Sparkles, 
  Check, 
  Copy, 
  FileText,
  User,
  Tag
} from 'lucide-react';
import { LectureNote } from '../types';

interface SlideReaderModalProps {
  isOpen: boolean;
  onClose: () => void;
  note: LectureNote | null;
  onFilterByNote?: (noteTitle: string) => void;
  /** Açılışta gösterilecek slayt numarası (aramadan gelince) */
  initialPageNumber?: number;
}

export const SlideReaderModal: React.FC<SlideReaderModalProps> = ({
  isOpen,
  onClose,
  note,
  onFilterByNote,
  initialPageNumber,
}) => {
  const [currentPageIndex, setCurrentPageIndex] = useState(() => {
    const i = initialPageNumber && note?.pages ? note.pages.findIndex((p) => p.pageNumber === initialPageNumber) : -1;
    return i >= 0 ? i : 0;
  });
  const [copied, setCopied] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  if (!isOpen || !note) return null;

  const totalPages = note.pages && note.pages.length > 0 ? note.pages.length : 1;
  const safeIndex = Math.min(Math.max(0, currentPageIndex), totalPages - 1);
  const activePage = note.pages && note.pages[safeIndex] 
    ? note.pages[safeIndex] 
    : {
        pageNumber: safeIndex + 1,
        content: 'Sayfa içeriği hazırlanıyor...',
        keywords: [],
      };

  const handleCopy = () => {
    const textToCopy = (activePage as any).repairedContent 
      ? `${activePage.content}\n\n${(activePage as any).repairedContent}`
      : activePage.content;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const filteredPages = searchQuery.trim()
    ? note.pages.filter((p) =>
        p.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.keywords.some((kw) => kw.toLowerCase().includes(searchQuery.toLowerCase()))
      )
    : note.pages;

  return (
    <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/70 backdrop-blur-xs animate-in fade-in duration-200">
      <div 
        className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-4xl max-h-[92dvh] flex flex-col overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-ink-surface text-white p-4 sm:p-5 flex items-start justify-between gap-3 shrink-0">
          <div className="space-y-1.5 min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <span className="bg-teal-700/80 text-teal-100 text-[11px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider border border-teal-500/30">
                {note.discipline}
              </span>
              <span className="text-xs text-teal-200 font-semibold flex items-center gap-1">
                <Layers className="w-3.5 h-3.5" />
                {note.totalSlides} Slayt / {totalPages} Bölüm Render Edildi
              </span>
            </div>
            <h2 className="text-base sm:text-lg font-black text-white leading-tight truncate">
              {note.title}
            </h2>
            {note.instructor && (
              <p className="text-xs text-teal-200/90 flex items-center gap-1">
                <User className="w-3 h-3 text-teal-400" />
                Ders Sorumlusu: {note.instructor}
              </p>
            )}
          </div>

          <div className="flex items-center gap-2 shrink-0">
            {note.driveFileUrl && (
              <a
                href={note.driveFileUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="bg-white/10 hover:bg-white/20 text-white border border-white/20 px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all shadow-xs"
              >
                <ExternalLink className="w-3.5 h-3.5 text-teal-300" />
                <span className="hidden sm:inline">Drive'da Orijinal PDF'i Aç</span>
                <span className="sm:hidden">Drive</span>
              </a>
            )}
            <button
              onClick={onClose}
              className="text-white/70 hover:text-white hover:bg-white/10 p-2 rounded-xl transition-all cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Toolbar & Page Navigation */}
        <div className="bg-slate-50 border-b border-slate-200 p-3 flex flex-wrap items-center justify-between gap-3 shrink-0">
          {/* Page Switcher */}
          <div className="flex items-center gap-2 w-full sm:w-auto min-w-0">
            <button
              onClick={() => setCurrentPageIndex((prev) => Math.max(0, prev - 1))}
              disabled={safeIndex === 0}
              className="p-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-100 disabled:opacity-40 disabled:pointer-events-none text-slate-700 transition-all cursor-pointer"
              title="Önceki Sayfa"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>

            <span className="shrink-0 whitespace-nowrap text-xs font-bold text-slate-800 px-2 py-1 bg-white rounded-md border border-slate-200 tabular-nums">
              <span className="hidden sm:inline">Sayfa / Bölüm </span>{safeIndex + 1} / {totalPages}
            </span>

            <button
              onClick={() => setCurrentPageIndex((prev) => Math.min(totalPages - 1, prev + 1))}
              disabled={safeIndex === totalPages - 1}
              className="p-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-100 disabled:opacity-40 disabled:pointer-events-none text-slate-700 transition-all cursor-pointer"
              title="Sonraki Sayfa"
            >
              <ChevronRight className="w-4 h-4" />
            </button>

            {/* Quick jump dropdown */}
            <select
              value={safeIndex}
              onChange={(e) => setCurrentPageIndex(Number(e.target.value))}
              aria-label="Bölüme git"
              className="min-w-0 flex-1 sm:flex-none sm:max-w-[260px] truncate text-xs font-semibold px-2 py-1 bg-white border border-slate-300 rounded-lg text-slate-700 cursor-pointer focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              {note.pages.map((p, idx) => (
                <option key={idx} value={idx}>
                  Bölüm {p.pageNumber}: {p.keywords.slice(0, 2).join(', ') || 'İçerik'}
                </option>
              ))}
            </select>
          </div>

          {/* Search inside note & copy button */}
          <div className="flex items-center gap-2 w-full sm:w-auto">
            <div className="relative flex-1 sm:w-56">
              <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Bu slayt içinde ara..."
                className="w-full text-xs pl-8 pr-3 py-1.5 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 text-slate-800"
              />
            </div>

            <button
              onClick={handleCopy}
              className="p-1.5 bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 rounded-lg text-xs font-medium flex items-center gap-1 transition-all cursor-pointer shrink-0"
              title="Metni Kopyala"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-slate-600" />}
              <span className="hidden sm:inline">{copied ? 'Kopyalandı' : 'Kopyala'}</span>
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-5 sm:p-6 space-y-6">
          {searchQuery.trim() && filteredPages.length === 0 ? (
            <div className="text-center py-10 text-slate-500 text-xs">
              "{searchQuery}" araması için bu notta eşleşen sayfa bulunamadı.
            </div>
          ) : (
            <div className="space-y-4">
              <div className="bg-teal-50/50 border border-teal-200/80 rounded-xl p-4 flex items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                  <span className="w-7 h-7 rounded-lg bg-teal-700 text-white font-black text-xs flex items-center justify-center shrink-0">
                    {activePage.pageNumber}
                  </span>
                  <div>
                    <h4 className="font-bold text-sm text-slate-900">
                      Bölüm {activePage.pageNumber} / {totalPages}
                    </h4>
                    <span className="text-[11px] text-teal-800 font-medium">
                      Doğrulanmış Kurul 1 Slayt Metni
                    </span>
                  </div>
                </div>

                {onFilterByNote && (
                  <button
                    onClick={() => {
                      onFilterByNote(note.title);
                      onClose();
                    }}
                    className="bg-emerald-600 hover:bg-emerald-700 text-white text-[11px] font-bold px-3 py-1.5 rounded-lg flex items-center gap-1 shadow-xs transition-all cursor-pointer"
                  >
                    <Sparkles className="w-3.5 h-3.5 text-emerald-200" />
                    <span>Bu Dersten Çıkan Soruları Havuzda Gör</span>
                  </button>
                )}
              </div>

              {/* Repaired / Supplemented with Redacted Summary Banner */}
              {(activePage as any).isRepairedWithRedaction && (
                <div className="p-3.5 bg-amber-50 border border-amber-200 rounded-xl flex items-center justify-between text-xs text-amber-900 shadow-2xs">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-amber-600 shrink-0" />
                    <span>
                      <strong>Amfi Redakte Dersi ile Onarıldı:</strong> Bu slaytın okunamayan veya eksik kısımları <em>"{(activePage as any).repairedSource || (note as any).matchedSummaryTitle || 'Amfi Ders Özeti'}"</em> ile tamamlanmıştır.
                    </span>
                  </div>
                </div>
              )}

              {/* Rendered Text Content */}
              <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-2xs space-y-4">
                <div className="prose prose-sm max-w-none text-slate-800 text-sm leading-relaxed whitespace-pre-wrap font-sans">
                  {activePage.content}
                </div>

                {(activePage as any).repairedContent && (
                  <div className="pt-4 border-t border-amber-200/80 bg-amber-50/60 p-4 rounded-xl text-amber-950 space-y-1.5">
                    <div className="text-xs font-bold text-amber-800 uppercase tracking-wider flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                      Redakte Amfi Dersi Tamamlayıcı Notu & Açıklaması
                    </div>
                    <div className="text-sm leading-relaxed whitespace-pre-line text-slate-800">
                      {(activePage as any).repairedContent}
                    </div>
                  </div>
                )}
              </div>

              {/* Keywords / High-Yield Medical Terms */}
              {activePage.keywords && activePage.keywords.length > 0 && (
                <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 space-y-2">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700">
                    <Tag className="w-3.5 h-3.5 text-teal-600" />
                    <span>Bu Bölümdeki Temel Tıbbi Terimler & Soru İpuçları:</span>
                  </div>
                  <div className="flex flex-wrap gap-1.5">
                    {activePage.keywords.map((kw, i) => (
                      <span
                        key={i}
                        className="text-[11px] font-semibold bg-white border border-teal-200 text-teal-900 px-2.5 py-1 rounded-md shadow-2xs"
                      >
                        #{kw}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-slate-50 border-t border-slate-200 p-3.5 flex items-center justify-between gap-3 text-xs text-slate-500 shrink-0">
          <span className="flex items-center gap-1">
            <BookOpen className="w-3.5 h-3.5 text-teal-700" />
            <span>MeDSor Slayt & Ders Notu Okuyucusu</span>
          </span>

          <div className="flex items-center gap-2">
            {note.driveFileUrl && (
              <a
                href={note.driveFileUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-teal-700 font-bold hover:text-teal-900 hover:underline flex items-center gap-1"
              >
                <span>Google Drive Linki</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            )}
            <button
              onClick={onClose}
              className="bg-slate-200 hover:bg-slate-300 text-slate-800 font-bold px-4 py-1.5 rounded-lg transition-colors cursor-pointer"
            >
              Kapat
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
