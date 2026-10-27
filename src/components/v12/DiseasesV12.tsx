/**
 * Hastalıklar — v12 "Net" (canvas panosu Glossary.dc.html, alt bölüm). Yalnız data-design='v12' iken DiseasesView'den
 * çizilir; v10/v11 atlası olduğu gibi kalır. Veri, süzme (tür, uzmanlık, kaydedilen, varlık, ders programı), 40'ar
 * kademeli çizim, ekleme/düzenleme formu ve adres çubuğu eşlemesi DiseasesView'dedir; bu bileşen görünümü kurar.
 *
 * Yapı:
 *  - Başlık: "Hastalıklar" · Sözlük | Hastalıklar geçişi · profil sayısı · Profil ekle
 *  - Liste paneli: arama ("/") + Süzgeç (çekmece: tür, uzmanlık, göster) · Kurul/Ders/Konu hızlı hapları ·
 *    A–Z şeridi (aramasız alfabetik sırada) · satırlar (ad + tek satır tanım ya da eşleşme nedeni)
 *  - Ayrıntı: başlık + tür/uzmanlık satırı + ICD/Latince rozetleri + eylemler; bölümler TANIM LİSTESİ (dt/dd) olarak
 *    madde madde (Tanım, Etiyoloji, Klinik, Tanı, Tedavi…); altında aynı panelde düz bölümler: ilişkili tablolar,
 *    ders programında, geçtiği yerler, birlikte geçen kavramlar, sınıflandırma, kaynaklar. Kart içinde kart yok.
 *  - Dar ekranda (<1024 px) ayrıntı tam görünüm (geri düğmesi + tarayıcı geri tuşu, DiseasesView adres eşlemesi).
 * Stil: styles/v12/glossary.css (.g12-*; tanım listesi .g12-dl).
 */
import React, { memo, startTransition, useEffect, useMemo, useRef, useState } from 'react';
import {
  ArrowUpRight, BookOpenText, Bookmark, ChevronLeft, ChevronRight, Copy, Edit2, ExternalLink, Flag, Play, Plus, Search, Share2,
  ShieldCheck, SlidersHorizontal, Tags, Trash2, X,
} from 'lucide-react';
import type { DiseaseFact, DiseaseProfile, DiseaseSectionId } from '../../types/disease';
import { ENTITY_TYPE_LABEL, KIND_LABEL, SECTION_ORDER, plainText, sectionFacts, sectionTitle } from '../../services/diseaseModel';
import { QuickPill, type ToolbarChip, type ToolbarQuick } from '../ui/PageToolbar';
import { Sheet } from '../ui/Sheet';
import { linkedQuestionCount, WHERE_ROWS, type useDiseaseInsights } from '../diseases/DiseaseInsights';
import { lessonFlagText, type LessonSel } from '../diseases/diseaseLessons';
import { linkClick, navigateTo, pathFor } from '../../router';
import { DiseaseAnatomy } from '../diseases/DiseaseAnatomy';
import '../../styles/v12/glossary.css';
import '../../styles/v15/sozluk.css';

type Insights = ReturnType<typeof useDiseaseInsights>['data'];
export interface DiseaseLessonRow { ti: number; n: number; f: number; x: { k: number; d: string; t: string } }
export interface DiseaseEntityGroup { type: string; items: Array<{ key: string; name: string; n: number }> }

