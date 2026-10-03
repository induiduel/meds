// Link past-exam files to the existing question pool and course material (retrieval only, no AI).
//
//   npx tsx scripts/link-exam-questions.mts <file-or-folder> [--out report.json]
//
// For every question found in a PDF/DOCX it reports:
//   - whether the question already exists in data/pastQuestions.json (near-duplicate) or which
//     existing questions are most similar,
//   - which lecture slides / summaries / transcripts it relates to.
// Scanned PDFs (no text layer) are listed as needing OCR.
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { searchRagChunks, MATERIAL_DOC_TYPES, type RagChunkResult } from '../src/services/ragService.ts';
import { foldTurkish } from '../src/services/localRagEngine.ts';

const require = createRequire(import.meta.url);
const pdfParseModule = require('pdf-parse');
const PDFParse = pdfParseModule.PDFParse || pdfParseModule.default || pdfParseModule;
const mammoth = require('mammoth');

export interface ParsedQuestion {
  number: number;
  text: string; // discipline/topic/stem as found in the file
  options: string[];
}

// pdf-parse drops the "fl"/"fi" ligature glyphs: "in!amatuar" -> "inflamatuar", "Nöro"bromatozis" -> "Nörofibromatozis".
const repairLigatures = (t: string) =>
  t.replace(/(?<=[a-zçğıöşü])!(?=[a-zçğıöşü])/gi, 'fl').replace(/(?<=[a-zçğıöşü])"(?=[a-zçğıöşü])/gi, 'fi');

async function extractText(file: string): Promise<{ text: string; pages: number }> {
  const buf = fs.readFileSync(file);
  if (file.toLowerCase().endsWith('.docx')) {
    return { text: (await mammoth.extractRawText({ buffer: buf })).value, pages: 1 };
  }
  const res = await new PDFParse({ data: buf }).getText();
  return { text: repairLigatures(res.text), pages: res.total ?? 1 };
}

const JUNK_LINE = [
  /^\d{4}\/\d{1,2}\/\d{1,2}\s/, // "2021/4/12 sinav.karabuk.edu.tr"
  /^\d{1,2}\.\d{1,2}\.\d{4}\s/, // "12.04.2021 sinav..."
  /https?:\/\/|\.edu\.tr/,
  /^-- \d+ of \d+ --$/,
  /^Soru - Konu Özeti$/i,
  /^(Sıra|No|Sıra No|No\s+Ders.*|Ders \/ Ünite.*|Cevabınız|Duru.*)$/i,
];
const ICON = /[\uf046\uf00d]/g; // ✓/✗ glyphs the exam system puts next to the student's answer
const QUESTION_START = /^\s*\d{1,3}\s*(\t.*)?$/; // "12" or "12 \tTıbbi Patoloji"
const isJunk = (l: string) => JUNK_LINE.some((re) => re.test(l));

/** Turn the lines before an options table into "discipline topic stem". */
function cleanHead(head: string): string {
  let lines = head.split('\n');
  // Drop everything up to the last table header (page headers, student name/score on page 1).
  const lastHeader = lines.map((l) => /Ders \/ Ünite/.test(l)).lastIndexOf(true);
  if (lastHeader >= 0) lines = lines.slice(lastHeader + 1);
  // A "N<TAB>Ders" line marks the question start; anything before it is a leftover answer.
  const lastStart = lines.map((l) => /^\s*\d{1,3}\s*\t/.test(l)).lastIndexOf(true);
  if (lastStart > 0) lines = lines.slice(lastStart);
  return lines
    .map((l) => l.replace(ICON, '').trim())
    .filter((l) => l && !isJunk(l) && !/^\d{1,3}$/.test(l))
    .join(' ')
    .replace(/^\d{1,3}\s+/, '')
    .replace(/\s+/g, ' ')
    .trim();
}

/** University exam-system export: "N  Ders/Konu  Soru ... Sıra No Cevap  1 ... 5 ...  <öğrenci cevabı>" */
function parseExamSystemFormat(text: string): ParsedQuestion[] {
  const segments = text.split(/Sıra\s*\n?\s*No\s*\t?\s*Cevap/);
  if (segments.length < 3) return [];
  const questions: ParsedQuestion[] = [];

  // segments[0] = header + Q1 head; segments[k] = options of Qk + student answer + Q(k+1) head
  let head = segments[0];
  for (let k = 1; k < segments.length; k++) {
    const lines = segments[k].split('\n');
    const options: string[] = [];
    let i = 0;
    for (; i < lines.length; i++) {
      const raw = lines[i];
      const line = raw.trim();
      const m = raw.match(/^\s*([1-5])\s+(.*)$/);
      if (m && Number(m[1]) === options.length + 1) {
        options.push(m[2].trim());
        continue;
      }
      if (options.length === 0) {
        if (!line) continue;
        break;
      }
      // Wrapped option text continues until a blank line, an answer icon, the next question or page junk.
      if (!line || /[\uf046\uf00d]/.test(line) || QUESTION_START.test(raw) || isJunk(line)) break;
      // After the last option, a line repeating an option is the student's answer ("Cevabınız").
      if (options.length === 5 && options.some((o) => o.startsWith(line) || line.startsWith(o))) {
        i++;
        while (i < lines.length && lines[i].trim() && !QUESTION_START.test(lines[i]) && !isJunk(lines[i].trim())) i++;
        break;
      }
      options[options.length - 1] += ' ' + line;
    }

    // Skip the student's answer: lone icon lines, then through the line ending with an icon.
    let j = i;
    while (j < lines.length && /^[\s\uf046\uf00d]*$/.test(lines[j])) j++;
    for (let t = j; t < Math.min(lines.length, j + 6); t++) {
      if (/[\uf046\uf00d]/.test(lines[t])) {
        j = t + 1;
        break;
      }
    }

    const qText = cleanHead(head);
    if (qText.length > 15) {
      questions.push({ number: questions.length + 1, text: qText, options: options.map((o) => o.replace(ICON, '').trim()) });
    }
    head = lines.slice(j).join('\n');
  }
  return questions;
}

/** "1- Soru?\nCevap" or "1. Soru\na) .. b) .." lists */
function parseNumberedFormat(text: string): ParsedQuestion[] {
  const lines = text.split('\n').map((l) => l.trim()).filter((l) => l && !isJunk(l));
  const questions: ParsedQuestion[] = [];
  let cur: ParsedQuestion | null = null;
  for (const line of lines) {
    const m = line.match(/^(\d{1,3})\s*[-.)]\s*(.*)$/);
    if (m) {
      if (cur) questions.push(cur);
      cur = { number: Number(m[1]), text: m[2], options: [] };
      continue;
    }
    if (!cur) continue;
    const opt = line.match(/^([a-eA-E])\s*[.)]\s*(.+)$/);
    if (opt) cur.options.push(opt[2]);
    else cur.text += ' ' + line;
  }
  if (cur) questions.push(cur);
  return questions;
}

