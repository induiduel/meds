import React, { useState } from 'react';
import {
  Sparkles,
  Zap,
  CheckCircle2,
  AlertCircle,
  Copy,
  Check,
  RefreshCw,
  X,
  Stethoscope,
  BookOpen,
  ArrowRight,
  ChevronDown,
  Layers,
  GraduationCap
} from 'lucide-react';
import { QuestionItem } from '../types';
import { safeJsonFetch } from '../services/api';

interface AdvancedQuestionUpgradeModalProps {
  question: QuestionItem;
  isOpen: boolean;
  onClose: () => void;
  onSaveUpgraded?: (questionId: string, advancedData: any) => void;
}

export const AdvancedQuestionUpgradeModal: React.FC<AdvancedQuestionUpgradeModalProps> = ({
  question,
  isOpen,
  onClose,
  onSaveUpgraded,
}) => {
  const [selectedModel, setSelectedModel] = useState<string>('gemini-3.8-flash');
  const [isGenerating, setIsGenerating] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [advancedResult, setAdvancedResult] = useState<any>(question.advancedQuestion || null);
  const [copied, setCopied] = useState(false);
  const [activeTab, setActiveTab] = useState<'comparison' | 'advanced'>('comparison');

  if (!isOpen) return null;

  const rawStem = question.rawQuestion?.stem || question.rawStem || question.fragments?.[0]?.text || '';
  const rawOptions = question.rawQuestion?.options || question.options || [];
  const recStem = question.reconstruction?.stem || question.stem || '';
  const recOptions = question.reconstruction?.options || question.options || [];

  const handleGenerateAdvanced = async () => {
    setIsGenerating(true);
    setErrorMsg(null);

    try {
      const res = await safeJsonFetch<any>('/api/ai/upgrade-advanced-question', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          questionId: question.id,
          question,
          model: selectedModel,
          preferredProvider: selectedModel.includes('deepseek') || selectedModel.includes('llama') ? 'groq' : 'auto'
        })
      });

      const data = res.data;
      if (!res.ok || !data?.success) {
        throw new Error(data?.error || res.error || 'Gelişmiş soru üretilemedi.');
      }

      setAdvancedResult(data.advancedQuestion);
      setActiveTab('advanced');
      if (onSaveUpgraded) {
        onSaveUpgraded(question.id, data.advancedQuestion);
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Bir hata oluştu.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="ms-overlay fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="ms-modal-panel bg-white rounded-2xl max-w-4xl w-full max-h-[92dvh] shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="p-5 border-b border-line bg-ink-surface text-white flex items-center justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-full bg-warn/20 text-warn border border-warn/30 text-2xs font-bold flex items-center gap-1">
                <Zap className="w-3 h-3 text-warn" />
                İleri Düzey Vaka Dönüştürücü
              </span>
              <span className="text-xs text-ink-3">
                {question.discipline} · {question.committeeId}
              </span>
            </div>
            <h2 className="text-lg sm:text-xl font-bold">
              Soruyu Çok Basamaklı Klinik Vaka Sorusuna Dönüştür
            </h2>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-ink-3 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation Tabs */}
        <div className="flex items-center border-b border-line bg-field px-5 gap-3">
          <button
            onClick={() => setActiveTab('comparison')}
            className={`py-3 text-xs sm:text-sm font-semibold border-b-2 transition-colors ${
              activeTab === 'comparison'
                ? 'border-accent text-accent'
                : 'border-transparent text-ink-3 hover:text-ink'
            }`}
          >
            1. Eski Soru & Redakte Soru Eşleşmesi
          </button>
          <button
            onClick={() => setActiveTab('advanced')}
            className={`py-3 text-xs sm:text-sm font-semibold border-b-2 transition-colors flex items-center gap-1.5 ${
              activeTab === 'advanced'
                ? 'border-accent text-accent'
                : 'border-transparent text-ink-3 hover:text-ink'
            }`}
          >
            <Sparkles className="w-4 h-4 text-warn" />
            2. Gelişmiş Klinik Vaka Sorusu
            {advancedResult && <span className="w-2 h-2 rounded-full bg-ok" />}
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto flex-1 space-y-6">
          {activeTab === 'comparison' ? (
            <div className="space-y-5">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Sol: Eski / Ham Soru */}
                <div className="bg-field border border-line rounded-xl p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold uppercase tracking-wider text-ink-3 flex items-center gap-1.5">
                      <GraduationCap className="w-4 h-4 text-ink-3" />
                      Eski / Ham Soru (Öğrenci Hafızası)
                    </span>
                    <span className="text-2xs bg-line text-ink-2 px-2 py-0.5 rounded font-mono">
                      {question.examYear || 'Çıkmış'}
                    </span>
                  </div>
                  <p className="text-sm text-ink font-medium leading-relaxed">
                    {rawStem || 'Ham soru metni kayıtlı değil.'}
                  </p>
                  <div className="space-y-1.5 pt-2 border-t border-line/60 text-xs text-ink-2">
                    {rawOptions.map((o: any, i: number) => (
                      <div key={i} className="flex gap-2">
                        <span className="font-bold text-ink-3">{typeof o === 'string' ? '' : `${o.key || o.label})`}</span>
                        <span>{typeof o === 'string' ? o : o.text}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Sağ: Redakte Edilmiş Kurul Sorusu */}
                <div className="bg-accent-soft/50 border border-accent/30 rounded-xl p-4 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold uppercase tracking-wider text-accent flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-ok" />
                      Redakte Edilmiş Kurul Sorusu
                    </span>
                    <span className="text-2xs bg-ok-soft text-ok border border-ok/30 px-2 py-0.5 rounded font-semibold">
                      Doğru: {question.reconstruction?.correctAnswer || question.claimedAnswer || '?'}
                    </span>
                  </div>
                  <p className="text-sm text-ink font-medium leading-relaxed">
                    {recStem || 'Redakte soru metni henüz oluşturulmamış.'}
                  </p>
                  <div className="space-y-1.5 pt-2 border-t border-accent/60 text-xs">
                    {recOptions.map((o: any, i: number) => {
                      const key = typeof o === 'string' ? '' : (o.key || o.label);
                      const isCorrect = key === (question.reconstruction?.correctAnswer || question.claimedAnswer);
                      return (
                        <div key={i} className={`flex gap-2 p-1.5 rounded ${isCorrect ? 'bg-ok-soft/70 text-ok font-semibold' : 'text-ink-2'}`}>
                          <span className="font-bold">{key ? `${key})` : ''}</span>
                          <span>{typeof o === 'string' ? o : o.text}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* Generation Controls */}
              <div className="bg-ink-surface text-white rounded-xl p-5 space-y-4">
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <h3 className="font-bold text-sm flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-warn" />
                      Yapay Zeka ile İleri Düzey Soruya Dönüştür
                    </h3>
                    <p className="text-xs text-ink-3">
                      Bu soruyu amfi notları, redakte özetler ve toplanan DeepSeek verilerini referans alarak USMLE / TUS formatında çok basamaklı bir vakaya çevirir.
                    </p>
                  </div>

                  <div className="flex items-center gap-2 w-full sm:w-auto">
                    <select
                      value={selectedModel}
                      onChange={(e) => setSelectedModel(e.target.value)}
                      className="bg-ink border border-line-2 rounded-lg text-xs text-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-accent"
                    >
                      <option value="gemini-3.8-flash">Google Gemini 3.8 Flash</option>
                      <option value="deepseek-r1-distill-llama-70b">Groq DeepSeek R1 70B (Akıl Yürütme)</option>
                      <option value="llama-3.3-70b-versatile">Groq Llama 3.3 70B</option>
                    </select>

                    <button
                      onClick={handleGenerateAdvanced}
                      disabled={isGenerating}
                      className="px-4 py-2 bg-accent hover:bg-accent disabled:bg-accent text-white font-bold text-xs rounded-lg transition-colors flex items-center gap-2 shrink-0 shadow-md"
                    >
                      {isGenerating ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Zap className="w-4 h-4 text-warn" />}
                      {isGenerating ? 'Dönüştürülüyor…' : 'Gelişmiş Soru Üret'}
                    </button>
                  </div>
                </div>

                {errorMsg && (
                  <div className="p-3 bg-bad/20 border border-bad/40 rounded-lg text-bad-soft text-xs flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 text-bad-text shrink-0" />
                    <span>{errorMsg}</span>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {!advancedResult ? (
                <div className="text-center py-12 space-y-3">
                  <Stethoscope className="w-10 h-10 text-ink-3 mx-auto" />
                  <p className="text-ink-2 text-sm font-medium">Henüz gelişmiş soru üretilmedi.</p>
                  <button
                    onClick={handleGenerateAdvanced}
                    disabled={isGenerating}
                    className="px-4 py-2 bg-accent hover:bg-accent text-white font-semibold text-xs rounded-lg inline-flex items-center gap-2 transition-colors"
                  >
                    {isGenerating ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                    Şimdi Gelişmiş Soru Üret
                  </button>
                </div>
              ) : (
                <div className="space-y-5">
                  {/* Klinik Senaryo */}
                  <div className="bg-warn-soft/70 border border-warn/80 rounded-xl p-5 space-y-2">
                    <span className="text-2xs font-bold text-warn uppercase tracking-wider flex items-center gap-1.5">
                      <Stethoscope className="w-4 h-4 text-warn" />
                      Klinik Vaka Senaryosu
                    </span>
                    <p className="text-sm text-ink leading-relaxed font-medium">
                      {advancedResult.clinicalScenario}
                    </p>
                  </div>

                  {/* Soru Kökü */}
                  <div className="bg-white border-2 border-accent/30 rounded-xl p-5 space-y-2 shadow-xs">
                    <span className="text-2xs font-bold text-accent uppercase tracking-wider">
                      Soru Kökü
                    </span>
                    <p className="text-base text-ink font-bold leading-snug">
                      {advancedResult.stem}
                    </p>
                  </div>

                  {/* Şıklar ve Çeldirici Analizleri */}
                  <div className="space-y-2.5">
                    <span className="text-xs font-bold text-ink-2 uppercase tracking-wider block">
                      Seçenekler & Çeldirici Analizi
                    </span>
                    {advancedResult.options?.map((opt: any) => {
                      const isCorrect = opt.key === advancedResult.correctAnswer || opt.isCorrect;
                      return (
                        <div
                          key={opt.key}
                          className={`p-3.5 rounded-xl border transition-all ${
                            isCorrect
                              ? 'bg-ok-soft border-ok/30 ring-2 ring-ok/20'
                              : 'bg-white border-line'
                          }`}
                        >
                          <div className="flex items-start justify-between gap-3">
                            <div className="flex items-start gap-2.5">
                              <span className={`w-6 h-6 rounded-md flex items-center justify-center text-xs font-bold shrink-0 ${
                                isCorrect ? 'bg-ok text-white' : 'bg-field text-ink-2'
                              }`}>
                                {opt.key}
                              </span>
                              <span className={`text-sm ${isCorrect ? 'font-bold text-ok' : 'text-ink'}`}>
                                {opt.text}
                              </span>
                            </div>
                            {isCorrect && (
                              <span className="px-2 py-0.5 rounded text-2xs font-bold bg-ok/20 text-ok shrink-0">
                                Doğru Cevap
                              </span>
                            )}
                          </div>
                          {opt.rationale && (
                            <p className="mt-2 text-xs text-ink-3 pl-8.5 border-l border-line">
                              {opt.rationale}
                            </p>
                          )}
                        </div>
                      );
                    })}
                  </div>

                  {/* Tıbbi Çözüm & Klinik Pearl */}
                  <div className="bg-accent text-white rounded-xl p-5 space-y-4">
                    <div className="space-y-1.5">
                      <span className="text-xs font-bold uppercase tracking-wider text-accent flex items-center gap-1.5">
                        <BookOpen className="w-4 h-4 text-accent" />
                        Akademik Çözüm & Patofizyoloji
                      </span>
                      <p className="text-xs sm:text-sm text-ink-3 leading-relaxed whitespace-pre-line">
                        {advancedResult.explanation}
                      </p>
                    </div>

                    {advancedResult.clinicalPearl && (
                      <div className="p-3 bg-warn/10 border border-warn/30 rounded-lg text-warn-soft text-xs flex items-start gap-2">
                        <Sparkles className="w-4 h-4 text-warn shrink-0 mt-0.5" />
                        <div>
                          <strong className="block text-warn font-bold mb-0.5">Klinik İnci / Altın İpucu:</strong>
                          {advancedResult.clinicalPearl}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-line bg-field flex items-center justify-between text-xs">
          <div className="flex items-center gap-2">
            {advancedResult && (
              <button
                onClick={() => handleCopy(JSON.stringify(advancedResult, null, 2))}
                className="px-3 py-1.5 rounded-lg border border-line bg-white hover:bg-field text-ink-2 font-semibold flex items-center gap-1.5 transition-colors"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-ok" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? 'Kopyalandı' : 'JSON Kopyala'}
              </button>
            )}
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-ink text-white rounded-lg font-semibold hover:bg-ink transition-colors"
            >
              Kapat
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
