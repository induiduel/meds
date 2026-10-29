/**
 * Sorgu zekâsı paketi derleyicisi (yalnız Node, ayrı süreçte çalışır — sunucu belleğine girmez).
 *
 * Girdi: data/local_rag_chunks.json (tüm arama derlemi) + sözlük kaynakları (hastalıklar, ansiklopedi,
 * tıbbi terimler sözlüğü, küratörlü halk dili eşanlamlıları, ders başlıkları).
 * Çıktı: data/search/query-intel.json (sözcükler, sıklıklar, kavramlar) + query-intel.bin (SymSpell + n-gram).
 * İmza aynıysa yeniden yazmaz (her açılışta çağrılabilir).
 */
import fs from 'fs';
import path from 'path';
import { type ConceptType, type PackedConcept, SYM_PREFIX, deleteKeys, fnv1a, fold, lemma, splitWords, PhraseMatcher } from './core';
import { PACK_VERSION, type QueryIntelPackJson, encodeBins } from './engine';

const BUILDER_REV = 10;

/** Halk dili / eski adlandırma → tıbbi terim. Sorgu yeniden yazımında güvenle kullanılır (güçlü takma ad). */
export const CURATED_SYNONYMS: Array<[string, string]> = [
  ['kansızlık', 'Anemi'], ['kırmızı küre', 'Eritrosit'], ['alyuvar', 'Eritrosit'], ['akyuvar', 'Lökosit'], ['beyaz küre', 'Lökosit'],
  ['kan pulcuğu', 'Trombosit'], ['yüksek tansiyon', 'Hipertansiyon'], ['tansiyon yüksekliği', 'Hipertansiyon'], ['düşük tansiyon', 'Hipotansiyon'],
  ['şeker hastalığı', 'Diabetes Mellitus'], ['diyabet', 'Diabetes Mellitus'], ['kalp krizi', 'Miyokard Enfarktüsü'], ['nefes darlığı', 'Dispne'],
  ['sarılık', 'İkter'], ['ishal', 'Diyare'], ['kabızlık', 'Konstipasyon'], ['çarpıntı', 'Palpitasyon'], ['kaşıntı', 'Pruritus'],
  ['böbrek yetmezliği', 'Renal Yetmezlik'], ['karaciğer yağlanması', 'Hepatosteatoz'], ['idrarda kan', 'Hematüri'], ['idrarda protein', 'Proteinüri'],
  ['idrar yolu enfeksiyonu', 'Üriner Sistem Enfeksiyonu'], ['iye', 'Üriner Sistem Enfeksiyonu'], ['bulantı', 'Nevze'], ['kusma', 'Emezis'],
  ['baş ağrısı', 'Sefalji'], ['ateş', 'Febril'], ['inme', 'Serebrovasküler Olay'], ['felç', 'Serebrovasküler Olay'],
  ['verem', 'Tüberküloz'], ['guatr', 'Guatr'], ['şişlik', 'Ödem'], ['morarma', 'Siyanoz'], ['bayılma', 'Senkop'], ['göğüs ağrısı', 'Göğüs Ağrısı'],
  ['kemik erimesi', 'Osteoporoz'], ['damar sertliği', 'Ateroskleroz'], ['kan zehirlenmesi', 'Sepsis'], ['kan pıhtısı', 'Trombüs'],
  ['düşük', 'Abortus'], ['dış gebelik', 'Ektopik Gebelik'], ['gebelik zehirlenmesi', 'Preeklampsi'], ['rahim', 'Uterus'], ['yumurtalık', 'Over'],
  ['böbrek taşı', 'Nefrolitiazis'], ['safra taşı', 'Kolelitiazis'], ['mide ülseri', 'Peptik Ülser'], ['reflü', 'Gastroözofageal Reflü'],
  ['kalp yetmezliği', 'Kalp Yetmezliği'], ['tiroid az çalışması', 'Hipotiroidi'], ['tiroid fazla çalışması', 'Hipertiroidi'],
  ['kireçlenme', 'Osteoartrit'], ['romatizma', 'Romatoid Artrit'], ['akciğer kanseri', 'Akciğer Karsinomu'], ['böbrek kanseri', 'Renal Hücreli Karsinom'],
  ['mesane kanseri', 'Ürotelyal Karsinom'], ['prostat büyümesi', 'Benign Prostat Hiperplazisi'], ['bph', 'Benign Prostat Hiperplazisi'],
  ['rhk', 'Renal Hücreli Karsinom'], ['mi', 'Miyokard Enfarktüsü'], ['kby', 'Kronik Böbrek Yetmezliği'], ['aby', 'Akut Böbrek Yetmezliği'],
  ['dm', 'Diabetes Mellitus'], ['htn', 'Hipertansiyon'], ['kah', 'Koroner Arter Hastalığı'], ['koah', 'Kronik Obstrüktif Akciğer Hastalığı'],
  ['sle', 'Sistemik Lupus Eritematozus'], ['ra', 'Romatoid Artrit'], ['dic', 'Dissemine İntravasküler Koagülasyon'], ['ttp', 'Trombotik Trombositopenik Purpura'],
  ['hus', 'Hemolitik Üremik Sendrom'], ['psgn', 'Poststreptokokal Glomerülonefrit'], ['fsgs', 'Fokal Segmental Glomerüloskleroz'],
  ['mgn', 'Membranöz Glomerülonefrit'], ['rpgn', 'Hızlı İlerleyen Glomerülonefrit'], ['adpkd', 'Otozomal Dominant Polikistik Böbrek Hastalığı'],
  ['hpv', 'İnsan Papilloma Virüsü'], ['hiv', 'İnsan İmmün Yetmezlik Virüsü'], ['tbc', 'Tüberküloz'], ['tb', 'Tüberküloz'],
];

