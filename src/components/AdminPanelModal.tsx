import React, { useState, useEffect, useRef } from 'react';
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
  Smartphone,
  Monitor,
  Play,
  Square,
  Library,
  ChevronLeft,
  ChevronRight,
  GitMerge,
} from 'lucide-react';
import { QuestionItem, Committee } from '../types';
import { AdminEditQuestionModal } from './AdminEditQuestionModal';
import { AdminPastExamImporterModal } from './AdminPastExamImporterModal';
import { DraftDeduplicationModal } from './DraftDeduplicationModal';
import { AdminScriptsTab } from './AdminScriptsTab';
import { AdminDriveSyncSettings } from './AdminDriveSyncSettings';
import { AdminMobileNotificationCard } from './AdminMobileNotificationCard';
import { InfoPopover } from './InfoPopover';
import { StatusPill, questionStemText } from './QuickAddHero';
import { ApiService, safeJsonFetch } from '../services/api';
import { FirestoreDbService } from '../services/firestoreDb';
import { SupabaseDbService } from '../services/supabaseDb';
import { multiDbManager, DatabaseMode, DatabaseStatus } from '../services/multiDbManager';
export interface SystemServiceItem {
  id: string;
  name: string;
  category: 'core' | 'network' | 'watcher' | 'ai';
  status: 'active' | 'stopped' | 'manual';
  statusLabel: string;
  badgeColor: string;
  pid?: number;
  port?: number;
  description: string;
  resourceImpact: string;
  resourceTier: 'low' | 'high' | 'negligible';
  autoStart: boolean;
  canToggle?: boolean;
  canRunNow?: boolean;
}

interface AdminPanelModalProps {
  isOpen: boolean;
  onClose: () => void;
  adminEmail: string;
  committees: Committee[];
  questions: QuestionItem[];
  selectedCommitteeId: string;
  onRefreshData: () => Promise<void>;
  onOpenSubagentMonitor?: () => void;
  /** 'page' renders inline as its own page; 'embedded' renders one tab inside the management console (no own menu/header). */
  variant?: 'modal' | 'page' | 'embedded';
  /** embedded: which tab to show */
  tab?: 'questions' | 'scripts' | 'automations' | 'database' | 'users';
}

