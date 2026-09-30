import React, { useState } from 'react';
import { 
  Brain, 
  CheckCircle2, 
  XCircle, 
  ArrowRight, 
  ArrowLeft, 
  RotateCcw, 
  BookOpen, 
  Sparkles,
  Trophy,
  HelpCircle
} from 'lucide-react';
import { QuestionItem } from '../types';

interface PracticeModeProps {
  questions: QuestionItem[];
  onOpenContributeModal: () => void;
}

export const PracticeMode: React.FC<PracticeModeProps> = ({
  questions,
  onOpenContributeModal,
}) => {
  // Only reconstructed questions can be practiced
  const reconstructedQuestions = questions.filter(
    (q) => q.status === 'completed' && q.reconstruction
  );

  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  const [showExplanations, setShowExplanations] = useState<Record<string, boolean>>({});

  if (reconstructedQuestions.length === 0) {
    return (
      <div className="bg-white rounded-xl border border-slate-200 p-10 text-center space-y-4 max-w-xl mx-auto shadow-xs">
        <div className="w-14 h-14 rounded-2xl bg-teal-50 border border-teal-200 text-teal-600 flex items-center justify-center mx-auto">
          <Brain className="w-7 h-7" />
        </div>
        <div>
          <h3 className="text-base font-bold text-slate-900">
            Henüz Çözülecek Rekonstrükte Soru Yok
          </h3>
          <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
            Test modunda soru çözebilmek için öğrenci hafıza havuzundaki soruların en az birini "AI ile Rekonstrükte Et" butonuyla tamamlamalısınız.
          </p>
        </div>
        <button
          onClick={onOpenContributeModal}
          className="bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold px-4 py-2 rounded-lg inline-flex items-center gap-2 cursor-pointer shadow-xs"
        >
          <span>İlk Soru Parçasını Ekle</span>
        </button>
      </div>
    );
  }

  const currentQ = reconstructedQuestions[currentIndex];
  const rec = currentQ.reconstruction!;
  const userAnswer = selectedAnswers[currentQ.id];
  const isAnswered = !!userAnswer;
  const isCorrect = userAnswer === rec.correctAnswer;
  const isExplanationShown = showExplanations[currentQ.id];

  // Stats
  const answeredCount = Object.keys(selectedAnswers).length;
  const correctCount = Object.entries(selectedAnswers).filter(
    ([qId, ans]) => {
      const q = reconstructedQuestions.find((item) => item.id === qId);
      return q?.reconstruction?.correctAnswer === ans;
    }
  ).length;

  const handleSelectOption = (key: string) => {
    if (isAnswered) return; // Prevent changing answer
    setSelectedAnswers((prev) => ({ ...prev, [currentQ.id]: key }));
    setShowExplanations((prev) => ({ ...prev, [currentQ.id]: true }));
  };

  const handleReset = () => {
    setSelectedAnswers({});
    setShowExplanations({});
    setCurrentIndex(0);
  };

  return (
    <div className="max-w-3xl mx-auto space-y-5">
      {/* Top Bar with Score */}
      <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-xs flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-teal-600" />
          <span className="font-bold text-sm text-slate-900">
            Soru {currentIndex + 1} / {reconstructedQuestions.length}
          </span>
          <span className="text-xs bg-teal-50 text-teal-800 border border-teal-200 px-2 py-0.5 rounded-full font-medium">
            {currentQ.discipline}
          </span>
        </div>

        <div className="flex items-center gap-4 text-xs">
          <div className="flex items-center gap-1.5 font-semibold text-slate-700">
            <Trophy className="w-4 h-4 text-amber-500" />
            <span>Doğru: {correctCount} / {answeredCount}</span>
            {answeredCount > 0 && (
              <span className="text-slate-400">
                (%{Math.round((correctCount / answeredCount) * 100)})
              </span>
            )}
          </div>

          <button
            onClick={handleReset}
            className="text-slate-400 hover:text-slate-700 flex items-center gap-1 cursor-pointer"
            title="Skoru Sıfırla"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Sıfırla</span>
          </button>
        </div>
      </div>

      {/* Main Question Box */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-5">
        <div className="flex items-center justify-between text-xs text-slate-500 border-b pb-2">
          <span className="font-bold text-teal-800 bg-teal-50 px-2 py-0.5 rounded">
            Soru #{currentQ.questionNumber} • {currentQ.topic}
          </span>
          <span className="flex items-center gap-1 text-emerald-700 font-medium">
            <Sparkles className="w-3.5 h-3.5" />
            Rekonstrüksiyon Güven: %{rec.confidenceScore}
          </span>
        </div>

        {/* Stem */}
        <p className="text-sm font-medium text-slate-900 leading-relaxed font-serif">
          {rec.stem}
        </p>

        {/* Options */}
        <div className="space-y-2.5 pt-2">
          {rec.options.map((opt) => {
            const isSelected = userAnswer === opt.key;
            const isThisCorrect = rec.correctAnswer === opt.key;

            let btnStyle = 'bg-white border-slate-200 hover:border-teal-400 hover:bg-slate-50 text-slate-800';
            let circleStyle = 'bg-slate-100 text-slate-700';

            if (isAnswered) {
              if (isThisCorrect) {
                btnStyle = 'bg-emerald-50 border-emerald-500 text-emerald-950 font-semibold ring-1 ring-emerald-500/20';
                circleStyle = 'bg-emerald-600 text-white';
              } else if (isSelected) {
                btnStyle = 'bg-rose-50 border-rose-400 text-rose-950 font-semibold';
                circleStyle = 'bg-rose-600 text-white';
              } else {
                btnStyle = 'bg-slate-50/50 border-slate-200 opacity-60 text-slate-600';
              }
            }

            return (
              <button
                key={opt.key}
                onClick={() => handleSelectOption(opt.key)}
                disabled={isAnswered}
                className={`w-full p-3 rounded-lg border text-xs flex items-center justify-between gap-3 text-left transition-all cursor-pointer ${btnStyle}`}
              >
                <div className="flex items-center gap-2.5">
                  <span className={`w-6 h-6 rounded-full flex items-center justify-center font-bold text-xs shrink-0 ${circleStyle}`}>
                    {opt.key}
                  </span>
                  <span>{opt.text}</span>
                </div>

                {isAnswered && isThisCorrect && (
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                )}
                {isAnswered && isSelected && !isThisCorrect && (
                  <XCircle className="w-4 h-4 text-rose-600 shrink-0" />
                )}
              </button>
            );
          })}
        </div>

        {/* Feedback & Medical Explanation */}
        {isAnswered && (
          <div className="mt-4 pt-4 border-t border-slate-100 space-y-3 animate-fadeIn">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {isCorrect ? (
                  <span className="text-xs font-bold text-emerald-700 flex items-center gap-1">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    Tebrikler! Doğru cevap ({rec.correctAnswer})
                  </span>
                ) : (
                  <span className="text-xs font-bold text-rose-700 flex items-center gap-1">
                    <XCircle className="w-4 h-4 text-rose-600" />
                    Yanlış. Doğru cevap: {rec.correctAnswer}
                  </span>
                )}
              </div>

              <button
                onClick={() =>
                  setShowExplanations((prev) => ({
                    ...prev,
                    [currentQ.id]: !prev[currentQ.id],
                  }))
                }
                className="text-xs text-teal-700 hover:text-teal-800 font-semibold cursor-pointer"
              >
                {isExplanationShown ? 'Açıklamayı Gizle' : 'Açıklamayı Göster'}
              </button>
            </div>

            {isExplanationShown && (
              <div className="bg-emerald-50/70 border border-emerald-200 rounded-lg p-3.5 text-xs space-y-1.5">
                <span className="font-bold text-emerald-950 flex items-center gap-1">
                  <BookOpen className="w-3.5 h-3.5 text-emerald-700" />
                  Tıbbi Gerekçe & Patofizyoloji:
                </span>
                <p className="text-emerald-900 leading-relaxed font-sans">{rec.explanation}</p>
              </div>
            )}
          </div>
        )}

        {/* Prev / Next Navigation */}
        <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
          <button
            onClick={() => setCurrentIndex((prev) => Math.max(0, prev - 1))}
            disabled={currentIndex === 0}
            className="px-3.5 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-30 flex items-center gap-1 cursor-pointer"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Önceki Soru</span>
          </button>

          <span className="text-xs text-slate-400">
            {currentIndex + 1} / {reconstructedQuestions.length}
          </span>

          <button
            onClick={() =>
              setCurrentIndex((prev) =>
                Math.min(reconstructedQuestions.length - 1, prev + 1)
              )
            }
            disabled={currentIndex === reconstructedQuestions.length - 1}
            className="px-3.5 py-1.5 rounded-lg bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold disabled:opacity-30 flex items-center gap-1 cursor-pointer"
          >
            <span>Sonraki Soru</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
