/**
 * Hat panosu — ders × aşama matrisi ve ders eylemleri (Yönetim › Hat, ManageHatSection.tsx).
 *
 *   GET  /api/admin/hat/dersler?kurul=N       — Kurul 2+ ders kayıt defteri × aşama durumu (matris satırları)
 *   GET  /api/admin/hat/dersler/:id           — tek ders: aşamalar + kapı ayrıntısı + eylem işleri + günlük satırları
 *   GET  /api/admin/hat/eylemler              — son eylem işleri (yoklama)
 *   POST /api/admin/hat/eylem                 — {eylem: surdur|bastan|denetci|cek, dersler: [id], onay?, kuru?}
 *   POST /api/admin/hat/eylem/:is/iptal       — sırada bekleyen işi iptal
 *
 * Aşamalar ve kaynakları (gerçek dosyalardan):
 *   isci, yayin  — Oracle ders işçisi: taslak/<is>/{baglam,durum,denetim,yayin,karar}.json + kuyruk.json + yayin_kaydi.json
 *                  (cihazda SSH ile salt-okunur, 60 sn önbellek; Oracle'da işçi iç API'si MEDS_ISCI_URL)
 *   hazirla … oracle — cihaz ders zinciri: meds_temp/hat/dersler/<id>.json (otomasyon/ders_zinciri.py yazar)
 * Eylemler istek içinde çalışmaz: meds_temp/hat/eylemler/<is>.json kuyruğa yazılır, otomasyon/hat_eylem.py geçici
 * systemd --user birimiyle (meds-hat-eylem; MemoryMax/CPUQuota, GPU kapalı) sırayla işler; gece hattı çalışırken bekler.
 * Oracle'da (MEDS_ISCI_URL tanımlı) uçlar salt okunurdur: ders zinciri yalnız cihazda çalışır.
 * server.ts: registerHatActionRoutes(app, { rootDir: __dirname, requireAdmin });
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { execFile } from 'child_process';
import type { Express, Request, Response, RequestHandler } from 'express';

type Durum = 'gecti' | 'calisiyor' | 'takildi' | 'bekliyor';
type Hucre = { asama: string; durum: Durum; kod?: number | null; zaman?: string | null; not?: string; hatalar?: string[] };
type Ders = { id: string; kod: string; kurul: number; brans: string; konu: string; tarih?: string; ogretim_uyesi?: string };
type Taslak = {
  is_id: string; ders_id?: string; durum?: string; ozet?: string; denetim_hata?: number | null; denetim_hatalar?: string[];
  yayin?: { durum?: string; hatalar?: string[]; zaman?: string } | null; karar?: { karar?: string } | null; zaman?: number | null;
};
type OracleAnlik = { taslaklar: Taslak[]; kuyruk: any[]; yayin: any[]; zaman: number; hata?: string };

export const ASAMALAR: { id: string; ad: string; yer: 'oracle' | 'cihaz' }[] = [
  { id: 'isci', ad: 'Ders işçisi', yer: 'oracle' },
  { id: 'yayin', ad: 'Yayın', yer: 'oracle' },
  { id: 'hazirla', ad: 'Hazırlık', yer: 'cihaz' },
  { id: 'onem', ad: 'Önem listesi', yer: 'cihaz' },
  { id: 'cozucu', ad: 'Soru çözücü', yer: 'cihaz' },
  { id: 'denetim', ad: 'Denetçi', yer: 'cihaz' },
  { id: 'birlestir', ad: 'Birleştirme', yer: 'cihaz' },
  { id: 'asistan', ad: 'Asistan', yer: 'cihaz' },
  { id: 'ses', ad: 'EMA ses', yer: 'cihaz' },
  { id: 'oracle', ad: 'Canlıya aktarım', yer: 'cihaz' },
];
const ZINCIR = ASAMALAR.filter((a) => a.yer === 'cihaz').map((a) => a.id);

// ders_zinciri.py çıkış kodlarının anlamı (kapı adı + ne olduğu)
const KOD_ANLAM: Record<string, Record<number, string>> = {
  hazirla: { 2: 'kaynak.md bulunamadı (Oracle\'dan çekilemedi)' },
  onem: { 1: 'onem_dogrula.py 3 düzeltme turundan sonra da HATA verdi' },
  cozucu: { 1: 'cozucu_dogrula.py 3 düzeltme turundan sonra da HATA verdi' },
  denetim: { 1: 'denetçi düzeltmesinden sonra onem_dogrula.py / cozucu_dogrula.py HATA verdi', 8: 'denetçi raporu (denetim/<kod>.md) yazılmadı' },
  birlestir: { 9: 'birleştirme bu dersin önem çıktısını yazmadı', 11: 'birleştirme başka içeriği sildi/küçülttü, yedek geri kondu', 13: 'aynı soru önem listesi ile çözücüde farklı doğru cevapla (H7)' },
  asistan: { 1: 'asistan_plan.py ya da asistan_dogrula.py HATA verdi', 11: 'asistan birleştirme içerik sildi, yedek geri kondu' },
  ses: {},
  oracle: { 12: 'canlıda ses klibi bulunamadı (H11)', 6: 'içerik sürüm kaydı yazılamadı' },
};
const kodAnlam = (asama: string, kod: number) =>
  KOD_ANLAM[asama]?.[kod] || (kod === 124 ? 'Claude oturumu 3 saatte bitmedi (zaman aşımı)' : `çıkış kodu ${kod}`);

const EYLEM_AD: Record<string, string> = {
  surdur: 'Takılan aşamadan sürdür', bastan: 'Baştan üret', denetci: 'Denetçiye gönder', cek: 'Yayından çek',
};
const TEHLIKELI = new Set(['bastan', 'cek']);
const DERS_ID = /^k[2-6]-\d{2,3}$/;

function oku<T>(p: string, yedek: T): T {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')) as T; } catch { return yedek; }
}
function kuyruk(p: string, n: number): string[] {
  try {
    const st = fs.statSync(p);
    const boy = Math.min(st.size, 64 * 1024);
    const fd = fs.openSync(p, 'r');
    const b = Buffer.alloc(boy);
    fs.readSync(fd, b, 0, boy, st.size - boy);
    fs.closeSync(fd);
    return b.toString('utf8').split('\n').filter((l) => l.trim()).slice(-n);
  } catch { return []; }
}
function calistir(komut: string, arg: string[], ms = 25000, girdi?: string): Promise<{ kod: number; out: string; err: string }> {
  return new Promise((resolve) => {
    const c = execFile(komut, arg, { timeout: ms, maxBuffer: 16 * 1024 * 1024 }, (e: any, out, err) =>
      resolve({ kod: e ? (typeof e.code === 'number' ? e.code : 1) : 0, out: String(out || ''), err: String(err || '') }));
    if (girdi != null) { c.stdin?.end(girdi); }
  });
}

// Oracle'da tek seferde çalışan salt-okunur özet (taslaklar + kuyruk + yayın kaydı)
const ORACLE_OZET_PY = `
import json, os
B = "/home/ubuntu/medsor/ders_isci"
def oku(p, y):
    try: return json.load(open(p))
    except Exception: return y
T = []
for ad in os.listdir(B + "/taslak"):
    d = B + "/taslak/" + ad
    if not os.path.isfile(d + "/baglam.json"): continue
    b = oku(d + "/baglam.json", {}); du = oku(d + "/durum.json", {}); de = oku(d + "/denetim.json", None)
    T.append({"is_id": ad, "ders_id": b.get("ders_id"), "durum": du.get("durum") or "isleniyor", "ozet": du.get("ozet", ""),
              "denetim_hata": de.get("hata") if de else None, "denetim_hatalar": (de or {}).get("hatalar", [])[:8],
              "yayin": oku(d + "/yayin.json", None), "karar": oku(d + "/karar.json", None), "zaman": du.get("zaman")})
K = [{k: j.get(k) for k in ("is_id", "yol", "durum", "son_mesaj", "deneme")} for j in oku(B + "/kuyruk.json", [])]
Y = [{k: y.get(k) for k in ("is_id", "kurul", "ders_id", "deste_id", "yayin_zamani")} for y in oku(B + "/yayin_kaydi.json", [])]
print(json.dumps({"taslaklar": T, "kuyruk": K, "yayin": Y}, ensure_ascii=False))
`;

export function registerHatActionRoutes(app: Express, deps: { rootDir: string; requireAdmin: RequestHandler }) {
  const MEDS = deps.rootDir;
  const KOK = path.resolve(MEDS, '..');
  const DURUM = path.join(KOK, 'meds_temp/hat/dersler');
  const EYLEM = path.join(KOK, 'meds_temp/hat/eylemler');
  const ISCI_URL = (process.env.MEDS_ISCI_URL || '').replace(/\/$/, '');
  const cihaz = !ISCI_URL; // Oracle'da işçi iç adresi tanımlıdır; ders zinciri ve eylemler yalnız cihazda
  const BRANS: Record<string, string> = Object.fromEntries(
    (oku<any>(path.join(MEDS, 'src/data/dersler/branslar.json'), { branslar: [] }).branslar || []).map((b: any) => [b.ad, b.slug]));

  const defter = (kurul?: number): Ders[] => {
    const out: Ders[] = [];
    for (let k = 2; k <= 6; k++) {
      if (kurul && k !== kurul) continue;
      out.push(...(oku<any>(path.join(MEDS, `src/data/dersler/k${k}.json`), { dersler: [] }).dersler || []));
    }
    return out;
  };

  // ── Oracle anlık görüntüsü (60 sn önbellek; aynı anda tek istek) ──
  let onbellek: OracleAnlik | null = null;
  let suruyor: Promise<OracleAnlik> | null = null;
  const oracleAnlik = (): Promise<OracleAnlik> => {
    if (onbellek && Date.now() - onbellek.zaman < 60_000) return Promise.resolve(onbellek);
    if (suruyor) return suruyor;
    suruyor = (async (): Promise<OracleAnlik> => {
      try {
        if (!cihaz) {
          const al = async (y: string) => { const r = await fetch(ISCI_URL + y, { signal: AbortSignal.timeout(15000) }); return r.ok ? r.json() : []; };
          const [t, k] = await Promise.all([al('/taslaklar'), al('/kuyruk')]);
          const taslaklar: Taslak[] = (t || []).map((x: any) => ({ ...x, denetim_hatalar: [] }));
          const yayin = oku<any[]>(path.join(MEDS, 'scripts/ders_isci/yayin_kaydi.json'), []);
          return { taslaklar, kuyruk: k || [], yayin, zaman: Date.now() };
        }
        const r = await calistir('ssh', ['-o', 'ConnectTimeout=10', '-o', 'BatchMode=yes', 'medsor-oracle', 'python3', '-'], 25000, ORACLE_OZET_PY);
        if (r.kod === 0 && r.out.trim().startsWith('{')) return { ...JSON.parse(r.out), zaman: Date.now() };
        throw new Error(r.err.trim().slice(0, 200) || `ssh kod ${r.kod}`);
      } catch (e: any) {
        // Oracle'a ulaşılamadı: cihazdaki yayın kaydı kopyası (yayinla.py --esitle günceller)
        const yayin = oku<any[]>(path.join(MEDS, 'scripts/ders_isci/yayin_kaydi.json'), []);
        return { taslaklar: [], kuyruk: [], yayin, zaman: Date.now(), hata: `Oracle ders işçisi okunamadı: ${String(e?.message || e)}` };
      }
    })().then((x) => { onbellek = x; suruyor = null; return x; });
    return suruyor;
  };

  const isler = (): any[] => {
    try {
      return fs.readdirSync(EYLEM).filter((f) => f.endsWith('.json')).map((f) => oku<any>(path.join(EYLEM, f), null)).filter(Boolean)
        .sort((a, b) => String(b.olusturma).localeCompare(String(a.olusturma)));
    } catch { return []; }
  };

  const satir = (d: Ders, o: OracleAnlik, tumIsler: any[]) => {
    const onek = d.id + '-';
    const taslak = o.taslaklar.filter((t) => String(t.ders_id || '').startsWith(onek))
      .sort((a, b) => Number(b.zaman || 0) - Number(a.zaman || 0))[0];
    const yayin = o.yayin.filter((y) => y.kurul === d.kurul && String(y.ders_id || '').startsWith(onek))
      .sort((a, b) => String(b.yayin_zamani).localeCompare(String(a.yayin_zamani)))[0];
    const ky = taslak ? o.kuyruk.find((k) => k.is_id === taslak.is_id) : null;
    const hucreler: Hucre[] = [];
    // isci
    if (!taslak) hucreler.push({ asama: 'isci', durum: yayin ? 'gecti' : 'bekliyor', not: yayin ? 'Yayın kaydında var' : 'PDF henüz işlenmedi' });
    else if (taslak.durum === 'isleniyor' || ky?.durum === 'isleniyor') hucreler.push({ asama: 'isci', durum: 'calisiyor', not: ky?.son_mesaj || 'İşçi bu dersi işliyor' });
    else if (ky?.durum === 'hata') hucreler.push({ asama: 'isci', durum: 'takildi', not: ky?.son_mesaj || 'İşçi hata verdi', hatalar: [] });
    else if ((taslak.denetim_hata ?? 0) > 0) hucreler.push({ asama: 'isci', durum: 'takildi', not: `denetle.py ${taslak.denetim_hata} HATA`, hatalar: taslak.denetim_hatalar || [] });
    else if (taslak.karar?.karar === 'reddet') hucreler.push({ asama: 'isci', durum: 'takildi', not: 'Taslak reddedildi' });
    else hucreler.push({ asama: 'isci', durum: 'gecti', not: taslak.ozet || '' });
    // yayin
    const yj = taslak?.yayin;
    if (yayin && (!yj || yj.durum === 'yayinlandi')) hucreler.push({ asama: 'yayin', durum: 'gecti', zaman: yayin.yayin_zamani, not: yayin.ders_id });
    else if (yj && yj.durum && yj.durum !== 'yayinlandi') hucreler.push({ asama: 'yayin', durum: 'takildi', zaman: yj.zaman, not: `yayinla.py: ${yj.durum}`, hatalar: yj.hatalar || [] });
    else if (taslak?.karar?.karar === 'onayla') hucreler.push({ asama: 'yayin', durum: 'calisiyor', not: 'Onaylandı; yayın zamanlayıcısı (10 dk) bekleniyor' });
    else hucreler.push({ asama: 'yayin', durum: 'bekliyor', not: taslak ? (taslak.durum === 'onay_bekliyor' ? 'Onay bekliyor' : taslak.durum) : '' });
    // cihaz zinciri
    const s = oku<any>(path.join(DURUM, `${d.id}.json`), { adimlar: {} });
    const calisanIs = tumIsler.find((j) => j.ders === d.id && j.durum === 'calisiyor');
    let calisiyorKondu = false;
    for (const a of ZINCIR) {
      const x = s.adimlar?.[a];
      if (x && x.kod === 0) { hucreler.push({ asama: a, durum: 'gecti', kod: 0, zaman: x.zaman }); continue; }
      if (calisanIs && !calisiyorKondu) { calisiyorKondu = true; hucreler.push({ asama: a, durum: 'calisiyor', zaman: calisanIs.baslama, not: EYLEM_AD[calisanIs.eylem] }); continue; }
      if (x && x.kod != null) hucreler.push({ asama: a, durum: 'takildi', kod: x.kod, zaman: x.zaman, not: kodAnlam(a, x.kod) });
      else hucreler.push({ asama: a, durum: 'bekliyor' });
    }
    const takilan = hucreler.find((h) => h.durum === 'takildi') || null;
    const bekleyenIs = tumIsler.find((j) => j.ders === d.id && (j.durum === 'bekliyor' || j.durum === 'calisiyor')) || null;
    // Oracle aşamasında takılan ders: sürdürme işçinin kendi uçlarıyla (/api/admin/ders-isci/…) yapılır
    let oracleEylem: { yol: string; ad: string } | null = null;
    if (takilan?.asama === 'yayin' && taslak) oracleEylem = { yol: `/api/admin/ders-isci/taslak/${taslak.is_id}/yeniden`, ad: 'Taslağı yayına yeniden gönder' };
    else if (takilan?.asama === 'isci' && taslak && ky?.durum === 'hata') oracleEylem = { yol: `/api/admin/ders-isci/kuyruk/${taslak.is_id}/yeniden-dene`, ad: 'İşçide yeniden dene' };
    return {
      id: d.id, kod: d.kod, kurul: d.kurul, brans: d.brans, ad: d.konu, tarih: d.tarih || null,
      hucreler, takilan: takilan ? takilan.asama : null,
      paket: !!yayin, is_id: taslak?.is_id || null, cekildi: s.cekildi || null, hataSayisi: Number(s.hata_sayisi || 0),
      sonHata: s.son_hata || null, is: bekleyenIs ? { id: bekleyenIs.id, eylem: bekleyenIs.eylem, durum: bekleyenIs.durum } : null,
      oracleEylem,
      klasor: `k${d.kurul}${BRANS[d.brans] || ''}`,
    };
  };

  app.get('/api/admin/hat/dersler', deps.requireAdmin, async (req: Request, res: Response) => {
    const k = Number(req.query.kurul) || undefined;
    const o = await oracleAnlik();
    const tum = isler();
    res.set('Cache-Control', 'no-store');
    res.json({
      cihaz, asamalar: ASAMALAR, oracleHata: o.hata || null, oracleZaman: new Date(o.zaman).toISOString(),
      gece: oku<any>(path.join(KOK, 'meds_temp/hat/durum.json'), {})?.ders_zinciri || null,
      dersler: defter(k).map((d) => satir(d, o, tum)),
      calisan: tum.filter((j) => j.durum === 'bekliyor' || j.durum === 'calisiyor').length,
    });
  });

  app.get('/api/admin/hat/dersler/:id', deps.requireAdmin, async (req: Request, res: Response) => {
    const id = String(req.params.id);
    const d = DERS_ID.test(id) ? defter().find((x) => x.id === id) : undefined;
    if (!d) return res.status(404).json({ error: 'Ders kayıt defterinde yok.' });
    const o = await oracleAnlik();
    const tum = isler();
    const r = satir(d, o, tum);
    const dersIsleri = tum.filter((j) => j.ders === id).slice(0, 10)
      .map((j) => ({ ...j, log: kuyruk(path.join(EYLEM, `${j.id}.log`), 80) }));
    // gece hattı günlüğü: bu dersin "▶ <id>" bloğu (ders_zinciri çıktısı journal'da)
    let gece: string[] = [];
    if (cihaz) {
      const j = await calistir('journalctl', ['--user', '-u', 'meds-hat-gece.service', '-n', '4000', '--no-pager', '-o', 'short-iso'], 8000);
      const satirlar = j.out.split('\n');
      let ic = false;
      for (const l of satirlar) {
        if (l.includes(`▶ ${id} `)) { ic = true; gece.push(l); continue; }
        if (ic && (/▶ /.test(l) || /\]: ▶ [a-z_]+: /.test(l))) ic = false;
        if (ic) gece.push(l);
      }
      gece = gece.slice(-80);
    }
    const claudeLog = cihaz ? kuyruk(path.join(KOK, 'meds_temp/spot_cozucu', r.klasor, 'claude.log'), 40) : [];
    const denetimRaporu = (() => { try { return fs.readFileSync(path.join(KOK, 'meds_temp/spot_cozucu', r.klasor, 'denetim', `${d.kod}.md`), 'utf8').slice(0, 20000); } catch { return ''; } })();
    res.set('Cache-Control', 'no-store');
    res.json({ cihaz, ders: { ...r, ogretim_uyesi: d.ogretim_uyesi || null }, isler: dersIsleri, gece, claudeLog, denetimRaporu, oracleHata: o.hata || null });
  });

  app.get('/api/admin/hat/eylemler', deps.requireAdmin, (_req: Request, res: Response) => {
    res.set('Cache-Control', 'no-store');
    res.json({ cihaz, isler: isler().slice(0, 50) });
  });

  // İşleyiciyi başlat (zaten çalışıyorsa yeni işleri kendisi alır)
  const isleyiciBaslat = async (): Promise<string | null> => {
    const PATH = [path.join(process.env.HOME || '/home/indu', '.local/bin'), process.env.PATH || '/usr/bin:/bin'].join(':');
    const arg = ['--user', '--unit=meds-hat-eylem', '--collect', '--quiet', '-p', 'MemoryMax=4G', '-p', 'CPUQuota=150%',
      '-p', 'OOMScoreAdjust=500', '--nice=10', `--working-directory=${KOK}`, '--setenv=CUDA_VISIBLE_DEVICES=', `--setenv=PATH=${PATH}`,
      '/usr/bin/python3', path.join(MEDS, 'otomasyon/hat_eylem.py'), '--isle'];
    for (let i = 0; i < 2; i++) {
      const r = await calistir('systemd-run', arg, 15000);
      if (r.kod === 0) return null;
      const etkin = await calistir('systemctl', ['--user', 'is-active', '--quiet', 'meds-hat-eylem.service'], 5000);
      if (etkin.kod === 0) return null; // çalışan işleyici yeni işi alır
      await new Promise((ok) => setTimeout(ok, 2000));
      if (i === 1) return (r.err || r.out).trim().slice(0, 300) || 'systemd-run başarısız';
    }
    return null;
  };

  app.post('/api/admin/hat/eylem', deps.requireAdmin, async (req: Request, res: Response) => {
    if (!cihaz) return res.status(409).json({ error: 'Ders zinciri yalnız cihazda çalışır. Paneli cihazdan (localhost) açın; burada pano salt okunurdur.' });
    const { eylem, dersler, onay, kuru } = req.body || {};
    if (!EYLEM_AD[eylem]) return res.status(400).json({ error: 'Bilinmeyen eylem.' });
    if (TEHLIKELI.has(eylem) && onay !== true) return res.status(400).json({ error: 'Bu eylem için onay gerekir.' });
    const liste: string[] = Array.isArray(dersler) ? [...new Set(dersler.map(String))].slice(0, 200) : [];
    if (!liste.length) return res.status(400).json({ error: 'Ders seçilmedi.' });
    const kayit = defter();
    const tum = isler();
    const kabul: string[] = []; const atlanan: { id: string; neden: string }[] = [];
    fs.mkdirSync(EYLEM, { recursive: true });
    for (const id of liste) {
      const d = DERS_ID.test(id) ? kayit.find((x) => x.id === id) : undefined;
      if (!d) { atlanan.push({ id, neden: 'Kurul 2+ ders kayıt defterinde yok (Kurul 1 otomatik hatta değil).' }); continue; }
      if (tum.some((j) => j.ders === id && (j.durum === 'bekliyor' || j.durum === 'calisiyor'))) { atlanan.push({ id, neden: 'Bu ders için sırada ya da çalışan bir iş var.' }); continue; }
      const is = {
        id: `${new Date().toISOString().replace(/\D/g, '').slice(0, 14)}-${crypto.randomBytes(3).toString('hex')}`,
        ders: id, kurul: d.kurul, eylem, durum: 'bekliyor', olusturma: new Date().toISOString(),
        kim: String(req.headers['x-admin-email'] || ''), ...(kuru === true ? { kuru: true } : {}),
      };
      fs.writeFileSync(path.join(EYLEM, `${is.id}.json`), JSON.stringify(is, null, 1));
      kabul.push(is.id);
    }
    let baslatmaHatasi: string | null = null;
    if (kabul.length) baslatmaHatasi = await isleyiciBaslat();
    res.json({ success: kabul.length > 0, eylem, kuyruga: kabul, atlanan, baslatmaHatasi });
  });

  app.post('/api/admin/hat/eylem/:is/iptal', deps.requireAdmin, (req: Request, res: Response) => {
    if (!cihaz) return res.status(409).json({ error: 'Salt okunur.' });
    const is = String(req.params.is);
    if (!/^\d{14}-[0-9a-f]{6}$/.test(is)) return res.status(400).json({ error: 'geçersiz iş' });
    const p = path.join(EYLEM, `${is}.json`);
    const j = oku<any>(p, null);
    if (!j) return res.status(404).json({ error: 'İş yok.' });
    if (j.durum !== 'bekliyor') return res.status(409).json({ error: 'Yalnız sırada bekleyen iş iptal edilir.' });
    fs.writeFileSync(p, JSON.stringify({ ...j, durum: 'iptal', bitis: new Date().toISOString() }, null, 1));
    res.json({ success: true });
  });
}
