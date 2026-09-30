import { jsPDF } from 'jspdf';
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

/**
 * Generates a clean, multi-page formatted medical exam PDF
 */
export function generateBookletPdfBlob(
  committee: Committee | undefined,
  questions: QuestionItem[]
): Blob {
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4',
  });

  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  const margin = 15;
  const contentWidth = pageWidth - margin * 2;
  let cursorY = margin;

  const addHeader = (pageNum: number) => {
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(10);
    doc.setTextColor(15, 118, 110); // Teal
    doc.text(
      `MEDSORU - TIP FAKÜLTESİ DÖNEM ${committee?.year || 3} KURUL ÇIKMIŞ SORULARI`,
      margin,
      10
    );

    doc.setFont('helvetica', 'normal');
    doc.setFontSize(8);
    doc.setTextColor(100, 116, 139);
    doc.text(`Sayfa ${pageNum}`, pageWidth - margin - 15, 10);

    doc.setDrawColor(226, 232, 240);
    doc.setLineWidth(0.3);
    doc.line(margin, 12, pageWidth - margin, 12);
  };

  const checkPageBreak = (neededHeight: number) => {
    if (cursorY + neededHeight > pageHeight - margin) {
      doc.addPage();
      const pageNum = doc.getNumberOfPages();
      addHeader(pageNum);
      cursorY = 20;
    }
  };

  // Title Page Header
  addHeader(1);
  cursorY = 22;

  doc.setFont('helvetica', 'bold');
  doc.setFontSize(15);
  doc.setTextColor(15, 23, 42); // Slate-900
  const titleText = (committee?.name || 'DÖNEM 3 KURUL SINAVI').toUpperCase();
  doc.text(titleText, margin, cursorY);
  cursorY += 7;

  doc.setFont('helvetica', 'normal');
  doc.setFontSize(9);
  doc.setTextColor(71, 85, 105);
  doc.text(
    `Akademik Yıl: ${committee?.term || '2025-2026'}  |  Tarih: ${new Date().toLocaleDateString('tr-TR')}  |  Kolektif Öğrenci Rekonstrüksiyon Arşivi`,
    margin,
    cursorY
  );
  cursorY += 5;

  doc.setDrawColor(15, 118, 110);
  doc.setLineWidth(0.6);
  doc.line(margin, cursorY, pageWidth - margin, cursorY);
  cursorY += 8;

  // Filter and sort questions by number
  const sortedQuestions = [...questions].sort(
    (a, b) => a.questionNumber - b.questionNumber
  );

  sortedQuestions.forEach((q) => {
    const hasRec = !!q.reconstruction;
    const stem = hasRec
      ? q.reconstruction!.stem
      : q.fragments.map((f) => f.text).join(' ');

    const options = hasRec
      ? q.reconstruction!.options
      : q.options;

    // Estimate box height
    const splitStem = doc.splitTextToSize(
      `SORU ${q.questionNumber} (${q.discipline}): ${stem || 'Soru kökü derleniyor...'}`,
      contentWidth
    );
    const estimatedHeight = 15 + splitStem.length * 4.5 + options.length * 5 + (hasRec ? 20 : 0);

    checkPageBreak(Math.min(estimatedHeight, 80));

    // Question Box background
    doc.setFillColor(248, 250, 252);
    doc.setDrawColor(226, 232, 240);
    doc.roundedRect(margin, cursorY, contentWidth, 7, 1, 1, 'FD');

    doc.setFont('helvetica', 'bold');
    doc.setFontSize(9);
    doc.setTextColor(15, 118, 110);
    doc.text(`SORU #${q.questionNumber} • ${q.discipline} - ${q.topic}`, margin + 3, cursorY + 5);

    if (hasRec) {
      doc.setFont('helvetica', 'bold');
      doc.setFontSize(8);
      doc.setTextColor(16, 149, 193);
      doc.text(`AI Güven: %${q.reconstruction?.confidenceScore}`, pageWidth - margin - 30, cursorY + 5);
    }

    cursorY += 10;

    // Question stem
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(9);
    doc.setTextColor(15, 23, 42);
    doc.text(splitStem, margin + 2, cursorY);
    cursorY += splitStem.length * 4.5 + 2;

    // Options
    options.forEach((opt) => {
      checkPageBreak(8);
      const isCorrect = hasRec && q.reconstruction!.correctAnswer === opt.key;
      const optText = `${opt.key}) ${opt.text}${isCorrect ? '  [DOĞRU CEVAP]' : ''}`;
      const splitOpt = doc.splitTextToSize(optText, contentWidth - 8);

      if (isCorrect) {
        doc.setFont('helvetica', 'bold');
        doc.setTextColor(5, 150, 105); // Emerald
      } else {
        doc.setFont('helvetica', 'normal');
        doc.setTextColor(51, 65, 85);
      }

      doc.text(splitOpt, margin + 5, cursorY);
      cursorY += splitOpt.length * 4 + 1.5;
    });

    // Medical Explanation
    if (hasRec && q.reconstruction?.explanation) {
      checkPageBreak(15);
      doc.setFont('helvetica', 'italic');
      doc.setFontSize(8);
      doc.setTextColor(4, 120, 87);
      const splitExp = doc.splitTextToSize(
        `Gerekçe & Patofizyoloji: ${q.reconstruction.explanation}`,
        contentWidth - 6
      );
      doc.text(splitExp, margin + 3, cursorY);
      cursorY += splitExp.length * 3.8 + 3;
    }

    // Divider line between questions
    cursorY += 4;
    doc.setDrawColor(241, 245, 249);
    doc.line(margin, cursorY, pageWidth - margin, cursorY);
    cursorY += 4;
  });

  // End Answer Key Table
  checkPageBreak(40);
  cursorY += 6;
  doc.setFont('helvetica', 'bold');
  doc.setFontSize(11);
  doc.setTextColor(15, 23, 42);
  doc.text('CEVAP ANAHTARI ÖZETİ', margin, cursorY);
  cursorY += 6;

  const reconstructedOnly = sortedQuestions.filter((q) => q.reconstruction);
  let keyRow = '';
  reconstructedOnly.forEach((q, idx) => {
    keyRow += `${q.questionNumber}: ${q.reconstruction!.correctAnswer}   `;
    if ((idx + 1) % 10 === 0 || idx === reconstructedOnly.length - 1) {
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(8);
      doc.setTextColor(71, 85, 105);
      doc.text(keyRow, margin, cursorY);
      cursorY += 5;
      keyRow = '';
      checkPageBreak(10);
    }
  });

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
  const pdfBlob = generateBookletPdfBlob(committee, questions);

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
export function downloadBookletPdfLocally(
  committee: Committee | undefined,
  questions: QuestionItem[],
  customFileName?: string
) {
  const blob = generateBookletPdfBlob(committee, questions);
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

