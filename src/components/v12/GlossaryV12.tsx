/**
 * Sözlük — v12 "Net" (canvas panosu Glossary.dc.html). Yalnız data-design='v12' iken MedicalEncyclopediaView'den çizilir;
 * v10/v11 sözlüğü olduğu gibi kalır. Veri, süzme, 40'ar kademeli çizim, harfe/maddeye gitme ve derin bağlantı
 * MedicalEncyclopediaView'dedir; bu bileşen yalnız görünümü kurar.
 *
 * Yapı:
 *  - Başlık: "Sözlük" · madde sayısı · "Hastalıklar’a git" bağlantısı (H404)
 *  - Liste paneli: arama ("/" kısayolu) + Süzgeç (çekmece) · A–Z şeridi (Türkçe harfler; boş harf soluk) ·
 *    harf başlıklı satırlar (terim + tek satır tanım)
 *  - Ayrıntı paneli: terim başlığı · Kaydet/Paylaş · İng./Lat. ad, kısaltma, kurul/branş satırı · okuma yazısıyla tanım ·
 *    bilgi kartı maddeleri · ders notu / mekanizma / ayırıcı tanı / tuzak / spot bölümleri · İlgili hapları ·
 *    Geçtiği dersler satırları · "Çıkmış sorularda · n" bağlantısı (arama sayfasına) · hata bildir / denetle
 *  - Dar ekranda (<1024 px) ayrıntı tam görünüm olarak açılır; geri düğmesi ve tarayıcı geri tuşu listeye döner.
 * Stil: styles/v12/glossary.css (.g12-*).
 */
import React, { startTransition, useEffect, useMemo, useRef, useState } from 'react';
import {
  AlertCircle, AlertTriangle, BookOpenText, Bookmark, Check, ChevronLeft, ChevronRight, FileText, Filter, GraduationCap, Lightbulb,
  RefreshCw, Search, Headphones, CircleHelp, Share2, SlidersHorizontal, Stethoscope, X,
} from 'lucide-react';
import type { EncyclopediaEntry, IndexedEncyclopediaEntry, InfoCardItem } from '../encyclopedia/MedicalEncyclopediaView';
import type { ToolbarChip } from '../ui/PageToolbar';
import { Sheet } from '../ui/Sheet';
import { fetchSearch } from '../search/searchShared';
import { deepLinkIdFor, linkClick, navigateTo, parseLocation, pathFor } from '../../router';
import '../../styles/v12/glossary.css';
import { cdListeGetir, type CdListeDers } from '../canliDers/canliDersStore';
import { useAppearance } from '../../utils/appearance';

export interface GlossaryV12Props {
  entries: IndexedEncyclopediaEntry[] | null;
  loadError: boolean;
  onReload: () => void;
  total: number;
  filteredCount: number;
  visibleCount: number;
  groups: { key: string; items: IndexedEncyclopediaEntry[] }[];
  hasMore: boolean;
  setSentinel: (el: HTMLLIElement | null) => void;
  /** Harf başlıkları ve A–Z şeridi (aramasız alfabetik sırada) */
  grouped: boolean;
  /** Grup başlığının DOM kimliği (harfe gitme bu kimliğe kaydırır) */
  groupDomId: (key: string) => string;
  alphabet: string[];
  letterSet: Set<string>;
  onJumpLetter: (ch: string) => void;
  searchQuery: string;
  onSearch: (q: string) => void;
  filters: React.ReactNode;
  chips: ToolbarChip[];
  onClearChips: () => void;
  onResetFilters: () => void;
  openEntry: EncyclopediaEntry | null;
  /** Liste + ayrıntı yan yana mı */
  wide: boolean;
  onSelect: (id: string) => void;
  onClose: () => void;
  saved: Set<string>;
  onBookmark: (id: string) => void;
  onShare: (e: EncyclopediaEntry) => void;
  copied: boolean;
  onReport: (e: EncyclopediaEntry) => void;
  onAudit: (e: EncyclopediaEntry) => void;
  auditing: boolean;
  auditMessage: string | null;
  related: (id: string) => EncyclopediaEntry | undefined;
  onOpenRelated: (id: string) => void;
  catLabel: (c?: string) => string;
}

