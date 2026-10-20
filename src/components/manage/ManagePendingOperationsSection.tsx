import React, { useEffect, useState, useMemo } from 'react';
import { confirmText } from '../ui/ConfirmDialog';
import {
  Sparkles,
  AlertTriangle,
  RotateCcw,
  Play,
  Pause,
  RefreshCw,
  Trash2,
  ShieldCheck,
  ExternalLink,
  MapPin,
  Clock,
  UserPlus,
  Tag,
  Reply,
  ShieldAlert,
} from 'lucide-react';
import { Drawer } from './consoleUi';
import { PageActions, StatRow, Tabs14, SearchField, Toolbar, DataTable, Pill, DetailNav, DetailLayout, FactList, Card14, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';
import {
  AutoRepairItemClient,
  AutoRepairStats,
  loadAutoRepairItems,
  loadAutoRepairStats,
  runNextAutoRepair,
  runAllAutoRepair,
  rollbackAutoRepair,
  retryAutoRepair,
  toggleAutoRepairWorker,
  deleteAutoRepairItem,
  clearProcessedAutoRepair,
  bulkDeleteAutoRepair,
} from '../../services/manageConsoleService';
import { toast } from '../ui/Toast';
import {
  buildUniversalReportUrl,
  getUniversalLocationBreadcrumb,
} from '../../services/universalRedirectService';
import { guardedInterval } from '../../services/net';
import { realtimeEventService } from '../../services/realtimeEvents';
import { useModerationMeta, ModerationActionDrawer, MetaPills, metaFacts, ReplyHistory, isSnoozed, isMine, type ActionMode } from './moderationActions';

export const ManagePendingOperationsSection: React.FC<{ onOpenModeration?: (id: string) => void }> = ({ onOpenModeration }) => {
  const { meta, act } = useModerationMeta();
  const [actMode, setActMode] = useState<ActionMode | null>(null);
  const [actIds, setActIds] = useState<string[]>([]);
  const openAction = (mode: ActionMode, ids: string[]) => { setActIds(ids); setActMode(mode); };
  /** Moderasyona aktar: kayıt işaretlenir, eşleşen bildirim varsa moderasyon ekranında açılır */
  const escalate = async (ids: string[]) => {
    if (!ids.length) return;
    const ok = await act(ids, 'escalate', { kind: 'repair' });
    if (ok && ids.length === 1 && onOpenModeration) onOpenModeration(ids[0]);
  };
  const [items, setItems] = useState<AutoRepairItemClient[]>([]);
  const [stats, setStats] = useState<AutoRepairStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionBusy, setActionBusy] = useState(false);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const selection = useSelection<string>();
  const selectedIds = [...selection.sel];

  // Filtreler
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterSource, setFilterSource] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const loadData = async () => {
    try {
      const [itemList, statData] = await Promise.all([
        loadAutoRepairItems(),
        loadAutoRepairStats(),
      ]);
      setItems(itemList);
      setStats(statData);
    } catch (e: any) {
      toast.error('Veriler yüklenemedi', e?.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();

    // 1. SSE (Server-Sent Events) Kalıcı Akış Dinleyicisi
    // Kuyrukta işlem işlendiğinde, hata veya onay geldiğinde 0ms anında yenile
    const unsub = realtimeEventService.onAutoRepairUpdate(() => {
      loadData();
    });

    // 2. Güvenlik ve yedek yoklama: 2.5 saniyeden 30 saniyeye çekildi (SSE ile %92 ağ tasarrufu)
    const stopInterval = guardedInterval(loadData, 30000);

    return () => {
      unsub();
      stopInterval();
    };
  }, []);

  const handleRunNext = async () => {
    setActionBusy(true);
    try {
      const res = await runNextAutoRepair();
      if (res.success) {
        toast.success('İşlem çalıştırıldı', res.message || 'Sıradaki işlem incelendi.');
        await loadData();
      } else {
        toast.error('Çalıştırılamadı', res.error);
      }
    } catch (e: any) {
      toast.error('Hata', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  const handleRunAll = async () => {
    setActionBusy(true);
    try {
      const res = await runAllAutoRepair();
      if (res.success) {
        toast.success('Toplu inceleme başlatıldı', res.message);
        await loadData();
      } else {
        toast.error('Başlatılamadı', res.error);
      }
    } catch (e: any) {
      toast.error('Hata', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  const handleRollback = async (id: string) => {
    if (!(await confirmText('Bu otomatik düzeltmeyi geri alıp orijinal haline döndürmek istediğine emin misin?'))) return;
    setActionBusy(true);
    try {
      const res = await rollbackAutoRepair(id);
      if (res.success) {
        toast.success('Geri Alındı', res.message);
        await loadData();
      } else {
        toast.error('Geri alınamadı', res.error);
      }
    } catch (e: any) {
      toast.error('Geri alma hatası', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  const handleRetry = async (id: string) => {
    setActionBusy(true);
    try {
      const res = await retryAutoRepair(id);
      if (res.success) {
        toast.success('Yeniden incelendi', 'İşlem Gemini tarafından tekrar işlendi.');
        await loadData();
      } else {
        toast.error('İşlenemedi', res.error);
      }
    } catch (e: any) {
      toast.error('Hata', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  const handleToggleWorker = async () => {
    if (!stats) return;
    setActionBusy(true);
    try {
      const nextPaused = stats.isWorkerActive; // aktifse duraklat
      await toggleAutoRepairWorker(nextPaused);
      toast.info(nextPaused ? 'Otomasyon Duraklatıldı' : 'Otomasyon Devam Ediyor', nextPaused ? 'Arka plan kuyruk işleyicisi beklemeye alındı.' : 'Kuyruk 20 saniyelik aralıklarla otomatik işlenecek.');
      await loadData();
    } catch (e: any) {
      toast.error('Ayar değiştirilemedi', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!(await confirmText("Bu kaydı kuyruktan kalıcı olarak silmek ve ID'sini banlamak istiyor musunuz?\n\nBu ID kalıcı olarak banlanacağı için bir daha asla kuyruğa geri dönemez."))) return;
    try {
      const ok = await deleteAutoRepairItem(id);
      if (ok) {
        toast.success('Silindi & Banlandı', "Hata bildirimi silindi ve ID'si kalıcı olarak banlandı. Tekrar geri gelmeyecek.");
        setItems((prev) => prev.filter((x) => x.id !== id));
        if (selection.has(id)) selection.toggle(id);
        if (expandedId === id) setExpandedId(null);
        await loadData();
      }
    } catch (e: any) {
      toast.error('Silinemedi', e?.message);
    }
  };

  const handleClearProcessed = async () => {
    const processedCount = items.filter(
      (x) => x.status === 'applied' || x.status === 'no_change' || x.status === 'rolled_back'
    ).length;
    if (processedCount === 0) {
      toast.info('İşlem Yapılmış Kayıt Yok', 'Kuyrukta temizlenecek tamamlanmış işlem bulunamadı.');
      return;
    }
    if (!(await confirmText(`İşlem yapılmış ${processedCount} adet hata bildirimini kuyruktan topluca temizlemek ve ID'lerini kalıcı olarak banlamak istiyor musunuz?\n\nBu sayede bu bildirimler bir daha asla kuyruğa geri dönemez.`))) return;

    setActionBusy(true);
    try {
      const res = await clearProcessedAutoRepair();
      if (res.success) {
        toast.success('Temizlendi & Banlandı', res.message || `${res.clearedCount} adet işlem yapılan kayıt temizlendi.`);
        await loadData();
      } else {
        toast.error('Temizleme başarısız', res.message);
      }
    } catch (e: any) {
      toast.error('Hata', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  // BulkBar iki dokunuşla onay aldığı için ayrıca soru sorulmaz
  const handleBulkDelete = async () => {
    if (selectedIds.length === 0) return;

    setActionBusy(true);
    try {
      const res = await bulkDeleteAutoRepair(selectedIds);
      if (res.success) {
        toast.success('Toplu Silindi', res.message || `${selectedIds.length} kayıt silindi ve banlandı.`);
        selection.clear();
        await loadData();
      } else {
        toast.error('Toplu silme başarısız', res.message);
      }
    } catch (e: any) {
      toast.error('Hata', e?.message);
    } finally {
      setActionBusy(false);
    }
  };

  // Filtreleme
  const filteredItems = useMemo(() => {
    return items.filter((item) => {
      const m = meta[item.id];
      if (filterStatus === 'snoozed') { if (!isSnoozed(m)) return false; }
      else if (filterStatus === 'mine') { if (!isMine(m)) return false; }
      else if (filterStatus !== 'all' && (item.status !== filterStatus || isSnoozed(m))) return false;
      if (filterSource !== 'all' && item.source !== filterSource) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const text = [
          item.targetId,
          item.userReport.reason,
          item.userReport.details,
          item.userReport.reportedBy,
          item.aiAnalysis?.changesSummary,
          item.aiAnalysis?.medicalReasoning,
          item.subTarget?.label,
          item.subTarget?.location,
          m?.assignee,
          ...(m?.tags || []),
        ].filter(Boolean).join(' ').toLowerCase();
        if (!text.includes(q)) return false;
      }
      return true;
    });
  }, [items, filterStatus, filterSource, searchQuery, meta]);

  const SOURCE_LABEL: Record<string, string> = {
    past_question: 'Çıkmış soru',
    practice_question: 'Örnek soru',
    interactive_deck: 'Öğrenme destesi',
  };
  const getSourceBadge = (source: string, subTarget?: any) => (
    <Pill tone={source === 'interactive_deck' ? 'ok' : source in SOURCE_LABEL ? 'acc' : ''}>
      {SOURCE_LABEL[source] || 'Ders notu / özet'}{source === 'interactive_deck' && subTarget?.slideNumber ? ` · Slayt ${subTarget.slideNumber}` : ''}
    </Pill>
  );

  const STATUS_META: Record<string, { label: string; tone: 'ok' | 'warn' | 'bad' | 'acc' | '' }> = {
    pending: { label: 'Kuyrukta', tone: 'warn' },
    processing: { label: 'İnceleniyor', tone: 'acc' },
    applied: { label: 'Uygulandı', tone: 'ok' },
    no_change: { label: 'Değişiklik gerekmedi', tone: '' },
    rolled_back: { label: 'Geri alındı', tone: 'acc' },
    error: { label: 'Hata', tone: 'bad' },
  };
  const getStatusBadge = (status: string) => {
    const m = STATUS_META[status];
    return m ? <Pill tone={m.tone}>{m.label}</Pill> : null;
  };

  const getTargetNavigation = (item: AutoRepairItemClient) => {
    const breadcrumb = getUniversalLocationBreadcrumb({
      type: item.source as any,
      targetId: item.targetId,
      subTarget: item.subTarget,
      highlightText: item.subTarget?.label || undefined,
    });

    const url = buildUniversalReportUrl({
      type: item.source as any,
      targetId: item.targetId,
      subTarget: item.subTarget,
      highlightText: item.subTarget?.label || undefined,
    });

    let label = 'Konuma Git';
    if (item.source === 'interactive_deck') {
      label = item.subTarget?.slideNumber ? `Slayt #${item.subTarget.slideNumber}'e Git` : 'Derse Git';
    } else if (item.source === 'past_question') {
      label = 'Çıkmış Soruya Git';
    } else if (item.source === 'practice_question') {
      label = 'Soru Havuzuna Git';
    }

    return {
      url,
      label,
      badgeLabel: breadcrumb.badge,
      description: breadcrumb.fullLocation,
      category: breadcrumb.category,
    };
  };

  const countOf = (st: string) => items.filter((x) => x.status === st).length;
  const openItem = items.find((x) => x.id === expandedId) || null;

  /** Seçili kayıtlarda tek kayıt API'sini sırayla çalıştırır */
  const runBulk = async (pick: (x: AutoRepairItemClient) => boolean, fn: (id: string) => Promise<{ success: boolean }>) => {
    const targets = items.filter((x) => selection.has(x.id) && pick(x));
    if (!targets.length) { toast.info('Uygun kayıt yok', 'Seçimde bu işleme uygun kayıt bulunmuyor.'); return; }
    setActionBusy(true);
    let ok = 0;
    let bad = 0;
    for (const t of targets) {
      try { const r = await fn(t.id); if (r.success) ok++; else bad++; } catch { bad++; }
    }
    setActionBusy(false);
    if (bad) toast.error('Toplu işlem', `${ok} başarılı, ${bad} hata.`);
    else { toast.success('Toplu işlem', `${ok} başarılı, 0 hata.`); selection.clear(); }
    await loadData();
  };

  const reviewNow = async (id: string) => {
    setActionBusy(true);
    try {
      const res = await retryAutoRepair(id);
      if (res.success) toast.success('İşlendi', 'Yapay zekâ incelemesi tamamlandı.');
      else toast.error('İşlenemedi', res.error);
      await loadData();
    } finally {
      setActionBusy(false);
    }
  };

  const cols: Col<AutoRepairItemClient>[] = [
    { key: 'r', label: 'İşlem', main: true, render: (x) => <>{x.userReport.reason}{x.userReport.details ? ` · ${x.userReport.details}` : ''}</> },
    { key: 's', label: 'Durum', render: (x) => getStatusBadge(x.status) },
    { key: 'k', label: 'Kaynak', render: (x) => getSourceBadge(x.source, x.subTarget) },
    { key: 'm', label: 'Atama ve etiket', render: (x) => <MetaPills m={meta[x.id]} />, width: '18%' },
    { key: 't', label: 'Hedef', mono: true, render: (x) => <span className="clip">#{x.targetId}</span>, width: '16%' },
    { key: 'z', label: 'Zaman', muted: true, render: (x) => new Date(x.userReport.reportedAt).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) },
  ];

  const snapshot = (snap: any, source: string, answerTone: string) =>
    source === 'interactive_deck' ? (
      <>
        <div className="font-semibold text-ink">{snap.title}</div>
        <div className="text-ink-2 text-sm mt-1 whitespace-pre-wrap">{snap.synthesisNarrative}</div>
      </>
    ) : (
      <>
        <div className="font-semibold text-ink whitespace-pre-wrap">{snap.stem || snap.questionText}</div>
        <div className={`${answerTone} font-semibold mt-1`}>Cevap: {snap.correctAnswer || snap.answer}</div>
        <div className="text-ink-2 text-sm mt-1 whitespace-pre-wrap">{snap.explanation}</div>
      </>
    );

  const renderDetail = (item: AutoRepairItemClient) => {
    const targetNav = getTargetNavigation(item);
    return (
      <DetailLayout
        main={
          <>
            <Card14 title="Kullanıcı bildirimi">
              <p className="m-0 text-base text-ink leading-relaxed whitespace-pre-wrap [overflow-wrap:anywhere]">
                <b>{item.userReport.reason}</b>
                {item.userReport.details ? <><br />{item.userReport.details}</> : <span className="text-warn text-sm"> (Kullanıcı açıklama girmedi; AI derin denetim yaptı)</span>}
              </p>
            </Card14>

            {item.beforeSnapshot && item.afterSnapshot && (
              <Card14 title="Değişiklik önizlemesi">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                  <div className="rounded-lg border border-line p-3 min-w-0 [overflow-wrap:anywhere]">
                    <div className="text-xs font-semibold text-bad-text mb-1">Önce</div>
                    {snapshot(item.beforeSnapshot, item.source, 'text-bad-text')}
                  </div>
                  <div className="rounded-lg border border-line p-3 min-w-0 [overflow-wrap:anywhere]">
                    <div className="text-xs font-semibold text-ok mb-1">Sonra</div>
                    {snapshot(item.afterSnapshot, item.source, 'text-ok')}
                  </div>
                </div>
              </Card14>
            )}

            {item.aiAnalysis && (
              <Card14 title={<span className="inline-flex items-center gap-1.5"><Sparkles className="w-4 h-4" aria-hidden="true" /> Yapay zekâ inceleme raporu</span>} tools={<span className="text-xs text-ink-3">{item.aiAnalysis.modelUsed} · {new Date(item.aiAnalysis.processedAt).toLocaleString('tr-TR')}</span>}>
                <div className="flex flex-col gap-2.5 text-sm [overflow-wrap:anywhere]">
                  {item.aiAnalysis.changesSummary && (
                    <div><div className="text-xs font-semibold text-ink-3">Değişiklik özeti</div><div className="text-ink mt-0.5">{item.aiAnalysis.changesSummary}</div></div>
                  )}
                  {item.aiAnalysis.detectedIssues && item.aiAnalysis.detectedIssues.length > 0 && (
                    <div>
                      <div className="text-xs font-semibold text-bad-text">Tespit edilen tıbbi hatalar</div>
                      <ul className="list-disc pl-5 mt-0.5 text-bad-text">{item.aiAnalysis.detectedIssues.map((issue, idx) => <li key={idx}>{issue}</li>)}</ul>
                    </div>
                  )}
                  {item.aiAnalysis.medicalReasoning && (
                    <div><div className="text-xs font-semibold text-ink-3">Tıbbi gerekçe</div><div className="text-ink-2 leading-relaxed mt-0.5 whitespace-pre-wrap">{item.aiAnalysis.medicalReasoning}</div></div>
                  )}
                </div>
              </Card14>
            )}

            {item.errorDetails && (
              <div className="ms-alert is-bad"><AlertTriangle aria-hidden="true" /><span><b>İnceleme sırasında hata:</b> {item.errorDetails}</span></div>
            )}
          </>
        }
        side={
          <>
            <Card14 title={<span className="inline-flex items-center gap-1.5"><MapPin className="w-4 h-4" aria-hidden="true" /> Konum</span>}>
              <div className="flex flex-col gap-2 text-sm [overflow-wrap:anywhere]">
                <code className="font-mono text-xs text-accent">{targetNav.badgeLabel}</code>
                <span className="text-ink-2">{targetNav.description}</span>
                <a href={targetNav.url} target="_blank" rel="noopener noreferrer" className="m14-btn self-start">
                  <ExternalLink aria-hidden="true" /> {targetNav.label}
                </a>
              </div>
            </Card14>
            <Card14 title="Bilgi">
              <FactList
                items={[
                  { k: 'Durum', v: getStatusBadge(item.status) },
                  { k: 'Kaynak', v: getSourceBadge(item.source, item.subTarget) },
                  { k: 'Hedef', v: <span className="font-mono text-xs [overflow-wrap:anywhere]">#{item.targetId}</span> },
                  { k: 'Bildiren', v: item.userReport.reportedBy || 'Anonim öğrenci' },
                  ...(item.userReport.email ? [{ k: 'E-posta', v: <span className="[overflow-wrap:anywhere]">{item.userReport.email}</span> }] : []),
                  { k: 'Tarih', v: new Date(item.userReport.reportedAt).toLocaleString('tr-TR') },
                  ...metaFacts(meta[item.id]),
                  ...(item.userReport.suggestedAnswer ? [{ k: 'Önerilen cevap', v: item.userReport.suggestedAnswer }] : []),
                  ...(item.aiAnalysis?.releaseQuarantine ? [{ k: 'Karantina', v: <Pill tone="ok">Karantinadan kurtarıldı</Pill> }] : []),
                  ...(item.aiAnalysis?.referencedRedactedId ? [{ k: 'Redakte soru', v: `#${item.aiAnalysis.referencedRedactedId}` }] : []),
                ]}
              />
            </Card14>
            {item.crossData && (
              <Card14 title={<span className="inline-flex items-center gap-1.5"><ShieldCheck className="w-4 h-4" aria-hidden="true" /> Çapraz veri denetimi</span>}>
                <div className="flex flex-col gap-1.5 text-sm text-ink-2 [overflow-wrap:anywhere]">
                  <div>
                    <b>Karantina:</b>{' '}
                    {item.crossData.isQuarantined
                      ? <span className="text-bad-text font-semibold">Karantinada ({item.crossData.quarantineReasons.join(', ') || 'Neden belirtilmemiş'})</span>
                      : <span className="text-ok">Karantinada değil</span>}
                  </div>
                  {item.crossData.mergeGroup && (
                    <div>
                      <b>Birleştirme grubu:</b> <code className="font-mono text-xs">{item.crossData.mergeGroup.groupId}</code> (asıl #{item.crossData.mergeGroup.asilId}, {item.crossData.mergeGroup.otherMembers.length} kardeş soru)
                    </div>
                  )}
                  {item.crossData.bestRedactedReference && (
                    <div>
                      <b>En temiz redaksiyon:</b> Soru #{item.crossData.bestRedactedReference.id} <Pill tone="acc">{item.crossData.bestRedactedReference.sourceType}</Pill>
                      <div className="text-xs italic mt-0.5">“{item.crossData.bestRedactedReference.stem}”</div>
                    </div>
                  )}
                </div>
              </Card14>
            )}
          </>
        }
      />
    );
  };

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <PageActions note="Kullanıcı bildirimleri kuyruğa alınır, ücretsiz model zinciriyle bağlam taranır ve düzeltmeler siteye işlenir; uygulanan her düzeltme geri alınabilir.">
        <button type="button" onClick={loadData} className="m14-btn ghost"><RefreshCw aria-hidden="true" /> Yenile</button>
        <button
          type="button"
          onClick={handleClearProcessed}
          disabled={actionBusy}
          className="m14-btn danger"
          title="İşlem yapılmış (uygulandı, doğru bulundu, geri alındı) tüm bildirimleri kalıcı olarak siler ve kimliklerini banlar"
        >
          <Trash2 aria-hidden="true" /> İşlem yapılanları temizle
        </button>
        <button
          type="button"
          onClick={handleToggleWorker}
          disabled={actionBusy}
          className="m14-btn"
          title={stats?.isWorkerActive ? 'Arka plan kuyruk işleyicisini duraklat' : 'Arka plan kuyruk işleyicisini başlat'}
        >
          {stats?.isWorkerActive ? <><Pause aria-hidden="true" /> Otomasyonu duraklat</> : <><Play aria-hidden="true" /> Otomasyonu başlat</>}
        </button>
        <button type="button" onClick={handleRunAll} disabled={actionBusy || (stats?.pending || 0) === 0} className="m14-btn" title="Tüm bekleyen bildirimleri sırayla arka planda incelet">
          <RefreshCw className={actionBusy ? 'animate-spin' : ''} aria-hidden="true" /> Tümünü incelet ({stats?.pending || 0})
        </button>
        <button type="button" onClick={handleRunNext} disabled={actionBusy || (stats?.pending || 0) === 0} className="m14-btn primary" title="Kuyruktaki ilk işlemi şimdi incelet">
          <Play aria-hidden="true" /> Sıradakini çalıştır
        </button>
      </PageActions>

      <StatRow
        stats={[
          { label: 'Kuyrukta bekleyen', value: stats?.pending ?? 0, tone: stats?.pending ? 'warn' : undefined, onClick: () => setFilterStatus('pending') },
          { label: 'Otomatik düzeltilen', value: stats?.applied ?? 0, tone: 'ok', onClick: () => setFilterStatus('applied') },
          { label: 'Değişiklik gerekmedi', value: stats?.noChange ?? 0, onClick: () => setFilterStatus('no_change') },
          { label: 'Geri alınan', value: stats?.rolledBack ?? 0, onClick: () => setFilterStatus('rolled_back') },
          { label: 'Otomasyon', value: stats?.isWorkerActive ? 'Çalışıyor' : 'Duraklatıldı', tone: stats?.isWorkerActive ? 'ok' : 'warn', hint: 'İnceleme modeli: Gemini 2.5 Flash (ücretsiz plan)' },
        ]}
      />

      <Toolbar>
        <Tabs14
          label="Durum"
          value={filterStatus}
          onChange={setFilterStatus}
          options={[
            { id: 'all', label: 'Tümü', n: items.length },
            { id: 'pending', label: 'Bekleyen', n: countOf('pending') },
            { id: 'applied', label: 'Uygulandı', n: countOf('applied') },
            { id: 'no_change', label: 'Değişiklik yok', n: countOf('no_change') },
            { id: 'rolled_back', label: 'Geri alındı', n: countOf('rolled_back') },
            { id: 'error', label: 'Hata', n: countOf('error') },
            { id: 'mine', label: 'Bana atanan', n: items.filter((x) => isMine(meta[x.id])).length },
            { id: 'snoozed', label: 'Ertelenenler', n: items.filter((x) => isSnoozed(meta[x.id])).length },
          ]}
        />
        <SearchField value={searchQuery} onChange={setSearchQuery} placeholder="Soru no, deste, kullanıcı notu, AI gerekçesi" label="İşlemlerde ara" />
        <label className="ms-select-chip !h-9">
          <span className="sr-only">Kaynak</span>
          <select value={filterSource} onChange={(e) => setFilterSource(e.target.value)}>
            <option value="all">Tüm kaynaklar</option>
            <option value="past_question">Çıkmış sorular</option>
            <option value="practice_question">Örnek sorular</option>
            <option value="interactive_deck">Öğrenme desteleri</option>
          </select>
        </label>
      </Toolbar>

      <BulkBar
        count={selection.count}
        noun="işlem"
        busy={actionBusy}
        onClear={selection.clear}
        actions={[
          { label: 'İncelet', kind: 'main', run: () => runBulk((x) => x.status !== 'processing' && x.status !== 'applied', retryAutoRepair) },
          { label: 'Geri al', run: () => runBulk((x) => x.status === 'applied', rollbackAutoRepair) },
          { label: 'Ertele', run: () => openAction('snooze', [...selection.sel]) },
          { label: 'Moderasyona aktar', run: () => escalate([...selection.sel]) },
          { label: 'Kişiye ata', run: () => openAction('assign', [...selection.sel]) },
          { label: 'Etiket ekle', run: () => openAction('tags', [...selection.sel]) },
          { label: 'Kişiye yanıt', run: () => openAction('reply', [...selection.sel]) },
          { label: 'Sil ve banla', kind: 'danger', confirm: `${selection.count} kayıt silinsin ve banlansın`, run: handleBulkDelete },
        ]}
      />

      {loading ? (
        <div className="py-16 text-center text-ink-3" role="status">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-accent" aria-hidden="true" />
          <p className="text-sm">Bekleyen işlemler yükleniyor…</p>
        </div>
      ) : (
        <DataTable
          rows={filteredItems}
          cols={cols}
          rowKey={(x) => x.id}
          onOpen={(x) => setExpandedId(x.id)}
          selection={selection}
          activeKey={expandedId}
          minWidth={960}
          empty={
            searchQuery || filterStatus !== 'all' || filterSource !== 'all'
              ? 'Seçili süzgeçlere uygun işlem bulunamadı.'
              : 'Kuyruk temiz. Kullanıcılar hata bildirdikçe kayıtlar buraya eklenir ve sırayla işlenir.'
          }
        />
      )}

      <Drawer
        open={!!openItem && !actMode}
        onClose={() => setExpandedId(null)}
        title={openItem ? openItem.userReport.reason : 'İşlem'}
        label="İşlem ayrıntısı"
        wide
        head={<DetailNav list={filteredItems} current={openItem} same={(a, b) => a.id === b.id} onGo={(x) => setExpandedId(x.id)} />}
        foot={openItem && (
          <>
            <button type="button" onClick={() => handleDelete(openItem.id)} className="m14-btn danger"><Trash2 aria-hidden="true" /> Sil ve banla</button>
            <button type="button" onClick={() => openAction('assign', [openItem.id])} className="m14-btn ghost"><UserPlus aria-hidden="true" /> Kişiye ata</button>
            <button type="button" onClick={() => openAction('tags', [openItem.id])} className="m14-btn ghost"><Tag aria-hidden="true" /> Etiket</button>
            <button type="button" onClick={() => openAction('reply', [openItem.id])} className="m14-btn ghost"><Reply aria-hidden="true" /> Kişiye yanıt</button>
            <button type="button" onClick={() => openAction('snooze', [openItem.id])} className="m14-btn ghost"><Clock aria-hidden="true" /> Ertele</button>
            {meta[openItem.id]?.escalated ? (
              <button type="button" onClick={() => void act([openItem.id], 'unescalate')} className="m14-btn ghost"><ShieldAlert aria-hidden="true" /> Aktarmayı geri al</button>
            ) : (
              <button type="button" onClick={() => void escalate([openItem.id])} className="m14-btn" title="Kaydı moderasyona elle karar için aktar"><ShieldAlert aria-hidden="true" /> Moderasyona aktar</button>
            )}
            {openItem.status === 'applied' && (
              <button type="button" onClick={() => handleRollback(openItem.id)} disabled={actionBusy} className="m14-btn" title="Bu değişikliği geri al ve eski veriyi yerine koy">
                <RotateCcw aria-hidden="true" /> Geri al
              </button>
            )}
            {(openItem.status === 'error' || openItem.status === 'rolled_back' || openItem.status === 'no_change') && (
              <button type="button" onClick={() => handleRetry(openItem.id)} disabled={actionBusy} className="m14-btn primary"><RefreshCw aria-hidden="true" /> Tekrar incelet</button>
            )}
            {openItem.status === 'pending' && (
              <button type="button" onClick={() => reviewNow(openItem.id)} disabled={actionBusy} className="m14-btn primary"><Sparkles aria-hidden="true" /> Şimdi incele</button>
            )}
          </>
        )}
      >
        {openItem && renderDetail(openItem)}
        {openItem && <div className="mt-3"><ReplyHistory m={meta[openItem.id]} /></div>}
      </Drawer>

      <ModerationActionDrawer
        mode={actMode}
        ids={actIds}
        kind="repair"
        current={actIds.length === 1 ? meta[actIds[0]] : undefined}
        onClose={() => setActMode(null)}
        act={act}
      />
    </div>
  );
};
