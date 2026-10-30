/**
 * Soru dışa aktarıcı · veri katmanı. Sitedeki her soru türü tek modele (AQ) çevrilir:
 *   cikmis   çıkmış sorular (ApiService.getPastQuestions; karantina/gizli/Dönem 3 dışı süzülür)
 *   havuz    öğrencilerin topladığı sorular (ApiService.getQuestions)
 *   ornek    kazanım temelli örnek sorular (src/data/ornek_sorular/k*)
 *   hoca     hoca üslubu sorular (src/data/hoca_uslubu_sorular/k*)
 *   cozucu   sesli soru çözücü setleri (src/data/<branş>_cozucu; ornek/benzer/cikmis türleriyle)
 *   hocaara  sesli dersteki "hocanın sorabileceği" sorular (k*hocaara_cozucu)
 *   calisma  Öğren çalışma soruları (src/data/study_questions)
 *   mini     Öğren destelerindeki mini sorular (seçilen desteler yüklenir)
 * Görünürlük: çözücü dizini panelde kapatılan dersleri zaten süzer (cozucuDizinYukle).
 */
import { ApiService } from '../../../services/api';
import { isDonem3Question, normalizeCommitteeId, normalizeDonem3Discipline } from '../../../data/curriculumData';
import { fromPastQuestion, fromPoolQuestion, loadOrnekQuestions, miniQuestionsFromDeck, ORNEK_INDEX, type PdfQuestion } from '../../pdf/pdfSources';
import { BRANSLAR, type Brans } from '../../spots/brans';
import { cozucuDersYukle, cozucuDizinYukle } from '../../spots/cozucu/cozucuVeri';
import { loadDeck, loadDeckCatalog, type DeckCatalogEntry } from '../../../data/deckStore';

export type KaynakId = 'cikmis' | 'havuz' | 'ornek' | 'hoca' | 'cozucu' | 'hocaara' | 'calisma' | 'mini';

export interface KaynakTanim { id: KaynakId; ad: string; alt: string }
export const KAYNAKLAR: KaynakTanim[] = [
  { id: 'cikmis', ad: 'Çıkmış sorular', alt: 'Geçmiş sınavlardan, şık analiziyle' },
  { id: 'ornek', ad: 'Örnek sorular', alt: 'Kazanım temelli, müfredata sadık' },
  { id: 'cozucu', ad: 'Sesli çözücü soruları', alt: 'Branş setleri: örnek, benzer, çıkmış' },
  { id: 'hoca', ad: 'Hoca üslubu sorular', alt: 'Hocanın soru mantığıyla yazılanlar' },
  { id: 'hocaara', ad: 'Hocanın sorabileceği', alt: 'Sesli dersteki ara sorular' },
  { id: 'calisma', ad: 'Öğren çalışma soruları', alt: 'Ders adımlarından pekiştirme' },
  { id: 'mini', ad: 'Öğren mini soruları', alt: 'Seçtiğin destelerin içinden' },
  { id: 'havuz', ad: 'Soru havuzu', alt: 'Öğrencilerin topladığı sorular' },
];
export const kaynakAdi = (id: KaynakId) => KAYNAKLAR.find((k) => k.id === id)?.ad || id;

/** Dışa aktarılan tek soru: PdfQuestion + süzgeç alanları */
export interface AQ extends PdfQuestion {
  /** benzersiz anahtar (kaynak önekli) */
  key: string;
  kaynak: KaynakId;
  kurul: number;
  /** ders/branş adı (süzgeç, renk) */
  ders: string;
  /** konu / ders başlığı */
  konu: string;
  /** soru türü: Çıkmış, Örnek, Benzer, Hoca … */
  tur: string;
  /** öğrenciye anlamlı etiketler (çıkmış `tags` + rozetler; hat/süreç etiketleri ayıklanır) */
  etiketler: string[];
  /** arama için katlanmış metin */
  ara: string;
}

/** Metin alanı: yalnız metin/sayı kabul edilir (veride boolean `false` gibi işaretler metne dönüşmesin) */
const s = (v: unknown) => (typeof v === 'string' || typeof v === 'number' ? String(v).trim() : '');
const HARF = ['A', 'B', 'C', 'D', 'E', 'F'];
export const katla = (t: string) =>
  t.toLocaleLowerCase('tr').replace(/[ıi̇]/g, 'i').replace(/ş/g, 's').replace(/ğ/g, 'g').replace(/ü/g, 'u').replace(/ö/g, 'o').replace(/ç/g, 'c');
