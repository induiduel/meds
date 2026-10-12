/**
 * Öğren · dersin özgün slayt PDF'i. Sunucudaki dosya PDF.js ile uygulama içinde çizilir (PdfDocView, tembel);
 * sunucu yoksa Drive önizlemesi, o da yoksa kullanıcının kendi seçtiği dosya. Adımın kaynak sayfaları vurgulanır
 * ve adım değişince oraya kaydırılır. Deste → PDF eşlemesi: services/deckPdfService.ts.
 */
import React, { Suspense, lazy, useEffect, useMemo, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Columns2, ExternalLink, FileText, FileX, MapPin, Maximize2, Upload, ZoomIn, ZoomOut, X } from 'lucide-react';
import type { InteractiveDeck, SlideItem } from './InteractiveDeckView';
import { getSlidePdfLocation } from '../../services/slidePdfMappingService';
import { drivePreviewUrl, driveViewUrl, useDeckPdf, type DeckPdfFile } from '../../services/deckPdfService';
import './pdf/pdfDoc.css';

const PdfDocView = lazy(() => import('./pdf/PdfDocView'));

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

const fmtMb = (b?: number) => (b ? `${(b / 1048576).toFixed(b < 10485760 ? 1 : 0)} MB` : '');

export const DeckPdfViewer: React.FC<DeckPdfViewerProps> = ({
  deck,
  currentSlideNumber = 1,
  currentSlide,
  targetPage,
  targetPageRange,
  onClose,
  isSplitView = false,
  onToggleSplitView,
  compact = false,
  onPageChange,
}) => {
  const info = useDeckPdf(deck.id);
  // Kullanıcının sekmeyle seçtiği dosya yalnız o adım için geçerli
  const [picked, setPicked] = useState<{ deck: string; slide: number; idx: number } | null>(null);
  const [custom, setCustom] = useState<{ url: string; name: string } | null>(null);
  const [numPages, setNumPages] = useState<number | null>(null);
  const [failed, setFailed] = useState<string | null>(null);
  const [zoom, setZoom] = useState(1);
  const [frameReady, setFrameReady] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);

  useEffect(() => () => { if (custom) URL.revokeObjectURL(custom.url); }, [custom]);

  const loc = useMemo(
    () => getSlidePdfLocation(deck.id, currentSlideNumber, currentSlide, deck.slides?.length, custom ? undefined : info?.slides),
    [deck.id, currentSlideNumber, currentSlide, deck.slides?.length, info?.slides, custom],
  );
  // Ders birden çok PDF'e yayılıyorsa her adım kendi dosyasını açar; kullanıcı sekmeyle başka dosyaya geçebilir
  // (bir sonraki adımda yeniden adımın dosyasına dönülür).
  const slideFile = info?.slides ? (loc.fileIndex ?? 0) : 0;
  const fileIdx = picked && picked.deck === deck.id && picked.slide === currentSlideNumber ? picked.idx : slideFile;
  const setFileIdx = (idx: number) => setPicked({ deck: deck.id, slide: currentSlideNumber, idx });
  const mapped = fileIdx === slideFile;
  const range: [number, number] = targetPageRange && !info?.slides ? targetPageRange : loc.pageRange;
  const wanted = mapped ? (targetPage ?? loc.primaryPage) : 1;
  const clamp = (p: number) => Math.max(1, Math.min(numPages || 9999, p));

  // Görünen sayfa (kaydırınca güncellenir) ve hedef (adım değişince/düğmeyle)
  const [page, setPage] = useState(wanted);
  const [target, setTarget] = useState(wanted);
  const [pageInput, setPageInput] = useState(String(wanted));
  useEffect(() => {
    setTarget(wanted);
    setPage(wanted);
    setPageInput(String(wanted));
  }, [wanted, currentSlideNumber, fileIdx]);

  const file: DeckPdfFile | undefined = info?.files[fileIdx];
  const appSrc = custom?.url || file?.url;
  const driveId = !custom && !file?.url ? file?.fileId : undefined;
  const openHref = custom?.url || (file?.url ? `${file.url}#page=${page}` : file?.fileId ? driveViewUrl(file.fileId) : undefined);
  const name = custom?.name || file?.name || `${deck.title}.pdf`;

  useEffect(() => {
    setNumPages(null);
    setFailed(null);
    setFrameReady(false);
  }, [appSrc, driveId]);

  const jump = (p: number) => {
    const c = clamp(p);
    setTarget(c);
    setPage(c);
    setPageInput(String(c));
    onPageChange?.(c);
  };
  const onVisible = (p: number) => {
    setPage(p);
    setPageInput(String(p));
    onPageChange?.(p);
  };

  const pickFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    e.target.value = '';
    if (!f) return;
    setCustom({ url: URL.createObjectURL(f), name: f.name });
  };

  const inRange = page >= range[0] && page <= range[1];
  const subtitle = custom
    ? 'Cihazınızdan seçilen dosya'
    : file?.url
      ? [file?.folder, numPages ? `${numPages} sayfa` : file?.pages ? `${file.pages} sayfa` : '', fmtMb(file?.size)].filter(Boolean).join(' · ')
      : driveId
        ? 'Google Drive önizlemesi'
        : deck.discipline || '';

  let body: React.ReactNode;
  if (!info && !custom) {
    body = (
      <div className="pdv-loading" role="status" style={{ margin: 'auto', position: 'static' }}>
        <span className="pdv-spin" aria-hidden />
        <span>Ders PDF'i aranıyor…</span>
      </div>
    );
  } else if (appSrc && !failed) {
    body = (
      <Suspense fallback={<div className="pdv-loading" role="status" style={{ margin: 'auto', position: 'static' }}><span className="pdv-spin" aria-hidden /><span>Görüntüleyici yükleniyor…</span></div>}>
        <PdfDocView
          src={appSrc}
          page={target}
          highlight={custom || !mapped ? undefined : range}
          zoom={zoom}
          onZoom={setZoom}
          onVisiblePage={onVisible}
          onLoaded={setNumPages}
          onError={setFailed}
        />
      </Suspense>
    );
  } else if (appSrc && failed) {
    // PDF.js açamadıysa (eski tarayıcı vb.) tarayıcının kendi görüntüleyicisi
    body = <iframe key={`${appSrc}#${target}`} className="dpv-frame" src={`${appSrc}#page=${target}`} title={name} />;
  } else if (driveId) {
    body = (
      <>
        {!frameReady && (
          <div className="pdv-loading" role="status" style={{ position: 'absolute', top: '40%', left: '50%', transform: 'translateX(-50%)' }}>
            <span className="pdv-spin" aria-hidden />
            <span>Drive önizlemesi açılıyor…</span>
          </div>
        )}
        <iframe key={driveId} className="dpv-frame" src={drivePreviewUrl(driveId)} title={name} allow="autoplay; fullscreen" onLoad={() => setFrameReady(true)} style={frameReady ? undefined : { opacity: 0 }} />
      </>
    );
  } else {
    const when = info?.missingDate ? new Date(`${info.missingDate}T12:00:00`) : null;
    const upcoming = when ? when.getTime() > Date.now() : false;
    const dateTxt = when ? when.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' }) : '';
    body = (
      <div className="dpv-empty">
        <FileX aria-hidden />
        <h3>{file ? 'PDF dosyasına şu an ulaşılamıyor' : "Bu dersin slayt PDF'i Drive'da henüz yok"}</h3>
        <p>
          {file
            ? `${file.name} sunucuda bulunamadı. Drive eşitlemesinden sonra yeniden açılır.`
            : when
              ? upcoming
                ? `Ders ${dateTxt} tarihinde. Hocanın slaytı Drive'daki 2026-27 klasörüne yüklenince burada kendiliğinden açılır.`
                : `Ders ${dateTxt} tarihinde işlendi ama slaytı Drive'daki 2026-27 klasöründe yok. Yüklendiğinde burada kendiliğinden açılır.`
              : "Slayt Drive'daki 2026-27 klasörüne yüklendiğinde burada kendiliğinden açılır."}{' '}
          Elinizde varsa kendi dosyanızı açabilirsiniz.
        </p>
        <div className="dpv-row">
          <button type="button" className="dpv-btn is-primary" onClick={() => fileInput.current?.click()}>
            <Upload aria-hidden /> PDF seç
          </button>
        </div>
      </div>
    );
  }

  const canNav = !!appSrc && !failed;
  const byFolder = !!info && new Set(info.files.map((f) => f.folder)).size === info.files.length;

  return (
    <div className={`dpv${compact ? ' is-compact' : ''}`}>
      <input ref={fileInput} type="file" accept="application/pdf,.pdf" onChange={pickFile} hidden />

      <header className="dpv-bar">
        <div className="dpv-title">
          <FileText aria-hidden />
          <div style={{ minWidth: 0 }}>
            <b title={name}>{name.replace(/\.pdf$/i, '')}</b>
            {subtitle && <small>{subtitle}</small>}
          </div>
        </div>
        <div className="dpv-acts">
          {custom && (
            <button type="button" className="dpv-ib" onClick={() => setCustom(null)} title="Dersin kendi PDF'ine dön">
              <X aria-hidden /><span className="dpv-lbl">Seçimi kapat</span>
            </button>
          )}
          <button type="button" className="dpv-ib" onClick={() => fileInput.current?.click()} title="Cihazınızdan başka bir PDF açın">
            <Upload aria-hidden /><span className="dpv-lbl">PDF seç</span>
          </button>
          {onToggleSplitView && (
            <button type="button" className={`dpv-ib${isSplitView ? ' is-on' : ''}`} onClick={onToggleSplitView} title={isSplitView ? 'Yalnız PDF' : 'Ders ile yan yana'} aria-pressed={isSplitView}>
              {isSplitView ? <Maximize2 aria-hidden /> : <Columns2 aria-hidden />}
              <span className="dpv-lbl">{isSplitView ? 'Tam PDF' : 'Yan yana'}</span>
            </button>
          )}
          {openHref && (
            <a className="dpv-ib" href={openHref} target="_blank" rel="noopener noreferrer" title="PDF'i yeni sekmede aç">
              <ExternalLink aria-hidden /><span className="dpv-lbl">Yeni sekme</span>
            </a>
          )}
          {onClose && (
            <button type="button" className="dpv-ib" onClick={onClose} title="Kapat" aria-label="PDF görüntüleyiciyi kapat">
              <X aria-hidden />
            </button>
          )}
        </div>
      </header>

      {(canNav || (info && info.files.length > 1)) && (
        <div className="dpv-nav">
          {canNav && (
            <>
              <button type="button" className="dpv-ib" onClick={() => jump(page - 1)} disabled={page <= 1} aria-label="Önceki sayfa"><ChevronLeft aria-hidden /></button>
              <form
                className="dpv-pg"
                onSubmit={(e) => {
                  e.preventDefault();
                  const v = parseInt(pageInput, 10);
                  if (v > 0) jump(v);
                }}
              >
                <input
                  inputMode="numeric"
                  value={pageInput}
                  onChange={(e) => setPageInput(e.target.value.replace(/\D/g, ''))}
                  onBlur={() => setPageInput(String(page))}
                  aria-label="Sayfa numarası"
                />
                <span>/ {numPages ?? '…'}</span>
              </form>
              <button type="button" className="dpv-ib" onClick={() => jump(page + 1)} disabled={!!numPages && page >= numPages} aria-label="Sonraki sayfa"><ChevronRight aria-hidden /></button>
              {!custom && mapped && (
                <button type="button" className={`dpv-src${inRange ? ' is-here' : ''}`} onClick={() => jump(range[0])} title={`Adım ${currentSlideNumber} bu sayfalardan anlatılıyor`}>
                  <MapPin aria-hidden />
                  Adım {currentSlideNumber}: {range[0] === range[1] ? `s. ${range[0]}` : `s. ${range[0]}–${range[1]}`}
                </button>
              )}
            </>
          )}
          {!custom && info && info.files.length > 1 && (
            <div className="dpv-files" role="tablist" aria-label="Ders PDF'leri">
              {info.files.map((f, i) => {
                // Dosyalar farklı ders dallarındaysa (ör. Üroloji / Enfeksiyon Hastalıkları) sekmede dal adı gösterilir
                const label = byFolder && f.folder ? f.folder : f.name.replace(/\.pdf$/i, '').replace(/^\s*\d+\s*\)\s*/, '');
                return (
                  <button key={`${f.folder}/${f.name}`} type="button" role="tab" aria-selected={i === fileIdx} className={`dpv-file${i === fileIdx ? ' is-on' : ''}`} onClick={() => setFileIdx(i)} title={f.folder ? `${f.folder} · ${f.name}` : f.name}>
                    {label}
                  </button>
                );
              })}
            </div>
          )}
          {canNav && (
            <div className="dpv-zoom">
              <button type="button" className="dpv-ib" onClick={() => setZoom((z) => Math.max(0.5, Math.round((z - 0.15) * 100) / 100))} aria-label="Uzaklaştır"><ZoomOut aria-hidden /></button>
              <button type="button" className="dpv-ib" onClick={() => setZoom(1)} title="Genişliğe sığdır"><span>%{Math.round(zoom * 100)}</span></button>
              <button type="button" className="dpv-ib" onClick={() => setZoom((z) => Math.min(3, Math.round((z + 0.15) * 100) / 100))} aria-label="Yakınlaştır"><ZoomIn aria-hidden /></button>
            </div>
          )}
        </div>
      )}

      <div className="dpv-body">{body}</div>
    </div>
  );
};
