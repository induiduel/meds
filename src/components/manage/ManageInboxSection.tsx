import React, { useMemo, useState } from 'react';
import { Flag, MessageSquare, FileText, Bell, Eye, Check, Send, Pencil, Trash2, Inbox, CheckCircle2, ChevronDown, Smartphone, User, ExternalLink } from 'lucide-react';
import type { QuestionItem, AdminNotification } from '../../types';
import type { InboxReport, InboxComment } from '../../services/manageConsoleService';
import { Panel, EmptyState, SearchBox, ChipBar, Switch, ConfirmButton, dayLabel, timeLabel } from './consoleUi';
import { AdminMobileNotificationCard } from '../AdminMobileNotificationCard';

/**
 * Gelen kutusu: bildirim, yorum, taslak ve sistem uyarıları tek iş kuyruğunda, en yenisi üstte.
 * Tür çipleri sayılarla süzer; her satır kendi işini satırın üstünde bitirir.
 */
type Kind = 'report' | 'comment' | 'draft' | 'notice';
type Filter = 'all' | Kind;

interface QueueItem {
  key: string;
  kind: Kind;
  at?: string;
  title: string;
  text?: string;
  sender?: string;
  reason?: string;
  questionId?: string;
  meta: string[];
  done?: boolean;
  unread?: boolean;
  report?: InboxReport;
  comment?: InboxComment;
  draft?: QuestionItem;
}

const KIND_META: Record<Kind, { icon: React.ElementType; tone: string; label: string }> = {
  report: { icon: Flag, tone: 'is-bad', label: 'Hata bildirimi' },
  comment: { icon: MessageSquare, tone: 'is-accent', label: 'Yorum' },
  draft: { icon: FileText, tone: 'is-warn', label: 'Taslak' },
  notice: { icon: Bell, tone: '', label: 'Sistem uyarısı' },
};

const PAGE = 40;

interface Props {
  reports: InboxReport[];
  comments: InboxComment[];
  drafts: QuestionItem[];
  notifications: AdminNotification[];
  resolvedIds: Set<string>;
  busyAction: string | null;
  loading: boolean;
  onReview: (r: InboxReport) => void;
  onResolve: (r: InboxReport) => void;
  onEditReport?: (r: InboxReport, updates: { reason: string; details: string }) => void;
  onDeleteReport?: (r: InboxReport) => void;
  onEditComment?: (c: InboxComment, text: string) => void;
  onDeleteComment: (c: InboxComment) => void;
  onEditDraft: (d: QuestionItem) => void;
  onPublishDraft: (d: QuestionItem) => void;
  onDeleteDraft: (d: QuestionItem) => void;
  onNavigateToData?: (questionId: string, dsId?: 'questions' | 'past') => void;
}

