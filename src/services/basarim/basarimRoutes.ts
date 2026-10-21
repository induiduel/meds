/**
 * Başarım uçları + topluluk eylemi ara katmanı (2026-10-20). Motor: ./basarimMotor.ts, kurallar: src/data/basarim/tanim.json.
 *
 *   GET  /api/basarim/tanim                 kurallar (herkese açık; hedef/başarım/kilit listeleri)
 *   GET  /api/basarim/durum                 giriş kaydı + değerlendirme + özet (Firebase jetonu zorunlu)
 *   POST /api/basarim/profil {donem,kurul}  dönem/kurul (girişte bir kez sorulur, ayarlardan değişir)
 *   POST /api/basarim/goruldu {at}          kutlaması gösterilen ödüller
 *   POST /api/basarim/satin-al {id}         ATP ile kilit açma
 *   POST /api/basarim/sec {tur,id}          unvan/çerçeve/efekt seçimi
 *   GET  /api/basarim/siralama?kapsam=hafta|kurul|tum&donem=3
 *   PUT  /api/admin/basarim/tanim           kuralları güncelle (doğrulayıcı geçmezse 400)
 *
 * Ara katman: başarılı (2xx) topluluk isteklerinde doğrulanmış kullanıcıya eylem yazar (yalnız puan). Kimliksiz istek
 * sayılmaz. Beğeni yalnız açılınca (yanıtta liked !== false) ve hedef başına bir kez.
 */
import type express from 'express';
import { requestUser } from '../firebaseIdentity';
import type { BasarimMotor } from './basarimMotor';

const KURALLAR: { m: string; re: RegExp; tur: (body: any, status: number, req: express.Request) => string | null; tekil?: boolean }[] = [
  { m: 'POST', re: /^\/api\/questions$/, tur: (b, s, req) => (s === 201 || b?.isNew ? 'soru_ekle' : req.body?.fragmentText ? 'parca' : null) },
  { m: 'POST', re: /^\/api\/question-intake$/, tur: () => 'soru_ekle' },
  { m: 'POST', re: /^\/api\/questions\/[^/]+\/fragments$/, tur: () => 'parca' },
  { m: 'POST', re: /^\/api\/questions\/[^/]+\/options$/, tur: () => 'sik' },
  { m: 'POST', re: /^\/api\/past-exams\/[^/]+\/comment$/, tur: () => 'yorum' },
  { m: 'POST', re: /^\/api\/learn\/social\/threads(\/[^/]+\/messages)?$/, tur: () => 'yorum' },
  { m: 'POST', re: /^\/api\/(questions\/[^/]+(\/(fragments|options)\/[^/]+)?\/upvote|past-exams\/[^/]+\/upvote|learn\/feedback\/[^/]+\/vote)$/, tur: (b) => (b?.liked === false ? null : 'begeni'), tekil: true },
  { m: 'POST', re: /^\/api\/(questions|past-exams|ornek-sorular|terms|cards)\/[^/]+\/report$/, tur: () => 'hata' },
  { m: 'POST', re: /^\/api\/(universal-report|learn\/feedback)$/, tur: () => 'hata' },
];

export const AI_TEST_UID = 'ai-test';

