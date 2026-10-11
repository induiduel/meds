import React, { useState, useMemo } from 'react';
import { CopyQuestionButton } from './ui/CopyQuestionButton';
import { getVoterId } from '../utils/voterId';
import { SourceText } from './ui/SourceText';
import {
  Plus,
  Check,
  CircleDashed,
  ChevronDown,
  ChevronUp,
  ChevronUp as Caret,
  RefreshCw,
  Flag,
  Brain,
  Sparkles,
  ExternalLink,
  History,
  Pencil,
  ThumbsUp,
  AlertTriangle,
  Wand2,
  Trash2,
  Layers,
  GraduationCap,
  ShieldCheck,
  CheckCircle2,
  Share2,
  AlertCircle,
  Send,
  X,
} from 'lucide-react';
import { ActionMenu } from './ui/ActionMenu';
import { QuestionItem } from '../types';
import { AppUser } from '../services/auth';
import { ErrorReportHistoryModal } from './ErrorReportHistoryModal';
import { shareDeepLink } from '../services/universalRedirectService';
import * as api from '../services/api';

const SOURCE_TYPE_LABELS: Record<string, string> = {
  past_question: 'Çıkmış soru',
  lecture_slide: 'Ders slaytı',
  summary: 'Ders özeti',
  transcript: 'Amfi kaydı',
};
import { StatusPill, questionStemText } from './QuickAddHero';
import { toast } from './ui/Toast';
import { validateNamePolicy } from '../utils/namePolicy';
import { useUiVersion } from '../utils/uiVersion';
import { disciplineClass, disciplineLabel } from '../utils/discipline';

type OptionKey = 'A' | 'B' | 'C' | 'D' | 'E';
const KEYS: OptionKey[] = ['A', 'B', 'C', 'D', 'E'];

interface QuestionCardProps {
  question: QuestionItem;
  currentUser?: AppUser | null;
  isAdmin?: boolean;
  onEditQuestion?: (question: QuestionItem) => void;
  onDeleteQuestion?: (question: QuestionItem) => void;
  onOpenHistory?: (question: QuestionItem) => void;
  onAddFragment: (questionId: string, text: string, author: string, type: 'stem' | 'clue' | 'option') => Promise<void>;
  onUpvoteFragment: (questionId: string, fragmentId: string) => Promise<void>;
  onAddOption: (questionId: string, key: OptionKey, text: string, suggestedBy: string) => Promise<void>;
  onUpvoteOption: (questionId: string, key: OptionKey) => Promise<void>;
  onUpvoteQuestion?: (questionId: string) => Promise<void>;
  onReconstructWithAi: (questionId: string) => Promise<void>;
  onOpenAiOptimizer?: (question: QuestionItem) => void;
  onSetClaimedAnswer: (questionId: string, answer: OptionKey) => Promise<void>;
  isReconstructing: boolean;
}

const SAVED_NAME_KEY = 'medsoru_saved_contributor_name';

/** Splits the redactor's 【Heading】: blocks into labelled sections. */
export const parseExplanation = (raw: string, correct?: string) => {
  const parts = raw.split(/【([^】]+)】\s*:?\s*/).map((s) => s.trim());
  if (parts.length < 3) return [{ label: 'Açıklama', body: raw.trim(), pearl: false }];
  const out: { label: string; body: string; pearl: boolean }[] = [];
  if (parts[0]) out.push({ label: 'Not', body: parts[0], pearl: false });
  for (let i = 1; i < parts.length; i += 2) {
    const h = parts[i];
    const body = parts[i + 1] || '';
    if (!body) continue;
    let label = h;
    let pearl = false;
    if (/mekanizma|patofizyoloji/i.test(h)) label = 'Mekanizma';
    else if (/doğru yanıt|gerekçe/i.test(h)) label = `Neden ${correct || 'bu cevap'}`;
    else if (/çeldirici/i.test(h)) label = 'Çeldiriciler';
    else if (/klinik ipucu|pearl|high-yield/i.test(h)) {
      label = 'Akılda tut';
      pearl = true;
    }
    out.push({ label, body, pearl });
  }
  return out;
};

/** Highlights text marked with ==...== using a styled <mark> element */
export const renderHighlightedSnippet = (snippet: string) => {
  if (!snippet) return null;
  const parts = snippet.split(/(==[^=]+==)/g);
  return parts.map((part, index) => {
    if (part.startsWith('==') && part.endsWith('==') && part.length > 4) {
      const text = part.slice(2, -2);
      return (
        <mark
          key={index}
          className="bg-warn-soft text-warn font-bold px-1 py-0.5 rounded border border-warn/30 shadow-xs"
        >
          {text}
        </mark>
      );
    }
    return <span key={index}>{part}</span>;
  });
};

/** "• A) Beyin: …" lines → definition list rows. */
const parseDistractors = (body: string) => {
  const rows = body
    .split(/\n|•/)
    .map((l) => l.trim())
    .filter(Boolean)
    .map((l) => l.match(/^([A-E])\)\s*(.*)$/))
    .filter(Boolean) as RegExpMatchArray[];
  return rows.length >= 2 ? rows.map((m) => ({ key: m[1], text: m[2] })) : null;
};

const fragmentTypeLabel = (t: string) => (t === 'stem' ? 'Soru kökü' : t === 'clue' ? 'İpucu' : t === 'answer' ? 'Doğru cevap' : 'Şık');

