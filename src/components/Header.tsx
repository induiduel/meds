import React from 'react';
import { 
  Stethoscope, 
  Sparkles, 
  PlusCircle, 
  BookOpen, 
  Layers, 
  Printer, 
  CheckCircle2, 
  FolderPlus, 
  ShieldCheck, 
  Cloud, 
  LogOut, 
  FileText, 
  LogIn, 
  Trophy, 
  BookMarked,
  Brain,
  Cpu
} from 'lucide-react';
import { Committee } from '../types';
import { AppUser, ADMIN_EMAIL, setLocalAdminSession } from '../services/auth';

interface HeaderProps {
  committees: Committee[];
  selectedCommitteeId: string;
  onSelectCommittee: (id: string) => void;
  activeTab: 'quick_add' | 'questions' | 'past_exams' | 'matrix' | 'leaderboard' | 'notes' | 'practice' | 'booklet';
  setActiveTab: (tab: 'quick_add' | 'questions' | 'past_exams' | 'matrix' | 'leaderboard' | 'notes' | 'practice' | 'booklet') => void;
  onOpenContributeModal: () => void;
  onOpenNewCommitteeModal: () => void;
  onOpenAdminPanel: () => void;
  onOpenPastExamModal?: () => void;
  onOpenNotebookLMModal?: () => void;
  onOpenSubagentMonitor?: () => void;
  onOpenProfileModal?: () => void;
  onOpenAuthModal?: (mode: 'login' | 'register' | 'admin') => void;
  completedCount: number;
  totalCount: number;
  targetCount: number;
  // Auth & Drive Props
  currentUser: AppUser | null;
  isAdmin: boolean;
  onLogin: () => void;
  onLogout: () => void;
  isLoggingIn: boolean;
  onUploadToDrive: () => void;
  isUploadingToDrive: boolean;
  driveLastUploadedLink: string | null;
  onOpenPdfModal: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  committees,
  selectedCommitteeId,
  onSelectCommittee,
  activeTab,
  setActiveTab,
  onOpenContributeModal,
  onOpenNewCommitteeModal,
  onOpenAdminPanel,
  onOpenPastExamModal,
  onOpenNotebookLMModal,
  onOpenSubagentMonitor,
  onOpenProfileModal,
  onOpenAuthModal,
  completedCount,
  totalCount,
  targetCount,
  currentUser,
  isAdmin,
  onLogin,
  onLogout,
  isLoggingIn,
  onUploadToDrive,
  isUploadingToDrive,
  driveLastUploadedLink,
  onOpenPdfModal,
}) => {
  const currentCommittee = committees.find((c) => c.id === selectedCommitteeId);
  const percentComplete = targetCount > 0 ? Math.round((completedCount / targetCount) * 100) : 0;

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">
      {/* Top Professional Banner */}
      <div className="bg-gradient-to-r from-teal-950 via-teal-900 to-slate-950 text-white px-4 py-1.5 text-xs flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="bg-teal-500/20 text-teal-200 border border-teal-400/30 px-2 py-0.5 rounded-full font-semibold flex items-center gap-1.5">
            <Stethoscope className="w-3.5 h-3.5 text-teal-300" />
            Tıp Fakültesi Soru Sistemi
          </span>
          <span className="hidden sm:inline text-slate-200">
            Kolektif Soru Toplama, Ders Notu & Slayt Eşleştirme Sistemi
          </span>
        </div>

        <div className="flex items-center gap-3 text-slate-200 text-[11px]">
          <span className="text-teal-300 font-medium">
            {currentCommittee?.code || 'TIP 300'} • {currentCommittee?.name || 'Aktif Kurul'}
          </span>
          {currentCommittee?.examDate && (
            <span className="bg-white/10 px-2 py-0.5 rounded text-slate-200">
              Sınav: {currentCommittee.examDate}
            </span>
          )}
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          {/* Logo & Subtitle */}
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-teal-600 to-emerald-600 flex items-center justify-center text-white shadow-md shadow-teal-700/20">
              <Stethoscope className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-1.5">
                  MedSoru <span className="text-teal-600 font-extrabold">Kurul</span>
                </h1>
                <span className="text-[11px] font-semibold uppercase tracking-wider bg-teal-50 text-teal-700 border border-teal-200 px-2 py-0.5 rounded-md">
                  Dönem 3
                </span>
                {isAdmin && (
                  <span className="text-[10px] font-bold uppercase tracking-wider bg-amber-100 text-amber-900 border border-amber-300 px-2 py-0.5 rounded-full flex items-center gap-1">
                    <ShieldCheck className="w-3 h-3 text-amber-700" />
                    Admin
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-500">
                Öğrenci Hafıza Havuzu, Ders Notu Eşleştirme ve Soru Arşivi
              </p>
            </div>
          </div>

          {/* Right Action buttons: Committee, Drive, Admin, Auth, Contribute */}
          <div className="flex flex-wrap items-center gap-1.5 sm:gap-2.5">
            {/* Committee selector */}
            <div className="flex items-center gap-1 bg-slate-50 border border-slate-200 rounded-lg p-1">
              <select
                value={selectedCommitteeId}
                onChange={(e) => onSelectCommittee(e.target.value)}
                className="bg-transparent text-xs sm:text-sm font-medium text-slate-800 py-1 px-1 sm:px-2 pr-5 outline-hidden cursor-pointer max-w-[140px] sm:max-w-[220px] md:max-w-xs truncate"
              >
                {committees.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} ({c.targetCount} Soru)
                  </option>
                ))}
              </select>
              {isAdmin && (
                <button
                  onClick={onOpenNewCommitteeModal}
                  title="Yeni Kurul / Komite Ekle"
                  className="p-1 text-slate-400 hover:text-teal-600 hover:bg-white rounded transition-colors"
                >
                  <FolderPlus className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* High-Quality A4 Exam Booklet & PDF Generator (Visible to all students/users on desktop/tablet) */}
            <button
              onClick={onOpenPdfModal}
              className="hidden md:inline-flex bg-white hover:bg-slate-50 border border-slate-200 hover:border-teal-400 text-slate-800 px-3 py-2 rounded-lg text-xs font-semibold items-center gap-1.5 shadow-2xs transition-all cursor-pointer active:scale-95"
              title="A4 formatında soru kitapçığı oluştur, yazdır veya PDF olarak indir"
            >
              <FileText className="w-4 h-4 text-teal-600" />
              <span>PDF Kitapçık</span>
            </button>

            {/* Google Drive PDF Save Button - ONLY VISIBLE TO ADMIN */}
            {isAdmin && (
              <button
                onClick={onUploadToDrive}
                disabled={isUploadingToDrive}
                className={`hidden md:inline-flex px-3 py-2 rounded-lg text-xs font-semibold items-center gap-1.5 border shadow-2xs transition-all cursor-pointer ${
                  driveLastUploadedLink
                    ? 'bg-emerald-50 border-emerald-300 text-emerald-800 hover:bg-emerald-100'
                    : 'bg-teal-50 border-teal-200 text-teal-800 hover:bg-teal-100'
                }`}
                title="Tüm çıkmış soruları PDF olarak Google Drive klasörüne kaydeder (Yönetici Özel)"
              >
                <Cloud className={`w-4 h-4 ${driveLastUploadedLink ? 'text-emerald-600' : 'text-teal-600'}`} />
                <span>
                  {isUploadingToDrive
                    ? 'Drive\'a Yükleniyor...'
                    : driveLastUploadedLink
                    ? 'Drive\'da Güncel'
                    : 'Drive\'a Kaydet'}
                </span>
              </button>
            )}

            {/* NotebookLM & Gemini Direct Connect Button - ONLY VISIBLE TO ADMIN */}
            {isAdmin && onOpenNotebookLMModal && (
              <button
                onClick={onOpenNotebookLMModal}
                className="hidden md:inline-flex bg-purple-50 hover:bg-purple-100 text-purple-950 border border-purple-300 px-3 py-2 rounded-lg text-xs font-bold items-center gap-1.5 shadow-2xs transition-all cursor-pointer active:scale-95"
                title="NotebookLM ve Gemini ile veritabanı eşitleme ve kaynak dışa aktarımı"
              >
                <Brain className="w-3.5 h-3.5 text-purple-700" />
                <span>NotebookLM / Gemini</span>
              </button>
            )}

            {/* Admin Past Exam Importer Button */}
            {isAdmin && onOpenPastExamModal && (
              <button
                onClick={onOpenPastExamModal}
                className="hidden md:inline-flex bg-emerald-50 hover:bg-emerald-100 text-emerald-950 border border-emerald-300 px-3 py-2 rounded-lg text-xs font-bold items-center gap-1.5 shadow-2xs transition-all cursor-pointer active:scale-95"
                title="Geçmiş yılların çıkmış sorularını yapay zekayla yükle"
              >
                <Sparkles className="w-3.5 h-3.5 text-emerald-700" />
                <span>Çıkmış Soru Yükle</span>
              </button>
            )}

            {/* AI Subagent & Worker Monitor Button */}
            {onOpenSubagentMonitor && (
              <button
                onClick={onOpenSubagentMonitor}
                className="hidden sm:inline-flex bg-slate-900 hover:bg-slate-800 text-teal-300 border border-slate-700 px-2.5 sm:px-3 py-1.5 sm:py-2 rounded-lg text-xs font-bold items-center gap-1.5 shadow-xs transition-all cursor-pointer active:scale-95"
                title="Yapay zeka subagentleri, OCR süreçleri ve yerel sunucu durumunu izle"
              >
                <Cpu className="w-3.5 h-3.5 text-teal-400 animate-pulse" />
                <span className="whitespace-nowrap">AI Subagent</span>
              </button>
            )}

            {/* Admin Panel Button - Prominently visible on all screen sizes */}
            <button
              onClick={() => {
                if (!isAdmin) {
                  setLocalAdminSession(ADMIN_EMAIL);
                }
                onOpenAdminPanel();
              }}
              className="px-2.5 sm:px-3 py-1.5 sm:py-2 rounded-lg text-xs font-bold inline-flex items-center gap-1.5 shadow-xs transition-all cursor-pointer active:scale-95 bg-amber-400 hover:bg-amber-300 text-slate-950 font-black ring-2 ring-amber-400/50"
              title="MedSoru Yönetici Paneli & Otomasyonlar"
            >
              <ShieldCheck className="w-4 h-4 text-slate-950" />
              <span className="whitespace-nowrap font-extrabold">Admin Paneli</span>
            </button>

            {/* Google Sign-in / User Profile */}
            {currentUser ? (
              <div className="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-lg p-1 px-2.5">
                <button
                  type="button"
                  onClick={onOpenProfileModal}
                  className="flex items-center gap-2 hover:opacity-80 transition-opacity cursor-pointer text-left"
                  title="Öğrenci profilini ve 11 haneli numaranı düzenle"
                >
                  {currentUser.photoURL ? (
                    <img
                      src={currentUser.photoURL}
                      alt={currentUser.displayName || 'User'}
                      className="w-6 h-6 rounded-full border border-slate-300"
                    />
                  ) : (
                    <div className="w-6 h-6 rounded-full bg-teal-700 text-white text-[11px] font-bold flex items-center justify-center">
                      {(currentUser.displayName || currentUser.email || 'Ö')[0].toUpperCase()}
                    </div>
                  )}
                  <div className="text-left hidden sm:block">
                    <span className="text-[11px] font-bold text-slate-800 block leading-tight truncate max-w-[130px]">
                      {currentUser.displayName || currentUser.email?.split('@')[0]}
                    </span>
                    <span className="text-[9px] text-teal-700 font-semibold block leading-none truncate max-w-[130px]">
                      {currentUser.studentNumber ? `No: ${currentUser.studentNumber}` : currentUser.email}
                    </span>
                  </div>
                </button>
                <button
                  onClick={onLogout}
                  title="Çıkış Yap"
                  className="text-slate-400 hover:text-rose-600 p-1 rounded transition-colors cursor-pointer ml-1"
                >
                  <LogOut className="w-3.5 h-3.5" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-1 sm:gap-1.5">
                <button
                  onClick={() => onOpenAuthModal ? onOpenAuthModal('login') : onLogin()}
                  className="bg-white hover:bg-slate-50 border border-slate-300 text-slate-800 px-2 sm:px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1 shadow-2xs transition-all cursor-pointer active:scale-95"
                  title="Öğrenci girişi yap veya yeni kayıt ol"
                >
                  <LogIn className="w-3.5 h-3.5 text-teal-700" />
                  <span className="hidden xs:inline">Öğrenci Girişi</span>
                  <span className="xs:hidden">Giriş</span>
                </button>

                <button
                  onClick={() => onOpenAuthModal ? onOpenAuthModal('admin') : onLogin()}
                  disabled={isLoggingIn}
                  className="bg-slate-900 hover:bg-slate-800 text-amber-300 border border-slate-800 px-2 sm:px-2.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1 shadow-2xs transition-all cursor-pointer active:scale-95"
                  title="Yönetici girişi (nofrostlife@gmail.com)"
                >
                  <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
                  <span className="hidden xs:inline">{isLoggingIn ? 'Giriş...' : 'Yönetici Girişi'}</span>
                  <span className="xs:hidden">Admin</span>
                </button>
              </div>
            )}

            {/* Quick Contribute CTA */}
            <button
              onClick={onOpenContributeModal}
              className="bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white px-2.5 sm:px-3.5 py-1.5 sm:py-2 rounded-lg text-xs sm:text-sm font-semibold flex items-center gap-1.5 sm:gap-2 shadow-sm transition-all shadow-teal-600/20 cursor-pointer active:scale-95 whitespace-nowrap shrink-0"
            >
              <PlusCircle className="w-4 h-4 shrink-0" />
              <span className="hidden xs:inline">Soru Katkısı Yap</span>
              <span className="xs:hidden">+ Katkı</span>
            </button>
          </div>
        </div>

        {/* Navigation Tabs and Progress Bar */}
        <div className="mt-3 pt-2 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <nav className="flex items-center gap-1 overflow-x-auto pb-1 sm:pb-0">
            <button
              onClick={() => setActiveTab('quick_add')}
              className={`px-3 py-1.5 rounded-lg text-xs sm:text-sm font-bold flex items-center gap-1.5 transition-colors cursor-pointer shrink-0 ${
                activeTab === 'quick_add'
                  ? 'bg-teal-700 text-white shadow-xs'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <PlusCircle className="w-4 h-4" />
              <span>Hızlı Soru Ekle</span>
            </button>

            <button
              onClick={() => setActiveTab('questions')}
              className={`px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium flex items-center gap-1.5 transition-colors cursor-pointer shrink-0 ${
                activeTab === 'questions'
                  ? 'bg-teal-50 text-teal-800 border border-teal-200'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              <span>Soru Havuzu ({totalCount})</span>
            </button>

            <button
              onClick={() => setActiveTab('past_exams')}
              className={`px-3 py-1.5 rounded-lg text-xs sm:text-sm font-semibold flex items-center gap-1.5 transition-all cursor-pointer shrink-0 ${
                activeTab === 'past_exams'
                  ? 'bg-gradient-to-r from-amber-500 to-amber-600 text-white shadow-xs font-bold'
                  : 'text-slate-700 hover:bg-amber-50/80 hover:text-amber-800'
              }`}
            >
              <Sparkles className={`w-4 h-4 ${activeTab === 'past_exams' ? 'text-amber-200' : 'text-amber-500'}`} />
              <span>Çıkmış Sorular</span>
              <span className={`text-[10px] px-1.5 py-0.5 rounded-full font-bold uppercase tracking-wider ${
                activeTab === 'past_exams' ? 'bg-amber-700/80 text-white' : 'bg-amber-100 text-amber-900 border border-amber-300'
              }`}>
                Arşiv
              </span>
            </button>

            <button
              onClick={() => setActiveTab('matrix')}
              className={`px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium flex items-center gap-1.5 transition-colors cursor-pointer shrink-0 ${
                activeTab === 'matrix'
                  ? 'bg-teal-50 text-teal-800 border border-teal-200'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <Layers className="w-4 h-4" />
              <span>1-{targetCount} Matris</span>
            </button>

            <button
              onClick={() => setActiveTab('leaderboard')}
              className={`px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium flex items-center gap-1.5 transition-colors cursor-pointer shrink-0 ${
                activeTab === 'leaderboard'
                  ? 'bg-amber-50 text-amber-900 border border-amber-300 font-bold'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <Trophy className="w-4 h-4 text-amber-600" />
              <span>Katkı Sıralaması</span>
            </button>

            <button
              onClick={() => setActiveTab('notes')}
              className={`px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium flex items-center gap-1.5 transition-colors cursor-pointer shrink-0 ${
                activeTab === 'notes'
                  ? 'bg-teal-50 text-teal-800 border border-teal-200'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <BookMarked className="w-4 h-4 text-teal-600" />
              <span>Ders Notları & Slaytlar</span>
            </button>

            <button
              onClick={() => setActiveTab('practice')}
              className={`px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium flex items-center gap-1.5 transition-colors cursor-pointer shrink-0 ${
                activeTab === 'practice'
                  ? 'bg-teal-50 text-teal-800 border border-teal-200'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <Brain className="w-4 h-4" />
              <span>Test Çöz</span>
            </button>

            <button
              onClick={() => setActiveTab('booklet')}
              className={`px-3 py-1.5 rounded-lg text-xs sm:text-sm font-medium flex items-center gap-1.5 transition-colors cursor-pointer shrink-0 ${
                activeTab === 'booklet'
                  ? 'bg-teal-50 text-teal-800 border border-teal-200'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <Printer className="w-4 h-4" />
              <span>A4 Kitapçık</span>
            </button>
          </nav>

          {/* Quick Progress Mini Badge */}
          <div className="flex items-center gap-3 bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-lg text-xs shrink-0">
            <div className="flex items-center gap-1.5 text-slate-700">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span className="font-semibold">{completedCount} / {targetCount}</span>
              <span className="text-slate-500">Soru</span>
            </div>
            <div className="w-16 bg-slate-200 rounded-full h-2 overflow-hidden">
              <div
                className="bg-emerald-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${Math.min(percentComplete, 100)}%` }}
              />
            </div>
            <span className="font-bold text-emerald-700">%{percentComplete}</span>
          </div>
        </div>
      </div>
    </header>
  );
};

