import React, { useState, useMemo, useEffect } from 'react';
import { Sheet } from '../ui/Sheet';
import { useUiVersion } from '../../utils/uiVersion';
import { PageHeader } from '../ui/PageHeader';
import { EmptySearch } from '../ui/Animations';
import {
  ChevronDown,
  Search,
  BookOpenText,
  Sparkles,
  ShieldCheck,
  AlertTriangle,
  Lightbulb,
  GraduationCap,
  Pill,
  Activity,
  Dna,
  FlaskConical,
  Tag,
  LayoutGrid,
  List as ListIcon,
  Bug,
  ArrowRight,
  ExternalLink,
  CheckCircle2,
  RefreshCw,
  X,
  ChevronRight,
  Bookmark,
  Share2,
  Stethoscope,
  Filter,
  Check,
  BrainCircuit,
  HelpCircle,
  Hash,
  Copy,
  AlertCircle,
  Send,
} from 'lucide-react';
import rawEncyclopediaData from '../../data/medical_encyclopedia.json';
import * as api from '../../services/api';
import { triggerDomHighlightAndScroll, shareDeepLink } from '../../services/universalRedirectService';

export type EncyclopediaCategory = 'all' | 'hastalik' | 'ilac' | 'patoloji' | 'patojen' | 'genetik' | 'terim' | 'protein';

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

const CATEGORY_TABS: { id: EncyclopediaCategory; label: string; icon: React.ElementType; color: string }[] = [
  { id: 'all', label: 'Tümü', icon: BookOpenText, color: 'text-ink' },
  { id: 'hastalik', label: 'Hastalıklar', icon: Activity, color: 'text-bad-text' },
  { id: 'ilac', label: 'İlaçlar & Tedavi', icon: Pill, color: 'text-accent' },
  { id: 'patoloji', label: 'Patoloji & Morfoloji', icon: Stethoscope, color: 'text-ok' },
  { id: 'patojen', label: 'Patojenler (Bakteri/Virüs)', icon: Bug, color: 'text-warn' },
  { id: 'genetik', label: 'Genetik & Gelişim', icon: Dna, color: 'text-ai' },
  { id: 'protein', label: 'Protein & Molekül', icon: FlaskConical, color: 'text-ink-2' },
  { id: 'terim', label: 'Terimler', icon: Tag, color: 'text-ink-2' },
];
/** Veride İngilizce ya da eşanlamlı gelen kategori adları tek kimliğe indirilir */
const CAT_ALIAS: Record<string, string> = { pathology: 'patoloji', genetic: 'genetik' };

const ALPHABET = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'.split('');

/** Kategori kimliği: ders renkleri (health.css .d-*) ve simge */
const CAT_TONE: Record<string, { cls: string; icon: React.ElementType; label: string }> = {
  hastalik: { cls: 'd-pat', icon: Activity, label: 'Hastalık' },
  ilac: { cls: 'd-farm', icon: Pill, label: 'İlaç & Tedavi' },
  patoloji: { cls: 'd-kardi', icon: Stethoscope, label: 'Patoloji' },
  patojen: { cls: 'd-enf', icon: Bug, label: 'Patojen' },
  genetik: { cls: 'd-gen', icon: Dna, label: 'Genetik' },
  protein: { cls: 'd-bio', icon: FlaskConical, label: 'Protein' },
  terim: { cls: 'd-ic', icon: Tag, label: 'Terim' },
};
const catTone = (c?: string) => CAT_TONE[c || ''] || { cls: 'd-ic', icon: BookOpenText, label: 'Tıbbi kavram' };
const firstLetterOf = (t?: string) => {
  const ch = String(t || '').trim().charAt(0).toLocaleUpperCase('tr-TR');
  return ALPHABET.includes(ch) ? ch : '#';
};


/** Kayıtlı yerel düzeltmeleri ham sözlük verisine uygular */
const readEntries = (): EncyclopediaEntry[] => {
  try {
    const stored = localStorage.getItem('medsoru_custom_encyclopedia_v1');
    if (stored) {
      const parsed = JSON.parse(stored) as Record<string, Partial<EncyclopediaEntry>>;
      return (rawEncyclopediaData as EncyclopediaEntry[]).map((entry) => {
        if (parsed[entry.id]) {
          return {
            ...entry,
            ...parsed[entry.id],
            aiAudit: {
              ...entry.aiAudit,
              ...(parsed[entry.id]?.aiAudit || {}),
            },
          };
        }
        return entry;
      });
    }
  } catch (e) {
    console.error('Local encyclopedia read error:', e);
  }
  return rawEncyclopediaData as EncyclopediaEntry[];
};
/** Adı boş gelen maddelere kimlikten okunur ad verir: "venoz-tromboz" → "Venöz tromboz" değil, "Venoz tromboz" (veri düzeltilene kadar) */
const withNames = (list: EncyclopediaEntry[]): EncyclopediaEntry[] =>
  list.map((e0) => {
    const c = String(e0.category || '').toLowerCase();
    const e = CAT_ALIAS[c] ? { ...e0, category: CAT_ALIAS[c] as EncyclopediaEntry['category'] } : e0;
    if (String(e.term || '').trim()) return e;
    const raw = String(e.id || '').replace(/[-_]+/g, ' ').trim();
    return { ...e, term: raw ? raw.charAt(0).toLocaleUpperCase('tr-TR') + raw.slice(1) : 'Adsız madde' };
  });


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

