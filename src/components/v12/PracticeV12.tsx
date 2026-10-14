import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { X, ChevronLeft, ChevronRight, LayoutGrid, Timer, Flag, Strikethrough, Pause, Play, Sparkles, BookOpen, RotateCcw } from 'lucide-react';
import { QuestionItem } from '../../types';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import '../../styles/v12/practice.css';

/**
 * v12 "Net" · Test ekranı ve sonuç (canvas panosu 10 "Test + sonuç").
 *  - TestRunnerV12: dikkat dağıtmayan test ekranı. Üst çubuk (Çık · başlık · Soru n/N · süre · Harita), ince ilerleme,
 *    ortada ≤720 px soru, alt çubuk (Önceki · İşaretle · Sonraki). Soru haritası ≥900 px'de sağ panel, altında alt sayfa.
 *    Veri ve işlev çağıranda kalır: PracticeMode (anında değerlendirme) ve Çalış › Test (sınav kipi, gözden geçirme) kullanır.
 *  - ResultsV12: tek satır sayı şeridi (başarı · D · Y · B · net = D − Y/4 · sn/soru), derslere göre tablo, yanlış listesi.
 */

export type OptState = 'idle' | 'sel' | 'ok' | 'bad' | 'dim';
export interface RunnerOption {
  key: string;
  text: string;
  state?: OptState;
  tag?: string;
  disabled?: boolean;
}
export interface RunnerCell {
  id: string;
  answered: boolean;
  flagged: boolean;
  /** Anında değerlendirme / gözden geçirmede doğru-yanlış tonu */
  tone?: 'ok' | 'bad';
}

const NARROW_Q = '(max-width: 899px)';
const isNarrow = () => typeof window !== 'undefined' && window.matchMedia(NARROW_Q).matches;

export const fmtClock = (sec: number) => {
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = sec % 60;
  return h > 0 ? `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}` : `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
};
const clockLabel = (sec: number) => {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m} dakika ${s} saniye`;
};
export const timerFor = (sec: number, kind: 'kalan' | 'gecen', tone?: 'low' | 'paused') => ({
  text: fmtClock(sec),
  label: `${kind === 'kalan' ? 'Kalan' : 'Geçen'} süre ${clockLabel(sec)}`,
  tone,
});

export interface TestRunnerV12Props {
  /** Kabuğun üstüne tam ekran katman olarak açılır (Çalış › Test); PracticeMode zaten tam sayfadır */
  overlay?: boolean;
  title: string;
  subtitle?: string;
  exitLabel?: string;
  onExit?: () => void;
  index: number;
  cells: RunnerCell[];
  onGo: (i: number) => void;
  timer?: { text: string; label: string; tone?: 'low' | 'paused' };
  /** Üst çubukta süreden sonra (ör. Duraklat) */
  headExtra?: React.ReactNode;
  qid: string;
  /** Soru başlığı solu (ders, yıl) */
  meta?: React.ReactNode;
  /** Soru başlığı sağı (AI'ya sor, Bildir) */
  tools?: React.ReactNode;
  stem: string;
  options: RunnerOption[];
  /** Verilmezse şıklar salt okunur (gözden geçirme) */
  onPick?: (key: string) => void;
  /** Şık eleme (üstünü çiz) düğmesi */
  eliminate?: boolean;
  flagged?: boolean;
  onFlag?: () => void;
  flagHint?: string;
  onPrev: () => void;
  prevDisabled?: boolean;
  onNext: () => void;
  nextLabel?: string;
  nextIsFinish?: boolean;
  nextDisabled?: boolean;
  /** Şıkların altında: geri bildirim, açıklama */
  children?: React.ReactNode;
  onFinish?: () => void;
  finishLabel?: string;
  /** Verilirse soru yerine gösterilir (duraklatıldı) */
  paused?: React.ReactNode;
  keysHint?: string;
}