/* ------------------------------------------------------------------ */
/* Metin yardımcıları                                                   */
/* ------------------------------------------------------------------ */

/** Alan metin, metin listesi ya da nesne olabilir: tek satır düz metin */
const line = (v: unknown): string =>
  v == null ? '' : typeof v === 'string' || typeof v === 'number' ? String(v)
    : Array.isArray(v) ? v.map(line).filter(Boolean).join(' · ')
    : Object.values(v as Record<string, unknown>).map(line).filter(Boolean).join(' — ');

const plain = (v: unknown) => line(v).replace(/\*\*/g, '').replace(/\s+/g, ' ').trim();

/** "**kalın**" → <b> */
/** "**kalın**" → <b>, "==vurgu==" → <mark> (v10/v11 okuyucularıyla aynı işaretler) */
const Inline: React.FC<{ text: string }> = ({ text }) => (
  <>
    {String(text).split(/(\*\*[^*]+\*\*|==[^=\n]+==)/g).map((part, i) =>
      part.startsWith('**') && part.endsWith('**') && part.length > 4
        ? <b key={i}>{part.slice(2, -2)}</b>
        : part.startsWith('==') && part.endsWith('==') && part.length > 4
          ? <mark key={i} className="g12-hl">{part.slice(2, -2)}</mark>
          : <React.Fragment key={i}>{part}</React.Fragment>,
    )}
  </>
);

/** Satır başı "- " / "• " / "1)" maddeleri listeye, boş satırla ayrılanlar ayrı paragrafa */
const BULLET = /^\s*(?:[-•*▪◦]|\d{1,2}[.)])\s+/;
const Blocks: React.FC<{ text: string; read?: boolean }> = ({ text, read }) => {
  const lines = text.split(/\n/).map((l) => l.trimEnd());
  const out: React.ReactNode[] = [];
  let para: string[] = [];
  let list: string[] = [];
  const flushPara = () => { if (para.length) out.push(<p key={out.length} className={read ? 'g12-read' : 'g12-text'}><Inline text={para.join(' ')} /></p>); para = []; };
  const flushList = () => { if (list.length) out.push(<ul key={out.length} className={`g12-ul ${read ? 'is-read' : ''}`}>{list.map((t, i) => <li key={i}><Inline text={t} /></li>)}</ul>); list = []; };
  for (const l of lines) {
    if (!l.trim()) { flushPara(); flushList(); continue; }
    if (BULLET.test(l)) { flushPara(); list.push(l.replace(BULLET, '')); } else { flushList(); para.push(l.trim()); }
  }
  flushPara(); flushList();
  return out.length === 1 ? <>{out[0]}</> : <div className="g12-blocks">{out}</div>;
};

/** Metin → paragraf/madde; liste → madde listesi */
const Rich: React.FC<{ value: unknown; read?: boolean }> = ({ value, read }) => {
  if (Array.isArray(value)) {
    const items = value.map(line).filter(Boolean);
    if (!items.length) return null;
    return <ul className={`g12-ul ${read ? 'is-read' : ''}`}>{items.map((t, i) => <li key={i}><Inline text={t} /></li>)}</ul>;
  }
  const t = line(value).trim();
  if (!t) return null;
  if (t.includes('\n')) return <Blocks text={t} read={read} />;
  return <p className={read ? 'g12-read' : 'g12-text'}><Inline text={t} /></p>;
};

const InfoItems: React.FC<{ items?: InfoCardItem[]; depth?: number }> = ({ items, depth = 1 }) => {
  if (!items?.length) return null;
  return (
    <ul className={`g12-ul is-read ${depth > 1 ? 'is-sub' : ''}`}>
      {items.map((it, i) => {
        const text = typeof it === 'string' ? it : it?.text;
        const sub = typeof it === 'string' ? undefined : it?.sub;
        if (!text) return null;
        return (
          <li key={i}>
            <Inline text={text} />
            {depth < 3 && <InfoItems items={sub} depth={depth + 1} />}
          </li>
        );
      })}
    </ul>
  );
};

/** Kısaltma gibi duran eş adlar ("ccRCC", "FSGS", "JGA"): en az iki büyük harf, boşluksuz, kısa */
const isAbbr = (s: string) => /^[A-Za-zÇĞİÖŞÜçğıöşü0-9/-]{2,9}$/.test(s) && (s.match(/[A-ZÇĞİÖŞÜ]/g) || []).length >= 2;

