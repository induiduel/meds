import React, { useState, useEffect, useMemo } from 'react';
import { PageHeader } from './ui/PageHeader';
import {
  Sparkles,
  Search,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  RefreshCw,
  ArrowLeft,
  Check,
  X,
  FileText,
  Clock,
  Terminal,
  Square,
  Cloud,
  ArrowUpDown,
  RotateCcw,
  Edit3,
  DollarSign,
  Copy,
} from 'lucide-react';
import { PastQuestionReviewRecord } from '../types';
import { ApiService } from '../services/api';
import { AppUser, ADMIN_EMAIL } from '../services/auth';
import { pathFor } from '../router';

// Kelime düzeyinde fark (LCS). Kök birkaç yüz kelimeyi geçmez; 400 kelime üstünde fark çizilmez.
type DiffPart = { t: string; k: 'same' | 'add' | 'del' };
function wordDiff(a: string, b: string): DiffPart[] | null {
  const A = a.split(/(\s+)/).filter(Boolean);
  const B = b.split(/(\s+)/).filter(Boolean);
  if (A.length > 800 || B.length > 800) return null;
  const n = A.length, m = B.length;
  const dp: number[][] = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(0));
  for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--) dp[i][j] = A[i] === B[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
  const out: DiffPart[] = [];
  let i = 0, j = 0;
  const push = (t: string, k: DiffPart['k']) => (out.length && out[out.length - 1].k === k ? (out[out.length - 1].t += t) : out.push({ t, k }));
  while (i < n && j < m) {
    if (A[i] === B[j]) { push(A[i], 'same'); i++; j++; }
    else if (dp[i + 1][j] >= dp[i][j + 1]) push(A[i++], 'del');
    else push(B[j++], 'add');
  }
  while (i < n) push(A[i++], 'del');
  while (j < m) push(B[j++], 'add');
  return out;
}

function DiffText({ before, after }: { before: string; after: string }) {
  const parts = useMemo(() => wordDiff(before, after), [before, after]);
  if (!parts) return <>{after}</>;
  return (
    <>
      {parts.map((p, i) =>
        p.k === 'same' ? (
          <span key={i}>{p.t}</span>
        ) : p.k === 'add' ? (
          <ins key={i} className="no-underline bg-emerald-100 text-emerald-900 rounded-sm px-0.5">{p.t}</ins>
        ) : /\S/.test(p.t) ? (
          <del key={i} className="bg-rose-100 text-rose-800 rounded-sm px-0.5 decoration-rose-500">{p.t}</del>
        ) : null,
      )}
    </>
  );
}

const PAGE_SIZE = 30;

