import React, { createContext, useContext, useMemo, useState } from 'react';
import { Flag, MapPin, Send, ThumbsDown, ThumbsUp } from 'lucide-react';
import { Dialog } from '../../ui/Dialog';
import { toast } from '../../ui/Toast';
import { FeedbackItem, FeedbackTarget, sendFeedback, voteFeedback } from './lessonFeedback';

/* ---------------------------------------------------------------------------
 * Bağlam: dersin tüm bildirimleri hedef anahtarına göre; bayraklar sayıyı buradan okur
 * ------------------------------------------------------------------------- */
interface Ctx {
  byKey: Map<string, FeedbackItem[]>;
  open: (t: FeedbackTarget) => void;
}
const FeedbackCtx = createContext<Ctx>({ byKey: new Map(), open: () => {} });
export const FeedbackProvider = FeedbackCtx.Provider;
export const useFeedback = () => useContext(FeedbackCtx);

export const groupFeedback = (list: FeedbackItem[]) => {
  const m = new Map<string, FeedbackItem[]>();
  list.forEach((f) => m.set(f.targetKey, [...(m.get(f.targetKey) || []), f]));
  return m;
};

/** Küçük bayrak: bildirim yoksa sade, varsa sayıyla vurgulu. */
export const FeedbackFlag: React.FC<{ target: FeedbackTarget; className?: string }> = ({ target, className = '' }) => {
  const { byKey, open } = useFeedback();
  const n = byKey.get(target.key)?.length || 0;
  return (
    <button
      type="button"
      className={`ls-flag ${n ? 'has-reports' : ''} ${className}`}
      onClick={(e) => {
        e.stopPropagation();
        open(target);
      }}
      aria-label={n ? `${target.label}: ${n} hata bildirimi, gör ya da ekle` : `${target.label}: hata bildir`}
      title={n ? `${n} bildirim · gör / ekle` : 'Hata bildir'}
    >
      <Flag aria-hidden />
      {n > 0 && <span className="c">{n}</span>}
    </button>
  );
};

/* ---------------------------------------------------------------------------
 * Pencere: bu öğedeki bildirimler (kim, ne, neden) + oy + yeni bildirim formu
 * ------------------------------------------------------------------------- */
const timeAgo = (iso: string) => {
  const s = Math.max(1, (Date.now() - new Date(iso).getTime()) / 1000);
  if (s < 60) return 'az önce';
  if (s < 3600) return `${Math.floor(s / 60)} dk önce`;
  if (s < 86400) return `${Math.floor(s / 3600)} sa önce`;
  if (s < 86400 * 30) return `${Math.floor(s / 86400)} gün önce`;
  return new Date(iso).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short', year: 'numeric' });
};
const initials = (name: string) => name.split(/\s+/).filter(Boolean).slice(0, 2).map((w) => w[0]?.toLocaleUpperCase('tr-TR')).join('') || '?';
const hue = (s: string) => [...s].reduce((a, c) => (a * 31 + c.charCodeAt(0)) % 360, 7);

const ReportCard: React.FC<{ item: FeedbackItem; onChange: (f: FeedbackItem) => void }> = ({ item, onChange }) => {
  const [busy, setBusy] = useState(false);
  const vote = async (v: 1 | -1) => {
    if (busy) return;
    setBusy(true);
    const next = item.myVote === v ? 0 : v;
    try {
      onChange(await voteFeedback(item, next));
    } catch (e: any) {
      toast.error('Oy kaydedilemedi', e?.message);
    } finally {
      setBusy(false);
    }
  };
  return (
    <article className="ls-report">
      <header>
        <span className="ls-avatar" style={{ ['--h' as string]: hue(item.author.id) }} aria-hidden>{initials(item.author.name)}</span>
        <span className="who">
          <b>{item.author.name}{item.mine && <span className="ls-tag is-accent">sen</span>}</b>
          <small>{timeAgo(item.createdAt)}{item.local ? ' · yalnızca bu cihazda' : ''}</small>
          {item.location && <span className="ls-report-loc"><MapPin aria-hidden /> {item.location}</span>}
        </span>
      </header>
      <dl>
        <div className="is-field"><dt>Yanlış olan bilgi</dt><dd>{item.field}</dd></div>
        <div><dt>Neden yanlış</dt><dd>{item.reason}</dd></div>
      </dl>
      <footer>
        <button type="button" className={`ls-vote ${item.myVote === 1 ? 'is-up' : ''}`} onClick={() => vote(1)} disabled={item.mine || busy || item.local} aria-pressed={item.myVote === 1} title={item.mine ? 'Kendi bildirimine oy veremezsin' : 'Katılıyorum: bu bilgi gerçekten yanlış'}>
          <ThumbsUp aria-hidden /> <span>{item.up}</span><span className="sr-only"> katılıyor</span>
        </button>
        <button type="button" className={`ls-vote ${item.myVote === -1 ? 'is-down' : ''}`} onClick={() => vote(-1)} disabled={item.mine || busy || item.local} aria-pressed={item.myVote === -1} title={item.mine ? 'Kendi bildirimine oy veremezsin' : 'Katılmıyorum: bilgi doğru'}>
          <ThumbsDown aria-hidden /> <span>{item.down}</span><span className="sr-only"> katılmıyor</span>
        </button>
        {item.up + item.down > 0 && (
          <span className="ls-vote-bar" aria-hidden><i style={{ width: `${(item.up / (item.up + item.down)) * 100}%` }} /></span>
        )}
      </footer>
    </article>
  );
};

