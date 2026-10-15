import React, { useState, useMemo, useEffect, useRef, useCallback, memo, useDeferredValue } from 'react';
import {
  BookOpenText,
  Activity,
  Heart,
  Bookmark,
  Share2,
  Copy,
  Plus,
  ChevronRight,
  ChevronLeft,
  Stethoscope,
  Pill,
  Sparkles,
  ExternalLink,
  Edit2,
  Trash2,
  Zap,
  Flag,
  Microscope,
  ScanLine,
  FlaskConical,
  TriangleAlert,
  Users,
  Info,
  Tags,
  Library,
  ShieldCheck,
  Play,
  Star,
  GraduationCap,
} from 'lucide-react';
import { PageToolbar, FilterPills, QuickOptions, type ToolbarChip, type ToolbarQuick } from '../ui/PageToolbar';
import type { DiseaseFact, DiseaseKind, DiseaseProfile, DiseaseSectionId } from '../../types/disease';
import { DiseaseService } from '../../services/diseaseService';
import {
  DISEASE_CATEGORIES, ENTITY_TYPE_LABEL, KIND_LABEL, SECTION_ORDER, buildEntityIndex, diseaseSearchText, entityKey, factPlain,
  lineToFact, plainText, sectionFacts, sectionTitle,
} from '../../services/diseaseModel';
import { shareDeepLink, triggerDomHighlightAndScroll } from '../../services/universalRedirectService';
import { toast } from '../ui/Toast';
import { Sheet } from '../ui/Sheet';
import { AppUser, ADMIN_EMAIL } from '../../services/auth';
import { safeJsonFetch } from '../../services/api';
import { pathFor, writeLocation } from '../../router';
import { foldText } from '../../services/searchText';
import { useAppearance } from '../../utils/appearance';
import { ConceptsCard, RelatedDiseasesCard, WhereCard, linkedQuestionCount, useDiseaseInsights } from './DiseaseInsights';
import { lessonFlagText, lessonSelOn, topicMatches, useDiseaseLessons, type LessonSel } from './diseaseLessons';
import { DiseasesV12 } from '../v12/DiseasesV12';
import './diseasesAtlas.css';

/**
 * Hastalıklar atlası (v10 kompakt).
 *  - Liste: ortak PageToolbar (başlık · sayaç · arama · tür segmenti · Süzgeç sayfasında uzmanlık/favori) + kompakt satırlar;
 *    470 profil kaydırdıkça 40'ar çizilir.
 *  - Ayrıntı: konum yolu, büyük başlık + tek satır tanım, Kaydet / "Soruları çöz · n", bölüm sekmeleri;
 *    Özet sekmesinde bölümler iki sütunlu kompakt kartlar + "Sınav spotu" kutusu; sağ panelde ilişkili tablolar,
 *    geçtiği yerler (deste, çıkmış, örnek, ders notu), kavramlar ve kaynaklar.
 *  - Ders programı süzgeci (Kurul ▾ · Ders ▾ · Konu ▾ hızlı hapları): profilin adı o konunun ders özeti, kazanımı,
 *    çıkmış sorusu ya da başlığında geçiyorsa listelenir (veri: diseaseLessons.ts → disease_lessons.json).
 *  - Görüntüleme modu "Odak" ve ≥1024 px: liste + ayrıntı yan yana; diğer modlarda ayrıntı ayrı sayfa (?id=, geri tuşu çalışır).
 * Sınıf öneki `hx-` (diseasesAtlas.css); madde biçimleri `dz-` (rebuild.css) paylaşılır.
 */

interface DiseasesViewProps {
  currentUser?: AppUser | null;
  onOpenReportModal?: (target: { type: string; id: string; title: string }) => void;
  /** Aramadan gelen hastalık: açılınca ayrıntı sayfası açılır */
  initialDiseaseId?: string;
}

/** Bölüm başına ikon ve vurgu tonu (başlık türe göre diseaseModel.sectionTitle'dan gelir) */

// Katlanmış (Türkçe duyarsız) ad ve tam arama metni profil nesnesi başına bir kez hesaplanır: her tuşta
// ya da sayfaya her dönüşte 470+ profilin tüm maddeleri yeniden katlanmasın. Düzenlenen profil yeni nesnedir.
const foldedNameCache = new WeakMap<object, string>();
const foldedTextCache = new WeakMap<object, string>();
function foldedName(d: DiseaseProfile): string {
  let v = foldedNameCache.get(d);
  if (v === undefined) foldedNameCache.set(d, (v = foldText(`${d.name} ${d.latinName || ''} ${d.icd_code || ''} ${(d.altNames || []).join(' ')}`)));
  return v;
}
function foldedSearchText(d: DiseaseProfile): string {
  let v = foldedTextCache.get(d);
  if (v === undefined) foldedTextCache.set(d, (v = foldText(diseaseSearchText(d))));
  return v;
}

const SECTION_META: Record<DiseaseSectionId, { icon: React.ElementType; tone: string }> = {
  definition: { icon: Info, tone: 'accent' },
  etiology: { icon: Activity, tone: 'ai' },
  physiology: { icon: Heart, tone: 'clinic' },
  pathology: { icon: Microscope, tone: 'bad' },
  symptoms: { icon: Stethoscope, tone: 'accent' },
  pathognomonic: { icon: Zap, tone: 'warn' },
  diagnosis: { icon: FlaskConical, tone: 'clinic' },
  imaging: { icon: ScanLine, tone: 'clinic' },
  treatment: { icon: Pill, tone: 'ok' },
  complications: { icon: TriangleAlert, tone: 'bad' },
  epidemiology: { icon: Users, tone: 'ai' },
  lecture: { icon: Sparkles, tone: 'ai' },
};

/** Hastalık kaydında sekme etiketleri kısa; diğer türlerde türün kendi bölüm başlığı kullanılır */
const SHORT_TAB: Record<DiseaseSectionId, string> = {
  definition: 'Tanım', etiology: 'Etiyoloji', physiology: 'Patogenez', pathology: 'Morfoloji', symptoms: 'Klinik',
  pathognomonic: 'Ayırıcı tanı', diagnosis: 'Tanı', imaging: 'Görüntüleme', treatment: 'Tedavi', complications: 'Komplikasyon',
  epidemiology: 'Epidemiyoloji', lecture: 'Ders notu',
};
const tabLabel = (d: DiseaseProfile, sec: DiseaseSectionId) => (d.kind === 'hastalik' ? SHORT_TAB[sec] : sectionTitle(d.kind, sec) || SHORT_TAB[sec]);

/** Özet sekmesinde kart başına gösterilen madde sayısı (fazlası bölüm sekmesinde) */
const CARD_LIMIT = 4;

type DetailTab = 'ozet' | DiseaseSectionId | 'siniflama';

/** ==terim== → fosforlu kalem vurgusu */
const FactText: React.FC<{ text: string }> = ({ text }) => {
  const parts = String(text || '').split(/==([^=]+)==/g);
  return <>{parts.map((p, i) => (i % 2 ? <mark key={i} className="dz-hl">{p}</mark> : <React.Fragment key={i}>{p}</React.Fragment>))}</>;
};

const factsToLines = (facts: DiseaseFact[] | undefined) => (facts || []).map((f) => (f.label ? `${f.label}: ${f.text}` : f.text)).join('\n');

/** Formdaki satırlar → maddeler; metni değişmeyen satır eski maddeyi (varlık etiketleriyle) korur */
function linesToFacts(str: string, prev: DiseaseFact[] | undefined): DiseaseFact[] {
  const old = new Map((prev || []).map((f) => [(f.label ? `${f.label}: ${f.text}` : f.text).trim(), f]));
  return str.split('\n').map((s) => s.trim()).filter(Boolean).map((line) => old.get(line) || lineToFact(line));
}

const FORM_KEYS: Array<DiseaseSectionId | 'hallmarks'> = ['hallmarks', ...SECTION_ORDER];

function useMedia(q: string) {
  const [on, setOn] = useState(() => typeof window !== 'undefined' && !!window.matchMedia?.(q).matches);
  useEffect(() => {
    const m = window.matchMedia?.(q);
    if (!m) return;
    const f = () => setOn(m.matches);
    f();
    m.addEventListener('change', f);
    return () => m.removeEventListener('change', f);
  }, [q]);
  return on;
}

const urlId = () => {
  try { return new URLSearchParams(window.location.search).get('id'); } catch { return null; }
};
/** Adreste profil var mı (?id= ya da /hastaliklar/<kimlik>) */
const urlHasDisease = () => {
  try { return Boolean(urlId()) || !/^\/hastaliklar\/?$/.test(window.location.pathname.replace(/^\/meds(?=\/|$)/, '')); } catch { return false; }
};

