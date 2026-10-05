#!/usr/bin/env node

/**
 * MedSoru Central Script & Automation Runner Engine
 * ----------------------------------------------------
 * Bu script; mevcut ve gelecekte oluşturulacak TÜM scriptlerin dinamik taranmasını,
 * manuel veya zincirleme (pipeline) olarak çalıştırılmasını, loglarının toplanmasını
 * ve arka planda otomasyon olarak tetiklenmesini sağlar.
 *
 * Kullanım (CLI):
 *   node scripts/automation-runner.mjs --list
 *   node scripts/automation-runner.mjs --run <script-adı> [--args "..."]
 *   node scripts/automation-runner.mjs --pipeline <pipeline-id>
 *   node scripts/automation-runner.mjs --schedule [dakika]
 */

import fs from 'fs';
import path from 'path';
import { spawn, exec } from 'child_process';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');
const SCRIPTS_DIR = path.resolve(PROJECT_ROOT, 'scripts');
const LOGS_DIR = path.resolve(PROJECT_ROOT, 'data', 'script_logs');
const META_FILE = path.resolve(SCRIPTS_DIR, 'scripts-meta.json');
const HISTORY_FILE = path.resolve(PROJECT_ROOT, 'data', 'script_jobs_history.json');

// Ensure log directory exists
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

// In-Memory Jobs Store
const activeJobs = new Map();
const recentJobs = [];
const MAX_HISTORY = 50;

// Load persisted history if available
try {
  if (fs.existsSync(HISTORY_FILE)) {
    const raw = fs.readFileSync(HISTORY_FILE, 'utf8');
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      recentJobs.push(...parsed.slice(-MAX_HISTORY));
    }
  }
} catch (_) {}

function saveJobsHistory() {
  try {
    const historyToSave = recentJobs.slice(-MAX_HISTORY).map((j) => ({
      id: j.id,
      name: j.name,
      type: j.type,
      args: j.args,
      status: j.status,
      startedAt: j.startedAt,
      completedAt: j.completedAt,
      durationMs: j.durationMs,
      exitCode: j.exitCode,
      requestedBy: j.requestedBy,
      logSummary: j.logs?.slice(-10).join('\n') || '',
    }));
    fs.writeFileSync(HISTORY_FILE, JSON.stringify(historyToSave, null, 2), 'utf8');
  } catch (_) {}
}

/**
 * Predefined Automation Pipelines
 */