/** Geniş ekran mı (ana-ayrıntı düzeni) */
const useWide = () => {
  const q = '(min-width: 1024px)';
  const [wide, setWide] = React.useState(() => typeof window !== 'undefined' && window.matchMedia(q).matches);
  React.useEffect(() => {
    const m = window.matchMedia(q);
    const on = () => setWide(m.matches);
    m.addEventListener('change', on);
    return () => m.removeEventListener('change', on);
  }, []);
  return wide;
};

export const MedicalEncyclopediaView: React.FC<MedicalEncyclopediaViewProps> = ({
  initialTermId,
  onNavigateToDeck,
}) => {
  // Load database with user's local enhancements from localStorage
  const [entries, setEntries] = useState<EncyclopediaEntry[]>(() => withNames(readEntries()));

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<EncyclopediaCategory>('all');
  const [selectedKurul, setSelectedKurul] = useState<string>('Tümü');
  const [selectedDiscipline, setSelectedDiscipline] = useState<string>('Tümü');
  const [onlyAiVerified, setOnlyAiVerified] = useState(false);
  const [selectedLetter, setSelectedLetter] = useState<string | null>(null);
  // Kaydedilenler görünümü ve sıralama
  const [onlySaved, setOnlySaved] = useState(false);
  const [sortMode, setSortMode] = useState<'default' | 'az' | 'za' | 'kurul'>('default');

  // Detail Modal State
  const { isV7 } = useUiVersion();
  const [activeEntry, setActiveEntry] = useState<EncyclopediaEntry | null>(() => {
    if (initialTermId) {
      return ((rawEncyclopediaData as EncyclopediaEntry[]) || []).find((e) => e.id === initialTermId) || null;
    }
    return null;
  });

  // AI Audit State
  const [isAiAuditing, setIsAiAuditing] = useState(false);
  const [auditMessage, setAuditMessage] = useState<string | null>(null);
  const [copiedLink, setCopiedLink] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [reportingEntry, setReportingEntry] = useState<EncyclopediaEntry | null>(null);
  const [reportReason, setReportReason] = useState('Tanım / Bilgi hatalı');
  const [reportDetails, setReportDetails] = useState('');
  const [reportSuggestedAnswer, setReportSuggestedAnswer] = useState('');
  const [isSubmittingReport, setIsSubmittingReport] = useState(false);

  const handleOpenReport = (entry: EncyclopediaEntry, e?: React.MouseEvent) => {
    e?.stopPropagation();
    setReportingEntry(entry);
    setShowReportModal(true);
  };

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

      await api.ApiService.reportTerm(
        reportingEntry.id,
        reportReason,
        detailsWithAnswer,
        'Öğrenci'
      );
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

  const [bookmarkedIds, setBookmarkedIds] = useState<string[]>(() => {
    try {
      return JSON.parse(localStorage.getItem('medsoru_bookmarked_encyclopedia') || '[]');
    } catch {
      return [];
    }
  });

  // Extract unique Kuruls and Disciplines
  const availableDisciplines = useMemo(() => {
    const set = new Set<string>();
    (entries || []).forEach((e) => {
      if (e.discipline) set.add(e.discipline);
    });
    return Array.from(set).sort();
  }, [entries]);

  // Handle URL Param change & Universal Highlight
  useEffect(() => {
    if (typeof window === 'undefined') return;
    const urlParams = new URLSearchParams(window.location.search);
    const targetId = initialTermId || urlParams.get('id') || urlParams.get('term');
    const highlight = urlParams.get('highlight');

    if (targetId) {
      const found = (entries || []).find(
        (e) => e.id === targetId || e.term.toLowerCase() === targetId.toLowerCase()
      );
      if (found) {
        setActiveEntry(found);
        // Izgara görünümünde ayrıntı paneli ayrıca açılmalı (derin bağlantı yalnız kartı seçiyordu).
        setGridSheet(true);
        if (highlight) {
          setTimeout(() => triggerDomHighlightAndScroll(highlight), 600);
        }
      }
    } else if (highlight) {
      setTimeout(() => triggerDomHighlightAndScroll(highlight), 400);
    }
  }, [initialTermId, entries]);

  const toggleBookmark = (id: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    setBookmarkedIds((prev) => {
      const next = prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id];
      try {
        localStorage.setItem('medsoru_bookmarked_encyclopedia', JSON.stringify(next));
      } catch (err) {
        console.error(err);
      }
      return next;
    });
  };

  // Filtered entries
  const filteredEntries = useMemo(() => {
    const q = searchQuery.trim().toLocaleLowerCase('tr-TR');

    const list = entries.filter((e) => {
      if (onlySaved && !bookmarkedIds.includes(e.id)) return false;
      // Category
      if (selectedCategory !== 'all' && e.category !== selectedCategory) return false;

      // Kurul
      if (selectedKurul !== 'Tümü' && e.kurul !== selectedKurul) return false;

      // Discipline
      if (selectedDiscipline !== 'Tümü' && e.discipline !== selectedDiscipline) return false;

      // AI verified only
      if (onlyAiVerified && !e.aiAudit?.verified) return false;

      // Alphabet letter filter
      if (selectedLetter) {
        const firstLetter = (e.term || '')[0]?.toLocaleUpperCase('tr-TR');
        if (firstLetter !== selectedLetter) return false;
      }

      // Search Query
      if (q) {
        const matchTerm = String(e.term ?? '').toLocaleLowerCase('tr-TR').includes(q);
        const matchLatin = (e.latinName || '').toLocaleLowerCase('tr-TR').includes(q);
        const matchAliases = (e.aliases || []).some((a) => a.toLocaleLowerCase('tr-TR').includes(q));
        const matchDefn = (e.definition || '').toLocaleLowerCase('tr-TR').includes(q);
        const matchNotes = (e.lectureContextNotes || '').toLocaleLowerCase('tr-TR').includes(q);
        const matchPearls = (e.examSpotPearls || '').toLocaleLowerCase('tr-TR').includes(q);
        const matchMech = (e.morphologyOrMechanism || '').toLocaleLowerCase('tr-TR').includes(q);
        if (!matchTerm && !matchLatin && !matchAliases && !matchDefn && !matchNotes && !matchPearls && !matchMech) {
          return false;
        }
      }

      return true;
    });
    const sorted = [...list];
    const term = (e: any) => String(e?.term ?? '');
    // Varsayılan: arama yoksa alfabetik (sözlük düzeni); aramada isabet sırası korunur
    if (sortMode === 'default') {
      if (!q) sorted.sort((a, b) => term(a).localeCompare(term(b), 'tr'));
      return sorted;
    }
    if (sortMode === 'az') sorted.sort((a, b) => term(a).localeCompare(term(b), 'tr'));
    if (sortMode === 'za') sorted.sort((a, b) => term(b).localeCompare(term(a), 'tr'));
    if (sortMode === 'kurul') sorted.sort((a, b) => String(a.kurul ?? '').localeCompare(String(b.kurul ?? ''), 'tr') || term(a).localeCompare(term(b), 'tr'));
    return sorted;
  }, [entries, searchQuery, selectedCategory, selectedKurul, selectedDiscipline, onlyAiVerified, selectedLetter, onlySaved, bookmarkedIds, sortMode]);

  const wide = useWide();
  const [filtersOpen, setFiltersOpen] = useState(false);
  // Görünüm: kart ızgarası (canvas "Glossary") ya da liste + ayrıntı; cihazda hatırlanır.
  const [view, setView] = useState<'grid' | 'list'>(() => {
    try { return localStorage.getItem('medsoru_glossary_view') === 'list' ? 'list' : 'grid'; } catch { return 'grid'; }
  });
  const pickView = (v: 'grid' | 'list') => { setView(v); try { localStorage.setItem('medsoru_glossary_view', v); } catch { /* yoksay */ } };
  const [gridLimit, setGridLimit] = useState(60);
  const [gridSheet, setGridSheet] = useState(false);
  const catCount = useMemo(() => {
    const m = new Map<string, number>();
    entries.forEach((e) => m.set(String(e.category), (m.get(String(e.category)) || 0) + 1));
    return m;
  }, [entries]);
  const activeFilterCount = [selectedKurul !== 'Tümü', selectedDiscipline !== 'Tümü', sortMode !== 'default', onlyAiVerified, onlySaved].filter(Boolean).length;
  const listRef = React.useRef<HTMLDivElement>(null);
  const grouped = !searchQuery.trim() && (sortMode === 'default' || sortMode === 'az' || sortMode === 'za');
  const groups = useMemo(() => {
    if (sortMode === 'kurul') {
      const m = new Map<string, EncyclopediaEntry[]>();
      filteredEntries.forEach((e) => {
        const k = String(e.kurul || 'Diğer');
        m.set(k, [...(m.get(k) || []), e]);
      });
      return [...m.entries()].map(([k, items]) => ({ key: k.replace(/\s+/g, '-'), title: k, items }));
    }
    if (!grouped) return [{ key: 'all', title: '', items: filteredEntries }];
    const m = new Map<string, EncyclopediaEntry[]>();
    filteredEntries.forEach((e) => {
      const k = firstLetterOf(e.term);
      m.set(k, [...(m.get(k) || []), e]);
    });
    const rank = (k: string) => (k === '#' ? 999 : ALPHABET.indexOf(k));
    const out = [...m.entries()].map(([k, items]) => ({ key: k, title: k, items })).sort((a, b) => rank(a.key) - rank(b.key));
    return sortMode === 'za' ? out.reverse() : out;
  }, [filteredEntries, grouped, sortMode]);
  const letterSet = useMemo(() => new Set(grouped ? groups.map((g) => g.key) : []), [groups, grouped]);
  const jumpTo = (ch: string) => document.getElementById(`gx-${ch}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  // Geniş ekranda ilk madde kendiliğinden açık gelir (boş panel kalmasın)
  React.useEffect(() => {
    if (wide && !activeEntry && filteredEntries[0]) setActiveEntry(filteredEntries[0]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [wide, filteredEntries]);

  // Statistics
  const stats = useMemo(() => {
    const total = entries.length;
    const hastalik = entries.filter((e) => e.category === 'hastalik').length;
    const ilac = entries.filter((e) => e.category === 'ilac').length;
    const patoloji = entries.filter((e) => e.category === 'patoloji').length;
    const patojen = entries.filter((e) => e.category === 'patojen').length;
    const genetik = entries.filter((e) => e.category === 'genetik').length;
    const verified = entries.filter((e) => e.aiAudit?.verified).length;
    return { total, hastalik, ilac, patoloji, patojen, genetik, verified };
  }, [entries]);

  // Run AI Audit on active entry
  const handleRunAiAudit = async (entry: EncyclopediaEntry) => {
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

      const updatedEntry: EncyclopediaEntry = {
        ...entry,
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

      // Persist to state and localStorage
      setEntries((prev) => prev.map((e) => (e.id === entry.id ? updatedEntry : e)));
      setActiveEntry(updatedEntry);

      // Save custom updates
      try {
        const stored = JSON.parse(localStorage.getItem('medsoru_custom_encyclopedia_v1') || '{}');
        stored[entry.id] = updatedEntry;
        localStorage.setItem('medsoru_custom_encyclopedia_v1', JSON.stringify(stored));
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
  };

  const copyShareLink = async (entry: EncyclopediaEntry, subTarget?: string) => {
    await shareDeepLink({
      type: 'term',
      id: entry.id,
      subTarget,
    });
    setCopiedLink(true);
    setTimeout(() => setCopiedLink(false), 2000);
  };

  const getCategoryBadge = (cat: string) => {
    switch (cat) {
      case 'hastalik':
        return { label: 'Hastalık', dot: 'bg-bad', cls: 'bg-bad/10 text-bad-text dark:text-rose-300 border-bad/20' };
      case 'ilac':
        return { label: 'İlaç & Tedavi', dot: 'bg-accent', cls: 'bg-accent/10 text-accent dark:text-blue-300 border-accent/20' };
      case 'patoloji':
        return { label: 'Patoloji', dot: 'bg-ok', cls: 'bg-ok/10 text-ok dark:text-emerald-300 border-ok/20' };
      case 'patojen':
        return { label: 'Patojen', dot: 'bg-warn', cls: 'bg-warn/10 text-warn dark:text-amber-300 border-warn/20' };
      case 'genetik':
        return { label: 'Genetik', dot: 'bg-ai', cls: 'bg-ai/10 text-ai dark:text-purple-300 border-ai/20' };
      default:
        return { label: 'Tıbbi Kavram', dot: 'bg-ok', cls: 'bg-ok/10 text-ok dark:text-teal-300 border-ok/20' };
    }
  };

  const detailPanel = activeEntry ? (
          <div className={wide || isV7 ? 'gx-pane flex flex-col overflow-hidden' : 'ds-modal w-full max-w-[720px] flex flex-col max-h-[92dvh] overflow-hidden'}>
            {/* Modal Header */}
            <div className="ds-modal-head">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2 flex-wrap mb-1.5">
                  <span className="ms-tag is-new">
                    {getCategoryBadge(activeEntry.category).label}
                  </span>
                  <span className="ms-tag">
                    {activeEntry.kurul} • {activeEntry.discipline}
                  </span>
                  {activeEntry.aiAudit?.verified && (
                    <span className="ms-tag is-ok">
                      <ShieldCheck aria-hidden />
                      <span>{activeEntry.uretici === 's13_study' ? 'Ders notuyla doğrulandı' : 'AI Onaylı'} {typeof activeEntry.aiAudit.accuracyScore === 'number' ? ` (%${activeEntry.aiAudit.accuracyScore})` : ''}</span>
                    </span>
                  )}
                </div>

                <h2 className="m-0 font-display text-xl sm:text-2xl font-bold tracking-[-0.02em] text-ink leading-tight">
                  {activeEntry.term}
                </h2>
                {activeEntry.latinName && (
                  <p className="m-0 text-sm text-ink-3 italic mt-0.5">
                    {activeEntry.latinName}
                  </p>
                )}
              </div>

              {/* Close & Action Buttons */}
              <div className="flex items-center gap-1.5 shrink-0">
                <button
                  type="button"
                  onClick={() => toggleBookmark(activeEntry.id)}
                  className="ms-btn is-icon is-ghost"
                  title="Kaydet"
                >
                  <Bookmark
                    fill={bookmarkedIds.includes(activeEntry.id) ? 'currentColor' : 'none'}
                  />
                </button>
                <button
                  type="button"
                  onClick={() => copyShareLink(activeEntry)}
                  className="ms-btn is-icon is-ghost"
                  title="Bağlantıyı Kopyala / Paylaş"
                >
                  {copiedLink ? <Check className="text-ok" /> : <Share2 />}
                </button>
                <button
                  type="button"
                  onClick={(e) => handleOpenReport(activeEntry, e)}
                  className="ms-btn is-icon is-ghost text-warn hover:text-warn"
                  title="Bu terim için hata bildir"
                >
                  <AlertCircle />
                </button>
                {!wide && (
                <button
                  type="button"
                  onClick={() => setActiveEntry(null)}
                  className="ms-btn is-icon is-ghost"
                  title="Kapat (Esc)"
                >
                  <X />
                </button>
                )}
              </div>
            </div>

            {/* Modal Body Content (Scrollable) */}
            <div className="ds-modal-body">
              {/* Notification if AI Audited recently */}
              {auditMessage && (
                <div className="ds-callout is-note">
                  <Sparkles className="w-4 h-4 shrink-0" />
                  <span>{auditMessage}</span>
                </div>
              )}

              {/* 1. Orijinal Ders Notu Bağlamı (Prof/Slayt Notu) */}
              {activeEntry.lectureContextNotes && (
                <div id={`term-${activeEntry.id}-lecture`} className="ds-callout is-clinic">
                  <div className="flex flex-col gap-0.5 min-w-0">
                    <span className="ds-callout-t">
                      <GraduationCap aria-hidden />
                      <span>Ders notu</span>
                    </span>
                    {activeEntry.instructorAndSource && (
                      <span className="text-sm text-ink-3 [overflow-wrap:anywhere]">
                        {activeEntry.instructorAndSource.replace(/\.txt\b/gi, '').replace(/^\d+\)\s*/, '')}
                      </span>
                    )}
                  </div>
                  <div className="m-0">
                    <RichField value={activeEntry.lectureContextNotes as unknown} />
                  </div>
                </div>
              )}

              {/* 2. Tanım */}
              <div id={`term-${activeEntry.id}-def`} className="flex flex-col gap-1">
                <span className="ds-label">Tanım</span>
                <div className="m-0 text-md text-ink leading-[1.6]">
                  <RichField value={activeEntry.definition as unknown} />
                </div>
              </div>

              {/* 3. Patoloji, Morfoloji ve Etki Mekanizması */}
              {activeEntry.morphologyOrMechanism && (
                <div id={`term-${activeEntry.id}-mech`} className="ds-callout">
                  <span className="ds-callout-t">
                    <Stethoscope aria-hidden />
                    <span>Patoloji, morfoloji ve mekanizma</span>
                  </span>
                  <div className="m-0 whitespace-pre-line">
                    <RichField value={activeEntry.morphologyOrMechanism as unknown} />
                  </div>
                </div>
              )}

              {/* 4. Ayırıcı Tanı Kriterleri */}
              {activeEntry.differentialDiagnosis && (
                <div id={`term-${activeEntry.id}-diff`} className="ds-callout is-note">
                  <span className="ds-callout-t">
                    <Filter aria-hidden />
                    <span>Ayırıcı tanı</span>
                  </span>
                  <div className="m-0">
                    <RichField value={activeEntry.differentialDiagnosis as unknown} />
                  </div>
                </div>
              )}

              {/* 5. Sınav Tuzağı & Dikkat Edilmesi Gerekenler */}
              {activeEntry.pitfallsAndWarnings && (
                <div id={`term-${activeEntry.id}-pitfalls`} className="ds-callout is-bad">
                  <span className="ds-callout-t">
                    <AlertTriangle aria-hidden />
                    <span>Sınav tuzağı</span>
                  </span>
                  <div className="m-0">
                    <RichField value={activeEntry.pitfallsAndWarnings as unknown} />
                  </div>
                </div>
              )}

              {/* 6. Hoca İncisi & Sınav Spotları */}
              {activeEntry.examSpotPearls && (
                <div id={`term-${activeEntry.id}-pearls`} className="ds-callout is-important">
                  <span className="ds-callout-t">
                    <Lightbulb aria-hidden />
                    <span>Sınav spotu</span>
                  </span>
                  <div className="m-0">
                    <RichField value={activeEntry.examSpotPearls as unknown} />
                  </div>
                </div>
              )}

              {/* 7. İlişkili Kavramlar (Clickable Chips) */}
              {activeEntry.relatedItems && activeEntry.relatedItems.length > 0 && (
                <div className="flex flex-col gap-1.5 pt-2 border-t border-line-soft">
                  <span className="ds-label">İlişkili maddeler</span>
                  <div className="flex items-center gap-1.5 flex-wrap">
                    {activeEntry.relatedItems.map((relId) => {
                      const rel = (entries || []).find((e) => e.id === relId);
                      return (
                        <button
                          key={relId}
                          type="button"
                          onClick={() => {
                            if (rel) setActiveEntry(rel);
                          }}
                          className="ms-btn is-outline is-sm"
                        >
                          <Hash aria-hidden />
                          <span>{rel ? rel.term : relId}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* 8. Örnek TUS / Komite Soru Kutusu */}
              {activeEntry.aiAudit?.sampleExamQuestion && (
                <div className="ds-callout">
                  <span className="ds-callout-t">
                    <HelpCircle aria-hidden />
                    <span>Örnek sınav sorusu</span>
                  </span>
                  <p className="m-0">
                    {activeEntry.aiAudit.sampleExamQuestion}
                  </p>
                </div>
              )}
            </div>

            {/* Modal Footer with AI Audit Action */}
            <div className="ds-modal-foot">
              <div className="ds-modal-note">
                <BrainCircuit aria-hidden />
                <span>
                  Doğrulama:{' '}
                  <strong className="text-ink">
                    {activeEntry.aiAudit?.verified ? `Doğrulandı${typeof activeEntry.aiAudit.accuracyScore === 'number' ? ` (%${activeEntry.aiAudit.accuracyScore})` : ''}` : 'Beklemede'}
                  </strong>
                </span>
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  disabled={isAiAuditing}
                  onClick={() => handleRunAiAudit(activeEntry)}
                  className="ms-btn is-primary w-full sm:w-auto"
                >
                  <RefreshCw className={isAiAuditing ? 'animate-spin' : ''} aria-hidden />
                  <span>{isAiAuditing ? 'Yapay zekâ denetliyor…' : 'Yapay zekâyla denetle'}</span>
                </button>
              </div>
            </div>
          </div>
  ) : null;

  return (
    <div className="ds-page">
      <PageHeader
        eyebrow="Müfredat kütüphanesi"
        title="Sözlük"
        description="Ders notlarından derlenen hastalıklar, bulgular, ilaçlar ve patojenler."
        stats={[{ label: 'madde', value: stats.total }]}
      />

      {/* Arama + hızlı süzgeçler */}
      <div className="ds-filters">
        <label className="cx-search">
          <Search aria-hidden />
          <input
            type="search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Hastalık, ilaç, bulgu ya da gen ara (RHK, VHL, apoptoz…)"
            aria-label="Sözlükte ara"
          />
          {searchQuery && (
            <button type="button" onClick={() => setSearchQuery('')} className="cx-search-x" aria-label="Aramayı temizle">
              <X aria-hidden />
            </button>
          )}
        </label>
        <button type="button" className={`ms-btn is-sm gx-ftoggle ${activeFilterCount ? 'is-tonal' : ''}`} onClick={() => setFiltersOpen((v) => !v)} aria-expanded={filtersOpen}>
          <Filter aria-hidden /> Süzgeç{activeFilterCount ? ` · ${activeFilterCount}` : ''}
        </button>
        <div className={`ds-toolbar gx-filters ${filtersOpen ? 'is-open' : ''}`}>
          <label className="ds-select">
            <span>Kurul</span>
            <select value={selectedKurul} onChange={(e) => setSelectedKurul(e.target.value)} aria-label="Kurul">
              <option value="Tümü">Tümü</option>
              <option value="Kurul 1">Kurul 1</option>
              <option value="Kurul 2">Kurul 2</option>
              <option value="Kurul 3">Kurul 3</option>
            </select>
            <ChevronDown aria-hidden />
          </label>
          <label className="ds-select">
            <span>Branş</span>
            <select value={selectedDiscipline} onChange={(e) => setSelectedDiscipline(e.target.value)} aria-label="Branş">
              <option value="Tümü">Tümü</option>
              {availableDisciplines.map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
            <ChevronDown aria-hidden />
          </label>
          <label className="ds-select">
            <span>Sırala</span>
            <select value={sortMode} onChange={(e) => setSortMode(e.target.value as any)} aria-label="Sırala">
              <option value="default">Önerilen</option>
              <option value="az">A → Z</option>
              <option value="za">Z → A</option>
              <option value="kurul">Kurula göre</option>
            </select>
            <ChevronDown aria-hidden />
          </label>
          <span className="ds-grow" />
          <button
            type="button"
            onClick={() => setOnlyAiVerified((prev) => !prev)}
            aria-pressed={onlyAiVerified}
            className={`ms-btn ${onlyAiVerified ? 'is-tonal' : 'is-outline'}`}
            title="Yalnızca denetlenmiş maddeleri göster"
          >
            <ShieldCheck aria-hidden /> Doğrulanmış
          </button>
          <button
            type="button"
            onClick={() => setOnlySaved((v) => !v)}
            aria-pressed={onlySaved}
            className={`ms-btn ${onlySaved ? 'is-tonal' : 'is-outline'}`}
            title="Yalnızca kaydettiğin terimleri göster"
          >
            <Bookmark fill={onlySaved ? 'currentColor' : 'none'} aria-hidden /> Kaydedilenler <small className="ds-n">{bookmarkedIds.length}</small>
          </button>
        </div>

        {/* Kategoriler: ikonlu, sayılı (canvas "Glossary") */}
        <div className="gl-cats" role="radiogroup" aria-label="Kategori">
          {CATEGORY_TABS.filter((tab) => tab.id === 'all' || catCount.get(tab.id)).map((tab) => {
            const isSelected = selectedCategory === tab.id;
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                type="button"
                role="radio"
                aria-checked={isSelected}
                onClick={() => { setSelectedCategory(tab.id); setSelectedLetter(null); setGridLimit(60); }}
                className={`gl-cat ${isSelected ? 'is-on' : ''}`}
              >
                <span className="gl-ci" aria-hidden><Icon /></span>
                {tab.label}
                <span className="gl-n">{tab.id === 'all' ? entries.length : catCount.get(tab.id) || 0}</span>
              </button>
            );
          })}
        </div>

        {/* Harf dizini */}
        <div className="ds-alpha" role="group" aria-label="Harfe göre">
          {ALPHABET.map((char) => (
            <button key={char} type="button" onClick={() => jumpTo(char)} disabled={!letterSet.has(char)} aria-label={`${char} harfine git`}>
              {char}
            </button>
          ))}
        </div>
      </div>

      {/* Sonuç satırı */}
      <div className="ds-resultbar">
        <span className="rb-viewseg gl-view" role="radiogroup" aria-label="Görünüm">
          <button type="button" role="radio" aria-checked={view === 'grid'} aria-label="Kart görünümü" title="Kartlar" onClick={() => pickView('grid')}><LayoutGrid /></button>
          <button type="button" role="radio" aria-checked={view === 'list'} aria-label="Liste görünümü" title="Liste" onClick={() => pickView('list')}><ListIcon /></button>
        </span>
        <span>
          <b>{filteredEntries.length}</b> madde
          {searchQuery && <> · “{searchQuery}”</>}
          {selectedLetter && <> · {selectedLetter} harfi</>}
        </span>
        {(searchQuery || selectedCategory !== 'all' || selectedKurul !== 'Tümü' || selectedDiscipline !== 'Tümü' || selectedLetter !== null || onlyAiVerified || onlySaved) && (
          <button
            type="button"
            onClick={() => {
              setSearchQuery('');
              setSelectedCategory('all');
              setSelectedKurul('Tümü');
              setSelectedDiscipline('Tümü');
              setSelectedLetter(null);
              setOnlyAiVerified(false);
              setOnlySaved(false);
            }}
            className="cx-clear"
          >
            Süzgeçleri temizle
          </button>
        )}
      </div>

      {/* Ana-ayrıntı: solda A–Z liste, sağda seçili madde */}
      {filteredEntries.length === 0 ? (
        <div className="ds-empty is-panel">
          <EmptySearch size={64} />
          <b>Eşleşen madde yok</b>
          <span>Farklı bir terim dene ya da süzgeçleri temizle.</span>
          <button
            type="button"
            onClick={() => {
              setSearchQuery('');
              setSelectedCategory('all');
              setSelectedLetter(null);
            }}
            className="ms-btn is-tonal is-sm"
          >
            Tüm maddeleri göster
          </button>
        </div>
      ) : view === 'grid' ? (
        <div className="gl-grid-wrap">
          <ul className="gl-grid">
            {filteredEntries.slice(0, gridLimit).map((entry) => {
              const tone = catTone(entry.category);
              const Icon = tone.icon;
              const saved = bookmarkedIds.includes(entry.id);
              return (
                <li key={entry.id} id={`term-${entry.id}`} className={tone.cls}>
                  <button type="button" className="gl-card" onClick={() => { setActiveEntry(entry); setGridSheet(true); }}>
                    <span className="gl-card-h">
                      <b>{entry.term}</b>
                      {entry.aiAudit?.verified && <ShieldCheck className="gl-ok" aria-label="Doğrulanmış" />}
                      {saved && <Bookmark className="gl-saved" fill="currentColor" aria-label="Kaydedildi" />}
                    </span>
                    {entry.latinName && <i className="gl-latin">{entry.latinName}</i>}
                    <span className="gl-def">{entry.definition}</span>
                    <span className="gl-tags">
                      <span className="gl-type"><Icon aria-hidden />{tone.label}</span>
                      {entry.kurul && <span className="gl-tag">{String(entry.kurul).replace('Kurul ', 'K')}</span>}
                      {entry.discipline && <span className="gl-tag">{entry.discipline}</span>}
                    </span>
                  </button>
                </li>
              );
            })}
          </ul>
          {filteredEntries.length > gridLimit && (
            <button type="button" className="os-btn gl-more" onClick={() => setGridLimit((n) => n + 60)}>
              {Math.min(60, filteredEntries.length - gridLimit)} madde daha göster
            </button>
          )}
        </div>
      ) : (
        <div className="gx">
          <div className="gx-list" ref={listRef}>
            {groups.map((g) => (
              <section key={g.key} className="gx-group" id={`gx-${g.key}`}>
                {g.title && <h3 className="gx-letter">{g.title}</h3>}
                <ul>
                  {g.items.map((entry) => {
                    const tone = catTone(entry.category);
                    const Icon = tone.icon;
                    const on = activeEntry?.id === entry.id;
                    const saved = bookmarkedIds.includes(entry.id);
                    return (
                      <li key={entry.id} id={`term-${entry.id}`} className={tone.cls}>
                        <div className="flex items-center w-full">
                          <button type="button" onClick={() => setActiveEntry(entry)} aria-current={on ? 'true' : undefined} className={`gx-row flex-1 ${on ? 'is-on' : ''}`}>
                            <span className="hk-tile is-sm"><Icon aria-hidden /></span>
                            <span className="gx-row-t">
                              <b>
                                {entry.term}
                                {entry.aiAudit?.verified && <ShieldCheck className="gx-ok" aria-label="Doğrulanmış" />}
                              </b>
                              <span>{entry.latinName || entry.definition}</span>
                            </span>
                            {saved && <Bookmark className="gx-saved" fill="currentColor" aria-label="Kaydedildi" />}
                            <span className="gx-kurul">{String(entry.kurul || '').replace('Kurul ', 'K')}</span>
                          </button>
                          <div className="flex items-center gap-1 shrink-0 px-2">
                            <button
                              type="button"
                              onClick={(e) => {
                                e.stopPropagation();
                                copyShareLink(entry);
                              }}
                              className="p-1.5 rounded-lg text-ink-3 hover:text-accent hover:bg-canvas-subtle transition-colors cursor-pointer"
                              title="Bağlantıyı Paylaş"
                              aria-label="Paylaş"
                            >
                              <Share2 className="w-3.5 h-3.5" />
                            </button>
                            <button
                              type="button"
                              onClick={(e) => handleOpenReport(entry, e)}
                              className="p-1.5 rounded-lg text-ink-3 hover:text-warn hover:bg-canvas-subtle transition-colors cursor-pointer"
                              title="Hata Bildir"
                              aria-label="Hata bildir"
                            >
                              <AlertCircle className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>
                      </li>
                    );
                  })}
                </ul>
              </section>
            ))}
          </div>
          {wide && (
            <aside className="gx-detail" aria-label="Madde ayrıntısı">
              {activeEntry ? detailPanel : (
                <div className="gx-placeholder">
                  <BookOpenText aria-hidden />
                  <b>Bir madde seç</b>
                  <span>Tanım, ders notu, ayırıcı tanı ve sınav spotları burada açılır.</span>
                </div>
              )}
            </aside>
          )}
        </div>
      )}

      {/* ========================================================= */}
      {/* DETAYLI ANSİKLOPEDİ MODAL / SLIDE-OVER                    */}
      {/* ========================================================= */}
      {(!wide || view === 'grid') && isV7 && (
        <Sheet open={!!activeEntry && (view === 'list' || gridSheet)} onClose={() => { setActiveEntry(null); setGridSheet(false); }} label={activeEntry?.term || 'Madde'} size="full" width={720} bare>
          {detailPanel}
        </Sheet>
      )}
      {activeEntry && !wide && !isV7 && (
        <div
          className="ms-overlay ds-modal-wrap fixed inset-0 z-[70] flex items-end sm:items-center justify-center sm:p-4"
          role="dialog"
          aria-modal="true"
        >
          {detailPanel}
        </div>
      )}

      {showReportModal && reportingEntry && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-white dark:bg-[#12161f] border border-line rounded-2xl w-full max-w-lg shadow-xl overflow-hidden flex flex-col max-h-[90vh]">
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
      )}
    </div>
  );
};
