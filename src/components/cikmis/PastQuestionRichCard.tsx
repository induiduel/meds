import React, { useEffect, useId, useRef, useState } from 'react';
import {
  Bookmark, BookOpen, Check, ChevronDown, Eye, FileText, Flag, History, Info, MessageSquare, RotateCcw, Share2, ThumbsDown, ThumbsUp, X,
} from 'lucide-react';
import type { CikmisCardProps } from '../../screens/cikmis/CikmisCard';
import { Highlight } from '../ui/StemText';
import { SourceText } from '../ui/SourceText';
import { ActionMenu, ActionItem } from '../ui/ActionMenu';
import { ApiService, AnswerVotes } from '../../services/api';
import { revealInView } from './revealInView';
import '../../styles/cikmis-card.css';

/**
 * Zengin çıkmış soru kartı ("Kart" görünümü, varsayılan).
 *
 * Kompakt karttaki (screens/cikmis/CikmisCard) bütün veriyi aynı props ile alır; ek olarak `rich` ile
 * kayıt/ilerleme/kaynak bilgisini taşır. Böylece PastExamsView aynı hesaplanmış props'u iki karta da verir.
 *
 * Anatomi:
 *  1. Künye: #no · yıl · ders · kurul · işaretler · durum rozeti · ⋯
 *  2. Soru kökü
 *  3. Şıklar A–E: dokununca cevaplanır; doğru/yanlış boyanır, varsa topluluk dağılımı şık içinde çubuk olur
 *     (anket, karşılaştırma, ham metin görünümünde `special` şıkların yerine geçer)
 *  4. Açıklama (açılır; cevaplayınca kendiliğinden açılır): açıklama · şık analizi · kazanım · kaynak · geçmiş
 *  5. İşlem çubuğu: beğen · yorumlar · kaydet · kaynak/bilgi · hata bildir · paylaş
 *  6. Yorumlar (mevcut yorum arayüzü) ya da son yorumun önizlemesi
 */
export interface RichCardExtras {
  /** Soru numarası (yoksa '?') */
  number?: string | number;
  year?: string;
  status?: { label: string; tone: 'ok' | 'warn' | 'bad' | 'info' } | null;
  saved: boolean;
  onToggleSave: () => void;
  /** "Kaynak ve bilgi": soru hakkında penceresi (künye, ders notu/slayt eşleşmesi, kanıt) */
  onInfo: () => void;
  /** Ders notunda aç (eşleşme varsa) */
  onOpenNote?: () => void;
  /** Daha önce bu cihazda verilen cevap */
  attempt?: { picked: string; correct: boolean } | null;
  onAnswer?: (key: string, correct: boolean) => void;
  /** Dağılım okumak için oy kimliği */
  voterUid?: string;
  commentPreview?: { author: string; text: string; more: number } | null;
}

export type PastQuestionRichCardProps = CikmisCardProps & { rich?: RichCardExtras };

const TONE_CLS: Record<string, string> = { ok: 'is-ok', warn: 'is-warn', bad: 'is-bad', info: 'is-info' };