export const AUTOMATION_PIPELINES = [
  {
    id: 'full-sync-and-cloud',
    title: '⚡ Tam Senkronizasyon & Bulut Pipeline',
    description: 'Drive\'dan çıkmış ve slaytları indirir, CPU ile okur, slaytları denetler, eşleştirir, veritabanı JSON üretir ve Supabase/Firestore\'a aktarır.',
    category: 'Otomasyon & Pipeline',
    steps: [
      { script: 'meds-local-sync.mjs', args: '', title: '1. Drive İndir & OCR İşle' },
      { script: 'audit-and-disconnect-faulty-slides.mjs', args: '', title: '2. Slayt İlişkilerini Denetle' },
      { script: 'match-and-link-lecture-slides.mjs', args: '', title: '3. Slaytları Eşleştir & Vurgula' },
      { script: 'build-database-json.mjs', args: '', title: '4. Veritabanı JSON Derle' },
      { script: 'sync-database-json-to-cloud.mjs', args: '', title: '5. Buluta Aktar (Supabase + Firestore)' },
    ],
  },
  {
    id: 'ai-verify-and-cloud',
    title: '🤖 AI Doğrulama & Bulut Eşitleme Pipeline',
    description: 'Doğrulanmamış soruları tıp AI modeliyle çözer, database_json üretir ve bulut veritabanlarına eşitler.',
    category: 'Otomasyon & Pipeline',
    steps: [
      { script: 'verify-question-answers.mjs', args: '--unverified', title: '1. Soruları AI ile Doğrula' },
      { script: 'build-database-json.mjs', args: '', title: '2. Veritabanı JSON Derle' },
      { script: 'sync-database-json-to-cloud.mjs', args: '', title: '3. Buluta Aktar' },
    ],
  },
  {
    id: 'deep-triple-slide-audit-and-heal',
    title: '🛡️ 3 Aşamalı Slayt Denetim & Otonom İyileştirme',
    description: 'Soruların gerçek tıbbi branşlarını belirler, soru dosyalarıyla kurulan hatalı bağları keser, 3 aşamalı katı kuralla amfi slaytlarını eşleştirir ve buluta senkronize eder.',
    category: 'Otomasyon & Pipeline',
    steps: [
      { script: 'deep-triple-slide-matcher.mjs', args: '', title: '1. 3 Aşamalı Derin Slayt Eşleştirme & Temizlik' },
      { script: 'self-healing-auditor.mjs', args: '', title: '2. Otonom Sağlık Denetimi' },
      { script: 'sync-all-to-supabase.mjs', args: '', title: '3. Supabase Senkronizasyonu' },
      { script: 'sync-all-to-firestore.mjs', args: '', title: '4. Firestore Senkronizasyonu' },
    ],
  },
  {
    id: 'slides-audit-and-rematch',
    title: '🔍 Slayt Denetim & Yeniden Eşleştirme',
    description: 'Hatalı slayt eşleşmelerini temizler, soruları ders notları slaytlarıyla yeniden eşleştirir ve buluta kaydeder.',
    category: 'Otomasyon & Pipeline',
    steps: [
      { script: 'deep-triple-slide-matcher.mjs', args: '', title: '1. Slaytları 3 Aşamalı Eşleştir' },
      { script: 'sync-database-json-to-cloud.mjs', args: '', title: '2. Buluta Aktar' },
    ],
  },
  {
    id: 'build-and-sync-json',
    title: '📦 JSON Derle & Bulut Senkronizasyonu',
    description: 'Tüm güncel soru havuzunu tek hamlede database_json formatına çevirip Supabase ve Firestore\'a gönderir.',
    category: 'Otomasyon & Pipeline',
    steps: [
      { script: 'build-database-json.mjs', args: '', title: '1. database_json Derle' },
      { script: 'sync-database-json-to-cloud.mjs', args: '', title: '2. Buluta Yükle' },
    ],
  },
  {
    id: 'cloud-backup-all',
    title: '☁️ Çift Bulut Yedekleme (Supabase + Firestore)',
    description: 'Tüm soru ve slayt verilerini hem Supabase PostgreSQL hem de Firestore veritabanlarına tam yedekler.',
    category: 'Otomasyon & Pipeline',
    steps: [
      { script: 'sync-all-to-supabase.mjs', args: '', title: '1. Supabase PostgreSQL Eşitle' },
      { script: 'sync-all-to-firestore.mjs', args: '', title: '2. Firestore NoSQL Eşitle' },
    ],
  },
  {
    id: 'phase5-multi-ai-consensus',
    title: '🧠 Faz 5: Çoklu AI Konsensüsü & Slayt İğne-Delik Tespiti',
    description: 'Yerel RTX 4060 GPU (Gemma3) ve Bulut AI eşzamanlı konsensüsü ile pedagojik analiz, tıbbi varlık çıkarımı ve slayt eşleştirmesi.',
    category: 'Otomasyon & Pipeline',
    steps: [
      { script: 'advanced_ai/multi_ai_consensus_phase5.py', args: '', title: '1. Çoklu AI Konsensüsü Yürüt' },
    ],
  },
  {
    id: 'phase6-deep-metadata-generator',
    title: '🏷️ Faz 6: Derin Tıbbi Metadata & Hiper-Etiket Motoru',
    steps: [
      { script: 'advanced_ai/deep_metadata_generator_phase6.py', args: '', title: '1. Çoklu AI Dinamik Metadata Üretimi' },
    ],
  },
  {
    id: 'phase7-microagent-storyteller',
    title: '📖 Faz 7: 5 Adımlı Mikro-Ajans Tıbbi Hikaye & Modelleme',
    description: 'Yerel GPU bilişsel yükünü 5 atomik mikro-adıma bölerek halüsinasyonsuz, çeldirici otopsili ve pedagojik klinik hikayeler üretir.',
    category: 'Otomasyon & Pipeline',
    steps: [
      { script: 'advanced_ai/microagent_storyteller_phase7.py', args: '', title: '1. 5 Adımlı Mikro-Ajans Modelleme ve 100 Altın Örnek' },
    ],
  },
];


