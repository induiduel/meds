/**
 * Yönetim v16 › Topluluk (server-only): mesaj şikâyetleri, sohbet odaları, mesaj arama/gizleme, arkadaşlık, paylaşılan notlar, kanallar.
 * Tablolar: topluluk_mesajlar (kanal `oda:<id>` = sohbet odası), sohbet_odalari/sohbet_uyeleri, arkadas_istek, paylasilan_notlar.
 * Mesaj/oda/arkadaşlık/not okuması kişisel veridir: denetim.ts KISISEL_OKUMA desenleri bu uçları kapsar (her okuma kayda düşer).
 * Silme: "gizle" yumuşaktır (silindi=true, geri alınabilir); kalıcı silme gövdede onay sözcüğü ister ("SIL").
 */
import crypto from 'crypto';
import type express from 'express';
import { pgDb } from '../pgDb';
import { denetimFark, denetimHedef, denetimNot } from './denetim.ts';
import { listeSorgusu } from './sayfalama.ts';
import { gelenOnbellekSil } from './sistemEk.ts';

type Deps = {
  requireAdmin: express.RequestHandler;
  isPgOnline: () => boolean;
  /** Öğrenci istemcilerine (topluluk, topluluk_sohbet, not_paylas) */
  broadcast: (ev: string, d: any) => void;
  /** Yalnız yönetici (topluluk_changed) */
  broadcastAdmin: (ev: string, d: any) => void;
  kimOf: (req: express.Request) => string;
};

const sayi = (v: unknown) => { const n = Number(v); return Number.isFinite(n) && n > 0 ? Math.floor(n) : 0; };

