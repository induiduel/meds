/**
 * Topluluk (v15 › L01 Sohbet listesi, L03 Yorumlar). Sunucu tarafı; services/topluluk.ts'i genişletir.
 * - Sohbet odaları (grup / birebir): sohbet_odalari + sohbet_uyeleri; mesajlar topluluk_mesajlar'a `oda:<id>` kanalıyla
 *   yazılır (tek mesaj tablosu). Oda içeriği yalnız üyelere açılır. Grup davet kodla (`/topluluk?katil=<kod>`), birebir
 *   sohbet bir kanal mesajının yazar özetinden açılır (uid/e-posta dışarı çıkmaz).
 * - Yorumlar: topluluk_mesajlar `ders:` / `soru:` kanalı; beğeni yorum_begeni (kişi başına bir, aç/kapa).
 *   "En faydalı" = beğeni sayısı. Yorum yazma mevcut POST /api/topluluk/mesaj ucuyla.
 * Yazma yalnız doğrulanmış Firebase kullanıcısıyla (verifiedUid). Hız sınırı: 3 sn'de 1, saatte 120 eylem.
 * SSE: `topluluk_sohbet` {oda} (içerik yok; istemci yetkiyle yeniden çeker), `topluluk` {kanal, tur:'begeni'}. LLM yok.
 */
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';
import type express from 'express';
import { pgDb } from './pgDb';
import { verifiedUid } from './adminAuth';
import { KANAL, ozet, temizle } from './topluluk';

interface Deps {
  rootDir: string;
  isPgOnline: () => boolean;
  broadcast: (event: string, data: any) => void;
}

const MESAJ_MAX = 800;
const ODA_UYE_MAX = 60;
const OZET_SQL = `left(encode(sha256(convert_to('topluluk:' || uid, 'UTF8')), 'hex'), 10)`;
const eylem = new Map<string, number[]>();
function hizli(uid: string, araMs = 3000, saatlik = 120): string {
  const simdi = Date.now();
  const g = (eylem.get(uid) || []).filter((t) => simdi - t < 3_600_000);
  if (g.length && simdi - g[g.length - 1] < araMs) return 'Biraz yavaş: birkaç saniye bekle.';
  if (g.length >= saatlik) return 'Saatlik sınıra ulaştın.';
  g.push(simdi); eylem.set(uid, g);
  if (eylem.size > 20000) eylem.clear();
  return '';
}

