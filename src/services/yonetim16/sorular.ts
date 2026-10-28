/**
 * Yönetim v16 — Sorular grubu uçları (server-only). Belge: docs/YONETIM_V16_KIT.md, plan §3.3.
 *
 *   GET   /api/admin/sorular/havuz            sayfalı havuz (db.questions) — s.kurul s.ders s.durum s.kaynak s.gizli
 *   GET   /api/admin/sorular/havuz/:id        tam kayıt
 *   PATCH /api/admin/sorular/havuz/:id        izinli alanlar (gizle/göster = hidden) → saveQuestionLive
 *   GET   /api/admin/sorular/cikmis           sayfalı çıkmış (ham kayıt + site görünümü bayrakları) — s.yil s.kurul s.ders s.durum
 *   GET   /api/admin/sorular/cikmis/meta      süzgeç seçenekleri
 *   GET   /api/admin/sorular/cikmis/:id       ham kayıt + site görünümü + birleşme grubu + cevap anahtarı durumu
 *   PATCH /api/admin/sorular/cikmis/:id       izinli alanlar; içerik alanında kopya kardeşlere yazılır (syncPastMergeSiblings)
 *   GET   /api/admin/sorular/birlesen[/:id]   kopya grupları (sayfalı) / tek grup ayrıntısı
 *   GET   /api/admin/sorular/ham              ham soru defteri özetleri (salt okunur, sayfalı)
 *   GET   /api/admin/sorular/sikayet          soru şikâyetleri (çıkmış + havuz + örnek) — s.kaynak s.durum
 *   POST  /api/admin/sorular/sikayet/coz      {kaynak, soruId, raporId, durum:'resolved'|'pending'}
 *   GET   /api/admin/sorular/faz14            Faz 14 kullanıcı kuyruğu (salt görünüm; başlatma POST /api/admin/faz14-kuyruk/baslat, elle)
 *   GET   /api/admin/sorular/ornek[/:id]      örnek sorular (salt okunur)
 *   GET   /api/admin/sorular/olasi            olası soru setleri + soruları (salt okunur)
 *   GET   /api/admin/havuz-dondur             dondurma durumu
 *   PUT   /api/admin/havuz-dondur             {dondur, neden, onay:'DONDUR'|'AC'} — yalnız bayrak; silme yok
 *
 * Yazım kuralları: pastQuestions.json'un TEK yazıcısı server.ts::savePastQuestionsDb'dir (toplu, atomik rename);
 * burada ikinci yazıcı açılmaz. Havuz yazımı saveQuestionLive (ham defter koruması dahil). Küçük dosyalar atomikJson.
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import type express from 'express';
import { listeSorgusu, katla, type ListeSorgusu, type ListeYaniti } from './sayfalama';
import { atomikJsonGuncelle, atomikJsonYaz } from './atomikJson';
import { denetimFark, denetimHedef, denetimNot } from './denetim';
import { readMergeGroups, type MergeGroup } from '../questionMerge';
import { checkSolveStatus } from '../questionQuarantine';

type Any = Record<string, any>;

export type SorularDeps = {
  rootDir: string;
  dataDir: string;
  requireAdmin: express.RequestHandler;
  havuz: () => Any[];
  havuzKaydet: (q: Any) => void;
  cikmisHam: () => Any[];
  cikmisSitede: () => Any[];
  cikmisKaydet: (list: Any[]) => void;
  cikmisOnbellekSil: () => void;
  kardeslereYaz: (list: Any[], kaynakId: string, editor: string, govde?: Any) => Any[];
  cikmisAynala: (q: Any) => Promise<unknown>;
  havuzAynala?: (q: Any) => unknown;
  yayinla: (olay: string, veri: Any) => void;
  hamOzet: (id: string) => Any;
  hamKimlikler: () => string[];
  faz14Liste: () => Any[];
  icerikDuzenleme?: (q: Any) => { at: string; kind: string } | null;
  ayniGorunum?: (a: Any, b: Any) => boolean;
  kimOf: (req: express.Request) => string;
};

const clip = (s: unknown, n = 160) => { const t = String(s ?? '').replace(/\s+/g, ' ').trim(); return t.length > n ? `${t.slice(0, n - 1)}…` : t; };
const kurulNo = (c: unknown) => { const m = String(c || '').match(/kurul(\d)/); return m ? m[1] : String(c || '').includes('final') ? 'final' : String(c || '').includes('butunleme') ? 'butunleme' : ''; };
const stemOf = (q: Any) => (q.reconstruction && q.reconstruction.stem) || q.stem || q.rawStem || (q.fragments || []).find((f: Any) => f.type === 'stem')?.text || '';
const answerOf = (q: Any) => (q.reconstruction && q.reconstruction.correctAnswer) || q.correctAnswer || q.claimedAnswer || '';
const acikRapor = (r: Any) => !r?.status || r.status === 'pending' || r.status === 'open';

/** Önceden katlanmış metinle hızlı sayfalama (diziSayfala ile aynı yanıt biçimi) */
function sayfala<T extends Any>(rows: T[], s: ListeSorgusu, o: {
  suzgecler?: Record<string, (t: T, v: string) => boolean>;
  siralayicilar?: Record<string, (t: T) => string | number>;
  yuzler?: Record<string, (t: T) => string | string[] | undefined>;
  varsayilanSira?: string;
}): ListeYaniti<Any> {
  let list = rows;
  for (const [k, v] of Object.entries(s.suzgec)) { const f = o.suzgecler?.[k]; if (f) list = list.filter((t) => f(t, v)); }
  if (s.q) { const terms = katla(s.q).split(/\s+/).filter(Boolean); list = list.filter((t) => terms.every((x) => t._ara.includes(x))); }
  let yuzler: ListeYaniti<T>['yuzler'];
  if (o.yuzler) {
    yuzler = {};
    for (const [k, f] of Object.entries(o.yuzler)) {
      const m = new Map<string, number>();
      for (const t of list) { const v = f(t); for (const x of Array.isArray(v) ? v : v == null || v === '' ? [] : [v]) m.set(x, (m.get(x) || 0) + 1); }
      yuzler[k] = [...m].map(([deger, n]) => ({ deger, n })).sort((a, b) => b.n - a.n).slice(0, 60);
    }
  }
  const anahtar = s.sirala || o.varsayilanSira || '';
  const sr = anahtar && o.siralayicilar?.[anahtar];
  if (sr) {
    const d = s.yon === 'artan' ? 1 : -1;
    list = [...list].sort((a, b) => { const x = sr(a), y = sr(b); return (x < y ? -1 : x > y ? 1 : 0) * d; });
  }
  const ogeler = list.slice(s.sayfa * s.boyut, s.sayfa * s.boyut + s.boyut).map(({ _ara, ...r }) => r);
  return { ogeler, toplam: list.length, sayfa: s.sayfa, boyut: s.boyut, ...(yuzler ? { yuzler } : {}) };
}

