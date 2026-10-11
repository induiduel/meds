import React, { useCallback, useEffect, useId, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { BookOpen, Check, Flag, History, Info, MessageSquare, Share2, ThumbsDown, ThumbsUp, X } from 'lucide-react';
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

/** Yükseklik canlandırmalı açılır bölüm (grid-template-rows 0fr → 1fr); kapalıyken içerik odak almaz. */
const Reveal: React.FC<{ open: boolean; id?: string; className?: string; children: React.ReactNode }> = ({ open, id, className = '', children }) => (
  <div id={id} className={`qk-rev ${open ? 'is-open' : ''} ${className}`}>
    <div className="qk-rev-in" inert={!open ? true : undefined}>{children}</div>
  </div>
);

const DRAWER_W = 112; // eylem çekmecesi genişliği (px)

/**
 * Kayan işlem çekmecesi olan şık satırı.
 * - Dokunma/tıklama: çekmeceyi açar/kapar (sınav kipinde dokunma cevap seçer, çekmece kaydırmayla açılır).
 * - Sürükleme: parmakla sola çekilir; eşiği geçerse yerine oturur (yay eğrisi), geçmezse geri döner.
 */
const OptRow: React.FC<{
  qid: string;
  k: string;
  cls: string;
  inner: React.ReactNode;
  pickable: boolean;
  onPick: () => void;
  open: boolean;
  setOpen: (v: boolean) => void;
  info: CikmisOptionInfo | null;
  canObject: boolean;
  onObject: () => void;
  onInfo: (info: CikmisOptionInfo) => void;
}> = ({ qid, k, cls, inner, pickable, onPick, open, setOpen, info, canObject, onObject, onInfo }) => {
  const [dx, setDx] = useState<number | null>(null);
  const start = useRef<{ x: number; y: number; base: number; locked: boolean | null } | null>(null);
  const moved = useRef(false);
  const hasActions = Boolean(info) || canObject;

  const onPointerDown = (e: React.PointerEvent) => {
    if (!hasActions || e.button !== 0) return;
    start.current = { x: e.clientX, y: e.clientY, base: open ? -DRAWER_W : 0, locked: null };
    moved.current = false;
  };
  const onPointerMove = (e: React.PointerEvent) => {
    const s = start.current;
    if (!s) return;
    const mx = e.clientX - s.x;
    const my = e.clientY - s.y;
    if (s.locked === null && (Math.abs(mx) > 6 || Math.abs(my) > 6)) s.locked = Math.abs(mx) > Math.abs(my);
    if (!s.locked) return;
    moved.current = true;
    try { (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId); } catch { /* yoksay */ }
    // Sağa aşırı çekişte direnç
    const raw = s.base + mx;
    setDx(raw > 0 ? Math.sqrt(raw) * 2 : Math.max(raw, -DRAWER_W - 24));
  };
  const onPointerUp = () => {
    start.current = null;
    if (dx !== null) {
      setOpen(dx < -DRAWER_W / 2.4);
      setDx(null);
    }
    window.setTimeout(() => { moved.current = false; }, 0);
  };
  const onClick = () => {
    if (moved.current) return;
    if (pickable) { onPick(); return; }
    if (hasActions) setOpen(!open);
  };

  const x = dx ?? (open ? -DRAWER_W : 0);
  return (
    <li id={`opt-${qid}-${k}`} className={`qk-opt-li qk-swipe ${open ? 'is-open' : ''} ${dx !== null ? 'is-drag' : ''}`}>
      <div className="qk-swipe-row">
        {hasActions && (
          <div className="qk-swipe-acts" aria-hidden={!open} style={{ width: DRAWER_W }}>
            {info && (
              <button type="button" tabIndex={open ? 0 : -1} className="qk-swipe-act is-info" onClick={() => { setOpen(false); onInfo(info); }}>
                <i aria-hidden><Info /></i><span>Bilgi</span>
              </button>
            )}
            {canObject && (
              <button type="button" tabIndex={open ? 0 : -1} className="qk-swipe-act is-flag" onClick={() => { setOpen(false); onObject(); }}>
                <i aria-hidden><Flag /></i><span>Bildir</span>
              </button>
            )}
          </div>
        )}
        <button
          type="button"
          className={`${cls} qk-swipe-front`}
          style={{ transform: `translate3d(${x}px,0,0)` }}
          onPointerDown={onPointerDown}
          onPointerMove={onPointerMove}
          onPointerUp={onPointerUp}
          onPointerCancel={onPointerUp}
          onClick={onClick}
          aria-expanded={hasActions && !pickable ? open : undefined}
          aria-label={pickable ? `${k} şıkkını işaretle` : undefined}
        >
          {inner}
          {info && <span className="qk-opt-dot" title="Bu şık düzeltildi" aria-hidden />}
        </button>
      </div>
    </li>
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
  const [flagsOpen, setFlagsOpen] = useState(false);
  const [openOpt, setOpenOpt] = useState<string | null>(null);
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

  // Açık çekmece: o şıkkın dışına dokununca ya da Esc ile kapanır.
  useEffect(() => {
    if (!openOpt) return;
    const close = (e: Event) => {
      const row = rootRef.current?.querySelector(`#opt-${CSS.escape(p.id)}-${CSS.escape(openOpt)}`);
      if (e instanceof KeyboardEvent ? e.key === 'Escape' : !row?.contains(e.target as Node)) setOpenOpt(null);
    };
    document.addEventListener('pointerdown', close);
    document.addEventListener('keydown', close);
    return () => {
      document.removeEventListener('pointerdown', close);
      document.removeEventListener('keydown', close);
    };
  }, [openOpt, p.id]);

  const toggle = (k: 'expl' | 'hist') => setPanel((v) => (v === k ? null : k));

  return (
    <article ref={rootRef} id={p.anchorId} className={`qk ${p.className || ''}`}>
      <header className={`qk-h ${flagsOpen ? 'is-flags-open' : ''}`}>
        {p.ders && <span className="qk-ders"><i className="hk-dot" aria-hidden />{p.ders}</span>}
        {p.kurul && <span className="qk-chip" title="Kurul">{p.kurul}</span>}
        <span className="qk-kunye" title={p.kunye}>{p.kunye}</span>
        {shownFlags.length > 0 && <span className="qk-flags">{shownFlags.map((f, i) => <React.Fragment key={i}>{f}</React.Fragment>)}</span>}
        {hiddenCount > 0 && (
          <button type="button" className="qk-more-flags" onClick={() => setFlagsOpen(true)} aria-label={`${hiddenCount} işaret daha göster`}>+{hiddenCount}</button>
        )}
        <span className="qk-sp" />
        {p.headExtra}
        <CopyQuestionButton stem={p.copy.stem} options={p.copy.options} className="qk-ib" />
        <button type="button" className="qk-ib" onClick={p.onReport} aria-label="Hata bildir" title="Hata bildir"><Flag aria-hidden /></button>
        <ActionMenu items={p.actions} title={`Soru ${p.numberLabel}`} highlight={p.menuHighlight} />
      </header>

      <div className="qk-stem">{p.stem}</div>

      {p.kazanim && (
        <p className="qk-kaz"><b>{p.kazanim.baslik}</b>{p.kazanim.metin}</p>
      )}

      {p.special ?? (
        p.options.length > 0 && (
          <ol className={`qk-opts is-swipe ${short ? 'is-short' : ''}`}>
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
                  open={openOpt === key}
                  setOpen={(v) => setOpenOpt(v ? key : null)}
                  info={hideAnswer ? null : p.optionInfo?.(key) ?? null}
                  canObject={!hideAnswer}
                  onObject={() => p.onObject(key, String(o.text ?? ''))}
                  onInfo={setInfoToast}
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
      </footer>

      {p.comments && <div id={`comments-${p.id}`}>{p.comments}</div>}
      {infoToast && <InfoToast info={infoToast} onClose={() => setInfoToast(null)} />}
    </article>
  );
};
