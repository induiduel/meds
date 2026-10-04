import React, { useEffect, useMemo, useState } from 'react';
import { ArrowRight, CheckCircle2, ChevronRight, ChevronDown, Check, CircleDashed, AlertCircle } from 'lucide-react';
import { Committee, QuestionItem } from '../types';
import { AppUser } from '../services/auth';
import { getDefaultActiveCommitteeId, filterCurrent2026_2027Committees } from '../services/firestoreDb';
import { pathFor, linkClick } from '../router';
import { OptionsEditor } from './ui/OptionsEditor';
import { BlurOverlay, SuccessCheck } from './ui/Animations';
import { toast } from './ui/Toast';
import { ApiService, SimilarPastQuestion } from '../services/api';

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

  // Yazarken benzer çıkmış sorular: 450 ms bekler, en az 12 karakter, en çok 3 sonuç
  useEffect(() => {
    const q = text.trim();
    if (mode === 'option' || q.length < 12) {
      setSimilar([]);
      return;
    }
    let alive = true;
    const t = window.setTimeout(() => {
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
    }, 450);
    return () => {
      alive = false;
      window.clearTimeout(t);
    };
  }, [text, mode, committee?.id]);
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

  useEffect(() => {
    if (!disciplines.includes(discipline)) setDiscipline(disciplines[0]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [committee]);

  // Pool stats for the selected committee
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

  return (
    <div className="w-full max-w-[640px] mx-auto flex flex-col gap-4 sm:gap-5 md:pt-6">
      {/* Title + committee */}
      <div className="flex flex-col items-start md:items-center gap-2.5 md:text-center">
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
        <h1 className="m-0 font-display font-bold text-[30px] md:text-[44px] leading-[1.05] tracking-[-0.03em] text-ink">Aklında ne kaldı?</h1>
        <p className="m-0 text-[15px] text-ink-2">Tek kelime bile işe yarar. Parçaları birleştirip soruyu birlikte kuruyoruz.</p>
      </div>

      {/* Composer */}
      <form
        onSubmit={handleSubmit}
        aria-busy={isSubmitting}
        className="relative bg-white border border-line rounded-[20px] p-3 sm:p-4 flex flex-col gap-3 shadow-[0_1px_2px_rgba(14,26,38,0.04)]"
      >
        <BlurOverlay show={isSubmitting} label="Havuza ekleniyor…" hint="Benzer parçalar varsa aynı soruya bağlıyoruz" />
        <div role="radiogroup" aria-label="Ne ekliyorsun?" className="grid grid-cols-3 gap-1 bg-canvas rounded-[12px] p-1">
          {MODES.map((m) => {
            const on = mode === m.id;
            return (
              <button
                key={m.id}
                type="button"
                role="radio"
                aria-checked={on}
                onClick={() => setMode(m.id)}
                className={`h-9 rounded-[9px] text-[13.5px] sm:text-[14px] whitespace-nowrap cursor-pointer transition-colors inline-flex items-center justify-center gap-1.5 ${
                  on ? 'bg-white text-ink font-semibold shadow-[0_1px_3px_rgba(14,26,38,0.12)]' : 'text-ink-2 hover:text-ink'
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
              className={`resize-none rounded-[14px] px-3.5 py-3 text-[16px] leading-[1.55] text-ink placeholder:text-[#7A8693] min-h-[132px] sm:min-h-[148px] ${field}`}
            />
          </>
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
              className={`appearance-none w-full h-11 rounded-[12px] pl-3 pr-8 text-[14px] text-ink cursor-pointer truncate ${field}`}
            >
              {disciplines.map((d) => (
                <option key={d} value={d}>
                  {d}
                </option>
              ))}
            </select>
            <ChevronDown className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-3" aria-hidden="true" />
          </label>
          <label className="flex items-center gap-1.5 h-11 w-[104px] px-3 rounded-[12px] bg-field border border-transparent focus-within:border-accent focus-within:bg-white">
            <span className="text-[13px] text-ink-3">No</span>
            <input
              type="text"
              inputMode="numeric"
              value={questionNumber}
              onChange={(e) => setQuestionNumber(e.target.value.replace(/[^0-9]/g, '').slice(0, 3))}
              placeholder="?"
              aria-label="Soru numarası (bilmiyorsan boş bırak)"
              className="w-full min-w-0 bg-transparent border-0 outline-0 text-[15px] font-mono placeholder:text-[#7A8693]"
            />
          </label>
          <button
            type="submit"
            disabled={isSubmitting}
            className={`h-12 sm:h-11 px-5 rounded-[12px] text-white text-[15px] font-semibold flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60 w-full sm:w-auto transition-colors ${
              canSubmit ? 'bg-accent hover:bg-accent-hover shadow-[0_6px_16px_rgba(30,79,216,0.25)]' : 'bg-accent/75'
            }`}
          >
            {isSubmitting ? 'Kaydediliyor…' : 'Havuza ekle'}
            <ArrowRight className="w-4 h-4" strokeWidth={2.2} />
          </button>
        </div>

        {formError && (
          <div role="alert" className="flex items-center gap-2 px-3 py-2.5 rounded-[12px] bg-bad-soft text-bad-text text-[14px]">
            <AlertCircle className="w-4 h-4 shrink-0 text-bad" />
            <span>{formError}</span>
          </div>
        )}
        {successMessage && (
          <div role="status" className="ms-pop-in flex items-center gap-3 px-3 py-2 rounded-[14px] bg-ok-tint border border-[#CDEBD8]">
            <SuccessCheck size={48} className="shrink-0 -my-1" />
            <span className="flex flex-col">
              <span className="text-[14.5px] font-semibold text-ok">Teşekkürler!</span>
              <span className="text-[13.5px] text-ink-2">{successMessage}</span>
            </span>
          </div>
        )}
      </form>

      {/* Pool progress: one quiet line */}
      <a
        href={pathFor('questions')}
        onClick={linkClick(() => onNavigateTab('questions'))}
        className="group bg-white border border-line rounded-[16px] px-4 py-3 flex items-center gap-3 hover:border-line-2"
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
            {drafts > 0 && <span className="bg-[#F59E0B]" style={{ width: `${draftPct}%` }} />}
          </span>
        </span>
        <span className="text-[13px] font-semibold text-accent inline-flex items-center gap-0.5 shrink-0">
          Havuz
          <ChevronRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
        </span>
      </a>
    </div>
  );
};
