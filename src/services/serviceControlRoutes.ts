/**
 * Yönetim › Sistem: servis denetimi (yeniden başlat / durdur / başlat) + servis başına günlük.
 *
 * Yalnız güçlü yönetici (isStrongAdmin; yönlendirilmiş — cf-connecting-ip / x-forwarded-for taşıyan — loopback
 * isteği loopback sayılmaz, Firebase yönetici jetonu ya da panel sırrı ister).
 *
 * İki makine:
 *  - Yerel cihaz: `systemctl --user <eylem> <birim>` / `journalctl --user -u <birim>` (execFile, kabuk yok).
 *  - Oracle (konteyner meds-app, kod /app): konteyner host systemctl/docker çalıştıramaz → istek dosyası.
 *    Sunucu /app/data/servis_kontrol/istekler/<id>.json yazar (host: ~/medsor/meds/data/servis_kontrol);
 *    host işçisi deploy/oracle/servis_isci.sh (meds-servis-isci.path) beyaz listeyi YENİDEN doğrular, uygular,
 *    sonuclar/<id>.json + durum.json (durum + son 200 satır günlük) yazar. meds_temp konteynerde salt-okunur
 *    olduğu için data/ kullanılır.
 *
 * Güvenlik kuralları (beyaz liste dışı hiçbir birim/eylem yok):
 *  - meds-web, meds-app, meds-pg, meds-server (Caddy kapısı), meds-tunnel: YALNIZ yeniden başlatma; kendini
 *    yeniden başlatma yanıt döndükten sonra gecikmeli yapılır.
 *  - GPU işçileri (meds-xtts-yerel): YALNIZ durdurma. AGENTS kural 10 başlatmayı koruyucu + saat kilidi
 *    koşuluna bağlar; panel bunu doğrulayamaz → başlatma/yeniden başlatma kapalı (terminalden yapılır).
 *  - meds-gpuguard: durdur/başlat (durdurmak BindsTo ile GPU işçisini de durdurur = güvenli yön).
 *
 * server.ts:  import { registerServiceControlRoutes } from './src/services/serviceControlRoutes.ts';
 *             registerServiceControlRoutes(app, { rootDir: __dirname, adminEmail: 'nofrostlife@gmail.com' });
 */
import express from 'express';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { execFile } from 'child_process';
import { isStrongAdmin } from './peopleInsights';
import { requestUser } from './firebaseIdentity';

type Action = 'restart' | 'stop' | 'start';
type Kind = 'user-unit' | 'system-unit' | 'container';
export interface ControlledService {
  id: string;
  label: string;
  kind: Kind;
  actions: Action[];
  note?: string;
  /** Bu sunucunun kendisi: yeniden başlatma gecikmeli */
  self?: boolean;
}

const RS: Action[] = ['restart', 'stop', 'start'];
const ONLY_RESTART: Action[] = ['restart'];

