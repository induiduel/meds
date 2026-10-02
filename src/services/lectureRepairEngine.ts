/**
 * ==============================================================================
 * Amfi Ders Notu Onarım ve Redakte Zenginleştirme Motoru
 * (src/services/lectureRepairEngine.ts)
 * ==============================================================================
 * Bu motor:
 * 1. lecture_notes.json (878 amfi slayt sunumu, 46.000+ slayt) ile
 *    lectureSummariesCatalog.json (347 redakte edilmiş amfi ders özeti) dosyalarını
 *    çapraz eşleştirir.
 * 2. OCR okuma hatası, boş slayt veya çok kısa (<30 karakter) olan slaytları tespit eder.
 * 3. Eşleşen redakte ders özetindeki akademik metinleri, spot bilgileri ve mekanizmaları
 *    bu slaytlara ekleyerek (repairedContent & redactedSupplement) slaytları onarır.
 * 4. Hem Slide Reader arayüzünde hem de RAG vektör indeksinde boş slayt yerine
 *    zenginleştirilmiş, eksiksiz tıbbi bilginin kullanılmasını sağlar.
 * ==============================================================================
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const DATA_DIR = path.resolve(PROJECT_ROOT, 'data');
const LECTURE_NOTES_FILE = path.resolve(DATA_DIR, 'lecture_notes.json');
const SUMMARIES_CATALOG_FILE = path.resolve(DATA_DIR, 'lectureSummariesCatalog.json');

export interface RepairStats {
  totalNotes: number;
  matchedNotes: number;
  totalSlides: number;
  emptySlidesFound: number;
  shortSlidesFound: number;
  slidesRepaired: number;
  repairedTimestamp: string;
}

function cleanTokens(str: string): Set<string> {
  const words = str.toLowerCase().match(/[a-zçğıöşü]{3,}/g) || [];
  const stopwords = new Set(['ders', 'notu', 'slayt', 'sunum', 'bolum', 'kurul', 'donem', 'tip', 'icin', 'olan']);
  return new Set(words.filter(w => !stopwords.has(w)));
}

/**
 * Execute automated cross-enrichment & slide repair
 */
export function repairAndEnrichLectureNotes(): RepairStats {
  if (!fs.existsSync(LECTURE_NOTES_FILE) || !fs.existsSync(SUMMARIES_CATALOG_FILE)) {
    console.warn('[LectureRepairEngine] Dosyalar eksik, onarım atlandı.');
    return {
      totalNotes: 0,
      matchedNotes: 0,
      totalSlides: 0,
      emptySlidesFound: 0,
      shortSlidesFound: 0,
      slidesRepaired: 0,
      repairedTimestamp: new Date().toISOString()
    };
  }

  const notes = JSON.parse(fs.readFileSync(LECTURE_NOTES_FILE, 'utf-8'));
  const summaries = JSON.parse(fs.readFileSync(SUMMARIES_CATALOG_FILE, 'utf-8'));

  // Pre-tokenize summaries
  const tokenizedSummaries = summaries.map((s: any) => ({
    raw: s,
    tokens: cleanTokens(s.title + ' ' + (s.discipline || ''))
  }));

  let matchedNotes = 0;
  let totalSlides = 0;
  let emptySlidesFound = 0;
  let shortSlidesFound = 0;
  let slidesRepaired = 0;

  for (const note of notes) {
    const noteTokens = cleanTokens(note.title + ' ' + (note.discipline || ''));
    
    // Find best matching summary
    let bestMatch: any = null;
    let maxOverlap = 0;

    for (const ts of tokenizedSummaries) {
      let overlap = 0;
      for (const t of noteTokens) {
        if (ts.tokens.has(t)) overlap++;
      }
      if (overlap > maxOverlap) {
        maxOverlap = overlap;
        bestMatch = ts.raw;
      }
    }

    if (maxOverlap >= 2 && bestMatch) {
      matchedNotes++;
      note.matchedSummaryId = bestMatch.id;
      note.matchedSummaryTitle = bestMatch.title;
      note.summaryKeyPoints = bestMatch.keyPoints || [];

      // Split summary into logical sections for slide supplementation
      const summarySections = (bestMatch.content || '').split(/\n(?=##\s+)/);

      if (Array.isArray(note.pages)) {
        totalSlides += note.pages.length;

        for (let pIdx = 0; pIdx < note.pages.length; pIdx++) {
          const page = note.pages[pIdx];
          const content = (page.content || '').trim();

          const isEmpty = content.length === 0;
          const isShort = content.length > 0 && content.length < 35;

          if (isEmpty) emptySlidesFound++;
          if (isShort) shortSlidesFound++;

          if (isEmpty || isShort) {
            // Assign a section from the redakte summary
            const targetSec = summarySections[pIdx % Math.max(1, summarySections.length)] || summarySections[0];
            if (targetSec && targetSec.trim().length > 30) {
              page.repairedContent = `[REDAKTE AMFİ NOTU İLE TAMAMLANDI]\n${targetSec.trim()}`;
              page.isRepairedWithRedaction = true;
              page.repairedSource = bestMatch.title;
              slidesRepaired++;
            }
          }
        }
      }
    }
  }

  // Save back to lecture_notes.json
  fs.writeFileSync(LECTURE_NOTES_FILE, JSON.stringify(notes, null, 2), 'utf-8');

  console.log('======================================================');
  console.log('✨ [LectureRepairEngine] Slayt Onarımı Tamamlandı');
  console.log(`• Toplam Sunum: ${notes.length} (Eşleşen: ${matchedNotes})`);
  console.log(`• Toplam Slayt Sayfası: ${totalSlides}`);
  console.log(`• Tespit Edilen Boş Slayt: ${emptySlidesFound}`);
  console.log(`• Tespit Edilen Kısa/Eksik Slayt: ${shortSlidesFound}`);
  console.log(`• Redakte Özetle Onarılan Slayt: ${slidesRepaired}`);
  console.log('======================================================');

  return {
    totalNotes: notes.length,
    matchedNotes,
    totalSlides,
    emptySlidesFound,
    shortSlidesFound,
    slidesRepaired,
    repairedTimestamp: new Date().toISOString()
  };
}
