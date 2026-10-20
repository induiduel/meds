/**
 * Çıkmış sorular — v12 "Net" (canvas panosu Cikmis.dc.html). Yalnız data-design='v12' iken PastExamsView'in v12 dalından
 * çizilir; v10/v11 araç çubuğu (PageToolbar) olduğu gibi kalır. Bütün durum ve işleyiciler PastExamsView'dendir
 * (süzme, sayılar, sıralama orada hesaplanır); bu bileşen yalnız yerleşimi kurar.
 *
 * Yapı:
 *  - Başlık satırı: "Çıkmış sorular" · n soru · kapsam · (yönetici) Faz 14 · Kart | Kompakt · Test oluştur
 *  - Araç satırı: arama ("/") · Tümü / Çözülmedi / Yanlışlar / Kaydedilen · Kurul ▾ · Yıl ▾ · Ders ▾ (· Konu ▾)
 *    · "Süzgeç n" · Basit | Gelişmiş (ayar: Görünüm › Süzgeç modu, appearance.filters)
 *  - Gelişmiş modda solda süzgeç sütunu (tüm süzgeçler, sıralama, "Görünümü kaydet", kayıtlı görünümler);
 *    dar kapta (< 820 px) aynı sütun alt sayfada açılır.
 *  - Sonuç başlığı: "n soru, m gösteriliyor" · Etiketler anahtarı (appearance.qtags) · Sıralama
 *  - Sonuçlar: PastExamsView'in mevcut kart listesi (children)
 * Stil: styles/v12/cikmis.css (.c12-*; v12'de ck-* kartını da panoya göre yeniden çizer).
 */
