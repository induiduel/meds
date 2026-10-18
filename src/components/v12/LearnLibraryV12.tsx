/**
 * Öğren kitaplığı — v12 "Net" (canvas panosu Learn.dc.html). Yalnız data-design='v12' iken InteractiveDeckView'den çizilir;
 * v10/v11 kitaplığı (LearnLibrary) olduğu gibi kalır. Veri ve kurallar LearnLibrary'deki yardımcılardan gelir.
 *
 * Yapı:
 *  - Başlık: "Öğren" · kapsam (kurul) · ders sayısı
 *  - Araç satırı: arama ("/" kısayolu) · Tümü / Devam eden / Biten · Kurul ▾ · Ders ▾ · Sırala ▾ · (yönetici) Küme ▾ · Liste | Izgara
 *  - "Devam et" paneli: yarım kalan en son 3 ders, düz satırlar (adım, ne zaman, % + ince çubuk)
 *  - "Hata defteri · n vadesi geldi" satırı
 *  - Ders dalına göre gruplanmış bölümler: başlık (n ders · k bitti) + sıkı satırlar ya da ızgara karoları
 *  - Boş durum: hangi süzgecin boşalttığını ve Tümü'ye dönünce kaç ders bulunacağını söyler
 * Stil: styles/v12/learn-library.css (.l12-*).
 */
import React, { useDeferredValue, useEffect, useMemo, useRef, useState } from 'react';
import { ChevronRight, FileQuestionMark, LayoutGrid, List, RotateCcw, Search } from 'lucide-react';
import { deckName, type DeckCatalogEntry } from '../../data/deckStore';
import { useDeckPdfIds, useDeckPdfMissing } from '../../services/deckPdfService';
import { useReviewCounts } from '../../hooks/useReviewCounts';
import { QuickOptions, QuickPill } from '../ui/PageToolbar';
import type { ArchiveFilter } from '../learn/LearnHub';
import {
  PAGE, SORT_KEY, SORT_LABEL, VIEW_KEY, branchOf, isPublished, kurulOf, orderOf, readPref, readRecent, schedOf, stateOf, trDate,
  unknownSource, writePref, type Progress, type Sort, type Status, type View,
} from '../learn/LearnLibrary';
import { KonuDugmeleri, KonuSureEtiketi } from '../takip/KonuTakip';
import { ogrenTakipId } from '../takip/ogrenTakipId';
import '../../styles/v12/learn-library.css';

export interface LearnLibraryV12Props {
  decks: DeckCatalogEntry[];
  progress: Progress;
  isAdmin?: boolean;
  archive: ArchiveFilter;
  onArchive: (f: ArchiveFilter) => void;
  onOpen: (id: string, pdf?: boolean) => void;
  versions?: Record<string, string[]>;
  onOpenReview?: (deckId?: string) => void;
  /** "Tekrar et": kalınan adımı başa alıp dersi açar */
  onRestart?: (id: string) => void;
}

const STATUS_LABEL: Record<Status, string> = { all: 'Tümü', active: 'Devam eden', done: 'Biten' };
const RESUME_MAX = 3;

/** Son açılma zamanı → "2 sa önce", "dün", "3 gün önce", "12 Ekim" */
const ago = (t?: number) => {
  if (!t) return '';
  const now = Date.now();
  const min = Math.max(0, Math.round((now - t) / 60_000));
  const day0 = new Date(); day0.setHours(0, 0, 0, 0);
  if (t >= day0.getTime()) {
    if (min < 1) return 'az önce';
    if (min < 60) return `${min} dk önce`;
    return `${Math.round(min / 60)} sa önce`;
  }
  const days = Math.ceil((day0.getTime() - t) / 864e5);
  if (days <= 1) return 'dün';
  if (days < 7) return `${days} gün önce`;
  return new Date(t).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' });
};

const Prog: React.FC<{ pct: number; done?: boolean }> = ({ pct, done }) => (
  <span className="l12-prog">
    <span className="l12-pct">{pct}%</span>
    <span className="l12-bar" aria-hidden><i className={done ? 'is-done' : ''} style={{ width: `${pct}%` }} /></span>
  </span>
);

