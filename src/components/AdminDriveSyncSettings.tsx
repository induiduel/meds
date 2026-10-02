import React, { useState, useEffect, useRef } from 'react';
import {
  Cloud,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  Search,
  FileText,
  Layers,
  Settings,
  Terminal,
  ExternalLink,
  FolderOpen,
  Clock,
  Bell,
  Play,
  Square,
  Copy,
  Sparkles,
  ChevronDown,
  ChevronUp,
  Check,
  FolderSync,
  HelpCircle,
} from 'lucide-react';
import {
  ApiService,
  DriveSyncSettings,
  DriveCheckResult,
  AdminScriptJob
} from '../services/api';

interface AdminDriveSyncSettingsProps {
  adminEmail: string;
  onRefreshData?: () => Promise<void>;
  selectedCommitteeId?: string;
}

export const AdminDriveSyncSettings: React.FC<AdminDriveSyncSettingsProps> = ({
  adminEmail,
  onRefreshData,
  selectedCommitteeId = 'donem3-kurul1',
}) => {
  // Settings State
  const [settings, setSettings] = useState<DriveSyncSettings>({
    autoSyncEnabled: false,
    syncInterval: '18:00',
    preferredScope: 'all',
    customFolderId: '',
    notifyOnUpdate: true,
    lastCheckedAt: null,
    lastSyncedAt: null,
    lastSyncedSummary: 'Henüz senkronizasyon yapılmadı',
  });
  const [isSavingSettings, setIsSavingSettings] = useState(false);
  const [settingsSavedMessage, setSettingsSavedMessage] = useState<string | null>(null);

  // Check / Dry-Run State
  const [isChecking, setIsChecking] = useState(false);
  const [checkResult, setCheckResult] = useState<DriveCheckResult | null>(null);
  const [checkFeedback, setCheckFeedback] = useState<string | null>(null);
  const [showFileList, setShowFileList] = useState(false);

  // Sync / Execution State
  const [isSyncing, setIsSyncing] = useState(false);
  const [activeJobId, setActiveJobId] = useState<string | null>(null);
  const [activeJob, setActiveJob] = useState<AdminScriptJob | null>(null);
  const [jobLogs, setJobLogs] = useState<string[]>([]);
  const [syncFeedback, setSyncFeedback] = useState<string | null>(null);
  const [forceReSync, setForceReSync] = useState(false);

  // Terminal & UI
  const [isTerminalOpen, setIsTerminalOpen] = useState(false);
  const [autoScroll, setAutoScroll] = useState(true);
  const [copiedLogs, setCopiedLogs] = useState(false);
  const logsEndRef = useRef<HTMLDivElement>(null);
  const pollingRef = useRef<any>(null);

  // Load settings on mount
  useEffect(() => {
    loadSettings();
    loadLatestCheckResult();
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, []);

  // Auto-scroll terminal
  useEffect(() => {
    if (autoScroll && logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [jobLogs, autoScroll]);

  const loadSettings = async () => {
    try {
      const res = await ApiService.getDriveSyncSettings(adminEmail);
      if (res.success && res.settings) {
        setSettings(res.settings);
      }
    } catch (_) {}
  };

  const loadLatestCheckResult = async () => {
    try {
      const res = await ApiService.getDriveCheckResult(adminEmail);
      if (res.success && res.result) {
        setCheckResult(res.result);
      }
    } catch (_) {}
  };

  // Save Settings Handler
  const handleSaveSettings = async () => {
    setIsSavingSettings(true);
    setSettingsSavedMessage(null);
    try {
      const res = await ApiService.saveDriveSyncSettings(settings, adminEmail);
      if (res.success) {
        setSettingsSavedMessage('✓ Ayarlar başarıyla kaydedildi.');
        setTimeout(() => setSettingsSavedMessage(null), 4000);
      } else {
        setSettingsSavedMessage('Hata: ' + res.message);
      }
    } catch (e: any) {
      setSettingsSavedMessage('Hata: ' + e.message);
    } finally {
      setIsSavingSettings(false);
    }
  };

  // 1. Dry-Run Check Handler (Değişiklikleri Denetle)
  const handleCheckDriveUpdates = async () => {
    setIsChecking(true);
    setCheckFeedback('Google Drive klasörleri taranıyor ve yerel arşivle karşılaştırılıyor...');
    try {
      const res = await ApiService.checkDriveUpdates({
        scope: settings.preferredScope,
        folderId: settings.preferredScope === 'custom' ? settings.customFolderId : undefined,
        adminEmail,
      });

      if (res.result) {
        setCheckResult(res.result);
        setShowFileList(res.result.hasUpdates);
      }

      setCheckFeedback(res.message);
      await loadSettings();
    } catch (e: any) {
      setCheckFeedback('Denetim hatası: ' + e.message);
    } finally {
      setIsChecking(false);
    }
  };

  // 2. Manual Sync Handler (Şimdi Manuel Güncelle)
  const handleTriggerSync = async (force: boolean = forceReSync) => {
    setIsSyncing(true);
    setIsTerminalOpen(true);
    setSyncFeedback('Google Drive senkronizasyonu başlatılıyor...');
    setJobLogs(['[Başlatılıyor] Google Drive manuel senkronizasyon motoru devrede...']);

    try {
      const res = await ApiService.triggerManualDriveSync({
        scope: settings.preferredScope,
        folderId: settings.preferredScope === 'custom' ? settings.customFolderId : undefined,
        force,
        adminEmail,
      });

      if (res.success && res.jobId) {
        setActiveJobId(res.jobId);
        startJobPolling(res.jobId);
        setSyncFeedback(`✓ Eşitleme süreci başlatıldı (Görev ID: ${res.jobId}). Konsoldan anlık izleniyor...`);
      } else {
        setSyncFeedback('Hata: ' + (res.message || 'Senkronizasyon başlatılamadı.'));
        setIsSyncing(false);
      }
    } catch (e: any) {
      setSyncFeedback('Hata: ' + e.message);
      setIsSyncing(false);
    }
  };

  // Poll Job Status
  const startJobPolling = (jobId: string) => {
    if (pollingRef.current) clearInterval(pollingRef.current);

    pollingRef.current = setInterval(async () => {
      try {
        const res = await ApiService.getScriptJobStatus(jobId);
        if (res.success && res.job) {
          setActiveJob(res.job);
          if (res.job.logs && res.job.logs.length > 0) {
            setJobLogs(res.job.logs);
          }

          if (res.job.status === 'completed') {
            clearInterval(pollingRef.current);
            setIsSyncing(false);
            setSyncFeedback('🎉 Tebrikler! Google Drive senkronizasyonu başarıyla tamamlandı. Veriler güncellendi.');
            if (onRefreshData) await onRefreshData();
            loadSettings();
            loadLatestCheckResult();
          } else if (res.job.status === 'failed' || res.job.status === 'cancelled') {
            clearInterval(pollingRef.current);
            setIsSyncing(false);
            setSyncFeedback(`⚠️ İşlem ${res.job.status === 'failed' ? 'hatayla sonuçlandı' : 'iptal edildi'}. Logları inceleyin.`);
          }
        }
      } catch (_) {}
    }, 1500);
  };

  // Stop Running Job
  const handleStopJob = async () => {
    if (!activeJobId) return;
    try {
      await ApiService.stopScriptJob(activeJobId, adminEmail);
      if (pollingRef.current) clearInterval(pollingRef.current);
      setIsSyncing(false);
      setSyncFeedback('İşlem durduruldu.');
    } catch (e: any) {
      setSyncFeedback('Durdurma hatası: ' + e.message);
    }
  };

  // Copy Logs
  const handleCopyLogs = () => {
    navigator.clipboard.writeText(jobLogs.join('\n'));
    setCopiedLogs(true);
    setTimeout(() => setCopiedLogs(false), 2000);
  };

  const formatDateTime = (isoStr?: string | null) => {
    if (!isoStr) return 'Bilinmiyor';
    try {
      const d = new Date(isoStr);
      return d.toLocaleDateString('tr-TR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch (_) {
      return isoStr;
    }
  };

  const TARGET_DRIVE_FOLDER_ID = '1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W';
  const TARGET_DRIVE_FOLDER_URL = `https://drive.google.com/drive/folders/${TARGET_DRIVE_FOLDER_ID}`;

  return (
    <div className="bg-gradient-to-br from-teal-50/90 via-cyan-50/70 to-white border border-teal-200/90 rounded-2xl p-4 sm:p-6 shadow-sm space-y-5 text-slate-800">
      {/* 1. Header with Status Badges */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-teal-200/80">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-teal-600 text-white flex items-center justify-center shrink-0 shadow-sm">
            <Cloud className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h4 className="font-bold text-sm sm:text-base text-slate-900">
                Google Drive Dosya Güncelleme & Manuel Senkronizasyon Ayarları
              </h4>
              <span className="bg-teal-700 text-white font-bold text-[10px] px-2 py-0.5 rounded-full">
                Yönetici Ayarı
              </span>
              {checkResult?.hasUpdates ? (
                <span className="bg-amber-100 text-amber-900 border border-amber-300 font-bold text-[10px] px-2 py-0.5 rounded-full flex items-center gap-1 animate-pulse">
                  <Sparkles className="w-3 h-3 text-amber-600" />
                  Drive'da {checkResult.newCount} Yeni Dosya Var!
                </span>
              ) : checkResult ? (
                <span className="bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold text-[10px] px-2 py-0.5 rounded-full flex items-center gap-1">
                  <Check className="w-3 h-3 text-emerald-600" />
                  Drive İle %100 Güncel
                </span>
              ) : null}
            </div>
            <p className="text-xs text-slate-600 mt-0.5">
              Google Drive'a yeni ders notları, amfi slaytları veya çıkmış sınav PDF'leri yüklendiğinde buradan manuel olarak güncelleyebilir veya otomatik tarama sıklığını belirleyebilirsiniz.
            </p>
          </div>
        </div>

        {/* Live status badge */}
        <div className="text-right shrink-0">
          <div className="inline-flex items-center gap-2 bg-white/90 border border-teal-200 px-3 py-1.5 rounded-xl text-xs font-semibold shadow-2xs">
            <div className={`w-2.5 h-2.5 rounded-full ${isSyncing ? 'bg-amber-500 animate-ping' : 'bg-emerald-500'}`} />
            <span>{isSyncing ? 'Senkronizasyon Sürüyor...' : 'İşleme Hazır'}</span>
          </div>
        </div>
      </div>

      {/* 2. Overview Stats & Last Run */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
        <div className="bg-white/80 border border-teal-100 p-3 rounded-xl space-y-1 shadow-2xs">
          <span className="text-[10px] font-bold text-slate-500 block uppercase tracking-wider">Son Drive Denetimi:</span>
          <div className="font-bold text-slate-800 flex items-center gap-1.5">
            <Search className="w-3.5 h-3.5 text-teal-600 shrink-0" />
            <span>{settings.lastCheckedAt ? formatDateTime(settings.lastCheckedAt) : 'Henüz yapılmadı'}</span>
          </div>
          <span className="text-[10px] text-slate-500 block">
            {checkResult ? `${checkResult.totalScanned} dosya tarandı (${checkResult.newCount} yeni)` : 'Durum tespiti için denetleyin'}
          </span>
        </div>

        <div className="bg-white/80 border border-teal-100 p-3 rounded-xl space-y-1 shadow-2xs">
          <span className="text-[10px] font-bold text-slate-500 block uppercase tracking-wider">Son Senkronizasyon:</span>
          <div className="font-bold text-slate-800 flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5 text-teal-600 shrink-0" />
            <span>{settings.lastSyncedAt ? formatDateTime(settings.lastSyncedAt) : 'Henüz senkronize edilmedi'}</span>
          </div>
          <span className="text-[10px] text-slate-500 block truncate" title={settings.lastSyncedSummary}>
            {settings.lastSyncedSummary || 'Geçmiş kayıt bulunamadı'}
          </span>
        </div>

        <div className="bg-white/80 border border-teal-100 p-3 rounded-xl space-y-1 shadow-2xs flex flex-col justify-between">
          <div>
            <span className="text-[10px] font-bold text-slate-500 block uppercase tracking-wider">Hedef Google Drive Klasörü:</span>
            <div className="font-bold text-teal-900 truncate">
              {settings.preferredScope === 'custom' && settings.customFolderId ? settings.customFolderId : 'Kurul 1-6 & Dönem 3 Çıkmışlar'}
            </div>
          </div>
          <a
            href={TARGET_DRIVE_FOLDER_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="text-[11px] font-bold text-teal-700 hover:text-teal-950 flex items-center gap-1 pt-1"
          >
            <FolderOpen className="w-3.5 h-3.5" />
            <span>Drive Klasörünü Aç ({TARGET_DRIVE_FOLDER_ID.slice(0, 10)}...)</span>
            <ExternalLink className="w-3 h-3 text-slate-400" />
          </a>
        </div>
      </div>

      {/* 3. Settings Form (Scope, Custom Folder, Auto-check, Interval) */}
      <div className="bg-white/90 border border-teal-200 rounded-xl p-4 sm:p-5 space-y-4 shadow-2xs">
        <div className="flex items-center justify-between pb-2 border-b border-slate-100">
          <h5 className="font-bold text-xs sm:text-sm text-slate-900 flex items-center gap-2">
            <Settings className="w-4 h-4 text-teal-600" />
            <span>Senkronizasyon & Tarama Tercihleri</span>
          </h5>
          <div className="flex items-center gap-2">
            {settingsSavedMessage && (
              <span className="text-[11px] font-bold text-emerald-700 animate-fade-in">
                {settingsSavedMessage}
              </span>
            )}
            <button
              type="button"
              onClick={handleSaveSettings}
              disabled={isSavingSettings}
              className="bg-teal-700 hover:bg-teal-800 disabled:opacity-50 text-white font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1 cursor-pointer transition-all shadow-2xs"
            >
              <Check className="w-3 h-3" />
              <span>{isSavingSettings ? 'Kaydediliyor...' : 'Ayarları Kaydet'}</span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          {/* Tarama Kapsamı */}
          <div className="space-y-1.5">
            <label className="font-bold text-slate-700 flex items-center gap-1.5 text-[11px]">
              <Layers className="w-3.5 h-3.5 text-teal-600" />
              <span>Güncelleme Kapsamı (Taranacak Alan):</span>
            </label>
            <select
              value={settings.preferredScope}
              onChange={(e) => setSettings({ ...settings, preferredScope: e.target.value as any })}
              className="w-full p-2.5 rounded-xl bg-slate-50 border border-slate-300 font-semibold focus:border-teal-500 focus:bg-white outline-none transition-all"
            >
              <option value="all">🌟 Tüm Drive Dosyaları (Ders Notları & Çıkmış Sorular - Önerilen)</option>
              <option value="lectures">📚 Yalnızca Ders Notları & Amfi Slaytları (Kurul 1-6)</option>
              <option value="exams">📝 Yalnızca Çıkmış Sorular & Arşiv Sınavları</option>
              <option value="custom">🔗 Özel Google Drive Klasörü (ID veya Bağlantı)</option>
            </select>
            <p className="text-[10px] text-slate-500">
              Hangi Drive klasörlerindeki güncellemelerin aranacağını belirler.
            </p>
          </div>

          {/* Otomatik Tarama Sıklığı */}
          <div className="space-y-1.5">
            <label className="font-bold text-slate-700 flex items-center gap-1.5 text-[11px]">
              <Clock className="w-3.5 h-3.5 text-teal-600" />
              <span>Otomatik Kontrol & Eşitleme Sıklığı:</span>
            </label>
            <select
              value={settings.syncInterval}
              onChange={(e) => setSettings({ ...settings, syncInterval: e.target.value as any })}
              className="w-full p-2.5 rounded-xl bg-slate-50 border border-slate-300 font-semibold focus:border-teal-500 focus:bg-white outline-none transition-all"
            >
              <option value="18:00">🕒 Hafta İçi Her Gün 18:00 (Masaüstü İşleyicisi)</option>
              <option value="1h">⏱️ Her 1 Saatte Bir Kontrol Et</option>
              <option value="30m">⏱️ Her 30 Dakikada Bir Kontrol Et</option>
              <option value="15m">⚡ Her 15 Dakikada Bir (Sınav Haftası Yoğun Mod)</option>
              <option value="manual">🛑 Yalnızca Manuel (Ben Butona Bastığımda)</option>
            </select>
            <p className="text-[10px] text-slate-500">
              Sistem arka planda çalışırken Drive'ı hangi periyotta denetleyecek.
            </p>
          </div>

          {/* Özel Klasör ID alanı (koşullu veya serbest) */}
          {settings.preferredScope === 'custom' && (
            <div className="space-y-1.5 md:col-span-2">
              <label className="font-bold text-slate-700 flex items-center gap-1.5 text-[11px]">
                <FolderOpen className="w-3.5 h-3.5 text-teal-600" />
                <span>Özel Google Drive Klasör ID'si veya Bağlantısı:</span>
              </label>
              <input
                type="text"
                value={settings.customFolderId}
                onChange={(e) => {
                  let val = e.target.value.trim();
                  // Extract ID if full URL pasted
                  const match = val.match(/folders\/([a-zA-Z0-9_-]+)/);
                  if (match && match[1]) val = match[1];
                  setSettings({ ...settings, customFolderId: val });
                }}
                placeholder="Örn: 1ozu5KiLZjFd4YKNMZ0bSRvLVV6b7lv0W veya https://drive.google.com/drive/folders/..."
                className="w-full p-2.5 rounded-xl bg-slate-50 border border-slate-300 font-mono text-xs focus:border-teal-500 focus:bg-white outline-none transition-all"
              />
              <p className="text-[10px] text-slate-500">
                Google Drive klasörünüzün adresindeki <code className="bg-slate-100 px-1 py-0.5 rounded font-mono">/folders/ID</code> kısmını veya doğrudan URL'yi yapıştırabilirsiniz.
              </p>
            </div>
          )}

          {/* Toggles (Notifications & Force) */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-2 border-t border-slate-100 md:col-span-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={settings.notifyOnUpdate}
                onChange={(e) => setSettings({ ...settings, notifyOnUpdate: e.target.checked })}
                className="w-4 h-4 text-teal-600 rounded"
              />
              <span className="text-[11px] font-semibold text-slate-700">
                Drive'da yeni veya güncellenen dosya bulunduğunda bildirim göster 🔔
              </span>
            </label>

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={forceReSync}
                onChange={(e) => setForceReSync(e.target.checked)}
                className="w-4 h-4 text-amber-600 rounded"
              />
              <span className="text-[11px] font-semibold text-slate-700">
                Tam Yeniden İndir (--force / Önceden indirilenleri atlama)
              </span>
            </label>
          </div>
        </div>
      </div>

      {/* 4. Action Buttons (Check & Manual Sync) */}
      <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
        <div className="text-xs text-slate-600 flex items-center gap-2">
          <HelpCircle className="w-4 h-4 text-teal-600 shrink-0" />
          <span>Drive'da bir değişiklik yaptığınızda önce <strong>"Denetle"</strong> butonuna basabilir veya doğrudan <strong>"Şimdi Güncelle"</strong> diyebilirsiniz.</span>
        </div>

        <div className="flex items-center gap-2.5 flex-wrap">
          {/* Button 1: Check Only (Dry Run) */}
          <button
            type="button"
            onClick={handleCheckDriveUpdates}
            disabled={isChecking || isSyncing}
            className="bg-white hover:bg-slate-50 border border-teal-300 text-teal-900 font-bold px-4 py-2.5 rounded-xl text-xs flex items-center gap-2 shadow-2xs cursor-pointer transition-all active:scale-95 disabled:opacity-50"
            title="Google Drive'daki yeni dosyaları tarar, indirme yapmadan değişiklikleri raporlar"
          >
            <Search className={`w-4 h-4 text-teal-600 ${isChecking ? 'animate-spin' : ''}`} />
            <span>{isChecking ? 'Drive Taranıyor...' : '1. Drive Güncellemelerini Denetle'}</span>
          </button>

          {/* Button 2: Trigger Manual Sync */}
          <button
            type="button"
            onClick={() => handleTriggerSync(forceReSync)}
            disabled={isSyncing || isChecking}
            className="bg-gradient-to-r from-teal-700 to-emerald-700 hover:from-teal-800 hover:to-emerald-800 disabled:opacity-50 text-white font-black px-5 py-2.5 rounded-xl text-xs flex items-center gap-2 shadow-md cursor-pointer transition-all active:scale-95"
            title="Tüm güncellenen dosyaları indirir, sayfa sayfa metne döker ve soru havuzuna işler"
          >
            <FolderSync className={`w-4 h-4 ${isSyncing ? 'animate-spin' : ''}`} />
            <span>{isSyncing ? 'Senkronizasyon Sürüyor...' : '2. Şimdi Manuel Güncelle & Senkronize Et'}</span>
          </button>
        </div>
      </div>

      {/* 5. Check Feedback & New Files Preview */}
      {checkFeedback && (
        <div className={`p-3.5 rounded-xl border text-xs flex items-start gap-3 ${
          checkResult?.hasUpdates
            ? 'bg-amber-50/90 border-amber-300 text-amber-950'
            : checkFeedback.startsWith('Hata')
            ? 'bg-rose-50 border-rose-300 text-rose-900'
            : 'bg-emerald-50/90 border-emerald-300 text-emerald-950'
        }`}>
          {checkResult?.hasUpdates ? (
            <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
          ) : checkFeedback.startsWith('Hata') ? (
            <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
          ) : (
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
          )}

          <div className="flex-1 space-y-1">
            <div className="font-bold flex items-center justify-between">
              <span>{checkFeedback}</span>
              {checkResult && checkResult.newFiles?.length > 0 && (
                <button
                  type="button"
                  onClick={() => setShowFileList(!showFileList)}
                  className="text-[11px] text-teal-800 hover:text-teal-950 underline flex items-center gap-1 font-semibold cursor-pointer"
                >
                  <span>{showFileList ? 'Listeyi Gizle' : `Dosyaları Göster (${checkResult.newCount})`}</span>
                  {showFileList ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                </button>
              )}
            </div>

            {/* List of New/Updated files */}
            {showFileList && checkResult && checkResult.newFiles && checkResult.newFiles.length > 0 && (
              <div className="mt-2 pt-2 border-t border-amber-200/80 space-y-1.5 max-h-48 overflow-y-auto pr-1">
                {checkResult.newFiles.map((file, idx) => (
                  <div key={idx} className="flex items-center justify-between bg-white/80 p-2 rounded-lg border border-amber-200/60 text-[11px]">
                    <div className="flex items-center gap-2 truncate pr-2">
                      <FileText className="w-3.5 h-3.5 text-teal-700 shrink-0" />
                      <span className="font-semibold text-slate-800 truncate" title={file.fullPath}>
                        {file.name}
                      </span>
                    </div>
                    <div className="flex items-center gap-1.5 shrink-0">
                      <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded ${
                        file.type === 'exam' ? 'bg-indigo-100 text-indigo-800' : 'bg-emerald-100 text-emerald-800'
                      }`}>
                        {file.type === 'exam' ? 'Çıkmış Sınav' : 'Ders Slaytı'}
                      </span>
                      <span className="text-[9px] font-bold bg-amber-100 text-amber-800 px-1.5 py-0.5 rounded">
                        {file.status}
                      </span>
                    </div>
                  </div>
                ))}

                <div className="pt-2 flex justify-end">
                  <button
                    type="button"
                    onClick={() => handleTriggerSync(false)}
                    disabled={isSyncing}
                    className="bg-amber-600 hover:bg-amber-700 text-white font-bold px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 cursor-pointer shadow-xs"
                  >
                    <FolderSync className="w-3.5 h-3.5" />
                    <span>Bu {checkResult.newCount} Dosyayı Hemen İndir ve İşle</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Sync Status Banner */}
      {syncFeedback && !isTerminalOpen && (
        <div className={`p-3.5 rounded-xl border text-xs flex items-center justify-between gap-3 ${
          syncFeedback.startsWith('✓') || syncFeedback.startsWith('🎉')
            ? 'bg-emerald-50 border-emerald-300 text-emerald-950'
            : syncFeedback.startsWith('Hata')
            ? 'bg-rose-50 border-rose-300 text-rose-900'
            : 'bg-teal-50 border-teal-300 text-teal-950'
        }`}>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
            <span className="font-bold">{syncFeedback}</span>
          </div>
          <button
            type="button"
            onClick={() => setIsTerminalOpen(true)}
            className="text-[11px] font-bold text-teal-700 hover:text-teal-900 underline flex items-center gap-1 cursor-pointer"
          >
            <Terminal className="w-3.5 h-3.5" />
            <span>Canlı Konsolu Aç</span>
          </button>
        </div>
      )}

      {/* 6. Real-Time Terminal / Console Drawer */}
      {isTerminalOpen && (
        <div className="bg-slate-950 border border-slate-800 rounded-2xl overflow-hidden shadow-xl space-y-0 text-white font-mono text-xs">
          {/* Terminal Top Bar */}
          <div className="bg-slate-900 px-4 py-2.5 flex items-center justify-between border-b border-slate-800">
            <div className="flex items-center gap-2">
              <Terminal className="w-4 h-4 text-emerald-400" />
              <span className="font-bold text-xs text-slate-200">
                Drive Senkronizasyon Konsolu {activeJobId ? `(Görev ID: ${activeJobId})` : ''}
              </span>
              {isSyncing && (
                <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
                  Çalışıyor
                </span>
              )}
            </div>

            <div className="flex items-center gap-2">
              <label className="text-[10px] text-slate-400 flex items-center gap-1 cursor-pointer">
                <input
                  type="checkbox"
                  checked={autoScroll}
                  onChange={(e) => setAutoScroll(e.target.checked)}
                  className="rounded text-teal-500 w-3 h-3"
                />
                <span>Oto-Kaydır</span>
              </label>

              <button
                type="button"
                onClick={handleCopyLogs}
                className="text-[11px] text-slate-300 hover:text-white bg-slate-800 px-2 py-1 rounded flex items-center gap-1 cursor-pointer"
                title="Logları Kopyala"
              >
                <Copy className="w-3 h-3" />
                <span>{copiedLogs ? 'Kopyalandı' : 'Kopyala'}</span>
              </button>

              {isSyncing && (
                <button
                  type="button"
                  onClick={handleStopJob}
                  className="text-[11px] bg-rose-900/60 hover:bg-rose-800 text-rose-200 border border-rose-700 px-2 py-1 rounded flex items-center gap-1 cursor-pointer"
                  title="Görevi İptal Et"
                >
                  <Square className="w-3 h-3 fill-current" />
                  <span>Durdur</span>
                </button>
              )}

              <button
                type="button"
                onClick={() => setIsTerminalOpen(false)}
                className="text-slate-400 hover:text-white text-xs px-2 py-1 rounded cursor-pointer"
                title="Konsolu Gizle"
              >
                Gizle
              </button>
            </div>
          </div>

          {/* Terminal Screen */}
          <div className="p-4 max-h-72 min-h-[160px] overflow-y-auto space-y-1 text-[11px] leading-relaxed bg-black/50 select-text">
            {jobLogs.length === 0 ? (
              <div className="text-slate-500 italic">Konsol çıktısı bekleniyor...</div>
            ) : (
              jobLogs.map((log, idx) => {
                let colorClass = 'text-slate-300';
                if (log.includes('HATA') || log.includes('ERR') || log.includes('error')) colorClass = 'text-rose-400 font-bold';
                else if (log.includes('✓') || log.includes('BAŞARIYLA') || log.includes('TAMAMLANDI')) colorClass = 'text-emerald-400 font-bold';
                else if (log.includes('⚠️') || log.includes('TESPİT EDİLDİ')) colorClass = 'text-amber-400 font-semibold';
                else if (log.includes('📥') || log.includes('İşleniyor') || log.includes('Taranıyor')) colorClass = 'text-teal-300';

                return (
                  <div key={idx} className={`${colorClass} font-mono break-all whitespace-pre-wrap`}>
                    {log}
                  </div>
                );
              })
            )}
            <div ref={logsEndRef} />
          </div>
        </div>
      )}
    </div>
  );
};
