/**
 * Öğren ortak katmanı (arayüz):
 *  - StepSocial: adımın altında herkese açık SPOT / ÖNEMLİ / VURGU notları, "Not ekle" formu ve adımdaki
 *    bildirilmiş metinlerin listesi. Ayrıca adım metninde bildirilen alıntının yanına kırmızı "!" düğmesi ekler,
 *    alıntıyı dalgalı kırmızı çizgiyle, metne bağlı notları türünün rengiyle işaretler (CSS Highlight API).
 *  - ReportSheet: seçili metni bildir (ilk mesajla tartışma açılır, yöneticiye bildirim gider).
 *  - ThreadSheet: bildirilen metin hakkında canlı sohbet.
 * Veri/bağlama: learnSocial.ts. Stil: styles/learn-v10.css (.ls-sx-*).
 */
import React, { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';
import { CheckCircle2, CircleAlert, Eye, EyeOff, MessageCircle, Plus, RotateCcw, Send, Trash2, X } from 'lucide-react';
import { Sheet } from '../../ui/Sheet';
import { toast } from '../../ui/Toast';
import type { LessonStep } from './lessonModel';
import { whoAmI } from './lessonFeedback';
import { useAppearance } from '../../../utils/appearance';
import {
  createNote, createThread, deleteMessage, deleteNote, findQuoteRange, flattenForSearch, loadThread, MESSAGE_MAX, NOTE_KINDS, NOTE_MAX,
  NoteKind, onSocialMessage, sendMessage, setThreadStatus, SocialMessage, SocialNote, SocialThread, useLearnSocial,
} from './learnSocial';

/* ---------------------------------------------------------------------------
 * Görünürlük tercihi (cihaz + profil eşitlemesi: medsoru_learn_social)
 * ------------------------------------------------------------------------- */
const SHOW_KEY = 'medsoru_learn_social';
const showListeners = new Set<() => void>();
let showState = (() => {
  try {
    return localStorage.getItem(SHOW_KEY) !== '0';
  } catch {
    return true;
  }
})();
export const setSocialVisible = (v: boolean) => {
  showState = v;
  try {
    localStorage.setItem(SHOW_KEY, v ? '1' : '0');
  } catch {
    /* yok */
  }
  showListeners.forEach((l) => l());
};
export const useSocialVisible = () => {
  const [v, setV] = useState(showState);
  useEffect(() => {
    const on = () => setV(showState);
    showListeners.add(on);
    return () => void showListeners.delete(on);
  }, []);
  return v;
};

/* ---------------------------------------------------------------------------
 * Bağlam
 * ------------------------------------------------------------------------- */
export interface ComposerReq { stepNumber: number; anchor: string; at: number }
export interface ReportReq { stepNumber: number; quote: string; prefix: string; suffix: string }
type Social = ReturnType<typeof useLearnSocial>;
interface Ctx {
  social: Social;
  deckId: string;
  deckTitle: string;
  visible: boolean;
  composer: ComposerReq | null;
  openComposer: (r: ComposerReq | null) => void;
  openThread: (id: string) => void;
}
const SocialCtx = createContext<Ctx | null>(null);
export const SocialProvider = SocialCtx.Provider;
const useSocial = () => useContext(SocialCtx);

const KIND_LABEL: Record<NoteKind, string> = { spot: 'SPOT', onemli: 'ÖNEMLİ', vurgu: 'VURGU' };

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
const short = (s: string, n = 90) => (s.length > n ? `${s.slice(0, n - 1)}…` : s);

/* ---------------------------------------------------------------------------
 * Metin içi işaretler: CSS Highlight (tüm adımlardan toplanır) + "!" düğmeleri
 * ------------------------------------------------------------------------- */
const HL_NAMES = ['ls-sx-report', 'ls-sx-spot', 'ls-sx-onemli', 'ls-sx-vurgu'] as const;
const hlByInstance = new Map<number, Partial<Record<(typeof HL_NAMES)[number], Range[]>>>();
let hlSeq = 0;
function repaintHighlights() {
  const reg = (globalThis as any).CSS?.highlights;
  const HL = (globalThis as any).Highlight;
  if (!reg || !HL) return;
  for (const name of HL_NAMES) {
    const all: Range[] = [];
    hlByInstance.forEach((m) => all.push(...(m[name] || [])));
    if (all.length) reg.set(name, new HL(...all));
    else reg.delete(name);
  }
}
const ALERT_SVG =
  '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>';

function useInlineMarks(sectionRef: React.RefObject<HTMLElement | null>, threads: SocialThread[], notes: SocialNote[], visible: boolean, onOpen: (id: string) => void) {
  const onOpenRef = useRef(onOpen);
  onOpenRef.current = onOpen;
  // Değişmeyen veride yeniden çizmemek için içerik imzası
  const sig = useMemo(
    () => JSON.stringify([threads.filter((t) => t.status === 'open').map((t) => [t.id, t.quote, t.prefix, t.suffix, t.messageCount]), visible ? notes.filter((n) => n.anchor).map((n) => [n.id, n.kind, n.anchor]) : []]),
    [threads, notes, visible]
  );
  useEffect(() => {
    const root = sectionRef.current?.parentElement?.querySelector<HTMLElement>(':scope > .ls-mark-layer .ls-content');
    if (!root) return;
    const id = ++hlSeq;
    const open = threads.filter((t) => t.status === 'open');
    const anchored = visible ? notes.filter((n) => n.anchor) : [];
    let obs: MutationObserver | null = null;
    let timer = 0;
    const paint = () => {
      obs?.disconnect();
      root.querySelectorAll('.ls-sx-flag').forEach((el) => {
        const island = el.closest('[data-ls-html]');
        el.remove();
        island?.normalize();
      });
      const flat = flattenForSearch(root);
      const hl: Partial<Record<(typeof HL_NAMES)[number], Range[]>> = {};
      const flags: { r: Range; t: SocialThread }[] = [];
      for (const t of open) {
        const r = findQuoteRange(root, t.quote, t.prefix, t.suffix, flat);
        if (!r) continue;
        (hl['ls-sx-report'] ||= []).push(r);
        flags.push({ r, t });
      }
      for (const n of anchored) {
        const r = findQuoteRange(root, n.anchor, '', '', flat);
        if (r) (hl[`ls-sx-${n.kind}` as const] ||= []).push(r);
      }
      // Belge sırasının tersine ekle: önceki aralıkların konumları kaymasın (aralıklar canlı da olsa güvenli)
      flags.sort((a, b) => b.r.compareBoundaryPoints(Range.END_TO_END, a.r));
      for (const { r, t } of flags) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'ls-sx-flag';
        btn.dataset.thread = t.id;
        btn.title = `Bildirilen metin · ${t.messageCount} mesaj — tartışmayı aç`;
        btn.setAttribute('aria-label', `Bildirilen metin: “${short(t.quote, 60)}” — ${t.messageCount} mesajlık tartışmayı aç`);
        btn.innerHTML = ALERT_SVG;
        const end = r.cloneRange();
        end.collapse(false);
        try {
          end.insertNode(btn);
        } catch {
          /* aralık geçersizleşti: bir sonraki çizimde yeniden denenir */
        }
      }
      hlByInstance.set(id, hl);
      repaintHighlights();
      obs?.takeRecords();
      obs?.observe(root, { childList: true, subtree: true, characterData: true });
    };
    // İçerik (terim sarmalama, canlı deste güncellemesi) değişince işaretleri yeniden kur
    obs = new MutationObserver(() => {
      window.clearTimeout(timer);
      timer = window.setTimeout(paint, 150);
    });
    const onClick = (e: MouseEvent) => {
      const b = (e.target as Element | null)?.closest?.('.ls-sx-flag') as HTMLElement | null;
      if (!b?.dataset.thread) return;
      e.preventDefault();
      e.stopPropagation();
      onOpenRef.current(b.dataset.thread);
    };
    root.addEventListener('click', onClick);
    // Prose/terim efektleri bitsin diye bir kare sonra
    const raf = requestAnimationFrame(paint);
    return () => {
      cancelAnimationFrame(raf);
      window.clearTimeout(timer);
      obs?.disconnect();
      root.removeEventListener('click', onClick);
      root.querySelectorAll('.ls-sx-flag').forEach((el) => {
        const island = el.closest('[data-ls-html]');
        el.remove();
        island?.normalize();
      });
      hlByInstance.delete(id);
      repaintHighlights();
    };
  }, [sig]); // eslint-disable-line react-hooks/exhaustive-deps
}

