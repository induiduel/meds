import React, { useState, useEffect, useRef } from 'react';
import {
  Terminal,
  Play,
  Square,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  Search,
  Zap,
  Clock,
  ExternalLink,
  Layers,
  Copy,
  Cpu,
  Filter,
  Eye,
  ChevronRight,
  Code,
  ShieldCheck,
  Check,
  X,
  FileCode,
  ArrowRight
} from 'lucide-react';
import {
  ApiService,
  AdminScriptItem,
  AdminPipelineItem,
  AdminScriptJob
} from '../services/api';

interface AdminScriptsTabProps {
  adminEmail: string;
  onRefreshAllData?: () => Promise<void>;
}

export const AdminScriptsTab: React.FC<AdminScriptsTabProps> = ({
  adminEmail,
  onRefreshAllData,
}) => {
  const [scripts, setScripts] = useState<AdminScriptItem[]>([]);
  const [pipelines, setPipelines] = useState<AdminPipelineItem[]>([]);
  const [activeJobs, setActiveJobs] = useState<Record<string, AdminScriptJob>>({});
  const [historyJobs, setHistoryJobs] = useState<AdminScriptJob[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('Tümü');
  const [customArgs, setCustomArgs] = useState<Record<string, string>>({});
  const [feedback, setFeedback] = useState<{ text: string; type: 'success' | 'error' | 'info' } | null>(null);

  // Terminal Console Drawer State
  const [isTerminalOpen, setIsTerminalOpen] = useState(false);
  const [terminalJobId, setTerminalJobId] = useState<string | null>(null);
  const [terminalJob, setTerminalJob] = useState<AdminScriptJob | null>(null);
  const [terminalLogs, setTerminalLogs] = useState<string[]>([]);
  const [autoScroll, setAutoScroll] = useState(true);
  const [copied, setCopied] = useState(false);
  const [runningJobName, setRunningJobName] = useState<string | null>(null);

  const logsEndRef = useRef<HTMLDivElement>(null);
  const pollingRef = useRef<any>(null);

  // Load scripts on mount
  useEffect(() => {
    loadScriptsData();
    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, []);

  // Auto-scroll terminal
  useEffect(() => {
    if (autoScroll && logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [terminalLogs, autoScroll]);

  // Polling for active job in terminal
  useEffect(() => {
    if (!terminalJobId) return;

    const fetchStatus = async () => {
      try {
        const res = await ApiService.getScriptJobStatus(terminalJobId);
        if (res.success && res.job) {
          setTerminalJob(res.job);
          if (res.job.logs) {
            setTerminalLogs(res.job.logs);
          }
          if (res.job.status !== 'running') {
            setRunningJobName(null);
            // Refresh list to update statuses
            loadScriptsData(true);
          }
        }
      } catch (_) {}
    };

    fetchStatus();
    if (pollingRef.current) clearInterval(pollingRef.current);

    pollingRef.current = setInterval(fetchStatus, 1200);

    return () => {
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, [terminalJobId]);

  const loadScriptsData = async (silent: boolean = false) => {
    if (!silent) setIsLoading(true);
    try {
      const res = await ApiService.getScriptsList();
      if (res.success) {
        setScripts(res.scripts);
        setPipelines(res.pipelines);
        if (res.jobs) {
          const map: Record<string, AdminScriptJob> = {};
          for (const j of res.jobs.active || []) {
            map[j.name] = j;
          }
          setActiveJobs(map);
          setHistoryJobs(res.jobs.history || []);
        }

        // Initialize default args if empty
        setCustomArgs((prev) => {
          const next = { ...prev };
          for (const s of res.scripts) {
            if (next[s.name] === undefined && s.defaultArgs) {
              next[s.name] = s.defaultArgs;
            }
          }
          return next;
        });
      }
    } catch (e: any) {
      setFeedback({ text: 'Script listesi alınamadı: ' + e.message, type: 'error' });
    } finally {
      if (!silent) setIsLoading(false);
    }
  };

  const handleRunScript = async (scriptName: string) => {
    const args = customArgs[scriptName] || '';
    setFeedback({ text: `${scriptName} başlatılıyor...`, type: 'info' });
    setRunningJobName(scriptName);

    try {
      const res = await ApiService.runScript(scriptName, args, adminEmail);
      if (res.success) {
        setFeedback({ text: res.message || `${scriptName} başarıyla başlatıldı.`, type: 'success' });
        if (res.job?.id) {
          setTerminalJobId(res.job.id);
          setTerminalJob(res.job);
          setTerminalLogs(res.job.logs || []);
          setIsTerminalOpen(true);
        }
        await loadScriptsData(true);
      } else {
        setFeedback({ text: 'Başlatılamadı: ' + res.message, type: 'error' });
        setRunningJobName(null);
      }
    } catch (e: any) {
      setFeedback({ text: 'Hata: ' + e.message, type: 'error' });
      setRunningJobName(null);
    }
  };

  const handleRunPipeline = async (pipelineId: string) => {
    setFeedback({ text: `Pipeline (${pipelineId}) başlatılıyor...`, type: 'info' });
    try {
      const res = await ApiService.runScriptPipeline(pipelineId, adminEmail);
      if (res.success) {
        setFeedback({ text: res.message || 'Pipeline başlatıldı.', type: 'success' });
        if (res.job?.id) {
          setTerminalJobId(res.job.id);
          setTerminalJob(res.job);
          setTerminalLogs(res.job.logs || []);
          setIsTerminalOpen(true);
        }
        await loadScriptsData(true);
      } else {
        setFeedback({ text: 'Pipeline başlatılamadı: ' + res.message, type: 'error' });
      }
    } catch (e: any) {
      setFeedback({ text: 'Pipeline hatası: ' + e.message, type: 'error' });
    }
  };

  const handleStopJob = async (jobId: string) => {
    try {
      const res = await ApiService.stopScriptJob(jobId, adminEmail);
      if (res.success) {
        setFeedback({ text: 'İşlem sonlandırıldı.', type: 'info' });
        await loadScriptsData(true);
      }
    } catch (e: any) {
      setFeedback({ text: 'Durdurma hatası: ' + e.message, type: 'error' });
    }
  };

  const openTerminalForJob = (job: AdminScriptJob) => {
    setTerminalJobId(job.id);
    setTerminalJob(job);
    setTerminalLogs(job.logs || []);
    setIsTerminalOpen(true);
  };

  // Categories list
  const categories = ['Tümü', ...Array.from(new Set(scripts.map((s) => s.category)))];

  // Filtered scripts
  const filteredScripts = scripts.filter((s) => {
    const matchesCat = selectedCategory === 'Tümü' || s.category === selectedCategory;
    const q = searchQuery.toLowerCase().trim();
    const matchesSearch =
      !q ||
      s.name.toLowerCase().includes(q) ||
      s.title.toLowerCase().includes(q) ||
      s.description.toLowerCase().includes(q) ||
      (s.tags && s.tags.some((t) => t.toLowerCase().includes(q)));
    return matchesCat && matchesSearch;
  });

  // Helper for runtime badge styling
  const getRuntimeBadge = (runtime: string) => {
    switch (runtime) {
      case 'node':
        return { label: 'Node.js', bg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' };
      case 'tsx':
        return { label: 'TypeScript', bg: 'bg-sky-500/20 text-sky-300 border-sky-500/30' };
      case 'python':
        return { label: 'Python 3', bg: 'bg-amber-500/20 text-amber-300 border-amber-500/30' };
      case 'batch':
        return { label: 'CMD / Batch', bg: 'bg-orange-500/20 text-orange-300 border-orange-500/30' };
      case 'powershell':
        return { label: 'PowerShell', bg: 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30' };
      default:
        return { label: runtime, bg: 'bg-slate-700 text-slate-300 border-slate-600' };
    }
  };

  return (
    <div className="flex flex-col h-full overflow-hidden bg-slate-950 text-slate-100 text-xs">
      {/* 1. Header Banner & Dynamic Auto-Discovery Info */}
      <div className="p-4 sm:p-5 border-b border-slate-800 bg-gradient-to-r from-slate-900 via-slate-900 to-indigo-950 shrink-0">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-indigo-600/30 border border-indigo-500/50 flex items-center justify-center text-indigo-400">
                <Terminal className="w-4 h-4" />
              </div>
              <h3 className="text-base sm:text-lg font-black text-white flex items-center gap-2">
                <span>Script & Görev Otomasyon Merkezi</span>
                <span className="bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 text-[11px] font-bold px-2 py-0.5 rounded-full">
                  {scripts.length} Script Hazır
                </span>
                {Object.keys(activeJobs).length > 0 && (
                  <span className="bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-[10px] font-extrabold px-2 py-0.5 rounded-full flex items-center gap-1 animate-pulse">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                    {Object.keys(activeJobs).length} Süreç Çalışıyor
                  </span>
                )}
              </h3>
            </div>
            <p className="text-[11px] text-slate-300 max-w-3xl leading-relaxed">
              Bu panel; <code className="bg-slate-800 text-indigo-300 px-1 py-0.5 rounded font-mono">scripts/</code> klasöründeki mevcut tüm betikleri ve <strong>ileride oluşturacağınız her yeni scripti</strong> otomatik olarak tanır. İstediğiniz argümanlarla anlık çalıştırabilir, toplu otomasyon zincirleri (pipelines) tetikleyebilir ve canlı çıktıları konsoldan izleyebilirsiniz.
            </p>
          </div>

          <div className="flex items-center gap-2 self-start md:self-center shrink-0">
            <button
              onClick={() => setIsTerminalOpen(!isTerminalOpen)}
              className={`px-3 py-2 rounded-xl font-bold flex items-center gap-1.5 transition-all cursor-pointer text-xs border ${
                isTerminalOpen
                  ? 'bg-indigo-600 text-white border-indigo-500 shadow-md'
                  : 'bg-slate-800 hover:bg-slate-700 text-indigo-300 border-slate-700'
              }`}
              title="Canlı terminal ve log konsolunu açar/kapatır"
            >
              <FileCode className="w-3.5 h-3.5" />
              <span>{isTerminalOpen ? 'Terminali Gizle' : 'Canlı Konsol'}</span>
              {terminalLogs.length > 0 && (
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              )}
            </button>

            <button
              onClick={() => loadScriptsData()}
              disabled={isLoading}
              className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-bold px-3.5 py-2 rounded-xl flex items-center gap-1.5 shadow-sm transition-all cursor-pointer text-xs"
              title="scripts/ klasörünü yeniden dinamik tarar"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
              <span>{isLoading ? 'Taranıyor...' : 'Yeniden Tara'}</span>
            </button>
          </div>
        </div>

        {/* Action feedback message */}
        {feedback && (
          <div
            className={`mt-3 p-2.5 rounded-xl border flex items-center justify-between text-xs animate-fadeIn ${
              feedback.type === 'success'
                ? 'bg-emerald-950/80 border-emerald-500/50 text-emerald-200'
                : feedback.type === 'error'
                ? 'bg-rose-950/80 border-rose-500/50 text-rose-200'
                : 'bg-indigo-950/80 border-indigo-500/50 text-indigo-200'
            }`}
          >
            <div className="flex items-center gap-2">
              {feedback.type === 'success' ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              ) : (
                <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
              )}
              <span>{feedback.text}</span>
            </div>
            <button
              onClick={() => setFeedback(null)}
              className="text-slate-400 hover:text-white p-1 cursor-pointer"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        )}
      </div>

      {/* 2. Main Scrollable Content */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-5 space-y-6">
        {/* Predefined Automation Pipelines (Chains) */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="font-bold text-sm text-white flex items-center gap-2">
              <Zap className="w-4 h-4 text-amber-400" />
              <span>Tek Tıkla Zincirleme Otomasyonlar (Pipelines)</span>
            </h4>
            <span className="text-[11px] text-slate-400">
              Birden fazla scripti sıralı ve hatasız icra eder
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {pipelines.map((pipe) => {
              const isPipeRunning =
                terminalJob?.type === 'pipeline' &&
                terminalJob?.pipelineId === pipe.id &&
                terminalJob?.status === 'running';

              return (
                <div
                  key={pipe.id}
                  className="bg-slate-900/90 border border-slate-800 hover:border-indigo-600/50 rounded-2xl p-4 flex flex-col justify-between transition-all shadow-sm"
                >
                  <div className="space-y-2">
                    <div className="flex items-start justify-between gap-2">
                      <h5 className="font-bold text-xs text-white leading-snug">{pipe.title}</h5>
                      <span className="text-[10px] bg-slate-800 text-slate-400 font-mono px-1.5 py-0.5 rounded shrink-0">
                        {pipe.steps.length} Adım
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-300 leading-relaxed">{pipe.description}</p>

                    <div className="bg-slate-950/60 p-2 rounded-xl border border-slate-800/80 space-y-1 text-[10px] font-mono text-slate-400">
                      {pipe.steps.map((st, idx) => (
                        <div key={idx} className="flex items-center gap-1.5 truncate">
                          <span className="text-indigo-400 shrink-0 font-bold">{idx + 1}.</span>
                          <span className="truncate text-slate-300">{st.title || st.script}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="pt-3 mt-3 border-t border-slate-800/80 flex items-center justify-between gap-2">
                    <span className="text-[10px] text-slate-400">Arka Plan Süreci</span>
                    <button
                      onClick={() => handleRunPipeline(pipe.id)}
                      disabled={isPipeRunning}
                      className={`px-3 py-1.5 rounded-xl font-bold text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer ${
                        isPipeRunning
                          ? 'bg-amber-600 text-white animate-pulse'
                          : 'bg-indigo-600 hover:bg-indigo-500 text-white active:scale-95'
                      }`}
                    >
                      {isPipeRunning ? (
                        <>
                          <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                          <span>Çalışıyor...</span>
                        </>
                      ) : (
                        <>
                          <Play className="w-3.5 h-3.5 fill-current" />
                          <span>Pipeline Başlat</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Filters and Search Bar */}
        <div className="space-y-3 pt-2">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div className="relative flex-1 max-w-md">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input
                type="text"
                placeholder="Script adı, açıklama veya etiket ara (örn: slide, supabase, verify)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-2.5 top-2.5 text-slate-400 hover:text-white"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>

            <span className="text-[11px] text-slate-400">
              Gösterilen: <strong>{filteredScripts.length}</strong> / Toplam: {scripts.length} script
            </span>
          </div>

          {/* Category Pills */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-[11px] scrollbar-none">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-3 py-1 rounded-xl font-bold whitespace-nowrap transition-all cursor-pointer shrink-0 ${
                  selectedCategory === cat
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-slate-800'
                }`}
              >
                {cat}
                <span className="ml-1 opacity-70 text-[10px]">
                  (
                  {cat === 'Tümü'
                    ? scripts.length
                    : scripts.filter((s) => s.category === cat).length}
                  )
                </span>
              </button>
            ))}
          </div>
        </div>

        {/* Individual Script Cards Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-3.5">
          {filteredScripts.map((script) => {
            const badge = getRuntimeBadge(script.runtime);
            const activeJob = activeJobs[script.name];
            const isCurrentlyRunning = Boolean(activeJob || runningJobName === script.name);
            const userArg = customArgs[script.name] !== undefined ? customArgs[script.name] : script.defaultArgs || '';

            return (
              <div
                key={script.name}
                className={`bg-slate-900/80 rounded-2xl p-4 border transition-all flex flex-col justify-between ${
                  isCurrentlyRunning
                    ? 'border-indigo-500 bg-indigo-950/20 shadow-lg'
                    : 'border-slate-800/90 hover:border-slate-700'
                }`}
              >
                <div className="space-y-2">
                  <div className="flex items-start justify-between gap-2 flex-wrap">
                    <div className="space-y-0.5">
                      <div className="flex items-center gap-2 flex-wrap">
                        <h5 className="font-black text-xs sm:text-sm text-white">{script.title}</h5>
                        {script.isCustom && (
                          <span className="bg-fuchsia-500/20 text-fuchsia-300 border border-fuchsia-500/30 text-[9px] font-bold px-1.5 py-0.2 rounded-full">
                            ✨ Yeni Eklenen
                          </span>
                        )}
                      </div>
                      <div className="flex items-center gap-1.5">
                        <code className="text-[10px] text-indigo-300 font-mono bg-slate-950 px-1.5 py-0.5 rounded border border-slate-800">
                          {script.name}
                        </code>
                        {script.sizeBytes ? (
                          <span className="text-[10px] text-slate-500">
                            ({(script.sizeBytes / 1024).toFixed(1)} KB)
                          </span>
                        ) : null}
                      </div>
                    </div>

                    <div className="flex items-center gap-1.5 shrink-0">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${badge.bg}`}>
                        {badge.label}
                      </span>
                    </div>
                  </div>

                  <p className="text-[11px] text-slate-300 leading-relaxed">{script.description}</p>

                  {/* Tags */}
                  {script.tags && script.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1 pt-1">
                      {script.tags.map((tag) => (
                        <span
                          key={tag}
                          className="text-[9px] bg-slate-950 text-slate-400 border border-slate-800 px-1.5 py-0.2 rounded"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Custom Parameter / Arg Input */}
                  <div className="pt-2">
                    <label className="text-[10px] text-slate-400 block mb-1 font-semibold flex items-center justify-between">
                      <span>Çalıştırma Argümanları (Opsiyonel):</span>
                      {script.defaultArgs && (
                        <button
                          onClick={() =>
                            setCustomArgs((prev) => ({ ...prev, [script.name]: script.defaultArgs || '' }))
                          }
                          className="text-indigo-400 hover:text-indigo-300 text-[9px] cursor-pointer"
                        >
                          Varsayılana Dön ({script.defaultArgs})
                        </button>
                      )}
                    </label>
                    <input
                      type="text"
                      placeholder="Örn: --unverified, --all, -Action check..."
                      value={userArg}
                      onChange={(e) =>
                        setCustomArgs((prev) => ({ ...prev, [script.name]: e.target.value }))
                      }
                      className="w-full bg-slate-950 border border-slate-800 rounded-xl px-2.5 py-1.5 text-[11px] font-mono text-indigo-200 placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                </div>

                {/* Card Footer Actions */}
                <div className="pt-3 mt-3 border-t border-slate-800/80 flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    {isCurrentlyRunning ? (
                      <span className="text-[11px] font-bold text-emerald-400 flex items-center gap-1.5 animate-pulse">
                        <span className="w-2 h-2 rounded-full bg-emerald-400" />
                        Çalışıyor...
                      </span>
                    ) : (
                      <span className="text-[10px] text-slate-500">Hazır</span>
                    )}
                  </div>

                  <div className="flex items-center gap-2">
                    {/* View Logs Button */}
                    <button
                      type="button"
                      onClick={() => {
                        const targetJob =
                          activeJob ||
                          historyJobs.find((h) => h.name.toLowerCase() === script.name.toLowerCase());
                        if (targetJob) {
                          openTerminalForJob(targetJob);
                        } else {
                          // Open empty terminal
                          setTerminalJobId(null);
                          setTerminalJob(null);
                          setTerminalLogs([
                            `[Bilgi] ${script.title} için henüz kayıtlı log bulunmuyor.`,
                            `Başlatmak için 'Çalıştır' butonuna basabilirsiniz.`
                          ]);
                          setIsTerminalOpen(true);
                        }
                      }}
                      className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-2.5 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1 cursor-pointer transition-all"
                      title="Bu betiğin son loglarını inceler"
                    >
                      <Eye className="w-3.5 h-3.5" />
                      <span>Loglar</span>
                    </button>

                    {/* Run / Stop Button */}
                    {isCurrentlyRunning && activeJob ? (
                      <button
                        type="button"
                        onClick={() => handleStopJob(activeJob.id)}
                        className="bg-rose-900/80 hover:bg-rose-800 text-rose-200 border border-rose-700/80 font-bold px-3 py-1.5 rounded-xl text-xs flex items-center gap-1 cursor-pointer transition-all"
                      >
                        <Square className="w-3.5 h-3.5 fill-current" />
                        <span>Durdur</span>
                      </button>
                    ) : (
                      <button
                        type="button"
                        onClick={() => handleRunScript(script.name)}
                        disabled={isCurrentlyRunning}
                        className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-black px-3.5 py-1.5 rounded-xl text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer active:scale-95"
                      >
                        <Play className="w-3.5 h-3.5 fill-current" />
                        <span>Çalıştır</span>
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 3. Interactive Live Terminal Drawer */}
      {isTerminalOpen && (
        <div className="border-t border-slate-700 bg-slate-950 flex flex-col h-72 sm:h-80 shadow-2xl shrink-0 animate-slideUp">
          {/* Terminal Header */}
          <div className="p-2.5 sm:px-4 bg-slate-900 border-b border-slate-800 flex items-center justify-between gap-3 text-xs">
            <div className="flex items-center gap-2 overflow-hidden">
              <Terminal className="w-4 h-4 text-emerald-400 shrink-0" />
              <div className="truncate">
                <span className="font-bold text-white truncate">
                  {terminalJob?.title || terminalJob?.name || 'Canlı Betik Konsolu'}
                </span>
                {terminalJob?.status && (
                  <span
                    className={`ml-2 text-[10px] font-extrabold px-1.5 py-0.2 rounded ${
                      terminalJob.status === 'running'
                        ? 'bg-amber-500/20 text-amber-300 animate-pulse'
                        : terminalJob.status === 'completed'
                        ? 'bg-emerald-500/20 text-emerald-300'
                        : 'bg-rose-500/20 text-rose-300'
                    }`}
                  >
                    {terminalJob.status.toUpperCase()}
                  </span>
                )}
                {terminalJob?.durationMs ? (
                  <span className="text-[10px] text-slate-400 ml-2">
                    ({(terminalJob.durationMs / 1000).toFixed(1)} sn)
                  </span>
                ) : null}
              </div>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <label className="hidden sm:flex items-center gap-1 text-[11px] text-slate-400 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={autoScroll}
                  onChange={(e) => setAutoScroll(e.target.checked)}
                  className="rounded w-3.5 h-3.5 text-indigo-600 bg-slate-800"
                />
                <span>Oto-Kaydır</span>
              </label>

              {terminalJob?.status === 'running' && (
                <button
                  onClick={() => handleStopJob(terminalJob.id)}
                  className="bg-rose-900/80 hover:bg-rose-800 text-rose-200 border border-rose-700/80 px-2.5 py-1 rounded-lg text-[11px] font-bold flex items-center gap-1 cursor-pointer"
                >
                  <Square className="w-3 h-3 fill-current" />
                  <span>Durdur</span>
                </button>
              )}

              <button
                onClick={() => {
                  navigator.clipboard.writeText(terminalLogs.join('\n'));
                  setCopied(true);
                  setTimeout(() => setCopied(false), 2000);
                }}
                className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-2.5 py-1 rounded-lg text-[11px] flex items-center gap-1 cursor-pointer"
                title="Tüm logları panoya kopyalar"
              >
                <Copy className="w-3 h-3" />
                <span>{copied ? '✓ Kopyalandı' : 'Kopyala'}</span>
              </button>

              <button
                onClick={() => setTerminalLogs([])}
                className="bg-slate-800 hover:bg-slate-700 text-slate-300 px-2.5 py-1 rounded-lg text-[11px] cursor-pointer"
                title="Konsol ekranını temizler"
              >
                Temizle
              </button>

              <button
                onClick={() => setIsTerminalOpen(false)}
                className="bg-slate-800 hover:bg-slate-700 text-slate-300 p-1.5 rounded-lg text-[11px] cursor-pointer"
                title="Terminali Kapat"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Terminal Logs View */}
          <div className="flex-1 p-3 font-mono text-[11px] overflow-y-auto leading-relaxed bg-slate-950 text-slate-200 select-text">
            {terminalLogs.length === 0 ? (
              <div className="text-slate-500 py-6 text-center font-sans">
                Henüz konsol çıktısı yok. Yukarıdan bir script veya otomasyon başlatın...
              </div>
            ) : (
              terminalLogs.map((log, index) => {
                let colorClass = 'text-slate-300';
                if (log.includes('[HATA]') || log.includes('[STDERR]') || log.includes('error') || log.includes('Error')) {
                  colorClass = 'text-rose-400 font-semibold';
                } else if (log.includes('[BAŞARILI]') || log.includes('✓') || log.includes('BAŞARIYLA')) {
                  colorClass = 'text-emerald-400 font-semibold';
                } else if (log.includes('[UYARI]') || log.includes('WARN')) {
                  colorClass = 'text-amber-400';
                } else if (log.includes('🚀') || log.includes('▶️') || log.includes('BAŞLADI')) {
                  colorClass = 'text-indigo-300 font-bold';
                }

                return (
                  <div key={index} className={`whitespace-pre-wrap break-all ${colorClass}`}>
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
