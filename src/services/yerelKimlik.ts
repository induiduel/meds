/**
 * yerelKimlik.ts — MeDSor hesapları ve oturumları (2026-11-02; Firebase Auth'un yerine).
 *
 * Veri Oracle meds-pg'de: auth_hesaplar / auth_oturumlar / auth_kodlar (deploy/pg/sql/kimlik.sql, açılışta uygulanır).
 * Jeton imzası/doğrulaması kimlikDogrulama.ts'de. İstemci: src/services/auth.ts.
 *
 * Uçlar (/api/kimlik/*):
 *   POST kayit        { email, sifre, ad?, ogrenciNo? }   → yeni hesap + oturum
 *   POST giris        { email, sifre }                    → oturum
 *   POST yenile       { yenileme }                        → yeni erişim jetonu (yenileme jetonu aynı kalır)
 *   POST cikis        { yenileme }                        → oturum silinir
 *   POST kod-gonder   { email, amac: 'sifre'|'giris' }    → e-postaya 6 haneli kod (15 dk, 5 deneme)
 *   POST kod-dogrula  { email, kod, amac, yeniSifre? }    → şifre belirlenir / kodla giriş, oturum
 *   POST sifre        (Bearer) { yeniSifre }              → açık oturumdaki hesabın şifresi
 *   POST profil       (Bearer) { ad?, foto? }             → hesap adı/fotoğrafı
 *   GET  ben          (Bearer)                            → hesap özeti
 *   GET  /api/admin/kimlik/hesaplar                       → yönetici: hesap listesi (özetsiz)
 *   POST /api/admin/kimlik/sifirlama-kodu { email }       → yönetici: e-posta gitmezse elle iletilecek kod
 *   POST /api/admin/kimlik/oturumlari-kapat { uid }       → yönetici: hesabın tüm oturumları
 *
 * Firebase döneminden taşınan hesapların şifresi bilinmez (sifre_ozeti null): kullanıcı "Şifremi unuttum / Şifre
 * belirle" ile e-postasına gelen kodla şifre koyar; uid aynı kaldığı için tüm verisi yerinde açılır.
 */
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import type express from 'express';
import { pgDb } from './pgDb';
import { erisimJetonuUret, erisimJetonuDogrula, bearerToken, oturumIptalZamani, ERISIM_OMRU_SN } from './kimlikDogrulama';

type Deps = {
  rootDir: string;
  adminEmail: string;
  isAdmin: (req: express.Request) => boolean;
  /** E-posta gönderir; SMTP yoksa false döner. */
  epostaGonder: (to: string, konu: string, html: string, metin: string) => Promise<boolean>;
  /** Yeni hesap açıldı (karşılama e-postası, users.json kaydı server.ts'de). */
  hesapAcildi?: (h: { uid: string; email: string; ad: string; ogrenciNo: string | null }) => void;
};

const YENILEME_OMRU_GUN = 180;
const KOD_OMRU_DK = 15;
const lc = (v: unknown) => String(v || '').trim().toLowerCase();
const EPOSTA = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const sha = (s: string) => crypto.createHash('sha256').update(s).digest('hex');

/* ---------------- şifre özeti (scrypt) ---------------- */
const SCRYPT = { N: 16384, r: 8, p: 1, len: 64 };
function sifreOzeti(sifre: string): Promise<string> {
  const tuz = crypto.randomBytes(16);
  return new Promise((ok, red) =>
    crypto.scrypt(sifre, tuz, SCRYPT.len, { N: SCRYPT.N, r: SCRYPT.r, p: SCRYPT.p }, (e, k) =>
      e ? red(e) : ok(`scrypt$${SCRYPT.N}$${SCRYPT.r}$${SCRYPT.p}$${tuz.toString('base64')}$${k.toString('base64')}`)));
}
function sifreDogru(sifre: string, ozet: string | null): Promise<boolean> {
  const p = String(ozet || '').split('$');
  if (p.length !== 6 || p[0] !== 'scrypt') return Promise.resolve(false);
  const [N, r, pp] = [Number(p[1]), Number(p[2]), Number(p[3])];
  const tuz = Buffer.from(p[4], 'base64');
  const beklenen = Buffer.from(p[5], 'base64');
  return new Promise((ok) =>
    crypto.scrypt(sifre, tuz, beklenen.length, { N, r, p: pp }, (e, k) => ok(!e && crypto.timingSafeEqual(k, beklenen))));
}

