import React, { useLayoutEffect, useCallback, useEffect, useId, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { BookOpen, Check, Flag, History, Info, MessageSquare, Share2, Strikethrough, ThumbsDown, ThumbsUp, X } from 'lucide-react';
import { useAppearance } from '../../utils/appearance';
import { Highlight } from '../../components/ui/StemText';
import { SourceText } from '../../components/ui/SourceText';
import { ActionMenu, ActionItem } from '../../components/ui/ActionMenu';
import { CopyQuestionButton } from '../../components/ui/CopyQuestionButton';

/**
 * Çıkmış soru kartı.
 *
 * Anatomi:
 *  1. Künye satırı: ders etiketi · kurul çipi · mono künye (yıl · S-no) · işaretler · kopyala · bildir · ⋯
 *  2. Soru kökü (kartın tam genişliğinde)
 *  3. Şıklar — her şıkta kayan işlem çekmecesi: şıkka dokununca (ya da sola kaydırınca) şık sola itilir,
 *     sağdan "Değişiklik" (varsa) ve "İtiraz" eylemleri çıkar. Değişiklik ayrıntısı şıkkın altında açılır.
 *  4. Açılır paneller: "Açıklama ve şık analizi", "Değişiklik geçmişi" — alt çubuktaki ikonlarla açılıp kapanır.
 *  5. Alt çubuk: beğen · beğenme · yorum · | açıklama · geçmiş · paylaş
 */
export interface CikmisOption { key: string; text: string; isAiGenerated?: boolean }
export interface CikmisOptionInfo { title: string; before?: string; after?: string; note?: string }

export interface CikmisCardProps {
  id: string;
  anchorId: string;
  className?: string;
  kurul: string | null;
  kunye: string;
  ders: string;
  numberLabel: string;
  flags: React.ReactNode[];
  headExtra?: React.ReactNode;
  stem: React.ReactNode;
  kazanim?: { baslik: string; metin: string } | null;
  /** Anket, karşılaştırma ya da ham metin görünümü: varsa şık listesinin yerine geçer */
  special?: React.ReactNode;
  options: CikmisOption[];
  correctAnswer?: string;
  terms?: string[];
  quiz: { on: boolean; picked?: string; onPick: (k: string) => void; onReset: () => void };
  optionInfo?: (key: string) => CikmisOptionInfo | null;
  onObject: (key: string, text: string) => void;
  notes?: React.ReactNode;
  explanation?: string;
  analysis: [string, string][];
  refs: string[];
  history?: React.ReactNode;
  historyBadge?: string;
  copy: { stem: string; options: { key?: string; text?: string }[] };
  actions: ActionItem[];
  menuHighlight?: { icon: React.ElementType; title: string };
  social: {
    liked: boolean; disliked: boolean; up: number; down: number; comments: number; commentsOpen: boolean;
    onLike: () => void; onDislike: () => void; onComments: () => void; onShare: () => void;
  };
  onReport: () => void;
  comments?: React.ReactNode;
}

/** Derin bağlantı bu kartın bu bölümünü mü istiyor? (/cikmis/<id>?sec=explanation ya da #expl-<id>) */
const wantsSection = (qid: string, sec: string) => {
  if (typeof window === 'undefined') return false;
  const { pathname, search, hash } = window.location;
  const forThis = pathname.endsWith(`/${encodeURIComponent(qid)}`) || hash.includes(qid);
  return forThis && (new URLSearchParams(search).get('sec') === sec || (sec === 'explanation' && hash.startsWith(`#expl-${qid}`)));
};

/** Yükseklik canlandırmalı açılır bölüm (grid-template-rows 0fr → 1fr); kapalıyken içerik odak almaz ve ilk açılışa kadar DOM'a bağlanmaz. */
const Reveal: React.FC<{ open: boolean; id?: string; className?: string; children: React.ReactNode }> = ({ open, id, className = '', children }) => {
  const [mounted, setMounted] = useState(open);
  useEffect(() => {
    if (open && !mounted) setMounted(true);
  }, [open, mounted]);
  return (
    <div id={id} className={`qk-rev ${open ? 'is-open' : ''} ${className}`}>
      <div className="qk-rev-in" inert={!open ? true : undefined}>{mounted ? children : null}</div>
    </div>
  );
};

/**
 * Şık satırı — iki etkileşim (Çıkmış):
 *  1) ÇEK-BIRAK: şık yatayda çekilip bırakılınca "kalkar" (yüzen kart: büyür, kenarlardan taşar, gölge,
 *     solda kırmızı parıltı) ve sağında gömülü eylem kapsülü belirir (Bilgi · Bildir). Tekrar çek-bırak → iner.
 *     Çekerken şık parmağı dirençle izler; bırakınca yaylanarak yerine döner.
 *  2) TEK DOKUNUŞ: dokunulan noktada halka dalgası + üstünde oklu balon (Bilgi · Hata Bildir). Sınav kipinde
 *     dokunuş cevap seçer (balon açılmaz).
 */
const LIFT_AT = 28; // çek-bırak eşiği (px)

const OptRow: React.FC<{
  qid: string;
  k: string;
  cls: string;
  inner: React.ReactNode;
  pickable: boolean;
  onPick: () => void;
  lifted: boolean;
  setLifted: (v: boolean) => void;
  onTap: (x: number, y: number) => void;
  info: CikmisOptionInfo | null;
  canObject: boolean;
  onObject: () => void;
  onInfo: (info: CikmisOptionInfo) => void;
  /** v12: satırın sağında görünür hızlı düğmeler (şıkkı bildir; cevaplamadan önce şıkkı ele) */
  quick?: boolean;
  eliminated?: boolean;
  onEliminate?: () => void;
}> = ({ qid, k, cls, inner, pickable, onPick, lifted, setLifted, onTap, info, canObject, onObject, onInfo, quick, eliminated, onEliminate }) => {
  const [dx, setDx] = useState<number | null>(null);
  const start = useRef<{ x: number; y: number; locked: boolean | null } | null>(null);
  const moved = useRef(false);
  const hasActions = Boolean(info) || canObject;

  useEffect(() => {
    if (lifted) { try { navigator.vibrate?.(10); } catch { /* yok */ } }
  }, [lifted]);

  const onPointerDown = (e: React.PointerEvent) => {
    if (e.button !== 0) return;
    start.current = { x: e.clientX, y: e.clientY, locked: null };
    moved.current = false;
  };
  const onPointerMove = (e: React.PointerEvent) => {
    const s = start.current;
    if (!s || !hasActions) return;
    const mx = e.clientX - s.x;
    const my = e.clientY - s.y;
    if (s.locked === null && (Math.abs(mx) > 6 || Math.abs(my) > 6)) s.locked = Math.abs(mx) > Math.abs(my);
    if (!s.locked) return;
    moved.current = true;
    try { (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId); } catch { /* yoksay */ }
    // Dirençli izleme: ilk 28px doğrusal, sonrası karekök
    const sgn = Math.sign(mx);
    const a = Math.abs(mx);
    setDx(sgn * (a <= LIFT_AT ? a : LIFT_AT + Math.sqrt(a - LIFT_AT) * 4));
  };
  const onPointerUp = () => {
    start.current = null;
    if (dx !== null) {
      if (Math.abs(dx) >= LIFT_AT) setLifted(!lifted);
      setDx(null);
    }
    window.setTimeout(() => { moved.current = false; }, 0);
  };
  const onClick = (e: React.MouseEvent) => {
    if (moved.current) return;
    if (pickable) { onPick(); return; }
    if (lifted) { setLifted(false); return; }
    if (hasActions) onTap(e.clientX || (e.currentTarget as HTMLElement).getBoundingClientRect().right - 40, e.clientY || (e.currentTarget as HTMLElement).getBoundingClientRect().top + 20);
  };

  return (
    <li id={`opt-${qid}-${k}`} className={`qk-opt-li qk-lift ${lifted ? 'is-lifted' : ''} ${dx !== null ? 'is-drag' : ''} ${quick ? 'has-quick' : ''} ${eliminated ? 'is-elim' : ''}`}>
      <div className="qk-lift-row" style={dx !== null ? { transform: `translate3d(${dx}px,0,0)` } : undefined}>
        <button
          type="button"
          className={`${cls} qk-lift-front`}
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onPointerUp={onPointerUp}
          onPointerCancel={onPointerUp}
          onClick={onClick}
          aria-haspopup={hasActions && !pickable ? 'dialog' : undefined}
          aria-label={pickable ? `${k} şıkkını işaretle` : undefined}
        >
          {inner}
          {info && !lifted && <span className="qk-opt-dot" aria-hidden />}
        </button>
        {hasActions && (
          <div className="qk-lift-pill" role="group" aria-label={`${k} şıkkı işlemleri`} aria-hidden={!lifted}>
            {info && (
              <button type="button" tabIndex={lifted ? 0 : -1} className="qk-lp is-info" onClick={() => { setLifted(false); onInfo(info); }} aria-label="Bu şıkta yapılan değişiklik" title="Bu şıkta yapılan değişiklik">
                <Info aria-hidden />
              </button>
            )}
            {info && canObject && <i className="qk-lp-sep" aria-hidden />}
            {canObject && (
              <button type="button" tabIndex={lifted ? 0 : -1} className="qk-lp is-flag" onClick={() => { setLifted(false); onObject(); }}>
                <Flag aria-hidden /><span>Bildir</span>
              </button>
            )}
          </div>
        )}
      </div>
      {quick && !lifted && (pickable ? onEliminate : canObject) && (
        <span className="qk-oquick">
          {pickable && onEliminate ? (
            <button type="button" className={`qk-oq ${eliminated ? 'is-on' : ''}`} onClick={onEliminate} aria-pressed={eliminated} aria-label={eliminated ? `${k} şıkkını geri al` : `${k} şıkkını ele`} title={eliminated ? 'Geri al' : 'Bu şıkkı ele (üstünü çiz)'}>
              <Strikethrough aria-hidden />
            </button>
          ) : (
            <button type="button" className="qk-oq is-flag" onClick={onObject} aria-label={`${k} şıkkını bildir`} title="Bu şıkkı bildir">
              <Flag aria-hidden />
            </button>
          )}
        </span>
      )}
    </li>
  );
};

/** Tek dokunuş balonu: dokunma noktasında halka dalgası, üstünde oklu eylem balonu (ekranda kalacak şekilde konumlanır). */
const TapPopover: React.FC<{
  x: number; y: number; info: CikmisOptionInfo | null; canObject: boolean;
  onInfo: () => void; onObject: () => void; onClose: () => void;
}> = ({ x, y, info, canObject, onInfo, onObject, onClose }) => {
  const ref = useRef<HTMLDivElement>(null);
  // Konum boyamadan ÖNCE hesaplanır (useLayoutEffect): balon kendi doğal genişliğinde ölçülür (CSS width:max-content,
  // nowrap) ve ekranın 10px içine sığacak şekilde kaydırılır. Eskiden kenara yakın dokunuşta balon önce dokunma
  // noktasına çizilip daralıyor, "Hata Bildir" iki satıra kırılıyor ve ok balonun dışına taşıyordu.
  const [pos, setPos] = useState<{ left: number; below: boolean; ax: number; ready: boolean }>({ left: x, below: false, ax: 0, ready: false });
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    const w = el.offsetWidth;
    const h = el.offsetHeight;
    const vw = document.documentElement.clientWidth;
    const left = Math.min(vw - w / 2 - 10, Math.max(w / 2 + 10, x));
    const topSafe = 64; // üst çubuk
    const below = y - h - 22 < topSafe;
    const ax = Math.max(-(w / 2 - 20), Math.min(w / 2 - 20, x - left)); // ok balonun köşelerine taşmasın
    setPos({ left, below, ax, ready: true });
  }, [x, y]);
  useEffect(() => {
    const close = (e: Event) => {
      if (e.type === 'keydown' && (e as KeyboardEvent).key !== 'Escape') return;
      if (e.type === 'pointerdown' && ref.current?.contains(e.target as Node)) return;
      onClose();
    };
    const t = window.setTimeout(() => {
      document.addEventListener('pointerdown', close);
      window.addEventListener('scroll', close, { passive: true, once: true });
    }, 0);
    document.addEventListener('keydown', close);
    return () => {
      window.clearTimeout(t);
      document.removeEventListener('pointerdown', close);
      window.removeEventListener('scroll', close);
      document.removeEventListener('keydown', close);
    };
  }, [x, y, onClose]);
  return createPortal(
    <>
      <span className="qk-ripple" style={{ left: x, top: y }} aria-hidden><i /><i /></span>
      <div
        ref={ref}
        className={`qk-pop ${pos.below ? 'is-below' : ''}`}
        role="dialog"
        aria-label="Şık işlemleri"
        style={{ left: pos.left, top: pos.below ? y + 22 : y - 22, ['--ax' as string]: `${pos.ax}px`, visibility: pos.ready ? undefined : 'hidden' }}
      >
        {info && (
          <button type="button" className="qk-pop-info" onClick={() => { onClose(); onInfo(); }} aria-label="Bu şıkta yapılan değişiklik" title="Bu şıkta yapılan değişiklik">
            <Info aria-hidden />
          </button>
        )}
        {canObject && (
          <button type="button" className="qk-pop-flag" onClick={() => { onClose(); onObject(); }} autoFocus>
            <Flag aria-hidden /><span>Hata Bildir</span>
          </button>
        )}
      </div>
    </>,
    document.body
  );
};