/* ---------------------------------------------------------------------------
 * Adımın ortak bölümü
 * ------------------------------------------------------------------------- */
export const StepSocial: React.FC<{ step: LessonStep }> = ({ step }) => {
  const ctx = useSocial();
  const ref = useRef<HTMLElement>(null);
  const num = step.number;
  const notes = useMemo(() => (ctx ? ctx.social.notes.filter((n) => n.stepNumber === num) : []), [ctx?.social.notes, num]); // eslint-disable-line react-hooks/exhaustive-deps
  const threads = useMemo(() => (ctx ? ctx.social.threads.filter((t) => t.stepNumber === num) : []), [ctx?.social.threads, num]); // eslint-disable-line react-hooks/exhaustive-deps
  useInlineMarks(ref, threads, notes, !!ctx?.visible, (id) => ctx?.openThread(id));
  if (!ctx) return null;
  const { visible, composer, openComposer, openThread, social } = ctx;
  const composing = composer && composer.stepNumber === num ? composer : null;
  const openThreads = threads.filter((t) => t.status === 'open');
  const resolved = threads.length - openThreads.length;
  const sorted = [...notes].sort((a, b) => NOTE_KINDS.findIndex((k) => k.id === a.kind) - NOTE_KINDS.findIndex((k) => k.id === b.kind) || a.createdAt.localeCompare(b.createdAt));

  return (
    <section ref={ref} className="ls-sx" aria-label="Ortak notlar ve bildirimler">
      <div className="ls-sx-h">
        <span className="ls-sx-title" title="Herkesin gördüğü notlar. Metin seçip “Not ekle” ya da “Bildir” de diyebilirsin.">Ortak notlar{notes.length > 0 && <small>{notes.length}</small>}</span>
        <span className="sp" />
        {notes.length > 0 && (
          <button type="button" className="ls-sx-iconbtn" onClick={() => setSocialVisible(!visible)} aria-pressed={!visible} title={visible ? 'Ortak notları gizle' : 'Ortak notları göster'} aria-label={visible ? 'Ortak notları gizle' : 'Ortak notları göster'}>
            {visible ? <EyeOff aria-hidden /> : <Eye aria-hidden />}
          </button>
        )}
        {!composing && (
          <button type="button" className="ls-sx-add" onClick={() => openComposer({ stepNumber: num, anchor: '', at: Date.now() })} disabled={social.offline}>
            <Plus aria-hidden /> Not ekle
          </button>
        )}
      </div>

      {composing && <NoteComposer req={composing} onDone={() => openComposer(null)} />}

      {visible && sorted.length > 0 && (
        <ul className="ls-sx-notes">
          {sorted.map((n) => <NoteCard key={n.id} note={n} onRemoved={social.removeNote} />)}
        </ul>
      )}
      {!visible && notes.length > 0 && (
        <button type="button" className="ls-sx-hidden" onClick={() => setSocialVisible(true)}>
          <EyeOff aria-hidden /> {notes.length} ortak not gizli · Göster
        </button>
      )}
      {social.offline && <p className="ls-sx-empty">Ortak notlara şu an ulaşılamıyor.</p>}

      {threads.length > 0 && (
        <div className="ls-sx-threads" aria-label="Bildirilen metinler">
          {openThreads.map((t) => (
            <button key={t.id} type="button" className="ls-sx-thread" onClick={() => openThread(t.id)}>
              <CircleAlert aria-hidden className="ic" />
              <span className="q">“{short(t.quote, 110)}”</span>
              <span className="c"><MessageCircle aria-hidden /> {t.messageCount}</span>
            </button>
          ))}
          {resolved > 0 && (
            <details className="ls-sx-resolved">
              <summary>{resolved} çözülmüş bildirim</summary>
              {threads.filter((t) => t.status === 'resolved').map((t) => (
                <button key={t.id} type="button" className="ls-sx-thread is-resolved" onClick={() => openThread(t.id)}>
                  <CheckCircle2 aria-hidden className="ic" />
                  <span className="q">“{short(t.quote, 110)}”</span>
                  <span className="c"><MessageCircle aria-hidden /> {t.messageCount}</span>
                </button>
              ))}
            </details>
          )}
        </div>
      )}
    </section>
  );
};

