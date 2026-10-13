/**
 * v10 slayt rayı (canvas "Slayt-Masaustu"): numaralı adımlar düz liste, bölüm adları ara başlık.
 * Numara karosu durumu taşır: tekrar (checkpoint) turuncu, biten yeşil, güncel dolu vurgu.
 * Masaüstünde (≥1024) sol ray, telefon/tablette Sheet içinde aynı liste.
 */
import React, { useEffect, useRef, useState } from 'react';
import { Check, ChevronRight, Search, X } from 'lucide-react';
import { useAppearance } from '../../../utils/appearance';
import type { LessonSection, LessonStep } from './lessonModel';

export const LessonRail: React.FC<{
  steps: LessonStep[];
  sections: LessonSection[];
  current: number;
  done: Set<number>;
  onPick: (i: number) => void;
}> = ({ steps, sections, current, done, onPick }) => {
  const [q, setQ] = useState('');
  // v12: bölümler katlanır (güncel adımın bölümü hep açık); slaytta isteğe bağlı `altBaslik` alt başlık çizer
  const v12 = useAppearance().design === 'v12';
  const [shut, setShut] = useState<Record<number, boolean>>({});
  const listRef = useRef<HTMLDivElement>(null);
  // Güncel adım görünür alanda kalsın (yalnız rayın kendi kaydırıcısı kayar)
  useEffect(() => {
    const box = listRef.current;
    const el = box?.querySelector<HTMLElement>('[aria-current="step"]');
    if (!box || !el) return;
    const top = el.offsetTop - box.offsetTop;
    if (top < box.scrollTop || top + el.offsetHeight > box.scrollTop + box.clientHeight) {
      box.scrollTo({ top: Math.max(0, top - box.clientHeight / 3) });
    }
  }, [current]);
  const nq = q.trim().toLocaleLowerCase('tr-TR');
  const showSections = sections.length > 1;
  return (
    <div className="lr">
      <label className="lr-search">
        <Search aria-hidden />
        <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Slaytlarda ara" aria-label="Slaytlarda ara" />
        {q && <button type="button" onClick={() => setQ('')} aria-label="Aramayı temizle"><X aria-hidden /></button>}
      </label>
      <div className="lr-list" ref={listRef}>
        {sections.map((sec) => {
          const items = sec.steps.filter((i) => !nq || steps[i].title.toLocaleLowerCase('tr-TR').includes(nq));
          if (!items.length) return null;
          const doneN = sec.steps.filter((i) => done.has(steps[i].number)).length;
          const hasCur = sec.steps.includes(current);
          const closed = v12 && showSections && !nq && !hasCur && !!shut[sec.index];
          let lastSub = '';
          return (
            <div key={sec.index} className="lr-sec" role="group" aria-label={`Bölüm ${sec.index + 1}: ${sec.name}`}>
              {showSections && (v12 ? (
                <button type="button" className={`lr-sec-h is-btn ${closed ? '' : 'is-open'}`} aria-expanded={!closed} disabled={hasCur || !!nq}
                  onClick={() => setShut((m) => ({ ...m, [sec.index]: !m[sec.index] }))}>
                  <ChevronRight aria-hidden className="lr-chev" />
                  <span>{sec.name}</span>
                  <small>{doneN}/{sec.steps.length}</small>
                </button>
              ) : (
                <div className="lr-sec-h">
                  <span>{sec.name}</span>
                  <small>{doneN}/{sec.steps.length}</small>
                </div>
              ))}
              {!closed && items.map((i) => {
                const s = steps[i];
                const sub = v12 ? String((s.slide as { altBaslik?: string }).altBaslik || '').trim() : '';
                const subHead = sub && sub !== lastSub ? sub : '';
                if (sub) lastSub = sub;
                const isDone = done.has(s.number);
                const isCur = i === current;
                const cp = s.checkpoint > 0;
                const game = s.game;
                return (
                  <React.Fragment key={i}>
                  {subHead && <div className="lr-sub" aria-hidden="true">{subHead}</div>}
                  <button
                    type="button"
                    className={`lr-item ${isCur ? 'is-cur' : ''} ${isDone ? 'is-done' : ''} ${cp ? 'is-cp' : ''} ${game ? 'is-game' : ''} ${sub ? 'is-sub' : ''}`}
                    aria-current={isCur ? 'step' : undefined}
                    onClick={() => onPick(i)}
                    title={s.title}
                  >
                    <span className="lr-no" aria-hidden>{isDone && !isCur && !cp ? <Check /> : s.number}</span>
                    <span className="lr-tx">
                      {cp ? `Tekrar · ${s.topic}` : game ? `Oyun · ${s.topic}` : s.topic}
                    </span>
                    <span className="sr-only">{sub ? ` (${sub})` : ''}{isDone ? ' (tamamlandı)' : ''}{cp ? ' (tekrar sayfası)' : ''}{game ? ' (ders sonu oyunları)' : ''}</span>
                  </button>
                  </React.Fragment>
                );
              })}
            </div>
          );
        })}
      </div>
    </div>
  );
};
