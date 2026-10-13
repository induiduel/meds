import React, { useEffect, useMemo, useState } from 'react';
import { X, ArrowLeft, ArrowRight, BookOpen, Sparkles, LayoutGrid, RotateCcw, Pause, Play, Bookmark, Timer, Flag } from 'lucide-react';
import { QuestionItem } from '../types';
import { parseExplanation } from './QuestionCard';
import { QuestionAiChatDrawer } from './QuestionAiChatDrawer';
import { Sheet } from './ui/Sheet';
import { confirmDialog } from './ui/ConfirmDialog';
import { TestNavigator, navCounts, NavItem } from './practice/TestNavigator';
import '../styles/practice-v10.css';

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
 * /test — Test çöz (v10). Yapı (canvas "Test-Masaustu"):
 *  - Üst çubuk: test adı · "Soru n / N" · süre · Duraklat · Bitir; altında çentikli ilerleme.
 *  - Orta: disiplin etiketi + İşaretle, soru kökü, A–E büyük satırlar, Önceki / Sonraki.
 *  - Sağ (≥1024): soru gezgini (cevaplanan / işaretli / boş / şu anki). Telefon ve tablette gezgin
 *    alt sayfada açılır; gezgin · önceki · sonraki alt çubukta sabit durur.
 *  - Cevap anında değerlendirilir (doğru/yanlış + kısa açıklama); Bitir sonuç ekranını açar.
 * Kısayollar: A–E cevap · ← → soru · M işaretle · P duraklat.
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
  const [marked, setMarked] = useState<Set<string>>(() => new Set());
  const [elapsed, setElapsed] = useState(0);
  const [paused, setPaused] = useState(false);
  const [finished, setFinished] = useState(false);
  const [aiChatOpen, setAiChatOpen] = useState(false);
  const [navOpen, setNavOpen] = useState(false);

  // Süre: duraklatınca ve sonuç ekranında durur
  useEffect(() => {
    if (paused || finished) return;
    const t = setInterval(() => setElapsed((s) => s + 1), 1000);
    return () => clearInterval(t);
  }, [paused, finished]);

  const total = items.length;
  const currentQ = items[Math.min(currentIndex, Math.max(total - 1, 0))];
  const rec = currentQ?.reconstruction;
  const userAnswer = currentQ ? selectedAnswers[currentQ.id] : undefined;
  const isAnswered = !!userAnswer;
  const isCorrect = !!rec && userAnswer === rec.correctAnswer;
  const isMarked = !!currentQ && marked.has(currentQ.id);

  const navItems = useMemo<NavItem[]>(
    () => items.map((q) => ({ id: q.id, answer: selectedAnswers[q.id], correct: q.reconstruction?.correctAnswer })),
    [items, selectedAnswers]
  );
  const counts = useMemo(() => navCounts(navItems, marked), [navItems, marked]);
  const answeredCount = counts.answered;
  const correctCount = counts.correct;

  // Short feedback: the "why correct" section if the redactor wrote one, else the first section
  const shortExplanation = useMemo(() => {
    if (!rec?.explanation) return '';
    const secs = parseExplanation(rec.explanation, rec.correctAnswer);
    const why = secs.find((s) => s.label.startsWith('Neden')) || secs.find((s) => s.label === 'Mekanizma') || secs[0];
    return why?.body || '';
  }, [rec]);

  const handleSelect = (key: string) => {
    if (!currentQ || isAnswered || paused) return;
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

  const toggleMark = () => {
    if (!currentQ) return;
    setMarked((prev) => {
      const next = new Set(prev);
      if (next.has(currentQ.id)) next.delete(currentQ.id);
      else next.add(currentQ.id);
      return next;
    });
  };

  const go = (i: number) => {
    setCurrentIndex(Math.max(0, Math.min(total - 1, i)));
    setNavOpen(false);
    setFinished(false);
    window.scrollTo({ top: 0 });
  };

  const finish = async () => {
    if (counts.empty > 0) {
      const ok = await confirmDialog({
        title: 'Test bitirilsin mi?',
        message: `${counts.empty} soru boş kaldı. Bitirince sonuç ekranı açılır; sorulara yine dönebilirsin.`,
        confirmLabel: 'Bitir',
        cancelLabel: 'Devam et',
      });
      if (!ok) return;
    }
    setPaused(false);
    setNavOpen(false);
    setFinished(true);
    window.scrollTo({ top: 0 });
  };

  const restart = () => {
    setSelectedAnswers({});
    setMarked(new Set());
    setElapsed(0);
    setPaused(false);
    setFinished(false);
    setCurrentIndex(0);
    window.scrollTo({ top: 0 });
  };

  // Keyboard: A–E answer, ← / → move, M mark, P pause, Esc closes the navigator
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (isTyping(e.target) || aiChatOpen || e.metaKey || e.ctrlKey || e.altKey) return;
      if (e.key === 'Escape' && navOpen) return setNavOpen(false);
      if (finished) return;
      if (e.key === 'p' || e.key === 'P') return setPaused((p) => !p);
      if (paused) return;
      if (e.key === 'ArrowRight') return go(currentIndex + 1);
      if (e.key === 'ArrowLeft') return go(currentIndex - 1);
      if (e.key === 'm' || e.key === 'M') return toggleMark();
      const k = e.key.toUpperCase();
      if (rec && /^[A-E]$/.test(k) && rec.options.some((o, i) => (o.key || 'ABCDE'[i]) === k)) handleSelect(k);
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  });

  const exitButton = onExit && (
    <button type="button" onClick={onExit} aria-label="Testten çık" className="tx-ib">
      <X aria-hidden />
    </button>
  );

  if (!currentQ || !rec) {
    return (
      <div className="tx tx-empty-page">
        <header className="tx-head">
          <div className="tx-head-in">
            {exitButton}
            <span className="tx-title"><b>{title}</b></span>
          </div>
        </header>
        <main className="tx-empty">
          <h1>Çözülecek soru henüz yok</h1>
          <p>
            Testte yalnızca yeniden kurulup doğrulanan sorular çıkar. Çıkmış sorularla pratik yapmak için Çalış sayfasını açabilir ya da bu kurula bir parça ekleyebilirsin.
          </p>
          <div className="tx-empty-act">
            {onExit && (
              <button type="button" onClick={onExit} className="ui-btn is-primary">
                Çalış'a dön
              </button>
            )}
            <button type="button" onClick={onOpenContributeModal} className="ui-btn">
              Parça ekle
            </button>
          </div>
        </main>
      </div>
    );
  }

  const position = currentIndex + 1;
  const pct = (position / total) * 100;
  const atEnd = currentIndex >= total - 1;

  const prevNext = (
    <>
      <button type="button" onClick={() => go(currentIndex - 1)} disabled={currentIndex === 0 || paused} className="tx-pn-btn" aria-label="Önceki soru">
        <ArrowLeft aria-hidden />
        <span>Önceki</span>
      </button>
      <button type="button" onClick={() => (atEnd ? finish() : go(currentIndex + 1))} disabled={paused} className="tx-pn-btn is-next">
        <span>{atEnd ? 'Testi bitir' : isAnswered ? 'Sonraki' : 'Atla'}</span>
        {atEnd ? <Flag aria-hidden /> : <ArrowRight aria-hidden />}
      </button>
    </>
  );

  return (
    <div className={`tx ${paused ? 'is-paused' : ''}`}>
      <header className="tx-head">
        <div className="tx-head-in">
          {exitButton}
          <span className="tx-title">
            <b>{title}</b>
            {subtitle && <span>{subtitle}</span>}
          </span>
          <span className="tx-pos" aria-label={`Soru ${position} / ${total}`}>
            <span className="tx-pos-l">Soru </span><b>{position}</b> / {total}
          </span>
          <span className="tx-sp" />
          <span role="timer" aria-label={`Geçen süre ${formatElapsed(elapsed)}`} className={`tx-timer ${paused ? 'is-paused' : ''}`}>
            <Timer aria-hidden />
            {formatElapsed(elapsed)}
          </span>
          {!finished && (
            <>
              <button
                type="button"
                onClick={() => setPaused((p) => !p)}
                aria-pressed={paused}
                className="tx-hbtn"
                aria-label={paused ? 'Devam et' : 'Duraklat'}
                title={paused ? 'Devam et (P)' : 'Duraklat (P)'}
              >
                {paused ? <Play aria-hidden /> : <Pause aria-hidden />}
                <span>{paused ? 'Devam' : 'Duraklat'}</span>
              </button>
              <button type="button" onClick={finish} className="tx-hbtn is-end">
                Bitir
              </button>
            </>
          )}
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

      {finished ? (
        <TestResults
          items={items}
          answers={selectedAnswers}
          marked={marked}
          elapsed={elapsed}
          onGo={go}
          onReview={() => setFinished(false)}
          onRestart={restart}
          onExit={onExit}
        />
      ) : (
        <div className="tx-body">
          <main className="tx-main">
            <article className="tx-q" aria-hidden={paused || undefined}>
              <div className="tx-meta">
                {currentQ.discipline && <span className="tx-disc">{currentQ.discipline}</span>}
                {answeredCount > 0 && (
                  <span className="tx-score">
                    <b>{correctCount}</b>/{answeredCount} doğru
                  </span>
                )}
                <span className="tx-sp" />
                <button type="button" onClick={() => setAiChatOpen(true)} className="tx-chip is-ai" title="Bu soruyu yapay zekâya sor">
                  <Sparkles aria-hidden />
                  <span>AI'ya sor</span>
                </button>
                <button type="button" onClick={toggleMark} aria-pressed={isMarked} className={`tx-chip ${isMarked ? 'is-mark' : ''}`} title="İşaretle (M)">
                  <Bookmark aria-hidden fill={isMarked ? 'currentColor' : 'none'} />
                  <span>{isMarked ? 'İşaretli' : 'İşaretle'}</span>
                </button>
              </div>

              <h1 className={`tx-stem ${rec.stem.length > 180 ? 'is-long' : ''}`}>{rec.stem}</h1>

              <div role="radiogroup" aria-label="Şıklar" className="tx-opts">
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
                      disabled={(isAnswered && !isPicked && !isThisCorrect) || paused}
                      className={`tm-opt tx-opt ${st}`}
                    >
                      <span className="tm-bubble tx-key" aria-hidden>{opt.key}</span>
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
                  <div className="tx-verdict-act">
                    <button type="button" onClick={() => setAiChatOpen(true)} className="is-acc">
                      <Sparkles aria-hidden />
                      {isCorrect ? 'Mekanizmayı sor' : 'Neden yanlış? Sor'}
                    </button>
                    {onOpenQuestion && (
                      <button type="button" onClick={() => onOpenQuestion(currentQ)}>
                        <BookOpen aria-hidden />
                        Tam açıklama
                      </button>
                    )}
                    <button type="button" onClick={handleReset}>
                      <RotateCcw aria-hidden />
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
                  <button type="button" onClick={finish} className="ui-btn is-tonal tx-done-btn">Sonuç ekranı</button>
                </section>
              )}

              {/* Masaüstü: soru altında önceki / sonraki */}
              <div className="tx-pn">{prevNext}</div>
            </article>

            {paused && (
              <div className="tx-pause" role="dialog" aria-label="Test duraklatıldı">
                <Pause aria-hidden />
                <b>Test duraklatıldı</b>
                <span>Süre durdu · {formatElapsed(elapsed)}</span>
                <button type="button" onClick={() => setPaused(false)} className="ui-btn is-primary" autoFocus>
                  <Play aria-hidden /> Devam et
                </button>
              </div>
            )}

            <p className="tx-keys">Kısayollar: A–E cevap · ← → soru · M işaretle · P duraklat</p>
          </main>

          <aside className="tx-aside" aria-label="Soru gezgini">
            <TestNavigator items={navItems} current={currentIndex} marked={marked} onGo={go} />
          </aside>
        </div>
      )}

      {/* Telefon ve tablet: gezgin · önceki · sonraki alt çubukta sabit */}
      {!finished && (
        <div className="tx-foot">
          <div className="tx-foot-in">
            <button type="button" onClick={() => setNavOpen(true)} aria-haspopup="dialog" className="tx-pn-btn is-nav" aria-label={`Soru gezgini, ${position} / ${total}`}>
              <LayoutGrid aria-hidden />
              <span>{position}/{total}</span>
            </button>
            {prevNext}
          </div>
        </div>
      )}

      {/* Soru gezgini: ortak alt sayfa */}
      <Sheet
        open={navOpen}
        onClose={() => setNavOpen(false)}
        title="Sorular"
        subtitle={`${correctCount} doğru · ${answeredCount - correctCount} yanlış · ${total - answeredCount} boş`}
        width={560}
      >
        <TestNavigator items={navItems} current={currentIndex} marked={marked} onGo={go} />
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

