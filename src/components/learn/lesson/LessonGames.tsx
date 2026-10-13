/**
 * Ders sonu oyunları (rehber §5.14): yalnız destenin SON slaytında (`isGameFinale: true`,
 * başlık "[OYUN SAYFASI] …") kullanılan dört etkileşim türü.
 *
 *  - sequence_order  Sırala            karışık basamakları dokunarak doğru sıraya diz
 *  - estimate_slider Değeri tahmin et  kaydırıcıyla sayısal değeri tahmin et (tolerans içinde doğru)
 *  - perturbation    Ne değişir?       bir müdahale sonrası her parametre için ↑ / ↓ / = seç
 *  - fix_the_text    Hatayı düzelt     paragraftaki yanlış kelimeleri bul, doğrusunu seç
 *
 * Son slaytta olduğu için ders boyunca anlatılan her şeyi sorabilirler (kronoloji kuralı kendiliğinden sağlanır).
 * Stil: styles/learn-games.css (.lg-*). Renkler yalnız --color-* token'larıyla.
 */
import React, { useMemo, useState } from 'react';
import { ArrowDown, ArrowUp, Check, Equal, RotateCcw, X } from 'lucide-react';
import '../../../styles/learn-games.css';

type Done = (() => void) | undefined;

const shuffle = <T,>(a: T[], seed: number): T[] => {
  // Tohumlu karıştırma: aynı oyun her açılışta aynı karışık sırayla gelir (yeniden denemede tohum değişir)
  const out = [...a];
  let s = seed || 1;
  for (let i = out.length - 1; i > 0; i--) {
    s = (s * 9301 + 49297) % 233280;
    const j = Math.floor((s / 233280) * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
};
const hashStr = (t: string) => [...t].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7);
const txt = (x: any) => String(typeof x === 'string' ? x : x?.text || x?.label || '').replace(/^\d+[.)]\s*/, '').trim();

const Verdict: React.FC<{ ok: boolean; good: string; bad: string; why?: string }> = ({ ok, good, bad, why }) => (
  <p className={`ls-fb ${ok ? 'is-ok' : 'is-bad'}`} role="status">
    <b>{ok ? good : bad}</b>
    {why && <> {why}</>}
  </p>
);

/* ------------------------------------------------------------------ Sırala */
export const SequenceOrder: React.FC<{ e: any; onDone?: Done }> = ({ e, onDone }) => {
  const steps: string[] = (e.steps || e.items || []).map(txt).filter(Boolean);
  const [round, setRound] = useState(1);
  const pool = useMemo(() => {
    let p = shuffle(steps.map((_, i) => i), hashStr(steps.join('|')) + round);
    if (p.every((v, i) => v === i) && p.length > 1) p = [...p.slice(1), p[0]]; // hiç karışmadıysa kaydır
    return p;
  }, [steps.join('|'), round]); // eslint-disable-line react-hooks/exhaustive-deps
  const [picked, setPicked] = useState<number[]>([]);
  const [checked, setChecked] = useState(false);
  const full = picked.length === steps.length;
  const right = checked && picked.every((v, i) => v === i);
  const restart = () => {
    setPicked([]);
    setChecked(false);
    setRound((r) => r + 1);
  };
  return (
    <div className="ls-ix-body">
      <p className="ls-ix-q">{e.prompt || e.title || 'Basamakları doğru sıraya diz.'}</p>
      <ol className="lg-seq" aria-label="Senin sıran">
        {steps.map((_, i) => {
          const v = picked[i];
          const state = !checked || v == null ? '' : v === i ? 'is-ok' : 'is-bad';
          return (
            <li key={i} className={`lg-seq-slot ${v == null ? 'is-empty' : ''} ${state}`}>
              <span className="n">{i + 1}</span>
              {v == null ? (
                <span className="t is-ph">{i === picked.length ? 'Sıradaki basamağı aşağıdan seç' : ''}</span>
              ) : (
                <button type="button" className="t" disabled={checked} onClick={() => setPicked((p) => p.filter((x) => x !== v))} aria-label={`${steps[v]} — geri al`}>
                  {steps[v]}
                </button>
              )}
              {checked && v != null && v !== i && <span className="lg-seq-fix">Doğrusu: {steps[i]}</span>}
            </li>
          );
        })}
      </ol>
      {!checked && pool.some((i) => !picked.includes(i)) && (
        <div className="lg-pool" role="group" aria-label="Karışık basamaklar">
          {pool.filter((i) => !picked.includes(i)).map((i) => (
            <button key={i} type="button" className="lg-chip" onClick={() => setPicked((p) => [...p, i])}>
              {steps[i]}
            </button>
          ))}
        </div>
      )}
      <div className="lg-actions">
        {!checked ? (
          <button
            type="button"
            className="ls-btn is-primary"
            disabled={!full}
            onClick={() => {
              setChecked(true);
              onDone?.();
            }}
          >
            <Check aria-hidden /> Kontrol et
          </button>
        ) : (
          <button type="button" className="ls-btn" onClick={restart}><RotateCcw aria-hidden /> Yeniden dene</button>
        )}
      </div>
      {checked && (
        <Verdict
          ok={right}
          good="Sıra doğru."
          bad={`${picked.filter((v, i) => v === i).length}/${steps.length} basamak yerinde.`}
          why={e.explanation}
        />
      )}
    </div>
  );
};

