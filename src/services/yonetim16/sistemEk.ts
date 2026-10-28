/**
 * Yönetim v16 — menüde "yakında" kalan son sayfaların uçları (2026-10-28):
 *  - Gelen kutusu             GET /api/admin/gelen                      (bekleyen her şey tek listede; satırda doğrudan işlem, H290)
 *                             POST /api/admin/gelen/hata/goruldu {kimlikler[]}  (istemci hatası grubu "görüldü"; yeni tekrar yeniden düşer)
 *  - Topluluk › Geri bildirim GET /api/admin/topluluk/geri-bildirim, PUT …/:id {durum, yanit}  (data/learn_feedback.json)
 *  - Sistem › Drive           GET /api/admin/sistem/drive, GET /api/admin/sistem/drive/dosyalar (tarama: mevcut POST /api/admin/drive/check-updates, elle)
 *  - Sistem › RAG             GET /api/admin/sistem/rag, POST /api/admin/sistem/rag/denetle {onay:'DENETLE', kuru?}  (yalnız cihaz, elle)
 *  - Sistem › Fazlar          GET /api/admin/sistem/fazlar/:kategori   (phaseDataExplorer → ListeYaniti; salt okunur)
 *  - Sistem › Bağlantılar     GET /api/admin/sistem/baglanti[/:ders]   (faz verisi: ders ↔ çıkmış soru ↔ slayt ↔ Öğren ↔ terim)
 * Hat sayfası mevcut uçları kullanır (/api/admin/hat, /api/admin/hat/{dersler,eylemler,gece}).
 * Kural 20: LLM başlatan uç yok; RAG denetimi CPU vektör servisini kullanır, yalnız elle + onay sözcüğüyle, zamanlayıcı yok.
 */
import type express from 'express';
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import { diziSayfala, listeSorgusu, katla } from './sayfalama.ts';
import { atomikJsonGuncelle } from './atomikJson.ts';
import { denetimHedef, denetimFark } from './denetim.ts';
import { pgDb } from '../pgDb';

type Any = Record<string, any>;
const oku = <T,>(f: string, v: T): T => { try { return JSON.parse(fs.readFileSync(f, 'utf8')) as T; } catch { return v; } };
const kirp = (s: unknown, n = 200) => String(s ?? '').replace(/\s+/g, ' ').trim().slice(0, n);
const kuyrukOku = (f: string, n: number): string[] => {
  try {
    const st = fs.statSync(f);
    const boy = Math.min(st.size, 200_000);
    const fd = fs.openSync(f, 'r');
    const b = Buffer.alloc(boy);
    fs.readSync(fd, b, 0, boy, st.size - boy);
    fs.closeSync(fd);
    return b.toString('utf8').split('\n').filter(Boolean).slice(-n);
  } catch { return []; }
};

export type SistemEkDeps = {
  rootDir: string;
  dataDir: string;
  port: number;
  requireAdmin: express.RequestHandler;
  isPgOnline: () => boolean;
  faz14Liste: () => Any[];
  /** server.ts createLearnFeedbackStore örneği (önbelleği olan tek yazıcı) */
  geriBildirim: { get: (id: string) => Any | undefined; resolve: (id: string) => boolean; update: (id: string, u: Any) => Any | null };
  fazKok: (id: string) => string;
  /** Çıkmış ham listesi (ders adı faz verisinde yoksa discipline'dan) */
  cikmisListe?: () => Any[];
  broadcast: (olay: string, veri: Any) => void;
};

// H290: Gelen önbelleği modül düzeyinde; işlem uçları (soru şikâyeti çöz, topluluk yok say/gizle, geri bildirim, hata görüldü)
// yazınca siler — yoksa 15 sn boyunca işlenen satır listeye geri dönüyordu.
let gelenOnbellek: { at: number; satirlar: Any[]; kaynaklar: Any } | null = null;
export const gelenOnbellekSil = () => { gelenOnbellek = null; };

