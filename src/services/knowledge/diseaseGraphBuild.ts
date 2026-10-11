/**
 * Hastalık bilgi grafiği derleyicisi (yalnız Node, ayrı süreçte; scripts/search/build-query-intel.mts çağırır).
 *
 * GraphRAG'in hafif ve yerel karşılığı: LLM yok, her çalıştırmada aynı sonuç, ~1 dk CPU.
 *  1) Düğümler: hastalıklar (diseases.json) + sorgu zekâsı paketindeki kavramlar (ilaç, gen, bulgu, patojen…)
 *  2) Derlemdeki her ders/soru cümlesinde hastalık adları ve kavramlar aranır (ek toleranslı eşleyici)
 *  3) Hastalık geçen cümle bölümüne göre sınıflanır → bölüm başına en iyi kanıtlar (kaynak künyesiyle)
 *  4) Aynı cümlede geçen kavram/hastalık → kenar; ağırlık = birlikte geçiş × idf (yaygın kavram sönümlenir)
 *  5) Denetim: profil alanı dolgu/şablon mu, boş mu, kanıtla güncellenebilir mi → öncelik puanı
 * Çıktı: data/knowledge/disease_graph.json. diseases.json'a YAZMAZ (doğrulanmamış veri veritabanına girmez);
 * öneriler yönetici/öğrenci incelemesine sunulur.
 */
import fs from 'fs';
import path from 'path';
import { PhraseMatcher, fold, splitWords, type IntentKey } from '../queryIntel/core';
import type { QueryIntelPackJson } from '../queryIntel/engine';
import { toFlatView } from '../diseaseModel';
import {
  EvidenceBucket, SECTION_FIELD, SOURCE_TIER, maskSig, placeholderSignatures, sectionsOf, sentenceQuality, splitSentences,
  type Evidence, type SectionKey,
} from './evidence';

const GRAPH_REV = 4;

export const PROFILE_SECTIONS: IntentKey[] = ['symptoms', 'pathognomonic', 'etiology', 'physiology', 'pathology', 'diagnosis', 'imaging', 'treatment', 'epidemiology'];

/** Elle bilinen dolgu kalıpları (tekrar sayısına bakmadan) */
const GENERIC_PATTERNS = [
  /^standart medikal protokol/, /^laboratuvar incelemeleri ve klinik/, /^radyolojik goruntuleme ve/, /tablosuna ozgu akut veya kronik/,
  /altta yatan tetikleyici genetik ve cevresel/, /^karakteristik histopatolojik doku/, /^hucresel duzeyde fizyopatolojik/,
  /ders mufredati kapsaminda ele alinmistir/, /^toplumda yas ve cinsiyet/, /klinik ve histopatolojik ayirici tani$/,
];

export type FieldStatus = 'ok' | 'placeholder' | 'empty';

export interface DiseaseAudit {
  fields: Partial<Record<IntentKey, FieldStatus>>;
  completeness: number;
  /** Dolgu/boş olup derlemde kanıtı bulunan bölümler (güncellenebilir) */
  updatable: IntentKey[];
  flags: string[];
  /** Güncelleme önceliği (yüksek = önce ele alınmalı): eksik alan × kanıt × anılma */
  priority: number;
}

export interface DiseaseNode {
  id: string;
  name: string;
  category: string;
  mentions: number;
  byType: Record<string, number>;
  sources: Array<{ title: string; type: string; n: number }>;
  evidence: Partial<Record<SectionKey, Evidence[]>>;
  related: Array<{ label: string; type: string; ref: string; w: number }>;
  relatedDiseases: Array<{ id: string; name: string; w: number; ddx: boolean }>;
  audit: DiseaseAudit;
}

export interface DiseaseGraph {
  v: number;
  builtAt: string;
  signature: string;
  stats: Record<string, number>;
  summary: {
    fieldStatus: Record<string, Record<FieldStatus, number>>;
    placeholderRate: number;
    noEvidence: number;
    duplicates: Array<{ key: string; ids: string[] }>;
    topPriority: Array<{ id: string; name: string; priority: number; updatable: number }>;
  };
  diseases: Record<string, DiseaseNode>;
}

function readJson<T = any>(p: string): T | null {
  try { return JSON.parse(fs.readFileSync(p, 'utf-8')) as T; } catch { return null; }
}
function mtimeOf(p: string): number {
  try { return Math.round(fs.statSync(p).mtimeMs); } catch { return 0; }
}

