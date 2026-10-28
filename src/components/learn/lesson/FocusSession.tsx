/**
 * Odak seansı (Öğren dersinde, Araçlar › Çalışma › Odak seansı, kısayol O).
 *
 *  Kurulum   süre (25/45/60 dk) + hedef (bu bölümü bitir · N adım · süre dolana kadar)
 *  Seans     üstte ince süre/hedef çubuğu; ray, bilgi çekmecesi ve ortak notlar gizlenir (kök sınıfı `is-focus`)
 *  Duraklama sekmeden çıkınca kendiliğinden durur; dönüşte "kaldığın yer" ile devam
 *  Nabız     son 6 sonuçta ≥4 yanlış VE ortalama yanıt süresi kişisel ortancanın yarısından kısaysa (aceleci
 *            yanlışlar) bir kez mola önerir; uzun seanslarda her 25 dakikada bir de önerir. Zorlamaz.
 *  Mola      3 dakikalık nefes ve göz dinlendirme ekranı (süreden sayılmaz)
 *  Fiş       süre, biten adım, etkileşim, doğruluk, en çok yanılınan 3 adım + "Hatalarını tekrar et"
 *
 * Sonuçlar LessonPlayer'dan `medsoru:learn-ix` olayıyla gelir. Seans kaydı learnReview.saveSession'a yazılır.
 * Stil: styles/learn-focus.css (.lf-*).
 */
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Check, Coffee, Pause, Play, RotateCcw, Target, Timer, X } from 'lucide-react';
import { Sheet } from '../../ui/Sheet';
import type { LessonSection, LessonStep } from './lessonModel';
import { medianMs, openEntries, saveSession } from '../../../services/learnReview';
import '../../../styles/ogren-ders.css';
import '../../../styles/learn-focus.css';

export const IX_EVENT = 'medsoru:learn-ix';
export interface IxEventDetail { deckId: string; slide: number; title: string; ok: boolean; ms?: number }

type GoalKind = 'section' | 'steps' | 'time';
interface Goal { kind: GoalKind; n?: number; stepNums?: number[]; label: string }
interface Run {
  id: string;
  startAt: number;
  plannedMs: number;
  activeMs: number;
  goal: Goal;
  doneAtStart: number[];
  results: IxEventDetail[];
  nextNudgeAt: number;
  lastPulseAt: number;
}
type Phase = 'idle' | 'running' | 'paused' | 'break' | 'receipt';

const MIN = 60_000;
const BREAK_MS = 3 * MIN;
const mmss = (ms: number) => {
  const s = Math.max(0, Math.round(ms / 1000));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
};

export interface FocusApi {
  active: boolean;
  openSetup: () => void;
}