const TERM_TYPE: Record<string, ConceptType> = {
  hastalik_sendrom: 'disease', ilac: 'drug', gen_protein_biyobelirtec: 'gene', belirti_semptom_bulgu: 'symptom',
  anatomi_doku_hucre: 'anatomy', patojen: 'pathogen', tani_yontem: 'procedure', fizyoloji_mekanizma: 'term', donem_siklus_kavram: 'term',
};
const ENC_TYPE: Record<string, ConceptType> = {
  hastalik: 'disease', patoloji: 'disease', pathology: 'disease', ilac: 'drug', genetik: 'gene', genetic: 'gene', protein: 'gene',
  patojen: 'pathogen', mikrobiyoloji: 'pathogen', parazitoloji: 'pathogen', terim: 'term',
};
const TYPE_RANK: Record<ConceptType, number> = { disease: 9, drug: 8, gene: 7, pathogen: 7, symptom: 6, procedure: 5, anatomy: 4, term: 3, topic: 2 };

/** Aramada anlamsız sözcük üreten başlık/etiket satırları */
const HEADER_LINE = /^\s*\[[^\]]{2,80}\]\s*$/;
const LABEL_PREFIX = /^\s*(?:⭐\s*)?([A-ZÇĞİÖŞÜ][\p{L} \/()-]{1,30}):\s*/u;
const META_WORDS = /denetleyici|onaylı|altın standart|doğrulandı|guyton\/robbins/giu;

export function cleanContent(text: string): string {
  const lines = String(text || '').split('\n');
  const out: string[] = [];
  for (const ln of lines) {
    if (HEADER_LINE.test(ln)) continue;
    // Yazdırma/OCR artığı satırlar: dosya yolu, URL, Arapça/İbranice yazı (ör. "cevapiniz.html … file:///Users/…")
    if (/file:\/\/|https?:\/\/|www\.|\.html?\b|[\u0590-\u06FF]/i.test(ln)) continue;
    out.push(ln.replace(LABEL_PREFIX, '').replace(META_WORDS, ' ').replace(/\((?:Sayfa|Slayt)[^)]*\)/giu, ' '));
  }
  return out.join('\n');
}

interface MutConcept {
  label: string;
  type: ConceptType;
  ref: string;
  aliases: Map<string, boolean>; // takma ad → güçlü mü
  discipline: string;
  mentions: number;
}

function readJson<T = any>(p: string): T | null {
  try { return JSON.parse(fs.readFileSync(p, 'utf-8')) as T; } catch { return null; }
}

function mtimeOf(p: string): number {
  try { return Math.round(fs.statSync(p).mtimeMs); } catch { return 0; }
}

export interface BuildOptions {
  projectRoot: string;
  chunksPath?: string;
  outDir?: string;
  force?: boolean;
  log?: (m: string) => void;
}

export interface BuildResult {
  skipped: boolean;
  signature: string;
  stats: Record<string, number>;
  jsonPath: string;
  binPath: string;
}

