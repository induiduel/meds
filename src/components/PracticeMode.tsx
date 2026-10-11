import React, { useEffect, useMemo, useState } from 'react';
import { X, ArrowLeft, ArrowRight, BookOpen, Sparkles, LayoutGrid, RotateCcw } from 'lucide-react';
import { QuestionItem } from '../types';
import { parseExplanation } from './QuestionCard';
import { QuestionAiChatDrawer } from './QuestionAiChatDrawer';
import { Sheet } from './ui/Sheet';

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
      if (rec && /^[A-E]$/.test(k) && rec.options.some((o, i) => (o.key || 'ABCDE'[i]) === k)) handleSelect(k);
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
          <h1 className="m-0 font-display text-3xl font-bold tracking-[-0.02em]">Çözülecek soru henüz yok</h1>
          <p className="m-0 text-md text-ink-2">
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
    <div className="tm min-h-[100dvh] text-ink flex flex-col">
      <header className="tm-head sticky top-0 z-20">
        <div className="max-w-[1280px] mx-auto px-3 sm:px-8 h-14 flex items-center gap-2 sm:gap-4">
          {exitButton}
          <div className="flex flex-col leading-[1.25] min-w-0 flex-1 sm:flex-none sm:max-w-[320px]">
            <span className="font-semibold truncate text-md">{title}</span>
            {subtitle && <span className="text-xs text-ink-3 truncate">{subtitle}</span>}
          </div>
          <span className="flex-1 hidden sm:block" />
          <span className="tm-count hk-num" aria-label={`Soru ${position} / ${total}`}>{position}<small>/{total}</small></span>
          <span className="shrink-0 font-mono text-sm px-2.5 h-8 inline-flex items-center rounded-lg bg-canvas text-ink-2" aria-label="Geçen süre">
            {formatElapsed(elapsed)}
          </span>
          <button
            type="button"
            onClick={() => setAiChatOpen(true)}
            className="h-9 px-2.5 sm:px-3 rounded-[10px] bg-accent-soft text-accent font-semibold text-sm inline-flex items-center gap-1.5 cursor-pointer shrink-0"
            title="Bu soruyu yapay zekâya sor"
          >
            <Sparkles className="w-4 h-4" />
            <span className="hidden sm:inline">AI'ya sor</span>
          </button>
        </div>
        {/* Çentikli ilerleme: her soru bir çentik — doğru, yanlış, boş, şu anki */}
        <div className="tm-track" role="progressbar" aria-valuemin={1} aria-valuemax={total} aria-valuenow={position} aria-label="İlerleme">
          {total <= 80 ? (
            items.map((q, i) => {
              const ans = selectedAnswers[q.id];
              const st = i === currentIndex ? 'is-now' : ans ? (ans === q.reconstruction?.correctAnswer ? 'is-ok' : 'is-bad') : '';
              return <i key={q.id} className={st} />;
            })
          ) : (
            <b style={{ width: `${pct}%` }} />
          )}
        </div>
      </header>

      <main className="flex-1 w-full max-w-[960px] mx-auto px-4 sm:px-8 pt-5 sm:pt-10 pb-32 flex flex-col gap-4 sm:gap-5">
        <div className="flex items-center justify-between gap-3 text-sm text-ink-3">
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
        <h1 className={`m-0 font-medium leading-[1.45] tracking-[-0.01em] ${rec.stem.length > 180 ? 'text-lg sm:text-xl' : 'text-xl sm:text-2xl'}`}>{rec.stem}</h1>

        <div role="radiogroup" aria-label="Şıklar" className="flex flex-col gap-2">
          {rec.options.map((o0, oi) => {
            // Bazı kayıtlarda şık harfi yok: sıradan üret (A, B, C…)
            const opt = { ...o0, key: o0.key || 'ABCDE'[oi] };
            const isThisCorrect = rec.correctAnswer === opt.key;
            const isPicked = userAnswer === opt.key;
            const st = isAnswered ? (isThisCorrect ? 'is-correct' : isPicked ? 'is-wrong' : 'is-dim') : '';
            return (
              <button
                key={opt.key}
                type="button"
                role="radio"
                aria-checked={isPicked}
                onClick={() => handleSelect(opt.key)}
                disabled={isAnswered && !isPicked && !isThisCorrect}
                className={`tm-opt ${st}`}
              >
                <span className="tm-bubble" aria-hidden>{opt.key}</span>
                <span className="flex-1 min-w-0">{opt.text}</span>
                {isAnswered && isThisCorrect && <span className="tm-tag is-ok">Doğru</span>}
                {isAnswered && isPicked && !isThisCorrect && <span className="tm-tag is-bad">Senin cevabın</span>}
              </button>
            );
          })}
        </div>

        {isAnswered && (
          <section className={`tm-verdict ${isCorrect ? 'is-ok' : 'is-bad'}`} role="status">
            <span className={`font-semibold text-md ${isCorrect ? 'text-ok' : 'text-bad-text'}`}>
              {isCorrect ? 'Doğru!' : `Doğru cevap ${rec.correctAnswer}`}
            </span>
            {shortExplanation && <p className="m-0 text-md leading-[1.6] text-ink whitespace-pre-line line-clamp-6">{shortExplanation}</p>}
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1 pt-1">
              <button type="button" onClick={() => setAiChatOpen(true)} className="h-9 text-base font-semibold text-accent inline-flex items-center gap-1.5 cursor-pointer">
                <Sparkles className="w-4 h-4" />
                {isCorrect ? 'Mekanizmayı sor' : 'Neden yanlış? Sor'}
              </button>
              {onOpenQuestion && (
                <button type="button" onClick={() => onOpenQuestion(currentQ)} className="h-9 text-base font-semibold text-ink-2 hover:text-ink inline-flex items-center gap-1.5 cursor-pointer">
                  <BookOpen className="w-4 h-4" />
                  Tam açıklama
                </button>
              )}
              <button type="button" onClick={handleReset} className="h-9 text-base font-semibold text-ink-2 hover:text-ink inline-flex items-center gap-1.5 cursor-pointer">
                <RotateCcw className="w-4 h-4" />
                Tekrar dene
              </button>
            </div>
          </section>
        )}

        {answeredCount === total && total > 0 && (
          <section className="tm-done" aria-label="Test sonucu">
            <div className="tm-done-score">
              <b className="hk-num">%{Math.round((correctCount / total) * 100)}</b>
              <span>{correctCount} doğru · {total - correctCount} yanlış · {formatElapsed(elapsed)}</span>
            </div>
            {total - correctCount > 0 && (
              <div className="tm-done-wrong">
                <span>Yanlışlara dön</span>
                <div>
                  {items.map((q, i) => (selectedAnswers[q.id] && selectedAnswers[q.id] !== q.reconstruction?.correctAnswer ? (
                    <button key={q.id} type="button" onClick={() => go(i)} className="tm-chip">{i + 1}</button>
                  ) : null))}
                </div>
              </div>
            )}
          </section>
        )}

        <p className="hidden md:block m-0 text-sm text-ink-3">Kısayollar: A–E cevap · ← → soru değiştir</p>
      </main>

      {/* Sticky bottom bar: navigator · previous · next */}
      <div className="tm-foot fixed bottom-0 left-0 right-0 z-20 pb-[max(env(safe-area-inset-bottom),10px)] pt-2.5">
        <div className="max-w-[960px] mx-auto px-4 sm:px-8 flex items-center gap-2">
          <button
            type="button"
            onClick={() => setNavOpen(true)}
            aria-haspopup="dialog"
            className="tm-nav-btn"
          >
            <LayoutGrid className="w-[18px] h-[18px] text-ink-2" />
            {position}/{total}
          </button>
          <button
            type="button"
            onClick={() => go(currentIndex - 1)}
            disabled={currentIndex === 0}
            aria-label="Önceki soru"
            className="tm-nav-btn is-icon"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <button
            type="button"
            onClick={() => go(currentIndex + 1)}
            disabled={currentIndex >= total - 1}
            className="ui-btn is-primary tm-next"
          >
            {isAnswered ? 'Sonraki soru' : 'Atla'}
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Soru gezgini: ortak alt sayfa */}
      <Sheet
        open={navOpen}
        onClose={() => setNavOpen(false)}
        title="Sorular"
        subtitle={`${correctCount} doğru · ${answeredCount - correctCount} yanlış · ${total - answeredCount} boş`}
        width={560}
      >
        <nav aria-label="Soru gezgini" className="tm-grid">
          {items.map((q, i) => {
            const ans = selectedAnswers[q.id];
            const current = i === currentIndex;
            const right = ans && ans === q.reconstruction?.correctAnswer;
            return (
              <button
                key={q.id}
                type="button"
                onClick={() => { go(i); setNavOpen(false); }}
                aria-current={current ? 'step' : undefined}
                aria-label={`Soru ${i + 1}${ans ? (right ? ', doğru' : ', yanlış') : ''}`}
                className={`tm-cell ${ans ? (right ? 'is-ok' : 'is-bad') : ''}`}
              >
                {i + 1}
              </button>
            );
          })}
        </nav>
      </Sheet>

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