export interface DiseasesV12Props {
  dataReady: boolean;
  loadError?: boolean;
  onReload?: () => void;
  total: number;
  filtered: DiseaseProfile[];
  limit: number;
  setLimit: React.Dispatch<React.SetStateAction<number>>;
  setSentinel: (el: HTMLDivElement | null) => void;
  /** Liste alfabetik mi (arama ve ders süzgeci yokken): A–Z şeridi ve harf başlıkları */
  alphabetical: boolean;
  searchQuery: string;
  onSearchQuery: (q: string) => void;
  filters: React.ReactNode;
  filterCount: number;
  chips: ToolbarChip[];
  onClearChips: () => void;
  filtersOn: boolean;
  onClearFilters: () => void;
  quick: ToolbarQuick[];
  /** Ders süzgeci notu ve varlık önerileri */
  notices?: React.ReactNode;
  onAdd: () => void;
  hitLabelOf: (d: DiseaseProfile) => string | undefined;
  sel: DiseaseProfile | null;
  split: boolean;
  favoriteIds: Set<string>;
  onOpen: (d: DiseaseProfile) => void;
  onFav: (id: string) => void;
  onClose: () => void;
  // Ayrıntı
  insights: Insights;
  insightsLoading: boolean;
  entities: DiseaseEntityGroup[];
  canEdit: boolean;
  onShare: (d: DiseaseProfile, sec?: string) => void;
  onCopy: () => void;
  onEdit: () => void;
  onDelete?: () => void;
  onOpenDisease: (id: string) => void;
  canOpen: (id: string) => boolean;
  onEntity: (key: string) => void;
  onSearch: (q: string) => void;
  onReport?: () => void;
  lessons: DiseaseLessonRow[];
  onLesson: (sel: LessonSel) => void;
}

/** Hastalık kaydında kısa bölüm adı; diğer türlerde türün kendi başlığı */
const SHORT: Record<DiseaseSectionId, string> = {
  definition: 'Tanım', etiology: 'Etiyoloji', physiology: 'Patogenez', pathology: 'Morfoloji', symptoms: 'Klinik',
  pathognomonic: 'Ayırıcı tanı', diagnosis: 'Tanı', imaging: 'Görüntüleme', treatment: 'Tedavi', complications: 'Komplikasyon',
  epidemiology: 'Epidemiyoloji', lecture: 'Ders notu',
};
const secLabel = (d: DiseaseProfile, s: DiseaseSectionId) => (d.kind === 'hastalik' ? SHORT[s] : sectionTitle(d.kind, s) || SHORT[s]);

const LETTERS = 'ABCÇDEFGHIİJKLMNOÖPRSŞTUÜVYZ'.split('');
const letterOf = (t: string) => {
  const ch = String(t || '').trim().charAt(0).toLocaleUpperCase('tr-TR');
  return LETTERS.includes(ch) ? ch : '#';
};

/** ==terim== → vurgu, **terim** → kalın */
const FactText: React.FC<{ text: string }> = ({ text }) => {
  const parts = String(text || '').split(/(==[^=\n]+==|\*\*[^*\n]+\*\*)/g);
  return <>{parts.map((x, i) => (
    x.length > 4 && x.startsWith('==') && x.endsWith('==') ? <mark key={i} className="g12-hl">{x.slice(2, -2)}</mark>
      : x.length > 4 && x.startsWith('**') && x.endsWith('**') ? <b key={i}>{x.slice(2, -2)}</b>
        : <React.Fragment key={i}>{x}</React.Fragment>
  ))}</>;
};

/** Ders notu dosya adı → okunur başlık */
const lectureLabel = (src: string) =>
  src.replace(/_/g, ' ').replace(/\.md\b/g, '').replace(/\b\d{6}\b/g, '').replace(/\b[A-Z]\d+\b/g, '').replace(/^\s*\d+\s/, '').replace(/\s{2,}/g, ' ').trim();