const NoteCard: React.FC<{ note: SocialNote; onRemoved: (id: string) => void }> = ({ note, onRemoved }) => {
  const [busy, setBusy] = useState(false);
  const remove = async () => {
    if (busy || !window.confirm('Bu not herkesten kaldırılsın mı?')) return;
    setBusy(true);
    try {
      await deleteNote(note.id);
      onRemoved(note.id);
    } catch (e: any) {
      toast.error('Not silinemedi', e?.message);
      setBusy(false);
    }
  };
  return (
    <li className={`ls-sx-note is-${note.kind}`}>
      <div className="top">
        <span className={`ls-sx-badge is-${note.kind}`}>{KIND_LABEL[note.kind]}</span>
        <span className="who">{note.author.name}{note.mine && <em> · sen</em>} · {timeAgo(note.createdAt)}</span>
        {note.canDelete && (
          <button type="button" className="ls-sx-iconbtn is-del" onClick={remove} disabled={busy} aria-label="Notu sil" title={note.mine ? 'Notunu sil' : 'Notu sil (yönetici)'}>
            <Trash2 aria-hidden />
          </button>
        )}
      </div>
      {note.anchor && <blockquote className="ls-sx-anchor">“{short(note.anchor, 160)}”</blockquote>}
      <p className="body">{note.body}</p>
    </li>
  );
};

