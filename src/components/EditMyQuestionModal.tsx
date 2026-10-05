import React, { useState } from 'react';
import { 
  X, 
  Edit3, 
  History, 
  Save, 
  AlertCircle, 
  CheckCircle2, 
  HelpCircle,
  FileText,
  Sparkles,
  RefreshCw
} from 'lucide-react';
import { QuestionItem, Committee } from '../types';
import { AppUser } from '../services/auth';
import { ApiService } from '../services/api';

interface EditMyQuestionModalProps {
  isOpen: boolean;
  onClose: () => void;
  question: QuestionItem | null;
  committee: Committee | undefined;
  currentUser: AppUser | null;
  onSaveSuccess: (updatedQuestion: QuestionItem) => void;
  onOpenHistory: () => void;
}

export const EditMyQuestionModal: React.FC<EditMyQuestionModalProps> = (props) => {
  if (!props.isOpen || !props.question) return null;
  return <EditMyQuestionModalContent {...props} question={props.question} />;
};

const EditMyQuestionModalContent: React.FC<EditMyQuestionModalProps & { question: QuestionItem }> = ({
  onClose,
  question,
  committee,
  currentUser,
  onSaveSuccess,
  onOpenHistory,
}) => {
  const currentStem = question.reconstruction?.stem || question.fragments[0]?.text || '';
  const disciplines = committee?.disciplines && committee.disciplines.length > 0
    ? committee.disciplines
    : ['Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'Tıbbi Genetik', 'Enfeksiyon Hastalıkları', 'İç Hastalıkları'];

  const [stem, setStem] = useState(currentStem);
  const [discipline, setDiscipline] = useState(question.discipline || disciplines[0]);
  const [topic, setTopic] = useState(question.topic || '');
  const [claimedAnswer, setClaimedAnswer] = useState<'A' | 'B' | 'C' | 'D' | 'E' | undefined>(question.claimedAnswer);
  
  const getOpt = (k: 'A' | 'B' | 'C' | 'D' | 'E') => {
    return question.options.find((o) => o.key === k)?.text || '';
  };

  const [optA, setOptA] = useState(getOpt('A'));
  const [optB, setOptB] = useState(getOpt('B'));
  const [optC, setOptC] = useState(getOpt('C'));
  const [optD, setOptD] = useState(getOpt('D'));
  const [optE, setOptE] = useState(getOpt('E'));

  const [changeSummary, setChangeSummary] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [isAiOptimizing, setIsAiOptimizing] = useState(false);
  const [aiBannerMsg, setAiBannerMsg] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAutoOptimizeWithAi = async () => {
    setIsAiOptimizing(true);
    setError(null);
    setAiBannerMsg(null);
    try {
      const res = await ApiService.optimizeQuestionWithAi({ question });
      if (res.success && res.optimizedQuestion) {
        const opt = res.optimizedQuestion;
        if (opt.discipline) setDiscipline(opt.discipline);
        if (opt.topic) setTopic(opt.topic);
        if (opt.stem) setStem(opt.stem);
        if (opt.options && Array.isArray(opt.options)) {
          const a = opt.options.find((o) => o.key === 'A')?.text || '';
          const b = opt.options.find((o) => o.key === 'B')?.text || '';
          const c = opt.options.find((o) => o.key === 'C')?.text || '';
          const d = opt.options.find((o) => o.key === 'D')?.text || '';
          const e = opt.options.find((o) => o.key === 'E')?.text || '';
          if (a) setOptA(a);
          if (b) setOptB(b);
          if (c) setOptC(c);
          if (d) setOptD(d);
          if (e) setOptE(e);
        }
        if (opt.correctAnswer) setClaimedAnswer(opt.correctAnswer as any);
        setChangeSummary(res.refinementSummary || 'Yapay zeka ve amfi ders notu zeminlemesi ile düzenlendi');
        const lectureTitle = res.matchedLecture ? `("${res.matchedLecture.noteTitle}", Slayt #${res.matchedLecture.pageNumber})` : 'tıp literatürü';
        setAiBannerMsg(`✓ Yapay zeka amfi ders notları ${lectureTitle} zeminlemesiyle tüm alanları otomatik düzenledi.`);
      } else {
        setError(res.error || 'Yapay zeka soru düzenleyemedi.');
      }
    } catch (e: any) {
      setError(e.message || 'Yapay zeka optimizasyonu sırasında bir hata oluştu.');
    } finally {
      setIsAiOptimizing(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentUser) {
      setError('Düzenleme yapmak için giriş yapmış olmalısınız.');
      return;
    }

    setIsSaving(true);
    setError(null);
    try {
      const optionsList: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string }[] = [];
      if (optA.trim()) optionsList.push({ key: 'A', text: optA.trim() });
      if (optB.trim()) optionsList.push({ key: 'B', text: optB.trim() });
      if (optC.trim()) optionsList.push({ key: 'C', text: optC.trim() });
      if (optD.trim()) optionsList.push({ key: 'D', text: optD.trim() });
      if (optE.trim()) optionsList.push({ key: 'E', text: optE.trim() });

      const updated = await ApiService.editUserQuestion({
        questionId: question.id,
        editorUid: currentUser.uid,
        editorName: currentUser.displayName || 'Öğrenci',
        editorStudentNumber: currentUser.studentNumber || undefined,
        stem: stem.trim(),
        discipline,
        topic: topic.trim() || question.topic,
        claimedAnswer,
        options: optionsList,
        changeSummary: changeSummary.trim() || 'Soru kökü ve şıkları güncellendi',
      });

      onSaveSuccess(updated);
      onClose();
    } catch (err: any) {
      setError(err.message || 'Güncelleme kaydedilemedi.');
    } finally {
      setIsSaving(false);
    }
  };

  const revisionCount = question.revisions?.length || 0;

  return (
    <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-fadeIn">
      <div 
        className="ms-modal-panel bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-2xl max-h-[90dvh] flex flex-col overflow-hidden relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-ink-surface p-5 text-white flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-white/10 text-teal-300">
              <Edit3 className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-base leading-tight">
                  Soruyu Düzenle {question.isUnassignedNumber ? '(Numarasız Havuz)' : `(#${question.questionNumber})`}
                </h3>
                <span className="text-[11px] font-bold bg-teal-500/20 text-teal-200 px-2 py-0.5 rounded-full border border-teal-400/30">
                  {revisionCount > 0 ? `${revisionCount} Versiyon` : 'İlk Versiyon'}
                </span>
              </div>
              <p className="text-xs text-teal-200/80">
                {committee?.name || 'Kurul Sınavı'}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleAutoOptimizeWithAi}
              disabled={isAiOptimizing}
              className="bg-teal-500/20 hover:bg-teal-500/30 text-teal-200 border border-teal-400/40 px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer shadow-2xs"
              title="Amfi ders notları ve tıp literatürüyle bu soruyu yapay zeka ile otomatik doldur"
            >
              {isAiOptimizing ? (
                <RefreshCw className="w-3.5 h-3.5 animate-spin text-teal-300" />
              ) : (
                <Sparkles className="w-3.5 h-3.5 text-teal-300" />
              )}
              <span>{isAiOptimizing ? 'İnceleniyor...' : 'AI ile Otomatik Düzenle'}</span>
            </button>

            {revisionCount > 0 && (
              <button
                type="button"
                onClick={onOpenHistory}
                className="bg-white/10 hover:bg-white/20 text-teal-100 px-2.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
              >
                <History className="w-3.5 h-3.5 text-teal-300" />
                <span>Eski Versiyonlar</span>
              </button>
            )}
            <button
              onClick={onClose}
              className="p-1 rounded-lg text-white/70 hover:text-white hover:bg-white/10 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Notice Banner */}
        <div className="bg-emerald-50 border-b border-emerald-200 px-5 py-2.5 text-xs text-emerald-900 flex items-center gap-2 shrink-0">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>
            <strong>Güvenli Versiyonlama:</strong> Yaptığınız düzenleme yeni bir versiyon olarak eklenir, sorunun eski halleri silinmez ve arşivde korunur.
          </span>
        </div>

        {/* AI Banner Message if generated */}
        {aiBannerMsg && (
          <div className="bg-teal-50 border-b border-teal-200 px-5 py-2.5 text-xs text-teal-900 flex items-center gap-2 shrink-0 animate-fadeIn">
            <Sparkles className="w-4 h-4 text-teal-600 shrink-0" />
            <span>{aiBannerMsg}</span>
          </div>
        )}

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 overflow-y-auto space-y-4 flex-1">
          {error && (
            <div className="bg-rose-50 border border-rose-200 text-rose-800 text-xs p-3 rounded-lg flex items-start gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Branş / Ders
              </label>
              <select
                value={discipline}
                onChange={(e) => setDiscipline(e.target.value)}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600 bg-white"
              >
                {disciplines.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Konu Başlığı
              </label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Örn: Akut Glomerülonefrit Patolojisi"
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">
              Soru Metni / Kökü
            </label>
            <textarea
              rows={4}
              required
              value={stem}
              onChange={(e) => setStem(e.target.value)}
              placeholder="Hatırladığınız soru kökünü yazınız..."
              className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600 font-sans leading-relaxed"
            />
          </div>

          {/* Options */}
          <div className="space-y-2 pt-2 border-t border-slate-100">
            <label className="block text-xs font-bold text-slate-700">
              Şıklar (A - E) ve Doğru Şık Seçimi
            </label>
            
            {[
              { key: 'A', val: optA, set: setOptA },
              { key: 'B', val: optB, set: setOptB },
              { key: 'C', val: optC, set: setOptC },
              { key: 'D', val: optD, set: setOptD },
              { key: 'E', val: optE, set: setOptE },
            ].map(({ key, val, set }) => (
              <div key={key} className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setClaimedAnswer(claimedAnswer === key ? undefined : (key as any))}
                  className={`w-7 h-7 rounded-lg text-xs font-bold shrink-0 transition-colors flex items-center justify-center cursor-pointer ${
                    claimedAnswer === key
                      ? 'bg-emerald-600 text-white shadow-xs'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                  title={claimedAnswer === key ? 'Doğru şık seçili' : 'Doğru şık olarak işaretle'}
                >
                  {key}
                </button>
                <input
                  type="text"
                  value={val}
                  onChange={(e) => set(e.target.value)}
                  placeholder={`${key} şıkkı metni...`}
                  className={`flex-1 px-3 py-1.5 text-xs border rounded-lg focus:outline-hidden focus:border-teal-600 ${
                    claimedAnswer === key ? 'border-emerald-400 bg-emerald-50/30' : 'border-slate-300'
                  }`}
                />
              </div>
            ))}
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">
              Değişiklik Notu / Özeti <span className="text-slate-400 font-normal">(Neyi düzelttiğinizi belirtin)</span>
            </label>
            <input
              type="text"
              value={changeSummary}
              onChange={(e) => setChangeSummary(e.target.value)}
              placeholder="Örn: Soru kökündeki semptomu düzelttim ve C şıkkını tamamladım"
              className="w-full px-3 py-2 text-xs border border-slate-300 rounded-lg focus:outline-hidden focus:border-teal-600"
            />
          </div>

          <div className="pt-3 border-t border-slate-200 flex items-center justify-between">
            <button
              type="button"
              onClick={onOpenHistory}
              className="text-xs text-teal-700 hover:text-teal-900 font-semibold flex items-center gap-1 cursor-pointer"
            >
              <History className="w-3.5 h-3.5" />
              <span>Versiyon Geçmişini Görüntüle ({revisionCount})</span>
            </button>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-800 hover:bg-slate-100 rounded-lg cursor-pointer"
              >
                Vazgeç
              </button>
              <button
                type="submit"
                disabled={isSaving}
                className="bg-teal-700 hover:bg-teal-800 text-white font-bold px-5 py-2 rounded-lg text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer disabled:opacity-50"
              >
                <Save className="w-4 h-4" />
                <span>{isSaving ? 'Kaydediliyor...' : 'Güncellemeyi Kaydet'}</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};
