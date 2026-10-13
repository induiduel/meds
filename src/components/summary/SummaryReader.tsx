import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowRight,
  ArrowUp,
  BookOpenCheck,
  ChevronDown,
  ChevronUp,
  Clock,
  Copy,
  Expand,
  FileQuestion,
  FileText,
  GraduationCap,
  ListTree,
  Printer,
  RotateCcw,
  Search,
  Shrink,
  Table2,
  Target,
  X,
  Zap,
} from 'lucide-react';
import type { SummaryDetail, SummaryMeta } from '../LectureSummariesView';
import { parseSummary, type Block, type Section } from './parseSummary';
import { formatInline } from './inlineFormat';
import { RichList } from './RichList';
import { Callout, DataTable, Objectives, QuestionCard, SpotWall } from './ReaderBlocks';
import { markReading, useReaderPrefs, useReadingProgress, type Measure } from './readerStore';
import { HighlighterToolbar, Highlightable } from '../ui/Highlighter';
import { Segmented, Switch } from '../ui/kit';
import { Sheet } from '../ui/Sheet';
import { toast } from '../ui/Toast';
import { MODE_LABELS, useAppearance, type ThemeMode } from '../../utils/appearance';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import { disciplineClass, disciplineLabel } from '../../utils/discipline';
import { driveViewUrl, resolveDeckPdf, type DeckPdfInfo } from '../../services/deckPdfService';
import { ReaderPanel, useLessonSpots, useScopeMarks, type ScopeMark } from './ReaderPanel';

/**
 * Ders özeti okuyucusu (v10 kompakt). Uygulamanın temasını ve paletini kullanır — ayrı okuyucu teması yok;
 * Aa panelindeki tema düğmesi tüm uygulamanın temasını değiştirir. Masaüstünde uygulamanın kenar menüsü açık kalır
 * (okuyucu --sh-side-w kadar sağdan başlar). Yapı:
 *   ince üst çubuk (kapat · içindekiler · başlık/etkin bölüm · ara · kalem · Aa) + ilerleme çizgisi
 *   ≥1024: sol içindekiler rayı (kırıntı, ders adı, bölümler, "Okuma: 6 / 14 dk") · dar ekranda alt sayfa
 *   orta okuma sütunu (~660 px, 16/1.7): araç satırı (A− / A+ · Slayt PDF'i) → kapak → bölümler → bitiş kartı
 *   ≥1180: sağ panel (Spotlar · n / Notlarım · n); daha dar ekranda ve akış düzeninde makalenin altında.
 * html[data-layout="akis"]: yalnız okuma sütunu (raylar kapanır; içindekiler alt sayfadan).
 * Hareket: açılış/kapanış kayması, bölümler görünür oldukça yükselir, ilerleme çizgisi, çözüm kayarak açılır.
 * prefers-reduced-motion'da hepsi kapanır. Stil: styles/summary.css (.sr-*).
 */

interface Props {
  summary: SummaryDetail;
  onClose: () => void;
  onOpenPdfModal?: () => void;
  /** Listede sıradaki özet (bitiş kartında) */
  next?: SummaryMeta;
  onOpenNext?: () => void;
}

const KIND_TITLE: Partial<Record<Section['kind'], string>> = {
  objectives: 'Öğrenim hedefleri',
  spot: 'Hızlı tekrar',
  questions: 'Çıkmış sorular',
};
const secTitle = (s: Section) => KIND_TITLE[s.kind] || s.title;

const SecMark: React.FC<{ s: Section; i: number }> = ({ s, i }) =>
  s.kind === 'objectives' ? <Target aria-hidden /> : s.kind === 'spot' ? <Zap aria-hidden /> : s.kind === 'questions' ? <FileQuestion aria-hidden /> : <>{String(s.number || i + 1).padStart(2, '0')}</>;

const MEASURES: { value: Measure; label: string }[] = [
  { value: 'narrow', label: 'Dar' },
  { value: 'normal', label: 'Normal' },
  { value: 'wide', label: 'Geniş' },
];
const MODES: ThemeMode[] = ['light', 'sepia', 'dark'];

const reduceMotion = () => typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
const isTyping = (t: EventTarget | null) => t instanceof HTMLElement && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName));

