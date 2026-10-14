/**
 * Ses kayıtları (amfi transkriptleri) — v12 "Net". Yalnız data-design='v12' iken TranscriptionsView'den çizilir;
 * liste/ayrıntı sorguları ve süzgeç oradadır. Dizin: ortak PageToolbar (arama + branş süzgeci) → tek panelde sıkı
 * satırlar (başlık · branş · dk · kelime · bölüm + ilk cümle). Okuyucu: ReaderV12 — içindekiler = transkript bölümleri,
 * kalemle işaretleme (kapsam `transcript:<id>`), "Notlarım" kenar paneli, kopyala / asistana sor menüde.
 * Stil: styles/v12/reader.css (.r12-*).
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ChevronRight, Copy, Mic, Sparkles } from 'lucide-react';
import type { TranscriptionDetail, TranscriptionMeta } from '../../hooks/useMedicalQueries';
import { HighlighterToolbar, Highlightable } from '../ui/Highlighter';
import { toast } from '../ui/Toast';
import { ReaderPanel, useScopeMarks } from '../summary/ReaderPanel';
import { disciplineClass } from '../../utils/discipline';
import { R12MenuGroup, R12MenuItem, ReaderV12, scrollToMark, type ReaderTocItem } from './ReaderV12';
import '../../styles/v12/reader.css';

export interface TranscriptionsV12Props {
  toolbar: React.ReactNode;
  isLoading: boolean;
  items: TranscriptionMeta[];
  hasAny: boolean;
  onOpen: (t: TranscriptionMeta) => void;
  selectedId: string | null;
  detail: TranscriptionDetail | null | undefined;
  isLoadingDetail: boolean;
  onClose: () => void;
  onCopy: (text: string) => void;
  onAskAiWithContext?: (contextText: string, title: string) => void;
}

const secId = (i: number) => `tr-sec-${i + 1}`;

const TranscriptReader: React.FC<{
  meta: TranscriptionMeta;
  detail: TranscriptionDetail | null | undefined;
  loading: boolean;
  onClose: () => void;
  onCopy: (text: string) => void;
  onAskAiWithContext?: (contextText: string, title: string) => void;
}> = ({ meta, detail, loading, onClose, onCopy, onAskAiWithContext }) => {
  const scope = `transcript:${meta.id}`;
  const [marks, refreshMarks] = useScopeMarks(scope);
  const hlRef = useRef<HTMLDivElement>(null);
  const timer = useRef(0);
  const refreshSoon = () => {
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(refreshMarks, 260);
  };
  useEffect(() => () => window.clearTimeout(timer.current), []);
  const sections = detail?.sections || [];
  const toc: ReaderTocItem[] = useMemo(
    () => sections.map((s, i) => ({ id: secId(i), title: s.title || `Bölüm ${i + 1}`, level: s.level >= 3 ? (3 as const) : (2 as const) })),
    [sections]
  );
  const jump = (m: Parameters<typeof scrollToMark>[1]) => scrollToMark(hlRef.current?.querySelector<HTMLElement>('.r12-hl'), m);
  const d = detail || meta;

  return (
    <ReaderV12
      className={disciplineClass(meta.discipline)}
      title={meta.title}
      meta={`${meta.discipline} · ses kaydı · ~${meta.estimatedMinutes} dk`}
      onBack={onClose}
      backLabel="Ses kayıtlarına dön"
      toc={toc}
      onPointerUp={refreshSoon}
      onKeyUp={refreshSoon}
      tools={<HighlighterToolbar className="r12-pen" />}
      menu={
        <R12MenuGroup label="Transkript">
          <R12MenuItem icon={Copy} label="Metni kopyala" disabled={!detail} onClick={() => detail && onCopy(detail.content)} />
          {onAskAiWithContext && (
            <R12MenuItem icon={Sparkles} label="Asistana sor" disabled={!detail} onClick={() => detail && onAskAiWithContext(detail.content, detail.title)} />
          )}
        </R12MenuGroup>
      }
      margin={<ReaderPanel spots={null} marks={marks} onJump={jump} />}
      marginLabel="Notlarım"
      after={detail ? <ReaderPanel spots={null} marks={marks} onJump={jump} inline /> : undefined}
    >
      <div ref={hlRef} style={{ display: 'contents' }}>
        <Highlightable scope={scope} className="r12-hl">
          <header className="r12-head">
            <h1 className="r12-h1">{meta.title}</h1>
            <p className="r12-meta">
              <span>{meta.discipline}</span>
              <span>
                ~<b>{d.estimatedMinutes}</b> dk dinleme
              </span>
              <span>
                <b>{d.wordCount.toLocaleString('tr-TR')}</b> kelime
              </span>
              <span>
                <b>{d.sectionsCount}</b> bölüm
              </span>
            </p>
          </header>
          {loading && !detail ? (
            <div className="r12-skel" aria-busy="true" aria-label="Transkript yükleniyor">
              {Array.from({ length: 12 }, (_, k) => (
                <i key={k} />
              ))}
            </div>
          ) : !detail ? (
            <p className="r12-meta">Transkript yüklenemedi. Bağlantını kontrol edip yeniden aç.</p>
          ) : (
            <>
              {sections.map((s, i) => (
                <section key={i} className="r12-sec" data-r12-sec={secId(i)} aria-labelledby={`${secId(i)}-h`}>
                  {s.level >= 3 ? (
                    <h3 id={`${secId(i)}-h`} className="r12-h3">
                      {s.title}
                    </h3>
                  ) : (
                    <h2 id={`${secId(i)}-h`} className="r12-h2">
                      {s.title}
                    </h2>
                  )}
                  {String(s.content || '')
                    .split(/\n{2,}/)
                    .map((para) => para.trim())
                    .filter(Boolean)
                    .map((para, k) => (
                      <p key={k} className="r12-p">
                        {para}
                      </p>
                    ))}
                </section>
              ))}
              <p className="r12-meta">Bu transkript RAG vektör sisteminde aramalara açıktır.</p>
            </>
          )}
        </Highlightable>
      </div>
    </ReaderV12>
  );
};

export const TranscriptionsV12: React.FC<TranscriptionsV12Props> = ({
  toolbar,
  isLoading,
  items,
  hasAny,
  onOpen,
  selectedId,
  detail,
  isLoadingDetail,
  onClose,
  onCopy,
  onAskAiWithContext,
}) => {
  // Okuyucu ayrıntı gelmeden açılır (iskelet); başlık bilgisi listedeki kayıttan
  const [openMeta, setOpenMeta] = useState<TranscriptionMeta | null>(null);
  useEffect(() => {
    if (!selectedId) setOpenMeta(null);
  }, [selectedId]);

  return (
    <div className="r12-page">
      {toolbar}

      {isLoading ? (
        <ul className="r12-list" aria-busy="true" aria-label="Ses kaydı transkriptleri yükleniyor">
          {[0, 1, 2, 3, 4].map((k) => (
            <li key={k} className="r12-skel-row" aria-hidden>
              <i />
              <i />
            </li>
          ))}
        </ul>
      ) : items.length === 0 ? (
        <div className="r12-empty">
          <Mic aria-hidden />
          <h3>{hasAny ? 'Aramana uygun transkript yok' : 'Henüz transkript yok'}</h3>
          <p>{hasAny ? 'Arama kelimesini ya da branş süzgecini değiştir.' : 'Amfi ses kayıtları çözümlendikçe burada listelenir.'}</p>
        </div>
      ) : (
        <ul className="r12-list">
          {items.map((t) => (
            <li key={t.id} className={disciplineClass(t.discipline)}>
              <button
                type="button"
                className="r12-row"
                onClick={() => {
                  setOpenMeta(t);
                  onOpen(t);
                }}
              >
                <span className="r12-row-main">
                  <span className="r12-row-t">{t.title}</span>
                  <span className="r12-row-m">
                    <i className="r12-dot" aria-hidden />
                    <span>{t.discipline}</span>
                    <span>· {t.wordCount.toLocaleString('tr-TR')} kelime</span>
                    <span className="is-fill is-opt">· {t.sectionsCount} bölüm</span>
                  </span>
                  {t.firstSnippet && <span className="r12-snip">{t.firstSnippet}</span>}
                </span>
                <span className="r12-row-s">~{t.estimatedMinutes} dk</span>
                <ChevronRight className="r12-go" aria-hidden />
              </button>
            </li>
          ))}
        </ul>
      )}

      {selectedId && (openMeta || detail) && (
        <TranscriptReader
          meta={(openMeta || detail)!}
          detail={detail && detail.id === selectedId ? detail : null}
          loading={isLoadingDetail}
          onClose={onClose}
          onCopy={(text) => {
            onCopy(text);
            toast.success('Transkript metni kopyalandı');
          }}
          onAskAiWithContext={onAskAiWithContext}
        />
      )}
    </div>
  );
};