/**
 * Şık değişikliği diyalog-toast'u: ekranın altından yaylanarak çıkar, önce/sonra karşılaştırmasını gösterir.
 * Esc, kapat düğmesi ya da dışarı dokunma kapatır; 12 sn sonra kendiliğinden çekilir (üzerindeyken beklemez).
 */
const InfoToast: React.FC<{ info: CikmisOptionInfo; onClose: () => void }> = ({ info, onClose }) => {
  const [leaving, setLeaving] = useState(false);
  const hover = useRef(false);
  const close = useCallback(() => { setLeaving(true); window.setTimeout(onClose, 220); }, [onClose]);
  useEffect(() => {
    const t = window.setInterval(() => { if (!hover.current) { window.clearInterval(t); close(); } }, 12000);
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape') close(); };
    document.addEventListener('keydown', esc);
    return () => { window.clearInterval(t); document.removeEventListener('keydown', esc); };
  }, [close]);
  return createPortal(
    <div className={`qk-toast-wrap ${leaving ? 'is-leaving' : ''}`} onPointerDown={(e) => { if (e.target === e.currentTarget) close(); }}>
      <div className="qk-toast" role="dialog" aria-label={info.title} onPointerEnter={() => { hover.current = true; }} onPointerLeave={() => { hover.current = false; }}>
        <span className="qk-toast-ic" aria-hidden><Info /></span>
        <div className="qk-toast-b">
          <b>{info.title}</b>
          {info.before !== undefined && <p className="is-before"><span>Önce</span>{info.before ? <del>{info.before}</del> : <i>(yoktu)</i>}</p>}
          {info.after !== undefined && <p className="is-after"><span>Sonra</span><ins>{info.after}</ins></p>}
          {info.note && <p className="is-note">{info.note}</p>}
        </div>
        <button type="button" className="qk-toast-x" onClick={close} aria-label="Kapat"><X aria-hidden /></button>
      </div>
    </div>,
    document.body
  );
};

