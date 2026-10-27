/**
 * Not paylaşımı (v15 › K05 Notu paylaş, K06 Benimle paylaşılanlar). Sunucu tarafı; LLM yok.
 * Not cihazda tutulur (NotlarimV15, userKvSync); paylaşınca o anki kopyası paylasilan_notlar'a yazılır.
 * Hedef bir sohbet odasıdır (services/toplulukSohbet.ts): grup = topluluk, birebir = kişi. Yalnız üyesi olduğun odaya
 * paylaşabilir, yalnız üyesi olduğun odaların notlarını görebilirsin. Odaya kısa bir "not paylaştı" mesajı da düşer.
 *   POST   /api/not-paylas             { odaId, baslik, metin, renk, benAd } → { id }
 *   GET    /api/not-paylas/benimle     → üyesi olduğum odalarda başkalarının paylaştığı notlar
 *   GET    /api/not-paylas/benim       → benim paylaştıklarım
 *   GET    /api/not-paylas/:id         → tek not (oda üyesine)
 *   POST   /api/not-paylas/:id/kaldir  → paylaşımı geri al (yalnız sahibi)
 * Yazma yalnız doğrulanmış Firebase kullanıcısıyla; hız sınırı: 5 sn'de 1, saatte 60 paylaşım (+ server.ts öğrenci yazma sınırı).
 * SSE: `not_paylas` {oda} (içerik yok; istemci yetkiyle yeniden çeker) + `topluluk_sohbet` {oda}.
 */
import fs from 'fs';
import path from 'path';
import type express from 'express';
import { pgDb } from './pgDb';
import { verifiedUid } from './adminAuth';
import { ozet, temizle } from './topluluk';

interface Deps { rootDir: string; isPgOnline: () => boolean; broadcast: (event: string, data: any) => void }

const BASLIK_MAX = 120;
const METIN_MAX = 20000;
const RENK = /^(none|red|amber|green|blue|violet)$/;
const eylem = new Map<string, number[]>();
function hizli(uid: string): string {
  const simdi = Date.now();
  const g = (eylem.get(uid) || []).filter((t) => simdi - t < 3_600_000);
  if (g.length && simdi - g[g.length - 1] < 5000) return 'Biraz yavaş: birkaç saniye bekle.';
  if (g.length >= 60) return 'Saatlik paylaşım sınırına ulaştın.';
  g.push(simdi); eylem.set(uid, g);
  if (eylem.size > 20000) eylem.clear();
  return '';
}

