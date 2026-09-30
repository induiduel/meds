import React, { useState } from 'react';
import { 
  Sparkles, 
  ThumbsUp, 
  MessageSquare, 
  Plus, 
  CheckCircle2, 
  AlertTriangle, 
  ChevronDown, 
  ChevronUp, 
  Send, 
  Bot, 
  BookOpen, 
  Tag, 
  RefreshCw,
  HelpCircle,
  Check,
  CheckCheck
} from 'lucide-react';
import { QuestionItem } from '../types';
import { AppUser } from '../services/auth';
import { Edit3, History, User, BookMarked, ExternalLink } from 'lucide-react';

interface QuestionCardProps {
  question: QuestionItem;
  currentUser?: AppUser | null;
  isAdmin?: boolean;
  onEditQuestion?: (question: QuestionItem) => void;
  onOpenHistory?: (question: QuestionItem) => void;
  onAddFragment: (questionId: string, text: string, author: string, type: 'stem' | 'clue' | 'option') => Promise<void>;
  onUpvoteFragment: (questionId: string, fragmentId: string) => Promise<void>;
  onAddOption: (questionId: string, key: 'A' | 'B' | 'C' | 'D' | 'E', text: string, suggestedBy: string) => Promise<void>;
  onUpvoteOption: (questionId: string, key: 'A' | 'B' | 'C' | 'D' | 'E') => Promise<void>;
  onReconstructWithAi: (questionId: string) => Promise<void>;
  onSetClaimedAnswer: (questionId: string, answer: 'A' | 'B' | 'C' | 'D' | 'E') => Promise<void>;
  isReconstructing: boolean;
}

const SAVED_NAME_KEY = 'medsoru_saved_contributor_name';

