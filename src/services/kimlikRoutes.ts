/**
 * Evrensel kimlik çözücü (GELECEK_PLANLAMASI §5): her kimlikli veri tek adresten bulunur.
 *   GET /api/k/:id → {id, tur, baslik, metin, yol, ust?}   (yol = ön yüzde gidilecek adres; #kimlik ile o öğeye kaydırılır)
 *
 * Desteklenen kimlikler:
 *   k2-07-c0142 / -p012 / -b03 → sesli ders cümlesi / paragrafı / bölümü (data/sesli_anlatim/v2/<anahtar>.json)
 *   k1-os-037                  → olası soru (data/olasi_sorular/k1.json)
 *   k2-07                      → ders kayıt defteri (src/data/dersler/k2.json)
 * Yeni bir kimlik türü eklemek = aşağıdaki COZUCULER listesine bir giriş.
 */
import fs from 'fs';
import path from 'path';
import type { Express, Request, Response } from 'express';

interface Sonuc { id: string; tur: string; baslik: string; metin?: string; yol: string; ust?: Record<string, string> }

export function registerKimlikRoutes(app: Express, opts: { rootDir: string }) {
  const V2 = path.join(opts.rootDir, 'data', 'sesli_anlatim', 'v2');
  let v2Dizin: { mtime: number; dosya: Map<string, string> } | null = null;

  /** ders kimliği (k1-03) → v2 dosyası; klasör değişince yenilenir. */
  const v2Dosya = (ders: string): string | null => {
    let mtime = 0;
    try { mtime = fs.statSync(V2).mtimeMs; } catch { return null; }
    if (!v2Dizin || v2Dizin.mtime !== mtime) {
      const dosya = new Map<string, string>();
      for (const f of fs.readdirSync(V2)) {
        const m = /^(k\d-\d{2})/.exec(f);
        if (m && f.endsWith('.json')) dosya.set(m[1], path.join(V2, f));
      }
      v2Dizin = { mtime, dosya };
    }
    return v2Dizin.dosya.get(ders) || null;
  };

  const oku = (p: string) => { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return null; } };

  const COZUCULER: Array<[RegExp, (m: RegExpExecArray) => Sonuc | null]> = [
    [/^(k\d-\d{2})-([bpc])(\d{2,4})$/, (m) => {
      const f = v2Dosya(m[1]);
      const d = f && oku(f);
      if (!d) return null;
      const id = m[0];
      for (const b of d.bolumler || []) {
        const yol = `/canliders/${encodeURIComponent(d.anahtar || m[1])}#${id}`;
        const ust = { ders: d.ders_id, dersBaslik: d.baslik, bolum: b.baslik };
        if (b.id === id) return { id, tur: 'sesli_bolum', baslik: b.baslik, yol, ust };
        for (const p of b.paragraflar || []) {
          if (p.id === id) return { id, tur: 'sesli_paragraf', baslik: b.baslik, metin: (p.cumleler || []).map((c: any) => c.ekran).join(' '), yol, ust: { ...ust, sayfa: String(p.sayfa ?? '') } };
          for (const c of p.cumleler || []) {
            if (c.id === id) return { id, tur: 'sesli_cumle', baslik: b.baslik, metin: c.ekran, yol, ust: { ...ust, sayfa: String(p.sayfa ?? ''), ses: c.ses } };
          }
        }
      }
      return null;
    }],
    [/^k(\d)-os-(\d{3}|s-[\w-]{6})$/, (m) => {
      const d = oku(path.join(opts.rootDir, 'data', 'olasi_sorular', `k${m[1]}.json`));
      const s = (d?.sorular || []).find((x: any) => x.id === m[0]);
      return s ? { id: m[0], tur: 'olasi_soru', baslik: `Kurul ${m[1]} · ${s.yuva}. soru`, metin: s.kok, yol: `/olasi-sorular?kurul=${m[1]}#${m[0]}` } : null;
    }],
    [/^k(\d)-(\d{2})$/, (m) => {
      const d = oku(path.join(opts.rootDir, 'src', 'data', 'dersler', `k${m[1]}.json`));
      const x = (d?.dersler || []).find((y: any) => y.id === m[0]);
      return x ? { id: m[0], tur: 'ders', baslik: x.konu, metin: `${x.brans} · ${x.ogretim_uyesi || ''} · ${x.tarih || ''}`.trim(), yol: `/ogren?ders=${m[0]}` } : null;
    }],
  ];

  app.get('/api/k/:id', (req: Request, res: Response) => {
    const id = String(req.params.id || '').trim().toLowerCase();
    if (!/^[a-z0-9-]{3,40}$/.test(id)) return res.status(400).json({ error: 'geçersiz kimlik' });
    for (const [re, coz] of COZUCULER) {
      const m = re.exec(id);
      if (!m) continue;
      const s = coz(m);
      if (s) { res.set('Cache-Control', 'public, max-age=120'); return res.json(s); }
    }
    res.status(404).json({ error: 'Bu kimlikle kayıt bulunamadı.', id });
  });
}
