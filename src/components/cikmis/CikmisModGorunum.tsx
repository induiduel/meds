import React, { useEffect, useRef, useState } from 'react';
import { Bookmark, ChevronLeft, ChevronRight } from 'lucide-react';
import type { QuestionItem } from '../../types';
import type { AttemptRecord } from '../../services/studyStore';
import { disciplineClass, disciplineLabel } from '../../utils/discipline';
import '../../styles/v15/cikmisMod.css';

/**
 * Çıkmış sorular · C (yoğun tablo) ve D (tek soru odak) yerleşimleri (docs/tasarim/cikmis-alternatifler.html).
 * Süzme, durum, kaydetme PastExamsView'dendir; soru kartı `render` ile mevcut zengin kart olarak çizilir
 * (çözme/işaretleme/yorum mantığı değişmez).
 */
type Durum = 'n' | 'ok' | 'bad';
const durumOf = (a?: AttemptRecord): Durum => (!a ? 'n' : a.correct ? 'ok' : 'bad');
const DURUM_IS: Record<Durum, [string, string]> = { n: ['○', 'Çözülmedi'], ok: ['✓', 'Doğru'], bad: ['✗', 'Yanlış'] };
const kokOf = (q: QuestionItem) =>
  String((q as any).reconstruction?.stem || q.stem || (q as any).fragments?.[0]?.text || q.topic || '').replace(/\s+/g, ' ').trim();
const dersOf = (q: QuestionItem) => disciplineLabel(q.discipline) || q.discipline || 'Tıp';
const kunyeOf = (q: QuestionItem) => [q.examYear, q.questionNumber ? `S${q.questionNumber}` : ''].filter(Boolean).join(' · ');

interface Props {
  mod: 'tablo' | 'odak';
  sorular: QuestionItem[];
  attempts: Record<string, AttemptRecord>;
  savedIds: Set<string>;
  onToggleSave: (id: string) => void;
  render: (q: QuestionItem) => React.ReactNode;
  limit: number;
  onMore: () => void;
}

export const CikmisModGorunum: React.FC<Props> = (p) => (p.mod === 'tablo' ? <Tablo {...p} /> : <Odak {...p} />);

const Tablo: React.FC<Props> = ({ sorular, attempts, savedIds, onToggleSave, render, limit, onMore }) => {
  const [acik, setAcik] = useState<string | null>(null);
  const son = useRef<HTMLDivElement>(null);
  const gorunen = sorular.slice(0, limit);
  useEffect(() => {
    const el = son.current;
    if (!el || gorunen.length >= sorular.length || typeof IntersectionObserver === 'undefined') return;
    const io = new IntersectionObserver((e) => { if (e[0]?.isIntersecting) onMore(); }, { rootMargin: '600px' });
    io.observe(el);
    return () => io.disconnect();
  }, [gorunen.length, sorular.length, onMore]);
  return (
    <div className="cm15-tablo" role="list" aria-label="Sorular (tablo)">
      <div className="cm15-th" aria-hidden><span>Durum</span><span>Yıl · No</span><span>Ders</span><span>Soru</span><span /></div>
      {gorunen.map((q) => {
        const id = String(q.id);
        const d = durumOf(attempts[id]);
        const on = acik === id;
        const kayitli = savedIds.has(id);
        return (
          <div key={id} role="listitem" className={`cm15-satir ${on ? 'is-acik' : ''}`}>
            <div className="cm15-tr">
              <button type="button" className="cm15-trb" aria-expanded={on} onClick={() => setAcik(on ? null : id)}>
                <span className={`cm15-st is-${d}`} title={DURUM_IS[d][1]} aria-label={DURUM_IS[d][1]}>{DURUM_IS[d][0]}</span>
                <span className="cm15-yil">{kunyeOf(q)}</span>
                <span className={`cm15-ders ${disciplineClass(q.discipline)}`}><i className="cm15-dot" aria-hidden />{dersOf(q)}</span>
                <span className="cm15-kok">{kokOf(q)}</span>
              </button>
              <button type="button" className={`cm15-kaydet ${kayitli ? 'is-on' : ''}`} aria-pressed={kayitli} aria-label={kayitli ? 'Kayıttan çıkar' : 'Kaydet'} onClick={() => onToggleSave(id)}>
                <Bookmark aria-hidden />
              </button>
            </div>
            {on && <div className="cm15-ac">{render(q)}</div>}
          </div>
        );
      })}
      {gorunen.length < sorular.length && (
        <div ref={son} className="cm15-daha">
          <button type="button" className="c12-btn sm" onClick={onMore}>Daha fazla göster ({(sorular.length - gorunen.length).toLocaleString('tr-TR')})</button>
        </div>
      )}
    </div>
  );
};