import React, { startTransition, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { ArrowUpDown, BookOpen, Bookmark, RefreshCw, Search, SlidersHorizontal, Sparkles, Tag, X } from 'lucide-react';
import { useAppearance } from '../../utils/appearance';
import { QuickOptions, QuickPill, type ToolbarQuick } from '../ui/PageToolbar';
import { Sheet } from '../ui/Sheet';
import { CikmisViewSwitch, type CikmisGorunum } from '../cikmis/CikmisViewSwitch';
import '../../styles/v12/cikmis.css';
import '../../styles/v13/cikmis.css';

export interface C12Option { id: string; label: string; count?: number; group?: string }
export interface C12Facet { id: string; label: string; value: string; options: C12Option[]; onPick: (v: string) => void }
export type C12Status = 'all' | 'unsolved' | 'wrong' | 'saved';
type Pick = { value: string; options: C12Option[]; onPick: (v: string) => void; label?: string };

export interface CikmisV12Props {
  /** Süzgeçlere uyan soru sayısı */
  total: number;
  /** Ekranda çizilen soru sayısı */
  shown: number;
  /** Başlıktaki kapsam (seçili kurulun kısa adı) */
  scope?: string;
  search: { value: string; onChange: (v: string) => void };
  suggest: { disciplines: [string, number][]; topics: [string, number][]; onDiscipline: (d: string) => void; onTopic: (t: string) => void };
  status: { value: C12Status; counts: Record<C12Status, number>; onPick: (v: C12Status) => void };
  committee: Pick | null;
  year: Pick;
  discipline: Pick;
  topic: Pick | null;
  sort: Pick;
  /** Sütundaki tek seçimli süzgeç grupları (Cevap, Açıklama, Tekrar, Havuz, Yenilik, Metin) */
  facets: C12Facet[];
  /** Yalnız yönetici: karantina, kaynak, denetleyici… */
  adminFacets?: C12Facet[];
  /** Hızlı haplarda görünmeyen etkin süzgeçler (kaldırılabilir) */
  chips: { label: string; onRemove: () => void }[];
  anyFilter: boolean;
  onClearAll: () => void;
  quiz: { on: boolean; onToggle: () => void };
  view: { value: CikmisGorunum; onChange: (v: CikmisGorunum) => void };
  adminHref?: string;
  practiceHref: string;
  sync: { busy: boolean; onSync: () => void; deviceCount: number };
  views: { snapshot: () => Record<string, string>; apply: (s: Record<string, string>) => void; suggestName: () => string };
  children: React.ReactNode;
}

const STATUS: [C12Status, string][] = [['all', 'Tümü'], ['unsolved', 'Çözülmedi'], ['wrong', 'Yanlışlar'], ['saved', 'Kaydedilen']];
const WIDE_AT = 820;
const SMALL_AT = 560;
const DISC_SHOWN = 8;
const VIEWS_KEY = 'medsoru_cikmis_kayitli_gorunumler';
const VIEWS_MAX = 12;
interface SavedView { id: string; name: string; state: Record<string, string>; at: number }
const readViews = (): SavedView[] => {
  try {
    const v = JSON.parse(localStorage.getItem(VIEWS_KEY) || '[]');
    return Array.isArray(v) ? v.filter((x) => x && typeof x.name === 'string' && x.state && typeof x.state === 'object') : [];
  } catch { return []; }
};
const writeViews = (v: SavedView[]) => { try { localStorage.setItem(VIEWS_KEY, JSON.stringify(v)); } catch { /* gizli pencere */ } };
const tr = (v: number) => v.toLocaleString('tr-TR');
const sameState = (a: Record<string, string>, b: Record<string, string>) => {
  const ka = Object.keys(a), kb = Object.keys(b);
  return ka.length === kb.length && ka.every((k) => a[k] === b[k]);
};

/** Tek seçimli hap grubu (sütunda Yıl, Cevap, Açıklama…) */
const PillGroup: React.FC<{ f: C12Facet }> = ({ f }) => (
  <fieldset className="c12-fs">
    <legend className="c12-label">{f.label}</legend>
    <div className="c12-pills">
      {f.options.map((o) => {
        const on = o.id === f.value;
        return (
          <button key={o.id} type="button" aria-pressed={on} className={`c12-pill ${on ? 'is-on' : ''} ${o.count === 0 && !on ? 'is-zero' : ''}`} onClick={() => f.onPick(o.id)}>
            <span>{o.label}</span>
            {o.count != null && <b>{tr(o.count)}</b>}
          </button>
        );
      })}
    </div>
  </fieldset>
);

const SelectField: React.FC<{ id: string; label: string; p: Pick; all: string }> = ({ id, label, p, all }) => (
  <div>
    <label className="c12-label" htmlFor={id}>{label}</label>
    <div className="c12-field">
      <select id={id} value={p.value} onChange={(e) => p.onPick(e.target.value)}>
        {p.options.map((o) => (
          <option key={o.id} value={o.id}>{o.id === 'all' ? all : o.label}{o.count != null ? ` · ${tr(o.count)}` : ''}</option>
        ))}
      </select>
    </div>
  </div>
);

export const CikmisV12: React.FC<CikmisV12Props> = (p) => {
  const look = useAppearance();
  const adv = look.filters === 'gelismis';
  const rootRef = useRef<HTMLDivElement>(null);
  const asideRef = useRef<HTMLElement>(null);
  const [wide, setWide] = useState(true);
  const [small, setSmall] = useState(false);
  const [sheet, setSheet] = useState(false);

  // Kap genişliği: sütun yalnız geniş kapta yanda durur; dar kapta alt sayfa
  useLayoutEffect(() => {
    const el = rootRef.current;
    if (!el) return;
    const measure = () => { const w = el.clientWidth; setWide(w >= WIDE_AT); setSmall(w < SMALL_AT); };
    measure();
    if (typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  useEffect(() => { if (wide) setSheet(false); }, [wide]);

  // Arama: kutu yerel durumla anında güncellenir, liste süzmesi geçiş önceliğinde koşar
  const [q, setQ] = useState(p.search.value);
  const sentRef = useRef(p.search.value);
  useEffect(() => {
    if (p.search.value !== sentRef.current) { sentRef.current = p.search.value; setQ(p.search.value); }
  }, [p.search.value]);
  const typeQ = (v: string) => {
    setQ(v);
    sentRef.current = v;
    startTransition(() => p.search.onChange(v));
  };
  const [focus, setFocus] = useState(false);
  const blurT = useRef<number | undefined>(undefined);
  useEffect(() => () => window.clearTimeout(blurT.current), []);
  const showSuggest = focus && q.trim().length >= 2;

  // Kayıtlı görünümler (bu cihazda)
  const [views, setViews] = useState<SavedView[]>(readViews);
  const [naming, setNaming] = useState<string | null>(null);
  const current = p.views.snapshot();
  const canSave = Object.keys(current).length > 0;
  const saveView = () => {
    const name = (naming || '').trim() || p.views.suggestName();
    const next = [{ id: `v${Date.now().toString(36)}`, name, state: current, at: Date.now() }, ...views.filter((v) => v.name !== name)].slice(0, VIEWS_MAX);
    setViews(next);
    writeViews(next);
    setNaming(null);
  };
  const removeView = (id: string) => {
    const next = views.filter((v) => v.id !== id);
    setViews(next);
    writeViews(next);
  };

  const [allDisc, setAllDisc] = useState(false);
  const activeCount = p.chips.length + (p.committee && p.committee.value !== 'all' ? 1 : 0) + (p.year.value !== 'all' ? 1 : 0) + (p.discipline.value !== 'all' ? 1 : 0) + (p.topic && p.topic.value !== 'all' ? 1 : 0);

  const setMode = (m: 'basit' | 'gelismis') => look.set({ filters: m });
  const openFilters = () => {
    if (!wide) { setSheet(true); return; }
    if (!adv) setMode('gelismis');
    else asideRef.current?.querySelector<HTMLElement>('h2')?.focus({ preventScroll: false });
  };

  const quick: ToolbarQuick[] = [
    ...(p.committee && p.committee.options.length > 2 ? [{
      id: 'kurul', label: 'Kurul', value: p.committee.value !== 'all' ? p.committee.label : undefined,
      onClear: () => p.committee!.onPick('all'),
      content: (close: () => void) => <QuickOptions close={close} value={p.committee!.value} onPick={p.committee!.onPick} options={p.committee!.options} />,
    }] : []),
    {
      id: 'yil', label: 'Yıl', value: p.year.value !== 'all' ? p.year.value : undefined,
      onClear: () => p.year.onPick('all'),
      content: (close) => <QuickOptions close={close} value={p.year.value} onPick={p.year.onPick} options={p.year.options} />,
    },
    {
      id: 'ders', label: 'Ders', wide: true, value: p.discipline.value !== 'all' ? p.discipline.label : undefined,
      onClear: () => p.discipline.onPick('all'),
      content: (close) => (
        <QuickOptions close={close} searchable={p.discipline.options.length > 8} placeholder="Ders ara" value={p.discipline.value} onPick={p.discipline.onPick} options={p.discipline.options} />
      ),
    },
    ...(p.topic ? [{
      id: 'konu', label: 'Konu', wide: true, value: p.topic.value !== 'all' ? p.topic.value : undefined,
      onClear: () => p.topic!.onPick('all'),
      content: (close: () => void) => (
        <QuickOptions close={close} searchable={p.topic!.options.length > 8} placeholder="Konu ara" value={p.topic!.value} onPick={p.topic!.onPick} options={p.topic!.options} />
      ),
    }] : []),
  ];

  const discOpts = p.discipline.options;
  const selIdx = discOpts.findIndex((o) => o.id === p.discipline.value);
  const discShown = allDisc || discOpts.length <= DISC_SHOWN + 1 ? discOpts : discOpts.filter((o, i) => i <= DISC_SHOWN || i === selIdx);

  const panel = (inSheet: boolean) => (
    <>
      {!inSheet && (
        <div className="c12-panel-h">
          <h2 className="c12-h2" tabIndex={-1}>Süzgeç</h2>
          <button type="button" className="c12-btn sm ghost" onClick={p.onClearAll} disabled={!p.anyFilter}>Temizle</button>
        </div>
      )}

      <PillGroup f={{ id: 'yil', label: 'Yıl', value: p.year.value, options: p.year.options.map((o) => (o.id === 'all' ? { ...o, label: 'Tümü' } : o)), onPick: p.year.onPick }} />

      {p.committee && p.committee.options.length > 2 && <SelectField id="c12-kurul" label="Kurul" p={p.committee} all="Tüm kurullar" />}

      <fieldset className="c12-fs">
        <legend className="c12-label">Ders</legend>
        <div className="c12-checks" role="radiogroup" aria-label="Ders">
          {discShown.map((o) => (
            <label key={o.id} className={`c12-check ${o.count === 0 && o.id !== p.discipline.value ? 'is-zero' : ''}`}>
              <input type="radio" name={inSheet ? 'c12-ders-s' : 'c12-ders'} checked={o.id === p.discipline.value} onChange={() => p.discipline.onPick(o.id)} />
              <span className="c12-check-t">{o.label}</span>
              {o.count != null && <span className="n">{tr(o.count)}</span>}
            </label>
          ))}
        </div>
        {discOpts.length > DISC_SHOWN + 1 && (
          <button type="button" className="c12-link" aria-expanded={allDisc} onClick={() => setAllDisc((v) => !v)}>
            {allDisc ? 'Daha az göster' : `Tüm dersler (${discOpts.length - 1})`}
          </button>
        )}
      </fieldset>

      {p.topic && <SelectField id={inSheet ? 'c12-konu-s' : 'c12-konu'} label="Konu" p={p.topic} all="Tüm konular" />}

      {p.facets.map((f) => <PillGroup key={f.id} f={f} />)}

      <fieldset className="c12-fs">
        <legend className="c12-label">Kompakt görünüm</legend>
        <label className="c12-check">
          <input type="checkbox" checked={p.quiz.on} onChange={p.quiz.onToggle} />
          <span className="c12-check-t">Kendini sına: cevapları gizle</span>
        </label>
      </fieldset>

      {p.adminFacets && p.adminFacets.length > 0 && (
        <details className="c12-admin">
          <summary className="c12-label">Yönetim</summary>
          <div className="c12-admin-b">{p.adminFacets.map((f) => <PillGroup key={f.id} f={f} />)}</div>
        </details>
      )}

      <SelectField id={inSheet ? 'c12-sort-s' : 'c12-sort-adv'} label="Sıralama" p={p.sort} all="" />

      {naming === null ? (
        <button type="button" className="c12-btn c12-wide" onClick={() => setNaming(p.views.suggestName())} disabled={!canSave} title={canSave ? undefined : 'Önce bir süzgeç seç'}>
          <Bookmark aria-hidden />Görünümü kaydet
        </button>
      ) : (
        <form className="c12-save" onSubmit={(e) => { e.preventDefault(); saveView(); }}>
          <label className="c12-label" htmlFor={inSheet ? 'c12-vn-s' : 'c12-vn'}>Görünüm adı</label>
          <div className="c12-field">
            <input id={inSheet ? 'c12-vn-s' : 'c12-vn'} value={naming} onChange={(e) => setNaming(e.target.value)} maxLength={80} autoFocus />
          </div>
          <div className="c12-save-r">
            <button type="button" className="c12-btn sm ghost" onClick={() => setNaming(null)}>Vazgeç</button>
            <button type="submit" className="c12-btn sm pri">Kaydet</button>
          </div>
        </form>
      )}

      {views.length > 0 && (
        <>
          <hr className="c12-sep" />
          <div className="c12-saved-list">
            <h3 className="c12-label">Kayıtlı görünümler</h3>
            {views.map((v) => {
              const on = sameState(v.state, current);
              return (
                <div key={v.id} className={`c12-saved ${on ? 'is-on' : ''}`}>
                  <button type="button" className="c12-saved-b" aria-pressed={on} onClick={() => { p.views.apply(v.state); if (inSheet) setSheet(false); }}>
                    <span className="c12-clamp1">{v.name}</span>
                  </button>
                  <button type="button" className="c12-saved-x" onClick={() => removeView(v.id)} aria-label={`${v.name} görünümünü sil`} title="Görünümü sil">
                    <X aria-hidden />
                  </button>
                </div>
              );
            })}
          </div>
        </>
      )}

      <hr className="c12-sep" />
      <button type="button" className="c12-btn sm ghost c12-sync" onClick={p.sync.onSync} disabled={p.sync.busy} title={`Cihazda ${tr(p.sync.deviceCount)} soru`}>
        <RefreshCw aria-hidden className={p.sync.busy ? 'c12-spin' : ''} />Güncellemeleri denetle
      </button>
    </>
  );

  const showAside = adv && wide;
  const v13 = !!look.v13;
  const topActions = (
    <>
      {p.adminHref && (
        <a href={p.adminHref} className="c12-btn sm ghost icon" title="Faz 14 düzeltme önerilerini incele" aria-label="Faz 14 incelemesi">
          <Sparkles aria-hidden />
        </a>
      )}
      <CikmisViewSwitch value={p.view.value} onChange={p.view.onChange} />
      <a href={p.practiceHref} className="c12-btn sm">Test oluştur</a>
    </>
  );

  return (
    <div ref={rootRef} className={`c12 ${showAside ? 'is-adv' : ''} ${small ? 'is-sm' : ''}`}>
      {v13 && <h1 className="c12-title">Çıkmış sorular</h1>}
      {!v13 && <header className="c12-top">
        <h1 className="c12-title">Çıkmış sorular</h1>
        <span className="c12-meta" aria-live="polite">
          <span className="c12-num">{tr(p.total)}</span> soru{p.scope ? ` · ${p.scope}` : ''}
        </span>
        <span className="c12-grow" />
        {p.adminHref && (
          <a href={p.adminHref} className="c12-btn sm ghost icon" title="Faz 14 düzeltme önerilerini incele" aria-label="Faz 14 incelemesi">
            <Sparkles aria-hidden />
          </a>
        )}
        <CikmisViewSwitch value={p.view.value} onChange={p.view.onChange} />
        <a href={p.practiceHref} className="c12-btn sm">Test oluştur</a>
      </header>}

      <div className="c12-bar" role="search">
        <div className="c12-searchwrap">
          <label className="c12-field c12-search">
            <Search aria-hidden />
            <input
              type="search"
              data-page-search
              value={q}
              onChange={(e) => typeQ(e.target.value)}
              onFocus={() => { window.clearTimeout(blurT.current); setFocus(true); }}
              onBlur={() => { blurT.current = window.setTimeout(() => setFocus(false), 120); }}
              onKeyDown={(e) => { if (e.key === 'Escape') setFocus(false); }}
              placeholder="Kökte, şıkta ya da konuda ara"
              aria-label="Çıkmış sorularda ara"
              enterKeyHint="search"
            />
            {q ? (
              <button type="button" className="c12-clear" onClick={() => typeQ('')} aria-label="Aramayı temizle"><X aria-hidden /></button>
            ) : (
              <kbd className="c12-kbd" aria-hidden>/</kbd>
            )}
          </label>
          {showSuggest && (
            <div className="c12-suggest">
              <div className="ms-suggest" role="listbox" aria-label="Arama önerileri" onMouseDown={(e) => e.preventDefault()}>
                <button type="button" className="ms-suggest-row is-active" onClick={() => setFocus(false)}>
                  <Search aria-hidden />
                  <span className="min-w-0 truncate">“{q.trim()}” için sonuçlar</span>
                  <span className="n">{tr(p.total)}</span>
                </button>
                {p.suggest.disciplines.length > 0 && <div className="ms-suggest-label">Ders olarak süz</div>}
                {p.suggest.disciplines.map(([d, c]) => (
                  <button key={d} type="button" className="ms-suggest-row" onClick={() => { p.suggest.onDiscipline(d); setFocus(false); }}>
                    <BookOpen aria-hidden /> <span className="min-w-0 truncate">{d}</span> <span className="n">{tr(c)}</span>
                  </button>
                ))}
                {p.suggest.topics.length > 0 && <div className="ms-suggest-label">Konu olarak süz</div>}
                {p.suggest.topics.map(([t, c]) => (
                  <button key={t} type="button" className="ms-suggest-row" onClick={() => { p.suggest.onTopic(t); setFocus(false); }}>
                    <Tag aria-hidden /> <span className="min-w-0 truncate">{t}</span> <span className="n">{tr(c)}</span>
                  </button>
                ))}
                <p className="ms-suggest-tip m-0">
                  <code>"tam ifade"</code> · <code>-hariç</code> · <code>#12</code> soru numarası. Türkçe karakter fark etmez.
                </p>
              </div>
            </div>
          )}
        </div>

        <div className="c13-row">
        <div className="c12-seg" role="tablist" aria-label="Çözüm durumu">
          {STATUS.map(([id, label]) => (
            <button key={id} type="button" role="tab" aria-selected={p.status.value === id} className={p.status.value === id ? 'is-on' : ''}
              onClick={() => p.status.onPick(id)} title={`${label}: ${tr(p.status.counts[id] || 0)} soru`}>
              {label}
            </button>
          ))}
        </div>

        <div className="c12-quick" role="toolbar" aria-label="Hızlı süzgeçler">
          {quick.map((qp) => <QuickPill key={qp.id} q={qp} />)}
          <button type="button" className={`c12-pill c12-fbtn ${showAside || activeCount > 0 ? 'is-on' : ''}`} onClick={openFilters}
            aria-haspopup={wide ? undefined : 'dialog'} aria-label={`Tüm süzgeçler${activeCount ? `, ${activeCount} etkin` : ''}`}>
            <SlidersHorizontal aria-hidden /><span>Süzgeç</span>{activeCount > 0 && <b>{activeCount}</b>}
          </button>
        </div>
        </div>

        {wide && (
          <>
            <span className="c12-grow" />
            <div className="c12-seg" role="group" aria-label="Süzgeç görünümü">
              <button type="button" aria-pressed={!adv} className={!adv ? 'is-on' : ''} onClick={() => setMode('basit')}>Basit</button>
              <button type="button" aria-pressed={adv} className={adv ? 'is-on' : ''} onClick={() => setMode('gelismis')}>Gelişmiş</button>
            </div>
          </>
        )}
      </div>

      {!showAside && p.chips.length > 0 && (
        <div className="c12-chips">
          {p.chips.map((c) => (
            <button key={c.label} type="button" className="c12-chip" onClick={c.onRemove} aria-label={`${c.label} süzgecini kaldır`}>
              <span>{c.label}</span><X aria-hidden />
            </button>
          ))}
          {p.chips.length > 1 && <button type="button" className="c12-link" onClick={p.onClearAll}>Temizle</button>}
        </div>
      )}

      <div className="c12-body">
        {showAside && (
          <aside ref={asideRef} className="c12-filters" aria-label="Gelişmiş süzgeç">
            {panel(false)}
          </aside>
        )}

        <section className="c12-results" aria-label="Sorular">
          <div className="c12-head">
            <span className="c12-meta c12-grow">
              <span className="c12-num c12-ink">{tr(p.total)}</span> soru{p.shown < p.total ? <>, <span className="c12-num">{tr(p.shown)}</span> gösteriliyor</> : ''}
            </span>
            <span className="c12-tagsw">
              <button type="button" role="switch" aria-checked={look.qtags} aria-labelledby="c12-tags-l" className={`c12-switch ${look.qtags ? 'is-on' : ''}`}
                onClick={() => look.set({ qtags: !look.qtags })} />
              <span id="c12-tags-l" className="c12-meta">Etiketler</span>
            </span>
            {!showAside && (
              <label className="c12-field c12-sort">
                <ArrowUpDown aria-hidden />
                <select aria-label="Sıralama" value={p.sort.value} onChange={(e) => p.sort.onPick(e.target.value)}>
                  {p.sort.options.map((o) => <option key={o.id} value={o.id}>{o.label}</option>)}
                </select>
              </label>
            )}
            {v13 && topActions}
          </div>
          {p.children}
        </section>
      </div>

      {!wide && (
        <Sheet open={sheet} onClose={() => setSheet(false)} title="Süzgeç" width={460}
          actions={<button type="button" className="c12-btn sm ghost" onClick={p.onClearAll} disabled={!p.anyFilter}>Temizle</button>}
          footer={<button type="button" className="c12-btn pri c12-wide" onClick={() => setSheet(false)}>{tr(p.total)} soruyu göster</button>}>
          <div className="c12-sheet">{panel(true)}</div>
        </Sheet>
      )}
    </div>
  );
};
