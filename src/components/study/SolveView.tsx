import React, { useEffect, useMemo, useState } from 'react';
import { CopyQuestionButton } from '../ui/CopyQuestionButton';
import { ArrowLeft, ArrowRight, Bookmark, BookmarkCheck, Star, NotebookPen, RotateCcw, Shuffle, Check, X as XIcon, SlidersHorizontal, ChevronDown, ChevronUp, Sparkles, PanelLeftClose, PanelLeftOpen } from 'lucide-react';
import { Committee } from '../../types';
import {
  StudyQuestion,
  OptionKey,
  getProgress,
  recordAttempt,
  getReview,
  setInReview,
  getFavorites,
  setFavorite,
  shuffle,
  getNotes,
  saveNotes,
  newNoteId,
  resetProgress,
} from '../../services/studyStore';
import { committeeShortLabel } from '../QuickAddHero';
import { Segmented, ExplanationBlock, EmptyState, cardCls, btnPrimary, btnSecondary, btnGhost, selectCls, Field, isTypingTarget } from './StudyUI';
import { QuestionAiChatDrawer } from '../QuestionAiChatDrawer';
import { StudyReportButton } from './StudyReportButton';

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
  const [favorites, setFavorites] = useState(getFavorites);
  const [noteOpen, setNoteOpen] = useState(false);
  const [noteText, setNoteText] = useState('');
  const [noteSaved, setNoteSaved] = useState(false);
  const [filtersOpen, setFiltersOpen] = useState(false);
  // Masaüstü filtre çekmecesi: tek tıkla kapanır, tercih cihazda saklanır.
  const [drawer, setDrawerState] = useState(() => {
    try { return localStorage.getItem('medsoru_solve_drawer') !== '0'; } catch { return true; }
  });
  const setDrawer = (open: boolean) => {
    setDrawerState(open);
    try { localStorage.setItem('medsoru_solve_drawer', open ? '1' : '0'); } catch { /* yoksay */ }
  };
  const [dersOpen, setDersOpen] = useState(true);
  const [aiChatOpen, setAiChatOpen] = useState(false);

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
    <div className={`grid grid-cols-1 ${drawer ? 'lg:grid-cols-[260px_minmax(0,1fr)]' : ''} gap-3 sm:gap-5 items-start`}>
      {/* ---------- Filters ---------- */}
      <aside aria-label="Filtreler" className={`${cardCls} p-2 lg:p-4 flex flex-col gap-3 lg:sticky lg:top-[88px] ${drawer ? '' : 'lg:hidden'} rb-anim`}>
        <div className="hidden lg:flex items-center gap-2 -mt-1 -mr-1">
          <span className="text-[15px] font-semibold">Filtreler</span>
          <span className="font-mono text-xs text-ink-3">{list.length}</span>
          <span className="flex-1" />
          <button type="button" onClick={() => setDrawer(false)} aria-label="Filtre panelini kapat" title="Filtre panelini kapat" className="w-8 h-8 rounded-lg inline-flex items-center justify-center text-ink-2 hover:bg-canvas cursor-pointer">
            <PanelLeftClose className="w-4 h-4" />
          </button>
        </div>
        <button
          type="button"
          onClick={() => setFiltersOpen((v) => !v)}
          aria-expanded={filtersOpen}
          aria-controls="solve-filters"
          className="lg:hidden min-h-10 px-2 rounded-[10px] flex items-center gap-2 text-left cursor-pointer"
        >
          <SlidersHorizontal className="w-4 h-4 text-ink-2 shrink-0" />
          <span className="flex-1 min-w-0 text-base truncate">
            <strong className="font-semibold">{committeeId === 'all' ? 'Tüm kurullar' : committeeName(committeeId)}</strong>
            <span className="text-ink-2">
              {' · '}
              {discipline === 'all' ? 'Tüm dersler' : discipline}
              {mode !== 'all' ? ` · ${mode === 'unsolved' ? 'Çözülmemiş' : mode === 'wrong' ? 'Yanlışlar' : 'Tekrar'}` : ''}
            </span>
          </span>
          <span className="font-mono text-xs text-ink-3 shrink-0">{list.length}</span>
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
          <button
            type="button"
            onClick={() => setDersOpen((v) => !v)}
            aria-expanded={dersOpen}
            className="flex items-center gap-2 min-h-8 -mx-1 px-1 rounded-md text-left cursor-pointer hover:bg-canvas"
          >
            <span className="text-xs font-semibold uppercase tracking-[0.06em] text-ink-3">Dersler</span>
            <span className="flex-1" />
            {!dersOpen && <span className="text-xs font-semibold text-accent truncate max-w-[120px]">{discipline === 'all' ? 'Tümü' : discipline}</span>}
            <ChevronDown className={`w-4 h-4 text-ink-3 transition-transform duration-200 ${dersOpen ? 'rotate-180' : ''}`} />
          </button>
          <div className={`grid transition-[grid-template-rows] duration-200 ease-out ${dersOpen ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'}`}>
          <div className="overflow-hidden flex flex-col gap-1">
          <button
            type="button"
            aria-pressed={discipline === 'all'}
            onClick={() => setDiscipline('all')}
            className={`flex items-center justify-between gap-2 min-h-9 px-2.5 rounded-lg text-base text-left cursor-pointer ${
              discipline === 'all' ? 'bg-accent-soft text-accent font-semibold' : 'hover:bg-canvas text-ink'
            }`}
          >
            Tümü <span className="font-mono text-xs">{scoped.length}</span>
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
                  <span className={`flex items-center justify-between gap-2 text-base ${on ? 'text-accent font-semibold' : 'text-ink'}`}>
                    <span className="truncate">{d}</span>
                    <span className="font-mono text-xs shrink-0">
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
          </div>
        </div>

        <div className="flex flex-col gap-1.5 border-t border-line-soft pt-3">
          <span className="text-sm font-semibold text-ink-2">Mod</span>
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
          <label className="flex items-center gap-2 min-h-9 text-base text-ink cursor-pointer">
            <input type="checkbox" checked={shuffled} onChange={(e) => setShuffled(e.target.checked)} className="w-4 h-4 accent-[#1E4FD8]" />
            Karışık sırala
            {shuffled && (
              <button type="button" onClick={() => setSeed((s) => s + 1)} className="ml-auto text-accent text-sm font-semibold inline-flex items-center gap-1 cursor-pointer">
                <Shuffle className="w-3.5 h-3.5" /> Yeniden
              </button>
            )}
          </label>
        </div>

        <div className="hidden lg:grid grid-cols-2 gap-2 border-t border-line-soft pt-3 text-xs text-ink-2">
          <div>
            Çözülen
            <div className="font-mono text-lg text-ink">{solvedInScope}</div>
          </div>
          <div>
            Doğruluk
            <div className="font-mono text-lg text-ink">{solvedInScope ? Math.round((correctInScope / solvedInScope) * 100) : 0}%</div>
          </div>
        </div>
        </div>
      </aside>

      {/* ---------- Question ---------- */}
      <section aria-live="polite" className="min-w-0">
        {!drawer && (
          <button
            type="button"
            onClick={() => setDrawer(true)}
            className="hidden lg:inline-flex items-center gap-2 h-8 px-2.5 mb-2 rounded-lg bg-accent-soft text-accent text-sm font-semibold cursor-pointer"
          >
            <PanelLeftOpen className="w-4 h-4" />
            Filtreler
            <span className="font-mono text-xs">{committeeId === 'all' ? 'Tüm kurullar' : committeeName(committeeId)} · {discipline === 'all' ? 'Tüm dersler' : discipline} · {list.length}</span>
          </button>
        )}
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
          <article data-auto-reveal className="qk is-solve">
            <header className="qk-h">
              {q.committeeId && <span className="qk-chip" title={committeeName(q.committeeId)}>{committeeName(q.committeeId).replace(/^Kurul\s*/i, 'K')}</span>}
              <span className="qk-kunye">{[q.year, q.number ? `S${q.number}` : null].filter(Boolean).join(' · ') || q.source}</span>
              {q.discipline && <span className="qk-ders">{q.discipline}</span>}
              {answered && (
                <span className="qk-flags">
                  <span className={`cx-flag ${attempt!.correct ? 'is-ok' : 'is-bad'}`}>
                    {attempt!.correct ? <Check aria-hidden /> : <XIcon aria-hidden />}{attempt!.correct ? 'Doğru' : 'Yanlış'}
                  </span>
                </span>
              )}
              <span className="qk-sp" />
              <span className="qk-pos">{index + 1}<small>/{list.length}</small></span>
              <button type="button" onClick={() => setAiChatOpen(true)} className="qk-ib" aria-label="Yapay zekâya sor" title="Yapay zekâya sor"><Sparkles aria-hidden /></button>
              <button type="button" onClick={toggleReview} aria-pressed={review.has(q.id)} className={`qk-ib ${review.has(q.id) ? 'is-on' : ''}`} aria-label={review.has(q.id) ? 'Tekrar listesinden çıkar' : 'Tekrar listesine ekle'} title={review.has(q.id) ? 'Tekrar listesinde' : 'Tekrar listesine ekle'}>
                {review.has(q.id) ? <BookmarkCheck aria-hidden /> : <Bookmark aria-hidden />}
              </button>
              <button type="button" onClick={() => setFavorites(new Set(setFavorite(q.id, !favorites.has(q.id))))} aria-pressed={favorites.has(q.id)} className={`qk-ib ${favorites.has(q.id) ? 'is-fav' : ''}`} aria-label={favorites.has(q.id) ? 'Favorilerden çıkar' : 'Favorilere ekle'} title="Favori">
                <Star fill={favorites.has(q.id) ? 'currentColor' : 'none'} aria-hidden />
              </button>
              <button type="button" onClick={() => setNoteOpen((v) => !v)} aria-expanded={noteOpen} className={`qk-ib ${noteOpen ? 'is-on' : ''}`} aria-label="Not al" title="Not al"><NotebookPen aria-hidden /></button>
              <CopyQuestionButton stem={q.stem} options={q.options} className="qk-ib" />
              <StudyReportButton q={q} compact className="qk-ib" />
            </header>

            <div className="qk-stem is-lead">{q.stem}</div>

            <ol role="radiogroup" aria-label="Şıklar" className="qk-opts">
              {q.options.map((o) => {
                const isAns = o.key === q.answer;
                const isPick = attempt?.picked === o.key;
                const cls = answered ? (isAns ? 'is-correct' : isPick ? 'is-wrong' : 'is-dim') : '';
                const tag = answered && (isAns || isPick) ? (isPick ? 'Senin cevabın' : 'Doğru cevap') : null;
                return (
                  <li key={o.key} className="qk-opt-li">
                    <button type="button" role="radio" aria-checked={isPick} disabled={answered} onClick={() => pick(o.key)} className={`qk-opt ${cls}`}>
                      <span className="qk-bub" aria-hidden>{answered && isAns ? <Check strokeWidth={3} /> : answered && isPick ? <XIcon strokeWidth={3} /> : o.key}</span>
                      <span className="qk-opt-t">{o.text}</span>
                      {tag && <span className={`qk-opt-tag ${isAns ? 'is-ok' : 'is-bad'}`}>{tag}</span>}
                    </button>
                  </li>
                );
              })}
            </ol>

            {!answered && <p className="qk-hint">Kısayol: A–E ile cevapla, ← → ile gez.</p>}

            {answered && (
              <>
                <p className={`qk-verdict ${attempt!.correct ? 'is-ok' : 'is-bad'}`} role="status">
                  <b>{attempt!.correct ? 'Doğru' : `Yanlış · doğru cevap ${q.answer}`}</b>
                  {!attempt!.correct && <span>Soru tekrar listene eklendi.</span>}
                  <span className="qk-sp" />
                  <button type="button" onClick={retry}><RotateCcw aria-hidden /> Yeniden çöz</button>
                </p>
                <div className="qk-discs">
                  <div className="qk-disc is-open">
                    <div className="qk-disc-h is-static"><NotebookPen aria-hidden /><span>Açıklama</span></div>
                    <div className="qk-disc-b"><div className="qk-disc-in">
                      <ExplanationBlock q={q} compact />
                      <button type="button" onClick={() => setAiChatOpen(true)} className="qk-link">
                        <Sparkles aria-hidden />
                        {attempt!.correct ? 'Mekanizmayı ve klinik incelikleri yapay zekâyla derinleştir' : 'Neden yanlış yaptım? Şıkları yapay zekâyla tartış'}
                      </button>
                    </div></div>
                  </div>
                </div>
              </>
            )}

            {noteOpen && (
              <div className="qk-note">
                <label htmlFor="solve-note">Bu soruya not</label>
                <textarea
                  id="solve-note"
                  rows={3}
                  autoFocus
                  value={noteText}
                  onChange={(e) => setNoteText(e.target.value)}
                  placeholder="İlk satır notun başlığı olur. Örn. Kurşun → kemikte birikir, FEP ve δ-ALA artar"
                />
                <div className="flex justify-end gap-2">
                  <button type="button" onClick={() => setNoteOpen(false)} className={btnGhost}>Vazgeç</button>
                  <button type="button" onClick={saveNote} disabled={!noteText.trim()} className={btnPrimary}>Notlarıma kaydet</button>
                </div>
              </div>
            )}
            {noteSaved && <p role="status" className="qk-hint is-ok">Not kaydedildi. Notlarım sekmesinde bulabilirsin.</p>}

            <footer className="qk-nav">
              <button type="button" onClick={() => go(-1)} disabled={index === 0} className={btnSecondary}>
                <ArrowLeft className="w-4 h-4" /> Önceki
              </button>
              <div className="qk-progress" aria-hidden><span style={{ width: `${((index + 1) / list.length) * 100}%` }} /></div>
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