const kurulNo = (v: unknown): number => {
  const m = /kurul\s*[_-]?\s*(\d)/i.exec(s(v)) || /^k(\d)/i.exec(s(v));
  return m ? Number(m[1]) : 0;
};
/** Süreç/hat etiketleri (check_solve, faz14_…, donem3-kurul1, 2018-2019, dosya adı) öğrenciye gösterilmez; ders/yıl/tür zaten ayrı alandır */
const GIZLI_ETIKET = new Set(['çıkmış sınav', 'geçmiş sınav', 'kategorisiz', 'dönem 1', 'dönem 2', 'dönem 3', 'kurul']);
export function etiketCikar(tags: unknown, q: PdfQuestion): string[] {
  const out: string[] = [];
  const ekle = (t: unknown) => {
    const v = s(t);
    if (!v || v.length > 60 || out.includes(v)) return;
    const k = v.toLocaleLowerCase('tr');
    if (/_/.test(v) || /^donem\d/i.test(v) || /^\d{4}-\d{4}/.test(v) || /\.(pdf|docx?|jpe?g|png)$/i.test(v)) return;
    if (GIZLI_ETIKET.has(k) || k === s(q.discipline).toLocaleLowerCase('tr') || k === s(q.year).toLocaleLowerCase('tr')) return;
    out.push(v);
  };
  if (Array.isArray(tags)) tags.forEach(ekle);
  // rozetler: "Denetleyici onaylı", "Cevap tartışmalı", "Klinik karar" …; süreç rozeti (Faz 14) öğrenciye anlamsız
  (q.badges || []).filter((b) => b.tone !== 'ai').forEach((b) => ekle(b.label));
  return out;
}
const tamamla = (q: PdfQuestion, ek: Omit<AQ, keyof PdfQuestion | 'ara' | 'key' | 'etiketler'> & { key?: string; etiketler?: string[] }): AQ => {
  const a: AQ = { ...q, ...ek, key: ek.key || `${ek.kaynak}:${q.id}`, etiketler: ek.etiketler || etiketCikar([], q), ara: '' };
  a.ara = katla([a.stem, a.ders, a.konu, a.year, ...a.etiketler, ...a.options.map((o) => o.text)].join(' '));
  return a;
};
/** Branş adı: "Kurul 2 Nöroloji" → "Nöroloji" */
const bransAdi = (b: Brans) => {
  const t = BRANSLAR.find((x) => x.id === b);
  return (t?.tam || String(b)).replace(/^Kurul\s*\d\s*/i, '');
};

/* ---------------------------------------------------------------------------
 * Yükleyiciler (her kaynak bir kez; bellekte tutulur)
 * ------------------------------------------------------------------------- */
const bellek = new Map<string, Promise<AQ[]>>();
const tek = (k: string, f: () => Promise<AQ[]>) => {
  let p = bellek.get(k);
  if (!p) {
    p = f();
    p.catch(() => bellek.delete(k));
    bellek.set(k, p);
  }
  return p;
};

async function cikmisYukle(): Promise<AQ[]> {
  const data: any[] = await ApiService.getPastQuestions();
  const out: AQ[] = [];
  for (const q of data) {
    if (q.id?.startsWith('civan-') || q.tags?.some((t: string) => /civan/i.test(t))) continue;
    if (q.isQuarantined || q.quarantined || (Array.isArray(q.tags) && q.tags.includes('karantina'))) continue;
    if (q.hidden || q.data?.hidden) continue;
    const committeeId = normalizeCommitteeId(q.committeeId) || q.committeeId;
    if (!isDonem3Question({ ...q, committeeId })) continue;
    const p = fromPastQuestion({ ...q, committeeId, discipline: normalizeDonem3Discipline(q.discipline) || q.discipline });
    if (!p || p.options.length < 2) continue;
    out.push(tamamla(p, { kaynak: 'cikmis', kurul: kurulNo(p.committeeId), ders: p.discipline, konu: p.topic || '', tur: 'Çıkmış', etiketler: etiketCikar(q.tags, p) }));
  }
  return out;
}

