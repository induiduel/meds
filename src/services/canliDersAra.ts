// Sesli derste geçen yerler (tasarım A05): GET /api/canli-ders/ara?q=<terim>&n=<en çok>
// Sesi olan derslerin metnini (metin/<key>.md) cümlelere böler, cümle başlangıç saniyesini cumle_zaman/<key>.json'dan
// (metinHash tutuyorsa, EMA varyantı öncelikli) alır. Dizin bellekte, ilk istekte kurulur, 10 dk sonra tazelenir.
// İstemciye büyük dosya gitmez: yanıt yalnız eşleşen cümle parçalarıdır.
import type { Express, Request, Response } from 'express';
import fs from 'fs';
import crypto from 'crypto';
import { metinParagraflari } from './sesliAnlatim';

export interface AraBagim {
  dersler: () => { key: string; baslik: string }[];
  metinYolu: (k: string) => string;
  cumleYolu: (k: string) => string;
  sesVar: (k: string) => boolean;
}
interface Cumle { k: string; p: number; c: number; t: number | null; m: string; n: string }
interface Dizin { at: number; cumleler: Cumle[]; baslik: Map<string, string> }

/** Arama için düzleştirme: Türkçe küçük harf, aksan/işaret yok, tek boşluk. */
export const duzle = (s: string) => s.toLocaleLowerCase('tr-TR')
  .replace(/[ıi̇]/g, 'i').replace(/ş/g, 's').replace(/ğ/g, 'g').replace(/ü/g, 'u').replace(/ö/g, 'o').replace(/ç/g, 'c')
  .replace(/[âà]/g, 'a').replace(/[îì]/g, 'i').replace(/[ûù]/g, 'u')
  .replace(/[^\p{L}\p{N}]+/gu, ' ').trim();

/** canliDersStore.ts::cumleSinirlari ile aynı kural (cümle dizini zamanlamayla birebir eşleşmeli). */
export function cumleBol(metin: string): string[] {
  const son: number[] = [];
  const re = /[.!?…]+["'”’)\]]*(?:\s+|$)/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(metin))) {
    if (!m[0]) { re.lastIndex++; continue; }
    const e = m.index + m[0].length;
    const s = metin.charAt(e);
    if (s && s !== s.toLocaleUpperCase('tr') && s === s.toLocaleLowerCase('tr')) continue;
    if (e > (son[son.length - 1] || 0)) son.push(e);
    if (re.lastIndex >= metin.length) break;
  }
  if (!son.length || son[son.length - 1] < metin.length) son.push(metin.length);
  return son.map((e, i) => metin.slice(i ? son[i - 1] : 0, e).trim());
}

let dizin: Dizin | null = null;
function dizinKur(b: AraBagim): Dizin {
  const cumleler: Cumle[] = [];
  const baslik = new Map<string, string>();
  for (const d of b.dersler()) {
    try {
      if (!b.sesVar(d.key) || !fs.existsSync(b.metinYolu(d.key))) continue;
      const pars = metinParagraflari(fs.readFileSync(b.metinYolu(d.key), 'utf8'));
      const h = crypto.createHash('sha1').update(pars.map((x) => x.t).join('\n')).digest('hex');
      let vz: any = null;
      try {
        const cz = JSON.parse(fs.readFileSync(b.cumleYolu(d.key), 'utf8'));
        if (cz?.metinHash === h && cz.varyantlar) {
          const e = Object.entries<any>(cz.varyantlar);
          vz = (e.find(([v]) => /ema/i.test(v)) || e[0])?.[1] || null;
        }
      } catch { /* zamanlama yok: yalnız paragraf */ }
      baslik.set(d.key, d.baslik);
      pars.forEach((p, pi) => cumleBol(p.t).forEach((m, ci) => {
        if (!m) return;
        const t = vz?.p?.[String(pi)]?.[ci];
        cumleler.push({ k: d.key, p: pi, c: ci, t: Number.isFinite(t) ? Math.floor(t) : null, m, n: ` ${duzle(m)} ` });
      }));
    } catch { /* bozuk ders atlanır */ }
  }
  return { at: Date.now(), cumleler, baslik };
}

/** Eşleşen yerin çevresinden ~140 karakterlik parça (ham metinde düzleştirilmiş konumla yaklaşık). */
function parca(m: string, terim: string): string {
  const d = duzle(m);
  const i = d.indexOf(terim);
  if (m.length <= 150 || i < 0) return m.length <= 150 ? m : `${m.slice(0, 147)}…`;
  const oran = m.length / Math.max(1, d.length);
  const bas = Math.max(0, Math.floor(i * oran) - 50);
  const s = m.slice(bas, bas + 150);
  return `${bas > 0 ? '…' : ''}${s}${bas + 150 < m.length ? '…' : ''}`;
}

export function canliDersAra(b: AraBagim, q: string, n = 20) {
  const terim = duzle(q);
  if (terim.length < 3) return [];
  if (!dizin || Date.now() - dizin.at > 600_000) dizin = dizinKur(b);
  const kelimeler = terim.split(' ');
  const out: { k: string; b: string; p: number; c: number; t: number | null; parca: string }[] = [];
  const dersSay = new Map<string, number>();
  // önce tam ifade (kelime başından), sonra tüm kelimeler; ders başına en çok 3 yer
  const tam = ` ${terim}`;
  const gecis = [(c: Cumle) => c.n.includes(tam), (c: Cumle) => kelimeler.length > 1 && kelimeler.every((w) => c.n.includes(` ${w}`))];
  const goruldu = new Set<Cumle>();
  for (const f of gecis) {
    for (const c of dizin.cumleler) {
      if (out.length >= n) break;
      if (goruldu.has(c) || !f(c) || (dersSay.get(c.k) || 0) >= 3) continue;
      goruldu.add(c);
      dersSay.set(c.k, (dersSay.get(c.k) || 0) + 1);
      out.push({ k: c.k, b: dizin.baslik.get(c.k) || c.k, p: c.p, c: c.c, t: c.t, parca: parca(c.m, kelimeler[0]) });
    }
  }
  return out;
}

/** registerCanliDersRoutes içinde /api/canli-ders/:key'den ÖNCE çağrılır. */
export function registerCanliDersAra(app: Express, b: AraBagim) {
  app.get('/api/canli-ders/ara', (req: Request, res: Response) => {
    const q = String(req.query.q || '').slice(0, 80);
    const n = Math.min(40, Math.max(1, Number(req.query.n) || 20));
    res.setHeader('Cache-Control', 'public, max-age=300');
    res.json({ q, sonuc: canliDersAra(b, q, n) });
  });
}