/** Firebase uid'lerine benzer 28 karakterlik kimlik */
function yeniUid(): string {
  const abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const b = crypto.randomBytes(28);
  return Array.from(b, (x) => abc[x % abc.length]).join('');
}

/* ---------------- hız sınırı (bellekte) ---------------- */
const sayac = new Map<string, number[]>();
function sinirAsildi(anahtar: string, adet: number, pencereMs: number): boolean {
  const now = Date.now();
  const a = (sayac.get(anahtar) || []).filter((t) => t > now - pencereMs);
  if (a.length >= adet) { sayac.set(anahtar, a); return true; }
  a.push(now);
  sayac.set(anahtar, a);
  if (sayac.size > 20000) sayac.clear();
  return false;
}
const ipOf = (req: express.Request) =>
  String(req.headers['cf-connecting-ip'] || req.headers['x-real-ip'] || String(req.headers['x-forwarded-for'] || '').split(',')[0] || req.socket?.remoteAddress || '').trim();

type Hesap = {
  uid: string; email: string; sifre_ozeti: string | null; ad: string | null; foto: string | null;
  eposta_dogrulandi: boolean; devre_disi: boolean; kaynak: string;
};

export function registerYerelKimlik(app: express.Express, d: Deps) {
  let sema = false;
  const semaKur = async () => {
    if (sema) return true;
    try {
      await pgDb.query(fs.readFileSync(path.join(d.rootDir, 'deploy', 'pg', 'sql', 'kimlik.sql'), 'utf8'));
      sema = true;
    } catch (e: any) {
      console.warn('[Kimlik] şema:', e?.message);
    }
    return sema;
  };
  void semaKur();

  const hazir = async (res: express.Response) => {
    if (await semaKur()) return true;
    res.status(503).json({ ok: false, error: 'Giriş sistemi şu an hazır değil. Biraz sonra tekrar deneyin.' });
    return false;
  };

  const hesapEposta = async (email: string): Promise<Hesap | null> =>
    (await pgDb.query('select * from auth_hesaplar where lower(email) = $1', [lc(email)])).rows[0] || null;
  const hesapUid = async (uid: string): Promise<Hesap | null> =>
    (await pgDb.query('select * from auth_hesaplar where uid = $1', [uid])).rows[0] || null;

  const disHesap = (h: Hesap) => ({
    uid: h.uid, email: h.email, displayName: h.ad || null, photoURL: h.foto || null,
    sifreVar: !!h.sifre_ozeti, epostaDogrulandi: !!h.eposta_dogrulandi,
  });

  /** Yeni oturum: yenileme jetonu (özeti saklanır) + erişim jetonu */
  async function oturumAc(h: Hesap, req: express.Request) {
    const yenileme = crypto.randomBytes(32).toString('base64url');
    const girisSn = Math.floor(Date.now() / 1000);
    await pgDb.query(
      `insert into auth_oturumlar (id, uid, giris_zamani, bitis, cihaz) values ($1, $2, to_timestamp($3), now() + ($4 || ' days')::interval, $5)`,
      [sha(yenileme), h.uid, girisSn, String(YENILEME_OMRU_GUN), String(req.headers['user-agent'] || '').slice(0, 200)],
    );
    await pgDb.query('update auth_hesaplar set son_giris = now() where uid = $1', [h.uid]);
    // Eski oturumları temizle (hesap başına en çok 20)
    void pgDb.query(
      `delete from auth_oturumlar where uid = $1 and id not in (select id from auth_oturumlar where uid = $1 order by son_kullanim desc limit 20)`,
      [h.uid]).catch(() => {});
    const e = erisimJetonuUret({ uid: h.uid, email: h.email, authTime: girisSn });
    return { ok: true, user: disHesap(h), token: e.token, exp: e.exp, yenileme };
  }

  const hata = (res: express.Response, kod: number, msg: string, extra: Record<string, unknown> = {}) =>
    res.status(kod).json({ ok: false, error: msg, ...extra });

  const sifreGecerli = (s: string) => s.length >= 6 && s.length <= 200;

  /* ---------------- kayıt ---------------- */
  app.post('/api/kimlik/kayit', async (req, res) => {
    if (!(await hazir(res))) return;
    const email = lc(req.body?.email);
    const sifre = String(req.body?.sifre || '');
    const ad = String(req.body?.ad || '').trim().slice(0, 80) || email.split('@')[0];
    const ogrenciNo = String(req.body?.ogrenciNo || '').replace(/\D/g, '').slice(0, 12) || null;
    if (!EPOSTA.test(email)) return hata(res, 400, 'E-posta adresi geçersiz.');
    if (!sifreGecerli(sifre)) return hata(res, 400, 'Şifre en az 6 karakter olmalı.');
    if (sinirAsildi(`kayit:${ipOf(req)}`, 10, 60 * 60_000)) return hata(res, 429, 'Çok fazla deneme yapıldı. Biraz sonra tekrar deneyin.');
    const var_ = await hesapEposta(email);
    if (var_) {
      if (!var_.sifre_ozeti) {
        return hata(res, 409, 'Bu e-postayla hesabın zaten var (eski giriş sisteminden taşındı). "Şifremi unuttum / Şifre belirle" ile e-postana gelen kodla şifreni belirle; tüm verilerin yerinde.', { kod: 'sifre-belirle' });
      }
      return hata(res, 409, 'Bu e-posta zaten kayıtlı. Giriş yapın ya da şifrenizi sıfırlayın.', { kod: 'kayitli' });
    }
    const uid = yeniUid();
    await pgDb.query(
      `insert into auth_hesaplar (uid, email, sifre_ozeti, ad, kaynak) values ($1, $2, $3, $4, 'yerel')`,
      [uid, email, await sifreOzeti(sifre), ad]);
    const h = (await hesapUid(uid))!;
    try { d.hesapAcildi?.({ uid, email, ad, ogrenciNo }); } catch { /* yok */ }
    res.json(await oturumAc(h, req));
  });

  /* ---------------- giriş ---------------- */
  app.post('/api/kimlik/giris', async (req, res) => {
    if (!(await hazir(res))) return;
    const email = lc(req.body?.email);
    const sifre = String(req.body?.sifre || '');
    if (!email || !sifre) return hata(res, 400, 'Lütfen e-posta ve şifrenizi giriniz.');
    if (sinirAsildi(`giris:${email}`, 10, 15 * 60_000) || sinirAsildi(`giris-ip:${ipOf(req)}`, 40, 15 * 60_000)) {
      return hata(res, 429, 'Çok fazla deneme yapıldı. Birkaç dakika sonra tekrar deneyin.');
    }
    const h = await hesapEposta(email);
    if (!h) return hata(res, 401, 'Bu e-postayla kayıtlı hesap yok. Önce kayıt olun.', { kod: 'yok' });
    if (h.devre_disi) return hata(res, 403, 'Bu hesap devre dışı bırakılmış.');
    if (!h.sifre_ozeti) {
      return hata(res, 401, 'Giriş sistemimiz yenilendi. Hesabın ve tüm verilerin yerinde; yalnız bir kez "Şifremi unuttum / Şifre belirle" ile e-postana gelen kodla yeni şifreni belirlemen gerekiyor.', { kod: 'sifre-belirle' });
    }
    if (!(await sifreDogru(sifre, h.sifre_ozeti))) return hata(res, 401, 'E-posta ya da şifre hatalı.', { kod: 'hatali' });
    res.json(await oturumAc(h, req));
  });

  /* ---------------- yenileme ---------------- */
  app.post('/api/kimlik/yenile', async (req, res) => {
    if (!(await hazir(res))) return;
    const yenileme = String(req.body?.yenileme || '');
    if (!yenileme) return hata(res, 401, 'Oturum yok.', { kod: 'oturum-yok' });
    const id = sha(yenileme);
    const o = (await pgDb.query(
      `select o.uid, extract(epoch from o.giris_zamani)::bigint as giris, o.bitis > now() as gecerli, h.email, h.devre_disi
       from auth_oturumlar o join auth_hesaplar h on h.uid = o.uid where o.id = $1`, [id])).rows[0];
    if (!o || !o.gecerli || o.devre_disi) {
      if (o) void pgDb.query('delete from auth_oturumlar where id = $1', [id]).catch(() => {});
      return hata(res, 401, 'Oturumun süresi doldu. Lütfen tekrar giriş yapın.', { kod: 'oturum-yok' });
    }
    const iptal = oturumIptalZamani(o.uid);
    if (iptal && Number(o.giris) * 1000 < iptal) {
      void pgDb.query('delete from auth_oturumlar where id = $1', [id]).catch(() => {});
      return hata(res, 401, 'Oturumun sonlandırıldı. Lütfen tekrar giriş yapın.', { kod: 'oturum-yok' });
    }
    void pgDb.query('update auth_oturumlar set son_kullanim = now() where id = $1', [id]).catch(() => {});
    const h = (await hesapUid(o.uid))!;
    const e = erisimJetonuUret({ uid: o.uid, email: o.email, authTime: Number(o.giris) });
    res.json({ ok: true, token: e.token, exp: e.exp, user: disHesap(h) });
  });

  app.post('/api/kimlik/cikis', async (req, res) => {
    const yenileme = String(req.body?.yenileme || '');
    if (yenileme && (await semaKur())) await pgDb.query('delete from auth_oturumlar where id = $1', [sha(yenileme)]).catch(() => {});
    res.json({ ok: true });
  });

  /* ---------------- e-posta kodu ---------------- */
  app.post('/api/kimlik/kod-gonder', async (req, res) => {
    if (!(await hazir(res))) return;
    const email = lc(req.body?.email);
    const amac = req.body?.amac === 'giris' ? 'giris' : 'sifre';
    if (!EPOSTA.test(email)) return hata(res, 400, 'Geçerli bir e-posta adresi yazın.');
    if (sinirAsildi(`kod:${email}`, 1, 60_000)) return hata(res, 429, 'Yeni kod için bir dakika bekleyin.');
    if (sinirAsildi(`kod-saat:${email}`, 6, 60 * 60_000) || sinirAsildi(`kod-ip:${ipOf(req)}`, 20, 60 * 60_000)) {
      return hata(res, 429, 'Çok fazla kod istendi. Biraz sonra tekrar deneyin.');
    }
    const h = await hesapEposta(email);
    // Hesap yoksa da aynı yanıt (e-posta taraması yapılamasın); kod yalnız var olan hesaba gider.
    if (h && !h.devre_disi) {
      const kod = String(crypto.randomInt(0, 1_000_000)).padStart(6, '0');
      await pgDb.query(
        `insert into auth_kodlar (email, amac, kod_ozeti, deneme, bitis) values ($1, $2, $3, 0, now() + interval '${KOD_OMRU_DK} minutes')
         on conflict (email, amac) do update set kod_ozeti = excluded.kod_ozeti, deneme = 0, bitis = excluded.bitis, olusturma = now()`,
        [email, amac, sha(`${email}|${amac}|${kod}`)]);
      const baslik = amac === 'giris' ? 'MeDSor giriş kodun' : 'MeDSor şifre belirleme kodun';
      const ne = amac === 'giris' ? 'giriş yapmak' : 'şifreni belirlemek';
      const metin = `Merhaba,\n\nMeDSor'da ${ne} için kodun: ${kod}\n\nKod ${KOD_OMRU_DK} dakika geçerlidir. Bu isteği sen yapmadıysan bu e-postayı yok sayabilirsin.\n\nMeDSor`;
      const html = `<div style="font-family:system-ui,sans-serif;font-size:15px;color:#1a1a1a"><p>Merhaba,</p><p>MeDSor'da ${ne} için kodun:</p><p style="font-size:30px;font-weight:700;letter-spacing:6px">${kod}</p><p>Kod ${KOD_OMRU_DK} dakika geçerlidir. Bu isteği sen yapmadıysan bu e-postayı yok sayabilirsin.</p><p>MeDSor</p></div>`;
      const gitti = await d.epostaGonder(email, baslik, html, metin).catch(() => false);
      if (!gitti) {
        console.warn('[Kimlik] kod e-postası gönderilemedi:', email.replace(/^(.).*@/, '$1***@'));
        return hata(res, 503, 'Kod e-postası şu an gönderilemedi. Yöneticiden şifre belirleme kodu isteyebilirsin.', { kod: 'eposta-yok' });
      }
    }
    res.json({ ok: true, mesaj: 'Bu e-postayla bir hesap varsa 6 haneli kod gönderildi. Gelen kutunu (ve gereksiz klasörünü) kontrol et.' });
  });

  app.post('/api/kimlik/kod-dogrula', async (req, res) => {
    if (!(await hazir(res))) return;
    const email = lc(req.body?.email);
    const amac = req.body?.amac === 'giris' ? 'giris' : 'sifre';
    const kod = String(req.body?.kod || '').replace(/\D/g, '');
    const yeniSifre = String(req.body?.yeniSifre || '');
    if (!EPOSTA.test(email) || kod.length !== 6) return hata(res, 400, 'E-posta ve 6 haneli kodu yazın.');
    if (amac === 'sifre' && !sifreGecerli(yeniSifre)) return hata(res, 400, 'Yeni şifre en az 6 karakter olmalı.');
    const k = (await pgDb.query(
      'select kod_ozeti, deneme, bitis > now() as gecerli from auth_kodlar where email = $1 and amac = $2', [email, amac])).rows[0];
    if (!k || !k.gecerli) return hata(res, 400, 'Kodun süresi dolmuş ya da kod istenmemiş. Yeni kod iste.');
    if (k.deneme >= 5) return hata(res, 429, 'Çok fazla hatalı deneme. Yeni kod iste.');
    const dogru = crypto.timingSafeEqual(Buffer.from(sha(`${email}|${amac}|${kod}`)), Buffer.from(String(k.kod_ozeti)));
    if (!dogru) {
      await pgDb.query('update auth_kodlar set deneme = deneme + 1 where email = $1 and amac = $2', [email, amac]);
      return hata(res, 400, 'Kod hatalı.');
    }
    await pgDb.query('delete from auth_kodlar where email = $1 and amac = $2', [email, amac]);
    const h = await hesapEposta(email);
    if (!h || h.devre_disi) return hata(res, 400, 'Hesap bulunamadı.');
    if (amac === 'sifre') {
      await pgDb.query(
        'update auth_hesaplar set sifre_ozeti = $2, eposta_dogrulandi = true, guncelleme = now() where uid = $1',
        [h.uid, await sifreOzeti(yeniSifre)]);
    } else {
      await pgDb.query('update auth_hesaplar set eposta_dogrulandi = true where uid = $1', [h.uid]);
    }
    res.json(await oturumAc((await hesapUid(h.uid))!, req));
  });

  /* ---------------- oturumdaki hesap ---------------- */
  const benKim = (req: express.Request) => {
    const u = erisimJetonuDogrula(bearerToken(req));
    if (!u) return null;
    const iptal = oturumIptalZamani(u.uid);
    return iptal ? null : u;
  };

  app.get('/api/kimlik/ben', async (req, res) => {
    if (!(await hazir(res))) return;
    const u = benKim(req);
    if (!u) return hata(res, 401, 'Oturum yok.', { kod: 'oturum-yok' });
    const h = await hesapUid(u.uid);
    if (!h) return hata(res, 401, 'Hesap bulunamadı.', { kod: 'oturum-yok' });
    res.json({ ok: true, user: disHesap(h) });
  });

  app.post('/api/kimlik/sifre', async (req, res) => {
    if (!(await hazir(res))) return;
    const u = benKim(req);
    if (!u) return hata(res, 401, 'Şifre belirlemek için önce giriş yapmalısınız.');
    const yeni = String(req.body?.yeniSifre || '');
    if (!sifreGecerli(yeni)) return hata(res, 400, 'Şifreniz en az 6 karakter olmalıdır.');
    await pgDb.query('update auth_hesaplar set sifre_ozeti = $2, guncelleme = now() where uid = $1', [u.uid, await sifreOzeti(yeni)]);
    res.json({ ok: true });
  });

  app.post('/api/kimlik/profil', async (req, res) => {
    if (!(await hazir(res))) return;
    const u = benKim(req);
    if (!u) return hata(res, 401, 'Oturum yok.');
    const ad = req.body?.ad !== undefined ? String(req.body.ad || '').trim().slice(0, 80) || null : undefined;
    const foto = req.body?.foto !== undefined ? (req.body.foto ? String(req.body.foto) : null) : undefined;
    if (foto && foto.length > 200_000) return hata(res, 413, 'Fotoğraf çok büyük.');
    if (ad !== undefined) await pgDb.query('update auth_hesaplar set ad = $2, guncelleme = now() where uid = $1', [u.uid, ad]);
    if (foto !== undefined) await pgDb.query('update auth_hesaplar set foto = $2, guncelleme = now() where uid = $1', [u.uid, foto]);
    res.json({ ok: true });
  });

  /* ---------------- yönetici ---------------- */
  app.get('/api/admin/kimlik/hesaplar', async (req, res) => {
    if (!d.isAdmin(req)) return hata(res, 403, 'Yetkisiz.');
    if (!(await hazir(res))) return;
    const r = await pgDb.query(
      `select h.uid, h.email, h.ad, h.kaynak, h.devre_disi, h.eposta_dogrulandi, h.sifre_ozeti is not null as sifre_var,
              h.olusturma, h.son_giris, (select count(*) from auth_oturumlar o where o.uid = h.uid and o.bitis > now())::int as oturum
       from auth_hesaplar h order by h.son_giris desc nulls last, h.olusturma desc`);
    res.json({ ok: true, hesaplar: r.rows });
  });

  app.post('/api/admin/kimlik/sifirlama-kodu', async (req, res) => {
    if (!d.isAdmin(req)) return hata(res, 403, 'Yetkisiz.');
    if (!(await hazir(res))) return;
    const email = lc(req.body?.email);
    const h = await hesapEposta(email);
    if (!h) return hata(res, 404, 'Bu e-postayla hesap yok.');
    const kod = String(crypto.randomInt(0, 1_000_000)).padStart(6, '0');
    await pgDb.query(
      `insert into auth_kodlar (email, amac, kod_ozeti, deneme, bitis) values ($1, 'sifre', $2, 0, now() + interval '24 hours')
       on conflict (email, amac) do update set kod_ozeti = excluded.kod_ozeti, deneme = 0, bitis = excluded.bitis, olusturma = now()`,
      [email, sha(`${email}|sifre|${kod}`)]);
    // Kod yalnız yöneticiye döner; öğrenciye yönetici kendi kanalından iletir (24 saat geçerli).
    res.json({ ok: true, email, kod, gecerlilik: '24 saat' });
  });

  app.post('/api/admin/kimlik/oturumlari-kapat', async (req, res) => {
    if (!d.isAdmin(req)) return hata(res, 403, 'Yetkisiz.');
    if (!(await hazir(res))) return;
    const uid = String(req.body?.uid || '');
    const r = await pgDb.query('delete from auth_oturumlar where uid = $1', [uid]);
    res.json({ ok: true, silinen: r.rowCount });
  });

  // Süresi geçmiş oturum/kod temizliği (günde bir; LLM yok)
  setInterval(() => {
    if (!sema) return;
    void pgDb.query('delete from auth_oturumlar where bitis < now()').catch(() => {});
    void pgDb.query('delete from auth_kodlar where bitis < now()').catch(() => {});
  }, 24 * 60 * 60_000).unref?.();
}

export { ERISIM_OMRU_SN };