export const TestRunnerV12: React.FC<TestRunnerV12Props> = ({
  overlay,
  title,
  subtitle,
  exitLabel = 'Çık',
  onExit,
  index,
  cells,
  onGo,
  timer,
  headExtra,
  qid,
  meta,
  tools,
  stem,
  options,
  onPick,
  eliminate,
  flagged,
  onFlag,
  flagHint,
  onPrev,
  prevDisabled,
  onNext,
  nextLabel = 'Sonraki',
  nextIsFinish,
  nextDisabled,
  children,
  onFinish,
  finishLabel = 'Testi bitir',
  paused,
  keysHint,
}) => {
  const total = cells.length;
  const [navOpen, setNavOpen] = useState(() => !isNarrow());
  const [narrow, setNarrow] = useState(isNarrow);
  const [elim, setElim] = useState<Record<string, string[]>>({});
  const scrollRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);
  const toggleRef = useRef<HTMLButtonElement>(null);

  // Ekran genişliği değişince harita kipini izle (sağ panel ↔ alt sayfa)
  useEffect(() => {
    const mq = window.matchMedia(NARROW_Q);
    const on = () => {
      setNarrow(mq.matches);
      setNavOpen(!mq.matches);
    };
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, []);

  // Tam ekran katmanda arka sayfa kaymaz
  useEffect(() => {
    if (!overlay) return;
    lockScroll();
    return () => unlockScroll();
  }, [overlay]);

  // Soru değişince okuma alanı başa döner
  useEffect(() => {
    scrollRef.current?.scrollTo({ top: 0 });
  }, [index]);

  const sheetOpen = narrow && navOpen;
  useEffect(() => {
    if (!sheetOpen) return;
    closeRef.current?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.stopPropagation();
        setNavOpen(false);
        toggleRef.current?.focus();
      }
    };
    document.addEventListener('keydown', onKey, true);
    return () => document.removeEventListener('keydown', onKey, true);
  }, [sheetOpen]);

  const go = useCallback(
    (i: number) => {
      onGo(i);
      if (isNarrow()) setNavOpen(false);
    },
    [onGo]
  );

  const elimSet = elim[qid] || [];
  const toggleElim = (k: string) =>
    setElim((p) => {
      const cur = p[qid] || [];
      return { ...p, [qid]: cur.includes(k) ? cur.filter((x) => x !== k) : [...cur, k] };
    });

  const counts = useMemo(() => {
    let answered = 0, flaggedN = 0, ok = 0, bad = 0;
    cells.forEach((c) => {
      if (c.answered) answered++;
      if (c.flagged) flaggedN++;
      if (c.tone === 'ok') ok++;
      if (c.tone === 'bad') bad++;
    });
    return { answered, flagged: flaggedN, empty: total - answered, ok, bad, toned: ok + bad > 0 };
  }, [cells, total]);

  const position = Math.min(index + 1, total);
  const pct = total ? (position / total) * 100 : 0;

  const screen = (
    <div className={`p12-run ${overlay ? 'is-overlay' : ''}`}>
      <header className="p12-top">
        {onExit && (
          <button type="button" onClick={onExit} className="p12-btn is-sm is-ghost p12-icon-xs" aria-label={exitLabel}>
            <X aria-hidden />
            <span>{exitLabel}</span>
          </button>
        )}
        <h1 className="p12-title p12-grow">
          <span className="p12-clamp1">{title}</span>
          {subtitle && <small className="p12-clamp1 p12-hide-xs">{subtitle}</small>}
        </h1>
        <span className="p12-pos" aria-label={`Soru ${position} / ${total}`}>
          <span className="p12-hide-xs">Soru </span>
          <b>
            {position} / {total}
          </b>
        </span>
        {timer && (
          <span className={`p12-timer ${timer.tone === 'low' ? 'is-low' : timer.tone === 'paused' ? 'is-paused' : ''}`} role="timer" aria-label={timer.label}>
            <Timer aria-hidden />
            {timer.text}
          </span>
        )}
        {headExtra}
        <button
          ref={toggleRef}
          type="button"
          onClick={() => setNavOpen((v) => !v)}
          aria-expanded={navOpen}
          aria-controls="p12-nav"
          className="p12-btn is-sm p12-icon-xs"
          aria-label="Soru haritası"
        >
          <LayoutGrid aria-hidden />
          <span>Harita</span>
        </button>
      </header>
      <div className="p12-prog" role="progressbar" aria-label="Test ilerlemesi" aria-valuemin={1} aria-valuemax={total} aria-valuenow={position}>
        <i style={{ width: `${pct}%` }} />
      </div>

      <div className="p12-body">
        <div className="p12-center">
          <div className="p12-scroll" ref={scrollRef}>
            <div className="p12-qwrap">
              {paused ? (
                <div className="p12-q">{paused}</div>
              ) : (
                <article className="p12-q" aria-labelledby="p12-stem">
                  <div className="p12-qhead">
                    <span className="p12-meta p12-num">Soru {position}</span>
                    {meta}
                    <span className="p12-grow" />
                    {flagged && <span className="p12-badge is-warn">İşaretli</span>}
                    {tools}
                  </div>
                  <p className="p12-stem" id="p12-stem">
                    {stem}
                  </p>
                  <ul className="p12-opts" role="radiogroup" aria-labelledby="p12-stem">
                    {options.map((o) => {
                      const st = o.state || 'idle';
                      const isElim = elimSet.includes(o.key);
                      const canElim = !!eliminate && !!onPick && !o.disabled && st !== 'ok' && st !== 'bad' && st !== 'sel';
                      return (
                        <li key={o.key} className={`p12-orow ${canElim ? 'has-elim' : ''} ${isElim ? 'is-elim' : ''}`}>
                          <button
                            type="button"
                            role="radio"
                            aria-checked={st === 'sel' || (st === 'bad') || (st === 'ok' && o.tag === 'Senin cevabın')}
                            onClick={onPick ? () => onPick(o.key) : undefined}
                            disabled={!onPick || o.disabled}
                            className={`p12-opt ${st !== 'idle' ? `is-${st}` : ''}`}
                          >
                            <span className="k" aria-hidden>
                              {o.key}
                            </span>
                            <span className="t">
                              {o.text}
                              {isElim && <span className="p12-sr"> (elendi)</span>}
                            </span>
                            {o.tag && <span className="tag">{o.tag}</span>}
                          </button>
                          {canElim && (
                            <button
                              type="button"
                              className="p12-elim"
                              aria-pressed={isElim}
                              aria-label={isElim ? `${o.key} şıkkını geri al` : `${o.key} şıkkını ele`}
                              title={isElim ? 'Elemeyi geri al' : 'Şıkkı ele (üstünü çiz)'}
                              onClick={() => toggleElim(o.key)}
                            >
                              <Strikethrough aria-hidden />
                            </button>
                          )}
                        </li>
                      );
                    })}
                  </ul>
                  {children}
                  {keysHint && <p className="p12-keys">{keysHint}</p>}
                </article>
              )}
            </div>
          </div>
          <div className="p12-foot">
            <div className="p12-foot-in">
              <button type="button" className="p12-btn" onClick={onPrev} disabled={(prevDisabled ?? index === 0) || !!paused} aria-label="Önceki soru">
                <ChevronLeft aria-hidden />
                <span className="p12-hide-xs">Önceki</span>
              </button>
              <span className="p12-grow" />
              {onFlag && (
                <button type="button" className={`p12-btn ${flagged ? 'is-on' : ''}`} aria-pressed={!!flagged} onClick={onFlag} disabled={!!paused} title={flagHint}>
                  <Flag aria-hidden fill={flagged ? 'currentColor' : 'none'} />
                  <span>{flagged ? 'İşaretli' : 'İşaretle'}</span>
                </button>
              )}
              <button type="button" className="p12-btn is-pri" onClick={onNext} disabled={nextDisabled || !!paused}>
                <span>{nextLabel}</span>
                {nextIsFinish ? <Flag aria-hidden /> : <ChevronRight aria-hidden />}
              </button>
            </div>
          </div>
        </div>

        {navOpen && (
          <>
            {narrow && <button type="button" className="p12-scrim" aria-label="Soru haritasını kapat" onClick={() => setNavOpen(false)} />}
            <aside className="p12-nav" id="p12-nav" aria-label="Soru haritası" role={narrow ? 'dialog' : undefined} aria-modal={narrow || undefined}>
              <span className="p12-handle" aria-hidden />
              <div className="p12-nav-h">
                <h2 className="p12-h2 p12-grow">Soru haritası</h2>
                <button ref={closeRef} type="button" className="p12-btn is-icon is-sm is-ghost" aria-label="Soru haritasını kapat" onClick={() => setNavOpen(false)}>
                  <X aria-hidden />
                </button>
              </div>
              <div className="p12-legend" aria-hidden>
                {counts.toned ? (
                  <>
                    <span><i className="p12-sw ok" />Doğru</span>
                    <span><i className="p12-sw bad" />Yanlış</span>
                  </>
                ) : (
                  <span><i className="p12-sw a" />Cevaplandı</span>
                )}
                <span><i className="p12-sw f" />İşaretli</span>
                <span><i className="p12-sw c" />Şu an</span>
                <span><i className="p12-sw" />Boş</span>
              </div>
              <nav className="p12-grid" aria-label="Sorular">
                {cells.map((c, i) => {
                  const isCur = i === index;
                  const cls = ['p12-cell', c.tone ? c.tone : c.answered ? 'a' : '', c.flagged ? 'f' : '', isCur ? 'c' : ''].filter(Boolean).join(' ');
                  const desc = [
                    `Soru ${i + 1}`,
                    isCur ? 'şu an' : '',
                    c.tone === 'ok' ? 'doğru' : c.tone === 'bad' ? 'yanlış' : c.answered ? 'cevaplandı' : 'boş',
                    c.flagged ? 'işaretli' : '',
                  ]
                    .filter(Boolean)
                    .join(', ');
                  return (
                    <button key={c.id} type="button" className={cls} aria-label={desc} aria-current={isCur ? 'step' : undefined} onClick={() => go(i)}>
                      {i + 1}
                    </button>
                  );
                })}
              </nav>
              <hr className="p12-sep" />
              <div className="p12-counts" aria-live="polite">
                {counts.toned ? (
                  <>
                    <span>Doğru <b>{counts.ok}</b></span>
                    <span>Yanlış <b>{counts.bad}</b></span>
                  </>
                ) : (
                  <span>Cevaplanan <b>{counts.answered}</b></span>
                )}
                <span>İşaretli <b>{counts.flagged}</b></span>
                <span>Boş <b>{counts.empty}</b></span>
              </div>
              {onFinish && (
                <button type="button" className="p12-btn is-block" onClick={onFinish}>
                  {finishLabel}
                </button>
              )}
            </aside>
          </>
        )}
      </div>
    </div>
  );
  // Katman, dönüşüm animasyonlu atalardan (sayfa girişi, sekme paneli) etkilenmesin diye body'ye taşınır
  return overlay && typeof document !== 'undefined' ? createPortal(screen, document.body) : screen;
};

