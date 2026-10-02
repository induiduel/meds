import { QuestionItem, Committee } from '../types';

export const FOLDER_NAME = 'MedSoru - Tıp Kurul Arşivi';

export interface DriveUploadResult {
  fileId: string;
  fileName: string;
  webViewLink?: string;
  folderId: string;
}

export interface ThresholdStatus {
  isThresholdMet: boolean;
  totalQuestions: number;
  highConfidenceCount: number;
  targetCount: number;
  requiredHighConfidence: number;
  percentageMet: number;
  summary: string;
}

/**
 * Checks the user's threshold:
 * "100 soru toplanıp soruların %80'i (80 soru) %90 doğruluğa ulaştığında otomatik olarak bir pdf oluşturup drive klasörüne kaydet"
 */
export function evaluateAutoBackupThreshold(
  questions: QuestionItem[],
  targetCount: number = 100
): ThresholdStatus {
  // Active questions with either reconstruction or fragments
  const activeQuestions = questions.filter(
    (q) => (q.fragments && q.fragments.length > 0) || q.reconstruction
  );

  const totalQuestions = activeQuestions.length;
  const highConfidenceQuestions = activeQuestions.filter(
    (q) => q.reconstruction && q.reconstruction.confidenceScore >= 90
  );

  const highConfidenceCount = highConfidenceQuestions.length;
  // 80% of 100 is 80 questions with >= 90% confidence
  const requiredTotal = Math.min(targetCount, 100);
  const requiredHighConfidence = Math.round(requiredTotal * 0.8); // 80 questions

  const isThresholdMet =
    totalQuestions >= requiredTotal && highConfidenceCount >= requiredHighConfidence;

  const percentageMet = Math.min(
    100,
    Math.round((highConfidenceCount / requiredHighConfidence) * 100)
  );

  const summary = isThresholdMet
    ? `Eşik Karşılandı: ${totalQuestions}/${requiredTotal} soru toplandı ve ${highConfidenceCount} soru %90+ doğruluğa ulaştı.`
    : `İlerleme: ${totalQuestions}/${requiredTotal} soru havuzda, ${highConfidenceCount}/${requiredHighConfidence} soru %90+ güvene ulaştı (%${percentageMet}).`;

  return {
    isThresholdMet,
    totalQuestions,
    highConfidenceCount,
    targetCount: requiredTotal,
    requiredHighConfidence,
    percentageMet,
    summary,
  };
}

export type BookletMode = 'student' | 'solution' | 'answers_only';

export interface BookletPdfOptions {
  /** student: no answers; solution: answers + explanations; answers_only: just the key */
  mode?: BookletMode;
  /** Append the answer key table (always on for answers_only) */
  includeAnswerKey?: boolean;
  title?: string;
  subtitle?: string;
}

// ---------- Unicode font (Turkish glyphs) ----------
// jsPDF's built-in Helvetica has no ş/ğ/ı/İ, so we embed Liberation Sans (SIL OFL,
// shipped in public/fonts). Fetched once, only when a PDF is generated.
type FontSet = { regular: string; bold: string; italic: string };
let fontCache: Promise<FontSet | null> | null = null;

const toBase64 = (buf: ArrayBuffer) => {
  const bytes = new Uint8Array(buf);
  let bin = '';
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(bin);
};

const loadFonts = (): Promise<FontSet | null> => {
  if (!fontCache) {
    const base = (import.meta as any).env?.BASE_URL || '/';
    const get = (f: string) =>
      fetch(`${base}fonts/${f}`).then((r) => {
        if (!r.ok) throw new Error(`${f}: ${r.status}`);
        return r.arrayBuffer();
      });
    fontCache = Promise.all([get('LiberationSans-Regular.ttf'), get('LiberationSans-Bold.ttf'), get('LiberationSans-Italic.ttf')])
      .then(([r, b, i]) => ({ regular: toBase64(r), bold: toBase64(b), italic: toBase64(i) }))
      .catch((e) => {
        console.warn('PDF fontu yüklenemedi, ASCII karşılıklar kullanılacak:', e);
        fontCache = null;
        return null;
      });
  }
  return fontCache;
};

