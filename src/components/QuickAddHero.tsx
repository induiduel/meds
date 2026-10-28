import { FastTextarea } from './ui/FastTextarea';
import React, { useEffect, useMemo, useState } from 'react';
import {
  ArrowRight,
  CheckCircle2,
  ChevronLeft,
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
} from 'lucide-react';
import { Committee, QuestionItem } from '../types';
import { AppUser } from '../services/auth';
import { getDefaultActiveCommitteeId, filterCurrent2026_2027Committees } from '../services/firestoreDb';
import { OptionsEditor } from './ui/OptionsEditor';
import { ComposerAssist } from './quickadd/ComposerAssist';
import { composerClient } from '../services/composerClient';
import { IntakeEcho } from './quickadd/IntakeEcho';
import { BlurOverlay } from './ui/Animations';
import { toast } from './ui/Toast';
import { ApiService, SimilarPastQuestion, SourceRefLite } from '../services/api';
import { validateNamePolicy } from '../utils/namePolicy';
import { RealtimeMatchItem, warmMedicalIndex } from '../services/draftClusteringService';
import { toContextHashtag } from '../utils/fuzzyMatching';
import { getSmartQuestionAssistant, SmartQuestionAssistantResult } from '../services/medicalPredictorService';
import { Colored, WordLegend, ContextBadge, sharedWordColors } from './draftHighlight';
import { MetaPicker } from './ui/MetaPicker';
import './quickadd/quickadd.css';
import '../styles/v12/quickadd.css';
import { useAppearance } from '../utils/appearance';
import { sinavPenceresi } from '../services/kurulPencere';
import { getScoreTier, HIGHLIGHT_MIN_SCORE, currentAcademicYear, academicYears, committeeShortLabel, questionStemText, StatusPill, COMMITTEE_EXAM_DATES, isCommitteeLocked } from './quickAddOrtak';
import '../styles/ayrik-qa.css';
export { getScoreTier, HIGHLIGHT_MIN_SCORE, currentAcademicYear, academicYears, committeeShortLabel, questionStemText, StatusPill, COMMITTEE_EXAM_DATES, isCommitteeLocked } from './quickAddOrtak';

const AiQuestionOptimizerModal = React.lazy(() =>
  import('./AiQuestionOptimizerModal').then((m) => ({ default: m.AiQuestionOptimizerModal }))
);


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
  }) => Promise<void | { intakeId?: string | null }>;
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
const ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI'];
const EXAM_YEAR_KEY = 'medsoru_contrib_exam_year';

// The correct answer is picked inside the option list (tap a letter), so there is no separate "Cevap" mode
type Mode = 'stem' | 'option' | 'clue';

const PLACEHOLDERS: Record<Mode, string> = {
  stem: "Sorudan hatırladığın kısmı yaz… örn. göçük altında kalan hasta, EKG'de sivri T",
  option: '',
  clue: 'Örn. idrarda delta-ALA yüksekti, kemik iliğinde halkalı sideroblast…',
};


