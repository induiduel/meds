/**
 * Öğren · dersin özgün slayt PDF'i. Sunucudaki dosya PDF.js ile uygulama içinde çizilir (PdfDocView, tembel);
 * sunucu yoksa Drive önizlemesi, o da yoksa kullanıcının kendi seçtiği dosya. Adımın kaynak sayfaları vurgulanır
 * ve adım değişince oraya kaydırılır. Deste → PDF eşlemesi: services/deckPdfService.ts.
 */
import React, { Suspense, lazy, useEffect, useMemo, useRef, useState } from 'react';
import {
  ChevronDown, ChevronLeft, ChevronRight, ChevronUp, Columns2, Download, ExternalLink, FileText, FileX, MapPin, Maximize, Maximize2, Minimize, Moon, MoreHorizontal,
  CloudDownload, CloudOff, MoveHorizontal, MoveVertical, PanelLeft, RotateCw, Search, Upload, ZoomIn, ZoomOut, X,
} from 'lucide-react';
import type { InteractiveDeck, SlideItem } from './InteractiveDeckView';
import { getSlidePdfLocation } from '../../services/slidePdfMappingService';
import { drivePreviewUrl, driveViewUrl, useDeckPdf, type DeckPdfFile } from '../../services/deckPdfService';
import { PDF_SAVED_EVENT, removeSavedPdf, savePdfOffline, savedPdfObjectUrl } from '../../services/deviceStorage';
import { isIosWebKit, wasRecentlyScrollingOrTouching } from '../../utils/fullscreen';
import { toast } from '../ui/Toast';
import './pdf/pdfDoc.css';

const PdfDocView = lazy(() => import('./pdf/PdfDocView'));
type SearchState = { hits: import('./pdf/PdfDocView').PdfSearchHit[]; done: boolean } | null;