/* =============================================================================
 * Sonuç
 * ============================================================================= */
export interface ResultsDiscRow {
  name: string;
  correct: number;
  wrong: number | null;
  blank: number | null;
  total: number;
}
export interface ResultsListRow {
  i: number;
  stem: string;
  discipline?: string;
  your?: string;
  right?: string;
  flagged?: boolean;
}
export interface ResultsV12Props {
  /** Verilirse üst çubuklu tam sayfa (PracticeMode); verilmezse sayfa içi başlık (Çalış) */
  page?: boolean;
  title: string;
  durationSec: number;
  total: number;
  correct: number;
  wrong: number;
  blank: number;
  disc: ResultsDiscRow[];
  listTitle: string;
  rows: ResultsListRow[];
  filter?: { value: string; options: { value: string; label: string; n: number }[]; onChange: (v: string) => void };
  onOpenRow: (i: number) => void;
  reviewLabel?: string;
  onReview?: () => void;
  backLabel?: string;
  onBack?: () => void;
  actions?: React.ReactNode;
  emptyText?: string;
}

const pctText = (n: number) => `%${n.toLocaleString('tr-TR', { maximumFractionDigits: 1 })}`;
const LIST_STEP = 5;

export const ResultsV12: React.FC<ResultsV12Props> = ({
  page,
  title,
  durationSec,
  total,
  correct,
  wrong,
  blank,
  disc,
  listTitle,
  rows,
  filter,
  onOpenRow,
  reviewLabel = 'Gözden geçir',
  onReview,
  backLabel,
  onBack,
  actions,
  emptyText = 'Bu grupta soru yok.',
}) => {
  const [shown, setShown] = useState(LIST_STEP);
  useEffect(() => setShown(LIST_STEP), [filter?.value]);
  const pct = total ? (correct / total) * 100 : 0;
  const net = correct - wrong / 4;
  const perQ = total ? Math.round(durationSec / total) : 0;
  const discSorted = useMemo(() => [...disc].sort((a, b) => b.total - a.total), [disc]);

  const body = (
    <div className={`p12-res ${page ? '' : 'is-inline'}`}>
      {!page && (
        <div className="p12-reshead">
          {onBack && (
            <button type="button" className="p12-btn is-sm is-ghost" onClick={onBack}>
              <ChevronLeft aria-hidden /> {backLabel}
            </button>
          )}
          <h2 className="p12-h2 p12-grow p12-clamp1">{title}</h2>
          <span className="p12-meta">
            Süre <b>{fmtClock(durationSec)}</b>
          </span>
        </div>
      )}

      <section className="p12-panel p12-sum" aria-label="Özet">
        <div className="p12-stat">
          <span className="p12-meta">Başarı</span>
          <span className="v">{pctText(pct)}</span>
        </div>
        <div className="p12-stat">
          <span className="p12-meta">Doğru</span>
          <span className="v ok">{correct}</span>
        </div>
        <div className="p12-stat">
          <span className="p12-meta">Yanlış</span>
          <span className="v bad">{wrong}</span>
        </div>
        <div className="p12-stat">
          <span className="p12-meta">Boş</span>
          <span className="v">{blank}</span>
        </div>
        <div className="p12-stat">
          <span className="p12-meta">
            Net <span className="p12-num">(D − Y/4)</span>
          </span>
          <span className="v">{net.toLocaleString('tr-TR', { maximumFractionDigits: 2 })}</span>
        </div>
        <div className="p12-stat">
          <span className="p12-meta">Ortalama</span>
          <span className="v">
            {perQ} <small>sn/soru</small>
          </span>
        </div>
      </section>

      {discSorted.length > 0 && (
        <section className="p12-panel" aria-labelledby="p12-ders-h">
          <div className="p12-panel-h">
            <h2 className="p12-h2 p12-grow" id="p12-ders-h">
              Derslere göre
            </h2>
            <span className="p12-meta">
              <span className="p12-num">{discSorted.length}</span> ders
            </span>
          </div>
          <div className="p12-tblbox">
            <table className="p12-tbl">
              <thead>
                <tr>
                  <th scope="col">Ders</th>
                  <th scope="col" className="r">Doğru</th>
                  <th scope="col" className="r">Yanlış</th>
                  <th scope="col" className="r">Boş</th>
                  <th scope="col">Oran</th>
                </tr>
              </thead>
              <tbody>
                {discSorted.map((d) => {
                  const p = d.total ? Math.round((d.correct / d.total) * 100) : 0;
                  return (
                    <tr key={d.name}>
                      <td className="d">{d.name}</td>
                      <td className="r">{d.correct}</td>
                      <td className="r">{d.wrong ?? '—'}</td>
                      <td className="r">{d.blank ?? '—'}</td>
                      <td>
                        <div className="p12-rate">
                          <div className="p12-bar" aria-hidden>
                            <i style={{ width: `${p}%` }} />
                          </div>
                          <span className="p12-num">%{p}</span>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      )}

      <section className="p12-panel" aria-labelledby="p12-list-h">
        <div className="p12-panel-h">
          <h2 className="p12-h2 p12-grow" id="p12-list-h">
            {listTitle}
          </h2>
          <span className="p12-meta">
            <span className="p12-num">{rows.length}</span> soru
          </span>
          {onReview && (
            <button type="button" className="p12-btn is-pri is-sm" onClick={onReview}>
              {reviewLabel}
            </button>
          )}
        </div>
        {filter && (
          <div className="p12-panel-h">
            <div className="p12-seg" role="radiogroup" aria-label="Listeyi süz">
              {filter.options.map((o) => (
                <button key={o.value} type="button" role="radio" aria-checked={filter.value === o.value} onClick={() => filter.onChange(o.value)}>
                  {o.label}
                  <b>{o.n}</b>
                </button>
              ))}
            </div>
          </div>
        )}
        {rows.length === 0 ? (
          <p className="p12-empty">{emptyText}</p>
        ) : (
          <>
            <ul className="p12-wlist">
              {rows.slice(0, shown).map((r) => (
                <li key={r.i}>
                  <button type="button" className="p12-wrow" onClick={() => onOpenRow(r.i)} aria-label={`Soru ${r.i + 1}: incele`}>
                    <span className="n">S {r.i + 1}</span>
                    <span className="p12-grow">
                      <span className="s p12-clamp2">{r.stem}</span>
                      <span className="p12-meta">
                        {[
                          r.discipline,
                          r.your && r.right && r.your !== r.right ? `senin cevabın ${r.your}, doğrusu ${r.right}` : r.your && r.right ? `cevabın ${r.your}, doğru` : r.right ? `boş, doğrusu ${r.right}` : '',
                          r.flagged ? 'işaretli' : '',
                        ]
                          .filter(Boolean)
                          .join(' · ')}
                      </span>
                    </span>
                  </button>
                </li>
              ))}
            </ul>
            {rows.length > shown && (
              <div className="p12-more">
                <button type="button" className="p12-btn is-sm is-ghost" onClick={() => setShown((s) => s + 20)}>
                  {Math.min(20, rows.length - shown)} soru daha göster
                </button>
              </div>
            )}
          </>
        )}
      </section>

      {actions && <div className="p12-res-act">{actions}</div>}
    </div>
  );

  if (!page) return body;
  return (
    <div className="p12-respage">
      <header className="p12-top">
        {onBack && (
          <button type="button" className="p12-btn is-sm is-ghost p12-icon-xs" onClick={onBack} aria-label={backLabel}>
            <ChevronLeft aria-hidden />
            <span>{backLabel}</span>
          </button>
        )}
        <h1 className="p12-title p12-grow">
          <span className="p12-clamp1">{title} · Sonuç</span>
        </h1>
        <span className="p12-pos">
          Süre <b>{fmtClock(durationSec)}</b>
        </span>
      </header>
      {body}
    </div>
  );
};

/* =============================================================================
 * PracticeMode (/test) bağlantısı: anında değerlendirmeli test + sonuç
 * ============================================================================= */
export interface PracticeV12Props {
  title: string;
  subtitle?: string;
  items: QuestionItem[];
  index: number;
  answers: Record<string, string>;
  marked: Set<string>;
  elapsed: number;
  paused: boolean;
  finished: boolean;
  shortExplanation: string;
  onSelect: (key: string) => void;
  onReset: () => void;
  onToggleMark: () => void;
  onGo: (i: number) => void;
  onFinish: () => void;
  onRestart: () => void;
  onReview: () => void;
  onTogglePause: () => void;
  onOpenAi: () => void;
  onOpenQuestion?: (q: QuestionItem) => void;
  onExit?: () => void;
}

export const PracticeV12: React.FC<PracticeV12Props> = (p) => {
  const { items, index, answers, marked } = p;
  const total = items.length;
  const q = items[Math.min(index, Math.max(total - 1, 0))];
  const rec = q.reconstruction!;
  const userAnswer = answers[q.id];
  const isAnswered = !!userAnswer;
  const isCorrect = isAnswered && userAnswer === rec.correctAnswer;
  const atEnd = index >= total - 1;

  const cells = useMemo<RunnerCell[]>(
    () =>
      items.map((it) => {
        const a = answers[it.id];
        return { id: it.id, answered: !!a, flagged: marked.has(it.id), tone: a ? (a === it.reconstruction?.correctAnswer ? 'ok' : 'bad') : undefined };
      }),
    [items, answers, marked]
  );

  if (p.finished) {
    return <PracticeResultsV12 items={items} answers={answers} marked={marked} elapsed={p.elapsed} onGo={p.onGo} onReview={p.onReview} onRestart={p.onRestart} onExit={p.onExit} title={p.title} page />;
  }

  const options: RunnerOption[] = rec.options.map((o0, oi) => {
    const key = o0.key || 'ABCDE'[oi];
    const isThis = rec.correctAnswer === key;
    const picked = userAnswer === key;
    const state: OptState = isAnswered ? (isThis ? 'ok' : picked ? 'bad' : 'dim') : 'idle';
    return {
      key,
      text: o0.text,
      state,
      tag: isAnswered && isThis ? (picked ? 'Senin cevabın' : 'Doğru') : isAnswered && picked ? 'Senin cevabın' : undefined,
      disabled: (isAnswered && !picked && !isThis) || p.paused,
    };
  });

  return (
    <TestRunnerV12
      title={p.title}
      subtitle={p.subtitle}
      exitLabel="Çık"
      onExit={p.onExit}
      index={index}
      cells={cells}
      onGo={p.onGo}
      timer={timerFor(p.elapsed, 'gecen', p.paused ? 'paused' : undefined)}
      headExtra={
        <button
          type="button"
          className="p12-btn is-sm is-icon"
          onClick={p.onTogglePause}
          aria-pressed={p.paused}
          aria-label={p.paused ? 'Devam et' : 'Duraklat'}
          title={p.paused ? 'Devam et (P)' : 'Duraklat (P)'}
        >
          {p.paused ? <Play aria-hidden /> : <Pause aria-hidden />}
        </button>
      }
      qid={q.id}
      meta={q.discipline ? <span className="p12-badge">{q.discipline}</span> : null}
      tools={
        <button type="button" className="p12-btn is-sm is-ghost is-acc" onClick={p.onOpenAi} title="Bu soruyu yapay zekâya sor">
          <Sparkles aria-hidden />
          <span>AI'ya sor</span>
        </button>
      }
      stem={rec.stem}
      options={options}
      onPick={isAnswered || p.paused ? undefined : p.onSelect}
      eliminate
      flagged={marked.has(q.id)}
      onFlag={p.onToggleMark}
      flagHint="İşaretle (M)"
      onPrev={() => p.onGo(index - 1)}
      onNext={() => (atEnd ? p.onFinish() : p.onGo(index + 1))}
      nextLabel={atEnd ? 'Testi bitir' : isAnswered ? 'Sonraki' : 'Atla'}
      nextIsFinish={atEnd}
      onFinish={p.onFinish}
      paused={
        p.paused ? (
          <div className="p12-pause" role="dialog" aria-label="Test duraklatıldı">
            <Pause aria-hidden />
            <b>Test duraklatıldı</b>
            <span className="p12-meta">
              Süre durdu · <b>{fmtClock(p.elapsed)}</b>
            </span>
            <button type="button" className="p12-btn is-pri" onClick={p.onTogglePause} autoFocus>
              <Play aria-hidden /> Devam et
            </button>
          </div>
        ) : undefined
      }
      keysHint="Kısayollar: A–E cevap · ← → soru · M işaretle · P duraklat"
    >
      {isAnswered && (
        <section className="p12-verdict" role="status">
          <div className={`p12-verdict-h ${isCorrect ? 'is-ok' : 'is-bad'}`}>{isCorrect ? 'Doğru' : `Yanlış · doğru cevap ${rec.correctAnswer}`}</div>
          {p.shortExplanation && <p className="p12-verdict-b">{p.shortExplanation}</p>}
          <div className="p12-verdict-act">
            <button type="button" className="p12-btn is-sm is-acc" onClick={p.onOpenAi}>
              <Sparkles aria-hidden />
              {isCorrect ? 'Mekanizmayı sor' : 'Neden yanlış? Sor'}
            </button>
            {p.onOpenQuestion && (
              <button type="button" className="p12-btn is-sm" onClick={() => p.onOpenQuestion!(q)}>
                <BookOpen aria-hidden />
                Tam açıklama
              </button>
            )}
            <button type="button" className="p12-btn is-sm is-ghost" onClick={p.onReset}>
              <RotateCcw aria-hidden />
              Tekrar dene
            </button>
          </div>
        </section>
      )}
    </TestRunnerV12>
  );
};

/** PracticeMode sonuç ekranı (v12). TestResults v12 dalı da bunu kullanır. */
export const PracticeResultsV12: React.FC<{
  items: QuestionItem[];
  answers: Record<string, string>;
  marked: Set<string>;
  elapsed: number;
  onGo: (i: number) => void;
  onReview: () => void;
  onRestart: () => void;
  onExit?: () => void;
  title?: string;
  page?: boolean;
}> = ({ items, answers, marked, elapsed, onGo, onReview, onRestart, onExit, title = 'Test', page }) => {
  const [filter, setFilter] = useState<'wrong' | 'flag' | 'blank'>('wrong');
  const sum = useMemo(() => {
    const wrong: number[] = [];
    const blank: number[] = [];
    const flag: number[] = [];
    let correct = 0;
    const byDisc = new Map<string, ResultsDiscRow>();
    items.forEach((q, i) => {
      const a = answers[q.id];
      const k = q.discipline || 'Diğer';
      const r = byDisc.get(k) || { name: k, correct: 0, wrong: 0, blank: 0, total: 0 };
      r.total++;
      if (!a) {
        blank.push(i);
        r.blank!++;
      } else if (a === q.reconstruction?.correctAnswer) {
        correct++;
        r.correct++;
      } else {
        wrong.push(i);
        r.wrong!++;
      }
      byDisc.set(k, r);
      if (marked.has(q.id)) flag.push(i);
    });
    return { wrong, blank, flag, correct, disc: [...byDisc.values()] };
  }, [items, answers, marked]);

  const list = filter === 'wrong' ? sum.wrong : filter === 'flag' ? sum.flag : sum.blank;
  const rows: ResultsListRow[] = list.map((i) => {
    const q = items[i];
    return { i, stem: q.reconstruction?.stem || '', discipline: q.discipline, your: answers[q.id], right: q.reconstruction?.correctAnswer, flagged: filter !== 'flag' && marked.has(q.id) };
  });

  return (
    <ResultsV12
      page={page}
      title={title}
      durationSec={elapsed}
      total={items.length}
      correct={sum.correct}
      wrong={sum.wrong.length}
      blank={sum.blank.length}
      disc={sum.disc}
      listTitle={filter === 'wrong' ? 'Yanlışların' : filter === 'flag' ? 'İşaretlediklerin' : 'Boş bıraktıkların'}
      rows={rows}
      filter={{
        value: filter,
        onChange: (v) => setFilter(v as typeof filter),
        options: [
          { value: 'wrong', label: 'Yanlış', n: sum.wrong.length },
          { value: 'flag', label: 'İşaretli', n: sum.flag.length },
          { value: 'blank', label: 'Boş', n: sum.blank.length },
        ],
      }}
      onOpenRow={onGo}
      reviewLabel={list.length ? 'Gözden geçir' : 'Soruları incele'}
      onReview={list.length ? () => onGo(list[0]) : onReview}
      backLabel="Çalış'a dön"
      onBack={onExit}
      emptyText={filter === 'wrong' ? 'Yanlış yok.' : filter === 'flag' ? 'İşaretlediğin soru yok.' : 'Boş bıraktığın soru yok.'}
      actions={
        <>
          <button type="button" className="p12-btn" onClick={onReview}>
            Soruları incele
          </button>
          <button type="button" className="p12-btn is-ghost" onClick={onRestart}>
            <RotateCcw aria-hidden /> Yeniden başla
          </button>
        </>
      }
    />
  );
};

/** /test boş durum (v12) */
export const PracticeEmptyV12: React.FC<{ title: string; onExit?: () => void; onContribute: () => void }> = ({ title, onExit, onContribute }) => (
  <div className="p12-respage">
    <header className="p12-top">
      {onExit && (
        <button type="button" onClick={onExit} className="p12-btn is-sm is-ghost p12-icon-xs" aria-label="Testten çık">
          <X aria-hidden />
          <span>Çık</span>
        </button>
      )}
      <h1 className="p12-title p12-grow">
        <span className="p12-clamp1">{title}</span>
      </h1>
    </header>
    <div className="p12-res">
      <section className="p12-panel" aria-labelledby="p12-empty-h">
        <div className="p12-panel-h">
          <h2 className="p12-h2" id="p12-empty-h">
            Çözülecek soru henüz yok
          </h2>
        </div>
        <p className="p12-empty" style={{ color: 'var(--color-ink-2)' }}>
          Testte yalnızca yeniden kurulup doğrulanan sorular çıkar. Çıkmış sorularla pratik yapmak için Çalış sayfasını açabilir ya da bu kurula bir parça ekleyebilirsin.
        </p>
        <div className="p12-more p12-res-act">
          {onExit && (
            <button type="button" onClick={onExit} className="p12-btn is-pri">
              Çalış'a dön
            </button>
          )}
          <button type="button" onClick={onContribute} className="p12-btn">
            Parça ekle
          </button>
        </div>
      </section>
    </div>
  </div>
);
