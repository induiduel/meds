import React, { useEffect, useMemo, useState } from 'react';
import { Flag, Save, Wand2, FilePlus2, Eye, EyeOff, Check, Trash2, Inbox, ShieldCheck } from 'lucide-react';
import type { QuestionItem, QuestionOption } from '../../types';
import { ApiService, safeJsonFetch } from '../../services/api';
import type { InboxReport } from '../../services/manageConsoleService';
import { Panel, EmptyState, Seg, ConfirmButton, Field, timeLabel } from './consoleUi';

const AiQuestionOptimizerModal = React.lazy(() => import('../AiQuestionOptimizerModal').then((m) => ({ default: m.AiQuestionOptimizerModal || (m as any).default })));

/**
 * Moderasyon: solda şikâyet kuyruğu, sağda şikâyet edilen sorunun tamamı. Kararlar yöneticinin:
 * düzelt, AI ile düzelt, taslağa çevir, gizle, hatasız kapat ya da sil.
 */
interface Props {
  adminEmail: string;
  selectedCommitteeId: string;
  reports: InboxReport[];
  questions: QuestionItem[];
  pastQuestions: QuestionItem[];
  setPastQuestions: React.Dispatch<React.SetStateAction<QuestionItem[]>>;
  resolvedIds: Set<string>;
  focusReportId: string;
  setFocusReportId: (id: string) => void;
  onResolve: (r: InboxReport) => Promise<void>;
  notify: (msg: string) => void;
  onRefreshData: () => Promise<void>;
  reloadInbox: () => Promise<void>;
}

const KEYS = ['A', 'B', 'C', 'D', 'E'] as const;
type Key = (typeof KEYS)[number];

