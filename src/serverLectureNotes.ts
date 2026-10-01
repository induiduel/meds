import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const pdfParseModule = require('pdf-parse');
const PDFParse = pdfParseModule.PDFParse || pdfParseModule.default || pdfParseModule;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Root paths
const PROJECT_ROOT = path.resolve(__dirname, '..');
const DATA_DIR = path.resolve(PROJECT_ROOT, 'data');
const LECTURE_NOTES_FILE = path.resolve(DATA_DIR, 'lecture_notes.json');

// Default target folder on user's Desktop
export const DESKTOP_DATABASE_DIR = process.env.MEDS_DATABASE_DIR || 'C:\\Users\\indui\\Desktop\\meds_database';

export interface LecturePageItem {
  pageNumber: number;
  content: string;
  keywords: string[];
}

export interface LectureNoteRecord {
  id: string;
  committeeId: string;
  title: string;
  discipline: string;
  instructor?: string;
  totalSlides: number;
  pages: LecturePageItem[];
  source: 'desktop_folder' | 'web_upload' | 'drive';
  filePath?: string;
  fileHash?: string;
  fileSize?: number;
  lastScannedAt?: string;
  createdAt: string;
  updatedAt: string;
}

// Stopwords to filter out from auto-keyword extraction
const TURKISH_STOPWORDS = new Set([
  've', 'ile', 'veya', 'için', 'gibi', 'kadar', 'daha', 'olan', 'olarak', 'bunun',
  'buna', 'şekilde', 'olarak', 'üzere', 'bir', 'bu', 'şu', 'o', 'her', 'tüm', 'bütün',
  'sayfa', 'slayt', 'bölüm', 'ders', 'notu', 'konu', 'ünite', 'tablo', 'şekil', 'görsel',
  'the', 'and', 'for', 'with', 'from', 'that', 'this', 'are', 'was'
]);

/**
 * Infer medical discipline from filename or folder path
 */
export function inferDiscipline(nameOrPath: string): string {
  const lower = nameOrPath.toLowerCase();
  if (lower.includes('patoloji')) return 'Tıbbi Patoloji';
  if (lower.includes('farmakoloji') || lower.includes('ilac') || lower.includes('ilaç') || lower.includes('antihipertansif') || lower.includes('antibiyotik')) return 'Tıbbi Farmakoloji';
  if (lower.includes('mikrobiyoloji') || lower.includes('bakteri') || lower.includes('viroloji') || lower.includes('parazit') || lower.includes('mantar')) return 'Tıbbi Mikrobiyoloji';
  if (lower.includes('genetik') || lower.includes('sitogenetik') || lower.includes('mutasyon')) return 'Tıbbi Genetik';
  if (lower.includes('halk sağlığı') || lower.includes('halk sagligi') || lower.includes('epidemiyoloji') || lower.includes('istatistik')) return 'Halk Sağlığı';
  if (lower.includes('üroloji') || lower.includes('uroloji')) return 'Üroloji';
  if (lower.includes('enfeksiyon')) return 'Enfeksiyon Hastalıkları';
  if (lower.includes('biyokimya') || lower.includes('enzim') || lower.includes('metabolizma')) return 'Tıbbi Biyokimya';
  if (lower.includes('fizyoloji')) return 'Tıbbi Fizyoloji';
  if (lower.includes('anatomi') || lower.includes('histoloji') || lower.includes('embriyoloji')) return 'Tıbbi Anatomi / Histoloji';
  if (lower.includes('dahiliye') || lower.includes('iç hastalıkları') || lower.includes('ic hastaliklari')) return 'İç Hastalıkları';
  if (lower.includes('kardiyo')) return 'Kardiyoloji';
  if (lower.includes('pediatri') || lower.includes('çocuk') || lower.includes('yenidoğan')) return 'Çocuk Sağlığı ve Hastalıkları';
  if (lower.includes('genel cerrahi')) return 'Genel Cerrahi';
  if (lower.includes('nöro') || lower.includes('noro') || lower.includes('psikiyatri')) return 'Nöroloji / Nöroşirürji';
  if (lower.includes('göz') || lower.includes('oftalmoloji')) return 'Göz Hastalıkları';
  if (lower.includes('kbb') || lower.includes('kulak burun')) return 'Kulak Burun Boğaz';
  if (lower.includes('derma') || lower.includes('cildiye')) return 'Dermatoloji';
  return 'Tıp Ders Notu';
}

