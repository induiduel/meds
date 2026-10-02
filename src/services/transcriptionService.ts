/**
 * ==============================================================================
 * Amfi Ses Kayıtları Transkripsiyon Servisi
 * (src/services/transcriptionService.ts)
 * ==============================================================================
 * Bu servis:
 * C:\Users\indui\Desktop\meds_database\transcriptions klasöründeki ses kayıt
 * transkriptlerini okur, üstbilgilerini (başlık, branş, kurul, süre, kelime sayısı)
 * derler ve hem web arayüzünde okunması hem de RAG vektör sisteminde
 * sorgulanması için sunar.
 * ==============================================================================
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
export const TRANSCRIPTIONS_DIR = process.env.MEDS_TRANSCRIPTIONS_DIR || 'C:\\Users\\indui\\Desktop\\meds_database\\transcriptions';

export interface TranscriptionMeta {
  id: string;
  fileName: string;
  title: string;
  discipline: string;
  committeeId: string;
  charCount: number;
  wordCount: number;
  estimatedMinutes: number;
  sectionsCount: number;
  firstSnippet: string;
}

export interface TranscriptionDetail extends TranscriptionMeta {
  content: string;
  sections: Array<{
    title: string;
    level: number;
    content: string;
  }>;
}

let cachedMetas: TranscriptionMeta[] | null = null;
let cachedDetailsMap = new Map<string, TranscriptionDetail>();

function determineDisciplineAndCommittee(fileName: string, title: string): { discipline: string; committeeId: string } {
  const text = (fileName + ' ' + title).toLowerCase();
  
  let discipline = 'Tıbbi Patoloji';
  let committeeId = 'donem3-kurul1';

  if (text.includes('halk') || text.includes('salgin') || text.includes('ana cocuk')) {
    discipline = 'Halk Sağlığı';
    committeeId = 'donem3-kurul1';
  } else if (text.includes('genetik') || text.includes('dismorfoloji') || text.includes('kromozom')) {
    discipline = 'Tıbbi Genetik';
    committeeId = 'donem3-kurul1';
  } else if (text.includes('izolasyon') || text.includes('enfeksiyon') || text.includes('cinsel yolla')) {
    discipline = 'Enfeksiyon Hastalıkları';
    committeeId = 'donem3-kurul1';
  } else if (text.includes('fmf') || text.includes('akdeniz atesi') || text.includes('uriner') || text.includes('urolitiyazis')) {
    discipline = 'İç Hastalıkları / Üroloji';
    committeeId = 'donem3-kurul1';
  } else if (text.includes('hucre') || text.includes('hasar') || text.includes('nekroz') || text.includes('adaptasyon')) {
    discipline = 'Tıbbi Patoloji';
    committeeId = 'donem3-kurul1';
  }

  return { discipline, committeeId };
}

/**
 * Load all transcriptions list metadata
 */
export function getAllTranscriptionsMeta(): TranscriptionMeta[] {
  if (cachedMetas) return cachedMetas;

  if (!fs.existsSync(TRANSCRIPTIONS_DIR)) {
    console.warn('[TranscriptionService] Transkripsiyon klasörü bulunamadı:', TRANSCRIPTIONS_DIR);
    return [];
  }

  const files = fs.readdirSync(TRANSCRIPTIONS_DIR).filter(f => f.endsWith('.md'));
  const metas: TranscriptionMeta[] = [];

  for (const f of files) {
    const fullPath = path.join(TRANSCRIPTIONS_DIR, f);
    const content = fs.readFileSync(fullPath, 'utf-8');

    // Extract title from first H1 line
    const firstLineMatch = content.match(/^#\s*(.+)$/m);
    const title = firstLineMatch 
      ? firstLineMatch[1].replace(/^[🩺\s]+/, '').trim()
      : f.replace(/_Transkript\.md|_KUSURSUZ\.md|\.md/g, '').replace(/_/g, ' ');

    const { discipline, committeeId } = determineDisciplineAndCommittee(f, title);
    const id = f.replace(/\.md$/, '').toLowerCase();
    const wordCount = content.split(/\s+/).filter(Boolean).length;
    const charCount = content.length;
    const estimatedMinutes = Math.max(1, Math.round(wordCount / 140)); // ~140 wpm spoken lecture speed

    const sections = content.split(/\n(?=#{1,3}\s+)/);

    const firstSnippet = content
      .replace(/^#.+$/m, '')
      .trim()
      .slice(0, 220)
      .replace(/\n+/g, ' ') + '...';

    metas.push({
      id,
      fileName: f,
      title,
      discipline,
      committeeId,
      charCount,
      wordCount,
      estimatedMinutes,
      sectionsCount: sections.length,
      firstSnippet
    });
  }

  // Sort alphabetically by title
  metas.sort((a, b) => a.title.localeCompare(b.title, 'tr-TR'));
  cachedMetas = metas;
  return metas;
}

/**
 * Load full details for a single transcription
 */
export function getTranscriptionById(id: string): TranscriptionDetail | null {
  const normId = id.toLowerCase().replace(/\.md$/, '');
  if (cachedDetailsMap.has(normId)) {
    return cachedDetailsMap.get(normId)!;
  }

  const allMetas = getAllTranscriptionsMeta();
  const meta = allMetas.find(m => m.id === normId || m.fileName.toLowerCase().replace(/\.md$/, '') === normId);
  if (!meta) return null;

  const fullPath = path.join(TRANSCRIPTIONS_DIR, meta.fileName);
  if (!fs.existsSync(fullPath)) return null;

  const content = fs.readFileSync(fullPath, 'utf-8');
  const rawSections = content.split(/\n(?=#{1,3}\s+)/);
  
  const sections = rawSections.map((sec, idx) => {
    const headerMatch = sec.match(/^(#{1,3})\s+(.+)/);
    const level = headerMatch ? headerMatch[1].length : 2;
    const secTitle = headerMatch ? headerMatch[2].trim() : `Bölüm #${idx + 1}`;
    const secBody = sec.replace(/^#{1,3}\s+.+$/m, '').trim();
    return {
      title: secTitle,
      level,
      content: secBody
    };
  }).filter(s => s.content.length > 0 || s.title.length > 0);

  const detail: TranscriptionDetail = {
    ...meta,
    content,
    sections
  };

  cachedDetailsMap.set(normId, detail);
  return detail;
}

/**
 * Invalidate cache if files change
 */
export function clearTranscriptionCache(): void {
  cachedMetas = null;
  cachedDetailsMap.clear();
}