const NoteComposer: React.FC<{ req: ComposerReq; onDone: () => void }> = ({ req, onDone }) => {
  const ctx = useSocial()!;
  const [kind, setKind] = useState<NoteKind>('spot');
  const [body, setBody] = useState('');
  const [anchor, setAnchor] = useState(req.anchor);
  // v12 (canvas sn-compose): tür seçici cümle düzeninde segment (Spot · Önemli · Vurgu), renk noktası CSS'ten
  const v12 = useAppearance().design === 'v12';
  const [busy, setBusy] = useState(false);
  const formRef = useRef<HTMLFormElement>(null);
  const taRef = useRef<HTMLTextAreaElement>(null);
  useEffect(() => {
    setAnchor(req.anchor);
    const t = window.setTimeout(() => {
      formRef.current?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      taRef.current?.focus({ preventScroll: true });
    }, 60);
    return () => window.clearTimeout(t);
  }, [req.at]); // eslint-disable-line react-hooks/exhaustive-deps
  const text = body.trim();
  const ok = text.length >= 3 && text.length <= NOTE_MAX;
  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ok || busy) return;
    setBusy(true);
    try {
      const n = await createNote(ctx.deckId, req.stepNumber, kind, text, anchor);
      ctx.social.upsertNote(n);
      if (!ctx.visible) setSocialVisible(true);
      toast.success('Not paylaşıldı', 'Bu dersi açan herkes görebilir.');
      onDone();
    } catch (err: any) {
      toast.error('Not paylaşılamadı', err?.message);
      setBusy(false);
    }
  };
  return (
    <form ref={formRef} className="ls-sx-form" onSubmit={submit} onKeyDown={(e) => e.key === 'Escape' && (e.stopPropagation(), onDone())}>
      <div className="ls-sx-kinds" role="radiogroup" aria-label="Not türü">
        {NOTE_KINDS.map((k) => (
          <button key={k.id} type="button" role="radio" aria-checked={kind === k.id} className={`ls-sx-badge is-${k.id} ${kind === k.id ? 'is-on' : ''}`} onClick={() => setKind(k.id)} title={k.hint}>
            {v12 ? k.label.charAt(0) + k.label.slice(1).toLocaleLowerCase('tr-TR') : k.label}
          </button>
        ))}
      </div>
      {anchor && (
        <div className="ls-sx-anchor-row">
          <blockquote className="ls-sx-anchor">“{short(anchor, 160)}”</blockquote>
          <button type="button" className="ls-sx-iconbtn" onClick={() => setAnchor('')} aria-label="Seçili metin bağını kaldır" title="Metin bağını kaldır"><X aria-hidden /></button>
        </div>
      )}
      <textarea
        ref={taRef}
        rows={3}
        maxLength={NOTE_MAX}
        value={body}
        onChange={(e) => setBody(e.target.value)}
        placeholder={NOTE_KINDS.find((k) => k.id === kind)?.hint + ' — herkesin göreceği notunu yaz'}
        aria-label="Not metni"
        onKeyDown={(e) => {
          if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) void submit(e as unknown as React.FormEvent);
        }}
      />
      <div className="ls-sx-form-f">
        <small>{whoAmI().name} olarak herkese açık · {body.length}/{NOTE_MAX}</small>
        <span className="sp" />
        <button type="button" className="ms-btn is-ghost" onClick={onDone}>Vazgeç</button>
        <button type="submit" className="ms-btn is-primary" disabled={!ok || busy}><Send aria-hidden /> {busy ? 'Paylaşılıyor…' : 'Paylaş'}</button>
      </div>
    </form>
  );
};

