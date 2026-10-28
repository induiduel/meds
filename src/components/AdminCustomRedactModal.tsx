import React, { useState } from 'react';
import {
  Sparkles,
  X,
  CheckCircle2,
  AlertTriangle,
  BookOpen,
  FileText,
  RefreshCw,
  Sliders,
  Check,
  Lock,
} from 'lucide-react';
import { QuestionItem, ReconstructedQuestion } from '../types';
import { YonetimApi } from '../services/api/yonetim';
import { ADMIN_EMAIL } from '../services/auth';

interface AdminCustomRedactModalProps {
  question: QuestionItem | null;
  isOpen: boolean;
  onClose: () => void;
  onSaved: (updatedQuestion: QuestionItem) => void;
  matchedSlideNote?: {
    noteTitle: string;
    pageNumber: number;
    snippet: string;
  } | null;
}

const PROMPT_SUGGESTIONS = [
  'Soru kökü ve şıklardaki yazım/harf hatalarını düzelt ve profesyonel sınav diline getir.',
  'Soru kökünü "aşağıdakilerden hangisi DEĞİLDİR / YANLIŞTIR" şeklinde olumsuz soruya dönüştür ve seçenekleri buna göre uyarla.',
  'Bu soruyu Robbins Temel Patoloji tıp kitabındaki TUS/USMLE formatında 5 şıklı klinik vaka sorusuna dönüştür.',
  'Amfi ders notunda vurgulanan fizyopatolojik mekanizmayı sorgulayacak şekilde soru kökünü ve çeldiricileri revize et.',
  'Çeldiricileri (şıkları) birbirini dışlayan ve ayırıcı tanı gerektiren güçlü tıp seçenekleriyle 5 şık olarak tamamla.',
  'Pediatrik / geriatrik hasta öyküsü, vital bulgular ve laboratuvar parametreleri (WBC, CRP vb.) ekleyerek senaryolaştır.',
  'Soru kökünü ve doğru cevabı koruyarak, şıkları TUS soru standardında alfabetik/mantıksal sıraya ve klinik dile göre dengele.'
];

