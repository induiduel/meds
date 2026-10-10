import React, { useState, useMemo, useEffect } from 'react';
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
  Copy
} from 'lucide-react';
import rawEncyclopediaData from '../../data/medical_encyclopedia.json';
import { callClientResilientAi } from '../../services/api';

export type EncyclopediaCategory = 'all' | 'hastalik' | 'ilac' | 'patoloji' | 'patojen' | 'genetik';

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
];

const ALPHABET = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'.split('');

/** Kategori kimliği: ders renkleri (health.css .d-*) ve simge */
const CAT_TONE: Record<string, { cls: string; icon: React.ElementType; label: string }> = {
  hastalik: { cls: 'd-pat', icon: Activity, label: 'Hastalık' },
  ilac: { cls: 'd-farm', icon: Pill, label: 'İlaç & Tedavi' },
  patoloji: { cls: 'd-kardi', icon: Stethoscope, label: 'Patoloji' },
  patojen: { cls: 'd-enf', icon: Bug, label: 'Patojen' },
  genetik: { cls: 'd-gen', icon: Dna, label: 'Genetik' },
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
  list.map((e) => {
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

  // Handle URL Param change
  useEffect(() => {
    if (initialTermId) {
      const found = (entries || []).find((e) => e.id === initialTermId);
      if (found) setActiveEntry(found);
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

      const res = await callClientResilientAi({
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

  const copyShareLink = (entry: EncyclopediaEntry) => {
    const url = `${window.location.origin}/sozluk?id=${entry.id}`;
    navigator.clipboard?.writeText(url).then(() => {
      setCopiedLink(true);
      setTimeout(() => setCopiedLink(false), 2000);
    });
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
          <div className={wide ? 'gx-pane flex flex-col overflow-hidden' : 'ds-modal w-full max-w-[720px] flex flex-col max-h-[92dvh] overflow-hidden'}>
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
                      <span>{activeEntry.uretici === 's13_study' ? 'Ders notuyla doğrulandı' : 'AI Onaylı'} (%{activeEntry.aiAudit.accuracyScore})</span>
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
                  title="Bağlantıyı Kopyala"
                >
                  {copiedLink ? <Check className="text-ok" /> : <Share2 />}
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
                <div className="ds-callout is-clinic">
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
              <div className="flex flex-col gap-1">
                <span className="ds-label">Tanım</span>
                <div className="m-0 text-md text-ink leading-[1.6]">
                  <RichField value={activeEntry.definition as unknown} />
                </div>
              </div>

              {/* 3. Patoloji, Morfoloji ve Etki Mekanizması */}
              {activeEntry.morphologyOrMechanism && (
                <div className="ds-callout">
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
                <div className="ds-callout is-note">
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
                <div className="ds-callout is-bad">
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
                <div className="ds-callout is-important">
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
                    {activeEntry.aiAudit?.verified ? `Doğrulandı (%${activeEntry.aiAudit.accuracyScore})` : 'Beklemede'}
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
        title="Sözlük & Ansiklopedi"
        description="Ders notlarından derlenen hastalıklar, patoloji bulguları, ilaçlar ve patojenler. Her madde amfi notu bağlamında korunur."
        stats={[
          { label: 'Toplam madde', value: stats.total },
          { label: 'Denetlenmiş', value: `%${stats.total ? Math.round((stats.verified / stats.total) * 100) : 0}`, tone: 'ok' },
        ]}
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

        {/* Kategori sekmeleri */}
        <div className="cx-tabs" role="tablist" aria-label="Kategori">
          {CATEGORY_TABS.map((tab) => {
            const isSelected = selectedCategory === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                role="tab"
                aria-selected={isSelected}
                onClick={() => {
                  setSelectedCategory(tab.id);
                  setSelectedLetter(null);
                }}
                className={`cx-tab ${isSelected ? 'is-on' : ''}`}
              >
                {tab.label}
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
                      <li key={entry.id} className={tone.cls}>
                        <button type="button" onClick={() => setActiveEntry(entry)} aria-current={on ? 'true' : undefined} className={`gx-row ${on ? 'is-on' : ''}`}>
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
      {activeEntry && !wide && (
        <div
          className="ms-overlay ds-modal-wrap fixed inset-0 z-[70] flex items-end sm:items-center justify-center sm:p-4"
          role="dialog"
          aria-modal="true"
        >
          {detailPanel}
        </div>
      )}
    </div>
  );
};
