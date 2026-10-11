import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { ingestNotebookLMData, parseNotebookLMPayload } from './notebooklmBridgeService.ts';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT_DIR = path.resolve(__dirname, '..', '..');
const DATA_DIR = path.resolve(ROOT_DIR, 'data');
const SRC_DATA_DIR = path.resolve(ROOT_DIR, 'src', 'data');

const CONTRIBUTIONS_FILE = path.resolve(DATA_DIR, 'notebooklm_contributions.json');
const SRC_CONTRIBUTIONS_FILE = path.resolve(SRC_DATA_DIR, 'notebooklm_contributions.json');

const PAST_QUESTIONS_FILE = path.resolve(DATA_DIR, 'pastQuestions.json');
const SRC_PAST_QUESTIONS_FILE = path.resolve(SRC_DATA_DIR, 'pastQuestions.json');
const SUMMARIES_CATALOG_FILE = path.resolve(SRC_DATA_DIR, 'lectureSummariesCatalog.json');
const DATA_SUMMARIES_CATALOG_FILE = path.resolve(DATA_DIR, 'lectureSummariesCatalog.json');
const LOCAL_CHUNKS_FILE = path.resolve(DATA_DIR, 'local_rag_chunks.json');

export type NotebookLMType =
  | 'past_question_correction'
  | 'interactive_deck'
  | 'spot_pearls'
  | 'practice_questions'
  | 'glossary_terms'
  | 'flashcards'
  | 'raw_json';

export interface NotebookLMContribution {
  id: string;
  title: string;
  type: NotebookLMType;
  status: 'alternative' | 'active' | 'archived';
  targetId?: string;
  originalSnapshot?: any;
  proposedData: any;
  notes?: string;
  ragOptimized: boolean;
  itemCount: number;
  createdAt: string;
  updatedAt: string;
}

function readJsonSafe<T>(filePath: string, fallback: T): T {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    }
  } catch (err) {
    console.error(`[NotebookLMManage] Okuma hatası (${filePath}):`, err);
  }
  return fallback;
}

function writeJsonAtomic(filePath: string, data: any) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const content = JSON.stringify(data, null, 2);
  const tempPath = `${filePath}.tmp_${Date.now()}`;
  fs.writeFileSync(tempPath, content, 'utf-8');
  fs.renameSync(tempPath, filePath);
}

export function normalizeContributionType(rawType?: string, payload?: any): NotebookLMType {
  if (!rawType) {
    if (Array.isArray(payload)) {
      if (payload.length > 0 && (payload[0].stem || payload[0].question || payload[0].options || payload[0].reconstruction)) {
        return 'past_question_correction';
      }
      if (payload.length > 0 && payload[0].front && payload[0].back) return 'flashcards';
      if (payload.length > 0 && payload[0].term && payload[0].definition) return 'glossary_terms';
    }
    if (typeof payload === 'object' && payload !== null) {
      if (payload.questions || payload.corrections || payload.stem || payload.reconstruction) return 'past_question_correction';
      if (payload.slides || payload.deckId || payload.deck) return 'interactive_deck';
      if (payload.keyPoints || payload.highYieldPearls) return 'spot_pearls';
      if (payload.terms || payload.thesaurus) return 'glossary_terms';
      if (payload.cards) return 'flashcards';
    }
    return 'raw_json';
  }

  const t = String(rawType).toLowerCase().trim();
  if (t.includes('question') || t.includes('soru') || t.startsWith('past_question')) return 'past_question_correction';
  if (t.includes('deck') || t.includes('deste') || t.includes('slide') || t.includes('ogren')) return 'interactive_deck';
  if (t.includes('spot') || t.includes('pearl') || t.includes('summary') || t.includes('ozet')) return 'spot_pearls';
  if (t.includes('glossary') || t.includes('sozluk') || t.includes('term')) return 'glossary_terms';
  if (t.includes('card') || t.includes('kart')) return 'flashcards';
  if (t.includes('practice')) return 'practice_questions';
  return 'raw_json';
}

/**
 * Get all NotebookLM contributions with auto-healing for missing snapshots
 */
