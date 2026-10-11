/**
 * Hastalık bilgi grafiği — sunucu çalışma zamanı (server-only).
 *
 *  - data/knowledge/disease_graph.json (derleyici: diseaseGraphBuild.ts) gecikmeli/asenkron yüklenir, dosya
 *    değişince yeniden okunur.
 *  - getDiseaseInsights(id): kanıtlar (bölüm bölüm, kaynak künyeli), ilişkili kavramlar/hastalıklar, denetim.
 *  - analyzeDiseaseByName(): grafikte olmayan (yeni / kullanıcı eklemesi) hastalık için ANLIK analiz — BM25 ile
 *    en ilgili ~80 parça, aynı cümle sınıflayıcısı. ~20-40 ms, LLM yok.
 */
import fs from 'fs';
import path from 'path';
import { PhraseMatcher, splitWords } from '../queryIntel/core';
import { getQueryIntel } from '../queryIntel/server';
import { EvidenceBucket, SOURCE_TIER, sectionsOf, sentenceQuality, splitSentences } from './evidence';
import { PROFILE_SECTIONS, auditFields, diseaseAliases, type DiseaseGraph, type DiseaseNode } from './diseaseGraphBuild';

const ROOT = path.resolve(process.env.MEDS_APP_DIR || process.cwd());
const GRAPH_PATH = path.join(ROOT, 'data', 'knowledge', 'disease_graph.json');

let graph: DiseaseGraph | null = null;
let mtime = 0;
let loading: Promise<void> | null = null;
let lastStat = 0;

async function load(): Promise<void> {
  try {
    const st = await fs.promises.stat(GRAPH_PATH);
    graph = JSON.parse(await fs.promises.readFile(GRAPH_PATH, 'utf-8'));
    mtime = st.mtimeMs;
  } catch { /* henüz derlenmedi */ }
}

async function getGraph(): Promise<DiseaseGraph | null> {
  const now = Date.now();
  if (!graph && !loading) loading = load().finally(() => { loading = null; });
  else if (graph && !loading && now - lastStat > 30_000) {
    lastStat = now;
    try {
      const st = await fs.promises.stat(GRAPH_PATH);
      if (st.mtimeMs !== mtime) loading = load().finally(() => { loading = null; });
    } catch { /* yok */ }
  }
  if (loading) await loading;
  return graph;
}

export interface DiseaseInsights extends Omit<DiseaseNode, 'audit'> {
  audit: DiseaseNode['audit'] | null;
  builtAt: string | null;
  /** grafikten mi, anlık analizden mi */
  mode: 'graph' | 'live';
}

export async function getDiseaseInsights(id: string): Promise<DiseaseInsights | null> {
  const g = await getGraph();
  const n = g?.diseases[id];
  if (!n) return null;
  return { ...n, builtAt: g!.builtAt, mode: 'graph' };
}

export async function getDiseaseAudit(): Promise<(DiseaseGraph['summary'] & { builtAt: string; stats: DiseaseGraph['stats'] }) | null> {
  const g = await getGraph();
  if (!g) return null;
  return { ...g.summary, builtAt: g.builtAt, stats: g.stats };
}

