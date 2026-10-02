import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { BookA, GraduationCap, Search, Shuffle, Repeat2, X, RotateCcw, Play, Check, Layers, Volume2 } from 'lucide-react';
import glossaryData from '../../data/medical_glossary.json';
import { SectionLoader, SuccessCheck } from '../ui/Animations';

// ---------------------------------------------------------------------------
// Card model + spaced repetition (Leitner boxes, stored per device)
// ---------------------------------------------------------------------------
interface StudyCard {
  id: string;
  group: string;
  front: string;
  back: string;
  sub?: string; // pronunciation or source line
  pearl?: string;
}

type Grade = 'again' | 'hard' | 'good';
interface CardState {
  box: number; // 0 = learning … 5 = long-term
  due: number; // epoch ms
  seen: number;
}

const STORE_KEY = 'medsoru_flashcards_v1';
const DAY = 86_400_000;
const INTERVALS = [0, 1, 3, 7, 14, 30].map((d) => d * DAY);
const MASTERED_BOX = 4;

const readStore = (): Record<string, CardState> => {
  try {
    return JSON.parse(localStorage.getItem(STORE_KEY) || '{}');
  } catch {
    return {};
  }
};
const writeStore = (s: Record<string, CardState>) => {
  try {
    localStorage.setItem(STORE_KEY, JSON.stringify(s));
  } catch {
    /* private mode: progress lives for this session only */
  }
};

const nextState = (prev: CardState | undefined, grade: Grade, now = Date.now()): CardState => {
  const box = prev?.box ?? 0;
  const seen = (prev?.seen ?? 0) + 1;
  if (grade === 'again') return { box: 0, due: now, seen };
  if (grade === 'hard') {
    const b = Math.max(1, box);
    return { box: b, due: now + Math.max(INTERVALS[1] / 2, INTERVALS[b] / 2), seen };
  }
  const b = Math.min(5, box + 1);
  return { box: b, due: now + INTERVALS[b], seen };
};

type Status = 'new' | 'due' | 'learning' | 'mastered';
const statusOf = (s: CardState | undefined, now: number): Status => {
  if (!s) return 'new';
  if (s.due <= now) return 'due';
  return s.box >= MASTERED_BOX ? 'mastered' : 'learning';
};
const STATUS_DOT: Record<Status, string> = { new: '#C9D2DB', due: '#F59E0B', learning: '#1E4FD8', mastered: '#1F9D55' };

// ---------------------------------------------------------------------------
// Sources
// ---------------------------------------------------------------------------
const glossaryGroup = (cat: string) => {
  if (/^klinik hastalık/i.test(cat)) return 'Klinik hastalıklar';
  if (/^latin/i.test(cat)) return 'Latince & anatomi';
  return (cat.split(/\s*[\/&]\s*/)[0] || 'Diğer').trim();
};

const GLOSSARY_CARDS: StudyCard[] = (glossaryData as any[])
  .filter((g) => g?.term && g?.definition)
  .map((g) => ({
    id: `g:${g.term}`,
    group: glossaryGroup(g.category || 'Diğer'),
    front: g.term,
    back: g.definition,
    sub: g.pronunciation,
    pearl: g.clinicalPearls,
  }));

const deckGroup = (raw: string) => (raw || 'Diğer').split(/\s*(?:\/|&|,|\sve\s)\s*/)[0].trim() || 'Diğer';

const loadDeckCards = async (): Promise<StudyCard[]> => {
  const mod: any = await import('../../data/interactive_learning_decks.json');
  const decks: any[] = mod.default || mod;
  const out: StudyCard[] = [];
  decks.forEach((d) =>
    (d.slides || []).forEach((s: any) =>
      (s.flashcards || []).forEach((c: any, i: number) => {
        const front = c.front || c.question;
        const back = c.back || c.answer;
        if (!front || !back) return;
        out.push({
          id: `d:${d.id}:${s.slideNumber}:${c.id || i}`,
          group: d.shortTitle || d.title,
          front,
          back,
          sub: `${deckGroup(d.discipline)} · slayt ${s.slideNumber}`,
          pearl: c.hint,
        });
      })
    )
  );
  return out;
};

