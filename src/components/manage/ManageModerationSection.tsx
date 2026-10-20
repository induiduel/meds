import React, { useEffect, useMemo, useState } from 'react';
import { Flag, Save, Wand2, FilePlus2, Eye, EyeOff, Check, Trash2, Inbox, UserPlus, Tag, Ban, Reply, Clock } from 'lucide-react';
import type { QuestionItem, QuestionOption } from '../../types';
import { ApiService, safeJsonFetch } from '../../services/api';
import type { InboxReport } from '../../services/manageConsoleService';
import { EmptyState, ConfirmButton, Field, timeLabel, Drawer } from './consoleUi';
import { StatRow, Tabs14, SearchField, Toolbar, DataTable, Pill, DetailNav, DetailLayout, FactList, Card14, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';
import { useModerationMeta, ModerationActionDrawer, MetaPills, metaFacts, ReplyHistory, isSnoozed, isRejected, isMine, type ActionMode } from './moderationActions';

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
  const [status, setStatus] = useState<'pending' | 'mine' | 'snoozed' | 'rejected' | 'resolved' | 'all'>('pending');
  const { meta, act } = useModerationMeta();
  const [actMode, setActMode] = useState<ActionMode | null>(null);
  const [actIds, setActIds] = useState<string[]>([]);
  const openAction = (mode: ActionMode, ids: string[]) => { setActIds(ids); setActMode(mode); };
  const [stem, setStem] = useState('');
  const [answer, setAnswer] = useState<Key>('A');
  const [explanation, setExplanation] = useState('');
  const [options, setOptions] = useState<{ key: Key; text: string }[]>([]);
  const [saving, setSaving] = useState(false);
  const [busy, setBusy] = useState<'' | 'hide' | 'delete' | 'draft' | 'resolve'>('');
  const [aiOpen, setAiOpen] = useState(false);

  const isDone = (r: InboxReport) => resolvedIds.has(r.id) || (r.status || 'pending') !== 'pending' || isRejected(meta[r.id]);
  const open = useMemo(() => reports.filter((r) => !isDone(r)), [reports, resolvedIds, meta]); // eslint-disable-line react-hooks/exhaustive-deps
  const pending = useMemo(() => open.filter((r) => !isSnoozed(meta[r.id])), [open, meta]);
  const snoozed = useMemo(() => open.filter((r) => isSnoozed(meta[r.id])), [open, meta]);
  const mine = useMemo(() => open.filter((r) => isMine(meta[r.id])), [open, meta]);
  const rejected = useMemo(() => reports.filter((r) => isRejected(meta[r.id])), [reports, meta]);
  const resolved = useMemo(() => reports.filter((r) => isDone(r) && !isRejected(meta[r.id])), [reports, resolvedIds, meta]); // eslint-disable-line react-hooks/exhaustive-deps
  const [q, setQ] = useState('');
  const list = useMemo(() => {
    const base = status === 'pending' ? pending : status === 'mine' ? mine : status === 'snoozed' ? snoozed : status === 'rejected' ? rejected : status === 'resolved' ? resolved : reports;
    const t = q.trim().toLocaleLowerCase('tr-TR');
    if (!t) return base;
    return base.filter((r) => [r.reason, r.details, r.questionTopic, r.questionId, r.reportedBy, meta[r.id]?.assignee, ...(meta[r.id]?.tags || [])].some((x) => String(x || '').toLocaleLowerCase('tr-TR').includes(t)));
  }, [status, pending, mine, snoozed, rejected, resolved, reports, q, meta]);
  const selection = useSelection<string>();
  const [bulkBusy, setBulkBusy] = useState(false);

  const report = useMemo(() => (focusReportId ? reports.find((r) => r.id === focusReportId) || null : null), [reports, focusReportId]);
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
        await ApiService.saveApprovedPastQuestion(updated, adminEmail);
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

  const bulkResolve = async () => {
    const items = reports.filter((r) => selection.has(r.id) && !isDone(r));
    setBulkBusy(true);
    let ok = 0;
    let bad = 0;
    for (const r of items) {
      try { await onResolve(r); ok++; } catch { bad++; }
    }
    setBulkBusy(false);
    notify(`${ok} başarılı, ${bad} hata.`);
    if (!bad) selection.clear();
    try { await reloadInbox(); } catch {}
  };

  const cols: Col<InboxReport>[] = [
    { key: 'reason', label: 'Bildirim', main: true, render: (r) => r.reason },
    { key: 'topic', label: 'Soru', render: (r) => <span className="clip">{r.questionTopic || r.questionId}</span>, width: '28%' },
    { key: 'who', label: 'Gönderen', muted: true, render: (r) => r.reportedBy || 'Anonim' },
    { key: 'st', label: 'Durum', render: (r) => (isRejected(meta[r.id]) ? <Pill tone="warn">Reddedildi</Pill> : isDone(r) ? <Pill tone="ok">Kapatıldı</Pill> : <Pill tone="bad">Açık</Pill>) },
    { key: 'meta', label: 'Atama ve etiket', render: (r) => <MetaPills m={meta[r.id]} />, width: '20%' },
    { key: 'when', label: 'Zaman', muted: true, render: (r) => (r.createdAt ? timeLabel(r.createdAt, true) : '—') },
  ];

  const metaActions = report ? (
    <>
      <button type="button" onClick={() => openAction('assign', [report.id])} className="m14-btn ghost"><UserPlus aria-hidden="true" /> Kişiye ata</button>
      <button type="button" onClick={() => openAction('tags', [report.id])} className="m14-btn ghost"><Tag aria-hidden="true" /> Etiket</button>
      <button type="button" onClick={() => openAction('snooze', [report.id])} className="m14-btn ghost"><Clock aria-hidden="true" /> Ertele</button>
      <button type="button" onClick={() => openAction('reply', [report.id])} className="m14-btn ghost"><Reply aria-hidden="true" /> Kişiye yanıt</button>
      <button type="button" onClick={() => openAction('reject', [report.id])} className="m14-btn ghost"><Ban aria-hidden="true" /> {isRejected(meta[report.id]) ? 'Ret' : 'Reddet'}</button>
    </>
  ) : null;

  const actions = question ? (
    <>
      {metaActions}
      <ConfirmButton icon={Trash2} className="m14-btn danger" confirmLabel="Kalıcı silmeyi onayla" busy={busy === 'delete'} busyLabel="Siliniyor…" onConfirm={remove}>
        Sil
      </ConfirmButton>
      {isPast && (
        <button type="button" onClick={() => void toggleHide()} disabled={busy === 'hide'} className="m14-btn ghost">
          {hidden ? <Eye aria-hidden="true" /> : <EyeOff aria-hidden="true" />} {hidden ? 'Yayına al' : 'Gizle'}
        </button>
      )}
      <button type="button" onClick={() => void toDraft()} disabled={busy === 'draft'} className="m14-btn ghost" title="Soruyu havuza taslak olarak kopyala, aslını gizle">
        <FilePlus2 aria-hidden="true" /> Taslağa çevir
      </button>
      <button type="button" onClick={() => void closeClean()} disabled={busy === 'resolve'} className="m14-btn" title="Soru doğru; bildirimi kapat">
        <Check aria-hidden="true" /> Hatasız, kapat
      </button>
      <button type="button" onClick={() => setAiOpen(true)} className="m14-btn">
        <Wand2 aria-hidden="true" /> AI ile düzelt
      </button>
      <button type="button" onClick={() => void save()} disabled={saving || !stem.trim()} className="m14-btn primary">
        <Save aria-hidden="true" /> {saving ? 'Kaydediliyor…' : 'Düzelt ve kapat'}
      </button>
    </>
  ) : report ? (
    <>
      {metaActions}
      <button type="button" onClick={() => void closeClean()} disabled={busy === 'resolve'} className="m14-btn primary">Bildirimi kapat</button>
    </>
  ) : null;

  return (
    <div className="min-w-0 flex flex-col gap-3">
      <StatRow
        stats={[
          { label: 'Bekleyen', value: pending.length, tone: pending.length ? 'bad' : 'ok', onClick: () => setStatus('pending') },
          { label: 'Bana atanan', value: mine.length, onClick: () => setStatus('mine') },
          { label: 'Ertelenen', value: snoozed.length, onClick: () => setStatus('snoozed') },
          { label: 'Çözülen', value: resolved.length, onClick: () => setStatus('resolved') },
          { label: 'Toplam bildirim', value: reports.length, onClick: () => setStatus('all') },
        ]}
      />
      <Toolbar>
        <Tabs14
          label="Bildirim durumu"
          value={status}
          onChange={setStatus}
          options={[
            { id: 'pending', label: 'Bekleyen', n: pending.length },
            { id: 'mine', label: 'Bana atanan', n: mine.length },
            { id: 'snoozed', label: 'Ertelenenler', n: snoozed.length },
            { id: 'rejected', label: 'Reddedilen', n: rejected.length },
            { id: 'resolved', label: 'Çözülen', n: resolved.length },
            { id: 'all', label: 'Tümü', n: reports.length },
          ]}
        />
        <SearchField value={q} onChange={setQ} placeholder="Bildirim, soru ya da kişi" />
      </Toolbar>
      <BulkBar
        count={selection.count}
        noun="bildirim"
        busy={bulkBusy}
        onClear={selection.clear}
        actions={[
          { label: 'Hatasız kapat', kind: 'main', run: bulkResolve },
          { label: 'Kişiye ata', run: () => openAction('assign', [...selection.sel]) },
          { label: 'Etiket ekle', run: () => openAction('tags', [...selection.sel]) },
          { label: 'Ertele', run: () => openAction('snooze', [...selection.sel]) },
          { label: 'Kişiye yanıt', run: () => openAction('reply', [...selection.sel]) },
          { label: 'Reddet', kind: 'danger', run: () => openAction('reject', [...selection.sel]) },
        ]}
      />
      <DataTable
        rows={list}
        cols={cols}
        rowKey={(r) => r.id}
        onOpen={(r) => setFocusReportId(r.id)}
        selection={selection}
        activeKey={report?.id || null}
        minWidth={860}
        empty={status === 'pending' ? 'Bekleyen şikâyet yok.' : 'Bu filtrede kayıt yok.'}
      />

      <Drawer
        open={!!report && !actMode}
        onClose={() => setFocusReportId('')}
        title={report?.reason || 'Bildirim'}
        label="Şikâyet edilen soru"
        wide
        head={<DetailNav list={list} current={report} same={(a, b) => a.id === b.id} onGo={(r) => setFocusReportId(r.id)} />}
        foot={actions}
      >
        {report && (
          <DetailLayout
            main={
              <>
                <Card14 title="Bildirim metni">
                  <p className="m-0 text-base text-ink leading-relaxed [overflow-wrap:anywhere]">{report.details || 'Öğrenci ayrıntı yazmamış.'}</p>
                </Card14>
                {!question ? (
                  <Card14>
                    <EmptyState icon={Inbox} title="Bağlı soru bulunamadı">Soru silinmiş ya da başka bir kurula taşınmış olabilir.</EmptyState>
                  </Card14>
                ) : (
                  <Card14 title="İlgili soru" tools={hidden ? <Pill tone="warn"><EyeOff aria-hidden="true" /> Gizli</Pill> : undefined}>
                    <div className="flex flex-col gap-4">
                      <Field label="Soru kökü">
                        <textarea value={stem} onChange={(e) => setStem(e.target.value)} rows={4} className="ms-input text-md" />
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
                                  className="ms-bare-input w-full min-w-0 h-9 bg-transparent border-0 outline-0 text-md text-ink"
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
                  </Card14>
                )}
              </>
            }
            side={
              <Card14 title="Bilgi">
                <FactList
                  items={[
                    { k: 'Gönderen', v: report.reportedBy || 'Anonim' },
                    { k: 'Tarih', v: report.createdAt ? new Date(report.createdAt).toLocaleString('tr-TR', { dateStyle: 'medium', timeStyle: 'short' }) : '—' },
                    { k: 'Durum', v: isDone(report) ? <Pill tone="ok"><Check aria-hidden="true" /> Kapatıldı</Pill> : <Pill tone="bad"><Flag aria-hidden="true" /> Açık</Pill> },
                    ...(question
                      ? [
                          { k: 'Tür', v: isPast ? 'Çıkmış soru' : 'Havuz sorusu' },
                          { k: 'Konu', v: [question.discipline, question.topic, question.examYear, `S.${question.questionNumber || '?'}`].filter(Boolean).join(' · ') },
                          { k: 'Kimlik', v: <span className="font-mono text-xs [overflow-wrap:anywhere]">{question.id}</span> },
                        ]
                      : [{ k: 'Soru kimliği', v: <span className="font-mono text-xs [overflow-wrap:anywhere]">{report.questionId}</span> }]),
                    ...metaFacts(meta[report.id]),
                  ]}
                />
              </Card14>
            }
          />
        )}
        {report && <div className="mt-3"><ReplyHistory m={meta[report.id]} /></div>}
      </Drawer>

      <ModerationActionDrawer
        mode={actMode}
        ids={actIds}
        kind="report"
        current={actIds.length === 1 ? meta[actIds[0]] : undefined}
        onClose={() => setActMode(null)}
        act={act}
      />

      {aiOpen && question && (
        <React.Suspense fallback={null}>
          <AiQuestionOptimizerModal
            question={question}
            isOpen
            onClose={() => setAiOpen(false)}
            onSaved={async (updated) => {
              setAiOpen(false);
              setPastQuestions((prev) => prev.map((q) => (q.id === updated.id ? updated : q)));
              if (report) await onResolve(report);
              notify('AI düzeltmesi kaydedildi ve bildirim kapatıldı.');
              try {
                await onRefreshData();
                await reloadInbox();
              } catch (_) {}
            }}
          />
        </React.Suspense>
      )}
    </div>
  );
};
