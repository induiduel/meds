/**
 * Taslak stüdyosu · AI ile dönüştür (yalnız sunucu).
 *
 * Bir soru adayının parçalarını kaynaklara dayandırarak tam soruya çevirir:
 *  - "cloud": generateResilientMedicalAi (Gemini anahtar havuzu → Groq → yedekler)
 *  - Yerel Ollama modelleri: alternatif soru üretir (sırayla, tek seferde bir model)
 *  - bge-m3 (gömme modeli): metin üretmez; kaynakları anlam benzerliğiyle yeniden sıralar
 *
 * Kurallar (CLAUDE.md "Grounding"): kaynak findSourcesForQuestion ile bulunur,
 * formatSourcesForPrompt ile isteme konur, model usedSources döndürür, toSourceRef ile geri verilir.
 */
import { generateResilientMedicalAi } from './aiProvider.ts';
import { findSourcesForQuestion, formatSourcesForPrompt, toSourceRef } from './ragService.ts';

const OLLAMA_URL = (process.env.OLLAMA_URL || 'http://localhost:11434').replace(/\/$/, '');

/** Yerelde soru yazdırılacak modeller (env ile değiştirilebilir). */
export const STUDIO_LOCAL_MODELS: string[] = (process.env.STUDIO_LOCAL_MODELS ||
  'medgemma1.5:4b,qwen3-vl:8b,deepseek-r1:1.5b-qwen-distill-q8_0,qwen3:1.7b-q8_0')
  .split(',')
  .map((s) => s.trim())
  .filter(Boolean);
export const STUDIO_EMBED_MODEL = process.env.STUDIO_EMBED_MODEL || 'bge-m3:latest';

export interface StudioAiInput {
  committeeId?: string;
  discipline?: string;
  topic?: string;
  stem?: string;
  options?: Partial<Record<'A' | 'B' | 'C' | 'D' | 'E', string>>;
  answer?: string;
  fragments: { kind: string; text: string }[];
  terms?: string[];
  notes?: string;
}

export interface StudioAiResult {
  target: string;
  label: string;
  ok: boolean;
  error?: string;
  ms: number;
  question?: {
    stem: string;
    options: { key: 'A' | 'B' | 'C' | 'D' | 'E'; text: string }[];
    correctAnswer: 'A' | 'B' | 'C' | 'D' | 'E';
    explanation: string;
    confidence: number;
  };
  sources: ReturnType<typeof toSourceRef>[];
  reranked?: boolean;
}

// ---------------------------------------------------------------- Ollama
async function ollamaTags(): Promise<string[]> {
  try {
    const r = await fetch(`${OLLAMA_URL}/api/tags`, { signal: AbortSignal.timeout(3000) });
    if (!r.ok) return [];
    const j: any = await r.json();
    return (j.models || []).map((m: any) => m.name as string);
  } catch {
    return [];
  }
}

/** Yerel modeller tek GPU/CPU'yu paylaşır: istekleri sıraya koy. */
let ollamaQueue: Promise<unknown> = Promise.resolve();
function queued<T>(fn: () => Promise<T>): Promise<T> {
  const run = ollamaQueue.then(fn, fn);
  ollamaQueue = run.catch(() => undefined);
  return run;
}