const shuffle = <T,>(a: T[]) => {
  const r = [...a];
  for (let i = r.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [r[i], r[j]] = [r[j], r[i]];
  }
  return r;
};

/** Strip **bold** markers for plain text rendering. */
const plain = (s?: string) => String(s || '').replace(/\*\*/g, '');

// ---------------------------------------------------------------------------
// Page
// ---------------------------------------------------------------------------
export const FlashcardsView: React.FC = () => {
  const [source, setSource] = useState<'terms' | 'lessons'>('terms');
  const [deckCards, setDeckCards] = useState<StudyCard[] | null>(null);
  const [group, setGroup] = useState('all');
  const [query, setQuery] = useState('');
  const [store, setStore] = useState<Record<string, CardState>>(readStore);
  const [doShuffle, setDoShuffle] = useState(true);
  const [reverse, setReverse] = useState(false);
  const [limit, setLimit] = useState(20);
  const [session, setSession] = useState<StudyCard[] | null>(null);
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    if (source === 'lessons' && !deckCards) loadDeckCards().then(setDeckCards).catch(() => setDeckCards([]));
  }, [source, deckCards]);
  useEffect(() => setGroup('all'), [source]);

  const all = source === 'terms' ? GLOSSARY_CARDS : deckCards || [];
  const groups = useMemo(() => {
    const m: Record<string, number> = {};
    all.forEach((c) => (m[c.group] = (m[c.group] || 0) + 1));
    return Object.entries(m).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'tr'));
  }, [all]);

  const inGroup = useMemo(() => all.filter((c) => group === 'all' || c.group === group), [all, group]);
  const visible = useMemo(() => {
    const q = query.trim().toLocaleLowerCase('tr-TR');
    return q ? inGroup.filter((c) => `${c.front} ${c.back}`.toLocaleLowerCase('tr-TR').includes(q)) : inGroup;
  }, [inGroup, query]);

  const counts = useMemo(() => {
    const c = { new: 0, due: 0, learning: 0, mastered: 0 } as Record<Status, number>;
    inGroup.forEach((card) => c[statusOf(store[card.id], now)]++);
    return c;
  }, [inGroup, store, now]);

  /** Due cards first, then new ones, then (if nothing left) everything. */
  const buildSession = (forceAll = false) => {
    const due = inGroup.filter((c) => statusOf(store[c.id], now) === 'due');
    const fresh = inGroup.filter((c) => statusOf(store[c.id], now) === 'new');
    let pool = forceAll ? inGroup : [...(doShuffle ? shuffle(due) : due), ...(doShuffle ? shuffle(fresh) : fresh)];
    if (!pool.length) pool = inGroup;
    if (forceAll && doShuffle) pool = shuffle(pool);
    setSession(pool.slice(0, limit > 0 ? limit : pool.length));
  };

  const grade = (card: StudyCard, g: Grade) => {
    setStore((prev) => {
      const next = { ...prev, [card.id]: nextState(prev[card.id], g) };
      writeStore(next);
      return next;
    });
  };

  if (session) {
    return (
      <StudySession
        cards={session}
        reverse={reverse}
        onGrade={grade}
        onExit={() => {
          setSession(null);
          setNow(Date.now());
        }}
        onRestart={() => {
          setNow(Date.now());
          buildSession(true);
        }}
      />
    );
  }

  const loading = source === 'lessons' && !deckCards;
  const startCount = Math.min(limit > 0 ? limit : inGroup.length, counts.due + counts.new || inGroup.length);

  return (
    <div className="w-full max-w-[880px] mx-auto flex flex-col gap-4 min-w-0">
      <div className="flex flex-col md:flex-row md:items-end gap-3">
        <div className="min-w-0 flex-1">
          <h1 className="m-0 font-display font-bold text-[28px] sm:text-[30px] leading-[1.1] tracking-[-0.03em]">Ezber kartları</h1>
          <p className="m-0 mt-1 text-[14px] text-ink-3">Kartı çevir, bildiğini işaretle. Bildiklerin giderek daha seyrek gelir.</p>
        </div>
        <div role="radiogroup" aria-label="Kaynak" className="grid grid-cols-2 gap-1 bg-white border border-line rounded-[14px] p-1 md:w-[360px]">
          {(
            [
              ['terms', BookA, `Tıbbi terimler · ${GLOSSARY_CARDS.length}`],
              ['lessons', GraduationCap, `Ders kartları${deckCards ? ` · ${deckCards.length}` : ''}`],
            ] as const
          ).map(([id, Icon, label]) => (
            <button
              key={id}
              type="button"
              role="radio"
              aria-checked={source === id}
              onClick={() => setSource(id)}
              className={`h-10 rounded-[11px] inline-flex items-center justify-center gap-1.5 text-[13.5px] cursor-pointer whitespace-nowrap ${
                source === id ? 'bg-ink text-white font-semibold' : 'text-ink-2 hover:text-ink'
              }`}
            >
              <Icon className="w-4 h-4" />
              {label}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <SectionLoader variant="book" label="Ders kartları yükleniyor…" />
      ) : (
        <>
          {/* Groups */}
          <div role="radiogroup" aria-label="Konu" className="flex gap-1.5 overflow-x-auto no-scrollbar -mx-3 px-3 sm:mx-0 sm:px-0 sm:flex-wrap">
            {[['all', all.length] as [string, number], ...groups].map(([g, n]) => {
              const on = group === g;
              return (
                <button
                  key={g}
                  type="button"
                  role="radio"
                  aria-checked={on}
                  onClick={() => setGroup(g)}
                  className={`shrink-0 h-9 px-3.5 rounded-full text-[13.5px] whitespace-nowrap cursor-pointer inline-flex items-center gap-1.5 transition-colors ${
                    on ? 'bg-ink text-white font-semibold' : 'bg-white border border-line text-ink hover:border-line-2'
                  }`}
                >
                  {g === 'all' ? 'Tümü' : g}
                  <span className={`font-mono text-[12px] ${on ? 'text-white/70' : 'text-ink-3'}`}>{n}</span>
                </button>
              );
            })}
          </div>

          {/* Start panel */}
          <section className="bg-white border border-line rounded-[20px] p-4 sm:p-5 flex flex-col gap-4">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {(
                [
                  ['due', 'Tekrar zamanı', counts.due],
                  ['new', 'Yeni', counts.new],
                  ['learning', 'Öğreniliyor', counts.learning],
                  ['mastered', 'Ezberlendi', counts.mastered],
                ] as const
              ).map(([k, label, n]) => (
                <div key={k} className="rounded-[14px] bg-canvas px-3 py-2.5 flex flex-col gap-0.5">
                  <span className="flex items-center gap-1.5 text-[12.5px] text-ink-2">
                    <span className="w-2 h-2 rounded-full" style={{ background: STATUS_DOT[k] }} />
                    {label}
                  </span>
                  <span className="font-mono text-[22px] font-semibold text-ink leading-tight">{n}</span>
                </div>
              ))}
            </div>
            {inGroup.length > 0 && (
              <div className="h-2 rounded-full bg-line-soft overflow-hidden flex" aria-hidden="true">
                <span style={{ width: `${(counts.mastered / inGroup.length) * 100}%`, background: STATUS_DOT.mastered }} />
                <span style={{ width: `${(counts.learning / inGroup.length) * 100}%`, background: STATUS_DOT.learning }} />
                <span style={{ width: `${(counts.due / inGroup.length) * 100}%`, background: STATUS_DOT.due }} />
              </div>
            )}

            <div className="flex flex-wrap items-center gap-2">
              <ToggleChip on={doShuffle} onClick={() => setDoShuffle((v) => !v)} icon={Shuffle} label="Karıştır" />
              <ToggleChip on={reverse} onClick={() => setReverse((v) => !v)} icon={Repeat2} label="Tanımdan terime" />
              <div role="radiogroup" aria-label="Kart sayısı" className="inline-grid grid-cols-4 gap-1 bg-canvas rounded-[11px] p-1 ml-auto">
                {[10, 20, 50, 0].map((n) => (
                  <button
                    key={n}
                    type="button"
                    role="radio"
                    aria-checked={limit === n}
                    onClick={() => setLimit(n)}
                    className={`h-8 px-2.5 rounded-[8px] text-[13px] cursor-pointer ${limit === n ? 'bg-white font-semibold text-ink shadow-[0_1px_3px_rgba(14,26,38,0.12)]' : 'text-ink-2'}`}
                  >
                    {n === 0 ? 'Hepsi' : n}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-2">
              <button
                type="button"
                onClick={() => buildSession(false)}
                disabled={inGroup.length === 0}
                className="flex-1 h-12 rounded-[14px] bg-accent hover:bg-accent-hover text-white text-[16px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 shadow-[0_6px_16px_rgba(30,79,216,0.25)]"
              >
                <Play className="w-4 h-4 fill-current" />
                {counts.due + counts.new > 0 ? `Çalışmaya başla · ${startCount} kart` : 'Hepsini tekrar et'}
              </button>
              {counts.due + counts.new > 0 && counts.learning + counts.mastered > 0 && (
                <button
                  type="button"
                  onClick={() => buildSession(true)}
                  className="h-12 px-4 rounded-[14px] border border-line bg-white text-[15px] font-semibold text-ink inline-flex items-center justify-center gap-2 cursor-pointer hover:border-line-2"
                >
                  <Layers className="w-4 h-4" />
                  Tüm kartlar
                </button>
              )}
            </div>
          </section>

          {/* Browse */}
          <section className="flex flex-col gap-2">
            <label className="flex items-center gap-2 h-11 px-3.5 rounded-[12px] bg-white border border-line focus-within:border-accent">
              <Search className="w-4 h-4 text-ink-3 shrink-0" />
              <span className="sr-only">Kartlarda ara</span>
              <input
                type="search"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Kartlarda ara"
                className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[16px] sm:text-[15px] placeholder:text-[#7A8693]"
              />
              <span className="text-[12.5px] text-ink-3 shrink-0">{visible.length} kart</span>
            </label>
            <BrowseList cards={visible} store={store} now={now} />
          </section>
        </>
      )}
    </div>
  );
};

const ToggleChip: React.FC<{ on: boolean; onClick: () => void; icon: React.ElementType; label: string }> = ({ on, onClick, icon: Icon, label }) => (
  <button
    type="button"
    aria-pressed={on}
    onClick={onClick}
    className={`h-9 px-3 rounded-full text-[13.5px] inline-flex items-center gap-1.5 cursor-pointer transition-colors ${
      on ? 'bg-accent-soft text-accent font-semibold ring-1 ring-inset ring-accent/40' : 'bg-white border border-line text-ink-2 hover:border-line-2'
    }`}
  >
    <Icon className="w-4 h-4" />
    {label}
  </button>
);

const BrowseList: React.FC<{ cards: StudyCard[]; store: Record<string, CardState>; now: number }> = ({ cards, store, now }) => {
  const [shown, setShown] = useState(24);
  const [open, setOpen] = useState<string | null>(null);
  useEffect(() => setShown(24), [cards]);
  if (!cards.length) return <p className="m-0 py-8 text-center text-[14px] text-ink-3">Bu aramada kart yok.</p>;
  return (
    <>
      <ul className="list-none m-0 p-0 grid grid-cols-1 sm:grid-cols-2 gap-2">
        {cards.slice(0, shown).map((c) => {
          const st = statusOf(store[c.id], now);
          const isOpen = open === c.id;
          return (
            <li key={c.id} className="min-w-0">
              <button
                type="button"
                onClick={() => setOpen(isOpen ? null : c.id)}
                aria-expanded={isOpen}
                className={`w-full text-left rounded-[14px] border bg-white px-3.5 py-3 flex flex-col gap-1 cursor-pointer transition-colors ${
                  isOpen ? 'border-accent' : 'border-line hover:border-line-2'
                }`}
              >
                <span className="flex items-center gap-2 min-w-0">
                  <span className="w-2 h-2 rounded-full shrink-0" style={{ background: STATUS_DOT[st] }} aria-hidden="true" />
                  <span className="text-[15px] font-semibold text-ink truncate">{plain(c.front)}</span>
                </span>
                <span className={`text-[13.5px] text-ink-2 leading-[1.5] ${isOpen ? '' : 'line-clamp-1'}`}>{plain(c.back)}</span>
              </button>
            </li>
          );
        })}
      </ul>
      {cards.length > shown && (
        <button
          type="button"
          onClick={() => setShown((n) => n + 48)}
          className="self-center h-10 px-4 rounded-[12px] border border-line bg-white text-[14px] font-semibold text-ink cursor-pointer hover:border-line-2"
        >
          Daha fazla göster · {cards.length - shown}
        </button>
      )}
    </>
  );
};

// ---------------------------------------------------------------------------
// Study session: flip card + again / hard / good, swipe and keyboard
// ---------------------------------------------------------------------------
const StudySession: React.FC<{
  cards: StudyCard[];
  reverse: boolean;
  onGrade: (c: StudyCard, g: Grade) => void;
  onExit: () => void;
  onRestart: () => void;
}> = ({ cards, reverse, onGrade, onExit, onRestart }) => {
  const [queue, setQueue] = useState<StudyCard[]>(cards);
  const [idx, setIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [tally, setTally] = useState({ good: 0, hard: 0, again: 0 });
  const [leaving, setLeaving] = useState<Grade | null>(null);
  const touch = useRef<{ x: number; y: number } | null>(null);

  const card = queue[idx];
  const done = !card;
  const total = cards.length;
  const answered = tally.good + tally.hard;

  const answer = useCallback(
    (g: Grade) => {
      if (!card || !flipped || leaving) return;
      onGrade(card, g);
      setTally((t) => ({ ...t, [g]: t[g] + 1 }));
      setLeaving(g);
      window.setTimeout(() => {
        // "Tekrar" cards come back at the end of this session
        if (g === 'again') setQueue((q) => [...q, card]);
        setIdx((i) => i + 1);
        setFlipped(false);
        setLeaving(null);
      }, 220);
    },
    [card, flipped, leaving, onGrade]
  );

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(t.tagName)) return;
      if (e.key === 'Escape') return onExit();
      if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        if (!done) setFlipped((f) => !f);
        return;
      }
      if (e.key === '1') answer('again');
      if (e.key === '2') answer('hard');
      if (e.key === '3') answer('good');
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [answer, done, onExit]);

  const speak = (text: string) => {
    if (!('speechSynthesis' in window)) return;
    try {
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = 'tr-TR';
      u.rate = 0.9;
      window.speechSynthesis.speak(u);
    } catch {
      /* no voice available */
    }
  };

  if (done) {
    return (
      <div className="w-full max-w-[520px] mx-auto bg-white border border-line rounded-[24px] px-6 py-10 flex flex-col items-center text-center gap-3 ms-pop-in">
        <SuccessCheck size={104} />
        <h1 className="m-0 font-display font-bold text-[26px] tracking-[-0.02em]">Oturum bitti!</h1>
        <p className="m-0 text-[15px] text-ink-2">{total} kart çalıştın. Bildiklerin bir sonraki tekrara kadar dinlenecek.</p>
        <div className="grid grid-cols-3 gap-2 w-full mt-1">
          {(
            [
              ['Biliyorum', tally.good, 'text-ok', 'bg-ok-tint'],
              ['Zor', tally.hard, 'text-warn', 'bg-warn-soft'],
              ['Tekrar', tally.again, 'text-[#B4233C]', 'bg-[#FFF1F3]'],
            ] as const
          ).map(([label, n, fg, bg]) => (
            <div key={label} className={`rounded-[14px] ${bg} py-3`}>
              <div className={`font-mono text-[22px] font-semibold ${fg}`}>{n}</div>
              <div className="text-[12.5px] text-ink-2">{label}</div>
            </div>
          ))}
        </div>
        <div className="flex gap-2 w-full mt-2">
          <button type="button" onClick={onExit} className="flex-1 h-12 rounded-[14px] border border-line bg-white text-[15px] font-semibold cursor-pointer">
            Kartlara dön
          </button>
          <button
            type="button"
            onClick={onRestart}
            className="flex-1 h-12 rounded-[14px] bg-accent hover:bg-accent-hover text-white text-[15px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer"
          >
            <RotateCcw className="w-4 h-4" />
            Yeniden çalış
          </button>
        </div>
      </div>
    );
  }

  const front = reverse ? card.back : card.front;
  const back = reverse ? card.front : card.back;
  const pct = Math.min(100, (answered / total) * 100);
  const leaveCls = leaving === 'good' ? 'translate-x-[40%] rotate-6 opacity-0' : leaving === 'again' ? '-translate-x-[40%] -rotate-6 opacity-0' : leaving === 'hard' ? 'translate-y-6 opacity-0' : '';

  return (
    <div className="w-full max-w-[640px] mx-auto flex flex-col gap-4 min-h-[calc(100dvh-220px)]">
      {/* Top bar */}
      <div className="flex items-center gap-3">
        <button type="button" onClick={onExit} aria-label="Oturumu bitir" className="w-10 h-10 -ml-1 rounded-full flex items-center justify-center text-ink-2 hover:bg-white cursor-pointer">
          <X className="w-5 h-5" />
        </button>
        <div className="flex-1 h-2 rounded-full bg-white overflow-hidden" aria-hidden="true">
          <div className="h-full rounded-full bg-accent transition-[width] duration-300" style={{ width: `${pct}%` }} />
        </div>
        <span className="font-mono text-[13px] text-ink-2 shrink-0">
          {Math.min(answered + 1, total)}/{total}
        </span>
      </div>

      {/* Card */}
      <div
        className="relative flex-1 min-h-[340px] [perspective:1400px]"
        onTouchStart={(e) => (touch.current = { x: e.touches[0].clientX, y: e.touches[0].clientY })}
        onTouchEnd={(e) => {
          if (!touch.current) return;
          const dx = e.changedTouches[0].clientX - touch.current.x;
          const dy = e.changedTouches[0].clientY - touch.current.y;
          touch.current = null;
          if (!flipped || Math.abs(dx) < 70 || Math.abs(dx) < Math.abs(dy) * 1.4) return;
          answer(dx > 0 ? 'good' : 'again');
        }}
      >
        <button
          type="button"
          onClick={() => setFlipped((f) => !f)}
          aria-label={flipped ? 'Kartın ön yüzüne dön' : 'Kartı çevir'}
          className={`absolute inset-0 w-full h-full cursor-pointer transition-all duration-500 [transform-style:preserve-3d] ${flipped ? '[transform:rotateY(180deg)]' : ''} ${leaveCls}`}
        >
          {/* Front */}
          <span
            className="absolute inset-0 rounded-[24px] bg-white border border-line shadow-[0_14px_40px_rgba(14,26,38,0.10)] [backface-visibility:hidden] flex flex-col p-5 sm:p-7 text-left"
            style={{ opacity: flipped ? 0 : 1, transition: 'opacity 0s linear 0.25s' }}
            aria-hidden={flipped}
          >
            <span className="flex items-center gap-2">
              <span className="h-6 px-2.5 rounded-full bg-accent-soft text-accent text-[12px] font-semibold inline-flex items-center max-w-[70%] truncate">{card.group}</span>
              <span className="ml-auto text-[12px] text-ink-3">{reverse ? 'Tanım' : 'Terim'}</span>
            </span>
            <span className="flex-1 flex flex-col items-center justify-center text-center gap-2 px-2">
              <span className={`font-display font-bold tracking-[-0.02em] text-ink ${reverse ? 'text-[18px] sm:text-[20px] leading-[1.45] font-medium' : 'text-[28px] sm:text-[34px] leading-[1.15]'}`}>
                {plain(front)}
              </span>
              {!reverse && card.sub && <span className="font-mono text-[13px] text-ink-3">{card.sub}</span>}
            </span>
            <span className="text-center text-[13px] text-ink-3">Çevirmek için dokun · boşluk tuşu</span>
          </span>
          {/* Back */}
          <span
            className="absolute inset-0 rounded-[24px] bg-white border border-accent/30 shadow-[0_14px_40px_rgba(30,79,216,0.14)] [backface-visibility:hidden] [transform:rotateY(180deg)] flex flex-col p-5 sm:p-7 text-left overflow-y-auto"
            style={{ opacity: flipped ? 1 : 0, transition: 'opacity 0s linear 0.25s' }}
            aria-hidden={!flipped}
          >
            <span className="flex items-center gap-2">
              <span className="text-[15px] font-semibold text-accent truncate">{plain(reverse ? card.back : card.front).slice(0, 60)}</span>
            </span>
            <span className="flex-1 flex flex-col justify-center gap-3 py-3">
              <span className={`text-ink ${reverse ? 'font-display font-bold text-[28px] leading-[1.15] text-center' : 'text-[17px] sm:text-[18px] leading-[1.6]'}`}>{plain(back)}</span>
              {card.pearl && (
                <span className="rounded-[14px] bg-[#FFF9EF] border border-[#F2DDB8] px-3.5 py-2.5 text-[14px] leading-[1.55] text-ink">
                  <span className="block text-[12px] font-semibold text-[#8A4405] mb-0.5">Akılda tut</span>
                  {plain(card.pearl)}
                </span>
              )}
            </span>
          </span>
        </button>
        {!reverse && (
          <button
            type="button"
            onClick={() => speak(plain(card.front))}
            aria-label="Terimi seslendir"
            className="absolute right-3 bottom-3 z-10 w-10 h-10 rounded-full bg-canvas text-ink-2 hover:text-accent flex items-center justify-center cursor-pointer"
          >
            <Volume2 className="w-[18px] h-[18px]" />
          </button>
        )}
      </div>

      {/* Actions */}
      {flipped ? (
        <div className="grid grid-cols-3 gap-2 ms-pop-in">
          {(
            [
              ['again', 'Tekrar', '1', 'bg-[#FFF1F3] text-[#B4233C] hover:bg-[#FFE4E9]'],
              ['hard', 'Zor', '2', 'bg-warn-soft text-warn hover:bg-[#FBE3C8]'],
              ['good', 'Biliyorum', '3', 'bg-ok text-white hover:bg-[#126A35]'],
            ] as const
          ).map(([g, label, key, cls]) => (
            <button
              key={g}
              type="button"
              onClick={() => answer(g)}
              className={`h-14 rounded-[16px] text-[15.5px] font-semibold inline-flex flex-col items-center justify-center cursor-pointer transition-colors ${cls}`}
            >
              <span className="inline-flex items-center gap-1.5">
                {g === 'good' && <Check className="w-4 h-4" strokeWidth={3} />}
                {label}
              </span>
              <span className="hidden md:block text-[11px] opacity-70 font-mono">{key}</span>
            </button>
          ))}
        </div>
      ) : (
        <button
          type="button"
          onClick={() => setFlipped(true)}
          className="h-14 rounded-[16px] bg-ink text-white text-[16px] font-semibold cursor-pointer hover:bg-[#1B2B3B]"
        >
          Cevabı göster
        </button>
      )}
      <p className="m-0 text-center text-[12.5px] text-ink-3">
        <span className="md:hidden">Çevirdikten sonra sağa kaydır: biliyorum · sola: tekrar</span>
        <span className="hidden md:inline">Boşluk: çevir · 1 tekrar · 2 zor · 3 biliyorum · Esc çık</span>
      </p>
    </div>
  );
};
