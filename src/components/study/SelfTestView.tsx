import React, { useEffect, useMemo, useRef, useState } from 'react';
import { confirmDialog } from '../ui/ConfirmDialog';
import { ArrowLeft, ArrowRight, Flag, Timer, Trash2, RotateCcw, ChevronDown, ChevronUp, Play, Bookmark, BookmarkCheck, Sparkles } from 'lucide-react';
import { Committee } from '../../types';
import {
  StudyQuestion,
  OptionKey,
  SelfTestResult,
  getProgress,
  getReview,
  recordAttempt,
  setInReview,
  shuffle,
  getTestHistory,
  saveTestResult,
  clearTestHistory,
} from '../../services/studyStore';
import { committeeShortLabel } from '../QuickAddHero';
import { Segmented, OptionButton, ExplanationBlock, EmptyState, cardCls, btnPrimary, btnSecondary, btnGhost, selectCls, Field, formatDuration, isTypingTarget } from './StudyUI';
import { StudyReportButton } from './StudyReportButton';
import { QuestionAiChatDrawer } from '../QuestionAiChatDrawer';

interface SelfTestViewProps {
  bank: StudyQuestion[];
  committees: Committee[];
  loading: boolean;
  initialCommitteeId?: string;
  onProgressChange?: () => void;
  /** Her artışında hızlı test başlar: tüm bankadan (arşiv + havuz) karışık 20 soru */
  quickStartNonce?: number;
}

type Phase = 'setup' | 'running' | 'result';
type TimeMode = 'none' | '60' | '90';

