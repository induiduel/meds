import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { Activity, ChevronLeft, ChevronRight, ChevronUp, Combine, LayoutGrid, Plus, Share2 } from 'lucide-react';
import type { Committee, QuestionItem } from '../../types';
import type { AppUser } from '../../services/auth';
import { QuestionCard } from '../QuestionCard';
import { committeeShortLabel } from '../QuickAddHero';
import { PageToolbar, FilterPills, ToolbarChip } from '../ui/PageToolbar';
import { ActionMenu, ActionItem } from '../ui/ActionMenu';
import { useAppearance } from '../../utils/appearance';
import { DAY, PoolSegment, PoolSummary, isMissing, statusOf, summarize } from './poolModel';
import { PoolOptFill, PoolRow, PoolRowSkeleton, PoolStatusMark, PoolTag } from './PoolRow';
import { PoolContribs } from './PoolContribs';
import { PoolLiveFeed, usePoolActivity } from './PoolLiveFeed';
import { poolDisciplineOptions, useMedia, usePoolClusters } from './poolHooks';
import { PoolV12 } from '../v12/PoolV12';
import '../../styles/pool.css';

/**
 * Soru havuzu (v12, sade): tek gruplu satır listesi; seçili soru tartışmasız belli.
 *  - Telefon/tablet ve 'akis' modu: satıra dokununca soru yerinde açılır (satır başlık olur, altta "Kapat").
 *  - 'odak' ≥1024 · 'pano' ≥1180: liste + ayrıntı bölmesi; bölmenin başlığı hangi sorunun açık olduğunu söyler.
 *  - İkincil bilgi sayfada değil: etkinlik/canlı akış "Etkinlik" düğmesinde (Sheet), birleştirme önerileri
 *    "Öneri taslak havuzu" düğmesinin rozetinde, havuz sayıları Süzgeç sayfasında.
 *  - Durum ve işleyiciler App.tsx'te kalır; bu bileşen yalnız gösterim, sıralama ve seçim durumunu tutar.
 */

type QCProps = React.ComponentProps<typeof QuestionCard>;
export type PoolCardHandlers = Omit<QCProps, 'question' | 'currentUser' | 'isAdmin' | 'isReconstructing'>;

const STATUS_LABEL: Record<string, string> = { completed: 'Doğrulanan', gathering: 'Taslak', empty: 'Boş yuva' };
const SEG_KEY = 'medsoru_pool_segment';
const PAGE = 30;

export interface PoolViewProps {
  loading: boolean;
  /** Kuruldaki bağımsız soruların tamamı (etkinlik ve süzgeç seçenekleri için) */
  allQuestions: QuestionItem[];
  /** App süzgeçlerinden (branş, durum, arama ya da "benim") geçen sorular */
  poolQuestions: QuestionItem[];
  focusQuestion?: QuestionItem;
  onClearFocus: () => void;
  visibleCount: number;
  setVisibleCount: React.Dispatch<React.SetStateAction<number>>;

  committees: Committee[];
  selectedCommitteeId: string;
  onSelectCommittee: (id: string) => void;
  selectedDiscipline: string;
  onSelectDiscipline: (d: string) => void;
  selectedStatus: string;
  onSelectStatus: (s: string) => void;
  searchQuery: string;
  onSearchChange: (q: string) => void;
  mineOnly: boolean;
  onSetMineOnly: (v: boolean) => void;
  myCount: number;

  stats: { target: number; gathered: number; completed: number; gathering: number; empty: number };
  isAdmin: boolean;
  onGenerateSlots: () => void;
  isGeneratingSlots: boolean;
  /** Öneri taslak havuzunu aç (kümeyle: doğrudan o kümenin ayrıntısı) */
  onOpenClusters: (clusterId?: string) => void;
  onContribute: () => void;

  currentUser: AppUser | null;
  reconstructingMap: Record<string, boolean>;
  card: PoolCardHandlers;
}

