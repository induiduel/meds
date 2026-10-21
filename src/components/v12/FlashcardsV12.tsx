import React, { startTransition, useCallback, useEffect, useRef, useState } from 'react';
import {
  AlertCircle, ChevronDown, ChevronLeft, ChevronRight, Layers, Play, Repeat2, RotateCcw, Search, Share2, Shuffle,
  SlidersHorizontal, Star, Volume2, X,
} from 'lucide-react';
import type { Grade, Status, StudyCard } from '../flashcards/FlashcardsView';
import type { FcDeck } from '../flashcards/FlashcardStudy';
import { CardExtras } from '../flashcards/CardExtras';
import { getFavoriteCards, toggleFavoriteCard } from '../../services/studyStore';
import { speak } from '../../utils/tts';
import { linkClick, navigateTo, pathFor } from '../../router';
import '../../styles/v12/cards.css';

/**
 * Ezber kartları — v12 "Net" (canvas Cards.dc.html, "Kartlar" görünümü).
 * Yerleşim tek orta sütun (≤720): Kartlar|Spotlar gezinmesi · kaynak + deste hapları · "n / N bugün" çubuğu ·
 * çevrilen kart (ön yüz; açılınca saç çizgisinin altında arka yüz) · puan düğmeleri · klavye ipuçları · kompakt "Göz at".
 * Aralıklı tekrar mantığı ve kayıt (medsoru_flashcards_v1) FlashcardsView'dadır; bu bileşen yalnız gösterir ve
 * aynı onGrade / intervalLabel işlevlerini çağırır. Puan türleri mevcut motorla aynı: Tekrar / Zor / İyi.
 */

const plain = (s?: string) => String(s || '').replace(/\*\*/g, '');
const fmt = (n: number) => n.toLocaleString('tr-TR');

type View = 'all' | 'new' | 'due' | 'learning' | 'mastered' | 'fav';

export interface FlashcardsV12Props {
  source: 'terms' | 'lessons';
  onSource: (s: 'terms' | 'lessons') => void;
  sourceCounts: { terms: number; lessons?: number };
  decks: FcDeck[];
  group: string;
  onPickDeck: (id: string) => void;
  loading: boolean;
  groupTotal: number;
  counts: Record<Status, number>;
  struggling: StudyCard[];
  session: StudyCard[] | null;
  onStart: (forceAll: boolean) => void;
  onStudyCards: (cards: StudyCard[]) => void;
  startCount: number;
  limit: number;
  onLimit: (n: number) => void;
  doShuffle: boolean;
  onShuffle: (v: boolean) => void;
  reverse: boolean;
  onReverse: (v: boolean) => void;
  onGrade: (c: StudyCard, g: Grade) => void;
  intervalLabel: (c: { id: string }, g: Grade) => string;
  onExit: () => void;
  onShare: (c: StudyCard) => void;
  onReport: (c: StudyCard) => void;
  visible: StudyCard[];
  view: View;
  onView: (v: View) => void;
  query: string;
  onQuery: (q: string) => void;
  statusFor: (id: string) => Status;
  favCount: number;
  reportDialog: React.ReactNode;
}

/** Kartlar | Spotlar — iki ayrı rota, tek gezinme (canvas üst segmenti) */
export const CardsSpotsNav: React.FC<{ active: 'cards' | 'spots' }> = ({ active }) => (
  <nav className="f12-seg" aria-label="Kartlar ve spotlar">
    {(
      [
        ['cards', 'Kartlar', pathFor('flashcards')],
        ['spots', 'Spotlar', pathFor('spots')],
      ] as const
    ).map(([id, label, href]) => (
      <a key={id} href={href} className={active === id ? 'on' : ''} aria-current={active === id ? 'page' : undefined}
        onClick={linkClick(() => navigateTo(href))}>
        {label}
      </a>
    ))}
  </nav>
);