export const FocusSession: React.FC<{
  deckId: string;
  deckTitle: string;
  steps: LessonStep[];
  sections: LessonSection[];
  index: number;
  done: Set<number>;
  setupOpen: boolean;
  onSetupClose: () => void;
  onActiveChange: (active: boolean) => void;
  onJump: (slideNumber: number) => void;
  onReview?: () => void;
}> = ({ deckId, deckTitle, steps, sections, index, done, setupOpen, onSetupClose, onActiveChange, onJump, onReview }) => {
  const [phase, setPhase] = useState<Phase>('idle');
  const [run, setRun] = useState<Run | null>(null);
  const [autoPaused, setAutoPaused] = useState(false);
  const [nudge, setNudge] = useState<null | 'pulse' | 'time'>(null);
  const [breakLeft, setBreakLeft] = useState(BREAK_MS);
  const [goalHit, setGoalHit] = useState(false);
  const runRef = useRef(run);
  runRef.current = run;
  const phaseRef = useRef(phase);
  phaseRef.current = phase;
  const savedRef = useRef<string | null>(null);

  // Kurulum seçimleri
  const [mins, setMins] = useState(25);
  const [goalKind, setGoalKind] = useState<GoalKind>('section');
  const [goalN, setGoalN] = useState(10);
  const step = steps[index];
  const section = step ? sections[step.section] : undefined;
  const sectionLeft = section ? section.steps.filter((i) => !done.has(steps[i].number)) : [];

  useEffect(() => onActiveChange(phase !== 'idle' && phase !== 'receipt'), [phase]); // eslint-disable-line react-hooks/exhaustive-deps

  const start = () => {
    const goal: Goal =
      goalKind === 'section' && section
        ? { kind: 'section', stepNums: section.steps.map((i) => steps[i].number), label: `Bölüm ${step.section + 1}: ${section.name}` }
        : goalKind === 'steps'
          ? { kind: 'steps', n: goalN, label: `${goalN} adım` }
          : { kind: 'time', label: 'Süre dolana kadar' };
    const now = Date.now();
    savedRef.current = null;
    setRun({ id: `fs-${now}`, startAt: now, plannedMs: mins * MIN, activeMs: 0, goal, doneAtStart: [...done], results: [], nextNudgeAt: 25 * MIN, lastPulseAt: 0 });
    setGoalHit(false);
    setNudge(null);
    setPhase('running');
    onSetupClose();
  };

  /* --- saat: yalnız çalışırken ve sekme görünürken ilerler --- */
  useEffect(() => {
    if (phase !== 'running') return;
    let last = Date.now();
    const t = window.setInterval(() => {
      const now = Date.now();
      const dt = Math.min(now - last, 5000); // uyku/askıdan dönüşte sıçrama yok
      last = now;
      if (document.visibilityState !== 'visible') return;
      setRun((r) => (r ? { ...r, activeMs: r.activeMs + dt } : r));
    }, 1000);
    return () => window.clearInterval(t);
  }, [phase]);

  /* --- sekmeden çıkınca kendiliğinden duraklat --- */
  useEffect(() => {
    const on = () => {
      if (document.visibilityState === 'hidden' && phaseRef.current === 'running') {
        setPhase('paused');
        setAutoPaused(true);
      }
    };
    document.addEventListener('visibilitychange', on);
    return () => document.removeEventListener('visibilitychange', on);
  }, []);

  /* --- etkileşim sonuçları + dikkat nabzı --- */
  useEffect(() => {
    const on = (e: Event) => {
      const d = (e as CustomEvent<IxEventDetail>).detail;
      if (!d || d.deckId !== deckId || phaseRef.current !== 'running') return;
      setRun((r) => {
        if (!r) return r;
        const results = [...r.results, d];
        const last6 = results.slice(-6);
        const wrong = last6.filter((x) => !x.ok).length;
        const ms = last6.map((x) => x.ms).filter((x): x is number => typeof x === 'number');
        const avg = ms.length ? ms.reduce((a, b) => a + b, 0) / ms.length : Infinity;
        const med = medianMs() ?? 10_000;
        const hasty = last6.length === 6 && wrong >= 4 && avg < med * 0.5;
        if (hasty && Date.now() - r.lastPulseAt > 10 * MIN) {
          setNudge('pulse');
          return { ...r, results, lastPulseAt: Date.now() };
        }
        return { ...r, results };
      });
    };
    window.addEventListener(IX_EVENT, on);
    return () => window.removeEventListener(IX_EVENT, on);
  }, [deckId]);

  /* --- hedef, süre sonu ve 25 dakikalık mola önerisi --- */
  const progress = useMemo(() => {
    if (!run) return { cur: 0, total: 1, label: '' };
    const g = run.goal;
    if (g.kind === 'section') {
      const total = g.stepNums?.length || 1;
      const cur = (g.stepNums || []).filter((x) => done.has(x)).length;
      return { cur, total, label: `${cur}/${total} adım` };
    }
    if (g.kind === 'steps') {
      const base = new Set(run.doneAtStart);
      const cur = [...done].filter((x) => !base.has(x)).length;
      return { cur: Math.min(cur, g.n || 1), total: g.n || 1, label: `${Math.min(cur, g.n || 1)}/${g.n} adım` };
    }
    return { cur: run.activeMs, total: run.plannedMs, label: '' };
  }, [run, done]);

  const finish = useCallback(() => {
    setPhase('receipt');
    setNudge(null);
  }, []);

  useEffect(() => {
    if (!run || phase !== 'running') return;
    if (run.activeMs >= run.plannedMs) return finish();
    if (run.goal.kind !== 'time' && progress.cur >= progress.total && !goalHit) {
      setGoalHit(true);
      return finish();
    }
    if (run.plannedMs >= 45 * MIN && run.activeMs >= run.nextNudgeAt && run.plannedMs - run.activeMs > 5 * MIN) {
      setRun({ ...run, nextNudgeAt: run.nextNudgeAt + 25 * MIN });
      setNudge((n) => n || 'time');
    }
  }, [run, phase, progress, goalHit, finish]);

  /* --- mola sayacı --- */
  useEffect(() => {
    if (phase !== 'break') return;
    const end = Date.now() + breakLeft;
    const t = window.setInterval(() => setBreakLeft(Math.max(0, end - Date.now())), 250);
    return () => window.clearInterval(t);
  }, [phase]); // eslint-disable-line react-hooks/exhaustive-deps

  /* --- fiş: bir kez kaydedilir --- */
  const stats = useMemo(() => {
    if (!run) return null;
    const ix = run.results.length;
    const correct = run.results.filter((r) => r.ok).length;
    const base = new Set(run.doneAtStart);
    const stepsDone = [...done].filter((x) => !base.has(x)).length;
    const by = new Map<number, { slide: number; title: string; wrong: number }>();
    run.results.filter((r) => !r.ok).forEach((r) => {
      const o = by.get(r.slide) || { slide: r.slide, title: r.title, wrong: 0 };
      o.wrong++;
      by.set(r.slide, o);
    });
    const weak = [...by.values()].sort((a, b) => b.wrong - a.wrong).slice(0, 3);
    return { ix, correct, stepsDone, weak, pct: ix ? Math.round((correct / ix) * 100) : null };
  }, [run, done]);

  useEffect(() => {
    if (phase !== 'receipt' || !run || !stats || savedRef.current === run.id) return;
    savedRef.current = run.id;
    saveSession({
      id: run.id, deckId, deckTitle, start: run.startAt, activeMs: run.activeMs, plannedMin: Math.round(run.plannedMs / MIN),
      goal: run.goal.label, stepsDone: stats.stepsDone, ix: stats.ix, correct: stats.correct, weak: stats.weak,
    });
  }, [phase, run, stats, deckId, deckTitle]);

  const extend = () => {
    if (!run) return;
    savedRef.current = null;
    setRun({ ...run, plannedMs: Math.max(run.plannedMs, run.activeMs) + 10 * MIN, goal: goalHit ? { kind: 'time', label: 'Süre dolana kadar' } : run.goal });
    setPhase('running');
  };
  const close = () => {
    setPhase('idle');
    setRun(null);
    setNudge(null);
  };
  const takeBreak = () => {
    setNudge(null);
    setBreakLeft(BREAK_MS);
    setPhase('break');
  };
  const resume = () => {
    setAutoPaused(false);
    setPhase('running');
  };

  const openErr = useMemo(() => (phase === 'receipt' ? openEntries(deckId).length : 0), [phase, deckId]);
  const left = run ? run.plannedMs - run.activeMs : 0;
  const timePct = run ? Math.min(100, (run.activeMs / run.plannedMs) * 100) : 0;
  const goalPct = run && run.goal.kind !== 'time' ? Math.min(100, (progress.cur / progress.total) * 100) : timePct;
  const cur = steps[index];

  return (
    <>
      <Sheet open={setupOpen} onClose={onSetupClose} title="Odak seansı" subtitle="Süreyi ve hedefi seç; arayüz sadeleşir, sekmeden çıkınca seans durur." width={440}>
        <div className="lf-setup">
          <div className="lf-field">
            <span className="ls-eyebrow">Süre</span>
            <div className="ls-seg" role="radiogroup" aria-label="Süre">
              {[25, 45, 60].map((m) => (
                <button key={m} type="button" role="radio" aria-checked={mins === m} onClick={() => setMins(m)}>{m} dk</button>
              ))}
            </div>
          </div>
          <div className="lf-field">
            <span className="ls-eyebrow">Hedef</span>
            <div className="lf-goals" role="radiogroup" aria-label="Hedef">
              <button type="button" role="radio" aria-checked={goalKind === 'section'} disabled={!section} onClick={() => setGoalKind('section')}>
                <b>Bu bölümü bitir</b>
                <small>{section ? `Bölüm ${(cur?.section ?? 0) + 1}: ${section.name} · ${sectionLeft.length} adım kaldı` : 'Bölüm yok'}</small>
              </button>
              <button type="button" role="radio" aria-checked={goalKind === 'steps'} onClick={() => setGoalKind('steps')}>
                <b>Adım sayısı</b>
                <small>Belirli sayıda adım tamamla</small>
              </button>
              <button type="button" role="radio" aria-checked={goalKind === 'time'} onClick={() => setGoalKind('time')}>
                <b>Süre dolana kadar</b>
                <small>Hedef yok, yalnız süre</small>
              </button>
            </div>
            {goalKind === 'steps' && (
              <div className="ls-seg" role="radiogroup" aria-label="Adım sayısı">
                {[5, 10, 15].map((k) => (
                  <button key={k} type="button" role="radio" aria-checked={goalN === k} onClick={() => setGoalN(k)}>{k} adım</button>
                ))}
              </div>
            )}
          </div>
          <button type="button" className="ls-btn is-primary lf-start" onClick={start}><Play aria-hidden /> Seansı başlat</button>
        </div>
      </Sheet>

      {run && (phase === 'running' || phase === 'paused') && (
        <div className={`lf-bar ${phase === 'paused' ? 'is-paused' : ''}`} role="status" aria-label="Odak seansı">
          <Timer aria-hidden />
          <b className="lf-time" title="Kalan süre">{mmss(left)}</b>
          <span className="lf-goal" title={run.goal.label}>
            <Target aria-hidden />
            <span className="lf-goal-t">{run.goal.kind === 'time' ? 'Süre hedefi' : run.goal.kind === 'steps' ? `Hedef ${progress.label}` : `${run.goal.label} · ${progress.label}`}</span>
          </span>
          <span className="sp" />
          {phase === 'running' ? (
            <button type="button" className="ls-btn is-sm is-ghost" onClick={() => setPhase('paused')} aria-label="Duraklat"><Pause aria-hidden /></button>
          ) : (
            <button type="button" className="ls-btn is-sm is-ghost" onClick={resume} aria-label="Devam et"><Play aria-hidden /></button>
          )}
          <button type="button" className="ls-btn is-sm is-ghost" onClick={takeBreak} aria-label="Mola ver" title="3 dakikalık mola"><Coffee aria-hidden /></button>
          <button type="button" className="ls-btn is-sm" onClick={finish}>Bitir</button>
          <i className="lf-line" style={{ width: `${goalPct}%` }} aria-hidden />
        </div>
      )}

      {phase === 'paused' && autoPaused && cur && (
        <div className="lf-toast" role="alert">
          <span><b>Seans duraklatıldı.</b> Kaldığın yer: Adım {cur.number} · {cur.topic}</span>
          <button type="button" className="ls-btn is-sm is-primary" onClick={resume}><Play aria-hidden /> Devam et</button>
        </div>
      )}

      {nudge && phase === 'running' && (
        <div className="lf-toast is-nudge" role="status">
          <span>
            {nudge === 'pulse'
              ? <><b>Art arda hızlı ve yanlış cevaplar.</b> Bu genelde yorgunluk işaretidir; kısa bir mola dikkati toplar.</>
              : <><b>25 dakikadır çalışıyorsun.</b> 3 dakikalık bir mola sonraki bölümü daha verimli yapar.</>}
          </span>
          <button type="button" className="ls-btn is-sm is-primary" onClick={takeBreak}><Coffee aria-hidden /> Mola ver</button>
          <button type="button" className="ls-btn is-sm is-ghost" onClick={() => setNudge(null)}>Devam</button>
        </div>
      )}

      {phase === 'break' && (
        <div className="lf-overlay" role="dialog" aria-modal="true" aria-label="Mola">
          <div className="lf-break">
            <span className="ls-eyebrow">Mola · süreden sayılmaz</span>
            <div className="lf-breath" aria-hidden><i /></div>
            <b className="lf-break-time">{mmss(breakLeft)}</b>
            <ul>
              <li>Halka büyürken nefes al, küçülürken ver.</li>
              <li>Ekrandan kalk, 6 metre uzağa 20 saniye bak.</li>
              <li>Su iç; telefona değil pencereye bak.</li>
            </ul>
            <button type="button" className="ls-btn is-primary" onClick={resume}>{breakLeft > 0 ? 'Molayı bitir' : 'Derse dön'}</button>
          </div>
        </div>
      )}

      {phase === 'receipt' && run && stats && (
        <div className="lf-overlay" role="dialog" aria-modal="true" aria-label="Seans özeti">
          <div className="lf-receipt">
            <header>
              <span className="lf-receipt-ico"><Check aria-hidden /></span>
              <div>
                <b>{goalHit ? 'Hedef tamam' : 'Seans bitti'}</b>
                <small>{deckTitle} · {run.goal.label}</small>
              </div>
              <button type="button" className="ls-btn is-icon is-ghost" onClick={close} aria-label="Kapat"><X aria-hidden /></button>
            </header>
            <dl className="lf-stats">
              <div><dt>Süre</dt><dd>{Math.max(1, Math.round(run.activeMs / MIN))} dk</dd></div>
              <div><dt>Biten adım</dt><dd>{stats.stepsDone}</dd></div>
              <div><dt>Etkileşim</dt><dd>{stats.ix}</dd></div>
              <div><dt>Doğruluk</dt><dd>{stats.pct == null ? '—' : `%${stats.pct}`}</dd></div>
            </dl>
            {stats.weak.length > 0 && (
              <div className="lf-weak">
                <span className="ls-eyebrow">En çok zorlandığın adımlar</span>
                {stats.weak.map((w) => (
                  <button key={w.slide} type="button" onClick={() => { close(); onJump(w.slide); }}>
                    <span className="n">{w.slide}</span>
                    <span className="t">{w.title}</span>
                    <small>{w.wrong} yanlış</small>
                  </button>
                ))}
              </div>
            )}
            <div className="lf-actions">
              {onReview && openErr > 0 && (
                <button type="button" className="ls-btn is-primary" onClick={() => { close(); onReview(); }}><RotateCcw aria-hidden /> Hatalarını tekrar et ({openErr})</button>
              )}
              <button type="button" className="ls-btn" onClick={extend}><Timer aria-hidden /> 10 dk daha</button>
              <button type="button" className="ls-btn is-ghost" onClick={close}>Kapat</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
