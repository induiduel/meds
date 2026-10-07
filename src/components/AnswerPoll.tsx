import React, { useEffect, useRef, useState } from 'react';
import { BarChart3, Check, Users } from 'lucide-react';
import { ApiService, AnswerVotes } from '../services/api';
import { Highlight } from './ui/StemText';

const KEYS = ['A', 'B', 'C', 'D', 'E'];

/** 0 → hedef sayı, kısa ve yavaşlayarak (hareketi azalt tercihinde anında). */
function useCountUp(target: number, run: boolean, ms = 750): number {
  const [v, setV] = useState(0);
  useEffect(() => {
    if (!run) return;
    if (typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) {
      setV(target);
      return;
    }
    let raf = 0;
    const from = v;
    const t0 = performance.now();
    const step = (t: number) => {
      const p = Math.min(1, (t - t0) / ms);
      const e = 1 - Math.pow(1 - p, 3);
      setV(Math.round(from + (target - from) * e));
      if (p < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target, run]);
  return v;
}

const Pct: React.FC<{ value: number; run: boolean }> = ({ value, run }) => <>%{useCountUp(value, run)}</>;

interface Props {
  questionId: string;
  options: { key: string; text: string }[] | Record<string, string>;
  voterUid: string | null;
  /** Anketin neden açık olduğu (tek satır) */
  hint?: string;
  terms?: string[];
  className?: string;
  /** Şık metnini özel çiz (ör. inceleme ekranında kelime farkı) */
  renderText?: (key: string, text: string) => React.ReactNode;
  /** Oylar her yüklendiğinde/değiştiğinde (ör. yönetici için öndeki şık) */
  onVotes?: (v: AnswerVotes) => void;
}

/**
 * Cevap anketi: şıklar anketin kendisidir. Her şıkkın arkasındaki çubuk oy oranıyla dolar,
 * en çok oy alan şık yeşille öne çıkar, kullanıcının oyu işaretlenir. Dağılım her zaman görünür.
 * Oylar görünür olunca yüklenir (uzun listede tek tek istek yağmuru olmasın).
 */
export const AnswerPoll: React.FC<Props> = ({ questionId, options, voterUid, hint, terms, className = '', renderText, onVotes }) => {
  const rootRef = useRef<HTMLElement>(null);
  const [visible, setVisible] = useState(false);
  const [votes, setVotes] = useState<AnswerVotes | null>(null);
  const [picked, setPicked] = useState<string | null>(null);
  const [run, setRun] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const el = rootRef.current;
    if (!el || typeof IntersectionObserver === 'undefined') { setVisible(true); return; }
    const io = new IntersectionObserver((es) => es.some((e) => e.isIntersecting) && (setVisible(true), io.disconnect()), { rootMargin: '200px' });
    io.observe(el);
    return () => io.disconnect();
  }, []);

  useEffect(() => {
    if (!visible) return;
    let alive = true;
    ApiService.getAnswerVotes(questionId, voterUid || '')
      .then((v) => alive && setVotes(v))
      .catch((e) => alive && setError(e.message));
    return () => { alive = false; };
  }, [visible, questionId, voterUid]);

  useEffect(() => {
    if (!votes) return;
    onVotes?.(votes);
    const id = requestAnimationFrame(() => setRun(true));
    return () => cancelAnimationFrame(id);
  }, [votes]);

  const rows = (Array.isArray(options) ? options : Object.entries(options || {}).map(([key, text]) => ({ key, text })))
    .map((o) => ({ key: String(o.key).toUpperCase(), text: String(o.text ?? '') }))
    .filter((o) => KEYS.includes(o.key));

  const total = votes?.total ?? 0;
  const counts = votes?.counts || {};
  const max = Math.max(0, ...KEYS.map((k) => counts[k] || 0));
  const leaders = KEYS.filter((k) => total > 0 && (counts[k] || 0) === max);
  const myVote = votes?.myVote || null;
  const canVote = Boolean(voterUid) && !myVote && !!votes;

  const submit = async (choice: string) => {
    if (!voterUid || busy || myVote) return;
    setBusy(true);
    setError('');
    try {
      setVotes(await ApiService.castAnswerVote(questionId, voterUid, choice));
      setPicked(null);
    } catch (e: any) {
      setError(e.message);
      ApiService.getAnswerVotes(questionId, voterUid).then(setVotes).catch(() => {});
    } finally {
      setBusy(false);
    }
  };

  const status = !votes
    ? error || 'Oylar yükleniyor…'
    : myVote
    ? `Oyun kaydedildi: ${myVote}`
    : !voterUid
    ? 'Oy vermek için giriş yap'
    : picked
    ? 'Seçimini onayla'
    : 'Doğru bildiğin şıkka dokun';

  return (
    <section ref={rootRef} className={`ms-poll ${className}`} aria-label="Cevap anketi" aria-busy={!votes}>
      <header className="ms-poll-head">
        <BarChart3 className="w-4 h-4 shrink-0" aria-hidden />
        <span className="font-semibold text-ink">Cevap anketi</span>
        <span className="ms-poll-total"><Users className="w-3.5 h-3.5" aria-hidden /> {total.toLocaleString('tr-TR')} oy</span>
        <span className={`ms-poll-status ${myVote ? 'is-done' : ''} ${error ? 'is-err' : ''}`}>{error && votes ? error : status}</span>
      </header>
      {hint && <p className="ms-poll-hint">{hint}</p>}

      <ol className="ms-poll-list">
        {rows.map((o, i) => {
          const n = counts[o.key] || 0;
          const pct = total ? Math.round((n / total) * 100) : 0;
          const lead = leaders.includes(o.key);
          const mine = myVote === o.key;
          const sel = !myVote && picked === o.key;
          return (
            <li key={o.key}>
              <button
                type="button"
                className={`ms-poll-row ${lead ? 'is-lead' : ''} ${mine ? 'is-mine' : ''} ${sel ? 'is-picked' : ''}`}
                onClick={() => canVote && setPicked((p) => (p === o.key ? null : o.key))}
                disabled={!canVote || busy}
                aria-pressed={sel || mine}
                aria-label={`${o.key} şıkkı, ${n} oy, yüzde ${pct}${lead ? ', en çok oy' : ''}${mine ? ', senin oyun' : ''}`}
              >
                <span className="ms-poll-fill" style={{ width: run ? `${pct}%` : '0%', transitionDelay: `${i * 55}ms` }} aria-hidden />
                <span className="ms-poll-key">{mine ? <Check className="w-3.5 h-3.5" strokeWidth={3} /> : o.key}</span>
                <span className="ms-poll-text">{renderText ? renderText(o.key, o.text) : <Highlight text={o.text} terms={terms} />}</span>
                <span className="ms-poll-meta">
                  {lead && <span className="ms-poll-tag">{leaders.length > 1 ? 'Eşit' : 'Önde'}</span>}
                  <span className="ms-poll-pct"><Pct value={pct} run={run} /></span>
                </span>
              </button>
            </li>
          );
        })}
      </ol>

      {picked && canVote && (
        <div className="ms-poll-confirm ms-pop-in">
          <span className="text-[13px] text-ink-2 min-w-0 flex-1">
            <b className="text-ink">{picked}</b> şıkkına oy vereceksin. Oy bir kez verilir.
          </span>
          <button type="button" onClick={() => setPicked(null)} className="ms-btn is-ghost is-sm">Vazgeç</button>
          <button type="button" onClick={() => submit(picked)} disabled={busy} className="ms-btn is-primary is-sm">
            {busy ? 'Gönderiliyor…' : 'Oyu gönder'}
          </button>
        </div>
      )}
    </section>
  );
};