export const FlashcardsV12: React.FC<FlashcardsV12Props> = (p) => {
  const [settingsOpen, setSettingsOpen] = useState(false);
  const autoStarted = useRef(false);

  // Canvas: sayfa açılınca bugünkü kart doğrudan görünür. Yalnız ilk yüklemede ve bekleyen kart varsa başlar;
  // oturum bitince ya da çıkınca başlangıç paneli kalır (kendiliğinden yeniden başlamaz).
  useEffect(() => {
    if (autoStarted.current || p.loading || p.session) return;
    if (!p.groupTotal) return;
    autoStarted.current = true;
    if (p.counts.due + p.counts.new > 0) p.onStart(false);
  }, [p.loading, p.session, p.groupTotal, p.counts.due, p.counts.new, p.onStart]);

  const pending = p.counts.due + p.counts.new;
  const allDeck = p.decks[0];
  const topDecks = p.decks.slice(1).slice().sort((a, b) => b.due - a.due || b.total - a.total).slice(0, 4);
  const activeInTop = p.group === 'all' || topDecks.some((d) => d.id === p.group);
  const activeDeck = p.decks.find((d) => d.id === p.group);

  return (
    <div className="f12-page">
      <h1 className="sr-only">Ezber kartları</h1>
      <div className={`f12-col${p.loading ? '' : ' has-browse'}`}>
        <div className="f12-head">
          <CardsSpotsNav active="cards" />
          <span className="f12-grow" />
          <div className="f12-seg" role="radiogroup" aria-label="Kaynak">
            {(
              [
                ['terms', 'Terimler', p.sourceCounts.terms],
                ['lessons', 'Ders kartları', p.sourceCounts.lessons],
              ] as const
            ).map(([id, label, n]) => (
              <button key={id} type="button" role="radio" aria-checked={p.source === id} className={p.source === id ? 'on' : ''}
                onClick={() => p.source !== id && p.onSource(id)}>
                {label}
                {n ? <span className="f12-num f12-dim">{fmt(n)}</span> : null}
              </button>
            ))}
          </div>
        </div>

        {/* Deste hapları: tümü + en çok tekrar bekleyen 4 deste; tamamı seçim kutusunda */}
        <div className="f12-decks" role="group" aria-label="Deste">
          {p.loading ? (
            Array.from({ length: 4 }, (_, i) => <span key={i} className="f12-skel f12-pill-skel" aria-hidden />)
          ) : (
            <>
              {allDeck && (
                <DeckPill d={{ ...allDeck, label: 'Vadesi gelenler' }} on={p.group === 'all'} onPick={p.onPickDeck} />
              )}
              {topDecks.map((d) => <DeckPill key={d.id} d={d} on={p.group === d.id} onPick={p.onPickDeck} />)}
              {!activeInTop && activeDeck && <DeckPill d={activeDeck} on onPick={p.onPickDeck} />}
            </>
          )}
          <span className="f12-grow" />
          {!p.loading && p.decks.length > 1 && (
            <label className="f12-field f12-deck-sel">
              <span className="f12-sr">{p.source === 'terms' ? 'Konu seç' : 'Deste seç'}</span>
              <select value={p.group} onChange={(e) => p.onPickDeck(e.target.value)}>
                {p.decks.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.id === 'all' ? (p.source === 'terms' ? 'Tüm konular' : 'Tüm desteler') : d.label}
                    {d.due ? ` · ${fmt(d.due)} tekrar` : ''} · {fmt(d.total)}
                  </option>
                ))}
              </select>
              <ChevronDown aria-hidden className="f12-ico" />
            </label>
          )}
          <button type="button" className="f12-btn icon sm ghost" aria-label="Oturum ayarları" aria-expanded={settingsOpen}
            aria-controls="f12-settings" onClick={() => setSettingsOpen((v) => !v)} title="Oturum ayarları">
            <SlidersHorizontal aria-hidden />
          </button>
        </div>

        {settingsOpen && (
          <div className="f12-panel f12-settings" id="f12-settings">
            <span className="f12-meta">Kart sayısı</span>
            <div className="f12-seg" role="radiogroup" aria-label="Kart sayısı">
              {[10, 20, 50, 0].map((n) => (
                <button key={n} type="button" role="radio" aria-checked={p.limit === n} className={p.limit === n ? 'on' : ''} onClick={() => p.onLimit(n)}>
                  {n === 0 ? 'Hepsi' : n}
                </button>
              ))}
            </div>
            <button type="button" className={`f12-pill${p.doShuffle ? ' on' : ''}`} aria-pressed={p.doShuffle} onClick={() => p.onShuffle(!p.doShuffle)}>
              <Shuffle aria-hidden className="f12-ico" /><span>Karıştır</span>
            </button>
            <button type="button" className={`f12-pill${p.reverse ? ' on' : ''}`} aria-pressed={p.reverse} onClick={() => p.onReverse(!p.reverse)}>
              <Repeat2 aria-hidden className="f12-ico" /><span>Ters çevir</span>
            </button>
            <span className="f12-meta f12-settings-n">Yeni oturumda geçerli olur</span>
          </div>
        )}

        {p.loading ? (
          <div className="f12-panel f12-card f12-card-skel" aria-busy="true" aria-label="Ders kartları yükleniyor">
            <span className="f12-skel" style={{ width: '40%', height: 12 }} />
            <span className="f12-skel" style={{ width: '90%', height: 18 }} />
            <span className="f12-skel" style={{ width: '70%', height: 18 }} />
          </div>
        ) : p.session ? (
          <StudyV12
            cards={p.session}
            reverse={p.reverse}
            onGrade={p.onGrade}
            intervalLabel={p.intervalLabel}
            onExit={p.onExit}
            onRestart={() => p.onStart(true)}
            onShare={p.onShare}
            onReport={p.onReport}
          />
        ) : (
          <section className="f12-panel f12-start" aria-label="Bugünkü oturum">
            <div className="f12-start-t">
              <h2 className="f12-h2">{pending > 0 ? `Bugün ${fmt(pending)} kart seni bekliyor` : 'Bugünlük hepsi tamam'}</h2>
              <p className="f12-meta">
                <span className="f12-num">{fmt(p.counts.due)}</span> tekrar · <span className="f12-num">{fmt(p.counts.new)}</span> yeni ·{' '}
                <span className="f12-num">{fmt(p.counts.learning)}</span> öğreniliyor · <span className="f12-num">{fmt(p.counts.mastered)}</span> ezber
              </p>
            </div>
            <div className="f12-start-a">
              <button type="button" className="f12-btn pri lg" onClick={() => p.onStart(false)} disabled={p.groupTotal === 0}>
                <Play aria-hidden />
                {pending > 0 ? `Başla · ${fmt(p.startCount)} kart` : 'Hepsini tekrar et'}
              </button>
              {pending > 0 && p.counts.learning + p.counts.mastered > 0 && (
                <button type="button" className="f12-btn" onClick={() => p.onStart(true)}>
                  <Layers aria-hidden /> Tüm kartlar
                </button>
              )}
              {p.struggling.length > 0 && (
                <button type="button" className="f12-btn" onClick={() => p.onStudyCards(p.struggling)} title="En az iki kez görülüp hâlâ ilk kutularda kalan kartlar">
                  Zorlanılan <span className="f12-num">{fmt(p.struggling.length)}</span>
                </button>
              )}
            </div>
          </section>
        )}

        <BrowseV12 {...p} />
      </div>
      {p.reportDialog}
    </div>
  );
};

