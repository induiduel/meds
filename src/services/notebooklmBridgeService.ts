import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT_DIR = path.resolve(__dirname, '..', '..'); // meds/
const DATA_DIR = path.resolve(ROOT_DIR, 'data');
const SRC_DATA_DIR = path.resolve(ROOT_DIR, 'src', 'data');
const REPO_ROOT = path.resolve(ROOT_DIR, '..'); // /home/indu/medsor

// Primary File Paths
const PAST_QUESTIONS_FILE = path.resolve(DATA_DIR, 'pastQuestions.json');
const SRC_PAST_QUESTIONS_FILE = path.resolve(SRC_DATA_DIR, 'pastQuestions.json');

const DECKS_FILE = path.resolve(SRC_DATA_DIR, 'interactive_learning_decks.json');
const DECK_ITEMS_DIR = path.resolve(SRC_DATA_DIR, 'decks', 'items');

const SUMMARIES_CATALOG_FILE = path.resolve(SRC_DATA_DIR, 'lectureSummariesCatalog.json');
const DATA_SUMMARIES_CATALOG_FILE = path.resolve(DATA_DIR, 'lectureSummariesCatalog.json');

const GLOSSARY_FILE = path.resolve(SRC_DATA_DIR, 'medical_glossary.json');
const ENCYCLOPEDIA_FILE = path.resolve(SRC_DATA_DIR, 'medical_encyclopedia.json');

const FLASHCARDS_FILE = path.resolve(SRC_DATA_DIR, 'question_cards.json');
const PRACTICE_QUESTIONS_DIR = path.resolve(SRC_DATA_DIR, 'ornek_sorular');

// Helper to safely read JSON
function readJsonSafe<T>(filePath: string, fallback: T): T {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    }
  } catch (err) {
    console.error(`[NotebookLMBridge] JSON okuma hatası (${filePath}):`, err);
  }
  return fallback;
}

// Helper to write JSON with backup
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