export const CikmisCard: React.FC<CikmisCardProps> = (p) => {
  const v12 = useAppearance().design === 'v12';
  const [flagsOpen, setFlagsOpen] = useState(false);
  // Şık eleme (yalnız cevaplamadan önce, v12): üstü çizilen şıklar; yeniden denemede sıfırlanır
  const [elim, setElim] = useState<Set<string>>(() => new Set());
  useEffect(() => { if (!p.quiz.picked) return; setElim(new Set()); }, [p.quiz.picked]);
  const [liftedOpt, setLiftedOpt] = useState<string | null>(null);
  const [pop, setPop] = useState<{ key: string; x: number; y: number } | null>(null);
  const closePop = useCallback(() => setPop(null), []);
  const [infoToast, setInfoToast] = useState<CikmisOptionInfo | null>(null);
  const explWanted = useCallback(() => wantsSection(p.id, 'explanation'), [p.id]);
  const [panel, setPanel] = useState<'expl' | 'hist' | null>(() => (explWanted() ? 'expl' : null));
  const rootRef = useRef<HTMLElement>(null);
  const panelId = useId();

  const shownFlags = flagsOpen ? p.flags : p.flags.slice(0, 2);
  const hiddenCount = p.flags.length - shownFlags.length;
  const hideAnswer = p.quiz.on && !p.quiz.picked;
  const short = p.options.every((o) => String(o.text ?? '').length <= 42);
  const hasExplain = !hideAnswer && (Boolean(p.explanation?.trim()) || p.analysis.length > 0 || p.refs.length > 0);

  // Uygulama içi gezinmede (bildirim, paylaşım) adres açıklamayı isterse panel açılır.
  useEffect(() => {
    const on = () => { if (explWanted()) setPanel('expl'); };
    window.addEventListener('popstate', on);
    return () => window.removeEventListener('popstate', on);
  }, [explWanted]);

  // Kalkık şık: o şıkkın dışına dokununca ya da Esc ile iner.
  useEffect(() => {
    if (!liftedOpt) return;
    const close = (e: Event) => {
      const row = rootRef.current?.querySelector(`#opt-${CSS.escape(p.id)}-${CSS.escape(liftedOpt)}`);
      if (e instanceof KeyboardEvent ? e.key === 'Escape' : !row?.contains(e.target as Node)) setLiftedOpt(null);
    };
    document.addEventListener('pointerdown', close);
    document.addEventListener('keydown', close);
    return () => {
      document.removeEventListener('pointerdown', close);
      document.removeEventListener('keydown', close);
    };
  }, [liftedOpt, p.id]);

  const toggle = (k: 'expl' | 'hist') => setPanel((v) => (v === k ? null : k));

  return (
    <article ref={rootRef} id={p.anchorId} className={`qk ${p.className || ''}`}>
      <header className={`qk-h ${flagsOpen ? 'is-flags-open' : ''}`}>
        {p.ders && <span className="qk-ders" title={p.ders}><i className="hk-dot" aria-hidden /><span className="qk-ders-t">{p.ders}</span></span>}
        {p.kurul && <span className="qk-chip" title="Kurul">{p.kurul}</span>}
        <span className="qk-kunye">{p.kunye}</span>
        {shownFlags.length > 0 && <span className="qk-flags">{shownFlags.map((f, i) => <React.Fragment key={i}>{f}</React.Fragment>)}</span>}
        {hiddenCount > 0 && (
          <button type="button" className="qk-more-flags" onClick={() => setFlagsOpen(true)} aria-label={`${hiddenCount} işaret daha göster`}>+{hiddenCount}</button>
        )}
        <span className="qk-sp" />
        {p.headExtra}
        {!v12 && <CopyQuestionButton stem={p.copy.stem} options={p.copy.options} className="qk-ib" />}
        {!v12 && <button type="button" className="qk-ib" onClick={p.onReport} aria-label="Hata bildir" title="Hata bildir"><Flag aria-hidden /></button>}
        <ActionMenu items={p.actions} title={`Soru ${p.numberLabel}`} highlight={p.menuHighlight} />
      </header>

      <div className="qk-stem">{p.stem}</div>

      {p.kazanim && (
        <p className="qk-kaz"><b>{p.kazanim.baslik}</b>{p.kazanim.metin}</p>
      )}

      {p.special ?? (
        p.options.length > 0 && (
          <ol className={`qk-opts is-lift ${short ? 'is-short' : ''}`}>
            {p.options.map((o) => {
              const key = String(o.key);
              const isCorrect = key === p.correctAnswer;
              const showCorrect = isCorrect && !hideAnswer;
              const wrong = p.quiz.on && p.quiz.picked === key && !isCorrect;
              const dim = p.quiz.on && p.quiz.picked && !showCorrect && !wrong;
              const cls = `qk-opt ${showCorrect ? 'is-correct' : ''} ${wrong ? 'is-wrong' : ''} ${dim ? 'is-dim' : ''}`;
              const inner = (
                <>
                  <span className="qk-bub" aria-hidden>{showCorrect ? <Check strokeWidth={3} /> : wrong ? <X strokeWidth={3} /> : key}</span>
                  <span className="qk-opt-t"><Highlight text={String(o.text ?? '')} terms={p.terms} />{showCorrect && <span className="sr-only"> (doğru cevap)</span>}</span>
                </>
              );
              return (
                <OptRow
                  key={key}
                  qid={p.id}
                  k={key}
                  cls={cls}
                  inner={inner}
                  pickable={p.quiz.on && !p.quiz.picked}
                  onPick={() => p.quiz.onPick(key)}
                  lifted={liftedOpt === key}
                  setLifted={(v) => { setPop(null); setLiftedOpt(v ? key : null); }}
                  onTap={(x, y) => { setLiftedOpt(null); setPop({ key, x, y }); }}
                  info={hideAnswer ? null : p.optionInfo?.(key) ?? null}
                  canObject={!hideAnswer}
                  onObject={() => p.onObject(key, String(o.text ?? ''))}
                  onInfo={setInfoToast}
                  quick={v12}
                  eliminated={elim.has(key)}
                  onEliminate={p.quiz.on && !p.quiz.picked ? () => setElim((m) => { const n = new Set(m); if (n.has(key)) n.delete(key); else n.add(key); return n; }) : undefined}
                />
              );
            })}
          </ol>
        )
      )}

      {p.quiz.on && p.quiz.picked && !p.special && (
        <p className={`qk-verdict ${p.quiz.picked === p.correctAnswer ? 'is-ok' : 'is-bad'}`} role="status">
          <b>{p.quiz.picked === p.correctAnswer ? 'Doğru' : `Yanlış · cevap ${p.correctAnswer}`}</b>
          <button type="button" onClick={p.quiz.onReset}>Yeniden dene</button>
        </p>
      )}

      {p.notes}

      {hasExplain && (
        <Reveal open={panel === 'expl'} id={`expl-${p.id}`} className="qk-panel">
          <div className="qk-panel-in" id={`${panelId}-expl`}>
            <h4 className="qk-panel-h"><BookOpen aria-hidden />Açıklama ve şık analizi</h4>
            {p.explanation?.trim() && <SourceText text={p.explanation} size="sm" />}
            {p.analysis.length > 0 && (
              <dl className="qk-analysis">
                {p.analysis.map(([k, v]) => (
                  <div key={k} className={String(k).toUpperCase() === String(p.correctAnswer || '').toUpperCase() ? 'is-correct' : ''}>
                    <dt>{k}</dt>
                    <dd>{String(v)}</dd>
                  </div>
                ))}
              </dl>
            )}
            {p.refs.length > 0 && <p className="qk-refs"><b>Kaynak</b>{p.refs.join(' · ')}</p>}
          </div>
        </Reveal>
      )}
      {p.history && (
        <Reveal open={panel === 'hist'} className="qk-panel">
          <div className="qk-panel-in" id={`${panelId}-hist`}>
            <h4 className="qk-panel-h"><History aria-hidden />Değişiklik geçmişi{p.historyBadge && <small>{p.historyBadge}</small>}</h4>
            {p.history}
          </div>
        </Reveal>
      )}

      <footer className="qk-f">
        <button type="button" onClick={p.social.onLike} aria-pressed={p.social.liked} className={`qk-act ${p.social.liked ? 'is-on' : ''}`} title={p.social.liked ? 'Beğeniyi geri al' : 'Soruyu beğen'}>
          <ThumbsUp className={p.social.liked ? 'fill-current' : ''} aria-hidden /><span>{p.social.up}</span><span className="sr-only"> beğeni</span>
        </button>
        <button type="button" onClick={p.social.onDislike} aria-pressed={p.social.disliked} className={`qk-act ${p.social.disliked ? 'is-bad' : ''}`} title={p.social.disliked ? 'Beğenmemeyi geri al' : 'Eksik ya da hatalı'}>
          <ThumbsDown className={p.social.disliked ? 'fill-current' : ''} aria-hidden /><span>{p.social.down}</span><span className="sr-only"> beğenmeme</span>
        </button>
        <button type="button" onClick={p.social.onComments} aria-expanded={p.social.commentsOpen} className={`qk-act ${p.social.commentsOpen ? 'is-on' : ''}`} title="Yorumlar">
          <MessageSquare aria-hidden /><span>{p.social.comments}</span><span className="sr-only"> yorum</span>
        </button>
        <span className="qk-sp" />
        {hasExplain && (
          <button type="button" onClick={() => toggle('expl')} aria-expanded={panel === 'expl'} aria-controls={`${panelId}-expl`} className={`qk-act qk-pt ${panel === 'expl' ? 'is-on' : ''}`} title="Açıklama ve şık analizi">
            <BookOpen aria-hidden /><span className="qk-pt-l">Açıklama</span>
          </button>
        )}
        {p.history && (
          <button type="button" onClick={() => toggle('hist')} aria-expanded={panel === 'hist'} aria-controls={`${panelId}-hist`} className={`qk-act qk-pt ${panel === 'hist' ? 'is-on' : ''}`} title="Değişiklik geçmişi">
            <History aria-hidden /><span className="qk-pt-l">Geçmiş</span>
          </button>
        )}
        <button type="button" onClick={p.social.onShare} className="qk-act" aria-label="Soruyu paylaş" title="Soru bağlantısını paylaş"><Share2 aria-hidden /></button>
        {v12 && <CopyQuestionButton stem={p.copy.stem} options={p.copy.options} className="qk-act" />}
        {v12 && <button type="button" className="qk-act qk-act-rep" onClick={p.onReport} aria-label="Soruyu bildir" title="Soruyu bildir"><Flag aria-hidden /></button>}
      </footer>

      {p.comments && <div id={`comments-${p.id}`}>{p.comments}</div>}
      {infoToast && <InfoToast info={infoToast} onClose={() => setInfoToast(null)} />}
      {pop && (() => {
        const o = p.options.find((x) => String(x.key) === pop.key);
        const info = hideAnswer ? null : p.optionInfo?.(pop.key) ?? null;
        return (
          <TapPopover
            key={`${pop.key}-${pop.x}-${pop.y}`}
            x={pop.x}
            y={pop.y}
            info={info}
            canObject={!hideAnswer}
            onInfo={() => info && setInfoToast(info)}
            onObject={() => p.onObject(pop.key, String(o?.text ?? ''))}
            onClose={closePop}
          />
        );
      })()}
    </article>
  );
};
