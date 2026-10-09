/**
 * Öğren açılış sayfası: kaldığın dersler, ders/durum filtreleri, arama ve ders kartları.
 * İlerleme InteractiveDeckView'in tuttuğu `medsoru_learn_progress_v1` kaydından okunur;
 * son açılma zamanı burada `medsoru_learn_recent_v1` içinde tutulur.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowRight, BookOpen, Check, FileText, HelpCircle, Layers, Lock, Play, Search, X } from 'lucide-react';
import { deckName, type DeckCatalogEntry } from '../../data/deckStore';
import { getDeckOriginalPdf } from '../../data/deckPdfCatalog';

type Progress = Record<string, { last?: number; seen?: number[] } | undefined>;
type Status = 'all' | 'active' | 'new' | 'done';
export type ArchiveFilter = 'new_only' | 'all' | 'legacy_only';

const RECENT_KEY = 'medsoru_learn_recent_v1';
const readRecent = (): Record<string, number> => {
  try {
    return JSON.parse(localStorage.getItem(RECENT_KEY) || '{}');
  } catch {
    return {};
  }
};
export const touchRecent = (id: string) => {
  try {
    localStorage.setItem(RECENT_KEY, JSON.stringify({ ...readRecent(), [id]: Date.now() }));
  } catch {
    /* ignore */
  }
};

/** "Enfeksiyon Hastalıkları / Klinik Mikrobiyoloji" → "Enfeksiyon Hastalıkları" */
export const disciplineGroup = (raw: string) => (raw || 'Diğer').split(/\s*(?:\/|&|,|\sve\s)\s*/)[0].trim() || 'Diğer';

const DOTS: Record<string, string> = {
  'Tıbbi Patoloji': '#E0566E',
  'Enfeksiyon Hastalıkları': '#1F9D55',
  'Halk Sağlığı': '#2B8BC6',
  'Tıbbi Genetik': '#6D5BD0',
  Üroloji: '#E0952B',
};
const FALLBACK = ['#0F7A5F', '#B4233C', '#4A5868', '#9A4D06', '#1E4FD8'];
export const groupDot = (g: string) => DOTS[g] || FALLBACK[[...g].reduce((n, ch) => n + ch.charCodeAt(0), 0) % FALLBACK.length];

/** k1p-k1-07-… → 7 ; sıra numarası olmayan desteler sona */
const orderOf = (d: DeckCatalogEntry) => {
  const m = /-k\d+-(\d+)/.exec(d.id);
  return m ? Number(m[1]) : 999;
};
const isPublished = (d: DeckCatalogEntry) => !!(d.isNew || String(d.version || '').startsWith('2') || (d.slideCount && d.slideCount >= 50) || ((d as any).totalSlides && (d as any).totalSlides >= 50));

const stateOf = (d: DeckCatalogEntry, p: Progress) => {
  const seen = p[d.id]?.seen?.length || 0;
  const pct = d.slideCount ? Math.min(100, Math.round((seen / d.slideCount) * 100)) : 0;
  const status: Exclude<Status, 'all'> = seen === 0 ? 'new' : seen >= d.slideCount ? 'done' : 'active';
  return { seen, pct, status, last: (p[d.id]?.last ?? 0) + 1 };
};

const Ring: React.FC<{ pct: number; done?: boolean }> = ({ pct, done }) => (
  <span className={`lh-ring ${done ? 'is-done' : ''}`} style={{ ['--p' as string]: pct }} aria-hidden>
    {done ? <Check /> : <b>{pct}</b>}
  </span>
);

