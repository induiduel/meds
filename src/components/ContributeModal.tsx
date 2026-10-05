import React, { useState, useEffect, useMemo } from 'react';
import { X, Sparkles, Stethoscope, AlertCircle, ArrowRight, ChevronDown } from 'lucide-react';
import { OptionsEditor, OPTION_KEYS, OptionKey } from './ui/OptionsEditor';
import { BlurOverlay, SuccessCheck } from './ui/Animations';
import { toast } from './ui/Toast';
import { Committee, QuestionItem } from '../types';
import { AppUser } from '../services/auth';
import { findRealtimeMatchingDraft, DraftCompatibilityResult } from '../services/draftClusteringService';
import { getSmartQuestionAssistant, SmartQuestionAssistantResult } from '../services/medicalPredictorService';
import { Collapsible } from './ui/Collapsible';
import { ApiService, safeJsonFetch, type SimilarPastQuestion } from '../services/api';
import { Colored, WordLegend, ContextBadge, sharedWordColors } from './draftHighlight';
import { validateNamePolicy } from '../utils/namePolicy';

const SAVED_NAME_KEY = 'medsoru_saved_contributor_name';

interface ContributeModalProps {
  isOpen: boolean;
  onClose: () => void;
  committees: Committee[];
  selectedCommitteeId: string;
  defaultQuestionNumber?: number;
  currentUser?: AppUser | null;
  questions?: QuestionItem[];
  onAddQuestionContribution: (data: {
    committeeId: string;
    questionNumber?: number;
    isUnknownNumber?: boolean;
    discipline: string;
    topic: string;
    fragmentText: string;
    author: string;
    authorUid?: string;
    authorStudentNumber?: string;
    claimedAnswer?: 'A' | 'B' | 'C' | 'D' | 'E';
    options?: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string }[];
  }) => Promise<void>;
}

const DISCIPLINES = [
  'Patoloji',
  'Farmakoloji',
  'Tıbbi Mikrobiyoloji',
  'Dahiliye',
  'Göğüs Hastalıkları',
  'Kardiyoloji',
  'Pediatri',
  'Anatomi',
  'Fizyoloji',
  'Tıbbi Biyokimya',
  'Tıbbi Biyoloji & Genetik',
  'Halk Sağlığı',
];