export function registerToplulukSohbet(app: express.Express, d: Deps) {
  let sema = false;
  const semaKur = async () => {
    if (sema || !d.isPgOnline()) return sema;
    try {
      await pgDb.query(fs.readFileSync(path.join(d.rootDir, 'deploy', 'pg', 'sql', 'topluluk.sql'), 'utf8'));
      await pgDb.query(fs.readFileSync(path.join(d.rootDir, 'deploy', 'pg', 'sql', 'topluluk_sohbet.sql'), 'utf8'));
      sema = true;
    } catch (e: any) { console.warn('[ToplulukSohbet] şema:', e?.message); }
    return sema;
  };
  void semaKur();
  const hazir = async (res: express.Response) => {
    if (await semaKur()) return true;
    res.status(503).json({ error: 'Topluluk şu an kullanılamıyor.' });
    return false;
  };
  const uye = async (oda: number, uid: string) =>
    (await pgDb.query(`select 1 from sohbet_uyeleri where oda_id = $1 and uid = $2`, [oda, uid])).rows.length > 0;
  const msj = (r: any, uid: string) => ({
    id: Number(r.id), kanal: r.kanal, ad: r.ad, metin: r.metin, yanitId: r.yanit_id ? Number(r.yanit_id) : null,
    at: new Date(r.olusturma).getTime(), yazar: ozet(r.uid), benim: r.uid === uid,
  });

  // L01 · sohbet listesi: üyesi olduğun odalar, son mesaj önizlemesi, okunmamış sayısı
  app.get('/api/topluluk/sohbetler', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.json({ sohbetler: [], girisli: false });
    if (!(await hazir(res))) return;
    const { rows } = await pgDb.query(
      `select o.id, o.tur, o.ad, o.kod, o.son, u.okundu_id,
         (select string_agg(x.ad, ', ' order by x.katilma) from sohbet_uyeleri x where x.oda_id = o.id and x.uid <> $1) diger,
         (select count(*)::int from sohbet_uyeleri x where x.oda_id = o.id) uye_n,
         m.ad son_ad, m.metin son_metin, m.uid son_uid, m.olusturma son_at,
         (select count(*)::int from topluluk_mesajlar y where y.kanal = 'oda:' || o.id and not y.silindi and y.id > u.okundu_id and y.uid <> $1) okunmamis
       from sohbet_uyeleri u join sohbet_odalari o on o.id = u.oda_id
       left join lateral (select ad, metin, uid, olusturma from topluluk_mesajlar where kanal = 'oda:' || o.id and not silindi order by id desc limit 1) m on true
       where u.uid = $1 order by coalesce(m.olusturma, o.son) desc limit 100`, [uid]);
    res.json({
      girisli: true,
      sohbetler: rows.map((r: any) => ({
        id: Number(r.id), tur: r.tur, ad: r.tur === 'grup' ? r.ad : (r.diger || 'Birebir sohbet'), kod: r.tur === 'grup' ? r.kod : undefined,
        uyeN: r.uye_n, okunmamis: r.okunmamis,
        son: r.son_metin ? { ad: r.son_uid === uid ? 'Sen' : r.son_ad, metin: String(r.son_metin).slice(0, 120), at: new Date(r.son_at).getTime() } : null,
        at: new Date(r.son_at || r.son).getTime(),
      })),
    });
  });

  // Yeni sohbet: {tur:'grup', ad, benAd} ya da {tur:'dm', yazar, benAd} (yazar = kanal mesajındaki yazar özeti)
  app.post('/api/topluluk/sohbet', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.status(401).json({ error: 'Sohbet için giriş yapmalısın.' });
    if (!(await hazir(res))) return;
    const benAd = temizle(req.body?.benAd, 40) || 'Öğrenci';
    const h = hizli(uid); if (h) return res.status(429).json({ error: h });
    if (req.body?.tur === 'grup') {
      const ad = temizle(req.body?.ad, 60);
      if (!ad) return res.status(400).json({ error: 'Grup adı gerekli.' });
      const kod = crypto.randomBytes(6).toString('base64url');
      const { rows } = await pgDb.query(`insert into sohbet_odalari (tur, ad, kod, olusturan) values ('grup', $1, $2, $3) returning id`, [ad, kod, uid]);
      await pgDb.query(`insert into sohbet_uyeleri (oda_id, uid, ad) values ($1, $2, $3)`, [rows[0].id, uid, benAd]);
      return res.json({ id: Number(rows[0].id), kod });
    }
    if (req.body?.tur === 'dm') {
      const yazar = String(req.body?.yazar || '');
      if (!/^[0-9a-f]{10}$/.test(yazar)) return res.status(400).json({ error: 'Geçersiz kişi.' });
      const k = await pgDb.query(
        `select uid, ad from topluluk_mesajlar where ${OZET_SQL} = $1 and not silindi and kanal not like 'oda:%' order by id desc limit 1`, [yazar]);
      const hedef = k.rows[0];
      if (!hedef) return res.status(404).json({ error: 'Kişi bulunamadı.' });
      if (hedef.uid === uid) return res.status(400).json({ error: 'Kendinle sohbet açamazsın.' });
      const anahtar = [uid, hedef.uid].sort().join('|');
      const var0 = await pgDb.query(`select id from sohbet_odalari where dm_anahtar = $1`, [anahtar]);
      if (var0.rows[0]) return res.json({ id: Number(var0.rows[0].id) });
      const { rows } = await pgDb.query(
        `insert into sohbet_odalari (tur, olusturan, dm_anahtar) values ('dm', $1, $2) on conflict (dm_anahtar) do update set son = sohbet_odalari.son returning id`, [uid, anahtar]);
      const id = Number(rows[0].id);
      await pgDb.query(`insert into sohbet_uyeleri (oda_id, uid, ad) values ($1, $2, $3), ($1, $4, $5) on conflict do nothing`, [id, uid, benAd, hedef.uid, hedef.ad]);
      d.broadcast('topluluk_sohbet', { oda: id });
      return res.json({ id });
    }
    res.status(400).json({ error: 'Geçersiz sohbet türü.' });
  });

  app.post('/api/topluluk/sohbet/katil', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.status(401).json({ error: 'Katılmak için giriş yapmalısın.' });
    if (!(await hazir(res))) return;
    const kod = String(req.body?.kod || '');
    if (!/^[A-Za-z0-9_-]{6,16}$/.test(kod)) return res.status(400).json({ error: 'Geçersiz davet.' });
    const o = (await pgDb.query(`select id from sohbet_odalari where kod = $1 and tur = 'grup'`, [kod])).rows[0];
    if (!o) return res.status(404).json({ error: 'Davet bulunamadı.' });
    const n = (await pgDb.query(`select count(*)::int n from sohbet_uyeleri where oda_id = $1`, [o.id])).rows[0].n;
    if (n >= ODA_UYE_MAX && !(await uye(Number(o.id), uid))) return res.status(409).json({ error: 'Grup dolu.' });
    await pgDb.query(`insert into sohbet_uyeleri (oda_id, uid, ad) values ($1, $2, $3) on conflict do nothing`, [o.id, uid, temizle(req.body?.benAd, 40) || 'Öğrenci']);
    d.broadcast('topluluk_sohbet', { oda: Number(o.id) });
    res.json({ id: Number(o.id) });
  });

  app.post('/api/topluluk/sohbet/:id/ayril', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.status(401).json({ error: 'Giriş gerekli.' });
    if (!(await hazir(res))) return;
    await pgDb.query(`delete from sohbet_uyeleri where oda_id = $1 and uid = $2`, [Number(req.params.id), uid]);
    d.broadcast('topluluk_sohbet', { oda: Number(req.params.id) });
    res.json({ ok: true });
  });

  app.get('/api/topluluk/sohbet/:id', async (req, res) => {
    const uid = verifiedUid(req);
    const oda = Number(req.params.id);
    if (!uid) return res.status(401).json({ error: 'Giriş gerekli.' });
    if (!(await hazir(res))) return;
    if (!(await uye(oda, uid))) return res.status(404).json({ error: 'Sohbet bulunamadı.' });
    const o = (await pgDb.query(`select tur, ad, kod from sohbet_odalari where id = $1`, [oda])).rows[0];
    const uyeler = (await pgDb.query(`select ad, uid from sohbet_uyeleri where oda_id = $1 order by katilma`, [oda])).rows;
    const once = Number(req.query.once) || 0;
    const { rows } = await pgDb.query(
      `select * from topluluk_mesajlar where kanal = $1 and not silindi ${once ? 'and id < $2' : 'and $2::bigint = 0'} order by id desc limit 60`, [`oda:${oda}`, once]);
    res.json({
      oda: { id: oda, tur: o.tur, ad: o.tur === 'grup' ? o.ad : uyeler.filter((u: any) => u.uid !== uid).map((u: any) => u.ad).join(', ') || 'Birebir sohbet', kod: o.tur === 'grup' ? o.kod : undefined, uyeler: uyeler.map((u: any) => (u.uid === uid ? 'Sen' : u.ad)) },
      mesajlar: rows.reverse().map((r: any) => msj(r, uid)), dahaVar: rows.length === 60,
    });
  });

  app.post('/api/topluluk/sohbet/:id/mesaj', async (req, res) => {
    const uid = verifiedUid(req);
    const oda = Number(req.params.id);
    if (!uid) return res.status(401).json({ error: 'Yazmak için giriş yapmalısın.' });
    if (!(await hazir(res))) return;
    const metin = temizle(req.body?.metin, MESAJ_MAX);
    if (!metin) return res.status(400).json({ error: 'Mesaj boş olamaz.' });
    const u = (await pgDb.query(`select ad from sohbet_uyeleri where oda_id = $1 and uid = $2`, [oda, uid])).rows[0];
    if (!u) return res.status(404).json({ error: 'Sohbet bulunamadı.' });
    const h = hizli(uid, 1500, 300); if (h) return res.status(429).json({ error: h });
    const { rows } = await pgDb.query(
      `insert into topluluk_mesajlar (kanal, uid, ad, metin, yanit_id) values ($1, $2, $3, $4, $5) returning *`,
      [`oda:${oda}`, uid, u.ad, metin, Number(req.body?.yanitId) || null]);
    await pgDb.query(`update sohbet_odalari set son = now() where id = $1`, [oda]);
    await pgDb.query(`update sohbet_uyeleri set okundu_id = $3 where oda_id = $1 and uid = $2`, [oda, uid, rows[0].id]);
    d.broadcast('topluluk_sohbet', { oda });
    res.json({ mesaj: msj(rows[0], uid) });
  });

  app.post('/api/topluluk/sohbet/:id/okundu', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.status(401).json({ error: 'Giriş gerekli.' });
    if (!(await hazir(res))) return;
    await pgDb.query(
      `update sohbet_uyeleri set okundu_id = greatest(okundu_id, coalesce((select max(id) from topluluk_mesajlar where kanal = 'oda:' || $1), 0))
       where oda_id = $1 and uid = $2`, [Number(req.params.id), uid]);
    res.json({ ok: true });
  });

  // L03 · yorumlar: üst düzey yorumlar + yanıtları, beğeni sayısı; sira=faydali (beğeni) | yeni
  app.get('/api/topluluk/yorumlar', async (req, res) => {
    const kanal = String(req.query.kanal || '');
    if (!KANAL.test(kanal) || !/^(ders|soru):/.test(kanal)) return res.status(400).json({ error: 'Geçersiz yorum kanalı.' });
    if (!(await hazir(res))) return;
    const uid = verifiedUid(req);
    const sira = req.query.sira === 'yeni' ? 'm.id desc' : 'begeni desc, m.id desc';
    const { rows } = await pgDb.query(
      `select m.*, (select count(*)::int from yorum_begeni b where b.mesaj_id = m.id) begeni,
         exists(select 1 from yorum_begeni b where b.mesaj_id = m.id and b.uid = $2) ben
       from topluluk_mesajlar m where m.kanal = $1 and not m.silindi and cardinality(m.sikayet_uid) < 3
       order by ${sira} limit 300`, [kanal, uid]);
    const hepsi = rows.map((r: any) => ({ ...msj(r, uid), begeni: r.begeni, begendim: !!r.ben }));
    const ids = new Set(hepsi.map((x) => x.id));
    const ust = hepsi.filter((x) => !x.yanitId || !ids.has(x.yanitId));
    const yanitlar = hepsi.filter((x) => x.yanitId && ids.has(x.yanitId)).sort((a, b) => a.id - b.id);
    res.json({ girisli: !!uid, toplam: hepsi.length, yorumlar: ust.map((y) => ({ ...y, yanitlar: yanitlar.filter((x) => x.yanitId === y.id) })) });
  });

  app.post('/api/topluluk/mesaj/:id/begen', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.status(401).json({ error: 'Beğenmek için giriş yapmalısın.' });
    if (!(await hazir(res))) return;
    const id = Number(req.params.id);
    const m = (await pgDb.query(`select kanal from topluluk_mesajlar where id = $1 and not silindi`, [id])).rows[0];
    if (!m || !/^(ders|soru):/.test(m.kanal)) return res.status(404).json({ error: 'Yorum bulunamadı.' });
    const h = hizli(`b:${uid}`, 300, 600); if (h) return res.status(429).json({ error: h });
    const sil = await pgDb.query(`delete from yorum_begeni where mesaj_id = $1 and uid = $2`, [id, uid]);
    if (!sil.rowCount) await pgDb.query(`insert into yorum_begeni (mesaj_id, uid) values ($1, $2) on conflict do nothing`, [id, uid]);
    const n = (await pgDb.query(`select count(*)::int n from yorum_begeni where mesaj_id = $1`, [id])).rows[0].n;
    d.broadcast('topluluk', { kanal: m.kanal, id, tur: 'begeni' });
    res.json({ begendim: !sil.rowCount, begeni: n });
  });
}
