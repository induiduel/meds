import React, { useEffect, useMemo, useState } from 'react';
import {
  Layers,
  RefreshCw,
  GitMerge,
  Check,
  Zap,
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
import { Seg, EmptyState, ConfirmButton, Drawer } from './consoleUi';
import { Card14, DataTable, DetailLayout, DetailNav, FactList, PageActions, Pill, SearchField, StatRow, Tabs14, Toolbar, type Col } from '../v14/pageKit';
import { BulkBar, useSelection } from '../v14/manageKit';

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
  const [locallyMergedSatelliteIds, setLocallyMergedSatelliteIds] = useState<Set<string>>(new Set());
  const [unmergingQuestionId, setUnmergingQuestionId] = useState<string | null>(null);
  const [ara, setAra] = useState('');
  const [acikKumeId, setAcikKumeId] = useState<string | null>(null);
  const [acikBirlesikId, setAcikBirlesikId] = useState<string | null>(null);
  const [acikTaslak, setAcikTaslak] = useState<{ id: string; liste: 'manual' | 'vague' } | null>(null);
  const [topluBusy, setTopluBusy] = useState(false);
  const kumeSecim = useSelection<string>();
  const birlesikSecim = useSelection<string>();
  const muglakSecim = useSelection<string>();
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

  const araEs = (q: QuestionItem) => {
    const t = ara.trim().toLocaleLowerCase('tr');
    return !t || `${fullText(q)} ${q.discipline || ''} ${q.topic || ''} ${q.questionNumber ?? ''}`.toLocaleLowerCase('tr').includes(t);
  };
  const filteredClusters = useMemo(() => {
    if (!analysis) return [];
    const f =
      activeFilter === 'all' ? analysis.clusters
      : activeFilter === 'ready' ? analysis.clusters.filter((c) => c.status === 'ready_to_merge')
      : activeFilter === 'review' ? analysis.clusters.filter((c) => c.status === 'needs_review')
      : [];
    const t = ara.trim().toLocaleLowerCase('tr');
    return t ? f.filter((c) => (c.detectedSubject || '').toLocaleLowerCase('tr').includes(t) || [c.anchorQuestion, ...c.satelliteDrafts.map((s) => s.question)].some(araEs)) : f;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [analysis, activeFilter, ara]);
  const gorunenBirlesik = mergedQuestions.filter(araEs);
  const gorunenMuglak = (analysis?.unmatchedVagueDrafts || []).filter(araEs);

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

  // ---------- toplu işlemler (tek öge uçları sırayla) ----------
  const topluCalistir = async <T,>(hedef: T[], fn: (x: T) => Promise<boolean>, ad: string) => {
    if (!hedef.length) return { ok: 0, err: 0 };
    setTopluBusy(true);
    let ok = 0, err = 0;
    try {
      for (const x of hedef) {
        try {
          if (await fn(x)) ok++; else err++;
        } catch {
          err++;
        }
      }
      notify(`${ad}: ${ok} başarılı, ${err} hata.`);
      if (ok > 0) {
        await onRefreshData();
        await runAnalysis();
      }
    } finally {
      setTopluBusy(false);
    }
    return { ok, err };
  };

  const topluKumeBirlestir = async () => {
    const hedef = filteredClusters.filter((c) => kumeSecim.has(c.id));
    const { err } = await topluCalistir(hedef, async (cluster) => {
      const anchor = effectiveAnchorOf(cluster);
      const satelliteIds = [cluster.anchorQuestion, ...cluster.satelliteDrafts.map((s) => s.question)].map((q) => q.id).filter((id) => id !== anchor.id);
      await ApiService.mergeDraftCluster(adminEmail, anchor.id, satelliteIds, adminName || 'Yönetici');
      setLocallyMergedSatelliteIds((prev) => new Set([...prev, ...satelliteIds]));
      return true;
    }, 'Küme birleştirme');
    if (!err) kumeSecim.clear();
  };
  const topluKumeDagit = () => {
    const ids = filteredClusters.filter((c) => kumeSecim.has(c.id)).map((c) => c.id);
    setAnalysis((prev) => {
      if (!prev) return null;
      const detached = prev.clusters.filter((c) => ids.includes(c.id)).reduce((n, c) => n + c.satelliteDrafts.length + 1, 0);
      const nextClusters = prev.clusters.filter((c) => !ids.includes(c.id));
      return { ...prev, clusters: nextClusters, mergeableClustersCount: nextClusters.length, vagueDraftsCount: prev.vagueDraftsCount + detached };
    });
    notify(`${ids.length} küme dağıtıldı (yalnızca görünüm).`);
    kumeSecim.clear();
  };
  const topluAyir = async () => {
    const hedef = gorunenBirlesik.filter((q) => birlesikSecim.has(q.id));
    const { err } = await topluCalistir(hedef, async (q) => {
      const res = await ApiService.unmergeDraftCluster(adminEmail, q.id, adminName || 'Yönetici');
      setLocallyMergedSatelliteIds((prev) => {
        const next = new Set(prev);
        res.restoredSatellites.forEach((s) => next.delete(s.id));
        return next;
      });
      return true;
    }, 'Ayırma');
    if (!err) birlesikSecim.clear();
  };
  const topluSil = async (hedef: QuestionItem[], temizle: () => void) => {
    const { err } = await topluCalistir(hedef, async (q) => (await deleteDraftEverywhere(adminEmail, q)).ok, 'Silme');
    if (!err) temizle();
  };
  const topluDonustur = async () => {
    const hedef = gorunenMuglak.filter((q) => muglakSecim.has(q.id));
    const { err } = await topluCalistir(hedef, async (q) => (await reconstructDraft(q)).ok, 'AI dönüştürme');
    if (!err) muglakSecim.clear();
  };

  // ---------- satır eylemleri ----------
  const DraftActions: React.FC<{ q: QuestionItem; compact?: boolean }> = ({ q }) => {
    const isRec = reconstructingIds.has(q.id);
    const isDel = deletingIds.has(q.id);
    return (
      <span className="inline-flex flex-wrap items-center gap-1" onClick={(e) => e.stopPropagation()}>
        <button type="button" onClick={() => setEditingDraft(q)} className="m14-btn ghost" title="Taslağı düzenle">
          <Pencil aria-hidden="true" /> Düzenle
        </button>
        <button type="button" onClick={() => setOptimizingQuestion(q)} className="m14-btn" title="Amfi slaytlarıyla tam soruya geliştir (önizlemeli)">
          <Wand2 aria-hidden="true" /> AI ile geliştir
        </button>
        <button type="button" onClick={() => { void handleReconstruct(q); }} disabled={isRec} className="m14-btn ghost" title="Doğrudan tam soruya dönüştür">
          {isRec ? <RefreshCw className="animate-spin" aria-hidden="true" /> : <Sparkles aria-hidden="true" />} {isRec ? 'Dönüşüyor…' : 'AI dönüştür'}
        </button>
        <button type="button" onClick={() => { void handleDeleteDraft(q); }} disabled={isDel} className="m14-btn danger" title="Taslağı her yerden sil">
          {isDel ? <RefreshCw className="animate-spin" aria-hidden="true" /> : <Trash2 aria-hidden="true" />} {isDel ? 'Siliniyor…' : 'Sil'}
        </button>
      </span>
    );
  };

  const tabs: { id: Filter; label: string; count?: number }[] = [
    { id: 'ready', label: 'Hazır', count: readyCount },
    { id: 'review', label: 'İncele', count: reviewCount },
    { id: 'all', label: 'Tüm kümeler', count: analysis?.clusters.length || 0 },
    { id: 'manual', label: 'Tek taslaklar · elle seç', count: manualFilteredQuestions.length },
    { id: 'vague', label: 'Muğlak', count: analysis?.vagueDraftsCount || 0 },
    { id: 'merged', label: 'Birleştirilmiş', count: mergedQuestions.length },
  ];

  const draftCols: Col<QuestionItem>[] = [
    { key: 'k', label: 'Taslak', main: true, render: (q) => stemOf(q) || <span className="text-ink-3">Metin girilmemiş</span> },
    { key: 'n', label: 'No', mono: true, render: (q) => numLabel(q) },
    { key: 'd', label: 'Ders · konu', muted: true, render: (q) => [q.discipline, q.topic].filter(Boolean).join(' · ') || '—' },
    { key: 'o', label: 'Şık', right: true, render: (q) => q.options?.length || 0 },
    { key: 'p', label: 'Parça', right: true, render: (q) => q.fragments?.length || 0 },
    { key: 'a', label: 'Ekleyen', muted: true, render: (q) => q.contributedByName || q.author || '—' },
  ];
  const manuelCols: Col<QuestionItem>[] = [
    draftCols[0],
    { key: 'c', label: 'Çapa', render: (q) => (selectedDraftIds.includes(q.id) && manualAnchorId === q.id ? <Pill tone="acc">Çapa</Pill> : '') },
    ...draftCols.slice(1),
  ];
  const kumeCols: Col<DraftCluster>[] = [
    { key: 'k', label: 'Küme', main: true, render: (c) => { const a = effectiveAnchorOf(c); return c.detectedSubject || stemOf(a) || a.topic || a.discipline; } },
    { key: 'g', label: 'Güven', render: (c) => <Pill tone={c.status === 'ready_to_merge' ? 'ok' : 'warn'}>%{c.overallConfidence}</Pill> },
    { key: 'u', label: 'Üye', right: true, render: (c) => c.satelliteDrafts.length + 1 },
    { key: 'n', label: 'No', mono: true, render: (c) => numLabel(effectiveAnchorOf(c)) },
    { key: 'd', label: 'Ders', muted: true, render: (c) => effectiveAnchorOf(c).discipline || '—' },
  ];
  const birlesikCols: Col<QuestionItem>[] = [
    { key: 'k', label: 'Birleşik soru', main: true, render: (q) => stemOf(q) || q.topic || q.discipline || 'Birleştirilmiş soru' },
    { key: 'n', label: 'No', mono: true, render: (q) => numLabel(q) },
    { key: 't', label: 'Taslak', right: true, render: (q) => { const n = q.mergedSatellites?.length || q.fragments?.filter((f) => f.text.includes('[Birleştirilen Taslak')).length || 0; return n > 0 ? n + 1 : '—'; } },
    { key: 'd', label: 'Ders', muted: true, render: (q) => q.discipline || '—' },
    { key: 'p', label: 'Parça', right: true, render: (q) => q.fragments?.length || 0 },
    { key: 'o', label: 'Şık', right: true, render: (q) => q.options?.length || 0 },
  ];

  // Elle seçim: DataTable seçimini selectedDraftIds + çapa mantığına bağlar
  const manuelSecim = {
    has: (id: string) => selectedDraftIds.includes(id),
    toggle: (id: string) => toggleSelectDraft(id),
    toggleAll: (ids: string[]) => {
      const all = ids.length > 0 && ids.every((id) => selectedDraftIds.includes(id));
      const next = all ? selectedDraftIds.filter((id) => !ids.includes(id)) : [...selectedDraftIds, ...ids.filter((id) => !selectedDraftIds.includes(id))];
      setSelectedDraftIds(next);
      if (!next.includes(manualAnchorId)) setManualAnchorId(next[0] || '');
    },
    allOf: (ids: string[]) => ids.length > 0 && ids.every((id) => selectedDraftIds.includes(id)),
    someOf: (ids: string[]) => ids.some((id) => selectedDraftIds.includes(id)),
  };

  const isCluster = activeFilter === 'ready' || activeFilter === 'review' || activeFilter === 'all';
  const acikKume = acikKumeId ? analysis?.clusters.find((c) => c.id === acikKumeId) || null : null;
  const acikBirlesik = acikBirlesikId ? mergedQuestions.find((q) => q.id === acikBirlesikId) || null : null;
  const taslakListe = acikTaslak?.liste === 'vague' ? gorunenMuglak : manualFilteredQuestions;
  const acikTaslakQ = acikTaslak ? taslakListe.find((q) => q.id === acikTaslak.id) || committeeQuestions.find((q) => q.id === acikTaslak.id) || null : null;

  const kumeAyrinti = (cluster: DraftCluster) => {
    const anchor = effectiveAnchorOf(cluster);
    const members = [cluster.anchorQuestion, ...cluster.satelliteDrafts.map((sd) => sd.question)];
    const satellites = members.filter((q) => q.id !== anchor.id);
    const clusterTexts = members.map(fullText);
    const colors = sharedWordColors(clusterTexts);
    return (
      <div className="flex flex-col gap-3">
        <div className="flex flex-wrap items-center gap-2">
          <Pill tone={cluster.status === 'ready_to_merge' ? 'ok' : 'warn'}>Güven %{cluster.overallConfidence}</Pill>
          <span className="text-sm text-ink-3">{anchor.discipline} · {satellites.length} taslak birleşecek</span>
          <label className="inline-flex items-center gap-1.5 text-sm text-ink-3 ml-auto max-w-full">
            Çapa
            <select value={anchor.id} onChange={(e) => setAnchorOverrides((prev) => ({ ...prev, [cluster.id]: e.target.value }))} className="pk14-sel" title="Birleşince ana soru olacak taslak">
              {members.map((m) => (
                <option key={m.id} value={m.id}>{numLabel(m)} · {(m.topic || m.discipline || '').slice(0, 40)}</option>
              ))}
            </select>
          </label>
        </div>
        <WordLegend texts={clusterTexts} colors={colors} />
        <DetailLayout
          main={
            <Card14 title={<span className="inline-flex items-center gap-1.5"><Layers className="w-4 h-4" aria-hidden="true" /> Çapa soru · {anchor.options?.length || 0} şık</span>} tools={<DraftActions q={anchor} />}>
              <p className="m-0 text-base text-ink leading-relaxed break-words">{stemOf(anchor) ? <Colored text={stemOf(anchor)} colors={colors} /> : 'Soru kökü henüz girilmemiş'}</p>
              {anchor.options && anchor.options.length > 0 && (
                <span className="flex flex-col gap-0.5 pt-2 mt-2 border-t border-line">
                  {anchor.options.map((o) => (
                    <span key={o.key} className="text-sm text-ink-2 break-words"><b className="font-mono text-ink mr-1">{o.key}</b><Colored text={o.text} colors={colors} /></span>
                  ))}
                </span>
              )}
            </Card14>
          }
          side={
            <ul className="list-none m-0 p-0 flex flex-col gap-2">
              {satellites.map((satQ) => {
                const comp = cluster.satelliteDrafts.find((sd) => sd.question.id === satQ.id)?.compatibility;
                return (
                  <li key={satQ.id} className="pk14-card" style={{ padding: '10px 12px' }}>
                    <div className="flex items-center gap-2 text-sm min-w-0 flex-wrap">
                      <span className="font-semibold text-ink truncate">{satQ.contributedByName || 'Anonim'}</span>
                      <span className="text-ink-3 shrink-0 font-mono">{numLabel(satQ)}</span>
                      {comp && <Pill tone="ok">%{comp.score}</Pill>}
                    </div>
                    <p className="m-0 mt-1 text-sm text-ink-2 leading-snug break-words">{stemOf(satQ) ? <Colored text={stemOf(satQ)} colors={colors} /> : 'Metin yok'}</p>
                    {comp && comp.reasons.length > 0 && (
                      <span className="flex flex-wrap gap-1 mt-1">{comp.reasons.map((r, i) => <Pill key={i}>{r}</Pill>)}</span>
                    )}
                    <div className="flex flex-wrap gap-1 mt-2">
                      <button type="button" onClick={() => handleDetachSatellite(cluster.id, satQ.id)} title="Kümeden çıkar (yalnızca görünüm)" className="m14-btn ghost"><Split aria-hidden="true" /> Çıkar</button>
                      <button type="button" onClick={() => handleMarkNotSame(anchor.id, satQ.id)} title="Farklı sorular; bir daha aynı kümede gösterme (kalıcı)" className="m14-btn danger"><X aria-hidden="true" /> Aynı değil</button>
                    </div>
                    <div className="mt-1"><DraftActions q={satQ} /></div>
                  </li>
                );
              })}
            </ul>
          }
        />
      </div>
    );
  };

  const birlesikAyrinti = (q: QuestionItem) => (
    <div className="flex flex-col gap-3">
      <Card14 title={q.topic || q.discipline || 'Birleştirilmiş soru'}>
        <p className="m-0 text-base text-ink leading-relaxed break-words">{stemOf(q) || <span className="text-ink-3">Soru kökü henüz girilmemiş</span>}</p>
        <p className="m-0 mt-2 text-sm text-ink-3">{[q.discipline, `${q.fragments?.length || 0} parça`, `${q.options?.length || 0} şık`].filter(Boolean).join(' · ')}</p>
      </Card14>
      {q.mergedSatellites && q.mergedSatellites.length > 0 ? (
        q.mergedSatellites.map((sat, sIdx) => (
          <div key={sat.id || sIdx} className="pk14-card flex flex-col gap-1.5 text-sm" style={{ padding: 12 }}>
            <div className="flex items-center justify-between gap-2">
              <span className="font-semibold text-ink">{sat.contributedByName || sat.author || 'Anonim'}</span>
              <span className="text-xs text-ink-3 font-mono">{numLabel(sat)}</span>
            </div>
            <p className="m-0 text-ink-2 leading-relaxed break-words">{stemOf(sat) || 'Metin girilmemiş'}</p>
            {sat.fragments && sat.fragments.length > 0 && (
              <ul className="m-0 p-0 list-none flex flex-col gap-0.5">
                {sat.fragments.map((sf) => (
                  <li key={sf.id} className="text-sm text-ink-3 break-words"><b className="font-medium text-ink-2">{sf.author}:</b> “{sf.text}”</li>
                ))}
              </ul>
            )}
            {sat.options && sat.options.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {sat.options.map((opt) => (
                  <span key={opt.key} className="m14-pill" style={{ whiteSpace: 'normal', height: 'auto' }}><b className="font-mono">{opt.key}</b> {opt.text}</span>
                ))}
              </div>
            )}
          </div>
        ))
      ) : (
        <p className="text-sm text-ink-3">Birleşen taslak kaydı yok.</p>
      )}
    </div>
  );

  const taslakAyrinti = (q: QuestionItem) => (
    <DetailLayout
      main={
        <Card14 title="Soru kökü">
          <p className="m-0 text-base text-ink leading-relaxed break-words">{stemOf(q) || <span className="text-ink-3">Metin girilmemiş</span>}</p>
          {q.options && q.options.length > 0 && (
            <span className="flex flex-col gap-0.5 pt-2 mt-2 border-t border-line">
              {q.options.map((o) => <span key={o.key} className="text-sm text-ink-2 break-words"><b className="font-mono text-ink mr-1">{o.key}</b><Colored text={o.text} colors={manualColors} /></span>)}
            </span>
          )}
          {q.fragments && q.fragments.length > 0 && (
            <ul className="m-0 mt-2 p-0 list-none flex flex-col gap-0.5">
              {q.fragments.map((f) => <li key={f.id} className="text-sm text-ink-3 break-words"><b className="font-medium text-ink-2">{f.author}:</b> “{f.text}”</li>)}
            </ul>
          )}
        </Card14>
      }
      side={
        <FactList items={[
          { k: 'No', v: numLabel(q) },
          { k: 'Ders', v: q.discipline || '—' },
          { k: 'Konu', v: q.topic || '—' },
          { k: 'Ekleyen', v: q.contributedByName || q.author || '—' },
          { k: 'Kimlik', v: <span className="font-mono text-xs">{q.id}</span> },
        ]} />
      }
    />
  );

  const sonrakiKume = (c: DraftCluster) => {
    const i = filteredClusters.findIndex((x) => x.id === c.id);
    const n = filteredClusters[i + 1];
    setAcikKumeId(n ? n.id : null);
  };

  return (
    <div className="flex flex-col gap-4 min-w-0">
      <PageActions>
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
          <button type="button" onClick={handleClearBlocked} title="“Aynı değil” engellerini temizle" className="m14-btn ghost">
            <X aria-hidden="true" /> {blockedCount} engel
          </button>
        )}
        <button type="button" onClick={() => { void runAnalysis(); }} disabled={loading} className="m14-btn">
          <RefreshCw className={loading ? 'animate-spin' : ''} aria-hidden="true" /> Yeniden analiz
        </button>
        {readyCount > 0 && (
          <ConfirmButton icon={Zap} className="m14-btn primary" confirmLabel={`Emin misin? ${readyCount} küme`} busy={isBatchMerging} busyLabel="Birleştiriliyor…" onConfirm={() => handleBatchMergeReady()}>
            Yüksek güvenli {readyCount} kümeyi birleştir
          </ConfirmButton>
        )}
      </PageActions>

      <StatRow
        stats={[
          { label: 'Taslak', value: analysis?.totalDrafts ?? '–', onClick: () => setActiveFilter('manual') },
          { label: 'Tahmini soru', value: analysis?.estimatedTrueQuestions ?? '–', tone: 'ok' },
          { label: `Otomatik birleşebilir (${analysis?.potentialSavedDuplicates ?? 0} mükerrer)`, value: readyCount, tone: 'ok', onClick: () => setActiveFilter('ready') },
          { label: 'Birleşik', value: mergedQuestions.length, onClick: () => setActiveFilter('merged') },
          { label: 'Muğlak', value: analysis?.vagueDraftsCount ?? '–', tone: 'warn', onClick: () => setActiveFilter('vague') },
        ]}
      />

      <Toolbar>
        <Tabs14<Filter> label="Taslak görünümü" value={activeFilter} onChange={setActiveFilter} options={tabs.map((t) => ({ id: t.id, label: t.label, n: t.count }))} />
        <SearchField
          value={activeFilter === 'manual' ? manualSearchQuery : ara}
          onChange={activeFilter === 'manual' ? setManualSearchQuery : setAra}
          placeholder={activeFilter === 'manual' ? 'Metin, konu, ders ya da soru no' : 'Taslak ya da küme ara'}
        />
      </Toolbar>

      {activeFilter === 'merged' && <p className="m-0 text-sm text-ink-3">Daha önce birleştirilmiş taslaklar. Parçaları incele; hata varsa <b className="text-ink">Ayır</b> ile eski hallerine döndür.</p>}
      {activeFilter === 'manual' && <p className="m-0 text-sm text-ink-3">Aynı soruya ait taslakları işaretle. Biri <b className="text-ink">çapa</b> olur; şıklar harmanlanır, mükerrerler temizlenir. Seçtiklerinde ortak geçen kelimeler aynı renkle boyanır.</p>}
      {activeFilter === 'vague' && <p className="m-0 text-sm text-ink-3">Bu taslaklarda güçlü bir eşleşme için yeterli bilgi yok. Yeni ipucu ya da şık geldikçe kendiliğinden bağlanırlar.</p>}

      {isCluster && (
        <BulkBar count={kumeSecim.count} noun="küme" busy={topluBusy || busy} onClear={kumeSecim.clear}
          actions={[
            { label: 'Birleştir', kind: 'main', run: () => topluKumeBirlestir() },
            { label: 'Kümeleri dağıt', run: () => topluKumeDagit() },
          ]} />
      )}
      {activeFilter === 'merged' && (
        <BulkBar count={birlesikSecim.count} noun="soru" busy={topluBusy} onClear={birlesikSecim.clear}
          actions={[
            { label: 'Ayır', kind: 'main', run: () => topluAyir() },
            { label: 'Sil', kind: 'danger', confirm: `${birlesikSecim.count} soruyu silmeyi onayla`, run: () => topluSil(gorunenBirlesik.filter((q) => birlesikSecim.has(q.id)), birlesikSecim.clear) },
          ]} />
      )}
      {activeFilter === 'vague' && (
        <BulkBar count={muglakSecim.count} noun="taslak" busy={topluBusy} onClear={muglakSecim.clear}
          actions={[
            { label: 'AI dönüştür', kind: 'main', run: () => topluDonustur() },
            { label: 'Sil', kind: 'danger', confirm: `${muglakSecim.count} taslağı silmeyi onayla`, run: () => topluSil(gorunenMuglak.filter((q) => muglakSecim.has(q.id)), muglakSecim.clear) },
          ]} />
      )}
      {activeFilter === 'manual' && selectedDraftIds.length > 0 && (
        <>
          {manualColors.size > 0 && <WordLegend texts={selectedQs.map(fullText)} colors={manualColors} />}
          {selectedDraftIds.length >= 2 && (
            <label className="inline-flex flex-wrap items-center gap-2 text-sm text-ink-3 max-w-full">
              Çapa soru
              <select className="pk14-sel" value={manualAnchorId} onChange={(e) => setManualAnchorId(e.target.value)} aria-label="Çapa soru">
                {selectedDraftIds.map((id) => {
                  const q = committeeQuestions.find((x) => x.id === id);
                  return <option key={id} value={id}>{q ? numLabel(q) : '?'} · {q?.topic || q?.discipline}</option>;
                })}
              </select>
            </label>
          )}
          <BulkBar count={selectedDraftIds.length} noun="taslak" busy={isManualMerging || isBulkDeleting} onClear={() => { setSelectedDraftIds([]); setManualAnchorId(''); }}
            actions={[
              { label: selectedDraftIds.length < 2 ? 'En az 2 seç' : 'Birleştir', kind: 'main', disabled: selectedDraftIds.length < 2, run: () => handleManualMergeSelected() },
              { label: 'Sil', kind: 'danger', confirm: `${selectedDraftIds.length} taslağı silmeyi onayla`, run: () => handleBulkDeleteSelected() },
            ]} />
        </>
      )}

      {loading ? (
        <div className="h-48 rounded-2xl ms-shimmer" role="status" aria-label="Taslaklar taranıyor" />
      ) : activeFilter === 'merged' ? (
        <DataTable rows={gorunenBirlesik} cols={birlesikCols} rowKey={(q) => q.id} onOpen={(q) => setAcikBirlesikId(q.id)} activeKey={acikBirlesikId} selection={birlesikSecim}
          empty={<EmptyState icon={Layers} title="Henüz birleştirilmiş soru yok">“Hazır” ya da “Tek taslaklar” sekmesinden birleştirebilirsin.</EmptyState>} />
      ) : activeFilter === 'manual' ? (
        <DataTable rows={manualFilteredQuestions} cols={manuelCols} rowKey={(q) => q.id} onOpen={(q) => setAcikTaslak({ id: q.id, liste: 'manual' })} activeKey={acikTaslak?.id ?? null} selection={manuelSecim}
          empty={<EmptyState icon={Check} title="Seçilebilir taslak yok" />} />
      ) : activeFilter === 'vague' ? (
        <DataTable rows={gorunenMuglak} cols={draftCols} rowKey={(q) => q.id} onOpen={(q) => setAcikTaslak({ id: q.id, liste: 'vague' })} activeKey={acikTaslak?.id ?? null} selection={muglakSecim}
          empty={<EmptyState icon={Check} title="Muğlak taslak yok" />} />
      ) : (
        <DataTable rows={filteredClusters} cols={kumeCols} rowKey={(c) => c.id} onOpen={(c) => setAcikKumeId(c.id)} activeKey={acikKumeId} selection={kumeSecim}
          empty={
            <EmptyState icon={Layers} title="Bu sekmede küme yok" action={<button type="button" onClick={() => setActiveFilter('manual')} className="m14-btn primary"><GitMerge aria-hidden="true" /> Elle seçime geç</button>}>
              Taslakları kendin birleştirmek istersen elle seçebilirsin.
            </EmptyState>
          } />
      )}

      <Drawer
        open={!!acikKume}
        onClose={() => setAcikKumeId(null)}
        wide
        title={acikKume ? acikKume.detectedSubject || effectiveAnchorOf(acikKume).topic || effectiveAnchorOf(acikKume).discipline || 'Küme' : ''}
        head={acikKume && <DetailNav list={filteredClusters} current={acikKume} same={(a, b) => a.id === b.id} onGo={(c) => setAcikKumeId(c.id)} />}
        foot={acikKume && (
          <div className="flex flex-wrap gap-2">
            <button type="button" onClick={() => { handleDissolveCluster(acikKume.id); sonrakiKume(acikKume); }} title="Bu kümeyi dağıt (yalnızca görünüm)" className="m14-btn ghost">
              <Split aria-hidden="true" /> Kümeyi dağıt
            </button>
            <button type="button" onClick={() => setOptimizingQuestion(effectiveAnchorOf(acikKume))} className="m14-btn">
              <Wand2 aria-hidden="true" /> İyileştir
            </button>
            <button type="button" onClick={() => { void handleMergeCluster(acikKume); }} disabled={mergingClusterId === acikKume.id || busy} className="m14-btn">
              <GitMerge aria-hidden="true" /> Birleştir
            </button>
            <button type="button" onClick={async () => { const c = acikKume; sonrakiKume(c); await handleMergeCluster(c); }} disabled={mergingClusterId === acikKume.id || busy} className="m14-btn primary">
              {mergingClusterId === acikKume.id ? <RefreshCw className="animate-spin" aria-hidden="true" /> : <GitMerge aria-hidden="true" />} {mergingClusterId === acikKume.id ? 'Birleştiriliyor…' : 'Birleştir ve sonraki'}
            </button>
          </div>
        )}
      >
        {acikKume && kumeAyrinti(acikKume)}
      </Drawer>

      <Drawer
        open={!!acikBirlesik}
        onClose={() => setAcikBirlesikId(null)}
        wide
        title={acikBirlesik ? `${numLabel(acikBirlesik)} · ${acikBirlesik.topic || acikBirlesik.discipline || 'Birleştirilmiş soru'}` : ''}
        head={acikBirlesik && <DetailNav list={gorunenBirlesik} current={acikBirlesik} same={(a, b) => a.id === b.id} onGo={(q) => setAcikBirlesikId(q.id)} />}
        foot={acikBirlesik && (
          <div className="flex flex-wrap gap-2 items-center">
            <DraftActions q={acikBirlesik} />
            <button type="button" onClick={() => { void handleUnmergeQuestion(acikBirlesik.id); }} disabled={unmergingQuestionId === acikBirlesik.id} className="m14-btn primary">
              {unmergingQuestionId === acikBirlesik.id ? <RefreshCw className="animate-spin" aria-hidden="true" /> : <Undo2 aria-hidden="true" />} {unmergingQuestionId === acikBirlesik.id ? 'Ayrılıyor…' : 'Ayır'}
            </button>
          </div>
        )}
      >
        {acikBirlesik && birlesikAyrinti(acikBirlesik)}
      </Drawer>

      <Drawer
        open={!!acikTaslakQ}
        onClose={() => setAcikTaslak(null)}
        wide
        title={acikTaslakQ ? `${numLabel(acikTaslakQ)} · ${acikTaslakQ.topic || acikTaslakQ.discipline || 'Taslak'}` : ''}
        head={acikTaslakQ && <DetailNav list={taslakListe} current={acikTaslakQ} same={(a, b) => a.id === b.id} onGo={(q) => setAcikTaslak((p) => (p ? { ...p, id: q.id } : p))} />}
        foot={acikTaslakQ && (
          <div className="flex flex-wrap gap-2 items-center">
            <DraftActions q={acikTaslakQ} />
            {acikTaslak?.liste === 'manual' && (
              <button type="button" className="m14-btn primary" onClick={() => toggleSelectDraft(acikTaslakQ.id)}>
                <Check aria-hidden="true" /> {selectedDraftIds.includes(acikTaslakQ.id) ? 'Seçimden çıkar' : 'Birleştirmek için seç'}
              </button>
            )}
          </div>
        )}
      >
        {acikTaslakQ && taslakAyrinti(acikTaslakQ)}
      </Drawer>

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
