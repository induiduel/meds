import React, { useState } from 'react';
import { Flag } from 'lucide-react';
import { ReportQuestionModal } from '../ReportQuestionModal';
import { ApiService } from '../../services/api';
import { StudyQuestion } from '../../services/studyStore';

/** Çalış'ta soruyu şikâyet et / hata bildir: çıkmış sorular ve soru havuzu kendi bildirim ucuna gider. */
export const StudyReportButton: React.FC<{ q: StudyQuestion; compact?: boolean; className?: string }> = ({ q, compact, className = '' }) => {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        title="Soruda hata ya da sorun bildir"
        aria-label="Soruyu bildir"
        className={`h-9 px-2.5 rounded-lg text-[13px] font-semibold inline-flex items-center gap-1.5 text-ink-2 hover:bg-bad-soft hover:text-bad-text cursor-pointer ${className}`}
      >
        <Flag className="w-4 h-4" />
        {!compact && <span className="hidden sm:inline">Bildir</span>}
      </button>
      {open && (
        <ReportQuestionModal
          question={{ ...q, questionNumber: q.number || undefined, examYear: q.year }}
          onClose={() => setOpen(false)}
          onSubmit={async (reason, details) => {
            const note = [details, `Kaynak: Çalış · ${q.source === 'arşiv' ? 'çıkmış soru' : 'soru havuzu'}`].filter(Boolean).join('\n');
            if (q.source === 'arşiv') await ApiService.reportPastQuestion(q.id, reason, note);
            else await ApiService.reportPoolQuestion(q.id, reason, note);
          }}
        />
      )}
    </>
  );
};