/**
 * Extract meaningful keywords directly from the page text (strictly verbatim, no AI hallucinations)
 */
export function extractVerbatimKeywords(text: string): string[] {
  if (!text) return [];
  const words = text
    .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?"'’“”…\[\]<>|\\]/g, ' ')
    .split(/\s+/)
    .map(w => w.trim().toLowerCase())
    .filter(w => w.length >= 4 && !TURKISH_STOPWORDS.has(w) && !/^\d+$/.test(w));

  const freqMap = new Map<string, number>();
  for (const w of words) {
    freqMap.set(w, (freqMap.get(w) || 0) + 1);
  }

  // Sort by frequency descending and take top 10 unique words
  return Array.from(freqMap.entries())
    .sort((a, b) => b[1] - a[1])
    .map(entry => entry[0])
    .slice(0, 10);
}

export interface SlideMatchResult {
  noteId: string;
  noteTitle: string;
  discipline: string;
  committeeId: string;
  pageNumber: number;
  totalSlides: number;
  score: number;
  snippet: string;
  fullContent: string;
  keywords: string[];
  reasoning: string;
  driveFileUrl?: string;
}

let cachedNotes: LectureNoteRecord[] | null = null;
let lastNotesMtime = 0;

/**
 * Load all lecture notes from data/lecture_notes.json with high-speed memory caching
 */
export function getCachedLectureNotes(): LectureNoteRecord[] {
  try {
    let targetPath = LECTURE_NOTES_FILE;
    if (!fs.existsSync(targetPath)) {
      const srcPath = path.resolve(PROJECT_ROOT, 'src', 'data', 'lecture_notes.json');
      if (fs.existsSync(srcPath)) targetPath = srcPath;
    }

    if (fs.existsSync(targetPath)) {
      const stat = fs.statSync(targetPath);
      if (!cachedNotes || stat.mtimeMs !== lastNotesMtime) {
        const raw = fs.readFileSync(targetPath, 'utf-8');
        cachedNotes = JSON.parse(raw);
        lastNotesMtime = stat.mtimeMs;
      }
      return cachedNotes || [];
    }
  } catch (err) {
    console.error('[LectureNotesManager] Error reading lecture notes cache:', err);
  }
  return getAllLectureNotes();
}

/**
 * High-speed slide search engine: finds best matching lecture notes & specific slides for a given question
 */