const TR_ASCII: Record<string, string> = { ş: 's', Ş: 'S', ğ: 'g', Ğ: 'G', ı: 'i', İ: 'I', ç: 'c', Ç: 'C', ö: 'o', Ö: 'O', ü: 'u', Ü: 'U' };
const asciiFold = (s: string) => s.replace(/[şŞğĞıİçÇöÖüÜ]/g, (c) => TR_ASCII[c] || c);

/** Redactor explanations use 【Başlık】: markers; turn them into readable paragraphs. */
const cleanExplanation = (raw: string) =>
  raw
    .replace(/【([^】]+)】\s*:?\s*/g, (_m, h) => `\n${String(h).trim()}: `)
    .replace(/\n{3,}/g, '\n\n')
    .trim();

/**
 * Generates an A4 exam booklet PDF with real Turkish text, per-line page breaks,
 * sequential numbering and the layout options chosen in the PDF dialog.
 */
export async function generateBookletPdfBlob(
  committee: Committee | undefined,
  questions: QuestionItem[],
  options: BookletPdfOptions = {}
): Promise<Blob> {
  const mode: BookletMode = options.mode || 'solution';
  const includeKey = mode === 'answers_only' ? true : options.includeAnswerKey ?? true;

  const { jsPDF } = await import('jspdf');
  const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });

  const fonts = await loadFonts();
  let FONT = 'helvetica';
  let T = (s: string) => asciiFold(s);
  if (fonts) {
    doc.addFileToVFS('LiberationSans-Regular.ttf', fonts.regular);
    doc.addFont('LiberationSans-Regular.ttf', 'Liberation', 'normal');
    doc.addFileToVFS('LiberationSans-Bold.ttf', fonts.bold);
    doc.addFont('LiberationSans-Bold.ttf', 'Liberation', 'bold');
    doc.addFileToVFS('LiberationSans-Italic.ttf', fonts.italic);
    doc.addFont('LiberationSans-Italic.ttf', 'Liberation', 'italic');
    FONT = 'Liberation';
    T = (s: string) => s;
  }

  // ---- Design tokens (match the site: ink, muted ink, line, accent, green) ----
  type RGB = [number, number, number];
  const INK: RGB = [14, 26, 38];
  const INK2: RGB = [74, 88, 104];
  const INK3: RGB = [120, 132, 146];
  const LINE: RGB = [226, 231, 236];
  const ACCENT: RGB = [30, 79, 216];
  const ACCENT_SOFT: RGB = [232, 238, 253];
  const OK: RGB = [21, 122, 62];
  const OK_SOFT: RGB = [236, 248, 241];
  const CANVAS: RGB = [246, 247, 249];

  const pageW = doc.internal.pageSize.getWidth();
  const pageH = doc.internal.pageSize.getHeight();
  const M = 20; // generous side margins
  const TOP = 24; // first baseline on continuation pages
  const BOTTOM = pageH - 20; // last baseline before the footer
  const W = pageW - M * 2;
  const BODY_X = M + 10; // text column right of the number badge
  const BODY_W = W - 10;
  let y = M;

  const title = (options.title || committee?.name || 'Dönem 3 Kurul Sınavı').trim();
  const shortTitle = title.length > 80 ? title.slice(0, 77) + '…' : title;

  const style = (weight: 'normal' | 'bold' | 'italic', size: number, rgb: RGB) => {
    doc.setFont(FONT, weight);
    doc.setFontSize(size);
    doc.setTextColor(rgb[0], rgb[1], rgb[2]);
  };
  const fill = (rgb: RGB) => doc.setFillColor(rgb[0], rgb[1], rgb[2]);
  const stroke = (rgb: RGB, w = 0.2) => {
    doc.setDrawColor(rgb[0], rgb[1], rgb[2]);
    doc.setLineWidth(w);
  };

  const runningHeader = () => {
    style('normal', 7, INK3);
    doc.text(T(shortTitle), M, 13);
    stroke(LINE);
    doc.line(M, 15.5, pageW - M, 15.5);
  };
  const newPage = () => {
    doc.addPage();
    runningHeader();
    y = TOP;
  };
  const ensure = (h: number) => {
    if (y + h > BOTTOM) newPage();
  };

  /**
   * Writes wrapped text line by line (so long stems/explanations flow across pages).
   * `decorate` runs before each line so backgrounds/bars follow the text onto new pages.
   */
  const write = (text: string, x: number, width: number, lineH: number, decorate?: (top: number, h: number) => void) => {
    const lines: string[] = doc.splitTextToSize(T(text), width);
    for (const line of lines) {
      ensure(lineH);
      decorate?.(y - lineH * 0.74, lineH);
      doc.text(line, x, y);
      y += lineH;
    }
  };

  // ---------- Title block ----------
  y = M + 2;
  style('bold', 7.5, ACCENT);
  doc.text(T('MEDSORU · SORU KİTAPÇIĞI'), M, y);
  y += 7;
  style('bold', 15, INK);
  write(title, M, W, 6.4);
  y += 0.5;
  const modeLabel = mode === 'student' ? 'Öğrenci sınavı' : mode === 'solution' ? 'Çözümlü ve açıklamalı' : 'Cevap anahtarı';
  style('normal', 8.5, INK2);
  write(
    [
      `${questions.length} soru`,
      mode !== 'answers_only' ? `~${Math.round(questions.length * 1.1)} dk` : '',
      modeLabel,
      options.subtitle || '',
      new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }),
    ]
      .filter(Boolean)
      .join('   ·   '),
    M,
    W,
    4.2
  );
  y += 3;

  if (mode === 'student') {
    // short instructions card
    const lines: string[] = doc.splitTextToSize(
      T('Her sorunun tek doğru cevabı vardır. Cevaplarını optik forma işaretle. Cevap anahtarı ayrı sayfadadır.'),
      W - 8
    );
    const h = lines.length * 3.8 + 5;
    fill(CANVAS);
    doc.roundedRect(M, y, W, h, 1.5, 1.5, 'F');
    style('normal', 8, INK2);
    doc.text(lines, M + 4, y + 4.6);
    y += h + 4;
  }

  stroke(INK, 0.4);
  doc.line(M, y, pageW - M, y);
  y += 9;

  // ---------- Questions ----------
  if (mode !== 'answers_only') {
    questions.forEach((q, idx) => {
      const rec = q.reconstruction;
      const stem = (rec?.stem || (q as any).rawStem || q.fragments?.map((f) => f.text).join(' ') || (q as any).stem || '').trim();
      const opts = ((rec?.options as any[]) || q.options || []).filter((o: any) => o && o.key && String(o.text || '').trim());
      const answer = rec?.correctAnswer || q.claimedAnswer || '';
      const num = idx + 1;

      // Keep the badge with at least the first three stem lines
      ensure(8 + 3 * 4.2);

      // Number badge
      const badge = String(num);
      fill(ACCENT_SOFT);
      doc.roundedRect(M, y - 4.1, 7, 5.6, 1.2, 1.2, 'F');
      style('bold', 8, ACCENT);
      doc.text(T(badge), M + 3.5, y - 0.2, { align: 'center' });

      // Meta (discipline · year · original no.)
      const meta = [q.discipline, q.examYear, q.questionNumber ? `S.${q.questionNumber}` : ''].filter(Boolean).join('  ·  ');
      style('normal', 7, INK3);
      doc.text(T(meta.toLocaleUpperCase('tr-TR')), BODY_X, y - 0.4, { maxWidth: BODY_W });
      y += 5;

      // Stem
      style('normal', 9.2, INK);
      write(stem || '(Soru kökü henüz derlenmedi)', BODY_X, BODY_W, 4.3);
      y += 1.6;

      // Options
      opts.forEach((o: any) => {
        const isCorrect = mode === 'solution' && !!answer && o.key === answer;
        style(isCorrect ? 'bold' : 'normal', 8.7, isCorrect ? OK : INK);
        write(
          `${o.key})  ${String(o.text).trim()}`,
          BODY_X + 2,
          BODY_W - 6,
          4.1,
          isCorrect
            ? (top, h) => {
                fill(OK_SOFT);
                doc.rect(BODY_X, top - 0.5, BODY_W, h, 'F');
              }
            : undefined
        );
        y += 0.6;
      });

      // Explanation with an accent bar that follows the text across pages
      if (mode === 'solution') {
        const exp = cleanExplanation(rec?.explanation || '');
        y += 2;
        const bar = (top: number, h: number) => {
          fill(OK);
          doc.rect(BODY_X, top, 0.6, h + 0.2, 'F');
        };
        style('bold', 7.8, OK);
        write(`Doğru cevap: ${answer || 'belirtilmemiş'}`, BODY_X + 3.5, BODY_W - 4, 3.7, bar);
        if (exp) {
          style('normal', 7.8, INK2);
          exp
            .split('\n')
            .map((p) => p.trim())
            .filter(Boolean)
            .forEach((para) => write(para, BODY_X + 3.5, BODY_W - 4, 3.6, bar));
        }
      }

      // Breathing room + hairline between questions
      y += 4;
      ensure(2);
      stroke(LINE);
      doc.line(BODY_X, y, pageW - M, y);
      y += 7.5;
    });
  }

  // ---------- Answer key ----------
  if (includeKey && questions.length > 0) {
    if (mode !== 'answers_only') newPage();
    style('bold', 7.5, ACCENT);
    doc.text(T('CEVAP ANAHTARI'), M, y);
    y += 4;
    style('normal', 8.5, INK2);
    doc.text(T(`${questions.length} soru`), M, y);
    y += 7;
    const cols = 10;
    const gap = 1.6;
    const cellW = (W - gap * (cols - 1)) / cols;
    const cellH = 10;
    questions.forEach((q, idx) => {
      const col = idx % cols;
      if (col === 0) ensure(cellH + gap);
      const x = M + col * (cellW + gap);
      const ans = q.reconstruction?.correctAnswer || q.claimedAnswer || '–';
      fill(CANVAS);
      doc.roundedRect(x, y, cellW, cellH, 1.2, 1.2, 'F');
      style('normal', 6.5, INK3);
      doc.text(String(idx + 1), x + cellW / 2, y + 3.4, { align: 'center' });
      style('bold', 10, ans === '–' ? INK3 : ACCENT);
      doc.text(T(ans), x + cellW / 2, y + 8, { align: 'center' });
      if (col === cols - 1 || idx === questions.length - 1) y += cellH + gap;
    });
  }

  // ---------- Footer with page numbers ----------
  const total = doc.getNumberOfPages();
  for (let p = 1; p <= total; p++) {
    doc.setPage(p);
    stroke(LINE);
    doc.line(M, pageH - 13.5, pageW - M, pageH - 13.5);
    style('normal', 7, INK3);
    doc.text(T('MedSoru · Dönem 3 kurul soru arşivi'), M, pageH - 9.5);
    doc.text(T(`${p} / ${total}`), pageW - M, pageH - 9.5, { align: 'right' });
  }

  return doc.output('blob');
}

