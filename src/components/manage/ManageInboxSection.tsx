import React, { useMemo, useState } from 'react';
import { Flag, MessageSquare, FileText, Bell, Eye, Check, Send, Pencil, Trash2, Inbox, CheckCircle2, ChevronDown } from 'lucide-react';
import type { QuestionItem, AdminNotification } from '../../types';
import type { InboxReport, InboxComment } from '../../services/manageConsoleService';
import { Panel, EmptyState, SearchBox, ChipBar, Switch, ConfirmButton, dayLabel, timeLabel } from './consoleUi';

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
  onDeleteComment: (c: InboxComment) => void;
  onEditDraft: (d: QuestionItem) => void;
  onPublishDraft: (d: QuestionItem) => void;
  onDeleteDraft: (d: QuestionItem) => void;
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
  onDeleteComment,
  onEditDraft,
  onPublishDraft,
  onDeleteDraft,
}) => {
  const [filter, setFilter] = useState<Filter>('all');
  const [query, setQuery] = useState('');
  const [showResolved, setShowResolved] = useState(false);
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
        meta: [r.questionTopic || r.questionId, r.reportedBy || 'Anonim'].filter(Boolean) as string[],
        done: isDone(r),
        report: r,
      });
    }
    for (const c of comments) {
      out.push({ key: `c-${c.id}`, kind: 'comment', at: c.createdAt, title: c.text, meta: [c.author, c.questionTopic || c.questionId].filter(Boolean) as string[], comment: c });
    }
    for (const d of drafts) {
      const num = d.isUnassignedNumber ? 'Numarasız' : d.questionNumber ? `S.${d.questionNumber}` : 'Numarasız';
      out.push({
        key: `d-${d.id}`,
        kind: 'draft',
        at: d.updatedAt || d.createdAt,
        title: d.topic || d.discipline || 'Konusuz taslak',
        text: d.reconstruction?.stem || d.stem || d.fragments?.[0]?.text,
        meta: [num, d.discipline, `${d.fragments?.length || 0} parça`, `${d.options?.length || 0} şık`].filter(Boolean) as string[],
        draft: d,
      });
    }
    for (const n of notifications) {
      out.push({ key: `n-${n.id}`, kind: 'notice', at: n.timestamp, title: n.title, text: n.message, meta: [n.author].filter(Boolean), unread: !n.isRead });
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
    rows.push(<QueueRow key={item.key} item={item} busyAction={busyAction} {...{ onReview, onResolve, onDeleteComment, onEditDraft, onPublishDraft, onDeleteDraft }} />);
  }

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <div className="flex flex-col md:flex-row md:items-center gap-2">
        <SearchBox value={query} onChange={(v) => { setQuery(v); setLimit(PAGE); }} placeholder="Kuyrukta ara: bildirim, yorum, taslak, kişi" className="flex-1" />
        {resolvedCount > 0 && <Switch checked={showResolved} onChange={setShowResolved} label={`Çözülenleri göster (${resolvedCount})`} />}
      </div>
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
          <button type="button" onClick={() => setLimit((n) => n + PAGE)} className="w-full h-11 border-t border-line-soft text-[13px] font-semibold text-accent inline-flex items-center justify-center gap-1 cursor-pointer hover:bg-canvas rounded-b-2xl">
            <ChevronDown className="w-4 h-4" /> {visible.length - limit} kayıt daha
          </button>
        )}
      </Panel>
    </div>
  );
};

const QueueRow: React.FC<
  { item: QueueItem; busyAction: string | null } & Pick<Props, 'onReview' | 'onResolve' | 'onDeleteComment' | 'onEditDraft' | 'onPublishDraft' | 'onDeleteDraft'>
> = ({ item, busyAction, onReview, onResolve, onDeleteComment, onEditDraft, onPublishDraft, onDeleteDraft }) => {
  const m = KIND_META[item.kind];
  const Icon = m.icon;
  const time = timeLabel(item.at);
  return (
    <li className={`ms-row ${item.done ? 'is-done' : ''}`}>
      <span className={`ms-ricon ${m.tone}`} title={m.label}>
        <Icon aria-hidden="true" />
      </span>
      <div className="ms-row-main">
        <span className={`ms-row-title ${item.kind === 'comment' ? 'font-medium' : ''}`}>
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
            <button type="button" onClick={() => onReview(item.report!)} className="ms-btn is-sm is-tonal">
              <Eye /> İncele
            </button>
            {!item.done && (
              <button type="button" onClick={() => onResolve(item.report!)} disabled={busyAction === `resolve-${item.report.id}`} className="ms-btn is-sm" title="Bildirimi kapat">
                <Check /> Çözüldü
              </button>
            )}
          </>
        )}
        {item.comment && (
          <ConfirmButton icon={Trash2} confirmLabel="Emin misin? Sil" busy={busyAction === `comment-${item.comment.id}`} onConfirm={() => onDeleteComment(item.comment!)} title="Yorumu sil">
            Sil
          </ConfirmButton>
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
