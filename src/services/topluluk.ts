/**
 * Topluluk (v15 › L "Topluluk: sohbet, yorumlar"). Sunucu tarafı.
 * Kanallar: `genel`, `kurul-N` (1–6), `ders:<anahtar>` (ders yorumları). Mesajlar meds-pg `topluluk_mesajlar`
 * (deploy/pg/sql/topluluk.sql, açılışta uygulanır). Yazma yalnız doğrulanmış Firebase kullanıcısıyla (req.verifiedUser;
 * istemcinin yolladığı uid/e-posta kimlik sayılmaz). Dışarı yalnız görünen ad + kısa yazar özeti çıkar; uid/e-posta çıkmaz.
 * Kendi mesajını sahibi, her mesajı yönetici siler; 3 farklı kişinin şikâyeti mesajı gizler. Hız sınırı: 5 sn'de 1,
 * saatte 60 mesaj. Değişiklik SSE `topluluk` olayıyla yayılır. LLM yok.
 */
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import type express from 'express';
import { pgDb } from './pgDb';
import { verifiedUid } from './adminAuth';

interface Deps {
  rootDir: string;
  isPgOnline: () => boolean;
  isAdmin: (req: express.Request) => boolean;
  broadcast: (event: string, data: any) => void;
}

const KANAL = /^(genel|kurul-[1-6]|ders:[a-z0-9][a-z0-9-]{2,90})$/;
const SIKAYET_GIZLE = 3;
const ozet = (uid: string) => crypto.createHash('sha256').update(`topluluk:${uid}`).digest('hex').slice(0, 10);
const temizle = (s: unknown, n: number) => String(s ?? '').replace(/[\u0000-\u0008\u000b-\u001f\u007f‪-‮⁦-⁩]/g, '').replace(/\n{3,}/g, '\n\n').trim().slice(0, n);
const sonYazma = new Map<string, number[]>();

export function registerTopluluk(app: express.Express, d: Deps) {
  let sema = false;
  const semaKur = async () => {
    if (sema || !d.isPgOnline()) return sema;
    try { await pgDb.query(fs.readFileSync(path.join(d.rootDir, 'deploy', 'pg', 'sql', 'topluluk.sql'), 'utf8')); sema = true; }
    catch (e: any) { console.warn('[Topluluk] şema:', e?.message); }
    return sema;
  };
  void semaKur();

  const disa = (r: any, uid: string, admin: boolean) => ({
    id: Number(r.id), kanal: r.kanal, ad: r.ad, metin: r.metin, yanitId: r.yanit_id ? Number(r.yanit_id) : null,
    at: new Date(r.olusturma).getTime(), yazar: ozet(r.uid), benim: !!uid && r.uid === uid,
    sikayet: admin ? (r.sikayet_uid || []).length : undefined,
  });

  app.get('/api/topluluk/kanallar', async (_req, res) => {
    if (!(await semaKur())) return res.status(503).json({ error: 'Topluluk şu an kullanılamıyor.' });
    const { rows } = await pgDb.query(
      `select kanal, count(*)::int n, max(olusturma) son from topluluk_mesajlar
       where not silindi and cardinality(sikayet_uid) < $1 and olusturma > now() - interval '30 days' group by kanal`, [SIKAYET_GIZLE]);
    res.json({ kanallar: rows.map((r: any) => ({ kanal: r.kanal, n: r.n, son: new Date(r.son).getTime() })) });
  });

  app.get('/api/topluluk/mesajlar', async (req, res) => {
    const kanal = String(req.query.kanal || '');
    if (!KANAL.test(kanal)) return res.status(400).json({ error: 'Geçersiz kanal.' });
    if (!(await semaKur())) return res.status(503).json({ error: 'Topluluk şu an kullanılamıyor.' });
    const once = Number(req.query.once) || 0;
    const admin = d.isAdmin(req);
    const { rows } = await pgDb.query(
      `select * from topluluk_mesajlar where kanal = $1 and not silindi ${admin ? '' : 'and cardinality(sikayet_uid) < $3'}
       ${once ? 'and id < $2' : 'and $2::bigint = 0'} order by id desc limit 60`,
      admin ? [kanal, once] : [kanal, once, SIKAYET_GIZLE]);
    const uid = verifiedUid(req);
    res.json({ mesajlar: rows.reverse().map((r: any) => disa(r, uid, admin)), dahaVar: rows.length === 60, girisli: !!uid });
  });

  app.post('/api/topluluk/mesaj', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.status(401).json({ error: 'Yazmak için giriş yapmalısın.' });
    const kanal = String(req.body?.kanal || '');
    const metin = temizle(req.body?.metin, 800);
    const ad = temizle(req.body?.ad, 40) || 'Öğrenci';
    if (!KANAL.test(kanal)) return res.status(400).json({ error: 'Geçersiz kanal.' });
    if (!metin) return res.status(400).json({ error: 'Mesaj boş olamaz.' });
    if (!(await semaKur())) return res.status(503).json({ error: 'Topluluk şu an kullanılamıyor.' });
    const simdi = Date.now();
    const gecmis = (sonYazma.get(uid) || []).filter((t) => simdi - t < 3_600_000);
    if (gecmis.length && simdi - gecmis[gecmis.length - 1] < 5000) return res.status(429).json({ error: 'Biraz yavaş: 5 saniyede bir mesaj.' });
    if (gecmis.length >= 60) return res.status(429).json({ error: 'Saatlik mesaj sınırına ulaştın.' });
    const yanit = Number(req.body?.yanitId) || null;
    const { rows } = await pgDb.query(
      `insert into topluluk_mesajlar (kanal, uid, ad, metin, yanit_id) values ($1,$2,$3,$4,$5) returning *`, [kanal, uid, ad, metin, yanit]);
    sonYazma.set(uid, [...gecmis, simdi]);
    d.broadcast('topluluk', { kanal, id: Number(rows[0].id), tur: 'yeni' });
    res.json({ mesaj: disa(rows[0], uid, false) });
  });

  app.post('/api/topluluk/mesaj/:id/sil', async (req, res) => {
    const uid = verifiedUid(req);
    const admin = d.isAdmin(req);
    if (!uid && !admin) return res.status(401).json({ error: 'Giriş gerekli.' });
    const { rows } = await pgDb.query(
      `update topluluk_mesajlar set silindi = true, silen = $2 where id = $1 and not silindi and ($3 or uid = $4) returning kanal`,
      [Number(req.params.id), admin ? 'yonetici' : 'sahibi', admin, uid]);
    if (!rows.length) return res.status(404).json({ error: 'Mesaj bulunamadı ya da senin değil.' });
    d.broadcast('topluluk', { kanal: rows[0].kanal, id: Number(req.params.id), tur: 'sil' });
    res.json({ ok: true });
  });

  app.post('/api/topluluk/mesaj/:id/sikayet', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.status(401).json({ error: 'Şikâyet için giriş yapmalısın.' });
    const { rows } = await pgDb.query(
      `update topluluk_mesajlar set sikayet_uid = array_append(sikayet_uid, $2)
       where id = $1 and not silindi and uid <> $2 and not ($2 = any(sikayet_uid)) returning kanal, cardinality(sikayet_uid) n`,
      [Number(req.params.id), uid]);
    if (rows[0] && rows[0].n >= SIKAYET_GIZLE) d.broadcast('topluluk', { kanal: rows[0].kanal, id: Number(req.params.id), tur: 'sil' });
    res.json({ ok: true });
  });
}
