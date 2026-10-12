import React, { useState, useMemo, useEffect, useRef, useCallback, memo } from 'react';
import {
  Search,
  BookOpenText,
  Activity,
  Heart,
  Bookmark,
  Share2,
  Copy,
  Plus,
  ChevronRight,
  Stethoscope,
  Pill,
  Sparkles,
  ExternalLink,
  Edit2,
  Trash2,
  X,
  Zap,
  Flag,
  Highlighter,
  Microscope,
  ScanLine,
  FlaskConical,
  TriangleAlert,
  Users,
  Info,
  Tags,
  Library,
  ShieldCheck,
} from 'lucide-react';
import { PageHeader } from '../ui/PageHeader';
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
import { writeLocation } from '../../router';
import { foldText } from '../../services/searchText';
import { RelatedPanel, useDiseaseInsights } from './DiseaseInsights';

interface DiseasesViewProps {
  currentUser?: AppUser | null;
  onOpenReportModal?: (target: { type: string; id: string; title: string }) => void;
  /** Aramadan gelen hastalık: açılınca ayrıntı sayfası açılır */
  initialDiseaseId?: string;
}

/** Bölüm başına ikon ve vurgu tonu (başlık türe göre diseaseModel.sectionTitle'dan gelir) */
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
  const [selectedDisease, setSelectedDisease] = useState<DiseaseProfile | null>(null);
  const [favoriteIds, setFavoriteIds] = useState<Set<string>>(new Set());

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
  const findById = (id: string) => diseases.find((d) => d.id === id) || diseases.find((d) => (d.aliases || []).includes(id));

  // URL derin bağlantısı (/hastaliklar?id=… ya da #disease-<kimlik>[-bölüm])
  useEffect(() => {
    if (typeof window === 'undefined' || !diseases.length) return;
    const params = new URLSearchParams(window.location.search);
    const hash = window.location.hash;
    let target: DiseaseProfile | undefined;
    const direct = initialDiseaseId || params.get('id');
    if (direct) target = findById(direct);
    if (!target && hash.startsWith('#disease-')) {
      // Kimlikler tire içerir: önce tam kimlik, sonra bölüm son eki atılarak denenir
      const parts = decodeURIComponent(hash.slice('#disease-'.length)).split('-');
      for (let k = parts.length; k >= 1 && !target; k--) target = findById(parts.slice(0, k).join('-'));
    }
    if (target) {
      setSelectedDisease(target);
      const t = target;
      setTimeout(() => triggerDomHighlightAndScroll(hash || `disease-${t.id}`), 300);
    }
  }, [diseases, initialDiseaseId]);

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

  // Varlık dizini: "belirti:ateş" → geçtiği profiller (sınıflandırma süzgeci)
  const entityIndex = useMemo(() => buildEntityIndex(diseases), [diseases]);
  const activeEntity = entityFilter ? entityIndex.get(entityFilter) : undefined;
  const entityIds = useMemo(() => new Set(activeEntity?.hits.map((h) => h.diseaseId) || []), [activeEntity]);

  /** Aranan sözcük bir varlık adıysa ("ateş") sınıflandırma önerisi */
  const entitySuggestions = useMemo(() => {
    const q = foldText(searchQuery.trim());
    if (q.length < 3 || entityFilter) return [];
    const out: Array<{ key: string; label: string; n: number }> = [];
    for (const [key, row] of entityIndex) {
      if (foldText(row.entity.name) !== q) continue;
      const n = new Set(row.hits.map((h) => h.diseaseId)).size;
      if (n >= 2) out.push({ key, label: `${ENTITY_TYPE_LABEL[row.entity.type]}: ${row.entity.name}`, n });
    }
    return out.sort((a, b) => b.n - a.n).slice(0, 4);
  }, [searchQuery, entityIndex, entityFilter]);

  const searchTexts = useMemo(() => new Map(diseases.map((d) => [d.id, foldText(diseaseSearchText(d))])), [diseases]);

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

  // Süzme: Türkçe karakter/büyük-küçük harf duyarsız; ad eşleşmesi ve sorgu zekâsının tanıdığı hastalıklar öne
  const filteredDiseases = useMemo(() => {
    const q = foldText(searchQuery.trim());
    const terms = q.split(/\s+/).filter((t) => t.length >= 2);
    const pinned = new Set(conceptIds);
    const scored: Array<{ d: DiseaseProfile; s: number }> = [];
    for (const d of diseases) {
      if (onlyFavorites && !favoriteIds.has(d.id)) continue;
      if (selectedCategory !== 'all' && d.category !== selectedCategory) continue;
      if (selectedKind !== 'all' && d.kind !== selectedKind) continue;
      if (activeEntity && !entityIds.has(d.id)) continue;
      if (!terms.length) { scored.push({ d, s: 0 }); continue; }
      const name = foldText(`${d.name} ${d.latinName || ''} ${d.icd_code || ''} ${(d.altNames || []).join(' ')}`);
      let s = 0;
      if (pinned.has(d.id)) s += 100;
      if (terms.every((t) => name.includes(t))) s += 50 + (name.startsWith(terms[0]) ? 10 : 0);
      else if (terms.every((t) => searchTexts.get(d.id)?.includes(t))) s += 10;
      if (s > 0) scored.push({ d, s });
    }
    if (terms.length) scored.sort((a, b) => b.s - a.s);
    else scored.sort((a, b) => a.d.name.localeCompare(b.d.name, 'tr'));
    return scored.map((x) => x.d);
  }, [diseases, searchQuery, selectedCategory, selectedKind, onlyFavorites, favoriteIds, conceptIds, activeEntity, entityIds, searchTexts]);

  // Kaydırdıkça yükleme: ilk 40 kart, alt uca yaklaşınca 40'ar eklenir (470 kartın tek seferde çizilmesi donma yapıyordu)
  const PAGE = 40;
  const [limit, setLimit] = useState(PAGE);
  useEffect(() => { setLimit(PAGE); }, [searchQuery, selectedCategory, selectedKind, onlyFavorites, entityFilter]);
  const sentinelRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    const el = sentinelRef.current;
    if (!el || typeof IntersectionObserver === 'undefined') return;
    const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) setLimit((n) => n + PAGE); }, { rootMargin: '600px 0px' });
    io.observe(el);
    return () => io.disconnect();
  }, [limit, filteredDiseases.length]);

  const handleToggleFavorite = useCallback((id: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    const isNow = DiseaseService.toggleFavorite(id);
    setFavoriteIds(DiseaseService.getFavoriteIds());
    if (isNow) toast.success('Favorilere eklendi', 'Profil favorilere kaydedildi.');
    else toast.info('Favorilerden çıkarıldı', 'Profil favorilerinden kaldırıldı.');
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
    if (selectedDisease?.id === id) setSelectedDisease(null);
    toast.info('Silindi', 'Kayıt silindi.');
  };

  const applyEntity = (key: string) => {
    setEntityFilter(key);
    setSelectedDisease(null);
    setSearchQuery('');
    setSelectedCategory('all');
    setSelectedKind('all');
  };

  const sel = selectedDisease;
  const { data: insights } = useDiseaseInsights(sel);
  const canEdit = Boolean(sel && (isAdmin || sel.isCustom));
  const counts = useMemo(() => {
    const cat = new Map<string, number>(); const kind = new Map<string, number>();
    for (const d of diseases) { cat.set(d.category, (cat.get(d.category) || 0) + 1); kind.set(d.kind, (kind.get(d.kind) || 0) + 1); }
    return { cat, kind };
  }, [diseases]);
  const catCount = (c: string) => (c === 'all' ? diseases.length : counts.cat.get(c) || 0);

  /** Seçili profilin varlıkları türlerine göre (sınıflandırma paneli) */
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

  const filtersOn = Boolean(searchQuery || selectedCategory !== 'all' || selectedKind !== 'all' || onlyFavorites || entityFilter);
  const clearFilters = () => { setSearchQuery(''); setSelectedCategory('all'); setSelectedKind('all'); setOnlyFavorites(false); setEntityFilter(null); };

  return (
    <div className="dz-page">
      <PageHeader
        title="Hastalıklar"
        description="Ders notları, Robbins düzeyi ders kitabı bilgisi ve resmi kılavuzlarla doğrulanmış profiller: tanımdan tedaviye, madde madde."
        stats={[
          { label: 'Profil', value: diseases.length.toLocaleString('tr-TR') },
          { label: 'Hastalık', value: diseases.filter((d) => d.kind === 'hastalik').length.toLocaleString('tr-TR'), tone: 'ok' },
          ...(favoriteIds.size ? [{ label: 'Favori', value: favoriteIds.size, tone: 'warn' as const }] : []),
        ]}
        actions={
          <button type="button" className="ui-btn is-primary is-sm" onClick={handleOpenAdd}>
            <Plus aria-hidden /> Profil ekle
          </button>
        }
      />

      <div className="cx-dock dz-dock">
        <div className="cx-search">
          <Search aria-hidden />
          <input
            type="search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Hastalık, belirti (ateş), ilaç, gen ya da bulgu ara"
            aria-label="Hastalıklarda ara"
          />
          {searchQuery && (
            <button type="button" className="dz-x" onClick={() => setSearchQuery('')} aria-label="Aramayı temizle"><X aria-hidden /></button>
          )}
          <button
            type="button"
            className={`dz-fav-btn ${onlyFavorites ? 'is-on' : ''}`}
            aria-pressed={onlyFavorites}
            onClick={() => setOnlyFavorites((v) => !v)}
            title="Yalnız favorileri göster"
          >
            <Bookmark className={onlyFavorites ? 'fill-current' : ''} aria-hidden />
            <span>Favoriler</span>
            {favoriteIds.size > 0 && <b>{favoriteIds.size}</b>}
          </button>
        </div>
        {kinds.length > 1 && (
          <nav className="cx-tabs" aria-label="Kayıt türü" onWheel={(e) => { if (e.deltaY) e.currentTarget.scrollLeft += e.deltaY; }}>
            {(['all', ...kinds] as Array<DiseaseKind | 'all'>).map((k) => (
              <button key={k} type="button" aria-pressed={selectedKind === k} className={`cx-tab ${selectedKind === k ? 'is-on' : ''}`} onClick={() => setSelectedKind(k)}>
                {k === 'all' ? 'Tüm türler' : KIND_LABEL[k]}
                <small>{k === 'all' ? diseases.length : counts.kind.get(k) || 0}</small>
              </button>
            ))}
          </nav>
        )}
        <nav className="cx-tabs" aria-label="Uzmanlık" onWheel={(e) => { if (e.deltaY) e.currentTarget.scrollLeft += e.deltaY; }}>
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              aria-pressed={selectedCategory === cat}
              className={`cx-tab ${selectedCategory === cat ? 'is-on' : ''}`}
              onClick={() => setSelectedCategory(cat)}
            >
              {cat === 'all' ? 'Tüm uzmanlıklar' : cat}
              <small>{catCount(cat)}</small>
            </button>
          ))}
        </nav>
      </div>

      {(activeEntity || entitySuggestions.length > 0) && (
        <div className="dz-entbar" role="status">
          {activeEntity ? (
            <span className="dz-entchip is-on">
              <Tags aria-hidden />
              <span><b>{ENTITY_TYPE_LABEL[activeEntity.entity.type]}:</b> {activeEntity.entity.name} — {entityIds.size} profilde geçiyor</span>
              <button type="button" onClick={() => setEntityFilter(null)} aria-label="Sınıflandırma süzgecini kaldır"><X aria-hidden /></button>
            </span>
          ) : (
            <>
              <span className="dz-entbar-h">Sınıflandır:</span>
              {entitySuggestions.map((s) => (
                <button key={s.key} type="button" className="dz-entchip" onClick={() => applyEntity(s.key)}>
                  <Tags aria-hidden /><span>{s.label} <small>{s.n} profil</small></span>
                </button>
              ))}
            </>
          )}
        </div>
      )}

      {!dataReady ? (
        <p className="dz-result" aria-live="polite">Profiller yükleniyor…</p>
      ) : filteredDiseases.length === 0 ? (
        <div className="dz-empty">
          <span className="dz-empty-ic" aria-hidden><BookOpenText /></span>
          <b>Eşleşen kayıt yok</b>
          <p>Aramayı kısalt ya da süzgeçleri kaldır.</p>
          {filtersOn && <button type="button" className="ui-btn is-tonal is-sm" onClick={clearFilters}>Süzgeçleri temizle</button>}
        </div>
      ) : (
        <>
          <p className="dz-result" aria-live="polite">{filteredDiseases.length.toLocaleString('tr-TR')} kayıt</p>
          <ul className="dz-grid">
            {filteredDiseases.slice(0, limit).map((d) => {
              const hit = activeEntity?.hits.find((h) => h.diseaseId === d.id);
              return (
                <DiseaseCard key={d.id} d={d} isFav={favoriteIds.has(d.id)} onOpen={setSelectedDisease} onFav={handleToggleFavorite}
                  hitLabel={hit && activeEntity ? `${sectionTitle(d.kind, hit.section as DiseaseSectionId) || 'Karakteristik özellik'}|${activeEntity.entity.name}${hit.qualifier ? ` (${hit.qualifier})` : ''}` : undefined} />
              );
            })}
          </ul>
          {filteredDiseases.length > limit && <div ref={sentinelRef} className="dz-more-sentinel" aria-hidden />}
        </>
      )}

      <Sheet
        open={Boolean(sel)}
        onClose={() => setSelectedDisease(null)}
        title={sel?.name || 'Hastalık'}
        subtitle={sel ? [KIND_LABEL[sel.kind], sel.category, sel.icd_code ? `ICD-10 ${sel.icd_code}` : null].filter(Boolean).join(' · ') : undefined}
        width={680}
        actions={sel && (
          <span className="dz-sheet-tools">
            <button type="button" className={`qk-ib ${favoriteIds.has(sel.id) ? 'is-fav' : ''}`} aria-pressed={favoriteIds.has(sel.id)} onClick={() => handleToggleFavorite(sel.id)} aria-label="Favori" title="Favori">
              <Bookmark className={favoriteIds.has(sel.id) ? 'fill-current' : ''} aria-hidden />
            </button>
            <button type="button" className="qk-ib" onClick={() => handleShare(sel)} aria-label="Paylaş" title="Paylaş"><Share2 aria-hidden /></button>
            <button type="button" className="qk-ib" onClick={() => handleCopySummary(sel)} aria-label="Kopyala" title="Özeti kopyala"><Copy aria-hidden /></button>
            {canEdit && <button type="button" className="qk-ib" onClick={() => handleOpenEdit(sel)} aria-label="Düzenle" title="Düzenle"><Edit2 aria-hidden /></button>}
          </span>
        )}
      >
        {sel && (
          <div className="dz-detail">
            {sel.verification && (
              <p className="dz-verif">
                <ShieldCheck aria-hidden />
                <span><b>Web kaynaklarıyla madde madde doğrulandı</b> · {sel.verification.checked} madde denetlendi
                  {sel.verification.fixed + sel.verification.conflict > 0 ? `, ${sel.verification.fixed + sel.verification.conflict} düzeltildi` : ''}
                  {` · ${new Date(sel.verification.at).toLocaleDateString('tr-TR')}`}</span>
              </p>
            )}
            {sel.latinName && sel.latinName !== sel.name && <p className="dz-latin dz-latin-d"><span>Latince / İngilizce</span>{sel.latinName}</p>}

            {sel.hallmarks.length > 0 && (
              <section id={`disease-${sel.id}-hallmarks`} className="dz-hallbox" aria-label="Karakteristik özellik">
                <p className="dz-hallbox-h"><Highlighter aria-hidden /> Karakteristik özellik</p>
                <div className="dz-hallrow">
                  {sel.hallmarks.map((h, k) => <mark key={k} className="dz-hall">{plainText(h.text)}</mark>)}
                </div>
              </section>
            )}

            {SECTION_ORDER.map((sec) => <DiseaseSection key={sec} d={sel} sec={sec} onShare={handleShare} />)}

            {selEntities.length > 0 && (
              <section className="dz-sec is-ai" id={`disease-${sel.id}-entities`}>
                <header className="dz-sec-h">
                  <span className="dz-sec-ic" aria-hidden><Tags /></span>
                  <h4>Sınıflandırma</h4>
                </header>
                <p className="dz-ent-intro">Bir öğeye dokun: aynı belirti, ilaç, gen ya da bulguyu içeren tüm profiller listelenir.</p>
                {selEntities.map((g) => (
                  <div key={g.type} className="dz-entgroup">
                    <h5 className="dz-sub">{ENTITY_TYPE_LABEL[g.type as keyof typeof ENTITY_TYPE_LABEL]}</h5>
                    <div className="dz-chips">
                      {g.items.map((it) => (
                        <button key={it.key} type="button" className="dz-chip" disabled={it.n < 2} onClick={() => applyEntity(it.key)}
                          title={it.n >= 2 ? `${it.name} geçen ${it.n} profili listele` : 'Yalnız bu profilde geçiyor'}>
                          {it.name}{it.n >= 2 && <em>{it.n}</em>}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </section>
            )}

            {(sel.references || []).length > 0 && (
              <section className="dz-sec is-ok" id={`disease-${sel.id}-references`}>
                <header className="dz-sec-h">
                  <span className="dz-sec-ic" aria-hidden><Library /></span>
                  <h4>Kaynaklar</h4>
                </header>
                <ul className="dz-list dz-refs">
                  {(sel.references || []).map((r, k) => (
                    <li key={k} id={`disease-${sel.id}-ref-${k}`}>
                      {r.url ? <a href={r.url} target="_blank" rel="noreferrer">{r.label} <ExternalLink aria-hidden /></a> : r.label}
                    </li>
                  ))}
                </ul>
              </section>
            )}

            <RelatedPanel
              data={insights}
              onOpenDisease={(id) => { const d = findById(id); if (d) setSelectedDisease(d); }}
              onSearch={(q) => { writeLocation('search', q); window.dispatchEvent(new PopStateEvent('popstate')); }}
            />
            {onOpenReportModal && (
              <button type="button" className="ui-btn is-ghost is-sm dz-report" onClick={() => onOpenReportModal({ type: 'disease', id: sel.id, title: sel.name })}>
                <Flag aria-hidden /> Bu profilde hata bildir
              </button>
            )}
          </div>
        )}
      </Sheet>

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
    </div>
  );
};

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

/** Ayrıntı bölümü: başlık türe göre; boş bölüm gösterilmez */
const DiseaseSection = memo(function DiseaseSection({ d, sec, onShare }: { d: DiseaseProfile; sec: DiseaseSectionId; onShare: (d: DiseaseProfile, sec?: string) => void }) {
  const title = sectionTitle(d.kind, sec);
  const shown = title ? sectionFacts(d, sec) : [];
  if (!title || !shown.length) return null;
  const { icon: Icon, tone } = SECTION_META[sec];
  return (
    <section id={`disease-${d.id}-${sec}`} className={`dz-sec is-${tone}`}>
      <header className="dz-sec-h">
        <span className="dz-sec-ic" aria-hidden><Icon /></span>
        <h4>{title}</h4>
        <button type="button" className="dz-sec-link" onClick={() => onShare(d, sec)} title="Bu bölümün bağlantısını paylaş">
          <Share2 aria-hidden /><span>Bağlantı</span>
        </button>
      </header>
      <ul className="dz-list">{shown.map((f, k) => <FactItem key={k} f={f} d={d} />)}</ul>
    </section>
  );
});

/** Liste kartı: yalnız kendi verisi değişince yeniden çizilir (paylaş/kopyala/düzenle ayrıntı panelinde) */
const DiseaseCard = memo(function DiseaseCard({ d, isFav, hitLabel, onOpen, onFav }: {
  d: DiseaseProfile; isFav: boolean; hitLabel?: string; onOpen: (d: DiseaseProfile) => void; onFav: (id: string, e?: React.MouseEvent) => void;
}) {
  const def = sectionFacts(d, 'definition')[0];
  const [hitTitle, hitText] = hitLabel ? hitLabel.split('|') : [];
  return (
    <li id={`disease-${d.id}`} className="dz-card" data-tone={toneOf(d.category)}>
      <button type="button" className="dz-card-main" onClick={() => onOpen(d)}>
        <span className="dz-card-top">
          <span className="dz-cat"><i aria-hidden />{d.category}</span>
          {d.kind !== 'hastalik' && <span className="dz-kind">{KIND_LABEL[d.kind]}</span>}
          {d.icd_code && <span className="dz-icd">{d.icd_code}</span>}
        </span>
        <span className="dz-name">{d.name}</span>
        {d.latinName && d.latinName !== d.name && <span className="dz-latin">{d.latinName}</span>}
        {d.hallmarks.length > 0 && (
          <span className="dz-hallrow">
            {d.hallmarks.slice(0, 2).map((h, k) => (
              <mark key={k} className="dz-hall is-sm" title={plainText(h.text)}><span>{plainText(h.text)}</span></mark>
            ))}
          </span>
        )}
        {hitTitle ? <span className="dz-clin"><b>{hitTitle}</b>{hitText}</span> : def && <span className="dz-clin">{plainText(def.text)}</span>}
      </button>
      <div className="dz-card-f">
        <button type="button" className={`qk-ib ${isFav ? 'is-fav' : ''}`} aria-pressed={isFav} onClick={(e) => { e.stopPropagation(); onFav(d.id, e); }} aria-label={isFav ? 'Favorilerden çıkar' : 'Favorilere ekle'} title={isFav ? 'Favorilerden çıkar' : 'Favorilere ekle'}>
          <Bookmark className={isFav ? 'fill-current' : ''} aria-hidden />
        </button>
        <span className="qk-sp" />
        <button type="button" className="dz-more" onClick={() => onOpen(d)}>Ayrıntı <ChevronRight aria-hidden /></button>
      </div>
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