// Convert markdown to clean, crawler-friendly semantic HTML
export function markdownToSemanticHtml(title: string, markdown: string): string {
  const escapeHtml = (str: string) =>
    str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  const lines = markdown.split('\n');
  const htmlParts: string[] = [];
  let inList = false;

  for (let line of lines) {
    const trimmed = line.trim();

    if (!trimmed) {
      if (inList) {
        htmlParts.push('</ul>');
        inList = false;
      }
      continue;
    }

    if (trimmed.startsWith('# ')) {
      if (inList) { htmlParts.push('</ul>'); inList = false; }
      htmlParts.push(`<h1>${escapeHtml(trimmed.slice(2))}</h1>`);
    } else if (trimmed.startsWith('## ')) {
      if (inList) { htmlParts.push('</ul>'); inList = false; }
      htmlParts.push(`<h2>${escapeHtml(trimmed.slice(3))}</h2>`);
    } else if (trimmed.startsWith('### ')) {
      if (inList) { htmlParts.push('</ul>'); inList = false; }
      htmlParts.push(`<h3>${escapeHtml(trimmed.slice(4))}</h3>`);
    } else if (trimmed.startsWith('#### ')) {
      if (inList) { htmlParts.push('</ul>'); inList = false; }
      htmlParts.push(`<h4>${escapeHtml(trimmed.slice(5))}</h4>`);
    } else if (trimmed === '---') {
      if (inList) { htmlParts.push('</ul>'); inList = false; }
      htmlParts.push('<hr>');
    } else if (trimmed.startsWith('> ')) {
      if (inList) { htmlParts.push('</ul>'); inList = false; }
      htmlParts.push(`<blockquote>${escapeHtml(trimmed.slice(2))}</blockquote>`);
    } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      if (!inList) {
        htmlParts.push('<ul>');
        inList = true;
      }
      let content = escapeHtml(trimmed.slice(2));
      content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      content = content.replace(/`([^`]+)`/g, '<code>$1</code>');
      htmlParts.push(`<li>${content}</li>`);
    } else if (trimmed.startsWith('  * ') || trimmed.startsWith('  - ')) {
      let content = escapeHtml(trimmed.slice(4));
      content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      content = content.replace(/`([^`]+)`/g, '<code>$1</code>');
      htmlParts.push(`<li style="margin-left: 20px;">${content}</li>`);
    } else {
      if (inList) { htmlParts.push('</ul>'); inList = false; }
      let content = escapeHtml(trimmed);
      content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      content = content.replace(/`([^`]+)`/g, '<code>$1</code>');
      htmlParts.push(`<p>${content}</p>`);
    }
  }

  if (inList) {
    htmlParts.push('</ul>');
  }

  return `<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(title)}</title>
  <style>
    body { font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 24px 16px; color: #1e293b; background: #fff; }
    h1 { color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; font-size: 26px; }
    h2 { color: #1e293b; margin-top: 28px; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px; font-size: 20px; }
    h3 { color: #334155; margin-top: 20px; font-size: 17px; }
    blockquote { border-left: 4px solid #3b82f6; background: #eff6ff; margin: 16px 0; padding: 12px 16px; border-radius: 6px; color: #1e40af; }
    ul { padding-left: 20px; margin: 10px 0; }
    li { margin-bottom: 6px; }
    p { margin: 8px 0; }
    strong { color: #0f172a; }
    code { background: #f1f5f9; color: #0f172a; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 0.9em; }
    hr { border: none; border-top: 1px solid #e2e8f0; margin: 28px 0; }
  </style>
</head>
<body>
  <article>
    ${htmlParts.join('\n')}
  </article>
</body>
</html>`;
}

// ---------------------------------------------------------------------------
// 1. EXPORT GENERATORS (Formatted for NotebookLM Consumption)
// ---------------------------------------------------------------------------

export function exportPastExamsToMarkdown(options: {
  kurul?: string;
  discipline?: string;
  limit?: number;
  offset?: number;
  search?: string;
} = {}): string {
  const questions: any[] = readJsonSafe(PAST_QUESTIONS_FILE, []);
  let filtered = questions;

  if (options.kurul) {
    const kStr = String(options.kurul).toLowerCase();
    filtered = filtered.filter((q) => {
      const qk = String(q.kurul || q.committeeId || '').toLowerCase();
      return qk.includes(kStr);
    });
  }

  if (options.discipline) {
    const dStr = String(options.discipline).toLowerCase();
    filtered = filtered.filter((q) => String(q.discipline || '').toLowerCase().includes(dStr));
  }

  if (options.search) {
    const sStr = String(options.search).toLowerCase();
    filtered = filtered.filter((q) => {
      const stem = String(q.stem || q.reconstruction?.stem || '').toLowerCase();
      const topic = String(q.topic || '').toLowerCase();
      return stem.includes(sStr) || topic.includes(sStr);
    });
  }

  const offset = options.offset || 0;
  const limit = options.limit || filtered.length;
  const sliced = filtered.slice(offset, offset + limit);

  let md = `# MEDSOR ÇIKMIŞ SORULAR ARŞİVİ (NOTEBOOKLM UYUMLU KAYNAK)\n`;
  md += `> Toplam Eşleşen: ${filtered.length} Soru | Gösterilen: ${sliced.length} (Ofset: ${offset})\n\n---\n\n`;

  sliced.forEach((q, idx) => {
    const qid = q.id || `q-${offset + idx + 1}`;
    const kurul = q.kurul || q.committeeId || 'Genel';
    const yil = q.examYear || 'Bilinmiyor';
    const brans = q.discipline || 'Genel Tıp';
    const konu = q.topic || 'Genel';
    const stem = String(q.stem || q.reconstruction?.stem || q.question || '').trim();
    const correct = q.correctAnswer || q.claimedAnswer || '';
    const explanation = String(q.explanation || q.tibbi_aciklama || q.reconstruction?.explanation || '').trim();
    const sikAnalizi = typeof q.sik_analizi === 'string'
      ? q.sik_analizi.trim()
      : (typeof q.sik_analizi === 'object' && q.sik_analizi !== null ? JSON.stringify(q.sik_analizi) : '');
    const quality = String(q.qualityTier || 'standart');

    md += `### Soru #${q.questionNumber || (offset + idx + 1)} | ID: \`${qid}\`\n`;
    md += `- **Kurul/Dönem:** Kurul ${kurul} | **Yıl:** ${yil} | **Branş:** ${brans} | **Konu:** ${konu} | **Kalite:** ${quality.toUpperCase()}\n`;
    md += `- **Soru Metni:** ${stem}\n`;

    if (q.options && Array.isArray(q.options) && q.options.length > 0) {
      md += `- **Seçenekler:**\n`;
      q.options.forEach((opt: any) => {
        const k = (opt.key || '').toUpperCase();
        const t = (opt.text || '').trim();
        const mark = k === String(correct).toUpperCase() ? ' **(✓ DOĞRU ŞIK)**' : '';
        md += `  * **${k})** ${t}${mark}\n`;
      });
    }

    md += `- **Doğru Cevap:** ${correct || '[Belirtilmemiş]'}\n`;
    if (explanation) {
      md += `- **Fizyopatolojik Açıklama:** ${explanation}\n`;
    }
    if (sikAnalizi) {
      md += `- **Şık Analizi & Çürütme:** ${sikAnalizi}\n`;
    }
    md += `\n---\n\n`;
  });

  return md;
}

export function exportSummariesToMarkdown(options: { kurul?: string; limit?: number } = {}): string {
  const summaries: any[] = readJsonSafe(SUMMARIES_CATALOG_FILE, []);
  let filtered = summaries;
  if (options.kurul) {
    const kStr = String(options.kurul).toLowerCase();
    filtered = filtered.filter((s) => String(s.kurul || s.committeeId || '').toLowerCase().includes(kStr));
  }
  const limit = options.limit || filtered.length;
  const sliced = filtered.slice(0, limit);

  let md = `# MEDSOR AMFİ DERS ÖZETLERİ VE SPOT BİLGİLER\n`;
  md += `> Toplam Ders: ${filtered.length} | Gösterilen: ${sliced.length}\n\n---\n\n`;

  sliced.forEach((s) => {
    md += `## [Ders ${s.id}] ${s.title}\n`;
    md += `- **Kurul:** Kurul ${s.kurul || s.committeeId} | **Branş:** ${s.discipline} | **Eğitmen:** ${s.instructor || 'Belirtilmemiş'}\n`;
    if (s.keyPoints && Array.isArray(s.keyPoints) && s.keyPoints.length > 0) {
      md += `\n### Yüksek Verimli Spot Bilgiler & Kilit Noktalar:\n`;
      s.keyPoints.forEach((kp: string) => {
        md += `- ${kp.replace(/^[-\s*]+/, '')}\n`;
      });
    }
    if (s.content) {
      md += `\n### Detaylı Ders Özeti:\n${s.content}\n`;
    }
    md += `\n---\n\n`;
  });

  return md;
}

export function exportGlossaryToMarkdown(options: { limit?: number; category?: string } = {}): string {
  const glossary: Record<string, any> = readJsonSafe(GLOSSARY_FILE, {});
  const encyclopedia: any[] = readJsonSafe(ENCYCLOPEDIA_FILE, []);

  let md = `# MEDSOR TIP SÖZLÜĞÜ VE KLİNİK ANSİKLOPEDİ\n`;
  md += `> Toplam Terim: ${Object.keys(glossary).length} Sözlük Maddesi, ${encyclopedia.length} Ansiklopedi Maddesi\n\n---\n\n`;

  // First output encyclopedia if available
  const encSliced = encyclopedia.slice(0, options.limit || encyclopedia.length);
  encSliced.forEach((item) => {
    md += `### ${item.term} (${item.latinName || ''})\n`;
    md += `- **Kategori:** ${item.category || 'Genel'} | **Branş:** ${item.discipline || 'Genel'}\n`;
    md += `- **Tanım:** ${item.definition || ''}\n`;
    if (item.morphologyOrMechanism) md += `- **Morfoloji / Mekanizma:** ${item.morphologyOrMechanism}\n`;
    if (item.differentialDiagnosis) md += `- **Ayırıcı Tanı:** ${item.differentialDiagnosis}\n`;
    if (item.examSpotPearls) md += `- **Sınav Spotu / İnci Bilgi:** ${item.examSpotPearls}\n`;
    if (item.pitfallsAndWarnings) md += `- **Tuzaklar & Uyarılar:** ${item.pitfallsAndWarnings}\n`;
    md += `\n---\n\n`;
  });

  return md;
}

export function exportFlashcardsToMarkdown(options: { group?: string; limit?: number } = {}): string {
  const cards: any[] = readJsonSafe(FLASHCARDS_FILE, []);
  let filtered = cards;
  if (options.group) {
    filtered = filtered.filter((c) => String(c.group || '').toLowerCase().includes(options.group!.toLowerCase()));
  }
  const sliced = filtered.slice(0, options.limit || filtered.length);

  let md = `# MEDSOR AKIL VE ÇALIŞMA KARTLARI (FLASHCARDS)\n`;
  md += `> Toplam Kart: ${filtered.length} | Gösterilen: ${sliced.length}\n\n---\n\n`;

  sliced.forEach((c, idx) => {
    md += `### Kart #${idx + 1} | ID: \`${c.id}\` [${c.group || 'Genel Tıp'}]\n`;
    md += `- **Ön Yüz (Soru/Kavram):** ${c.front}\n`;
    md += `- **Arka Yüz (Cevap):** ${c.back}\n`;
    if (c.note) md += `- **Klinik Not:** ${c.note}\n`;
    md += `\n---\n\n`;
  });

  return md;
}

export function exportDecksToMarkdown(options: { deckId?: string } = {}): string {
  const decks: any[] = readJsonSafe(DECKS_FILE, []);
  let filtered = decks;
  if (options.deckId) {
    filtered = filtered.filter((d) => d.id === options.deckId);
  }

  let md = `# MEDSOR İNTERAKTİF ÖĞRENME DESTELERİ VE SLAYTLARI\n`;
  md += `> Toplam Deste Sayısı: ${filtered.length}\n\n---\n\n`;

  filtered.forEach((deck) => {
    md += `## [Deste ID: ${deck.id}] ${deck.title}\n`;
    md += `- **Açıklama:** ${deck.description || ''}\n`;
    md += `- **Kurul/Dönem:** ${deck.committee || deck.donem || ''} | **Toplam Slayt:** ${deck.slides?.length || 0}\n\n`;

    if (deck.slides && Array.isArray(deck.slides)) {
      deck.slides.slice(0, 30).forEach((slide: any, sIdx: number) => {
        md += `#### Slayt #${sIdx + 1}: ${slide.title}\n`;
        md += `${slide.synthesisNarrative || slide.content || ''}\n\n`;
      });
      if (deck.slides.length > 30) {
        md += `*(Devam eden ${deck.slides.length - 30} slayt katalogda mevcuttur)*\n\n`;
      }
    }
    md += `\n---\n\n`;
  });

  return md;
}

// ---------------------------------------------------------------------------
// 2. NOTEBOOKLM INGESTION & UPDATE PIPELINE
// ---------------------------------------------------------------------------

export interface IngestionResult {
  success: boolean;
  type: string;
  count: number;
  updatedIds: string[];
  message: string;
  warnings?: string[];
}

/**
 * Universally parses raw NotebookLM output (JSON, markdown code blocks, or structured text)
 */
export function parseNotebookLMPayload(raw: any): { type?: string; payload: any } {
  let parsedObj: any = raw;

  if (typeof raw === 'string') {
    const str = raw.trim();
    // Try extracting from markdown code block ```json ... ```
    const jsonMatch = str.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
    if (jsonMatch) {
      try {
        parsedObj = JSON.parse(jsonMatch[1]);
      } catch (_) {}
    } else {
      try {
        parsedObj = JSON.parse(str);
      } catch (_) {}
    }
  }

  const detectedType = parsedObj?.type || inferPayloadType(parsedObj);
  return {
    type: detectedType !== 'unknown' ? detectedType : undefined,
    payload: parsedObj
  };
}

/**
 * Central Ingestion Router
 */
export async function ingestNotebookLMData(rawInput: any, forcedType?: string): Promise<IngestionResult> {
  const { type: detectedType, payload } = parseNotebookLMPayload(rawInput);
  const targetType = forcedType || detectedType || inferPayloadType(payload);

  switch (targetType) {
    case 'past_question_correction':
    case 'past_question_correction_full_schema':
    case 'past_questions':
    case 'soru_duzeltme':
      return ingestPastQuestionCorrections(payload);

    case 'interactive_deck':
    case 'interactive_slides':
    case 'ogren_destesi':
      return ingestInteractiveDeck(payload);

    case 'spot_pearls':
    case 'ders_ozeti':
    case 'summaries':
      return ingestSpotPearls(payload);

    case 'practice_questions':
    case 'ornek_sorular':
      return ingestPracticeQuestions(payload);

    case 'glossary_terms':
    case 'sozluk':
    case 'thesaurus':
      return ingestGlossaryTerms(payload);

    case 'flashcards':
    case 'kartlar':
      return ingestFlashcards(payload);

    default:
      return {
        success: false,
        type: 'unknown',
        count: 0,
        updatedIds: [],
        message: `Bilinmeyen veya desteklenmeyen veri tipi: "${targetType}". Lütfen geçerli bir NotebookLM veri şablonu (type: past_question_correction, interactive_deck, spot_pearls, practice_questions, glossary_terms, flashcards) kullanın.`
      };
  }
}

function inferPayloadType(data: any): string {
  if (!data) return 'unknown';
  if (Array.isArray(data)) {
    if (data.length > 0 && (data[0].stem || data[0].question || data[0].options)) return 'past_question_correction';
    if (data.length > 0 && (data[0].front && data[0].back)) return 'flashcards';
    if (data.length > 0 && (data[0].term && data[0].definition)) return 'glossary_terms';
  }
  if (typeof data === 'object') {
    if (data.questions || data.corrections) return 'past_question_correction';
    if (data.stem || data.reconstruction || (data.options && Array.isArray(data.options))) return 'past_question_correction';
    if (data.slides || data.deckId) return 'interactive_deck';
    if (data.keyPoints || data.highYieldPearls) return 'spot_pearls';
    if (data.terms || data.thesaurus) return 'glossary_terms';
    if (data.cards) return 'flashcards';
  }
  return 'unknown';
}

// ---------------------------------------------------------------------------
// 3. SPECIALIZED INGESTION ENGINES
// ---------------------------------------------------------------------------

/**
 * Normalizes question options into MeDSor standard QuestionOption array
 */
function normalizeQuestionOptions(
  rawOptions: any,
  correctAnswer?: string
): Array<{ key: 'A' | 'B' | 'C' | 'D' | 'E'; label: string; text: string; isCorrect: boolean; upvotes: number }> {
  if (!rawOptions) return [];
  const keys: Array<'A' | 'B' | 'C' | 'D' | 'E'> = ['A', 'B', 'C', 'D', 'E'];
  const targetAnswer = (correctAnswer || '').trim().toUpperCase();

  // If object like { "A": "...", "B": "..." }
  if (typeof rawOptions === 'object' && !Array.isArray(rawOptions)) {
    return keys
      .filter((k) => rawOptions[k] !== undefined || rawOptions[k.toLowerCase()] !== undefined)
      .map((k) => {
        const text = String(rawOptions[k] ?? rawOptions[k.toLowerCase()] ?? '').trim();
        return {
          key: k,
          label: k,
          text,
          isCorrect: k === targetAnswer,
          upvotes: 0,
        };
      });
  }

  // If array of strings or objects
  if (Array.isArray(rawOptions)) {
    return rawOptions.map((opt, idx) => {
      const fallbackKey = keys[idx] || 'A';
      if (typeof opt === 'string') {
        const match = opt.match(/^\s*([A-Ea-e])[\).\s:-]+(.*)$/);
        const key = (match ? match[1].toUpperCase() : fallbackKey) as 'A' | 'B' | 'C' | 'D' | 'E';
        const text = (match ? match[2] : opt).trim();
        return {
          key,
          label: key,
          text,
          isCorrect: key === targetAnswer,
          upvotes: 0,
        };
      } else if (typeof opt === 'object' && opt !== null) {
        const key = (String(opt.key || opt.label || fallbackKey).toUpperCase().trim()) as 'A' | 'B' | 'C' | 'D' | 'E';
        const text = String(opt.text || opt.content || opt.value || '').trim();
        const isCorrect = opt.isCorrect !== undefined ? Boolean(opt.isCorrect) : key === targetAnswer;
        return {
          key,
          label: key,
          text,
          isCorrect,
          upvotes: Number(opt.upvotes) || 0,
        };
      }
      return {
        key: fallbackKey,
        label: fallbackKey,
        text: String(opt || ''),
        isCorrect: fallbackKey === targetAnswer,
        upvotes: 0,
      };
    });
  }

  return [];
}

const COMMITTEE_CODE_MAP: Record<number, string> = {
  1: 'TIP310',
  2: 'TIP311',
  3: 'TIP312',
  4: 'TIP313',
  5: 'TIP314',
  6: 'TIP315',
};

/**
 * Ingest past exam corrections into pastQuestions.json (both data/ and src/data/)
 */
export function ingestPastQuestionCorrections(payload: any): IngestionResult {
  const items: any[] = Array.isArray(payload)
    ? payload
    : Array.isArray(payload.questions)
      ? payload.questions
      : Array.isArray(payload.corrections)
        ? payload.corrections
        : [payload];

  if (items.length === 0) {
    return { success: false, type: 'past_question_correction', count: 0, updatedIds: [], message: 'İşlenecek soru bulunamadı.' };
  }

  const existingQuestions: any[] = readJsonSafe(PAST_QUESTIONS_FILE, []);
  const questionMap = new Map<string, number>();
  existingQuestions.forEach((q, idx) => {
    if (q.id) questionMap.set(String(q.id), idx);
  });

  const updatedIds: string[] = [];
  const warnings: string[] = [];

  items.forEach((item) => {
    const rawQid = item.id ? String(item.id).trim() : null;
    const cleanQid = rawQid ? rawQid.replace(/^q:/i, '').trim() : null;
    let targetIdx = cleanQid ? (questionMap.get(cleanQid) ?? (rawQid ? questionMap.get(rawQid) : undefined)) : undefined;

    // If ID not found, attempt match by questionNumber and kurul ONLY IF no question ID was provided
    if (targetIdx === undefined && !rawQid && !cleanQid && item.questionNumber && item.kurul) {
      targetIdx = existingQuestions.findIndex(
        (q) => String(q.kurul) === String(item.kurul) && Number(q.questionNumber) === Number(item.questionNumber)
      );
    }

    const correctAns = (item.correctAnswer || item.claimedAnswer || 'A').toString().trim().toUpperCase() as 'A' | 'B' | 'C' | 'D' | 'E';
    const normOptions = normalizeQuestionOptions(item.options, correctAns);

    if (targetIdx !== undefined && targetIdx >= 0) {
      // Update existing question
      const curr = existingQuestions[targetIdx];
      const finalOptions = normOptions.length > 0 ? normOptions : (curr.options || []);
      const finalStem = item.stem || item.question || curr.stem || '';
      const finalExplanation = item.explanation || item.tibbi_aciklama || curr.explanation || '';
      const oncul = Array.isArray(item.oncul_maddeleri) ? item.oncul_maddeleri : curr.oncul_maddeleri;

      // Update both root fields and reconstruction object so all views (Booklet, Solve, Drafts) sync perfectly
      const reconstruction = {
        stem: finalStem,
        options: finalOptions,
        correctAnswer: correctAns,
        explanation: finalExplanation,
        confidenceScore: 98,
        qualityScore: 95,
        isAiRefined: true,
        lastUpdated: new Date().toISOString(),
        oncul_maddeleri: oncul,
      };

      existingQuestions[targetIdx] = {
        ...curr,
        ...item,
        stem: finalStem,
        options: finalOptions,
        correctAnswer: correctAns,
        claimedAnswer: correctAns,
        explanation: finalExplanation,
        tibbi_aciklama: item.tibbi_aciklama || finalExplanation,
        sik_analizi: item.sik_analizi || curr.sik_analizi || '',
        cevap_gerekcesi: item.cevap_gerekcesi || curr.cevap_gerekcesi || '',
        referans_kaynaklar: item.referans_kaynaklar || curr.referans_kaynaklar || [],
        oncul_maddeleri: oncul,
        discipline: item.discipline || curr.discipline,
        topic: item.topic || curr.topic,
        status: item.status || 'verified',
        reconstruction,
        qualityTier: item.qualityTier || curr.qualityTier || 'altin',
        updatedAt: new Date().toISOString(),
        denetleyiciOnayi: true,
        denetleyici_onayi: true,
        notebooklmAudited: true,
      };
      updatedIds.push(curr.id);
    } else {
      // Create new question entry
      const newId = cleanQid || rawQid || `q-nlm-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`;
      const kurulNum = Number(item.kurul) || 1;
      const committeeId = item.committeeId || COMMITTEE_CODE_MAP[kurulNum] || `donem3-kurul${kurulNum}`;
      const finalStem = item.stem || item.question || '';
      const finalExplanation = item.explanation || item.tibbi_aciklama || '';
      const oncul = Array.isArray(item.oncul_maddeleri) ? item.oncul_maddeleri : undefined;

      const reconstruction = {
        stem: finalStem,
        options: normOptions,
        correctAnswer: correctAns,
        explanation: finalExplanation,
        confidenceScore: 98,
        qualityScore: 95,
        isAiRefined: true,
        lastUpdated: new Date().toISOString(),
        oncul_maddeleri: oncul,
      };

      const newQ = {
        ...item,
        id: newId,
        kurul: kurulNum,
        committeeId,
        questionNumber: item.questionNumber || existingQuestions.length + 1,
        examYear: item.examYear || '2023-2024',
        discipline: item.discipline || 'Genel Tıp',
        topic: item.topic || 'Genel',
        stem: finalStem,
        options: normOptions,
        correctAnswer: correctAns,
        claimedAnswer: correctAns,
        explanation: finalExplanation,
        tibbi_aciklama: finalExplanation,
        sik_analizi: item.sik_analizi || '',
        cevap_gerekcesi: item.cevap_gerekcesi || '',
        referans_kaynaklar: item.referans_kaynaklar || [],
        oncul_maddeleri: oncul,
        status: item.status || 'verified',
        reconstruction,
        qualityTier: item.qualityTier || 'altin',
        updatedAt: new Date().toISOString(),
        isPastExam: true,
        denetleyiciOnayi: true,
        denetleyici_onayi: true,
        notebooklmAudited: true,
      };
      existingQuestions.push(newQ);
      questionMap.set(newId, existingQuestions.length - 1);
      updatedIds.push(newId);
    }
  });

  // Save to both data/pastQuestions.json and src/data/pastQuestions.json
  writeJsonAtomic(PAST_QUESTIONS_FILE, existingQuestions);
  writeJsonAtomic(SRC_PAST_QUESTIONS_FILE, existingQuestions);

  return {
    success: true,
    type: 'past_question_correction',
    count: updatedIds.length,
    updatedIds,
    message: `${updatedIds.length} çıkmış soru veritabanında başarıyla güncellendi/kaydedildi.`,
    warnings: warnings.length > 0 ? warnings : undefined,
  };
}

/**
 * Ingest or update an interactive learning deck into interactive_learning_decks.json
 */
export function ingestInteractiveDeck(payload: any): IngestionResult {
  const deck = payload.deck || payload;
  const deckId = deck.id || deck.deckId;

  if (!deckId) {
    return { success: false, type: 'interactive_deck', count: 0, updatedIds: [], message: 'Deste ID (id veya deckId) eksik.' };
  }

  const existingDecks: any[] = readJsonSafe(DECKS_FILE, []);
  const targetIdx = existingDecks.findIndex((d) => d.id === deckId);

  const formattedDeck = {
    ...deck,
    id: deckId,
    title: deck.title || 'İnteraktif Öğrenme Destesi',
    slides: deck.slides || [],
    updatedAt: new Date().toISOString(),
    source: 'notebooklm_pipeline',
  };

  if (targetIdx >= 0) {
    existingDecks[targetIdx] = formattedDeck;
  } else {
    existingDecks.push(formattedDeck);
  }

  // Save to interactive_learning_decks.json
  writeJsonAtomic(DECKS_FILE, existingDecks);

  // Also save item file to decks/items/<id>.json
  const itemPath = path.resolve(DECK_ITEMS_DIR, `${deckId}.json`);
  writeJsonAtomic(itemPath, formattedDeck);

  // Dışa aktarım paketleri `npm run decks:packages` ile kaynaktan üretilir.

  return {
    success: true,
    type: 'interactive_deck',
    count: formattedDeck.slides.length,
    updatedIds: [deckId],
    message: `Deste "${deckId}" (${formattedDeck.slides.length} slayt) sisteme ve derleme dosyalarına başarıyla yazıldı.`,
  };
}

/**
 * Ingest high yield spot pearls into lectureSummariesCatalog.json
 */
export function ingestSpotPearls(payload: any): IngestionResult {
  const items: any[] = Array.isArray(payload) ? payload : [payload];
  const summaries: any[] = readJsonSafe(SUMMARIES_CATALOG_FILE, []);
  const updatedIds: string[] = [];

  items.forEach((item) => {
    const lectureId = item.lectureId || item.id;
    const titleMatch = item.title ? String(item.title).toLowerCase() : '';

    const targetIdx = summaries.findIndex(
      (s) => (lectureId && String(s.id) === String(lectureId)) || (titleMatch && String(s.title).toLowerCase().includes(titleMatch))
    );

    if (targetIdx >= 0) {
      const curr = summaries[targetIdx];
      const newKeyPoints = Array.from(new Set([...(curr.keyPoints || []), ...(item.keyPoints || item.highYieldPearls || [])]));
      summaries[targetIdx] = {
        ...curr,
        keyPoints: newKeyPoints,
        content: item.content || curr.content,
        updatedAt: new Date().toISOString(),
      };
      updatedIds.push(String(curr.id));
    }
  });

  writeJsonAtomic(SUMMARIES_CATALOG_FILE, summaries);
  writeJsonAtomic(DATA_SUMMARIES_CATALOG_FILE, summaries);

  return {
    success: true,
    type: 'spot_pearls',
    count: updatedIds.length,
    updatedIds,
    message: `${updatedIds.length} dersin spot bilgileri ve özetleri güncellendi.`,
  };
}

/**
 * Ingest practice questions into ornek_sorular
 */
export function ingestPracticeQuestions(payload: any): IngestionResult {
  const lectureId = payload.lectureId || payload.id || 'k1-genel';
  const questions = payload.questions || (Array.isArray(payload) ? payload : [payload]);
  const filePath = path.resolve(PRACTICE_QUESTIONS_DIR, 'k1', `${lectureId}.json`);

  const existing = readJsonSafe<any[]>(filePath, []);
  const merged = [...existing, ...questions];

  writeJsonAtomic(filePath, merged);

  return {
    success: true,
    type: 'practice_questions',
    count: questions.length,
    updatedIds: [lectureId],
    message: `${questions.length} örnek soru "${lectureId}.json" dosyasına başarıyla kaydedildi.`,
  };
}

/**
 * Ingest medical glossary & encyclopedia terms
 */
export function ingestGlossaryTerms(payload: any): IngestionResult {
  const terms: any[] = Array.isArray(payload)
    ? payload
    : Array.isArray(payload.terms)
      ? payload.terms
      : [payload];

  const glossary: Record<string, any> = readJsonSafe(GLOSSARY_FILE, {});
  const encyclopedia: any[] = readJsonSafe(ENCYCLOPEDIA_FILE, []);
  const updatedIds: string[] = [];

  terms.forEach((t) => {
    const termKey = String(t.term || t.name || '').toLowerCase().trim();
    if (!termKey) return;

    glossary[termKey] = {
      term: t.term || t.name,
      category: t.category || 'genel',
      definition: t.definition || '',
      pronunciation: t.pronunciation || t.latinName || '',
    };

    const encIdx = encyclopedia.findIndex((e) => String(e.term).toLowerCase().trim() === termKey);
    const encItem = {
      id: t.id || `enc-${termKey.replace(/\s+/g, '-')}`,
      term: t.term || t.name,
      latinName: t.latinName || '',
      category: t.category || 'genel',
      discipline: t.discipline || 'Genel Tıp',
      definition: t.definition || '',
      morphologyOrMechanism: t.morphologyOrMechanism || '',
      differentialDiagnosis: t.differentialDiagnosis || '',
      examSpotPearls: t.examSpotPearls || t.spot || '',
      pitfallsAndWarnings: t.pitfallsAndWarnings || '',
      updatedAt: new Date().toISOString(),
    };

    if (encIdx >= 0) {
      encyclopedia[encIdx] = { ...encyclopedia[encIdx], ...encItem };
    } else {
      encyclopedia.push(encItem);
    }

    updatedIds.push(termKey);
  });

  writeJsonAtomic(GLOSSARY_FILE, glossary);
  writeJsonAtomic(ENCYCLOPEDIA_FILE, encyclopedia);

  return {
    success: true,
    type: 'glossary_terms',
    count: updatedIds.length,
    updatedIds,
    message: `${updatedIds.length} tıbbi terim sözlüğe ve ansiklopediye işlendi.`,
  };
}

/**
 * Ingest flashcards into question_cards.json
 */
export function ingestFlashcards(payload: any): IngestionResult {
  const cards: any[] = Array.isArray(payload)
    ? payload
    : Array.isArray(payload.cards)
      ? payload.cards
      : [payload];

  const existingCards: any[] = readJsonSafe(FLASHCARDS_FILE, []);
  const updatedIds: string[] = [];

  cards.forEach((c) => {
    const cardId = c.id || `fc-nlm-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`;
    const newCard = {
      id: cardId,
      front: c.front || '',
      back: c.back || '',
      answer: c.answer || c.back || '',
      note: c.note || '',
      group: c.group || 'Genel Tıp',
      kurul: c.kurul || 1,
      options: c.options || undefined,
    };
    existingCards.push(newCard);
    updatedIds.push(cardId);
  });

  writeJsonAtomic(FLASHCARDS_FILE, existingCards);

  return {
    success: true,
    type: 'flashcards',
    count: updatedIds.length,
    updatedIds,
    message: `${updatedIds.length} akıl kartı question_cards.json dosyasına eklendi.`,
  };
}

// ---------------------------------------------------------------------------
// 4. NOTEBOOKLM INSTRUCTION CONTRACTS & PROMPTS
// ---------------------------------------------------------------------------

export function getNotebookLMContracts(): Record<string, any> {
  return {
    system_description: "MeDSor AI & Tıp Müfredatı Entegrasyon Altyapısı",
    instruction_overview: "NotebookLM'e kaynak olarak aktarılan tıp fakültesi ders notları ve çıkmış sorular üzerinde çalışırken, aşağıdaki görev tiplerine ait JSON şablonlarını kullanın. Çıktıyı doğrudan MeDSor sistemine yapıştırarak tüm veritabanını anında güncelleyebilirsiniz.",
    contracts: {
      past_question_correction: {
        description: "Çıkmış soru düzeltme, eksik şık tamamlama, cevap anahtarı doğrulama, öncül ayrıştırma ve şık analizi",
        required_schema: {
          type: "past_question_correction",
          questions: [
            {
              id: "0d5ceef7f165 (Mevcut soru güncellenecekse soru ID'si; yeni soru ise boş bırakılabilir)",
              kurul: 1,
              committeeId: "TIP310 (veya kurul numarasına göre otomatik atanır: 1->TIP310, 2->TIP311 vb.)",
              questionNumber: 15,
              examYear: "2023-2024",
              discipline: "Tıbbi Patoloji",
              topic: "Endometriyal Hiperplaziler ve Kanserler",
              stem: "Endometriyal hiperplaziler ve endometrioid karsinom gelişimi ile ilgili aşağıdaki ifadelerden hangileri doğrudur?",
              oncul_maddeleri: [
                "I. PTEN tümör baskılayıcı gen inaktivasyonu karsinojenezde en erken moleküler lezyondur.",
                "II. Atipisiz endometriyal hiperplazide kanser gelişme riski %25-50 düzeyindedir.",
                "III. En sık klinik başvuru semptomu perimenopozal veya postmenopozal anormal uterin kanamadır."
              ],
              options: [
                { "key": "A", "label": "A", "text": "Yalnız I", "isCorrect": false },
                { "key": "B", "label": "B", "text": "I ve III", "isCorrect": true },
                { "key": "C", "label": "C", "text": "II ve III", "isCorrect": false },
                { "key": "D", "label": "D", "text": "I, II ve III", "isCorrect": false },
                { "key": "E", "label": "E", "text": "Yalnız II", "isCorrect": false }
              ],
              correctAnswer: "B",
              explanation: "Fizyopatolojik gerekçe: PTEN mutasyonu endometriyal karsinojenezin en erken evresinde (%30-80) görülür. Karşılanmamış östrojen maruziyetine bağlı gelişen endometriyal hiperplazinin en sık semptomu anormal uterin kanamadır. Atipisiz hiperplazide kanserleşme riski %1-3 iken, atipili (EIN) hiperplazide bu risk %25-40'a yükselir.",
              sik_analizi: "A) Eksik: III. öncül de klinik pratikte en temel gerçektir.\nB) DOĞRU: I ve III fizyopatolojik ve klinik olarak teyitlidir.\nC) Yanlış: II. öncül yanlıştır (atipisiz hiperplazi riski %1-3'tür, %25-50 değildir).\nD) Yanlış: II. öncülün hatalı oranı nedeniyle elenir.\nE) Yanlış: II hem tek başına yanlış hem de eksiktir.",
              sourceNote: "Patoloji Ders Notu: Uterus Patolojisi (Slayt 24-28)",
              qualityTier: "altin"
            }
          ]
        }
      },
      interactive_deck: {
        description: "İnteraktif Öğrenme Slaytı ve Destesi Üretimi (OGREN_ETKILESIM_REHBERI.md kurallarına tam uyumlu)",
        required_schema: {
          type: "interactive_deck",
          deck: {
            id: "k1p-k1-55-konu-adi",
            title: "Ders Başlığı: Alt Başlık",
            committee: "donem3-kurul1",
            slides: [
              {
                id: "slide-1",
                slideNumber: 1,
                title: "Konu: Tanım ve Giriş",
                synthesisNarrative: "En az 60 kelime (ideal 70-150 kelime) nefes alan paragraflar ve - **Başlık:** Açıklama madde imleri ile yazılmış detaylı fizyopatolojik metin.\n\n> [!NOTE]\n> Klinik önem kutusu.",
                interactiveBlocks: [
                  {
                    type: "micro_quiz",
                    question: "Mekanizma odaklı sınav sorusu?",
                    options: [
                      { "key": "A", "text": "Çeldirici", "isCorrect": false, "explanation": "Gerekçe" },
                      { "key": "B", "text": "Doğru şık", "isCorrect": true, "explanation": "Gerekçe" }
                    ]
                  }
                ]
              }
            ]
          }
        }
      },
      spot_pearls: {
        description: "Yüksek verimli spot bilgiler ve ders özetleri güncellemesi",
        required_schema: {
          type: "spot_pearls",
          lectureId: "54_uterus_duz_kas_ve_trofoblastik_tumorleri",
          title: "Uterus Düz Kas ve Trofoblastik Tümörleri",
          keyPoints: [
            "- **Spot 1:** Leiomyosarkom de novo gelişir; leiomyom zemininden kaynaklanmaz.",
            "- **Spot 2:** Komplet mol 46,XX androgenetik olup p57 negatiftir."
          ]
        }
      },
      practice_questions: {
        description: "Amfi ders notuna sadık yeni örnek soru üretimi",
        required_schema: {
          type: "practice_questions",
          lectureId: "k1-54-uterus-tumorleri",
          questions: [
            {
              id: "ps-k1-54-01",
              stem: "Vaka veya mekanizma kökü...",
              options: [
                { "key": "A", "text": "..." },
                { "key": "B", "text": "..." },
                { "key": "C", "text": "..." },
                { "key": "D", "text": "..." },
                { "key": "E", "text": "..." }
              ],
              correctAnswer: "C",
              explanation: "Ders notu kaynaklı izahat...",
              subspecialty: "Tıbbi Patoloji"
            }
          ]
        }
      },
      glossary_terms: {
        description: "Tıbbi terimler sözlüğü ve ansiklopedi maddesi ekleme/güncelleme",
        required_schema: {
          type: "glossary_terms",
          terms: [
            {
              term: "Adenomyozis",
              latinName: "Adenomyosis uteri",
              category: "Patoloji",
              discipline: "Tıbbi Patoloji",
              definition: "Endometrial gland ve stromanın myometrium içinde bulunması.",
              morphologyOrMechanism: "Diffüz büyümüş küre şeklinde süngerimsi uterus; trabeküler yapı.",
              differentialDiagnosis: "Leiomyom (kapsüllü ve sınırlı) ve endometriozis.",
              examSpotPearls: "Siklik kanama göstermez (bazal tabaka kaynaklıdır); dismenore ve menoraji yapar."
            }
          ]
        }
      },
      flashcards: {
        description: "Hızlı aktif hatırlama akıl kartları",
        required_schema: {
          type: "flashcards",
          cards: [
            {
              front: "Leiomyosarkom triadında yer alan 3 histopatolojik kriter nedir?",
              back: "1. Belirgin nükleer atipi\n2. ≥10 mitoz / 10 BBA\n3. Koagülatif tümör hücre nekrozu",
              group: "Tıbbi Patoloji",
              note: "Herhangi 2 kriter varlığında bile malignite düşünülür."
            }
          ]
        }
      }
    }
  };
}