export function findBestMatchingLectureSlides(
  queryText: string,
  disciplineHint?: string,
  committeeId?: string,
  limit: number = 3
): SlideMatchResult[] {
  if (!queryText || !queryText.trim()) return [];

  const notes = getCachedLectureNotes();
  if (!notes || notes.length === 0) return [];

  // Normalize query
  const cleanQuery = queryText
    .replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?"'’“”…\[\]<>|\\]/g, ' ')
    .toLowerCase();

  const words = cleanQuery
    .split(/\s+/)
    .map(w => w.trim())
    .filter(w => w.length >= 3 && !TURKISH_STOPWORDS.has(w));

  if (words.length === 0) return [];

  // Bigrams for high-precision phrases (e.g. "antihipertansif ilac", "papiller karsinom", "kuru oksuruk")
  const bigrams: string[] = [];
  for (let i = 0; i < words.length - 1; i++) {
    bigrams.push(`${words[i]} ${words[i + 1]}`);
  }

  const results: SlideMatchResult[] = [];

  for (const note of notes) {
    const noteTitleNorm = (note.title || '').toLowerCase();
    const effectiveDiscipline = note.discipline && note.discipline !== 'Tıp Ders Notu' 
      ? note.discipline 
      : inferDiscipline(note.title);
    const noteDisciplineNorm = effectiveDiscipline.toLowerCase();

    let noteBaseBonus = 0;
    if (committeeId && note.committeeId === committeeId) {
      noteBaseBonus += 15;
    }
    if (disciplineHint && (noteDisciplineNorm.includes(disciplineHint.toLowerCase()) || disciplineHint.toLowerCase().includes(noteDisciplineNorm))) {
      noteBaseBonus += 25;
    }
    // Check if words match note title
    for (const w of words) {
      if (noteTitleNorm.includes(w)) {
        noteBaseBonus += 20;
      }
    }

    for (const page of note.pages || []) {
      const content = page.content || '';
      if (!content || content.length < 10) continue;
      const contentNorm = content.toLowerCase();

      let pageScore = noteBaseBonus;
      const matchedTerms: string[] = [];

      // Check bigram matches (very strong signal)
      for (const bg of bigrams) {
        if (contentNorm.includes(bg)) {
          pageScore += 45;
          matchedTerms.push(bg);
        }
      }

      // Check word matches
      for (const w of words) {
        if (contentNorm.includes(w)) {
          pageScore += 12;
          if (!matchedTerms.includes(w)) matchedTerms.push(w);
        }
      }

      // Check keywords list on page
      for (const kw of page.keywords || []) {
        const kwNorm = kw.toLowerCase();
        if (cleanQuery.includes(kwNorm)) {
          pageScore += 15;
          if (!matchedTerms.includes(kw)) matchedTerms.push(kw);
        }
      }

      if (pageScore >= 35 && matchedTerms.length >= 1) {
        // Build concise snippet around the best match
        let bestSnippet = content.slice(0, 240).replace(/\s+/g, ' ');
        for (const term of matchedTerms) {
          const idx = contentNorm.indexOf(term.toLowerCase());
          if (idx !== -1) {
            const start = Math.max(0, idx - 60);
            const end = Math.min(content.length, idx + term.length + 120);
            bestSnippet = (start > 0 ? '...' : '') + content.slice(start, end).replace(/\s+/g, ' ') + (end < content.length ? '...' : '');
            break;
          }
        }

        results.push({
          noteId: note.id,
          noteTitle: note.title,
          discipline: effectiveDiscipline,
          committeeId: note.committeeId,
          pageNumber: page.pageNumber,
          totalSlides: note.totalSlides || (note.pages ? note.pages.length : 1),
          score: Math.min(100, pageScore),
          snippet: bestSnippet,
          fullContent: content.slice(0, 1500),
          keywords: page.keywords || [],
          reasoning: `Amfi Slayt Eşleşmesi: "${note.title}" dersinin ${page.pageNumber}. slaytındaki (${matchedTerms.slice(0, 4).join(', ')}) ifadeleri soru içeriği ile örtüşmektedir.`,
          driveFileUrl: (note as any).driveFileUrl
        });
      }
    }
  }

  // Sort by score descending and return top matches
  results.sort((a, b) => b.score - a.score);
  return results.slice(0, limit);
}

/**
 * Load all lecture notes from data/lecture_notes.json
 */
