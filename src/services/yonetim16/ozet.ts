/**
 * Yönetim v16 — GET /api/admin/ozet (Genel bakış sayaçları, server-only).
 * İstemci dizilerinden sayım yapılmaz; her şey tek uçtan gelir. Pahalı taramalar 30 sn önbellekte.
 */
import type express from 'express';
import fs from 'fs';
import path from 'path';
import os from 'os';
import { pgDb } from '../pgDb.ts';
import { sonDenetimler } from './denetim.ts';
import { siteAyarOku } from './siteAyar.ts';

export type OzetDeps = {
  rootDir: string;
  dataDir: string;
  requireAdmin: express.RequestHandler;
  isPgOnline: () => boolean;
  /** Bekleyen soru şikâyeti sayısı (çıkmış + havuz raporları) */
  bekleyenSikayet: () => number;
  /** Onarım kuyruğu bekleyen */
  onarimBekleyen: () => number;
  faz14Bekleyen: () => number;
  sseIstemci: () => number;
};

let cache: { at: number; v: any } | null = null;

function jsonlSay24s(file: string, alan = 'at'): number {
  try {
    if (!fs.existsSync(file)) return 0;
    const sinir = Date.now() - 86_400_000;
    const satir = fs.readFileSync(file, 'utf8').trim().split('\n').slice(-2000);
    let n = 0;
    for (const l of satir) { try { if (Date.parse(JSON.parse(l)[alan]) >= sinir) n++; } catch { /* */ } }
    return n;
  } catch { return 0; }
}

function oku<T>(file: string, fb: T): T {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch { return fb; }
}

export function registerOzetRoutes(app: express.Express, d: OzetDeps) {
  app.get('/api/admin/ozet', d.requireAdmin, async (req, res) => {
    if (cache && Date.now() - cache.at < 30_000 && req.query.taze !== '1') return res.json({ ...cache.v, onbellek: true });
    const t0 = Date.now();
    const kullanici = { bugun: 0, simdi: 0, hafta: 0 };
    if (d.isPgOnline()) {
      try {
        const { rows } = await pgDb.query(`select
          (select count(distinct coalesce(uid, device_id))::int from public.user_usage_daily where day = current_date) bugun,
          (select count(distinct coalesce(uid, device_id))::int from public.user_usage_daily where day > current_date - 7) hafta,
          (select count(distinct coalesce(uid, device_id))::int from public.user_devices where last_seen > now() - interval '5 minutes') simdi`);
        Object.assign(kullanici, rows[0] || {});
      } catch { /* tablo yoksa 0 */ }
    }
    const fb = oku<any[]>(path.join(d.dataDir, 'learn_feedback.json'), []);
    const tuyoBekleyen = (() => {
      try {
        const f = path.join(d.dataDir, 'kamp', 'tuyolar.jsonl');
        if (!fs.existsSync(f)) return 0;
        const durum = new Map<string, string>();
        for (const l of fs.readFileSync(f, 'utf8').split('\n')) { try { const e = JSON.parse(l); if (e.id) durum.set(e.id, e.durum || durum.get(e.id) || ''); } catch { /* */ } }
        return [...durum.values()].filter((x) => x === 'oneri').length;
      } catch { return 0; }
    })();
    const surum = oku<any>(path.join(d.rootDir, 'dist', 'surum.json'), null);
    const dagitim = oku<any>(path.join(d.rootDir, 'dist', 'dagitim.json'), null);
    const ayar = siteAyarOku();
    const mem = process.memoryUsage();
    const v = {
      zaman: new Date().toISOString(),
      saglik: {
        pg: d.isPgOnline(),
        calismaSn: Math.round(process.uptime()),
        yiginMb: Math.round(mem.heapUsed / 1048576),
        rssMb: Math.round(mem.rss / 1048576),
        // H174: yığın toplamı ayrı alan; ekran "kullanılan / ayrılan yığın" ve RSS'i ayrı etiketle gösterir
        yiginToplamMb: Math.round(mem.heapTotal / 1048576),
        yuk: os.loadavg()[0],
        sseIstemci: d.sseIstemci(),
        sunucu: os.hostname(),
      },
      kullanici,
      bekleyen: {
        sikayet: d.bekleyenSikayet(),
        geriBildirim: Array.isArray(fb) ? fb.filter((x) => x?.status === 'open').length : 0,
        tuyo: tuyoBekleyen,
        onarim: d.onarimBekleyen(),
        faz14: d.faz14Bekleyen(),
      },
      hata: { istemci24s: jsonlSay24s(path.join(d.dataDir, 'istemci_hatalari.jsonl')) },
      site: { bakim: ayar.bakim?.acik === true, duyuru: ayar.duyuru?.acik === true, gizliSayfa: Object.values(ayar.sayfalar || {}).filter((x) => x !== 'acik').length },
      surum: { onem: surum?.onem ?? null, baslik: surum?.baslik ?? null, commit: dagitim?.commit ?? null, dagitim: dagitim?.zaman ?? null },
      sonDenetim: await sonDenetimler(8, true), // H173: yalnız yazma
      sureMs: 0,
    };
    v.sureMs = Date.now() - t0;
    cache = { at: Date.now(), v };
    res.json(v);
  });
}
