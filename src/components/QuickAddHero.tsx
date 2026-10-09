import React, { useEffect, useMemo, useState } from 'react';
import {
  ArrowRight,
  CheckCircle2,
  ChevronRight,
  ChevronDown,
  Check,
  CircleDashed,
  AlertCircle,
  Sparkles,
  CheckSquare,
  Square,
  Layers,
  X,
  Wand2,
  Link2,
  FileText,
  Copy,
  Lock,
  Plus,
  BookOpen,
  CalendarDays,
  Hash,
  Lightbulb,
  ListChecks,
  PenLine,
} from 'lucide-react';
import { Committee, QuestionItem } from '../types';
import { AppUser } from '../services/auth';
import { getDefaultActiveCommitteeId, filterCurrent2026_2027Committees } from '../services/firestoreDb';
import { pathFor, linkClick } from '../router';
import { OptionsEditor } from './ui/OptionsEditor';
import { BlurOverlay, SuccessCheck } from './ui/Animations';
import { toast } from './ui/Toast';
import { ApiService, SimilarPastQuestion, SourceRefLite } from '../services/api';
import { validateNamePolicy } from '../utils/namePolicy';
import { useUiVersion } from '../utils/uiVersion';
import { findRealtimeMatchingDrafts, RealtimeMatchItem, DraftCompatibilityResult, warmMedicalIndex } from '../services/draftClusteringService';
import { getSmartQuestionAssistant, SmartQuestionAssistantResult } from '../services/medicalPredictorService';
import { Colored, WordLegend, ContextBadge, sharedWordColors } from './draftHighlight';
import { AiQuestionOptimizerModal } from './AiQuestionOptimizerModal';
import { LoveNote } from './home/LoveNote';
import { MetaPicker } from './ui/MetaPicker';

// Benzerlik puanı kademesine göre renk ve stil haritası
export const getScoreTier = (score: number) => {
  if (score >= 80) {
    return {
      tierName: 'Çok Yüksek Uyum',
      pillBg: 'bg-emerald-500/15 text-emerald-900 border-emerald-300',
      barColor: 'bg-emerald-500',
      cardBorder: 'border-emerald-300 bg-emerald-50/50 hover:border-emerald-400',
    };
  }
  if (score >= 65) {
    return {
      tierName: 'Yüksek Benzerlik',
      pillBg: 'bg-amber-500/15 text-amber-900 border-amber-300',
      barColor: 'bg-amber-500',
      cardBorder: 'border-amber-300 bg-amber-50/50 hover:border-amber-400',
    };
  }
  if (score >= 50) {
    return {
      tierName: 'Orta Benzerlik',
      pillBg: 'bg-sky-500/15 text-sky-900 border-sky-300',
      barColor: 'bg-sky-500',
      cardBorder: 'border-sky-200 bg-sky-50/40 hover:border-sky-300',
    };
  }
  return {
    tierName: 'İlişkili Konu',
    pillBg: 'bg-purple-500/15 text-purple-900 border-purple-200',
    barColor: 'bg-purple-500',
    cardBorder: 'border-purple-200 bg-purple-50/30 hover:border-purple-300',
  };
};

// Kaynak türü etiketi ve rengi (tasarımdaki Slayt / Özet / Çıkmış / Deşifre)
const SOURCE_KIND: Record<string, { label: string; cls: string }> = {
  lecture_slide: { label: 'Slayt', cls: 'bg-accent-soft text-accent' },
  summary: { label: 'Özet', cls: 'bg-ok-soft text-ok' },
  past_question: { label: 'Çıkmış', cls: 'bg-violet-50 text-violet-700' },
  transcript: { label: 'Deşifre', cls: 'bg-warn-soft text-warn' },
};

type OptionKey = 'A' | 'B' | 'C' | 'D' | 'E';
const KEYS: OptionKey[] = ['A', 'B', 'C', 'D', 'E'];

interface QuickAddHeroProps {
  committee: Committee | undefined;
  committees: Committee[];
  onSelectCommittee: (committeeId: string) => void;
  onSubmitContribution: (data: {
    committeeId: string;
    questionNumber?: number;
    isUnknownNumber?: boolean;
    discipline: string;
    topic: string;
    fragmentText: string;
    author: string;
    authorUid?: string;
    authorStudentNumber?: string;
    claimedAnswer?: OptionKey;
    options?: { key: OptionKey; text: string }[];
    targetQuestionId?: string;
    /** Sınav yılı ("2025-2026"); bilinmiyorsa yok */
    examYear?: string;
  }) => Promise<void>;
  unassignedCount: number;
  totalQuestionsCount: number;
  questions?: QuestionItem[];
  onOpenQuestion?: (question: QuestionItem) => void;
  onNavigateTab: (tab: 'matrix' | 'questions' | 'practice' | 'booklet' | 'notes' | 'past_exams' | 'study' | 'learn') => void;
  isAdmin: boolean;
  currentUser?: AppUser | null;
  onOpenAdminPanel?: () => void;
  onQuestionsUpdated?: () => Promise<void>;
}

const SAVED_NAME_KEY = 'medsoru_saved_contributor_name';
const EXAM_YEAR_KEY = 'medsoru_contrib_exam_year';
/** Öğretim yılı Eylül'de başlar: 9 Ekim 2026 → "2026-2027" */
export const currentAcademicYear = (d = new Date()) => {
  const y = d.getMonth() >= 8 ? d.getFullYear() : d.getFullYear() - 1;
  return `${y}-${y + 1}`;
};
/** 2016-2017'den bu yıla kadar öğretim yılları, yeniden eskiye */
export const academicYears = () => {
  const last = Number(currentAcademicYear().slice(0, 4));
  return Array.from({ length: last - 2016 + 1 }, (_, i) => `${last - i}-${last - i + 1}`);
};

// The correct answer is picked inside the option list (tap a letter), so there is no separate "Cevap" mode
type Mode = 'stem' | 'option' | 'clue';
const MODES: { id: Mode; label: string }[] = [
  { id: 'stem', label: 'Soru kökü' },
  { id: 'option', label: 'Şıklar' },
  { id: 'clue', label: 'İpucu' },
];

const PLACEHOLDERS: Record<Mode, string> = {
  stem: "Sorudan hatırladığın kısmı yaz… örn. göçük altında kalan hasta, EKG'de sivri T",
  option: '',
  clue: 'Örn. idrarda delta-ALA yüksekti, kemik iliğinde halkalı sideroblast…',
};

export const committeeShortLabel = (c: Committee) => {
  const m = c.name.match(/Kurul\s*(\d+)/i);
  if (m) return `Kurul ${m[1]}`;
  // Önce kimliğe bakılır: Final kurulunun adı "bütünleme" sözcüğünü de içerebiliyor
  if (/final/i.test(c.id)) return 'Final';
  if (/b[uü]t[uü]nleme/i.test(c.id)) return 'Bütünleme';
  if (/bütünleme/i.test(c.name)) return 'Bütünleme';
  if (/final/i.test(c.name)) return 'Final';
  return c.code || c.name;
};

export const questionStemText = (q: QuestionItem) =>
  q.reconstruction?.stem || q.rawStem || q.fragments.find((f) => f.type === 'stem')?.text || q.fragments[0]?.text || q.topic;

