/**
 * Faz verisi gezgini (server-only): yönetim konsolundaki "Faz verileri" sekmesi için tüm türetilmiş veriyi
 * kategori kategori düz satırlara çevirir; arama yapmadan listelenir, her alan (anahtar) için sorgu yapılır.
 * Kaynaklar $MEDS_DATABASE_DIR/derived altındadır; dosyalar değişince (mtime) yeniden okunur.
 */
import fs from 'fs';
import path from 'path';
import { getPhaseOverride } from './phaseInsightsService';

type Row = Record<string, string | number | boolean | null>;

const dbDir = () => process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database');
const derived = (...p: string[]) => path.join(dbDir(), 'derived', ...p);

const fileCache = new Map<string, { mtime: number; data: any }>();
function readCached(file: string, parse: (raw: string) => any): any {
  try {
    const st = fs.statSync(file);
    const c = fileCache.get(file);
    if (c && c.mtime === st.mtimeMs) return c.data;
    const data = parse(fs.readFileSync(file, 'utf-8'));
    fileCache.set(file, { mtime: st.mtimeMs, data });
    return data;
  } catch {
    return null;
  }
}
const readJson = (f: string) => readCached(f, (r) => JSON.parse(r));
const readJsonl = (f: string) =>
  readCached(f, (r) =>
    r
      .split('\n')
      .filter((l) => l.trim())
      .map((l) => {
        try {
          return JSON.parse(l);
        } catch {
          return null;
        }
      })
      .filter(Boolean),
  );

const join = (v: any) => (Array.isArray(v) ? v.filter(Boolean).join(', ') : v == null ? null : String(v));

export type Category = { id: string; label: string; desc: string; build: () => Row[] };

function insights(): Record<string, any> {
  return readJson(derived('phase_insights', 'insights.json'))?.items || {};
}

