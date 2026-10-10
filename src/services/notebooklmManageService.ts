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

/**
 * Get all NotebookLM contributions
 */
export function getAllNotebookLMContributions(): NotebookLMContribution[] {
  const list = readJsonSafe<NotebookLMContribution[]>(CONTRIBUTIONS_FILE, []);
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
function captureOriginalSnapshot(type: NotebookLMType, proposedData: any): { targetId?: string; snapshot?: any } {
  try {
    if (type === 'past_question_correction') {
      const qItem = Array.isArray(proposedData) ? proposedData[0] : (proposedData.questions?.[0] || proposedData);
      const qid = qItem?.id;
      const questions: any[] = readJsonSafe(PAST_QUESTIONS_FILE, []);
      if (qid) {
        const found = questions.find((q) => String(q.id) === String(qid));
        if (found) return { targetId: String(qid), snapshot: found };
      }
      if (qItem?.questionNumber && qItem?.kurul) {
        const found = questions.find(
          (q) => String(q.kurul) === String(qItem.kurul) && Number(q.questionNumber) === Number(qItem.questionNumber)
        );
        if (found) return { targetId: String(found.id), snapshot: found };
      }
    } else if (type === 'spot_pearls') {
      const sItem = Array.isArray(proposedData) ? proposedData[0] : proposedData;
      const lectureId = sItem.lectureId || sItem.id;
      const summaries: any[] = readJsonSafe(SUMMARIES_CATALOG_FILE, []);
      const found = summaries.find((s) => String(s.id) === String(lectureId));
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
    const type: NotebookLMType = (detectedType as NotebookLMType) || 'raw_json';

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
