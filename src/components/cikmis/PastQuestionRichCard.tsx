import React, { useEffect, useId, useRef, useState } from 'react';
import {
  Bookmark, BookOpen, Check, ChevronDown, Eye, FileText, Flag, Heart, History, Info, MessageSquare, RotateCcw, Share2, Strikethrough, ThumbsDown, ThumbsUp, X,
} from 'lucide-react';
import { CopyQuestionButton } from '../ui/CopyQuestionButton';
import { useAppearance } from '../../utils/appearance';
import type { CikmisCardProps } from '../../screens/cikmis/CikmisCard';
import { Highlight } from '../ui/StemText';
import { useLiveEvent } from '../../hooks/useLiveEvent';
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
  /** Konu (v12 etiket satırında) */
  topic?: string;
}

export type PastQuestionRichCardProps = CikmisCardProps & { rich?: RichCardExtras };

const TONE_CLS: Record<string, string> = { ok: 'is-ok', warn: 'is-warn', bad: 'is-bad', info: 'is-info' };

export const PastQuestionRichCard: React.FC<PastQuestionRichCardProps> = (p) => {
  const r = p.rich;
  const uid = useId();
  // v12: şık satırında hızlı düğme (cevaplamadan önce ele, sonra şıkkı bildir) + alt çubukta kopyala
  const look = useAppearance();
  const v12 = look.design === 'v12';
  // Ayarlar › Görünüm › Çıkmış soru kartı: mod + açılıp kapanan alanlar
  const qc = look.qcard;
  const [folded, setFolded] = useState(true);
  const collapsed = qc.mode === 'katlanir' && folded;
  const analysis = qc.sikAciklama ? p.analysis : [];
  const [elim, setElim] = useState<Set<string>>(() => new Set());
  const key = p.correctAnswer ? String(p.correctAnswer).toUpperCase() : '';
  const [picked, setPicked] = useState<string | null>(() => (r?.attempt?.picked ? String(r.attempt.picked).toUpperCase() : null));
  const [peek, setPeek] = useState(false); // cevaplamadan "cevabı göster"
  const revealed = Boolean(picked) || peek;
  const hasExplain = qc.aciklama && (Boolean(p.explanation?.trim()) || analysis.length > 0 || p.refs.length > 0 || Boolean(p.kazanim) || Boolean(r?.onOpenNote));
  const [explOpen, setExplOpen] = useState(() => Boolean(r?.attempt?.picked));
  const [explMounted, setExplMounted] = useState(() => Boolean(r?.attempt?.picked));
  const [histOpen, setHistOpen] = useState(false);
  const [infoKey, setInfoKey] = useState<string | null>(null);
  const [votes, setVotes] = useState<AnswerVotes | null>(null);
  const explRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (explOpen && !explMounted) setExplMounted(true);
  }, [explOpen, explMounted]);

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

  // Açık dağılım başka öğrencinin oyuyla canlı güncellenir
  useLiveEvent(
    'votes_changed',
    (e) => {
      if (e?.resync || e?.questionId === p.id) ApiService.getAnswerVotes(p.id, r?.voterUid || '').then(setVotes).catch(() => {});
    },
    { enabled: !!votes },
  );

  // Kaydırma: aria-expanded + aria-controls taşıyan düğmeleri utils/autoReveal.ts zaten görünür alana getirir
  // (çift kaydırma olmasın diye burada yalnız düğmesiz açılış — şık seçince açıklamanın açılması — kaydırılır).
  const openExpl = (v: boolean, scroll = false) => {
    if (v && !explMounted) setExplMounted(true);
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
    setElim(new Set());
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

  // Açıklama gövdesi: v10/v11'de şıkların altında başlıklı bölüm, v12'de işlem çubuğunun altında (çubuktaki "Açıklama" açar)
  const explRev = hasExplain ? (
    <div className="ck-rev" id={`${uid}-expl`} ref={explRef}>
      <div className="ck-rev-in" inert={!explOpen ? true : undefined}>
        {explMounted ? (
          <div className="ck-expl-b">
            {p.explanation?.trim() ? <SourceText text={p.explanation} size="sm" /> : <p className="ck-muted">Bu soruya henüz açıklama yazılmadı.</p>}
            {analysis.length > 0 && (
              <dl className="ck-analysis">
                {analysis.map(([k, v]) => (
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
        ) : null}
      </div>
    </div>
  ) : null;

  return (
    <article id={p.anchorId} className={`ck ${qc.mode === 'dar' ? 'is-dar' : ''} ${collapsed ? 'is-folded' : ''} ${p.className || ''}`} aria-labelledby={`${uid}-stem`}>
      {v12 ? (
        <header className="ck-meta">
          <span className="ck-no">S {r?.number != null && r.number !== '' ? r.number : '?'}</span>
          {qc.yil && r?.year && <span className="ck-m">{r.year}</span>}
          {qc.kurul && p.kurul && <span className="ck-m" title="Kurul">{p.kurul.replace(/^K(?=\d)/, 'Kurul ')}</span>}
          {qc.ders && p.ders && <span className="ck-m ck-ders" title={p.ders}><i className="ck-dot" aria-hidden />{p.ders}</span>}
          {picked && key && <span className={`ck-badge ${picked === key ? 'is-ok' : 'is-bad'}`}>{picked === key ? 'Doğru' : 'Yanlış'}</span>}
          {r?.status && <span className={`ck-badge ${TONE_CLS[r.status.tone] || ''}`}>{r.status.label}</span>}
          <span className="ck-sp" />
          {r && (
            <button type="button" className={`c12-qsave ${r.saved ? 'is-on' : ''}`} onClick={r.onToggleSave} aria-pressed={r.saved} aria-label={r.saved ? 'Kaydedildi, kaydı kaldır' : 'Soruyu kaydet'} title={r.saved ? 'Kaydedilenlerden çıkar' : 'Kaydet'}>
              <Bookmark aria-hidden className={r.saved ? 'is-fill' : ''} />
            </button>
          )}
          <ActionMenu items={menu} title={`Soru ${no}`} highlight={p.menuHighlight} className="ck-menu" />
        </header>
      ) : (
      <header className="ck-meta">
        <span className="ck-no">{no}</span>
        {qc.yil && r?.year && <span className="ck-m">{r.year}</span>}
        {qc.ders && p.ders && <span className="ck-m ck-ders" title={p.ders}><i className="ck-dot" aria-hidden />{p.ders}</span>}
        {qc.kurul && p.kurul && <span className="ck-m" title="Kurul">{p.kurul}</span>}
        {p.flags.length > 0 && <span className="ck-flags">{p.flags.map((f, i) => <React.Fragment key={i}>{f}</React.Fragment>)}</span>}
        <span className="ck-sp" />
        {r?.status && <span className={`ck-badge ${TONE_CLS[r.status.tone] || ''}`}>{r.status.label}</span>}
        <ActionMenu items={menu} title={`Soru ${no}`} highlight={p.menuHighlight} className="ck-menu" />
      </header>
      )}

      <div className="ck-stem" id={`${uid}-stem`}>{p.stem}</div>

      {qc.mode === 'katlanir' && (
        <button type="button" className="ck-fold" aria-expanded={!folded} aria-controls={`${uid}-body`} onClick={() => setFolded((v) => !v)}>
          <ChevronDown aria-hidden className={folded ? '' : 'is-open'} />
          {folded ? 'Şıkları göster' : 'Şıkları gizle'}
        </button>
      )}

      {collapsed ? null : (<div className="ck-body" id={`${uid}-body`}>
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
                <li key={k} className={`ck-opt-li ${v12 ? 'has-quick' : ''} ${!revealed && elim.has(k) ? 'is-elim' : ''}`}>
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
                    {v12 && (!revealed ? (
                      <button type="button" className={`ck-oq ${elim.has(k) ? 'is-on' : ''}`} aria-pressed={elim.has(k)}
                        onClick={() => setElim((m) => { const n = new Set(m); if (n.has(k)) n.delete(k); else n.add(k); return n; })}
                        aria-label={elim.has(k) ? `${k} şıkkını geri al` : `${k} şıkkını ele`} title={elim.has(k) ? 'Geri al' : 'Bu şıkkı ele (üstünü çiz)'}>
                        <Strikethrough aria-hidden />
                      </button>
                    ) : !info && (
                      <button type="button" className="ck-oq is-flag" onClick={() => p.onObject(k, String(o.text ?? ''))} aria-label={`${k} şıkkını bildir`} title="Bu şıkkı bildir">
                        <Flag aria-hidden />
                      </button>
                    ))}
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

      {v12 && look.qtags && (
        <div className="c12-tags">
          {r?.topic && r.topic !== p.ders && <span className="c12-tag" title={r.topic}>{r.topic}</span>}
          {p.flags.map((f, i) => <React.Fragment key={i}>{f}</React.Fragment>)}
          {p.kazanim && <span className="c12-tag is-acc" title={p.kazanim.metin}>Kazanım: {p.kazanim.metin}</span>}
        </div>
      )}

      {hasExplain && !v12 && (
        <section className={`ck-expl ${explOpen ? 'is-open' : ''}`}>
          <button type="button" className="ck-expl-h" aria-expanded={explOpen} aria-controls={`${uid}-expl`} onClick={() => openExpl(!explOpen)}>
            <BookOpen aria-hidden />
            <span>Açıklama</span>
            {!revealed && !explOpen && <small>cevabı da gösterir</small>}
            <ChevronDown aria-hidden className="ck-chev" />
          </button>
          {explRev}
        </section>
      )}

      {v12 ? (
        <footer className="ck-bar" role="toolbar" aria-label="Soru işlemleri">
          <button type="button" className={`ck-act ${p.social.liked ? 'is-on' : ''}`} onClick={p.social.onLike} aria-pressed={p.social.liked} aria-label={`Beğen, ${p.social.up} beğeni`} title={p.social.liked ? 'Beğeniyi geri al' : 'Soruyu beğen'}>
            <Heart aria-hidden className={p.social.liked ? 'is-fill' : ''} /><span className="c12-n" aria-hidden>{p.social.up}</span>
          </button>
          <button type="button" className={`ck-act ${p.social.commentsOpen ? 'is-on' : ''}`} onClick={p.social.onComments} aria-expanded={p.social.commentsOpen} aria-controls={`${uid}-comm`} aria-label={`Yorumlar, ${p.social.comments}`} title="Yorumlar">
            <MessageSquare aria-hidden /><span className="c12-n" aria-hidden>{p.social.comments}</span>
          </button>
          {hasExplain && (
            <button type="button" className={`ck-act c12-act-exp ${explOpen ? 'is-on' : ''}`} aria-expanded={explOpen} aria-controls={`${uid}-expl`} onClick={() => openExpl(!explOpen)}
              title={!revealed && !explOpen ? 'Açıklamayı aç (cevabı da gösterir)' : 'Açıklama'}>
              <Info aria-hidden /><span>Açıklama</span>
            </button>
          )}
          <span className="ck-sp" />
          <CopyQuestionButton stem={p.copy.stem} options={p.copy.options} className="ck-act ck-copy" />
          <button type="button" className="ck-act" onClick={p.social.onShare} aria-label="Soruyu paylaş" title="Soru bağlantısını paylaş">
            <Share2 aria-hidden />
          </button>
          <button type="button" className="ck-act c12-act-rep" onClick={p.onReport} aria-label="Soruyu bildir" title="Hata bildir">
            <Flag aria-hidden />
          </button>
        </footer>
      ) : (
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
      )}

      {v12 && explRev && <section className={`ck-expl c12-expl ${explOpen ? 'is-open' : ''}`} aria-label="Açıklama">{explRev}</section>}
      </div>)}

      {collapsed ? null : p.social.commentsOpen ? (
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
export const LoadMoreSentinel: React.FC<{ onMore: () => void; remaining: number; shown?: number; total?: number }> = ({ onMore, remaining, shown, total }) => {
  const v12 = useAppearance().design === 'v12';
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
      {v12 && shown != null && total != null ? (
        <button type="button" className="c12-more" onClick={onMore}>
          Daha fazla yükle · <span className="c12-more-n">{shown.toLocaleString('tr-TR')} / {total.toLocaleString('tr-TR')}</span>
        </button>
      ) : (
        <button type="button" className="ui-btn is-ghost" onClick={onMore}>{remaining.toLocaleString('tr-TR')} soru daha</button>
      )}
    </div>
  );
};