/** Bitir sonrası sonuç ekranı: puan, döküm ve yanlış / işaretli / boş sorulara dönüş */
const TestResults: React.FC<{
  items: QuestionItem[];
  answers: Record<string, string>;
  marked: Set<string>;
  elapsed: number;
  onGo: (i: number) => void;
  onReview: () => void;
  onRestart: () => void;
  onExit?: () => void;
}> = ({ items, answers, marked, elapsed, onGo, onReview, onRestart, onExit }) => {
  const total = items.length;
  const wrong: number[] = [];
  const empty: number[] = [];
  const flagged: number[] = [];
  let correct = 0;
  items.forEach((q, i) => {
    const a = answers[q.id];
    if (!a) empty.push(i);
    else if (a === q.reconstruction?.correctAnswer) correct++;
    else wrong.push(i);
    if (marked.has(q.id)) flagged.push(i);
  });
  const pct = total ? Math.round((correct / total) * 100) : 0;
  const groups: [string, number[], string][] = [
    ['Yanlışlar', wrong, 'is-bad'],
    ['İşaretliler', flagged, 'is-mark'],
    ['Boş bırakılanlar', empty, ''],
  ];
  return (
    <main className="tx-res">
      <section className="tx-res-card" aria-label="Test sonucu">
        <span className="tx-res-k">Sonuç</span>
        <b className="tx-res-pct hk-num">%{pct}</b>
        <div className="tx-res-tiles">
          <span className="is-ok"><b>{correct}</b>Doğru</span>
          <span className="is-bad"><b>{wrong.length}</b>Yanlış</span>
          <span><b>{empty.length}</b>Boş</span>
          <span><b>{formatElapsed(elapsed)}</b>Süre</span>
        </div>
        {groups.map(([label, list, tone]) =>
          list.length ? (
            <div key={label} className="tx-res-g">
              <span>{label} · {list.length}</span>
              <div>
                {list.map((i) => (
                  <button key={i} type="button" onClick={() => onGo(i)} className={`tx-res-chip ${tone}`} aria-label={`Soru ${i + 1}`}>
                    {i + 1}
                  </button>
                ))}
              </div>
            </div>
          ) : null
        )}
        <div className="tx-res-act">
          <button type="button" onClick={onReview} className="ui-btn">Soruları incele</button>
          <button type="button" onClick={onRestart} className="ui-btn is-tonal">
            <RotateCcw aria-hidden /> Yeniden başla
          </button>
          {onExit && <button type="button" onClick={onExit} className="ui-btn is-primary">Çalış'a dön</button>}
        </div>
      </section>
    </main>
  );
};