export function lexiconSources(root: string) {
  return {
    diseases: path.join(root, 'src', 'data', 'diseases.json'),
    encyclopedia: path.join(root, 'src', 'data', 'medical_encyclopedia.json'),
    glossary: path.join(root, 'src', 'data', 'medical_glossary.json'),
    // Konteynerde meds_database_v2 farklı yere bağlanabilir: MEDS_DATABASE_V2_DIR
    terms: path.join(process.env.MEDS_DATABASE_V2_DIR || path.join(root, '..', 'meds_database_v2'), 'tibbi_terimler_sozlugu', 'tibbi_terimler_sozlugu.json'),
  };
}

/** Kavram sözlüğü (derlem geçişinden önce) */
function buildConcepts(root: string): MutConcept[] {
  const src = lexiconSources(root);
  const byKey = new Map<string, MutConcept>();
  const keyOf = (s: string) => fold(s).replace(/\s*\([^)]*\)\s*/g, ' ').replace(/[^a-z0-9]+/g, ' ').trim();
  const add = (label: string, type: ConceptType, ref: string, discipline: string, aliases: Array<[string, boolean]>): MutConcept | null => {
    label = String(label || '').replace(/_\s*/g, ': ').replace(/\s+/g, ' ').trim();
    if (label.length < 2 || label.length > 90) return null;
    const k = keyOf(label);
    if (!k) return null;
    // Tek sözcüklük çekimli etiket ("Tümörün", "Neoplazmlarının") kavram değildir (hastalık sayfaları hariç)
    if (!k.includes(' ') && lemma(k) !== k && !ref.startsWith('disease:')) return null;
    let c = byKey.get(k);
    if (!c) {
      c = { label, type, ref, aliases: new Map(), discipline: discipline || '', mentions: 0 };
      byKey.set(k, c);
    } else if (TYPE_RANK[type] > TYPE_RANK[c.type] || (!c.ref && ref)) {
      // Daha güçlü kaynak (hastalık sayfası) etiketi ve bağlantıyı devralır; eski etiket takma ad olur
      if (c.label !== label) c.aliases.set(c.label, true);
      if (TYPE_RANK[type] >= TYPE_RANK[c.type]) { c.label = label; c.type = type; }
      if (ref && (!c.ref || ref.startsWith('disease:'))) c.ref = ref;
      if (!c.discipline) c.discipline = discipline || '';
    }
    for (const [a, strong] of aliases) {
      const al = String(a || '').replace(/\s+/g, ' ').trim();
      if (/_|sayfa|slayt/i.test(al)) continue;
      if (al.length < 2 || al.length > 80 || keyOf(al) === keyOf(c.label)) continue;
      if (!c.aliases.has(al) || strong) c.aliases.set(al, strong || c.aliases.get(al) || false);
      // Takma ad aynı zamanda ayrı bir kavram anahtarıysa onu da bu kavrama yönlendir (birleştirme sonra)
    }
    return c;
  };
  const paren = (name: string): Array<[string, boolean]> => {
    const out: Array<[string, boolean]> = [];
    if (!name) return out;
    name = String(name);
    const m = name.match(/\(([^)]{2,40})\)/);
    if (m) {
      for (const part of m[1].split(/[\/,;]/)) out.push([part.trim(), true]);
      out.push([name.replace(/\s*\([^)]*\)\s*/g, ' ').trim(), true]);
    }
    return out;
  };

  const diseases = readJson<any[]>(src.diseases) || [];
  for (const d of diseases) {
    // Birleştirilmiş eski kayıtların adları (altNames) da aynı kavrama bağlanır
    const alt = (d.altNames || []).flatMap((n: string) => [[n, true], ...paren(n)]);
    add(d.name, 'disease', `disease:${d.id}`, d.category || '', [[d.latinName, true], ...paren(d.name), ...alt]);
  }
  const enc = readJson<any[]>(src.encyclopedia) || [];
  const diseaseIds = new Set(diseases.map((d) => d.id));
  for (const e of enc) {
    const type = ENC_TYPE[String(e.category || '').toLowerCase()] || 'term';
    const ref = diseaseIds.has(e.id) ? `disease:${e.id}` : `glossary:${e.id}`;
    add(e.term, type, ref, e.discipline || '', [[e.latinName, true], ...(e.aliases || []).map((a: string) => [a, true] as [string, boolean]), ...paren(e.term)]);
  }
  const gl = readJson<Record<string, any>>(src.glossary) || {};
  for (const [k, v] of Object.entries(gl)) {
    const type = ENC_TYPE[String(v.category || '').toLowerCase()] || 'term';
    add(v.term || k, type, `glossary:${v.id || v.term || k}`, v.discipline || '', [...(v.aliases || []).map((a: string) => [a, true] as [string, boolean]), ...paren(v.term || k)]);
  }
  const terms = readJson<any>(src.terms);
  for (const [k, v] of Object.entries<any>(terms?.terimler || {})) {
    if (v.tibbi_terim === false || v.sinif_gerekce === 'tum_kelimeler_halk_bilir') continue;
    const type = TERM_TYPE[v.kategori] || 'term';
    const al: Array<[string, boolean]> = [];
    if (v.latin) al.push([v.latin, false]);
    if (v.english && String(v.english).length >= 4) al.push([v.english, false]);
    for (const s of v.esanlamlilar || []) {
      const t = String(s || '').trim();
      if (t && t.split(/\s+/).length <= 3 && t.length <= 40) al.push([t, false]);
    }
    const label = String(v.turkce || k).trim();
    // Sözlükte çekimli biçimler ayrı terim olarak duruyor ("Tümörleri", "Hastalarında"): kavram değil
    const lf = fold(label);
    if (!label.includes(' ') && lemma(lf) !== lf) continue;
    if (label.includes(' ') && lemma(lf.split(' ').pop()!) !== lf.split(' ').pop() && /(larinda|lerinde|larinin|lerinin|larina|lerine|lari|leri)$/.test(lf)) continue;
    add(label.charAt(0).toLocaleUpperCase('tr-TR') + label.slice(1), type, `term:${v.id || k}`, '', al);
  }
  for (const [halk, tip] of CURATED_SYNONYMS) {
    const c = byKey.get(keyOf(tip)) || add(tip, 'term', '', '', []);
    if (!c || keyOf(halk) === keyOf(c.label)) continue;
    c.aliases.set(halk, true);
    // Halk dili ifadesi ayrıca kendi kavramıysa ("Yüksek tansiyon" terimi) hedef kavrama katılır
    const dup = byKey.get(keyOf(halk));
    if (dup && dup !== c) {
      for (const [a, st] of dup.aliases) if (keyOf(a) !== keyOf(c.label)) c.aliases.set(a, st || c.aliases.get(a) || false);
      if (!c.ref && dup.ref) c.ref = dup.ref;
      byKey.delete(keyOf(halk));
    }
  }
  return [...byKey.values()];
}

