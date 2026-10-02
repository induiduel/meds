/**
 * MedSoru Ders Özetleri ve Spot Bilgi Kataloğu Derleyicisi
 * (scripts/compile-summaries-catalog.mjs)
 * 
 * C:\Users\indui\Desktop\meds_database\redakte_ozet altındaki 347 adet
 * Markdown ders özetini okur, ayrıştırır ve web uygulamasında anında
 * görüntülenebilmesi için src/data/lectureSummariesCatalog.json ve
 * data/lectureSummariesCatalog.json dosyalarına derler.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');
const SRC_SUMMARIES_DIR = 'C:\\Users\\indui\\Desktop\\meds_database\\redakte_ozet';
const FALLBACK_SUMMARIES_DIR = 'C:\\Users\\indui\\Desktop\\meds_database\\kurul_ders_notlari_ozet';
const OUT_DATA_PATH = path.join(ROOT_DIR, 'data', 'lectureSummariesCatalog.json');
const OUT_SRC_PATH = path.join(ROOT_DIR, 'src', 'data', 'lectureSummariesCatalog.json');

function cleanTitle(title) {
  if (!title) return '';
  return title
    .replace(/\.(md|txt|pdf)$/i, '')
    .replace(/^(\d+[\.\-\)]\s*)+/, '')
    .replace(/[_]+/g, ' ')
    .trim();
}

function extractKeyPointsFromMarkdown(content, maxPoints = 5) {
  const lines = content.split('\n');
  const points = [];
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('- **') || trimmed.startsWith('* **')) {
      const clean = trimmed.replace(/^[\-\*]\s*\*\*/, '').replace(/\*\*.*$/, '').replace(/[:\.\s]+$/, '').trim();
      if (clean.length > 15 && clean.length < 120 && !clean.includes('Giriş')) {
        points.push(clean);
        if (points.length >= maxPoints) break;
      }
    }
  }
  return points;
}

export function compileSummaries() {
  console.log('📚 [Ders Özetleri Derleyicisi] Başlatılıyor...');

  const baseDir = fs.existsSync(SRC_SUMMARIES_DIR) ? SRC_SUMMARIES_DIR : FALLBACK_SUMMARIES_DIR;
  if (!fs.existsSync(baseDir)) {
    throw new Error(`Özet dizini bulunamadı: ${baseDir}`);
  }

  const summaries = [];
  const kurulFolders = fs.readdirSync(baseDir, { withFileTypes: true })
    .filter(d => d.isDirectory() && d.name.toLowerCase().startsWith('kurul'));

  console.log(`📁 Bulunan Kurul Klasörleri: ${kurulFolders.map(k => k.name).join(', ')}`);

  for (const kFolder of kurulFolders) {
    const kPath = path.join(baseDir, kFolder.name);
    const kurulNumMatch = kFolder.name.match(/\d+/);
    const kurulNum = kurulNumMatch ? parseInt(kurulNumMatch[0], 10) : 1;
    const committeeId = `donem3-kurul${kurulNum}`;

    // Subdirectories are disciplines (e.g. Tıbbi Farmakoloji, Tıbbi Patoloji) OR direct markdown files
    const entries = fs.readdirSync(kPath, { withFileTypes: true });

    for (const entry of entries) {
      if (entry.isDirectory()) {
        const discPath = path.join(kPath, entry.name);
        const discName = entry.name;
        const mdFiles = fs.readdirSync(discPath).filter(f => f.endsWith('.md'));

function normalizeMarkdown(content) {
  if (!content) return '';
  // Convert CRLF to LF
  let text = content.replace(/\r\n/g, '\n').replace(/\r/g, '\n');
  // Clean runaway tabs that mash words together
  text = text.replace(/([^\n\t])\t+([^\n\t])/g, '$1 $2');
  text = text.replace(/\t+/g, ' ');
  return text.trim();
}

        for (const file of mdFiles) {
          const filePath = path.join(discPath, file);
          const rawContent = normalizeMarkdown(fs.readFileSync(filePath, 'utf8'));
          const title = cleanTitle(file);
          const keyPoints = extractKeyPointsFromMarkdown(rawContent, 6);

          summaries.push({
            id: `sum-k${kurulNum}-${file.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase()}`,
            kurul: kurulNum,
            committeeId,
            discipline: discName,
            title,
            fileName: file,
            keyPoints,
            charCount: rawContent.length,
            content: rawContent,
            readingTimeMinutes: Math.max(3, Math.round(rawContent.split(/\s+/).length / 150))
          });
        }
      } else if (entry.isFile() && entry.name.endsWith('.md')) {
        const filePath = path.join(kPath, entry.name);
        const rawContent = normalizeMarkdown(fs.readFileSync(filePath, 'utf8'));
        const title = cleanTitle(entry.name);
        const keyPoints = extractKeyPointsFromMarkdown(rawContent, 6);

        summaries.push({
          id: `sum-k${kurulNum}-${entry.name.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase()}`,
          kurul: kurulNum,
          committeeId,
          discipline: 'Dönem 3 Ders Notu',
          title,
          fileName: entry.name,
          keyPoints,
          charCount: rawContent.length,
          content: rawContent,
          readingTimeMinutes: Math.max(3, Math.round(rawContent.split(/\s+/).length / 150))
        });
      }
    }
  }

  console.log(`✅ Toplam ${summaries.length} adet amfi ders özeti başarıyla derlendi.`);

  // 1. Lightweight meta (only ~85KB) for instant initial render
  const metaList = summaries.map(s => ({
    id: s.id,
    kurul: s.kurul,
    committeeId: s.committeeId,
    discipline: s.discipline,
    title: s.title,
    fileName: s.fileName,
    keyPoints: s.keyPoints,
    charCount: s.charCount,
    readingTimeMinutes: s.readingTimeMinutes
  }));

  const metaPath = path.join(ROOT_DIR, 'src', 'data', 'summaries_meta.json');
  fs.writeFileSync(metaPath, JSON.stringify(metaList, null, 2), 'utf8');

  // 2. Full catalog (data/ and src/data/)
  const jsonStr = JSON.stringify(summaries, null, 2);
  fs.writeFileSync(OUT_DATA_PATH, jsonStr, 'utf8');
  if (fs.existsSync(path.dirname(OUT_SRC_PATH))) {
    fs.writeFileSync(OUT_SRC_PATH, jsonStr, 'utf8');
  }

  // 3. Local committee chunks (kurul 1-6) for fast code-split client loading
  const summariesDir = path.join(ROOT_DIR, 'src', 'data', 'summaries');
  if (!fs.existsSync(summariesDir)) {
    fs.mkdirSync(summariesDir, { recursive: true });
  }
  for (let k = 1; k <= 6; k++) {
    const kList = summaries.filter(s => s.kurul === k || s.committeeId === `donem3-kurul${k}`);
    const kPath = path.join(summariesDir, `kurul${k}.json`);
    fs.writeFileSync(kPath, JSON.stringify(kList), 'utf8');
  }
  console.log(`💾 Yerel kurul özet parçaları oluşturuldu (src/data/summaries/kurul1..6.json)`);

  console.log(`💾 Hafif meta listesi kaydedildi: ${metaPath} (${(fs.statSync(metaPath).size / 1024).toFixed(1)} KB)`);
  console.log(`💾 Tam katalog kaydedildi: ${OUT_SRC_PATH}`);
  return summaries;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  compileSummaries();
}
