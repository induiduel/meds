import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { PageHeader } from '../ui/PageHeader';
import { BookA, GraduationCap, FileQuestion, Search, Shuffle, Repeat2, X, RotateCcw, Play, Check, Layers, Volume2, ChevronLeft, ChevronRight, ChevronDown, Star } from 'lucide-react';
import { getFavoriteCards, toggleFavoriteCard } from '../../services/studyStore';
import { GLOSSARY } from '../../data/glossary';
import { EmptySearch, SectionLoader, SuccessCheck } from '../ui/Animations';

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

const GLOSSARY_CARDS: StudyCard[] = GLOSSARY.map((g) => ({
  id: `g:${g.term}`,
  group: glossaryGroup(g.category || 'Diğer'),
  front: g.term,
  back: g.definition,
  sub: g.pronunciation,
  pearl: g.clinicalPearls,
}));

const deckGroup = (raw: string) => (raw || 'Diğer').split(/\s*(?:\/|&|,|\sve\s)\s*/)[0].trim() || 'Diğer';

const loadDeckCards = async (): Promise<StudyCard[]> => {
  const { loadAllDecks } = await import('../../data/deckStore');
  const decks: any[] = await loadAllDecks();
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
  // Göz atma süzgeci: duruma göre ya da favoriler (favoriler kaynak/konu seçiminden bağımsız)
  type View = 'all' | 'new' | 'due' | 'learning' | 'mastered' | 'fav';
  const [view, setView] = useState<View>('all');
  const [favCards, setFavCards] = useState(getFavoriteCards);
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
  const favAsCards = useMemo<StudyCard[]>(
    () => favCards.map((f) => ({ id: f.id, group: f.group || 'Favori', front: f.front, back: f.back })),
    [favCards]
  );
  const visible = useMemo(() => {
    const q = query.trim().toLocaleLowerCase('tr-TR');
    const base = view === 'fav' ? favAsCards : view === 'all' ? inGroup : inGroup.filter((c) => statusOf(store[c.id], now) === view);
    return q ? base.filter((c) => `${c.front} ${c.back}`.toLocaleLowerCase('tr-TR').includes(q)) : base;
  }, [inGroup, query, view, favAsCards, store, now]);

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
          setFavCards(getFavoriteCards());
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
    <div className="ds-page">
      <PageHeader
        title="Kartlar"
        stats={[
          { label: 'kart', value: inGroup.length.toLocaleString('tr-TR') },
          { label: 'tekrar', value: counts.due, tone: counts.due ? 'warn' : 'default' },
          { label: 'ezber', value: counts.mastered, tone: 'ok' },
        ]}
        description="Kartı çevir, bildiğini işaretle; bildiklerin giderek daha seyrek gelir."
      />

      {/* Kaynak ve konu */}
      <div className="ds-toolbar">
        <div role="radiogroup" aria-label="Kaynak" className="ds-seg">
          {(
            [
              ['terms', BookA, 'Terimler', GLOSSARY_CARDS.length],
              ['lessons', GraduationCap, 'Ders kartları', deckCards?.length],
            ] as const
          ).map(([id, Icon, label, n]) => (
            <button key={id} type="button" role="radio" aria-checked={source === id} onClick={() => setSource(id)}>
              <Icon aria-hidden />
              {label}
              {n ? <small>{n}</small> : null}
            </button>
          ))}
        </div>
        {!loading && (
          <label className="ds-select">
            <span>{source === 'terms' ? 'Konu' : 'Ders'}</span>
            <select value={group} onChange={(e) => setGroup(e.target.value)} aria-label={source === 'terms' ? 'Konu' : 'Ders'}>
              <option value="all">Tümü · {all.length}</option>
              {groups.map(([g, n]) => <option key={g} value={g}>{g} · {n}</option>)}
            </select>
            <ChevronDown aria-hidden />
          </label>
        )}
      </div>

      {loading ? (
        <SectionLoader label="Ders kartları yükleniyor…" />
      ) : (
        <>
          {/* Başlat paneli: ilerleme, ayarlar ve tek birincil eylem */}
          <section className="ds-panel ds-fc-start">
            {inGroup.length > 0 && (
              <div className="ds-meter" aria-hidden="true">
                <span style={{ width: `${(counts.mastered / inGroup.length) * 100}%`, background: 'var(--color-ok)' }} />
                <span style={{ width: `${(counts.learning / inGroup.length) * 100}%`, background: 'var(--color-accent)' }} />
                <span style={{ width: `${(counts.due / inGroup.length) * 100}%`, background: 'var(--color-warn)' }} />
              </div>
            )}
            <div className="ds-legend">
              {(
                [
                  ['due', 'tekrar', counts.due, 'var(--color-warn)'],
                  ['new', 'yeni', counts.new, 'var(--color-line-2)'],
                  ['learning', 'öğreniliyor', counts.learning, 'var(--color-accent)'],
                  ['mastered', 'ezber', counts.mastered, 'var(--color-ok)'],
                ] as const
              ).map(([k, label, n, c]) => (
                <span key={k}>
                  <i style={{ background: c }} />
                  <b>{n}</b> {label}
                </span>
              ))}
            </div>
            <div className="ds-fc-row">
              <ToggleChip on={doShuffle} onClick={() => setDoShuffle((v) => !v)} icon={Shuffle} label="Karıştır" />
              <ToggleChip on={reverse} onClick={() => setReverse((v) => !v)} icon={Repeat2} label="Ters çevir" />
              <div role="radiogroup" aria-label="Kart sayısı" className="ds-seg is-compact">
                {[10, 20, 50, 0].map((n) => (
                  <button key={n} type="button" role="radio" aria-checked={limit === n} onClick={() => setLimit(n)}>
                    {n === 0 ? 'Hepsi' : n}
                  </button>
                ))}
              </div>
              <span className="ds-grow" />
              {counts.due + counts.new > 0 && counts.learning + counts.mastered > 0 && (
                <button type="button" onClick={() => buildSession(true)} className="ms-btn is-ghost">
                  <Layers aria-hidden /> Tüm kartlar
                </button>
              )}
              <button type="button" onClick={() => buildSession(false)} disabled={inGroup.length === 0} className="ms-btn is-primary">
                <Play className="fill-current" aria-hidden />
                {counts.due + counts.new > 0 ? `Başla · ${startCount} kart` : 'Hepsini tekrar et'}
              </button>
            </div>
          </section>

          {/* Göz at: durum ve favori süzgeci */}
          <section className="ds-section">
            <div className="ds-tabrail">
              <div role="tablist" aria-label="Kart süzgeci" className="cx-tabs">
                {(
                  [
                    ['all', 'Tümü', inGroup.length],
                    ['due', 'Tekrar', counts.due],
                    ['new', 'Yeni', counts.new],
                    ['learning', 'Öğreniliyor', counts.learning],
                    ['mastered', 'Ezber', counts.mastered],
                    ['fav', 'Favoriler', favCards.length],
                  ] as const
                ).map(([id, label, n]) => (
                  <button key={id} type="button" role="tab" aria-selected={view === id} onClick={() => setView(id)} className={`cx-tab ${view === id ? 'is-on' : ''} ${n ? '' : 'is-zero'}`}>
                    {label} <small>{n}</small>
                  </button>
                ))}
              </div>
              {view !== 'all' && visible.length > 0 && (
                <button
                  type="button"
                  onClick={() => setSession(doShuffle ? shuffle(visible) : visible)}
                  className="ms-btn is-tonal is-sm"
                  title="Yalnızca bu süzgeçteki kartları çalış"
                >
                  <Play className="fill-current" aria-hidden /> Bunları çalış
                </button>
              )}
            </div>
            <label className="cx-search">
              <Search aria-hidden />
              <span className="sr-only">Kartlarda ara</span>
              <input type="search" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Terim ya da tanım ara" />
              <span className="ds-count">{visible.length} kart</span>
            </label>
            <BrowseList cards={visible} store={store} now={now} />
          </section>
        </>
      )}
    </div>
  );
};