/** Ders başlığı kavramları: slayt/özet/deste başlıklarından ("21)Glomerüler Hastalıklar_ Nefrotik Sendrom (Sayfa 34)") */
function topicFromTitle(title: string): string | null {
  let t = String(title || '')
    .replace(/^⭐\s*\[[^\]]*\]\s*/u, '')
    .replace(/\((?:Sayfa|Slayt)[^)]*\)/giu, '')
    .replace(/^\s*\d{1,3}\s*[)\-.]\s*/u, '')
    .replace(/_/g, ':')
    .replace(/\s+/g, ' ')
    .trim();
  if (t.includes(' — ')) t = t.split(' — ')[0].trim();
  if (/^(Örnek Soru|Sözlük|Hastalık):/u.test(t)) t = t.replace(/^[^:]+:\s*/u, '');
  if (t.length < 6 || t.length > 70 || /^\d+$/.test(t) || !/\p{L}{3}/u.test(t)) return null;
  return t;
}

/**
 * Derlemden kısaltma madenciliği: "Von Hippel-Lindau (VHL)", "Ani Kardiyak Ölüm (AKÖ)".
 * Uzun biçim, kısaltmanın harfleri sondan geriye sözcük baş harfleriyle eşleşene kadar kırpılır ("ve/ile" atlanır);
 * eşleşmeyen çiftler ("Hepsi ← III ve IV") elenir.
 */
