/**
 * Yönetim v16 › Sistem (server-only): sağlık, LLM işleri durumu (kural 20: yalnız durum; başlatma mevcut elle uçlardan),
 * dağıtım bilgisi. Hiçbir uç zamanlayıcı kurmaz ya da LLM işi başlatmaz.
 */
import { execFile } from 'child_process';
import fs from 'fs';
import os from 'os';
import path from 'path';
import type express from 'express';
import { pgDb } from '../pgDb';

type Deps = {
  rootDir: string;
  dataDir: string;
  requireAdmin: express.RequestHandler;
  isPgOnline: () => boolean;
  sseIstemci: () => number;
  faz14: () => { bekleyen: number; calisiyor: boolean };
  onarim: () => { aktif: boolean; bekleyen: number; isleniyor: number; hata: number };
};

const komut = (cmd: string, args: string[], ms = 2500) => new Promise<string>((coz) => {
  execFile(cmd, args, { timeout: ms, encoding: 'utf8' }, (_e, out) => coz(String(out || '').trim()));
});

const yokla = async (url: string, ms = 1500) => {
  const t0 = Date.now();
  try {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), ms);
    const r = await fetch(url, { signal: ctl.signal });
    clearTimeout(t);
    return { ok: r.ok, durum: r.status, ms: Date.now() - t0 };
  } catch (e: any) {
    return { ok: false, durum: 0, ms: Date.now() - t0, hata: e?.name === 'AbortError' ? 'zaman aşımı' : String(e?.message || e).slice(0, 120) };
  }
};

const jsonOku = (f: string) => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return null; } };

export function registerYonetimSistem(app: express.Express, d: Deps) {
  const A = d.requireAdmin;

  app.get('/api/admin/sistem/saglik', A, async (_req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    const m = process.memoryUsage();
    let pg: any = { cevrimici: d.isPgOnline() };
    if (pg.cevrimici) {
      const t0 = Date.now();
      try {
        const r = await pgDb.query(`select pg_database_size(current_database())::bigint boyut,
          (select count(*)::int from pg_stat_activity where datname = current_database()) baglanti,
          (select count(*)::int from pg_stat_activity where datname = current_database() and state = 'active') etkin`);
        pg = { cevrimici: true, ms: Date.now() - t0, boyutMb: Math.round(Number(r.rows[0].boyut) / 1048576), baglanti: r.rows[0].baglanti, etkin: r.rows[0].etkin };
      } catch (e: any) { pg = { cevrimici: false, hata: e?.message }; }
    }
    const embedBge = (process.env.MEDS_EMBED_URL || 'http://127.0.0.1:8094').replace(/\/(embed|v1.*)?$/, '');
    const [bge, e5] = await Promise.all([yokla(`${embedBge}/health`), yokla(`${(process.env.MEDS_EMBED_E5_URL || 'http://127.0.0.1:8091').replace(/\/$/, '')}/health`)]);
    // İstemci hataları (son 24 saat) + son kayıt
    let istemci = { son24s: 0, son: null as any };
    try {
      const f = path.join(d.dataDir, 'istemci_hatalari.jsonl');
      if (fs.existsSync(f)) {
        const st = fs.statSync(f);
        const fd = fs.openSync(f, 'r');
        const n = Math.min(st.size, 512 * 1024);
        const buf = Buffer.alloc(n);
        fs.readSync(fd, buf, 0, n, st.size - n);
        fs.closeSync(fd);
        const satir = buf.toString('utf8').split('\n').filter(Boolean).slice(1).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
        const sinir = Date.now() - 86_400_000;
        istemci = { son24s: satir.filter((x: any) => Date.parse(x.at || x.zaman || '') > sinir).length, son: satir[satir.length - 1] || null };
      }
    } catch { /* */ }
    let sonSunucuHatasi: any = null;
    if (d.isPgOnline()) {
      try { sonSunucuHatasi = (await pgDb.query(`select at, yontem, uc, durum, ozet->>'hata' hata from public.yonetici_denetim where durum >= 500 order by at desc limit 1`)).rows[0] || null; } catch { /* */ }
    }
    res.json({
      sunucu: { ana: os.hostname(), node: process.version, calismaSn: Math.round(process.uptime()), pid: process.pid },
      bellek: { yiginMb: Math.round(m.heapUsed / 1048576), yiginTavanMb: Math.round(m.heapTotal / 1048576), rssMb: Math.round(m.rss / 1048576), sistemBosMb: Math.round(os.freemem() / 1048576), sistemToplamMb: Math.round(os.totalmem() / 1048576) },
      yuk: os.loadavg().map((x) => Math.round(x * 100) / 100), cekirdek: os.cpus().length,
      pg, embed: { bge, e5 }, sseIstemci: d.sseIstemci(), istemci, sonSunucuHatasi,
    });
  });

  app.get('/api/admin/llm-durum', A, async (_req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    const isciUrl = (process.env.MEDS_ISCI_URL || 'http://meds-ders-isci:8095').replace(/\/$/, '');
    const [isci, zamanlayici] = await Promise.all([
      yokla(`${isciUrl}/saglik`, 1500),
      komut('systemctl', ['--user', 'is-enabled', 'meds-hat-gece.timer', 'meds-olasi-soru.timer', 'meds-faz14-otomatik.timer']),
    ]);
    const zl = zamanlayici.split('\n');
    res.json({
      kilit: {
        otomatik: process.env.MEDS_LLM_OTOMATIK === '1',
        claudeAnahtari: Boolean(process.env.CLAUDE_CODE_OAUTH_TOKEN),
        aciklama: 'Kural 20: LLM işleri yalnız elle başlar. MEDS_LLM_OTOMATIK panelden değiştirilemez.',
      },
      faz14: d.faz14(),
      onarim: d.onarim(),
      dersIsci: { ulasilabilir: isci.ok, durum: isci.durum, hata: (isci as any).hata },
      zamanlayicilar: ['meds-hat-gece.timer', 'meds-olasi-soru.timer', 'meds-faz14-otomatik.timer'].map((ad, i) => ({ ad, durum: zl[i] || 'bilinmiyor' })),
    });
  });

  app.get('/api/admin/sistem/dagitim', A, async (_req, res) => {
    res.setHeader('Cache-Control', 'no-store');
    const r = d.rootDir;
    const [commit, dal, kirli, sonCommit] = await Promise.all([
      komut('git', ['-C', r, 'rev-parse', 'HEAD']),
      komut('git', ['-C', r, 'rev-parse', '--abbrev-ref', 'HEAD']),
      komut('git', ['-C', r, 'status', '--porcelain', '-uno']),
      komut('git', ['-C', r, 'log', '-8', '--pretty=format:%h%x09%cI%x09%an%x09%s']),
    ]);
    res.json({
      surum: jsonOku(path.join(r, 'dist', 'surum.json')),
      dagitim: jsonOku(path.join(r, 'dist', 'dagitim.json')),
      not: jsonOku(path.join(r, 'guncelleme_notu.json')),
      git: commit ? {
        commit, dal, kirliDosya: kirli ? kirli.split('\n').length : 0,
        son: sonCommit ? sonCommit.split('\n').map((l) => { const [h, at, kim, ...m] = l.split('\t'); return { h, at, kim, mesaj: m.join('\t') }; }) : [],
      } : null,
      sunucu: os.hostname(),
    });
  });
}
