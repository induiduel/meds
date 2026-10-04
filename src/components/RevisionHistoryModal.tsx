import React from 'react';
import { 
  X, 
  History, 
  Calendar, 
  User, 
  Hash, 
  CheckCircle2, 
  ArrowRight,
  BookOpen
} from 'lucide-react';
import { QuestionItem } from '../types';

interface RevisionHistoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  question: QuestionItem | null;
}

export const RevisionHistoryModal: React.FC<RevisionHistoryModalProps> = ({
  isOpen,
  onClose,
  question,
}) => {
  if (!isOpen || !question) return null;

  const revisions = question.revisions || [];

  return (
    <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-fadeIn">
      <div 
        className="ms-modal-panel bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-900 via-teal-800 to-slate-900 p-5 text-white flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-white/10 text-teal-300">
              <History className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-base leading-tight">
                Versiyon & Değişiklik Geçmişi
              </h3>
              <p className="text-xs text-teal-200/80">
                {question.isUnassignedNumber ? 'Numarasız Soru' : `Soru #${question.questionNumber}`} • {question.discipline}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1 rounded-lg text-white/70 hover:text-white hover:bg-white/10 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Info */}
        <div className="bg-slate-50 border-b border-slate-200 px-5 py-2.5 text-xs text-slate-600 flex items-center justify-between shrink-0">
          <span>Toplam <strong>{revisions.length}</strong> versiyon kaydedildi. Eski versiyonlar arşivde tutulur.</span>
          <span className="text-[11px] text-teal-700 font-semibold">Ters Kronolojik Sıralama</span>
        </div>

        {/* Revision List */}
        <div className="p-6 overflow-y-auto space-y-5 flex-1">
          {revisions.length === 0 ? (
            <div className="text-center py-10 text-slate-400">
              <History className="w-8 h-8 mx-auto mb-2 opacity-40" />
              <p className="text-xs">Bu soru için henüz ek bir düzenleme versiyonu bulunmuyor.</p>
            </div>
          ) : (
            [...revisions].reverse().map((rev, index) => {
              const revNum = rev.version || (revisions.length - index);
              const isLatest = index === 0;

              return (
                <div
                  key={rev.id || index}
                  className={`rounded-xl border p-4.5 transition-all ${
                    isLatest
                      ? 'bg-teal-50/40 border-teal-300 shadow-2xs'
                      : 'bg-white border-slate-200'
                  }`}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2.5 border-b border-slate-100">
                    <div className="flex items-center gap-2">
                      <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${
                        isLatest
                          ? 'bg-teal-600 text-white'
                          : 'bg-slate-100 text-slate-700'
                      }`}>
                        Versiyon {revNum} {isLatest && '(Güncel)'}
                      </span>
                      <span className="text-xs font-bold text-slate-900">
                        {rev.changeSummary || 'Düzenleme'}
                      </span>
                    </div>

                    <div className="flex items-center gap-3 text-[11px] text-slate-500">
                      <span className="flex items-center gap-1">
                        <User className="w-3 h-3 text-slate-400" />
                        <strong>{rev.editorName || 'Anonim'}</strong>
                        {rev.editorStudentNumber && (
                          <span className="font-mono text-slate-400">({rev.editorStudentNumber})</span>
                        )}
                      </span>
                      <span>•</span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3 text-slate-400" />
                        {new Date(rev.editedAt).toLocaleString('tr-TR', {
                          day: '2-digit',
                          month: '2-digit',
                          year: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </span>
                    </div>
                  </div>

                  {/* Soru Kökü */}
                  {rev.stem && (
                    <div className="mt-3">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                        Bu Versiyondaki Soru Metni:
                      </span>
                      <p className="text-xs text-slate-800 bg-slate-50 p-2.5 rounded-lg border border-slate-100 leading-relaxed font-sans whitespace-pre-wrap">
                        {rev.stem}
                      </p>
                    </div>
                  )}

                  {/* Options if recorded */}
                  {rev.options && rev.options.length > 0 && (
                    <div className="mt-2.5 space-y-1">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                        Şıklar:
                      </span>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5 mt-1">
                        {rev.options.map((o) => (
                          <div
                            key={o.key}
                            className={`text-[11px] px-2.5 py-1 rounded-md flex items-center gap-1.5 border ${
                              rev.claimedAnswer === o.key
                                ? 'bg-emerald-50 border-emerald-300 text-emerald-950 font-semibold'
                                : 'bg-slate-50 border-slate-200 text-slate-700'
                            }`}
                          >
                            <span className="font-bold">{o.key})</span>
                            <span className="truncate">{o.text}</span>
                            {rev.claimedAnswer === o.key && (
                              <CheckCircle2 className="w-3 h-3 text-emerald-600 shrink-0 ml-auto" />
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 flex justify-end shrink-0">
          <button
            type="button"
            onClick={onClose}
            className="px-5 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-bold transition-colors cursor-pointer"
          >
            Kapat
          </button>
        </div>
      </div>
    </div>
  );
};
