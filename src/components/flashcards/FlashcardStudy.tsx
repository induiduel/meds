import React, { useCallback, useEffect, useRef, useState } from 'react';
import { speak } from '../../utils/tts';
import { X, RotateCcw, Volume2, ChevronLeft, ChevronRight, ChevronDown, Star, Share2, AlertCircle, BookA, GraduationCap } from 'lucide-react';
import { CardExtras } from './CardExtras';
import { getFavoriteCards, toggleFavoriteCard } from '../../services/studyStore';
import { SuccessCheck } from '../ui/Animations';

/**
 * Ezber kartları (v10) — canvas "Kartlar-Masaustu".
 *  - FlashcardDeckPanel: masaüstünde (≥1024) sol panel — başlık + toplam, Tekrar / Yeni / Zorlanılan
 *    kutucukları, bekleyen tekrar rozetli deste listesi. Telefon/tablette üstte kompakt seçim satırı.
 *  - FlashcardStudy: ilerleme satırı, tek büyük kart (soru; cevap kesikli çizginin altında açılır),
 *    puan satırı (Tekrar / Zor / İyi + sonraki aralık + 1–3 tuşu). Telefonda puan satırı sekme
 *    çubuğunun üstüne yapışır. Kaydırma: açıkken sağa iyi · sola tekrar.
 */
export interface FcCard {
  id: string;
  group: string;
  front: string;
  back: string;
  sub?: string;
  pearl?: string;
}
export type FcGrade = 'again' | 'hard' | 'good';

const plain = (s?: string) => String(s || '').replace(/\*\*/g, '');
const fmt = (n: number) => n.toLocaleString('tr-TR');

// ---------------------------------------------------------------------------
// Sol panel / üst seçim satırı
// ---------------------------------------------------------------------------
export interface FcDeck {
  id: string;
  label: string;
  total: number;
  due: number;
}

export const FlashcardDeckPanel: React.FC<{
  source: 'terms' | 'lessons';
  onSource: (s: 'terms' | 'lessons') => void;
  sourceCounts: { terms: number; lessons?: number };
  total: number;
  stats: { due: number; fresh: number; hard: number };
  onStat: (k: 'due' | 'fresh' | 'hard') => void;
  decks: FcDeck[];
  active: string;
  onPick: (id: string) => void;
  loading?: boolean;
}> = ({ source, onSource, sourceCounts, total, stats, onStat, decks, active, onPick, loading }) => (
  <aside className="fv-panel" aria-label="Desteler">
    <div className="fv-panel-h">
      <h1>Ezber kartları</h1>
      <span className="fv-panel-n" aria-label={`${fmt(total)} kart`}>{fmt(total)}</span>
    </div>
    <div role="radiogroup" aria-label="Kaynak" className="fv-src">
      {(
        [
          ['terms', BookA, 'Terimler', sourceCounts.terms],
          ['lessons', GraduationCap, 'Ders kartları', sourceCounts.lessons],
        ] as const
      ).map(([id, Icon, label, n]) => (
        <button key={id} type="button" role="radio" aria-checked={source === id} onClick={() => onSource(id)}>
          <Icon aria-hidden />
          <span>{label}</span>
          {n ? <small>{fmt(n)}</small> : null}
        </button>
      ))}
    </div>
    <div className="fv-tiles">
      {(
        [
          ['due', stats.due, 'Tekrar', 'is-warn', 'Tekrar zamanı gelen kartları göster'],
          ['fresh', stats.fresh, 'Yeni', 'is-acc', 'Yeni kartları göster'],
          ['hard', stats.hard, 'Zorlanılan', 'is-bad', 'Zorlandığın kartları çalış'],
        ] as const
      ).map(([k, n, label, tone, title]) => (
        <button key={k} type="button" className={`fv-tile ${tone}`} onClick={() => onStat(k)} disabled={loading || !n} title={title}>
          {loading ? <span className="ui-skel fv-tile-skel" aria-hidden /> : <strong>{fmt(n)}</strong>}
          <span>{label}</span>
        </button>
      ))}
    </div>

    {/* Masaüstü: liste · telefon/tablet: seçim kutusu */}
    <span className="fv-panel-k" id="fv-decks-k">{source === 'terms' ? 'KONULAR' : 'DESTELER'}</span>
    {loading ? (
      <div className="fv-decks" aria-hidden>
        {Array.from({ length: 6 }, (_, i) => <span key={i} className="ui-skel fv-deck-skel" />)}
      </div>
    ) : (
      <>
        <nav className="fv-decks" aria-labelledby="fv-decks-k">
          {decks.map((d) => (
            <button key={d.id} type="button" onClick={() => onPick(d.id)} aria-current={active === d.id ? 'true' : undefined} className="fv-deck">
              <span className="fv-deck-t">{d.label}</span>
              <span className={`fv-badge ${d.due ? 'is-due' : ''}`} aria-label={`${d.due} tekrar bekliyor, ${d.total} kart`}>{fmt(d.due)}</span>
            </button>
          ))}
        </nav>
        <label className="fv-pick">
          <span className="sr-only">{source === 'terms' ? 'Konu' : 'Deste'}</span>
          <select value={active} onChange={(e) => onPick(e.target.value)}>
            {decks.map((d) => (
              <option key={d.id} value={d.id}>
                {d.label} · {d.due ? `${fmt(d.due)} tekrar · ` : ''}{fmt(d.total)}
              </option>
            ))}
          </select>
          <ChevronDown aria-hidden />
        </label>
      </>
    )}
  </aside>
);

