import React, { useEffect, useMemo, useState } from 'react';
import { pathFor } from '../router';
import { copyQuestion } from '../utils/copyQuestion';
import { getVoterId } from '../utils/voterId';
import { disciplineClass, disciplineLabel } from '../utils/discipline';
import {
  Check,
  X,
  RotateCcw,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  History,
  Flag,
  Maximize2,
  Search,
  Trophy,
  ThumbsUp,
  ThumbsDown,
  MessageSquare,
  Copy,
  Share2,
  Info,
  Send,
} from 'lucide-react';
import { ReportQuestionModal } from './ReportQuestionModal';
import { QuestionAboutDialog } from './QuestionAboutDialog';
import { toast } from './ui/Toast';
import { ApiService, safeJsonFetch } from '../services/api';
import { contentReady, isContentChanged, onContentChanged } from '../services/contentLive';
import { useAppearance } from '../utils/appearance';
import '../styles/v12/secondary.css';

/**
 * Kurul 1 kazanım temelli örnek sorular (/ornek-sorular, varsayılan sekme).
 * Veri: src/data/ornek_sorular/k1/<ders-id>.json — `python -m v2 ornek-k1 build --export`
 * (ders paketi özeti + bilgi paketi + müfredat kazanımları; editör yazımı, doğrulayıcıdan geçmiş).
 * Ders → kazanım → sorular; her kazanımda en az bir kolay/orta/zor soru, her şık için açıklama.
 */
type Zorluk = 'kolay' | 'orta' | 'zor';
type Soru = {
  id: string;
  kazanim: number;
  zorluk: Zorluk;
  soru: string;
  secenekler: Record<string, string>;
  dogru: string;
  aciklama: string;
  sik_aciklamalari: Record<string, string>;
};
type Cikmis = { id: string; soru: string; secenekler: Record<string, string>; cevap?: string | null };
type Kazanim = { no: number; metin: string; sorular: Soru[]; ilgili_cikmis: Cikmis[] };
type Ders = {
  id: string; sira: number; ders: string; konu: string; ogretim_uyesi: string; tarih: string;
  kazanimlar: Kazanim[]; soru_sayisi: number;
};
type IndexRow = { id: string; sira: number; ders: string; konu: string; ogretim_uyesi: string; soru_sayisi: number; kazanim: number };

const indexModules = import.meta.glob('../data/ornek_sorular/k1/index.json', { eager: true, import: 'default' }) as Record<string, IndexRow[]>;
const loaders = import.meta.glob('../data/ornek_sorular/k1/k1-*.json', { import: 'default' }) as Record<string, () => Promise<Ders>>;
const INDEX: IndexRow[] = Object.values(indexModules)[0] || [];

const LETTERS = ['A', 'B', 'C', 'D', 'E'];
const SECIM_KEY = 'medsoru_ornek_k1_ders';
const CEVAP_KEY = 'medsoru_ornek_k1_cevap';

function readSecim(): string | null {
  try { return window.localStorage.getItem(SECIM_KEY); } catch { return null; }
}
function writeSecim(v: string | null) {
  try { v ? window.localStorage.setItem(SECIM_KEY, v) : window.localStorage.removeItem(SECIM_KEY); } catch { /* depolama kapalı */ }
}

/* Cevaplar (soru id → seçilen şık + doğru mu) tarayıcıda tutulur; ders listesindeki ilerleme buradan okunur. */
type Cevap = { s: string; ok: boolean };
let CEVAPLAR: Record<string, Cevap> = (() => {
  try { return JSON.parse(window.localStorage.getItem(CEVAP_KEY) || '{}') || {}; } catch { return {}; }
})();
const dinleyiciler = new Set<() => void>();
function setCevap(id: string, c: Cevap | null) {
  CEVAPLAR = { ...CEVAPLAR };
  if (c) CEVAPLAR[id] = c; else delete CEVAPLAR[id];
  try { window.localStorage.setItem(CEVAP_KEY, JSON.stringify(CEVAPLAR)); } catch { /* depolama kapalı */ }
  dinleyiciler.forEach((f) => f());
}
function useCevaplar() {
  const [, tik] = useState(0);
  useEffect(() => { const f = () => tik((n) => n + 1); dinleyiciler.add(f); return () => { dinleyiciler.delete(f); }; }, []);
  return CEVAPLAR;
}
function dersIlerleme(id: string, c: Record<string, Cevap>) {
  let n = 0, d = 0; const p = `${id.split('-').slice(0, 2).join('-')}-q`;
  for (const k in c) if (k.startsWith(p)) { n++; if (c[k].ok) d++; }
  return { n, d };
}

function BildirButonu({ q, ders }: { q: Soru; ders: string }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button type="button" onClick={() => setOpen(true)} title="Soruda hata ya da sorun bildir" aria-label="Hata bildir" className="qk-ib">
        <Flag aria-hidden />
      </button>
      {open && (
        <ReportQuestionModal
          question={{ stem: q.soru, correctAnswer: q.dogru, discipline: ders, questionNumber: q.id }}
          onClose={() => setOpen(false)}
          onSubmit={async (reason, details) => {
            await ApiService.reportOrnekQuestion(q.id, reason, [details, `Kaynak: Örnek sorular · ${ders} · K${q.kazanim}`].filter(Boolean).join('\n'));
          }}
        />
      )}
    </>
  );
}

