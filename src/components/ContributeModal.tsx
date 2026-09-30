import React, { useState } from 'react';
import { X, Sparkles, Send, Stethoscope, AlertCircle, Plus, Check } from 'lucide-react';
import { Committee } from '../types';
import { AppUser } from '../services/auth';

const SAVED_NAME_KEY = 'medsoru_saved_contributor_name';

interface ContributeModalProps {
  isOpen: boolean;
  onClose: () => void;
  committees: Committee[];
  selectedCommitteeId: string;
  defaultQuestionNumber?: number;
  currentUser?: AppUser | null;
  onAddQuestionContribution: (data: {
    committeeId: string;
    questionNumber?: number;
    isUnknownNumber?: boolean;
    discipline: string;
    topic: string;
    fragmentText: string;
    author: string;
    authorUid?: string;
    authorStudentNumber?: string;
    claimedAnswer?: 'A' | 'B' | 'C' | 'D' | 'E';
    options?: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string }[];
  }) => Promise<void>;
}

const DISCIPLINES = [
  'Patoloji',
  'Farmakoloji',
  'Tıbbi Mikrobiyoloji',
  'Dahiliye',
  'Göğüs Hastalıkları',
  'Kardiyoloji',
  'Pediatri',
  'Anatomi',
  'Fizyoloji',
  'Tıbbi Biyokimya',
  'Tıbbi Biyoloji & Genetik',
  'Halk Sağlığı',
];