/** "Ders notu: 5)Üriner Sistem Enfeksiyonlari s.29; …" → ders adı + sayfa/satır */
function lessonRows(src?: string): Array<{ title: string; at: string[] }> {
  const raw = String(src || '').trim();
  if (!raw) return [];
  const isNote = /^ders notu\s*:/i.test(raw);
  const parts = (isNote ? raw.replace(/^ders notu\s*:\s*/i, '') : raw).split(';');
  const out = new Map<string, { title: string; at: string[] }>();
  for (const p of parts) {
    const page = p.match(/\bs\.\s*(\d+)\s*$/)?.[1];
    const row = p.match(/\(satır\s*(\d+)\)/i)?.[1];
    const title = p
      .replace(/\(satır[^)]*\)/gi, '')
      .replace(/\bs\.\s*\d+\s*$/, '')
      .replace(/\.(txt|md|pdf)\b/gi, '')
      .replace(/^\s*\d+\)\s*/, '')
      .replace(/^\s*D\d+\s+/, '')
      .replace(/_/g, ' ')
      .replace(/\s{2,}/g, ' ')
      .trim();
    if (!title) continue;
    const k = title.toLocaleLowerCase('tr-TR');
    const cur = out.get(k) || { title, at: [] };
    if (page && !cur.at.includes(`s. ${page}`)) cur.at.push(`s. ${page}`);
    if (row && !cur.at.includes(`satır ${row}`)) cur.at.push(`satır ${row}`);
    out.set(k, cur);
  }
  return [...out.values()].slice(0, 6);
}

/** "Derste dinle" (tasarım B10): terimin geçtiği ders notunun adını sesli ders listesindeki başlıkla eşleştirir;
 *  bulunursa ders, terimin geçtiği paragrafa (?ara=) açılır. Eşleşme yoksa çip çıkmaz. */
const katlaG = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i').replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();
let cdListe: CdListeDers[] | null = null;
function useDersteDinle(basliklar: string[], terim: string) {
  const [liste, setListe] = useState<CdListeDers[] | null>(cdListe);
  useEffect(() => { if (!cdListe) cdListeGetir(false).then((l) => { cdListe = l; setListe(l); }, () => {}); }, []);
  return useMemo(() => {
    if (!liste || !basliklar.length) return null;
    for (const b of basliklar) {
      const k = katlaG(b);
      if (k.length < 6) continue;
      const d = liste.find((x) => !x.sinama && (katlaG(x.baslik).includes(k) || k.includes(katlaG(x.baslik))));
      if (d) return { ad: d.baslik, yol: `${pathFor('canli_ders', d.key)}?ara=${encodeURIComponent(terim)}` };
    }
    return null;
  }, [liste, basliklar.join('|'), terim]);
}

/** Çıkmış soru sayısı: arama sayfasının çıkmış soru sonucu (aynı sorgu, aynı sayı); seçim durulunca bir kez sorulur */
function usePastCount(query: string | null) {
  const [res, setRes] = useState<{ q: string; n: number; capped: boolean } | null>(null);
  useEffect(() => {
    if (!query) return;
    const ctrl = new AbortController();
    const t = window.setTimeout(async () => {
      const r = await fetchSearch(query, { types: ['past_question'], limit: 1, fast: true }, ctrl.signal).catch(() => null);
      if (!ctrl.signal.aborted && r) setRes({ q: query, n: r.total, capped: r.capped });
    }, 450);
    return () => { ctrl.abort(); window.clearTimeout(t); };
  }, [query]);
  return res && res.q === query ? res : null;
}

const SKEL: [string, string][] = [['46%', '78%'], ['58%', '64%'], ['40%', '82%'], ['52%', '70%'], ['36%', '76%']];
const SkelRow = React.forwardRef<HTMLLIElement, { i: number }>(({ i }, ref) => (
  <li ref={ref} className="g12-row is-skel" aria-hidden>
    <span className="ui-skel" style={{ width: SKEL[i % SKEL.length][0], height: 12 }} />
    <span className="ui-skel" style={{ width: SKEL[i % SKEL.length][1], height: 10 }} />
  </li>
));
SkelRow.displayName = 'SkelRow';