export const ManageInboxSection: React.FC<Props> = ({
  reports,
  comments,
  drafts,
  notifications,
  resolvedIds,
  busyAction,
  loading,
  onReview,
  onResolve,
  onEditReport,
  onDeleteReport,
  onEditComment,
  onDeleteComment,
  onEditDraft,
  onPublishDraft,
  onDeleteDraft,
  onNavigateToData,
}) => {
  const [filter, setFilter] = useState<Filter>('all');
  const [query, setQuery] = useState('');
  const [showResolved, setShowResolved] = useState(false);
  const [showNotificationCard, setShowNotificationCard] = useState(false);
  const [limit, setLimit] = useState(PAGE);

  const isDone = (r: InboxReport) => resolvedIds.has(r.id) || (r.status || 'pending') !== 'pending';

  const all: QueueItem[] = useMemo(() => {
    const out: QueueItem[] = [];
    for (const r of reports) {
      out.push({
        key: `r-${r.id}`,
        kind: 'report',
        at: r.createdAt,
        title: r.reason,
        text: r.details,
        sender: r.reportedBy || 'Anonim Öğrenci',
        reason: r.reason,
        questionId: r.questionId,
        meta: [r.questionTopic || `Soru #${r.questionId}`, r.reportedBy ? `Gönderen: ${r.reportedBy}` : 'Anonim'].filter(Boolean) as string[],
        done: isDone(r),
        report: r,
      });
    }
    for (const c of comments) {
      out.push({
        key: `c-${c.id}`,
        kind: 'comment',
        at: c.createdAt,
        title: c.text,
        sender: c.author || 'Öğrenci',
        reason: 'Soruya yeni yorum yapıldı',
        questionId: c.questionId,
        meta: [c.author ? `Yazan: ${c.author}` : 'Öğrenci', c.questionTopic || `Soru #${c.questionId}`].filter(Boolean) as string[],
        comment: c,
      });
    }
    for (const d of drafts) {
      const num = d.isUnassignedNumber ? 'Numarasız' : d.questionNumber ? `S.${d.questionNumber}` : 'Numarasız';
      out.push({
        key: `d-${d.id}`,
        kind: 'draft',
        at: d.updatedAt || d.createdAt,
        title: d.topic || d.discipline || 'Konusuz taslak',
        text: d.reconstruction?.stem || d.stem || d.fragments?.[0]?.text,
        sender: d.contributedByName || d.author || d.fragments?.[0]?.author || 'Öğrenci Katkısı',
        reason: 'Taslak soru onayı bekleniyor',
        questionId: d.id,
        meta: [num, d.discipline, `${d.fragments?.length || 0} parça`, `${d.options?.length || 0} şık`].filter(Boolean) as string[],
        draft: d,
      });
    }
    for (const n of notifications) {
      out.push({
        key: `n-${n.id}`,
        kind: 'notice',
        at: n.timestamp,
        title: n.title,
        text: n.message,
        sender: n.author || 'Sistem',
        reason: n.type === 'new_fragment' ? 'Yeni hafıza parçası eklendi' : n.type === 'unassigned_question' ? 'Numarasız soru girildi' : 'Sistem bildirimi',
        questionId: n.questionId,
        meta: [n.author ? `Kaynak: ${n.author}` : ''].filter(Boolean) as string[],
        unread: !n.isRead,
      });
    }
    return out.sort((a, b) => (b.at || '').localeCompare(a.at || ''));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [reports, comments, drafts, notifications, resolvedIds]);

  const q = query.trim().toLocaleLowerCase('tr-TR');
  const base = all.filter((i) => (showResolved || !i.done) && (!q || [i.title, i.text, ...i.meta].join(' ').toLocaleLowerCase('tr-TR').includes(q)));
  const count = (k: Kind) => base.filter((i) => i.kind === k).length;
  const visible = filter === 'all' ? base : base.filter((i) => i.kind === filter);
  const shown = visible.slice(0, limit);

  const pendingReports = reports.filter((r) => !isDone(r)).length;
  const resolvedCount = reports.length - pendingReports;

  const [editingReport, setEditingReport] = useState<{ report: InboxReport; reason: string; details: string } | null>(null);
  const [editingComment, setEditingComment] = useState<{ comment: InboxComment; text: string } | null>(null);

  // Gün başlıklarıyla gruplanmış satırlar
  const rows: React.ReactNode[] = [];
  let lastDay = '';
  for (const item of shown) {
    const day = dayLabel(item.at);
    if (day !== lastDay) {
      rows.push(
        <li key={`day-${day}-${item.key}`} className="ms-day" aria-hidden="true">
          {day}
        </li>,
      );
      lastDay = day;
    }
    rows.push(
      <QueueRow
        key={item.key}
        item={item}
        busyAction={busyAction}
        onReview={onReview}
        onResolve={onResolve}
        onStartEditReport={(r) => setEditingReport({ report: r, reason: r.reason || '', details: r.details || '' })}
        onDeleteReport={onDeleteReport}
        onStartEditComment={(c) => setEditingComment({ comment: c, text: c.text || '' })}
        onDeleteComment={onDeleteComment}
        onEditDraft={onEditDraft}
        onPublishDraft={onPublishDraft}
        onDeleteDraft={onDeleteDraft}
        onNavigateToData={onNavigateToData}
      />
    );
  }

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <div className="flex flex-col md:flex-row md:items-center gap-2">
        <SearchBox value={query} onChange={(v) => { setQuery(v); setLimit(PAGE); }} placeholder="Kuyrukta ara: bildirim, yorum, taslak, kişi" className="flex-1" />
        <button
          type="button"
          onClick={() => setShowNotificationCard(!showNotificationCard)}
          aria-pressed={showNotificationCard}
          className={`ui-btn is-sm shrink-0 ${showNotificationCard ? 'is-primary' : 'is-tonal'}`}
          title="Telefonda (nofrostlife.com.tr) yönetici bildirim ayarları"
        >
          <Smartphone />
          <span>{showNotificationCard ? 'Bildirim ayarlarını kapat' : 'Telefon bildirimleri'}</span>
        </button>
        {resolvedCount > 0 && <Switch checked={showResolved} onChange={setShowResolved} label={`Çözülenleri göster (${resolvedCount})`} />}
      </div>

      {showNotificationCard && (
        <div className="animate-fade-in my-1">
          <AdminMobileNotificationCard onClose={() => setShowNotificationCard(false)} />
        </div>
      )}
      <ChipBar
        label="Tür"
        value={filter}
        onChange={(v) => { setFilter(v); setLimit(PAGE); }}
        options={[
          { id: 'all', label: 'Tümü', n: base.length },
          { id: 'report', label: 'Hata bildirimi', n: count('report'), icon: Flag },
          { id: 'comment', label: 'Yorum', n: count('comment'), icon: MessageSquare },
          { id: 'draft', label: 'Taslak', n: count('draft'), icon: FileText },
          { id: 'notice', label: 'Sistem uyarısı', n: count('notice'), icon: Bell },
        ]}
      />

      <Panel flush>
        {loading && all.length === 0 ? (
          <div className="px-4 py-6 flex flex-col gap-2" role="status" aria-label="Kuyruk yükleniyor">
            {[0, 1, 2].map((i) => (
              <div key={i} className="h-14 rounded-xl bg-field ms-shimmer" />
            ))}
          </div>
        ) : shown.length === 0 ? (
          q ? (
            <EmptyState icon={Inbox} title="Aramaya uyan kayıt yok">“{query}” için kuyrukta bir şey bulunamadı.</EmptyState>
          ) : (
            <EmptyState icon={CheckCircle2} title="Kuyruk boş">
              {filter === 'all' ? 'Bekleyen bildirim, yorum, taslak ya da uyarı yok.' : `Bu türde bekleyen ${KIND_META[filter].label.toLocaleLowerCase('tr-TR')} yok.`}
            </EmptyState>
          )
        ) : (
          <ul className="ms-rows">{rows}</ul>
        )}
        {visible.length > limit && (
          <button type="button" onClick={() => setLimit((n) => n + PAGE)} className="w-full h-11 border-t border-line-soft text-sm font-semibold text-accent inline-flex items-center justify-center gap-1 cursor-pointer hover:bg-canvas rounded-b-2xl">
            <ChevronDown className="w-4 h-4" /> {visible.length - limit} kayıt daha
          </button>
        )}
      </Panel>

      {/* Hata Bildirimi Düzenleme Penceresi */}
      {editingReport && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/60 backdrop-blur-xs animate-fade-in" onClick={() => setEditingReport(null)}>
          <div className="bg-white rounded-2xl shadow-2xl border border-line w-full max-w-lg p-5 flex flex-col gap-4" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between pb-2 border-b border-line">
              <h3 className="font-bold text-base text-ink flex items-center gap-2">
                <Flag className="w-4 h-4 text-bad" />
                <span>Hata Bildirimini Düzenle</span>
              </h3>
              <span className="text-xs font-mono text-ink-3">#{editingReport.report.id}</span>
            </div>

            <div className="flex flex-col gap-3">
              <label className="flex flex-col gap-1">
                <span className="text-xs font-semibold text-ink-2">Bildirim Konusu / Sebep:</span>
                <input
                  type="text"
                  value={editingReport.reason}
                  onChange={(e) => setEditingReport({ ...editingReport, reason: e.target.value })}
                  className="h-10 px-3 rounded-lg border border-line-2 text-sm focus:border-accent outline-0"
                  placeholder="Örn: Yanlış şık / Doğru cevap C olmalı"
                />
              </label>

              <label className="flex flex-col gap-1">
                <span className="text-xs font-semibold text-ink-2">Detaylı Açıklama:</span>
                <textarea
                  value={editingReport.details}
                  onChange={(e) => setEditingReport({ ...editingReport, details: e.target.value })}
                  rows={4}
                  className="p-3 rounded-lg border border-line-2 text-sm focus:border-accent outline-0 resize-y"
                  placeholder="Öğrencinin veya kullanıcının bildirdiği hata ayrıntısı..."
                />
              </label>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-line">
              <button
                type="button"
                onClick={() => setEditingReport(null)}
                className="px-4 py-2 rounded-lg text-xs font-semibold text-ink-2 hover:bg-field"
              >
                Vazgeç
              </button>
              <button
                type="button"
                disabled={!editingReport.reason.trim()}
                onClick={async () => {
                  if (onEditReport) {
                    await onEditReport(editingReport.report, {
                      reason: editingReport.reason.trim(),
                      details: editingReport.details.trim(),
                    });
                  }
                  setEditingReport(null);
                }}
                className="px-4 py-2 rounded-lg text-xs font-semibold bg-accent text-white hover:bg-accent/90 disabled:opacity-50"
              >
                Değişiklikleri Kaydet
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Yorum Düzenleme Penceresi */}
      {editingComment && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/60 backdrop-blur-xs animate-fade-in" onClick={() => setEditingComment(null)}>
          <div className="bg-white rounded-2xl shadow-2xl border border-line w-full max-w-lg p-5 flex flex-col gap-4" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between pb-2 border-b border-line">
              <h3 className="font-bold text-base text-ink flex items-center gap-2">
                <MessageSquare className="w-4 h-4 text-accent" />
                <span>Öğrenci Yorumunu Düzenle</span>
              </h3>
              <span className="text-xs font-mono text-ink-3">#{editingComment.comment.id}</span>
            </div>

            <div className="flex flex-col gap-3">
              <label className="flex flex-col gap-1">
                <span className="text-xs font-semibold text-ink-2">Yorum Metni:</span>
                <textarea
                  value={editingComment.text}
                  onChange={(e) => setEditingComment({ ...editingComment, text: e.target.value })}
                  rows={4}
                  className="p-3 rounded-lg border border-line-2 text-sm focus:border-accent outline-0 resize-y"
                  placeholder="Yorum veya çözüm önerisi..."
                />
              </label>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-line">
              <button
                type="button"
                onClick={() => setEditingComment(null)}
                className="px-4 py-2 rounded-lg text-xs font-semibold text-ink-2 hover:bg-field"
              >
                Vazgeç
              </button>
              <button
                type="button"
                disabled={!editingComment.text.trim()}
                onClick={async () => {
                  if (onEditComment) {
                    await onEditComment(editingComment.comment, editingComment.text.trim());
                  }
                  setEditingComment(null);
                }}
                className="px-4 py-2 rounded-lg text-xs font-semibold bg-accent text-white hover:bg-accent/90 disabled:opacity-50"
              >
                Değişiklikleri Kaydet
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

interface QueueRowProps {
  item: QueueItem;
  busyAction: string | null;
  onReview: (r: InboxReport) => void;
  onResolve: (r: InboxReport) => void;
  onStartEditReport?: (r: InboxReport) => void;
  onDeleteReport?: (r: InboxReport) => void;
  onStartEditComment?: (c: InboxComment) => void;
  onDeleteComment: (c: InboxComment) => void;
  onEditDraft: (d: QuestionItem) => void;
  onPublishDraft: (d: QuestionItem) => void;
  onDeleteDraft: (d: QuestionItem) => void;
  onNavigateToData?: (questionId: string, dsId?: 'questions' | 'past') => void;
}

const QueueRow: React.FC<QueueRowProps> = ({
  item,
  busyAction,
  onReview,
  onResolve,
  onStartEditReport,
  onDeleteReport,
  onStartEditComment,
  onDeleteComment,
  onEditDraft,
  onPublishDraft,
  onDeleteDraft,
  onNavigateToData,
}) => {
  const m = KIND_META[item.kind];
  const Icon = m.icon;
  const time = timeLabel(item.at);
  return (
    <li className={`ms-row ${item.done ? 'is-done' : ''}`}>
      <span className={`ms-ricon ${m.tone}`} title={m.label}>
        <Icon aria-hidden="true" />
      </span>
      <div className="ms-row-main">
        {/* Kimden & Neden Başlığı */}
        <div className="flex flex-wrap items-center gap-1.5 text-xs text-ink-3">
          <span className="inline-flex items-center gap-1 font-semibold text-ink bg-surface-2 px-2 py-0.5 rounded-md border border-line-soft">
            <User className="w-3.5 h-3.5 text-accent" />
            {item.sender || 'Bilinmiyor'}
          </span>
          <span className="text-ink-3">·</span>
          <span className="text-ink-2 font-medium bg-warn-soft text-warn border border-warn/60 px-2 py-0.5 rounded-md text-xs">
            {item.reason || m.label}
          </span>
          {item.questionId && onNavigateToData && (
            <button
              type="button"
              onClick={() => onNavigateToData(item.questionId!)}
              className="text-accent hover:underline inline-flex items-center gap-0.5 text-xs font-semibold ml-1 cursor-pointer"
              title="Bu soruyu veritabanında bul ve düzenle"
            >
              <span>{item.questionId.startsWith('past-') ? 'Çıkmış Soru' : 'Soru'} #{item.questionId.replace(/^q-|^past-/, '')}</span>
              <ExternalLink className="w-3 h-3" />
            </button>
          )}
        </div>

        <span className={`ms-row-title ${item.kind === 'comment' ? 'font-medium' : ''} mt-0.5`}>
          <span className="sr-only">{m.label}: </span>
          {item.title}
        </span>
        {item.text && <span className="ms-row-text">{item.text}</span>}
        <span className="ms-row-meta">
          {item.done && <span className="ms-tag is-ok"><Check /> Çözüldü</span>}
          {item.unread && <span className="ms-tag is-accent">Yeni</span>}
          {item.meta.map((x, i) => (
            <span key={i} className="truncate max-w-[32ch]">{x}</span>
          ))}
          {time && <span className="tabular-nums">{time}</span>}
        </span>
      </div>
      <div className="ms-row-actions">
        {item.report && (
          <>
            <button type="button" onClick={() => onReview(item.report!)} className="ms-btn is-sm is-tonal" title="Soruyu incele">
              <Eye /> İncele
            </button>
            {onStartEditReport && (
              <button type="button" onClick={() => onStartEditReport(item.report!)} className="ms-btn is-sm" title="Hata bildirimini düzenle">
                <Pencil /> Düzenle
              </button>
            )}
            {!item.done && (
              <button type="button" onClick={() => onResolve(item.report!)} disabled={busyAction === `resolve-${item.report.id}`} className="ms-btn is-sm" title="Bildirimi kapat">
                <Check /> Çözüldü
              </button>
            )}
            {onDeleteReport && (
              <ConfirmButton
                icon={Trash2}
                confirmLabel="Kalıcı Silinsin mi?"
                busy={busyAction === `delreport-${item.report.id}`}
                onConfirm={() => onDeleteReport(item.report!)}
                title="Hata bildirimini tüm veritabanından kalıcı olarak sil"
              >
                Sil
              </ConfirmButton>
            )}
          </>
        )}
        {item.comment && (
          <>
            {onStartEditComment && (
              <button type="button" onClick={() => onStartEditComment(item.comment!)} className="ms-btn is-sm" title="Yorumu düzenle">
                <Pencil /> Düzenle
              </button>
            )}
            <ConfirmButton icon={Trash2} confirmLabel="Emin misin? Sil" busy={busyAction === `comment-${item.comment.id}`} onConfirm={() => onDeleteComment(item.comment!)} title="Yorumu sil">
              Sil
            </ConfirmButton>
          </>
        )}
        {item.draft && (
          <>
            <button type="button" onClick={() => onEditDraft(item.draft!)} className="ms-btn is-sm">
              <Pencil /> Düzenle
            </button>
            <button type="button" onClick={() => onPublishDraft(item.draft!)} disabled={busyAction === `publish-${item.draft.id}`} className="ms-btn is-sm is-ok" title="Taslağı onayla ve yayınla">
              <Send /> {busyAction === `publish-${item.draft.id}` ? 'Yayınlanıyor…' : 'Yayınla'}
            </button>
            <ConfirmButton icon={Trash2} confirmLabel="Emin misin?" busy={busyAction === `deldraft-${item.draft.id}`} onConfirm={() => onDeleteDraft(item.draft!)} title="Taslağı her yerden sil">
              Sil
            </ConfirmButton>
          </>
        )}
      </div>
    </li>
  );
};

