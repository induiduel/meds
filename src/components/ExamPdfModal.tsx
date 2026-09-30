import React, { useState } from 'react';
import { 
  X, 
  Printer, 
  Download, 
  Eye, 
  EyeOff, 
  FileText, 
  CheckCircle2, 
  Columns, 
  Square, 
  Sparkles,
  BookOpen,
  HelpCircle
} from 'lucide-react';
import { Committee, QuestionItem } from '../types';

interface ExamPdfModalProps {
  isOpen: boolean;
  onClose: () => void;
  committee: Committee | undefined;
  questions: QuestionItem[];
}

export const ExamPdfModal: React.FC<ExamPdfModalProps> = ({
  isOpen,
  onClose,
  committee,
  questions,
}) => {
  const [mode, setMode] = useState<'student' | 'solution' | 'answers_only'>('student');
  const [columns, setColumns] = useState<'two' | 'one'>('two');
  const [filterReadyOnly, setFilterReadyOnly] = useState(false);

  if (!isOpen) return null;

  // Filter and sort questions
  const sortedQuestions = [...questions].sort(
    (a, b) => a.questionNumber - b.questionNumber
  );

  const displayQuestions = sortedQuestions.filter((q) => {
    if (filterReadyOnly) {
      return !!q.reconstruction || q.status === 'completed';
    }
    return !!q.reconstruction || q.fragments.length > 0 || q.options.length > 0;
  });

  const targetCount = committee?.targetCount || (committee?.id.includes('final') || committee?.id.includes('butunleme') ? 150 : 100);
  const examDuration = Math.round(targetCount * 1.1); // ~1.1 min per question

  const handlePrint = () => {
    window.print();
  };

  const handleDownloadHtml = () => {
    const printableElement = document.getElementById('exam-printable-content');
    if (!printableElement) return;

    const htmlContent = `<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>${committee?.name || 'Tip Fakültesi Kurul Sınavı'} - Soru Kitapçığı</title>
  <style>
    @page { size: A4; margin: 12mm; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; color: #0f172a; margin: 0; padding: 20px; line-height: 1.4; font-size: 11pt; background: #fff; }
    .header { border-bottom: 2px solid #0f172a; padding-bottom: 12px; margin-bottom: 20px; text-align: center; }
    .header h1 { margin: 4px 0; font-size: 16pt; text-transform: uppercase; letter-spacing: 0.5px; }
    .header .sub { font-size: 10pt; color: #475569; margin: 2px 0; }
    .instructions { background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 6px; padding: 8px 14px; font-size: 9pt; margin-bottom: 20px; }
    .columns-2 { columns: 2; column-gap: 24px; column-rule: 1px solid #e2e8f0; }
    .question { break-inside: avoid; page-break-inside: avoid; margin-bottom: 18px; font-size: 10pt; }
    .q-header { font-weight: bold; color: #0f766e; margin-bottom: 4px; display: flex; justify-content: space-between; font-size: 9.5pt; }
    .q-stem { margin-bottom: 8px; font-family: Georgia, serif; line-height: 1.45; }
    .q-option { margin-bottom: 4px; padding-left: 6px; display: flex; gap: 6px; }
    .q-option.correct { font-weight: bold; color: #065f46; background: #ecfdf5; border-radius: 4px; padding: 2px 6px; }
    .explanation { margin-top: 6px; padding: 6px 10px; background: #f0fdf4; border-left: 3px solid #059669; font-size: 9pt; color: #065f46; }
    .answer-key { break-before: page; page-break-before: always; margin-top: 30px; }
    table { width: 100%; border-collapse: collapse; font-size: 9pt; margin-top: 10px; }
    th, td { border: 1px solid #cbd5e1; padding: 6px 8px; text-align: center; }
    th { background: #f1f5f9; font-weight: bold; }
    @media print {
      body { padding: 0; }
      .no-print { display: none !important; }
    }
  </style>
</head>
<body>
  ${printableElement.innerHTML}
</body>
</html>`;

    const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${(committee?.name || 'Kurul_Kitapcigi').replace(/[^a-zA-Z0-9_\u00C0-\u017F-]/g, '_')}_A4_Kitapcik.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/70 backdrop-blur-xs flex items-center justify-center p-2 sm:p-4 overflow-y-auto">
      <div className="bg-slate-100 rounded-2xl max-w-5xl w-full shadow-2xl border border-slate-300 overflow-hidden my-4 flex flex-col max-h-[95vh]">
        {/* Top Control Bar (Hidden when printing) */}
        <div className="bg-slate-900 text-white p-4 shrink-0 flex flex-wrap items-center justify-between gap-3 no-print">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-500/20 text-teal-400 border border-teal-500/30 flex items-center justify-center">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-sm font-bold flex items-center gap-2">
                A4 Tıp Kurul Sınav Kitapçığı & PDF Çıktısı
                <span className="bg-teal-500/30 text-teal-300 text-[10px] font-mono px-2 py-0.5 rounded-full border border-teal-500/40">
                  {displayQuestions.length} Soru
                </span>
              </h2>
              <p className="text-xs text-slate-400">
                {committee?.name || 'Dönem 3 Kurul Sınavı'} • İki sütunlu klasik fakülte mizanpajı
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handlePrint}
              className="bg-teal-600 hover:bg-teal-500 text-white px-3.5 py-2 rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-sm cursor-pointer transition-all active:scale-95"
              title="Yazıcıdan veya tarayıcının 'PDF olarak kaydet' seçeneğiyle yüksek çözünürlüklü vektör PDF oluşturur"
            >
              <Printer className="w-4 h-4" />
              <span>Yazdır / PDF Olarak Kaydet</span>
            </button>

            <button
              onClick={handleDownloadHtml}
              className="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3 py-2 rounded-lg text-xs font-semibold flex items-center gap-1.5 cursor-pointer transition-colors"
              title="İnternetsiz de açılabilen tek dosya HTML kitapçık indirir"
            >
              <Download className="w-4 h-4 text-slate-300" />
              <span className="hidden sm:inline">HTML İndir</span>
            </button>

            <button
              onClick={onClose}
              className="p-2 text-slate-400 hover:text-white hover:bg-slate-800 rounded-lg cursor-pointer transition-colors ml-1"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Options Bar (Hidden in print) */}
        <div className="bg-white border-b border-slate-200 p-3 px-5 flex flex-wrap items-center justify-between gap-3 shrink-0 no-print text-xs">
          {/* Mode Selector */}
          <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200">
            <button
              onClick={() => setMode('student')}
              className={`px-3 py-1.5 rounded-md font-semibold transition-all cursor-pointer ${
                mode === 'student'
                  ? 'bg-white text-teal-800 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Öğrenci Sınavı (Cevaplar Gizli)
            </button>
            <button
              onClick={() => setMode('solution')}
              className={`px-3 py-1.5 rounded-md font-semibold transition-all cursor-pointer ${
                mode === 'solution'
                  ? 'bg-white text-teal-800 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Çözümlü & Açıklamalı Kitapçık
            </button>
            <button
              onClick={() => setMode('answers_only')}
              className={`px-3 py-1.5 rounded-md font-semibold transition-all cursor-pointer ${
                mode === 'answers_only'
                  ? 'bg-white text-teal-800 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              Sadece Cevap Anahtarı
            </button>
          </div>

          {/* Layout & Filter toggles */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200">
              <button
                onClick={() => setColumns('two')}
                className={`p-1.5 rounded transition-all cursor-pointer ${
                  columns === 'two' ? 'bg-white text-teal-700 shadow-xs font-bold' : 'text-slate-500'
                }`}
                title="İki Sütunlu Klasik Sınav Kitapçığı"
              >
                <Columns className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={() => setColumns('one')}
                className={`p-1.5 rounded transition-all cursor-pointer ${
                  columns === 'one' ? 'bg-white text-teal-700 shadow-xs font-bold' : 'text-slate-500'
                }`}
                title="Tek Sütunlu Geniş Görünüm"
              >
                <Square className="w-3.5 h-3.5" />
              </button>
            </div>

            <label className="flex items-center gap-1.5 cursor-pointer text-slate-700 select-none">
              <input
                type="checkbox"
                checked={filterReadyOnly}
                onChange={(e) => setFilterReadyOnly(e.target.checked)}
                className="rounded border-slate-300 text-teal-600 focus:ring-teal-500"
              />
              <span>Yalnızca Hazır Sorular ({sortedQuestions.filter(q => q.reconstruction).length})</span>
            </label>
          </div>
        </div>

        {/* Printable A4 Content Area */}
        <div className="overflow-y-auto p-4 sm:p-8 flex justify-center bg-slate-200/70">
          <div
            id="exam-printable-content"
            className="print-container bg-white shadow-lg border border-slate-300 p-8 sm:p-12 w-full max-w-[210mm] min-h-[297mm] text-slate-900 font-sans print:shadow-none print:border-none print:p-0 print:m-0"
          >
            {/* Official Exam Header */}
            <div className="border-b-2 border-slate-900 pb-4 mb-5 text-center space-y-1">
              <div className="flex items-center justify-between text-[11px] font-bold text-slate-500 uppercase tracking-widest border-b border-slate-200 pb-1.5 mb-2">
                <span>T.C. TIP FAKÜLTESİ DEKANLIĞI</span>
                <span>DÖNEM III • {committee?.term || '2026-2027'}</span>
                <span className="bg-slate-900 text-white px-2 py-0.5 rounded text-[10px]">A KİTAPÇIĞI</span>
              </div>

              <h1 className="text-base sm:text-lg font-black text-slate-900 uppercase tracking-tight">
                {committee?.name || 'TIP 300 - DÖNEM III KURUL SINAVI'}
              </h1>

              <div className="flex flex-wrap items-center justify-center gap-3 text-xs text-slate-700 font-serif pt-1">
                <span><strong>Soru Sayısı:</strong> {targetCount} Soru</span>
                <span>•</span>
                <span><strong>Sınav Süresi:</strong> {examDuration} Dakika</span>
                {committee?.examDate && (
                  <>
                    <span>•</span>
                    <span><strong>Sınav Tarihi:</strong> {committee.examDate}</span>
                  </>
                )}
                <span>•</span>
                <span><strong>Format:</strong> {mode === 'student' ? 'Öğrenci Sınav Denemesi' : mode === 'solution' ? 'Çözümlü Çalışma Kitapçığı' : 'Cevap Anahtarı Matrisi'}</span>
              </div>
            </div>

            {/* Exam Instructions Banner */}
            {mode !== 'answers_only' && (
              <div className="instructions bg-slate-50 border border-slate-200 rounded-md p-2.5 mb-6 text-[11px] text-slate-700 space-y-0.5">
                <p className="font-bold text-slate-900">SINAV YÖNERGESİ VE KURALLAR:</p>
                <p>1. Bu soru kitapçığında toplam {displayQuestions.length} soru yer almaktadır. Her sorunun yalnızca tek bir doğru cevabı vardır.</p>
                <p>2. Cevaplarınızı optik cevap kâğıdındaki ilgili soru numarasına taşıyınız. Yanlış cevaplar doğru cevapları götürmez.</p>
                <p className="text-[10px] text-slate-500 italic">MedSoru Tıp Kurul Kolektif Hafıza & Yapay Zeka Rekonstrüksiyon Arşivi tarafından derlenmiştir.</p>
              </div>
            )}

            {/* Questions Layout */}
            {mode !== 'answers_only' && (
              <div
                className={`exam-columns-${columns === 'two' ? '2' : '1'} ${
                  columns === 'two' ? 'columns-1 md:columns-2 gap-8' : 'space-y-6'
                } text-xs leading-relaxed`}
              >
                {displayQuestions.map((q) => {
                  const hasRec = !!q.reconstruction;
                  const stem = hasRec
                    ? q.reconstruction!.stem
                    : q.fragments.map((f) => f.text).join(' ') || 'Soru kökü derleniyor...';
                  
                  const options = hasRec
                    ? q.reconstruction!.options
                    : q.options;

                  return (
                    <div
                      key={q.id}
                      className="exam-question-item mb-5 pb-3 border-b border-slate-200 break-inside-avoid page-break-inside-avoid"
                    >
                      {/* Question meta bar */}
                      <div className="flex items-center justify-between text-[11px] font-bold text-slate-800 mb-1.5">
                        <span className="bg-slate-900 text-white font-mono px-2 py-0.5 rounded text-[10px] tracking-wide">
                          SORU {q.questionNumber}
                        </span>
                        <span className="text-teal-800 font-semibold text-[10px] uppercase truncate max-w-[200px]">
                          {q.discipline} {q.topic ? `• ${q.topic}` : ''}
                        </span>
                      </div>

                      {/* Question Case Stem */}
                      <p className="font-serif text-[11.5px] font-normal text-slate-900 leading-normal mb-2 whitespace-pre-line text-justify">
                        {stem}
                      </p>

                      {/* Options */}
                      <div className="space-y-1 pl-1 text-[11px]">
                        {options.map((opt) => {
                          const isCorrect = hasRec && q.reconstruction!.correctAnswer === opt.key;
                          const showAsCorrect = mode === 'solution' && isCorrect;

                          return (
                            <div
                              key={opt.key}
                              className={`flex items-start gap-2 py-0.5 px-1 rounded transition-colors ${
                                showAsCorrect
                                  ? 'bg-emerald-50 text-emerald-900 font-bold border border-emerald-300'
                                  : 'text-slate-800'
                              }`}
                            >
                              <span className="font-bold shrink-0 font-mono">
                                {opt.key})
                              </span>
                              <span className="leading-tight">{opt.text}</span>
                              {showAsCorrect && (
                                <span className="ml-auto text-[9px] text-emerald-700 uppercase font-mono font-bold shrink-0">
                                  [DOĞRU CEVAP]
                                </span>
                              )}
                            </div>
                          );
                        })}
                      </div>

                      {/* Detailed Medical Explanation (Solution Mode) */}
                      {mode === 'solution' && hasRec && q.reconstruction?.explanation && (
                        <div className="mt-2.5 p-2 bg-emerald-50/70 border-l-2 border-emerald-600 rounded text-[10.5px] text-emerald-950 space-y-0.5">
                          <div className="font-bold flex items-center gap-1 text-emerald-900 text-[11px]">
                            <CheckCircle2 className="w-3 h-3 text-emerald-600 shrink-0" />
                            <span>Gerekçe & Patofizyolojik Açıklama (Doğru Cevap: {q.reconstruction.correctAnswer}):</span>
                          </div>
                          <p className="leading-snug text-slate-700 italic">
                            {q.reconstruction.explanation}
                          </p>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}

            {/* Answer Key Summary Table */}
            {(mode === 'answers_only' || mode === 'solution' || mode === 'student') && (
              <div className="exam-answer-table mt-8 pt-6 border-t-2 border-slate-900 page-break-before">
                <div className="text-center mb-4">
                  <h3 className="text-sm font-bold uppercase tracking-wider text-slate-900">
                    CEVAP ANAHTARI ÖZETİ (A KİTAPÇIĞI)
                  </h3>
                  <p className="text-[11px] text-slate-500 font-serif">
                    {committee?.name} • Toplam {sortedQuestions.length} Soru
                  </p>
                </div>

                <div className="grid grid-cols-5 sm:grid-cols-10 gap-1.5 text-center text-xs">
                  {sortedQuestions.slice(0, targetCount).map((q) => {
                    const ans = q.reconstruction?.correctAnswer || q.claimedAnswer || '-';
                    return (
                      <div
                        key={q.questionNumber}
                        className={`p-1.5 rounded border ${
                          ans !== '-'
                            ? 'bg-slate-50 border-slate-300 text-slate-900'
                            : 'bg-slate-100/50 border-slate-200 text-slate-400'
                        }`}
                      >
                        <span className="block text-[9px] text-slate-500 font-mono">
                          #{q.questionNumber}
                        </span>
                        <span className="block font-black text-xs text-teal-800">
                          {mode === 'student' ? '___' : ans}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Official Footer */}
            <div className="mt-8 pt-4 border-t border-slate-200 flex items-center justify-between text-[10px] text-slate-400 font-mono">
              <span>MedSoru - Tıp Fakültesi Kurul Soru Havuzu</span>
              <span>Sayfa Sonu • Başarılar Dileriz</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