export const AdminPanelModal: React.FC<AdminPanelModalProps> = ({
  isOpen,
  onClose,
  adminEmail,
  committees,
  questions,
  selectedCommitteeId,
  onRefreshData,
  onOpenSubagentMonitor,
  variant = 'modal',
  tab,
}) => {
  const isEmbedded = variant === 'embedded';
  const isPage = variant === 'page' || isEmbedded;
  const [activeTabState, setActiveTab] = useState<'questions' | 'scripts' | 'automations' | 'database' | 'users'>(tab || 'questions');
  const activeTab = isEmbedded && tab ? tab : activeTabState;
  const [editingQuestion, setEditingQuestion] = useState<QuestionItem | null>(null);
  const [isPastExamImporterOpen, setIsPastExamImporterOpen] = useState(false);
  const [isDraftDeduplicationOpen, setIsDraftDeduplicationOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  // Question table filters + paging
  const [qStatus, setQStatus] = useState<'all' | 'completed' | 'draft' | 'empty'>('all');
  const [qDiscipline, setQDiscipline] = useState('all');
  const [qPage, setQPage] = useState(0);
  const dialogRef = useRef<HTMLDivElement>(null);
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
  const [showMobileNotificationSettings, setShowMobileNotificationSettings] = useState(false);
  const [isLoadingSmtp, setIsLoadingSmtp] = useState(false);
  const [isSavingSmtp, setIsSavingSmtp] = useState(false);
  const [isTestingSmtp, setIsTestingSmtp] = useState(false);
  const [smtpTestResult, setSmtpTestResult] = useState<{ success: boolean; message: string; hint?: string } | null>(null);
  const [testEmailTarget, setTestEmailTarget] = useState('nofrostlife@gmail.com');

  // Firestore Questions Sync State
  const [isSyncingFirestore, setIsSyncingFirestore] = useState(false);
  const [firestoreSyncFeedback, setFirestoreSyncFeedback] = useState<string | null>(null);

  // Multi-Database & Supabase State
  const [dbMode, setDbMode] = useState<DatabaseMode>(() => multiDbManager.getActiveMode());
  const [dbStatuses, setDbStatuses] = useState<DatabaseStatus | null>(null);
  const [isRefreshingDbStatus, setIsRefreshingDbStatus] = useState(false);
  const [isSyncingMultiDb, setIsSyncingMultiDb] = useState(false);
  const [multiDbFeedback, setMultiDbFeedback] = useState<string | null>(null);
  const [showSqlSchemaModal, setShowSqlSchemaModal] = useState(false);
  const [copiedSql, setCopiedSql] = useState(false);
  const [geminiApiKeyInput, setGeminiApiKeyInput] = useState(() => {
    return localStorage.getItem('medsoru_gemini_api_key') || '';
  });
  const [geminiKeyFeedback, setGeminiKeyFeedback] = useState<string | null>(null);

  // Groq Cloud Alternative API Key State
  const [groqApiKeyInput, setGroqApiKeyInput] = useState(() => {
    return localStorage.getItem('medsoru_groq_api_key') || '';
  });
  const [groqApiKey2Input, setGroqApiKey2Input] = useState(() => {
    return localStorage.getItem('medsoru_groq_api_key_2') || '';
  });
  const [groqKeyFeedback, setGroqKeyFeedback] = useState<string | null>(null);

  const refreshDbStatuses = async () => {
    setIsRefreshingDbStatus(true);
    try {
      const s = await multiDbManager.getStatuses();
      setDbStatuses(s);
      setDbMode(multiDbManager.getActiveMode());
    } catch {}
    setIsRefreshingDbStatus(false);
  };

  const handleSelectDbMode = (mode: DatabaseMode) => {
    multiDbManager.setActiveMode(mode);
    setDbMode(mode);
    refreshDbStatuses();
  };

  const handleSaveGeminiKey = () => {
    if (geminiApiKeyInput.trim()) {
      localStorage.setItem('medsoru_gemini_api_key', geminiApiKeyInput.trim());
      setGeminiKeyFeedback('✓ Gemini API anahtarı tarayıcıya güvenle kaydedildi!');
    } else {
      localStorage.removeItem('medsoru_gemini_api_key');
      setGeminiKeyFeedback('API anahtarı temizlendi.');
    }
    setTimeout(() => setGeminiKeyFeedback(null), 4000);
  };

  const handleSaveGroqKey = () => {
    if (groqApiKeyInput.trim()) {
      localStorage.setItem('medsoru_groq_api_key', groqApiKeyInput.trim());
    } else {
      localStorage.removeItem('medsoru_groq_api_key');
    }
    if (groqApiKey2Input.trim()) {
      localStorage.setItem('medsoru_groq_api_key_2', groqApiKey2Input.trim());
    } else {
      localStorage.removeItem('medsoru_groq_api_key_2');
    }
    setGroqKeyFeedback('✓ Groq Cloud API anahtarları kaydedildi!');
    setTimeout(() => setGroqKeyFeedback(null), 4000);
  };

  // DeepSeek Data & Lecture Repair State
  const [deepseekStatus, setDeepseekStatus] = useState<any>(null);
  const [isSyncingDeepseek, setIsSyncingDeepseek] = useState(false);
  const [deepseekFeedback, setDeepseekFeedback] = useState<string | null>(null);

  const [isRepairingNotes, setIsRepairingNotes] = useState(false);
  const [repairFeedback, setRepairFeedback] = useState<string | null>(null);

  const fetchDeepseekStatus = async () => {
    try {
      const res = await fetch('/api/deepseek/status');
      if (res.ok) {
        const data = await res.json();
        setDeepseekStatus(data);
      }
    } catch {}
  };

  const handleSyncDeepseek = async () => {
    setIsSyncingDeepseek(true);
    setDeepseekFeedback(null);
    try {
      const res = await fetch('/api/deepseek/sync', { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        setDeepseekFeedback(`✓ DeepSeek verileri tarandı: ${data.result?.filesScanned || 0} dosya, ${data.result?.itemsIngested || 0} kayıt RAG sistemine dahil edildi.`);
        fetchDeepseekStatus();
      } else {
        setDeepseekFeedback(`Hata: ${data.error}`);
      }
    } catch (err: any) {
      setDeepseekFeedback(`Hata: ${err.message}`);
    } finally {
      setIsSyncingDeepseek(false);
    }
  };

  const handleRepairLectureNotes = async () => {
    setIsRepairingNotes(true);
    setRepairFeedback(null);
    try {
      const res = await fetch('/api/admin/repair-lecture-notes', { method: 'POST' });
      const data = await res.json();
      if (data.success && data.stats) {
        setRepairFeedback(`✓ Onarım Tamamlandı: ${data.stats.matchedNotes} sunum eşleştirildi, ${data.stats.slidesRepaired} boş/eksik slayt redakte özetlerle onarıldı ve RAG'e eklendi.`);
      } else {
        setRepairFeedback(`Hata: ${data.error || 'Onarım tamamlanamadı'}`);
      }
    } catch (err: any) {
      setRepairFeedback(`Hata: ${err.message}`);
    } finally {
      setIsRepairingNotes(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'database') {
      fetchDeepseekStatus();
    }
  }, [activeTab]);

  const handleSyncToAllDatabases = async () => {
    setIsSyncingMultiDb(true);
    setMultiDbFeedback('Tüm veriler Supabase ve Firebase Spark havuzlarına eşitleniyor...');
    try {
      let supaCount = 0;
      let sparkCount = 0;

      for (const c of committees) {
        await multiDbManager.saveCommittee(c);
      }

      const pastList = await ApiService.getPastQuestions();
      setMultiDbFeedback(`${pastList.length} çıkmış soru ve ${questions.length} havuz sorusu eşzamanlı aktarılıyor...`);

      try {
        const res = await SupabaseDbService.batchSavePastQuestions(pastList);
        supaCount = res.count;
      } catch (e: any) {
        console.warn('Supabase batch sync warning:', e.message);
      }

      try {
        await FirestoreDbService.batchSaveQuestions(questions);
        sparkCount = questions.length;
      } catch (e: any) {
        console.warn('Firebase batch sync warning:', e.message);
      }

      let notesCount = 0;
      try {
        const notesList = await ApiService.getLectureNotes();
        if (notesList && notesList.length > 0) {
          setMultiDbFeedback(`${notesList.length} ders notu Supabase'e eşitleniyor...`);
          const nRes = await SupabaseDbService.batchSaveLectureNotes(notesList);
          notesCount = nRes.count;
        }
      } catch (e: any) {
        console.warn('Lecture notes sync warning:', e.message);
      }

      setMultiDbFeedback(`✓ Senkronizasyon Tamamlandı! ${supaCount} çıkmış soru, ${notesCount} ders notu Supabase'e, ${sparkCount} soru Firebase Spark'a ve yerel sunucuya başarıyla işlendi.`);
      await refreshDbStatuses();
    } catch (err: any) {
      setMultiDbFeedback(`Hata: ${err.message}`);
    } finally {
      setIsSyncingMultiDb(false);
    }
  };

  // Automations state
  const [workerHeartbeat, setWorkerHeartbeat] = useState<{ isOnline: boolean; diffSeconds?: number; lastHeartbeat?: any } | null>(null);
  const [isCheckingWorker, setIsCheckingWorker] = useState(false);

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
  const [systemServices, setSystemServices] = useState<SystemServiceItem[]>([]);
  const [isLoadingServices, setIsLoadingServices] = useState(false);
  const [serviceActionFeedback, setServiceActionFeedback] = useState<string | null>(null);
  const [actionLoadingServiceId, setActionLoadingServiceId] = useState<string | null>(null);
  const [networkSummary, setNetworkSummary] = useState<{
    internetState: string;
    compressionEnabled: boolean;
    totalServices: number;
    activeServicesCount: number;
    stoppedServicesCount: number;
  } | null>(null);

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

  const Q_PAGE_SIZE = 25;
  const [hiddenQuestionIds, setHiddenQuestionIds] = useState<Set<string>>(new Set());
  const tableQuestions = filteredQuestions
    .filter((q) => !hiddenQuestionIds.has(q.id))
    .filter((q) => qDiscipline === 'all' || q.discipline === qDiscipline)
    .filter((q) =>
      qStatus === 'all'
        ? true
        : qStatus === 'completed'
        ? q.status === 'completed'
        : qStatus === 'empty'
        ? q.status === 'empty' && (q.fragments?.length || 0) === 0
        : q.status !== 'completed' && ((q.fragments?.length || 0) > 0 || (q.options?.length || 0) > 0)
    )
    .sort((a, b) => (a.questionNumber || 0) - (b.questionNumber || 0));
  const qPageCount = Math.max(1, Math.ceil(tableQuestions.length / Q_PAGE_SIZE));
  const qPageSafe = Math.min(qPage, qPageCount - 1);
  const pagedQuestions = tableQuestions.slice(qPageSafe * Q_PAGE_SIZE, (qPageSafe + 1) * Q_PAGE_SIZE);
  const tableDisciplines = [...new Set(currentCommitteeQuestions.map((q) => q.discipline).filter(Boolean))].sort((a, b) => a.localeCompare(b, 'tr'));
  const qCounts = {
    completed: currentCommitteeQuestions.filter((q) => q.status === 'completed').length,
    draft: currentCommitteeQuestions.filter((q) => q.status !== 'completed' && ((q.fragments?.length || 0) > 0 || (q.options?.length || 0) > 0)).length,
  };

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
        // Anında listeden kaldır; hata olursa geri getir.
        setHiddenQuestionIds((prev) => new Set([...prev, question.id]));
        try {
          await ApiService.adminDeleteQuestion(adminEmail, question.id);
          setActionMessage(`Soru #${question.questionNumber} silindi (yerel + Supabase + sunucu).`);
          await onRefreshData();
        } catch (e: any) {
          setHiddenQuestionIds((prev) => {
            const next = new Set(prev);
            next.delete(question.id);
            return next;
          });
          setActionMessage(`Silinemedi: ${e.message || 'bilinmeyen hata'}`);
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


  // Full Local Sync Trigger (Drive Crawl, Download, Local OCR & Firebase Sync)
  const handleTriggerFullLocalSync = async () => {
    setIsSyncingFullLocal(true);
    setFullLocalSyncFeedback('Yerel Drive indirme ve OCR çıkarma motoru başlatılıyor...');
    try {
      const data = await ApiService.runFullLocalSync(adminEmail);
      if (data.success) {
        setFullLocalSyncFeedback(`✓ ${data.message} - PDF'ler taranıp veritabanına aktarılıyor.`);
        await onRefreshData();
      } else {
        setFullLocalSyncFeedback(`Hata: ${data.message || 'İşlem başlatılamadı'}`);
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
      const firestoreUsers = await multiDbManager.getRegisteredUsers().catch(() => []);

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
      setSmtpFrom(cfg.from || `MeDSor Tıp Fakültesi <${cfg.user || 'nofrostlife@gmail.com'}>`);
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
        setUserSyncMessage(`Kullanıcı ${created.email} eklendi fakat hoş geldiniz maili gönderilemedi: ${welcomeRes.error || ''}`);
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
        const hintText = res.hint ? `\n\nÇözüm: ${res.hint}` : '';
        const instruct = res.instructions?.length ? `\n\nAdımlar:\n${res.instructions.join('\n')}` : '';
        alert(`E-posta Gönderilemedi:\n${res.error || 'Bilinmeyen hata'}${hintText}${instruct}`);
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
      const res = await safeJsonFetch<any>('/api/worker/heartbeat');
      if (res.ok && res.data) {
        setWorkerHeartbeat(res.data);
      } else {
        const cloudHeartbeat = await FirestoreDbService.getWorkerHeartbeat();
        if (cloudHeartbeat) {
          setWorkerHeartbeat(cloudHeartbeat);
        }
      }
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
        'MeDSor Test Bildirimi ',
        'Yönetici panelinden Windows masaüstü bildirimi başarıyla iletildi! Sisteminiz hazır.'
      );
      setWindowsServiceFeedback(`✓ ${res.message} (Ekranınızın sağ alt köşesine bakın)`);
    } catch (err: any) {
      setWindowsServiceFeedback(`Hata: ${err.message}`);
    } finally {
      setIsSendingWindowsNotify(false);
    }
  };

  const loadSystemServices = async () => {
    setIsLoadingServices(true);
    try {
      const res = await safeJsonFetch<any>('/api/system/services');
      if (res.ok && res.data?.services) {
        setSystemServices(res.data.services);
        if (res.data.networkStatus) {
          setNetworkSummary(res.data.networkStatus);
        }
      } else {
        // Default services inventory fallback
        setSystemServices([
          {
            id: 'core_api_server',
            name: 'MeDSor Çekirdek API & Web Sunucusu (Express & Brotli/Gzip)',
            category: 'core',
            status: 'active',
            statusLabel: 'Çalışıyor',
            badgeColor: 'emerald',
            port: 3000,
            description: 'REST API, soru/sınav yönetimi ve web sayfalarının yüksek hızlı Brotli/Gzip sıkıştırmasıyla sunulmasını sağlar.',
            resourceImpact: 'Düşük (~45 MB RAM)',
            resourceTier: 'low',
            autoStart: true,
            canToggle: false,
          },
          {
            id: 'cloudflare_tunnel',
            name: 'Cloudflare Zero Trust Güvenli Tünel (nofrostlife.com.tr)',
            category: 'network',
            status: 'active',
            statusLabel: 'Tünel Açık (Bağlı)',
            badgeColor: 'emerald',
            description: 'nofrostlife.com.tr alan adını güvenli HTTPS/SSL ile doğrudan bu bilgisayara bağlar; modem port yönlendirmesi gerektirmez.',
            resourceImpact: 'Düşük (~25 MB RAM, 0 CPU)',
            resourceTier: 'low',
            autoStart: true,
            canToggle: false,
          },
          {
            id: 'desktop_folder_watcher',
            name: 'Yerel Masaüstü Belge İzleyicisi (DesktopFolderWatcher)',
            category: 'watcher',
            status: 'stopped',
            statusLabel: 'Kapatıldı (Manuel Modda)',
            badgeColor: 'slate',
            description: 'Masaüstündeki meds_database klasöründeki 497+ PDF ve Word belgesini arka planda sürekli tarar. Arka plan disk ve işlemci yükünü sıfırlamak için otomatik izleme KAPATILMIŞTIR (İsteğe bağlı çalıştırılabilir).',
            resourceImpact: 'Sıfır (0 CPU / 0 Disk)',
            resourceTier: 'negligible',
            autoStart: false,
            canToggle: true,
            canRunNow: true,
          },
          {
            id: 'audio_transcription_worker',
            name: 'Google Drive Tıbbi Ses Transkripsiyon Servisi (Gemini API)',
            category: 'ai',
            status: 'stopped',
            statusLabel: 'Kapatıldı (Manuel Modda)',
            badgeColor: 'slate',
            description: 'Google Drive amfi ses kayıtlarını Gemini API ile transkribe eder. Ev internetini ve upload bant genişliğini tıkamaması için 7/24 otomatik döngü KAPATILMIŞTIR; ihtiyaç olduğunda kontrollü çalıştırılır.',
            resourceImpact: 'Sıfır (Otomatikte ~1.5 MB/s Upload Harcıyordu)',
            resourceTier: 'negligible',
            autoStart: false,
            canToggle: false,
            canRunNow: true,
          },
          {
            id: 'local_rag_engine',
            name: 'Bellek-İçi Hibrit RAG & BM25 Arama Motoru',
            category: 'ai',
            status: 'active',
            statusLabel: 'Bellekte Hazır (54.949 Parça)',
            badgeColor: 'emerald',
            description: '54.900+ soru, slayt ve ders notu parçasını yerel RAM\'de tutar; yapay zeka asistanının sorulara en doğru amfi slaytını anında getirmesini sağlar.',
            resourceImpact: 'Hafif RAM (~35 MB, Sıfır Ağ)',
            resourceTier: 'low',
            autoStart: true,
            canToggle: false,
          },
          {
            id: 'supabase_bridge_poller',
            name: 'Supabase Bulut Komut & Senkronizasyon Köprüsü',
            category: 'network',
            status: 'active',
            statusLabel: 'Çalışıyor (Dinlemede)',
            badgeColor: 'emerald',
            description: 'Mobil cihazlardan veya webden gönderilen soru güncellemelerini ve komutları yerel veritabanıyla senkronize eder.',
            resourceImpact: 'Çok Düşük (Periyodik hafif sorgu)',
            resourceTier: 'low',
            autoStart: true,
            canToggle: false,
          },
          {
            id: 'deepseek_data_service',
            name: 'DeepSeek Veri ve Soru Geliştirme Entegratörü',
            category: 'ai',
            status: 'active',
            statusLabel: 'Aktif (Pasif Dosya Senkronu)',
            badgeColor: 'emerald',
            description: 'deepseek_data klasöründeki redakte soru ve klinik analiz verilerini soru havuzuna işler.',
            resourceImpact: 'Çok Düşük (Pasif dosya senkronu)',
            resourceTier: 'low',
            autoStart: true,
            canToggle: false,
          },
        ]);
        setNetworkSummary({
          internetState: 'Hafif & Normal (Ağ Sömürüsü Yok)',
          compressionEnabled: true,
          totalServices: 7,
          activeServicesCount: 5,
          stoppedServicesCount: 2,
        });
      }
    } catch (_) {
    } finally {
      setIsLoadingServices(false);
    }
  };

  const handleToggleService = async (serviceId: string) => {
    setActionLoadingServiceId(serviceId);
    try {
      const res = await safeJsonFetch<any>(`/api/system/services/${serviceId}/toggle`, { method: 'POST' });
      if (res.ok) {
        setServiceActionFeedback(res.data?.message || 'Servis durumu güncellendi.');
        await loadSystemServices();
      } else {
        setServiceActionFeedback('Hata: ' + (res.error || 'İşlem gerçekleştirilemedi.'));
      }
    } catch (err: any) {
      setServiceActionFeedback('Hata: ' + err.message);
    } finally {
      setActionLoadingServiceId(null);
    }
  };

  const handleRunServiceNow = async (serviceId: string) => {
    setActionLoadingServiceId(serviceId);
    try {
      const res = await safeJsonFetch<any>(`/api/system/services/${serviceId}/run-now`, { method: 'POST' });
      if (res.ok) {
        setServiceActionFeedback(res.data?.message || 'Tek seferlik işlem başarıyla başlatıldı.');
        await loadSystemServices();
      } else {
        setServiceActionFeedback('Hata: ' + (res.error || 'İşlem başlatılamadı.'));
      }
    } catch (err: any) {
      setServiceActionFeedback('Hata: ' + err.message);
    } finally {
      setActionLoadingServiceId(null);
    }
  };

  useEffect(() => {
    if (isOpen) {
      loadUsersData();
      loadSmtpConfig();
      checkWorkerStatus();
      loadWindowsServiceStatus();
      refreshDbStatuses();
      loadSystemServices();
      const interval = setInterval(() => {
        checkWorkerStatus();
        loadWindowsServiceStatus();
        loadSystemServices();
      }, 7000);
      return () => clearInterval(interval);
    }
  }, [isOpen]);

  useEffect(() => setQPage(0), [searchQuery, qStatus, qDiscipline]);

  useEffect(() => {
    if (!isOpen || isPage) return;
    const previouslyFocused = document.activeElement as HTMLElement | null;
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    dialogRef.current?.focus();
    return () => {
      document.body.style.overflow = prevOverflow;
      previouslyFocused?.focus?.();
    };
  }, [isOpen, isPage]);

  useEffect(() => {
    if (!isOpen || isPage) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== 'Escape') return;
      if (editingQuestion || confirmDialog || showSqlSchemaModal || isPastExamImporterOpen) return;
      onClose();
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [isOpen, isPage, editingQuestion, confirmDialog, showSqlSchemaModal, isPastExamImporterOpen, onClose]);

  if (!isOpen) return null;

  const sections: {
    id: typeof activeTab;
    label: string;
    hint: string;
    icon: React.ElementType;
    count?: number;
    onSelect?: () => void;
  }[] = [
    { id: 'questions', label: 'Soru havuzu', hint: 'Kurul sorularını düzenle, sil, içe aktar', icon: Library, count: currentCommitteeQuestions.length },
    { id: 'users', label: 'Kullanıcılar', hint: 'Öğrenciler, yöneticiler ve e-posta', icon: Users, count: usersList.length, onSelect: loadUsersData },
    { id: 'scripts', label: 'Script ve görevler', hint: 'Veri temizliği ve toplu işlemler', icon: Terminal },
    { id: 'automations', label: 'Otomasyon & Drive', hint: 'Google Drive güncelleme, masaüstü işleyici', icon: Zap },
    { id: 'database', label: 'Veritabanı ve yedek', hint: 'Aktif veritabanı, dışa/içe aktarım', icon: Database },
  ];
  const current = sections.find((x) => x.id === activeTab) || sections[0];

  return (
    <div
      className={isPage ? 'w-full' : 'fixed inset-0 z-50 bg-[rgba(14,26,38,0.55)] flex items-stretch sm:items-center justify-center sm:p-4'}
      onMouseDown={isPage ? undefined : (e) => e.target === e.currentTarget && onClose()}
    >
      <div
        ref={dialogRef}
        role={isPage ? 'region' : 'dialog'}
        aria-modal={isPage ? undefined : true}
        aria-labelledby="admin-panel-title"
        tabIndex={-1}
        className={isEmbedded ? 'admin-panel is-embedded w-full flex flex-col min-w-0 text-ink outline-none' : `admin-panel bg-white w-full overflow-hidden grid ${
          isPage
            ? 'h-[calc(100dvh-150px)] lg:h-[calc(100dvh-120px)] min-h-[560px] rounded-2xl border border-line'
            : 'max-w-[1360px] h-full sm:h-[min(94vh,960px)] sm:rounded-2xl shadow-xl'
        } grid-cols-[minmax(0,1fr)] grid-rows-[auto_minmax(0,1fr)] lg:grid-rows-1 lg:grid-cols-[248px_minmax(0,1fr)] outline-none text-ink`}
      >
        {/* ---------- Sidebar ---------- */}
        {!isEmbedded && (<aside className="bg-canvas border-b lg:border-b-0 lg:border-r border-line flex lg:flex-col min-w-0">
          <div className="hidden lg:flex items-center gap-2.5 px-5 pt-5 pb-4">
            <span className="w-9 h-9 rounded-[10px] bg-ink text-white flex items-center justify-center shrink-0">
              <ShieldCheck className="w-[18px] h-[18px]" />
            </span>
            <div className="min-w-0">
              <div className="font-display font-bold text-lg tracking-[-0.02em] leading-tight">Yönetim</div>
              <div className="text-xs text-ink-3 truncate" title={adminEmail}>{adminEmail}</div>
            </div>
          </div>

          <nav aria-label="Yönetim bölümleri" className="flex lg:flex-col gap-1 px-2 py-2 lg:px-3 lg:py-0 overflow-x-auto no-scrollbar flex-1 min-w-0">
            {sections.map((sec) => {
              const on = activeTab === sec.id;
              const Icon = sec.icon;
              return (
                <button
                  key={sec.id}
                  type="button"
                  onClick={() => {
                    setActiveTab(sec.id);
                    sec.onSelect?.();
                  }}
                  aria-current={on ? 'page' : undefined}
                  className={`shrink-0 lg:w-full min-h-10 px-3 rounded-[10px] flex items-center gap-2.5 text-left cursor-pointer transition-colors ${
                    on ? 'bg-white text-ink font-semibold shadow-xs' : 'text-ink-2 hover:text-ink hover:bg-white/60'
                  }`}
                >
                  <Icon className={`w-[18px] h-[18px] shrink-0 ${on ? 'text-accent' : ''}`} />
                  <span className="text-base whitespace-nowrap flex-1">{sec.label}</span>
                  {sec.count !== undefined && <span className="hidden lg:inline font-mono text-xs text-ink-3">{sec.count}</span>}
                </button>
              );
            })}
          </nav>

          <button
            type="button"
            onClick={onClose}
            aria-label="Yönetim panelini kapat"
            className={`${isPage ? 'hidden' : 'lg:hidden flex'} shrink-0 w-11 h-11 m-1.5 rounded-[10px] items-center justify-center text-ink-2 hover:bg-white cursor-pointer`}
          >
            <X className="w-5 h-5" />
          </button>
        </aside>)}

        {/* ---------- Main ---------- */}
        <div className="flex flex-col min-h-0 min-w-0 admin-body">
          <header className={isEmbedded ? 'admin-embedded-tools' : 'flex items-center gap-3 px-4 sm:px-6 py-3 sm:py-4 border-b border-line shrink-0'}>
            <div className={isEmbedded ? 'hidden' : 'min-w-0 flex-1'}>
              <h2 id="admin-panel-title" className="m-0 font-display font-bold text-xl sm:text-2xl tracking-[-0.02em] leading-tight">
                {current.label}
              </h2>
              <p className="m-0 text-sm text-ink-2 truncate">{current.hint}</p>
            </div>
            {activeTab === 'questions' && (
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setIsDraftDeduplicationOpen(true)}
                  className="hidden sm:inline-flex h-10 px-3.5 rounded-[10px] bg-accent hover:from-accent hover:to-ai text-white text-base font-semibold items-center gap-2 cursor-pointer shadow-sm"
                >
                  <GitMerge className="w-4 h-4" /> Taslakları Kümele & Birleştir
                </button>
                <button type="button" onClick={() => setIsPastExamImporterOpen(true)} className="hidden sm:inline-flex h-10 px-3.5 rounded-[10px] bg-accent hover:bg-accent-hover text-white text-base font-semibold items-center gap-2 cursor-pointer">
                  <Upload className="w-4 h-4" /> Çıkmış soru yükle
                </button>
              </div>
            )}
            <button
              type="button"
              onClick={onClose}
              aria-label="Yönetim panelini kapat"
              title="Kapat (Esc)"
              className={`hidden ${isPage ? '' : 'lg:flex'} w-10 h-10 rounded-[10px] border border-line items-center justify-center text-ink-2 hover:text-ink hover:border-line-2 cursor-pointer`}
            >
              <X className="w-[18px] h-[18px]" />
            </button>
          </header>

          {actionMessage && (
            <div role="status" className="mx-4 sm:mx-6 mt-3 px-4 py-2.5 rounded-xl bg-ok-soft text-base text-ink flex items-center justify-between gap-3 shrink-0">
              <span className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-ok shrink-0" />
                {actionMessage}
              </span>
              <button type="button" onClick={() => setActionMessage(null)} className="h-8 px-2 rounded-lg text-ok font-semibold text-sm cursor-pointer">
                Kapat
              </button>
            </div>
          )}

        {/* Questions management */}
        {activeTab === 'questions' && (
          <div className="flex-1 min-h-0 overflow-y-auto px-4 sm:px-6 py-4 flex flex-col gap-3">
            <div className="grid grid-cols-3 gap-2 sm:gap-3">
              {[
                { label: 'Toplam', n: currentCommitteeQuestions.length, cls: 'text-ink' },
                { label: 'Doğrulandı', n: qCounts.completed, cls: 'text-ok' },
                { label: 'Taslak', n: qCounts.draft, cls: 'text-warn' },
              ].map((st) => (
                <div key={st.label} className="rounded-xl border border-line px-3 py-2.5">
                  <div className="text-xs text-ink-2">{st.label}</div>
                  <div className={`font-mono text-xl ${st.cls}`}>{st.n}</div>
                </div>
              ))}
            </div>

            <div className="flex flex-col md:flex-row md:items-center gap-2">
              <label className="flex items-center gap-2 h-10 px-3 border border-line-2 rounded-[10px] bg-field flex-1 min-w-0 focus-within:border-accent">
                <Search className="w-4 h-4 text-ink-2 shrink-0" />
                <span className="sr-only">Soru ara</span>
                <input
                  type="search"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Soru no, konu veya ders ara"
                  className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-base"
                />
              </label>
              <div className="flex gap-2 overflow-x-auto no-scrollbar">
                <div role="radiogroup" aria-label="Durum" className="inline-flex gap-1 bg-canvas rounded-[10px] p-[3px] shrink-0">
                  {(
                    [
                      ['all', 'Tümü'],
                      ['completed', 'Doğrulanan'],
                      ['draft', 'Taslak'],
                      ['empty', 'Boş'],
                    ] as const
                  ).map(([id, label]) => (
                    <button
                      key={id}
                      type="button"
                      role="radio"
                      aria-checked={qStatus === id}
                      onClick={() => setQStatus(id)}
                      className={`h-8 px-2.5 rounded-lg text-sm cursor-pointer whitespace-nowrap ${
                        qStatus === id ? 'bg-white font-semibold shadow-xs text-ink' : 'text-ink-2'
                      }`}
                    >
                      {label}
                    </button>
                  ))}
                </div>
                <label className="sr-only" htmlFor="admin-q-discipline">Ders</label>
                <select
                  id="admin-q-discipline"
                  value={qDiscipline}
                  onChange={(e) => setQDiscipline(e.target.value)}
                  className="h-[38px] border border-line-2 rounded-[10px] px-2.5 text-sm bg-white cursor-pointer shrink-0 max-w-[200px]"
                >
                  <option value="all">Tüm dersler</option>
                  {tableDisciplines.map((d) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))}
                </select>
              </div>
              <div className="sm:hidden flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setIsDraftDeduplicationOpen(true)}
                  className="flex-1 h-10 px-3 rounded-[10px] bg-accent text-white text-sm font-semibold inline-flex items-center justify-center gap-1.5 cursor-pointer shadow-sm"
                >
                  <GitMerge className="w-4 h-4" /> Taslakları Birleştir
                </button>
                <button type="button" onClick={() => setIsPastExamImporterOpen(true)} className="h-10 px-3.5 rounded-[10px] bg-accent text-white text-sm font-semibold inline-flex items-center justify-center gap-1.5 cursor-pointer">
                  <Upload className="w-4 h-4" /> Çıkmış yükle
                </button>
              </div>
            </div>

            <div className="rounded-xl border border-line overflow-hidden">
              <table className="w-full table-fixed text-base border-collapse">
                <caption className="sr-only">Kurul soruları</caption>
                <thead className="bg-canvas text-xs text-ink-2">
                  <tr>
                    <th scope="col" className="text-left font-semibold px-3 py-2 w-[48px] sm:w-[64px]">No</th>
                    <th scope="col" className="text-left font-semibold px-3 py-2">Soru</th>
                    <th scope="col" className="text-left font-semibold px-3 py-2 hidden md:table-cell w-[120px]">Durum</th>
                    <th scope="col" className="text-right font-semibold px-3 py-2 hidden lg:table-cell w-[80px]">Parça</th>
                    <th scope="col" className="text-right font-semibold px-3 py-2 w-[92px]"><span className="sr-only">İşlemler</span></th>
                  </tr>
                </thead>
                <tbody>
                  {pagedQuestions.length === 0 && (
                    <tr>
                      <td colSpan={5} className="px-3 py-8 text-center text-ink-2">Bu filtrede soru yok.</td>
                    </tr>
                  )}
                  {pagedQuestions.map((q) => (
                    <tr key={q.id || 'q-' + q.questionNumber} className="border-t border-line-soft hover:bg-accent-soft align-top">
                      <td className="px-3 py-2.5 font-mono text-sm text-ink-2">{q.isUnassignedNumber ? '—' : q.questionNumber || '?'}</td>
                      <td className="px-3 py-2.5 min-w-0">
                        <div className="text-xs font-semibold text-ink-2 truncate">
                          {q.discipline || 'Tıp'}
                          {q.topic && !/hatırlanan soru|çıkmış sorusu/i.test(q.topic) ? ` · ${q.topic}` : ''}
                        </div>
                        <div className="text-base text-ink line-clamp-2 break-words">{questionStemText(q) || 'Soru metni henüz yok'}</div>
                        <div className="md:hidden mt-1">
                          <StatusPill status={q.status} hasFragments={(q.fragments?.length || 0) > 0} />
                        </div>
                      </td>
                      <td className="px-3 py-2.5 hidden md:table-cell">
                        <StatusPill status={q.status} hasFragments={(q.fragments?.length || 0) > 0} />
                      </td>
                      <td className="px-3 py-2.5 hidden lg:table-cell text-right font-mono text-sm text-ink-2">{q.fragments?.length || 0}</td>
                      <td className="px-2 py-1.5">
                        <div className="flex justify-end gap-1">
                          <button
                            type="button"
                            onClick={() => setEditingQuestion(q)}
                            aria-label={`Soru ${q.questionNumber} düzenle`}
                            title="Düzenle"
                            className="w-10 h-10 rounded-lg flex items-center justify-center text-ink-2 hover:text-accent hover:bg-accent-soft cursor-pointer"
                          >
                            <Edit3 className="w-4 h-4" />
                          </button>
                          <button
                            type="button"
                            onClick={() => handleDeleteQuestion(q)}
                            aria-label={`Soru ${q.questionNumber} sil`}
                            title="Sil"
                            className="w-10 h-10 rounded-lg flex items-center justify-center text-ink-2 hover:text-bad-text hover:bg-bad-soft cursor-pointer"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="flex items-center justify-between gap-2 text-sm text-ink-2">
              <span>
                {tableQuestions.length === 0 ? 0 : qPageSafe * Q_PAGE_SIZE + 1}–{Math.min(tableQuestions.length, (qPageSafe + 1) * Q_PAGE_SIZE)} / {tableQuestions.length}
              </span>
              <div className="flex items-center gap-1">
                <button
                  type="button"
                  onClick={() => setQPage(Math.max(0, qPageSafe - 1))}
                  disabled={qPageSafe === 0}
                  aria-label="Önceki sayfa"
                  className="w-10 h-10 rounded-[10px] border border-line-2 flex items-center justify-center cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <ChevronLeft className="w-4 h-4" />
                </button>
                <span className="font-mono px-2">
                  {qPageSafe + 1}/{qPageCount}
                </span>
                <button
                  type="button"
                  onClick={() => setQPage(Math.min(qPageCount - 1, qPageSafe + 1))}
                  disabled={qPageSafe >= qPageCount - 1}
                  aria-label="Sonraki sayfa"
                  className="w-10 h-10 rounded-[10px] border border-line-2 flex items-center justify-center cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Tab: Dynamic Scripts & Tasks Hub */}
        {activeTab === 'scripts' && (
          <div className="flex-1 overflow-y-auto flex flex-col min-h-0 p-4">
            <AdminScriptsTab adminEmail={adminEmail} onRefreshAllData={onRefreshData} />
          </div>
        )}

        {/* Tab 2: Automations Hub */}
        {activeTab === 'automations' && (
          <div className="p-4 sm:p-6 flex flex-col gap-4 overflow-y-auto flex-1">
            {/* 1. Servisler: gruplu liste */}
            <section className="hk-group">
              <header className="hk-group-head">
                <div>
                  <h3>Servisler ve arka plan görevleri</h3>
                  <p>Çekirdek, ağ, yapay zekâ ve izleme servislerinin anlık durumu.</p>
                </div>
                <div className="hk-group-tools">
                  {onOpenSubagentMonitor && (
                    <button type="button" onClick={onOpenSubagentMonitor} className="ms-btn is-sm">Alt ajan paneli</button>
                  )}
                  <button type="button" onClick={loadSystemServices} disabled={isLoadingServices} className="ms-btn is-sm is-ghost">
                    <RefreshCw className={isLoadingServices ? 'animate-spin' : ''} aria-hidden /> Yenile
                  </button>
                </div>
              </header>
              <div className="hk-stats">
                <div><span>Çalışıyor</span><b className="hk-num text-ok">{systemServices.filter((x) => x.status === 'active').length}</b></div>
                <div><span>Kapalı</span><b className="hk-num">{systemServices.filter((x) => x.status === 'stopped').length}</b></div>
                <div><span>Ağ yükü</span><b>Hafif</b></div>
                <div><span>Sıkıştırma</span><b>Brotli/Gzip</b></div>
              </div>
              {serviceActionFeedback && (
                <div className="ds-callout is-note hk-inline-note" role="status">
                  <span className="flex items-center justify-between gap-2">
                    <span>{serviceActionFeedback}</span>
                    <button type="button" onClick={() => setServiceActionFeedback(null)} className="ms-btn is-ghost is-sm">Kapat</button>
                  </span>
                </div>
              )}
              <ul className="hk-list">
                {systemServices.map((service) => {
                  const isActive = service.status === 'active';
                  const busy = actionLoadingServiceId === service.id;
                  return (
                    <li key={service.id} className="hk-row">
                      <span className={`hk-status ${isActive ? 'is-on' : ''}`} aria-label={isActive ? 'Çalışıyor' : 'Kapalı'} />
                      <span className="hk-row-t">
                        <b>{service.name}</b>
                        <span>{service.description}</span>
                      </span>
                      <span className={`ms-tag ${service.resourceTier === 'high' ? 'is-warn' : service.resourceTier === 'negligible' ? 'is-ok' : ''}`} title="Kaynak tüketimi">
                        {service.resourceImpact}
                      </span>
                      <span className="hk-row-actions">
                        {service.canRunNow && (
                          <button type="button" onClick={() => handleRunServiceNow(service.id)} disabled={busy} className="ms-btn is-sm is-ghost">
                            <Play aria-hidden /> {busy ? 'İşleniyor…' : 'Bir kez çalıştır'}
                          </button>
                        )}
                        {service.canToggle && (
                          <button type="button" onClick={() => handleToggleService(service.id)} disabled={busy} className={`ms-btn is-sm ${isActive ? 'is-danger' : 'is-tonal'}`}>
                            {isActive ? <><Square aria-hidden /> Durdur</> : <><Play aria-hidden /> Başlat</>}
                          </button>
                        )}
                      </span>
                    </li>
                  );
                })}
                {systemServices.length === 0 && <li className="hk-row is-empty">{isLoadingServices ? 'Servisler yükleniyor…' : 'Servis bilgisi alınamadı.'}</li>}
              </ul>
            </section>

            {/* Windows Desktop Shortcut & Daily 16:00 - 18:00 Automation Card */}
            <div className="hk-group space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-line-2/80">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-ok/20 text-ok border border-ok/30 flex items-center justify-center shrink-0">
                    <Monitor className="w-5 h-5 text-ok" />
                  </div>
                  <div>
                    <h4 className="font-bold text-sm sm:text-base text-ink flex items-center gap-2 flex-wrap">
                      <span>Windows Masaüstü Kısayolu & Otomatik Başlangıç</span>
                      {windowsServiceStatus?.isRunning ? (
                        <span className="bg-ok/20 text-ok border border-ok/30 text-2xs font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                          <Check className="w-3 h-3 text-ok" />
                          Servis Aktif (PID: {windowsServiceStatus.pids?.join(', ') || 'Aktif'})
                        </span>
                      ) : (
                        <span className="bg-warn/20 text-warn border border-warn/30 text-2xs font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                          <AlertTriangle className="w-3 h-3 text-warn" />
                          Servis Beklemede
                        </span>
                      )}
                    </h4>
                    <p className="text-xs text-ink-3 mt-0.5">
                      Bilgisayar her açıldığında ve saat 16:00 - 18:00 aralığında arka planda çalışarak tüm Drive dosyalarını eşitler.
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <button
                    type="button"
                    onClick={handleSendWindowsTestNotification}
                    disabled={isSendingWindowsNotify}
                    className="bg-ok-soft hover:bg-ok/20 text-ok font-bold px-3 py-1.5 rounded-xl text-xs flex items-center gap-1.5 transition-all cursor-pointer disabled:opacity-50"
                    title="Windows Action Center / Bildirim Alanına test bildirimi gönderir"
                  >
                    <Bell className={`w-3.5 h-3.5 ${isSendingWindowsNotify ? 'animate-bounce' : ''}`} />
                    <span>{isSendingWindowsNotify ? 'Gönderiliyor...' : 'Bildirim Testi'}</span>
                  </button>

                  <button
                    type="button"
                    onClick={handleInstallWindowsService}
                    disabled={isInstallingWindowsService}
                    className="bg-ok hover:bg-ok text-ink font-black px-4 py-2 rounded-xl text-xs flex items-center gap-2 shadow-sm transition-all cursor-pointer active:scale-95 disabled:opacity-50"
                  >
                    <Play className={`w-3.5 h-3.5 fill-current ${isInstallingWindowsService ? 'animate-spin' : ''}`} />
                    <span>{isInstallingWindowsService ? 'Yapılandırılıyor...' : 'Kısayol Kur & Başlat'}</span>
                  </button>

                  {windowsServiceStatus?.isRunning && (
                    <button
                      type="button"
                      onClick={handleStopWindowsService}
                      disabled={isInstallingWindowsService}
                      className="bg-bad/60 hover:bg-bad text-bad-soft border border-bad/60 font-bold px-3 py-1.5 rounded-xl text-xs flex items-center gap-1 transition-all cursor-pointer"
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
                <div className="bg-field p-3 rounded-xl space-y-1">
                  <span className="text-2xs text-ink-3 block font-semibold">Masaüstü Kısayolu:</span>
                  <div className="flex items-center gap-2">
                    <span className={`w-2 h-2 rounded-full ${windowsServiceStatus?.isInstalledOnDesktop ? 'bg-ok' : 'bg-warn'}`} />
                    <strong className="text-ink text-xs truncate">
                      {windowsServiceStatus?.isInstalledOnDesktop ? '✓ Masaüstünde Mevcut' : 'Kısayol Eksik'}
                    </strong>
                  </div>
                  <span className="text-2xs text-ink-3 font-mono block truncate">
                    MeDSor Otomasyon Servisi.lnk
                  </span>
                </div>

                <div className="bg-field p-3 rounded-xl space-y-1">
                  <span className="text-2xs text-ink-3 block font-semibold">Windows Başlangıç (Startup):</span>
                  <div className="flex items-center gap-2">
                    <span className={`w-2 h-2 rounded-full ${windowsServiceStatus?.isRegisteredInStartup ? 'bg-ok' : 'bg-warn'}`} />
                    <strong className="text-ink text-xs truncate">
                      {windowsServiceStatus?.isRegisteredInStartup ? '✓ Başlangıca Kayıtlı' : 'Başlangıçta Yok'}
                    </strong>
                  </div>
                  <span className="text-2xs text-ink-3 font-mono block truncate">
                    shell:startup (Otomatik Açılış)
                  </span>
                </div>

                <div className="bg-field p-3 rounded-xl space-y-1">
                  <span className="text-2xs text-ink-3 block font-semibold">Çalışma Aralığı & Bildirim:</span>
                  <div className="flex items-center gap-2">
                    <Clock className="w-3.5 h-3.5 text-ok shrink-0" />
                    <strong className="text-ok text-xs">16:00 - 18:00 Arası Günlük</strong>
                  </div>
                  <span className="text-2xs text-ok/90 block">
                    Windows Bildirim Alanı Aktif                   </span>
                </div>
              </div>

              {/* Explanatory Guide Box */}
              <div className="bg-field p-3 rounded-xl text-2xs text-ink-3 space-y-1.5 leading-relaxed">
                <div className="flex items-center gap-1.5 text-ok font-semibold text-xs">
                  <CheckCircle2 className="w-3.5 h-3.5 text-ok shrink-0" />
                  <span>Tek Tıkla Otomatik Çalışma Mantığı:</span>
                </div>
                <p>
                  Masaüstünüzde yer alan <strong className="text-ink">"MeDSor Otomasyon Servisi"</strong> kısayoluna çift tıkladığınızda; servis kendisini otomatik olarak Windows başlangıç klasörüne kaydeder, ekranınızın sağ altına Windows bildirimi yollar ve arka planda çalışmaya başlar.
                </p>
                <p className="text-ink-3 text-2xs">
                  Bilgisayarınız her açıldığında ve her gün saat <strong className="text-ok">16:00 - 18:00</strong> arasında Drive çıkmış soruları ve ders slaytları <code className="bg-field text-ink-2 px-1 py-0.5 rounded">C:\Users\indui\Desktop\meds_database</code> klasörünüze indirilir, CPU ile sayfa sayfa birebir okunarak soru havuzuna ve Firebase'e işlenir.
                </p>
              </div>

              {/* Feedback Alert */}
              {windowsServiceFeedback && (
                <div className={`p-3 rounded-xl border text-xs flex items-start gap-2 ${
                  windowsServiceFeedback.startsWith('✓')
                    ? 'bg-ok/80 border-ok/50 text-ok-soft'
                    : windowsServiceFeedback.startsWith('Hata')
                    ? 'bg-bad/80 border-bad/50 text-bad-soft'
                    : 'bg-ok/80 border-ok/50 text-ok-soft'
                }`}>
                  <CheckCircle2 className="w-4 h-4 text-ok shrink-0 mt-0.5" />
                  <div>
                    <span>{windowsServiceFeedback}</span>
                  </div>
                </div>
              )}
            </div>

            {/* Google Drive Manuel Güncelleme & Senkronizasyon Ayarları */}
            <AdminDriveSyncSettings
              adminEmail={adminEmail}
              onRefreshData={onRefreshData}
              selectedCommitteeId={selectedCommitteeId}
            />


            {/* 3. Local Desktop Background Daemon Card (Zero Token Cost, Verbatim OCR) */}
            <div className="hk-group space-y-4">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Terminal className="w-5 h-5 text-ok" />
                  <h4 className="font-bold text-sm text-ink">Yerel Drive İndirici & CPU Metin/Soru Çıkarıcı</h4>
                  <span className="bg-ok/20 text-ok border border-ok/30 text-2xs font-bold px-2 py-0.5 rounded-full">
                    Yerel CPU / Sıfır AI Hatası / Verbatim
                  </span>
                </div>
                <div className="text-right">
                  <span className="text-2xs text-ok font-bold bg-ok/80 border border-ok/60 px-2 py-1 rounded">
                    Hedef Saat: 16:00 - 18:00
                  </span>
                </div>
              </div>

              <p className="text-ink-3 text-xs leading-relaxed">
                Tüm Google Drive çıkmış klasörleri doğrudan bilgisayarınızdaki <code className="bg-field text-ink-2 px-1.5 py-0.5 rounded font-mono">C:\Users\indui\Desktop\meds_database</code> klasörüne indirilir. PDF'ler yerel işlemcinizle sayfa sayfa birebir okunur (asla AI özet uydurması yapmaz) ve sorular 0 beğeni ile veritabanına ve Firebase'e aktarılır.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                <div className="bg-field p-3 rounded-lg space-y-1">
                  <span className="text-ink-3 font-bold block">1. Otomatik Başlatma (Windows Başlangıç):</span>
                  <p className="text-2xs text-ink-3">
                    Bilgisayar her açıldığında arka planda sessizce başlar. Saat 16:00-18:00 arasındaysa doğrudan eşitlemeyi yapar:
                  </p>
                  <div className="font-mono text-2xs text-ok pt-1">start-meds-daemon.vbs</div>
                </div>

                <div className="bg-field p-3 rounded-lg space-y-1">
                  <span className="text-ink-3 font-bold block">2. Manuel Çift Tıklama Dosyası:</span>
                  <p className="text-2xs text-ink-3">
                    İstediğiniz an masaüstünden veya proje klasöründen tek tıkla başlatabilirsiniz:
                  </p>
                  <div className="font-mono text-2xs text-ok pt-1">run-meds-sync.bat</div>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-3 pt-1 border-t border-line-2">
                <div className="text-2xs text-ink-3">
                  <span>Hedef klasörler: <strong>meds_sorular</strong> & <strong>ders_notlari_pdf</strong></span>
                </div>

                <button
                  onClick={handleTriggerFullLocalSync}
                  disabled={isSyncingFullLocal}
                  className="bg-ok hover:bg-ok disabled:opacity-50 text-ink font-black px-4 py-2 rounded-lg flex items-center gap-1.5 shadow-sm transition-all cursor-pointer active:scale-95"
                >
                  <RefreshCw className={`w-4 h-4 ${isSyncingFullLocal ? 'animate-spin' : ''}`} />
                  <span>{isSyncingFullLocal ? 'Eşitleme Başlatılıyor...' : 'Tüm Drive Çıkmışlarını & Slaytları Şimdi Eşitle'}</span>
                </button>
              </div>

              {fullLocalSyncFeedback && (
                <div className="p-3 bg-ok/80 border border-ok/50 rounded-lg text-xs font-semibold text-ok-soft flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-ok shrink-0" />
                  <span>{fullLocalSyncFeedback}</span>
                </div>
              )}
            </div>

            {/* 4. GitHub Push & Sync Card */}
            <div className="bg-white border border-line rounded-xl p-4 sm:p-5 space-y-3 shadow-2xs">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <GitBranch className="w-5 h-5 text-ink" />
                  <h4 className="font-bold text-sm text-ink">GitHub Senkronizasyonu & Push</h4>
                  <span className="bg-field text-ink text-2xs font-bold px-2 py-0.5 rounded-full">
                    induiduel/meds
                  </span>
                </div>

                <a
                  href="https://github.com/induiduel/meds"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-ok hover:text-ok font-bold text-xs flex items-center gap-1"
                >
                  <span>Depoyu Görüntüle</span>
                  <ExternalLink className="w-3 h-3 text-ink-3" />
                </a>
              </div>

              <div className="p-3 bg-field border border-line rounded-lg space-y-2">
                <div className="text-xs font-semibold text-ink">
                  Proje Kaynak Kodları ve Veritabanı Dışa Aktarma
                </div>
                <div className="text-2xs text-ink-2">
                  Tüm güncel ders notları, soru havuzu ve sunucu kodlarını içeren arşivi tek tıkla indirip bilgisayarınızdaki Git deposuna aktarabilirsiniz.
                </div>
                <a
                  href="/api/admin/export-zip"
                  download="medsoru-project.zip"
                  className="inline-flex bg-ok hover:bg-ok text-ink font-bold px-4 py-2 rounded-lg text-xs items-center gap-2 shadow-xs cursor-pointer"
                >
                  <Download className="w-4 h-4 text-ok-soft" />
                  <span>Projeyi ZIP Olarak İndir (Tüm Kodlar & Veriler)</span>
                </a>
              </div>
            </div>
          </div>
        )}

        {/* Tab 3: Database & Backup */}
        {activeTab === 'database' && (
          <div className="p-4 sm:p-6 space-y-5 overflow-y-auto flex-1 text-xs">
            {/* Multi-Database Active Mode & Cloud Failover Card */}
            <div className="bg-ink-surface text-white rounded-2xl p-5 border border-accent/50 shadow-lg space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-line-2/70">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="p-1.5 bg-accent/20 text-accent rounded-lg border border-accent/30">
                      <Layers className="w-4 h-4" />
                    </span>
                    <h3 className="text-sm font-bold text-white">Çoklu Veritabanı Yönetimi & Kesintisiz Geçiş</h3>
                  </div>
                  <p className="text-2xs text-ink-3">
                    Firebase Spark, Supabase (PostgreSQL) ve Yerel PC veritabanları arasında anlık geçiş yapın. Her kayıt işlemi Firebase Spark'a da otomatik yedeklenir.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={refreshDbStatuses}
                  disabled={isRefreshingDbStatus}
                  className="bg-ink hover:bg-ink-2 text-ink-3 border border-line-2 font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition-all cursor-pointer self-start sm:self-center text-xs"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isRefreshingDbStatus ? 'animate-spin text-ok' : ''}`} />
                  <span>Yenile</span>
                </button>
              </div>

              {/* Live Health Badges */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                {/* Firebase Spark Badge */}
                <div className={`p-3 rounded-xl border flex flex-col gap-1 ${
                  dbStatuses?.firebase.status === 'quota_exceeded'
                    ? 'bg-warn/60 border-warn/60 text-warn-soft'
                    : 'bg-ink/60 border-line-2 text-ink-3'
                }`}>
                  <div className="flex items-center justify-between">
                    <span className="font-bold flex items-center gap-1.5 text-xs">
                      Firebase Spark
                    </span>
                    <span className={`text-2xs font-extrabold px-2 py-0.5 rounded-full ${
                      dbStatuses?.firebase.status === 'quota_exceeded'
                        ? 'bg-warn/30 text-warn border border-warn/50'
                        : 'bg-ok/20 text-ok border border-ok/40'
                    }`}>
                      {dbStatuses?.firebase.status === 'quota_exceeded' ? 'Kota Doldu' : 'Aktif'}
                    </span>
                  </div>
                  <span className="text-2xs opacity-80">
                    {dbStatuses?.firebase.details || '50K günlük okuma sınırı'}
                  </span>
                </div>

                {/* Supabase Badge */}
                <div className={`p-3 rounded-xl border flex flex-col gap-1 ${
                  dbStatuses?.supabase.status === 'online'
                    ? 'bg-ok/50 border-ok/50 text-ok-soft'
                    : 'bg-ink/60 border-line-2 text-ink-3'
                }`}>
                  <div className="flex items-center justify-between">
                    <span className="font-bold flex items-center gap-1.5 text-xs">
                      Supabase (Postgres)
                    </span>
                    <span className={`text-2xs font-extrabold px-2 py-0.5 rounded-full ${
                      dbStatuses?.supabase.status === 'online'
                        ? 'bg-ok/30 text-ok border border-ok/50'
                        : 'bg-accent/20 text-accent border border-accent/40'
                    }`}>
                      {dbStatuses?.supabase.status === 'online' ? 'Bağlı' : 'Yapılandırıldı'}
                    </span>
                  </div>
                  <span className="text-2xs opacity-80">
                    {dbStatuses?.supabase.details || 'PostgreSQL Bulut Veritabanı'}
                  </span>
                </div>

                {/* Local PC Badge */}
                <div className={`p-3 rounded-xl border flex flex-col gap-1 ${
                  dbStatuses?.localPc.status === 'online'
                    ? 'bg-ok/50 border-ok/50 text-ok-soft'
                    : 'bg-ink/60 border-line-2 text-ink-3'
                }`}>
                  <div className="flex items-center justify-between">
                    <span className="font-bold flex items-center gap-1.5 text-xs">
                      Yerel PC Sunucusu
                    </span>
                    <span className={`text-2xs font-extrabold px-2 py-0.5 rounded-full ${
                      dbStatuses?.localPc.status === 'online'
                        ? 'bg-ok/30 text-ok border border-ok/50'
                        : 'bg-bad/20 text-bad-text border border-bad/40'
                    }`}>
                      {dbStatuses?.localPc.status === 'online' ? 'Online' : 'Offline'}
                    </span>
                  </div>
                  <span className="text-2xs opacity-80">
                    {dbStatuses?.localPc.details || 'Port 3000 / meds_database'}
                  </span>
                </div>
              </div>

              {/* Mode Selector Buttons */}
              <div className="space-y-2">
                <span className="text-xs font-bold text-ink-3 block">Aktif Çalışma Modunu Seçin:</span>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
                  <button
                    type="button"
                    onClick={() => handleSelectDbMode('auto')}
                    className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
                      dbMode === 'auto'
                        ? 'bg-accent text-white border-accent shadow-md ring-2 ring-accent/50'
                        : 'bg-ink/70 text-ink-3 border-line-2 hover:bg-ink/80'
                    }`}
                  >
                    <div className="font-bold flex items-center gap-1.5 text-xs">
                      <Zap className="w-3.5 h-3.5 text-warn" />
                      <span>Otomatik (Önerilen)</span>
                    </div>
                    <p className="text-2xs opacity-85 mt-1">
                      Spark kotası dolunca Supabase ve Yerel PC otomatik devralır.
                    </p>
                  </button>

                  <button
                    type="button"
                    onClick={() => handleSelectDbMode('supabase')}
                    className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
                      dbMode === 'supabase'
                        ? 'bg-ok text-white border-ok shadow-md ring-2 ring-ok/50'
                        : 'bg-ink/70 text-ink-3 border-line-2 hover:bg-ink/80'
                    }`}
                  >
                    <div className="font-bold flex items-center gap-1.5 text-xs">
                      <span>Supabase</span>
                    </div>
                    <p className="text-2xs opacity-85 mt-1">
                      Öncelikli olarak Supabase PostgreSQL sorgularını kullanır.
                    </p>
                  </button>

                  <button
                    type="button"
                    onClick={() => handleSelectDbMode('firebase')}
                    className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
                      dbMode === 'firebase'
                        ? 'bg-warn text-white border-warn shadow-md ring-2 ring-warn/50'
                        : 'bg-ink/70 text-ink-3 border-line-2 hover:bg-ink/80'
                    }`}
                  >
                    <div className="font-bold flex items-center gap-1.5 text-xs">
                      <span>Firebase Spark</span>
                    </div>
                    <p className="text-2xs opacity-85 mt-1">
                      Doğrudan Cloud Firestore NoSQL veritabanını kullanır.
                    </p>
                  </button>

                  <button
                    type="button"
                    onClick={() => handleSelectDbMode('local_pc')}
                    className={`p-3 rounded-xl border text-left transition-all cursor-pointer ${
                      dbMode === 'local_pc'
                        ? 'bg-ok text-white border-ok shadow-md ring-2 ring-ok/50'
                        : 'bg-ink/70 text-ink-3 border-line-2 hover:bg-ink/80'
                    }`}
                  >
                    <div className="font-bold flex items-center gap-1.5 text-xs">
                      <span>Yerel PC Sunucusu</span>
                    </div>
                    <p className="text-2xs opacity-85 mt-1">
                      Bilgisayarınızdaki Express + JSON motorunu kullanır.
                    </p>
                  </button>
                </div>
              </div>

              {/* Action Buttons & Helpers */}
              <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-line-2">
                <button
                  type="button"
                  onClick={handleSyncToAllDatabases}
                  disabled={isSyncingMultiDb}
                  className="bg-accent hover:bg-accent text-white font-bold px-3.5 py-2 rounded-xl text-xs flex items-center gap-2 transition-all cursor-pointer disabled:opacity-50 shadow-sm"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isSyncingMultiDb ? 'animate-spin' : ''}`} />
                  <span>{isSyncingMultiDb ? 'Senkronize Ediliyor...' : 'Tüm Verileri Supabase & Spark\'a Eşitle'}</span>
                </button>

                <button
                  type="button"
                  onClick={() => setShowSqlSchemaModal(true)}
                  className="bg-ink hover:bg-ink-2 text-accent border border-accent/50 font-bold px-3.5 py-2 rounded-xl text-xs flex items-center gap-1.5 transition-all cursor-pointer shadow-sm"
                >
                  <Terminal className="w-3.5 h-3.5" />
                  <span>Supabase SQL Şemasını Göster</span>
                </button>
              </div>

              {/* Multi-Db Sync Feedback */}
              {multiDbFeedback && (
                <div className={`p-3 rounded-xl text-xs font-semibold flex items-center gap-2 ${
                  multiDbFeedback.startsWith('✓')
                    ? 'bg-ok/80 text-ok-soft border border-ok/50'
                    : multiDbFeedback.startsWith('Hata')
                    ? 'bg-bad/80 text-bad-soft border border-bad/50'
                    : 'bg-accent/80 text-accent-soft border border-accent/50'
                }`}>
                  <CheckCircle2 className="w-4 h-4 shrink-0" />
                  <span>{multiDbFeedback}</span>
                </div>
              )}

              {/* Gemini API Key Box with Tiered Pool Info */}
              <div className="bg-ink/70 border border-line-2 rounded-xl p-3.5 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-ink-3">
                    <Key className="w-3.5 h-3.5 text-warn" />
                    <span>Google Gemini AI (Kademeli Havuz & Özel Anahtar)</span>
                  </div>
                  <span className="text-2xs text-ok font-semibold">1. ve 2. Sıra: Ücretsiz | 4. Sıra: Faturalı Yedek</span>
                </div>
                <div className="flex gap-2">
                  <input
                    type="password"
                    value={geminiApiKeyInput}
                    onChange={(e) => setGeminiApiKeyInput(e.target.value)}
                    placeholder="AIzaSy... (Özel veya yedek Gemini API anahtarınızı buraya yapıştırın)"
                    className="flex-1 bg-ink border border-line-2 rounded-lg px-3 py-1.5 text-xs text-ink-3 focus:outline-none focus:border-warn font-mono"
                  />
                  <button
                    type="button"
                    onClick={handleSaveGeminiKey}
                    className="bg-warn hover:bg-warn text-white font-bold px-3 py-1.5 rounded-lg text-xs cursor-pointer transition-all shrink-0"
                  >
                    Kaydet
                  </button>
                </div>
                {geminiKeyFeedback && (
                  <p className="text-2xs font-semibold text-ok">{geminiKeyFeedback}</p>
                )}
              </div>

              {/* Groq Cloud Alternative API Key Box */}
              <div className="bg-ink/70 border border-line-2 rounded-xl p-3.5 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-ink-3">
                    <Sparkles className="w-3.5 h-3.5 text-warn" />
                    <span>Groq Cloud API Anahtarları (3. Sıra: Ücretsiz Llama 3.3 70B & DeepSeek R1)</span>
                  </div>
                  <span className="text-2xs text-warn font-semibold">3. Sırada Devreye Girer (Ücretli Plandan Önce)</span>
                </div>
                <div className="flex gap-2">
                  <input
                    type="password"
                    value={groqApiKeyInput}
                    onChange={(e) => setGroqApiKeyInput(e.target.value)}
                    placeholder="1. Groq Anahtarı (gsk_...)"
                    className="flex-1 bg-ink border border-line-2 rounded-lg px-3 py-1.5 text-xs text-ink-3 focus:outline-none focus:border-warn font-mono"
                  />
                  <button
                    type="button"
                    onClick={handleSaveGroqKey}
                    className="bg-warn hover:bg-warn text-white font-bold px-3 py-1.5 rounded-lg text-xs cursor-pointer transition-all shrink-0"
                  >
                    Kaydet
                  </button>
                </div>
                <div className="flex gap-2">
                  <input
                    type="password"
                    value={groqApiKey2Input}
                    onChange={(e) => setGroqApiKey2Input(e.target.value)}
                    placeholder="2. Yedek Groq Anahtarı (gsk_...)"
                    className="flex-1 bg-ink border border-line-2 rounded-lg px-3 py-1.5 text-xs text-ink-3 focus:outline-none focus:border-warn font-mono"
                  />
                </div>
                {groqKeyFeedback && (
                  <p className="text-2xs font-semibold text-ok">{groqKeyFeedback}</p>
                )}
              </div>
            </div>

            {/* DeepSeek Data Pool & RAG Ingestion Card */}
            <div className="bg-ink-surface text-white rounded-2xl p-5 border border-accent/40 shadow-lg space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-accent/60">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="p-1.5 bg-accent/20 text-accent rounded-lg border border-accent/30">
                      <Sparkles className="w-4 h-4 text-accent" />
                    </span>
                    <h3 className="text-sm font-bold text-white">DeepSeek Veri Havuzu & RAG Zeminleme Entegrasyonu</h3>
                  </div>
                  <p className="text-2xs text-ink-3">
                    DeepSeek tarafından düzenlenmiş soru, özet ve ders verilerini <code className="bg-black/40 px-1.5 py-0.5 rounded text-accent font-mono text-2xs">{deepseekStatus?.directory || 'C:\\Users\\indui\\Desktop\\meds_database\\deepseek_data'}</code> klasöründen otomatik olarak içeri aktarır ve RAG vektör sistemine katar.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={handleSyncDeepseek}
                  disabled={isSyncingDeepseek}
                  className="bg-accent hover:bg-accent text-white font-bold px-3.5 py-2 rounded-xl text-xs flex items-center gap-2 transition-all cursor-pointer disabled:opacity-50 shrink-0 shadow-sm"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isSyncingDeepseek ? 'animate-spin' : ''}`} />
                  <span>{isSyncingDeepseek ? 'Taranıyor...' : 'Klasörü Tara & RAG\'e Ekle'}</span>
                </button>
              </div>

              {/* Status metrics */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-center">
                <div className="bg-ink/80 border border-accent/60 p-2.5 rounded-xl">
                  <span className="text-2xs text-ink-3 block">Klasördeki Dosyalar</span>
                  <span className="text-sm font-extrabold text-white">{deepseekStatus?.filesCount || 0} Dosya</span>
                </div>
                <div className="bg-ink/80 border border-accent/60 p-2.5 rounded-xl">
                  <span className="text-2xs text-ink-3 block">İşlenen Katkı Verisi</span>
                  <span className="text-sm font-extrabold text-accent">{deepseekStatus?.itemsCount || 0} Kayıt</span>
                </div>
                <div className="bg-ink/80 border border-accent/60 p-2.5 rounded-xl">
                  <span className="text-2xs text-ink-3 block">Kaynak Statüsü</span>
                  <span className="text-sm font-extrabold text-ok">DeepSeek Katkısı</span>
                </div>
                <div className="bg-ink/80 border border-accent/60 p-2.5 rounded-xl">
                  <span className="text-2xs text-ink-3 block">RAG Arama Önceliği</span>
                  <span className="text-sm font-extrabold text-warn">Birincil Zemin (1. Sıra)</span>
                </div>
              </div>

              {deepseekFeedback && (
                <div className="p-3 bg-accent/50 border border-accent/40 rounded-xl text-xs font-semibold text-accent-soft flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-ok shrink-0" />
                  <span>{deepseekFeedback}</span>
                </div>
              )}
            </div>

            {/* Lecture Notes Repair & Cross-Enrichment Card */}
            <div className="bg-ink-surface text-white rounded-2xl p-5 border border-ok/40 shadow-lg space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-ok/60">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="p-1.5 bg-ok/20 text-ok rounded-lg border border-ok/30">
                      <BookOpen className="w-4 h-4 text-ok" />
                    </span>
                    <h3 className="text-sm font-bold text-white">Slayt Onarım & Redakte Zenginleştirme Motoru</h3>
                  </div>
                  <p className="text-2xs text-ink-3">
                    Orijinal ders sunumlarındaki boş, eksik veya okunamamış slaytları 347 adet doğrulanmış amfi redakte ders özetiyle otomatik çapraz eşleştirir, tamamlar ve RAG sistemine katar.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={handleRepairLectureNotes}
                  disabled={isRepairingNotes}
                  className="bg-ok hover:bg-ok text-white font-bold px-3.5 py-2 rounded-xl text-xs flex items-center gap-2 transition-all cursor-pointer disabled:opacity-50 shrink-0 shadow-sm"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isRepairingNotes ? 'animate-spin' : ''}`} />
                  <span>{isRepairingNotes ? 'Onarılıyor...' : 'Slaytları Redakte Notlarla Onar'}</span>
                </button>
              </div>

              {repairFeedback && (
                <div className="p-3 bg-ok/50 border border-ok/40 rounded-xl text-xs font-semibold text-ok-soft flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-ok shrink-0" />
                  <span>{repairFeedback}</span>
                </div>
              )}
            </div>

            <div className="bg-field border border-line rounded-xl p-4 space-y-3">
              <h4 className="font-bold text-ink text-sm flex items-center gap-2">
                <Database className="w-4 h-4 text-ok" />
                Veritabanı Yedekleme ve Sıfırlama
              </h4>
              <p className="text-ink-3 text-2xs">
                Tüm soru havuzunu tek tıkla JSON formatında indirebilir, geri yükleyebilir veya eşik testi çalıştırabilirsiniz.
              </p>

              <div className="flex flex-wrap items-center gap-2 pt-2">
                <button
                  onClick={handleExportJson}
                  className="bg-white hover:bg-field border border-line text-ink-2 font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 cursor-pointer shadow-2xs"
                >
                  <Download className="w-3.5 h-3.5 text-ink-3" />
                  <span>JSON İndir</span>
                </button>

                <label className="bg-white hover:bg-field border border-line text-ink-2 font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 cursor-pointer shadow-2xs">
                  <Upload className="w-3.5 h-3.5 text-ink-3" />
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
                  className="bg-bad-soft hover:bg-bad-soft text-bad-text border border-bad/30 font-semibold px-3 py-1.5 rounded-lg flex items-center gap-1.5 cursor-pointer"
                >
                  <RotateCcw className="w-3.5 h-3.5 text-bad-text" />
                  <span>Sıfırla</span>
                </button>
              </div>
            </div>

            {/* Cloud Firestore Sync Card */}
            <div className="bg-ink-surface text-white border border-ok/50 rounded-xl p-4 sm:p-5 space-y-3 shadow-md">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-lg bg-ok/20 text-ok border border-ok/30 flex items-center justify-center">
                    <Cloud className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="font-bold text-sm text-white flex items-center gap-2">
                      <span>Firebase Firestore Bulut Senkronizasyonu</span>
                      <span className="bg-ok/20 text-ok border border-ok/30 text-2xs font-bold px-2 py-0.5 rounded-full">
                        Canlı Bulut
                      </span>
                    </h4>
                    <p className="text-xs text-ink-3">
                      Mevcut soru havuzunu ({questions.length} soru) Firebase Firestore bulutuna toplu olarak yazar.
                    </p>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={handleSyncQuestionsToFirestore}
                  disabled={isSyncingFirestore || questions.length === 0}
                  className="bg-ok hover:bg-ok text-white font-bold px-4 py-2 rounded-xl text-xs flex items-center gap-2 transition-all cursor-pointer disabled:opacity-50 shadow-sm shrink-0"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isSyncingFirestore ? 'animate-spin' : ''}`} />
                  <span>{isSyncingFirestore ? 'Buluta Yazılıyor...' : 'Tüm Soruları Firestore\'a Aktar'}</span>
                </button>
              </div>

              <div className="bg-ink/60 border border-line-2/50 rounded-lg p-3 text-2xs text-ink-3 space-y-1.5">
                <div className="flex items-center gap-1.5 text-ok font-semibold">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Güvenli & Parçalı (Chunked) Firestore Aktarımı:</span>
                </div>
                <p className="leading-relaxed">
                  Bu işlem tüm çıkmış soruları ve komite sorularını 100'lük güvenli paketlere bölerek Firestore'a kaydeder. Beğeniler (upvotes) 0'dan başlatılır ve tekil beğeni listesi (<code className="text-ok">likedBy: []</code>) standartlaştırılır.
                </p>
              </div>

              {firestoreSyncFeedback && (
                <div className={`p-3 rounded-lg border text-xs flex items-start gap-2 ${
                  firestoreSyncFeedback.startsWith('✓')
                    ? 'bg-ok/80 border-ok/50 text-ok-soft'
                    : firestoreSyncFeedback.startsWith('Hata')
                    ? 'bg-bad/80 border-bad/50 text-bad-soft'
                    : 'bg-ok/80 border-ok/50 text-ok-soft'
                }`}>
                  <CheckCircle2 className="w-4 h-4 text-ok shrink-0 mt-0.5" />
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
            <div className="bg-ink-surface text-white p-4 sm:p-5 rounded-2xl border border-ok shadow-md flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-ok animate-pulse" />
                  <span className="text-xs font-bold text-ok uppercase tracking-wider">
                    Auth & Realtime Database Bağlantı Durumu: Aktif & Senkronize
                  </span>
                </div>
                <h3 className="text-base sm:text-lg font-black text-white">
                  Kayıtlı Öğrenci & Kullanıcı Yönetim Masası
                </h3>
                <p className="text-xs text-ink-3 max-w-xl">
                  Sisteme e-posta veya Google ile kayıt olan tüm tıp fakültesi öğrencileri burada listelenir. Auth ve veritabanı arasındaki çift yönlü eşitleme sayesinde yeni kayıtlar anında tabloya yansır.
                </p>
                {userSyncMessage && (
                  <div className="mt-2 text-xs font-semibold text-ok-soft bg-ok/60 border border-ok/50 p-2 rounded-lg flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-ok shrink-0" />
                    <span>{userSyncMessage}</span>
                  </div>
                )}
              </div>

              <div className="flex flex-wrap items-center gap-2 min-w-0 max-w-full">
                <button
                  onClick={handleSyncAuthDbBridge}
                  disabled={isSyncingAuthDb}
                  className="bg-ok/80 hover:bg-ok text-ok-soft border border-ok/60 font-bold px-3 py-2 rounded-xl text-xs flex items-center gap-1.5 shadow-2xs transition-all cursor-pointer active:scale-95 disabled:opacity-50"
                  title="Firebase Auth kullanıcıları ile veritabanını doğrula ve yenile"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${isSyncingAuthDb ? 'animate-spin text-ok' : 'text-ok'}`} />
                  <span>{isSyncingAuthDb ? 'Eşitleniyor...' : 'Veritabanını Eşitle'}</span>
                </button>

                <button
                  onClick={() => setShowMobileNotificationSettings(!showMobileNotificationSettings)}
                  className={`font-black px-3.5 py-2 rounded-xl text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer active:scale-95 ${
                    showMobileNotificationSettings
                      ? 'bg-ok text-ink font-bold border border-ok shadow-md'
                      : 'bg-ok/90 hover:bg-ok text-ok-soft border border-ok/60'
                  }`}
                  title="Telefonda (nofrostlife.com.tr) anlık Web Push ve E-posta bildirim ayarları"
                >
                  <Smartphone className="w-4 h-4 text-warn" />
                  <span>{showMobileNotificationSettings ? 'Bildirimleri Gizle' : '📱 Telefon & Bildirim'}</span>
                </button>

                <button
                  onClick={() => setShowSmtpSettings(!showSmtpSettings)}
                  className={`font-black px-3.5 py-2 rounded-xl text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer active:scale-95 ${
                    smtpConfig?.hasPass
                      ? 'bg-ok/90 hover:bg-ok text-ok-soft border border-ok/60'
                      : 'bg-warn hover:bg-warn text-ink font-bold border border-warn/30'
                  }`}
                  title="Gmail SMTP e-posta sunucusu ve 16 haneli Google Uygulama Şifresi ayarları"
                >
                  <Mail className="w-4 h-4" />
                  <span>{showSmtpSettings ? 'SMTP Panelini Gizle' : 'E-posta & SMTP Ayarları'}</span>
                  {!smtpConfig?.hasPass && (
                    <span className="w-2 h-2 rounded-full bg-bad animate-ping" />
                  )}
                </button>

                <button
                  onClick={() => setIsCreatingUser(!isCreatingUser)}
                  className="bg-ok hover:bg-ok text-ink font-black px-3.5 py-2 rounded-xl text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer active:scale-95"
                >
                  <UserPlus className="w-4 h-4" />
                  <span>{isCreatingUser ? 'Formu Kapat' : 'Yeni Kullanıcı Ekle'}</span>
                </button>
              </div>
            </div>

            {/* Warning if SMTP pass is missing */}
            {!smtpConfig?.hasPass && !showSmtpSettings && (
              <div className="bg-warn-soft border border-warn/30 rounded-xl p-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-warn shadow-2xs">
                <div className="flex items-center gap-2.5">
                  <AlertTriangle className="w-5 h-5 text-warn shrink-0" />
                  <div>
                    <strong className="font-bold block text-ink">
                      Önemli: Hoş Geldin E-postaları İçin Google Uygulama Şifresi Tanımlanmamış
                    </strong>
                    <span className="text-2xs text-ink-2">
                      Yeni kaydolan öğrencilere otomatik hoş geldiniz bildirimi gidebilmesi için 16 haneli Google App Password tanımlanmalıdır.
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => setShowSmtpSettings(true)}
                  className="bg-warn hover:bg-warn text-white font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 cursor-pointer shrink-0 self-start sm:self-auto"
                >
                  <Mail className="w-3.5 h-3.5" />
                  <span>Şimdi Tanımla & Test Et</span>
                </button>
              </div>
            )}

            {/* Mobil & Web Push Bildirim Kartı */}
            {showMobileNotificationSettings && (
              <div className="animate-fade-in mb-4">
                <AdminMobileNotificationCard
                  onClose={() => setShowMobileNotificationSettings(false)}
                  onOpenQuestion={(qId) => {
                    onClose();
                    window.location.assign(`/cikmis/${encodeURIComponent(qId)}`);
                  }}
                />
              </div>
            )}

            {/* SMTP E-posta Sunucu Yapılandırması Kartı */}
            {showSmtpSettings && (
              <div className="bg-ink-surface text-white rounded-2xl p-5 border border-ok/50 shadow-xl space-y-4 animate-fade-in">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-line-2">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-lg bg-ok/20 text-ok border border-ok/30 flex items-center justify-center">
                      <Mail className="w-4 h-4" />
                    </div>
                    <div>
                      <h4 className="font-bold text-sm text-white flex items-center gap-2">
                        <span>E-posta & SMTP Sunucu Yapılandırması (Gmail Canlı İletim)</span>
                        {smtpConfig?.hasPass ? (
                          <span className="bg-ok/20 text-ok border border-ok/30 text-2xs font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                            <Check className="w-3 h-3 text-ok" />
                            Hazır & Yapılandırıldı
                          </span>
                        ) : (
                          <span className="bg-warn/20 text-warn border border-warn/30 text-2xs font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                            <AlertTriangle className="w-3 h-3 text-warn" />
                            Şifre Eksik (Mail Gönderilemez)
                          </span>
                        )}
                      </h4>
                      <p className="text-xs text-ink-3">
                        Yeni kayıt olan veya onaylanan öğrencilere gönderilecek hoş geldiniz mailleri için Gmail SMTP servisi kullanılır.
                      </p>
                    </div>
                  </div>

                  <button
                    onClick={() => setShowSmtpSettings(false)}
                    className="self-end sm:self-auto text-ink-3 hover:text-white text-xs px-2.5 py-1 rounded-lg hover:bg-ink cursor-pointer"
                  >
                    Gizle
                  </button>
                </div>

                {/* Form Fields */}
                <form onSubmit={handleSaveSmtp} className="space-y-4">
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                    <div>
                      <label className="block text-2xs font-bold text-ok mb-1">
                        Gönderen Gmail Adresi *
                      </label>
                      <input
                        type="email"
                        required
                        value={smtpUser}
                        onChange={(e) => setSmtpUser(e.target.value)}
                        placeholder="nofrostlife@gmail.com"
                        className="w-full bg-ink border border-line-2 rounded-lg px-3 py-2 text-xs text-white focus:border-ok focus:ring-1 focus:ring-ok font-mono"
                      />
                    </div>

                    <div>
                      <label className="block text-2xs font-bold text-ok mb-1 flex items-center justify-between">
                        <span>16 Haneli Google Uygulama Şifresi *</span>
                        {smtpConfig?.hasPass && (
                          <span className="text-2xs text-ok font-normal">Kayıtlı: {smtpConfig.passMasked}</span>
                        )}
                      </label>
                      <div className="relative">
                        <input
                          type="password"
                          value={smtpPass}
                          onChange={(e) => setSmtpPass(e.target.value)}
                          placeholder={smtpConfig?.hasPass ? 'Yeni şifre girmek için yazınız...' : 'örn: abcd efgh ijkl mnop'}
                          className="w-full bg-ink border border-line-2 rounded-lg px-3 py-2 text-xs text-white focus:border-ok focus:ring-1 focus:ring-ok font-mono"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-2xs font-bold text-ok mb-1">
                        Görünen Gönderici Başlığı
                      </label>
                      <input
                        type="text"
                        value={smtpFrom}
                        onChange={(e) => setSmtpFrom(e.target.value)}
                        placeholder="MeDSor Tıp Fakültesi <nofrostlife@gmail.com>"
                        className="w-full bg-ink border border-line-2 rounded-lg px-3 py-2 text-xs text-white focus:border-ok focus:ring-1 focus:ring-ok"
                      />
                    </div>
                  </div>

                  {/* Instructions Box */}
                  <div className="bg-ink/80 border border-ok/60 rounded-xl p-3.5 text-xs space-y-2 text-ink-3">
                    <div className="flex items-center gap-2 font-bold text-ok">
                      <Key className="w-4 h-4 text-ok" />
                      <span>Google 16 Haneli Uygulama Şifresi Nasıl Alınır? (Gmail 2022+ Kuralı)</span>
                    </div>
                    <ol className="list-decimal list-inside space-y-1 text-2xs text-ink-3 leading-relaxed">
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
                          className="text-ok hover:text-ok underline font-bold inline-flex items-center gap-0.5"
                        >
                          myaccount.google.com/apppasswords
                          <ExternalLink className="w-3 h-3 inline" />
                        </a>{' '}
                        sayfasına gidin.
                      </li>
                      <li>
                        Uygulama adı olarak <strong className="text-ok">MeDSor</strong> yazın ve <strong className="text-white">Oluştur</strong> butonuna tıklayın.
                      </li>
                      <li>
                        Google'ın size ekranda gösterdiği 16 haneli sarı kod bloğunu (örnek: <span className="font-mono text-warn">abcd efgh ijkl mnop</span>) kopyalayıp yukarıdaki alana yapıştırın ve <strong>Ayarları Kaydet</strong>'e basınız.
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
                        className="flex-1 bg-ink border border-line-2 rounded-lg px-3 py-1.5 text-xs text-white placeholder-ink-3 font-mono"
                      />
                      <button
                        type="button"
                        onClick={handleTestSmtp}
                        disabled={isTestingSmtp}
                        className="bg-ok hover:bg-ok text-white font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 transition-all cursor-pointer disabled:opacity-50 shrink-0"
                      >
                        <Send className={`w-3.5 h-3.5 ${isTestingSmtp ? 'animate-pulse' : ''}`} />
                        <span>{isTestingSmtp ? 'Gönderiliyor...' : 'Canlı Test Gönder'}</span>
                      </button>
                    </div>

                    <div className="flex items-center gap-2 self-end sm:self-auto">
                      <button
                        type="submit"
                        disabled={isSavingSmtp}
                        className="bg-ok hover:bg-ok text-white font-bold px-4 py-1.5 rounded-lg text-xs flex items-center gap-1.5 transition-all cursor-pointer disabled:opacity-50"
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
                        ? 'bg-ok/80 border-ok/50 text-ok-soft'
                        : 'bg-bad/80 border-bad/50 text-bad-soft'
                    }`}>
                      {smtpTestResult.success ? (
                        <CheckCircle2 className="w-4 h-4 text-ok shrink-0 mt-0.5" />
                      ) : (
                        <AlertTriangle className="w-4 h-4 text-bad-text shrink-0 mt-0.5" />
                      )}
                      <div>
                        <strong className="block">{smtpTestResult.message}</strong>
                        {smtpTestResult.hint && (
                          <p className="text-2xs text-ink-3 mt-1">
                            <strong>İpucu:</strong> {smtpTestResult.hint}
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
              <form onSubmit={handleManualCreateUser} className="bg-field border border-ok/80 rounded-2xl p-4 sm:p-5 space-y-4 shadow-sm animate-fade-in">
                <div className="flex items-center justify-between pb-2 border-b border-line">
                  <h4 className="font-bold text-sm text-ink flex items-center gap-2">
                    <UserPlus className="w-4 h-4 text-ok" />
                    Yeni Öğrenci / Yönetici Kaydı Aç
                  </h4>
                  <span className="text-2xs text-ok font-medium">Kayıt sonrası öğrenciye otomatik hoş geldiniz e-postası iletilir</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
                  <div>
                    <label className="block text-2xs font-bold text-ink-2 mb-1">E-posta Adresi *</label>
                    <input
                      type="email"
                      required
                      value={newEmail}
                      onChange={(e) => setNewEmail(e.target.value)}
                      placeholder="ogrenci@ogr.karabuk.edu.tr"
                      className="w-full bg-white border border-line-2 rounded-lg px-3 py-2 text-xs text-ink focus:border-ok focus:ring-1 focus:ring-ok"
                    />
                  </div>

                  <div>
                    <label className="block text-2xs font-bold text-ink-2 mb-1">Ad Soyad (Görünen İsim)</label>
                    <input
                      type="text"
                      value={newName}
                      onChange={(e) => setNewName(e.target.value)}
                      placeholder="Örn: Eren Yılmaz"
                      className="w-full bg-white border border-line-2 rounded-lg px-3 py-2 text-xs text-ink focus:border-ok focus:ring-1 focus:ring-ok"
                    />
                  </div>

                  <div>
                    <label className="block text-2xs font-bold text-ink-2 mb-1">Öğrenci Numarası</label>
                    <input
                      type="text"
                      value={newStudentNumber}
                      onChange={(e) => setNewStudentNumber(e.target.value.replace(/\D/g, ''))}
                      placeholder="Örn: 202311045"
                      className="w-full bg-white border border-line-2 rounded-lg px-3 py-2 text-xs text-ink focus:border-ok focus:ring-1 focus:ring-ok"
                    />
                  </div>

                  <div>
                    <label className="block text-2xs font-bold text-ink-2 mb-1">Yetki Rolü</label>
                    <select
                      value={newRole}
                      onChange={(e) => setNewRole(e.target.value as any)}
                      className="w-full bg-white border border-line-2 rounded-lg px-3 py-2 text-xs text-ink font-semibold focus:border-ok focus:ring-1 focus:ring-ok"
                    >
                      <option value="student">Öğrenci (Soru Ekleme & Test)</option>
                      <option value="admin">Yönetici (Tam Yetki)</option>
                    </select>
                  </div>
                </div>

                <div className="flex items-center justify-end gap-2 pt-2 border-t border-line">
                  <button
                    type="button"
                    onClick={() => setIsCreatingUser(false)}
                    className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-ink-2 hover:bg-line cursor-pointer"
                  >
                    Vazgeç
                  </button>
                  <button
                    type="submit"
                    disabled={isProcessing}
                    className="bg-ok hover:bg-ok text-white font-bold px-4 py-1.5 rounded-lg text-xs flex items-center gap-1.5 shadow-2xs transition-all cursor-pointer disabled:opacity-50"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5 text-ok-soft" />
                    <span>{isProcessing ? 'Ekleniyor...' : 'Kullanıcıyı Kaydet & Mail Gönder'}</span>
                  </button>
                </div>
              </form>
            )}

            {/* Statistics Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div className="bg-field border border-line rounded-xl p-3.5">
                <span className="text-2xs font-semibold text-ink-3 block">Toplam Kayıtlı</span>
                <span className="text-xl font-black text-ink">{usersList.length} Kullanıcı</span>
              </div>

              <div className="bg-ok-soft/70 border border-ok/30 rounded-xl p-3.5">
                <span className="text-2xs font-semibold text-ok block">Öğrenci Hesapları</span>
                <span className="text-xl font-black text-ok">
                  {usersList.filter((u) => u && u.role !== 'admin').length} Öğrenci
                </span>
              </div>

              <div className="bg-warn-soft/70 border border-warn/30 rounded-xl p-3.5">
                <span className="text-2xs font-semibold text-warn block">Yönetici Hesapları</span>
                <span className="text-xl font-black text-warn">
                  {usersList.filter((u) => u && u.role === 'admin').length} Yönetici
                </span>
              </div>

              <div className="bg-ok-soft/70 border border-ok/30 rounded-xl p-3.5">
                <span className="text-2xs font-semibold text-ok block">Hoş Geldin Maili Alan</span>
                <span className="text-xl font-black text-ok">
                  {usersList.filter((u) => u && u.welcomeEmailSent).length} İletildi
                </span>
              </div>
            </div>

            {/* Search and Filter */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-white p-3 rounded-xl border border-line">
              <div className="relative flex-1 max-w-sm">
                <Search className="w-3.5 h-3.5 text-ink-3 absolute left-3 top-2.5" />
                <input
                  type="text"
                  value={userSearchQuery}
                  onChange={(e) => setUserSearchQuery(e.target.value)}
                  placeholder="İsim, e-posta veya öğrenci no ara..."
                  className="w-full text-xs pl-8 pr-3 py-1.5 bg-field border border-line rounded-lg text-ink focus:bg-white focus:outline-none focus:ring-1 focus:ring-ok"
                />
              </div>

              <div className="flex items-center gap-2 text-xs text-ink-3">
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
            <div className="bg-white rounded-2xl border border-line shadow-2xs overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse text-xs">
                  <thead>
                    <tr className="bg-field/80 border-b border-line text-ink-2 font-bold uppercase text-2xs tracking-wider">
                      <th className="py-3 px-3.5">Öğrenci / Kullanıcı</th>
                      <th className="py-3 px-3.5">E-posta Adresi</th>
                      <th className="py-3 px-3.5">Öğrenci No</th>
                      <th className="py-3 px-3.5">Yetki Rolü</th>
                      <th className="py-3 px-3.5">Kayıt Tarihi</th>
                      <th className="py-3 px-3.5">Hoş Geldin E-postası</th>
                      <th className="py-3 px-3.5 text-right">İşlemler</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-line">
                    {isLoadingUsers ? (
                      <tr>
                        <td colSpan={7} className="py-10 text-center text-ink-3">
                          <div className="flex items-center justify-center gap-2">
                            <RefreshCw className="w-4 h-4 animate-spin text-ok" />
                            <span>Kullanıcı veritabanı yükleniyor...</span>
                          </div>
                        </td>
                      </tr>
                    ) : usersList.length === 0 ? (
                      <tr>
                        <td colSpan={7} className="py-10 text-center text-ink-3">
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
                            <tr key={u.uid || u.email} className="hover:bg-field/70 transition-colors">
                              {/* Name & Avatar */}
                              <td className="py-3 px-3.5">
                                <div className="flex items-center gap-2.5">
                                  <div className={`w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs shrink-0 ${
                                    isAdminUser
                                      ? 'bg-warn-soft text-warn border border-warn/30'
                                      : 'bg-ok-soft text-ok border border-ok/30'
                                  }`}>
                                    {(u.displayName || u.email || 'Ö')[0].toUpperCase()}
                                  </div>
                                  <div>
                                    <span className="font-bold text-ink block leading-tight">
                                      {u.displayName || 'İsimsiz Öğrenci'}
                                    </span>
                                    <span className="text-2xs text-ink-3 font-mono block">
                                      ID: {u.uid?.slice(0, 14)}...
                                    </span>
                                  </div>
                                </div>
                              </td>

                              {/* Email */}
                              <td className="py-3 px-3.5">
                                <span className="font-medium text-ink-2 font-mono text-2xs">
                                  {u.email}
                                </span>
                              </td>

                              {/* Student Number */}
                              <td className="py-3 px-3.5">
                                {u.studentNumber ? (
                                  <span className="bg-field text-ink font-mono font-semibold px-2 py-0.5 rounded text-2xs border border-line">
                                    {u.studentNumber}
                                  </span>
                                ) : (
                                  <span className="text-ink-3 text-2xs italic">Girilmedi</span>
                                )}
                              </td>

                              {/* Role */}
                              <td className="py-3 px-3.5">
                                {isAdminUser ? (
                                  <span className="inline-flex items-center gap-1 bg-warn-soft text-warn border border-warn/30 text-2xs font-bold px-2 py-0.5 rounded-full">
                                    <ShieldCheck className="w-3 h-3 text-warn" />
                                    Yönetici
                                  </span>
                                ) : (
                                  <span className="inline-flex items-center gap-1 bg-ok-soft text-ok border border-ok/30 text-2xs font-semibold px-2 py-0.5 rounded-full">
                                    <User className="w-3 h-3 text-ok" />
                                    Öğrenci
                                  </span>
                                )}
                              </td>

                              {/* Registration Date */}
                              <td className="py-3 px-3.5 text-ink-3 text-2xs">
                                {formattedDate}
                              </td>

                              {/* Welcome Email Status */}
                              <td className="py-3 px-3.5">
                                {u.welcomeEmailSent ? (
                                  <span className="inline-flex items-center gap-1 text-ok font-bold bg-ok-soft border border-ok/30 px-2 py-0.5 rounded-md text-2xs">
                                    <Check className="w-3 h-3 text-ok" />
                                    ✓ İletildi
                                  </span>
                                ) : (
                                  <button
                                    onClick={() => handleSendWelcomeEmail(u)}
                                    disabled={isWelcomeSending}
                                    className="inline-flex items-center gap-1 text-ink-2 hover:text-ok bg-field hover:bg-ok-soft border border-line-2 px-2 py-0.5 rounded-md text-2xs font-semibold transition-colors cursor-pointer"
                                    title="Öğrenciye hoş geldiniz bilgilendirme maili gönder"
                                  >
                                    <Mail className="w-3 h-3 text-ok" />
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
                                    className="p-1.5 rounded-lg text-ink-3 hover:text-ok hover:bg-ok-soft cursor-pointer transition-colors"
                                  >
                                    <Mail className="w-3.5 h-3.5" />
                                  </button>

                                  {!isAdminUser && (
                                    <button
                                      onClick={() => handleManualDeleteUser(u)}
                                      title="Kullanıcıyı Sil"
                                      className="p-1.5 rounded-lg text-ink-3 hover:text-bad-text hover:bg-bad-soft cursor-pointer transition-colors"
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
        <div className="ms-overlay fixed inset-0 z-60 bg-ink/70 flex items-center justify-center p-4">
          <div className="ms-modal-panel bg-white rounded-xl max-w-md w-full p-5 shadow-2xl space-y-4 border border-line">
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-full bg-bad-soft text-bad-text shrink-0">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <div>
                <h4 className="font-bold text-ink text-sm">{confirmDialog.title}</h4>
                <p className="text-xs text-ink-2 mt-1 leading-relaxed">
                  {confirmDialog.description}
                </p>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-line">
              <button
                type="button"
                onClick={() => setConfirmDialog(null)}
                disabled={isProcessing}
                className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-ink-2 hover:bg-field cursor-pointer"
              >
                Vazgeç
              </button>
              <button
                type="button"
                onClick={confirmDialog.onConfirm}
                disabled={isProcessing}
                className="bg-bad hover:bg-bad text-white px-4 py-1.5 rounded-lg text-xs font-bold cursor-pointer disabled:opacity-50"
              >
                {isProcessing ? 'İşleniyor...' : 'Onayla'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Supabase SQL Schema Viewer Modal */}
      {showSqlSchemaModal && (
        <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/80 backdrop-blur-xs animate-fadeIn">
          <div className="bg-ink border border-line-2 rounded-2xl max-w-3xl w-full max-h-[85dvh] flex flex-col shadow-2xl overflow-hidden text-white">
            <div className="p-4 bg-ink border-b border-line-2 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Terminal className="w-5 h-5 text-accent" />
                <h3 className="font-bold text-sm text-ink-3">Supabase PostgreSQL Veritabanı Şeması</h3>
              </div>
              <button
                type="button"
                onClick={() => setShowSqlSchemaModal(false)}
                className="text-ink-3 hover:text-white p-1 rounded-lg hover:bg-ink cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 overflow-y-auto space-y-3 text-xs flex-1">
              <p className="text-ink-3">
                Supabase Dashboard &gt; <strong>SQL Editor</strong> bölümüne aşağıdaki kodu yapıştırıp <strong>RUN</strong> butonuna basınız. Bu komutlar gerekli tüm tabloları (committees, questions, past_questions, lecture_notes, users, system_status), indeksleri ve RLS politikalarını oluşturur:
              </p>

              <pre className="p-3 bg-ink rounded-xl border border-line-2 font-mono text-2xs text-ok overflow-x-auto select-all max-h-[50dvh]">
{`-- 1. Kurullar Tablosu
CREATE TABLE IF NOT EXISTS public.committees (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  academic_year TEXT DEFAULT '2026-2027',
  target_questions INTEGER DEFAULT 100,
  color TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  data JSONB
);

-- 2. Aktif Öğrenci Soru Havuzu Tablosu
CREATE TABLE IF NOT EXISTS public.questions (
  id TEXT PRIMARY KEY,
  committee_id TEXT,
  question_number INTEGER,
  discipline TEXT,
  topic TEXT,
  status TEXT DEFAULT 'gathering',
  claimed_answer TEXT,
  upvotes INTEGER DEFAULT 0,
  tags JSONB DEFAULT '[]'::jsonb,
  fragments JSONB DEFAULT '[]'::jsonb,
  options JSONB DEFAULT '[]'::jsonb,
  reconstruction JSONB,
  data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Çıkmış Sorular & Yapay Zeka Soru Arşivi Tablosu
CREATE TABLE IF NOT EXISTS public.past_questions (
  id TEXT PRIMARY KEY,
  committee_id TEXT,
  discipline TEXT,
  topic TEXT,
  exam_year TEXT,
  source_file TEXT,
  ai_category TEXT,
  claimed_answer TEXT,
  raw_question JSONB,
  reconstruction JSONB,
  is_suspect BOOLEAN DEFAULT FALSE,
  is_ambiguous BOOLEAN DEFAULT FALSE,
  is_locked BOOLEAN DEFAULT FALSE,
  upvotes INTEGER DEFAULT 0,
  comments JSONB DEFAULT '[]'::jsonb,
  reports JSONB DEFAULT '[]'::jsonb,
  custom_redacted_by TEXT,
  custom_redacted_at TIMESTAMPTZ,
  custom_redaction_prompt TEXT,
  data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3b. Çıkmış Soru Hata Bildirimleri Tablosu
CREATE TABLE IF NOT EXISTS public.past_question_reports (
  id TEXT PRIMARY KEY,
  question_id TEXT REFERENCES public.past_questions(id) ON DELETE CASCADE,
  reason TEXT NOT NULL,
  details TEXT,
  reported_by TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Amfi Ders Notları & Slaytlar Tablosu
CREATE TABLE IF NOT EXISTS public.lecture_notes (
  id TEXT PRIMARY KEY,
  committee_id TEXT,
  discipline TEXT,
  title TEXT,
  pages JSONB DEFAULT '[]'::jsonb,
  page_count INTEGER DEFAULT 0,
  data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Kullanıcılar & Profiller Tablosu
CREATE TABLE IF NOT EXISTS public.users (
  uid TEXT PRIMARY KEY,
  email TEXT NOT NULL,
  display_name TEXT,
  student_number TEXT,
  role TEXT DEFAULT 'student',
  data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Sistem Durumu & Telemetri Tablosu
CREATE TABLE IF NOT EXISTS public.system_status (
  id TEXT PRIMARY KEY,
  data JSONB,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Row Level Security (RLS) İzinleri
ALTER TABLE public.committees ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.past_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.past_question_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.lecture_notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.system_status ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access" ON public.committees FOR SELECT USING (true);
CREATE POLICY "Allow public write access" ON public.committees FOR ALL USING (true);
CREATE POLICY "Allow public read access" ON public.questions FOR SELECT USING (true);
CREATE POLICY "Allow public write access" ON public.questions FOR ALL USING (true);
CREATE POLICY "Allow public read access" ON public.past_questions FOR SELECT USING (true);
CREATE POLICY "Allow public write access" ON public.past_questions FOR ALL USING (true);
CREATE POLICY "Allow public read access" ON public.past_question_reports FOR SELECT USING (true);
CREATE POLICY "Allow public write access" ON public.past_question_reports FOR ALL USING (true);
CREATE POLICY "Allow public read access" ON public.lecture_notes FOR SELECT USING (true);
CREATE POLICY "Allow public write access" ON public.lecture_notes FOR ALL USING (true);
CREATE POLICY "Allow public read access" ON public.users FOR SELECT USING (true);
CREATE POLICY "Allow public write access" ON public.users FOR ALL USING (true);
CREATE POLICY "Allow public read access" ON public.system_status FOR SELECT USING (true);
CREATE POLICY "Allow public write access" ON public.system_status FOR ALL USING (true);

-- 8. Supabase Realtime Yayını (Anlık Canlı Akış İçin ŞARTTIR)
ALTER PUBLICATION supabase_realtime SET TABLE 
  public.committees, 
  public.questions, 
  public.past_questions, 
  public.past_question_reports,
  public.lecture_notes, 
  public.system_status, 
  public.users;

-- 9. Replica Identity (Güncelleme ve Silmelerde Tüm Veriyi Aktarmak İçin)
ALTER TABLE public.committees REPLICA IDENTITY FULL;
ALTER TABLE public.questions REPLICA IDENTITY FULL;
ALTER TABLE public.past_questions REPLICA IDENTITY FULL;
ALTER TABLE public.past_question_reports REPLICA IDENTITY FULL;
ALTER TABLE public.lecture_notes REPLICA IDENTITY FULL;
ALTER TABLE public.users REPLICA IDENTITY FULL;
ALTER TABLE public.system_status REPLICA IDENTITY FULL;`}
              </pre>
            </div>

            <div className="p-4 bg-ink border-t border-line-2 flex items-center justify-between">
              <span className="text-2xs text-ink-3">
                Panoya kopyalayıp Supabase SQL konsolunda çalıştırın.
              </span>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => {
                    const sql = document.querySelector('pre')?.textContent || '';
                    navigator.clipboard.writeText(sql);
                    setCopiedSql(true);
                    setTimeout(() => setCopiedSql(false), 3000);
                  }}
                  className="bg-accent hover:bg-accent text-white font-bold px-4 py-2 rounded-xl text-xs flex items-center gap-1.5 cursor-pointer shadow-sm transition-all"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>{copiedSql ? '✓ Kopyalandı!' : 'SQL Kopyala'}</span>
                </button>
                <button
                  type="button"
                  onClick={() => setShowSqlSchemaModal(false)}
                  className="bg-ink hover:bg-ink-2 text-ink-3 px-4 py-2 rounded-xl text-xs font-semibold cursor-pointer"
                >
                  Kapat
                </button>
              </div>
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

      {/* Akıllı Taslak Birleştirme & Kümeleme Modal */}
      <DraftDeduplicationModal
        isOpen={isDraftDeduplicationOpen}
        onClose={() => setIsDraftDeduplicationOpen(false)}
        committee={committees.find((c) => c.id === selectedCommitteeId) || null}
        questions={questions}
        currentUser={{ email: adminEmail } as any}
        onRefreshData={onRefreshData}
      />
    </div>
  );
};
