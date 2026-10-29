/**
 * Arkadaşlık + açık profil + kapsamlı sıralama (v15 › Arkadaşlar, /kisi/<kimlik>, Sıralama). Sunucu tarafı. 2026-10-27.
 *
 * Kimlik: istemciye uid/e-posta ÇIKMAZ. Açık profil kimliği = topluluk yazar özeti (sha256('topluluk:'+uid) ilk 10),
 * böylece sohbetteki kişi ile profil aynı kimliği taşır. Özet → uid çözümü yalnız sunucuda (başarım motorundaki kişiler).
 * Veri: başarım motoru (profil yedeğinden türeyen gün ölçüleri: çalışma süresi, çözülen soru, konu süreleri) + profil
 * yedeğindeki `medsoru_calisma_takip_v1` (son çalışılan dersler, zaman) ve `stats.activityLog` (doğru/yanlış). Öğrenci bu
 * verileri zaten profil eşitlemesiyle yolluyor; yeni eşitleme gerekmez. Uydurma veri yok.
 * Gizlilik: varsayılan herkese açık; "Profilim herkese açık" kapatılınca sıralamada "Gizli kullanıcı", profil kapalı.
 *
 *   GET  /api/kisi/ben                       kendi kimliğim + gizlilik
 *   POST /api/kisi/gizlilik {acik}           profilim herkese açık mı
 *   GET  /api/kisi/ara?q=                    ad ile kişi bulma (gizliler çıkmaz)
 *   GET  /api/kisi/siralama?olcu=puan|calisma|soru|bitir|basarim|hucre|oyun[&oyun=<tür>]&kapsam=hafta|kurul|tum|gun&yer=sinif|uni|tr|arkadas
 *   GET  /api/kisi/:kimlik                   açık profil
 *   GET  /api/arkadas                        arkadaşlar + gelen/giden istekler
 *   POST /api/arkadas/istek|kabul|reddet|cikar {kimlik}
 *   POST /api/arkadas/sohbet {kimlik, benAd}  birebir sohbeti aç (topluluk sohbet odası; arkadaş olmak gerekmez)
 *   POST /api/arkadas/davet {kimlik, oda}    arkadaşı soru çözme odasına davet (bildirim + sohbet mesajı)
 * Yazma uçları doğrulanmış Firebase kullanıcısı ister (verifiedUid), uid başına hız sınırı. SSE `arkadas_changed`
 * {who: userEventHash(uid)} yalnız ilgili kişinin istemcisini tazeler (içerik taşımaz); kalıcı bildirim notifyStudent ile.
 * LLM, zamanlayıcı yok.
 */
import fs from 'fs';
import path from 'path';
import type express from 'express';
import { pgDb } from './pgDb';
import { verifiedUid } from './adminAuth';
import { temizle } from './topluluk';
import type { BasarimMotor, SiraOlcu } from './basarim/basarimMotor';
const SIRA_OLCU = ['puan', 'calisma', 'soru', 'bitir', 'basarim', 'hucre', 'oyun'] as const;

interface Bildirim { type: string; title: string; message: string; deepLinkUrl?: string; targetType?: string; targetId?: string; dedupeKey?: string }
interface Deps {
  rootDir: string;
  isPgOnline: () => boolean;
  motor: BasarimMotor;
  okuYedek: (uid: string) => any | null;
  broadcast: (event: string, data: any) => void;
  userEventHash: (uid: string) => string;
  notifyStudent: (target: { uid?: string | null }, n: Bildirim) => unknown;
}

