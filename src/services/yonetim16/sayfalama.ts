/**
 * Yönetim v16 — ortak sayfalama/süzgeç yardımcısı (server-only).
 * Her liste ucu aynı yanıtı döner: { ogeler, toplam, sayfa, boyut, yuzler? }.
 * Sorgu parametreleri: ?sayfa=0&boyut=50&q=&sirala=alan&yon=artan|azalan&s.<alan>=<değer> (süzgeç çipleri)
 */
import type express from 'express';

export type ListeSorgusu = {
  sayfa: number;
  boyut: number;
  q: string;
  sirala: string;
  yon: 'artan' | 'azalan';
  suzgec: Record<string, string>;
};
export type ListeYaniti<T> = { ogeler: T[]; toplam: number; sayfa: number; boyut: number; yuzler?: Record<string, { deger: string; n: number }[]> };

export const katla = (s: string) => String(s ?? '').toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');

export function listeSorgusu(req: express.Request, o: { varsayilanBoyut?: number; enFazla?: number } = {}): ListeSorgusu {
  const q: any = req.query || {};
  const enFazla = o.enFazla ?? 500;
  const boyut = Math.min(enFazla, Math.max(1, Number(q.boyut) || o.varsayilanBoyut || 50));
  const suzgec: Record<string, string> = {};
  for (const [k, v] of Object.entries(q)) if (k.startsWith('s.') && String(v)) suzgec[k.slice(2)] = String(v);
  return {
    sayfa: Math.max(0, Math.floor(Number(q.sayfa) || 0)),
    boyut,
    q: String(q.q || '').trim().slice(0, 200),
    sirala: String(q.sirala || '').replace(/[^\w.-]/g, '').slice(0, 60),
    yon: q.yon === 'artan' ? 'artan' : 'azalan',
    suzgec,
  };
}

/** Bellekteki dizi (JSON dosyası) için sayfalama + arama + süzgeç + yüz sayıları */
export function diziSayfala<T>(
  items: T[],
  s: ListeSorgusu,
  o: {
    araMetni?: (t: T) => string;
    siralayicilar?: Record<string, (t: T) => string | number>;
    suzgecler?: Record<string, (t: T, deger: string) => boolean>;
    yuzler?: Record<string, (t: T) => string | string[] | undefined>;
    eslestir?: (t: T) => unknown;
  } = {},
): ListeYaniti<unknown> {
  let list = items;
  for (const [k, v] of Object.entries(s.suzgec)) {
    const f = o.suzgecler?.[k];
    if (f) list = list.filter((t) => f(t, v));
  }
  if (s.q && o.araMetni) {
    const terms = katla(s.q).split(/\s+/).filter(Boolean);
    list = list.filter((t) => { const m = katla(o.araMetni!(t)); return terms.every((x) => m.includes(x)); });
  }
  let yuzler: ListeYaniti<T>['yuzler'];
  if (o.yuzler) {
    yuzler = {};
    for (const [k, f] of Object.entries(o.yuzler)) {
      const m = new Map<string, number>();
      for (const t of list) { const v = f(t); for (const x of Array.isArray(v) ? v : v == null ? [] : [v]) m.set(x, (m.get(x) || 0) + 1); }
      yuzler[k] = [...m].map(([deger, n]) => ({ deger, n })).sort((a, b) => b.n - a.n).slice(0, 50);
    }
  }
  const sr = s.sirala && o.siralayicilar?.[s.sirala];
  if (sr) {
    const d = s.yon === 'artan' ? 1 : -1;
    list = [...list].sort((a, b) => { const x = sr(a), y = sr(b); return (x < y ? -1 : x > y ? 1 : 0) * d; });
  }
  const sayfaOgeleri = list.slice(s.sayfa * s.boyut, s.sayfa * s.boyut + s.boyut);
  return { ogeler: o.eslestir ? sayfaOgeleri.map(o.eslestir) : sayfaOgeleri, toplam: list.length, sayfa: s.sayfa, boyut: s.boyut, ...(yuzler ? { yuzler } : {}) };
}

/**
 * meds-pg tablosu için sayfalı sorgu kurar. Sütun adları yalnız izin listesinden gelir (SQL enjeksiyonu yok).
 * Dönüş: { veri: sql, sayim: sql, degerler } — iki sorguyu pgDb.query ile çalıştırın.
 */
export function pgSayfaSorgusu(s: ListeSorgusu, o: {
  tablo: string;
  sutunlar?: string;
  araSutunlari?: string[];
  siralanabilir: string[];
  varsayilanSira: string;
  suzgecSutunlari?: Record<string, string>;
  ekKosul?: string[];
}) {
  const where = [...(o.ekKosul || [])];
  const degerler: unknown[] = [];
  for (const [k, v] of Object.entries(s.suzgec)) {
    const col = o.suzgecSutunlari?.[k];
    if (!col) continue;
    degerler.push(v);
    where.push(`${col} = $${degerler.length}`);
  }
  if (s.q && o.araSutunlari?.length) {
    degerler.push(`%${s.q}%`);
    where.push(`(${o.araSutunlari.map((c) => `${c}::text ilike $${degerler.length}`).join(' or ')})`);
  }
  const w = where.length ? `where ${where.join(' and ')}` : '';
  const sira = o.siralanabilir.includes(s.sirala) ? s.sirala : o.varsayilanSira;
  return {
    veri: `select ${o.sutunlar || '*'} from ${o.tablo} ${w} order by ${sira} ${s.yon === 'artan' ? 'asc' : 'desc'} nulls last limit ${s.boyut} offset ${s.sayfa * s.boyut}`,
    sayim: `select count(*)::int n from ${o.tablo} ${w}`,
    degerler,
  };
}