export const DiseasesView: React.FC<DiseasesViewProps> = ({
  currentUser,
  onOpenReportModal,
  initialDiseaseId,
}) => {
  const isAdmin = currentUser?.email === ADMIN_EMAIL || Boolean((currentUser as any)?.isMasterAdmin);
  const [diseases, setDiseases] = useState<DiseaseProfile[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedKind, setSelectedKind] = useState<DiseaseKind | 'all'>('all');
  const [entityFilter, setEntityFilter] = useState<string | null>(null);
  const [onlyFavorites, setOnlyFavorites] = useState(false);
  const [lessonSel, setLessonSel] = useState<LessonSel>({});
  const lessonData = useDiseaseLessons();
  const [selectedDisease, setSelectedDisease] = useState<DiseaseProfile | null>(null);
  const [favoriteIds, setFavoriteIds] = useState<Set<string>>(new Set());
  const [tab, setTab] = useState<DetailTab>('ozet');

  // Görüntüleme modu: Odak + geniş ekran → liste ve ayrıntı yan yana
  const { layout, design } = useAppearance();
  const v12 = design === 'v12';
  const isWide = useMedia('(min-width: 1024px)');
  // v12: geniş ekranda her zaman liste + ayrıntı (DiseasesV12)
  const split = isWide && (v12 || layout === 'odak');
  const rootRef = useRef<HTMLDivElement>(null);

  // Ekleme / Düzenleme
  const [showAddEditModal, setShowAddEditModal] = useState(false);
  const [editingDisease, setEditingDisease] = useState<DiseaseProfile | null>(null);
  const [formName, setFormName] = useState('');
  const [formLatinName, setFormLatinName] = useState('');
  const [formIcdCode, setFormIcdCode] = useState('');
  const [formCategory, setFormCategory] = useState<string>('Genel Patoloji');
  const [formKind, setFormKind] = useState<DiseaseKind>('hastalik');
  const [formSecs, setFormSecs] = useState<Record<string, string>>({});
  const setFormSec = (k: string, v: string | ((cur: string) => string)) =>
    setFormSecs((s) => ({ ...s, [k]: typeof v === 'function' ? v(s[k] || '') : v }));

  const reloadDiseases = () => {
    setDiseases(DiseaseService.getAllDiseases());
    setFavoriteIds(DiseaseService.getFavoriteIds());
  };

  const [dataReady, setDataReady] = useState(DiseaseService.isLoaded());
  useEffect(() => {
    let alive = true;
    DiseaseService.load().then(() => { if (alive) { reloadDiseases(); setDataReady(true); } });
    window.addEventListener('medsoru:diseases-changed', reloadDiseases);
    return () => { alive = false; window.removeEventListener('medsoru:diseases-changed', reloadDiseases); };
  }, []);

  /** Kimlik ya da birleştirilmiş eski kimlik */
  const findById = useCallback(
    (id: string) => diseases.find((d) => d.id === id) || diseases.find((d) => (d.aliases || []).includes(id)),
    [diseases],
  );

  // URL derin bağlantısı (/hastaliklar?id=… ya da #disease-<kimlik>[-bölüm])
  const handledPropRef = useRef<string | null>(null);
  useEffect(() => {
    if (typeof window === 'undefined' || !diseases.length) return;
    const params = new URLSearchParams(window.location.search);
    const hash = window.location.hash;
    let target: DiseaseProfile | undefined;
    // Uygulamadan gelen kimlik yalnız ilk kez (ya da değişince) uygulanır; sonra adres çubuğu esastır
    const fromProp = initialDiseaseId && initialDiseaseId !== handledPropRef.current ? initialDiseaseId : null;
    if (initialDiseaseId) handledPropRef.current = initialDiseaseId;
    const direct = params.get('id') || fromProp;
    if (direct) target = findById(direct);
    if (!target && hash.startsWith('#disease-')) {
      // Kimlikler tire içerir: önce tam kimlik, sonra bölüm son eki atılarak denenir
      const parts = decodeURIComponent(hash.slice('#disease-'.length)).split('-');
      for (let k = parts.length; k >= 1 && !target; k--) target = findById(parts.slice(0, k).join('-'));
    }
    if (target) {
      setSelectedDisease(target);
      setTab('ozet');
      const t = target;
      setTimeout(() => triggerDomHighlightAndScroll(hash || `disease-${t.id}`), 300);
    }
  }, [diseases, initialDiseaseId]);

  // Geri / ileri: adresteki ?id= ayrıntıyı açar ya da kapatır
  useEffect(() => {
    const onPop = () => {
      if (!/\/hastaliklar\/?$/.test(window.location.pathname.replace(/^\/meds(?=\/|$)/, ''))) return;
      const id = urlId();
      if (!id) { setSelectedDisease(null); return; }
      const d = findById(id);
      if (d) { setSelectedDisease(d); setTab('ozet'); }
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, [findById]);

  // Sorgu zekâsı: yazım hatası / eşanlamlı / kısaltma ("kansizlik", "ttp") → hastalık kimlikleri
  const [conceptIds, setConceptIds] = useState<string[]>([]);
  useEffect(() => {
    const q = searchQuery.trim();
    if (q.length < 3) { setConceptIds([]); return; }
    const ctrl = new AbortController();
    const t = window.setTimeout(async () => {
      const r = await safeJsonFetch<{ success: boolean; corrected: string | null; concepts: Array<{ ref: { kind: string; id: string } | null }> }>(
        `/api/search/understand?q=${encodeURIComponent(q)}`, { signal: ctrl.signal });
      if (ctrl.signal.aborted || !r.ok || !r.data?.success) return;
      setConceptIds(r.data.concepts.filter((c) => c.ref?.kind === 'disease').map((c) => c.ref!.id));
    }, 160);
    return () => { ctrl.abort(); window.clearTimeout(t); };
  }, [searchQuery]);

  // Arama ve süzme ertelenmiş sorguyla çalışır: yazarken giriş kutusu bekletilmez
  const deferredQuery = useDeferredValue(searchQuery);
  const foldedQuery = useMemo(() => foldText(deferredQuery.trim()), [deferredQuery]);

  // Varlık dizini: "belirti:ateş" → geçtiği profiller (sınıflandırma süzgeci). Açılışta değil, ilk gerektiğinde
  // (en az 3 harflik arama ya da varlık süzgeci) bir kez kurulur.
  const needEntities = Boolean(entityFilter) || foldedQuery.length >= 3;
  const entityIndex = useMemo(
    () => (needEntities ? buildEntityIndex(diseases) : new Map<string, { entity: { name: string; type: any }; hits: { diseaseId: string; section: any }[] }>()),
    [diseases, needEntities],
  ) as ReturnType<typeof buildEntityIndex>;
  const entityFolded = useMemo(() => {
    const m = new Map<string, string>();
    for (const [k, row] of entityIndex) m.set(k, foldText(row.entity.name));
    return m;
  }, [entityIndex]);
  const activeEntity = entityFilter ? entityIndex.get(entityFilter) : undefined;
  const entityIds = useMemo(() => new Set(activeEntity?.hits.map((h) => h.diseaseId) || []), [activeEntity]);

  /** Aranan sözcük bir varlık adıysa ("ateş") sınıflandırma önerisi */
  const entitySuggestions = useMemo(() => {
    const q = foldedQuery;
    if (q.length < 3 || entityFilter) return [];
    const out: Array<{ key: string; label: string; n: number }> = [];
    for (const [key, row] of entityIndex) {
      if (entityFolded.get(key) !== q) continue;
      const n = new Set(row.hits.map((h) => h.diseaseId)).size;
      if (n >= 2) out.push({ key, label: `${ENTITY_TYPE_LABEL[row.entity.type]}: ${row.entity.name}`, n });
    }
    return out.sort((a, b) => b.n - a.n).slice(0, 4);
  }, [foldedQuery, entityIndex, entityFolded, entityFilter]);


  const categories = useMemo(() => {
    const present = new Set(diseases.map((d) => d.category).filter(Boolean));
    const ordered = DISEASE_CATEGORIES.filter((c) => present.has(c));
    const extra = [...present].filter((c) => !(DISEASE_CATEGORIES as readonly string[]).includes(c)).sort((a, b) => a.localeCompare(b, 'tr'));
    return ['all', ...ordered, ...extra];
  }, [diseases]);
  const kinds = useMemo(() => {
    const present = new Set(diseases.map((d) => d.kind));
    return (Object.keys(KIND_LABEL) as DiseaseKind[]).filter((k) => present.has(k));
  }, [diseases]);

  // Ders programı süzgeci: seçime uyan konularda geçen profiller (en güçlü konu + toplam geçiş)
  const lessonOn = lessonSelOn(lessonSel);
  const lessonMatch = useMemo(() => {
    const out = new Map<string, { n: number; flags: number; best: number; bestN: number }>();
    if (!lessonData || !lessonOn) return out;
    for (const [id, rows] of Object.entries(lessonData.hastaliklar)) {
      for (const [ti, n, f] of rows) {
        if (!topicMatches(lessonData.konular[ti], ti, lessonSel)) continue;
        const cur = out.get(id);
        if (!cur) out.set(id, { n, flags: f, best: ti, bestN: n });
        else { cur.n += n; cur.flags |= f; if (n > cur.bestN) { cur.best = ti; cur.bestN = n; } }
      }
    }
    return out;
  }, [lessonData, lessonOn, lessonSel]);

  /** Seçenek sayıları: her kurul / ders / konuda geçen (yüklü) profil sayısı */
  const lessonCounts = useMemo(() => {
    const kurul = new Map<number, Set<string>>();
    const ders = new Map<string, Set<string>>();
    const konu = new Map<number, number>();
    const all = new Set<string>();
    if (!lessonData) return { kurul, ders, konu, all };
    const present = new Set(diseases.map((d) => d.id));
    for (const [id, rows] of Object.entries(lessonData.hastaliklar)) {
      if (!present.has(id)) continue;
      all.add(id);
      for (const [ti] of rows) {
        const x = lessonData.konular[ti];
        const dk = `${x.k}|${x.d}`;
        if (!kurul.has(x.k)) kurul.set(x.k, new Set());
        kurul.get(x.k)!.add(id);
        if (!ders.has(dk)) ders.set(dk, new Set());
        ders.get(dk)!.add(id);
        konu.set(ti, (konu.get(ti) || 0) + 1);
      }
    }
    return { kurul, ders, konu, all };
  }, [lessonData, diseases]);

  // Süzme: Türkçe karakter/büyük-küçük harf duyarsız; ad eşleşmesi ve sorgu zekâsının tanıdığı hastalıklar öne
  const filteredDiseases = useMemo(() => {
    const terms = foldedQuery.split(/\s+/).filter((t) => t.length >= 2);
    const pinned = new Set(conceptIds);
    const scored: Array<{ d: DiseaseProfile; s: number }> = [];
    for (const d of diseases) {
      if (onlyFavorites && !favoriteIds.has(d.id)) continue;
      if (selectedCategory !== 'all' && d.category !== selectedCategory) continue;
      if (selectedKind !== 'all' && d.kind !== selectedKind) continue;
      if (activeEntity && !entityIds.has(d.id)) continue;
      if (lessonOn && !lessonMatch.has(d.id)) continue;
      if (!terms.length) { scored.push({ d, s: lessonOn ? lessonMatch.get(d.id)!.n : 0 }); continue; }
      const name = foldedName(d);
      let s = 0;
      if (pinned.has(d.id)) s += 100;
      if (terms.every((t) => name.includes(t))) s += 50 + (name.startsWith(terms[0]) ? 10 : 0);
      else { const txt = foldedSearchText(d); if (terms.every((t) => txt.includes(t))) s += 10; }
      if (s > 0) scored.push({ d, s });
    }
    // Ders süzgecinde konuda en çok geçen profiller öne gelir
    if (terms.length || lessonOn) scored.sort((a, b) => b.s - a.s || a.d.name.localeCompare(b.d.name, 'tr'));
    else scored.sort((a, b) => a.d.name.localeCompare(b.d.name, 'tr'));
    return scored.map((x) => x.d);
  }, [diseases, foldedQuery, selectedCategory, selectedKind, onlyFavorites, favoriteIds, conceptIds, activeEntity, entityIds, lessonOn, lessonMatch]);

  // Kaydırdıkça yükleme: ilk 40 satır, alt uca yaklaşınca 40'ar eklenir (470 kaydın tek seferde çizilmesi donma yapıyordu)
  const PAGE = 40;
  const [limit, setLimit] = useState(PAGE);
  useEffect(() => { setLimit(PAGE); }, [searchQuery, selectedCategory, selectedKind, onlyFavorites, entityFilter, lessonSel]);
  const [sentinel, setSentinel] = useState<HTMLDivElement | null>(null);
  useEffect(() => {
    if (!sentinel || typeof IntersectionObserver === 'undefined') return;
    const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) setLimit((n) => n + PAGE); }, { rootMargin: '600px 0px' });
    io.observe(sentinel);
    return () => io.disconnect();
  }, [sentinel, limit, filteredDiseases.length]);

  // Üst çubuğun yüksekliği: bölmeli düzende ayrıntı bölmesi bunun altına yapışır
  useEffect(() => {
    const root = rootRef.current;
    const bar = root?.querySelector('.pt-root') as HTMLElement | null;
    if (!root || !bar || typeof ResizeObserver === 'undefined') return;
    const ro = new ResizeObserver(() => root.style.setProperty('--hx-bar', `${Math.round(bar.getBoundingClientRect().height)}px`));
    ro.observe(bar);
    return () => ro.disconnect();
  }, [dataReady, selectedDisease == null, split]);

  /* ---------------- Ayrıntıyı açma / kapama (adres çubuğuyla eş) ---------------- */
  const pushedRef = useRef(false);
  const lastOpenRef = useRef<string | null>(null);

  const openDisease = useCallback((d: DiseaseProfile) => {
    setSelectedDisease(d);
    setTab('ozet');
    lastOpenRef.current = d.id;
    try {
      if (urlId() !== d.id) {
        const next = `${pathFor('diseases')}?id=${encodeURIComponent(d.id)}`;
        // Bölmeli düzende her seçim yeni geçmiş kaydı açmaz; ayrı sayfada geri tuşu listeye döner
        if (split || urlId()) window.history.replaceState(window.history.state, '', next);
        else { window.history.pushState({ route: 'diseases' }, '', next); pushedRef.current = true; }
      }
    } catch { /* adres yazılamadıysa yalnız durum */ }
    if (!split) requestAnimationFrame(() => window.scrollTo({ top: 0 }));
    else requestAnimationFrame(() => document.querySelector('.hx-pane')?.scrollTo({ top: 0 }));
  }, [split]);

  const closeDisease = useCallback(() => {
    const id = selectedDisease?.id || lastOpenRef.current;
    setSelectedDisease(null);
    try {
      if (urlHasDisease()) {
        if (pushedRef.current && urlId()) { pushedRef.current = false; window.history.back(); }
        else window.history.replaceState(window.history.state, '', pathFor('diseases'));
      }
    } catch { /* yoksay */ }
    // Listeye dönünce açılan satır görünür olsun
    if (id) requestAnimationFrame(() => document.getElementById(`hx-item-${id}`)?.scrollIntoView({ block: 'center' }));
  }, [selectedDisease]);

  const openById = useCallback((id: string) => { const d = findById(id); if (d) openDisease(d); }, [findById, openDisease]);

  const handleToggleFavorite = useCallback((id: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    const isNow = DiseaseService.toggleFavorite(id);
    setFavoriteIds(DiseaseService.getFavoriteIds());
    if (isNow) toast.success('Kaydedildi', 'Profil favorilere eklendi.');
    else toast.info('Kayıttan çıkarıldı', 'Profil favorilerden kaldırıldı.');
  }, []);

  const handleShare = useCallback(async (disease: DiseaseProfile, section?: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    await shareDeepLink({
      type: 'disease',
      id: disease.id,
      title: `${disease.name} · MeDSor Hastalıklar`,
      subTarget: section,
      highlightText: disease.name,
    });
  }, []);

  const handleCopySummary = (disease: DiseaseProfile, e?: React.MouseEvent) => {
    e?.stopPropagation();
    const lines = [
      `${disease.name}${disease.latinName ? ` (${disease.latinName})` : ''}`,
      disease.icd_code ? `ICD-10: ${disease.icd_code}` : '',
      `${KIND_LABEL[disease.kind]} · ${disease.category}`,
    ];
    if (disease.hallmarks.length) lines.push('', 'Karakteristik özellik:', ...disease.hallmarks.map((f) => `• ${factPlain(f)}`));
    for (const sec of SECTION_ORDER) {
      const title = sectionTitle(disease.kind, sec);
      const facts = sectionFacts(disease, sec);
      if (!title || !facts.length) continue;
      lines.push('', `${title}:`, ...facts.map((f) => `• ${factPlain(f)}`));
    }
    lines.push('', `MeDSor: ${window.location.origin}/hastaliklar?id=${disease.id}`);
    navigator.clipboard.writeText(lines.filter((l, i) => l || lines[i - 1]).join('\n'));
    toast.success('Kopyalandı', 'Profil özeti panoya kopyalandı.');
  };

  const handleOpenEdit = (disease: DiseaseProfile, e?: React.MouseEvent) => {
    e?.stopPropagation();
    setEditingDisease(disease);
    setFormName(disease.name);
    setFormLatinName(disease.latinName || '');
    setFormIcdCode(disease.icd_code || '');
    setFormCategory(disease.category);
    setFormKind(disease.kind);
    const secs: Record<string, string> = { hallmarks: factsToLines(disease.hallmarks) };
    for (const sec of SECTION_ORDER) secs[sec] = factsToLines(disease.sections[sec]);
    setFormSecs(secs);
    setShowAddEditModal(true);
  };

  const handleOpenAdd = () => {
    setEditingDisease(null);
    setFormName('');
    setFormLatinName('');
    setFormIcdCode('');
    setFormCategory('Genel Patoloji');
    setFormKind('hastalik');
    setFormSecs({});
    setShowAddEditModal(true);
  };

  const handleSaveForm = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formName.trim()) {
      toast.error('Eksik bilgi', 'Lütfen adı girin.');
      return;
    }
    const slug = editingDisease?.id || formName.trim().toLocaleLowerCase('tr-TR')
      .replace(/ğ/g, 'g').replace(/ü/g, 'u').replace(/ş/g, 's')
      .replace(/ı/g, 'i').replace(/ö/g, 'o').replace(/ç/g, 'c')
      .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    const sections: DiseaseProfile['sections'] = {};
    for (const sec of SECTION_ORDER) {
      const facts = linesToFacts(formSecs[sec] || '', editingDisease?.sections[sec]);
      if (facts.length) sections[sec] = facts;
    }
    const now = new Date().toISOString();
    const profile: DiseaseProfile = {
      ...(editingDisease || {}),
      id: slug,
      name: formName.trim(),
      latinName: formLatinName.trim() || undefined,
      icd_code: formIcdCode.trim() || null,
      kind: formKind,
      category: formCategory.trim() || 'Genel Patoloji',
      hallmarks: linesToFacts(formSecs.hallmarks || '', editingDisease?.hallmarks),
      sections,
      schemaVersion: 2,
      isCustom: true,
      createdBy: editingDisease?.createdBy || currentUser?.displayName || currentUser?.email || 'Öğrenci',
      createdAt: editingDisease?.createdAt || now,
      updatedAt: now,
    };
    DiseaseService.saveDisease(profile);
    reloadDiseases();
    setShowAddEditModal(false);
    if (selectedDisease?.id === profile.id) setSelectedDisease(profile);
    toast.success('Kaydedildi', editingDisease ? 'Profil güncellendi.' : 'Yeni profil eklendi.');
  };

  const handleDelete = (id: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    if (!window.confirm('Bu kaydı silmek istediğine emin misin?')) return;
    DiseaseService.deleteDisease(id);
    reloadDiseases();
    if (selectedDisease?.id === id) closeDisease();
    toast.info('Silindi', 'Kayıt silindi.');
  };

  const applyEntity = (key: string) => {
    setEntityFilter(key);
    if (!split) closeDisease();
    setSearchQuery('');
    setSelectedCategory('all');
    setSelectedKind('all');
  };

  const goSearch = (q: string) => { writeLocation('search', q); window.dispatchEvent(new PopStateEvent('popstate')); };

  const sel = selectedDisease;
  const { data: insights, loading: insightsLoading } = useDiseaseInsights(sel);
  const canEdit = Boolean(sel && (isAdmin || sel.isCustom));
  const counts = useMemo(() => {
    const cat = new Map<string, number>(); const kind = new Map<string, number>();
    for (const d of diseases) { cat.set(d.category, (cat.get(d.category) || 0) + 1); kind.set(d.kind, (kind.get(d.kind) || 0) + 1); }
    return { cat, kind };
  }, [diseases]);
  const catCount = (c: string) => (c === 'all' ? diseases.length : counts.cat.get(c) || 0);

  /** Seçili profilin varlıkları türlerine göre (sınıflandırma sekmesi) */
  const selEntities = useMemo(() => {
    if (!sel) return [];
    const groups = new Map<string, Array<{ key: string; name: string; n: number }>>();
    const seen = new Set<string>();
    const facts = [...sel.hallmarks, ...SECTION_ORDER.flatMap((s) => sectionFacts(sel, s))];
    for (const f of facts) for (const en of f.entities || []) {
      const key = entityKey(en);
      if (seen.has(key)) continue;
      seen.add(key);
      const row = entityIndex.get(key);
      const n = row ? new Set(row.hits.map((h) => h.diseaseId)).size : 1;
      if (!groups.has(en.type)) groups.set(en.type, []);
      groups.get(en.type)!.push({ key, name: row?.entity.name || en.name, n });
    }
    const order = Object.keys(ENTITY_TYPE_LABEL);
    return [...groups.entries()]
      .sort((a, b) => order.indexOf(a[0]) - order.indexOf(b[0]))
      .map(([type, items]) => ({ type, items: items.sort((a, b) => b.n - a.n) }));
  }, [sel, entityIndex]);

  const field = (label: string, value: string, set: (v: string) => void, opts: { area?: boolean; required?: boolean; ph?: string; hint?: string; rows?: number } = {}) => (
    <label className="dz-field" key={label}>
      <span>{label}{opts.required && <b aria-hidden> *</b>}{opts.hint && <small>{opts.hint}</small>}</span>
      {opts.area ? (
        <textarea rows={opts.rows || 3} value={value} onChange={(e) => set(e.target.value)} placeholder={opts.ph} />
      ) : (
        <input type="text" value={value} required={opts.required} onChange={(e) => set(e.target.value)} placeholder={opts.ph} />
      )}
    </label>
  );

  const filtersOn = Boolean(searchQuery || selectedCategory !== 'all' || selectedKind !== 'all' || onlyFavorites || entityFilter || lessonOn);
  const clearFilters = () => { setSearchQuery(''); setSelectedCategory('all'); setSelectedKind('all'); setOnlyFavorites(false); setEntityFilter(null); setLessonSel({}); };

  /** Profil ayrıntısından "bu konudakileri göster": süzgeci kurar, ayrı sayfa düzeninde listeye döner */
  const applyLesson = (sel: LessonSel) => {
    setLessonSel(sel);
    setSearchQuery('');
    setEntityFilter(null);
    if (!split) closeDisease();
  };

  /* Ders programı hızlı hapları: Kurul ▾ · Ders ▾ (aranabilir, kurula göre gruplu) · Konu ▾ (ders seçilince) */
  const lessonQuick: ToolbarQuick[] = [];
  if (lessonData) {
    const kName = (k: number) => lessonData.kurullar.find((x) => x.k === k)?.ad || '';
    const dersOpts = [...lessonCounts.ders.entries()]
      .map(([key, set]) => { const [k, d] = key.split('|'); return { key, k: Number(k), d, n: set.size }; })
      .filter((x) => lessonSel.k == null || x.k === lessonSel.k)
      .sort((a, b) => a.k - b.k || a.d.localeCompare(b.d, 'tr'));
    const konuOpts = lessonSel.d != null
      ? lessonData.konular.map((x, i) => ({ x, i })).filter(({ x, i }) => x.k === lessonSel.k && x.d === lessonSel.d && lessonCounts.konu.has(i))
      : [];
    const short = (t: string, n = 26) => (t.length > n ? `${t.slice(0, n - 1)}…` : t);
    lessonQuick.push({
      id: 'kurul',
      label: 'Kurul',
      value: lessonSel.k != null ? `Kurul ${lessonSel.k}` : undefined,
      onClear: () => setLessonSel({}),
      content: (close) => (
        <QuickOptions
          close={close}
          value={lessonSel.k != null ? String(lessonSel.k) : 'all'}
          onPick={(id) => setLessonSel(id === 'all' ? {} : { k: Number(id) })}
          options={[
            { id: 'all', label: 'Tüm kurullar', count: lessonCounts.all.size },
            ...lessonData.kurullar.filter((k) => lessonCounts.kurul.has(k.k)).map((k) => ({
              id: String(k.k), label: `Kurul ${k.k}`, hint: k.ad, count: lessonCounts.kurul.get(k.k)!.size,
            })),
          ]}
        />
      ),
    });
    lessonQuick.push({
      id: 'ders',
      label: 'Ders',
      wide: true,
      value: lessonSel.d != null ? short(lessonSel.d, 22) : undefined,
      onClear: () => setLessonSel((s) => ({ k: s.k })),
      content: (close) => (
        <QuickOptions
          close={close}
          searchable
          placeholder="Ders ara"
          value={lessonSel.d != null ? `${lessonSel.k}|${lessonSel.d}` : 'all'}
          onPick={(id) => {
            if (id === 'all') { setLessonSel((s) => ({ k: s.k })); return; }
            const [k, d] = id.split('|');
            setLessonSel({ k: Number(k), d });
          }}
          options={[
            { id: 'all', label: lessonSel.k != null ? `Kurul ${lessonSel.k} · tüm dersler` : 'Tüm dersler', count: lessonSel.k != null ? lessonCounts.kurul.get(lessonSel.k)?.size : lessonCounts.all.size },
            ...dersOpts.map((x) => ({ id: x.key, label: x.d, count: x.n, group: lessonSel.k == null ? `Kurul ${x.k} · ${kName(x.k)}` : undefined })),
          ]}
        />
      ),
    });
    if (lessonSel.d != null) {
      const cur = lessonSel.t != null ? lessonData.konular[lessonSel.t] : null;
      lessonQuick.push({
        id: 'konu',
        label: 'Konu',
        wide: true,
        value: cur ? short(cur.t) : undefined,
        onClear: () => setLessonSel((s) => ({ k: s.k, d: s.d })),
        content: (close) => (
          <QuickOptions
            close={close}
            searchable={konuOpts.length > 8}
            placeholder="Konu ara"
            value={lessonSel.t != null ? String(lessonSel.t) : 'all'}
            onPick={(id) => setLessonSel((s) => ({ k: s.k, d: s.d, ...(id === 'all' ? {} : { t: Number(id) }) }))}
            options={[
              { id: 'all', label: `${lessonSel.d} · tüm konular`, count: lessonCounts.ders.get(`${lessonSel.k}|${lessonSel.d}`)?.size },
              ...konuOpts.map(({ x, i }) => ({ id: String(i), label: x.t, count: lessonCounts.konu.get(i) || 0 })),
            ]}
          />
        ),
      });
    }
  }

  /** Seçili profilin ders programındaki yerleri (ayrıntı yan paneli) */
  const selLessons = useMemo(() => {
    if (!sel || !lessonData) return [];
    return (lessonData.hastaliklar[sel.id] || []).map(([ti, n, f]) => ({ ti, n, f, x: lessonData.konular[ti] }));
  }, [sel, lessonData]);

  const chips: ToolbarChip[] = [
    ...(selectedCategory !== 'all' ? [{ id: 'cat', label: selectedCategory, onRemove: () => setSelectedCategory('all') }] : []),
    ...(onlyFavorites ? [{ id: 'fav', label: 'Kaydedilenler', onRemove: () => setOnlyFavorites(false) }] : []),
    ...(activeEntity ? [{ id: 'ent', label: `${ENTITY_TYPE_LABEL[activeEntity.entity.type]}: ${activeEntity.entity.name}`, onRemove: () => setEntityFilter(null) }] : []),
  ];

  /** Ayrı sayfa düzeninde ayrıntı açıkken liste ve araç çubuğu gizlenir (konum yolundan dönülür) */
  const detailPage = Boolean(sel) && !split;

  /** Satırdaki eşleşme nedeni: varlık süzgeci ya da ders programı konusu ("başlık|metin") */
  const hitLabelOf = (d: DiseaseProfile): string | undefined => {
    const hit = activeEntity?.hits.find((h) => h.diseaseId === d.id);
    const lm = lessonOn && !hit ? lessonMatch.get(d.id) : undefined;
    const lessonLabel = lm && lessonData
      ? `${lessonSel.t != null ? 'Bu konuda' : lessonData.konular[lm.best].t}|${lm.n} kez · ${lessonFlagText(lm.flags)}`
      : undefined;
    return hit && activeEntity ? `${sectionTitle(d.kind, hit.section as DiseaseSectionId) || 'Karakteristik özellik'}|${activeEntity.entity.name}${hit.qualifier ? ` (${hit.qualifier})` : ''}` : lessonLabel;
  };

  const list = (
    <div className="hx-listwrap">
      {!dataReady ? (
        <ul className="hx-list" aria-busy="true" aria-label="Profiller yükleniyor">
          {Array.from({ length: 8 }, (_, i) => (
            <li key={i} className="hx-item is-skel">
              <span className="ui-skel" style={{ width: 110, height: 10 }} />
              <span className="ui-skel" style={{ width: `${50 + ((i * 17) % 40)}%`, height: 15 }} />
              <span className="ui-skel" style={{ width: '85%', height: 10 }} />
            </li>
          ))}
        </ul>
      ) : filteredDiseases.length === 0 ? (
        <div className="hx-empty">
          <span className="hx-empty-ic" aria-hidden><BookOpenText /></span>
          <b>Eşleşen kayıt yok</b>
          <p>Aramayı kısalt ya da süzgeçleri kaldır.</p>
          {filtersOn && <button type="button" className="ui-btn is-tonal is-sm" onClick={clearFilters}>Süzgeçleri temizle</button>}
        </div>
      ) : (
        <>
          <ul className="hx-list" data-layout-grid={split ? undefined : ''}>
            {filteredDiseases.slice(0, limit).map((d) => (
              <DiseaseRow key={d.id} d={d} isFav={favoriteIds.has(d.id)} active={sel?.id === d.id} onOpen={openDisease} onFav={handleToggleFavorite}
                hitLabel={hitLabelOf(d)} />
            ))}
          </ul>
          {filteredDiseases.length > limit && <div ref={setSentinel} className="hx-more-sentinel" aria-hidden><span className="ui-skel" /></div>}
        </>
      )}
    </div>
  );

  const editSheet = (
    <Sheet
      open={showAddEditModal}
      onClose={() => setShowAddEditModal(false)}
      title={editingDisease ? 'Profili düzenle' : 'Yeni profil'}
      subtitle='Her satır bir madde olarak kaydedilir. "Etiket: açıklama" yazarsan etiket kalın görünür; ==terim== vurgulanır.'
      width={680}
    >
      <form onSubmit={handleSaveForm} className="dz-form">
        <div className="dz-form-2">
          {field('Ad', formName, setFormName, { required: true, ph: 'Örn. Akut apandisit' })}
          {field('Latince / İngilizce adı', formLatinName, setFormLatinName, { ph: 'Örn. Acute appendicitis' })}
          {field('ICD-10 kodu', formIcdCode, setFormIcdCode, { ph: 'Örn. K35' })}
          <label className="dz-field">
            <span>Tür</span>
            <select value={formKind} onChange={(e) => setFormKind(e.target.value as DiseaseKind)}>
              {(Object.keys(KIND_LABEL) as DiseaseKind[]).map((k) => <option key={k} value={k}>{KIND_LABEL[k]}</option>)}
            </select>
          </label>
          <label className="dz-field">
            <span>Uzmanlık</span>
            <select value={formCategory} onChange={(e) => setFormCategory(e.target.value)}>
              {[...DISEASE_CATEGORIES, ...(DISEASE_CATEGORIES as readonly string[]).includes(formCategory) ? [] : [formCategory]].map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </label>
        </div>
        {FORM_KEYS.map((k) => {
          const title = k === 'hallmarks' ? 'Karakteristik özellik' : sectionTitle(formKind, k);
          if (!title) return null;
          return field(title, formSecs[k] || '', (v) => setFormSec(k, v), {
            area: true,
            rows: k === 'hallmarks' ? 2 : 3,
            hint: k === 'hallmarks' ? 'Tek bakışta tanıtan bulgu (ör. Çilek serviks)' : undefined,
          });
        })}
        <div className="dz-form-f">
          <button type="button" className="ui-btn is-ghost" onClick={() => setShowAddEditModal(false)}>Vazgeç</button>
          <button type="submit" className="ui-btn is-primary">{editingDisease ? 'Kaydet' : 'Ekle'}</button>
        </div>
      </form>
    </Sheet>
  );

  if (v12) {
    return (
      <>
        <DiseasesV12
          dataReady={dataReady}
          total={diseases.length}
          filtered={filteredDiseases}
          limit={limit}
          setLimit={setLimit}
          setSentinel={setSentinel}
          alphabetical={!searchQuery.trim() && !lessonOn}
          searchQuery={searchQuery}
          onSearchQuery={setSearchQuery}
          filters={(
            <>
              {kinds.length > 1 && (
                <FilterPills<DiseaseKind | 'all'>
                  label="Kayıt türü"
                  value={selectedKind}
                  onChange={setSelectedKind}
                  options={[{ id: 'all' as const, label: 'Tümü', count: diseases.length }, ...kinds.map((k) => ({ id: k, label: KIND_LABEL[k], count: counts.kind.get(k) || 0 }))]}
                />
              )}
              <FilterPills
                label="Uzmanlık / sistem"
                value={selectedCategory}
                onChange={setSelectedCategory}
                options={categories.map((c) => ({ id: c, label: c === 'all' ? 'Tümü' : c, count: catCount(c) }))}
              />
              <FilterPills
                label="Göster"
                value={onlyFavorites ? 'fav' : 'all'}
                onChange={(v) => setOnlyFavorites(v === 'fav')}
                options={[{ id: 'all', label: 'Tüm profiller' }, { id: 'fav', label: 'Kaydedilenler', count: favoriteIds.size }]}
              />
            </>
          )}
          filterCount={(selectedKind !== 'all' ? 1 : 0) + (selectedCategory !== 'all' ? 1 : 0) + (onlyFavorites ? 1 : 0)}
          chips={[
            ...(selectedKind !== 'all' ? [{ id: 'kind', label: KIND_LABEL[selectedKind], onRemove: () => setSelectedKind('all') }] : []),
            ...chips,
          ]}
          onClearChips={() => { setSelectedKind('all'); setSelectedCategory('all'); setOnlyFavorites(false); setEntityFilter(null); }}
          filtersOn={filtersOn}
          onClearFilters={clearFilters}
          quick={lessonQuick}
          notices={(lessonOn && lessonData) || entitySuggestions.length > 0 ? (
            <div className="g12-notices">
              {lessonOn && lessonData && (
                <p className="g12-notice" role="status">
                  <GraduationCap aria-hidden />
                  <span>
                    {lessonSel.t != null
                      ? <>Bu konunun ders özeti, kazanımları ya da çıkmış sorularında adı geçen profiller; en çok geçen üstte.</>
                      : <>Seçili {lessonSel.d != null ? 'dersin' : 'kurulun'} konularında adı geçen profiller; satırda en çok geçtiği konu yazar.</>}
                    {' '}<button type="button" onClick={() => setLessonSel({})}>Kaldır</button>
                  </span>
                </p>
              )}
              {entitySuggestions.length > 0 && (
                <div className="g12-notice" role="status">
                  <Tags aria-hidden />
                  <span>Sınıflandır:</span>
                  {entitySuggestions.map((sg) => (
                    <button key={sg.key} type="button" className="g12-pill" onClick={() => applyEntity(sg.key)}>
                      <span>{sg.label}</span><b className="g12-num">{sg.n}</b>
                    </button>
                  ))}
                </div>
              )}
            </div>
          ) : undefined}
          onAdd={handleOpenAdd}
          hitLabelOf={hitLabelOf}
          sel={sel}
          split={split}
          favoriteIds={favoriteIds}
          onOpen={openDisease}
          onFav={handleToggleFavorite}
          onClose={closeDisease}
          insights={insights}
          insightsLoading={insightsLoading}
          entities={selEntities}
          canEdit={canEdit}
          onShare={handleShare}
          onCopy={() => sel && handleCopySummary(sel)}
          onEdit={() => sel && handleOpenEdit(sel)}
          onDelete={sel?.isCustom ? () => handleDelete(sel.id) : undefined}
          onOpenDisease={openById}
          canOpen={(id) => Boolean(findById(id))}
          onEntity={applyEntity}
          onSearch={goSearch}
          onReport={onOpenReportModal && sel ? () => onOpenReportModal({ type: 'disease', id: sel.id, title: sel.name }) : undefined}
          lessons={selLessons}
          onLesson={applyLesson}
        />
        {editSheet}
      </>
    );
  }

  return (
    <div className={`hx-page ${split ? 'is-split' : ''}`} ref={rootRef}>
      {!detailPage && (
        <PageToolbar
          title="Hastalıklar"
          count={dataReady ? (filtersOn ? `${filteredDiseases.length.toLocaleString('tr-TR')} / ${diseases.length.toLocaleString('tr-TR')} profil` : `${diseases.length.toLocaleString('tr-TR')} profil`) : undefined}
          search={{ value: searchQuery, onChange: setSearchQuery, placeholder: 'Hastalık, belirti, ilaç, gen ara' }}
          segments={kinds.length > 1 ? {
            label: 'Kayıt türü',
            value: selectedKind,
            onChange: (v) => setSelectedKind(v),
            options: [{ id: 'all' as const, label: 'Tümü', count: diseases.length }, ...kinds.map((k) => ({ id: k, label: KIND_LABEL[k], count: counts.kind.get(k) || 0 }))],
          } : undefined}
          filters={(
            <>
              <FilterPills
                label="Uzmanlık / sistem"
                value={selectedCategory}
                onChange={setSelectedCategory}
                options={categories.map((c) => ({ id: c, label: c === 'all' ? 'Tümü' : c, count: catCount(c) }))}
              />
              <FilterPills
                label="Göster"
                value={onlyFavorites ? 'fav' : 'all'}
                onChange={(v) => setOnlyFavorites(v === 'fav')}
                options={[{ id: 'all', label: 'Tüm profiller' }, { id: 'fav', label: 'Kaydedilenler', count: favoriteIds.size }]}
              />
            </>
          )}
          filterCount={(selectedCategory !== 'all' ? 1 : 0) + (onlyFavorites ? 1 : 0)}
          filterTitle="Hastalık süzgeci"
          chips={chips}
          onClearChips={() => { setSelectedCategory('all'); setOnlyFavorites(false); setEntityFilter(null); }}
          quick={lessonQuick.length ? lessonQuick : undefined}
          tools={(
            <button type="button" className="ui-btn is-primary is-sm hx-add" onClick={handleOpenAdd} aria-label="Profil ekle">
              <Plus aria-hidden /> <span>Profil ekle</span>
            </button>
          )}
        >
          {lessonOn && lessonData && (
            <p className="hx-lessonnote" role="status">
              <GraduationCap aria-hidden />
              <span>
                {lessonSel.t != null
                  ? <>Bu konunun ders özeti, kazanımları ya da çıkmış sorularında adı geçen profiller; en çok geçen üstte.</>
                  : <>Seçili {lessonSel.d != null ? 'dersin' : 'kurulun'} konularında adı geçen profiller; satırda en çok geçtiği konu yazar.</>}
                {' '}<button type="button" onClick={() => setLessonSel({})}>Kaldır</button>
              </span>
            </p>
          )}
          {entitySuggestions.length > 0 && (
            <div className="hx-entbar" role="status">
              <span className="hx-entbar-h">Sınıflandır:</span>
              {entitySuggestions.map((s) => (
                <button key={s.key} type="button" className="dz-entchip" onClick={() => applyEntity(s.key)}>
                  <Tags aria-hidden /><span>{s.label} <small>{s.n} profil</small></span>
                </button>
              ))}
            </div>
          )}
        </PageToolbar>
      )}

      {split ? (
        <div className="hx-split">
          <div className="hx-split-list">{list}</div>
          <div className="hx-pane">
            {sel ? (
              <DiseaseDetail
                d={sel} split tab={tab} setTab={setTab} isFav={favoriteIds.has(sel.id)} canEdit={canEdit}
                insights={insights} insightsLoading={insightsLoading} entities={selEntities}
                onClose={closeDisease} onFav={() => handleToggleFavorite(sel.id)} onShare={handleShare} onCopy={() => handleCopySummary(sel)}
                onEdit={() => handleOpenEdit(sel)} onDelete={sel.isCustom ? () => handleDelete(sel.id) : undefined}
                onOpenDisease={openById} canOpen={(id) => Boolean(findById(id))} onEntity={applyEntity} onSearch={goSearch}
                onReport={onOpenReportModal ? () => onOpenReportModal({ type: 'disease', id: sel.id, title: sel.name }) : undefined}
                lessons={selLessons} onLesson={applyLesson}
              />
            ) : (
              <div className="hx-pane-empty">
                <BookOpenText aria-hidden />
                <b>Bir profil seç</b>
                <p>Soldaki listeden bir hastalığa dokun; tanımdan tedaviye bölümleri burada açılır.</p>
              </div>
            )}
          </div>
        </div>
      ) : sel ? (
        <DiseaseDetail
          d={sel} split={false} tab={tab} setTab={setTab} isFav={favoriteIds.has(sel.id)} canEdit={canEdit}
          insights={insights} insightsLoading={insightsLoading} entities={selEntities}
          onClose={closeDisease} onFav={() => handleToggleFavorite(sel.id)} onShare={handleShare} onCopy={() => handleCopySummary(sel)}
          onEdit={() => handleOpenEdit(sel)} onDelete={sel.isCustom ? () => handleDelete(sel.id) : undefined}
          onOpenDisease={openById} canOpen={(id) => Boolean(findById(id))} onEntity={applyEntity} onSearch={goSearch}
          onReport={onOpenReportModal ? () => onOpenReportModal({ type: 'disease', id: sel.id, title: sel.name }) : undefined}
          lessons={selLessons} onLesson={applyLesson}
        />
      ) : list}

      {editSheet}
    </div>
  );
};

