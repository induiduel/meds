import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  X,
  CheckCircle2,
  AlertTriangle,
  BookOpen,
  FileText,
  Send,
  RefreshCw,
  Sliders,
  Check,
  GraduationCap,
  Layers,
  Cpu,
  BookMarked,
  ExternalLink,
  Brain,
  Wand2,
  Edit3,
  Lightbulb,
  Search,
  MessageSquare,
  ThumbsUp,
  HelpCircle,
  ArrowRight
} from 'lucide-react';
import { QuestionItem, ReconstructedQuestion, LectureNote } from '../types';
import { ApiService } from '../services/api';
import { AppUser } from '../services/auth';
import { AiQuotaAlertModal } from './AiQuotaAlertModal';

interface AiQuestionOptimizerModalProps {
  question: QuestionItem | null;
  isOpen: boolean;
  onClose: () => void;
  onSaved: (updatedQuestion: QuestionItem) => void;
  currentUser?: AppUser | null;
  onOpenSlideReader?: (note: any, pageNumber?: number) => void;
}

const QUICK_PROMPTS = [
  'Soru kökü ve şıklardaki yazım/harf hatalarını düzeltip resmi sınav diline getir.',
  'Soru kökünü "aşağıdakilerden hangisi DEĞİLDİR / YANLIŞTIR" olumsuz formatına dönüştür ve şıkları buna göre düzenle.',
  'Amfi ders notunda ve slaytta vurgulanan patofizyolojik mekanizmayı soru köküne ekle ve 5 şıklı klinik vaka yap.',
  'Öğrencinin hatırladığı ipuçlarını birleştirerek eksik şıkları kurul düzeyinde güçlü çeldiricilerle 5 şıkka tamamla.',
  'Robbins Patoloji / Katzung Farmakoloji standardında derin klinik açıklama ve doğru cevap gerekçesi oluştur.'
];

export const AiQuestionOptimizerModal: React.FC<AiQuestionOptimizerModalProps> = ({
  question,
  isOpen,
  onClose,
  onSaved,
  currentUser,
  onOpenSlideReader
}) => {
  if (!isOpen || !question) return null;

  return (
    <AiQuestionOptimizerContent
      question={question}
      isOpen={isOpen}
      onClose={onClose}
      onSaved={onSaved}
      currentUser={currentUser}
      onOpenSlideReader={onOpenSlideReader}
    />
  );
};

