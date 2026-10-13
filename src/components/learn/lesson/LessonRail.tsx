/**
 * v10 slayt rayı (canvas "Slayt-Masaustu"): numaralı adımlar düz liste, bölüm adları ara başlık.
 * Numara karosu durumu taşır: tekrar (checkpoint) turuncu, biten yeşil, güncel dolu vurgu.
 * Masaüstünde (≥1024) sol ray, telefon/tablette Sheet içinde aynı liste.
 */
import React, { useEffect, useRef, useState } from 'react';
import { Check, Search, X } from 'lucide-react';
import type { LessonSection, LessonStep } from './lessonModel';

export const LessonRail: React.FC<{
  steps: LessonStep[];
  sections: LessonSection[];
  current: number;
  done: Set<number>;
  onPick: (i: number) => void;
}> = ({ steps, sections, current, done, onPick }) => {
  const [q, setQ] = useState('');
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
          return (
            <div key={sec.index} className="lr-sec" role="group" aria-label={`Bölüm ${sec.index + 1}: ${sec.name}`}>
              {showSections && (
                <div className="lr-sec-h">
                  <span>{sec.name}</span>
                  <small>{doneN}/{sec.steps.length}</small>
                </div>
              )}
              {items.map((i) => {
                const s = steps[i];
                const isDone = done.has(s.number);
                const isCur = i === current;
                const cp = s.checkpoint > 0;
                const game = s.game;
                return (
                  <button
                    key={i}
                    type="button"
                    className={`lr-item ${isCur ? 'is-cur' : ''} ${isDone ? 'is-done' : ''} ${cp ? 'is-cp' : ''} ${game ? 'is-game' : ''}`}
                    aria-current={isCur ? 'step' : undefined}
                    onClick={() => onPick(i)}
                    title={s.title}
                  >
                    <span className="lr-no" aria-hidden>{isDone && !isCur && !cp ? <Check /> : s.number}</span>
                    <span className="lr-tx">
                      {cp ? `Tekrar · ${s.topic}` : game ? `Oyun · ${s.topic}` : s.topic}
                    </span>
                    <span className="sr-only">{isDone ? ' (tamamlandı)' : ''}{cp ? ' (tekrar sayfası)' : ''}{game ? ' (ders sonu oyunları)' : ''}</span>
                  </button>
                );
              })}
            </div>
          );
        })}
      </div>
    </div>
  );
};
