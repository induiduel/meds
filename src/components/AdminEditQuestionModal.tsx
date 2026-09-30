import React, { useState } from 'react';
import { X, Save, ShieldAlert, Sparkles } from 'lucide-react';
import { QuestionItem } from '../types';

interface AdminEditQuestionModalProps {
  isOpen: boolean;
  onClose: () => void;
  question: QuestionItem | null;
  adminEmail: string;
  onSaveQuestion: (updated: Partial<QuestionItem>) => Promise<void>;
}

export const AdminEditQuestionModal: React.FC<AdminEditQuestionModalProps> = ({
  isOpen,
  onClose,
  question,
  adminEmail,
  onSaveQuestion,
}) => {
  if (!isOpen || !question) return null;

  const [questionNumber, setQuestionNumber] = useState(question.questionNumber);
  const [discipline, setDiscipline] = useState(question.discipline);
  const [topic, setTopic] = useState(question.topic);
  const [status, setStatus] = useState(question.status);
  const [claimedAnswer, setClaimedAnswer] = useState(question.claimedAnswer || '');

  // Reconstruction fields
  const rec = question.reconstruction;
  const [stem, setStem] = useState(rec?.stem || '');
  const [correctAnswer, setCorrectAnswer] = useState(rec?.correctAnswer || 'A');
  const [explanation, setExplanation] = useState(rec?.explanation || '');
  const [confidenceScore, setConfidenceScore] = useState(rec?.confidenceScore || 90);

  const [optA, setOptA] = useState(rec?.options.find((o) => o.key === 'A')?.text || '');
  const [optB, setOptB] = useState(rec?.options.find((o) => o.key === 'B')?.text || '');
  const [optC, setOptC] = useState(rec?.options.find((o) => o.key === 'C')?.text || '');
  const [optD, setOptD] = useState(rec?.options.find((o) => o.key === 'D')?.text || '');
  const [optE, setOptE] = useState(rec?.options.find((o) => o.key === 'E')?.text || '');

  const [isSaving, setIsSaving] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      const updatedOptions = [
        { key: 'A' as const, text: optA, isAiFilled: false },
        { key: 'B' as const, text: optB, isAiFilled: false },
        { key: 'C' as const, text: optC, isAiFilled: false },
        { key: 'D' as const, text: optD, isAiFilled: false },
        { key: 'E' as const, text: optE, isAiFilled: false },
      ].filter((o) => o.text.trim().length > 0);

      const hasValidRec = stem.trim().length > 0 && updatedOptions.length >= 2;

      await onSaveQuestion({
        questionNumber: Number(questionNumber),
        discipline,
        topic,
        status: hasValidRec ? 'completed' : status,
        claimedAnswer: (claimedAnswer as any) || undefined,
        reconstruction: hasValidRec
          ? {
              stem: stem.trim(),
              options: updatedOptions,
              correctAnswer: correctAnswer as any,
              explanation: explanation.trim(),
              confidenceScore: Number(confidenceScore),
              notesAndDiscrepancies: rec?.notesAndDiscrepancies || 'Yönetici tarafından güncellendi.',
              lastUpdated: new Date().toISOString(),
            }
          : undefined,
      });

      onClose();
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl max-w-2xl w-full shadow-2xl border border-slate-200 overflow-hidden my-6">
        <div className="bg-slate-900 text-white p-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="p-1.5 rounded-lg bg-teal-500/20 text-teal-400">
              <ShieldAlert className="w-4 h-4" />
            </span>
            <div>
              <h3 className="font-bold text-sm">
                Yönetici Soru Düzenleme: #{question.questionNumber}
              </h3>
              <p className="text-[11px] text-slate-400">
                Oturum: {adminEmail} (Yetkili)
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-5 space-y-4 max-h-[75vh] overflow-y-auto text-xs">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Soru No</label>
              <input
                type="number"
                value={questionNumber}
                onChange={(e) => setQuestionNumber(Number(e.target.value))}
                className="w-full bg-slate-50 border border-slate-200 rounded p-1.5 font-bold"
                required
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Ders</label>
              <input
                type="text"
                value={discipline}
                onChange={(e) => setDiscipline(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded p-1.5"
                required
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-700 mb-1">Konu Başlığı</label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded p-1.5"
                required
              />
            </div>
          </div>

          <div className="space-y-3 pt-2 border-t border-slate-100">
            <div className="flex items-center justify-between">
              <span className="font-bold text-slate-900 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-teal-600" />
                Rekonstrükte Soru Kökü & Metni
              </span>
              <div className="flex items-center gap-2">
                <label className="font-semibold text-slate-600">Güven (%):</label>
                <input
                  type="number"
                  min={0}
                  max={100}
                  value={confidenceScore}
                  onChange={(e) => setConfidenceScore(Number(e.target.value))}
                  className="w-16 bg-slate-50 border border-slate-200 rounded px-1.5 py-0.5 text-center font-bold text-teal-700"
                />
              </div>
            </div>

            <textarea
              rows={4}
              value={stem}
              onChange={(e) => setStem(e.target.value)}
              placeholder="Tam soru metnini buraya yazın..."
              className="w-full bg-slate-50 border border-slate-200 rounded p-2.5 text-slate-900 focus:bg-white"
            />
          </div>

          {/* Options */}
          <div className="space-y-2 pt-2 border-t border-slate-100">
            <span className="font-bold text-slate-900 block">Şıklar (A - E)</span>
            {[
              { key: 'A', val: optA, set: setOptA },
              { key: 'B', val: optB, set: setOptB },
              { key: 'C', val: optC, set: setOptC },
              { key: 'D', val: optD, set: setOptD },
              { key: 'E', val: optE, set: setOptE },
            ].map(({ key, val, set }) => (
              <div key={key} className="flex items-center gap-2">
                <span className="w-6 h-6 rounded bg-slate-200 font-bold flex items-center justify-center shrink-0">
                  {key}
                </span>
                <input
                  type="text"
                  value={val}
                  onChange={(e) => set(e.target.value)}
                  placeholder={`${key} şıkkı metni`}
                  className="flex-1 bg-slate-50 border border-slate-200 rounded px-2.5 py-1 text-slate-800"
                />
                <button
                  type="button"
                  onClick={() => setCorrectAnswer(key as any)}
                  className={`px-2 py-1 rounded font-bold text-[11px] cursor-pointer ${
                    correctAnswer === key
                      ? 'bg-emerald-600 text-white'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  {correctAnswer === key ? '✓ Doğru' : 'Doğru Yap'}
                </button>
              </div>
            ))}
          </div>

          {/* Explanation */}
          <div className="space-y-1.5 pt-2 border-t border-slate-100">
            <label className="block font-bold text-slate-900">
              Tıbbi Gerekçe & Patofizyoloji Açıklaması
            </label>
            <textarea
              rows={3}
              value={explanation}
              onChange={(e) => setExplanation(e.target.value)}
              placeholder="Robbins / Katzung standartlarında açıklama..."
              className="w-full bg-slate-50 border border-slate-200 rounded p-2 text-slate-900 focus:bg-white"
            />
          </div>

          <div className="pt-3 border-t border-slate-100 flex items-center justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-3.5 py-1.5 rounded-lg text-slate-600 hover:bg-slate-100 cursor-pointer"
            >
              Vazgeç
            </button>
            <button
              type="submit"
              disabled={isSaving}
              className="bg-teal-700 hover:bg-teal-800 text-white px-4 py-1.5 rounded-lg font-bold flex items-center gap-1.5 cursor-pointer disabled:opacity-50"
            >
              <Save className="w-3.5 h-3.5" />
              <span>{isSaving ? 'Kaydediliyor...' : 'Değişiklikleri Kaydet'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
