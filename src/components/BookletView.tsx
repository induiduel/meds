import React, { useState } from 'react';
import { Printer, Download, Eye, EyeOff, FileText, CheckCircle2 } from 'lucide-react';
import { QuestionItem, Committee } from '../types';

interface BookletViewProps {
  committee?: Committee;
  questions: QuestionItem[];
  onOpenPdfModal?: () => void;
}

export const BookletView: React.FC<BookletViewProps> = ({
  committee,
  questions,
  onOpenPdfModal,
}) => {
  const [showAnswerKey, setShowAnswerKey] = useState(false);
  const [showExplanations, setShowExplanations] = useState(false);

  // Filter questions that have either reconstruction or fragments
  const activeQuestions = questions.filter(
    (q) => q.reconstruction || q.fragments.length > 0
  );

  const handlePrint = () => {
    if (onOpenPdfModal) {
      onOpenPdfModal();
    } else {
      window.print();
    }
  };

  return (
    <div className="space-y-6">
      {/* Print Controls Bar (hidden in print media) */}
      <div className="print:hidden bg-white rounded-xl border border-slate-200 p-4 shadow-xs flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <FileText className="w-4 h-4 text-teal-600" />
            A4 Kurul Sınavı Soru Kitapçığı Görünümü
          </h3>
          <p className="text-xs text-slate-500">
            Öğrencilerin katkıları ve AI ile tamamlanan soruların iki sütunlu klasik sınav kitapçığı formatı.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <button
            onClick={() => setShowAnswerKey(!showAnswerKey)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 border transition-colors cursor-pointer ${
              showAnswerKey
                ? 'bg-teal-50 border-teal-300 text-teal-800'
                : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
            }`}
          >
            {showAnswerKey ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
            <span>Cevap Anahtarı: {showAnswerKey ? 'Açık' : 'Gizli'}</span>
          </button>

          <button
            onClick={() => setShowExplanations(!showExplanations)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 border transition-colors cursor-pointer ${
              showExplanations
                ? 'bg-emerald-50 border-emerald-300 text-emerald-800'
                : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
            }`}
          >
            <span>Tıbbi Açıklamalar: {showExplanations ? 'Açık' : 'Gizli'}</span>
          </button>

          <button
            onClick={handlePrint}
            className="bg-teal-700 hover:bg-teal-800 text-white px-4 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 shadow-xs cursor-pointer active:scale-95"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Yazdır / PDF Olarak Kaydet</span>
          </button>
        </div>
      </div>

      {/* A4 Printable Paper Container */}
      <div className="bg-white rounded-xl border border-slate-200 p-8 shadow-md max-w-4xl mx-auto print:shadow-none print:border-none print:p-0">
        {/* Booklet Header */}
        <div className="border-b-2 border-slate-900 pb-4 mb-6 text-center space-y-1">
          <span className="text-xs uppercase tracking-widest font-bold text-slate-500">
            T.C. TIP FAKÜLTESİ • DÖNEM {committee?.year || 3}
          </span>
          <h1 className="text-lg font-black text-slate-900 uppercase">
            {committee?.name || 'DÖNEM 3 KURUL SINAVI'}
          </h1>
          <div className="flex items-center justify-center gap-4 text-xs text-slate-600 font-serif">
            <span>Akademik Yıl: {committee?.term || '2025-2026'}</span>
            <span>•</span>
            <span>Kolektif Öğrenci Rekonstrüksiyon Kitapçığı</span>
            <span>•</span>
            <span>Toplam Soru: {activeQuestions.length}</span>
          </div>
        </div>

        {/* Questions Grid: Two Columns on Large Screens & Print */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6 text-xs text-slate-900 print:grid-cols-2">
          {activeQuestions.map((q) => {
            const hasRec = !!q.reconstruction;
            const stem = hasRec
              ? q.reconstruction!.stem
              : q.fragments.map((f) => f.text).join(' ');
            const options = hasRec
              ? q.reconstruction!.options
              : q.options;

            return (
              <div
                key={q.id}
                className="space-y-2 border-b border-slate-100 pb-4 break-inside-avoid"
              >
                <div className="flex items-center justify-between text-[11px] font-bold text-slate-700">
                  <span className="bg-slate-100 px-1.5 py-0.5 rounded text-slate-800">
                    SORU {q.questionNumber}
                  </span>
                  <span className="text-slate-500 font-sans">{q.discipline}</span>
                </div>

                {/* Soru Metni */}
                <p className="leading-relaxed font-serif text-[12px] font-medium text-slate-900">
                  {stem}
                </p>

                {/* Şıklar */}
                <div className="space-y-1 pl-1">
                  {options.map((opt) => {
                    const isCorrect = hasRec && q.reconstruction!.correctAnswer === opt.key;
                    return (
                      <div
                        key={opt.key}
                        className={`flex items-start gap-1.5 ${
                          showAnswerKey && isCorrect
                            ? 'font-bold text-emerald-800 bg-emerald-50/60 p-0.5 rounded'
                            : 'text-slate-800'
                        }`}
                      >
                        <span className="font-bold shrink-0">{opt.key})</span>
                        <span className="leading-tight">{opt.text}</span>
                      </div>
                    );
                  })}
                </div>

                {/* Explanation (if enabled) */}
                {showExplanations && hasRec && (
                  <div className="mt-2 p-2 bg-slate-50 border border-slate-200 rounded text-[11px] text-slate-700">
                    <span className="font-bold text-slate-900 block mb-0.5">
                      Doğru Cevap: {q.reconstruction!.correctAnswer}
                    </span>
                    <p className="text-slate-600 leading-snug">{q.reconstruction!.explanation}</p>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Answer Key Table at bottom */}
        {showAnswerKey && (
          <div className="mt-10 pt-6 border-t-2 border-slate-900 break-inside-avoid">
            <h4 className="text-sm font-bold uppercase mb-3 text-center">
              Cevap Anahtarı (Rekonstrükte Sorular)
            </h4>
            <div className="grid grid-cols-10 gap-1.5 text-center text-xs">
              {activeQuestions
                .filter((q) => q.reconstruction)
                .map((q) => (
                  <div key={q.id} className="p-1.5 border border-slate-200 rounded bg-slate-50">
                    <span className="block text-[10px] text-slate-500">#{q.questionNumber}</span>
                    <span className="font-bold text-slate-900">
                      {q.reconstruction!.correctAnswer}
                    </span>
                  </div>
                ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
