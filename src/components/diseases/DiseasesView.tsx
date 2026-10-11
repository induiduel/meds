import React, { useState, useMemo, useEffect } from 'react';
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
  ShieldCheck,
  Edit2,
  Trash2,
  X,
  Zap,
  Flag,
} from 'lucide-react';
import { PageHeader } from '../ui/PageHeader';
import { DiseaseProfile } from '../../types/disease';
import { DiseaseService } from '../../services/diseaseService';
import { shareDeepLink, triggerDomHighlightAndScroll } from '../../services/universalRedirectService';
import { toast } from '../ui/Toast';
import { Sheet } from '../ui/Sheet';
import { AppUser, ADMIN_EMAIL } from '../../services/auth';
import { safeJsonFetch } from '../../services/api';
import { writeLocation } from '../../router';
import { foldText } from '../../services/searchText';
import { EvidenceList, QualityStrip, RelatedPanel, useDiseaseInsights, type Evidence, type SectionKey } from './DiseaseInsights';

interface DiseasesViewProps {
  currentUser?: AppUser | null;
  onOpenReportModal?: (target: { type: string; id: string; title: string }) => void;
  /** Aramadan gelen hastalık: açılınca ayrıntı sayfası açılır */
  initialDiseaseId?: string;
}

export const DiseasesView: React.FC<DiseasesViewProps> = ({
  currentUser,
  onOpenReportModal,
  initialDiseaseId,
}) => {
  const isAdmin = currentUser?.email === ADMIN_EMAIL || Boolean((currentUser as any)?.isMasterAdmin);
  const [diseases, setDiseases] = useState<DiseaseProfile[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [onlyFavorites, setOnlyFavorites] = useState(false);
  const [selectedDisease, setSelectedDisease] = useState<DiseaseProfile | null>(null);
  const [favoriteIds, setFavoriteIds] = useState<Set<string>>(new Set());

  // Ekleme / Düzenleme Modalı
  const [showAddEditModal, setShowAddEditModal] = useState(false);
  const [editingDisease, setEditingDisease] = useState<DiseaseProfile | null>(null);
  const [formName, setFormName] = useState('');
  const [formLatinName, setFormLatinName] = useState('');
  const [formIcdCode, setFormIcdCode] = useState('');
  const [formCategory, setFormCategory] = useState('Genel Patoloji');
  const [formEtiology, setFormEtiology] = useState('');
  const [formMorphology, setFormMorphology] = useState('');
  const [formSymptoms, setFormSymptoms] = useState('');
  const [formPathognomonic, setFormPathognomonic] = useState('');
  const [formDiagnosis, setFormDiagnosis] = useState('');
  const [formImaging, setFormImaging] = useState('');
  const [formTreatment, setFormTreatment] = useState('');
  const [formPhysiology, setFormPhysiology] = useState('');
  const [formNotes, setFormNotes] = useState('');

  // Veri yükleme
  const reloadDiseases = () => {
    const list = DiseaseService.getAllDiseases();
    setDiseases(list);
    setFavoriteIds(DiseaseService.getFavoriteIds());
  };

  useEffect(() => {
    reloadDiseases();
  }, []);

  // URL Deep Link kontrolü (örn. /hastaliklar?id=akut-apendisit veya hash #disease-...)
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const params = new URLSearchParams(window.location.search);
    const targetId = params.get('id');
    const hash = window.location.hash;

    let targetDiseaseId = initialDiseaseId || targetId;
    if (!targetDiseaseId && hash.startsWith('#disease-')) {
      // Kimlikler tire içerir (akut-apendisit): önce tam kimlik, sonra bölüm son eki (-etiology …) atılarak denenir
      const raw = decodeURIComponent(hash.slice('#disease-'.length));
      const ids = new Set(diseases.map((d) => d.id));
      const parts = raw.split('-');
      for (let k = parts.length; k >= 1 && !targetDiseaseId; k--) {
        const cand = parts.slice(0, k).join('-');
        if (ids.has(cand)) targetDiseaseId = cand;
      }
    }

    if (targetDiseaseId) {
      const found = diseases.find(d => d.id === targetDiseaseId);
      if (found) {
        setSelectedDisease(found);
        setTimeout(() => {
          triggerDomHighlightAndScroll(hash || `disease-${targetDiseaseId}`);
        }, 300);
      }
    }
  }, [diseases, initialDiseaseId]);

  // Kaynak analizi: profil doluluğu (liste rozetleri ve şablon metinlerin gizlenmesi için kompakt harita)
  const [quality, setQuality] = useState<Record<string, [number, string[], number]>>({});
  useEffect(() => {
    safeJsonFetch<{ success: boolean; q: Record<string, [number, string[], number]> }>('/api/diseases/quality').then((r) => {
      if (r.ok && r.data?.success) setQuality(r.data.q || {});
    });
  }, []);
  const isWeak = (d: DiseaseProfile, field: string) => Boolean(quality[d.id]?.[1].includes(field));

  // Sorgu zekâsı: yazım hatası / eşanlamlı / kısaltma ("kansizlik", "ttp", "bobrek tumoru") → hastalık kimlikleri
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

  // Kategoriler
  const categories = useMemo(() => {
    const cats = new Set<string>();
    diseases.forEach(d => {
      if (d.category) cats.add(d.category);
    });
    return ['all', ...Array.from(cats)];
  }, [diseases]);

  // Filtreleme
  // Türkçe karakter ve büyük/küçük harf duyarsız; ad/Latince/ICD eşleşmesi ve sorgu zekâsının tanıdığı hastalıklar öne
  const filteredDiseases = useMemo(() => {
    const q = foldText(searchQuery.trim());
    const terms = q.split(/\s+/).filter((t) => t.length >= 2);
    const pinned = new Set(conceptIds);
    const scored: Array<{ d: DiseaseProfile; s: number }> = [];
    for (const d of diseases) {
      if (onlyFavorites && !favoriteIds.has(d.id)) continue;
      if (selectedCategory !== 'all' && d.category !== selectedCategory) continue;
      if (!terms.length) { scored.push({ d, s: 0 }); continue; }
      const name = foldText(`${d.name} ${d.latinName || ''} ${d.icd_code || ''}`);
      let s = 0;
      if (pinned.has(d.id)) s += 100;
      if (terms.every((t) => name.includes(t))) s += 50 + (name.startsWith(terms[0]) ? 10 : 0);
      else {
        // Profil içeriği (yalnız gerçek, şablon olmayan bölümler)
        const body = foldText([
          ...(isWeak(d, 'symptoms') ? [] : d.symptoms_clinical), ...(isWeak(d, 'pathognomonic') ? [] : d.pathognomonic_features),
          ...(isWeak(d, 'etiology') ? [] : d.etiology), ...(isWeak(d, 'treatment') ? [] : d.treatment), d.source_notes_summary || '',
        ].join(' '));
        if (terms.every((t) => name.includes(t) || body.includes(t))) s += 10;
      }
      if (s > 0) scored.push({ d, s });
    }
    if (terms.length) scored.sort((a, b) => b.s - a.s);
    return scored.map((x) => x.d);
  }, [diseases, searchQuery, selectedCategory, onlyFavorites, favoriteIds, conceptIds, quality]);

  // Favori Aç/Kapa
  const handleToggleFavorite = (id: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    const isNow = DiseaseService.toggleFavorite(id);
    setFavoriteIds(DiseaseService.getFavoriteIds());
    if (isNow) {
      toast.success('Favorilere Eklendi', 'Hastalık profiliniz favorilere kaydedildi.');
    } else {
      toast.info('Favorilerden Çıkarıldı', 'Hastalık favorilerinizden kaldırıldı.');
    }
  };

  // Paylaş
  const handleShare = async (disease: DiseaseProfile, section?: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    await shareDeepLink({
      type: 'disease',
      id: disease.id,
      title: `${disease.name} · MeDSor Tıbbi Hastalık Atlası`,
      subTarget: section,
      highlightText: disease.name,
    });
  };

  // Kopyala
  const handleCopySummary = (disease: DiseaseProfile, e?: React.MouseEvent) => {
    e?.stopPropagation();
    const lines = [
      `🩺 ${disease.name} ${disease.latinName ? `(${disease.latinName})` : ''}`,
      disease.icd_code ? `ICD-10: ${disease.icd_code}` : '',
      `Kategori: ${disease.category}`,
      '',
      '📌 [Klinik & Semptomlar]:',
      disease.symptoms_clinical.map(s => `• ${s}`).join('\n'),
      '',
      '🎯 [Patognomonik & Sınav Spotu]:',
      disease.pathognomonic_features.map(p => `• ${p}`).join('\n'),
      '',
      '🔬 [Morfoloji & Patoloji]:',
      disease.morphology_pathology.map(m => `• ${m}`).join('\n'),
      '',
      '💊 [Tedavi Protokolü]:',
      disease.treatment.map(t => `• ${t}`).join('\n'),
      '',
      '🔗 MeDSor Klinik Atlası: ' + window.location.origin + `/hastaliklar?id=${disease.id}`
    ].filter(Boolean).join('\n');

    navigator.clipboard.writeText(lines);
    toast.success('Kopyalandı', 'Hastalık klinik özeti panoya kopyalandı.');
  };

  // Düzenleme aç
  const handleOpenEdit = (disease: DiseaseProfile, e?: React.MouseEvent) => {
    e?.stopPropagation();
    setEditingDisease(disease);
    setFormName(disease.name);
    setFormLatinName(disease.latinName || '');
    setFormIcdCode(disease.icd_code || '');
    setFormCategory(disease.category);
    setFormEtiology(disease.etiology.join('\n'));
    setFormMorphology(disease.morphology_pathology.join('\n'));
    setFormSymptoms(disease.symptoms_clinical.join('\n'));
    setFormPathognomonic(disease.pathognomonic_features.join('\n'));
    setFormDiagnosis(disease.diagnostic_methods.join('\n'));
    setFormImaging(disease.imaging_findings.join('\n'));
    setFormTreatment(disease.treatment.join('\n'));
    setFormPhysiology((disease.physiology_pathophysiology || []).join('\n'));
    setFormNotes(disease.source_notes_summary || '');
    setShowAddEditModal(true);
  };

  // Kaynak kanıtını forma aktar: düzenleme formu açılır, cümle ilgili alana eklenir (alan şablonsa şablonun yerine)
  const handleAdoptEvidence = (disease: DiseaseProfile, e: Evidence, weak: boolean) => {
    handleOpenEdit(disease);
    const setters: Partial<Record<SectionKey, React.Dispatch<React.SetStateAction<string>>>> = {
      symptoms: setFormSymptoms, pathognomonic: setFormPathognomonic, etiology: setFormEtiology, physiology: setFormPhysiology,
      pathology: setFormMorphology, diagnosis: setFormDiagnosis, imaging: setFormImaging, treatment: setFormTreatment,
    };
    const set = setters[e.section] || setFormNotes;
    set((cur) => (weak || !cur.trim() ? e.t : cur.includes(e.t) ? cur : `${cur}\n${e.t}`));
    toast.info('Forma aktarıldı', 'Kaynak cümlesi ilgili alana eklendi; gözden geçirip kaydedebilirsin.');
  };

  // Yeni ekleme aç
  const handleOpenAdd = () => {
    setEditingDisease(null);
    setFormName('');
    setFormLatinName('');
    setFormIcdCode('');
    setFormCategory('Genel Patoloji');
    setFormEtiology('');
    setFormMorphology('');
    setFormSymptoms('');
    setFormPathognomonic('');
    setFormDiagnosis('');
    setFormImaging('');
    setFormTreatment('');
    setFormPhysiology('');
    setFormNotes('');
    setShowAddEditModal(true);
  };

  // Form Kaydet
  const handleSaveForm = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formName.trim()) {
      toast.error('Hata', 'Lütfen hastalık adını girin.');
      return;
    }

    const splitLines = (str: string) => str.split('\n').map(s => s.trim()).filter(Boolean);

    const slug = editingDisease?.id || formName.trim().toLowerCase()
      .replace(/ğ/g, 'g').replace(/ü/g, 'u').replace(/ş/g, 's')
      .replace(/ı/g, 'i').replace(/ö/g, 'o').replace(/ç/g, 'c')
      .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

    const newProfile: DiseaseProfile = {
      id: slug,
      name: formName.trim(),
      latinName: formLatinName.trim() || undefined,
      icd_code: formIcdCode.trim() || undefined,
      category: formCategory.trim() || 'Genel Patoloji',
      etiology: splitLines(formEtiology),
      morphology_pathology: splitLines(formMorphology),
      symptoms_clinical: splitLines(formSymptoms),
      pathognomonic_features: splitLines(formPathognomonic),
      diagnostic_methods: splitLines(formDiagnosis),
      imaging_findings: splitLines(formImaging),
      treatment: splitLines(formTreatment),
      physiology_pathophysiology: splitLines(formPhysiology),
      source_notes_summary: formNotes.trim() || undefined,
      isCustom: true,
      createdBy: currentUser?.displayName || currentUser?.email || 'Öğrenci',
      createdAt: editingDisease?.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      verifiedSources: [
        {
          source: 'Kullanıcı Katkısı',
          verified: true,
          verifiedAt: new Date().toISOString()
        }
      ]
    };

    DiseaseService.saveDisease(newProfile);
    reloadDiseases();
    setShowAddEditModal(false);
    toast.success('Başarılı', editingDisease ? 'Hastalık profili güncellendi.' : 'Yeni hastalık atlasa eklendi.');
  };

  // Silme
  const handleDelete = (id: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    if (!window.confirm('Bu hastalığı atlas veritabanından silmek istediğinize emin misiniz?')) return;
    DiseaseService.deleteDisease(id);
    reloadDiseases();
    if (selectedDisease?.id === id) {
      setSelectedDisease(null);
    }
    toast.info('Silindi', 'Hastalık kaydı silindi.');
  };

  const sel = selectedDisease;
  const { data: insights, loading: insightsLoading } = useDiseaseInsights(sel);
  const canEdit = Boolean(sel && (isAdmin || sel.isCustom));
  const catCount = (c: string) => (c === 'all' ? diseases.length : diseases.filter((d) => d.category === c).length);

  /** Ayrıntı bölümü: ikon karolu başlık + madde listesi; boş bölüm gösterilmez. */
  const Sec: React.FC<{ id: string; icon: React.ElementType; tone: string; title: string; items?: string[]; shareKey?: string; secKey?: SectionKey; children?: React.ReactNode }> = ({ id, icon: Icon, tone, title, items, shareKey, secKey, children }) => {
    // Profil alanı şablon/boş ise (kaynak analizi) şablon metni gösterilmez; yerine ders kaynaklarından kanıtlar
    const status = secKey ? insights?.audit?.fields[secKey] : undefined;
    const weak = status === 'placeholder' || status === 'empty';
    const ev = secKey ? insights?.evidence[secKey] : undefined;
    const shownItems = weak ? [] : items;
    if (!children && (!shownItems || shownItems.length === 0) && !(weak && ev?.length)) return null;
    return (
      <section id={id} className={`dz-sec is-${tone}`}>
        <header className="dz-sec-h">
          <span className="dz-sec-ic" aria-hidden><Icon /></span>
          <h4>{title}</h4>
          {shareKey && sel && (
            <button type="button" className="dz-sec-link" onClick={() => handleShare(sel, shareKey)} title="Bu bölümün bağlantısını paylaş">
              <Share2 aria-hidden /><span>Bağlantı</span>
            </button>
          )}
        </header>
        {shownItems && shownItems.length > 0 && (
          <ul className="dz-list">{shownItems.map((t, k) => <li key={k}>{t}</li>)}</ul>
        )}
        {children}
        {weak && ev && ev.length > 0 && (
          <EvidenceList items={ev} onAdopt={canEdit && sel ? (e) => handleAdoptEvidence(sel, e, true) : undefined} />
        )}
      </section>
    );
  };

  const field = (label: string, value: string, set: (v: string) => void, opts: { area?: boolean; required?: boolean; ph?: string; hint?: string } = {}) => (
    <label className="dz-field">
      <span>{label}{opts.required && <b aria-hidden> *</b>}{opts.hint && <small>{opts.hint}</small>}</span>
      {opts.area ? (
        <textarea rows={3} value={value} onChange={(e) => set(e.target.value)} placeholder={opts.ph} />
      ) : (
        <input type="text" value={value} required={opts.required} onChange={(e) => set(e.target.value)} placeholder={opts.ph} />
      )}
    </label>
  );

  return (
    <div className="dz-page">
      <PageHeader
        title="Hastalıklar"
        description="Ders notları ve amfi slaytlarından derlenen hastalık profilleri: etiyolojiden tedaviye."
        stats={[
          { label: 'Hastalık', value: diseases.length.toLocaleString('tr-TR') },
          { label: 'Doğrulanmış', value: diseases.filter((d) => (d.verifiedSources || []).length > 0).length.toLocaleString('tr-TR'), tone: 'ok' },
          ...(favoriteIds.size ? [{ label: 'Favori', value: favoriteIds.size, tone: 'warn' as const }] : []),
        ]}
        actions={
          <button type="button" className="ui-btn is-primary is-sm" onClick={handleOpenAdd}>
            <Plus aria-hidden /> Hastalık ekle
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
            placeholder="Hastalık, semptom, ICD-10 ya da tedavi ara"
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
        <nav className="cx-tabs" aria-label="Uzmanlık" onWheel={(e) => { if (e.deltaY) e.currentTarget.scrollLeft += e.deltaY; }}>
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              aria-pressed={selectedCategory === cat}
              className={`cx-tab ${selectedCategory === cat ? 'is-on' : ''}`}
              onClick={() => setSelectedCategory(cat)}
            >
              {cat === 'all' ? 'Tümü' : cat}
              <small>{catCount(cat)}</small>
            </button>
          ))}
        </nav>
      </div>

      {filteredDiseases.length === 0 ? (
        <div className="dz-empty">
          <span className="dz-empty-ic" aria-hidden><BookOpenText /></span>
          <b>Eşleşen hastalık yok</b>
          <p>Aramayı kısalt ya da uzmanlık süzgecini "Tümü"ye al.</p>
          {(searchQuery || selectedCategory !== 'all' || onlyFavorites) && (
            <button type="button" className="ui-btn is-tonal is-sm" onClick={() => { setSearchQuery(''); setSelectedCategory('all'); setOnlyFavorites(false); }}>
              Süzgeçleri temizle
            </button>
          )}
        </div>
      ) : (
        <>
          <p className="dz-result" aria-live="polite">{filteredDiseases.length.toLocaleString('tr-TR')} hastalık</p>
          <ul className="dz-grid">
            {filteredDiseases.map((d) => {
              const isFav = favoriteIds.has(d.id);
              return (
                <li key={d.id} id={`disease-${d.id}`} className="dz-card" data-tone={toneOf(d.category)}>
                  <button type="button" className="dz-card-main" onClick={() => setSelectedDisease(d)}>
                    <span className="dz-card-top">
                      <span className="dz-cat"><i aria-hidden />{d.category}</span>
                      {d.icd_code && <span className="dz-icd">{d.icd_code}</span>}
                      {quality[d.id] && (
                        <span className={`dz-qbadge ${quality[d.id][0] >= 70 ? 'is-good' : ''} ${d.icd_code ? '' : 'ml-auto'}`} title="Profil doluluğu (kaynak analizi)">%{quality[d.id][0]}</span>
                      )}
                    </span>
                    <span className="dz-name">{d.name}</span>
                    {d.latinName && d.latinName !== d.name && <span className="dz-latin">{d.latinName}</span>}
                    {d.pathognomonic_features.length > 0 && !isWeak(d, 'pathognomonic') && (
                      <span className="dz-tip"><Zap aria-hidden /><span><b>Ayırıcı ipucu</b>{d.pathognomonic_features[0]}</span></span>
                    )}
                    {d.symptoms_clinical.length > 0 && !isWeak(d, 'symptoms') && (
                      <span className="dz-clin"><b>Klinik</b>{d.symptoms_clinical.slice(0, 2).join(' · ')}</span>
                    )}
                  </button>
                  <div className="dz-card-f">
                    <button type="button" className={`qk-ib ${isFav ? 'is-fav' : ''}`} aria-pressed={isFav} onClick={(e) => handleToggleFavorite(d.id, e)} aria-label={isFav ? 'Favorilerden çıkar' : 'Favorilere ekle'} title={isFav ? 'Favorilerden çıkar' : 'Favorilere ekle'}>
                      <Bookmark className={isFav ? 'fill-current' : ''} aria-hidden />
                    </button>
                    <button type="button" className="qk-ib" onClick={(e) => handleShare(d, undefined, e)} aria-label="Bağlantıyı paylaş" title="Bağlantıyı paylaş"><Share2 aria-hidden /></button>
                    <button type="button" className="qk-ib" onClick={(e) => handleCopySummary(d, e)} aria-label="Klinik özeti kopyala" title="Klinik özeti kopyala"><Copy aria-hidden /></button>
                    {onOpenReportModal && (
                      <button type="button" className="qk-ib" onClick={(e) => { e.stopPropagation(); onOpenReportModal({ type: 'disease', id: d.id, title: d.name }); }} aria-label="Hata bildir" title="Hata bildir"><Flag aria-hidden /></button>
                    )}
                    {(isAdmin || d.isCustom) && (
                      <>
                        <button type="button" className="qk-ib" onClick={(e) => handleOpenEdit(d, e)} aria-label="Düzenle" title="Düzenle"><Edit2 aria-hidden /></button>
                        <button type="button" className="qk-ib is-danger" onClick={(e) => handleDelete(d.id, e)} aria-label="Sil" title="Sil"><Trash2 aria-hidden /></button>
                      </>
                    )}
                    <span className="qk-sp" />
                    <button type="button" className="dz-more" onClick={() => setSelectedDisease(d)}>Ayrıntı <ChevronRight aria-hidden /></button>
                  </div>
                </li>
              );
            })}
          </ul>
        </>
      )}

      <Sheet
        open={Boolean(sel)}
        onClose={() => setSelectedDisease(null)}
        title={sel?.name || 'Hastalık'}
        subtitle={sel ? [sel.category, sel.icd_code ? `ICD-10 ${sel.icd_code}` : null].filter(Boolean).join(' · ') : undefined}
        width={640}
        actions={sel && (
          <span className="dz-sheet-tools">
            <button type="button" className={`qk-ib ${favoriteIds.has(sel.id) ? 'is-fav' : ''}`} aria-pressed={favoriteIds.has(sel.id)} onClick={() => handleToggleFavorite(sel.id)} aria-label="Favori" title="Favori">
              <Bookmark className={favoriteIds.has(sel.id) ? 'fill-current' : ''} aria-hidden />
            </button>
            <button type="button" className="qk-ib" onClick={() => handleShare(sel)} aria-label="Paylaş" title="Paylaş"><Share2 aria-hidden /></button>
            <button type="button" className="qk-ib" onClick={() => handleCopySummary(sel)} aria-label="Kopyala" title="Klinik özeti kopyala"><Copy aria-hidden /></button>
          </span>
        )}
      >
        {sel && (
          <div className="dz-detail">
            <QualityStrip data={insights} loading={insightsLoading} />
            {(sel.latinName || (sel.verifiedSources && sel.verifiedSources.length > 0)) && (
              <div className="dz-meta">
                {sel.latinName && <p className="dz-latin"><span>Latince</span>{sel.latinName}</p>}
                {sel.verifiedSources && sel.verifiedSources.length > 0 && (
                  <div className="dz-srcs">
                    {sel.verifiedSources.map((vs, k) => (
                      <span key={k} className="dz-src">
                        <ShieldCheck aria-hidden />{vs.source}
                        {vs.referenceUrl && <a href={vs.referenceUrl} target="_blank" rel="noreferrer" aria-label="Kaynağı aç"><ExternalLink aria-hidden /></a>}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            )}
            <Sec id={`disease-${sel.id}-pathognomonic`} icon={Zap} tone="warn" title="Patognomonik ve ayırıcı tanı" items={sel.pathognomonic_features} shareKey="pathognomonic" secKey="pathognomonic" />
            <Sec id={`disease-${sel.id}-symptoms`} icon={Stethoscope} tone="accent" title="Klinik belirti ve bulgular" items={sel.symptoms_clinical} shareKey="symptoms" secKey="symptoms" />
            <Sec id={`disease-${sel.id}-etiology`} icon={Activity} tone="ai" title="Etiyoloji ve risk faktörleri" items={sel.etiology} shareKey="etiology" secKey="etiology" />
            <Sec id={`disease-${sel.id}-physiology`} icon={Heart} tone="clinic" title="Fizyopatoloji" items={sel.physiology_pathophysiology} secKey="physiology" />
            <Sec id={`disease-${sel.id}-pathology`} icon={BookOpenText} tone="bad" title="Morfoloji ve patoloji" items={sel.morphology_pathology} shareKey="pathology" secKey="pathology" />
            {(() => {
              const dxWeak = insights?.audit?.fields.diagnosis && insights.audit.fields.diagnosis !== 'ok';
              const imWeak = insights?.audit?.fields.imaging && insights.audit.fields.imaging !== 'ok';
              const dx = dxWeak ? [] : sel.diagnostic_methods;
              const im = imWeak ? [] : sel.imaging_findings || [];
              const dxEv = dxWeak ? insights?.evidence.diagnosis : undefined;
              const imEv = imWeak ? insights?.evidence.imaging : undefined;
              if (!dx.length && !im.length && !dxEv?.length && !imEv?.length) return null;
              const adopt = canEdit ? (e: Evidence) => handleAdoptEvidence(sel, e, true) : undefined;
              return (
                <Sec id={`disease-${sel.id}-diagnosis`} icon={Stethoscope} tone="clinic" title="Tanı ve görüntüleme" shareKey="diagnosis">
                  {(dx.length > 0 || (dxEv?.length || 0) > 0) && <h5 className="dz-sub">Laboratuvar ve biyopsi</h5>}
                  {dx.length > 0 && <ul className="dz-list">{dx.map((t, k) => <li key={k}>{t}</li>)}</ul>}
                  <EvidenceList items={dxEv} onAdopt={adopt} limit={3} />
                  {(im.length > 0 || (imEv?.length || 0) > 0) && <h5 className="dz-sub">Görüntüleme</h5>}
                  {im.length > 0 && <ul className="dz-list">{im.map((t, k) => <li key={k}>{t}</li>)}</ul>}
                  <EvidenceList items={imEv} onAdopt={adopt} limit={3} />
                </Sec>
              );
            })()}
            <Sec id={`disease-${sel.id}-treatment`} icon={Pill} tone="ok" title="Tedavi ve ilaçlar" items={sel.treatment} shareKey="treatment" secKey="treatment" />
            {sel.source_notes_summary && (
              <Sec id={`disease-${sel.id}-notes`} icon={Sparkles} tone="ai" title="Amfi ve ders notu vurguları">
                <p className="dz-note">{sel.source_notes_summary}</p>
              </Sec>
            )}
            <RelatedPanel
              data={insights}
              onOpenDisease={(id) => { const d = diseases.find((x) => x.id === id); if (d) setSelectedDisease(d); }}
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
        title={editingDisease ? 'Hastalığı düzenle' : 'Yeni hastalık'}
        subtitle="Her satır bir madde olarak kaydedilir."
        width={640}
      >
        <form onSubmit={handleSaveForm} className="dz-form">
          <div className="dz-form-2">
            {field('Hastalık adı', formName, setFormName, { required: true, ph: 'Örn. Akut apandisit' })}
            {field('Latince adı', formLatinName, setFormLatinName, { ph: 'Örn. Appendicitis acuta' })}
            {field('ICD-10 kodu', formIcdCode, setFormIcdCode, { ph: 'Örn. K35' })}
            {field('Uzmanlık', formCategory, setFormCategory, { ph: 'Örn. Tıbbi Patoloji' })}
          </div>
          {field('Klinik belirtiler', formSymptoms, setFormSymptoms, { area: true, ph: 'Periumbilikal başlayan ağrı\nSağ alt kadrana yerleşme' })}
          {field('Patognomonik ve ayırıcı tanı', formPathognomonic, setFormPathognomonic, { area: true, ph: 'McBurney noktasında hassasiyet' })}
          {field('Etiyoloji ve risk faktörleri', formEtiology, setFormEtiology, { area: true, ph: 'Fekalit ile tıkanma' })}
          {field('Fizyopatoloji', formPhysiology, setFormPhysiology, { area: true })}
          {field('Morfoloji ve patoloji', formMorphology, setFormMorphology, { area: true, ph: 'Muskularis propriada nötrofil infiltrasyonu' })}
          <div className="dz-form-2">
            {field('Tanı yöntemleri', formDiagnosis, setFormDiagnosis, { area: true, ph: 'Lökositoz, USG' })}
            {field('Görüntüleme', formImaging, setFormImaging, { area: true, ph: 'BT: periapendiküler yağ dokusunda kirlenme' })}
          </div>
          {field('Tedavi', formTreatment, setFormTreatment, { area: true, ph: 'Erken apendektomi' })}
          {field('Amfi ve ders notu vurguları', formNotes, setFormNotes, { area: true, hint: 'Sınavda öne çıkan noktalar' })}
          <div className="dz-form-f">
            <button type="button" className="ui-btn is-ghost" onClick={() => setShowAddEditModal(false)}>Vazgeç</button>
            <button type="submit" className="ui-btn is-primary">{editingDisease ? 'Kaydet' : 'Ekle'}</button>
          </div>
        </form>
      </Sheet>
    </div>
  );
};

/** Uzmanlığa göre sabit vurgu tonu (yalnız DS tokenları): aynı uzmanlık her yerde aynı renkte. */
const TONES = ['accent', 'clinic', 'ai', 'warn', 'ok', 'bad'] as const;
function toneOf(cat: string) {
  let h = 0;
  for (const ch of String(cat || '')) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
  return TONES[h % TONES.length];
}