/* ================================================================================================
 * Ayrıntı
 * ============================================================================================== */

interface DetailProps {
  d: DiseaseProfile;
  split: boolean;
  tab: DetailTab;
  setTab: (t: DetailTab) => void;
  isFav: boolean;
  canEdit: boolean;
  insights: ReturnType<typeof useDiseaseInsights>['data'];
  insightsLoading: boolean;
  entities: Array<{ type: string; items: Array<{ key: string; name: string; n: number }> }>;
  onClose: () => void;
  onFav: () => void;
  onShare: (d: DiseaseProfile, sec?: string) => void;
  onCopy: () => void;
  onEdit: () => void;
  onDelete?: () => void;
  onOpenDisease: (id: string) => void;
  canOpen: (id: string) => boolean;
  onEntity: (key: string) => void;
  onSearch: (q: string) => void;
  onReport?: () => void;
  lessons: Array<{ ti: number; n: number; f: number; x: { k: number; d: string; t: string } }>;
  onLesson: (sel: LessonSel) => void;
}

const DiseaseDetail: React.FC<DetailProps> = ({
  d, split, tab, setTab, isFav, canEdit, insights, insightsLoading, entities,
  onClose, onFav, onShare, onCopy, onEdit, onDelete, onOpenDisease, canOpen, onEntity, onSearch, onReport, lessons, onLesson,
}) => {
  const [allLessons, setAllLessons] = useState(false);
  useEffect(() => { setAllLessons(false); }, [d.id]);
  const defFacts = sectionFacts(d, 'definition');
  const def = defFacts[0];
  const secs = SECTION_ORDER.filter((s) => sectionTitle(d.kind, s) && sectionFacts(d, s).length > 0);
  const tabs: Array<{ id: DetailTab; label: string; n?: number }> = [
    { id: 'ozet', label: 'Özet' },
    ...secs.map((s) => ({ id: s as DetailTab, label: tabLabel(d, s), n: sectionFacts(d, s).length })),
    ...(entities.length ? [{ id: 'siniflama' as DetailTab, label: 'Sınıflandırma' }] : []),
  ];
  const active: DetailTab = tabs.some((t) => t.id === tab) ? tab : 'ozet';
  // Sınav spotu: kritik (key) işaretli maddelerden ilk üçü
  const spots = useMemo(() => SECTION_ORDER.flatMap((s) => sectionFacts(d, s).filter((f) => f.key)).slice(0, 3), [d]);
  const qCount = linkedQuestionCount(insights);
  const plainName = d.name.replace(/\s*\([^)]*\)/g, '');
  const H = split ? 'h2' : 'h1';
  const tabsRef = useRef<HTMLDivElement>(null);

  // Sekme klavye gezintisi (ok tuşları)
  const onTabKey = (e: React.KeyboardEvent) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const i = tabs.findIndex((t) => t.id === active);
    const n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
    setTab(n.id);
    requestAnimationFrame(() => tabsRef.current?.querySelector<HTMLButtonElement>(`[data-tab="${n.id}"]`)?.focus());
    e.preventDefault();
  };

  return (
    <article className="hx-detail" id={`disease-${d.id}`} aria-labelledby={`hx-title-${d.id}`}>
      <header className="hx-dh">
        <nav className="hx-crumb" aria-label="Konum">
          <button type="button" onClick={onClose}>
            {!split && <ChevronLeft aria-hidden />}Hastalıklar
          </button>
          <span aria-hidden>›</span>
          <span className="hx-crumb-cat">{d.category}</span>
        </nav>
        <div className="hx-dh-row">
          <div className="hx-dh-main">
            <H id={`hx-title-${d.id}`} className="hx-dh-title">{d.name}</H>
            {def && <p className="hx-dh-def">{plainText(def.text)}</p>}
            <p className="hx-dh-meta">
              <span className="hx-kind">{KIND_LABEL[d.kind]}</span>
              {d.icd_code && <span className="hx-icd">ICD-10 {d.icd_code}</span>}
              {d.latinName && d.latinName !== d.name && <span className="hx-latin">{d.latinName}</span>}
            </p>
          </div>
          <div className="hx-dh-acts">
            <button type="button" className={`ui-btn is-sm ${isFav ? 'is-tonal' : 'is-ghost'} hx-save`} aria-pressed={isFav} onClick={onFav}>
              <Bookmark className={isFav ? 'fill-current' : ''} aria-hidden /> {isFav ? 'Kaydedildi' : 'Kaydet'}
            </button>
            {qCount > 0 && (
              <button type="button" className="ui-btn is-primary is-sm" onClick={() => onSearch(plainName)}>
                <Play aria-hidden /> Soruları çöz · {qCount.toLocaleString('tr-TR')}
              </button>
            )}
            <span className="hx-dh-icons">
              <button type="button" className="qk-ib" onClick={() => onShare(d)} aria-label="Paylaş" title="Paylaş"><Share2 aria-hidden /></button>
              <button type="button" className="qk-ib" onClick={onCopy} aria-label="Özeti kopyala" title="Özeti kopyala"><Copy aria-hidden /></button>
              {canEdit && <button type="button" className="qk-ib" onClick={onEdit} aria-label="Düzenle" title="Düzenle"><Edit2 aria-hidden /></button>}
              {canEdit && onDelete && <button type="button" className="qk-ib hx-del" onClick={onDelete} aria-label="Sil" title="Sil"><Trash2 aria-hidden /></button>}
            </span>
          </div>
        </div>
        {d.hallmarks.length > 0 && (
          <div className="hx-hall" id={`disease-${d.id}-hallmarks`} aria-label="Karakteristik özellik">
            <span className="hx-hall-h">Karakteristik</span>
            {d.hallmarks.map((h, k) => <mark key={k} className="dz-hall is-sm"><span>{plainText(h.text)}</span></mark>)}
          </div>
        )}
        <div className="hx-tabs" role="tablist" aria-label="Profil bölümleri" ref={tabsRef} onKeyDown={onTabKey}>
          {tabs.map((t) => (
            <button
              key={t.id}
              type="button"
              role="tab"
              data-tab={t.id}
              id={`hx-tab-${d.id}-${t.id}`}
              aria-selected={active === t.id}
              aria-controls={`hx-panel-${d.id}`}
              tabIndex={active === t.id ? 0 : -1}
              className={active === t.id ? 'is-on' : ''}
              onClick={() => setTab(t.id)}
            >
              {t.label}
            </button>
          ))}
        </div>
      </header>

      <div className="hx-dbody">
        <div className="hx-dmain" role="tabpanel" id={`hx-panel-${d.id}`} aria-labelledby={`hx-tab-${d.id}-${active}`}>
          {active === 'ozet' ? (
            <div className="hx-grid bento is-duo is-rhythm">
              {secs.map((sec) => {
                // Tanımın ilk maddesi başlıkta; kartta yalnız kalanlar
                const facts = sec === 'definition' ? defFacts.slice(1) : sectionFacts(d, sec);
                if (!facts.length) return null;
                return <SectionCard key={sec} d={d} sec={sec} facts={facts} limit={CARD_LIMIT} onMore={() => setTab(sec)} onShare={onShare} />;
              })}
              {spots.length > 0 && (
                <aside className="hx-spot bt-full" aria-label="Sınav spotu">
                  <p className="hx-spot-h"><Star aria-hidden /> Sınav spotu</p>
                  <ul>
                    {spots.map((f, k) => <li key={k}>{f.label && <b>{f.label}: </b>}<FactText text={f.text} /></li>)}
                  </ul>
                </aside>
              )}
            </div>
          ) : active === 'siniflama' ? (
            <section className="hx-card hx-sec is-wide" aria-label="Sınıflandırma">
              <p className="hx-ent-intro">Bir öğeye dokun: aynı belirti, ilaç, gen ya da bulguyu içeren tüm profiller listelenir.</p>
              {entities.map((g) => (
                <div key={g.type} className="hx-entgroup">
                  <h3 className="hx-sec-h">{ENTITY_TYPE_LABEL[g.type as keyof typeof ENTITY_TYPE_LABEL]}</h3>
                  <div className="dz-chips hx-chips">
                    {g.items.map((it) => (
                      <button key={it.key} type="button" className="dz-chip" disabled={it.n < 2} onClick={() => onEntity(it.key)}
                        title={it.n >= 2 ? `${it.name} geçen ${it.n} profili listele` : 'Yalnız bu profilde geçiyor'}>
                        {it.name}{it.n >= 2 && <em>{it.n}</em>}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </section>
          ) : (
            <SectionCard d={d} sec={active} facts={sectionFacts(d, active)} wide onShare={onShare} />
          )}
        </div>

        <aside className="hx-aside" aria-label="Bağlantılar">
          {d.verification && (
            <p className="dz-verif">
              <ShieldCheck aria-hidden />
              <span><b>Web kaynaklarıyla madde madde doğrulandı</b> · {d.verification.checked} madde denetlendi
                {d.verification.fixed + d.verification.conflict > 0 ? `, ${d.verification.fixed + d.verification.conflict} düzeltildi` : ''}
                {` · ${new Date(d.verification.at).toLocaleDateString('tr-TR')}`}</span>
            </p>
          )}
          <RelatedDiseasesCard data={insights} loading={insightsLoading} onOpenDisease={onOpenDisease} canOpen={canOpen} />
          {lessons.length > 0 && (
            <section className="hx-card hx-aside-card" aria-labelledby={`hx-prog-${d.id}`}>
              <h2 id={`hx-prog-${d.id}`} className="hx-aside-h"><GraduationCap aria-hidden /> Ders programında</h2>
              <ul className="hx-prog">
                {(allLessons ? lessons : lessons.slice(0, 5)).map((l) => (
                  <li key={l.ti}>
                    <button type="button" onClick={() => onLesson({ k: l.x.k, d: l.x.d, t: l.ti })} title="Bu konuda geçen tüm profilleri listele">
                      <span className="hx-prog-t">{l.x.t}</span>
                      <span className="hx-prog-s">Kurul {l.x.k} · {l.x.d}</span>
                      <span className="hx-prog-s">{l.n} kez · {lessonFlagText(l.f)}</span>
                    </button>
                  </li>
                ))}
              </ul>
              {lessons.length > 5 && (
                <button type="button" className="hx-aside-link" onClick={() => setAllLessons((v) => !v)}>
                  {allLessons ? 'Daha az göster' : `${lessons.length - 5} konu daha`}
                </button>
              )}
            </section>
          )}
          <WhereCard data={insights} loading={insightsLoading} lectures={d.relatedLectures} onSearch={() => onSearch(plainName)} />
          <ConceptsCard data={insights} onSearch={onSearch} />
          {(d.references || []).length > 0 && (
            <section className="hx-card hx-aside-card" aria-labelledby={`hx-refs-${d.id}`} id={`disease-${d.id}-references`}>
              <h2 id={`hx-refs-${d.id}`} className="hx-aside-h"><Library aria-hidden /> Kaynaklar</h2>
              <ol className="hx-refs">
                {(d.references || []).map((r, k) => (
                  <li key={k} id={`disease-${d.id}-ref-${k}`}>
                    {r.url ? <a href={r.url} target="_blank" rel="noreferrer">{r.label} <ExternalLink aria-hidden /></a> : r.label}
                  </li>
                ))}
              </ol>
            </section>
          )}
          {onReport && (
            <button type="button" className="ui-btn is-ghost is-sm hx-report" onClick={onReport}>
              <Flag aria-hidden /> Bu profilde hata bildir
            </button>
          )}
        </aside>
      </div>
    </article>
  );
};

/** Bölüm kartı: başlık (türe göre) + madde listesi; Özet'te ilk `limit` madde, fazlası bölüm sekmesinde */
const SectionCard = memo(function SectionCard({ d, sec, facts, limit, wide, onMore, onShare }: {
  d: DiseaseProfile; sec: DiseaseSectionId; facts: DiseaseFact[]; limit?: number; wide?: boolean; onMore?: () => void; onShare: (d: DiseaseProfile, sec?: string) => void;
}) {
  const title = sectionTitle(d.kind, sec);
  if (!title || !facts.length) return null;
  const { tone } = SECTION_META[sec];
  const shown = limit ? facts.slice(0, limit) : facts;
  const rest = facts.length - shown.length;
  return (
    <section id={`disease-${d.id}-${sec}`} className={`hx-card hx-sec is-${tone} ${wide ? 'is-wide' : ''}`} aria-labelledby={`hx-sec-${d.id}-${sec}`}>
      <header className="hx-sec-top">
        <h3 id={`hx-sec-${d.id}-${sec}`} className="hx-sec-h">{title}</h3>
        <button type="button" className="hx-sec-link" onClick={() => onShare(d, sec)} aria-label={`${title} bölümünün bağlantısını paylaş`} title="Bu bölümün bağlantısını paylaş">
          <Share2 aria-hidden />
        </button>
      </header>
      <ul className="dz-list hx-list-facts">{shown.map((f, k) => <FactItem key={k} f={f} d={d} />)}</ul>
      {rest > 0 && onMore && (
        <button type="button" className="hx-sec-more" onClick={onMore}>
          {rest} madde daha <ChevronRight aria-hidden />
        </button>
      )}
    </section>
  );
});

/** Ders notu dosya adını okunur başlığa çevirir ("D4_D5_hiper_hipo_tiroid_260427_085228.md (Kurul 6)" → "hiper hipo tiroid (Kurul 6)") */
function lectureLabel(src: string): string {
  return src.replace(/_/g, ' ').replace(/\.md\b/g, '').replace(/\b\d{6}\b/g, '').replace(/\b[A-Z]\d+\b/g, '')
    .replace(/^\s*\d+\s/, '').replace(/\s{2,}/g, ' ').trim();
}

/** Tek madde: etiket kalın, ==vurgu== fosforlu, kaynak numaraları tıklanabilir */
const FactItem = memo(function FactItem({ f, d }: { f: DiseaseFact; d: DiseaseProfile }) {
  return (
    <li className={f.key ? 'is-key' : undefined}>
      {f.label && <b className="dz-lab">{f.label}</b>}
      {f.text && <FactText text={f.text} />}
      {f.key && <span className="dz-keytag" title="Sınavda sorulan kritik bilgi">Sınav</span>}
      {(f.refs || []).map((r) => (
        <a key={r} className="dz-ref" href={`#disease-${d.id}-ref-${r}`} title={d.references?.[r]?.label}
          onClick={(e) => { e.preventDefault(); document.getElementById(`disease-${d.id}-ref-${r}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' }); }}>[{r + 1}]</a>
      ))}
      {f.items && f.items.length > 0 && <ul className="dz-sublist">{f.items.map((it, k) => <li key={k}><FactText text={it} /></li>)}</ul>}
      {f.source && <small className="dz-fsrc">Ders notunda da var · {lectureLabel(f.source)}</small>}
    </li>
  );
});

/** Liste satırı: yalnız kendi verisi değişince yeniden çizilir */
const DiseaseRow = memo(function DiseaseRow({ d, isFav, active, hitLabel, onOpen, onFav }: {
  d: DiseaseProfile; isFav: boolean; active: boolean; hitLabel?: string; onOpen: (d: DiseaseProfile) => void; onFav: (id: string, e?: React.MouseEvent) => void;
}) {
  const def = sectionFacts(d, 'definition')[0];
  const [hitTitle, hitText] = hitLabel ? hitLabel.split('|') : [];
  const hall = d.hallmarks[0];
  return (
    <li id={`hx-item-${d.id}`} className={`hx-item ${active ? 'is-on' : ''}`} data-tone={toneOf(d.category)}>
      <button type="button" className="hx-item-main" onClick={() => onOpen(d)} aria-current={active ? 'true' : undefined}>
        <span className="hx-item-top">
          <span className="hx-cat"><i aria-hidden />{d.category}</span>
          {d.kind !== 'hastalik' && <span className="hx-kind">{KIND_LABEL[d.kind]}</span>}
          {d.icd_code && <span className="hx-icd">{d.icd_code}</span>}
        </span>
        <span className="hx-item-name">{d.name}</span>
        {hitTitle
          ? <span className="hx-item-def"><b>{hitTitle}</b> {hitText}</span>
          : def ? <span className="hx-item-def">{plainText(def.text)}</span>
            : hall ? <span className="hx-item-def">{plainText(hall.text)}</span> : null}
      </button>
      <button type="button" className={`qk-ib hx-item-fav ${isFav ? 'is-fav' : ''}`} aria-pressed={isFav} onClick={(e) => { e.stopPropagation(); onFav(d.id, e); }} aria-label={isFav ? 'Kayıttan çıkar' : 'Kaydet'} title={isFav ? 'Kayıttan çıkar' : 'Kaydet'}>
        <Bookmark className={isFav ? 'fill-current' : ''} aria-hidden />
      </button>
    </li>
  );
});

/** Uzmanlığa göre sabit vurgu tonu (yalnız DS tokenları): aynı uzmanlık her yerde aynı renkte. */
const TONES = ['accent', 'clinic', 'ai', 'warn', 'ok', 'bad'] as const;
function toneOf(cat: string) {
  let h = 0;
  for (const ch of String(cat || '')) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return TONES[h % TONES.length];
}
