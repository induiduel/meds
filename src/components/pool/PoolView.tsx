import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Combine, LayoutGrid, Plus, Share2 } from 'lucide-react';
import { ApiService } from '../../services/api';
import type { Committee, QuestionItem } from '../../types';
import type { AppUser } from '../../services/auth';
import { QuestionCard } from '../QuestionCard';
import { committeeShortLabel } from '../QuickAddHero';
import { PageToolbar, FilterPills, ToolbarChip } from '../ui/PageToolbar';
import { ActionMenu, ActionItem } from '../ui/ActionMenu';
import { useAppearance } from '../../utils/appearance';
import { DAY, HOUR, PoolSegment, PoolSummary, activityIn, isMissing, summarize } from './poolModel';
import { PoolRow, PoolRowSkeleton } from './PoolRow';
import { PoolContribs } from './PoolContribs';
import { PoolLiveFeed } from './PoolLiveFeed';
import '../../styles/pool.css';

/**
 * Soru havuzu (v11): kompakt satır listesi + yerinde açılan soru kartı; geniş ekranda liste + ayrıntı bölmesi.
 *  - Görüntüleme modu (Ayarlar): 'akis' tek sütun · 'odak' ≥1024 bölmeli · 'pano' ≥1180 bölmeli; telefonda hep tek sütun.
 *  - ≥1440 bölmeli görünümde sağda "Canlı akış" (tüm sorulardaki son katkılar).
 *  - Durum ve işleyiciler App.tsx'te kalır; bu bileşen yalnız gösterim, sıralama ve seçim durumunu tutar.
 */

type QCProps = React.ComponentProps<typeof QuestionCard>;
export type PoolCardHandlers = Omit<QCProps, 'question' | 'currentUser' | 'isAdmin' | 'isReconstructing'>;

const GENERIC_DISC = /^(belirtilmedi|genel|belirsiz|)$/i;
const STATUS_LABEL: Record<string, string> = { completed: 'Doğrulanan', gathering: 'Taslak', empty: 'Boş yuva' };
const SEG_KEY = 'medsoru_pool_segment';
const PAGE = 30;

export interface PoolViewProps {
  loading: boolean;
  /** Kuruldaki bağımsız soruların tamamı (etkinlik bandı ve canlı akış için) */
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

function useMedia(query: string): boolean {
  const get = () => typeof window !== 'undefined' && !!window.matchMedia?.(query).matches;
  const [m, setM] = useState(get);
  useEffect(() => {
    const mq = window.matchMedia?.(query);
    if (!mq) return;
    const on = () => setM(mq.matches);
    on();
    mq.addEventListener?.('change', on);
    return () => mq.removeEventListener?.('change', on);
  }, [query]);
  return m;
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

export const PoolView: React.FC<PoolViewProps> = (p) => {
  const { layout } = useAppearance();
  const wideOdak = useMedia('(min-width: 1024px)');
  const widePano = useMedia('(min-width: 1180px)');
  const xwide = useMedia('(min-width: 1440px)');
  const split = layout === 'odak' ? wideOdak : layout === 'pano' ? widePano : false;
  const showFeed = split && xwide;

  // Göreli zamanlar dakikada bir tazelenir
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    const t = window.setInterval(() => setNow(Date.now()), 60_000);
    return () => window.clearInterval(t);
  }, []);

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

  // Açık/seçili soru (telefonda yerinde açılan, geniş ekranda sağ bölmedeki)
  const [openId, setOpenId] = useState<string | undefined>(p.focusQuestion?.id);
  useEffect(() => {
    if (p.focusQuestion) setOpenId(p.focusQuestion.id);
  }, [p.focusQuestion?.id]);
  const selectedId = split ? (openId && (list.some((s) => s.q.id === openId) || sumById.has(openId)) ? openId : shown[0]?.q.id) : openId;
  const selected = selectedId ? list.find((s) => s.q.id === selectedId) || sumById.get(selectedId) : undefined;
  const onToggle = useCallback((id: string) => {
    setOpenId((cur) => (split ? id : cur === id ? undefined : id));
  }, [split]);

