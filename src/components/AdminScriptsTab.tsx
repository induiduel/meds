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
import { BUNDLED_SCRIPTS, BUNDLED_PIPELINES } from '../data/bundledScripts';
import { toast } from './ui/Toast';
import { Panel, EmptyState, SearchBox, ChipBar, Switch, Drawer, logTone } from './manage/consoleUi';

interface AdminScriptsTabProps {
  adminEmail: string;
  onRefreshAllData?: () => Promise<void>;
}

export const AdminScriptsTab: React.FC<AdminScriptsTabProps> = ({
  adminEmail,
  onRefreshAllData,
}) => {
  const [scripts, setScripts] = useState<AdminScriptItem[]>(() => BUNDLED_SCRIPTS);
  const [pipelines, setPipelines] = useState<AdminPipelineItem[]>(() => BUNDLED_PIPELINES);
  const [activeJobs, setActiveJobs] = useState<Record<string, AdminScriptJob>>({});
  const [historyJobs, setHistoryJobs] = useState<AdminScriptJob[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('Tümü');
  const [customArgs, setCustomArgs] = useState<Record<string, string>>(() => {
    const init: Record<string, string> = {};
    for (const s of BUNDLED_SCRIPTS) {
      if (s.defaultArgs) init[s.name] = s.defaultArgs;
    }
    return init;
  });
  // Durum iletileri uygulama genelindeki toast ile gösterilir
  const setFeedback = (f: { text: string; type: 'success' | 'error' | 'info' } | null) => {
    if (!f) return;
    if (f.type === 'error') toast.error(f.text);
    else if (f.type === 'success') toast.success(f.text);
  };

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

  // Veri başlıklarındaki baştaki emoji ve elle yazılmış "1." numarası görünümde atılır
  const cleanTitle = (t: string) => t.replace(/^[\p{Extended_Pictographic}\uFE0F\u200D\s]+/u, '').replace(/^\d+\.\s*/, '');
  const RUNTIME_LABEL: Record<string, string> = { node: 'Node.js', tsx: 'TypeScript', python: 'Python', batch: 'Batch', powershell: 'PowerShell' };
  const runningCount = Object.keys(activeJobs).length;
  const catCount = (cat: string) => (cat === 'Tümü' ? scripts.length : scripts.filter((s) => s.category === cat).length);

  const openLogsFor = (script: AdminScriptItem) => {
    const targetJob = activeJobs[script.name] || historyJobs.find((h) => h.name.toLowerCase() === script.name.toLowerCase());
    if (targetJob) {
      openTerminalForJob(targetJob);
    } else {
      setTerminalJobId(null);
      setTerminalJob(null);
      setTerminalLogs([`[Bilgi] ${script.title} için henüz kayıtlı günlük yok.`, `Başlatmak için "Çalıştır"a bas.`]);
      setIsTerminalOpen(true);
    }
  };

  const jobStatusTag = (status?: string) =>
    status === 'running' ? (
      <span className="ms-tag is-warn"><span className="ms-sdot is-warn is-live" /> Çalışıyor</span>
    ) : status === 'completed' ? (
      <span className="ms-tag is-ok"><Check /> Tamamlandı</span>
    ) : status ? (
      <span className="ms-tag is-bad">{status === 'cancelled' ? 'Durduruldu' : 'Hata'}</span>
    ) : null;

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <div className="flex flex-col md:flex-row md:items-center gap-2">
        <SearchBox value={searchQuery} onChange={setSearchQuery} placeholder="Betik adı, açıklama ya da etiket (slide, supabase, verify…)" count={`${filteredScripts.length} betik`} className="flex-1" />
        <div className="flex items-center gap-2">
          <button type="button" onClick={() => setIsTerminalOpen(true)} className="ms-btn" title="Canlı betik konsolunu aç">
            <FileCode /> Konsol
            {runningCount > 0 && <span className="ms-btn-badge">{runningCount}</span>}
          </button>
          <button type="button" onClick={() => loadScriptsData()} disabled={isLoading} className="ms-btn is-ghost" title="scripts/ klasörünü yeniden tarar; yeni betikler kendiliğinden listelenir">
            <RefreshCw className={isLoading ? 'animate-spin' : ''} /> {isLoading ? 'Taranıyor…' : 'Yeniden tara'}
          </button>
        </div>
      </div>

      <Panel flush title="Zincirler" icon={Zap} count={pipelines.length} desc="Birden çok betiği sırayla çalıştırır; bir adım hata verirse zincir durur.">
        <ul className="ms-rows">
          {pipelines.map((pipe) => {
            const running = terminalJob?.type === 'pipeline' && terminalJob?.pipelineId === pipe.id && terminalJob?.status === 'running';
            return (
              <li key={pipe.id} className="ms-row">
                <span className="ms-ricon is-accent"><Layers aria-hidden="true" /></span>
                <div className="ms-row-main">
                  <span className="ms-row-title">{cleanTitle(pipe.title)}</span>
                  <span className="ms-row-text">{pipe.description}</span>
                  <ol className="m-0 p-0 list-none flex flex-wrap items-center gap-1 pt-1">
                    {pipe.steps.map((st, idx) => (
                      <li key={idx} className="inline-flex items-center gap-1 text-[12px] text-ink-2">
                        {idx > 0 && <ArrowRight className="w-3 h-3 text-ink-3" aria-hidden="true" />}
                        <span className="h-6 px-2 rounded-md bg-canvas inline-flex items-center gap-1.5">
                          <span className="font-mono text-[11.5px] text-ink-3">{idx + 1}</span>
                          {cleanTitle(st.title || st.script)}
                        </span>
                      </li>
                    ))}
                  </ol>
                </div>
                <div className="ms-row-actions">
                  <button type="button" onClick={() => handleRunPipeline(pipe.id)} disabled={running} className={`ms-btn is-sm ${running ? 'is-warn' : 'is-primary'}`}>
                    {running ? <RefreshCw className="animate-spin" /> : <Play />} {running ? 'Çalışıyor…' : 'Başlat'}
                  </button>
                </div>
              </li>
            );
          })}
        </ul>
      </Panel>

      <ChipBar
        label="Kategori"
        value={selectedCategory}
        onChange={setSelectedCategory}
        options={categories.map((cat) => ({ id: cat, label: cat, n: catCount(cat) }))}
      />

      <Panel flush>
        {filteredScripts.length === 0 ? (
          <EmptyState icon={Search} title="Betik bulunamadı">Aramayı ya da kategoriyi değiştir.</EmptyState>
        ) : (
          <ul className="ms-rows">
            {filteredScripts.map((script) => {
              const activeJob = activeJobs[script.name];
              const running = Boolean(activeJob || runningJobName === script.name);
              const userArg = customArgs[script.name] !== undefined ? customArgs[script.name] : script.defaultArgs || '';
              return (
                <li key={script.name} className={`ms-row ${running ? 'bg-accent-soft/50' : ''}`}>
                  <span className={`ms-ricon ${running ? 'is-warn' : ''}`}><Code aria-hidden="true" /></span>
                  <div className="ms-row-main">
                    <span className="flex flex-wrap items-center gap-x-2 gap-y-1">
                      <span className="ms-row-title">{cleanTitle(script.title)}</span>
                      <span className="ms-tag">{RUNTIME_LABEL[script.runtime] || script.runtime}</span>
                      {script.isCustom && <span className="ms-tag is-accent">Yeni</span>}
                      {running && <span className="ms-tag is-warn"><span className="ms-sdot is-warn is-live" /> Çalışıyor</span>}
                    </span>
                    <span className="ms-row-text">{script.description}</span>
                    <span className="ms-row-meta">
                      <code className="font-mono text-[12px] text-ink-2">{script.name}</code>
                      {script.sizeBytes ? <span>{(script.sizeBytes / 1024).toFixed(1)} KB</span> : null}
                      {script.tags && script.tags.length > 0 && <span>{script.tags.map((t) => `#${t}`).join(' ')}</span>}
                    </span>
                    <span className="flex items-center gap-2 pt-1.5 max-w-[640px]">
                      <input
                        type="text"
                        value={userArg}
                        onChange={(e) => setCustomArgs((prev) => ({ ...prev, [script.name]: e.target.value }))}
                        placeholder="Argümanlar (isteğe bağlı): --all, --unverified …"
                        aria-label={`${script.title} argümanları`}
                        spellCheck={false}
                        className="ms-input is-sm is-mono flex-1"
                      />
                      {script.defaultArgs && userArg !== script.defaultArgs && (
                        <button type="button" onClick={() => setCustomArgs((prev) => ({ ...prev, [script.name]: script.defaultArgs || '' }))} className="ms-btn is-sm is-ghost" title={`Varsayılan: ${script.defaultArgs}`}>
                          Varsayılan
                        </button>
                      )}
                    </span>
                  </div>
                  <div className="ms-row-actions">
                    <button type="button" onClick={() => openLogsFor(script)} className="ms-btn is-sm is-ghost" title="Bu betiğin son günlüğü">
                      <Eye /> Günlük
                    </button>
                    {running && activeJob ? (
                      <button type="button" onClick={() => handleStopJob(activeJob.id)} className="ms-btn is-sm is-danger">
                        <Square /> Durdur
                      </button>
                    ) : (
                      <button type="button" onClick={() => handleRunScript(script.name)} disabled={running} className="ms-btn is-sm is-primary">
                        <Play /> Çalıştır
                      </button>
                    )}
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </Panel>

      <Drawer
        open={isTerminalOpen}
        onClose={() => setIsTerminalOpen(false)}
        wide
        label="Betik konsolu"
        title={terminalJob?.title || terminalJob?.name || 'Betik konsolu'}
        head={
          <span className="hidden sm:inline-flex items-center gap-1.5">
            {jobStatusTag(terminalJob?.status)}
            {terminalJob?.durationMs ? <span className="text-[12px] text-ink-3 tabular-nums">{(terminalJob.durationMs / 1000).toFixed(1)} sn</span> : null}
          </span>
        }
        foot={
          <>
            <button
              type="button"
              onClick={() => {
                navigator.clipboard.writeText(terminalLogs.join('\n'));
                setCopied(true);
                setTimeout(() => setCopied(false), 2000);
              }}
              className="ms-btn"
            >
              {copied ? <Check /> : <Copy />} {copied ? 'Kopyalandı' : 'Kopyala'}
            </button>
            <button type="button" onClick={() => setTerminalLogs([])} className="ms-btn">
              Temizle
            </button>
            {terminalJob?.status === 'running' && (
              <button type="button" onClick={() => handleStopJob(terminalJob.id)} className="ms-btn is-danger">
                <Square /> Durdur
              </button>
            )}
          </>
        }
      >
        <Switch checked={autoScroll} onChange={setAutoScroll} label="Yeni satırlara otomatik kaydır" />
        <pre className="ms-term flex-1 !max-h-none min-h-[50vh]" aria-live="polite">
          {terminalLogs.length === 0 ? (
            <span className="t">Henüz çıktı yok. Bir betik ya da zincir başlat.</span>
          ) : (
            terminalLogs.map((log, index) => (
              <div key={index} className={logTone(log)}>
                {log}
              </div>
            ))
          )}
          <div ref={logsEndRef} />
        </pre>
        {historyJobs.length > 0 && (
          <section className="ms-dsec">
            <h3>Son çalışmalar <span className="n">{historyJobs.length}</span></h3>
            <ul className="ms-dlist">
              {historyJobs.slice(0, 8).map((j) => (
                <li key={j.id} className="!p-0">
                  <button type="button" onClick={() => openTerminalForJob(j)} className="w-full flex items-center gap-2 px-2.5 py-2 text-left cursor-pointer hover:bg-field rounded-[10px]">
                    <span className="flex-1 min-w-0 truncate">{j.title || j.name}</span>
                    {jobStatusTag(j.status)}
                  </button>
                </li>
              ))}
            </ul>
          </section>
        )}
      </Drawer>
    </div>
  );
};