const readSeg = (): Exclude<PoolSegment, 'mine'> => {
  try {
    const v = localStorage.getItem(SEG_KEY);
    if (v === 'new' || v === 'order' || v === 'missing') return v;
  } catch { /* yoksay */ }
  return 'new';
};

const byNumber = (a: PoolSummary, b: PoolSummary) => {
  const na = a.q.questionNumber || Number.MAX_SAFE_INTEGER;
  const nb = b.q.questionNumber || Number.MAX_SAFE_INTEGER;
  return na - nb;
};
const byRecent = (a: PoolSummary, b: PoolSummary) => b.lastAt - a.lastAt || byNumber(a, b);

/** Üst çubuk + yapışkan araç çubuğunun alt kenarı (kaydırma hedefi bunun altında kalır) */
function stickyBottom(): number {
  const sh = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--sh-top-h')) || 52;
  const bar = document.querySelector<HTMLElement>('.pv-root .pt-root');
  if (!bar) return sh;
  const cs = getComputedStyle(bar);
  if (cs.position !== 'sticky' && cs.position !== 'fixed') return sh;
  return Math.max(sh, (parseFloat(cs.top) || sh) + bar.offsetHeight);
}

/** Öğeyi yapışkan başlıkların altına getirir. top: başını hizala; değilse yalnız görünmüyorsa en yakın kenara kaydır. */
function bringIntoView(el: Element | null, mode: 'top' | 'nearest') {
  if (!el) return;
  const r = el.getBoundingClientRect();
  const off = stickyBottom() + 8;
  const vh = window.innerHeight;
  let dy = 0;
  if (mode === 'top') dy = r.top - off;
  else if (r.top < off) dy = r.top - off;
  else if (r.bottom > vh - 12) dy = Math.min(r.bottom - (vh - 12), r.top - off);
  if (Math.abs(dy) < 2) return;
  const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  window.scrollTo({ top: Math.max(0, window.scrollY + dy), behavior: reduce ? 'auto' : 'smooth' });
}

/** v12 'Net' görünümünde ayrı yapı (components/v12/PoolV12); v10/v11 aşağıdaki klasik görünümü çizer. */
export const PoolView: React.FC<PoolViewProps> = (p) =>
  useAppearance().design === 'v12' ? <PoolV12 {...p} /> : <PoolViewClassic {...p} />;