/**
 * Searches or creates a folder on Google Drive
 */
async function getOrCreateDriveFolder(
  accessToken: string,
  folderName: string = FOLDER_NAME
): Promise<string> {
  // Search for existing folder
  const query = encodeURIComponent(
    `name = '${folderName}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false`
  );
  const searchRes = await fetch(
    `https://www.googleapis.com/drive/v3/files?q=${query}&fields=files(id,name)`,
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (!searchRes.ok) {
    const errText = await searchRes.text();
    throw new Error(`Google Drive klasör araması başarısız: ${errText}`);
  }

  const searchData = await searchRes.json();
  if (searchData.files && searchData.files.length > 0) {
    return searchData.files[0].id;
  }

  // Create folder if not found
  const createRes = await fetch('https://www.googleapis.com/drive/v3/files', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: folderName,
      mimeType: 'application/vnd.google-apps.folder',
      description: 'MedSoru Tıp Fakültesi Kurul Çıkmış Soruları Arşivi',
    }),
  });

  if (!createRes.ok) {
    const errText = await createRes.text();
    throw new Error(`Google Drive klasörü oluşturulamadı: ${errText}`);
  }

  const createData = await createRes.json();
  return createData.id;
}

/**
 * Uploads booklet PDF directly to Google Drive in the specified folder
 */