const Fact = memo(function Fact({ f, d }: { f: DiseaseFact; d: DiseaseProfile }) {
  return (
    <li>
      {f.label && <b>{f.label}: </b>}
      {f.text && <FactText text={f.text} />}
      {f.key && <span className="g12-badge is-warn" title="Sınavda sorulan kritik bilgi">Sınav</span>}
      {(f.refs || []).map((r) => (
        <a key={r} className="g12-ref" href={`#disease-${d.id}-ref-${r}`} title={d.references?.[r]?.label}
          onClick={(e) => { e.preventDefault(); document.getElementById(`disease-${d.id}-ref-${r}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' }); }}>[{r + 1}]</a>
      ))}
      {f.items && f.items.length > 0 && <ul>{f.items.map((it, k) => <li key={k}><FactText text={it} /></li>)}</ul>}
      {f.source && <small className="g12-m g12-fsrc">Ders notunda da var · {lectureLabel(f.source)}</small>}
    </li>
  );
});

const Row = memo(function Row({ d, on, fav, hint, onOpen, onFav }: {
  d: DiseaseProfile; on: boolean; fav: boolean; hint?: string; onOpen: (d: DiseaseProfile) => void; onFav: (id: string) => void;
}) {
  const def = sectionFacts(d, 'definition')[0] || d.hallmarks[0];
  const [ht, hx] = hint ? hint.split('|') : [];
  return (
    <li id={`hx-item-${d.id}`} className="g12-rowli">
      <button type="button" className={`g12-row ${on ? 'is-on' : ''}`} aria-current={on ? 'true' : undefined} onClick={() => onOpen(d)}>
        <span className="g12-row-t">
          <span className="t">{d.name}</span>
          {d.kind !== 'hastalik' && <span className="g12-badge">{KIND_LABEL[d.kind]}</span>}
        </span>
        {ht ? <span className="d"><b>{ht}</b> {hx}</span> : def ? <span className="d">{plainText(def.text)}</span> : null}
      </button>
      <button type="button" className={`g12-ibtn is-ghost is-sm g12-rowfav ${fav ? 'is-on' : ''}`} aria-pressed={fav} onClick={() => onFav(d.id)}
        aria-label={fav ? `${d.name}: kayıttan çıkar` : `${d.name}: kaydet`} title={fav ? 'Kayıttan çıkar' : 'Kaydet'}>
        <Bookmark fill={fav ? 'currentColor' : 'none'} aria-hidden />
      </button>
    </li>
  );
});

export const DiseasesV12: React.FC<DiseasesV12Props> = (p) => {
  const { sel, split, filtered, limit } = p;

  // Arama: yerel durum + geçiş önceliği
  const [q, setQ] = useState(p.searchQuery);
  const sentRef = useRef(p.searchQuery);
  useEffect(() => {
    if (p.searchQuery !== sentRef.current) { sentRef.current = p.searchQuery; setQ(p.searchQuery); }
  }, [p.searchQuery]);
  const typeQ = (v: string) => { setQ(v); sentRef.current = v; startTransition(() => p.onSearchQuery(v)); };
  const inputRef = useRef<HTMLInputElement>(null);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== '/' || e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target as HTMLElement | null;
      if (t && t.closest('input, textarea, select, [contenteditable="true"]')) return;
      e.preventDefault();
      inputRef.current?.focus();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [mode, setMode] = useState<'liste' | 'anatomi'>('liste');

  /* ---------- A–Z: harf grupları ve harfe gitme ---------- */
  const letterSet = useMemo(() => new Set(p.alphabetical ? filtered.map((d) => letterOf(d.name)) : []), [filtered, p.alphabetical]);
  const visible = useMemo(() => filtered.slice(0, limit), [filtered, limit]);
  const groups = useMemo(() => {
    const out: { key: string; items: DiseaseProfile[] }[] = [];
    for (const d of visible) {
      const k = p.alphabetical ? letterOf(d.name) : '';
      const g = out[out.length - 1];
      if (g && g.key === k) g.items.push(d);
      else out.push({ key: k, items: [d] });
    }
    return out;
  }, [visible, p.alphabetical]);
  const [activeLetter, setActiveLetter] = useState<string | null>(null);
  const [pendingLetter, setPendingLetter] = useState<string | null>(null);
  const { setLimit } = p;
  useEffect(() => {
    if (!pendingLetter) return;
    const idx = filtered.findIndex((d) => letterOf(d.name) === pendingLetter);
    if (idx < 0) { setPendingLetter(null); return; }
    if (idx >= limit) { setLimit(Math.ceil((idx + 1) / 40) * 40 + 40); return; }
    const ch = pendingLetter;
    setPendingLetter(null);
    requestAnimationFrame(() => document.getElementById(`g12-dl-${ch}`)?.scrollIntoView({ block: 'start' }));
  }, [pendingLetter, filtered, limit, setLimit]);
  const curLetter = activeLetter || (sel ? letterOf(sel.name) : null);

  // Geniş ekranda yeni seçimde ayrıntının başı görünür olsun
  const detailRef = useRef<HTMLElement>(null);
  useEffect(() => {
    if (!sel || !split) return;
    const el = detailRef.current;
    if (el && el.getBoundingClientRect().top < 0) el.scrollIntoView({ block: 'start' });
  }, [sel?.id, split]); // eslint-disable-line react-hooks/exhaustive-deps

  const detailOnly = !!sel && !split;
  const count = p.dataReady
    ? (p.filtersOn ? `${filtered.length.toLocaleString('tr-TR')} / ${p.total.toLocaleString('tr-TR')} profil` : `${p.total.toLocaleString('tr-TR')} profil`)
    : 'yükleniyor…';

  const header = (
    <header className="g12-head">
      <h1 className="g12-h1">Hastalıklar</h1>
      <nav className="g12-seg" aria-label="Kaynak">
        <a href={pathFor('glossary')} onClick={linkClick(() => navigateTo(pathFor('glossary')))}>Sözlük</a>
        <a href={pathFor('diseases')} aria-current="page" className="is-on" onClick={linkClick(() => undefined)}>Hastalıklar</a>
      </nav>
      <span className="g12-m g12-num" aria-live="polite">{count}</span>
      <span className="g12-grow" />
      <div className="g12-seg an15-mode" role="group" aria-label="Görünüm">
        <button type="button" className={mode === 'liste' ? 'is-on' : ''} aria-pressed={mode === 'liste'} onClick={() => setMode('liste')}>Liste</button>
        <button type="button" className={mode === 'anatomi' ? 'is-on' : ''} aria-pressed={mode === 'anatomi'} onClick={() => setMode('anatomi')}>Anatomi</button>
      </div>
      <button type="button" className="g12-btn is-sm" onClick={p.onAdd}>
        <Plus aria-hidden /> <span>Profil ekle</span>
      </button>
    </header>
  );

  const list = (
    <section className="g12-panel g12-list" aria-label="Profil listesi">
      <div className="g12-tools">
        <label className="g12-field g12-grow">
          <Search aria-hidden />
          <input ref={inputRef} type="search" data-page-search value={q} onChange={(e) => typeQ(e.target.value)}
            placeholder="Hastalık, belirti, ilaç, gen ara" aria-label="Hastalıklarda ara" enterKeyHint="search" />
          {q ? (
            <button type="button" className="g12-clear" onClick={() => { typeQ(''); inputRef.current?.focus(); }} aria-label="Aramayı temizle"><X aria-hidden /></button>
          ) : <kbd className="g12-kbd" aria-hidden>/</kbd>}
        </label>
        <button type="button" className="g12-ibtn" onClick={() => setFiltersOpen(true)} aria-haspopup="dialog" aria-label={p.filterCount ? `Süzgeç, ${p.filterCount} etkin` : 'Süzgeç'}>
          <SlidersHorizontal aria-hidden />
          {p.filterCount > 0 && <span className="g12-badge-n" aria-hidden>{p.filterCount}</span>}
        </button>
      </div>
      {p.quick.length > 0 && (
        <div className="pt-quick g12-quick" role="toolbar" aria-label="Ders programı süzgeci">
          {p.quick.map((qp) => <QuickPill key={qp.id} q={qp} />)}
        </div>
      )}
      {p.chips.length > 0 && (
        <div className="g12-chips">
          {p.chips.map((c) => (
            <button key={c.id} type="button" className="g12-chip" onClick={c.onRemove} aria-label={`${c.label} süzgecini kaldır`}>
              <span>{c.label}</span><X aria-hidden />
            </button>
          ))}
          {p.chips.length > 1 && <button type="button" className="g12-chip-clear" onClick={p.onClearChips}>Temizle</button>}
        </div>
      )}
      {p.notices}
      {p.alphabetical && p.dataReady && filtered.length > 0 && (
        <nav className="g12-az" aria-label="Harfe atla">
          {LETTERS.map((ch) => (
            <button key={ch} type="button" className={curLetter === ch ? 'is-on' : ''} disabled={!letterSet.has(ch)}
              aria-current={curLetter === ch ? 'true' : undefined} aria-label={`${ch} harfine git`}
              onClick={() => { setActiveLetter(ch); setPendingLetter(ch); }}>
              {ch}
            </button>
          ))}
        </nav>
      )}
      <div className="g12-scroll" aria-busy={!p.dataReady}>
        {p.loadError ? (
          <div className="g12-empty">
            <b>Hastalık profilleri yüklenemedi</b>
            <span>Bağlantını kontrol edip yeniden dene.</span>
            {p.onReload && (
              <button type="button" className="g12-btn is-sm" onClick={p.onReload}>
                Yeniden dene
              </button>
            )}
          </div>
        ) : !p.dataReady ? (
          <ul className="g12-ul-rows" aria-label="Profiller yükleniyor">
            {Array.from({ length: 10 }, (_, i) => (
              <li key={i} className="g12-row is-skel" aria-hidden>
                <span className="ui-skel" style={{ width: `${40 + ((i * 17) % 35)}%`, height: 12 }} />
                <span className="ui-skel" style={{ width: '80%', height: 10 }} />
              </li>
            ))}
          </ul>
        ) : filtered.length === 0 ? (
          <div className="g12-empty">
            <b>Eşleşen kayıt yok</b>
            <span>Aramayı kısalt ya da süzgeçleri kaldır.</span>
            {p.filtersOn && <button type="button" className="g12-btn is-sm" onClick={p.onClearFilters}>Süzgeçleri temizle</button>}
          </div>
        ) : (
          <>
            {groups.map((g, gi) => (
              <section key={`${g.key}-${gi}`} aria-label={g.key || undefined}>
                {g.key && <h2 className="g12-letter" id={`g12-dl-${g.key}`}>{g.key}</h2>}
                <ul className="g12-ul-rows">
                  {g.items.map((d) => (
                    <Row key={d.id} d={d} on={sel?.id === d.id} fav={p.favoriteIds.has(d.id)} hint={p.hitLabelOf(d)} onOpen={p.onOpen} onFav={p.onFav} />
                  ))}
                </ul>
              </section>
            ))}
            {filtered.length > limit && (
              <div ref={p.setSentinel} className="g12-row is-skel" aria-hidden>
                <span className="ui-skel" style={{ width: '50%', height: 12 }} />
                <span className="ui-skel" style={{ width: '80%', height: 10 }} />
              </div>
            )}
            <p className="g12-listfoot g12-m" aria-live="polite">
              {filtered.length > limit
                ? `${Math.min(limit, filtered.length).toLocaleString('tr-TR')} / ${filtered.length.toLocaleString('tr-TR')} · kaydırdıkça 40’ar yüklenir`
                : `${filtered.length.toLocaleString('tr-TR')} profilin tümü gösteriliyor`}
            </p>
          </>
        )}
      </div>
    </section>
  );

  return (
    <div className={`g12 ${split ? 'is-wide' : ''}`}>
      {!detailOnly && header}
      {mode === 'anatomi' && !detailOnly && p.dataReady ? (
        <>
          <p className="g12-m an15-sub">Anatomiden gez · {filtered.length.toLocaleString('tr-TR')} profil</p>
          <DiseaseAnatomy diseases={filtered} onOpen={(d) => { setMode('liste'); p.onOpen(d); }} />
        </>
      ) : (
      <div className="g12-split">
        {!detailOnly && list}
        {(split || sel) && (sel ? (
          <DiseaseDetailV12 key={sel.id} {...p} d={sel} detailRef={detailRef} />
        ) : (
          <section className="g12-panel g12-detail g12-placeholder" aria-label="Profil ayrıntısı">
            <BookOpenText aria-hidden />
            <b>Bir profil seç</b>
            <span>Soldaki listeden bir hastalığa dokun; tanımdan tedaviye bölümler burada açılır.</span>
          </section>
        ))}
      </div>
      )}
      <Sheet open={filtersOpen} onClose={() => setFiltersOpen(false)} title="Hastalık süzgeci" width={460}
        footer={<button type="button" className="ui-btn is-primary" style={{ width: '100%' }} onClick={() => setFiltersOpen(false)}>Uygula</button>}>
        <div className="pt-sheet">{p.filters}</div>
      </Sheet>
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* Ayrıntı                                                              */
/* ------------------------------------------------------------------ */

const DiseaseDetailV12: React.FC<DiseasesV12Props & { d: DiseaseProfile; detailRef: React.RefObject<HTMLElement | null> }> = ({
  d, detailRef, split, favoriteIds, onFav, onClose, insights, insightsLoading, entities, canEdit, onShare, onCopy, onEdit, onDelete,
  onOpenDisease, canOpen, onEntity, onSearch, onReport, lessons, onLesson,
}) => {
  const [allLessons, setAllLessons] = useState(false);
  const isFav = favoriteIds.has(d.id);
  const secs = SECTION_ORDER.filter((s) => sectionTitle(d.kind, s) && sectionFacts(d, s).length > 0);
  const qCount = linkedQuestionCount(insights);
  const plainName = d.name.replace(/\s*\([^)]*\)/g, '').trim();
  const H = split ? 'h2' : 'h1';
  const relDis = (insights?.relatedDiseases || []).filter((r) => canOpen(r.id)).slice(0, 6);
  const where = WHERE_ROWS.map((r) => ({ ...r, n: r.keys.reduce((a, k) => a + (insights?.byType[k] || 0), 0) })).filter((r) => r.n > 0);
  const topDeck = insights?.sources.find((s) => s.type === 'deck_slide')?.title.split(' — ')[0];
  const topPast = insights?.sources.find((s) => s.type === 'past_question')?.title;
  const lec = (d.relatedLectures || []).slice(0, 3);
  const concepts = (insights?.related || []).filter((r) => r.type !== 'topic').slice(0, 8);
  const loadingLinks = insightsLoading && !insights;
  const searchHref = pathFor('search', plainName);

  return (
    <article ref={detailRef as React.RefObject<HTMLElement>} className="g12-panel g12-detail" id={`disease-${d.id}`} aria-labelledby={`g12-ds-${d.id}`}>
      {!split && (
        <div className="g12-backbar">
          <button type="button" className="g12-back" onClick={onClose}><ChevronLeft aria-hidden /> Hastalıklar</button>
        </div>
      )}
      <header className="g12-dsh">
        <div className="g12-dsh-row">
          <div className="g12-grow g12-dsh-main">
            <H id={`g12-ds-${d.id}`} className="g12-h2">{d.name}</H>
            <span className="g12-m">{['Hastalıklar', d.category, KIND_LABEL[d.kind]].filter(Boolean).join(' · ')}</span>
          </div>
          {d.icd_code && <span className="g12-badge">ICD-10 {d.icd_code}</span>}
        </div>
        {d.latinName && d.latinName !== d.name && <p className="g12-m">İng./Lat. <i>{d.latinName}</i></p>}
        <div className="g12-acts">
          <button type="button" className={`g12-btn is-sm ${isFav ? 'is-tonal' : ''}`} aria-pressed={isFav} onClick={() => onFav(d.id)}>
            <Bookmark fill={isFav ? 'currentColor' : 'none'} aria-hidden /> {isFav ? 'Kaydedildi' : 'Kaydet'}
          </button>
          {qCount > 0 && (
            <button type="button" className="g12-btn is-sm is-pri" onClick={() => onSearch(plainName)}>
              <Play aria-hidden /> Soruları çöz · <span className="g12-num">{qCount.toLocaleString('tr-TR')}</span>
            </button>
          )}
          <span className="g12-grow" />
          <button type="button" className="g12-ibtn is-ghost is-sm" onClick={() => onShare(d)} aria-label="Paylaş" title="Paylaş"><Share2 aria-hidden /></button>
          <button type="button" className="g12-ibtn is-ghost is-sm" onClick={onCopy} aria-label="Özeti kopyala" title="Özeti kopyala"><Copy aria-hidden /></button>
          {canEdit && <button type="button" className="g12-ibtn is-ghost is-sm" onClick={onEdit} aria-label="Düzenle" title="Düzenle"><Edit2 aria-hidden /></button>}
          {canEdit && onDelete && <button type="button" className="g12-ibtn is-ghost is-sm is-bad" onClick={onDelete} aria-label="Sil" title="Sil"><Trash2 aria-hidden /></button>}
        </div>
      </header>

      <dl className="g12-dl">
        {d.hallmarks.length > 0 && (
          <>
            <dt id={`disease-${d.id}-hallmarks`} data-sec="hallmarks">Karakteristik</dt>
            <dd data-sec="hallmarks"><ul>{d.hallmarks.map((h, k) => <Fact key={k} f={h} d={d} />)}</ul></dd>
          </>
        )}
        {secs.map((s) => {
          const label = secLabel(d, s);
          return (
            <React.Fragment key={s}>
              <dt id={`disease-${d.id}-${s}`} data-sec={s}>
                <span>{label}</span>
                <button type="button" className="g12-dt-share" onClick={() => onShare(d, s)} aria-label={`${label} bölümünün bağlantısını paylaş`} title="Bu bölümün bağlantısını paylaş">
                  <Share2 aria-hidden />
                </button>
              </dt>
              <dd data-sec={s}><ul>{sectionFacts(d, s).map((f, k) => <Fact key={k} f={f} d={d} />)}</ul></dd>
            </React.Fragment>
          );
        })}
      </dl>
      {!secs.length && !d.hallmarks.length && <p className="g12-sec g12-m">Bu profilde henüz bölüm yok.</p>}

      {d.verification && (
        <p className="g12-sec g12-verif">
          <ShieldCheck aria-hidden />
          <span><b>Web kaynaklarıyla madde madde doğrulandı</b> · {d.verification.checked} madde denetlendi
            {d.verification.fixed + d.verification.conflict > 0 ? `, ${d.verification.fixed + d.verification.conflict} düzeltildi` : ''}
            {` · ${new Date(d.verification.at).toLocaleDateString('tr-TR')}`}</span>
        </p>
      )}

      {loadingLinks && (
        <div className="g12-sec" aria-hidden>
          <span className="ui-skel" style={{ width: '30%', height: 11 }} />
          <span className="ui-skel" style={{ height: 28 }} />
          <span className="ui-skel" style={{ height: 28 }} />
        </div>
      )}

      {relDis.length > 0 && (
        <section className="g12-sec" aria-labelledby={`g12-rel-${d.id}`}>
          <h3 id={`g12-rel-${d.id}`} className="g12-sub">İlişkili tablolar</h3>
          <ul className="g12-lessons">
            {relDis.map((r) => (
              <li key={r.id}>
                <button type="button" className="g12-lesson is-btn" onClick={() => onOpenDisease(r.id)}>
                  <span className="g12-grow"><span className="t">{r.name}</span></span>
                  {r.ddx && <span className="g12-badge">ayırıcı tanı</span>}
                  <ChevronRight className="g12-chev" aria-hidden />
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      {lessons.length > 0 && (
        <section className="g12-sec" aria-labelledby={`g12-prog-${d.id}`}>
          <h3 id={`g12-prog-${d.id}`} className="g12-sub">Ders programında</h3>
          <ul className="g12-lessons">
            {(allLessons ? lessons : lessons.slice(0, 5)).map((l) => (
              <li key={l.ti}>
                <button type="button" className="g12-lesson is-btn" onClick={() => onLesson({ k: l.x.k, d: l.x.d, t: l.ti })} title="Bu konuda geçen tüm profilleri listele">
                  <span className="g12-grow">
                    <span className="t">{l.x.t}</span>
                    <span className="g12-m">Kurul {l.x.k} · {l.x.d} · {l.n} kez · {lessonFlagText(l.f)}</span>
                  </span>
                  <ChevronRight className="g12-chev" aria-hidden />
                </button>
              </li>
            ))}
          </ul>
          {lessons.length > 5 && (
            <button type="button" className="g12-linkbtn" onClick={() => setAllLessons((v) => !v)}>
              {allLessons ? 'Daha az göster' : `${lessons.length - 5} konu daha`}
            </button>
          )}
        </section>
      )}

      {(where.length > 0 || lec.length > 0) && (
        <section className="g12-sec" aria-labelledby={`g12-where-${d.id}`}>
          <h3 id={`g12-where-${d.id}`} className="g12-sub">Geçtiği yerler</h3>
          <ul className="g12-lessons">
            {where.map((r) => (
              <li key={r.label} className="g12-lesson">
                <span className="g12-grow">
                  <span className="t">{r.label} · <span className="g12-num">{r.n.toLocaleString('tr-TR')}</span> {r.unit}</span>
                  {r.keys[0] === 'deck_slide' && topDeck && <span className="g12-m">{topDeck}</span>}
                  {r.keys[0] === 'past_question' && topPast && <span className="g12-m">{topPast}</span>}
                </span>
              </li>
            ))}
            {lec.map((l) => (
              <li key={l} className="g12-lesson" style={{ cursor: 'pointer' }} onClick={() => onSearch(l)} title={`${l} konusunu tüm kaynaklarda ara`}>
                <span className="g12-grow"><span className="t">{l}</span><span className="g12-m">Ders · Ara</span></span>
              </li>
            ))}
          </ul>
          {where.length > 0 && (
            <a className="g12-link" href={searchHref} onClick={linkClick(() => navigateTo(searchHref))}>
              Tüm kaynaklarda ara <ArrowUpRight aria-hidden />
            </a>
          )}
        </section>
      )}

      {concepts.length > 0 && insights && (
        <section className="g12-sec" aria-labelledby={`g12-con-${d.id}`}>
          <h3 id={`g12-con-${d.id}`} className="g12-sub">Sık birlikte geçen kavramlar</h3>
          <div className="g12-pills">
            {concepts.map((r) => (
              <button key={r.ref} type="button" className="g12-pill" onClick={() => onSearch(`${plainName} ${r.label}`)} title={`${r.label} — ikisini birlikte ara`}>
                <span>{r.label}</span>
              </button>
            ))}
          </div>
        </section>
      )}

      {entities.length > 0 && (
        <section className="g12-sec" aria-labelledby={`g12-ent-${d.id}`}>
          <h3 id={`g12-ent-${d.id}`} className="g12-sub"><Tags aria-hidden />Sınıflandırma</h3>
          <p className="g12-m">Bir öğeye dokun: aynı belirti, ilaç, gen ya da bulguyu içeren tüm profiller listelenir.</p>
          <dl className="g12-dl is-compact">
            {entities.map((g) => (
              <React.Fragment key={g.type}>
                <dt>{ENTITY_TYPE_LABEL[g.type as keyof typeof ENTITY_TYPE_LABEL] || g.type}</dt>
                <dd>
                  <div className="g12-pills">
                    {g.items.map((it) => (
                      <button key={it.key} type="button" className="g12-pill" disabled={it.n < 2} onClick={() => onEntity(it.key)}
                        title={it.n >= 2 ? `${it.name} geçen ${it.n} profili listele` : 'Yalnız bu profilde geçiyor'}>
                        <span>{it.name}</span>{it.n >= 2 && <b className="g12-num">{it.n}</b>}
                      </button>
                    ))}
                  </div>
                </dd>
              </React.Fragment>
            ))}
          </dl>
        </section>
      )}

      {(d.references || []).length > 0 && (
        <section className="g12-sec" aria-labelledby={`g12-refs-${d.id}`} id={`disease-${d.id}-references`}>
          <h3 id={`g12-refs-${d.id}`} className="g12-sub">Kaynaklar</h3>
          <ol className="g12-refs">
            {(d.references || []).map((r, k) => (
              <li key={k} id={`disease-${d.id}-ref-${k}`}>
                {r.url ? <a href={r.url} target="_blank" rel="noreferrer">{r.label} <ExternalLink aria-hidden /></a> : r.label}
              </li>
            ))}
          </ol>
        </section>
      )}

      {onReport && (
        <div className="g12-dacts">
          <button type="button" className="g12-btn is-sm is-ghost" onClick={onReport}><Flag aria-hidden /> Bu profilde hata bildir</button>
        </div>
      )}
    </article>
  );
};