/* Yerel cihaz (systemd --user) */
export const LOCAL_SERVICES: ControlledService[] = [
  { id: 'meds-web.service', label: 'Yerel web sunucusu (3000)', kind: 'user-unit', actions: ONLY_RESTART, self: true, note: 'Bu panelin sunucusu; yalnız yeniden başlatılır (~20-30 sn).' },
  { id: 'meds-embed-bge.service', label: 'Vektörleme bge-m3 (8094)', kind: 'user-unit', actions: RS },
  { id: 'meds-embed.service', label: 'Vektörleme e5-small (8091)', kind: 'user-unit', actions: RS },
  { id: 'meds-ema.service', label: 'EMA ses işçisi (CPU)', kind: 'user-unit', actions: RS },
  { id: 'meds-core.service', label: 'Core v2 veri hattı', kind: 'user-unit', actions: RS },
  { id: 'meds-pipeline.service', label: 'Veri hattı', kind: 'user-unit', actions: RS },
  { id: 'meds-phases.service', label: 'Aşama işçisi', kind: 'user-unit', actions: RS },
  { id: 'meds-revize.service', label: 'Revize işçisi', kind: 'user-unit', actions: RS },
  { id: 'meds-downloads-watcher.service', label: 'İndirilenler izleyicisi', kind: 'user-unit', actions: RS },
  { id: 'meds-v2search.service', label: 'v2 arama', kind: 'user-unit', actions: RS },
  { id: 'meds-v2semantic.service', label: 'v2 anlamsal arama', kind: 'user-unit', actions: RS },
  { id: 'meds-watchdog.service', label: 'Bekçi (watchdog)', kind: 'user-unit', actions: RS },
  { id: 'meds-dashboard.service', label: 'Eski pano sunucusu', kind: 'user-unit', actions: RS },
  { id: 'meds-gpuguard.service', label: 'GPU koruyucu', kind: 'user-unit', actions: ['stop', 'start'], note: 'Durdurmak GPU işçilerini de durdurur.' },
  { id: 'meds-xtts-yerel.service', label: 'XTTS v2 yerel ses işçisi (GPU)', kind: 'user-unit', actions: ['stop'], note: 'GPU kuralı: panelden yalnız durdurulur; başlatma terminalden (koruyucu + saat kilidi).' },
  { id: 'meds-hat-gece.timer', label: 'Gece hattı zamanlayıcısı (02:30)', kind: 'user-unit', actions: RS },
  { id: 'meds-olasi-soru.timer', label: 'Olası soru zamanlayıcısı', kind: 'user-unit', actions: RS },
  { id: 'meds-kelime-zaman-hat.timer', label: 'Kelime zamanlama zamanlayıcısı', kind: 'user-unit', actions: RS, note: 'İşin kendisi koruyucu kapalıysa CPU’ya döner.' },
  { id: 'meds-ses-aktar.timer', label: 'Ses aktarım zamanlayıcısı', kind: 'user-unit', actions: RS },
  { id: 'meds-cikmis-yedek.timer', label: 'Çıkmış yedek zamanlayıcısı', kind: 'user-unit', actions: RS },
];

/* Oracle (host işçisi aynı listeyi servis_isci.sh içinde yeniden doğrular — ikisi birlikte güncellenir) */
export const ORACLE_SERVICES: ControlledService[] = [
  { id: 'meds-app', label: 'Uygulama sunucusu (meds-app)', kind: 'container', actions: ONLY_RESTART, self: true, note: 'Bu panelin sunucusu; yalnız yeniden başlatılır.' },
  { id: 'meds-pg', label: 'Veritabanı (meds-pg)', kind: 'container', actions: ONLY_RESTART, note: 'Asla durdurulmaz; yalnız yeniden başlatma.' },
  { id: 'meds-server', label: 'Kapı (Caddy)', kind: 'container', actions: ONLY_RESTART },
  { id: 'meds-tunnel', label: 'Cloudflare tüneli', kind: 'container', actions: ONLY_RESTART, note: 'Durdurmak siteyi erişilemez yapar; yalnız yeniden başlatma.' },
  { id: 'meds-embed', label: 'Vektörleme bge-m3', kind: 'container', actions: RS },
  { id: 'meds-ema', label: 'EMA ses işçisi', kind: 'container', actions: RS },
  { id: 'meds-ders-isci', label: 'Ders işçisi', kind: 'container', actions: RS },
  { id: 'meds-ders-yayin.timer', label: 'Ders yayın zamanlayıcısı', kind: 'system-unit', actions: RS },
  { id: 'meds-cumle-zaman.timer', label: 'Cümle zamanlama zamanlayıcısı', kind: 'system-unit', actions: RS },
  { id: 'meds-arama-paketi.timer', label: 'Arama paketi zamanlayıcısı', kind: 'system-unit', actions: RS },
  { id: 'meds-pg-yedek.timer', label: 'Veritabanı yedek zamanlayıcısı', kind: 'system-unit', actions: RS },
];

const ACTION_LABEL: Record<Action, string> = { restart: 'yeniden başlatıldı', stop: 'durduruldu', start: 'başlatıldı' };

