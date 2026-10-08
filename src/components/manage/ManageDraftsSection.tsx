import React, { useEffect, useMemo, useState } from 'react';
import {
  Layers,
  RefreshCw,
  GitMerge,
  Check,
  ChevronDown,
  Zap,
  Eye,
  EyeOff,
  Undo2,
  Split,
  Trash2,
  Pencil,
  Sparkles,
  X,
  Wand2,
} from 'lucide-react';
import type { QuestionItem, ClusterAnalysisSummary, DraftCluster, ClusterTuning } from '../../types';
import { ApiService } from '../../services/api';
import {
  CLUSTER_PRESETS,
  blockPair,
  clearBlockedPairs,
  loadBlockedPairs,
} from '../../services/draftClusteringService';
import { AdminEditQuestionModal } from '../AdminEditQuestionModal';
import { sharedWordColors, Colored, WordLegend } from '../draftHighlight';
import { AiQuestionOptimizerModal } from '../AiQuestionOptimizerModal';
import {
  deleteDraftEverywhere,
  reconstructDraft,
} from '../../services/manageConsoleService';
import { Seg, SearchBox, EmptyState, ConfirmButton } from './consoleUi';

interface ManageDraftsSectionProps {
  adminEmail: string;
  adminName?: string;
  committeeId: string;
  committeeName?: string;
  questions: QuestionItem[];
  onRefreshData: () => Promise<void>;
  notify: (msg: string) => void;
}

type Filter = 'ready' | 'review' | 'merged' | 'manual' | 'all' | 'vague';

