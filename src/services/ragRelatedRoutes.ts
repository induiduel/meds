/**
 * Anlamsal ilişki uç noktası (server-only): saklanan bge-m3/e5 vektörlerinden "bununla ilgili ne var?" sorusunu yanıtlar.
 *
 *   GET /api/rag/related?id=<parçaId>                       — doğrudan parça
 *   GET /api/rag/related?type=past_question&doc=<soruId>    — belgenin ilk parçası
 *     &mod=ilgili (varsayılan) | benzer | kopya
 *        ilgili: ders materyali (slayt, özet, deste, hastalık, sözlük, transkript)
 *        benzer: benzer sorular (çıkmış + örnek); kaynak soru değilse aynı türden içerik
 *        kopya : aynı türde neredeyse aynı içerik (benzerlik ≥ 0.93) — kopya/birleştirme adayı
 *     &types=a,b  &kurul=<committeeId>  &limit=8
 *
 * Embed servisi gerekmez (vektör veritabanında); yanıt kısa tutulur (parça başına ≤ 280 karakter özet) ve önbelleğe
 * alınabilir. Yapay zekâ çıktıları (ai_qa, ai_refinement, deepseek) kanıt sayılmadığı için hiçbir modda dönmez.
 */
import type express from 'express';
import fs from 'fs';
import path from 'path';
import { pgDb } from './pgDb';
import { relatedChunks, chunkIdForDocument } from './vectorSearch.ts';
import { notificationLinkFor } from './notificationLinks.ts';

const MATERIAL_TYPES = ['lecture_slide', 'summary', 'deck_slide', 'disease', 'glossary_term', 'transcript'];
const QUESTION_TYPES = ['past_question', 'ornek_question'];
const RELATED_TYPES = [...MATERIAL_TYPES, ...QUESTION_TYPES];
const ALLOWED = new Set([...RELATED_TYPES, 'active_question', 'user_contribution']);

function linkFor(r: Record<string, any>): string | null {
  const m = r.metadata || {};
  switch (r.document_type) {
    case 'past_question':
      return notificationLinkFor({ kind: 'past_question', id: String(r.document_id) });
    case 'ornek_question':
      return notificationLinkFor({ kind: 'ornek_question', id: String(r.document_id) });
    case 'disease':
      return notificationLinkFor({ kind: 'disease', id: String(r.document_id) });
    case 'deck_slide':
      return notificationLinkFor({ kind: 'deck', id: String(m.deckId || r.document_id), slideNumber: Number(m.slideNumber || r.page_number) || undefined });
    default:
      return null;
  }
}

