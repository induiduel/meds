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
} from 'lucide-react';
import { Committee, QuestionItem } from '../types';
import { AppUser } from '../services/auth';
import { getDefaultActiveCommitteeId, filterCurrent2026_2027Committees } from '../services/firestoreDb';
import { pathFor, linkClick } from '../router';
import { OptionsEditor } from './ui/OptionsEditor';
import { BlurOverlay, SuccessCheck } from './ui/Animations';
import { toast } from './ui/Toast';
import { ApiService, SimilarPastQuestion, SourceRefLite } from '../services/api';
import { useUiVersion } from '../utils/uiVersion';
import { findRealtimeMatchingDrafts, RealtimeMatchItem, DraftCompatibilityResult } from '../services/draftClusteringService';
import { getSmartQuestionAssistant, SmartQuestionAssistantResult } from '../services/medicalPredictorService';
import { Colored, WordLegend, ContextBadge, sharedWordColors } from './draftHighlight';
import { AiQuestionOptimizerModal } from './AiQuestionOptimizerModal';

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
  }) => Promise<void>;
  unassignedCount: number;
  totalQuestionsCount: number;
  questions?: QuestionItem[];
  onOpenQuestion?: (question: QuestionItem) => void;
  onNavigateTab: (tab: 'matrix' | 'questions' | 'practice' | 'booklet' | 'notes' | 'past_exams' | 'study' | 'learn') => void;
  isAdmin: boolean;
  currentUser?: AppUser | null;
  onOpenAdminPanel?: () => void;
}