export const CATEGORIES: Category[] = [
  {
    id: 'mufredat',
    label: 'Kazanım (Faz 8/9)',
    desc: 'Sorunun müfredat kazanımı; sınav başlığından kesin ya da Faz 8 yüksek güven',
    build: () =>
      Object.entries(insights()).flatMap(([id, it]) => {
        const m = it.mufredat || it.faz8;
        const k = m?.kazanimlar?.[0];
        return k ? [{ soru_id: id, kurul: k.kurul ?? null, ders: k.ders ?? null, konu: k.konu ?? null, kazanim: k.kazanim ?? null, guven: m.guven ?? null, kaynak: m.dogrulama ?? null }] : [];
      }),
  },
  {
    id: 'sinav_basligi',
    label: 'Kurul/ders düzeltmesi',
    desc: 'Sınav başlığından ya da Faz 8\'den çözülen içerik kurulu (sitedeki filtreyi belirler)',
    build: () =>
      Object.entries(readJson(derived('curriculum_links', 'soru_mufredat.json'))?.sorular || {}).map(([id, v]: [string, any]) => ({
        soru_id: id, kurul: v.kurul ?? null, ders: v.ders ?? null, konu: v.konu ?? null, kaynak: v.kaynak ?? null,
      })),
  },
  {
    id: 'slayt',
    label: 'Slayt eşleşmesi (Faz 11)',
    desc: 'Soru → ders slaytı; güven yüksek/orta yayınlanır',
    build: () =>
      Object.entries(insights()).flatMap(([id, it]) =>
        (it.slayt?.slaytlar || []).map((s: any, i: number) => ({
          soru_id: id, sira: i + 1, guven: it.slayt.guven ?? null, kaynak: s.kaynak ?? null, sayfa: s.sayfa ?? null, gerekce: join(s.gerekce),
        })),
      ),
  },
  {
    id: 'ogren',
    label: 'Öğren bağlantısı',
    desc: 'Soru → Öğren destesi slaytı (cross-encoder eşikli)',
    build: () =>
      Object.entries(readJson(derived('learn_links.json'))?.baglantilar || {}).map(([id, v]: [string, any]) => ({
        soru_id: id, deste: v.deckTitle ?? null, slayt_no: v.slideNumber ?? null, slayt: v.slideTitle ?? null, guven: v.guven ?? null, skor: v.skor ?? null,
      })),
  },
  {
    id: 'kisaltma',
    label: 'Kısaltma açılımı',
    desc: 'Soruda geçen kısaltmanın ders materyalinden açılımı',
    build: () =>
      Object.entries(insights()).flatMap(([id, it]) =>
        Object.entries(it.faz6_5?.kisaltmalar || {}).map(([k, v]) => ({ soru_id: id, kisaltma: k, acilim: String(v) })),
      ),
  },
  {
    id: 'terim',
    label: 'Terimler (Faz 5/6.5)',
    desc: 'Sorudaki tıbbi terimler ve eş anlamlılar',
    build: () =>
      Object.entries(insights()).flatMap(([id, it]) => {
        const t = [...(it.faz6_5?.terimler || []), ...(it.faz5?.terimler || [])];
        const es = Object.entries(it.faz6_5?.esanlamlilar || {}).map(([k, v]: [string, any]) => `${k} = ${join(v)}`);
        return t.length || es.length ? [{ soru_id: id, terimler: join(Array.from(new Set(t))), esanlamlilar: es.join('; ') || null, ders_faz5: it.faz5?.ders ?? null }] : [];
      }),
  },
  {
    id: 'varlik',
    label: 'Tıbbi varlıklar (Faz 13)',
    desc: 'GLiNER + terminoloji; kimlikli olanlar sitede görünür',
    build: () =>
      (readJsonl(derived('entities', 'soru_varliklar.jsonl')) || []).flatMap((r: any) =>
        (r.varliklar || []).map((v: any) => ({
          soru_id: r.soru_id, ad: v.ad ?? v.metin ?? null, metin: v.metin ?? null, tur: v.tur ?? null, kaynak: v.kaynak ?? null,
          kimlikli: Boolean(v.kavram), kavram: v.kavram ?? null, skor: v.gliner_skor ?? null,
        })),
      ),
  },
  {
    id: 'faz6',
    label: 'Ayırıcı tanı (Faz 6)',
    desc: 'Bulut modelinin ayırıcı tanı önerileri; doğrulama durumuyla',
    build: () =>
      Object.entries(insights()).flatMap(([id, it]) =>
        (it.faz6?.ayirici_tani || []).map((d: any) => ({
          soru_id: id, hastalik: d.hastalik ?? null, ozellik: d.ozellik ?? null, kaynak: it.faz6.kaynak ?? null, dogrulanmadi: Boolean(it.faz6.dogrulanmadi),
        })),
      ),
  },
  {
    id: 'karantina',
    label: 'Karantina',
    desc: 'Birleşik/bozuk sorular (okuma sırasında gizlenir)',
    build: () =>
      Object.entries(readJson(derived('quarantine', 'karantina.json'))?.sorular || {}).map(([id, v]: [string, any]) => ({
        soru_id: id, neden: join(v.neden), kaynak: v.kaynak ?? null, dosya: v.dosya ?? null,
      })),
  },
  {
    id: 'cevap',
    label: 'Cevap anahtarı (hakem)',
    desc: 'Sınav çıktısı soruları için kayıtlı cevabı görmeden hakemin verdiği cevap',
    build: () =>
      (readJsonl(derived('curriculum_links', 'cevap_anahtari.jsonl')) || []).map((r: any) => ({
        soru_id: r.soru_id, cevap: r.cevap ?? null, kayitli_cevap: r.kayitli_cevap ?? null, uyusuyor: r.cevap === r.kayitli_cevap, cevap_metni: r.cevap_metni ?? null, model: r.model ?? null,
      })),
  },
  {
    id: 'duzeltme',
    label: 'Elle düzeltmeler',
    desc: 'Bu konsoldan yapılan düzeltmeler',
    build: () =>
      Object.entries(readJson(derived('manual_overrides', 'faz_duzeltmeleri.json')) || {}).map(([id, v]: [string, any]) => ({
        soru_id: id, gizle: join(v.gizle), kazanim: v.kazanim ? [v.kazanim.ders, v.kazanim.konu].filter(Boolean).join(' · ') : null,
        slayt_sayisi: v.slaytlar?.length ?? 0, kisaltma_sayisi: Object.keys(v.kisaltmalar || {}).length, not: v.not ?? null, guncelleyen: v.guncelleyen ?? null, guncelleme: v.guncelleme ?? null,
      })),
  },
];

