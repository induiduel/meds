/**
 * Ders notları — v12 "Net" (canvas panosu Notes.dc.html). Yalnız data-design='v12' iken LectureNotesView'den çizilir;
 * durum, işleme/silme/eşitleme ve canlı güncelleme oradadır (bu dosya yalnız görünüm + okuyucu açık/kapalı durumu).
 *
 * Dizin: ortak PageToolbar (Slayt kataloğu | İşlenmiş notlar, arama, anabilim dalı/durum süzgeçleri, araçlar)
 *   → tek satır işleme ilerlemesi → tek panelde sıkı satırlar.
 *   Katalog satırı: no · başlık · dal · sayfa · konular · İşlendi/Bekliyor · Drive · yeniden işle · sil · Oku/İşle.
 *   İşlenmiş not satırı: no · başlık · dal · sayfa · hoca · Oku.
 * Okuyucu: ReaderV12 — içindekiler = sayfalar (sayfanın ilk satırı), sayfa sayfa slayt metni, kalemle işaretleme
 *   (kapsam `lecture-note:<id>`), "Notlarım" kenar paneli, Slayt PDF'i / tam ekran / sil menüde.
 * Derin bağlantı /notlar?id=<not>&page=<n>: LectureNotesView notu seçer, burada okuyucu açılır, sayfaya kayılır
 * (sayfa öğeleri aynı `ln-page-<n>` kimliğini taşır). Stil: styles/v12/reader.css (.r12-*).
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { BookMarked, BookOpen, Check, CheckCircle2, ChevronRight, Copy, ExternalLink, FileText, FolderGit2, Play, Plus, RefreshCw, Search, Trash2, X } from 'lucide-react';
import type { LectureNote } from '../../types';
import type { DriveSlideMeta } from '../../data/driveCatalog';
import { SourceText } from '../ui/SourceText';
import { HighlighterToolbar, Highlightable } from '../ui/Highlighter';
import { ReaderPanel, useScopeMarks } from '../summary/ReaderPanel';
import { disciplineClass } from '../../utils/discipline';
import { R12MenuGroup, R12MenuItem, ReaderV12, scrollToMark, type ReaderTocItem } from './ReaderV12';
import '../../styles/v12/reader.css';

export interface LectureNotesV12Props {
  /** PageToolbar; içine ilerleme satırı (children) verilir */
  renderToolbar: (children: React.ReactNode) => React.ReactNode;
  onCatalog: boolean;
  goCatalog: () => void;
  feedbackMessage: string | null;
  clearFeedback: () => void;
  catalog: DriveSlideMeta[];
  isSlideRendered: (s: DriveSlideMeta) => LectureNote | undefined;
  renderingSlideId: string | null;
  onRenderSlide: (s: DriveSlideMeta) => void;
  onDeleteNote: (id: string, title: string) => Promise<void> | void;
  isAdmin: boolean;
  notes: LectureNote[];
  filteredNotes: LectureNote[];
  activeNote: LectureNote | null;
  setActiveNote: (n: LectureNote) => void;
  progressPercent: number;
  renderedPages: number;
  totalPages: number;
  onPurge: () => void;
  pdfHrefFor: (n: LectureNote) => string | undefined;
  onFullscreen: (n: LectureNote) => void;
  copyPage: (text: string, page: number) => void;
  copied: Record<number, boolean>;
  splitTitle: (raw: string) => { no: string; title: string };
  fmtDate: (v?: string) => string;
  /** Not yükleme penceresi ve tam ekran okuyucu */
  modals?: React.ReactNode;
}