export const StatusPill: React.FC<{ status: QuestionItem['status']; hasFragments?: boolean }> = ({ status, hasFragments }) => {
  if (status === 'completed') {
    return (
      <span className="inline-flex items-center gap-1.5 h-7 px-2.5 rounded-full bg-ok-soft text-ok text-[12px] font-semibold whitespace-nowrap">
        <Check className="w-[13px] h-[13px]" strokeWidth={3} />
        Doğrulandı
      </span>
    );
  }
  if (status === 'empty' && !hasFragments) {
    return (
      <span className="inline-flex items-center gap-1.5 h-7 px-2.5 rounded-full bg-canvas text-ink-2 text-[12px] font-semibold whitespace-nowrap">
        Boş
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1.5 h-7 px-2.5 rounded-full bg-warn-soft text-warn text-[12px] font-semibold whitespace-nowrap">
      <CircleDashed className="w-[13px] h-[13px]" strokeWidth={2.6} />
      Taslak
    </span>
  );
};

const titleCase = (c: Committee) => {
  return committeeShortLabel(c);
};

/**
 * Resmi ders programına göre bir kurulun soru girişine açılıp açılmadığını kontrol eder.
 * Kural: Önceki kurulun sınav tarihi tamamlanmadan bir sonraki kurula soru yazılamaz.
 * (Kurul 1 daima açıktır; Kurul 2 için Kurul 1 sınavı bitmiş olmalıdır; vb.)
 */
export const COMMITTEE_EXAM_DATES: Record<string, string> = {
  'donem3-kurul1': '2026-10-23T23:59:59',
  'donem3-kurul2': '2026-12-04T23:59:59',
  'donem3-kurul3': '2027-01-22T23:59:59',
  'donem3-kurul4': '2027-03-05T23:59:59',
  'donem3-kurul5': '2027-04-22T23:59:59',
  'donem3-kurul6': '2027-06-11T23:59:59',
  'donem3-final': '2027-06-28T23:59:59',
  'donem3-butunleme': '2027-07-16T23:59:59',
};

const COMMITTEE_SEQUENCE = [
  'donem3-kurul1',
  'donem3-kurul2',
  'donem3-kurul3',
  'donem3-kurul4',
  'donem3-kurul5',
  'donem3-kurul6',
  'donem3-final',
  'donem3-butunleme',
];

export const isCommitteeLocked = (committeeId: string): boolean => {
  const idx = COMMITTEE_SEQUENCE.indexOf(committeeId);
  if (idx <= 0) return false; // Kurul 1 her zaman açıktır
  const prevCommitteeId = COMMITTEE_SEQUENCE[idx - 1];
  const prevDateStr = COMMITTEE_EXAM_DATES[prevCommitteeId];
  if (!prevDateStr) return false;
  return new Date() < new Date(prevDateStr);
};

/**
 * Home page: nothing but adding a remembered piece of a question.
 * One composer (stem / option / clue / answer), committee + discipline + number, and a quiet pool bar.
 */
export const QuickAddHero: React.FC<QuickAddHeroProps> = ({
  committee,
  committees,
  onSelectCommittee,
  onSubmitContribution,
  unassignedCount,
  totalQuestionsCount,
  questions = [],
  onNavigateTab,
  currentUser,
  onQuestionsUpdated,
}) => {
  const disciplines =
    committee?.disciplines && committee.disciplines.length > 0
      ? committee.disciplines
      : ['Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'Tıbbi Biyokimya', 'Halk Sağlığı', 'İç Hastalıkları'];

  const [mode, setMode] = useState<Mode>('stem');
  // Each mode keeps its own text: typing a stem must not leak into the clue
  type TextMode = Exclude<Mode, 'option'>;
  const [texts, setTexts] = useState<Record<TextMode, string>>({ stem: '', clue: '' });
  const text = mode === 'option' ? '' : texts[mode];

  const setText = (v: string) => mode !== 'option' && setTexts((prev) => ({ ...prev, [mode]: v }));
  const [answerReason, setAnswerReason] = useState('');
  const hasAnyText = Object.values(texts).some((t) => t.trim()) || !!answerReason.trim();
  const [options, setOptions] = useState<Record<OptionKey, string>>({ A: '', B: '', C: '', D: '', E: '' });
  const [optionCount, setOptionCount] = useState(1);
  const [claimedAnswer, setClaimedAnswer] = useState<OptionKey | undefined>(undefined);
  const [discipline, setDiscipline] = useState(disciplines[0]);
  const [questionNumber, setQuestionNumber] = useState('');
  // Sınav yılı: varsayılan bu öğretim yılı; "" = bilmiyorum (seçim cihazda hatırlanır)
  const [examYear, setExamYearState] = useState<string>(() => {
    try {
      const v = localStorage.getItem(EXAM_YEAR_KEY);
      if (v !== null) return v;
    } catch { /* yok */ }
    return currentAcademicYear();
  });
  const setExamYear = (v: string) => {
    setExamYearState(v);
    try { localStorage.setItem(EXAM_YEAR_KEY, v); } catch { /* yok */ }
  };
  const [userManualDiscipline, setUserManualDiscipline] = useState(false);
  const [userManualNumber, setUserManualNumber] = useState(false);
  // Alt şerit: değer otomatik mi geldi (eşleşen taslak/tahmin) — kullanıcıya "otomatik" diye gösterilir
  const [autoDisc, setAutoDisc] = useState(false);
  const [autoNum, setAutoNum] = useState(false);
  const [discMenu, setDiscMenu] = useState(false);
  const [discQuery, setDiscQuery] = useState('');
  const [linkedQuestion, setLinkedQuestion] = useState<QuestionItem | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [similar, setSimilar] = useState<SimilarPastQuestion[]>([]);
  const [simOpen, setSimOpen] = useState(false);
  const { isV3 } = useUiVersion();
  const [sources, setSources] = useState<SourceRefLite[]>([]);
  const [realtimeMatches, setRealtimeMatches] = useState<RealtimeMatchItem[]>([]);
  const [selectedMatchIds, setSelectedMatchIds] = useState<Set<string>>(new Set());
  const [isMergingSelected, setIsMergingSelected] = useState(false);
  const [smartAssistant, setSmartAssistant] = useState<SmartQuestionAssistantResult | null>(null);
  const [optimizingQuestion, setOptimizingQuestion] = useState<QuestionItem | null>(null);
  const [debouncedText, setDebouncedText] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  // Tıbbi kavram sözlüğünü sayfa açılışında boşta kur (yazarken takılmasın)
  useEffect(() => { warmMedicalIndex(); }, []);

  // Kurul kilitli mi kontrolü: Sınav tarihi gelmeden soru yazılamaz
  const isLocked = useMemo(() => {
    return committee ? isCommitteeLocked(committee.id) : false;
  }, [committee]);

  // 1. Kelime-bazlı ve boşluk tetiklemeli (Space-delimited / Word-level) gecikmeli metin optimizasyonu:
  // - Kullanıcı boşluk (' ') veya noktalama (. , ! ? \n) bastığı an, tamamlanan son kelimeye kadar olan
  //   kısmı (yazılmakta olan eksik kelime hariç / 1 kelime öncesi) hemen işleme alır.
  // - Kullanıcı boşluk basmadan duraklarsa fallback (500ms) devreye girerek mevcut metni tamamlar.
  // - Bu sayede her harfte hesaplama yapmak yerine kelime bazlı tetiklenir, mobil ve masaüstünde donma engellenir.
  useEffect(() => {
    const raw = text || '';
    if (!raw.trim()) {
      setDebouncedText('');
      setIsSearching(false);
      return;
    }

    // Kullanıcı bir boşluk veya noktalama girdiyse, son tamamlanan kelimeye kadar olan kısmı al
    const endsWithBoundary = /[\s.,;:!?\n]$/.test(raw);
    if (endsWithBoundary) {
      // Tamamlanmış kelimeler kümesi
      const completedWords = raw.replace(/\S+$/, '').trim();
      if (completedWords.length >= 6) {
        setIsSearching(true);
        // Doğrudan mikrogörev / kısa zamanlayıcı ile işle (UI thread'ini kilitlemez)
        const t = window.setTimeout(() => {
          setDebouncedText(completedWords);
        }, 60);
        return () => window.clearTimeout(t);
      }
    }

    // Boşluk bırakılmadıysa veya henüz kelime tamamlanmadıysa (yazarken duraksama fallback'i):
    // 500ms duraklama sonrası tam metni değerlendir
    setIsSearching(true);
    const idleTimer = window.setTimeout(() => {
      setDebouncedText(raw.trim());
    }, 500);

    return () => window.clearTimeout(idleTimer);
  }, [text]);

  // 2. Havuz Chunking ve Ön Filtreleme:
  // Mevcut soru listesini aranabilir hafif token indekslerine dönüştürür.
  const indexedPool = useMemo(() => {
    if (!questions || questions.length === 0) return [];
    return questions.map((q) => {
      const stem = (q.reconstruction?.stem || q.stem || q.rawStem || q.fragments?.[0]?.text || q.topic || '').toLowerCase();
      const optionsText = (q.options || []).map((o) => o.text.toLowerCase()).join(' ');
      const tokens = new Set([...stem.split(/\s+/), ...optionsText.split(/\s+/)].filter((w) => w.length > 2));
      return {
        question: q,
        committeeId: q.committeeId,
        discipline: (q.discipline || '').toLowerCase(),
        stem,
        tokens,
      };
    });
  }, [questions]);

  // Taslak aramasına şıklar da katılır: öğrenci yalnızca şık hatırlıyor olabilir
  const optionsText = KEYS.map((k) => options[k].trim()).filter(Boolean).join(' ');
  // Ders, eşleştirmeye ref ile verilir: ders değişince arama yeniden tetiklenmesin (aksi halde
  // eşleşme dersi değiştiriyor → arama yeniden çalışıyor → tahmin dersi geri çeviriyordu: yanıp sönme)
  const disciplineRef = React.useRef(discipline);
  disciplineRef.current = discipline;
  const matchedDiscRef = React.useRef(false);

  // 3. Anlık taslak eşleme ve Kurul/Ders tahmin asistanı:
  // debouncedText üzerinden, requestAnimationFrame veya setTimeout chunking ile non-blocking çalışır.
  useEffect(() => {
    const q = `${mode === 'option' ? texts.stem.trim() : debouncedText} ${optionsText}`.trim();
    if (q.length < 8 || !committee?.id) {
      if (!q) matchedDiscRef.current = false; // yeni soru: eşleşme önceliği sıfırlanır
      setRealtimeMatches([]);
      setSelectedMatchIds(new Set());
      setSmartAssistant(null);
      setIsSearching(false);
      return;
    }

    let isCancelled = false;
    setIsSearching(true);

    const optionsList = KEYS.filter((k) => options[k].trim()).map((k) => ({ key: k, text: options[k].trim() }));

    // Chunking: İşlemi bir sonraki frame'e bırakarak textarea render döngüsünü %100 akıcı tutar
    const chunkTimer = window.setTimeout(() => {
      if (isCancelled) return;

      try {
        // 1. Akıllı Asistan Analizi (Kurul, Ders, Tıbbi Kavram & Çapraz Kurul Tespiti)
        const assistantRes = getSmartQuestionAssistant(q, optionsList, committee.id);
        if (isCancelled) return;
        setSmartAssistant(assistantRes);

        // Kullanıcı elle ders seçmediyse ve tahmin edilen ders bu kurula aitse otomatik uygula
        // (eşleşen taslaktan gelen ders önceliklidir; tahmin onu ezmez)
        if (!userManualDiscipline && !matchedDiscRef.current && assistantRes.predictedDiscipline) {
          const predDisc = assistantRes.predictedDiscipline.discipline;
          if (disciplines.includes(predDisc) && predDisc !== disciplineRef.current) {
            setDiscipline(predDisc);
            setAutoDisc(true);
          }
        }

        // 2. Chunk / Hızlı Ön Filtreleme ile Aday Havuzu Daraltma
        const qWords = q.toLowerCase().split(/\s+/).filter((w) => w.length > 2);
        // Sadece soru metninde veya şıklarında en az 1 ortak token içeren ya da aynı kurul/ders olanları al
        const filteredCandidateQuestions = indexedPool.length > 0
          ? indexedPool
              .filter((item) => {
                if (item.committeeId === committee.id) return true;
                // Çapraz kurul için en az bir kelime benzerliği şartı
                return qWords.some((w) => item.tokens.has(w) || item.stem.includes(w));
              })
              .map((item) => item.question)
          : questions;

        // 3. Taslak Eşleme (optimize edilmiş aday kümesi üzerinde)
        const matches = findRealtimeMatchingDrafts(
          {
            committeeId: committee.id,
            discipline: disciplineRef.current,
            topic: `${disciplineRef.current} Hatırlanan Soru`,
            text: q,
            options: optionsList.length > 0 ? optionsList : undefined,
          },
          filteredCandidateQuestions,
          35, // En az %35 benzerlik
          4,  // En fazla 4 aday göster
          true // Çapraz kurul taslaklarını da göster
        );

        if (isCancelled) return;
        setRealtimeMatches(matches);

        // Geçersiz kalan seçili id'leri temizle
        setSelectedMatchIds((prev) => {
          const validIds = new Set(matches.map((m) => m.question.id));
          const next = new Set<string>();
          prev.forEach((id) => {
            if (validIds.has(id)) next.add(id);
          });
          return next;
        });
      } finally {
        if (!isCancelled) {
          setIsSearching(false);
        }
      }
    }, 20);

    return () => {
      isCancelled = true;
      window.clearTimeout(chunkTimer);
    };
  }, [debouncedText, mode, committee?.id, optionsText, questions, indexedPool]);

  const toggleSelectMatch = (id: string) => {
    setSelectedMatchIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const selectAllMatches = () => {
    setSelectedMatchIds(new Set(realtimeMatches.map((m) => m.question.id)));
  };

  const clearSelection = () => {
    setSelectedMatchIds(new Set());
  };

  // Çıkmış sorudan yalnızca soru kökünü editöre kopyalama
  const handleCopyQuestionStem = (stemText: string) => {
    setTexts((prev) => ({ ...prev, stem: stemText.trim() }));
    if (mode === 'option') setMode('stem');
    navigator.clipboard?.writeText(stemText.trim()).catch(() => {});
    toast.success('Kök Kopyalandı', 'Soru kökü editöre aktarıldı ve panoya kopyalandı.');
  };

  // Çıkmış soruyu tamamen editöre aktarma (kök + şıklar + cevap)
  const handleTransferEntireQuestion = async (similarItem: SimilarPastQuestion) => {
    setTexts((prev) => ({ ...prev, stem: similarItem.stem.trim() }));
    if (mode === 'option') setMode('stem');
    if (similarItem.discipline && disciplines.includes(similarItem.discipline)) {
      setDiscipline(similarItem.discipline);
      setUserManualDiscipline(true);
    }
    // Şıklar benzer soru sonucuyla birlikte gelir; yoksa çıkmış soru listesinden tamamlanır
    let sourceOptions: { key: string; text: string }[] = similarItem.options || [];
    let ans = similarItem.claimedAnswer;
    if (sourceOptions.length === 0) {
      try {
        const pastList = await ApiService.getPastQuestions({ query: similarItem.id, includeAmbiguous: true });
        const fullQ = pastList.find((p) => String(p.id) === String(similarItem.id));
        if (fullQ) {
          sourceOptions = fullQ.reconstruction?.options || fullQ.options || [];
          ans = fullQ.reconstruction?.correctAnswer || fullQ.correctAnswer || fullQ.claimedAnswer || ans;
        }
      } catch (_) {}
    }
    if (sourceOptions.length > 0) {
      const newOpts: Record<OptionKey, string> = { A: '', B: '', C: '', D: '', E: '' };
      sourceOptions.forEach((o) => {
        if (o.key && (KEYS as string[]).includes(o.key)) newOpts[o.key as OptionKey] = (o.text || '').trim();
      });
      setOptions(newOpts);
      setOptionCount(KEYS.filter((k) => newOpts[k]).length || 5);
    }
    if (ans && (KEYS as string[]).includes(ans)) setClaimedAnswer(ans as OptionKey);
    setSimOpen(false);

    toast.success('Soru aktarıldı', sourceOptions.length ? `Kök, ${sourceOptions.length} şık ve cevap eklendi.` : 'Soru kökü eklendi.');
  };

  // Bir soruya doğrudan bağlama aksiyonu
  const handleLinkToQuestion = (targetQ: QuestionItem) => {
    setLinkedQuestion(targetQ);
    if (targetQ.questionNumber) {
      setQuestionNumber(String(targetQ.questionNumber));
      setUserManualNumber(true);
    }
    if (targetQ.discipline && targetQ.discipline !== 'Belirtilmedi') {
      setDiscipline(targetQ.discipline);
      setUserManualDiscipline(true);
    }
    toast.success(
      'Soruya bağlandı',
      targetQ.questionNumber
        ? `Parçan Soru #${targetQ.questionNumber} ile birleştirilecek.`
        : 'Parçan mevcut taslağın katkılarına eklenecek.'
    );
  };

  // Seçilen taslakları gruplandırıp birleştirme
  const handleMergeAndGroupSelected = async () => {
    if (selectedMatchIds.size === 0) return;
    const selectedList = realtimeMatches.filter((m) => selectedMatchIds.has(m.question.id));
    if (selectedList.length === 0) return;

    setIsMergingSelected(true);
    try {
      const anchor = selectedList[0].question;
      const targetCommittee = committee || (committees && committees.length > 0 ? committees[0] : undefined);
      if (!targetCommittee) {
        toast.error('Hata', 'Kurul seçili değil.');
        return;
      }

      if (selectedList.length > 1) {
        // Çoklu seçim: Seçilen taslakları birleştir
        const satellites = selectedList.slice(1).map((m) => m.question.id);
        const adminName = currentUser?.displayName || 'Kullanıcı';
        const adminEmail = currentUser?.email || 'admin@medsoru.local';
        await ApiService.mergeDraftCluster(adminEmail, anchor.id, satellites, adminName);
      }

      // Kullanıcının yazdığı parçayı da bu anchor soruya ekle
      const optionsList = KEYS.filter((k) => options[k].trim()).map((k) => ({ key: k, text: options[k].trim() }));
      const fragmentText = [
        texts.stem.trim(),
        texts.clue.trim() ? `İpucu: ${texts.clue.trim()}` : '',
        claimedAnswer && answerReason.trim() ? `Cevap notu (${claimedAnswer}): ${answerReason.trim()}` : '',
      ]
        .filter(Boolean)
        .join('\n');

      if (fragmentText || optionsList.length > 0 || claimedAnswer) {
        const savedName = localStorage.getItem(SAVED_NAME_KEY) || '';
        await onSubmitContribution({
          committeeId: targetCommittee.id,
          questionNumber: anchor.questionNumber,
          isUnknownNumber: !anchor.questionNumber,
          discipline: anchor.discipline || discipline,
          topic: `${anchor.discipline || discipline} Hatırlanan Soru`,
          fragmentText: fragmentText || 'Benzer taslak birleştirme',
          author: currentUser?.displayName || savedName || 'Dönem 3 Öğrencisi',
          authorUid: currentUser?.uid,
          authorStudentNumber: currentUser?.studentNumber || undefined,
          claimedAnswer,
          options: optionsList.length > 0 ? optionsList : undefined,
          targetQuestionId: anchor.id,
          examYear: examYear || undefined,
        });
      }

      toast.success(
        'Taslaklar Birleştirildi!',
        selectedList.length > 1
          ? `${selectedList.length} adet taslak başarıyla tek bir soruda birleştirildi.`
          : `Parçan Soru #${anchor.questionNumber || 'taslak'} ile birleştirildi.`
      );

      setTexts({ stem: '', clue: '' });
      setOptions({ A: '', B: '', C: '', D: '', E: '' });
      setOptionCount(1);
      setAnswerReason('');
      setClaimedAnswer(undefined);
      setQuestionNumber('');
      setLinkedQuestion(null);
      setSelectedMatchIds(new Set());
      setRealtimeMatches([]);

      if (onQuestionsUpdated) {
        await onQuestionsUpdated();
      }
    } catch (err: any) {
      toast.error('Birleştirme Başarısız', err?.message || 'Bir hata oluştu');
    } finally {
      setIsMergingSelected(false);
    }
  };

  // Tüm adayların ve kullanıcının metinlerindeki ortak kelime paleti (debouncedText ile optimize edildi)
  const sharedColors = useMemo(() => {
    if (realtimeMatches.length === 0 || !debouncedText) return new Map<string, string>();
    const allStems = [debouncedText, ...realtimeMatches.map((m) => questionStemText(m.question))];
    return sharedWordColors(allStems);
  }, [realtimeMatches, debouncedText]);

  useEffect(() => {
    if (!disciplines.includes(discipline)) setDiscipline(disciplines[0]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [committee]);

  // Pool stats for the selected committee
  // Yazarken benzer çıkmış sorular: debouncedText üzerinden çalışır, ana thread'i bloke etmez
  useEffect(() => {
    const q = debouncedText;
    if (mode === 'option' || q.length < 12) {
      setSimilar([]);
      if (q.length < 12) setSources([]);
      return;
    }
    let alive = true;
    const t = window.setTimeout(() => {
      ApiService.findSourcesForFragment(q, committee?.id, discipline)
        .then((r) => alive && setSources(r.slice(0, 4)))
        .catch(() => alive && setSources([]));
      ApiService.findSimilarPastQuestions(q, committee?.id)
        // Ham BM25 puanı sorgu uzunluğuyla büyür: kelime başına en az 14 ve en iyinin %70'i;
        // aksi halde alakasız "benzer" sorular gürültü yapar.
        .then((r) => {
          if (!alive) return;
          const words = q.split(/\s+/).filter((w) => w.length > 1).length || 1;
          const top = r?.[0]?.score || 0;
          setSimilar((r || []).filter((x) => (x.score || 0) >= words * 14 && (x.score || 0) >= top * 0.7).slice(0, 3));
        })
        .catch(() => alive && setSimilar([]));
    }, 200);
    return () => {
      alive = false;
      window.clearTimeout(t);
    };
  }, [debouncedText, mode, committee?.id, discipline]);

  const target = committee?.targetCount || 100;
  const completed = questions.filter((q) => q.status === 'completed').length;
  const drafts = questions.filter((q) => q.status !== 'completed' && (q.fragments.length > 0 || q.options.length > 0)).length;
  const pctNum = (n: number) => Math.min(100, (n / Math.max(target, 1)) * 100);
  // Drafts can exceed the target (archive imports); never let the bar overflow
  const draftPct = Math.max(0, Math.min(pctNum(drafts), 100 - pctNum(completed)));

  const activeCommitteeId = getDefaultActiveCommitteeId();
  const sortedCommittees = useMemo(() => filterCurrent2026_2027Committees(committees), [committees]);
  const isCollecting = committee?.id === activeCommitteeId;
  const shortName = committee ? titleCase(committee) : 'Kurul';

  const canSubmit = hasAnyText || KEYS.some((k) => options[k].trim()) || !!claimedAnswer;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    const targetCommittee = committee || (committees && committees.length > 0 ? committees[0] : undefined);
    if (!targetCommittee) {
      setFormError('Lütfen önce bir kurul seçiniz.');
      return;
    }

    if (isCommitteeLocked(targetCommittee.id)) {
      const msg = 'Ders programına göre bu kurulun sınav tarihi henüz gelmedi. Önceki kurul sınavı tamamlanmadan sonraki kurula soru yazılamaz.';
      setFormError(msg);
      toast.error('Kurul Henüz Açılmadı', msg);
      return;
    }

    const optionsList = KEYS.filter((k) => options[k].trim()).map((k) => ({ key: k, text: options[k].trim() }));
    if (!hasAnyText && optionsList.length === 0 && !claimedAnswer) {
      setFormError('Sorudan aklında kalan en az bir kelime, şık ya da cevap yaz.');
      return;
    }

    const num = parseInt(questionNumber, 10);
    const hasNumber = Number.isFinite(num) && num >= 1 && num <= target;
    // Everything written in the different modes goes in as one fragment
    const fragmentText = [
      texts.stem.trim(),
      texts.clue.trim() ? `İpucu: ${texts.clue.trim()}` : '',
      claimedAnswer && answerReason.trim() ? `Cevap notu (${claimedAnswer}): ${answerReason.trim()}` : '',
    ]
      .filter(Boolean)
      .join('\n');
    const savedName = localStorage.getItem(SAVED_NAME_KEY) || '';
    const authorCandidate = currentUser?.displayName || savedName;
    if (authorCandidate) {
      const nameCheck = validateNamePolicy(authorCandidate);
      if (!nameCheck.isValid) {
        setFormError(nameCheck.errorMessage || 'Geçersiz yazar / katkıcı adı.');
        toast.error('İsim Kuralı Hatası', nameCheck.errorMessage || 'Geçersiz isim.');
        return;
      }
    }

    setIsSubmitting(true);
    try {
      await onSubmitContribution({
        committeeId: targetCommittee.id,
        questionNumber: hasNumber ? num : undefined,
        isUnknownNumber: !hasNumber,
        discipline,
        topic: `${discipline} Hatırlanan Soru`,
        fragmentText,
        author: currentUser?.displayName || savedName || 'Dönem 3 Öğrencisi',
        authorUid: currentUser?.uid,
        authorStudentNumber: currentUser?.studentNumber || undefined,
        claimedAnswer,
        options: optionsList.length > 0 ? optionsList : undefined,
        targetQuestionId: linkedQuestion?.id,
        examYear: examYear || undefined,
      });
      setTexts({ stem: '', clue: '' });
      setOptions({ A: '', B: '', C: '', D: '', E: '' });
      setOptionCount(1);
      setAnswerReason('');
      setClaimedAnswer(undefined);
      setQuestionNumber('');
      setUserManualDiscipline(false);
      setUserManualNumber(false);
      setLinkedQuestion(null);
      setSuccessMessage(
        linkedQuestion
          ? `Parçan Soru #${linkedQuestion.questionNumber || 'taslak'} katkılarına eklendi.`
          : hasNumber
          ? `Soru ${num} için eklediğin parça havuza kaydedildi.`
          : 'Parçan havuza kaydedildi. Numarası bilinmeyenler benzerlerine göre yerleştirilir.'
      );
      setTimeout(() => setSuccessMessage(null), 6000);
      if (onQuestionsUpdated) {
        await onQuestionsUpdated();
      }
    } catch (err: any) {
      setFormError('Kayıt sırasında bir hata oluştu: ' + (err?.message || 'bilinmeyen hata'));
      toast.error('Parça kaydedilemedi', err?.message || 'Bağlantını kontrol edip tekrar dene.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const field = 'bg-field border border-transparent outline-0 focus:border-accent focus:bg-white';

  // v3 · minimal ana sayfa: tek alan, tek düğme. Benzerler ve şıklar yalnızca istenince.
  // Kutudaki ders/numara overlay'leri 2+ kelimeden sonra (ya da değer girildiyse) görünür
  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
  // Künye (kurul, ders, sene, no) yalnız soru kökü yazılınca sorulur
  const showMeta = mode !== 'option' && (texts.stem.trim().length > 0 || !!linkedQuestion);
  const filledOptionCount = KEYS.filter((k) => options[k].trim()).length;

  // Eşleşen taslak varsa ders ve numara otomatik dolar; elle girilen değer korunur
  useEffect(() => {
    const top = realtimeMatches[0];
    if (!top || top.isCrossCommittee || top.compatibility.score < 60) return;
    if (!userManualNumber && top.question.questionNumber) { setQuestionNumber(String(top.question.questionNumber)); setAutoNum(true); }
    if (!userManualDiscipline && top.question.discipline && disciplines.includes(top.question.discipline)) {
      matchedDiscRef.current = true;
      if (top.question.discipline !== disciplineRef.current) setDiscipline(top.question.discipline);
      setAutoDisc(true);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [realtimeMatches]);

  // "Bunu mu kastettiniz?": derlem sözlüğüne göre yazım önerisi (2+ kelime)
  const [spell, setSpell] = useState<{ text: string | null; changes: { from: string; to: string }[] } | null>(null);
  const [dismissedSpell, setDismissedSpell] = useState<string | null>(null);
  useEffect(() => {
    const q = debouncedText;
    if (mode === 'option' || q.split(/\s+/).length < 2) { setSpell(null); return; }
    const ctrl = new AbortController();
    const t = window.setTimeout(() => {
      ApiService.suggestSpelling(q, ctrl.signal).then((r) => {
        if (ctrl.signal.aborted || !r?.text) { if (!ctrl.signal.aborted) setSpell(null); return; }
        // Öneri yazılmakta olan metne uygulanır: yalnızca değişen sözcükler değiştirilir
        let next = text;
        r.changes.forEach((c) => { next = next.replace(new RegExp(`(^|[^\\p{L}])${c.from.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?=$|[^\\p{L}])`, 'u'), `$1${c.to}`); });
        setSpell(next !== text ? { text: next, changes: r.changes } : null);
      });
    }, 350);
    return () => { ctrl.abort(); window.clearTimeout(t); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debouncedText, mode]);

  // Telefonda yazma alanı tam ekran açılır (animasyonla), kapatınca yerine animasyonla döner; geri tuşu da kapatır
  const [full, setFull] = useState<false | 'open' | 'closing'>(false);
  const fullRef = React.useRef(full);
  fullRef.current = full;
  const openFull = () => {
    if (fullRef.current || !window.matchMedia('(max-width: 767px)').matches) return;
    setFull('open');
    try { window.history.pushState({ ...(window.history.state || {}), msComposer: 1 }, ''); } catch { /* yok */ }
  };
  const finishClose = () => {
    setFull('closing');
    window.setTimeout(() => setFull(false), 240);
    (document.activeElement as HTMLElement | null)?.blur?.();
  };
  const closeFull = () => {
    if (fullRef.current !== 'open') return;
    if (window.history.state?.msComposer) window.history.back();
    else finishClose();
  };
  useEffect(() => {
    const onPop = () => { if (fullRef.current === 'open') finishClose(); };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);
  useEffect(() => {
    if (!full) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = prev; };
  }, [full]);
  // Gönderim başarılı olunca (metin temizlenir) tam ekran kapanır
  useEffect(() => {
    if (full === 'open' && successMessage && !texts.stem.trim() && !texts.clue.trim()) closeFull();
  }, [successMessage, texts]); // eslint-disable-line react-hooks/exhaustive-deps

  if (isV3) {
    return (
      <div className="w-full max-w-[760px] mx-auto lg:mx-0 flex flex-col gap-5 pt-4 sm:pt-8">
        <LoveNote />
        <div className="flex flex-col items-center text-center lg:items-start lg:text-left gap-2">
          <span className="inline-flex items-center text-[13px] text-ink-3">
            <span className={`w-1.5 h-1.5 rounded-full mr-2 ${isCollecting ? 'bg-ok-bright' : 'bg-line-2'}`} aria-hidden="true" />
            {committee ? titleCase(committee) : 'Kurul'}{isCollecting ? ' · toplama açık' : ''}
          </span>
          <h1 className="ms-page-title m-0 text-[30px] sm:text-[36px] text-ink">Aklında ne kaldı?</h1>
          {isLocked && (
            <div className="ms-pop-in flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-300/80 text-amber-900 text-[12.5px] font-medium mt-1">
              <Lock className="w-3.5 h-3.5 text-amber-600 shrink-0" />
              <span>Ders programına göre sınav tamamlanmadan bu kurula soru yazılamaz.</span>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} aria-busy={isSubmitting} className="relative flex flex-col gap-3">
          <BlurOverlay show={isSubmitting} label="Havuza ekleniyor…" hint="Benzer parçalar varsa aynı soruya bağlıyoruz" />
          {mode === 'option' ? (
            <div className="bg-white rounded-2xl p-3 shadow-sm">
              <OptionsEditor
                options={options}
                onChange={(k, v) => setOptions((p) => ({ ...p, [k]: v }))}
                count={optionCount}
                onCountChange={setOptionCount}
                answer={claimedAnswer}
                onAnswerChange={setClaimedAnswer}
                reason={answerReason}
                onReasonChange={setAnswerReason}
              />
            </div>
          ) : (
            <>
              <label htmlFor="hatira" className="sr-only">Hatırladığın kısım</label>
              <div className={`ms-composer ${showMeta ? 'has-meta' : ''} ${full ? `is-full ${full === 'closing' ? 'is-closing' : ''}` : ''}`}>
                {full && (
                  <div className="ms-composer-top">
                    <button type="button" className="ms-composer-close" onClick={closeFull} aria-label="Kapat">
                      <ChevronDown />
                    </button>
                    <span className="ms-composer-title">{mode === 'clue' ? 'İpucu' : 'Aklında ne kaldı?'}</span>
                    <button type="submit" className="ms-composer-send" disabled={isSubmitting || isLocked || !text.trim()}>
                      {isSubmitting ? 'Ekleniyor…' : 'Ekle'}
                    </button>
                  </div>
                )}
                <textarea
                  id="hatira"
                  rows={4}
                  value={text}
                  onFocus={openFull}
                  onChange={(e) => setText(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                      e.preventDefault();
                      e.currentTarget.form?.requestSubmit();
                    }
                  }}
                  placeholder="Tek kelime bile işe yarar…"
                  className="ms-bare-input w-full block resize-none px-4 pt-3.5 pb-2 text-[16px] leading-[1.6] text-ink placeholder:text-ink-3 bg-transparent border-0 outline-0 min-h-[128px]"
                />
                {/* Alt şerit: soru kimliği. Ders ve numara akıllı etiketler; otomatik dolanlar işaretli */}
                {showMeta && (
                  <div className="ms-meta" data-no-tip>
                    <MetaPicker variant="token" label="Kurul" icon={Layers} value={committee ? titleCase(committee) : 'Kurul'} width={280}>
                      {(close) => (
                        <ul className="qa-list" role="listbox" aria-label="Kurul">
                          {sortedCommittees.map((c) => {
                            const locked = isCommitteeLocked(c.id);
                            const on = c.id === committee?.id;
                            return (
                              <li key={c.id}>
                                <button type="button" role="option" aria-selected={on} disabled={locked} className={on ? 'is-on' : ''} onClick={() => { onSelectCommittee(c.id); close(); }}>
                                  <i className={`qa-dot ${c.id === activeCommitteeId ? 'is-live' : ''}`} aria-hidden />
                                  <span className="qa-list-t">{titleCase(c)}</span>
                                  <small>{locked ? <><Lock aria-hidden /> açılmadı</> : c.id === activeCommitteeId ? 'toplama açık' : ''}</small>
                                  {on && <Check className="qa-list-ok" aria-hidden />}
                                </button>
                              </li>
                            );
                          })}
                        </ul>
                      )}
                    </MetaPicker>
                    <MetaPicker variant="token" label="Ders" icon={BookOpen} value={discipline} auto={autoDisc && !userManualDiscipline} width={300}>
                      {(close) => {
                        const list = disciplines.filter((d) => !discQuery || d.toLocaleLowerCase('tr').includes(discQuery.toLocaleLowerCase('tr')));
                        return (
                          <>
                            {disciplines.length > 6 && (
                              <input autoFocus value={discQuery} onChange={(e) => setDiscQuery(e.target.value)} placeholder="Ders ara" aria-label="Ders ara" className="qa-pop-search" />
                            )}
                            <ul className="qa-list" role="listbox" aria-label="Ders">
                              {list.map((d) => (
                                <li key={d}>
                                  <button type="button" role="option" aria-selected={d === discipline} className={d === discipline ? 'is-on' : ''} onClick={() => { setDiscipline(d); setUserManualDiscipline(true); setAutoDisc(false); setDiscQuery(''); close(); }}>
                                    <span className="qa-list-t">{d}</span>
                                    {d === discipline && <Check className="qa-list-ok" aria-hidden />}
                                  </button>
                                </li>
                              ))}
                              {list.length === 0 && <li className="qa-list-empty">“{discQuery}” bu kurulun derslerinde yok.</li>}
                            </ul>
                          </>
                        );
                      }}
                    </MetaPicker>
                    <MetaPicker variant="token" label="Sene" icon={CalendarDays} value={((y: string) => (y ? `${y.slice(0, 4)}–${y.slice(7, 9)}` : 'Sene?'))(examYear)} empty={!examYear} width={300} title="Sorunun çıktığı sınavın öğretim yılı">
                      {(close) => (
                        <div className="qa-years">
                          <div className="qa-years-grid" role="listbox" aria-label="Öğretim yılı">
                            {academicYears().map((y) => (
                              <button key={y} type="button" role="option" aria-selected={examYear === y} className={examYear === y ? 'is-on' : ''} onClick={() => { setExamYear(y); close(); }}>
                                {`${y.slice(0, 4)}–${y.slice(7, 9)}`}
                                {y === currentAcademicYear() && <small>bu yıl</small>}
                              </button>
                            ))}
                          </div>
                          <button type="button" className={`qa-years-none ${!examYear ? 'is-on' : ''}`} onClick={() => { setExamYear(''); close(); }}>Bilmiyorum</button>
                        </div>
                      )}
                    </MetaPicker>
                    <label className={`ms-meta-token is-number ${autoNum && !userManualNumber ? 'is-auto' : ''}`} title="Soru numarası (bilmiyorsan boş bırak)">
                      <span className="opacity-70">No</span>
                      <input
                        type="text"
                        inputMode="numeric"
                        value={questionNumber}
                        onChange={(e) => { setQuestionNumber(e.target.value.replace(/[^0-9]/g, '').slice(0, 3)); setUserManualNumber(true); setAutoNum(false); }}
                        placeholder="—"
                        aria-label="Soru numarası (bilmiyorsan boş bırak)"
                      />
                      {autoNum && !userManualNumber && <Sparkles className="ms-meta-auto w-3 h-3 shrink-0" aria-label="otomatik" />}
                    </label>
                    {(autoDisc || autoNum) && !(userManualDiscipline && userManualNumber) && (
                      <span className="hidden sm:inline ml-auto text-[12px] text-ink-3 truncate">Eşleşen taslaktan dolduruldu</span>
                    )}
                  </div>
                )}
              </div>
              {spell?.text && spell.text !== dismissedSpell && (
                <div className="ms-pop-in flex items-center gap-2 text-[14px] text-ink-2 min-w-0">
                  <span className="shrink-0 text-ink-3">Bunu mu kastettiniz?</span>
                  <button
                    type="button"
                    onClick={() => { setText(spell.text!); setSpell(null); }}
                    className="min-w-0 truncate text-left text-accent font-medium hover:underline cursor-pointer"
                  >
                    {spell.changes.map((c) => c.to).join(', ')}
                  </button>
                  <button type="button" onClick={() => setDismissedSpell(spell.text)} aria-label="Öneriyi kapat" className="shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-ink-3 hover:bg-field cursor-pointer">
                    <X className="w-3.5 h-3.5" />
                  </button>
                </div>
              )}
              {/* Canlı arama mikro-animasyonu / yükleme göstergesi */}
              {isSearching && text.trim().length >= 6 && (
                <div className="ms-fade-in flex items-center gap-2 px-3 py-1.5 rounded-xl bg-accent-soft/60 border border-accent/20 text-accent text-[12px] font-medium w-fit">
                  <span className="w-2 h-2 rounded-full bg-accent animate-ping" />
                  <span className="flex items-center gap-1">
                    <Sparkles className="w-3.5 h-3.5 animate-spin" />
                    Benzer soru, kurul ve taslaklar taranıyor…
                  </span>
                </div>
              )}

              {/* Seçili Soruya / Taslağa Bağlandı Rozeti */}
              {linkedQuestion && (
                <div className="ms-pop-in flex items-center justify-between gap-2 px-3.5 py-2 rounded-xl bg-teal-50 border border-teal-200 text-teal-900 text-[13px]">
                  <div className="flex items-center gap-2 min-w-0">
                    <Link2 className="w-4 h-4 text-teal-600 shrink-0" />
                    <span className="font-semibold text-teal-950 truncate">
                      {linkedQuestion.questionNumber ? `Soru #${linkedQuestion.questionNumber} ile bağlandı` : 'Mevcut taslakla bağlandı'}
                    </span>
                    <span className="text-teal-700 text-[12px] hidden sm:inline truncate">
                      (Yazdıkların bu sorunun katkılarına eklenecek)
                    </span>
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      setLinkedQuestion(null);
                      setQuestionNumber('');
                    }}
                    className="p-1 text-teal-700 hover:text-teal-950 hover:bg-teal-100 rounded-lg cursor-pointer transition-colors shrink-0"
                    title="Bağlantıyı kaldır"
                  >
                    <X className="w-3.5 h-3.5" />
                  </button>
                </div>
              )}
            </>
          )}

          {/* Akıllı Kurul & Ders Öneri ve Uyarı Kutusu */}
          {smartAssistant && mode !== 'option' && (smartAssistant.crossCommitteeWarning || smartAssistant.suggestedTopics.length > 0) && (
            <div className="ms-pop-in rounded-2xl bg-amber-500/10 border border-amber-300/80 p-3.5 flex flex-col gap-2.5">
              {smartAssistant.crossCommitteeWarning && smartAssistant.predictedCommittee && (
                <div className="flex items-start justify-between gap-3 flex-wrap sm:flex-nowrap">
                  <div className="flex items-start gap-2 text-[13px] text-amber-950 leading-snug">
                    <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-bold">Kurul Uyuşmazlığı Olabilir: </span>
                      {smartAssistant.crossCommitteeWarning}
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      if (smartAssistant.predictedCommittee) {
                        onSelectCommittee(smartAssistant.predictedCommittee.committeeId);
                        if (smartAssistant.predictedDiscipline) {
                          setDiscipline(smartAssistant.predictedDiscipline.discipline);
                        }
                        toast.success('Kurul Değiştirildi', `${smartAssistant.predictedCommittee.committeeName} kuruluna geçildi.`);
                      }
                    }}
                    className="shrink-0 h-8 px-3 rounded-xl bg-amber-600 hover:bg-amber-700 text-white text-[12px] font-bold inline-flex items-center gap-1 cursor-pointer transition-colors shadow-xs"
                  >
                    Bu Kurula Geç
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              )}

              {/* Tespit Edilen Tıbbi Konular / Kavramlar */}
              {smartAssistant.suggestedTopics.length > 0 && (
                <div className="flex items-center gap-1.5 flex-wrap pt-0.5">
                  <span className="text-[11.5px] font-bold uppercase tracking-wider text-amber-900/80 flex items-center gap-1">
                    <Sparkles className="w-3 h-3 text-amber-600" />
                    İlişkili Konu Önerileri:
                  </span>
                  {smartAssistant.suggestedTopics.slice(0, 3).map((st, i) => (
                    <span
                      key={i}
                      className="h-6 px-2.5 rounded-full bg-white text-amber-950 text-[12px] font-semibold border border-amber-200 shadow-2xs inline-flex items-center gap-1"
                    >
                      {st.topic}
                    </span>
                  ))}
                  {smartAssistant.predictedDiscipline && discipline !== smartAssistant.predictedDiscipline.discipline && (
                    <button
                      type="button"
                      onClick={() => setDiscipline(smartAssistant.predictedDiscipline!.discipline)}
                      className="h-6 px-2.5 rounded-full bg-accent/15 hover:bg-accent/25 text-accent text-[12px] font-bold border border-accent/30 inline-flex items-center gap-1 cursor-pointer transition-colors"
                      title="Dersi otomatik eşle"
                    >
                      Dersi "{smartAssistant.predictedDiscipline.discipline}" yap
                    </button>
                  )}
                </div>
              )}
            </div>
          )}

          {realtimeMatches.length > 0 && mode !== 'option' && (
            <div className="flex flex-col gap-2.5">
              <div className="flex items-center justify-between gap-2 px-1">
                <span className="flex items-center gap-1.5 text-[12px] font-bold uppercase tracking-wider text-ink-3">
                  <Sparkles className="w-3.5 h-3.5 text-accent animate-pulse" />
                  Benzer Taslaklar ({realtimeMatches.length})
                </span>
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={selectedMatchIds.size === realtimeMatches.length ? clearSelection : selectAllMatches}
                    className="text-[12px] font-semibold text-accent hover:underline cursor-pointer"
                  >
                    {selectedMatchIds.size === realtimeMatches.length ? 'Seçimi Bırak' : 'Tümünü Seç'}
                  </button>
                </div>
              </div>

              {/* Benzer sorular listesi: En belirgin soru ilk sırada */}
              <div className="flex flex-col gap-2">
                {realtimeMatches.map((m, idx) => {
                  const q = m.question;
                  const stem = questionStemText(q);
                  const isTop = idx === 0;
                  const isSelected = selectedMatchIds.has(q.id);
                  const tier = getScoreTier(m.compatibility.score);

                  return (
                    <div
                      key={q.id}
                      className={`ms-pop-in rounded-2xl border transition-all p-3.5 flex flex-col gap-2 relative ${
                        isSelected
                          ? 'border-accent bg-accent-soft/30 shadow-xs ring-1 ring-accent'
                          : tier.cardBorder
                      }`}
                      style={{ animationDelay: `${idx * 60}ms` }}
                    >
                      <div className="flex items-center justify-between gap-2 flex-wrap">
                        <div className="flex items-center gap-2 flex-wrap">
                          <button
                            type="button"
                            onClick={() => toggleSelectMatch(q.id)}
                            className="cursor-pointer text-ink-2 hover:text-ink focus:outline-none"
                            title={isSelected ? 'Seçimi Kaldır' : 'Seç'}
                            aria-label={`Soru ${q.questionNumber || 'taslak'} seç`}
                          >
                            {isSelected ? (
                              <CheckSquare className="w-4 h-4 text-accent fill-accent-soft" />
                            ) : (
                              <Square className="w-4 h-4 text-ink-3 hover:text-ink" />
                            )}
                          </button>

                          {isTop && (
                            <span className="h-5 px-2 rounded-full bg-accent text-white text-[11px] font-bold uppercase tracking-wider">
                              En Yakın
                            </span>
                          )}

                          <span className={`h-6 px-2.5 rounded-full text-[12px] font-semibold inline-flex items-center gap-1 border ${tier.pillBg}`}>
                            <span className={`w-1.5 h-1.5 rounded-full ${tier.barColor}`} />
                            %{m.compatibility.score} · {tier.tierName}
                          </span>

                          {m.isCrossCommittee && (
                            <span className="h-5 px-2 rounded-full bg-purple-600 text-white text-[11px] font-bold uppercase tracking-wider">
                              Farklı Kurul Taslağı
                            </span>
                          )}

                          {m.contextHashtag && (
                            <ContextBadge hashtag={m.contextHashtag} colorIndex={idx} />
                          )}
                        </div>

                        <span className="text-[12px] font-mono font-bold text-ink-2">
                          {q.questionNumber ? `Soru #${q.questionNumber}` : 'Numarasız'}
                        </span>
                      </div>

                      <div className="text-[13px] leading-relaxed text-ink bg-white/90 rounded-xl p-2.5 border border-line-soft">
                        <Colored text={stem} colors={sharedColors} />
                      </div>

                      <div className="flex items-center justify-between gap-2 pt-1">
                        <div className="flex items-center gap-1.5 flex-wrap">
                          <button
                            type="button"
                            onClick={() => handleLinkToQuestion(q)}
                            className="h-7 px-2.5 rounded-lg bg-white hover:bg-canvas text-ink text-[12px] font-medium border border-line inline-flex items-center gap-1 cursor-pointer transition-colors shadow-2xs"
                          >
                            <CheckCircle2 className="w-3.5 h-3.5 text-accent" />
                            {q.questionNumber ? `S.${q.questionNumber} ile Bağla` : 'Bu Taslakla Bağla'}
                          </button>
                          <button
                            type="button"
                            onClick={() => setOptimizingQuestion(q)}
                            className="h-7 px-2.5 rounded-lg bg-accent-soft hover:bg-accent/20 text-accent text-[12px] font-semibold inline-flex items-center gap-1 cursor-pointer transition-colors shadow-2xs"
                            title="Taslağı amfi slaytları ve AI ile tam soruya dönüştür"
                          >
                            <Wand2 className="w-3.5 h-3.5" />
                            AI ile Dönüştür
                          </button>
                        </div>
                        {q.discipline && (
                          <span className="text-[11.5px] text-ink-3 truncate">{q.discipline}</span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Ortak kelimeler renk kılavuzu */}
              <WordLegend texts={[text, ...realtimeMatches.map((m) => questionStemText(m.question))]} colors={sharedColors} />

              {/* Seçim yapıldığında ortaya çıkan bağlamsal çubuk */}
              {selectedMatchIds.size > 0 && (
                <div className="ms-pop-in sticky bottom-3 z-20 flex items-center justify-between gap-3 p-3 rounded-2xl bg-ink text-white shadow-xl border border-white/10 backdrop-blur-md">
                  <div className="flex items-center gap-2 min-w-0">
                    <span className="w-6 h-6 rounded-full bg-accent text-white text-[12px] font-bold flex items-center justify-center shrink-0">
                      {selectedMatchIds.size}
                    </span>
                    <span className="text-[13px] font-medium truncate">
                      {selectedMatchIds.size === 1
                        ? '1 soru seçildi'
                        : `${selectedMatchIds.size} soru seçildi`}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <button
                      type="button"
                      onClick={clearSelection}
                      className="h-8 px-2.5 rounded-lg hover:bg-white/10 text-white/80 hover:text-white text-[12px] font-medium cursor-pointer transition-colors"
                    >
                      İptal
                    </button>
                    <button
                      type="button"
                      disabled={isMergingSelected}
                      onClick={handleMergeAndGroupSelected}
                      className="h-8 px-3.5 rounded-lg bg-accent hover:bg-accent-hover text-white text-[12.5px] font-bold inline-flex items-center gap-1.5 cursor-pointer shadow-md disabled:opacity-50 transition-colors"
                    >
                      <Layers className="w-3.5 h-3.5" />
                      {isMergingSelected
                        ? 'Birleştiriliyor…'
                        : selectedMatchIds.size === 1
                        ? 'Bu Soru ile Birleştir'
                        : `Seçilenleri Gruplandır & Birleştir (${selectedMatchIds.size})`}
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {similar.length > 0 && mode !== 'option' && (
            <button
              type="button"
              onClick={() => setSimOpen((v) => !v)}
              aria-expanded={simOpen}
              className="ms-pop-in w-full min-h-11 px-4 rounded-2xl bg-field hover:bg-line flex items-center gap-3 text-left text-[14px] cursor-pointer"
            >
              <span className="h-6 min-w-6 px-2 rounded-full bg-accent-soft text-accent text-[12px] font-semibold inline-flex items-center justify-center">
                {similar.length}
              </span>
              <span className="flex-1 text-ink-2">benzer çıkmış soru bulundu</span>
              <span className="text-[13px] text-ink-3">{simOpen ? 'Gizle' : 'Göster'}</span>
            </button>
          )}
          {simOpen && similar.length > 0 && mode !== 'option' && (
            <ul className="list-none m-0 p-0 flex flex-col gap-2">
              {similar.map((s, i) => (
                <li
                  key={s.id}
                  className="ms-pop-in p-3 rounded-xl bg-field/60 border border-line-soft hover:bg-field text-[14px] text-ink flex flex-col gap-2"
                  style={{ animationDelay: `${i * 60}ms` }}
                >
                  <div className="flex flex-col gap-0.5 min-w-0">
                    <span className="line-clamp-2 text-ink-2 font-medium">{s.stem}</span>
                    {s.options && s.options.length > 0 && (
                      <ol className="m-0 mt-1 p-0 list-none grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-0.5 text-[13px] text-ink-2">
                        {s.options.map((o) => (
                          <li key={o.key} className={`min-w-0 truncate ${o.key === s.claimedAnswer ? 'text-ok font-semibold' : ''}`}>
                            <span className="font-mono text-ink-3 mr-1">{o.key})</span>{o.text}
                          </li>
                        ))}
                      </ol>
                    )}
                    <span className="text-[12px] text-ink-3">
                      {[s.discipline, s.examYear ? `Çıkmış ${s.examYear}` : 'Çıkmış', s.claimedAnswer ? `Cevap: ${s.claimedAnswer}` : ''].filter(Boolean).join(' · ')}
                    </span>
                  </div>
                  <div className="flex items-center gap-2 pt-1 border-t border-line-soft">
                    <button
                      type="button"
                      onClick={() => handleTransferEntireQuestion(s)}
                      className="h-7 px-2.5 rounded-lg bg-accent text-white text-[12px] font-semibold inline-flex items-center gap-1 cursor-pointer hover:bg-accent-hover shadow-2xs transition-colors"
                      title="Sorunun kökünü, branşını ve şıklarını editöre aktar"
                    >
                      <FileText className="w-3.5 h-3.5" />
                      {s.options && s.options.length ? 'Kök + şıkları aktar' : 'Soruyu aktar'}
                    </button>
                    <button
                      type="button"
                      onClick={() => handleCopyQuestionStem(s.stem)}
                      className="h-7 px-2.5 rounded-lg bg-white text-ink text-[12px] font-medium border border-line inline-flex items-center gap-1 cursor-pointer hover:bg-canvas shadow-2xs transition-colors"
                      title="Yalnızca soru kökünü editöre yaz ve panoya kopyala"
                    >
                      <Copy className="w-3.5 h-3.5 text-accent" />
                      Yalnızca Kökü Al
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}

          <div className="flex items-center gap-2 text-[13px] text-ink-3">
            <span className="flex-1" />
            {/* Şık ekle: gönder düğmesinin solunda küçük baloncuk */}
            <button
              type="button"
              onClick={() => setMode(mode === 'option' ? 'stem' : 'option')}
              aria-pressed={mode === 'option'}
              className={`ms-opt-bubble ${mode === 'option' || filledOptionCount > 0 ? 'is-on' : ''}`}
            >
              {mode === 'option' ? (
                <>Köke dön</>
              ) : filledOptionCount > 0 ? (
                <>{filledOptionCount} şık{claimedAnswer ? ` · ${claimedAnswer}` : ''}</>
              ) : (
                <><Plus className="w-3.5 h-3.5" strokeWidth={2.4} /> Şık</>
              )}
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="h-12 sm:h-11 px-6 rounded-full bg-accent hover:bg-accent-hover text-white text-[15px] sm:text-[14.5px] font-semibold cursor-pointer disabled:opacity-60 transition-colors shrink-0"
            >
              {isSubmitting ? 'Kaydediliyor…' : 'Havuza ekle'}
            </button>
          </div>

          {formError && (
            <div role="alert" className="ms-shake px-4 py-3 rounded-2xl bg-bad-soft text-bad-text text-[14px]">{formError}</div>
          )}
          {successMessage && (
            <div role="status" className="ms-pop-in px-4 py-3 rounded-2xl bg-ok-soft text-ok text-[14px] font-medium">Teşekkürler! {successMessage}</div>
          )}
        </form>

        {optimizingQuestion && (
          <AiQuestionOptimizerModal
            question={optimizingQuestion}
            isOpen={Boolean(optimizingQuestion)}
            onClose={() => setOptimizingQuestion(null)}
            currentUser={currentUser}
            onSaved={async (updated) => {
              setOptimizingQuestion(null);
              toast.success('Taslak Geliştirildi', `Soru #${updated.questionNumber || 'taslak'} başarıyla güncellendi.`);
              if (onQuestionsUpdated) {
                await onQuestionsUpdated();
              }
            }}
          />
        )}
      </div>
    );
  }


  return (
    <div className="w-full grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_340px] gap-4 lg:gap-5 md:pt-2">
      <div className="flex flex-col gap-3 min-w-0">
      {/* Başlık + kurul (tasarım: sola hizalı, kompakt) */}
      <div className="flex flex-wrap items-end justify-between gap-x-4 gap-y-2">
        <div className="flex flex-col gap-1.5 min-w-0">
        <label className="relative inline-flex items-center">
          <span className="sr-only">Kurul seç</span>
          <span
            className={`pointer-events-none absolute left-3 w-2 h-2 rounded-full ${isCollecting ? 'bg-ok-bright' : 'bg-line-2'}`}
            aria-hidden="true"
          />
          <select
            value={committee?.id || ''}
            onChange={(e) => onSelectCommittee(e.target.value)}
            className={`appearance-none h-8 pl-7 pr-8 rounded-full text-[13px] font-semibold cursor-pointer border-0 outline-0 ${
              isCollecting ? 'bg-ok-soft text-ok' : 'bg-white text-ink-2 ring-1 ring-inset ring-line'
            }`}
          >
            {sortedCommittees.map((c) => {
              const locked = isCommitteeLocked(c.id);
              return (
                <option key={c.id} value={c.id} disabled={locked}>
                  {titleCase(c)}
                  {c.id === activeCommitteeId ? ' · toplama açık' : ''}
                  {locked ? ' · (Henüz Açılmadı)' : ''}
                </option>
              );
            })}
          </select>
          <ChevronDown className="pointer-events-none absolute right-2.5 w-3.5 h-3.5 opacity-70" aria-hidden="true" />
        </label>
        {isLocked && (
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-300 text-amber-900 text-[12px] font-semibold">
            <Lock className="w-3 h-3 text-amber-600" />
            Sınav tamamlanmadan bu kurula soru eklenemez
          </span>
        )}
        <span className="ms-eyebrow">Soru ekle</span>
        <h1 className="ms-page-title m-0 text-[24px] sm:text-[28px] text-ink">Hatırladığın soruyu yaz</h1>
        </div>
        <p className="m-0 text-[13px] text-ink-3">Parça parça da olur; gerisini kaynaklardan tamamlarız.</p>
      </div>

      {/* Composer */}
      <form
        onSubmit={handleSubmit}
        aria-busy={isSubmitting}
        className="relative bg-white border border-line rounded-xl p-3 sm:p-5 flex flex-col gap-3"
      >
        <BlurOverlay show={isSubmitting} label="Havuza ekleniyor…" hint="Benzer parçalar varsa aynı soruya bağlıyoruz" />
        <div role="radiogroup" aria-label="Ne ekliyorsun?" className="grid grid-cols-3 gap-1 bg-canvas rounded-xl p-1">
          {MODES.map((m) => {
            const on = mode === m.id;
            return (
              <button
                key={m.id}
                type="button"
                role="radio"
                aria-checked={on}
                onClick={() => setMode(m.id)}
                className={`h-9 rounded-lg text-[13.5px] sm:text-[14px] whitespace-nowrap cursor-pointer transition-colors inline-flex items-center justify-center gap-1.5 ${
                  on ? 'bg-white text-ink font-semibold shadow-xs' : 'text-ink-2 hover:text-ink'
                }`}
              >
                {m.label}
                {m.id === 'option' && claimedAnswer && (
                  <span className="h-5 min-w-5 px-1 rounded-full bg-ok text-white text-[11px] font-mono font-semibold inline-flex items-center justify-center" aria-label={`Cevap ${claimedAnswer}`}>
                    {claimedAnswer}
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {mode === 'option' ? (
          <OptionsEditor
            options={options}
            onChange={(k, v) => setOptions((p) => ({ ...p, [k]: v }))}
            count={optionCount}
            onCountChange={setOptionCount}
            answer={claimedAnswer}
            onAnswerChange={setClaimedAnswer}
            reason={answerReason}
            onReasonChange={setAnswerReason}
          />
        ) : (
          <>
            <label htmlFor="hatira" className="sr-only">
              Hatırladığın kısım
            </label>
            <textarea
              id="hatira"
              rows={4}
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder={PLACEHOLDERS[mode]}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                  e.preventDefault();
                  e.currentTarget.form?.requestSubmit();
                }
              }}
              className={`resize-y rounded-[10px] px-3.5 py-3 text-[15px] leading-[1.6] text-ink placeholder:text-ink-3 min-h-[132px] sm:min-h-[150px] ${field}`}
            />
            <div className="flex items-center justify-between gap-1.5 text-[12px] text-ink-3 -mt-1 flex-wrap">
              <div className="flex items-center gap-1.5">
                <span className="font-mono">{text.length} karakter</span>
                <span aria-hidden="true">·</span>
                <span className="truncate">Şıkları “Şıklar” sekmesinden ekleyebilirsin</span>
              </div>
              {/* Canlı arama mikro-animasyonu / yükleme göstergesi */}
              {isSearching && text.trim().length >= 6 && (
                <div className="ms-fade-in flex items-center gap-1.5 text-accent text-[11.5px] font-medium">
                  <Sparkles className="w-3.5 h-3.5 animate-spin" />
                  <span>Eşleşmeler taranıyor…</span>
                </div>
              )}
            </div>

            {/* Seçili Soruya / Taslağa Bağlandı Rozeti */}
            {linkedQuestion && (
              <div className="ms-pop-in flex items-center justify-between gap-2 px-3.5 py-2 rounded-xl bg-teal-50 border border-teal-200 text-teal-900 text-[13px]">
                <div className="flex items-center gap-2 min-w-0">
                  <Link2 className="w-4 h-4 text-teal-600 shrink-0" />
                  <span className="font-semibold text-teal-950 truncate">
                    {linkedQuestion.questionNumber ? `Soru #${linkedQuestion.questionNumber} ile bağlandı` : 'Mevcut taslakla bağlandı'}
                  </span>
                  <span className="text-teal-700 text-[12px] hidden sm:inline truncate">
                    (Yazdıkların bu sorunun katkılarına eklenecek)
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    setLinkedQuestion(null);
                    setQuestionNumber('');
                  }}
                  className="p-1 text-teal-700 hover:text-teal-950 hover:bg-teal-100 rounded-lg cursor-pointer transition-colors shrink-0"
                  title="Bağlantıyı kaldır"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
            )}
          </>
        )}

        {realtimeMatches.length > 0 && mode !== 'option' && (
          <div className="flex flex-col gap-2.5">
            <div className="flex items-center justify-between gap-2 px-1">
              <span className="flex items-center gap-1.5 text-[12px] font-bold uppercase tracking-wider text-ink-3">
                <Sparkles className="w-3.5 h-3.5 text-accent animate-pulse" />
                Benzer / Devamı Olan Taslaklar ({realtimeMatches.length})
              </span>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={selectedMatchIds.size === realtimeMatches.length ? clearSelection : selectAllMatches}
                  className="text-[12px] font-semibold text-accent hover:underline cursor-pointer"
                >
                  {selectedMatchIds.size === realtimeMatches.length ? 'Seçimi Bırak' : 'Tümünü Seç'}
                </button>
              </div>
            </div>

            {/* Benzer sorular listesi: En belirgin soru ilk sırada */}
            <div className="flex flex-col gap-2.5">
              {realtimeMatches.map((m, idx) => {
                const q = m.question;
                const stem = questionStemText(q);
                const isTop = idx === 0;
                const isSelected = selectedMatchIds.has(q.id);
                const tier = getScoreTier(m.compatibility.score);

                return (
                  <div
                    key={q.id}
                    className={`ms-pop-in rounded-xl border transition-all p-3.5 sm:p-4 flex flex-col gap-2.5 relative shadow-2xs ${
                      isSelected
                        ? 'border-accent bg-accent-soft/30 ring-1 ring-accent'
                        : tier.cardBorder
                    }`}
                    style={{ animationDelay: `${idx * 60}ms` }}
                  >
                    <div className="flex items-center justify-between gap-2 flex-wrap">
                      <div className="flex items-center gap-2 flex-wrap">
                        <button
                          type="button"
                          onClick={() => toggleSelectMatch(q.id)}
                          className="cursor-pointer text-ink-2 hover:text-ink focus:outline-none"
                          title={isSelected ? 'Seçimi Kaldır' : 'Seç'}
                          aria-label={`Soru ${q.questionNumber || 'taslak'} seç`}
                        >
                          {isSelected ? (
                            <CheckSquare className="w-4 h-4 text-accent fill-accent-soft" />
                          ) : (
                            <Square className="w-4 h-4 text-ink-3 hover:text-ink" />
                          )}
                        </button>

                        {isTop && (
                          <span className="h-5 px-2 rounded-full bg-accent text-white text-[11px] font-bold uppercase tracking-wider">
                            En Yakın
                          </span>
                        )}

                        <span className={`h-6 px-2.5 rounded-full text-[12px] font-semibold inline-flex items-center gap-1.5 border ${tier.pillBg}`}>
                          <span className={`w-1.5 h-1.5 rounded-full ${tier.barColor}`} />
                          %{m.compatibility.score} uyum · {tier.tierName}
                        </span>

                        {m.contextHashtag && (
                          <ContextBadge hashtag={m.contextHashtag} colorIndex={idx} />
                        )}
                      </div>

                      <span className="text-[12px] font-mono font-bold text-ink-2">
                        {q.questionNumber ? `Soru #${q.questionNumber}` : 'Numarasız Taslak'}
                      </span>
                    </div>

                    <div className="text-[13.5px] leading-relaxed text-ink bg-white/95 rounded-xl p-3 border border-line-soft">
                      <div className="text-[11px] font-semibold uppercase tracking-wider text-ink-3 mb-1 flex items-center justify-between">
                        <span>Havuzdaki Taslak Metni:</span>
                        {q.discipline && (
                          <span className="font-normal text-[11.5px] text-ink-3">{q.discipline}</span>
                        )}
                      </div>
                      <p className="m-0 line-clamp-3">
                        <Colored text={stem} colors={sharedColors} />
                      </p>
                    </div>

                    <div className="flex flex-wrap items-center gap-2 pt-1 border-t border-line-soft/80">
                      <button
                        type="button"
                        onClick={() => handleLinkToQuestion(q)}
                        className="h-8 px-3 rounded-lg bg-white hover:bg-canvas text-ink text-[12.5px] font-semibold border border-line inline-flex items-center gap-1.5 cursor-pointer shadow-2xs transition-colors"
                      >
                        <CheckCircle2 className="w-3.5 h-3.5 text-accent" />
                        {q.questionNumber ? `Bu soruya bağla (S.${q.questionNumber})` : 'Bu taslağa bağla'}
                      </button>
                      <button
                        type="button"
                        onClick={() => setOptimizingQuestion(q)}
                        className="h-8 px-3 rounded-lg bg-accent-soft hover:bg-accent/20 text-accent text-[12px] font-semibold inline-flex items-center gap-1.5 cursor-pointer transition-colors shadow-2xs"
                        title="Taslağı amfi slaytları ve AI ile tam soruya dönüştür"
                      >
                        <Wand2 className="w-3.5 h-3.5" />
                        AI ile Dönüştür
                      </button>
                      <span className="text-[12px] text-ink-3">
                        veya çoklu seçim yapıp birleştirebilirsin.
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Ortak kelimeler renk kılavuzu */}
            <WordLegend texts={[text, ...realtimeMatches.map((m) => questionStemText(m.question))]} colors={sharedColors} />

            {/* Seçim yapıldığında ortaya çıkan bağlamsal çubuk */}
            {selectedMatchIds.size > 0 && (
              <div className="ms-pop-in sticky bottom-3 z-20 flex items-center justify-between gap-3 p-3 sm:p-3.5 rounded-2xl bg-ink text-white shadow-xl border border-white/10 backdrop-blur-md">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="w-6 h-6 rounded-full bg-accent text-white text-[12px] font-bold flex items-center justify-center shrink-0">
                    {selectedMatchIds.size}
                  </span>
                  <span className="text-[13px] font-medium truncate">
                    {selectedMatchIds.size === 1
                      ? '1 soru seçildi'
                      : `${selectedMatchIds.size} soru seçildi`}
                  </span>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <button
                    type="button"
                    onClick={clearSelection}
                    className="h-8 px-2.5 rounded-lg hover:bg-white/10 text-white/80 hover:text-white text-[12px] font-medium cursor-pointer transition-colors"
                  >
                    İptal
                  </button>
                  <button
                    type="button"
                    disabled={isMergingSelected}
                    onClick={handleMergeAndGroupSelected}
                    className="h-8 px-3.5 rounded-lg bg-accent hover:bg-accent-hover text-white text-[12.5px] font-bold inline-flex items-center gap-1.5 cursor-pointer shadow-md disabled:opacity-50 transition-colors"
                  >
                    <Layers className="w-3.5 h-3.5" />
                    {isMergingSelected
                      ? 'Birleştiriliyor…'
                      : selectedMatchIds.size === 1
                      ? 'Bu Soru ile Birleştir'
                      : `Seçilenleri Gruplandır & Birleştir (${selectedMatchIds.size})`}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {similar.length > 0 && mode !== 'option' && (
          <div className="flex flex-col gap-1" aria-live="polite">
            <span className="flex items-center gap-1.5 text-[11.5px] font-semibold uppercase tracking-[.06em] text-ink-3">
              Benzer çıkmış sorular
              <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" aria-hidden="true" />
            </span>
            {similar.map((s, i) => {
              // Ham arama puanı yüzde değildir: çubuk yalnızca en iyi sonuca göre göreli yakınlığı gösterir
              const top = similar[0]?.score || 0;
              const rel = top > 0 && typeof s.score === 'number' ? Math.max(8, Math.round((s.score / top) * 100)) : null;
              return (
                <details
                  key={s.id}
                  className="ms-pop-in group rounded-[10px] border border-line bg-white open:bg-canvas hover:border-accent transition-colors"
                  style={{ animationDelay: `${i * 70}ms` }}
                >
                  <summary className="list-none cursor-pointer min-h-10 px-2.5 py-1.5 flex items-center gap-2 text-[13px]">
                    {rel !== null && (
                      <span className="shrink-0 hidden sm:block w-9 h-1 rounded-full bg-line overflow-hidden" title="Göreli benzerlik">
                        <span className="block h-full bg-accent" style={{ width: `${rel}%` }} />
                      </span>
                    )}
                    <span className="min-w-0 flex-1 truncate group-open:whitespace-normal text-ink-2" title={s.stem}>
                      {s.stem}
                    </span>
                    <span className="shrink-0 text-[11px] font-semibold px-1.5 py-0.5 rounded-md bg-violet-50 text-violet-700">
                      {s.examYear ? `Çıkmış ${s.examYear}` : 'Çıkmış'}
                    </span>
                  </summary>
                  <div className="px-2.5 pb-2.5 flex flex-col gap-2 border-t border-line-soft pt-1.5">
                    <div className="text-[12px] text-ink-3">
                      {[s.discipline, s.title].filter(Boolean).join(' · ')}
                      {s.claimedAnswer ? ` · Cevap: ${s.claimedAnswer}` : ''}
                    </div>
                    <div className="flex items-center gap-2 pt-0.5">
                      <button
                        type="button"
                        onClick={() => handleTransferEntireQuestion(s)}
                        className="h-7 px-2.5 rounded-lg bg-accent text-white text-[12px] font-semibold inline-flex items-center gap-1 cursor-pointer hover:bg-accent-hover shadow-2xs transition-colors"
                        title="Sorunun kökünü, branşını ve şıklarını editöre aktar"
                      >
                        <FileText className="w-3.5 h-3.5" />
                        Soruyu Aktar
                      </button>
                      <button
                        type="button"
                        onClick={() => handleCopyQuestionStem(s.stem)}
                        className="h-7 px-2.5 rounded-lg bg-white text-ink text-[12px] font-medium border border-line inline-flex items-center gap-1 cursor-pointer hover:bg-canvas shadow-2xs transition-colors"
                        title="Yalnızca soru kökünü editöre yaz ve panoya kopyala"
                      >
                        <Copy className="w-3.5 h-3.5 text-accent" />
                        Yalnızca Kökü Al
                      </button>
                    </div>
                  </div>
                </details>
              );
            })}
          </div>
        )}

        <div className="flex flex-wrap sm:flex-nowrap items-center gap-2">
          <label className="relative flex-1 min-w-[150px]">
            <span className="sr-only">Ders</span>
            <select
              value={discipline}
              onChange={(e) => {
                setDiscipline(e.target.value);
                setUserManualDiscipline(true);
              }}
              className={`appearance-none w-full h-11 rounded-xl pl-3 pr-8 text-[14px] text-ink cursor-pointer truncate ${field}`}
            >
              {disciplines.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
            <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-3" aria-hidden="true" />
          </label>
          <label className="flex items-center gap-1.5 h-11 w-[104px] px-3 rounded-xl bg-field border border-transparent focus-within:border-accent focus-within:bg-white">
            <span className="text-[13px] text-ink-3">No</span>
            <input
              type="text"
              inputMode="numeric"
              value={questionNumber}
              onChange={(e) => {
                setQuestionNumber(e.target.value.replace(/[^0-9]/g, '').slice(0, 3));
                setUserManualNumber(true);
              }}
              placeholder="?"
              aria-label="Soru numarası (bilmiyorsan boş bırak)"
              className="w-full min-w-0 bg-transparent border-0 outline-0 text-[15px] font-mono placeholder:text-slate-600"
            />
          </label>
          <button
            type="submit"
            disabled={isSubmitting}
            className={`h-12 sm:h-11 px-5 rounded-xl text-white text-[15px] font-semibold flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60 w-full sm:w-auto transition-colors ${
              canSubmit ? 'bg-accent hover:bg-accent-hover shadow-md' : 'bg-accent/75'
            }`}
          >
            {isSubmitting ? 'Kaydediliyor…' : 'Havuza ekle'}
            <ArrowRight className="w-4 h-4" strokeWidth={2.2} />
          </button>
        </div>

        {formError && (
          <div role="alert" className="flex items-center gap-2 px-3 py-2.5 rounded-xl bg-bad-soft text-bad-text text-[14px]">
            <AlertCircle className="w-4 h-4 shrink-0 text-bad" />
            <span>{formError}</span>
          </div>
        )}
        {successMessage && (
          <div role="status" className="ms-pop-in flex items-center gap-3 px-3 py-2 rounded-xl bg-ok-tint border border-emerald-200">
            <SuccessCheck size={48} className="shrink-0 -my-1" />
            <span className="flex flex-col">
              <span className="text-[14.5px] font-semibold text-ok">Teşekkürler!</span>
              <span className="text-[13.5px] text-ink-2">{successMessage}</span>
            </span>
          </div>
        )}
      </form>

      </div>

      {/* Sağ sütun: bulunan kaynaklar, havuz durumu, kısayol */}
      <aside className="flex flex-col gap-3 min-w-0 lg:pt-[52px]">
        <section className="bg-white border border-line rounded-xl px-4 py-3" aria-live="polite">
          <h2 className="m-0 mb-1 text-[11px] font-semibold uppercase tracking-[.06em] text-ink-3">Bulunan kaynaklar</h2>
          {sources.length === 0 ? (
            <p className="m-0 py-2 text-[13px] text-ink-3">Yazmaya başlayınca soruna en yakın slayt, özet ve çıkmış sorular burada görünür.</p>
          ) : (
            <ul className="list-none m-0 p-0">
              {sources.map((src, i) => {
                const kind = SOURCE_KIND[src.documentType] || SOURCE_KIND.lecture_slide;
                return (
                  <li
                    key={`${src.documentId}-${src.pageNumber ?? i}`}
                    className="ms-pop-in flex items-center gap-2 py-2 border-t first:border-t-0 border-line text-[13px]"
                    style={{ animationDelay: `${i * 60}ms` }}
                    title={src.snippet}
                  >
                    <span className={`shrink-0 text-[11px] font-semibold px-1.5 py-0.5 rounded-md ${kind.cls}`}>{kind.label}</span>
                    <span className="min-w-0 flex-1 truncate text-ink">{src.title}</span>
                    {src.pageNumber ? <span className="shrink-0 text-[12px] text-ink-3 font-mono">s.{src.pageNumber}</span> : null}
                  </li>
                );
              })}
            </ul>
          )}
        </section>
      <a
        href={pathFor('questions')}
        onClick={linkClick(() => onNavigateTab('questions'))}
        className="group bg-white border border-line rounded-xl px-4 py-3 flex items-center gap-3 hover:border-line-2"
      >
        <span className="flex-1 min-w-0 flex flex-col gap-1.5">
          <span className="flex items-baseline gap-2 text-[14px] min-w-0">
            <span className="font-semibold text-ink shrink-0">{shortName} havuzu</span>
            <span className="font-mono text-ink-2 shrink-0">
              {completed}/{target}
            </span>
            <span className="text-ink-3 truncate">kuruldu · {drafts} taslak</span>
          </span>
          <span role="img" aria-label={`${completed} doğrulandı, ${drafts} taslak`} className="flex h-1.5 rounded-full overflow-hidden gap-[2px] bg-line-soft">
            {completed > 0 && <span className="bg-ok-bright" style={{ width: `${pctNum(completed)}%` }} />}
            {drafts > 0 && <span className="bg-amber-600" style={{ width: `${draftPct}%` }} />}
          </span>
        </span>
        <span className="text-[13px] font-semibold text-accent inline-flex items-center gap-0.5 shrink-0">
          Havuz
          <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
        </span>
      </a>
        <p className="hidden lg:block m-0 px-1 text-[12px] text-ink-3">
          Kısayol: <kbd className="font-mono border border-line rounded px-1">Ctrl</kbd> + <kbd className="font-mono border border-line rounded px-1">Enter</kbd> gönderir.
        </p>
      </aside>

      {optimizingQuestion && (
        <AiQuestionOptimizerModal
          question={optimizingQuestion}
          isOpen={Boolean(optimizingQuestion)}
          onClose={() => setOptimizingQuestion(null)}
          currentUser={currentUser}
          onSaved={async (updated) => {
            setOptimizingQuestion(null);
            toast.success('Taslak Geliştirildi', `Soru #${updated.questionNumber || 'taslak'} başarıyla güncellendi.`);
            if (onQuestionsUpdated) {
              await onQuestionsUpdated();
            }
          }}
        />
      )}
    </div>
  );
};
