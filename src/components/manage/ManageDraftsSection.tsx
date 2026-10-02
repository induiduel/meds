import React, { useEffect, useMemo, useState } from 'react';
import {
  Layers,
  RefreshCw,
  GitMerge,
  Check,
  ChevronDown,
  Zap,
  Search,
  Eye,
  EyeOff,
  Undo2,
  Split,
  Trash2,
  Pencil,
  Sparkles,
} from 'lucide-react';
import type { QuestionItem, ClusterAnalysisSummary, DraftCluster } from '../../types';
import { ApiService } from '../../services/api';
import { AdminEditQuestionModal } from '../AdminEditQuestionModal';
import { sharedWordColors, Colored, WordLegend } from '../draftHighlight';
import {
  deleteDraftEverywhere,
  reconstructDraft,
} from '../../services/manageConsoleService';

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
  committeeName,
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
  const [reconstructingIds, setReconstructingIds] = useState<Set<string>>(new Set());
  const [deletingIds, setDeletingIds] = useState<Set<string>>(new Set());
  const [confirmBatch, setConfirmBatch] = useState(false);
  const [confirmBulkDelete, setConfirmBulkDelete] = useState(false);

  const runAnalysis = async () => {
    if (!committeeId) return;
    setLoading(true);
    try {
      const summary = await ApiService.getCommitteeDraftClusters(committeeId);
      setAnalysis(summary);
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Analiz sırasında hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void runAnalysis();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [committeeId, questions.length]);

  useEffect(() => {
    if (!confirmBatch) return;
    const t = window.setTimeout(() => setConfirmBatch(false), 4000);
    return () => window.clearTimeout(t);
  }, [confirmBatch]);

  useEffect(() => {
    if (!confirmBulkDelete) return;
    const t = window.setTimeout(() => setConfirmBulkDelete(false), 4000);
    return () => window.clearTimeout(t);
  }, [confirmBulkDelete]);

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
  const handleMergeCluster = async (cluster: DraftCluster) => {
    setMergingClusterId(cluster.id);
    try {
      const satelliteIds = cluster.satelliteDrafts.map((s) => s.question.id);
      await ApiService.mergeDraftCluster(adminEmail, cluster.anchorQuestion.id, satelliteIds, adminName || 'Yönetici');
      setLocallyMergedSatelliteIds((prev) => new Set([...prev, ...satelliteIds]));
      setSelectedDraftIds((prev) => prev.filter((id) => !satelliteIds.includes(id)));
      notify(`Soru #${cluster.anchorQuestion.questionNumber || 'Çapa'} için ${satelliteIds.length} taslak birleştirildi.`);
      await onRefreshData();
      await runAnalysis();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Birleştirme başarısız oldu.');
    } finally {
      setMergingClusterId(null);
    }
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
      setConfirmBulkDelete(false);
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
    const btn = 'h-8 px-2.5 rounded-[8px] border border-line bg-white text-[12.5px] font-medium text-ink-2 hover:text-ink inline-flex items-center gap-1 cursor-pointer disabled:opacity-50';
    return (
      <span className={`inline-flex items-center gap-1.5 ${compact ? '' : 'flex-wrap'}`} onClick={(e) => e.stopPropagation()}>
        <button type="button" onClick={() => setEditingDraft(q)} className={btn} title="Taslağı düzenle">
          <Pencil className="w-3.5 h-3.5" /><span>Düzenle</span>
        </button>
        <button type="button" onClick={() => { void handleReconstruct(q); }} disabled={isRec} className={btn} title="Yapay zekaya tam soruya dönüştür">
          {isRec ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
          <span>{isRec ? 'Dönüşüyor…' : 'AI Dönüştür'}</span>
        </button>
        <button type="button" onClick={() => { void handleDeleteDraft(q); }} disabled={isDel}
          className="h-8 px-2.5 rounded-[8px] border border-[#FDA29B] bg-[#FEF3F2] text-[#B4233C] text-[12.5px] font-semibold hover:bg-[#FEE4E2] inline-flex items-center gap-1 cursor-pointer disabled:opacity-50" title="Taslağı her yerden sil">
          {isDel ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Trash2 className="w-3.5 h-3.5" />}
          <span>{isDel ? 'Siliniyor…' : 'Sil'}</span>
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

  const stats = [
    { label: 'Taslak', value: analysis?.totalDrafts ?? '–', hint: 'öğrenci girdisi', dot: '#4A5868' },
    { label: 'Tahmini soru', value: analysis?.estimatedTrueQuestions ?? '–', hint: 'hedefe doğru', dot: '#1F9D55' },
    { label: 'Hazır küme', value: readyCount, hint: `${analysis?.potentialSavedDuplicates ?? 0} mükerrer`, dot: '#1E4FD8' },
    { label: 'Birleşik', value: mergedQuestions.length, hint: 'konsolide soru', dot: '#10B981' },
    { label: 'Muğlak', value: analysis?.vagueDraftsCount ?? '–', hint: 'eşleşme arıyor', dot: '#F59E0B' },
  ];

  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-col xl:flex-row xl:items-center gap-2">
        <div className="flex items-center gap-2.5 min-w-0 flex-1">
          <span className="w-10 h-10 rounded-[12px] bg-accent text-white flex items-center justify-center shrink-0">
            <Layers className="w-5 h-5" />
          </span>
          <div className="min-w-0">
            <h3 className="m-0 font-display font-bold text-[18px] tracking-[-0.02em]">Taslak atölyesi</h3>
            <p className="m-0 text-[13px] text-ink-3 truncate">{committeeName || 'Seçili kurul'} — topla, birleştir, sil, düzenle, AI ile dönüştür</p>
          </div>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <button type="button" onClick={() => { void runAnalysis(); }} disabled={loading}
            className="h-10 px-3.5 rounded-[10px] border border-line-2 text-[14px] font-semibold inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} /> Yeniden analiz
          </button>
          {readyCount > 0 && (
            <button type="button" disabled={isBatchMerging}
              onClick={() => (confirmBatch ? (setConfirmBatch(false), void handleBatchMergeReady()) : setConfirmBatch(true))}
              className={`h-10 px-3.5 rounded-[10px] text-[14px] font-semibold inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50 ${confirmBatch ? 'bg-[#B4233C] text-white' : 'bg-ok text-white hover:bg-[#126A35]'}`}>
              <Zap className="w-4 h-4" />{confirmBatch ? 'Emin misin? Birleştir' : `Hazır ${readyCount} kümeyi birleştir`}
            </button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
        {stats.map((s) => (
          <div key={s.label} className="rounded-[14px] bg-canvas px-3 py-2 flex flex-col">
            <span className="flex items-center gap-1.5 text-[12px] text-ink-2">
              <span className="w-2 h-2 rounded-full" style={{ background: s.dot }} aria-hidden="true" />{s.label}
            </span>
            <span className="flex items-baseline gap-1.5">
              <span className="font-mono text-[20px] font-semibold text-ink leading-tight">{s.value}</span>
              {s.hint && <span className="text-[12px] text-ink-3 truncate">{s.hint}</span>}
            </span>
          </div>
        ))}
      </div>

      <div className="flex items-center gap-2">
        <div role="tablist" aria-label="Taslak görünümü" className="flex gap-1 bg-canvas rounded-[12px] p-1 overflow-x-auto min-w-0">
          {tabs.map((t) => {
            const on = activeFilter === t.id;
            return (
              <button key={t.id} type="button" role="tab" aria-selected={on} onClick={() => setActiveFilter(t.id)}
                className={`shrink-0 h-8 px-3 rounded-[9px] text-[13.5px] whitespace-nowrap cursor-pointer inline-flex items-center gap-1.5 ${on ? 'bg-white text-ink font-semibold shadow' : 'text-ink-2 hover:text-ink'}`}>
                {t.id === 'manual' && <GitMerge className="w-3.5 h-3.5" />}{t.label}
                {t.count !== undefined && <span className={`font-mono text-[12px] ${on ? 'text-accent' : 'text-ink-3'}`}>{t.count}</span>}
              </button>
            );
          })}
        </div>
      </div>

      {loading ? (
        <div role="status" className="py-14 text-center text-[15px] font-semibold text-ink">Taslaklar taranıyor…</div>
      ) : activeFilter === 'merged' ? (
        <div className="flex flex-col gap-3">
          <p className="m-0 text-[13.5px] text-ink-2">Daha önce birleştirilmiş taslaklar. Parçaları inceleyebilir, hata varsa <strong className="text-ink">"Ayır (Geri Al)"</strong> ile eski hallerine döndürebilirsiniz.</p>
          {mergedQuestions.length === 0 && (
            <div className="rounded-xl border border-line px-4 py-10 text-center text-[14px] text-ink-2">Henüz birleştirilmiş soru yok. "Hazır" veya "Elle seç" sekmesinden birleştirebilirsiniz.</div>
          )}
          {mergedQuestions.map((q) => {
            const isInspecting = inspectingMergedId === q.id;
            const isUnmerging = unmergingQuestionId === q.id;
            const satelliteCount = q.mergedSatellites?.length || q.fragments?.filter((f) => f.text.includes('[Birleştirilen Taslak')).length || 0;
            return (
              <article key={q.id} className="rounded-[16px] bg-white border border-[#CDEBD8] overflow-hidden flex flex-col">
                <div className="flex items-center gap-3 px-4 py-3 bg-[#F6FEF9] border-b border-[#E1F6EB] flex-wrap">
                  <span className="w-9 h-9 rounded-[10px] bg-ok-soft text-ok font-mono text-[13px] font-bold flex items-center justify-center shrink-0">{numLabel(q)}</span>
                  <div className="flex-1 min-w-[200px]">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-ink text-[14.5px] truncate">{q.topic || q.discipline || 'Birleştirilmiş Soru'}</span>
                      <span className="h-5 px-2 rounded-full bg-ok text-white text-[11px] font-semibold inline-flex items-center gap-1 shrink-0">
                        <Layers className="w-3 h-3" />{satelliteCount > 0 ? `${satelliteCount + 1} taslak birleşik` : 'Birleşik'}
                      </span>
                    </div>
                    <span className="text-[12px] text-ink-3">{q.discipline} · {q.fragments?.length || 0} parça · {q.options?.length || 0} şık</span>
                  </div>
                  <div className="flex items-center gap-1.5 shrink-0 flex-wrap">
                    <DraftActions q={q} compact />
                    <button type="button" onClick={() => setInspectingMergedId(isInspecting ? null : q.id)}
                      className="h-8 px-2.5 rounded-[8px] border border-line bg-white text-[12.5px] font-medium text-ink-2 hover:text-ink inline-flex items-center gap-1 cursor-pointer">
                      {isInspecting ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}<span>{isInspecting ? 'Kapat' : 'İncele'}</span>
                    </button>
                    <button type="button" onClick={() => { void handleUnmergeQuestion(q.id); }} disabled={isUnmerging}
                      className="h-8 px-2.5 rounded-[8px] border border-[#FDA29B] bg-[#FEF3F2] text-[#B4233C] text-[12.5px] font-semibold hover:bg-[#FEE4E2] inline-flex items-center gap-1 cursor-pointer disabled:opacity-50">
                      {isUnmerging ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Undo2 className="w-3.5 h-3.5" />}
                      <span>{isUnmerging ? 'Ayrılıyor…' : 'Ayır (Geri Al)'}</span>
                    </button>
                  </div>
                </div>
                <div className="p-3.5 flex flex-col gap-2">
                  <p className="m-0 text-[14px] text-ink leading-relaxed">{stemOf(q) || 'Soru kökü henüz girilmemiş'}</p>
                  {isInspecting && q.mergedSatellites && q.mergedSatellites.length > 0 && (
                    <div className="flex flex-col gap-2 mt-1">
                      {q.mergedSatellites.map((sat, sIdx) => (
                        <div key={sat.id || sIdx} className="rounded-[10px] bg-canvas border border-line-soft p-2.5 text-[13px]">
                          <div className="font-semibold text-ink">Taslak #{sIdx + 1}: {sat.contributedByName || 'Anonim'}</div>
                          <p className="m-0 text-ink-2">{stemOf(sat) || 'Metin girilmemiş'}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </article>
            );
          })}
        </div>
      ) : activeFilter === 'manual' ? (
        <div className="flex flex-col gap-2.5">
          <p className="m-0 text-[13.5px] text-ink-2">Aynı soruya ait taslakları işaretleyin. Biri <strong className="text-ink">çapa</strong> olur; şıklar harmanlanır, mükerrerler temizlenir. <strong className="text-ink">Seçtiklerinizde ortak geçen kelimeler aynı renkle boyanır.</strong></p>
          {manualColors.size > 0 && <WordLegend texts={selectedQs.map(fullText)} colors={manualColors} />}
          <label className="flex items-center gap-2 h-11 px-3.5 rounded-[12px] bg-white border border-line focus-within:border-accent">
            <Search className="w-4 h-4 text-ink-3 shrink-0" />
            <span className="sr-only">Taslaklarda ara</span>
            <input type="search" placeholder="Metin, konu, ders ya da soru no ara" value={manualSearchQuery} onChange={(e) => setManualSearchQuery(e.target.value)}
              className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[15px] placeholder:text-[#7A8693]" />
            <span className="text-[12.5px] text-ink-3 shrink-0">{manualFilteredQuestions.length}</span>
          </label>
          <ul className="list-none m-0 p-0 flex flex-col gap-1.5">
            {manualFilteredQuestions.map((q) => {
              const on = selectedDraftIds.includes(q.id);
              const isAnchor = on && manualAnchorId === q.id;
              return (
                <li key={q.id} className={`rounded-[14px] border px-3 py-2.5 flex items-start gap-3 ${on ? 'bg-accent-soft/60 border-accent/40' : 'bg-white border-line'}`}>
                  <button type="button" role="checkbox" aria-checked={on} onClick={() => toggleSelectDraft(q.id)} aria-label="Taslağı seç"
                    className={`mt-0.5 w-5 h-5 rounded-[6px] flex items-center justify-center shrink-0 cursor-pointer ${on ? 'bg-accent text-white' : 'bg-white border border-line-2'}`}>
                    {on && <Check className="w-3.5 h-3.5" strokeWidth={3} />}
                  </button>
                  <span className="flex-1 min-w-0 flex flex-col gap-1">
                    <span className="flex items-center gap-2 min-w-0 text-[12.5px] text-ink-3">
                      <span className="font-mono font-semibold text-ink">{numLabel(q)}</span>
                      <span className="truncate">{q.discipline}{q.topic ? ` · ${q.topic}` : ''}</span>
                      {isAnchor && <span className="ml-auto shrink-0 h-5 px-2 rounded-full bg-accent text-white text-[11px] font-semibold inline-flex items-center">Çapa</span>}
                    </span>
                    <span className="text-[14px] text-ink leading-snug">
                      {stemOf(q) ? <Colored text={stemOf(q)} colors={manualColors} /> : 'Metin girilmemiş'}
                    </span>
                    {q.options && q.options.length > 0 && (
                      <span className="flex flex-wrap gap-1">
                        {q.options.map((o) => (
                          <span key={o.key} className="max-w-[260px] truncate h-6 px-2 rounded-[7px] bg-canvas text-[12px] text-ink-2 inline-flex items-center">
                            <strong className="font-mono mr-1">{o.key}</strong><Colored text={o.text} colors={manualColors} />
                          </span>
                        ))}
                      </span>
                    )}
                    <span className="mt-1"><DraftActions q={q} compact /></span>
                  </span>
                </li>
              );
            })}
          </ul>
          {selectedDraftIds.length > 0 && (
            <div className="sticky bottom-0 flex items-center gap-2 px-3 py-2.5 rounded-[14px] bg-ink text-white shadow-lg flex-wrap">
              <span className="text-[13.5px] shrink-0"><strong>{selectedDraftIds.length}</strong> seçili</span>
              {selectedDraftIds.length >= 2 && (
                <label className="relative min-w-0 flex-1 sm:flex-none sm:w-[280px]">
                  <span className="sr-only">Çapa soru</span>
                  <select value={manualAnchorId} onChange={(e) => setManualAnchorId(e.target.value)}
                    className="appearance-none w-full h-10 rounded-[11px] bg-white/10 border border-white/20 pl-3 pr-8 text-[13.5px] cursor-pointer truncate">
                    {selectedDraftIds.map((id) => {
                      const q = committeeQuestions.find((x) => x.id === id);
                      return <option key={id} value={id} className="text-black">Çapa: {q ? numLabel(q) : '?'} · {q?.topic || q?.discipline}</option>;
                    })}
                  </select>
                  <ChevronDown className="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 w-4 h-4 opacity-70" />
                </label>
              )}
              <button type="button" onClick={() => { setSelectedDraftIds([]); setManualAnchorId(''); }}
                className="h-10 px-3 rounded-[11px] text-[13.5px] font-semibold hover:bg-white/10 cursor-pointer">Temizle</button>
              <button type="button" onClick={() => { void handleManualMergeSelected(); }} disabled={isManualMerging || selectedDraftIds.length < 2}
                className="h-10 px-4 rounded-[11px] bg-accent hover:bg-accent-hover text-white text-[14px] font-semibold inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50 shrink-0">
                {isManualMerging ? <RefreshCw className="w-4 h-4 animate-spin" /> : <GitMerge className="w-4 h-4" />}
                {selectedDraftIds.length < 2 ? 'En az 2 seç' : 'Birleştir'}
              </button>
              <button type="button"
                onClick={() => (confirmBulkDelete ? void handleBulkDeleteSelected() : setConfirmBulkDelete(true))}
                disabled={isBulkDeleting}
                className={`h-10 px-4 rounded-[11px] text-[14px] font-semibold inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50 shrink-0 ${confirmBulkDelete ? 'bg-[#B4233C] text-white' : 'bg-white/10 hover:bg-white/20'}`}>
                {isBulkDeleting ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Trash2 className="w-4 h-4" />}
                {confirmBulkDelete ? 'Emin misin? Sil' : 'Seçilenleri sil'}
              </button>
            </div>
          )}
        </div>
      ) : activeFilter === 'vague' ? (
        <div className="flex flex-col gap-2">
          <p className="m-0 text-[13.5px] text-ink-2">Bu taslaklarda henüz güçlü bir eşleşme için yeterli bilgi yok. Yeni ipucu ya da şık geldikçe otomatik bağlanırlar.</p>
          {!analysis?.unmatchedVagueDrafts.length ? (
            <div className="rounded-xl border border-line px-4 py-10 text-center text-[14px] text-ink-2">Muğlak taslak yok.</div>
          ) : (
            analysis.unmatchedVagueDrafts.map((q) => (
              <div key={q.id} className="rounded-[14px] bg-white border border-line px-3.5 py-2.5 flex flex-col gap-1.5">
                <span className="flex items-center gap-2 text-[12.5px] text-ink-3 min-w-0">
                  <span className="font-mono font-semibold text-ink">{numLabel(q)}</span>
                  <span className="truncate">{q.discipline}{q.topic ? ` · ${q.topic}` : ''}</span>
                </span>
                <span className="text-[14px] text-ink leading-snug">{stemOf(q) || 'Metin girilmemiş'}</span>
                <span><DraftActions q={q} compact /></span>
              </div>
            ))
          )}
        </div>
      ) : filteredClusters.length === 0 ? (
        <div className="rounded-xl border border-line px-4 py-10 text-center flex flex-col items-center gap-3">
          <p className="m-0 text-[15px] font-semibold">Bu sekmede küme yok</p>
          <p className="m-0 text-[14px] text-ink-2">Taslakları kendin birleştirmek istersen elle seçebilirsin.</p>
          <button type="button" onClick={() => setActiveFilter('manual')} className="h-10 px-4 rounded-[10px] bg-accent text-white text-[14px] font-semibold cursor-pointer">Elle seçime geç</button>
        </div>
      ) : (
        filteredClusters.map((cluster) => {
          const anchor = cluster.anchorQuestion;
          const open = expandedClusterId === cluster.id;
          const merging = mergingClusterId === cluster.id;
          const ready = cluster.status === 'ready_to_merge';
          const clusterTexts = [anchor, ...cluster.satelliteDrafts.map((sd) => sd.question)].map(fullText);
          const colors = sharedWordColors(clusterTexts);
          return (
            <article key={cluster.id} className={`rounded-[18px] bg-white border overflow-hidden ${ready ? 'border-[#CDEBD8]' : 'border-line'}`}>
              <div className="flex items-center gap-3 px-3.5 py-3 flex-wrap">
                <span className={`w-10 h-10 rounded-[12px] flex items-center justify-center shrink-0 font-mono text-[13px] font-semibold ${ready ? 'bg-ok-soft text-ok' : 'bg-warn-soft text-warn'}`}>
                  {anchor.isUnassignedNumber || !anchor.questionNumber ? '?' : anchor.questionNumber}
                </span>
                <span className="flex-1 min-w-[220px] flex flex-col">
                  <span className="flex items-center gap-2 min-w-0">
                    <span className="text-[14.5px] font-semibold text-ink truncate">{cluster.detectedSubject || anchor.topic || anchor.discipline}</span>
                    <span className={`shrink-0 h-5 px-1.5 rounded-full text-[11.5px] font-mono font-semibold inline-flex items-center ${ready ? 'bg-ok-soft text-ok' : 'bg-warn-soft text-warn'}`}>%{cluster.overallConfidence}</span>
                  </span>
                  <span className="text-[12.5px] text-ink-3 truncate">{anchor.discipline} · {cluster.satelliteDrafts.length} taslak birleşecek</span>
                  <span className="mt-1"><WordLegend texts={clusterTexts} colors={colors} /></span>
                </span>
                <button type="button" onClick={() => handleDissolveCluster(cluster.id)} title="Bu kümeyi dağıt (yalnızca görünüm)"
                  className="h-9 px-2.5 rounded-[10px] border border-line bg-white text-[12px] font-medium text-ink-2 hover:text-[#B4233C] items-center gap-1 cursor-pointer hidden sm:inline-flex">
                  <Split className="w-3.5 h-3.5" /><span>Kümeyi Dağıt</span>
                </button>
                <button type="button" onClick={() => setExpandedClusterId(open ? null : cluster.id)} aria-expanded={open}
                  className="h-9 px-3 rounded-[10px] border border-line bg-white text-[13px] font-semibold text-ink-2 items-center gap-1 cursor-pointer hover:border-line-2 hidden sm:inline-flex">
                  Karşılaştır<ChevronDown className={`w-4 h-4 transition-transform ${open ? 'rotate-180' : ''}`} />
                </button>
                <button type="button" onClick={() => { void handleMergeCluster(cluster); }} disabled={merging || busy}
                  className={`h-9 px-3 rounded-[10px] text-[13px] font-semibold text-white inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50 ${ready ? 'bg-ok hover:bg-[#126A35]' : 'bg-ink hover:bg-[#1B2B3B]'}`}>
                  {merging ? <RefreshCw className="w-4 h-4 animate-spin" /> : <GitMerge className="w-4 h-4" />}
                  <span>{merging ? 'Birleştiriliyor…' : 'Birleştir'}</span>
                </button>
              </div>

              <div className="grid grid-cols-1 xl:grid-cols-[minmax(0,1fr)_minmax(0,1fr)] gap-2 px-3.5 pb-3.5">
                <div className="rounded-[14px] bg-canvas px-3 py-2.5 flex flex-col gap-1.5">
                  <span className="flex items-center gap-1.5 text-[12px] font-semibold text-accent">
                    <Layers className="w-3.5 h-3.5" />Çapa soru
                    <span className="ml-auto font-normal text-ink-3">{anchor.options?.length || 0} şık</span>
                  </span>
                  <span className={`text-[13.5px] text-ink leading-relaxed ${open ? '' : 'line-clamp-3'}`}>
                    {stemOf(anchor) ? <Colored text={stemOf(anchor)} colors={colors} /> : 'Soru kökü henüz girilmemiş'}
                  </span>
                  {open && anchor.options && anchor.options.length > 0 && (
                    <span className="flex flex-col gap-0.5 pt-1 border-t border-line-soft mt-1">
                      {anchor.options.map((o) => (
                        <span key={o.key} className="text-[12.5px] text-ink-2">
                          <strong className="font-mono text-ink mr-1">{o.key})</strong><Colored text={o.text} colors={colors} />
                        </span>
                      ))}
                    </span>
                  )}
                  <span className="pt-1"><DraftActions q={anchor} compact /></span>
                </div>
                <ul className={`list-none m-0 p-0 flex flex-col gap-1.5 ${open ? '' : 'max-h-[220px] overflow-y-auto'}`}>
                  {cluster.satelliteDrafts.map((sat, idx) => (
                    <li key={sat.question.id || idx} className="rounded-[12px] border border-line-soft px-3 py-2 flex flex-col gap-1">
                      <div className="flex items-center gap-2 text-[12.5px] min-w-0 flex-wrap">
                        <span className="font-semibold text-ink truncate">{sat.question.contributedByName || 'Anonim'}</span>
                        <span className="text-ink-3 shrink-0">· {numLabel(sat.question)}</span>
                        <span className="shrink-0 font-mono text-[12px] font-semibold text-ok">%{sat.compatibility.score}</span>
                        <button type="button" onClick={() => handleDetachSatellite(cluster.id, sat.question.id)} title="Bu taslağı kümeden çıkar (yalnızca görünüm)"
                          className="ml-auto text-[11.5px] px-2 py-0.5 rounded-[6px] text-ink-3 hover:text-[#B4233C] hover:bg-[#FEE4E2] border border-line-soft cursor-pointer inline-flex items-center gap-1 shrink-0">
                          <Split className="w-3 h-3" /><span>Ayır</span>
                        </button>
                      </div>
                      <span className={`text-[13px] text-ink-2 leading-snug ${open ? '' : 'line-clamp-2'}`}>
                        {stemOf(sat.question) ? <Colored text={stemOf(sat.question)} colors={colors} /> : 'Metin'}
                      </span>
                      {open && sat.compatibility.reasons.length > 0 && (
                        <span className="flex flex-wrap gap-1">
                          {sat.compatibility.reasons.map((r, i) => (
                            <span key={i} className="px-2 py-0.5 rounded-[7px] bg-canvas text-[11.5px] text-ink-2">{r}</span>
                          ))}
                        </span>
                      )}
                      <span><DraftActions q={sat.question} compact /></span>
                    </li>
                  ))}
                </ul>
              </div>
              <button type="button" onClick={() => setExpandedClusterId(open ? null : cluster.id)}
                className="sm:hidden w-full h-10 border-t border-line-soft text-[13px] font-semibold text-ink-2 inline-flex items-center justify-center gap-1 cursor-pointer">
                {open ? 'Daha az' : 'Karşılaştır'}<ChevronDown className={`w-4 h-4 transition-transform ${open ? 'rotate-180' : ''}`} />
              </button>
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
    </div>
  );
};
