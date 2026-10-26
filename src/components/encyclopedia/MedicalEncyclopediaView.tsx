import React, { useState, useMemo, useEffect, useLayoutEffect, useDeferredValue, useCallback, useRef } from 'react';
import { PageToolbar, FilterPills, type ToolbarChip, type ToolbarSegment } from '../ui/PageToolbar';
import { EmptySearch } from '../ui/Animations';
import {
  ChevronDown,
  BookOpenText,
  Sparkles,
  ShieldCheck,
  AlertTriangle,
  Lightbulb,
  GraduationCap,
  RefreshCw,
  X,
  Bookmark,
  Share2,
  Stethoscope,
  Filter,
  Check,
  BrainCircuit,
  HelpCircle,
  Hash,
  AlertCircle,
  Send,
  ListTree,
} from 'lucide-react';
import * as api from '../../services/api';
import { triggerDomHighlightAndScroll, shareDeepLink } from '../../services/universalRedirectService';
import { useAppearance } from '../../utils/appearance';
import { GlossaryV12 } from '../v12/GlossaryV12';
import './glossary.css';

/**
 * Sözlük (v10): kompakt PageToolbar + A–Z akordeon liste.
 *  - Veri (medical_encyclopedia.json, ~3 MB) ekranla birlikte değil, ayrı parça olarak dinamik yüklenir;
 *    araç çubuğu ve iskelet satırlar hemen görünür.
 *  - Liste 40'ar madde çizilir; sondaki iskelet satır görünür olunca 40 daha eklenir (IntersectionObserver).
 *  - Satırlar React.memo; açılan maddenin ayrıntısı yalnız o satırda çizilir (aynı anda tek madde açık).
 *  - geniş ekranda (≥1024, Akış dışı) satır seçilir, ayrıntı sağdaki yapışkan panelde okunur;
 *    diğer görünümlerde her genişlikte tek sütun akordeon.
 *  - Açılan içeriğin görünür alana kaydırılması utils/autoReveal.ts'tedir (aria-expanded + aria-controls);
 *    burada yalnız üstte kapanan maddenin yarattığı kayma düzeltilir.
 */

export type EncyclopediaCategory = string;

/** Bilgi kartı maddesi: düz metin ya da alt maddeli (en çok 3 düzey); **kalın** desteklenir */
export type InfoCardItem = string | { text: string; sub?: InfoCardItem[] };
export interface InfoCardSection { title?: string; intro?: string; items: InfoCardItem[] }

export interface EncyclopediaEntry {
  id: string;
  term: string;
  latinName?: string;
  aliases: string[];
  category: 'hastalik' | 'ilac' | 'patoloji' | 'patojen' | 'genetik' | string;
  kurul: string;
  discipline: string;
  instructorAndSource?: string;
  definition: string;
  lectureContextNotes: string;
  morphologyOrMechanism?: string;
  differentialDiagnosis?: string;
  examSpotPearls?: string;
  pitfallsAndWarnings?: string;
  relatedItems?: string[];
  badgeColor?: string;
  /** Alt sınıf yolu: "Enfeksiyon › Cinsel yolla bulaşan › Bakteriyel" (sözlük v2) */
  subcategory?: string;
  /** Kısa bilgi kartı: iç içe maddeler (sözlük v2, scripts/sozluk_v2) */
  infoCard?: { sections: InfoCardSection[] };
  /** 's13_study': tanım ders notu alıntılarından yazıldı (scripts/v2 study build). */
  uretici?: string;
  aiAudit: {
    verified: boolean;
    verifiedAt: string;
    accuracyScore: number;
    auditSummary: string;
    sampleExamQuestion?: string;
    userNotes?: string;
  };
}

interface MedicalEncyclopediaViewProps {
  initialTermId?: string;
  onNavigateToDeck?: (deckId: string) => void;
}

/** Bir seferde çizilen madde sayısı */
const PAGE = 40;
const ALPHABET = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'.split('');
/** v12 A–Z şeridi: Türkçede sözcük başında gelmeyen Ğ yok */
const V12_ALPHABET = ALPHABET.filter((c) => c !== 'Ğ');
const CUSTOM_KEY = 'medsoru_custom_encyclopedia_v1';
const BOOKMARK_KEY = 'medsoru_bookmarked_encyclopedia';

/** Kategori adları (veri kimliği → kısa Türkçe ad) */
const CAT_LABEL: Record<string, string> = {
  hastalik: 'Hastalık',
  ilac: 'İlaç',
  patoloji: 'Patoloji',
  patojen: 'Patojen',
  genetik: 'Genetik',
  protein: 'Protein',
  tani: 'Tanı & yöntem',
  'halk-sagligi': 'Halk sağlığı',
  terim: 'Terim',
  kisaltma: 'Kısaltma',
  fizyoloji: 'Fizyoloji',
  anatomi: 'Anatomi',
  tedavi: 'Tedavi',
  mikrobiyoloji: 'Mikrobiyoloji',
  parazitoloji: 'Parazitoloji',
  uroloji: 'Üroloji',
};
const catLabel = (c?: string) => CAT_LABEL[c || ''] || (c ? c.charAt(0).toLocaleUpperCase('tr-TR') + c.slice(1) : 'Kavram');
/** Araç çubuğunda segment olarak duran ana kategoriler; gerisi Süzgeç sayfasında */
const SEGMENT_IDS = ['all', 'hastalik', 'patoloji', 'ilac', 'genetik', 'terim', 'kisaltma', 'kart'];
/** Veride İngilizce ya da eşanlamlı gelen kategori adları tek kimliğe indirilir */
const CAT_ALIAS: Record<string, string> = { pathology: 'patoloji', genetic: 'genetik', epidemiyoloji: 'halk-sagligi' };

