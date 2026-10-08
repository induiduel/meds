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
  Copy,
  Info,
  BookOpen,
  Flag,
  BarChart3,
  Gift,
} from 'lucide-react';
import { PastQuestionReviewRecord } from '../types';
import { ApiService } from '../services/api';
import { AppUser, ADMIN_EMAIL } from '../services/auth';
import { pathFor } from '../router';
import { AnswerPoll } from './AnswerPoll';
import { safeJsonFetch } from '../services/api';
import { StemText } from './ui/StemText';
import { Collapsible } from './ui/Collapsible';
import { ActionMenu, ActionItem } from './ui/ActionMenu';

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

/** Değişikliğin olduğu yerdeki bilgi simgesi: tıklayınca o değişikliğin ayrıntısı açılır (Esc / dışarı tıkla kapanır). */
function ChangeInfo({ title, before, after, note }: { title: string; before?: string; after?: string; note?: string }) {
  const [open, setOpen] = useState(false);
  const ref = React.useRef<HTMLSpanElement>(null);
  useEffect(() => {
    if (!open) return;
    const close = (e: MouseEvent | KeyboardEvent) => {
      if (e instanceof KeyboardEvent ? e.key === 'Escape' : !ref.current?.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener('mousedown', close);
    document.addEventListener('keydown', close);
    return () => {
      document.removeEventListener('mousedown', close);
      document.removeEventListener('keydown', close);
    };
  }, [open]);
  return (
    <span ref={ref} className="relative inline-flex align-middle shrink-0">
      <button
        type="button"
        onClick={(e) => {
          e.stopPropagation();
          setOpen((v) => !v);
        }}
        className="w-6 h-6 -m-1 inline-flex items-center justify-center rounded-full text-violet-600 hover:bg-violet-100 cursor-pointer"
        aria-label={`${title}: değişikliği göster`}
        aria-expanded={open}
      >
        <Info className="w-3.5 h-3.5" />
      </button>
      {open && (
        <span role="dialog" className="absolute z-30 top-6 right-0 w-[min(22rem,80vw)] p-3 rounded-lg bg-white border border-line shadow-lg text-[12.5px] font-normal normal-case tracking-normal text-ink-2 flex flex-col gap-1.5 text-left">
          <b className="text-ink">{title}</b>
          {before !== undefined && (
            <span>
              <span className="text-ink-3">Önce:</span> {before ? <del className="bg-rose-50 text-rose-800 decoration-rose-400">{before}</del> : <i>(yoktu)</i>}
            </span>
          )}
          {after !== undefined && (
            <span>
              <span className="text-ink-3">Sonra:</span> <ins className="no-underline bg-emerald-50 text-emerald-900">{after}</ins>
            </span>
          )}
          {note && <span className="text-ink-3">{note}</span>}
        </span>
      )}
    </span>
  );
}

/** Soru için faz verisi (terimler, eş anlamlılar, kısaltmalar, Faz 13 varlıkları, kazanım) + önerinin değiştirdiği alanlar. */
function TermsDialog({ rev, onClose }: { rev: PastQuestionReviewRecord; onClose: () => void }) {
  const [data, setData] = useState<any | null | undefined>(undefined);
  const closeRef = React.useRef(onClose);
  closeRef.current = onClose;
  useEffect(() => {
    safeJsonFetch<{ insights: any }>(`/api/questions/${encodeURIComponent(String(rev.question_id))}/insights`).then((r) =>
      setData(r.ok ? r.data?.insights || null : null),
    );
    const esc = (e: KeyboardEvent) => e.key === 'Escape' && closeRef.current();
    document.addEventListener('keydown', esc);
    return () => document.removeEventListener('keydown', esc);
  }, [rev.question_id]);
  const prop: any = rev.proposal || {};
  const yzv = prop.YZV?.degisiklik_ozeti && typeof prop.YZV.degisiklik_ozeti === 'object' ? prop.YZV.degisiklik_ozeti : null;
  const terms: string[] = Array.from(new Set([...(data?.varliklar || []).map((v: any) => v.ad), ...(data?.faz6_5?.terimler || []), ...(data?.faz5?.terimler || [])]));
  const syn = Object.entries((data?.faz6_5?.esanlamlilar || {}) as Record<string, string[]>);
  const abbr = Object.entries((data?.faz6_5?.kisaltmalar || {}) as Record<string, string>);
  const k = (data?.mufredat || data?.faz8)?.kazanimlar?.[0];
  const h = 'm-0 text-[11.5px] font-semibold uppercase tracking-wide text-ink-3';
  return (
    <div className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-4" role="dialog" aria-modal="true" aria-label="Terim ve sözlük bilgisi" onClick={onClose}>
      <div className="ms-modal-panel bg-white w-full max-w-xl overflow-y-auto px-5 pt-4 pb-5 flex flex-col gap-3" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between gap-2">
          <h3 className="m-0 font-display text-[17px] font-semibold text-ink">Terimler ve sözlük <span className="font-mono text-[13px] font-normal text-ink-3">#{String(rev.question_id).slice(0, 8)}</span></h3>
          <button type="button" onClick={onClose} className="ms-btn is-ghost is-icon" aria-label="Kapat">
            <X />
          </button>
        </div>
        <section className="flex flex-col gap-1">
          <h4 className={h}>Bu öneride değişenler</h4>
          {(prop.degisen_alanlar || []).length ? (
            <div className="flex flex-wrap gap-1">{prop.degisen_alanlar.map((f: string) => <span key={f} className="text-[12px] px-1.5 rounded bg-violet-50 text-violet-700">{f}</span>)}</div>
          ) : (
            <p className="m-0 text-[13px] text-ink-3">Değişen alan bildirilmedi.</p>
          )}
          {yzv?.soru_koku_duzeltmesi && <p className="m-0 text-[13px]"><b>Kök:</b> {yzv.soru_koku_duzeltmesi}</p>}
          {yzv?.aciklama_duzeltmesi && <p className="m-0 text-[13px]"><b>Açıklama:</b> {yzv.aciklama_duzeltmesi}</p>}
          {yzv?.mufredat_atamasi && <p className="m-0 text-[13px]"><b>Müfredat:</b> {yzv.mufredat_atamasi}</p>}
          {prop.YZV?.referans_literatur && <p className="m-0 text-[13px]"><b>Literatür:</b> {prop.YZV.referans_literatur}</p>}
        </section>
        {data === undefined ? (
          <p className="m-0 text-[13px] text-ink-3">Faz verisi yükleniyor…</p>
        ) : !data ? (
          <p className="m-0 text-[13px] text-ink-3">Bu soru için faz verisi (terim, sözlük) yok.</p>
        ) : (
          <>
            {k && (
              <section className="flex flex-col gap-0.5">
                <h4 className={h}>Kazanım</h4>
                <p className="m-0 text-[13px] text-ink">{['Kurul ' + k.kurul, k.ders, k.konu].filter(Boolean).join(' · ')}</p>
                {k.kazanim && <p className="m-0 text-[13px] text-ink-2">{k.kazanim}</p>}
              </section>
            )}
            {terms.length > 0 && (
              <section className="flex flex-col gap-1">
                <h4 className={h}>Terimler ({terms.length})</h4>
                <div className="flex flex-wrap gap-1">{terms.map((t) => <span key={t} className="text-[12px] px-2 py-0.5 rounded-full bg-canvas text-ink-2">{t}</span>)}</div>
              </section>
            )}
            {syn.length > 0 && (
              <section className="flex flex-col gap-0.5">
                <h4 className={h}>Eş anlamlılar</h4>
                {syn.map(([t, v]) => <p key={t} className="m-0 text-[13px]"><b>{t}</b> = {(v || []).join(', ')}</p>)}
              </section>
            )}
            {abbr.length > 0 && (
              <section className="flex flex-col gap-0.5">
                <h4 className={h}>Kısaltmalar</h4>
                {abbr.map(([a, e]) => <p key={a} className="m-0 text-[13px]"><b>{a}</b> = {e}</p>)}
              </section>
            )}
            {(data.varliklar || []).length > 0 && (
              <section className="flex flex-col gap-0.5">
                <h4 className={h}>Kimlikli tıbbi varlıklar (Faz 13)</h4>
                {(data.varliklar || []).map((v: any) => (
                  <p key={v.ad} className="m-0 text-[12.5px]">
                    <b>{v.ad}</b>
                    <span className="text-ink-3"> · {v.tur || 'tür yok'} · {v.kaynak}{v.kimlik && Object.keys(v.kimlik).length ? ' · ' + Object.entries(v.kimlik).map(([kk, vv]: any) => `${kk}: ${(vv || []).join(',')}`).join(' · ') : ''}</span>
                  </p>
                ))}
              </section>
            )}
          </>
        )}
      </div>
    </div>
  );
}

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
  const [statusFilter, setStatusFilter] = useState<string>('review_required');
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
  const [termsFor, setTermsFor] = useState<PastQuestionReviewRecord | null>(null);
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
    paralel?: { guncelleme: string; anahtarlar: Record<string, { kalan: number; cozulen: number; bekleme_bitis: string | null; ardisik_hata: number }> } | null;
    logs: string[];
  } | null>(null);
  const [isTriggering, setIsTriggering] = useState(false);
  const [triggerLimit, setTriggerLimit] = useState(5);
  const [liteOn, setLiteOn] = useState<boolean | null>(null);
  const [autoOn, setAutoOn] = useState<boolean | null>(null);
  const [autoLimit, setAutoLimit] = useState(4000);
  const [showConsole, setShowConsole] = useState(false);

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
      // Aynı soru için birden çok kayıt olabilir (yeniden değerlendirme): en güncel kayıt gösterilir
      const stamp = (r: any) => Date.parse(r.last_edited_at || r.processed_at || '') || 0;
      const rawList = [...(data.reviews || [])].sort((a: any, b: any) => stamp(b) - stamp(a));
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
    ApiService.getPhase14Settings(ADMIN_EMAIL).then((s) => {
      setLiteOn(s ? s.lite_kullan : null);
      setAutoOn(s ? s.otomatik_ucretsiz : null);
      if (s?.otomatik_limit) setAutoLimit(s.otomatik_limit);
    });
    fetchLiveStatus();
    const interval = setInterval(() => {
      if (!document.hidden) fetchLiveStatus();
    }, 3000);
    return () => clearInterval(interval);
  }, [isAdmin]);

  // filtre/arama değişince listeyi başa al
  useEffect(() => setVisibleCount(PAGE_SIZE), [statusFilter, searchQuery, sortOrder]);

  const handleStartReview = async (mode: 'cloud' | 'local' | 'free') => {
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

  const toggleLite = async () => {
    if (liteOn === null) return;
    try {
      const s = await ApiService.setPhase14Settings(ADMIN_EMAIL, { lite_kullan: !liteOn });
      setLiteOn(s.lite_kullan);
      setActionFeedback({
        message: s.lite_kullan
          ? '✓ Lite yedeği açık: Flash kotası bitince Flash-Lite ile devam edilir (Lite\'ın cevap oyu sayılmaz).'
          : '✓ Lite yedeği kapalı: Flash kotası bitince Faz 14 durur.',
        type: 'ok',
      });
    } catch (err: any) {
      setActionFeedback({ message: `Ayar kaydedilemedi: ${err.message}`, type: 'err' });
    }
  };

  const toggleAuto = async () => {
    if (autoOn === null) return;
    const acilacak = !autoOn;
    if (acilacak && !window.confirm(`Otomatik ücretsiz inceleme açılsın mı?\n\nİncelenmemiş ${autoLimit} soru ücretsiz anahtarlara dağıtılır; her anahtar kendi sorularını tek tek çözer, kota bitince 1/10/30 dk bekleyip devam eder. Ücretli anahtar kullanılmaz. Kapatana ya da "Durdur"a basana kadar sürer.`)) return;
    setIsTriggering(true);
    try {
      const s = await ApiService.setPhase14Settings(ADMIN_EMAIL, { otomatik_ucretsiz: acilacak, otomatik_limit: autoLimit });
      setAutoOn(s.otomatik_ucretsiz);
      setActionFeedback({
        message: s.otomatik_ucretsiz
          ? s.started
            ? `✓ Otomatik ücretsiz inceleme başladı (${s.otomatik_limit} soru, ücretsiz anahtarlar paralel).`
            : '✓ Otomatik ücretsiz inceleme açık. Şu an başka bir Faz 14 çalışıyor; o bitince en geç 5 dk içinde başlar.'
          : '✓ Otomatik ücretsiz inceleme kapatıldı ve durduruldu.',
        type: 'ok',
      });
      await fetchLiveStatus();
    } catch (err: any) {
      setActionFeedback({ message: `Ayar kaydedilemedi: ${err.message}`, type: 'err' });
    } finally {
      setIsTriggering(false);
    }
  };

  const handleStopReview = async () => {
    setIsTriggering(true);
    try {
      await ApiService.stopPastQuestionReview(ADMIN_EMAIL);
      setAutoOn((v) => (v ? false : v));                 // Durdur otomatik kipi de kapatır
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

  // Cevabı belirsiz soru: seçilen (yoksa anketteki öndeki) şık kaydedilir, soru normal inceleme listesine döner
  const [answerPick, setAnswerPick] = useState<Record<string, string>>({});
  const [pollLeader, setPollLeader] = useState<Record<string, string>>({});
  const handleCompleteAnswerDoubt = async (qId: string, choice?: string) => {
    setProcessingId(qId);
    try {
      // 1) Cevabı yaz, belirsiz işaretini kaldır  2) Öneriyi onayla: soru /cikmis'teki canlı soruya uygulanır
      const res = await ApiService.completeAnswerDoubt(ADMIN_EMAIL, qId, choice);
      await ApiService.approvePastQuestionReview(ADMIN_EMAIL, qId);
      setAllReviews((prev) => prev.map((r) => (String(r.question_id) === qId ? { ...r, status: 'approved' as any, answer_doubtful: false, answer_poll_open: true, answer_vote_result: { winner: res.winner, by: 'admin' } } : r)));
      setActionFeedback({ message: `Soru #${qId.slice(0, 8)}: cevap ${res.winner} olarak kaydedildi ve çıkmış sorulara gönderildi. Anket açık kalıyor; topluluk cevabı karşılaştırılacak.`, type: 'ok' });
      fetchReviews(true);
    } catch (err: any) {
      setActionFeedback({ message: `Hata: ${err.message}`, type: 'err' });
    } finally {
      setProcessingId(null);
    }
  };

  const handleToggleAnswerDoubt = async (qId: string, value: boolean) => {
    setProcessingId(qId);
    setAllReviews(prev => prev.map(r => String(r.question_id) === qId ? { ...r, answer_doubtful: value, ...(value ? {} : { answer_poll_open: false }) } : r));
    try {
      await ApiService.setPastQuestionAnswerDoubt(ADMIN_EMAIL, qId, value);
      if (value) setStatusFilter('answer_doubtful');
      setActionFeedback({ message: value ? `✓ Soru #${qId} için cevap anketi açıldı.` : `✓ Soru #${qId} için cevap anketi kapatıldı.`, type: 'ok' });
    } catch (err: any) {
      setActionFeedback({ message: `Hata: ${err.message}`, type: 'err' });
      fetchReviews(true);
    } finally {
      setProcessingId(null);
    }
  };

  const handleToggleSuspicious = async (qId: string, value: boolean) => {
    setProcessingId(qId);
    setAllReviews(prev => prev.map(r => String(r.question_id) === qId ? { ...r, suspicious: value } : r));
    try {
      await ApiService.setPastQuestionReviewSuspicious(ADMIN_EMAIL, qId, value);
      setActionFeedback({ message: value ? `✓ Soru #${qId} şüpheli olarak işaretlendi.` : `✓ Soru #${qId} şüpheli işareti kaldırıldı.`, type: 'ok' });
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

  const handleSaveEditProposal = async (approveAfter = false) => {
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
      if (approveAfter) {
        await ApiService.approvePastQuestionReview(ADMIN_EMAIL, qId);
        setActionFeedback({ message: `✓ Soru #${qId} kaydedildi ve ana soru havuzuna onaylandı.`, type: 'ok' });
      } else {
        setActionFeedback({ message: `✓ Soru #${qId} önerisi başarıyla kaydedildi.`, type: 'ok' });
      }
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
    const pending = allReviews.filter((r) => r.status === 'review_required' && !r.answer_doubtful).length;
    const doubtful = allReviews.filter((r) => r.answer_doubtful && r.status === 'review_required').length;
    const approved = allReviews.filter((r) => r.status === 'approved').length;
    const rejected = allReviews.filter((r) => r.status === 'rejected').length;
    const unchanged = allReviews.filter((r) => r.status === 'unchanged').length;
    const suspicious = allReviews.filter((r) => r.suspicious && r.status === 'review_required').length;
    return { total, pending, approved, rejected, unchanged, suspicious, doubtful };
  }, [allReviews]);

  const filteredReviews = useMemo(() => {
    let list = allReviews;

    if (statusFilter === 'suspicious') {
      list = list.filter((r) => r.suspicious && r.status === 'review_required');
    } else if (statusFilter === 'answer_doubtful') {
      list = list.filter((r) => r.answer_doubtful && r.status === 'review_required');
    } else if (statusFilter === 'review_required') {
      list = list.filter((r) => r.status === 'review_required' && !r.answer_doubtful);
    } else if (statusFilter !== 'all') {
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
        // Faz 14 verisinin tamamı aranabilir: şıklar, açıklama, kurul/ders/konu, model notları
        const fullMatch = JSON.stringify([r.proposal || {}, r.source?.secenekler || {}, r.source?.aciklama || '', r.source?.konu_adi || '']).toLowerCase().includes(q);
        return idMatch || stemMatch || propMatch || discMatch || summaryMatch || fullMatch;
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

  const statusTabs = [
    { id: 'review_required', label: 'İnceleme bekliyor', count: stats.pending },
    { id: 'answer_doubtful', label: 'Cevap belirsiz', count: stats.doubtful },
    { id: 'suspicious', label: 'Şüpheli', count: stats.suspicious },
    { id: 'approved', label: 'Onaylandı', count: stats.approved },
    { id: 'rejected', label: 'Reddedildi', count: stats.rejected },
    { id: 'unchanged', label: 'Değişiklik yok', count: stats.unchanged },
    { id: 'all', label: 'Tümü', count: stats.total },
  ];
  const total = liveStatus?.totalCandidate || 0;
  const processed = liveStatus?.processed ?? allReviews.length;
  const progressPct = total ? Math.min(100, Math.round((processed / total) * 100)) : 0;

  return (
    <div className="flex flex-col gap-3 pb-16 min-w-0 w-full max-w-[1400px] mx-auto">
      <PageHeader
        title="Faz 14 incelemesi"
        description="Çıkmış sorular için önerilen OCR, imla ve eksik şık düzeltmeleri. Öneri yalnız onaylanınca canlı soruya uygulanır."
        actions={
          <div className="flex items-center gap-1.5">
            <button type="button" onClick={() => fetchReviews()} disabled={isLoading} className="ms-btn is-ghost is-sm" aria-label="Yenile">
              <RefreshCw className={isLoading ? 'animate-spin' : ''} /> <span className="hidden sm:inline">Yenile</span>
            </button>
            <a
              href={pathFor('past_exams')}
              onClick={(e) => {
                if (onBackToPastExams) {
                  e.preventDefault();
                  onBackToPastExams();
                }
              }}
              className="ms-btn is-tonal is-sm"
            >
              <ArrowLeft /> Çıkmış sorular
            </a>
          </div>
        }
      />

      {/* Süreç paneli (yönetici): tek satır durum + ilerleme; ayarlar ve konsol istenince açılır */}
      {isAdmin && (
        <section className="ms-qcard gap-2.5!" aria-label="Faz 14 süreci">
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
            <span className="inline-flex items-center gap-2 text-[13.5px] font-semibold text-ink">
              <span className={`w-2 h-2 rounded-full ${liveStatus?.isRunning ? 'bg-ok animate-pulse' : 'bg-line-2'}`} aria-hidden />
              {liveStatus?.isRunning ? `Çalışıyor · ${liveStatus.activeMode === 'cloud' ? 'Gemini' : 'yerel model'}` : 'Süreç bekliyor'}
            </span>
            <dl className="m-0 flex flex-wrap gap-x-4 gap-y-1 text-[12.5px] text-ink-3">
              {[
                ['Havuz', total ? total.toLocaleString('tr-TR') : '—'],
                ['İşlenen', processed.toLocaleString('tr-TR')],
                ['Kalan', liveStatus?.remaining != null ? liveStatus.remaining.toLocaleString('tr-TR') : '—'],
                ['Onaylanan', String(liveStatus?.approved ?? stats.approved)],
                ['Bu ay', `${(liveStatus?.costTracking?.cost_tl ?? 0).toFixed(2)} ₺ / ${liveStatus?.costTracking?.max_budget_tl ?? 1000} ₺`],
              ].map(([k, v]) => (
                <div key={k} className="flex items-baseline gap-1.5">
                  <dt>{k}</dt>
                  <dd className="m-0 font-semibold text-ink tabular-nums">{v}</dd>
                </div>
              ))}
            </dl>
            <span className="flex-1" />
            <div className="flex flex-wrap items-center gap-1.5">
              <label className="ms-btn is-sm relative" title="Bir çalıştırmada işlenecek soru sayısı">
                Parti: {triggerLimit}
                <select value={triggerLimit} onChange={(e) => setTriggerLimit(Number(e.target.value))} className="absolute inset-0 opacity-0 cursor-pointer" aria-label="Parti büyüklüğü">
                  {[5, 10, 25, 50, 100, 200].map((v) => <option key={v} value={v}>{v} soru</option>)}
                </select>
              </label>
              <button
                type="button"
                role="switch"
                aria-checked={liteOn === true}
                onClick={toggleLite}
                disabled={liteOn === null}
                title="Açıkken: ücretsiz Flash kotası bitince Flash-Lite ile devam edilir; Lite yalnız soruyu düzeltir, cevabı bağımsız modeller belirler. Kapalıyken: Flash yoksa Faz 14 durur."
                className={`ms-btn is-sm ${liteOn ? 'is-on' : ''}`}
              >
                <span className={`relative inline-block w-7 h-4 rounded-full transition-colors ${liteOn ? 'bg-accent' : 'bg-line-2'}`} aria-hidden>
                  <span className={`absolute top-0.5 w-3 h-3 rounded-full bg-white transition-all ${liteOn ? 'left-3.5' : 'left-0.5'}`} />
                </span>
                Lite yedeği
              </button>
              <button
                type="button"
                role="switch"
                aria-checked={autoOn === true}
                onClick={toggleAuto}
                disabled={autoOn === null || isTriggering}
                title="Açıkken: incelenmemiş sorular yalnız ücretsiz anahtarlarla, anahtar başına tek tek ve paralel incelenir; kota bitince 1/10/30 dk bekleyip sürer. İş durursa en geç 5 dk içinde kaldığı yerden yeniden başlar; işlenen soru tekrar çözülmez."
                className={`ms-btn is-sm ${autoOn ? 'is-on' : ''}`}
              >
                <span className={`relative inline-block w-7 h-4 rounded-full transition-colors ${autoOn ? 'bg-accent' : 'bg-line-2'}`} aria-hidden>
                  <span className={`absolute top-0.5 w-3 h-3 rounded-full bg-white transition-all ${autoOn ? 'left-3.5' : 'left-0.5'}`} />
                </span>
                Otomatik ücretsiz inceleme{autoOn ? ` · ${autoLimit}` : ''}
              </button>
              {liveStatus?.isRunning ? (
                <button type="button" onClick={handleStopReview} disabled={isTriggering} className="ms-btn is-sm is-danger bg-bad-soft!">
                  <Square /> Durdur
                </button>
              ) : (
                <>
                  <button
                    type="button"
                    onClick={() => handleStartReview('free')}
                    disabled={isTriggering}
                    className="ms-btn is-sm"
                    title="Yalnız ücretsiz anahtarlar. Sorular anahtarlara dağıtılır, her anahtar kendi sorularını paralel çözer; yanıt alamazsa 1 dk → 10 dk → 30 dk bekleyip yeniden dener, başarılı olunca hemen sıradakine geçer."
                  >
                    <Gift /> Ücretsiz başlat
                  </button>
                  <button type="button" onClick={() => handleStartReview('cloud')} disabled={isTriggering} className="ms-btn is-sm is-primary" title="Önce ücretsiz, tükenince ücretli anahtar (günlük 100 istek, aylık 100 TL sınırı)">
                    <Cloud /> Başlat (ücretli izinli)
                  </button>
                </>
              )}
              {stats.unchanged > 0 && (
                <button type="button" onClick={() => handleReEvaluateUnchanged()} disabled={isTriggering} className="ms-btn is-sm is-ghost" title="Değişiklik yapılmamış soruları Faz 14 için yeniden kuyruğa al">
                  <RotateCcw /> Değişmeyenleri yeniden değerlendir ({stats.unchanged})
                </button>
              )}
            </div>
          </div>
          {liveStatus?.isRunning && liveStatus.paralel?.anahtarlar && (
            <ul className="m-0 p-0 list-none flex flex-wrap gap-1.5 text-[12px]" aria-label="Ücretsiz anahtar durumu">
              {Object.entries(liveStatus.paralel.anahtarlar).map(([ad, d]) => {
                const bekliyor = d.bekleme_bitis && Date.parse(d.bekleme_bitis) > Date.now();
                return (
                  <li key={ad} className={`px-2 py-1 rounded-md border ${d.kalan === 0 ? 'border-line text-ink-3' : bekliyor ? 'border-amber-300 bg-amber-50 text-amber-900' : 'border-emerald-300 bg-emerald-50 text-emerald-900'}`}>
                    {ad.replace('ücretsiz:', '').replace('GEMINI_FREE_KEY_', 'Anahtar ').replace('GEMINI_API_KEY', 'Anahtar 1')} · {d.cozulen} çözüldü · {d.kalan} kaldı
                    {bekliyor ? ` · ${new Date(d.bekleme_bitis!).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })}'e kadar bekliyor` : d.kalan ? ' · çalışıyor' : ''}
                  </li>
                );
              })}
            </ul>
          )}
          <div className={`ms-progress ${liveStatus?.isRunning && !total ? 'is-indeterminate' : ''}`} role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={progressPct} aria-label="İşlenen soru oranı">
            <span style={{ width: `${progressPct}%` }} />
          </div>
          <Collapsible
            className="ms-disc"
            open={showConsole}
            onToggle={setShowConsole}
            title={
              <span className="inline-flex items-center gap-2">
                <Terminal className="w-3.5 h-3.5 text-ink-3" /> Canlı günlük <span className="font-normal text-ink-3">phase14.log · son 50 satır</span>
              </span>
            }
          >
            <div className="bg-slate-950 p-3 rounded-lg font-mono text-[12px] text-slate-300 max-h-56 overflow-y-auto flex flex-col gap-0.5 select-text">
              {liveStatus?.logs && liveStatus.logs.length > 0 ? (
                liveStatus.logs.map((line, idx) => {
                  const isErr = line.includes('ERROR') || line.includes('hata') || line.includes('429') || line.includes('404');
                  const isOk = line.includes('✓') || line.includes('başarıyla') || line.includes('unchanged');
                  const isWarn = line.includes('WARNING') || line.includes('review_required');
                  return (
                    <div key={idx} className={`leading-relaxed whitespace-pre-wrap ${isErr ? 'text-rose-400' : isOk ? 'text-emerald-400' : isWarn ? 'text-amber-300' : 'text-slate-300'}`}>
                      {line}
                    </div>
                  );
                })
              ) : (
                <div className="text-slate-500">Henüz günlük kaydı yok.</div>
              )}
            </div>
          </Collapsible>
        </section>
      )}

      {actionFeedback && (
        <div role="status" className={`ms-pop-in flex items-center gap-2 px-3.5 py-2.5 rounded-xl text-[13.5px] font-medium ${actionFeedback.type === 'ok' ? 'bg-ok-soft text-ok' : 'bg-bad-soft text-bad-text'}`}>
          {actionFeedback.type === 'ok' ? <CheckCircle2 className="w-4 h-4 shrink-0" /> : <AlertTriangle className="w-4 h-4 shrink-0" />}
          <span className="flex-1 min-w-0">{actionFeedback.message.replace(/^✓\s*/, '')}</span>
          <button type="button" onClick={() => setActionFeedback(null)} className="ms-btn is-ghost is-sm is-icon text-inherit!" aria-label="Kapat">
            <X />
          </button>
        </div>
      )}

      {/* Arama + görünüm + sıralama */}
      <div className="flex flex-wrap items-center gap-2 min-w-0">
        <div className="ms-qsearch flex-1 basis-[260px]">
          <Search aria-hidden />
          <input type="search" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} placeholder="Soru ID, kök, şık, ders ya da not ara" aria-label="İncelemelerde ara" />
          {searchQuery && (
            <button type="button" onClick={() => setSearchQuery('')} className="ms-btn is-ghost is-sm is-icon" aria-label="Aramayı temizle">
              <X />
            </button>
          )}
        </div>
        <div className="ms-seg" role="radiogroup" aria-label="Görünüm">
          {([['list', 'Liste'], ['detail', 'Ayrıntılı']] as const).map(([id, label]) => (
            <button key={id} type="button" role="radio" aria-checked={layout === id} onClick={() => changeLayout(id)}>
              {label}
            </button>
          ))}
        </div>
        <label className="ms-btn is-ghost is-sm relative">
          <ArrowUpDown />
          {{ newest: 'En yeni', oldest: 'En eski', evidence_low: 'Kanıtı en zayıf', evidence_high: 'Kanıtı en güçlü' }[sortOrder]}
          <select value={sortOrder} onChange={(e) => setSortOrder(e.target.value as typeof sortOrder)} className="absolute inset-0 opacity-0 cursor-pointer" aria-label="Sıralama">
            <option value="newest">En yeni</option>
            <option value="oldest">En eski</option>
            <option value="evidence_low">Kanıtı en zayıf</option>
            <option value="evidence_high">Kanıtı en güçlü</option>
          </select>
        </label>
      </div>

      <div className="ms-chipbar" role="tablist" aria-label="Durum">
        {statusTabs.map((tab) => {
          const on = statusFilter === tab.id;
          return (
            <button key={tab.id} type="button" role="tab" aria-selected={on} onClick={() => setStatusFilter(tab.id)} className={`ms-fchip ${on ? 'is-on' : ''} ${!tab.count && !on ? 'is-zero' : ''}`}>
              {tab.id === 'answer_doubtful' && <BarChart3 className="w-3.5 h-3.5" aria-hidden />}
              {tab.label} <span className="n">{tab.count.toLocaleString('tr-TR')}</span>
            </button>
          );
        })}
      </div>

      {/* Liste & karşılaştırma kartları */}
      {isLoading ? (
        <div className="ms-qcard items-center py-10 text-ink-2">
          <div className="ms-progress is-indeterminate w-40"><span /></div>
          <span className="text-[13.5px]">İnceleme kayıtları yükleniyor…</span>
        </div>
      ) : error ? (
        <div className="ms-qcard items-center text-center py-8 text-bad-text">
          <AlertTriangle className="w-7 h-7" />
          <p className="m-0 font-semibold">{error}</p>
          <button type="button" onClick={() => fetchReviews()} className="ms-btn is-tonal">Yeniden dene</button>
        </div>
      ) : filteredReviews.length === 0 ? (
        <div className="ms-qcard items-center text-center py-10 text-ink-2">
          <Sparkles className="w-7 h-7 text-ink-3" />
          <h3 className="m-0 font-semibold text-[16px] text-ink">{searchQuery ? 'Aramaya uyan kayıt yok' : 'Bu durumda kayıt yok'}</h3>
          <p className="m-0 text-[13.5px] max-w-md text-ink-3">
            {searchQuery ? 'Farklı bir kelime ya da durum seç.' : 'Faz 14 bu süzgeç için henüz kayıt üretmedi. Süreci yukarıdan başlatabilirsin.'}
          </p>
        </div>
      ) : (
        <div className="flex flex-col gap-2.5 ms-stagger" key={statusFilter}>
          {filteredReviews.slice(0, visibleCount).map((rev) => {
            const qId = rev.question_id;
            const src = rev.source || ({} as any);
            const prop = rev.proposal || ({} as any);
            const isPending = rev.status === 'review_required';
            const isApproved = rev.status === 'approved';
            const isRejected = rev.status === 'rejected';
            const isUnchanged = rev.status === 'unchanged';
            const isDuplicate = (rev.status as string) === 'duplicate';
            const doubtful = Boolean(rev.answer_doubtful);
            // Cevabı kabul edilmiş ama anketi açık tutulan soru: kabul edilen cevap + topluluk oyları birlikte gösterilir
            const keptPoll = !doubtful && Boolean(rev.answer_poll_open) && Boolean(rev.answer_vote_result?.winner);
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
              ? { label: 'Onaylandı', cls: 'is-ok', Icon: CheckCircle2, dot: 'bg-ok' }
              : isRejected
              ? { label: 'Reddedildi', cls: 'is-bad', Icon: XCircle, dot: 'bg-bad' }
              : isUnchanged
              ? { label: 'Değişiklik yok', cls: '', Icon: Check, dot: 'bg-line-2' }
              : isDuplicate
              ? { label: `Kopya · #${(rev as any).duplicate_of || '?'}`, cls: '', Icon: Copy, dot: 'bg-line-2' }
              : { label: 'İnceleme bekliyor', cls: 'is-warn', Icon: Clock, dot: 'bg-warn' };
            const onCopy = async (which: 'src' | 'prop') => {
              const ok = await copyText(questionText(rev, which));
              if (ok) {
                setCopiedId(`${qId}:${which}`);
                window.setTimeout(() => setCopiedId((c) => (c === `${qId}:${which}` ? null : c)), 1600);
              } else {
                setActionFeedback({ message: 'Kopyalanamadı: tarayıcı panoya erişime izin vermedi.', type: 'err' });
              }
            };
            const copyBtn = (which: 'src' | 'prop', label: string) => {
              const done = copiedId === `${qId}:${which}`;
              return (
                <button
                  type="button"
                  onClick={(e) => { e.stopPropagation(); onCopy(which); }}
                  className="ms-btn is-ghost is-sm"
                  title={`${label} soruyu ve şıklarını kopyala (cevap anahtarı hariç)`}
                  aria-label={done ? 'Kopyalandı' : `${label} soruyu kopyala`}
                >
                  {done ? <Check className="text-ok" /> : <Copy />}
                  <span className="hidden sm:inline">{label}</span>
                </button>
              );
            };
            const srcExpl = String(src.aciklama || '');
            const propExpl = String(prop.aciklama || '');
            const explChanged = Boolean(propExpl) && propExpl.trim() !== srcExpl.trim();
            const pollOptions = (prop.secenekler && Object.keys(prop.secenekler).length ? prop.secenekler : src.secenekler) || {};
            const busy = processingId === qId;

            // Liste görünümü: tek satır; tıklayınca ayrıntılı kart açılır
            if (layout === 'list' && !openRows[qId]) {
              return (
                <article
                  key={qId}
                  className="ms-qcard flex-row! items-center gap-2! py-2! px-3! cursor-pointer"
                  onClick={() => setOpenRows((o) => ({ ...o, [qId]: true }))}
                >
                  <span className={`w-2 h-2 rounded-full shrink-0 ${status.dot}`} title={status.label} />
                  <span className="font-mono text-[12px] text-ink-3 shrink-0 hidden sm:inline">#{qId.slice(0, 8)}</span>
                  <span className="text-[13.5px] text-ink truncate min-w-0 flex-1">{propStem || srcStem}</span>
                  {doubtful && <span className="ms-tag is-warn hidden sm:inline-flex"><BarChart3 /> anket</span>}
                  {changes.length > 0 && <span className="ms-tag is-warn hidden md:inline-flex">müfredat</span>}
                  {explChanged && <span className="ms-tag is-ai hidden md:inline-flex">açıklama</span>}
                  <span className={`text-[12px] font-mono shrink-0 ${ratioPercent >= 80 ? 'text-ok' : 'text-bad-text'}`}>%{ratioPercent}</span>
                  {isAdmin && !isApproved && (
                    <button type="button" onClick={(e) => { e.stopPropagation(); handleApprove(qId); }} disabled={busy} className="ms-btn is-ghost is-sm is-icon text-ok!" title="Onayla" aria-label="Onayla">
                      <Check />
                    </button>
                  )}
                  {isAdmin && !isRejected && (
                    <button type="button" onClick={(e) => { e.stopPropagation(); handleReject(qId); }} disabled={busy} className="ms-btn is-ghost is-sm is-icon text-bad-text!" title="Reddet" aria-label="Reddet">
                      <X />
                    </button>
                  )}
                </article>
              );
            }

            const optList = (opts: Record<string, any>, correct: string | undefined, kind: 'src' | 'prop') => (
              <ol className="ms-opts gap-1!">
                {Object.entries(opts).map(([k, v]) => {
                  const upperKey = k.toUpperCase();
                  const isCorrect = !doubtful && String(correct || '').toUpperCase() === upperKey;
                  const before = srcOpt(upperKey);
                  const isAiCompleted = kind === 'prop' && (!before || aiCompletedList.includes(upperKey));
                  const optChanged = kind === 'prop' && view !== 'prop' && before && before.trim() !== String(v).trim();
                  return (
                    <li key={k} className={`ms-opt min-h-9! py-1.5! text-[13.5px]! ${isCorrect ? 'is-correct' : ''}`}>
                      <span className="ms-opt-key w-6! h-6! text-[12px]!">{isCorrect ? <Check className="w-3.5 h-3.5" strokeWidth={3} /> : upperKey}</span>
                      <span>{optChanged ? <DiffText before={before} after={String(v)} /> : String(v)}</span>
                      <span className="ms-opt-side">
                        {isAiCompleted && <span className="ms-tag is-ai" title="Bu şık kaynakta yoktu; AI tamamladı">AI</span>}
                        {kind === 'prop' && (isAiCompleted || (before && before.trim() !== String(v).trim())) && (
                          <ChangeInfo
                            title={`${upperKey} şıkkı ${isAiCompleted && !before ? 'eklendi' : 'değişti'}`}
                            before={before}
                            after={String(v)}
                            note={isAiCompleted ? 'Kaynakta bu şık eksikti; yapay zekâ tamamladı (doğrulanmadı).' : undefined}
                          />
                        )}
                      </span>
                    </li>
                  );
                })}
              </ol>
            );
            const answerLabel = (v?: string) => (doubtful ? <span className="ms-tag is-warn">Cevap belirsiz</span> : v ? <span className="ms-tag is-ok">Cevap {String(v).toUpperCase()}</span> : <span className="ms-tag">Cevap yok</span>);

            const moreActions: ActionItem[] = isAdmin
              ? [
                  ...(isPending
                    ? [
                        { label: rev.suspicious ? 'Şüpheli işaretini kaldır' : 'Şüpheli olarak işaretle', icon: Flag, onClick: () => handleToggleSuspicious(qId, !rev.suspicious) },
                        { label: doubtful ? 'Cevap anketini kapat' : 'Cevap anketini aç', icon: BarChart3, onClick: () => handleToggleAnswerDoubt(qId, !doubtful) },
                      ]
                    : []),
                  ...(keptPoll ? [{ label: 'Cevap anketini kapat', icon: BarChart3, onClick: () => handleToggleAnswerDoubt(qId, false) }] : []),
                  ...(isUnchanged || isRejected ? [{ label: 'Tekrar değerlendir', icon: RotateCcw, onClick: () => handleReEvaluateUnchanged(qId) }] : []),
                  { label: 'Terimler ve sözlük', icon: BookOpen, group: 'Bilgi', onClick: () => setTermsFor(rev) },
                ]
              : [{ label: 'Terimler ve sözlük', icon: BookOpen, onClick: () => setTermsFor(rev) }];

            return (
              <article key={qId} className="ms-qcard p-0! gap-0! overflow-hidden">
                {/* Başlık */}
                <header className="ms-qcard-head px-3 sm:px-4 pt-2.5 pb-2">
                  <span className="ms-qcard-num" title={`#${qId}`}>#{qId.slice(0, 8)}</span>
                  <span className={`ms-tag ${status.cls}`}><status.Icon /> <span className="hidden sm:inline">{status.label}</span></span>
                  {rev.answer_vote_result && (
                    <span className="ms-tag is-ok" title={`Kabul edilen cevap: ${rev.answer_vote_result.winner}${rev.answer_vote_result.total ? ` · kayıt anında ${rev.answer_vote_result.counts?.[rev.answer_vote_result.winner] || 0}/${rev.answer_vote_result.total} oy` : ''}${keptPoll ? ' · anket açık' : ''}`}>
                      <BarChart3 /> {rev.answer_vote_result.by === 'admin' ? 'Cevap seçildi' : 'Anket'}: {rev.answer_vote_result.winner}
                    </span>
                  )}
                  {doubtful && <span className="ms-tag is-warn"><BarChart3 /> Cevap belirsiz</span>}
                  {rev.suspicious && <span className="ms-tag is-bad"><Flag /> Şüpheli</span>}
                  <span className={`ms-tag ${ratioPercent >= 80 ? 'is-ok' : 'is-bad'} font-mono`} title={`Önerinin kaynak metinle örtüşme oranı: %${ratioPercent}`}>%{ratioPercent}</span>
                  <span className="ms-qcard-meta" title={changes.length ? 'Müfredat değişikliği önerildi' : undefined}>
                    {[kurulLabel(src.kurul_adi), src.ders_adi].filter(Boolean).join(' · ')}
                    {changes.some((c) => c.alan === 'Kurul' || c.alan === 'Ders') && (
                      <>
                        {' → '}
                        <b className="text-warn font-semibold">{[kurulLabel(prop.kurul_adi || src.kurul_adi), prop.ders_adi || src.ders_adi].filter(Boolean).join(' · ')}</b>
                      </>
                    )}
                  </span>
                  <span className="inline-flex items-center gap-0.5 ml-auto">
                    {copyBtn('src', 'Eski')}
                    {propStem && copyBtn('prop', 'Yeni')}
                    {layout === 'list' && (
                      <button type="button" onClick={() => setOpenRows((o) => ({ ...o, [qId]: false }))} className="ms-btn is-ghost is-sm">Daralt</button>
                    )}
                    <ActionMenu items={moreActions} title={`Soru #${qId.slice(0, 8)}`} />
                  </span>
                </header>

                {changes.length > 0 && (
                  <p className="mx-3 sm:mx-4 mb-2 m-0 px-2.5 py-1.5 rounded-lg bg-warn-soft text-warn text-[12.5px] leading-snug">
                    <b className="font-semibold">Müfredat:</b>{' '}
                    {changes.map((c, i) => (
                      <span key={c.alan}>
                        {i > 0 && ' · '}
                        {c.alan !== 'Kurul' && `${c.alan} `}
                        <span className="line-through opacity-70">{c.eski}</span> → <b>{c.yeni}</b>
                      </span>
                    ))}
                    {yzvNote?.mufredat_atamasi && <span className="block opacity-90 mt-0.5">{yzvNote.mufredat_atamasi}</span>}
                  </p>
                )}

                {/* Telefon/tablet: görünüm seçici */}
                <div className="lg:hidden px-3 sm:px-4 pb-2">
                  <div className="ms-seg w-full" role="tablist" aria-label="Karşılaştırma görünümü">
                    {([['diff', 'Fark'], ['src', 'Mevcut'], ['prop', 'Öneri']] as const).map(([id, label]) => (
                      <button key={id} type="button" role="tab" aria-selected={view === id} onClick={() => setCardView((v) => ({ ...v, [qId]: id }))} className="flex-1 justify-center">
                        {label}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="px-3 sm:px-4 pb-3 grid grid-cols-1 lg:grid-cols-2 gap-2.5">
                  {/* Mevcut kayıt */}
                  <section className={`${view === 'src' ? 'flex' : 'hidden'} lg:flex flex-col gap-2 p-3 rounded-xl bg-canvas min-w-0`}>
                    <h4 className="m-0 flex items-center justify-between gap-2 text-[12px] font-semibold text-ink-3">
                      <span className="inline-flex items-center gap-1"><FileText className="w-3.5 h-3.5" /> Mevcut kayıt</span>
                      {answerLabel(src.dogru_secenek)}
                    </h4>
                    {srcStem ? <StemText text={srcStem} size="sm" /> : <p className="m-0 text-[13.5px] text-ink-3 italic">Soru kökü boş</p>}
                    {src.secenekler && Object.keys(src.secenekler).length > 0 && optList(src.secenekler, src.dogru_secenek, 'src')}
                  </section>

                  {/* Öneri (fark işaretli) */}
                  <section className={`${view === 'src' ? 'hidden' : 'flex'} lg:flex flex-col gap-2 p-3 rounded-xl bg-accent-soft/40 min-w-0`}>
                    <h4 className="m-0 flex items-center justify-between gap-2 text-[12px] font-semibold text-accent">
                      <span className="inline-flex items-center gap-1"><Sparkles className="w-3.5 h-3.5" /> {modelLabel(rev.model)}</span>
                      <span className="inline-flex items-center gap-1">
                        {answerLabel(prop.dogru_secenek)}
                        {!doubtful && src.dogru_secenek && prop.dogru_secenek && String(src.dogru_secenek).toUpperCase() !== String(prop.dogru_secenek).toUpperCase() && (
                          <ChangeInfo title="Cevap değişti" before={String(src.dogru_secenek)} after={String(prop.dogru_secenek)} />
                        )}
                      </span>
                    </h4>
                    {!propStem ? (
                      <p className="m-0 text-[13.5px] text-ink-3 italic">Kökte değişiklik önerilmedi</p>
                    ) : stemChanged && view !== 'prop' ? (
                      <div className="flex items-start gap-1">
                        <p className="ms-stem is-sm m-0 flex-1 whitespace-pre-wrap"><DiffText before={srcStem} after={propStem} /></p>
                        <ChangeInfo title="Soru kökü değişikliği" before={srcStem} after={propStem} note={yzvNote?.soru_koku_duzeltmesi} />
                      </div>
                    ) : (
                      <StemText text={propStem} size="sm" />
                    )}
                    {doubtful || keptPoll ? (
                      <AnswerPoll
                        questionId={qId}
                        acceptedAnswer={keptPoll ? rev.answer_vote_result?.winner : undefined}
                        options={pollOptions}
                        voterUid={currentUser?.uid || null}
                        className="pt-1"
                        hint={keptPoll ? 'Cevap kabul edildi; anket açık kalıyor. Topluluğun cevabı kabul edilen cevapla karşılaştırılır.' : 'Çözücüler aynı şıkta uzlaşamadı. Doğru bildiğin şıkkı seç; herkes bir kez oy verebilir.'}
                        onVotes={(v) => {
                          const max = Math.max(0, ...Object.values(v.counts));
                          const lead = Object.keys(v.counts).filter((k) => max > 0 && v.counts[k] === max);
                          setPollLeader((m) => (lead.length === 1 && m[qId] !== lead[0] ? { ...m, [qId]: lead[0] } : m));
                        }}
                        renderText={(k, t) => {
                          const before = srcOpt(k);
                          return view !== 'prop' && before && before.trim() !== t.trim() ? <DiffText before={before} after={t} /> : t;
                        }}
                      />
                    ) : (
                      prop.secenekler && Object.keys(prop.secenekler).length > 0 && optList(prop.secenekler, prop.dogru_secenek, 'prop')
                    )}
                    {stemChanged && view !== 'prop' && (
                      <p className="m-0 text-[11.5px] text-ink-3">
                        <ins className="no-underline bg-emerald-100 text-emerald-900 rounded-sm px-0.5">eklenen</ins>{' '}
                        <del className="bg-rose-100 text-rose-800 rounded-sm px-0.5">çıkarılan</del> kelimeler, mevcut kayda göre
                      </p>
                    )}
                    {prop.cevap_belirsiz && !doubtful && (
                      <p className="ms-note is-warn m-0 rounded-lg bg-warn-soft px-2.5 py-1.5">Çözücüler aynı şıkta uzlaşamadı; cevap işaretlenmedi. Onaylamadan önce cevap anketini aç ya da "Düzenle" ile şıkkı seç.</p>
                    )}
                    {prop.aciklama_gecersiz && (
                      <p className="ms-note is-warn m-0 rounded-lg bg-warn-soft px-2.5 py-1.5">
                        Açıklama {prop.cevap_dogrulama?.aciklama_gosterdigi ? `${prop.cevap_dogrulama.aciklama_gosterdigi} şıkkını` : 'başka bir şıkkı'} savunuyor; işaretlenen cevap {String(prop.dogru_secenek || '–')}. Onaylamadan önce düzeltin.
                      </p>
                    )}
                  </section>
                </div>

                <div className="px-3 sm:px-4 pb-3 flex flex-col gap-2">
                  {(prop.degisiklik_ozeti || (prop.degisen_alanlar?.length ?? 0) > 0 || yzvNote?.soru_koku_duzeltmesi || prop.YZV?.referans_literatur || prop.cevap_dogrulama || prop.tespit_raporu || prop.secenek_analizi) && (
                    <Collapsible
                      className="ms-disc"
                      title={
                        <span className="inline-flex flex-wrap items-center gap-1.5">
                          Değişiklik notu
                          {(prop.degisen_alanlar || []).slice(0, 4).map((f: string) => <span key={f} className="ms-tag is-ai font-normal">{f}</span>)}
                        </span>
                      }
                    >
                      <div className="text-[13px] text-ink-2 flex flex-col gap-1.5 leading-relaxed">
                        {prop.degisiklik_ozeti && <p className="m-0">{typeof prop.degisiklik_ozeti === 'string' ? prop.degisiklik_ozeti : JSON.stringify(prop.degisiklik_ozeti)}</p>}
                        {yzvNote?.soru_koku_duzeltmesi && <p className="m-0"><b className="text-ink">Kök:</b> {yzvNote.soru_koku_duzeltmesi}</p>}
                        {prop.cevap_dogrulama && (
                          <p className="m-0">
                            <b className="text-ink">Cevap kontrolü:</b>{' '}
                            {prop.cevap_dogrulama.oylar
                              ? Object.entries(prop.cevap_dogrulama.oylar as Record<string, string>)
                                  .map(([k, v]) => `${({ duzelten_model: 'düzelten model', gpt_oss: 'gpt-oss', ucuncu: '3. çözücü', gemini: 'Gemini' } as Record<string, string>)[k] || k} ${v || '?'}`)
                                  .join(' · ')
                              : `model ${prop.cevap_dogrulama.oneri || '–'} · bağımsız ${prop.cevap_dogrulama.dogrulayici || '?'}`}
                            {' → '}
                            <b className="text-ink">{prop.dogru_secenek || 'belirsiz'}</b>
                            {prop.cevap_dogrulama.eski_anahtar ? ` (eski anahtar ${prop.cevap_dogrulama.eski_anahtar}, kararda kullanılmadı)` : ''}
                          </p>
                        )}
                        {Array.isArray(prop.cevap_secenekleri) && prop.cevap_secenekleri.length > 0 && (
                          <p className="m-0 rounded-md bg-warn-soft px-2 py-1">
                            <b className="text-ink">Şüpheli cevap · {prop.cevap_secenekleri.length} cevap:</b>{' '}
                            {(prop.cevap_secenekleri as { model: string; cevap: string }[])
                              .map((c) => `${String(c.model).replace(/^(groq|gemini):/, '').replace('openai/', '')} → ${c.cevap}`)
                              .join(' · ')}
                          </p>
                        )}
                        {prop.YZV?.referans_literatur && <p className="m-0"><b className="text-ink">Literatür:</b> {prop.YZV.referans_literatur}</p>}
                        {prop.tespit_raporu?.tespit_edilen_kusur && <p className="m-0"><b className="text-ink">Tespit edilen kusur:</b> {String(prop.tespit_raporu.tespit_edilen_kusur)}</p>}
                        {prop.tespit_raporu?.uygulanan_mudahale && <p className="m-0"><b className="text-ink">Uygulanan müdahale:</b> {String(prop.tespit_raporu.uygulanan_mudahale)}</p>}
                        {prop.secenek_analizi && typeof prop.secenek_analizi === 'object' && (
                          <div className="flex flex-col gap-1 pt-1">
                            <b className="text-ink">Şık analizi</b>
                            {['A', 'B', 'C', 'D', 'E'].map((k) => {
                              const t = (prop.secenek_analizi as Record<string, any>)[k] ?? (prop.secenek_analizi as Record<string, any>)[k.toLowerCase()];
                              return t ? (
                                <p key={k} className={`m-0 ${!doubtful && String(prop.dogru_secenek || '').toUpperCase() === k ? 'text-ok font-medium' : ''}`}>
                                  <b>{k}:</b> {String(t)}
                                </p>
                              ) : null;
                            })}
                          </div>
                        )}
                      </div>
                    </Collapsible>
                  )}

                  {(srcExpl || propExpl) && (
                    <Collapsible
                      className="ms-disc"
                      title={
                        <span className="inline-flex flex-wrap items-center gap-1.5">
                          Açıklama
                          <span className={`ms-tag font-normal ${explChanged ? 'is-ai' : ''}`}>{explChanged ? (srcExpl ? 'değiştirildi' : 'yeni eklendi') : 'değişmedi'}</span>
                        </span>
                      }
                    >
                      {yzvNote?.aciklama_duzeltmesi && <p className="m-0 mb-2 text-[12.5px] text-ink-3">{yzvNote.aciklama_duzeltmesi}</p>}
                      <div className="grid gap-2 lg:grid-cols-2 text-[13px]">
                        <div className="rounded-lg bg-white p-2.5 min-w-0">
                          <p className="m-0 mb-1 text-[11.5px] font-semibold text-ink-3">Eski</p>
                          <p className="m-0 whitespace-pre-wrap leading-relaxed text-ink-2 wrap-anywhere">{srcExpl || <i className="text-ink-3">Açıklama yoktu</i>}</p>
                        </div>
                        <div className="rounded-lg bg-white p-2.5 min-w-0">
                          <p className="m-0 mb-1 text-[11.5px] font-semibold text-accent">Yeni</p>
                          <p className="m-0 whitespace-pre-wrap leading-relaxed text-ink wrap-anywhere">{propExpl || <i className="text-ink-3">Öneri açıklama içermiyor</i>}</p>
                        </div>
                      </div>
                      {explChanged && srcExpl && (
                        <details className="pt-2 text-[13px] text-ink-2">
                          <summary className="cursor-pointer text-[12.5px] text-ink-3 py-1">Kelime farkını göster</summary>
                          <p className="m-0 whitespace-pre-wrap leading-relaxed break-words"><DiffText before={srcExpl} after={propExpl} /></p>
                        </details>
                      )}
                    </Collapsible>
                  )}
                </div>

                {/* Eylemler + künye */}
                <footer className="px-3 sm:px-4 py-2 border-t border-line-soft flex flex-wrap items-center gap-1.5">
                  {isAdmin && (
                    <>
                      {isPending && doubtful ? (
                        <div className="flex flex-wrap items-center gap-1.5 w-full sm:w-auto">
                          <span className="text-[12.5px] text-ink-3">Doğru cevap</span>
                          <div className="ms-seg" role="radiogroup" aria-label="Kaydedilecek doğru cevap">
                            {Object.keys(pollOptions).map((k) => k.toUpperCase()).filter((k) => /^[A-E]$/.test(k)).map((k) => {
                              const sel = (answerPick[qId] || pollLeader[qId]) === k;
                              return (
                                <button key={k} type="button" role="radio" aria-checked={sel} onClick={() => setAnswerPick((m) => ({ ...m, [qId]: k }))} className={`font-mono min-w-8 justify-center ${sel ? 'bg-ok! text-white! shadow-none!' : ''}`} title={pollLeader[qId] === k ? 'Ankette önde' : undefined}>
                                  {k}
                                </button>
                              );
                            })}
                          </div>
                          <button
                            type="button"
                            onClick={() => handleCompleteAnswerDoubt(qId, answerPick[qId] || pollLeader[qId])}
                            disabled={busy || !(answerPick[qId] || pollLeader[qId])}
                            className="ms-btn is-sm is-ok"
                            title="Seçili şıkkı cevap olarak kaydet ve soruyu onaylayıp çıkmış sorulara gönder"
                          >
                            <Check /> Kaydet · çıkmışa gönder
                          </button>
                        </div>
                      ) : (
                        !isApproved && (
                          <button type="button" onClick={() => handleApprove(qId)} disabled={busy} className="ms-btn is-sm is-ok">
                            <Check /> Onayla
                          </button>
                        )
                      )}
                      {!isRejected && (
                        <button type="button" onClick={() => handleReject(qId)} disabled={busy} className="ms-btn is-sm is-danger">
                          <X /> Reddet
                        </button>
                      )}
                      <button type="button" onClick={() => openEditModal(rev)} className="ms-btn is-sm is-ghost">
                        <Edit3 /> Düzenle
                      </button>
                    </>
                  )}
                  <p className="m-0 ml-auto text-[11.5px] text-ink-3 flex flex-wrap gap-x-2.5 gap-y-0.5 min-w-0">
                    <span className="font-mono">{rev.model || 'model bilinmiyor'}</span>
                    {rev.processed_at && <span>{rev.processed_at.slice(0, 16).replace('T', ' ')}</span>}
                    {rev.approved_at && <span className="text-ok">Onay {rev.approved_at.slice(0, 16).replace('T', ' ')}</span>}
                    {rev.rejected_at && <span className="text-bad-text">Red {rev.rejected_at.slice(0, 16).replace('T', ' ')}</span>}
                  </p>
                </footer>
              </article>
            );
          })}
          {filteredReviews.length > visibleCount && (
            <button type="button" onClick={() => setVisibleCount((c) => c + PAGE_SIZE)} className="ms-btn is-outline h-11! w-full">
              Daha fazla göster ({(filteredReviews.length - visibleCount).toLocaleString('tr-TR')} kayıt daha)
            </button>
          )}
        </div>
      )}

      {termsFor && <TermsDialog rev={termsFor} onClose={() => setTermsFor(null)} />}

      {/* Öneriyi düzenle */}
      {editingReview && (
        <div
          className="ms-overlay fixed inset-0 z-50 flex items-center justify-center p-4"
          role="dialog"
          aria-modal="true"
          aria-labelledby="tc-edit-title"
          onMouseDown={(e) => e.target === e.currentTarget && !isSavingEdit && setEditingReview(null)}
          onKeyDown={(e) => e.key === 'Escape' && !isSavingEdit && setEditingReview(null)}
        >
          <div className="ms-modal-panel bg-white w-full max-w-2xl flex flex-col overflow-hidden">
            <header className="flex items-center gap-2 px-5 pt-4 pb-3 border-b border-line-soft">
              <h3 id="tc-edit-title" className="m-0 flex-1 min-w-0 font-display text-[17px] font-semibold text-ink truncate">
                Öneriyi düzenle <span className="font-mono text-[13px] font-normal text-ink-3">#{editingReview.question_id.slice(0, 8)}</span>
              </h3>
              <button type="button" onClick={() => setEditingReview(null)} aria-label="Kapat" className="ms-btn is-ghost is-icon">
                <X />
              </button>
            </header>

            <div className="flex-1 min-h-0 overflow-y-auto px-5 py-4 flex flex-col gap-4">
              <p className="m-0 text-[12.5px] leading-relaxed text-warn bg-warn-soft rounded-lg px-3 py-2">
                Kökün yönünü (olumlu/olumsuz) ve cevabı değiştirecek oynamalar yapma; yalnız imla, OCR bozukluğu, terim ve eksik şıkları düzelt.
              </p>

              <label className="flex flex-col gap-1.5">
                <span className="text-[12.5px] font-semibold text-ink-3">Soru kökü</span>
                <textarea
                  rows={5}
                  value={editStem}
                  onChange={(e) => setEditStem(e.target.value)}
                  className="w-full p-3 rounded-xl bg-field border border-transparent focus:border-accent focus:bg-white text-ink text-[16px] sm:text-[14px] outline-0 leading-relaxed resize-y"
                  placeholder="Düzeltilmiş soru kökü"
                />
                <span className="text-[11.5px] text-ink-3">Maddeli kökte her maddeyi ayrı satıra yaz (I. … / II. …); listede maddeler ayrı gösterilir.</span>
              </label>

              <fieldset className="m-0 p-0 border-0 flex flex-col gap-1.5">
                <legend className="mb-1.5 text-[12.5px] font-semibold text-ink-3">Şıklar · doğru şıkkın harfine dokun</legend>
                {(['A', 'B', 'C', 'D', 'E'] as const).map((key) => {
                  const on = editCorrectAnswer === key;
                  return (
                    <div key={key} className="flex items-center gap-2">
                      <button
                        type="button"
                        role="radio"
                        aria-checked={on}
                        aria-label={`${key} doğru cevap`}
                        onClick={() => setEditCorrectAnswer(key)}
                        className={`w-9 h-9 rounded-xl font-mono text-[13px] font-semibold shrink-0 inline-flex items-center justify-center cursor-pointer transition-colors ${on ? 'bg-ok text-white' : 'bg-field text-ink-2 hover:bg-line'}`}
                      >
                        {on ? <Check className="w-4 h-4" strokeWidth={3} /> : key}
                      </button>
                      <input
                        type="text"
                        value={editOptions[key]}
                        onChange={(e) => setEditOptions((prev) => ({ ...prev, [key]: e.target.value }))}
                        className={`flex-1 min-w-0 h-10 px-3 rounded-xl border text-[16px] sm:text-[14px] text-ink outline-0 focus:border-accent ${on ? 'bg-ok-tint border-transparent' : 'bg-field border-transparent focus:bg-white'}`}
                        placeholder={`${key} şıkkı`}
                      />
                    </div>
                  );
                })}
              </fieldset>

              <label className="flex flex-col gap-1.5">
                <span className="text-[12.5px] font-semibold text-ink-3">Açıklama</span>
                <textarea
                  rows={4}
                  value={editExplanation}
                  onChange={(e) => setEditExplanation(e.target.value)}
                  className="w-full p-3 rounded-xl bg-field border border-transparent focus:border-accent focus:bg-white text-ink text-[16px] sm:text-[14px] outline-0 leading-relaxed resize-y"
                  placeholder="Soruya ait tıbbi açıklama"
                />
              </label>

              <label className="flex flex-col gap-1.5">
                <span className="text-[12.5px] font-semibold text-ink-3">Değişiklik notu</span>
                <input
                  type="text"
                  value={editSummary}
                  onChange={(e) => setEditSummary(e.target.value)}
                  className="w-full h-10 px-3 rounded-xl bg-field border border-transparent focus:border-accent focus:bg-white text-[16px] sm:text-[14px] text-ink outline-0"
                  placeholder="Örn: C şıkkındaki imla hatası düzeltildi."
                />
              </label>
            </div>

            <footer className="flex flex-wrap items-center justify-end gap-2 px-5 py-3 border-t border-line-soft" style={{ paddingBottom: 'max(0.75rem, env(safe-area-inset-bottom))' }}>
              <button type="button" onClick={() => setEditingReview(null)} disabled={isSavingEdit} className="ms-btn is-ghost">
                İptal
              </button>
              <button type="button" onClick={() => handleSaveEditProposal(false)} disabled={isSavingEdit} className="ms-btn is-tonal">
                Kaydet
              </button>
              <button type="button" onClick={() => handleSaveEditProposal(true)} disabled={isSavingEdit} className="ms-btn is-ok">
                {isSavingEdit ? <RefreshCw className="animate-spin" /> : <Check />}
                {isSavingEdit ? 'Kaydediliyor…' : 'Kaydet ve onayla'}
              </button>
            </footer>
          </div>
        </div>
      )}
    </div>
  );
};