/* ------------------------------------------------------------------ */
/* Satır                                                                */
/* ------------------------------------------------------------------ */

const Row = React.memo<{ e: IndexedEncyclopediaEntry; on: boolean; saved: boolean; onPick: (id: string) => void }>(({ e, on, saved, onPick }) => {
  const def = plain(e.definition) || plain(e.latinName) || '';
  return (
    <li id={`term-${e.id}`}>
      <button type="button" className={`g12-row ${on ? 'is-on' : ''}`} aria-current={on ? 'true' : undefined} onClick={() => onPick(e.id)}>
        <span className="g12-row-t">
          <span className="t">{e.term}</span>
          {saved && <Bookmark className="g12-row-saved" fill="currentColor" aria-label="Kaydedildi" />}
        </span>
        {def && <span className="d">{def}</span>}
      </button>
    </li>
  );
});
Row.displayName = 'GlossaryV12Row';

/* ------------------------------------------------------------------ */
/* Ekran                                                                */
/* ------------------------------------------------------------------ */

export const GlossaryV12: React.FC<GlossaryV12Props> = (p) => {
  const { entries, openEntry, wide } = p;

  // Arama: kutu yerel durumla anında güncellenir, süzme geçiş önceliğinde koşar
  const [q, setQ] = useState(p.searchQuery);
  const sentRef = useRef(p.searchQuery);
  useEffect(() => {
    if (p.searchQuery !== sentRef.current) { sentRef.current = p.searchQuery; setQ(p.searchQuery); }
  }, [p.searchQuery]);
  const typeQ = (v: string) => {
    setQ(v);
    sentRef.current = v;
    startTransition(() => p.onSearch(v));
  };
  const inputRef = useRef<HTMLInputElement>(null);
  // "/" kısayolu: başka bir alana yazılmıyorsa aramaya odaklanır
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== '/' || e.metaKey || e.ctrlKey || e.altKey) return;
      const t = e.target as HTMLElement | null;
      if (t && (t.closest('input, textarea, select, [contenteditable="true"]'))) return;
      e.preventDefault();
      inputRef.current?.focus();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const [filtersOpen, setFiltersOpen] = useState(false);
  const [activeLetter, setActiveLetter] = useState<string | null>(null);
  const jump = (ch: string) => { setActiveLetter(ch); p.onJumpLetter(ch); };
  const curLetter = activeLetter || (openEntry ? (openEntry as IndexedEncyclopediaEntry)._firstLetter : null);

  /* ---------- Dar ekran: ayrıntı tam görünüm, geçmişle eş ---------- */
  const pushedRef = useRef(false);
  const lastOpenRef = useRef<string | null>(null);
  const pick = (id: string) => {
    p.onSelect(id);
    try {
      if (new URLSearchParams(window.location.search).get('id') !== id) {
        const next = `${pathFor('glossary')}?id=${encodeURIComponent(id)}`;
        if (wide) {
          window.history.replaceState(window.history.state, '', next);
        } else {
          window.history.pushState({ route: 'glossary' }, '', next);
          pushedRef.current = true;
        }
      }
    } catch { /* adres yazılamadıysa yalnız durum */ }
    if (!wide) requestAnimationFrame(() => window.scrollTo({ top: 0 }));
  };
  const back = () => {
    if (pushedRef.current) { pushedRef.current = false; window.history.back(); return; }
    try { window.history.replaceState(window.history.state, '', pathFor('glossary')); } catch { /* yoksay */ }
    p.onClose();
  };
  // Tarayıcı geri tuşu: adreste madde kalmadıysa listeye dön
  const onCloseRef = useRef(p.onClose);
  onCloseRef.current = p.onClose;
  const wideRef = useRef(wide);
  wideRef.current = wide;
  useEffect(() => {
    const onPop = () => {
      const { route, param } = parseLocation();
      if (route !== 'glossary' || wideRef.current) return;
      if (!deepLinkIdFor('glossary', param)) { pushedRef.current = false; onCloseRef.current(); }
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);
  // Listeye dönünce açılan satır görünür olsun; geniş ekranda yeni seçimde ayrıntının başı görünür olsun
  const detailRef = useRef<HTMLElement>(null);
  useEffect(() => {
    if (openEntry) {
      lastOpenRef.current = openEntry.id;
      if (wide) {
        const el = detailRef.current;
        if (el && el.getBoundingClientRect().top < 0) el.scrollIntoView({ block: 'start' });
      }
      return;
    }
    const id = lastOpenRef.current;
    if (!wide && id) requestAnimationFrame(() => document.getElementById(`term-${id}`)?.scrollIntoView({ block: 'center' }));
  }, [openEntry?.id, wide]); // eslint-disable-line react-hooks/exhaustive-deps

  const showDetailOnly = !wide && !!openEntry;
  const count = !entries
    ? (p.loadError ? '' : 'yükleniyor…')
    : p.filteredCount !== p.total
      ? `${p.filteredCount.toLocaleString('tr-TR')} / ${p.total.toLocaleString('tr-TR')} terim`
      : `${p.total.toLocaleString('tr-TR')} terim`;

  const header = (
    <header className="g12-head">
      <h1 className="g12-h1">Sözlük</h1>
      {/* H404: Sözlük | Hastalıklar sekme tekrarı kalktı (menüde ikisi ayrı); yerine tek küçük çapraz bağlantı */}
      <span className="g12-m g12-num" aria-live="polite">{count}</span>
      <a className="g12-capraz" href={pathFor('diseases')} onClick={linkClick(() => navigateTo(pathFor('diseases')))}>Hastalıklar’a git →</a>
    </header>
  );

  const list = (
    <section className="g12-panel g12-list" aria-label="Terim listesi">
      <div className="g12-tools">
        <label className="g12-field g12-grow">
          <Search aria-hidden />
          <input
            ref={inputRef}
            type="search"
            data-page-search
            value={q}
            onChange={(e) => typeQ(e.target.value)}
            placeholder="Terim ya da İngilizce karşılık"
            aria-label="Sözlükte ara"
            enterKeyHint="search"
          />
          {q ? (
            <button type="button" className="g12-clear" onClick={() => { typeQ(''); inputRef.current?.focus(); }} aria-label="Aramayı temizle">
              <X aria-hidden />
            </button>
          ) : <kbd className="g12-kbd" aria-hidden>/</kbd>}
        </label>
        <button type="button" className="g12-ibtn" onClick={() => setFiltersOpen(true)} aria-haspopup="dialog" aria-label={p.chips.length ? `Süzgeç, ${p.chips.length} etkin` : 'Süzgeç'}>
          <SlidersHorizontal aria-hidden />
          {p.chips.length > 0 && <span className="g12-badge-n" aria-hidden>{p.chips.length}</span>}
        </button>
      </div>
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
      {p.grouped && !!entries && p.filteredCount > 0 && (
        <nav className="g12-az" aria-label="Harfe atla">
          {p.alphabet.map((ch) => {
            const has = p.letterSet.has(ch);
            return (
              <button
                key={ch}
                type="button"
                className={`${curLetter === ch ? 'is-on' : ''}`}
                disabled={!has}
                aria-current={curLetter === ch ? 'true' : undefined}
                aria-label={`${ch} harfine git`}
                onClick={() => jump(ch)}
              >
                {ch}
              </button>
            );
          })}
        </nav>
      )}
      <div className="g12-scroll" aria-busy={!entries}>
        {p.loadError ? (
          <div className="g12-empty">
            <b>Sözlük yüklenemedi</b>
            <span>Bağlantını kontrol edip yeniden dene.</span>
            <button type="button" className="g12-btn is-sm" onClick={p.onReload}>Yeniden dene</button>
          </div>
        ) : !entries ? (
          <ul className="g12-ul-rows" aria-label="Yükleniyor">{Array.from({ length: 12 }, (_, i) => <SkelRow key={i} i={i} />)}</ul>
        ) : p.filteredCount === 0 ? (
          <div className="g12-empty">
            <b>Eşleşen terim yok</b>
            <span>Farklı bir terim dene ya da süzgeçleri temizle.</span>
            <button type="button" className="g12-btn is-sm" onClick={p.onResetFilters}>Tüm terimleri göster</button>
          </div>
        ) : (
          <>
            {p.groups.map((g, gi) => {
              const last = gi === p.groups.length - 1;
              return (
                <section key={`${g.key}-${gi}`} aria-label={g.key || undefined}>
                  {g.key && <h2 className="g12-letter" id={p.groupDomId(g.key)}>{g.key}</h2>}
                  <ul className="g12-ul-rows">
                    {g.items.map((e) => (
                      <Row key={e.id} e={e} on={openEntry?.id === e.id} saved={p.saved.has(e.id)} onPick={pick} />
                    ))}
                    {last && p.hasMore && [0, 1, 2].map((i) => <SkelRow key={`sk${i}`} i={i} ref={i === 0 ? p.setSentinel : undefined} />)}
                  </ul>
                </section>
              );
            })}
            <p className="g12-listfoot g12-m" aria-live="polite">
              {p.hasMore
                ? `${p.visibleCount.toLocaleString('tr-TR')} / ${p.filteredCount.toLocaleString('tr-TR')} · kaydırdıkça 40’ar yüklenir`
                : `${p.filteredCount.toLocaleString('tr-TR')} terimin tümü gösteriliyor`}
            </p>
          </>
        )}
      </div>
    </section>
  );

  return (
    <div className={`g12 ${wide ? 'is-wide' : ''}`}>
      {!showDetailOnly && header}
      <div className="g12-split">
        {!showDetailOnly && list}
        {(wide || openEntry) && (
          openEntry ? (
            <EntryDetailV12 key={openEntry.id} {...p} entry={openEntry} detailRef={detailRef} onBack={wide ? undefined : back} />
          ) : (
            <section className="g12-panel g12-detail g12-placeholder" aria-label="Madde ayrıntısı">
              <BookOpenText aria-hidden />
              <b>{entries ? 'Bir terim seç' : 'Sözlük yükleniyor'}</b>
              <span>Tanım, ders notu, ilgili terimler ve geçtiği dersler burada açılır.</span>
            </section>
          )
        )}
      </div>

      <Sheet open={filtersOpen} onClose={() => setFiltersOpen(false)} title="Sözlük süzgeci" width={460}
        footer={<button type="button" className="ui-btn is-primary" style={{ width: '100%' }} onClick={() => setFiltersOpen(false)}>Uygula</button>}>
        <div className="pt-sheet">{p.filters}</div>
      </Sheet>
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* Ayrıntı                                                              */
/* ------------------------------------------------------------------ */

const EntryDetailV12: React.FC<GlossaryV12Props & {
  entry: EncyclopediaEntry;
  detailRef: React.RefObject<HTMLElement | null>;
  onBack?: () => void;
}> = ({ entry, detailRef, onBack, saved, onBookmark, onShare, copied, onReport, onAudit, auditing, auditMessage, related, onOpenRelated, catLabel }) => {
  const isSaved = saved.has(entry.id);
  const aliases = (entry.aliases || []).map((a) => String(a || '').trim()).filter((a) => a && a !== entry.term);
  const abbr = aliases.filter(isAbbr).slice(0, 2);
  const otherNames = aliases.filter((a) => !abbr.includes(a)).slice(0, 4);
  const latin = String(entry.latinName || '').trim();
  const where = [entry.kurul, entry.discipline].filter(Boolean).join(' · ');
  const path = entry.subcategory ? entry.subcategory.split('›').map((s) => s.trim()).filter(Boolean) : [];
  const cardSections = (entry.infoCard?.sections || []).filter((s) => s?.items?.length);
  const rel = useMemo(
    () => (entry.relatedItems || []).map((id) => related(id)).filter((x): x is EncyclopediaEntry => !!x),
    [entry.relatedItems, related],
  );
  const lessons = useMemo(() => lessonRows(entry.instructorAndSource), [entry.instructorAndSource]);
  const isNoteSource = /^ders notu\s*:/i.test(String(entry.instructorAndSource || '').trim());
  const bare = String(entry.term || '').replace(/\s*\([^)]*\)/g, ' ').replace(/\s+/g, ' ').trim();
  const past = usePastCount(bare || null);
  const v15 = useAppearance().v15;
  const derste = useDersteDinle(v15 ? lessons.map((l) => l.title) : [], bare);
  const searchHref = pathFor('search', bare);
  const verified = entry.aiAudit?.verified
    ? `${entry.uretici === 's13_study' || entry.uretici === 'sozluk_v2' ? 'Ders notuyla doğrulandı' : 'Doğrulandı'}${typeof entry.aiAudit.accuracyScore === 'number' ? ` (%${entry.aiAudit.accuracyScore})` : ''}`
    : 'Doğrulama beklemede';

  // Tonlu bölümler (v10/v11'deki renkli bilgi kutuları): başlık + tonlu zeminli gövde
  const sec = (id: string, label: React.ReactNode, body: React.ReactNode, tone?: 'bad' | 'warn' | 'clinic' | 'ai' | 'accent') => (
    <section id={`term-${entry.id}-${id}`} className={`g12-sec ${tone ? `has-tone is-${tone}` : ''}`} aria-label={typeof label === 'string' ? label : undefined}>
      {tone ? (
        <div className="g12-box">
          <h3 className={`g12-sub is-${tone}`}>{label}</h3>
          {body}
        </div>
      ) : (
        <>
          <h3 className="g12-sub">{label}</h3>
          {body}
        </>
      )}
    </section>
  );

  return (
    <article ref={detailRef as React.RefObject<HTMLElement>} className="g12-panel g12-detail" aria-labelledby={`g12-term-${entry.id}`}>
      {onBack && (
        <div className="g12-backbar">
          <button type="button" className="g12-back" onClick={onBack}>
            <ChevronLeft aria-hidden /> Sözlük
          </button>
        </div>
      )}
      <header className="g12-dh">
        <div className="g12-dh-row">
          <h2 id={`g12-term-${entry.id}`} className="g12-title">{entry.term}</h2>
          <button type="button" className="g12-ibtn is-ghost is-sm" onClick={() => onBookmark(entry.id)} aria-pressed={isSaved} aria-label={isSaved ? 'Kayıttan çıkar' : 'Kaydet'} title={isSaved ? 'Kaydedildi' : 'Kaydet'}>
            <Bookmark fill={isSaved ? 'currentColor' : 'none'} aria-hidden />
          </button>
          <button type="button" className="g12-ibtn is-ghost is-sm" onClick={() => onShare(entry)} aria-label={copied ? 'Bağlantı kopyalandı' : 'Paylaş'} title={copied ? 'Kopyalandı' : 'Paylaş'}>
            {copied ? <Check aria-hidden /> : <Share2 aria-hidden />}
          </button>
        </div>
        <p className="g12-meta">
          <span>{catLabel(entry.category)}</span>
          {latin && latin !== entry.term && <><span aria-hidden>·</span><span>İng./Lat. <i>{latin}</i></span></>}
          {abbr.length > 0 && <><span aria-hidden>·</span><span>Kısalt. {abbr.join(', ')}</span></>}
          {where && <><span aria-hidden>·</span><span>{where}</span></>}
        </p>
        {(path.length > 0 || otherNames.length > 0) && (
          <p className="g12-meta">
            {path.length > 0 && <span aria-label="Sınıflandırma">{path.join(' › ')}</span>}
            {path.length > 0 && otherNames.length > 0 && <span aria-hidden>·</span>}
            {otherNames.length > 0 && <span>Diğer adları: {otherNames.join(', ')}</span>}
          </p>
        )}
      </header>

      {v15 && (derste || (past && past.n > 0)) && (
        <div className="g15-cip">
          {derste && <a href={derste.yol} onClick={linkClick(() => navigateTo(derste.yol))} title={derste.ad}><Headphones aria-hidden /> Derste dinle</a>}
          {past && past.n > 0 && <a href={searchHref} onClick={linkClick(() => navigateTo(searchHref))}><CircleHelp aria-hidden /> {past.n.toLocaleString('tr-TR')}{past.capped ? '+' : ''} soru</a>}
        </div>
      )}
      {auditMessage && <p className="g12-status" role="status"><RefreshCw className={auditing ? 'animate-spin' : ''} aria-hidden />{auditMessage}</p>}

      <section id={`term-${entry.id}-def`} className="g12-sec">
        <Rich value={entry.definition as unknown} read />
        {cardSections.length === 1 && !cardSections[0].title && (
          <>
            {cardSections[0].intro && <p className="g12-read is-sm"><Inline text={cardSections[0].intro} /></p>}
            <InfoItems items={cardSections[0].items} />
          </>
        )}
      </section>

      {!(cardSections.length === 1 && !cardSections[0].title) && cardSections.map((s, i) => (
        <section key={i} id={i === 0 ? `term-${entry.id}-card` : undefined} className="g12-sec">
          {s.title && <h3 className="g12-sub">{s.title}</h3>}
          {s.intro && <p className="g12-read is-sm"><Inline text={s.intro} /></p>}
          <InfoItems items={s.items} />
        </section>
      ))}

      {!!line(entry.lectureContextNotes).trim() && sec('lecture', <><GraduationCap aria-hidden />Ders notu</>, <Rich value={entry.lectureContextNotes as unknown} />, 'clinic')}
      {!!line(entry.morphologyOrMechanism).trim() && sec('mech', <><Stethoscope aria-hidden />Patoloji, morfoloji ve mekanizma</>, <div className="g12-pre"><Rich value={entry.morphologyOrMechanism as unknown} /></div>, 'accent')}
      {!!line(entry.differentialDiagnosis).trim() && sec('diff', <><Filter aria-hidden />Ayırıcı tanı</>, <Rich value={entry.differentialDiagnosis as unknown} />, 'ai')}
      {!!line(entry.pitfallsAndWarnings).trim() && sec('pitfalls', <><AlertTriangle aria-hidden />Sınav tuzağı</>, <Rich value={entry.pitfallsAndWarnings as unknown} />, 'bad')}
      {!!line(entry.examSpotPearls).trim() && sec('pearls', <><Lightbulb aria-hidden />Sınav spotu</>, <Rich value={entry.examSpotPearls as unknown} />, 'warn')}

      {rel.length > 0 && sec('related', 'İlgili', (
        <div className="g12-pills">
          {rel.map((r) => (
            <button key={r.id} type="button" className="g12-pill" onClick={() => onOpenRelated(r.id)} title={r.term}>
              <span>{r.term}</span>
            </button>
          ))}
        </div>
      ))}

      {lessons.length > 0 && sec('lessons', isNoteSource ? 'Geçtiği dersler' : 'Kaynak', (
        <ul className="g12-lessons">
          {lessons.map((l) => (
            <li
              key={l.title}
              className="g12-lesson"
              style={{ cursor: 'pointer' }}
              onClick={() => navigateTo(pathFor('search', l.title))}
              title={`${l.title} konusunu tüm kaynaklarda ara`}
            >
              <span className="g12-lead" aria-hidden><FileText /></span>
              <span className="g12-grow">
                <span className="t">{l.title}</span>
                <span className="g12-m">{[where, isNoteSource ? `Ders notu${l.at.length ? `, ${l.at.join(', ')}` : ''}` : ''].filter(Boolean).join(' · ')}</span>
              </span>
            </li>
          ))}
        </ul>
      ))}

      {entry.aiAudit?.sampleExamQuestion && sec('sample', 'Örnek sınav sorusu', <p className="g12-text">{entry.aiAudit.sampleExamQuestion}</p>)}

      <footer className="g12-dfoot">
        {bare && (
          <a className="g12-link" href={searchHref} onClick={linkClick(() => navigateTo(searchHref))}>
            {past && past.n > 0
              ? <>Çıkmış sorularda · <span className="g12-num">{past.n.toLocaleString('tr-TR')}{past.capped ? '+' : ''}</span></>
              : past && past.n === 0 ? 'Tüm kaynaklarda ara' : 'Çıkmış sorularda ara'}
            <ChevronRight aria-hidden />
          </a>
        )}
        <span className="g12-grow" />
        <span className="g12-m">{verified}</span>
      </footer>
      <div className="g12-dacts">
        <button type="button" className="g12-btn is-sm is-ghost" onClick={() => onReport(entry)}>
          <AlertCircle aria-hidden /> Hata bildir
        </button>
        <button type="button" className="g12-btn is-sm is-ghost" onClick={() => onAudit(entry)} disabled={auditing}>
          <RefreshCw className={auditing ? 'animate-spin' : ''} aria-hidden />
          {auditing ? 'Denetleniyor…' : 'Yapay zekâyla denetle'}
        </button>
      </div>
    </article>
  );
};
