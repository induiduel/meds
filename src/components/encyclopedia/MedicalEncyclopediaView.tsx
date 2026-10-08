import React, { useState, useMemo, useEffect } from 'react';
import { PageHeader } from '../ui/PageHeader';
import {
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
  { id: 'hastalik', label: 'Hastalıklar', icon: Activity, color: 'text-rose-600' },
  { id: 'ilac', label: 'İlaçlar & Tedavi', icon: Pill, color: 'text-blue-600' },
  { id: 'patoloji', label: 'Patoloji & Morfoloji', icon: Stethoscope, color: 'text-emerald-600' },
  { id: 'patojen', label: 'Patojenler (Bakteri/Virüs)', icon: Bug, color: 'text-amber-600' },
  { id: 'genetik', label: 'Genetik & Gelişim', icon: Dna, color: 'text-purple-600' },
];

const ALPHABET = 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ'.split('');

export const MedicalEncyclopediaView: React.FC<MedicalEncyclopediaViewProps> = ({
  initialTermId,
  onNavigateToDeck,
}) => {
  // Load database with user's local enhancements from localStorage
  const [entries, setEntries] = useState<EncyclopediaEntry[]>(() => {
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
  });

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
    if (sortMode === 'default') return list;
    const sorted = [...list];
    const term = (e: any) => String(e?.term ?? '');
    if (sortMode === 'az') sorted.sort((a, b) => term(a).localeCompare(term(b), 'tr'));
    if (sortMode === 'za') sorted.sort((a, b) => term(b).localeCompare(term(a), 'tr'));
    if (sortMode === 'kurul') sorted.sort((a, b) => String(a.kurul ?? '').localeCompare(String(b.kurul ?? ''), 'tr') || term(a).localeCompare(term(b), 'tr'));
    return sorted;
  }, [entries, searchQuery, selectedCategory, selectedKurul, selectedDiscipline, onlyAiVerified, selectedLetter, onlySaved, bookmarkedIds, sortMode]);

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
        return { label: 'Hastalık', dot: 'bg-rose-500', cls: 'bg-rose-500/10 text-rose-700 dark:text-rose-300 border-rose-500/20' };
      case 'ilac':
        return { label: 'İlaç & Tedavi', dot: 'bg-blue-500', cls: 'bg-blue-500/10 text-blue-700 dark:text-blue-300 border-blue-500/20' };
      case 'patoloji':
        return { label: 'Patoloji', dot: 'bg-emerald-500', cls: 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border-emerald-500/20' };
      case 'patojen':
        return { label: 'Patojen', dot: 'bg-amber-500', cls: 'bg-amber-500/10 text-amber-700 dark:text-amber-300 border-amber-500/20' };
      case 'genetik':
        return { label: 'Genetik', dot: 'bg-purple-500', cls: 'bg-purple-500/10 text-purple-700 dark:text-purple-300 border-purple-500/20' };
      default:
        return { label: 'Tıbbi Kavram', dot: 'bg-teal-500', cls: 'bg-teal-500/10 text-teal-700 dark:text-teal-300 border-teal-500/20' };
    }
  };

  return (
    <div className="w-full min-w-0 text-ink pb-8">
      <PageHeader
        className="mb-5"
        eyebrow="Müfredat kütüphanesi"
        title="Sözlük & Ansiklopedi"
        description="Ders notlarından derlenen hastalıklar, patoloji bulguları, ilaçlar ve patojenler. Her madde amfi notu bağlamında korunur."
        stats={[
          { label: 'Toplam madde', value: stats.total },
          { label: 'Denetlenmiş', value: `%${stats.total ? Math.round((stats.verified / stats.total) * 100) : 0}`, tone: 'ok' },
        ]}
      />

      {/* Search and Filter Bar */}
      <div className="bg-white border border-line rounded-2xl p-3 sm:p-4 shadow-xs mb-5 flex flex-col gap-3">
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5">
          {/* Main Search Input */}
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-ink-3 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Hastalık, ilaç, patoloji bulgusu, genetik mutasyon veya hoca notu ara (örn. RHK, VHL, Benzatin, Apoptoz)..."
              className="w-full pl-10 pr-9 py-2.5 text-[14px] bg-canvas border border-line rounded-xl outline-none focus:border-accent focus:ring-2 focus:ring-accent/10 transition-all placeholder:text-ink-3"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-3 hover:text-ink p-1 cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Quick Selects */}
          <div className="flex flex-wrap items-center gap-2 [&>select]:min-w-0 [&>select]:flex-1">
            <select
              value={selectedKurul}
              onChange={(e) => setSelectedKurul(e.target.value)}
              className="px-3 py-2.5 text-[13px] font-medium bg-canvas border border-line rounded-xl outline-none text-ink cursor-pointer hover:border-accent/40"
            >
              <option value="Tümü">Tüm Kurullar</option>
              <option value="Kurul 1">Kurul 1</option>
              <option value="Kurul 2">Kurul 2</option>
              <option value="Kurul 3">Kurul 3</option>
            </select>

            <select
              value={selectedDiscipline}
              onChange={(e) => setSelectedDiscipline(e.target.value)}
              className="px-3 py-2.5 text-[13px] font-medium bg-canvas border border-line rounded-xl outline-none text-ink cursor-pointer hover:border-accent/40 max-w-[150px] truncate"
            >
              <option value="Tümü">Tüm Branşlar</option>
              {availableDisciplines.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>

            <button
              type="button"
              onClick={() => setOnlyAiVerified((prev) => !prev)}
              className={`px-3 py-2.5 text-[12.5px] font-semibold rounded-xl border transition-all flex items-center gap-1.5 cursor-pointer shrink-0 ${
                onlyAiVerified
                  ? 'bg-emerald-500 text-white border-emerald-600 shadow-2xs'
                  : 'bg-canvas text-ink-2 border-line hover:border-accent/40'
              }`}
              title="Yalnızca yapay zeka tarafından denetlenmiş maddeleri göster"
            >
              <ShieldCheck className="w-4 h-4" />
              <span className="hidden md:inline">Doğrulanmış</span>
            </button>

            <button
              type="button"
              onClick={() => setOnlySaved((v) => !v)}
              aria-pressed={onlySaved}
              className={`px-3 py-2.5 text-[12.5px] font-semibold rounded-xl border transition-all flex items-center gap-1.5 cursor-pointer shrink-0 ${
                onlySaved ? 'bg-amber-500 text-white border-amber-600' : 'bg-canvas text-ink-2 border-line hover:border-accent/40'
              }`}
              title="Yalnızca kaydettiğin terimleri göster"
            >
              <Bookmark className="w-4 h-4" fill={onlySaved ? 'currentColor' : 'none'} />
              <span>Kaydedilenler</span>
              <span className="tabular-nums opacity-80">{bookmarkedIds.length}</span>
            </button>

            <select
              value={sortMode}
              onChange={(e) => setSortMode(e.target.value as any)}
              aria-label="Sırala"
              title="Sırala"
              className="px-3 py-2.5 text-[13px] font-medium bg-canvas border border-line rounded-xl outline-none text-ink cursor-pointer hover:border-accent/40"
            >
              <option value="default">Sıralama: önerilen</option>
              <option value="az">A → Z</option>
              <option value="za">Z → A</option>
              <option value="kurul">Kurula göre</option>
            </select>
          </div>
        </div>

        {/* Category Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none">
          {CATEGORY_TABS.map((tab) => {
            const Icon = tab.icon;
            const isSelected = selectedCategory === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                onClick={() => {
                  setSelectedCategory(tab.id);
                  setSelectedLetter(null);
                }}
                className={`px-3 py-1.5 rounded-lg text-[12.5px] font-semibold transition-all flex items-center gap-1.5 whitespace-nowrap cursor-pointer ${
                  isSelected
                    ? 'bg-accent text-white shadow-2xs'
                    : 'bg-canvas text-ink-2 hover:bg-canvas-2 border border-line/60'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isSelected ? 'text-white' : tab.color}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Alphabet Jump Bar */}
        <div className="pt-2 border-t border-line/60 flex items-center gap-1 overflow-x-auto scrollbar-none text-[11.5px] font-mono font-bold text-ink-3">
          <button
            type="button"
            onClick={() => setSelectedLetter(null)}
            className={`px-2 py-0.5 rounded cursor-pointer ${
              selectedLetter === null ? 'bg-accent text-white' : 'hover:text-accent'
            }`}
          >
            TÜMÜ
          </button>
          {ALPHABET.map((char) => (
            <button
              key={char}
              type="button"
              onClick={() => setSelectedLetter(selectedLetter === char ? null : char)}
              className={`w-6 h-6 rounded flex items-center justify-center cursor-pointer transition-colors ${
                selectedLetter === char ? 'bg-accent text-white' : 'hover:bg-accent-soft hover:text-accent'
              }`}
            >
              {char}
            </button>
          ))}
        </div>
      </div>

      {/* Result Count and Active Filters Bar */}
      <div className="flex items-center justify-between gap-2 px-1 mb-4 text-[12.5px] text-ink-3">
        <div>
          <span className="font-semibold text-ink">{filteredEntries.length}</span> tıbbi terim ve hastalık listeleniyor
          {searchQuery && (
            <span>
              {' '}
              • "<strong>{searchQuery}</strong>" araması
            </span>
          )}
          {selectedLetter && (
            <span>
              {' '}
              • "<strong>{selectedLetter}</strong>" harfi
            </span>
          )}
        </div>

        {(searchQuery || selectedCategory !== 'all' || selectedKurul !== 'Tümü' || selectedDiscipline !== 'Tümü' || selectedLetter !== null || onlyAiVerified) && (
          <button
            type="button"
            onClick={() => {
              setSearchQuery('');
              setSelectedCategory('all');
              setSelectedKurul('Tümü');
              setSelectedDiscipline('Tümü');
              setSelectedLetter(null);
              setOnlyAiVerified(false);
            }}
            className="text-accent hover:underline font-semibold cursor-pointer"
          >
            Filtreleri Sıfırla
          </button>
        )}
      </div>

      {/* Grid of Encyclopedia Entries */}
      {filteredEntries.length === 0 ? (
        <div className="text-center py-16 bg-white dark:bg-panel border border-line rounded-2xl p-6">
          <BookOpenText className="w-12 h-12 text-ink-3 opacity-40 mx-auto mb-3" />
          <h3 className="text-[17px] font-bold text-ink mb-1">Aramanızla Eşleşen Madde Bulunamadı</h3>
          <p className="text-[13.5px] text-ink-2 max-w-md mx-auto mb-4">
            "{searchQuery}" araması için sonuç bulunamadı. Farklı bir terim deneyebilir veya filtreleri temizleyebilirsiniz.
          </p>
          <button
            type="button"
            onClick={() => {
              setSearchQuery('');
              setSelectedCategory('all');
              setSelectedLetter(null);
            }}
            className="px-4 py-2 rounded-xl bg-accent text-white text-[13px] font-semibold cursor-pointer shadow-2xs"
          >
            Tüm Maddeleri Göster
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {filteredEntries.map((entry) => {
            const badge = getCategoryBadge(entry.category);
            const isBookmarked = bookmarkedIds.includes(entry.id);

            return (
              <div
                key={entry.id}
                onClick={() => setActiveEntry(entry)}
                className="group rounded-2xl border border-line hover:border-line-2 bg-white p-4 flex flex-col transition-colors cursor-pointer min-w-0"
              >
                <div className="flex items-center gap-2 text-[12px] text-ink-3 min-w-0">
                  <span className={`shrink-0 w-1.5 h-1.5 rounded-full ${badge.dot}`} aria-hidden="true" />
                  <span className="truncate">{badge.label} · {entry.kurul}</span>
                  {entry.aiAudit?.verified && (
                    <ShieldCheck className="w-3.5 h-3.5 text-ok shrink-0" aria-label="Doğrulanmış" />
                  )}
                  <span className="flex-1" />
                  <button
                    type="button"
                    onClick={(e) => toggleBookmark(entry.id, e)}
                    className={`-m-1.5 w-8 h-8 shrink-0 rounded-lg flex items-center justify-center hover:bg-canvas transition-colors cursor-pointer ${
                      isBookmarked ? 'text-amber-500' : 'text-ink-3 hover:text-ink'
                    }`}
                    aria-label={isBookmarked ? 'Yer işaretlerinden kaldır' : 'Yer işaretlerine ekle'}
                  >
                    <Bookmark className="w-4 h-4" fill={isBookmarked ? 'currentColor' : 'none'} />
                  </button>
                </div>
                <h3 className="m-0 mt-2 text-[16px] font-semibold text-ink group-hover:text-accent transition-colors leading-snug">
                  {entry.term}
                </h3>
                {entry.latinName && (
                  <p className="m-0 text-[12.5px] text-ink-3 italic truncate">{entry.latinName}</p>
                )}
                <p className="m-0 mt-2 text-[14px] text-ink-2 line-clamp-3 leading-[1.6]">{entry.definition}</p>
              </div>
            );
          })}
        </div>
      )}

      {/* ========================================================= */}
      {/* DETAYLI ANSİKLOPEDİ MODAL / SLIDE-OVER                    */}
      {/* ========================================================= */}
      {activeEntry && (
        <div
          className="ms-overlay fixed inset-0 z-[70] bg-[rgba(14,26,38,0.6)] backdrop-blur-xs flex items-center justify-center p-2 sm:p-4 md:p-6"
          role="dialog"
          aria-modal="true"
        >
          <div className="w-full max-w-3xl bg-white dark:bg-panel border border-line rounded-2xl shadow-2xl flex flex-col max-h-[90dvh] overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            {/* Modal Header */}
            <div className="p-4 sm:p-5 border-b border-line flex items-start justify-between gap-3 bg-canvas/40">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2 flex-wrap mb-1.5">
                  <span className={`text-[11.5px] font-bold px-2 py-0.5 rounded-md border ${getCategoryBadge(activeEntry.category).cls}`}>
                    {getCategoryBadge(activeEntry.category).label}
                  </span>
                  <span className="text-[11px] font-semibold px-2 py-0.5 rounded bg-canvas text-ink-3 border border-line">
                    {activeEntry.kurul} • {activeEntry.discipline}
                  </span>
                  {activeEntry.aiAudit?.verified && (
                    <span className="inline-flex items-center gap-1 text-[11px] font-bold text-emerald-600 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>{activeEntry.uretici === 's13_study' ? 'Ders notuyla doğrulandı' : 'AI Onaylı'} (%{activeEntry.aiAudit.accuracyScore})</span>
                    </span>
                  )}
                </div>

                <h2 className="text-xl sm:text-2xl font-extrabold text-ink leading-tight">
                  {activeEntry.term}
                </h2>
                {activeEntry.latinName && (
                  <p className="text-[13px] sm:text-[14px] text-ink-3 italic font-serif mt-0.5">
                    {activeEntry.latinName}
                  </p>
                )}
              </div>

              {/* Close & Action Buttons */}
              <div className="flex items-center gap-1.5 shrink-0">
                <button
                  type="button"
                  onClick={() => toggleBookmark(activeEntry.id)}
                  className="p-2 rounded-xl border border-line hover:bg-canvas text-ink-2 hover:text-ink cursor-pointer transition-colors"
                  title="Kaydet"
                >
                  <Bookmark
                    className="w-4 h-4"
                    fill={bookmarkedIds.includes(activeEntry.id) ? 'currentColor' : 'none'}
                  />
                </button>
                <button
                  type="button"
                  onClick={() => copyShareLink(activeEntry)}
                  className="p-2 rounded-xl border border-line hover:bg-canvas text-ink-2 hover:text-ink cursor-pointer transition-colors"
                  title="Bağlantıyı Kopyala"
                >
                  {copiedLink ? <Check className="w-4 h-4 text-emerald-600" /> : <Share2 className="w-4 h-4" />}
                </button>
                <button
                  type="button"
                  onClick={() => setActiveEntry(null)}
                  className="p-2 rounded-xl border border-line hover:bg-canvas text-ink-2 hover:text-ink cursor-pointer transition-colors"
                  title="Kapat (Esc)"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Modal Body Content (Scrollable) */}
            <div className="flex-1 min-h-0 overflow-y-auto p-4 sm:p-6 flex flex-col gap-4">
              {/* Notification if AI Audited recently */}
              {auditMessage && (
                <div className="p-3 rounded-xl bg-accent-soft text-accent text-[13px] font-semibold flex items-center gap-2 border border-accent/20 animate-in fade-in">
                  <Sparkles className="w-4 h-4 shrink-0" />
                  <span>{auditMessage}</span>
                </div>
              )}

              {/* 1. Orijinal Ders Notu Bağlamı (Prof/Slayt Notu) */}
              {activeEntry.lectureContextNotes && (
                <div className="rounded-xl p-3.5 sm:p-4 bg-teal-500/10 dark:bg-teal-950/20 flex flex-col gap-2 min-w-0">
                  <div className="flex flex-col gap-0.5 min-w-0">
                    <span className="text-[13px] font-semibold text-teal-800 dark:text-teal-300 flex items-center gap-1.5">
                      <GraduationCap className="w-4 h-4 text-teal-600 shrink-0" />
                      <span>Ders notu</span>
                    </span>
                    {activeEntry.instructorAndSource && (
                      <span className="text-[12.5px] text-ink-3 [overflow-wrap:anywhere]">
                        {activeEntry.instructorAndSource.replace(/\.txt\b/gi, '').replace(/^\d+\)\s*/, '')}
                      </span>
                    )}
                  </div>
                  <p className="m-0 text-[13px] sm:text-[13.5px] text-teal-950 dark:text-teal-100 leading-relaxed font-normal">
                    {activeEntry.lectureContextNotes}
                  </p>
                </div>
              )}

              {/* 2. Tanım */}
              <div className="flex flex-col gap-1">
                <span className="text-[11px] font-bold uppercase tracking-wider text-ink-3">Tanım</span>
                <p className="text-[14px] sm:text-[14.5px] text-ink leading-relaxed">
                  {activeEntry.definition}
                </p>
              </div>

              {/* 3. Patoloji, Morfoloji ve Etki Mekanizması */}
              {activeEntry.morphologyOrMechanism && (
                <div className="rounded-xl p-3.5 sm:p-4 bg-canvas border border-line flex flex-col gap-1.5">
                  <span className="text-[11.5px] font-bold uppercase tracking-wider text-ink-2 flex items-center gap-1.5">
                    <Stethoscope className="w-4 h-4 text-accent" />
                    <span>Patoloji, Morfoloji & Etki Mekanizması</span>
                  </span>
                  <p className="m-0 text-[13px] sm:text-[13.5px] text-ink-2 leading-relaxed whitespace-pre-line">
                    {activeEntry.morphologyOrMechanism}
                  </p>
                </div>
              )}

              {/* 4. Ayırıcı Tanı Kriterleri */}
              {activeEntry.differentialDiagnosis && (
                <div className="rounded-xl p-3.5 sm:p-4 bg-blue-500/5 dark:bg-blue-950/20 border-l-4 border-l-blue-600 border border-blue-500/20 flex flex-col gap-1.5">
                  <span className="text-[11.5px] font-bold uppercase tracking-wider text-blue-900 dark:text-blue-300 flex items-center gap-1.5">
                    <Filter className="w-4 h-4 text-blue-600" />
                    <span>Ayırıcı Tanı & Ayırt Edici Özellikler</span>
                  </span>
                  <p className="m-0 text-[13px] sm:text-[13.5px] text-ink-2 leading-relaxed">
                    {activeEntry.differentialDiagnosis}
                  </p>
                </div>
              )}

              {/* 5. Sınav Tuzağı & Dikkat Edilmesi Gerekenler */}
              {activeEntry.pitfallsAndWarnings && (
                <div className="rounded-xl p-3.5 sm:p-4 bg-rose-500/10 dark:bg-rose-950/30 border-l-4 border-l-rose-600 border border-rose-500/20 flex flex-col gap-1.5">
                  <span className="text-[11.5px] font-bold uppercase tracking-wider text-rose-900 dark:text-rose-300 flex items-center gap-1.5">
                    <AlertTriangle className="w-4 h-4 text-rose-600" />
                    <span>Sınav Tuzağı & Dikkat Edilmesi Gerekenler</span>
                  </span>
                  <p className="m-0 text-[13px] sm:text-[13.5px] text-rose-950 dark:text-rose-100 leading-relaxed font-medium">
                    {activeEntry.pitfallsAndWarnings}
                  </p>
                </div>
              )}

              {/* 6. Hoca İncisi & Sınav Spotları */}
              {activeEntry.examSpotPearls && (
                <div className="rounded-xl p-3.5 sm:p-4 bg-amber-500/10 dark:bg-amber-950/30 border-l-4 border-l-amber-600 border border-amber-500/20 flex flex-col gap-1.5">
                  <span className="text-[11.5px] font-bold uppercase tracking-wider text-amber-900 dark:text-amber-300 flex items-center gap-1.5">
                    <Lightbulb className="w-4 h-4 text-amber-600" />
                    <span>Hoca İncisi & Sınav Spotu</span>
                  </span>
                  <p className="m-0 text-[13px] sm:text-[13.5px] text-amber-950 dark:text-amber-100 leading-relaxed font-medium">
                    {activeEntry.examSpotPearls}
                  </p>
                </div>
              )}

              {/* 7. İlişkili Kavramlar (Clickable Chips) */}
              {activeEntry.relatedItems && activeEntry.relatedItems.length > 0 && (
                <div className="flex flex-col gap-2 pt-2 border-t border-line/60">
                  <span className="text-[11.5px] font-bold uppercase tracking-wider text-ink-3">
                    İlişkili Hastalıklar & İlaçlar
                  </span>
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
                          className="px-2.5 py-1 rounded-lg bg-canvas hover:bg-accent-soft text-ink-2 hover:text-accent border border-line text-[12px] font-semibold flex items-center gap-1 transition-colors cursor-pointer"
                        >
                          <Hash className="w-3 h-3 text-accent" />
                          <span>{rel ? rel.term : relId}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* 8. Örnek TUS / Komite Soru Kutusu */}
              {activeEntry.aiAudit?.sampleExamQuestion && (
                <div className="rounded-xl p-3.5 bg-canvas/80 border border-line flex flex-col gap-1 text-[12.5px]">
                  <span className="font-bold text-accent flex items-center gap-1">
                    <HelpCircle className="w-3.5 h-3.5" />
                    <span>Örnek Sınav Sorusu & Kazanım</span>
                  </span>
                  <p className="m-0 text-ink-2 italic font-sans leading-relaxed">
                    {activeEntry.aiAudit.sampleExamQuestion}
                  </p>
                </div>
              )}
            </div>

            {/* Modal Footer with AI Audit Action */}
            <div className="p-3.5 sm:p-4 border-t border-line bg-canvas/60 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5">
              <div className="text-[11.5px] text-ink-3 flex items-center gap-1.5">
                <BrainCircuit className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>
                  Doğrulama Durumu:{' '}
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
                  className="w-full sm:w-auto px-4 py-2 rounded-xl bg-accent hover:bg-accent/90 text-white text-[12.5px] font-bold flex items-center justify-center gap-2 shadow-2xs transition-all cursor-pointer disabled:opacity-50"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isAiAuditing ? 'animate-spin' : ''}`} />
                  <span>{isAiAuditing ? 'Yapay Zeka Denetliyor...' : 'AI ile Denetle & Geliştir'}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