export const SelfTestView: React.FC<SelfTestViewProps> = ({ bank, committees, loading, initialCommitteeId, onProgressChange, quickStartNonce = 0 }) => {
  const [phase, setPhase] = useState<Phase>('setup');
  const [history, setHistory] = useState(getTestHistory);

  // setup
  const [committeeId, setCommitteeId] = useState(() => {
    if (initialCommitteeId && initialCommitteeId !== 'all') return initialCommitteeId;
    return 'all';
  });
  const [picked, setPicked] = useState<string[]>([]);
  const [count, setCount] = useState(20);
  const [timeMode, setTimeMode] = useState<TimeMode>('60');
  const [onlyUnsolved, setOnlyUnsolved] = useState(false);

  // running
  const [items, setItems] = useState<StudyQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<string, OptionKey | undefined>>({});
  const [flags, setFlags] = useState<Set<string>>(new Set());
  const [cur, setCur] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const [limit, setLimit] = useState<number | null>(null);
  const [result, setResult] = useState<SelfTestResult | null>(null);
  const [confirmFinish, setConfirmFinish] = useState(false);
  const finishedRef = useRef(false);

  const committeeName = (id: string) => {
    const c = (committees || []).find((x) => x.id === id);
    if (c) return committeeShortLabel(c).charAt(0) + committeeShortLabel(c).slice(1).toLocaleLowerCase('tr-TR');
    const m = id.match(/kurul(\d+)/i);
    return m ? `Kurul ${m[1]}` : /final/i.test(id) ? 'Final' : id;
  };
  const committeeIds = useMemo(() => {
    const fromCommittees = (committees || []).map((c) => c.id);
    const fromBank = new Set(bank.map((q) => q.committeeId).filter(Boolean));
    const ordered = fromCommittees.filter((id) => fromBank.has(id));
    const others = [...fromBank].filter((id) => !fromCommittees.includes(id)).sort();
    return [...ordered, ...others];
  }, [bank, committees]);
  const scoped = useMemo(() => bank.filter((q) => committeeId === 'all' || q.committeeId === committeeId), [bank, committeeId]);
  const disciplineCounts = useMemo(() => {
    const m: Record<string, number> = {};
    scoped.forEach((q) => (m[q.discipline] = (m[q.discipline] || 0) + 1));
    return Object.entries(m).sort((a, b) => b[1] - a[1]);
  }, [scoped]);
  const pool = useMemo(() => {
    const progress = onlyUnsolved ? getProgress() : {};
    return scoped.filter((q) => (picked.length === 0 || picked.includes(q.discipline)) && (!onlyUnsolved || !progress[q.id]));
  }, [scoped, picked, onlyUnsolved]);

  const toggleDiscipline = (d: string) => setPicked((p) => (p.includes(d) ? p.filter((x) => x !== d) : [...p, d]));

  const start = () => runTest(shuffle(pool).slice(0, count));

  // Hızlı test: seçili kurulda en az 10 soru varsa oradan, yoksa tüm bankadan; daha önce
  // çözülmemiş sorular önce gelir ki her seferinde aynı sorular çıkmasın
  useEffect(() => {
    if (!quickStartNonce || bank.length === 0) return;
    const inCommittee = bank.filter((q) => q.committeeId === initialCommitteeId);
    const source = inCommittee.length >= 10 ? inCommittee : bank;
    const progress = getProgress();
    const fresh = shuffle(source.filter((q) => !progress[q.id]));
    const seen = shuffle(source.filter((q) => progress[q.id]));
    runTest([...fresh, ...seen].slice(0, 20));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [quickStartNonce, bank.length]);

  function runTest(chosen: StudyQuestion[]) {
    if (chosen.length === 0) return;
    setItems(chosen);
    setAnswers({});
    setFlags(new Set());
    setCur(0);
    setElapsed(0);
    setLimit(timeMode === 'none' ? null : Math.round(chosen.length * Number(timeMode)));
    setResult(null);
    setConfirmFinish(false);
    finishedRef.current = false;
    setPhase('running');
    window.scrollTo({ top: 0 });
  }

  useEffect(() => {
    if (phase !== 'running') return;
    const t = setInterval(() => setElapsed((s) => s + 1), 1000);
    return () => clearInterval(t);
  }, [phase]);

  const finish = () => {
    if (finishedRef.current) return;
    finishedRef.current = true;
    let correct = 0;
    let wrong = 0;
    let blank = 0;
    const byDiscipline: SelfTestResult['byDiscipline'] = {};
    items.forEach((q) => {
      const a = answers[q.id];
      const d = (byDiscipline[q.discipline] ||= { total: 0, correct: 0 });
      d.total++;
      if (!a) blank++;
      else if (a === q.answer) {
        correct++;
        d.correct++;
        recordAttempt(q.id, a, true);
      } else {
        wrong++;
        recordAttempt(q.id, a, false);
      }
    });
    const title =
      (committeeId === 'all' ? 'Karışık' : committeeName(committeeId)) + (picked.length ? ` · ${picked.length === 1 ? picked[0] : `${picked.length} ders`}` : '');
    const r: SelfTestResult = {
      id: `t-${Date.now().toString(36)}`,
      at: new Date().toISOString(),
      title,
      durationSec: elapsed,
      total: items.length,
      correct,
      wrong,
      blank,
      byDiscipline,
      questionIds: items.map((q) => q.id),
      answers,
    };
    setHistory(saveTestResult(r));
    setResult(r);
    setPhase('result');
    onProgressChange?.();
    window.scrollTo({ top: 0 });
  };

  // Auto-finish when time runs out
  useEffect(() => {
    if (phase === 'running' && limit !== null && elapsed >= limit) finish();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [elapsed, limit, phase]);

  // Keyboard during the test
  useEffect(() => {
    if (phase !== 'running') return;
    const onKey = (e: KeyboardEvent) => {
      if (isTypingTarget(e.target) || e.metaKey || e.ctrlKey || e.altKey) return;
      const q = items[cur];
      const k = e.key.toUpperCase();
      if (q && ['A', 'B', 'C', 'D', 'E'].includes(k) && q.options.some((o) => o.key === k)) {
        e.preventDefault();
        setAnswers((p) => ({ ...p, [q.id]: p[q.id] === k ? undefined : (k as OptionKey) }));
      } else if (q && k === 'F') {
        e.preventDefault();
        setFlags((f) => {
          const n = new Set(f);
          n.has(q.id) ? n.delete(q.id) : n.add(q.id);
          return n;
        });
      } else if (e.key === 'ArrowRight') setCur((i) => Math.min(items.length - 1, i + 1));
      else if (e.key === 'ArrowLeft') setCur((i) => Math.max(0, i - 1));
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [phase, items, cur]);

  // ---------------- SETUP ----------------
  if (phase === 'setup') {
    const effective = Math.min(count, pool.length);
    return (
      <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)] gap-3 sm:gap-5 items-start">
        <section className={`${cardCls} p-4 sm:p-6 flex flex-col gap-4`}>
          <div>
            <h2 className="m-0 font-display text-2xl font-bold tracking-[-0.02em]">Deneme oluştur</h2>
            <p className="m-0 mt-1 text-base text-ink-2">Çıkmış ve kurulan sorulardan rastgele bir deneme. Bitirince ders ders sonucunu görürsün.</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <Field label="Kurul">
              <select value={committeeId} onChange={(e) => { setCommitteeId(e.target.value); setPicked([]); }} className={selectCls}>
                <option value="all">Tüm kurullar ({bank.length})</option>
                {committeeIds.map((id) => (
                  <option key={id} value={id}>
                    {committeeName(id)} ({bank.filter((q) => q.committeeId === id).length})
                  </option>
                ))}
              </select>
            </Field>
            <div className="flex flex-col gap-1.5">
              <span className="text-sm font-semibold text-ink-2">Süre</span>
              <Segmented<TimeMode>
                label="Süre"
                value={timeMode}
                onChange={setTimeMode}
                options={[
                  { value: 'none', label: 'Süresiz' },
                  { value: '60', label: '1 dk/soru' },
                  { value: '90', label: '1,5 dk/soru' },
                ]}
              />
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <span className="text-sm font-semibold text-ink-2">Soru sayısı</span>
            <Segmented<number>
              label="Soru sayısı"
              value={count}
              onChange={setCount}
              options={[10, 20, 40, 60, 100].map((n) => ({ value: n, label: String(n) }))}
            />
          </div>

          <fieldset className="border-0 p-0 m-0 flex flex-col gap-2">
            <legend className="text-sm font-semibold text-ink-2 mb-2 flex items-center gap-2">
              Dersler <span className="font-normal text-ink-3">{picked.length ? `${picked.length} seçili` : 'hepsi'}</span>
              {picked.length > 0 && (
                <button type="button" onClick={() => setPicked([])} className="text-accent text-sm font-semibold cursor-pointer">
                  Temizle
                </button>
              )}
            </legend>
            <div className="flex flex-wrap gap-1.5 max-h-[156px] overflow-y-auto">
              {disciplineCounts.map(([d, n]) => {
                const on = picked.includes(d);
                return (
                  <button
                    key={d}
                    type="button"
                    aria-pressed={on}
                    onClick={() => toggleDiscipline(d)}
                    className={`h-8 px-3 rounded-full text-sm cursor-pointer ${
                      on ? 'bg-accent-soft text-accent font-semibold ring-1 ring-inset ring-accent/40' : 'bg-white border border-line text-ink hover:border-line-2'
                    }`}
                  >
                    {d} <span className={`font-mono text-2xs ${on ? 'text-accent/70' : 'text-ink-3'}`}>{n}</span>
                  </button>
                );
              })}
            </div>
          </fieldset>

          <label className="flex items-center gap-2 min-h-9 text-base text-ink cursor-pointer">
            <input type="checkbox" checked={onlyUnsolved} onChange={(e) => setOnlyUnsolved(e.target.checked)} className="w-4 h-4 accent-[#1E4FD8]" />
            Yalnızca daha önce çözmediğim sorular
          </label>

          <div className="flex flex-wrap items-center justify-between gap-3 border-t border-line-soft pt-4">
            <span className="text-base text-ink-2">
              <strong className="text-ink">{effective}</strong> soru
              {timeMode !== 'none' && effective > 0 && <> · {formatDuration(Math.round(effective * Number(timeMode)))} süre</>}
              {pool.length < count && pool.length > 0 && (
                <span className="text-warn">
                  {' '}· bu filtrede {pool.length} soru var{' '}
                  <button type="button" onClick={() => setCount(pool.length)} className="text-accent underline font-semibold cursor-pointer">
                    (tamamını seç)
                  </button>
                </span>
              )}
            </span>
            <button type="button" onClick={start} disabled={loading || effective === 0} className={btnPrimary}>
              <Play className="w-4 h-4" /> {loading && bank.length === 0 ? 'Sorular yükleniyor…' : 'Denemeyi başlat'}
            </button>
          </div>
        </section>

        <section className={`${cardCls} p-4 sm:p-5 flex flex-col gap-3`}>
          <div className="flex items-center justify-between">
            <h2 className="m-0 text-md font-semibold">Geçmiş denemeler</h2>
            {history.length > 0 && (
              <button
                type="button"
                onClick={async () => {
                  if (await confirmDialog({ title: 'Tüm deneme geçmişi silinsin mi?', confirmLabel: 'Sil', tone: 'danger' })) {
                    clearTestHistory();
                    setHistory([]);
                  }
                }}
                className="h-8 px-2 rounded-lg text-sm text-ink-2 hover:text-bad-text inline-flex items-center gap-1 cursor-pointer"
              >
                <Trash2 className="w-3.5 h-3.5" /> Temizle
              </button>
            )}
          </div>
          {history.length === 0 ? (
            <p className="m-0 text-base text-ink-2">İlk denemeni çözdüğünde sonuçların burada listelenir.</p>
          ) : (
            <ol className="list-none m-0 p-0 flex flex-col">
              {history.slice(0, 10).map((h) => {
                const pct = Math.round((h.correct / Math.max(1, h.total)) * 100);
                return (
                  <li key={h.id}>
                    <button
                      type="button"
                      onClick={() => {
                        setResult(h);
                        setItems(h.questionIds.map((id) => (bank || []).find((q) => q.id === id)).filter(Boolean) as StudyQuestion[]);
                        setPhase('result');
                      }}
                      className="w-full grid grid-cols-[minmax(0,1fr)_auto] gap-x-3 gap-y-1 items-center py-2.5 border-b border-line-soft text-left cursor-pointer hover:bg-accent-soft rounded"
                    >
                      <span className="text-base font-semibold truncate">{h.title}</span>
                      <span className={`font-mono text-base ${pct >= 70 ? 'text-ok' : pct >= 50 ? 'text-warn' : 'text-bad-text'}`}>%{pct}</span>
                      <span className="text-xs text-ink-3">
                        {new Date(h.at).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })} · {h.correct}/{h.total} ·{' '}
                        {formatDuration(h.durationSec)}
                      </span>
                      <span className="h-1 w-16 rounded-full bg-line-soft">
                        <span className="block h-1 rounded-full bg-accent" style={{ width: `${pct}%` }} />
                      </span>
                    </button>
                  </li>
                );
              })}
            </ol>
          )}
        </section>
      </div>
    );
  }

  // ---------------- RUNNING ----------------
  if (phase === 'running') {
    const q = items[cur];
    const answeredCount = Object.values(answers).filter(Boolean).length;
    const remaining = limit !== null ? Math.max(0, limit - elapsed) : null;
    const low = remaining !== null && remaining <= 60;
    return (
      <div className="tsx">
        {/* Üst çubuk: süre · çentikli ilerleme · bitir (canvas "Test") */}
        <div className="tsx-bar">
          <span className={`tsx-time ${low ? 'is-low' : ''}`} aria-label="Süre"><Timer aria-hidden />{remaining !== null ? formatDuration(remaining) : formatDuration(elapsed)}</span>
          <span className="tsx-count"><b>{answeredCount}</b>/{items.length}</span>
          <div className="tsx-notches" aria-hidden>
            {items.slice(0, 60).map((it, i) => (
              <span key={it.id} className={`${answers[it.id] ? 'is-done' : ''} ${flags.has(it.id) ? 'is-flag' : ''} ${i === cur ? 'is-cur' : ''}`} />
            ))}
          </div>
          {confirmFinish ? (
            <span className="tsx-confirm">
              <span>{items.length - answeredCount} boş. Emin misin?</span>
              <button type="button" onClick={() => setConfirmFinish(false)} className={btnGhost}>Devam</button>
              <button type="button" onClick={finish} className={btnPrimary}>Bitir</button>
            </span>
          ) : (
            <button type="button" onClick={() => (answeredCount < items.length ? setConfirmFinish(true) : finish())} className={btnPrimary}>Bitir</button>
          )}
        </div>

        <div className="tsx-body">
          <article className="qk is-solve">
            <header className="qk-h">
              <span className="qk-chip">{cur + 1}</span>
              <span className="qk-kunye">{[q.year, q.number ? `S${q.number}` : null].filter(Boolean).join(' · ') || 'Soru'}</span>
              {q.discipline && <span className="qk-ders">{q.discipline}</span>}
              {flags.has(q.id) && <span className="qk-flags"><span className="cx-flag is-warn">İşaretli</span></span>}
              <span className="qk-sp" />
              <button
                type="button"
                aria-pressed={flags.has(q.id)}
                onClick={() => setFlags((f) => { const n = new Set(f); n.has(q.id) ? n.delete(q.id) : n.add(q.id); return n; })}
                className={`qk-ib ${flags.has(q.id) ? 'is-fav' : ''}`}
                aria-label={flags.has(q.id) ? 'İşareti kaldır' : 'Sonra bakmak için işaretle'}
                title="Sonra bak"
              >
                <Flag aria-hidden />
              </button>
              <StudyReportButton q={q} compact className="qk-ib" />
            </header>
            <div className="qk-stem is-lead">{q.stem}</div>
            <ol role="radiogroup" aria-label="Şıklar" className="qk-opts">
              {q.options.map((o) => {
                const sel = answers[q.id] === o.key;
                return (
                  <li key={o.key} className="qk-opt-li">
                    <button type="button" role="radio" aria-checked={sel} onClick={() => setAnswers((p) => ({ ...p, [q.id]: p[q.id] === o.key ? undefined : o.key }))} className={`qk-opt ${sel ? 'is-sel' : ''}`}>
                      <span className="qk-bub" aria-hidden>{o.key}</span>
                      <span className="qk-opt-t">{o.text}</span>
                    </button>
                  </li>
                );
              })}
            </ol>
            <p className="qk-hint">A–E seç · tekrar basınca boşalır · ← → gezin</p>
            <footer className="qk-nav">
              <button type="button" onClick={() => setCur((i) => Math.max(0, i - 1))} disabled={cur === 0} className={btnSecondary}>
                <ArrowLeft className="w-4 h-4" /> Önceki
              </button>
              <div className="qk-progress" aria-hidden><span style={{ width: `${((cur + 1) / items.length) * 100}%` }} /></div>
              <button type="button" onClick={() => setCur((i) => Math.min(items.length - 1, i + 1))} disabled={cur >= items.length - 1} className={btnPrimary}>
                Sonraki <ArrowRight className="w-4 h-4" />
              </button>
            </footer>
          </article>

          <nav aria-label="Optik form" className="tsx-sheet">
            <div className="tsx-sheet-h">
              <b>Optik form</b>
              <span className="tsx-lg"><i className="is-done" />Dolu <i className="is-flag" />İşaretli</span>
            </div>
            <div className="tsx-grid">
              {items.map((it, i) => {
                const a = answers[it.id];
                const isCur = i === cur;
                const flagged = flags.has(it.id);
                return (
                  <button
                    key={it.id}
                    type="button"
                    onClick={() => setCur(i)}
                    aria-current={isCur ? 'step' : undefined}
                    aria-label={`Soru ${i + 1}${a ? `, ${a} işaretli` : ', boş'}${flagged ? ', sonra bakılacak' : ''}`}
                    className={`${a ? 'is-done' : ''} ${isCur ? 'is-cur' : ''} ${flagged ? 'is-flag' : ''}`}
                  >
                    {a ? `${i + 1}${a}` : i + 1}
                  </button>
                );
              })}
            </div>
            <button type="button" onClick={async () => (await confirmDialog({ title: 'Deneme iptal edilsin mi?', message: 'Cevapların kaydedilmez.', confirmLabel: 'İptal et', cancelLabel: 'Devam et', tone: 'danger' })) && setPhase('setup')} className={`${btnGhost} self-start`}>
              Denemeyi iptal et
            </button>
          </nav>
        </div>
      </div>
    );
  }

  // ---------------- RESULT ----------------
  if (!result) return <EmptyState title="Sonuç bulunamadı" action={<button type="button" className={btnSecondary} onClick={() => setPhase('setup')}>Yeni deneme</button>} />;
  return (
    <ResultView
      result={result}
      items={items}
      onRestart={() => setPhase('setup')}
      onAddWrongToReview={() => {
        items.forEach((q) => {
          const a = result.answers[q.id];
          if (a && a !== q.answer) setInReview(q.id, true);
        });
        onProgressChange?.();
      }}
    />
  );
};