async function havuzYukle(): Promise<AQ[]> {
  const data = await ApiService.getQuestions({});
  return data
    .map(fromPoolQuestion)
    .filter((p): p is PdfQuestion => !!p && p.options.length >= 2)
    .map((p) => tamamla(p, { kaynak: 'havuz', kurul: kurulNo(p.committeeId), ders: p.discipline, konu: p.topic || '', tur: 'Havuz' }));
}

async function ornekYukle(): Promise<AQ[]> {
  const lists = await Promise.all(
    ORNEK_INDEX.map(async (r) => {
      const qs = await loadOrnekQuestions(r.id).catch(() => [] as PdfQuestion[]);
      const kurul = kurulNo(r.id) || 1;
      return qs.map((p) => tamamla({ ...p, committeeId: `donem3-kurul${kurul}` }, { kaynak: 'ornek', kurul, ders: p.discipline, konu: r.konu || p.topic || '', tur: 'Örnek' }));
    }),
  );
  return lists.flat();
}

const hocaDosya = import.meta.glob('../../../data/hoca_uslubu_sorular/k[1-6]/k[1-6]-*.json', { import: 'default' }) as Record<string, () => Promise<any>>;
async function hocaYukle(): Promise<AQ[]> {
  const out: AQ[] = [];
  for (const [yol, f] of Object.entries(hocaDosya).sort()) {
    const d = await f().catch(() => null);
    if (!d) continue;
    const kurul = kurulNo(/\/(k\d)\//.exec(yol)?.[1]) || 1;
    (d.sorular || []).forEach((q: any, i: number) => {
      const options = (q.siklar || []).map((t: string, j: number) => ({ key: HARF[j], text: s(t), why: s(q.aciklama?.[HARF[j]]) || undefined }));
      if (options.length < 2 || !s(q.kok)) return;
      const p: PdfQuestion = {
        id: s(q.id) || `${d.ders_id}-${i + 1}`, source: 'ornek', number: i + 1, committeeId: `donem3-kurul${kurul}`,
        discipline: s(d.brans) || 'Tıp', topic: s(d.konu), stem: s(q.kok), options, answer: s(q.cevap).toUpperCase().slice(0, 1) || undefined,
        explanation: s(q.cikarim) || undefined, refs: q.kaynak ? [s(q.kaynak)] : [], badges: [],
        kazanim: q.kazanim ? { text: s(q.kazanim) } : undefined,
      };
      out.push(tamamla(p, { kaynak: 'hoca', kurul, ders: p.discipline, konu: p.topic || '', tur: 'Hoca üslubu' }));
    });
  }
  return out;
}

const TUR_AD: Record<string, string> = { ornek: 'Örnek', benzer: 'Benzer', cikmis: 'Çıkmış' };
/** Ders kayıt defteri (k2-07 → branş): ara soruların dersini bulmak için */
const KAYIT = import.meta.glob('../../../data/dersler/k[1-6].json', { eager: true, import: 'default' }) as Record<string, { dersler?: { id: string; brans?: string }[] }>;
const kayitBrans = (key: string | undefined): string => {
  const id = /^(?:y25-)?(k\d-\d+)/.exec(s(key))?.[1];
  if (!id) return '';
  for (const k of Object.values(KAYIT)) {
    const d = k.dersler?.find((x) => x.id === id);
    if (d?.brans) return d.brans;
  }
  return '';
};
async function cozucuYukle(ara: boolean): Promise<AQ[]> {
  const branslar = BRANSLAR.filter((b) => /hocaara$/.test(b.id) === ara);
  const out: AQ[] = [];
  for (const b of branslar) {
    const dz = await cozucuDizinYukle(b.id).catch(() => null);
    if (!dz) continue;
    const kurul = /^k(\d)/.exec(b.id) ? Number(b.id[1]) : 1;
    const ders = ara ? '' : bransAdi(b.id);
    const dersler = await Promise.all(dz.dersler.map((x) => cozucuDersYukle(x.kod, b.id).then((d) => ({ d, key: x.key }), () => null)));
    for (const r of dersler) {
      if (!r) continue;
      const d = r.d;
      const dersAd = ders || kayitBrans(r.key) || 'Tıp';
      for (const q of d.sorular || []) {
        const options = HARF.slice(0, 5)
          .filter((h) => s((q.secenekler as any)?.[h]))
          .map((h) => ({ key: h, text: s((q.secenekler as any)[h]), why: s((q.siklar as any)?.[h]) || undefined }));
        if (options.length < 2) continue;
        const sayfa = Array.isArray(q.sayfa) && q.sayfa.length ? `Slayt ${q.sayfa.join(', ')}` : '';
        const p: PdfQuestion = {
          id: `${d.kod}-${q.no}`, source: 'ornek', number: q.no, committeeId: `donem3-kurul${kurul}`,
          discipline: dersAd, topic: s(d.baslik), year: q.tur === 'cikmis' ? s(q.sinav) || undefined : undefined,
          difficulty: q.zorluk, stem: s(q.soru), options, answer: s(q.dogru) || undefined, explanation: s(q.cozum) || undefined,
          refs: sayfa ? [sayfa] : [], badges: [],
        };
        out.push(tamamla(p, {
          key: `${ara ? 'hocaara' : 'cozucu'}:${b.id}:${d.kod}:${q.no}`, kaynak: ara ? 'hocaara' : 'cozucu', kurul,
          ders: dersAd, konu: s(d.baslik),
          tur: ara ? 'Hoca sorabilir' : /hoca$/.test(b.id) ? 'Hoca sorusu' : TUR_AD[q.tur || 'ornek'] || 'Örnek',
        }));
      }
    }
  }
  return out;
}

const calismaDosya = import.meta.glob('../../../data/study_questions/chunk_*.json', { import: 'default' }) as Record<string, () => Promise<any[]>>;
async function calismaYukle(): Promise<AQ[]> {
  const parts = await Promise.all(Object.values(calismaDosya).map((f) => f().catch(() => [] as any[])));
  const out: AQ[] = [];
  for (const q of parts.flat()) {
    const options = (q.options || []).map((t: string, j: number) => ({ key: HARF[j], text: s(t).replace(/^\s*[A-Ea-e][).:-]\s*/, '') }));
    if (options.length < 2 || !s(q.question)) continue;
    const ans = typeof q.correctAnswer === 'number' ? HARF[q.correctAnswer] : s(q.correctAnswer).toUpperCase().slice(0, 1);
    const kurul = kurulNo(q.committee) || 1;
    const ders = s(q.discipline).split(/\s*\/\s*/)[0] || 'Tıp';
    const p: PdfQuestion = {
      id: s(q.id), source: 'mini', committeeId: `donem3-kurul${kurul}`, discipline: ders, topic: s(q.deckTitle),
      group: q.slideTitle ? `Adım ${q.slideNumber} · ${s(q.slideTitle)}` : undefined, stem: s(q.question), options,
      answer: ans || undefined, explanation: s(q.explanation) || undefined, refs: [], badges: [],
    };
    out.push(tamamla(p, { kaynak: 'calisma', kurul, ders, konu: s(q.deckTitle), tur: 'Çalışma' }));
  }
  return out;
}

