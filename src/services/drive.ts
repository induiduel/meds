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
  /** Two-column compact booklet (default) or a single wide column */
  columns?: 'one' | 'two';
  /** Solution mode: mark the correct option in green (default true). Off = plain "Cevap: X" line only. */
  highlightCorrect?: boolean;
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

/** Embeds the Turkish-capable font into a jsPDF doc; returns the font name and a text mapper. */
export async function setupPdfFonts(doc: any): Promise<{ font: string; T: (s: string) => string }> {
  const fonts = await loadFonts();
  if (!fonts) return { font: 'helvetica', T: (s: string) => asciiFold(s) };
  doc.addFileToVFS('LiberationSans-Regular.ttf', fonts.regular);
  doc.addFont('LiberationSans-Regular.ttf', 'Liberation', 'normal');
  doc.addFileToVFS('LiberationSans-Bold.ttf', fonts.bold);
  doc.addFont('LiberationSans-Bold.ttf', 'Liberation', 'bold');
  doc.addFileToVFS('LiberationSans-Italic.ttf', fonts.italic);
  doc.addFont('LiberationSans-Italic.ttf', 'Liberation', 'italic');
  return { font: 'Liberation', T: (s: string) => s };
}

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
  const twoCol = (options.columns || 'two') === 'two';
  const highlight = options.highlightCorrect ?? true;

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

  // ---- Design tokens (same palette as the site) ----
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

  // ---- Page geometry: compact booklet ----
  const pageW = doc.internal.pageSize.getWidth();
  const pageH = doc.internal.pageSize.getHeight();
  const M = 14; // side margin
  const GUTTER = 7; // between columns
  const TOP = 19; // first baseline on continuation pages
  const BOTTOM = pageH - 15; // last baseline before the footer
  const W = pageW - M * 2;
  const COL_W = twoCol ? (W - GUTTER) / 2 : W;
  const BADGE = 5.2; // number gutter
  const TEXT_W = COL_W - BADGE;

  // type scale (pt) and line heights (mm)
  const SZ = { stem: 8.2, opt: 7.8, meta: 5.9, exp: 6.8, title: 12.5, sub: 7.4 };
  const LH = { stem: 3.6, opt: 3.4, exp: 3.05 };

  let col = 0;
  let y = M;
  let colTop = TOP; // where columns start on the current page
  const columnTops: number[] = []; // per page, for drawing the column rule

  const title = (options.title || committee?.name || 'Dönem 3 Kurul Sınavı').trim();
  const shortTitle = title.length > 90 ? title.slice(0, 87) + '…' : title;

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
  const colX = () => M + col * (COL_W + GUTTER);

  const runningHeader = () => {
    style('normal', 6.5, INK3);
    doc.text(T(shortTitle), M, 10.5, { maxWidth: W - 30 });
    style('bold', 6.5, ACCENT);
    doc.text(T('MEDSORU'), pageW - M, 10.5, { align: 'right' });
    stroke(LINE);
    doc.line(M, 12.5, pageW - M, 12.5);
  };
  const newPage = () => {
    doc.addPage();
    runningHeader();
    col = 0;
    colTop = TOP;
    y = TOP;
    columnTops.push(TOP);
  };
  const nextColumn = () => {
    if (twoCol && col === 0) {
      col = 1;
      y = colTop;
    } else newPage();
  };
  const ensure = (h: number) => {
    if (y + h > BOTTOM) nextColumn();
  };

  /** Line-by-line writer: text (and its decoration) flows across columns and pages. */
  const write = (text: string, dx: number, width: number, lineH: number, decorate?: (x: number, top: number, h: number) => void) => {
    const lines: string[] = doc.splitTextToSize(T(text), width);
    for (const line of lines) {
      ensure(lineH);
      const x = colX() + dx;
      decorate?.(x, y - lineH * 0.76, lineH);
      doc.text(line, x, y);
      y += lineH;
    }
  };

  // ---------- Title block (full width) ----------
  style('bold', 6.8, ACCENT);
  doc.text(T('MEDSORU · SORU KİTAPÇIĞI'), M, M);
  y = M + 5.6;
  style('bold', SZ.title, INK);
  for (const line of doc.splitTextToSize(T(title), W) as string[]) {
    doc.text(line, M, y);
    y += 5.4;
  }
  const modeLabel = mode === 'student' ? 'Öğrenci sınavı' : mode === 'solution' ? 'Çözümlü' : 'Cevap anahtarı';
  style('normal', SZ.sub, INK2);
  const metaLine = [
    `${questions.length} soru`,
    mode !== 'answers_only' ? `~${Math.round(questions.length * 1.1)} dk` : '',
    modeLabel,
    options.subtitle || '',
    new Date().toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' }),
  ]
    .filter(Boolean)
    .join('  ·  ');
  doc.text(T(metaLine), M, y - 0.6, { maxWidth: W });
  y += 2.6;
  if (mode === 'student') {
    fill(CANVAS);
    doc.roundedRect(M, y, W, 6.4, 1.2, 1.2, 'F');
    style('normal', 7, INK2);
    doc.text(T('Her sorunun tek doğru cevabı vardır. Cevaplarını optik forma işaretle. Cevap anahtarı son sayfadadır.'), M + 3, y + 4.1, { maxWidth: W - 6 });
    y += 6.4 + 3;
  }
  stroke(INK, 0.35);
  doc.line(M, y, pageW - M, y);
  y += 6.2;
  colTop = y;
  columnTops.push(colTop);

  // ---------- Questions ----------
  // Compact layout: number in a narrow gutter, a tiny meta line, the stem, options
  // (two per row when every option fits on half a line) and a short answer note.
  const green = highlight && mode === 'solution';
  if (mode !== 'answers_only') {
    questions.forEach((q, idx) => {
      const rec = q.reconstruction;
      const stem = (rec?.stem || (q as any).rawStem || q.fragments?.map((f) => f.text).join(' ') || (q as any).stem || '').trim();
      const opts = ((rec?.options as any[]) || q.options || []).filter((o: any) => o && o.key && String(o.text || '').trim());
      const answer = rec?.correctAnswer || q.claimedAnswer || '';

      // number + meta + first two stem lines stay together
      ensure(2.8 + 2 * LH.stem);

      const meta = [q.discipline, q.examYear].filter(Boolean).join(' · ');
      if (meta) {
        style('normal', SZ.meta, INK3);
        doc.text(T(meta), colX() + BADGE, y - 0.9, { maxWidth: TEXT_W });
        y += 2.7;
      }
      style('bold', SZ.stem, ACCENT);
      doc.text(`${idx + 1}.`, colX(), y);

      style('normal', SZ.stem, INK);
      write(stem || '(Soru kökü henüz derlenmedi)', BADGE, TEXT_W, LH.stem);
      y += 0.7;

      // Options: two per row when all are short
      const half = (TEXT_W - 2) / 2;
      style('normal', SZ.opt, INK);
      const optText = (o: any) => T(`${o.key})  ${String(o.text).trim()}`);
      const short = opts.length > 0 && opts.every((o: any) => doc.getTextWidth(optText(o)) <= half - 1.5);
      const isMarked = (o: any) => mode === 'solution' && green && !!answer && o.key === answer;
      const optStyle = (o: any) => style(isMarked(o) ? 'bold' : 'normal', SZ.opt, isMarked(o) ? OK : INK);
      const markRow = (x: number, w: number) => {
        fill(OK_SOFT);
        doc.roundedRect(x - 1, y - LH.opt * 0.78, w, LH.opt + 0.2, 0.6, 0.6, 'F');
      };

      if (short) {
        for (let i = 0; i < opts.length; i += 2) {
          ensure(LH.opt);
          const pair = opts.slice(i, i + 2);
          pair.forEach((o: any, j: number) => {
            const x = colX() + BADGE + 1 + j * (half + 2);
            if (isMarked(o)) markRow(x, half);
            optStyle(o);
            doc.text(optText(o), x, y);
          });
          y += LH.opt;
        }
      } else {
        // hanging indent: wrapped lines align with the option text, not the letter
        const KEY_W = 4.4;
        opts.forEach((o: any) => {
          optStyle(o);
          const lines: string[] = doc.splitTextToSize(T(String(o.text).trim()), TEXT_W - 2 - KEY_W);
          lines.forEach((ln, li) => {
            ensure(LH.opt);
            const x = colX() + BADGE + 1;
            if (isMarked(o)) {
              fill(OK_SOFT);
              doc.rect(x - 1, y - LH.opt * 0.78, TEXT_W - 0.2, LH.opt, 'F');
            }
            optStyle(o);
            if (li === 0) doc.text(`${o.key})`, x, y);
            doc.text(ln, x + KEY_W, y);
            y += LH.opt;
          });
        });
      }

      if (mode === 'solution') {
        const exp = cleanExplanation(rec?.explanation || '');
        y += 1;
        const barColor = green ? OK : LINE;
        const bar = (x: number, top: number, h: number) => {
          fill(barColor);
          doc.rect(x - 2, top, 0.45, h + 0.15, 'F');
        };
        style('bold', SZ.exp, green ? OK : INK);
        write(`Cevap: ${answer || 'belirtilmemiş'}`, BADGE + 2, TEXT_W - 2.2, LH.exp, bar);
        if (exp) {
          style('normal', SZ.exp, INK2);
          exp
            .split('\n')
            .map((p) => p.trim())
            .filter(Boolean)
            .forEach((para) => write(para, BADGE + 2, TEXT_W - 2.2, LH.exp, bar));
        }
      }

      // space + hairline between questions (skipped at a column break)
      y += 1.8;
      if (y + 4 <= BOTTOM) {
        stroke(LINE, 0.15);
        doc.line(colX() + BADGE, y, colX() + COL_W, y);
      }
      y += 3.6;
    });
  }

  // ---------- Answer key (full width) ----------
  let keyStartPage = Infinity;
  if (includeKey && questions.length > 0) {
    if (mode !== 'answers_only') newPage();
    keyStartPage = doc.getNumberOfPages();
    const keyCols = 15;
    const gap = 1.2;
    const cellW = (W - gap * (keyCols - 1)) / keyCols;
    const cellH = 8.2;
    style('bold', 6.8, ACCENT);
    doc.text(T('CEVAP ANAHTARI'), M, y);
    style('normal', 6.8, INK3);
    doc.text(T(`${questions.length} soru`), pageW - M, y, { align: 'right' });
    y += 4;
    questions.forEach((q, idx) => {
      const c = idx % keyCols;
      if (c === 0 && y + cellH > BOTTOM) newPage();
      const x = M + c * (cellW + gap);
      const ans = q.reconstruction?.correctAnswer || q.claimedAnswer || '–';
      fill(CANVAS);
      doc.roundedRect(x, y, cellW, cellH, 1, 1, 'F');
      style('normal', 5.8, INK3);
      doc.text(String(idx + 1), x + cellW / 2, y + 2.9, { align: 'center' });
      style('bold', 8.6, ans === '–' ? INK3 : ACCENT);
      doc.text(T(ans), x + cellW / 2, y + 6.6, { align: 'center' });
      if (c === keyCols - 1 || idx === questions.length - 1) y += cellH + gap;
    });
  }

  // ---------- Column rules + footer ----------
  const total = doc.getNumberOfPages();
  for (let p = 1; p <= total; p++) {
    doc.setPage(p);
    const isKeyPage = mode === 'answers_only' || p >= keyStartPage;
    if (twoCol && mode !== 'answers_only' && !isKeyPage) {
      stroke(LINE);
      const mid = M + COL_W + GUTTER / 2;
      doc.line(mid, (columnTops[p - 1] ?? TOP) - 3, mid, BOTTOM);
    }
    stroke(LINE);
    doc.line(M, pageH - 11, pageW - M, pageH - 11);
    style('normal', 6.5, INK3);
    doc.text(T('MedSoru · Dönem 3 kurul soru arşivi'), M, pageH - 7.5);
    doc.text(T(`${p} / ${total}`), pageW - M, pageH - 7.5, { align: 'right' });
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

