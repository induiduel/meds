/**
 * Öğren kitaplığı (v10 kompakt). Yapı (canvas "Ogren-Masaustu"):
 *  - PageToolbar: "Öğren" · deste sayısı · arama · Tümü / Devam eden / Bitirilen · Süzgeç (ders dalı, kurul; yöneticide deste kümesi)
 *  - "Devam et" şeridi: yarım kalan en son 2 deste, ilerleme halkasıyla
 *  - Ders dalı hapları
 *  - Deste kartı ızgarası (masaüstü 3, tablet 2, telefon 1 sütun; Akış modunda tek sütun); 24'er 24'er çizilir
 * İlerleme InteractiveDeckView'in tuttuğu `medsoru_learn_progress_v1` kaydından (görülen adımlar) okunur;
 * son açılma zamanı LearnHub'daki `medsoru_learn_recent_v1` (touchRecent) kaydındadır.
 * Stil: styles/learn-v10.css (.lv-*).
 */
import { getAppearance, useAppearance } from '../../utils/appearance';
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowRight, Check, FileQuestionMark, FileText, LayoutGrid, Layers, RotateCcw, Rows3, Search } from 'lucide-react';
import { useReviewCounts } from '../../hooks/useReviewCounts';
import '../../styles/learn-focus.css';
import { deckName, type DeckCatalogEntry } from '../../data/deckStore';
import { useDeckPdfIds, useDeckPdfMissing } from '../../services/deckPdfService';
import { disciplineClass, disciplineLabel } from '../../utils/discipline';
import { FilterPills, PageToolbar, QuickOptions, type ToolbarChip } from '../ui/PageToolbar';
import SCHEDULE from '../../data/deckSchedule.json';
import { disciplineGroup, type ArchiveFilter } from './LearnHub';
import '../../styles/learn-v10.css';
import { KonuIsaret } from '../takip/KonuTakip';
import { ogrenTakipId } from '../takip/ogrenTakipId';
import CihazdaIsaret from '../cevrimdisi/CihazdaIsaret';

export type Progress = Record<string, { last?: number; seen?: number[] } | undefined>;
export type Status = 'all' | 'active' | 'done';
export const PAGE = 24;

/** Ders programı kaydı (scripts/build_deck_schedule.py): s sıra, t tarih, k kurul, h hoca */
type Sched = { s: number; t?: string; k?: number; h?: string };
const SCHED = SCHEDULE as Record<string, Sched>;
/** V2 gibi sürümler ana dersin program yerini paylaşır */
export const schedOf = (d: DeckCatalogEntry): Sched | undefined => SCHED[d.id] || SCHED[d.id.replace(/-v\d+$/i, '')];

export type View = 'grid' | 'list';
export type Sort = 'program' | 'date_desc' | 'alpha' | 'alpha_desc' | 'progress' | 'recent' | 'slides';
export const SORT_LABEL: Record<Sort, string> = {
  program: 'Ders programı',
  date_desc: 'En yeni ders',
  alpha: 'A → Z',
  alpha_desc: 'Z → A',
  progress: 'İlerleme',
  recent: 'Son açılan',
  slides: 'Slayt sayısı',
};
export const VIEW_KEY = 'medsoru_learn_view';
export const SORT_KEY = 'medsoru_learn_sort';
export const readPref = <T extends string>(k: string, ok: readonly T[], def: T): T => {
  try {
    const v = localStorage.getItem(k) as T | null;
    return v && ok.includes(v) ? v : def;
  } catch {
    return def;
  }
};
export const writePref = (k: string, v: string) => { try { localStorage.setItem(k, v); } catch { /* yok */ } };

const RECENT_KEY = 'medsoru_learn_recent_v1';
export const readRecent = (): Record<string, number> => {
  try {
    return JSON.parse(localStorage.getItem(RECENT_KEY) || '{}');
  } catch {
    return {};
  }
};