export const PastQuestionRichCard: React.FC<PastQuestionRichCardProps> = (p) => {
  const r = p.rich;
  const uid = useId();
  const key = p.correctAnswer ? String(p.correctAnswer).toUpperCase() : '';
  const [picked, setPicked] = useState<string | null>(() => (r?.attempt?.picked ? String(r.attempt.picked).toUpperCase() : null));
  const [peek, setPeek] = useState(false); // cevaplamadan "cevabı göster"
  const revealed = Boolean(picked) || peek;
  const hasExplain = Boolean(p.explanation?.trim()) || p.analysis.length > 0 || p.refs.length > 0 || Boolean(p.kazanim) || Boolean(r?.onOpenNote);
  const [explOpen, setExplOpen] = useState(() => Boolean(r?.attempt?.picked));
  const [histOpen, setHistOpen] = useState(false);
  const [infoKey, setInfoKey] = useState<string | null>(null);
  const [votes, setVotes] = useState<AnswerVotes | null>(null);
  const explRef = useRef<HTMLDivElement>(null);

  // Yeni cevap kaydı (ör. başka sekmede çözüldü) gelirse yansıt
  useEffect(() => {
    if (r?.attempt?.picked && !picked) setPicked(String(r.attempt.picked).toUpperCase());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [r?.attempt?.picked]);

  // Topluluk dağılımı: yalnız cevap açılınca ve şıklar kartın kendisindeyken bir kez okunur
  useEffect(() => {
    if (!revealed || p.special || votes || !p.options.length) return;
    let alive = true;
    ApiService.getAnswerVotes(p.id, r?.voterUid || '')
      .then((v) => alive && setVotes(v))
      .catch(() => { /* dağılım yoksa sessizce geç */ });
    return () => { alive = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [revealed, p.special, p.id]);

  // Kaydırma: aria-expanded + aria-controls taşıyan düğmeleri utils/autoReveal.ts zaten görünür alana getirir
  // (çift kaydırma olmasın diye burada yalnız düğmesiz açılış — şık seçince açıklamanın açılması — kaydırılır).
  const openExpl = (v: boolean, scroll = false) => {
    setExplOpen(v);
    if (v) {
      if (!revealed) setPeek(true);
      if (scroll) revealInView(explRef.current);
    }
  };

  const pick = (k: string) => {
    if (revealed) return;
    const correct = Boolean(key) && k === key;
    setPicked(k);
    r?.onAnswer?.(k, correct);
    if (hasExplain) openExpl(true, true);
  };

  const reset = () => {
    setPicked(null);
    setPeek(false);
    setExplOpen(false);
  };

  const total = votes?.total || 0;
  const pctOf = (k: string) => (total ? Math.round(((votes?.counts?.[k] || 0) / total) * 100) : 0);
  const showDist = revealed && total > 0;

  const menu: ActionItem[] = [
    { label: p.social.disliked ? 'Beğenmemeyi geri al' : 'Eksik ya da hatalı (beğenme)', icon: ThumbsDown, group: 'Soru', hint: p.social.down ? String(p.social.down) : undefined, onClick: p.social.onDislike },
    ...(revealed ? [{ label: 'Cevabı gizle, yeniden çöz', icon: RotateCcw, group: 'Soru', onClick: reset }] : []),
    ...p.actions,
  ];
  const no = r?.number != null && r.number !== '' ? `#${r.number}` : '#?';

  return (
    <article id={p.anchorId} className={`ck ${p.className || ''}`} aria-labelledby={`${uid}-stem`}>
      <header className="ck-meta">
        <span className="ck-no">{no}</span>
        {r?.year && <span className="ck-m">{r.year}</span>}
        {p.ders && <span className="ck-m ck-ders" title={p.ders}><i className="ck-dot" aria-hidden />{p.ders}</span>}
        {p.kurul && <span className="ck-m" title="Kurul">{p.kurul}</span>}
        {p.flags.length > 0 && <span className="ck-flags">{p.flags.map((f, i) => <React.Fragment key={i}>{f}</React.Fragment>)}</span>}
        <span className="ck-sp" />
        {r?.status && <span className={`ck-badge ${TONE_CLS[r.status.tone] || ''}`}>{r.status.label}</span>}
        <ActionMenu items={menu} title={`Soru ${no}`} highlight={p.menuHighlight} className="ck-menu" />
      </header>

      <div className="ck-stem" id={`${uid}-stem`}>{p.stem}</div>

      {p.special ? (
        <div className="ck-special">{p.special}</div>
      ) : p.options.length > 0 ? (
        <>
          <ol className={`ck-opts ${revealed ? 'is-revealed' : ''}`} aria-label="Şıklar">
            {p.options.map((o) => {
              const k = String(o.key).toUpperCase();
              const isKey = revealed && k === key;
              const isWrong = revealed && picked === k && k !== key;
              const pct = pctOf(k);
              const info = revealed ? p.optionInfo?.(k) ?? null : null;
              const st = isKey ? 'is-ok' : isWrong ? 'is-bad' : revealed ? 'is-dim' : '';
              return (
                <li key={k} className="ck-opt-li">
                  <div className={`ck-opt ${st} ${picked === k ? 'is-picked' : ''}`}>
                    <button
                      type="button"
                      className="ck-opt-b"
                      onClick={() => pick(k)}
                      aria-disabled={revealed || undefined}
                      aria-label={
                        revealed
                          ? `${k}: ${String(o.text ?? '')}${isKey ? ', doğru cevap' : ''}${isWrong ? ', senin cevabın, yanlış' : ''}${showDist ? `, yüzde ${pct}` : ''}`
                          : `${k} şıkkını işaretle: ${String(o.text ?? '')}`
                      }
                    >
                      {showDist && <span className="ck-fill" style={{ width: `${pct}%` }} aria-hidden />}
                      <span className="ck-key" aria-hidden>{isKey ? <Check strokeWidth={3} /> : isWrong ? <X strokeWidth={3} /> : k}</span>
                      <span className="ck-opt-t" aria-hidden><Highlight text={String(o.text ?? '')} terms={p.terms} /></span>
                      {showDist && <span className="ck-pct" aria-hidden>%{pct}</span>}
                    </button>
                    {info && (
                      <button type="button" className="ck-opt-i" onClick={() => setInfoKey((v) => (v === k ? null : k))} aria-expanded={infoKey === k} aria-label={`${k} şıkkında yapılan değişiklik`} title="Bu şıkta yapılan değişiklik">
                        <Info aria-hidden />
                      </button>
                    )}
                  </div>
                  {info && infoKey === k && (
                    <div className="ck-opt-note" role="note">
                      <b>{info.title}</b>
                      {info.before !== undefined && <p><span>Önce</span>{info.before ? <del>{info.before}</del> : <i>(yoktu)</i>}</p>}
                      {info.after !== undefined && <p><span>Sonra</span><ins>{info.after}</ins></p>}
                      {info.note && <p className="is-note">{info.note}</p>}
                      <button type="button" className="ck-link" onClick={() => p.onObject(k, String(o.text ?? ''))}>Bu şıkka itiraz et</button>
                    </div>
                  )}
                </li>
              );
            })}
          </ol>
          {picked && key ? (
            <p className={`ck-verdict ${picked === key ? 'is-ok' : 'is-bad'}`} role="status">
              <b>{picked === key ? 'Doğru' : `Yanlış · doğru cevap ${key}`}</b>
              {showDist && <span className="ck-verdict-n">{total.toLocaleString('tr-TR')} kişi cevapladı</span>}
              <button type="button" className="ck-link" onClick={reset}><RotateCcw aria-hidden />Yeniden çöz</button>
            </p>
          ) : picked && !key ? (
            <p className="ck-verdict is-info" role="status"><b>Cevap anahtarı yok</b><span className="ck-verdict-n">Cevabın kaydedildi</span></p>
          ) : !revealed && key ? (
            <p className="ck-hint">
              Bir şıkka dokunarak cevapla
              <button type="button" className="ck-link" onClick={() => setPeek(true)}><Eye aria-hidden />Cevabı göster</button>
            </p>
          ) : null}
        </>
      ) : null}

      {p.notes}

      {hasExplain && (
        <section className={`ck-expl ${explOpen ? 'is-open' : ''}`}>
          <button type="button" className="ck-expl-h" aria-expanded={explOpen} aria-controls={`${uid}-expl`} onClick={() => openExpl(!explOpen)}>
            <BookOpen aria-hidden />
            <span>Açıklama</span>
            {!revealed && !explOpen && <small>cevabı da gösterir</small>}
            <ChevronDown aria-hidden className="ck-chev" />
          </button>
          <div className="ck-rev" id={`${uid}-expl`} ref={explRef}>
            <div className="ck-rev-in" inert={!explOpen ? true : undefined}>
              <div className="ck-expl-b">
                {p.explanation?.trim() ? <SourceText text={p.explanation} size="sm" /> : <p className="ck-muted">Bu soruya henüz açıklama yazılmadı.</p>}
                {p.analysis.length > 0 && (
                  <dl className="ck-analysis">
                    {p.analysis.map(([k, v]) => (
                      <div key={k} className={String(k).toUpperCase() === key ? 'is-ok' : ''}>
                        <dt>{k}</dt>
                        <dd>{String(v)}</dd>
                      </div>
                    ))}
                  </dl>
                )}
                {p.kazanim && <p className="ck-kaz"><b>{p.kazanim.baslik}</b>{p.kazanim.metin}</p>}
                {(p.refs.length > 0 || r?.onOpenNote) && (
                  <p className="ck-refs">
                    <FileText aria-hidden />
                    <span>{p.refs.length > 0 ? p.refs.join(' · ') : 'Ders notu'}</span>
                    {r?.onOpenNote && <button type="button" className="ck-link" onClick={r.onOpenNote}>Ders notunda aç</button>}
                  </p>
                )}
                {p.history && (
                  <>
                    <button type="button" className="ck-link" aria-expanded={histOpen} aria-controls={`${uid}-hist`} onClick={() => setHistOpen((v) => !v)}>
                      <History aria-hidden />Değişiklik geçmişi{p.historyBadge ? ` · ${p.historyBadge}` : ''}
                    </button>
                    <div id={`${uid}-hist`} className="ck-hist" hidden={!histOpen}>{histOpen && p.history}</div>
                  </>
                )}
              </div>
            </div>
          </div>
        </section>
      )}

      <footer className="ck-bar" aria-label="Soru işlemleri">
        <button type="button" className={`ck-act ${p.social.liked ? 'is-on' : ''}`} onClick={p.social.onLike} aria-pressed={p.social.liked} aria-label={`Beğen, ${p.social.up} beğeni`} title={p.social.liked ? 'Beğeniyi geri al' : 'Soruyu beğen'}>
          <ThumbsUp aria-hidden className={p.social.liked ? 'is-fill' : ''} /><span aria-hidden>{p.social.up}</span>
        </button>
        <button type="button" className={`ck-act ${p.social.commentsOpen ? 'is-on' : ''}`} onClick={p.social.onComments} aria-expanded={p.social.commentsOpen} aria-controls={`${uid}-comm`} aria-label={`Yorumlar, ${p.social.comments}`} title="Yorumlar">
          <MessageSquare aria-hidden /><span aria-hidden>{p.social.comments}</span>
        </button>
        <button type="button" className={`ck-act ${r?.saved ? 'is-on' : ''}`} onClick={r?.onToggleSave} aria-pressed={Boolean(r?.saved)} aria-label={r?.saved ? 'Kaydedildi, kaydı kaldır' : 'Kaydet'} title={r?.saved ? 'Kaydedilenlerden çıkar' : 'Kaydet'} disabled={!r}>
          <Bookmark aria-hidden className={r?.saved ? 'is-fill' : ''} />
        </button>
        <button type="button" className="ck-act" onClick={r?.onInfo} aria-label="Kaynak ve bilgi" title="Kaynak ve bilgi" disabled={!r}>
          <Info aria-hidden />
        </button>
        <button type="button" className="ck-act" onClick={p.onReport} aria-label="Hata bildir" title="Hata bildir">
          <Flag aria-hidden />
        </button>
        <span className="ck-sp" />
        <button type="button" className="ck-act" onClick={p.social.onShare} aria-label="Soruyu paylaş" title="Soru bağlantısını paylaş">
          <Share2 aria-hidden />
        </button>
      </footer>

      {p.social.commentsOpen ? (
        <div id={`${uid}-comm`} className="ck-comments">{p.comments}</div>
      ) : r?.commentPreview ? (
        <button type="button" className="ck-cprev" onClick={p.social.onComments} aria-label={`Yorumları aç: ${r.commentPreview.author}`}>
          <span className="ck-av" aria-hidden>{r.commentPreview.author.trim().charAt(0).toLocaleUpperCase('tr-TR') || 'T'}</span>
          <span className="ck-cprev-t"><b>{r.commentPreview.author}</b> {r.commentPreview.text}</span>
          {r.commentPreview.more > 0 && <span className="ck-cprev-more">+{r.commentPreview.more} yorum</span>}
        </button>
      ) : null}
    </article>
  );
};

/** Yüklenirken kart iskeleti (.ui-skel) */
export const RichCardSkeleton: React.FC = () => (
  <div className="ck ck-skel" aria-hidden>
    <div className="ck-meta"><span className="ui-skel" style={{ width: 34, height: 12 }} /><span className="ui-skel" style={{ width: 110, height: 12 }} /></div>
    <span className="ui-skel" style={{ width: '92%', height: 16 }} />
    <span className="ui-skel" style={{ width: '64%', height: 16 }} />
    <div className="ck-opts">
      {[0, 1, 2, 3, 4].map((i) => <span key={i} className="ui-skel" style={{ height: 42, borderRadius: 10 }} />)}
    </div>
    <span className="ui-skel" style={{ width: '50%', height: 28 }} />
  </div>
);

/**
 * Kademeli çizim: liste sonuna konur; görünür olunca (ya da yaklaşınca) `onMore` çağrılır.
 * IntersectionObserver yoksa düğme olarak kalır.
 */
export const LoadMoreSentinel: React.FC<{ onMore: () => void; remaining: number }> = ({ onMore, remaining }) => {
  const ref = useRef<HTMLDivElement>(null);
  const cb = useRef(onMore);
  cb.current = onMore;
  useEffect(() => {
    const el = ref.current;
    if (!el || typeof IntersectionObserver === 'undefined') return;
    const io = new IntersectionObserver((es) => { if (es.some((e) => e.isIntersecting)) cb.current(); }, { rootMargin: '800px 0px' });
    io.observe(el);
    return () => io.disconnect();
  }, [remaining]);
  if (remaining <= 0) return null;
  return (
    <div ref={ref} className="ck-more">
      <button type="button" className="ui-btn is-ghost" onClick={onMore}>{remaining.toLocaleString('tr-TR')} soru daha</button>
    </div>
  );
};