export const AdminCustomRedactModal: React.FC<AdminCustomRedactModalProps> = ({
  question,
  isOpen,
  onClose,
  onSaved,
  matchedSlideNote
}) => {
  if (!isOpen || !question) return null;

  const currentRecon = question.reconstruction;
  const initialStem = currentRecon?.stem || (question as any).rawQuestion?.stem || question.fragments?.[0]?.text || question.topic || '';
  const initialOptions = currentRecon?.options || (question as any).rawQuestion?.options || question.options || [
    { key: 'A', text: '', isAiFilled: false },
    { key: 'B', text: '', isAiFilled: false },
    { key: 'C', text: '', isAiFilled: false },
    { key: 'D', text: '', isAiFilled: false },
    { key: 'E', text: '', isAiFilled: false },
  ];
  const initialCorrect = currentRecon?.correctAnswer || question.claimedAnswer || 'A';
  const initialExplanation = currentRecon?.explanation || '';

  // Prompt Form States
  const [customPrompt, setCustomPrompt] = useState('');
  const [includeSlideGrounding, setIncludeSlideGrounding] = useState(true);
  const [selectedModel, setSelectedModel] = useState('gemini-3.8-flash');
  const [isGenerating, setIsGenerating] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Editable Draft States
  const [draftStem, setDraftStem] = useState(initialStem);
  const [draftOptions, setDraftOptions] = useState<{ key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string; isAiFilled: boolean }[]>(
    ['A', 'B', 'C', 'D', 'E'].map(k => {
      const existing = initialOptions.find((o: any) => o.key === k);
      return {
        key: k as any,
        text: existing?.text || '',
        isAiFilled: Boolean(existing?.isAiFilled || existing?.isAiGenerated)
      };
    })
  );
  const [draftCorrectAnswer, setDraftCorrectAnswer] = useState<'A' | 'B' | 'C' | 'D' | 'E'>(initialCorrect as any);
  const [draftExplanation, setDraftExplanation] = useState(initialExplanation);
  const [draftNotes, setDraftNotes] = useState(currentRecon?.notesAndDiscrepancies || '');
  const [isSaving, setIsSaving] = useState(false);
  const [hasGeneratedOnce, setHasGeneratedOnce] = useState(false);

  // Is locked by 90%+ student approval
  const isStudentLocked = (question.upvotes || 0) >= 10 && (!question.reports || question.reports.length === 0);

  const handleApplySuggestion = (suggestion: string) => {
    setCustomPrompt(prev => prev ? `${prev}\n\n${suggestion}` : suggestion);
  };

  const handleGenerate = async () => {
    if (!customPrompt.trim()) {
      setErrorMsg('Lütfen yapay zekaya nasıl bir redaksiyon yapmasını istediğinizi belirten bir talimat girin.');
      return;
    }

    setIsGenerating(true);
    setErrorMsg(null);

    try {
      const groundingText = includeSlideGrounding && matchedSlideNote
        ? `Ders Notu: ${matchedSlideNote.noteTitle} (Sayfa #${matchedSlideNote.pageNumber})\nSlayt Özeti: ${matchedSlideNote.snippet}`
        : undefined;

      const customApiKey = localStorage.getItem('medsoru_gemini_api_key') || localStorage.getItem('medsoru_custom_gemini_key') || undefined;
      const groqApiKey = localStorage.getItem('medsoru_groq_api_key') || undefined;
      const isGroq = selectedModel.includes('llama') || selectedModel.includes('deepseek');

      const res = await YonetimApi.adminCustomRedactQuestion({
        question,
        customPrompt: customPrompt.trim(),
        groundingNote: groundingText,
        model: selectedModel,
        adminEmail: ADMIN_EMAIL,
        apiKey: customApiKey,
        groqApiKey,
        preferredProvider: isGroq ? 'groq' : 'auto',
      });

      if (res.success && res.reconstruction) {
        setDraftStem(res.reconstruction.stem);
        setDraftOptions(res.reconstruction.options as any);
        setDraftCorrectAnswer(res.reconstruction.correctAnswer);
        setDraftExplanation(res.reconstruction.explanation);
        setDraftNotes(res.reconstruction.notesAndDiscrepancies || 'Admin özel redaksiyonu tamamlandı.');
        setHasGeneratedOnce(true);
      } else {
        setErrorMsg(res.error || 'Yapay zeka redaksiyonu üretirken bir sorun oluştu.');
      }
    } catch (e: any) {
      setErrorMsg('Hata: ' + e.message);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSave = async () => {
    setIsSaving(true);
    setErrorMsg(null);
    try {
      const updatedReconstruction: ReconstructedQuestion = {
        stem: draftStem.trim(),
        options: draftOptions.map(o => ({
          key: o.key,
          text: o.text.trim(),
          isAiFilled: o.isAiFilled
        })),
        correctAnswer: draftCorrectAnswer,
        explanation: draftExplanation.trim(),
        confidenceScore: currentRecon?.confidenceScore || 96,
        notesAndDiscrepancies: draftNotes || `Admin özel talimatı (${customPrompt.slice(0, 50)}...) ile redakte edildi.`,
        lastUpdated: new Date().toISOString()
      };

      const updatedQuestion: QuestionItem = {
        ...question,
        status: 'completed',
        claimedAnswer: draftCorrectAnswer,
        reconstruction: updatedReconstruction,
        isLocked: isStudentLocked || true,
        customRedactedBy: ADMIN_EMAIL,
        customRedactedAt: new Date().toISOString(),
        customRedactionPrompt: customPrompt,
        updatedAt: new Date().toISOString()
      };

      // Save approved question directly across all databases (Local Server + Supabase + Firebase Spark)
      await YonetimApi.saveApprovedPastQuestion(updatedQuestion);

      onSaved(updatedQuestion);
      onClose();
    } catch (err: any) {
      setErrorMsg('Kaydedilemedi: ' + err.message);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-[var(--color-scrim)] overflow-y-auto animate-fadeIn">
      <div className="ms-modal-panel bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[92dvh] flex flex-col border border-line overflow-hidden">
        
        {/* Header */}
        <div className="p-4 sm:p-5 bg-ink-surface text-white flex items-center justify-between shrink-0">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="p-1.5 bg-ok/60 rounded-lg">
                <Sparkles className="w-5 h-5 text-ok-soft" />
              </span>
              <h2 className="text-base sm:text-lg font-bold">
                Yapay Zeka ile Özel Soru Redaksiyonu (Admin)
              </h2>
            </div>
            <p className="text-xs text-ok-soft flex flex-wrap items-center gap-2">
              <span>Kurul: <strong>{question.committeeId}</strong></span>
              <span>•</span>
              <span>Disiplin: <strong>{question.discipline}</strong></span>
              <span>•</span>
              <span>Konu: <strong>{question.topic}</strong></span>
              {isStudentLocked && (
                <span className="inline-flex items-center gap-1 bg-warn text-warn font-extrabold px-2 py-0.5 rounded-full text-2xs">
                  <Lock className="w-3 h-3" />
                  %90+ Öğrenci Onaylı Soru (Yalnızca Admin Değiştirebilir)
                </span>
              )}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-ok-soft hover:text-white rounded-lg hover:bg-white/10 transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-5">
          
          {/* Soru Kaynak & Ham Metin Önizlemesi */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            <div className="bg-field border border-line rounded-xl p-3.5 space-y-1.5">
              <div className="flex items-center justify-between font-bold text-ink-2 border-b border-line pb-1">
                <span className="flex items-center gap-1.5">
                  <FileText className="w-3.5 h-3.5 text-ink-3" />
                  Orijinal Ham Soru Metni
                </span>
                <span className="text-2xs text-ink-3 bg-white px-1.5 py-0.5 rounded border border-line">
                  {question.sourceFile || 'PDF Kaynağı'}
                </span>
              </div>
              <p className="text-ink leading-relaxed font-sans max-h-28 overflow-y-auto pr-1">
                {(question as any).rawQuestion?.stem || question.fragments?.[0]?.text || question.rawStem || question.topic}
              </p>
            </div>

            {matchedSlideNote ? (
              <div className="bg-ok-soft/60 border border-ok/30 rounded-xl p-3.5 space-y-1.5">
                <div className="flex items-center justify-between font-bold text-ok border-b border-ok/30 pb-1">
                  <span className="flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-ok" />
                    Amfi Slayt Bağlamı (#{matchedSlideNote.pageNumber})
                  </span>
                  <label className="flex items-center gap-1 text-2xs text-ok font-semibold cursor-pointer">
                    <input
                      type="checkbox"
                      checked={includeSlideGrounding}
                      onChange={(e) => setIncludeSlideGrounding(e.target.checked)}
                      className="rounded text-ok focus:ring-ok"
                    />
                    <span>İsteme Dahil Et</span>
                  </label>
                </div>
                <p className="text-ok leading-relaxed max-h-28 overflow-y-auto pr-1">
                  <strong>{matchedSlideNote.noteTitle}:</strong> {matchedSlideNote.snippet}
                </p>
              </div>
            ) : (
              <div className="bg-field border border-line rounded-xl p-3.5 flex items-center justify-center text-ink-3 italic">
                Bu soruyla doğrudan eşleşen amfi slaytı bulunamadı (Genel Tıp literatürü kullanılacak).
              </div>
            )}
          </div>

          {/* Admin Custom Redaction Prompt Input */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-xs sm:text-sm font-bold text-ink flex items-center gap-1.5">
                <Sliders className="w-4 h-4 text-ok" />
                <span>Yapay Zekaya Özel Redaksiyon Talimatınız:</span>
              </label>
              <div className="flex items-center gap-2">
                <span className="text-2xs font-semibold text-ink-3">Yapay Zeka Modeli:</span>
                <select
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                  className="bg-field border border-line-2 rounded-md px-2 py-0.5 text-xs font-semibold text-ink"
                >
                  <optgroup label="Google Gemini">
                    <option value="gemini-3.8-flash">Gemini 3.8 Flash (Otomatik Çok Kademeli Havuz)</option>
                    <option value="gemini-2.5-pro">Gemini 2.5 Pro (Gelişmiş Tıbbi Mantık)</option>
                  </optgroup>
                  <optgroup label="Groq Cloud (Ücretsiz & Limitsiz)">
                    <option value="llama-3.3-70b-versatile">Groq Llama 3.3 70B (Çok Hızlı & Kota Bağımsız)</option>
                    <option value="deepseek-r1-distill-llama-70b">Groq DeepSeek R1 70B (Derin Akıl Yürütme)</option>
                  </optgroup>
                </select>
              </div>
            </div>

            <textarea
              rows={3}
              value={customPrompt}
              onChange={(e) => setCustomPrompt(e.target.value)}
              placeholder="Örn: Bu soruyu Robbins Temel Patoloji kitabındaki gibi 5 şıklı klinik vaka sorusuna çevir. Şıklara tipik çeldiriciler ekle, doğru cevabı açıkla..."
              className="w-full bg-field border border-line-2 rounded-xl p-3 text-xs sm:text-sm text-ink focus:bg-white focus:border-ok focus:ring-1 focus:ring-ok leading-relaxed"
            />

            {/* Prompt Quick Chips */}
            <div className="space-y-1">
              <span className="text-2xs font-semibold text-ink-3">Hızlı Şablon İstemler:</span>
              <div className="flex flex-wrap gap-1.5">
                {PROMPT_SUGGESTIONS.map((s, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleApplySuggestion(s)}
                    className="text-2xs bg-field hover:bg-ok-soft hover:text-ok border border-line hover:border-ok/30 rounded-lg px-2.5 py-1 text-ink-2 transition-colors text-left cursor-pointer"
                  >
                    + {s.substring(0, 48)}...
                  </button>
                ))}
              </div>
            </div>

            {/* Run AI Button */}
            <div className="pt-1 flex items-center justify-end">
              <button
                type="button"
                onClick={handleGenerate}
                disabled={isGenerating || !customPrompt.trim()}
                className="bg-accent hover:from-ok hover:to-accent text-white font-bold text-xs sm:text-sm px-4 py-2.5 rounded-xl shadow-md flex items-center gap-2 transition-all disabled:opacity-50 cursor-pointer"
              >
                {isGenerating ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin text-ok-soft" />
                    <span>Yapay Zeka ile Redakte Ediliyor...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 text-ok-soft" />
                    <span>Yapay Zeka ile Yeniden Redakte Et</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {errorMsg && (
            <div className="p-3 bg-bad-soft border border-bad/30 rounded-xl text-xs text-bad-text flex items-start gap-2">
              <AlertTriangle className="w-4 h-4 text-bad-text shrink-0 mt-0.5" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Result Review & Editable Form */}
          <div className="border-t border-line pt-4 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-xs sm:text-sm font-bold text-ink flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-ok" />
                <span>Redakte Edilmiş Soru Taslağı (Düzenlenebilir):</span>
              </h3>
              {hasGeneratedOnce && (
                <span className="text-2xs bg-ok-soft text-ok font-bold px-2 py-0.5 rounded-full border border-ok/30">
                  ✓ Yapay Zeka Tarafından Başarıyla Oluşturuldu
                </span>
              )}
            </div>

            {/* Stem Input */}
            <div className="space-y-1">
              <label className="text-2xs font-bold text-ink-2">Soru Kökü (Klinik Senaryo):</label>
              <textarea
                rows={3}
                value={draftStem}
                onChange={(e) => setDraftStem(e.target.value)}
                className="w-full bg-white border border-line-2 rounded-xl p-2.5 text-xs text-ink focus:border-ok"
              />
            </div>

            {/* 5 Options Grid */}
            <div className="space-y-2">
              <label className="text-2xs font-bold text-ink-2 flex items-center justify-between">
                <span>5 Seçenek (A, B, C, D, E) & Doğru Cevap:</span>
                <span className="text-ink-3 font-normal">Doğru cevabı radyo butonundan seçin</span>
              </label>
              <div className="grid grid-cols-1 gap-2">
                {draftOptions.map((opt, idx) => (
                  <div
                    key={opt.key}
                    className={`flex items-center gap-2 p-2 rounded-xl border transition-all ${
                      draftCorrectAnswer === opt.key
                        ? 'bg-ok-soft border-ok'
                        : 'bg-white border-line'
                    }`}
                  >
                    <label className="flex items-center gap-1.5 cursor-pointer shrink-0">
                      <input
                        type="radio"
                        name="correctAnswerGroup"
                        checked={draftCorrectAnswer === opt.key}
                        onChange={() => setDraftCorrectAnswer(opt.key)}
                        className="text-ok focus:ring-ok cursor-pointer"
                      />
                      <span className={`w-5 h-5 rounded-full flex items-center justify-center text-2xs font-bold ${
                        draftCorrectAnswer === opt.key ? 'bg-ok text-white' : 'bg-line text-ink-2'
                      }`}>
                        {opt.key}
                      </span>
                    </label>

                    <input
                      type="text"
                      value={opt.text}
                      onChange={(e) => {
                        const newOpts = [...draftOptions];
                        newOpts[idx].text = e.target.value;
                        setDraftOptions(newOpts);
                      }}
                      placeholder={`${opt.key} seçeneği metni...`}
                      className="flex-1 bg-transparent text-xs text-ink focus:outline-none"
                    />

                    {draftCorrectAnswer === opt.key && (
                      <span className="text-2xs bg-ok/20 text-ok px-2 py-0.5 rounded font-extrabold shrink-0">
                        Doğru Cevap
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Explanation & Discrepancies */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <div className="space-y-1">
                <label className="text-2xs font-bold text-ink-2">Klinik Patofizyolojik Açıklama:</label>
                <textarea
                  rows={3}
                  value={draftExplanation}
                  onChange={(e) => setDraftExplanation(e.target.value)}
                  placeholder="Detaylı patofizyoloji ve literatür dayanağı..."
                  className="w-full bg-white border border-line-2 rounded-xl p-2.5 text-xs text-ink focus:border-ok"
                />
              </div>

              <div className="space-y-1">
                <label className="text-2xs font-bold text-ink-2">Redaksiyon Notu & Gerekçe:</label>
                <textarea
                  rows={3}
                  value={draftNotes}
                  onChange={(e) => setDraftNotes(e.target.value)}
                  placeholder="Admin talimatı doğrultusunda yapılan değişiklikler..."
                  className="w-full bg-white border border-line-2 rounded-xl p-2.5 text-xs text-ink focus:border-ok"
                />
              </div>
            </div>

          </div>

        </div>

        {/* Modal Footer */}
        <div className="p-4 bg-field border-t border-line flex items-center justify-between gap-3 shrink-0">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-xs font-semibold text-ink-2 hover:bg-line transition-colors cursor-pointer"
          >
            İptal
          </button>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleSave}
              disabled={isSaving || !draftStem.trim()}
              className="bg-ok hover:bg-ok text-white font-bold text-xs sm:text-sm px-5 py-2.5 rounded-xl shadow-sm flex items-center gap-1.5 transition-all disabled:opacity-50 cursor-pointer"
            >
              {isSaving ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-white" />
                  <span>Veritabanına Kaydediliyor...</span>
                </>
              ) : (
                <>
                  <Check className="w-4 h-4" />
                  <span>Değişiklikleri Onayla & Kaydet</span>
                </>
              )}
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};