/**
 * Read known metadata from scripts-meta.json
 */
function loadKnownMeta() {
  try {
    if (fs.existsSync(META_FILE)) {
      const parsed = JSON.parse(fs.readFileSync(META_FILE, 'utf8'));
      if (Array.isArray(parsed.scripts)) {
        const map = new Map();
        for (const s of parsed.scripts) {
          map.set(s.name.toLowerCase(), s);
        }
        return map;
      }
    }
  } catch (e) {
    console.warn('[AutomationRunner] Meta file load warning:', e.message);
  }
  return new Map();
}

/**
 * Determine runner command & shell wrapper based on file extension
 */
export function getScriptRunnerInfo(filename) {
  const ext = path.extname(filename).toLowerCase();
  switch (ext) {
    case '.mjs':
    case '.cjs':
    case '.js':
      return { runtime: 'node', command: 'node', isShell: false };
    case '.ts':
      return { runtime: 'tsx', command: 'npx', prefixArgs: ['tsx'], isShell: process.platform === 'win32' };
    case '.py':
      return { runtime: 'python', command: process.platform === 'win32' ? 'python' : 'python3', isShell: false };
    case '.sh':
      return { runtime: 'bash', command: 'bash', isShell: false };
    case '.bat':
    case '.cmd':
      return { runtime: 'batch', command: 'cmd.exe', prefixArgs: ['/c'], isShell: true };
    case '.ps1':
      return {
        runtime: 'powershell',
        command: 'powershell.exe',
        prefixArgs: ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File'],
        isShell: true,
      };
    default:
      return null;
  }
}

/**
 * Infer human-friendly title and description for any unknown/future script
 */
