/**
 * Yönetim v16 — önceden "yakında" kalan küçük sayfaların uçları (2026-10-28):
 *  - Sorular › Taslaklar        GET /api/admin/sorular/taslak            (havuzdaki eksik/birleştirilmiş taslaklar, salt okunur)
 *  - Kullanıcılar › Gizlilik    GET /api/admin/gizlilik, PUT /api/admin/gizlilik/:id, öğrenci POST /api/gizlilik/talep
 *  - Oyunlar › Quiz havuzu      GET /api/admin/quiz/havuz[/:id]          (meds_database_v2/ders_isci/yayinlanan/<ders>/quiz_havuzu.json)
 *  - Öğrenme › Ses kuyruğu      GET /api/admin/sesli-kuyruk               (data/sesli_anlatim/kuyruk.json; eylemler eski uçtan, elle)
 * LLM/ses üretimi BAŞLATAN uç yok (kural 20): kuyruk eylemleri mevcut /api/sesli-anlatim/kuyruk/:id/:eylem ucundadır.
 */
import type express from 'express';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { diziSayfala, listeSorgusu } from './sayfalama.ts';
import { atomikJsonGuncelle } from './atomikJson.ts';
import { denetimFark, denetimHedef } from './denetim.ts';

type Any = Record<string, any>;
const oku = <T,>(f: string, v: T): T => { try { return JSON.parse(fs.readFileSync(f, 'utf8')) as T; } catch { return v; } };
const kirp = (s: unknown, n = 200) => String(s ?? '').replace(/\s+/g, ' ').trim().slice(0, n);
const kurulNo = (c: unknown) => (String(c || '').match(/kurul[_-]?(\d)/) || [])[1] || '';

export type EkSayfaDeps = {
  rootDir: string;
  dataDir: string;
  requireAdmin: express.RequestHandler;
  havuz: () => Any[];
  /** Doğrulanmış öğrenci (Firebase jetonu) → { uid, email } ya da null */
  dogrulanmisKisi: (req: express.Request) => { uid: string; email: string } | null;
  broadcastAdmin: (olay: string, veri: Any) => void;
};

