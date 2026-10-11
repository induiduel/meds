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

interface DiseasesViewProps {
  currentUser?: AppUser | null;
  onOpenReportModal?: (target: { type: string; id: string; title: string }) => void;
}

export const DiseasesView: React.FC<DiseasesViewProps> = ({
  currentUser,
  onOpenReportModal,
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

    let targetDiseaseId = targetId;
    if (!targetDiseaseId && hash.startsWith('#disease-')) {
      const parts = hash.replace('#disease-', '').split('-');
      targetDiseaseId = parts[0];
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
  }, [diseases]);

  // Kategoriler
  const categories = useMemo(() => {
    const cats = new Set<string>();
    diseases.forEach(d => {
      if (d.category) cats.add(d.category);
    });
    return ['all', ...Array.from(cats)];
  }, [diseases]);

  // Filtreleme
  const filteredDiseases = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    return diseases.filter(d => {
      if (onlyFavorites && !favoriteIds.has(d.id)) return false;
      if (selectedCategory !== 'all' && d.category !== selectedCategory) return false;

      if (!q) return true;

      const nameMatch = d.name.toLowerCase().includes(q) || (d.latinName && d.latinName.toLowerCase().includes(q));
      const icdMatch = d.icd_code && d.icd_code.toLowerCase().includes(q);
      const symptomMatch = d.symptoms_clinical.some(s => s.toLowerCase().includes(q));
      const pathogMatch = d.pathognomonic_features.some(p => p.toLowerCase().includes(q));
      const etiologyMatch = d.etiology.some(e => e.toLowerCase().includes(q));
      const treatmentMatch = d.treatment.some(t => t.toLowerCase().includes(q));

      return nameMatch || icdMatch || symptomMatch || pathogMatch || etiologyMatch || treatmentMatch;
    });
  }, [diseases, searchQuery, selectedCategory, onlyFavorites, favoriteIds]);

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
  const catCount = (c: string) => (c === 'all' ? diseases.length : diseases.filter((d) => d.category === c).length);

  /** Ayrıntı bölümü: ikon karolu başlık + madde listesi; boş bölüm gösterilmez. */
  const Sec: React.FC<{ id: string; icon: React.ElementType; tone: string; title: string; items?: string[]; shareKey?: string; children?: React.ReactNode }> = ({ id, icon: Icon, tone, title, items, shareKey, children }) => {
    if (!children && (!items || items.length === 0)) return null;
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
        {items && items.length > 0 && (
          <ul className="dz-list">{items.map((t, k) => <li key={k}>{t}</li>)}</ul>
        )}
        {children}
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
                    </span>
                    <span className="dz-name">{d.name}</span>
                    {d.latinName && d.latinName !== d.name && <span className="dz-latin">{d.latinName}</span>}
                    {d.pathognomonic_features.length > 0 && (
                      <span className="dz-tip"><Zap aria-hidden /><span><b>Ayırıcı ipucu</b>{d.pathognomonic_features[0]}</span></span>
                    )}
                    {d.symptoms_clinical.length > 0 && (
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
            <Sec id={`disease-${sel.id}-pathognomonic`} icon={Zap} tone="warn" title="Patognomonik ve ayırıcı tanı" items={sel.pathognomonic_features} shareKey="pathognomonic" />
            <Sec id={`disease-${sel.id}-symptoms`} icon={Stethoscope} tone="accent" title="Klinik belirti ve bulgular" items={sel.symptoms_clinical} shareKey="symptoms" />
            <Sec id={`disease-${sel.id}-etiology`} icon={Activity} tone="ai" title="Etiyoloji ve risk faktörleri" items={sel.etiology} shareKey="etiology" />
            <Sec id={`disease-${sel.id}-physiology`} icon={Heart} tone="clinic" title="Fizyopatoloji" items={sel.physiology_pathophysiology} />
            <Sec id={`disease-${sel.id}-pathology`} icon={BookOpenText} tone="bad" title="Morfoloji ve patoloji" items={sel.morphology_pathology} shareKey="pathology" />
            {(sel.diagnostic_methods.length > 0 || (sel.imaging_findings || []).length > 0) && (
              <Sec id={`disease-${sel.id}-diagnosis`} icon={Stethoscope} tone="clinic" title="Tanı ve görüntüleme" shareKey="diagnosis">
                {sel.diagnostic_methods.length > 0 && (<><h5 className="dz-sub">Laboratuvar ve biyopsi</h5><ul className="dz-list">{sel.diagnostic_methods.map((t, k) => <li key={k}>{t}</li>)}</ul></>)}
                {(sel.imaging_findings || []).length > 0 && (<><h5 className="dz-sub">Görüntüleme</h5><ul className="dz-list">{sel.imaging_findings.map((t, k) => <li key={k}>{t}</li>)}</ul></>)}
              </Sec>
            )}
            <Sec id={`disease-${sel.id}-treatment`} icon={Pill} tone="ok" title="Tedavi ve ilaçlar" items={sel.treatment} shareKey="treatment" />
            {sel.source_notes_summary && (
              <Sec id={`disease-${sel.id}-notes`} icon={Sparkles} tone="ai" title="Amfi ve ders notu vurguları">
                <p className="dz-note">{sel.source_notes_summary}</p>
              </Sec>
            )}
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