export const ContributeModal: React.FC<ContributeModalProps> = ({
  isOpen,
  onClose,
  committees,
  selectedCommitteeId,
  defaultQuestionNumber,
  currentUser,
  questions = [],
  onAddQuestionContribution,
}) => {
  const [committeeId, setCommitteeId] = useState(selectedCommitteeId);
  const selectedComm = committees.find((c) => c.id === committeeId) || committees[0];
  const activeDisciplines = (selectedComm?.disciplines && selectedComm.disciplines.length > 0)
    ? selectedComm.disciplines
    : DISCIPLINES;

  const [isUnknownNumber, setIsUnknownNumber] = useState(!defaultQuestionNumber);
  const [questionNumber, setQuestionNumber] = useState(defaultQuestionNumber || 1);
  const [discipline, setDiscipline] = useState(activeDisciplines[0] || 'Farmakoloji');
  const [topic, setTopic] = useState('');
  const [fragmentText, setFragmentText] = useState('');
  const [author, setAuthor] = useState(() => currentUser?.displayName || localStorage.getItem(SAVED_NAME_KEY) || '');
  const [claimedAnswer, setClaimedAnswer] = useState<'A' | 'B' | 'C' | 'D' | 'E' | ''>('');

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Akıllı Taslak Eşleştirme Canlı Durumu
  const [realtimeMatch, setRealtimeMatch] = useState<{
    matchedQuestion?: QuestionItem;
    compatibility?: DraftCompatibilityResult;
    contextHashtag?: string;
  } | null>(null);

  React.useEffect(() => {
    if (isOpen) {
      if (selectedCommitteeId) {
        setCommitteeId(selectedCommitteeId);
      }
      if (defaultQuestionNumber) {
        setQuestionNumber(defaultQuestionNumber);
        setIsUnknownNumber(false);
      } else {
        setIsUnknownNumber(true);
      }
      setFormError(null);
      setSaveSuccess(false);
    }
  }, [isOpen, selectedCommitteeId, defaultQuestionNumber]);

  React.useEffect(() => {
    if (currentUser?.displayName && !author) {
      setAuthor(currentUser.displayName);
    }
  }, [currentUser]);

  const handleAuthorChange = (val: string) => {
    setAuthor(val);
    localStorage.setItem(SAVED_NAME_KEY, val);
  };

  React.useEffect(() => {
    if (activeDisciplines && activeDisciplines.length > 0) {
      if (!activeDisciplines.includes(discipline)) {
        setDiscipline(activeDisciplines[0]);
      }
    }
  }, [committeeId, selectedComm]);

  // Remembered options: start with one row, grow with (+)
  const [options, setOptions] = useState<Record<OptionKey, string>>({ A: '', B: '', C: '', D: '', E: '' });
  const [optionCount, setOptionCount] = useState(1);
  const [answerReason, setAnswerReason] = useState('');
  const filledOptions = OPTION_KEYS.filter((k) => options[k].trim()).map((k) => ({ key: k, text: options[k].trim() }));

  const [smartAssistant, setSmartAssistant] = useState<SmartQuestionAssistantResult | null>(null);

  // Canlı Benzerlik Taraması & Akıllı Kurul/Ders Tahmini (Debounce ile 350ms)
  useEffect(() => {
    if (!fragmentText || fragmentText.trim().length < 8) {
      setRealtimeMatch(null);
      setSmartAssistant(null);
      return;
    }

    const timer = setTimeout(() => {
      // 1. Akıllı Asistan Analizi (Kurul, Ders, Tıbbi Kavram & Çapraz Kurul Tespiti)
      const assistantRes = getSmartQuestionAssistant(fragmentText, filledOptions, committeeId || selectedCommitteeId);
      setSmartAssistant(assistantRes);

      // 2. Taslak Eşleştirme
      if (!questions || questions.length === 0) {
        setRealtimeMatch(null);
        return;
      }

      const match = findRealtimeMatchingDraft(
        {
          committeeId: committeeId || selectedCommitteeId,
          discipline,
          topic,
          text: fragmentText,
          options: filledOptions,
        },
        questions
      );

      if (match.matchFound && match.matchedQuestion) {
        setRealtimeMatch({
          matchedQuestion: match.matchedQuestion,
          compatibility: match.compatibility,
          contextHashtag: match.contextHashtag,
        });
      } else {
        setRealtimeMatch(null);
      }
    }, 350);

    return () => clearTimeout(timer);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fragmentText, discipline, topic, options, questions, committeeId]);

  const matchedStem = useMemo(() => {
    if (!realtimeMatch?.matchedQuestion) return '';
    const q = realtimeMatch.matchedQuestion;
    return q.reconstruction?.stem || (q as any)?.stem || q.fragments?.[0]?.text || q.topic || '';
  }, [realtimeMatch]);

  const sharedColors = useMemo(() => {
    if (!realtimeMatch?.matchedQuestion || !fragmentText.trim() || !matchedStem) return new Map<string, string>();
    return sharedWordColors([fragmentText, matchedStem]);
  }, [realtimeMatch, fragmentText, matchedStem]);

  // Past exam questions that look like what the student remembers (debounced, retrieval only)
  const [similarPast, setSimilarPast] = useState<SimilarPastQuestion[]>([]);
  useEffect(() => {
    const text = `${topic} ${fragmentText}`.trim();
    if (text.length < 12) {
      setSimilarPast([]);
      return;
    }
    let cancelled = false;
    const timer = setTimeout(async () => {
      const results = await ApiService.findSimilarPastQuestions(text, committeeId || selectedCommitteeId);
      if (!cancelled) setSimilarPast(results);
    }, 600);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [fragmentText, topic, committeeId, selectedCommitteeId]);

  const [aiAssisting, setAiAssisting] = useState(false);
  const [aiSuggestion, setAiSuggestion] = useState<{
    suggestedStem?: string;
    suggestedOptions?: { key: string; text: string }[];
    probableAnswer?: string;
    sources?: { title: string; pageNumber?: number }[];
  } | null>(null);

  // Escape closes (unless saving)
  useEffect(() => {
    if (!isOpen) return;
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && !isSubmitting && onClose();
    document.addEventListener('keydown', onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = prev;
    };
  }, [isOpen, isSubmitting, onClose]);

  if (!isOpen) return null;

  const handleQuickAiAssist = async () => {
    if (!fragmentText.trim()) return;
    setAiAssisting(true);
    try {
      const res = await safeJsonFetch<any>('/api/ai/quick-assist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          committeeId: committeeId || selectedCommitteeId,
          discipline,
          topic,
          fragment: fragmentText,
        }),
      });
      if (!res.ok || !res.data) throw new Error(res.error || 'AI önerisi alınamadı');
      const data = res.data;
      setAiSuggestion(data);
      if (data.suggestedOptions) {
        let maxIdx = optionCount - 1;
        setOptions((prev) => {
          const next = { ...prev };
          data.suggestedOptions.forEach((opt: { key: string; text: string }) => {
            const k = String(opt.key || '').toUpperCase() as OptionKey;
            if (OPTION_KEYS.includes(k) && !next[k]) {
              next[k] = opt.text;
              maxIdx = Math.max(maxIdx, OPTION_KEYS.indexOf(k));
            }
          });
          return next;
        });
        setOptionCount(maxIdx + 1);
      }
    } catch (e: any) {
      console.error(e);
      toast.error('AI önerisi alınamadı', 'Sunucuya ulaşılamadı. Biraz sonra tekrar dene.');
    } finally {
      setAiAssisting(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    const trimmedStem = fragmentText.trim();
    const hasOptions = filledOptions.length > 0;
    const hasTopic = topic.trim().length > 0;
    const hasClaimedAnswer = Boolean(claimedAnswer);

    // Kök, şık, konu veya doğru cevaptan en az biri girilmiş olmalı
    if (!trimmedStem && !hasOptions && !hasTopic && !hasClaimedAnswer) {
      setFormError('Soru kökünden, şıklardan ya da konudan en az birini yaz.');
      return;
    }

    if (!isUnknownNumber) {
      const maxTarget = selectedComm?.targetCount || 150;
      const num = Number(questionNumber);
      if (!Number.isFinite(num) || num < 1 || num > maxTarget) {
        setFormError(`Soru numarası 1 ile ${maxTarget} arasında olmalı. Hatırlamıyorsan numarayı boş bırak.`);
        return;
      }
    }

    if (author.trim()) {
      const nameCheck = validateNamePolicy(author.trim());
      if (!nameCheck.isValid) {
        setFormError(nameCheck.errorMessage || 'Geçersiz isim girdiniz.');
        return;
      }
    }

    setIsSubmitting(true);
    try {
      const finalTopic =
        topic.trim() || (trimmedStem ? (trimmedStem.length > 50 ? trimmedStem.substring(0, 50) + '...' : trimmedStem) : `${discipline} Taslak Sorusu`);
      const reasonLine = claimedAnswer && answerReason.trim() ? `Cevap notu (${claimedAnswer}): ${answerReason.trim()}` : '';

      await onAddQuestionContribution({
        committeeId: committeeId || selectedCommitteeId,
        questionNumber: isUnknownNumber ? undefined : Number(questionNumber),
        isUnknownNumber,
        discipline,
        topic: finalTopic,
        fragmentText: [trimmedStem, reasonLine].filter(Boolean).join('\n'),
        author: author.trim() || currentUser?.displayName || 'Anonim Tıbbiyeli',
        authorUid: currentUser?.uid,
        authorStudentNumber: currentUser?.studentNumber || undefined,
        claimedAnswer: (claimedAnswer as any) || undefined,
        options: filledOptions,
      });

      setSaveSuccess(true);
      setTimeout(() => {
        onClose();
      }, 1400);
    } catch (err: any) {
      console.error('ContributeModal submit error:', err);
      setFormError('Kaydedilirken bir sorun oluştu: ' + (err?.message || 'Lütfen tekrar dene.'));
      toast.error('Soru kaydedilemedi', err?.message || 'Bağlantını kontrol edip tekrar dene.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const fieldCls =
    'w-full rounded-xl bg-field border border-transparent px-3.5 text-[15px] text-ink outline-0 focus:border-accent focus:bg-white placeholder:text-slate-600';
  const labelCls = 'text-[12px] font-semibold uppercase tracking-[0.07em] text-ink-3';

  return (
    <div
      className="ms-overlay fixed inset-0 z-[70] bg-[rgba(14,26,38,0.45)] backdrop-blur-[3px] flex items-end sm:items-center justify-center sm:p-5 ms-fade-in"
      onMouseDown={(e) => e.target === e.currentTarget && !isSubmitting && onClose()}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="contribute-title"
        className="relative w-full sm:max-w-[600px] max-h-[calc(var(--vvh,100dvh)-12px)] sm:max-h-[92dvh] bg-white rounded-t-2xl sm:rounded-2xl shadow-xl grid grid-rows-[auto_minmax(0,1fr)_auto] overflow-hidden ms-pop-in"
      >
        {/* Header */}
        <header className="flex items-center gap-3 px-5 pt-3 sm:pt-4 pb-3 border-b border-line-soft">
          <span className="sm:hidden absolute left-1/2 -translate-x-1/2 top-1.5 w-10 h-[5px] rounded-full bg-line-2" aria-hidden="true" />
          <span className="w-10 h-10 rounded-xl bg-accent text-white flex items-center justify-center shrink-0 mt-1 sm:mt-0 shadow-md">
            <Stethoscope className="w-5 h-5" />
          </span>
          <div className="flex-1 min-w-0 mt-1 sm:mt-0">
            <h2 id="contribute-title" className="m-0 font-display font-bold text-[19px] tracking-[-0.02em] leading-tight">
              Soru ekle
            </h2>
            <p className="m-0 text-[13px] text-ink-3 truncate">Hatırladığın her küçük detay soruyu kurmaya yardım eder.</p>
          </div>
          <button
            type="button"
            onClick={onClose}
            disabled={isSubmitting}
            aria-label="Kapat"
            className="w-10 h-10 rounded-full flex items-center justify-center text-ink-2 hover:text-ink hover:bg-canvas cursor-pointer shrink-0"
          >
            <X className="w-5 h-5" />
          </button>
        </header>

        {saveSuccess ? (
          <div role="status" className="row-span-2 flex flex-col items-center justify-center gap-2 px-6 py-14 text-center">
            <SuccessCheck size={96} />
            <p className="m-0 font-display text-[22px] font-bold tracking-[-0.02em]">Havuza eklendi!</p>
            <p className="m-0 text-[15px] text-ink-2 max-w-[340px]">Teşekkürler. Benzer parçalar varsa aynı soruda birleştiriyoruz.</p>
          </div>
        ) : (
          <>
            <form id="contribute-form" onSubmit={handleSubmit} noValidate className="relative overflow-y-auto px-5 py-4 flex flex-col gap-5">
              {/* Which question */}
              <section className="flex flex-col gap-2">
                <span className={labelCls}>Hangi soru?</span>
                <div className="grid grid-cols-1 sm:grid-cols-[minmax(0,1fr)_minmax(0,1fr)] gap-2">
                  <label className="relative">
                    <span className="sr-only">Kurul</span>
                    <select value={committeeId} onChange={(e) => setCommitteeId(e.target.value)} className={`${fieldCls} h-12 pr-9 appearance-none cursor-pointer truncate`}>
                      {committees.map((c) => (
                        <option key={c.id} value={c.id}>
                          {c.name.replace(/^Dönem 3\s*-\s*/i, '')}
                        </option>
                      ))}
                    </select>
                    <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-3" />
                  </label>
                  <label className="relative">
                    <span className="sr-only">Ders</span>
                    <select value={discipline} onChange={(e) => setDiscipline(e.target.value)} className={`${fieldCls} h-12 pr-9 appearance-none cursor-pointer truncate`}>
                      {activeDisciplines.map((d) => (
                        <option key={d} value={d}>
                          {d}
                        </option>
                      ))}
                    </select>
                    <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-3" />
                  </label>
                </div>
                <div className="flex items-center gap-2">
                  <label className={`flex items-center gap-2 h-12 w-[132px] px-3.5 rounded-xl bg-field border border-transparent focus-within:border-accent focus-within:bg-white ${isUnknownNumber ? '' : ''}`}>
                    <span className="text-[13px] text-ink-3 shrink-0">Soru no</span>
                    <input
                      type="text"
                      inputMode="numeric"
                      value={isUnknownNumber ? '' : String(questionNumber || '')}
                      onChange={(e) => {
                        const v = e.target.value.replace(/[^0-9]/g, '').slice(0, 3);
                        setIsUnknownNumber(v === '');
                        setQuestionNumber(v === '' ? ('' as any) : Number(v));
                        if (formError) setFormError(null);
                      }}
                      placeholder="?"
                      aria-label="Soru numarası (bilmiyorsan boş bırak)"
                      className="w-full min-w-0 bg-transparent border-0 outline-0 text-[15px] font-mono placeholder:text-slate-600"
                    />
                  </label>
                  <span className="text-[13px] text-ink-3">{isUnknownNumber ? 'Bilmiyorsan boş bırak, biz yerleştiririz.' : `${selectedComm?.targetCount || 150} sorudan biri`}</span>
                </div>
              </section>

              {/* Stem */}
              <section className="flex flex-col gap-2">
                <div className="flex items-center justify-between gap-2">
                  <label htmlFor="contrib-stem" className={labelCls}>
                    Soru kökü / ipucu
                  </label>
                  <button
                    type="button"
                    onClick={handleQuickAiAssist}
                    disabled={aiAssisting || !fragmentText.trim()}
                    className="h-8 px-2.5 rounded-lg text-[13px] font-semibold text-accent bg-accent-soft inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
                  >
                    <Sparkles className={`w-3.5 h-3.5 ${aiAssisting ? 'animate-pulse' : ''}`} />
                    {aiAssisting ? 'AI düşünüyor…' : 'AI ile tamamla'}
                  </button>
                </div>
                <textarea
                  id="contrib-stem"
                  rows={4}
                  placeholder="Örn. 45 yaşında kadın, el bileklerinde sabah tutukluğu, RF ve anti-CCP pozitif. İlk basamak DMARD soruluyordu…"
                  value={fragmentText}
                  onChange={(e) => {
                    setFragmentText(e.target.value);
                    if (formError) setFormError(null);
                  }}
                  className={`${fieldCls} py-3 resize-none leading-[1.55] min-h-[112px]`}
                />
                <input
                  type="text"
                  placeholder="Konu (isteğe bağlı) · örn. Myastenia gravis, digoksin toksisitesi"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  aria-label="Konu"
                  className={`${fieldCls} h-11 text-[14px]`}
                />

                {/* Akıllı Kurul / Ders ve Konu Asistanı Bildirimi */}
                {smartAssistant && (smartAssistant.crossCommitteeWarning || smartAssistant.suggestedTopics.length > 0) && (
                  <div className="ms-pop-in rounded-xl bg-amber-500/10 border border-amber-300/80 p-3 flex flex-col gap-2">
                    {smartAssistant.crossCommitteeWarning && smartAssistant.predictedCommittee && (
                      <div className="flex items-start justify-between gap-2.5 flex-wrap sm:flex-nowrap">
                        <div className="flex items-start gap-2 text-[12.5px] text-amber-950 leading-snug">
                          <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                          <div>
                            <span className="font-bold">Kurul Önerisi: </span>
                            {smartAssistant.crossCommitteeWarning}
                          </div>
                        </div>
                        <button
                          type="button"
                          onClick={() => {
                            if (smartAssistant.predictedCommittee) {
                              setCommitteeId(smartAssistant.predictedCommittee.committeeId);
                              if (smartAssistant.predictedDiscipline) {
                                setDiscipline(smartAssistant.predictedDiscipline.discipline);
                              }
                              toast.success('Kurul Değiştirildi', `${smartAssistant.predictedCommittee.committeeName} kuruluna geçildi.`);
                            }
                          }}
                          className="shrink-0 h-7 px-2.5 rounded-lg bg-amber-600 hover:bg-amber-700 text-white text-[11.5px] font-bold inline-flex items-center gap-1 cursor-pointer transition-colors shadow-2xs"
                        >
                          Bu Kurula Geç
                          <ArrowRight className="w-3 h-3" />
                        </button>
                      </div>
                    )}

                    {smartAssistant.suggestedTopics.length > 0 && (
                      <div className="flex items-center gap-1.5 flex-wrap pt-0.5">
                        <span className="text-[11px] font-bold uppercase tracking-wider text-amber-900/80 flex items-center gap-1">
                          <Sparkles className="w-3 h-3 text-amber-600" />
                          Önerilen Konular:
                        </span>
                        {smartAssistant.suggestedTopics.slice(0, 3).map((st, i) => (
                          <button
                            key={i}
                            type="button"
                            onClick={() => setTopic(st.topic)}
                            className="h-6 px-2.5 rounded-full bg-white hover:bg-amber-50 text-amber-950 text-[11.5px] font-semibold border border-amber-200 shadow-2xs inline-flex items-center gap-1 cursor-pointer transition-colors"
                            title="Konu olarak seç"
                          >
                            {st.topic}
                          </button>
                        ))}
                        {smartAssistant.predictedDiscipline && discipline !== smartAssistant.predictedDiscipline.discipline && (
                          <button
                            type="button"
                            onClick={() => setDiscipline(smartAssistant.predictedDiscipline!.discipline)}
                            className="h-6 px-2 rounded-full bg-accent/15 hover:bg-accent/25 text-accent text-[11px] font-bold border border-accent/30 inline-flex items-center gap-1 cursor-pointer transition-colors"
                            title="Dersi eşle"
                          >
                            Dersi "{smartAssistant.predictedDiscipline.discipline}" yap
                          </button>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {realtimeMatch?.matchedQuestion && (
                  <div className="ms-pop-in rounded-xl bg-amber-50/90 border border-amber-300 p-3.5 flex flex-col gap-2.5">
                    <div className="flex items-center justify-between gap-2 flex-wrap">
                      <div className="flex items-center gap-1.5 flex-wrap">
                        <span className="h-6 px-2.5 rounded-full bg-amber-500/15 text-amber-900 text-[12px] font-semibold inline-flex items-center gap-1.5">
                          <Sparkles className="w-3.5 h-3.5 text-amber-800 shrink-0" />
                          Benzer bir taslak var · %{realtimeMatch.compatibility?.score} uyum
                        </span>
                        {realtimeMatch.contextHashtag && (
                          <ContextBadge hashtag={realtimeMatch.contextHashtag} colorIndex={0} />
                        )}
                      </div>
                      <span className="text-[12px] font-mono text-amber-800/80">
                        {realtimeMatch.matchedQuestion?.questionNumber ? `S.${realtimeMatch.matchedQuestion.questionNumber}` : 'Numarasız'}
                      </span>
                    </div>

                    <div className="text-[13px] leading-relaxed text-ink bg-white/90 rounded-xl p-2.5 border border-amber-200/60">
                      <Colored text={matchedStem} colors={sharedColors} />
                    </div>

                    <WordLegend texts={[fragmentText, matchedStem]} colors={sharedColors} />

                    {realtimeMatch.matchedQuestion?.questionNumber && (
                      <button
                        type="button"
                        onClick={() => {
                          const mq = realtimeMatch.matchedQuestion!;
                          setIsUnknownNumber(false);
                          setQuestionNumber(mq.questionNumber);
                          if (mq.discipline && mq.discipline !== 'Belirtilmedi') setDiscipline(mq.discipline);
                          if (mq.topic) setTopic(mq.topic);
                          toast.success('Soruya bağlandı', `Soru #${mq.questionNumber} ile eşleştirildi.`);
                        }}
                        className="self-start h-9 px-3.5 rounded-[10px] bg-amber-800 hover:bg-amber-900 text-white text-[13px] font-semibold cursor-pointer shadow-xs transition-colors"
                      >
                        Bu soruya bağla (S.{realtimeMatch.matchedQuestion.questionNumber})
                      </button>
                    )}
                  </div>
                )}

                {similarPast.length > 0 && (
                  <Collapsible bubble title="Benzer sorular" count={similarPast.length} className="ms-pop-in self-start w-full">
                  <div className="flex flex-col gap-1" aria-live="polite">
                    {similarPast.map((pq, i) => (
                      <details
                        key={pq.id}
                        className="ms-pop-in group rounded-[10px] border border-line bg-white open:bg-canvas transition-colors"
                        style={{ animationDelay: `${i * 60}ms` }}
                      >
                        <summary className="list-none cursor-pointer min-h-10 px-2.5 py-1.5 flex items-center gap-2 text-[13px]">
                          <span className="shrink-0 text-[11px] font-semibold px-1.5 py-0.5 rounded-md bg-violet-50 text-violet-700">
                            {pq.examYear || 'Çıkmış'}
                          </span>
                          <span className="min-w-0 flex-1 truncate text-ink-2 group-open:whitespace-normal" title={pq.stem}>
                            {pq.stem}
                          </span>
                          {pq.claimedAnswer && <span className="shrink-0 font-mono text-[12px] text-ok">{pq.claimedAnswer}</span>}
                        </summary>
                        {pq.discipline && <div className="px-2.5 pb-2 text-[12px] text-ink-3">{pq.discipline}</div>}
                      </details>
                    ))}
                  </div>
                  </Collapsible>
                )}

                {aiSuggestion?.suggestedStem && (
                  <div className="ms-pop-in rounded-xl bg-accent-soft/60 p-3 flex flex-col gap-1">
                    <span className="text-[12.5px] font-semibold text-accent inline-flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5" />
                      AI'nın önerdiği soru kalıbı
                    </span>
                    <p className="m-0 text-[14px] text-ink leading-[1.55]">{aiSuggestion.suggestedStem}</p>
                    {aiSuggestion.sources && aiSuggestion.sources.length > 0 && (
                      <span className="text-[12px] text-ink-3">
                        Kaynak: {aiSuggestion.sources.map((src) => src.title + (src.pageNumber ? ` (s.${src.pageNumber})` : '')).join(' · ')}
                      </span>
                    )}
                  </div>
                )}
              </section>

              {/* Options + answer */}
              <section className="flex flex-col gap-2">
                <span className={labelCls}>Şıklar</span>
                <OptionsEditor
                  options={options}
                  onChange={(k, v) => setOptions((p) => ({ ...p, [k]: v }))}
                  count={optionCount}
                  onCountChange={setOptionCount}
                  answer={(claimedAnswer || undefined) as OptionKey | undefined}
                  onAnswerChange={(k) => setClaimedAnswer(k || '')}
                  reason={answerReason}
                  onReasonChange={setAnswerReason}
                />
              </section>

              {/* Author */}
              <section className="flex flex-col gap-2">
                <label htmlFor="contrib-author" className={labelCls}>
                  Rumuz <span className="normal-case tracking-normal font-normal">· isteğe bağlı</span>
                </label>
                <input
                  id="contrib-author"
                  type="text"
                  placeholder="Örn. Tıbbiyeli3"
                  value={author}
                  onChange={(e) => handleAuthorChange(e.target.value)}
                  className={`${fieldCls} h-11`}
                />
              </section>

              {formError && (
                <div role="alert" className="flex items-start gap-2 px-3 py-2.5 rounded-xl bg-bad-soft text-bad-text text-[14px]">
                  <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-bad" />
                  <span>{formError}</span>
                </div>
              )}
            </form>

            <footer className="flex items-center gap-2 px-5 py-3 pb-[max(env(safe-area-inset-bottom),12px)] sm:pb-3 border-t border-line-soft bg-white">
              <button
                type="button"
                onClick={onClose}
                disabled={isSubmitting}
                className="h-12 sm:h-11 px-4 rounded-xl text-[15px] font-semibold text-ink-2 hover:bg-canvas cursor-pointer disabled:opacity-50"
              >
                Vazgeç
              </button>
              <button
                type="submit"
                form="contribute-form"
                disabled={isSubmitting}
                className="flex-1 sm:flex-none sm:ml-auto h-12 sm:h-11 px-6 rounded-xl bg-accent hover:bg-accent-hover text-white text-[15px] font-semibold inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60 shadow-md"
              >
                Havuza ekle
                <ArrowRight className="w-4 h-4" />
              </button>
            </footer>
          </>
        )}

        <BlurOverlay show={isSubmitting} label="Havuza ekleniyor…" hint="Benzer parçalar varsa aynı soruya bağlıyoruz" rounded="rounded-t-2xl sm:rounded-2xl" />
      </div>
    </div>
  );
};
