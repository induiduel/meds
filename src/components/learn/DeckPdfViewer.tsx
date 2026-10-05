import React, { useState, useEffect, useMemo, useRef } from 'react';
import {
  FileText,
  ExternalLink,
  Download,
  Upload,
  RefreshCw,
  Maximize2,
  Minimize2,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Columns,
  Eye,
  X,
  AlertCircle,
  CheckCircle2,
  BookOpen,
  ArrowRight,
  ArrowLeft,
  HardDrive,
  Cloud,
  ChevronLeft,
  ChevronRight,
  Compass,
} from 'lucide-react';
import type { InteractiveDeck, SlideItem } from './InteractiveDeckView';
import { getDeckOriginalPdf, DeckPdfMeta } from '../../data/deckPdfCatalog';
import { getSlidePdfLocation, SlidePdfLocation } from '../../services/slidePdfMappingService';

export interface DeckPdfViewerProps {
  deck: InteractiveDeck;
  currentSlideNumber?: number;
  currentSlide?: SlideItem;
  targetPage?: number;
  targetPageRange?: [number, number];
  onClose?: () => void;
  isSplitView?: boolean;
  onToggleSplitView?: () => void;
  compact?: boolean;
  onPageChange?: (page: number) => void;
}

type PdfSourceType = 'drive' | 'local' | 'custom';