/** Inline "Soru? a. .. b. .. c. .. d. .. e. .. Cevap: x" (e.g. Word tables). */
function parseInlineFormat(text: string): ParsedQuestion[] {
  const flat = text.replace(/\s+/g, ' ');
  const re = /([^?]{15,}?\?)\s*a[.)]\s*(.+?)\s+b[.)]\s*(.+?)\s+c[.)]\s*(.+?)\s+d[.)]\s*(.+?)\s+e[.)]\s*(.+?)(?=\s+Cevap\b|\s+\d{1,3}[.)-]\s|$)/g;
  const questions: ParsedQuestion[] = [];
  for (const m of flat.matchAll(re)) {
    const stem = m[1].replace(/^.*?(Eski Soru \d+|Yeni Soru \d+|Soru No)\s*/g, '').trim();
    questions.push({ number: questions.length + 1, text: stem, options: m.slice(2, 7).map((o) => o.trim()) });
  }
  return questions;
}

// OCR noise like "- - - O - - T kre!tze" is not a question.
const looksLikeText = (q: ParsedQuestion) => {
  const letters = (q.text.match(/[a-zA-ZçğıöşüÇĞİÖŞÜ]/g) || []).length;
  const words = q.text.split(/\s+/).filter((w) => /^[a-zA-ZçğıöşüÇĞİÖŞÜ]{3,}/.test(w)).length;
  return words >= 3 && letters / Math.max(1, q.text.length) > 0.6;
};

