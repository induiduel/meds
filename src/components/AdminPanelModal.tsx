import React, { useState } from 'react';
import { 
  X, 
  ShieldCheck, 
  Database, 
  Download, 
  Upload, 
  RotateCcw, 
  Trash2, 
  Edit3, 
  CheckCircle2, 
  AlertTriangle,
  Search,
  Sparkles,
  Zap,
  FilePlus,
  BookOpen,
  Cloud,
  GitBranch,
  Terminal,
  Clock,
  Calendar,
  Check,
  ExternalLink,
  Layers,
  RefreshCw,
  FolderOpen
} from 'lucide-react';
import { QuestionItem, Committee } from '../types';
import { AdminEditQuestionModal } from './AdminEditQuestionModal';
import { AdminPastExamImporterModal } from './AdminPastExamImporterModal';
import { InfoPopover } from './InfoPopover';
import { ApiService } from '../services/api';
import { runDriveSyncAndAutoMatch, TARGET_DRIVE_FOLDER_ID, TARGET_DRIVE_FOLDER_URL } from '../services/driveAutomation';

interface AdminPanelModalProps {
  isOpen: boolean;
  onClose: () => void;
  adminEmail: string;
  committees: Committee[];
  questions: QuestionItem[];
  selectedCommitteeId: string;
  onRefreshData: () => Promise<void>;
}

