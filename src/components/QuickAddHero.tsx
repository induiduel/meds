import React, { useEffect, useMemo, useState } from 'react';
import { ArrowRight, CheckCircle2, ChevronRight, BookOpen, Check, CircleDashed, AlertCircle, ListChecks, Sparkles } from 'lucide-react';
import { Committee, QuestionItem } from '../types';
import { AppUser } from '../services/auth';
import { ApiService } from '../services/api';
import { getDefaultActiveCommitteeId, filterCurrent2026_2027Committees } from '../services/firestoreDb';

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

type Mode = 'stem' | 'option' | 'clue' | 'answer';
const MODES: { id: Mode; label: string }[] = [
  { id: 'stem', label: 'Soru kökü' },
  { id: 'option', label: 'Şık' },
  { id: 'clue', label: 'Klinik / lab ipucu' },
  { id: 'answer', label: 'Doğru cevap' },
];

const PLACEHOLDERS: Record<Mode, string> = {
  stem: "Örn. 24 saat göçük altında kalan hasta, nabız 56, TA 80/60… EKG'de sivri T vardı",
  option: '',
  clue: 'Örn. idrarda delta-ALA yüksekti, kemik iliğinde halkalı sideroblast…',
  answer: 'İstersen cevabın neden doğru olduğunu da yaz (opsiyonel)',
};

export const committeeShortLabel = (c: Committee) => {
  const m = c.name.match(/Kurul\s*(\d+)/i);
  if (m) return `KURUL ${m[1]}`;
  if (/bütünleme/i.test(c.name)) return 'BÜTÜNLEME';
  if (/final/i.test(c.name)) return 'FİNAL';
  return (c.code || c.name).toLocaleUpperCase('tr-TR');
};

const committeeOrder = (c: Committee) => {
  const m = c.name.match(/Kurul\s*(\d+)/i);
  if (m) return Number(m[1]);
  return /bütünleme/i.test(c.name) ? 101 : 100;
};

export const questionStemText = (q: QuestionItem) =>
  q.reconstruction?.stem || q.rawStem || q.fragments.find((f) => f.type === 'stem')?.text || q.fragments[0]?.text || q.topic;

const formatCount = (n: number) => n.toLocaleString('tr-TR');

/** Why a gathering question still needs help — shown in "Yardımına ihtiyaç var". */
const helpReason = (q: QuestionItem): string => {
  const have = new Set(q.options.map((o) => o.key));
  const missing = KEYS.filter((k) => !have.has(k));
  if (q.options.length === 0) return 'Sadece kök hatırlanıyor';
  if (missing.length > 0 && missing.length <= 3) {
    return missing.length === 1 ? `${missing[0]} şıkkı eksik` : `${missing.slice(0, -1).join(', ')} ve ${missing[missing.length - 1]} şıkları eksik`;
  }
  if (missing.length > 3) return `${missing.length} şık eksik`;
  if (!q.claimedAnswer) return 'Cevapta görüş ayrılığı';
  return 'Yeniden kurulmayı bekliyor';
};

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

