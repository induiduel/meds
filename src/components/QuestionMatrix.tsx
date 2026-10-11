import React from 'react';
import { PageHeader } from './ui/PageHeader';
import { Sparkles, Plus, Clock } from 'lucide-react';
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
    <div className="flex flex-col gap-4">
    <PageHeader
      eyebrow="Kurul görünümü"
      title="Soru haritası"
      description={`1–${targetCount} arası her kutu sınavdaki bir soru. Numaraya tıklayıp soruyu açabilir ya da aklındaki parçayı ekleyebilirsin.`}
    />
    <div className="bg-white rounded-2xl border border-line p-4 sm:p-6 shadow-xs space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-line-soft">
        {/* Legend */}
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-3.5 rounded bg-ok border border-ok inline-block" />
            <span className="text-ink-2">AI Rekonstrükte (%90+)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-3.5 rounded bg-warn border border-warn inline-block" />
            <span className="text-ink-2">Taslak / Katkı Var</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-3.5 h-3.5 rounded bg-field border border-line-2 inline-block" />
            <span className="text-ink-2">Henüz Hatırlanmadı</span>
          </div>
        </div>
      </div>

      {/* Grid of 100/150 buttons */}
      <div className="grid grid-cols-5 sm:grid-cols-10 md:grid-cols-12 lg:grid-cols-15 gap-2">
        {slots.map((num) => {
          const item = questionMap.get(num);
          const isCompleted = item?.status === 'completed' && item.reconstruction;
          const isGathering = item?.status === 'gathering' || (item?.fragments && item.fragments.length > 0);

          let bgClasses = 'bg-field border-line text-ink-3 hover:border-ok hover:bg-ok-soft/50 hover:text-ok';
          let badgeIcon = <Plus className="w-2.5 h-2.5 opacity-40 group-hover:opacity-100" />;

          if (isCompleted) {
            bgClasses = 'bg-ok-soft border-ok text-ok shadow-xs hover:bg-ok-soft hover:border-ok font-bold';
            badgeIcon = <Sparkles className="w-3 h-3 text-ok" />;
          } else if (isGathering) {
            bgClasses = 'bg-warn-soft border-warn/30 text-warn hover:bg-warn-soft hover:border-warn font-semibold';
            badgeIcon = <Clock className="w-3 h-3 text-warn" />;
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
    </div>
  );
};