export async function uploadBookletPdfToDrive({
  committee,
  questions,
  accessToken,
  customFileName,
}: {
  committee?: Committee;
  questions: QuestionItem[];
  accessToken: string;
  customFileName?: string;
}): Promise<DriveUploadResult> {
  if (!accessToken) {
    throw new Error('Google Drive erişim belirteci bulunamadı. Lütfen giriş yapın.');
  }

  // 1. Get or create folder
  const folderId = await getOrCreateDriveFolder(accessToken, FOLDER_NAME);

  // 2. Generate PDF
  const pdfBlob = await generateBookletPdfBlob(committee, questions);

  // 3. Format filename
  const sanitizedCommitteeName = (committee?.name || 'Donem_3_Kurul_Sorulari')
    .replace(/[^a-zA-Z0-9_\u00C0-\u017F]/g, '_')
    .slice(0, 50);
  const timestamp = new Date().toISOString().slice(0, 10);
  const fileName =
    customFileName ||
    `${sanitizedCommitteeName}_Cikmis_Sorular_${timestamp}.pdf`;

  // 4. Multipart upload
  const boundary = '-------MedSoruBoundary' + Date.now();
  const delimiter = `\r\n--${boundary}\r\n`;
  const closeDelimiter = `\r\n--${boundary}--`;

  const metadata = {
    name: fileName,
    mimeType: 'application/pdf',
    parents: [folderId],
    description: `Tıp Fakültesi Kurul Sınavı Kolektif Rekonstrüksiyon Arşivi (${questions.length} Soru)`,
  };

  const metadataPart =
    delimiter +
    'Content-Type: application/json; charset=UTF-8\r\n\r\n' +
    JSON.stringify(metadata) +
    '\r\n';

  const multipartBlob = new Blob(
    [
      metadataPart,
      delimiter,
      'Content-Type: application/pdf\r\n\r\n',
      pdfBlob,
      closeDelimiter,
    ],
    { type: `multipart/related; boundary=${boundary}` }
  );

  const uploadRes = await fetch(
    'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,webViewLink,webContentLink',
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': `multipart/related; boundary=${boundary}`,
      },
      body: multipartBlob,
    }
  );

  if (!uploadRes.ok) {
    const errText = await uploadRes.text();
    throw new Error(`Google Drive yüklemesi başarısız oldu: ${errText}`);
  }

  const uploadData = await uploadRes.json();

  return {
    fileId: uploadData.id,
    fileName: uploadData.name || fileName,
    webViewLink: uploadData.webViewLink,
    folderId,
  };
}

/**
 * Downloads the booklet PDF directly to the user's browser/device
 */
export async function downloadBookletPdfLocally(
  committee: Committee | undefined,
  questions: QuestionItem[],
  customFileName?: string,
  options?: BookletPdfOptions
) {
  const blob = await generateBookletPdfBlob(committee, questions, options);
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  const sanitizedCommitteeName = (committee?.name || 'Donem_3_Kurul_Sorulari')
    .replace(/[^a-zA-Z0-9_\u00C0-\u017F]/g, '_')
    .slice(0, 50);
  const timestamp = new Date().toISOString().slice(0, 10);
  a.download =
    customFileName ||
    `${sanitizedCommitteeName}_Cikmis_Sorular_${timestamp}.pdf`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