const HAVUZ_IZINLI = ['topic', 'discipline', 'committeeId', 'questionNumber', 'status', 'tags', 'claimedAnswer', 'correctAnswer', 'reconstruction', 'hidden', 'adminNote', 'examYear'];
const CIKMIS_IZINLI = ['stem', 'options', 'correctAnswer', 'claimedAnswer', 'explanation', 'reconstruction', 'topic', 'discipline', 'committeeId', 'questionNumber', 'examYear', 'tags', 'hidden', 'adminNote'];
const kaynakOf = (q: Any) => (q.isPastExam ? 'cikmis' : q.contributedByUid ? 'ogrenci' : 'diger');

export function registerSorularRoutes(app: express.Express, d: SorularDeps) {
  const A = d.requireAdmin;

  // ---------------------------------------------------------------- Havuz
  let havuzIdx: { ref: Any[]; n: number; at: number; rows: Any[] } | null = null;
  const havuzSatirlari = () => {
    const list = d.havuz();
    if (havuzIdx && havuzIdx.ref === list && havuzIdx.n === list.length && Date.now() - havuzIdx.at < 5_000) return havuzIdx.rows;
    const rows = list.map((q) => ({
      id: String(q.id), kurul: kurulNo(q.committeeId), committeeId: q.committeeId || '', ders: q.discipline || '', konu: q.topic || '',
      no: Number(q.questionNumber) || 0, durum: q.status || '', kaynak: kaynakOf(q), gizli: !!q.hidden, kok: clip(stemOf(q)),
      cevap: answerOf(q), katki: Array.isArray(q.fragments) ? q.fragments.length : 0, sikayet: (q.reports || []).filter(acikRapor).length,
      yil: q.examYear || '', guncellendi: q.updatedAt || q.createdAt || '',
      _ara: katla(`${q.id} ${q.topic} ${q.discipline} ${stemOf(q)} ${(q.tags || []).join(' ')}`),
    }));
    havuzIdx = { ref: list, n: list.length, at: Date.now(), rows };
    return rows;
  };
  app.get('/api/admin/sorular/havuz', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    res.json(sayfala(havuzSatirlari(), s, {
      suzgecler: { kurul: (t, v) => t.kurul === v, ders: (t, v) => t.ders === v, durum: (t, v) => t.durum === v, kaynak: (t, v) => t.kaynak === v, gizli: (t, v) => t.gizli === (v === 'evet'), sikayet: (t) => t.sikayet > 0 },
      siralayicilar: { no: (t) => t.no, guncellendi: (t) => t.guncellendi, ders: (t) => t.ders, katki: (t) => t.katki },
      yuzler: { kurul: (t) => t.kurul, ders: (t) => t.ders, durum: (t) => t.durum, kaynak: (t) => t.kaynak, gizli: (t) => (t.gizli ? 'evet' : 'hayir') },
      varsayilanSira: 'guncellendi',
    }));
  });
  app.get('/api/admin/sorular/havuz/:id', A, (req, res) => {
    const q = d.havuz().find((x) => String(x.id) === req.params.id);
    if (!q) return res.status(404).json({ error: 'Havuz sorusu bulunamadı.' });
    res.json({ kayit: q });
  });
  app.patch('/api/admin/sorular/havuz/:id', A, (req, res) => {
    const q = d.havuz().find((x) => String(x.id) === req.params.id);
    if (!q) return res.status(404).json({ error: 'Havuz sorusu bulunamadı.' });
    const yama = Object.fromEntries(Object.entries(req.body?.yama || {}).filter(([k]) => HAVUZ_IZINLI.includes(k)));
    if (!Object.keys(yama).length) return res.status(400).json({ error: 'Düzenlenebilir alan yok.' });
    const once = Object.fromEntries(Object.keys(yama).map((k) => [k, q[k] ?? null]));
    Object.assign(q, yama, { updatedAt: new Date().toISOString() });
    d.havuzKaydet(q);
    havuzIdx = null;
    denetimHedef(res, `soru:${q.id}`);
    denetimFark(res, once, yama);
    res.json({ success: true, kayit: q });
  });

  // ---------------------------------------------------------------- Çıkmış
  let cikIdx: { ham: Any[]; site: Any[]; mg: MergeGroup[]; rows: Any[] } | null = null;
  const cikmisSatirlari = () => {
    const ham = d.cikmisHam();
    const site = d.cikmisSitede();
    const mg = readMergeGroups();
    // ham: getPastQuestionsDb sığ kopya döner → kimlik karşılaştırması için uzunluk + ilk/son öge yeterli değil; site listesi
    // her kayıtta yeniden kurulur (sürüm anahtarı), bu yüzden site referansı değişmediyse dizin geçerlidir.
    if (cikIdx && cikIdx.site === site && cikIdx.mg === mg && cikIdx.ham.length === ham.length) return cikIdx.rows;
    const siteMap = new Map<string, Any>();
    const gosterenOf = new Map<string, string>();
    for (const q of site) { siteMap.set(String(q.id), q); for (const h of q.mergedFrom || []) gosterenOf.set(String(h), String(q.id)); }
    const grupOf = new Map<string, MergeGroup>();
    for (const g of mg) if (g.durum !== 'ayrildi') for (const u of g.uyeler) grupOf.set(u, g);
    const rows = ham.map((q) => {
      const id = String(q.id);
      const sv = siteMap.get(id);
      const g = grupOf.get(id);
      const cs = checkSolveStatus(q);
      const karantina = !!sv?.isQuarantined || cs === 'karantina';
      const sitede = sv ? (karantina ? 'karantina' : 'gorunur') : gosterenOf.has(id) ? 'birlesik' : 'yok';
      const durumlar: string[] = [];
      if (karantina) durumlar.push('karantina');
      if (q.hidden) durumlar.push('gizli');
      if (g) durumlar.push(g.asil === id ? 'asil' : 'kopya');
      if (cs === 'onayli') durumlar.push('onayli');
      if (q.phase14 || (q.tags || []).includes('faz14_duzeltildi')) durumlar.push('faz14');
      const sikayet = (q.reports || []).filter(acikRapor).length;
      if (sikayet) durumlar.push('sikayet');
      if (!answerOf(q)) durumlar.push('cevapsiz');
      return {
        id, kurul: kurulNo(q.committeeId), committeeId: q.committeeId || '', ders: q.discipline || '', konu: q.topic || '',
        yil: String(q.examYear || 'Bilinmiyor'), no: Number(q.questionNumber) || 0, kok: clip(stemOf(q)), cevap: answerOf(q),
        sitede, durumlar, grup: g?.id || '', sikayet, gizli: !!q.hidden, kalite: q.qualityTier || '', guncellendi: q.updatedAt || '',
        _ara: katla(`${id} ${q.topic} ${q.discipline} ${stemOf(q)} ${q.examYear || ''} ${q.sinavKimligi || ''}`),
      };
    });
    cikIdx = { ham, site, mg, rows };
    return rows;
  };
  app.get('/api/admin/sorular/cikmis/meta', A, (_req, res) => {
    const rows = cikmisSatirlari();
    const say = (f: (r: Any) => string | string[]) => {
      const m = new Map<string, number>();
      for (const r of rows) for (const v of ([] as string[]).concat(f(r))) if (v) m.set(v, (m.get(v) || 0) + 1);
      return [...m].map(([deger, n]) => ({ deger, n })).sort((a, b) => a.deger.localeCompare(b.deger, 'tr'));
    };
    res.json({ toplam: rows.length, yil: say((r) => r.yil), kurul: say((r) => r.kurul), ders: say((r) => r.ders), durum: say((r) => r.durumlar) });
  });
  app.get('/api/admin/sorular/cikmis', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    res.json(sayfala(cikmisSatirlari(), s, {
      suzgecler: { yil: (t, v) => t.yil === v, kurul: (t, v) => t.kurul === v, ders: (t, v) => t.ders === v, durum: (t, v) => t.durumlar.includes(v), sitede: (t, v) => t.sitede === v, grup: (t, v) => t.grup === v },
      siralayicilar: { no: (t) => t.no, guncellendi: (t) => t.guncellendi, yil: (t) => t.yil, ders: (t) => t.ders, sikayet: (t) => t.sikayet },
      yuzler: { yil: (t) => t.yil, kurul: (t) => t.kurul, durum: (t) => t.durumlar, sitede: (t) => t.sitede },
      varsayilanSira: 'guncellendi',
    }));
  });
  app.get('/api/admin/sorular/cikmis/:id', A, (req, res) => {
    const id = String(req.params.id);
    const q = d.cikmisHam().find((x) => String(x.id) === id);
    if (!q) return res.status(404).json({ error: 'Çıkmış soru bulunamadı.' });
    const site = d.cikmisSitede();
    const sv = site.find((x) => String(x.id) === id) || null;
    const gosteren = sv ? null : site.find((x) => (x.mergedFrom || []).map(String).includes(id)) || null;
    const g = readMergeGroups().find((x) => x.uyeler.includes(id)) || null;
    res.json({
      kayit: q,
      site: sv ? { durum: sv.isQuarantined ? 'karantina' : 'gorunur', karantinaNedeni: sv.quarantineReasons || [], cevapDurumu: sv.answerStatus || null, cevapNotu: sv.answerNote || null, cevapSupheli: !!sv.answerDoubtful, cevap: answerOf(sv) }
        : gosteren ? { durum: 'birlesik', gosteren: String(gosteren.id) } : { durum: 'yok' },
      grup: g,
      checkSolve: q.checkSolve ? { durum: q.checkSolve.status, at: q.checkSolve.at, gerekce: q.checkSolve.karantinaGerekcesi || null } : null,
    });
  });
  app.patch('/api/admin/sorular/cikmis/:id', A, (req, res) => {
    const id = String(req.params.id);
    const list = d.cikmisHam();
    const idx = list.findIndex((x) => String(x.id) === id);
    if (idx === -1) return res.status(404).json({ error: 'Çıkmış soru bulunamadı.' });
    const yama = Object.fromEntries(Object.entries(req.body?.yama || {}).filter(([k]) => CIKMIS_IZINLI.includes(k)));
    if (!Object.keys(yama).length) return res.status(400).json({ error: 'Düzenlenebilir alan yok.' });
    // "Boş sonuçla ezme" kuralı: içerik alanı boşa çekilemez
    for (const k of ['stem', 'options', 'correctAnswer', 'explanation']) {
      const v = (yama as Any)[k];
      if (k in yama && (v == null || (typeof v === 'string' && !v.trim()) || (Array.isArray(v) && !v.length))) return res.status(400).json({ error: `${k} boş bırakılamaz.` });
    }
    const eski = list[idx];
    const once = Object.fromEntries(Object.keys(yama).map((k) => [k, eski[k] ?? null]));
    const kim = d.kimOf(req);
    const rev = { editedAt: new Date().toISOString(), editorName: `Yönetim v16 (${kim})`, editorRole: 'admin', changeSummary: `Alanlar: ${Object.keys(yama).join(', ')}`, before: once };
    // Revizyon yalnız içerik alanında; null = meta alanını kaldır (adminNote, hidden, tags…)
    const icerikMi = Object.keys(yama).some((k) => ['stem', 'options', 'correctAnswer', 'claimedAnswer', 'explanation', 'reconstruction'].includes(k));
    const yeni: Any = { ...eski, ...yama, id, updatedAt: new Date().toISOString(), ...(icerikMi ? { revisions: [...(Array.isArray(eski.revisions) ? eski.revisions : []), rev].slice(-30) } : {}) };
    for (const [k, v] of Object.entries(yama)) if (v === null) delete yeni[k];
    list[idx] = yeni;
    const kardes = req.body?.kardeslereYaz === false ? [] : d.kardeslereYaz(list, id, `Yönetim v16 (${kim})`, yama);
    d.cikmisKaydet(list);
    d.cikmisOnbellekSil();
    cikIdx = null;
    d.cikmisAynala(yeni).catch(() => {});
    d.yayinla('past_question_updated', { question: yeni, id, time: Date.now() });
    denetimHedef(res, `soru:${id}`);
    denetimFark(res, once, yama);
    if (kardes.length) denetimNot(res, { kardeslereYazildi: kardes.map((x) => x.id) });
    res.json({ success: true, kayit: yeni, kardesler: kardes.map((x) => String(x.id)) });
  });

  // ---------------------------------------------------------------- Birleşenler
  const grupSatiri = (g: MergeGroup) => ({ id: g.id, asil: g.asil, uye: g.uyeler.length, durum: g.durum, birebir: !!g.birebir_ayni, benzerlik: g.benzerlik, olusturma: g.olusturma || '', karar: g.karar_zamani || '' });
  app.get('/api/admin/sorular/birlesen', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    const ham = new Map(d.cikmisHam().map((q) => [String(q.id), q]));
    const rows = readMergeGroups().map((g) => {
      const q = ham.get(g.asil) || {};
      return { ...grupSatiri(g), kok: clip(stemOf(q), 140), ders: q.discipline || '', kurul: kurulNo(q.committeeId), _ara: katla(`${g.id} ${g.uyeler.join(' ')} ${stemOf(q)} ${q.discipline || ''}`) };
    });
    res.json(sayfala(rows, s, {
      suzgecler: { durum: (t, v) => t.durum === v, birebir: (t, v) => t.birebir === (v === 'evet'), kurul: (t, v) => t.kurul === v },
      siralayicilar: { uye: (t) => t.uye, benzerlik: (t) => t.benzerlik, olusturma: (t) => t.olusturma },
      yuzler: { durum: (t) => t.durum, birebir: (t) => (t.birebir ? 'evet' : 'hayir'), kurul: (t) => t.kurul },
      varsayilanSira: 'olusturma',
    }));
  });
  app.get('/api/admin/sorular/birlesen/:id', A, (req, res) => {
    const g = readMergeGroups().find((x) => x.id === req.params.id);
    if (!g) return res.status(404).json({ error: 'Grup bulunamadı.' });
    const ham = new Map(d.cikmisHam().map((q) => [String(q.id), q]));
    const shownOf = new Map<string, string>();
    for (const q of d.cikmisSitede()) { shownOf.set(String(q.id), String(q.id)); for (const h of q.mergedFrom || []) shownOf.set(String(h), String(q.id)); }
    const gorunen = g.durum === 'ayrildi' ? null : shownOf.get(g.asil) || g.uyeler.map((u) => shownOf.get(u)).find(Boolean) || null;
    const shownQ = gorunen ? ham.get(gorunen) : null;
    const sorular = g.uyeler.map((id) => {
      const q: Any = ham.get(id) || {};
      const rec = q.reconstruction && typeof q.reconstruction === 'object' ? q.reconstruction : {};
      const opts = (Array.isArray(rec.options) && rec.options.length ? rec.options : q.options) || [];
      const edit = d.icerikDuzenleme?.(q) || null;
      return {
        id, var: ham.has(id), stem: rec.stem || q.stem || '', options: opts.map((o: Any) => (typeof o === 'string' ? o : o?.text || '')),
        correctAnswer: rec.correctAnswer || q.correctAnswer || '', committeeId: q.committeeId || '', discipline: q.discipline || '', year: q.examYear || '',
        source: q.sourceFile || q.source || '', duzenleme: edit,
        ayrisik: !!(shownQ && id !== gorunen && ham.get(id) && edit && edit.at > String(g.olusturma || '') && d.ayniGorunum && !d.ayniGorunum(q, shownQ)),
      };
    });
    res.json({ grup: { ...g, gorunen, ayrisik: sorular.some((x) => x.ayrisik) }, sorular });
  });

  // ---------------------------------------------------------------- Ham defter (salt okunur)
  let hamIdx: { at: number; rows: Any[] } | null = null;
  app.get('/api/admin/sorular/ham', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    if (!hamIdx || Date.now() - hamIdx.at > 60_000 || req.query.taze) {
      const rows = d.hamKimlikler().map((id) => {
        try {
          const o = d.hamOzet(id);
          const katkı = Object.values(o.counts || {}).reduce((a: number, b: any) => a + (Number(b) || 0), 0);
          return { id, baslik: clip(o.title, 160), kurul: kurulNo(o.committeeId), ders: o.discipline || '', no: Number(o.questionNumber) || 0, silinmis: !!o.deleted, katki: katkı, yz: o.aiCount || 0, olay: o.eventCount ?? o.totalEvents ?? null, son: o.lastEventAt || o.lastTs || '', _ara: katla(`${id} ${o.title} ${o.discipline || ''}`) };
        } catch { return { id, baslik: id, kurul: '', ders: '', no: 0, silinmis: false, katki: 0, yz: 0, olay: null, son: '', _ara: katla(id) }; }
      });
      hamIdx = { at: Date.now(), rows };
    }
    res.json(sayfala(hamIdx.rows as any, s, {
      suzgecler: { kurul: (t: Any, v) => t.kurul === v, silinmis: (t: Any, v) => t.silinmis === (v === 'evet'), ders: (t: Any, v) => t.ders === v },
      siralayicilar: { katki: (t: Any) => t.katki, no: (t: Any) => t.no, son: (t: Any) => t.son, yz: (t: Any) => t.yz },
      yuzler: { kurul: (t: Any) => t.kurul, silinmis: (t: Any) => (t.silinmis ? 'evet' : 'hayir') },
      varsayilanSira: 'katki',
    }));
  });

  // ---------------------------------------------------------------- Şikâyetler (soru tarafı)
  const ORNEK_BILDIRIM = path.join(d.dataDir, 'ornek_soru_bildirimleri.jsonl');
  const ORNEK_DURUM = path.join(d.dataDir, 'ornek_soru_bildirim_durum.json');
  const ornekRaporlari = (): Any[] => {
    let durum: Any = {};
    try { durum = JSON.parse(fs.readFileSync(ORNEK_DURUM, 'utf8')); } catch { durum = {}; }
    let satirlar: string[] = [];
    try { satirlar = fs.readFileSync(ORNEK_BILDIRIM, 'utf8').split('\n'); } catch { satirlar = []; }
    const out: Any[] = [];
    for (const l of satirlar) {
      if (!l.trim()) continue;
      try {
        const r = JSON.parse(l);
        const rid = 'orn-' + crypto.createHash('sha1').update(l).digest('hex').slice(0, 12);
        out.push({ ...r, id: rid, status: durum[rid]?.status || 'pending', resolvedAt: durum[rid]?.at });
      } catch { /* bozuk satır */ }
    }
    return out;
  };
  const tumSikayetler = () => {
    const rows: Any[] = [];
    const ekle = (kaynak: string, q: Any, r: Any, i: number) => rows.push({
      id: `${kaynak}:${q.id}:${r.id || i}`, raporId: String(r.id || i), kaynak, soruId: String(q.id), ders: q.discipline || '', kurul: kurulNo(q.committeeId),
      neden: clip(r.reason || 'Hata bildirimi', 120), ayrinti: clip(r.details || '', 400), kim: r.reportedBy || 'Anonim', at: r.timestamp || r.createdAt || '',
      durum: acikRapor(r) ? 'acik' : 'cozuldu', kok: clip(stemOf(q), 120),
      _ara: katla(`${q.id} ${r.reason || ''} ${r.details || ''} ${q.discipline || ''} ${r.reportedBy || ''}`),
    });
    for (const q of d.cikmisHam()) (q.reports || []).forEach((r: Any, i: number) => ekle('cikmis', q, r, i));
    for (const q of d.havuz()) (q.reports || []).forEach((r: Any, i: number) => ekle('havuz', q, r, i));
    for (const r of ornekRaporlari()) ekle('ornek', { id: r.soru_id, discipline: '', committeeId: `kurul${String(r.soru_id).match(/^k(\d)/)?.[1] || ''}` }, r, 0);
    return rows;
  };
  app.get('/api/admin/sorular/sikayet', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    if (!('durum' in s.suzgec)) s.suzgec.durum = 'acik';
    if (s.suzgec.durum === 'hepsi') delete s.suzgec.durum;
    res.json(sayfala(tumSikayetler(), s, {
      suzgecler: { kaynak: (t, v) => t.kaynak === v, durum: (t, v) => t.durum === v, kurul: (t, v) => t.kurul === v },
      siralayicilar: { at: (t) => t.at, kaynak: (t) => t.kaynak },
      yuzler: { kaynak: (t) => t.kaynak, kurul: (t) => t.kurul },
      varsayilanSira: 'at',
    }));
  });
  app.post('/api/admin/sorular/sikayet/coz', A, async (req, res) => {
    const { kaynak, soruId, raporId } = req.body || {};
    const durum = req.body?.durum === 'pending' ? 'pending' : 'resolved';
    const kim = d.kimOf(req);
    const isaretle = (r: Any) => (durum === 'resolved' ? { ...r, status: 'resolved', resolvedAt: new Date().toISOString(), resolvedBy: kim } : { ...r, status: 'pending', resolvedAt: undefined, resolvedBy: undefined });
    denetimHedef(res, `soru:${soruId}`);
    try {
      if (kaynak === 'cikmis') {
        const list = d.cikmisHam();
        const q = list.find((x) => String(x.id) === String(soruId));
        if (!q) return res.status(404).json({ error: 'Soru bulunamadı.' });
        let bulundu = false;
        q.reports = (q.reports || []).map((r: Any, i: number) => (String(r.id || i) === String(raporId) ? ((bulundu = true), isaretle(r)) : r));
        if (!bulundu) return res.status(404).json({ error: 'Bildirim bulunamadı.' });
        q.updatedAt = new Date().toISOString();
        d.cikmisKaydet(list);
        d.cikmisOnbellekSil();
        cikIdx = null;
        d.cikmisAynala(q).catch(() => {});
      } else if (kaynak === 'havuz') {
        const q = d.havuz().find((x) => String(x.id) === String(soruId));
        if (!q) return res.status(404).json({ error: 'Soru bulunamadı.' });
        let bulundu = false;
        q.reports = (q.reports || []).map((r: Any, i: number) => (String(r.id || i) === String(raporId) ? ((bulundu = true), isaretle(r)) : r));
        if (!bulundu) return res.status(404).json({ error: 'Bildirim bulunamadı.' });
        d.havuzKaydet(q);
        havuzIdx = null;
      } else if (kaynak === 'ornek') {
        // Bildirim defteri (jsonl) yalnız eklenir; durum ayrı dosyada tutulur
        await atomikJsonGuncelle<Any>(ORNEK_DURUM, (eski) => ({ ...(eski || {}), [String(raporId)]: { status: durum, at: new Date().toISOString(), by: kim } }));
      } else return res.status(400).json({ error: 'Geçersiz kaynak.' });
      d.yayinla('reports_changed', { kaynak, soruId, raporId, durum, time: Date.now() });
      res.json({ success: true });
    } catch (e: any) { res.status(500).json({ error: e?.message || String(e) }); }
  });

  // ---------------------------------------------------------------- Faz 14 kuyruğu (salt görünüm)
  app.get('/api/admin/sorular/faz14', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    const rows = d.faz14Liste().map((i) => ({
      id: String(i.id), soruId: String(i.questionId || ''), durum: i.status || '', not: (i.notes || []).length, son: i.updatedAt || i.createdAt || '',
      ilkNot: clip(i.notes?.[0]?.message || i.notes?.[0]?.reason || '', 160), kim: i.notes?.[0]?.name || '', olusturma: i.createdAt || '',
      _ara: katla(`${i.id} ${i.questionId} ${(i.notes || []).map((n: Any) => `${n.reason || ''} ${n.message || ''} ${n.name || ''}`).join(' ')}`),
    }));
    res.json(sayfala(rows, s, {
      suzgecler: { durum: (t, v) => t.durum === v },
      siralayicilar: { son: (t) => t.son, not: (t) => t.not },
      yuzler: { durum: (t) => t.durum },
      varsayilanSira: 'son',
    }));
  });

  // ---------------------------------------------------------------- Örnek sorular (salt okunur)
  let ornekCache: { at: number; rows: Any[] } | null = null;
  const ornekSorular = () => {
    if (ornekCache && Date.now() - ornekCache.at < 60_000) return ornekCache.rows;
    const out: Any[] = [];
    const dir = path.join(d.rootDir, 'src', 'data', 'ornek_sorular');
    const bildirim = new Map<string, number>();
    for (const r of ornekRaporlari()) if (r.status !== 'resolved') bildirim.set(r.soru_id, (bildirim.get(r.soru_id) || 0) + 1);
    for (const k of fs.existsSync(dir) ? fs.readdirSync(dir) : []) {
      const kd = path.join(dir, k);
      try { if (!fs.statSync(kd).isDirectory()) continue; } catch { continue; }
      for (const f of fs.readdirSync(kd)) {
        if (!f.endsWith('.json') || f === 'index.json') continue;
        let ders: Any;
        try { ders = JSON.parse(fs.readFileSync(path.join(kd, f), 'utf8')); } catch { continue; }
        for (const kz of ders.kazanimlar || []) for (const q of kz.sorular || []) {
          out.push({
            id: String(q.id), kurul: String(q.id).match(/^k(\d)/)?.[1] || String(ders.kurul || k.replace(/\D/g, '')), dersId: ders.id || f.replace(/\.json$/, ''), ders: ders.ders || '', konu: ders.konu || '',
            soru: clip(q.soru, 200), zorluk: q.zorluk || '', cevap: q.dogru_cevap || q.cevap || '', kazanim: clip(kz.metin, 160), bildirim: bildirim.get(String(q.id)) || 0,
            _kayit: q, _ara: katla(`${q.id} ${q.soru} ${ders.ders} ${ders.konu} ${kz.metin}`),
          });
        }
      }
    }
    ornekCache = { at: Date.now(), rows: out };
    return out;
  };
  app.get('/api/admin/sorular/ornek', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    const r = sayfala(ornekSorular(), s, {
      suzgecler: { kurul: (t, v) => t.kurul === v, ders: (t, v) => t.ders === v, zorluk: (t, v) => t.zorluk === v, bildirim: (t) => t.bildirim > 0 },
      siralayicilar: { id: (t) => t.id, bildirim: (t) => t.bildirim },
      yuzler: { kurul: (t) => t.kurul, ders: (t) => t.ders, zorluk: (t) => t.zorluk },
      varsayilanSira: 'id',
    });
    res.json({ ...r, ogeler: r.ogeler.map(({ _kayit, ...x }: Any) => x) });
  });
  app.get('/api/admin/sorular/ornek/:id', A, (req, res) => {
    const x = ornekSorular().find((r) => r.id === req.params.id);
    if (!x) return res.status(404).json({ error: 'Örnek soru bulunamadı.' });
    const { _ara, _kayit, ...ozet } = x;
    res.json({ ozet, kayit: _kayit, bildirimler: ornekRaporlari().filter((r) => r.soru_id === x.id) });
  });

  // ---------------------------------------------------------------- Olası sorular (salt okunur)
  app.get('/api/admin/sorular/olasi', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    const dir = path.join(d.rootDir, 'data', 'olasi_sorular');
    const setler: Any[] = [];
    const rows: Any[] = [];
    for (let k = 1; k <= 6; k++) {
      let set: Any = {};
      try { set = JSON.parse(fs.readFileSync(path.join(dir, `k${k}.json`), 'utf8')); } catch { continue; }
      const gb = new Map<string, Any>();
      try {
        for (const l of fs.readFileSync(path.join(dir, `geri_bildirim_k${k}.jsonl`), 'utf8').split('\n')) {
          if (!l.trim()) continue;
          try { const r = JSON.parse(l); const o = gb.get(r.id) || { boyleydi: 0, degildi: 0, duzeltme: 0 }; o[r.karar] = (o[r.karar] || 0) + 1; gb.set(String(r.id), o); } catch { /* */ }
        }
      } catch { /* geri bildirim yok */ }
      setler.push({ kurul: k, soru: (set.sorular || []).length, uretildi: set.uretildi || null });
      for (const q of set.sorular || []) {
        const g = gb.get(String(q.id)) || { boyleydi: 0, degildi: 0, duzeltme: 0 };
        rows.push({ id: String(q.id), kurul: String(k), ders: q.ders || q.discipline || '', soru: clip(q.soru || q.stem || q.metin, 200), olasilik: q.olasilik ?? q.puan ?? null, ...g, _ara: katla(`${q.id} ${q.soru || q.stem || ''} ${q.ders || ''}`) });
      }
    }
    res.json({ setler, ...sayfala(rows, s, {
      suzgecler: { kurul: (t, v) => t.kurul === v, ders: (t, v) => t.ders === v },
      siralayicilar: { olasilik: (t) => Number(t.olasilik) || 0, boyleydi: (t) => t.boyleydi, degildi: (t) => t.degildi },
      yuzler: { kurul: (t) => t.kurul, ders: (t) => t.ders },
      varsayilanSira: 'olasilik',
    }) });
  });

  // ---------------------------------------------------------------- Havuz dondurma
  const DONDUR = path.join(d.dataDir, 'havuz_dondur.json');
  const dondurOku = () => { try { return { var: true, ...JSON.parse(fs.readFileSync(DONDUR, 'utf8')) }; } catch { return { var: false, dondur: false }; } };
  app.get('/api/admin/havuz-dondur', A, (_req, res) => res.json(dondurOku()));
  app.put('/api/admin/havuz-dondur', A, async (req, res) => {
    const dondur = req.body?.dondur === true;
    const beklenen = dondur ? 'DONDUR' : 'AC';
    if (String(req.body?.onay || '') !== beklenen) return res.status(400).json({ error: `Onay sözcüğü gerekli: ${beklenen}` });
    const once = dondurOku();
    const { var: _v, ...onceki } = once as Any;
    const yeni = { ...onceki, dondur, neden: clip(req.body?.neden || onceki.neden || '', 500), [dondur ? 'baslangic' : 'bitis']: new Date().toISOString(), guncelleyen: d.kimOf(req) };
    await atomikJsonYaz(DONDUR, yeni, { yedek: 3 });
    denetimHedef(res, 'havuz-dondur');
    denetimFark(res, { dondur: !!onceki.dondur }, { dondur });
    d.yayinla('havuz_dondur_changed', { dondur, time: Date.now() });
    res.json({ success: true, ...yeni });
  });
}
