import React, { useMemo, useState } from 'react';
import { X, Save, ShieldAlert, Sparkles, Users, Eye, RotateCcw, AlertTriangle } from 'lucide-react';
import { QuestionItem, QuestionOption } from '../types';

interface AdminEditQuestionModalProps {
  isOpen: boolean;
  onClose: () => void;
  question: QuestionItem | null;
  adminEmail: string;
  onSaveQuestion: (updated: Partial<QuestionItem>) => Promise<void>;
}

type OptKey = 'A' | 'B' | 'C' | 'D' | 'E';
const OPT_KEYS: OptKey[] = ['A', 'B', 'C', 'D', 'E'];

export const AdminEditQuestionModal: React.FC<AdminEditQuestionModalProps> = (props) => {
  if (!props.isOpen || !props.question) return null;
  return <AdminEditQuestionModalContent key={props.question.id} {...props} question={props.question} />;
};

const AdminEditQuestionModalContent: React.FC<AdminEditQuestionModalProps & { question: QuestionItem }> = ({
  onClose,
  question,
  adminEmail,
  onSaveQuestion,
}) => {
  const rec = question.reconstruction;

  // ---- Uygun veri uygun girdiye: önce redaksiyon, yoksa taslak kaynakları ----
  const initialStem =
    rec?.stem ||
    question.stem ||
    question.rawStem ||
    (question.fragments || []).map((f) => f.text).join('\n\n') ||
    '';
  const initialOptions: Record<OptKey, string> = { A: '', B: '', C: '', D: '', E: '' };
  if (rec?.options && rec.options.length > 0) {
    for (const o of rec.options) initialOptions[o.key] = o.text || '';
  } else {
    for (const o of question.options || []) initialOptions[o.key] = o.text || '';
  }
  const initialAnswer: OptKey =
    rec?.correctAnswer || question.claimedAnswer || question.correctAnswer || 'A';
  const initialExplanation = rec?.explanation || question.explanation || '';

  const [questionNumber, setQuestionNumber] = useState(question.questionNumber);
  const [discipline, setDiscipline] = useState(question.discipline || '');
  const [topic, setTopic] = useState(question.topic || '');
  const [status, setStatus] = useState(question.status);
  const [claimedAnswer, setClaimedAnswer] = useState<'' | OptKey>(question.claimedAnswer || '');
  const [stem, setStem] = useState(initialStem);
  const [correctAnswer, setCorrectAnswer] = useState<OptKey>(initialAnswer);
  const [explanation, setExplanation] = useState(initialExplanation);
  const [confidenceScore, setConfidenceScore] = useState(rec?.confidenceScore ?? 90);
  const [opts, setOpts] = useState<Record<OptKey, string>>(initialOptions);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const filledOptionCount = useMemo(
    () => OPT_KEYS.filter((k) => opts[k].trim().length > 0).length,
    [opts]
  );
  const canPublish = stem.trim().length > 0 && filledOptionCount >= 2;
  const hasSourceFragments = (question.fragments || []).length > 0;

  const fillFromFragments = () => {
    const text = (question.fragments || []).map((f) => f.text).join('\n\n');
    if (text.trim()) setStem(text);
  };

  const resetToSource = () => {
    setStem(initialStem);
    setOpts({ ...initialOptions });
    setCorrectAnswer(initialAnswer);
    setExplanation(initialExplanation);
    setClaimedAnswer(question.claimedAnswer || '');
    setStatus(question.status);
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!topic.trim()) {
      setError('Konu başlığı boş bırakılamaz.');
      return;
    }
    setIsSaving(true);
    try {
      const optionTexts: Record<OptKey, string> = {
        A: opts.A.trim(),
        B: opts.B.trim(),
        C: opts.C.trim(),
        D: opts.D.trim(),
        E: opts.E.trim(),
      };
      const keptKeys = OPT_KEYS.filter((k) => optionTexts[k].length > 0);
      // Öğrenci şıkları korunur: metni yönetici değiştirdiyse üzerine yazılır, yeniler eklenir.
      const mergedOptions: QuestionOption[] = OPT_KEYS.filter((k) => optionTexts[k]).map((k) => {
        const existing = (question.options || []).find((o) => o.key === k);
        return {
          key: k,
          text: optionTexts[k],
          suggestedBy: existing?.suggestedBy || 'Yönetici',
          suggestedByUid: existing?.suggestedByUid,
          upvotes: existing?.upvotes ?? 1,
        };
      });

      const patch: Partial<QuestionItem> = {
        questionNumber: Number(questionNumber) || question.questionNumber,
        discipline: discipline.trim() || question.discipline,
        topic: topic.trim(),
        status: canPublish ? 'completed' : status,
        options: mergedOptions,
      };
      if (claimedAnswer) patch.claimedAnswer = claimedAnswer;

      if (canPublish) {
        patch.reconstruction = {
          stem: stem.trim(),
          options: keptKeys.map((k) => ({ key: k, text: optionTexts[k], isAiFilled: false })),
          correctAnswer,
          explanation: explanation.trim(),
          confidenceScore: Math.min(100, Math.max(0, Number(confidenceScore) || 0)),
          notesAndDiscrepancies: rec?.notesAndDiscrepancies || 'Yönetici tarafından güncellendi.',
          lastUpdated: new Date().toISOString(),
        };
      } else if (rec) {
        // Tam redaksiyon yoksa mevcut redaksiyonu silme, aynen koru.
        patch.reconstruction = rec;
      }

      await onSaveQuestion(patch);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Kaydedilemedi.');
    } finally {
      setIsSaving(false);
    }
  };

  const inputCls =
    'w-full bg-field border border-line-2 rounded-[10px] px-3 py-2 text-[14px] text-ink outline-0 focus:border-accent focus:bg-white placeholder:text-[#7A8693]';

  return (
    <div className="fixed inset-0 z-50 bg-[rgba(14,26,38,0.55)] flex items-stretch sm:items-center justify-center sm:p-4 overflow-y-auto">
      <div className="bg-white w-full max-w-5xl sm:rounded-[20px] shadow-[0_24px_80px_rgba(14,26,38,0.28)] overflow-hidden my-0 sm:my-6 flex flex-col max-h-dvh">
        {/* Header */}
        <div className="bg-ink text-white px-4 sm:px-5 py-3.5 flex items-center gap-3 shrink-0">
          <span className="w-9 h-9 rounded-[10px] bg-white/10 text-white flex items-center justify-center shrink-0">
            <ShieldAlert className="w-[18px] h-[18px]" />
          </span>
          <div className="flex-1 min-w-0">
            <h3 className="m-0 font-display font-bold text-[16px] sm:text-[18px] tracking-[-0.01em] truncate">
              Soru düzenle: {question.isUnassignedNumber ? 'No ?' : `#${question.questionNumber}`} · {question.discipline}
            </h3>
            <p className="m-0 text-[12px] text-white/60 truncate">
              Oturum: {adminEmail} (Yetkili) · {question.status === 'completed' ? 'Doğrulanmış soru' : 'Taslak soru'}
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Kapat"
            className="w-10 h-10 rounded-[10px] flex items-center justify-center text-white/70 hover:text-white hover:bg-white/10 cursor-pointer shrink-0"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex-1 min-h-0 overflow-y-auto">
          <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1fr)_340px]">
            {/* ---------- Sol: düzenleme formu ---------- */}
            <div className="p-4 sm:p-5 flex flex-col gap-4 min-w-0">
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                <label className="flex flex-col gap-1">
                  <span className="text-[12px] font-semibold text-ink-2">Soru No</span>
                  <input type="number" value={questionNumber} onChange={(e) => setQuestionNumber(Number(e.target.value))} className={`${inputCls} font-mono font-bold`} required />
                </label>
                <label className="flex flex-col gap-1">
                  <span className="text-[12px] font-semibold text-ink-2">Ders</span>
                  <input type="text" value={discipline} onChange={(e) => setDiscipline(e.target.value)} className={inputCls} required />
                </label>
                <label className="flex flex-col gap-1 col-span-2 sm:col-span-1">
                  <span className="text-[12px] font-semibold text-ink-2">Durum</span>
                  <select value={status} onChange={(e) => setStatus(e.target.value as QuestionItem['status'])} className={`${inputCls} cursor-pointer`}>
                    <option value="empty">Boş</option>
                    <option value="gathering">Taslak (parça toplanıyor)</option>
                    <option value="completed">Doğrulanmış</option>
                  </select>
                </label>
                <label className="flex flex-col gap-1 col-span-2">
                  <span className="text-[12px] font-semibold text-ink-2">Konu başlığı</span>
                  <input type="text" value={topic} onChange={(e) => setTopic(e.target.value)} className={inputCls} required />
                </label>
                <div className="flex flex-col gap-1 col-span-2">
                  <span className="text-[12px] font-semibold text-ink-2">Öğrencilerin bildirdiği cevap</span>
                  <div className="flex gap-1.5">
                    {OPT_KEYS.map((k) => (
                      <button key={k} type="button" onClick={() => setClaimedAnswer(claimedAnswer === k ? '' : k)} aria-pressed={claimedAnswer === k}
                        className={`flex-1 h-10 rounded-[10px] font-mono text-[14px] font-semibold cursor-pointer border ${claimedAnswer === k ? 'bg-accent text-white border-accent' : 'bg-field text-ink-2 border-line-2 hover:border-accent'}`}>
                        {k}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div className="flex flex-col gap-2 pt-3 border-t border-line-soft">
                <div className="flex items-center justify-between gap-2 flex-wrap">
                  <span className="font-bold text-[14px] text-ink flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4 text-accent" /> Soru kökü & metni
                  </span>
                  <div className="flex items-center gap-2">
                    {hasSourceFragments && (
                      <button type="button" onClick={fillFromFragments} className="h-8 px-2.5 rounded-lg border border-line text-[12.5px] font-semibold text-ink-2 hover:text-ink cursor-pointer">
                        Parçalardan doldur
                      </button>
                    )}
                    <label className="flex items-center gap-1.5 text-[12.5px] font-semibold text-ink-2">
                      Güven (%):
                      <input type="number" min={0} max={100} value={confidenceScore} onChange={(e) => setConfidenceScore(Number(e.target.value))}
                        className="w-16 bg-field border border-line-2 rounded-lg px-1.5 py-1 text-center font-bold text-accent outline-0 focus:border-accent" />
                    </label>
                  </div>
                </div>
                <textarea rows={5} value={stem} onChange={(e) => setStem(e.target.value)} placeholder="Tam soru metnini buraya yazın…"
                  className={`${inputCls} resize-y leading-relaxed`} />
                <span className="self-end text-[12px] text-ink-3 font-mono">{stem.trim().length} karakter</span>
              </div>

              <div className="flex flex-col gap-2 pt-3 border-t border-line-soft">
                <span className="font-bold text-[14px] text-ink">Şıklar (A – E) · doğru cevabı işaretleyin</span>
                {OPT_KEYS.map((k) => (
                  <div key={k} className="flex items-center gap-2">
                    <span className={`w-7 h-9 rounded-lg font-mono font-bold text-[14px] flex items-center justify-center shrink-0 ${correctAnswer === k ? 'bg-ok text-white' : 'bg-canvas text-ink-2'}`}>{k}</span>
                    <input type="text" value={opts[k]} onChange={(e) => setOpts((p) => ({ ...p, [k]: e.target.value }))} placeholder={`${k} şıkkı metni`} className={inputCls} />
                    <button type="button" onClick={() => setCorrectAnswer(k)}
                      className={`h-9 px-2.5 rounded-[10px] text-[12.5px] font-bold cursor-pointer shrink-0 ${correctAnswer === k ? 'bg-ok text-white' : 'bg-canvas text-ink-2 hover:text-ink'}`}>
                      {correctAnswer === k ? '✓ Doğru' : 'Doğru Yap'}
                    </button>
                  </div>
                ))}
                <span className="text-[12px] text-ink-3">{filledOptionCount} şık dolu · yayın için en az 2 şık ve soru kökü gerekir.</span>
              </div>

              <label className="flex flex-col gap-1.5 pt-3 border-t border-line-soft">
                <span className="font-bold text-[14px] text-ink">Tıbbi gerekçe & açıklama</span>
                <textarea rows={3} value={explanation} onChange={(e) => setExplanation(e.target.value)} placeholder="Robbins / Katzung standartlarında açıklama…"
                  className={`${inputCls} resize-y leading-relaxed`} />
              </label>

              {!canPublish && (
                <p className="m-0 rounded-[12px] bg-warn-soft px-3 py-2 text-[13px] text-ink-2 flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-warn" />
                  <span>Redaksiyon tamamlanmadığı için kayıt <strong>taslak</strong> olarak saklanacak; mevcut doğrulanmış içerik silinmeyecek.</span>
                </p>
              )}
              {error && (
                <p role="alert" className="m-0 rounded-[12px] bg-bad-soft px-3 py-2 text-[13px] text-bad-text">{error}</p>
              )}
            </div>

            {/* ---------- Sağ: kaynaklar + önizleme ---------- */}
            <aside className="border-t lg:border-t-0 lg:border-l border-line bg-canvas/60 p-4 sm:p-5 flex flex-col gap-4 min-w-0">
              <section className="flex flex-col gap-2 min-w-0">
                <h4 className="m-0 text-[13px] font-bold text-ink flex items-center gap-1.5">
                  <Users className="w-4 h-4 text-ink-3" /> Öğrenci parçaları ({question.fragments?.length || 0})
                </h4>
                {(question.fragments || []).length === 0 && (
                  <p className="m-0 text-[13px] text-ink-3">Parça girilmemiş.</p>
                )}
                <div className="flex flex-col gap-1.5 max-h-[260px] overflow-y-auto pr-0.5">
                  {(question.fragments || []).map((f) => (
                    <div key={f.id} className="rounded-[10px] bg-white border border-line-soft px-2.5 py-2">
                      <div className="flex items-center justify-between gap-2 text-[11.5px] text-ink-3">
                        <span className="font-semibold text-ink truncate">{f.author || 'Anonim'}</span>
                        <span className="shrink-0">↑{f.upvotes || 0} · {f.type === 'stem' ? 'kök' : f.type === 'option' ? 'şık' : 'ipucu'}</span>
                      </div>
                      <p className="m-0 mt-0.5 text-[13px] text-ink-2 leading-snug">{f.text}</p>
                    </div>
                  ))}
                </div>
              </section>

              <section className="flex flex-col gap-2 min-w-0">
                <h4 className="m-0 text-[13px] font-bold text-ink flex items-center gap-1.5">
                  <Eye className="w-4 h-4 text-ink-3" /> Canlı önizleme
                </h4>
                <div className="rounded-[12px] bg-white border border-line p-3 flex flex-col gap-2">
                  <p className="m-0 text-[13.5px] text-ink leading-relaxed">{stem.trim() || <span className="text-ink-3 italic">Soru kökü henüz yazılmadı…</span>}</p>
                  <div className="flex flex-col gap-1">
                    {OPT_KEYS.filter((k) => opts[k].trim()).map((k) => (
                      <div key={k} className={`rounded-lg px-2 py-1 text-[13px] ${correctAnswer === k ? 'bg-ok-soft font-semibold' : 'bg-canvas text-ink-2'}`}>
                        <strong className="font-mono mr-1">{k})</strong>{opts[k].trim()}
                      </div>
                    ))}
                    {filledOptionCount === 0 && <span className="text-[12.5px] text-ink-3 italic">Şık girilmedi…</span>}
                  </div>
                </div>
              </section>

              {(question.revisions || []).length > 0 && (
                <section className="flex flex-col gap-1.5 min-w-0">
                  <h4 className="m-0 text-[13px] font-bold text-ink">Son değişiklikler</h4>
                  {question.revisions!.slice(-3).reverse().map((r) => (
                    <div key={r.id} className="text-[12px] text-ink-2">
                      <span className="font-semibold text-ink">{r.editorName}</span> · {r.changeSummary || `sürüm ${r.version}`}
                    </div>
                  ))}
                </section>
              )}
            </aside>
          </div>

          {/* Footer */}
          <div className="sticky bottom-0 bg-white border-t border-line px-4 sm:px-5 py-3 flex items-center gap-2">
            <button type="button" onClick={resetToSource} className="h-11 px-3 rounded-[10px] text-[14px] font-semibold text-ink-2 hover:bg-canvas cursor-pointer inline-flex items-center gap-1.5">
              <RotateCcw className="w-4 h-4" /> Geri al
            </button>
            <span className="flex-1" />
            <button type="button" onClick={onClose} className="h-11 px-4 rounded-[10px] text-[14px] font-semibold text-ink-2 hover:bg-canvas cursor-pointer">
              Vazgeç
            </button>
            <button type="submit" disabled={isSaving}
              className="h-11 px-5 rounded-[10px] bg-accent hover:bg-accent-hover text-white font-semibold text-[14px] inline-flex items-center gap-2 cursor-pointer disabled:opacity-50">
              <Save className="w-4 h-4" /><span>{isSaving ? 'Kaydediliyor…' : canPublish ? 'Kaydet & Yayınla' : 'Taslak olarak kaydet'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