const SAVED_NAME_KEY = 'medsoru_saved_contributor_name';

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
  if (m) return `KURUL ${m[1]}`;
  if (/bütünleme/i.test(c.name)) return 'BÜTÜNLEME';
  if (/final/i.test(c.name)) return 'FİNAL';
  return (c.code || c.name).toLocaleUpperCase('tr-TR');
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
  const short = committeeShortLabel(c);
  return short.charAt(0) + short.slice(1).toLocaleLowerCase('tr-TR');
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
  questions = [],
  onNavigateTab,
  currentUser,
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

  // 1. Yazarken gecikmeli metin (debouncedText) güncelleme (250ms)
  useEffect(() => {
    const timer = window.setTimeout(() => {
      setDebouncedText(text.trim());
    }, 250);
    return () => window.clearTimeout(timer);
  }, [text]);

  // 2. Anlık taslak eşleme ve Kurul/Ders tahmin asistanı: debouncedText üzerinden çalışır
  useEffect(() => {
    const q = debouncedText;
    if (mode === 'option' || q.length < 8 || !committee?.id) {
      setRealtimeMatches([]);
      setSelectedMatchIds(new Set());
      setSmartAssistant(null);
      return;
    }

    const optionsList = KEYS.filter((k) => options[k].trim()).map((k) => ({ key: k, text: options[k].trim() }));

    // 1. Akıllı Asistan Analizi (Kurul, Ders, Tıbbi Kavram & Çapraz Kurul Tespiti)
    const assistantRes = getSmartQuestionAssistant(q, optionsList, committee.id);
    setSmartAssistant(assistantRes);

    // 2. Taslak Eşleme (Çapraz Kurul Desteği ile)
    const matches = findRealtimeMatchingDrafts(
      {
        committeeId: committee.id,
        discipline,
        topic: `${discipline} Hatırlanan Soru`,
        text: q,
        options: optionsList.length > 0 ? optionsList : undefined,
      },
      questions,
      35, // En az %35 benzerlik
      4,  // En fazla 4 aday göster
      true // Çapraz kurul taslaklarını da göster
    );
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
  }, [debouncedText, mode, committee?.id, discipline, options, questions]);

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

  // Bir soruya doğrudan bağlama aksiyonu
  const handleLinkToQuestion = (targetQ: QuestionItem) => {
    if (targetQ.questionNumber) {
      setQuestionNumber(String(targetQ.questionNumber));
    }
    if (targetQ.discipline && targetQ.discipline !== 'Belirtilmedi') {
      setDiscipline(targetQ.discipline);
    }
    toast.success(
      'Soruya bağlandı',
      targetQ.questionNumber
        ? `Parçan Soru #${targetQ.questionNumber} ile birleştirilecek.`
        : 'Parçan mevcut taslağa eklenecek.'
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
      setSelectedMatchIds(new Set());
      setRealtimeMatches([]);
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
      });
      setTexts({ stem: '', clue: '' });
      setOptions({ A: '', B: '', C: '', D: '', E: '' });
      setOptionCount(1);
      setAnswerReason('');
      setClaimedAnswer(undefined);
      setQuestionNumber('');
      setSuccessMessage(
        hasNumber
          ? `Soru ${num} için eklediğin parça havuza kaydedildi.`
          : 'Parçan havuza kaydedildi. Numarası bilinmeyenler benzerlerine göre yerleştirilir.'
      );
      setTimeout(() => setSuccessMessage(null), 6000);
    } catch (err: any) {
      setFormError('Kayıt sırasında bir hata oluştu: ' + (err?.message || 'bilinmeyen hata'));
      toast.error('Parça kaydedilemedi', err?.message || 'Bağlantını kontrol edip tekrar dene.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const field = 'bg-field border border-transparent outline-0 focus:border-accent focus:bg-white';

  // v3 · minimal ana sayfa: tek alan, tek düğme. Benzerler ve şıklar yalnızca istenince.
  if (isV3) {
    return (
      <div className="w-full max-w-[680px] mx-auto flex flex-col gap-5 pt-6 sm:pt-16">
        <div className="flex flex-col items-center text-center gap-2">
          <label className="relative inline-flex items-center text-[13px] text-ink-3">
            <span className="sr-only">Kurul seç</span>
            <span className={`w-1.5 h-1.5 rounded-full mr-2 ${isCollecting ? 'bg-ok-bright' : 'bg-line-2'}`} aria-hidden="true" />
            <select
              value={committee?.id || ''}
              onChange={(e) => onSelectCommittee(e.target.value)}
              className="appearance-none bg-transparent border-0 outline-0 cursor-pointer pr-4 text-ink-3 hover:text-ink [field-sizing:content]"
            >
              {sortedCommittees.map((c) => (
                <option key={c.id} value={c.id}>
                  {titleCase(c)}
                  {c.id === activeCommitteeId ? ' · toplama açık' : ''}
                </option>
              ))}
            </select>
            <ChevronDown className="pointer-events-none absolute right-0 w-3 h-3" aria-hidden="true" />
          </label>
          <h1 className="ms-page-title m-0 text-[30px] sm:text-[40px] text-ink">Aklında ne kaldı?</h1>
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
              <textarea
                id="hatira"
                rows={4}
                value={text}
                onChange={(e) => setText(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                    e.preventDefault();
                    e.currentTarget.form?.requestSubmit();
                  }
                }}
                placeholder="Tek kelime bile işe yarar…"
                className="resize-none rounded-2xl px-4 py-3.5 text-[16px] leading-[1.6] text-ink placeholder:text-ink-3 bg-field border-0 outline-0 focus:bg-white focus:ring-2 focus:ring-accent transition-[background,box-shadow] min-h-[140px]"
              />
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
            <ul className="list-none m-0 p-0 flex flex-col">
              {similar.map((s, i) => (
                <li key={s.id} className="ms-pop-in px-4 py-2.5 rounded-xl hover:bg-field text-[14px] text-ink-2" style={{ animationDelay: `${i * 60}ms` }} title={s.stem}>
                  <span className="line-clamp-2">{s.stem}</span>
                  <span className="block text-[12px] text-ink-3 mt-0.5">{[s.discipline, s.examYear].filter(Boolean).join(' · ')}</span>
                </li>
              ))}
            </ul>
          )}

          <div className="flex flex-wrap items-center gap-x-2 gap-y-2 text-[13px] text-ink-3">
            <select
              value={discipline}
              onChange={(e) => setDiscipline(e.target.value)}
              aria-label="Ders"
              className="appearance-none bg-transparent border-0 outline-0 cursor-pointer max-w-[220px] truncate hover:text-ink [field-sizing:content]"
            >
              {disciplines.map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
            <span aria-hidden="true">·</span>
            <input
              type="text"
              inputMode="numeric"
              value={questionNumber}
              onChange={(e) => setQuestionNumber(e.target.value.replace(/[^0-9]/g, '').slice(0, 3))}
              placeholder="numara?"
              aria-label="Soru numarası (bilmiyorsan boş bırak)"
              className="w-[70px] bg-transparent border-0 outline-0 placeholder:text-ink-3 text-ink"
            />
            <button
              type="button"
              onClick={() => setMode(mode === 'option' ? 'stem' : 'option')}
              className="h-8 px-3 rounded-full hover:bg-field text-accent font-semibold cursor-pointer"
            >
              {mode === 'option' ? 'Soru köküne dön' : claimedAnswer ? `Şıklar · ${claimedAnswer}` : 'Şık ekle'}
            </button>
            <span className="flex-1" />
            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full sm:w-auto h-12 sm:h-11 px-6 rounded-full bg-accent hover:bg-accent-hover text-white text-[15px] sm:text-[14.5px] font-semibold cursor-pointer disabled:opacity-60 transition-colors"
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
      </div>
    );
  }


  return (
    <div className="w-full max-w-[1200px] mx-auto grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_340px] gap-4 lg:gap-5 md:pt-2">
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
            {sortedCommittees.map((c) => (
              <option key={c.id} value={c.id}>
                {titleCase(c)}
                {c.id === activeCommitteeId ? ' · toplama açık' : ''}
              </option>
            ))}
          </select>
          <ChevronDown className="pointer-events-none absolute right-2.5 w-3.5 h-3.5 opacity-70" aria-hidden="true" />
        </label>
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
            <div className="flex items-center gap-1.5 text-[12px] text-ink-3 -mt-1">
              <span className="font-mono">{text.length} karakter</span>
              <span aria-hidden="true">·</span>
              <span className="truncate">Şıkları “Şıklar” sekmesinden ekleyebilirsin</span>
            </div>
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
                  <div className="px-2.5 pb-2 text-[12px] text-ink-3">
                    {[s.discipline, s.title].filter(Boolean).join(' · ')}
                    {s.claimedAnswer ? ` · Cevap: ${s.claimedAnswer}` : ''}
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
              onChange={(e) => setDiscipline(e.target.value)}
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
              onChange={(e) => setQuestionNumber(e.target.value.replace(/[^0-9]/g, '').slice(0, 3))}
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
          onSaved={(updated) => {
            setOptimizingQuestion(null);
            toast.success('Taslak Geliştirildi', `Soru #${updated.questionNumber || 'taslak'} başarıyla güncellendi.`);
          }}
        />
      )}
    </div>
  );
};