/** Mini sorular için seçilebilir desteler (yayındakiler) */
export async function miniDesteler(): Promise<DeckCatalogEntry[]> {
  const [k, m] = await Promise.all([loadDeckCatalog(), import('../../learn/LearnLibrary')]);
  return k.filter((d) => m.isPublished(d) && (d.questionCount || 0) > 0);
}
async function miniYukle(desteIds: string[]): Promise<AQ[]> {
  const kat = await loadDeckCatalog();
  const lists = await Promise.all(
    desteIds.map(async (id) => {
      const d: any = await loadDeck(id).catch(() => null);
      if (!d) return [] as AQ[];
      const e = kat.find((x) => x.id === id);
      const kurul = kurulNo(e?.committee || d.committee) || 1;
      const ders = s(d.discipline || e?.discipline).split(/\s*\/\s*/)[0] || 'Tıp';
      return miniQuestionsFromDeck(d, true).map((p) =>
        tamamla({ ...p, committeeId: `donem3-kurul${kurul}` }, { key: `mini:${p.id}`, kaynak: 'mini', kurul, ders, konu: s(d.shortTitle || d.title), tur: p.badges.length ? 'Klinik karar' : 'Mini soru' }),
      );
    }),
  );
  return lists.flat();
}

export function kaynakYukle(id: KaynakId, opts: { desteler?: string[] } = {}): Promise<AQ[]> {
  switch (id) {
    case 'cikmis': return tek(id, cikmisYukle);
    case 'havuz': return tek(id, havuzYukle);
    case 'ornek': return tek(id, ornekYukle);
    case 'hoca': return tek(id, hocaYukle);
    case 'cozucu': return tek(id, () => cozucuYukle(false));
    case 'hocaara': return tek(id, () => cozucuYukle(true));
    case 'calisma': return tek(id, calismaYukle);
    case 'mini': {
      const ids = [...(opts.desteler || [])].sort();
      return ids.length ? tek(`mini:${ids.join(',')}`, () => miniYukle(ids)) : Promise.resolve([]);
    }
  }
}