const firstLetterOf = (t?: string) => {
  const ch = String(t || '').trim().charAt(0).toLocaleUpperCase('tr-TR');
  return ALPHABET.includes(ch) ? ch : '#';
};
const collator = new Intl.Collator('tr', { sensitivity: 'base' });
const prefersReducedMotion = () =>
  typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const getGlossaryUrlTarget = (): string | null => {
  if (typeof window === 'undefined') return null;
  try {
    const sp = new URLSearchParams(window.location.search);
    const q = sp.get('id') || sp.get('term') || sp.get('terim');
    if (q) return q;
    const clean = window.location.pathname.replace(/^\/meds(?=\/|$)/, '');
    const m = clean.match(/^\/sozluk\/([^\/?#]+)/);
    return m ? decodeURIComponent(m[1]) : null;
  } catch {
    return null;
  }
};

/* ------------------------------------------------------------------ */
/* Veri: dinamik yükleme + yerel düzeltmeler + hafif dizin              */
/* ------------------------------------------------------------------ */

let dataPromise: Promise<EncyclopediaEntry[]> | null = null;
/** Ham sözlüğü ayrı parça olarak bir kez indirir (glossary.ts de aynı parçayı kullanır) */
const loadEncyclopedia = (): Promise<EncyclopediaEntry[]> => {
  if (!dataPromise) {
    dataPromise = import('../../data/medical_encyclopedia.json')
      .then((m) => ((m as { default?: unknown }).default ?? m) as unknown as EncyclopediaEntry[])
      .catch((err) => {
        dataPromise = null;
        throw err;
      });
  }
  return dataPromise;
};

/** Kayıtlı yerel düzeltmeleri ham sözlük verisine uygular */
const applyLocalEdits = (raw: EncyclopediaEntry[]): EncyclopediaEntry[] => {
  try {
    const stored = localStorage.getItem(CUSTOM_KEY);
    if (stored) {
      const parsed = JSON.parse(stored) as Record<string, Partial<EncyclopediaEntry>>;
      return raw.map((entry) =>
        parsed[entry.id]
          ? { ...entry, ...parsed[entry.id], aiAudit: { ...entry.aiAudit, ...(parsed[entry.id]?.aiAudit || {}) } }
          : entry,
      );
    }
  } catch (e) {
    console.error('Local encyclopedia read error:', e);
  }
  return raw;
};

/** Kategori adını tek kimliğe indirir; adı boş gelen maddelere kimlikten okunur ad verir */
const normalizeEntry = (e0: EncyclopediaEntry): EncyclopediaEntry => {
  const c = String(e0.category || '').toLowerCase();
  const cat = CAT_ALIAS[c] || (c.startsWith('patoloji') ? 'patoloji' : c);
  const e = cat !== e0.category ? { ...e0, category: cat } : e0;
  if (String(e.term || '').trim()) return e;
  const raw = String(e.id || '').replace(/[-_]+/g, ' ').trim();
  return { ...e, term: raw ? raw.charAt(0).toLocaleUpperCase('tr-TR') + raw.slice(1) : 'Adsız madde' };
};

export interface IndexedEncyclopediaEntry extends EncyclopediaEntry {
  _termNorm: string;
  _firstLetter: string;
  /** Alfabetik sıra (yüklemede bir kez hesaplanır) */
  _rank: number;
}

const indexEntry = (e: EncyclopediaEntry, rank = 0): IndexedEncyclopediaEntry => ({
  ...e,
  _termNorm: String(e.term || '').toLocaleLowerCase('tr-TR'),
  _firstLetter: firstLetterOf(e.term),
  _rank: rank,
});

const hasInfoCard = (e: EncyclopediaEntry) => !!e.infoCard?.sections?.some((s) => s?.items?.length);

const infoCardText = (card?: EncyclopediaEntry['infoCard']): string => {
  const walk = (items?: InfoCardItem[]): string[] =>
    (items || []).flatMap((it) => (typeof it === 'string' ? [it] : [it?.text || '', ...walk(it?.sub)]));
  return (card?.sections || []).flatMap((s) => [s.title || '', s.intro || '', ...walk(s.items)]).join(' ').replace(/\*\*/g, '');
};

const asText = (v: unknown): string =>
  v == null ? '' : typeof v === 'string' ? v : Array.isArray(v) ? v.map(asText).join(' ') : JSON.stringify(v);

/** Arama metni maddeye özgü, ilk aramada (ya da boşta) bir kez üretilir */
const corpusCache = new WeakMap<EncyclopediaEntry, string>();
const corpusOf = (e: EncyclopediaEntry): string => {
  let c = corpusCache.get(e);
  if (c === undefined) {
    c = [
      e.term, e.latinName, ...(e.aliases || []), e.subcategory, infoCardText(e.infoCard),
      asText(e.definition), asText(e.lectureContextNotes), asText(e.examSpotPearls),
      asText(e.morphologyOrMechanism), asText(e.differentialDiagnosis), asText(e.pitfallsAndWarnings),
    ].filter(Boolean).join(' ').toLocaleLowerCase('tr-TR');
    corpusCache.set(e, c);
  }
  return c;
};

/* ------------------------------------------------------------------ */
/* Küçük yardımcı bileşenler                                            */
/* ------------------------------------------------------------------ */

/** Sözlük alanı metin, metin listesi ya da nesne listesi olabilir ({condition, distinction} gibi); hepsini okunur gösterir */
const RichField: React.FC<{ value: unknown }> = ({ value }) => {
  const line = (v: unknown): string =>
    v == null ? '' : typeof v === 'string' || typeof v === 'number' ? String(v)
      : Array.isArray(v) ? v.map(line).filter(Boolean).join(' · ')
      : Object.values(v as Record<string, unknown>).map(line).filter(Boolean).join(' — ');
  if (Array.isArray(value)) {
    const items = value.map(line).filter(Boolean);
    if (!items.length) return null;
    return (
      <ul className="gx-points">
        {items.map((t, i) => <li key={i}>{t}</li>)}
      </ul>
    );
  }
  return <>{line(value)}</>;
};

/** "**kalın**" işaretini <strong>'a çevirir (bilgi kartı maddeleri) */
const Inline: React.FC<{ text: string }> = ({ text }) => (
  <>
    {String(text).split(/(\*\*[^*]+\*\*)/g).map((part, i) =>
      part.startsWith('**') && part.endsWith('**') && part.length > 4
        ? <strong key={i} className="text-ink">{part.slice(2, -2)}</strong>
        : <React.Fragment key={i}>{part}</React.Fragment>,
    )}
  </>
);

const InfoItems: React.FC<{ items?: InfoCardItem[]; depth?: number }> = ({ items, depth = 1 }) => {
  if (!items?.length) return null;
  return (
    <ul className={`gx-tree is-d${depth}`}>
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

/** Bilgi kartı: başlıklı bölümler + iç içe maddeler */
const InfoCardView: React.FC<{ card?: EncyclopediaEntry['infoCard'] }> = ({ card }) => {
  const sections = (card?.sections || []).filter((s) => s?.items?.length);
  if (!sections.length) return null;
  return (
    <div className="gx-info">
      {sections.map((s, i) => (
        <section key={i} className="gx-info-s">
          {s.title && <h4 className="gx-info-t">{s.title}</h4>}
          {s.intro && <p className="gx-info-i"><Inline text={s.intro} /></p>}
          <InfoItems items={s.items} />
        </section>
      ))}
    </div>
  );
};

/** Geniş ekran mı (ana-ayrıntı düzeni) */
const useWide = () => {
  const q = '(min-width: 1024px)';
  const [wide, setWide] = useState(() => typeof window !== 'undefined' && window.matchMedia(q).matches);
  useEffect(() => {
    const m = window.matchMedia(q);
    const on = () => setWide(m.matches);
    m.addEventListener('change', on);
    return () => m.removeEventListener('change', on);
  }, []);
  return wide;
};

/** Öğenin kaydırılan atası (yoksa pencere) */
const scrollParentOf = (el: HTMLElement): HTMLElement | Window => {
  let p = el.parentElement;
  while (p && p !== document.body && p !== document.documentElement) {
    const oy = getComputedStyle(p).overflowY;
    if ((oy === 'auto' || oy === 'scroll') && p.scrollHeight > p.clientHeight) return p;
    p = p.parentElement;
  }
  return window;
};

/* ------------------------------------------------------------------ */
/* Satır ve iskelet                                                     */
/* ------------------------------------------------------------------ */

interface RowProps {
  entry: IndexedEncyclopediaEntry;
  open: boolean;
  saved: boolean;
  /** true: akordeon (telefon/tablet); false: seçim (geniş ekran, ayrıntı sağ panelde) */
  inline: boolean;
  onToggle: (id: string) => void;
  /** Yalnız açık satıra verilir; kapalı satırlarda null (memo bozulmasın) */
  detail: React.ReactNode;
}

const GlossaryRow = React.memo<RowProps>(({ entry, open, saved, inline, onToggle, detail }) => {
  const panelId = `term-${entry.id}-panel`;
  const sub = [catLabel(entry.category), entry.discipline].filter(Boolean).join(' · ');
  return (
    <li id={`term-${entry.id}`} className={`gz-li ${open ? 'is-open' : ''}`}>
      <button
        type="button"
        className={`gz-row ${open && !inline ? 'is-on' : ''}`}
        onClick={() => onToggle(entry.id)}
        aria-expanded={inline ? open : undefined}
        aria-controls={inline ? panelId : undefined}
        aria-current={!inline && open ? 'true' : undefined}
      >
        <span className="gz-t">
          <b>{entry.term}</b>
          <span>{entry.latinName ? `${entry.latinName} · ${sub}` : sub}</span>
        </span>
        <span className="gz-meta">
          {saved && <Bookmark className="gz-saved" fill="currentColor" aria-label="Kaydedildi" />}
          {entry.aiAudit?.verified && <ShieldCheck className="gz-ok" aria-label="Doğrulanmış" />}
          {entry.kurul && <span>{String(entry.kurul).replace('Kurul ', 'K')}</span>}
        </span>
        {inline && <ChevronDown className="gz-chev" aria-hidden />}
      </button>
      {inline && open && detail && (
        <div id={panelId} className="gz-detail" role="region" aria-label={entry.term}>
          {detail}
        </div>
      )}
    </li>
  );
});
GlossaryRow.displayName = 'GlossaryRow';

const SKEL_W: [string, string][] = [['46%', '28%'], ['58%', '24%'], ['40%', '30%'], ['52%', '22%'], ['36%', '26%']];
/** Gerçek satırla aynı yükseklikte (48 px) iskelet satır */
const SkeletonRow = React.forwardRef<HTMLLIElement, { i: number }>(({ i }, ref) => {
  const [a, b] = SKEL_W[i % SKEL_W.length];
  return (
    <li ref={ref} className="gz-li gz-sk" aria-hidden>
      <span className="ui-skel" style={{ width: a }} />
      <span className="ui-skel" style={{ width: b }} />
    </li>
  );
});
SkeletonRow.displayName = 'SkeletonRow';

/* ------------------------------------------------------------------ */
/* Ayrıntı                                                              */
/* ------------------------------------------------------------------ */

interface DetailProps {
  entry: EncyclopediaEntry;
  variant: 'inline' | 'pane';
  saved: boolean;
  copied: boolean;
  auditing: boolean;
  auditMessage: string | null;
  related: (id: string) => EncyclopediaEntry | undefined;
  onBookmark: (id: string) => void;
  onShare: (entry: EncyclopediaEntry) => void;
  onReport: (entry: EncyclopediaEntry) => void;
  onAudit: (entry: EncyclopediaEntry) => void;
  onOpenRelated: (id: string) => void;
  onClose?: () => void;
}

const EntryDetail: React.FC<DetailProps> = ({
  entry, variant, saved, copied, auditing, auditMessage, related, onBookmark, onShare, onReport, onAudit, onOpenRelated, onClose,
}) => {
  const verifiedLabel = entry.aiAudit?.verified
    ? `${entry.uretici === 's13_study' || entry.uretici === 'sozluk_v2' ? 'Ders notuyla doğrulandı' : 'Doğrulandı'}${typeof entry.aiAudit.accuracyScore === 'number' ? ` (%${entry.aiAudit.accuracyScore})` : ''}`
    : '';
  const tags = (
    <div className="gz-tags">
      <span className="gz-tag is-accent">{catLabel(entry.category)}</span>
      {(entry.kurul || entry.discipline) && <span className="gz-tag">{[entry.kurul, entry.discipline].filter(Boolean).join(' · ')}</span>}
      {verifiedLabel && <span className="gz-tag is-ok"><ShieldCheck aria-hidden />{verifiedLabel}</span>}
    </div>
  );
  const path = entry.subcategory ? (
    <p className="gx-path" aria-label="Sınıflandırma">
      {entry.subcategory.split('›').map((p) => p.trim()).filter(Boolean).map((p, i) => <span key={i}>{p}</span>)}
    </p>
  ) : null;
  const actions = (
    <div className="gz-actions">
      <button type="button" className="gz-act" onClick={() => onBookmark(entry.id)} aria-pressed={saved}>
        <Bookmark fill={saved ? 'currentColor' : 'none'} aria-hidden /> {saved ? 'Kaydedildi' : 'Kaydet'}
      </button>
      <button type="button" className="gz-act" onClick={() => onShare(entry)}>
        {copied ? <Check aria-hidden /> : <Share2 aria-hidden />} {copied ? 'Kopyalandı' : 'Paylaş'}
      </button>
      <button type="button" className="gz-act" onClick={() => onReport(entry)}>
        <AlertCircle aria-hidden /> Hata bildir
      </button>
      <button type="button" className="gz-act is-ai" onClick={() => onAudit(entry)} disabled={auditing}>
        <RefreshCw className={auditing ? 'animate-spin' : ''} aria-hidden />
        {auditing ? 'Denetleniyor…' : 'Yapay zekâyla denetle'}
      </button>
    </div>
  );

  const body = (
    <>
      {auditMessage && (
        <div className="ds-callout is-note">
          <Sparkles className="w-4 h-4 shrink-0" aria-hidden />
          <span>{auditMessage}</span>
        </div>
      )}

      <div id={`term-${entry.id}-def`} className="gz-def">
        <RichField value={entry.definition as unknown} />
      </div>

      {hasInfoCard(entry) && (
        <div id={`term-${entry.id}-card`} className="ds-callout gx-info-box">
          <span className="ds-callout-t"><ListTree aria-hidden /><span>Bilgi kartı</span></span>
          <InfoCardView card={entry.infoCard} />
        </div>
      )}

      {entry.lectureContextNotes && (
        <div id={`term-${entry.id}-lecture`} className="ds-callout is-clinic">
          <span className="ds-callout-t"><GraduationCap aria-hidden /><span>Ders notu</span></span>
          {entry.instructorAndSource && (
            <span className="gz-src">{entry.instructorAndSource.replace(/\.txt\b/gi, '').replace(/^\d+\)\s*/, '')}</span>
          )}
          <div><RichField value={entry.lectureContextNotes as unknown} /></div>
        </div>
      )}

      {entry.morphologyOrMechanism && (
        <div id={`term-${entry.id}-mech`} className="ds-callout">
          <span className="ds-callout-t"><Stethoscope aria-hidden /><span>Patoloji, morfoloji ve mekanizma</span></span>
          <div className="whitespace-pre-line"><RichField value={entry.morphologyOrMechanism as unknown} /></div>
        </div>
      )}

      {entry.differentialDiagnosis && (
        <div id={`term-${entry.id}-diff`} className="ds-callout is-note">
          <span className="ds-callout-t"><Filter aria-hidden /><span>Ayırıcı tanı</span></span>
          <div><RichField value={entry.differentialDiagnosis as unknown} /></div>
        </div>
      )}

      {entry.pitfallsAndWarnings && (
        <div id={`term-${entry.id}-pitfalls`} className="ds-callout is-bad">
          <span className="ds-callout-t"><AlertTriangle aria-hidden /><span>Sınav tuzağı</span></span>
          <div><RichField value={entry.pitfallsAndWarnings as unknown} /></div>
        </div>
      )}

      {entry.examSpotPearls && (
        <div id={`term-${entry.id}-pearls`} className="ds-callout is-important">
          <span className="ds-callout-t"><Lightbulb aria-hidden /><span>Sınav spotu</span></span>
          <div><RichField value={entry.examSpotPearls as unknown} /></div>
        </div>
      )}

      {!!entry.relatedItems?.length && (
        <div className="gz-related">
          <span className="ds-label">İlişkili maddeler</span>
          <div className="gz-related-l">
            {entry.relatedItems.map((relId) => {
              const rel = related(relId);
              return (
                <button key={relId} type="button" className="gz-rel" disabled={!rel} onClick={() => rel && onOpenRelated(rel.id)}>
                  <Hash aria-hidden />
                  <span>{rel ? rel.term : relId}</span>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {entry.aiAudit?.sampleExamQuestion && (
        <div className="ds-callout">
          <span className="ds-callout-t"><HelpCircle aria-hidden /><span>Örnek sınav sorusu</span></span>
          <p className="m-0">{entry.aiAudit.sampleExamQuestion}</p>
        </div>
      )}
    </>
  );

  if (variant === 'inline') {
    return (
      <>
        {tags}
        {path}
        {body}
        {actions}
      </>
    );
  }

  return (
    <article className="gz-pane" key={entry.id}>
      <header className="gz-pane-h">
        <div className="gz-pane-ht">
          <h2>{entry.term}</h2>
          {entry.latinName && <p className="gz-latin">{entry.latinName}</p>}
          {path}
        </div>
        {onClose && (
          <button type="button" className="gz-x" onClick={onClose} aria-label="Ayrıntıyı kapat">
            <X aria-hidden />
          </button>
        )}
      </header>
      {tags}
      {body}
      <div className="gz-pane-note">
        <BrainCircuit aria-hidden />
        <span>Doğrulama: <strong>{verifiedLabel || 'Beklemede'}</strong></span>
      </div>
      {actions}
    </article>
  );
};

/* ------------------------------------------------------------------ */
/* Harf dizini (telefon): ince dikey ray, dokun ya da sürükle           */
/* ------------------------------------------------------------------ */

const LetterRail: React.FC<{ letters: Set<string>; onJump: (ch: string) => void }> = ({ letters, onJump }) => {
  const last = useRef<string | null>(null);
  const pick = (e: React.PointerEvent<HTMLElement>) => {
    const rail = e.currentTarget.getBoundingClientRect();
    const el = document.elementFromPoint(rail.left + rail.width / 2, e.clientY) as HTMLElement | null;
    const ch = el?.closest<HTMLElement>('[data-l]')?.dataset.l;
    if (ch && ch !== last.current && letters.has(ch)) {
      last.current = ch;
      onJump(ch);
    }
  };
  return (
    <nav
      className="gz-rail"
      aria-label="Harf dizini"
      onPointerDown={(e) => {
        if (e.pointerType === 'mouse') return; // farede tıklama düğmeye kalır
        last.current = null;
        e.currentTarget.setPointerCapture(e.pointerId);
        pick(e);
      }}
      onPointerMove={(e) => { if (e.currentTarget.hasPointerCapture(e.pointerId)) pick(e); }}
      onPointerUp={(e) => { if (e.currentTarget.hasPointerCapture(e.pointerId)) e.currentTarget.releasePointerCapture(e.pointerId); }}
    >
      {ALPHABET.map((ch) => (
        <button
          key={ch}
          type="button"
          data-l={ch}
          disabled={!letters.has(ch)}
          onClick={() => { if (last.current !== ch) onJump(ch); last.current = null; }}
          aria-label={`${ch} harfine git`}
        >
          {ch}
        </button>
      ))}
    </nav>
  );
};

/* ------------------------------------------------------------------ */
/* Ekran                                                                */
/* ------------------------------------------------------------------ */

type SortMode = 'default' | 'az' | 'za' | 'kurul';
type Pending = { kind: 'id' | 'letter'; value: string; at: number };

export const MedicalEncyclopediaView: React.FC<MedicalEncyclopediaViewProps> = ({ initialTermId }) => {
  // Veri ayrı parça olarak gelir; gelene dek iskelet satırlar gösterilir
  const [entries, setEntries] = useState<IndexedEncyclopediaEntry[] | null>(null);
  const [loadError, setLoadError] = useState(false);
  const [reloadKey, setReloadKey] = useState(0);
  useEffect(() => {
    let alive = true;
    setLoadError(false);
    loadEncyclopedia()
      .then((raw) => {
        if (!alive) return;
        const list = applyLocalEdits(Array.isArray(raw) ? raw : []).map(normalizeEntry);
        const order = list.map((e, i) => ({ i, k: String(e.term || '') })).sort((a, b) => collator.compare(a.k, b.k));
        const ranked: IndexedEncyclopediaEntry[] = new Array(list.length);
        order.forEach((o, r) => { ranked[r] = indexEntry(list[o.i], r); });
        setEntries(ranked);
      })
      .catch((err) => {
        console.error('Sözlük yüklenemedi:', err);
        if (alive) setLoadError(true);
      });
    return () => { alive = false; };
  }, [reloadKey]);

  // Boşta arama metinlerini parça parça hazırla (ilk arama takılmasın)
  useEffect(() => {
    if (!entries) return;
    let i = 0;
    let handle = 0;
    const ric: (cb: () => void) => number = (window as any).requestIdleCallback
      ? (cb) => (window as any).requestIdleCallback(cb, { timeout: 2000 })
      : (cb) => window.setTimeout(cb, 120);
    const cic = (h: number) => ((window as any).cancelIdleCallback ? (window as any).cancelIdleCallback(h) : clearTimeout(h));
    const step = () => {
      const end = Math.min(entries.length, i + 250);
      for (; i < end; i++) corpusOf(entries[i]);
      if (i < entries.length) handle = ric(step);
    };
    handle = ric(step);
    return () => cic(handle);
  }, [entries]);

  const byId = useMemo(() => {
    const m = new Map<string, IndexedEncyclopediaEntry>();
    (entries || []).forEach((e) => m.set(e.id, e));
    return m;
  }, [entries]);
  const related = useCallback((id: string) => byId.get(id), [byId]);

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<EncyclopediaCategory>('all');
  const [selectedKurul, setSelectedKurul] = useState<string>('Tümü');
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('Tümü');
  const [onlyAiVerified, setOnlyAiVerified] = useState(false);
  const [onlySaved, setOnlySaved] = useState(false);
  const [sortMode, setSortMode] = useState<SortMode>('default');

  const [openId, setOpenId] = useState<string | null>(null);

  const [isAiAuditing, setIsAiAuditing] = useState(false);
  const [auditMessage, setAuditMessage] = useState<string | null>(null);
  const [copiedLink, setCopiedLink] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [reportingEntry, setReportingEntry] = useState<EncyclopediaEntry | null>(null);
  const [reportReason, setReportReason] = useState('Tanım / Bilgi hatalı');
  const [reportDetails, setReportDetails] = useState('');
  const [reportSuggestedAnswer, setReportSuggestedAnswer] = useState('');
  const [isSubmittingReport, setIsSubmittingReport] = useState(false);

  const [bookmarkedIds, setBookmarkedIds] = useState<string[]>(() => {
    try {
      return JSON.parse(localStorage.getItem(BOOKMARK_KEY) || '[]');
    } catch {
      return [];
    }
  });
  const bookmarkedSet = useMemo(() => new Set(bookmarkedIds), [bookmarkedIds]);

  const toggleBookmark = useCallback((id: string) => {
    setBookmarkedIds((prev) => {
      const next = prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id];
      try {
        localStorage.setItem(BOOKMARK_KEY, JSON.stringify(next));
      } catch (err) {
        console.error(err);
      }
      return next;
    });
  }, []);

  const handleOpenReport = useCallback((entry: EncyclopediaEntry) => {
    setReportingEntry(entry);
    setShowReportModal(true);
  }, []);

  const handleReportSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reportingEntry) return;
    if (!reportDetails.trim() && !reportSuggestedAnswer.trim()) {
      alert('Lütfen hata veya düzeltme önerinizi açıklayın.');
      return;
    }
    setIsSubmittingReport(true);
    try {
      const detailsWithAnswer = reportSuggestedAnswer.trim()
        ? `${reportDetails.trim()}\n[Önerilen Doğru Bilgi]: ${reportSuggestedAnswer.trim()}`
        : reportDetails.trim();
      await api.ApiService.reportTerm(reportingEntry.id, reportReason, detailsWithAnswer, 'Öğrenci');
      alert('Hata bildiriminiz yapay zeka denetim kuyruğuna alındı.');
      setShowReportModal(false);
      setReportDetails('');
      setReportSuggestedAnswer('');
      setReportingEntry(null);
    } catch (err: any) {
      alert(`Bildirim gönderilemedi: ${err.message || 'Bilinmeyen hata'}`);
    } finally {
      setIsSubmittingReport(false);
    }
  };

  /* ---------------- Sayımlar ve süzgeç seçenekleri ---------------- */

  const { catCount, cardCount, kurulOptions, disciplineOptions } = useMemo(() => {
    const cats = new Map<string, number>();
    const kuruls = new Map<string, number>();
    const discs = new Set<string>();
    let cards = 0;
    for (const e of entries || []) {
      const c = String(e.category || '');
      cats.set(c, (cats.get(c) || 0) + 1);
      if (e.kurul) kuruls.set(String(e.kurul), (kuruls.get(String(e.kurul)) || 0) + 1);
      if (e.discipline) discs.add(e.discipline);
      if (hasInfoCard(e)) cards++;
    }
    return {
      catCount: cats,
      cardCount: cards,
      kurulOptions: [...kuruls.entries()].sort((a, b) => collator.compare(a[0], b[0])),
      disciplineOptions: [...discs].sort((a, b) => collator.compare(a, b)),
    };
  }, [entries]);
  const total = entries?.length || 0;

  /* ---------------- Süzme ve sıralama ---------------- */

  const deferredSearchQuery = useDeferredValue(searchQuery);
  const filteredEntries = useMemo(() => {
    if (!entries) return [] as IndexedEncyclopediaEntry[];
    const rawQ = deferredSearchQuery.trim().toLocaleLowerCase('tr-TR');
    const qTokens = rawQ ? rawQ.split(/\s+/).filter(Boolean) : null;
    const list = entries.filter((e) => {
      if (onlySaved && !bookmarkedSet.has(e.id)) return false;
      if (selectedCategory === 'kart') { if (!hasInfoCard(e)) return false; }
      else if (selectedCategory !== 'all' && e.category !== selectedCategory) return false;
      if (selectedKurul !== 'Tümü' && e.kurul !== selectedKurul) return false;
      if (selectedDiscipline !== 'Tümü' && e.discipline !== selectedDiscipline) return false;
      if (onlyAiVerified && !e.aiAudit?.verified) return false;
      if (qTokens) {
        const c = corpusOf(e);
        for (let i = 0; i < qTokens.length; i++) if (!c.includes(qTokens[i])) return false;
      }
      return true;
    });
    // Aramada isabet sırası: tam ad → ad başı → adda geçen → takma ad → metinde geçen
    if (qTokens && sortMode === 'default') {
      const score = (e: IndexedEncyclopediaEntry) =>
        e._termNorm === rawQ ? 0
          : e._termNorm.startsWith(rawQ) ? 1
          : e._termNorm.includes(rawQ) ? 2
          : (e.aliases || []).some((a) => String(a).toLocaleLowerCase('tr-TR').includes(rawQ)) ? 3 : 4;
      return list.map((e) => ({ e, s: score(e) })).sort((a, b) => a.s - b.s || a.e._rank - b.e._rank).map((x) => x.e);
    }
    if (sortMode === 'za') return list.reverse();
    if (sortMode === 'kurul') {
      return list.sort((a, b) => collator.compare(String(a.kurul ?? 'ÿ'), String(b.kurul ?? 'ÿ')) || a._rank - b._rank);
    }
    return list; // varsayılan ve A→Z: yüklemedeki alfabetik sıra korunur
  }, [entries, deferredSearchQuery, selectedCategory, selectedKurul, selectedDiscipline, onlyAiVerified, onlySaved, bookmarkedSet, sortMode]);

  /** Harf grupları yalnız aramasız alfabetik sıralamada; kurul sırasında kurul başlıkları */
  const grouped = !deferredSearchQuery.trim() && sortMode !== 'kurul';
  const groupKeyOf = useCallback(
    (e: IndexedEncyclopediaEntry) => (sortMode === 'kurul' ? String(e.kurul || 'Diğer') : grouped ? e._firstLetter : ''),
    [sortMode, grouped],
  );
  const letterSet = useMemo(
    () => new Set(grouped ? filteredEntries.map((e) => e._firstLetter) : []),
    [filteredEntries, grouped],
  );

  /* ---------------- Kademeli çizim (40'ar) ---------------- */

  const [limit, setLimit] = useState(PAGE);
  const filterSig = `${deferredSearchQuery}|${selectedCategory}|${selectedKurul}|${selectedDiscipline}|${onlyAiVerified}|${onlySaved}|${sortMode}`;
  // Süzgeç değişince baştan 40 (bu etki, aşağıdaki hedef etkisinden ÖNCE tanımlı kalmalı)
  useEffect(() => { setLimit(PAGE); }, [filterSig]);

  const visible = useMemo(() => filteredEntries.slice(0, limit), [filteredEntries, limit]);
  const hasMore = filteredEntries.length > limit;
  const groups = useMemo(() => {
    const out: { key: string; items: IndexedEncyclopediaEntry[] }[] = [];
    for (const e of visible) {
      const k = groupKeyOf(e);
      const g = out[out.length - 1];
      if (g && g.key === k) g.items.push(e);
      else out.push({ key: k, items: [e] });
    }
    return out;
  }, [visible, groupKeyOf]);

  const [sentinel, setSentinel] = useState<HTMLLIElement | null>(null);
  useEffect(() => {
    if (!sentinel || !hasMore || typeof IntersectionObserver === 'undefined') return;
    // Her eklemeden sonra yeniden gözlenir: iskelet hâlâ görünürse 40 daha eklenir
    const io = new IntersectionObserver(
      (list) => { if (list.some((x) => x.isIntersecting)) setLimit((n) => n + PAGE); },
      { rootMargin: '0px 0px 600px 0px' },
    );
    io.observe(sentinel);
    return () => io.disconnect();
  }, [sentinel, hasMore, limit]);

  /* ---------------- Açma/kapama, hedefe gitme ---------------- */

  const isWide = useWide();
  const { layout, design } = useAppearance();
  // v11: geniş ekranda liste + ayrıntı bölmesi varsayılan (Akış modunda tek sütun akordeon kalır)
  // v12: geniş ekranda liste + ayrıntı; Akış (sade) modunda tek sütun, ayrıntı tam görünüm (GlossaryV12)
  const v12 = design === 'v12';
  const wide = isWide && (design === 'v10' ? layout === 'odak' : layout !== 'akis');
  const wideRef = useRef(wide);
  wideRef.current = wide;
  const anchorRef = useRef<{ id: string; top: number } | null>(null);

  const onToggle = useCallback((id: string) => {
    const el = document.getElementById(`term-${id}`);
    anchorRef.current = el ? { id, top: el.getBoundingClientRect().top } : null;
    setAuditMessage(null);
    setOpenId((prev) => (prev === id && !wideRef.current ? null : id));
  }, []);

  // v12: seçim akordeon gibi kapanmaz; dar ekranda kapatma geri düğmesindedir
  const selectEntry = useCallback((id: string) => { setAuditMessage(null); setOpenId(id); }, []);
  const closeEntry = useCallback(() => setOpenId(null), []);

  // Üstteki açık madde kapanınca dokunulan satır yerinde kalsın (görünür alana getirme: autoReveal)
  useLayoutEffect(() => {
    const a = anchorRef.current;
    anchorRef.current = null;
    if (!a || wide) return;
    const el = document.getElementById(`term-${a.id}`);
    if (!el) return;
    const delta = el.getBoundingClientRect().top - a.top;
    if (Math.abs(delta) > 1) scrollParentOf(el).scrollBy({ top: delta, behavior: 'auto' });
  }, [openId, wide]);

  // Hedef (madde ya da harf) henüz çizilmemişse sınır o noktaya kadar büyütülür, sonra kaydırılır
  const [pending, setPending] = useState<Pending | null>(null);
  useEffect(() => {
    if (!pending || !entries) return;
    if (Date.now() - pending.at > 4000) { setPending(null); return; }
    const idx = pending.kind === 'id'
      ? filteredEntries.findIndex((e) => e.id === pending.value)
      : filteredEntries.findIndex((e) => e._firstLetter === pending.value);
    if (idx < 0) return; // süzgeç/arama yetişince yeniden denenir
    if (idx >= limit) {
      setLimit(Math.ceil((idx + 1) / PAGE) * PAGE + PAGE);
      return;
    }
    const target = pending;
    setPending(null);
    requestAnimationFrame(() => {
      const el = document.getElementById(target.kind === 'id' ? `term-${target.value}` : `gz-h-${target.value}`);
      if (!el) return;
      if (target.kind === 'letter') el.scrollIntoView({ block: 'start', behavior: 'auto' });
      else el.scrollIntoView({ block: wide ? 'nearest' : 'start', behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
    });
  }, [pending, filteredEntries, limit, entries, wide]);

  const jumpToLetter = useCallback((ch: string) => setPending({ kind: 'letter', value: ch, at: Date.now() }), []);

  const resetFilters = useCallback(() => {
    setSearchQuery('');
    setSelectedCategory('all');
    setSelectedKurul('Tümü');
    setSelectedDiscipline('Tümü');
    setOnlyAiVerified(false);
    setOnlySaved(false);
    setSortMode('default');
  }, []);

  /** Maddeyi açar ve ona kaydırır; süzgeç dışında kalıyorsa süzgeçler temizlenir */
  const filteredRef = useRef(filteredEntries);
  filteredRef.current = filteredEntries;
  const focusEntry = useCallback((id: string) => {
    if (!filteredRef.current.some((e) => e.id === id)) resetFilters();
    setAuditMessage(null);
    setOpenId(id);
    setPending({ kind: 'id', value: id, at: Date.now() });
  }, [resetFilters]);

  // Derin bağlantı (initialTermId ya da /sozluk/<id> ya da ?id= / ?term=) ve evrensel vurgulama
  const loaded = !!entries;
  useEffect(() => {
    if (!loaded || typeof window === 'undefined') return;
    const urlParams = new URLSearchParams(window.location.search);
    const targetId = initialTermId || getGlossaryUrlTarget();
    const highlight = urlParams.get('highlight');
    if (targetId) {
      // Arama sonucunda kimlik yerine terim ADI gelir ("apoptoz", "Apoptoz (Programlı Hücre Ölümü)"):
      // kimlik → tam ad → parantezsiz ad → eşanlamlı sırasıyla eşlenir.
      const norm = (t?: string) => (t || '').toLocaleLowerCase('tr').replace(/\s*\(.*?\)\s*/g, ' ').replace(/\s+/g, ' ').trim();
      const want = targetId.toLocaleLowerCase('tr').trim();
      const wantBare = norm(targetId);
      const list = entries || [];
      const found =
        byId.get(targetId) ||
        list.find((e) => (e.id || '').toLocaleLowerCase('tr').trim() === want) ||
        list.find((e) => (e.term || '').toLocaleLowerCase('tr').trim() === want) ||
        list.find((e) => norm(e.term) === wantBare) ||
        list.find((e) => (e.aliases || []).some((al) => norm(al) === wantBare));
      if (found) {
        focusEntry(found.id);
        if (highlight) setTimeout(() => triggerDomHighlightAndScroll(highlight), 700);
      } else {
        // Ansiklopedide karşılığı olmayan terim (ör. tıbbi terimler sözlüğü): liste o terimle süzülür.
        setOpenId(null);
        setSearchQuery(targetId.replace(/\s*\(.*?\)\s*/g, ' ').trim());
      }
    } else if (highlight) {
      setTimeout(() => triggerDomHighlightAndScroll(highlight), 400);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialTermId, loaded]);

  // Geniş ekranda hedef yoksa ilk madde kendiliğinden seçili gelir (boş panel kalmasın)
  const firstFilteredId = filteredEntries[0]?.id;
  useEffect(() => {
    const hasTarget = Boolean(initialTermId || getGlossaryUrlTarget());
    if (wide && !openId && !hasTarget && firstFilteredId) setOpenId(firstFilteredId);
  }, [wide, openId, initialTermId, firstFilteredId]);

  // Geri / ileri: adresteki terim ayrıntıyı açar ya da kapatır
  useEffect(() => {
    const onPop = () => {
      const clean = window.location.pathname.replace(/^\/meds(?=\/|$)/, '');
      if (!/^\/sozluk(?:\/|$)/.test(clean)) return;
      const target = getGlossaryUrlTarget();
      if (!target) {
        if (!wideRef.current) setOpenId(null);
        else if (filteredRef.current[0]?.id) setOpenId(filteredRef.current[0].id);
        return;
      }
      const list = entries || [];
      const want = target.toLocaleLowerCase('tr').trim();
      const found = byId.get(target) || list.find((e) => (e.id || '').toLocaleLowerCase('tr').trim() === want || (e.term || '').toLocaleLowerCase('tr').trim() === want);
      if (found) focusEntry(found.id);
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, [byId, entries, focusEntry]);

  /* ---------------- Yapay zekâ denetimi, paylaşım ---------------- */

  const handleRunAiAudit = useCallback(async (entry: EncyclopediaEntry) => {
    setIsAiAuditing(true);
    setAuditMessage('Yapay zeka tıp müfredatı ve ders notları bağlamında denetim yapıyor...');
    try {
      const prompt = `
Aşağıdaki tıbbi kavramı/hastalığı/ilacı Tıp Fakültesi dönem 3 kurul ders notları (özellikle ${entry.kurul} ${entry.discipline} müfredatı) bağlamında harfiyen denetle ve genişlet.

Kavram: ${entry.term} (${entry.latinName || ''})
Mevcut Tanım: ${entry.definition}
Ders Notu Bağlamı: ${entry.lectureContextNotes}
Morfoloji/Mekanizma: ${entry.morphologyOrMechanism || ''}
Ayırıcı Tanı: ${entry.differentialDiagnosis || ''}

Lütfen bu kavramı fakülte sınavları ve TUS açısından en yüksek verimle denetle ve aşağıdaki geçerli JSON formatında döndür:
{
  "auditSummary": "Yapay zeka denetim özeti ve ders notu uyumluluk doğrulaması",
  "accuracyScore": 99,
  "enhancedDefinition": "Daha net, akademik ve doğru tanım",
  "enhancedMorphology": "Ders slaytlarındaki histopatolojik/farmakolojik kilit noktalar",
  "differentialDiagnosis": "Ayırıcı tanıda en çok karışan hastalık/ilaç ve kesin ayrım kriteri",
  "examSpotPearls": "Komite ve TUS için en kilit soru ipucu",
  "pitfallsAndWarnings": "Sınavda en çok düşülen tuzak veya kontrendikasyon",
  "sampleExamQuestion": "Bu konuyla ilgili komite/TUS tarzı 5 şıklı soru ve cevabı"
}
`;
      const res = await api.callClientResilientAi({
        prompt,
        responseFormat: 'json',
        preferredProvider: 'auto',
        systemInstruction: 'Sen Tıp Fakültesi Patoloji, Farmakoloji ve Mikrobiyoloji anabilim dallarında uzman kıdemli bir tıp akademisyenisin. Ders notu bağlamından asla sapmadan, en doğru tıbbi terminolojiyle JSON döndür.',
      });
      const parsed = JSON.parse(res.text);
      const { _termNorm, _firstLetter, _rank, ...plain } = entry as IndexedEncyclopediaEntry;
      void _termNorm; void _firstLetter;
      const updatedEntry: EncyclopediaEntry = {
        ...plain,
        definition: parsed.enhancedDefinition || entry.definition,
        morphologyOrMechanism: parsed.enhancedMorphology || entry.morphologyOrMechanism,
        differentialDiagnosis: parsed.differentialDiagnosis || entry.differentialDiagnosis,
        examSpotPearls: parsed.examSpotPearls || entry.examSpotPearls,
        pitfallsAndWarnings: parsed.pitfallsAndWarnings || entry.pitfallsAndWarnings,
        aiAudit: {
          verified: true,
          verifiedAt: new Date().toISOString().split('T')[0],
          accuracyScore: parsed.accuracyScore || 100,
          auditSummary: parsed.auditSummary || 'Yapay zeka tarafından başarıyla denetlendi ve güncellendi.',
          sampleExamQuestion: parsed.sampleExamQuestion || entry.aiAudit?.sampleExamQuestion,
        },
      };
      const updatedIndexed = indexEntry(updatedEntry, typeof _rank === 'number' ? _rank : 0);
      setEntries((prev) => (prev ? prev.map((e) => (e.id === entry.id ? updatedIndexed : e)) : prev));
      try {
        const stored = JSON.parse(localStorage.getItem(CUSTOM_KEY) || '{}');
        stored[entry.id] = updatedEntry;
        localStorage.setItem(CUSTOM_KEY, JSON.stringify(stored));
      } catch (err) {
        console.error('LocalStorage write error:', err);
      }
      setAuditMessage('Yapay zeka denetimi tamamlandı! Ders notları ve sınav spotları güncellendi.');
      setTimeout(() => setAuditMessage(null), 4000);
    } catch (err: any) {
      console.error('AI Audit error:', err);
      setAuditMessage(`Denetim sırasında hata oluştu: ${err.message || 'Bilinmeyen hata'}`);
      setTimeout(() => setAuditMessage(null), 5000);
    } finally {
      setIsAiAuditing(false);
    }
  }, []);

  const copyShareLink = useCallback(async (entry: EncyclopediaEntry) => {
    await shareDeepLink({ type: 'term', id: entry.id });
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2000);
  }, []);

  const openEntry = openId ? byId.get(openId) || null : null;
  const renderDetail = (variant: 'inline' | 'pane') =>
    openEntry ? (
      <EntryDetail
        entry={openEntry}
        variant={variant}
        saved={bookmarkedSet.has(openEntry.id)}
        copied={copiedLink}
        auditing={isAiAuditing}
        auditMessage={auditMessage}
        related={related}
        onBookmark={toggleBookmark}
        onShare={copyShareLink}
        onReport={handleOpenReport}
        onAudit={handleRunAiAudit}
        onOpenRelated={focusEntry}
      />
    ) : null;
  const inlineDetail = !wide ? renderDetail('inline') : null;

  /* ---------------- Araç çubuğu ---------------- */

  const segments: ToolbarSegment[] = SEGMENT_IDS
    .map((id) => ({
      id,
      label: id === 'all' ? 'Tümü' : id === 'kart' ? 'Bilgi kartı' : catLabel(id),
      count: entries ? (id === 'all' ? total : id === 'kart' ? cardCount : catCount.get(id) || 0) : undefined,
    }))
    .filter((s) => !entries || s.id === 'all' || (s.count || 0) > 0);

  const categoryOptions = useMemo(
    () => [
      { id: 'all', label: 'Tümü', count: total },
      ...(cardCount ? [{ id: 'kart', label: 'Bilgi kartı', count: cardCount }] : []),
      ...[...catCount.entries()]
        .filter(([id]) => id)
        .sort((a, b) => b[1] - a[1])
        .map(([id, count]) => ({ id, label: catLabel(id), count })),
    ],
    [catCount, cardCount, total],
  );

  const SORT_LABEL: Record<SortMode, string> = { default: 'Önerilen', az: 'A → Z', za: 'Z → A', kurul: 'Kurula göre' };
  const chips: ToolbarChip[] = [];
  if (!SEGMENT_IDS.includes(selectedCategory)) chips.push({ id: 'cat', label: catLabel(selectedCategory), onRemove: () => setSelectedCategory('all') });
  if (selectedKurul !== 'Tümü') chips.push({ id: 'kurul', label: selectedKurul, onRemove: () => setSelectedKurul('Tümü') });
  if (selectedDiscipline !== 'Tümü') chips.push({ id: 'disc', label: selectedDiscipline, onRemove: () => setSelectedDiscipline('Tümü') });
  if (sortMode !== 'default') chips.push({ id: 'sort', label: SORT_LABEL[sortMode], onRemove: () => setSortMode('default') });
  if (onlyAiVerified) chips.push({ id: 'ver', label: 'Doğrulanmış', onRemove: () => setOnlyAiVerified(false) });
  if (onlySaved) chips.push({ id: 'saved', label: 'Kaydedilenler', onRemove: () => setOnlySaved(false) });

  const filtersSheet = (
    <>
      <FilterPills label="Kategori" options={categoryOptions} value={selectedCategory} onChange={setSelectedCategory} />
      <FilterPills
        label="Kurul"
        options={[{ id: 'Tümü', label: 'Tümü' }, ...kurulOptions.map(([k, n]) => ({ id: k, label: k, count: n }))]}
        value={selectedKurul}
        onChange={setSelectedKurul}
      />
      <fieldset className="pt-fgroup">
        <legend>Branş</legend>
        <select value={selectedDiscipline} onChange={(e) => setSelectedDiscipline(e.target.value)} aria-label="Branş">
          <option value="Tümü">Tümü</option>
          {disciplineOptions.map((d) => <option key={d} value={d}>{d}</option>)}
        </select>
      </fieldset>
      <FilterPills<SortMode>
        label="Sırala"
        options={(Object.keys(SORT_LABEL) as SortMode[]).map((id) => ({ id, label: SORT_LABEL[id] }))}
        value={sortMode}
        onChange={setSortMode}
      />
      <fieldset className="pt-fgroup">
        <legend>Durum</legend>
        <div className="pt-pills">
          <button type="button" aria-pressed={onlyAiVerified} className={onlyAiVerified ? 'is-on' : ''} onClick={() => setOnlyAiVerified((v) => !v)}>
            Doğrulanmış
          </button>
          <button type="button" aria-pressed={onlySaved} className={onlySaved ? 'is-on' : ''} onClick={() => setOnlySaved((v) => !v)}>
            Kaydedilenler <span>{bookmarkedIds.length}</span>
          </button>
        </div>
      </fieldset>
    </>
  );

  const isFiltered = filteredEntries.length !== total;
  const countText = !entries
    ? (loadError ? '' : 'yükleniyor…')
    : isFiltered
      ? `${filteredEntries.length.toLocaleString('tr-TR')} / ${total.toLocaleString('tr-TR')}`
      : `${total.toLocaleString('tr-TR')} madde`;

  const showRail = !wide && grouped && !!entries && filteredEntries.length > PAGE;
  const rowSep = (k: string) => (sortMode === 'kurul' ? k.replace(/\s+/g, '-') : k);

  const reportModal = showReportModal && reportingEntry && (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-[var(--color-scrim)] animate-in fade-in duration-200">
      <div className="bg-white border border-line rounded-2xl w-full max-w-lg shadow-xl overflow-hidden flex flex-col max-h-[90vh]">
        <div className="flex items-center justify-between px-6 py-4 border-b border-line bg-canvas">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-warn" />
            <h3 className="font-semibold text-lg text-ink">Terim / Sözlük Hata Bildirimi</h3>
          </div>
          <button
            type="button"
            onClick={() => setShowReportModal(false)}
            className="p-1 rounded-lg hover:bg-canvas text-ink-3 hover:text-ink cursor-pointer transition-colors"
            aria-label="Kapat"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        <form onSubmit={handleReportSubmit} className="p-6 flex flex-col gap-4 overflow-y-auto">
          <div className="p-3 bg-canvas rounded-xl border border-line flex flex-col gap-1">
            <span className="text-xs font-semibold text-ink-2">Bildirilen Terim:</span>
            <span className="font-bold text-ink">{reportingEntry.term}</span>
            {reportingEntry.kurul && <span className="text-xs text-ink-3">{reportingEntry.kurul} · {reportingEntry.discipline}</span>}
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-ink-2 uppercase tracking-wider">Hata Türü</label>
            <select
              value={reportReason}
              onChange={(e) => setReportReason(e.target.value)}
              className="w-full px-3 py-2 text-sm rounded-xl border border-line bg-canvas text-ink focus:border-accent outline-hidden"
            >
              <option value="Tanım / Bilgi hatalı">Tanım / Bilgi hatalı</option>
              <option value="Mekanizma veya patoloji yanlış">Mekanizma veya patoloji yanlış</option>
              <option value="Sınav tuzağı / spot bilgisi eksik veya hatalı">Sınav tuzağı / spot bilgisi eksik veya hatalı</option>
              <option value="Ders notu / slayt uyumsuz">Ders notu / slayt uyumsuz</option>
              <option value="Diğer">Diğer</option>
            </select>
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-ink-2 uppercase tracking-wider">Açıklama *</label>
            <textarea
              rows={3}
              value={reportDetails}
              onChange={(e) => setReportDetails(e.target.value)}
              placeholder="Tespit ettiğiniz eksik veya hatalı kısmı belirtin..."
              required
              className="w-full px-3 py-2 text-sm rounded-xl border border-line bg-canvas text-ink focus:border-accent outline-hidden resize-none"
            />
          </div>
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-ink-2 uppercase tracking-wider">Önerilen Doğru Bilgi / Metin (İsteğe Bağlı)</label>
            <input
              type="text"
              value={reportSuggestedAnswer}
              onChange={(e) => setReportSuggestedAnswer(e.target.value)}
              placeholder="Doğru ifade veya eklenmesini önerdiğiniz bilgi..."
              className="w-full px-3 py-2 text-sm rounded-xl border border-line bg-canvas text-ink focus:border-accent outline-hidden"
            />
          </div>
          <div className="flex items-center justify-end gap-3 pt-3 border-t border-line">
            <button
              type="button"
              onClick={() => setShowReportModal(false)}
              className="px-4 py-2 text-sm font-semibold rounded-xl text-ink-2 hover:bg-canvas cursor-pointer transition-colors"
            >
              Vazgeç
            </button>
            <button
              type="submit"
              disabled={isSubmittingReport}
              className="px-5 py-2 text-sm font-semibold rounded-xl bg-accent text-white hover:bg-accent-hover disabled:opacity-50 cursor-pointer flex items-center gap-2 transition-colors"
            >
              <Send className="w-4 h-4" />
              {isSubmittingReport ? 'Gönderiliyor...' : 'Bildirimi Gönder'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  if (v12) {
    return (
      <>
        <GlossaryV12
          entries={entries}
          loadError={loadError}
          onReload={() => setReloadKey((n) => n + 1)}
          total={total}
          filteredCount={filteredEntries.length}
          visibleCount={visible.length}
          groups={groups}
          hasMore={hasMore}
          setSentinel={setSentinel}
          grouped={grouped}
          groupDomId={(k) => `gz-h-${rowSep(k)}`}
          alphabet={V12_ALPHABET}
          letterSet={letterSet}
          onJumpLetter={jumpToLetter}
          searchQuery={searchQuery}
          onSearch={setSearchQuery}
          filters={filtersSheet}
          chips={chips}
          onClearChips={() => {
            if (!SEGMENT_IDS.includes(selectedCategory)) setSelectedCategory('all');
            setSelectedKurul('Tümü');
            setSelectedDiscipline('Tümü');
            setSortMode('default');
            setOnlyAiVerified(false);
            setOnlySaved(false);
          }}
          onResetFilters={resetFilters}
          openEntry={openEntry}
          wide={wide}
          onSelect={selectEntry}
          onClose={closeEntry}
          saved={bookmarkedSet}
          onBookmark={toggleBookmark}
          onShare={copyShareLink}
          copied={copiedLink}
          onReport={handleOpenReport}
          onAudit={handleRunAiAudit}
          auditing={isAiAuditing}
          auditMessage={auditMessage}
          related={related}
          onOpenRelated={focusEntry}
          catLabel={catLabel}
        />
        {reportModal}
      </>
    );
  }

  return (
    <div className="ds-page gz-page">
      <PageToolbar
        title="Sözlük"
        count={countText}
        search={{ value: searchQuery, onChange: setSearchQuery, placeholder: 'Terim, ilaç, bulgu ara' }}
        segments={{ options: segments, value: selectedCategory, onChange: setSelectedCategory, label: 'Kategori' }}
        filters={filtersSheet}
        filterCount={chips.length}
        filterTitle="Sözlük süzgeci"
        chips={chips}
        onClearChips={() => {
          if (!SEGMENT_IDS.includes(selectedCategory)) setSelectedCategory('all');
          setSelectedKurul('Tümü');
          setSelectedDiscipline('Tümü');
          setSortMode('default');
          setOnlyAiVerified(false);
          setOnlySaved(false);
        }}
      />

      {loadError ? (
        <div className="ds-empty is-panel">
          <b>Sözlük yüklenemedi</b>
          <span>Bağlantını kontrol edip yeniden dene.</span>
          <button type="button" className="ms-btn is-tonal is-sm" onClick={() => setReloadKey((n) => n + 1)}>Yeniden dene</button>
        </div>
      ) : entries && filteredEntries.length === 0 ? (
        <div className="ds-empty is-panel">
          <EmptySearch size={64} />
          <b>Eşleşen madde yok</b>
          <span>Farklı bir terim dene ya da süzgeçleri temizle.</span>
          <button type="button" onClick={resetFilters} className="ms-btn is-tonal is-sm">Tüm maddeleri göster</button>
        </div>
      ) : (
        <div className={`gz ${wide ? 'is-wide' : ''}`}>
          <div className={`gz-list ${showRail ? 'has-rail' : ''}`} aria-busy={!entries}>
            {!entries ? (
              <ul className="gz-ul" aria-label="Yükleniyor">
                {Array.from({ length: 12 }, (_, i) => <SkeletonRow key={i} i={i} />)}
              </ul>
            ) : (
              groups.map((g, gi) => {
                const last = gi === groups.length - 1;
                return (
                  <section key={`${g.key}-${gi}`} className="gz-group" aria-label={g.key || undefined}>
                    {g.key && <h3 className="gz-h" id={`gz-h-${rowSep(g.key)}`}>{g.key}</h3>}
                    <ul className="gz-ul">
                      {g.items.map((entry) => {
                        const open = openId === entry.id;
                        return (
                          <GlossaryRow
                            key={entry.id}
                            entry={entry}
                            open={open}
                            saved={bookmarkedSet.has(entry.id)}
                            inline={!wide}
                            onToggle={onToggle}
                            detail={open ? inlineDetail : null}
                          />
                        );
                      })}
                      {last && hasMore && [0, 1, 2].map((i) => (
                        <SkeletonRow key={`sk${i}`} i={i} ref={i === 0 ? setSentinel : undefined} />
                      ))}
                    </ul>
                  </section>
                );
              })
            )}
            {entries && (
              <p className="gz-foot" aria-live="polite">
                {hasMore
                  ? `${visible.length.toLocaleString('tr-TR')} / ${filteredEntries.length.toLocaleString('tr-TR')} · kaydırdıkça 40’ar yüklenir`
                  : `${filteredEntries.length.toLocaleString('tr-TR')} maddenin tümü gösteriliyor`}
              </p>
            )}
          </div>

          {wide && (
            <aside className="gz-aside" aria-label="Madde ayrıntısı">
              {openEntry ? renderDetail('pane') : (
                <div className="gz-placeholder">
                  <BookOpenText aria-hidden />
                  <b>{entries ? 'Bir madde seç' : 'Sözlük yükleniyor'}</b>
                  <span>Tanım, ders notu, ayırıcı tanı ve sınav spotları burada açılır.</span>
                </div>
              )}
            </aside>
          )}
        </div>
      )}

      {showRail && <LetterRail letters={letterSet} onJump={jumpToLetter} />}

      {reportModal}
    </div>
  );
};