export function registerYonetimSistemEk(app: express.Express, d: SistemEkDeps) {
  const A = d.requireAdmin;
  const KOK = path.resolve(d.rootDir, '..');

  /* ================= Geri bildirim (Öğren ekranı) ================= */
  const LF = path.join(d.dataDir, 'learn_feedback.json');
  const YANIT = path.join(d.dataDir, 'learn_feedback_yanit.json');
  const gbSatir = (f: Any, y: Any) => {
    const oy = Object.values(f.votes || {}) as number[];
    return {
      id: String(f.id), at: f.createdAt || '', deste: f.deckTitle || f.deckId || '', deckId: f.deckId || '', adim: Number(f.slideNumber) || 0,
      yer: kirp(f.location, 160), alan: kirp(f.field, 300), neden: kirp(f.reason, 600), kim: f.author?.name || 'Anonim', kimId: f.author?.id || '',
      durum: f.status === 'resolved' ? 'cozuldu' : 'acik', yukari: oy.filter((v) => v === 1).length, asagi: oy.filter((v) => v === -1).length,
      baglanti: f.link || '', yanit: y?.yanit || '', yanitAt: y?.at || '', yanitKim: y?.kim || '',
    };
  };
  const gbListe = () => {
    const y = oku<Any>(YANIT, {});
    return (oku<Any[]>(LF, []) || []).filter((x) => x && x.id).map((f) => gbSatir(f, y[f.id]));
  };
  app.get('/api/admin/topluluk/geri-bildirim', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    if (!('durum' in s.suzgec)) s.suzgec.durum = 'acik';
    if (s.suzgec.durum === 'hepsi') delete s.suzgec.durum;
    if (!s.sirala) s.sirala = 'at';
    res.setHeader('Cache-Control', 'no-store');
    res.json(diziSayfala(gbListe(), s, {
      araMetni: (x) => `${x.id} ${x.deste} ${x.yer} ${x.alan} ${x.neden} ${x.kim}`,
      siralayicilar: { at: (x) => x.at, yukari: (x) => x.yukari, deste: (x) => x.deste },
      suzgecler: { durum: (x, v) => x.durum === v, deste: (x, v) => x.deckId === v },
      yuzler: { durum: (x) => x.durum, deste: (x) => x.deckId },
    }));
  });
  app.put('/api/admin/topluluk/geri-bildirim/:id', A, async (req, res) => {
    const id = String(req.params.id);
    const f = d.geriBildirim.get(id);
    if (!f) return res.status(404).json({ error: 'Bildirim bulunamadı.' });
    denetimHedef(res, `geri-bildirim:${id}`);
    const { durum, yanit } = req.body || {};
    const once = { durum: f.status, yanit: oku<Any>(YANIT, {})[id]?.yanit || '' };
    if (durum === 'cozuldu' && f.status !== 'resolved') d.geriBildirim.resolve(id);
    else if (durum === 'acik' && f.status === 'resolved') { f.status = 'open'; d.geriBildirim.update(id, {}); }
    else if (durum !== undefined && durum !== 'cozuldu' && durum !== 'acik') return res.status(400).json({ error: 'durum: acik | cozuldu' });
    if (typeof yanit === 'string') {
      const kim = String(req.headers['x-admin-email'] || (req as any).adminAuth?.via || 'yönetici');
      await atomikJsonGuncelle<Any>(YANIT, (eski) => {
        const v = { ...(eski || {}) };
        if (yanit.trim()) v[id] = { yanit: kirp(yanit, 2000), at: new Date().toISOString(), kim };
        else delete v[id];
        return Object.keys(v).length ? v : { _bos: true };
      }, { yedek: 1 } as any).catch(() => undefined);
    }
    denetimFark(res, once, { durum: d.geriBildirim.get(id)?.status, yanit: typeof yanit === 'string' ? yanit : once.yanit });
    gelenOnbellekSil(); // H290
    d.broadcast('learn_feedback_changed', { id, deckId: f.deckId, time: Date.now() });
    const y = oku<Any>(YANIT, {});
    res.json({ success: true, oge: gbSatir(d.geriBildirim.get(id)!, y[id]) });
  });

  /* ================= Gelen kutusu ================= */
  const icIstek = async (yol: string): Promise<Any | null> => {
    try {
      const ctl = new AbortController();
      const t = setTimeout(() => ctl.abort(), 8000);
      const r = await fetch(`http://127.0.0.1:${d.port}${yol}`, { signal: ctl.signal, headers: { accept: 'application/json' } });
      clearTimeout(t);
      return r.ok ? await r.json() : null;
    } catch { return null; }
  };
  // H292: "görüldü" işaretli istemci hatası grupları (kimlik → işaret zamanı); grup ancak işaretten SONRA yeniden olursa listeye döner
  const GORULDU = path.join(d.dataDir, 'istemci_hata_goruldu.json');
  const gelenTopla = async () => {
    if (gelenOnbellek && Date.now() - gelenOnbellek.at < 15_000) return gelenOnbellek;
    const satirlar: Any[] = [];
    const kaynaklar: Record<string, { toplam: number; hata?: boolean }> = {};
    const ekle = (r: Any) => satirlar.push({ ...r, id: `${r.tur}:${r.kimlik}` });

    // 1. Soru şikâyetleri (çıkmış + havuz + örnek; sorular.ts'in kendi listesi, iç istek = loopback yönetici)
    const ss = await icIstek('/api/admin/sorular/sikayet?boyut=300&sirala=at');
    kaynaklar.soru = { toplam: ss?.toplam ?? 0, hata: !ss };
    for (const x of ss?.ogeler || []) ekle({ tur: 'soru', kimlik: x.id, at: x.at, baslik: x.neden, ayrinti: x.ayrinti || x.kok, kim: x.kim, ek: `${x.kaynak} · ${x.soruId}`, hedef: `sorular/sikayet?q=${encodeURIComponent(x.soruId)}` });

    // 2. Topluluk mesaj şikâyetleri (meds-pg)
    if (d.isPgOnline()) {
      try {
        const [{ rows }, c] = await Promise.all([
          pgDb.query(`select m.id, m.kanal, m.ad, m.metin, m.olusturma at, cardinality(m.sikayet_uid)::int sikayet from topluluk_mesajlar m
                       where cardinality(m.sikayet_uid) > 0 and not m.silindi order by m.olusturma desc nulls last limit 200`),
          // H291: gizlenen mesajın şikâyeti işlenmiş sayılır (ozet.ts sayacıyla aynı koşul); yoksa "Mesajı gizle" satırı listede kalıyordu
          pgDb.query(`select count(*)::int n from topluluk_mesajlar where cardinality(sikayet_uid) > 0 and not silindi`),
        ]);
        kaynaklar.topluluk = { toplam: c.rows[0]?.n || 0 };
        for (const m of rows as Any[]) ekle({ tur: 'topluluk', kimlik: String(m.id), at: m.at ? new Date(m.at).toISOString() : '', baslik: `${m.sikayet} şikâyet · ${m.kanal}`, ayrinti: kirp(m.metin, 300), kim: m.ad || '', ek: m.kanal, hedef: `topluluk/sikayet?q=${encodeURIComponent(kirp(m.metin, 40))}` });
      } catch { kaynaklar.topluluk = { toplam: 0, hata: true }; }
    } else kaynaklar.topluluk = { toplam: 0, hata: true };

    // 3. Öğren geri bildirimleri (açık)
    const gb = gbListe().filter((x) => x.durum === 'acik');
    kaynaklar.geriBildirim = { toplam: gb.length };
    for (const x of gb) ekle({ tur: 'geri-bildirim', kimlik: x.id, at: x.at, baslik: x.alan, ayrinti: x.neden, kim: x.kim, ek: `${x.deste} · adım ${x.adim}`, hedef: `topluluk/geri-bildirim/${encodeURIComponent(x.id)}` });

    // 4. İstemci hataları (son 24 saat, mesaja göre gruplu)
    const sinir = Date.now() - 86_400_000;
    const grup = new Map<string, { n: number; at: string; mesaj: string; yer: string }>();
    for (const l of kuyrukOku(path.join(d.dataDir, 'istemci_hatalari.jsonl'), 2000)) {
      try {
        const e = JSON.parse(l);
        if (!(Date.parse(e.at) >= sinir)) continue;
        const k = kirp(e.mesaj, 160);
        const g = grup.get(k) || { n: 0, at: e.at, mesaj: k, yer: e.yol || e.url || e.sayfa || '' };
        g.n++; if (String(e.at) > g.at) g.at = e.at;
        grup.set(k, g);
      } catch { /* bozuk satır */ }
    }
    const gorulen = oku<Record<string, string>>(GORULDU, {}); // H292
    for (const [k, g] of [...grup]) { const gk = katla(g.mesaj).slice(0, 80); if (gorulen[gk] && String(g.at) <= gorulen[gk]) grup.delete(k); }
    kaynaklar.hata = { toplam: grup.size };
    for (const g of grup.values()) ekle({ tur: 'hata', kimlik: katla(g.mesaj).slice(0, 80), at: g.at, baslik: g.mesaj, ayrinti: g.yer ? String(g.yer).slice(0, 200) : '', kim: '', ek: `${g.n} kez / 24 sa`, hedef: `sistem/hata?q=${encodeURIComponent(g.mesaj.slice(0, 40))}` });

    // 5. Gizlilik talepleri (bekleyen / işleniyor)
    const giz = oku<Any[]>(path.join(d.dataDir, 'gizlilik_talepleri.json'), []).filter((x) => x?.durum === 'bekliyor' || x?.durum === 'isleniyor');
    kaynaklar.gizlilik = { toplam: giz.length };
    const TUR: Record<string, string> = { 'disa-aktar': 'Verimi indir', sil: 'Hesabımı sil', duzelt: 'Düzeltme' };
    for (const x of giz) ekle({ tur: 'gizlilik', kimlik: x.id, at: x.at, baslik: TUR[x.tur] || x.tur, ayrinti: kirp(x.not, 300), kim: x.email || x.uid, ek: x.durum, hedef: `kisi/gizlilik?q=${encodeURIComponent(x.email || x.uid || '')}` });

    // 6. Faz 14 bekleyen
    const f14 = (d.faz14Liste() || []).filter((i) => i?.status === 'bekliyor');
    kaynaklar.faz14 = { toplam: f14.length };
    for (const i of f14.slice(0, 300)) ekle({ tur: 'faz14', kimlik: String(i.id), at: i.updatedAt || i.createdAt || '', baslik: `Soru ${i.questionId}`, ayrinti: kirp(i.notes?.[0]?.message || i.notes?.[0]?.reason || '', 300), kim: i.notes?.[0]?.name || '', ek: `${(i.notes || []).length} not`, hedef: `sorular/faz14?q=${encodeURIComponent(String(i.questionId || i.id))}` });

    // 7. Kamp tüyo önerileri (olay defteri katlanır)
    const tuyo = new Map<string, Any>();
    for (const l of kuyrukOku(path.join(d.dataDir, 'kamp', 'tuyolar.jsonl'), 20000)) {
      try {
        const o = JSON.parse(l);
        if (o.olay === 'ekle') tuyo.set(o.id, { ...o });
        else if (o.olay === 'karar' && tuyo.has(o.id)) tuyo.get(o.id)!.durum = o.karar === 'onayla' ? 'onayli' : 'reddedildi';
      } catch { /* */ }
    }
    const oneri = [...tuyo.values()].filter((t) => t.durum === 'oneri');
    kaynaklar.tuyo = { toplam: oneri.length };
    for (const t of oneri) ekle({ tur: 'tuyo', kimlik: t.id, at: t.ts || '', baslik: `Kurul ${t.kurul} · ${t.brans}`, ayrinti: kirp(t.metin, 300), kim: t.kim || '', ek: t.ders_id || '', hedef: 'ogrenme/kamp' });

    gelenOnbellek = { at: Date.now(), satirlar, kaynaklar };
    return gelenOnbellek;
  };
  app.get('/api/admin/gelen', A, async (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    if (!s.sirala) s.sirala = 'at';
    if (req.query.taze === '1') gelenOnbellek = null;
    const g = await gelenTopla();
    res.setHeader('Cache-Control', 'no-store');
    res.json({
      ...diziSayfala(g.satirlar, s, {
        araMetni: (x) => `${x.baslik} ${x.ayrinti} ${x.kim} ${x.ek}`,
        siralayicilar: { at: (x) => x.at || '', tur: (x) => x.tur },
        suzgecler: { tur: (x, v) => x.tur === v },
        yuzler: { tur: (x) => x.tur },
      }),
      kaynaklar: g.kaynaklar,
    });
  });
  // H292: istemci hatası grubunu "görüldü" işaretle (yalnız Gelen'den düşer; günlük dosyasına dokunulmaz). 2 günden eski işaretler budanır.
  app.post('/api/admin/gelen/hata/goruldu', A, async (req, res) => {
    const kimlikler = (Array.isArray(req.body?.kimlikler) ? req.body.kimlikler : []).map((x: unknown) => String(x).slice(0, 80)).filter(Boolean).slice(0, 500);
    if (!kimlikler.length) return res.status(400).json({ error: 'kimlikler gerekli.' });
    const simdi = new Date().toISOString();
    const sinir = new Date(Date.now() - 2 * 86_400_000).toISOString();
    try {
      await atomikJsonGuncelle<Record<string, string>>(GORULDU, (eski) => {
        const v: Record<string, string> = {};
        for (const [k, at] of Object.entries(eski || {})) if (at >= sinir) v[k] = at;
        for (const k of kimlikler) v[k] = simdi;
        return v;
      });
      denetimHedef(res, `istemci-hata:${kimlikler.length === 1 ? kimlikler[0] : `${kimlikler.length} grup`}`);
      gelenOnbellekSil();
      res.json({ ok: true, n: kimlikler.length });
    } catch (e: any) { res.status(500).json({ error: e?.message || String(e) }); }
  });

  /* ================= Drive ================= */
  app.get('/api/admin/sistem/drive', A, (_req, res) => {
    const ayar = oku<Any>(path.join(d.dataDir, 'drive_sync_settings.json'), {});
    const son = oku<Any | null>(path.join(d.dataDir, 'drive_check_result.json'), null);
    const ogr = oku<Any | null>(path.join(d.dataDir, 'ogrenci_drive_envanter.json'), null);
    const kat = oku<Any | null>(path.join(d.dataDir, 'user_drive_catalog.json'), null);
    let ogrDosya = 0;
    const ogrKurul: Any[] = [];
    for (const [k, v] of Object.entries<Any>(ogr?.kurullar || {})) {
      let n = 0;
      for (const b of Object.values<Any>(v.branslar || {})) n += (b.dosyalar || []).length;
      ogrDosya += n;
      ogrKurul.push({ kurul: k, brans: Object.keys(v.branslar || {}).length, dosya: n });
    }
    const birim = (ad: string) => { try { return fs.existsSync(path.join(process.env.HOME || '', '.config/systemd/user', ad)); } catch { return false; } };
    res.setHeader('Cache-Control', 'no-store');
    res.json({
      ayar: { otomatik: ayar.autoSyncEnabled === true, aralik: ayar.syncInterval || 'manual', kapsam: ayar.preferredScope || ayar.scope || '', klasor: ayar.customFolderId || '', sonKontrol: ayar.lastCheckedAt || null, sonEsitleme: ayar.lastSyncedAt || null, durum: ayar.status || '', mesaj: ayar.message || '' },
      sonTarama: son ? { zaman: son.checkedAt, kapsam: son.scope, taranan: son.totalScanned, guncel: son.upToDateCount, yeni: son.newCount, var: son.hasUpdates } : null,
      ogrenci: ogr ? { zaman: ogr.taranma_zamani, kok: ogr.kok_id, dosya: ogrDosya, kurullar: ogrKurul } : null,
      katalog: kat ? { zaman: kat.updatedAt, kok: kat.rootFolderId, oge: kat.totalItems, pdf: kat.totalPdfs } : null,
      zamanlayici: { driveIzleyici: birim('meds-drive-izle.timer') },
    });
  });
  app.get('/api/admin/sistem/drive/dosyalar', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    const rows: Any[] = [];
    const son = oku<Any | null>(path.join(d.dataDir, 'drive_check_result.json'), null);
    for (const f of son?.newFiles || []) rows.push({ id: `tarama:${f.fullPath}`, kaynak: 'tarama', ad: f.name, yol: f.fullPath, tur: f.type || '', kurul: (String(f.committeeId || '').match(/kurul(\d)/) || [])[1] || '', durum: f.status || '' });
    const ogr = oku<Any | null>(path.join(d.dataDir, 'ogrenci_drive_envanter.json'), null);
    for (const [k, v] of Object.entries<Any>(ogr?.kurullar || {})) for (const [b, bv] of Object.entries<Any>(v.branslar || {})) for (const f of bv.dosyalar || [])
      rows.push({ id: `ogrenci:${f.id}`, kaynak: 'ogrenci', ad: f.name, yol: f.path || `${v.klasor_adi} / ${b} / ${f.name}`, tur: f.tur || f.uzanti || '', kurul: k, durum: '', driveId: f.id });
    const kat = oku<Any | null>(path.join(d.dataDir, 'user_drive_catalog.json'), null);
    for (const f of kat?.items || []) if (!f.isFolder) rows.push({ id: `okul:${f.id}`, kaynak: 'okul', ad: f.name, yol: f.fullPath, tur: f.mime === 'application/pdf' ? 'pdf' : f.mime || '', kurul: (String(f.fullPath || '').match(/Kurul\s*(\d)/i) || [])[1] || '', durum: '', driveId: f.id });
    res.json(diziSayfala(rows, s, {
      araMetni: (x) => `${x.ad} ${x.yol}`,
      siralayicilar: { ad: (x) => x.ad, kurul: (x) => x.kurul },
      suzgecler: { kaynak: (x, v) => x.kaynak === v, kurul: (x, v) => x.kurul === v, durum: (x, v) => x.durum === v },
      yuzler: { kaynak: (x) => x.kaynak, kurul: (x) => x.kurul || undefined, durum: (x) => x.durum || undefined },
    }));
  });

  /* ================= RAG ================= */
  const RAG_BETIK = path.join(d.rootDir, 'scripts/advanced_ai/rag_vektor_hatti.py');
  const RAG_PY = path.join(d.rootDir, '.venv-ocr/bin/python');
  const ragCihaz = () => fs.existsSync(RAG_BETIK) && fs.existsSync(RAG_PY) && !process.env.DERS_ISCI_URL;
  const RAG_LOG_DIR = path.join(KOK, 'meds_temp', 'logs');
  let ragIs: { id: string; baslama: string; bitis?: string; kod?: number | null; kuru: boolean; log: string; kim: string } | null = null;
  app.get('/api/admin/sistem/rag', A, (_req, res) => {
    const dbDir = process.env.MEDS_DATABASE_DIR || path.join(KOK, 'meds_database');
    const rapor = oku<Any | null>(path.join(dbDir, 'derived', 'rag_vektor', 'hat_rapor.json'), null);
    const hatDurum = oku<Any>(path.join(KOK, 'meds_temp/hat/durum.json'), {})?.rag_vektor || null;
    res.setHeader('Cache-Control', 'no-store');
    res.json({
      cihaz: ragCihaz(), rapor, hatDurum,
      cronLog: kuyrukOku(path.join(RAG_LOG_DIR, 'rag_vektor_hatti_cron.log'), 40),
      is: ragIs ? { ...ragIs, log: undefined, cikti: kuyrukOku(ragIs.log, 80) } : null,
    });
  });
  app.post('/api/admin/sistem/rag/denetle', A, (req, res) => {
    if (!ragCihaz()) return res.status(409).json({ error: 'Vektör denetimi yalnız cihazda (yerel meds-pg + bge-m3 servisi) çalışır.' });
    if (req.body?.onay !== 'DENETLE') return res.status(400).json({ error: 'Onay sözcüğü (DENETLE) gerekir.' });
    if (ragIs && ragIs.bitis === undefined) return res.status(409).json({ error: 'Bir denetim zaten çalışıyor.' });
    const kuru = req.body?.kuru !== false;
    fs.mkdirSync(RAG_LOG_DIR, { recursive: true });
    const id = new Date().toISOString().replace(/\D/g, '').slice(0, 14);
    const log = path.join(RAG_LOG_DIR, `rag_denetle_${id}.log`);
    const out = fs.openSync(log, 'a');
    const arg = [RAG_BETIK, '--denetle', ...(kuru ? ['--kuru'] : [])];
    const c = spawn('nice', ['-n', '10', RAG_PY, ...arg], { cwd: d.rootDir, env: { ...process.env, CUDA_VISIBLE_DEVICES: '' }, stdio: ['ignore', out, out] });
    const kim = String(req.headers['x-admin-email'] || (req as any).adminAuth?.via || 'yönetici');
    ragIs = { id, baslama: new Date().toISOString(), kuru, log, kim };
    const bu = ragIs;
    c.on('close', (kod) => { bu.bitis = new Date().toISOString(); bu.kod = kod; try { fs.closeSync(out); } catch { /* */ } });
    c.on('error', (e) => { bu.bitis = new Date().toISOString(); bu.kod = -1; try { fs.appendFileSync(log, `\n${e.message}\n`); } catch { /* */ } });
    console.log(`[rag] --denetle${kuru ? ' --kuru' : ''} elle başlatıldı (${kim})`);
    res.json({ success: true, id, kuru });
  });

  /* ================= Fazlar (salt okunur) ================= */
  app.get('/api/admin/sistem/fazlar/:kategori', A, async (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50, enFazla: 200 });
    const { explore } = await import('../phaseDataExplorer.ts');
    const r: Any = explore({ kategori: String(req.params.kategori), alan: String(req.query.alan || ''), deger: s.q, sirala: s.sirala, yon: s.yon, sayfa: s.sayfa + 1, boyut: Math.max(10, s.boyut) }, d.fazKok);
    if (r.hata) return res.status(404).json({ error: r.hata });
    res.json({ ogeler: (r.satirlar || []).map((x: Any, i: number) => ({ ...x, _id: `${x.soru_id}#${s.sayfa * s.boyut + i}` })), toplam: r.toplam, sayfa: s.sayfa, boyut: r.boyut, alanlar: r.alanlar, dagilim: r.dagilim });
  });

  /* ================= Bağlantılar: ders ↔ çıkmış ↔ slayt ↔ Öğren ↔ terim ================= */
  let bagOnbellek: { at: number; dersler: Any[]; sorular: Map<string, Any> } | null = null;
  const bagKur = async () => {
    if (bagOnbellek && Date.now() - bagOnbellek.at < 300_000) return bagOnbellek;
    const { explore } = await import('../phaseDataExplorer.ts');
    const hepsi = (kategori: string): Any[] => {
      const out: Any[] = [];
      for (let sayfa = 1; sayfa < 500; sayfa++) {
        const r: Any = explore({ kategori, alan: '', deger: '', sirala: '', yon: 'artan', sayfa, boyut: 200 }, () => '');
        if (r.hata || !(r.satirlar || []).length) break;
        out.push(...r.satirlar);
        if (out.length >= r.toplam) break;
      }
      return out;
    };
    const sorular = new Map<string, Any>();
    const soru = (id: string) => { let q = sorular.get(id); if (!q) { q = { id, ders: '', kurul: '', konu: '', kazanim: '', slayt: [], ogren: [], terim: [], kisaltma: [] }; sorular.set(id, q); } return q; };
    for (const r of hepsi('sinav_basligi')) { const q = soru(String(r.soru_id)); q.ders = r.ders || q.ders; q.kurul = String(r.kurul ?? q.kurul); q.konu = r.konu || q.konu; }
    for (const r of hepsi('mufredat')) { const q = soru(String(r.soru_id)); q.ders = q.ders || r.ders || ''; q.kurul = q.kurul || String(r.kurul ?? ''); q.konu = q.konu || r.konu || ''; q.kazanim = r.kazanim || ''; }
    for (const r of hepsi('slayt')) soru(String(r.soru_id)).slayt.push({ kaynak: r.kaynak, sayfa: r.sayfa, guven: r.guven });
    for (const r of hepsi('ogren')) soru(String(r.soru_id)).ogren.push({ deste: r.deste, slaytNo: r.slayt_no, slayt: r.slayt, guven: r.guven });
    for (const r of hepsi('terim')) { const t = Array.isArray(r.terimler) ? r.terimler : String(r.terimler || '').split(/[,;]\s*/); soru(String(r.soru_id)).terim.push(...t.filter(Boolean)); }
    for (const r of hepsi('kisaltma')) soru(String(r.soru_id)).kisaltma.push(`${r.kisaltma}${r.acilim ? ` = ${r.acilim}` : ''}`);
    if (d.cikmisListe) {
      const disiplin = new Map<string, Any>();
      for (const q of d.cikmisListe() || []) if (q?.id) disiplin.set(String(q.id), q);
      for (const q of sorular.values()) if (!q.ders) { const c = disiplin.get(q.id); if (c) { q.ders = c.discipline || ''; q.kurul = q.kurul || ((String(c.committeeId || '').match(/kurul[_-]?(\d)/) || [])[1] || ''); } }
    }
    const dm = new Map<string, Any>();
    for (const q of sorular.values()) {
      const ad = q.ders || '(ders belirsiz)';
      const x = dm.get(ad) || { id: ad, ders: ad, kurul: new Set<string>(), soru: 0, slayt: 0, ogren: 0, terim: 0, kaynak: new Set<string>() };
      x.soru++; if (q.kurul) x.kurul.add(q.kurul);
      if (q.slayt.length) x.slayt++;
      if (q.ogren.length) x.ogren++;
      if (q.terim.length || q.kisaltma.length) x.terim++;
      for (const s of q.slayt) if (s.kaynak) x.kaynak.add(String(s.kaynak));
      dm.set(ad, x);
    }
    const dersler = [...dm.values()].map((x) => ({ ...x, kurul: [...x.kurul].sort().join(', '), kaynak: x.kaynak.size }));
    bagOnbellek = { at: Date.now(), dersler, sorular };
    return bagOnbellek;
  };
  app.get('/api/admin/sistem/baglanti', A, async (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 100 });
    if (!s.sirala) s.sirala = 'soru';
    const b = await bagKur();
    res.json(diziSayfala(b.dersler, s, {
      araMetni: (x) => x.ders,
      siralayicilar: { soru: (x) => x.soru, ders: (x) => x.ders, slayt: (x) => x.slayt, ogren: (x) => x.ogren, terim: (x) => x.terim },
      suzgecler: { kurul: (x, v) => String(x.kurul).split(', ').includes(v) },
      yuzler: { kurul: (x) => String(x.kurul).split(', ').filter(Boolean) },
    }));
  });
  app.get('/api/admin/sistem/baglanti/:ders', A, async (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    const ders = String(req.params.ders);
    const b = await bagKur();
    const rows = [...b.sorular.values()].filter((q) => (q.ders || '(ders belirsiz)') === ders).map((q) => ({
      id: q.id, kurul: q.kurul, konu: q.konu, kazanim: q.kazanim, kok: kirp(d.fazKok(q.id), 140),
      slayt: q.slayt.slice(0, 2).map((x: Any) => `${x.kaynak}${x.sayfa ? ` s.${x.sayfa}` : ''}`).join(' · '), slaytN: q.slayt.length,
      ogren: q.ogren.slice(0, 2).map((x: Any) => `${x.deste}${x.slaytNo ? ` #${x.slaytNo}` : ''}`).join(' · '), ogrenN: q.ogren.length,
      terim: [...q.terim, ...q.kisaltma].slice(0, 5).join(', '),
      var: [q.slayt.length ? 'slayt' : '', q.ogren.length ? 'ogren' : '', q.terim.length || q.kisaltma.length ? 'terim' : ''].filter(Boolean),
    }));
    res.json(diziSayfala(rows, s, {
      araMetni: (x) => `${x.id} ${x.konu} ${x.kazanim} ${x.kok} ${x.terim}`,
      siralayicilar: { konu: (x) => x.konu, slaytN: (x) => x.slaytN, ogrenN: (x) => x.ogrenN },
      suzgecler: { var: (x, v) => (v.startsWith('-') ? !x.var.includes(v.slice(1)) : x.var.includes(v)) },
      yuzler: { var: (x) => x.var },
    }));
  });
}