const QuestionCardComponent: React.FC<QuestionCardProps> = ({
  question,
  currentUser,
  isAdmin = false,
  onEditQuestion,
  onDeleteQuestion,
  onOpenHistory,
  onAddFragment,
  onUpvoteFragment,
  onAddOption,
  onUpvoteOption,
  onUpvoteQuestion,
  onReconstructWithAi,
  onOpenAiOptimizer,
  onSetClaimedAnswer,
  isReconstructing,
}) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const { isV7 } = useUiVersion();
  // Phones: explanation + side column live behind one toggle to keep the list scannable
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [flagsOpen, setFlagsOpen] = useState(false);
  const [stemOpen, setStemOpen] = useState(false);
  const longStem = questionStemText(question).length > 180;
  const [showAddFragment, setShowAddFragment] = useState(false);
  const [showAddOption, setShowAddOption] = useState(false);
  const [showReportHistoryModal, setShowReportHistoryModal] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [reportReason, setReportReason] = useState('Cevap anahtarı / Şık hatalı');
  const [reportDetails, setReportDetails] = useState('');
  const [reportSuggestedAnswer, setReportSuggestedAnswer] = useState('');
  const [isSubmittingReport, setIsSubmittingReport] = useState(false);

  const handleReportSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reportDetails.trim() && !reportSuggestedAnswer.trim()) {
      toast.error('Eksik Bilgi', 'Lütfen hatayı veya önerinizi kısaca açıklayın.');
      return;
    }
    setIsSubmittingReport(true);
    try {
      const detailsWithAnswer = reportSuggestedAnswer.trim()
        ? `${reportDetails.trim()}\n[Önerilen Doğru Şık/Cevap]: ${reportSuggestedAnswer.trim()}`
        : reportDetails.trim();

      await api.ApiService.reportPoolQuestion(
        question.id,
        reportReason,
        detailsWithAnswer,
        currentUser?.displayName || currentUser?.email || 'Anonim Öğrenci'
      );
      toast.success('Bildirim Alındı', 'Hata bildiriminiz yapay zeka ve moderatör inceleme sırasına eklendi.');
      setShowReportModal(false);
      setReportDetails('');
      setReportSuggestedAnswer('');
    } catch (err: any) {
      toast.error('Hata', err.message || 'Bildirim kaydedilemedi.');
    } finally {
      setIsSubmittingReport(false);
    }
  };

  const handleShareQuestion = async () => {
    await shareDeepLink({
      type: 'pool_question',
      id: question.id,
      committeeId: question.committeeId,
    });
  };

  const currentUserId = getVoterId(currentUser);
  const isQuestionLiked = !!question.likedBy?.includes(currentUserId);

  // Satellites and merged contributions
  const isMergedQuestion = Boolean(
    question.isMerged ||
    (question.mergedSatellites && question.mergedSatellites.length > 0) ||
    question.tags?.includes('taslak-birlestirildi')
  );
  const satelliteCount = question.mergedSatellites?.length || 0;

  // Derinlemesine kullanıcı katkı kontrolü (birleştirilmiş alt taslaklar dahil)
  const isMyQuestion =
    !!currentUser &&
    (question.contributedByUid === currentUser.uid ||
      (currentUser.email && question.contributedByName === currentUser.displayName) ||
      question.fragments.some((f) => f.authorUid === currentUser.uid || (currentUser.displayName && f.author === currentUser.displayName)) ||
      question.options.some((o) => o.suggestedByUid === currentUser.uid || (currentUser.displayName && o.suggestedBy === currentUser.displayName)) ||
      (question.mergedSatellites && question.mergedSatellites.some((sat) =>
        sat.contributedByUid === currentUser.uid ||
        (currentUser.displayName && sat.contributedByName === currentUser.displayName) ||
        sat.fragments?.some((f) => f.authorUid === currentUser.uid || (currentUser.displayName && f.author === currentUser.displayName)) ||
        sat.options?.some((o) => o.suggestedByUid === currentUser.uid || (currentUser.displayName && o.suggestedBy === currentUser.displayName))
      )));

  // Tüm parçaları topla: ana sorunun parçaları + birleştirilen uydu taslakların parçaları
  const allFragments = useMemo(() => {
    const list: (typeof question.fragments[0] & { isSatellite?: boolean; satelliteAuthor?: string })[] = [
      ...(question.fragments || [])
    ];
    if (question.mergedSatellites && question.mergedSatellites.length > 0) {
      const seenTexts = new Set(list.map((f) => f.text.trim().toLowerCase()));
      for (const sat of question.mergedSatellites) {
        const satAuthor = sat.contributedByName || sat.author || 'Taslak Katkısı';
        // 1. Uydu taslağın kökü
        const satStem = sat.reconstruction?.stem || sat.stem || sat.rawStem || '';
        if (satStem && !seenTexts.has(satStem.trim().toLowerCase())) {
          seenTexts.add(satStem.trim().toLowerCase());
          list.push({
            id: `sat-stem-${sat.id}`,
            text: satStem,
            author: satAuthor,
            authorUid: sat.contributedByUid,
            type: 'stem',
            timestamp: sat.updatedAt || sat.createdAt || new Date().toISOString(),
            upvotes: sat.upvotes || 0,
            isSatellite: true,
            satelliteAuthor: satAuthor,
          });
        }
        // 2. Uydu taslağın hafıza parçaları
        if (sat.fragments && sat.fragments.length > 0) {
          for (const sf of sat.fragments) {
            const cleanText = sf.text.trim().toLowerCase();
            if (!seenTexts.has(cleanText)) {
              seenTexts.add(cleanText);
              list.push({
                ...sf,
                isSatellite: true,
                satelliteAuthor: sf.author || satAuthor,
              });
            }
          }
        }
      }
    }
    return list;
  }, [question.fragments, question.mergedSatellites]);

  const revisionCount = question.revisions?.length || 0;

  const [fragmentText, setFragmentText] = useState('');
  const [fragmentAuthor, setFragmentAuthor] = useState(() => localStorage.getItem(SAVED_NAME_KEY) || '');
  const [fragmentType, setFragmentType] = useState<'stem' | 'clue' | 'option'>('clue');
  const [isSubmittingFragment, setIsSubmittingFragment] = useState(false);

  const [optionKey, setOptionKey] = useState<OptionKey>('A');
  const [optionText, setOptionText] = useState('');
  const [optionAuthor, setOptionAuthor] = useState(() => localStorage.getItem(SAVED_NAME_KEY) || '');
  const [isSubmittingOption, setIsSubmittingOption] = useState(false);

  const handleAuthorUpdate = (val: string) => {
    setFragmentAuthor(val);
    setOptionAuthor(val);
    localStorage.setItem(SAVED_NAME_KEY, val);
  };

  const rec = question.reconstruction;
  const hasReconstruction = !!rec;

  const handleFragmentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!fragmentText.trim()) return;
    if (fragmentAuthor.trim()) {
      const nameCheck = validateNamePolicy(fragmentAuthor.trim(), { adminEmail: currentUser?.email, isAdmin });
      if (!nameCheck.isValid) {
        toast.error('İsim Kuralı Hatası', nameCheck.errorMessage || 'Geçersiz yazar adı.');
        return;
      }
    }
    setIsSubmittingFragment(true);
    try {
      await onAddFragment(question.id, fragmentText.trim(), fragmentAuthor || 'Anonim Tıbbiyeli', fragmentType);
      setFragmentText('');
      setShowAddFragment(false);
    } catch (err) {
      console.error('Fragment submit error:', err);
    } finally {
      setIsSubmittingFragment(false);
    }
  };

  const handleOptionSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!optionText.trim()) return;
    if (optionAuthor.trim()) {
      const nameCheck = validateNamePolicy(optionAuthor.trim(), { adminEmail: currentUser?.email, isAdmin });
      if (!nameCheck.isValid) {
        toast.error('İsim Kuralı Hatası', nameCheck.errorMessage || 'Geçersiz yazar adı.');
        return;
      }
    }
    setIsSubmittingOption(true);
    try {
      await onAddOption(question.id, optionKey, optionText.trim(), optionAuthor || 'Anonim Tıbbiyeli');
      setOptionText('');
      setShowAddOption(false);
    } catch (err) {
      console.error('Option submit error:', err);
    } finally {
      setIsSubmittingOption(false);
    }
  };

  // ---- Options: reconstruction first, student options fill the rest ----
  const studentByKey = new Map(question.options.map((o) => [o.key, o]));
  const correctKey = rec?.correctAnswer || question.claimedAnswer;
  const correctLabel = rec ? 'Doğru cevap' : 'Öğrencilerin cevabı';
  const rows = KEYS.map((key) => {
    const recOpt = rec?.options.find((o) => o.key === key);
    const stu = studentByKey.get(key);
    const text = recOpt?.text || stu?.text;
    if (!text) return null;
    return {
      key,
      text,
      votes: stu?.upvotes || 0,
      liked: !!stu?.likedBy?.includes(currentUserId),
      hasStudent: !!stu,
      ai: !!recOpt?.isAiFilled || (!!rec && !stu),
      correct: correctKey === key,
    };
  }).filter(Boolean) as {
    key: OptionKey;
    text: string;
    votes: number;
    liked: boolean;
    hasStudent: boolean;
    ai: boolean;
    correct: boolean;
  }[];
  const maxVotes = Math.max(1, ...rows.map((r) => r.votes));
  const anyVotes = rows.some((r) => r.votes > 0);

  const sections = rec?.explanation ? parseExplanation(rec.explanation, rec.correctAnswer) : [];

  // ---- Reconstruction checklist ----
  const rememberedCount = rows.filter((r) => r.hasStudent).length;
  const aiCount = rows.filter((r) => r.ai).length;
  const checklist = [
    { ok: !!rec?.stem || question.fragments.some((f) => f.type === 'stem'), label: rec?.stem ? 'Soru kökü eksiksiz' : 'Soru kökü parçası var' },
    {
      ok: rows.length >= 5,
      label: rows.length === 0 ? 'Şık henüz yok' : aiCount > 0 ? `${rememberedCount} şık hatırlandı, ${aiCount} şık AI` : `${rememberedCount} şık hatırlandı`,
    },
    { ok: !!question.claimedAnswer && (!rec || question.claimedAnswer === rec.correctAnswer), label: question.claimedAnswer ? 'Cevapta öğrenci uzlaşısı' : 'Cevap belirlenmedi' },
    { ok: !!question.lectureReference, label: question.lectureReference ? 'Ders slaytıyla eşleşti' : 'Slayt eşleşmesi yok' },
  ];

  const lastUpdated = rec?.lastUpdated || question.updatedAt;
  const lastUpdatedText = lastUpdated ? new Date(lastUpdated).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }) : '';

  const btnSecondary =
    'shrink-0 whitespace-nowrap h-10 px-3.5 rounded-[10px] border border-line bg-white text-ink text-base font-semibold inline-flex items-center gap-2 cursor-pointer hover:border-line-2 disabled:opacity-50';
  const mobileHidden = detailsOpen ? 'flex' : 'hidden sm:flex';
  const field = 'border border-line-2 rounded-[10px] bg-white px-3 text-md text-ink outline-0 focus:border-accent placeholder:text-ink-2';

  return (
    <article
      id={`q-${question.id}`}
      data-question-id={question.id}
      className={isV7 ? `qc ${disciplineClass(question.discipline)}` : 'bg-white border border-line rounded-2xl overflow-hidden transition-all duration-300'}
    >
      <div className={`grid grid-cols-1 ${isExpanded ? 'lg:grid-cols-[minmax(0,1.75fr)_minmax(0,1fr)]' : ''}`}>
        {/* ---------------- Main column ---------------- */}
        <div className="p-4 sm:p-6 flex flex-col gap-4 sm:gap-5 min-w-0">
          {isV7 && (() => {
            const reps = question.reports || [];
            const solved = reps.filter((r) => r.status === 'resolved' || r.status === 'verified_correct').length;
            const flagNodes: React.ReactNode[] = [<StatusPill key="st" status={question.status} hasFragments={question.fragments.length > 0} />];
            if (isMyQuestion) flagNodes.push(<span key="me" className="cx-flag is-new">Senin katkın</span>);
            // Yalnız açık bildirim gösterilir; çözülmüş bildirim ve düzenleme tarihçesi ⋯ menüsünde.
            if (reps.length > solved) flagNodes.push(
              <button key="rep" type="button" onClick={() => setShowReportHistoryModal(true)} className="cx-flag is-warn" title="Bildirim ve çözüm geçmişi">
                <AlertTriangle aria-hidden />{reps.length - solved} bildirim
              </button>
            );
            if (isMergedQuestion) flagNodes.push(<span key="mg" className="cx-flag is-ok"><Layers aria-hidden />{satelliteCount > 0 ? `${satelliteCount + 1} taslak` : 'Birleşik'}</span>);
            const shown = flagsOpen ? flagNodes : flagNodes.slice(0, 2);
            return (
              <header className={`qk-h is-pool ${flagsOpen ? 'is-flags-open' : ''}`}>
                <span className="qk-chip" title={question.isUnassignedNumber ? 'Soru numarası bilinmiyor' : `Soru ${question.questionNumber}`}>{question.isUnassignedNumber ? '?' : `S${question.questionNumber}`}</span>
                <span className="qk-ders"><i className="hk-dot" aria-hidden />{disciplineLabel(question.discipline) || question.discipline || 'Tıp'}</span>
                {question.topic && !/hatırlanan soru|çıkmış sorusu/i.test(question.topic) && <span className="qk-kunye is-topic" title={question.topic}>{question.topic}</span>}
                <span className="qk-flags">{shown}</span>
                {flagNodes.length > shown.length && <button type="button" className="qk-more-flags" onClick={() => setFlagsOpen(true)}>+{flagNodes.length - shown.length}</button>}
                <span className="qk-sp" />
                <CopyQuestionButton
                  stem={question.reconstruction?.stem || question.fragments?.[0]?.text || question.topic}
                  options={(question.reconstruction?.options?.length ? question.reconstruction.options : question.options) as any[]}
                  className="qk-ib"
                />
                <button type="button" onClick={() => setShowReportModal(true)} className="qk-ib" aria-label="Hata bildir" title="Hata bildir"><Flag aria-hidden /></button>
                <button type="button" onClick={handleShareQuestion} className="qk-ib" aria-label="Soruyu paylaş" title="Soruyu paylaş"><Share2 aria-hidden /></button>
                <button type="button" onClick={() => setIsExpanded(!isExpanded)} aria-expanded={isExpanded} aria-label={isExpanded ? 'Soruyu daralt' : 'Soruyu genişlet'} className="qk-ib">
                  <ChevronDown className={`qk-chev ${isExpanded ? 'is-open' : ''}`} aria-hidden />
                </button>
              </header>
            );
          })()}
          {!isV7 && (
          <div className="flex items-start gap-3">
            <div className="flex gap-2 flex-wrap flex-1 min-w-0">
              <StatusPill status={question.status} hasFragments={question.fragments.length > 0} />
              <span className="h-7 px-2.5 rounded-full bg-canvas text-ink-2 text-xs font-semibold inline-flex items-center font-mono">
                {question.isUnassignedNumber ? 'No ?' : `S.${question.questionNumber}`}
              </span>
              <span className="h-7 px-2.5 rounded-full bg-canvas text-ink-2 text-xs font-semibold inline-flex items-center">{question.discipline}</span>
              {question.topic && !/hatırlanan soru|çıkmış sorusu/i.test(question.topic) && (
                <span className="h-7 px-2.5 rounded-full bg-canvas text-ink-2 text-xs font-semibold hidden sm:inline-flex items-center max-w-[260px] truncate">
                  {question.topic}
                </span>
              )}
              {question.notebooklm_verisi?.mufredat && (
                <span className="h-7 px-2.5 rounded-full bg-ai-soft text-ai text-xs font-semibold inline-flex items-center gap-1">
                  <GraduationCap className="w-3.5 h-3.5" />
                  {question.notebooklm_verisi.mufredat}
                </span>
              )}
              {isMyQuestion && (
                <span className="h-7 px-2.5 rounded-full bg-accent-soft text-accent text-xs font-semibold inline-flex items-center">Senin katkın</span>
              )}
              {isMergedQuestion && (
                <span className="h-7 px-2.5 rounded-full bg-ok-soft border border-ok/30 text-ok text-xs font-semibold inline-flex items-center gap-1">
                  <Layers className="w-3.5 h-3.5 text-ok" />
                  {satelliteCount > 0 ? `${satelliteCount + 1} taslak birleşik` : 'Birleşik taslak'}
                </span>
              )}
              <button
                type="button"
                onClick={handleShareQuestion}
                className="h-7 px-2.5 rounded-full bg-canvas hover:bg-accent-soft hover:text-accent text-ink-2 text-xs font-semibold inline-flex items-center gap-1 cursor-pointer transition-colors"
                title="Sorunun derin bağlantısını kopyala / paylaş"
                aria-label="Soruyu paylaş"
              >
                <Share2 className="w-3.5 h-3.5" />
                <span>Paylaş</span>
              </button>
              <button
                type="button"
                onClick={() => setShowReportModal(true)}
                className="h-7 px-2.5 rounded-full bg-canvas hover:bg-warn-soft hover:text-warn text-ink-2 text-xs font-semibold inline-flex items-center gap-1 cursor-pointer transition-colors"
                title="Hata bildirimi gönder"
                aria-label="Hata bildir"
              >
                <AlertCircle className="w-3.5 h-3.5" />
                <span>Hata Bildir</span>
              </button>
              {/* Hata Bildirimi & Çözüm Durumu Rozeti */}
              {(() => {
                const reportsList = question.reports || [];
                const resolvedReports = reportsList.filter((r) => r.status === 'resolved' || r.status === 'verified_correct');
                const hasReports = reportsList.length > 0;
                const isFullyResolved = hasReports && resolvedReports.length === reportsList.length;
                const hasRevisions = (question.revisions || []).length > 0;

                if (hasReports && isFullyResolved) {
                  return (
                    <button
                      type="button"
                      onClick={() => setShowReportHistoryModal(true)}
                      className="h-7 px-2.5 rounded-full bg-ok-soft text-ok text-xs font-semibold inline-flex items-center gap-1 cursor-pointer transition-colors"
                      title="Bu sorudaki hata bildirimleri incelendi ve çözüldü. Değişim geçmişini görmek için tıklayın."
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>✓ Çözüldü ({reportsList.length})</span>
                    </button>
                  );
                }
                if (hasReports && !isFullyResolved) {
                  return (
                    <button
                      type="button"
                      onClick={() => setShowReportHistoryModal(true)}
                      className="h-7 px-2.5 rounded-full bg-warn-soft text-warn text-xs font-semibold inline-flex items-center gap-1 cursor-pointer transition-colors"
                      title="Bu soruda hata bildirimi mevcut. Çözüm ve inceleme geçmişini görmek için tıklayın."
                    >
                      <AlertTriangle className="w-3.5 h-3.5" />
                      <span>{reportsList.length} Bildirim ({resolvedReports.length} Çözüldü)</span>
                    </button>
                  );
                }
                if (hasRevisions) {
                  return (
                    <button
                      type="button"
                      onClick={() => setShowReportHistoryModal(true)}
                      className="h-7 px-2.5 rounded-full bg-canvas text-ink-2 text-xs font-semibold inline-flex items-center gap-1 cursor-pointer transition-colors"
                      title="Soru düzenleme ve versiyon geçmişini gör"
                    >
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>Tarihçe ({(question.revisions || []).length})</span>
                    </button>
                  );
                }
                return null;
              })()}
            </div>
            <button
              type="button"
              onClick={() => setIsExpanded(!isExpanded)}
              aria-expanded={isExpanded}
              aria-label={isExpanded ? 'Soruyu daralt' : 'Soruyu genişlet'}
              className="w-10 h-10 -mt-1 -mr-1 rounded-[10px] border border-line flex items-center justify-center shrink-0 cursor-pointer hover:border-line-2"
            >
              {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>
          </div>

          )}

          <h3
            id={`stem-${question.id}`}
            className={isV7 ? `qk-stem is-pool ${longStem && !stemOpen ? 'is-clamped' : ''}` : `m-0 font-display font-medium leading-[1.3] tracking-[-0.02em] text-ink ${
              longStem ? 'text-lg sm:text-xl' : 'text-xl sm:text-2xl'
            } ${longStem && !stemOpen ? 'line-clamp-6 sm:line-clamp-none' : ''}`}
          >
            {questionStemText(question)}
          </h3>
          {longStem && (
            <button
              type="button"
              onClick={() => setStemOpen((v) => !v)}
              aria-expanded={stemOpen}
              className="sm:hidden -mt-2 self-start text-base font-semibold text-accent cursor-pointer"
            >
              {stemOpen ? 'Kısalt' : 'Tamamını göster'}
            </button>
          )}

          {(question.oncul_maddeleri || question.reconstruction?.oncul_maddeleri) && (
            <div className="flex flex-col gap-1.5 py-2.5 px-3.5 bg-canvas rounded-xl font-medium text-md sm:text-md text-ink border border-line my-1">
              {(question.oncul_maddeleri || question.reconstruction?.oncul_maddeleri)?.map((p, idx) => (
                <div key={idx} className="leading-snug">{p}</div>
              ))}
            </div>
          )}

          {question.notebooklm_verisi?.kazanim && (
            <div className="flex items-start gap-2.5 p-3 sm:p-3.5 bg-ai-soft rounded-xl text-sm text-ink my-1">
              <GraduationCap className="w-4.5 h-4.5 text-ai shrink-0 mt-0.5" />
              <div className="flex-1 min-w-0">
                <div className="text-2xs font-bold uppercase tracking-wider text-ai mb-0.5 flex flex-wrap items-center gap-1.5">
                  <span>Resmi Fakülte Müfredat Kazanımı</span>
                  {question.notebooklm_verisi.ders && (
                    <span className="font-normal text-ink-3">· {question.notebooklm_verisi.ders}</span>
                  )}
                  {question.notebooklm_verisi.konu && (
                    <span className="font-normal text-ink-3">· {question.notebooklm_verisi.konu}</span>
                  )}
                </div>
                <div className="font-medium leading-relaxed text-ink">{question.notebooklm_verisi.kazanim}</div>
              </div>
            </div>
          )}

          {isExpanded && (
            <>
              {rows.length > 0 ? (
                <div className="flex flex-col gap-2.5">
                  <ol className="qk-opts is-pool">
                    {rows.map((o) => (
                      <li key={o.key} id={`opt-${question.id}-${o.key}`} className="qk-opt-li">
                        <div className={`qk-opt ${o.correct ? 'is-correct' : ''} ${o.ai ? 'is-ai' : ''}`}>
                          <span className="qk-bub" aria-hidden>{o.correct ? <Check strokeWidth={3} /> : o.key}</span>
                          <span className="qk-opt-t">
                            {o.text}
                            {o.ai && <span className="qk-opt-sub"><Sparkles aria-hidden />Kimse hatırlamadı, yapay zekâ tamamladı</span>}
                            {o.correct && <span className="qk-opt-sub is-ok">{correctLabel}</span>}
                          </span>
                          <span className="qk-votebar" aria-hidden><i style={{ width: `${Math.max(2, (o.votes / maxVotes) * 100)}%` }} className={o.correct ? 'is-ok' : ''} /></span>
                        </div>
                        {o.hasStudent ? (
                          <button type="button" onClick={() => onUpvoteOption(question.id, o.key)} aria-pressed={o.liked} aria-label={o.liked ? `${o.key} şıkkına verdiğin oyu geri çek` : `${o.key} şıkkını ben de böyle hatırlıyorum`} className={`qk-vote ${o.liked ? 'is-on' : ''}`}>
                            <Caret aria-hidden strokeWidth={2.6} />{o.votes}
                          </button>
                        ) : (
                          <span className="qk-vote is-off" aria-label="Oy yok">0</span>
                        )}
                      </li>
                    ))}
                  </ol>
                </div>
              ) : (
                <p className="m-0 text-base text-ink-2 bg-canvas rounded-xl px-4 py-3">Henüz şık girilmedi. Hatırladığın bir şık varsa ekle.</p>
              )}

              {/* Alternatif Şıklar (Birleştirmelerde farklı hatırlanan varyasyonlar) */}
              {question.alternativeOptions && question.alternativeOptions.length > 0 && (
                <div className="ms-pop-in rounded-xl border border-ai/80 bg-ai-soft/40 p-3 sm:p-4 flex flex-col gap-2.5">
                  <div className="flex items-center justify-between gap-2">
                    <span className="flex items-center gap-1.5 text-xs font-bold text-ai uppercase tracking-wider">
                      <Layers className="w-3.5 h-3.5 text-ai" />
                      Alternatif Şıklar ({question.alternativeOptions.length})
                    </span>
                    <span className="text-xs text-ai">
                      Farklı hatırlanan şık varyasyonları
                    </span>
                  </div>
                  <ul className="list-none m-0 p-0 flex flex-col gap-2">
                    {question.alternativeOptions.map((alt, idx) => (
                      <li
                        key={alt.id || idx}
                        className="flex items-start justify-between gap-3 p-2.5 rounded-lg bg-white border border-ai/30 text-base text-ink"
                      >
                        <div className="flex flex-col gap-0.5 min-w-0">
                          <span className="font-medium text-ink-1 break-words">{alt.text}</span>
                          <span className="text-xs text-ink-3">
                            {[alt.suggestedBy && `Ekleyen: ${alt.suggestedBy}`, alt.reason].filter(Boolean).join(' · ')}
                          </span>
                        </div>
                        {typeof alt.upvotes === 'number' && alt.upvotes > 0 && (
                          <span className="shrink-0 text-xs font-mono font-semibold px-2 py-0.5 rounded-md bg-ai-soft/70 text-ai">
                            +{alt.upvotes}
                          </span>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Inline forms */}
              {showAddFragment && (
                <form onSubmit={handleFragmentSubmit} className="flex flex-col gap-3 bg-canvas rounded-xl p-4">
                  <div className="flex flex-wrap gap-2" role="radiogroup" aria-label="Parça türü">
                    {(
                      [
                        ['stem', 'Soru kökü'],
                        ['clue', 'Klinik / lab ipucu'],
                        ['option', 'Şık detayı'],
                      ] as const
                    ).map(([id, label]) => (
                      <button
                        key={id}
                        type="button"
                        role="radio"
                        aria-checked={fragmentType === id}
                        onClick={() => setFragmentType(id)}
                        className={`h-9 px-3.5 rounded-full text-base cursor-pointer ${
                          fragmentType === id ? 'border-[1.5px] border-accent bg-accent-soft text-accent font-semibold' : 'border border-line bg-white text-ink'
                        }`}
                      >
                        {label}
                      </button>
                    ))}
                  </div>
                  <label className="sr-only" htmlFor={`frag-${question.id}`}>
                    Hatırladığın parça
                  </label>
                  <textarea
                    id={`frag-${question.id}`}
                    rows={3}
                    required
                    value={fragmentText}
                    onChange={(e) => setFragmentText(e.target.value)}
                    placeholder="Örn. hastanın EKG'sinde ST elevasyonu ve troponin yüksekliği vardı…"
                    className={`${field} py-3 resize-none leading-[1.5]`}
                  />
                  <div className="flex flex-wrap items-center gap-2">
                    <input
                      type="text"
                      value={fragmentAuthor}
                      onChange={(e) => handleAuthorUpdate(e.target.value)}
                      placeholder="Rumuz (opsiyonel)"
                      aria-label="Rumuz"
                      className={`${field} h-11 flex-1 min-w-[160px]`}
                    />
                    <button type="button" onClick={() => setShowAddFragment(false)} className="h-11 px-4 rounded-[10px] text-ink-2 font-semibold cursor-pointer">
                      Vazgeç
                    </button>
                    <button type="submit" disabled={isSubmittingFragment} className="h-11 px-5 rounded-[10px] bg-accent hover:bg-accent-hover text-white font-semibold cursor-pointer disabled:opacity-60">
                      {isSubmittingFragment ? 'Kaydediliyor…' : 'Parçayı ekle'}
                    </button>
                  </div>
                </form>
              )}

              {showAddOption && (
                <form onSubmit={handleOptionSubmit} className="flex flex-col gap-3 bg-canvas rounded-xl p-4">
                  <div className="flex gap-2">
                    <label className="sr-only" htmlFor={`optkey-${question.id}`}>
                      Şık harfi
                    </label>
                    <select
                      id={`optkey-${question.id}`}
                      value={optionKey}
                      onChange={(e) => setOptionKey(e.target.value as OptionKey)}
                      className={`${field} h-11 w-20 font-mono cursor-pointer`}
                    >
                      {KEYS.map((k) => (
                        <option key={k} value={k}>
                          {k}
                        </option>
                      ))}
                    </select>
                    <input
                      type="text"
                      required
                      value={optionText}
                      onChange={(e) => setOptionText(e.target.value)}
                      placeholder="Şık metni"
                      aria-label="Şık metni"
                      className={`${field} h-11 flex-1 min-w-0`}
                    />
                  </div>
                  <div className="flex flex-wrap items-center gap-2">
                    <input
                      type="text"
                      value={optionAuthor}
                      onChange={(e) => handleAuthorUpdate(e.target.value)}
                      placeholder="Rumuz (opsiyonel)"
                      aria-label="Rumuz"
                      className={`${field} h-11 flex-1 min-w-[160px]`}
                    />
                    <button type="button" onClick={() => setShowAddOption(false)} className="h-11 px-4 rounded-[10px] text-ink-2 font-semibold cursor-pointer">
                      Vazgeç
                    </button>
                    <button type="submit" disabled={isSubmittingOption} className="h-11 px-5 rounded-[10px] bg-accent hover:bg-accent-hover text-white font-semibold cursor-pointer disabled:opacity-60">
                      {isSubmittingOption ? 'Kaydediliyor…' : 'Şıkkı kaydet'}
                    </button>
                  </div>
                </form>
              )}

              {/* Actions: two primary, the rest in one menu */}
              <div className="qk-f is-pool">
                {onUpvoteQuestion && (
                  <button
                    type="button"
                    onClick={() => onUpvoteQuestion(question.id)}
                    aria-pressed={isQuestionLiked}
                    aria-label="Soruyu beğen"
                    className={`qk-act ${isQuestionLiked ? 'is-on' : ''}`}
                  >
                    <ThumbsUp className={isQuestionLiked ? 'fill-current' : ''} aria-hidden />
                    {question.upvotes || 0}
                  </button>
                )}
                <span className="flex-1" />
                <button
                  type="button"
                  onClick={() => {
                    setShowAddOption((v) => !v);
                    setShowAddFragment(false);
                  }}
                  aria-pressed={showAddOption}
                  className={btnSecondary}
                >
                  Şık ekle
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowAddFragment((v) => !v);
                    setShowAddOption(false);
                  }}
                  aria-pressed={showAddFragment}
                  className="shrink-0 whitespace-nowrap h-10 px-3.5 sm:px-4 rounded-[10px] bg-accent hover:bg-accent-hover text-white text-base font-semibold inline-flex items-center gap-1.5 cursor-pointer"
                >
                  <Plus className="w-4 h-4" strokeWidth={2.2} />
                  Parça ekle
                </button>
                <ActionMenu
                  title={question.isUnassignedNumber ? 'Soru işlemleri' : `Soru ${question.questionNumber}`}
                  items={[
                    {
                      label: isReconstructing ? 'Kuruluyor…' : hasReconstruction ? 'AI ile yeniden kur' : 'AI ile kur',
                      icon: isReconstructing ? RefreshCw : Sparkles,
                      group: 'Yapay zekâ',
                      tone: 'accent',
                      disabled: isReconstructing || (question.fragments.length === 0 && question.options.length === 0),
                      onClick: () => onReconstructWithAi(question.id),
                    },
                    {
                      label: 'Soruyu Paylaş (Deep Link)',
                      icon: Share2,
                      group: 'Paylaşım',
                      onClick: handleShareQuestion,
                    },
                    {
                      label: 'Hata Bildir',
                      icon: AlertCircle,
                      group: 'Geri Bildirim',
                      onClick: () => setShowReportModal(true),
                    },
                    ...(isAdmin && onOpenAiOptimizer
                      ? [{ label: 'AI ile düzenle', icon: Wand2, group: 'Yapay zekâ', onClick: () => onOpenAiOptimizer(question) }]
                      : []),
                    ...((isMyQuestion || isAdmin) && onEditQuestion
                      ? [{ label: 'Düzenle', icon: Pencil, group: 'Soru', onClick: () => onEditQuestion(question) }]
                      : []),
                    ...((isMyQuestion || isAdmin || question.isUnassignedNumber) && onDeleteQuestion
                      ? [
                          {
                            label: question.isUnassignedNumber ? 'Taslağı Sil' : 'Soruyu Sil',
                            icon: Trash2,
                            group: 'Soru',
                            tone: 'danger' as const,
                            onClick: () => onDeleteQuestion(question),
                          },
                        ]
                      : []),
                    ...(revisionCount > 0 && onOpenHistory
                      ? [{ label: 'Değişiklik geçmişi', icon: History, group: 'Soru', hint: String(revisionCount), onClick: () => onOpenHistory(question) }]
                      : []),
                    ...((question.reports || []).length > 0
                      ? [{ label: 'Bildirim geçmişi', icon: AlertTriangle, group: 'Soru', hint: String((question.reports || []).length), onClick: () => setShowReportHistoryModal(true) }]
                      : []),
                  ]}
                />
              </div>

              {/* Phone-only disclosure for explanation + details */}
              <button
                type="button"
                onClick={() => setDetailsOpen((v) => !v)}
                aria-expanded={detailsOpen}
                className="qk-disc-h is-pool-disc"
              >
                <span>
                  {sections.length > 0 || Boolean(question.sik_analizi) ? 'Açıklama ve ayrıntılar' : 'Ayrıntılar'}
                  <span className="font-normal text-ink-2"> · {question.fragments.length} parça</span>
                </span>
                {detailsOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              </button>

              {/* Explanation */}
              {(sections.length > 0 || Boolean(question.sik_analizi)) && (
                <section id={`expl-${question.id}`} aria-label="Açıklama" className={`${detailsOpen ? 'flex' : 'hidden'} qk-pool-expl flex-col gap-5`}>
                  {sections.map((s, i) => {
                    const distractors = s.label === 'Çeldiriciler' ? parseDistractors(s.body) : null;
                    if (sections.length === 1 && s.label === 'Açıklama') {
                      return (
                        <SourceText key={i} text={s.body} className="text-md!" />
                      );
                    }
                    return (
                      <div key={i} className="grid grid-cols-1 sm:grid-cols-[160px_minmax(0,1fr)] gap-2 sm:gap-6 items-start">
                        <h5 className="m-0 text-sm font-semibold text-ink-2 uppercase tracking-[0.06em]">{s.label}</h5>
                        {distractors ? (
                          <dl className="m-0 grid grid-cols-[28px_minmax(0,1fr)] gap-x-2 gap-y-2.5 text-md leading-[1.55]">
                            {distractors.map((d) => (
                              <React.Fragment key={d.key}>
                                <dt className="font-mono text-ink-2">{d.key}</dt>
                                <dd className="m-0">{d.text}</dd>
                              </React.Fragment>
                            ))}
                          </dl>
                        ) : (
                          <div className={s.pearl ? 'px-[18px] py-4 rounded-xl bg-accent-soft' : ''}><SourceText text={s.body} className="text-md!" /></div>
                        )}
                      </div>
                    );
                  })}
                  {question.sik_analizi && (
                    <div className="grid grid-cols-1 sm:grid-cols-[160px_minmax(0,1fr)] gap-2 sm:gap-6 items-start">
                      <h5 className="m-0 text-sm font-semibold text-ink-2 uppercase tracking-[0.06em] flex items-center gap-1.5">
                        <ShieldCheck className="w-4 h-4 text-ok" />
                        Şık Analizi
                      </h5>
                      <div className="flex flex-col gap-2">
                        {typeof question.sik_analizi === 'object' && question.sik_analizi !== null ? (
                          Object.entries(question.sik_analizi).sort(([a], [b]) => a.localeCompare(b)).map(([k, val]) => {
                            const isCorrect = correctKey === k;
                            return (
                              <div
                                key={k}
                                className={`p-2.5 sm:p-3 rounded-xl border text-sm flex items-start gap-2.5 transition ${
                                  isCorrect
                                    ? 'bg-ok-soft/70 border-ok/40 text-ink shadow-2xs'
                                    : 'bg-canvas border-line text-ink-2'
                                }`}
                              >
                                <span
                                  className={`w-5 h-5 rounded-md flex items-center justify-center font-bold text-xs shrink-0 ${
                                    isCorrect ? 'bg-ok text-white' : 'bg-line-2 text-ink-2 font-mono'
                                  }`}
                                >
                                  {k}
                                </span>
                                <div className="flex-1 leading-relaxed">
                                  {String(val)}
                                </div>
                              </div>
                            );
                          })
                        ) : (
                          <div className="p-3 rounded-xl bg-canvas border border-line text-sm whitespace-pre-wrap text-ink-2 leading-relaxed">
                            {String(question.sik_analizi)}
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                  {rec?.notesAndDiscrepancies && (
                    <div className="flex items-start gap-2.5 rounded-xl bg-warn-soft px-4 py-3 text-base text-ink">
                      <AlertTriangle className="w-4 h-4 text-warn shrink-0 mt-0.5" />
                      <span>
                        <strong className="font-semibold">Hafıza notu: </strong>
                        {rec.notesAndDiscrepancies}
                      </span>
                    </div>
                  )}
                  {rec?.sources && rec.sources.length > 0 && (
                    <div className="flex flex-col gap-1.5 rounded-xl border border-line px-4 py-3 text-base">
                      <strong className="font-semibold text-ink">Dayandığı kaynaklar</strong>
                      {rec.sources.map((src, i) => (
                        <div key={`${src.documentId}-${i}`} className="text-ink-2">
                          <span className="font-medium">{SOURCE_TYPE_LABELS[src.documentType] || 'Kaynak'}:</span>{' '}
                          {src.title}
                          {src.pageNumber ? ` · s.${src.pageNumber}` : ''}
                        </div>
                      ))}
                    </div>
                  )}
                </section>
              )}
            </>
          )}
        </div>

        {/* ---------------- Side column ---------------- */}
        {isExpanded && (
          <aside className={`${mobileHidden} rb-qside bg-canvas border-t lg:border-t-0 lg:border-l border-line p-3 sm:p-4 flex-col gap-3`}>
            <section className="bg-white border border-line rounded-xl p-3 sm:p-4 flex flex-col gap-3">
              <h4 className="rb-qside-h"><span className="ic is-accent" aria-hidden><RefreshCw /></span>Yeniden kurulum<span className="n">{checklist.filter((c) => c.ok).length}/{checklist.length}</span></h4>
              <ul className="list-none m-0 p-0 flex flex-col gap-3 text-base">
                {checklist.map((c) => (
                  <li key={c.label} className={`flex gap-2.5 items-center ${c.ok ? 'text-ink' : 'text-ink-2'}`}>
                    {c.ok ? <Check className="w-[18px] h-[18px] text-ok shrink-0" strokeWidth={2.6} /> : <CircleDashed className="w-[18px] h-[18px] text-ink-3 shrink-0" />}
                    {c.label}
                  </li>
                ))}
              </ul>
              <div className="pt-3 border-t border-line-soft flex flex-col gap-3">
                <div className="text-sm font-semibold text-ink-2">Öğrencilerin cevabı</div>
                <div className="flex gap-1.5" role="radiogroup" aria-label="Öğrencilerin belirlediği cevap">
                  {KEYS.map((k) => (
                    <button
                      key={k}
                      type="button"
                      role="radio"
                      aria-checked={question.claimedAnswer === k}
                      onClick={() => onSetClaimedAnswer(question.id, k)}
                      className={`flex-1 h-11 rounded-[10px] font-mono text-base cursor-pointer ${
                        question.claimedAnswer === k ? 'bg-accent-soft text-accent font-semibold ring-1 ring-inset ring-accent/40' : 'bg-white border border-line-2 text-ink hover:border-ink-3'
                      }`}
                    >
                      {k}
                    </button>
                  ))}
                </div>
              </div>
              <p className="m-0 text-sm text-ink-2 pt-3 border-t border-line-soft">
                {lastUpdatedText && `Son güncelleme ${lastUpdatedText}`}
                {` · sürüm ${revisionCount + 1}`}
                {rec?.confidenceScore != null && ` · %${rec.confidenceScore} güven`}
              </p>
            </section>

            {question.lectureReference && (
              <section className="bg-white border border-line rounded-xl sm:rounded-2xl p-4 sm:p-6 flex flex-col gap-3.5">
                <h4 className="m-0 text-md font-semibold flex items-center justify-between">
                  <span>Kaynak slayt</span>
                  {question.lectureReference.confidenceScore ? (
                    <span className="text-xs font-medium text-ok bg-ok-soft border border-ok/30 px-2 py-0.5 rounded-full">
                      %{question.lectureReference.confidenceScore} eşleşme
                    </span>
                  ) : null}
                </h4>

                {question.lectureReference.matchedSnippet && (
                  <p className="m-0 rounded-[10px] bg-canvas border border-line px-3.5 py-3 text-sm leading-[1.65] text-ink-2">
                    {renderHighlightedSnippet(question.lectureReference.matchedSnippet)}
                  </p>
                )}

                {question.lectureReference.highlightedText && (
                  <div className="rounded-[10px] bg-warn-soft/70 border border-warn/30 p-2.5 text-xs leading-relaxed text-warn">
                    <span className="font-bold block text-warn mb-0.5">Slayttaki İlgili Bilgi & Metin:</span>
                    {renderHighlightedSnippet(question.lectureReference.highlightedText)}
                  </div>
                )}

                <div className="flex flex-col gap-0.5">
                  <span className="font-semibold text-md">{question.lectureReference.noteTitle}</span>
                  <span className="text-base text-ink-2">
                    {question.lectureReference.discipline} · sayfa {question.lectureReference.pageNumber}
                  </span>
                </div>
                {question.lectureReference.driveFileUrl && (
                  <a
                    href={question.lectureReference.driveFileUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="h-11 rounded-[10px] border border-line-2 flex items-center justify-center gap-2 font-semibold text-base text-ink hover:border-ink-3"
                  >
                    Slaytı aç
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </section>
            )}

            <section className="bg-white border border-line rounded-xl p-3 sm:p-4 flex flex-col gap-3">
              <h4 className="rb-qside-h"><span className="ic is-clinic" aria-hidden><Brain /></span>Hafıza parçaları ve katkılar<span className="n">{allFragments.length}</span></h4>
              {allFragments.length === 0 ? (
                <p className="m-0 text-base text-ink-2">Henüz parça yok. İlk hatırlayan sen ol.</p>
              ) : (
                <ol className="list-none m-0 p-0 flex flex-col max-h-[420px] overflow-y-auto">
                  {allFragments.map((frag, i) => {
                    const liked = !!frag.likedBy?.includes(currentUserId);
                    const last = i === allFragments.length - 1;
                    return (
                      <li key={frag.id} className={`grid grid-cols-[14px_minmax(0,1fr)] gap-3 ${last ? '' : 'pb-4'}`}>
                        <span className="flex flex-col items-center gap-1">
                          <span className={`w-2.5 h-2.5 rounded-full border-2 ${frag.isSatellite ? 'border-ok bg-ok-soft' : 'border-accent bg-white'} mt-[5px]`} />
                          {!last && <span className="flex-1 w-0.5 bg-line-soft" />}
                        </span>
                        <span className="flex flex-col gap-1.5 min-w-0">
                          <span className="flex gap-2 items-center text-xs text-ink-2 flex-wrap">
                            <span className="font-semibold text-ink">{fragmentTypeLabel(frag.type)}</span>· <span className="truncate">{frag.author}</span>
                            {frag.isSatellite && (
                              <span className="px-1.5 py-0.2 rounded bg-ok-soft/70 border border-ok/30 text-ok text-xs font-semibold">
                                Birleştirilen Taslak
                              </span>
                            )}
                          </span>
                          <span className="text-base leading-[1.5] break-words">“{frag.text}”</span>
                          <button
                            type="button"
                            onClick={() => onUpvoteFragment(question.id, frag.id)}
                            aria-pressed={liked}
                            aria-label="Ben de böyle hatırlıyorum"
                            className={`self-start h-7 px-2.5 rounded-lg border text-xs inline-flex items-center gap-1.5 cursor-pointer ${
                              liked ? 'border-accent bg-accent-soft text-accent font-semibold' : 'border-line bg-white text-ink-2 hover:text-accent'
                            }`}
                          >
                            <Caret className="w-3 h-3" strokeWidth={2.4} />
                            {frag.upvotes || 0}
                          </button>
                        </span>
                      </li>
                    );
                  })}
                </ol>
              )}
            </section>
          </aside>
        )}
      </div>

      {showReportHistoryModal && (
        <ErrorReportHistoryModal
          isOpen={showReportHistoryModal}
          onClose={() => setShowReportHistoryModal(false)}
          question={question}
        />
      )}

      {showReportModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-white dark:bg-[#12161f] border border-line rounded-2xl w-full max-w-lg shadow-xl overflow-hidden flex flex-col max-h-[90vh]">
            <div className="flex items-center justify-between px-6 py-4 border-b border-line bg-canvas">
              <div className="flex items-center gap-2">
                <AlertCircle className="w-5 h-5 text-warn" />
                <h3 className="font-semibold text-lg text-ink">Soru Hata Bildirimi</h3>
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
              <p className="text-sm text-ink-2">
                Bu soruda hatalı bir kök, yanlış şık, çelişkili cevap anahtarı veya eksik bilgi tespit ettiyseniz bildirin.
                Bildiriminiz yapay zeka denetim kuyruğuna alınacak ve otomatik düzeltilecektir.
              </p>
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-semibold text-ink-2 uppercase tracking-wider">Hata Türü</label>
                <select
                  value={reportReason}
                  onChange={(e) => setReportReason(e.target.value)}
                  className="w-full px-3 py-2 text-sm rounded-xl border border-line bg-canvas text-ink focus:border-accent outline-hidden"
                >
                  <option value="Cevap anahtarı / Şık hatalı">Cevap anahtarı / Şık hatalı</option>
                  <option value="Soru kökü veya öncüllerde hata var">Soru kökü veya öncüllerde hata var</option>
                  <option value="Yapay zeka analizinde hata var">Yapay zeka analizinde hata var</option>
                  <option value="Müfredat dışı / Yanlış komite">Müfredat dışı / Yanlış komite</option>
                  <option value="Diğer">Diğer</option>
                </select>
              </div>
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-semibold text-ink-2 uppercase tracking-wider">Açıklama / Tespit Edilen Hata *</label>
                <textarea
                  rows={3}
                  value={reportDetails}
                  onChange={(e) => setReportDetails(e.target.value)}
                  placeholder="Örn: Doğru cevap C değil D olmalıdır çünkü..."
                  required
                  className="w-full px-3 py-2 text-sm rounded-xl border border-line bg-canvas text-ink focus:border-accent outline-hidden resize-none"
                />
              </div>
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-semibold text-ink-2 uppercase tracking-wider">Önerilen Doğru Çözüm / Şık (İsteğe Bağlı)</label>
                <input
                  type="text"
                  value={reportSuggestedAnswer}
                  onChange={(e) => setReportSuggestedAnswer(e.target.value)}
                  placeholder="Örn: Doğru şık D: Lizozomal depo hastalığı"
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
    </article>
  );
};

export const QuestionCard = React.memo(QuestionCardComponent);