export const ManageDraftsSection: React.FC<ManageDraftsSectionProps> = ({
  adminEmail,
  adminName,
  committeeId,
  questions,
  onRefreshData,
  notify,
}) => {
  const [analysis, setAnalysis] = useState<ClusterAnalysisSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeFilter, setActiveFilter] = useState<Filter>('ready');
  const [mergingClusterId, setMergingClusterId] = useState<string | null>(null);
  const [isBatchMerging, setIsBatchMerging] = useState(false);
  const [expandedClusterId, setExpandedClusterId] = useState<string | null>(null);
  const [locallyMergedSatelliteIds, setLocallyMergedSatelliteIds] = useState<Set<string>>(new Set());
  const [unmergingQuestionId, setUnmergingQuestionId] = useState<string | null>(null);
  const [inspectingMergedId, setInspectingMergedId] = useState<string | null>(null);
  const [selectedDraftIds, setSelectedDraftIds] = useState<string[]>([]);
  const [manualAnchorId, setManualAnchorId] = useState<string>('');
  const [manualSearchQuery, setManualSearchQuery] = useState('');
  // Birleştir'e basıldığı an elle-seç listesinden kalkması için iyimser gizleme
  const [manuallyHiddenIds, setManuallyHiddenIds] = useState<Set<string>>(new Set());
  const [isManualMerging, setIsManualMerging] = useState(false);
  const [isBulkDeleting, setIsBulkDeleting] = useState(false);
  const [editingDraft, setEditingDraft] = useState<QuestionItem | null>(null);
  const [optimizingQuestion, setOptimizingQuestion] = useState<QuestionItem | null>(null);
  const [reconstructingIds, setReconstructingIds] = useState<Set<string>>(new Set());
  const [deletingIds, setDeletingIds] = useState<Set<string>>(new Set());
  const [sensitivity, setSensitivity] = useState<'strict' | 'balanced' | 'loose'>(() => {
    try {
      const s = localStorage.getItem('medsoru_cluster_sensitivity');
      return s === 'strict' || s === 'loose' ? s : 'balanced';
    } catch {
      return 'balanced';
    }
  });
  const [anchorOverrides, setAnchorOverrides] = useState<Record<string, string>>({});
  const [blockedCount, setBlockedCount] = useState(() => loadBlockedPairs().size);

  const tuning: ClusterTuning = useMemo(() => ({ ...CLUSTER_PRESETS[sensitivity] }), [sensitivity]);

  const runAnalysis = async () => {
    if (!committeeId) return;
    setLoading(true);
    try {
      const summary = await ApiService.getCommitteeDraftClusters(committeeId, tuning);
      setAnalysis(summary);
      setBlockedCount(loadBlockedPairs().size);
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Analiz sırasında hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void runAnalysis();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [committeeId, questions.length, sensitivity]);

  const changeSensitivity = (s: 'strict' | 'balanced' | 'loose') => {
    setSensitivity(s);
    try {
      localStorage.setItem('medsoru_cluster_sensitivity', s);
    } catch {
      /* yoksay */
    }
  };

  const stemOf = (q: QuestionItem) =>
    q.reconstruction?.stem || q.stem || q.fragments?.[0]?.text || '';
  const fullText = (q: QuestionItem) => [stemOf(q), ...(q.options || []).map((o) => o.text)].join(' ');
  const numLabel = (q: QuestionItem) => (q.isUnassignedNumber || !q.questionNumber ? 'No ?' : `S.${q.questionNumber}`);

  const committeeQuestions = useMemo(
    () =>
      questions.filter((q) => {
        if (committeeId && q.committeeId !== committeeId) return false;
        if (locallyMergedSatelliteIds.has(q.id)) return false;
        return true;
      }),
    [questions, committeeId, locallyMergedSatelliteIds]
  );

  const mergedQuestions = useMemo(
    () =>
      committeeQuestions.filter(
        (q) =>
          q.tags?.includes('taslak-birlestirildi') ||
          q.isMerged ||
          (q.mergedSatellites && q.mergedSatellites.length > 0) ||
          (q.fragments && q.fragments.some((f) => f.text.includes('[Birleştirilen Taslak')))
      ),
    [committeeQuestions]
  );

  const filteredClusters = useMemo(() => {
    if (!analysis) return [];
    if (activeFilter === 'all') return analysis.clusters;
    if (activeFilter === 'ready') return analysis.clusters.filter((c) => c.status === 'ready_to_merge');
    if (activeFilter === 'review') return analysis.clusters.filter((c) => c.status === 'needs_review');
    return [];
  }, [analysis, activeFilter]);

  const manualFilteredQuestions = useMemo(() => {
    // Birleştirilmiş sorular ve az önce birleştirilenler elle-seçimde görünmez
    const mergedIds = new Set(mergedQuestions.map((q) => q.id));
    const selectable = committeeQuestions.filter((q) => !mergedIds.has(q.id) && !manuallyHiddenIds.has(q.id));
    if (!manualSearchQuery.trim()) return selectable;
    const q = manualSearchQuery.toLowerCase();
    return selectable.filter((item) => {
      const stem = item.reconstruction?.stem || item.stem || item.fragments?.map((f) => f.text).join(' ') || '';
      return (
        stem.toLowerCase().includes(q) ||
        item.discipline?.toLowerCase().includes(q) ||
        item.topic?.toLowerCase().includes(q) ||
        item.questionNumber?.toString() === q
      );
    });
  }, [committeeQuestions, manualSearchQuery, mergedQuestions, manuallyHiddenIds]);

  const selectedQs = selectedDraftIds
    .map((id) => committeeQuestions.find((x) => x.id === id))
    .filter((x): x is QuestionItem => Boolean(x));
  const manualColors = selectedQs.length >= 2 ? sharedWordColors(selectedQs.map(fullText)) : new Map<string, string>();

  const readyCount = analysis?.clusters.filter((c) => c.status === 'ready_to_merge').length || 0;
  const reviewCount = analysis?.clusters.filter((c) => c.status === 'needs_review').length || 0;
  const busy = loading || isBatchMerging || isManualMerging || isBulkDeleting || !!mergingClusterId;

  // ---------- actions ----------
  const effectiveAnchorOf = (cluster: DraftCluster): QuestionItem => {
    const overrideId = anchorOverrides[cluster.id];
    if (!overrideId) return cluster.anchorQuestion;
    const all = [cluster.anchorQuestion, ...cluster.satelliteDrafts.map((s) => s.question)];
    return all.find((q) => q.id === overrideId) || cluster.anchorQuestion;
  };

  const handleMergeCluster = async (cluster: DraftCluster) => {
    const anchor = effectiveAnchorOf(cluster);
    setMergingClusterId(cluster.id);
    try {
      const satelliteIds = [cluster.anchorQuestion, ...cluster.satelliteDrafts.map((s) => s.question)]
        .map((q) => q.id)
        .filter((id) => id !== anchor.id);
      await ApiService.mergeDraftCluster(adminEmail, anchor.id, satelliteIds, adminName || 'Yönetici');
      setLocallyMergedSatelliteIds((prev) => new Set([...prev, ...satelliteIds]));
      setSelectedDraftIds((prev) => prev.filter((id) => !satelliteIds.includes(id) && id !== anchor.id));
      setAnchorOverrides((prev) => {
        const next = { ...prev };
        delete next[cluster.id];
        return next;
      });
      notify(`Soru #${anchor.questionNumber || 'Çapa'} için ${satelliteIds.length} taslak birleştirildi.`);
      await onRefreshData();
      await runAnalysis();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Birleştirme başarısız oldu.');
    } finally {
      setMergingClusterId(null);
    }
  };

  const handleMarkNotSame = (anchorId: string, satelliteId: string) => {
    const next = blockPair(anchorId, satelliteId);
    setBlockedCount(next.size);
    // Ekrandan da anında kaldır (görünüm); bir dahaki analizde zaten gelmez.
    setAnalysis((prev) => {
      if (!prev) return null;
      const nextClusters = prev.clusters
        .map((c) => ({ ...c, satelliteDrafts: c.satelliteDrafts.filter((s) => !(s.question.id === satelliteId && c.anchorQuestion.id === anchorId)) }))
        .filter((c) => c.satelliteDrafts.length > 0);
      return { ...prev, clusters: nextClusters, mergeableClustersCount: nextClusters.length };
    });
    notify('Bu ikisi artık aynı kümede gösterilmeyecek (kalıcı).');
  };

  const handleClearBlocked = () => {
    clearBlockedPairs();
    setBlockedCount(0);
    notify('Engel listesi temizlendi; analiz yenileniyor.');
    void runAnalysis();
  };

  const handleBatchMergeReady = async () => {
    setIsBatchMerging(true);
    try {
      const res = await ApiService.autoMergeHighConfidenceClusters(adminEmail, committeeId, adminName || 'Akıllı Konsolidasyon');
      notify(`Toplu işlem tamamlandı: ${res.mergedClustersCount} küme birleştirildi, ${res.savedDuplicatesCount} mükerrer taslak entegre edildi.`);
      await onRefreshData();
      await runAnalysis();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Toplu birleştirme başarısız oldu.');
    } finally {
      setIsBatchMerging(false);
    }
  };

  const handleManualMergeSelected = async () => {
    if (selectedDraftIds.length < 2) {
      notify('Birleştirmek için en az 2 taslak seçmelisiniz.');
      return;
    }
    const idsToMerge = [...selectedDraftIds];
    const anchorId = manualAnchorId || idsToMerge[0];
    const satelliteIds = idsToMerge.filter((id) => id !== anchorId);
    // Basıldığı an listeden kaldır (sonuç beklenmez); hata olursa geri getirilir.
    setManuallyHiddenIds((prev) => new Set([...prev, ...idsToMerge]));
    setSelectedDraftIds([]);
    setManualAnchorId('');
    setIsManualMerging(true);
    try {
      await ApiService.mergeDraftCluster(adminEmail, anchorId, satelliteIds, adminName || 'Yönetici');
      setLocallyMergedSatelliteIds((prev) => new Set([...prev, ...satelliteIds]));
      notify(`Seçtiğiniz ${satelliteIds.length + 1} taslak tek bir soru altında toplandı.`);
      await onRefreshData();
      await runAnalysis();
    } catch (e) {
      setManuallyHiddenIds((prev) => {
        const next = new Set(prev);
        idsToMerge.forEach((id) => next.delete(id));
        return next;
      });
      setSelectedDraftIds(idsToMerge);
      setManualAnchorId(anchorId);
      notify(e instanceof Error ? e.message : 'Manuel birleştirme başarısız oldu.');
    } finally {
      setIsManualMerging(false);
    }
  };

  const handleBulkDeleteSelected = async () => {
    if (selectedDraftIds.length === 0) {
      notify('Silmek için önce taslak seçmelisiniz.');
      return;
    }
    const idsToDelete = [...selectedDraftIds];
    setManuallyHiddenIds((prev) => new Set([...prev, ...idsToDelete]));
    setSelectedDraftIds([]);
    setManualAnchorId('');
    setIsBulkDeleting(true);
    try {
      const failed: string[] = [];
      let ok = 0;
      for (const id of idsToDelete) {
        const q = committeeQuestions.find((x) => x.id === id);
        if (!q) continue;
        const res = await deleteDraftEverywhere(adminEmail, q);
        if (res.ok) ok++;
        else failed.push(id);
      }
      if (failed.length > 0) {
        setManuallyHiddenIds((prev) => {
          const next = new Set(prev);
          failed.forEach((id) => next.delete(id));
          return next;
        });
      }
      notify(`Toplu silme tamamlandı: ${ok} silindi${failed.length > 0 ? `, ${failed.length} başarısız (listeye geri alındı)` : ''}.`);
      if (ok > 0) {
        await onRefreshData();
        await runAnalysis();
      }
    } finally {
      setIsBulkDeleting(false);
    }
  };

  const handleDetachSatellite = (clusterId: string, satelliteQuestionId: string) => {
    if (!analysis) return;
    setAnalysis((prev) => {
      if (!prev) return null;
      const nextClusters = prev.clusters
        .map((c) => (c.id !== clusterId ? c : { ...c, satelliteDrafts: c.satelliteDrafts.filter((s) => s.question.id !== satelliteQuestionId) }))
        .filter((c) => c.satelliteDrafts.length > 0);
      return { ...prev, clusters: nextClusters, mergeableClustersCount: nextClusters.length, vagueDraftsCount: prev.vagueDraftsCount + 1 };
    });
    notify('Taslak bu kümeden çıkarıldı (yalnızca görünüm; kalıcı ayırma için birleştirip "Ayır" kullanın).');
  };

  const handleDissolveCluster = (clusterId: string) => {
    if (!analysis) return;
    setAnalysis((prev) => {
      if (!prev) return null;
      const target = prev.clusters.find((c) => c.id === clusterId);
      const detachedCount = (target?.satelliteDrafts.length || 0) + 1;
      const nextClusters = prev.clusters.filter((c) => c.id !== clusterId);
      return { ...prev, clusters: nextClusters, mergeableClustersCount: nextClusters.length, vagueDraftsCount: prev.vagueDraftsCount + detachedCount };
    });
    notify('Küme dağıtıldı (yalnızca görünüm).');
  };

  const handleUnmergeQuestion = async (questionId: string) => {
    setUnmergingQuestionId(questionId);
    try {
      const res = await ApiService.unmergeDraftCluster(adminEmail, questionId, adminName || 'Yönetici');
      setLocallyMergedSatelliteIds((prev) => {
        const next = new Set(prev);
        res.restoredSatellites.forEach((s) => next.delete(s.id));
        return next;
      });
      notify(`${res.restoredSatellites.length} taslak bağımsız hale getirildi.`);
      await onRefreshData();
      await runAnalysis();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Ayırma başarısız oldu.');
    } finally {
      setUnmergingQuestionId(null);
    }
  };

  const handleDeleteDraft = async (q: QuestionItem) => {
    // Anında listeden kaldır; tüm kanallar başarısız olursa geri getir.
    setDeletingIds((prev) => new Set(prev).add(q.id));
    setManuallyHiddenIds((prev) => new Set([...prev, q.id]));
    setSelectedDraftIds((prev) => prev.filter((id) => id !== q.id));
    try {
      const res = await deleteDraftEverywhere(adminEmail, q);
      notify(res.message);
      if (!res.ok) {
        setManuallyHiddenIds((prev) => {
          const next = new Set(prev);
          next.delete(q.id);
          return next;
        });
      } else {
        await onRefreshData();
        await runAnalysis();
      }
    } finally {
      setDeletingIds((prev) => {
        const next = new Set(prev);
        next.delete(q.id);
        return next;
      });
    }
  };

  const handleReconstruct = async (q: QuestionItem) => {
    setReconstructingIds((prev) => new Set(prev).add(q.id));
    try {
      const res = await reconstructDraft(q);
      notify(res.message);
      if (res.ok) {
        await onRefreshData();
        await runAnalysis();
      }
    } finally {
      setReconstructingIds((prev) => {
        const next = new Set(prev);
        next.delete(q.id);
        return next;
      });
    }
  };

  const toggleSelectDraft = (id: string) => {
    setSelectedDraftIds((prev) => {
      const next = prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id];
      if (!manualAnchorId && next.length > 0) {
        setManualAnchorId(next[0]);
      } else if (!next.includes(manualAnchorId)) {
        setManualAnchorId(next[0] || '');
      }
      return next;
    });
  };

  // ---------- shared row actions ----------
  const DraftActions: React.FC<{ q: QuestionItem; compact?: boolean }> = ({ q, compact }) => {
    const isRec = reconstructingIds.has(q.id);
    const isDel = deletingIds.has(q.id);
    return (
      <span className={`inline-flex items-center gap-1 ${compact ? '' : 'flex-wrap'}`} onClick={(e) => e.stopPropagation()}>
        <button type="button" onClick={() => setEditingDraft(q)} className="ms-btn is-sm is-ghost" title="Taslağı düzenle">
          <Pencil /> Düzenle
        </button>
        <button type="button" onClick={() => setOptimizingQuestion(q)} className="ms-btn is-sm is-tonal" title="Amfi slaytlarıyla tam soruya geliştir (önizlemeli)">
          <Wand2 /> AI ile geliştir
        </button>
        <button type="button" onClick={() => { void handleReconstruct(q); }} disabled={isRec} className="ms-btn is-sm is-ghost" title="Doğrudan tam soruya dönüştür">
          {isRec ? <RefreshCw className="animate-spin" /> : <Sparkles />} {isRec ? 'Dönüşüyor…' : 'AI dönüştür'}
        </button>
        <button type="button" onClick={() => { void handleDeleteDraft(q); }} disabled={isDel} className="ms-btn is-sm is-danger" title="Taslağı her yerden sil">
          {isDel ? <RefreshCw className="animate-spin" /> : <Trash2 />} {isDel ? 'Siliniyor…' : 'Sil'}
        </button>
      </span>
    );
  };

  const tabs: { id: Filter; label: string; count?: number }[] = [
    { id: 'ready', label: 'Hazır', count: readyCount },
    { id: 'review', label: 'İncele', count: reviewCount },
    { id: 'merged', label: 'Birleştirilenler', count: mergedQuestions.length },
    { id: 'all', label: 'Tümü', count: analysis?.clusters.length || 0 },
    { id: 'vague', label: 'Muğlak', count: analysis?.vagueDraftsCount || 0 },
    { id: 'manual', label: 'Elle seç', count: selectedDraftIds.length || undefined },
  ];

  const summary = [
    { label: 'taslak', value: analysis?.totalDrafts ?? '–', tone: '' },
    { label: 'tahmini soru', value: analysis?.estimatedTrueQuestions ?? '–', tone: 'is-ok' },
    { label: `hazır küme (${analysis?.potentialSavedDuplicates ?? 0} mükerrer)`, value: readyCount, tone: 'is-ok' },
    { label: 'birleşik', value: mergedQuestions.length, tone: '' },
    { label: 'muğlak', value: analysis?.vagueDraftsCount ?? '–', tone: 'is-warn' },
  ];

  const qrow = (q: QuestionItem, extra?: React.ReactNode, colors?: Map<string, string>) => (
    <>
      <span className="ms-row-meta">
        <span className="font-mono font-semibold text-ink">{numLabel(q)}</span>
        <span className="truncate">{q.discipline}{q.topic ? ` · ${q.topic}` : ''}</span>
        {extra}
      </span>
      <span className="text-[14px] text-ink leading-snug">{stemOf(q) ? (colors ? <Colored text={stemOf(q)} colors={colors} /> : stemOf(q)) : <span className="text-ink-3">Metin girilmemiş</span>}</span>
    </>
  );

  return (
    <div className="flex flex-col gap-3 min-w-0">
      <div className="flex flex-col xl:flex-row xl:items-center gap-2">
        <p className="m-0 flex flex-wrap items-center gap-x-4 gap-y-1 text-[13px] text-ink-2 flex-1 min-w-0">
          {summary.map((x) => (
            <span key={x.label} className="inline-flex items-center gap-1.5 tabular-nums">
              <span className={`ms-sdot ${x.tone}`} aria-hidden="true" />
              <b className="text-ink">{x.value}</b> {x.label}
            </span>
          ))}
        </p>
        <div className="flex items-center gap-2 shrink-0 flex-wrap">
          <Seg
            label="Kümeleme hassasiyeti"
            value={sensitivity}
            onChange={(v) => changeSensitivity(v)}
            options={[
              { id: 'strict', label: 'Sıkı' },
              { id: 'balanced', label: 'Dengeli' },
              { id: 'loose', label: 'Gevşek' },
            ]}
          />
          {blockedCount > 0 && (
            <button type="button" onClick={handleClearBlocked} title="“Aynı değil” engellerini temizle" className="ms-btn is-ghost">
              <X /> {blockedCount} engel
            </button>
          )}
          <button type="button" onClick={() => { void runAnalysis(); }} disabled={loading} className="ms-btn">
            <RefreshCw className={loading ? 'animate-spin' : ''} /> Yeniden analiz
          </button>
          {readyCount > 0 && (
            <ConfirmButton icon={Zap} className="ms-btn is-ok" confirmLabel={`Emin misin? ${readyCount} küme`} busy={isBatchMerging} busyLabel="Birleştiriliyor…" onConfirm={() => handleBatchMergeReady()}>
              Hazır {readyCount} kümeyi birleştir
            </ConfirmButton>
          )}
        </div>
      </div>

      <Seg
        label="Taslak görünümü"
        value={activeFilter}
        onChange={setActiveFilter}
        className="self-start"
        options={tabs.map((t) => ({ id: t.id, label: t.id === 'manual' ? <><GitMerge className="w-3.5 h-3.5" />{t.label}</> : t.label, n: t.count }))}
      />

      {loading ? (
        <div className="flex flex-col gap-3" role="status" aria-label="Taslaklar taranıyor">
          {[0, 1, 2].map((i) => <div key={i} className="h-28 rounded-2xl ms-shimmer" />)}
        </div>
      ) : activeFilter === 'merged' ? (
        <div className="flex flex-col gap-3">
          <p className="m-0 text-[13.5px] text-ink-2">Daha önce birleştirilmiş taslaklar. Parçaları incele; hata varsa <b className="text-ink">Ayır</b> ile eski hallerine döndür.</p>
          {mergedQuestions.length === 0 && (
            <section className="ms-panel"><EmptyState icon={Layers} title="Henüz birleştirilmiş soru yok">“Hazır” ya da “Elle seç” sekmesinden birleştirebilirsin.</EmptyState></section>
          )}
          {mergedQuestions.map((q) => {
            const isInspecting = inspectingMergedId === q.id;
            const isUnmerging = unmergingQuestionId === q.id;
            const satelliteCount = q.mergedSatellites?.length || q.fragments?.filter((f) => f.text.includes('[Birleştirilen Taslak')).length || 0;
            return (
              <article key={q.id} className="ms-panel">
                <div className="ms-row !border-t-0">
                  <span className="ms-ricon is-ok font-mono text-[12.5px] font-bold">{numLabel(q)}</span>
                  <div className="ms-row-main">
                    <span className="flex flex-wrap items-center gap-2">
                      <span className="ms-row-title truncate">{q.topic || q.discipline || 'Birleştirilmiş soru'}</span>
                      <span className="ms-tag is-ok"><Layers /> {satelliteCount > 0 ? `${satelliteCount + 1} taslak` : 'Birleşik'}</span>
                    </span>
                    <span className="ms-row-meta"><span>{q.discipline}</span><span>{q.fragments?.length || 0} parça</span><span>{q.options?.length || 0} şık</span></span>
                    <p className="m-0 pt-1 text-[14px] text-ink leading-relaxed">{stemOf(q) || <span className="text-ink-3">Soru kökü henüz girilmemiş</span>}</p>
                  </div>
                </div>
                <div className="flex flex-wrap items-center gap-1 px-4 pb-3 pl-[60px]">
                  <DraftActions q={q} compact />
                  <span className="flex-1" />
                  <button type="button" onClick={() => setInspectingMergedId(isInspecting ? null : q.id)} className="ms-btn is-sm">
                    {isInspecting ? <EyeOff /> : <Eye />} {isInspecting ? 'Kapat' : 'Parçalar'}
                  </button>
                  <button type="button" onClick={() => { void handleUnmergeQuestion(q.id); }} disabled={isUnmerging} className="ms-btn is-sm is-warn">
                    {isUnmerging ? <RefreshCw className="animate-spin" /> : <Undo2 />} {isUnmerging ? 'Ayrılıyor…' : 'Ayır'}
                  </button>
                </div>
                {isInspecting && q.mergedSatellites && q.mergedSatellites.length > 0 && (
                  <div className="flex flex-col gap-2 px-4 pb-4 pl-[60px]">
                    {q.mergedSatellites.map((sat, sIdx) => (
                      <div key={sat.id || sIdx} className="rounded-xl bg-canvas p-3 text-[13px] flex flex-col gap-1.5">
                        <div className="flex items-center justify-between gap-2">
                          <span className="font-semibold text-ink">{sat.contributedByName || sat.author || 'Anonim'}</span>
                          <span className="text-[11.5px] text-ink-3 font-mono">{numLabel(sat)}</span>
                        </div>
                        <p className="m-0 text-ink-2 leading-relaxed">{stemOf(sat) || 'Metin girilmemiş'}</p>
                        {sat.fragments && sat.fragments.length > 0 && (
                          <ul className="m-0 p-0 list-none flex flex-col gap-0.5">
                            {sat.fragments.map((sf) => (
                              <li key={sf.id} className="text-[12.5px] text-ink-3"><b className="font-medium text-ink-2">{sf.author}:</b> “{sf.text}”</li>
                            ))}
                          </ul>
                        )}
                        {sat.options && sat.options.length > 0 && (
                          <div className="flex flex-wrap gap-1">
                            {sat.options.map((opt) => (
                              <span key={opt.key} className="ms-tag !h-auto !py-1 !whitespace-normal"><b className="font-mono">{opt.key}</b> {opt.text}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </article>
            );
          })}
        </div>
      ) : activeFilter === 'manual' ? (
        <div className="flex flex-col gap-2.5">
          <p className="m-0 text-[13.5px] text-ink-2">Aynı soruya ait taslakları işaretle. Biri <b className="text-ink">çapa</b> olur; şıklar harmanlanır, mükerrerler temizlenir. Seçtiklerinde ortak geçen kelimeler aynı renkle boyanır.</p>
          {manualColors.size > 0 && <WordLegend texts={selectedQs.map(fullText)} colors={manualColors} />}
          <SearchBox value={manualSearchQuery} onChange={setManualSearchQuery} placeholder="Metin, konu, ders ya da soru no" count={manualFilteredQuestions.length} />
          <section className="ms-panel">
            <ul className="ms-rows">
              {manualFilteredQuestions.map((q) => {
                const on = selectedDraftIds.includes(q.id);
                const isAnchor = on && manualAnchorId === q.id;
                return (
                  <li key={q.id} className={`ms-row ${on ? 'is-on' : ''}`}>
                    <button type="button" role="checkbox" aria-checked={on} onClick={() => toggleSelectDraft(q.id)} aria-label="Taslağı seç"
                      className={`mt-0.5 w-5 h-5 rounded-md flex items-center justify-center shrink-0 cursor-pointer transition-colors ${on ? 'bg-accent text-white' : 'bg-white border border-line-2 hover:border-accent'}`}>
                      {on && <Check className="w-3.5 h-3.5" strokeWidth={3} />}
                    </button>
                    <div className="ms-row-main">
                      {qrow(q, isAnchor ? <span className="ms-tag is-accent">Çapa</span> : undefined, manualColors)}
                      {q.options && q.options.length > 0 && (
                        <span className="flex flex-wrap gap-1 pt-0.5">
                          {q.options.map((o) => (
                            <span key={o.key} className="ms-tag max-w-[260px] truncate"><b className="font-mono">{o.key}</b> <Colored text={o.text} colors={manualColors} /></span>
                          ))}
                        </span>
                      )}
                      <span className="pt-1"><DraftActions q={q} compact /></span>
                    </div>
                  </li>
                );
              })}
            </ul>
          </section>
          {selectedDraftIds.length > 0 && (
            <div className="ms-bulkbar">
              <b>{selectedDraftIds.length} seçili</b>
              {selectedDraftIds.length >= 2 && (
                <select value={manualAnchorId} onChange={(e) => setManualAnchorId(e.target.value)} aria-label="Çapa soru">
                  {selectedDraftIds.map((id) => {
                    const q = committeeQuestions.find((x) => x.id === id);
                    return <option key={id} value={id}>Çapa: {q ? numLabel(q) : '?'} · {q?.topic || q?.discipline}</option>;
                  })}
                </select>
              )}
              <button type="button" onClick={() => { setSelectedDraftIds([]); setManualAnchorId(''); }} className="ms-btn">Temizle</button>
              <ConfirmButton icon={Trash2} className="ms-btn" confirmLabel="Emin misin? Sil" busy={isBulkDeleting} onConfirm={() => handleBulkDeleteSelected()}>
                Sil
              </ConfirmButton>
              <button type="button" onClick={() => { void handleManualMergeSelected(); }} disabled={isManualMerging || selectedDraftIds.length < 2} className="ms-btn is-primary">
                {isManualMerging ? <RefreshCw className="animate-spin" /> : <GitMerge />}
                {selectedDraftIds.length < 2 ? 'En az 2 seç' : 'Birleştir'}
              </button>
            </div>
          )}
        </div>
      ) : activeFilter === 'vague' ? (
        <div className="flex flex-col gap-2">
          <p className="m-0 text-[13.5px] text-ink-2">Bu taslaklarda güçlü bir eşleşme için yeterli bilgi yok. Yeni ipucu ya da şık geldikçe kendiliğinden bağlanırlar.</p>
          <section className="ms-panel">
            {!analysis?.unmatchedVagueDrafts.length ? (
              <EmptyState icon={Check} title="Muğlak taslak yok" />
            ) : (
              <ul className="ms-rows">
                {analysis.unmatchedVagueDrafts.map((q) => (
                  <li key={q.id} className="ms-row">
                    <div className="ms-row-main">
                      {qrow(q)}
                      <span className="pt-1"><DraftActions q={q} compact /></span>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      ) : filteredClusters.length === 0 ? (
        <section className="ms-panel">
          <EmptyState icon={Layers} title="Bu sekmede küme yok" action={<button type="button" onClick={() => setActiveFilter('manual')} className="ms-btn is-primary"><GitMerge /> Elle seçime geç</button>}>
            Taslakları kendin birleştirmek istersen elle seçebilirsin.
          </EmptyState>
        </section>
      ) : (
        filteredClusters.map((cluster) => {
          const anchor = effectiveAnchorOf(cluster);
          const members = [cluster.anchorQuestion, ...cluster.satelliteDrafts.map((sd) => sd.question)];
          const satellites = members.filter((q) => q.id !== anchor.id);
          const open = expandedClusterId === cluster.id;
          const merging = mergingClusterId === cluster.id;
          const ready = cluster.status === 'ready_to_merge';
          const clusterTexts = members.map(fullText);
          const colors = sharedWordColors(clusterTexts);
          return (
            <article key={cluster.id} className="ms-panel">
              <header className="ms-panel-head">
                <span className={`ms-ricon ${ready ? 'is-ok' : 'is-warn'} font-mono text-[12.5px] font-bold`}>{anchor.isUnassignedNumber || !anchor.questionNumber ? '?' : anchor.questionNumber}</span>
                <span className="flex-1 min-w-[200px] flex flex-col gap-0.5">
                  <span className="flex items-center gap-2 min-w-0">
                    <span className="text-[14.5px] font-semibold text-ink truncate">{cluster.detectedSubject || anchor.topic || anchor.discipline}</span>
                    <span className={`ms-tag ${ready ? 'is-ok' : 'is-warn'} tabular-nums`}>%{cluster.overallConfidence}</span>
                  </span>
                  <span className="text-[12.5px] text-ink-3 truncate">{anchor.discipline} · {satellites.length} taslak birleşecek</span>
                </span>
                <span className="ms-panel-tools">
                  <label className="inline-flex items-center gap-1.5 text-[12.5px] text-ink-3">
                    Çapa
                    <select value={anchor.id} onChange={(e) => setAnchorOverrides((prev) => ({ ...prev, [cluster.id]: e.target.value }))} className="ms-input is-sm !w-auto max-w-[220px]" title="Birleşince ana soru olacak taslak">
                      {members.map((m) => (
                        <option key={m.id} value={m.id}>{numLabel(m)} · {(m.topic || m.discipline || '').slice(0, 40)}</option>
                      ))}
                    </select>
                  </label>
                  <button type="button" onClick={() => handleDissolveCluster(cluster.id)} title="Bu kümeyi dağıt (yalnızca görünüm)" className="ms-btn is-sm is-ghost">
                    <Split /> Dağıt
                  </button>
                  <button type="button" onClick={() => setExpandedClusterId(open ? null : cluster.id)} aria-expanded={open} className="ms-btn is-sm">
                    Karşılaştır <ChevronDown className={`transition-transform ${open ? 'rotate-180' : ''}`} />
                  </button>
                  <button type="button" onClick={() => { void handleMergeCluster(cluster); }} disabled={merging || busy} className={`ms-btn is-sm ${ready ? 'is-ok' : 'is-primary'}`}>
                    {merging ? <RefreshCw className="animate-spin" /> : <GitMerge />} {merging ? 'Birleştiriliyor…' : 'Birleştir'}
                  </button>
                </span>
              </header>
              <div className="px-4 pt-2"><WordLegend texts={clusterTexts} colors={colors} /></div>
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-2 p-3 pt-2">
                <div className="rounded-xl bg-accent-soft/60 px-3 py-2.5 flex flex-col gap-1.5 min-w-0">
                  <span className="flex items-center gap-1.5 text-[12px] font-semibold text-accent">
                    <Layers className="w-3.5 h-3.5" /> Çapa soru
                    <span className="ml-auto font-normal text-ink-3">{anchor.options?.length || 0} şık</span>
                  </span>
                  <span className={`text-[13.5px] text-ink leading-relaxed ${open ? '' : 'line-clamp-3'}`}>
                    {stemOf(anchor) ? <Colored text={stemOf(anchor)} colors={colors} /> : 'Soru kökü henüz girilmemiş'}
                  </span>
                  {open && anchor.options && anchor.options.length > 0 && (
                    <span className="flex flex-col gap-0.5 pt-1.5 mt-1 border-t border-accent/15">
                      {anchor.options.map((o) => (
                        <span key={o.key} className="text-[12.5px] text-ink-2">
                          <b className="font-mono text-ink mr-1">{o.key}</b><Colored text={o.text} colors={colors} />
                        </span>
                      ))}
                    </span>
                  )}
                  <span className="pt-1"><DraftActions q={anchor} compact /></span>
                </div>
                <ul className={`list-none m-0 p-0 flex flex-col gap-1.5 ${open ? '' : 'max-h-[240px] overflow-y-auto'}`}>
                  {satellites.map((satQ) => {
                    const comp = cluster.satelliteDrafts.find((sd) => sd.question.id === satQ.id)?.compatibility;
                    return (
                      <li key={satQ.id} className="rounded-xl bg-canvas px-3 py-2 flex flex-col gap-1 min-w-0">
                        <div className="flex items-center gap-2 text-[12.5px] min-w-0 flex-wrap">
                          <span className="font-semibold text-ink truncate">{satQ.contributedByName || 'Anonim'}</span>
                          <span className="text-ink-3 shrink-0 font-mono">{numLabel(satQ)}</span>
                          {comp && <span className="ms-tag is-ok tabular-nums">%{comp.score}</span>}
                          <span className="ml-auto inline-flex items-center gap-1 shrink-0">
                            <button type="button" onClick={() => handleDetachSatellite(cluster.id, satQ.id)} title="Kümeden çıkar (yalnızca görünüm)" className="ms-btn is-sm is-ghost"><Split /> Çıkar</button>
                            <button type="button" onClick={() => handleMarkNotSame(anchor.id, satQ.id)} title="Farklı sorular; bir daha aynı kümede gösterme (kalıcı)" className="ms-btn is-sm is-danger"><X /> Aynı değil</button>
                          </span>
                        </div>
                        <span className={`text-[13px] text-ink-2 leading-snug ${open ? '' : 'line-clamp-2'}`}>
                          {stemOf(satQ) ? <Colored text={stemOf(satQ)} colors={colors} /> : 'Metin yok'}
                        </span>
                        {open && comp && comp.reasons.length > 0 && (
                          <span className="flex flex-wrap gap-1">
                            {comp.reasons.map((r, i) => <span key={i} className="ms-tag">{r}</span>)}
                          </span>
                        )}
                        {open && <span><DraftActions q={satQ} compact /></span>}
                      </li>
                    );
                  })}
                </ul>
              </div>
            </article>
          );
        })
      )}
      {editingDraft && (
        <AdminEditQuestionModal
          isOpen
          question={editingDraft}
          adminEmail={adminEmail}
          onClose={() => setEditingDraft(null)}
          onSaveQuestion={async (updated) => {
            await ApiService.adminUpdateQuestion(adminEmail, editingDraft.id, updated);
            setEditingDraft(null);
            notify('Taslak güncellendi.');
            await onRefreshData();
            await runAnalysis();
          }}
        />
      )}

      {optimizingQuestion && (
        <AiQuestionOptimizerModal
          question={optimizingQuestion}
          isOpen={Boolean(optimizingQuestion)}
          onClose={() => setOptimizingQuestion(null)}
          currentUser={{ email: adminEmail, displayName: adminName || 'Yönetici' } as any}
          onSaved={async () => {
            setOptimizingQuestion(null);
            notify('Taslak AI ile başarıyla geliştirildi.');
            await onRefreshData();
            await runAnalysis();
          }}
        />
      )}
    </div>
  );
};