export function getAllLectureNotes(): LectureNoteRecord[] {
  try {
    if (!fs.existsSync(DATA_DIR)) {
      fs.mkdirSync(DATA_DIR, { recursive: true });
    }
    if (fs.existsSync(LECTURE_NOTES_FILE)) {
      const raw = fs.readFileSync(LECTURE_NOTES_FILE, 'utf-8');
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        return parsed;
      }
    }
    const srcPath = path.resolve(PROJECT_ROOT, 'src', 'data', 'lecture_notes.json');
    if (fs.existsSync(srcPath)) {
      const raw = fs.readFileSync(srcPath, 'utf-8');
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) return parsed;
    }
  } catch (err) {
    console.error('[LectureNotesManager] Error reading lecture_notes.json:', err);
  }
  return [];
}
export async function extractVerbatimPdfPages(
  buffer: Buffer,
  fileName?: string
): Promise<{
  pages: LecturePageItem[];
  totalPages: number;
  fullText: string;
  title: string;
  discipline: string;
  instructor?: string;
}> {
  let rawPages: Array<{ num: number; text: string }> = [];
  let fullText = '';

  if (typeof PDFParse === 'function' && PDFParse.prototype?.getText) {
    const parser = new PDFParse({ data: buffer });
    try {
      const parsed = await parser.getText();
      if (parsed.pages && Array.isArray(parsed.pages) && parsed.pages.length > 0) {
        rawPages = parsed.pages.map((p: any) => ({
          num: p.num || 0,
          text: (p.text || '').trim(),
        }));
      } else if (parsed.text) {
        fullText = parsed.text;
        // Split by form feeds or multiple newlines
        const splits = fullText.split(/\f|\n{4,}/);
        rawPages = splits.map((s, idx) => ({ num: idx + 1, text: s.trim() }));
      }
    } finally {
      await parser.destroy?.();
    }
  } else if (typeof pdfParseModule === 'function') {
    const parsed = await pdfParseModule(buffer);
    fullText = parsed.text || '';
    const splits = fullText.split(/\f|\n{4,}/);
    rawPages = splits.map((s: string, idx: number) => ({ num: idx + 1, text: s.trim() }));
  }

  // Sort pages by page number
  rawPages.sort((a, b) => a.num - b.num);

  // If no pages were parsed at all, provide a single initial page
  if (rawPages.length === 0) {
    rawPages = [{ num: 1, text: fullText.trim() }];
  }

  let cleanTitle = fileName
    ? fileName.replace(/\.[^/.]+$/, '').trim()
    : 'Ders Notu Belgesi';

  let instructor: string | undefined = undefined;

  // Scan first 3 pages to extract meaningful title and instructor if filename is short/cryptic
  const firstPagesText = rawPages.slice(0, 3).map(p => p.text).join('\n');
  const instructorMatch = firstPagesText.match(/(?:Prof\.|Doç\.|Dr\.)\s*(?:Dr\.)?\s*([A-ZÇĞİÖŞÜa-zçğıöşü\s]{3,30})/);
  if (instructorMatch) {
    instructor = instructorMatch[0].replace(/\s+/g, ' ').trim();
  }

  // If cleanTitle is short (<= 4 chars, e.g. g17, p01) or generic
  if (cleanTitle.length <= 4 || /^(ders|not|slayt)[\s_-]*\d*$/i.test(cleanTitle)) {
    const lines = firstPagesText
      .split('\n')
      .map(l => l.replace(/[\r\t]+/g, ' ').trim())
      .filter(l => l.length > 5 && !l.startsWith('--') && !/^(prof|doç|dr\.)/i.test(l) && !/^\d+\s*[-.]/i.test(l));

    if (lines.length > 0) {
      const candidate = lines[0].replace(/^o\s+/i, '').replace(/^[•\-*]\s*/, '').trim();
      if (candidate.length > 3) {
        cleanTitle = `${candidate} (${fileName?.replace(/\.[^/.]+$/, '')})`;
      }
    }
  }

  const discipline = inferDiscipline(fileName + ' ' + cleanTitle + ' ' + firstPagesText.slice(0, 1000));

  const pages: LecturePageItem[] = rawPages.map((p, index) => {
    const pageNum = p.num || index + 1;
    // Clean null bytes and strange control characters
    const cleanText = (p.text || '')
      .replace(/\u0000/g, '')
      .replace(/[\r\t]+/g, ' ')
      .trim();

    const content = cleanText.length > 0
      ? cleanText
      : `[Sayfa ${pageNum}: Görsel / Şema]`;

    return {
      pageNumber: pageNum,
      content,
      keywords: extractVerbatimKeywords(cleanText),
    };
  });

  const assembledFullText = pages.map(p => `--- Sayfa ${p.pageNumber} ---\n${p.content}`).join('\n\n');

  return {
    pages,
    totalPages: pages.length,
    fullText: assembledFullText,
    title: cleanTitle,
    discipline,
    instructor,
  };
}

/**
 * Save or update a single lecture note in data/lecture_notes.json
 */
export function saveLectureNote(note: Partial<LectureNoteRecord> & { title: string }): LectureNoteRecord {
  const notes = getAllLectureNotes();
  const id = note.id || `note-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`;
  const now = new Date().toISOString();

  const record: LectureNoteRecord = {
    id,
    committeeId: note.committeeId || 'donem3-kurul1',
    title: note.title,
    discipline: note.discipline || inferDiscipline(note.title),
    instructor: note.instructor || undefined,
    totalSlides: note.pages?.length || note.totalSlides || 1,
    pages: note.pages || [],
    source: note.source || 'web_upload',
    filePath: note.filePath || undefined,
    fileHash: note.fileHash || undefined,
    fileSize: note.fileSize || undefined,
    lastScannedAt: now,
    createdAt: note.createdAt || now,
    updatedAt: now,
  };

  const existingIndex = notes.findIndex(n => n.id === id || (note.filePath && n.filePath === note.filePath));
  if (existingIndex >= 0) {
    notes[existingIndex] = {
      ...notes[existingIndex],
      ...record,
      createdAt: notes[existingIndex].createdAt || record.createdAt,
      updatedAt: now,
    };
  } else {
    notes.unshift(record);
  }

  fs.writeFileSync(LECTURE_NOTES_FILE, JSON.stringify(notes, null, 2), 'utf-8');
  console.log(`[LectureNotesManager] Saved "${record.title}" (${record.totalSlides} pages) to database.`);
  return record;
}

/**
 * Delete a lecture note by ID
 */
