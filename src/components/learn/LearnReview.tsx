/**
 * Tekrar ekranı (hata defteri): derste yanlış yapılan etkileşimler aralıklı tekrar kuyruğundan, karışık sırada
 * (farklı ders/adımlar iç içe) kendi bileşenleriyle yeniden oynatılır. Kayıt ve kutu mantığı services/learnReview.ts.
 *
 *  - "Bugün" vadesi gelenler; "Tüm hatalarım" öğrenilmemiş bütün ögeler (sınavdan önceki gece).
 *  - Kapsam: açıldığı ders ya da tüm dersler.
 *  - Her ögede kaynak satırı (ders · adım) ve "Kaynağa git": dersi o adımda açar.
 *  - Deste güncellenip öge değiştiyse (içerik özeti tutmuyor) öge sessizce defterden düşer.
 * Stil: styles/learn-focus.css (.lr-rv-*) + ders ekranının .ls-* sınıfları (ls-root kabuğu); v12 görünümü styles/v12/learn-library.css.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { BookOpenText, Check, ChevronLeft, ChevronRight, PartyPopper, RotateCcw } from 'lucide-react';
import { loadDeck } from '../../data/deckStore';
import { buildSteps, practiceOf, type PracticeItem } from './lesson/lessonModel';
import { PracticeCard } from './lesson/LessonBlocks';
import { dropEntry, dueEntries, itemSig, MASTER_BOX, openEntries, recordResult, type ReviewEntry } from '../../services/learnReview';
import '../../styles/learn-focus.css';
import '../../styles/learn-v10.css';
import '../../styles/v12/learn-library.css';

interface QItem { e: ReviewEntry; item: PracticeItem; stepTitle: string }
type Mode = 'due' | 'all';

const seeded = <T,>(a: T[], seed: number): T[] => {
  const out = [...a];
  let s = seed || 1;
  for (let i = out.length - 1; i > 0; i--) {
    s = (s * 9301 + 49297) % 233280;
    const j = Math.floor((s / 233280) * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
};
/** Karışık sıra ama aynı adımın ögeleri art arda gelmesin (iç içe tekrar) */
const interleave = (q: QItem[], seed: number) => {
  const s = seeded(q, seed);
  for (let i = 1; i < s.length; i++) {
    const same = (a: QItem, b: QItem) => a.e.deckId === b.e.deckId && a.e.slide === b.e.slide;
    if (same(s[i], s[i - 1])) {
      const k = s.findIndex((x, j) => j > i && !same(x, s[i - 1]));
      if (k > 0) [s[i], s[k]] = [s[k], s[i]];
    }
  }
  return s;
};

