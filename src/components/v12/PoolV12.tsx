import React, { startTransition, useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { Activity, ChevronDown, ChevronLeft, ChevronRight, ChevronUp, Combine, LayoutGrid, Plus, Search, Share2, SlidersHorizontal, X } from 'lucide-react';
import type { PoolViewProps } from '../pool/PoolView';
import type { QuestionItem } from '../../types';
import { QuestionCard } from '../QuestionCard';
import { committeeShortLabel } from '../quickAddOrtak';
import { ActionMenu, ActionItem } from '../ui/ActionMenu';
import { useAppearance } from '../../utils/appearance';
import { yanlisOku } from '../../services/yanlislarim';
import { getFavorites } from '../../services/studyStore';
import '../../styles/v15/ogren.css';
import '../../styles/v15/liste2.css';
import { topBarOffset } from '../../utils/uiZoom';
import { PoolSegment, PoolSummary, fullTime, isMissing, relTime, summarize } from '../pool/poolModel';
import { PoolOptFill } from '../pool/PoolRow';
import { PoolContribs } from '../pool/PoolContribs';
import { PoolLiveFeed, usePoolActivity } from '../pool/PoolLiveFeed';
import { poolDisciplineOptions, useMedia, usePoolClusters } from '../pool/poolHooks';
import '../../styles/pool.css';
import '../../styles/v12/pool.css';
import '../../styles/v15/havuz.css';
import { useV15Baslik } from '../v15/baslik';

/**
 * Soru havuzu — v12 "Net" (canvas panosu Pool.dc.html, sol yarı).
 *  - Panel: "Havuz" + sayı + Tümü/Katkılarım; arama; durum hapları (İnceleniyor / Doğrulandı / Parça) sayılarıyla.
 *  - Satır: durum rozeti (+ "YZ tamamladı"), kurul · ders, göreli zaman, 2 satır parça, katkı sayısı · son güncelleme.
 *  - YZ'nin tamamladığı ya da kurduğu her kayıt "İnceleniyor"dur; "Doğrulandı" yalnız onaylı (status: completed) kayıttır.
 *  - ≥1180 px (akış düzeni dışında): sağda ayrıntı bölmesi; daha darda satır yerinde açılır.
 *  - Veri, süzgeçler ve işleyiciler App.tsx'ten (PoolViewProps); klasik PoolView ile aynı kancalar (pool/poolHooks).
 */

type Q12Status = 'review' | 'verified' | 'fragment';
const STATUS_TEXT: Record<Q12Status, string> = { review: 'İnceleniyor', verified: 'Doğrulandı', fragment: 'Parça' };
const STATUS_TONE: Record<Q12Status, string> = { review: 'is-warn', verified: 'is-ok', fragment: '' };
const APP_STATUS_LABEL: Record<string, string> = { completed: 'Doğrulanan', gathering: 'Taslak', empty: 'Boş yuva' };
const SEG_KEY = 'medsoru_pool_segment';
const PAGE = 30;

/** YZ bu kaydın kökünü ya da şıklarını tamamladı mı (onaylanmadıkça İnceleniyor kalır) */
const aiCompleted = (q: QuestionItem) =>
  q.status === 'reconstructing' ||
  !!q.reconstruction?.stem?.trim() ||
  (q.reconstruction?.options || []).some((o) => o.text?.trim()) ||
  (q.options || []).some((o) => o.isAiGenerated && o.text?.trim());

function q12StatusOf(s: PoolSummary): Q12Status {
  if (s.q.status === 'completed') return 'verified';
  // Kökü ve en az iki şıkkı olan soru incelemeye girer; tek başına kök/şık/ipucu "Parça"dır
  if (aiCompleted(s.q) || (s.hasStem && s.filled.size >= 2)) return 'review';
  return 'fragment';
}

/** Katkı = kök/şık/ipucu/cevap parçaları, şık önerileri ve açılış (yorum ve düzenleme hariç) */
const contribCount = (s: PoolSummary) => s.events.filter((e) => e.kind !== 'comment' && e.kind !== 'revision').length;

/** "3 sa" → "3 sa önce"; "dün" / "12 Eki" olduğu gibi */
const agoText = (at: number, now: number) => {
  const r = relTime(at, now);
  return /^\d+ (dk|sa|gün)$/.test(r) ? `${r} önce` : r;
};

/** Son güncelleme: bugünse saat, değilse gün ay */
const updatedText = (at: number, now: number) => {
  if (!at) return '';
  const d = new Date(at);
  const today = new Date(now);
  return d.toDateString() === today.toDateString()
    ? d.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
    : d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
};

const readSeg = (): Exclude<PoolSegment, 'mine'> => {
  try {
    const v = localStorage.getItem(SEG_KEY);
    if (v === 'new' || v === 'order' || v === 'missing') return v;
  } catch { /* yoksay */ }
  return 'new';
};

const byNumber = (a: PoolSummary, b: PoolSummary) =>
  (a.q.questionNumber || Number.MAX_SAFE_INTEGER) - (b.q.questionNumber || Number.MAX_SAFE_INTEGER);
const byRecent = (a: PoolSummary, b: PoolSummary) => b.lastAt - a.lastAt || byNumber(a, b);

/** Öğeyi yapışkan üst çubuğun altına getirir */
function bringIntoView(el: Element | null, mode: 'top' | 'nearest') {
  if (!el) return;
  const sh = topBarOffset();
  const r = el.getBoundingClientRect();
  const off = sh + 8;
  const vh = window.innerHeight;
  let dy = 0;
  if (mode === 'top') dy = r.top - off;
  else if (r.top < off) dy = r.top - off;
  else if (r.bottom > vh - 12) dy = Math.min(r.bottom - (vh - 12), r.top - off);
  if (Math.abs(dy) < 2) return;
  const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches || document.documentElement.dataset.motion === 'reduced';
  window.scrollTo({ top: Math.max(0, window.scrollY + dy), behavior: reduce ? 'auto' : 'smooth' });
}

const StatusBadge: React.FC<{ s: Q12Status }> = ({ s }) => <span className={`q12-badge ${STATUS_TONE[s]}`}>{STATUS_TEXT[s]}</span>;

/** Havuz satırı (canvas .pl-item) */
const PoolItemV12 = React.memo(function PoolItemV12({ sum, now, label, mode, selected, onToggle }: {
  sum: PoolSummary;
  now: number;
  label: string;
  mode: 'expand' | 'select';
  selected: boolean;
  onToggle: (id: string) => void;
}) {
  const { q } = sum;
  const st = q12StatusOf(sum);
  const ai = st === 'review' && aiCompleted(q);
  const n = contribCount(sum);
  const disc = (q.discipline || '').trim();
  const where = [q.questionNumber ? `Soru ${q.questionNumber}` : '', label, disc && !/^(belirtilmedi|genel|belirsiz)$/i.test(disc) ? disc : ''].filter(Boolean).join(' · ');
  const a11y = mode === 'expand' ? { 'aria-expanded': selected } : { 'aria-current': selected ? ('true' as const) : undefined };
  return (
    <button
      type="button"
      className={`q12-item ${selected ? 'is-on' : ''}`}
      data-row={q.id}
      onClick={() => onToggle(q.id)}
      aria-label={`${where || 'Numarasız soru'}, ${STATUS_TEXT[st]}${ai ? ', yapay zekâ tamamladı' : ''}: ${sum.stem.slice(0, 90) || 'kök yok'}`}
      {...a11y}
    >
      <span className="q12-item-top" aria-hidden>
        <StatusBadge s={st} />
        {ai && <span className="q12-badge is-ai">YZ tamamladı</span>}
        <span className="q12-meta q12-grow q12-clamp1">{where}</span>
        {sum.lastAt > 0 && <time className="q12-meta" dateTime={new Date(sum.lastAt).toISOString()} title={fullTime(sum.lastAt)}>{agoText(sum.lastAt, now)}</time>}
      </span>
      <span className={`q12-item-s q12-clamp2 ${sum.hasStem ? '' : 'is-empty'}`} aria-hidden>{sum.stem || 'Kök henüz yok — hatırladığını ekle'}</span>
      <span className="q12-meta" aria-hidden>
        {n > 0 ? <><span className="q12-num">{n}</span> katkı</> : 'Katkı yok'}
        {sum.lastAt > 0 && <> · son güncelleme {updatedText(sum.lastAt, now)}</>}
      </span>
      {mode === 'expand' && <ChevronDown className="q12-item-chev" aria-hidden />}
    </button>
  );
});

const PoolItemSkeleton: React.FC = () => (
  <div className="q12-item is-skel" aria-hidden>
    <span className="q12-skel" style={{ width: 160, height: 14 }} />
    <span className="q12-skel" style={{ height: 13 }} />
    <span className="q12-skel" style={{ width: '62%', height: 13 }} />
  </div>
);

export const PoolV12: React.FC<PoolViewProps> = (p) => {
  const { layout, v15 } = useAppearance();
  useV15Baslik(v15 ? { baslik: 'Soru havuzu', alt: 'Hatırladığın parçaları birleştir' } : null);
  const wide = useMedia('(min-width: 1180px)');
  const split = layout !== 'akis' && wide;

  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    const t = window.setInterval(() => setNow(Date.now()), 60_000);
    return () => window.clearInterval(t);
  }, []);

  // Arama: yerel değer anında, App'e geçiş önceliğinde (yazarken takılmaz)
  const [q, setQ] = useState(p.searchQuery);
  const sentQ = useRef(p.searchQuery);
  useEffect(() => {
    if (p.searchQuery !== sentQ.current) { sentQ.current = p.searchQuery; setQ(p.searchQuery); }
  }, [p.searchQuery]);
  const onSearch = (v: string) => {
    setQ(v);
    sentQ.current = v;
    startTransition(() => p.onSearchChange(v));
  };

  const [openId, setOpenId] = useState<string | undefined>(p.focusQuestion?.id);
  const [pinnedId, setPinnedId] = useState<string | undefined>();
  const revealRef = useRef<string | undefined>(p.focusQuestion?.id);
  useEffect(() => {
    if (p.focusQuestion) { setOpenId(p.focusQuestion.id); revealRef.current = p.focusQuestion.id; }
  }, [p.focusQuestion?.id]);

  const [sort, setSortRaw] = useState(readSeg);
  const setSort = (s: Exclude<PoolSegment, 'mine'>) => {
    setSortRaw(s);
    try { localStorage.setItem(SEG_KEY, s); } catch { /* yoksay */ }
    p.setVisibleCount(PAGE);
  };
  const [stFilter, setStFilter] = useState<Q12Status | null>(null);
  const [moreOpen, setMoreOpen] = useState(false);

  const setMine = (v: boolean) => {
    if (v !== p.mineOnly) p.onSetMineOnly(v);
    p.setVisibleCount(PAGE);
    if (!split) setOpenId(undefined);
    setPinnedId(undefined);
  };

  const allSums = useMemo(() => p.allQuestions.map(summarize), [p.allQuestions]);
  const sumById = useMemo(() => new Map(allSums.map((s) => [s.q.id, s])), [allSums]);
  const sumOf = useCallback((x: QuestionItem) => {
    const s = sumById.get(x.id);
    return s && s.q === x ? s : summarize(x);
  }, [sumById]);
  const poolSums = useMemo(() => p.poolQuestions.map(sumOf), [p.poolQuestions, sumOf]);
  const statusById = useMemo(() => new Map(poolSums.map((s) => [s.q.id, q12StatusOf(s)])), [poolSums]);
  const stCounts = useMemo(() => {
    const c: Record<Q12Status, number> = { review: 0, verified: 0, fragment: 0 };
    statusById.forEach((v) => { c[v]++; });
    return c;
  }, [statusById]);

  // tasarım L04 kişisel süzgeç (v15): Hepsi · Yanlışlarım · Kaydettiklerim · Yorumlu
  const [kisi, setKisi] = useState<'hepsi' | 'yanlis' | 'kayit' | 'yorum'>('hepsi');
  const kisiSet = useMemo(() => (kisi === 'yanlis' ? new Set(Object.keys(yanlisOku())) : kisi === 'kayit' ? getFavorites() : null), [kisi]);
  const list = useMemo(() => {
    if (p.focusQuestion) return [sumOf(p.focusQuestion)];
    const base0 = stFilter ? poolSums.filter((s) => statusById.get(s.q.id) === stFilter) : poolSums;
    const base = kisi === 'hepsi' ? base0 : base0.filter((s) => (kisi === 'yorum' ? (s.q.comments?.length || 0) > 0 : !!kisiSet?.has(s.q.id)));
    if (sort === 'order') return [...base].sort(byNumber);
    if (sort === 'missing') return base.filter(isMissing).sort(byNumber);
    return [...base].sort(byRecent);
  }, [poolSums, statusById, stFilter, sort, p.focusQuestion, sumOf, kisi, kisiSet]);
  const shown = list.slice(0, p.visibleCount);
  const hasMore = !p.focusQuestion && list.length > p.visibleCount;
  const inList = useCallback((id?: string) => !!id && list.some((s) => s.q.id === id), [list]);

  const pinned = pinnedId && pinnedId === openId && !inList(pinnedId) ? sumById.get(pinnedId) : undefined;
  const selectedId = split ? (inList(openId) || pinned ? openId : shown[0]?.q.id) : openId;
  const selected = selectedId ? list.find((s) => s.q.id === selectedId) || sumById.get(selectedId) : undefined;

  const { setVisibleCount } = p;
  const openQuestion = useCallback((id: string) => {
    const idx = list.findIndex((s) => s.q.id === id);
    if (idx >= 0) {
      setPinnedId(undefined);
      setVisibleCount((v) => (idx >= v ? Math.ceil((idx + 1) / PAGE) * PAGE : v));
    } else setPinnedId(id);
    setOpenId(id);
    revealRef.current = id;
  }, [list, setVisibleCount]);

  const onToggle = useCallback((id: string) => {
    if (split) { setOpenId(id); setPinnedId(undefined); return; }
    setOpenId((cur) => {
      if (cur === id) return undefined;
      revealRef.current = id;
      return id;
    });
  }, [split]);
  const closeOpen = useCallback(() => {
    const id = openId;
    setOpenId(undefined);
    setPinnedId(undefined);
    window.requestAnimationFrame(() => {
      const row = document.querySelector<HTMLElement>(`.q12-pool [data-row="${CSS.escape(id || '')}"]`);
      if (row) { bringIntoView(row, 'nearest'); row.focus({ preventScroll: true }); }
    });
  }, [openId]);

  const listRef = useRef<HTMLUListElement>(null);
  const detailRef = useRef<HTMLElement>(null);
  useLayoutEffect(() => {
    if (split && detailRef.current) detailRef.current.scrollTop = 0;
  }, [split, selectedId]);
  useEffect(() => {
    const id = revealRef.current;
    if (!id) return;
    revealRef.current = undefined;
    const raf = window.requestAnimationFrame(() => {
      const li = listRef.current?.querySelector<HTMLElement>(`[data-qid="${CSS.escape(id)}"]`);
      if (li) bringIntoView(split ? li.querySelector('.q12-item') : li, split ? 'nearest' : 'top');
    });
    return () => window.cancelAnimationFrame(raf);
  });

  const onListKey = (e: React.KeyboardEvent<HTMLUListElement>) => {
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
    const rows = Array.from(e.currentTarget.querySelectorAll<HTMLButtonElement>('.q12-item[data-row]'));
    const i = rows.findIndex((r) => r === document.activeElement);
    if (i < 0) return;
    const nxt = rows[e.key === 'ArrowDown' ? i + 1 : i - 1];
    if (!nxt) return;
    e.preventDefault();
    nxt.focus();
    if (split && nxt.dataset.row) { setOpenId(nxt.dataset.row); setPinnedId(undefined); }
  };

  const sentinel = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = sentinel.current;
    if (!el || !hasMore || typeof IntersectionObserver === 'undefined') return;
    const io = new IntersectionObserver((ents) => {
      if (ents.some((x) => x.isIntersecting)) setVisibleCount((v) => v + PAGE);
    }, { rootMargin: '600px 0px' });
    io.observe(el);
    return () => io.disconnect();
  }, [hasMore, shown.length, setVisibleCount]);

  const activity = usePoolActivity(allSums, now);
  const [feedOpen, setFeedOpen] = useState(false);

  const committee = p.committees.find((c) => c.id === p.selectedCommitteeId);
  const kLabel = committee ? committeeShortLabel(committee) : '';

  const discOptions = useMemo(() => poolDisciplineOptions(p.allQuestions), [p.allQuestions]);
  const { selectedDiscipline, onSelectDiscipline } = p;
  useEffect(() => {
    if (!p.loading && p.allQuestions.length && selectedDiscipline && selectedDiscipline !== 'Tümü' && !discOptions.some((o) => o.id === selectedDiscipline)) onSelectDiscipline('Tümü');
  }, [discOptions, selectedDiscipline, onSelectDiscipline, p.loading, p.allQuestions.length]);

  const { clusters, clusterOf } = usePoolClusters(p.selectedCommitteeId, p.allQuestions.length);
  const mergeCount = clusters.length;

  const discOn = !!p.selectedDiscipline && p.selectedDiscipline !== 'Tümü';
  const appStatusOn = !!p.selectedStatus && p.selectedStatus !== 'Tümü';
  const moreCount = (discOn ? 1 : 0) + (appStatusOn ? 1 : 0) + (sort !== 'new' ? 1 : 0);
  const clearAll = () => {
    setStFilter(null);
    if (discOn) p.onSelectDiscipline('Tümü');
    if (appStatusOn) p.onSelectStatus('Tümü');
    if (q) onSearch('');
  };

  const adminItems: ActionItem[] = p.isAdmin
    ? [{
        label: p.isGeneratingSlots ? 'Yuvalar açılıyor…' : `1–${p.stats.target} soru yuvalarını aç`,
        icon: LayoutGrid,
        onClick: p.onGenerateSlots,
        disabled: p.isGeneratingSlots || p.stats.empty === 0,
        hint: p.stats.empty > 0 ? `${p.stats.empty} boş` : 'tamam',
        group: 'Yönetici',
      }]
    : [];

  const renderBody = (s: PoolSummary) => {
    const c = clusterOf.get(s.q.id);
    return (
      <>
        <div className="q12-facts">
          <PoolOptFill filled={s.filled} />
          <span className="q12-meta">{s.people.length} kişi · {s.q.fragments?.length || 0} parça · {s.comments} yorum</span>
        </div>
        {q12StatusOf(s) === 'review' && aiCompleted(s.q) && (
          <p className="q12-ainote" role="note">
            <span className="q12-badge is-ai">YZ tamamladı</span>
            <span>Yapay zekânın tamamladığı kısımlar doğrulanmış bilgi değildir; inceleme bitene kadar <b>İnceleniyor</b> olarak kalır.</span>
          </p>
        )}
        {c && (
          <button type="button" className="q12-mhint" onClick={() => p.onOpenClusters(c.id)}>
            <Combine aria-hidden />
            <span>{c.size - 1} başka kayıt aynı soruyu anlatıyor olabilir</span>
            <b>Öneriyi aç <ChevronRight aria-hidden /></b>
          </button>
        )}
        <PoolContribs sum={s} now={now} />
        <QuestionCard
          question={s.q}
          currentUser={p.currentUser}
          isAdmin={p.isAdmin}
          isReconstructing={!!p.reconstructingMap[s.q.id]}
          {...p.card}
        />
      </>
    );
  };

  const renderItem = (s: PoolSummary, extra = '') => {
    const isOpen = s.q.id === selectedId;
    return (
      <li key={s.q.id} data-qid={s.q.id} className={`q12-li ${isOpen ? 'is-open' : ''} ${extra}`}>
        <PoolItemV12 sum={s} now={now} label={kLabel} mode={split ? 'select' : 'expand'} selected={isOpen} onToggle={onToggle} />
        {!split && isOpen && (
          <div className="q12-expand" role="region" aria-label={`Soru ${s.q.questionNumber || ''}`}>
            {renderBody(s)}
            <button type="button" className="q12-btn q12-close" onClick={closeOpen}>
              <ChevronUp aria-hidden />Kapat
            </button>
          </div>
        )}
      </li>
    );
  };

  const empty = !p.loading && list.length === 0 && !pinned;
  const idx = selected ? list.findIndex((s) => s.q.id === selected.q.id) : -1;
  const prev = idx > 0 ? list[idx - 1] : undefined;
  const next = idx >= 0 && idx < list.length - 1 ? list[idx + 1] : undefined;
  const filtersOn = !!stFilter || discOn || appStatusOn || !!q;

  return (
    <div className={`q12-pool ${split && !empty ? 'is-split' : ''}`}>
      <header className="q12-head">
        <div className="q12-head-t">
          <h1 className="q12-title">Soru havuzu</h1>
          <p className="q12-meta">Hatırladığın soru parçalarını birleştir; doğrulanınca çıkmış sorulara geçer.</p>
        </div>
        <div className="q12-head-a">
          <label className="q12-field q12-kurul">
            <span className="sr-only">Kurul</span>
            <select value={p.selectedCommitteeId} onChange={(e) => p.onSelectCommittee(e.target.value)}>
              {p.committees.map((c) => <option key={c.id} value={c.id}>{committeeShortLabel(c)}</option>)}
            </select>
            <ChevronDown aria-hidden className="q12-field-chev" />
          </label>
          <button
            type="button"
            className="q12-btn is-icon is-ghost q12-tool"
            onClick={() => setFeedOpen(true)}
            aria-haspopup="dialog"
            aria-label={activity ? `Havuz etkinliği — ${activity.label}: ${activity.newQ} yeni soru, ${activity.parts} parça` : 'Havuz etkinliği'}
            title="Havuz etkinliği"
          >
            <Activity aria-hidden />
            {activity?.recent && <span className="q12-dot" aria-hidden />}
          </button>
          <button
            type="button"
            className="q12-btn is-icon is-ghost q12-tool"
            onClick={() => p.onOpenClusters()}
            aria-label={mergeCount ? `Öneri taslak havuzu — ${mergeCount} birleştirme önerisi` : 'Öneri taslak havuzu'}
            title="Öneri taslak havuzu: aynı soruyu hatırlayan parçaların birleştirildiği taslaklar"
          >
            <Combine aria-hidden />
            {mergeCount > 0 && <span className="q12-tool-n" aria-hidden>{mergeCount > 99 ? '99+' : mergeCount}</span>}
          </button>
          {adminItems.length > 0 && <ActionMenu items={adminItems} title="Havuz araçları" />}
          <button type="button" className="q12-btn is-pri" onClick={p.onContribute}>
            <Plus aria-hidden />Soru ekle
          </button>
        </div>
      </header>

      {v15 && !p.focusQuestion && (
        <div className="o15-cipler v15-hscroll q15-kisi" role="toolbar" aria-label="Kişisel süzgeç">
          {([['hepsi', 'Hepsi'], ['yanlis', 'Yanlışlarım'], ['kayit', 'Kaydettiklerim'], ['yorum', 'Yorumlu']] as const).map(([id, t]) => (
            <button key={id} type="button" className={`o15-cip${kisi === id ? ' is-on' : ''}`} aria-pressed={kisi === id} onClick={() => setKisi(id)}>{t}</button>
          ))}
        </div>
      )}
      {p.focusQuestion && (
        <div className="q12-band" role="status">
          <Share2 aria-hidden />
          <span>Paylaşılan soru</span>
          <button type="button" className="q12-btn is-sm is-ghost" onClick={p.onClearFocus}>Tüm sorular <ChevronRight aria-hidden /></button>
        </div>
      )}

      <div className="q12-split">
        <section className="q12-panel q12-listp" aria-labelledby="q12-list-h" aria-busy={p.loading || undefined}>
          <div className="q12-panel-h">
            <h2 className="q12-h2" id="q12-list-h">Havuz</h2>
            <span className="q12-meta q12-num q12-grow">{p.loading ? '' : list.length.toLocaleString('tr-TR')}</span>
            <div className="q12-seg" role="group" aria-label="Kapsam">
              <button type="button" className={!p.mineOnly ? 'is-on' : ''} aria-pressed={!p.mineOnly} onClick={() => setMine(false)}>Tümü</button>
              <button type="button" className={p.mineOnly ? 'is-on' : ''} aria-pressed={p.mineOnly} onClick={() => setMine(true)}>
                Katkılarım{p.myCount > 0 && <b className="q12-num">{p.myCount}</b>}
              </button>
            </div>
          </div>

          <div className="q12-filt">
            <label className="q12-field q12-search">
              <Search aria-hidden />
              <input
                type="search"
                data-page-search
                value={q}
                onChange={(e) => onSearch(e.target.value)}
                placeholder="Parçada ara: soru no, hastalık, ilaç"
                aria-label="Havuzda ara"
                enterKeyHint="search"
              />
              {q && <button type="button" className="q12-x" onClick={() => onSearch('')} aria-label="Aramayı temizle"><X aria-hidden /></button>}
            </label>
            <div className="q12-pills" role="group" aria-label="Durum">
              {(['review', 'verified', 'fragment'] as Q12Status[]).map((k) => (
                <button
                  key={k}
                  type="button"
                  className={`q12-pill ${stFilter === k ? 'is-on' : ''}`}
                  aria-pressed={stFilter === k}
                  onClick={() => { setStFilter((cur) => (cur === k ? null : k)); p.setVisibleCount(PAGE); }}
                >
                  <span>{STATUS_TEXT[k]}</span><b className="q12-num">{stCounts[k]}</b>
                </button>
              ))}
              <button
                type="button"
                className={`q12-pill q12-pill-more ${moreOpen || moreCount ? 'is-soft' : ''}`}
                aria-expanded={moreOpen}
                aria-controls="q12-more"
                onClick={() => setMoreOpen((v) => !v)}
              >
                <SlidersHorizontal aria-hidden /><span>Daha fazla</span>{moreCount > 0 && <b className="q12-num">{moreCount}</b>}
              </button>
            </div>
            {moreOpen && (
              <div className="q12-more" id="q12-more">
                <div className="q12-more-row">
                  <span className="q12-label" id="q12-sort-l">Sırala</span>
                  <div className="q12-seg" role="group" aria-labelledby="q12-sort-l">
                    {([['new', 'Yeni'], ['order', 'Soru no'], ['missing', 'Eksik']] as const).map(([id, l]) => (
                      <button key={id} type="button" className={sort === id ? 'is-on' : ''} aria-pressed={sort === id} onClick={() => setSort(id)}>{l}</button>
                    ))}
                  </div>
                </div>
                <div className="q12-more-row">
                  <label className="q12-label" htmlFor="q12-disc">Ders</label>
                  <span className="q12-field q12-grow">
                    <select id="q12-disc" value={p.selectedDiscipline || 'Tümü'} onChange={(e) => p.onSelectDiscipline(e.target.value)}>
                      {discOptions.map((o) => <option key={o.id} value={o.id}>{o.label}{o.count ? ` (${o.count})` : ''}</option>)}
                    </select>
                    <ChevronDown aria-hidden className="q12-field-chev" />
                  </span>
                </div>
                <dl className="q12-stats" aria-label="Kurul hedefi">
                  <div><dt>Onaylı</dt><dd className="q12-num">{p.stats.completed.toLocaleString('tr-TR')}<small> / {p.stats.target}</small></dd></div>
                  <div><dt>Taslak</dt><dd className="q12-num">{p.stats.gathering.toLocaleString('tr-TR')}</dd></div>
                  <div><dt>Boş yuva</dt><dd className="q12-num">{p.stats.empty.toLocaleString('tr-TR')}</dd></div>
                </dl>
              </div>
            )}
            {appStatusOn && (
              <div className="q12-chips">
                <button type="button" className="q12-pill is-soft" onClick={() => p.onSelectStatus('Tümü')} aria-label={`${APP_STATUS_LABEL[p.selectedStatus] || p.selectedStatus} süzgecini kaldır`}>
                  <span>{APP_STATUS_LABEL[p.selectedStatus] || p.selectedStatus}</span><X aria-hidden />
                </button>
              </div>
            )}
            {discOn && !moreOpen && (
              <div className="q12-chips">
                <button type="button" className="q12-pill is-soft" onClick={() => p.onSelectDiscipline('Tümü')} aria-label={`${p.selectedDiscipline} süzgecini kaldır`}>
                  <span>{p.selectedDiscipline}</span><X aria-hidden />
                </button>
              </div>
            )}
          </div>

          {empty ? (
            <div className="q12-empty">
              <h3 className="q12-h2">{p.mineOnly ? 'Henüz katkıda bulunduğun soru yok' : sort === 'missing' ? 'Eksik soru kalmadı' : 'Bu süzgeçlere uyan soru yok'}</h3>
              <p className="q12-meta">{p.mineOnly ? 'Aklında kalan tek bir kelime bile işe yarar; parçayı ekle, kaynaklarla tamamlansın.' : filtersOn ? 'Aramayı kısalt ya da süzgeçleri temizle.' : 'Sıralamayı ya da dersi değiştir.'}</p>
              <div className="q12-empty-a">
                {p.mineOnly && <button type="button" className="q12-btn" onClick={() => setMine(false)}>Tüm soruları göster</button>}
                {!p.mineOnly && filtersOn && <button type="button" className="q12-btn" onClick={clearAll}>Süzgeçleri temizle</button>}
                <button type="button" className="q12-btn is-pri" onClick={p.onContribute}>Soru parçası ekle</button>
              </div>
            </div>
          ) : (
            <>
              <ul className="q12-list" ref={listRef} onKeyDown={onListKey}>
                {p.loading
                  ? [0, 1, 2, 3, 4].map((i) => <li key={i} className="q12-li"><PoolItemSkeleton /></li>)
                  : (
                    <>
                      {pinned && renderItem(pinned, 'is-pinned')}
                      {shown.map((s) => renderItem(s))}
                    </>
                  )}
              </ul>
              {hasMore && (
                <div ref={sentinel} className="q12-listfoot">
                  <button type="button" className="q12-btn is-sm" onClick={() => p.setVisibleCount((v) => v + PAGE)}>
                    {(list.length - p.visibleCount).toLocaleString('tr-TR')} soru daha
                  </button>
                </div>
              )}
              {!p.loading && !hasMore && list.length > PAGE && <p className="q12-listfoot q12-meta">Hepsi bu kadar · {list.length.toLocaleString('tr-TR')} soru</p>}
            </>
          )}
        </section>

        {split && !empty && (
          <section ref={detailRef} className="q12-detail" aria-label="Açık soru">
            {p.loading ? (
              <div className="q12-dskel" aria-hidden><span className="q12-skel" /><span className="q12-skel" /><span className="q12-skel" /></div>
            ) : selected ? (
              <article className="q12-det" key={selected.q.id}>
                <header className="q12-det-h">
                  <div className="q12-grow">
                    <h2 className="q12-h2">Soru {selected.q.questionNumber || '—'}{pinned ? <span className="q12-meta"> · listede değil</span> : null}</h2>
                    <span className="q12-det-m">
                      <StatusBadge s={q12StatusOf(selected)} />
                      <span className="q12-meta q12-clamp1">{[kLabel, selected.q.discipline, selected.q.topic && selected.q.topic !== selected.q.discipline ? selected.q.topic : ''].filter(Boolean).join(' · ')}</span>
                    </span>
                  </div>
                  <span className="q12-det-nav">
                    {idx >= 0 && <span className="q12-meta q12-num">{idx + 1}/{list.length}</span>}
                    <button type="button" className="q12-btn is-icon is-sm is-ghost" disabled={!prev} onClick={() => prev && openQuestion(prev.q.id)} aria-label="Önceki soru"><ChevronLeft aria-hidden /></button>
                    <button type="button" className="q12-btn is-icon is-sm is-ghost" disabled={!next} onClick={() => next && openQuestion(next.q.id)} aria-label="Sonraki soru"><ChevronRight aria-hidden /></button>
                  </span>
                </header>
                {renderBody(selected)}
              </article>
            ) : (
              <p className="q12-meta">Soldan bir soru seç.</p>
            )}
          </section>
        )}
      </div>

      <PoolLiveFeed
        open={feedOpen}
        onClose={() => setFeedOpen(false)}
        sums={allSums}
        now={now}
        activity={activity}
        onOpen={(id) => { setFeedOpen(false); openQuestion(id); }}
      />
    </div>
  );
};