/** Hastalık adının arama takma adları: ad, parantezsiz ad, parantez içi kısaltma (≥3 harf), Latince ad, ansiklopedi takma adları */
export function diseaseAliases(d: any, enc?: any): string[] {
  const out = new Set<string>();
  const name = String(d.name || '').trim();
  if (!name) return [];
  out.add(name);
  const bare = name.replace(/\s*\([^)]*\)\s*/g, ' ').replace(/\s+/g, ' ').trim();
  if (bare.length >= 4) out.add(bare);
  const m = name.match(/\(([^)]{2,40})\)/);
  if (m) for (const p of m[1].split(/[\/,;]| ve /)) { const t = p.trim(); if (t.length >= 3) out.add(t); }
  if (d.latinName && String(d.latinName).length >= 4) out.add(String(d.latinName));
  for (const a of d.altNames || []) { const t = String(a).replace(/\s*\([^)]*\)\s*/g, ' ').replace(/\s+/g, ' ').trim(); if (t.length >= 4) out.add(t); }
  for (const a of enc?.aliases || []) if (String(a).length >= 3) out.add(String(a));
  // Çok genel tek sözcüklü adlar (≤4 harf, kısaltma değil) eşleşmeyi bozar
  return [...out].filter((a) => !(a.split(/\s+/).length === 1 && a.length <= 4 && a !== a.toLocaleUpperCase('tr-TR')));
}

export function auditFields(d: any, placeholders: Set<string>): Partial<Record<IntentKey, FieldStatus>> {
  const res: Partial<Record<IntentKey, FieldStatus>> = {};
  for (const sec of PROFILE_SECTIONS) {
    const v = d[SECTION_FIELD[sec]];
    const items = (Array.isArray(v) ? v : v ? [v] : []).map((x: any) => String(x || '').trim()).filter(Boolean);
    if (!items.length) { res[sec] = 'empty'; continue; }
    const real = items.filter((s: string) => {
      const sig = maskSig(s, d.name);
      if (placeholders.has(sig)) return false;
      const f = fold(s);
      return !GENERIC_PATTERNS.some((re) => re.test(f)) && s.length >= 15;
    });
    res[sec] = real.length ? 'ok' : 'placeholder';
  }
  return res;
}

export interface GraphBuildOptions { projectRoot: string; force?: boolean; log?: (m: string) => void }

