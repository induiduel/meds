/**
 * Yönetim v16 › Oyunlar (server-only, 2026-10-28).
 *  - GET    /api/admin/quiz/odalar          RAM'deki canlı odalar + oyuncular
 *  - DELETE /api/admin/quiz/odalar/:id      odayı kapat (oyunculara bildirilir)
 *  - GET    /api/admin/quiz/kaynaklar       tüm oyun soru kaynakları + açık/kapalı (bayrak oyun_kaynak_<brans>)
 *  - GET    /api/admin/quiz/modlar          oyun modları ve bayrak durumları
 * Aç/kapa yazımı site ayarı üzerinden: PUT /api/admin/site-ayar {bayraklar:{oyun_kaynak_<b>|oyun_mod_<m>: bool|null}}
 */
import type express from 'express';
import { oyunKaynaklari } from '../quiz/oyunSoruKaynagi';
import { bayrakAcik } from './siteAyar.ts';
import { denetimHedef } from './denetim.ts';

/** İstemci OyunlarV15 MODLAR kimlikleri ile aynı; bayrak `oyun_mod_<id>` */
export const OYUN_MODLARI: { id: string; ad: string; sunucu?: boolean }[] = [
  { id: 'canli', ad: 'Canlı yarışma', sunucu: true },
  { id: 'takim', ad: 'Takım modu', sunucu: true },
  { id: 'katil', ad: 'Kodla katıl' },
  { id: 'blitz', ad: 'Blitz' },
  { id: 'hayatta', ad: 'Hayatta kal' },
  { id: 'gorsel', ad: 'Görselli soru' },
  { id: 'kaydir', ad: 'Kaydır' },
  { id: 'sirala', ad: 'Sırala' },
  { id: 'izgara', ad: 'Izgara' },
  { id: 'eslestir', ad: 'Eşleştir' },
  { id: 'bosluk', ad: 'Boşluk doldur' },
];

type QuizYonetim = { odaListesi: () => any[]; odaKapat: (id: string, neden?: string) => boolean };

export function registerOyunYonetimRoutes(app: express.Express, d: { requireAdmin: express.RequestHandler; quiz: QuizYonetim }) {
  app.get('/api/admin/quiz/odalar', d.requireAdmin, (_req, res) => {
    const odalar = d.quiz.odaListesi();
    res.json({ ogeler: odalar, toplam: odalar.length, oyunlarAcik: bayrakAcik('oyunlar') });
  });

  app.delete('/api/admin/quiz/odalar/:id', d.requireAdmin, (req, res) => {
    const id = String(req.params.id).slice(0, 40);
    denetimHedef(res, `quiz-oda:${id}`);
    if (!d.quiz.odaKapat(id)) return res.status(404).json({ error: 'Oda bulunamadı (oyun bitmiş olabilir).' });
    res.json({ ok: true });
  });

  app.get('/api/admin/quiz/kaynaklar', d.requireAdmin, (_req, res) => {
    try {
      const k = oyunKaynaklari(true);
      res.json({ ogeler: k, toplam: k.length });
    } catch (e: any) {
      res.status(500).json({ error: e?.message || 'Kaynaklar okunamadı' });
    }
  });

  app.get('/api/admin/quiz/modlar', d.requireAdmin, (_req, res) => {
    res.json({ ogeler: OYUN_MODLARI.map((m) => ({ ...m, acik: bayrakAcik(`oyun_mod_${m.id}`) })), oyunlarAcik: bayrakAcik('oyunlar') });
  });
}