export const LearnReview: React.FC<{
  deckId?: string;
  onClose: () => void;
  onOpenSource: (deckId: string, slide: number) => void;
}> = ({ deckId, onClose, onOpenSource }) => {
  const [scope, setScope] = useState<string | undefined>(deckId);
  const [mode, setMode] = useState<Mode>(() => (dueEntries(Date.now(), deckId).length ? 'due' : 'all'));
  const [queue, setQueue] = useState<QItem[] | null>(null);
  const [pos, setPos] = useState(0);
  const [results, setResults] = useState<Record<number, boolean>>({});
  const [round, setRound] = useState(0);

  useEffect(() => {
    let alive = true;
    setQueue(null);
    setPos(0);
    setResults({});
    const list = mode === 'due' ? dueEntries(Date.now(), scope) : openEntries(scope);
    const ids = [...new Set(list.map((e) => e.deckId))];
    Promise.all(ids.map((id) => loadDeck<any>(id).then((d) => [id, d] as const).catch(() => [id, null] as const))).then((pairs) => {
      if (!alive) return;
      const steps = new Map(pairs.map(([id, d]) => [id, d && Array.isArray(d.slides) ? buildSteps(d) : null]));
      const q: QItem[] = [];
      for (const e of list) {
        const st = steps.get(e.deckId);
        if (!st) continue; // deste yüklenemedi (çevrimdışı): defterde kalsın
        const step = st.find((x) => x.number === e.slide);
        const item = step ? practiceOf(step)[e.ix] : undefined;
        if (!step || !item || itemSig(item) !== e.sig) {
          dropEntry(e.key);
          continue;
        }
        q.push({ e, item, stepTitle: step.title });
      }
      setQueue(interleave(q, Math.floor(Date.now() / 86_400_000) + round));
    });
    return () => {
      alive = false;
    };
  }, [mode, scope, round]);

  useEffect(() => {
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    const onKey = (ev: KeyboardEvent) => ev.key === 'Escape' && onClose();
    document.addEventListener('keydown', onKey);
    return () => {
      document.body.style.overflow = prev;
      document.removeEventListener('keydown', onKey);
    };
  }, [onClose]);

  const cur = queue?.[pos];
  const answered = cur ? pos in results : false;
  const doneN = Object.keys(results).length;
  const rightN = Object.values(results).filter(Boolean).length;
  const finished = queue != null && queue.length > 0 && pos >= queue.length;
  const counts = useMemo(() => ({ due: dueEntries(Date.now(), scope).length, all: openEntries(scope).length }), [scope, queue]); // eslint-disable-line react-hooks/exhaustive-deps
  const title = deckId && scope ? queue?.[0]?.e.deckTitle || 'Bu ders' : 'Tüm dersler';

  return (
    <div className="ls-root is-A" role="dialog" aria-modal="true" aria-label="Tekrar: hata defteri">
      <header className="ls-top lv-top lr-rv-top">
        <button type="button" className="ls-btn is-icon is-ghost" onClick={onClose} aria-label="Kapat" title="Kapat (Esc)"><ChevronLeft aria-hidden /></button>
        <div className="ttl">
          <small>Hata defteri · {title}</small>
          <b>Tekrar</b>
        </div>
        {queue && queue.length > 0 && !finished && <span className="ls-count">{pos + 1}<i>/</i>{queue.length}</span>}
        <div className="lv-top-prog" aria-hidden><i style={{ width: `${queue?.length ? (doneN / queue.length) * 100 : 0}%` }} /></div>
      </header>
      <main className="lr-rv-main">
        <div className="lr-rv-col">
          <div className="lr-rv-seg">
            <div className="ls-seg" role="radiogroup" aria-label="Kuyruk">
              <button type="button" role="radio" aria-checked={mode === 'due'} onClick={() => setMode('due')}>Bugün ({counts.due})</button>
              <button type="button" role="radio" aria-checked={mode === 'all'} onClick={() => setMode('all')}>Tüm hatalarım ({counts.all})</button>
            </div>
            {deckId && (
              <div className="ls-seg" role="radiogroup" aria-label="Kapsam">
                <button type="button" role="radio" aria-checked={scope === deckId} onClick={() => setScope(deckId)}>Bu ders</button>
                <button type="button" role="radio" aria-checked={!scope} onClick={() => setScope(undefined)}>Tüm dersler</button>
              </div>
            )}
          </div>

          {queue == null ? (
            <p className="ls-hint">Ögeler yükleniyor…</p>
          ) : queue.length === 0 ? (
            <div className="lr-rv-empty">
              <PartyPopper aria-hidden />
              <b>{mode === 'due' ? 'Bugün tekrar edilecek öge yok' : 'Hata defterin boş'}</b>
              <span>{mode === 'due' && counts.all > 0 ? `Defterde ${counts.all} öge var; vadeleri henüz gelmedi. İstersen "Tüm hatalarım" ile hepsini çöz.` : 'Derste yanlış yaptığın etkileşimler buraya düşer ve aralıklarla geri gelir.'}</span>
            </div>
          ) : finished ? (
            <div className="lr-rv-empty">
              <Check aria-hidden />
              <b>{rightN}/{queue.length} doğru</b>
              <span>Doğru yaptıkların daha uzun aralıkla geri gelecek; yanlışlar yarın yeniden karşına çıkacak.</span>
              <div className="lr-rv-nav">
                <button type="button" className="ls-btn" onClick={() => setRound((r) => r + 1)}><RotateCcw aria-hidden /> Yeniden başlat</button>
                <button type="button" className="ls-btn is-primary" onClick={onClose}>Kapat</button>
              </div>
            </div>
          ) : cur ? (
            <>
              <div className="lr-rv-src">
                <span><b>{cur.e.deckTitle}</b> · Adım {cur.e.slide} · {cur.stepTitle}</span>
                <span className="sp" />
                <span className="lr-rv-box">{cur.e.wrong} yanlış · kutu {Math.min(cur.e.box, MASTER_BOX)}/{MASTER_BOX}</span>
                <button type="button" className="ls-btn is-sm" onClick={() => onOpenSource(cur.e.deckId, cur.e.slide)}><BookOpenText aria-hidden /> Kaynağa git</button>
              </div>
              <PracticeCard
                key={`${round}:${pos}:${cur.e.key}`}
                item={cur.item}
                done={answered}
                onDone={(r) => {
                  if (!r) return setResults((m) => ({ ...m, [pos]: true }));
                  recordResult({ deckId: cur.e.deckId, deckTitle: cur.e.deckTitle, slide: cur.e.slide, stepTitle: cur.stepTitle, ix: cur.e.ix, item: cur.item, review: true }, r);
                  setResults((m) => ({ ...m, [pos]: r.ok }));
                }}
              />
              <div className="lr-rv-nav">
                {answered && (
                  <span className={`ls-tag ${results[pos] ? 'is-ok' : 'is-bad'}`}>{results[pos] ? 'Doğru · aralık uzadı' : 'Yanlış · yarın yine'}</span>
                )}
                <button type="button" className="ls-btn is-primary" onClick={() => setPos((p) => p + 1)}>
                  {answered ? 'Sonraki' : 'Atla'} <ChevronRight aria-hidden />
                </button>
              </div>
            </>
          ) : null}
        </div>
      </main>
    </div>
  );
};
