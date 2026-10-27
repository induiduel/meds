import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { FlashcardStudy, FlashcardDeckPanel, FcDeck } from './FlashcardStudy';
import { PageToolbar } from '../ui/PageToolbar';
import { Shuffle, Repeat2, X, Play, Layers, ChevronDown, Share2, AlertCircle } from 'lucide-react';
import { getFavoriteCards } from '../../services/studyStore';
import { GLOSSARY } from '../../data/glossary';
import { EmptySearch, SectionLoader } from '../ui/Animations';
import { shareDeepLink, executeDeepLinkFocus } from '../../services/universalRedirectService';
import { ApiService } from '../../services/api';
import { toast } from '../ui/Toast';
import './fcHero.css';
import '../../styles/flashcards-v10.css';
import { useAppearance } from '../../utils/appearance';
import { FlashcardsV12 } from '../v12/FlashcardsV12';
import { useV15Baslik } from '../v15/baslik';
import '../../styles/v15/kartlar.css';

// ---------------------------------------------------------------------------
// Card model + spaced repetition (Leitner boxes, stored per device)
// ---------------------------------------------------------------------------
export interface StudyCard {
  id: string;
  group: string;
  front: string;
  back: string;
  sub?: string; // pronunciation or source line
  pearl?: string;
  /** Kartın ait olduğu kurullar; boşsa yalnız "Tümü"nde görünür */
  kurullar?: number[];
}

export type Grade = 'again' | 'hard' | 'good' | 'easy';
export interface CardState {
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
  // Kolay (tasarım F04 dörtlüsü): kutu iki basamak ilerler
  const b = Math.min(5, box + (grade === 'easy' ? 2 : 1));
  return { box: b, due: now + INTERVALS[b], seen };
};

export type Status = 'new' | 'due' | 'learning' | 'mastered';
const statusOf = (s: CardState | undefined, now: number): Status => {
  if (!s) return 'new';
  if (s.due <= now) return 'due';
  return s.box >= MASTERED_BOX ? 'mastered' : 'learning';
};

/** Zorlanılan: en az iki kez görülmüş ama hâlâ ilk kutularda kalan kart (tekrar/zor puanları) */
const isStruggling = (s: CardState | undefined) => !!s && s.seen >= 2 && s.box <= 1;

/** Puan düğmesindeki "sonraki geliş" etiketi (nextState'in gerçek aralığından) */
const gapLabel = (ms: number) => {
  if (ms < 60_000) return 'oturum sonu';
  if (ms < 3_600_000) return `${Math.round(ms / 60_000)} dk`;
  if (ms < DAY) return `${Math.round(ms / 3_600_000)} sa`;
  if (ms < 30 * DAY) return `${Math.round(ms / DAY)} gün`;
  return `${Math.round(ms / (30 * DAY))} ay`;
};

// ---------------------------------------------------------------------------
// Sources
// ---------------------------------------------------------------------------
const glossaryGroup = (cat: string) => {
  if (/^klinik hastalık/i.test(cat)) return 'Klinik hastalıklar';
  if (/^latin/i.test(cat)) return 'Latince & anatomi';
  return (cat.split(/\s*[\/&]\s*/)[0] || 'Diğer').trim();
};

const glossaryCards = (): StudyCard[] => GLOSSARY.map((g) => ({
  id: `g:${g.term}`,
  group: glossaryGroup(g.category || 'Diğer'),
  front: g.term,
  back: g.definition,
  sub: g.pronunciation,
  pearl: g.clinicalPearls,
  kurullar: g.kurullar,
}));

const deckGroup = (raw: string) => (raw || 'Diğer').split(/\s*(?:\/|&|,|\sve\s)\s*/)[0].trim() || 'Diğer';