export const ContributeModal: React.FC<ContributeModalProps> = ({
  isOpen,
  onClose,
  committees,
  selectedCommitteeId,
  defaultQuestionNumber,
  currentUser,
  onAddQuestionContribution,
}) => {
  const [committeeId, setCommitteeId] = useState(selectedCommitteeId);
  const selectedComm = committees.find((c) => c.id === committeeId) || committees[0];
  const activeDisciplines = (selectedComm?.disciplines && selectedComm.disciplines.length > 0)
    ? selectedComm.disciplines
    : DISCIPLINES;

  const [isUnknownNumber, setIsUnknownNumber] = useState(!defaultQuestionNumber);
  const [questionNumber, setQuestionNumber] = useState(defaultQuestionNumber || 1);
  const [discipline, setDiscipline] = useState(activeDisciplines[0] || 'Farmakoloji');
  const [topic, setTopic] = useState('');
  const [fragmentText, setFragmentText] = useState('');
  const [author, setAuthor] = useState(() => currentUser?.displayName || localStorage.getItem(SAVED_NAME_KEY) || '');
  const [claimedAnswer, setClaimedAnswer] = useState<'A' | 'B' | 'C' | 'D' | 'E' | ''>('');

  React.useEffect(() => {
    if (currentUser?.displayName && !author) {
      setAuthor(currentUser.displayName);
    }
  }, [currentUser]);

  const handleAuthorChange = (val: string) => {
    setAuthor(val);
    localStorage.setItem(SAVED_NAME_KEY, val);
  };

  React.useEffect(() => {
    if (activeDisciplines && activeDisciplines.length > 0) {
      if (!activeDisciplines.includes(discipline)) {
        setDiscipline(activeDisciplines[0]);
      }
    }
  }, [committeeId, selectedComm]);

  // Remembered options
  const [optionA, setOptionA] = useState('');
  const [optionB, setOptionB] = useState('');
  const [optionC, setOptionC] = useState('');
  const [optionD, setOptionD] = useState('');
  const [optionE, setOptionE] = useState('');

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [aiAssisting, setAiAssisting] = useState(false);
  const [aiSuggestion, setAiSuggestion] = useState<{
    suggestedStem?: string;
    suggestedOptions?: { key: string; text: string }[];
    probableAnswer?: string;
  } | null>(null);

  if (!isOpen) return null;

  const handleQuickAiAssist = async () => {
    if (!fragmentText.trim()) return;
    setAiAssisting(true);
    try {
      const res = await fetch('/api/ai/quick-assist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          discipline,
          topic,
          fragment: fragmentText,
        }),
      });
      const data = await res.json();
      setAiSuggestion(data);
      if (data.suggestedOptions) {
        data.suggestedOptions.forEach((opt: { key: string; text: string }) => {
          if (opt.key === 'A' && !optionA) setOptionA(opt.text);
          if (opt.key === 'B' && !optionB) setOptionB(opt.text);
          if (opt.key === 'C' && !optionC) setOptionC(opt.text);
          if (opt.key === 'D' && !optionD) setOptionD(opt.text);
          if (opt.key === 'E' && !optionE) setOptionE(opt.text);
        });
      }
    } catch (e) {
      console.error(e);
    } finally {
      setAiAssisting(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!fragmentText.trim()) return;

    setIsSubmitting(true);
    try {
      const optionsPayload: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string }[] = [];
      if (optionA.trim()) optionsPayload.push({ key: 'A', text: optionA.trim() });
      if (optionB.trim()) optionsPayload.push({ key: 'B', text: optionB.trim() });
      if (optionC.trim()) optionsPayload.push({ key: 'C', text: optionC.trim() });
      if (optionD.trim()) optionsPayload.push({ key: 'D', text: optionD.trim() });
      if (optionE.trim()) optionsPayload.push({ key: 'E', text: optionE.trim() });

      await onAddQuestionContribution({
        committeeId: committeeId || selectedCommitteeId,
        questionNumber: isUnknownNumber ? undefined : Number(questionNumber),
        isUnknownNumber,
        discipline,
        topic: topic || `${discipline} Sorusu`,
        fragmentText: fragmentText.trim(),
        author: author.trim() || currentUser?.displayName || 'Anonim Tıbbiyeli',
        authorUid: currentUser?.uid,
        authorStudentNumber: currentUser?.studentNumber || undefined,
        claimedAnswer: (claimedAnswer as any) || undefined,
        options: optionsPayload,
      });

      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl max-w-2xl w-full shadow-2xl border border-slate-200 overflow-hidden my-8">
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-700 to-emerald-700 text-white p-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center border border-white/20">
              <Stethoscope className="w-5 h-5 text-teal-100" />
            </div>
            <div>
              <h3 className="text-base font-bold">Soru / Şık Hatırlatma & Katkı Formu</h3>
              <p className="text-xs text-teal-100/90">
                Sınavda aklınızda kalan her küçük detay, sorunun tam halini yeniden inşa etmek için çok değerlidir.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-white/70 hover:text-white hover:bg-white/10 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-5 space-y-4 max-h-[75vh] overflow-y-auto">
          {/* Sınav ve Soru No */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Kurul / Sınav</label>
              <select
                value={committeeId}
                onChange={(e) => setCommitteeId(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs text-slate-800"
              >
                {committees.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Soru Numarası</label>
              <label className="flex items-center gap-1.5 p-1.5 rounded bg-teal-50 border border-teal-200 text-teal-900 text-xs font-semibold cursor-pointer mb-1.5 select-none">
                <input
                  type="checkbox"
                  checked={isUnknownNumber}
                  onChange={(e) => setIsUnknownNumber(e.target.checked)}
                  className="rounded border-slate-300 text-teal-600 focus:ring-teal-500"
                />
                <span>Numarayı hatırlamıyorum</span>
              </label>
              {!isUnknownNumber && (
                <input
                  type="number"
                  min={1}
                  max={selectedComm?.targetCount || 150}
                  value={questionNumber}
                  onChange={(e) => setQuestionNumber(Number(e.target.value))}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs font-bold text-teal-800"
                  required
                />
              )}
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Ders / Anabilim Dalı</label>
              <select
                value={discipline}
                onChange={(e) => setDiscipline(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs text-slate-800"
              >
                {activeDisciplines.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Konu / Başlık */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Konu / Hastalık / İlaç Başlığı
            </label>
            <input
              type="text"
              placeholder="Örnek: Myastenia Gravis, Digoksin Toksisitesi, Atipik Pnömoni..."
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 text-xs text-slate-800 placeholder:text-slate-400"
            />
          </div>

          {/* Aklında Kalan Soru Parçası */}
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="block text-xs font-bold text-slate-800">
                Aklınızda Kalan Soru Kökü, Vaka Hikayesi veya İpuçları *
              </label>
              <button
                type="button"
                onClick={handleQuickAiAssist}
                disabled={aiAssisting || !fragmentText.trim()}
                className="text-[11px] text-teal-700 hover:text-teal-800 font-semibold flex items-center gap-1 bg-teal-50 hover:bg-teal-100 px-2 py-0.5 rounded border border-teal-200 cursor-pointer disabled:opacity-40"
              >
                <Sparkles className="w-3 h-3 text-teal-600" />
                <span>{aiAssisting ? 'AI Analiz Ediyor...' : 'AI Soru Kalıbı Öner'}</span>
              </button>
            </div>
            <textarea
              rows={3}
              placeholder="Ör: 45 yaşında kadın hasta el bileklerinde ve MCP eklemlerinde sabah tutukluğu ile geliyor. RF pozitif, anti-CCP yüksek. Hoca ilk basamakta başlanacak DMARD ilacı hangisidir diye sormuştu..."
              value={fragmentText}
              onChange={(e) => setFragmentText(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-900 focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-teal-500/20 focus:border-teal-600"
              required
            />
          </div>

          {/* AI Quick Suggestion Preview */}
          {aiSuggestion && (
            <div className="bg-teal-50/70 border border-teal-200 rounded-lg p-3 text-xs space-y-1.5 animate-fadeIn">
              <span className="font-bold text-teal-900 flex items-center gap-1">
                <Sparkles className="w-3.5 h-3.5 text-teal-600" />
                Gemini Önerilen Soru Taslağı:
              </span>
              <p className="text-teal-950 font-serif italic">{aiSuggestion.suggestedStem}</p>
            </div>
          )}

          {/* Hatırlanan Şıklar */}
          <div className="space-y-2 pt-1 border-t border-slate-100">
            <span className="text-xs font-bold text-slate-700 block">
              Hatırladığınız Şıklar (A - E) (Bildiğiniz kadarını yazabilirsiniz)
            </span>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <div className="flex items-center gap-1.5">
                <span className="w-6 h-6 rounded bg-slate-200 text-slate-800 text-xs font-bold flex items-center justify-center shrink-0">
                  A
                </span>
                <input
                  type="text"
                  placeholder="A şıkkı metni..."
                  value={optionA}
                  onChange={(e) => setOptionA(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded px-2.5 py-1 text-xs"
                />
              </div>

              <div className="flex items-center gap-1.5">
                <span className="w-6 h-6 rounded bg-slate-200 text-slate-800 text-xs font-bold flex items-center justify-center shrink-0">
                  B
                </span>
                <input
                  type="text"
                  placeholder="B şıkkı metni..."
                  value={optionB}
                  onChange={(e) => setOptionB(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded px-2.5 py-1 text-xs"
                />
              </div>

              <div className="flex items-center gap-1.5">
                <span className="w-6 h-6 rounded bg-slate-200 text-slate-800 text-xs font-bold flex items-center justify-center shrink-0">
                  C
                </span>
                <input
                  type="text"
                  placeholder="C şıkkı metni..."
                  value={optionC}
                  onChange={(e) => setOptionC(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded px-2.5 py-1 text-xs"
                />
              </div>

              <div className="flex items-center gap-1.5">
                <span className="w-6 h-6 rounded bg-slate-200 text-slate-800 text-xs font-bold flex items-center justify-center shrink-0">
                  D
                </span>
                <input
                  type="text"
                  placeholder="D şıkkı metni..."
                  value={optionD}
                  onChange={(e) => setOptionD(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded px-2.5 py-1 text-xs"
                />
              </div>

              <div className="flex items-center gap-1.5 sm:col-span-2">
                <span className="w-6 h-6 rounded bg-slate-200 text-slate-800 text-xs font-bold flex items-center justify-center shrink-0">
                  E
                </span>
                <input
                  type="text"
                  placeholder="E şıkkı metni..."
                  value={optionE}
                  onChange={(e) => setOptionE(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded px-2.5 py-1 text-xs"
                />
              </div>
            </div>
          </div>

          {/* Doğru Olduğunu Düşündüğünüz Şık & İsim */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 border-t border-slate-100">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Sizce Doğru Cevap Hangi Şıktı?
              </label>
              <div className="flex items-center gap-2">
                {(['A', 'B', 'C', 'D', 'E'] as const).map((key) => (
                  <button
                    key={key}
                    type="button"
                    onClick={() => setClaimedAnswer(claimedAnswer === key ? '' : key)}
                    className={`w-7 h-7 rounded font-bold text-xs transition-colors cursor-pointer ${
                      claimedAnswer === key
                        ? 'bg-emerald-600 text-white'
                        : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                    }`}
                  >
                    {key}
                  </button>
                ))}
                {claimedAnswer && (
                  <span className="text-[11px] text-emerald-700 font-medium">Seçildi</span>
                )}
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Adınız / Rumuzunuz
              </label>
              <input
                type="text"
                placeholder="Örnek: Stj. Dr. Eren, Tıbbiyeli3"
                value={author}
                onChange={(e) => handleAuthorChange(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded px-3 py-1.5 text-xs text-slate-800"
              />
            </div>
          </div>

          {/* Footer CTA */}
          <div className="pt-4 border-t border-slate-100 flex items-center justify-end gap-2.5">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer"
            >
              Vazgeç
            </button>
            <button
              type="submit"
              disabled={isSubmitting || !fragmentText.trim()}
              className="bg-gradient-to-r from-teal-700 to-emerald-700 hover:from-teal-800 hover:to-emerald-800 text-white px-5 py-2 text-xs font-bold rounded-lg shadow-sm transition-all disabled:opacity-50 flex items-center gap-1.5 cursor-pointer active:scale-95"
            >
              <Send className="w-3.5 h-3.5" />
              <span>{isSubmitting ? 'Kaydediliyor...' : 'Hafıza Havuzuna Ekle'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
