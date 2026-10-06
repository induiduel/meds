import React, { useState, useEffect, useMemo } from 'react';
import { PageHeader } from './ui/PageHeader';
import {
  Sparkles,
  Search,
  Filter,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  RefreshCw,
  ArrowLeft,
  Check,
  X,
  FileText,
  Clock,
  ExternalLink,
  ShieldCheck,
  ChevronDown,
  Layers,
  Info,
  Terminal,
  Play,
  Square,
  Cpu,
  Cloud,
  ArrowUpDown,
  RotateCcw
} from 'lucide-react';
import { PastQuestionReviewRecord } from '../types';
import { ApiService } from '../services/api';
import { AppUser, ADMIN_EMAIL } from '../services/auth';
import { pathFor } from '../router';

interface TestCikmisViewProps {
  currentUser: AppUser | null;
  isAdmin: boolean;
  onBackToPastExams?: () => void;
}

export const TestCikmisView: React.FC<TestCikmisViewProps> = ({
  currentUser,
  isAdmin,
  onBackToPastExams,
}) => {
  const [allReviews, setAllReviews] = useState<PastQuestionReviewRecord[]>([]);
  const [report, setReport] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters & Sorting
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedReviewId, setSelectedReviewId] = useState<string | null>(null);
  const [sortOrder, setSortOrder] = useState<'newest' | 'oldest'>('newest');

  // Action status
  const [processingId, setProcessingId] = useState<string | null>(null);
  const [actionFeedback, setActionFeedback] = useState<{ message: string; type: 'ok' | 'err' } | null>(null);

  // Runner and log status
  const [liveStatus, setLiveStatus] = useState<{
    isRunning: boolean;
    activeMode: 'cloud' | 'local' | null;
    totalCandidate: number;
    processed: number;
    remaining: number;
    approved: number;
    pending: number;
    report: any;
    logs: string[];
  } | null>(null);
  const [isTriggering, setIsTriggering] = useState(false);
  const [triggerLimit, setTriggerLimit] = useState(15);
  const [showConsole, setShowConsole] = useState(true);

  const fetchLiveStatus = async () => {
    try {
      const data = await ApiService.getPastQuestionReviewLogs();
      setLiveStatus(data);
    } catch (_) {}
  };

  const fetchReviews = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await ApiService.getPastQuestionReviews({ status: 'all' });
      // Soru ID'sine göre tekilleştir (en son işlenen/güncellenen kaydı tut)
      const rawList = data.reviews || [];
      const seen = new Set<string>();
      const deduped: PastQuestionReviewRecord[] = [];
      for (const item of rawList) {
        const qId = String(item.question_id || '');
        if (!qId || seen.has(qId)) continue;
        seen.add(qId);
        deduped.push(item);
      }
      setAllReviews(deduped);
      setReport(data.report || null);
    } catch (err: any) {
      console.error('[TestCikmisView] Fetch error:', err);
      setError(err.message || 'İnceleme kayıtları alınamadı.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchReviews();
    fetchLiveStatus();
    const interval = setInterval(() => {
      fetchLiveStatus();
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleStartReview = async (mode: 'cloud' | 'local') => {
    setIsTriggering(true);
    setActionFeedback(null);
    try {
      const res = await ApiService.triggerPastQuestionReview(ADMIN_EMAIL, mode, triggerLimit);
      setActionFeedback({ message: `✓ ${res.message || 'İşlem başlatıldı.'}`, type: 'ok' });
      await fetchLiveStatus();
      await fetchReviews();
    } catch (err: any) {
      setActionFeedback({ message: `Başlatılamadı: ${err.message}`, type: 'err' });
    } finally {
      setIsTriggering(false);
    }
  };

  const handleStopReview = async () => {
    setIsTriggering(true);
    try {
      await ApiService.stopPastQuestionReview(ADMIN_EMAIL);
      setActionFeedback({ message: '✓ Faz 14 süreci durduruldu.', type: 'ok' });
      await fetchLiveStatus();
    } catch (err: any) {
      setActionFeedback({ message: `Durdurulamadı: ${err.message}`, type: 'err' });
    } finally {
      setIsTriggering(false);
    }
  };

  const handleApprove = async (qId: string) => {
    setProcessingId(qId);
    setActionFeedback(null);
    // İyimser güncelleme
    setAllReviews(prev => prev.map(r => String(r.question_id) === qId ? { ...r, status: 'approved' as any } : r));
    try {
      await ApiService.approvePastQuestionReview(ADMIN_EMAIL, qId);
      setActionFeedback({ message: `✓ Soru #${qId} başarıyla güncellendi ve ana soru havuzuna onaylandı.`, type: 'ok' });
      fetchReviews();
    } catch (err: any) {
      setActionFeedback({ message: `Hata: ${err.message}`, type: 'err' });
      fetchReviews();
    } finally {
      setProcessingId(null);
    }
  };

  const handleReject = async (qId: string) => {
    const reason = 'Yönetici incelemesinde reddedildi.';
    setProcessingId(qId);
    setActionFeedback(null);
    // İyimser güncelleme
    setAllReviews(prev => prev.map(r => String(r.question_id) === qId ? { ...r, status: 'rejected' as any } : r));
    try {
      await ApiService.rejectPastQuestionReview(ADMIN_EMAIL, qId, reason);
      setActionFeedback({ message: `✓ Soru #${qId} önerisi reddedildi.`, type: 'ok' });
      fetchReviews();
    } catch (err: any) {
      setActionFeedback({ message: `Hata: ${err.message}`, type: 'err' });
      fetchReviews();
    } finally {
      setProcessingId(null);
    }
  };

  const handleReEvaluateUnchanged = async (questionId?: string) => {
    setIsTriggering(true);
    setActionFeedback(null);
    try {
      const res = await ApiService.reEvaluateUnchangedPastQuestionReviews(ADMIN_EMAIL, questionId);
      setActionFeedback({
        message: `✓ ${res.message || 'Değişiklik olmayan sorular tekrar değerlendirme kuyruğuna alındı.'}`,
        type: 'ok'
      });
      await fetchReviews();
      await fetchLiveStatus();
    } catch (err: any) {
      setActionFeedback({ message: `Hata: ${err.message}`, type: 'err' });
    } finally {
      setIsTriggering(false);
    }
  };

  const stats = useMemo(() => {
    const total = allReviews.length;
    const pending = allReviews.filter((r) => r.status === 'review_required').length;
    const approved = allReviews.filter((r) => r.status === 'approved').length;
    const rejected = allReviews.filter((r) => r.status === 'rejected').length;
    const unchanged = allReviews.filter((r) => r.status === 'unchanged').length;
    return { total, pending, approved, rejected, unchanged };
  }, [allReviews]);

  const filteredReviews = useMemo(() => {
    let list = allReviews;

    if (statusFilter !== 'all') {
      list = list.filter((r) => r.status === statusFilter);
    }

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      list = list.filter((r) => {
        const idMatch = String(r.question_id || '').toLowerCase().includes(q);
        const stemMatch = String(r.source?.soru_koku || '').toLowerCase().includes(q);
        const propMatch = String(r.proposal?.soru_koku || '').toLowerCase().includes(q);
        const discMatch = String(r.source?.ders_adi || r.proposal?.ders_adi || '').toLowerCase().includes(q);
        const summaryMatch = String(r.proposal?.degisiklik_ozeti || '').toLowerCase().includes(q);
        return idMatch || stemMatch || propMatch || discMatch || summaryMatch;
      });
    }

    // Sıralama: En son eklenen / işlenen soru en başta (varsayılan)
    const sorted = [...list].sort((a, b) => {
      const tA = new Date(a.processed_at || 0).getTime();
      const tB = new Date(b.processed_at || 0).getTime();
      return sortOrder === 'newest' ? tB - tA : tA - tB;
    });

    return sorted;
  }, [allReviews, statusFilter, searchQuery, sortOrder]);

  return (
    <div className="flex flex-col gap-4 pb-16 min-w-0 w-full max-w-[1400px] mx-auto">
      <PageHeader
        eyebrow="Faz 14 · Canlı Test & İnceleme Katmanı"
        title="Test Edilen Çıkmış Sorular"
        description="Yerel model (gemma3:4b) ve bulut yapay zeka tarafından üretilen kanıta dayalı OCR/imla redaksiyon önerileri. Canlı soru havuzuna doğrudan yazılmaz; yalnızca onaylanan kayıtlar ana veri tabanına işlenir."
        stats={[
          { label: 'İncelenen Soru', value: stats.total.toLocaleString('tr-TR') },
          { label: 'İnceleme Bekleyen', value: stats.pending.toLocaleString('tr-TR'), tone: stats.pending > 0 ? 'warn' : 'default' },
          { label: 'Onaylanan', value: stats.approved.toLocaleString('tr-TR'), tone: 'ok' },
          { label: 'Reddedilen', value: stats.rejected.toLocaleString('tr-TR'), tone: 'default' },
        ]}
        actions={
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={fetchReviews}
              disabled={isLoading}
              className="h-10 px-3.5 rounded-xl border border-line bg-white text-ink text-[13.5px] font-semibold inline-flex items-center gap-2 hover:bg-canvas cursor-pointer disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin text-accent' : ''}`} />
              <span>Yenile</span>
            </button>
            <a
              href={pathFor('past_exams')}
              onClick={(e) => {
                if (onBackToPastExams) {
                  e.preventDefault();
                  onBackToPastExams();
                }
              }}
              className="h-10 px-4 rounded-xl bg-accent text-white font-semibold text-[13.5px] inline-flex items-center gap-2 hover:bg-accent-hover cursor-pointer"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Çıkmış Sorulara Dön</span>
            </a>
          </div>
        }
      />

      {/* Canlı İşlem, Kalan Soru & Manuel Çalıştırma Kontrol Paneli (Sadece Admin) */}
      {isAdmin && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-white shadow-lg space-y-4">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className={`w-2.5 h-2.5 rounded-full ${liveStatus?.isRunning ? 'bg-emerald-400 animate-ping' : 'bg-slate-500'}`} />
                <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
                  Faz 14 Canlı Süreç ve Denetim Kokpiti
                </span>
              {liveStatus?.isRunning && (
                <span className="text-[11px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-bold">
                  ● {liveStatus.activeMode === 'cloud' ? 'Google Gemini Flash-Lite / Flash (En Düşük Maliyet)' : 'Gemma 3 (Yerel RTX 4060 GPU)'} Çalışıyor
                </span>
              )}
            </div>
            <p className="text-xs text-slate-400">
              Çıkmış sınav sorularını tıbbi literatüre göre tarar, eksik kök ve şıkları düzeltir, YZV bloğuyla inceleme katmanına aktarır.
            </p>
          </div>

          {/* Manuel Tetikleme Butonları */}
          <div className="flex flex-wrap items-center gap-2">
            <div className="flex items-center gap-1.5 bg-slate-800/80 px-2.5 py-1 rounded-xl border border-slate-700">
              <span className="text-[11px] text-slate-400">Parti:</span>
              <select
                value={triggerLimit}
                onChange={(e) => setTriggerLimit(Number(e.target.value))}
                className="bg-transparent text-white text-xs font-bold outline-0 cursor-pointer"
              >
                <option value={5} className="bg-slate-800 text-white">5 Soru</option>
                <option value={10} className="bg-slate-800 text-white">10 Soru</option>
                <option value={25} className="bg-slate-800 text-white">25 Soru</option>
                <option value={50} className="bg-slate-800 text-white">50 Soru</option>
              </select>
            </div>

            <button
              type="button"
              onClick={() => handleStartReview('cloud')}
              disabled={isTriggering || liveStatus?.isRunning}
              className="h-9 px-3.5 rounded-xl bg-gradient-to-r from-indigo-500 to-violet-600 hover:from-indigo-600 hover:to-violet-700 text-white font-bold text-xs inline-flex items-center gap-1.5 transition disabled:opacity-50 cursor-pointer shadow-md"
            >
              <Cloud className="w-3.5 h-3.5" />
              <span>Bulut Başlat (Gemini)</span>
            </button>

            <button
              type="button"
              onClick={() => handleStartReview('local')}
              disabled={isTriggering || liveStatus?.isRunning}
              className="h-9 px-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-bold text-xs inline-flex items-center gap-1.5 transition disabled:opacity-50 cursor-pointer"
            >
              <Cpu className="w-3.5 h-3.5 text-emerald-400" />
              <span>Yerel Başlat (RTX 4060)</span>
            </button>

            {liveStatus?.isRunning && (
              <button
                type="button"
                onClick={handleStopReview}
                disabled={isTriggering}
                className="h-9 px-3.5 rounded-xl bg-rose-600/90 hover:bg-rose-600 text-white font-bold text-xs inline-flex items-center gap-1.5 transition cursor-pointer"
              >
                <Square className="w-3.5 h-3.5" />
                <span>Durdur</span>
              </button>
            )}

            <button
              type="button"
              onClick={() => setShowConsole(!showConsole)}
              className="h-9 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 font-semibold text-xs inline-flex items-center gap-1.5 transition cursor-pointer"
            >
              <Terminal className="w-3.5 h-3.5 text-amber-400" />
              <span>{showConsole ? 'Konsolu Gizle' : 'Konsolu Aç'}</span>
            </button>
          </div>
        </div>

        {/* İlerleme ve Kalan Soru Metrikleri */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 border-t border-slate-800 text-center font-mono">
          <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[10px] uppercase text-slate-400 block">Toplam Havuz</span>
            <strong className="text-base text-slate-200">4.926</strong>
            <span className="text-[10px] text-slate-500 block">Aday Çıkmış</span>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[10px] uppercase text-slate-400 block">İşlenen Soru</span>
            <strong className="text-base text-cyan-400">{liveStatus?.processed ?? allReviews.length}</strong>
            <span className="text-[10px] text-cyan-500 block">reviews.jsonl</span>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[10px] uppercase text-slate-400 block">Kalan Soru</span>
            <strong className="text-base text-amber-400">{liveStatus?.remaining ?? Math.max(0, 4926 - allReviews.length)}</strong>
            <span className="text-[10px] text-amber-500 block">Sırada Bekleyen</span>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[10px] uppercase text-slate-400 block">Onaylanan</span>
            <strong className="text-base text-emerald-400">{liveStatus?.approved ?? stats.approved}</strong>
            <span className="text-[10px] text-emerald-500 block">Ana Havuza Aktarıldı</span>
          </div>
        </div>

        {/* Canlı Konsol Log Alanı (Terminal Çıktısı) */}
        {showConsole && (
          <div className="pt-2 border-t border-slate-800/80 space-y-1.5">
            <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono">
              <span className="flex items-center gap-1.5 text-slate-300">
                <Terminal className="w-3.5 h-3.5 text-amber-400" />
                <span>Canlı Terminal & Log Akışı (phase14.log)</span>
              </span>
              <span>Son 50 satır</span>
            </div>
            <div className="bg-slate-950 p-3 rounded-xl border border-slate-800/80 font-mono text-xs text-slate-300 max-h-48 overflow-y-auto space-y-1 select-text">
              {liveStatus?.logs && liveStatus.logs.length > 0 ? (
                liveStatus.logs.map((line, idx) => {
                  const isErr = line.includes('ERROR') || line.includes('hata') || line.includes('429') || line.includes('404');
                  const isOk = line.includes('✓') || line.includes('başarıyla') || line.includes('unchanged');
                  const isWarn = line.includes('WARNING') || line.includes('review_required');
                  return (
                    <div
                      key={idx}
                      className={`leading-relaxed whitespace-pre-wrap ${
                        isErr
                          ? 'text-rose-400'
                          : isOk
                          ? 'text-emerald-400'
                          : isWarn
                          ? 'text-amber-300'
                          : 'text-slate-300'
                      }`}
                    >
                      {line}
                    </div>
                  );
                })
              ) : (
                <div className="text-slate-500 italic">Henüz log kaydı yok veya işlem bekleniyor...</div>
              )}
            </div>
          </div>
        )}
        </div>
      )}

      {actionFeedback && (
        <div
          className={`p-3.5 rounded-xl border text-[13.5px] font-medium flex items-center justify-between gap-2 ${
            actionFeedback.type === 'ok'
              ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
              : 'bg-rose-50 text-rose-800 border-rose-200'
          }`}
        >
          <span>{actionFeedback.message}</span>
          <button
            type="button"
            onClick={() => setActionFeedback(null)}
            className="p-1 text-ink-3 hover:text-ink cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Arama & Durum Filtreleri */}
      <div className="flex flex-col sm:flex-row gap-2.5">
        <label className="flex-1 flex items-center gap-2 h-11 px-3.5 rounded-xl bg-white border border-line focus-within:border-accent">
          <Search className="w-4 h-4 text-ink-3 shrink-0" />
          <input
            type="search"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Soru ID, kök, ders ya da değişiklik özeti ara..."
            className="flex-1 bg-transparent border-0 outline-0 text-[14.5px] text-ink placeholder:text-ink-3"
          />
          {searchQuery && (
            <button
              type="button"
              onClick={() => setSearchQuery('')}
              className="text-ink-3 hover:text-ink cursor-pointer p-1"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </label>

        <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar pb-1 sm:pb-0">
          {[
            { id: 'all', label: 'Tümü', count: stats.total },
            { id: 'review_required', label: 'İnceleme Gerekli', count: stats.pending },
            { id: 'approved', label: 'Onaylandı', count: stats.approved },
            { id: 'rejected', label: 'Reddedildi', count: stats.rejected },
            { id: 'unchanged', label: 'Değişiklik Yok', count: stats.unchanged },
          ].map((tab) => {
            const on = statusFilter === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                onClick={() => setStatusFilter(tab.id)}
                className={`h-11 px-3.5 sm:px-4 rounded-xl text-[13.5px] font-semibold whitespace-nowrap cursor-pointer transition-colors inline-flex items-center gap-1.5 ${
                  on
                    ? 'bg-accent text-white shadow-xs'
                    : 'bg-white text-ink-2 border border-line hover:text-ink hover:bg-canvas'
                }`}
              >
                <span>{tab.label}</span>
                <span className={`text-[11px] px-1.5 py-0.2 rounded-full font-mono ${
                  on ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-600'
                }`}>
                  {tab.count}
                </span>
              </button>
            );
          })}

          {/* Sıralama Butonu */}
          <button
            type="button"
            onClick={() => setSortOrder(prev => prev === 'newest' ? 'oldest' : 'newest')}
            className="h-11 px-3.5 rounded-xl border border-line bg-white hover:bg-canvas text-ink-2 hover:text-ink text-[13px] font-semibold whitespace-nowrap inline-flex items-center gap-1.5 cursor-pointer shadow-xs ml-1"
            title="Sıralamayı Değiştir"
          >
            <ArrowUpDown className="w-4 h-4 text-accent" />
            <span>{sortOrder === 'newest' ? 'En Yeni İlk' : 'En Eski İlk'}</span>
          </button>

          {/* Admin: Değişiklik Olmayanları Tekrar Değerlendir Butonu */}
          {isAdmin && stats.unchanged > 0 && (
            <button
              type="button"
              onClick={() => handleReEvaluateUnchanged()}
              disabled={isTriggering}
              className="h-11 px-3.5 rounded-xl border border-amber-300 bg-amber-50 hover:bg-amber-100 text-amber-800 text-[13px] font-bold whitespace-nowrap inline-flex items-center gap-1.5 cursor-pointer shadow-xs ml-1 transition disabled:opacity-50"
              title="Değişiklik yapılmamış tüm soruları checkpoint'ten çıkarıp Faz 14 için tekrar hazırla"
            >
              <RotateCcw className="w-3.5 h-3.5 text-amber-600" />
              <span>Değişiklik Olmayanları Tekrar Değerlendir ({stats.unchanged})</span>
            </button>
          )}
        </div>
      </div>

      {/* Liste & Karşılaştırma Kartları */}
      {isLoading ? (
        <div className="bg-white border border-line rounded-2xl p-12 text-center text-ink-2 flex flex-col items-center gap-3">
          <RefreshCw className="w-6 h-6 animate-spin text-accent" />
          <span className="text-[14px]">İnceleme kuyruğu ve Faz 14 önerileri yükleniyor...</span>
        </div>
      ) : error ? (
        <div className="bg-white border border-rose-200 rounded-2xl p-8 text-center text-rose-700 flex flex-col items-center gap-2">
          <AlertTriangle className="w-8 h-8 text-rose-500" />
          <p className="font-semibold">{error}</p>
          <button
            type="button"
            onClick={fetchReviews}
            className="mt-2 h-9 px-4 rounded-lg bg-rose-600 text-white text-xs font-semibold cursor-pointer"
          >
            Yeniden Dene
          </button>
        </div>
      ) : filteredReviews.length === 0 ? (
        <div className="bg-white border border-line rounded-2xl p-12 text-center text-ink-2 flex flex-col items-center gap-2">
          <Sparkles className="w-8 h-8 text-ink-3" />
          <h3 className="font-bold text-[16px] text-ink">Henüz İnceleme Kaydı Bulunamadı</h3>
          <p className="text-[13.5px] max-w-md text-ink-3">
            {searchQuery
              ? 'Arama kriterlerine uygun öneri bulunamadı.'
              : 'Faz 14 betiği (phase14_past_question_editor.py) henüz bu filtre için kayıt üretmedi. Yönetim panelinden "Script ve görevler" sekmesini kullanarak partiler halinde çalıştırabilirsiniz.'}
          </p>
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          {filteredReviews.map((rev) => {
            const qId = rev.question_id;
            const src = rev.source || ({} as any);
            const prop = rev.proposal || ({} as any);
            const isPending = rev.status === 'review_required';
            const isApproved = rev.status === 'approved';
            const isRejected = rev.status === 'rejected';
            const isUnchanged = rev.status === 'unchanged';
            const ratioPercent = Math.round((rev.support_ratio || 0) * 100);
            const isSelected = selectedReviewId === qId;

            return (
              <article
                key={qId}
                className={`bg-white border rounded-2xl transition-all shadow-xs overflow-hidden ${
                  isSelected ? 'border-accent ring-2 ring-accent/20' : 'border-line hover:border-line-2'
                }`}
              >
                {/* Header bar */}
                <div className="px-4 sm:px-6 py-3.5 bg-canvas border-b border-line flex flex-wrap items-center justify-between gap-3">
                  <div className="flex items-center gap-2.5 min-w-0">
                    <span className="font-mono font-bold text-[14px] text-ink px-2.5 py-1 rounded-lg bg-white border border-line">
                      #{qId}
                    </span>
                    {src.kurul_adi && (
                      <span className="text-[12px] font-semibold px-2 py-0.5 rounded-md bg-blue-50 text-blue-700 border border-blue-200 truncate max-w-[200px]">
                        {src.kurul_adi}
                      </span>
                    )}
                    {src.ders_adi && (
                      <span className="text-[12px] font-medium text-ink-3 truncate">
                        {src.ders_adi}
                      </span>
                    )}
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <span
                      className={`text-[11.5px] font-semibold px-2.5 py-1 rounded-full border flex items-center gap-1 ${
                        isApproved
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-300'
                          : isRejected
                          ? 'bg-rose-50 text-rose-700 border-rose-300'
                          : isUnchanged
                          ? 'bg-slate-100 text-slate-700 border-slate-300'
                          : isPending
                          ? 'bg-amber-50 text-amber-700 border-amber-300'
                          : 'bg-slate-50 text-slate-700 border-slate-300'
                      }`}
                    >
                      {isApproved ? (
                        <>
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                          <span>Onaylandı</span>
                        </>
                      ) : isRejected ? (
                        <>
                          <XCircle className="w-3.5 h-3.5 text-rose-600" />
                          <span>Reddedildi</span>
                        </>
                      ) : isUnchanged ? (
                        <>
                          <Check className="w-3.5 h-3.5 text-slate-500" />
                          <span>Değişiklik Yok</span>
                        </>
                      ) : (
                        <>
                          <Clock className="w-3.5 h-3.5 text-amber-600" />
                          <span>İnceleme Bekliyor</span>
                        </>
                      )}
                    </span>

                    <span
                      className={`text-[11.5px] font-mono font-semibold px-2 py-1 rounded-md border ${
                        ratioPercent >= 80
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                          : 'bg-rose-50 text-rose-700 border-rose-200'
                      }`}
                      title={`Kaynak metinle token örtüşme desteği: %${ratioPercent}`}
                    >
                      Kanıt: %{ratioPercent}
                    </span>

                    {/* Admin Onay / Red Butonları */}
                    {isAdmin && (
                      <div className="flex items-center gap-1.5 ml-2">
                        {!isApproved && (
                          <button
                            type="button"
                            onClick={() => handleApprove(qId)}
                            disabled={processingId === qId}
                            className="h-8 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold inline-flex items-center gap-1 cursor-pointer disabled:opacity-50"
                            title="Öneriyi onayla ve canlı geçmiş sınav sorularına uygula"
                          >
                            <Check className="w-3.5 h-3.5" />
                            <span>Onayla</span>
                          </button>
                        )}
                        {!isRejected && (
                          <button
                            type="button"
                            onClick={() => handleReject(qId)}
                            disabled={processingId === qId}
                            className="h-8 px-2.5 rounded-lg border border-line bg-white hover:bg-rose-50 hover:text-rose-600 text-ink-2 text-xs font-medium inline-flex items-center gap-1 cursor-pointer disabled:opacity-50"
                            title="Öneriyi reddet"
                          >
                            <X className="w-3.5 h-3.5" />
                            <span>Reddet</span>
                          </button>
                        )}
                        {(isUnchanged || isRejected) && (
                          <button
                            type="button"
                            onClick={() => handleReEvaluateUnchanged(qId)}
                            disabled={processingId === qId || isTriggering}
                            className="h-8 px-2.5 rounded-lg border border-amber-300 bg-amber-50 hover:bg-amber-100 text-amber-800 text-xs font-semibold inline-flex items-center gap-1 cursor-pointer disabled:opacity-50"
                            title="Bu soruyu tekrar Faz 14 değerlendirme kuyruğuna al"
                          >
                            <RotateCcw className="w-3.5 h-3.5 text-amber-600" />
                            <span>Tekrar Değerlendir</span>
                          </button>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                {/* Content: Side-by-side or stacked diff comparison */}
                <div className="p-4 sm:p-6 grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
                  {/* Sol Kolon: Mevcut Kaynak Soru */}
                  <div className="flex flex-col gap-3 p-4 rounded-xl bg-slate-50/80 border border-slate-200">
                    <div className="flex items-center justify-between pb-2 border-b border-slate-200">
                      <span className="text-xs font-bold uppercase tracking-wider text-slate-600 flex items-center gap-1.5">
                        <FileText className="w-3.5 h-3.5" />
                        <span>Mevcut Kayıt (Kaynak Veri)</span>
                      </span>
                      {src.dogru_secenek && (
                        <span className="font-mono font-bold text-xs bg-white px-2 py-0.5 rounded border border-slate-200 text-slate-700">
                          Cevap: {src.dogru_secenek}
                        </span>
                      )}
                    </div>

                    <div className="text-[14px] leading-relaxed text-slate-800 font-medium whitespace-pre-wrap">
                      {src.soru_koku || <span className="text-slate-400 italic">(Soru kökü boş)</span>}
                    </div>

                    {src.secenekler && Object.keys(src.secenekler).length > 0 && (
                      <div className="space-y-1.5 pt-1">
                        {Object.entries(src.secenekler).map(([k, v]) => (
                          <div
                            key={k}
                            className={`p-2 rounded-lg text-[13px] flex items-start gap-2 border ${
                              k === src.dogru_secenek
                                ? 'bg-emerald-50 border-emerald-200 text-emerald-900 font-semibold'
                                : 'bg-white border-slate-200 text-slate-700'
                            }`}
                          >
                            <span className="font-mono font-bold shrink-0">{k})</span>
                            <span className="flex-1">{String(v)}</span>
                          </div>
                        ))}
                      </div>
                    )}

                    {src.aciklama && (
                      <div className="text-xs bg-white p-2.5 rounded-lg border border-slate-200 text-slate-600 space-y-1">
                        <span className="font-bold text-slate-700 block">Mevcut Açıklama:</span>
                        <p className="whitespace-pre-wrap leading-relaxed">{src.aciklama}</p>
                      </div>
                    )}
                  </div>

                  {/* Sağ Kolon: Yerel Modelin Redaksiyon Önerisi */}
                  <div className="flex flex-col gap-3 p-4 rounded-xl bg-violet-50/50 border border-violet-200">
                    <div className="flex items-center justify-between pb-2 border-b border-violet-200">
                      <span className="text-xs font-bold uppercase tracking-wider text-violet-800 flex items-center gap-1.5">
                        <Sparkles className="w-3.5 h-3.5 text-violet-600" />
                        <span>Yerel AI Redaksiyon Önerisi</span>
                      </span>
                      {prop.dogru_secenek && (
                        <span className="font-mono font-bold text-xs bg-white px-2 py-0.5 rounded border border-violet-200 text-violet-800">
                          Önerilen: {prop.dogru_secenek}
                        </span>
                      )}
                    </div>

                    <div className="text-[14px] leading-relaxed text-violet-950 font-medium whitespace-pre-wrap">
                      {prop.soru_koku || <span className="text-violet-400 italic">(Değişiklik önerilmedi)</span>}
                    </div>

                    {prop.secenekler && Object.keys(prop.secenekler).length > 0 && (
                      <div className="space-y-1.5 pt-1">
                        {Object.entries(prop.secenekler).map(([k, v]) => {
                          const upperKey = k.toUpperCase();
                          const srcHasOption = Boolean(src.secenekler && (src.secenekler[k] || src.secenekler[upperKey]));
                          const aiCompletedList: string[] = (prop.yapay_zeka_tamamlanan_siklar || []).map((x: any) => String(x).toUpperCase());
                          const isAiCompleted = !srcHasOption || aiCompletedList.includes(upperKey);

                          return (
                            <div
                              key={k}
                              className={`p-2 rounded-lg text-[13px] flex items-start gap-2 border ${
                                k === prop.dogru_secenek
                                  ? 'bg-emerald-50 border-emerald-200 text-emerald-900 font-semibold'
                                  : isAiCompleted
                                  ? 'bg-purple-50/80 border-purple-200 text-purple-950'
                                  : 'bg-white border-violet-200 text-violet-900'
                              }`}
                            >
                              <span className="font-mono font-bold shrink-0">{k})</span>
                              <span className="flex-1">{String(v)}</span>
                              {isAiCompleted && (
                                <span className="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[10.5px] font-bold bg-purple-100 text-purple-700 border border-purple-200 shrink-0">
                                  <Sparkles className="w-3 h-3 text-purple-600" />
                                  <span>AI Tamamladı</span>
                                </span>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    )}

                    {prop.aciklama && (
                      <div className="text-xs bg-white p-2.5 rounded-lg border border-violet-200 text-violet-900 space-y-1">
                        <span className="font-bold text-violet-950 block">Önerilen Açıklama:</span>
                        <p className="whitespace-pre-wrap leading-relaxed">{prop.aciklama}</p>
                      </div>
                    )}

                    {prop.degisiklik_ozeti && (
                      <div className="text-xs bg-amber-50/80 p-2.5 rounded-lg border border-amber-200 text-amber-900 flex items-start gap-1.5">
                        <Info className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                        <div>
                          <span className="font-bold">Değişiklik Özeti:</span> {typeof prop.degisiklik_ozeti === 'string' ? prop.degisiklik_ozeti : JSON.stringify(prop.degisiklik_ozeti)}
                          {prop.degisen_alanlar && prop.degisen_alanlar.length > 0 && (
                            <span className="block mt-1 text-[11px] text-amber-800">
                              Değişen alanlar: {prop.degisen_alanlar.join(', ')}
                            </span>
                          )}
                        </div>
                      </div>
                    )}

                    {prop.YZV && (
                      <div className="text-xs bg-violet-100/70 p-2.5 rounded-lg border border-violet-300 text-violet-950 space-y-1">
                        <div className="font-bold flex items-center gap-1.5 text-violet-900">
                          <Sparkles className="w-3.5 h-3.5 text-violet-700" />
                          <span>YZV (Yapay Zeka Verisi) Doğrulama Bloğu</span>
                        </div>
                        {prop.YZV.referans_literatur && (
                          <p className="text-[12px]"><strong className="text-violet-900">Referans Literatür:</strong> {prop.YZV.referans_literatur}</p>
                        )}
                        {prop.YZV.degisiklik_ozeti && typeof prop.YZV.degisiklik_ozeti === 'object' && (
                          <div className="text-[11.5px] bg-white/80 p-2 rounded border border-violet-200 space-y-0.5 mt-1">
                            {prop.YZV.degisiklik_ozeti.soru_koku_duzeltmesi && (
                              <p><strong>Kök Düzeltmesi:</strong> {prop.YZV.degisiklik_ozeti.soru_koku_duzeltmesi}</p>
                            )}
                            {prop.YZV.degisiklik_ozeti.aciklama_duzeltmesi && (
                              <p><strong>Açıklama:</strong> {prop.YZV.degisiklik_ozeti.aciklama_duzeltmesi}</p>
                            )}
                            {prop.YZV.degisiklik_ozeti.mufredat_atamasi && (
                              <p><strong>Müfredat:</strong> {prop.YZV.degisiklik_ozeti.mufredat_atamasi}</p>
                            )}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                {/* Footer metadata */}
                <div className="px-4 sm:px-6 py-2.5 bg-slate-50 border-t border-line flex flex-wrap items-center justify-between gap-2 text-[11.5px] text-ink-3">
                  <div className="flex items-center gap-3">
                    <span>Model: <strong className="font-mono text-ink-2">{rev.model || 'gemma3:4b'}</strong></span>
                    <span>İşlem: <strong className="font-mono text-ink-2">{rev.processed_at?.replace('T', ' ')}</strong></span>
                    {rev.approved_at && (
                      <span className="text-emerald-700 font-medium">
                        Onay: {rev.approved_at.slice(0, 19).replace('T', ' ')} ({rev.approved_by})
                      </span>
                    )}
                    {rev.rejected_at && (
                      <span className="text-rose-700 font-medium">
                        Red: {rev.rejected_at.slice(0, 19).replace('T', ' ')} ({rev.reject_reason || rev.rejected_by})
                      </span>
                    )}
                  </div>

                  <a
                    href={`/v1/past-exams?query=${encodeURIComponent(qId)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-ink-2 hover:text-accent font-medium"
                  >
                    <span>Canlı API'de İncele</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
};
