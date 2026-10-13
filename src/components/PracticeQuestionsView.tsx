import React, { useEffect, useMemo, useState } from 'react';
import { copyQuestion } from '../utils/copyQuestion';
import { getVoterId } from '../utils/voterId';
import {
  BookOpen,
  Check,
  X,
  RotateCcw,
  Sparkles,
  Filter,
  Search,
  ThumbsUp,
  ThumbsDown,
  MessageSquare,
  Copy,
  Share2,
  Info,
  Send,
  Flag,
} from 'lucide-react';
import { ReportQuestionModal } from './ReportQuestionModal';
import { PageHeader } from './ui/PageHeader';
import { QuestionAboutDialog } from './QuestionAboutDialog';
import { toast } from './ui/Toast';
import { safeJsonFetch, ApiService } from '../services/api';
import { KazanimSorulariView, KAZANIM_INDEX } from './KazanimSorulariView';
import { pathFor } from '../router';

/**
 * Örnek çalışma soruları (/ornek-sorular): müfredata dayalı, Drive ders notlarından (drive_root) yapay zekâ ile üretilmiş,
 * her biri ders notundan birebir alıntıyla kaynaklı. Yönetici doğrulamasından geçmemiştir — sayfada açıkça belirtilir.
 * Veri: /api/practice-questions (meds_database/derived/ornek_sorular/sorular.jsonl).
 */
type PQ = {
  id: string;
  kurul: number;
  lesson_id?: string;
  ders: string;
  konu: string;
  ogretim_uyesi?: string;
  kazanim_no?: number;
  kazanim_metin?: string;
  soru_koku: string;
  soru?: string;
  secenekler: Record<string, string>;
  dogru_secenek: string;
  dogru?: string;
  aciklama?: string;
  aciklama_maddeleri?: string[];
  sik_aciklamalari?: Record<string, string>;
  zorluk?: string;
  version?: string;
  kaynak?: { ders_notu?: string; sayfa?: number; alinti?: string };
  model?: string;
  olusturma?: string;
};

const LETTERS = ['A', 'B', 'C', 'D', 'E'];

type PQComment = { id: string; author: string; text: string; timestamp: string };
type PQSocial = {
  upvotes: number;
  downvotes: number;
  liked: boolean;
  disliked: boolean;
  comments: PQComment[];
};

const PQ_SOCIAL_KEY = 'medsoru_ornek_havuz_social';
let PQ_SOCIAL_STORE: Record<string, PQSocial> = (() => {
  try { return JSON.parse(window.localStorage.getItem(PQ_SOCIAL_KEY) || '{}') || {}; } catch { return {}; }
})();
const pqSocialListeners = new Set<() => void>();

function notifyPqSocial() {
  try { window.localStorage.setItem(PQ_SOCIAL_KEY, JSON.stringify(PQ_SOCIAL_STORE)); } catch {}
  pqSocialListeners.forEach((fn) => fn());
}