export function registerBasarimRoutes(app: express.Express, motor: BasarimMotor, opts: { requireAdmin: express.RequestHandler; onDegisti?: (uid: string) => void; aiTestGecerli?: (req: express.Request) => boolean }) {
  /** Doğrulanmış öğrenci; yapay zekâ test oturumu ayrı kimlikle (sıralamaya ve ödemelere girmez). */
  const kim = async (req: express.Request): Promise<{ uid: string; email: string } | null> =>
    (await requestUser(req)).user || (opts.aiTestGecerli?.(req) ? { uid: AI_TEST_UID, email: '' } : null);

  // Ara katman: express.json'dan sonra, rotalardan önce kurulmalı
  app.use((req, res, next) => {
    const kural = KURALLAR.find((k) => k.m === req.method && k.re.test(req.path));
    if (!kural || !String(req.headers.authorization || '').toLowerCase().startsWith('bearer ')) return next(); // test oturumu eylem toplamaz
    let govde: any = null;
    const json = res.json.bind(res);
    res.json = (b: any) => { govde = b; return json(b); };
    res.on('finish', () => {
      if (res.statusCode >= 300) return;
      const tur = kural.tur(govde, res.statusCode, req);
      if (!tur) return;
      void kim(req).then((u) => {
        if (!u) return;
        motor.eylem(u.uid, tur, kural.tekil ? `${req.path}` : undefined);
        opts.onDegisti?.(u.uid);
      }).catch(() => 0);
    });
    next();
  });

  app.get('/api/basarim/tanim', (_req, res) => { res.set('Cache-Control', 'no-cache'); res.json(motor.tanim()); });

  const korumali = (f: (req: express.Request, res: express.Response, uid: string, ad: string) => void) => async (req: express.Request, res: express.Response) => {
    const u = await kim(req);
    if (!u) return res.status(401).json({ error: 'Giriş gerekli.' });
    try { f(req, res, u.uid, String((u as any).name || u.email?.split('@')[0] || '')); } catch (e: any) { res.status(500).json({ error: e?.message || 'Hata' }); }
  };

  app.get('/api/basarim/durum', korumali((req, res, uid) => {
    res.set('Cache-Control', 'no-store');
    res.json(motor.durum(uid, String(req.query.ad || '')));
  }));
  app.post('/api/basarim/profil', korumali((req, res, uid) => {
    const donem = Number(req.body?.donem), kurul = Number(req.body?.kurul);
    if (!(donem >= 1 && donem <= 6) || !(kurul >= 1 && kurul <= 10)) return res.status(400).json({ error: 'Dönem 1–6, kurul 1–10 olmalı.' });
    motor.profil(uid, donem, kurul, String(req.body?.ad || ''));
    res.json(motor.ozet(motor.kisi(uid)));
  }));
  app.post('/api/basarim/goruldu', korumali((req, res, uid) => { motor.goruldu(uid, String(req.body?.at || '')); res.json({ ok: true }); }));
  app.post('/api/basarim/satin-al', korumali((req, res, uid) => {
    const r = motor.satinAl(uid, String(req.body?.id || ''));
    if ('hata' in r) return res.status(400).json({ error: r.hata });
    opts.onDegisti?.(uid);
    res.json(motor.ozet(motor.kisi(uid)));
  }));
  app.post('/api/basarim/sec', korumali((req, res, uid) => {
    const tur = req.body?.tur;
    if (!['unvan', 'cerceve', 'efekt'].includes(tur)) return res.status(400).json({ error: 'Geçersiz tür.' });
    if (!motor.sec(uid, tur, req.body?.id || null)) return res.status(400).json({ error: 'Bu kilit açık değil.' });
    res.json(motor.ozet(motor.kisi(uid)));
  }));
  app.get('/api/basarim/siralama', async (req, res) => {
    const u = await kim(req);
    const kapsam = (['hafta', 'kurul', 'tum'].includes(String(req.query.kapsam)) ? req.query.kapsam : 'hafta') as 'hafta' | 'kurul' | 'tum';
    const donem = Number(req.query.donem) || (u ? motor.kisi(u.uid).donem : null) || 3;
    res.set('Cache-Control', 'no-store');
    res.json({ donem, ...motor.siralamaListesi(u?.uid || null, donem, kapsam) });
  });
  // Aynı kişinin ikinci hesabını sıralamadan çıkar: {kaynak, hedef} (hedef null → geri al)
  app.post('/api/admin/basarim/birlestir', opts.requireAdmin, (req, res) => {
    const kaynak = String(req.body?.kaynak || ''), hedef = req.body?.hedef ? String(req.body.hedef) : null;
    if (!kaynak || kaynak === hedef) return res.status(400).json({ error: 'kaynak ve hedef farklı uid olmalı.' });
    motor.birlestir(kaynak, hedef);
    opts.onDegisti?.(kaynak);
    res.json({ ok: true });
  });
  app.put('/api/admin/basarim/tanim', opts.requireAdmin, (req, res) => {
    const h = motor.tanimYaz(req.body);
    if (h.length) return res.status(400).json({ error: 'Tanım geçersiz', hatalar: h });
    res.json({ ok: true, tanim: motor.tanim() });
  });
}