const loadDeckCards = async (): Promise<StudyCard[]> => {
  const { loadDeckFlashcards, loadAllDecks, loadDeckCatalog } = await import('../../data/deckStore');
  const katalog = await loadDeckCatalog();
  const kurulOf = new Map<string, number[]>();
  katalog.forEach((d: any) => {
    const m = /Kurul\s*(\d)/gi;
    const ks = new Set<number>();
    for (const x of String(d.committee || '').matchAll(m)) ks.add(Number(x[1]));
    if (!ks.size && /Ürogenital Sistem Komitesi/i.test(String(d.committee || ''))) ks.add(1);
    if (ks.size) kurulOf.set(d.id, [...ks].sort());
  });
  const prebuilt = await loadDeckFlashcards();
  if (prebuilt && prebuilt.length > 0) {
    return (prebuilt as StudyCard[]).map((c) => ({ ...c, kurullar: kurulOf.get(String(c.id).split(':')[1]) }));
  }
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
          kurullar: kurulOf.get(d.id),
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
  const gorunum = useAppearance();
  const v12 = gorunum.design === 'v12';
  useV15Baslik(gorunum.v15 ? { baslik: 'Ezber kartları' } : null);
  const [source, setSource] = useState<'terms' | 'lessons'>('terms');
  const [deckCards, setDeckCards] = useState<StudyCard[] | null>(null);
  // Sözlük panelden değişince (canlı içerik) terim kartları yeniden kurulur
  const [termCards, setTermCards] = useState<StudyCard[]>(glossaryCards);
  useEffect(() => {
    const onChange = () => setTermCards(glossaryCards());
    window.addEventListener('medsoru:glossary-changed', onChange);
    return () => window.removeEventListener('medsoru:glossary-changed', onChange);
  }, []);
  const [group, setGroup] = useState('all');
  const [kurul, setKurul] = useState<number>(0); // 0 = tüm kurullar
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

  const allRaw = source === 'terms' ? termCards : deckCards || [];
  const kurulSayilari = useMemo(() => {
    const m: Record<number, number> = {};
    allRaw.forEach((c) => c.kurullar?.forEach((k) => (m[k] = (m[k] || 0) + 1)));
    return m;
  }, [allRaw]);
  const all = useMemo(() => (kurul ? allRaw.filter((c) => c.kurullar?.includes(kurul)) : allRaw), [allRaw, kurul]);
  useEffect(() => setGroup('all'), [kurul]);
  const kurulBar = (
    <div className="fv-kurul" role="radiogroup" aria-label="Kurul" style={{ display: 'flex', gap: 6, flexWrap: 'wrap', margin: '8px 0' }}>
      {[0, ...Object.keys(kurulSayilari).map(Number).sort()].map((k) => (
        <button
          key={k}
          type="button"
          role="radio"
          aria-checked={kurul === k}
          onClick={() => { setSession(null); setKurul(k); }}
          style={{
            padding: '4px 12px', borderRadius: 999, font: 'inherit', cursor: 'pointer',
            border: '1px solid var(--line, #8884)', background: kurul === k ? 'var(--accent, #2563eb)' : 'transparent',
            color: kurul === k ? '#fff' : 'inherit',
          }}
        >
          {k === 0 ? 'Tüm kurullar' : `Kurul ${k} · ${kurulSayilari[k]}`}
        </button>
      ))}
    </div>
  );
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

  /** Due cards first, then new ones, then (if nothing left) everything. `forGroup`: oturum sırasında deste değişimi */
  const buildSession = (forceAll = false, forGroup?: string) => {
    const src = forGroup === undefined ? inGroup : all.filter((c) => forGroup === 'all' || c.group === forGroup);
    const due = src.filter((c) => statusOf(store[c.id], now) === 'due');
    const fresh = src.filter((c) => statusOf(store[c.id], now) === 'new');
    let pool = forceAll ? src : [...(doShuffle ? shuffle(due) : due), ...(doShuffle ? shuffle(fresh) : fresh)];
    if (!pool.length) pool = src;
    if (forceAll && doShuffle) pool = shuffle(pool);
    setSession(pool.slice(0, limit > 0 ? limit : pool.length));
  };

  // v10 sol panel: deste listesi (bekleyen tekrar rozetli) + Zorlanılan sayısı
  const decks = useMemo<FcDeck[]>(() => {
    const due: Record<string, number> = {};
    let dueAll = 0;
    all.forEach((c) => {
      if (statusOf(store[c.id], now) !== 'due') return;
      due[c.group] = (due[c.group] || 0) + 1;
      dueAll++;
    });
    return [
      { id: 'all', label: 'Tümü', total: all.length, due: dueAll },
      ...groups.map(([g, n]) => ({ id: g, label: g, total: n, due: due[g] || 0 })),
    ];
  }, [all, groups, store, now]);
  const struggling = useMemo(() => inGroup.filter((c) => isStruggling(store[c.id])), [inGroup, store]);

  const intervalLabel = useCallback(
    (c: { id: string }, g: Grade) => {
      const t = Date.now();
      return gapLabel(nextState(store[c.id], g, t).due - t);
    },
    [store]
  );

  /** Panelden deste seçimi: oturum açıksa o destenin oturumu hemen başlar */
  const pickDeck = (id: string) => {
    setGroup(id);
    if (session) {
      setNow(Date.now());
      buildSession(false, id);
    }
  };
  const onStat = (k: 'due' | 'fresh' | 'hard') => {
    if (k === 'hard') {
      if (struggling.length) setSession(doShuffle ? shuffle(struggling) : struggling);
      return;
    }
    setSession(null);
    setView(k === 'due' ? 'due' : 'new');
    window.setTimeout(() => document.getElementById('fv-browse')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 60);
  };

  const grade = (card: StudyCard, g: Grade) => {
    setStore((prev) => {
      const next = { ...prev, [card.id]: nextState(prev[card.id], g) };
      writeStore(next);
      return next;
    });
  };

  const [reportingCard, setReportingCard] = useState<StudyCard | null>(null);
  const [reportReason, setReportReason] = useState('Hatalı Tanım / Cevap');
  const [reportDetails, setReportDetails] = useState('');
  const [isSubmittingReport, setIsSubmittingReport] = useState(false);

  const handleShare = useCallback((c: StudyCard) => {
    shareDeepLink({
      type: 'flashcard',
      targetId: c.id,
      title: `Akıl Kartı: ${plain(c.front)}`,
      highlightText: plain(c.back),
    });
  }, []);

  const handleReport = useCallback((c: StudyCard) => {
    setReportingCard(c);
    setReportReason('Hatalı Tanım / Cevap');
    setReportDetails('');
  }, []);

  const submitCardReport = async () => {
    if (!reportingCard) return;
    setIsSubmittingReport(true);
    try {
      await ApiService.reportFlashcard(reportingCard.id, reportReason, reportDetails);
      toast.success('Hata Bildirildi', 'Kart bildirimi kaydedildi, inceleme kuyruğuna alındı.');
      setReportingCard(null);
    } catch (err: any) {
      toast.error('Hata', err?.message || 'Bildirim kaydedilemedi.');
    } finally {
      setIsSubmittingReport(false);
    }
  };

  // Derin Bağlantı (Deep Link) ile karta doğrudan zıplama
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const sp = new URLSearchParams(window.location.search);
    const targetId = sp.get('id') || (window.location.hash.startsWith('#card-') ? decodeURIComponent(window.location.hash.slice(6)) : null);
    if (targetId && all.length > 0) {
      const found = all.find((c) => c.id === targetId || c.id === `g:${targetId}` || c.front.toLowerCase() === targetId.toLowerCase());
      if (found) {
        setSession([found]);
        setTimeout(() => executeDeepLinkFocus({ targetId: found.id }), 300);
      }
    }
  }, [all]);

  const loading = source === 'lessons' && !deckCards;
  const startCount = Math.min(limit > 0 ? limit : inGroup.length, counts.due + counts.new || inGroup.length);

  const reportDialog = reportingCard && (
    <div className="cf-root" role="dialog" aria-modal="true">
      <div className="cf max-w-md w-full !text-left">
        <div className="flex items-center justify-between w-full border-b border-line pb-2 mb-2">
          <div className="flex items-center gap-2">
            <div className="cf-ic !w-8 !h-8 !mb-0 bg-bad-soft text-bad-text">
              <AlertCircle className="w-4 h-4" />
            </div>
            <h3 className="font-bold text-base m-0 text-ink">Kart Hata Bildirimi</h3>
          </div>
          <button
            type="button"
            onClick={() => setReportingCard(null)}
            className="ms-btn is-icon is-ghost !w-7 !h-7"
            aria-label="Kapat"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="bg-canvas p-2.5 rounded-xl border border-line text-xs space-y-1 mb-2">
          <div className="font-semibold text-ink line-clamp-1">{plain(reportingCard.front)}</div>
          <div className="text-ink-3 line-clamp-2">{plain(reportingCard.back)}</div>
        </div>

        <label className="text-xs font-semibold text-ink-2 mb-1 block">Bildirim Sebebi</label>
        <select
          value={reportReason}
          onChange={(e) => setReportReason(e.target.value)}
          className="w-full h-10 px-3 rounded-lg border border-line bg-canvas text-sm text-ink mb-3"
        >
          <option value="Hatalı Tanım / Cevap">Hatalı Tanım / Cevap</option>
          <option value="İmla / Yazım Yanlışı">İmla / Yazım Yanlışı</option>
          <option value="Ders Notu Uyuşmazlığı">Ders Notu Uyuşmazlığı</option>
          <option value="Eksik Kilit Bilgi">Eksik Kilit Bilgi</option>
          <option value="Diğer">Diğer</option>
        </select>

        <label className="text-xs font-semibold text-ink-2 mb-1 block">Detay / Doğru Bilgi (Opsiyonel)</label>
        <textarea
          value={reportDetails}
          onChange={(e) => setReportDetails(e.target.value)}
          placeholder="Düzeltilmesi gereken noktayı açıklayabilirsiniz…"
          rows={3}
          className="w-full p-2.5 rounded-lg border border-line bg-canvas text-sm text-ink mb-4 resize-none"
        />

        <div className="flex justify-end gap-2 w-full">
          <button
            type="button"
            onClick={() => setReportingCard(null)}
            className="ms-btn is-ghost is-sm"
          >
            Vazgeç
          </button>
          <button
            type="button"
            disabled={isSubmittingReport}
            onClick={submitCardReport}
            className="ms-btn is-primary is-sm bg-bad hover:bg-bad-hover text-white font-semibold"
          >
            {isSubmittingReport ? 'Gönderiliyor…' : 'Bildirimi Gönder'}
          </button>
        </div>
      </div>
    </div>
  );

  if (v12) {
    return (
      <FlashcardsV12
        source={source}
        onSource={(s) => {
          setSession(null);
          setSource(s);
        }}
        sourceCounts={{ terms: termCards.length, lessons: deckCards?.length }}
        kurulBar={kurulBar}
        decks={decks}
        group={group}
        onPickDeck={(id) => {
          setGroup(id);
          setNow(Date.now());
          buildSession(false, id);
        }}
        loading={loading}
        groupTotal={inGroup.length}
        counts={counts}
        struggling={struggling}
        session={session}
        onStart={(forceAll) => {
          setNow(Date.now());
          buildSession(forceAll);
        }}
        onStudyCards={(cards) => setSession(doShuffle ? shuffle(cards) : cards)}
        startCount={startCount}
        limit={limit}
        onLimit={setLimit}
        doShuffle={doShuffle}
        onShuffle={setDoShuffle}
        reverse={reverse}
        onReverse={setReverse}
        onGrade={grade}
        intervalLabel={intervalLabel}
        onExit={() => {
          setSession(null);
          setNow(Date.now());
          setFavCards(getFavoriteCards());
        }}
        onShare={handleShare}
        onReport={handleReport}
        visible={visible}
        view={view}
        onView={setView}
        query={query}
        onQuery={setQuery}
        statusFor={(id) => statusOf(store[id], now)}
        favCount={favCards.length}
        reportDialog={reportDialog}
      />
    );
  }

  // v10 yerleşim: solda deste paneli (telefon/tablette üstte kompakt seçim), sağda oturum ya da başlangıç + göz at
  return (
    <div className={`ds-page fv ${session ? 'is-study' : ''}`}>
      <FlashcardDeckPanel
        source={source}
        onSource={(s) => {
          setSession(null);
          setSource(s);
        }}
        sourceCounts={{ terms: termCards.length, lessons: deckCards?.length }}
        total={all.length}
        stats={{ due: counts.due, fresh: counts.new, hard: struggling.length }}
        onStat={onStat}
        decks={decks}
        active={group}
        onPick={pickDeck}
        loading={loading}
      />

      <div className="fv-main">
        {!session && kurulBar}
        {session ? (
          <FlashcardStudy
            cards={session}
            reverse={reverse}
            onGrade={grade}
            intervalLabel={intervalLabel}
            onExit={() => {
              setSession(null);
              setNow(Date.now());
              setFavCards(getFavoriteCards());
            }}
            onRestart={() => {
              setNow(Date.now());
              buildSession(true);
            }}
            onShare={handleShare}
            onReport={handleReport}
          />
        ) : loading ? (
          <SectionLoader label="Ders kartları yükleniyor…" />
        ) : (
          <>
            {/* Bugünkü oturum (v9): ilerleme halkası + durum hapları + tek satır ayar + tek birincil eylem */}
            <section className="fc-hero" aria-label="Bugünkü oturum">
              <div className="fc-hero-top">
                <Ring value={inGroup.length ? counts.mastered / inGroup.length : 0} />
                <div className="fc-hero-t">
                  <b>{counts.due + counts.new > 0 ? `Bugün ${counts.due + counts.new} kart seni bekliyor` : 'Bugünlük hepsi tamam'}</b>
                  <div className="fc-pills">
                    {(
                      [
                        ['tekrar', counts.due, 'is-warn'],
                        ['yeni', counts.new, ''],
                        ['öğreniliyor', counts.learning, 'is-acc'],
                        ['ezber', counts.mastered, 'is-ok'],
                      ] as const
                    ).map(([label, n, tone]) => (
                      <span key={label} className={`fc-pill ${tone}`}><b>{n.toLocaleString('tr-TR')}</b> {label}</span>
                    ))}
                  </div>
                </div>
              </div>
              <div className="fc-hero-ctl">
                <div role="radiogroup" aria-label="Kart sayısı" className="ds-seg is-compact fc-count">
                  {[10, 20, 50, 0].map((n) => (
                    <button key={n} type="button" role="radio" aria-checked={limit === n} onClick={() => setLimit(n)}>
                      {n === 0 ? 'Hepsi' : n}
                    </button>
                  ))}
                </div>
                <ToggleChip on={doShuffle} onClick={() => setDoShuffle((v) => !v)} icon={Shuffle} label="Karıştır" />
                <ToggleChip on={reverse} onClick={() => setReverse((v) => !v)} icon={Repeat2} label="Ters çevir" />
                {counts.due + counts.new > 0 && counts.learning + counts.mastered > 0 && (
                  <button type="button" onClick={() => buildSession(true)} className="fc-ibtn" aria-label="Tüm kartlarla başla" title="Tüm kartlar">
                    <Layers aria-hidden />
                  </button>
                )}
              </div>
              <button type="button" onClick={() => buildSession(false)} disabled={inGroup.length === 0} className="fc-go">
                <Play className="fill-current" aria-hidden />
                {counts.due + counts.new > 0 ? `Başla · ${startCount} kart` : 'Hepsini tekrar et'}
              </button>
            </section>

            {/* Göz at: durum ve favori süzgeci (ortak kompakt başlık) */}
            <section className="fv-browse" id="fv-browse" aria-label="Kartlara göz at">
              <PageToolbar
                className="fv-toolbar"
                title="Göz at"
                count={`${visible.length.toLocaleString('tr-TR')} kart`}
                search={{ value: query, onChange: setQuery, placeholder: 'Terim ya da tanım ara' }}
                segments={{
                  label: 'Kart süzgeci',
                  value: view,
                  onChange: setView,
                  options: [
                    { id: 'all', label: 'Tümü', count: inGroup.length },
                    { id: 'due', label: 'Tekrar', count: counts.due },
                    { id: 'new', label: 'Yeni', count: counts.new },
                    { id: 'learning', label: 'Öğreniliyor', count: counts.learning },
                    { id: 'mastered', label: 'Ezber', count: counts.mastered },
                    { id: 'fav', label: 'Favoriler', count: favCards.length },
                  ],
                }}
                tools={
                  view !== 'all' && visible.length > 0 ? (
                    <button
                      type="button"
                      onClick={() => setSession(doShuffle ? shuffle(visible) : visible)}
                      className="ms-btn is-tonal is-sm"
                      title="Yalnızca bu süzgeçteki kartları çalış"
                    >
                      <Play className="fill-current" aria-hidden /> Bunları çalış
                    </button>
                  ) : undefined
                }
              />
              <BrowseList
                cards={visible}
                store={store}
                now={now}
                onShare={handleShare}
                onReport={handleReport}
              />
            </section>
          </>
        )}
      </div>

      {reportDialog}
    </div>
  );
};