/* ------------------------------------------------------------------ Değeri tahmin et */
const fmt = (n: number, step: number) => {
  const d = step < 1 ? Math.min(3, String(step).split('.')[1]?.length || 1) : 0;
  return n.toLocaleString('tr-TR', { minimumFractionDigits: d, maximumFractionDigits: d });
};
export const EstimateSlider: React.FC<{ e: any; onDone?: Done }> = ({ e, onDone }) => {
  const rounds: any[] = Array.isArray(e.items) && e.items.length ? e.items : [e];
  const [r, setR] = useState(0);
  const cur = rounds[r] || {};
  const min = Number(cur.min ?? 0);
  const max = Number(cur.max ?? 100);
  const step = Number(cur.step ?? (max - min > 20 ? 1 : 0.1));
  const answer = Number(cur.answer);
  const tol = Math.abs(Number(cur.tolerance ?? 0));
  const [val, setVal] = useState<number>(() => +(min + (max - min) / 2).toFixed(3));
  const [shown, setShown] = useState(false);
  const [score, setScore] = useState(0);
  const ok = Math.abs(val - answer) <= tol + 1e-9;
  const pct = (x: number) => `${((x - min) / (max - min || 1)) * 100}%`;
  const next = () => {
    const nr = r + 1;
    setR(nr);
    setShown(false);
    const n = rounds[nr] || {};
    setVal(+(Number(n.min ?? 0) + (Number(n.max ?? 100) - Number(n.min ?? 0)) / 2).toFixed(3));
  };
  const finished = shown && r + 1 >= rounds.length;
  return (
    <div className="ls-ix-body">
      {rounds.length > 1 && <span className="lg-count">Tur {r + 1} / {rounds.length}</span>}
      <p className="ls-ix-q">{cur.prompt || cur.question}</p>
      <div className="lg-est">
        <output className="lg-est-val" aria-live="polite">
          {fmt(val, step)} {cur.unit && <small>{cur.unit}</small>}
        </output>
        <div className="lg-est-track">
          {shown && <span className="lg-est-band" style={{ left: pct(Math.max(min, answer - tol)), width: `calc(${pct(Math.min(max, answer + tol))} - ${pct(Math.max(min, answer - tol))})` }} aria-hidden />}
          {shown && <span className="lg-est-ans" style={{ left: pct(answer) }} aria-hidden />}
          <input
            type="range"
            min={min}
            max={max}
            step={step}
            value={val}
            disabled={shown}
            onChange={(ev) => setVal(Number(ev.target.value))}
            aria-label={`Tahminin${cur.unit ? ` (${cur.unit})` : ''}`}
          />
        </div>
        <div className="lg-est-scale" aria-hidden>
          <span>{fmt(min, step)}</span>
          <span>{fmt(max, step)}</span>
        </div>
      </div>
      <div className="lg-actions">
        {!shown ? (
          <button
            type="button"
            className="ls-btn is-primary"
            onClick={() => {
              setShown(true);
              if (ok) setScore((s) => s + 1);
              if (r + 1 >= rounds.length) onDone?.();
            }}
          >
            <Check aria-hidden /> Tahmini kilitle
          </button>
        ) : r + 1 < rounds.length ? (
          <button type="button" className="ls-btn is-primary" onClick={next}>Sonraki tur</button>
        ) : null}
      </div>
      {shown && (
        <Verdict
          ok={ok}
          good="Aralıkta."
          bad={`Doğrusu ${fmt(answer, step)}${cur.unit ? ` ${cur.unit}` : ''}${tol ? ` (±${fmt(tol, step)})` : ''}.`}
          why={cur.explanation}
        />
      )}
      {finished && rounds.length > 1 && <span className="lg-count">Sonuç: {score} / {rounds.length} tur aralıkta</span>}
    </div>
  );
};