function inspectScriptContent(filePath, filename) {
  let title = filename
    .replace(/\.[^/.]+$/, '')
    .replace(/[-_]/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
  let description = `Özel betik: ${filename}`;
  let category = 'Özel / Yeni Script';

  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const firstLines = content.split('\n').slice(0, 30).join('\n');

    // Check for comment descriptions
    const descMatch =
      firstLines.match(/(?:\/\*\*|\/\*|\/\/|#|::|rem)\s*(?:description|açıklama|özet)?[:\-]?\s*([^\r\n*]+)/i) ||
      firstLines.match(/(?:\/\*\*|\/\*)\s*\n\s*\*\s*([^\r\n*]+)/);

    if (descMatch && descMatch[1] && descMatch[1].trim().length > 5) {
      description = descMatch[1].trim();
    }

    // Auto-categorize based on keywords
    const lower = (filename + ' ' + content.slice(0, 500)).toLowerCase();
    if (lower.includes('slide') || lower.includes('slayt')) {
      category = 'Slayt & Eşleştirme';
    } else if (lower.includes('supabase') || lower.includes('firestore') || lower.includes('database') || lower.includes('sync')) {
      category = 'Veritabanı & Bulut';
    } else if (lower.includes('verify') || lower.includes('redact') || lower.includes('gemini') || lower.includes('ai')) {
      category = 'AI & Doğrulama';
    } else if (lower.includes('ocr') || lower.includes('soru') || lower.includes('pdf') || lower.includes('clean')) {
      category = 'OCR & Veri Ayıklama';
    } else if (lower.includes('tunnel') || lower.includes('cloudflare') || lower.includes('port')) {
      category = 'Ağ & Tünel';
    } else if (lower.includes('service') || lower.includes('notify') || lower.includes('daemon')) {
      category = 'Sistem & Servis';
    }
  } catch (_) {}

  return { title, description, category };
}

/**
 * Dynamically scan SCRIPTS_DIR: Discovers all existing AND future scripts!
 */
export function getAllScripts() {
  const knownMeta = loadKnownMeta();
  const result = [];

  if (!fs.existsSync(SCRIPTS_DIR)) {
    return result;
  }

  const entries = fs.readdirSync(SCRIPTS_DIR, { withFileTypes: true });

  for (const entry of entries) {
    if (!entry.isFile()) continue;

    const filename = entry.name;
    // Don't list scripts-meta.json, automation-runner itself, or lock/hidden files
    if (
      filename.startsWith('.') ||
      filename.endsWith('.json') ||
      filename.endsWith('.log') ||
      filename === 'automation-runner.mjs'
    ) {
      continue;
    }

    const runner = getScriptRunnerInfo(filename);
    if (!runner) continue; // Unsupported extension

    const fullPath = path.join(SCRIPTS_DIR, filename);
    let stat = null;
    try {
      stat = fs.statSync(fullPath);
    } catch (_) {}

    const known = knownMeta.get(filename.toLowerCase());

    if (known) {
      result.push({
        name: filename,
        title: known.title || filename,
        category: known.category || 'Genel',
        description: known.description || '',
        defaultArgs: known.defaultArgs || '',
        tags: known.tags || [],
        danger: Boolean(known.danger),
        runtime: runner.runtime,
        sizeBytes: stat?.size || 0,
        modifiedAt: stat?.mtime ? stat.mtime.toISOString() : null,
        isCustom: false,
      });
    } else {
      // Discovered dynamically (New or Future script!)
      const inferred = inspectScriptContent(fullPath, filename);
      result.push({
        name: filename,
        title: inferred.title,
        category: inferred.category,
        description: inferred.description,
        defaultArgs: '',
        tags: ['özel', 'dinamik-keşif', runner.runtime],
        danger: false,
        runtime: runner.runtime,
        sizeBytes: stat?.size || 0,
        modifiedAt: stat?.mtime ? stat.mtime.toISOString() : null,
        isCustom: true,
      });
    }
  }

  // Sort by category then title
  result.sort((a, b) => {
    if (a.category !== b.category) return a.category.localeCompare(b.category, 'tr');
    return a.title.localeCompare(b.title, 'tr');
  });

  return result;
}

/**
 * Parse string arguments safely into array
 */
function parseArgs(argsStr = '') {
  if (!argsStr || typeof argsStr !== 'string') return [];
  const regex = /[^\s"']+|"([^"]*)"|'([^']*)'/g;
  const matches = [];
  let match;
  while ((match = regex.exec(argsStr)) !== null) {
    matches.push(match[1] || match[2] || match[0]);
  }
  return matches;
}

/**
 * Start execution of a single script
 */
export function startScriptJob(scriptName, rawArgs = '', requestedBy = 'admin') {
  const allScripts = getAllScripts();
  const scriptItem = allScripts.find((s) => s.name.toLowerCase() === scriptName.toLowerCase());

  if (!scriptItem) {
    throw new Error(`Belirtilen script bulunamadı: ${scriptName}`);
  }

  const scriptPath = path.join(SCRIPTS_DIR, scriptItem.name);
  if (!fs.existsSync(scriptPath)) {
    throw new Error(`Script dosyası diskte bulunamadı: ${scriptPath}`);
  }

  const runner = getScriptRunnerInfo(scriptItem.name);
  if (!runner) {
    throw new Error(`Bu dosya uzantısı için çalıştırıcı bulunamadı: ${scriptItem.name}`);
  }

  const jobId = `job_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
  const logFile = path.join(LOGS_DIR, `${jobId}.log`);
  const logStream = fs.createWriteStream(logFile, { flags: 'a', encoding: 'utf8' });

  const parsedUserArgs = parseArgs(rawArgs || scriptItem.defaultArgs || '');
  const finalArgs = [...(runner.prefixArgs || []), scriptPath, ...parsedUserArgs];

  const job = {
    id: jobId,
    type: 'single',
    name: scriptItem.name,
    title: scriptItem.title,
    category: scriptItem.category,
    args: rawArgs,
    command: `${runner.command} ${finalArgs.join(' ')}`,
    status: 'running',
    startedAt: new Date().toISOString(),
    completedAt: null,
    durationMs: 0,
    exitCode: null,
    requestedBy,
    logs: [],
    process: null,
    logFile,
  };

  function appendLog(line) {
    const clean = line.replace(/\r\n/g, '\n');
    const timestamp = new Date().toLocaleTimeString('tr-TR');
    const formatted = `[${timestamp}] ${clean}`;
    job.logs.push(formatted);
    if (job.logs.length > 2000) job.logs.shift(); // circular buffer

    try {
      logStream.write(formatted + '\n');
    } catch (_) {}
  }

  appendLog(`🚀 [BAŞLADI] ${scriptItem.title} (${scriptItem.name}) yürütülüyor...`);
  appendLog(`💻 Çalışma Dizini: ${PROJECT_ROOT}`);
  appendLog(`⚙️ Komut: ${job.command}`);
  appendLog('------------------------------------------------------------');

  const startTime = Date.now();

  try {
    const child = spawn(runner.command, finalArgs, {
      cwd: PROJECT_ROOT,
      shell: runner.isShell,
      env: { ...process.env, FORCE_COLOR: '1' },
    });

    job.process = child;
    activeJobs.set(jobId, job);

    child.stdout.on('data', (chunk) => {
      const text = chunk.toString('utf8');
      const lines = text.split('\n').filter((l) => l.trim().length > 0);
      for (const line of lines) appendLog(line);
    });

    child.stderr.on('data', (chunk) => {
      const text = chunk.toString('utf8');
      const lines = text.split('\n').filter((l) => l.trim().length > 0);
      for (const line of lines) appendLog(`[STDERR] ${line}`);
    });

    child.on('error', (err) => {
      appendLog(`❌ [HATA]: ${err.message}`);
      job.status = 'failed';
      job.completedAt = new Date().toISOString();
      job.durationMs = Date.now() - startTime;
      job.exitCode = -1;
      logStream.end();
      activeJobs.delete(jobId);
      recentJobs.unshift(job);
      saveJobsHistory();
    });

    child.on('close', (code) => {
      const isSuccess = code === 0;
      job.status = isSuccess ? 'completed' : 'failed';
      job.completedAt = new Date().toISOString();
      job.durationMs = Date.now() - startTime;
      job.exitCode = code;

      appendLog('------------------------------------------------------------');
      if (isSuccess) {
        appendLog(`✅ [BAŞARILI] İşlem tamamlandı. Süre: ${(job.durationMs / 1000).toFixed(1)} sn.`);
      } else {
        appendLog(`⚠️ [UYARI] İşlem çıkış kodu ${code} ile sonlandı. Süre: ${(job.durationMs / 1000).toFixed(1)} sn.`);
      }

      logStream.end();
      activeJobs.delete(jobId);
      recentJobs.unshift(job);
      saveJobsHistory();
    });
  } catch (err) {
    appendLog(`❌ [BAŞLATILAMADI]: ${err.message}`);
    job.status = 'failed';
    job.completedAt = new Date().toISOString();
    job.durationMs = Date.now() - startTime;
    job.exitCode = -1;
    logStream.end();
    recentJobs.unshift(job);
    saveJobsHistory();
  }

  return {
    id: job.id,
    name: job.name,
    title: job.title,
    status: job.status,
    startedAt: job.startedAt,
    command: job.command,
  };
}

/**
 * Start execution of a pipeline (chain of multiple scripts)
 */
export async function startPipelineJob(pipelineId, requestedBy = 'admin') {
  const pipeline = AUTOMATION_PIPELINES.find((p) => p.id === pipelineId);
  if (!pipeline) {
    throw new Error(`Pipeline bulunamadı: ${pipelineId}`);
  }

  const jobId = `pipe_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
  const logFile = path.join(LOGS_DIR, `${jobId}.log`);
  const logStream = fs.createWriteStream(logFile, { flags: 'a', encoding: 'utf8' });

  const job = {
    id: jobId,
    type: 'pipeline',
    pipelineId: pipeline.id,
    name: pipeline.id,
    title: pipeline.title,
    category: pipeline.category,
    status: 'running',
    startedAt: new Date().toISOString(),
    completedAt: null,
    durationMs: 0,
    exitCode: 0,
    requestedBy,
    logs: [],
    currentStepIndex: 0,
    totalSteps: pipeline.steps.length,
    activeChildProcess: null,
    logFile,
  };

  function appendLog(line) {
    const clean = line.replace(/\r\n/g, '\n');
    const timestamp = new Date().toLocaleTimeString('tr-TR');
    const formatted = `[${timestamp}] ${clean}`;
    job.logs.push(formatted);
    if (job.logs.length > 3000) job.logs.shift();

    try {
      logStream.write(formatted + '\n');
    } catch (_) {}
  }

  appendLog(`🌟 [PIPELINE BAŞLADI] ${pipeline.title}`);
  appendLog(`ℹ️ ${pipeline.description}`);
  appendLog(`📊 Toplam ${pipeline.steps.length} adım icra edilecek.`);
  appendLog('============================================================');

  activeJobs.set(jobId, job);
  const startTime = Date.now();

  // Async sequence runner
  (async () => {
    let failed = false;

    for (let i = 0; i < pipeline.steps.length; i++) {
      if (job.status === 'cancelled') {
        appendLog(`⏹ Pipeline kullanıcı tarafından iptal edildi.`);
        break;
      }

      const step = pipeline.steps[i];
      job.currentStepIndex = i;
      appendLog(`\n▶️ [Adım ${i + 1}/${pipeline.steps.length}]: ${step.title || step.script}`);

      const runner = getScriptRunnerInfo(step.script);
      if (!runner) {
        appendLog(`❌ Adım çalıştırılamadı: Geçersiz dosya formatı (${step.script})`);
        failed = true;
        break;
      }

      const scriptPath = path.join(SCRIPTS_DIR, step.script);
      const parsedArgs = parseArgs(step.args || '');
      const finalArgs = [...(runner.prefixArgs || []), scriptPath, ...parsedArgs];

      const stepCode = await new Promise((resolve) => {
        try {
          const child = spawn(runner.command, finalArgs, {
            cwd: PROJECT_ROOT,
            shell: runner.isShell,
            env: { ...process.env, FORCE_COLOR: '1' },
          });

          job.activeChildProcess = child;

          child.stdout.on('data', (d) => {
            for (const l of d.toString('utf8').split('\n').filter((x) => x.trim())) {
              appendLog(`  ${l}`);
            }
          });

          child.stderr.on('data', (d) => {
            for (const l of d.toString('utf8').split('\n').filter((x) => x.trim())) {
              appendLog(`  [STDERR] ${l}`);
            }
          });

          child.on('error', (err) => {
            appendLog(`❌ Adım yürütülürken hata: ${err.message}`);
            resolve(-1);
          });

          child.on('close', (code) => {
            resolve(code);
          });
        } catch (err) {
          appendLog(`❌ Spawn hatası: ${err.message}`);
          resolve(-1);
        }
      });

      if (stepCode !== 0) {
        appendLog(`❌ [Adım Başarısız]: ${step.script} çıkış kodu: ${stepCode}`);
        failed = true;
        job.exitCode = stepCode;
        break;
      } else {
        appendLog(`✓ [Adım Tamamlandı]: ${step.title || step.script}`);
      }
    }

    job.completedAt = new Date().toISOString();
    job.durationMs = Date.now() - startTime;
    job.status = failed ? 'failed' : (job.status === 'cancelled' ? 'cancelled' : 'completed');

    appendLog('============================================================');
    if (job.status === 'completed') {
      appendLog(`🎉 [PIPELINE BAŞARIYLA TAMAMLANDI] Toplam Süre: ${(job.durationMs / 1000).toFixed(1)} sn.`);
    } else {
      appendLog(`⚠️ [PIPELINE SONLANDI] Durum: ${job.status}, Süre: ${(job.durationMs / 1000).toFixed(1)} sn.`);
    }

    logStream.end();
    activeJobs.delete(jobId);
    recentJobs.unshift(job);
    saveJobsHistory();
  })();

  return {
    id: job.id,
    title: job.title,
    status: job.status,
    startedAt: job.startedAt,
    totalSteps: job.totalSteps,
  };
}

/**
 * Kill running process cleanly
 */
export function killJob(jobId) {
  const job = activeJobs.get(jobId);
  if (!job) return false;

  job.status = 'cancelled';
  const proc = job.process || job.activeChildProcess;

  if (proc && proc.pid) {
    try {
      if (process.platform === 'win32') {
        exec(`taskkill /pid ${proc.pid} /f /t`, () => {});
      } else {
        proc.kill('SIGTERM');
      }
    } catch (_) {}
  }
  return true;
}

/**
 * Get Job Status & Logs
 */
export function getJob(jobId) {
  const active = activeJobs.get(jobId);
  if (active) {
    return {
      id: active.id,
      name: active.name,
      title: active.title,
      type: active.type,
      status: active.status,
      startedAt: active.startedAt,
      completedAt: active.completedAt,
      durationMs: active.durationMs || Date.now() - new Date(active.startedAt).getTime(),
      exitCode: active.exitCode,
      currentStepIndex: active.currentStepIndex,
      totalSteps: active.totalSteps,
      logs: active.logs,
      requestedBy: active.requestedBy,
    };
  }

  const past = recentJobs.find((j) => j.id === jobId);
  if (past) {
    // If logs not fully in memory, read from log file
    let logs = past.logs;
    if ((!logs || logs.length === 0) && past.logFile && fs.existsSync(past.logFile)) {
      try {
        logs = fs.readFileSync(past.logFile, 'utf8').split('\n');
      } catch (_) {}
    }
    return { ...past, logs: logs || [] };
  }

  return null;
}

/**
 * Get all active and recent jobs summary
 */
export function getAllJobs() {
  const activeList = Array.from(activeJobs.values()).map((j) => ({
    id: j.id,
    name: j.name,
    title: j.title,
    type: j.type,
    status: j.status,
    startedAt: j.startedAt,
    durationMs: Date.now() - new Date(j.startedAt).getTime(),
    currentStepIndex: j.currentStepIndex,
    totalSteps: j.totalSteps,
    requestedBy: j.requestedBy,
    lastLog: j.logs[j.logs.length - 1] || '',
  }));

  const pastList = recentJobs.slice(0, 20).map((j) => ({
    id: j.id,
    name: j.name,
    title: j.title,
    type: j.type,
    status: j.status,
    startedAt: j.startedAt,
    completedAt: j.completedAt,
    durationMs: j.durationMs,
    exitCode: j.exitCode,
    requestedBy: j.requestedBy,
    lastLog: j.logs ? j.logs[j.logs.length - 1] : '',
  }));

  return { active: activeList, history: pastList };
}

// -------------------------------------------------------------
// CLI Execution Handler
// -------------------------------------------------------------
if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(__filename)) {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.length === 0) {
    console.log(`
=============================================================
  MedSoru Merkezi Otomasyon & Script Yöneticisi (CLI)
=============================================================
Kullanım:
  node scripts/automation-runner.mjs --list
      Mevcut ve yeni eklenen tüm scriptleri listeler.

  node scripts/automation-runner.mjs --pipelines
      Kayıtlı zincirleme otomasyonları (pipeline) listeler.

  node scripts/automation-runner.mjs --run <script-adı> [--args "<argümanlar>"]
      Belirtilen scripti çalıştırır ve canlı logları ekrana basar.
      Örnek: node scripts/automation-runner.mjs --run verify-question-answers.mjs --args "--unverified"

  node scripts/automation-runner.mjs --pipeline <pipeline-id>
      Belirtilen otomasyon zincirini çalıştırır.
      Örnek: node scripts/automation-runner.mjs --pipeline full-sync-and-cloud

  node scripts/automation-runner.mjs --schedule [dakika]
      Belirli aralıklarla tam senkronizasyon pipeline'ını çalıştırır.
=============================================================
`);
    process.exit(0);
  }

  if (args.includes('--list')) {
    const scripts = getAllScripts();
    console.log(`\n📋 Kayıtlı ve Keşfedilen Scriptler (${scripts.length} Adet):\n`);
    let currentCat = '';
    for (const s of scripts) {
      if (s.category !== currentCat) {
        currentCat = s.category;
        console.log(`\n📁 [${currentCat}]`);
      }
      console.log(`  • ${s.name.padEnd(38)} | ${s.title} (${s.runtime})`);
      if (s.description) console.log(`    ↳ ${s.description}`);
    }
    process.exit(0);
  }

  if (args.includes('--pipelines')) {
    console.log(`\n⚡ Kayıtlı Otomasyon Pipeline'ları (${AUTOMATION_PIPELINES.length} Adet):\n`);
    for (const p of AUTOMATION_PIPELINES) {
      console.log(`  🚀 [${p.id}] ${p.title}`);
      console.log(`     ${p.description}`);
      console.log(`     Adımlar: ${p.steps.map((st) => st.script).join(' ➔ ')}\n`);
    }
    process.exit(0);
  }

  const runIdx = args.indexOf('--run');
  if (runIdx !== -1 && args[runIdx + 1]) {
    const scriptName = args[runIdx + 1];
    const argsIdx = args.indexOf('--args');
    const scriptArgs = argsIdx !== -1 && args[argsIdx + 1] ? args[argsIdx + 1] : '';

    console.log(`⚡ Script başlatılıyor: ${scriptName} (Args: "${scriptArgs}")...`);
    try {
      const job = startScriptJob(scriptName, scriptArgs, 'cli');
      const interval = setInterval(() => {
        const current = getJob(job.id);
        if (!current || current.status !== 'running') {
          clearInterval(interval);
          console.log(`\n[Bitti] Durum: ${current?.status}, Çıkış Kodu: ${current?.exitCode}`);
          process.exit(current?.exitCode || 0);
        }
      }, 500);
    } catch (e) {
      console.error(`❌ Hata: ${e.message}`);
      process.exit(1);
    }
  }

  const pipeIdx = args.indexOf('--pipeline');
  if (pipeIdx !== -1 && args[pipeIdx + 1]) {
    const pipeId = args[pipeIdx + 1];
    console.log(`🚀 Pipeline başlatılıyor: ${pipeId}...`);
    try {
      startPipelineJob(pipeId, 'cli').then((job) => {
        const interval = setInterval(() => {
          const current = getJob(job.id);
          if (!current || current.status !== 'running') {
            clearInterval(interval);
            console.log(`\n[Pipeline Bitti] Durum: ${current?.status}`);
            process.exit(current?.status === 'completed' ? 0 : 1);
          }
        }, 1000);
      });
    } catch (e) {
      console.error(`❌ Hata: ${e.message}`);
      process.exit(1);
    }
  }

  const schedIdx = args.indexOf('--schedule');
  if (schedIdx !== -1) {
    const intervalMin = parseInt(args[schedIdx + 1], 10) || 60;
    console.log(`⏰ Zamanlanmış otomasyon modu aktif! Her ${intervalMin} dakikada bir 'full-sync-and-cloud' çalışacak.`);
    setInterval(() => {
      console.log(`\n[${new Date().toLocaleTimeString()}] Otomasyon döngüsü tetikleniyor...`);
      startPipelineJob('full-sync-and-cloud', 'scheduler');
    }, intervalMin * 60 * 1000);
  }
}
