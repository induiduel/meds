/**
 * Öğren açılış sayfası: kaldığın dersler, ders/durum filtreleri, arama ve ders kartları.
 * İlerleme InteractiveDeckView'in tuttuğu `medsoru_learn_progress_v1` kaydından okunur;
 * son açılma zamanı burada `medsoru_learn_recent_v1` içinde tutulur.
 */
import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowRight, Check, FileText, Lock, Play, Search, X } from 'lucide-react';
import { deckName, type DeckCatalogEntry } from '../../data/deckStore';
import { useDeckPdfIds } from '../../services/deckPdfService';
import { disciplineClass } from '../../utils/discipline';
import { Segmented } from '../ui/kit';

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

/** İki (ya da daha çok) sürümü olan dersin satırda görünen işareti: üst üste binmiş sürüm kartları, en yenisi önde. */
const VersionStack: React.FC<{ labels: string[] }> = ({ labels }) => {
  const shown = labels.slice(-3);
  return (
    <span className="lcx-ver" title={`Bu dersin ${labels.length} sürümü var (${labels.join(', ')}) — açınca seçersin`}>
      <span className="lcx-ver-stack" aria-hidden>
        {shown.map((l, i) => <i key={l} className={i === shown.length - 1 ? 'is-new' : ''}>{l}</i>)}
      </span>
      <small><span className="sr-only">Bu dersin </span>{labels.length} sürüm</small>
    </span>
  );
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
  /** Sürümlü dersler: grup (V1) kimliği → sürüm etiketleri (["V1", "V2"]) */
  versions?: Record<string, string[]>;
}> = ({ decks: all, progress, isAdmin, archive, onArchive, onOpen, versions }) => {
  const [query, setQuery] = useState('');
  const [group, setGroup] = useState('all');
  const [status, setStatus] = useState<Status>('all');
  const [recent] = useState(readRecent);
  const searchRef = useRef<HTMLInputElement>(null);
  const pdfIds = useDeckPdfIds(); // sunucuda dosyası ya da Drive kimliği olan desteler

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
    let cards = 0;
    scoped.forEach((d) => {
      steps += d.slideCount || 0;
      seen += Math.min(d.slideCount || 0, progress[d.id]?.seen?.length || 0);
      cards += d.cardCount || d.flashcardCount || 0;
    });
    return { steps, seen, cards, pct: steps ? Math.round((seen / steps) * 100) : 0 };
  }, [scoped, progress]);

  const filtered = !!q || group !== 'all' || status !== 'all';
  const reset = () => {
    setQuery('');
    setGroup('all');
    setStatus('all');
  };

  return (
    <div className="lh">
      <header className="cx-page">
        <div className="cx-head">
          <h1 className="ms-page-title cx-title">Öğren</h1>
          <span className="cx-count" aria-live="polite">
            <span className="cx-stat">{scoped.length} <small>ders</small></span>
            <span className="cx-stat"><i aria-hidden>·</i>{totals.steps.toLocaleString('tr-TR')} <small>adım</small></span>
            <span className="cx-stat"><i aria-hidden>·</i>{totals.cards.toLocaleString('tr-TR')} <small>kart</small></span>
            {totals.pct > 0 && <span className="cx-stat is-accent"><i aria-hidden>·</i>%{totals.pct} <small>ilerleme</small></span>}
          </span>
        </div>
      </header>

      {resume.length > 0 && !filtered && (
        <section className="lh-resume" aria-label="Kaldığın dersler">
          {resume.map((d, i) => {
            const s = stateOf(d, progress);
            const g = disciplineGroup(d.discipline);
            return (
              <button key={d.id} type="button" className={`lh-res ${i === 0 ? 'is-main' : ''} ${disciplineClass(g)}`} onClick={() => onOpen(d.id)}>
                <Ring pct={s.pct} />
                <span className="lh-res-body">
                  <small><i className="hk-dot" />{i === 0 ? 'Kaldığın yer' : g} · Adım {s.last}/{d.slideCount}</small>
                  <b>{deckName(d)}</b>
                </span>
                <span className="lh-res-go">{i === 0 ? <>Devam et <ArrowRight /></> : <ArrowRight />}</span>
              </button>
            );
          })}
        </section>
      )}

      <div className="cx-dock lh-dock">
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
          <Segmented<Status>
            className="lh-status"
            label="Durum"
            value={status}
            onChange={setStatus}
            options={([['all', 'Tümü'], ['active', 'Sürüyor'], ['new', 'Yeni'], ['done', 'Biten']] as [Status, string][]).map(([k, l]) => ({
              value: k,
              label: <>{l} <span className="lh-n">{statusCount[k]}</span></>,
            }))}
          />
          {isAdmin && (
            <div className="lh-admin" title="Yalnız yöneticiler görür">
              <Lock aria-hidden />
              <Segmented<ArchiveFilter>
                label="Yönetici: deste kümesi"
                value={archive}
                onChange={onArchive}
                options={([['new_only', 'Yayında', counts.published], ['legacy_only', 'Arşiv', counts.legacy], ['all', 'Tümü', all.length]] as [ArchiveFilter, string, number][]).map(([k, l, n]) => ({
                  value: k,
                  label: <>{l} <span className="lh-n">{n}</span></>,
                }))}
              />
            </div>
          )}
        </div>

        {groups.length > 1 && (
          <nav className="cx-tabs" aria-label="Ders dalı">
            {[['all', scoped.length] as [string, number], ...groups].map(([g, n]) => (
              <button key={g} type="button" aria-pressed={group === g} className={`cx-tab ${group === g ? 'is-on' : ''} ${g !== 'all' ? disciplineClass(g) : ''}`} onClick={() => setGroup(g)}>
                {g !== 'all' && <i className="hk-dot" aria-hidden />}
                {g === 'all' ? 'Tüm dallar' : g}
                <small>{n}</small>
              </button>
            ))}
          </nav>
        )}
      </div>

      {visible.length === 0 ? (
        <div className="ui-card lh-empty">
          <Search aria-hidden />
          <b>{q ? `“${query.trim()}” için ders yok` : 'Bu filtrede ders yok'}</b>
          <p>Filtreleri temizleyip tüm derslere dönebilirsin.</p>
          <button type="button" className="ui-btn is-tonal" onClick={reset}>Süzgeçleri temizle</button>
        </div>
      ) : (
        <div className="lcx">
          {(() => {
            // Ders dalına göre gruplu, tek satırlı liste (canvas "LearnCatalog")
            const byGroup = new Map<string, typeof visible>();
            visible.forEach((d) => {
              const g = disciplineGroup(d.discipline);
              byGroup.set(g, [...(byGroup.get(g) || []), d]);
            });
            return [...byGroup.entries()].map(([g, decks]) => (
              <section key={g} className={`lcx-g ${disciplineClass(g)}`} aria-label={g}>
                <header className="lcx-gh"><i className="hk-dot" aria-hidden /><b>{g}</b><span>{decks.length} deste</span></header>
                <ul>
                  {decks.map((d) => {
                    const s = stateOf(d, progress);
                    const pdf = !!pdfIds?.has(d.id);
                    const no = orderOf(d);
                    const ver = versions?.[d.id];
                    return (
                      <li key={d.id} className={`lcx-row${ver ? ' has-ver' : ''}`}>
                        <button type="button" className="lcx-main" onClick={() => onOpen(d.id)} aria-label={`${deckName(d, false)} — ${s.status === 'done' ? 'tamamlandı' : s.status === 'active' ? `%${s.pct}, devam et` : 'başla'}`}>
                          {no < 999 && <span className="lcx-no">{String(no).padStart(2, '0')}</span>}
                          <span className="lcx-t">
                            <span className="lcx-tl">
                              <b title={deckName(d, false)}>{deckName(d, false)}</b>
                              {ver && <VersionStack labels={ver} />}
                            </span>
                            <span>{d.slideCount} adım{d.cardCount > 0 ? ` · ${d.cardCount} kart` : ''}{s.status === 'active' ? ` · %${s.pct}` : ''}</span>
                          </span>
                          {s.status === 'done' ? (
                            <span className="cx-flag is-ok"><Check aria-hidden />Bitti</span>
                          ) : s.status === 'active' ? (
                            <span className="lcx-bar" aria-hidden><i style={{ width: `${s.pct}%` }} /></span>
                          ) : (
                            <span className="lcx-start"><Play aria-hidden />Başla</span>
                          )}
                          <ArrowRight className="lcx-go" aria-hidden />
                        </button>
                        {pdf && (
                          <button type="button" className="qk-ib" onClick={() => onOpen(d.id, true)} title="Ders slaytını (PDF) aç" aria-label={`${deckName(d)} slayt PDF'ini aç`}>
                            <FileText aria-hidden />
                          </button>
                        )}
                      </li>
                    );
                  })}
                </ul>
              </section>
            ));
          })()}
        </div>
      )}
    </div>
  );
};