export function getAllNotebookLMContributions(): NotebookLMContribution[] {
  const list = readJsonSafe<NotebookLMContribution[]>(CONTRIBUTIONS_FILE, []);
  let dirty = false;
  list.forEach((item) => {
    // Normalize type if needed
    const normType = normalizeContributionType(item.type, item.proposedData);
    if (item.type !== normType) {
      item.type = normType;
      dirty = true;
    }
    // Auto-heal snapshot if missing or null
    if (!item.originalSnapshot) {
      const { snapshot, targetId } = captureOriginalSnapshot(item.type, item.proposedData);
      if (snapshot) {
        item.originalSnapshot = snapshot;
        if (targetId && !item.targetId) item.targetId = targetId;
        dirty = true;
      }
    }
  });
  if (dirty) {
    saveAllContributions(list);
  }
  return list.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
}

/**
 * Save all contributions with sync to both data/ and src/data/
 */
function saveAllContributions(list: NotebookLMContribution[]) {
  writeJsonAtomic(CONTRIBUTIONS_FILE, list);
  writeJsonAtomic(SRC_CONTRIBUTIONS_FILE, list);
}

/**
 * Finds snapshot of original data from canonical DB for diffing & safe rollback
 */
function captureOriginalSnapshot(rawType: any, proposedData: any): { targetId?: string; snapshot?: any } {
  try {
    const type = normalizeContributionType(rawType, proposedData);
    if (type === 'past_question_correction') {
      const qList = Array.isArray(proposedData)
        ? proposedData
        : Array.isArray(proposedData?.questions)
          ? proposedData.questions
          : [proposedData];

      const questions: any[] = readJsonSafe(PAST_QUESTIONS_FILE, []);
      const questionMap = new Map<string, any>();
      questions.forEach((q) => {
        if (q.id) {
          questionMap.set(String(q.id).toLowerCase(), q);
          questionMap.set(String(q.id).replace(/^q:/i, '').toLowerCase(), q);
        }
      });

      const snapshots: Record<string, any> = {};
      let firstTargetId: string | undefined;

      qList.forEach((qItem: any) => {
        const rawQid = qItem?.id ? String(qItem.id).trim() : '';
        const cleanQid = rawQid.replace(/^q:/i, '').trim();

        let found = cleanQid ? (questionMap.get(cleanQid.toLowerCase()) ?? (rawQid ? questionMap.get(rawQid.toLowerCase()) : undefined)) : undefined;

        // Fallback to questionNumber and kurul ONLY IF no question ID was provided
        if (!found && !rawQid && !cleanQid && qItem?.questionNumber && qItem?.kurul) {
          found = questions.find(
            (q) => String(q.kurul) === String(qItem.kurul) && Number(q.questionNumber) === Number(qItem.questionNumber)
          );
        }

        if (found) {
          if (!firstTargetId) firstTargetId = String(found.id);
          const key = cleanQid || rawQid || String(found.id);
          snapshots[key] = found;
          if (cleanQid && cleanQid !== key) snapshots[cleanQid] = found;
          if (found.id && String(found.id) !== key) snapshots[String(found.id)] = found;
        }
      });

      return {
        targetId: firstTargetId,
        snapshot: qList.length === 1 && firstTargetId && snapshots[firstTargetId] ? snapshots[firstTargetId] : snapshots,
      };
    } else if (type === 'spot_pearls') {
      const sItem = Array.isArray(proposedData) ? proposedData[0] : proposedData;
      const lectureId = sItem?.lectureId || sItem?.id;
      const summaries: any[] = readJsonSafe(SUMMARIES_CATALOG_FILE, []);
      const found = summaries.find((s) => String(s.id) === String(lectureId));
      if (found) return { targetId: String(found.id), snapshot: found };
    } else if (type === 'interactive_deck') {
      const deck = proposedData?.deck || proposedData;
      const deckId = deck?.id || deck?.deckId;
      const DECKS_FILE = path.resolve(SRC_DATA_DIR, 'interactive_learning_decks.json');
      const decks: any[] = readJsonSafe(DECKS_FILE, []);
      const found = decks.find((d) => d.id === deckId);
      if (found) return { targetId: String(found.id), snapshot: found };
    }
  } catch (err) {
    console.error('[NotebookLMManage] Snapshot alma hatası:', err);
  }
  return {};
}

/**
 * Stages NotebookLM input as an ALTERNATIVE without touching the canonical database
 */