/** Sayfanın ilk anlamlı satırı (içindekiler başlığı) */
const firstLine = (t: string) => {
  const line = String(t || '')
    .split('\n')
    .map((l) => l.replace(/^[#>*\-•\d.)\s]+/, '').replace(/\*\*|==|`/g, '').trim())
    .find((l) => l.length > 2);
  if (!line) return '';
  return line.length > 72 ? `${line.slice(0, 70).trimEnd()}…` : line;
};

const NoteReader: React.FC<{
  note: LectureNote;
  title: string;
  onClose: () => void;
  isAdmin: boolean;
  pdfHref?: string;
  onFullscreen: () => void;
  onDelete: () => void;
  copyPage: (text: string, page: number) => void;
  copied: Record<number, boolean>;
  fmtDate: (v?: string) => string;
}> = ({ note, title, onClose, isAdmin, pdfHref, onFullscreen, onDelete, copyPage, copied, fmtDate }) => {
  const scope = `lecture-note:${note.id}`;
  const [marks, refreshMarks] = useScopeMarks(scope);
  const hlRef = useRef<HTMLDivElement>(null);
  const timer = useRef(0);
  const refreshSoon = () => {
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(refreshMarks, 260);
  };
  useEffect(() => () => window.clearTimeout(timer.current), []);
  const toc: ReaderTocItem[] = useMemo(
    () => note.pages.map((p) => ({ id: `ln-page-${p.pageNumber}`, title: `${p.pageNumber}. ${firstLine(p.content) || `Sayfa ${p.pageNumber}`}` })),
    [note.pages]
  );
  const total = note.totalSlides || note.pages.length;
  const jump = (m: Parameters<typeof scrollToMark>[1]) => scrollToMark(hlRef.current?.querySelector<HTMLElement>('.r12-hl'), m);
  const date = fmtDate(note.uploadedAt);

  return (
    <ReaderV12
      className={disciplineClass(note.discipline)}
      title={title}
      meta={`${note.discipline} · ders notu · ${total} sayfa`}
      onBack={onClose}
      backLabel="Notlara dön"
      toc={toc}
      onPointerUp={refreshSoon}
      onKeyUp={refreshSoon}
      tools={<HighlighterToolbar className="r12-pen" />}
      menu={
        <R12MenuGroup label="Not">
          {pdfHref && <R12MenuItem icon={FileText} label="Slayt PDF’i" href={pdfHref} />}
          <R12MenuItem icon={BookOpen} label="Tam ekran okuyucu" onClick={onFullscreen} />
          {isAdmin && <R12MenuItem icon={Trash2} label="Bu notu sil" danger onClick={onDelete} />}
        </R12MenuGroup>
      }
      margin={<ReaderPanel spots={null} marks={marks} onJump={jump} />}
      marginLabel="Notlarım"
      after={<ReaderPanel spots={null} marks={marks} onJump={jump} inline />}
    >
      <div ref={hlRef} style={{ display: 'contents' }}>
        <Highlightable scope={scope} className="r12-hl">
          <header className="r12-head">
            <h1 className="r12-h1">{title}</h1>
            <p className="r12-meta">
              <span>{note.discipline}</span>
              <span>
                <b>{total}</b> sayfa
              </span>
              {note.instructor && <span>{note.instructor}</span>}
              {note.uploadedBy && <span>Yükleyen: {note.uploadedBy}</span>}
              {date && <span>{date}</span>}
            </p>
          </header>
          {note.pages.map((page) => {
            const id = `ln-page-${page.pageNumber}`;
            const done = !!copied[page.pageNumber];
            return (
              <section key={page.pageNumber} id={id} data-r12-sec={id} className="r12-pg" aria-labelledby={`${id}-h`}>
                <div className="r12-pg-h">
                  <h2 id={`${id}-h`}>
                    Sayfa {page.pageNumber} <small>/ {total}</small>
                  </h2>
                  {/* Etiket sabit kalır: kalem işaretlerinin metin konumu kaymasın; durum simgeyle ve duyuruyla verilir */}
                  <button
                    type="button"
                    className={`r12-tbtn ${done ? 'is-done' : ''}`}
                    onClick={() => copyPage(page.content, page.pageNumber)}
                    aria-label={done ? `Sayfa ${page.pageNumber} kopyalandı` : `Sayfa ${page.pageNumber} metnini kopyala`}
                  >
                    {done ? <Check aria-hidden /> : <Copy aria-hidden />}
                    <span aria-hidden>Kopyala</span>
                  </button>
                </div>
                <SourceText text={String(page.content || '')} />
                {page.keywords && page.keywords.length > 0 && (
                  <ul className="r12-kw" aria-label="Kavramlar">
                    {page.keywords.map((kw, i) => (
                      <li key={i}>{kw}</li>
                    ))}
                  </ul>
                )}
              </section>
            );
          })}
        </Highlightable>
      </div>
    </ReaderV12>
  );
};

export const LectureNotesV12: React.FC<LectureNotesV12Props> = (p) => {
  const [readingId, setReadingId] = useState<string | null>(null);
  const reading = readingId ? p.notes.find((n) => n.id === readingId) || null : null;

  const read = (note: LectureNote) => {
    p.setActiveNote(note);
    setReadingId(note.id);
  };

  // Derin bağlantı: üst bileşen notu seçince okuyucu bir kez kendiliğinden açılır
  const autoOpened = useRef(false);
  useEffect(() => {
    if (autoOpened.current || !p.activeNote) return;
    const id = new URLSearchParams(window.location.search).get('id');
    if (id && id === p.activeNote.id) {
      autoOpened.current = true;
      setReadingId(id);
    }
  }, [p.activeNote]);

  const prog = (
    <div className="r12-prog" aria-label="Slayt işleme durumu">
      <span>
        <b>%{p.progressPercent}</b> · {p.renderedPages.toLocaleString('tr-TR')} / {p.totalPages.toLocaleString('tr-TR')} sayfa işlendi
      </span>
      <span className="r12-bar" role="progressbar" aria-valuenow={p.progressPercent} aria-valuemin={0} aria-valuemax={100} aria-label="Slayt işleme ilerlemesi">
        <i style={{ transform: `scaleX(${p.progressPercent / 100})` }} />
      </span>
      {p.isAdmin && p.notes.length > 0 && (
        <button type="button" className="r12-btn" onClick={p.onPurge} title="Önbellekte kalan örnek notları temizler">
          Örnekleri temizle
        </button>
      )}
    </div>
  );

  return (
    <div className="r12-page">
      {p.renderToolbar(prog)}

      {p.feedbackMessage && (
        <div role="status" className="r12-feedback">
          <CheckCircle2 aria-hidden />
          <span>{p.feedbackMessage}</span>
          <button type="button" className="r12-ib" onClick={p.clearFeedback} aria-label="Bildirimi kapat">
            <X aria-hidden />
          </button>
        </div>
      )}

      {p.onCatalog &&
        (p.catalog.length === 0 ? (
          <div className="r12-empty">
            <Search aria-hidden />
            <h3>Aramana uygun slayt yok</h3>
            <p>Başka bir anabilim dalı ya da anahtar kelime dene.</p>
          </div>
        ) : (
          <ul className="r12-list">
            {p.catalog.map((slide, i) => {
              const rendered = p.isSlideRendered(slide);
              const busy = p.renderingSlideId === slide.id;
              const { no, title } = p.splitTitle(slide.title);
              const topics = slide.keyTopics
                .map((t) => p.splitTitle(t).title)
                .filter((t) => t && t.toLocaleLowerCase('tr-TR') !== title.toLocaleLowerCase('tr-TR'));
              return (
                <li key={slide.id} className={disciplineClass(slide.discipline)}>
                  <div className="r12-row is-wrap">
                    <span className="r12-no" aria-hidden>
                      {no || i + 1}
                    </span>
                    <span className="r12-row-main">
                      <span className="r12-row-t">{title}</span>
                      <span className="r12-row-m">
                        <i className="r12-dot" aria-hidden />
                        <span>{slide.discipline}</span>
                        <span>· {slide.totalRealPages} sayfa</span>
                        {topics.length > 0 && <span className="is-fill is-opt">· {topics.slice(0, 4).join(', ')}</span>}
                      </span>
                    </span>
                    {rendered ? (
                      <span className="r12-badge is-ok">
                        <Check aria-hidden /> İşlendi
                      </span>
                    ) : (
                      <span className="r12-badge">Bekliyor</span>
                    )}
                    <span className="r12-acts">
                      <a className="r12-ib" href={`https://drive.google.com/file/d/${slide.fileId}/view?usp=sharing`} target="_blank" rel="noreferrer" aria-label="Drive'da aç" title="Drive'da aç">
                        <ExternalLink aria-hidden />
                      </a>
                      {rendered && (
                        <button type="button" className="r12-ib" onClick={() => p.onRenderSlide(slide)} disabled={busy} aria-label="Yeniden işle" title="Tüm sayfaları yeniden işler">
                          <RefreshCw className={busy ? 'animate-spin' : ''} aria-hidden />
                        </button>
                      )}
                      {rendered && p.isAdmin && (
                        <button type="button" className="r12-ib is-danger" onClick={() => p.onDeleteNote(slide.id, slide.title)} aria-label="İşlenmiş notu sil" title="İşlenmiş notu sil">
                          <Trash2 aria-hidden />
                        </button>
                      )}
                      {rendered ? (
                        <button type="button" className="r12-btn" onClick={() => read(rendered)}>
                          <BookOpen aria-hidden /> Oku
                        </button>
                      ) : (
                        <button type="button" className="r12-btn is-pri" onClick={() => p.onRenderSlide(slide)} disabled={busy} aria-busy={busy}>
                          {busy ? <RefreshCw className="animate-spin" aria-hidden /> : <Play aria-hidden />}
                          {busy ? 'İşleniyor…' : 'İşle'}
                        </button>
                      )}
                    </span>
                  </div>
                </li>
              );
            })}
          </ul>
        ))}

      {!p.onCatalog &&
        (p.notes.length === 0 ? (
          <div className="r12-empty">
            <BookMarked aria-hidden />
            <h3>Henüz işlenmiş ders notu yok</h3>
            <p>Slayt kataloğundan bir slaytı işle ya da kendi notunu yükle.</p>
            <button type="button" className="r12-btn" onClick={p.goCatalog}>
              <FolderGit2 aria-hidden /> Slayt kataloğuna git
            </button>
          </div>
        ) : (
          <div className="r12-group">
            {p.filteredNotes.length === 0 ? (
              <div className="r12-empty">
                <Search aria-hidden />
                <h3>Eşleşen not yok</h3>
                <p>Aramayı ya da anabilim dalı süzgecini değiştir.</p>
              </div>
            ) : (
              <ul className="r12-list">
                {p.filteredNotes.map((note, i) => {
                  const { no, title } = p.splitTitle(note.title);
                  return (
                    <li key={note.id} className={disciplineClass(note.discipline)}>
                      <button type="button" className="r12-row" onClick={() => read(note)} aria-current={p.activeNote?.id === note.id ? 'true' : undefined}>
                        <span className="r12-no" aria-hidden>
                          {no || i + 1}
                        </span>
                        <span className="r12-row-main">
                          <span className="r12-row-t">{title}</span>
                          <span className="r12-row-m">
                            <i className="r12-dot" aria-hidden />
                            <span>{note.discipline}</span>
                            <span>· {note.totalSlides} sayfa</span>
                            {note.instructor && <span className="is-fill is-opt">· {note.instructor}</span>}
                          </span>
                        </span>
                        <span className="r12-row-s is-txt">Oku</span>
                        <ChevronRight className="r12-go" aria-hidden />
                      </button>
                    </li>
                  );
                })}
              </ul>
            )}
            <div>
              <button type="button" className="r12-btn" onClick={p.goCatalog}>
                <Plus aria-hidden /> Katalogdan slayt işle
              </button>
            </div>
          </div>
        ))}

      {reading && (
        <NoteReader
          note={reading}
          title={p.splitTitle(reading.title).title}
          onClose={() => setReadingId(null)}
          isAdmin={p.isAdmin}
          pdfHref={p.pdfHrefFor(reading)}
          onFullscreen={() => {
            setReadingId(null);
            p.onFullscreen(reading);
          }}
          onDelete={() => p.onDeleteNote(reading.id, reading.title)}
          copyPage={p.copyPage}
          copied={p.copied}
          fmtDate={p.fmtDate}
        />
      )}

      {p.modals}
    </div>
  );
};