/* ---------------------------------------------------------------------------
 * Süzgeç
 * ------------------------------------------------------------------------- */
export interface Suzgec {
  kaynaklar: KaynakId[];
  kurullar: number[];
  dersler: string[];
  konular: string[];
  yillar: string[];
  turler: string[];
  zorluk: string[];
  /** seçilen etiketlerden en az birini taşıyan sorular */
  etiketler: string[];
  arama: string;
  cevapli: boolean;
  aciklamali: boolean;
  desteler: string[];
}
export const BOS_SUZGEC: Suzgec = {
  kaynaklar: ['cikmis'], kurullar: [], dersler: [], konular: [], yillar: [], turler: [], zorluk: [], etiketler: [], arama: '',
  cevapli: false, aciklamali: false, desteler: [],
};

/** Tek alan dışındaki süzgeçleri uygular (seçenek sayımları kendi alanını yok sayar) */
export function suz(list: AQ[], f: Suzgec, haric?: keyof Suzgec): AQ[] {
  const ara = katla(f.arama.trim()).split(/\s+/).filter(Boolean);
  const k = (alan: keyof Suzgec, v: any[]) => haric === alan || !v?.length;
  return list.filter((q) =>
    (k('kurullar', f.kurullar) || f.kurullar.includes(q.kurul)) &&
    (k('dersler', f.dersler) || f.dersler.includes(q.ders)) &&
    (k('konular', f.konular) || f.konular.includes(q.konu)) &&
    (k('yillar', f.yillar) || f.yillar.includes(q.year || '—')) &&
    (k('turler', f.turler) || f.turler.includes(q.tur)) &&
    (k('zorluk', f.zorluk) || f.zorluk.includes(q.difficulty || '—')) &&
    (k('etiketler', f.etiketler) || q.etiketler.some((t) => f.etiketler.includes(t))) &&
    (!f.cevapli || !!q.answer) &&
    (!f.aciklamali || !!q.explanation || q.options.some((o) => o.why)) &&
    (!ara.length || ara.every((w) => q.ara.includes(w))),
  );
}

export type SecenekAlan = 'kurullar' | 'dersler' | 'konular' | 'yillar' | 'turler' | 'zorluk' | 'etiketler';
/** Bir alanın değerleri ve sayıları (diğer süzgeçler uygulanmış hâlde); etikette bir soru birden çok değere sayılır */
export function secenekler(list: AQ[], f: Suzgec, alan: SecenekAlan): { v: string; n: number }[] {
  const m = new Map<string, number>();
  for (const q of suz(list, f, alan)) {
    if (alan === 'etiketler') { for (const t of q.etiketler) m.set(t, (m.get(t) || 0) + 1); continue; }
    const v = alan === 'kurullar' ? String(q.kurul) : alan === 'dersler' ? q.ders : alan === 'konular' ? q.konu : alan === 'yillar' ? q.year || '—' : alan === 'turler' ? q.tur : q.difficulty || '—';
    if (!v) continue;
    m.set(v, (m.get(v) || 0) + 1);
  }
  const arr = [...m].map(([v, n]) => ({ v, n }));
  if (alan === 'yillar') return arr.sort((a, b) => b.v.localeCompare(a.v, 'tr', { numeric: true }));
  if (alan === 'kurullar') return arr.sort((a, b) => Number(a.v) - Number(b.v));
  if (alan === 'zorluk') { const o = ['kolay', 'orta', 'zor', '—']; return arr.sort((a, b) => o.indexOf(a.v) - o.indexOf(b.v)); }
  return arr.sort((a, b) => b.n - a.n || a.v.localeCompare(b.v, 'tr'));
}