/** Grafikte olmayan hastalık profili için anlık kanıt + ilişki analizi */
export async function analyzeDiseaseByName(profile: { id?: string; name: string; latinName?: string; aliases?: string[] } & Record<string, any>): Promise<DiseaseInsights> {
  const { searchLocalRag } = await import('../localRagEngine');
  const aliases = [...diseaseAliases(profile), ...(profile.aliases || [])].filter(Boolean);
  const matcher = new PhraseMatcher();
  aliases.forEach((a) => matcher.add(a, 0));
  const hits = await searchLocalRag(aliases.slice(0, 2).join(' '), {
    limit: 80,
    documentTypes: ['lecture_slide', 'summary', 'transcript', 'past_question', 'ornek_question', 'deck_slide'],
  });
  const bucket = new EvidenceBucket(6);
  const byType: Record<string, number> = {};
  const srcs = new Map<string, { title: string; type: string; n: number }>();
  const eng = getQueryIntel();
  const rel = new Map<string, { label: string; type: string; ref: string; w: number }>();
  let mentions = 0;
  for (const h of hits) {
    const tier = SOURCE_TIER[h.documentType] || 1;
    for (const s of splitSentences(h.content)) {
      const spans = splitWords(s);
      if (!matcher.scan(spans).length) continue;
      mentions++;
      byType[h.documentType] = (byType[h.documentType] || 0) + 1;
      const title = String(h.title || '').replace(/\s*\((?:Sayfa|Slayt)[^)]*\)/giu, '').slice(0, 90);
      const k = `${h.documentType}|${title}`;
      const e = srcs.get(k);
      if (e) e.n++; else srcs.set(k, { title, type: h.documentType, n: 1 });
      const q = sentenceQuality(s);
      if (q > 0) {
        for (const [sec, w] of sectionsOf(s)) {
          bucket.add({ t: s, section: sec, score: Math.round(q * tier * (sec === 'general' ? 0.5 : 1 + Math.min(w, 6) / 6) * 1000) / 1000, src: { type: h.documentType, title, chunkId: h.id, committee: h.committeeId, discipline: h.discipline } });
        }
      }
      if (eng) {
        for (const c of eng.detectConcepts(s, spans)) {
          if (!c.ref || c.type === 'topic' || aliases.some((a) => a.toLocaleLowerCase('tr-TR') === c.label.toLocaleLowerCase('tr-TR'))) continue;
          const key = `${c.ref.kind}:${c.ref.id}`;
          const cur = rel.get(key);
          if (cur) cur.w++; else rel.set(key, { label: c.label, type: c.type, ref: key, w: 1 });
        }
      }
    }
  }
  const relatedDiseases = [...rel.values()].filter((r) => r.ref.startsWith('disease:') && r.ref !== `disease:${profile.id}`).sort((a, b) => b.w - a.w).slice(0, 8)
    .map((r) => ({ id: r.ref.slice(8), name: r.label, w: r.w, ddx: false }));
  const related = [...rel.values()].filter((r) => !r.ref.startsWith('disease:')).sort((a, b) => b.w - a.w).slice(0, 14);
  const fields = auditFields(profile, new Set());
  const updatable = PROFILE_SECTIONS.filter((s) => fields[s] !== 'ok' && bucket.count(s) > 0);
  const ok = PROFILE_SECTIONS.filter((s) => fields[s] === 'ok').length;
  return {
    id: profile.id || '',
    name: profile.name,
    category: profile.category || '',
    mentions,
    byType,
    sources: [...srcs.values()].sort((a, b) => b.n - a.n).slice(0, 8),
    evidence: bucket.toJSON(),
    related,
    relatedDiseases,
    audit: { fields, completeness: Math.round((ok / PROFILE_SECTIONS.length) * 100) / 100, updatable, flags: mentions ? [] : ['derlemde-gecmiyor'], priority: 0 },
    builtAt: null,
    mode: 'live',
  };
}

/** Açılışta grafiği gecikmeli ısıt */
export function warmDiseaseGraph(): void {
  setTimeout(() => { getGraph().catch(() => {}); }, 8_000).unref?.();
}

/** Liste ekranı için kompakt kalite haritası: id → [doluluk %, dolgu/boş bölümler, kaynak cümlesi sayısı] */
export async function getDiseaseQualityMap(): Promise<{ builtAt: string; q: Record<string, [number, string[], number]> } | null> {
  const g = await getGraph();
  if (!g) return null;
  const q: Record<string, [number, string[], number]> = {};
  for (const [id, n] of Object.entries(g.diseases)) {
    const weak = Object.entries(n.audit.fields).filter(([, st]) => st !== 'ok').map(([k]) => k);
    q[id] = [Math.round(n.audit.completeness * 100), weak, n.mentions];
  }
  return { builtAt: g.builtAt, q };
}