export function deleteLectureNote(id: string): boolean {
  try {
    const notes = getAllLectureNotes();
    const filtered = notes.filter(n => n.id !== id);
    if (filtered.length !== notes.length) {
      fs.writeFileSync(LECTURE_NOTES_FILE, JSON.stringify(filtered, null, 2), 'utf-8');
      return true;
    }
  } catch (err) {
    console.error('[LectureNotesManager] Error deleting note:', err);
  }
  return false;
}

/**
 * Verbatim rendering of a slide
 */
// Helper to download binary buffer from Google Drive with redirect follow
function downloadDriveBuffer(fileId: string): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    const https = require('https');
    const initialUrl = `https://drive.usercontent.google.com/download?id=${fileId}&export=download&authuser=0&confirm=t`;
    function makeReq(url: string, redCount = 0) {
      if (redCount > 5) return reject(new Error('Çok fazla yönlendirme'));
      https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' } }, (res: any) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          return makeReq(res.headers.location, redCount + 1);
        }
        if (res.statusCode !== 200) {
          return reject(new Error(`HTTP Durumu: ${res.statusCode}`));
        }
        const chunks: Buffer[] = [];
        res.on('data', (c: Buffer) => chunks.push(c));
        res.on('end', () => resolve(Buffer.concat(chunks)));
        res.on('error', reject);
      }).on('error', reject);
    }
    makeReq(initialUrl);
  });
}

/**
 * Verbatim rendering of a slide:
 * 1. Checks C:\Users\indui\Desktop\meds_database (and subdirs: ders_notlari_pdf, meds_sorular)
 * 2. If not found, downloads reliably from Google Drive with redirect support
 * 3. Extracts verbatim text page-by-page using PDFParse
 * 4. Saves note to database and returns the record
 */