export function registerNotPaylas(app: express.Express, d: Deps) {
  let sema = false;
  const semaKur = async () => {
    if (sema || !d.isPgOnline()) return sema;
    try {
      for (const f of ['topluluk.sql', 'topluluk_sohbet.sql', 'not_paylas.sql']) {
        await pgDb.query(fs.readFileSync(path.join(d.rootDir, 'deploy', 'pg', 'sql', f), 'utf8'));
      }
      sema = true;
    } catch (e: any) { console.warn('[NotPaylas] şema:', e?.message); }
    return sema;
  };
  void semaKur();
  const hazir = async (res: express.Response) => {
    if (await semaKur()) return true;
    res.status(503).json({ error: 'Paylaşım şu an kullanılamıyor.' });
    return false;
  };
  const SEC = `select n.id, n.oda_id, n.sahip, n.sahip_ad, n.baslik, n.metin, n.renk, n.olusturma, o.tur oda_tur, o.ad oda_ad
    from paylasilan_notlar n join sohbet_odalari o on o.id = n.oda_id`;
  const bicim = (r: any, uid: string, tam = false) => ({
    id: Number(r.id), odaId: Number(r.oda_id), odaTur: r.oda_tur, odaAd: r.oda_tur === 'grup' ? r.oda_ad : 'Birebir',
    sahipAd: r.sahip === uid ? 'Sen' : r.sahip_ad, yazar: ozet(r.sahip), benim: r.sahip === uid,
    baslik: r.baslik, renk: r.renk, at: new Date(r.olusturma).getTime(),
    metin: tam ? r.metin : String(r.metin).slice(0, 240), uzunluk: String(r.metin).length,
  });

  app.post('/api/not-paylas', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.status(401).json({ error: 'Paylaşmak için giriş yapmalısın.' });
    if (!(await hazir(res))) return;
    const oda = Number(req.body?.odaId);
    const baslik = temizle(req.body?.baslik, BASLIK_MAX);
    const metin = String(req.body?.metin ?? '').replace(/[\u0000-\u0008\u000b-\u001f\u007f]/g, '').slice(0, METIN_MAX).trim();
    const renk = RENK.test(String(req.body?.renk)) ? String(req.body.renk) : 'none';
    if (!oda) return res.status(400).json({ error: 'Paylaşılacak sohbeti seç.' });
    if (!baslik && !metin) return res.status(400).json({ error: 'Boş not paylaşılamaz.' });
    const u = (await pgDb.query(`select ad from sohbet_uyeleri where oda_id = $1 and uid = $2`, [oda, uid])).rows[0];
    if (!u) return res.status(404).json({ error: 'Sohbet bulunamadı.' });
    const h = hizli(uid); if (h) return res.status(429).json({ error: h });
    const ad = temizle(req.body?.benAd, 40) || u.ad;
    const { rows } = await pgDb.query(
      `insert into paylasilan_notlar (oda_id, sahip, sahip_ad, baslik, metin, renk) values ($1, $2, $3, $4, $5, $6) returning id`,
      [oda, uid, ad, baslik, metin, renk]);
    const id = Number(rows[0].id);
    const m = await pgDb.query(`insert into topluluk_mesajlar (kanal, uid, ad, metin) values ($1, $2, $3, $4) returning id`,
      [`oda:${oda}`, uid, u.ad, `Not paylaştı: ${baslik || 'Başlıksız not'} — Notlarım › Benimle paylaşılanlar`]);
    await pgDb.query(`update sohbet_odalari set son = now() where id = $1`, [oda]);
    await pgDb.query(`update sohbet_uyeleri set okundu_id = $3 where oda_id = $1 and uid = $2`, [oda, uid, m.rows[0].id]);
    d.broadcast('not_paylas', { oda });
    d.broadcast('topluluk_sohbet', { oda });
    res.json({ id });
  });

  app.get('/api/not-paylas/benimle', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.json({ notlar: [], girisli: false });
    if (!(await hazir(res))) return;
    const { rows } = await pgDb.query(
      `${SEC} join sohbet_uyeleri u on u.oda_id = n.oda_id and u.uid = $1 where not n.silindi and n.sahip <> $1 order by n.id desc limit 200`, [uid]);
    res.json({ girisli: true, notlar: rows.map((r: any) => bicim(r, uid)) });
  });

  app.get('/api/not-paylas/benim', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.json({ notlar: [], girisli: false });
    if (!(await hazir(res))) return;
    const { rows } = await pgDb.query(`${SEC} where not n.silindi and n.sahip = $1 order by n.id desc limit 200`, [uid]);
    res.json({ girisli: true, notlar: rows.map((r: any) => bicim(r, uid)) });
  });

  app.get('/api/not-paylas/:id', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.status(401).json({ error: 'Giriş gerekli.' });
    if (!(await hazir(res))) return;
    const { rows } = await pgDb.query(
      `${SEC} where n.id = $2 and not n.silindi and (n.sahip = $1 or exists (select 1 from sohbet_uyeleri u where u.oda_id = n.oda_id and u.uid = $1))`,
      [uid, Number(req.params.id) || 0]);
    if (!rows[0]) return res.status(404).json({ error: 'Not bulunamadı.' });
    res.json({ not: bicim(rows[0], uid, true) });
  });

  app.post('/api/not-paylas/:id/kaldir', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.status(401).json({ error: 'Giriş gerekli.' });
    if (!(await hazir(res))) return;
    const { rows } = await pgDb.query(
      `update paylasilan_notlar set silindi = true where id = $1 and sahip = $2 and not silindi returning oda_id`, [Number(req.params.id) || 0, uid]);
    if (!rows[0]) return res.status(404).json({ error: 'Not bulunamadı.' });
    d.broadcast('not_paylas', { oda: Number(rows[0].oda_id) });
    res.json({ ok: true });
  });
}
