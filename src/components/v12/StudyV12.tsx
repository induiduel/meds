import React, { useMemo, useState } from 'react';
import { createPortal } from 'react-dom';
import { Zap, Play, Trash2, RotateCcw, Bookmark, BookmarkCheck, Sparkles } from 'lucide-react';
import { StudyQuestion, SelfTestResult, OptionKey, getReview, setInReview } from '../../services/studyStore';
import { ExplanationBlock, formatDuration } from '../study/StudyUI';
import { StudyReportButton } from '../study/StudyReportButton';
import { QuestionAiChatDrawer } from '../QuestionAiChatDrawer';
import { TestRunnerV12, ResultsV12, RunnerCell, RunnerOption, ResultsDiscRow, ResultsListRow, fmtClock } from './PracticeV12';
import '../../styles/v12/practice.css';

/**
 * v12 "Net" · Çalış (/calis) — başlık + sekmeler, Test sekmesinin kurulum formu, sonuç ve gözden geçirme.
 * Veri ve işlev StudyHub / SelfTestView'da kalır; bu dosya yalnız v12 yapısını kurar (canvas panosu 10 ile aynı dil).
 */

/* ── Çalış başlığı + sekmeler ─────────────────────────────────────────────── */
export interface StudyHubV12Tab {
  id: string;
  label: string;
  icon: React.ElementType;
  count?: number;
}
export const StudyHubV12: React.FC<{
  loading: boolean;
  bankSize: number;
  solved: number;
  accuracy: number;
  tabs: StudyHubV12Tab[];
  section: string;
  onSection: (id: string) => void;
  onQuick: () => void;
  children: React.ReactNode;
}> = ({ loading, bankSize, solved, accuracy, tabs, section, onSection, onQuick, children }) => {
  const onTabKey = (e: React.KeyboardEvent, i: number) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    e.preventDefault();
    const n = (i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
    onSection(tabs[n].id);
    (e.currentTarget.parentElement?.children[n] as HTMLElement | undefined)?.focus();
  };
  return (
    <div className="p12-hub">
      <header className="p12-hub-h">
        <h1>Çalış</h1>
        <span className="p12-meta p12-grow">
          {loading && bankSize === 0 ? (
            'Soru bankası yükleniyor…'
          ) : (
            <>
              <b>{bankSize.toLocaleString('tr-TR')}</b> soru
              {solved > 0 && (
                <>
                  {' · '}
                  <b>{solved.toLocaleString('tr-TR')}</b> çözülen · <b>{accuracy}%</b> doğru
                </>
              )}
            </>
          )}
        </span>
        <button type="button" className="p12-btn is-pri" onClick={onQuick} disabled={bankSize === 0} title="Karışık 20 soruluk hızlı test">
          <Zap aria-hidden /> Hızlı test
        </button>
      </header>
      <div className="p12-tabs" role="tablist" aria-label="Çalışma bölümleri">
        {tabs.map((t, i) => {
          const Icon = t.icon;
          const on = section === t.id;
          return (
            <button
              key={t.id}
              type="button"
              role="tab"
              id={`study-tab-${t.id}`}
              aria-selected={on}
              aria-controls={`study-panel-${t.id}`}
              tabIndex={on ? 0 : -1}
              className="p12-tab"
              onClick={() => onSection(t.id)}
              onKeyDown={(e) => onTabKey(e, i)}
            >
              <Icon aria-hidden />
              {t.label}
              {t.count ? <span className="n">{t.count}</span> : null}
            </button>
          );
        })}
      </div>
      {children}
    </div>
  );
};

/* ── Test kurulumu ───────────────────────────────────────────────────────── */
type TimeMode = 'none' | '60' | '90';
export interface SelfTestSetupV12Props {
  loading: boolean;
  bankSize: number;
  committeeId: string;
  committeeOptions: { id: string; label: string; n: number }[];
  onCommittee: (id: string) => void;
  timeMode: TimeMode;
  onTimeMode: (v: TimeMode) => void;
  count: number;
  onCount: (n: number) => void;
  disciplineCounts: [string, number][];
  picked: string[];
  onToggleDiscipline: (d: string) => void;
  onClearPicked: () => void;
  onlyUnsolved: boolean;
  onOnlyUnsolved: (v: boolean) => void;
  poolSize: number;
  onStart: () => void;
  history: SelfTestResult[];
  onOpenHistory: (h: SelfTestResult) => void;
  onClearHistory: () => void;
}