/** Açık/kapalı ayar: simge + etiket (telefonda yalnız simge; etiket aria-label ve ipucunda) */
const ToggleChip: React.FC<{ on: boolean; onClick: () => void; icon: React.ElementType; label: string }> = ({ on, onClick, icon: Icon, label }) => (
  <button type="button" aria-pressed={on} onClick={onClick} className={`fc-toggle ${on ? 'is-on' : ''}`} aria-label={label} title={label}>
    <Icon aria-hidden />
    <span>{label}</span>
  </button>
);

/** Ezber oranı halkası */
const Ring: React.FC<{ value: number }> = ({ value }) => {
  const pct = Math.round(value * 100);
  return (
    <span className="fc-ring" role="img" aria-label={`Ezber oranı yüzde ${pct}`}>
      <svg viewBox="0 0 44 44" aria-hidden="true">
        <circle cx="22" cy="22" r="18" fill="none" stroke="var(--color-line)" strokeWidth="5" />
        <circle cx="22" cy="22" r="18" fill="none" stroke="var(--color-ok)" strokeWidth="5" strokeLinecap="round" strokeDasharray={`${(value * 113.1).toFixed(1)} 113.1`} transform="rotate(-90 22 22)" className="fc-ring-arc" />
      </svg>
      <b>%{pct}</b>
    </span>
  );
};