const ToggleChip: React.FC<{ on: boolean; onClick: () => void; icon: React.ElementType; label: string }> = ({ on, onClick, icon: Icon, label }) => (
  <button type="button" aria-pressed={on} onClick={onClick} className={`ms-btn ${on ? 'is-tonal' : 'is-outline'}`}>
    <Icon aria-hidden />
    {label}
  </button>
);

const STATUS_LABEL: Record<Status, string> = { new: 'Yeni', due: 'Tekrar', learning: 'Öğreniliyor', mastered: 'Ezber' };
const STATUS_TONE: Record<Status, string> = { new: '', due: 'is-warn', learning: 'is-new', mastered: 'is-ok' };

const BrowseList: React.FC<{ cards: StudyCard[]; store: Record<string, CardState>; now: number }> = ({ cards, store, now }) => {
  const [shown, setShown] = useState(24);
  const [open, setOpen] = useState<string | null>(null);
  useEffect(() => setShown(24), [cards]);
  if (!cards.length)
    return (
      <div className="ds-empty">
        <EmptySearch size={56} />
        <b>Bu aramada kart yok</b>
        <span>Başka bir kelime dene ya da süzgeci “Tümü” yap.</span>
      </div>
    );
  return (
    <>
      <ul className="ds-list">
        {cards.slice(0, shown).map((c) => {
          const st = statusOf(store[c.id], now);
          const isOpen = open === c.id;
          return (
            <li key={c.id}>
              <button type="button" onClick={() => setOpen(isOpen ? null : c.id)} aria-expanded={isOpen} className={`ds-row ${isOpen ? 'is-open' : ''}`}>
                <span className="ds-row-t">
                  <b>{plain(c.front)}</b>
                  <span className={isOpen ? '' : 'line-clamp-1'}>{plain(c.back)}</span>
                </span>
                <span className={`ms-tag ${STATUS_TONE[st]}`}>{STATUS_LABEL[st]}</span>
                <ChevronDown className={`ds-row-chev ${isOpen ? 'is-open' : ''}`} aria-hidden />
              </button>
            </li>
          );
        })}
      </ul>
      {cards.length > shown && (
        <button type="button" onClick={() => setShown((n) => n + 48)} className="ms-btn is-outline ds-more">
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
  const [favIds, setFavIds] = useState(() => new Set(getFavoriteCards().map((c) => c.id)));
  const touch = useRef<{ x: number; y: number } | null>(null);

  // İleri/geri: puan vermeden kartlar arasında gezinme
  const goPrev = useCallback(() => {
    if (leaving) return;
    setIdx((i) => Math.max(0, i - 1));
    setFlipped(false);
  }, [leaving]);
  const goNext = useCallback(() => {
    if (leaving) return;
    setIdx((i) => Math.min(queue.length, i + 1));
    setFlipped(false);
  }, [leaving, queue.length]);
  const toggleFav = useCallback((c: StudyCard) => {
    const next = toggleFavoriteCard({ id: c.id, front: plain(c.front), back: plain(c.back), group: c.group });
    setFavIds(new Set(next.map((x) => x.id)));
  }, []);

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
      if (e.key === 'ArrowLeft') return goPrev();
      if (e.key === 'ArrowRight') return goNext();
      if ((e.key === 'f' || e.key === 'F') && card) return toggleFav(card);
      if (e.key === '1') answer('again');
      if (e.key === '2') answer('hard');
      if (e.key === '3') answer('good');
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [answer, done, onExit, goPrev, goNext, toggleFav, card]);

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
      <div className="ds-panel ds-fc-done ms-pop-in">
        <SuccessCheck size={72} />
        <h1 className="m-0 font-display font-bold text-xl tracking-[-0.02em]">Oturum bitti</h1>
        <p className="m-0 text-base text-ink-2">{total} kart çalıştın. Bildiklerin bir sonraki tekrara kadar dinlenecek.</p>
        <div className="grid grid-cols-3 gap-2 w-full mt-1">
          {(
            [
              ['Biliyorum', tally.good, 'text-ok', 'bg-ok-soft'],
              ['Zor', tally.hard, 'text-warn', 'bg-warn-soft'],
              ['Tekrar', tally.again, 'text-bad-text', 'bg-bad-soft'],
            ] as const
          ).map(([label, n, fg, bg]) => (
            <div key={label} className={`rounded-lg ${bg} py-2`}>
              <div className={`font-mono text-lg font-semibold ${fg}`}>{n}</div>
              <div className="text-sm text-ink-2">{label}</div>
            </div>
          ))}
        </div>
        <div className="flex gap-2 w-full mt-2">
          <button type="button" onClick={onExit} className="ms-btn is-outline flex-1">
            Kartlara dön
          </button>
          <button
            type="button"
            onClick={onRestart}
            className="ms-btn is-primary flex-1"
          >
            <RotateCcw aria-hidden />
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
    <div className="ds-fc-session">
      {/* Top bar */}
      <div className="flex items-center gap-3">
        <button type="button" onClick={onExit} aria-label="Oturumu bitir" className="ms-btn is-icon is-ghost">
          <X className="w-5 h-5" />
        </button>
        <div className="flex-1 h-1.5 rounded-full bg-line overflow-hidden" aria-hidden="true">
          <div className="h-full rounded-full bg-accent transition-[width] duration-300" style={{ width: `${pct}%` }} />
        </div>
        <div className="flex items-center gap-0.5 shrink-0">
          <button type="button" onClick={goPrev} disabled={idx === 0} aria-label="Önceki kart" className="ms-btn is-icon is-ghost">
            <ChevronLeft className="w-5 h-5" />
          </button>
          <span className="font-mono text-sm text-ink-2 min-w-[3.5ch] text-center tabular-nums">
            {Math.min(idx + 1, queue.length)}/{queue.length}
          </span>
          <button type="button" onClick={goNext} aria-label="Sonraki kart" className="ms-btn is-icon is-ghost">
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Card */}
      <div
        className="relative flex-1 min-h-[300px] [perspective:1400px]"
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
            className="ds-flip-face absolute inset-0 [backface-visibility:hidden] flex flex-col text-left"
            style={{ opacity: flipped ? 0 : 1, transition: 'opacity 0s linear 0.25s' }}
            aria-hidden={flipped}
          >
            <span className="flex items-center gap-2">
              <span className="ms-tag is-new max-w-[70%] truncate">{card.group}</span>
              <span className="ml-auto mr-12 text-xs text-ink-3">{card.id.startsWith('q:') ? (reverse ? 'Cevap' : 'Soru') : reverse ? 'Tanım' : 'Terim'}</span>
            </span>
            <span className="flex-1 flex flex-col items-center justify-center text-center gap-2 px-2">
              <span className={`font-display font-bold tracking-[-0.02em] text-ink whitespace-pre-line ${reverse || plain(front).length > 60 ? 'text-lg sm:text-xl leading-[1.45] font-medium' : 'text-2xl sm:text-3xl leading-[1.18]'} ${plain(front).length > 60 ? 'self-stretch text-left' : ''}`}>
                {plain(front)}
              </span>
              {!reverse && card.sub && <span className="font-mono text-sm text-ink-3">{card.sub}</span>}
            </span>
            <span className="text-center text-xs text-ink-3">Çevirmek için dokun · boşluk tuşu</span>
          </span>
          {/* Back */}
          <span
            className="ds-flip-face is-back absolute inset-0 [backface-visibility:hidden] [transform:rotateY(180deg)] flex flex-col text-left overflow-y-auto"
            style={{ opacity: flipped ? 1 : 0, transition: 'opacity 0s linear 0.25s' }}
            aria-hidden={!flipped}
          >
            <span className="flex items-center gap-2">
              <span className="text-md font-semibold text-accent truncate pr-12">{plain(reverse ? card.back : card.front).slice(0, 60)}</span>
            </span>
            <span className="flex-1 flex flex-col justify-center gap-3 py-3">
              <span className={`text-ink ${reverse ? 'font-display font-bold text-3xl leading-[1.15] text-center' : 'text-md sm:text-md leading-[1.6]'}`}>{plain(back)}</span>
              {card.pearl && (
                <span className="ds-callout is-important">
                  <b>Akılda tut</b>
                  {plain(card.pearl)}
                </span>
              )}
            </span>
          </span>
        </button>
        <button
          type="button"
          onClick={() => toggleFav(card)}
          aria-pressed={favIds.has(card.id)}
          aria-label={favIds.has(card.id) ? 'Favorilerden çıkar' : 'Favorilere ekle'}
          className={`ms-btn is-icon absolute right-2.5 top-2.5 z-10 ${favIds.has(card.id) ? 'is-fav' : 'is-ghost'}`}
        >
          <Star className="w-[18px] h-[18px]" fill={favIds.has(card.id) ? 'currentColor' : 'none'} />
        </button>
        {!reverse && (
          <button
            type="button"
            onClick={() => speak(plain(card.front))}
            aria-label="Terimi seslendir"
            className="ms-btn is-icon is-ghost absolute right-2.5 bottom-2.5 z-10"
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
              ['again', 'Tekrar', '1', 'is-again'],
              ['hard', 'Zor', '2', 'is-hard'],
              ['good', 'Biliyorum', '3', 'is-good'],
            ] as const
          ).map(([g, label, key, cls]) => (
            <button
              key={g}
              type="button"
              onClick={() => answer(g)}
              className={`ds-grade ${cls}`}
            >
              <span className="inline-flex items-center gap-1.5">
                {g === 'good' && <Check className="w-4 h-4" strokeWidth={3} />}
                {label}
              </span>
              <span className="hidden md:block text-2xs opacity-70 font-mono">{key}</span>
            </button>
          ))}
        </div>
      ) : (
        <button
          type="button"
          onClick={() => setFlipped(true)}
          className="ds-grade is-reveal"
        >
          Cevabı göster
        </button>
      )}
      <p className="m-0 text-center text-sm text-ink-3">
        <span className="md:hidden">Çevirdikten sonra sağa kaydır: biliyorum · sola: tekrar</span>
        <span className="hidden md:inline">Boşluk: çevir · ← → gezin · F favori · 1 tekrar · 2 zor · 3 biliyorum</span>
      </p>
    </div>
  );
};
