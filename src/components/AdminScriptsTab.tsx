import React, { useState, useEffect, useRef } from 'react';
import {
  Play,
  Square,
  RefreshCw,
  Search,
  Zap,
  Layers,
  Copy,
  Eye,
  Code,
  Check,
  FileCode,
  ArrowRight,
} from 'lucide-react';
import {
  AdminScriptItem,
  AdminPipelineItem,
  AdminScriptJob
} from '../services/api';
import { YonetimApi } from '../services/api/yonetim';
import { BUNDLED_SCRIPTS, BUNDLED_PIPELINES } from '../data/bundledScripts';
import { toast } from './ui/Toast';
import { Panel, EmptyState, Switch, Drawer, logTone } from './manage/consoleUi';
import { PageActions, Toolbar, Tabs14, SearchField, DataTable, Pill, type Col } from './v14/pageKit';
import { BulkBar, useSelection } from './v14/manageKit';
import { guardedInterval } from '../services/net';

/**
 * Betikler (v14, canvas Betikler.dc.html): kategori sekmeleri + arama → zincirler → seçimli betik tablosu →
 * seçilenleri sırayla çalıştır (her biri bitmeden sonraki başlamaz; biri hata verirse sıra durur) → çıktı konsolu (Drawer).
 * Sunucu zinciri (runScriptPipeline) yalnız tanımlı zincir kimliği alır; serbest seçim tek tek runScript ile yürür.
 */
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

  const scriptSel = useSelection<string>();
  const [seq, setSeq] = useState<{ i: number; n: number; name: string } | null>(null);
  const seqStop = useRef(false);

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
        const res = await YonetimApi.getScriptJobStatus(terminalJobId);
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
    // Önceki durum isteği bitmeden yenisi atılmaz
    const stop = guardedInterval(fetchStatus, 1200);

    return () => {
      stop();
      if (pollingRef.current) clearInterval(pollingRef.current);
    };
  }, [terminalJobId]);

  const loadScriptsData = async (silent: boolean = false) => {
    if (!silent) setIsLoading(true);
    try {
      const res = await YonetimApi.getScriptsList();
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
      const res = await YonetimApi.runScript(scriptName, args, adminEmail);
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
      const res = await YonetimApi.runScriptPipeline(pipelineId, adminEmail);
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
      const res = await YonetimApi.stopScriptJob(jobId, adminEmail);
      if (res.success) {
        setFeedback({ text: 'İşlem sonlandırıldı.', type: 'info' });
        await loadScriptsData(true);
      }
    } catch (e: any) {
      setFeedback({ text: 'Durdurma hatası: ' + e.message, type: 'error' });
    }
  };

  /** Seçilen betikleri sırayla çalıştırır: her işin bitmesi beklenir; hata ya da durdurma sırayı keser */
  const runSequence = async () => {
    const names = scripts.filter((x) => scriptSel.has(x.name)).map((x) => x.name);
    if (!names.length) return;
    seqStop.current = false;
    let ok = 0;
    let bad = 0;
    for (let i = 0; i < names.length; i++) {
      if (seqStop.current) break;
      const name = names[i];
      setSeq({ i: i + 1, n: names.length, name });
      setRunningJobName(name);
      try {
        const res = await YonetimApi.runScript(name, customArgs[name] || '', adminEmail);
        if (!res.success || !res.job?.id) {
          bad++;
          setFeedback({ text: `${name} başlatılamadı: ${res.message}`, type: 'error' });
          break;
        }
        setTerminalJobId(res.job.id);
        setTerminalJob(res.job);
        setTerminalLogs(res.job.logs || []);
        setIsTerminalOpen(true);
        let status = res.job.status;
        while (status === 'running') {
          await new Promise((r) => setTimeout(r, 1500));
          const st = await YonetimApi.getScriptJobStatus(res.job.id);
          if (st.success && st.job) status = st.job.status;
        }
        if (status === 'completed') ok++;
        else {
          bad++;
          break;
        }
      } catch (e: any) {
        bad++;
        setFeedback({ text: `${name}: ${e?.message || 'hata'}`, type: 'error' });
        break;
      }
    }
    setSeq(null);
    setRunningJobName(null);
    await loadScriptsData(true);
    const msg = `${ok} başarılı, ${bad} hata${seqStop.current ? ' (durduruldu)' : ''}.`;
    if (bad) toast.error(msg);
    else toast.success(msg);
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

  const stop = (e: React.SyntheticEvent) => e.stopPropagation();
  const scriptCols: Col<AdminScriptItem>[] = [
    {
      key: 'title',
      label: 'Betik',
      render: (script) => (
        <span className="flex flex-col gap-0.5 min-w-0" style={{ maxWidth: 360 }}>
          <span className="font-semibold text-ink truncate">{cleanTitle(script.title)}</span>
          <span className="text-sm text-ink-3 truncate" title={script.description}>{script.description}</span>
          <code className="font-mono text-xs text-ink-2 truncate">{script.name}{script.tags?.length ? ` · ${script.tags.map((t) => `#${t}`).join(' ')}` : ''}</code>
        </span>
      ),
    },
    { key: 'rt', label: 'Ortam', render: (script) => <span className="flex flex-wrap gap-1"><Pill>{RUNTIME_LABEL[script.runtime] || script.runtime}</Pill>{script.isCustom && <Pill tone="acc">Yeni</Pill>}</span> },
    {
      key: 'state',
      label: 'Durum',
      render: (script) => (activeJobs[script.name] || runningJobName === script.name ? <Pill tone="warn">Çalışıyor</Pill> : <span className="text-ink-3">Hazır</span>),
    },
    {
      key: 'args',
      label: 'Argümanlar',
      render: (script) => {
        const userArg = customArgs[script.name] !== undefined ? customArgs[script.name] : script.defaultArgs || '';
        return (
          <span className="flex items-center gap-1" onClick={stop} onKeyDown={stop}>
            <input
              type="text"
              value={userArg}
              onChange={(e) => setCustomArgs((prev) => ({ ...prev, [script.name]: e.target.value }))}
              placeholder="--all …"
              aria-label={`${script.title} argümanları`}
              spellCheck={false}
              className="ms-input is-sm is-mono"
              style={{ width: 180 }}
            />
            {script.defaultArgs && userArg !== script.defaultArgs && (
              <button type="button" onClick={() => setCustomArgs((prev) => ({ ...prev, [script.name]: script.defaultArgs || '' }))} className="m14-btn ghost" title={`Varsayılan: ${script.defaultArgs}`}>
                Varsayılan
              </button>
            )}
          </span>
        );
      },
    },
    {
      key: 'act',
      label: <span className="sr-only">İşlemler</span>,
      render: (script) => {
        const activeJob = activeJobs[script.name];
        const running = Boolean(activeJob || runningJobName === script.name);
        return (
          <span className="flex items-center justify-end gap-1" onClick={stop} onKeyDown={stop}>
            <button type="button" onClick={() => openLogsFor(script)} className="m14-btn ghost" title="Bu betiğin son günlüğü">
              <Eye aria-hidden="true" /> Günlük
            </button>
            {running && activeJob ? (
              <button type="button" onClick={() => handleStopJob(activeJob.id)} className="m14-btn danger">
                <Square aria-hidden="true" /> Durdur
              </button>
            ) : (
              <button type="button" onClick={() => handleRunScript(script.name)} disabled={running || !!seq} className="m14-btn primary">
                <Play aria-hidden="true" /> Çalıştır
              </button>
            )}
          </span>
        );
      },
    },
  ];

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <PageActions note={seq ? `Sırayla çalışıyor · ${seq.i} / ${seq.n} · ${seq.name}` : 'Seçilen betikler sırayla çalışır; biri hata verirse sıra durur.'}>
        <button type="button" onClick={() => setIsTerminalOpen(true)} className="m14-btn" title="Canlı betik konsolunu aç">
          <FileCode aria-hidden="true" /> Çıktı konsolu
          {runningCount > 0 && <span className="ms-btn-badge">{runningCount}</span>}
        </button>
        <button type="button" onClick={() => loadScriptsData()} disabled={isLoading} className="m14-btn ghost" title="scripts/ klasörünü yeniden tarar; yeni betikler kendiliğinden listelenir">
          <RefreshCw className={isLoading ? 'animate-spin' : ''} aria-hidden="true" /> {isLoading ? 'Taranıyor…' : 'Yeniden tara'}
        </button>
      </PageActions>

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
                      <li key={idx} className="inline-flex items-center gap-1 text-xs text-ink-2">
                        {idx > 0 && <ArrowRight className="w-3 h-3 text-ink-3" aria-hidden="true" />}
                        <span className="h-6 px-2 rounded-md bg-canvas inline-flex items-center gap-1.5">
                          <span className="font-mono text-xs text-ink-3">{idx + 1}</span>
                          {cleanTitle(st.title || st.script)}
                        </span>
                      </li>
                    ))}
                  </ol>
                </div>
                <div className="ms-row-actions">
                  <button type="button" onClick={() => handleRunPipeline(pipe.id)} disabled={running} className={`m14-btn ${running ? '' : 'primary'}`}>
                    {running ? <RefreshCw className="animate-spin" /> : <Play />} {running ? 'Çalışıyor…' : 'Başlat'}
                  </button>
                </div>
              </li>
            );
          })}
        </ul>
      </Panel>

      <Toolbar>
        <Tabs14 label="Kategori" value={selectedCategory} onChange={setSelectedCategory} options={categories.map((cat) => ({ id: cat, label: cat, n: catCount(cat) }))} />
        <SearchField value={searchQuery} onChange={setSearchQuery} placeholder="Betik adı, açıklama ya da etiket" label="Betik ara" />
        <span className="pk14-note">{filteredScripts.length} betik</span>
      </Toolbar>

      <BulkBar
        count={scriptSel.count}
        noun="betik"
        busy={!!seq}
        onClear={scriptSel.clear}
        actions={[{ label: 'Sırayla çalıştır', kind: 'main', run: runSequence }]}
      />
      {seq && (
        <div className="pk14-actions">
          <p className="pk14-note" aria-live="polite">Çalışıyor · {seq.i} / {seq.n}: {seq.name}</p>
          <div className="pk14-actions-btns">
            <button type="button" className="m14-btn danger" onClick={() => { seqStop.current = true; if (terminalJob?.status === 'running') void handleStopJob(terminalJob.id); }}>
              <Square aria-hidden="true" /> Sırayı durdur
            </button>
          </div>
        </div>
      )}

      {filteredScripts.length === 0 ? (
        <EmptyState icon={Search} title="Betik bulunamadı">Aramayı ya da kategoriyi değiştir.</EmptyState>
      ) : (
        <DataTable rows={filteredScripts} cols={scriptCols} rowKey={(x) => x.name} onOpen={openLogsFor} selection={scriptSel} activeKey={seq?.name || null} minWidth={880} />
      )}

      <Drawer
        open={isTerminalOpen}
        onClose={() => setIsTerminalOpen(false)}
        wide
        label="Betik konsolu"
        title={terminalJob?.title || terminalJob?.name || 'Betik konsolu'}
        head={
          <span className="hidden sm:inline-flex items-center gap-1.5">
            {jobStatusTag(terminalJob?.status)}
            {terminalJob?.durationMs ? <span className="text-xs text-ink-3 tabular-nums">{(terminalJob.durationMs / 1000).toFixed(1)} sn</span> : null}
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