const STATUS_LABEL: Record<Status, string> = { new: 'Yeni', due: 'Tekrar', learning: 'Öğreniliyor', mastered: 'Ezber' };
const STATUS_TONE: Record<Status, string> = { new: '', due: 'is-warn', learning: 'is-new', mastered: 'is-ok' };

const BrowseList: React.FC<{
  cards: StudyCard[];
  store: Record<string, CardState>;
  now: number;
  onShare: (c: StudyCard) => void;
  onReport: (c: StudyCard) => void;
}> = ({ cards, store, now, onShare, onReport }) => {
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
            <li key={c.id} id={`card-${c.id}`}>
              <div className={`ds-row ${isOpen ? 'is-open' : ''} flex-col !items-stretch`}>
                <div
                  role="button"
                  tabIndex={0}
                  onClick={() => setOpen(isOpen ? null : c.id)}
                  onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && setOpen(isOpen ? null : c.id)}
                  aria-expanded={isOpen}
                  className="flex items-center gap-3 cursor-pointer w-full text-left"
                >
                  <span className="ds-row-t flex-1 min-w-0">
                    <b>{plain(c.front)}</b>
                    <span className={isOpen ? '' : 'line-clamp-1'}>{plain(c.back)}</span>
                  </span>
                  <span className={`ms-tag ${STATUS_TONE[st]}`}>{STATUS_LABEL[st]}</span>
                  <ChevronDown className={`ds-row-chev ${isOpen ? 'is-open' : ''}`} aria-hidden />
                </div>
                {isOpen && (
                  <div className="flex items-center gap-2 mt-2 pt-2 border-t border-line/60">
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        onShare(c);
                      }}
                      className="ms-btn is-sm is-ghost gap-1.5"
                      title="Kartı Paylaş"
                    >
                      <Share2 className="w-3.5 h-3.5" />
                      <span>Paylaş</span>
                    </button>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        onReport(c);
                      }}
                      className="ms-btn is-sm is-ghost gap-1.5 text-ink-3 hover:text-bad-text"
                      title="Hata Bildir"
                    >
                      <AlertCircle className="w-3.5 h-3.5" />
                      <span>Hata Bildir</span>
                    </button>
                  </div>
                )}
              </div>
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