type SoruComment = { id: string; author: string; text: string; timestamp: string };
type SoruSocial = {
  upvotes: number;
  downvotes: number;
  liked: boolean;
  disliked: boolean;
  comments: SoruComment[];
};

const SOCIAL_KEY = 'medsoru_ornek_k1_social';
let SOCIAL_STORE: Record<string, SoruSocial> = (() => {
  try { return JSON.parse(window.localStorage.getItem(SOCIAL_KEY) || '{}') || {}; } catch { return {}; }
})();
const socialListeners = new Set<() => void>();

function notifySocial() {
  try { window.localStorage.setItem(SOCIAL_KEY, JSON.stringify(SOCIAL_STORE)); } catch {}
  socialListeners.forEach((fn) => fn());
}

function useSoruSocial(id: string): [SoruSocial, { toggleLike: () => void; toggleDislike: () => void; addComment: (text: string, author?: string) => void }] {
  const [, setTick] = useState(0);
  useEffect(() => {
    const fn = () => setTick((t) => t + 1);
    socialListeners.add(fn);
    return () => { socialListeners.delete(fn); };
  }, []);

  const current: SoruSocial = SOCIAL_STORE[id] || { upvotes: 0, downvotes: 0, liked: false, disliked: false, comments: [] };

  const actions = useMemo(() => ({
    toggleLike: () => {
      const prev = SOCIAL_STORE[id] || { upvotes: 0, downvotes: 0, liked: false, disliked: false, comments: [] };
      const isLiked = prev.liked;
      const isDisliked = prev.disliked;
      const newLiked = !isLiked;
      const newDisliked = isLiked ? isDisliked : false;
      const newUp = isLiked ? Math.max(0, prev.upvotes - 1) : prev.upvotes + 1;
      const newDown = isDisliked ? Math.max(0, prev.downvotes - 1) : prev.downvotes;
      SOCIAL_STORE = {
        ...SOCIAL_STORE,
        [id]: { ...prev, liked: newLiked, disliked: newDisliked, upvotes: newUp, downvotes: newDown }
      };
      notifySocial();
      try { ApiService.upvotePastQuestion(id, getVoterId()); } catch {}
    },
    toggleDislike: () => {
      const prev = SOCIAL_STORE[id] || { upvotes: 0, downvotes: 0, liked: false, disliked: false, comments: [] };
      const isDisliked = prev.disliked;
      const isLiked = prev.liked;
      const newDisliked = !isDisliked;
      const newLiked = isDisliked ? isLiked : false;
      const newDown = isDisliked ? Math.max(0, prev.downvotes - 1) : prev.downvotes + 1;
      const newUp = isLiked ? Math.max(0, prev.upvotes - 1) : prev.upvotes;
      SOCIAL_STORE = {
        ...SOCIAL_STORE,
        [id]: { ...prev, liked: newLiked, disliked: newDisliked, upvotes: newUp, downvotes: newDown }
      };
      notifySocial();
      try { ApiService.downvotePastQuestion(id, getVoterId()); } catch {}
    },
    addComment: (text: string, author: string = 'Tıp Öğrencisi') => {
      if (!text.trim()) return;
      const prev = SOCIAL_STORE[id] || { upvotes: 0, downvotes: 0, liked: false, disliked: false, comments: [] };
      const newComment: SoruComment = {
        id: `c_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
        author: author.trim() || 'Tıp Öğrencisi',
        text: text.trim(),
        timestamp: new Date().toISOString(),
      };
      SOCIAL_STORE = {
        ...SOCIAL_STORE,
        [id]: { ...prev, comments: [...(prev.comments || []), newComment] }
      };
      notifySocial();
      ApiService.commentPastQuestion(id, author, text.trim()).catch((e) => console.warn('[yorum] gönderilemedi:', e?.message));
    }
  }), [id]);

  return [current, actions];
}

function SoruKarti({
  q,
  n,
  ders,
  konu,
  buyuk = false,
  onOpenAbout,
}: {
  q: Soru;
  n: number;
  ders: string;
  konu?: string;
  buyuk?: boolean;
  onOpenAbout?: (q: Soru) => void;
}) {
  const cevaplar = useCevaplar();
  const picked = cevaplar[q.id]?.s ?? null;
  const done = picked !== null;
  const correct = picked === q.dogru;
  const pick = (k: string) => { if (!done) setCevap(q.id, { s: k, ok: k === q.dogru }); };
  const reset = () => setCevap(q.id, null);

  const [social, socialActions] = useSoruSocial(q.id);
  const [showComments, setShowComments] = useState(false);
  const [commentText, setCommentText] = useState('');
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    void copyQuestion(q.soru, LETTERS.filter((k) => q.secenekler[k]).map((k) => ({ key: k, text: q.secenekler[k] })));
    setCopied(true);
    toast.success('Soru kopyalandı', 'Soru metni ve şıklar panoya kopyalandı.');
    setTimeout(() => setCopied(false), 2000);
  };

  const handleShare = async () => {
    const url = `${window.location.origin}${pathFor('ornek_sorular', q.id)}`;
    const title = `Örnek Soru · ${ders} · K${q.kazanim}`;
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

  const ZORLUK_FLAG: Record<Zorluk, string> = { kolay: 'is-ok', orta: '', zor: 'is-warn' };
  const why = LETTERS.filter((k) => q.secenekler[k] && q.sik_aciklamalari[k]);

  return (
    <article data-auto-reveal className={`qk is-ornek ${buyuk ? 'is-big' : ''}`}>
      <header className="qk-h">
        <span className="qk-chip" title={`Kazanım ${q.kazanim}`}>K{q.kazanim}</span>
        <span className="qk-kunye">{`#${n}`}</span>
        {konu && <span className="qk-ders" title={konu}>{konu}</span>}
        <span className="qk-flags"><span className={`cx-flag ${ZORLUK_FLAG[q.zorluk]}`}>{q.zorluk}</span></span>
        {done && <span className="qk-flags"><span className={`cx-flag ${correct ? 'is-ok' : 'is-bad'}`}>{correct ? 'Doğru' : 'Yanlış'}</span></span>}
        <span className="qk-sp" />
        {onOpenAbout && (
          <button type="button" onClick={() => onOpenAbout(q)} className="qk-ib" aria-label="Soru hakkında" title="Soru hakkında"><Info aria-hidden /></button>
        )}
        <button type="button" onClick={handleCopy} className={`qk-ib ${copied ? 'is-done' : ''}`} aria-label={copied ? 'Kopyalandı' : 'Soru kökünü ve şıkları kopyala'} title={copied ? 'Kopyalandı' : 'Soru kökünü ve şıkları kopyala'}>
          {copied ? <Check aria-hidden /> : <Copy aria-hidden />}
        </button>
        <BildirButonu q={q} ders={ders} />
      </header>
      <div className={`qk-stem whitespace-pre-line ${buyuk ? 'is-lead' : ''}`}>{q.soru}</div>
      <ol className="qk-opts" aria-label="Şıklar">
        {LETTERS.filter((k) => q.secenekler[k]).map((k) => {
          const isRight = k === q.dogru;
          const isPicked = k === picked;
          const st = !done ? '' : isRight ? 'is-correct' : isPicked ? 'is-wrong' : 'is-dim';
          return (
            <li key={k} className="qk-opt-li">
              <button type="button" disabled={done} onClick={() => !done && pick(k)} className={`qk-opt ${st}`} aria-pressed={isPicked}>
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
            <b>{correct ? 'Doğru' : `Yanlış · doğru cevap ${q.dogru}`}</b>
            <span className="qk-sp" />
            <button type="button" onClick={reset}><RotateCcw aria-hidden /> Tekrar çöz</button>
          </p>
          <div className="qk-discs">
            <div className="qk-disc is-open">
              <div className="qk-disc-h is-static"><Info aria-hidden /><span>Açıklama ve şık analizi</span>{why.length > 0 && <span className="qk-disc-badge">{why.length} şık</span>}</div>
              <div className="qk-disc-b"><div className="qk-disc-in">
                {q.aciklama && <p className="m-0 text-[14px] leading-relaxed text-ink">{q.aciklama}</p>}
                {why.length > 0 && (
                  <dl className="qk-analysis">
                    {why.map((k) => (
                      <div key={k} className={k === q.dogru ? 'is-correct' : ''}><dt>{k}</dt><dd>{q.sik_aciklamalari[k]}</dd></div>
                    ))}
                  </dl>
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

function CikmisListesi({ items }: { items: Cikmis[] }) {
  const [open, setOpen] = useState(false);
  if (!items.length) return null;
  return (
    <div className="rounded-xl border border-line-soft bg-field">
      <button type="button" onClick={() => setOpen((o) => !o)} aria-expanded={open}
        className="w-full min-h-10 px-3 flex items-center gap-2 text-sm font-semibold text-ink-2 cursor-pointer">
        <History className="w-4 h-4" /> Bu kazanımla ilişkili çıkmış sorular ({items.length})
        <ChevronDown className={`w-4 h-4 ml-auto transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <ul className="m-0 px-3 pb-3 flex flex-col gap-2 list-none">
          {items.map((c) => (
            <li key={c.id} className="text-base text-ink-2 leading-relaxed border-t border-line-soft pt-2">
              <p className="m-0 text-ink">{c.soru}</p>
              {Object.keys(c.secenekler || {}).length > 0 && (
                <p className="m-0 mt-1 text-sm">
                  {Object.entries(c.secenekler).map(([k, v]) => (
                    <span key={k} className={`mr-3 ${c.cevap === k ? 'font-semibold text-ok' : ''}`}>{k}) {v}</span>
                  ))}
                </p>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

/** Tam ekran çözüm: tek soru, ilerleme çubuğu, klavye (A–E, ←/→, Esc), sonunda özet. */
function TamEkran({
  sorular,
  ders,
  konu,
  baslik,
  onClose,
  onOpenAbout,
}: {
  sorular: Soru[];
  ders: string;
  konu?: string;
  baslik: string;
  onClose: () => void;
  onOpenAbout?: (q: Soru) => void;
}) {
  const cevaplar = useCevaplar();
  const ilk = Math.max(0, sorular.findIndex((q) => !cevaplar[q.id]));
  const [i, setI] = useState(ilk);
  const ozet = i >= sorular.length;
  const q = sorular[Math.min(i, sorular.length - 1)];
  const cozulen = sorular.filter((x) => cevaplar[x.id]).length;
  const dogru = sorular.filter((x) => cevaplar[x.id]?.ok).length;

  useEffect(() => {
    const prev = document.body.style.overflow; document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = prev; };
  }, []);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (document.querySelector('[role="dialog"][aria-modal="true"]:not([data-tam-ekran])')) return;
      if (e.target instanceof HTMLElement && /INPUT|TEXTAREA/.test(e.target.tagName)) return;
      if (e.key === 'Escape') onClose();
      else if (e.key === 'ArrowRight') setI((n) => Math.min(sorular.length, n + 1));
      else if (e.key === 'ArrowLeft') setI((n) => Math.max(0, n - 1));
      else if (!ozet && q) {
        const k = e.key.toUpperCase();
        if (q.secenekler[k] && !CEVAPLAR[q.id]) setCevap(q.id, { s: k, ok: k === q.dogru });
      }
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [q, ozet, sorular.length, onClose]);

  const yanlislar = sorular.filter((x) => cevaplar[x.id] && !cevaplar[x.id].ok);
  return (
    <div role="dialog" aria-modal="true" data-tam-ekran aria-label="Tam ekran çözüm" className="fixed inset-0 z-50 bg-canvas flex flex-col">
      <div className="shrink-0 border-b border-line bg-white">
        <div className="max-w-5xl mx-auto px-4 h-14 flex items-center gap-3">
          <button type="button" onClick={onClose} aria-label="Tam ekrandan çık" className="h-9 w-9 -ml-2 rounded-lg inline-flex items-center justify-center text-ink-2 hover:bg-canvas cursor-pointer"><X className="w-5 h-5" /></button>
          <span className="min-w-0 truncate text-base font-semibold text-ink">{baslik}</span>
          <span className="ml-auto shrink-0 font-mono text-sm text-ink-2">{ozet ? 'Özet' : `${i + 1} / ${sorular.length}`}</span>
        </div>
        <div className="h-1 bg-line-soft"><div className="h-full bg-accent transition-all" style={{ width: `${(cozulen / sorular.length) * 100}%` }} /></div>
      </div>
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-5xl mx-auto px-4 py-5 sm:py-8">
          {ozet ? (
            <div className="bg-white border border-line rounded-2xl p-6 flex flex-col gap-4 text-center items-center">
              <Trophy className="w-10 h-10 text-accent" />
              <h3 className="m-0 text-2xl font-bold text-ink">Bitti!</h3>
              <p className="m-0 text-md text-ink-2">{cozulen} sorudan <b className="text-ok">{dogru}</b> doğru{cozulen ? ` · %${Math.round((dogru / cozulen) * 100)}` : ''}</p>
              {cozulen < sorular.length && <p className="m-0 text-sm text-ink-3">{sorular.length - cozulen} soru boş bırakıldı.</p>}
              <div className="flex flex-wrap gap-2 justify-center">
                {yanlislar.length > 0 && (
                  <button type="button" onClick={() => setI(sorular.indexOf(yanlislar[0]))} className="h-10 px-4 rounded-xl border border-line bg-white text-base font-semibold text-ink cursor-pointer hover:bg-canvas">Yanlışlara dön ({yanlislar.length})</button>
                )}
                <button type="button" onClick={() => { sorular.forEach((x) => setCevap(x.id, null)); setI(0); }} className="h-10 px-4 rounded-xl border border-line bg-white text-base font-semibold text-ink cursor-pointer hover:bg-canvas inline-flex items-center gap-1.5"><RotateCcw className="w-4 h-4" /> Baştan çöz</button>
                <button type="button" onClick={onClose} className="h-10 px-4 rounded-xl bg-ink text-white text-base font-semibold cursor-pointer">Kapat</button>
              </div>
            </div>
          ) : (
            <SoruKarti
              key={q.id}
              q={q}
              n={i + 1}
              ders={ders}
              konu={konu}
              buyuk
              onOpenAbout={onOpenAbout}
            />
          )}
          <p className="hidden sm:block m-0 mt-4 text-center text-xs text-ink-3">Klavye: A–E şık seçer · ← → sorular arasında gezer · Esc çıkar</p>
        </div>
      </div>
      <div className="shrink-0 border-t border-line bg-white">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center gap-2">
          <button type="button" disabled={i === 0} onClick={() => setI((n) => Math.max(0, n - 1))}
            className="h-11 px-4 rounded-xl border border-line bg-white text-base font-semibold text-ink-2 inline-flex items-center gap-1 cursor-pointer disabled:opacity-40 disabled:cursor-default"><ChevronLeft className="w-4 h-4" /> Önceki</button>
          <span className="mx-auto text-sm text-ink-3 font-mono">{dogru}/{cozulen} doğru</span>
          {!ozet && (
            <button type="button" onClick={() => setI((n) => n + 1)}
              className={`h-11 px-5 rounded-xl text-base font-semibold inline-flex items-center gap-1 cursor-pointer ${cevaplar[q.id] ? 'bg-ink text-white' : 'border border-line bg-white text-ink-2'}`}>
              {i === sorular.length - 1 ? 'Bitir' : cevaplar[q.id] ? 'Sonraki' : 'Atla'} <ChevronRight className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

function DersGorunumu({ id, initialKazanimNo, initialQuestionId, onBack }: { id: string; initialKazanimNo?: number; initialQuestionId?: string; onBack: () => void }) {
  const [ders, setDers] = useState<Ders | null>(null);
  const [hata, setHata] = useState(false);
  const [zorluk, setZorluk] = useState<Zorluk | ''>('');
  const [aboutQuestion, setAboutQuestion] = useState<{ q: Soru; ders: string; konu: string } | null>(null);
  const [tam, setTam] = useState<{ sorular: Soru[]; baslik: string } | null>(null);
  const cevaplar = useCevaplar();
  const v12 = useAppearance().design === 'v12';
  // Kazanım grupları akordiyon; "Tüm soruları göster" sağda o kazanımın soru listesini açar.
  const [acik, setAcik] = useState<Set<number>>(() => new Set(initialKazanimNo ? [initialKazanimNo] : []));
  const [panelK, setPanelK] = useState<number | null>(null);
  const toggleK = (no: number) => setAcik((s) => { const n = new Set(s); n.has(no) ? n.delete(no) : n.add(no); return n; });
  const gitSoru = (k: number, qid: string) => {
    setAcik((s) => new Set(s).add(k));
    window.setTimeout(() => document.getElementById(`os-${qid}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' }), 120);
  };

  // Panelden bu dersin soruları değişince (canlı içerik) yeniden yüklenir
  const [canli, setCanli] = useState(0);
  useEffect(() => onContentChanged('ornek', (ids) => { if (!ids.length || isContentChanged('ornek', `k1/${id}`)) setCanli((n) => n + 1); }), [id]);

  useEffect(() => {
    const load = loaders[`../data/ornek_sorular/k1/${id}.json`];
    if (!load) { setHata(true); return; }
    if (!canli) setDers(null);
    (async (): Promise<Ders> => {
      await contentReady();
      if (isContentChanged('ornek', `k1/${id}`)) {
        const r = await safeJsonFetch<Ders>(`/api/content/ornek/k1/${id}`, { cache: 'no-store' });
        if (r.ok && r.data?.kazanimlar) return r.data;
      }
      return load();
    })().then((data) => {
      setDers(data);
      // Derin bağlantı (/ornek-sorular/<soruId>): sorunun kazanımı açılır, soruya kayılır ve vurgulanır.
      // Canlı tazelemede kaydırma tekrarlanmaz
      const hedef = !canli && initialQuestionId ? data.kazanimlar.find((k) => k.sorular.some((q) => q.id === initialQuestionId)) : undefined;
      if (hedef && initialQuestionId) {
        setZorluk('');
        setAcik((s) => new Set(s).add(hedef.no));
        let n = 0;
        // Kartlar açılırken sayfa uzar ve kaydırma kesilebilir: soru görünür alana oturana dek yeniden dener.
        const odak = () => {
          const el = document.getElementById(`os-${initialQuestionId}`);
          if (!el) { if (++n < 12) window.setTimeout(odak, 150); return; }
          const r = el.getBoundingClientRect();
          if (r.top < 0 || r.top > window.innerHeight * 0.6) {
            el.scrollIntoView({ behavior: n < 2 ? 'smooth' : 'auto', block: 'center' });
            if (++n < 8) { window.setTimeout(odak, 450); return; }
          }
          if (!el.classList.contains('deep-link-highlight-pulse')) {
            el.classList.add('deep-link-highlight-pulse');
            window.setTimeout(() => el.classList.remove('deep-link-highlight-pulse'), 3200);
          }
        };
        window.setTimeout(odak, 120);
      } else if (initialKazanimNo && !canli) {
        setTimeout(() => {
          document.getElementById(`kz-${initialKazanimNo}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 120);
      }
    }).catch(() => setHata(true));
  }, [id, initialKazanimNo, initialQuestionId, canli]);

  if (hata) return <p className="m-0 text-base text-bad-text">Bu dersin soruları yüklenemedi. Sayfayı yenileyip tekrar deneyin.</p>;
  if (!ders) return <p className="m-0 text-base text-ink-3">Sorular yükleniyor…</p>;

  const tumu = ders.kazanimlar.flatMap((k) => k.sorular);
  const filtreli = tumu.filter((q) => !zorluk || q.zorluk === zorluk);
  const cozulen = tumu.filter((q) => cevaplar[q.id]).length;
  const dogru = tumu.filter((q) => cevaplar[q.id]?.ok).length;
  const yanlis = tumu.filter((q) => cevaplar[q.id] && !cevaplar[q.id].ok);
  let sayac = 0;

  const zSay = (z: Zorluk | '') => (z ? tumu.filter((q) => q.zorluk === z).length : tumu.length);
  const panel = panelK != null ? ders.kazanimlar.find((k) => k.no === panelK) || null : null;
  const panelSorular = panel ? panel.sorular.filter((q) => !zorluk || q.zorluk === zorluk) : [];

  return (
    <div className="os">
      <div className="os-top">
        <button type="button" onClick={onBack} className="os-back"><ChevronLeft aria-hidden /> Tüm dersler</button>
        <div className="os-title">
          <span className="os-eyebrow">Kurul 1 · {ders.sira}. ders · {ders.ders}</span>
          <h2>{ders.konu}</h2>
          <span className="os-meta">{ders.ogretim_uyesi} · {ders.kazanimlar.length} kazanım · {ders.soru_sayisi} soru</span>
        </div>
        <div className="os-progress">
          <span className="os-bar" aria-hidden><span style={{ width: `${(cozulen / Math.max(1, tumu.length)) * 100}%` }} /></span>
          <span className="os-num">{cozulen}/{tumu.length} · {dogru} doğru</span>
        </div>
        <div className="os-actions">
          <button type="button" onClick={() => setTam({ sorular: filtreli, baslik: ders.konu })} className="os-btn is-primary">
            <Maximize2 aria-hidden /> Tam ekran çöz{zorluk ? ` (${zorluk})` : ''}
          </button>
          {yanlis.length > 0 && (
            <button type="button" onClick={() => setTam({ sorular: yanlis, baslik: `${ders.konu} · yanlışlarım` })} className="os-btn">
              <RotateCcw aria-hidden /> Yanlışlarım ({yanlis.length})
            </button>
          )}
          {cozulen > 0 && <button type="button" onClick={() => tumu.forEach((q) => setCevap(q.id, null))} className="os-btn is-ghost">Sıfırla</button>}
        </div>
      </div>

      <div className="os-cats" data-autohide role="radiogroup" aria-label="Zorluk">
        <span className="os-cats-l">Zorluk</span>
        {(['', 'kolay', 'orta', 'zor'] as const).map((z) => (
          <button key={z || 'tum'} type="button" role="radio" aria-checked={zorluk === z} onClick={() => setZorluk(z)} className={`os-cat ${zorluk === z ? 'is-on' : ''}`}>
            {z ? z[0].toLocaleUpperCase('tr-TR') + z.slice(1) : 'Tümü'}<span>{zSay(z)}</span>
          </button>
        ))}
      </div>

      <div className={`os-body ${panel ? 'has-panel' : ''}`}>
        <div className="os-groups">
          {ders.kazanimlar.map((k) => {
            const qs = k.sorular.filter((q) => !zorluk || q.zorluk === zorluk);
            const kc = k.sorular.filter((q) => cevaplar[q.id]).length;
            const open = acik.has(k.no);
            const sel = panelK === k.no;
            const startN = sayac;
            sayac += qs.length;
            return (
              <section key={k.no} className={`os-g ${sel ? 'is-sel' : ''}`} id={`kz-${k.no}`} aria-labelledby={`kzb-${k.no}`}>
                <div className="os-gh">
                  <button type="button" className="os-gt" aria-expanded={open} onClick={() => toggleK(k.no)}>
                    <ChevronDown className={`os-chev ${open ? 'is-open' : ''}`} aria-hidden />
                    <span className="os-gk">K{k.no}</span>
                    <span className="os-gm">
                      <b id={`kzb-${k.no}`}>{k.metin}</b>
                      <span>{qs.length} soru · {kc} çözüldü</span>
                    </span>
                  </button>
                  <button type="button" className={`os-all ${sel ? 'is-on' : ''}`} aria-pressed={sel} onClick={() => setPanelK(sel ? null : k.no)}>
                    Tüm soruları göster <ChevronRight aria-hidden />
                  </button>
                </div>
                {open && (
                  <div className="os-gb">
                    {qs.map((q, i) => (
                      <div key={q.id} id={`os-${q.id}`}>
                        <SoruKarti
                          q={q}
                          n={startN + i + 1}
                          ders={ders.ders}
                          konu={undefined}
                          onOpenAbout={(selQ) => setAboutQuestion({ q: selQ, ders: ders.ders, konu: ders.konu })}
                        />
                      </div>
                    ))}
                    <CikmisListesi items={k.ilgili_cikmis} />
                  </div>
                )}
              </section>
            );
          })}
        </div>

        {panel && (
          <aside className="os-panel" aria-label={`K${panel.no} · tüm sorular`}>
            <div className="os-ph">
              <div className="min-w-0 flex-1">
                <span className="os-eyebrow">{v12 ? `Tüm sorular · K${panel.no}` : `TÜM SORULAR · K${panel.no}`}</span>
                <b>{panel.metin}</b>
                <span className="os-meta">{panelSorular.length} soru{zorluk ? ` · ${zorluk}` : ''}</span>
              </div>
              <button type="button" className="qk-ib" aria-label="Listeyi kapat" onClick={() => setPanelK(null)}><X aria-hidden /></button>
            </div>
            <ol className="os-pl">
              {panelSorular.map((q, i) => {
                const c = cevaplar[q.id];
                return (
                  <li key={q.id}>
                    <button type="button" onClick={() => gitSoru(panel.no, q.id)}>
                      <span className="os-pn">{i + 1}</span>
                      <span className="os-pt">{q.soru}</span>
                      <span className={`cx-flag ${c ? (c.ok ? 'is-ok' : 'is-bad') : q.zorluk === 'zor' ? 'is-warn' : q.zorluk === 'kolay' ? 'is-ok' : ''}`}>{c ? (c.ok ? 'Doğru' : 'Yanlış') : q.zorluk}</span>
                    </button>
                  </li>
                );
              })}
            </ol>
            <div className="os-pf">
              <button type="button" className="os-btn is-primary" onClick={() => setTam({ sorular: panelSorular, baslik: `K${panel.no} · ${panel.metin}` })}>
                {panelSorular.length} soruyla çalış
              </button>
            </div>
          </aside>
        )}
      </div>

      {tam && tam.sorular.length > 0 && (
        <TamEkran
          sorular={tam.sorular}
          ders={ders.ders}
          konu={ders.konu}
          baslik={tam.baslik}
          onClose={() => setTam(null)}
          onOpenAbout={(selQ) => setAboutQuestion({ q: selQ, ders: ders.ders, konu: ders.konu })}
        />
      )}

      {aboutQuestion && (
        <QuestionAboutDialog
          questionId={aboutQuestion.q.id}
          title={`Örnek Soru · ${aboutQuestion.ders}`}
          subtitle={aboutQuestion.konu}
          facts={[
            { label: 'Kurul', value: 'Kurul 1 (TIP 310)' },
            { label: 'Ders', value: aboutQuestion.ders },
            { label: 'Konu', value: aboutQuestion.konu, wide: true },
            { label: 'Soru ID', value: aboutQuestion.q.id, mono: true },
            { label: 'Kazanım', value: `K${aboutQuestion.q.kazanim}`, mono: true },
            { label: 'Zorluk', value: aboutQuestion.q.zorluk.toUpperCase() },
            { label: 'Doğru Cevap', value: `${aboutQuestion.q.dogru} Şıkkı`, mono: true },
            {
              label: 'Veri tabanına eklenme',
              value: ders.tarih
                ? new Date(ders.tarih).toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' })
                : undefined,
            },
            {
              label: 'Son düzenlenme',
              value: new Date('2026-10-09T08:30:00Z').toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' }),
            },
          ]}
          question={{
            id: aboutQuestion.q.id,
            kazanim: aboutQuestion.q.kazanim,
            zorluk: aboutQuestion.q.zorluk,
            ders: aboutQuestion.ders,
            konu: aboutQuestion.konu,
            soru: aboutQuestion.q.soru,
            secenekler: aboutQuestion.q.secenekler,
            dogru: aboutQuestion.q.dogru,
            aciklama: aboutQuestion.q.aciklama,
            sik_aciklamalari: aboutQuestion.q.sik_aciklamalari,
            kurul: 'Kurul 1 (TIP 310)',
            tarih: ders.tarih,
          }}
          explanation={aboutQuestion.q.aciklama}
          sikAnalizi={aboutQuestion.q.sik_aciklamalari}
          answerKey={aboutQuestion.q.dogru}
          options={LETTERS.filter((l) => aboutQuestion.q.secenekler[l]).map((l) => ({
            key: l,
            text: aboutQuestion.q.secenekler[l],
          }))}
          onClose={() => setAboutQuestion(null)}
        />
      )}
    </div>
  );
}

/** Soru kimliğinden dersi bulur: "k1-05-hucre-hasari-…-k03-q11" ve "k1-01-q01" biçimleri ("k1-NN" öneki). */
export const lessonIdForQuestion = (qid?: string | null): string | null => {
  if (!qid) return null;
  const direct = INDEX.find((x) => qid.startsWith(`${x.id}-`));
  if (direct) return direct.id;
  const m = /^(k\d+-\d+)-/.exec(qid);
  return (m && INDEX.find((x) => x.id.startsWith(`${m[1]}-`))?.id) || null;
};

export const KazanimSorulariView: React.FC<{
  initialLessonId?: string | null;
  initialKazanimNo?: number | null;
  initialQuestionId?: string | null;
}> = ({ initialLessonId: lessonProp, initialKazanimNo, initialQuestionId }) => {
  const initialLessonId = lessonProp || lessonIdForQuestion(initialQuestionId);
  const [secili, setSecili] = useState<string | null>(() => {
    if (initialLessonId && INDEX.some((x) => x.id === initialLessonId)) return initialLessonId;
    const s = readSecim();
    return s && INDEX.some((x) => x.id === s) ? s : null;
  });

  useEffect(() => {
    if (initialLessonId && INDEX.some((x) => x.id === initialLessonId)) {
      setSecili(initialLessonId);
      writeSecim(initialLessonId);
    }
  }, [initialLessonId]);

  const [brans, setBrans] = useState('');
  const [ara, setAra] = useState('');
  const cevaplar = useCevaplar();
  const branslar = useMemo(() => {
    const m = new Map<string, number>();
    INDEX.forEach((x) => m.set(x.ders, (m.get(x.ders) || 0) + 1));
    return Array.from(m.entries());
  }, []);
  const norm = (t: string) => t.toLocaleLowerCase('tr');
  const liste = INDEX.filter((x) => (!brans || x.ders === brans) && (!ara || norm(`${x.konu} ${x.ders} ${x.ogretim_uyesi}`).includes(norm(ara))));
  const toplamSoru = INDEX.reduce((a, x) => a + x.soru_sayisi, 0);
  const toplamCozulen = Object.keys(cevaplar).filter((k) => k.startsWith('k1-')).length;

  const sec = (id: string | null) => { setSecili(id); writeSecim(id); window.scrollTo({ top: 0 }); };

  if (secili) return <DersGorunumu id={secili} initialKazanimNo={initialKazanimNo || undefined} initialQuestionId={secili === initialLessonId ? initialQuestionId || undefined : undefined} onBack={() => sec(null)} />;

  if (!INDEX.length) {
    return <p className="m-0 rounded-2xl border border-line bg-white p-6 text-center text-base text-ink-3 o12-empty">Kurul 1 örnek soruları henüz hazırlanmadı.</p>;
  }

  return (
    <div className="flex flex-col gap-3 o12-ks">
      <div className="cx-dock">
        <label className="cx-search">
          <Search aria-hidden />
          <span className="sr-only">Ders ara</span>
          <input type="search" value={ara} onChange={(e) => setAra(e.target.value)} placeholder="Ders, konu veya öğretim üyesi ara" />
          {ara && <button type="button" className="cx-search-x" onClick={() => setAra('')} aria-label="Aramayı temizle"><X /></button>}
        </label>
        <div className="cx-rail">
          <nav className="cx-tabs" aria-label="Branş">
            {([['', INDEX.length], ...branslar] as [string, number][]).map(([b, c]) => (
              <button key={b || 'tum'} type="button" onClick={() => setBrans(b)} aria-pressed={brans === b} className={`cx-tab ${brans === b ? 'is-on' : ''}`}>
                {b || 'Tümü'}<small>{c}</small>
              </button>
            ))}
          </nav>
          <span className="cx-count ks-solved" title={`${toplamSoru.toLocaleString('tr-TR')} sorudan`}>{toplamCozulen.toLocaleString('tr-TR')} <small>çözdüğün</small></span>
        </div>
      </div>
      {liste.length === 0 && (
        <div className="ui-card flex flex-col items-center gap-2 text-center o12-empty" style={{ paddingBlock: 32 }}>
          <b>Aramanla eşleşen ders yok</b>
          <span className="ui-hint">Kelimeyi kısalt ya da branş süzgecini kaldır.</span>
          <button type="button" className="ui-btn is-tonal is-sm" onClick={() => { setAra(''); setBrans(''); }}>Temizle</button>
        </div>
      )}
      <ul className="ui-grid m-0 p-0 list-none o12-ks-list">
        {liste.map((x) => {
          const { n, d } = dersIlerleme(x.id, cevaplar);
          const yuzde = Math.min(100, Math.round((n / x.soru_sayisi) * 100));
          return (
            <li key={x.id} className={disciplineClass(x.ders)}>
              <button type="button" onClick={() => sec(x.id)} className="ks-lesson">
                <span className="ks-lesson-top">
                  <span className="hk-eyebrow"><i className="hk-dot" aria-hidden /><span>{disciplineLabel(x.ders) || x.ders}</span></span>
                  <span className="ks-lesson-no hk-num">{String(x.sira).padStart(2, '0')}</span>
                </span>
                <span className="ks-lesson-t">{x.konu}</span>
                <span className="ks-lesson-who">{x.ogretim_uyesi}</span>
                <span className="ks-lesson-bar" aria-hidden><span style={{ width: `${yuzde}%` }} /></span>
                <span className="ks-lesson-foot">
                  {n ? <><b className="hk-num">{n}/{x.soru_sayisi}</b> çözüldü · {d} doğru</> : <>{x.soru_sayisi} soru · {x.kazanim} kazanım</>}
                  <ChevronRight aria-hidden />
                </span>
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export const KAZANIM_INDEX = INDEX;
export default KazanimSorulariView;
