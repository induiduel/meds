import React, { useEffect, useId, useState } from 'react';
import { BookOpen, Check, ChevronDown, Flag, History, MessageSquare, Share2, ShieldAlert, ThumbsDown, ThumbsUp, X } from 'lucide-react';
import { Highlight } from '../../components/ui/StemText';
import { SourceText } from '../../components/ui/SourceText';
import { ActionMenu, ActionItem } from '../../components/ui/ActionMenu';
import { CopyQuestionButton } from '../../components/ui/CopyQuestionButton';

/**
 * Çıkmış soru kartı — yeniden kurulum (2026-10-11, canvas "Main" artboard'u).
 *
 * Anatomi:
 *  1. Künye satırı: kurul çipi · mono künye (yıl · S-no) · ders etiketi · en çok 2 durum işareti (+n) · kopyala · bildir · ⋯
 *  2. Soru kökü
 *  3. Şıklar (tek sütun, kabarcık) ya da özel görünüm (anket / karşılaştırma / ham metin)
 *  4. Kart içi akordiyonlar: "Açıklama ve şık analizi", "Değişiklik geçmişi" — içerik akışta kalır, alttaki kartı iter
 *  5. Eylem satırı: beğen · beğenme · yorum · paylaş; yorumlar kartın içinde açılır
 * Veri ve iş mantığı çağıran ekranda kalır; bu bileşen yalnız yapıyı ve etkileşim durumunu taşır.
 */
export interface CikmisOption { key: string; text: string; isAiGenerated?: boolean }

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
  optionInfo?: (key: string) => React.ReactNode;
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

const Disclosure: React.FC<{ icon: React.ElementType; title: string; badge?: string; anchor?: string; deepOpen?: () => boolean; children: React.ReactNode }> = ({ icon: Icon, title, badge, anchor, deepOpen, children }) => {
  const [open, setOpen] = useState(() => Boolean(deepOpen?.()));
  const bodyId = useId();
  // Uygulama içi gezinmede (bildirim, paylaşım) adres değişince bölüm açılır.
  useEffect(() => {
    if (!deepOpen) return;
    const on = () => { if (deepOpen()) setOpen(true); };
    window.addEventListener('popstate', on);
    return () => window.removeEventListener('popstate', on);
  }, [deepOpen]);
  return (
    <div id={anchor} className={`qk-disc ${open ? 'is-open' : ''}`}>
      <button type="button" className="qk-disc-h" aria-expanded={open} aria-controls={bodyId} onClick={() => setOpen((v) => !v)}>
        <Icon aria-hidden />
        <span>{title}</span>
        {badge && <span className="qk-disc-badge">{badge}</span>}
        <ChevronDown className="qk-chev" aria-hidden />
      </button>
      <div id={bodyId} className="qk-disc-b">
        <div className="qk-disc-in" inert={!open ? true : undefined}>{children}</div>
      </div>
    </div>
  );
};

export const CikmisCard: React.FC<CikmisCardProps> = (p) => {
  const [flagsOpen, setFlagsOpen] = useState(false);
  const shownFlags = flagsOpen ? p.flags : p.flags.slice(0, 2);
  const hiddenCount = p.flags.length - shownFlags.length;
  const hideAnswer = p.quiz.on && !p.quiz.picked;
  const short = p.options.every((o) => String(o.text ?? '').length <= 42);
  const hasExplain = !hideAnswer && (Boolean(p.explanation?.trim()) || p.analysis.length > 0 || p.refs.length > 0);
  const explWanted = React.useCallback(() => wantsSection(p.id, 'explanation'), [p.id]);

  return (
    <article id={p.anchorId} className={`qk ${p.className || ''}`}>
      <header className={`qk-h ${flagsOpen ? 'is-flags-open' : ''}`}>
        {p.kurul && <span className="qk-chip" title="Kurul">{p.kurul}</span>}
        <span className="qk-kunye" title={p.kunye}>{p.kunye}</span>
        {p.ders && <span className="qk-ders"><i className="hk-dot" aria-hidden />{p.ders}</span>}
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
          <ol className={`qk-opts ${short ? 'is-short' : ''}`}>
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
                <li key={key} id={`opt-${p.id}-${key}`} className="qk-opt-li">
                  {p.quiz.on && !p.quiz.picked ? (
                    <button type="button" className={cls} onClick={() => p.quiz.onPick(key)} aria-label={`${key} şıkkını işaretle`}>{inner}</button>
                  ) : (
                    <div className={cls}>{inner}</div>
                  )}
                  {p.optionInfo?.(key)}
                  {!hideAnswer && (
                    <button type="button" className="qk-obj" onClick={() => p.onObject(key, String(o.text ?? ''))} aria-label={`${key} şıkkına itiraz et`} title={`${key} şıkkına itiraz et`}>
                      <ShieldAlert aria-hidden />
                    </button>
                  )}
                </li>
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

      {(hasExplain || p.history) && (
        <div className="qk-discs">
          {hasExplain && (
            <Disclosure icon={BookOpen} title="Açıklama ve şık analizi" badge={p.analysis.length ? `${p.analysis.length} şık` : undefined} anchor={`expl-${p.id}`} deepOpen={explWanted}>
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
              {p.refs.length > 0 && (
                <p className="qk-refs"><b>Kaynak</b>{p.refs.join(' · ')}</p>
              )}
            </Disclosure>
          )}
          {p.history && (
            <Disclosure icon={History} title="Değişiklik geçmişi" badge={p.historyBadge}>
              {p.history}
            </Disclosure>
          )}
        </div>
      )}

      <footer className="qk-f">
        <button type="button" onClick={p.social.onLike} aria-pressed={p.social.liked} className={`qk-act ${p.social.liked ? 'is-on' : ''}`} title={p.social.liked ? 'Beğeniyi geri al' : 'Soruyu beğen'}>
          <ThumbsUp className={p.social.liked ? 'fill-current' : ''} aria-hidden /><span>{p.social.up}</span><span className="sr-only"> beğeni</span>
        </button>
        <button type="button" onClick={p.social.onDislike} aria-pressed={p.social.disliked} className={`qk-act ${p.social.disliked ? 'is-bad' : ''}`} title={p.social.disliked ? 'Beğenmemeyi geri al' : 'Eksik ya da hatalı'}>
          <ThumbsDown className={p.social.disliked ? 'fill-current' : ''} aria-hidden /><span>{p.social.down}</span><span className="sr-only"> beğenmeme</span>
        </button>
        <button type="button" onClick={p.social.onComments} aria-expanded={p.social.commentsOpen} className={`qk-act ${p.social.commentsOpen ? 'is-on' : ''}`}>
          <MessageSquare aria-hidden /><span>{p.social.comments}</span><span className="sr-only"> yorum</span>
        </button>
        <span className="qk-sp" />
        <button type="button" onClick={p.social.onShare} className="qk-act" aria-label="Soruyu paylaş" title="Soru bağlantısını paylaş"><Share2 aria-hidden /></button>
      </footer>

      {p.comments && <div id={`comments-${p.id}`}>{p.comments}</div>}
    </article>
  );
};