async function ollamaChat(model: string, system: string, user: string): Promise<string> {
  return queued(async () => {
    // 8 GB GPU'da modeller birlikte sığmaz: iş bitince boşalt (keep_alive 0), ağ hatasında bir kez daha dene
    const call = () => fetch(`${OLLAMA_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      signal: AbortSignal.timeout(240_000),
      body: JSON.stringify({
        model,
        stream: false,
        format: 'json',
        think: false,
        keep_alive: 0,
        options: { temperature: 0.5, num_ctx: 8192 },
        messages: [
          { role: 'system', content: system },
          { role: 'user', content: user },
        ],
      }),
    });
    let r: Response;
    try {
      r = await call();
    } catch {
      await new Promise((ok) => setTimeout(ok, 1500));
      r = await call();
    }
    if (!r.ok) throw new Error(`Ollama ${r.status}: ${(await r.text()).slice(0, 160)}`);
    const j: any = await r.json();
    return String(j?.message?.content || '');
  });
}

async function embed(texts: string[]): Promise<number[][] | null> {
  try {
    const r = await queued(() =>
      fetch(`${OLLAMA_URL}/api/embed`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        signal: AbortSignal.timeout(60_000),
        body: JSON.stringify({ model: STUDIO_EMBED_MODEL, input: texts }),
      })
    );
    if (!r.ok) return null;
    const j: any = await r.json();
    return Array.isArray(j.embeddings) ? j.embeddings : null;
  } catch {
    return null;
  }
}

const cosine = (a: number[], b: number[]) => {
  let d = 0, na = 0, nb = 0;
  for (let i = 0; i < a.length; i++) {
    d += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  return d / (Math.sqrt(na) * Math.sqrt(nb) || 1);
};

// ---------------------------------------------------------------- kaynaklar
const sourceCache = new Map<string, { at: number; sources: any[]; reranked: boolean }>();

async function groundingFor(input: StudioAiInput) {
  const text = [input.stem, ...input.fragments.map((f) => f.text), ...(input.terms || [])].filter(Boolean).join(' ');
  const key = `${input.committeeId}|${input.discipline}|${text}`.slice(0, 2000);
  const hit = sourceCache.get(key);
  if (hit && Date.now() - hit.at < 10 * 60_000) return hit;
  let sources = await findSourcesForQuestion(
    { committeeId: input.committeeId, discipline: input.discipline, topic: input.topic, fragments: input.fragments.map((f) => ({ text: f.text })) },
    (input.terms || []).join(' '),
    12
  );
  let reranked = false;
  if (sources.length > 1) {
    const vecs = await embed([text, ...sources.map((s: any) => String(s.content || '').slice(0, 1200))]);
    if (vecs && vecs.length === sources.length + 1) {
      const scored = sources.map((s: any, i: number) => ({ s, v: cosine(vecs[0], vecs[i + 1]) }));
      scored.sort((a, b) => b.v - a.v);
      sources = scored.map((x) => x.s);
      reranked = true;
    }
  }
  const out = { at: Date.now(), sources: sources.slice(0, 6), reranked };
  sourceCache.set(key, out);
  return out;
}

// ---------------------------------------------------------------- istem
const SYSTEM = `Sen Türkiye'de tıp fakültesi Dönem 3 kurul sınavı sorularını yeniden kuran bir uzmansın.
Öğrencilerin hatırladığı dağınık parçaları ve verilen fakülte kaynaklarını kullanarak tek, tutarlı,
tek doğru cevaplı, 5 şıklı (A–E) bir çoktan seçmeli soru yazarsın. Türkçe yazarsın.
Kaynakta olmayan bilgi uydurmazsın; parçalarda verilen şıkları ve cevabı korursun.
YALNIZCA geçerli JSON döndürürsün.`;

function buildPrompt(input: StudioAiInput, sourcesText: string, variant: 'primary' | 'alternative') {
  const opts = Object.entries(input.options || {})
    .filter(([, v]) => v && String(v).trim())
    .map(([k, v]) => `${k}) ${v}`)
    .join('\n');
  const frs = input.fragments.map((f, i) => `${i + 1}. [${f.kind}] ${f.text}`).join('\n');
  return `DERS: ${input.discipline || 'Belirtilmedi'}
KONU: ${input.topic || 'Belirtilmedi'}
${input.stem ? `EDİTÖRÜN YAZDIĞI KÖK: ${input.stem}\n` : ''}${opts ? `EDİTÖRÜN ŞIKLARI:\n${opts}\n` : ''}${input.answer ? `İDDİA EDİLEN CEVAP: ${input.answer}\n` : ''}${input.terms?.length ? `ANAHTAR TERİMLER: ${input.terms.join(', ')}\n` : ''}${input.notes ? `EDİTÖR NOTU: ${input.notes}\n` : ''}
ÖĞRENCİ PARÇALARI:
${frs || '(yok)'}

FAKÜLTE KAYNAKLARI (numaralı):
${sourcesText || '(kaynak bulunamadı)'}

GÖREV: ${
    variant === 'primary'
      ? 'Parçalara en sadık, sınavda sorulmuş olması en muhtemel soruyu kur.'
      : 'Aynı bilgiyi ölçen, parçalara dayanan özgün bir ALTERNATİF soru kur (farklı kök ya da çeldiriciler olabilir).'
  }
Şıklar 5 tane olmalı (A–E), tek doğru cevap olmalı. Açıklama 2–4 cümle, kaynağa dayalı.

JSON biçimi:
{"stem":"...","options":[{"key":"A","text":"..."},{"key":"B","text":"..."},{"key":"C","text":"..."},{"key":"D","text":"..."},{"key":"E","text":"..."}],"correctAnswer":"A","explanation":"...","confidence":0-100,"usedSources":[1,2]}`;
}

function parseJson(raw: string): any {
  const cleaned = raw.replace(/<think>[\s\S]*?<\/think>/gi, '').trim();
  try {
    return JSON.parse(cleaned);
  } catch {
    const m = cleaned.match(/\{[\s\S]*\}/);
    if (m) return JSON.parse(m[0]);
    throw new Error('Model geçerli JSON döndürmedi');
  }
}

function normalize(p: any) {
  const keys = ['A', 'B', 'C', 'D', 'E'] as const;
  const raw = Array.isArray(p?.options)
    ? p.options
    : p?.options && typeof p.options === 'object'
      ? Object.entries(p.options).map(([key, text]) => ({ key, text }))
      : [];
  const options = keys.map((k, i) => {
    const o = raw.find((x: any) => String(x?.key || '').toUpperCase() === k) || raw[i];
    return { key: k, text: String(typeof o === 'string' ? o : o?.text || '').replace(/^[A-E]\s*[)\].:-]\s*/, '').trim() };
  });
  const ans = String(p?.correctAnswer || p?.answer || '').trim().toUpperCase().charAt(0);
  if (!String(p?.stem || '').trim()) throw new Error('Model soru kökü üretmedi');
  if (options.filter((o) => o.text).length < 4) throw new Error('Model yeterli şık üretmedi');
  return {
    stem: String(p.stem).trim(),
    options,
    correctAnswer: (keys.includes(ans as any) ? ans : 'A') as (typeof keys)[number],
    explanation: String(p?.explanation || '').trim(),
    confidence: Math.max(0, Math.min(100, Number(p?.confidence) || 0)),
    usedSources: Array.isArray(p?.usedSources) ? p.usedSources.map(Number).filter((n: number) => n > 0) : [],
  };
}

// ---------------------------------------------------------------- dışa açık
export async function listStudioAiModels() {
  const tags = await ollamaTags();
  return {
    cloud: { target: 'cloud', label: 'Bulut AI (Gemini → Groq)', available: true },
    local: STUDIO_LOCAL_MODELS.map((m) => ({ target: m, label: m, available: tags.includes(m) })),
    embed: { model: STUDIO_EMBED_MODEL, available: tags.includes(STUDIO_EMBED_MODEL), role: 'Kaynak sıralama (gömme modeli, soru yazmaz)' },
    ollamaReachable: tags.length > 0,
  };
}

export async function generateStudioQuestion(target: string, input: StudioAiInput): Promise<StudioAiResult> {
  const t0 = Date.now();
  const isCloud = target === 'cloud';
  if (!isCloud && !STUDIO_LOCAL_MODELS.includes(target)) {
    return { target, label: target, ok: false, error: 'Bu model listede yok', ms: 0, sources: [] };
  }
  const g = await groundingFor(input);
  const sourcesText = formatSourcesForPrompt(g.sources, 500);
  const prompt = buildPrompt(input, sourcesText, isCloud ? 'primary' : 'alternative');
  try {
    let raw: string;
    let label = target;
    if (isCloud) {
      const r = await generateResilientMedicalAi({ prompt, systemInstruction: SYSTEM, responseFormat: 'json' });
      raw = r.text;
      label = `Bulut · ${r.providerUsed}`;
    } else {
      raw = await ollamaChat(target, SYSTEM, prompt);
    }
    let q: ReturnType<typeof normalize>;
    try {
      q = normalize(parseJson(raw));
    } catch (first) {
      if (isCloud) throw first;
      // Küçük modeller bazen eksik şık döndürür: biçimi hatırlatıp bir kez daha iste
      raw = await ollamaChat(target, SYSTEM, `${prompt}\n\nÖNCEKİ YANITIN GEÇERSİZDİ (${(first as Error).message}). Tam 5 şık (A, B, C, D, E) ve "stem" içeren JSON döndür.`);
      q = normalize(parseJson(raw));
    }
    const used = q.usedSources.map((n: number) => g.sources[n - 1]).filter(Boolean);
    return {
      target,
      label,
      ok: true,
      ms: Date.now() - t0,
      question: { stem: q.stem, options: q.options, correctAnswer: q.correctAnswer, explanation: q.explanation, confidence: q.confidence },
      sources: (used.length ? used : g.sources.slice(0, 3)).map(toSourceRef),
      reranked: g.reranked,
    };
  } catch (e: any) {
    return { target, label: target, ok: false, error: String(e?.message || e).slice(0, 300), ms: Date.now() - t0, sources: g.sources.slice(0, 3).map(toSourceRef), reranked: g.reranked };
  }
}