/** k1p-k1-07-… → 7 ; sıra numarası olmayan desteler sona */
export const orderOf = (d: DeckCatalogEntry) => {
  const m = /-k\d+-(\d+)/.exec(d.id);
  return m ? Number(m[1]) : 999;
};
export const isPublished = (d: DeckCatalogEntry) => !!(d.isNew || String(d.version || '').startsWith('2') || (d.slideCount && d.slideCount >= 50) || (d.totalSlides && d.totalSlides >= 50));

/** Kitaplıktaki kısa ders dalı adı: "Üroloji / Tıbbi Patoloji" → "Üroloji" */
export const branchOf = (d: DeckCatalogEntry) => disciplineLabel(disciplineGroup(d.discipline));
/** "Kurul 1 - Ürogenital…" → "Kurul 1"; kurul numarası yoksa "Diğer" */
/** /ogren?kurul=N → "Kurul N" süzgeciyle açılır (Geçmiş kurullar bağlantısı); yoksa tümü */
export const urlKurulSuzgeci = (): string => {
  try { const n = Number(new URLSearchParams(location.search).get('kurul')); return n >= 1 && n <= 6 ? `Kurul ${n}` : 'all'; } catch { return 'all'; }
};

export const kurulOf = (d: DeckCatalogEntry) => {
  const m = /kurul\s*(\d+)/i.exec(String(d.committee || d.category || ''));
  return m ? `Kurul ${m[1]}` : 'Diğer';
};

export const stateOf = (d: DeckCatalogEntry, p: Progress) => {
  const total = d.slideCount || 0;
  const seen = Math.min(total, p[d.id]?.seen?.length || 0);
  const pct = total ? Math.min(100, Math.round((seen / total) * 100)) : 0;
  const status: 'new' | 'active' | 'done' = seen === 0 ? 'new' : total && seen >= total ? 'done' : 'active';
  return { seen, pct, status, last: Math.min(total || 1, (p[d.id]?.last ?? 0) + 1) };
};