/* ------------------------------------------------------------------ Ne değişir? */
type Dir = 'up' | 'down' | 'same';
const normDir = (x: any): Dir => {
  const t = String(x || '').toLocaleLowerCase('tr-TR');
  if (/^(up|artar|art|↑|\+|yüksel|inc)/.test(t)) return 'up';
  if (/^(down|azalır|aza|↓|-|düş|dec)/.test(t)) return 'down';
  return 'same';
};
const DIRS: [Dir, React.ElementType, string][] = [
  ['up', ArrowUp, 'Artar'],
  ['down', ArrowDown, 'Azalır'],
  ['same', Equal, 'Değişmez'],
];
export const Perturbation: React.FC<{ e: any; onDone?: Done }> = ({ e, onDone }) => {
  const params: any[] = e.parameters || e.items || [];
  const [ans, setAns] = useState<Record<number, Dir>>({});
  const [checked, setChecked] = useState(false);
  const all = params.length > 0 && Object.keys(ans).length === params.length;
  const correct = params.reduce((a, p, i) => (ans[i] === normDir(p.correct) ? a + 1 : a), 0);
  return (
    <div className="ls-ix-body">
      {e.scenario && <p className="lg-case">{e.scenario}</p>}
      <p className="ls-ix-q">{e.question || 'Her parametre nasıl değişir?'}</p>
      <ul className="lg-pert">
        {params.map((p, i) => {
          const target = normDir(p.correct);
          const mine = ans[i];
          const state = checked ? (mine === target ? 'is-ok' : 'is-bad') : '';
          return (
            <li key={i} className={state}>
              <span className="lg-pert-name">{p.name || p.parameter}</span>
              <span className="lg-pert-btns" role="radiogroup" aria-label={p.name || p.parameter}>
                {DIRS.map(([d, Icon, label]) => (
                  <button
                    key={d}
                    type="button"
                    role="radio"
                    aria-checked={mine === d}
                    aria-label={label}
                    title={label}
                    disabled={checked}
                    className={`lg-dir ${mine === d ? 'is-on' : ''} ${checked && d === target ? 'is-target' : ''}`}
                    onClick={() => setAns((a) => ({ ...a, [i]: d }))}
                  >
                    <Icon aria-hidden />
                  </button>
                ))}
              </span>
              {checked && p.explanation && <span className="lg-pert-why">{p.explanation}</span>}
            </li>
          );
        })}
      </ul>
      <div className="lg-actions">
        {!checked ? (
          <button
            type="button"
            className="ls-btn is-primary"
            disabled={!all}
            onClick={() => {
              setChecked(true);
              onDone?.();
            }}
          >
            <Check aria-hidden /> Kontrol et
          </button>
        ) : (
          <button type="button" className="ls-btn" onClick={() => { setAns({}); setChecked(false); }}><RotateCcw aria-hidden /> Yeniden dene</button>
        )}
      </div>
      {checked && <Verdict ok={correct === params.length} good="Hepsi doğru." bad={`${correct}/${params.length} doğru.`} why={e.explanation} />}
    </div>
  );
};

