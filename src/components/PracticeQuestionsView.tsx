import React, { useEffect, useMemo, useState } from 'react';
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
} from 'lucide-react';
import { PageHeader } from './ui/PageHeader';
import { QuestionAboutDialog } from './QuestionAboutDialog';
import { toast } from './ui/Toast';
import { safeJsonFetch, ApiService } from '../services/api';
import { KazanimSorulariView, KAZANIM_INDEX } from './KazanimSorulariView';

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
      try { ApiService.upvotePastQuestion(id, 'anonim-std'); } catch {}
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
      try { ApiService.downvotePastQuestion(id, 'anonim-std'); } catch {}
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
      try { ApiService.commentPastQuestion(id, author, text.trim()); } catch {}
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

  const handleCopy = () => {
    const seceneklerText = LETTERS
      .filter((k) => q.secenekler && q.secenekler[k])
      .map((k) => `${k}) ${q.secenekler[k]}`)
      .join('\n');
    const fullText = `[Örnek Soru · Kurul ${q.kurul} · ${q.ders}${q.kazanim_no ? ` · K${q.kazanim_no}` : ''}]\n\n${soruMetni}\n\n${seceneklerText}\n\nDoğru Cevap: ${correctVal}${aciklamalar.length > 0 ? `\n\nAçıklama: ${aciklamalar.join('\n')}` : ''}`;
    navigator.clipboard.writeText(fullText);
    setCopied(true);
    toast.success('Soru kopyalandı', 'Soru metni ve şıklar panoya kopyalandı.');
    setTimeout(() => setCopied(false), 2000);
  };

  const handleShare = async () => {
    const url = `${window.location.origin}${window.location.pathname}?havuzId=${encodeURIComponent(q.id)}`;
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
    <article className="bg-white border border-line rounded-2xl p-4 sm:p-5 flex flex-col gap-3">
      <header className="flex flex-wrap items-center gap-2 text-[12.5px] text-ink-3">
        <span className="font-mono font-semibold text-ink">{n}.</span>
        <span>Kurul {q.kurul} · {q.ders}</span>
        {q.kazanim_no && <span className="font-mono text-[11px] bg-canvas px-1.5 py-0.5 rounded text-accent">K{q.kazanim_no}</span>}
        {q.zorluk && <span className="px-1.5 py-0.5 rounded bg-canvas text-ink-2 capitalize">{q.zorluk}</span>}
        {q.version && <span className="px-1.5 py-0.5 rounded bg-accent-soft text-accent text-[11px] font-mono">{q.version}</span>}
      </header>
      <p className="m-0 text-[16px] sm:text-[17px] font-medium text-ink leading-[1.5]">{soruMetni}</p>
      <ol className="list-none m-0 p-0 flex flex-col gap-1.5" aria-label="Şıklar">
        {LETTERS.filter((k) => q.secenekler && q.secenekler[k]).map((k) => {
          const isRight = k === correctVal;
          const isPicked = k === picked;
          const tone = !done
            ? 'bg-white border-line-soft hover:border-accent cursor-pointer'
            : isRight
            ? 'bg-ok-tint border-ok'
            : isPicked
            ? 'bg-bad-soft border-bad'
            : 'bg-white border-line-soft opacity-80';
          return (
            <li key={k}>
              <button
                type="button"
                disabled={done}
                onClick={() => setPicked(k)}
                className={`w-full min-h-11 grid grid-cols-[28px_minmax(0,1fr)_auto] items-center gap-2.5 px-3 py-2.5 rounded-xl border text-left ${tone}`}
                aria-pressed={isPicked}
              >
                <span className={`w-7 h-7 rounded-lg flex items-center justify-center font-mono text-[13px] font-semibold ${done && isRight ? 'bg-ok text-white' : 'bg-canvas text-ink-2'}`}>{k}</span>
                <span className="text-[14.5px] leading-[1.45] text-ink">{q.secenekler[k]}</span>
                {done && isRight ? <Check className="w-4 h-4 text-ok" /> : done && isPicked ? <X className="w-4 h-4 text-bad" /> : <span />}
              </button>
              {done && q.sik_aciklamalari && q.sik_aciklamalari[k] && (
                <p className={`m-0 px-3 py-1.5 pl-[48px] text-[13px] leading-relaxed ${isRight ? 'text-ok' : 'text-ink-2'}`}>
                  {q.sik_aciklamalari[k]}
                </p>
              )}
            </li>
          );
        })}
      </ol>
      {done && (
        <div className="flex flex-col gap-2.5">
          <p className={`m-0 text-[14px] font-semibold ${correct ? 'text-ok' : 'text-bad-text'}`}>
            {correct ? 'Doğru!' : `Yanlış — doğru cevap ${correctVal}`}
          </p>
          {aciklamalar.length > 0 && (
            <ul className="m-0 pl-5 flex flex-col gap-1 text-[14px] text-ink-2 leading-relaxed">
              {aciklamalar.map((m, i) => (
                <li key={i}>{m}</li>
              ))}
            </ul>
          )}
          {q.kaynak?.alinti && (
            <blockquote className="m-0 rounded-xl bg-field px-3 py-2.5 text-[13px] text-ink-2 flex flex-col gap-1">
              <span className="flex items-center gap-1.5 text-[12px] font-semibold text-ink-3">
                <BookOpen className="w-3.5 h-3.5" /> {q.kaynak.ders_notu}
                {q.kaynak.sayfa ? ` · sayfa ${q.kaynak.sayfa}` : ''}
              </span>
              <span className="italic">“{q.kaynak.alinti}”</span>
            </blockquote>
          )}
          <button type="button" onClick={() => setPicked(null)} className="self-start h-9 px-3 rounded-lg border border-line text-[13px] text-ink-2 inline-flex items-center gap-1.5 cursor-pointer hover:bg-canvas">
            <RotateCcw className="w-3.5 h-3.5" /> Tekrar çöz
          </button>
        </div>
      )}

      {/* Aksiyon Butonları (Like, Dislike, Yorum, Hakkında, Kopyala, Paylaş) */}
      <footer className="ms-qcard-foot pt-2 border-t border-line-soft">
        <button
          type="button"
          onClick={socialActions.toggleLike}
          aria-pressed={social.liked}
          title={social.liked ? 'Beğeniyi geri al' : 'Soruyu beğen'}
          className={`ms-btn is-sm ${social.liked ? 'is-on' : 'is-ghost'}`}
        >
          <ThumbsUp className={social.liked ? 'fill-current' : ''} /> {social.upvotes || 0}
        </button>
        <button
          type="button"
          onClick={socialActions.toggleDislike}
          aria-pressed={social.disliked}
          title={social.disliked ? 'Beğenmemeyi geri al' : 'Eksik ya da hatalı'}
          className={`ms-btn is-sm ${social.disliked ? 'is-danger bg-bad-soft!' : 'is-ghost'}`}
        >
          <ThumbsDown className={social.disliked ? 'fill-current' : ''} /> {social.downvotes || 0}
        </button>
        <button
          type="button"
          onClick={() => setShowComments((prev) => !prev)}
          aria-expanded={showComments}
          className={`ms-btn is-sm ${showComments ? 'is-on' : 'is-ghost'}`}
        >
          <MessageSquare /> {(social.comments || []).length > 0 ? `${social.comments.length} yorum` : 'Yorum'}
        </button>
        <span className="ms-qcard-foot-sep" aria-hidden />
        {onOpenAbout && (
          <button
            type="button"
            onClick={() => onOpenAbout(q)}
            className="ms-btn is-sm is-ghost is-icon text-ink-2 hover:text-ink"
            aria-label="Soru hakkında"
            title="Soru hakkında (künye, kazanım, kaynak not)"
          >
            <Info className="w-4 h-4" />
          </button>
        )}
        <button
          type="button"
          onClick={handleCopy}
          className={`ms-btn is-sm is-ghost is-icon ${copied ? 'text-ok!' : ''}`}
          aria-label={copied ? 'Soru kopyalandı' : 'Soruyu kopyala'}
          title={copied ? 'Kopyalandı' : 'Soruyu metin olarak kopyala'}
        >
          {copied ? <Check /> : <Copy />}
        </button>
        <button
          type="button"
          onClick={handleShare}
          className="ms-btn is-sm is-ghost is-icon"
          aria-label="Soruyu paylaş"
          title="Soru bağlantısını paylaş"
        >
          <Share2 />
        </button>
      </footer>

      {/* Yorumlar Paneli */}
      {showComments && (
        <div className="ms-pop-in bg-field rounded-xl p-2.5 flex flex-col gap-2">
          <div className="flex flex-col gap-1.5 max-h-56 overflow-y-auto">
            {(social.comments || []).length > 0 ? (
              social.comments.map((c) => (
                <div key={c.id} className="bg-white rounded-[10px] px-3 py-2 flex flex-col gap-0.5">
                  <div className="flex items-center justify-between gap-2 text-[12px] text-ink-3">
                    <span className="font-semibold text-ink">{c.author || 'Tıp Öğrencisi'}</span>
                    <span>{new Date(c.timestamp).toLocaleDateString('tr-TR')}</span>
                  </div>
                  <p className="m-0 text-[14px] text-ink-2 leading-relaxed">{c.text}</p>
                </div>
              ))
            ) : (
              <p className="m-0 px-1 text-[13.5px] text-ink-3">Henüz yorum yok. Bir ipucu ya da not ekleyen ilk kişi ol.</p>
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
              className="flex-1 min-w-0 h-10 bg-white border border-line rounded-full px-4 text-[15px] outline-0 focus:border-accent"
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
}> = ({ initialLessonId, initialKazanimNo }) => {
  const [sekme, setSekme] = useState<'k1' | 'havuz'>(() => {
    if (initialLessonId) return 'k1';
    try { return (window.localStorage.getItem(SEKME_KEY) as any) || 'k1'; } catch { return 'k1'; }
  });

  useEffect(() => {
    if (initialLessonId) {
      setSekme('k1');
    }
  }, [initialLessonId]);

  const sekmeSec = (v: 'k1' | 'havuz') => { 
    setSekme(v); 
    try { window.localStorage.setItem(SEKME_KEY, v); } catch { /* depolama kapalı */ } 
  };

  const k1Soru = KAZANIM_INDEX.reduce((a, x) => a + x.soru_sayisi, 0);
  const k1Kazanim = KAZANIM_INDEX.reduce((a, x) => a + x.kazanim, 0);
  const sekmeBtn = (v: 'k1' | 'havuz', label: string) => (
    <button type="button" role="tab" aria-selected={sekme === v} onClick={() => sekmeSec(v)}
      className={`h-10 px-3.5 rounded-lg text-[14px] font-medium cursor-pointer ${sekme === v ? 'bg-white text-ink shadow-sm' : 'text-ink-2 hover:text-ink'}`}>
      {label}
    </button>
  );

  return (
    <div className="flex flex-col gap-4 pb-16 w-full min-w-0">
      <PageHeader
        title="Örnek sorular"
        description="Kurul 1 derslerinin müfredat kazanımlarına göre hazırlanmış çalışma soruları. Her kazanımda kolay, orta ve zor sorular; cevapladıktan sonra her şıkkın neden doğru ya da yanlış olduğu gösterilir."
        stats={[
          { label: 'Kurul 1 Ders', value: String(KAZANIM_INDEX.length) },
          { label: 'Kazanım', value: k1Kazanim.toLocaleString('tr-TR') },
          { label: 'Kurul 1 Soru', value: k1Soru.toLocaleString('tr-TR') },
        ]}
      />
      <div role="tablist" aria-label="Soru kümesi" className="self-start flex gap-1 p-1 rounded-xl bg-field border border-line-soft">
        {sekmeBtn('k1', `Kurul 1 · Kazanım ve Ders Kataloğu (${k1Soru.toLocaleString('tr-TR')} Soru)`)}
        {sekmeBtn('havuz', 'Kurul 1 · Serbest Filtre & Arama')}
      </div>
      {sekme === 'k1' ? (
        <KazanimSorulariView
          initialLessonId={initialLessonId}
          initialKazanimNo={initialKazanimNo}
        />
      ) : (
        <TumHavuzUretim />
      )}
    </div>
  );
};

/** Supabase practice_questions tablosundan tüm soruları çeken ve filtreleyen görünüm */
const TumHavuzUretim: React.FC = () => {
  const [all, setAll] = useState<PQ[] | null>(null);

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

    safeJsonFetch<{ sorular: PQ[]; toplam: number }>(url).then((r) => {
      if (r.ok && r.data) {
        setAll(r.data.sorular || []);
        setTotalCount(r.data.toplam || (r.data.sorular || []).length);
      } else {
        setError('Örnek sorular alınamadı. Bağlantınızı kontrol edip sayfayı yenileyin.');
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
  }, [all, ders, konu, search]);

  const groups = useMemo(() => {
    const m = new Map<string, PQ[]>();
    for (const q of shown) {
      const key = `${q.ders} · ${q.konu}`;
      m.set(key, [...(m.get(key) || []), q]);
    }
    return Array.from(m.entries());
  }, [shown]);

  const [aboutQuestion, setAboutQuestion] = useState<PQ | null>(null);

  const sel = 'h-11 px-3 rounded-xl border border-line bg-white text-[14px] text-ink min-w-0';

  return (
    <div className="flex flex-col gap-4">
      <div className="rounded-xl bg-accent-soft text-ink px-3.5 py-2.5 text-[13px] flex items-center justify-between gap-2">
        <span className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-accent shrink-0" />
          <span><b>Supabase Havuzu:</b> Toplam <b>{totalCount.toLocaleString('tr-TR')}</b> soru yerel veritabanında aktif.</span>
        </span>
        <span className="text-[12px] font-mono text-ink-3">Gösterilen: {shown.length} soru</span>
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
          className="w-full h-11 pl-9 pr-3 rounded-xl bg-white border border-line text-[14px] text-ink placeholder:text-ink-3 outline-none focus:border-accent"
        />
      </div>

      {error ? (
        <p className="m-0 text-[14px] text-bad-text">{error}</p>
      ) : all === null ? (
        <p className="m-0 text-[14px] text-ink-3">Sorular yükleniyor…</p>
      ) : shown.length === 0 ? (
        <div className="rounded-2xl border border-line bg-white p-8 text-center text-ink-3 text-[14px] flex flex-col items-center gap-2">
          <Filter className="w-6 h-6" />
          <span>Filtreye uyan soru bulunamadı.</span>
        </div>
      ) : (
        groups.map(([title, qs]) => (
          <section key={title} className="flex flex-col gap-3">
            <h2 className="m-0 text-[13px] font-semibold uppercase tracking-wide text-ink-3">{title} · {qs.length} soru</h2>
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

