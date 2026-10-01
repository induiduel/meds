import React, { useState, useEffect } from 'react';
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
  FolderOpen,
  Users,
  Mail,
  UserPlus,
  UserCheck,
  Hash,
  User,
  Key,
  Send,
  Server,
  Settings,
  Lock,
  Bell,
  Monitor,
  Play,
  Square
} from 'lucide-react';
import { QuestionItem, Committee } from '../types';
import { AdminEditQuestionModal } from './AdminEditQuestionModal';
import { AdminPastExamImporterModal } from './AdminPastExamImporterModal';
import { InfoPopover } from './InfoPopover';
import { ApiService } from '../services/api';
import { FirestoreDbService } from '../services/firestoreDb';
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
  const [activeTab, setActiveTab] = useState<'questions' | 'automations' | 'database' | 'users'>('questions');
  const [editingQuestion, setEditingQuestion] = useState<QuestionItem | null>(null);
  const [isPastExamImporterOpen, setIsPastExamImporterOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  // User Management State
  const [usersList, setUsersList] = useState<any[]>([]);
  const [isLoadingUsers, setIsLoadingUsers] = useState(false);
  const [userSearchQuery, setUserSearchQuery] = useState('');
  const [isCreatingUser, setIsCreatingUser] = useState(false);
  const [newEmail, setNewEmail] = useState('');
  const [newName, setNewName] = useState('');
  const [newStudentNumber, setNewStudentNumber] = useState('');
  const [newRole, setNewRole] = useState<'student' | 'admin'>('student');
  const [isSyncingAuthDb, setIsSyncingAuthDb] = useState(false);
  const [userSyncMessage, setUserSyncMessage] = useState<string | null>(null);
  const [sendingWelcomeForEmail, setSendingWelcomeForEmail] = useState<string | null>(null);

  // SMTP Configuration State
  const [smtpConfig, setSmtpConfig] = useState<{
    enabled: boolean;
    service: string;
    host: string;
    port: number;
    secure: boolean;
    user: string;
    from: string;
    hasPass: boolean;
    passMasked: string;
  } | null>(null);
  const [smtpUser, setSmtpUser] = useState('nofrostlife@gmail.com');
  const [smtpPass, setSmtpPass] = useState('');
  const [smtpFrom, setSmtpFrom] = useState('');
  const [showSmtpSettings, setShowSmtpSettings] = useState(false);
  const [isLoadingSmtp, setIsLoadingSmtp] = useState(false);
  const [isSavingSmtp, setIsSavingSmtp] = useState(false);
  const [isTestingSmtp, setIsTestingSmtp] = useState(false);
  const [smtpTestResult, setSmtpTestResult] = useState<{ success: boolean; message: string; hint?: string } | null>(null);
  const [testEmailTarget, setTestEmailTarget] = useState('nofrostlife@gmail.com');

  // Firestore Questions Sync State
  const [isSyncingFirestore, setIsSyncingFirestore] = useState(false);
  const [firestoreSyncFeedback, setFirestoreSyncFeedback] = useState<string | null>(null);

  // Automations state
  const [workerHeartbeat, setWorkerHeartbeat] = useState<{ isOnline: boolean; diffSeconds?: number; lastHeartbeat?: any } | null>(null);
  const [isCheckingWorker, setIsCheckingWorker] = useState(false);
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

  // Full Local Sync state
  const [isSyncingFullLocal, setIsSyncingFullLocal] = useState(false);
  const [fullLocalSyncFeedback, setFullLocalSyncFeedback] = useState<string | null>(null);

  // Windows Service & Desktop Shortcut state
  const [windowsServiceStatus, setWindowsServiceStatus] = useState<{
    success?: boolean;
    isInstalledOnDesktop?: boolean;
    isRegisteredInStartup?: boolean;
    isRunning?: boolean;
    pids?: number[];
    desktopShortcutPath?: string;
    startupShortcutPath?: string;
    nextWindow?: string;
    lastHeartbeat?: any;
    error?: string;
  } | null>(null);
  const [isLoadingWindowsService, setIsLoadingWindowsService] = useState(false);
  const [isInstallingWindowsService, setIsInstallingWindowsService] = useState(false);
  const [isSendingWindowsNotify, setIsSendingWindowsNotify] = useState(false);
  const [windowsServiceFeedback, setWindowsServiceFeedback] = useState<string | null>(null);

  // Destructive confirmation state
  const [confirmDialog, setConfirmDialog] = useState<{
    isOpen: boolean;
    title: string;
    description: string;
    onConfirm: () => Promise<void>;
  } | null>(null);

  const currentCommitteeQuestions = (questions || []).filter(
    (q) => Boolean(q && (!selectedCommitteeId || q.committeeId === selectedCommitteeId))
  );

  const filteredQuestions = currentCommitteeQuestions.filter(
    (q) =>
      Boolean(q) && (
        (q?.questionNumber?.toString() || '').includes(searchQuery) ||
        (q?.topic || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
        (q?.discipline || '').toLowerCase().includes(searchQuery.toLowerCase())
      )
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

  // Sync all questions from current memory/server to Firestore
  const handleSyncQuestionsToFirestore = async () => {
    if (!questions || questions.length === 0) {
      alert('Soru havuzunda yüklenecek soru bulunmuyor.');
      return;
    }
    setIsSyncingFirestore(true);
    setFirestoreSyncFeedback(`Firebase Firestore bulutuna aktarılıyor (0 / ${questions.length})...`);
    try {
      const res = await FirestoreDbService.batchSaveQuestions(questions);
      setFirestoreSyncFeedback(`✓ ${res.count} adet soru Firebase Firestore bulutuna başarıyla aktarıldı!`);
      await onRefreshData();
    } catch (e: any) {
      setFirestoreSyncFeedback(`Hata: ${e.message || 'Firebase aktarımı başarısız'}`);
    } finally {
      setIsSyncingFirestore(false);
    }
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

  // Full Local Sync Trigger (Drive Crawl, Download, Local OCR & Firebase Sync)
  const handleTriggerFullLocalSync = async () => {
    setIsSyncingFullLocal(true);
    setFullLocalSyncFeedback('Yerel Drive indirme ve OCR çıkarma motoru başlatılıyor...');
    try {
      const res = await fetch('/api/automation/run-full-local-sync', { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        setFullLocalSyncFeedback(`✓ ${data.message} - PDF'ler yerel CPU ile taranıp metinleri ve soruları veritabanına aktarılıyor.`);
        await onRefreshData();
      } else {
        setFullLocalSyncFeedback(`Hata: ${data.error || 'İşlem başlatılamadı'}`);
      }
    } catch (e: any) {
      setFullLocalSyncFeedback(`Hata: ${e.message}`);
    } finally {
      setIsSyncingFullLocal(false);
    }
  };

  // Load and merge users from Server API and Firestore Realtime Database
  const loadUsersData = async () => {
    setIsLoadingUsers(true);
    try {
      const serverUsers = await ApiService.adminGetUsers(adminEmail).catch(() => []);
      const firestoreUsers = await FirestoreDbService.getRegisteredUsers().catch(() => []);

      const map = new Map<string, any>();

      // Admin baseline
      map.set('nofrostlife@gmail.com', {
        uid: 'admin-nofrostlife',
        email: 'nofrostlife@gmail.com',
        displayName: 'Yönetici (nofrostlife)',
        studentNumber: '202311001',
        role: 'admin',
        createdAt: '2026-09-01T08:00:00.000Z',
        lastLoginAt: new Date().toISOString(),
        welcomeEmailSent: true,
      });

      serverUsers.forEach((u: any) => {
        if (!u) return;
        const key = (u.email || u.uid).toLowerCase();
        map.set(key, {
          ...u,
          role: u.email?.toLowerCase() === 'nofrostlife@gmail.com' ? 'admin' : (u.role || 'student'),
        });
      });

      firestoreUsers.forEach((u: any) => {
        if (!u) return;
        const key = (u.email || u.uid || '').toLowerCase();
        if (!key) return;
        if (map.has(key)) {
          const existing = map.get(key);
          map.set(key, {
            ...existing,
            ...u,
            displayName: u.displayName || existing.displayName,
            studentNumber: u.studentNumber || existing.studentNumber,
            role: (u.email?.toLowerCase() === 'nofrostlife@gmail.com' || existing.role === 'admin') ? 'admin' : 'student',
          });
        } else {
          map.set(key, {
            uid: u.uid || ('std-' + Date.now().toString(36)),
            email: u.email || 'anonim@medsoru.local',
            displayName: u.displayName || 'Öğrenci',
            studentNumber: u.studentNumber || null,
            role: u.email?.toLowerCase() === 'nofrostlife@gmail.com' ? 'admin' : 'student',
            createdAt: u.createdAt || new Date().toISOString(),
            lastLoginAt: u.updatedAt || new Date().toISOString(),
            welcomeEmailSent: false,
          });
        }
      });

      const combined = Array.from(map.values()).sort((a, b) => {
        if (a.role === 'admin' && b.role !== 'admin') return -1;
        if (b.role === 'admin' && a.role !== 'admin') return 1;
        return new Date(b.createdAt || 0).getTime() - new Date(a.createdAt || 0).getTime();
      });

      setUsersList(combined);
    } catch (e: any) {
      console.warn('Error loading users:', e);
    } finally {
      setIsLoadingUsers(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      loadUsersData();
    }
  }, [isOpen]);

  const loadSmtpConfig = async () => {
    setIsLoadingSmtp(true);
    try {
      const cfg = await ApiService.getSmtpConfig();
      setSmtpConfig(cfg);
      setSmtpUser(cfg.user || 'nofrostlife@gmail.com');
      setSmtpFrom(cfg.from || `MedSoru Tıp Fakültesi <${cfg.user || 'nofrostlife@gmail.com'}>`);
    } catch (e) {
      console.warn('Could not load SMTP config:', e);
    } finally {
      setIsLoadingSmtp(false);
    }
  };

  const handleSaveSmtp = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setIsSavingSmtp(true);
    setSmtpTestResult(null);
    try {
      const res = await ApiService.saveSmtpConfig({
        user: smtpUser.trim(),
        pass: smtpPass.trim() ? smtpPass.trim() : undefined,
        from: smtpFrom.trim(),
      });
      setSmtpTestResult({
        success: true,
        message: res.message || 'SMTP e-posta sunucu ayarları başarıyla kaydedildi.',
      });
      setSmtpPass('');
      await loadSmtpConfig();
    } catch (e: any) {
      setSmtpTestResult({
        success: false,
        message: e.message || 'SMTP ayarları kaydedilemedi.',
      });
    } finally {
      setIsSavingSmtp(false);
    }
  };

  const handleTestSmtp = async () => {
    setIsTestingSmtp(true);
    setSmtpTestResult(null);
    try {
      const res = await ApiService.testSmtp(testEmailTarget.trim() || smtpUser.trim());
      if (res.success) {
        setSmtpTestResult({
          success: true,
          message: res.message || 'Canlı SMTP bağlantısı ve test e-postası başarıyla gönderildi!',
        });
      } else {
        setSmtpTestResult({
          success: false,
          message: res.error || 'Test e-postası gönderilemedi.',
          hint: res.hint,
        });
      }
    } catch (e: any) {
      setSmtpTestResult({
        success: false,
        message: e.message || 'Bağlantı hatası.',
      });
    } finally {
      setIsTestingSmtp(false);
    }
  };

  const handleManualCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newEmail.trim()) return;
    setIsProcessing(true);
    try {
      const created = await ApiService.adminCreateUser(adminEmail, {
        email: newEmail.trim(),
        displayName: newName.trim() || undefined,
        studentNumber: newStudentNumber.trim() || undefined,
        role: newRole,
      });

      const welcomeRes = await ApiService.sendWelcomeEmail(created.email, created.displayName, created.studentNumber);

      if (welcomeRes.success) {
        setUserSyncMessage(`✓ Kullanıcı ${created.email} eklendi ve hoş geldiniz e-postası başarıyla iletildi.`);
      } else {
        setUserSyncMessage(`⚠️ Kullanıcı ${created.email} eklendi fakat hoş geldiniz maili gönderilemedi: ${welcomeRes.error || ''}`);
      }

      setIsCreatingUser(false);
      setNewEmail('');
      setNewName('');
      setNewStudentNumber('');
      await loadUsersData();
    } catch (err: any) {
      alert('Hata: ' + err.message);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleManualDeleteUser = (u: any) => {
    if (u.email?.toLowerCase() === 'nofrostlife@gmail.com') {
      alert('Ana yönetici hesabı silinemez.');
      return;
    }
    setConfirmDialog({
      isOpen: true,
      title: `${u.displayName || u.email} Kullanıcısı Silinsin mi?`,
      description: 'Bu kullanıcının sistem kaydı veritabanından kalıcı olarak silinecektir. Onaylıyor musunuz?',
      onConfirm: async () => {
        setIsProcessing(true);
        try {
          await ApiService.adminDeleteUser(adminEmail, u.uid);
          setUserSyncMessage(`✓ ${u.email} kullanıcısı veritabanından silindi.`);
          await loadUsersData();
        } finally {
          setIsProcessing(false);
          setConfirmDialog(null);
        }
      },
    });
  };

  const handleSendWelcomeEmail = async (u: any) => {
    setSendingWelcomeForEmail(u.email);
    try {
      const res = await ApiService.sendWelcomeEmail(u.email, u.displayName, u.studentNumber);
      if (res.success) {
        setUserSyncMessage(`✓ Hoş geldiniz e-postası ${u.email} adresine iletildi.`);
        await loadUsersData();
      } else {
        const hintText = res.hint ? `\n\n📌 Çözüm: ${res.hint}` : '';
        const instruct = res.instructions?.length ? `\n\nAdımlar:\n${res.instructions.join('\n')}` : '';
        alert(`❌ E-posta Gönderilemedi:\n${res.error || 'Bilinmeyen hata'}${hintText}${instruct}`);
      }
    } catch (e: any) {
      alert('Hata: ' + e.message);
    } finally {
      setSendingWelcomeForEmail(null);
    }
  };

  const handleSyncAuthDbBridge = async () => {
    setIsSyncingAuthDb(true);
    setUserSyncMessage('Firebase Auth ve Realtime Veritabanı senkronize ediliyor...');
    try {
      await loadUsersData();
      setUserSyncMessage('✓ Firebase Auth ve Veritabanı başarıyla senkronize edildi. Tüm kullanıcılar güncel!');
    } catch (err: any) {
      setUserSyncMessage('Hata: ' + err.message);
    } finally {
      setIsSyncingAuthDb(false);
    }
  };

  const checkWorkerStatus = async () => {
    setIsCheckingWorker(true);
    try {
      const res = await fetch('/api/worker/heartbeat');
      const data = await res.json();
      setWorkerHeartbeat(data);
    } catch (e) {
      // ignore
    } finally {
      setIsCheckingWorker(false);
    }
  };

  const loadWindowsServiceStatus = async () => {
    setIsLoadingWindowsService(true);
    try {
      const res = await ApiService.getWindowsServiceStatus();
      setWindowsServiceStatus(res);
    } catch (err) {
      console.warn('Windows service status error:', err);
    } finally {
      setIsLoadingWindowsService(false);
    }
  };

  const handleInstallWindowsService = async () => {
    setIsInstallingWindowsService(true);
    setWindowsServiceFeedback('Masaüstü kısayolu oluşturuluyor, Windows başlangıcına ekleniyor...');
    try {
      const res = await ApiService.installWindowsService();
      setWindowsServiceFeedback(`✓ ${res.message}`);
      await loadWindowsServiceStatus();
      await checkWorkerStatus();
    } catch (err: any) {
      setWindowsServiceFeedback(`Hata: ${err.message}`);
    } finally {
      setIsInstallingWindowsService(false);
    }
  };

  const handleStopWindowsService = async () => {
    setIsInstallingWindowsService(true);
    try {
      const res = await ApiService.stopWindowsService();
      setWindowsServiceFeedback(res.message);
      await loadWindowsServiceStatus();
      await checkWorkerStatus();
    } catch (err: any) {
      setWindowsServiceFeedback(`Hata: ${err.message}`);
    } finally {
      setIsInstallingWindowsService(false);
    }
  };

  const handleSendWindowsTestNotification = async () => {
    setIsSendingWindowsNotify(true);
    try {
      const res = await ApiService.sendWindowsTestNotification(
        'MedSoru Test Bildirimi 🔔',
        'Yönetici panelinden Windows masaüstü bildirimi başarıyla iletildi! Sisteminiz hazır.'
      );
      setWindowsServiceFeedback(`✓ ${res.message} (Ekranınızın sağ alt köşesine bakın)`);
    } catch (err: any) {
      setWindowsServiceFeedback(`Hata: ${err.message}`);
    } finally {
      setIsSendingWindowsNotify(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      loadUsersData();
      loadSmtpConfig();
      checkWorkerStatus();
      loadWindowsServiceStatus();
      const interval = setInterval(() => {
        checkWorkerStatus();
        loadWindowsServiceStatus();
      }, 7000);
      return () => clearInterval(interval);
    }
  }, [isOpen]);

  if (!isOpen) return null;

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
        <div className="bg-slate-100 border-b border-slate-200 px-3 sm:px-4 flex items-center gap-1 sm:gap-2 shrink-0 overflow-x-auto no-scrollbar whitespace-nowrap">
          <button
            onClick={() => setActiveTab('questions')}
            className={`py-3 px-3 text-xs font-bold border-b-2 flex items-center gap-1.5 transition-all cursor-pointer shrink-0 ${
              activeTab === 'questions'
                ? 'border-teal-700 text-teal-900 bg-white shadow-2xs'
                : 'border-transparent text-slate-600 hover:text-slate-900'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5 text-teal-600" />
            <span>Soru Havuzu ({questions.length})</span>
          </button>

          <button
            onClick={() => {
              setActiveTab('users');
              loadUsersData();
            }}
            className={`py-3 px-3 text-xs font-bold border-b-2 flex items-center gap-1.5 transition-all cursor-pointer shrink-0 ${
              activeTab === 'users'
                ? 'border-teal-700 text-teal-900 bg-white shadow-2xs'
                : 'border-transparent text-slate-600 hover:text-slate-900'
            }`}
          >
            <Users className="w-3.5 h-3.5 text-teal-600" />
            <span>Kullanıcı Yönetimi ({usersList.length})</span>
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
          </button>

          <button
            onClick={() => setActiveTab('automations')}
            className={`py-3 px-3 text-xs font-bold border-b-2 flex items-center gap-1.5 transition-all cursor-pointer shrink-0 ${
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
            className={`py-3 px-3 text-xs font-bold border-b-2 flex items-center gap-1.5 transition-all cursor-pointer shrink-0 ${
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
              {filteredQuestions.filter(Boolean).slice(0, 30).map((q) => (
                <div
                  key={q.id || ('q-' + q.questionNumber)}
                  className="p-3 bg-white rounded-lg border border-slate-200 hover:border-teal-400 transition-all flex items-center justify-between gap-3"
                >
                  <div className="space-y-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-900">#{q.questionNumber || '?'}</span>
                      <span className="bg-teal-100 text-teal-800 text-[10px] font-bold px-2 py-0.5 rounded">
                        {q.discipline || 'Tıp'}
                      </span>
                      <span className="text-slate-600 font-medium truncate">{q.topic || 'Genel Konu'}</span>
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
            {/* Live Worker Agent Heartbeat Monitor */}
            <div className={`p-4 sm:p-5 rounded-2xl border shadow-sm transition-all ${
              workerHeartbeat?.isOnline
                ? 'bg-gradient-to-r from-emerald-900 via-teal-900 to-slate-900 text-white border-emerald-500'
                : 'bg-amber-50/90 border-amber-300 text-amber-950'
            }`}>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-white/10">
                <div className="flex items-center gap-2.5">
                  <div className={`w-3.5 h-3.5 rounded-full shrink-0 ${workerHeartbeat?.isOnline ? 'bg-emerald-400 animate-pulse' : 'bg-amber-500'}`} />
                  <div>
                    <h4 className="font-bold text-sm sm:text-base flex items-center gap-2">
                      {workerHeartbeat?.isOnline ? '🟢 Yerel Masaüstü İşleyicisi ÇEVRİMİÇİ (ONLINE)' : '🟡 Yerel Masaüstü İşleyicisi BEKLENİYOR (OFFLINE)'}
                    </h4>
                    <p className={`text-xs ${workerHeartbeat?.isOnline ? 'text-teal-200' : 'text-amber-800'}`}>
                      {workerHeartbeat?.isOnline
                        ? `Bilgisayarınız bağlı ve arkaplanda çalışıyor. Son sinyal: ${workerHeartbeat.diffSeconds} sn önce`
                        : 'Bilgisayarınızda start-worker.bat henüz başlatılmamış veya sinyal bekleniyor.'}
                    </p>
                  </div>
                </div>

                <button
                  onClick={checkWorkerStatus}
                  disabled={isCheckingWorker}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer shrink-0 ${
                    workerHeartbeat?.isOnline
                      ? 'bg-emerald-500 hover:bg-emerald-400 text-slate-950'
                      : 'bg-amber-600 hover:bg-amber-700 text-white'
                  }`}
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isCheckingWorker ? 'animate-spin' : ''}`} />
                  <span>{isCheckingWorker ? 'Kontrol Ediliyor...' : 'Bağlantıyı Test Et'}</span>
                </button>
              </div>

              {workerHeartbeat?.isOnline ? (
                <div className="mt-3 grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs text-teal-100">
                  <div className="bg-white/10 p-2.5 rounded-xl">
                    <span className="text-[10px] text-teal-300 block">Bağlı Bilgisayar:</span>
                    <strong className="font-mono text-white">{workerHeartbeat.lastHeartbeat?.hostname || 'Yerel PC'}</strong>
                  </div>
                  <div className="bg-white/10 p-2.5 rounded-xl">
                    <span className="text-[10px] text-teal-300 block">Arkaplan Süreç (PID):</span>
                    <strong className="font-mono text-white">PID {workerHeartbeat.lastHeartbeat?.pid || 'Aktif'}</strong>
                  </div>
                  <div className="bg-white/10 p-2.5 rounded-xl">
                    <span className="text-[10px] text-teal-300 block">Çalışma Durumu:</span>
                    <strong className="text-emerald-300">Google Drive & Slaytlar Taranıyor</strong>
                  </div>
                </div>
              ) : (
                <div className="mt-3 bg-white p-3 rounded-xl border border-amber-200 text-xs text-amber-900 space-y-1.5">
                  <p className="font-bold text-slate-900">📌 Arka Planda Çalıştığını Nasıl Teyit Edebilirsiniz?</p>
                  <ol className="list-decimal list-inside space-y-1 text-slate-700 text-[11px]">
                    <li>İndirdiğiniz <strong>start-worker.bat</strong> dosyasına çift tıklayın.</li>
                    <li>Açılan siyah pencerede yeşil renkle <strong>"[BAŞLADI] Otomasyon servisi aktif"</strong> ve <strong>"[Sinyal Gönderildi]"</strong> yazısını görürsünüz.</li>
                    <li>O pencere açık kaldığı sürece bilgisayarınızın işlemcisiyle dosyalar okunur ve buradaki durum <strong>ÇEVRİMİÇİ</strong>'ye döner.</li>
                  </ol>
                </div>
              )}
            </div>

            {/* Windows Desktop Shortcut & Daily 16:00 - 18:00 Automation Card */}
            <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-teal-950 text-white rounded-2xl p-5 border border-teal-600/40 shadow-xl space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-700/80">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-teal-400 border border-teal-500/30 flex items-center justify-center shrink-0">
                    <Monitor className="w-5 h-5 text-teal-300" />
                  </div>
                  <div>
                    <h4 className="font-bold text-sm sm:text-base text-white flex items-center gap-2 flex-wrap">
                      <span>Windows Masaüstü Kısayolu & Otomatik Başlangıç</span>
                      {windowsServiceStatus?.isRunning ? (
                        <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                          <Check className="w-3 h-3 text-emerald-400" />
                          Servis Aktif (PID: {windowsServiceStatus.pids?.join(', ') || 'Aktif'})
                        </span>
                      ) : (
                        <span className="bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                          <AlertTriangle className="w-3 h-3 text-amber-400" />
                          Servis Beklemede
                        </span>
                      )}
                    </h4>
                    <p className="text-xs text-slate-300 mt-0.5">
                      Bilgisayar her açıldığında ve saat 16:00 - 18:00 aralığında arka planda çalışarak tüm Drive dosyalarını eşitler.
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <button
                    type="button"
                    onClick={handleSendWindowsTestNotification}
                    disabled={isSendingWindowsNotify}
                    className="bg-slate-800 hover:bg-slate-700 text-teal-300 border border-teal-600/40 font-bold px-3 py-1.5 rounded-xl text-xs flex items-center gap-1.5 transition-all cursor-pointer disabled:opacity-50"
                    title="Windows Action Center / Bildirim Alanına test bildirimi gönderir"
                  >
                    <Bell className={`w-3.5 h-3.5 ${isSendingWindowsNotify ? 'animate-bounce' : ''}`} />
                    <span>{isSendingWindowsNotify ? 'Gönderiliyor...' : 'Bildirim Testi'}</span>
                  </button>

                  <button
                    type="button"
                    onClick={handleInstallWindowsService}
                    disabled={isInstallingWindowsService}
                    className="bg-teal-500 hover:bg-teal-400 text-slate-950 font-black px-4 py-2 rounded-xl text-xs flex items-center gap-2 shadow-sm transition-all cursor-pointer active:scale-95 disabled:opacity-50"
                  >
                    <Play className={`w-3.5 h-3.5 fill-current ${isInstallingWindowsService ? 'animate-spin' : ''}`} />
                    <span>{isInstallingWindowsService ? 'Yapılandırılıyor...' : 'Kısayol Kur & Başlat'}</span>
                  </button>

                  {windowsServiceStatus?.isRunning && (
                    <button
                      type="button"
                      onClick={handleStopWindowsService}
                      disabled={isInstallingWindowsService}
                      className="bg-rose-900/60 hover:bg-rose-800 text-rose-200 border border-rose-700/60 font-bold px-3 py-1.5 rounded-xl text-xs flex items-center gap-1 transition-all cursor-pointer"
                      title="Çalışan arka plan servisini durdurur"
                    >
                      <Square className="w-3 h-3 fill-current" />
                      <span>Durdur</span>
                    </button>
                  )}
                </div>
              </div>

              {/* Status Badges Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs">
                <div className="bg-slate-950/70 border border-slate-700/60 p-3 rounded-xl space-y-1">
                  <span className="text-[10px] text-slate-400 block font-semibold">Masaüstü Kısayolu:</span>
                  <div className="flex items-center gap-2">
                    <span className={`w-2 h-2 rounded-full ${windowsServiceStatus?.isInstalledOnDesktop ? 'bg-emerald-400' : 'bg-amber-400'}`} />
                    <strong className="text-white text-xs truncate">
                      {windowsServiceStatus?.isInstalledOnDesktop ? '✓ Masaüstünde Mevcut' : '⚠️ Kısayol Eksik'}
                    </strong>
                  </div>
                  <span className="text-[10px] text-slate-500 font-mono block truncate">
                    MedSoru Otomasyon Servisi.lnk
                  </span>
                </div>

                <div className="bg-slate-950/70 border border-slate-700/60 p-3 rounded-xl space-y-1">
                  <span className="text-[10px] text-slate-400 block font-semibold">Windows Başlangıç (Startup):</span>
                  <div className="flex items-center gap-2">
                    <span className={`w-2 h-2 rounded-full ${windowsServiceStatus?.isRegisteredInStartup ? 'bg-emerald-400' : 'bg-amber-400'}`} />
                    <strong className="text-white text-xs truncate">
                      {windowsServiceStatus?.isRegisteredInStartup ? '✓ Başlangıca Kayıtlı' : '⚠️ Başlangıçta Yok'}
                    </strong>
                  </div>
                  <span className="text-[10px] text-slate-500 font-mono block truncate">
                    shell:startup (Otomatik Açılış)
                  </span>
                </div>

                <div className="bg-slate-950/70 border border-slate-700/60 p-3 rounded-xl space-y-1">
                  <span className="text-[10px] text-slate-400 block font-semibold">Çalışma Aralığı & Bildirim:</span>
                  <div className="flex items-center gap-2">
                    <Clock className="w-3.5 h-3.5 text-teal-400 shrink-0" />
                    <strong className="text-emerald-300 text-xs">16:00 - 18:00 Arası Günlük</strong>
                  </div>
                  <span className="text-[10px] text-teal-400/90 block">
                    Windows Bildirim Alanı Aktif 🔔
                  </span>
                </div>
              </div>

              {/* Explanatory Guide Box */}
              <div className="bg-slate-950/50 border border-teal-500/20 p-3 rounded-xl text-[11px] text-slate-300 space-y-1.5 leading-relaxed">
                <div className="flex items-center gap-1.5 text-teal-300 font-semibold text-xs">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                  <span>Tek Tıkla Otomatik Çalışma Mantığı:</span>
                </div>
                <p>
                  Masaüstünüzde yer alan <strong className="text-white">"MedSoru Otomasyon Servisi"</strong> kısayoluna çift tıkladığınızda; servis kendisini otomatik olarak Windows başlangıç klasörüne kaydeder, ekranınızın sağ altına Windows bildirimi yollar ve arka planda çalışmaya başlar.
                </p>
                <p className="text-slate-400 text-[10px]">
                  Bilgisayarınız her açıldığında ve her gün saat <strong className="text-teal-300">16:00 - 18:00</strong> arasında Drive çıkmış soruları ve ders slaytları <code className="bg-slate-800 text-teal-300 px-1 py-0.5 rounded">C:\Users\indui\Desktop\meds_database</code> klasörünüze indirilir, CPU ile sayfa sayfa birebir okunarak soru havuzuna ve Firebase'e işlenir.
                </p>
              </div>

              {/* Feedback Alert */}
              {windowsServiceFeedback && (
                <div className={`p-3 rounded-xl border text-xs flex items-start gap-2 ${
                  windowsServiceFeedback.startsWith('✓')
                    ? 'bg-emerald-950/80 border-emerald-500/50 text-emerald-200'
                    : windowsServiceFeedback.startsWith('Hata')
                    ? 'bg-rose-950/80 border-rose-500/50 text-rose-200'
                    : 'bg-teal-950/80 border-teal-500/50 text-teal-200'
                }`}>
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <div>
                    <span>{windowsServiceFeedback}</span>
                  </div>
                </div>
              )}
            </div>

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

            {/* 3. Local Desktop Background Daemon Card (Zero Token Cost, Verbatim OCR) */}
            <div className="bg-slate-900 text-white rounded-xl p-4 sm:p-5 space-y-4">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Terminal className="w-5 h-5 text-emerald-400" />
                  <h4 className="font-bold text-sm text-white">Yerel Drive İndirici & CPU Metin/Soru Çıkarıcı</h4>
                  <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full">
                    Yerel CPU / Sıfır AI Hatası / Verbatim
                  </span>
                </div>
                <div className="text-right">
                  <span className="text-[10px] text-emerald-400 font-bold bg-emerald-950/80 border border-emerald-700/60 px-2 py-1 rounded">
                    🕒 Hedef Saat: 16:00 - 18:00
                  </span>
                </div>
              </div>

              <p className="text-slate-300 text-xs leading-relaxed">
                Tüm Google Drive çıkmış klasörleri doğrudan bilgisayarınızdaki <code className="bg-slate-800 text-teal-300 px-1.5 py-0.5 rounded font-mono">C:\Users\indui\Desktop\meds_database</code> klasörüne indirilir. PDF'ler yerel işlemcinizle sayfa sayfa birebir okunur (asla AI özet uydurması yapmaz) ve sorular 0 beğeni ile veritabanına ve Firebase'e aktarılır.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                  <span className="text-slate-400 font-bold block">1. Otomatik Başlatma (Windows Başlangıç):</span>
                  <p className="text-[11px] text-slate-400">
                    Bilgisayar her açıldığında arka planda sessizce başlar. Saat 16:00-18:00 arasındaysa doğrudan eşitlemeyi yapar:
                  </p>
                  <div className="font-mono text-[11px] text-teal-300 pt-1">start-meds-daemon.vbs</div>
                </div>

                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800 space-y-1">
                  <span className="text-slate-400 font-bold block">2. Manuel Çift Tıklama Dosyası:</span>
                  <p className="text-[11px] text-slate-400">
                    İstediğiniz an masaüstünden veya proje klasöründen tek tıkla başlatabilirsiniz:
                  </p>
                  <div className="font-mono text-[11px] text-emerald-400 pt-1">run-meds-sync.bat</div>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-3 pt-1 border-t border-slate-800">
                <div className="text-[11px] text-slate-400">
                  <span>Hedef klasörler: <strong>meds_sorular</strong> & <strong>ders_notlari_pdf</strong></span>
                </div>

                <button
                  onClick={handleTriggerFullLocalSync}
                  disabled={isSyncingFullLocal}
                  className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-slate-950 font-black px-4 py-2 rounded-lg flex items-center gap-1.5 shadow-sm transition-all cursor-pointer active:scale-95"
                >
                  <RefreshCw className={`w-4 h-4 ${isSyncingFullLocal ? 'animate-spin' : ''}`} />
                  <span>{isSyncingFullLocal ? 'Eşitleme Başlatılıyor...' : 'Tüm Drive Çıkmışlarını & Slaytları Şimdi Eşitle'}</span>
                </button>
              </div>

              {fullLocalSyncFeedback && (
                <div className="p-3 bg-emerald-950/80 border border-emerald-500/50 rounded-lg text-xs font-semibold text-emerald-200 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                  <span>{fullLocalSyncFeedback}</span>
                </div>
              )}
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

              <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg space-y-2">
                <div className="text-xs font-semibold text-slate-800">
                  📦 Proje Kaynak Kodları ve Veritabanı Dışa Aktarma
                </div>
                <div className="text-[11px] text-slate-600">
                  Tüm güncel ders notları, soru havuzu ve sunucu kodlarını içeren arşivi tek tıkla indirip bilgisayarınızdaki Git deposuna aktarabilirsiniz.
                </div>
                <a
                  href="/api/admin/export-zip"
                  download="medsoru-project.zip"
                  className="inline-flex bg-teal-700 hover:bg-teal-800 text-white font-bold px-4 py-2 rounded-lg text-xs items-center gap-2 shadow-xs cursor-pointer"
                >
                  <Download className="w-4 h-4 text-teal-200" />
                  <span>Projeyi ZIP Olarak İndir (Tüm Kodlar & Veriler)</span>
                </a>
              </div>
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

            {/* Cloud Firestore Sync Card */}
            <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-teal-950 text-white border border-teal-700/50 rounded-xl p-4 sm:p-5 space-y-3 shadow-md">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-teal-500/20 text-teal-400 border border-teal-500/30 flex items-center justify-center">
                    <Cloud className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="font-bold text-sm text-white flex items-center gap-2">
                      <span>Firebase Firestore Bulut Senkronizasyonu</span>
                      <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full">
                        Canlı Bulut
                      </span>
                    </h4>
                    <p className="text-xs text-slate-400">
                      Mevcut soru havuzunu ({questions.length} soru) Firebase Firestore bulutuna toplu olarak yazar.
                    </p>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={handleSyncQuestionsToFirestore}
                  disabled={isSyncingFirestore || questions.length === 0}
                  className="bg-teal-600 hover:bg-teal-500 text-white font-bold px-4 py-2 rounded-xl text-xs flex items-center gap-2 transition-all cursor-pointer disabled:opacity-50 shadow-sm shrink-0"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isSyncingFirestore ? 'animate-spin' : ''}`} />
                  <span>{isSyncingFirestore ? 'Buluta Yazılıyor...' : 'Tüm Soruları Firestore\'a Aktar'}</span>
                </button>
              </div>

              <div className="bg-slate-950/60 border border-slate-700/50 rounded-lg p-3 text-[11px] text-slate-300 space-y-1.5">
                <div className="flex items-center gap-1.5 text-teal-300 font-semibold">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Güvenli & Parçalı (Chunked) Firestore Aktarımı:</span>
                </div>
                <p className="leading-relaxed">
                  Bu işlem tüm çıkmış soruları ve komite sorularını 100'lük güvenli paketlere bölerek Firestore'a kaydeder. Beğeniler (upvotes) 0'dan başlatılır ve tekil beğeni listesi (<code className="text-teal-300">likedBy: []</code>) standartlaştırılır.
                </p>
              </div>

              {firestoreSyncFeedback && (
                <div className={`p-3 rounded-lg border text-xs flex items-start gap-2 ${
                  firestoreSyncFeedback.startsWith('✓')
                    ? 'bg-emerald-950/80 border-emerald-500/50 text-emerald-200'
                    : firestoreSyncFeedback.startsWith('Hata')
                    ? 'bg-rose-950/80 border-rose-500/50 text-rose-200'
                    : 'bg-teal-950/80 border-teal-500/50 text-teal-200'
                }`}>
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{firestoreSyncFeedback}</span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 4: USERS MANAGEMENT & AUTH-DATABASE SYNC */}
        {activeTab === 'users' && (
          <div className="p-4 sm:p-6 overflow-y-auto space-y-5">
            {/* Top Status & Sync Banner */}
            <div className="bg-gradient-to-r from-teal-900 via-slate-900 to-teal-950 text-white p-4 sm:p-5 rounded-2xl border border-teal-800 shadow-md flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
                  <span className="text-xs font-bold text-teal-300 uppercase tracking-wider">
                    Auth & Realtime Database Bağlantı Durumu: Aktif & Senkronize
                  </span>
                </div>
                <h3 className="text-base sm:text-lg font-black text-white">
                  Kayıtlı Öğrenci & Kullanıcı Yönetim Masası
                </h3>
                <p className="text-xs text-slate-300 max-w-xl">
                  Sisteme e-posta veya Google ile kayıt olan tüm tıp fakültesi öğrencileri burada listelenir. Auth ve veritabanı arasındaki çift yönlü eşitleme sayesinde yeni kayıtlar anında tabloya yansır.
                </p>
                {userSyncMessage && (
                  <div className="mt-2 text-xs font-semibold text-teal-200 bg-teal-800/60 border border-teal-600/50 p-2 rounded-lg flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span>{userSyncMessage}</span>
                  </div>
                )}
              </div>

              <div className="flex flex-wrap items-center gap-2 shrink-0">
                <button
                  onClick={handleSyncAuthDbBridge}
                  disabled={isSyncingAuthDb}
                  className="bg-teal-700/80 hover:bg-teal-700 text-teal-100 border border-teal-500/60 font-bold px-3 py-2 rounded-xl text-xs flex items-center gap-1.5 shadow-2xs transition-all cursor-pointer active:scale-95 disabled:opacity-50"
                  title="Firebase Auth kullanıcıları ile veritabanını doğrula ve yenile"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isSyncingAuthDb ? 'animate-spin text-emerald-400' : 'text-teal-300'}`} />
                  <span>{isSyncingAuthDb ? 'Eşitleniyor...' : 'Veritabanını Eşitle'}</span>
                </button>

                <button
                  onClick={() => setShowSmtpSettings(!showSmtpSettings)}
                  className={`font-black px-3.5 py-2 rounded-xl text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer active:scale-95 ${
                    smtpConfig?.hasPass
                      ? 'bg-teal-800/90 hover:bg-teal-700 text-teal-100 border border-teal-500/60'
                      : 'bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold border border-amber-300'
                  }`}
                  title="Gmail SMTP e-posta sunucusu ve 16 haneli Google Uygulama Şifresi ayarları"
                >
                  <Mail className="w-4 h-4" />
                  <span>{showSmtpSettings ? 'SMTP Panelini Gizle' : 'E-posta & SMTP Ayarları'}</span>
                  {!smtpConfig?.hasPass && (
                    <span className="w-2 h-2 rounded-full bg-rose-600 animate-ping" />
                  )}
                </button>

                <button
                  onClick={() => setIsCreatingUser(!isCreatingUser)}
                  className="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black px-3.5 py-2 rounded-xl text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer active:scale-95"
                >
                  <UserPlus className="w-4 h-4" />
                  <span>{isCreatingUser ? 'Formu Kapat' : 'Yeni Kullanıcı Ekle'}</span>
                </button>
              </div>
            </div>

            {/* Warning if SMTP pass is missing */}
            {!smtpConfig?.hasPass && !showSmtpSettings && (
              <div className="bg-amber-50 border border-amber-300 rounded-xl p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-amber-900 shadow-2xs">
                <div className="flex items-center gap-2.5">
                  <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0" />
                  <div>
                    <strong className="font-bold block text-slate-900">
                      Önemli: Hoş Geldin E-postaları İçin Google Uygulama Şifresi Tanımlanmamış
                    </strong>
                    <span className="text-[11px] text-slate-600">
                      Yeni kaydolan öğrencilere otomatik hoş geldiniz bildirimi gidebilmesi için 16 haneli Google App Password tanımlanmalıdır.
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => setShowSmtpSettings(true)}
                  className="bg-amber-600 hover:bg-amber-700 text-white font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 cursor-pointer shrink-0 self-start sm:self-auto"
                >
                  <Mail className="w-3.5 h-3.5" />
                  <span>Şimdi Tanımla & Test Et</span>
                </button>
              </div>
            )}

            {/* SMTP E-posta Sunucu Yapılandırması Kartı */}
            {showSmtpSettings && (
              <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-teal-950 text-white rounded-2xl p-5 border border-teal-700/50 shadow-xl space-y-4 animate-fade-in">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-700">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-lg bg-teal-500/20 text-teal-400 border border-teal-500/30 flex items-center justify-center">
                      <Mail className="w-4 h-4" />
                    </div>
                    <div>
                      <h4 className="font-bold text-sm text-white flex items-center gap-2">
                        <span>E-posta & SMTP Sunucu Yapılandırması (Gmail Canlı İletim)</span>
                        {smtpConfig?.hasPass ? (
                          <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                            <Check className="w-3 h-3 text-emerald-400" />
                            Hazır & Yapılandırıldı
                          </span>
                        ) : (
                          <span className="bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                            <AlertTriangle className="w-3 h-3 text-amber-400" />
                            Şifre Eksik (Mail Gönderilemez)
                          </span>
                        )}
                      </h4>
                      <p className="text-xs text-slate-400">
                        Yeni kayıt olan veya onaylanan öğrencilere gönderilecek hoş geldiniz mailleri için Gmail SMTP servisi kullanılır.
                      </p>
                    </div>
                  </div>

                  <button
                    onClick={() => setShowSmtpSettings(false)}
                    className="self-end sm:self-auto text-slate-400 hover:text-white text-xs px-2.5 py-1 rounded-lg hover:bg-slate-800 cursor-pointer"
                  >
                    Gizle
                  </button>
                </div>

                {/* Form Fields */}
                <form onSubmit={handleSaveSmtp} className="space-y-4">
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                    <div>
                      <label className="block text-[11px] font-bold text-teal-300 mb-1">
                        Gönderen Gmail Adresi *
                      </label>
                      <input
                        type="email"
                        required
                        value={smtpUser}
                        onChange={(e) => setSmtpUser(e.target.value)}
                        placeholder="nofrostlife@gmail.com"
                        className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:border-teal-400 focus:ring-1 focus:ring-teal-400 font-mono"
                      />
                    </div>

                    <div>
                      <label className="block text-[11px] font-bold text-teal-300 mb-1 flex items-center justify-between">
                        <span>16 Haneli Google Uygulama Şifresi *</span>
                        {smtpConfig?.hasPass && (
                          <span className="text-[10px] text-emerald-400 font-normal">Kayıtlı: {smtpConfig.passMasked}</span>
                        )}
                      </label>
                      <div className="relative">
                        <input
                          type="password"
                          value={smtpPass}
                          onChange={(e) => setSmtpPass(e.target.value)}
                          placeholder={smtpConfig?.hasPass ? 'Yeni şifre girmek için yazınız...' : 'örn: abcd efgh ijkl mnop'}
                          className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:border-teal-400 focus:ring-1 focus:ring-teal-400 font-mono"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-[11px] font-bold text-teal-300 mb-1">
                        Görünen Gönderici Başlığı
                      </label>
                      <input
                        type="text"
                        value={smtpFrom}
                        onChange={(e) => setSmtpFrom(e.target.value)}
                        placeholder="MedSoru Tıp Fakültesi <nofrostlife@gmail.com>"
                        className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:border-teal-400 focus:ring-1 focus:ring-teal-400"
                      />
                    </div>
                  </div>

                  {/* Instructions Box */}
                  <div className="bg-slate-950/80 border border-teal-900/60 rounded-xl p-3.5 text-xs space-y-2 text-slate-300">
                    <div className="flex items-center gap-2 font-bold text-teal-300">
                      <Key className="w-4 h-4 text-teal-400" />
                      <span>Google 16 Haneli Uygulama Şifresi Nasıl Alınır? (Gmail 2022+ Kuralı)</span>
                    </div>
                    <ol className="list-decimal list-inside space-y-1 text-[11px] text-slate-400 leading-relaxed">
                      <li>
                        Gmail normal e-posta şifrenizle programlardan giriş yapılmasına izin vermez. 
                        Önce Google hesabınızda <strong className="text-white">2 Adımlı Doğrulama</strong>'nın açık olduğundan emin olun.
                      </li>
                      <li>
                        Tarayıcınızda{' '}
                        <a
                          href="https://myaccount.google.com/apppasswords"
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-teal-400 hover:text-teal-300 underline font-bold inline-flex items-center gap-0.5"
                        >
                          myaccount.google.com/apppasswords
                          <ExternalLink className="w-3 h-3 inline" />
                        </a>{' '}
                        sayfasına gidin.
                      </li>
                      <li>
                        Uygulama adı olarak <strong className="text-teal-300">MedSoru</strong> yazın ve <strong className="text-white">Oluştur</strong> butonuna tıklayın.
                      </li>
                      <li>
                        Google'ın size ekranda gösterdiği 16 haneli sarı kod bloğunu (örnek: <span className="font-mono text-amber-300">abcd efgh ijkl mnop</span>) kopyalayıp yukarıdaki alana yapıştırın ve <strong>Ayarları Kaydet</strong>'e basınız.
                      </li>
                    </ol>
                  </div>

                  {/* Actions & Live Test */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-1">
                    <div className="flex items-center gap-2 flex-1 max-w-md">
                      <input
                        type="email"
                        value={testEmailTarget}
                        onChange={(e) => setTestEmailTarget(e.target.value)}
                        placeholder="Test maili alıcısı (örn: nofrostlife@gmail.com)"
                        className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white placeholder-slate-500 font-mono"
                      />
                      <button
                        type="button"
                        onClick={handleTestSmtp}
                        disabled={isTestingSmtp}
                        className="bg-teal-600 hover:bg-teal-500 text-white font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 transition-all cursor-pointer disabled:opacity-50 shrink-0"
                      >
                        <Send className={`w-3.5 h-3.5 ${isTestingSmtp ? 'animate-pulse' : ''}`} />
                        <span>{isTestingSmtp ? 'Gönderiliyor...' : 'Canlı Test Gönder'}</span>
                      </button>
                    </div>

                    <div className="flex items-center gap-2 self-end sm:self-auto">
                      <button
                        type="submit"
                        disabled={isSavingSmtp}
                        className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-4 py-1.5 rounded-lg text-xs flex items-center gap-1.5 transition-all cursor-pointer disabled:opacity-50"
                      >
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>{isSavingSmtp ? 'Kaydediliyor...' : 'Ayarları Kaydet'}</span>
                      </button>
                    </div>
                  </div>

                  {/* Feedback Message */}
                  {smtpTestResult && (
                    <div className={`p-3 rounded-xl border text-xs flex items-start gap-2 ${
                      smtpTestResult.success
                        ? 'bg-emerald-950/80 border-emerald-500/50 text-emerald-200'
                        : 'bg-rose-950/80 border-rose-500/50 text-rose-200'
                    }`}>
                      {smtpTestResult.success ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      ) : (
                        <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                      )}
                      <div>
                        <strong className="block">{smtpTestResult.message}</strong>
                        {smtpTestResult.hint && (
                          <p className="text-[11px] text-slate-300 mt-1">
                            📌 <strong>İpucu:</strong> {smtpTestResult.hint}
                          </p>
                        )}
                      </div>
                    </div>
                  )}
                </form>
              </div>
            )}

            {/* Quick Add User Form (Collapsible) */}
            {isCreatingUser && (
              <form onSubmit={handleManualCreateUser} className="bg-slate-50 border border-teal-300/80 rounded-2xl p-4 sm:p-5 space-y-4 shadow-sm animate-fade-in">
                <div className="flex items-center justify-between pb-2 border-b border-slate-200">
                  <h4 className="font-bold text-sm text-slate-800 flex items-center gap-2">
                    <UserPlus className="w-4 h-4 text-teal-700" />
                    Yeni Öğrenci / Yönetici Kaydı Aç
                  </h4>
                  <span className="text-[11px] text-teal-700 font-medium">Kayıt sonrası öğrenciye otomatik hoş geldiniz e-postası iletilir</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
                  <div>
                    <label className="block text-[11px] font-bold text-slate-700 mb-1">E-posta Adresi *</label>
                    <input
                      type="email"
                      required
                      value={newEmail}
                      onChange={(e) => setNewEmail(e.target.value)}
                      placeholder="ogrenci@ogr.karabuk.edu.tr"
                      className="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-900 focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
                    />
                  </div>

                  <div>
                    <label className="block text-[11px] font-bold text-slate-700 mb-1">Ad Soyad (Görünen İsim)</label>
                    <input
                      type="text"
                      value={newName}
                      onChange={(e) => setNewName(e.target.value)}
                      placeholder="Örn: Eren Yılmaz"
                      className="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-900 focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
                    />
                  </div>

                  <div>
                    <label className="block text-[11px] font-bold text-slate-700 mb-1">Öğrenci Numarası</label>
                    <input
                      type="text"
                      value={newStudentNumber}
                      onChange={(e) => setNewStudentNumber(e.target.value.replace(/\D/g, ''))}
                      placeholder="Örn: 202311045"
                      className="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-900 focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
                    />
                  </div>

                  <div>
                    <label className="block text-[11px] font-bold text-slate-700 mb-1">Yetki Rolü</label>
                    <select
                      value={newRole}
                      onChange={(e) => setNewRole(e.target.value as any)}
                      className="w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-900 font-semibold focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
                    >
                      <option value="student">Öğrenci (Soru Ekleme & Test)</option>
                      <option value="admin">Yönetici (Tam Yetki)</option>
                    </select>
                  </div>
                </div>

                <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-200">
                  <button
                    type="button"
                    onClick={() => setIsCreatingUser(false)}
                    className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-200 cursor-pointer"
                  >
                    Vazgeç
                  </button>
                  <button
                    type="submit"
                    disabled={isProcessing}
                    className="bg-teal-700 hover:bg-teal-800 text-white font-bold px-4 py-1.5 rounded-lg text-xs flex items-center gap-1.5 shadow-2xs transition-all cursor-pointer disabled:opacity-50"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5 text-teal-200" />
                    <span>{isProcessing ? 'Ekleniyor...' : 'Kullanıcıyı Kaydet & Mail Gönder'}</span>
                  </button>
                </div>
              </form>
            )}

            {/* Statistics Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                <span className="text-[11px] font-semibold text-slate-500 block">Toplam Kayıtlı</span>
                <span className="text-xl font-black text-slate-900">{usersList.length} Kullanıcı</span>
              </div>

              <div className="bg-teal-50/70 border border-teal-200 rounded-xl p-3.5">
                <span className="text-[11px] font-semibold text-teal-700 block">Öğrenci Hesapları</span>
                <span className="text-xl font-black text-teal-950">
                  {usersList.filter((u) => u && u.role !== 'admin').length} Öğrenci
                </span>
              </div>

              <div className="bg-amber-50/70 border border-amber-200 rounded-xl p-3.5">
                <span className="text-[11px] font-semibold text-amber-700 block">Yönetici Hesapları</span>
                <span className="text-xl font-black text-amber-950">
                  {usersList.filter((u) => u && u.role === 'admin').length} Yönetici
                </span>
              </div>

              <div className="bg-emerald-50/70 border border-emerald-200 rounded-xl p-3.5">
                <span className="text-[11px] font-semibold text-emerald-700 block">Hoş Geldin Maili Alan</span>
                <span className="text-xl font-black text-emerald-950">
                  {usersList.filter((u) => u && u.welcomeEmailSent).length} İletildi
                </span>
              </div>
            </div>

            {/* Search and Filter */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-3 rounded-xl border border-slate-200">
              <div className="relative flex-1 max-w-sm">
                <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
                <input
                  type="text"
                  value={userSearchQuery}
                  onChange={(e) => setUserSearchQuery(e.target.value)}
                  placeholder="İsim, e-posta veya öğrenci no ara..."
                  className="w-full text-xs pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 focus:bg-white focus:outline-none focus:ring-1 focus:ring-teal-500"
                />
              </div>

              <div className="flex items-center gap-2 text-xs text-slate-500">
                <span>Tabloda gösterilen: <strong>{
                  usersList.filter((u) =>
                    Boolean(u) && (
                      !userSearchQuery ||
                      (u.displayName && u.displayName.toLowerCase().includes(userSearchQuery.toLowerCase())) ||
                      (u.email && u.email.toLowerCase().includes(userSearchQuery.toLowerCase())) ||
                      (u.studentNumber && String(u.studentNumber).includes(userSearchQuery))
                    )
                  ).length
                }</strong> / {usersList.length}</span>
              </div>
            </div>

            {/* Comprehensive Users Table */}
            <div className="bg-white rounded-2xl border border-slate-200 shadow-2xs overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse text-xs">
                  <thead>
                    <tr className="bg-slate-50/80 border-b border-slate-200 text-slate-700 font-bold uppercase text-[10px] tracking-wider">
                      <th className="py-3 px-3.5">Öğrenci / Kullanıcı</th>
                      <th className="py-3 px-3.5">E-posta Adresi</th>
                      <th className="py-3 px-3.5">Öğrenci No</th>
                      <th className="py-3 px-3.5">Yetki Rolü</th>
                      <th className="py-3 px-3.5">Kayıt Tarihi</th>
                      <th className="py-3 px-3.5">Hoş Geldin E-postası</th>
                      <th className="py-3 px-3.5 text-right">İşlemler</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {isLoadingUsers ? (
                      <tr>
                        <td colSpan={7} className="py-10 text-center text-slate-400">
                          <div className="flex items-center justify-center gap-2">
                            <RefreshCw className="w-4 h-4 animate-spin text-teal-600" />
                            <span>Kullanıcı veritabanı yükleniyor...</span>
                          </div>
                        </td>
                      </tr>
                    ) : usersList.length === 0 ? (
                      <tr>
                        <td colSpan={7} className="py-10 text-center text-slate-400">
                          Henüz kayıtlı kullanıcı bulunmuyor.
                        </td>
                      </tr>
                    ) : (
                      usersList
                        .filter((u) =>
                          Boolean(u) && (
                            !userSearchQuery ||
                            (u.displayName && u.displayName.toLowerCase().includes(userSearchQuery.toLowerCase())) ||
                            (u.email && u.email.toLowerCase().includes(userSearchQuery.toLowerCase())) ||
                            (u.studentNumber && String(u.studentNumber).includes(userSearchQuery))
                          )
                        )
                        .map((u) => {
                          const isAdminUser = u.role === 'admin' || u.email?.toLowerCase() === 'nofrostlife@gmail.com';
                          const isWelcomeSending = sendingWelcomeForEmail === u.email;
                          const formattedDate = u.createdAt
                            ? new Date(u.createdAt).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', year: 'numeric' })
                            : 'Kayıtlı';

                          return (
                            <tr key={u.uid || u.email} className="hover:bg-slate-50/70 transition-colors">
                              {/* Name & Avatar */}
                              <td className="py-3 px-3.5">
                                <div className="flex items-center gap-2.5">
                                  <div className={`w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs shrink-0 ${
                                    isAdminUser
                                      ? 'bg-amber-100 text-amber-900 border border-amber-300'
                                      : 'bg-teal-100 text-teal-900 border border-teal-300'
                                  }`}>
                                    {(u.displayName || u.email || 'Ö')[0].toUpperCase()}
                                  </div>
                                  <div>
                                    <span className="font-bold text-slate-900 block leading-tight">
                                      {u.displayName || 'İsimsiz Öğrenci'}
                                    </span>
                                    <span className="text-[10px] text-slate-400 font-mono block">
                                      ID: {u.uid?.slice(0, 14)}...
                                    </span>
                                  </div>
                                </div>
                              </td>

                              {/* Email */}
                              <td className="py-3 px-3.5">
                                <span className="font-medium text-slate-700 font-mono text-[11px]">
                                  {u.email}
                                </span>
                              </td>

                              {/* Student Number */}
                              <td className="py-3 px-3.5">
                                {u.studentNumber ? (
                                  <span className="bg-slate-100 text-slate-800 font-mono font-semibold px-2 py-0.5 rounded text-[11px] border border-slate-200">
                                    {u.studentNumber}
                                  </span>
                                ) : (
                                  <span className="text-slate-400 text-[11px] italic">Girilmedi</span>
                                )}
                              </td>

                              {/* Role */}
                              <td className="py-3 px-3.5">
                                {isAdminUser ? (
                                  <span className="inline-flex items-center gap-1 bg-amber-100 text-amber-900 border border-amber-300 text-[10px] font-bold px-2 py-0.5 rounded-full">
                                    <ShieldCheck className="w-3 h-3 text-amber-700" />
                                    Yönetici
                                  </span>
                                ) : (
                                  <span className="inline-flex items-center gap-1 bg-teal-50 text-teal-800 border border-teal-200 text-[10px] font-semibold px-2 py-0.5 rounded-full">
                                    <User className="w-3 h-3 text-teal-600" />
                                    Öğrenci
                                  </span>
                                )}
                              </td>

                              {/* Registration Date */}
                              <td className="py-3 px-3.5 text-slate-500 text-[11px]">
                                {formattedDate}
                              </td>

                              {/* Welcome Email Status */}
                              <td className="py-3 px-3.5">
                                {u.welcomeEmailSent ? (
                                  <span className="inline-flex items-center gap-1 text-emerald-700 font-bold bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-md text-[10px]">
                                    <Check className="w-3 h-3 text-emerald-600" />
                                    ✓ İletildi
                                  </span>
                                ) : (
                                  <button
                                    onClick={() => handleSendWelcomeEmail(u)}
                                    disabled={isWelcomeSending}
                                    className="inline-flex items-center gap-1 text-slate-700 hover:text-teal-900 bg-slate-100 hover:bg-teal-50 border border-slate-300 px-2 py-0.5 rounded-md text-[10px] font-semibold transition-colors cursor-pointer"
                                    title="Öğrenciye hoş geldiniz bilgilendirme maili gönder"
                                  >
                                    <Mail className="w-3 h-3 text-teal-600" />
                                    <span>{isWelcomeSending ? 'Gönderiliyor...' : 'Mail Gönder'}</span>
                                  </button>
                                )}
                              </td>

                              {/* Actions */}
                              <td className="py-3 px-3.5 text-right">
                                <div className="flex items-center justify-end gap-1.5">
                                  <button
                                    onClick={() => handleSendWelcomeEmail(u)}
                                    disabled={isWelcomeSending}
                                    title="Hoş Geldin E-postası Gönder"
                                    className="p-1.5 rounded-lg text-slate-500 hover:text-teal-700 hover:bg-teal-50 cursor-pointer transition-colors"
                                  >
                                    <Mail className="w-3.5 h-3.5" />
                                  </button>

                                  {!isAdminUser && (
                                    <button
                                      onClick={() => handleManualDeleteUser(u)}
                                      title="Kullanıcıyı Sil"
                                      className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 cursor-pointer transition-colors"
                                    >
                                      <Trash2 className="w-3.5 h-3.5" />
                                    </button>
                                  )}
                                </div>
                              </td>
                            </tr>
                          );
                        })
                    )}
                  </tbody>
                </table>
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