const PoolViewClassic: React.FC<PoolViewProps> = (p) => {
  const { layout } = useAppearance();
  const wideOdak = useMedia('(min-width: 1024px)');
  const widePano = useMedia('(min-width: 1180px)');
  const split = layout === 'odak' ? wideOdak : layout === 'pano' ? widePano : false;

  // Göreli zamanlar dakikada bir tazelenir
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    const t = window.setInterval(() => setNow(Date.now()), 60_000);
    return () => window.clearInterval(t);
  }, []);

  // Açık/seçili soru; pinnedId: listede olmayan (ör. etkinlikten açılan) soru
  const [openId, setOpenId] = useState<string | undefined>(p.focusQuestion?.id);
  const [pinnedId, setPinnedId] = useState<string | undefined>();
  const revealRef = useRef<string | undefined>(p.focusQuestion?.id);
  useEffect(() => {
    if (p.focusQuestion) { setOpenId(p.focusQuestion.id); revealRef.current = p.focusQuestion.id; }
  }, [p.focusQuestion?.id]);

  const [segLocal, setSegLocal] = useState(readSeg);
  const segment: PoolSegment = p.mineOnly ? 'mine' : segLocal;
  const changeSegment = (s: PoolSegment) => {
    if (s === 'mine') p.onSetMineOnly(true);
    else {
      if (p.mineOnly) p.onSetMineOnly(false);
      setSegLocal(s);
      try { localStorage.setItem(SEG_KEY, s); } catch { /* yoksay */ }
    }
    p.setVisibleCount(PAGE);
    if (!split) setOpenId(undefined);
    setPinnedId(undefined);
  };

  // Özetler: kurulun tamamı bir kez; süzülmüş liste aynı nesneleri paylaşır
  const allSums = useMemo(() => p.allQuestions.map(summarize), [p.allQuestions]);
  const sumById = useMemo(() => new Map(allSums.map((s) => [s.q.id, s])), [allSums]);
  const sumOf = useCallback((q: QuestionItem) => {
    const s = sumById.get(q.id);
    return s && s.q === q ? s : summarize(q);
  }, [sumById]);
  const poolSums = useMemo(() => p.poolQuestions.map(sumOf), [p.poolQuestions, sumOf]);

  const counts = useMemo(() => ({
    fresh: poolSums.filter((s) => s.lastAt > 0 && now - s.lastAt < DAY).length,
    missing: poolSums.filter(isMissing).length,
  }), [poolSums, now]);

  const list = useMemo(() => {
    if (p.focusQuestion) return [sumOf(p.focusQuestion)];
    if (segment === 'order') return [...poolSums].sort(byNumber);
    if (segment === 'missing') return poolSums.filter(isMissing).sort(byNumber);
    return [...poolSums].sort(byRecent);
  }, [poolSums, segment, p.focusQuestion, sumOf]);
  const shown = list.slice(0, p.visibleCount);
  const hasMore = !p.focusQuestion && list.length > p.visibleCount;
  const inList = useCallback((id?: string) => !!id && list.some((s) => s.q.id === id), [list]);

  const pinned = pinnedId && pinnedId === openId && !inList(pinnedId) ? sumById.get(pinnedId) : undefined;
  const selectedId = split ? (inList(openId) || pinned ? openId : shown[0]?.q.id) : openId;
  const selected = selectedId ? list.find((s) => s.q.id === selectedId) || sumById.get(selectedId) : undefined;

  const { setVisibleCount } = p;
  /** Bir soruyu aç/seç; gerekirse listede o soruya kadar yükle, listede yoksa en üste iğnele, görünür alana getir */
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
    // Kapatınca satıra geri dön (uzun karttan sonra kaybolmasın) ve odağı satıra ver
    window.requestAnimationFrame(() => {
      const row = document.querySelector<HTMLElement>(`.pv-root [data-row="${CSS.escape(id || '')}"]`);
      if (row) { bringIntoView(row, 'nearest'); row.focus({ preventScroll: true }); }
    });
  }, [openId]);

  // Açılan/seçilen soru görünür alana gelir; bölmede ayrıntı en üstten başlar
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
      if (!li) return;
      bringIntoView(split ? li.querySelector('.pv-row') : li, split ? 'nearest' : 'top');
    });
    return () => window.cancelAnimationFrame(raf);
  });

  // Klavye: ↑/↓ satırlar arasında gezer (bölmede seçimi de taşır)
  const onListKey = (e: React.KeyboardEvent<HTMLUListElement>) => {
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
    const rows = Array.from(e.currentTarget.querySelectorAll<HTMLButtonElement>('.pv-row[data-row]'));
    const i = rows.findIndex((r) => r === document.activeElement);
    if (i < 0) return;
    const nxt = rows[e.key === 'ArrowDown' ? i + 1 : i - 1];
    if (!nxt) return;
    e.preventDefault();
    nxt.focus();
    if (split && nxt.dataset.row) { setOpenId(nxt.dataset.row); setPinnedId(undefined); }
  };

  // Kaydırınca otomatik yükleme; IntersectionObserver yoksa düğme kalır
  const sentinel = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = sentinel.current;
    if (!el || !hasMore || typeof IntersectionObserver === 'undefined') return;
    const io = new IntersectionObserver((ents) => {
      if (ents.some((e) => e.isIntersecting)) setVisibleCount((v) => v + PAGE);
    }, { rootMargin: '600px 0px' });
    io.observe(el);
    return () => io.disconnect();
  }, [hasMore, shown.length, setVisibleCount]);

  const activity = usePoolActivity(allSums, now);
  const [feedOpen, setFeedOpen] = useState(false);

  const committee = p.committees.find((c) => c.id === p.selectedCommitteeId);

  // Ders süzgeci kurulun gerçek derslerinden (sayılarıyla)
  const discOptions = useMemo(() => poolDisciplineOptions(p.allQuestions), [p.allQuestions]);
  const { selectedDiscipline, onSelectDiscipline } = p;
  useEffect(() => {
    // Kayıtlı süzgeç bu kurulda yoksa (ör. eski "Patoloji") liste boş kalmasın
    if (!p.loading && p.allQuestions.length && selectedDiscipline && selectedDiscipline !== 'Tümü' && !discOptions.some((o) => o.id === selectedDiscipline)) onSelectDiscipline('Tümü');
  }, [discOptions, selectedDiscipline, onSelectDiscipline, p.loading, p.allQuestions.length]);

  // Birleştirme önerileri (sunucu motoru: aynı soruyu anlatan kayıtlar). Soru → küme eşlemi ayrıntı için.
  const { clusters, clusterOf } = usePoolClusters(p.selectedCommitteeId, p.allQuestions.length);

  const chips: ToolbarChip[] = [];
  if (p.selectedDiscipline && p.selectedDiscipline !== 'Tümü') chips.push({ id: 'd', label: p.selectedDiscipline, onRemove: () => p.onSelectDiscipline('Tümü') });
  if (p.selectedStatus && p.selectedStatus !== 'Tümü') chips.push({ id: 's', label: STATUS_LABEL[p.selectedStatus] || p.selectedStatus, onRemove: () => p.onSelectStatus('Tümü') });

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

  const filters = (
    <>
      <dl className="pv-fsum" aria-label="Havuz durumu">
        <div><dt>Doğrulanan</dt><dd>{p.stats.completed.toLocaleString('tr-TR')}<small> / {p.stats.target}</small></dd></div>
        <div><dt>Taslak</dt><dd>{p.stats.gathering.toLocaleString('tr-TR')}</dd></div>
        <div><dt>Boş yuva</dt><dd>{p.stats.empty.toLocaleString('tr-TR')}</dd></div>
      </dl>
      <fieldset className="pt-fgroup">
        <legend>Kurul</legend>
        <label className="sr-only" htmlFor="pool-committee">Kurul</label>
        <select id="pool-committee" value={p.selectedCommitteeId} onChange={(e) => p.onSelectCommittee(e.target.value)}>
          {p.committees.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
        </select>
      </fieldset>
      <FilterPills<string>
        label="Durum"
        value={p.selectedStatus || 'Tümü'}
        onChange={p.onSelectStatus}
        options={[
          { id: 'Tümü', label: 'Tümü' },
          { id: 'completed', label: 'Doğrulanan', count: p.stats.completed },
          { id: 'gathering', label: 'Taslak', count: p.stats.gathering },
        ]}
      />
      <FilterPills<string>
        label="Disiplin"
        value={p.selectedDiscipline || 'Tümü'}
        onChange={p.onSelectDiscipline}
        options={discOptions}
      />
    </>
  );

  const renderBody = (s: PoolSummary) => (
    <>
      <div className="pv-facts">
        <PoolOptFill filled={s.filled} />
        <span>{s.people.length} kişi · {s.q.fragments?.length || 0} parça · {s.comments} yorum</span>
      </div>
      <MergeHint c={clusterOf.get(s.q.id)} onOpen={p.onOpenClusters} />
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

  /** Telefon: satır + yerinde açılan gövde + alt "Kapat" */
  const renderItem = (s: PoolSummary, extra = '') => {
    const isOpen = s.q.id === selectedId;
    const exId = `pv-x-${s.q.id}`;
    return (
      <li key={s.q.id} data-qid={s.q.id} className={`pv-li ${isOpen ? 'is-open' : ''} ${extra}`}>
        <PoolRow sum={s} now={now} mode={split ? 'select' : 'expand'} selected={isOpen} onToggle={onToggle} />
        {!split && isOpen && (
          <div id={exId} className="pv-expand" role="region" aria-label={`Soru ${s.q.questionNumber || ''}`}>
            {renderBody(s)}
            <button type="button" className="pv-close" onClick={closeOpen}>
              <ChevronUp aria-hidden />Soru {s.q.questionNumber || ''} kapat
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
  const mergeCount = clusters.length;

  return (
    <div className={`pv-root ${split ? 'is-split' : ''}`}>
      <PageToolbar<PoolSegment>
        title="Soru havuzu"
        count={p.loading ? undefined : `${committee ? committeeShortLabel(committee) + ' · ' : ''}${p.poolQuestions.length.toLocaleString('tr-TR')}`}
        search={{ value: p.searchQuery, onChange: p.onSearchChange, placeholder: 'Soru no, hastalık, ilaç, kelime' }}
        segments={{
          label: 'Sıralama',
          value: segment,
          onChange: changeSegment,
          options: [
            { id: 'new', label: 'Yeni', count: counts.fresh || undefined },
            { id: 'order', label: 'Sıra' },
            { id: 'missing', label: 'Eksik', count: counts.missing || undefined },
            { id: 'mine', label: 'Benim', count: p.myCount || undefined },
          ],
        }}
        filters={filters}
        filterCount={chips.length}
        filterTitle="Havuz süzgeci"
        chips={chips}
        onClearChips={() => { p.onSelectDiscipline('Tümü'); p.onSelectStatus('Tümü'); }}
        tools={
          <>
            <button
              type="button"
              className="pt-icon pv-tool"
              onClick={() => setFeedOpen(true)}
              aria-haspopup="dialog"
              aria-label={activity ? `Havuz etkinliği — ${activity.label}: ${activity.newQ} yeni soru, ${activity.parts} parça` : 'Havuz etkinliği'}
              title="Havuz etkinliği"
            >
              <Activity aria-hidden />
              {activity?.recent && <span className="pv-tool-dot" aria-hidden />}
            </button>
            <button
              type="button"
              className="pt-icon pv-tool"
              onClick={() => p.onOpenClusters()}
              aria-label={mergeCount ? `Öneri taslak havuzu — ${mergeCount} birleştirme önerisi` : 'Öneri taslak havuzu'}
              title="Öneri taslak havuzu: aynı soruyu hatırlayan parçaların birleştirildiği taslaklar"
            >
              <Combine aria-hidden />
              {mergeCount > 0 && <span className="pv-tool-n" aria-hidden>{mergeCount > 99 ? '99+' : mergeCount}</span>}
            </button>
            <button type="button" className="pt-icon pv-tool pv-tool-add" onClick={p.onContribute} aria-label="Soru ekle" title="Soru ekle">
              <Plus aria-hidden />
            </button>
            {adminItems.length > 0 && <ActionMenu items={adminItems} title="Havuz araçları" />}
          </>
        }
      />

      {p.focusQuestion && (
        <div className="pv-band" role="status">
          <Share2 aria-hidden />
          <span>Paylaşılan soru</span>
          <button type="button" onClick={p.onClearFocus}>Tüm sorular <ChevronRight aria-hidden /></button>
        </div>
      )}

      {empty ? (
        <div className="pv-empty">
          <h3>{p.mineOnly ? 'Henüz katkıda bulunduğun soru yok' : segment === 'missing' ? 'Eksik soru kalmadı' : 'Bu süzgeçlere uyan soru yok'}</h3>
          <p>{p.mineOnly ? 'Aklında kalan tek bir kelime bile işe yarar; parçayı ekle, kaynaklarla tamamlansın.' : p.searchQuery ? 'Aramayı kısalt ya da süzgeçleri temizle.' : 'Süzgeçten durumu ya da dersi değiştir.'}</p>
          <div className="pv-empty-a">
            {p.mineOnly && <button type="button" className="ui-btn" onClick={() => changeSegment('new')}>Tüm soruları göster</button>}
            {!p.mineOnly && p.searchQuery && <button type="button" className="ui-btn" onClick={() => p.onSearchChange('')}>Aramayı temizle</button>}
            {!p.mineOnly && !p.searchQuery && chips.length > 0 && <button type="button" className="ui-btn" onClick={() => { p.onSelectDiscipline('Tümü'); p.onSelectStatus('Tümü'); }}>Süzgeçleri temizle</button>}
            <button type="button" className="ui-btn is-primary" onClick={p.onContribute}>Soru parçası ekle</button>
          </div>
        </div>
      ) : (
        <div className="pv-body">
          <section className="pv-list" aria-label="Sorular" aria-busy={p.loading || undefined}>
            <ul className="pv-ul" ref={listRef} onKeyDown={onListKey}>
              {p.loading
                ? [0, 1, 2, 3, 4, 5].map((i) => <li key={i} className="pv-li"><PoolRowSkeleton /></li>)
                : (
                  <>
                    {pinned && renderItem(pinned, 'is-pinned')}
                    {shown.map((s) => renderItem(s))}
                  </>
                )}
            </ul>
            {hasMore && (
              <div ref={sentinel} className="pv-more">
                <button type="button" className="ui-btn" onClick={() => p.setVisibleCount((v) => v + PAGE)}>
                  {(list.length - p.visibleCount).toLocaleString('tr-TR')} soru daha
                </button>
              </div>
            )}
            {!p.loading && !hasMore && list.length > PAGE && <p className="pv-end">Hepsi bu kadar · {list.length.toLocaleString('tr-TR')} soru</p>}
          </section>

          {split && (
            <section ref={detailRef} className="pv-detail" aria-label="Açık soru">
              {p.loading ? (
                <div className="pv-dskel" aria-hidden><span className="ui-skel" /><span className="ui-skel" /><span className="ui-skel" /></div>
              ) : selected ? (
                <article className="pv-det" key={selected.q.id}>
                  <header className="pv-dh">
                    <span className="pv-no is-on" aria-hidden>{selected.q.questionNumber || '—'}</span>
                    <div className="pv-dh-t">
                      <h2>Soru {selected.q.questionNumber || '—'}{pinned ? <small> · listede değil</small> : null}</h2>
                      <span className="pv-dh-m">
                        <PoolTag discipline={selected.q.discipline} />
                        <PoolStatusMark status={statusOf(selected)} />
                        {selected.q.topic && selected.q.topic !== selected.q.discipline && <span className="pv-dh-topic">{selected.q.topic}</span>}
                      </span>
                    </div>
                    <span className="pv-dh-nav">
                      {idx >= 0 && <span className="pv-dh-pos">{idx + 1}/{list.length}</span>}
                      <button type="button" className="pv-nav" disabled={!prev} onClick={() => prev && openQuestion(prev.q.id)} aria-label="Önceki soru"><ChevronLeft aria-hidden /></button>
                      <button type="button" className="pv-nav" disabled={!next} onClick={() => next && openQuestion(next.q.id)} aria-label="Sonraki soru"><ChevronRight aria-hidden /></button>
                    </span>
                  </header>
                  {renderBody(selected)}
                </article>
              ) : (
                <p className="pv-note">Soldan bir soru seç.</p>
              )}
            </section>
          )}
        </div>
      )}

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

/** Bu kayıt bir birleştirme önerisinin üyesiyse: kaç kayıtla aynı soruyu anlattığı + öneriyi aç */
const MergeHint: React.FC<{ c?: { id: string; size: number }; onOpen: (id?: string) => void }> = ({ c, onOpen }) =>
  c ? (
    <button type="button" className="pv-mhint" onClick={() => onOpen(c.id)}>
      <Combine aria-hidden />
      <span>{c.size - 1} başka kayıt aynı soruyu anlatıyor olabilir</span>
      <b>Öneriyi aç <ChevronRight aria-hidden /></b>
    </button>
  ) : null;
