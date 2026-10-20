import React, { useMemo, useState } from 'react';
import { Flag, MessageSquare, FileText, Bell, Eye, Check, Send, Pencil, Trash2, Inbox, CheckCircle2, ChevronDown, Smartphone, ExternalLink, UserPlus, Tag, Ban, Reply, Clock } from 'lucide-react';
import type { QuestionItem, AdminNotification } from '../../types';
import type { InboxReport, InboxComment } from '../../services/manageConsoleService';
import { EmptyState, Switch, ConfirmButton, timeLabel, Drawer, Field } from './consoleUi';
import { PageActions, StatRow, Tabs14, SearchField, Toolbar, DataTable, Pill, DetailNav, DetailLayout, FactList, Card14, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';
import { toast } from '../ui/Toast';
import { AdminMobileNotificationCard } from '../AdminMobileNotificationCard';
import { inAppPath } from '../../services/universalRedirectService';
import { useModerationMeta, ModerationActionDrawer, MetaPills, metaFacts, ReplyHistory, isSnoozed, isRejected, isMine, type ActionMode } from './moderationActions';

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
  /** Bildirimin hedefi (sitedeki yol); varsa satırda "Sitede gör" bağlantısı çıkar */
  url?: string;
  meta: string[];
  done?: boolean;
  unread?: boolean;
  report?: InboxReport;
  comment?: InboxComment;
  draft?: QuestionItem;
}