// ---------------------------------------------------------------------------
// Çalışma oturumu
// ---------------------------------------------------------------------------
const GRADES: [FcGrade, string, string, string][] = [
  ['again', 'Tekrar', '1', 'is-again'],
  ['hard', 'Zor', '2', 'is-hard'],
  ['good', 'İyi', '3', 'is-good'],
];

export const FlashcardStudy: React.FC<{
  cards: FcCard[];
  reverse: boolean;
  onGrade: (c: FcCard, g: FcGrade) => void;
  /** Bu puan verilirse kartın bir sonraki gelişi (ör. "1 gün") */
  intervalLabel: (c: FcCard, g: FcGrade) => string;
  onExit: () => void;
  onRestart: () => void;
  onShare?: (c: FcCard) => void;
  onReport?: (c: FcCard) => void;
}> = ({ cards, reverse, onGrade, intervalLabel, onExit, onRestart, onShare, onReport }) => {
  const [queue, setQueue] = useState<FcCard[]>(cards);
  const [idx, setIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [tally, setTally] = useState({ good: 0, hard: 0, again: 0 });
  const [leaving, setLeaving] = useState<FcGrade | null>(null);
  const [favIds, setFavIds] = useState(() => new Set(getFavoriteCards().map((c) => c.id)));
  const touch = useRef<{ x: number; y: number } | null>(null);

  // Deste değişince oturum baştan kurulur
  useEffect(() => {
    setQueue(cards);
    setIdx(0);
    setFlipped(false);
    setTally({ good: 0, hard: 0, again: 0 });
  }, [cards]);

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
  const toggleFav = useCallback((c: FcCard) => {
    const next = toggleFavoriteCard({ id: c.id, front: plain(c.front), back: plain(c.back), group: c.group });
    setFavIds(new Set(next.map((x) => x.id)));
  }, []);

  const card = queue[idx];
  const done = !card;
  const total = cards.length;
  const answered = tally.good + tally.hard;

  const answer = useCallback(
    (g: FcGrade) => {
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
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(t.tagName) || t.isContentEditable) return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === 'Escape') return onExit();
      if (e.key === ' ' || e.key === 'Enter') {
        // Odaktaki düğmenin kendi eylemi (ör. Notum) boşlukla çakışmasın
        if (t.tagName === 'BUTTON' && !t.closest('.fv-card')) return;
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

  // Ön yüz her zaman; kart açıksa cevap ve "Akılda tut" da okunur.
  const speakCard = () => {
    if (!card) return;
    const parts = [plain(front)];
    if (flipped) parts.push(plain(back), card.pearl ? `Akılda tut: ${plain(card.pearl)}` : '');
    speak(parts.filter(Boolean).join('. '));
  };

  if (done) {
    return (
      <div className="fv-done ms-pop-in">
        <SuccessCheck size={72} />
        <h2>Oturum bitti</h2>
        <p>{total} kart çalıştın. Bildiklerin bir sonraki tekrara kadar dinlenecek.</p>
        <div className="fv-done-tiles">
          {(
            [
              ['İyi', tally.good, 'is-ok'],
              ['Zor', tally.hard, 'is-warn'],
              ['Tekrar', tally.again, 'is-bad'],
            ] as const
          ).map(([label, n, tone]) => (
            <span key={label} className={tone}>
              <b>{n}</b>
              {label}
            </span>
          ))}
        </div>
        <div className="fv-done-act">
          <button type="button" onClick={onExit} className="ui-btn">
            Kartlara dön
          </button>
          <button type="button" onClick={onRestart} className="ui-btn is-primary">
            <RotateCcw aria-hidden />
            Yeniden çalış
          </button>
        </div>
      </div>
    );
  }

  const front = reverse ? card.back : card.front;
  const back = reverse ? card.front : card.back;
  const pct = Math.min(100, (answered / Math.max(total, 1)) * 100);
  const isQ = card.id.startsWith('q:') || card.id.startsWith('d:');
  const frontLabel = isQ ? (reverse ? 'CEVAP' : 'SORU') : reverse ? 'TANIM' : 'TERİM';
  const backLabel = isQ ? (reverse ? 'SORU' : 'CEVAP') : reverse ? 'TERİM' : 'TANIM';
  const isFav = favIds.has(card.id);
  const answerId = `fv-ans-${idx}`;

  return (
    <div className="fv-study">
      {/* İlerleme satırı: çıkış · deste · çubuk · sayaç */}
      <div className="fv-prog">
        <button type="button" onClick={onExit} aria-label="Oturumu bitir" title="Oturumu bitir (Esc)" className="fv-ib">
          <X aria-hidden />
        </button>
        <span className="fv-prog-t">{reverse ? 'Ters yön · ' : ''}{card.group || 'Ezber kartları'}</span>
        <span className="fv-bar" role="progressbar" aria-valuemin={0} aria-valuemax={total} aria-valuenow={answered} aria-label="İlerleme">
          <i style={{ width: `${pct}%` }} />
        </span>
        <span className="fv-prog-n">
          {Math.min(idx + 1, queue.length)} / {queue.length}
        </span>
      </div>

      {/* Tek büyük kart: soru, açılınca kesikli çizginin altında cevap */}
      <section
        id={`card-${card.id}`}
        aria-label="Kart"
        className={`fv-card ${flipped ? 'is-open' : ''} ${leaving ? `is-leave-${leaving}` : ''}`}
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
        <div className="fv-card-tools">
          <button type="button" onClick={goPrev} disabled={idx === 0} aria-label="Önceki kart" title="Önceki (←)" className="fv-ib"><ChevronLeft aria-hidden /></button>
          <button type="button" onClick={goNext} aria-label="Sonraki kart" title="Sonraki (→)" className="fv-ib"><ChevronRight aria-hidden /></button>
          <span className="fv-sp" />
          <button type="button" onClick={() => toggleFav(card)} aria-pressed={isFav} aria-label={isFav ? 'Favorilerden çıkar' : 'Favorilere ekle'} title="Favori (F)" className={`fv-ib ${isFav ? 'is-fav' : ''}`}>
            <Star fill={isFav ? 'currentColor' : 'none'} aria-hidden />
          </button>
          <button type="button" onClick={speakCard} aria-label={flipped ? 'Kartı seslendir' : 'Soruyu seslendir'} title={flipped ? 'Soru + cevabı oku' : 'Soruyu oku'} className="fv-ib"><Volume2 aria-hidden /></button>
          {onShare && <button type="button" onClick={() => onShare(card)} aria-label="Kartı paylaş" title="Kartı paylaş" className="fv-ib"><Share2 aria-hidden /></button>}
          {onReport && <button type="button" onClick={() => onReport(card)} aria-label="Hata bildir" title="Hata bildir" className="fv-ib"><AlertCircle aria-hidden /></button>}
        </div>

        <div className="fv-q">
          <span className="fv-k">{frontLabel}</span>
          <strong className={plain(front).length > 90 ? 'is-long' : ''}>{plain(front)}</strong>
          {!reverse && card.sub && <small>{card.sub}</small>}
        </div>

        {flipped ? (
          <div className="fv-a" id={answerId}>
            <span className="fv-k is-ok">{backLabel}</span>
            <strong className={reverse ? 'is-big' : plain(back).length > 160 ? 'is-long' : ''}>{plain(back)}</strong>
            {card.pearl && (
              <span className="fv-pearl">
                <b>Akılda tut</b>
                {plain(card.pearl)}
              </span>
            )}
          </div>
        ) : (
          <button type="button" className="fv-peek" onClick={() => setFlipped(true)} aria-expanded={false} aria-controls={answerId}>
            Cevabı göstermek için dokun · boşluk
          </button>
        )}
      </section>

      <CardExtras card={card} />

      {/* Puan satırı (telefonda sekme çubuğunun üstüne yapışık) */}
      <div className="fv-rate-wrap">
        {flipped ? (
          <div role="group" aria-label="Ne kadar iyi hatırladın" className="fv-rate">
            {GRADES.map(([g, label, key, cls]) => (
              <button key={g} type="button" onClick={() => answer(g)} className={`fv-grade ${cls}`} aria-keyshortcuts={key}>
                <span className="fv-grade-t">{label}</span>
                <span className="fv-grade-s">{intervalLabel(card, g)}</span>
                <kbd aria-hidden>{key}</kbd>
              </button>
            ))}
          </div>
        ) : (
          <button type="button" onClick={() => setFlipped(true)} className="fv-grade is-reveal" aria-keyshortcuts="Space">
            <span className="fv-grade-t">Cevabı göster</span>
            <kbd aria-hidden>Boşluk</kbd>
          </button>
        )}
      </div>
      <p className="fv-keys">
        <span className="fv-keys-touch">Açtıktan sonra sağa kaydır: iyi · sola: tekrar</span>
        <span className="fv-keys-kb">Boşluk: çevir · ← → gezin · F favori · 1 tekrar · 2 zor · 3 iyi · Esc çık</span>
      </p>
    </div>
  );
};