const rowCache = new Map<string, { at: number; rows: Row[] }>();
function rowsOf(cat: Category): Row[] {
  const c = rowCache.get(cat.id);
  if (c && Date.now() - c.at < 30_000) return c.rows;
  const rows = cat.build();
  rowCache.set(cat.id, { at: Date.now(), rows });
  return rows;
}

export function listCategories() {
  return CATEGORIES.map((c) => {
    const rows = rowsOf(c);
    return { id: c.id, label: c.label, desc: c.desc, satir: rows.length, soru: new Set(rows.map((r) => r.soru_id)).size, alanlar: rows[0] ? Object.keys(rows[0]) : [] };
  });
}

export type ExploreQuery = {
  kategori: string;
  alan?: string; // filtrelenecek anahtar ("" = tüm alanlarda ara)
  deger?: string; // içerir (büyük/küçük harf ve Türkçe katlama duyarsız); "=x" tam eşleşme; "boş" / "dolu"
  sirala?: string;
  yon?: 'artan' | 'azalan';
  sayfa?: number;
  boyut?: number;
};

const fold = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i');

export function explore(q: ExploreQuery, stemOf: (id: string) => string) {
  const cat = CATEGORIES.find((c) => c.id === q.kategori);
  if (!cat) return { hata: `bilinmeyen kategori: ${q.kategori}` };
  let rows = rowsOf(cat);
  const alanlar = rows[0] ? Object.keys(rows[0]) : [];
  const deger = (q.deger || '').trim();
  if (deger) {
    const keys = q.alan && alanlar.includes(q.alan) ? [q.alan] : alanlar;
    const exact = deger.startsWith('=');
    const want = fold(exact ? deger.slice(1) : deger);
    rows = rows.filter((r) =>
      keys.some((k) => {
        const v = r[k];
        if (want === 'bos') return v == null || v === '';
        if (want === 'dolu') return v != null && v !== '';
        const s = fold(String(v ?? ''));
        return exact ? s === want : s.includes(want);
      }),
    );
  }
  // Alan değer dağılımı (seçili alan için en sık 12 değer) — sorgu önerisi
  let dagilim: { deger: string; sayi: number }[] = [];
  if (q.alan && alanlar.includes(q.alan)) {
    const m = new Map<string, number>();
    for (const r of rows) {
      const v = String(r[q.alan] ?? '(boş)');
      m.set(v, (m.get(v) || 0) + 1);
    }
    dagilim = [...m.entries()].sort((a, b) => b[1] - a[1]).slice(0, 12).map(([deger, sayi]) => ({ deger, sayi }));
  }
  if (q.sirala && alanlar.includes(q.sirala)) {
    const k = q.sirala;
    const dir = q.yon === 'azalan' ? -1 : 1;
    rows = [...rows].sort((a, b) => {
      const x = a[k];
      const y = b[k];
      if (typeof x === 'number' && typeof y === 'number') return (x - y) * dir;
      return String(x ?? '').localeCompare(String(y ?? ''), 'tr') * dir;
    });
  }
  const boyut = Math.min(Math.max(q.boyut || 50, 10), 200);
  const sayfa = Math.max(q.sayfa || 1, 1);
  const OV_KEY: Record<string, string> = { mufredat: 'mufredat', slayt: 'slayt', kisaltma: 'kisaltmalar', terim: 'terimler', varlik: 'varliklar', faz6: 'faz6' };
  const parca = rows.slice((sayfa - 1) * boyut, sayfa * boyut).map((r) => {
    const ov = getPhaseOverride(String(r.soru_id));
    const k = OV_KEY[cat.id];
    return {
      ...r,
      _kok: stemOf(String(r.soru_id)).slice(0, 160),
      _elle: Boolean(ov),
      _durum: k && ov?.kaldir?.includes(k) ? 'kaldırıldı' : k && ov?.gizle?.includes(k) ? 'gizli' : null,
    };
  });
  return { kategori: cat.id, alanlar, toplam: rows.length, sayfa, boyut, satirlar: parca, dagilim };
}
