// Ders özetlerini resmi ders programıyla ve kaynak PDF'leriyle eşleştirir.
// Girdi:  src/data/summaries_meta.json
//         $MEDS_DATABASE_DIR/taxonomy/donem3_ders_programi.json (dersler, konular, PDF adayları)
//         $MEDS_DOWNLOADS_DIR/_manifest.json + indirilen PDF'ler (tarih için pdfinfo)
// Çıktı:  src/data/summaries_enrichment.json  { [özetId]: { lessonTitle, discipline, instructor, sourceDate, sourceYear, pdfName, programDate } }
//         src/data/curriculum_disciplines.json { [kurul]: ["Tıbbi Genetik", ...] }
// Çalıştır: node scripts/pipeline/10-enrich-summaries.mjs
import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';
import { fileURLToPath } from 'url';
import { DOWNLOADS_DIR, DATABASE_DIR } from './config.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const META = path.join(ROOT, 'src/data/summaries_meta.json');
const OUT = path.join(ROOT, 'src/data/summaries_enrichment.json');
const OUT_DISC = path.join(ROOT, 'src/data/curriculum_disciplines.json');
const TAXONOMY = path.join(DATABASE_DIR, 'taxonomy/donem3_ders_programi.json');
const MANIFEST = path.join(DOWNLOADS_DIR, '_manifest.json');

const fold = (s) =>
  String(s || '')
    .replace(/İ/g, 'i').replace(/I/g, 'ı').toLocaleLowerCase('tr')
    .replace(/ı/g, 'i').replace(/ğ/g, 'g').replace(/ü/g, 'u').replace(/ş/g, 's').replace(/ö/g, 'o').replace(/ç/g, 'c')
    .replace(/±/g, 'i');
const STOP = new Set(['ve', 'ile', 'de', 'da', 'bir', 'pdf', 'md', 'donusturuldu', 'son', 'kopya', 'ders', 'notu', 'slayt']);
const tokens = (s) =>
  new Set(
    fold(s)
      .replace(/\.(pdf|md|pptx?|docx?)$/i, '')
      .replace(/[^a-z0-9]+/g, ' ')
      .split(' ')
      .filter((w) => w.length >= 3 && !STOP.has(w) && !/^\d+$/.test(w))
      .map((w) => w.slice(0, 6))
  );
const similarity = (a, b) => {
  if (!a.size || !b.size) return 0;
  let inter = 0;
  for (const t of a) if (b.has(t)) inter++;
  return inter / Math.min(a.size, b.size) * (inter / Math.max(a.size, b.size)) ** 0.25;
};
const titleCase = (s) =>
  String(s || '')
    .toLocaleLowerCase('tr')
    .replace(/(^|[\s(.-])(\p{L})/gu, (m, p, c) => p + c.toLocaleUpperCase('tr'))
    .replace(/\b(Dr|Prof|Doç|Öğr|Üyesi|Uz)\b\.?/g, (m) => m)
    .trim();

function pdfDate(file) {
  try {
    const out = execFileSync('pdfinfo', [file], { encoding: 'utf8', timeout: 8000, stdio: ['ignore', 'pipe', 'ignore'] });
    const line = out.split('\n').find((l) => /^CreationDate:/.test(l)) || out.split('\n').find((l) => /^ModDate:/.test(l));
    if (!line) return null;
    const d = new Date(line.replace(/^\w+:\s*/, '').trim());
    return isNaN(d.getTime()) ? null : d;
  } catch {
    return null;
  }
}

if (!fs.existsSync(META)) throw new Error('summaries_meta.json yok');
const summaries = JSON.parse(fs.readFileSync(META, 'utf8'));
const taxonomy = fs.existsSync(TAXONOMY) ? JSON.parse(fs.readFileSync(TAXONOMY, 'utf8')) : { kurullar: [] };
const manifest = fs.existsSync(MANIFEST) ? JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) : { items: [] };

// Kurul başına resmi ders listesi
const disciplines = {};
for (const k of taxonomy.kurullar || []) disciplines[k.kurul] = (k.dersler || []).map((d) => d.ders);

// Kurul başına konu listesi (ders programı)
const konular = [];
for (const k of taxonomy.kurullar || []) for (const c of k.konular || []) if (c.tur === 'ders' && c.konu) konular.push({ ...c, kurul: k.kurul, tok: tokens(c.konu) });

// İndirilmiş PDF'ler (tüm kökler)
const pdfs = (manifest.items || [])
  .filter((i) => !i.is_folder && /\.pdf$/i.test(i.name || ''))
  .map((i) => ({
    name: i.name,
    root: i.root,
    path: i.path,
    file: path.join(DOWNLOADS_DIR, i.root, i.path),
    kurul: Number((i.path.match(/kurul\s*(\d)/i) || [])[1]) || null,
    tok: tokens(i.name),
  }))
  .filter((p) => fs.existsSync(p.file));

const result = {};
let matchedLesson = 0;
let matchedPdf = 0;
for (const s of summaries) {
  const st = tokens(`${s.title} ${s.fileName}`);
  // 1) Ders programındaki konu
  let bestK = null;
  let bestKs = 0;
  for (const c of konular) {
    if (c.kurul !== s.kurul) continue;
    const sc = similarity(st, c.tok);
    if (sc > bestKs) { bestKs = sc; bestK = c; }
  }
  // 2) Kaynak PDF (önce aynı kurul klasörü)
  let bestP = null;
  let bestPs = 0;
  for (const p of pdfs) {
    if (p.kurul && p.kurul !== s.kurul) continue;
    const sc = similarity(st, p.tok) + (p.kurul === s.kurul ? 0.05 : 0);
    if (sc > bestPs) { bestPs = sc; bestP = p; }
  }
  const entry = {};
  if (bestK && bestKs >= 0.5) {
    matchedLesson++;
    entry.lessonTitle = bestK.konu.trim();
    entry.discipline = bestK.ders;
    if (bestK.ogretim_uyesi) entry.instructor = titleCase(bestK.ogretim_uyesi);
    if (bestK.tarih) entry.programDate = bestK.tarih;
  }
  if (bestP && bestPs >= 0.5) {
    matchedPdf++;
    entry.pdfName = bestP.name;
    const d = pdfDate(bestP.file);
    if (d) {
      entry.sourceDate = d.toISOString().slice(0, 10);
      entry.sourceYear = d.getFullYear();
    }
  }
  if (Object.keys(entry).length) result[s.id] = entry;
}

if (Object.keys(result).length === 0) {
  console.error('[enrich] Hiç eşleşme bulunamadı; mevcut dosya korunuyor.');
  process.exit(1);
}
fs.writeFileSync(OUT, JSON.stringify(result, null, 1));
if (Object.keys(disciplines).length) fs.writeFileSync(OUT_DISC, JSON.stringify(disciplines, null, 1));
console.log(`[enrich] ${summaries.length} özet · ders eşleşmesi ${matchedLesson} · PDF eşleşmesi ${matchedPdf} · ${pdfs.length} PDF tarandı`);