/** Ders PDF'i eşlenemeyen ve ders günü üzerinden en az bir hafta geçmiş deste: kaynağı bilinmiyor (LearnHub ile aynı kural). */
const SOURCE_WAIT_DAYS = 7;
export const unknownSource = (tarih: string | undefined) => {
  if (tarih === undefined) return false;
  if (!tarih) return true;
  return Date.now() - new Date(`${tarih}T00:00:00`).getTime() >= SOURCE_WAIT_DAYS * 864e5;
};
export const trDate = (t: string) => (t ? new Date(`${t}T00:00:00`).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' }) : '');

/** Kartın tek satırlık özeti: alt başlık / açıklama / genel bakışın ilk cümlesi (kesme CSS'te) */
const blurbOf = (d: DeckCatalogEntry) => {
  const raw = String(d.subtitle || d.description || d.overview || '').replace(/\s+/g, ' ').trim();
  const first = raw.split(/(?<=[.!?])\s/)[0] || raw;
  return first;
};

const Ring: React.FC<{ pct: number }> = ({ pct }) => (
  <span className="lv-ring" style={{ ['--p' as string]: pct }} aria-hidden>
    <b>%{pct}</b>
  </span>
);

export const LearnLibrary: React.FC<{
  decks: DeckCatalogEntry[];
  progress: Progress;
  isAdmin?: boolean;
  archive: ArchiveFilter;
  onArchive: (f: ArchiveFilter) => void;
  onOpen: (id: string, pdf?: boolean) => void;
  /** Sürümlü dersler: listede gösterilen (en yeni) sürümün kimliği → sürüm etiketleri (["V1", "V2"]) */
  versions?: Record<string, string[]>;
  /** Hata defteri (tekrar ekranı); deckId verilirse yalnız o ders */
  onOpenReview?: (deckId?: string) => void;
  /** "Tekrar et": kalınan adımı başa alıp açar (klasik görünümde yalnız Bitirdim işareti var) */
  onRestart?: (id: string) => void;
}> = ({ decks: all, progress, isAdmin, archive, onArchive, onOpen, versions, onOpenReview }) => {
  const review = useReviewCounts();
  const [query, setQuery] = useState('');
  const [branch, setBranch] = useState('all');
  const [kurul, setKurul] = useState(urlKurulSuzgeci);
  const [status, setStatus] = useState<Status>('all');
  const [limit, setLimit] = useState(PAGE);
  const [recent] = useState(readRecent);
  const isV11 = useAppearance().design !== 'v10';
  const [view, setViewState] = useState<View>(() => readPref<View>(VIEW_KEY, ['grid', 'list'], getAppearance().design === 'v10' ? 'grid' : 'list'));
  const [sort, setSortState] = useState<Sort>(() => readPref<Sort>(SORT_KEY, Object.keys(SORT_LABEL) as Sort[], 'program'));
  const setView = (v: View) => { setViewState(v); writePref(VIEW_KEY, v); };
  const setSort = (v: Sort) => { setSortState(v); writePref(SORT_KEY, v); };
  const rootRef = useRef<HTMLDivElement>(null);
  const pdfIds = useDeckPdfIds();
  const pdfMissing = useDeckPdfMissing();

  // "/" arama kutusuna odaklanır
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (e.key !== '/' || e.metaKey || e.ctrlKey || (t && /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) || t?.isContentEditable) return;
      if (document.querySelector('.ls-root')) return; // ders açıkken kısayol dersin
      const input = rootRef.current?.querySelector<HTMLInputElement>('[data-page-search]');
      if (!input) return;
      e.preventDefault();
      input.focus();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  // Revize sürümü (V2…) olan ders, V1'i kısa/eski olsa da yayındadır
  const published = (d: DeckCatalogEntry) => isPublished(d) || !!versions?.[d.id];
  const counts = useMemo(() => ({
    published: all.filter(published).length,
    legacy: all.filter((d) => !published(d)).length,
  }), [all, versions]); // eslint-disable-line react-hooks/exhaustive-deps

  // Öğrenci yalnız yayındaki dersleri görür (hiç yoksa hepsini); yönetici arşivi de seçebilir
  const scoped = useMemo(() => {
    const f = isAdmin ? archive : 'new_only';
    const list = f === 'all' ? all : f === 'legacy_only' ? all.filter((d) => !published(d)) : all.filter(published);
    return (list.length || isAdmin ? list : all).slice().sort((a, b) => orderOf(a) - orderOf(b) || deckName(a).localeCompare(deckName(b), 'tr'));
  }, [all, isAdmin, archive, versions]); // eslint-disable-line react-hooks/exhaustive-deps

  const branches = useMemo(() => {
    const m = new Map<string, number>();
    scoped.forEach((d) => m.set(branchOf(d), (m.get(branchOf(d)) || 0) + 1));
    return [...m.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'tr'));
  }, [scoped]);
  const kurullar = useMemo(() => {
    const m = new Map<string, number>();
    scoped.forEach((d) => m.set(kurulOf(d), (m.get(kurulOf(d)) || 0) + 1));
    return [...m.entries()].sort((a, b) => a[0].localeCompare(b[0], 'tr', { numeric: true }));
  }, [scoped]);
  useEffect(() => {
    if (branch !== 'all' && !branches.some(([g]) => g === branch)) setBranch('all');
    if (kurul !== 'all' && !kurullar.some(([k]) => k === kurul)) setKurul('all');
  }, [branches, kurullar, branch, kurul]);

  const q = query.trim().toLocaleLowerCase('tr-TR');
  const byQuery = useMemo(
    () => scoped.filter((d) =>
      (branch === 'all' || branchOf(d) === branch) &&
      (kurul === 'all' || kurulOf(d) === kurul) &&
      (!q || [d.title, d.shortTitle, d.discipline, d.instructor, d.overview, ...(d.highYieldPearls || [])].join(' ').toLocaleLowerCase('tr-TR').includes(q))),
    [scoped, branch, kurul, q]
  );
  const statusCount = useMemo(() => {
    const c = { all: byQuery.length, active: 0, done: 0, new: 0 };
    byQuery.forEach((d) => { c[stateOf(d, progress).status] += 1; });
    return c;
  }, [byQuery, progress]);
  const visible = useMemo(() => {
    const list = status === 'all' ? byQuery.slice() : byQuery.filter((d) => stateOf(d, progress).status === status);
    const name = (d: DeckCatalogEntry) => deckName(d, false);
    // Programda olmayan desteler program sıralamalarında sona, kendi aralarında eski sıra numarasıyla
    const prog = (a: DeckCatalogEntry, b: DeckCatalogEntry) =>
      (schedOf(a)?.s ?? 1e4 + orderOf(a)) - (schedOf(b)?.s ?? 1e4 + orderOf(b)) || name(a).localeCompare(name(b), 'tr');
    const cmp: Record<Sort, (a: DeckCatalogEntry, b: DeckCatalogEntry) => number> = {
      program: prog,
      date_desc: (a, b) => (schedOf(b)?.t || '').localeCompare(schedOf(a)?.t || '') || prog(b, a),
      alpha: (a, b) => name(a).localeCompare(name(b), 'tr', { numeric: true }),
      alpha_desc: (a, b) => name(b).localeCompare(name(a), 'tr', { numeric: true }),
      progress: (a, b) => stateOf(b, progress).pct - stateOf(a, progress).pct || prog(a, b),
      recent: (a, b) => (recent[b.id] || 0) - (recent[a.id] || 0) || prog(a, b),
      slides: (a, b) => (b.slideCount || 0) - (a.slideCount || 0) || prog(a, b),
    };
    return list.sort(cmp[sort]);
  }, [byQuery, status, progress, sort, recent]);

  // Süzgeç değişince ilk sayfaya dön
  useEffect(() => setLimit(PAGE), [q, branch, kurul, status, archive, sort]);
  const shown = visible.slice(0, limit);
  const hasMore = visible.length > limit;
  const sentinel = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = sentinel.current;
    if (!el || !hasMore || typeof IntersectionObserver === 'undefined') return;
    const io = new IntersectionObserver((ents) => {
      if (ents.some((e) => e.isIntersecting)) setLimit((v) => v + PAGE);
    }, { rootMargin: '600px 0px' });
    io.observe(el);
    return () => io.disconnect();
  }, [hasMore, shown.length]);

  // Devam et: yarım kalanlar, en son açılan önce (en çok 2)
  const resume = useMemo(
    () => scoped.filter((d) => stateOf(d, progress).status === 'active').sort((a, b) => (recent[b.id] || 0) - (recent[a.id] || 0)).slice(0, 2),
    [scoped, progress, recent]
  );

  const filtered = !!q || branch !== 'all' || kurul !== 'all' || status !== 'all';
  const reset = () => {
    setQuery('');
    setBranch('all');
    setKurul('all');
    setStatus('all');
  };

  const chips: ToolbarChip[] = [
    ...(branch !== 'all' ? [{ id: 'b', label: branch, onRemove: () => setBranch('all') }] : []),
    ...(kurul !== 'all' ? [{ id: 'k', label: kurul, onRemove: () => setKurul('all') }] : []),
    ...(isAdmin && archive !== 'new_only' ? [{ id: 'a', label: archive === 'all' ? 'Tüm desteler' : 'Arşiv', onRemove: () => onArchive('new_only') }] : []),
  ];

  const filters = (
    <>
      <FilterPills<string>
        label="Ders dalı"
        value={branch}
        onChange={setBranch}
        options={[{ id: 'all', label: 'Tümü', count: scoped.length }, ...branches.map(([g, n]) => ({ id: g, label: g, count: n }))]}
      />
      {kurullar.length > 1 && (
        <FilterPills<string>
          label="Kurul"
          value={kurul}
          onChange={setKurul}
          options={[{ id: 'all', label: 'Tümü', count: scoped.length }, ...kurullar.map(([k, n]) => ({ id: k, label: k, count: n }))]}
        />
      )}
      {isAdmin && (
        <FilterPills<ArchiveFilter>
          label="Deste kümesi (yönetici)"
          value={archive}
          onChange={onArchive}
          options={[
            { id: 'new_only', label: 'Yayında', count: counts.published },
            { id: 'legacy_only', label: 'Arşiv', count: counts.legacy },
            { id: 'all', label: 'Tümü', count: all.length },
          ]}
        />
      )}
    </>
  );

  return (
    <div className="lv" ref={rootRef}>
      <PageToolbar<Status>
        title="Etkileşimli dersler"
        count={`${scoped.length.toLocaleString('tr-TR')} deste`}
        search={{ value: query, onChange: setQuery, placeholder: 'Deste, ders, konu ara' }}
        segments={{
          label: 'Durum',
          value: status,
          onChange: setStatus,
          options: [
            { id: 'all', label: 'Tümü' },
            { id: 'active', label: 'Devam eden', count: statusCount.active || undefined },
            { id: 'done', label: 'Bitirilen', count: statusCount.done || undefined },
          ],
        }}
        filters={filters}
        filterCount={chips.length}
        filterTitle="Öğren süzgeci"
        quick={[{
          id: 'sirala',
          label: 'Sırala',
          value: sort !== 'program' ? SORT_LABEL[sort] : undefined,
          onClear: () => setSort('program'),
          content: (close) => (
            <QuickOptions close={close} value={sort} onPick={(v) => setSort(v as Sort)} options={(Object.keys(SORT_LABEL) as Sort[]).map((id) => ({
              id,
              label: SORT_LABEL[id],
              hint: id === 'program' ? 'kurul ve ders günü sırası' : undefined,
            }))} />
          ),
        }]}
        tools={
          <div className="pt-view" role="radiogroup" aria-label="Görünüm">
            {([['grid', 'Izgara', LayoutGrid], ['list', 'Liste', Rows3]] as const).map(([id, label, Icon]) => (
              <button key={id} type="button" role="radio" aria-checked={view === id} className={view === id ? 'is-on' : ''} onClick={() => setView(id)} title={id === 'grid' ? 'Izgara: kartlar' : 'Liste: her deste tek satır'}>
                <Icon aria-hidden />
                <span className="ck-view-l">{label}</span>
              </button>
            ))}
          </div>
        }
        chips={chips}
        onClearChips={() => { setBranch('all'); setKurul('all'); onArchive('new_only'); }}
      />

      {!filtered && ((onOpenReview && review.total.open > 0) || resume.length > 0) && (
      <div className={isV11 ? 'lv-cont' : 'lv-cont-v10'}>
      {onOpenReview && review.total.open > 0 && (
        <button type="button" className="lr-due-card" onClick={() => onOpenReview()}>
          <span className="ico"><RotateCcw aria-hidden /></span>
          <span className="tx">
            <b>{review.total.due > 0 ? `Bugün ${review.total.due} öge tekrar zamanı` : 'Hata defteri'}</b>
            <small>{review.total.due > 0 ? `~${Math.max(1, Math.round(review.total.due * 0.5))} dk · derste yanlış yaptıkların aralıklarla geri gelir` : `${review.total.open} öge defterde; vadeleri henüz gelmedi`}</small>
          </span>
          <span className="go">{review.total.due > 0 ? 'Başla' : 'Aç'}</span>
        </button>
      )}

      {resume.length > 0 && (
        <section className={isV11 ? 'lv-resume' : 'lv-resume bento is-duo is-list'} aria-label="Devam et">
          {resume.map((d) => {
            const s = stateOf(d, progress);
            return (
              <button key={d.id} type="button" className={`lv-res ${disciplineClass(d.discipline)}`} onClick={() => onOpen(d.id)} aria-label={`${deckName(d, false)} — %${s.pct}, sürdür`}>
                <Ring pct={s.pct} />
                <span className="lv-res-body">
                  <small>Devam et · {branchOf(d)}</small>
                  <b>{deckName(d)}</b>
                  <span>Slayt {s.last} / {d.slideCount} · {s.seen} görüldü</span>
                </span>
                <span className="lv-res-go">Sürdür <ArrowRight aria-hidden /></span>
              </button>
            );
          })}
        </section>
      )}
      </div>
      )}

      {branches.length > 1 && (
        <nav className="lv-pills" aria-label="Ders dalı">
          {[['all', scoped.length] as [string, number], ...branches].map(([g, n]) => (
            <button key={g} type="button" aria-pressed={branch === g} className={branch === g ? 'is-on' : ''} onClick={() => setBranch(g)}>
              {g === 'all' ? 'Tümü' : g}
              <small>{n}</small>
            </button>
          ))}
        </nav>
      )}

      {visible.length === 0 ? (
        <div className="lv-empty">
          <Search aria-hidden />
          <b>{q ? `“${query.trim()}” için deste yok` : 'Bu süzgeçte deste yok'}</b>
          <p>Süzgeçleri temizleyip tüm destelere dönebilirsin.</p>
          <button type="button" className="ui-btn is-tonal" onClick={reset}>Süzgeçleri temizle</button>
        </div>
      ) : (
        <>
          {view === 'list' ? (
            <ol className="lv-rows" aria-label="Desteler">
              {shown.map((d) => {
                const s = stateOf(d, progress);
                const sc = schedOf(d);
                const pdf = !!pdfIds?.has(d.id);
                return (
                  <li key={d.id} className={`lv-row ${disciplineClass(d.discipline)} is-${s.status}`}>
                    <button type="button" className="lv-row-main" onClick={() => onOpen(d.id)} aria-label={`${deckName(d, false)} — ${s.status === 'done' ? 'tamamlandı' : s.status === 'active' ? `%${s.pct}, devam et` : 'başla'}`}>
                      <span className="lv-row-n">{sc ? sc.s : '—'}</span>
                      <span className="lv-row-date">{sc?.t ? trDate(sc.t) : ''}</span>
                      <span className="lv-row-t">
                        <b>{deckName(d, false)}</b>
                        <small>{[branchOf(d), versions?.[d.id] ? versions[d.id].join('/') : '', (review.counts[d.id]?.due ?? 0) > 0 ? `${review.counts[d.id].due} tekrar` : ''].filter(Boolean).join(' · ')}</small>
                      </span>
                      <span className="lv-row-sl">{d.slideCount} slayt</span>
                      <span className="lv-row-st">
                        <span className="lv-bar" aria-hidden><i style={{ width: `${s.pct}%` }} /></span>
                        {s.status === 'done' ? <><Check aria-hidden />Bitti</> : s.status === 'active' ? `%${s.pct}` : 'Başla'}
                      </span>
                    </button>
                    <CihazdaIsaret paket={`ogren:${d.id}`} />
                    <KonuIsaret modul="ogren" konu={ogrenTakipId(d.id)} ad={deckName(d, false)} turetilen={s.status === 'done'} />
                    {pdf ? (
                      <button type="button" className="lv-card-pdf" onClick={() => onOpen(d.id, true)} title="Ders slaytını (PDF) aç" aria-label={`${deckName(d)} slayt PDF'ini aç`}>
                        <FileText aria-hidden />
                      </button>
                    ) : <span className="lv-row-pad" aria-hidden />}
                  </li>
                );
              })}
            </ol>
          ) : (
          <ul className="lv-grid bento is-rhythm is-list" aria-label="Desteler">
            {shown.map((d) => {
              const s = stateOf(d, progress);
              const pdf = !!pdfIds?.has(d.id);
              const ver = versions?.[d.id];
              const noSrc = !pdf && unknownSource(pdfMissing?.[d.id]);
              const noSrcTip = `Bu dersin 2026-27 slaytı Drive'da yok${pdfMissing?.[d.id] ? ` (ders ${trDate(pdfMissing[d.id])})` : ''}; içerik önceki yılın kaynağından hazırlandı, hangi PDF'e ait olduğu bilinmiyor.`;
              const blurb = blurbOf(d);
              return (
                <li key={d.id} className={`lv-card ${disciplineClass(d.discipline)} ${pdf ? 'has-pdf' : ''} is-${s.status}`}>
                  <button
                    type="button"
                    className="lv-card-main"
                    onClick={() => onOpen(d.id)}
                    aria-label={`${deckName(d, false)} — ${s.status === 'done' ? 'tamamlandı' : s.status === 'active' ? `%${s.pct}, devam et` : 'başla'}`}
                  >
                    <span className="lv-card-top">
                      <span className="lv-tag">{branchOf(d)}</span>
                      {ver && (
                        <span className="lv-ver" title={`Bu dersin ${ver.length} sürümü var (${ver.join(', ')}); listede ${d.versionLabel || ver[ver.length - 1]} gösteriliyor — açınca seçersin`}>
                          <Layers aria-hidden />
                          {ver.map((l) => (
                            <i key={l} className={l === (d.versionLabel || 'V1') ? 'is-on' : ''}>{l}</i>
                          ))}
                        </span>
                      )}
                      {noSrc && <span className="lv-nosrc" title={noSrcTip}><FileQuestionMark aria-hidden /><span className="sr-only">Uyarı: kaynak PDF bilinmiyor</span></span>}
                      {(review.counts[d.id]?.due ?? 0) > 0 && <span className="lr-badge" title="Bu derste tekrar zamanı gelen hata defteri ögeleri"><RotateCcw aria-hidden width={11} height={11} />{review.counts[d.id].due}</span>}
                      <span className="lv-n">{d.slideCount} slayt</span>
                    </span>
                    <strong className="lv-card-t">{deckName(d, false)}</strong>
                    {blurb && <span className="lv-card-m">{blurb}</span>}
                    <span className="lv-card-foot">
                      <span className="lv-bar" aria-hidden><i style={{ width: `${s.pct}%` }} /></span>
                      <span className="lv-st">
                        {s.status === 'done' ? <><Check aria-hidden />Bitti</> : s.status === 'active' ? `%${s.pct}` : 'Başla'}
                      </span>
                    </span>
                  </button>
                  {pdf && (
                    <button type="button" className="lv-card-pdf" onClick={() => onOpen(d.id, true)} title="Ders slaytını (PDF) aç" aria-label={`${deckName(d)} slayt PDF'ini aç`}>
                      <FileText aria-hidden />
                    </button>
                  )}
                </li>
              );
            })}
          </ul>
          )}
          {hasMore && (
            <div ref={sentinel} className="lv-more">
              <button type="button" className="ui-btn is-tonal" onClick={() => setLimit((v) => v + PAGE)}>
                Daha fazla göster ({(visible.length - limit).toLocaleString('tr-TR')})
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

/** Deste yüklenirken oynatıcının gerçek ölçülerinde iskelet (üst çubuk · bölüm rayı · okuma sütunu) */
export const LessonSkeleton: React.FC<{ onCancel: () => void }> = ({ onCancel }) => (
  <div className="lv-skel" role="status" aria-live="polite" aria-label="Ders açılıyor">
    <div className="lv-skel-top">
      <span className="ui-skel" style={{ width: 36, height: 36, borderRadius: 10 }} />
      <span className="ui-skel" style={{ width: 'min(320px, 45%)', height: 16 }} />
      <span className="lv-skel-sp" />
      <button type="button" className="ui-btn is-sm is-ghost" onClick={onCancel}>Vazgeç</button>
    </div>
    <div className="lv-skel-body">
      <div className="lv-skel-rail" aria-hidden>
        {Array.from({ length: 12 }, (_, i) => <span key={i} className="ui-skel" style={{ height: 34, borderRadius: 8 }} />)}
      </div>
      <div className="lv-skel-col" aria-hidden>
        <span className="ui-skel" style={{ width: 120, height: 12 }} />
        <span className="ui-skel" style={{ width: '70%', height: 28 }} />
        <span className="ui-skel" style={{ width: '100%', height: 16 }} />
        <span className="ui-skel" style={{ width: '94%', height: 16 }} />
        <span className="ui-skel" style={{ width: '82%', height: 16 }} />
        <span className="ui-skel" style={{ width: '100%', height: 150, borderRadius: 14, marginTop: 8 }} />
      </div>
    </div>
    <span className="sr-only">Ders açılıyor…</span>
  </div>
);