export const LearnHub: React.FC<{
  decks: DeckCatalogEntry[];
  progress: Progress;
  isAdmin?: boolean;
  archive: ArchiveFilter;
  onArchive: (f: ArchiveFilter) => void;
  onOpen: (id: string, pdf?: boolean) => void;
}> = ({ decks: all, progress, isAdmin, archive, onArchive, onOpen }) => {
  const [query, setQuery] = useState('');
  const [group, setGroup] = useState('all');
  const [status, setStatus] = useState<Status>('all');
  const [recent] = useState(readRecent);
  const searchRef = useRef<HTMLInputElement>(null);

  // "/" arama kutusuna odaklanır
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (e.key !== '/' || e.metaKey || e.ctrlKey || (t && /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) || t?.isContentEditable) return;
      e.preventDefault();
      searchRef.current?.focus();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const counts = useMemo(() => ({
    published: all.filter(isPublished).length,
    legacy: all.filter((d) => !isPublished(d)).length,
  }), [all]);

  // Öğrenci yalnız yayındaki dersleri görür (hiç yoksa hepsini); yönetici arşivi de seçebilir
  const scoped = useMemo(() => {
    const f = isAdmin ? archive : 'new_only';
    const list = f === 'all' ? all : f === 'legacy_only' ? all.filter((d) => !isPublished(d)) : all.filter(isPublished);
    return (list.length || isAdmin ? list : all).slice().sort((a, b) => orderOf(a) - orderOf(b) || deckName(a).localeCompare(deckName(b), 'tr'));
  }, [all, isAdmin, archive]);

  const groups = useMemo(() => {
    const m = new Map<string, number>();
    scoped.forEach((d) => m.set(disciplineGroup(d.discipline), (m.get(disciplineGroup(d.discipline)) || 0) + 1));
    return [...m.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'tr'));
  }, [scoped]);
  useEffect(() => {
    if (group !== 'all' && !groups.some(([g]) => g === group)) setGroup('all');
  }, [groups, group]);

  const q = query.trim().toLocaleLowerCase('tr-TR');
  const byQuery = useMemo(
    () => scoped.filter((d) => (group === 'all' || disciplineGroup(d.discipline) === group) && (!q || [d.title, d.shortTitle, d.discipline, d.instructor, d.overview, ...(d.highYieldPearls || [])].join(' ').toLocaleLowerCase('tr-TR').includes(q))),
    [scoped, group, q]
  );
  const statusCount = useMemo(() => {
    const c = { all: byQuery.length, active: 0, new: 0, done: 0 };
    byQuery.forEach((d) => { c[stateOf(d, progress).status] += 1; });
    return c;
  }, [byQuery, progress]);
  const visible = status === 'all' ? byQuery : byQuery.filter((d) => stateOf(d, progress).status === status);

  // Kaldığın dersler: yarım kalanlar, en son açılan önce
  const resume = useMemo(
    () => scoped.filter((d) => stateOf(d, progress).status === 'active').sort((a, b) => (recent[b.id] || 0) - (recent[a.id] || 0)).slice(0, 3),
    [scoped, progress, recent]
  );

  const totals = useMemo(() => {
    let steps = 0;
    let seen = 0;
    let questions = 0;
    scoped.forEach((d) => {
      steps += d.slideCount || 0;
      seen += Math.min(d.slideCount || 0, progress[d.id]?.seen?.length || 0);
      questions += d.questionCount || 0;
    });
    return { steps, seen, questions, pct: steps ? Math.round((seen / steps) * 100) : 0 };
  }, [scoped, progress]);

  const filtered = !!q || group !== 'all' || status !== 'all';
  const reset = () => {
    setQuery('');
    setGroup('all');
    setStatus('all');
  };

  return (
    <div className="lh">
      <header className="lh-head">
        <div className="lh-title">
          <h1 className="ms-page-title m-0">Öğren</h1>
          <p>Ders anlatımı, etkinlikler ve çıkmış sorularla adım adım çalış.</p>
        </div>
        <dl className="lh-stats">
          <div><dt>Ders</dt><dd>{scoped.length}</dd></div>
          <div><dt>Adım</dt><dd>{totals.steps.toLocaleString('tr-TR')}</dd></div>
          <div><dt>Soru</dt><dd>{totals.questions.toLocaleString('tr-TR')}</dd></div>
          <div className="is-accent"><dt>İlerleme</dt><dd>%{totals.pct}</dd></div>
        </dl>
      </header>

      {resume.length > 0 && !filtered && (
        <section className="lh-resume" aria-label="Kaldığın dersler">
          {resume.map((d, i) => {
            const s = stateOf(d, progress);
            const g = disciplineGroup(d.discipline);
            return (
              <button key={d.id} type="button" className={`lh-res ${i === 0 ? 'is-main' : ''}`} onClick={() => onOpen(d.id)}>
                <Ring pct={s.pct} />
                <span className="lh-res-body">
                  <small><i style={{ background: groupDot(g) }} />{i === 0 ? 'Kaldığın yer' : g} · Adım {s.last}/{d.slideCount}</small>
                  <b>{deckName(d)}</b>
                </span>
                <span className="lh-res-go">{i === 0 ? <>Devam et <ArrowRight /></> : <ArrowRight />}</span>
              </button>
            );
          })}
        </section>
      )}

      <div className="lh-tools">
        <label className="lh-search">
          <Search aria-hidden />
          <span className="sr-only">Derslerde ara</span>
          <input ref={searchRef} type="search" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Ders, konu ya da kavram ara" />
          {query ? (
            <button type="button" onClick={() => setQuery('')} aria-label="Aramayı temizle"><X /></button>
          ) : (
            <kbd className="ms-kbd lh-kbd">/</kbd>
          )}
        </label>
        <div className="ms-seg" role="radiogroup" aria-label="Durum">
          {([['all', 'Tümü'], ['active', 'Devam eden'], ['new', 'Başlanmadı'], ['done', 'Biten']] as [Status, string][]).map(([k, l]) => (
            <button key={k} type="button" role="radio" aria-checked={status === k} onClick={() => setStatus(k)} disabled={k !== 'all' && statusCount[k] === 0 && status !== k}>
              {l} <span className="n">{statusCount[k]}</span>
            </button>
          ))}
        </div>
        {isAdmin && (
          <div className="lh-admin" title="Yalnız yöneticiler görür">
            <Lock aria-hidden />
            <div className="ms-seg" role="radiogroup" aria-label="Yönetici: deste kümesi">
              {([['new_only', 'Yayında', counts.published], ['legacy_only', 'Arşiv', counts.legacy], ['all', 'Tümü', all.length]] as [ArchiveFilter, string, number][]).map(([k, l, n]) => (
                <button key={k} type="button" role="radio" aria-checked={archive === k} onClick={() => onArchive(k)}>
                  {l} <span className="n">{n}</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {groups.length > 1 && (
        <div className="ms-chipbar" role="radiogroup" aria-label="Ders dalı">
          {[['all', scoped.length] as [string, number], ...groups].map(([g, n]) => (
            <button key={g} type="button" role="radio" aria-checked={group === g} className={`ms-chip ${group === g ? 'is-on' : ''}`} onClick={() => setGroup(g)}>
              {g !== 'all' && <span className="lh-dot" style={{ background: groupDot(g) }} aria-hidden />}
              {g === 'all' ? 'Tüm dallar' : g}
              <span className="ms-chip-count">{n}</span>
            </button>
          ))}
        </div>
      )}

      {visible.length === 0 ? (
        <div className="ms-empty lh-empty">
          <Search aria-hidden />
          <b>{q ? `“${query.trim()}” için ders yok` : 'Bu filtrede ders yok'}</b>
          <p>Filtreleri temizleyip tüm derslere dönebilirsin.</p>
          <button type="button" className="ms-btn is-tonal" onClick={reset}>Filtreleri temizle</button>
        </div>
      ) : (
        <ul className="lh-grid">
          {visible.map((d, i) => {
            const s = stateOf(d, progress);
            const g = disciplineGroup(d.discipline);
            const pdf = !!getDeckOriginalPdf(d.id);
            const no = orderOf(d);
            return (
              <li key={d.id} className="lh-card" style={{ animationDelay: `${Math.min(i, 14) * 22}ms` }}>
                <button type="button" className="lh-card-main" onClick={() => onOpen(d.id)} aria-label={`${deckName(d, false)} — ${s.status === 'done' ? 'tamamlandı' : s.status === 'active' ? `%${s.pct}, devam et` : 'başla'}`}>
                  <span className="lh-card-top">
                    <span className="lh-card-g"><i style={{ background: groupDot(g) }} />{g}</span>
                    {no < 999 && <span className="lh-card-no">{String(no).padStart(2, '0')}</span>}
                  </span>
                  <b className="lh-card-t" title={deckName(d, false)}>{deckName(d, false)}</b>
                  <span className="lh-card-meta">
                    <span><Layers aria-hidden />{d.slideCount} adım</span>
                    {d.questionCount > 0 && <span><HelpCircle aria-hidden />{d.questionCount} soru</span>}
                    {d.cardCount > 0 && <span><BookOpen aria-hidden />{d.cardCount} kart</span>}
                  </span>
                  <span className="lh-card-foot">
                    <span className={`lh-bar ${s.status === 'done' ? 'is-done' : ''}`} aria-hidden><i style={{ width: `${s.pct}%` }} /></span>
                    <span className={`lh-state is-${s.status}`}>
                      {s.status === 'done' ? <><Check aria-hidden />Bitti</> : s.status === 'active' ? `%${s.pct}` : <><Play aria-hidden />Başla</>}
                    </span>
                  </span>
                </button>
                {pdf && (
                  <button type="button" className="lh-card-pdf" onClick={() => onOpen(d.id, true)} title="Ders slaytını (PDF) aç" aria-label={`${deckName(d)} slayt PDF'ini aç`}>
                    <FileText />
                  </button>
                )}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
};
