import React, { useState, useEffect } from 'react';
import { 
  Sparkles, 
  Send, 
  CheckCircle2, 
  HelpCircle, 
  Layers, 
  FileText, 
  GraduationCap, 
  BookOpen, 
  Clock, 
  User, 
  Calendar,
  AlertCircle
} from 'lucide-react';
import { Committee, QuestionItem } from '../types';
import { AppUser } from '../services/auth';

interface QuickAddHeroProps {
  committee: Committee | undefined;
  committees: Committee[];
  onSelectCommittee: (committeeId: string) => void;
  onSubmitContribution: (data: {
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
  unassignedCount: number;
  totalQuestionsCount: number;
  onNavigateTab: (tab: 'matrix' | 'questions' | 'practice' | 'booklet') => void;
  isAdmin: boolean;
  currentUser?: AppUser | null;
  onOpenAdminPanel?: () => void;
}

const SAVED_NAME_KEY = 'medsoru_saved_contributor_name';

export const QuickAddHero: React.FC<QuickAddHeroProps> = ({
  committee,
  committees,
  onSelectCommittee,
  onSubmitContribution,
  unassignedCount,
  totalQuestionsCount,
  onNavigateTab,
  isAdmin,
  currentUser,
  onOpenAdminPanel,
}) => {
  // Author name remembered in localStorage or currentUser
  const [author, setAuthor] = useState(() => {
    return currentUser?.displayName || localStorage.getItem(SAVED_NAME_KEY) || '';
  });

  useEffect(() => {
    if (currentUser?.displayName && !author) {
      setAuthor(currentUser.displayName);
    }
  }, [currentUser]);

  // Default: Soru numarasını hatırlamıyorum is TRUE (Default checked as requested!)
  const [isUnknownNumber, setIsUnknownNumber] = useState(true);
  const [questionNumber, setQuestionNumber] = useState(1);

  // Disciplines of the current committee
  const disciplines = committee?.disciplines && committee.disciplines.length > 0
    ? committee.disciplines
    : ['Tıbbi Patoloji', 'Tıbbi Farmakoloji', 'Tıbbi Mikrobiyoloji', 'Dahiliye', 'Genel Tıp'];

  const [discipline, setDiscipline] = useState(disciplines[0] || 'Tıbbi Patoloji');
  const [topic, setTopic] = useState('');
  const [fragmentText, setFragmentText] = useState('');
  
  // Options
  const [showOptions, setShowOptions] = useState(false);
  const [optA, setOptA] = useState('');
  const [optB, setOptB] = useState('');
  const [optC, setOptC] = useState('');
  const [optD, setOptD] = useState('');
  const [optE, setOptE] = useState('');
  const [claimedAnswer, setClaimedAnswer] = useState<'A' | 'B' | 'C' | 'D' | 'E' | undefined>(undefined);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Sync discipline when committee changes
  useEffect(() => {
    if (disciplines.length > 0 && !disciplines.includes(discipline)) {
      setDiscipline(disciplines[0]);
    }
  }, [committee]);

  const handleAuthorChange = (val: string) => {
    setAuthor(val);
    localStorage.setItem(SAVED_NAME_KEY, val);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!committee) return;
    if (!fragmentText.trim() && !optA.trim() && !optB.trim()) {
      alert('Lütfen sorudan aklınızda kalan en az bir cümle veya bir şık yazınız.');
      return;
    }

    setIsSubmitting(true);
    try {
      const optionsList: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string }[] = [];
      if (optA.trim()) optionsList.push({ key: 'A', text: optA.trim() });
      if (optB.trim()) optionsList.push({ key: 'B', text: optB.trim() });
      if (optC.trim()) optionsList.push({ key: 'C', text: optC.trim() });
      if (optD.trim()) optionsList.push({ key: 'D', text: optD.trim() });
      if (optE.trim()) optionsList.push({ key: 'E', text: optE.trim() });

      await onSubmitContribution({
        committeeId: committee.id,
        questionNumber: isUnknownNumber ? undefined : Number(questionNumber),
        isUnknownNumber,
        discipline,
        topic: topic.trim() || `${discipline} Hatırlanan Soru`,
        fragmentText: fragmentText.trim(),
        author: author.trim() || currentUser?.displayName || 'Dönem 3 Öğrencisi',
        authorUid: currentUser?.uid,
        authorStudentNumber: currentUser?.studentNumber || undefined,
        claimedAnswer,
        options: optionsList.length > 0 ? optionsList : undefined,
      });

      // Clear fields
      setFragmentText('');
      setTopic('');
      setOptA('');
      setOptB('');
      setOptC('');
      setOptD('');
      setOptE('');
      setClaimedAnswer(undefined);
      setShowOptions(false);

      setSuccessMessage(
        isUnknownNumber
          ? 'Katkınız başarıyla havuza kaydedildi! Soru numarasını hatırlamasanız bile yapay zeka ve yöneticimiz soruyu 100 soru arasına yerleştirecektir.'
          : `Soru #${questionNumber} için girdiğiniz parça başarıyla arşive eklendi!`
      );

      setTimeout(() => {
        setSuccessMessage(null);
      }, 7000);
    } catch (err: any) {
      alert('Kayıt sırasında bir hata oluştu: ' + err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  const targetCount = committee?.targetCount || 100;

  return (
    <div className="space-y-6">
      {/* Active Exam Status Banner */}
      <div className="bg-gradient-to-r from-teal-900 via-teal-800 to-slate-900 text-white rounded-2xl p-5 sm:p-7 shadow-lg border border-teal-700/40 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div className="space-y-1.5">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/20 border border-teal-400/30 text-teal-300 text-xs font-semibold">
              <Calendar className="w-3.5 h-3.5" />
              <span>GÜNCEL AKTİF SINAV DÖNEMİ</span>
            </div>

            <h1 className="text-xl sm:text-2xl font-black tracking-tight text-white">
              {committee?.name || 'Dönem 3 Kurul Sınavı'}
            </h1>

            <p className="text-xs sm:text-sm text-teal-100/80 max-w-2xl font-normal leading-relaxed">
              {committee?.description || 'Dönem 3 kurul çıkmış sorularını kolektif hafıza ile eksiksiz olarak yeniden derliyoruz.'}
            </p>
          </div>

          {/* Quick Committee Switcher */}
          <div className="shrink-0 bg-slate-900/60 p-3 rounded-xl border border-teal-500/30 backdrop-blur-xs flex flex-col gap-1.5">
            <label className="text-[11px] text-teal-300 font-semibold uppercase tracking-wider">
              Kurul Değiştir:
            </label>
            <select
              value={committee?.id}
              onChange={(e) => onSelectCommittee(e.target.value)}
              className="bg-slate-800 text-white text-xs rounded-lg px-3 py-2 border border-teal-500/40 focus:ring-2 focus:ring-teal-400 focus:outline-hidden cursor-pointer"
            >
              {committees.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.code ? `[${c.code}] ` : ''}{c.name.split(':')[1]?.trim() || c.name} ({c.targetCount} Soru)
                </option>
              ))}
            </select>
            {committee?.examDate && (
              <span className="text-[10px] text-teal-300/80 font-mono">
                📅 Sınav: {committee.examDate}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Main Single-Purpose Contribution Card */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-md p-5 sm:p-8 relative">
        <div className="border-b border-slate-100 pb-4 mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-lg sm:text-xl font-bold text-slate-900 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-teal-600" />
              Aklınızda Kalan Soruyu Ekleyin
            </h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Soru numarasını bilmeseniz bile aklınızdaki her kelime, vaka detayı veya şık yapay zekanın soruyu tam çıkarmasını sağlar.
            </p>
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="bg-teal-50 text-teal-800 border border-teal-200 px-2.5 py-1 rounded-full font-semibold">
              Hedef: {targetCount} Soru
            </span>
            {unassignedCount > 0 && (
              <span className="bg-amber-50 text-amber-800 border border-amber-200 px-2.5 py-1 rounded-full font-semibold">
                {unassignedCount} Numarasız Soru Havuzda
              </span>
            )}
          </div>
        </div>

        {/* Success Alert */}
        {successMessage && (
          <div className="mb-6 p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 text-xs flex items-start gap-3 animate-fade-in shadow-xs">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
            <div>
              <p className="font-bold text-sm text-emerald-950">Teşekkürler!</p>
              <p className="mt-0.5 leading-relaxed">{successMessage}</p>
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Top Form Row: Author, Number Unknown Toggle, Discipline */}
          <div className="grid grid-cols-1 sm:grid-cols-12 gap-4">
            {/* Contributor Name (Persisted across sessions) */}
            <div className="sm:col-span-4 space-y-1">
              <label className="block text-xs font-bold text-slate-700 flex items-center gap-1.5">
                <User className="w-3.5 h-3.5 text-teal-600" />
                İsminiz / Rumuzunuz
              </label>
              <input
                type="text"
                value={author}
                onChange={(e) => handleAuthorChange(e.target.value)}
                placeholder="Örn: Dr. Ahmet, Anonim35..."
                className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-900 focus:bg-white focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
              />
              <span className="text-[10px] text-slate-400">Girdiğiniz isim sonraki ziyaretleriniz için otomatik hatırlanır.</span>
            </div>

            {/* Discipline Dropdown */}
            <div className="sm:col-span-4 space-y-1">
              <label className="block text-xs font-bold text-slate-700">
                Ders / Anabilim Dalı
              </label>
              <select
                value={discipline}
                onChange={(e) => setDiscipline(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-900 focus:bg-white focus:border-teal-500 focus:ring-1 focus:ring-teal-500 cursor-pointer"
              >
                {disciplines.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
              <span className="text-[10px] text-slate-400">{committee?.code || 'Kurul'} ders programındaki ilgili branş.</span>
            </div>

            {/* Question Number or "Hatırlamıyorum" Toggle */}
            <div className="sm:col-span-4 space-y-1">
              <label className="block text-xs font-bold text-slate-700">
                Soru Numarası
              </label>
              
              <div className="flex items-center gap-2">
                <label className="flex items-center gap-2 px-3 py-2 rounded-lg bg-teal-50/80 border border-teal-200 text-teal-900 text-xs font-semibold cursor-pointer w-full select-none hover:bg-teal-100/80 transition-colors">
                  <input
                    type="checkbox"
                    checked={isUnknownNumber}
                    onChange={(e) => setIsUnknownNumber(e.target.checked)}
                    className="w-4 h-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500"
                  />
                  <span>Soru numarasını hatırlamıyorum</span>
                </label>
              </div>

              {!isUnknownNumber && (
                <div className="mt-2 flex items-center gap-2 animate-fade-in">
                  <input
                    type="number"
                    min={1}
                    max={targetCount}
                    value={questionNumber}
                    onChange={(e) => setQuestionNumber(Math.max(1, Math.min(targetCount, Number(e.target.value))))}
                    className="w-24 bg-white border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs text-slate-900 font-bold font-mono focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
                  />
                  <span className="text-xs text-slate-500 font-serif">. soru (1 - {targetCount} arası)</span>
                </div>
              )}
            </div>
          </div>

          {/* Question Topic / Keyword (Optional) */}
          <div className="space-y-1">
            <label className="block text-xs font-bold text-slate-700">
              Konu veya Anahtar Kelime <span className="text-slate-400 font-normal">(Opsiyonel)</span>
            </label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Örn: Enalapril öksürüğü, Glomerülonefrit, Bradikinin reseptörleri, Crohn hastalığı..."
              className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-900 focus:bg-white focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
            />
          </div>

          {/* Question Text / Memory Fragment */}
          <div className="space-y-1">
            <label className="block text-xs font-bold text-slate-900 flex items-center justify-between">
              <span>Soru Metninden veya Vakasından Ne Hatırlıyorsunuz? *</span>
              <span className="text-[11px] text-teal-700 font-normal">Aklınızda kalan her kelime değerlidir</span>
            </label>
            <textarea
              rows={4}
              value={fragmentText}
              onChange={(e) => setFragmentText(e.target.value)}
              placeholder="Vaka nasıl başlıyordu? Örneğin: '58 yaşında hipertansiyon hastasına ilaç başlanıyor, 3 hafta sonra kuru öksürük gelişiyor. Hangi mediyatör sorumludur gibi bir soru vardı...' ya da şıklardan aklınızda kalanları buraya yazabilirsiniz."
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs sm:text-sm text-slate-900 leading-relaxed focus:bg-white focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
              required
            />
          </div>

          {/* Optional Options Toggle */}
          <div className="border border-slate-200 rounded-xl overflow-hidden bg-slate-50/50">
            <button
              type="button"
              onClick={() => setShowOptions(!showOptions)}
              className="w-full px-4 py-2.5 text-left text-xs font-bold text-slate-700 hover:text-teal-800 flex items-center justify-between cursor-pointer"
            >
              <span>+ Hatırladığınız Şıkları veya Doğru Cevabı Eklemek İster misiniz? (Opsiyonel)</span>
              <span className="text-slate-400 text-xs">{showOptions ? '▲ Gizle' : '▼ Göster'}</span>
            </button>

            {showOptions && (
              <div className="p-4 pt-2 border-t border-slate-200 bg-white space-y-3">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  {(['A', 'B', 'C', 'D', 'E'] as const).map((letter) => {
                    const val = letter === 'A' ? optA : letter === 'B' ? optB : letter === 'C' ? optC : letter === 'D' ? optD : optE;
                    const setVal = letter === 'A' ? setOptA : letter === 'B' ? setOptB : letter === 'C' ? setOptC : letter === 'D' ? setOptD : setOptE;

                    return (
                      <div key={letter} className="flex items-center gap-2">
                        <span className="w-6 font-bold text-slate-700 text-center font-mono">
                          {letter})
                        </span>
                        <input
                          type="text"
                          value={val}
                          onChange={(e) => setVal(e.target.value)}
                          placeholder={`${letter} şıkkı metni...`}
                          className="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs text-slate-800 focus:bg-white focus:border-teal-500"
                        />
                      </div>
                    );
                  })}
                </div>

                <div className="flex items-center gap-2 pt-2 border-t border-slate-100 text-xs">
                  <span className="font-semibold text-slate-700">Hatırlanan Doğru Cevap:</span>
                  {(['A', 'B', 'C', 'D', 'E'] as const).map((letter) => (
                    <button
                      key={letter}
                      type="button"
                      onClick={() => setClaimedAnswer(claimedAnswer === letter ? undefined : letter)}
                      className={`w-7 h-7 rounded-md font-mono font-bold transition-all cursor-pointer ${
                        claimedAnswer === letter
                          ? 'bg-emerald-600 text-white shadow-xs scale-105'
                          : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                      }`}
                    >
                      {letter}
                    </button>
                  ))}
                  {claimedAnswer && (
                    <button
                      type="button"
                      onClick={() => setClaimedAnswer(undefined)}
                      className="text-[11px] text-slate-400 hover:text-slate-600 underline ml-2"
                    >
                      Temizle
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Submit Button */}
          <div className="pt-2 flex flex-col sm:flex-row items-center justify-between gap-3">
            <p className="text-[11px] text-slate-500 leading-normal">
              🛡️ Eklenen tüm parçalar güvenle veritabanında saklanır ve yapay zeka rekonstrüksiyonunda değerlendirilir.
            </p>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full sm:w-auto bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white px-6 py-2.5 rounded-xl text-sm font-bold flex items-center justify-center gap-2 shadow-sm transition-all cursor-pointer disabled:opacity-50 active:scale-95 shrink-0"
            >
              <Send className="w-4 h-4" />
              <span>{isSubmitting ? 'Havuza Kaydediliyor...' : 'Soruyu Havuza Ekle ve Kaydet'}</span>
            </button>
          </div>
        </form>
      </div>

      {/* Secondary Fast Navigation Tiles */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {/* Tile 1: Question Matrix */}
        <button
          onClick={() => onNavigateTab('matrix')}
          className="bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs hover:shadow-md hover:border-teal-400 transition-all text-left flex items-start gap-3 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-700 flex items-center justify-center shrink-0 group-hover:bg-teal-600 group-hover:text-white transition-colors">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900 group-hover:text-teal-800 transition-colors">
              1-{targetCount} Soru Haritası
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Hangi soruların dolduğunu, hangilerinin eksik olduğunu matris üzerinden inceleyin.
            </p>
          </div>
        </button>

        {/* Tile 2: A4 PDF Exam Booklet */}
        <button
          onClick={() => onNavigateTab('booklet')}
          className="bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs hover:shadow-md hover:border-teal-400 transition-all text-left flex items-start gap-3 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center shrink-0 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900 group-hover:text-emerald-800 transition-colors">
              A4 Soru Kitapçığı & PDF
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Fakülte sınav formatında iki sütunlu çözümlü veya deneme kitapçığı yazdırın / indirin.
            </p>
          </div>
        </button>

        {/* Tile 3: Practice Exam Mode */}
        <button
          onClick={() => onNavigateTab('practice')}
          className="bg-white p-5 rounded-2xl border border-slate-200 shadow-2xs hover:shadow-md hover:border-teal-400 transition-all text-left flex items-start gap-3 cursor-pointer group"
        >
          <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-700 flex items-center justify-center shrink-0 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
            <GraduationCap className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900 group-hover:text-indigo-800 transition-colors">
              Sınav Deneme Modu
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Çıkmış soruları süre tutarak çözün, optik cevaplayıp anında puanınızı görün.
            </p>
          </div>
        </button>
      </div>

      {/* Admin Quick Notification Bar (If Admin) */}
      {isAdmin && unassignedCount > 0 && (
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-amber-900">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
            <span>
              <strong>Yönetici Bildirimi:</strong> Bu kurulda henüz bir numaraya yerleştirilmemiş <strong>{unassignedCount} adet</strong> numarasız soru bulunuyor.
            </span>
          </div>

          <button
            onClick={onOpenAdminPanel}
            className="bg-amber-600 hover:bg-amber-700 text-white font-bold px-3 py-1.5 rounded-lg shrink-0 cursor-pointer transition-colors"
          >
            Muallak Soruları İncele & Numaraya Ata ➔
          </button>
        </div>
      )}
    </div>
  );
};