/* ---------------------------------------------------------------------------
 * Bildir penceresi (seçili metin → tartışma)
 * ------------------------------------------------------------------------- */
export const ReportSheet: React.FC<{ req: ReportReq | null; onClose: () => void; onCreated: (t: SocialThread) => void }> = ({ req, onClose, onCreated }) => {
  const ctx = useSocial();
  const [body, setBody] = useState('');
  const [busy, setBusy] = useState(false);
  useEffect(() => {
    if (req) setBody('');
  }, [req]);
  const ok = body.trim().length >= 5;
  const submit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!req || !ctx || !ok || busy) return;
    setBusy(true);
    try {
      const { item, created } = await createThread({ deckId: ctx.deckId, deckTitle: ctx.deckTitle, stepNumber: req.stepNumber, quote: req.quote, prefix: req.prefix, suffix: req.suffix, body: body.trim() });
      ctx.social.upsertThread(item);
      toast.success(created ? 'Metin bildirildi' : 'Mesajın mevcut tartışmaya eklendi', 'Herkes metnin yanında kırmızı işareti görür; tartışma açıldı.');
      onCreated(item);
    } catch (err: any) {
      toast.error('Bildirilemedi', err?.message);
    } finally {
      setBusy(false);
    }
  };
  return (
    <Sheet
      open={!!req}
      onClose={onClose}
      title="Metni bildir"
      subtitle={req ? `Adım ${req.stepNumber} · herkes görebilir, yöneticiye de iletilir` : undefined}
      width={520}
      footer={
        <>
          <button type="button" className="ms-btn is-ghost mr-auto" onClick={onClose}>Vazgeç</button>
          <button type="submit" form="ls-sx-report" className="ms-btn is-primary" disabled={!ok || busy}><Send aria-hidden /> {busy ? 'Gönderiliyor…' : 'Bildir'}</button>
        </>
      }
    >
      {req && (
        <form id="ls-sx-report" className="ls-sx-sheet" onSubmit={submit}>
          <blockquote className="ls-sx-quote"><CircleAlert aria-hidden /> <span>“{req.quote}”</span></blockquote>
          <label className="ls-sx-label" htmlFor="ls-sx-report-body">Bu metinde ne yanlış ya da belirsiz?</label>
          <textarea
            id="ls-sx-report-body"
            className="ls-sx-ta"
            rows={4}
            maxLength={MESSAGE_MAX}
            value={body}
            onChange={(e) => setBody(e.target.value)}
            placeholder="Örn. “Bu oran slaytta %15 değil %1,5” — doğrusunu ve kaynağını yazarsan tartışma hızlanır."
            autoFocus
          />
          <small className="ls-sx-count">{whoAmI().name} olarak · {body.length}/{MESSAGE_MAX}</small>
        </form>
      )}
    </Sheet>
  );
};