function onOracle(rootDir: string) {
  const forced = String(process.env.MEDS_SERVIS_MAKINE || '').toLowerCase();
  if (forced === 'oracle' || forced === 'yerel') return forced === 'oracle';
  return path.resolve(rootDir) === '/app' && fs.existsSync('/.dockerenv');
}

function run(cmd: string, args: string[], timeout = 20000): Promise<{ code: number; out: string }> {
  return new Promise((resolve) => {
    execFile(cmd, args, { timeout, maxBuffer: 4 * 1024 * 1024, env: { ...process.env, LANG: 'C.UTF-8', SYSTEMD_COLORS: '0' } }, (err, stdout, stderr) => {
      const code = err ? (typeof (err as any).code === 'number' ? (err as any).code : 1) : 0;
      resolve({ code, out: `${stdout || ''}${stderr ? `\n${stderr}` : ''}`.trim() });
    });
  });
}

async function strongAdmin(req: express.Request, adminEmail: string) {
  const forwarded = !!(req.headers['cf-connecting-ip'] || req.headers['x-forwarded-for']);
  if (!forwarded) return isStrongAdmin(req, adminEmail);
  // Tünelden/kapıdan gelen istek loopback ayrıcalığı almaz
  const who = await requestUser(req);
  if (who.user && String(who.user.email || '').toLowerCase() === adminEmail.toLowerCase()) return true;
  const sec = String(process.env.MEDS_PANEL_SECRET || '').trim();
  const sup = String(req.headers['x-panel-secret'] || '');
  return sec.length >= 24 && sup.length === sec.length && crypto.timingSafeEqual(Buffer.from(sup), Buffer.from(sec));
}

async function localStatus(svc: ControlledService) {
  const r = await run('systemctl', ['--user', 'show', svc.id, '--no-pager', '-p', 'ActiveState,SubState,UnitFileState,ActiveEnterTimestamp,LoadState']);
  const m: Record<string, string> = {};
  for (const line of r.out.split('\n')) {
    const i = line.indexOf('=');
    if (i > 0) m[line.slice(0, i)] = line.slice(i + 1);
  }
  return {
    active: m.ActiveState || 'unknown',
    sub: m.SubState || '',
    enabled: m.UnitFileState || '',
    since: m.ActiveEnterTimestamp || '',
    loaded: m.LoadState !== 'not-found',
  };
}