export const LearnLibraryV12: React.FC<LearnLibraryV12Props> = ({ decks: all, progress, isAdmin, archive, onArchive, onOpen, versions, onOpenReview, onRestart }) => {
  const review = useReviewCounts();
  const [input, setInput] = useState('');
  const query = useDeferredValue(input);
  const [branch, setBranch] = useState('all');
  const [kurul, setKurul] = useState('all');
  const [status, setStatus] = useState<Status>('all');
  const [limit, setLimit] = useState(PAGE);
  const [recent] = useState(readRecent);
  const [view, setViewState] = useState<View>(() => readPref<View>(VIEW_KEY, ['grid', 'list'], 'list'));
  const [sort, setSortState] = useState<Sort>(() => readPref<Sort>(SORT_KEY, Object.keys(SORT_LABEL) as Sort[], 'program'));
  const setView = (v: View) => { setViewState(v); writePref(VIEW_KEY, v); };
  const setSort = (v: Sort) => { setSortState(v); writePref(SORT_KEY, v); };
  const searchRef = useRef<HTMLInputElement>(null);
  const pdfIds = useDeckPdfIds();
  const pdfMissing = useDeckPdfMissing();

  // "/" arama kutusuna odaklanır (ders açıkken kısayol dersin)
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (e.key !== '/' || e.metaKey || e.ctrlKey || (t && /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) || t?.isContentEditable) return;
      if (document.querySelector('.ls-root')) return;
      if (!searchRef.current) return;
      e.preventDefault();
      searchRef.current.focus();
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

  // Bölüm başlığı sayıları tüm sonuçtan (sayfalanmış dilimden değil)
  const groupStats = useMemo(() => {
    const m = new Map<string, { n: number; done: number }>();
    visible.forEach((d) => {
      const g = branchOf(d);
      const s = m.get(g) || { n: 0, done: 0 };
      s.n += 1;
      if (stateOf(d, progress).status === 'done') s.done += 1;
      m.set(g, s);
    });
    return m;
  }, [visible, progress]);

  useEffect(() => setLimit(PAGE), [q, branch, kurul, status, archive, sort]);
  const shown = visible.slice(0, limit);
  const hasMore = visible.length > limit;
  // Gruplar sıralamadaki ilk görünüşlerine göre dizilir (Ders programı sırasında: ilk dersi önce olan dal önce)
  const groups = useMemo(() => {
    const m = new Map<string, DeckCatalogEntry[]>();
    shown.forEach((d) => {
      const g = branchOf(d);
      const l = m.get(g);
      if (l) l.push(d); else m.set(g, [d]);
    });
    return [...m.entries()];
  }, [shown]);

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

  const resume = useMemo(
    () => scoped.filter((d) => stateOf(d, progress).status === 'active').sort((a, b) => (recent[b.id] || 0) - (recent[a.id] || 0)).slice(0, RESUME_MAX),
    [scoped, progress, recent]
  );

  const filtered = !!q || branch !== 'all' || kurul !== 'all' || status !== 'all';
  const reset = () => {
    setInput('');
    setBranch('all');
    setKurul('all');
    setStatus('all');
  };

  const hocaOf = (d: DeckCatalogEntry) => String(d.instructor || schedOf(d)?.h || '').trim();
  const verOf = (d: DeckCatalogEntry) => {
    const ver = versions?.[d.id];
    if (!ver) return null;
    const cur = String(d.versionLabel || ver[ver.length - 1]);
    return { cur, title: `Bu dersin ${ver.length} sürümü var (${ver.join(', ')}); açınca hangisini istediğini seçersin` };
  };

  /** Satır ve karonun ortak üst bilgi satırı: hoca · adım · sürüm · PDF · tekrar · kaynak uyarısı */
  const metaOf = (d: DeckCatalogEntry) => {
    const hoca = hocaOf(d);
    const pdf = !!pdfIds?.has(d.id);
    const ver = verOf(d);
    const due = review.counts[d.id]?.due ?? 0;
    const noSrc = !pdf && unknownSource(pdfMissing?.[d.id]);
    const sc = schedOf(d);
    return (
      <span className="l12-meta">
        <span className="l12-sub">
          {hoca && <>{hoca} · </>}
          <span className="l12-num">{d.slideCount || 0}</span> adım
          {sc?.t && <span className="l12-date"> · {trDate(sc.t)}</span>}
        </span>
        {ver && <span className="l12-badge is-acc" title={ver.title}>{ver.cur}<span className="sr-only"> sürümü; başka sürümü de var</span></span>}
        {pdf && (
          <button type="button" className="l12-badge l12-pdf" onClick={() => onOpen(d.id, true)} title="Ders slaytını (PDF) aç" aria-label={`${deckName(d)} slayt PDF'ini aç`}>
            PDF
          </button>
        )}
        {due > 0 && (
          <span className="l12-badge is-warn" title="Bu derste tekrar zamanı gelen hata defteri ögeleri">
            <RotateCcw aria-hidden /><span className="l12-num">{due}</span> tekrar
          </span>
        )}
        {noSrc && (
          <span className="l12-badge" title={`Bu dersin 2026-27 slaytı Drive'da yok${pdfMissing?.[d.id] ? ` (ders ${trDate(pdfMissing[d.id])})` : ''}; içerik önceki yılın kaynağından hazırlandı, hangi PDF'e ait olduğu bilinmiyor.`}>
            <FileQuestionMark aria-hidden />Kaynak?<span className="sr-only"> kaynak PDF bilinmiyor</span>
          </span>
        )}
      </span>
    );
  };

  /** Bitirdim / Bitti + Tekrar et (konu takibi; tüm adımlar görüldüyse kendiliğinden bitti) */
  const takipDugme = (d: DeckCatalogEntry, s: ReturnType<typeof stateOf>) => (
    <KonuDugmeleri kucuk className="l12-takip" modul="ogren" konu={ogrenTakipId(d.id)} ad={deckName(d, false)} turetilen={s.status === 'done'}
      onTekrar={() => (onRestart ? onRestart(d.id) : onOpen(d.id))} />
  );

  const openLabel = (d: DeckCatalogEntry, s: ReturnType<typeof stateOf>) =>
    `${deckName(d, false)} — ${s.status === 'done' ? 'tamamlandı' : s.status === 'active' ? `%${s.pct}, devam et` : 'başla'}`;

  const sortQuick = {
    id: 'sirala',
    label: 'Sırala',
    value: sort !== 'program' ? SORT_LABEL[sort] : undefined,
    onClear: () => setSort('program'),
    content: (close: () => void) => (
      <QuickOptions close={close} value={sort} onPick={(v) => setSort(v as Sort)} options={(Object.keys(SORT_LABEL) as Sort[]).map((id) => ({
        id, label: SORT_LABEL[id], hint: id === 'program' ? 'kurul ve ders günü sırası' : undefined,
      }))} />
    ),
  };

  // Boş durum açıklaması: hangi süzgeç boşalttı, durum Tümü olsa kaç ders çıkardı
  const emptyText = () => {
    const parts = [status !== 'all' ? STATUS_LABEL[status] : '', kurul !== 'all' ? kurul : '', branch !== 'all' ? branch : ''].filter(Boolean);
    const head = q
      ? `“${query.trim()}” için ${status !== 'all' ? `${STATUS_LABEL[status].toLocaleLowerCase('tr-TR')} ` : ''}ders yok`
      : scoped.length === 0 ? 'Henüz ders yok' : 'Bu süzgeçte ders yok';
    const hint = status !== 'all' && byQuery.length > 0
      ? `Durumu Tümü yaparsan ${q ? 'bu konu ' : ''}${byQuery.length.toLocaleString('tr-TR')} derste ${q ? 'geçiyor' : 'var'}.`
      : scoped.length === 0 ? 'Yayındaki dersler burada listelenir.' : 'Süzgeçleri temizleyip tüm derslere dönebilirsin.';
    return { head, sub: [parts.length ? `Süzgeç: ${parts.join(' · ')}.` : '', hint].filter(Boolean).join(' ') };
  };

  return (
    <div className="l12">
      <header className="l12-head">
        <h1 className="l12-h1">Etkileşimli dersler</h1>
        <span className="l12-head-m">
          {kurul !== 'all' && <>{kurul} · </>}
          <span className="l12-num">{scoped.length.toLocaleString('tr-TR')}</span> ders
        </span>
      </header>

      <div className="l12-tool" role="search">
        <label className="l12-search">
          <Search aria-hidden />
          <input
            ref={searchRef}
            data-page-search
            type="search"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Escape' && input) { e.preventDefault(); setInput(''); } }}
            placeholder="Ders ya da konu ara"
            aria-label="Derslerde ara"
          />
          <kbd className="l12-kbd" aria-hidden>/</kbd>
        </label>
        <div className="l12-seg" role="radiogroup" aria-label="Durum">
          {(['all', 'active', 'done'] as Status[]).map((s) => (
            <button key={s} type="button" role="radio" aria-checked={status === s} className={status === s ? 'is-on' : ''} onClick={() => setStatus(s)}>
              {STATUS_LABEL[s]}
              {s !== 'all' && statusCount[s] > 0 && <span className="l12-seg-n">{statusCount[s]}</span>}
            </button>
          ))}
        </div>
        <div className="l12-pills">
          {kurullar.length > 1 && (
            <QuickPill q={{
              id: 'kurul',
              label: 'Kurul',
              value: kurul !== 'all' ? kurul.replace(/^Kurul\s*/, '') : undefined,
              onClear: () => setKurul('all'),
              content: (close) => (
                <QuickOptions close={close} value={kurul} onPick={setKurul}
                  options={[{ id: 'all', label: 'Tüm kurullar', count: scoped.length }, ...kurullar.map(([k, n]) => ({ id: k, label: k, count: n }))]} />
              ),
            }} />
          )}
          {branches.length > 1 && (
            <QuickPill q={{
              id: 'ders',
              label: 'Ders',
              value: branch !== 'all' ? branch : undefined,
              onClear: () => setBranch('all'),
              content: (close) => (
                <QuickOptions close={close} value={branch} onPick={setBranch} searchable={branches.length > 8} placeholder="Ders ara"
                  options={[{ id: 'all', label: 'Tüm dersler', count: scoped.length }, ...branches.map(([g, n]) => ({ id: g, label: g, count: n }))]} />
              ),
            }} />
          )}
          <QuickPill q={sortQuick} />
          {isAdmin && (
            <QuickPill q={{
              id: 'kume',
              label: 'Küme',
              value: archive !== 'new_only' ? (archive === 'all' ? 'Tümü' : 'Arşiv') : undefined,
              onClear: () => onArchive('new_only'),
              content: (close) => (
                <QuickOptions close={close} value={archive} onPick={(v) => onArchive(v as ArchiveFilter)} options={[
                  { id: 'new_only', label: 'Yayında', count: counts.published },
                  { id: 'legacy_only', label: 'Arşiv', count: counts.legacy, hint: 'yönetici' },
                  { id: 'all', label: 'Tümü', count: all.length },
                ]} />
              ),
            }} />
          )}
        </div>
        <span className="l12-grow" />
        <div className="l12-view" role="radiogroup" aria-label="Görünüm">
          <button type="button" role="radio" aria-checked={view === 'list'} aria-label="Liste görünümü" title="Liste" onClick={() => setView('list')}><List aria-hidden /></button>
          <button type="button" role="radio" aria-checked={view === 'grid'} aria-label="Izgara görünümü" title="Izgara" onClick={() => setView('grid')}><LayoutGrid aria-hidden /></button>
        </div>
      </div>

      {!filtered && resume.length > 0 && (
        <section className="l12-panel" aria-labelledby="l12-cont-h">
          <div className="l12-panel-h">
            <h2 className="l12-h2" id="l12-cont-h">Devam et</h2>
            <span className="l12-m">son açılana göre</span>
          </div>
          <ul className="l12-cont-list">
            {resume.map((d, i) => {
              const s = stateOf(d, progress);
              const when = ago(recent[d.id]);
              return (
                <li key={d.id} className="l12-cont">
                  <span className="l12-main">
                    <span className="l12-t">{deckName(d, false)}</span>
                    <span className="l12-sub">Adım <span className="l12-num">{s.last} / {d.slideCount}</span>{when && <> · {when}</>}</span>
                  </span>
                  <Prog pct={s.pct} />
                  <button type="button" className={`l12-btn${i === 0 ? ' is-pri' : ''}`} onClick={() => onOpen(d.id)} aria-label={`${deckName(d, false)} — devam et, %${s.pct}`}>
                    Devam et
                  </button>
                </li>
              );
            })}
          </ul>
        </section>
      )}

      {!filtered && onOpenReview && review.total.open > 0 && (
        <button type="button" className="l12-panel l12-link" onClick={() => onOpenReview()}>
          <span className="l12-lead" aria-hidden><RotateCcw /></span>
          <span className="l12-link-t">
            Hata defteri <span className="l12-m">· yanlış yaptığın etkileşimler tekrar sırasında</span>
          </span>
          {review.total.due > 0
            ? <span className="l12-badge is-warn"><span className="l12-num">{review.total.due}</span>&nbsp;vadesi geldi</span>
            : <span className="l12-badge"><span className="l12-num">{review.total.open}</span>&nbsp;öge</span>}
          <ChevronRight className="l12-chev" aria-hidden />
        </button>
      )}

      {visible.length === 0 ? (
        <div className="l12-empty" role="status">
          <span className="l12-empty-t">
            <b>{emptyText().head}</b>
            <span className="l12-m">{emptyText().sub}</span>
          </span>
          {filtered && <button type="button" className="l12-btn" onClick={reset}>Süzgeci temizle</button>}
        </div>
      ) : (
        <>
          {groups.map(([g, list]) => {
            const st = groupStats.get(g) || { n: list.length, done: 0 };
            const hid = `l12-g-${g.replace(/[^\p{L}\p{N}]+/gu, '-')}`;
            return (
              <section key={g} className="l12-group" aria-labelledby={hid}>
                <div className="l12-gh">
                  <h2 className="l12-h2" id={hid}>{g}</h2>
                  <span className="l12-m">
                    <span className="l12-num">{st.n}</span> ders{st.done > 0 && <> · <span className="l12-num">{st.done}</span> bitti</>}
                  </span>
                </div>
                {view === 'list' ? (
                  <ul className="l12-panel l12-list">
                    {list.map((d) => {
                      const s = stateOf(d, progress);
                      return (
                        <li key={d.id} className={`l12-row is-${s.status}`}>
                          <span className="l12-main">
                            <button type="button" className="l12-open l12-t" onClick={() => onOpen(d.id)} aria-label={openLabel(d, s)}>
                              {deckName(d, false)}
                            </button>
                            {metaOf(d)}
                            <KonuSureEtiketi modul="ogren" konu={ogrenTakipId(d.id)} />
                          </span>
                          <Prog pct={s.pct} done={s.status === 'done'} />
                          {takipDugme(d, s)}
                        </li>
                      );
                    })}
                  </ul>
                ) : (
                  <ul className="l12-grid">
                    {list.map((d) => {
                      const s = stateOf(d, progress);
                      return (
                        <li key={d.id} className={`l12-panel l12-tile is-${s.status}`}>
                          <button type="button" className="l12-open l12-t l12-tile-t" onClick={() => onOpen(d.id)} aria-label={openLabel(d, s)}>
                            {deckName(d, false)}
                          </button>
                          {metaOf(d)}
                          <KonuSureEtiketi modul="ogren" konu={ogrenTakipId(d.id)} />
                          <span className="l12-tile-f">
                            <Prog pct={s.pct} done={s.status === 'done'} />
                            {takipDugme(d, s)}
                          </span>
                        </li>
                      );
                    })}
                  </ul>
                )}
              </section>
            );
          })}
          {hasMore && (
            <div ref={sentinel} className="l12-more">
              <button type="button" className="l12-btn" onClick={() => setLimit((v) => v + PAGE)}>
                Daha fazla göster (<span className="l12-num">{(visible.length - limit).toLocaleString('tr-TR')}</span>)
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default LearnLibraryV12;