// Kurul adı iki biçimde gelir: kaynakta "donem3-kurul1", öneride "TIP310". Karşılaştırma ve gösterim için tek biçim.
function kurulKey(v?: string): string {
  const s = String(v || '').trim();
  let m = s.match(/kurul\s*-?\s*(\d)/i) || s.match(/^TIP\s*3(\d)0$/i);
  if (m) return `kurul${m[1]}`;
  if (/final/i.test(s)) return 'final';
  if (/b[uü]t[uü]nleme/i.test(s)) return 'butunleme';
  return s.toLocaleLowerCase('tr-TR');
}
function kurulLabel(v?: string): string {
  const k = kurulKey(v);
  if (/^kurul\d$/.test(k)) return `Kurul ${k.slice(5)}`;
  if (k === 'final') return 'Final';
  if (k === 'butunleme') return 'Bütünleme';
  return String(v || '');
}
type CurriculumChange = { alan: string; eski: string; yeni: string };
function curriculumChanges(src: any, prop: any): CurriculumChange[] {
  const out: CurriculumChange[] = [];
  if (!prop) return out;
  if (prop.kurul_adi && kurulKey(prop.kurul_adi) !== kurulKey(src?.kurul_adi))
    out.push({ alan: 'Kurul', eski: kurulLabel(src?.kurul_adi) || '—', yeni: kurulLabel(prop.kurul_adi) });
  const norm = (x?: string) => String(x || '').trim().toLocaleLowerCase('tr-TR');
  if (prop.ders_adi && norm(prop.ders_adi) !== norm(src?.ders_adi)) out.push({ alan: 'Ders', eski: src?.ders_adi || '—', yeni: prop.ders_adi });
  if (prop.konu_adi && norm(prop.konu_adi) !== norm(src?.konu_adi)) out.push({ alan: 'Konu', eski: src?.konu_adi || '—', yeni: prop.konu_adi });
  return out;
}
function questionText(rev: PastQuestionReviewRecord, which: 'src' | 'prop'): string {
  const src: any = rev.source || {};
  const prop: any = rev.proposal || {};
  const q = which === 'prop' && prop.soru_koku ? prop : src;
  const opts = q.secenekler && Object.keys(q.secenekler).length ? q.secenekler : src.secenekler || {};
  const lines: string[] = [];
  const ch = which === 'prop' ? curriculumChanges(src, prop) : [];
  if (ch.length) lines.push(`[Müfredat değişikliği: ${ch.map((c) => (c.alan === 'Kurul' ? `${c.eski} → ${c.yeni}` : `${c.alan}: ${c.eski} → ${c.yeni}`)).join(' · ')}]`);
  const meta = [kurulLabel(q.kurul_adi || src.kurul_adi), q.ders_adi || src.ders_adi, q.konu_adi || src.konu_adi].filter(Boolean).join(' · ');
  if (meta) lines.push(meta);
  lines.push('', String(q.soru_koku || '').trim(), '');
  for (const [k, v] of Object.entries(opts)) lines.push(`${k.toUpperCase()}) ${String(v).trim()}`);
  return lines.join('\n').trim();
}
async function copyText(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    try {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      const ok = document.execCommand('copy');
      ta.remove();
      return ok;
    } catch {
      return false;
    }
  }
}
const modelLabel = (m?: string) => {
  const s = String(m || '').toLowerCase();
  if (!s) return 'AI önerisi';
  if (s.includes('gemini')) return 'Gemini önerisi';
  if (s.includes('muse')) return 'Muse Spark önerisi';
  if (s.includes('gemma') || s.includes('qwen')) return 'Yerel model önerisi';
  return `${m} önerisi`;
};

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
  const [sortOrder, setSortOrder] = useState<'newest' | 'oldest' | 'evidence_low' | 'evidence_high'>('newest');
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
  // Telefonda kart başına görünüm: fark (varsayılan) | mevcut | öneri
  const [cardView, setCardView] = useState<Record<string, 'diff' | 'src' | 'prop'>>({});
  const [copiedId, setCopiedId] = useState<string | null>(null);
  // Görünüm: "list" (her soru tek satır, tıklayınca açılır) | "detail" (tam karşılaştırma kartı). Cihazda hatırlanır.
  const [layout, setLayout] = useState<'list' | 'detail'>(() => {
    try {
      return (localStorage.getItem('tc_layout') as 'list' | 'detail') || 'detail';
    } catch {
      return 'detail';
    }
  });
  const [openRows, setOpenRows] = useState<Record<string, boolean>>({});
  const changeLayout = (v: 'list' | 'detail') => {
    setLayout(v);
    try {
      localStorage.setItem('tc_layout', v);
    } catch {
      /* depolama kapalı */
    }
  };

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
    costTracking?: {
      month: string;
      total_requests: number;
      input_tokens: number;
      output_tokens: number;
      cost_usd: number;
      cost_tl: number;
      max_budget_tl: number;
      last_updated: string;
    } | null;
    logs: string[];
  } | null>(null);
  const [isTriggering, setIsTriggering] = useState(false);
  const [triggerLimit, setTriggerLimit] = useState(15);
  const [showConsole, setShowConsole] = useState(() => typeof window === 'undefined' || window.innerWidth >= 1024);

  // Edit proposal modal state
  const [editingReview, setEditingReview] = useState<PastQuestionReviewRecord | null>(null);
  const [editStem, setEditStem] = useState('');
  const [editOptions, setEditOptions] = useState<{ A: string; B: string; C: string; D: string; E: string }>({
    A: '', B: '', C: '', D: '', E: ''
  });
  const [editCorrectAnswer, setEditCorrectAnswer] = useState('A');
  const [editExplanation, setEditExplanation] = useState('');
  const [editSummary, setEditSummary] = useState('');
  const [isSavingEdit, setIsSavingEdit] = useState(false);

  const fetchLiveStatus = async () => {
    try {
      const data = await ApiService.getPastQuestionReviewLogs();
      setLiveStatus(data);
    } catch (_) {}
  };

  // silent: işlem sonrası arkada yenile — liste yükleme ekranıyla değişmez, kaydırma konumu korunur
  const fetchReviews = async (silent = false) => {
    if (!silent) setIsLoading(true);
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
      if (!silent) setError(err.message || 'İnceleme kayıtları alınamadı.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchReviews();
    if (!isAdmin) return;
    fetchLiveStatus();
    const interval = setInterval(() => {
      if (!document.hidden) fetchLiveStatus();
    }, 3000);
    return () => clearInterval(interval);
  }, [isAdmin]);

  // filtre/arama değişince listeyi başa al
  useEffect(() => setVisibleCount(PAGE_SIZE), [statusFilter, searchQuery, sortOrder]);

  const handleStartReview = async (mode: 'cloud' | 'local') => {
    setIsTriggering(true);
    setActionFeedback(null);
    try {
      const res = await ApiService.triggerPastQuestionReview(ADMIN_EMAIL, mode, triggerLimit);
      setActionFeedback({ message: `✓ ${res.message || 'İşlem başlatıldı.'}`, type: 'ok' });
      await fetchLiveStatus();
      await fetchReviews(true);
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
      fetchReviews(true);
    } catch (err: any) {
      setActionFeedback({ message: `Hata: ${err.message}`, type: 'err' });
      fetchReviews(true);
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
      fetchReviews(true);
    } catch (err: any) {
      setActionFeedback({ message: `Hata: ${err.message}`, type: 'err' });
      fetchReviews(true);
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
      await fetchReviews(true);
      await fetchLiveStatus();
    } catch (err: any) {
      setActionFeedback({ message: `Hata: ${err.message}`, type: 'err' });
    } finally {
      setIsTriggering(false);
    }
  };

  const openEditModal = (rev: PastQuestionReviewRecord) => {
    const prop = rev.proposal || ({} as any);
    const src = rev.source || ({} as any);
    setEditingReview(rev);
    setEditStem(prop.soru_koku || src.soru_koku || '');
    const opts = prop.secenekler || src.secenekler || {};
    setEditOptions({
      A: opts.A || opts.a || '',
      B: opts.B || opts.b || '',
      C: opts.C || opts.c || '',
      D: opts.D || opts.d || '',
      E: opts.E || opts.e || '',
    });
    setEditCorrectAnswer(String(prop.dogru_secenek || src.dogru_secenek || 'A').toUpperCase());
    setEditExplanation(prop.aciklama || src.aciklama || '');
    setEditSummary(prop.degisiklik_ozeti || 'Kullanıcı/Hoca tarafından akademik literatüre göre revize edildi.');
  };

  const handleSaveEditProposal = async () => {
    if (!editingReview) return;
    const qId = String(editingReview.question_id);
    setIsSavingEdit(true);
    setActionFeedback(null);
    try {
      const res = await ApiService.updatePastQuestionReviewProposal(ADMIN_EMAIL, qId, {
        soru_koku: editStem,
        secenekler: editOptions,
        dogru_secenek: editCorrectAnswer,
        aciklama: editExplanation,
        degisiklik_ozeti: editSummary,
      });
      setActionFeedback({ message: `✓ Soru #${qId} önerisi başarıyla kaydedildi.`, type: 'ok' });
      setEditingReview(null);
      await fetchReviews(true);
    } catch (err: any) {
      setActionFeedback({ message: `Kayıt başarısız: ${err.message}`, type: 'err' });
    } finally {
      setIsSavingEdit(false);
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
      if (sortOrder === 'evidence_low' || sortOrder === 'evidence_high') {
        const d = (a.support_ratio || 0) - (b.support_ratio || 0);
        return sortOrder === 'evidence_low' ? d : -d;
      }
      const tA = new Date(a.processed_at || 0).getTime();
      const tB = new Date(b.processed_at || 0).getTime();
      return sortOrder === 'newest' ? tB - tA : tA - tB;
    });

    return sorted;
  }, [allReviews, statusFilter, searchQuery, sortOrder]);

  return (
    <div className="flex flex-col gap-4 pb-16 min-w-0 w-full max-w-[1400px] mx-auto">
      <PageHeader
        title="Test Edilen Çıkmış Sorular"
        description="Faz 14'ün çıkmış sorular için önerdiği OCR, imla ve eksik şık düzeltmeleri. Öneriler soru havuzuna kendiliğinden yazılmaz; yalnız onaylanan düzeltme canlı soruya uygulanır."
        stats={[
          { label: 'İncelenen Soru', value: stats.total.toLocaleString('tr-TR') },
          { label: 'İnceleme Bekleyen', value: stats.pending.toLocaleString('tr-TR'), tone: stats.pending > 0 ? 'warn' : 'default' },
          { label: 'Onaylanan', value: stats.approved.toLocaleString('tr-TR'), tone: 'ok' },
          { label: 'Reddedilen', value: stats.rejected.toLocaleString('tr-TR'), tone: 'default' },
        ]}
        actions={
          <div className="flex flex-wrap items-center gap-2">
            <button
              type="button"
              onClick={() => fetchReviews()}
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
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 sm:p-5 text-white shadow-lg space-y-4">
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
            <div className="flex items-center gap-1.5 bg-slate-800/80 px-2.5 h-11 sm:h-9 rounded-xl border border-slate-700">
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
              className="h-11 sm:h-9 px-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs inline-flex items-center gap-1.5 transition disabled:opacity-50 cursor-pointer shadow-md"
            >
              <Cloud className="w-3.5 h-3.5" />
              <span>Bulut Başlat (Gemini)</span>
            </button>

            {liveStatus?.isRunning && (
              <button
                type="button"
                onClick={handleStopReview}
                disabled={isTriggering}
                className="h-11 sm:h-9 px-3.5 rounded-xl bg-rose-600/90 hover:bg-rose-600 text-white font-bold text-xs inline-flex items-center gap-1.5 transition cursor-pointer"
              >
                <Square className="w-3.5 h-3.5" />
                <span>Durdur</span>
              </button>
            )}

            <button
              type="button"
              onClick={() => setShowConsole(!showConsole)}
              className="h-11 sm:h-9 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 font-semibold text-xs inline-flex items-center gap-1.5 transition cursor-pointer"
            >
              <Terminal className="w-3.5 h-3.5 text-amber-400" />
              <span>{showConsole ? 'Konsolu Gizle' : 'Konsolu Aç'}</span>
            </button>
          </div>
        </div>

        {/* İlerleme ve Kalan Soru Metrikleri */}
        <div className="grid grid-cols-3 sm:grid-cols-5 gap-2 sm:gap-3 pt-2 border-t border-slate-800 text-center font-mono">
          <div className="p-1.5 sm:p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[10px] uppercase text-slate-400 block">Toplam Havuz</span>
            <strong className="text-base text-slate-200">{liveStatus?.totalCandidate ? liveStatus.totalCandidate.toLocaleString('tr-TR') : '—'}</strong>
            <span className="text-[10px] text-slate-500 hidden sm:block">Aday Çıkmış</span>
          </div>
          <div className="p-1.5 sm:p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[10px] uppercase text-slate-400 block">İşlenen Soru</span>
            <strong className="text-base text-cyan-400">{liveStatus?.processed ?? allReviews.length}</strong>
            <span className="text-[10px] text-cyan-500 hidden sm:block">reviews.jsonl</span>
          </div>
          <div className="p-1.5 sm:p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[10px] uppercase text-slate-400 block">Kalan Soru</span>
            <strong className="text-base text-amber-400">{liveStatus?.remaining ?? '—'}</strong>
            <span className="text-[10px] text-amber-500 hidden sm:block">Sırada Bekleyen</span>
          </div>
          <div className="p-1.5 sm:p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-[10px] uppercase text-slate-400 block">Onaylanan</span>
            <strong className="text-base text-emerald-400">{liveStatus?.approved ?? stats.approved}</strong>
            <span className="text-[10px] text-emerald-500 hidden sm:block">Ana Havuza Aktarıldı</span>
          </div>
          <div className="p-1.5 sm:p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80 col-span-2 sm:col-span-1">
            <span className="text-[10px] uppercase text-violet-400 block flex items-center justify-center gap-1">
              <DollarSign className="w-3 h-3 text-violet-400" />
              <span>Aylık Bütçe</span>
            </span>
            <strong className="text-base text-violet-300">
              {liveStatus?.costTracking ? `${liveStatus.costTracking.cost_tl.toFixed(2)} ₺` : '0.00 ₺'}
            </strong>
            <span className="text-[10px] text-violet-400 hidden sm:block">
              / {liveStatus?.costTracking?.max_budget_tl ?? 1000} ₺ Tavan
            </span>
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

        <div className="flex flex-wrap items-center gap-1.5">
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

          {/* Görünüm: liste / ayrıntılı */}
          <div className="h-11 p-1 rounded-xl border border-line bg-white inline-flex items-center gap-0.5" role="radiogroup" aria-label="Görünüm">
            {([['list', 'Liste'], ['detail', 'Ayrıntılı']] as const).map(([id, label]) => (
              <button
                key={id}
                type="button"
                role="radio"
                aria-checked={layout === id}
                onClick={() => changeLayout(id)}
                className={`h-full px-3 rounded-lg text-[13px] font-semibold cursor-pointer ${layout === id ? 'bg-accent text-white' : 'text-ink-2 hover:text-ink'}`}
              >
                {label}
              </button>
            ))}
          </div>

          {/* Sıralama Butonu */}
          <label className="h-11 px-3 rounded-xl border border-line bg-white text-ink-2 text-[13px] font-semibold whitespace-nowrap inline-flex items-center gap-1.5 shrink-0 ml-1">
            <ArrowUpDown className="w-4 h-4 text-accent" />
            <span className="sr-only">Sıralama</span>
            <select
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value as typeof sortOrder)}
              className="bg-transparent outline-0 cursor-pointer text-ink"
            >
              <option value="newest">En yeni</option>
              <option value="oldest">En eski</option>
              <option value="evidence_low">Kanıtı en zayıf</option>
              <option value="evidence_high">Kanıtı en güçlü</option>
            </select>
          </label>

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
              <span>Değişmeyenleri tekrar değerlendir ({stats.unchanged})</span>
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
            onClick={() => fetchReviews()}
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
        <div className="flex flex-col gap-3">
          {filteredReviews.slice(0, visibleCount).map((rev) => {
            const qId = rev.question_id;
            const src = rev.source || ({} as any);
            const prop = rev.proposal || ({} as any);
            const isPending = rev.status === 'review_required';
            const isApproved = rev.status === 'approved';
            const isRejected = rev.status === 'rejected';
            const isUnchanged = rev.status === 'unchanged';
            const ratioPercent = Math.round((rev.support_ratio || 0) * 100);
            const view = cardView[qId] || 'diff';
            const srcStem = String(src.soru_koku || '');
            const propStem = String(prop.soru_koku || '');
            const stemChanged = Boolean(propStem) && propStem.trim() !== srcStem.trim();
            const srcOpt = (k: string) => String((src.secenekler || {})[k] ?? (src.secenekler || {})[k.toLowerCase()] ?? '');
            const changes = curriculumChanges(src, prop);
            const yzvNote = prop.YZV?.degisiklik_ozeti && typeof prop.YZV.degisiklik_ozeti === 'object' ? prop.YZV.degisiklik_ozeti : null;
            const aiCompletedList: string[] = (prop.yapay_zeka_tamamlanan_siklar || []).map((x: any) => String(x).toUpperCase());
            const status = isApproved
              ? { label: 'Onaylandı', cls: 'bg-emerald-50 text-emerald-700', Icon: CheckCircle2 }
              : isRejected
              ? { label: 'Reddedildi', cls: 'bg-rose-50 text-rose-700', Icon: XCircle }
              : isUnchanged
              ? { label: 'Değişiklik yok', cls: 'bg-slate-100 text-slate-600', Icon: Check }
              : { label: 'İnceleme bekliyor', cls: 'bg-amber-50 text-amber-800', Icon: Clock };
            const onCopy = async (which: 'src' | 'prop') => {
              const ok = await copyText(questionText(rev, which));
              if (ok) {
                setCopiedId(`${qId}:${which}`);
                window.setTimeout(() => setCopiedId((c) => (c === `${qId}:${which}` ? null : c)), 1600);
              } else {
                setActionFeedback({ message: 'Kopyalanamadı: tarayıcı panoya erişime izin vermedi.', type: 'err' });
              }
            };
            const btn = 'h-11 sm:h-8 px-3 rounded-lg text-[13px] sm:text-[12.5px] font-semibold inline-flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50 transition-colors';
            const copyBtn = (which: 'src' | 'prop', label: string) => {
              const done = copiedId === `${qId}:${which}`;
              return (
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    onCopy(which);
                  }}
                  className="h-11 sm:h-8 px-2 rounded-lg inline-flex items-center gap-1 text-[12px] font-semibold text-ink-3 hover:text-ink hover:bg-canvas cursor-pointer shrink-0"
                  title={`${label} soruyu ve şıklarını kopyala (cevap anahtarı hariç)`}
                  aria-label={done ? 'Kopyalandı' : `${label} soruyu kopyala`}
                >
                  {done ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{label}</span>
                </button>
              );
            };
            const copyButtons = (
              <>
                {copyBtn('src', 'Eski')}
                {propStem && copyBtn('prop', 'Yeni')}
              </>
            );
            const srcExpl = String(src.aciklama || '');
            const propExpl = String(prop.aciklama || '');
            const explChanged = Boolean(propExpl) && propExpl.trim() !== srcExpl.trim();

            // Liste görünümü: tek satır; tıklayınca ayrıntılı kart açılır
            if (layout === 'list' && !openRows[qId]) {
              return (
                <article
                  key={qId}
                  className="bg-white border border-line rounded-xl px-3 py-2 flex items-center gap-2 min-w-0 cursor-pointer hover:border-line-2"
                  onClick={() => setOpenRows((o) => ({ ...o, [qId]: true }))}
                >
                  <span className={`w-2 h-2 rounded-full shrink-0 ${isApproved ? 'bg-emerald-500' : isRejected ? 'bg-rose-500' : isUnchanged ? 'bg-slate-400' : 'bg-amber-500'}`} title={status.label} />
                  <span className="font-mono text-[12px] text-ink-3 shrink-0 hidden sm:inline">#{qId.slice(0, 8)}</span>
                  <span className="text-[13.5px] text-ink truncate min-w-0 flex-1">{propStem || srcStem}</span>
                  {changes.length > 0 && <span className="hidden md:inline text-[11.5px] px-1.5 py-0.5 rounded bg-amber-50 text-amber-800 shrink-0">müfredat</span>}
                  {explChanged && <span className="hidden md:inline text-[11.5px] px-1.5 py-0.5 rounded bg-violet-50 text-violet-700 shrink-0">açıklama</span>}
                  <span className={`text-[11.5px] font-mono shrink-0 ${ratioPercent >= 80 ? 'text-emerald-700' : 'text-rose-700'}`}>%{ratioPercent}</span>
                  {copyButtons}
                  {isAdmin && !isApproved && (
                    <button type="button" onClick={(e) => { e.stopPropagation(); handleApprove(qId); }} disabled={processingId === qId} className="w-11 h-11 sm:w-8 sm:h-8 rounded-lg inline-flex items-center justify-center text-emerald-700 hover:bg-emerald-50 cursor-pointer shrink-0 disabled:opacity-50" title="Onayla" aria-label="Onayla">
                      <Check className="w-4 h-4" />
                    </button>
                  )}
                  {isAdmin && !isRejected && (
                    <button type="button" onClick={(e) => { e.stopPropagation(); handleReject(qId); }} disabled={processingId === qId} className="w-11 h-11 sm:w-8 sm:h-8 rounded-lg inline-flex items-center justify-center text-rose-700 hover:bg-rose-50 cursor-pointer shrink-0 disabled:opacity-50" title="Reddet" aria-label="Reddet">
                      <X className="w-4 h-4" />
                    </button>
                  )}
                </article>
              );
            }

            return (
              <article key={qId} className="bg-white border border-line rounded-xl overflow-hidden">
                {/* Başlık: tek satır */}
                <header className="px-3 sm:px-4 pt-2.5 pb-2 flex items-center gap-2 min-w-0">
                  <span className="font-mono text-[12.5px] font-semibold text-ink shrink-0">#{qId}</span>
                  <span className={`h-[22px] px-2 rounded-full text-[11.5px] font-semibold inline-flex items-center gap-1 shrink-0 ${status.cls}`}>
                    <status.Icon className="w-3 h-3" />
                    <span className="hidden xs:inline sm:inline">{status.label}</span>
                  </span>
                  <span
                    className={`h-[22px] px-1.5 rounded-md text-[11.5px] font-mono font-semibold inline-flex items-center shrink-0 ${ratioPercent >= 80 ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'}`}
                    title={`Önerinin kaynak metinle örtüşme oranı: %${ratioPercent}`}
                  >
                    %{ratioPercent}
                  </span>
                  <span className="text-[12.5px] text-ink-3 truncate min-w-0">
                    {[kurulLabel(src.kurul_adi), src.ders_adi].filter(Boolean).join(' · ')}
                  </span>
                  <span className="flex-1" />
                  {copyButtons}
                  {layout === 'list' && (
                    <button type="button" onClick={() => setOpenRows((o) => ({ ...o, [qId]: false }))} className="h-11 sm:h-8 px-2.5 rounded-lg text-[12.5px] font-semibold text-ink-3 hover:text-ink hover:bg-canvas cursor-pointer shrink-0">
                      Daralt
                    </button>
                  )}
                </header>

                {/* Müfredat değişikliği */}
                {changes.length > 0 && (
                  <div className="mx-3 sm:mx-4 mb-2 px-2.5 py-1.5 rounded-lg bg-amber-50 text-amber-900 text-[12.5px] leading-snug">
                    <span className="font-semibold">Müfredat değişikliği:</span>{' '}
                    {changes.map((c, i) => (
                      <span key={c.alan}>
                        {i > 0 && ' · '}
                        {c.alan !== 'Kurul' && `${c.alan} `}
                        <span className="line-through decoration-amber-500/70">{c.eski}</span> → <b>{c.yeni}</b>
                      </span>
                    ))}
                    {yzvNote?.mufredat_atamasi && <span className="block text-amber-800/90 mt-0.5">{yzvNote.mufredat_atamasi}</span>}
                  </div>
                )}

                {/* Telefon/tablet: görünüm seçici */}
                <div className="lg:hidden px-3 sm:px-4 pb-2" role="tablist" aria-label="Karşılaştırma görünümü">
                  <div className="grid grid-cols-3 gap-1 p-0.5 rounded-lg bg-canvas">
                    {([['diff', 'Fark'], ['src', 'Mevcut'], ['prop', 'Öneri']] as const).map(([id, label]) => (
                      <button
                        key={id}
                        type="button"
                        role="tab"
                        aria-selected={view === id}
                        onClick={() => setCardView((v) => ({ ...v, [qId]: id }))}
                        className={`h-11 sm:h-9 rounded-md text-[13px] font-semibold cursor-pointer ${view === id ? 'bg-white text-ink shadow-xs' : 'text-ink-3'}`}
                      >
                        {label}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="px-3 sm:px-4 pb-3 grid grid-cols-1 lg:grid-cols-2 gap-2.5 lg:gap-3">
                  {/* Mevcut kayıt */}
                  <section className={`${view === 'src' ? 'flex' : 'hidden'} lg:flex flex-col gap-2 p-3 rounded-lg bg-slate-50 min-w-0`}>
                    <h4 className="m-0 flex items-center justify-between gap-2 text-[11.5px] font-semibold uppercase tracking-wide text-slate-500">
                      <span className="inline-flex items-center gap-1"><FileText className="w-3.5 h-3.5" /> Mevcut kayıt</span>
                      {src.dogru_secenek && <span className="normal-case tracking-normal font-mono text-slate-600">Cevap {src.dogru_secenek}</span>}
                    </h4>
                    <p className="m-0 text-[14px] leading-relaxed text-ink font-medium whitespace-pre-wrap break-words">
                      {srcStem || <span className="text-slate-400 italic">Soru kökü boş</span>}
                    </p>
                    {src.secenekler && Object.keys(src.secenekler).length > 0 && (
                      <ul className="m-0 p-0 list-none flex flex-col gap-1">
                        {Object.entries(src.secenekler).map(([k, v]) => (
                          <li key={k} className={`px-2 py-1 rounded-md text-[13px] flex items-start gap-1.5 ${k === src.dogru_secenek ? 'bg-emerald-50 text-emerald-900 font-semibold' : 'text-slate-700'}`}>
                            <span className="font-mono font-semibold shrink-0">{k})</span>
                            <span className="flex-1 min-w-0 break-words">{String(v)}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </section>

                  {/* Öneri (fark işaretli) */}
                  <section className={`${view === 'src' ? 'hidden' : 'flex'} lg:flex flex-col gap-2 p-3 rounded-lg bg-violet-50/60 min-w-0`}>
                    <h4 className="m-0 flex items-center justify-between gap-2 text-[11.5px] font-semibold uppercase tracking-wide text-violet-700">
                      <span className="inline-flex items-center gap-1"><Sparkles className="w-3.5 h-3.5" /> {modelLabel(rev.model)}</span>
                      {prop.dogru_secenek && <span className="normal-case tracking-normal font-mono">Cevap {prop.dogru_secenek}</span>}
                    </h4>
                    <p className="m-0 text-[14px] leading-relaxed text-violet-950 font-medium whitespace-pre-wrap break-words">
                      {!propStem ? (
                        <span className="text-violet-500 italic">Kökte değişiklik önerilmedi</span>
                      ) : stemChanged && view !== 'prop' ? (
                        <DiffText before={srcStem} after={propStem} />
                      ) : (
                        propStem
                      )}
                    </p>
                    {prop.secenekler && Object.keys(prop.secenekler).length > 0 && (
                      <ul className="m-0 p-0 list-none flex flex-col gap-1">
                        {Object.entries(prop.secenekler).map(([k, v]) => {
                          const upperKey = k.toUpperCase();
                          const isAiCompleted = !srcOpt(upperKey) || aiCompletedList.includes(upperKey);
                          const optChanged = view !== 'prop' && srcOpt(upperKey) && srcOpt(upperKey).trim() !== String(v).trim();
                          return (
                            <li key={k} className={`px-2 py-1 rounded-md text-[13px] flex items-start gap-1.5 ${k === prop.dogru_secenek ? 'bg-emerald-50 text-emerald-900 font-semibold' : 'text-violet-950'}`}>
                              <span className="font-mono font-semibold shrink-0">{k})</span>
                              <span className="flex-1 min-w-0 break-words">
                                {optChanged ? <DiffText before={srcOpt(upperKey)} after={String(v)} /> : String(v)}
                              </span>
                              {isAiCompleted && (
                                <span className="shrink-0 text-[10.5px] font-semibold px-1.5 py-0.5 rounded bg-purple-100 text-purple-700" title="Bu şık kaynakta yoktu; AI tamamladı">
                                  AI
                                </span>
                              )}
                            </li>
                          );
                        })}
                      </ul>
                    )}
                    {stemChanged && view !== 'prop' && (
                      <p className="m-0 text-[11.5px] text-ink-3">
                        <ins className="no-underline bg-emerald-100 text-emerald-900 rounded-sm px-0.5">eklenen</ins>{' '}
                        <del className="bg-rose-100 text-rose-800 rounded-sm px-0.5">çıkarılan</del> kelimeler, mevcut kayda göre
                      </p>
                    )}
                    {(prop.degisiklik_ozeti || (prop.degisen_alanlar?.length ?? 0) > 0 || yzvNote?.soru_koku_duzeltmesi || prop.YZV?.referans_literatur) && (
                      <div className="text-[12.5px] text-violet-950 bg-white/70 rounded-md px-2.5 py-2 flex flex-col gap-1 leading-relaxed">
                        <p className="m-0 font-semibold flex flex-wrap items-center gap-1">
                          Değişiklik notu
                          {(prop.degisen_alanlar || []).map((f: string) => (
                            <span key={f} className="font-normal text-[11.5px] px-1.5 rounded bg-violet-100 text-violet-800">{f}</span>
                          ))}
                        </p>
                        {prop.degisiklik_ozeti && (
                          <p className="m-0">{typeof prop.degisiklik_ozeti === 'string' ? prop.degisiklik_ozeti : JSON.stringify(prop.degisiklik_ozeti)}</p>
                        )}
                        {yzvNote?.soru_koku_duzeltmesi && <p className="m-0"><b>Kök:</b> {yzvNote.soru_koku_duzeltmesi}</p>}
                        {prop.YZV?.referans_literatur && <p className="m-0 text-violet-800"><b>Literatür:</b> {prop.YZV.referans_literatur}</p>}
                      </div>
                    )}
                  </section>
                </div>

                {/* Açıklama: eski ↔ yeni (kelime farkı) */}
                {(srcExpl || propExpl) && (
                  <section className="mx-3 sm:mx-4 mb-3 rounded-lg border border-line">
                    <h4 className="m-0 px-3 pt-2 flex flex-wrap items-center gap-2 text-[11.5px] font-semibold uppercase tracking-wide text-ink-3">
                      Açıklama
                      <span className={`normal-case tracking-normal text-[11.5px] px-1.5 rounded ${explChanged ? 'bg-violet-50 text-violet-700' : 'bg-slate-100 text-slate-600'}`}>
                        {explChanged ? (srcExpl ? 'değiştirildi' : 'yeni eklendi') : 'değişmedi'}
                      </span>
                      {yzvNote?.aciklama_duzeltmesi && <span className="normal-case tracking-normal font-normal text-ink-3">· {yzvNote.aciklama_duzeltmesi}</span>}
                    </h4>
                    <details open={layout === 'detail'} className="px-3 pb-2 text-[13px] text-ink-2">
                      <summary className="cursor-pointer text-[12.5px] text-ink-3 py-1">
                        {explChanged && srcExpl ? 'Farkı göster / gizle (yeşil eklenen, kırmızı çıkarılan)' : 'Göster / gizle'}
                      </summary>
                      <p className="m-0 whitespace-pre-wrap leading-relaxed break-words">
                        {explChanged && srcExpl ? <DiffText before={srcExpl} after={propExpl} /> : propExpl || srcExpl}
                      </p>
                    </details>
                  </section>
                )}

                {/* Eylemler + künye */}
                <footer className="px-3 sm:px-4 py-2 border-t border-line flex flex-col sm:flex-row sm:items-center gap-2">
                  {isAdmin && (
                    <div className="grid grid-cols-2 sm:flex gap-1.5">
                      {!isApproved && (
                        <button type="button" onClick={() => handleApprove(qId)} disabled={processingId === qId} className={`${btn} bg-emerald-600 hover:bg-emerald-700 text-white`}>
                          <Check className="w-3.5 h-3.5" /> Onayla
                        </button>
                      )}
                      {!isRejected && (
                        <button type="button" onClick={() => handleReject(qId)} disabled={processingId === qId} className={`${btn} border border-line bg-white hover:bg-rose-50 hover:text-rose-700 text-ink-2`}>
                          <X className="w-3.5 h-3.5" /> Reddet
                        </button>
                      )}
                      <button type="button" onClick={() => openEditModal(rev)} className={`${btn} border border-line bg-white hover:bg-canvas text-ink-2`}>
                        <Edit3 className="w-3.5 h-3.5" /> Düzenle
                      </button>
                      {(isUnchanged || isRejected) && (
                        <button type="button" onClick={() => handleReEvaluateUnchanged(qId)} disabled={processingId === qId || isTriggering} className={`${btn} border border-line bg-white hover:bg-amber-50 text-ink-2`}>
                          <RotateCcw className="w-3.5 h-3.5" /> Tekrar değerlendir
                        </button>
                      )}
                    </div>
                  )}
                  <p className="m-0 sm:ml-auto text-[11.5px] text-ink-3 flex flex-wrap gap-x-2.5 gap-y-0.5 min-w-0">
                    <span className="font-mono break-all">{rev.model || 'model bilinmiyor'}</span>
                    {rev.processed_at && <span>{rev.processed_at.slice(0, 16).replace('T', ' ')}</span>}
                    {rev.approved_at && <span className="text-emerald-700">Onay {rev.approved_at.slice(0, 16).replace('T', ' ')}</span>}
                    {rev.rejected_at && <span className="text-rose-700">Red {rev.rejected_at.slice(0, 16).replace('T', ' ')}</span>}
                  </p>
                </footer>
              </article>
            );
          })}
          {filteredReviews.length > visibleCount && (
            <button
              type="button"
              onClick={() => setVisibleCount((c) => c + PAGE_SIZE)}
              className="h-12 rounded-xl border border-line bg-white text-ink text-[14px] font-semibold hover:bg-canvas cursor-pointer"
            >
              Daha fazla göster ({(filteredReviews.length - visibleCount).toLocaleString('tr-TR')} kayıt daha)
            </button>
          )}
        </div>
      )}

      {/* Soru Önerisi Düzenleme / Revize Etme Modalı */}
      {editingReview && (
        <div className="fixed inset-0 z-50 flex items-stretch sm:items-center justify-center sm:p-4 bg-slate-900/60" role="dialog" aria-modal="true" aria-labelledby="tc-edit-title" onKeyDown={(e) => e.key === 'Escape' && !isSavingEdit && setEditingReview(null)}>
          <div className="bg-white sm:rounded-2xl shadow-2xl border border-line w-full max-w-2xl h-full sm:h-auto sm:max-h-[90vh] flex flex-col overflow-hidden">
            {/* Modal Header */}
            <div className="px-4 sm:px-6 py-3 sm:py-4 border-b border-line bg-canvas flex items-center justify-between gap-2" style={{ paddingTop: 'max(0.75rem, env(safe-area-inset-top))' }}>
              <div className="flex items-center gap-2">
                <Edit3 className="w-5 h-5 text-indigo-600" />
                <h3 id="tc-edit-title" className="font-bold text-base text-ink">
                  Soru #{editingReview.question_id} Önerisini Düzenle
                </h3>
              </div>
              <button
                type="button"
                onClick={() => setEditingReview(null)}
                aria-label="Kapat"
                className="w-11 h-11 inline-flex items-center justify-center rounded-lg hover:bg-slate-200 text-slate-500 hover:text-slate-800 transition cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-4 sm:p-6 overflow-y-auto space-y-4 text-sm flex-1">
              <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-xs text-amber-900 space-y-1">
                <span className="font-bold block flex items-center gap-1">
                  <AlertTriangle className="w-4 h-4 text-amber-600" />
                  Akademik Kural & Soru Bütünlüğü Uyarısı:
                </span>
                <p>
                  Soru kökünün yönünü değiştirmeyiniz (örn. olumlu soruyu olumsuza çevirmeyiniz). Doğru cevabı değiştirecek köklü oynamalar yapmayınız; yalnızca imla, OCR bozukluğu, tıbbi terminoloji veya eksik şıkları tamamlayınız.
                </p>
              </div>

              {/* Soru Kökü */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-ink-2 mb-1.5">
                  Soru Kökü
                </label>
                <textarea
                  rows={4}
                  value={editStem}
                  onChange={(e) => setEditStem(e.target.value)}
                  className="w-full p-3 rounded-xl border border-line focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 text-ink text-[16px] sm:text-sm outline-0 leading-relaxed font-sans"
                  placeholder="Düzeltilmiş soru kökünü buraya yazın..."
                />
              </div>

              {/* Seçenekler A-E */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="block text-xs font-bold uppercase tracking-wider text-ink-2">
                    Seçenekler (A - E)
                  </label>
                  <div className="flex items-center gap-2 text-xs">
                    <span className="text-ink-3">Doğru Cevap:</span>
                    <select
                      value={editCorrectAnswer}
                      onChange={(e) => setEditCorrectAnswer(e.target.value)}
                      className="h-10 px-2 rounded-lg border border-line font-bold text-indigo-600 bg-white cursor-pointer"
                    >
                      {['A', 'B', 'C', 'D', 'E'].map((opt) => (
                        <option key={opt} value={opt}>
                          Şık {opt}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {(['A', 'B', 'C', 'D', 'E'] as const).map((key) => (
                  <div key={key} className="flex items-center gap-2">
                    <span
                      className={`w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs shrink-0 ${
                        editCorrectAnswer === key
                          ? 'bg-emerald-600 text-white'
                          : 'bg-slate-100 text-slate-700'
                      }`}
                    >
                      {key}
                    </span>
                    <input
                      type="text"
                      value={editOptions[key]}
                      onChange={(e) =>
                        setEditOptions((prev) => ({ ...prev, [key]: e.target.value }))
                      }
                      className="flex-1 min-w-0 h-11 px-3 rounded-lg border border-line focus:border-indigo-500 text-[16px] sm:text-sm text-ink outline-0"
                      placeholder={`${key} şıkkı metni...`}
                    />
                  </div>
                ))}
              </div>

              {/* Açıklama */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-ink-2 mb-1.5">
                  Tıbbi Açıklama ve Kanıt Gerekçesi
                </label>
                <textarea
                  rows={3}
                  value={editExplanation}
                  onChange={(e) => setEditExplanation(e.target.value)}
                  className="w-full p-3 rounded-xl border border-line focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 text-ink text-[16px] sm:text-sm outline-0 leading-relaxed"
                  placeholder="Soruya ait tıbbi açıklama..."
                />
              </div>

              {/* Değişiklik Notu */}
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-ink-2 mb-1.5">
                  Değişiklik / Revizyon Notu
                </label>
                <input
                  type="text"
                  value={editSummary}
                  onChange={(e) => setEditSummary(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl border border-line focus:border-indigo-500 text-sm text-ink outline-0"
                  placeholder="Örn: C şıkkındaki imla hatası düzeltildi, soru kökündeki harf eksikliği giderildi."
                />
              </div>
            </div>

            {/* Modal Footer */}
            <div className="px-4 sm:px-6 py-3 sm:py-4 border-t border-line bg-canvas grid grid-cols-2 sm:flex sm:items-center sm:justify-end gap-2.5" style={{ paddingBottom: 'max(0.75rem, env(safe-area-inset-bottom))' }}>
              <button
                type="button"
                onClick={() => setEditingReview(null)}
                disabled={isSavingEdit}
                className="h-11 px-4 rounded-xl border border-line bg-white hover:bg-slate-100 text-ink-2 text-[13.5px] font-semibold cursor-pointer"
              >
                İptal
              </button>
              <button
                type="button"
                onClick={handleSaveEditProposal}
                disabled={isSavingEdit}
                className="h-11 px-4 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-[13.5px] font-bold inline-flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50 shadow-sm"
              >
                {isSavingEdit ? (
                  <>
                    <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    <span>Kaydediliyor...</span>
                  </>
                ) : (
                  <>
                    <Check className="w-3.5 h-3.5" />
                    <span>Öneriyi kaydet</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