export async function renderSlideVerbatim(params: {
  id: string;
  title: string;
  discipline: string;
  fileId?: string;
  committeeId?: string;
}): Promise<LectureNoteRecord> {
  const { id, title, discipline, fileId, committeeId = 'donem3-kurul1' } = params;

  let targetBuffer: Buffer | null = null;
  let sourcePath: string | undefined = undefined;
  let source: 'desktop_folder' | 'drive' = 'desktop_folder';

  // Turkish & medical synonym normalization
  const normalizeForMatch = (s: string) => {
    if (!s) return '';
    return s
      .replace(/İ/g, 'i')
      .replace(/I/g, 'ı')
      .toLowerCase()
      .replace(/intrasell[uü]ler/gi, 'hücre içi')
      .replace(/ekstrasell[uü]ler/gi, 'hücre dışı')
      .replace(/enflamasyon/gi, 'iltihap')
      .replace(/[^a-z0-9ğüşıöç]/gi, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  };

  // 1. Find all PDF files recursively inside meds_database (ders_notlari_pdf prioritized)
  const getAllLocalPdfs = (): { fullPath: string; fileName: string; folder: string }[] => {
    const results: { fullPath: string; fileName: string; folder: string }[] = [];
    const searchDirs = [
      path.join(DESKTOP_DATABASE_DIR, 'ders_notlari_pdf'),
      DESKTOP_DATABASE_DIR,
      path.join(DESKTOP_DATABASE_DIR, 'meds_sorular'),
    ];

    const visitedPaths = new Set<string>();

    const scan = (dir: string) => {
      if (!fs.existsSync(dir)) return;
      try {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        for (const entry of entries) {
          const full = path.join(dir, entry.name);
          if (entry.isDirectory()) {
            scan(full);
          } else if (entry.isFile() && entry.name.toLowerCase().endsWith('.pdf')) {
            const key = full.toLowerCase();
            if (!visitedPaths.has(key)) {
              visitedPaths.add(key);
              results.push({
                fullPath: full,
                fileName: entry.name,
                folder: dir,
              });
            }
          }
        }
      } catch (e) {}
    };

    for (const d of searchDirs) {
      scan(d);
    }
    return results;
  };

  const localPdfs = getAllLocalPdfs();
  const cleanTitle = normalizeForMatch(title);
  const titleTokens = cleanTitle.split(' ').filter(w => w.length > 2 && !TURKISH_STOPWORDS.has(w));
  const numMatch = title.match(/^(\d{1,2})/);
  const titleNum = numMatch ? numMatch[1] : null;

  let bestCandidate: { fullPath: string; score: number } | null = null;

  for (const item of localPdfs) {
    const cleanFileName = normalizeForMatch(item.fileName.replace(/\.pdf$/i, ''));
    const fileTokens = new Set(cleanFileName.split(' ').filter(w => w.length > 2));
    const fileNumMatch = item.fileName.match(/^(\d{1,2})/);
    const fileNum = fileNumMatch ? fileNumMatch[1] : null;

    let score = 0;

    // Exact match
    if (cleanFileName === cleanTitle) {
      score += 100;
    } else if (cleanFileName.includes(cleanTitle) || cleanTitle.includes(cleanFileName)) {
      score += 70;
    }

    // Number match
    if (titleNum && fileNum) {
      if (titleNum === fileNum) {
        score += 35;
      } else {
        score -= 50; // Different starting chapter number
      }
    }

    // Token overlap
    let matchCount = 0;
    for (const t of titleTokens) {
      if (fileTokens.has(t) || cleanFileName.includes(t)) {
        matchCount++;
      }
    }
    if (titleTokens.length > 0) {
      score += Math.round((matchCount / titleTokens.length) * 50);
    }

    // Discipline match bonus
    if (discipline && (item.fullPath.toLowerCase().includes(discipline.toLowerCase()) || cleanFileName.includes(normalizeForMatch(discipline)))) {
      score += 20;
    }

    // Prioritize ders_notlari_pdf
    if (item.folder.toLowerCase().includes('ders_notlari_pdf')) {
      score += 15;
    }

    if (score >= 40) {
      if (!bestCandidate || score > bestCandidate.score) {
        bestCandidate = { fullPath: item.fullPath, score };
      }
    }
  }

  if (bestCandidate) {
    try {
      targetBuffer = fs.readFileSync(bestCandidate.fullPath);
      sourcePath = bestCandidate.fullPath;
      console.log(`[RenderVerbatim] Yerel klasörde eşleşti (Skor: ${bestCandidate.score}): ${bestCandidate.fullPath}`);
    } catch (e) {}
  }

  // 2. Fallback: Google Drive Download
  let effectiveFileId = fileId;
  if (!targetBuffer && !effectiveFileId) {
    try {
      const realSlidesPath = path.resolve(DATA_DIR, 'real_drive_slides.json');
      if (fs.existsSync(realSlidesPath)) {
        const slides = JSON.parse(fs.readFileSync(realSlidesPath, 'utf8'));
        const match = slides.find((s: any) => 
          s.id === id || 
          normalizeForMatch(s.name).includes(cleanTitle) || 
          cleanTitle.includes(normalizeForMatch(s.name))
        );
        if (match?.id) effectiveFileId = match.id;
      }
    } catch (e) {}
  }

  if (!targetBuffer && effectiveFileId) {
    console.log(`[RenderVerbatim] Google Drive'dan güvenli indiriliyor (fileId: ${effectiveFileId}, title: "${title}")...`);
    try {
      const buf = await downloadDriveBuffer(effectiveFileId);
      if (buf && buf.slice(0, 5).toString() === '%PDF-') {
        targetBuffer = buf;
        source = 'drive';
        // Cache directly to meds_database/ders_notlari_pdf
        try {
          const cacheDir = path.join(DESKTOP_DATABASE_DIR, 'ders_notlari_pdf');
          if (!fs.existsSync(cacheDir)) {
            fs.mkdirSync(cacheDir, { recursive: true });
          }
          const safeName = title.replace(/[/\\?%*:|"<>]/g, '_') + '.pdf';
          const localDest = path.join(cacheDir, safeName);
          if (!fs.existsSync(localDest)) {
            fs.writeFileSync(localDest, buf);
            console.log(`[RenderVerbatim] PDF yerel önbelleğe kaydedildi: ${localDest}`);
          }
          sourcePath = localDest;
        } catch (e) {}
      }
    } catch (e: any) {
      console.warn(`[RenderVerbatim] Google Drive indirme hatası (${effectiveFileId}):`, e.message);
    }
  }

  if (!targetBuffer) {
    throw new Error(
      `"${title}" dersine ait PDF dosyası C:\\Users\\indui\\Desktop\\meds_database\\ders_notlari_pdf klasöründe ve alt dizinlerde bulunamadı. Lütfen ilgili PDF belgesinin ders_notlari_pdf klasörüne eklendiğinden emin olunuz.`
    );
  }

  // 3. Extract 100% verbatim text page by page
  const extracted = await extractVerbatimPdfPages(targetBuffer, `${title}.pdf`);

  const record: LectureNoteRecord = {
    id,
    committeeId,
    title,
    discipline: discipline || extracted.discipline,
    instructor: extracted.instructor,
    totalSlides: extracted.totalPages,
    pages: extracted.pages,
    source,
    filePath: sourcePath,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  saveLectureNote(record);
  return record;
}

/**
 * Scan target folder (C:\Users\indui\Desktop\meds_database) for all PDFs and DOCX files.
 * Extracts verbatim content from all pages and updates the database.
 */
export async function scanDesktopDatabaseFolder(folderPath: string = DESKTOP_DATABASE_DIR): Promise<{
  success: boolean;
  folderPath: string;
  totalFilesFound: number;
  newlyAdded: number;
  updated: number;
  totalNotes: number;
  processedFiles: string[];
}> {
  console.log(`[DesktopSync] 🔍 Taranıyor: ${folderPath}`);

  if (!fs.existsSync(folderPath)) {
    try {
      fs.mkdirSync(folderPath, { recursive: true });
      console.log(`[DesktopSync] Klasör oluşturuldu: ${folderPath}`);
    } catch (e: any) {
      console.error(`[DesktopSync] Klasör oluşturulamadı: ${e.message}`);
      return {
        success: false,
        folderPath,
        totalFilesFound: 0,
        newlyAdded: 0,
        updated: 0,
        totalNotes: getAllLectureNotes().length,
        processedFiles: [],
      };
    }
  }

  // Find all PDF and DOCX files recursively
  const findFiles = (dir: string): string[] => {
    let results: string[] = [];
    try {
      const list = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of list) {
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          results = results.concat(findFiles(full));
        } else if (entry.isFile()) {
          const ext = path.extname(entry.name).toLowerCase();
          if (ext === '.pdf' || ext === '.docx') {
            results.push(full);
          }
        }
      }
    } catch (e: any) {
      console.warn(`[DesktopSync] Dizin okuma uyarısı (${dir}):`, e.message);
    }
    return results;
  };

  const files = findFiles(folderPath);
  console.log(`[DesktopSync] Bulunan belge sayısı: ${files.length}`);

  let newlyAdded = 0;
  let updated = 0;
  const processedFiles: string[] = [];
  const existingNotes = getAllLectureNotes();

  for (const filePath of files) {
    try {
      const fileName = path.basename(filePath);
      const stats = fs.statSync(filePath);

      // Fast check: If file already indexed with identical path and size, skip without reading buffer
      const existingByPath = existingNotes.find(n => n.filePath === filePath);
      if (existingByPath && existingByPath.fileSize === stats.size && existingByPath.totalSlides > 0 && existingByPath.pages?.length > 0) {
        continue;
      }

      const buffer = fs.readFileSync(filePath);
      const hash = crypto.createHash('md5').update(buffer).digest('hex');

      // Check if file already processed with matching hash
      const existing = existingByPath || existingNotes.find(n => n.fileHash === hash);
      if (existing && existing.fileHash === hash && existing.totalSlides > 0 && existing.pages?.length > 0) {
        continue;
      }

      console.log(`[DesktopSync] ⚙️ İşleniyor: "${fileName}" (${(stats.size / 1024 / 1024).toFixed(2)} MB)...`);
      const isPdf = fileName.toLowerCase().endsWith('.pdf');

      let pages: LecturePageItem[] = [];
      let totalSlides = 0;
      let discipline = inferDiscipline(filePath);
      let title = fileName.replace(/\.[^/.]+$/, '').trim();
      let instructor: string | undefined = undefined;

      if (isPdf) {
        const extracted = await extractVerbatimPdfPages(buffer, fileName);
        pages = extracted.pages;
        totalSlides = extracted.totalPages;
        discipline = extracted.discipline;
        title = extracted.title;
        instructor = extracted.instructor;
      }

      const noteRecord: Partial<LectureNoteRecord> & { title: string } = {
        id: existing?.id || `note-${hash.slice(0, 10)}`,
        committeeId: 'donem3-kurul1',
        title,
        discipline,
        instructor,
        totalSlides,
        pages,
        source: 'desktop_folder',
        filePath,
        fileHash: hash,
        fileSize: stats.size,
      };

      saveLectureNote(noteRecord);
      processedFiles.push(fileName);

      if (existing) {
        updated++;
      } else {
        newlyAdded++;
      }

      console.log(`[DesktopSync] ✓ "${fileName}" başarıyla kaydedildi: Toplam ${totalSlides} sayfa birebir metin çıkarıldı.`);
    } catch (err: any) {
      console.error(`[DesktopSync] Hata (${filePath}):`, err.message);
    }
  }

  const finalNotes = getAllLectureNotes();
  return {
    success: true,
    folderPath,
    totalFilesFound: files.length,
    newlyAdded,
    updated,
    totalNotes: finalNotes.length,
    processedFiles,
  };
}

// In-memory status for monitoring
let lastScanResult: any = null;
let lastScanTime: string | null = null;
let watcherActive = false;

export function getDesktopFolderStatus() {
  const filesCount = fs.existsSync(DESKTOP_DATABASE_DIR)
    ? fs.readdirSync(DESKTOP_DATABASE_DIR).filter(f => f.toLowerCase().endsWith('.pdf') || f.toLowerCase().endsWith('.docx')).length
    : 0;

  return {
    folderPath: DESKTOP_DATABASE_DIR,
    folderExists: fs.existsSync(DESKTOP_DATABASE_DIR),
    filesCount,
    lastScanTime,
    lastScanResult,
    watcherActive,
    scheduledHour: 18,
    scheduleDescription: 'Her gün saat 18:00 (Ayrıca klasöre yeni dosya atıldığında anında otomatik)',
    totalDatabaseNotes: getAllLectureNotes().length,
  };
}

/**
 * Start the folder watcher and daily 18:00 scheduler
 */
export function startDesktopFolderWatcherAndScheduler(folderPath: string = DESKTOP_DATABASE_DIR) {
  console.log(`[DesktopSync] 🕒 Otomasyon başlatılıyor. Hedef Klasör: ${folderPath}`);

  // 1. Initial scan on server boot
  setTimeout(async () => {
    try {
      console.log(`[DesktopSync] İlk açılış taraması başlatılıyor...`);
      lastScanResult = await scanDesktopDatabaseFolder(folderPath);
      lastScanTime = new Date().toISOString();
    } catch (e: any) {
      console.error('[DesktopSync] İlk açılış taraması hatası:', e.message);
    }
  }, 2000);

  // 2. Watcher for instant detection when user drops a PDF into the folder
  if (!watcherActive && fs.existsSync(folderPath)) {
    try {
      let debounceTimer: NodeJS.Timeout | null = null;
      fs.watch(folderPath, { recursive: true }, (eventType, filename) => {
        if (!filename) return;
        const ext = path.extname(filename).toLowerCase();
        if (ext === '.pdf' || ext === '.docx') {
          console.log(`[DesktopSync] 📂 Klasörde değişiklik tespit edildi (${eventType}): ${filename}`);
          if (debounceTimer) clearTimeout(debounceTimer);
          debounceTimer = setTimeout(async () => {
            console.log(`[DesktopSync] 🔄 Otomatik senkronizasyon tetiklendi...`);
            lastScanResult = await scanDesktopDatabaseFolder(folderPath);
            lastScanTime = new Date().toISOString();
          }, 3000);
        }
      });
      watcherActive = true;
      console.log(`[DesktopSync] 👁️ Gerçek zamanlı dosya izleyici devrede (fs.watch).`);
    } catch (e: any) {
      console.warn('[DesktopSync] fs.watch başlatılamadı:', e.message);
    }
  }

  // 3. Daily 18:00 Scheduler Check (checked every 30 seconds)
  let lastRanDateString = '';
  setInterval(async () => {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const dateStr = now.toDateString();

    // Trigger exactly at 18:00 (runs once per day)
    if (hours === 18 && minutes === 0 && lastRanDateString !== dateStr) {
      lastRanDateString = dateStr;
      console.log(`\n========================================================`);
      console.log(`[18:00 OTOMASYONU] ⏰ Saat 18:00 - Günlük ders notu senkronizasyonu başlatılıyor...`);
      console.log(`========================================================\n`);
      try {
        lastScanResult = await scanDesktopDatabaseFolder(folderPath);
        lastScanTime = new Date().toISOString();
        console.log(`[18:00 OTOMASYONU] Tamamlandı: ${lastScanResult.newlyAdded} yeni, ${lastScanResult.updated} güncellendi.`);
      } catch (err: any) {
        console.error('[18:00 OTOMASYONU] Hata:', err.message);
      }
    }
  }, 30000);
}
