import React, { useState, useEffect, useMemo } from 'react';
import {
  Sparkles,
  X,
  CheckCircle2,
  AlertTriangle,
  Layers,
  ArrowRight,
  RefreshCw,
  GitMerge,
  Filter,
  Check,
  HelpCircle,
  Hash,
  ChevronDown,
  ChevronUp,
  FileQuestion,
  Users,
  ShieldAlert,
  Zap
} from 'lucide-react';
import { QuestionItem, Committee, ClusterAnalysisSummary, DraftCluster } from '../types';
import { ApiService } from '../services/api';
import { AppUser } from '../services/auth';

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
  const [activeFilter, setActiveFilter] = useState<'all' | 'ready' | 'review' | 'vague'>('ready');
  const [mergingClusterId, setMergingClusterId] = useState<string | null>(null);
  const [isBatchMerging, setIsBatchMerging] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'ok' | 'err'; message: string } | null>(null);
  const [expandedClusterId, setExpandedClusterId] = useState<string | null>(null);

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
    if (!window.confirm('Yüksek uyumlu (>=%80) tüm taslak kümeleri otomatik birleştirilecek. Onaylıyor musunuz?')) return;

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

  const filteredClusters = useMemo(() => {
    if (!analysis) return [];
    if (activeFilter === 'all') return analysis.clusters;
    if (activeFilter === 'ready') return analysis.clusters.filter((c) => c.status === 'ready_to_merge');
    if (activeFilter === 'review') return analysis.clusters.filter((c) => c.status === 'needs_review');
    return [];
  }, [analysis, activeFilter]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-slate-950/70 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white w-full max-w-5xl rounded-2xl shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[92vh]">
        {/* Header */}
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/20 border border-indigo-400/30 flex items-center justify-center text-indigo-400">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-bold">Akıllı Taslak Birleştirme ve Kümeleme Merkezi</h2>
                <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-400/30">
                  {committee?.name || 'Seçili Kurul'}
                </span>
              </div>
              <p className="text-xs text-slate-300">
                Farklı kitapçık şık ve numara varyasyonlarını analiz eder, 100 soru hedefine konsolide eder.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={runAnalysis}
              disabled={loading}
              title="Yeniden Analiz Et"
              className="w-9 h-9 rounded-lg bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors cursor-pointer disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={onClose}
              className="w-9 h-9 rounded-lg bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Feedback Alert */}
        {feedback && (
          <div
            className={`px-5 py-2.5 text-xs font-medium flex items-center gap-2 border-b ${
              feedback.type === 'ok'
                ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                : 'bg-rose-50 text-rose-800 border-rose-200'
            }`}
          >
            {feedback.type === 'ok' ? <Check className="w-4 h-4 text-emerald-600" /> : <AlertTriangle className="w-4 h-4 text-rose-600" />}
            <span>{feedback.message}</span>
          </div>
        )}

        {/* Metric Cards Banner */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 bg-slate-50 border-b border-slate-200 text-xs">
          <div className="bg-white p-3 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
            <span className="text-slate-500 font-medium">Toplam Taslak Havuzu</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-xl font-bold text-slate-800 font-mono">{analysis?.totalDrafts ?? '...'}</span>
              <span className="text-[11px] text-slate-400">öğrenci girdisi</span>
            </div>
          </div>

          <div className="bg-white p-3 rounded-xl border border-emerald-200 bg-emerald-50/30 shadow-sm flex flex-col justify-between">
            <span className="text-emerald-700 font-medium">Tahmini Gerçek Soru</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-xl font-bold text-emerald-700 font-mono">
                {analysis?.estimatedTrueQuestions ?? '...'}
              </span>
              <span className="text-[11px] text-emerald-600">/ 100 Hedef</span>
            </div>
          </div>

          <div className="bg-white p-3 rounded-xl border border-indigo-200 bg-indigo-50/30 shadow-sm flex flex-col justify-between">
            <span className="text-indigo-700 font-medium">Birleşmeye Hazır Küme</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-xl font-bold text-indigo-700 font-mono">
                {analysis?.clusters.filter((c) => c.status === 'ready_to_merge').length ?? '...'}
              </span>
              <span className="text-[11px] text-indigo-600">
                ({analysis?.potentialSavedDuplicates ?? 0} mükerrer)
              </span>
            </div>
          </div>

          <div className="bg-white p-3 rounded-xl border border-amber-200 bg-amber-50/30 shadow-sm flex flex-col justify-between">
            <span className="text-amber-700 font-medium">Muğlak / Tekil Parça</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-xl font-bold text-amber-700 font-mono">
                {analysis?.vagueDraftsCount ?? '...'}
              </span>
              <span className="text-[11px] text-amber-600">eşleşme arayan</span>
            </div>
          </div>
        </div>

        {/* Filter Tabs and Quick Actions */}
        <div className="px-5 py-3 border-b border-slate-200 flex flex-wrap items-center justify-between gap-3 bg-white">
          <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar">
            <button
              onClick={() => setActiveFilter('ready')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer ${
                activeFilter === 'ready'
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              <CheckCircle2 className="w-3.5 h-3.5" />
              Yüksek Uyum (%80+) ({analysis?.clusters.filter((c) => c.status === 'ready_to_merge').length || 0})
            </button>

            <button
              onClick={() => setActiveFilter('review')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer ${
                activeFilter === 'review'
                  ? 'bg-amber-600 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              <HelpCircle className="w-3.5 h-3.5" />
              İnceleme Bekleyenler ({analysis?.clusters.filter((c) => c.status === 'needs_review').length || 0})
            </button>

            <button
              onClick={() => setActiveFilter('all')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer ${
                activeFilter === 'all'
                  ? 'bg-slate-800 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              <Filter className="w-3.5 h-3.5" />
              Tüm Kümeler ({analysis?.clusters.length || 0})
            </button>

            <button
              onClick={() => setActiveFilter('vague')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer ${
                activeFilter === 'vague'
                  ? 'bg-purple-600 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              <FileQuestion className="w-3.5 h-3.5" />
              Muğlak Taslaklar ({analysis?.vagueDraftsCount || 0})
            </button>
          </div>

          {activeFilter === 'ready' && (analysis?.clusters.filter((c) => c.status === 'ready_to_merge').length || 0) > 0 && (
            <button
              onClick={handleBatchMergeReady}
              disabled={isBatchMerging}
              className="px-3.5 py-1.5 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white text-xs font-bold flex items-center gap-2 shadow-sm transition-all cursor-pointer disabled:opacity-50"
            >
              <Zap className="w-3.5 h-3.5" />
              {isBatchMerging ? 'Birleştiriliyor...' : 'Tüm Yüksek Uyumlu Kümeleri Tek Tıkla Konsolide Et'}
            </button>
          )}
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 bg-slate-100/50">
          {loading ? (
            <div className="flex flex-col items-center justify-center py-16 gap-3 text-slate-400">
              <RefreshCw className="w-8 h-8 animate-spin text-indigo-500" />
              <p className="text-sm font-medium">Taslaklar taranıyor, şık permütasyonları ve kitapçık varyasyonları analiz ediliyor...</p>
            </div>
          ) : activeFilter === 'vague' ? (
            // Vague drafts list
            <div className="space-y-3">
              <div className="p-3 bg-purple-50 border border-purple-200 rounded-xl text-xs text-purple-900 flex items-start gap-2">
                <HelpCircle className="w-4 h-4 text-purple-600 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold">Muğlak Taslaklar Hakkında:</span> Bu sorular başlık, ders veya yeterli şık bilgisi içermediği için henüz hiçbir çapa soruyla güçlü bir eşleşme kuramadı. Öğrenciler bu sorulara yeni ipucu veya şık ekledikçe otomatik olarak ilgili ana soruya bağlanacaktır.
                </div>
              </div>

              {analysis?.unmatchedVagueDrafts.length === 0 ? (
                <div className="text-center py-12 text-slate-400 text-sm">
                  Tebrikler! Eşleşmemiş muğlak taslak bulunmuyor.
                </div>
              ) : (
                analysis?.unmatchedVagueDrafts.map((q) => (
                  <div key={q.id} className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-start justify-between gap-4">
                    <div className="space-y-1 text-xs">
                      <div className="flex items-center gap-2">
                        <span className="font-mono font-bold text-slate-700">#{q.questionNumber || 'Belirsiz'}</span>
                        <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-semibold">{q.discipline}</span>
                        <span className="text-slate-400">{q.topic}</span>
                      </div>
                      <p className="text-slate-800 font-medium">
                        {q.reconstruction?.stem || q.stem || q.fragments?.[0]?.text || 'Metin belirtilmemiş'}
                      </p>
                      {q.options && q.options.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-1 text-[11px] text-slate-600">
                          {q.options.map((o) => (
                            <span key={o.key} className="px-2 py-0.5 rounded bg-slate-50 border border-slate-200">
                              {o.key}) {o.text}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          ) : filteredClusters.length === 0 ? (
            <div className="text-center py-16 text-slate-400 text-sm">
              <CheckCircle2 className="w-10 h-10 text-emerald-500 mx-auto mb-2 opacity-80" />
              <p className="font-semibold text-slate-700">Bu kategoride bekleyen küme bulunmuyor.</p>
              <p className="text-xs text-slate-400 mt-1">Tüm taslaklar ya birleştirildi ya da benzersiz kabul edildi.</p>
            </div>
          ) : (
            // Cluster Cards
            filteredClusters.map((cluster) => {
              const anchor = cluster.anchorQuestion;
              const isExpanded = expandedClusterId === cluster.id;
              const isMerging = mergingClusterId === cluster.id;
              const isReady = cluster.status === 'ready_to_merge';

              return (
                <div
                  key={cluster.id}
                  className={`bg-white rounded-2xl border transition-all shadow-sm overflow-hidden ${
                    isReady ? 'border-emerald-200 shadow-emerald-50/50' : 'border-slate-200'
                  }`}
                >
                  {/* Cluster Card Header */}
                  <div className="p-4 sm:p-5 flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-100 bg-gradient-to-r from-slate-50 to-white">
                    <div className="flex items-start gap-3">
                      <div
                        className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 font-mono font-bold text-sm ${
                          isReady
                            ? 'bg-emerald-100 text-emerald-700 border border-emerald-300'
                            : 'bg-amber-100 text-amber-700 border border-amber-300'
                        }`}
                      >
                        {anchor.isUnassignedNumber ? '?' : `#${anchor.questionNumber}`}
                      </div>
                      <div>
                        <div className="flex flex-wrap items-center gap-2">
                          <h3 className="font-bold text-sm text-slate-900">{anchor.discipline}</h3>
                          <span className="text-xs text-slate-400">·</span>
                          <span className="text-xs font-semibold text-slate-600">{anchor.topic}</span>
                          <span
                            className={`px-2 py-0.5 rounded-full text-[11px] font-bold ${
                              isReady
                                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                : 'bg-amber-50 text-amber-700 border border-amber-200'
                            }`}
                          >
                            %{cluster.overallConfidence} Uyumlu
                          </span>
                        </div>
                        <p className="text-xs text-slate-500 mt-0.5">
                          {cluster.satelliteDrafts.length} adet benzer taslak bu çapa soru etrafında kümelendi.
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 self-end md:self-center">
                      <button
                        onClick={() => setExpandedClusterId(isExpanded ? null : cluster.id)}
                        className="px-3 py-1.5 rounded-lg border border-slate-200 hover:bg-slate-50 text-xs font-semibold text-slate-600 flex items-center gap-1 cursor-pointer"
                      >
                        {isExpanded ? 'Detayları Gizle' : 'Karşılaştır ve İncele'}
                        {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                      </button>

                      <button
                        onClick={() => handleMergeCluster(cluster)}
                        disabled={isMerging}
                        className={`px-4 py-1.5 rounded-lg text-xs font-bold text-white flex items-center gap-1.5 shadow-sm transition-all cursor-pointer disabled:opacity-50 ${
                          isReady
                            ? 'bg-emerald-600 hover:bg-emerald-700'
                            : 'bg-slate-800 hover:bg-slate-900'
                        }`}
                      >
                        <GitMerge className="w-3.5 h-3.5" />
                        {isMerging ? 'Birleştiriliyor...' : 'Bu Kümeyi Birleştir'}
                      </button>
                    </div>
                  </div>

                  {/* Anchor & Satellites Overview */}
                  <div className="p-4 sm:p-5 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                    {/* Left: Anchor Question */}
                    <div className="bg-slate-50/80 p-3.5 rounded-xl border border-slate-200 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-indigo-900 flex items-center gap-1.5">
                          <Layers className="w-3.5 h-3.5 text-indigo-600" />
                          Ana Soru Çatısı (Çapa)
                        </span>
                        <span className="text-[11px] font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">
                          {anchor.options?.length || 0} Şık Mevcut
                        </span>
                      </div>
                      <p className="text-slate-800 line-clamp-3 font-medium">
                        {anchor.reconstruction?.stem || anchor.stem || anchor.fragments?.[0]?.text || 'Soru kökü henüz girilmemiş'}
                      </p>
                      {anchor.options && anchor.options.length > 0 && (
                        <div className="space-y-1 pt-1 border-t border-slate-200">
                          {anchor.options.slice(0, 3).map((o) => (
                            <div key={o.key} className="text-[11px] text-slate-600 truncate">
                              <span className="font-bold font-mono text-slate-800">{o.key})</span> {o.text}
                            </div>
                          ))}
                          {anchor.options.length > 3 && (
                            <span className="text-[10px] text-slate-400 font-medium">
                              +{anchor.options.length - 3} şık daha...
                            </span>
                          )}
                        </div>
                      )}
                    </div>

                    {/* Right: Satellites to be Merged */}
                    <div className="space-y-2">
                      <div className="flex items-center justify-between text-xs font-bold text-slate-700">
                        <span>İç İçe Geçecek Uydu Taslaklar ({cluster.satelliteDrafts.length})</span>
                      </div>

                      <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
                        {cluster.satelliteDrafts.map((sat, idx) => (
                          <div
                            key={sat.question.id || idx}
                            className="p-3 bg-white rounded-xl border border-slate-200 shadow-2xs space-y-1.5"
                          >
                            <div className="flex items-center justify-between">
                              <span className="font-bold text-slate-800">
                                {sat.question.contributedByName || 'Anonim Tıbbiyeli'}
                                {sat.question.questionNumber ? ` · Soru #${sat.question.questionNumber}` : ' · Numarasız'}
                              </span>
                              <span className="font-mono font-bold text-[11px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                                %{sat.compatibility.score} Uyum
                              </span>
                            </div>

                            <p className="text-slate-600 line-clamp-2">
                              {sat.question.reconstruction?.stem || sat.question.stem || sat.question.fragments?.[0]?.text || 'Metin'}
                            </p>

                            {/* Reasons list */}
                            <div className="flex flex-wrap gap-1 text-[10px]">
                              {sat.compatibility.reasons.map((r, rIdx) => (
                                <span key={rIdx} className="bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded">
                                  {r}
                                </span>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Expandable Deep Diff & Reconciliation Details */}
                  {isExpanded && (
                    <div className="p-4 sm:p-5 border-t border-slate-100 bg-slate-50 space-y-3 text-xs animate-in slide-in-from-top-2">
                      <h4 className="font-bold text-slate-800 flex items-center gap-1.5">
                        <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
                        Birleştirme ve Şık Konsolidasyonu Önizlemesi
                      </h4>

                      <div className="p-3 bg-indigo-50 border border-indigo-200 rounded-xl text-indigo-950 space-y-1">
                        <p className="font-semibold">Bu birleştirme uygulandığında:</p>
                        <ul className="list-disc list-inside space-y-0.5 text-[11px] text-indigo-900">
                          <li>Tüm öğrencilerin girdiği ipuçları ve soru parçaları hafıza havuzuna aktarılacak (isimler ve puanlar korunur).</li>
                          <li>Farklı kitapçıklardaki şıklar permütasyon filtresinden geçirilerek eksiksiz 5 şık oluşturulacaktır.</li>
                          <li>Fazladan açılan mükerrer taslaklar veritabanından güvenle arşivlenecek, soru sayısı 100 hedefine yaklaşacaktır.</li>
                        </ul>
                      </div>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>

        {/* Modal Footer */}
        <div className="px-5 py-3 border-t border-slate-200 flex items-center justify-between bg-white text-xs text-slate-500">
          <span>
            MedSoru Çok Katmanlı Kümeleme Motoru · Karışık Şık & Numara Korumalı
          </span>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 font-semibold text-slate-700 cursor-pointer"
          >
            Kapat
          </button>
        </div>
      </div>
    </div>
  );
};