/** Görüntüleme tercihleri cihazda saklanır */
const PREF_KEY = 'medsoru_pdf_view';
interface ViewPrefs {
  fit: 'width' | 'page';
  thumbs: boolean;
  night: boolean;
  /** Başlık şeridi (ad · Tam PDF · Tam ekran) gizli */
  hideBar: boolean;
}
const loadPrefs = (): ViewPrefs => {
  const d: ViewPrefs = { fit: 'width', thumbs: false, night: false, hideBar: false };
  try {
    return { ...d, ...JSON.parse(localStorage.getItem(PREF_KEY) || '{}') };
  } catch {
    return d;
  }
};
const ZOOM_MIN = 0.5;
const ZOOM_MAX = 4;
const ZOOM_STEPS = [0.5, 0.75, 1, 1.25, 1.5, 2, 3, 4];
const nextZoom = (z: number, dir: 1 | -1) =>
  dir > 0 ? ZOOM_STEPS.find((s) => s > z + 0.01) ?? ZOOM_MAX : [...ZOOM_STEPS].reverse().find((s) => s < z - 0.01) ?? ZOOM_MIN;

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
  /** Görünen sayfa değişince (dosya sırası: deckPdfService; userScroll: kullanıcı kaydırdı/atladı) */
  onPageChange?: (page: number, fileIndex: number, userScroll?: boolean) => void;
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
  const rootRef = useRef<HTMLDivElement>(null);
  const [prefs, setPrefs] = useState<ViewPrefs>(loadPrefs);
  const setPref = <K extends keyof ViewPrefs>(k: K, v: ViewPrefs[K]) =>
    setPrefs((p) => {
      const n = { ...p, [k]: v };
      try {
        localStorage.setItem(PREF_KEY, JSON.stringify(n));
      } catch {
        /* ignore */
      }
      return n;
    });
  const [rotation, setRotation] = useState(0);
  const [moreOpen, setMoreOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [debounced, setDebounced] = useState('');
  const [search, setSearch] = useState<SearchState>(null);
  const [hitIdx, setHitIdx] = useState(0);
  const searchInput = useRef<HTMLInputElement>(null);
  useEffect(() => {
    const t = window.setTimeout(() => setDebounced(searchOpen ? query : ''), 280);
    return () => window.clearTimeout(t);
  }, [query, searchOpen]);
  useEffect(() => setHitIdx(0), [debounced]);

  /* --- tam ekran: görüntüleyicinin kendisi; API yoksa ya da iOS/iPadOS ise ekranı kaplayan katman --- */
  const [isFs, setIsFs] = useState(false);
  const [maxed, setMaxed] = useState(false);
  const hadNativeFsRef = useRef(false);
  useEffect(() => {
    const on = () => {
      const fs = ((document as any).fullscreenElement || (document as any).webkitFullscreenElement) === rootRef.current && !!rootRef.current;
      setIsFs(fs);
      if (fs) {
        hadNativeFsRef.current = true;
      } else if (hadNativeFsRef.current) {
        hadNativeFsRef.current = false;
        if (isIosWebKit() || wasRecentlyScrollingOrTouching()) {
          setMaxed(true);
        }
      }
    };
    document.addEventListener('fullscreenchange', on);
    document.addEventListener('webkitfullscreenchange', on);
    return () => {
      document.removeEventListener('fullscreenchange', on);
      document.removeEventListener('webkitfullscreenchange', on);
    };
  }, []);
  const fsOn = isFs || maxed;
  const toggleFs = () => {
    const d = document as any;
    if (maxed) {
      setMaxed(false);
      if (isFs) {
        hadNativeFsRef.current = false;
        (d.exitFullscreen || d.webkitExitFullscreen)?.call(d)?.catch?.(() => {});
      }
      return;
    }
    if (isFs) {
      hadNativeFsRef.current = false;
      (d.exitFullscreen || d.webkitExitFullscreen)?.call(d)?.catch?.(() => {});
      return;
    }
    const el: any = rootRef.current;
    const req = !isIosWebKit() && (el?.requestFullscreen || el?.webkitRequestFullscreen);
    if (!req) return setMaxed(true);
    // İstek reddedilir ya da yanıtsız kalırsa (gömülü görünümler) ekranı kaplayan katmana geçilir
    let settled = false;
    try {
      const pr = req.call(el, { navigationUI: 'hide' });
      pr?.then?.(() => (settled = true), () => {
        settled = true;
        setMaxed(true);
      });
    } catch {
      setMaxed(true);
      return;
    }
    window.setTimeout(() => {
      if (!settled && !d.fullscreenElement && !d.webkitFullscreenElement) setMaxed(true);
    }, 1500);
  };
  // Katman modunda Esc yalnız katmanı kapatsın (dersi değil)
  useEffect(() => {
    if (!maxed) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== 'Escape') return;
      e.stopImmediatePropagation();
      e.preventDefault();
      setMaxed(false);
    };
    window.addEventListener('keydown', onKey, true);
    return () => window.removeEventListener('keydown', onKey, true);
  }, [maxed]);

  // Menü dışına tıklayınca kapanır
  useEffect(() => {
    if (!moreOpen) return;
    const off = (e: PointerEvent) => {
      if (!(e.target as HTMLElement).closest?.('.dpv-more')) setMoreOpen(false);
    };
    document.addEventListener('pointerdown', off);
    return () => document.removeEventListener('pointerdown', off);
  }, [moreOpen]);

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
  // Çevrimdışı için indirilmiş kopya: varsa görüntüleyici cihazdan (blob) açar
  const [offline, setOffline] = useState<{ src: string; url: string } | null>(null);
  const [saving, setSaving] = useState(false);
  useEffect(() => {
    const u = file?.url;
    let alive = true;
    let made: string | null = null;
    const check = () => {
      if (!u) return setOffline(null);
      void savedPdfObjectUrl(u).then((b) => {
        if (!alive) { if (b) URL.revokeObjectURL(b); return; }
        made = b;
        setOffline((prev) => {
          if (prev && prev.url === u && b) { URL.revokeObjectURL(b); made = prev.src; return prev; }
          return b ? { src: b, url: u } : null;
        });
      });
    };
    check();
    window.addEventListener(PDF_SAVED_EVENT, check);
    return () => {
      alive = false;
      window.removeEventListener(PDF_SAVED_EVENT, check);
      if (made) URL.revokeObjectURL(made);
    };
  }, [file?.url]);
  const isSaved = !!offline && offline.url === file?.url;
  const toggleOffline = async () => {
    if (!file?.url || saving) return;
    setSaving(true);
    try {
      if (isSaved) {
        await removeSavedPdf(file.url);
        toast.success('PDF cihazdan kaldırıldı.');
      } else {
        await savePdfOffline(file.url);
        toast.success('PDF çevrimdışı kullanım için indirildi.');
      }
    } catch {
      toast.error('PDF indirilemedi', 'Bağlantını kontrol edip tekrar dene.');
    } finally {
      setSaving(false);
    }
  };
  const appSrc = custom?.url || (isSaved ? offline!.src : file?.url);
  const driveId = !custom && !file?.url ? file?.fileId : undefined;
  const openHref = custom?.url || (file?.url ? `${file.url}#page=${page}` : file?.fileId ? driveViewUrl(file.fileId) : undefined);
  const name = custom?.name || file?.name || `${deck.title}.pdf`;

  useEffect(() => {
    setNumPages(null);
    setFailed(null);
    setFrameReady(false);
    setSearch(null);
  }, [appSrc, driveId]);
  const downloadHref = custom?.url || file?.url;

  const jump = (p: number) => {
    const c = clamp(p);
    setTarget(c);
    setPage(c);
    setPageInput(String(c));
    onPageChange?.(c, fileIdx, true);
  };
  const onVisible = (p: number) => {
    setPage(p);
    setPageInput(String(p));
    onPageChange?.(p, fileIdx, true);
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
      ? [file?.folder, numPages ? `${numPages} sayfa` : file?.pages ? `${file.pages} sayfa` : '', fmtMb(file?.size), isSaved ? 'cihazda' : ''].filter(Boolean).join(' · ')
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
          fit={prefs.fit}
          rotation={rotation}
          thumbs={prefs.thumbs}
          query={debounced}
          onSearch={setSearch}
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
  const hits = search?.hits ?? [];
  const goHit = (i: number) => {
    if (!hits.length) return;
    const k = (i + hits.length) % hits.length;
    setHitIdx(k);
    jump(hits[k].page);
  };
  const openSearch = () => {
    setSearchOpen(true);
    window.setTimeout(() => searchInput.current?.select(), 0);
  };

  // Görüntüleyici içindeyken kısayollar (dersin ok tuşları değişmez)
  const onKeyDown = (e: React.KeyboardEvent) => {
    const t = e.target as HTMLElement;
    if (t.closest('input, textarea, select, [contenteditable="true"]')) return;
    if (e.altKey) return;
    const mod = e.ctrlKey || e.metaKey;
    let handled = true;
    if (mod && e.key.toLowerCase() === 'f' && canNav) openSearch();
    else if (mod) handled = false;
    else if ((e.key === '+' || e.key === '=') && canNav) setZoom((z) => nextZoom(z, 1));
    else if (e.key === '-' && canNav) setZoom((z) => nextZoom(z, -1));
    else if (e.key === '0' && canNav) setZoom(1);
    else if (e.key.toLowerCase() === 'f') toggleFs();
    else if (e.key.toLowerCase() === 'r' && canNav) setRotation((r) => (r + 90) % 360);
    else if (e.key === 'PageDown' && canNav) jump(page + 1);
    else if (e.key === 'PageUp' && canNav) jump(page - 1);
    else handled = false;
    if (handled) {
      e.preventDefault();
      e.stopPropagation();
    }
  };

  const zoomPct = Math.round(zoom * 100);

  return (
    <div
      ref={rootRef}
      className={`dpv${compact ? ' is-compact' : ''}${maxed ? ' is-max' : ''}${prefs.night ? ' is-night' : ''}`}
      onKeyDown={onKeyDown}
      role={maxed ? 'dialog' : undefined}
      aria-modal={maxed || undefined}
      aria-label={maxed ? 'PDF tam ekran' : undefined}
    >
      <input ref={fileInput} type="file" accept="application/pdf,.pdf" onChange={pickFile} hidden />

      {prefs.hideBar ? (
        <button type="button" className="dpv-bar-show" onClick={() => setPref('hideBar', false)} title="Başlığı göster" aria-label="PDF başlığını göster">
          <ChevronDown aria-hidden />
        </button>
      ) : (
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
          {canNav && (
            <button type="button" className={`dpv-ib${searchOpen ? ' is-on' : ''}`} onClick={() => (searchOpen ? setSearchOpen(false) : openSearch())} title="PDF'te ara (Ctrl+F)" aria-pressed={searchOpen}>
              <Search aria-hidden />
            </button>
          )}
          {onToggleSplitView && !fsOn && (
            <button type="button" className={`dpv-ib${isSplitView ? ' is-on' : ''}`} onClick={onToggleSplitView} title={isSplitView ? 'PDF tüm alanı kaplasın' : 'Ders ile yan yana'} aria-pressed={isSplitView}>
              {isSplitView ? <Maximize2 aria-hidden /> : <Columns2 aria-hidden />}
              <span className="dpv-lbl">{isSplitView ? 'Tam PDF' : 'Yan yana'}</span>
            </button>
          )}
          <button type="button" className={`dpv-ib${fsOn ? ' is-on' : ''}`} onClick={toggleFs} title={fsOn ? 'Tam ekrandan çık (Esc)' : 'Tam ekran (F)'} aria-pressed={fsOn}>
            {fsOn ? <Minimize aria-hidden /> : <Maximize aria-hidden />}
            <span className="dpv-lbl">{fsOn ? 'Küçült' : 'Tam ekran'}</span>
          </button>
          <button type="button" className="dpv-ib" onClick={() => { setMoreOpen(false); setPref('hideBar', true); }} title="Başlığı gizle" aria-label="PDF başlığını gizle">
            <ChevronUp aria-hidden />
          </button>
          <div className="dpv-more">
            <button type="button" className={`dpv-ib${moreOpen ? ' is-on' : ''}`} onClick={() => setMoreOpen((v) => !v)} aria-haspopup="menu" aria-expanded={moreOpen} title="Diğer ayarlar">
              <MoreHorizontal aria-hidden />
            </button>
            {moreOpen && (
              <div className="dpv-menu" role="menu">
                {canNav && (
                  <>
                    <span className="dpv-menu-h">Görünüm</span>
                    <div className="dpv-seg" role="radiogroup" aria-label="Sığdırma">
                      <button type="button" role="radio" aria-checked={prefs.fit === 'width'} onClick={() => { setPref('fit', 'width'); setZoom(1); }}>
                        <MoveHorizontal aria-hidden /> Genişliğe
                      </button>
                      <button type="button" role="radio" aria-checked={prefs.fit === 'page'} onClick={() => { setPref('fit', 'page'); setZoom(1); }}>
                        <MoveVertical aria-hidden /> Sayfaya
                      </button>
                    </div>
                    <button type="button" role="menuitemcheckbox" aria-checked={prefs.thumbs} className="dpv-mi" onClick={() => setPref('thumbs', !prefs.thumbs)}>
                      <PanelLeft aria-hidden /> Sayfa önizlemeleri<span className="dpv-tog" />
                    </button>
                    <button type="button" role="menuitemcheckbox" aria-checked={prefs.night} className="dpv-mi" onClick={() => setPref('night', !prefs.night)}>
                      <Moon aria-hidden /> Gece okuması<span className="dpv-tog" />
                    </button>
                    <button type="button" role="menuitem" className="dpv-mi" onClick={() => setRotation((r) => (r + 90) % 360)}>
                      <RotateCw aria-hidden /> Döndür{rotation ? ` · ${rotation}°` : ''}<kbd>R</kbd>
                    </button>
                    <span className="dpv-menu-sep" />
                  </>
                )}
                <button type="button" role="menuitem" className="dpv-mi" onClick={() => { setMoreOpen(false); fileInput.current?.click(); }}>
                  <Upload aria-hidden /> Cihazdan PDF aç
                </button>
                {!custom && file?.url && (
                  <button type="button" role="menuitem" className="dpv-mi" disabled={saving} onClick={() => { setMoreOpen(false); void toggleOffline(); }}>
                    {isSaved ? <><CloudOff aria-hidden /> Cihazdan kaldır</> : <><CloudDownload aria-hidden /> {saving ? 'İndiriliyor…' : 'Çevrimdışı için indir'}</>}
                  </button>
                )}
                {downloadHref && (
                  <a role="menuitem" className="dpv-mi" href={downloadHref} download={name} onClick={() => setMoreOpen(false)}>
                    <Download aria-hidden /> İndir
                  </a>
                )}
                {openHref && (
                  <a role="menuitem" className="dpv-mi" href={openHref} target="_blank" rel="noopener noreferrer" onClick={() => setMoreOpen(false)}>
                    <ExternalLink aria-hidden /> Yeni sekmede aç
                  </a>
                )}
                {canNav && (
                  <p className="dpv-menu-k">
                    <kbd>+</kbd><kbd>−</kbd> yakınlaştır · <kbd>0</kbd> sıfırla · <kbd>F</kbd> tam ekran · <kbd>Ctrl</kbd>+<kbd>F</kbd> ara · Ctrl+tekerlek yakınlaştırır
                  </p>
                )}
              </div>
            )}
          </div>
          {onClose && !fsOn && (
            <button type="button" className="dpv-ib" onClick={onClose} title="Kapat" aria-label="PDF görüntüleyiciyi kapat">
              <X aria-hidden />
            </button>
          )}
        </div>
      </header>
      )}

      {searchOpen && canNav && (
        <div className="dpv-search">
          <form
            className="dpv-search-f"
            onSubmit={(e) => {
              e.preventDefault();
              // İlk Enter geçerli eşleşmeye, sonrakiler bir sonrakine
              goHit(hits[hitIdx] && hits[hitIdx].page !== page ? hitIdx : hitIdx + 1);
            }}
          >
            <Search aria-hidden />
            <input
              ref={searchInput}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Escape') {
                  e.stopPropagation();
                  e.preventDefault();
                  setSearchOpen(false);
                } else if (e.key === 'Enter' && e.shiftKey) {
                  e.preventDefault();
                  goHit(hitIdx - 1);
                }
              }}
              placeholder="PDF'te ara…"
              aria-label="PDF'te ara"
              autoFocus
            />
            <span className="dpv-search-n" aria-live="polite">
              {debounced.trim().length < 2 ? '' : !search ? 'aranıyor…' : hits.length ? `${Math.min(hitIdx + 1, hits.length)}/${hits.length} sayfa${search.done ? '' : '…'}` : search.done ? 'bulunamadı' : 'aranıyor…'}
            </span>
            <button type="button" className="dpv-ib" onClick={() => goHit(hitIdx - 1)} disabled={!hits.length} aria-label="Önceki eşleşme"><ChevronLeft aria-hidden /></button>
            <button type="submit" className="dpv-ib" disabled={!hits.length} aria-label="Sonraki eşleşme"><ChevronRight aria-hidden /></button>
            <button type="button" className="dpv-ib" onClick={() => setSearchOpen(false)} aria-label="Aramayı kapat"><X aria-hidden /></button>
          </form>
          {hits.length > 0 && (
            <ul className="dpv-hits" aria-label="Eşleşen sayfalar">
              {hits.map((h, i) => (
                <li key={h.page}>
                  <button type="button" className={i === hitIdx ? 'is-on' : ''} onClick={() => { setHitIdx(i); jump(h.page); }}>
                    <b>s. {h.page}</b>
                    <span>{h.snippet}</span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

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
                  onFocus={(e) => e.target.select()}
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
              <button type="button" className={`dpv-ib${prefs.thumbs ? ' is-on' : ''}`} onClick={() => setPref('thumbs', !prefs.thumbs)} title="Sayfa önizlemeleri" aria-pressed={prefs.thumbs}><PanelLeft aria-hidden /></button>
              <button type="button" className="dpv-ib" onClick={() => setPref('fit', prefs.fit === 'width' ? 'page' : 'width')} title={prefs.fit === 'width' ? 'Sayfanın tamamını göster' : 'Genişliğe sığdır'}>
                {prefs.fit === 'width' ? <MoveVertical aria-hidden /> : <MoveHorizontal aria-hidden />}
              </button>
              <button type="button" className="dpv-ib" onClick={() => setZoom((z) => nextZoom(z, -1))} disabled={zoom <= ZOOM_MIN} aria-label="Uzaklaştır (−)"><ZoomOut aria-hidden /></button>
              <select className="dpv-zsel" value={ZOOM_STEPS.includes(zoom) ? String(zoom) : 'x'} onChange={(e) => setZoom(Number(e.target.value))} aria-label="Yakınlaştırma" title={prefs.fit === 'width' ? 'Genişliğe göre' : 'Sayfaya göre'}>
                {!ZOOM_STEPS.includes(zoom) && <option value="x">%{zoomPct}</option>}
                {ZOOM_STEPS.map((z) => (
                  <option key={z} value={z}>%{Math.round(z * 100)}</option>
                ))}
              </select>
              <button type="button" className="dpv-ib" onClick={() => setZoom((z) => nextZoom(z, 1))} disabled={zoom >= ZOOM_MAX} aria-label="Yakınlaştır (+)"><ZoomIn aria-hidden /></button>
            </div>
          )}
        </div>
      )}

      <div className="dpv-body">{body}</div>
    </div>
  );
};
