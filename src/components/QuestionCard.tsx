import React, { useState } from 'react';
import {
  Plus,
  Check,
  CircleDashed,
  ChevronDown,
  ChevronUp,
  ChevronUp as Caret,
  RefreshCw,
  Sparkles,
  ExternalLink,
  History,
  Pencil,
  ThumbsUp,
  AlertTriangle,
} from 'lucide-react';
import { QuestionItem } from '../types';
import { AppUser } from '../services/auth';
import { StatusPill, questionStemText } from './QuickAddHero';

type OptionKey = 'A' | 'B' | 'C' | 'D' | 'E';
const KEYS: OptionKey[] = ['A', 'B', 'C', 'D', 'E'];

interface QuestionCardProps {
  question: QuestionItem;
  currentUser?: AppUser | null;
  isAdmin?: boolean;
  onEditQuestion?: (question: QuestionItem) => void;
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
          className="bg-amber-100 text-amber-950 font-bold px-1 py-0.5 rounded border border-amber-300 shadow-xs"
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

export const QuestionCard: React.FC<QuestionCardProps> = ({
  question,
  currentUser,
  isAdmin = false,
  onEditQuestion,
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
  // Phones: explanation + side column live behind one toggle to keep the list scannable
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [stemOpen, setStemOpen] = useState(false);
  const longStem = questionStemText(question).length > 180;
  const [showAddFragment, setShowAddFragment] = useState(false);
  const [showAddOption, setShowAddOption] = useState(false);

  const currentUserId =
    currentUser?.uid ||
    currentUser?.email ||
    (typeof localStorage !== 'undefined' ? localStorage.getItem('medsoru_device_token') || 'local_user' : 'local_user');
  const isQuestionLiked = !!question.likedBy?.includes(currentUserId);

  const isMyQuestion =
    !!currentUser &&
    (question.contributedByUid === currentUser.uid ||
      (currentUser.email && question.contributedByName === currentUser.displayName) ||
      question.fragments.some((f) => f.authorUid === currentUser.uid || (currentUser.displayName && f.author === currentUser.displayName)) ||
      question.options.some((o) => o.suggestedByUid === currentUser.uid || (currentUser.displayName && o.suggestedBy === currentUser.displayName)));

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
    setIsSubmittingFragment(true);
    try {
      await onAddFragment(question.id, fragmentText, fragmentAuthor || 'Anonim Tıbbiyeli', fragmentType);
      setFragmentText('');
      setShowAddFragment(false);
    } finally {
      setIsSubmittingFragment(false);
    }
  };

  const handleOptionSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!optionText.trim()) return;
    setIsSubmittingOption(true);
    try {
      await onAddOption(question.id, optionKey, optionText, optionAuthor || 'Anonim Tıbbiyeli');
      setOptionText('');
      setShowAddOption(false);
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
    'shrink-0 whitespace-nowrap h-10 sm:h-11 px-3.5 sm:px-[18px] rounded-[10px] border border-line-2 bg-white text-ink text-[14px] sm:text-[15px] font-semibold inline-flex items-center gap-2 cursor-pointer hover:border-ink-3 disabled:opacity-50';
  const mobileHidden = detailsOpen ? 'flex' : 'hidden sm:flex';
  const field = 'border border-line-2 rounded-[10px] bg-white px-3 text-[15px] text-ink outline-0 focus:border-accent placeholder:text-[#6B7785]';

  return (
    <article className="bg-white border border-line rounded-[18px] overflow-hidden">
      <div className={`grid grid-cols-1 ${isExpanded ? 'lg:grid-cols-[minmax(0,1.75fr)_minmax(0,1fr)]' : ''}`}>
        {/* ---------------- Main column ---------------- */}
        <div className="p-4 sm:p-9 flex flex-col gap-4 sm:gap-7 min-w-0">
          <div className="flex items-start gap-3">
            <div className="flex gap-2 flex-wrap flex-1 min-w-0">
              <StatusPill status={question.status} hasFragments={question.fragments.length > 0} />
              <span className="h-7 px-2.5 rounded-full bg-canvas text-ink-2 text-[12px] font-semibold inline-flex items-center font-mono">
                {question.isUnassignedNumber ? 'No ?' : `S.${question.questionNumber}`}
              </span>
              <span className="h-7 px-2.5 rounded-full bg-canvas text-ink-2 text-[12px] font-semibold inline-flex items-center">{question.discipline}</span>
              {question.topic && !/hatırlanan soru|çıkmış sorusu/i.test(question.topic) && (
                <span className="h-7 px-2.5 rounded-full bg-canvas text-ink-2 text-[12px] font-semibold hidden sm:inline-flex items-center max-w-[260px] truncate">
                  {question.topic}
                </span>
              )}
              {isMyQuestion && (
                <span className="h-7 px-2.5 rounded-full bg-accent-soft text-accent text-[12px] font-semibold inline-flex items-center">Senin katkın</span>
              )}
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

          <h3
            className={`m-0 font-display font-medium leading-[1.3] tracking-[-0.02em] text-ink ${
              longStem ? 'text-[17px] sm:text-[22px]' : 'text-[20px] sm:text-[30px]'
            } ${longStem && !stemOpen ? 'line-clamp-6 sm:line-clamp-none' : ''}`}
          >
            {questionStemText(question)}
          </h3>
          {longStem && (
            <button
              type="button"
              onClick={() => setStemOpen((v) => !v)}
              aria-expanded={stemOpen}
              className="sm:hidden -mt-2 self-start text-[14px] font-semibold text-accent cursor-pointer"
            >
              {stemOpen ? 'Kısalt' : 'Tamamını göster'}
            </button>
          )}

          {isExpanded && (
            <>
              {rows.length > 0 ? (
                <div className="flex flex-col gap-2.5">
                  <ol className="list-none m-0 p-0 flex flex-col gap-2.5">
                    {rows.map((o) => (
                      <li
                        key={o.key}
                        className={`grid grid-cols-[32px_minmax(0,1fr)_auto] sm:grid-cols-[40px_minmax(0,1fr)_180px] gap-x-3 sm:gap-x-4 items-center px-2.5 sm:px-4 py-2 sm:py-3 rounded-xl sm:rounded-[14px] ${
                          o.correct ? 'border-[1.5px] border-ok-bright bg-ok-tint' : o.ai ? 'border border-dashed border-line-2' : 'border border-line'
                        }`}
                      >
                        <span
                          className={`w-8 h-8 sm:w-9 sm:h-9 rounded-lg sm:rounded-[10px] flex items-center justify-center font-mono text-[13px] sm:text-[14px] ${
                            o.correct ? 'bg-ok text-white' : 'bg-canvas text-ink'
                          }`}
                        >
                          {o.key}
                        </span>
                        <span className="flex flex-col gap-0.5 min-w-0">
                          <span className="text-[15px] sm:text-[17px] leading-snug font-medium text-ink">{o.text}</span>
                          {o.ai && (
                            <span className="text-[12px] text-ink-2 inline-flex items-center gap-1">
                              <Sparkles className="w-3 h-3" />
                              <span className="sm:hidden">AI tamamladı</span>
                              <span className="hidden sm:inline">Kimse hatırlamadı, AI tamamladı</span>
                            </span>
                          )}
                          {o.correct && <span className="text-[12px] text-ok font-semibold">{correctLabel}</span>}
                        </span>
                        <span className="flex items-center gap-2.5">
                          <span className="hidden sm:block flex-1 h-1.5 rounded-full bg-line-soft">
                            <span
                              className="block h-1.5 rounded-full"
                              style={{ width: `${Math.max(2, (o.votes / maxVotes) * 100)}%`, background: o.correct ? '#1F9D55' : '#AEB8C3' }}
                            />
                          </span>
                          {o.hasStudent ? (
                            <button
                              type="button"
                              onClick={() => onUpvoteOption(question.id, o.key)}
                              aria-pressed={o.liked}
                              aria-label={`${o.key} şıkkını ben de böyle hatırlıyorum`}
                              className={`min-w-11 h-8 px-1.5 rounded-lg font-mono text-[12px] inline-flex items-center justify-end gap-1 cursor-pointer ${
                                o.liked ? 'text-accent font-semibold' : 'text-ink-2 hover:text-accent'
                              }`}
                            >
                              <Caret className="w-3 h-3" strokeWidth={2.6} />
                              {o.votes}
                            </button>
                          ) : (
                            <span className="min-w-11 text-right font-mono text-[12px] text-ink-2">0</span>
                          )}
                        </span>
                      </li>
                    ))}
                  </ol>
                  {anyVotes && <p className="m-0 text-[13px] text-ink-3">Çubuklar, öğrencilerin hangi şıkkı doğru hatırladığını gösterir.</p>}
                </div>
              ) : (
                <p className="m-0 text-[14px] text-ink-2 bg-canvas rounded-xl px-4 py-3">Henüz şık girilmedi. Hatırladığın bir şık varsa ekle.</p>
              )}

              {/* Inline forms */}
              {showAddFragment && (
                <form onSubmit={handleFragmentSubmit} className="flex flex-col gap-3 bg-canvas rounded-[14px] p-4">
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
                        className={`h-9 px-3.5 rounded-full text-[14px] cursor-pointer ${
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
                <form onSubmit={handleOptionSubmit} className="flex flex-col gap-3 bg-canvas rounded-[14px] p-4">
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
                      Şıkkı kaydet
                    </button>
                  </div>
                </form>
              )}

              {/* Actions */}
              <div className="flex gap-2 sm:gap-2.5 overflow-x-auto no-scrollbar -mx-4 px-4 sm:mx-0 sm:px-0 sm:flex-wrap border-t border-line-soft pt-4 sm:pt-5">
                <button
                  type="button"
                  onClick={() => {
                    setShowAddFragment((v) => !v);
                    setShowAddOption(false);
                  }}
                  className="shrink-0 whitespace-nowrap h-10 sm:h-11 px-3.5 sm:px-[18px] rounded-[10px] bg-accent hover:bg-accent-hover text-white text-[14px] sm:text-[15px] font-semibold inline-flex items-center gap-2 cursor-pointer"
                >
                  <Plus className="w-4 h-4" strokeWidth={2.2} />
                  Parça ekle
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowAddOption((v) => !v);
                    setShowAddFragment(false);
                  }}
                  className={btnSecondary}
                >
                  Şık ekle
                </button>
                {(isMyQuestion || isAdmin) && onEditQuestion && (
                  <button type="button" onClick={() => onEditQuestion(question)} className={btnSecondary}>
                    <Pencil className="w-4 h-4" />
                    Düzenle
                  </button>
                )}
                {revisionCount > 0 && onOpenHistory && (
                  <button type="button" onClick={() => onOpenHistory(question)} className={btnSecondary}>
                    <History className="w-4 h-4" />
                    Değişiklik geçmişi
                  </button>
                )}
                <button
                  type="button"
                  onClick={() => onReconstructWithAi(question.id)}
                  disabled={isReconstructing || (question.fragments.length === 0 && question.options.length === 0)}
                  className={btnSecondary}
                  title="Öğrencilerin hatırladığı parçaları birleştirip tam bir soru ve 5 şık üretir"
                >
                  {isReconstructing ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                  {isReconstructing ? 'Kuruluyor…' : hasReconstruction ? 'AI ile yeniden kur' : 'AI ile kur'}
                </button>
                {isAdmin && onOpenAiOptimizer && (
                  <button
                    type="button"
                    onClick={() => onOpenAiOptimizer(question)}
                    className="h-10 sm:h-11 px-3 sm:px-3.5 rounded-[10px] bg-gradient-to-r from-teal-50 to-cyan-50 hover:from-teal-100 hover:to-cyan-100 text-teal-800 border border-teal-300 font-semibold text-[13px] inline-flex items-center gap-1.5 transition-all cursor-pointer shadow-2xs"
                    title="Amfi ders notları ve tıp literatürüyle bu soruyu yapay zeka ile düzenle"
                  >
                    <Sparkles className="w-4 h-4 text-teal-600" />
                    <span>AI ile Düzenle</span>
                  </button>
                )}
                <span className="hidden sm:block flex-1" />
                {onUpvoteQuestion && (
                  <button
                    type="button"
                    onClick={() => onUpvoteQuestion(question.id)}
                    aria-pressed={isQuestionLiked}
                    aria-label="Soruyu beğen"
                    className={`shrink-0 h-10 sm:h-11 min-w-11 px-3 rounded-[10px] border inline-flex items-center justify-center gap-1.5 cursor-pointer font-mono text-[13px] ${
                      isQuestionLiked ? 'border-accent bg-accent-soft text-accent' : 'border-line-2 bg-white text-ink'
                    }`}
                  >
                    <ThumbsUp className={`w-4 h-4 ${isQuestionLiked ? 'fill-current' : ''}`} />
                    {question.upvotes || 0}
                  </button>
                )}
              </div>

              {/* Phone-only disclosure for explanation + details */}
              <button
                type="button"
                onClick={() => setDetailsOpen((v) => !v)}
                aria-expanded={detailsOpen}
                className="sm:hidden -mb-1 h-11 px-3 rounded-[10px] bg-canvas text-[14px] font-semibold text-ink flex items-center justify-between cursor-pointer"
              >
                <span>
                  {sections.length > 0 ? 'Açıklama ve ayrıntılar' : 'Ayrıntılar'}
                  <span className="font-normal text-ink-2"> · {question.fragments.length} parça</span>
                </span>
                {detailsOpen ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
              </button>

              {/* Explanation */}
              {sections.length > 0 && (
                <section aria-label="Açıklama" className={`${mobileHidden} flex-col gap-5 sm:gap-7 border-t border-line-soft pt-5 sm:pt-8`}>
                  <h4 className="hidden sm:block m-0 font-display text-[24px] font-bold tracking-[-0.02em]">Açıklama</h4>
                  {sections.map((s, i) => {
                    const distractors = s.label === 'Çeldiriciler' ? parseDistractors(s.body) : null;
                    if (sections.length === 1 && s.label === 'Açıklama') {
                      return (
                        <p key={i} className="m-0 text-[16px] leading-[1.65] whitespace-pre-line">
                          {s.body}
                        </p>
                      );
                    }
                    return (
                      <div key={i} className="grid grid-cols-1 sm:grid-cols-[160px_minmax(0,1fr)] gap-2 sm:gap-6 items-start">
                        <h5 className="m-0 text-[13px] font-semibold text-ink-2 uppercase tracking-[0.06em]">{s.label}</h5>
                        {distractors ? (
                          <dl className="m-0 grid grid-cols-[28px_minmax(0,1fr)] gap-x-2 gap-y-2.5 text-[15px] leading-[1.55]">
                            {distractors.map((d) => (
                              <React.Fragment key={d.key}>
                                <dt className="font-mono text-ink-2">{d.key}</dt>
                                <dd className="m-0">{d.text}</dd>
                              </React.Fragment>
                            ))}
                          </dl>
                        ) : (
                          <p className={`m-0 text-[16px] leading-[1.65] whitespace-pre-line ${s.pearl ? 'px-[18px] py-4 rounded-xl bg-accent-soft' : ''}`}>{s.body}</p>
                        )}
                      </div>
                    );
                  })}
                  {rec?.notesAndDiscrepancies && (
                    <div className="flex items-start gap-2.5 rounded-xl bg-warn-soft px-4 py-3 text-[14px] text-ink">
                      <AlertTriangle className="w-4 h-4 text-warn shrink-0 mt-0.5" />
                      <span>
                        <strong className="font-semibold">Hafıza notu: </strong>
                        {rec.notesAndDiscrepancies}
                      </span>
                    </div>
                  )}
                </section>
              )}
            </>
          )}
        </div>

        {/* ---------------- Side column ---------------- */}
        {isExpanded && (
          <aside className={`${mobileHidden} bg-[#FAFBFC] border-t lg:border-t-0 lg:border-l border-line p-3 sm:p-6 flex-col gap-3 sm:gap-5`}>
            <section className="bg-white border border-line rounded-[14px] sm:rounded-[18px] p-4 sm:p-6 flex flex-col gap-4">
              <h4 className="m-0 text-[15px] font-semibold">Yeniden kurulum</h4>
              <ul className="list-none m-0 p-0 flex flex-col gap-3 text-[14px]">
                {checklist.map((c) => (
                  <li key={c.label} className={`flex gap-2.5 items-center ${c.ok ? 'text-ink' : 'text-ink-2'}`}>
                    {c.ok ? <Check className="w-[18px] h-[18px] text-ok shrink-0" strokeWidth={2.6} /> : <CircleDashed className="w-[18px] h-[18px] text-ink-3 shrink-0" />}
                    {c.label}
                  </li>
                ))}
              </ul>
              <div className="pt-3 border-t border-line-soft flex flex-col gap-3">
                <div className="text-[13px] font-semibold text-ink-2">Öğrencilerin cevabı</div>
                <div className="flex gap-1.5" role="radiogroup" aria-label="Öğrencilerin belirlediği cevap">
                  {KEYS.map((k) => (
                    <button
                      key={k}
                      type="button"
                      role="radio"
                      aria-checked={question.claimedAnswer === k}
                      onClick={() => onSetClaimedAnswer(question.id, k)}
                      className={`flex-1 h-11 rounded-[10px] font-mono text-[14px] cursor-pointer ${
                        question.claimedAnswer === k ? 'bg-ink text-white' : 'bg-white border border-line-2 text-ink hover:border-ink-3'
                      }`}
                    >
                      {k}
                    </button>
                  ))}
                </div>
              </div>
              <p className="m-0 text-[13px] text-ink-2 pt-3 border-t border-line-soft">
                {lastUpdatedText && `Son güncelleme ${lastUpdatedText}`}
                {` · sürüm ${revisionCount + 1}`}
                {rec?.confidenceScore != null && ` · %${rec.confidenceScore} güven`}
              </p>
            </section>

            {question.lectureReference && (
              <section className="bg-white border border-line rounded-[14px] sm:rounded-[18px] p-4 sm:p-6 flex flex-col gap-3.5">
                <h4 className="m-0 text-[15px] font-semibold flex items-center justify-between">
                  <span>Kaynak slayt</span>
                  {question.lectureReference.confidenceScore ? (
                    <span className="text-[12px] font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full">
                      %{question.lectureReference.confidenceScore} eşleşme
                    </span>
                  ) : null}
                </h4>

                {question.lectureReference.matchedSnippet && (
                  <p className="m-0 rounded-[10px] bg-canvas border border-line px-3.5 py-3 text-[13px] leading-[1.65] text-ink-2">
                    {renderHighlightedSnippet(question.lectureReference.matchedSnippet)}
                  </p>
                )}

                {question.lectureReference.highlightedText && (
                  <div className="rounded-[10px] bg-amber-50/70 border border-amber-200 p-2.5 text-[12px] leading-relaxed text-amber-950">
                    <span className="font-bold block text-amber-900 mb-0.5">📌 Slayttaki İlgili Bilgi & Metin:</span>
                    {renderHighlightedSnippet(question.lectureReference.highlightedText)}
                  </div>
                )}

                <div className="flex flex-col gap-0.5">
                  <span className="font-semibold text-[15px]">{question.lectureReference.noteTitle}</span>
                  <span className="text-[14px] text-ink-2">
                    {question.lectureReference.discipline} · sayfa {question.lectureReference.pageNumber}
                  </span>
                </div>
                {question.lectureReference.driveFileUrl && (
                  <a
                    href={question.lectureReference.driveFileUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="h-11 rounded-[10px] border border-line-2 flex items-center justify-center gap-2 font-semibold text-[14px] text-ink hover:border-ink-3"
                  >
                    Slaytı aç
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </section>
            )}

            <section className="bg-white border border-line rounded-[14px] sm:rounded-[18px] p-4 sm:p-6 flex flex-col gap-4">
              <div className="flex justify-between items-baseline">
                <h4 className="m-0 text-[15px] font-semibold">Hafıza parçaları</h4>
                <span className="font-mono text-[12px] text-ink-2">{question.fragments.length}</span>
              </div>
              {question.fragments.length === 0 ? (
                <p className="m-0 text-[14px] text-ink-2">Henüz parça yok. İlk hatırlayan sen ol.</p>
              ) : (
                <ol className="list-none m-0 p-0 flex flex-col max-h-[420px] overflow-y-auto">
                  {question.fragments.map((frag, i) => {
                    const liked = !!frag.likedBy?.includes(currentUserId);
                    const last = i === question.fragments.length - 1;
                    return (
                      <li key={frag.id} className={`grid grid-cols-[14px_minmax(0,1fr)] gap-3 ${last ? '' : 'pb-4'}`}>
                        <span className="flex flex-col items-center gap-1">
                          <span className="w-2.5 h-2.5 rounded-full border-2 border-accent bg-white mt-[5px]" />
                          {!last && <span className="flex-1 w-0.5 bg-line-soft" />}
                        </span>
                        <span className="flex flex-col gap-1.5 min-w-0">
                          <span className="flex gap-2 items-center text-[12px] text-ink-2">
                            <span className="font-semibold text-ink">{fragmentTypeLabel(frag.type)}</span>· <span className="truncate">{frag.author}</span>
                          </span>
                          <span className="text-[14px] leading-[1.5] break-words">“{frag.text}”</span>
                          <button
                            type="button"
                            onClick={() => onUpvoteFragment(question.id, frag.id)}
                            aria-pressed={liked}
                            aria-label="Ben de böyle hatırlıyorum"
                            className={`self-start h-7 px-2.5 rounded-lg border text-[12px] inline-flex items-center gap-1.5 cursor-pointer ${
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
    </article>
  );
};