export const FeedbackDialog: React.FC<{
  deckId: string;
  deckTitle?: string;
  target: FeedbackTarget;
  items: FeedbackItem[];
  onClose: () => void;
  onAdd: (f: FeedbackItem) => void;
  onUpdate: (f: FeedbackItem) => void;
}> = ({ deckId, deckTitle, target, items, onClose, onAdd, onUpdate }) => {
  const sorted = useMemo(() => [...items].sort((a, b) => b.up - b.down - (a.up - a.down) || b.createdAt.localeCompare(a.createdAt)), [items]);
  const [writing, setWriting] = useState(items.length === 0);
  const [field, setField] = useState('');
  const [reason, setReason] = useState('');
  const [busy, setBusy] = useState(false);
  const ok = field.trim().length >= 3 && reason.trim().length >= 5;
  const submit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!ok || busy) return;
    setBusy(true);
    try {
      const item = await sendFeedback(deckId, target, field.trim(), reason.trim(), deckTitle);
      onAdd(item);
      setField('');
      setReason('');
      setWriting(false);
      toast.success(item.local ? 'Bildirim bu cihazda saklandı' : 'Bildirimin alındı', item.local ? 'Sunucuya şu an ulaşılamıyor; diğer öğrenciler henüz göremez.' : 'Diğer öğrenciler de görüp oylayabilir.');
    } catch (err: any) {
      toast.error('Bildirim gönderilemedi', err?.message);
    } finally {
      setBusy(false);
    }
  };
  return (
    <Dialog
      title={`Hata bildirimi · ${target.label}`}
      subtitle={`Adım ${target.slideNumber}${items.length ? ` · ${items.length} bildirim` : ''}`}
      onClose={onClose}
      width="max-w-lg"
      footer={
        writing ? (
          <>
            {items.length > 0 && <button type="button" className="ms-btn is-ghost mr-auto" onClick={() => setWriting(false)}>Vazgeç</button>}
            <button type="submit" form="ls-report-form" className="ms-btn is-primary" disabled={!ok || busy}>
              <Send /> {busy ? 'Gönderiliyor…' : 'Bildir'}
            </button>
          </>
        ) : (
          <>
            <button type="button" className="ms-btn is-ghost mr-auto" onClick={onClose}>Kapat</button>
            <button type="button" className="ms-btn is-primary" onClick={() => setWriting(true)}><Flag /> Yeni bildirim</button>
          </>
        )
      }
    >
      <div className="ls-report-wrap">
        {sorted.length > 0 && (
          <section className="ls-report-list" aria-label="Bu öğedeki bildirimler">
            {sorted.map((f) => <ReportCard key={f.id} item={f} onChange={onUpdate} />)}
          </section>
        )}
        {writing && (
          <form id="ls-report-form" className="ls-report-form" onSubmit={submit}>
            <p className="ls-hint"><span className="ls-report-loc"><MapPin aria-hidden /> {target.location || target.label}</span>{target.hint && <><br />Bildirdiğin öğe: <b>{target.hint}</b></>}</p>
            <label htmlFor="ls-report-field">
              <span>Hangi bilgi yanlış?</span>
              <textarea id="ls-report-field" rows={2} maxLength={600} value={field} onChange={(e) => setField(e.target.value)} placeholder="Örn. “Ekzom genomun %15'ini oluşturur” cümlesi" autoFocus />
            </label>
            <label htmlFor="ls-report-reason">
              <span>Neden yanlış? Doğrusu ne?</span>
              <textarea id="ls-report-reason" rows={4} maxLength={1500} value={reason} onChange={(e) => setReason(e.target.value)} placeholder="Doğru bilgiyi ve mümkünse kaynağını (kitap, slayt sayfası) yaz." />
              <small>{reason.length}/1500</small>
            </label>
          </form>
        )}
      </div>
    </Dialog>
  );
};