export const QuickAddHero: React.FC<QuickAddHeroProps> = ({
  committee,
  committees,
  onSelectCommittee,
  onSubmitContribution,
  unassignedCount,
  questions = [],
  onOpenQuestion,
  onNavigateTab,
  isAdmin,
  currentUser,
  onOpenAdminPanel,
}) => {
  const disciplines =
    committee?.disciplines && committee.disciplines.length > 0
      ? committee.disciplines
      : ['Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'Tıbbi Biyokimya', 'Halk Sağlığı', 'İç Hastalıkları'];

  // ---- Composer state ----
  const [mode, setMode] = useState<Mode>('stem');
  const [text, setText] = useState('');
  const [options, setOptions] = useState<Record<OptionKey, string>>({ A: '', B: '', C: '', D: '', E: '' });
  const [claimedAnswer, setClaimedAnswer] = useState<OptionKey | undefined>(undefined);
  const [discipline, setDiscipline] = useState(disciplines[0]);
  const [questionNumber, setQuestionNumber] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    if (!disciplines.includes(discipline)) setDiscipline(disciplines[0]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [committee]);

  // ---- Archive + notes (instant local count, 0 network lag on homepage) ----
  const [archiveByCommittee, setArchiveByCommittee] = useState<Record<string, number>>(() => ({
    'donem3-kurul1': 796,
    'donem3-kurul2': 20,
    'donem3-kurul3': 3,
    'donem3-kurul4': 100,
    'donem3-kurul5': 119,
    'donem3-kurul6': 11,
    'donem3-final': 257,
    'donem3-butunleme': 4,
  }));
  const [notesCount, setNotesCount] = useState<number>(43);
  const [archive, setArchive] = useState<{ committeeId: string; discipline: string }[]>([]);

  useEffect(() => {
    let alive = true;
    // Fast non-blocking check from cached index without downloading full payload
    import('../data/driveCatalog').then((mod) => {
      if (alive && mod.DRIVE_SLIDES_CATALOG) {
        setNotesCount(mod.DRIVE_SLIDES_CATALOG.length);
      }
    }).catch(() => {});

    import('../services/pastQuestionsCache').then(async (mod) => {
      if (!alive) return;
      try {
        const cached = await mod.pastQuestionsCache.getCachedQuestions();
        if (cached && cached.length > 0 && alive) {
          setArchive(cached.map((q) => ({ committeeId: q.committeeId, discipline: q.discipline })));
          const m: Record<string, number> = {};
          cached.forEach((q) => {
            if (q.committeeId) m[q.committeeId] = (m[q.committeeId] || 0) + 1;
          });
          setArchiveByCommittee(prev => ({ ...prev, ...m }));
        }
      } catch (_) {}
    }).catch(() => {});

    return () => {
      alive = false;
    };
  }, []);

  const archiveByDiscipline = useMemo(() => {
    const m: Record<string, number> = {};
    archive.forEach((q) => q.discipline && (m[q.discipline] = (m[q.discipline] || 0) + 1));
    const rows = Object.entries(m).sort((a, b) => b[1] - a[1]).slice(0, 8);
    const max = rows[0]?.[1] || 1;
    return rows.map(([ad, n]) => ({ ad, n, w: Math.max(1.5, (n / max) * 100) }));
  }, [archive]);

  // ---- Pool stats for the selected committee ----
  const target = committee?.targetCount || 100;
  const completed = questions.filter((q) => q.status === 'completed').length;
  const drafts = questions.filter((q) => q.status !== 'completed' && (q.fragments.length > 0 || q.options.length > 0)).length;
  const empty = Math.max(0, target - completed - drafts);
  const pctNum = (n: number) => Math.min(100, (n / Math.max(target, 1)) * 100);
  const pct = (n: number) => `${pctNum(n)}%`;
  // Drafts can exceed the target (archive imports); never let the bar overflow
  const draftPct = `${Math.max(0, Math.min(pctNum(drafts), 100 - pctNum(completed)))}%`;

  const needsHelp = useMemo(
    () =>
      questions
        .filter((q) => q.status !== 'completed' && (q.fragments.length > 0 || q.options.length > 0))
        .sort((a, b) => b.fragments.length - a.fragments.length)
        .slice(0, 3),
    [questions]
  );

  const [recentFilter, setRecentFilter] = useState<'all' | 'done' | 'draft'>('all');
  const recent = useMemo(
    () =>
      questions
        .filter((q) => q.fragments.length > 0 || q.options.length > 0 || q.reconstruction)
        .filter((q) => (recentFilter === 'all' ? true : recentFilter === 'done' ? q.status === 'completed' : q.status !== 'completed'))
        .sort((a, b) => (b.updatedAt || '').localeCompare(a.updatedAt || ''))
        .slice(0, 6),
    [questions, recentFilter]
  );

  const activeCommitteeId = getDefaultActiveCommitteeId();
  const sortedCommittees = useMemo(() => filterCurrent2026_2027Committees(committees), [committees]);
  const isCollecting = committee?.id === activeCommitteeId;
  const shortName = committee ? committeeShortLabel(committee) : 'KURUL';
  const titleCaseShort = shortName.charAt(0) + shortName.slice(1).toLocaleLowerCase('tr-TR');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!committee) return;
    setFormError(null);

    const optionsList = KEYS.filter((k) => options[k].trim()).map((k) => ({ key: k, text: options[k].trim() }));
    if (!text.trim() && optionsList.length === 0 && !claimedAnswer) {
      setFormError('Sorudan aklında kalan en az bir kelime, şık ya da cevap yaz.');
      return;
    }

    const num = parseInt(questionNumber, 10);
    const hasNumber = Number.isFinite(num) && num >= 1 && num <= target;
    const prefix = mode === 'clue' && text.trim() ? 'İpucu: ' : '';
    const savedName = localStorage.getItem(SAVED_NAME_KEY) || '';

    setIsSubmitting(true);
    try {
      await onSubmitContribution({
        committeeId: committee.id,
        questionNumber: hasNumber ? num : undefined,
        isUnknownNumber: !hasNumber,
        discipline,
        topic: `${discipline} Hatırlanan Soru`,
        fragmentText: prefix + text.trim(),
        author: currentUser?.displayName || savedName || 'Dönem 3 Öğrencisi',
        authorUid: currentUser?.uid,
        authorStudentNumber: currentUser?.studentNumber || undefined,
        claimedAnswer,
        options: optionsList.length > 0 ? optionsList : undefined,
      });
      setText('');
      setOptions({ A: '', B: '', C: '', D: '', E: '' });
      setClaimedAnswer(undefined);
      setQuestionNumber('');
      setSuccessMessage(
        hasNumber
          ? `Soru ${num} için eklediğin parça havuza kaydedildi.`
          : 'Parçan havuza kaydedildi. Numarası bilinmeyen sorular benzerlerine göre yerleştirilir.'
      );
      setTimeout(() => setSuccessMessage(null), 7000);
    } catch (err: any) {
      setFormError('Kayıt sırasında bir hata oluştu: ' + (err?.message || 'bilinmeyen hata'));
    } finally {
      setIsSubmitting(false);
    }
  };

  const card = 'bg-white border border-line rounded-[18px]';

  return (
    <div className="flex flex-col gap-4 sm:gap-10">
      {/* Mobile committee pills */}
      <div role="tablist" aria-label="Kurul seç" className="sm:hidden flex gap-1.5 overflow-x-auto no-scrollbar -mx-3 px-3">
        {sortedCommittees.map((c) => {
          const sel = c.id === committee?.id;
          return (
            <button
              key={c.id}
              type="button"
              role="tab"
              aria-selected={sel}
              onClick={() => onSelectCommittee(c.id)}
              className={`shrink-0 h-8 px-3 rounded-full text-[13px] cursor-pointer ${
                sel ? 'bg-accent-soft text-accent font-semibold ring-1 ring-inset ring-accent/40' : 'bg-white border border-line text-ink'
              }`}
            >
              {committeeShortLabel(c).charAt(0) + committeeShortLabel(c).slice(1).toLocaleLowerCase('tr-TR')}
            </button>
          );
        })}
      </div>

      {/* ÖĞREN HUB'I ÇAĞRISI (Ses Transkriptleri & Slayt Sunuları) */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-950 via-indigo-950 to-slate-900 text-white p-4 sm:p-6 border border-indigo-900/60 shadow-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="space-y-1.5 max-w-2xl">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 text-[11px] font-bold tracking-wide uppercase border border-indigo-400/30">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            Yeni Bölüm • Ses & Slayt Eşleşmeli İnteraktif Öğrenme
          </div>
          <h2 className="text-base sm:text-xl font-black text-white tracking-tight">
            Hocanın Ses Kayıtları, Slayt Vurguları & Çıkmış Sorularla Öğren
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            Hocanın amfide <span className="text-amber-300 font-semibold">"Buradan soru sorarız"</span> ve <span className="text-amber-300 font-semibold">"Slaytta yok, beni dinleyin"</span> dediği noktaları tam ekran PPTX slayt sunumu veya dikey akışla incele; her slaytta eşleşen gerçek kurul çıkmış sorularını çöz.
          </p>
        </div>

        <button
          type="button"
          onClick={() => onNavigateTab('learn')}
          className="shrink-0 px-5 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs sm:text-sm flex items-center gap-2 shadow-lg shadow-indigo-600/30 transition-all hover:scale-[1.02] cursor-pointer"
        >
          <span>Öğrenmeye Başla</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>

      {/* HERO: composer + pool */}
      <section className="grid grid-cols-1 lg:grid-cols-[minmax(0,1.45fr)_minmax(0,1fr)] gap-3 sm:gap-6">
        <div className={`${card} p-4 sm:p-9 flex flex-col gap-3.5 sm:gap-6`}>
          <div className="flex flex-col gap-1.5 sm:gap-3">
            <div className={`flex items-center gap-2 text-[12px] sm:text-[13px] font-semibold ${isCollecting ? 'text-ok' : 'text-ink-2'}`}>
              <span className={`w-2 h-2 rounded-full ${isCollecting ? 'bg-ok-bright' : 'bg-line-2'}`} />
              {isCollecting ? `${titleCaseShort} için toplama açık` : `${titleCaseShort} arşivi`}
            </div>
            <h1 className="m-0 font-display font-bold text-[24px] sm:text-[44px] leading-[1.05] tracking-[-0.03em] text-ink">
              <span className="hidden sm:inline">Sınavdan yeni çıktın.<br /></span>Aklında ne kaldı?
            </h1>
            <p className="hidden sm:block m-0 text-ink-2 text-[16px] max-w-[520px]">
              Tek bir kelime bile işe yarar. Herkesin hatırladığı parçaları birleştirip soruyu baştan kuruyoruz.
            </p>
          </div>

          {successMessage && (
            <div role="status" className="flex items-start gap-3 p-4 rounded-xl bg-ok-soft text-ok text-[14px]">
              <CheckCircle2 className="w-5 h-5 shrink-0 mt-px" />
              <div>
                <p className="m-0 font-semibold">Teşekkürler!</p>
                <p className="m-0 text-ink">{successMessage}</p>
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="flex flex-col gap-3 sm:gap-3.5">
            <fieldset className="border-0 p-0 m-0 flex gap-1.5 sm:gap-2 flex-nowrap sm:flex-wrap overflow-x-auto no-scrollbar -mx-4 px-4 sm:mx-0 sm:px-0">
              <legend className="sr-only sm:not-sr-only text-[13px] font-semibold text-ink-2 mb-2">Ne ekliyorsun?</legend>
              {MODES.map((m) => {
                const on = mode === m.id;
                return (
                  <button
                    key={m.id}
                    type="button"
                    aria-pressed={on}
                    onClick={() => setMode(m.id)}
                    className={`shrink-0 whitespace-nowrap h-8 sm:h-9 px-3 sm:px-3.5 rounded-full text-[13px] sm:text-[14px] cursor-pointer transition-colors ${
                      on ? 'border-[1.5px] border-accent bg-accent-soft text-accent font-semibold' : 'border border-line bg-white text-ink hover:border-line-2'
                    }`}
                  >
                    {m.label}
                  </button>
                );
              })}
            </fieldset>

            {mode === 'option' ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {KEYS.map((k) => (
                  <label key={k} className="flex items-center gap-2.5 h-10 sm:h-11 pl-1.5 pr-3 border border-line-2 rounded-[10px] bg-field focus-within:border-accent">
                    <span className="w-8 h-8 rounded-lg bg-white border border-line flex items-center justify-center font-mono text-[13px] text-ink">{k}</span>
                    <input
                      type="text"
                      value={options[k]}
                      onChange={(e) => setOptions((p) => ({ ...p, [k]: e.target.value }))}
                      placeholder={`${k} şıkkı`}
                      aria-label={`${k} şıkkı`}
                      className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[15px] placeholder:text-[#6B7785]"
                    />
                  </label>
                ))}
              </div>
            ) : (
              <>
                {mode === 'answer' && (
                  <div className="flex items-center gap-2 flex-wrap" role="radiogroup" aria-label="Hatırlanan doğru cevap">
                    {KEYS.map((k) => (
                      <button
                        key={k}
                        type="button"
                        role="radio"
                        aria-checked={claimedAnswer === k}
                        onClick={() => setClaimedAnswer(claimedAnswer === k ? undefined : k)}
                        className={`w-11 h-11 rounded-[10px] font-mono text-[15px] cursor-pointer transition-colors ${
                          claimedAnswer === k ? 'bg-ok text-white' : 'bg-white border border-line-2 text-ink hover:border-ink-3'
                        }`}
                      >
                        {k}
                      </button>
                    ))}
                  </div>
                )}
                <label htmlFor="hatira" className="sr-only">
                  Hatırladığın kısım
                </label>
                <textarea
                  id="hatira"
                  rows={mode === 'answer' ? 2 : 4}
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder={PLACEHOLDERS[mode]}
                  className="resize-none h-[92px] sm:h-auto border border-line-2 rounded-xl px-3.5 sm:px-4 py-3 sm:py-3.5 text-[16px] leading-[1.5] text-ink bg-field outline-0 focus:border-accent placeholder:text-[#6B7785]"
                />
              </>
            )}

            <div className="flex flex-wrap sm:flex-nowrap gap-2 sm:gap-3 items-end">
              <label className="flex flex-col gap-1 sm:gap-1.5 text-[12px] sm:text-[13px] font-semibold text-ink-2 flex-1 min-w-[150px]">
                Ders
                <select
                  value={discipline}
                  onChange={(e) => setDiscipline(e.target.value)}
                  className="h-11 border border-line-2 rounded-[10px] px-3 text-[15px] font-normal text-ink bg-white cursor-pointer"
                >
                  {disciplines.map((d) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))}
                </select>
              </label>
              <label className="flex flex-col gap-1 sm:gap-1.5 text-[12px] sm:text-[13px] font-semibold text-ink-2 w-[112px]">
                Soru no
                <input
                  type="text"
                  inputMode="numeric"
                  value={questionNumber}
                  onChange={(e) => setQuestionNumber(e.target.value.replace(/[^0-9]/g, '').slice(0, 3))}
                  placeholder="Bilmiyorum"
                  className="h-11 border border-line-2 rounded-[10px] px-3 text-[15px] font-normal text-ink placeholder:text-[#6B7785]"
                />
              </label>
              <button
                type="submit"
                disabled={isSubmitting || !committee}
                className="h-11 px-[22px] rounded-[10px] bg-accent hover:bg-accent-hover text-white text-[15px] font-semibold flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60 w-full sm:w-auto"
              >
                {isSubmitting ? 'Kaydediliyor…' : 'Havuza ekle'}
                <ArrowRight className="w-4 h-4" strokeWidth={2.2} />
              </button>
            </div>
            {formError ? (
              <p role="alert" className="m-0 text-[13px] text-bad-text">{formError}</p>
            ) : (
              <p className="hidden sm:block m-0 text-[13px] text-ink-3">Benzer bir parça zaten varsa otomatik olarak o soruya bağlanır. İsim gerekmez.</p>
            )}
          </form>
        </div>

        <div className="flex flex-col gap-3 sm:gap-6">
          {/* Pool card */}
          <div className="bg-white border border-line rounded-[18px] p-4 sm:p-6 flex flex-col gap-2.5 sm:gap-4">
            <div className="flex justify-between items-baseline gap-3">
              <h2 className="m-0 text-[14px] sm:text-[15px] font-semibold">{titleCaseShort} havuzu</h2>
              <span className="font-mono text-[12px] text-ink-3">{committee?.examDate || ''}</span>
            </div>
            <div className="flex items-baseline gap-2.5">
              <span className="font-display text-[34px] sm:text-[52px] font-bold leading-none tracking-[-0.03em] text-ink">{completed}</span>
              <span className="text-[14px] sm:text-[15px] text-ink-2">/ {target} soru kuruldu</span>
            </div>
            <div
              role="img"
              aria-label={`Havuz durumu: ${completed} doğrulandı, ${drafts} taslak, ${empty} boş`}
              className="flex h-2 rounded-full overflow-hidden gap-[2px] bg-line-soft"
            >
              {completed > 0 && <span className="bg-ok-bright" style={{ width: pct(completed) }} />}
              {drafts > 0 && <span className="bg-[#F59E0B]" style={{ width: draftPct }} />}
            </div>
            <div className="grid grid-cols-3 gap-3 text-[12px] sm:text-[13px]">
              {[
                { label: 'Doğrulandı', n: completed, c: '#1F9D55' },
                { label: 'Taslak', n: drafts, c: '#F59E0B' },
                { label: 'Boş', n: empty, c: '#C9D2DB' },
              ].map((s) => (
                <div key={s.label} className="flex flex-col gap-0.5">
                  <span className="flex items-center gap-1.5 text-ink-2">
                    <span className="w-2 h-2 rounded-[2px]" style={{ background: s.c }} />
                    {s.label}
                  </span>
                  <span className="font-mono text-[15px] sm:text-[18px] text-ink">{s.n}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Needs help */}
          <div className={`${card} p-0 sm:p-6 flex flex-col gap-2 sm:gap-3.5 border-0 sm:border bg-transparent sm:bg-white`}>
            <div className="flex justify-between items-baseline">
              <h2 className="m-0 text-[16px] sm:text-[15px] font-semibold">Yardımına ihtiyaç var</h2>
              <button type="button" onClick={() => onNavigateTab('questions')} className="text-[13px] font-semibold text-accent cursor-pointer">
                Tümü
              </button>
            </div>
            {needsHelp.length === 0 ? (
              <p className="m-0 text-[14px] text-ink-2 bg-white sm:bg-canvas rounded-xl p-4">
                Şu an eksik parçası olan soru yok. İlk parçayı sen ekleyebilirsin.
              </p>
            ) : (
              needsHelp.map((q, i) => (
                <button
                  key={q.id}
                  type="button"
                  onClick={() => onOpenQuestion?.(q)}
                  className={`flex items-center gap-3 px-3 py-2.5 sm:p-3 rounded-xl text-left cursor-pointer border sm:border-0 ${
                    i === 0 ? 'bg-white sm:bg-warn-soft border-line' : 'bg-white sm:bg-[#F4F6F8] border-line'
                  }`}
                >
                  <span
                    className={`hidden sm:flex font-mono text-[13px] w-10 h-10 rounded-[10px] bg-white items-center justify-center shrink-0 ${
                      i === 0 ? 'text-warn' : 'text-ink-2'
                    }`}
                  >
                    {q.isUnassignedNumber ? '?' : `S.${q.questionNumber}`}
                  </span>
                  <span className={`sm:hidden w-2 h-9 rounded-full shrink-0 ${i === 0 ? 'bg-[#F59E0B]' : 'bg-[#AEB8C3]'}`} />
                  <span className="flex flex-col flex-1 min-w-0">
                    <span className="font-semibold text-[14px] text-ink">{helpReason(q)}</span>
                    <span className="text-[13px] text-ink-2 truncate">
                      {q.discipline} · {questionStemText(q)}
                    </span>
                  </span>
                  <ChevronRight className="w-4 h-4 text-ink-2 shrink-0" />
                </button>
              ))
            )}
          </div>
        </div>
      </section>

      {isAdmin && unassignedCount > 0 && (
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 rounded-xl bg-warn-soft px-4 py-3 text-[14px] text-ink">
          <span className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-warn shrink-0" />
            Bu kurulda numaraya yerleştirilmemiş <strong>{unassignedCount}</strong> soru var.
          </span>
          <button type="button" onClick={onOpenAdminPanel} className="h-10 px-4 rounded-[10px] bg-white border border-line-2 font-semibold cursor-pointer">
            İncele ve numara ata
          </button>
        </div>
      )}

      {/* Committees (2026-2027) */}
      <section aria-labelledby="kurullar" className="hidden sm:flex flex-col gap-4">
        <div className="flex justify-between items-baseline">
          <h2 id="kurullar" className="m-0 font-display text-[26px] font-bold tracking-[-0.02em]">
            2026-2027 Kurulları
          </h2>
          <span className="text-[13px] text-ink-3">Dönem 3 Kurul ve Sınav Programı</span>
        </div>
        <div className="grid grid-cols-[repeat(auto-fill,minmax(150px,1fr))] gap-3">
          {sortedCommittees.map((c) => {
            const sel = c.id === committee?.id;
            const isFinalish = /final|bütünleme/i.test(c.name);
            return (
              <button
                key={c.id}
                type="button"
                title={c.name}
                aria-pressed={sel}
                onClick={() => onSelectCommittee(c.id)}
                className={`bg-white rounded-[14px] p-4 flex flex-col gap-2 min-h-[110px] text-left cursor-pointer transition-colors ${
                  sel ? 'border-[1.5px] border-accent shadow-xs' : isFinalish ? 'border border-dashed border-line-2 hover:border-ink-3' : 'border border-line hover:border-line-2'
                }`}
              >
                <div className="flex justify-between items-center text-[12px] font-semibold">
                  <span className={sel ? 'text-accent' : 'text-ink-2'}>{committeeShortLabel(c)}</span>
                  {c.id === activeCommitteeId && (
                    <span className="bg-ok-soft text-ok text-[12px] font-semibold px-1.5 py-0.5 rounded">
                      AKTİF
                    </span>
                  )}
                </div>
                <div className="text-[12px] font-semibold text-ink line-clamp-2 mt-auto">
                  {c.name.replace(/Dönem 3\s*/i, '').trim()}
                </div>
                <div className="text-[12px] text-ink-3">
                  {c.examDate || '2026-2027'}
                </div>
              </button>
            );
          })}
        </div>
      </section>

      {/* Recent + archive breakdown */}
      <section className="grid grid-cols-1 lg:grid-cols-[minmax(0,1.6fr)_minmax(0,1fr)] gap-3 sm:gap-6 items-start">
        <div className={`${card} overflow-hidden`}>
          <div className="flex flex-wrap justify-between items-center gap-2 sm:gap-3 px-4 sm:px-6 py-3 sm:py-5 border-b border-line">
            <h2 className="m-0 font-display text-[18px] sm:text-[22px] font-bold tracking-[-0.02em]">Son hareketler</h2>
            <div role="group" aria-label="Filtre" className="flex gap-1 bg-canvas rounded-[10px] p-[3px]">
              {(
                [
                  ['all', 'Tümü'],
                  ['done', 'Doğrulanan'],
                  ['draft', 'Taslak'],
                ] as const
              ).map(([id, label]) => (
                <button
                  key={id}
                  type="button"
                  aria-pressed={recentFilter === id}
                  onClick={() => setRecentFilter(id)}
                  className={`h-8 px-3 rounded-lg text-[13px] cursor-pointer ${
                    recentFilter === id ? 'bg-white font-semibold shadow-[0_1px_2px_rgba(14,26,38,0.08)] text-ink' : 'text-ink-2'
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
          {recent.length === 0 ? (
            <p className="m-0 px-6 py-8 text-[14px] text-ink-2">Bu kurulda henüz hareket yok.</p>
          ) : (
            recent.map((q, i) => (
              <button
                key={q.id}
                type="button"
                onClick={() => onOpenQuestion?.(q)}
                className={`w-full ${i >= 4 ? "hidden sm:grid" : "grid"} grid-cols-[44px_minmax(0,1fr)] sm:grid-cols-[64px_minmax(0,1fr)_128px] gap-x-3 sm:gap-x-4 gap-y-1.5 items-center px-4 sm:px-6 py-3 sm:py-[18px] border-b border-line-soft text-left cursor-pointer hover:bg-[#FAFBFC]`}
              >
                <span className="font-mono text-[13px] text-ink-2">{q.isUnassignedNumber ? '—' : `S.${q.questionNumber}`}</span>
                <span className="flex flex-col gap-1 min-w-0">
                  <span className="text-[12px] font-semibold text-ink-2">
                    {q.discipline}
                    {q.examYear ? ` · ${q.examYear}` : ''}
                  </span>
                  <span className="text-[14px] sm:text-[15px] text-ink truncate">{questionStemText(q)}</span>
                </span>
                <span className="col-start-2 sm:col-start-auto sm:justify-self-end">
                  <StatusPill status={q.status} hasFragments={q.fragments.length > 0} />
                </span>
              </button>
            ))
          )}
          <button type="button" onClick={() => onNavigateTab('questions')} className="block w-full text-left px-4 sm:px-6 py-3 sm:py-4 text-[14px] font-semibold text-accent cursor-pointer">
            Soru havuzunun tamamı
          </button>
        </div>

        <div className="flex flex-col gap-3 sm:gap-6">
          <div className={`${card} p-4 sm:p-6 flex flex-col gap-3 sm:gap-4`}>
            <div className="flex flex-col gap-0.5">
              <h2 className="m-0 font-display text-[18px] sm:text-[22px] font-bold tracking-[-0.02em]">Derslere göre arşiv</h2>
              <span className="text-[13px] text-ink-3">Tüm kurullar, çıkmış sorular</span>
            </div>
            {archiveByDiscipline.length === 0 ? (
              <p className="m-0 text-[14px] text-ink-2">Arşiv yükleniyor…</p>
            ) : (
              archiveByDiscipline.map((d, i) => (
                <div key={d.ad} className={`${i >= 5 ? "hidden sm:flex" : "flex"} flex-col gap-1.5`}>
                  <div className="flex justify-between text-[14px]">
                    <span>{d.ad}</span>
                    <span className="font-mono text-ink-2">{formatCount(d.n)}</span>
                  </div>
                  <div className="h-1.5 bg-line-soft rounded-full">
                    <div className="h-1.5 rounded-full bg-accent" style={{ width: `${d.w}%` }} />
                  </div>
                </div>
              ))
            )}
            <button type="button" onClick={() => onNavigateTab('past_exams')} className="self-start text-[14px] font-semibold text-accent cursor-pointer">
              Çıkmış sorulara git
            </button>
          </div>

          <button
            type="button"
            onClick={() => onNavigateTab('study')}
            className="bg-ok-soft rounded-[18px] p-4 sm:p-6 flex gap-3 sm:gap-4 items-start text-left cursor-pointer hover:brightness-[0.98] border border-ok-tint transition-all"
          >
            <span className="w-10 h-10 sm:w-11 sm:h-11 shrink-0 rounded-xl bg-white flex items-center justify-center shadow-2xs">
              <ListChecks className="w-[22px] h-[22px] text-ok" />
            </span>
            <span className="flex flex-col gap-1">
              <span className="font-semibold text-[16px] text-ink">
                Test Çöz & Deneme Sınavı
              </span>
              <span className="text-[14px] text-ink-2">
                2.100+ çözümlü çıkmış soru, süreli optik formlu denemeler ve kişisel çalışma notları.
              </span>
            </span>
          </button>

          <button
            type="button"
            onClick={() => onNavigateTab('notes')}
            className="bg-accent-soft rounded-[18px] p-4 sm:p-6 flex gap-3 sm:gap-4 items-start text-left cursor-pointer hover:brightness-[0.98]"
          >
            <span className="w-10 h-10 sm:w-11 sm:h-11 shrink-0 rounded-xl bg-white flex items-center justify-center">
              <BookOpen className="w-[22px] h-[22px] text-accent" />
            </span>
            <span className="flex flex-col gap-1">
              <span className="font-semibold text-[16px] text-ink">
                {notesCount ? `${formatCount(notesCount)} ders notu ve slayt` : 'Ders notları ve slaytlar'}
              </span>
              <span className="text-[14px] text-ink-2">Her soru, ilgili slayt sayfasıyla eşleşiyor. Cevabın nereden geldiğini gör.</span>
            </span>
          </button>
        </div>
      </section>
    </div>
  );
};