export function stageNotebookLMInput(
  rawInput: any,
  title?: string,
  notes?: string
): { success: boolean; contribution?: NotebookLMContribution; message: string } {
  try {
    const { type: detectedType, payload } = parseNotebookLMPayload(rawInput);
    const type: NotebookLMType = normalizeContributionType(detectedType, payload);

    let count = 1;
    if (Array.isArray(payload)) {
      count = payload.length;
    } else if (payload && typeof payload === 'object') {
      if (Array.isArray(payload.questions)) count = payload.questions.length;
      else if (Array.isArray(payload.slides)) count = payload.slides.length;
      else if (Array.isArray(payload.terms)) count = payload.terms.length;
      else if (Array.isArray(payload.cards)) count = payload.cards.length;
      else if (Array.isArray(payload.keyPoints)) count = payload.keyPoints.length;
    }

    const { targetId, snapshot } = captureOriginalSnapshot(type, payload);

    let autoTitle = title;
    if (!autoTitle) {
      if (type === 'past_question_correction') {
        autoTitle = targetId ? `Soru #${targetId} Düzeltme Alternatifi` : `${count} Çıkmış Soru Önerisi`;
      } else if (type === 'spot_pearls') {
        autoTitle = `Ders Spot Bilgileri (${payload.lectureId || targetId || 'Ders'})`;
      } else if (type === 'interactive_deck') {
        autoTitle = `İnteraktif Deste (${payload.deck?.title || payload.title || 'Deste'})`;
      } else if (type === 'flashcards') {
        autoTitle = `${count} Akıl Kartı Paketi`;
      } else if (type === 'glossary_terms') {
        autoTitle = `${count} Tıbbi Terim Önerisi`;
      } else {
        autoTitle = `NotebookLM Veri Paketi (${new Date().toLocaleDateString('tr-TR')})`;
      }
    }

    const newContribution: NotebookLMContribution = {
      id: `nlm-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`,
      title: autoTitle,
      type,
      status: 'alternative', // STAGED AS ALTERNATIVE, NOT APPLIED
      targetId,
      originalSnapshot: snapshot || null,
      proposedData: payload,
      notes: notes || 'NotebookLM üzerinden aktarıldı, onay/tercih bekliyor.',
      ragOptimized: false,
      itemCount: count,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    const list = getAllNotebookLMContributions();
    list.unshift(newContribution);
    saveAllContributions(list);

    return {
      success: true,
      contribution: newContribution,
      message: `NotebookLM verisi sisteme güvenle eklendi ve "Alternatif" olarak kaydedildi. Mevcut verilerin üzerine yazılmadı.`
    };
  } catch (err: any) {
    return {
      success: false,
      message: `Veri ayrıştırılamadı veya eklenemedi: ${err.message}`
    };
  }
}

/**
 * Activates a NotebookLM alternative (Chooses this data to apply to canonical DB)
 */
export async function activateNotebookLMContribution(id: string): Promise<{ success: boolean; message: string }> {
  const list = getAllNotebookLMContributions();
  const item = list.find((c) => c.id === id);

  if (!item) {
    return { success: false, message: 'Kayıt bulunamadı.' };
  }

  try {
    // If not captured yet, capture original state before applying
    if (!item.originalSnapshot) {
      const { snapshot, targetId } = captureOriginalSnapshot(item.type, item.proposedData);
      item.originalSnapshot = snapshot || null;
      if (targetId) item.targetId = targetId;
    }

    // Apply to canonical database using existing bridge engine
    const ingestResult = await ingestNotebookLMData(item.proposedData, item.type);
    if (!ingestResult.success) {
      return { success: false, message: `Veritabanına uygulanamadı: ${ingestResult.message}` };
    }

    // Mark as active
    item.status = 'active';
    item.ragOptimized = true;
    item.updatedAt = new Date().toISOString();

    saveAllContributions(list);

    // Sync to RAG automatically
    syncContributionToRag(item);

    return {
      success: true,
      message: `"${item.title}" başarıyla tercih edildi ve ana sisteme entegre edildi. RAG dizini güncellendi.`
    };
  } catch (err: any) {
    return { success: false, message: `Hata oluştu: ${err.message}` };
  }
}

/**
 * Deactivates a NotebookLM contribution (Rolls back canonical DB to original snapshot)
 */
export async function deactivateNotebookLMContribution(id: string): Promise<{ success: boolean; message: string }> {
  const list = getAllNotebookLMContributions();
  const item = list.find((c) => c.id === id);

  if (!item) {
    return { success: false, message: 'Kayıt bulunamadı.' };
  }

  try {
    if (item.originalSnapshot) {
      // Revert canonical DB to original snapshot
      if (item.type === 'past_question_correction') {
        const questions: any[] = readJsonSafe(PAST_QUESTIONS_FILE, []);
        const idx = questions.findIndex((q) => String(q.id) === String(item.targetId));
        if (idx >= 0) {
          questions[idx] = item.originalSnapshot;
          writeJsonAtomic(PAST_QUESTIONS_FILE, questions);
          writeJsonAtomic(SRC_PAST_QUESTIONS_FILE, questions);
        }
      } else if (item.type === 'spot_pearls') {
        const summaries: any[] = readJsonSafe(SUMMARIES_CATALOG_FILE, []);
        const idx = summaries.findIndex((s) => String(s.id) === String(item.targetId));
        if (idx >= 0) {
          summaries[idx] = item.originalSnapshot;
          writeJsonAtomic(SUMMARIES_CATALOG_FILE, summaries);
          writeJsonAtomic(DATA_SUMMARIES_CATALOG_FILE, summaries);
        }
      }
    }

    item.status = 'alternative';
    item.updatedAt = new Date().toISOString();
    saveAllContributions(list);

    return {
      success: true,
      message: `"${item.title}" pasife alındı ve orijinal veritabanı yedeği geri yüklendi.`
    };
  } catch (err: any) {
    return { success: false, message: `Geri alma hatası: ${err.message}` };
  }
}

/**
 * Updates a NotebookLM contribution (edit proposed data, title, notes)
 */
export function updateNotebookLMContribution(
  id: string,
  updates: Partial<NotebookLMContribution>
): { success: boolean; contribution?: NotebookLMContribution; message: string } {
  const list = getAllNotebookLMContributions();
  const idx = list.findIndex((c) => c.id === id);

  if (idx === -1) {
    return { success: false, message: 'Kayıt bulunamadı.' };
  }

  const existing = list[idx];
  const updated: NotebookLMContribution = {
    ...existing,
    title: updates.title !== undefined ? updates.title : existing.title,
    notes: updates.notes !== undefined ? updates.notes : existing.notes,
    proposedData: updates.proposedData !== undefined ? updates.proposedData : existing.proposedData,
    updatedAt: new Date().toISOString(),
  };

  list[idx] = updated;
  saveAllContributions(list);

  return {
    success: true,
    contribution: updated,
    message: 'Kayıt başarıyla güncellendi.'
  };
}

/**
 * Deletes a contribution record permanently
 */
export function deleteNotebookLMContribution(id: string): { success: boolean; message: string } {
  const list = getAllNotebookLMContributions();
  const item = list.find((c) => c.id === id);

  if (!item) {
    return { success: false, message: 'Kayıt bulunamadı.' };
  }

  const filtered = list.filter((c) => c.id !== id);
  saveAllContributions(filtered);

  return {
    success: true,
    message: `"${item.title}" kaydı kalıcı olarak silindi.`
  };
}

/**
 * Optimizes active NotebookLM contributions into local RAG engine chunks
 */
export function syncContributionToRag(item: NotebookLMContribution) {
  try {
    const chunks: any[] = readJsonSafe(LOCAL_CHUNKS_FILE, []);
    const chunkId = `rag-nlm-${item.id}`;

    // Extract rich searchable medical content
    let textContent = `${item.title}\n`;
    if (item.type === 'past_question_correction') {
      const q = Array.isArray(item.proposedData) ? item.proposedData[0] : (item.proposedData.questions?.[0] || item.proposedData);
      textContent += `Soru: ${q.stem || ''}\nDoğru Cevap: ${q.correctAnswer || ''}\nFizyopatolojik Açıklama: ${q.explanation || ''}\nŞık Analizi: ${q.sik_analizi || ''}`;
    } else if (item.type === 'spot_pearls') {
      const kps = item.proposedData.keyPoints || [];
      textContent += `Spot Bilgiler:\n${kps.join('\n')}`;
    } else {
      textContent += JSON.stringify(item.proposedData);
    }

    const existingIdx = chunks.findIndex((c) => c.id === chunkId);
    const newChunk = {
      id: chunkId,
      documentId: item.id,
      documentType: 'notebooklm_contribution',
      committeeId: 'donem3',
      title: item.title,
      content: textContent,
      discipline: item.type,
      topic: item.title,
      confidenceScore: 1.0,
      metadata: {
        source: 'notebooklm_verified',
        type: item.type,
        updatedAt: item.updatedAt,
        targetId: item.targetId,
      }
    };

    if (existingIdx >= 0) {
      chunks[existingIdx] = newChunk;
    } else {
      chunks.push(newChunk);
    }

    writeJsonAtomic(LOCAL_CHUNKS_FILE, chunks);
  } catch (err) {
    console.error('[NotebookLMManage] RAG eşitleme hatası:', err);
  }
}