export const QuestionCard: React.FC<QuestionCardProps> = ({
  question,
  currentUser,
  isAdmin = false,
  onEditQuestion,
  onOpenHistory,
  onAddFragment,
  onUpvoteFragment,
  onAddOption,
  onUpvoteOption,
  onReconstructWithAi,
  onSetClaimedAnswer,
  isReconstructing,
}) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const [showAddFragment, setShowAddFragment] = useState(false);
  const [showAddOption, setShowAddOption] = useState(false);

  const isMyQuestion = !!currentUser && (
    question.contributedByUid === currentUser.uid ||
    (currentUser.email && question.contributedByName === currentUser.displayName) ||
    question.fragments.some((f) => f.authorUid === currentUser.uid || (currentUser.displayName && f.author === currentUser.displayName)) ||
    question.options.some((o) => o.suggestedByUid === currentUser.uid || (currentUser.displayName && o.suggestedBy === currentUser.displayName))
  );

  const revisionCount = question.revisions?.length || 0;
  
  // Fragment form state with remembered author
  const [fragmentText, setFragmentText] = useState('');
  const [fragmentAuthor, setFragmentAuthor] = useState(() => localStorage.getItem(SAVED_NAME_KEY) || '');
  const [fragmentType, setFragmentType] = useState<'stem' | 'clue' | 'option'>('clue');
  const [isSubmittingFragment, setIsSubmittingFragment] = useState(false);

  // Option form state with remembered author
  const [optionKey, setOptionKey] = useState<'A' | 'B' | 'C' | 'D' | 'E'>('A');
  const [optionText, setOptionText] = useState('');
  const [optionAuthor, setOptionAuthor] = useState(() => localStorage.getItem(SAVED_NAME_KEY) || '');
  const [isSubmittingOption, setIsSubmittingOption] = useState(false);

  const handleAuthorUpdate = (val: string) => {
    setFragmentAuthor(val);
    setOptionAuthor(val);
    localStorage.setItem(SAVED_NAME_KEY, val);
  };

  const hasReconstruction = !!question.reconstruction;

  const handleFragmentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!fragmentText.trim()) return;
    setIsSubmittingFragment(true);
    try {
      await onAddFragment(question.id, fragmentText, fragmentAuthor || 'Anonim Tıbbiyeli', fragmentType);
      setFragmentText('');
      setShowAddFragment(false);
    } finally {
      setIsSubmittingFragment(false);
    }
  };

  const handleOptionSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!optionText.trim()) return;
    setIsSubmittingOption(true);
    try {
      await onAddOption(question.id, optionKey, optionText, optionAuthor || 'Anonim Tıbbiyeli');
      setOptionText('');
      setShowAddOption(false);
    } finally {
      setIsSubmittingOption(false);
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs transition-all hover:border-slate-300">
      {/* Card Header */}
      <div className="p-4 sm:p-5 border-b border-slate-100 flex flex-wrap items-center justify-between gap-3 bg-slate-50/50">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-teal-800 text-white font-bold flex items-center justify-center text-base shadow-xs">
            #{question.questionNumber}
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-teal-100/80 text-teal-800 border border-teal-200">
                {question.discipline}
              </span>
              {isMyQuestion && (
                <span className="text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-300 px-2 py-0.5 rounded-full flex items-center gap-1">
                  <User className="w-3 h-3 text-amber-700" />
                  Senin Katkın
                </span>
              )}
              {revisionCount > 0 && (
                <button
                  type="button"
                  onClick={() => onOpenHistory?.(question)}
                  className="text-[10px] font-semibold bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200 px-2 py-0.5 rounded-full flex items-center gap-1 cursor-pointer transition-colors"
                  title="Tüm versiyon geçmişini gör"
                >
                  <History className="w-3 h-3 text-teal-600" />
                  <span>v{revisionCount} Geçmiş</span>
                </button>
              )}
              <h3 className="text-base font-bold text-slate-900">{question.topic}</h3>
            </div>
            <div className="flex items-center gap-2 text-xs text-slate-500 mt-0.5">
              <span>{question.fragments.length} hafıza parçası</span>
              <span>•</span>
              <span>{question.options.length} öğrenci şıkkı</span>
              {question.contributedByName && (
                <>
                  <span>•</span>
                  <span className="text-slate-600 font-medium">
                    Ekleyen: {question.contributedByName}
                    {question.contributedByStudentNumber ? ` (${question.contributedByStudentNumber})` : ''}
                  </span>
                </>
              )}
              {hasReconstruction && (
                <>
                  <span>•</span>
                  <span className="text-emerald-700 font-semibold flex items-center gap-1">
                    <Sparkles className="w-3 h-3" />
                    AI Güven: %{question.reconstruction?.confidenceScore}
                  </span>
                </>
              )}
            </div>

            {/* Lecture Note & Slide Match Badge */}
            {question.lectureReference && (
              <div className="mt-2 inline-flex flex-wrap items-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-900 px-2.5 py-1 rounded-lg text-xs">
                <BookMarked className="w-3.5 h-3.5 text-emerald-700 shrink-0" />
                <span>
                  <strong>Ders Slaytı:</strong> {question.lectureReference.noteTitle} • <strong>Sayfa {question.lectureReference.pageNumber}</strong>
                </span>
                <span className="text-[10px] bg-emerald-200/80 text-emerald-950 font-bold px-1.5 py-0.2 rounded">
                  %{question.lectureReference.confidenceScore} Eşleşme
                </span>
                {question.lectureReference.driveFileUrl && (
                  <a
                    href={question.lectureReference.driveFileUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="inline-flex items-center gap-1 font-bold text-emerald-800 hover:text-emerald-950 bg-white border border-emerald-300 px-2 py-0.5 rounded text-[11px] shadow-2xs hover:bg-emerald-100 transition-colors"
                    title="Google Drive'da ilgili slayt PDF dosyasını aç"
                  >
                    <ExternalLink className="w-3 h-3 text-emerald-700" />
                    <span>Drive'da Slaytı Aç</span>
                  </a>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          {/* Edit Button for Owner or Admin */}
          {(isMyQuestion || isAdmin) && onEditQuestion && (
            <button
              onClick={() => onEditQuestion(question)}
              className="bg-white hover:bg-teal-50 border border-slate-300 hover:border-teal-400 text-slate-800 hover:text-teal-900 text-xs font-semibold px-2.5 py-1.5 rounded-lg flex items-center gap-1.5 shadow-2xs transition-all cursor-pointer active:scale-95"
              title="Soruyu düzenle (Eski versiyon silinmeden yeni versiyon olarak eklenir)"
            >
              <Edit3 className="w-3.5 h-3.5 text-teal-700" />
              <span>Düzenle</span>
            </button>
          )}

          <button
            onClick={() => onReconstructWithAi(question.id)}
            disabled={isReconstructing || (question.fragments.length === 0 && question.options.length === 0)}
            className="bg-gradient-to-r from-emerald-600 to-teal-700 hover:from-emerald-700 hover:to-teal-800 text-white text-xs font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 shadow-xs transition-all disabled:opacity-50 cursor-pointer active:scale-95"
            title="Öğrencilerin hatırladığı tüm parçaları yapay zeka ile birleştirip tam bir soru ve 5 şık haline getirir"
          >
            {isReconstructing ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>AI Sentezliyor...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-3.5 h-3.5" />
                <span>{hasReconstruction ? 'AI ile Yenile' : 'AI ile Rekonstrükte Et'}</span>
              </>
            )}
          </button>

          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors cursor-pointer"
          >
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {isExpanded && (
        <div className="p-4 sm:p-5 space-y-6">
          {/* Main Grid: Student Crowdsourced Pool (Left) & AI Reconstructed View (Right) */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* LEFT COLUMN: Student Memory Fragments */}
            <div className="space-y-4">
              <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                <div className="flex items-center gap-2">
                  <MessageSquare className="w-4 h-4 text-teal-600" />
                  <h4 className="text-sm font-bold text-slate-800">
                    Öğrenci Hafıza Havuzu ({question.fragments.length})
                  </h4>
                </div>
                <button
                  onClick={() => setShowAddFragment(!showAddFragment)}
                  className="text-xs text-teal-700 hover:text-teal-800 font-medium flex items-center gap-1 bg-teal-50 px-2 py-1 rounded border border-teal-200 cursor-pointer"
                >
                  <Plus className="w-3 h-3" />
                  <span>İpucu / Parça Ekle</span>
                </button>
              </div>

              {/* Add Fragment Form */}
              {showAddFragment && (
                <form onSubmit={handleFragmentSubmit} className="bg-slate-50 border border-slate-200 rounded-lg p-3 space-y-2.5">
                  <div className="flex items-center justify-between text-xs text-slate-600">
                    <span className="font-semibold">Aklınızda Kalanı Ekleyin:</span>
                    <select
                      value={fragmentType}
                      onChange={(e) => setFragmentType(e.target.value as any)}
                      className="bg-white border border-slate-200 text-xs rounded px-2 py-0.5"
                    >
                      <option value="stem">Soru Kökü Parçası</option>
                      <option value="clue">Klinik/Lab İpucu</option>
                      <option value="option">Hatırlanan Şık Detayı</option>
                    </select>
                  </div>
                  <textarea
                    rows={2}
                    placeholder="Örnek: Hoca bu vakada hastanın EKG'sinde ST elevasyonu ve troponin yüksekliği var demişti..."
                    value={fragmentText}
                    onChange={(e) => setFragmentText(e.target.value)}
                    className="w-full bg-white border border-slate-200 rounded p-2 text-xs text-slate-800 focus:outline-hidden focus:ring-1 focus:ring-teal-500"
                    required
                  />
                  <div className="flex items-center justify-between gap-2">
                    <input
                      type="text"
                      placeholder="Rumuzunuz (ör: Dr. Ahmet Tıp-3)"
                      value={fragmentAuthor}
                      onChange={(e) => handleAuthorUpdate(e.target.value)}
                      className="bg-white border border-slate-200 rounded px-2 py-1 text-xs w-48 text-slate-700"
                    />
                    <div className="flex items-center gap-1.5">
                      <button
                        type="button"
                        onClick={() => setShowAddFragment(false)}
                        className="text-xs text-slate-500 px-2 py-1 hover:bg-slate-200 rounded cursor-pointer"
                      >
                        İptal
                      </button>
                      <button
                        type="submit"
                        disabled={isSubmittingFragment}
                        className="bg-teal-700 text-white text-xs px-3 py-1 rounded font-semibold hover:bg-teal-800 disabled:opacity-50 cursor-pointer"
                      >
                        {isSubmittingFragment ? 'Kaydediliyor...' : 'Havuza Ekle'}
                      </button>
                    </div>
                  </div>
                </form>
              )}

              {/* Fragment List */}
              {question.fragments.length === 0 ? (
                <div className="text-center py-6 bg-slate-50 rounded-lg border border-dashed border-slate-200 text-slate-400 text-xs">
                  Henüz hafıza parçası girilmedi. İlk hatırlayan siz olun!
                </div>
              ) : (
                <div className="space-y-2.5 max-h-80 overflow-y-auto pr-1">
                  {question.fragments.map((frag) => (
                    <div
                      key={frag.id}
                      className="bg-slate-50/80 border border-slate-200/90 rounded-lg p-3 text-xs space-y-1.5 hover:bg-slate-50 transition-colors"
                    >
                      <div className="flex items-center justify-between text-slate-500">
                        <div className="flex items-center gap-1.5">
                          <span className="font-semibold text-slate-700">{frag.author}</span>
                          <span className="text-[10px] bg-slate-200 px-1.5 py-0.2 rounded text-slate-600">
                            {frag.type === 'stem' ? 'Soru Kökü' : frag.type === 'clue' ? 'İpucu' : 'Şık'}
                          </span>
                        </div>
                        <button
                          onClick={() => onUpvoteFragment(question.id, frag.id)}
                          className="flex items-center gap-1 text-[11px] text-slate-500 hover:text-teal-700 bg-white border border-slate-200 px-1.5 py-0.5 rounded cursor-pointer active:scale-95 transition-all"
                          title="Ben de böyle hatırlıyorum (+1)"
                        >
                          <ThumbsUp className="w-3 h-3 text-teal-600" />
                          <span>{frag.upvotes || 0}</span>
                        </button>
                      </div>
                      <p className="text-slate-800 leading-relaxed font-sans">{frag.text}</p>
                    </div>
                  ))}
                </div>
              )}

              {/* Student Options Input & List */}
              <div className="pt-2">
                <div className="flex items-center justify-between pb-1.5 border-b border-slate-100">
                  <h5 className="text-xs font-bold text-slate-700">Hatırlanan Şıklar (A - E)</h5>
                  <button
                    onClick={() => setShowAddOption(!showAddOption)}
                    className="text-[11px] text-teal-700 hover:text-teal-800 font-medium flex items-center gap-1 cursor-pointer"
                  >
                    <Plus className="w-3 h-3" />
                    <span>Şık Ekle</span>
                  </button>
                </div>

                {showAddOption && (
                  <form onSubmit={handleOptionSubmit} className="mt-2 bg-slate-50 border border-slate-200 rounded-lg p-2.5 space-y-2">
                    <div className="flex items-center gap-2">
                      <select
                        value={optionKey}
                        onChange={(e) => setOptionKey(e.target.value as any)}
                        className="bg-white border border-slate-200 text-xs font-bold rounded px-2 py-1 text-teal-800"
                      >
                        <option value="A">A</option>
                        <option value="B">B</option>
                        <option value="C">C</option>
                        <option value="D">D</option>
                        <option value="E">E</option>
                      </select>
                      <input
                        type="text"
                        placeholder="Şık metni (ör: Legionella pneumophila)"
                        value={optionText}
                        onChange={(e) => setOptionText(e.target.value)}
                        className="flex-1 bg-white border border-slate-200 rounded px-2 py-1 text-xs text-slate-800 focus:outline-hidden"
                        required
                      />
                    </div>
                    <div className="flex items-center justify-between gap-2">
                      <input
                        type="text"
                        placeholder="Öneren rumuzu (isteğe bağlı)"
                        value={optionAuthor}
                        onChange={(e) => handleAuthorUpdate(e.target.value)}
                        className="bg-white border border-slate-200 rounded px-2 py-0.5 text-xs text-slate-600 w-44"
                      />
                      <div className="flex items-center gap-1">
                        <button
                          type="button"
                          onClick={() => setShowAddOption(false)}
                          className="text-xs text-slate-500 px-2 py-0.5 cursor-pointer"
                        >
                          İptal
                        </button>
                        <button
                          type="submit"
                          disabled={isSubmittingOption}
                          className="bg-teal-700 text-white text-xs px-2.5 py-0.5 rounded font-semibold hover:bg-teal-800 cursor-pointer"
                        >
                          Kaydet
                        </button>
                      </div>
                    </div>
                  </form>
                )}

                {/* Display Student Options */}
                {question.options.length > 0 ? (
                  <div className="mt-2 space-y-1.5">
                    {question.options.map((opt) => (
                      <div
                        key={opt.key}
                        className="flex items-center justify-between bg-slate-50 border border-slate-200/80 rounded px-2.5 py-1.5 text-xs"
                      >
                        <div className="flex items-center gap-2">
                          <span className="w-5 h-5 rounded-full bg-slate-200 font-bold text-slate-700 flex items-center justify-center text-[11px]">
                            {opt.key}
                          </span>
                          <span className="text-slate-800">{opt.text}</span>
                        </div>
                        <div className="flex items-center gap-1.5">
                          {opt.suggestedBy && (
                            <span className="text-[10px] text-slate-400">({opt.suggestedBy})</span>
                          )}
                          <button
                            onClick={() => onUpvoteOption(question.id, opt.key)}
                            className="flex items-center gap-1 text-[10px] text-slate-500 hover:text-teal-700 bg-white border border-slate-200 px-1 py-0.5 rounded cursor-pointer"
                          >
                            <ThumbsUp className="w-2.5 h-2.5 text-teal-600" />
                            <span>{opt.upvotes || 0}</span>
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="mt-2 text-xs text-slate-400 italic">Öğrenciler henüz şık girmedi.</p>
                )}
              </div>
            </div>

            {/* RIGHT COLUMN: AI Reconstructed Final Medical Question */}
            <div className="bg-gradient-to-br from-slate-50 via-teal-50/20 to-emerald-50/20 border border-teal-200/80 rounded-xl p-4 sm:p-5 flex flex-col justify-between shadow-xs">
              <div className="space-y-4">
                <div className="flex items-start justify-between pb-2 border-b border-teal-200/60">
                  <div className="flex items-start gap-2">
                    <div className="p-1 rounded-md bg-teal-600 text-white mt-0.5">
                      <Bot className="w-4 h-4" />
                    </div>
                    <div>
                      <div className="flex items-center gap-1.5">
                        <h4 className="text-sm font-bold text-slate-900">
                          AI Versiyonu (Rekonstrüksiyon)
                        </h4>
                        {hasReconstruction && (
                          <span className="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-1.5 py-0.5 rounded-full">
                            %{question.reconstruction?.confidenceScore} Güven
                          </span>
                        )}
                      </div>
                      <p className="text-[10px] text-teal-800/80 mt-0.5">
                        Orijinal soru ve öğrenci hafıza parçaları asla silinmez, korunur.
                      </p>
                    </div>
                  </div>

                  {hasReconstruction && (
                    <span className="text-[10px] text-slate-400 shrink-0">
                      {new Date(question.reconstruction!.lastUpdated).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  )}
                </div>

                {/* Student-Selected Most Accurate Answer Bar */}
                <div className="bg-amber-50/90 border border-amber-200 rounded-lg p-2.5 text-xs flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-amber-600 shrink-0" />
                    <span className="font-bold text-amber-900">Öğrencilerin Belirlediği En Doğru Şık:</span>
                    <span className="bg-amber-500 text-white font-black px-2 py-0.5 rounded text-xs shadow-2xs">
                      {question.claimedAnswer || 'Seçilmedi'}
                    </span>
                  </div>

                  <div className="flex items-center gap-1">
                    <span className="text-[10px] text-amber-800 font-semibold mr-0.5">Şık Seç:</span>
                    {(['A', 'B', 'C', 'D', 'E'] as const).map((key) => (
                      <button
                        key={key}
                        type="button"
                        onClick={() => onSetClaimedAnswer(question.id, key)}
                        className={`w-6 h-6 rounded text-xs font-bold transition-all cursor-pointer ${
                          question.claimedAnswer === key
                            ? 'bg-amber-600 text-white ring-2 ring-amber-400 shadow-2xs'
                            : 'bg-white hover:bg-amber-100 text-amber-900 border border-amber-300'
                        }`}
                        title={`${key} şıkkını kurulda sorulan en doğru cevap olarak işaretle`}
                      >
                        {key}
                      </button>
                    ))}
                  </div>
                </div>

                {!hasReconstruction ? (
                  <div className="text-center py-10 space-y-3">
                    <Sparkles className="w-10 h-10 text-teal-400 mx-auto animate-pulse" />
                    <div>
                      <p className="text-sm font-semibold text-slate-700">
                        Bu soru henüz AI ile rekonstrükte edilmedi
                      </p>
                      <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
                        Soldaki öğrenci hafıza havuzundaki parçaları ve şıkları birleştirip tam bir TUS/Kurul sorusu üretmek için yukarıdaki butona tıklayın.
                      </p>
                    </div>
                    <button
                      onClick={() => onReconstructWithAi(question.id)}
                      disabled={isReconstructing || (question.fragments.length === 0 && question.options.length === 0)}
                      className="bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold px-4 py-2 rounded-lg inline-flex items-center gap-2 shadow-sm cursor-pointer disabled:opacity-50"
                    >
                      <Sparkles className="w-3.5 h-3.5" />
                      <span>Hafıza Parçalarını Birleştir & Sentezle</span>
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {/* Stem */}
                    <div className="bg-white p-3.5 rounded-lg border border-slate-200/90 shadow-2xs">
                      <span className="text-[10px] font-bold tracking-wider uppercase text-teal-800 bg-teal-50 px-1.5 py-0.5 rounded border border-teal-200 mb-1.5 inline-block">
                        Rekonstrükte Soru Kökü
                      </span>
                      <p className="text-sm font-medium text-slate-900 leading-relaxed font-serif">
                        {question.reconstruction?.stem}
                      </p>
                    </div>

                    {/* Options (5 options: A-E) */}
                    <div className="space-y-1.5">
                      <span className="text-[11px] font-bold text-slate-600 block">Şıklar:</span>
                      {question.reconstruction?.options.map((opt) => {
                        const isCorrect = question.reconstruction?.correctAnswer === opt.key;
                        return (
                          <div
                            key={opt.key}
                            className={`p-2.5 rounded-lg border text-xs flex items-center justify-between gap-2 transition-all ${
                              isCorrect
                                ? 'bg-emerald-50 border-emerald-400 text-emerald-950 font-medium ring-1 ring-emerald-500/20'
                                : 'bg-white border-slate-200 text-slate-800'
                            }`}
                          >
                            <div className="flex items-center gap-2.5">
                              <span
                                className={`w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold shrink-0 ${
                                  isCorrect
                                    ? 'bg-emerald-600 text-white'
                                    : 'bg-slate-100 text-slate-700'
                                }`}
                              >
                                {opt.key}
                              </span>
                              <span className="leading-snug">{opt.text}</span>
                            </div>

                            <div className="flex items-center gap-1.5 shrink-0">
                              {opt.isAiFilled && (
                                <span className="text-[9px] bg-sky-100 text-sky-800 px-1.5 py-0.5 rounded border border-sky-200">
                                  AI Çeldirici
                                </span>
                              )}
                              {isCorrect && (
                                <span className="bg-emerald-600 text-white text-[10px] font-bold px-2 py-0.5 rounded flex items-center gap-0.5">
                                  <Check className="w-3 h-3" /> Doğru Cevap
                                </span>
                              )}
                            </div>
                          </div>
                        );
                      })}
                    </div>

                    {/* Medical Explanation & Rationale */}
                    {question.reconstruction?.explanation && (
                      <div className="bg-emerald-50/70 border border-emerald-200 rounded-lg p-3 text-xs space-y-1">
                        <span className="font-bold text-emerald-900 flex items-center gap-1">
                          <BookOpen className="w-3.5 h-3.5 text-emerald-700" />
                          Tıbbi Gerekçe & Öğrenme Notu:
                        </span>
                        <p className="text-emerald-950 leading-relaxed">
                          {question.reconstruction.explanation}
                        </p>
                      </div>
                    )}

                    {/* Discrepancies / Missing details note */}
                    {question.reconstruction?.notesAndDiscrepancies && (
                      <div className="bg-amber-50/70 border border-amber-200 rounded-lg p-2.5 text-xs text-amber-900 flex items-start gap-1.5">
                        <AlertTriangle className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
                        <div>
                          <span className="font-semibold">Hafıza & Çelişki Notu: </span>
                          <span>{question.reconstruction.notesAndDiscrepancies}</span>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Bottom footer bar for Right Column */}
              {hasReconstruction && (
                <div className="mt-4 pt-3 border-t border-teal-200/60 flex items-center justify-between text-xs text-slate-500">
                  <div className="flex items-center gap-1.5">
                    <span className="text-slate-600 font-medium">Doğruluk Güvencesi:</span>
                    <div className="w-20 bg-slate-200 rounded-full h-1.5 overflow-hidden">
                      <div
                        className="bg-emerald-600 h-1.5 rounded-full"
                        style={{ width: `${question.reconstruction?.confidenceScore || 0}%` }}
                      />
                    </div>
                    <span className="font-bold text-emerald-700">%{question.reconstruction?.confidenceScore}</span>
                  </div>

                  <span className="text-[11px] text-teal-700 font-medium">
                    Tıp Fakültesi Standartlarında Derlendi
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