export function buildDiseaseGraph(opts: GraphBuildOptions): { skipped: boolean; stats: Record<string, number>; outPath: string } {
  const log = opts.log || (() => {});
  const root = opts.projectRoot;
  const t0 = Date.now();
  const chunksPath = path.join(root, 'data', 'local_rag_chunks.json');
  const diseasesPath = path.join(root, 'src', 'data', 'diseases.json');
  const encPath = path.join(root, 'src', 'data', 'medical_encyclopedia.json');
  const packPath = path.join(root, 'data', 'search', 'query-intel.json');
  const outPath = path.join(root, 'data', 'knowledge', 'disease_graph.json');

  const pack = readJson<QueryIntelPackJson>(packPath);
  const signature = [GRAPH_REV, pack?.signature || '-', mtimeOf(diseasesPath), mtimeOf(encPath)].join('|');
  const prev = readJson<DiseaseGraph>(outPath);
  if (!opts.force && prev && prev.signature === signature) {
    log('[disease-graph] imza aynı, atlandı');
    return { skipped: true, stats: prev.stats, outPath };
  }

  // Şema 2 (yapılandırılmış maddeler) → denetim/eşleyicinin kullandığı düz alan görünümü
  const diseases = (readJson<any[]>(diseasesPath) || []).map(toFlatView);
  const enc = new Map<string, any>((readJson<any[]>(encPath) || []).map((e) => [e.id, e]));
  const chunks = readJson<any[]>(chunksPath) || [];
  if (!diseases.length || chunks.length < 100) throw new Error('hastalık ya da derlem verisi yok');

  // ---- eşleyiciler: hastalıklar (0..D-1) + kavramlar (D..)
  const D = diseases.length;
  const matcher = new PhraseMatcher();
  diseases.forEach((d, i) => { for (const a of diseaseAliases(d, enc.get(d.id))) matcher.add(a, i); });
  const concepts = (pack?.concepts || []).filter((c) => c[1] !== 'topic' && !String(c[2]).startsWith('disease:'));
  concepts.forEach((c, j) => {
    matcher.add(c[0], D + j);
    c[4].forEach((a, ai) => { if (c[6] & (1 << ai)) matcher.add(a, D + j); });
  });
  log(`[disease-graph] ${D} hastalık, ${concepts.length} kavram düğümü (${matcher.size} ad)`);

  const buckets = diseases.map(() => new EvidenceBucket(6));
  const mentions = new Int32Array(D);
  const byType = diseases.map(() => new Map<string, number>());
  const srcCount = diseases.map(() => new Map<string, { title: string; type: string; n: number }>());
  const coC = diseases.map(() => new Map<number, number>()); // kavram kenarları
  const coD = diseases.map(() => new Map<number, number>()); // hastalık kenarları
  const ddx = diseases.map(() => new Set<number>());
  const conceptSentFreq = new Map<number, number>();
  let sentences = 0;

  for (const ch of chunks) {
    const tier = SOURCE_TIER[ch.documentType];
    if (!tier) continue;
    for (const s of splitSentences(ch.content || '')) {
      const spans = splitWords(s);
      const hits = matcher.scan(spans);
      if (!hits.length) continue;
      sentences++;
      const dIds = new Set<number>();
      const cIds = new Set<number>();
      for (const h of hits) {
        const raw = s.slice(spans[h.from].s, spans[h.to - 1].e);
        // ≤3 harflik eşleşme yalnız büyük harfle yazılmışsa (kısaltma) kabul
        if (raw.length <= 3 && raw !== raw.toLocaleUpperCase('tr-TR')) continue;
        for (const id of h.ids) (id < D ? dIds : cIds).add(id);
      }
      for (const c of cIds) conceptSentFreq.set(c, (conceptSentFreq.get(c) || 0) + 1);
      if (!dIds.size) continue;
      const q = sentenceQuality(s);
      const secs = q > 0 ? sectionsOf(s) : [];
      const isDdx = /ayırıcı tanı|ayirici tani|karışır|ayırt edil/i.test(s);
      for (const d of dIds) {
        mentions[d]++;
        byType[d].set(ch.documentType, (byType[d].get(ch.documentType) || 0) + 1);
        const title = String(ch.title || '').replace(/\s*\((?:Sayfa|Slayt)[^)]*\)/giu, '').slice(0, 90);
        const sk = `${ch.documentType}|${title}`;
        const sc = srcCount[d].get(sk);
        if (sc) sc.n++; else srcCount[d].set(sk, { title, type: ch.documentType, n: 1 });
        for (const c of cIds) coC[d].set(c, (coC[d].get(c) || 0) + 1);
        for (const o of dIds) if (o !== d) { coD[d].set(o, (coD[d].get(o) || 0) + 1); if (isDdx) ddx[d].add(o); }
        // Kanıt: birden çok hastalık geçen cümle o hastalıklar için daha az özgül
        const spec = 1 / Math.sqrt(dIds.size);
        for (const [sec, w] of secs) {
          buckets[d].add({
            t: s,
            section: sec,
            score: Math.round((q * tier * spec * (sec === 'general' ? 0.5 : 1 + Math.min(w, 6) / 6)) * 1000) / 1000,
            src: { type: ch.documentType, title, chunkId: ch.id, committee: ch.committeeId, discipline: ch.discipline },
          });
        }
      }
    }
  }
  log(`[disease-graph] ${sentences} eşleşen cümle (${Date.now() - t0} ms)`);

  // ---- denetim + düğümler
  const placeholders = placeholderSignatures(diseases, PROFILE_SECTIONS.map((s) => SECTION_FIELD[s]));
  const nodes: Record<string, DiseaseNode> = {};
  const fieldStatus: Record<string, Record<FieldStatus, number>> = {};
  let phCount = 0;
  let total = 0;
  let noEvidence = 0;
  diseases.forEach((d, i) => {
    const fields = auditFields(d, placeholders);
    const updatable: IntentKey[] = [];
    let ok = 0;
    for (const sec of PROFILE_SECTIONS) {
      const st = fields[sec]!;
      (fieldStatus[sec] ||= { ok: 0, placeholder: 0, empty: 0 })[st]++;
      total++;
      if (st === 'ok') ok++; else { phCount++; if (buckets[i].count(sec) > 0) updatable.push(sec); }
    }
    const flags: string[] = [];
    if (!d.icd_code) flags.push('icd-yok');
    if (!d.source_notes_summary) flags.push('ders-notu-ozeti-yok');
    if (mentions[i] === 0) { flags.push('derlemde-gecmiyor'); noEvidence++; }
    if (!(d.relatedLectures || []).length) flags.push('ders-baglantisi-yok');
    const completeness = Math.round((ok / PROFILE_SECTIONS.length) * 100) / 100;
    const priority = Math.round((1 - completeness) * 50 + updatable.length * 6 + Math.min(30, Math.log2(1 + mentions[i]) * 3));

    const N = Math.max(1, sentences);
    const related = [...coC[i].entries()]
      .map(([c, n]) => ({ c, w: n * Math.log(N / (1 + (conceptSentFreq.get(c) || 0))) }))
      .filter((x) => x.w > 0)
      .sort((a, b) => b.w - a.w)
      .slice(0, 16)
      .map(({ c, w }) => { const p = concepts[c - D]; return { label: p[0], type: p[1], ref: p[2], w: Math.round(w * 10) / 10 }; });
    const relatedDiseases = [...coD[i].entries()]
      .map(([o, n]) => ({ o, w: n * Math.log(N / (1 + mentions[o])) * (ddx[i].has(o) ? 2 : 1) }))
      .filter((x) => x.w > 0)
      .sort((a, b) => b.w - a.w)
      .slice(0, 10)
      .map(({ o, w }) => ({ id: diseases[o].id, name: diseases[o].name, w: Math.round(w * 10) / 10, ddx: ddx[i].has(o) }));

    nodes[d.id] = {
      id: d.id,
      name: d.name,
      category: d.category || '',
      mentions: mentions[i],
      byType: Object.fromEntries(byType[i]),
      sources: [...srcCount[i].values()].sort((a, b) => b.n - a.n).slice(0, 8),
      evidence: buckets[i].toJSON(),
      related,
      relatedDiseases,
      audit: { fields, completeness, updatable, flags, priority },
    };
  });

  // Olası kopya profiller: yalın adı aynı ya da biri ötekinin başı olan ("Botulizm" ~ "Botulizm (besin kaynaklı)")
  const bareKey = (n: string) => fold(n.replace(/\s*\([^)]*\)/g, ' ')).replace(/[^a-z0-9]+/g, ' ').trim();
  const byBare = new Map<string, string[]>();
  for (const d of diseases) {
    const k = bareKey(d.name);
    if (k.length < 4) continue;
    (byBare.get(k) || byBare.set(k, []).get(k)!).push(d.id);
  }
  const duplicates: Array<{ key: string; ids: string[] }> = [];
  for (const [k, ids] of byBare) {
    if (ids.length > 1) duplicates.push({ key: k, ids });
  }
  for (const g of duplicates) for (const id of g.ids) nodes[id]?.audit.flags.push(`olasi-kopya:${g.ids.filter((x) => x !== id).join(',')}`);

  const topPriority = Object.values(nodes)
    .sort((a, b) => b.audit.priority - a.audit.priority)
    .slice(0, 40)
    .map((n) => ({ id: n.id, name: n.name, priority: n.audit.priority, updatable: n.audit.updatable.length }));
  const graph: DiseaseGraph = {
    v: GRAPH_REV,
    builtAt: new Date().toISOString(),
    signature,
    stats: { diseases: D, concepts: concepts.length, sentences, placeholders: placeholders.size, buildMs: Date.now() - t0 },
    summary: { fieldStatus, placeholderRate: Math.round((phCount / Math.max(1, total)) * 1000) / 1000, noEvidence, duplicates, topPriority },
    diseases: nodes,
  };
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath + '.tmp', JSON.stringify(graph));
  fs.renameSync(outPath + '.tmp', outPath);
  log(`[disease-graph] yazıldı: ${(fs.statSync(outPath).size / 1e6).toFixed(1)} MB · dolgu/boş alan oranı %${(graph.summary.placeholderRate * 100).toFixed(0)} · derlemde geçmeyen ${noEvidence} (${Date.now() - t0} ms)`);
  return { skipped: false, stats: graph.stats, outPath };
}