const titleCase = (c: Committee) => {
  return committeeShortLabel(c);
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
  isAdmin = false,
}) => {
  const disciplines =
    committee?.disciplines && committee.disciplines.length > 0
      ? committee.disciplines
      : ['Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'Tıbbi Biyokimya', 'Halk Sağlığı', 'İç Hastalıkları'];

  // v12 "Net": sade sayfa + her genişlikte tam ekran sihirbaz (eski ayrı yapı components/v12/QuickAddV12 artık kullanılmıyor)
  const v12 = useAppearance().design === 'v12';
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
  const [intakeId, setIntakeId] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [similar, setSimilar] = useState<SimilarPastQuestion[]>([]);
  const [simOpen, setSimOpen] = useState(false);
  const [sources, setSources] = useState<SourceRefLite[]>([]);
  const [realtimeMatches, setRealtimeMatches] = useState<RealtimeMatchItem[]>([]);
  // Öğrenci kararları (öğrenme verisi): son eşleşme sorgusunun metni ve bu yazımda reddedilen öneriler
  const lastMatchTextRef = React.useRef('');
  const [dismissedMatchIds, setDismissedMatchIds] = useState<Set<string>>(new Set());
  // Yeni soruya geçilince (kutu boşalınca) reddedilenler sıfırlanır
  useEffect(() => { if (!text.trim()) setDismissedMatchIds(new Set()); }, [text]);
  const dismissedRef = React.useRef(dismissedMatchIds);
  dismissedRef.current = dismissedMatchIds;
  const rejectMatch = (id: string) => {
    sendDecision(id, 'farkli');
    setDismissedMatchIds((prev) => new Set(prev).add(id));
    setRealtimeMatches((prev) => prev.filter((x) => x.question.id !== id));
    setSelectedMatchIds((prev) => { const n = new Set(prev); n.delete(id); return n; });
  };
  const sendDecision = (questionId: string, decision: 'ayni' | 'farkli') => {
    const text = lastMatchTextRef.current;
    const m = realtimeMatches.find((x) => x.question.id === questionId);
    if (!text || !committee?.id) return;
    ApiService.recallFeedback({ text, committeeId: committee.id, questionId, decision, prob: m ? m.compatibility.score / 100 : undefined });
  };
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
    return committee ? isCommitteeLocked(committee.id, examYear) : false;
  }, [committee, examYear]);

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
    const ctrl = new AbortController();
    setIsSearching(true);

    const optionsList = KEYS.filter((k) => options[k].trim()).map((k) => ({ key: k, text: options[k].trim() }));

    const timer = window.setTimeout(async () => {
      if (isCancelled) return;
      try {
        // Kurul uyuşmazlığı uyarısı yerel ve hafif; ders/konu tahmini ve havuz eşleşmesi sunucudaki motordan
        // (src/services/recall/; ölçüm scripts/eval/recall-realtime.mts: ilk öneri doğru %83, ders %63 —
        // eski tarayıcı algoritması %54,5 / %36 ve yazarken 39 ms ana iş parçacığı yükü).
        const local = getSmartQuestionAssistant(q, optionsList, committee.id);
        lastMatchTextRef.current = q;
        const r = await ApiService.recallMatch({
          text: q,
          committeeId: committee.id,
          discipline: userManualDiscipline ? disciplineRef.current : undefined,
          options: optionsList,
          questionNumber: userManualNumber && Number(questionNumber) > 0 ? Number(questionNumber) : undefined,
          limit: 4,
        }, ctrl.signal);
        if (isCancelled) return;
        const top = r?.ders?.[0];
        const assistantRes: SmartQuestionAssistantResult = {
          ...local,
          predictedDiscipline: top && top.p >= 0.5 && disciplines.includes(top.name)
            ? { discipline: top.name, confidence: Math.round(top.p * 100), sampleKeywords: r!.terms }
            : undefined,
          suggestedTopics: r ? [r.konu?.name, ...r.terms].filter((t): t is string => !!t).slice(0, 3).map((topic) => ({ topic, confidence: 1 })) : [],
        };
        setSmartAssistant(assistantRes);

        // Kullanıcı elle ders seçmediyse ve motor güvenliyse (p ≥ 0.75, ölçümde %89 isabet) dersi uygula
        // (eşleşen taslaktan gelen ders önceliklidir; tahmin onu ezmez)
        if (!userManualDiscipline && !matchedDiscRef.current && top && top.p >= 0.75 && disciplines.includes(top.name) && top.name !== disciplineRef.current) {
          setDiscipline(top.name);
          setAutoDisc(true);
        }

        const byId = new Map(questions.map((x) => [String(x.id), x]));
        const matches: RealtimeMatchItem[] = (r?.matches || [])
          .map((m) => {
            const question = byId.get(String(m.questionId)) || m.question;
            if (!question) return null;
            return {
              question,
              compatibility: {
                score: Math.round(m.prob * 100),
                recommendation: m.prob >= 0.85 ? 'suggest_merge' : 'distinct',
                reasons: [],
                stemSimilarity: m.prob,
                optionSetSimilarity: 0,
                sharedMedicalEntities: r!.terms,
                sharedConcepts: [],
                contextHashtag: r!.konu?.name ? toContextHashtag(r!.konu.name) : undefined,
                targetQuestionAlignment: 'matching',
                matchedOptionAlignments: [],
              },
              contextHashtag: r!.konu?.name ? toContextHashtag(r!.konu.name) : undefined,
            } as RealtimeMatchItem;
          })
          .filter((m): m is RealtimeMatchItem => !!m && !dismissedRef.current.has(m.question.id));
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
        if (!isCancelled) setIsSearching(false);
      }
    }, 20);

    return () => {
      isCancelled = true;
      ctrl.abort();
      window.clearTimeout(timer);
    };
  }, [debouncedText, mode, committee?.id, optionsText, questions]);

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
    sendDecision(targetQ.id, 'ayni');
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
    for (const m of selectedList) sendDecision(m.question.id, 'ayni');

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
      setPremises(['', '', '']);
      setQType(null);
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

  // Tüm adayların ve kullanıcının metinlerindeki ortak kelime paleti (debouncedText ile optimize edildi).
  // Renkler kullanıcının metnine çapalanır (çapa 0): iki taslağın kendi arasındaki
  // ortak kelimesi boyanmaz; yalnızca kullanıcıyla örtüşen kelimeler aynı rengi alır.
  // Boya yalnızca %80+ kartlardan kurulur; altındaki kartlar boyasız kalır.
  const sharedColors = useMemo(() => {
    if (realtimeMatches.length === 0 || !debouncedText) return new Map<string, string>();
    const trusted = realtimeMatches.filter((m) => m.compatibility.score >= HIGHLIGHT_MIN_SCORE);
    if (trusted.length === 0) return new Map<string, string>();
    const allStems = [debouncedText, ...trusted.map((m) => questionStemText(m.question))];
    return sharedWordColors(allStems, 0);
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
    // Telefon sihirbazı: Yalnızca 'son' adımında ve kullanıcının açıkça 'Havuza ekle' düğmesine basmasıyla gönderim yapılır.
    // Başka bir adımda (kök, tür, öncüller, şıklar) veya klavyenin Enter/Git tuşuyla yanlışlıkla form gönderimi kesinlikle engellenir.
    if (fullRef.current === 'open') {
      if (wizRef.current !== 'son') {
        return;
      }
      const submitter = (e.nativeEvent as SubmitEvent | undefined)?.submitter as HTMLElement | null;
      if (submitter && !submitter.classList.contains('wz-submit')) {
        return;
      }
    }
    setFormError(null);

    const targetCommittee = committee || (committees && committees.length > 0 ? committees[0] : undefined);
    if (!targetCommittee) {
      setFormError('Lütfen önce bir kurul seçiniz.');
      return;
    }

    if (isCommitteeLocked(targetCommittee.id, examYear)) {
      const msg = 'Ders programına göre bu kurulun sınav tarihi henüz gelmedi. Önceki kurul sınavı tamamlanmadan sonraki kurula soru yazılamaz.';
      setFormError(msg);
      toast.error('Kurul Henüz Açılmadı', msg);
      return;
    }

    const optionsList = KEYS.filter((k) => options[k].trim()).map((k) => ({ key: k, text: options[k].trim() }));
    if (!hasAnyText && optionsList.length === 0 && !claimedAnswer && !(qType === 'onculu' && premises.some((p) => p.trim()))) {
      setFormError('Sorudan aklında kalan en az bir kelime, şık ya da cevap yaz.');
      return;
    }

    const num = parseInt(questionNumber, 10);
    const hasNumber = Number.isFinite(num) && num >= 1 && num <= target;
    // Everything written in the different modes goes in as one fragment
    const premiseLines = qType === 'onculu' ? premises.map((p) => p.trim()).filter(Boolean).map((p, i) => `${ROMAN[i]}. ${p}`) : [];
    const fragmentText = [
      texts.stem.trim(),
      ...premiseLines,
      texts.clue.trim() ? `İpucu: ${texts.clue.trim()}` : '',
      claimedAnswer && answerReason.trim() ? `Cevap notu (${claimedAnswer}): ${answerReason.trim()}` : '',
    ]
      .filter(Boolean)
      .join('\n');
    const savedName = localStorage.getItem(SAVED_NAME_KEY) || '';
    const authorCandidate = currentUser?.displayName || savedName;
    if (authorCandidate) {
      const nameCheck = validateNamePolicy(authorCandidate, { adminEmail: currentUser?.email });
      if (!nameCheck.isValid) {
        setFormError(nameCheck.errorMessage || 'Geçersiz yazar / katkıcı adı.');
        toast.error('İsim Kuralı Hatası', nameCheck.errorMessage || 'Geçersiz isim.');
        return;
      }
    }

    setIsSubmitting(true);
    setIntakeId(null);
    try {
      const submitted = await onSubmitContribution({
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
      if (submitted && submitted.intakeId) setIntakeId(submitted.intakeId);
      setTexts({ stem: '', clue: '' });
      setOptions({ A: '', B: '', C: '', D: '', E: '' });
      setOptionCount(1);
      setAnswerReason('');
      setClaimedAnswer(undefined);
      setQuestionNumber('');
      setUserManualDiscipline(false);
      setUserManualNumber(false);
      setLinkedQuestion(null);
      setQType(null);
      setPremises(['', '', '']);
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

  // "Bunu mu kastettiniz?": anlık yerel tıp sözlüğü + derlem yazım önerisi (2+ kelime)
  const [spell, setSpell] = useState<{ text: string | null; changes: { from: string; to: string }[] } | null>(null);
  const [dismissedSpell, setDismissedSpell] = useState<string | null>(null);
  useEffect(() => {
    const q = debouncedText || text;
    // Kökte öneri ComposerAssist kutusunda gösterilir
    if (mode === 'option' || mode === 'stem' || !q.trim() || q.trim().split(/\s+/).length < 2) { setSpell(null); return; }

    // 1. Önce yerel derlem sözlüğü (yazım işçisinde; ana iş parçacığını kilitlemez)
    // 2. Yerelde bulunamazsa arka planda sunucudan yokla
    const ctrl = new AbortController();
    let t = 0;
    composerClient.spell(q).then((localSpell) => {
      if (ctrl.signal.aborted) return;
      if (localSpell && localSpell.changes.length > 0) { setSpell(localSpell.text !== text ? localSpell : null); return; }
      t = window.setTimeout(() => {
        ApiService.suggestSpelling(q, ctrl.signal).then((r) => {
          if (ctrl.signal.aborted || !r?.text) { if (!ctrl.signal.aborted) setSpell(null); return; }
          setSpell(r.text !== text ? r : null);
        });
      }, 400);
    });
    return () => { ctrl.abort(); window.clearTimeout(t); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debouncedText, text, mode]);

  // Telefonda tam ekran yazma adım adım ilerler: kök → soru tipi → (öncüller) → şıklar → ipucu ve künye
  type WizStep = 'kok' | 'tur' | 'onculler' | 'siklar' | 'son';
  const [qType, setQType] = useState<'klasik' | 'onculu' | null>(null);
  const [premises, setPremises] = useState<string[]>(['', '', '']);
  const [wiz, setWizRaw] = useState<WizStep>('kok');
  const [wizDir, setWizDir] = useState<1 | -1>(1);
  const wizRef = React.useRef<WizStep>('kok');
  wizRef.current = wiz;
  const wizSteps: WizStep[] = qType === 'onculu' ? ['kok', 'tur', 'onculler', 'siklar', 'son'] : ['kok', 'tur', 'siklar', 'son'];
  const goWiz = (to: WizStep) => {
    const order: WizStep[] = ['kok', 'tur', 'onculler', 'siklar', 'son'];
    setWizDir(order.indexOf(to) >= order.indexOf(wizRef.current) ? 1 : -1);
    setWizRaw(to);
  };
  const wizNext = () => {
    const i = wizSteps.indexOf(wiz);
    if (i >= 0 && i < wizSteps.length - 1) goWiz(wizSteps[i + 1]);
  };
  const wizBack = () => {
    const i = wizSteps.indexOf(wizRef.current);
    if (i > 0) goWiz(wizSteps[i - 1]);
  };
  const pickType = (t: 'klasik' | 'onculu') => {
    setQType(t);
    setWizDir(1);
    setWizRaw(t === 'onculu' ? 'onculler' : 'siklar');
  };
  // Öncüllü sorularda sık şık kalıpları: dokununca ilk boş şıkka yazılır
  const premiseCount = Math.max(2, premises.filter((p) => p.trim()).length);
  const comboChips = (() => {
    const R = ROMAN.slice(0, Math.min(premiseCount, 5));
    const out: string[] = R.map((r) => `Yalnız ${r}`);
    for (let a = 0; a < R.length; a++) for (let b = a + 1; b < R.length; b++) out.push(`${R[a]} ve ${R[b]}`);
    if (R.length >= 3) out.push(`${R.slice(0, -1).join(', ')} ve ${R[R.length - 1]}`);
    return out.slice(0, 12);
  })();
  const fillNextOption = (text: string) => {
    const k = KEYS.find((key, i) => i < optionCount && !options[key].trim()) || (optionCount < 5 ? KEYS[optionCount] : null);
    if (!k) return;
    if (KEYS.indexOf(k) >= optionCount) setOptionCount(KEYS.indexOf(k) + 1);
    setOptions((p) => ({ ...p, [k]: text }));
  };

  // Masaüstü öncül düzenleyici yardımcıları
  const PREMISE_MAX = 6;
  const premiseLineRe = /^\s*(VI|IV|V|I{1,3})\s*[.)\-:]\s+(.+)$/;
  const splitPremiseLines = (raw: string) =>
    raw.split(/\r?\n/).map((l) => l.trim()).filter(Boolean).map((l) => l.replace(premiseLineRe, '$2').replace(/^[-•*]\s+/, ''));
  // Kökte "I. … II. …" satırları varsa öncüllere ayrılabilir
  const stemPremiseLines = texts.stem.split(/\r?\n/).filter((l) => premiseLineRe.test(l));
  const looksOnculu = qType === null && (stemPremiseLines.length >= 2 || /hangiler/i.test(texts.stem));
  const extractPremisesFromStem = () => {
    const lines = texts.stem.split(/\r?\n/);
    const prem = lines.filter((l) => premiseLineRe.test(l)).map((l) => l.replace(premiseLineRe, '$2').trim());
    const rest = lines.filter((l) => !premiseLineRe.test(l)).join('\n').replace(/\n{2,}/g, '\n').trim();
    setTexts((p) => ({ ...p, stem: rest }));
    setPremises(prem.slice(0, PREMISE_MAX));
    setQType('onculu');
  };
  const setPremiseAt = (i: number, v: string) => setPremises((p) => p.map((x, j) => (j === i ? v : x)));
  const focusPremise = (i: number) => window.setTimeout(() => document.getElementById(`qh-prem-${i}`)?.focus(), 0);
  const addPremise = (after?: number) => {
    if (premises.length >= PREMISE_MAX) return;
    const at = after === undefined ? premises.length : after + 1;
    setPremises((p) => [...p.slice(0, at), '', ...p.slice(at)]);
    focusPremise(at);
  };
  const removePremise = (i: number) => {
    if (premises.length <= 2) { setPremiseAt(i, ''); return; }
    setPremises((p) => p.filter((_, j) => j !== i));
    focusPremise(Math.max(0, i - 1));
  };
  const pastePremises = (i: number, e: React.ClipboardEvent<HTMLInputElement>) => {
    const raw = e.clipboardData.getData('text');
    if (!/\n/.test(raw.trim())) return;
    e.preventDefault();
    const parts = splitPremiseLines(raw);
    setPremises((p) => [...p.slice(0, i), ...parts, ...p.slice(i + 1).filter((x) => x.trim())].slice(0, PREMISE_MAX));
  };
  const filledPremiseCount = premises.filter((p) => p.trim()).length;
  // Öncül sayısına göre sınavlarda en sık görülen beş şık
  const standardCombos = (n: number): string[] => {
    if (n <= 2) return ['Yalnız I', 'Yalnız II', 'I ve II', 'Hiçbiri', 'Belirlenemez'].slice(0, 3);
    if (n === 3) return ['Yalnız I', 'Yalnız II', 'I ve II', 'II ve III', 'I, II ve III'];
    if (n === 4) return ['I ve II', 'I ve III', 'II ve IV', 'I, II ve III', 'I, II, III ve IV'];
    return ['I ve II', 'II ve IV', 'I, III ve V', 'II, III ve IV', 'I, II, III, IV ve V'];
  };
  const fillStandardOptions = () => {
    const set = standardCombos(Math.max(2, filledPremiseCount));
    setOptions(KEYS.reduce((acc, k, i) => ({ ...acc, [k]: set[i] || '' }), {} as Record<OptionKey, string>));
    setOptionCount(set.length);
    setClaimedAnswer(undefined);
  };
  const romansIn = (t: string) => new Set((t.match(/\b(VI|IV|V|I{1,3})\b/g) || []) as string[]);
  // Doğru şık işaretliyse hangi öncüllerin doğru sayıldığı
  const truePremises = qType === 'onculu' && claimedAnswer && options[claimedAnswer].trim() ? romansIn(options[claimedAnswer]) : null;

  // Telefonda yazma alanı tam ekran açılır (animasyonla), kapatınca yerine animasyonla döner; geri tuşu da kapatır
  const [full, setFull] = useState<false | 'open' | 'closing'>(false);
  // Sınav günü + sonraki 7 gün: "Kaçıncı soruydu?" alanı kökün üstünde öne çıkar (olası soru yuvası numarayla kurulur)
  const sinavPen = useMemo(() => sinavPenceresi(), []);
  const numaraOne = sinavPen ? (
    <label className={`qa-numara ${full ? 'is-full' : ''}`}>
      <span className="qa-numara-l">Kaçıncı soruydu?<small>Kurul {sinavPen.kurul.kurul} sınavı · 1–100, bilmiyorsan boş bırak</small></span>
      <input
        type="text"
        inputMode="numeric"
        enterKeyHint="done"
        value={questionNumber}
        onChange={(e) => {
          const v = e.target.value.replace(/[^0-9]/g, '').slice(0, 3);
          if (v && (Number(v) < 1 || Number(v) > 100)) return;
          setQuestionNumber(v); setUserManualNumber(true); setAutoNum(false);
        }}
        onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); (e.target as HTMLInputElement).blur(); } }}
        placeholder="—"
        aria-label="Sınavda kaçıncı soruydu (1–100)"
      />
    </label>
  ) : null;
  const fullRef = React.useRef(full);
  fullRef.current = full;
  const isClosingRef = React.useRef(false);

  const openFull = () => {
    if (fullRef.current || (!v12 && !window.matchMedia('(max-width: 767px)').matches)) return;
    isClosingRef.current = false;
    setFull('open');
    setWizRaw('kok');
    try { window.history.pushState({ ...(window.history.state || {}), msComposer: 1 }, ''); } catch { /* yok */ }
  };
  const finishClose = () => {
    isClosingRef.current = false;
    setFull('closing');
    window.setTimeout(() => setFull(false), 240);
    (document.activeElement as HTMLElement | null)?.blur?.();
  };
  const closeFull = () => {
    if (fullRef.current !== 'open' || isClosingRef.current) return;
    isClosingRef.current = true;
    if (window.history.state?.msComposer) window.history.back();
    else finishClose();
  };
  useEffect(() => {
    // Geri tuşu: önce bir önceki adıma döner, ilk adımda tam ekranı kapatır
    const onPop = () => {
      if (fullRef.current !== 'open') return;
      if (isClosingRef.current) {
        finishClose();
        return;
      }
      // Açık künye/alt sayfa (Kurul, Ders vb.) varsa önce onu kapat
      const openSheetCloseBtn = document.querySelector('.qa-pop.is-sheet .qa-pop-head button, .qa-pop-scrim') as HTMLElement | null;
      if (openSheetCloseBtn) {
        openSheetCloseBtn.click();
        try { window.history.pushState({ ...(window.history.state || {}), msComposer: 1 }, ''); } catch { /* yok */ }
        return;
      }
      if (wizRef.current !== 'kok') {
        wizBack();
        try { window.history.pushState({ ...(window.history.state || {}), msComposer: 1 }, ''); } catch { /* yok */ }
        return;
      }
      finishClose();
    };
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

  // v10 kompakt (2026-10-13, "SoruEkle-Masaustu"): ≥768 px'te iki bölmeli form (solda künye + kök + A–E şıklar,
  // sağda "Benzer sorular · tekrar riski" ve öneri kutusu). Telefonda yukarıdaki tam ekran sihirbaz aynen kalır.
  const [isWide, setIsWide] = useState(() => typeof window !== 'undefined' && window.matchMedia('(min-width: 768px)').matches);
  useEffect(() => {
    const mq = window.matchMedia('(min-width: 768px)');
    const on = () => setIsWide(mq.matches);
    mq.addEventListener('change', on);
    return () => mq.removeEventListener('change', on);
  }, []);
  useEffect(() => {
    if (!isWide || v12) return;
    // Geniş ekranda kök ve şıklar aynı anda görünür: tek kip (kök); telefondan büyütülürse tam ekran kapanır (v12'de sihirbaz her genişlikte)
    if (mode !== 'stem') setMode('stem');
    if (fullRef.current) setFull(false);
  }, [isWide, mode, v12]);

  // Taslak kaydet: form bu cihazda saklanır, gönderim başarılı olunca silinir
  type QhDraft = {
    at: string; stem: string; clue: string; options: Record<OptionKey, string>; answer?: OptionKey; reason: string;
    discipline: string; questionNumber: string; examYear: string;
    qType?: 'klasik' | 'onculu' | null; premises?: string[];
  };
  const QH_DRAFT_KEY = 'medsoru_quickadd_draft_v1';
  const [savedDraft, setSavedDraft] = useState<QhDraft | null>(() => {
    try { const raw = localStorage.getItem(QH_DRAFT_KEY); return raw ? (JSON.parse(raw) as QhDraft) : null; } catch { return null; }
  });
  const [clueOpen, setClueOpen] = useState(false);
  const saveDraft = () => {
    const d: QhDraft = {
      at: new Date().toISOString(), stem: texts.stem, clue: texts.clue, options, answer: claimedAnswer, reason: answerReason,
      discipline, questionNumber, examYear, qType, premises,
    };
    try { localStorage.setItem(QH_DRAFT_KEY, JSON.stringify(d)); } catch { /* yok */ }
    setSavedDraft(d);
    toast.success('Taslak kaydedildi', 'Bu cihazda saklanır; havuza gönderince silinir.');
  };
  const dropDraft = () => {
    try { localStorage.removeItem(QH_DRAFT_KEY); } catch { /* yok */ }
    setSavedDraft(null);
  };
  const restoreDraft = () => {
    if (!savedDraft) return;
    setTexts({ stem: savedDraft.stem || '', clue: savedDraft.clue || '' });
    setOptions(KEYS.reduce((acc, k) => ({ ...acc, [k]: (savedDraft.options || {})[k] || '' }), {} as Record<OptionKey, string>));
    setOptionCount(Math.max(1, KEYS.reduce((n, k, i) => ((savedDraft.options || {})[k]?.trim() ? i + 1 : n), 1)));
    setClaimedAnswer(savedDraft.answer);
    setAnswerReason(savedDraft.reason || '');
    if (savedDraft.discipline && disciplines.includes(savedDraft.discipline)) { setDiscipline(savedDraft.discipline); setUserManualDiscipline(true); }
    if (savedDraft.questionNumber) { setQuestionNumber(savedDraft.questionNumber); setUserManualNumber(true); }
    if (savedDraft.examYear !== undefined) setExamYear(savedDraft.examYear);
    if (savedDraft.clue) setClueOpen(true);
    if (savedDraft.qType !== undefined) setQType(savedDraft.qType);
    if (savedDraft.premises?.length) setPremises(savedDraft.premises);
  };
  useEffect(() => {
    if (successMessage) dropDraft();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [successMessage]);
  const formEmpty = !hasAnyText && filledOptionCount === 0 && !claimedAnswer && !premises.some((p) => p.trim());

  // v12 (2026-10-14, kullanıcı isteği): v10 kadar sade sayfa + her genişlikte tam ekran adım adım sihirbaz (aşağıdaki telefon yolu).

  if (isWide && !v12) {
    const riskCls = (s: number) => (s >= 80 ? 'is-bad' : s >= 65 ? 'is-warn' : 'is-mid');
    const yearLabel = (y: string) => `${y.slice(0, 4)}–${y.slice(7, 9)}`;
    const hasSuggest = !!smartAssistant && (!!smartAssistant.crossCommitteeWarning || smartAssistant.suggestedTopics.length > 0);
    const noResults = realtimeMatches.length === 0 && similar.length === 0;
    return (
      <div className="qh">
        <form
          onSubmit={handleSubmit}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && (e.target as HTMLElement).tagName === 'INPUT') {
              e.preventDefault();
            }
          }}
          aria-busy={isSubmitting}
          className="qh-grid"
        >
          <div className="qh-main">
            <BlurOverlay show={isSubmitting} label="Havuza ekleniyor…" hint="Benzer parçalar varsa aynı soruya bağlıyoruz" />
            <header className="qh-head">
              <h1>Soru ekle</h1>
              <p>Hatırladığın parçayı yaz; gerisini birlikte tamamlarız.</p>
              <span className={`qh-live ${isCollecting ? 'is-on' : ''}`}>
                <i aria-hidden />{committee ? titleCase(committee) : 'Kurul'}{isCollecting ? ' · toplama açık' : ''}
              </span>
            </header>
            {isLocked && (
              <div className="qh-note is-warn" role="status">
                <Lock aria-hidden />
                <span>Ders programına göre sınav tamamlanmadan bu kurula soru yazılamaz.</span>
              </div>
            )}
            {savedDraft && formEmpty && (
              <div className="qh-note is-draft" role="status">
                <FileText aria-hidden />
                <span>Kaydedilmiş taslağın var · {new Date(savedDraft.at).toLocaleString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })}</span>
                <button type="button" onClick={restoreDraft}>Geri yükle</button>
                <button type="button" className="is-quiet" onClick={dropDraft}>Sil</button>
              </div>
            )}

            <div className="qh-meta">
              <label className="qh-field">
                <span>Kurul</span>
                <select value={committee?.id || ''} onChange={(e) => onSelectCommittee(e.target.value)}>
                  {!committee && <option value="">Seç</option>}
                  {sortedCommittees.map((c) => {
                    const locked = isCommitteeLocked(c.id, examYear);
                    return (
                      <option key={c.id} value={c.id} disabled={locked}>
                        {titleCase(c)}{locked ? ' · açılmadı' : c.id === activeCommitteeId ? ' · toplama açık' : ''}
                      </option>
                    );
                  })}
                </select>
              </label>
              <label className="qh-field">
                <span>Ders{autoDisc && !userManualDiscipline && <em className="qh-auto"><Sparkles aria-hidden /> otomatik</em>}</span>
                <select
                  value={discipline}
                  onChange={(e) => { setDiscipline(e.target.value); setUserManualDiscipline(true); setAutoDisc(false); }}
                >
                  {disciplines.map((d) => <option key={d} value={d}>{d}</option>)}
                </select>
              </label>
              <label className="qh-field">
                <span>Sınav yılı</span>
                <select value={examYear} onChange={(e) => setExamYear(e.target.value)}>
                  <option value="">Bilmiyorum</option>
                  {academicYears().map((y) => (
                    <option key={y} value={y}>{yearLabel(y)}{y === currentAcademicYear() ? ' · bu yıl' : ''}</option>
                  ))}
                </select>
              </label>
              <label className="qh-field is-num">
                <span>Soru no{autoNum && !userManualNumber && <em className="qh-auto"><Sparkles aria-hidden /> otomatik</em>}</span>
                <input
                  type="text"
                  inputMode="numeric"
                  value={questionNumber}
                  onChange={(e) => { setQuestionNumber(e.target.value.replace(/[^0-9]/g, '').slice(0, 3)); setUserManualNumber(true); setAutoNum(false); }}
                  placeholder="—"
                  aria-label="Soru numarası (bilmiyorsan boş bırak)"
                />
              </label>
            </div>

            <div className="qh-block">
              <label htmlFor="hatira" className="qh-label">Soru kökü</label>
              <div className="ms-composer qh-stem">
                <FastTextarea
                  id="hatira"
                  rows={3}
                  value={text}
                  onValue={setText}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                      e.preventDefault();
                      e.currentTarget.form?.requestSubmit();
                    }
                  }}
                  placeholder={PLACEHOLDERS.stem}
                  className="ms-bare-input w-full block resize-none px-3 pt-2.5 pb-2 text-md leading-[1.55] text-ink placeholder:text-ink-3 bg-transparent border-0 outline-0 min-h-[96px]"
                />
                {/* Akıllı soru tamamlama ve yazım yardımcısı (Web Worker, composerClient) */}
                <ComposerAssist active={mode === 'stem'} value={text} onChange={setText} textareaId="hatira" committeeId={committee?.id} />
              </div>
              {linkedQuestion && (
                <div className="qh-note is-ok" role="status">
                  <Link2 aria-hidden />
                  <span>{linkedQuestion.questionNumber ? `Soru #${linkedQuestion.questionNumber} ile bağlandı` : 'Mevcut taslakla bağlandı'} · yazdıkların bu sorunun katkılarına eklenecek</span>
                  <button type="button" className="is-quiet" onClick={() => { setLinkedQuestion(null); setQuestionNumber(''); }} aria-label="Bağlantıyı kaldır"><X aria-hidden /></button>
                </div>
              )}
            </div>

            <div className="qh-block">
              <div className="qh-type" role="radiogroup" aria-label="Soru tipi">
                <span className="qh-label">Soru tipi</span>
                <div className="qh-seg">
                  <button type="button" role="radio" aria-checked={qType !== 'onculu'} className={qType !== 'onculu' ? 'is-on' : ''} onClick={() => setQType('klasik')}>Klasik</button>
                  <button type="button" role="radio" aria-checked={qType === 'onculu'} className={qType === 'onculu' ? 'is-on' : ''} onClick={() => { setQType('onculu'); if (!premises.some((x) => x.trim())) focusPremise(0); }}>Öncüllü <small>I · II · III</small></button>
                </div>
                {looksOnculu && (
                  <button type="button" className="qh-hint" onClick={() => (stemPremiseLines.length >= 2 ? extractPremisesFromStem() : (setQType('onculu'), focusPremise(0)))}>
                    <Sparkles aria-hidden />
                    {stemPremiseLines.length >= 2 ? `Kökteki ${stemPremiseLines.length} öncülü ayır` : 'Öncüllü soruya benziyor · öncülleri ekle'}
                  </button>
                )}
              </div>
              {qType === 'onculu' && (
                <div className="qh-prem" aria-label="Öncüller">
                  {premises.map((pr, i) => {
                    const r = ROMAN[i];
                    const verdict = truePremises ? (truePremises.has(r) ? 'is-true' : 'is-false') : '';
                    return (
                      <div key={i} className={`qh-prem-row ${verdict}`}>
                        <span className="r" aria-hidden>{r}</span>
                        <input
                          id={`qh-prem-${i}`}
                          value={pr}
                          onChange={(e) => setPremiseAt(i, e.target.value)}
                          onPaste={(e) => pastePremises(i, e)}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                              e.preventDefault();
                              if (i + 1 < premises.length) focusPremise(i + 1);
                              else if (pr.trim() && premises.length < PREMISE_MAX) addPremise(i);
                              else document.querySelector<HTMLInputElement>('.qh-opts input.t')?.focus();
                            } else if (e.key === 'Backspace' && !pr && premises.length > 2) {
                              e.preventDefault();
                              removePremise(i);
                            } else if (e.key === 'ArrowDown') { e.preventDefault(); focusPremise(i + 1); }
                            else if (e.key === 'ArrowUp') { e.preventDefault(); focusPremise(i - 1); }
                          }}
                          placeholder={i === 0 ? 'Öncül yaz · Enter ile sonrakine, çok satır yapıştırınca bölünür' : `${r}. öncül`}
                          aria-label={`${r}. öncül`}
                        />
                        {verdict && <em className="v">{verdict === 'is-true' ? 'doğru' : 'yanlış'}</em>}
                        <button type="button" className="x" onClick={() => removePremise(i)} aria-label={`${r}. öncülü sil`} tabIndex={-1}><X aria-hidden /></button>
                      </div>
                    );
                  })}
                  {premises.length < PREMISE_MAX && (
                    <button type="button" className="qh-prem-add" onClick={() => addPremise()}><Plus aria-hidden />{ROMAN[premises.length]}. öncülü ekle</button>
                  )}
                </div>
              )}
            </div>

            <fieldset className="qh-opts">
              <legend>Şıklar · doğruyu işaretle</legend>
              {qType === 'onculu' && (
                <div className="qh-combos">
                  <button type="button" className="qh-combo is-fill" onClick={fillStandardOptions} disabled={filledPremiseCount < 2} title="A–E'yi öncül sayısına uygun sık kalıplarla doldur">
                    <Wand2 aria-hidden />Kalıp şıkları doldur
                  </button>
                  {comboChips.map((c) => (
                    <button key={c} type="button" className="qh-combo" onMouseDown={(e) => e.preventDefault()} onClick={() => {
                      const el = document.activeElement as HTMLInputElement | null;
                      const fk = el?.classList.contains('t') ? (el.getAttribute('data-k') as OptionKey | null) : null;
                      if (fk) setOptions((p) => ({ ...p, [fk]: c })); else fillNextOption(c);
                    }}>{c}</button>
                  ))}
                </div>
              )}
              {KEYS.map((k, i) => (
                <div key={k} className={`qh-opt ${claimedAnswer === k ? 'is-ok' : ''}`}>
                  <input
                    type="radio"
                    name="qh-dogru"
                    checked={claimedAnswer === k}
                    onChange={() => setClaimedAnswer(k)}
                    aria-label={`${k} doğru cevap`}
                  />
                  <span className="k" aria-hidden>{k}</span>
                  <input
                    className="t bg-transparent"
                    value={options[k]}
                    onChange={(e) => {
                      const v = e.target.value;
                      setOptions((p) => ({ ...p, [k]: v }));
                      if (v.trim() && i + 1 > optionCount) setOptionCount(i + 1);
                    }}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault();
                        const all = e.currentTarget.closest('fieldset')?.querySelectorAll<HTMLInputElement>('input.t');
                        all?.[i + 1]?.focus();
                      }
                    }}
                    enterKeyHint={i < 4 ? 'next' : 'done'}
                    data-k={k}
                    placeholder={qType === 'onculu' ? 'örn. I ve III' : 'Şık yaz'}
                    aria-label={`${k} şıkkı`}
                  />
                </div>
              ))}
              {claimedAnswer && (
                <div className="qh-why">
                  <input
                    value={answerReason}
                    onChange={(e) => setAnswerReason(e.target.value)}
                    placeholder={`Neden ${claimedAnswer}? (isteğe bağlı)`}
                    aria-label="Cevap gerekçesi (isteğe bağlı)"
                  />
                  <button type="button" onClick={() => { setClaimedAnswer(undefined); setAnswerReason(''); }}>Cevabı bilmiyorum</button>
                </div>
              )}
            </fieldset>

            <div className="qh-block">
              <button
                type="button"
                className="qh-disc"
                aria-expanded={clueOpen || !!texts.clue.trim()}
                aria-controls="qh-clue"
                onClick={() => setClueOpen((v) => !v)}
              >
                <ChevronDown aria-hidden className={clueOpen || texts.clue.trim() ? 'is-open' : ''} />
                İpucu <small>isteğe bağlı · hocanın vurgusu, vaka ayrıntısı</small>
              </button>
              <div id="qh-clue" hidden={!(clueOpen || !!texts.clue.trim())}>
                <textarea
                  className="qh-clue"
                  rows={2}
                  value={texts.clue}
                  onChange={(e) => setTexts((prev) => ({ ...prev, clue: e.target.value }))}
                  placeholder={PLACEHOLDERS.clue}
                  aria-label="İpucu"
                />
              </div>
            </div>

            {formError && <div role="alert" className="ms-shake qh-note is-bad"><AlertCircle aria-hidden /><span>{formError}</span></div>}
            {successMessage && <div role="status" className="ms-pop-in qh-note is-ok"><CheckCircle2 aria-hidden /><span>Teşekkürler! {successMessage}</span></div>}
            {intakeId && <IntakeEcho key={intakeId} intakeId={intakeId} onClose={() => setIntakeId(null)} />}

            <div className="qh-actions">
              <button type="button" className="qh-btn" onClick={saveDraft} disabled={formEmpty}>Taslak kaydet</button>
              <button type="submit" className="qh-btn is-primary" disabled={isSubmitting || isLocked}>
                {isSubmitting ? 'Gönderiliyor…' : 'Havuza gönder'}
              </button>
              <span className="qh-kbd">Ctrl + Enter ile gönder</span>
            </div>
          </div>

          <aside className="qh-side" aria-label="Benzer sorular ve öneriler">
            <section className="qh-sec" aria-labelledby="qh-sim-h" aria-busy={isSearching}>
              <div className="qh-sec-h">
                <h2 id="qh-sim-h">Benzer sorular · tekrar riski</h2>
                {realtimeMatches.length > 1 && (
                  <button type="button" onClick={selectedMatchIds.size === realtimeMatches.length ? clearSelection : selectAllMatches}>
                    {selectedMatchIds.size === realtimeMatches.length ? 'Seçimi bırak' : 'Tümünü seç'}
                  </button>
                )}
              </div>

              {isSearching && noResults && text.trim().length >= 6 && (
                <div className="qh-skels" aria-hidden>
                  {[0, 1, 2].map((i) => <div key={i} className="qh-skel"><span className="ui-skel" /><span className="ui-skel" /><span className="ui-skel" /></div>)}
                </div>
              )}
              {!isSearching && noResults && (
                <p className="qh-empty">Yazdıkça havuzdaki benzer taslaklar ve çıkmış sorular burada belirir; aynı soruyu ikinci kez eklemeyi önler.</p>
              )}

              {realtimeMatches.map((m, idx) => {
                const q = m.question;
                const isSelected = selectedMatchIds.has(q.id);
                const score = m.compatibility.score;
                return (
                  <article key={q.id} className={`qh-sim ${isSelected ? 'is-sel' : ''}`}>
                    <div className="qh-sim-top">
                      <button
                        type="button"
                        className="qh-check"
                        onClick={() => toggleSelectMatch(q.id)}
                        aria-pressed={isSelected}
                        aria-label={`Soru ${q.questionNumber || 'taslak'} seç`}
                      >
                        {isSelected ? <CheckSquare aria-hidden /> : <Square aria-hidden />}
                      </button>
                      <span className={`qh-risk ${riskCls(score)}`}>%{score} benzer</span>
                      {idx === 0 && <span className="qh-tag">En yakın</span>}
                      {m.isCrossCommittee && <span className="qh-tag is-ai">Farklı kurul</span>}
                      {m.contextHashtag && score >= HIGHLIGHT_MIN_SCORE && <ContextBadge hashtag={m.contextHashtag} colorIndex={idx} />}
                      <span className="qh-num">{q.questionNumber ? `#${q.questionNumber}` : 'Numarasız'}</span>
                    </div>
                    <p className="qh-sim-t"><Colored text={questionStemText(q)} colors={sharedColors} /></p>
                    <div className="qh-sim-act">
                      <button type="button" onClick={() => handleLinkToQuestion(q)}>
                        <CheckCircle2 aria-hidden />{q.questionNumber ? `S.${q.questionNumber} ile bağla` : 'Bu taslakla bağla'}
                      </button>
                      {isAdmin && (
                        <button type="button" className="is-ai" onClick={() => setOptimizingQuestion(q)} title="Taslağı amfi slaytları ve AI ile tam soruya dönüştür">
                          <Wand2 aria-hidden />AI ile dönüştür
                        </button>
                      )}
                      <button type="button" onClick={() => rejectMatch(q.id)} title="Bu öneri benim hatırladığım soru değil (öneriler bundan öğrenir)">
                        <X aria-hidden />Farklı soru
                      </button>
                      {q.discipline && <span className="qh-sim-d">{q.discipline}</span>}
                    </div>
                  </article>
                );
              })}
              {realtimeMatches.length > 0 && (
                <WordLegend texts={[debouncedText || text, ...realtimeMatches.map((m) => questionStemText(m.question))]} colors={sharedColors} />
              )}

              {selectedMatchIds.size > 0 && (
                <div className="qh-merge">
                  <span className="n">{selectedMatchIds.size}</span>
                  <span className="t">{selectedMatchIds.size} soru seçildi</span>
                  <button type="button" onClick={clearSelection}>İptal</button>
                  <button type="button" className="is-primary" disabled={isMergingSelected} onClick={handleMergeAndGroupSelected}>
                    <Layers aria-hidden />
                    {isMergingSelected ? 'Birleştiriliyor…' : selectedMatchIds.size === 1 ? 'Bu soruyla birleştir' : `Birleştir (${selectedMatchIds.size})`}
                  </button>
                </div>
              )}

              {similar.length > 0 && (
                <>
                  <h3 className="qh-sub">Çıkmış sorularda</h3>
                  {similar.map((s) => (
                    <article key={s.id} className="qh-sim is-past">
                      <p className="qh-sim-t">{s.stem}</p>
                      {s.options && s.options.length > 0 && (
                        <ol className="qh-past-opts">
                          {s.options.map((o) => (
                            <li key={o.key} className={o.key === s.claimedAnswer ? 'is-ok' : ''}><b>{o.key})</b> {o.text}</li>
                          ))}
                        </ol>
                      )}
                      <span className="qh-sim-d">{[s.discipline, s.examYear ? `Çıkmış ${s.examYear}` : 'Çıkmış', s.claimedAnswer ? `Cevap: ${s.claimedAnswer}` : ''].filter(Boolean).join(' · ')}</span>
                      <div className="qh-sim-act">
                        <button type="button" onClick={() => handleTransferEntireQuestion(s)} title="Sorunun kökünü, branşını ve şıklarını forma aktar">
                          <FileText aria-hidden />{s.options && s.options.length ? 'Kök + şıkları aktar' : 'Soruyu aktar'}
                        </button>
                        <button type="button" onClick={() => handleCopyQuestionStem(s.stem)} title="Yalnızca soru kökünü forma yaz ve panoya kopyala">
                          <Copy aria-hidden />Yalnızca kökü al
                        </button>
                      </div>
                    </article>
                  ))}
                </>
              )}
            </section>

            {hasSuggest && smartAssistant && (
              <section className="qh-tip" aria-label="Öneri">
                <strong><Sparkles aria-hidden /> Öneri</strong>
                {smartAssistant.crossCommitteeWarning && smartAssistant.predictedCommittee && (
                  <>
                    <span><b>Kurul uyuşmazlığı olabilir:</b> {smartAssistant.crossCommitteeWarning}</span>
                    <button
                      type="button"
                      className="qh-tip-btn"
                      onClick={() => {
                        if (smartAssistant.predictedCommittee) {
                          onSelectCommittee(smartAssistant.predictedCommittee.committeeId);
                          if (smartAssistant.predictedDiscipline) setDiscipline(smartAssistant.predictedDiscipline.discipline);
                          toast.success('Kurul Değiştirildi', `${smartAssistant.predictedCommittee.committeeName} kuruluna geçildi.`);
                        }
                      }}
                    >
                      Bu kurula geç <ArrowRight aria-hidden />
                    </button>
                  </>
                )}
                {smartAssistant.suggestedTopics.length > 0 && (
                  <span className="qh-topics">
                    İlişkili konular:
                    {smartAssistant.suggestedTopics.slice(0, 3).map((st, i) => <em key={i}>{st.topic}</em>)}
                  </span>
                )}
                {smartAssistant.predictedDiscipline && discipline !== smartAssistant.predictedDiscipline.discipline && (
                  <button type="button" className="qh-tip-btn" onClick={() => setDiscipline(smartAssistant.predictedDiscipline!.discipline)}>
                    Dersi “{smartAssistant.predictedDiscipline.discipline}” yap
                  </button>
                )}
              </section>
            )}
          </aside>
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
    <div className="w-full max-w-[760px] mx-auto lg:mx-0 flex flex-col gap-5 pt-4 sm:pt-8">
      <div className="flex flex-col items-center text-center lg:items-start lg:text-left gap-2">
        <span className="inline-flex items-center text-sm text-ink-3">
          <span className={`w-1.5 h-1.5 rounded-full mr-2 ${isCollecting ? 'bg-ok-bright' : 'bg-line-2'}`} aria-hidden="true" />
          {committee ? titleCase(committee) : 'Kurul'}{isCollecting ? ' · toplama açık' : ''}
        </span>
        <h1 className="ms-page-title m-0 text-3xl sm:text-4xl text-ink">Aklında ne kaldı?</h1>
        {isLocked && (
          <div className="ms-pop-in flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-warn/10 border border-warn/80 text-warn text-sm font-medium mt-1">
            <Lock className="w-3.5 h-3.5 text-warn shrink-0" />
            <span>Ders programına göre sınav tamamlanmadan bu kurula soru yazılamaz.</span>
          </div>
        )}
      </div>

      <form
        onSubmit={handleSubmit}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && (e.target as HTMLElement).tagName === 'INPUT') {
            e.preventDefault();
          }
        }}
        aria-busy={isSubmitting}
        className={`relative flex flex-col gap-3 ${v12 ? 'qa12' : ''}`}
      >
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
            {!full && numaraOne}
            <label htmlFor="hatira" className="sr-only">Hatırladığın kısım</label>
            <div className={`ms-composer ${showMeta ? 'has-meta' : ''} ${full ? `is-full ${full === 'closing' ? 'is-closing' : ''}` : ''}`}>
              {full && (
                <>
                  <div className="ms-composer-top">
                    {wiz === 'kok' ? (
                      <button type="button" className="ms-composer-close" onClick={closeFull} aria-label="Kapat"><ChevronDown /></button>
                    ) : (
                      <button type="button" className="ms-composer-close" onClick={wizBack} aria-label="Geri"><ChevronLeft /></button>
                    )}
                    <span className="ms-composer-title">
                      {({ kok: 'Soru kökü', tur: 'Soru tipi', onculler: 'Öncüller', siklar: 'Şıklar', son: 'Son dokunuş' } as Record<WizStep, string>)[wiz]}
                      <small>{wizSteps.indexOf(wiz) + 1} / {wiz === 'kok' || wiz === 'tur' ? (qType === 'onculu' ? 5 : qType ? 4 : '4–5') : wizSteps.length}</small>
                    </span>
                    {/* Son adımda sağ üstte 'Havuza ekle' butonu konmaz; önceki adımda (şıklar)
                        'Devam et'e basan kullanıcının çift dokunuşla ya da refleksle künye ve
                        ipucunu doldurmadan soruyu göndermesini önlemek için gönderim yalnızca panelin
                        altındaki birincil .wz-submit butonuyla yapılır. */}
                    {wiz !== 'tur' && wiz !== 'son' ? (
                      <button type="button" className="ms-composer-send" disabled={wiz === 'kok' && !texts.stem.trim()} onClick={wizNext}>
                        Devam et
                      </button>
                    ) : <span className="w-[74px]" aria-hidden />}
                  </div>
                  <div className="wz-progress" aria-hidden><i style={{ width: `${((wizSteps.indexOf(wiz) + 1) / (qType ? wizSteps.length : 4.5)) * 100}%` }} /></div>
                  {wiz === 'kok' && numaraOne}
                </>
              )}
              <FastTextarea
                id="hatira"
                hidden={!!full && wiz !== 'kok'}
                rows={4}
                value={text}
                onFocus={openFull}
                onValue={setText}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                    e.preventDefault();
                    e.currentTarget.form?.requestSubmit();
                  }
                }}
                placeholder="Tek kelime bile işe yarar…"
                className="ms-bare-input w-full block resize-none px-4 pt-3.5 pb-2 text-md leading-[1.6] text-ink placeholder:text-ink-3 bg-transparent border-0 outline-0 min-h-[128px]"
              />
              {/* Akıllı soru tamamlama, klinik devam ve yazım yardımcısı (Masaüstü ve Mobil) */}
              <ComposerAssist
                active={(!full || full === 'open') && (wiz === 'kok' || !full) && mode === 'stem'}
                value={text}
                onChange={setText}
                textareaId="hatira"
                committeeId={committee?.id}
              />
              {full && wiz !== 'kok' && (
                <div key={wiz} className={`wz-panel ${wizDir > 0 ? 'is-fwd' : 'is-back'}`}>
                  {wiz === 'tur' && (
                    <>
                      <p className="wz-q">Soru nasıl bir soruydu?</p>
                      <div className="wz-types" role="radiogroup" aria-label="Soru tipi">
                        <button type="button" role="radio" aria-checked={qType === 'klasik'} className={`wz-type ${qType === 'klasik' ? 'is-on' : ''}`} onClick={() => pickType('klasik')}>
                          <span className="wz-type-art" aria-hidden><i /><i /><b>A</b><b>B</b><b>C</b></span>
                          <b>Klasik</b>
                          <small>Kök ve beş şık. Doğrudan şıklara geçersin.</small>
                        </button>
                        <button type="button" role="radio" aria-checked={qType === 'onculu'} className={`wz-type ${qType === 'onculu' ? 'is-on' : ''}`} onClick={() => pickType('onculu')}>
                          <span className="wz-type-art" aria-hidden><i /><em>I</em><em>II</em><em>III</em><b>Yalnız I</b></span>
                          <b>Öncüllü</b>
                          <small>I, II, III ifadeleri; şıklar “Yalnız I”, “I ve II” gibi.</small>
                        </button>
                      </div>
                    </>
                  )}
                  {wiz === 'onculler' && (
                    <>
                      <p className="wz-q">Öncülleri yaz <small>hatırladıkların yeter, sırası önemli</small></p>
                      <ol className="wz-prem">
                        {premises.map((p, i) => (
                          <li key={i}>
                            <span className="wz-prem-k">{ROMAN[i]}</span>
                            <input
                              value={p}
                              autoFocus={i === 0}
                              onChange={(e) => setPremises((list) => list.map((x, j) => (j === i ? e.target.value : x)))}
                              onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                  e.preventDefault();
                                  const ol = e.currentTarget.closest('ol');
                                  if (i === premises.length - 1 && premises.length < 6) setPremises((l) => [...l, '']);
                                  window.setTimeout(() => (ol?.querySelectorAll('input')[i + 1] as HTMLInputElement | undefined)?.focus(), 0);
                                }
                              }}
                              placeholder={`${ROMAN[i]}. öncül`}
                              aria-label={`${ROMAN[i]}. öncül`}
                              enterKeyHint="next"
                            />
                            {premises.length > 2 && (
                              <button type="button" className="wz-prem-x" onClick={() => setPremises((l) => l.filter((_, j) => j !== i))} aria-label={`${ROMAN[i]}. öncülü sil`}><X /></button>
                            )}
                          </li>
                        ))}
                      </ol>
                      {premises.length < 6 && (
                        <button type="button" className="wz-add" onClick={() => setPremises((l) => [...l, ''])}>
                          <Plus aria-hidden /> {ROMAN[premises.length]}. öncülü ekle
                        </button>
                      )}
                      <button type="button" className="wz-submit wz-next-action mt-3" onClick={wizNext}>
                        Şıklara geç <ArrowRight aria-hidden />
                      </button>
                    </>
                  )}
                  {wiz === 'siklar' && (
                    <>
                      <p className="wz-q">Şıkları yaz <small>{qType === 'onculu' ? 'kalıplara dokununca sıradaki boş şıkka yazılır' : 'A’dan E’ye; hatırladıkların yeter'}</small></p>
                      {qType === 'onculu' && (
                        <div className="wz-chips" aria-label="Sık kullanılan şık kalıpları">
                          {comboChips.map((c) => (
                            <button key={c} type="button" onClick={() => fillNextOption(c)} disabled={KEYS.filter((k) => options[k].trim()).length >= 5}>{c}</button>
                          ))}
                        </div>
                      )}
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
                      <button type="button" className="wz-submit wz-next-action mt-3" onClick={wizNext}>
                        Devam et <ArrowRight aria-hidden />
                      </button>
                    </>
                  )}
                  {wiz === 'son' && (
                    <>
                      <p className="wz-q">İpucu <small>isteğe bağlı · hocanın vurgusu, vaka ayrıntısı…</small></p>
                      <textarea
                        className="wz-clue"
                        rows={3}
                        value={texts.clue}
                        onChange={(e) => setTexts((prev) => ({ ...prev, clue: e.target.value }))}
                        placeholder={PLACEHOLDERS.clue}
                        aria-label="İpucu"
                      />
                      <p className="wz-q">Hangi soru? <small>bilmediğini boş bırak</small></p>
                      <div className="wz-kunye">
                        <MetaPicker label="Kurul" icon={Layers} value={committee ? titleCase(committee) : 'Seç'}>
                          {(close) => (
                            <ul className="qa-list" role="listbox" aria-label="Kurul">
                              {sortedCommittees.map((c) => {
                                const locked = isCommitteeLocked(c.id, examYear);
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
                        <MetaPicker label="Ders" icon={BookOpen} value={discipline} auto={autoDisc && !userManualDiscipline}>
                          {(close) => (
                            <ul className="qa-list" role="listbox" aria-label="Ders">
                              {disciplines.map((d) => (
                                <li key={d}>
                                  <button type="button" role="option" aria-selected={d === discipline} className={d === discipline ? 'is-on' : ''} onClick={() => { setDiscipline(d); setUserManualDiscipline(true); setAutoDisc(false); close(); }}>
                                    <span className="qa-list-t">{d}</span>
                                    {d === discipline && <Check className="qa-list-ok" aria-hidden />}
                                  </button>
                                </li>
                              ))}
                            </ul>
                          )}
                        </MetaPicker>
                        <MetaPicker label="Sene" icon={CalendarDays} value={examYear ? `${examYear.slice(0, 4)}–${examYear.slice(7, 9)}` : 'Bilmiyorum'} empty={!examYear}>
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
                        <label className={`qa-tok is-num ${!questionNumber ? 'is-empty' : ''}`}>
                          <Hash className="qa-tok-i" aria-hidden />
                          <span className="qa-tok-l">Soru no</span>
                          <input
                            type="text"
                            inputMode="numeric"
                            value={questionNumber}
                            onChange={(e) => { setQuestionNumber(e.target.value.replace(/[^0-9]/g, '').slice(0, 3)); setUserManualNumber(true); setAutoNum(false); }}
                            enterKeyHint="done"
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') {
                                e.preventDefault();
                                e.stopPropagation();
                                (e.target as HTMLInputElement).blur();
                              }
                            }}
                            placeholder="bilmiyorum"
                            aria-label="Soru numarası (bilmiyorsan boş bırak)"
                          />
                        </label>
                      </div>
                      <div className="wz-sum">
                        <span>{texts.stem.trim() ? texts.stem.trim().split(/\s+/).length : 0} kelime kök</span>
                        {qType === 'onculu' && <span>{premises.filter((p) => p.trim()).length} öncül</span>}
                        <span>{filledOptionCount} şık{claimedAnswer ? ` · cevap ${claimedAnswer}` : ''}</span>
                      </div>
                      {formError && <div role="alert" className="qa-note is-bad">{formError}</div>}
                      <button type="submit" className="wz-submit" disabled={isSubmitting || isLocked}>
                        {isSubmitting ? 'Ekleniyor…' : 'Havuza ekle'} <ArrowRight aria-hidden />
                      </button>
                    </>
                  )}
                </div>
              )}
              {/* Alt şerit: soru kimliği. Ders ve numara akıllı etiketler; otomatik dolanlar işaretli */}
              {showMeta && (
                <div className="ms-meta" data-no-tip>
                  <MetaPicker variant="token" label="Kurul" icon={Layers} value={committee ? titleCase(committee) : 'Kurul'} width={280}>
                    {(close) => (
                      <ul className="qa-list" role="listbox" aria-label="Kurul">
                        {sortedCommittees.map((c) => {
                          const locked = isCommitteeLocked(c.id, examYear);
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
                    <span className="hidden sm:inline ml-auto text-xs text-ink-3 truncate">Eşleşen taslaktan dolduruldu</span>
                  )}
                </div>
              )}
            </div>
            {mode !== 'stem' && spell?.text && spell.text !== dismissedSpell && (
              <div className="ms-pop-in flex items-center gap-2 text-base text-ink-2 min-w-0">
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
              <div className="ms-fade-in flex items-center gap-2 px-3 py-1.5 rounded-xl bg-accent-soft/60 border border-accent/20 text-accent text-xs font-medium w-fit">
                <span className="w-2 h-2 rounded-full bg-accent animate-ping" />
                <span className="flex items-center gap-1">
                  <Sparkles className="w-3.5 h-3.5 animate-spin" />
                  Benzer soru, kurul ve taslaklar taranıyor…
                </span>
              </div>
            )}

            {/* Seçili Soruya / Taslağa Bağlandı Rozeti */}
            {linkedQuestion && (
              <div className="ms-pop-in flex items-center justify-between gap-2 px-3.5 py-2 rounded-xl bg-ok-soft border border-ok/30 text-ok text-sm">
                <div className="flex items-center gap-2 min-w-0">
                  <Link2 className="w-4 h-4 text-ok shrink-0" />
                  <span className="font-semibold text-ok truncate">
                    {linkedQuestion.questionNumber ? `Soru #${linkedQuestion.questionNumber} ile bağlandı` : 'Mevcut taslakla bağlandı'}
                  </span>
                  <span className="text-ok text-xs hidden sm:inline truncate">
                    (Yazdıkların bu sorunun katkılarına eklenecek)
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => {
                    setLinkedQuestion(null);
                    setQuestionNumber('');
                  }}
                  className="p-1 text-ok hover:text-ok hover:bg-ok-soft rounded-lg cursor-pointer transition-colors shrink-0"
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
          <div className="ms-pop-in rounded-2xl bg-warn/10 border border-warn/80 p-3.5 flex flex-col gap-2.5">
            {smartAssistant.crossCommitteeWarning && smartAssistant.predictedCommittee && (
              <div className="flex items-start justify-between gap-3 flex-wrap sm:flex-nowrap">
                <div className="flex items-start gap-2 text-sm text-warn leading-snug">
                  <AlertCircle className="w-4 h-4 text-warn shrink-0 mt-0.5" />
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
                  className="shrink-0 h-8 px-3 rounded-xl bg-warn hover:bg-warn text-white text-xs font-bold inline-flex items-center gap-1 cursor-pointer transition-colors shadow-xs"
                >
                  Bu Kurula Geç
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            )}

            {/* Tespit Edilen Tıbbi Konular / Kavramlar */}
            {smartAssistant.suggestedTopics.length > 0 && (
              <div className="flex items-center gap-1.5 flex-wrap pt-0.5">
                <span className="text-xs font-bold uppercase tracking-wider text-warn/80 flex items-center gap-1">
                  <Sparkles className="w-3 h-3 text-warn" />
                  İlişkili Konu Önerileri:
                </span>
                {smartAssistant.suggestedTopics.slice(0, 3).map((st, i) => (
                  <span
                    key={i}
                    className="h-6 px-2.5 rounded-full bg-white text-warn text-xs font-semibold border border-warn/30 shadow-2xs inline-flex items-center gap-1"
                  >
                    {st.topic}
                  </span>
                ))}
                {smartAssistant.predictedDiscipline && discipline !== smartAssistant.predictedDiscipline.discipline && (
                  <button
                    type="button"
                    onClick={() => setDiscipline(smartAssistant.predictedDiscipline!.discipline)}
                    className="h-6 px-2.5 rounded-full bg-accent/15 hover:bg-accent/25 text-accent text-xs font-bold border border-accent/30 inline-flex items-center gap-1 cursor-pointer transition-colors"
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
              <span className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-ink-3">
                <Sparkles className="w-3.5 h-3.5 text-accent animate-pulse" />
                Benzer Taslaklar ({realtimeMatches.length})
              </span>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={selectedMatchIds.size === realtimeMatches.length ? clearSelection : selectAllMatches}
                  className="text-xs font-semibold text-accent hover:underline cursor-pointer"
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
                          <span className="h-5 px-2 rounded-full bg-accent text-white text-2xs font-bold uppercase tracking-wider">
                            En Yakın
                          </span>
                        )}

                        <span className={`h-6 px-2.5 rounded-full text-xs font-semibold inline-flex items-center gap-1 border ${tier.pillBg}`}>
                          <span className={`w-1.5 h-1.5 rounded-full ${tier.barColor}`} />
                          %{m.compatibility.score} · {tier.tierName}
                        </span>

                        {m.isCrossCommittee && (
                          <span className="h-5 px-2 rounded-full bg-ai text-white text-2xs font-bold uppercase tracking-wider">
                            Farklı Kurul Taslağı
                          </span>
                        )}

                        {m.contextHashtag && m.compatibility.score >= HIGHLIGHT_MIN_SCORE && (
                          <ContextBadge hashtag={m.contextHashtag} colorIndex={idx} />
                        )}
                      </div>

                      <span className="text-xs font-mono font-bold text-ink-2">
                        {q.questionNumber ? `Soru #${q.questionNumber}` : 'Numarasız'}
                      </span>
                    </div>

                    <div className="text-sm leading-relaxed text-ink bg-white/90 rounded-xl p-2.5 border border-line-soft">
                      <Colored text={stem} colors={sharedColors} />
                    </div>

                    <div className="flex items-center justify-between gap-2 pt-1">
                      <div className="flex items-center gap-1.5 flex-wrap">
                        <button
                          type="button"
                          onClick={() => handleLinkToQuestion(q)}
                          className="h-7 px-2.5 rounded-lg bg-white hover:bg-canvas text-ink text-xs font-medium border border-line inline-flex items-center gap-1 cursor-pointer transition-colors shadow-2xs"
                        >
                          <CheckCircle2 className="w-3.5 h-3.5 text-accent" />
                          {q.questionNumber ? `S.${q.questionNumber} ile Bağla` : 'Bu Taslakla Bağla'}
                        </button>
                        {isAdmin && <button
                          type="button"
                          onClick={() => setOptimizingQuestion(q)}
                          className="h-7 px-2.5 rounded-lg bg-accent-soft hover:bg-accent/20 text-accent text-xs font-semibold inline-flex items-center gap-1 cursor-pointer transition-colors shadow-2xs"
                          title="Taslağı amfi slaytları ve AI ile tam soruya dönüştür"
                        >
                          <Wand2 className="w-3.5 h-3.5" />
                          AI ile Dönüştür
                        </button>}
                        <button
                          type="button"
                          onClick={() => rejectMatch(q.id)}
                          className="h-7 px-2.5 rounded-lg text-ink-2 hover:text-ink hover:bg-canvas text-xs font-medium inline-flex items-center gap-1 cursor-pointer transition-colors"
                          title="Bu öneri benim hatırladığım soru değil (öneriler bundan öğrenir)"
                        >
                          <X className="w-3.5 h-3.5" />
                          Farklı soru
                        </button>
                      </div>
                      {q.discipline && (
                        <span className="text-xs text-ink-3 truncate">{q.discipline}</span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Ortak kelimeler renk kılavuzu */}
            <WordLegend texts={[debouncedText || text, ...realtimeMatches.map((m) => questionStemText(m.question))]} colors={sharedColors} />

            {/* Seçim yapıldığında ortaya çıkan bağlamsal çubuk */}
            {selectedMatchIds.size > 0 && (
              <div className="ms-pop-in sticky bottom-3 z-20 flex items-center justify-between gap-3 p-3 rounded-2xl bg-ink text-white shadow-xl border border-white/10 backdrop-blur-md">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="w-6 h-6 rounded-full bg-accent text-white text-xs font-bold flex items-center justify-center shrink-0">
                    {selectedMatchIds.size}
                  </span>
                  <span className="text-sm font-medium truncate">
                    {selectedMatchIds.size === 1
                      ? '1 soru seçildi'
                      : `${selectedMatchIds.size} soru seçildi`}
                  </span>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <button
                    type="button"
                    onClick={clearSelection}
                    className="h-8 px-2.5 rounded-lg hover:bg-white/10 text-white/80 hover:text-white text-xs font-medium cursor-pointer transition-colors"
                  >
                    İptal
                  </button>
                  <button
                    type="button"
                    disabled={isMergingSelected}
                    onClick={handleMergeAndGroupSelected}
                    className="h-8 px-3.5 rounded-lg bg-accent hover:bg-accent-hover text-white text-sm font-bold inline-flex items-center gap-1.5 cursor-pointer shadow-md disabled:opacity-50 transition-colors"
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
            className="ms-pop-in w-full min-h-11 px-4 rounded-2xl bg-field hover:bg-line flex items-center gap-3 text-left text-base cursor-pointer"
          >
            <span className="h-6 min-w-6 px-2 rounded-full bg-accent-soft text-accent text-xs font-semibold inline-flex items-center justify-center">
              {similar.length}
            </span>
            <span className="flex-1 text-ink-2">benzer çıkmış soru bulundu</span>
            <span className="text-sm text-ink-3">{simOpen ? 'Gizle' : 'Göster'}</span>
          </button>
        )}
        {simOpen && similar.length > 0 && mode !== 'option' && (
          <ul className="list-none m-0 p-0 flex flex-col gap-2">
            {similar.map((s, i) => (
              <li
                key={s.id}
                className="ms-pop-in p-3 rounded-xl bg-field/60 border border-line-soft hover:bg-field text-base text-ink flex flex-col gap-2"
                style={{ animationDelay: `${i * 60}ms` }}
              >
                <div className="flex flex-col gap-0.5 min-w-0">
                  <span className="line-clamp-2 text-ink-2 font-medium">{s.stem}</span>
                  {s.options && s.options.length > 0 && (
                    <ol className="m-0 mt-1 p-0 list-none grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-0.5 text-sm text-ink-2">
                      {s.options.map((o) => (
                        <li key={o.key} className={`min-w-0 truncate ${o.key === s.claimedAnswer ? 'text-ok font-semibold' : ''}`}>
                          <span className="font-mono text-ink-3 mr-1">{o.key})</span>{o.text}
                        </li>
                      ))}
                    </ol>
                  )}
                  <span className="text-xs text-ink-3">
                    {[s.discipline, s.examYear ? `Çıkmış ${s.examYear}` : 'Çıkmış', s.claimedAnswer ? `Cevap: ${s.claimedAnswer}` : ''].filter(Boolean).join(' · ')}
                  </span>
                </div>
                <div className="flex items-center gap-2 pt-1 border-t border-line-soft">
                  <button
                    type="button"
                    onClick={() => handleTransferEntireQuestion(s)}
                    className="h-7 px-2.5 rounded-lg bg-accent text-white text-xs font-semibold inline-flex items-center gap-1 cursor-pointer hover:bg-accent-hover shadow-2xs transition-colors"
                    title="Sorunun kökünü, branşını ve şıklarını editöre aktar"
                  >
                    <FileText className="w-3.5 h-3.5" />
                    {s.options && s.options.length ? 'Kök + şıkları aktar' : 'Soruyu aktar'}
                  </button>
                  <button
                    type="button"
                    onClick={() => handleCopyQuestionStem(s.stem)}
                    className="h-7 px-2.5 rounded-lg bg-white text-ink text-xs font-medium border border-line inline-flex items-center gap-1 cursor-pointer hover:bg-canvas shadow-2xs transition-colors"
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

        <div className="flex items-center gap-2 text-sm text-ink-3">
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
            className="h-12 sm:h-11 px-6 rounded-full bg-accent hover:bg-accent-hover text-white text-md sm:text-md font-semibold cursor-pointer disabled:opacity-60 transition-colors shrink-0"
          >
            {isSubmitting ? 'Kaydediliyor…' : 'Havuza ekle'}
          </button>
        </div>

        {formError && (
          <div role="alert" className="ms-shake px-4 py-3 rounded-2xl bg-bad-soft text-bad-text text-base">{formError}</div>
        )}
        {successMessage && (
          <div role="status" className="ms-pop-in px-4 py-3 rounded-2xl bg-ok-soft text-ok text-base font-medium">Teşekkürler! {successMessage}</div>
        )}
        {intakeId && <IntakeEcho key={intakeId} intakeId={intakeId} onClose={() => setIntakeId(null)} />}
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
};