export const SummaryReader: React.FC<Props> = ({ summary, onClose, onOpenPdfModal, next, onOpenNext }) => {
  const [prefs, setPrefs] = useReaderPrefs();
  const appearance = useAppearance();
  const progressMap = useReadingProgress();
  const doc = useMemo(() => parseSummary(summary.content || ''), [summary.content]);
  const ready = !!summary.content;

  const rootRef = useRef<HTMLDivElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const [closing, setClosing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [activeSec, setActiveSec] = useState('');
  const [activeSub, setActiveSub] = useState('');
  const [railMq, setRailMq] = useState(() => typeof window !== 'undefined' && window.matchMedia('(min-width: 1024px)').matches);
  const [panelMq, setPanelMq] = useState(() => typeof window !== 'undefined' && window.matchMedia('(min-width: 1180px)').matches);
  const akis = appearance.layout === 'akis';
  const wide = railMq && !akis;
  const panelSide = panelMq && !akis;
  const [sideOpen, setSideOpen] = useState(true);
  const [tocSheet, setTocSheet] = useState(false);
  const [aaOpen, setAaOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [hits, setHits] = useState<HTMLElement[]>([]);
  const [hitIdx, setHitIdx] = useState(0);
  const [picked, setPicked] = useState<Record<string, string>>({});
  const [revealed, setRevealed] = useState<Record<string, boolean>>({});
  const [resume, setResume] = useState<{ p: number; y: number } | null>(null);
  const [fullscreen, setFullscreen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  // --- Açılış: arka sayfa kilitlenir; özet değişince en başa dönülür -------------------------------
  useLayoutEffect(() => {
    lockScroll();
    return unlockScroll;
  }, []);

  useEffect(() => {
    const a = window.matchMedia('(min-width: 1024px)');
    const b = window.matchMedia('(min-width: 1180px)');
    const on = () => {
      setRailMq(a.matches);
      setPanelMq(b.matches);
    };
    a.addEventListener('change', on);
    b.addEventListener('change', on);
    return () => {
      a.removeEventListener('change', on);
      b.removeEventListener('change', on);
    };
  }, []);

  // Sağ panel: bu dersin sınav spotları + bu özetteki kalem işaretleri
  const scope = `summary:${summary.id}`;
  const lessonSpots = useLessonSpots(summary);
  const [marks, refreshMarks] = useScopeMarks(scope);
  const markTimer = useRef(0);
  const refreshMarksSoon = () => {
    window.clearTimeout(markTimer.current);
    markTimer.current = window.setTimeout(refreshMarks, 260);
  };
  useEffect(() => () => window.clearTimeout(markTimer.current), []);
  const jumpToMark = (m: ScopeMark) => {
    const root = scrollRef.current?.querySelector<HTMLElement>('.sr-col');
    if (!root) return;
    const text = root.textContent || '';
    let at = text.slice(m.start, m.end) === m.text ? m.start : text.indexOf(m.text);
    if (at < 0) at = m.start;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let pos = 0;
    let node: Node | null;
    while ((node = walker.nextNode())) {
      const len = node.textContent?.length || 0;
      if (pos + len > at) {
        const el = node.parentElement;
        el?.closest('.sr-reveal')?.classList.add('is-in');
        el?.scrollIntoView({ behavior: reduceMotion() ? 'auto' : 'smooth', block: 'center' });
        break;
      }
      pos += len;
    }
  };

  // Slayt PDF'i: Kurul 1 dersleri Öğren'deki "k1p-<ders>" destesiyle aynı, içerikle doğrulanmış eşlemeyi kullanır
  const [pdfInfo, setPdfInfo] = useState<DeckPdfInfo | null>(null);
  useEffect(() => {
    setPdfInfo(null);
    if (summary.kurul !== 1) return;
    let live = true;
    resolveDeckPdf(`k1p-${summary.id}`).then((r) => live && setPdfInfo(r));
    return () => {
      live = false;
    };
  }, [summary.id, summary.kurul]);
  const pdfFile = pdfInfo?.files[0];
  const pdfHref = pdfFile ? pdfFile.url || (pdfFile.fileId ? driveViewUrl(pdfFile.fileId) : undefined) : undefined;

  const saveNow = useCallback(() => {
    const el = scrollRef.current;
    if (!el || !ready) return;
    const max = el.scrollHeight - el.clientHeight;
    markReading(summary.id, max > 0 ? (el.scrollTop / max) * 100 : 0, el.scrollTop);
  }, [summary.id, ready]);

  const close = useCallback(() => {
    if (closing) return;
    saveNow();
    if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {});
    setClosing(true);
    window.setTimeout(onClose, reduceMotion() ? 0 : 200);
  }, [closing, onClose, saveNow]);

  // Özet değişince (sonraki ders) baştan başla, kaldığı yer varsa öner
  const resumeFor = useRef('');
  useEffect(() => {
    if (!ready || resumeFor.current === summary.id) return;
    resumeFor.current = summary.id;
    scrollRef.current?.scrollTo({ top: 0 });
    setPicked({});
    setRevealed({});
    setActiveSec('');
    const mark = progressMap[summary.id];
    setResume(mark && mark.y > 400 && mark.p < 97 ? { p: mark.p, y: mark.y } : null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ready, summary.id]);

  useEffect(() => {
    if (!resume) return;
    const t = window.setTimeout(() => setResume(null), 9000);
    return () => window.clearTimeout(t);
  }, [resume]);

  // Kapanırken / sekme gizlenince ilerleme yazılır
  useEffect(() => {
    const onHide = () => document.visibilityState === 'hidden' && saveNow();
    document.addEventListener('visibilitychange', onHide);
    return () => {
      document.removeEventListener('visibilitychange', onHide);
      saveNow();
    };
  }, [saveNow]);

  // --- Kaydırma: ilerleme, etkin bölüm/alt başlık, ara sıra kayıt ---------------------------------
  const raf = useRef(0);
  const lastSave = useRef(0);
  const onScroll = () => {
    if (raf.current) return;
    raf.current = requestAnimationFrame(() => {
      raf.current = 0;
      const el = scrollRef.current;
      if (!el) return;
      const max = el.scrollHeight - el.clientHeight;
      const p = max > 0 ? Math.min(100, Math.max(0, (el.scrollTop / max) * 100)) : 0;
      setProgress(p);
      setScrolled(el.scrollTop > 640);
      const top = el.getBoundingClientRect().top + 96;
      let sec = '';
      let secEl: Element | null = null;
      el.querySelectorAll<HTMLElement>('[data-sec]').forEach((h) => {
        if (h.getBoundingClientRect().top <= top) {
          sec = h.dataset.sec || '';
          secEl = h;
        }
      });
      let sub = '';
      (secEl as HTMLElement | null)?.querySelectorAll<HTMLElement>('[data-anchor]').forEach((h) => {
        if (h.getBoundingClientRect().top <= top) sub = h.dataset.anchor || '';
      });
      setActiveSec(sec);
      setActiveSub(sub);
      if (resume && el.scrollTop > resume.y - 300) setResume(null);
      const now = Date.now();
      if (now - lastSave.current > 1200) {
        lastSave.current = now;
        markReading(summary.id, p, el.scrollTop);
      }
    });
  };
  useEffect(() => () => cancelAnimationFrame(raf.current), []);

  const jump = (id: string) => {
    const el = scrollRef.current?.querySelector<HTMLElement>(`[data-sec="${id}"], [data-anchor="${id}"]`);
    if (!el) return;
    el.classList.add('is-in');
    el.scrollIntoView({ behavior: reduceMotion() ? 'auto' : 'smooth', block: 'start' });
    setTocSheet(false);
  };
  const toTop = () => scrollRef.current?.scrollTo({ top: 0, behavior: reduceMotion() ? 'auto' : 'smooth' });

  // --- Bölümler görünür oldukça yükselir (bir kez) ------------------------------------------------
  useEffect(() => {
    const root = scrollRef.current;
    if (!root || !ready) return;
    const items = Array.from(root.querySelectorAll<HTMLElement>('.sr-reveal:not(.is-in)'));
    if (reduceMotion() || typeof IntersectionObserver === 'undefined') {
      items.forEach((n) => n.classList.add('is-in'));
      return;
    }
    const io = new IntersectionObserver(
      (entries) =>
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add('is-in');
            io.unobserve(e.target);
          }
        }),
      { root, rootMargin: '0px 0px -6% 0px', threshold: 0.01 }
    );
    items.forEach((n) => io.observe(n));
    return () => io.disconnect();
  }, [doc, ready]);

  // --- Belge içi arama --------------------------------------------------------------------------
  const liveQuery = searchOpen ? query.trim() : '';
  useEffect(() => {
    if (liveQuery.length < 2) {
      setHits([]);
      return;
    }
    const id = requestAnimationFrame(() => {
      const found = Array.from(scrollRef.current?.querySelectorAll<HTMLElement>('mark.sr-hit') || []).filter((m) => !m.closest('.sr-q-sol:not(.is-open)'));
      setHits(found);
      setHitIdx(0);
    });
    return () => cancelAnimationFrame(id);
  }, [liveQuery, doc, prefs.markers]);

  useEffect(() => {
    hits.forEach((h, i) => h.classList.toggle('is-current', i === hitIdx));
    const cur = hits[hitIdx];
    if (cur) {
      cur.closest('.sr-reveal')?.classList.add('is-in');
      cur.scrollIntoView({ behavior: reduceMotion() ? 'auto' : 'smooth', block: 'center' });
    }
  }, [hits, hitIdx]);

  const stepHit = (d: 1 | -1) => hits.length && setHitIdx((i) => (i + d + hits.length) % hits.length);
  const closeSearch = () => {
    setSearchOpen(false);
    setQuery('');
  };

  // --- Klavye -----------------------------------------------------------------------------------
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (tocSheet) return; // alt sayfa kendi Esc'ini işler
      if (e.key === 'Escape') {
        if (document.fullscreenElement) return; // tarayıcı tam ekrandan çıkar
        if (aaOpen) return setAaOpen(false);
        if (searchOpen) return closeSearch();
        return close();
      }
      if (((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'f') || (e.key === '/' && !isTyping(e.target))) {
        e.preventDefault();
        setSearchOpen(true);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [aaOpen, searchOpen, tocSheet, close]);

  // --- Tam ekran --------------------------------------------------------------------------------
  useEffect(() => {
    const on = () => setFullscreen(!!document.fullscreenElement && document.fullscreenElement === rootRef.current);
    document.addEventListener('fullscreenchange', on);
    return () => document.removeEventListener('fullscreenchange', on);
  }, []);
  const toggleFullscreen = () => {
    if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {});
    else rootRef.current?.requestFullscreen?.().catch(() => toast.info('Tam ekran desteklenmiyor', 'Bu tarayıcı okuyucuyu tam ekran açamıyor.'));
  };

  const copyMarkdown = () => {
    if (!summary.content) return;
    navigator.clipboard?.writeText(summary.content).then(
      () => toast.success('Özet metni kopyalandı'),
      () => toast.error('Kopyalanamadı', 'Tarayıcı panoya erişime izin vermedi.')
    );
  };

  // --- Metin çizimi -----------------------------------------------------------------------------
  const renderText = useCallback(
    (t: string) => <span dangerouslySetInnerHTML={{ __html: formatInline(t, { markers: prefs.markers, query: liveQuery }) }} />,
    [prefs.markers, liveQuery]
  );

  const allQuestions = useMemo(() => doc.sections.flatMap((s) => s.questions), [doc]);
  const answered = allQuestions.filter((q) => picked[q.id]);
  const correct = answered.filter((q) => q.answer && picked[q.id] === q.answer).length;
  const showSide = wide && sideOpen;
  const totalMin = Math.max(1, summary.readingTimeMinutes || 1);
  const readMin = Math.min(totalMin, Math.round(totalMin * (progress / 100)));
  const activeSection = doc.sections.find((s) => s.id === activeSec);
  const instructor = summary.instructor || doc.meta.instructor;
  const realSource = doc.meta.sources && /ders notu/i.test(doc.meta.sources) ? doc.meta.sources.replace(/^ders notu:\s*/i, '') : '';

  const toggleToc = () => (wide ? setSideOpen((v) => !v) : setTocSheet(true));

  const Toc = (
    <nav className="sr-toc" aria-label="İçindekiler">
      <div className="sr-toc-head">
        <span className="sr-toc-crumb">Ders özetleri › {disciplineLabel(summary.discipline)}</span>
        <strong className="sr-toc-title">{summary.title}</strong>
      </div>
      <ol className="sr-toc-list">
        {doc.sections.map((s, i) => {
          const on = activeSec === s.id;
          const count = s.kind === 'questions' ? s.questions.length : s.kind === 'spot' ? s.spots.length : 0;
          return (
            <li key={s.id} className={on ? 'is-on' : ''}>
              <button type="button" onClick={() => jump(s.id)} aria-current={on ? 'location' : undefined}>
                <span className="sr-toc-n">
                  <SecMark s={s} i={i} />
                </span>
                <span className="sr-toc-t">{secTitle(s)}</span>
                {count > 0 && <small>{count}</small>}
              </button>
              {s.subs.length > 0 && (
                <div className={`sr-toc-subs ${on ? 'is-open' : ''}`}>
                  <ol>
                    {s.subs.map((sub) => (
                      <li key={sub.id}>
                        <button type="button" tabIndex={on ? 0 : -1} className={activeSub === sub.id ? 'is-on' : ''} onClick={() => jump(sub.id)}>
                          {sub.table && <Table2 aria-hidden />}
                          <span>{sub.title}</span>
                        </button>
                      </li>
                    ))}
                  </ol>
                </div>
              )}
            </li>
          );
        })}
      </ol>
      <div className="sr-toc-foot">
        <span>{progress >= 99 ? `Tamamlandı · ${totalMin} dk` : `Okuma: ${readMin} / ${totalMin} dk`}</span>
        <span
          className="sr-toc-bar"
          role="progressbar"
          aria-label="Okuma ilerlemesi"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={Math.round(progress)}
        >
          <i style={{ transform: `scaleX(${progress / 100})` }} />
        </span>
      </div>
    </nav>
  );

  const renderBlock = (b: Block, i: number) => {
    switch (b.kind) {
      case 'rich':
        return <RichList key={i} groups={b.groups} renderText={renderText} />;
      case 'sub':
        return (
          <div key={i} className="sr-sub" data-anchor={b.id}>
            <h3>{renderText(b.title)}</h3>
            {b.groups.length > 0 && <RichList groups={b.groups} renderText={renderText} />}
          </div>
        );
      case 'callout':
        return <Callout key={i} tone={b.tone} title={b.title} text={b.text} items={b.items} renderText={renderText} />;
      case 'table':
        return <DataTable key={i} id={b.id} headers={b.headers} rows={b.rows} renderText={renderText} />;
      default:
        return (
          <p key={i} className="sr-para">
            {renderText(b.text)}
          </p>
        );
    }
  };

  return (
    <div
      ref={rootRef}
      className={`sr-root ${disciplineClass(summary.discipline)} ${closing ? 'is-closing' : ''} ${panelSide ? 'has-panel' : ''}`}
      role="dialog"
      aria-label={summary.title}
    >
      {/* ── Üst çubuk ── */}
      <header className={`sr-bar ${searchOpen ? 'is-search' : ''}`}>
        <button type="button" className="sr-ib" onClick={close} aria-label="Okuyucuyu kapat" title="Kapat (Esc)">
          <X />
        </button>
        <button type="button" className={`sr-ib ${showSide ? 'is-on' : ''}`} onClick={toggleToc} aria-label="İçindekiler" aria-pressed={wide ? showSide : undefined} title="İçindekiler">
          <ListTree />
        </button>

        {searchOpen ? (
          <div className="sr-find">
            <Search aria-hidden />
            <input
              type="search"
              autoFocus
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  stepHit(e.shiftKey ? -1 : 1);
                }
              }}
              placeholder="Özette ara"
              aria-label="Özette ara"
            />
            <span className="sr-find-n" aria-live="polite">
              {liveQuery.length >= 2 ? (hits.length ? `${hitIdx + 1}/${hits.length}` : 'yok') : ''}
            </span>
            <button type="button" className="sr-ib is-sm" onClick={() => stepHit(-1)} disabled={!hits.length} aria-label="Önceki eşleşme">
              <ChevronUp />
            </button>
            <button type="button" className="sr-ib is-sm" onClick={() => stepHit(1)} disabled={!hits.length} aria-label="Sonraki eşleşme">
              <ChevronDown />
            </button>
            <button type="button" className="sr-ib is-sm" onClick={closeSearch} aria-label="Aramayı kapat">
              <X />
            </button>
          </div>
        ) : (
          <div className="sr-bar-title">
            <b>{summary.title}</b>
            <span key={activeSection?.id || 'cover'} className="sr-bar-sub">
              {activeSection ? secTitle(activeSection) : `Kurul ${summary.kurul} · ${disciplineLabel(summary.discipline)}`}
            </span>
          </div>
        )}

        <div className="sr-bar-tools">
          {!searchOpen && (
            <button type="button" className="sr-ib" onClick={() => setSearchOpen(true)} aria-label="Özette ara" title="Ara ( / )">
              <Search />
            </button>
          )}
          <HighlighterToolbar className="sr-pen" />
          <div className="sr-aa-wrap">
            <button type="button" className={`sr-ib sr-aa ${aaOpen ? 'is-on' : ''}`} onClick={() => setAaOpen((v) => !v)} aria-expanded={aaOpen} aria-haspopup="dialog" aria-label="Görünüm ayarları" title="Görünüm">
              Aa
            </button>
            {aaOpen && (
              <>
                <button type="button" className="sr-pop-scrim" aria-label="Kapat" onClick={() => setAaOpen(false)} />
                <div className="sr-pop" role="dialog" aria-label="Görünüm ayarları">
                  <div className="sr-pop-scale" role="group" aria-label="Yazı boyutu">
                    <button type="button" onClick={() => setPrefs({ scale: prefs.scale - 10 })} disabled={prefs.scale <= 80} aria-label="Yazıyı küçült">
                      <span style={{ fontSize: 13 }}>A</span>
                    </button>
                    <button type="button" className="sr-pop-pct" onClick={() => setPrefs({ scale: 100 })} aria-label="Yazı boyutunu sıfırla">
                      %{prefs.scale}
                    </button>
                    <button type="button" onClick={() => setPrefs({ scale: prefs.scale + 10 })} disabled={prefs.scale >= 150} aria-label="Yazıyı büyüt">
                      <span style={{ fontSize: 20 }}>A</span>
                    </button>
                  </div>
                  <div className="sr-pop-themes" role="radiogroup" aria-label="Tema">
                    {MODES.map((m) => (
                      <button key={m} type="button" role="radio" aria-checked={appearance.mode === m} className={`sr-theme is-${m}`} onClick={() => appearance.set({ mode: m })}>
                        <i aria-hidden>Aa</i>
                        {MODE_LABELS[m]}
                      </button>
                    ))}
                  </div>
                  <div className="sr-pop-group">
                    <span className="sr-pop-label">Satır genişliği</span>
                    <div className="sr-pop-seg">
                      <Segmented label="Satır genişliği" value={prefs.measure} options={MEASURES} onChange={(v) => setPrefs({ measure: v })} />
                    </div>
                    <label className="sr-pop-row">
                      <span>Kitap yazı tipi</span>
                      <Switch label="Kitap yazı tipi" checked={prefs.serif} onChange={(v) => setPrefs({ serif: v })} />
                    </label>
                    <label className="sr-pop-row">
                      <span>Anahtar kelime vurguları</span>
                      <Switch label="Anahtar kelime vurguları" checked={prefs.markers} onChange={(v) => setPrefs({ markers: v })} />
                    </label>
                  </div>
                  <div className="sr-pop-group">
                    <button type="button" className="sr-pop-row" onClick={toggleFullscreen}>
                      <span>{fullscreen ? 'Tam ekrandan çık' : 'Tam ekran'}</span>
                      {fullscreen ? <Shrink aria-hidden /> : <Expand aria-hidden />}
                    </button>
                    <button type="button" className="sr-pop-row" onClick={() => { setAaOpen(false); window.setTimeout(() => window.print(), 50); }}>
                      <span>Yazdır / PDF</span>
                      <Printer aria-hidden />
                    </button>
                    <button type="button" className="sr-pop-row" onClick={copyMarkdown}>
                      <span>Metni kopyala</span>
                      <Copy aria-hidden />
                    </button>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
        <div className="sr-progress" aria-hidden>
          <i style={{ transform: `scaleX(${progress / 100})` }} />
        </div>
      </header>

      <div className="sr-body">
        {wide && (
          <aside className={`sr-side ${showSide ? 'is-open' : ''}`} aria-hidden={!showSide} inert={!showSide ? true : undefined}>
            {ready ? Toc : <div className="sr-toc-skel" aria-hidden>{[0, 1, 2, 3, 4].map((k) => <span key={k} className="ui-skel" />)}</div>}
          </aside>
        )}

        <div ref={scrollRef} className="sr-scroll" onScroll={onScroll} onPointerUp={refreshMarksSoon} onKeyUp={refreshMarksSoon}>
          {/* Araç satırı Highlightable dışında: PDF düğmesi sonradan gelince işaret konumları kaymasın */}
          <div className={`sr-tools m-${prefs.measure}`}>
            <div className="sr-fs" role="group" aria-label="Yazı boyutu">
              <button type="button" onClick={() => setPrefs({ scale: prefs.scale - 10 })} disabled={prefs.scale <= 80} aria-label="Yazıyı küçült" title={`Yazı %${prefs.scale}`}>
                A−
              </button>
              <button type="button" onClick={() => setPrefs({ scale: prefs.scale + 10 })} disabled={prefs.scale >= 150} aria-label="Yazıyı büyüt" title={`Yazı %${prefs.scale}`}>
                A+
              </button>
            </div>
            {pdfHref && (
              <a className="sr-tool" href={pdfHref} target="_blank" rel="noopener noreferrer" title={pdfFile?.name}>
                <FileText aria-hidden /> Slayt PDF’i
              </a>
            )}
            {onOpenPdfModal && (
              <button type="button" className="sr-tool" onClick={onOpenPdfModal}>
                PDF indir
              </button>
            )}
          </div>
          <Highlightable
            scope={scope}
            className={`sr-col m-${prefs.measure} ${prefs.serif ? 'is-serif' : ''}`}
            style={{ '--sr-scale': prefs.scale / 100 } as React.CSSProperties}
          >
            {/* ── Kapak (kompakt) ── */}
            <header className="sr-hero">
              <div className="sr-hero-eyebrow">
                <i className="hk-dot" aria-hidden />
                <span>{disciplineLabel(summary.discipline)}</span>
                <span aria-hidden>·</span>
                <span>Kurul {summary.kurul}</span>
                {summary.sourceYear && (
                  <>
                    <span aria-hidden>·</span>
                    <span>{summary.sourceYear}</span>
                  </>
                )}
              </div>
              <h1>{summary.title}</h1>
              <ul className="sr-hero-stats" aria-label="Özet bilgileri">
                {instructor && (
                  <li>
                    <GraduationCap aria-hidden /> {instructor}
                  </li>
                )}
                <li>
                  <Clock aria-hidden />
                  <b>{summary.readingTimeMinutes}</b> dk okuma
                </li>
                {ready && (
                  <>
                    <li>
                      <b>{doc.counts.sections}</b> bölüm
                    </li>
                    {doc.counts.tables > 0 && (
                      <li>
                        <b>{doc.counts.tables}</b> tablo
                      </li>
                    )}
                    {doc.counts.spots > 0 && (
                      <li>
                        <b>{doc.counts.spots}</b> spot
                      </li>
                    )}
                    {doc.counts.questions > 0 && (
                      <li>
                        <b>{doc.counts.questions}</b> soru
                      </li>
                    )}
                  </>
                )}
              </ul>
              {realSource && <p className="sr-hero-src">Kaynak: {realSource}</p>}
            </header>

            {!ready ? (
              <div className="sr-skel" aria-busy="true" aria-label="Özet yükleniyor">
                {[0, 1, 2].map((k) => (
                  <div key={k} className="sr-skel-sec">
                    <i className="w-40" />
                    <i className="w-100" />
                    <i className="w-90" />
                    <i className="w-70" />
                  </div>
                ))}
              </div>
            ) : (
              <>
                {doc.sections.map((s, i) => (
                  <section key={s.id} className={`sr-sec sr-reveal is-${s.kind}`} data-sec={s.id} aria-labelledby={`${s.id}-h`}>
                    <header className="sr-sec-h">
                      <span className="sr-sec-n" aria-hidden>
                        <SecMark s={s} i={i} />
                      </span>
                      <div>
                        <h2 id={`${s.id}-h`}>{secTitle(s)}</h2>
                        {s.context && <p>{renderText(s.context)}</p>}
                      </div>
                      {s.kind === 'questions' && answered.length > 0 && (
                        <span className={`sr-score ${correct * 2 < answered.length ? 'is-low' : ''}`}>
                          {correct}/{answered.length} doğru
                          <button type="button" className="sr-ib is-sm" onClick={() => { setPicked({}); setRevealed({}); }} aria-label="Soruları sıfırla" title="Sıfırla">
                            <RotateCcw />
                          </button>
                        </span>
                      )}
                    </header>

                    {s.objectives.length > 0 && <Objectives items={s.objectives} renderText={renderText} />}
                    {s.spots.length > 0 && <SpotWall spots={s.spots} renderText={renderText} />}
                    {s.blocks.length > 0 && <div className="sr-blocks">{s.blocks.map(renderBlock)}</div>}
                    {s.questions.length > 0 && (
                      <div className="sr-qs">
                        {s.questions.map((q) => (
                          <QuestionCard
                            key={q.id}
                            q={q}
                            picked={picked[q.id]}
                            revealed={!!revealed[q.id]}
                            onPick={(l) => setPicked((p) => ({ ...p, [q.id]: l }))}
                            onReveal={() => setRevealed((r) => ({ ...r, [q.id]: true }))}
                            renderText={renderText}
                          />
                        ))}
                      </div>
                    )}
                  </section>
                ))}

                {/* ── Bitiş ── */}
                <footer className="sr-end sr-reveal">
                  <span className="sr-end-badge" aria-hidden>
                    <BookOpenCheck />
                  </span>
                  <h3>Özetin sonuna geldin</h3>
                  <p>
                    {answered.length > 0
                      ? `${answered.length} sorudan ${correct} tanesini doğru yanıtladın.`
                      : allQuestions.length > 0
                        ? `Pekiştirmek için ${allQuestions.length} çıkmış soruyu çözebilirsin.`
                        : 'Hızlı tekrar bölümüne dönüp spotları gözden geçirebilirsin.'}
                  </p>
                  <div className="sr-end-actions">
                    <button type="button" className="ms-btn" onClick={toTop}>
                      <ArrowUp aria-hidden /> Başa dön
                    </button>
                    {onOpenPdfModal && (
                      <button type="button" className="ms-btn" onClick={onOpenPdfModal}>
                        PDF indir
                      </button>
                    )}
                  </div>
                  {next && onOpenNext && (
                    <button type="button" className={`sr-next ${disciplineClass(next.discipline)}`} onClick={onOpenNext}>
                      <span>
                        <small>Sıradaki ders</small>
                        <b>{next.title}</b>
                        <em>
                          <i className="hk-dot" aria-hidden /> {disciplineLabel(next.discipline)} · ~{next.readingTimeMinutes} dk
                        </em>
                      </span>
                      <ArrowRight aria-hidden />
                    </button>
                  )}
                </footer>
              </>
            )}
          </Highlightable>
          {!panelSide && ready && (
            <div className={`sr-after m-${prefs.measure}`}>
              <ReaderPanel spots={lessonSpots} marks={marks} onJump={jumpToMark} inline />
            </div>
          )}
        </div>

        {panelSide && (
          <aside className="sr-rpanel" aria-label="Ders paneli">
            <ReaderPanel spots={lessonSpots} marks={marks} onJump={jumpToMark} />
          </aside>
        )}
      </div>

      {/* ── Yüzen düğmeler ── */}
      {resume && (
        <div className="sr-resume" role="status">
          <button
            type="button"
            onClick={() => {
              scrollRef.current?.scrollTo({ top: resume.y, behavior: reduceMotion() ? 'auto' : 'smooth' });
              setResume(null);
            }}
          >
            <RotateCcw aria-hidden /> Kaldığın yerden devam et · %{Math.round(resume.p)}
          </button>
          <button type="button" className="sr-resume-x" onClick={() => setResume(null)} aria-label="Kapat">
            <X />
          </button>
        </div>
      )}
      <button type="button" className={`sr-top ${scrolled && !resume ? 'is-on' : ''}`} onClick={toTop} aria-label="Başa dön" tabIndex={scrolled ? 0 : -1}>
        <ArrowUp />
      </button>

      <Sheet open={tocSheet && !wide} onClose={() => setTocSheet(false)} title="İçindekiler" subtitle={summary.title} size="full">
        {/* Alt sayfa body'ye taşınır: ders rengi (--d) burada yeniden verilir */}
        <div className={disciplineClass(summary.discipline)}>{Toc}</div>
      </Sheet>
    </div>
  );
};
