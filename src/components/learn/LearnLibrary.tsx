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
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowRight, Check, FileQuestionMark, FileText, Layers, Search } from 'lucide-react';
import { deckName, type DeckCatalogEntry } from '../../data/deckStore';
import { useDeckPdfIds, useDeckPdfMissing } from '../../services/deckPdfService';
import { disciplineClass, disciplineLabel } from '../../utils/discipline';
import { FilterPills, PageToolbar, type ToolbarChip } from '../ui/PageToolbar';
import { disciplineGroup, type ArchiveFilter } from './LearnHub';
import '../../styles/learn-v10.css';

type Progress = Record<string, { last?: number; seen?: number[] } | undefined>;
type Status = 'all' | 'active' | 'done';
const PAGE = 24;

const RECENT_KEY = 'medsoru_learn_recent_v1';
const readRecent = (): Record<string, number> => {
  try {
    return JSON.parse(localStorage.getItem(RECENT_KEY) || '{}');
  } catch {
    return {};
  }
};

/** k1p-k1-07-… → 7 ; sıra numarası olmayan desteler sona */
const orderOf = (d: DeckCatalogEntry) => {
  const m = /-k\d+-(\d+)/.exec(d.id);
  return m ? Number(m[1]) : 999;
};
const isPublished = (d: DeckCatalogEntry) => !!(d.isNew || String(d.version || '').startsWith('2') || (d.slideCount && d.slideCount >= 50) || (d.totalSlides && d.totalSlides >= 50));

/** Kitaplıktaki kısa ders dalı adı: "Üroloji / Tıbbi Patoloji" → "Üroloji" */
const branchOf = (d: DeckCatalogEntry) => disciplineLabel(disciplineGroup(d.discipline));
/** "Kurul 1 - Ürogenital…" → "Kurul 1"; kurul numarası yoksa "Diğer" */
const kurulOf = (d: DeckCatalogEntry) => {
  const m = /kurul\s*(\d+)/i.exec(String(d.committee || d.category || ''));
  return m ? `Kurul ${m[1]}` : 'Diğer';
};

const stateOf = (d: DeckCatalogEntry, p: Progress) => {
  const total = d.slideCount || 0;
  const seen = Math.min(total, p[d.id]?.seen?.length || 0);
  const pct = total ? Math.min(100, Math.round((seen / total) * 100)) : 0;
  const status: 'new' | 'active' | 'done' = seen === 0 ? 'new' : total && seen >= total ? 'done' : 'active';
  return { seen, pct, status, last: Math.min(total || 1, (p[d.id]?.last ?? 0) + 1) };
};

/** Ders PDF'i eşlenemeyen ve ders günü üzerinden en az bir hafta geçmiş deste: kaynağı bilinmiyor (LearnHub ile aynı kural). */
const SOURCE_WAIT_DAYS = 7;
const unknownSource = (tarih: string | undefined) => {
  if (tarih === undefined) return false;
  if (!tarih) return true;
  return Date.now() - new Date(`${tarih}T00:00:00`).getTime() >= SOURCE_WAIT_DAYS * 864e5;
};
const trDate = (t: string) => (t ? new Date(`${t}T00:00:00`).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' }) : '');

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
  /** Sürümlü dersler: grup (V1) kimliği → sürüm etiketleri (["V1", "V2"]) */
  versions?: Record<string, string[]>;
}> = ({ decks: all, progress, isAdmin, archive, onArchive, onOpen, versions }) => {
  const [query, setQuery] = useState('');
  const [branch, setBranch] = useState('all');
  const [kurul, setKurul] = useState('all');
  const [status, setStatus] = useState<Status>('all');
  const [limit, setLimit] = useState(PAGE);
  const [recent] = useState(readRecent);
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
  const visible = useMemo(
    () => (status === 'all' ? byQuery : byQuery.filter((d) => stateOf(d, progress).status === status)),
    [byQuery, status, progress]
  );

  // Süzgeç değişince ilk sayfaya dön
  useEffect(() => setLimit(PAGE), [q, branch, kurul, status, archive]);
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
        title="Öğren"
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
        chips={chips}
        onClearChips={() => { setBranch('all'); setKurul('all'); onArchive('new_only'); }}
      />

      {resume.length > 0 && !filtered && (
        <section className="lv-resume" aria-label="Devam et">
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
          <ul className="lv-grid" aria-label="Desteler">
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
                      {ver && <span className="lv-ver" title={`Bu dersin ${ver.length} sürümü var (${ver.join(', ')}) — açınca seçersin`}><Layers aria-hidden />{ver.length} sürüm</span>}
                      {noSrc && <span className="lv-nosrc" title={noSrcTip}><FileQuestionMark aria-hidden /><span className="sr-only">Uyarı: kaynak PDF bilinmiyor</span></span>}
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