const KIND_META: Record<Kind, { icon: React.ElementType; tone: 'bad' | 'acc' | 'warn' | ''; label: string }> = {
  report: { icon: Flag, tone: 'bad', label: 'Hata bildirimi' },
  comment: { icon: MessageSquare, tone: 'acc', label: 'Yorum' },
  draft: { icon: FileText, tone: 'warn', label: 'Taslak' },
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
  const [view, setView] = useState<'open' | 'mine' | 'snoozed'>('open');
  const { meta, act } = useModerationMeta();
  const [actMode, setActMode] = useState<ActionMode | null>(null);
  const [actIds, setActIds] = useState<string[]>([]);
  const [actKind, setActKind] = useState('report');
  const openAction = (mode: ActionMode, ids: string[], kind: string) => { setActIds(ids); setActKind(kind); setActMode(mode); };
  /** Yan kayıt kimliği: bildirim ve yorumun kendi kimliği */
  const metaId = (i: QueueItem) => i.report?.id || i.comment?.id || '';

  const isDone = (r: InboxReport) => resolvedIds.has(r.id) || (r.status || 'pending') !== 'pending' || isRejected(meta[r.id]);

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
        // Etiketler ("Tıbbi Terim: x", "Ders · Adım 3") soru kimliği değildir; veri ekranına götürülmez.
        questionId: n.questionId && !/[:·\s]/.test(n.questionId) ? n.questionId : undefined,
        url: inAppPath(n.url) || undefined,
        meta: [n.author ? `Kaynak: ${n.author}` : ''].filter(Boolean) as string[],
        unread: !n.isRead,
      });
    }
    return out.sort((a, b) => (b.at || '').localeCompare(a.at || ''));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [reports, comments, drafts, notifications, resolvedIds, meta]);

  const q = query.trim().toLocaleLowerCase('tr-TR');
  const inView = (i: QueueItem) => {
    const m = meta[metaId(i)];
    if (view === 'mine') return isMine(m);
    if (view === 'snoozed') return isSnoozed(m);
    return !isSnoozed(m);
  };
  const base = all.filter((i) => inView(i) && (showResolved || !i.done) && (!q || [i.title, i.text, ...i.meta, meta[metaId(i)]?.assignee, ...(meta[metaId(i)]?.tags || [])].join(' ').toLocaleLowerCase('tr-TR').includes(q)));
  const count = (k: Kind) => base.filter((i) => i.kind === k).length;
  const visible = filter === 'all' ? base : base.filter((i) => i.kind === filter);
  const shown = visible.slice(0, limit);

  const pendingReports = reports.filter((r) => !isDone(r)).length;
  const resolvedCount = reports.length - pendingReports;

  const [editingReport, setEditingReport] = useState<{ report: InboxReport; reason: string; details: string } | null>(null);
  const [editingComment, setEditingComment] = useState<{ comment: InboxComment; text: string } | null>(null);
  const [openKey, setOpenKey] = useState<string | null>(null);
  const selection = useSelection<string>();
  const [bulkBusy, setBulkBusy] = useState(false);
  const openItem = all.find((i) => i.key === openKey) || null;
  const picked = () => all.filter((i) => selection.has(i.key));

  /** Seçili ögelerde tek öge işleyicisini sırayla çalıştırır */
  const runBulk = async (pick: (i: QueueItem) => boolean, fn: (i: QueueItem) => unknown) => {
    const items = picked().filter(pick);
    if (!items.length) { toast.error('Seçimde bu işleme uygun öge yok.'); return; }
    setBulkBusy(true);
    let ok = 0;
    let bad = 0;
    for (const it of items) {
      try { await fn(it); ok++; } catch { bad++; }
    }
    setBulkBusy(false);
    if (bad) toast.error(`${ok} başarılı, ${bad} hata.`);
    else { toast.success(`${ok} başarılı, 0 hata.`); selection.clear(); }
  };

  const cols: Col<QueueItem>[] = [
    {
      key: 'title', label: 'Başlık', main: true, render: (i) => (
        <>{i.unread && <span className="sr-only">Yeni: </span>}{i.title}</>
      ),
    },
    {
      key: 'kind', label: 'Tür', render: (i) => (
        <span className="inline-flex gap-1 flex-wrap">
          <Pill tone={KIND_META[i.kind].tone}>{KIND_META[i.kind].label}</Pill>
          {i.done && <Pill tone="ok">Çözüldü</Pill>}
          {i.unread && <Pill tone="acc">Yeni</Pill>}
        </span>
      ),
    },
    { key: 'from', label: 'Gönderen', render: (i) => <span className="clip">{i.sender || 'Bilinmiyor'}</span> },
    { key: 'mm', label: 'Atama ve etiket', render: (i) => (metaId(i) ? <MetaPills m={meta[metaId(i)]} /> : <span className="text-ink-3">—</span>), width: '18%' },
    { key: 'ctx', label: 'Bağlam', muted: true, render: (i) => <span className="clip">{i.meta[0] || '—'}</span>, width: '22%' },
    { key: 'at', label: 'Zaman', muted: true, render: (i) => timeLabel(i.at) || '—' },
  ];

  const deleteActions = [
    onDeleteReport && { label: 'Bildirimleri sil', test: (i: QueueItem) => !!i.report, fn: (i: QueueItem) => onDeleteReport(i.report!) },
    { label: 'Yorumları sil', test: (i: QueueItem) => !!i.comment, fn: (i: QueueItem) => onDeleteComment(i.comment!) },
    { label: 'Taslakları sil', test: (i: QueueItem) => !!i.draft, fn: (i: QueueItem) => onDeleteDraft(i.draft!) },
  ].filter(Boolean) as { label: string; test: (i: QueueItem) => boolean; fn: (i: QueueItem) => unknown }[];
  const sel = picked();

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <PageActions>
        {resolvedCount > 0 && <Switch checked={showResolved} onChange={setShowResolved} label={`Çözülenleri göster (${resolvedCount})`} />}
        <button
          type="button"
          onClick={() => setShowNotificationCard(!showNotificationCard)}
          aria-pressed={showNotificationCard}
          className={`m14-btn ${showNotificationCard ? 'primary' : ''}`}
          title="Telefonda (nofrostlife.com.tr) yönetici bildirim ayarları"
        >
          <Smartphone aria-hidden="true" />
          <span>{showNotificationCard ? 'Bildirim ayarlarını kapat' : 'Telefon bildirimleri'}</span>
        </button>
      </PageActions>

      {showNotificationCard && (
        <div className="animate-fade-in my-1">
          <AdminMobileNotificationCard onClose={() => setShowNotificationCard(false)} />
        </div>
      )}

      <StatRow
        stats={[
          { label: 'Bekleyen bildirim', value: pendingReports, tone: pendingReports ? 'bad' : 'ok', onClick: () => setFilter('report') },
          { label: 'Taslak', value: drafts.length, tone: drafts.length ? 'warn' : undefined, onClick: () => setFilter('draft') },
          { label: 'Yorum', value: comments.length, onClick: () => setFilter('comment') },
          { label: 'Okunmamış uyarı', value: notifications.filter((n) => !n.isRead).length, onClick: () => setFilter('notice') },
        ]}
      />

      <Toolbar>
        <Tabs14
          label="Tür"
          value={filter}
          onChange={(v) => { setFilter(v); setLimit(PAGE); }}
          options={[
            { id: 'all', label: 'Tümü', n: base.length },
            { id: 'report', label: 'Bildirim', n: count('report') },
            { id: 'comment', label: 'Yorum', n: count('comment') },
            { id: 'draft', label: 'Taslak', n: count('draft') },
            { id: 'notice', label: 'Uyarı', n: count('notice') },
          ]}
        />
        <SearchField value={query} onChange={(v) => { setQuery(v); setLimit(PAGE); }} placeholder="Bildirim, yorum, taslak, kişi" label="Kuyrukta ara" />
        <label className="ms-select-chip !h-9">
          <span className="sr-only">Görünüm</span>
          <select value={view} onChange={(e) => { setView(e.target.value as typeof view); setLimit(PAGE); }}>
            <option value="open">Açık iş</option>
            <option value="mine">Bana atanan</option>
            <option value="snoozed">Ertelenenler</option>
          </select>
        </label>
      </Toolbar>

      <BulkBar
        count={selection.count}
        noun="öge"
        busy={bulkBusy || !!busyAction}
        onClear={selection.clear}
        actions={[
          ...(sel.some((i) => i.report && !i.done) ? [{ label: 'Çözüldü', kind: 'main' as const, run: () => runBulk((i) => !!i.report && !i.done, (i) => onResolve(i.report!)) }] : []),
          ...(sel.some((i) => metaId(i)) ? [
            { label: 'Kişiye ata', run: () => openAction('assign', sel.map(metaId).filter(Boolean), 'mixed') },
            { label: 'Etiket ekle', run: () => openAction('tags', sel.map(metaId).filter(Boolean), 'mixed') },
            { label: 'Ertele', run: () => openAction('snooze', sel.map(metaId).filter(Boolean), 'mixed') },
            { label: 'Kişiye yanıt', run: () => openAction('reply', sel.map(metaId).filter(Boolean), 'mixed') },
          ] : []),
          ...(sel.some((i) => i.report && !i.done) ? [{ label: 'Reddet', kind: 'danger' as const, run: () => openAction('reject', sel.filter((i) => i.report && !i.done).map((i) => i.report!.id), 'report') }] : []),
          ...(sel.some((i) => i.draft) ? [{ label: 'Taslakları yayınla', run: () => runBulk((i) => !!i.draft, (i) => onPublishDraft(i.draft!)) }] : []),
          ...deleteActions.filter((a) => sel.some(a.test)).map((a) => ({ label: a.label, kind: 'danger' as const, confirm: `${sel.filter(a.test).length} öge kalıcı silinsin`, run: () => runBulk(a.test, a.fn) })),
        ]}
      />

      {loading && all.length === 0 ? (
        <div className="flex flex-col gap-2" role="status" aria-label="Kuyruk yükleniyor">
          {[0, 1, 2].map((i) => <div key={i} className="h-14 rounded-xl bg-field ms-shimmer" />)}
        </div>
      ) : (
        <DataTable
          rows={shown}
          cols={cols}
          rowKey={(i) => i.key}
          onOpen={(i) => setOpenKey(i.key)}
          selection={selection}
          activeKey={openKey}
          minWidth={900}
          empty={
            q ? (
              <EmptyState icon={Inbox} title="Aramaya uyan kayıt yok">“{query}” için kuyrukta bir şey bulunamadı.</EmptyState>
            ) : (
              <EmptyState icon={CheckCircle2} title="Kuyruk boş">
                {filter === 'all' ? 'Bekleyen bildirim, yorum, taslak ya da uyarı yok.' : `Bu türde bekleyen ${KIND_META[filter].label.toLocaleLowerCase('tr-TR')} yok.`}
              </EmptyState>
            )
          }
        />
      )}
      {visible.length > limit && (
        <button type="button" onClick={() => setLimit((n) => n + PAGE)} className="m14-btn self-center">
          <ChevronDown aria-hidden="true" /> {visible.length - limit} kayıt daha
        </button>
      )}

      <Drawer
        open={!!openItem && !editingReport && !editingComment && !actMode}
        onClose={() => setOpenKey(null)}
        title={openItem?.title || 'Öge'}
        label="Gelen kutusu ögesi"
        wide
        head={<DetailNav list={visible} current={openItem} same={(a, b) => a.key === b.key} onGo={(i) => setOpenKey(i.key)} />}
        foot={openItem && (
          <ItemActions
            item={openItem}
            busyAction={busyAction}
            onReview={onReview}
            onResolve={onResolve}
            onStartEditReport={onEditReport ? (r) => setEditingReport({ report: r, reason: r.reason || '', details: r.details || '' }) : undefined}
            onDeleteReport={onDeleteReport}
            onStartEditComment={onEditComment ? (c) => setEditingComment({ comment: c, text: c.text || '' }) : undefined}
            onDeleteComment={onDeleteComment}
            onEditDraft={onEditDraft}
            onPublishDraft={onPublishDraft}
            onDeleteDraft={onDeleteDraft}
            onAction={metaId(openItem) ? (mode) => openAction(mode, [metaId(openItem)], openItem.report ? 'report' : 'comment') : undefined}
            rejected={isRejected(meta[metaId(openItem)])}
          />
        )}
      >
        {openItem && (
          <DetailLayout
            main={
              <Card14 title="İçerik">
                <p className="m-0 text-base text-ink leading-relaxed whitespace-pre-wrap [overflow-wrap:anywhere]">{openItem.text || openItem.title}</p>
              </Card14>
            }
            side={
              <Card14 title="Bilgi">
                <FactList
                  items={[
                    { k: 'Tür', v: <Pill tone={KIND_META[openItem.kind].tone}>{KIND_META[openItem.kind].label}</Pill> },
                    { k: 'Gönderen', v: openItem.sender || 'Bilinmiyor' },
                    { k: 'Neden', v: openItem.reason || '—' },
                    { k: 'Zaman', v: openItem.at ? new Date(openItem.at).toLocaleString('tr-TR', { dateStyle: 'medium', timeStyle: 'short' }) : '—' },
                    ...(openItem.done ? [{ k: 'Durum', v: <Pill tone="ok"><Check aria-hidden="true" /> Çözüldü</Pill> }] : []),
                    ...openItem.meta.map((m) => ({ k: 'Not', v: m })),
                    ...metaFacts(meta[metaId(openItem)]),
                    ...(openItem.questionId && onNavigateToData
                      ? [{
                          k: 'Soru',
                          v: (
                            <button type="button" onClick={() => onNavigateToData(openItem.questionId!)} className="m14-btn ghost" title="Bu soruyu veritabanında bul ve düzenle">
                              {openItem.questionId.startsWith('past-') ? 'Çıkmış soru' : 'Soru'} #{openItem.questionId.replace(/^q-|^past-/, '')} <ExternalLink aria-hidden="true" />
                            </button>
                          ),
                        }]
                      : []),
                    ...(openItem.url
                      ? [{ k: 'Bağlantı', v: <a href={openItem.url} target="_blank" rel="noopener" title="Bildirilen yeri sitede yeni sekmede aç">Sitede gör <ExternalLink className="inline w-3 h-3" aria-hidden="true" /></a> }]
                      : []),
                  ]}
                />
              </Card14>
            }
          />
        )}
        {openItem && metaId(openItem) && <div className="mt-3"><ReplyHistory m={meta[metaId(openItem)]} /></div>}
      </Drawer>

      <ModerationActionDrawer
        mode={actMode}
        ids={actIds}
        kind={actKind}
        current={actIds.length === 1 ? meta[actIds[0]] : undefined}
        onClose={() => setActMode(null)}
        act={act}
      />

      <Drawer
        open={!!editingReport}
        onClose={() => setEditingReport(null)}
        title="Hata bildirimini düzenle"
        head={editingReport && <span className="font-mono text-xs text-ink-3">#{editingReport.report.id}</span>}
        foot={editingReport && (
          <>
            <button type="button" onClick={() => setEditingReport(null)} className="m14-btn ghost">Vazgeç</button>
            <button
              type="button"
              disabled={!editingReport.reason.trim()}
              onClick={async () => {
                if (onEditReport) await onEditReport(editingReport.report, { reason: editingReport.reason.trim(), details: editingReport.details.trim() });
                setEditingReport(null);
              }}
              className="m14-btn primary"
            >
              Değişiklikleri kaydet
            </button>
          </>
        )}
      >
        {editingReport && (
          <Card14>
            <div className="flex flex-col gap-3">
              <Field label="Bildirim konusu">
                <input type="text" value={editingReport.reason} onChange={(e) => setEditingReport({ ...editingReport, reason: e.target.value })} className="ms-input" placeholder="Örn: Yanlış şık / Doğru cevap C olmalı" />
              </Field>
              <Field label="Ayrıntılı açıklama">
                <textarea value={editingReport.details} onChange={(e) => setEditingReport({ ...editingReport, details: e.target.value })} rows={5} className="ms-input" placeholder="Öğrencinin bildirdiği hata ayrıntısı" />
              </Field>
            </div>
          </Card14>
        )}
      </Drawer>

      <Drawer
        open={!!editingComment}
        onClose={() => setEditingComment(null)}
        title="Öğrenci yorumunu düzenle"
        head={editingComment && <span className="font-mono text-xs text-ink-3">#{editingComment.comment.id}</span>}
        foot={editingComment && (
          <>
            <button type="button" onClick={() => setEditingComment(null)} className="m14-btn ghost">Vazgeç</button>
            <button
              type="button"
              disabled={!editingComment.text.trim()}
              onClick={async () => {
                if (onEditComment) await onEditComment(editingComment.comment, editingComment.text.trim());
                setEditingComment(null);
              }}
              className="m14-btn primary"
            >
              Değişiklikleri kaydet
            </button>
          </>
        )}
      >
        {editingComment && (
          <Card14>
            <Field label="Yorum metni">
              <textarea value={editingComment.text} onChange={(e) => setEditingComment({ ...editingComment, text: e.target.value })} rows={6} className="ms-input" placeholder="Yorum veya çözüm önerisi" />
            </Field>
          </Card14>
        )}
      </Drawer>
    </div>
  );
};