const ABBR_RE = /([A-Za-zÇĞİÖŞÜçğıöşüâî][A-Za-zÇĞİÖŞÜçğıöşüâî'’ -]{3,80}?)\s*\(([A-ZÇĞİÖŞÜ][A-ZÇĞİÖŞÜ0-9-]{1,7})\)/gu;
const ABBR_SKIP = new Set(['ve', 'ile', 'veya', 'of', 'and', 'the', 'de', 'da']);

export function abbreviationLongForm(longRaw: string, acr: string): string | null {
  const letters = fold(acr).replace(/[^a-z]/g, '');
  if (letters.length < 2) return null;
  const words = longRaw.trim().split(/\s+/);
  // Kısa çizgili sözcük parçaları ayrı baş harf verir: Hippel-Lindau → H, L
  const parts: Array<{ w: string; idx: number }> = [];
  words.forEach((w, idx) => w.split('-').forEach((p) => p && parts.push({ w: p, idx })));
  let li = letters.length - 1;
  let startIdx = -1;
  for (let i = parts.length - 1; i >= 0 && li >= 0; i--) {
    const f = fold(parts[i].w).replace(/[^a-z0-9]/g, '');
    if (!f) continue;
    if (ABBR_SKIP.has(f)) continue;
    if (f[0] !== letters[li]) return null;
    li--;
    startIdx = parts[i].idx;
  }
  if (li >= 0 || startIdx < 0) return null;
  const long = words.slice(startIdx).join(' ').replace(/[,;:.]+$/, '').trim();
  return long.length >= 4 && long.length <= 70 ? long : null;
}

export function buildQueryIntelPack(opts: BuildOptions): BuildResult {
  const log = opts.log || (() => {});
  const root = opts.projectRoot;
  const chunksPath = opts.chunksPath || path.join(root, 'data', 'local_rag_chunks.json');
  const outDir = opts.outDir || path.join(root, 'data', 'search');
  const jsonPath = path.join(outDir, 'query-intel.json');
  const binPath = path.join(outDir, 'query-intel.bin');
  const t0 = Date.now();

  const chunks = readJson<any[]>(chunksPath) || [];
  if (chunks.length < 100) throw new Error(`derlem boş ya da okunamadı: ${chunksPath}`);
  let totalLen = 0;
  for (const c of chunks) totalLen += (c.content || '').length;
  const src = lexiconSources(root);
  const signature = [PACK_VERSION, BUILDER_REV, chunks.length, totalLen, ...Object.values(src).map(mtimeOf)].join(':');
  const prev = readJson<QueryIntelPackJson>(jsonPath);
  if (!opts.force && prev && prev.signature === signature && fs.existsSync(binPath)) {
    log(`[query-intel] imza aynı, atlandı (${signature})`);
    return { skipped: true, signature, stats: prev.stats || {}, jsonPath, binPath };
  }
  log(`[query-intel] derlem ${chunks.length} parça okundu (${Date.now() - t0} ms)`);

  // ---- 1) kavramlar + başlık kavramları
  const concepts = buildConcepts(root);
  const topicCount = new Map<string, { label: string; n: number; disc: string }>();
  for (const c of chunks) {
    if (c.documentType === 'ai_qa' || c.documentType === 'ai_refinement') continue;
    if (!['lecture_slide', 'summary', 'deck_slide'].includes(c.documentType)) continue;
    const t = topicFromTitle(c.title);
    if (!t) continue;
    const k = fold(t);
    const e = topicCount.get(k);
    if (e) e.n++; else topicCount.set(k, { label: t, n: 1, disc: c.discipline || '' });
  }
  const conceptKeys = new Set(concepts.map((c) => fold(c.label)));
  for (const [k, e] of topicCount) {
    if (e.n < 3 || conceptKeys.has(k)) continue;
    let label = e.label.replace(/^['"“”‘’]+|['"“”‘’.]+$/g, '').trim();
    if (label === label.toLocaleUpperCase('tr-TR')) {
      label = label.toLocaleLowerCase('tr-TR').replace(/(^|\s)(\p{L})/gu, (_m, sp, ch) => sp + ch.toLocaleUpperCase('tr-TR')).replace(/\b(Ve|İle|Veya)\b/gu, (w) => w.toLocaleLowerCase('tr-TR'));
    }
    concepts.push({ label, type: 'topic', ref: `topic:${label}`, aliases: new Map(), discipline: e.disc, mentions: 0 });
  }
  log(`[query-intel] ${concepts.length} kavram`);

  // ---- 2) sözcük sıklıkları + yüzey biçimleri + kavram anma sayıları
  const matcher = new PhraseMatcher();
  concepts.forEach((c, i) => { matcher.add(c.label, i); for (const a of c.aliases.keys()) matcher.add(a, i); });
  const df = new Map<string, number>();
  const surfaces = new Map<string, Map<string, number>>();
  const upperCount = new Map<string, number>();
  const cleaned: string[] = new Array(chunks.length);
  const NGRAM_TYPES = new Set(['past_question', 'ornek_question', 'lecture_slide', 'summary', 'deck_slide', 'transcript', 'deepseek_contribution', 'active_question', 'user_contribution']);
  const seenInDoc = new Set<string>();
  const abbr = new Map<string, Map<string, { surface: string; n: number }>>();
  for (let ci = 0; ci < chunks.length; ci++) {
    const c = chunks[ci];
    if (c.documentType === 'ai_qa' || c.documentType === 'ai_refinement') continue;
    const text = cleanContent(c.content || '');
    if (NGRAM_TYPES.has(c.documentType)) cleaned[ci] = text;
    const spans = splitWords(text);
    seenInDoc.clear();
    for (const s of spans) {
      if (s.f.length < 2 || s.f.length > 30 || !/[a-z]/.test(s.f)) continue;
      if (!seenInDoc.has(s.f)) { seenInDoc.add(s.f); df.set(s.f, (df.get(s.f) || 0) + 1); }
      const low = s.w.toLocaleLowerCase('tr-TR');
      let m = surfaces.get(s.f);
      if (!m) { m = new Map(); surfaces.set(s.f, m); }
      m.set(low, (m.get(low) || 0) + 1);
      if (s.w.length >= 2 && s.w.length <= 6 && s.w === s.w.toLocaleUpperCase('tr-TR') && s.w !== low) upperCount.set(s.f, (upperCount.get(s.f) || 0) + 1);
    }
    for (const m of matcher.scan(spans)) for (const id of m.ids) concepts[id].mentions++;
    if (text.includes('(')) {
      ABBR_RE.lastIndex = 0;
      let am: RegExpExecArray | null;
      while ((am = ABBR_RE.exec(text))) {
        const long = abbreviationLongForm(am[1], am[2]);
        if (!long) continue;
        const acr = am[2];
        const lk = fold(long).replace(/[^a-z0-9]+/g, ' ').trim();
        let m = abbr.get(acr);
        if (!m) { m = new Map(); abbr.set(acr, m); }
        const e = m.get(lk);
        if (e) e.n++; else m.set(lk, { surface: long, n: 1 });
      }
    }
  }
  // Kısaltmaları kavramlara bağla: ≥2 kez görülen uzun biçim; tek anlamlıysa (pay ≥ %75) güçlü takma ad
  const keyOfC = (x: string) => fold(x).replace(/\s*\([^)]*\)\s*/g, ' ').replace(/[^a-z0-9]+/g, ' ').trim();
  const conceptByKey = new Map<string, MutConcept>();
  for (const c of concepts) {
    conceptByKey.set(keyOfC(c.label), c);
    for (const a of c.aliases.keys()) if (!conceptByKey.has(keyOfC(a))) conceptByKey.set(keyOfC(a), c);
  }
  let abbrLinked = 0;
  let abbrNew = 0;
  for (const [acr, forms] of abbr) {
    const total = [...forms.values()].reduce((a, e) => a + e.n, 0);
    for (const [lk, e] of forms) {
      if (e.n < 2) continue;
      const strong = e.n / total >= 0.75;
      let c = conceptByKey.get(lk);
      if (!c) {
        if (e.n < 3) continue;
        const label = e.surface === e.surface.toLocaleUpperCase('tr-TR')
          ? e.surface.toLocaleLowerCase('tr-TR').replace(/(^|\s)(\p{L})/gu, (_m, sp, ch) => sp + ch.toLocaleUpperCase('tr-TR'))
          : e.surface.charAt(0).toLocaleUpperCase('tr-TR') + e.surface.slice(1);
        c = { label, type: 'term', ref: '', aliases: new Map(), discipline: '', mentions: e.n };
        concepts.push(c);
        conceptByKey.set(lk, c);
        abbrNew++;
      }
      if (!c.aliases.has(acr)) { c.aliases.set(acr, strong); abbrLinked++; }
    }
  }
  log(`[query-intel] sözcük sıklıkları: ${df.size} farklı; kısaltma: ${abbr.size} aday, ${abbrLinked} bağlandı, ${abbrNew} yeni kavram (${Date.now() - t0} ms)`);

  // Kavram sözcükleri derlemde nadir olsa da sözlüğe girer (öneri ve düzeltme hedefi olabilsinler)
  const conceptWords = new Map<string, string>();
  for (const c of concepts) for (const n of [c.label, ...c.aliases.keys()]) for (const s of splitWords(n)) if (!conceptWords.has(s.f)) conceptWords.set(s.f, s.w.toLocaleLowerCase('tr-TR'));
  const VOWEL = /[aeiou]/;
  const keep: string[] = [];
  for (const [f, n] of df) {
    const isConcept = conceptWords.has(f);
    if (n < (isConcept ? 1 : 3)) continue;
    if (/(.)\1\1/.test(f)) continue;
    // Kodlama bozulması (UTF-8'in Latin-1 okunması: "aåÿaäÿä", "ÄŸÄ") ve Latin dışı yazı sözlüğe girmez
    if (/[ãåÿ¤ð\u0590-\u06FF]/.test(f)) continue;
    const upper = (upperCount.get(f) || 0) / Math.max(1, [...(surfaces.get(f)?.values() || [])].reduce((a, b) => a + b, 0));
    if (!VOWEL.test(f) && f.length >= 4 && upper < 0.6 && !isConcept) continue;
    keep.push(f);
  }
  // Etiket sözcükleri derlemde hiç yoksa da ekle
  for (const f of conceptWords.keys()) if (!df.has(f) && f.length >= 2 && /[a-z]/.test(f)) { df.set(f, 1); keep.push(f); }
  keep.push('?');
  keep.sort();
  const words: string[] = [];
  const freq: number[] = [];
  const share: number[] = [];
  const acr: number[] = [];
  const idOf = new Map<string, number>();
  for (const f of keep) {
    const id = words.length;
    idOf.set(f, id);
    if (f === '?') { words.push('?'); freq.push(0); share.push(100); continue; }
    const m = surfaces.get(f);
    let best = f;
    let bn = 0;
    let tot = 0;
    if (m) for (const [w, k] of m) { tot += k; if (k > bn) { bn = k; best = w; } }
    else best = conceptWords.get(f) || f; // yalnız sözlükten gelen sözcük: sözlükteki yazım
    const up = upperCount.get(f) || 0;
    // Kısaltma: neredeyse hep büyük harfle yazılan kısa sözcük (VHL, ANCA, CD4); başlık sözcükleri (YANLIŞ, SPOTU) değil
    const vowels = (f.match(/[aeiou]/g) || []).length;
    if (tot >= 3 && up / tot >= 0.85 && (f.length <= 4 || /\d/.test(f) || vowels <= 1)) { acr.push(id); best = best.toLocaleUpperCase('tr-TR'); }
    words.push(best);
    freq.push(df.get(f) || 0);
    share.push(tot ? Math.round((bn / tot) * 100) : 100);
  }
  log(`[query-intel] sözlük: ${words.length} sözcük (${acr.length} kısaltma)`);

  // ---- 3) SymSpell (önek 8, tek silme) — özet + id çiftleri Float64 ile tek seferde sıralanır
  const pairs: number[] = [];
  const keySet = new Set<string>();
  for (let i = 0; i < keep.length; i++) {
    const f = keep[i];
    if (f.length < 3) continue;
    keySet.clear();
    deleteKeys(f, keySet);
    for (const k of keySet) pairs.push(fnv1a(k) * 0x100000 + i);
  }
  const sorted = Float64Array.from(pairs).sort();
  const symHash = new Uint32Array(sorted.length);
  const symId = new Int32Array(sorted.length);
  for (let j = 0; j < sorted.length; j++) {
    const h = Math.floor(sorted[j] / 0x100000);
    symHash[j] = h;
    symId[j] = sorted[j] - h * 0x100000;
  }
  log(`[query-intel] SymSpell: ${symHash.length} anahtar (önek ${SYM_PREFIX})`);

  // ---- 4) n-gram (ikili + üçlü bağlam → sonraki sözcük)
  const bi = new Map<number, number>();
  const tri = new Map<number, number>();
  const SENT_SPLIT = /(?<=[.!?…])\s+|\n+|;\s*/;
  const ctxHash = new Map<string, number>();
  const hashCtx = (s: string) => { let h = ctxHash.get(s); if (h === undefined) { h = fnv1a(s); if (ctxHash.size < 3_000_000) ctxHash.set(s, h); } return h; };
  const qId = idOf.get('?')!;
  for (const text of cleaned) {
    if (!text) continue;
    for (const sent of text.split(SENT_SPLIT)) {
      const t = sent.trim();
      if (t.length < 8) continue;
      const sp = splitWords(t);
      const ids: number[] = [];
      const fs_: string[] = [];
      for (const s of sp) { ids.push(idOf.get(s.f) ?? -1); fs_.push(s.f); }
      if (t.endsWith('?')) { ids.push(qId); fs_.push('?'); }
      for (let i = 1; i < ids.length; i++) {
        const nx = ids[i];
        if (nx < 0) continue;
        if (ids[i - 1] >= 0) {
          const k = hashCtx(fs_[i - 1]) * 0x100000 + nx;
          bi.set(k, (bi.get(k) || 0) + 1);
          if (i >= 2 && ids[i - 2] >= 0) {
            const k3 = hashCtx(`${fs_[i - 2]} ${fs_[i - 1]}`) * 0x100000 + nx;
            tri.set(k3, (tri.get(k3) || 0) + 1);
          }
        }
      }
    }
  }
  ctxHash.clear();
  log(`[query-intel] n-gram sayımı: ikili ${bi.size}, üçlü ${tri.size} (${Date.now() - t0} ms)`);

  // Budama: sayım ≥ 2, bağlam başına en çok K sonraki sözcük; ikili ve üçlü bağlamlar aynı tabloda (özetleri farklı)
  const ctxMap = new Map<number, Array<[number, number]>>();
  const collect = (m: Map<number, number>, K: number, minCount: number) => {
    for (const [k, n] of m) {
      if (n < minCount) continue;
      const h = Math.floor(k / 0x100000);
      const id = k - h * 0x100000;
      let arr = ctxMap.get(h);
      if (!arr) { arr = []; ctxMap.set(h, arr); }
      arr.push([id, n]);
    }
    m.clear();
    for (const arr of ctxMap.values()) if (arr.length > K) { arr.sort((a, b) => b[1] - a[1]); arr.length = K; }
  };
  collect(tri, 6, 2);
  collect(bi, 10, 2);
  const ctxList = [...ctxMap.entries()].filter(([, arr]) => arr.reduce((a, x) => a + x[1], 0) >= 3).sort((a, b) => a[0] - b[0]);
  const ngHash = new Uint32Array(ctxList.length);
  const ngStart = new Uint32Array(ctxList.length + 1);
  let k = 0;
  for (const [, arr] of ctxList) k += Math.min(arr.length, 10);
  const ngNext = new Int32Array(k);
  const ngCount = new Uint16Array(k);
  let p = 0;
  ctxList.forEach(([h, arr], i) => {
    arr.sort((a, b) => b[1] - a[1]);
    ngHash[i] = h;
    ngStart[i] = p;
    for (const [id, n] of arr.slice(0, 10)) { ngNext[p] = id; ngCount[p] = Math.min(65535, n); p++; }
  });
  ngStart[ctxList.length] = p;
  log(`[query-intel] n-gram: ${ngHash.length} bağlam, ${p} geçiş`);

  // ---- 5) yaz
  // Tamlayan ekli tek sözcük ("Tümörün"): kökü derlemde çok daha sıksa çekimli biçimdir (heparin ≠ hepar+in)
  const inflected = (c: MutConcept) => {
    const f = fold(c.label);
    if (f.includes(' ') || c.ref.startsWith('disease:')) return false;
    const m = f.match(/^(.{4,}?)(nin|nun|in|un)$/);
    return Boolean(m && (df.get(m[1]) || 0) > 2 * (df.get(f) || 0) + 5);
  };
  const packedConcepts: PackedConcept[] = concepts
    .filter((c) => !inflected(c))
    .map((c) => {
      const aliases = [...c.aliases.entries()].slice(0, 15);
      let mask = 0;
      aliases.forEach(([, strong], i) => { if (strong) mask |= 1 << i; });
      const weight = Math.round(Math.min(3, Math.log10(1 + c.mentions)) * 100) / 100;
      return [c.label, c.type, c.ref, weight, aliases.map(([a]) => a), c.discipline, mask];
    });
  const stats = {
    chunks: chunks.length, words: words.length, acronyms: acr.length, concepts: packedConcepts.length,
    symKeys: symHash.length, ngContexts: ngHash.length, ngEdges: p, buildMs: Date.now() - t0,
  };
  const pack: QueryIntelPackJson = { v: PACK_VERSION, builtAt: new Date().toISOString(), signature, words, freq, share, acr, concepts: packedConcepts, stats };
  fs.mkdirSync(outDir, { recursive: true });
  const bin = encodeBins({ symHash, symId, ngHash, ngStart, ngNext, ngCount });
  // Önce .bin, sonra .json (json imzayı taşır; yarım yazımda eski json eski bin ile kalmasın diye ikisi de geçici adla)
  fs.writeFileSync(binPath + '.tmp', bin);
  fs.writeFileSync(jsonPath + '.tmp', JSON.stringify(pack));
  fs.renameSync(binPath + '.tmp', binPath);
  fs.renameSync(jsonPath + '.tmp', jsonPath);
  log(`[query-intel] yazıldı: ${(bin.length / 1e6).toFixed(1)} MB bin + ${(fs.statSync(jsonPath).size / 1e6).toFixed(1)} MB json (${stats.buildMs} ms)`);
  return { skipped: false, signature, stats, jsonPath, binPath };
}
