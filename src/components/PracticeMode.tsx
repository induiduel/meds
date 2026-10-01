import React, { useEffect, useMemo, useState } from 'react';
import { X, ArrowLeft, ArrowRight, BookOpen } from 'lucide-react';
import { QuestionItem } from '../types';
import { parseExplanation } from './QuestionCard';

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

  const exitButton = onExit && (
    <button
      type="button"
      onClick={onExit}
      aria-label="Testten çık"
      className="w-10 h-10 rounded-[10px] border border-line flex items-center justify-center shrink-0 cursor-pointer hover:border-line-2"
    >
      <X className="w-4 h-4 text-ink" />
    </button>
  );

  if (!currentQ || !rec) {
    return (
      <div className="min-h-screen bg-white flex flex-col">
        <header className="border-b border-line">
          <div className="max-w-[1280px] mx-auto px-4 sm:px-8 h-16 flex items-center gap-4">
            {exitButton}
            <span className="font-semibold text-ink">{title}</span>
          </div>
        </header>
        <main className="flex-1 w-full max-w-[560px] mx-auto px-4 sm:px-8 py-16 flex flex-col gap-4 text-center items-center">
          <h1 className="m-0 font-display text-[28px] font-bold tracking-[-0.02em]">Çözülecek soru henüz yok</h1>
          <p className="m-0 text-[16px] text-ink-2">
            Test modunda yalnızca yeniden kurulup doğrulanan sorular çıkar. Hafıza parçası ekleyip soruların kurulmasına yardım edebilirsin.
          </p>
          <button
            type="button"
            onClick={onOpenContributeModal}
            className="h-12 px-6 rounded-xl bg-accent hover:bg-accent-hover text-white font-semibold cursor-pointer"
          >
            İlk parçayı ekle
          </button>
        </main>
      </div>
    );
  }

  const position = currentIndex + 1;

  return (
    <div className="min-h-screen bg-white text-ink flex flex-col">
      <header className="border-b border-line sticky top-0 bg-white z-20">
        <div className="max-w-[1280px] mx-auto px-4 sm:px-8 h-16 flex items-center gap-3 sm:gap-5">
          {exitButton}
          <div className="flex flex-col leading-[1.25] min-w-0">
            <span className="font-semibold truncate">{title}</span>
            {subtitle && <span className="text-[13px] text-ink-2 truncate">{subtitle}</span>}
          </div>
          <div className="flex-1 hidden sm:flex items-center gap-3 max-w-[420px] ml-auto">
            <div className="flex-1 h-1.5 rounded-full bg-line-soft">
              <div className="h-1.5 rounded-full bg-accent transition-all" style={{ width: `${(position / total) * 100}%` }} />
            </div>
            <span className="font-mono text-[13px] text-ink-2 whitespace-nowrap">
              {position} / {total}
            </span>
          </div>
          <span className="ml-auto sm:ml-0 font-mono text-[14px] px-3 py-2 rounded-[10px] bg-canvas" aria-label="Geçen süre">
            {formatElapsed(elapsed)}
          </span>
        </div>
        <div className="sm:hidden h-1 bg-line-soft">
          <div className="h-1 bg-accent" style={{ width: `${(position / total) * 100}%` }} />
        </div>
      </header>

      <main className="flex-1 w-full max-w-[760px] mx-auto px-4 sm:px-8 pt-10 sm:pt-14 pb-10 flex flex-col gap-6 sm:gap-7">
        <div className="flex items-center justify-between gap-3">
          <span className="font-mono text-[13px] text-ink-2">
            SORU {position}
            {currentQ.discipline ? ` · ${currentQ.discipline.toLocaleUpperCase('tr-TR')}` : ''}
          </span>
          {answeredCount > 0 && (
            <span className="font-mono text-[13px] text-ink-2">
              {correctCount}/{answeredCount} doğru
            </span>
          )}
        </div>
        <h1
          className={`m-0 font-display font-medium leading-[1.3] tracking-[-0.02em] ${
            rec.stem.length > 180 ? 'text-[20px] sm:text-[24px]' : 'text-[24px] sm:text-[32px]'
          }`}
        >
          {rec.stem}
        </h1>

        <div role="radiogroup" aria-label="Şıklar" className="flex flex-col gap-2.5">
          {rec.options.map((opt) => {
            const isThisCorrect = rec.correctAnswer === opt.key;
            const isPicked = userAnswer === opt.key;
            let box = 'border border-line bg-white hover:border-line-2';
            let key = 'bg-canvas text-ink';
            let tag = '';
            let tagCls = 'text-ink-2';
            if (isAnswered && isThisCorrect) {
              box = 'border-[1.5px] border-ok-bright bg-ok-tint';
              key = 'bg-ok text-white';
              tag = 'Doğru cevap';
              tagCls = 'text-ok';
            } else if (isAnswered && isPicked) {
              box = 'border-[1.5px] border-bad bg-bad-soft';
              key = 'bg-bad text-white';
              tag = 'Senin cevabın';
              tagCls = 'text-bad-text';
            } else if (isAnswered) {
              box = 'border border-line bg-white opacity-70';
            }
            return (
              <button
                key={opt.key}
                type="button"
                role="radio"
                aria-checked={isPicked}
                onClick={() => handleSelect(opt.key)}
                className={`flex items-center gap-4 min-h-[60px] px-4 py-2.5 rounded-[14px] text-[16px] sm:text-[17px] text-left cursor-pointer transition-colors ${box} ${
                  isAnswered ? 'cursor-default' : ''
                }`}
              >
                <span className={`w-9 h-9 shrink-0 rounded-[10px] flex items-center justify-center font-mono text-[14px] ${key}`}>{opt.key}</span>
                <span className="flex-1">{opt.text}</span>
                {tag && <span className={`text-[13px] font-semibold whitespace-nowrap ${tagCls}`}>{tag}</span>}
              </button>
            );
          })}
        </div>

        {isAnswered && (
          <section className={`rounded-2xl px-[22px] py-5 flex flex-col gap-2 ${isCorrect ? 'bg-ok-soft' : 'bg-bad-soft'}`}>
            <span className={`font-semibold text-[16px] ${isCorrect ? 'text-ok' : 'text-bad-text'}`}>
              {isCorrect
                ? `Doğru. ${rec.options.find((o) => o.key === rec.correctAnswer)?.text || ''}`
                : `Doğru cevap ${rec.correctAnswer} — ${rec.options.find((o) => o.key === rec.correctAnswer)?.text || ''}`}
            </span>
            {shortExplanation && <p className="m-0 text-[15px] leading-[1.6] whitespace-pre-line line-clamp-6">{shortExplanation}</p>}
            {onOpenQuestion && (
              <button
                type="button"
                onClick={() => onOpenQuestion(currentQ)}
                className="self-start text-[14px] font-semibold text-accent inline-flex items-center gap-1.5 cursor-pointer"
              >
                <BookOpen className="w-4 h-4" />
                Tam açıklama ve kaynak slayt
              </button>
            )}
          </section>
        )}

        <div className="flex gap-3 justify-between pt-2">
          <button
            type="button"
            onClick={() => setCurrentIndex((i) => Math.max(0, i - 1))}
            disabled={currentIndex === 0}
            className="h-12 px-5 rounded-xl border border-line-2 bg-white font-semibold text-ink inline-flex items-center gap-2 cursor-pointer disabled:opacity-40"
          >
            <ArrowLeft className="w-4 h-4" />
            Önceki
          </button>
          <div className="flex gap-2 sm:gap-3">
            {isAnswered && (
              <button type="button" onClick={handleReset} className="h-12 px-4 sm:px-5 rounded-xl font-semibold text-ink-2 cursor-pointer">
                Sıfırla
              </button>
            )}
            <button
              type="button"
              onClick={() => setCurrentIndex((i) => Math.min(total - 1, i + 1))}
              disabled={currentIndex >= total - 1}
              className="h-12 px-5 sm:px-6 rounded-xl bg-accent hover:bg-accent-hover font-semibold text-white inline-flex items-center gap-2 cursor-pointer disabled:opacity-40"
            >
              Sonraki soru
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </main>

      <footer className="border-t border-line bg-[#F7F8FA]">
        <div className="max-w-[1280px] mx-auto px-4 sm:px-8 py-4 flex items-start gap-4">
          <span className="text-[13px] font-semibold text-ink-2 shrink-0 leading-7">Sorular</span>
          <nav aria-label="Soru gezgini" className="flex gap-1.5 flex-wrap max-h-[132px] overflow-y-auto">
            {items.map((q, i) => {
              const ans = selectedAnswers[q.id];
              const current = i === currentIndex;
              const right = ans && ans === q.reconstruction?.correctAnswer;
              const cls = current
                ? 'bg-white text-accent border-2 border-accent'
                : ans
                  ? right
                    ? 'bg-[#DDF1E4] text-ok'
                    : 'bg-[#FDE5D8] text-bad-text'
                  : 'bg-white text-ink-2 border border-line';
              return (
                <button
                  key={q.id}
                  type="button"
                  onClick={() => setCurrentIndex(i)}
                  aria-current={current ? 'step' : undefined}
                  aria-label={`Soru ${i + 1}${ans ? (right ? ', doğru' : ', yanlış') : ''}`}
                  className={`w-7 h-7 rounded-[7px] flex items-center justify-center font-mono text-[11px] cursor-pointer ${cls}`}
                >
                  {i + 1}
                </button>
              );
            })}
          </nav>
        </div>
      </footer>
    </div>
  );
};