  // Kaydırınca otomatik yükleme; IntersectionObserver yoksa düğme kalır
  const sentinel = useRef<HTMLDivElement>(null);
  const { setVisibleCount } = p;
  useEffect(() => {
    const el = sentinel.current;
    if (!el || !hasMore || typeof IntersectionObserver === 'undefined') return;
    const io = new IntersectionObserver((ents) => {
      if (ents.some((e) => e.isIntersecting)) setVisibleCount((v) => v + PAGE);
    }, { rootMargin: '600px 0px' });
    io.observe(el);
    return () => io.disconnect();
  }, [hasMore, shown.length, setVisibleCount]);

  // Etkinlik bandı: son 1 saat, yoksa son 24 saat
  const activity = useMemo(() => {
    const h = activityIn(allSums, HOUR, now);
    if (h.parts || h.newQ) return { label: 'Son 1 saat', ...h };
    const d = activityIn(allSums, DAY, now);
    if (d.parts || d.newQ) return { label: 'Son 24 saat', ...d };
    return null;
  }, [allSums, now]);

  const committee = p.committees.find((c) => c.id === p.selectedCommitteeId);

  // Ders süzgeci kurulun gerçek derslerinden (sayılarıyla); eski sabit liste ("Patoloji", "Dahiliye") veriyle eşleşmiyordu
  const discOptions = useMemo(() => {
    const m = new Map<string, number>();
    for (const q of p.allQuestions) {
      const d = (q.discipline || '').trim();
      if (d && !GENERIC_DISC.test(d)) m.set(d, (m.get(d) || 0) + 1);
    }
    return [{ id: 'Tümü', label: 'Tümü' }, ...[...m].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'tr')).map(([d, c]) => ({ id: d, label: d, count: c }))];
  }, [p.allQuestions]);
  const { selectedDiscipline, onSelectDiscipline } = p;
  useEffect(() => {
    // Kayıtlı süzgeç bu kurulda yoksa (ör. eski "Patoloji") liste boş kalmasın
    if (!p.loading && p.allQuestions.length && selectedDiscipline && selectedDiscipline !== 'Tümü' && !discOptions.some((o) => o.id === selectedDiscipline)) onSelectDiscipline('Tümü');
  }, [discOptions, selectedDiscipline, onSelectDiscipline, p.loading, p.allQuestions.length]);

  // Birleştirme önerileri (sunucu motoru: aynı soruyu anlatan kayıtlar). Soru → küme eşlemi satır/ayrıntı için.
  const [clusters, setClusters] = useState<{ id: string; committeeId: string; sourceQuestionIds: string[]; mergedQuestionCount: number; clusterTitle: string }[]>([]);
  useEffect(() => {
    let alive = true;
    const t = window.setTimeout(() => {
      ApiService.getPoolQuestionClusters()
        .then((list: any[]) => { if (alive) setClusters((list || []).filter((c) => c.committeeId === p.selectedCommitteeId && c.mergedQuestionCount >= 2)); })
        .catch(() => {});
    }, 400);
    return () => { alive = false; window.clearTimeout(t); };
  }, [p.selectedCommitteeId, p.allQuestions.length]);
  const clusterOf = useMemo(() => {
    const m = new Map<string, { id: string; size: number }>();
    for (const c of clusters) for (const qid of c.sourceQuestionIds || []) m.set(qid, { id: c.id, size: c.mergedQuestionCount });
    return m;
  }, [clusters]);

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
      <div className="pv-fsum" aria-label="Havuz durumu">
        <span><b>{p.stats.completed}</b> / {p.stats.target} doğrulandı</span>
        <span><b>{p.stats.gathering}</b> taslak</span>
        <span><b>{p.stats.empty}</b> boş yuva</span>
      </div>
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

  const detailId = 'pv-detail';
  const renderCard = (s: PoolSummary) => (
    <QuestionCard
      question={s.q}
      currentUser={p.currentUser}
      isAdmin={p.isAdmin}
      isReconstructing={!!p.reconstructingMap[s.q.id]}
      {...p.card}
    />
  );

  const empty = !p.loading && list.length === 0;

  return (
    <div className={`pv-root ${split ? 'is-split' : ''} ${showFeed ? 'has-feed' : ''}`}>
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
            <button type="button" className="pt-icon" onClick={() => p.onOpenClusters()} aria-label="Öneri taslak havuzu" title="Öneri taslak havuzu: aynı soruyu hatırlayan parçaların birleştirildiği taslaklar">
              <Combine aria-hidden />
            </button>
            <button type="button" className="pt-icon pv-tool-add" onClick={p.onContribute} aria-label="Soru ekle" title="Soru ekle">
              <Plus aria-hidden />
            </button>
            {adminItems.length > 0 && <ActionMenu items={adminItems} title="Havuz araçları" />}
          </>
        }
      />

      {activity && !p.focusQuestion && (
        <button
          type="button"
          className="pv-pulse"
          onClick={() => { changeSegment('new'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
          aria-label={`${activity.label}: ${activity.newQ} yeni soru, ${activity.parts} parça, ${activity.people} katkıcı. Yeni sorulara geç`}
        >
          <span className="pv-dot" aria-hidden />
          <span className="pv-pulse-t"><b>{activity.label}:</b> {activity.newQ} yeni soru, {activity.parts} parça, {activity.people} katkıcı</span>
          <span className="pv-pulse-go" aria-hidden>Gör <ChevronRight /></span>
        </button>
      )}

      {clusters.length > 0 && !p.focusQuestion && (
        <button type="button" className="pv-pulse pv-merge" onClick={() => p.onOpenClusters()} aria-label={`${clusters.length} birleştirme önerisi: aynı soruyu anlatan kayıtlar. Önerileri aç`}>
          <Combine aria-hidden className="pv-merge-i" />
          <span className="pv-pulse-t"><b>{clusters.length} birleştirme önerisi:</b> {clusters.reduce((t, c) => t + c.mergedQuestionCount, 0)} kayıt aynı soruları anlatıyor olabilir</span>
          <span className="pv-pulse-go" aria-hidden>Aç <ChevronRight /></span>
        </button>
      )}

      {p.focusQuestion && (
        <div className="ms-shared-band" role="status">
          <Share2 className="w-4 h-4 shrink-0" aria-hidden />
          <span className="min-w-0 flex-1">Paylaşılan soru gösteriliyor</span>
          <button type="button" onClick={p.onClearFocus} className="ms-btn is-ghost is-sm">Tüm sorular <ChevronRight className="w-4 h-4" /></button>
        </div>
      )}

      {empty ? (
        <div className="pv-empty">
          <h3>{p.mineOnly ? 'Henüz katkıda bulunduğun soru yok' : segment === 'missing' ? 'Eksik soru kalmadı' : 'Bu süzgeçlere uyan soru yok'}</h3>
          <p>{p.mineOnly ? 'Aklında kalan tek bir kelime bile işe yarar; parçayı ekle, kaynaklarla tamamlansın.' : 'Branşı ya da durumu değiştir, veya aramayı kısalt.'}</p>
          <div className="pv-empty-a">
            {p.mineOnly && <button type="button" className="ui-btn" onClick={() => changeSegment('new')}>Tüm soruları göster</button>}
            <button type="button" className="ui-btn is-primary" onClick={p.onContribute}>Soru parçası ekle</button>
          </div>
        </div>
      ) : (
        <div className="pv-body">
          <section className="pv-list" aria-label="Sorular" aria-busy={p.loading || undefined}>
            <ul className="pv-ul">
              {p.loading
                ? [0, 1, 2, 3, 4, 5].map((i) => <li key={i}><PoolRowSkeleton /></li>)
                : shown.map((s) => {
                    const isOpen = split ? s.q.id === selectedId : s.q.id === openId;
                    const exId = `pv-x-${s.q.id}`;
                    return (
                      <li key={s.q.id} data-qid={s.q.id} className={`pv-li scroll-mt-20 ${isOpen && !split ? 'is-open' : ''}`}>
                        <PoolRow sum={s} now={now} mode={split ? 'select' : 'expand'} open={isOpen} controls={split ? detailId : exId} onToggle={onToggle} similar={clusterOf.get(s.q.id)?.size} />
                        {!split && isOpen && (
                          <div id={exId} className="pv-expand" role="region" aria-label={`Soru ${s.q.questionNumber || ''} ayrıntısı`}>
                            <MergeHint c={clusterOf.get(s.q.id)} onOpen={p.onOpenClusters} />
                            <PoolContribs sum={s} now={now} />
                            {renderCard(s)}
                          </div>
                        )}
                      </li>
                    );
                  })}
            </ul>
            {hasMore && (
              <div ref={sentinel} className="pv-more">
                <button type="button" className="ui-btn" onClick={() => p.setVisibleCount((v) => v + PAGE)}>
                  Daha fazla göster ({(list.length - p.visibleCount).toLocaleString('tr-TR')} soru daha)
                </button>
              </div>
            )}
          </section>

          {split && (
            <section id={detailId} className="pv-detail" aria-label="Seçili soru">
              {selected ? (
                <PoolDetail
                  key={selected.q.id}
                  sum={selected}
                  now={now}
                  list={list}
                  onSelect={(id) => setOpenId(id)}
                  merge={<MergeHint c={clusterOf.get(selected.q.id)} onOpen={p.onOpenClusters} />}
                >
                  {renderCard(selected)}
                </PoolDetail>
              ) : (
                <p className="pv-contrib-empty">Soldan bir soru seç.</p>
              )}
            </section>
          )}

          {showFeed && <PoolLiveFeed sums={allSums} now={now} onOpen={(id) => setOpenId(id)} />}
        </div>
      )}
    </div>
  );
};

/** Geniş ekran ayrıntı bölmesi: başlık (no, ders, sayılar, önceki/sonraki) + katkılar + soru kartı */
const PoolDetail: React.FC<{ sum: PoolSummary; now: number; list: PoolSummary[]; onSelect: (id: string) => void; merge?: React.ReactNode; children: React.ReactNode }> = ({ sum, now, list, onSelect, merge, children }) => {
  const { q } = sum;
  const i = list.findIndex((s) => s.q.id === q.id);
  const prev = i > 0 ? list[i - 1] : undefined;
  const next = i >= 0 && i < list.length - 1 ? list[i + 1] : undefined;
  const parts = q.fragments?.length || 0;
  const isNew = sum.lastAt > 0 && now - sum.lastAt < DAY;
  return (
    <div className="pv-det">
      <div className="pv-det-h">
        <strong>Soru {q.questionNumber || '—'}</strong>
        {isNew && <span className="pv-new">YENİ</span>}
        <span className="pv-det-d">{[q.discipline, q.topic].filter(Boolean).join(' · ')}</span>
        <span className="pv-sp" />
        <span className="pv-det-n">{sum.people.length} katkıcı · {parts} parça · {sum.comments} yorum</span>
        <button type="button" className="pv-nav" disabled={!prev} onClick={() => prev && onSelect(prev.q.id)} aria-label="Önceki soru"><ChevronLeft aria-hidden /></button>
        <button type="button" className="pv-nav" disabled={!next} onClick={() => next && onSelect(next.q.id)} aria-label="Sonraki soru"><ChevronRight aria-hidden /></button>
      </div>
      {merge}
      <PoolContribs sum={sum} now={now} />
      {children}
    </div>
  );
};

/** Bu kayıt bir birleştirme önerisinin üyesiyse: kaç kayıtla aynı soruyu anlattığı + öneriyi aç */
const MergeHint: React.FC<{ c?: { id: string; size: number }; onOpen: (id?: string) => void }> = ({ c, onOpen }) =>
  c ? (
    <button type="button" className="pv-mhint" onClick={() => onOpen(c.id)}>
      <Combine aria-hidden />
      <span>Bu kayıt {c.size - 1} başka kayıtla aynı soruyu anlatıyor olabilir</span>
      <b>Öneriyi aç <ChevronRight aria-hidden /></b>
    </button>
  ) : null;
