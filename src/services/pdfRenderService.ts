/**
 * PDF Stüdyosu sunucu tarafı: istemcinin uygulamanın kendi CSS'iyle kurduğu HTML belgesini başsız Chrome'a
 * bastırır. Ekrandaki tasarım (font, renk, köşe, gölge) birebir korunur; metin vektör kalır.
 *
 * Güvenlik: belge about:blank üzerine `Page.setDocumentContent` ile yazılır (file:// erişimi yok), JavaScript
 * kapalıdır ve tüm ağ istekleri yakalanır: yalnızca Google Fonts'a izin verilir. Böylece gönderilen HTML iç
 * ağdaki adreslere ya da yerel dosyalara ulaşamaz. Bağımlılık yok: Chrome DevTools Protocol, Node'un yerleşik
 * WebSocket'i ile konuşulur. Chrome yolu `CHROME_PATH` ile verilebilir.
 */
import { spawn, type ChildProcess } from 'child_process';
import fs from 'fs';
import os from 'os';
import path from 'path';

const CANDIDATES = [
  process.env.CHROME_PATH,
  '/usr/bin/google-chrome',
  '/usr/bin/google-chrome-stable',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/snap/bin/chromium',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
].filter(Boolean) as string[];

export const findChrome = (): string | null => CANDIDATES.find((p) => fs.existsSync(p)) || null;

const ALLOWED_HOSTS = new Set(['fonts.googleapis.com', 'fonts.gstatic.com']);
export const MAX_HTML_BYTES = 25 * 1024 * 1024;
const TIMEOUT_MS = 120_000;

/** Gönderilen belgeden çalıştırılabilir ve gömülü içerikleri ayıklar (ikinci savunma hattı). */
const sanitize = (html: string) =>
  html
    .replace(/<script\b[\s\S]*?<\/script\s*>/gi, '')
    .replace(/<(iframe|object|embed|frame|frameset|portal)\b[\s\S]*?(<\/\1\s*>|\/?>)/gi, '')
    .replace(/<meta[^>]+http-equiv[^>]*>/gi, '')
    .replace(/\son[a-z]+\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)/gi, '');

type Pending = { resolve: (v: any) => void; reject: (e: Error) => void };

class Cdp {
  private ws: WebSocket;
  private id = 0;
  private pending = new Map<number, Pending>();
  private listeners: ((m: any) => void)[] = [];
  constructor(ws: WebSocket) {
    this.ws = ws;
    ws.addEventListener('message', (ev: MessageEvent) => {
      const msg = JSON.parse(String(ev.data));
      if (msg.id && this.pending.has(msg.id)) {
        const p = this.pending.get(msg.id)!;
        this.pending.delete(msg.id);
        msg.error ? p.reject(new Error(msg.error.message)) : p.resolve(msg.result);
      } else this.listeners.forEach((l) => l(msg));
    });
  }
  send(method: string, params: Record<string, any> = {}, sessionId?: string): Promise<any> {
    const id = ++this.id;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
    });
  }
  on(fn: (m: any) => void) {
    this.listeners.push(fn);
  }
  waitFor(pred: (m: any) => boolean, ms: number): Promise<any> {
    return new Promise((resolve, reject) => {
      const t = setTimeout(() => reject(new Error('Chrome yanıt vermedi')), ms);
      this.on((m) => {
        if (pred(m)) {
          clearTimeout(t);
          resolve(m);
        }
      });
    });
  }
}

const launch = async (chrome: string): Promise<{ proc: ChildProcess; dir: string; wsUrl: string }> => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'medsoru-pdf-'));
  const args = [
    '--headless=new',
    '--disable-gpu',
    '--hide-scrollbars',
    '--mute-audio',
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-extensions',
    '--disable-background-networking',
    '--disable-sync',
    '--remote-debugging-port=0',
    `--user-data-dir=${dir}`,
    ...(process.getuid?.() === 0 ? ['--no-sandbox'] : []),
    'about:blank',
  ];
  const proc = spawn(chrome, args, { stdio: 'ignore' });
  const portFile = path.join(dir, 'DevToolsActivePort');
  const started = Date.now();
  while (!fs.existsSync(portFile) || fs.readFileSync(portFile, 'utf8').split('\n').length < 2) {
    if (proc.exitCode != null) throw new Error('Chrome başlatılamadı');
    if (Date.now() - started > 20_000) throw new Error('Chrome zamanında başlamadı');
    await new Promise((r) => setTimeout(r, 60));
  }
  const [port, wsPath] = fs.readFileSync(portFile, 'utf8').trim().split('\n');
  return { proc, dir, wsUrl: `ws://127.0.0.1:${port}${wsPath}` };
};