export const ManageModerationSection: React.FC<Props> = ({
  adminEmail,
  selectedCommitteeId,
  reports,
  questions,
  pastQuestions,
  setPastQuestions,
  resolvedIds,
  focusReportId,
  setFocusReportId,
  onResolve,
  notify,
  onRefreshData,
  reloadInbox,
}) => {
  const [status, setStatus] = useState<'pending' | 'resolved' | 'all'>('pending');
  const [stem, setStem] = useState('');
  const [answer, setAnswer] = useState<Key>('A');
  const [explanation, setExplanation] = useState('');
  const [options, setOptions] = useState<{ key: Key; text: string }[]>([]);
  const [saving, setSaving] = useState(false);
  const [busy, setBusy] = useState<'' | 'hide' | 'delete' | 'draft' | 'resolve'>('');
  const [aiOpen, setAiOpen] = useState(false);

  const isDone = (r: InboxReport) => resolvedIds.has(r.id) || (r.status || 'pending') !== 'pending';
  const pending = useMemo(() => reports.filter((r) => !isDone(r)), [reports, resolvedIds]); // eslint-disable-line react-hooks/exhaustive-deps
  const resolved = useMemo(() => reports.filter((r) => isDone(r)), [reports, resolvedIds]); // eslint-disable-line react-hooks/exhaustive-deps
  const list = status === 'pending' ? pending : status === 'resolved' ? resolved : reports;

  const report = useMemo(() => reports.find((r) => r.id === (focusReportId || pending[0]?.id)) || null, [reports, focusReportId, pending]);
  const question: QuestionItem | null = useMemo(() => {
    if (!report) return null;
    return pastQuestions.find((q) => q.id === report.questionId) || questions.find((q) => q.id === report.questionId) || null;
  }, [report, pastQuestions, questions]);

  // Bulut listesinde olmayan (sayfalama/senkron farkı) şikâyetli soruyu yerel sunucudan kimliğiyle getir
  const [lookupDone, setLookupDone] = useState<string | null>(null);
  useEffect(() => {
    const id = report?.questionId;
    if (!id || question || lookupDone === id) return;
    setLookupDone(id);
    safeJsonFetch<any>(`/api/past-exams?query=${encodeURIComponent(id)}`).then((res) => {
      const found: QuestionItem | undefined = (Array.isArray(res.data) ? res.data : res.data?.questions || res.data?.items || []).find((q: QuestionItem) => q.id === id);
      if (found) setPastQuestions((prev) => (prev.some((q) => q.id === id) ? prev : [...prev, { ...found, isPastExam: true } as QuestionItem]));
    });
  }, [report?.questionId, question, lookupDone, setPastQuestions]);

  useEffect(() => {
    if (!question) return;
    setStem(question.reconstruction?.stem || question.stem || question.fragments?.[0]?.text || '');
    setAnswer(((question.reconstruction?.correctAnswer || question.claimedAnswer || 'A') as Key));
    setExplanation(question.reconstruction?.explanation || '');
    const opts = (question.reconstruction?.options || (question.options || []).map((o: QuestionOption) => ({ key: o.key, text: o.text }))) as { key: string; text: string }[];
    setOptions(KEYS.map((k) => ({ key: k, text: opts.find((o) => o.key === k)?.text || '' })));
    if (!focusReportId && report) setFocusReportId(report.id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [question?.id]);

  const isPast = !!question && (question.isPastExam || pastQuestions.some((q) => q.id === question.id));
  const hidden = Boolean((question as any)?.hidden);
  const cleanOptions = () => options.filter((o) => o.text.trim()).map((o) => ({ key: o.key, text: o.text.trim() }));

  const save = async () => {
    if (!question || !report) return;
    setSaving(true);
    try {
      const reconstruction = {
        stem: stem.trim(),
        options: cleanOptions(),
        correctAnswer: answer,
        explanation: explanation.trim(),
        confidenceScore: question.reconstruction?.confidenceScore ?? 90,
        lastUpdated: new Date().toISOString(),
      };
      if (isPast) {
        const updated: QuestionItem = { ...question, reconstruction, claimedAnswer: answer, status: 'completed', updatedAt: new Date().toISOString() };
        await ApiService.saveApprovedPastQuestion(updated);
        setPastQuestions((prev) => prev.map((q) => (q.id === updated.id ? updated : q)));
      } else {
        await ApiService.adminUpdateQuestion(adminEmail, question.id, { reconstruction, claimedAnswer: answer, status: 'completed' } as Partial<QuestionItem>);
      }
      await onResolve(report);
      notify(`Soru düzeltildi ve "${report.reason}" bildirimi kapatıldı.`);
      await onRefreshData();
      await reloadInbox();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Düzeltme kaydedilemedi.');
    } finally {
      setSaving(false);
    }
  };

  const toggleHide = async () => {
    if (!question || !isPast) return;
    setBusy('hide');
    try {
      const updated = await ApiService.adminPatchPastQuestion(adminEmail, question.id, { hidden: !hidden });
      setPastQuestions((prev) => prev.map((q) => (q.id === updated.id ? updated : q)));
      notify(hidden ? 'Soru yeniden yayında.' : 'Soru gizlendi; öğrenciler artık görmüyor.');
    } catch (e) {
      notify(e instanceof Error ? e.message : 'İşlem yapılamadı.');
    } finally {
      setBusy('');
    }
  };

  const remove = async () => {
    if (!question || !report) return;
    setBusy('delete');
    try {
      if (isPast) {
        await ApiService.adminDeletePastQuestion(adminEmail, question.id);
        try {
          const { pastQuestionsCache } = await import('../../services/pastQuestionsCache');
          await pastQuestionsCache.removeQuestions([question.id]);
        } catch {}
        setPastQuestions((prev) => prev.filter((q) => q.id !== question.id));
      } else {
        await ApiService.deleteQuestion(question.id, { email: adminEmail } as any);
      }
      await onResolve(report);
      notify('Soru silindi ve bildirim kapatıldı.');
      setFocusReportId('');
      await onRefreshData();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Soru silinemedi.');
    } finally {
      setBusy('');
    }
  };

  /** Çıkmış soruyu havuza taslak olarak kopyalar ve aslını gizler (topluluk yeniden kurar) */
  const toDraft = async () => {
    if (!question || !report) return;
    setBusy('draft');
    try {
      const opts = cleanOptions();
      await ApiService.addQuestionContribution({
        committeeId: question.committeeId || selectedCommitteeId,
        isUnknownNumber: true,
        discipline: question.discipline || 'Belirtilmedi',
        topic: question.topic || `${question.discipline || ''} Şikâyetten taslak`.trim(),
        fragmentText: stem.trim(),
        author: 'Yönetici (şikâyetten taslak)',
        claimedAnswer: (answer || undefined) as any,
        options: opts.length ? opts : undefined,
      });
      if (isPast && !hidden) {
        const updated = await ApiService.adminPatchPastQuestion(adminEmail, question.id, { hidden: true });
        setPastQuestions((prev) => prev.map((q) => (q.id === updated.id ? updated : q)));
      }
      await onResolve(report);
      notify('Soru taslak olarak havuza eklendi' + (isPast ? ', aslı gizlendi.' : '.'));
      await onRefreshData();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Taslağa çevrilemedi.');
    } finally {
      setBusy('');
    }
  };

  const closeClean = async () => {
    if (!report) return;
    setBusy('resolve');
    try {
      await onResolve(report);
    } finally {
      setBusy('');
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[320px_minmax(0,1fr)] gap-3 items-start min-w-0">
      <Panel flush className="lg:sticky lg:top-0">
        <div className="p-2 border-b border-line-soft">
          <Seg
            label="Bildirim durumu"
            value={status}
            onChange={setStatus}
            className="w-full [&>button]:flex-1 [&>button]:justify-center"
            options={[
              { id: 'pending', label: 'Bekleyen', n: pending.length },
              { id: 'resolved', label: 'Çözülen', n: resolved.length },
              { id: 'all', label: 'Tümü' },
            ]}
          />
        </div>
        {list.length === 0 ? (
          <EmptyState icon={status === 'pending' ? ShieldCheck : Inbox} title={status === 'pending' ? 'Bekleyen şikâyet yok' : 'Bu filtrede kayıt yok'} />
        ) : (
          <ul className="ms-rows max-h-[38vh] lg:max-h-[calc(var(--vvh,100dvh)-260px)] overflow-y-auto overscroll-contain">
            {list.map((r) => {
              const on = report?.id === r.id;
              const done = isDone(r);
              return (
                <li key={r.id}>
                  <button type="button" onClick={() => setFocusReportId(r.id)} aria-current={on || undefined} className={`ms-row is-button ${on ? 'is-on' : ''}`}>
                    <span className={`ms-ricon ${done ? '' : 'is-bad'}`}>
                      {done ? <Check aria-hidden="true" /> : <Flag aria-hidden="true" />}
                    </span>
                    <span className="ms-row-main">
                      <span className="ms-row-title truncate">{r.reason}</span>
                      <span className="text-[13px] text-ink-2 truncate">{r.questionTopic || r.questionId}</span>
                      <span className="ms-row-meta">
                        <span className="truncate max-w-[18ch]">{r.reportedBy || 'Anonim'}</span>
                        {r.createdAt && <span>{timeLabel(r.createdAt, true)}</span>}
                      </span>
                    </span>
                  </button>
                </li>
              );
            })}
          </ul>
        )}
      </Panel>

      {!report ? (
        <Panel>
          <EmptyState icon={Flag} title="Bir şikâyet seç">Soldaki listeden bir bildirim seçince şikâyet edilen soru burada açılır.</EmptyState>
        </Panel>
      ) : (
        <section className="ms-panel" aria-label="Şikâyet edilen soru">
          <header className="flex items-start gap-3 px-4 py-3.5 border-b border-line-soft">
            <span className="ms-ricon is-bad mt-0.5"><Flag aria-hidden="true" /></span>
            <div className="min-w-0 flex-1 flex flex-col gap-1">
              <h2 className="m-0 text-[16px] font-semibold text-ink leading-snug">{report.reason}</h2>
              <p className="m-0 text-[14px] text-ink-2 leading-relaxed [overflow-wrap:anywhere]">{report.details || 'Öğrenci ayrıntı yazmamış.'}</p>
              <span className="ms-row-meta">
                <span>{report.reportedBy || 'Anonim'}</span>
                {report.createdAt && <span>{new Date(report.createdAt).toLocaleString('tr-TR', { dateStyle: 'medium', timeStyle: 'short' })}</span>}
                {isDone(report) && <span className="ms-tag is-ok"><Check /> Kapatıldı</span>}
              </span>
            </div>
          </header>

          {!question ? (
            <EmptyState icon={Inbox} title="Bağlı soru bulunamadı" action={<button type="button" onClick={() => void closeClean()} disabled={busy === 'resolve'} className="ms-btn">Bildirimi kapat</button>}>
              Soru silinmiş ya da başka bir kurula taşınmış olabilir.
            </EmptyState>
          ) : (
            <>
              <div className="px-4 py-4 flex flex-col gap-4">
                <div className="flex flex-wrap items-center gap-1.5 text-[12.5px] text-ink-3">
                  <span className={`ms-tag ${isPast ? '' : 'is-accent'}`}>{isPast ? 'Çıkmış soru' : 'Havuz sorusu'}</span>
                  {hidden && <span className="ms-tag is-warn"><EyeOff /> Gizli</span>}
                  <span className="truncate">{[question.discipline, question.topic, question.examYear, `S.${question.questionNumber || '?'}`].filter(Boolean).join(' · ')}</span>
                  <span className="font-mono text-[11.5px] text-ink-3 ml-auto truncate max-w-[24ch]" title={question.id}>{question.id}</span>
                </div>

                <Field label="Soru kökü">
                  <textarea value={stem} onChange={(e) => setStem(e.target.value)} rows={4} className="ms-input text-[15px]" />
                </Field>

                <div className="ms-field">
                  <span className="lbl">Şıklar · doğru cevabı harfe dokunarak seç</span>
                  <ol className="m-0 p-0 list-none flex flex-col gap-1.5">
                    {options.map((o, i) => {
                      const correct = answer === o.key;
                      return (
                        <li key={o.key} className={`ms-opt ${correct ? 'is-correct' : ''} !grid-cols-[28px_minmax(0,1fr)] !py-1 !pl-1.5`}>
                          <button type="button" onClick={() => setAnswer(o.key)} aria-pressed={correct} aria-label={`${o.key} şıkkını doğru cevap yap`} className="ms-opt-key cursor-pointer">
                            {o.key}
                          </button>
                          <input
                            value={o.text}
                            onChange={(e) => setOptions((prev) => prev.map((x, j) => (j === i ? { ...x, text: e.target.value } : x)))}
                            placeholder={`${o.key} şıkkı`}
                            aria-label={`${o.key} şıkkı`}
                            className="ms-bare-input w-full min-w-0 h-9 bg-transparent border-0 outline-0 text-[14.5px] text-ink"
                          />
                        </li>
                      );
                    })}
                  </ol>
                </div>

                <Field label="Açıklama" hint="Öğrenci doğru cevabın gerekçesini burada görür.">
                  <textarea value={explanation} onChange={(e) => setExplanation(e.target.value)} rows={3} className="ms-input" />
                </Field>
              </div>

              <div className="ms-actionbar">
                <button type="button" onClick={() => void save()} disabled={saving || !stem.trim()} className="ms-btn is-primary">
                  <Save /> {saving ? 'Kaydediliyor…' : 'Düzelt ve kapat'}
                </button>
                <button type="button" onClick={() => setAiOpen(true)} className="ms-btn is-tonal">
                  <Wand2 /> AI ile düzelt
                </button>
                <button type="button" onClick={() => void closeClean()} disabled={busy === 'resolve'} className="ms-btn" title="Soru doğru; bildirimi kapat">
                  <Check /> Hatasız, kapat
                </button>
                <button type="button" onClick={() => void toDraft()} disabled={busy === 'draft'} className="ms-btn is-ghost" title="Soruyu havuza taslak olarak kopyala, aslını gizle">
                  <FilePlus2 /> Taslağa çevir
                </button>
                {isPast && (
                  <button type="button" onClick={() => void toggleHide()} disabled={busy === 'hide'} className="ms-btn is-ghost">
                    {hidden ? <Eye /> : <EyeOff />} {hidden ? 'Yayına al' : 'Gizle'}
                  </button>
                )}
                <span className="flex-1" />
                <ConfirmButton icon={Trash2} className="ms-btn is-danger" confirmLabel="Kalıcı silmeyi onayla" busy={busy === 'delete'} busyLabel="Siliniyor…" onConfirm={remove}>
                  Sil
                </ConfirmButton>
              </div>
            </>
          )}
        </section>
      )}

      {aiOpen && question && (
        <React.Suspense fallback={null}>
          <AiQuestionOptimizerModal
            question={question}
            isOpen
            onClose={() => setAiOpen(false)}
            onSaved={(updated) => {
              setAiOpen(false);
              setPastQuestions((prev) => prev.map((q) => (q.id === updated.id ? updated : q)));
              if (report) void onResolve(report);
              notify('AI düzeltmesi kaydedildi ve bildirim kapatıldı.');
            }}
          />
        </React.Suspense>
      )}
    </div>
  );
};