export function registerEkSayfa16Routes(app: express.Express, d: EkSayfaDeps) {
  const A = d.requireAdmin;

  /* ================= Taslaklar (salt okunur görünüm; kümeleme aracı ?kabuk=v14 Taslaklar'da) ================= */
  const stemOf = (q: Any) => q.reconstruction?.stem || q.stem || q.rawStem || (q.fragments || [])[0]?.text || '';
  const birlesikMi = (q: Any) => (q.tags || []).includes('taslak-birlestirildi') || q.isMerged || (q.mergedSatellites || []).length > 0;
  const taslakTuru = (q: Any): 'birlesik' | 'eksik' | null => {
    if (birlesikMi(q)) return 'birlesik';
    const secenek = (q.reconstruction?.options || q.options || []).filter((o: Any) => String(o?.text || '').trim()).length;
    const cevap = q.reconstruction?.correctAnswer || q.correctAnswer;
    if (!q.reconstruction?.stem || secenek < 4 || !cevap) return 'eksik';
    return null;
  };
  app.get('/api/admin/sorular/taslak', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    const rows: Any[] = [];
    for (const q of d.havuz()) {
      if (q.deleted || q.isDeleted) continue;
      const tur = taslakTuru(q);
      if (!tur) continue;
      rows.push({
        id: String(q.id), tur, kurul: kurulNo(q.committeeId), ders: q.discipline || '', no: Number(q.questionNumber) || 0,
        metin: kirp(stemOf(q), 200), parca: (q.fragments || []).length, uydu: (q.mergedSatellites || []).length,
        at: q.updatedAt || q.createdAt || '',
      });
    }
    res.setHeader('Cache-Control', 'no-store');
    res.json(diziSayfala(rows, s, {
      araMetni: (x) => `${x.id} ${x.metin} ${x.ders}`,
      siralayicilar: { at: (x) => x.at, no: (x) => x.no, parca: (x) => x.parca },
      suzgecler: { tur: (x, v) => x.tur === v, kurul: (x, v) => x.kurul === v },
      yuzler: { tur: (x) => x.tur, kurul: (x) => x.kurul },
    }));
  });

  /* ================= Gizlilik talepleri (KVKK: veri dışa aktarma / silme) ================= */
  // Kişisel veri: data/gizlilik_talepleri.json (gitignore). Öğrenci talebi yalnız doğrulanmış oturumla; e-posta istemciden alınmaz.
  const GIZ = path.join(d.dataDir, 'gizlilik_talepleri.json');
  const TURLER = new Set(['disa-aktar', 'sil', 'duzelt']);
  const DURUMLAR = new Set(['bekliyor', 'isleniyor', 'tamam', 'reddedildi']);
  app.post('/api/gizlilik/talep', async (req, res) => {
    const k = d.dogrulanmisKisi(req);
    if (!k) return res.status(401).json({ error: 'Giriş gerekli.' });
    const tur = String(req.body?.tur || '');
    if (!TURLER.has(tur)) return res.status(400).json({ error: 'Talep türü geçersiz.' });
    const liste = oku<Any[]>(GIZ, []);
    if (liste.some((x) => x.uid === k.uid && x.tur === tur && (x.durum === 'bekliyor' || x.durum === 'isleniyor')))
      return res.status(409).json({ error: 'Bu türde açık bir talebin zaten var.' });
    const kayit = { id: `gz-${Date.now().toString(36)}-${crypto.randomBytes(2).toString('hex')}`, at: new Date().toISOString(), uid: k.uid, email: k.email, tur, not: kirp(req.body?.not, 1000), durum: 'bekliyor' };
    await atomikJsonGuncelle<Any[]>(GIZ, (eski) => [...(Array.isArray(eski) ? eski : []), kayit]);
    d.broadcastAdmin('gizlilik_changed', { id: kayit.id, at: Date.now() });
    res.json({ ok: true, id: kayit.id });
  });
  app.get('/api/admin/gizlilik', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    const rows = oku<Any[]>(GIZ, []);
    res.setHeader('Cache-Control', 'no-store');
    res.json(diziSayfala(rows, s, {
      araMetni: (x) => `${x.id} ${x.email} ${x.uid} ${x.not}`,
      siralayicilar: { at: (x) => x.at, durum: (x) => x.durum },
      suzgecler: { tur: (x, v) => x.tur === v, durum: (x, v) => x.durum === v },
      yuzler: { tur: (x) => x.tur, durum: (x) => x.durum },
    }));
  });
  app.put('/api/admin/gizlilik/:id', A, async (req, res) => {
    const id = String(req.params.id);
    const durum = String(req.body?.durum || '');
    if (!DURUMLAR.has(durum)) return res.status(400).json({ error: 'Durum geçersiz.' });
    let once: Any = {}, sonra: Any = {};
    try {
      await atomikJsonGuncelle<Any[]>(GIZ, (eski) => {
        const l = Array.isArray(eski) ? eski : [];
        const x = l.find((t) => t.id === id);
        if (!x) throw new Error('Talep bulunamadı');
        once = { durum: x.durum, yanit: x.yanit };
        x.durum = durum;
        if ('yanit' in (req.body || {})) x.yanit = kirp(req.body.yanit, 1000);
        x.guncellendi = new Date().toISOString();
        sonra = { durum: x.durum, yanit: x.yanit };
        return l;
      });
    } catch (e: any) { return res.status(404).json({ error: e?.message || 'Talep bulunamadı' }); }
    denetimHedef(res, `gizlilik:${id}`);
    denetimFark(res, once, sonra);
    d.broadcastAdmin('gizlilik_changed', { id, at: Date.now() });
    res.json({ ok: true });
  });

  /* ================= Quiz havuzu (salt okunur) ================= */
  const YAYIN = path.resolve(d.rootDir, '..', 'meds_database_v2', 'ders_isci', 'yayinlanan');
  let quizOnbellek: { at: number; rows: Any[]; dosyalar: Map<string, string> } | null = null;
  const quizSatirlari = () => {
    if (quizOnbellek && Date.now() - quizOnbellek.at < 60_000) return quizOnbellek;
    const rows: Any[] = [];
    const dosyalar = new Map<string, string>();
    let klasorler: string[] = [];
    try { klasorler = fs.readdirSync(YAYIN); } catch { klasorler = []; }
    for (const k of klasorler) {
      const f = path.join(YAYIN, k, 'quiz_havuzu.json');
      if (!fs.existsSync(f)) continue;
      const h = oku<Any>(f, null as any);
      for (const q of h?.questions || []) {
        const id = String(q.id || '');
        if (!id) continue;
        dosyalar.set(id, f);
        rows.push({
          id, ders: String(q.topic_id || h.topic_id || k), kurul: kurulNo(q.board_id || h.board_id), yon: q.direction || '', tur: q.archetype || '',
          soru: kirp(q.prompt, 220), cevap: q.correct_option || q.correct_answer || '', cift: q.question_pair_id || '', klasor: k,
        });
      }
    }
    quizOnbellek = { at: Date.now(), rows, dosyalar };
    return quizOnbellek;
  };
  app.get('/api/admin/quiz/havuz', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    res.json(diziSayfala(quizSatirlari().rows, s, {
      araMetni: (x) => `${x.id} ${x.soru} ${x.ders}`,
      siralayicilar: { id: (x) => x.id, ders: (x) => x.ders },
      suzgecler: { ders: (x, v) => x.ders === v, yon: (x, v) => x.yon === v, tur: (x, v) => x.tur === v, kurul: (x, v) => x.kurul === v },
      yuzler: { ders: (x) => x.ders, yon: (x) => x.yon, tur: (x) => x.tur },
    }));
  });
  app.get('/api/admin/quiz/havuz/:id', A, (req, res) => {
    const f = quizSatirlari().dosyalar.get(String(req.params.id));
    const q = f ? (oku<Any>(f, {}).questions || []).find((x: Any) => x.id === req.params.id) : null;
    if (!q) return res.status(404).json({ error: 'Soru bulunamadı' });
    res.json(q);
  });

  /* ================= Sesli ders üretim kuyruğu (görünüm) ================= */
  const KUYRUK = path.join(d.dataDir, 'sesli_anlatim', 'kuyruk.json');
  app.get('/api/admin/sesli-kuyruk', A, (req, res) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50 });
    const rows = oku<Any[]>(KUYRUK, []).map((x, sira) => ({
      id: x.id, sira, key: x.key, saglayici: x.saglayici, ses: x.ses, durum: x.durum, isci: x.isci || '',
      ilerleme: x.ilerleme ? `${x.ilerleme.bitti}/${x.ilerleme.toplam}` : '', yuzde: x.ilerleme?.toplam ? Math.round((100 * x.ilerleme.bitti) / x.ilerleme.toplam) : 0,
      olusturuldu: x.olusturuldu || '', bitti: x.bitti || '', hata: kirp(x.hata, 200), isteyen: x.isteyen || '',
    }));
    res.setHeader('Cache-Control', 'no-store');
    res.json(diziSayfala(rows, s, {
      araMetni: (x) => `${x.id} ${x.key} ${x.isci}`,
      siralayicilar: { olusturuldu: (x) => x.olusturuldu, sira: (x) => x.sira, durum: (x) => x.durum },
      suzgecler: { durum: (x, v) => x.durum === v, saglayici: (x, v) => x.saglayici === v },
      yuzler: { durum: (x) => x.durum, saglayici: (x) => x.saglayici },
    }));
  });
  app.get('/api/admin/sesli-kuyruk/:id', A, (req, res) => {
    const x = oku<Any[]>(KUYRUK, []).find((t) => t.id === req.params.id);
    if (!x) return res.status(404).json({ error: 'İş bulunamadı' });
    res.json(x);
  });
}