const Odak: React.FC<Props> = ({ sorular, attempts, savedIds, onToggleSave, render }) => {
  const [i, setI] = useState(0);
  const ust = useRef<HTMLDivElement>(null);
  useEffect(() => { setI(0); }, [sorular]);
  const n = sorular.length;
  const idx = Math.min(i, Math.max(0, n - 1));
  const q = sorular[idx];
  const git = (k: number) => {
    setI(Math.max(0, Math.min(n - 1, k)));
    ust.current?.scrollIntoView({ block: 'nearest' });
  };
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      if (t?.closest?.('input, textarea, select, [contenteditable="true"]')) return;
      if (e.key === 'ArrowRight') git(idx + 1);
      else if (e.key === 'ArrowLeft') git(idx - 1);
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  });
  if (!q) return null;
  const cozulen = sorular.reduce((s, x) => s + (attempts[String(x.id)] ? 1 : 0), 0);
  const pct = n ? Math.round((cozulen / n) * 100) : 0;
  const id = String(q.id);
  const kayitli = savedIds.has(id);
  return (
    <div className="cm15-odak" ref={ust}>
      <div className="cm15-o-ana">
        <div className="cm15-o-ilerleme" aria-hidden><span style={{ width: `${n ? ((idx + 1) / n) * 100 : 0}%` }} /></div>
        <div className="cm15-o-kart" key={id}>{render(q)}</div>
        <nav className="cm15-o-alt" aria-label="Soru gezinme">
          <button type="button" className="c12-btn" onClick={() => git(idx - 1)} disabled={idx === 0}><ChevronLeft aria-hidden />Önceki</button>
          <span className="cm15-o-no"><b>{idx + 1}</b> / {n.toLocaleString('tr-TR')}</span>
          <button type="button" className={`c12-btn cm15-o-kay ${kayitli ? 'is-on' : ''}`} aria-pressed={kayitli} onClick={() => onToggleSave(id)} aria-label={kayitli ? 'Kayıttan çıkar' : 'Kaydet'}>
            <Bookmark aria-hidden /><span className="cm15-o-kl">{kayitli ? 'Kaydedildi' : 'Kaydet'}</span>
          </button>
          <button type="button" className="c12-btn pri" onClick={() => git(idx + 1)} disabled={idx >= n - 1}>Sonraki<ChevronRight aria-hidden /></button>
        </nav>
      </div>
      <aside className="cm15-o-yan" aria-label="İlerleme ve soru numaraları">
        <div className="cm15-halka" style={{ ['--p' as string]: `${pct}%` }} role="img" aria-label={`${cozulen} / ${n} çözüldü`}>
          <span>%{pct}</span>
        </div>
        <p className="cm15-o-ozet"><b>{cozulen.toLocaleString('tr-TR')}</b> / {n.toLocaleString('tr-TR')} çözüldü</p>
        <div className="cm15-izgara">
          {sorular.map((x, k) => {
            const d = durumOf(attempts[String(x.id)]);
            return (
              <button key={String(x.id)} type="button" className={`cm15-num is-${d} ${k === idx ? 'is-on' : ''}`} onClick={() => git(k)}
                aria-current={k === idx ? 'true' : undefined} title={`${kunyeOf(x)} · ${DURUM_IS[d][1]}`}>{k + 1}</button>
            );
          })}
        </div>
      </aside>
    </div>
  );
};