/* ------------------------------------------------------------------ Hatayı düzelt */
interface FixErr { wrong: string; correct: string; options: string[]; explanation?: string }
type Seg = { t: string; err?: number };
const segmentText = (text: string, errs: FixErr[]): Seg[] => {
  // Hatalı ifadeleri metinde ilk geçtikleri yerden ayır; geri kalan kelimeler de dokunulabilir (yanlış dokunuş sayılır)
  const marks: { s: number; e: number; i: number }[] = [];
  const low = text.toLocaleLowerCase('tr-TR');
  errs.forEach((er, i) => {
    const at = low.indexOf(er.wrong.toLocaleLowerCase('tr-TR'));
    if (at >= 0 && !marks.some((m) => at < m.e && at + er.wrong.length > m.s)) marks.push({ s: at, e: at + er.wrong.length, i });
  });
  marks.sort((a, b) => a.s - b.s);
  const out: Seg[] = [];
  let pos = 0;
  const words = (chunk: string) => chunk.split(/(\s+)/).forEach((w) => w && out.push({ t: w }));
  marks.forEach((m) => {
    words(text.slice(pos, m.s));
    out.push({ t: text.slice(m.s, m.e), err: m.i });
    pos = m.e;
  });
  words(text.slice(pos));
  return out;
};
export const FixTheText: React.FC<{ e: any; onDone?: Done }> = ({ e, onDone }) => {
  const errs: FixErr[] = (e.errors || []).filter((x: any) => x?.wrong && x?.correct);
  const text = String(e.text || '');
  const segs = useMemo(() => segmentText(text, errs), [text, errs.length]); // eslint-disable-line react-hooks/exhaustive-deps
  const [open, setOpen] = useState<number | null>(null);
  const [fixed, setFixed] = useState<Record<number, { pick: string; ok: boolean }>>({});
  const [miss, setMiss] = useState<number | null>(null);
  const [misses, setMisses] = useState(0);
  const doneN = Object.keys(fixed).length;
  const opts = (er: FixErr) => {
    const set = Array.from(new Set([er.correct, ...(er.options || [])].map((s) => String(s).trim()).filter(Boolean)));
    return shuffle(set, hashStr(er.wrong));
  };
  const choose = (i: number, pick: string) => {
    const ok = pick.trim().toLocaleLowerCase('tr-TR') === errs[i].correct.trim().toLocaleLowerCase('tr-TR');
    const next = { ...fixed, [i]: { pick, ok } };
    setFixed(next);
    setOpen(null);
    if (Object.keys(next).length === errs.length) onDone?.();
  };
  const ok = errs.filter((_, i) => fixed[i]?.ok).length;
  return (
    <div className="ls-ix-body">
      <p className="ls-ix-q">{e.prompt || `Metinde ${errs.length} hata var. Hatalı kelimeye dokun, doğrusunu seç.`}</p>
      <p className="lg-fix">
        {segs.map((s, k) => {
          if (/^\s+$/.test(s.t)) return s.t;
          if (s.err == null) {
            if (!/[\p{L}\d]/u.test(s.t)) return <span key={k}>{s.t}</span>;
            return (
              <button
                key={k}
                type="button"
                className={`lg-w ${miss === k ? 'is-miss' : ''}`}
                disabled={doneN === errs.length}
                onClick={() => {
                  setMiss(k);
                  setMisses((m) => m + 1);
                  window.setTimeout(() => setMiss((v) => (v === k ? null : v)), 600);
                }}
              >
                {s.t}
              </button>
            );
          }
          const f = fixed[s.err];
          return (
            <span key={k} className="lg-err-wrap">
              <button
                type="button"
                className={`lg-w lg-err ${f ? (f.ok ? 'is-ok' : 'is-bad') : ''} ${open === s.err ? 'is-open' : ''}`}
                disabled={!!f}
                aria-expanded={open === s.err}
                onClick={() => setOpen((o) => (o === s.err ? null : s.err!))}
              >
                {f ? (f.ok ? errs[s.err].correct : <><s>{f.pick}</s> {errs[s.err].correct}</>) : s.t}
              </button>
              {open === s.err && !f && (
                <span className="lg-fix-pop" role="group" aria-label="Doğrusu hangisi?">
                  {opts(errs[s.err]).map((o) => (
                    <button key={o} type="button" className="lg-chip" onClick={() => choose(s.err!, o)}>{o}</button>
                  ))}
                  <button type="button" className="lg-chip is-ghost" onClick={() => setOpen(null)} aria-label="Kapat"><X aria-hidden /></button>
                </span>
              )}
            </span>
          );
        })}
      </p>
      <span className="lg-count">{doneN}/{errs.length} hata bulundu{misses ? ` · ${misses} yanlış dokunuş` : ''}</span>
      {doneN === errs.length && (
        <>
          <Verdict ok={ok === errs.length && misses === 0} good="Metni kusursuz düzelttin." bad={`${ok}/${errs.length} doğru düzeltme.`} />
          <ul className="lg-fix-why">
            {errs.map((er, i) => (
              <li key={i}><s>{er.wrong}</s> → <b>{er.correct}</b>{er.explanation && <>: {er.explanation}</>}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
};

export const GAME_TYPES = ['sequence_order', 'estimate_slider', 'perturbation', 'fix_the_text'] as const;