// The same exam is often exported several times into one PDF; keep the first copy.
function dedupe(questions: ParsedQuestion[]): ParsedQuestion[] {
  const seen = new Set<string>();
  return questions.filter((q) => {
    const key = foldTurkish(q.text).replace(/[^a-z0-9]/g, '').slice(-120);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function parseQuestions(text: string): ParsedQuestion[] {
  for (const parser of [parseExamSystemFormat, parseNumberedFormat, parseInlineFormat]) {
    const found = parser(text).filter(looksLikeText);
    if (found.length > 0) return dedupe(found);
  }
  return [];
}

// Question boilerplate says nothing about the topic; ignore it when comparing questions.
const BOILERPLATE = new Set(
  ['asagidakilerden', 'asagidaki', 'hangisi', 'hangisidir', 'hangileri', 'yanlistir', 'dogrudur', 'degildir', 'ile', 'ilgili',
   'olan', 'icin', 'ifadelerden', 'verilen', 'bulunur', 'gorulur', 'yoktur', 'isaretleyiniz', 'yalniz', 'olarak', 'hastada', 'hasta']
);
const tokens = (s: string) =>
  new Set(foldTurkish(s).split(/[^a-z0-9]+/).filter((w) => w.length >= 3 && !BOILERPLATE.has(w)));
/** Share of the pool question's words that appear in the new question (stems are short, so
 *  the new text, which also carries discipline/topic, should contain nearly all of them). */
function overlap(newText: string, poolStem: string): { ratio: number; words: number } {
  const A = tokens(newText), B = tokens(poolStem);
  if (B.size === 0) return { ratio: 0, words: 0 };
  let inter = 0;
  for (const t of B) if (A.has(t)) inter++;
  return { ratio: inter / B.size, words: B.size };
}
const pastStem = (r: RagChunkResult) => (r.content.match(/Soru Kökü:\n([\s\S]*?)\n\nSeçenekler:/)?.[1] || r.content).trim();
const pastOptions = (r: RagChunkResult) =>
  (r.content.match(/Seçenekler:\n([\s\S]*?)\n\nDoğru/)?.[1] || '')
    .split('\n')
    .map((l) => l.replace(/^[A-Ea-e]\)\s*/, '').trim())
    .filter(Boolean);

/** Share of options (by normalized text) the two questions have in common. */
function optionOverlap(a: string[], b: string[]): number {
  const norm = (o: string) => foldTurkish(o).replace(/[^a-z0-9]/g, '').slice(0, 40);
  const A = new Set(a.map(norm).filter((o) => o.length >= 2));
  const B = new Set(b.map(norm).filter((o) => o.length >= 2));
  if (A.size < 3 || B.size < 3) return 0;
  let inter = 0;
  for (const o of A) if (B.has(o)) inter++;
  return inter / Math.min(A.size, B.size);
}

export async function linkQuestion(q: ParsedQuestion) {
  const query = [q.text, ...q.options].join(' ').slice(0, 1500);
  const [past, material] = await Promise.all([
    searchRagChunks(query, undefined, { documentType: 'past_question', limit: 3 }),
    searchRagChunks(query, undefined, { documentTypes: MATERIAL_DOC_TYPES, limit: 3 }),
  ]);
  const similar = past.map((r) => {
    const stemSim = overlap(q.text, pastStem(r));
    return {
      id: r.documentId,
      title: r.title,
      examYear: r.metadata?.examYear,
      stem: pastStem(r).slice(0, 300),
      overlap: Math.round(stemSim.ratio * 100),
      stemWords: stemSim.words,
      optionOverlap: Math.round(optionOverlap(q.options, pastOptions(r)) * 100),
    };
  });
  // Pool stems are often OCR-damaged, reworded or generic, so a binary answer would be wrong too often.
  //   same:   stem and options agree (or a long stem matches almost word for word)
  //   likely: stem or options largely agree -> a human should check
  //   new:    nothing close in the pool
  type Sim = (typeof similar)[number];
  const isSame = (s: Sim) =>
    s.stemWords >= 2 && ((s.overlap >= 75 && s.optionOverlap >= 60) || (s.overlap >= 90 && s.stemWords >= 5));
  const isLikely = (s: Sim) => s.stemWords >= 2 && (s.overlap >= 60 || s.optionOverlap >= 60);
  const poolMatch: 'same' | 'likely' | 'new' = similar.some(isSame) ? 'same' : similar.some(isLikely) ? 'likely' : 'new';
  return {
    ...q,
    poolMatch,
    alreadyInPool: poolMatch === 'same',
    similarPastQuestions: similar,
    material: material.map((r) => ({
        type: r.documentType,
        title: r.title,
        discipline: r.discipline,
        pageNumber: r.pageNumber,
        snippet: r.content.replace(/\s+/g, ' ').slice(0, 200),
      })),
  };
}

async function main() {
  const target = process.argv[2];
  const outIdx = process.argv.indexOf('--out');
  if (!target) {
    console.error('Kullanım: npx tsx scripts/link-exam-questions.mts <dosya-veya-klasör> [--out rapor.json]');
    process.exit(1);
  }
  const files = fs.statSync(target).isDirectory()
    ? fs.readdirSync(target).filter((f) => /\.(pdf|docx)(\.download)?$/i.test(f)).map((f) => path.join(target, f))
    : [target];

  const report: any[] = [];
  for (const file of files) {
    const name = path.basename(file);
    let extracted;
    try {
      extracted = await extractText(file);
    } catch (e: any) {
      console.log(`✗ ${name}: okunamadı (${e.message})`);
      report.push({ file: name, status: 'unreadable', error: e.message, questions: [] });
      continue;
    }
    const isDocx = file.toLowerCase().endsWith('.docx');
    const charsPerPage = extracted.text.replace(/-- \d+ of \d+ --|\s/g, '').length / Math.max(1, extracted.pages);
    const questions = parseQuestions(extracted.text);
    if (questions.length === 0) {
      const status = !isDocx && charsPerPage < 200 ? 'needs_ocr' : 'no_questions_found';
      console.log(`✗ ${name}: ${status === 'needs_ocr' ? 'taranmış görüntü, OCR gerekli' : 'soru bulunamadı'}`);
      report.push({ file: name, status, questions: [] });
      continue;
    }
    const linked: Awaited<ReturnType<typeof linkQuestion>>[] = [];
    for (const q of questions) linked.push(await linkQuestion(q));
    const count = (m: string) => linked.filter((l) => l.poolMatch === m).length;
    const withMaterial = linked.filter((l) => l.material.length > 0).length;
    const scanned = !isDocx && charsPerPage < 200 ? ' (kısmen taranmış olabilir)' : '';
    console.log(
      `✓ ${name}: ${linked.length} soru · havuzda aynısı ${count('same')} · muhtemelen aynı ${count('likely')} · yeni ${count('new')} · ${withMaterial} ders materyaliyle eşleşti${scanned}`
    );
    report.push({ file: name, status: 'ok', questions: linked });
  }

  if (outIdx > 0 && process.argv[outIdx + 1]) {
    fs.writeFileSync(process.argv[outIdx + 1], JSON.stringify(report, null, 2));
    console.log(`Rapor: ${process.argv[outIdx + 1]}`);
  }
  process.exit(0);
}

if (import.meta.url === `file://${process.argv[1]}`) main();