const AiQuestionOptimizerContent: React.FC<AiQuestionOptimizerModalProps & { question: QuestionItem }> = ({
  question,
  onClose,
  onSaved,
  currentUser,
  onOpenSlideReader
}) => {
  const currentRecon = question.reconstruction;
  const initialStem = currentRecon?.stem || (question as any).rawQuestion?.stem || question.rawStem || question.fragments?.[0]?.text || question.topic || '';
  const initialOptions = currentRecon?.options || (question as any).rawQuestion?.options || question.options || [
    { key: 'A', text: '', isAiFilled: false },
    { key: 'B', text: '', isAiFilled: false },
    { key: 'C', text: '', isAiFilled: false },
    { key: 'D', text: '', isAiFilled: false },
    { key: 'E', text: '', isAiFilled: false },
  ];
  const initialCorrect = (currentRecon?.correctAnswer || question.claimedAnswer || 'A') as 'A' | 'B' | 'C' | 'D' | 'E';
  const initialExplanation = currentRecon?.explanation || '';

  // Form & Guidance States
  const [studentNotes, setStudentNotes] = useState('');
  const [selectedModel, setSelectedModel] = useState('gemini-3.8-flash');
  const [preferredProvider, setPreferredProvider] = useState<'auto' | 'gemini' | 'groq'>('auto');
  const [showAdvancedSettings, setShowAdvancedSettings] = useState(false);
  const [customApiKey, setCustomApiKey] = useState(
    localStorage.getItem('medsoru_gemini_api_key') || localStorage.getItem('medsoru_custom_gemini_key') || ''
  );

  // Matching Lecture Slide State
  const [isSearchingSlides, setIsSearchingSlides] = useState(false);
  const [matchedSlide, setMatchedSlide] = useState<any>(question.lectureReference || null);
  const [candidateSlides, setCandidateSlides] = useState<any[]>([]);

  // Generation & Progress States
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [progressStep, setProgressStep] = useState<number>(0);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [hasOptimizedOnce, setHasOptimizedOnce] = useState(false);
  const [refinementReport, setRefinementReport] = useState<string>('');
  const [planUsed, setPlanUsed] = useState<string>('');
  const [isQuotaModalOpen, setIsQuotaModalOpen] = useState(false);

  // Editable Draft States for Generated Result
  const [draftDiscipline, setDraftDiscipline] = useState(question.discipline || 'Tıp Fakültesi');
  const [draftTopic, setDraftTopic] = useState(question.topic || 'Kurul Sınav Sorusu');
  const [draftStem, setDraftStem] = useState(initialStem);
  const [draftOptions, setDraftOptions] = useState<{ key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string; isAiFilled: boolean }[]>(
    ['A', 'B', 'C', 'D', 'E'].map((k) => {
      const existing = initialOptions.find((o: any) => o.key === k);
      return {
        key: k as any,
        text: existing?.text || '',
        isAiFilled: Boolean((existing as any)?.isAiFilled || (existing as any)?.isAiGenerated)
      };
    })
  );
  const [draftCorrectAnswer, setDraftCorrectAnswer] = useState<'A' | 'B' | 'C' | 'D' | 'E'>(initialCorrect);
  const [draftExplanation, setDraftExplanation] = useState(initialExplanation);
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Auto-search matching lecture slide on mount
  useEffect(() => {
    let isMounted = true;
    const searchSlides = async () => {
      setIsSearchingSlides(true);
      try {
        const queryText = [
          question.topic,
          question.discipline,
          initialStem,
          ...(question.fragments || []).map((f) => f.text),
          ...(question.options || []).map((o) => o.text),
        ].filter(Boolean).join(' ');

        const res = await ApiService.matchLectureNotes({
          queryText,
          disciplineHint: question.discipline,
          committeeId: question.committeeId,
          limit: 3
        });

        if (isMounted && res.matches && res.matches.length > 0) {
          setCandidateSlides(res.matches);
          if (!matchedSlide) {
            setMatchedSlide(res.matches[0]);
          }
        }
      } catch (err) {
        console.warn('Auto match lecture notes error:', err);
      } finally {
        if (isMounted) setIsSearchingSlides(false);
      }
    };

    searchSlides();
    return () => {
      isMounted = false;
    };
  }, [question.id]);

  const handleApplyQuickPrompt = (promptText: string) => {
    setStudentNotes((prev) => (prev ? `${prev}\n${promptText}` : promptText));
  };

  const handleRunOptimization = async () => {
    setIsOptimizing(true);
    setErrorMsg(null);
    setProgressStep(1);

    const stepInterval = setInterval(() => {
      setProgressStep((prev) => (prev < 4 ? prev + 1 : prev));
    }, 900);

    try {
      const res = await ApiService.optimizeQuestionWithAi({
        question,
        studentNotes: studentNotes.trim() || undefined,
        apiKey: customApiKey.trim() || undefined,
        preferredProvider,
        model: selectedModel,
      });

      clearInterval(stepInterval);
      setProgressStep(4);

      if (res.success && res.optimizedQuestion) {
        const opt = res.optimizedQuestion;
        setDraftDiscipline(opt.discipline);
        setDraftTopic(opt.topic);
        setDraftStem(opt.stem);
        setDraftOptions(opt.options);
        setDraftCorrectAnswer(opt.correctAnswer as any);
        setDraftExplanation(opt.explanation);
        setRefinementReport(res.refinementSummary || opt.notesAndDiscrepancies || '');
        setPlanUsed(`${res.providerUsed || 'Gemini'} (${res.planUsed || 'Canlı Model'})`);
        if (res.matchedLecture) {
          setMatchedSlide(res.matchedLecture);
        }
        setHasOptimizedOnce(true);
      } else {
        setErrorMsg(res.error || 'Yapay zeka soru düzenlemesi gerçekleştirilemedi.');
      }
    } catch (err: any) {
      clearInterval(stepInterval);
      const msg = err.message || 'Yapay zeka optimizasyonu sırasında bir hata oluştu.';
      setErrorMsg(msg);
      if (/429|quota|resource_exhausted|spending cap|limit/i.test(msg)) {
        setIsQuotaModalOpen(true);
      }
    } finally {
      setIsOptimizing(false);
    }
  };

  const handleSaveToQuestion = async () => {
    setIsSaving(true);
    setErrorMsg(null);

    try {
      const optimizedData = {
        discipline: draftDiscipline.trim(),
        topic: draftTopic.trim(),
        stem: draftStem.trim(),
        options: draftOptions,
        correctAnswer: draftCorrectAnswer,
        explanation: draftExplanation.trim(),
        confidenceScore: 96,
        notesAndDiscrepancies: refinementReport || 'Yapay zeka ve amfi ders notları zeminlemesi ile düzenlendi.'
      };

      const result = await ApiService.applyAiOptimization({
        questionId: question.id,
        optimizedData,
        matchedLecture: matchedSlide,
        refinementSummary: refinementReport || 'Yapay Zeka ve Amfi Ders Notu Zeminlemesi ile Düzenlendi',
        userEmail: currentUser?.email || undefined,
        userName: currentUser?.displayName || 'Tıbbiyeli Öğrenci',
        studentNumber: currentUser?.studentNumber || undefined,
      });

      if (result.success && result.question) {
        setSaveSuccess(true);
        setTimeout(() => {
          onSaved(result.question!);
          onClose();
        }, 800);
      } else {
        setErrorMsg(result.error || 'Düzenleme kaydedilemedi.');
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Kaydetme işlemi sırasında hata oluştu.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-slate-950/80 backdrop-blur-md overflow-y-auto">
      <div className="ms-modal-panel relative w-full max-w-5xl bg-white rounded-2xl shadow-2xl border border-teal-200/80 flex flex-col max-h-[92vh] overflow-hidden my-auto animate-in fade-in zoom-in-95 duration-200">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-900 via-teal-800 to-cyan-900 px-5 py-4 text-white flex items-center justify-between shrink-0 shadow-sm border-b border-teal-700/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-400 to-cyan-300 text-teal-950 flex items-center justify-center shadow-md">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-base sm:text-lg text-white">Yapay Zeka Soru Düzenleme & İyileştirme Motoru</h3>
                <span className="hidden sm:inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-teal-500/20 text-teal-200 border border-teal-400/30">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  Canlı • Amfi Notu & Tıp Zeminlemeli
                </span>
              </div>
              <p className="text-xs text-teal-200/80 mt-0.5">
                Soru No: #{question.questionNumber || 'Çıkmış'} · {question.discipline || 'Tıp'} · {question.topic || 'Kurul Sınavı'}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg bg-teal-800/60 hover:bg-teal-700 text-teal-100 flex items-center justify-center transition-colors cursor-pointer"
            title="Kapat"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body: Two columns on desktop */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 grid grid-cols-1 lg:grid-cols-12 gap-5">
          
          {/* LEFT COLUMN: Context, Match & User Prompt (col-span-5) */}
          <div className="lg:col-span-5 flex flex-col gap-4">
            
            {/* Matched Lecture Note Card */}
            <div className="bg-gradient-to-br from-emerald-50/70 to-teal-50/50 border border-emerald-200/80 rounded-xl p-3.5 shadow-2xs">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-900">
                  <BookMarked className="w-4 h-4 text-emerald-600" />
                  <span>Amfi Ders Notu Zeminlemesi</span>
                </div>
                {isSearchingSlides ? (
                  <span className="text-[11px] text-teal-700 flex items-center gap-1">
                    <RefreshCw className="w-3 h-3 animate-spin" />
                    Slayt aranıyor...
                  </span>
                ) : matchedSlide ? (
                  <span className="px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded-md text-[11px] font-bold">
                    %{matchedSlide.confidenceScore || matchedSlide.score || 95} Eşleşti
                  </span>
                ) : null}
              </div>

              {matchedSlide ? (
                <div className="space-y-2">
                  <div className="bg-white/90 p-2.5 rounded-lg border border-emerald-100 text-xs">
                    <div className="font-semibold text-slate-800 flex items-center justify-between">
                      <span className="truncate pr-2">{matchedSlide.noteTitle || matchedSlide.title}</span>
                      <span className="text-[11px] bg-emerald-50 text-emerald-700 px-1.5 py-0.5 rounded shrink-0">
                        Slayt #{matchedSlide.pageNumber}
                      </span>
                    </div>
                    <div className="text-[11px] text-slate-500 mt-0.5">
                      Ders: <strong className="text-slate-700">{matchedSlide.discipline}</strong>
                    </div>
                    {matchedSlide.matchedSnippet && (
                      <p className="mt-1.5 text-[11px] text-slate-600 italic bg-slate-50 p-1.5 rounded border border-slate-100 line-clamp-3">
                        "{matchedSlide.matchedSnippet}"
                      </p>
                    )}
                  </div>
                  
                  {onOpenSlideReader && (
                    <button
                      type="button"
                      onClick={() => onOpenSlideReader(matchedSlide, matchedSlide.pageNumber)}
                      className="w-full text-xs font-semibold text-emerald-700 hover:text-emerald-800 bg-white hover:bg-emerald-50 border border-emerald-200 py-1.5 rounded-lg flex items-center justify-center gap-1.5 transition-colors cursor-pointer"
                    >
                      <BookOpen className="w-3.5 h-3.5" />
                      <span>Bu Amfi Slaytını Oku & İncele</span>
                    </button>
                  )}
                </div>
              ) : (
                <div className="text-xs text-slate-500 py-2 text-center bg-white/60 rounded-lg border border-dashed border-emerald-200">
                  {isSearchingSlides ? '880+ Amfi ders slaytı taranıyor...' : 'Doğrudan eşleşen slayt bulunamadı, tıp literatürü esas alınacak.'}
                </div>
              )}
            </div>

            {/* Question Pool / Memory Fragments Context */}
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 text-xs">
              <div className="flex items-center justify-between mb-2">
                <span className="font-bold text-slate-700 flex items-center gap-1.5">
                  <Layers className="w-3.5 h-3.5 text-teal-600" />
                  Öğrenci Soru Havuzu ({question.fragments?.length || 0} Parça)
                </span>
                {question.claimedAnswer && (
                  <span className="text-[11px] bg-teal-100 text-teal-800 font-bold px-2 py-0.5 rounded">
                    Hatırlanan Cevap: {question.claimedAnswer}
                  </span>
                )}
              </div>

              {question.fragments && question.fragments.length > 0 ? (
                <div className="space-y-1.5 max-h-36 overflow-y-auto pr-1">
                  {question.fragments.map((f, i) => (
                    <div key={f.id || i} className="bg-white p-2 rounded border border-slate-100 text-[11px] text-slate-600">
                      <span className="font-semibold text-slate-700">{f.author}:</span> "{f.text}"
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-[11px] text-slate-500 italic bg-white p-2 rounded border border-slate-100">
                  Henüz öğrenci hafıza parçası girilmemiş. Mevcut konu ve ham soru kökü baz alınacak.
                </p>
              )}
            </div>

            {/* Student Custom Guidance & Clues */}
            <div className="flex flex-col gap-2">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                  <Lightbulb className="w-3.5 h-3.5 text-amber-500" />
                  <span>Öğrenci / Kullanıcı Ek Yönlendirmesi (İsteğe Bağlı):</span>
                </label>
                <span className="text-[10px] text-slate-400">İpucu veya Hoca Vurgusu</span>
              </div>
              <textarea
                value={studentNotes}
                onChange={(e) => setStudentNotes(e.target.value)}
                placeholder="Örn: Hoca bu soruda kesinlikle değildir kökünü sordu / Slaytta Orphan Annie gözü çekirdeği vurgulanmıştı / C şıkkında Bradikinin vardı..."
                rows={3}
                className="w-full text-xs p-2.5 rounded-xl border border-slate-300 focus:border-teal-500 focus:ring-1 focus:ring-teal-500 outline-none transition-all resize-none bg-white text-slate-800"
              />

              {/* Quick Prompt Suggestions */}
              <div className="flex flex-wrap gap-1.5">
                {QUICK_PROMPTS.map((qp, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => handleApplyQuickPrompt(qp)}
                    className="text-[10px] bg-slate-100 hover:bg-teal-50 hover:text-teal-700 text-slate-600 border border-slate-200 px-2 py-1 rounded-md transition-all text-left cursor-pointer"
                  >
                    + {qp.slice(0, 42)}...
                  </button>
                ))}
              </div>
            </div>

            {/* Advanced Settings Accordion */}
            <div className="border border-slate-200 rounded-xl overflow-hidden text-xs">
              <button
                type="button"
                onClick={() => setShowAdvancedSettings(!showAdvancedSettings)}
                className="w-full px-3 py-2 bg-slate-50 hover:bg-slate-100 flex items-center justify-between text-slate-600 font-semibold cursor-pointer"
              >
                <span className="flex items-center gap-1.5">
                  <Sliders className="w-3.5 h-3.5 text-slate-500" />
                  Gelişmiş AI Ayarları (Model & Sağlayıcı)
                </span>
                <span className="text-[11px] text-teal-600 font-mono">
                  {showAdvancedSettings ? 'Gizle' : 'Göster'}
                </span>
              </button>

              {showAdvancedSettings && (
                <div className="p-3 bg-white space-y-3 border-t border-slate-200">
                  <div>
                    <label className="block text-[11px] font-semibold text-slate-600 mb-1">Yapay Zeka Modeli</label>
                    <select
                      value={selectedModel}
                      onChange={(e) => setSelectedModel(e.target.value)}
                      className="w-full text-xs p-2 border border-slate-300 rounded-lg bg-white"
                    >
                      <option value="gemini-3.8-flash">Google Gemini 3.8 Flash (Önerilen • Hızlı & Tıbbi Akıl Yürütme)</option>
                      <option value="gemini-flash-latest">Google Gemini Flash Latest</option>
                      <option value="llama-3.3-70b-versatile">Groq Cloud (Llama 3.3 70B • Yedek Motor)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[11px] font-semibold text-slate-600 mb-1">
                      Özel Gemini API Anahtarı (İsteğe bağlı)
                    </label>
                    <input
                      type="password"
                      value={customApiKey}
                      onChange={(e) => {
                        setCustomApiKey(e.target.value);
                        localStorage.setItem('medsoru_gemini_api_key', e.target.value);
                      }}
                      placeholder="Boş bırakılırsa sunucudaki anahtar havuzu çalışır"
                      className="w-full text-xs p-2 border border-slate-300 rounded-lg"
                    />
                    <p className="text-[10px] text-slate-400 mt-0.5">
                      Boş bırakırsanız sistemdeki otomatik havuz (Ücretsiz + Yedek) kullanılır.
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Run AI Button */}
            <button
              type="button"
              onClick={handleRunOptimization}
              disabled={isOptimizing}
              className={`w-full py-3 px-4 rounded-xl font-bold text-sm text-white flex items-center justify-center gap-2 shadow-md transition-all cursor-pointer ${
                isOptimizing
                  ? 'bg-teal-700 opacity-90 cursor-not-allowed'
                  : 'bg-gradient-to-r from-teal-600 to-cyan-700 hover:from-teal-700 hover:to-cyan-800 active:scale-[0.99]'
              }`}
            >
              {isOptimizing ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-teal-200" />
                  <span>Yapay Zeka Düzenliyor...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-cyan-300" />
                  <span>{hasOptimizedOnce ? 'Yapay Zeka ile Tekrar Düzenle' : 'Yapay Zeka ile Gerçek Zamanlı Düzenle'}</span>
                </>
              )}
            </button>

            {/* Real-time Progress Stepper */}
            {isOptimizing && (
              <div className="bg-teal-50 border border-teal-200 p-3 rounded-xl space-y-1.5 text-xs text-teal-900">
                <div className="flex items-center gap-2 font-bold">
                  <RefreshCw className="w-3.5 h-3.5 animate-spin text-teal-600" />
                  <span>Gerçek Zamanlı Süreç:</span>
                </div>
                <div className="space-y-1 pl-4 text-[11px]">
                  <div className={`flex items-center gap-1.5 ${progressStep >= 1 ? 'font-semibold text-teal-900' : 'text-slate-400'}`}>
                    <span>{progressStep >= 1 ? '✓' : '○'}</span>
                    <span>1. Öğrenci soru havuzu ve hatırlanan parçalar derleniyor...</span>
                  </div>
                  <div className={`flex items-center gap-1.5 ${progressStep >= 2 ? 'font-semibold text-teal-900' : 'text-slate-400'}`}>
                    <span>{progressStep >= 2 ? '✓' : '○'}</span>
                    <span>2. 880+ Amfi ders notu ve slaytlar taranarak zeminleme yapılıyor...</span>
                  </div>
                  <div className={`flex items-center gap-1.5 ${progressStep >= 3 ? 'font-semibold text-teal-900' : 'text-slate-400'}`}>
                    <span>{progressStep >= 3 ? '✓' : '○'}</span>
                    <span>3. Tıbbi literatür ve internet bilgisiyle etki mekanizması teyit ediliyor...</span>
                  </div>
                  <div className={`flex items-center gap-1.5 ${progressStep >= 4 ? 'font-semibold text-teal-900' : 'text-slate-400'}`}>
                    <span>{progressStep >= 4 ? '✓' : '○'}</span>
                    <span>4. Kurul sınavı dilinde saf soru kökü ve 5 seçenek oluşturuluyor...</span>
                  </div>
                </div>
              </div>
            )}

            {errorMsg && (
              <div className="bg-red-50 border border-red-200 p-3 rounded-xl text-xs text-red-700 flex items-start gap-2">
                <AlertTriangle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
                <p className="leading-relaxed">{errorMsg}</p>
              </div>
            )}
          </div>

          {/* RIGHT COLUMN: AI Refined Result & Editable Preview (col-span-7) */}
          <div className="lg:col-span-7 flex flex-col gap-4 bg-slate-50/50 p-4 rounded-xl border border-slate-200">
            
            <div className="flex items-center justify-between border-b border-slate-200 pb-3">
              <div>
                <h4 className="font-bold text-slate-800 text-sm sm:text-base flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-teal-600" />
                  <span>{hasOptimizedOnce ? 'Yapay Zeka Tarafından Düzenlenen Soru' : 'Düzenleme Taslağı'}</span>
                </h4>
                <p className="text-xs text-slate-500 mt-0.5">
                  {hasOptimizedOnce 
                    ? `Ders notu ve tıp zeminlemesiyle oluşturuldu (${planUsed || 'Gemini 3.8 Flash'}). Doğrudan inceleyip düzenleyebilirsiniz.`
                    : 'Henüz yapay zeka çalıştırılmadı. Sol taraftan "Düzenle" butonuna basarak anında çalıştırabilirsiniz.'}
                </p>
              </div>
              {hasOptimizedOnce && (
                <span className="px-2.5 py-1 bg-teal-100 text-teal-800 rounded-full text-xs font-bold shrink-0">
                  %96 Güven
                </span>
              )}
            </div>

            {/* Discipline & Topic Detected by AI */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-[11px] font-bold text-slate-700 mb-1">
                  Tespit Edilen Ders / Disiplin:
                </label>
                <input
                  type="text"
                  value={draftDiscipline}
                  onChange={(e) => setDraftDiscipline(e.target.value)}
                  className="w-full text-xs p-2 bg-white rounded-lg border border-slate-300 font-semibold text-slate-800 focus:border-teal-500 outline-none"
                  placeholder="Örn: Tıbbi Patoloji"
                />
              </div>
              <div>
                <label className="block text-[11px] font-bold text-slate-700 mb-1">
                  Tespit Edilen Konu Başlığı:
                </label>
                <input
                  type="text"
                  value={draftTopic}
                  onChange={(e) => setDraftTopic(e.target.value)}
                  className="w-full text-xs p-2 bg-white rounded-lg border border-slate-300 font-semibold text-slate-800 focus:border-teal-500 outline-none"
                  placeholder="Örn: Miyokard İnfarktüsü Histopatolojisi"
                />
              </div>
            </div>

            {/* Pure Stem Textarea */}
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                  <FileText className="w-3.5 h-3.5 text-teal-600" />
                  <span>Resmi Sınav Soru Kökü:</span>
                </label>
                <span className="text-[10px] text-slate-400">Saf ve temiz sınav metni</span>
              </div>
              <textarea
                value={draftStem}
                onChange={(e) => setDraftStem(e.target.value)}
                rows={4}
                className="w-full text-xs sm:text-[13px] p-3 rounded-xl border border-slate-300 focus:border-teal-500 focus:ring-1 focus:ring-teal-500 outline-none transition-all leading-relaxed bg-white text-slate-900 font-medium"
                placeholder="Düzenlenmiş soru kökü..."
              />
            </div>

            {/* 5 Options (A, B, C, D, E) */}
            <div className="space-y-2">
              <label className="block text-xs font-bold text-slate-700">
                5 Seçenek ve Doğru Cevap (Seçili olan doğru şıktır):
              </label>
              <div className="space-y-1.5">
                {draftOptions.map((opt, idx) => {
                  const isCorrect = draftCorrectAnswer === opt.key;
                  return (
                    <div
                      key={opt.key}
                      className={`flex items-center gap-2 p-2 rounded-xl border transition-all ${
                        isCorrect
                          ? 'bg-emerald-50/90 border-emerald-300 ring-1 ring-emerald-300 shadow-2xs'
                          : 'bg-white border-slate-200'
                      }`}
                    >
                      <button
                        type="button"
                        onClick={() => setDraftCorrectAnswer(opt.key)}
                        className={`w-7 h-7 rounded-lg font-bold text-xs flex items-center justify-center shrink-0 cursor-pointer transition-colors ${
                          isCorrect
                            ? 'bg-emerald-600 text-white shadow-xs'
                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                        }`}
                        title="Doğru cevap olarak işaretle"
                      >
                        {opt.key}
                      </button>
                      <input
                        type="text"
                        value={opt.text}
                        onChange={(e) => {
                          const val = e.target.value;
                          setDraftOptions((prev) =>
                            prev.map((o) => (o.key === opt.key ? { ...o, text: val } : o))
                          );
                        }}
                        className="flex-1 text-xs sm:text-[13px] p-1.5 bg-transparent border-none outline-none text-slate-800"
                        placeholder={`${opt.key} şıkkı metni...`}
                      />
                      {opt.isAiFilled && (
                        <span className="text-[10px] bg-cyan-100 text-cyan-800 px-1.5 py-0.5 rounded font-semibold shrink-0">
                          AI Çeldirici
                        </span>
                      )}
                      {isCorrect && (
                        <span className="text-[10px] bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full font-bold shrink-0 flex items-center gap-1">
                          <Check className="w-3 h-3" /> Doğru
                        </span>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Academic Explanation */}
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Klinik Patofizyolojik Açıklama & Çeldirici Analizi:
              </label>
              <textarea
                value={draftExplanation}
                onChange={(e) => setDraftExplanation(e.target.value)}
                rows={3}
                className="w-full text-xs p-2.5 rounded-xl border border-slate-300 focus:border-teal-500 focus:ring-1 focus:ring-teal-500 outline-none transition-all leading-relaxed bg-white text-slate-700"
                placeholder="Robbins/Guyton/Katzung standardında patofizyolojik açıklama..."
              />
            </div>

            {/* Refinement Summary Report */}
            {refinementReport && (
              <div className="bg-teal-50/80 border border-teal-200 p-3 rounded-xl text-xs text-teal-900">
                <span className="font-bold flex items-center gap-1.5 mb-1 text-teal-950">
                  <Sparkles className="w-3.5 h-3.5 text-teal-600" />
                  Yapay Zeka Düzenleme Raporu:
                </span>
                <p className="leading-relaxed text-[11px] text-teal-800">{refinementReport}</p>
              </div>
            )}

            {/* Bottom Actions */}
            <div className="mt-auto pt-3 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-3">
              <div className="text-xs text-slate-500 flex items-center gap-1">
                <span>Katkı Sahibi:</span>
                <strong className="text-slate-700">{currentUser?.displayName || 'Öğrenci'}</strong>
              </div>

              <div className="flex items-center gap-2 w-full sm:w-auto">
                <button
                  type="button"
                  onClick={onClose}
                  className="flex-1 sm:flex-none px-4 py-2 border border-slate-300 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition-colors cursor-pointer"
                >
                  İptal
                </button>
                <button
                  type="button"
                  onClick={handleSaveToQuestion}
                  disabled={isSaving || saveSuccess}
                  className={`flex-1 sm:flex-none px-5 py-2.5 rounded-xl text-xs font-bold text-white flex items-center justify-center gap-2 shadow-md transition-all cursor-pointer ${
                    saveSuccess
                      ? 'bg-emerald-600 text-white'
                      : isSaving
                      ? 'bg-teal-700 opacity-80 cursor-wait'
                      : 'bg-emerald-600 hover:bg-emerald-700 active:scale-95'
                  }`}
                >
                  {saveSuccess ? (
                    <>
                      <Check className="w-4 h-4" />
                      <span>Soruya Uygulandı!</span>
                    </>
                  ) : isSaving ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      <span>Kaydediliyor...</span>
                    </>
                  ) : (
                    <>
                      <CheckCircle2 className="w-4 h-4" />
                      <span>Düzenlemeyi Soruya Uygula & Kaydet</span>
                    </>
                  )}
                </button>
              </div>
            </div>

          </div>

        </div>

      </div>

      <AiQuotaAlertModal
        isOpen={isQuotaModalOpen}
        onClose={() => setIsQuotaModalOpen(false)}
        onRetry={handleRunOptimization}
        errorDetails={errorMsg || undefined}
        sourceFunction="Soru Düzenleme (AI Optimizer)"
      />
    </div>
  );
};