export function registerYonetimTopluluk(app: express.Express, d: Deps) {
  // Oda kapatma sütunları (topluluk_sohbet.sql ile aynı, idempotent): sohbet şeması henüz uygulanmadıysa da çalışsın
  let sema = false;
  const hazir = async (res: express.Response) => {
    if (!d.isPgOnline()) { res.status(503).json({ error: 'meds-pg çevrimdışı.' }); return false; }
    if (!sema) {
      try { await pgDb.query(`alter table sohbet_odalari add column if not exists kapali timestamptz; alter table sohbet_odalari add column if not exists kapatan text;`); sema = true; }
      catch (e: any) { res.status(503).json({ error: `Topluluk şeması hazır değil: ${e?.message}` }); return false; }
    }
    res.setHeader('Cache-Control', 'no-store');
    return true;
  };
  const fail = (res: express.Response, e: any) => res.status(e?.status || 500).json({ error: e?.message || String(e) });
  const haber = (kanal: string, id?: number) => {
    const oda = /^oda:(\d+)$/.exec(kanal)?.[1];
    if (oda) d.broadcast('topluluk_sohbet', { oda: Number(oda) });
    else d.broadcast('topluluk', { kanal, id, tur: 'sil' });
    d.broadcastAdmin('topluluk_changed', { kanal, at: Date.now() });
  };
  const A = d.requireAdmin;

  /** Ortak mesaj sorgusu (şikâyet ve mesaj listeleri) */
  const mesajListesi = async (req: express.Request, ekKosul: string[]) => {
    const s = listeSorgusu(req, { varsayilanBoyut: 50, enFazla: 200 });
    const where = [...ekKosul];
    const vals: unknown[] = [];
    const add = (sql: string, v: unknown) => { vals.push(v); where.push(sql.replace(/\?/g, `$${vals.length}`)); };
    const f = s.suzgec;
    if (f.tur === 'oda') where.push(`m.kanal like 'oda:%'`);
    if (f.tur === 'kanal') where.push(`m.kanal not like 'oda:%'`);
    if (f.durum === 'gorunur') where.push('not m.silindi');
    if (f.durum === 'gizli') where.push('m.silindi');
    if (f.sikayet === 'var') where.push('cardinality(m.sikayet_uid) > 0');
    if (f.kanal) add('m.kanal = ?', f.kanal);
    if (f.uid) add('m.uid = ?', f.uid);
    if (s.q) add('(m.metin ilike ? or m.ad ilike ? or m.kanal ilike ?)', `%${s.q}%`);
    const w = where.length ? `where ${where.join(' and ')}` : '';
    const sira = ({ at: 'm.olusturma', sikayet: 'cardinality(m.sikayet_uid)', kanal: 'm.kanal', ad: 'm.ad' } as Record<string, string>)[s.sirala] || 'm.id';
    const [{ rows }, c, y] = await Promise.all([
      pgDb.query(
        `select m.id, m.kanal, m.uid, m.ad, m.metin, m.yanit_id, m.olusturma at, m.silindi, m.silen, cardinality(m.sikayet_uid)::int sikayet,
                m.ek, o.ad oda_ad, o.tur oda_tur
           from topluluk_mesajlar m
           left join sohbet_odalari o on m.kanal = 'oda:' || o.id
           ${w} order by ${sira} ${s.yon === 'artan' ? 'asc' : 'desc'} nulls last, m.id desc limit ${s.boyut} offset ${s.sayfa * s.boyut}`, vals),
      pgDb.query(`select count(*)::int n from topluluk_mesajlar m ${w}`, vals),
      pgDb.query(`select case when m.kanal like 'oda:%' then 'oda' else 'kanal' end deger, count(*)::int n from topluluk_mesajlar m ${w} group by 1`, vals),
    ]);
    return { ogeler: rows.map((r: any) => ({ ...r, id: Number(r.id) })), toplam: c.rows[0]?.n || 0, sayfa: s.sayfa, boyut: s.boyut, yuzler: { tur: y.rows } };
  };

  // ---- Şikâyetler (topluluk mesajı) ----
  app.get('/api/admin/topluluk/sikayetler', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try { res.json(await mesajListesi(req, ['cardinality(m.sikayet_uid) > 0'])); } catch (e) { fail(res, e); }
  });
  /** Şikâyeti yersiz bul: şikâyet listesi temizlenir, mesaj gizliyse geri açılır */
  app.post('/api/admin/topluluk/sikayetler/:id/yoksay', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      const id = sayi(req.params.id);
      const r = await pgDb.query(
        `update topluluk_mesajlar set sikayet_uid = '{}', silindi = case when silen like 'yonetici%' then silindi else false end
          where id = $1 returning kanal, cardinality(sikayet_uid) n`, [id]);
      if (!r.rows[0]) return res.status(404).json({ error: 'Mesaj bulunamadı.' });
      denetimHedef(res, `mesaj:${id}`);
      gelenOnbellekSil(); // H290
      haber(r.rows[0].kanal, id);
      res.json({ ok: true });
    } catch (e) { fail(res, e); }
  });

  // ---- Mesajlar ----
  app.get('/api/admin/topluluk/mesajlar', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try { res.json(await mesajListesi(req, [])); } catch (e) { fail(res, e); }
  });
  app.post('/api/admin/topluluk/mesajlar/:id/gizle', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      const id = sayi(req.params.id);
      const gizli = req.body?.gizli !== false;
      const once = (await pgDb.query(`select kanal, silindi, silen from topluluk_mesajlar where id = $1`, [id])).rows[0];
      if (!once) return res.status(404).json({ error: 'Mesaj bulunamadı.' });
      const silen = gizli ? `yonetici:${d.kimOf(req)}`.slice(0, 120) : null;
      await pgDb.query(`update topluluk_mesajlar set silindi = $2, silen = $3 where id = $1`, [id, gizli, silen]);
      denetimHedef(res, `mesaj:${id}`);
      denetimFark(res, { silindi: once.silindi, silen: once.silen }, { silindi: gizli, silen });
      gelenOnbellekSil(); // H290
      haber(once.kanal, id);
      res.json({ ok: true, gizli });
    } catch (e) { fail(res, e); }
  });
  app.delete('/api/admin/topluluk/mesajlar/:id', A, async (req, res) => {
    if (!(await hazir(res))) return;
    if (req.body?.onay !== 'SIL') return res.status(400).json({ error: 'Kalıcı silme için onay sözcüğü (SIL) gerekli.' });
    try {
      const id = sayi(req.params.id);
      const r = await pgDb.query(`delete from topluluk_mesajlar where id = $1 returning kanal, uid, ad, left(metin, 200) metin`, [id]);
      if (!r.rows[0]) return res.status(404).json({ error: 'Mesaj bulunamadı.' });
      denetimHedef(res, `mesaj:${id}`);
      denetimNot(res, { silinen: { kanal: r.rows[0].kanal, ad: r.rows[0].ad, metin: r.rows[0].metin } });
      haber(r.rows[0].kanal, id);
      res.json({ ok: true });
    } catch (e) { fail(res, e); }
  });

  // ---- Kanallar (oda dışı kanal ve ders yorum kanalları) ----
  app.get('/api/admin/topluluk/kanallar', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      const s = listeSorgusu(req, { varsayilanBoyut: 100, enFazla: 500 });
      const vals: unknown[] = [];
      let w = `where kanal not like 'oda:%'`;
      if (s.q) { vals.push(`%${s.q}%`); w += ` and kanal ilike $1`; }
      const sira = ({ kanal: 'kanal', n: 'n', sikayet: 'sikayet', son: 'son' } as Record<string, string>)[s.sirala] || 'son';
      const [{ rows }, c] = await Promise.all([
        pgDb.query(
          `select kanal, count(*)::int n, count(*) filter (where silindi)::int gizli, count(*) filter (where cardinality(sikayet_uid) > 0)::int sikayet,
                  count(distinct uid)::int yazar, max(olusturma) son
             from topluluk_mesajlar ${w} group by kanal order by ${sira} ${s.yon === 'artan' ? 'asc' : 'desc'} nulls last limit ${s.boyut} offset ${s.sayfa * s.boyut}`, vals),
        pgDb.query(`select count(distinct kanal)::int n from topluluk_mesajlar ${w}`, vals),
      ]);
      res.json({ ogeler: rows, toplam: c.rows[0]?.n || 0, sayfa: s.sayfa, boyut: s.boyut });
    } catch (e) { fail(res, e); }
  });

  // ---- Sohbet odaları ----
  app.get('/api/admin/topluluk/odalar', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      const s = listeSorgusu(req, { varsayilanBoyut: 50, enFazla: 200 });
      const where: string[] = [];
      const vals: unknown[] = [];
      if (s.suzgec.tur === 'dm' || s.suzgec.tur === 'grup') { vals.push(s.suzgec.tur); where.push(`o.tur = $${vals.length}`); }
      if (s.suzgec.durum === 'acik') where.push('o.kapali is null');
      if (s.suzgec.durum === 'kapali') where.push('o.kapali is not null');
      if (s.q) {
        vals.push(`%${s.q}%`);
        where.push(`(o.ad ilike $${vals.length} or o.id::text = $${vals.length + 1} or exists (select 1 from sohbet_uyeleri u where u.oda_id = o.id and (u.ad ilike $${vals.length} or u.uid = $${vals.length + 1})))`);
        vals.push(s.q);
      }
      const w = where.length ? `where ${where.join(' and ')}` : '';
      const sira = ({ son: 'o.son', olusturma: 'o.olusturma', uye: 'uye', mesaj: 'mesaj', ad: 'o.ad' } as Record<string, string>)[s.sirala] || 'o.son';
      const [{ rows }, c, y] = await Promise.all([
        pgDb.query(
          `select o.id, o.tur, o.ad, o.kod, o.olusturan, o.olusturma, o.son, o.kapali, o.kapatan,
                  (select count(*)::int from sohbet_uyeleri u where u.oda_id = o.id) uye,
                  (select count(*)::int from topluluk_mesajlar m where m.kanal = 'oda:' || o.id) mesaj,
                  (select string_agg(u.ad, ', ' order by u.katilma) from (select ad, katilma from sohbet_uyeleri where oda_id = o.id order by katilma limit 4) u) uye_adlari
             from sohbet_odalari o ${w} order by ${sira} ${s.yon === 'artan' ? 'asc' : 'desc'} nulls last, o.id desc limit ${s.boyut} offset ${s.sayfa * s.boyut}`, vals),
        pgDb.query(`select count(*)::int n from sohbet_odalari o ${w}`, vals),
        pgDb.query(`select o.tur deger, count(*)::int n from sohbet_odalari o ${w} group by 1`, vals),
      ]);
      res.json({ ogeler: rows.map((r: any) => ({ ...r, id: Number(r.id) })), toplam: c.rows[0]?.n || 0, sayfa: s.sayfa, boyut: s.boyut, yuzler: { tur: y.rows } });
    } catch (e) { fail(res, e); }
  });
  app.get('/api/admin/topluluk/odalar/:id', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      const id = sayi(req.params.id);
      const o = (await pgDb.query(`select * from sohbet_odalari where id = $1`, [id])).rows[0];
      if (!o) return res.status(404).json({ error: 'Oda bulunamadı.' });
      const uyeler = (await pgDb.query(
        `select u.uid, u.ad, u.katilma, u.okundu_id, u.sessiz,
                (select count(*)::int from topluluk_mesajlar m where m.kanal = 'oda:' || u.oda_id and m.uid = u.uid) mesaj
           from sohbet_uyeleri u where u.oda_id = $1 order by u.katilma`, [id])).rows;
      res.json({ oda: { ...o, id: Number(o.id) }, uyeler });
    } catch (e) { fail(res, e); }
  });
  app.get('/api/admin/topluluk/odalar/:id/mesajlar', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      req.query[`s.kanal`] = `oda:${sayi(req.params.id)}`;
      res.json(await mesajListesi(req, []));
    } catch (e) { fail(res, e); }
  });
  /** Kapat/aç (arşiv): kapalı odaya yeni üye katılamaz ve mesaj yazılamaz (toplulukSohbet.ts denetler) */
  app.post('/api/admin/topluluk/odalar/:id/kapat', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      const id = sayi(req.params.id);
      const kapali = req.body?.kapali !== false;
      const once = (await pgDb.query(`select kapali, kapatan from sohbet_odalari where id = $1`, [id])).rows[0];
      if (!once) return res.status(404).json({ error: 'Oda bulunamadı.' });
      const r = await pgDb.query(
        `update sohbet_odalari set kapali = ${kapali ? 'coalesce(kapali, now())' : 'null'}, kapatan = $2 where id = $1 returning kapali, kapatan`,
        [id, kapali ? d.kimOf(req).slice(0, 120) : null]);
      denetimHedef(res, `oda:${id}`);
      denetimFark(res, once, r.rows[0]);
      haber(`oda:${id}`);
      res.json({ ok: true, ...r.rows[0] });
    } catch (e) { fail(res, e); }
  });
  app.post('/api/admin/topluluk/odalar/:id/kod-sifirla', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      const id = sayi(req.params.id);
      const kod = crypto.randomBytes(6).toString('base64url');
      const r = await pgDb.query(`update sohbet_odalari set kod = $2 where id = $1 and tur = 'grup' returning id`, [id, kod]);
      if (!r.rows[0]) return res.status(404).json({ error: 'Grup odası bulunamadı (birebir sohbetin davet kodu yoktur).' });
      denetimHedef(res, `oda:${id}`);
      denetimNot(res, { kod: 'yenilendi' });
      haber(`oda:${id}`);
      res.json({ ok: true, kod });
    } catch (e) { fail(res, e); }
  });
  app.delete('/api/admin/topluluk/odalar/:id/uyeler/:uid', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      const id = sayi(req.params.id);
      const uid = String(req.params.uid || '');
      const r = await pgDb.query(`delete from sohbet_uyeleri where oda_id = $1 and uid = $2 returning ad`, [id, uid]);
      if (!r.rows[0]) return res.status(404).json({ error: 'Üye bulunamadı.' });
      denetimHedef(res, `oda:${id}`);
      denetimNot(res, { cikarilan: { uid, ad: r.rows[0].ad } });
      haber(`oda:${id}`);
      res.json({ ok: true });
    } catch (e) { fail(res, e); }
  });

  // ---- Arkadaşlık ----
  app.get('/api/admin/topluluk/arkadaslik', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      const s = listeSorgusu(req, { varsayilanBoyut: 50, enFazla: 200 });
      const where: string[] = [];
      const vals: unknown[] = [];
      if (s.suzgec.durum === 'bekliyor' || s.suzgec.durum === 'kabul') { vals.push(s.suzgec.durum); where.push(`a.durum = $${vals.length}`); }
      if (s.q) { vals.push(`%${s.q}%`); where.push(`(a.gonderen ilike $${vals.length} or a.alan ilike $${vals.length} or g.ad ilike $${vals.length} or l.ad ilike $${vals.length})`); }
      const w = where.length ? `where ${where.join(' and ')}` : '';
      // Ad: kişinin sohbet/kanal kayıtlarındaki son adı (ayrı ad tablosu yok)
      const adSql = (k: string) => `left join lateral (select ad from sohbet_uyeleri where uid = a.${k} order by katilma desc limit 1) ${k === 'gonderen' ? 'g' : 'l'} on true`;
      const sira = ({ olusturma: 'a.olusturma', guncelleme: 'a.guncelleme', durum: 'a.durum' } as Record<string, string>)[s.sirala] || 'a.guncelleme';
      const [{ rows }, c, y] = await Promise.all([
        pgDb.query(`select a.*, g.ad gonderen_ad, l.ad alan_ad from arkadas_istek a ${adSql('gonderen')} ${adSql('alan')} ${w}
                    order by ${sira} ${s.yon === 'artan' ? 'asc' : 'desc'} limit ${s.boyut} offset ${s.sayfa * s.boyut}`, vals),
        pgDb.query(`select count(*)::int n from arkadas_istek a ${adSql('gonderen')} ${adSql('alan')} ${w}`, vals),
        pgDb.query(`select a.durum deger, count(*)::int n from arkadas_istek a ${adSql('gonderen')} ${adSql('alan')} ${w} group by 1`, vals),
      ]);
      res.json({ ogeler: rows, toplam: c.rows[0]?.n || 0, sayfa: s.sayfa, boyut: s.boyut, yuzler: { durum: y.rows } });
    } catch (e) { fail(res, e); }
  });
  app.post('/api/admin/topluluk/arkadaslik/kaldir', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      const g = String(req.body?.gonderen || ''), a = String(req.body?.alan || '');
      const r = await pgDb.query(`delete from arkadas_istek where gonderen = $1 and alan = $2 returning durum`, [g, a]);
      if (!r.rows[0]) return res.status(404).json({ error: 'Kayıt bulunamadı.' });
      denetimHedef(res, `arkadaslik:${g}|${a}`);
      denetimNot(res, { durum: r.rows[0].durum });
      d.broadcast('arkadas_changed', { at: Date.now() });
      d.broadcastAdmin('topluluk_changed', { at: Date.now() });
      res.json({ ok: true });
    } catch (e) { fail(res, e); }
  });

  // ---- Paylaşılan notlar ----
  app.get('/api/admin/topluluk/notlar', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      const s = listeSorgusu(req, { varsayilanBoyut: 50, enFazla: 200 });
      const where: string[] = [];
      const vals: unknown[] = [];
      if (s.suzgec.durum === 'gorunur') where.push('not n.silindi');
      if (s.suzgec.durum === 'gizli') where.push('n.silindi');
      if (s.q) { vals.push(`%${s.q}%`); where.push(`(n.baslik ilike $1 or n.metin ilike $1 or n.sahip_ad ilike $1)`); }
      const w = where.length ? `where ${where.join(' and ')}` : '';
      const sira = ({ olusturma: 'n.olusturma', baslik: 'n.baslik', sahip_ad: 'n.sahip_ad' } as Record<string, string>)[s.sirala] || 'n.id';
      const [{ rows }, c] = await Promise.all([
        pgDb.query(`select n.id, n.oda_id, n.sahip, n.sahip_ad, n.baslik, left(n.metin, 4000) metin, length(n.metin) uzunluk, n.renk, n.silindi, n.olusturma,
                           o.ad oda_ad, o.tur oda_tur
                      from paylasilan_notlar n left join sohbet_odalari o on o.id = n.oda_id ${w}
                     order by ${sira} ${s.yon === 'artan' ? 'asc' : 'desc'} limit ${s.boyut} offset ${s.sayfa * s.boyut}`, vals),
        pgDb.query(`select count(*)::int n from paylasilan_notlar n ${w}`, vals),
      ]);
      res.json({ ogeler: rows.map((r: any) => ({ ...r, id: Number(r.id) })), toplam: c.rows[0]?.n || 0, sayfa: s.sayfa, boyut: s.boyut });
    } catch (e) { fail(res, e); }
  });
  app.post('/api/admin/topluluk/notlar/:id/gizle', A, async (req, res) => {
    if (!(await hazir(res))) return;
    try {
      const id = sayi(req.params.id);
      const gizli = req.body?.gizli !== false;
      const r = await pgDb.query(`update paylasilan_notlar set silindi = $2 where id = $1 returning oda_id`, [id, gizli]);
      if (!r.rows[0]) return res.status(404).json({ error: 'Not bulunamadı.' });
      denetimHedef(res, `not:${id}`);
      denetimNot(res, { gizli });
      d.broadcast('not_paylas', { oda: Number(r.rows[0].oda_id) });
      d.broadcastAdmin('topluluk_changed', { at: Date.now() });
      res.json({ ok: true, gizli });
    } catch (e) { fail(res, e); }
  });

  // ---- Sayaçlar (sekme rozetleri) ----
  app.get('/api/admin/topluluk/ozet', A, async (_req, res) => {
    if (!(await hazir(res))) return;
    try {
      const { rows } = await pgDb.query(`select
        (select count(*)::int from topluluk_mesajlar where cardinality(sikayet_uid) > 0 and not silindi) sikayet,
        (select count(*)::int from topluluk_mesajlar) mesaj,
        (select count(*)::int from topluluk_mesajlar where olusturma > now() - interval '24 hours') mesaj24,
        (select count(*)::int from sohbet_odalari) oda,
        (select count(*)::int from sohbet_odalari where kapali is not null) kapali_oda,
        (select count(*)::int from arkadas_istek where durum = 'bekliyor') bekleyen_istek,
        (select count(*)::int from arkadas_istek where durum = 'kabul') arkadaslik,
        (select count(*)::int from paylasilan_notlar where not silindi) not_`);
      res.json(rows[0]);
    } catch (e) { fail(res, e); }
  });
}
