import React, { useEffect, useMemo, useState } from 'react';
import { X, ArrowLeft, ArrowRight, BookOpen, Sparkles, LayoutGrid, RotateCcw } from 'lucide-react';
import { QuestionItem } from '../types';
import { parseExplanation } from './QuestionCard';
import { QuestionAiChatDrawer } from './QuestionAiChatDrawer';

interface PracticeModeProps {
  questions: QuestionItem[];
  onOpenContributeModal: () => void;
  onExit?: () => void;
  onOpenQuestion?: (question: QuestionItem) => void;
  title?: string;
  subtitle?: string;
}

const formatElapsed = (s: number) => {
  const m = Math.floor(s / 60);
  const ss = String(s % 60).padStart(2, '0');
  return m >= 60 ? `${Math.floor(m / 60)}:${String(m % 60).padStart(2, '0')}:${ss}` : `${String(m).padStart(2, '0')}:${ss}`;
};

const isTyping = (t: EventTarget | null) => {
  const el = t as HTMLElement | null;
  return !!el && (['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName) || el.isContentEditable);
};

/**
 * /test — focused, full-screen test mode. One question at a time, a sticky bottom bar
 * (navigator · previous · next) like a phone app, keyboard shortcuts A–E and ← / →.
 */
export const PracticeMode: React.FC<PracticeModeProps> = ({
  questions,
  onOpenContributeModal,
  onExit,
  onOpenQuestion,
  title = 'Test çöz',
  subtitle,
}) => {
  // Only reconstructed questions can be practiced
  const items = useMemo(() => questions.filter((q) => q.status === 'completed' && q.reconstruction), [questions]);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  const [elapsed, setElapsed] = useState(0);
  const [aiChatOpen, setAiChatOpen] = useState(false);
  const [navOpen, setNavOpen] = useState(false);

  useEffect(() => {
    const t = setInterval(() => setElapsed((s) => s + 1), 1000);
    return () => clearInterval(t);
  }, []);

  const total = items.length;
  const currentQ = items[Math.min(currentIndex, Math.max(total - 1, 0))];
  const rec = currentQ?.reconstruction;
  const userAnswer = currentQ ? selectedAnswers[currentQ.id] : undefined;
  const isAnswered = !!userAnswer;
  const isCorrect = !!rec && userAnswer === rec.correctAnswer;

  const answeredCount = Object.keys(selectedAnswers).length;
  const correctCount = items.filter((q) => selectedAnswers[q.id] && selectedAnswers[q.id] === q.reconstruction?.correctAnswer).length;

  // Short feedback: the "why correct" section if the redactor wrote one, else the first section
  const shortExplanation = useMemo(() => {
    if (!rec?.explanation) return '';
    const secs = parseExplanation(rec.explanation, rec.correctAnswer);
    const why = secs.find((s) => s.label.startsWith('Neden')) || secs.find((s) => s.label === 'Mekanizma') || secs[0];
    return why?.body || '';
  }, [rec]);

  const handleSelect = (key: string) => {
    if (!currentQ || isAnswered) return;
    setSelectedAnswers((prev) => ({ ...prev, [currentQ.id]: key }));
  };

  const handleReset = () => {
    if (!currentQ) return;
    setSelectedAnswers((prev) => {
      const next = { ...prev };
      delete next[currentQ.id];
      return next;
    });
  };

  const go = (i: number) => {
    setCurrentIndex(Math.max(0, Math.min(total - 1, i)));
    setNavOpen(false);
    window.scrollTo({ top: 0 });
  };

  // Keyboard: A–E answer, ← / → move, Esc closes the navigator
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (isTyping(e.target) || aiChatOpen || e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === 'Escape' && navOpen) return setNavOpen(false);
      if (e.key === 'ArrowRight') return go(currentIndex + 1);
      if (e.key === 'ArrowLeft') return go(currentIndex - 1);
      const k = e.key.toUpperCase();
      if (rec && /^[A-E]$/.test(k) && rec.options.some((o) => o.key === k)) handleSelect(k);
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  });

  const exitButton = onExit && (
    <button
      type="button"
      onClick={onExit}
      aria-label="Testten çık"
      className="w-10 h-10 -ml-1 rounded-[10px] flex items-center justify-center shrink-0 cursor-pointer hover:bg-canvas"
    >
      <X className="w-5 h-5 text-ink" />
    </button>
  );

  if (!currentQ || !rec) {
    return (
      <div className="min-h-[100dvh] bg-white flex flex-col">
        <header className="border-b border-line">
          <div className="max-w-[1280px] mx-auto px-3 sm:px-8 h-14 flex items-center gap-3">
            {exitButton}
            <span className="font-semibold text-ink">{title}</span>
          </div>
        </header>
        <main className="flex-1 w-full max-w-[520px] mx-auto px-5 py-16 flex flex-col gap-4 text-center items-center">
          <h1 className="m-0 font-display text-[26px] font-bold tracking-[-0.02em]">Çözülecek soru henüz yok</h1>
          <p className="m-0 text-[15px] text-ink-2">
            Testte yalnızca yeniden kurulup doğrulanan sorular çıkar. Çıkmış sorularla pratik yapmak için Çalış sayfasını açabilir ya da bu kurula bir parça ekleyebilirsin.
          </p>
          <div className="flex flex-wrap gap-2 justify-center">
            {onExit && (
              <button type="button" onClick={onExit} className="h-11 px-5 rounded-xl bg-accent hover:bg-accent-hover text-white font-semibold cursor-pointer">
                Çalış'a dön
              </button>
            )}
            <button type="button" onClick={onOpenContributeModal} className="h-11 px-5 rounded-xl border border-line-2 text-ink font-semibold cursor-pointer">
              Parça ekle
            </button>
          </div>
        </main>
      </div>
    );
  }

  const position = currentIndex + 1;
  const pct = (position / total) * 100;

  return (
    <div className="min-h-[100dvh] bg-white text-ink flex flex-col">
      <header className="sticky top-0 bg-white/95 backdrop-blur z-20 border-b border-line">
        <div className="max-w-[1280px] mx-auto px-3 sm:px-8 h-14 flex items-center gap-2 sm:gap-4">
          {exitButton}
          <div className="flex flex-col leading-[1.25] min-w-0 flex-1 sm:flex-none sm:max-w-[320px]">
            <span className="font-semibold truncate text-[15px]">{title}</span>
            {subtitle && <span className="text-[12px] text-ink-3 truncate">{subtitle}</span>}
          </div>
          <div className="hidden sm:flex flex-1 items-center gap-3 max-w-[460px] mx-auto">
            <div className="flex-1 h-1.5 rounded-full bg-line-soft">
              <div className="h-1.5 rounded-full bg-accent transition-all" style={{ width: `${pct}%` }} />
            </div>
            <span className="font-mono text-[13px] text-ink-2 whitespace-nowrap">
              {position}/{total}
            </span>
          </div>
          <span className="shrink-0 font-mono text-[13px] px-2.5 h-8 inline-flex items-center rounded-[9px] bg-canvas text-ink-2" aria-label="Geçen süre">
            {formatElapsed(elapsed)}
          </span>
          <button
            type="button"
            onClick={() => setAiChatOpen(true)}
            className="h-9 px-2.5 sm:px-3 rounded-[10px] bg-accent-soft text-accent font-semibold text-[13px] inline-flex items-center gap-1.5 cursor-pointer shrink-0"
            title="Bu soruyu yapay zekâya sor"
          >
            <Sparkles className="w-4 h-4" />
            <span className="hidden sm:inline">AI'ya sor</span>
          </button>
        </div>
        <div className="sm:hidden h-[3px] bg-line-soft">
          <div className="h-[3px] bg-accent transition-all" style={{ width: `${pct}%` }} />
        </div>
      </header>

      <main className="flex-1 w-full max-w-[720px] mx-auto px-4 sm:px-8 pt-5 sm:pt-10 pb-32 flex flex-col gap-4 sm:gap-5">
        <div className="flex items-center justify-between gap-3 text-[13px] text-ink-3">
          <span>
            <span className="font-mono font-semibold text-ink">Soru {position}</span>
            {currentQ.discipline ? ` · ${currentQ.discipline}` : ''}
          </span>
          {answeredCount > 0 && (
            <span className="font-mono">
              <span className="text-ok font-semibold">{correctCount}</span>/{answeredCount} doğru
            </span>
          )}
        </div>
        <h1 className={`m-0 font-medium leading-[1.45] tracking-[-0.01em] ${rec.stem.length > 180 ? 'text-[17px] sm:text-[19px]' : 'text-[19px] sm:text-[23px]'}`}>{rec.stem}</h1>

        <div role="radiogroup" aria-label="Şıklar" className="flex flex-col gap-2">
          {rec.options.map((opt) => {
            const isThisCorrect = rec.correctAnswer === opt.key;
            const isPicked = userAnswer === opt.key;
            let box = 'border border-line bg-white hover:border-accent/60';
            let key = 'bg-canvas text-ink-2';
            let tag = '';
            let tagCls = 'text-ink-2';
            if (isAnswered && isThisCorrect) {
              box = 'border-[1.5px] border-ok-bright bg-ok-tint';
              key = 'bg-ok text-white';
              tag = 'Doğru';
              tagCls = 'text-ok';
            } else if (isAnswered && isPicked) {
              box = 'border-[1.5px] border-bad bg-bad-soft';
              key = 'bg-bad text-white';
              tag = 'Senin cevabın';
              tagCls = 'text-bad-text';
            } else if (isAnswered) {
              box = 'border border-line-soft bg-white opacity-60';
            }
            return (
              <button
                key={opt.key}
                type="button"
                role="radio"
                aria-checked={isPicked}
                onClick={() => handleSelect(opt.key)}
                className={`flex items-center gap-3 min-h-[52px] px-3 py-2.5 rounded-[14px] text-[15px] sm:text-[16px] leading-snug text-left transition-colors ${box} ${
                  isAnswered ? 'cursor-default' : 'cursor-pointer'
                }`}
              >
                <span className={`w-8 h-8 shrink-0 rounded-[9px] flex items-center justify-center font-mono text-[13px] font-semibold ${key}`}>{opt.key}</span>
                <span className="flex-1">{opt.text}</span>
                {tag && <span className={`text-[12px] font-semibold whitespace-nowrap ${tagCls}`}>{tag}</span>}
              </button>
            );
          })}
        </div>

        {isAnswered && (
          <section className={`rounded-[16px] px-4 py-4 flex flex-col gap-2 ${isCorrect ? 'bg-ok-soft' : 'bg-bad-soft'}`}>
            <span className={`font-semibold text-[15px] ${isCorrect ? 'text-ok' : 'text-bad-text'}`}>
              {isCorrect ? 'Doğru!' : `Doğru cevap ${rec.correctAnswer}`}
            </span>
            {shortExplanation && <p className="m-0 text-[15px] leading-[1.6] text-ink whitespace-pre-line line-clamp-6">{shortExplanation}</p>}
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1 pt-1">
              <button type="button" onClick={() => setAiChatOpen(true)} className="h-9 text-[14px] font-semibold text-accent inline-flex items-center gap-1.5 cursor-pointer">
                <Sparkles className="w-4 h-4" />
                {isCorrect ? 'Mekanizmayı sor' : 'Neden yanlış? Sor'}
              </button>
              {onOpenQuestion && (
                <button type="button" onClick={() => onOpenQuestion(currentQ)} className="h-9 text-[14px] font-semibold text-ink-2 hover:text-ink inline-flex items-center gap-1.5 cursor-pointer">
                  <BookOpen className="w-4 h-4" />
                  Tam açıklama
                </button>
              )}
              <button type="button" onClick={handleReset} className="h-9 text-[14px] font-semibold text-ink-2 hover:text-ink inline-flex items-center gap-1.5 cursor-pointer">
                <RotateCcw className="w-4 h-4" />
                Tekrar dene
              </button>
            </div>
          </section>
        )}

        <p className="hidden md:block m-0 text-[12.5px] text-ink-3">Kısayollar: A–E cevap · ← → soru değiştir</p>
      </main>

      {/* Sticky bottom bar: navigator · previous · next */}
      <div className="fixed bottom-0 left-0 right-0 z-20 bg-white/95 backdrop-blur border-t border-line pb-[max(env(safe-area-inset-bottom),10px)] pt-2.5">
        <div className="max-w-[720px] mx-auto px-4 sm:px-8 flex items-center gap-2">
          <button
            type="button"
            onClick={() => setNavOpen(true)}
            aria-haspopup="dialog"
            className="h-12 px-3 rounded-[14px] border border-line bg-white inline-flex items-center gap-2 font-mono text-[14px] text-ink cursor-pointer shrink-0"
          >
            <LayoutGrid className="w-[18px] h-[18px] text-ink-2" />
            {position}/{total}
          </button>
          <button
            type="button"
            onClick={() => go(currentIndex - 1)}
            disabled={currentIndex === 0}
            aria-label="Önceki soru"
            className="w-12 h-12 rounded-[14px] border border-line bg-white flex items-center justify-center cursor-pointer disabled:opacity-40 shrink-0"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <button
            type="button"
            onClick={() => go(currentIndex + 1)}
            disabled={currentIndex >= total - 1}
            className="flex-1 h-12 rounded-[14px] bg-accent hover:bg-accent-hover text-white font-semibold text-[16px] inline-flex items-center justify-center gap-2 cursor-pointer disabled:opacity-40"
          >
            {isAnswered ? 'Sonraki soru' : 'Atla'}
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Question navigator sheet */}
      {navOpen && (
        <div className="fixed inset-0 z-[60] flex items-end sm:items-center justify-center" role="dialog" aria-modal="true" aria-label="Soru gezgini">
          <button type="button" aria-label="Kapat" onClick={() => setNavOpen(false)} className="absolute inset-0 bg-[rgba(14,26,38,0.4)] cursor-default" />
          <div className="relative w-full sm:max-w-[560px] max-h-[80dvh] overflow-y-auto bg-white rounded-t-[24px] sm:rounded-[20px] px-4 sm:px-5 pt-2 sm:pt-5 pb-[max(env(safe-area-inset-bottom),20px)] sm:pb-5 flex flex-col gap-3">
            <span className="sm:hidden self-center w-10 h-[5px] rounded-full bg-line-2" aria-hidden="true" />
            <div className="flex items-center gap-3">
              <span className="flex-1 text-[18px] font-bold">Sorular</span>
              <span className="font-mono text-[13px] text-ink-2">
                <span className="text-ok font-semibold">{correctCount}</span> doğru · {answeredCount - correctCount} yanlış · {total - answeredCount} boş
              </span>
              <button type="button" onClick={() => setNavOpen(false)} aria-label="Kapat" className="w-9 h-9 -mr-1 rounded-full flex items-center justify-center text-ink-2 cursor-pointer hover:bg-canvas">
                <X className="w-5 h-5" />
              </button>
            </div>
            <nav aria-label="Soru gezgini" className="grid grid-cols-[repeat(auto-fill,minmax(44px,1fr))] gap-1.5">
              {items.map((q, i) => {
                const ans = selectedAnswers[q.id];
                const current = i === currentIndex;
                const right = ans && ans === q.reconstruction?.correctAnswer;
                const cls = current
                  ? 'bg-white text-accent ring-2 ring-inset ring-accent font-semibold'
                  : ans
                    ? right
                      ? 'bg-ok-soft text-ok'
                      : 'bg-bad-soft text-bad-text'
                    : 'bg-canvas text-ink-2';
                return (
                  <button
                    key={q.id}
                    type="button"
                    onClick={() => go(i)}
                    aria-current={current ? 'step' : undefined}
                    aria-label={`Soru ${i + 1}${ans ? (right ? ', doğru' : ', yanlış') : ''}`}
                    className={`h-11 rounded-[10px] flex items-center justify-center font-mono text-[13px] cursor-pointer ${cls}`}
                  >
                    {i + 1}
                  </button>
                );
              })}
            </nav>
          </div>
        </div>
      )}

      {/* AI Live Tutor Chat Drawer */}
      <QuestionAiChatDrawer
        isOpen={aiChatOpen}
        onClose={() => setAiChatOpen(false)}
        questionContext={
          currentQ && rec
            ? {
                id: currentQ.id,
                discipline: currentQ.discipline,
                topic: currentQ.topic,
                committeeId: currentQ.committeeId,
                number: currentQ.questionNumber,
                stem: rec.stem,
                options: rec.options.map((o) => ({ key: o.key, text: o.text })),
                correctAnswer: rec.correctAnswer,
                explanation: rec.explanation,
                userAnswer: userAnswer,
                lectureReference: currentQ.lectureReference,
                slideSnippet: currentQ.lectureReference?.matchedSnippet,
              }
            : null
        }
      />
    </div>
  );
};