function snippet(content: string): string {
  // Parça başlığı/üst bilgi satırlarını ("[ÇIKMIŞ SINAV SORUSU]", "Ders / Branş: …") atla, asıl metinden başla
  const lines = String(content || '').split('\n').map((l) => l.trim()).filter(Boolean);
  const META = /^(Ders \/ Branş|Ders|Deste|Kurul|Sınav Yılı|Kazanım|Konu \/ Başlık|Konu|Bölüm|Kaynak|Denetim Statüsü|Tür|Zorluk|Slayt \d+)\s*:/;
  const LABEL = /^(Soru Kökü|Soru|Seçenekler|Özet Metin|İçerik|Tanım)\s*:\s*/;
  const body = lines
    .filter((l) => !/^\[.*\]$/.test(l) && !META.test(l))
    .map((l) => l.replace(LABEL, ''))
    .filter(Boolean);
  const text = (body.length ? body : lines)
    .join(' ')
    .replace(/[#*=_`>]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
  return text.length > 280 ? text.slice(0, 277).trimEnd() + '…' : text;
}

let healthCache: { at: number; body: any } | null = null;

export function registerRagRelatedRoutes(app: express.Express) {
  // Vektör sağlığı: tür başına kapsama + son hat raporu (scripts/advanced_ai/rag_vektor_hatti.py). 60 sn önbellek.
  app.get('/api/rag/vectors/health', async (_req, res) => {
    try {
      if (!healthCache || Date.now() - healthCache.at > 60_000) {
        const r = await pgDb.query(
          `select document_type, count(*)::int as toplam, count(embedding_bge_m3)::int as bge_m3, count(embedding_e5)::int as e5,
                  count(*) filter (where embedding_bge_m3 is not null and content_hash_bge_m3 is distinct from content_hash)::int as bge_eski,
                  max(updated_at) as son
             from rag_chunks group by 1 order by 2 desc`,
        );
        let hat: any = null;
        const dbDir = process.env.MEDS_DATABASE_DIR || path.resolve(process.cwd(), '..', 'meds_database');
        try { hat = JSON.parse(fs.readFileSync(path.join(dbDir, 'derived', 'rag_vektor', 'hat_rapor.json'), 'utf-8')); } catch { /* Oracle'da yok */ }
        const rows = r.rows as Array<{ toplam: number; bge_m3: number; e5: number; bge_eski: number }>;
        const sum = (k: 'toplam' | 'bge_m3' | 'e5' | 'bge_eski') => rows.reduce((a, x) => a + x[k], 0);
        healthCache = {
          at: Date.now(),
          body: {
            toplam: sum('toplam'),
            bge_m3: sum('bge_m3'),
            e5: sum('e5'),
            bge_eski: sum('bge_eski'),
            kapsama: sum('toplam') ? Math.round((sum('bge_m3') / sum('toplam')) * 1000) / 10 : 0,
            turler: r.rows,
            sonHatTuru: hat,
          },
        };
      }
      res.json(healthCache.body);
    } catch (err: any) {
      res.status(503).json({ error: 'Vektör durumu alınamadı: ' + (err?.message || err) });
    }
  });

  app.get('/api/rag/related', async (req, res) => {
    try {
      const q = req.query as Record<string, string | undefined>;
      const mod = q.mod === 'benzer' || q.mod === 'kopya' ? q.mod : 'ilgili';
      const limit = Math.min(Math.max(Number(q.limit) || 8, 1), 20);
      let sourceId = String(q.id || '').trim();
      let sourceType = String(q.type || '').trim();
      if (!sourceId) {
        const doc = String(q.doc || '').trim();
        if (!doc || !ALLOWED.has(sourceType)) return res.status(400).json({ error: 'id ya da type+doc gerekli' });
        sourceId = (await chunkIdForDocument(sourceType, doc)) || '';
        if (!sourceId) return res.json({ source: null, mod, items: [] });
      }
      const asked = String(q.types || '').split(',').map((t) => t.trim()).filter((t) => RELATED_TYPES.includes(t));
      if (!sourceType) sourceType = sourceId.startsWith('chunk-pq-') ? 'past_question' : '';
      const sameType = sourceType && RELATED_TYPES.includes(sourceType) ? [sourceType] : undefined;
      const documentTypes = asked.length
        ? asked
        : mod === 'ilgili'
          ? MATERIAL_TYPES
          : mod === 'benzer' && (!sourceType || QUESTION_TYPES.includes(sourceType) || sourceType === 'active_question')
            ? QUESTION_TYPES
            : sameType;
      const rows = await relatedChunks(sourceId, {
        documentTypes,
        committeeId: q.kurul || undefined,
        limit,
        minSim: mod === 'kopya' ? 0.93 : mod === 'benzer' ? 0.7 : 0.55,
        perDocument: mod === 'ilgili' ? 2 : 1,
      });
      // Aynı metnin kopyaları (ör. havuzdaki yinelenen soru) "kopya" dışındaki modlarda bir kez gösterilir
      const seenText = new Set<string>();
      const unique = mod === 'kopya' ? rows : rows.filter((r) => {
        const k = snippet(r.content).toLocaleLowerCase('tr').replace(/[^\p{L}\p{N}]+/gu, '').slice(0, 160);
        if (seenText.has(k)) return false;
        seenText.add(k);
        return true;
      });
      res.setHeader('Cache-Control', 'public, max-age=600');
      res.json({
        source: sourceId,
        mod,
        items: unique.map((r) => ({
          id: r.id,
          documentId: r.document_id,
          documentType: r.document_type,
          committeeId: r.committee_id,
          discipline: r.discipline,
          title: r.title,
          pageNumber: r.page_number ?? null,
          similarity: Math.round((Number(r.similarity) || 0) * 1000) / 1000,
          snippet: snippet(r.content),
          link: linkFor(r),
        })),
      });
    } catch (err: any) {
      res.status(500).json({ error: 'İlgili içerik alınamadı: ' + (err?.message || err) });
    }
  });
}
