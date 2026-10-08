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
import { Switch, logTone } from './manage/consoleUi';

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

  const statusTag = checkResult?.hasUpdates ? (
    <span className="ms-tag is-warn"><Sparkles /> Drive'da {checkResult.newCount} yeni dosya</span>
  ) : checkResult ? (
    <span className="ms-tag is-ok"><Check /> Drive ile güncel</span>
  ) : null;
  const feedbackTone = (msg: string) => (/hata|Hata|⚠|başlatılamadı|iptal/.test(msg) ? 'is-bad' : /✓|🎉|tamamlandı|güncel/i.test(msg) ? 'is-ok' : 'is-accent');
  const clean = (msg: string) => msg.replace(/^[✓🎉⚠️\s]+/u, '');

  return (
    <section className="ms-panel" aria-label="Google Drive eşitlemesi">
      <header className="ms-panel-head">
        <h2 className="ms-panel-title">
          <Cloud aria-hidden="true" /> Google Drive eşitlemesi
        </h2>
        <div className="ms-panel-tools">
          {statusTag}
          <span className="inline-flex items-center gap-1.5 text-[12.5px] text-ink-2">
            <span className={`ms-sdot ${isSyncing ? 'is-warn is-live' : 'is-ok'}`} aria-hidden="true" />
            {isSyncing ? 'Eşitleniyor' : 'Hazır'}
          </span>
        </div>
        <p className="ms-panel-desc">Drive'a yeni ders slaytı ya da çıkmış soru PDF'i yüklenince önce denetle, sonra indirip işle. Otomatik tarama sıklığını da buradan seç.</p>
      </header>

      <div className="ms-panel-body">
        <dl className="ms-kv">
          <dt>Son denetim</dt>
          <dd>
            {settings.lastCheckedAt ? formatDateTime(settings.lastCheckedAt) : 'Henüz yapılmadı'}
            {checkResult && <span className="text-ink-3"> · {checkResult.totalScanned} dosya tarandı, {checkResult.newCount} yeni</span>}
          </dd>
          <dt>Son eşitleme</dt>
          <dd>
            {settings.lastSyncedAt ? formatDateTime(settings.lastSyncedAt) : 'Henüz eşitlenmedi'}
            {settings.lastSyncedSummary && <span className="text-ink-3"> · {settings.lastSyncedSummary}</span>}
          </dd>
          <dt>Hedef klasör</dt>
          <dd className="flex flex-wrap items-center gap-x-2">
            <span>{settings.preferredScope === 'custom' && settings.customFolderId ? <span className="font-mono text-[12.5px]">{settings.customFolderId}</span> : 'Kurul 1–6 ve Dönem 3 çıkmışları'}</span>
            <a href={TARGET_DRIVE_FOLDER_URL} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 text-accent font-semibold hover:underline underline-offset-2">
              <FolderOpen className="w-3.5 h-3.5" /> Drive'da aç <ExternalLink className="w-3 h-3" />
            </a>
          </dd>
        </dl>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
          <label className="ms-field">
            <span className="lbl">Kapsam</span>
            <select value={settings.preferredScope} onChange={(e) => setSettings({ ...settings, preferredScope: e.target.value as any })} className="ms-input">
              <option value="all">Tüm Drive dosyaları (önerilen)</option>
              <option value="lectures">Yalnız ders notları ve amfi slaytları</option>
              <option value="exams">Yalnız çıkmış sorular</option>
              <option value="custom">Özel klasör (kimlik ya da bağlantı)</option>
            </select>
          </label>
          <label className="ms-field">
            <span className="lbl">Otomatik denetim</span>
            <select value={settings.syncInterval} onChange={(e) => setSettings({ ...settings, syncInterval: e.target.value as any })} className="ms-input">
              <option value="18:00">Hafta içi her gün 18:00</option>
              <option value="1h">Saatte bir</option>
              <option value="30m">30 dakikada bir</option>
              <option value="15m">15 dakikada bir (sınav haftası)</option>
              <option value="manual">Yalnız elle</option>
            </select>
          </label>
          {settings.preferredScope === 'custom' && (
            <label className="ms-field md:col-span-2">
              <span className="lbl">Özel klasör</span>
              <input
                type="text"
                value={settings.customFolderId}
                onChange={(e) => {
                  let val = e.target.value.trim();
                  const match = val.match(/folders\/([a-zA-Z0-9_-]+)/);
                  if (match && match[1]) val = match[1];
                  setSettings({ ...settings, customFolderId: val });
                }}
                placeholder="Klasör kimliği ya da drive.google.com/drive/folders/… bağlantısı"
                className="ms-input is-mono"
              />
              <span className="hint">Bağlantıyı yapıştırınca kimlik kendiliğinden ayıklanır.</span>
            </label>
          )}
        </div>
        <div className="flex flex-col sm:flex-row sm:flex-wrap gap-x-6 gap-y-1">
          <Switch checked={settings.notifyOnUpdate} onChange={(v) => setSettings({ ...settings, notifyOnUpdate: v })} label="Yeni dosya bulununca bildir" />
          <Switch checked={forceReSync} onChange={setForceReSync} label="Tam yeniden indir" hint="Önceden indirilenleri de yeniden indirir (--force)." />
        </div>

        <div className="flex flex-wrap items-center gap-2 pt-1">
          <button type="button" onClick={handleCheckDriveUpdates} disabled={isChecking || isSyncing} className="ms-btn" title="İndirmeden, yalnız yeni ve değişen dosyaları raporlar">
            <Search className={isChecking ? 'animate-pulse' : ''} /> {isChecking ? 'Drive taranıyor…' : 'Değişiklikleri denetle'}
          </button>
          <button type="button" onClick={() => handleTriggerSync(forceReSync)} disabled={isSyncing || isChecking} className="ms-btn is-primary" title="Değişen dosyaları indirir, metne döker ve veri hattına verir">
            <FolderSync className={isSyncing ? 'animate-spin' : ''} /> {isSyncing ? 'Eşitleniyor…' : 'Şimdi eşitle'}
          </button>
          <span className="flex-1" />
          {settingsSavedMessage && <span className={`text-[12.5px] font-semibold ${settingsSavedMessage.startsWith('Hata') ? 'text-bad-text' : 'text-ok'}`}>{clean(settingsSavedMessage)}</span>}
          <button type="button" onClick={handleSaveSettings} disabled={isSavingSettings} className="ms-btn is-tonal">
            <Check /> {isSavingSettings ? 'Kaydediliyor…' : 'Drive ayarlarını kaydet'}
          </button>
        </div>

        {checkFeedback && (
          <div className={`ms-alert ${checkResult?.hasUpdates ? 'is-warn' : feedbackTone(checkFeedback)} flex-col !gap-2`}>
            <div className="flex items-start gap-2.5 w-full">
              {checkResult?.hasUpdates || checkFeedback.startsWith('Denetim hatası') ? <AlertTriangle aria-hidden="true" /> : <CheckCircle2 aria-hidden="true" />}
              <span className="flex-1 font-medium">{checkFeedback}</span>
              {checkResult && checkResult.newFiles?.length > 0 && (
                <button type="button" onClick={() => setShowFileList(!showFileList)} className="ms-btn is-sm is-ghost">
                  {showFileList ? <ChevronUp /> : <ChevronDown />} {showFileList ? 'Listeyi gizle' : `Dosyalar (${checkResult.newCount})`}
                </button>
              )}
            </div>
            {showFileList && checkResult && checkResult.newFiles?.length > 0 && (
              <div className="w-full flex flex-col gap-1.5">
                <ul className="m-0 p-0 list-none flex flex-col gap-1 max-h-56 overflow-y-auto">
                  {checkResult.newFiles.map((file, idx) => (
                    <li key={idx} className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-white/70 text-[12.5px]">
                      <FileText className="w-3.5 h-3.5 text-ink-3 shrink-0" />
                      <span className="flex-1 min-w-0 truncate text-ink" title={file.fullPath}>{file.name}</span>
                      <span className={`ms-tag ${file.type === 'exam' ? 'is-accent' : ''}`}>{file.type === 'exam' ? 'Çıkmış sınav' : 'Ders slaytı'}</span>
                      <span className="ms-tag is-warn">{file.status}</span>
                    </li>
                  ))}
                </ul>
                <button type="button" onClick={() => handleTriggerSync(false)} disabled={isSyncing} className="ms-btn is-sm is-primary self-end">
                  <FolderSync /> Bu {checkResult.newCount} dosyayı indir ve işle
                </button>
              </div>
            )}
          </div>
        )}

        {syncFeedback && !isTerminalOpen && (
          <div className={`ms-alert ${feedbackTone(syncFeedback)} items-center`}>
            {feedbackTone(syncFeedback) === 'is-bad' ? <AlertTriangle aria-hidden="true" /> : <CheckCircle2 aria-hidden="true" />}
            <span className="flex-1 font-medium">{clean(syncFeedback)}</span>
            <button type="button" onClick={() => setIsTerminalOpen(true)} className="ms-btn is-sm is-ghost">
              <Terminal /> Konsolu aç
            </button>
          </div>
        )}

        {isTerminalOpen && (
          <div className="flex flex-col gap-2">
            <div className="flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-2 text-[13px] font-semibold text-ink mr-auto">
                <Terminal className="w-4 h-4 text-ink-3" /> Eşitleme konsolu
                {activeJobId && <span className="font-mono text-[11.5px] text-ink-3 font-normal">{activeJobId}</span>}
                {isSyncing && <span className="ms-tag is-ok"><span className="ms-sdot is-ok is-live" /> Çalışıyor</span>}
                {activeJob?.status === 'failed' && <span className="ms-tag is-bad">Hata</span>}
              </span>
              <Switch checked={autoScroll} onChange={setAutoScroll} label={<span className="text-[13px]">Otomatik kaydır</span>} />
              <button type="button" onClick={handleCopyLogs} className="ms-btn is-sm is-ghost">
                {copiedLogs ? <Check /> : <Copy />} {copiedLogs ? 'Kopyalandı' : 'Kopyala'}
              </button>
              {isSyncing && (
                <button type="button" onClick={handleStopJob} className="ms-btn is-sm is-danger">
                  <Square /> Durdur
                </button>
              )}
              <button type="button" onClick={() => setIsTerminalOpen(false)} className="ms-btn is-sm is-ghost">
                Gizle
              </button>
            </div>
            <pre className="ms-term" aria-live="polite">
              {jobLogs.length === 0 ? (
                <span className="t">Konsol çıktısı bekleniyor…</span>
              ) : (
                jobLogs.map((log, idx) => (
                  <div key={idx} className={logTone(log)}>
                    {log}
                  </div>
                ))
              )}
              <div ref={logsEndRef} />
            </pre>
          </div>
        )}
      </div>
    </section>
  );
};
