import React from 'react';
import { Sparkles, Plus, Clock, HelpCircle, Layers } from 'lucide-react';
import { QuestionItem } from '../types';

interface QuestionMatrixProps {
  questions: QuestionItem[];
  targetCount: number;
  onSelectQuestion: (question: QuestionItem) => void;
  onAddContributionForNumber: (questionNumber: number) => void;
}

export const QuestionMatrix: React.FC<QuestionMatrixProps> = ({
  questions,
  targetCount,
  onSelectQuestion,
  onAddContributionForNumber,
}) => {
  // Map questions by questionNumber
  const questionMap = new Map<number, QuestionItem>();
  questions.forEach((q) => {
    questionMap.set(q.questionNumber, q);
  });

  const slots = Array.from({ length: targetCount }, (_, i) => i + 1);

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
        <div>
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
            <Layers className="w-5 h-5 text-teal-600" />
            1-{targetCount} Soru Haritası ve Tamamlanma Durumu
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Her kutucuk kurul sınavındaki bir soruyu temsil eder. Herhangi bir numaraya tıklayarak soruyu açabilir veya aklınızdaki parçayı ekleyebilirsiniz.
          </p>
        </div>

        {/* Legend */}
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-3.5 rounded bg-emerald-500 border border-emerald-600 inline-block" />
            <span className="text-slate-600">AI Rekonstrükte (%90+)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-3.5 rounded bg-amber-400 border border-amber-500 inline-block" />
            <span className="text-slate-600">Taslak / Katkı Var</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-3.5 rounded bg-slate-100 border border-slate-300 inline-block" />
            <span className="text-slate-600">Henüz Hatırlanmadı</span>
          </div>
        </div>
      </div>

      {/* Grid of 100/150 buttons */}
      <div className="grid grid-cols-5 sm:grid-cols-10 md:grid-cols-12 lg:grid-cols-15 gap-2">
        {slots.map((num) => {
          const item = questionMap.get(num);
          const isCompleted = item?.status === 'completed' && item.reconstruction;
          const isGathering = item?.status === 'gathering' || (item?.fragments && item.fragments.length > 0);

          let bgClasses = 'bg-slate-50 border-slate-200 text-slate-500 hover:border-teal-400 hover:bg-teal-50/50 hover:text-teal-700';
          let badgeIcon = <Plus className="w-2.5 h-2.5 opacity-40 group-hover:opacity-100" />;

          if (isCompleted) {
            bgClasses = 'bg-emerald-50 border-emerald-400 text-emerald-800 shadow-xs hover:bg-emerald-100 hover:border-emerald-500 font-bold';
            badgeIcon = <Sparkles className="w-3 h-3 text-emerald-600" />;
          } else if (isGathering) {
            bgClasses = 'bg-amber-50 border-amber-300 text-amber-800 hover:bg-amber-100 hover:border-amber-400 font-semibold';
            badgeIcon = <Clock className="w-3 h-3 text-amber-600" />;
          }

          return (
            <button
              key={num}
              onClick={() => {
                if (item && (item.fragments.length > 0 || item.reconstruction)) {
                  onSelectQuestion(item);
                } else {
                  onAddContributionForNumber(num);
                }
              }}
              title={
                item
                  ? `Soru #${num}: ${item.discipline} - ${item.topic} (${item.status})`
                  : `Soru #${num}: Henüz parça girilmedi. Tıkla ve katkı yap.`
              }
              className={`group relative p-2 rounded-lg border text-xs flex flex-col items-center justify-center transition-all cursor-pointer aspect-square ${bgClasses}`}
            >
              <span className="text-sm font-semibold">{num}</span>
              <div className="absolute bottom-1 right-1">{badgeIcon}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
