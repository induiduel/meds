import React, { useState, useEffect, useMemo } from 'react';
import { X, Layers, RefreshCw, GitMerge, Check, ChevronDown, Zap, Search, Eye, EyeOff, Undo2, Split, Trash2, Wand2 } from 'lucide-react';
import { toast } from './ui/Toast';
import { CapsuleLoader, SuccessCheck } from './ui/Animations';
import { sharedWordColors, Colored, WordLegend } from './draftHighlight';
import { QuestionItem, Committee, ClusterAnalysisSummary, DraftCluster } from '../types';
import { ApiService } from '../services/api';
import { AppUser } from '../services/auth';
import { AiQuestionOptimizerModal } from './AiQuestionOptimizerModal';

interface DraftDeduplicationModalProps {
  isOpen: boolean;
  onClose: () => void;
  committee: Committee | null;
  questions: QuestionItem[];
  currentUser?: AppUser | null;
  onRefreshData: () => Promise<void>;
}

export const DraftDeduplicationModal: React.FC<DraftDeduplicationModalProps> = ({
  isOpen,
  onClose,
  committee,
  questions,
  currentUser,
  onRefreshData,
}) => {
  const [analysis, setAnalysis] = useState<ClusterAnalysisSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeFilter, setActiveFilter] = useState<'ready' | 'review' | 'merged' | 'manual' | 'all' | 'vague'>('ready');
  const [mergingClusterId, setMergingClusterId] = useState<string | null>(null);
  const [isBatchMerging, setIsBatchMerging] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'ok' | 'err'; message: string } | null>(null);
  const [expandedClusterId, setExpandedClusterId] = useState<string | null>(null);

  // Yerel birleştirilen uyduların listeden anında gizlenmesi
  const [locallyMergedSatelliteIds, setLocallyMergedSatelliteIds] = useState<Set<string>>(new Set());
  const [unmergingQuestionId, setUnmergingQuestionId] = useState<string | null>(null);
  const [inspectingMergedId, setInspectingMergedId] = useState<string | null>(null);

  // Manuel çoklu seçim durumu
  const [selectedDraftIds, setSelectedDraftIds] = useState<string[]>([]);
  const [manualAnchorId, setManualAnchorId] = useState<string>('');
  // Birleştir'e basıldığı an elle-seç listesinden kalkması için iyimser gizleme
  const [manuallyHiddenIds, setManuallyHiddenIds] = useState<Set<string>>(new Set());
  const [manualSearchQuery, setManualSearchQuery] = useState('');
  const [isManualMerging, setIsManualMerging] = useState(false);
  const [optimizingQuestion, setOptimizingQuestion] = useState<QuestionItem | null>(null);

  const committeeId = committee?.id || '';

  const runAnalysis = async () => {
    if (!committeeId) return;
    setLoading(true);
    setFeedback(null);
    try {
      const summary = await ApiService.getCommitteeDraftClusters(committeeId);
      setAnalysis(summary);
    } catch (e: any) {
      setFeedback({ type: 'err', message: e.message || 'Analiz sırasında hata oluştu.' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen && committeeId) {
      runAnalysis();
    }
  }, [isOpen, committeeId, questions.length]);

  const handleMergeCluster = async (cluster: DraftCluster) => {
    if (!currentUser?.email) {
      setFeedback({ type: 'err', message: 'Taslak birleştirmek için giriş yapmış olmalısınız.' });
      return;
    }
    setMergingClusterId(cluster.id);
    setFeedback(null);
    try {
      const satelliteIds = cluster.satelliteDrafts.map((s) => s.question.id);
      await ApiService.mergeDraftCluster(
        currentUser.email,
        cluster.anchorQuestion.id,
        satelliteIds,
        currentUser.displayName || 'Yönetici'
      );
      // Birleştirilen uyduları anında gizle
      setLocallyMergedSatelliteIds((prev) => new Set([...prev, ...satelliteIds]));
      setSelectedDraftIds((prev) => prev.filter((id) => !satelliteIds.includes(id)));
      setFeedback({
        type: 'ok',
        message: `Soru #${cluster.anchorQuestion.questionNumber || 'Çapa'} için ${satelliteIds.length} taslak başarıyla birleştirildi!`,
      });
      await onRefreshData();
      await runAnalysis();
    } catch (e: any) {
      setFeedback({ type: 'err', message: e.message || 'Birleştirme başarısız oldu.' });
    } finally {
      setMergingClusterId(null);
    }
  };

  const handleBatchMergeReady = async () => {
    if (!currentUser?.email) return;

    setIsBatchMerging(true);
    setFeedback(null);
    try {
      const res = await ApiService.autoMergeHighConfidenceClusters(
        currentUser.email,
        committeeId,
        currentUser.displayName || 'Akıllı Konsolidasyon'
      );
      setFeedback({
        type: 'ok',
        message: `Toplu işlem tamamlandı: ${res.mergedClustersCount} küme birleştirildi, ${res.savedDuplicatesCount} mükerrer taslak ana sorulara entegre edildi.`,
      });
      await onRefreshData();
      await runAnalysis();
    } catch (e: any) {
      setFeedback({ type: 'err', message: e.message || 'Toplu birleştirme başarısız oldu.' });
    } finally {
      setIsBatchMerging(false);
    }
  };

  // Manuel Çoklu Birleştirme İşlemi
  const handleManualMergeSelected = async () => {
    if (selectedDraftIds.length < 2) {
      setFeedback({ type: 'err', message: 'Birleştirmek için en az 2 taslak seçmelisiniz.' });
      return;
    }
    if (!currentUser?.email) {
      setFeedback({ type: 'err', message: 'Taslak birleştirmek için giriş yapmış olmalısınız.' });
      return;
    }

    const anchorId = manualAnchorId || selectedDraftIds[0];
    const satelliteIds = selectedDraftIds.filter((id) => id !== anchorId);
    const idsToMerge = [...selectedDraftIds];

    // Basıldığı an listeden kaldır (sonuç beklenmez); hata olursa geri getirilir.
    setManuallyHiddenIds((prev) => new Set([...prev, ...idsToMerge]));
    setSelectedDraftIds([]);
    setManualAnchorId('');

    setIsManualMerging(true);
    setFeedback(null);
    try {
      await ApiService.mergeDraftCluster(
        currentUser.email,
        anchorId,
        satelliteIds,
        currentUser.displayName || 'Yönetici'
      );
      // Birleştirilen uyduları manuel listeden anında kaldır
      setLocallyMergedSatelliteIds((prev) => new Set([...prev, ...satelliteIds]));
      setFeedback({
        type: 'ok',
        message: `Seçtiğiniz ${satelliteIds.length + 1} taslak başarıyla tek bir soru altında toplandı!`,
      });
      await onRefreshData();
      await runAnalysis();
    } catch (e: any) {
      setManuallyHiddenIds((prev) => {
        const next = new Set(prev);
        idsToMerge.forEach((id) => next.delete(id));
        return next;
      });
      setSelectedDraftIds(idsToMerge);
      setManualAnchorId(anchorId);
      setFeedback({ type: 'err', message: e.message || 'Manuel birleştirme başarısız oldu.' });
    } finally {
      setIsManualMerging(false);
    }
  };

  // Otomatik Kümeden Tek Bir Taslağı Ayırma / Çıkarma
  const handleDetachSatelliteFromCluster = (clusterId: string, satelliteQuestionId: string) => {
    if (!analysis) return;
    setAnalysis((prev) => {
      if (!prev) return null;
      const nextClusters = prev.clusters
        .map((c) => {
          if (c.id !== clusterId) return c;
          const nextSatellites = c.satelliteDrafts.filter((s) => s.question.id !== satelliteQuestionId);
          return {
            ...c,
            satelliteDrafts: nextSatellites
          };
        })
        .filter((c) => c.satelliteDrafts.length > 0);

      return {
        ...prev,
        clusters: nextClusters,
        mergeableClustersCount: nextClusters.length,
        vagueDraftsCount: prev.vagueDraftsCount + 1
      };
    });
    toast.success('Kümeden Ayrıldı', 'Taslak bu kümeden çıkarıldı ve bağımsız hale getirildi.');
  };

  // Otomatik Kümeyi Tamamen Dağıtma / Ayırma
  const handleDissolveCluster = (clusterId: string) => {
    if (!analysis) return;
    setAnalysis((prev) => {
      if (!prev) return null;
      const target = prev.clusters.find((c) => c.id === clusterId);
      const detachedCount = (target?.satelliteDrafts.length || 0) + 1;
      const nextClusters = prev.clusters.filter((c) => c.id !== clusterId);
      return {
        ...prev,
        clusters: nextClusters,
        mergeableClustersCount: nextClusters.length,
        vagueDraftsCount: prev.vagueDraftsCount + detachedCount
      };
    });
    toast.success('Küme Dağıtıldı', 'Kümeye ait tüm taslaklar serbest bırakıldı.');
  };

  // Birleştirilmiş Soruyu Eski Haline Ayırma (Unmerge)
  const handleUnmergeQuestion = async (questionId: string) => {
    if (!currentUser?.email) {
      toast.error('Yetki Yok', 'Taslak ayırmak için giriş yapmış olmalısınız.');
      return;
    }
    setUnmergingQuestionId(questionId);
    try {
      const res = await ApiService.unmergeDraftCluster(
        currentUser.email,
        questionId,
        currentUser.displayName || 'Yönetici'
      );
      // Geri yüklenen uyduları gizlilik kümesinden çıkar
      setLocallyMergedSatelliteIds((prev) => {
        const next = new Set(prev);
        res.restoredSatellites.forEach((s) => next.delete(s.id));
        return next;
      });
      toast.success('Taslaklar Ayrıldı', `${res.restoredSatellites.length} adet taslak bağımsız hale getirildi ve geri yüklendi.`);
      await onRefreshData();
      await runAnalysis();
    } catch (e: any) {
      toast.error('Ayırma Başarısız', e.message || 'Taslak ayırma işlemi sırasında hata oluştu.');
    } finally {
      setUnmergingQuestionId(null);
    }
  };

  // Taslağı Kalıcı Olarak Silme
  const handleDeleteDraft = async (draftId: string, topic: string) => {
    if (!window.confirm(`"${topic || 'Bu taslağı'}" kalıcı olarak silmek istediğinize emin misiniz?`)) {
      return;
    }
    try {
      await ApiService.deleteQuestion(draftId, currentUser);
      setLocallyMergedSatelliteIds((prev) => new Set([...prev, draftId]));
      setSelectedDraftIds((prev) => prev.filter((id) => id !== draftId));
      toast.success('Taslak Silindi', 'Taslak veritabanından kalıcı olarak kaldırıldı.');
      await onRefreshData();
      await runAnalysis();
    } catch (err: any) {
      toast.error('Silme Başarısız', err.message || 'Taslak silinemedi.');
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

  const filteredClusters = useMemo(() => {
    if (!analysis) return [];
    if (activeFilter === 'all') return analysis.clusters;
    if (activeFilter === 'ready') return analysis.clusters.filter((c) => c.status === 'ready_to_merge');
    if (activeFilter === 'review') return analysis.clusters.filter((c) => c.status === 'needs_review');
    return [];
  }, [analysis, activeFilter]);

  const committeeQuestions = useMemo(() => {
    return questions.filter((q) => {
      if (committeeId && q.committeeId !== committeeId) return false;
      if (locallyMergedSatelliteIds.has(q.id)) return false;
      return true;
    });
  }, [questions, committeeId, locallyMergedSatelliteIds]);

  const mergedQuestions = useMemo(() => {
    return questions.filter((q) => {
      if (committeeId && q.committeeId !== committeeId) return false;
      if (locallyMergedSatelliteIds.has(q.id)) return false;
      return (
        q.tags?.includes('taslak-birlestirildi') ||
        q.isMerged ||
        (q.mergedSatellites && q.mergedSatellites.length > 0) ||
        (q.fragments && q.fragments.some((f) => f.text.includes('[Birleştirilen Taslak')))
      );
    });
  }, [questions, committeeId, locallyMergedSatelliteIds]);

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

  // Results also surface as floating toasts
  useEffect(() => {
    if (!feedback) return;
    if (feedback.type === 'ok') toast.success('Birleştirildi', feedback.message);
    else toast.error('İşlem tamamlanamadı', feedback.message);
  }, [feedback]);

  const [confirmBatch, setConfirmBatch] = useState(false);
  useEffect(() => {
    if (!confirmBatch) return;
    const t = window.setTimeout(() => setConfirmBatch(false), 4000);
    return () => window.clearTimeout(t);
  }, [confirmBatch]);

  useEffect(() => {
    if (!isOpen) return;
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    document.addEventListener('keydown', onKey);
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = prev;
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const readyCount = analysis?.clusters.filter((c) => c.status === 'ready_to_merge').length || 0;
  const reviewCount = analysis?.clusters.filter((c) => c.status === 'needs_review').length || 0;
  const stemOf = (q: QuestionItem) => q.reconstruction?.stem || (q as any).stem || q.fragments?.[0]?.text || '';
  const fullText = (q: QuestionItem) => [stemOf(q), ...(q.options || []).map((o) => o.text)].join(' ');
  // Manual tab: colour words the selected drafts share (and show them in the other rows too)
  const selectedQs = selectedDraftIds.map((id) => committeeQuestions.find((x) => x.id === id)).filter(Boolean) as QuestionItem[];
  const manualColors = selectedQs.length >= 2 ? sharedWordColors(selectedQs.map(fullText)) : new Map<string, string>();
  const numLabel = (q: QuestionItem) => (q.isUnassignedNumber || !q.questionNumber ? 'No ?' : `S.${q.questionNumber}`);
  const shortCommittee = (committee?.name || 'Seçili kurul').replace(/^Dönem 3\s*-\s*/i, '');

  const tabs: { id: typeof activeFilter; label: string; count?: number }[] = [
    { id: 'ready', label: 'Hazır', count: readyCount },
    { id: 'review', label: 'İncele', count: reviewCount },
    { id: 'merged', label: 'Birleştirilenler', count: mergedQuestions.length },
    { id: 'all', label: 'Tümü', count: analysis?.clusters.length || 0 },
    { id: 'vague', label: 'Muğlak', count: analysis?.vagueDraftsCount || 0 },
    { id: 'manual', label: 'Elle seç', count: selectedDraftIds.length || undefined },
  ];

  const stats: { label: string; value: React.ReactNode; hint?: string; dot: string }[] = [
    { label: 'Taslak', value: analysis?.totalDrafts ?? '–', hint: 'öğrenci girdisi', dot: '#4A5868' },
    { label: 'Tahmini soru', value: analysis?.estimatedTrueQuestions ?? '–', hint: '/ 100 hedef', dot: '#1F9D55' },
    { label: 'Hazır küme', value: readyCount, hint: `${analysis?.potentialSavedDuplicates ?? 0} mükerrer`, dot: '#1E4FD8' },
    { label: 'Birleşik', value: mergedQuestions.length, hint: 'konsolide soru', dot: '#10B981' },
    { label: 'Muğlak', value: analysis?.vagueDraftsCount ?? '–', hint: 'eşleşme arıyor', dot: '#F59E0B' },
  ];

  const busy = loading || isBatchMerging || isManualMerging || !!mergingClusterId;

  return (
    <div
      className="ms-overlay fixed inset-0 z-[70] bg-[rgba(14,26,38,0.45)] backdrop-blur-[3px] flex items-end sm:items-center justify-center sm:p-5 ms-fade-in"
      onMouseDown={(e) => e.target === e.currentTarget && onClose()}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="dedup-title"
        className="relative w-full sm:max-w-[980px] h-[94dvh] sm:h-[min(92vh,900px)] bg-white rounded-t-2xl sm:rounded-2xl shadow-xl grid grid-rows-[auto_auto_auto_minmax(0,1fr)_auto] overflow-hidden ms-pop-in"
      >
        {/* Header */}
        <header className="relative flex items-center gap-3 px-4 sm:px-5 pt-4 pb-3">
          <span className="sm:hidden absolute left-1/2 -translate-x-1/2 top-1.5 w-10 h-[5px] rounded-full bg-line-2" aria-hidden="true" />
          <span className="w-10 h-10 rounded-xl bg-accent text-white flex items-center justify-center shrink-0 shadow-md">
            <Layers className="w-5 h-5" />
          </span>
          <div className="flex-1 min-w-0">
            <h2 id="dedup-title" className="m-0 font-display font-bold text-[19px] tracking-[-0.02em] leading-tight">
              Taslak birleştirme
            </h2>
            <p className="m-0 text-[13px] text-ink-3 truncate">{shortCommittee}</p>
          </div>
          <button
            type="button"
            onClick={runAnalysis}
            disabled={loading}
            aria-label="Yeniden analiz et"
            title="Yeniden analiz et"
            className="w-10 h-10 rounded-full flex items-center justify-center text-ink-2 hover:text-ink hover:bg-canvas cursor-pointer disabled:opacity-50"
          >
            <RefreshCw className={`w-[18px] h-[18px] ${loading ? 'animate-spin' : ''}`} />
          </button>
          <button
            type="button"
            onClick={onClose}
            aria-label="Kapat"
            className="w-10 h-10 rounded-full flex items-center justify-center text-ink-2 hover:text-ink hover:bg-canvas cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </header>

        {/* Stats */}
        {/* Hidden on short screens (landscape phones) so the list keeps its room */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 px-4 sm:px-5 pb-3 [@media(max-height:620px)]:hidden">
          {stats.map((s) => (
            <div key={s.label} className="rounded-xl bg-canvas px-3 py-2 flex flex-col">
              <span className="flex items-center gap-1.5 text-[12px] text-ink-2">
                <span className="w-2 h-2 rounded-full" style={{ background: s.dot }} aria-hidden="true" />
                {s.label}
              </span>
              <span className="flex items-baseline gap-1.5">
                <span className="font-mono text-[20px] font-semibold text-ink leading-tight">{s.value}</span>
                {s.hint && <span className="text-[12px] text-ink-3 truncate">{s.hint}</span>}
              </span>
            </div>
          ))}
        </div>

        {/* Tabs + batch action */}
        <div className="flex items-center gap-2 px-4 sm:px-5 pb-3 border-b border-line-soft">
          <div role="tablist" aria-label="Görünüm" className="flex gap-1 bg-canvas rounded-xl p-1 overflow-x-auto no-scrollbar min-w-0">
            {tabs.map((t) => {
              const on = activeFilter === t.id;
              return (
                <button
                  key={t.id}
                  type="button"
                  role="tab"
                  aria-selected={on}
                  onClick={() => setActiveFilter(t.id)}
                  className={`shrink-0 h-8 px-3 rounded-lg text-[13.5px] whitespace-nowrap cursor-pointer inline-flex items-center gap-1.5 transition-colors ${
                    on ? 'bg-white text-ink font-semibold shadow-xs' : 'text-ink-2 hover:text-ink'
                  }`}
                >
                  {t.id === 'manual' && <GitMerge className="w-3.5 h-3.5" />}
                  {t.label}
                  {t.count !== undefined && <span className={`font-mono text-[12px] ${on ? 'text-accent' : 'text-ink-3'}`}>{t.count}</span>}
                </button>
              );
            })}
          </div>
          <span className="flex-1" />
          {activeFilter === 'ready' && readyCount > 0 && (
            <button
              type="button"
              onClick={() => (confirmBatch ? (setConfirmBatch(false), handleBatchMergeReady()) : setConfirmBatch(true))}
              disabled={isBatchMerging}
              className={`shrink-0 h-10 px-3.5 rounded-[11px] text-[13.5px] font-semibold inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50 transition-colors ${
                confirmBatch ? 'bg-rose-700 text-white' : 'bg-ok text-white hover:bg-emerald-900'
              }`}
            >
              <Zap className="w-4 h-4" />
              <span className="hidden sm:inline">{confirmBatch ? 'Emin misin? Birleştir' : `Hazır ${readyCount} kümeyi birleştir`}</span>
              <span className="sm:hidden">{confirmBatch ? 'Onayla' : `Hepsi (${readyCount})`}</span>
            </button>
          )}
        </div>

        {/* Body */}
        <div className="relative overflow-y-auto bg-blue-50 px-4 sm:px-5 py-4 flex flex-col gap-2.5">
          {loading ? (
            <div role="status" className="py-14 flex flex-col items-center gap-2 text-center ms-fade-in">
              <CapsuleLoader />
              <p className="m-0 text-[15px] font-semibold text-ink">Taslaklar taranıyor…</p>
              <p className="m-0 text-[13px] text-ink-3">Tıbbi kavramlar ve şık varyasyonları karşılaştırılıyor</p>
            </div>
          ) : activeFilter === 'merged' ? (
            <>
              <div className="flex items-center justify-between gap-2">
                <p className="m-0 text-[13.5px] text-ink-2">
                  Daha önce birleştirilmiş (iç içe geçmiş) taslaklar aşağıda listelenmiştir. Her bir taslağın parçalarını inceleyebilir, hata durumunda <strong className="text-ink">"Taslakları Ayır (Geri Al)"</strong> butonuyla eski bağımsız hallerine döndürebilirsiniz.
                </p>
              </div>
              {mergedQuestions.length === 0 ? (
                <EmptyState
                  title="Henüz birleştirilmiş soru yok"
                  text="Taslakları 'Hazır' veya 'Elle seç' sekmesinden birleştirebilirsiniz."
                  action={{ label: 'Taslak seçimine geç', onClick: () => setActiveFilter('manual') }}
                />
              ) : (
                <ul className="list-none m-0 p-0 flex flex-col gap-3">
                  {mergedQuestions.map((q) => {
                    const isInspecting = inspectingMergedId === q.id;
                    const isUnmerging = unmergingQuestionId === q.id;
                    const satelliteCount =
                      q.mergedSatellites?.length ||
                      (q.fragments?.filter((f) => f.text.includes('[Birleştirilen Taslak')).length || 0);

                    return (
                      <li
                        key={q.id}
                        className="rounded-2xl bg-white border border-emerald-200 shadow-sm overflow-hidden flex flex-col"
                      >
                        {/* Başlık ve Butonlar */}
                        <div className="flex items-center gap-3 px-4 py-3 bg-emerald-50 border-b border-emerald-100">
                          <span className="w-9 h-9 rounded-[10px] bg-ok-soft text-ok font-mono text-[13px] font-bold flex items-center justify-center shrink-0">
                            {numLabel(q)}
                          </span>
                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2">
                              <span className="font-semibold text-ink text-[14.5px] truncate">
                                {q.topic || q.discipline || 'Birleştirilmiş Soru'}
                              </span>
                              <span className="h-5 px-2 rounded-full bg-ok text-white text-[11px] font-semibold inline-flex items-center gap-1 shrink-0">
                                <Layers className="w-3 h-3" />
                                {satelliteCount > 0 ? `${satelliteCount + 1} taslak birleşik` : 'Birleşik'}
                              </span>
                            </div>
                            <span className="text-[12px] text-ink-3">
                              {q.discipline} · {q.fragments?.length || 0} parça · {q.options?.length || 0} şık
                            </span>
                          </div>
                          <div className="flex items-center gap-1.5 shrink-0">
                            <button
                              type="button"
                              onClick={() => setOptimizingQuestion(q)}
                              className="h-8 px-2.5 rounded-lg bg-accent-soft hover:bg-accent/20 text-accent text-[12.5px] font-semibold inline-flex items-center gap-1 cursor-pointer transition-colors"
                              title="Taslağı amfi slaytları ve AI ile tam soruya dönüştür"
                            >
                              <Wand2 className="w-3.5 h-3.5" />
                              <span>AI ile Geliştir</span>
                            </button>
                            <button
                              type="button"
                              onClick={() => setInspectingMergedId(isInspecting ? null : q.id)}
                              className="h-8 px-2.5 rounded-lg border border-line bg-white text-[12.5px] font-medium text-ink-2 hover:text-ink inline-flex items-center gap-1 cursor-pointer"
                            >
                              {isInspecting ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                              <span>{isInspecting ? 'Kapat' : 'İncele'}</span>
                            </button>
                            <button
                              type="button"
                              onClick={() => handleUnmergeQuestion(q.id)}
                              disabled={isUnmerging}
                              className="h-8 px-2.5 rounded-lg border border-rose-300 bg-rose-50 text-rose-700 text-[12.5px] font-semibold hover:bg-rose-100 inline-flex items-center gap-1 cursor-pointer disabled:opacity-50 transition-colors"
                              title="İç içe geçmiş taslakları ayrıştırıp bağımsız taslaklar olarak geri yükler"
                            >
                              {isUnmerging ? (
                                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                              ) : (
                                <Undo2 className="w-3.5 h-3.5" />
                              )}
                              <span>{isUnmerging ? 'Ayrılıyor…' : 'Ayır (Geri Al)'}</span>
                            </button>
                          </div>
                        </div>

                        {/* Konsolide Soru Önizlemesi */}
                        <div className="p-3.5 flex flex-col gap-2">
                          <p className="m-0 text-[13.5px] text-ink leading-relaxed">
                            {stemOf(q) || 'Soru kökü henüz girilmemiş'}
                          </p>
                          {q.options && q.options.length > 0 && (
                            <div className="flex flex-wrap gap-1.5 pt-1 border-t border-line-soft">
                              {q.options.map((opt) => (
                                <span key={opt.key} className="h-6 px-2 rounded-md bg-canvas text-[12px] text-ink-2 inline-flex items-center">
                                  <strong className="font-mono text-ink mr-1">{opt.key})</strong>
                                  {opt.text}
                                </span>
                              ))}
                            </div>
                          )}

                          {/* Detaylı İnceleme Bölümü */}
                          {isInspecting && (
                            <div className="mt-2 pt-3 border-t border-line flex flex-col gap-2.5 bg-canvas/60 p-3 rounded-xl">
                              <span className="text-[12.5px] font-semibold text-accent flex items-center gap-1.5">
                                <Layers className="w-3.5 h-3.5" />
                                İç İçe Geçen Taslaklar ve Öğrenci Katkıları
                              </span>

                              {/* Varsa Orijinal Uydu Taslak Kayıtları */}
                              {q.mergedSatellites && q.mergedSatellites.length > 0 ? (
                                <div className="flex flex-col gap-2">
                                  {q.mergedSatellites.map((sat, sIdx) => (
                                    <div key={sat.id || sIdx} className="rounded-[10px] bg-white border border-line-soft p-2.5 flex flex-col gap-1 text-[12.5px]">
                                      <div className="flex items-center justify-between text-ink-3">
                                        <span className="font-semibold text-ink">
                                          Taslak #{sIdx + 1}: {sat.contributedByName || sat.author || 'Anonim Katkıcı'}
                                        </span>
                                        <span className="font-mono text-[11.5px]">{numLabel(sat)}</span>
                                      </div>
                                      <p className="m-0 text-ink-2 leading-snug">
                                        {stemOf(sat) || 'Metin girilmemiş'}
                                      </p>
                                      {sat.fragments && sat.fragments.length > 0 && (
                                        <div className="flex flex-col gap-1 mt-1 pl-2 border-l-2 border-accent/40">
                                          {sat.fragments.map((sf) => (
                                            <div key={sf.id} className="text-[11.5px] text-ink-3">
                                              <span className="font-medium text-ink-2">{sf.author}:</span> “{sf.text}”
                                            </div>
                                          ))}
                                        </div>
                                      )}
                                      {sat.options && sat.options.length > 0 && (
                                        <div className="flex flex-wrap gap-1 mt-0.5">
                                          {sat.options.map((o) => (
                                            <span key={o.key} className="px-1.5 py-0.5 rounded bg-canvas text-[11px] text-ink-3">
                                              {o.key}) {o.text}
                                            </span>
                                          ))}
                                        </div>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              ) : (
                                /* Parçalardan derleme görünümü */
                                <div className="flex flex-col gap-1.5">
                                  {(q.fragments || [])
                                    .filter((f) => f.text.includes('[Birleştirilen Taslak'))
                                    .map((f, fIdx) => (
                                      <div key={f.id || fIdx} className="rounded-[10px] bg-white border border-line-soft p-2.5 flex flex-col gap-0.5 text-[12.5px]">
                                        <div className="flex items-center justify-between text-ink-3">
                                          <span className="font-semibold text-ink">{f.author || 'Taslak Parçası'}</span>
                                          {f.timestamp && <span className="text-[11px]">{new Date(f.timestamp).toLocaleDateString('tr-TR')}</span>}
                                        </div>
                                        <p className="m-0 text-ink-2 leading-snug">{f.text}</p>
                                      </div>
                                    ))}
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      </li>
                    );
                  })}
                </ul>
              )}
            </>
          ) : activeFilter === 'manual' ? (
            <>
              <p className="m-0 text-[13.5px] text-ink-2">
                Aynı soruya ait taslakları işaretle. Biri <strong className="text-ink">çapa</strong> olur; şıklar harmanlanır, mükerrerler temizlenir.
              </p>
              {manualColors.size > 0 && <WordLegend texts={selectedQs.map(fullText)} colors={manualColors} />}
              <label className="flex items-center gap-2 h-11 px-3.5 rounded-xl bg-white border border-line focus-within:border-accent">
                <Search className="w-4 h-4 text-ink-3 shrink-0" />
                <span className="sr-only">Taslaklarda ara</span>
                <input
                  type="search"
                  placeholder="Metin, konu, ders ya da soru no ara"
                  value={manualSearchQuery}
                  onChange={(e) => setManualSearchQuery(e.target.value)}
                  className="flex-1 min-w-0 bg-transparent border-0 outline-0 text-[16px] sm:text-[14.5px] placeholder:text-slate-600"
                />
                <span className="text-[12.5px] text-ink-3 shrink-0">{manualFilteredQuestions.length}</span>
              </label>
              <ul className="list-none m-0 p-0 flex flex-col gap-1.5">
                {manualFilteredQuestions.map((q) => {
                  const on = selectedDraftIds.includes(q.id);
                  const isAnchor = on && manualAnchorId === q.id;
                  return (
                    <li key={q.id}>
                      <div className="flex items-center gap-1.5 w-full">
                        <button
                          type="button"
                          role="checkbox"
                          aria-checked={on}
                          onClick={() => toggleSelectDraft(q.id)}
                          className={`flex-1 text-left rounded-xl border px-3 py-2.5 flex items-start gap-3 cursor-pointer transition-colors ${
                            on ? 'bg-accent-soft/60 border-accent/40' : 'bg-white border-line hover:border-line-2'
                          }`}
                        >
                          <span
                            className={`mt-0.5 w-5 h-5 rounded-md flex items-center justify-center shrink-0 ${on ? 'bg-accent text-white' : 'bg-white border border-line-2'}`}
                            aria-hidden="true"
                          >
                            {on && <Check className="w-3.5 h-3.5" strokeWidth={3} />}
                          </span>
                          <span className="flex-1 min-w-0 flex flex-col gap-1">
                            <span className="flex items-center gap-2 min-w-0 text-[12.5px] text-ink-3">
                              <span className="font-mono font-semibold text-ink">{numLabel(q)}</span>
                              <span className="truncate">
                                {q.discipline}
                                {q.topic ? ` · ${q.topic}` : ''}
                              </span>
                              {isAnchor && (
                                <span className="ml-auto shrink-0 h-5 px-2 rounded-full bg-accent text-white text-[11px] font-semibold inline-flex items-center">Çapa</span>
                              )}
                            </span>
                            <span className="text-[14px] text-ink leading-snug line-clamp-2">
                              {stemOf(q) ? <Colored text={stemOf(q)} colors={manualColors} /> : 'Metin girilmemiş'}
                            </span>
                            {q.options?.length > 0 && (
                              <span className="flex flex-wrap gap-1">
                                {q.options.slice(0, 3).map((o) => (
                                  <span key={o.key} className="max-w-[220px] truncate h-6 px-2 rounded-md bg-canvas text-[12px] text-ink-2 inline-flex items-center">
                                    <strong className="font-mono mr-1">{o.key}</strong>
                                    <Colored text={o.text} colors={manualColors} />
                                  </span>
                                ))}
                                {q.options.length > 3 && <span className="h-6 px-2 text-[12px] text-ink-3 inline-flex items-center">+{q.options.length - 3}</span>}
                              </span>
                            )}
                          </span>
                        </button>
                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDeleteDraft(q.id, q.topic || q.discipline);
                          }}
                          className="w-10 h-10 rounded-xl border border-line bg-white flex items-center justify-center text-ink-3 hover:text-bad-text hover:bg-bad-soft hover:border-bad/30 cursor-pointer shrink-0 transition-colors"
                          title="Taslağı kalıcı olarak veritabanından sil"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </li>
                  );
                })}
              </ul>
            </>
          ) : activeFilter === 'vague' ? (
            <>
              <p className="m-0 text-[13.5px] text-ink-2">
                Bu taslaklarda henüz güçlü bir eşleşme için yeterli bilgi yok. Yeni ipucu ya da şık geldikçe otomatik bağlanırlar.
              </p>
              {!analysis?.unmatchedVagueDrafts.length ? (
                <EmptyState title="Muğlak taslak yok" text="Bütün taslaklar bir soruyla eşleşmiş görünüyor." />
              ) : (
                analysis.unmatchedVagueDrafts.map((q) => (
                  <div key={q.id} className="rounded-xl bg-white border border-line px-3.5 py-2.5 flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0 flex flex-col gap-1">
                      <span className="flex items-center gap-2 text-[12.5px] text-ink-3 min-w-0">
                        <span className="font-mono font-semibold text-ink">{numLabel(q)}</span>
                        <span className="truncate">
                          {q.discipline}
                          {q.topic ? ` · ${q.topic}` : ''}
                        </span>
                      </span>
                      <span className="text-[14px] text-ink leading-snug line-clamp-2">{stemOf(q) || 'Metin girilmemiş'}</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleDeleteDraft(q.id, q.topic || q.discipline)}
                      className="w-9 h-9 rounded-[10px] border border-line bg-white flex items-center justify-center text-ink-3 hover:text-bad-text hover:bg-bad-soft hover:border-bad/30 cursor-pointer shrink-0 transition-colors"
                      title="Taslağı kalıcı olarak sil"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))
              )}
            </>
          ) : filteredClusters.length === 0 ? (
            <EmptyState
              title="Bu sekmede küme yok"
              text="Taslakları kendin birleştirmek istersen elle seçebilirsin."
              action={{ label: 'Elle seçime geç', onClick: () => setActiveFilter('manual') }}
            />
          ) : (
            filteredClusters.map((cluster) => {
              const anchor = cluster.anchorQuestion;
              const open = expandedClusterId === cluster.id;
              const merging = mergingClusterId === cluster.id;
              const ready = cluster.status === 'ready_to_merge';
              const clusterTexts = [anchor, ...cluster.satelliteDrafts.map((sd) => sd.question)].map(fullText);
              const colors = sharedWordColors(clusterTexts);
              return (
                <article
                  key={cluster.id}
                  className={`rounded-2xl bg-white border overflow-hidden ${ready ? 'border-emerald-200' : 'border-line'}`}
                >
                  {/* Row: number, subject, confidence, actions */}
                  <div className="flex items-center gap-3 px-3.5 py-3">
                    <span
                      className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 font-mono text-[13px] font-semibold ${
                        ready ? 'bg-ok-soft text-ok' : 'bg-warn-soft text-warn'
                      }`}
                    >
                      {anchor.isUnassignedNumber || !anchor.questionNumber ? '?' : anchor.questionNumber}
                    </span>
                    <span className="flex-1 min-w-0 flex flex-col">
                      <span className="flex items-center gap-2 min-w-0">
                        <span className="text-[14.5px] font-semibold text-ink truncate">{cluster.detectedSubject || anchor.topic || anchor.discipline}</span>
                        <span
                          className={`shrink-0 h-5 px-1.5 rounded-full text-[11.5px] font-mono font-semibold inline-flex items-center ${
                            ready ? 'bg-ok-soft text-ok' : 'bg-warn-soft text-warn'
                          }`}
                        >
                          %{cluster.overallConfidence}
                        </span>
                      </span>
                      <span className="text-[12.5px] text-ink-3 truncate">
                        {anchor.discipline} · {cluster.satelliteDrafts.length} taslak birleşecek
                      </span>
                      <span className="mt-1">
                        <WordLegend texts={clusterTexts} colors={colors} />
                      </span>
                    </span>
                    <button
                      type="button"
                      onClick={() => handleDissolveCluster(cluster.id)}
                      title="Bu kümeyi dağıtıp taslakları ayır"
                      className="hidden sm:inline-flex h-9 px-2.5 rounded-[10px] border border-line bg-white text-[12px] font-medium text-ink-2 hover:text-rose-700 hover:border-rose-200 hover:bg-rose-50 items-center gap-1 cursor-pointer"
                    >
                      <Split className="w-3.5 h-3.5" />
                      <span>Kümeyi Dağıt</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => setExpandedClusterId(open ? null : cluster.id)}
                      aria-expanded={open}
                      className="hidden sm:inline-flex h-9 px-3 rounded-[10px] border border-line bg-white text-[13px] font-semibold text-ink-2 items-center gap-1 cursor-pointer hover:border-line-2"
                    >
                      Karşılaştır
                      <ChevronDown className={`w-4 h-4 transition-transform ${open ? 'rotate-180' : ''}`} />
                    </button>
                    <button
                      type="button"
                      onClick={() => handleMergeCluster(cluster)}
                      disabled={merging || busy}
                      className={`h-9 px-3 rounded-[10px] text-[13px] font-semibold text-white inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50 ${
                        ready ? 'bg-ok hover:bg-emerald-900' : 'bg-ink hover:bg-blue-950'
                      }`}
                    >
                      {merging ? <RefreshCw className="w-4 h-4 animate-spin" /> : <GitMerge className="w-4 h-4" />}
                      <span className="hidden sm:inline">{merging ? 'Birleştiriliyor…' : 'Birleştir'}</span>
                    </button>
                  </div>

                  {/* Anchor + satellites, compact */}
                  <div className="grid grid-cols-1 md:grid-cols-[minmax(0,1fr)_minmax(0,1fr)] gap-2 px-3.5 pb-3.5">
                    <div className="rounded-xl bg-canvas px-3 py-2.5 flex flex-col gap-1">
                      <span className="flex items-center gap-1.5 text-[12px] font-semibold text-accent">
                        <Layers className="w-3.5 h-3.5" />
                        Çapa soru
                        <span className="ml-auto font-normal text-ink-3">{anchor.options?.length || 0} şık</span>
                      </span>
                      <span className={`text-[13.5px] text-ink leading-snug ${open ? '' : 'line-clamp-2'}`}>{stemOf(anchor) ? <Colored text={stemOf(anchor)} colors={colors} /> : 'Soru kökü henüz girilmemiş'}</span>
                      {open && anchor.options?.length > 0 && (
                        <span className="flex flex-col gap-0.5 pt-1 border-t border-line-soft mt-1">
                          {anchor.options.map((o) => (
                            <span key={o.key} className="text-[12.5px] text-ink-2">
                              <strong className="font-mono text-ink mr-1">{o.key})</strong>
                              <Colored text={o.text} colors={colors} />
                            </span>
                          ))}
                        </span>
                      )}
                    </div>
                    <ul className={`list-none m-0 p-0 flex flex-col gap-1.5 ${open ? '' : 'max-h-[132px] overflow-y-auto'}`}>
                      {cluster.satelliteDrafts.map((sat, idx) => (
                        <li key={sat.question.id || idx} className="rounded-xl border border-line-soft px-3 py-2 flex flex-col gap-1">
                          <div className="flex items-center gap-2 text-[12.5px] min-w-0">
                            <span className="font-semibold text-ink truncate">{sat.question.contributedByName || 'Anonim'}</span>
                            <span className="text-ink-3 shrink-0">· {numLabel(sat.question)}</span>
                            <span className="shrink-0 font-mono text-[12px] font-semibold text-ok">%{sat.compatibility.score}</span>
                            <button
                              type="button"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleDetachSatelliteFromCluster(cluster.id, sat.question.id);
                              }}
                              title="Bu taslağı bu kümeden ayır (bağımsız yap)"
                              className="ml-auto text-[11.5px] px-2 py-0.5 rounded-md text-ink-3 hover:text-rose-700 hover:bg-rose-100 border border-line-soft transition-colors cursor-pointer inline-flex items-center gap-1 shrink-0"
                            >
                              <Split className="w-3 h-3" />
                              <span>Kümeden Ayır</span>
                            </button>
                            <button
                              type="button"
                              onClick={(e) => {
                                e.stopPropagation();
                                handleDeleteDraft(sat.question.id, sat.question.topic || sat.question.discipline);
                              }}
                              title="Taslağı kalıcı olarak veritabanından sil"
                              className="text-[11.5px] px-2 py-0.5 rounded-md text-ink-3 hover:text-bad-text hover:bg-bad-soft border border-line-soft transition-colors cursor-pointer inline-flex items-center gap-1 shrink-0"
                            >
                              <Trash2 className="w-3 h-3" />
                              <span>Sil</span>
                            </button>
                          </div>
                          <span className={`text-[13px] text-ink-2 leading-snug ${open ? '' : 'line-clamp-1'}`}>{stemOf(sat.question) ? <Colored text={stemOf(sat.question)} colors={colors} /> : 'Metin'}</span>
                          {open && sat.compatibility.reasons.length > 0 && (
                            <span className="flex flex-wrap gap-1">
                              {sat.compatibility.reasons.map((r, i) => (
                                <span key={i} className="px-2 py-0.5 rounded-md bg-canvas text-[11.5px] text-ink-2">
                                  {r}
                                </span>
                              ))}
                            </span>
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {open && (
                    <p className="m-0 mx-3.5 mb-3.5 rounded-xl bg-accent-soft/60 px-3 py-2 text-[12.5px] text-ink-2 leading-[1.55]">
                      Birleşince ipuçları ve parçalar çapa soruya taşınır (isimler ve puanlar korunur), şıklar 5'e tamamlanır, mükerrer taslaklar silinir.
                    </p>
                  )}
                  <button
                    type="button"
                    onClick={() => setExpandedClusterId(open ? null : cluster.id)}
                    className="sm:hidden w-full h-10 border-t border-line-soft text-[13px] font-semibold text-ink-2 inline-flex items-center justify-center gap-1 cursor-pointer"
                  >
                    {open ? 'Daha az' : 'Karşılaştır'}
                    <ChevronDown className={`w-4 h-4 transition-transform ${open ? 'rotate-180' : ''}`} />
                  </button>
                </article>
              );
            })
          )}
        </div>

        {/* Footer: manual-merge bar, or a quiet close */}
        <footer className="flex items-center gap-2 px-4 sm:px-5 py-3 pb-[max(env(safe-area-inset-bottom),12px)] sm:pb-3 border-t border-line-soft bg-white">
          {activeFilter === 'manual' && selectedDraftIds.length > 0 ? (
            <>
              <span className="text-[13.5px] text-ink-2 shrink-0">
                <strong className="text-ink">{selectedDraftIds.length}</strong> seçili
              </span>
              {selectedDraftIds.length >= 2 && (
                <label className="relative min-w-0 flex-1 sm:flex-none sm:w-[280px]">
                  <span className="sr-only">Çapa soru</span>
                  <select
                    value={manualAnchorId}
                    onChange={(e) => setManualAnchorId(e.target.value)}
                    className="appearance-none w-full h-10 rounded-[11px] bg-field border border-line pl-3 pr-8 text-[13.5px] text-ink cursor-pointer truncate"
                  >
                    {selectedDraftIds.map((id) => {
                      const q = committeeQuestions.find((x) => x.id === id);
                      return (
                        <option key={id} value={id}>
                          Çapa: {q ? numLabel(q) : '?'} · {q?.topic || q?.discipline}
                        </option>
                      );
                    })}
                  </select>
                  <ChevronDown className="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-3" />
                </label>
              )}
              <button
                type="button"
                onClick={() => {
                  setSelectedDraftIds([]);
                  setManualAnchorId('');
                }}
                className="hidden sm:inline-flex h-10 px-3 rounded-[11px] text-[13.5px] font-semibold text-ink-2 hover:bg-canvas cursor-pointer items-center"
              >
                Temizle
              </button>
              <button
                type="button"
                onClick={handleManualMergeSelected}
                disabled={isManualMerging || selectedDraftIds.length < 2}
                className="ml-auto h-10 px-4 rounded-[11px] bg-accent hover:bg-accent-hover text-white text-[14px] font-semibold inline-flex items-center gap-1.5 cursor-pointer disabled:opacity-50 shrink-0"
              >
                {isManualMerging ? <RefreshCw className="w-4 h-4 animate-spin" /> : <GitMerge className="w-4 h-4" />}
                {selectedDraftIds.length < 2 ? 'En az 2 seç' : 'Birleştir'}
              </button>
            </>
          ) : (
            <>
              <span className="text-[12.5px] text-ink-3 truncate">Kavram ve şık permütasyonuna göre kümeleme</span>
              <button
                type="button"
                onClick={onClose}
                className="ml-auto h-10 px-4 rounded-[11px] bg-canvas hover:bg-line-soft text-[14px] font-semibold text-ink cursor-pointer shrink-0"
              >
                Kapat
              </button>
            </>
          )}
        </footer>
      </div>

      {optimizingQuestion && (
        <AiQuestionOptimizerModal
          question={optimizingQuestion}
          isOpen={Boolean(optimizingQuestion)}
          onClose={() => setOptimizingQuestion(null)}
          currentUser={currentUser}
          onSaved={async () => {
            setOptimizingQuestion(null);
            await onRefreshData();
            await runAnalysis();
            toast.success('Taslak AI ile Geliştirildi', 'Soru amfi slaytları referansıyla güncellendi.');
          }}
        />
      )}
    </div>
  );
};

const EmptyState: React.FC<{ title: string; text: string; action?: { label: string; onClick: () => void } }> = ({ title, text, action }) => (
  <div className="py-12 flex flex-col items-center gap-2 text-center">
    <SuccessCheck size={72} />
    <p className="m-0 text-[16px] font-semibold text-ink">{title}</p>
    <p className="m-0 text-[13.5px] text-ink-2 max-w-[340px]">{text}</p>
    {action && (
      <button
        type="button"
        onClick={action.onClick}
        className="mt-1 h-10 px-4 rounded-[11px] bg-accent-soft text-accent text-[14px] font-semibold inline-flex items-center gap-1.5 cursor-pointer"
      >
        <GitMerge className="w-4 h-4" />
        {action.label}
      </button>
    )}
  </div>
);