export const AdminPanelModal: React.FC<AdminPanelModalProps> = ({
  isOpen,
  onClose,
  adminEmail,
  committees,
  questions,
  selectedCommitteeId,
  onRefreshData,
}) => {
  const [activeTab, setActiveTab] = useState<'questions' | 'automations' | 'database'>('questions');
  const [editingQuestion, setEditingQuestion] = useState<QuestionItem | null>(null);
  const [isPastExamImporterOpen, setIsPastExamImporterOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  // Automations state
  const [driveAutoActive, setDriveAutoActive] = useState(() => {
    return localStorage.getItem('medsoru_admin_drive_active') !== 'false';
  });
  const [driveSyncDays, setDriveSyncDays] = useState('Hafta İçi (Pazartesi - Cuma)');
  const [driveSyncHour, setDriveSyncHour] = useState('18:00');
  const [isSyncingDriveManual, setIsSyncingDriveManual] = useState(false);
  const [driveSyncFeedback, setDriveSyncFeedback] = useState<string | null>(null);

  // Civan's Notes Sync state
  const [isSyncingCivan, setIsSyncingCivan] = useState(false);
  const [civanSyncResult, setCivanSyncResult] = useState<string | null>(null);

  // Git Push state
  const [githubToken, setGithubToken] = useState('');
  const [isPushingGit, setIsPushingGit] = useState(false);
  const [gitPushResult, setGitPushResult] = useState<string | null>(null);
  const [gitPushError, setGitPushError] = useState<string | null>(null);

  // Destructive confirmation state
  const [confirmDialog, setConfirmDialog] = useState<{
    isOpen: boolean;
    title: string;
    description: string;
    onConfirm: () => Promise<void>;
  } | null>(null);

  if (!isOpen) return null;

  const currentCommitteeQuestions = questions.filter(
    (q) => !selectedCommitteeId || q.committeeId === selectedCommitteeId
  );

  const filteredQuestions = currentCommitteeQuestions.filter(
    (q) =>
      q.questionNumber.toString().includes(searchQuery) ||
      q.topic.toLowerCase().includes(searchQuery.toLowerCase()) ||
      q.discipline.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Handle Question Edit
  const handleSaveQuestion = async (updated: Partial<QuestionItem>) => {
    if (!editingQuestion) return;
    try {
      await ApiService.adminUpdateQuestion(adminEmail, editingQuestion.id, updated);
      setActionMessage(`Soru #${editingQuestion.questionNumber} başarıyla güncellendi.`);
      await onRefreshData();
    } catch (e: any) {
      alert('Hata: ' + e.message);
    }
  };

  // Handle Question Delete with explicit confirmation
  const handleDeleteQuestion = (question: QuestionItem) => {
    setConfirmDialog({
      isOpen: true,
      title: `Soru #${question.questionNumber} Silinsin mi?`,
      description: `Bu soruyu ve öğrencilerin girdiği tüm hafıza parçalarını kalıcı olarak silmek üzeresiniz. Bu işlem geri alınamaz.`,
      onConfirm: async () => {
        setIsProcessing(true);
        try {
          await ApiService.adminDeleteQuestion(adminEmail, question.id);
          setActionMessage(`Soru #${question.questionNumber} silindi.`);
          await onRefreshData();
        } finally {
          setIsProcessing(false);
          setConfirmDialog(null);
        }
      },
    });
  };

  // Export JSON Backup
  const handleExportJson = async () => {
    try {
      const data = await ApiService.adminExportDb();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `medsoru_database_backup_${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e: any) {
      alert('Dışa aktarma hatası: ' + e.message);
    }
  };

  // Import JSON Backup with confirmation
  const handleImportFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (event) => {
      try {
        const json = JSON.parse(event.target?.result as string);
        setConfirmDialog({
          isOpen: true,
          title: 'Veritabanı Yedeği İçe Aktarılsın mı?',
          description: `Seçilen JSON dosyasındaki veriler mevcut veritabanının üzerine yazılacaktır (${json.questions?.length || 0} soru). Onaylıyor musunuz?`,
          onConfirm: async () => {
            setIsProcessing(true);
            try {
              await ApiService.adminImportDb(adminEmail, json);
              setActionMessage('Veritabanı başarıyla içe aktarıldı.');
              await onRefreshData();
            } finally {
              setIsProcessing(false);
              setConfirmDialog(null);
            }
          },
        });
      } catch (err) {
        alert('Geçersiz JSON dosyası.');
      }
    };
    reader.readAsText(file);
  };

  // Reset to seed with confirmation
  const handleResetDatabase = () => {
    setConfirmDialog({
      isOpen: true,
      title: 'Veritabanı Sıfırlansın mı?',
      description: 'Tüm sorular sıfırlanacak ve orijinal tıp fakültesi başlangıç verileri geri yüklenecektir. Bu işlem geri alınamaz.',
      onConfirm: async () => {
        setIsProcessing(true);
        try {
          await ApiService.adminResetDb(adminEmail);
          setActionMessage('Veritabanı sıfırlandı.');
          await onRefreshData();
        } finally {
          setIsProcessing(false);
          setConfirmDialog(null);
        }
      },
    });
  };

  // Drive sync manual trigger
  const handleTriggerDriveSync = async () => {
    setIsSyncingDriveManual(true);
    setDriveSyncFeedback('Google Drive taranıyor...');
    try {
      const res = await runDriveSyncAndAutoMatch(
        selectedCommitteeId || 'donem3-kurul1',
        questions,
        (msg) => setDriveSyncFeedback(msg)
      );
      setDriveSyncFeedback(`✓ Drive senkronizasyonu tamamlandı. ${res.syncedNotes.length} ders slaytı ve ${res.matchedQuestions.length} soru eşleşmesi işlendi.`);
      await onRefreshData();
    } catch (e: any) {
      setDriveSyncFeedback(`Hata: ${e.message}`);
    } finally {
      setIsSyncingDriveManual(false);
    }
  };

  // Civan's Notes Sync
  const handleSyncCivan = async () => {
    setIsSyncingCivan(true);
    setCivanSyncResult(null);
    try {
      const res = await fetch('/api/automation/civan-sync', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-admin-email': adminEmail,
        },
        body: JSON.stringify({ adminEmail }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Senkronizasyon başarısız');
      setCivanSyncResult(`✓ ${data.message}`);
      await onRefreshData();
    } catch (err: any) {
      setCivanSyncResult(`Hata: ${err.message}`);
    } finally {
      setIsSyncingCivan(false);
    }
  };

  // GitHub Push
  const handleGitPush = async () => {
    setIsPushingGit(true);
    setGitPushResult(null);
    setGitPushError(null);
    try {
      const res = await fetch('/api/admin/git-push', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-admin-email': adminEmail,
        },
        body: JSON.stringify({
          adminEmail,
          githubToken: githubToken.trim() || undefined,
          commitMessage: `feat: MedSoru veritabani ve otomasyon guncellemesi (${new Date().toLocaleDateString('tr-TR')})`,
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || data.details || 'Push işlemi başarısız');
      }
      setGitPushResult(data.message || 'GitHub deposu başarıyla güncellendi!');
    } catch (err: any) {
      setGitPushError(err.message);
    } finally {
      setIsPushingGit(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl max-w-4xl w-full shadow-2xl border border-slate-200 overflow-hidden my-4 sm:my-6 flex flex-col max-h-[92vh]">
        {/* Header */}
        <div className="bg-slate-900 text-white p-4 sm:p-5 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-teal-400 border border-teal-400/30 flex items-center justify-center">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-sm sm:text-base">MedSoru Yönetici & Otomasyon Kontrol Merkezi</h3>
                <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full">
                  Admin
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Hesap: <strong className="text-teal-300">{adminEmail}</strong> (Tam Yetki)
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

        {/* Tab Navigation */}
        <div className="bg-slate-100 border-b border-slate-200 px-4 flex items-center gap-2 shrink-0">
          <button
            onClick={() => setActiveTab('questions')}
            className={`py-3 px-3 text-xs font-bold border-b-2 flex items-center gap-1.5 transition-all cursor-pointer ${
              activeTab === 'questions'
                ? 'border-teal-700 text-teal-900 bg-white shadow-2xs'
                : 'border-transparent text-slate-600 hover:text-slate-900'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5 text-teal-600" />
            <span>Soru Havuzu ({questions.length})</span>
          </button>

          <button
            onClick={() => setActiveTab('automations')}
            className={`py-3 px-3 text-xs font-bold border-b-2 flex items-center gap-1.5 transition-all cursor-pointer ${
              activeTab === 'automations'
                ? 'border-teal-700 text-teal-900 bg-white shadow-2xs'
                : 'border-transparent text-slate-600 hover:text-slate-900'
            }`}
          >
            <Zap className="w-3.5 h-3.5 text-amber-600" />
            <span>Otomasyonlar & Masaüstü İşleyici</span>
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          </button>

          <button
            onClick={() => setActiveTab('database')}
            className={`py-3 px-3 text-xs font-bold border-b-2 flex items-center gap-1.5 transition-all cursor-pointer ${
              activeTab === 'database'
                ? 'border-teal-700 text-teal-900 bg-white shadow-2xs'
                : 'border-transparent text-slate-600 hover:text-slate-900'
            }`}
          >
            <Database className="w-3.5 h-3.5 text-teal-600" />
            <span>Veritabanı & Yedekler</span>
          </button>
        </div>

        {/* Action alert message */}
        {actionMessage && (
          <div className="bg-teal-50 border-b border-teal-200 px-5 py-2 text-xs text-teal-900 flex items-center justify-between">
            <span className="flex items-center gap-1.5 font-medium">
              <CheckCircle2 className="w-4 h-4 text-teal-600" />
              {actionMessage}
            </span>
            <button
              onClick={() => setActionMessage(null)}
              className="text-teal-600 hover:text-teal-800 text-xs font-bold"
            >
              Kapat
            </button>
          </div>
        )}

        {/* Tab 1: Questions Management */}
        {activeTab === 'questions' && (
          <div className="p-4 sm:p-6 space-y-4 overflow-y-auto flex-1 text-xs">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="relative flex-1">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Soru no, konu veya branş ara..."
                  className="w-full pl-9 pr-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500"
                />
              </div>

              <button
                onClick={() => setIsPastExamImporterOpen(true)}
                className="bg-teal-700 hover:bg-teal-800 text-white font-bold px-4 py-2 rounded-lg flex items-center gap-1.5 shadow-xs cursor-pointer"
              >
                <Sparkles className="w-4 h-4 text-teal-200" />
                <span>Çıkmış Soru Yükle (PDF/DOCX)</span>
              </button>
            </div>

            <div className="space-y-2">
              {filteredQuestions.slice(0, 30).map((q) => (
                <div
                  key={q.id}
                  className="p-3 bg-white rounded-lg border border-slate-200 hover:border-teal-400 transition-all flex items-center justify-between gap-3"
                >
                  <div className="space-y-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-900">#{q.questionNumber}</span>
                      <span className="bg-teal-100 text-teal-800 text-[10px] font-bold px-2 py-0.5 rounded">
                        {q.discipline}
                      </span>
                      <span className="text-slate-600 font-medium truncate">{q.topic}</span>
                    </div>
                    <p className="text-slate-500 line-clamp-1 italic">
                      {q.reconstruction?.stem || q.fragments?.[0]?.text || 'Soru metni henüz tamamlanmadı'}
                    </p>
                  </div>

                  <div className="flex items-center gap-1 shrink-0">
                    <button
                      onClick={() => setEditingQuestion(q)}
                      className="p-1.5 hover:bg-slate-100 rounded text-slate-600 hover:text-teal-700 cursor-pointer"
                      title="Düzenle"
                    >
                      <Edit3 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleDeleteQuestion(q)}
                      className="p-1.5 hover:bg-rose-50 rounded text-slate-400 hover:text-rose-600 cursor-pointer"
                      title="Sil"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tab 2: Automations Hub */}
        {activeTab === 'automations' && (
          <div className="p-4 sm:p-6 space-y-5 overflow-y-auto flex-1 text-xs">
            {/* 1. Google Drive Automation Card */}
            <div className="bg-gradient-to-br from-teal-50 to-cyan-50 border border-teal-200 rounded-xl p-4 sm:p-5 space-y-3">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Cloud className="w-5 h-5 text-teal-700" />
                  <h4 className="font-bold text-sm text-slate-900">Google Drive Klasör Senkronizasyonu</h4>
                  <span className="bg-teal-700 text-white font-bold text-[10px] px-2 py-0.5 rounded-full">
                    Otomasyon
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  <label className="flex items-center gap-2 text-xs font-semibold cursor-pointer">
                    <span>Durum:</span>
                    <input
                      type="checkbox"
                      checked={driveAutoActive}
                      onChange={(e) => {
                        setDriveAutoActive(e.target.checked);
                        localStorage.setItem('medsoru_admin_drive_active', String(e.target.checked));
                      }}
                      className="w-4 h-4 text-teal-600 rounded"
                    />
                    <span className={driveAutoActive ? 'text-emerald-700 font-bold' : 'text-slate-500'}>
                      {driveAutoActive ? 'Aktif' : 'Devre Dışı'}
                    </span>
                  </label>
                </div>
              </div>

              <p className="text-slate-600 text-xs">
                Hedef Google Drive klasörüne yüklenen yeni ders slaytları PDF olarak taranır, sayfa sayfa metne dönüştürülür ve öğrenci sorularıyla otomatik eşleştirilir.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2 border-t border-teal-200/80">
                <div className="space-y-1">
                  <label className="text-[11px] font-bold text-slate-700 flex items-center gap-1">
                    <Calendar className="w-3.5 h-3.5 text-teal-600" />
                    Çalışma Günleri:
                  </label>
                  <select
                    value={driveSyncDays}
                    onChange={(e) => setDriveSyncDays(e.target.value)}
                    className="w-full text-xs p-2 rounded-lg bg-white border border-slate-300 font-semibold"
                  >
                    <option value="Hafta İçi (Pazartesi - Cuma)">Hafta İçi (Pazartesi - Cuma)</option>
                    <option value="Her Gün (Hafta Sonu Dahil)">Her Gün (Hafta Sonu Dahil)</option>
                    <option value="Sadece Sınav Haftası">Sadece Sınav Haftası (Yoğun Mod)</option>
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="text-[11px] font-bold text-slate-700 flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-teal-600" />
                    Çalışma Saati:
                  </label>
                  <input
                    type="time"
                    value={driveSyncHour}
                    onChange={(e) => setDriveSyncHour(e.target.value)}
                    className="w-full text-xs p-2 rounded-lg bg-white border border-slate-300 font-semibold"
                  />
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                <a
                  href={TARGET_DRIVE_FOLDER_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-teal-800 hover:text-teal-950 font-bold text-xs flex items-center gap-1"
                >
                  <FolderOpen className="w-4 h-4 text-teal-600" />
                  <span>Hedef Klasörü Drive'da Aç ({TARGET_DRIVE_FOLDER_ID})</span>
                  <ExternalLink className="w-3 h-3 text-slate-400" />
                </a>

                <button
                  onClick={handleTriggerDriveSync}
                  disabled={isSyncingDriveManual}
                  className="bg-teal-700 hover:bg-teal-800 disabled:opacity-50 text-white font-bold px-4 py-2 rounded-lg flex items-center gap-1.5 shadow-xs cursor-pointer active:scale-95"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isSyncingDriveManual ? 'animate-spin' : ''}`} />
                  <span>Şimdi Manuel Tara & Slaytları Renderla</span>
                </button>
              </div>

              {driveSyncFeedback && (
                <div className="p-2.5 bg-white border border-teal-300 rounded-lg text-xs font-semibold text-teal-950 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-teal-600 shrink-0" />
                  <span>{driveSyncFeedback}</span>
                </div>
              )}
            </div>

            {/* 2. Civan'ın Notları (civaninotlari.vercel.app) Integration Card */}
            <div className="bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200 rounded-xl p-4 sm:p-5 space-y-3">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-amber-700" />
                  <h4 className="font-bold text-sm text-slate-900">Civan'ın Notları Çıkmış Soru Entegrasyonu</h4>
                  <span className="bg-amber-700 text-white font-bold text-[10px] px-2 py-0.5 rounded-full">
                    426 Soru
                  </span>
                </div>

                <a
                  href="https://civaninotlari.vercel.app/#/landing"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-amber-800 hover:text-amber-950 font-bold text-xs flex items-center gap-1"
                >
                  <span>civaninotlari.vercel.app</span>
                  <ExternalLink className="w-3 h-3 text-slate-400" />
                </a>
              </div>

              <div className="bg-white/80 p-3 rounded-lg border border-amber-200 text-slate-700 text-xs leading-relaxed space-y-1.5">
                <p>
                  <strong>Maliyet & Kota Tasarrufu Bildirimi:</strong> Kullanıcı talebi doğrultusunda, sunucu depolama ve yapay zeka faturalandırmasında ücrete yakalanmamak için <strong>ders notları veritabanına eklenmemektedir</strong>.
                </p>
                <p>
                  Yalnızca 2020-2026 dönemine ait <strong>426 adet doğrulanmış Kurul 1 çıkmış sorusu</strong> (Patoloji, Farmakoloji, Enfeksiyon Hastalıkları, Genetik, Halk Sağlığı, Üroloji) standart formata dönüştürülmüştür.
                </p>
              </div>

              <div className="flex items-center justify-between gap-3 pt-1">
                <span className="text-slate-600 font-semibold text-xs">
                  Hazır Durum: 426 çıkmış soru (Şıklar, vaka analizleri ve klinik açıklamalar ile)
                </span>

                <button
                  onClick={handleSyncCivan}
                  disabled={isSyncingCivan}
                  className="bg-amber-600 hover:bg-amber-700 disabled:opacity-50 text-white font-bold px-4 py-2 rounded-lg flex items-center gap-1.5 shadow-xs cursor-pointer active:scale-95"
                >
                  <Sparkles className="w-3.5 h-3.5 text-amber-200" />
                  <span>{isSyncingCivan ? 'Aktarılıyor...' : '426 Çıkmış Soruyu Soru Havuzuna Aktar'}</span>
                </button>
              </div>

              {civanSyncResult && (
                <div className="p-2.5 bg-white border border-amber-300 rounded-lg text-xs font-semibold text-amber-950 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>{civanSyncResult}</span>
                </div>
              )}
            </div>

            {/* 3. Local Desktop Background Daemon Card (Zero Token Cost) */}
            <div className="bg-slate-900 text-white rounded-xl p-4 sm:p-5 space-y-3">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Terminal className="w-5 h-5 text-emerald-400" />
                  <h4 className="font-bold text-sm text-white">Yerel Bilgisayar Arka Plan Çalışanı (Desktop Worker)</h4>
                  <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full">
                    Sıfır Token / Sınırsız Hız
                  </span>
                </div>
              </div>

              <p className="text-slate-300 text-xs leading-relaxed">
                Bilgisayarınızı açık bırakarak yoğun slayt ve çıkmışları yapay zekaya token harcatmadan kendi internetiniz ve işlemciniz üzerinden otomatik taratabilirsiniz.
              </p>

              <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 font-mono text-xs text-emerald-400 space-y-1">
                <div className="text-slate-500">// Terminalde veya Komut Satırında Çalıştırın:</div>
                <div className="select-all font-bold">node scripts/local-drive-sync-agent.mjs</div>
                <div className="text-slate-500 pt-1">// Veya Windows'ta çift tıklayarak başlatın:</div>
                <div className="text-slate-300">start-worker.bat</div>
              </div>

              <div className="text-slate-400 text-[11px] flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-emerald-400" />
                <span>Drive klasörüne dosya eklediğiniz an otomatik olarak arka planda okunup MedSoru'ya kaydedilir.</span>
              </div>
            </div>

            {/* 4. GitHub Push & Sync Card */}
            <div className="bg-white border border-slate-200 rounded-xl p-4 sm:p-5 space-y-3 shadow-2xs">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <GitBranch className="w-5 h-5 text-slate-800" />
                  <h4 className="font-bold text-sm text-slate-900">GitHub Senkronizasyonu & Push</h4>
                  <span className="bg-slate-100 text-slate-800 text-[10px] font-bold px-2 py-0.5 rounded-full">
                    induiduel/meds
                  </span>
                </div>

                <a
                  href="https://github.com/induiduel/meds"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-teal-700 hover:text-teal-900 font-bold text-xs flex items-center gap-1"
                >
                  <span>Depoyu Görüntüle</span>
                  <ExternalLink className="w-3 h-3 text-slate-400" />
                </a>
              </div>

              <div className="space-y-1.5">
                <label className="text-[11px] font-bold text-slate-700">
                  GitHub Personal Access Token (Opsiyonel / İzin için):
                </label>
                <div className="flex gap-2">
                  <input
                    type="password"
                    value={githubToken}
                    onChange={(e) => setGithubToken(e.target.value)}
                    placeholder="ghp_xxxxxxxxxxxx (GitHub Settings > Developer Settings > Tokens)"
                    className="flex-1 text-xs p-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 font-mono"
                  />
                  <button
                    onClick={handleGitPush}
                    disabled={isPushingGit}
                    className="bg-slate-900 hover:bg-slate-800 disabled:opacity-50 text-white font-bold px-4 py-2 rounded-lg flex items-center gap-1.5 cursor-pointer shrink-0"
                  >
                    <GitBranch className="w-3.5 h-3.5 text-teal-400" />
                    <span>{isPushingGit ? 'Pushlanıyor...' : 'GitHub\'a Pushla'}</span>
                  </button>
                </div>
              </div>

              {gitPushResult && (
                <div className="p-2.5 bg-emerald-50 border border-emerald-300 text-emerald-950 rounded-lg text-xs font-semibold flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>{gitPushResult}</span>
                </div>
              )}

              {gitPushError && (
                <div className="p-2.5 bg-rose-50 border border-rose-300 text-rose-950 rounded-lg text-xs font-semibold space-y-1">
                  <div className="flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />
                    <span>Push Hatası: {gitPushError}</span>
                  </div>
                  <p className="text-[11px] text-slate-600">
                    GitHub şifreleri yerine "Personal Access Token (classic/fine-grained)" kabul etmektedir. Token girerek işlemi onaylayabilirsiniz.
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Tab 3: Database & Backup */}
        {activeTab === 'database' && (
          <div className="p-4 sm:p-6 space-y-5 overflow-y-auto flex-1 text-xs">
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-3">
              <h4 className="font-bold text-slate-900 text-sm flex items-center gap-2">
                <Database className="w-4 h-4 text-teal-600" />
                Veritabanı Yedekleme ve Sıfırlama
              </h4>
              <p className="text-slate-500 text-[11px]">
                Tüm soru havuzunu tek tıkla JSON formatında indirebilir, geri yükleyebilir veya eşik testi çalıştırabilirsiniz.
              </p>

              <div className="flex flex-wrap items-center gap-2 pt-2">
                <button
                  onClick={handleExportJson}
                  className="bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 cursor-pointer shadow-2xs"
                >
                  <Download className="w-3.5 h-3.5 text-slate-500" />
                  <span>JSON İndir</span>
                </button>

                <label className="bg-white hover:bg-slate-100 border border-slate-200 text-slate-700 font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 cursor-pointer shadow-2xs">
                  <Upload className="w-3.5 h-3.5 text-slate-500" />
                  <span>JSON Yükle</span>
                  <input
                    type="file"
                    accept=".json"
                    onChange={handleImportFile}
                    className="hidden"
                  />
                </label>

                <button
                  onClick={handleResetDatabase}
                  className="bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 cursor-pointer"
                >
                  <RotateCcw className="w-3.5 h-3.5 text-rose-600" />
                  <span>Sıfırla</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="bg-slate-50 border-t border-slate-200 p-4 flex items-center justify-between text-xs text-slate-500 shrink-0">
          <span>
            nofrostlife@gmail.com olarak yönetici yetkilerine sahipsiniz.
          </span>
          <button
            onClick={onClose}
            className="bg-slate-800 hover:bg-slate-900 text-white font-semibold px-4 py-1.5 rounded-lg text-xs cursor-pointer"
          >
            Kapat
          </button>
        </div>
      </div>

      {/* Edit Modal */}
      {editingQuestion && (
        <AdminEditQuestionModal
          isOpen={true}
          onClose={() => setEditingQuestion(null)}
          question={editingQuestion}
          adminEmail={adminEmail}
          onSaveQuestion={handleSaveQuestion}
        />
      )}

      {/* Confirmation Dialog */}
      {confirmDialog && (
        <div className="fixed inset-0 z-60 bg-slate-950/70 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-5 shadow-2xl space-y-4 border border-slate-200">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-full bg-rose-100 text-rose-600 shrink-0">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-slate-900 text-sm">{confirmDialog.title}</h4>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  {confirmDialog.description}
                </p>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                type="button"
                onClick={() => setConfirmDialog(null)}
                disabled={isProcessing}
                className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-100 cursor-pointer"
              >
                Vazgeç
              </button>
              <button
                type="button"
                onClick={confirmDialog.onConfirm}
                disabled={isProcessing}
                className="bg-rose-600 hover:bg-rose-700 text-white px-4 py-1.5 rounded-lg text-xs font-bold cursor-pointer disabled:opacity-50"
              >
                {isProcessing ? 'İşleniyor...' : 'Onayla'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Admin Past Exam Importer Modal */}
      <AdminPastExamImporterModal
        isOpen={isPastExamImporterOpen}
        onClose={() => setIsPastExamImporterOpen(false)}
        adminEmail={adminEmail}
        committees={committees}
        selectedCommitteeId={selectedCommitteeId}
        onImportSuccess={async () => {
          await onRefreshData();
          setActionMessage('Çıkmış sorular başarıyla veritabanına aktarıldı ve soru havuzuna eklendi.');
        }}
      />
    </div>
  );
};