const DeckPill: React.FC<{ d: FcDeck; on: boolean; onPick: (id: string) => void }> = ({ d, on, onPick }) => (
  <button type="button" className={`f12-pill${on ? ' on' : ''}`} aria-pressed={on} onClick={() => onPick(d.id)}
    title={`${d.label} · ${fmt(d.due)} tekrar bekliyor · ${fmt(d.total)} kart`}>
    <span>{d.label}</span>
    <b aria-label={`${fmt(d.due)} tekrar bekliyor`}>{fmt(d.due)}</b>
  </button>
);

// ---------------------------------------------------------------------------
// Çalışma oturumu (kuyruk/çevirme durumu; puanlama üst bileşende)
// ---------------------------------------------------------------------------
const GRADES: [Grade, string, string, string][] = [
  ['again', 'Tekrar', '1', 'is-again'],
  ['hard', 'Zor', '2', 'is-hard'],
  ['good', 'İyi', '3', 'is-good'],
];

const StudyV12: React.FC<{
  cards: StudyCard[];
  reverse: boolean;
  onGrade: (c: StudyCard, g: Grade) => void;
  intervalLabel: (c: { id: string }, g: Grade) => string;
  onExit: () => void;
  onRestart: () => void;
  onShare: (c: StudyCard) => void;
  onReport: (c: StudyCard) => void;
}> = ({ cards, reverse, onGrade, intervalLabel, onExit, onRestart, onShare, onReport }) => {
  const [queue, setQueue] = useState<StudyCard[]>(cards);
  const [idx, setIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [tally, setTally] = useState({ good: 0, hard: 0, again: 0 });
  const [leaving, setLeaving] = useState<Grade | null>(null);
  const [favIds, setFavIds] = useState(() => new Set(getFavoriteCards().map((c) => c.id)));
  const touch = useRef<{ x: number; y: number } | null>(null);

  useEffect(() => {
    setQueue(cards);
    setIdx(0);
    setFlipped(false);
    setTally({ good: 0, hard: 0, again: 0 });
  }, [cards]);

  const card = queue[idx];
  const done = !card;
  const total = cards.length;
  const answered = tally.good + tally.hard;

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

  const answer = useCallback(
    (g: Grade) => {
      if (!card || !flipped || leaving) return;
      onGrade(card, g);
      setTally((t) => ({ ...t, [g]: t[g] + 1 }));
      setLeaving(g);
      window.setTimeout(() => {
        // "Tekrar" verilen kart bu oturumun sonunda yeniden gelir
        if (g === 'again') setQueue((q) => [...q, card]);
        setIdx((i) => i + 1);
        setFlipped(false);
        setLeaving(null);
      }, 180);
    },
    [card, flipped, leaving, onGrade]
  );

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(t.tagName) || t.isContentEditable) return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (document.querySelector('.cf-root, [role="dialog"][aria-modal="true"]')) return;
      if (e.key === 'Escape') return onExit();
      if (e.key === ' ' || e.key === 'Enter') {
        if (t.tagName === 'BUTTON' && !t.closest('.f12-card')) return;
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

  if (done) {
    return (
      <section className="f12-panel f12-done" aria-label="Oturum bitti">
        <h2 className="f12-h2">Oturum bitti</h2>
        <p className="f12-meta">{fmt(total)} kart çalıştın. Bildiklerin bir sonraki tekrara kadar dinlenecek.</p>
        <dl className="f12-done-n">
          {(
            [
              ['İyi', tally.good, 'ok'],
              ['Zor', tally.hard, 'warn'],
              ['Tekrar', tally.again, 'bad'],
            ] as const
          ).map(([label, n, tone]) => (
            <div key={label} className={`f12-done-i is-${tone}`}>
              <dt>{label}</dt>
              <dd className="f12-num">{fmt(n)}</dd>
            </div>
          ))}
        </dl>
        <div className="f12-start-a">
          <button type="button" className="f12-btn" onClick={onExit}>Kartlara dön</button>
          <button type="button" className="f12-btn pri" onClick={onRestart}><RotateCcw aria-hidden /> Yeniden çalış</button>
        </div>
      </section>
    );
  }

  const front = reverse ? card.back : card.front;
  const back = reverse ? card.front : card.back;
  const pct = Math.min(100, (answered / Math.max(total, 1)) * 100);
  const isFav = favIds.has(card.id);
  const answerId = `f12-ans-${idx}`;
  const remaining = Math.max(0, queue.length - idx);
  const speakCard = () => {
    const parts = [plain(front)];
    if (flipped) parts.push(plain(back), card.pearl ? `Akılda tut: ${plain(card.pearl)}` : '');
    speak(parts.filter(Boolean).join('. '));
  };

  return (
    <>
      <div className="f12-prog">
        <span className="f12-meta"><span className="f12-num f12-ink">{fmt(answered)} / {fmt(total)}</span> bugün</span>
        <span className="f12-bar" role="progressbar" aria-valuenow={answered} aria-valuemin={0} aria-valuemax={total} aria-label="Bugünkü ilerleme">
          <i style={{ width: `${pct}%` }} />
        </span>
        <span className="f12-meta">kalan <span className="f12-num">{fmt(remaining)}</span></span>
      </div>

      {/* Kart: her yerine dokunmak çevirir; erişilebilir eylem aşağıdaki "Cevabı göster" düğmesi ve Space */}
      <section
        id={`card-${card.id}`}
        aria-label="Kart"
        className={`f12-panel f12-card${flipped ? ' is-open' : ''}${leaving ? ` is-leave is-leave-${leaving}` : ''}`}
        onClick={(e) => {
          if ((e.target as HTMLElement).closest('button, a, textarea, input, select')) return;
          setFlipped((f) => !f);
        }}
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
        <div className="f12-face">
          <div className="f12-cap">
            <span className="f12-meta f12-grow f12-clamp1">{reverse ? 'Ters yön · ' : ''}{card.group || 'Ezber kartları'}{!reverse && card.sub ? ` · ${card.sub}` : ''}</span>
            <span className="f12-badge">Ön yüz</span>
          </div>
          <p className="f12-q">{plain(front)}</p>
        </div>
        {flipped ? (
          <>
            <hr className="f12-sep" />
            <div className="f12-face f12-face-b" id={answerId}>
              <div className="f12-cap">
                <span className="f12-meta f12-grow">Cevap</span>
                <span className="f12-badge ok">Arka yüz</span>
              </div>
              <p className="f12-a">{plain(back)}</p>
              {card.pearl && (
                <p className="f12-pearl"><b>Akılda tut</b> {plain(card.pearl)}</p>
              )}
            </div>
          </>
        ) : (
          <div className="f12-face f12-face-hint">
            <span className="f12-meta">Cevabı görmek için karta dokun ya da <kbd className="f12-kbd">Space</kbd></span>
          </div>
        )}
      </section>

      {flipped ? (
        <div className="f12-ans" role="group" aria-label="Ne kadar iyi hatırladın?">
          {GRADES.map(([g, label, key, cls]) => (
            <button key={g} type="button" className={cls} onClick={() => answer(g)} aria-keyshortcuts={key}>
              <kbd className="f12-kbd" aria-hidden>{key}</kbd>
              <span className="f12-ans-t">{label}</span>
              <span className="f12-ans-iv">{intervalLabel(card, g)}</span>
            </button>
          ))}
        </div>
      ) : (
        <button type="button" className="f12-btn pri f12-reveal" onClick={() => setFlipped(true)} aria-expanded={false} aria-controls={answerId} aria-keyshortcuts="Space">
          Cevabı göster
        </button>
      )}

      <div className="f12-tools" role="group" aria-label="Kart araçları">
        <button type="button" className="f12-btn icon sm ghost" onClick={goPrev} disabled={idx === 0} aria-label="Önceki kart" title="Önceki (←)"><ChevronLeft aria-hidden /></button>
        <button type="button" className="f12-btn icon sm ghost" onClick={goNext} aria-label="Sonraki kart" title="Sonraki (→)"><ChevronRight aria-hidden /></button>
        <span className="f12-tools-sep" aria-hidden />
        <button type="button" className={`f12-btn icon sm ghost${isFav ? ' is-fav' : ''}`} onClick={() => toggleFav(card)} aria-pressed={isFav}
          aria-label={isFav ? 'Favorilerden çıkar' : 'Favorilere ekle'} title="Favori (F)">
          <Star fill={isFav ? 'currentColor' : 'none'} aria-hidden />
        </button>
        <button type="button" className="f12-btn icon sm ghost" onClick={speakCard} aria-label={flipped ? 'Kartı seslendir' : 'Soruyu seslendir'} title="Seslendir"><Volume2 aria-hidden /></button>
        <button type="button" className="f12-btn icon sm ghost" onClick={() => onShare(card)} aria-label="Kartı paylaş" title="Paylaş"><Share2 aria-hidden /></button>
        <button type="button" className="f12-btn icon sm ghost" onClick={() => onReport(card)} aria-label="Hata bildir" title="Hata bildir"><AlertCircle aria-hidden /></button>
        <span className="f12-tools-sep" aria-hidden />
        <button type="button" className="f12-btn sm ghost" onClick={onExit} title="Oturumu bitir (Esc)"><X aria-hidden /> Bitir</button>
      </div>

      <div className="f12-keys f12-meta">
        <span><kbd className="f12-kbd">Space</kbd> çevir</span>
        <span><kbd className="f12-kbd">1</kbd> <kbd className="f12-kbd">2</kbd> <kbd className="f12-kbd">3</kbd> değerlendir</span>
        <span><kbd className="f12-kbd">←</kbd> <kbd className="f12-kbd">→</kbd> gezin</span>
        <span><kbd className="f12-kbd">F</kbd> favori</span>
        <span><kbd className="f12-kbd">Esc</kbd> bitir</span>
      </div>
      <p className="f12-swipe f12-meta">Açtıktan sonra sağa kaydır: iyi · sola: tekrar</p>

      <div className="f12-extras">
        <CardExtras card={card} />
      </div>
    </>
  );
};

// ---------------------------------------------------------------------------
// Göz at — kompakt liste
// ---------------------------------------------------------------------------
const STATUS_LABEL: Record<Status, string> = { new: 'Yeni', due: 'Tekrar', learning: 'Öğreniliyor', mastered: 'Ezber' };
const STATUS_TONE: Record<Status, string> = { new: '', due: 'warn', learning: 'acc', mastered: 'ok' };

const BrowseV12: React.FC<FlashcardsV12Props> = ({ visible, view, onView, query, onQuery, counts, groupTotal, favCount, statusFor, onStudyCards, onShare, onReport, loading }) => {
  const [q, setQ] = useState(query);
  const [shown, setShown] = useState(24);
  const [open, setOpen] = useState<string | null>(null);
  useEffect(() => setQ(query), [query]);
  useEffect(() => setShown(24), [visible]);
  if (loading) return null;

  const options: [View, string, number][] = [
    ['all', 'Tümü', groupTotal],
    ['due', 'Tekrar', counts.due],
    ['new', 'Yeni', counts.new],
    ['learning', 'Öğreniliyor', counts.learning],
    ['mastered', 'Ezber', counts.mastered],
    ['fav', 'Favoriler', favCount],
  ];

  return (
    <section className="f12-browse" aria-labelledby="f12-browse-h">
      <div className="f12-gh">
        <h2 className="f12-h2" id="f12-browse-h">Göz at</h2>
        <span className="f12-meta"><span className="f12-num">{fmt(visible.length)}</span> kart</span>
        <span className="f12-grow" />
        {view !== 'all' && visible.length > 0 && (
          <button type="button" className="f12-btn sm" onClick={() => onStudyCards(visible)} title="Yalnızca bu süzgeçteki kartları çalış">
            <Play aria-hidden /> Bunları çalış
          </button>
        )}
      </div>
      <div className="f12-tool">
        <label className="f12-field f12-search">
          <Search aria-hidden className="f12-ico" />
          <span className="f12-sr">Kartlarda ara</span>
          <input type="search" value={q} placeholder="Terim ya da tanım ara"
            onChange={(e) => {
              const v = e.target.value;
              setQ(v);
              startTransition(() => onQuery(v));
            }} />
          {q && (
            <button type="button" className="f12-x" aria-label="Aramayı temizle" onClick={() => { setQ(''); onQuery(''); }}>
              <X aria-hidden />
            </button>
          )}
        </label>
        <div className="f12-filters" role="radiogroup" aria-label="Kart süzgeci">
          {options.map(([id, label, n]) => (
            <button key={id} type="button" role="radio" aria-checked={view === id} className={`f12-pill${view === id ? ' on' : ''}`} onClick={() => onView(id)}>
              <span>{label}</span><b>{fmt(n)}</b>
            </button>
          ))}
        </div>
      </div>

      {visible.length === 0 ? (
        <div className="f12-panel f12-empty">
          <b>Bu aramada kart yok</b>
          <span className="f12-meta">Başka bir kelime dene ya da süzgeci “Tümü” yap.</span>
        </div>
      ) : (
        <ul className="f12-panel f12-list">
          {visible.slice(0, shown).map((c) => {
            const st = statusFor(c.id);
            const isOpen = open === c.id;
            const bodyId = `f12-b-${c.id}`;
            return (
              <li key={c.id} id={`card-${c.id}`} className={`f12-row${isOpen ? ' is-open' : ''}`}>
                <button type="button" className="f12-row-h" aria-expanded={isOpen} aria-controls={bodyId} onClick={() => setOpen(isOpen ? null : c.id)}>
                  <span className="f12-row-t">
                    <b className="f12-clamp1">{plain(c.front)}</b>
                    {!isOpen && <span className="f12-meta f12-clamp1">{plain(c.back)}</span>}
                  </span>
                  <span className={`f12-badge ${STATUS_TONE[st]}`}>{STATUS_LABEL[st]}</span>
                  <ChevronDown aria-hidden className={`f12-ico f12-chev${isOpen ? ' is-open' : ''}`} />
                </button>
                {isOpen && (
                  <div className="f12-row-b" id={bodyId}>
                    <p>{plain(c.back)}</p>
                    {c.sub && <span className="f12-meta">{c.sub}</span>}
                    <div className="f12-row-a">
                      <button type="button" className="f12-btn sm ghost" onClick={() => onShare(c)}><Share2 aria-hidden /> Paylaş</button>
                      <button type="button" className="f12-btn sm ghost" onClick={() => onReport(c)}><AlertCircle aria-hidden /> Hata bildir</button>
                    </div>
                  </div>
                )}
              </li>
            );
          })}
        </ul>
      )}
      {visible.length > shown && (
        <button type="button" className="f12-btn f12-more" onClick={() => setShown((n) => n + 48)}>
          Daha fazla göster · <span className="f12-num">{fmt(visible.length - shown)}</span>
        </button>
      )}
    </section>
  );
};