function usePqSocial(id: string): [PQSocial, { toggleLike: () => void; toggleDislike: () => void; addComment: (text: string, author?: string) => void }] {
  const [, setTick] = useState(0);
  useEffect(() => {
    const fn = () => setTick((t) => t + 1);
    pqSocialListeners.add(fn);
    return () => { pqSocialListeners.delete(fn); };
  }, []);

  const current: PQSocial = PQ_SOCIAL_STORE[id] || { upvotes: 0, downvotes: 0, liked: false, disliked: false, comments: [] };

  const actions = useMemo(() => ({
    toggleLike: () => {
      const prev = PQ_SOCIAL_STORE[id] || { upvotes: 0, downvotes: 0, liked: false, disliked: false, comments: [] };
      const isLiked = prev.liked;
      const isDisliked = prev.disliked;
      const newLiked = !isLiked;
      const newDisliked = isLiked ? isDisliked : false;
      const newUp = isLiked ? Math.max(0, prev.upvotes - 1) : prev.upvotes + 1;
      const newDown = isDisliked ? Math.max(0, prev.downvotes - 1) : prev.downvotes;
      PQ_SOCIAL_STORE = {
        ...PQ_SOCIAL_STORE,
        [id]: { ...prev, liked: newLiked, disliked: newDisliked, upvotes: newUp, downvotes: newDown }
      };
      notifyPqSocial();
      try { ApiService.upvotePastQuestion(id, getVoterId()); } catch {}
    },
    toggleDislike: () => {
      const prev = PQ_SOCIAL_STORE[id] || { upvotes: 0, downvotes: 0, liked: false, disliked: false, comments: [] };
      const isDisliked = prev.disliked;
      const isLiked = prev.liked;
      const newDisliked = !isDisliked;
      const newLiked = isDisliked ? isLiked : false;
      const newDown = isDisliked ? Math.max(0, prev.downvotes - 1) : prev.downvotes + 1;
      const newUp = isLiked ? Math.max(0, prev.upvotes - 1) : prev.upvotes;
      PQ_SOCIAL_STORE = {
        ...PQ_SOCIAL_STORE,
        [id]: { ...prev, liked: newLiked, disliked: newDisliked, upvotes: newUp, downvotes: newDown }
      };
      notifyPqSocial();
      try { ApiService.downvotePastQuestion(id, getVoterId()); } catch {}
    },
    addComment: (text: string, author: string = 'Tıp Öğrencisi') => {
      if (!text.trim()) return;
      const prev = PQ_SOCIAL_STORE[id] || { upvotes: 0, downvotes: 0, liked: false, disliked: false, comments: [] };
      const newComment: PQComment = {
        id: `c_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
        author: author.trim() || 'Tıp Öğrencisi',
        text: text.trim(),
        timestamp: new Date().toISOString(),
      };
      PQ_SOCIAL_STORE = {
        ...PQ_SOCIAL_STORE,
        [id]: { ...prev, comments: [...(prev.comments || []), newComment] }
      };
      notifyPqSocial();
      ApiService.commentPastQuestion(id, author, text.trim()).catch((e) => console.warn('[yorum] gönderilemedi:', e?.message));
    }
  }), [id]);

  return [current, actions];
}

function QuestionCard({ q, n, onOpenAbout }: { q: PQ; n: number; onOpenAbout?: (q: PQ) => void }) {
  const [picked, setPicked] = useState<string | null>(null);
  const done = picked !== null;
  const correctVal = q.dogru_secenek || q.dogru || 'A';
  const correct = picked === correctVal;
  const soruMetni = q.soru_koku || q.soru || '';
  const aciklamalar = q.aciklama_maddeleri && q.aciklama_maddeleri.length > 0 
    ? q.aciklama_maddeleri 
    : (q.aciklama ? [q.aciklama] : []);

  const [social, socialActions] = usePqSocial(q.id);
  const [showComments, setShowComments] = useState(false);
  const [commentText, setCommentText] = useState('');
  const [copied, setCopied] = useState(false);
  const [reporting, setReporting] = useState(false);

  const handleCopy = () => {
    void copyQuestion(soruMetni, LETTERS.filter((k) => q.secenekler && q.secenekler[k]).map((k) => ({ key: k, text: q.secenekler[k] })));
    setCopied(true);
    toast.success('Soru kopyalandı', 'Soru metni ve şıklar panoya kopyalandı.');
    setTimeout(() => setCopied(false), 2000);
  };

  const handleShare = async () => {
    const url = `${window.location.origin}${pathFor('ornek_sorular')}?havuzId=${encodeURIComponent(q.id)}`;
    const title = `Örnek Soru · ${q.ders} · ${q.konu}`;
    if (navigator.share && window.matchMedia?.('(pointer: coarse)').matches) {
      try {
        await navigator.share({ title, url });
        return;
      } catch (e: any) {
        if (e?.name === 'AbortError') return;
      }
    }
    try {
      await navigator.clipboard.writeText(url);
      toast.success('Bağlantı kopyalandı', 'Soruyu bu bağlantıyla paylaşabilirsin.');
    } catch {
      toast.info('Bağlantı', url);
    }
  };

  const handleAddComment = () => {
    if (!commentText.trim()) return;
    socialActions.addComment(commentText);
    setCommentText('');
    toast.success('Yorum eklendi');
  };

  return (
    <article data-auto-reveal className="qk is-ornek">
      <header className="qk-h">
        {q.kurul && <span className="qk-chip" title={`Kurul ${q.kurul}`}>K{q.kurul}</span>}
        <span className="qk-kunye">{[`#${n}`, q.kazanim_no ? `Kaz. ${q.kazanim_no}` : null].filter(Boolean).join(' · ')}</span>
        {q.ders && <span className="qk-ders">{q.ders}</span>}
        <span className="qk-flags">
          {q.zorluk && <span className={`cx-flag ${q.zorluk === 'zor' ? 'is-warn' : q.zorluk === 'kolay' ? 'is-ok' : ''}`}>{q.zorluk}</span>}
          {done && <span className={`cx-flag ${correct ? 'is-ok' : 'is-bad'}`}>{correct ? 'Doğru' : 'Yanlış'}</span>}
        </span>
        <span className="qk-sp" />
        {onOpenAbout && (
          <button type="button" onClick={() => onOpenAbout(q)} className="qk-ib" aria-label="Soru hakkında" title="Soru hakkında"><Info aria-hidden /></button>
        )}
        <button type="button" onClick={handleCopy} className={`qk-ib ${copied ? 'is-done' : ''}`} aria-label={copied ? 'Kopyalandı' : 'Soru kökünü ve şıkları kopyala'} title={copied ? 'Kopyalandı' : 'Soru kökünü ve şıkları kopyala'}>
          {copied ? <Check aria-hidden /> : <Copy aria-hidden />}
        </button>
        <button type="button" onClick={() => setReporting(true)} className="qk-ib" aria-label="Hata bildir" title="Soruda hata ya da sorun bildir"><Flag aria-hidden /></button>
      </header>
      <div className="qk-stem">{soruMetni}</div>
      <ol className="qk-opts" aria-label="Şıklar">
        {LETTERS.filter((k) => q.secenekler && q.secenekler[k]).map((k) => {
          const isRight = k === correctVal;
          const isPicked = k === picked;
          const st = !done ? '' : isRight ? 'is-correct' : isPicked ? 'is-wrong' : 'is-dim';
          return (
            <li key={k} className="qk-opt-li">
              <button type="button" disabled={done} onClick={() => setPicked(k)} className={`qk-opt ${st}`} aria-pressed={isPicked}>
                <span className="qk-bub" aria-hidden>{done && isRight ? <Check strokeWidth={3} /> : done && isPicked ? <X strokeWidth={3} /> : k}</span>
                <span className="qk-opt-t">{q.secenekler[k]}</span>
                {done && (isRight || isPicked) && <span className={`qk-opt-tag ${isRight ? 'is-ok' : 'is-bad'}`}>{isPicked ? 'Senin cevabın' : 'Doğru cevap'}</span>}
              </button>
            </li>
          );
        })}
      </ol>
      {done && (
        <>
          <p className={`qk-verdict ${correct ? 'is-ok' : 'is-bad'}`} role="status">
            <b>{correct ? 'Doğru' : `Yanlış · doğru cevap ${correctVal}`}</b>
            <span className="qk-sp" />
            <button type="button" onClick={() => setPicked(null)}><RotateCcw aria-hidden /> Tekrar çöz</button>
          </p>
          <div className="qk-discs">
            <div className="qk-disc is-open">
              <div className="qk-disc-h is-static"><BookOpen aria-hidden /><span>Açıklama ve şık analizi</span></div>
              <div className="qk-disc-b"><div className="qk-disc-in">
                {aciklamalar.length > 0 && (
                  <ul className="m-0 pl-5 flex flex-col gap-1 text-[14px] text-ink leading-relaxed">
                    {aciklamalar.map((m, i) => <li key={i}>{m}</li>)}
                  </ul>
                )}
                {q.sik_aciklamalari && LETTERS.some((k) => q.sik_aciklamalari![k]) && (
                  <dl className="qk-analysis">
                    {LETTERS.filter((k) => q.sik_aciklamalari![k]).map((k) => (
                      <div key={k} className={k === correctVal ? 'is-correct' : ''}><dt>{k}</dt><dd>{q.sik_aciklamalari![k]}</dd></div>
                    ))}
                  </dl>
                )}
                {q.kaynak?.alinti && (
                  <p className="qk-refs"><b>Kaynak</b>{q.kaynak.ders_notu}{q.kaynak.sayfa ? ` · s. ${q.kaynak.sayfa}` : ''} — “{q.kaynak.alinti}”</p>
                )}
              </div></div>
            </div>
          </div>
        </>
      )}

      <footer className="qk-f">
        <button type="button" onClick={socialActions.toggleLike} aria-pressed={social.liked} title={social.liked ? 'Beğeniyi geri al' : 'Soruyu beğen'} className={`qk-act ${social.liked ? 'is-on' : ''}`}>
          <ThumbsUp className={social.liked ? 'fill-current' : ''} aria-hidden /><span>{social.upvotes || 0}</span>
        </button>
        <button type="button" onClick={socialActions.toggleDislike} aria-pressed={social.disliked} title={social.disliked ? 'Beğenmemeyi geri al' : 'Eksik ya da hatalı'} className={`qk-act ${social.disliked ? 'is-bad' : ''}`}>
          <ThumbsDown className={social.disliked ? 'fill-current' : ''} aria-hidden /><span>{social.downvotes || 0}</span>
        </button>
        <button type="button" onClick={() => setShowComments((prev) => !prev)} aria-expanded={showComments} className={`qk-act ${showComments ? 'is-on' : ''}`}>
          <MessageSquare aria-hidden /><span>{(social.comments || []).length}</span><span className="sr-only"> yorum</span>
        </button>
        <span className="qk-sp" />
        <button type="button" onClick={handleShare} className="qk-act" aria-label="Soruyu paylaş" title="Soru bağlantısını paylaş"><Share2 aria-hidden /></button>
      </footer>
      {reporting && (
        <ReportQuestionModal
          question={{ stem: soruMetni, correctAnswer: correctVal, discipline: q.ders, questionNumber: q.id }}
          onClose={() => setReporting(false)}
          onSubmit={async (reason, details) => {
            await ApiService.reportOrnekQuestion(q.id, reason, [details, `Kaynak: Çalışma soruları · Kurul ${q.kurul} · ${q.ders}`].filter(Boolean).join('\n'));
          }}
        />
      )}

      {/* Yorumlar Paneli */}
      {showComments && (
        <div className="ms-pop-in bg-field rounded-xl p-2.5 m-2 mt-0 flex flex-col gap-2">
          <div className="flex flex-col gap-1.5 max-h-56 overflow-y-auto">
            {(social.comments || []).length > 0 ? (
              social.comments.map((c) => (
                <div key={c.id} className="bg-white rounded-[10px] px-3 py-2 flex flex-col gap-0.5">
                  <div className="flex items-center justify-between gap-2 text-xs text-ink-3">
                    <span className="font-semibold text-ink">{c.author || 'Tıp Öğrencisi'}</span>
                    <span>{new Date(c.timestamp).toLocaleDateString('tr-TR')}</span>
                  </div>
                  <p className="m-0 text-base text-ink-2 leading-relaxed">{c.text}</p>
                </div>
              ))
            ) : (
              <p className="m-0 px-1 text-base text-ink-3">Henüz yorum yok. Bir ipucu ya da not ekleyen ilk kişi ol.</p>
            )}
          </div>
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') handleAddComment(); }}
              placeholder="Yorum ya da ipucu yaz…"
              aria-label="Yorum"
              className="flex-1 min-w-0 h-10 bg-white border border-line rounded-full px-4 text-md outline-0 focus:border-accent"
            />
            <button
              type="button"
              onClick={handleAddComment}
              disabled={!commentText.trim()}
              aria-label="Gönder"
              className="ms-btn is-primary is-icon"
            >
              <Send />
            </button>
          </div>
        </div>
      )}
    </article>
  );
}

const SEKME_KEY = 'medsoru_ornek_sekme';

export const PracticeQuestionsView: React.FC<{
  initialLessonId?: string | null;
  initialKazanimNo?: number | null;
  /** Derin bağlantı: /ornek-sorular/<soruId> (eski ?ornekId=) kazanım sorusu; ?havuzId= serbest havuz sorusu */
  initialQuestionId?: string | null;
}> = ({ initialLessonId, initialKazanimNo, initialQuestionId }) => {
  const havuzId = useMemo(() => {
    try { return new URLSearchParams(window.location.search).get('havuzId'); } catch { return null; }
  }, [initialQuestionId]);
  const [sekme, setSekme] = useState<'k1' | 'havuz'>(() => {
    if (initialLessonId || initialQuestionId) return 'k1';
    if (havuzId) return 'havuz';
    try { return (window.localStorage.getItem(SEKME_KEY) as any) || 'k1'; } catch { return 'k1'; }
  });

  useEffect(() => {
    if (initialLessonId || initialQuestionId) setSekme('k1');
    else if (havuzId) setSekme('havuz');
  }, [initialLessonId, initialQuestionId, havuzId]);

  const sekmeSec = (v: 'k1' | 'havuz') => { 
    setSekme(v); 
    try { window.localStorage.setItem(SEKME_KEY, v); } catch { /* depolama kapalı */ } 
  };

  const k1Soru = KAZANIM_INDEX.reduce((a, x) => a + x.soru_sayisi, 0);
  const k1Kazanim = KAZANIM_INDEX.reduce((a, x) => a + x.kazanim, 0);
  const sekmeBtn = (v: 'k1' | 'havuz', label: string) => (
    <button type="button" role="tab" aria-selected={sekme === v} onClick={() => sekmeSec(v)}>
      {label}
    </button>
  );

  return (
    <div className="flex flex-col gap-4 pb-16 w-full min-w-0">
      <PageHeader
        title="Örnek sorular"
        description="Kurul 1 kazanımlarına göre kolay, orta ve zor sorular; cevaplayınca her şıkkın gerekçesi açılır."
        stats={[
          { label: 'ders', value: String(KAZANIM_INDEX.length) },
          { label: 'kazanım', value: k1Kazanim.toLocaleString('tr-TR') },
          { label: 'soru', value: k1Soru.toLocaleString('tr-TR') },
        ]}
      />
      <div role="tablist" aria-label="Soru kümesi" className="ms-seg self-start">
        {sekmeBtn('k1', 'Ders kataloğu')}
        {sekmeBtn('havuz', 'Serbest arama')}
      </div>
      {sekme === 'k1' ? (
        <KazanimSorulariView
          initialLessonId={initialLessonId}
          initialKazanimNo={initialKazanimNo}
          initialQuestionId={initialQuestionId}
        />
      ) : (
        <TumHavuzUretim focusId={havuzId} />
      )}
    </div>
  );
};

/** Supabase practice_questions tablosundan tüm soruları çeken ve filtreleyen görünüm */
const TumHavuzUretim: React.FC<{ focusId?: string | null }> = ({ focusId }) => {
  const [all, setAll] = useState<PQ[] | null>(null);
  // Paylaşılan havuz sorusu (?havuzId=) yalnız o soruyla açılır; "Tüm sorular" listeye döner.
  const [odak, setOdak] = useState<string | null>(focusId || null);
  useEffect(() => { setOdak(focusId || null); }, [focusId]);

  const [totalCount, setTotalCount] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);
  const [kurul, setKurul] = useState<string>('');
  const [version, setVersion] = useState<string>('');
  const [ders, setDers] = useState<string>('');
  const [konu, setKonu] = useState<string>('');
  const [zorluk, setZorluk] = useState<string>('');
  const [search, setSearch] = useState<string>('');

  useEffect(() => {
    let url = '/api/practice-questions?limit=1000';
    if (kurul) url += `&kurul=${encodeURIComponent(kurul)}`;
    if (version) url += `&version=${encodeURIComponent(version)}`;
    if (zorluk) url += `&zorluk=${encodeURIComponent(zorluk)}`;

    const cacheKey = `medsoru_practice_pool_cache_${kurul}_${version}_${zorluk}`;

    safeJsonFetch<{ sorular: PQ[]; toplam: number }>(url).then((r) => {
      if (r.ok && r.data) {
        setAll(r.data.sorular || []);
        setTotalCount(r.data.toplam || (r.data.sorular || []).length);
        setError(null);
        try {
          sessionStorage.setItem(cacheKey, JSON.stringify(r.data));
        } catch (_) {}
      } else {
        // Çevrimdışıyken veya hata anında yerel oturum önbelleğine bak
        try {
          const cached = sessionStorage.getItem(cacheKey);
          if (cached) {
            const data = JSON.parse(cached);
            if (data.sorular && data.sorular.length > 0) {
              setAll(data.sorular);
              setTotalCount(data.toplam || data.sorular.length);
              setError(null);
              return;
            }
          }
        } catch (_) {}
        setError('Örnek sorular alınamadı. İnternet bağlantınızı kontrol edip tekrar deneyin.');
      }
    });
  }, [kurul, version, zorluk]);

  const opts = useMemo(() => {
    const list = all || [];
    const kurullar = Array.from(new Set(list.map((q) => q.kurul))).filter(Boolean).sort((a, b) => a - b);
    const versions = Array.from(new Set(list.map((q) => q.version))).filter(Boolean);
    const dersler = Array.from(new Set(list.map((q) => q.ders))).filter(Boolean);
    const konular = Array.from(new Set(list.filter((q) => !ders || q.ders === ders).map((q) => q.konu))).filter(Boolean);
    return { kurullar, versions, dersler, konular };
  }, [all, ders]);

  const shown = useMemo(() => {
    if (odak) return (all || []).filter((q) => String(q.id) === odak);
    return (all || []).filter((q) => {
      if (ders && q.ders !== ders) return false;
      if (konu && q.konu !== konu) return false;
      if (search.trim()) {
        const s = search.toLowerCase();
        const text = `${q.soru_koku || q.soru || ''} ${q.ders} ${q.konu}`.toLowerCase();
        if (!text.includes(s)) return false;
      }
      return true;
    });
  }, [all, ders, konu, search, odak]);

  const groups = useMemo(() => {
    const m = new Map<string, PQ[]>();
    for (const q of shown) {
      const key = `${q.ders} · ${q.konu}`;
      m.set(key, [...(m.get(key) || []), q]);
    }
    return Array.from(m.entries());
  }, [shown]);

  const [aboutQuestion, setAboutQuestion] = useState<PQ | null>(null);

  const sel = 'h-11 px-3 rounded-xl border border-line bg-white text-base text-ink min-w-0';

  return (
    <div className="flex flex-col gap-4">
      <div className="rounded-xl bg-accent-soft text-ink px-3.5 py-2.5 text-sm flex items-center justify-between gap-2">
        <span className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-accent shrink-0" />
          <span><b>Supabase Havuzu:</b> Toplam <b>{totalCount.toLocaleString('tr-TR')}</b> soru yerel veritabanında aktif.</span>
        </span>
        <span className="text-xs font-mono text-ink-3">Gösterilen: {shown.length} soru</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2" role="group" aria-label="Filtreler">
        <select className={sel} value={version} onChange={(e) => setVersion(e.target.value)}>
          <option value="">Tüm Sürümler (v1, v5_muse, v6...)</option>
          {opts.versions.map((v) => <option key={v} value={v}>{v}</option>)}
        </select>
        <select className={sel} value={ders} onChange={(e) => { setDers(e.target.value); setKonu(''); }}>
          <option value="">Tüm Dersler</option>
          {opts.dersler.map((d) => <option key={d} value={d}>{d}</option>)}
        </select>
        <select className={sel} value={konu} onChange={(e) => setKonu(e.target.value)}>
          <option value="">Tüm Konular</option>
          {opts.konular.map((k) => <option key={k} value={k}>{k}</option>)}
        </select>
        <select className={sel} value={zorluk} onChange={(e) => setZorluk(e.target.value)}>
          <option value="">Tüm Zorluklar</option>
          <option value="kolay">Kolay</option>
          <option value="orta">Orta</option>
          <option value="zor">Zor</option>
        </select>
      </div>

      <div className="relative">
        <Search className="w-4 h-4 text-ink-3 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
        <input
          type="search"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Soru metni veya kavram ara..."
          className="w-full h-11 pl-9 pr-3 rounded-xl bg-white border border-line text-base text-ink placeholder:text-ink-3 outline-none focus:border-accent"
        />
      </div>

      {odak && all !== null && (
        <div className="flex items-center justify-between gap-2 text-sm text-ink-3">
          <span>{shown.length ? 'Paylaşılan soru gösteriliyor.' : 'Paylaşılan soru bulunamadı; kaldırılmış olabilir.'}</span>
          <button type="button" onClick={() => { setOdak(null); try { window.history.replaceState(window.history.state, '', pathFor('ornek_sorular')); } catch { /* yoksay */ } }} className="ms-btn is-ghost is-sm">Tüm sorular</button>
        </div>
      )}

      {error ? (
        <p className="m-0 text-base text-bad-text">{error}</p>
      ) : all === null ? (
        <p className="m-0 text-base text-ink-3">Sorular yükleniyor…</p>
      ) : shown.length === 0 ? (
        <div className="rounded-2xl border border-line bg-white p-8 text-center text-ink-3 text-base flex flex-col items-center gap-2">
          <Filter className="w-6 h-6" />
          <span>Filtreye uyan soru bulunamadı.</span>
        </div>
      ) : (
        groups.map(([title, qs]) => (
          <section key={title} className="flex flex-col gap-3">
            <h2 className="m-0 text-sm font-semibold uppercase tracking-wide text-ink-3">{title} · {qs.length} soru</h2>
            {qs.map((q, i) => (
              <QuestionCard key={q.id} q={q} n={i + 1} onOpenAbout={(selQ) => setAboutQuestion(selQ)} />
            ))}
          </section>
        ))
      )}

      {aboutQuestion && (
        <QuestionAboutDialog
          questionId={aboutQuestion.id}
          title={`Örnek Soru · ${aboutQuestion.ders}`}
          subtitle={aboutQuestion.konu}
          facts={[
            { label: 'Kurul', value: `Kurul ${aboutQuestion.kurul}` },
            { label: 'Ders', value: aboutQuestion.ders },
            { label: 'Konu', value: aboutQuestion.konu, wide: true },
            { label: 'Soru ID', value: aboutQuestion.id, mono: true },
            ...(aboutQuestion.kazanim_no ? [{ label: 'Kazanım', value: `K${aboutQuestion.kazanim_no}`, mono: true }] : []),
            ...(aboutQuestion.zorluk ? [{ label: 'Zorluk', value: aboutQuestion.zorluk.toUpperCase() }] : []),
            { label: 'Doğru Cevap', value: `${aboutQuestion.dogru_secenek || aboutQuestion.dogru || 'A'} Şıkkı`, mono: true },
            ...(aboutQuestion.kaynak?.ders_notu ? [{ label: 'Ders Notu', value: `${aboutQuestion.kaynak.ders_notu}${aboutQuestion.kaynak.sayfa ? ` (s. ${aboutQuestion.kaynak.sayfa})` : ''}`, wide: true }] : []),
          ]}
          explanation={
            aboutQuestion.aciklama_maddeleri && aboutQuestion.aciklama_maddeleri.length > 0
              ? aboutQuestion.aciklama_maddeleri.join('\n')
              : (aboutQuestion.aciklama || '')
          }
          evidence={aboutQuestion.kaynak?.alinti}
          evidenceTitle={aboutQuestion.kaynak?.ders_notu ? `${aboutQuestion.kaynak.ders_notu}${aboutQuestion.kaynak.sayfa ? ` · Sayfa ${aboutQuestion.kaynak.sayfa}` : ''}` : undefined}
          sikAnalizi={aboutQuestion.sik_aciklamalari}
          answerKey={aboutQuestion.dogru_secenek || aboutQuestion.dogru || 'A'}
          options={LETTERS.filter((l) => aboutQuestion.secenekler && aboutQuestion.secenekler[l]).map((l) => ({
            key: l,
            text: aboutQuestion.secenekler[l],
          }))}
          onClose={() => setAboutQuestion(null)}
        />
      )}
    </div>
  );
};

export default PracticeQuestionsView;