interface ItemActionsProps {
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
  onAction?: (mode: ActionMode) => void;
  rejected?: boolean;
}

/** Ayrıntı alanının alt eylem şeridi: türe göre */
const ItemActions: React.FC<ItemActionsProps> = ({
  item, busyAction, onReview, onResolve, onStartEditReport, onDeleteReport, onStartEditComment, onDeleteComment, onEditDraft, onPublishDraft, onDeleteDraft, onAction, rejected,
}) => (
  <>
    {onAction && (
      <>
        <button type="button" onClick={() => onAction('assign')} className="m14-btn ghost"><UserPlus aria-hidden="true" /> Kişiye ata</button>
        <button type="button" onClick={() => onAction('tags')} className="m14-btn ghost"><Tag aria-hidden="true" /> Etiket</button>
        <button type="button" onClick={() => onAction('snooze')} className="m14-btn ghost"><Clock aria-hidden="true" /> Ertele</button>
        <button type="button" onClick={() => onAction('reply')} className="m14-btn ghost"><Reply aria-hidden="true" /> Kişiye yanıt</button>
        {item.report && (!item.done || rejected) && (
          <button type="button" onClick={() => onAction('reject')} className="m14-btn ghost"><Ban aria-hidden="true" /> {rejected ? 'Ret' : 'Reddet'}</button>
        )}
      </>
    )}
    {item.report && (
      <>
        {onDeleteReport && (
          <ConfirmButton icon={Trash2} className="m14-btn danger" confirmLabel="Kalıcı silinsin mi?" busy={busyAction === `delreport-${item.report.id}`} onConfirm={() => onDeleteReport(item.report!)} title="Hata bildirimini tüm veritabanından kalıcı olarak sil">
            Sil
          </ConfirmButton>
        )}
        {onStartEditReport && (
          <button type="button" onClick={() => onStartEditReport(item.report!)} className="m14-btn"><Pencil aria-hidden="true" /> Düzenle</button>
        )}
        <button type="button" onClick={() => onReview(item.report!)} className="m14-btn" title="Soruyu moderasyonda incele"><Eye aria-hidden="true" /> İncele</button>
        {!item.done && (
          <button type="button" onClick={() => onResolve(item.report!)} disabled={busyAction === `resolve-${item.report.id}`} className="m14-btn primary"><Check aria-hidden="true" /> Çözüldü</button>
        )}
      </>
    )}
    {item.comment && (
      <>
        <ConfirmButton icon={Trash2} className="m14-btn danger" confirmLabel="Emin misin? Sil" busy={busyAction === `comment-${item.comment.id}`} onConfirm={() => onDeleteComment(item.comment!)} title="Yorumu sil">
          Sil
        </ConfirmButton>
        {onStartEditComment && (
          <button type="button" onClick={() => onStartEditComment(item.comment!)} className="m14-btn primary"><Pencil aria-hidden="true" /> Düzenle</button>
        )}
      </>
    )}
    {item.draft && (
      <>
        <ConfirmButton icon={Trash2} className="m14-btn danger" confirmLabel="Emin misin?" busy={busyAction === `deldraft-${item.draft.id}`} onConfirm={() => onDeleteDraft(item.draft!)} title="Taslağı her yerden sil">
          Sil
        </ConfirmButton>
        <button type="button" onClick={() => onEditDraft(item.draft!)} className="m14-btn"><Pencil aria-hidden="true" /> Düzenle</button>
        <button type="button" onClick={() => onPublishDraft(item.draft!)} disabled={busyAction === `publish-${item.draft.id}`} className="m14-btn primary" title="Taslağı onayla ve yayınla">
          <Send aria-hidden="true" /> {busyAction === `publish-${item.draft.id}` ? 'Yayınlanıyor…' : 'Yayınla'}
        </button>
      </>
    )}
  </>
);