export interface RenderOptions {
  /** Belge başlığı (PDF meta verisi) */
  title?: string;
}

const render = async (html: string, _opts: RenderOptions): Promise<Buffer> => {
  const chrome = findChrome();
  if (!chrome) throw Object.assign(new Error('Sunucuda Chrome bulunamadı'), { status: 503 });
  const { proc, dir, wsUrl } = await launch(chrome);
  let ws: WebSocket | null = null;
  try {
    ws = new WebSocket(wsUrl);
    await new Promise<void>((resolve, reject) => {
      ws!.addEventListener('open', () => resolve(), { once: true });
      ws!.addEventListener('error', () => reject(new Error('Chrome bağlantısı kurulamadı')), { once: true });
    });
    const cdp = new Cdp(ws);
    const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
    const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
    const s = (m: string, p: Record<string, any> = {}) => cdp.send(m, p, sessionId);

    // Ağ: yalnız Google Fonts
    cdp.on((m) => {
      if (m.method !== 'Fetch.requestPaused' || m.sessionId !== sessionId) return;
      let allowed = false;
      try {
        const u = new URL(m.params.request.url);
        allowed = u.protocol === 'https:' && ALLOWED_HOSTS.has(u.hostname);
      } catch {
        allowed = false;
      }
      (allowed
        ? s('Fetch.continueRequest', { requestId: m.params.requestId })
        : s('Fetch.failRequest', { requestId: m.params.requestId, errorReason: 'BlockedByClient' })
      ).catch(() => {});
    });
    // Ağ boşta mı: yazı tipi dosyaları yerleşim sırasında istenir, bitene kadar beklenir
    const inflight = new Set<string>();
    let lastActivity = Date.now();
    cdp.on((m) => {
      if (m.sessionId !== sessionId) return;
      if (m.method === 'Network.requestWillBeSent') inflight.add(m.params.requestId);
      else if (m.method === 'Network.loadingFinished' || m.method === 'Network.loadingFailed') inflight.delete(m.params.requestId);
      else return;
      lastActivity = Date.now();
    });
    await s('Network.enable');
    await s('Fetch.enable', { patterns: [{ urlPattern: '*' }] });
    await s('Emulation.setScriptExecutionDisabled', { value: true });
    await s('Page.enable');
    const { frameTree } = await s('Page.getFrameTree');
    await s('Page.setDocumentContent', { frameId: frameTree.frame.id, html: sanitize(html) });
    const until = Date.now() + 25_000;
    while (Date.now() < until && (inflight.size > 0 || Date.now() - lastActivity < 500)) await new Promise((r) => setTimeout(r, 100));
    const { data } = await s('Page.printToPDF', {
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: false,
      generateTaggedPDF: true,
      generateDocumentOutline: true,
    });
    return Buffer.from(data, 'base64');
  } finally {
    try {
      ws?.close();
    } catch {}
    try {
      proc.kill('SIGKILL');
    } catch {}
    setTimeout(() => fs.rm(dir, { recursive: true, force: true }, () => {}), 500);
  }
};

// Aynı anda en çok 2 Chrome; kuyruk sınırı aşılırsa istek reddedilir (makineyi korur)
let running = 0;
const queue: (() => void)[] = [];
const MAX_PARALLEL = 2;
const MAX_QUEUE = 8;

export async function renderHtmlToPdf(html: string, opts: RenderOptions = {}): Promise<Buffer> {
  if (Buffer.byteLength(html, 'utf8') > MAX_HTML_BYTES) throw Object.assign(new Error('Belge çok büyük'), { status: 413 });
  if (running >= MAX_PARALLEL) {
    if (queue.length >= MAX_QUEUE) throw Object.assign(new Error('PDF sırası dolu, birazdan tekrar dene'), { status: 429 });
    await new Promise<void>((r) => queue.push(r));
  }
  running++;
  try {
    return await Promise.race([
      render(html, opts),
      new Promise<never>((_, rej) => setTimeout(() => rej(Object.assign(new Error('PDF oluşturma zaman aşımına uğradı'), { status: 504 })), TIMEOUT_MS)),
    ]);
  } finally {
    running--;
    queue.shift()?.();
  }
}