export const SelfTestSetupV12: React.FC<SelfTestSetupV12Props> = (p) => {
  const effective = Math.min(p.count, p.poolSize);
  return (
    <div className="p12-setup">
      <section className="p12-panel" aria-labelledby="p12-setup-h">
        <div className="p12-form">
          <div className="p12-form-h">
            <h2 className="p12-h2" id="p12-setup-h">
              Deneme oluştur
            </h2>
            <p>Çıkmış ve kurulan sorulardan rastgele bir deneme. Bitirince ders ders sonucunu görürsün.</p>
          </div>

          <div className="p12-frow">
            <div>
              <label className="p12-label" htmlFor="p12-kurul">
                Kurul
              </label>
              <div className="p12-field">
                <select id="p12-kurul" value={p.committeeId} onChange={(e) => p.onCommittee(e.target.value)}>
                  <option value="all">Tüm kurullar ({p.bankSize})</option>
                  {p.committeeOptions.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.label} ({c.n})
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <div>
              <span className="p12-label" id="p12-sure-l">
                Süre
              </span>
              <div className="p12-seg" role="radiogroup" aria-labelledby="p12-sure-l">
                {(
                  [
                    ['none', 'Süresiz'],
                    ['60', '1 dk/soru'],
                    ['90', '1,5 dk/soru'],
                  ] as [TimeMode, string][]
                ).map(([v, l]) => (
                  <button key={v} type="button" role="radio" aria-checked={p.timeMode === v} onClick={() => p.onTimeMode(v)}>
                    {l}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div>
            <span className="p12-label" id="p12-sayi-l">
              Soru sayısı
            </span>
            <div className="p12-seg" role="radiogroup" aria-labelledby="p12-sayi-l">
              {[10, 20, 40, 60, 100].map((n) => (
                <button key={n} type="button" role="radio" aria-checked={p.count === n} onClick={() => p.onCount(n)} className="p12-num">
                  {n}
                </button>
              ))}
            </div>
          </div>

          <fieldset className="p12-fs">
            <legend>
              <span className="p12-label">Dersler</span>
              <span className="p12-meta">{p.picked.length ? `${p.picked.length} seçili` : 'hepsi'}</span>
              {p.picked.length > 0 && (
                <button type="button" className="p12-linkbtn" onClick={p.onClearPicked}>
                  Temizle
                </button>
              )}
            </legend>
            <div className="p12-pills">
              {p.disciplineCounts.map(([d, n]) => (
                <button key={d} type="button" className="p12-pill" aria-pressed={p.picked.includes(d)} onClick={() => p.onToggleDiscipline(d)}>
                  <span>{d}</span>
                  <b>{n}</b>
                </button>
              ))}
            </div>
          </fieldset>

          <label className="p12-check">
            <input type="checkbox" role="switch" className="p12-switch" checked={p.onlyUnsolved} onChange={(e) => p.onOnlyUnsolved(e.target.checked)} />
            Yalnızca daha önce çözmediğim sorular
          </label>
        </div>

        <div className="p12-setup-foot">
          <span className="p12-meta p12-grow">
            <b>{effective}</b> soru
            {p.timeMode !== 'none' && effective > 0 && (
              <>
                {' · '}
                <b>{formatDuration(Math.round(effective * Number(p.timeMode)))}</b> süre
              </>
            )}
            {p.poolSize < p.count && p.poolSize > 0 && (
              <span className="p12-warn">
                {' · '}bu filtrede {p.poolSize} soru var{' '}
                <button type="button" className="p12-linkbtn" onClick={() => p.onCount(p.poolSize)}>
                  tamamını seç
                </button>
              </span>
            )}
          </span>
          <button type="button" className="p12-btn is-pri" onClick={p.onStart} disabled={p.loading || effective === 0}>
            <Play aria-hidden /> {p.loading && p.bankSize === 0 ? 'Sorular yükleniyor…' : 'Teste başla'}
          </button>
        </div>
      </section>

      <section className="p12-panel" aria-labelledby="p12-hist-h">
        <div className="p12-panel-h">
          <h2 className="p12-h2 p12-grow" id="p12-hist-h">
            Geçmiş denemeler
          </h2>
          {p.history.length > 0 && (
            <button type="button" className="p12-btn is-sm is-ghost is-danger" onClick={p.onClearHistory}>
              <Trash2 aria-hidden /> Temizle
            </button>
          )}
        </div>
        {p.history.length === 0 ? (
          <p className="p12-empty">İlk denemeni çözdüğünde sonuçların burada listelenir.</p>
        ) : (
          <ul className="p12-wlist">
            {p.history.slice(0, 10).map((h) => {
              const pct = Math.round((h.correct / Math.max(1, h.total)) * 100);
              return (
                <li key={h.id}>
                  <button type="button" className="p12-hrow" onClick={() => p.onOpenHistory(h)}>
                    <span className="t">{h.title}</span>
                    <span className="p">{pct}%</span>
                    <span className="p12-meta">
                      {new Date(h.at).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })} · {h.correct}/{h.total} ·{' '}
                      {formatDuration(h.durationSec)}
                    </span>
                    <span className="p12-bar" aria-hidden>
                      <i style={{ width: `${pct}%` }} />
                    </span>
                  </button>
                </li>
              );
            })}
          </ul>
        )}
      </section>
    </div>
  );
};

/* ── Sonuç + gözden geçirme ──────────────────────────────────────────────── */
type ResFilter = 'wrong' | 'blank' | 'correct' | 'all';

export const SelfTestResultV12: React.FC<{
  result: SelfTestResult;
  items: StudyQuestion[];
  onRestart: () => void;
  onAddWrongToReview: () => void;
}> = ({ result, items, onRestart, onAddWrongToReview }) => {
  const [filter, setFilter] = useState<ResFilter>(() => (result.wrong > 0 ? 'wrong' : result.blank > 0 ? 'blank' : 'all'));
  const [added, setAdded] = useState(false);
  const [review, setReview] = useState<number | null>(null);
  const [chatQuestion, setChatQuestion] = useState<StudyQuestion | null>(null);
  const [, setTick] = useState(0);

  const disc = useMemo<ResultsDiscRow[]>(() => {
    // Ders bazında yanlış/boş yalnız sorular hâlâ bankadaysa hesaplanır; yoksa kayıtlı doğru/toplam gösterilir
    const complete = items.length === result.questionIds.length;
    return Object.entries(result.byDiscipline).map(([name, s]) => {
      if (!complete) return { name, correct: s.correct, wrong: null, blank: null, total: s.total };
      let wrong = 0, blank = 0;
      items.forEach((q) => {
        if (q.discipline !== name) return;
        const a = result.answers[q.id];
        if (!a) blank++;
        else if (a !== q.answer) wrong++;
      });
      return { name, correct: s.correct, wrong, blank, total: s.total };
    });
  }, [items, result]);

  const groups = useMemo(() => {
    const g: Record<ResFilter, number[]> = { wrong: [], blank: [], correct: [], all: [] };
    items.forEach((q, i) => {
      const a = result.answers[q.id];
      g.all.push(i);
      if (!a) g.blank.push(i);
      else if (a === q.answer) g.correct.push(i);
      else g.wrong.push(i);
    });
    return g;
  }, [items, result]);

  const rows: ResultsListRow[] = groups[filter].map((i) => {
    const q = items[i];
    return { i, stem: q.stem, discipline: q.discipline, your: result.answers[q.id], right: q.answer };
  });

  const reviewList = groups[filter].length ? groups[filter] : groups.all;

  if (review !== null && items[review]) {
    const q = items[review];
    const a = result.answers[q.id] as OptionKey | undefined;
    const pos = reviewList.indexOf(review);
    const cells: RunnerCell[] = items.map((it) => {
      const ans = result.answers[it.id];
      return { id: it.id, answered: !!ans, flagged: false, tone: ans ? (ans === it.answer ? 'ok' : 'bad') : undefined };
    });
    const options: RunnerOption[] = q.options.map((o) => ({
      key: o.key,
      text: o.text,
      state: o.key === q.answer ? 'ok' : o.key === a ? 'bad' : 'dim',
      tag: o.key === a ? 'Senin cevabın' : o.key === q.answer ? 'Doğru cevap' : undefined,
    }));
    const inReview = getReview().has(q.id);
    // Önceki/Sonraki seçili gruptaki sorular arasında gezer; harita tüm sorulara açıktır
    const step = (d: number) => {
      const next = pos !== -1 ? reviewList[pos + d] : d > 0 ? reviewList.find((x) => x > review) : [...reviewList].reverse().find((x) => x < review);
      if (next !== undefined) setReview(next);
    };
    const atEnd = pos !== -1 ? pos >= reviewList.length - 1 : !reviewList.some((x) => x > review);
    const atStart = pos !== -1 ? pos === 0 : !reviewList.some((x) => x < review);
    return (
      <>
        <TestRunnerV12
          overlay
          title={`${result.title} · Gözden geçir`}
          exitLabel="Sonuca dön"
          onExit={() => setReview(null)}
          index={review}
          cells={cells}
          onGo={setReview}
          timer={{ text: fmtClock(result.durationSec), label: `Test süresi ${fmtClock(result.durationSec)}` }}
          qid={q.id}
          meta={
            <>
              {q.discipline && <span className="p12-badge">{q.discipline}</span>}
              {(q.year || q.number) && <span className="p12-meta">{[q.year, q.number ? `S${q.number}` : null].filter(Boolean).join(' · ')}</span>}
            </>
          }
          tools={<StudyReportButton q={q} compact className="p12-btn is-sm is-ghost" />}
          stem={q.stem}
          options={options}
          onPrev={() => step(-1)}
          prevDisabled={atStart}
          onNext={() => (atEnd ? setReview(null) : step(1))}
          nextLabel={atEnd ? 'Sonuca dön' : 'Sonraki'}
        >
          <section className="p12-verdict" aria-label="Açıklama">
            <div className={`p12-verdict-h ${!a ? '' : a === q.answer ? 'is-ok' : 'is-bad'}`}>
              {!a ? `Boş bıraktın · doğru cevap ${q.answer}` : a === q.answer ? 'Doğru' : `Yanlış · doğru cevap ${q.answer}`}
            </div>
            <ExplanationBlock q={q} compact />
            <div className="p12-verdict-act">
              <button
                type="button"
                className={`p12-btn is-sm ${inReview ? 'is-acc' : ''}`}
                aria-pressed={inReview}
                onClick={() => {
                  setInReview(q.id, !inReview);
                  setAdded(false);
                  setTick((t) => t + 1);
                }}
              >
                {inReview ? <BookmarkCheck aria-hidden /> : <Bookmark aria-hidden />}
                {inReview ? 'Tekrar listesinde' : 'Tekrar listesine ekle'}
              </button>
              <button type="button" className="p12-btn is-sm is-acc" onClick={() => setChatQuestion(q)}>
                <Sparkles aria-hidden /> AI ile incele
              </button>
            </div>
          </section>
        </TestRunnerV12>
        <ResultChat q={chatQuestion} result={result} onClose={() => setChatQuestion(null)} />
      </>
    );
  }

  return (
    <>
      <ResultsV12
        title={result.title}
        durationSec={result.durationSec}
        total={result.total}
        correct={result.correct}
        wrong={result.wrong}
        blank={result.blank}
        disc={disc}
        listTitle={{ wrong: 'Yanlışların', blank: 'Boş bıraktıkların', correct: 'Doğruların', all: 'Tüm sorular' }[filter]}
        rows={rows}
        filter={{
          value: filter,
          onChange: (v) => setFilter(v as ResFilter),
          options: [
            { value: 'wrong', label: 'Yanlış', n: result.wrong },
            { value: 'blank', label: 'Boş', n: result.blank },
            { value: 'correct', label: 'Doğru', n: result.correct },
            { value: 'all', label: 'Tümü', n: result.total },
          ],
        }}
        onOpenRow={setReview}
        onReview={items.length ? () => setReview(reviewList[0]) : undefined}
        backLabel="Testlere dön"
        onBack={onRestart}
        emptyText={items.length === 0 ? 'Bu denemenin soruları artık bankada bulunmuyor.' : 'Bu grupta soru yok.'}
        actions={
          <>
            <button type="button" className="p12-btn is-pri" onClick={onRestart}>
              <RotateCcw aria-hidden /> Yeni deneme
            </button>
            {result.wrong > 0 && (
              <button
                type="button"
                className="p12-btn"
                onClick={() => {
                  onAddWrongToReview();
                  setAdded(true);
                }}
                disabled={added}
              >
                {added ? 'Tekrar listesine eklendi' : 'Yanlışları tekrar listesine ekle'}
              </button>
            )}
          </>
        }
      />
      <ResultChat q={chatQuestion} result={result} onClose={() => setChatQuestion(null)} />
    </>
  );
};

/** Sohbet çekmecesi body'de açılır: gözden geçirme katmanının (z 45) üstünde kalır */
const ResultChat: React.FC<{ q: StudyQuestion | null; result: SelfTestResult; onClose: () => void }> = ({ q, result, onClose }) =>
  createPortal(
    <QuestionAiChatDrawer
      isOpen={!!q}
      onClose={onClose}
      questionContext={
        q
          ? {
              id: q.id,
              discipline: q.discipline,
              topic: q.topic,
              committeeId: q.committeeId,
              committeeName: q.committeeId,
              year: q.year,
              number: q.number,
              stem: q.stem,
              options: q.options,
              correctAnswer: q.answer,
              explanation: q.explanation,
              userAnswer: result.answers[q.id],
            }
          : null
      }
    />,
    document.body
  );