export const DeckPdfViewer: React.FC<DeckPdfViewerProps> = ({
  deck,
  currentSlideNumber = 1,
  currentSlide,
  targetPage: propTargetPage,
  targetPageRange: propTargetPageRange,
  onClose,
  isSplitView = false,
  onToggleSplitView,
  compact = false,
  onPageChange,
}) => {
  const pdfMeta: DeckPdfMeta | undefined = useMemo(() => {
    return getDeckOriginalPdf(deck.id);
  }, [deck.id]);

  // Compute slide-to-PDF location mapping
  const slideLoc: SlidePdfLocation = useMemo(() => {
    return getSlidePdfLocation(deck.id, currentSlideNumber, currentSlide, deck.slides?.length);
  }, [deck.id, currentSlideNumber, currentSlide, deck.slides?.length]);

  const activeTargetPage = propTargetPage ?? slideLoc.primaryPage;
  const activePageRange = propTargetPageRange ?? slideLoc.pageRange;

  const [activePage, setActivePage] = useState<number>(activeTargetPage);
  const [sourceType, setSourceType] = useState<PdfSourceType>('local');
  const [customFileUrl, setCustomFileUrl] = useState<string | null>(null);
  const [customFileName, setCustomFileName] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [zoom, setZoom] = useState<number>(100);
  const [hasError, setHasError] = useState(false);
  const [isLocalServerAvailable, setIsLocalServerAvailable] = useState<boolean | null>(null);
  const [pageInputVal, setPageInputVal] = useState<string>(String(activeTargetPage));
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Sync internal active page when currentSlideNumber or propTargetPage changes
  useEffect(() => {
    const newPage = propTargetPage ?? slideLoc.primaryPage;
    setActivePage(newPage);
    setPageInputVal(String(newPage));
    onPageChange?.(newPage);
  }, [propTargetPage, slideLoc.primaryPage, currentSlideNumber]);

  // Check if local backend endpoint is reachable and has the PDF
  useEffect(() => {
    let active = true;
    const testLocalPdf = async () => {
      if (!pdfMeta?.fileName && !pdfMeta?.localFileName) return;
      const targetName = pdfMeta.localFileName || pdfMeta.fileName;
      try {
        const resp = await fetch(`/api/lecture-pdf/${encodeURIComponent(targetName)}`, {
          method: 'HEAD',
        });
        if (active) {
          if (resp.ok) {
            setIsLocalServerAvailable(true);
            setSourceType('local'); // Default to local for fast direct #page navigation
          } else {
            setIsLocalServerAvailable(false);
            setSourceType('drive');
          }
        }
      } catch {
        if (active) {
          setIsLocalServerAvailable(false);
          setSourceType('drive');
        }
      }
    };
    testLocalPdf();
    return () => {
      active = false;
    };
  }, [pdfMeta]);

  // Clean up object URL on unmount
  useEffect(() => {
    return () => {
      if (customFileUrl) {
        URL.revokeObjectURL(customFileUrl);
      }
    };
  }, [customFileUrl]);

  // Construct iframe URL based on selected source type & activePage
  const pdfUrl = useMemo(() => {
    if (sourceType === 'custom' && customFileUrl) {
      return `${customFileUrl}#page=${activePage}&zoom=${zoom}`;
    }
    if (sourceType === 'local' && (pdfMeta?.localFileName || pdfMeta?.fileName)) {
      const fn = pdfMeta.localFileName || pdfMeta.fileName;
      return `/api/lecture-pdf/${encodeURIComponent(fn)}#page=${activePage}&zoom=${zoom}`;
    }
    // Default: Google Drive Preview Embed
    if (pdfMeta?.fileId) {
      return `https://drive.google.com/file/d/${pdfMeta.fileId}/preview`;
    }
    return null;
  }, [sourceType, customFileUrl, pdfMeta, activePage, zoom]);

  // Direct download / open link
  const directLink = useMemo(() => {
    if (sourceType === 'custom' && customFileUrl) return customFileUrl;
    if (sourceType === 'local' && (pdfMeta?.localFileName || pdfMeta?.fileName)) {
      return `/api/lecture-pdf/${encodeURIComponent(pdfMeta.localFileName || pdfMeta.fileName)}#page=${activePage}`;
    }
    if (pdfMeta?.driveUrl) return pdfMeta.driveUrl;
    if (pdfMeta?.fileId) return `https://drive.google.com/file/d/${pdfMeta.fileId}/view`;
    return null;
  }, [sourceType, customFileUrl, pdfMeta, activePage]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (customFileUrl) URL.revokeObjectURL(customFileUrl);
    const objUrl = URL.createObjectURL(file);
    setCustomFileUrl(objUrl);
    setCustomFileName(file.name);
    setSourceType('custom');
    setIsLoading(true);
    setHasError(false);
  };

  const handleJumpToPage = (p: number) => {
    const safePage = Math.max(1, Math.min(slideLoc.totalPages || 300, p));
    setActivePage(safePage);
    setPageInputVal(String(safePage));
    onPageChange?.(safePage);
  };

  const handlePageInputSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const val = parseInt(pageInputVal, 10);
    if (!isNaN(val) && val > 0) {
      handleJumpToPage(val);
    }
  };

  // Generate range of buttons for the current slide mapping
  const rangePages = useMemo(() => {
    const [start, end] = activePageRange;
    const pages: number[] = [];
    const count = Math.min(6, end - start + 1);
    for (let p = start; p < start + count; p++) {
      pages.push(p);
    }
    return pages;
  }, [activePageRange]);

  const displayName = customFileName || pdfMeta?.fileName || `${deck.title}.pdf`;

  return (
    <div className={`flex flex-col h-full bg-slate-900 text-slate-100 select-none overflow-hidden ${compact ? 'rounded-xl border border-slate-800' : ''}`}>
      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        accept="application/pdf"
        onChange={handleFileUpload}
        className="hidden"
      />

      {/* Top Controls Toolbar */}
      <header className="shrink-0 bg-slate-950/95 border-b border-slate-800 px-3 py-2 flex items-center justify-between gap-2 flex-wrap text-[12px]">
        {/* Title & Document Badge */}
        <div className="flex items-center gap-2 min-w-0">
          <div className="w-7 h-7 rounded-lg bg-rose-500/20 text-rose-400 border border-rose-500/30 flex items-center justify-center shrink-0">
            <FileText className="w-4 h-4" />
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-1.5">
              <span className="font-semibold text-white truncate max-w-[200px] sm:max-w-xs md:max-w-md" title={displayName}>
                {displayName}
              </span>
              <span className="text-[11px] font-mono px-1.5 py-0.2 rounded bg-rose-500/10 text-rose-300 border border-rose-500/20 shrink-0">
                PDF
              </span>
            </div>
            {!compact && (
              <span className="text-[11px] text-slate-400 block truncate">
                {deck.discipline} · {deck.instructor || 'Karabük Tıp Fakültesi'}
              </span>
            )}
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-1.5 ml-auto">
          {/* Source switch pills */}
          <div className="hidden sm:inline-flex items-center bg-slate-900 border border-slate-800 rounded-lg p-0.5 text-[11px]">
            {isLocalServerAvailable && (
              <button
                type="button"
                onClick={() => {
                  setSourceType('local');
                  setIsLoading(true);
                }}
                className={`px-2 py-1 rounded-md cursor-pointer transition-colors flex items-center gap-1 ${
                  sourceType === 'local' ? 'bg-emerald-600 text-white font-medium shadow-xs' : 'text-slate-400 hover:text-white'
                }`}
                title="Yerel Bilgisayar Veritabanından Doğrudan Sayfa Senkronizasyonu"
              >
                <HardDrive className="w-3 h-3" />
                <span>Yerel</span>
              </button>
            )}
            {pdfMeta?.fileId && (
              <button
                type="button"
                onClick={() => {
                  setSourceType('drive');
                  setIsLoading(true);
                }}
                className={`px-2 py-1 rounded-md cursor-pointer transition-colors flex items-center gap-1 ${
                  sourceType === 'drive' ? 'bg-accent text-white font-medium shadow-xs' : 'text-slate-400 hover:text-white'
                }`}
                title="Google Drive Bulut Önizleyicisi"
              >
                <Cloud className="w-3 h-3" />
                <span>Drive</span>
              </button>
            )}
            {customFileUrl && (
              <button
                type="button"
                onClick={() => {
                  setSourceType('custom');
                  setIsLoading(true);
                }}
                className={`px-2 py-1 rounded-md cursor-pointer transition-colors flex items-center gap-1 ${
                  sourceType === 'custom' ? 'bg-purple-600 text-white font-medium shadow-xs' : 'text-slate-400 hover:text-white'
                }`}
                title="Yüklediğiniz Özel PDF"
              >
                <Upload className="w-3 h-3" />
                <span>Özel</span>
              </button>
            )}
          </div>

          {/* Upload Custom PDF Button */}
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            title="Bilgisayarınızdan başka bir slayt PDF'i seçip yükleyin"
            className="h-7 px-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-800 inline-flex items-center gap-1 cursor-pointer transition-colors text-[11px]"
          >
            <Upload className="w-3.5 h-3.5 text-accent" />
            <span className="hidden md:inline">PDF Seç</span>
          </button>

          {/* Zoom controls for local/custom mode */}
          {sourceType !== 'drive' && (
            <div className="hidden lg:flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg p-0.5 text-[11px]">
              <button
                type="button"
                onClick={() => setZoom((z) => Math.max(50, z - 15))}
                title="Uzaklaştır"
                className="w-6 h-6 flex items-center justify-center text-slate-400 hover:text-white rounded cursor-pointer"
              >
                <ZoomOut className="w-3 h-3" />
              </button>
              <span className="px-1 text-[11px] font-mono text-slate-300">{zoom}%</span>
              <button
                type="button"
                onClick={() => setZoom((z) => Math.min(200, z + 15))}
                title="Yakınlaştır"
                className="w-6 h-6 flex items-center justify-center text-slate-400 hover:text-white rounded cursor-pointer"
              >
                <ZoomIn className="w-3 h-3" />
              </button>
              <button
                type="button"
                onClick={() => setZoom(100)}
                title="Sıfırla"
                className="w-6 h-6 flex items-center justify-center text-slate-400 hover:text-white rounded cursor-pointer"
              >
                <RotateCcw className="w-3 h-3" />
              </button>
            </div>
          )}

          {/* Split view toggle */}
          {onToggleSplitView && (
            <button
              type="button"
              onClick={onToggleSplitView}
              title={isSplitView ? 'Sadece Slaytı Göster' : 'Yan Yana Bölünmüş Ekran'}
              className={`h-7 px-2 rounded-lg border inline-flex items-center gap-1 cursor-pointer transition-colors text-[11px] ${
                isSplitView
                  ? 'bg-accent/20 border-accent/40 text-accent font-semibold'
                  : 'bg-slate-900 hover:bg-slate-800 text-slate-300 border-slate-800'
              }`}
            >
              <Columns className="w-3.5 h-3.5" />
              <span className="hidden md:inline">{isSplitView ? 'Bölünmüş' : 'Yan Yana'}</span>
            </button>
          )}

          {/* Open in new window */}
          {directLink && (
            <a
              href={directLink}
              target="_blank"
              rel="noopener noreferrer"
              title="Orijinal PDF'i Yeni Sekmede Aç"
              className="h-7 px-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-800 inline-flex items-center gap-1 cursor-pointer transition-colors text-[11px]"
            >
              <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
              <span className="hidden sm:inline">Yeni Sekme</span>
            </a>
          )}

          {/* Close button if provided */}
          {onClose && (
            <button
              type="button"
              onClick={onClose}
              title="PDF Görüntüleyiciyi Kapat"
              className="w-7 h-7 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white border border-slate-800 flex items-center justify-center cursor-pointer transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>
      </header>

      {/* Synchronized Page Navigation Banner (İlişkilendirilmiş Sayfa Gezinme Çubuğu) */}
      <div className="shrink-0 bg-slate-950/80 border-b border-slate-800/80 px-3 py-1.5 flex items-center justify-between gap-2 flex-wrap text-[11px]">
        {/* Mapping info badge */}
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1 text-accent font-medium">
            <Compass className="w-3.5 h-3.5 animate-pulse" />
            <span>Slayt #{currentSlideNumber} Kaynağı:</span>
          </div>
          <span className="font-semibold text-amber-300 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-md">
            {slideLoc.citation}
          </span>
          <span className="text-slate-400 hidden md:inline">
            (Toplam {slideLoc.totalPages} sayfa)
          </span>
        </div>

        {/* Quick Jump Page Pills */}
        <div className="flex items-center gap-1.5 ml-auto">
          <div className="flex items-center gap-1">
            <button
              type="button"
              onClick={() => handleJumpToPage(activePage - 1)}
              disabled={activePage <= 1}
              title="Önceki Sayfa"
              className="w-6 h-6 rounded flex items-center justify-center bg-slate-900 border border-slate-800 text-slate-300 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
            </button>

            {/* Quick Range Buttons */}
            {rangePages.map((p) => (
              <button
                key={p}
                type="button"
                onClick={() => handleJumpToPage(p)}
                className={`px-2 py-0.5 rounded text-[11px] font-mono cursor-pointer transition-colors ${
                  activePage === p
                    ? 'bg-accent text-white font-bold shadow-xs'
                    : 'bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800/80'
                }`}
                title={`Sayfa ${p}'e git`}
              >
                S.{p}
              </button>
            ))}

            <button
              type="button"
              onClick={() => handleJumpToPage(activePage + 1)}
              disabled={activePage >= (slideLoc.totalPages || 300)}
              title="Sonraki Sayfa"
              className="w-6 h-6 rounded flex items-center justify-center bg-slate-900 border border-slate-800 text-slate-300 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer"
            >
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Direct Page Input */}
          <form onSubmit={handlePageInputSubmit} className="flex items-center gap-1 ml-1">
            <span className="text-slate-500 font-mono text-[11px]">S:</span>
            <input
              type="number"
              min="1"
              max={slideLoc.totalPages || 300}
              value={pageInputVal}
              onChange={(e) => setPageInputVal(e.target.value)}
              onBlur={() => {
                const val = parseInt(pageInputVal, 10);
                if (!isNaN(val) && val > 0) handleJumpToPage(val);
              }}
              className="w-11 h-6 bg-slate-900 border border-slate-700 rounded px-1 text-center font-mono text-[11px] text-white focus:outline-hidden focus:border-accent"
              title="Doğrudan sayfa numarası girip Enter'a basın"
            />
          </form>
        </div>
      </div>

      {/* Main Viewer Area */}
      <div className="relative flex-1 min-h-0 w-full bg-slate-950 flex items-center justify-center overflow-hidden">
        {/* Loading Spinner */}
        {isLoading && (
          <div className="absolute inset-0 z-10 flex flex-col items-center justify-center gap-3 bg-slate-950/80 backdrop-blur-xs text-slate-200">
            <RefreshCw className="w-8 h-8 text-accent animate-spin" />
            <p className="m-0 text-[13px] font-medium text-slate-300">
              Orijinal PDF hazırlanıyor (Sayfa {activePage})…
            </p>
            <span className="text-[11px] text-slate-500 font-mono">{displayName}</span>
          </div>
        )}

        {/* Main PDF iframe */}
        {pdfUrl && !hasError ? (
          <iframe
            key={`${pdfUrl}-${sourceType}-${activePage}`}
            src={pdfUrl}
            title={displayName}
            onLoad={() => setIsLoading(false)}
            onError={() => {
              setIsLoading(false);
              setHasError(true);
            }}
            className="w-full h-full border-0 bg-white"
            allow="autoplay; fullscreen"
          />
        ) : (
          <div className="flex flex-col items-center justify-center gap-3 p-6 text-center max-w-md text-slate-300">
            <div className="w-12 h-12 rounded-2xl bg-amber-500/20 text-amber-400 border border-amber-500/30 flex items-center justify-center">
              <AlertCircle className="w-6 h-6" />
            </div>
            <h3 className="m-0 text-[15px] font-bold text-white">PDF Sayfa İçinde Yüklenemedi</h3>
            <p className="m-0 text-[12px] text-slate-400 leading-relaxed">
              Tarayıcınızın üçüncü taraf çerez ayarları Google Drive önizleyicisini engellemiş olabilir veya yerel sunucu bağlantısı kapalıdır.
            </p>
            <div className="flex items-center gap-2 pt-2 flex-wrap justify-center">
              {directLink && (
                <a
                  href={directLink}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="h-9 px-4 rounded-xl bg-accent hover:bg-accent-hover text-white text-[13px] font-semibold inline-flex items-center gap-2 transition-colors shadow-xs"
                >
                  <ExternalLink className="w-4 h-4" />
                  <span>Google Drive'da Aç (Sayfa {activePage})</span>
                </a>
              )}
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="h-9 px-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-[13px] font-medium inline-flex items-center gap-2 transition-colors border border-slate-700"
              >
                <Upload className="w-4 h-4 text-accent" />
                <span>Yerel Dosyadan Seç</span>
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Footer Info Strip */}
      <footer className="shrink-0 bg-slate-950 border-t border-slate-800/80 px-3 py-1.5 flex items-center justify-between text-[11px] text-slate-400">
        <div className="flex items-center gap-2 truncate">
          <span className={`w-2 h-2 rounded-full shrink-0 ${sourceType === 'local' ? 'bg-emerald-400' : 'bg-accent'}`} />
          <span className="truncate">
            {sourceType === 'local'
              ? 'Yerel Amfi PDF Motoru (Sayfa Senkronizasyonu Aktif)'
              : sourceType === 'drive'
              ? 'Google Drive Bulut Önizleyicisi'
              : 'Özel Kullanıcı PDF Dokümanı'}
          </span>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <span className="font-mono text-slate-400">
            Aktif PDF Sayfası: <strong className="text-amber-400 font-bold">#{activePage}</strong> / {slideLoc.totalPages}
          </span>
        </div>
      </footer>
    </div>
  );
};