export function registerServiceControlRoutes(app: express.Express, deps: { rootDir: string; adminEmail: string }) {
  const oracle = onOracle(deps.rootDir);
  const list = oracle ? ORACLE_SERVICES : LOCAL_SERVICES;
  const byId = new Map(list.map((s) => [s.id, s]));
  const ctlDir = path.resolve(deps.rootDir, 'data', 'servis_kontrol');
  const reqDir = path.join(ctlDir, 'istekler');
  const resDir = path.join(ctlDir, 'sonuclar');
  const statusFile = path.join(ctlDir, 'durum.json');
  let lastAction = 0;

  const guard: express.RequestHandler = async (req, res, next) => {
    try {
      if (await strongAdmin(req, deps.adminEmail)) return next();
    } catch {
      /* düşer */
    }
    res.status(403).json({ error: 'Bu işlem yalnız yönetici oturumuyla yapılabilir.' });
  };

  const readOracleStatus = (): { at?: string; services?: Record<string, any> } => {
    try {
      return JSON.parse(fs.readFileSync(statusFile, 'utf8'));
    } catch {
      return {};
    }
  };

  app.get('/api/admin/servis/list', guard, async (_req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    if (oracle) {
      const st = readOracleStatus();
      const at = st.at ? Date.parse(st.at) : 0;
      return res.json({
        machine: 'oracle',
        statusAt: st.at || null,
        helperOnline: !!at && Date.now() - at < 3 * 60_000,
        services: list.map((s) => {
          const x = st.services?.[s.id] || {};
          return { ...s, active: x.active || 'unknown', sub: x.sub || '', enabled: x.enabled || '', since: x.since || '', loaded: x.loaded !== false };
        }),
      });
    }
    const services = await Promise.all(list.map(async (s) => ({ ...s, ...(await localStatus(s)) })));
    res.json({ machine: 'yerel', statusAt: new Date().toISOString(), helperOnline: true, services });
  });

  app.get('/api/admin/servis/logs', guard, async (req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    const svc = byId.get(String(req.query.service || ''));
    if (!svc) return res.status(400).json({ error: 'Bilinmeyen servis.' });
    const lines = Math.max(20, Math.min(1000, Number(req.query.lines) || 200));
    if (oracle) {
      const st = readOracleStatus();
      const log: string = st.services?.[svc.id]?.log || '';
      return res.json({ service: svc.id, at: st.at || null, lines: log.split('\n').slice(-lines).join('\n'), note: 'Host işçisinin her dakika aldığı son 200 satır.' });
    }
    const r = await run('journalctl', ['--user', '-u', svc.id, '-n', String(lines), '--no-pager', '-o', 'short-iso'], 15000);
    res.json({ service: svc.id, at: new Date().toISOString(), lines: r.out });
  });

  app.post('/api/admin/servis/action', guard, express.json(), async (req, res) => {
    const svc = byId.get(String(req.body?.service || ''));
    const action = String(req.body?.action || '') as Action;
    if (!svc) return res.status(400).json({ error: 'Bilinmeyen servis.' });
    if (!svc.actions.includes(action)) return res.status(400).json({ error: `${svc.label}: bu eylem izinli değil.` });
    // Hızlı ardışık tıklamaya karşı küçük fren (toplu işlem sırayla gönderir)
    const now = Date.now();
    if (now - lastAction < 300) return res.status(429).json({ error: 'Çok hızlı; bir saniye sonra yeniden dene.' });
    lastAction = now;
    console.log(`[servis] ${action} ${svc.id} (${oracle ? 'oracle' : 'yerel'})`);

    if (oracle) {
      try {
        fs.mkdirSync(reqDir, { recursive: true });
        const id = `${Date.now()}-${crypto.randomBytes(4).toString('hex')}`;
        const tmp = path.join(reqDir, `.${id}.tmp`);
        fs.writeFileSync(tmp, JSON.stringify({ id, service: svc.id, action, at: new Date().toISOString() }));
        fs.renameSync(tmp, path.join(reqDir, `${id}.json`));
        return res.json({ pending: true, requestId: id, message: `${svc.label}: istek host işçisine iletildi.` });
      } catch (e: any) {
        return res.status(500).json({ error: `İstek yazılamadı: ${e?.message || e}` });
      }
    }

    if (svc.self) {
      res.json({ ok: true, delayed: true, message: `${svc.label} 2 sn sonra yeniden başlıyor; ~30 sn sonra sayfayı yenile.` });
      setTimeout(() => void run('systemctl', ['--user', '--no-block', 'restart', svc.id]), 2000);
      return;
    }
    const r = await run('systemctl', ['--user', action, svc.id], 60000);
    const st = await localStatus(svc);
    if (r.code !== 0) return res.status(500).json({ error: `${svc.label}: ${r.out || 'systemctl hatası'}`, status: st });
    res.json({ ok: true, status: st, message: `${svc.label} ${ACTION_LABEL[action]}.` });
  });

  app.get('/api/admin/servis/result/:id', guard, (req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    const id = String(req.params.id || '');
    if (!/^\d+-[0-9a-f]{8}$/.test(id)) return res.status(400).json({ error: 'Geçersiz istek kimliği.' });
    try {
      const out = JSON.parse(fs.readFileSync(path.join(resDir, `${id}.json`), 'utf8'));
      return res.json({ done: true, ...out });
    } catch {
      const waiting = fs.existsSync(path.join(reqDir, `${id}.json`));
      return res.json({ done: false, waiting });
    }
  });
}
