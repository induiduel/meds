import React, { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, ArrowRight, Bookmark, BookmarkCheck, NotebookPen, RotateCcw, Shuffle, Check, X as XIcon, SlidersHorizontal, ChevronDown, ChevronUp, Sparkles } from 'lucide-react';
import { Committee } from '../../types';
import {
  StudyQuestion,
  OptionKey,
  getProgress,
  recordAttempt,
  getReview,
  setInReview,
  shuffle,
  getNotes,
  saveNotes,
  newNoteId,
  resetProgress,
} from '../../services/studyStore';
import { committeeShortLabel } from '../QuickAddHero';
import { Segmented, OptionButton, ExplanationBlock, EmptyState, cardCls, btnPrimary, btnSecondary, btnGhost, selectCls, Field, isTypingTarget } from './StudyUI';
import { QuestionAiChatDrawer } from '../QuestionAiChatDrawer';

type Mode = 'all' | 'unsolved' | 'review' | 'wrong';

interface SolveViewProps {
  bank: StudyQuestion[];
  committees: Committee[];
  loading: boolean;
  initialCommitteeId?: string;
  onProgressChange?: () => void;
}

export const SolveView: React.FC<SolveViewProps> = ({ bank, committees, loading, initialCommitteeId, onProgressChange }) => {
  const [committeeId, setCommitteeId] = useState(() => {
    if (initialCommitteeId && initialCommitteeId !== 'all') return initialCommitteeId;
    return 'all';
  });
  const [discipline, setDiscipline] = useState('all');
  const [source, setSource] = useState<'all' | 'arşiv' | 'havuz'>('all');
  const [mode, setMode] = useState<Mode>('all');
  const [shuffled, setShuffled] = useState(false);
  const [seed, setSeed] = useState(0);
  const [index, setIndex] = useState(0);
  const [progress, setProgress] = useState(getProgress);
  const [review, setReview] = useState(getReview);
  const [noteOpen, setNoteOpen] = useState(false);
  const [noteText, setNoteText] = useState('');
  const [noteSaved, setNoteSaved] = useState(false);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [aiChatOpen, setAiChatOpen] = useState(false);

  const committeeName = (id: string) => {
    const c = committees.find((x) => x.id === id);
    if (c) return committeeShortLabel(c).charAt(0) + committeeShortLabel(c).slice(1).toLocaleLowerCase('tr-TR');
    const m = id.match(/kurul(\d+)/i);
    return m ? `Kurul ${m[1]}` : /final/i.test(id) ? 'Final' : id;
  };

  const committeeIds = useMemo(() => {
    const fromCommittees = committees.map((c) => c.id);
    const fromBank = new Set(bank.map((q) => q.committeeId).filter(Boolean));
    const ordered = fromCommittees.filter((id) => fromBank.has(id));
    const others = [...fromBank].filter((id) => !fromCommittees.includes(id)).sort();
    return [...ordered, ...others];
  }, [bank, committees]);

  const scoped = useMemo(
    () => bank.filter((q) => (committeeId === 'all' || q.committeeId === committeeId) && (source === 'all' || q.source === source)),
    [bank, committeeId, source]
  );

  const disciplines = useMemo(() => {
    const m: Record<string, { total: number; solved: number; correct: number }> = {};
    scoped.forEach((q) => {
      const d = (m[q.discipline] ||= { total: 0, solved: 0, correct: 0 });
      d.total++;
      const p = progress[q.id];
      if (p) {
        d.solved++;
        if (p.correct) d.correct++;
      }
    });
    return Object.entries(m).sort((a, b) => b[1].total - a[1].total);
  }, [scoped, progress]);

  const list = useMemo(() => {
    let l = scoped.filter((q) => discipline === 'all' || q.discipline === discipline);
    if (mode === 'unsolved') l = l.filter((q) => !progress[q.id]);
    if (mode === 'review') l = l.filter((q) => review.has(q.id));
    if (mode === 'wrong') l = l.filter((q) => progress[q.id] && !progress[q.id].correct);
    if (shuffled) l = shuffle(l);
    else l = [...l].sort((a, b) => a.committeeId.localeCompare(b.committeeId) || a.year.localeCompare(b.year) || a.number - b.number);
    return l;
    // progress intentionally excluded for 'unsolved' so the current card does not vanish after answering
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [scoped, discipline, mode, shuffled, seed, review]);

  useEffect(() => setIndex(0), [committeeId, discipline, source, mode, shuffled, seed]);
  useEffect(() => {
    setNoteOpen(false);
    setNoteText('');
    setNoteSaved(false);
  }, [index, list]);

  const q = list[Math.min(index, Math.max(0, list.length - 1))];
  const attempt = q ? progress[q.id] : undefined;
  const answered = !!attempt;

  const pick = (key: OptionKey) => {
    if (!q || answered) return;
    const next = recordAttempt(q.id, key, key === q.answer);
    setProgress({ ...next });
    setReview(getReview());
    onProgressChange?.();
  };

  const retry = () => {
    if (!q) return;
    resetProgress([q.id]);
    setProgress(getProgress());
    onProgressChange?.();
  };

  const toggleReview = () => {
    if (!q) return;
    setReview(new Set(setInReview(q.id, !review.has(q.id))));
    onProgressChange?.();
  };

  const go = (d: number) => setIndex((i) => Math.max(0, Math.min(list.length - 1, i + d)));

  // Keyboard: A–E to answer, ←/→ to move
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (isTypingTarget(e.target) || e.metaKey || e.ctrlKey || e.altKey) return;
      const k = e.key.toUpperCase();
      if (q && ['A', 'B', 'C', 'D', 'E'].includes(k) && q.options.some((o) => o.key === k)) {
        e.preventDefault();
        pick(k as OptionKey);
      } else if (e.key === 'ArrowRight') go(1);
      else if (e.key === 'ArrowLeft') go(-1);
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  });

  const saveNote = () => {
    if (!q || !noteText.trim()) return;
    const now = new Date().toISOString();
    saveNotes([
      {
        id: newNoteId(),
        title: noteText.trim().split('\n')[0].slice(0, 80),
        body: noteText.trim(),
        discipline: q.discipline,
        questionId: q.id,
        questionStem: q.stem.slice(0, 280),
        createdAt: now,
        updatedAt: now,
      },
      ...getNotes(),
    ]);
    setNoteSaved(true);
    setNoteOpen(false);
    setNoteText('');
  };

  const solvedInScope = scoped.filter((q2) => progress[q2.id]).length;
  const correctInScope = scoped.filter((q2) => progress[q2.id]?.correct).length;

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[260px_minmax(0,1fr)] gap-3 sm:gap-5 items-start">
      {/* ---------- Filters ---------- */}
      <aside aria-label="Filtreler" className={`${cardCls} p-2 lg:p-4 flex flex-col gap-3 lg:sticky lg:top-[88px]`}>
        <button
          type="button"
          onClick={() => setFiltersOpen((v) => !v)}
          aria-expanded={filtersOpen}
          aria-controls="solve-filters"
          className="lg:hidden min-h-10 px-2 rounded-[10px] flex items-center gap-2 text-left cursor-pointer"
        >
          <SlidersHorizontal className="w-4 h-4 text-ink-2 shrink-0" />
          <span className="flex-1 min-w-0 text-[14px] truncate">
            <strong className="font-semibold">{committeeId === 'all' ? 'Tüm kurullar' : committeeName(committeeId)}</strong>
            <span className="text-ink-2">
              {' · '}
              {discipline === 'all' ? 'Tüm dersler' : discipline}
              {mode !== 'all' ? ` · ${mode === 'unsolved' ? 'Çözülmemiş' : mode === 'wrong' ? 'Yanlışlar' : 'Tekrar'}` : ''}
            </span>
          </span>
          <span className="font-mono text-[12px] text-ink-3 shrink-0">{list.length}</span>
          {filtersOpen ? <ChevronUp className="w-4 h-4 text-ink-2" /> : <ChevronDown className="w-4 h-4 text-ink-2" />}
        </button>
        <div id="solve-filters" className={`${filtersOpen ? 'flex' : 'hidden'} lg:flex flex-col gap-3 px-1 pb-1 lg:p-0`}>
        <div className="grid grid-cols-2 lg:grid-cols-1 gap-2.5">
          <Field label="Kurul">
            <select value={committeeId} onChange={(e) => setCommitteeId(e.target.value)} className={selectCls}>
              <option value="all">Tüm kurullar</option>
              {committeeIds.map((id) => (
                <option key={id} value={id}>
                  {committeeName(id)}
                </option>
              ))}
            </select>
          </Field>
          <Field label="Kaynak">
            <select value={source} onChange={(e) => setSource(e.target.value as any)} className={selectCls}>
              <option value="all">Tümü</option>
              <option value="arşiv">Çıkmış sorular</option>
              <option value="havuz">Kurulan havuz soruları</option>
            </select>
          </Field>
        </div>

        <Field label="Göster" className="lg:hidden">
          <select value={discipline} onChange={(e) => setDiscipline(e.target.value)} className={selectCls}>
            <option value="all">Tüm dersler ({scoped.length})</option>
            {disciplines.map(([d, s]) => (
              <option key={d} value={d}>
                {d} ({s.total})
              </option>
            ))}
          </select>
        </Field>

        <div className="hidden lg:flex flex-col gap-1">
          <span className="text-[13px] font-semibold text-ink-2 mb-0.5">Dersler</span>
          <button
            type="button"
            aria-pressed={discipline === 'all'}
            onClick={() => setDiscipline('all')}
            className={`flex items-center justify-between gap-2 min-h-9 px-2.5 rounded-lg text-[14px] text-left cursor-pointer ${
              discipline === 'all' ? 'bg-accent-soft text-accent font-semibold' : 'hover:bg-canvas text-ink'
            }`}
          >
            Tümü <span className="font-mono text-[12px]">{scoped.length}</span>
          </button>
          <div className="flex flex-col gap-0.5 max-h-[320px] overflow-y-auto -mr-1 pr-1">
            {disciplines.map(([d, s]) => {
              const on = discipline === d;
              return (
                <button
                  key={d}
                  type="button"
                  aria-pressed={on}
                  onClick={() => setDiscipline(d)}
                  className={`flex flex-col gap-1 px-2.5 py-1.5 rounded-lg text-left cursor-pointer ${on ? 'bg-accent-soft' : 'hover:bg-canvas'}`}
                >
                  <span className={`flex items-center justify-between gap-2 text-[14px] ${on ? 'text-accent font-semibold' : 'text-ink'}`}>
                    <span className="truncate">{d}</span>
                    <span className="font-mono text-[12px] shrink-0">
                      {s.solved}/{s.total}
                    </span>
                  </span>
                  <span className="h-1 rounded-full bg-line-soft overflow-hidden">
                    <span className="block h-1 bg-accent rounded-full" style={{ width: `${(s.solved / Math.max(1, s.total)) * 100}%` }} />
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="flex flex-col gap-1.5 border-t border-line-soft pt-3">
          <span className="text-[13px] font-semibold text-ink-2">Mod</span>
          <Segmented<Mode>
            label="Mod"
            size="sm"
            value={mode}
            onChange={setMode}
            options={[
              { value: 'all', label: 'Tümü' },
              { value: 'unsolved', label: 'Çözülmemiş' },
              { value: 'wrong', label: 'Yanlışlar' },
              { value: 'review', label: `Tekrar ${review.size}` },
            ]}
          />
          <label className="flex items-center gap-2 min-h-9 text-[14px] text-ink cursor-pointer">
            <input type="checkbox" checked={shuffled} onChange={(e) => setShuffled(e.target.checked)} className="w-4 h-4 accent-[#1E4FD8]" />
            Karışık sırala
            {shuffled && (
              <button type="button" onClick={() => setSeed((s) => s + 1)} className="ml-auto text-accent text-[13px] font-semibold inline-flex items-center gap-1 cursor-pointer">
                <Shuffle className="w-3.5 h-3.5" /> Yeniden
              </button>
            )}
          </label>
        </div>

        <div className="hidden lg:grid grid-cols-2 gap-2 border-t border-line-soft pt-3 text-[12px] text-ink-2">
          <div>
            Çözülen
            <div className="font-mono text-[18px] text-ink">{solvedInScope}</div>
          </div>
          <div>
            Doğruluk
            <div className="font-mono text-[18px] text-ink">{solvedInScope ? Math.round((correctInScope / solvedInScope) * 100) : 0}%</div>
          </div>
        </div>
        </div>
      </aside>

      {/* ---------- Question ---------- */}
      <section aria-live="polite" className="min-w-0">
        {loading && bank.length === 0 ? (
          <EmptyState title="Soru bankası yükleniyor…" body="Çıkmış sorular ve kurulan havuz soruları hazırlanıyor." />
        ) : !q ? (
          <EmptyState
            title={mode === 'review' ? 'Tekrar listen boş' : mode === 'wrong' ? 'Yanlışın yok' : mode === 'unsolved' ? 'Hepsini çözmüşsün' : 'Bu filtrede soru yok'}
            body={mode === 'review' ? 'Yanlış yaptığın ya da işaretlediğin sorular burada toplanır.' : 'Filtreleri değiştirip tekrar dene.'}
            action={
              <button type="button" onClick={() => setMode('all')} className={btnSecondary}>
                Tüm sorulara dön
              </button>
            }
          />
        ) : (
          <article className={`${cardCls} p-4 sm:p-6 flex flex-col gap-4`}>
            <header className="flex flex-wrap items-center gap-2">
              <span className="font-mono text-[13px] text-ink-2">
                {index + 1} / {list.length}
              </span>
              <span className="h-6 px-2 rounded-full bg-canvas text-ink-2 text-[12px] font-semibold inline-flex items-center">{q.discipline}</span>
              <span className="h-6 px-2 rounded-full bg-canvas text-ink-2 text-[12px] font-semibold inline-flex items-center">
                {committeeName(q.committeeId)}
                {q.year ? ` · ${q.year}` : ''}
                {q.number ? ` · S.${q.number}` : ''}
              </span>
              {answered && (
                <span
                  className={`h-6 px-2 rounded-full text-[12px] font-semibold inline-flex items-center gap-1 ${
                    attempt!.correct ? 'bg-ok-soft text-ok' : 'bg-bad-soft text-bad-text'
                  }`}
                >
                  {attempt!.correct ? <Check className="w-3 h-3" strokeWidth={3} /> : <XIcon className="w-3 h-3" strokeWidth={3} />}
                  {attempt!.correct ? 'Doğru' : 'Yanlış'}
                </span>
              )}
              <span className="flex-1" />
              <button
                type="button"
                onClick={() => setAiChatOpen(true)}
                className="h-9 px-2.5 sm:px-3 rounded-lg text-[13px] font-semibold inline-flex items-center gap-1.5 bg-accent hover:bg-accent-hover text-white shadow-xs cursor-pointer transition-all shrink-0"
                title="Yapay zeka ile bu soru hakkında canlı sohbet et"
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Yapay Zekaya Sor</span>
                <span className="sm:hidden">AI Sor</span>
              </button>
              <button
                type="button"
                onClick={toggleReview}
                aria-pressed={review.has(q.id)}
                className={`h-9 px-2.5 rounded-lg text-[13px] font-semibold inline-flex items-center gap-1.5 cursor-pointer ${
                  review.has(q.id) ? 'bg-accent-soft text-accent' : 'text-ink-2 hover:bg-canvas'
                }`}
              >
                {review.has(q.id) ? <BookmarkCheck className="w-4 h-4" /> : <Bookmark className="w-4 h-4" />}
                <span className="hidden sm:inline">{review.has(q.id) ? 'Tekrar listesinde' : 'Tekrar listesine ekle'}</span>
              </button>
              <button
                type="button"
                onClick={() => setNoteOpen((v) => !v)}
                aria-expanded={noteOpen}
                className="h-9 px-2.5 rounded-lg text-[13px] font-semibold inline-flex items-center gap-1.5 text-ink-2 hover:bg-canvas cursor-pointer"
              >
                <NotebookPen className="w-4 h-4" />
                <span className="hidden sm:inline">Not al</span>
              </button>
            </header>

            <h2 className={`m-0 font-display font-medium tracking-[-0.01em] leading-[1.35] ${q.stem.length > 220 ? 'text-[17px] sm:text-[19px]' : 'text-[19px] sm:text-[22px]'}`}>{q.stem}</h2>

            <div role="radiogroup" aria-label="Şıklar" className="flex flex-col gap-2">
              {q.options.map((o) => {
                let state: 'idle' | 'correct' | 'wrong' | 'muted' = 'idle';
                let tag: string | undefined;
                if (answered) {
                  if (o.key === q.answer) {
                    state = 'correct';
                    tag = attempt!.picked === o.key ? 'Senin cevabın' : 'Doğru cevap';
                  } else if (o.key === attempt!.picked) {
                    state = 'wrong';
                    tag = 'Senin cevabın';
                  } else state = 'muted';
                }
                return <OptionButton key={o.key} opt={o} state={state} tag={tag} disabled={answered} onClick={() => pick(o.key)} />;
              })}
            </div>

            {!answered && <p className="m-0 text-[12px] text-ink-3 hidden sm:block">Kısayol: A–E ile cevapla, ← → ile gez.</p>}

            {answered && (
              <section className={`rounded-xl px-4 py-3.5 flex flex-col gap-2.5 ${attempt!.correct ? 'bg-ok-soft' : 'bg-bad-soft'}`}>
                <div className="flex items-center justify-between gap-2">
                  <span className={`font-semibold text-[15px] ${attempt!.correct ? 'text-ok' : 'text-bad-text'}`}>
                    {attempt!.correct ? 'Doğru.' : `Doğru cevap ${q.answer}.`}
                    {!attempt!.correct && <span className="font-normal text-ink"> Soru tekrar listene eklendi.</span>}
                  </span>
                  <button type="button" onClick={retry} className="h-8 px-2 rounded-lg text-[13px] font-semibold text-ink-2 hover:bg-white/60 inline-flex items-center gap-1 cursor-pointer shrink-0">
                    <RotateCcw className="w-3.5 h-3.5" /> Yeniden çöz
                  </button>
                </div>
                <div className="bg-white/70 rounded-lg p-3">
                  <ExplanationBlock q={q} compact />
                  <div className="pt-2.5 mt-2.5 border-t border-line/25 flex items-center justify-between">
                    <button
                      type="button"
                      onClick={() => setAiChatOpen(true)}
                      className="text-[13px] font-semibold text-accent hover:text-accent-hover inline-flex items-center gap-1.5 cursor-pointer"
                    >
                      <Sparkles className="w-3.5 h-3.5" />
                      {attempt!.correct
                        ? 'Mekanizmayı ve klinik incelikleri AI ile derinleştir'
                        : 'Neden yanlış yaptım? Şıkları AI ile tartış'}
                    </button>
                  </div>
                </div>
              </section>
            )}

            {noteOpen && (
              <div className="flex flex-col gap-2 bg-canvas rounded-xl p-3">
                <label htmlFor="solve-note" className="text-[13px] font-semibold text-ink-2">
                  Bu soruya not
                </label>
                <textarea
                  id="solve-note"
                  rows={3}
                  autoFocus
                  value={noteText}
                  onChange={(e) => setNoteText(e.target.value)}
                  placeholder="İlk satır notun başlığı olur. Örn. Kurşun → kemikte birikir, FEP ve δ-ALA artar"
                  className="resize-y border border-line-2 rounded-[10px] px-3 py-2.5 text-[15px] bg-white outline-0 focus:border-accent"
                />
                <div className="flex justify-end gap-2">
                  <button type="button" onClick={() => setNoteOpen(false)} className={btnGhost}>
                    Vazgeç
                  </button>
                  <button type="button" onClick={saveNote} disabled={!noteText.trim()} className={btnPrimary}>
                    Notlarıma kaydet
                  </button>
                </div>
              </div>
            )}
            {noteSaved && <p role="status" className="m-0 text-[13px] text-ok font-semibold">Not kaydedildi. Notlarım sekmesinde bulabilirsin.</p>}

            <footer className="flex items-center justify-between gap-2 border-t border-line-soft pt-3">
              <button type="button" onClick={() => go(-1)} disabled={index === 0} className={btnSecondary}>
                <ArrowLeft className="w-4 h-4" /> Önceki
              </button>
              <div className="flex-1 mx-2 hidden sm:block h-1.5 rounded-full bg-line-soft">
                <div className="h-1.5 rounded-full bg-accent" style={{ width: `${((index + 1) / list.length) * 100}%` }} />
              </div>
              <button type="button" onClick={() => go(1)} disabled={index >= list.length - 1} className={btnPrimary}>
                Sonraki <ArrowRight className="w-4 h-4" />
              </button>
            </footer>
          </article>
        )}
      </section>

      {/* AI Live Tutor Chat Drawer */}
      <QuestionAiChatDrawer
        isOpen={aiChatOpen}
        onClose={() => setAiChatOpen(false)}
        questionContext={q ? {
          id: q.id,
          discipline: q.discipline,
          topic: q.topic,
          committeeId: q.committeeId,
          committeeName: committeeName(q.committeeId),
          year: q.year,
          number: q.number,
          stem: q.stem,
          options: q.options,
          correctAnswer: q.answer,
          explanation: q.explanation,
          userAnswer: attempt?.picked,
        } : null}
      />
    </div>
  );
};