const KIMLIK = /^[0-9a-f]{10}$/;
const ODA = /^[A-Z0-9]{4,6}$/;
const ARKADAS_MAX = 500;
const eylem = new Map<string, number[]>();
function hizli(anahtar: string, araMs = 1500, saatlik = 120): string {
  const simdi = Date.now();
  const g = (eylem.get(anahtar) || []).filter((t) => simdi - t < 3_600_000);
  if (g.length && simdi - g[g.length - 1] < araMs) return 'Biraz yavaş: birkaç saniye bekle.';
  if (g.length >= saatlik) return 'Saatlik sınıra ulaştın.';
  g.push(simdi); eylem.set(anahtar, g);
  if (eylem.size > 20000) eylem.clear();
  return '';
}
const kvJson = (b: any, key: string) => { try { const r = b?.kv?.[key]; return r?.v ? JSON.parse(r.v) : null; } catch { return null; } };
const fold = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');

export function registerArkadaslik(app: express.Express, d: Deps) {
  const { motor } = d;
  let sema = false;
  const semaKur = async () => {
    if (sema || !d.isPgOnline()) return sema;
    try { await pgDb.query(fs.readFileSync(path.join(d.rootDir, 'deploy', 'pg', 'sql', 'arkadaslik.sql'), 'utf8')); sema = true; }
    catch (e: any) { console.warn('[Arkadaslik] şema:', e?.message); }
    return sema;
  };
  void semaKur();
  const hazir = async (res: express.Response) => {
    if (await semaKur()) return true;
    res.status(503).json({ error: 'Arkadaşlık şu an kullanılamıyor.' });
    return false;
  };

  // Özet → uid (yalnız sunucuda). Önbellek 60 sn; bulunamazsa bir kez tazelenir.
  let harita = new Map<string, string>(); let haritaAt = 0;
  const haritaKur = () => { harita = new Map(motor.hepsi().map((k) => [motor.kisiKimlik(k.uid), k.uid])); haritaAt = Date.now(); };
  const uidOf = (kimlik: string): string | null => {
    if (!KIMLIK.test(kimlik)) return null;
    if (!haritaAt || Date.now() - haritaAt > 60_000) haritaKur();
    let u = harita.get(kimlik);
    if (!u && Date.now() - haritaAt > 5_000) { haritaKur(); u = harita.get(kimlik); }
    return u || null;
  };

  /** Ben ↔ o: 'arkadas' | 'giden' | 'gelen' | 'yok' */
  const iliski = async (ben: string, o: string): Promise<'arkadas' | 'giden' | 'gelen' | 'yok'> => {
    if (!sema) return 'yok';
    const { rows } = await pgDb.query(`select gonderen, durum from arkadas_istek where (gonderen = $1 and alan = $2) or (gonderen = $2 and alan = $1)`, [ben, o]);
    if (rows.some((r: any) => r.durum === 'kabul')) return 'arkadas';
    if (rows.some((r: any) => r.gonderen === ben)) return 'giden';
    if (rows.length) return 'gelen';
    return 'yok';
  };
  const arkadasUidleri = async (uid: string): Promise<string[]> => {
    if (!(await semaKur())) return [];
    const { rows } = await pgDb.query(
      `select case when gonderen = $1 then alan else gonderen end o from arkadas_istek where durum = 'kabul' and (gonderen = $1 or alan = $1) limit ${ARKADAS_MAX}`, [uid]);
    return rows.map((r: any) => r.o);
  };

  /** Profil yedeğinden: son çalışılan dersler (zamanla) + doğru/yanlış sayısı */
  const yedekOzeti = (uid: string) => {
    const b = d.okuYedek(uid);
    const takip = kvJson(b, 'medsoru_calisma_takip_v1');
    const dersler = Object.entries<any>(takip?.k || {})
      .filter(([, r]) => r?.sonAt && (Number(r.sn) || 0) + (Number(r.soru) || 0) > 0)
      .map(([id, r]) => ({ id, ...motor.konuAdi(id), sn: Math.max(0, Number(r.sn) || 0), soru: Math.max(0, Number(r.soru) || 0), bitti: r.durum === 'bitti', sonAt: Date.parse(r.sonAt) || 0 }))
      .sort((a, b2) => b2.sonAt - a.sonAt);
    let dogru = 0, yanlis = 0;
    for (const a of Array.isArray(b?.stats?.activityLog) ? b.stats.activityLog : []) {
      if (a?.kind === 'coz') dogru++; else if (a?.kind === 'yanlis') yanlis++;
    }
    return { dersler, dogru, yanlis };
  };

  const kart = (uid: string, ekSon = false) => {
    const k = motor.kisi(uid);
    const o = motor.profilOlcu(uid);
    const son = ekSon ? yedekOzeti(uid).dersler[0] : undefined;
    return {
      kimlik: motor.kisiKimlik(uid), ad: k.gizli ? 'Gizli kullanıcı' : o.ad, foto: k.gizli ? undefined : o.foto,
      universite: k.gizli ? '' : o.universite, donem: o.donem, gizli: !!k.gizli || undefined,
      haftaSn: k.gizli ? undefined : o.calisma.hafta, bugunSn: k.gizli ? undefined : o.calisma.bugun,
      son: !k.gizli && son ? { ad: son.ad, modul: son.modul, at: son.sonAt } : undefined,
    };
  };

  /** Hedef kişinin istemcisini tazele (içerik yok) */
  const haber = (...uidler: string[]) => { for (const u of uidler) d.broadcast('arkadas_changed', { who: d.userEventHash(u), at: Date.now() }); };

  // ───── Kimlik ve gizlilik ─────
  app.get('/api/kisi/ben', (req, res) => {
    const uid = verifiedUid(req);
    res.set('Cache-Control', 'no-store');
    if (!uid) return res.json({ girisli: false });
    res.json({ girisli: true, kimlik: motor.kisiKimlik(uid), acik: !motor.kisi(uid).gizli });
  });
  app.post('/api/kisi/gizlilik', (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.status(401).json({ error: 'Giriş gerekli.' });
    const h = hizli(`g:${uid}`, 1000, 60); if (h) return res.status(429).json({ error: h });
    motor.gizlilik(uid, req.body?.acik === false);
    d.broadcast('siralama_changed', { at: Date.now() });
    res.json({ ok: true, acik: !motor.kisi(uid).gizli });
  });

  // ───── Kişi bulma ─────
  app.get('/api/kisi/ara', async (req, res) => {
    const uid = verifiedUid(req);
    if (!uid) return res.status(401).json({ error: 'Kişi aramak için giriş yapmalısın.' });
    const q = fold(String(req.query.q || '').trim()).slice(0, 40);
    res.set('Cache-Control', 'no-store');
    if (q.length < 2) return res.json({ kisiler: [] });
    const h = hizli(`a:${uid}`, 250, 600); if (h) return res.status(429).json({ error: h });
    await semaKur();
    const bul = motor.hepsi().filter((k) => k.uid !== uid && !k.gizli && k.ad && fold(k.ad).includes(q)).slice(0, 20);
    const kisiler = [];
    for (const k of bul) kisiler.push({ ...kart(k.uid), iliski: await iliski(uid, k.uid) });
    res.json({ kisiler });
  });

  // ───── Oyun rekorları: profil yedeğindeki medsoru_oyun_rekor_v1 (`<oyun>:<ders|*>` → en iyi skor), 60 sn önbellek ─────
  let rekorOnb: { t: number; m: Map<string, Record<string, number>> } = { t: 0, m: new Map() };
  const rekorlar = () => {
    if (Date.now() - rekorOnb.t < 60_000) return rekorOnb.m;
    const m = new Map<string, Record<string, number>>();
    for (const k of motor.hepsi()) {
      const r = kvJson(d.okuYedek(k.uid), 'medsoru_oyun_rekor_v1');
      if (r && typeof r === 'object') m.set(k.uid, r);
    }
    rekorOnb = { t: Date.now(), m };
    return m;
  };
  // Eşleştir rekoru süredir (küçük iyi), puan toplamına girmez
  const SUREli = new Set(['eslestir']);
  /** Seçili oyun türünün (yoksa tüm puanlı oyunların) ders başına en iyi skorlarının toplamı */
  const oyunPuani = (uid: string, oyun: string) => Object.entries(rekorlar().get(uid) || {})
    .reduce((a, [anahtar, v]) => { const t = anahtar.split(':')[0]; return !SUREli.has(t) && (!oyun || t === oyun) ? a + Math.max(0, Math.round(Number(v) || 0)) : a; }, 0);
  const oyunTurleri = () => [...new Set([...rekorlar().values()].flatMap((r) => Object.keys(r).map((a) => a.split(':')[0])))].filter((t) => !SUREli.has(t)).sort();

  // ───── Sıralama: puan | çalışma × sınıf | üni | Türkiye | arkadaşlar ─────
  app.get('/api/kisi/siralama', async (req, res) => {
    const uid = verifiedUid(req) || null;
    const olcu = (SIRA_OLCU as readonly string[]).includes(String(req.query.olcu)) ? String(req.query.olcu) as SiraOlcu : 'puan';
    const kq = String(req.query.kapsam);
    const kapsam = olcu === 'calisma' ? (kq === 'gun' ? 'gun' : 'hafta')
      : olcu === 'soru' || olcu === 'bitir' ? (['gun', 'hafta', 'tum'].includes(kq) ? kq : 'hafta')
      : olcu === 'puan' ? (['hafta', 'kurul', 'tum'].includes(kq) ? kq : 'hafta') : 'tum';
    const oyunSec = String(req.query.oyun || '').replace(/[^a-z0-9_-]/gi, '').slice(0, 24);
    const ek = olcu === 'oyun' ? { disDeger: (u: string) => oyunPuani(u, oyunSec), oyunlar: oyunTurleri() } : {};
    const disDeger = (ek as any).disDeger as ((u: string) => number) | undefined;
    const oyunlar = (ek as any).oyunlar as string[] | undefined;
    const yer = ['sinif', 'uni', 'arkadas'].includes(String(req.query.yer)) ? String(req.query.yer) : 'tr';
    res.set('Cache-Control', 'no-store');
    const benimDonem = uid && motor.varMi(uid) ? motor.kisi(uid).donem : null;
    const donem = Number(req.query.donem) || benimDonem || 3;
    if (yer === 'arkadas') {
      if (!uid) return res.json({ olcu, kapsam, yer, girisli: false, satir: [] });
      const ark = await arkadasUidleri(uid);
      if (!ark.length) return res.json({ olcu, kapsam, yer, arkadasN: 0, satir: [] });
      return res.json({ olcu, kapsam, yer, oyunlar, arkadasN: ark.length, ...motor.kisiSiralama({ uid, olcu, kapsam, donem: null, uidler: new Set([...ark, uid]), disDeger }) });
    }
    if (yer === 'sinif' || yer === 'uni') {
      const uni = uid ? motor.universiteOf(uid) : '';
      if (!uni) return res.json({ olcu, kapsam, yer, universite: '', satir: [] });
      return res.json({ olcu, kapsam, yer, oyunlar, universite: uni, donem: yer === 'sinif' ? donem : undefined, ...motor.kisiSiralama({ uid, olcu, kapsam, donem: yer === 'sinif' ? donem : null, universite: uni, disDeger }) });
    }
    res.json({ olcu, kapsam, yer, oyunlar, donem, ...motor.kisiSiralama({ uid, olcu, kapsam, donem, disDeger }) });
  });

  // ───── Arkadaş listesi ─────
  app.get('/api/arkadas', async (req, res) => {
    const uid = verifiedUid(req);
    res.set('Cache-Control', 'no-store');
    if (!uid) return res.json({ girisli: false, arkadaslar: [], gelen: [], giden: [] });
    if (!(await hazir(res))) return;
    const { rows } = await pgDb.query(
      `select gonderen, alan, durum, guncelleme from arkadas_istek where gonderen = $1 or alan = $1 order by guncelleme desc limit ${ARKADAS_MAX * 2}`, [uid]);
    const arkadaslar: any[] = [], gelen: any[] = [], giden: any[] = [];
    for (const r of rows) {
      const o = r.gonderen === uid ? r.alan : r.gonderen;
      if (!motor.varMi(o)) continue;
      const at = new Date(r.guncelleme).getTime();
      if (r.durum === 'kabul') arkadaslar.push({ ...kart(o, true), at });
      else if (r.gonderen === uid) giden.push({ ...kart(o), at });
      else gelen.push({ ...kart(o), at });
    }
    arkadaslar.sort((a, b) => (b.son?.at || 0) - (a.son?.at || 0));
    res.json({ girisli: true, kimlik: motor.kisiKimlik(uid), arkadaslar, gelen, giden });
  });

  const hedefAl = (req: express.Request, res: express.Response): { uid: string; o: string } | null => {
    const uid = verifiedUid(req);
    if (!uid) { res.status(401).json({ error: 'Bunun için giriş yapmalısın.' }); return null; }
    const o = uidOf(String(req.body?.kimlik || ''));
    if (!o) { res.status(404).json({ error: 'Kişi bulunamadı.' }); return null; }
    if (o === uid) { res.status(400).json({ error: 'Bu sensin.' }); return null; }
    return { uid, o };
  };
  const benAdi = (uid: string) => motor.kisi(uid).ad || 'Bir arkadaşın';

  app.post('/api/arkadas/istek', async (req, res) => {
    const h0 = hedefAl(req, res); if (!h0) return;
    const { uid, o } = h0;
    if (!(await hazir(res))) return;
    const h = hizli(`i:${uid}`, 1500, 60); if (h) return res.status(429).json({ error: h });
    const durum = await iliski(uid, o);
    if (durum === 'arkadas') return res.json({ iliski: 'arkadas' });
    if (durum === 'giden') return res.json({ iliski: 'giden' });
    if (durum === 'gelen') {
      // Karşı taraf zaten istek yollamış: kabul et
      await pgDb.query(`update arkadas_istek set durum = 'kabul', guncelleme = now() where gonderen = $1 and alan = $2`, [o, uid]);
      d.notifyStudent({ uid: o }, { type: 'arkadas', title: 'Arkadaşlık isteğin kabul edildi', message: `${benAdi(uid)} artık arkadaşın.`, deepLinkUrl: `/kisi/${motor.kisiKimlik(uid)}`, dedupeKey: `arkadas_kabul:${motor.kisiKimlik(uid)}:${motor.kisiKimlik(o)}` });
      haber(uid, o);
      return res.json({ iliski: 'arkadas' });
    }
    const n = (await pgDb.query(`select count(*)::int n from arkadas_istek where gonderen = $1 and durum = 'bekliyor'`, [uid])).rows[0].n;
    if (n >= 100) return res.status(409).json({ error: 'Çok fazla bekleyen isteğin var; önce bazılarını geri çek.' });
    await pgDb.query(`insert into arkadas_istek (gonderen, alan) values ($1, $2) on conflict do nothing`, [uid, o]);
    d.notifyStudent({ uid: o }, { type: 'arkadas', title: 'Yeni arkadaşlık isteği', message: `${benAdi(uid)} seni arkadaş olarak eklemek istiyor.`, deepLinkUrl: `/arkadaslar?kimlik=${motor.kisiKimlik(uid)}`, dedupeKey: `arkadas_istek:${motor.kisiKimlik(uid)}:${motor.kisiKimlik(o)}:${new Date().toISOString().slice(0, 10)}` });
    haber(uid, o);
    res.json({ iliski: 'giden' });
  });

  app.post('/api/arkadas/kabul', async (req, res) => {
    const h0 = hedefAl(req, res); if (!h0) return;
    const { uid, o } = h0;
    if (!(await hazir(res))) return;
    const r = await pgDb.query(`update arkadas_istek set durum = 'kabul', guncelleme = now() where gonderen = $1 and alan = $2 and durum = 'bekliyor'`, [o, uid]);
    if (!r.rowCount) return res.status(404).json({ error: 'Bekleyen istek bulunamadı.' });
    d.notifyStudent({ uid: o }, { type: 'arkadas', title: 'Arkadaşlık isteğin kabul edildi', message: `${benAdi(uid)} artık arkadaşın.`, deepLinkUrl: `/kisi/${motor.kisiKimlik(uid)}`, dedupeKey: `arkadas_kabul:${motor.kisiKimlik(uid)}:${motor.kisiKimlik(o)}` });
    haber(uid, o);
    res.json({ iliski: 'arkadas' });
  });

  // Reddet (gelen), geri çek (giden) ve arkadaşlıktan çıkar aynı işlem: iki yöndeki satır silinir
  const sil = async (req: express.Request, res: express.Response) => {
    const h0 = hedefAl(req, res); if (!h0) return;
    const { uid, o } = h0;
    if (!(await hazir(res))) return;
    const h = hizli(`s:${uid}`, 500, 200); if (h) return res.status(429).json({ error: h });
    await pgDb.query(`delete from arkadas_istek where (gonderen = $1 and alan = $2) or (gonderen = $2 and alan = $1)`, [uid, o]);
    haber(uid, o);
    res.json({ iliski: 'yok' });
  };
  app.post('/api/arkadas/reddet', sil);
  app.post('/api/arkadas/cikar', sil);

  /** Birebir sohbet odası (topluluk sohbet tabloları; toplulukSohbet.ts ile aynı dm_anahtar) */
  const dmAc = async (uid: string, o: string, benAd: string): Promise<number> => {
    await pgDb.query(fs.readFileSync(path.join(d.rootDir, 'deploy', 'pg', 'sql', 'topluluk.sql'), 'utf8')).catch(() => 0);
    await pgDb.query(fs.readFileSync(path.join(d.rootDir, 'deploy', 'pg', 'sql', 'topluluk_sohbet.sql'), 'utf8')).catch(() => 0);
    const anahtar = [uid, o].sort().join('|');
    const var0 = await pgDb.query(`select id from sohbet_odalari where dm_anahtar = $1`, [anahtar]);
    let id = var0.rows[0] ? Number(var0.rows[0].id) : 0;
    if (!id) {
      const { rows } = await pgDb.query(
        `insert into sohbet_odalari (tur, olusturan, dm_anahtar) values ('dm', $1, $2) on conflict (dm_anahtar) do update set son = sohbet_odalari.son returning id`, [uid, anahtar]);
      id = Number(rows[0].id);
    }
    await pgDb.query(`insert into sohbet_uyeleri (oda_id, uid, ad) values ($1, $2, $3), ($1, $4, $5) on conflict do nothing`,
      [id, uid, benAd, o, motor.kisi(o).ad || 'Öğrenci']);
    return id;
  };
  app.post('/api/arkadas/sohbet', async (req, res) => {
    const h0 = hedefAl(req, res); if (!h0) return;
    const { uid, o } = h0;
    if (!d.isPgOnline()) return res.status(503).json({ error: 'Sohbet şu an kullanılamıyor.' });
    if (motor.kisi(o).gizli && (await iliski(uid, o)) !== 'arkadas') return res.status(404).json({ error: 'Kişi bulunamadı.' });
    const h = hizli(`m:${uid}`, 1500, 120); if (h) return res.status(429).json({ error: h });
    const id = await dmAc(uid, o, temizle(req.body?.benAd, 40) || motor.kisi(uid).ad || 'Öğrenci');
    d.broadcast('topluluk_sohbet', { oda: id });
    res.json({ id });
  });

  app.post('/api/arkadas/davet', async (req, res) => {
    const h0 = hedefAl(req, res); if (!h0) return;
    const { uid, o } = h0;
    if (!(await hazir(res))) return;
    const oda = String(req.body?.oda || '').toUpperCase();
    if (!ODA.test(oda)) return res.status(400).json({ error: 'Geçersiz oda kodu.' });
    if ((await iliski(uid, o)) !== 'arkadas') return res.status(403).json({ error: 'Yalnız arkadaşlarını davet edebilirsin.' });
    const h = hizli(`d:${uid}`, 3000, 60); if (h) return res.status(429).json({ error: h });
    const ad = benAdi(uid);
    const link = `/sorular/oyunlar?oda=${oda}`;
    let sohbetId = 0;
    try {
      sohbetId = await dmAc(uid, o, temizle(req.body?.benAd, 40) || motor.kisi(uid).ad || 'Öğrenci');
      const u = (await pgDb.query(`select ad from sohbet_uyeleri where oda_id = $1 and uid = $2`, [sohbetId, uid])).rows[0];
      const { rows } = await pgDb.query(`insert into topluluk_mesajlar (kanal, uid, ad, metin) values ($1, $2, $3, $4) returning id`,
        [`oda:${sohbetId}`, uid, u?.ad || ad, `Soru çözmeye davet: oda ${oda}. Katılmak için: ${link}`]);
      await pgDb.query(`update sohbet_odalari set son = now() where id = $1`, [sohbetId]);
      await pgDb.query(`update sohbet_uyeleri set okundu_id = $3 where oda_id = $1 and uid = $2`, [sohbetId, uid, rows[0].id]);
      d.broadcast('topluluk_sohbet', { oda: sohbetId });
    } catch (e: any) { console.warn('[Arkadaslik] davet mesajı:', e?.message); }
    d.notifyStudent({ uid: o }, { type: 'davet', title: 'Soru çözmeye davet', message: `${ad} seni ${oda} odasında soru çözmeye çağırıyor.`, deepLinkUrl: link, dedupeKey: `davet:${motor.kisiKimlik(uid)}:${motor.kisiKimlik(o)}:${oda}` });
    haber(o);
    res.json({ ok: true, sohbet: sohbetId || undefined });
  });

  // ───── Açık profil (en sonda: /api/kisi/ben, /ara, /siralama önce eşleşir) ─────
  app.get('/api/kisi/:kimlik', async (req, res) => {
    const ben = verifiedUid(req);
    res.set('Cache-Control', 'no-store');
    if (!ben) return res.status(401).json({ error: 'Profilleri görmek için giriş yapmalısın.' });
    const o = uidOf(String(req.params.kimlik));
    if (!o) return res.status(404).json({ error: 'Kişi bulunamadı.' });
    await semaKur();
    const kendim = o === ben;
    const ili = kendim ? 'ben' : await iliski(ben, o);
    const k = motor.kisi(o);
    const arkadasN = (await arkadasUidleri(o)).length;
    if (k.gizli && !kendim) return res.json({ kimlik: req.params.kimlik, gizli: true, ad: 'Gizli kullanıcı', iliski: ili });
    const olcu = motor.profilOlcu(o);
    const y = yedekOzeti(o);
    res.json({
      kimlik: motor.kisiKimlik(o), ben: kendim, iliski: ili, arkadasN, acik: !k.gizli,
      ad: olcu.ad, foto: olcu.foto, universite: olcu.universite, donem: olcu.donem, kidem: olcu.kidem, unvan: olcu.unvan,
      calisma: olcu.calisma, soru: olcu.soru, bitirilen: olcu.bitirilen, basarim: olcu.basarim, puan: olcu.puan,
      dogru: y.dogru, yanlis: y.yanlis,
      son: y.dersler[0] ? { ad: y.dersler[0].ad, modul: y.dersler[0].modul, at: y.dersler[0].sonAt } : null,
      dersler: y.dersler.slice(0, 12).map((x) => ({ ad: x.ad, modul: x.modul, sn: x.sn, soru: x.soru, bitti: x.bitti, at: x.sonAt })),
      haftaDersler: olcu.haftaDersler.map((x) => ({ ad: x.ad, modul: x.modul, sn: x.sn })),
    });
  });
}