const ResultView: React.FC<{
  result: SelfTestResult;
  items: StudyQuestion[];
  onRestart: () => void;
  onAddWrongToReview: () => void;
}> = ({ result, items, onRestart, onAddWrongToReview }) => {
  const [filter, setFilter] = useState<'wrong' | 'blank' | 'correct' | 'all'>(() => {
    if (result.wrong > 0) return 'wrong';
    if (result.blank > 0) return 'blank';
    return 'all';
  });
  const [open, setOpen] = useState<string | null>(null);
  const [added, setAdded] = useState(false);
  const [chatQuestion, setChatQuestion] = useState<StudyQuestion | null>(null);
  const pct = Math.round((result.correct / Math.max(1, result.total)) * 100);
  const net = result.correct - result.wrong / 4;
  const rows = items.filter((q) => {
    const a = result.answers[q.id];
    if (filter === 'all') return true;
    if (filter === 'blank') return !a;
    if (filter === 'correct') return a === q.answer;
    return a && a !== q.answer;
  });
  const disc = Object.entries(result.byDiscipline).sort((a, b) => b[1].total - a[1].total);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.5fr)] gap-3 sm:gap-5 items-start">
      <section className="flex flex-col gap-3 sm:gap-4">
        <div className="bg-white border border-line rounded-2xl p-4 sm:p-5 flex flex-col gap-3">
          <div className="flex justify-between items-baseline gap-2">
            <h2 className="m-0 text-md font-semibold truncate text-ink">{result.title}</h2>
            <span className="font-mono text-xs text-ink-3 shrink-0">{formatDuration(result.durationSec)}</span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="font-display text-4xl sm:text-4xl font-bold leading-none tracking-[-0.03em] text-ink">%{pct}</span>
            <span className="text-base text-ink-2">net {net.toLocaleString('tr-TR', { maximumFractionDigits: 2 })}</span>
          </div>
          <div className="flex h-2 rounded-full overflow-hidden gap-[2px] bg-line-soft">
            <span className="bg-ok-bright" style={{ width: `${(result.correct / result.total) * 100}%` }} />
            <span className="bg-bad" style={{ width: `${(result.wrong / result.total) * 100}%` }} />
          </div>
          <div className="grid grid-cols-3 gap-2 text-sm">
            {[
              ['Doğru', result.correct, '#1F9D55'],
              ['Yanlış', result.wrong, '#C2410C'],
              ['Boş', result.blank, '#C9D2DB'],
            ].map(([l, n, c]) => (
              <div key={l as string} className="flex flex-col">
                <span className="flex items-center gap-1.5 text-ink-2">
                  <span className="w-2 h-2 rounded-sm" style={{ background: c as string }} />
                  {l}
                </span>
                <span className="font-mono text-lg text-ink">{n}</span>
              </div>
            ))}
          </div>
        </div>

        <div className={`${cardCls} p-4 sm:p-5 flex flex-col gap-3`}>
          <h3 className="m-0 text-md font-semibold">Derslere göre</h3>
          {disc.map(([d, s]) => {
            const p = Math.round((s.correct / Math.max(1, s.total)) * 100);
            return (
              <div key={d} className="flex flex-col gap-1">
                <div className="flex justify-between text-base gap-2">
                  <span className="truncate">{d}</span>
                  <span className="font-mono text-ink-2 shrink-0">
                    {s.correct}/{s.total}
                  </span>
                </div>
                <div className="h-1.5 rounded-full bg-line-soft">
                  <div className={`h-1.5 rounded-full ${p >= 70 ? 'bg-ok-bright' : p >= 50 ? 'bg-warn' : 'bg-bad'}`} style={{ width: `${Math.max(2, p)}%` }} />
                </div>
              </div>
            );
          })}
        </div>

        <div className="flex flex-wrap gap-2">
          <button type="button" onClick={onRestart} className={btnPrimary}>
            <RotateCcw className="w-4 h-4" /> Yeni deneme
          </button>
          {result.wrong > 0 && (
            <button
              type="button"
              onClick={() => {
                onAddWrongToReview();
                setAdded(true);
              }}
              disabled={added}
              className={btnSecondary}
            >
              {added ? 'Tekrar listesine eklendi' : 'Yanlışları tekrar listesine ekle'}
            </button>
          )}
        </div>
      </section>

      <section className={`${cardCls} overflow-hidden`}>
        <div className="flex flex-wrap items-center justify-between gap-2 px-4 py-3 border-b border-line">
          <h3 className="m-0 text-md font-semibold">Cevap anahtarı</h3>
          <Segmented
            label="Göster"
            size="sm"
            value={filter}
            onChange={setFilter}
            options={[
              { value: 'wrong', label: `Yanlış ${result.wrong}` },
              { value: 'blank', label: `Boş ${result.blank}` },
              { value: 'correct', label: `Doğru ${result.correct}` },
              { value: 'all', label: `Tümü ${result.total}` },
            ]}
          />
        </div>
        {items.length === 0 ? (
          <p className="m-0 px-4 py-6 text-base text-ink-2">Bu denemenin soruları artık bankada bulunmuyor.</p>
        ) : rows.length === 0 ? (
          <p className="m-0 px-4 py-6 text-base text-ink-2">Bu grupta soru yok.</p>
        ) : (
          <ol className="list-none m-0 p-0">
            {rows.map((q) => {
              const i = items.indexOf(q);
              const a = result.answers[q.id];
              const isOpen = open === q.id;
              const ok = a === q.answer;
              return (
                <li key={q.id} className="border-b border-line-soft">
                  <button
                    type="button"
                    onClick={() => setOpen(isOpen ? null : q.id)}
                    aria-expanded={isOpen}
                    className="w-full grid grid-cols-[36px_minmax(0,1fr)_auto] gap-3 items-center px-4 py-3 text-left cursor-pointer hover:bg-accent-soft"
                  >
                    <span className="font-mono text-sm text-ink-2">{i + 1}</span>
                    <span className="flex flex-col gap-0.5 min-w-0">
                      <span className="text-xs font-semibold text-ink-2">{q.discipline}</span>
                      <span className="text-base truncate">{q.stem}</span>
                    </span>
                    <span className="flex items-center gap-2">
                      <span className={`font-mono text-sm ${!a ? 'text-ink-3' : ok ? 'text-ok' : 'text-bad-text'}`}>{a || '—'}</span>
                      <span className="font-mono text-sm text-ok">→{q.answer}</span>
                      {isOpen ? <ChevronUp className="w-4 h-4 text-ink-2" /> : <ChevronDown className="w-4 h-4 text-ink-2" />}
                    </span>
                  </button>
                  {isOpen && (
                    <div className="px-4 pb-4 flex flex-col gap-2.5">
                      <p className="m-0 text-md leading-[1.5]">{q.stem}</p>
                      <div className="flex flex-col gap-1.5">
                        {q.options.map((o) => (
                          <OptionButton
                            key={o.key}
                            opt={o}
                            disabled
                            state={o.key === q.answer ? 'correct' : o.key === a ? 'wrong' : 'muted'}
                            tag={o.key === a ? 'Senin cevabın' : o.key === q.answer ? 'Doğru cevap' : undefined}
                          />
                        ))}
                      </div>
                      <div className="bg-canvas rounded-lg p-3">
                        <ExplanationBlock q={q} compact />
                      </div>
                      <div className="flex items-center justify-between pt-1">
                        <button
                          type="button"
                          onClick={() => {
                            const isRev = getReview().has(q.id);
                            setInReview(q.id, !isRev);
                            setAdded(false);
                          }}
                          className={`h-8 px-2.5 rounded-lg text-sm font-semibold inline-flex items-center gap-1.5 cursor-pointer ${
                            getReview().has(q.id) ? 'bg-accent-soft text-accent' : 'text-ink-2 hover:bg-canvas'
                          }`}
                        >
                          {getReview().has(q.id) ? <BookmarkCheck className="w-3.5 h-3.5" /> : <Bookmark className="w-3.5 h-3.5" />}
                          {getReview().has(q.id) ? 'Tekrar listesinde' : 'Tekrar listesine ekle'}
                        </button>
                        <StudyReportButton q={q} className="h-8! ml-auto mr-1" />
                        <button
                          type="button"
                          onClick={() => setChatQuestion(q)}
                          className="h-8 px-2.5 rounded-lg text-sm font-semibold inline-flex items-center gap-1.5 text-accent hover:bg-accent-soft cursor-pointer transition-colors"
                        >
                          <Sparkles className="w-3.5 h-3.5" />
                          <span>AI ile İncele</span>
                        </button>
                      </div>
                    </div>
                  )}
                </li>
              );
            })}
          </ol>
        )}
      </section>

      {/* AI Live Tutor Chat Drawer */}
      <QuestionAiChatDrawer
        isOpen={!!chatQuestion}
        onClose={() => setChatQuestion(null)}
        questionContext={chatQuestion ? {
          id: chatQuestion.id,
          discipline: chatQuestion.discipline,
          topic: chatQuestion.topic,
          committeeId: chatQuestion.committeeId,
          committeeName: chatQuestion.committeeId,
          year: chatQuestion.year,
          number: chatQuestion.number,
          stem: chatQuestion.stem,
          options: chatQuestion.options,
          correctAnswer: chatQuestion.answer,
          explanation: chatQuestion.explanation,
          userAnswer: result?.answers[chatQuestion.id],
        } : null}
      />
    </div>
  );
};