/* ---------------------------------------------------------------------------
 * Tartışma penceresi
 * ------------------------------------------------------------------------- */
export const ThreadSheet: React.FC<{ threadId: string | null; onClose: () => void; onJump?: (stepNumber: number) => void }> = ({ threadId, onClose, onJump }) => {
  const ctx = useSocial();
  const [thread, setThread] = useState<SocialThread | null>(null);
  const [messages, setMessages] = useState<SocialMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [text, setText] = useState('');
  const [busy, setBusy] = useState(false);
  const listRef = useRef<HTMLDivElement>(null);
  const me = whoAmI().id;
  const isAdmin = !!ctx?.social.isAdmin;
  const live = ctx?.social.threads.find((t) => t.id === threadId) || thread;

  const scrollEnd = useCallback(() => requestAnimationFrame(() => listRef.current?.scrollTo({ top: listRef.current.scrollHeight })), []);
  useEffect(() => {
    if (!threadId) return;
    let alive = true;
    setLoading(true);
    setThread(null);
    setMessages([]);
    setText('');
    loadThread(threadId)
      .then((r) => {
        if (!alive) return;
        setThread(r.item);
        setMessages(r.messages);
        scrollEnd();
      })
      .catch((e) => alive && toast.error('Tartışma açılamadı', e?.message))
      .finally(() => alive && setLoading(false));
    const off = onSocialMessage((e) => {
      if (e.threadId !== threadId) return;
      if (e.op === 'delete') setMessages((l) => l.filter((m) => m.id !== e.id));
      else if (e.item) {
        const m = e.item as SocialMessage;
        const mine = m.author.id === me;
        setMessages((l) => (l.some((x) => x.id === m.id) ? l : [...l, { ...m, mine, canDelete: mine || isAdmin }]));
        scrollEnd();
      }
    });
    return () => {
      alive = false;
      off();
    };
  }, [threadId]); // eslint-disable-line react-hooks/exhaustive-deps

  const send = async (e?: React.FormEvent) => {
    e?.preventDefault();
    const body = text.trim();
    if (!threadId || !body || busy) return;
    setBusy(true);
    try {
      const m = await sendMessage(threadId, body);
      setMessages((l) => (l.some((x) => x.id === m.id) ? l : [...l, m]));
      setText('');
      scrollEnd();
    } catch (err: any) {
      toast.error('Mesaj gönderilemedi', err?.message);
    } finally {
      setBusy(false);
    }
  };
  const remove = async (m: SocialMessage) => {
    if (!window.confirm('Bu mesaj silinsin mi?')) return;
    try {
      await deleteMessage(m.id);
      setMessages((l) => l.filter((x) => x.id !== m.id));
    } catch (err: any) {
      toast.error('Mesaj silinemedi', err?.message);
    }
  };
  const toggleStatus = async () => {
    if (!live) return;
    try {
      const t = await setThreadStatus(live.id, live.status === 'open' ? 'resolved' : 'open');
      setThread(t);
      ctx?.social.upsertThread(t);
      toast.success(t.status === 'resolved' ? 'Bildirim çözüldü olarak işaretlendi' : 'Bildirim yeniden açıldı');
    } catch (err: any) {
      toast.error('Durum değiştirilemedi', err?.message);
    }
  };
  const canResolve = !!live && (isAdmin || live.reporter.id === me);

  return (
    <Sheet
      open={!!threadId}
      onClose={onClose}
      title="Bildirilen metin"
      subtitle={live ? `Adım ${live.stepNumber} · ${live.reporter.name} bildirdi · ${timeAgo(live.createdAt)}` : 'Yükleniyor…'}
      size="full"
      width={560}
      actions={
        canResolve && live ? (
          <button type="button" className="ms-btn is-ghost" onClick={toggleStatus} title={live.status === 'open' ? 'Sorun giderildiyse kapat' : 'Yeniden aç'}>
            {live.status === 'open' ? <><CheckCircle2 aria-hidden /> Çözüldü</> : <><RotateCcw aria-hidden /> Yeniden aç</>}
          </button>
        ) : undefined
      }
      footer={
        <form className="ls-sx-compose" onSubmit={send}>
          <textarea
            className="ls-sx-ta"
            rows={1}
            maxLength={MESSAGE_MAX}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey && !e.nativeEvent.isComposing) {
                e.preventDefault();
                void send();
              }
            }}
            placeholder="Bu metin hakkında yaz… (Enter gönderir, Shift+Enter yeni satır)"
            aria-label="Mesaj"
          />
          <button type="submit" className="ms-btn is-primary" disabled={!text.trim() || busy} aria-label="Gönder"><Send aria-hidden /></button>
        </form>
      }
    >
      {live && (
        <div className="ls-sx-sheet">
          <blockquote className={`ls-sx-quote ${live.status === 'resolved' ? 'is-resolved' : ''}`}>
            {live.status === 'resolved' ? <CheckCircle2 aria-hidden /> : <CircleAlert aria-hidden />}
            <span>{live.prefix && <span className="ctx">…{short(live.prefix, 50).slice(-50)} </span>}<b>“{live.quote}”</b>{live.suffix && <span className="ctx"> {short(live.suffix, 50)}…</span>}</span>
          </blockquote>
          <div className="ls-sx-meta">
            <span className={`ls-sx-status is-${live.status}`}>{live.status === 'open' ? 'Açık' : 'Çözüldü'}</span>
            {onJump && <button type="button" className="ls-sx-link" onClick={() => onJump(live.stepNumber)}>Metne git</button>}
          </div>
          <div className="ls-sx-msgs" ref={listRef} aria-live="polite">
            {loading && <p className="ls-sx-empty">Yükleniyor…</p>}
            {!loading && messages.length === 0 && <p className="ls-sx-empty">Henüz mesaj yok.</p>}
            {messages.map((m) => (
              <article key={m.id} className={`ls-sx-msg ${m.mine ? 'is-mine' : ''}`}>
                <span className="ls-avatar" style={{ ['--h' as string]: hue(m.author.id) }} aria-hidden>{initials(m.author.name)}</span>
                <div className="bubble">
                  <header>
                    <b>{m.author.name}</b>
                    {m.isAdmin && <span className="ls-tag is-accent">Yönetici</span>}
                    <small>{timeAgo(m.createdAt)}</small>
                    {(m.canDelete || m.mine || isAdmin) && (
                      <button type="button" className="ls-sx-iconbtn is-del" onClick={() => remove(m)} aria-label="Mesajı sil"><Trash2 aria-hidden /></button>
                    )}
                  </header>
                  <p>{m.body}</p>
                </div>
              </article>
            ))}
          </div>
        </div>
      )}
    </Sheet>
  );
};
