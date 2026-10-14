import React, { useEffect, useId, useMemo, useState } from 'react';
import { ArrowRight, Plus } from 'lucide-react';
import { PageToolbar } from './ui/PageToolbar';
import { Sheet } from './ui/Sheet';
import { committeeShortLabel, questionStemText } from './QuickAddHero';
import type { Committee, QuestionItem } from '../types';
import '../styles/matrix.css';
import '../styles/v12/secondary.css';

/**
 * Soru haritası (v10): kurul sınavının 1–N numaralı her sorusu bir kutu.
 *  - Tam = kök + 5 şık, Eksik = parça/şık var ama tamamlanmamış, Boş = henüz kimse girmedi.
 *  - Kutuya basınca ayrıntı açılır: masaüstünde sağ panel (300 px), tablet/Akış'ta ızgaranın altında, telefonda alt sayfa.
 *  - Ayrıntıdan "Soruyu aç" (havuzda o numara) ve "Şık ekle / Parça ekle" (katkı penceresi o numarayla) çağrılır.
 * Stil: styles/matrix.css (.qm-*).
 */
interface QuestionMatrixProps {
  questions: QuestionItem[];
  targetCount: number;
  committee?: Committee;
  onSelectQuestion: (question: QuestionItem) => void;
  onAddContributionForNumber: (questionNumber: number) => void;
}

type CellState = 'full' | 'part' | 'empty';
interface Cell {
  n: number;
  q?: QuestionItem;
  state: CellState;
  hasStem: boolean;
  optCount: number;
  contributors: number;
}

const KEYS = ['A', 'B', 'C', 'D', 'E'];
// "Şık A" gibi yer tutucu metinler dolu şık sayılmaz (studyStore ile aynı kural)
const isRealOption = (o: { key?: string; text?: string } | undefined) =>
  !!o && KEYS.includes(String(o.key || '').trim().toUpperCase()) && !!String(o.text || '').trim() && !/^(şık\s*)?[a-e][).]?$/i.test(String(o.text).trim());

const analyze = (q: QuestionItem): Omit<Cell, 'n' | 'q'> => {
  const hasStem = !!(q.reconstruction?.stem?.trim() || q.rawStem?.trim() || q.fragments?.some((f) => f.type === 'stem' && f.text.trim()));
  const keys = new Set<string>();
  for (const o of q.reconstruction?.options || []) if (isRealOption(o)) keys.add(o.key);
  for (const o of q.options || []) if (isRealOption(o)) keys.add(o.key);
  const optCount = keys.size;
  const people = new Set<string>();
  for (const f of q.fragments || []) if (f.authorUid || f.author) people.add(f.authorUid || f.author);
  for (const o of q.options || []) if (o.suggestedByUid || o.suggestedBy) people.add(String(o.suggestedByUid || o.suggestedBy));
  if (q.contributedByUid || q.contributedByName) people.add(String(q.contributedByUid || q.contributedByName));
  const any = hasStem || optCount > 0 || (q.fragments?.length || 0) > 0 || !!q.reconstruction;
  const state: CellState = hasStem && optCount >= 5 ? 'full' : any ? 'part' : 'empty';
  return { hasStem, optCount, contributors: people.size, state };
};

const RANK: Record<CellState, number> = { full: 2, part: 1, empty: 0 };

/** Telefon kırılımı (<768): ayrıntı alt sayfada açılır */
const usePhone = () => {
  const q = '(max-width: 767px)';
  const [m, setM] = useState(() => typeof window !== 'undefined' && !!window.matchMedia?.(q).matches);
  useEffect(() => {
    const mq = window.matchMedia?.(q);
    if (!mq) return;
    const on = () => setM(mq.matches);
    on();
    mq.addEventListener?.('change', on);
    return () => mq.removeEventListener?.('change', on);
  }, []);
  return m;
};

export const QuestionMatrix: React.FC<QuestionMatrixProps> = ({
  questions,
  targetCount,
  committee,
  onSelectQuestion,
  onAddContributionForNumber,
}) => {
  const phone = usePhone();
  const detailId = useId();
  const [selected, setSelected] = useState<number | null>(null);

  // Her numara için en dolu kayıt (aynı numarada birden çok taslak olabilir)
  const cells = useMemo<Cell[]>(() => {
    const best = new Map<number, { q: QuestionItem; a: Omit<Cell, 'n' | 'q'> }>();
    for (const q of questions) {
      if (q.isUnassignedNumber || !(q.questionNumber >= 1 && q.questionNumber <= targetCount)) continue;
      const a = analyze(q);
      const prev = best.get(q.questionNumber);
      if (!prev || RANK[a.state] > RANK[prev.a.state] || (RANK[a.state] === RANK[prev.a.state] && a.optCount > prev.a.optCount)) {
        best.set(q.questionNumber, { q, a });
      }
    }
    return Array.from({ length: targetCount }, (_, i) => {
      const n = i + 1;
      const b = best.get(n);
      return b ? { n, q: b.q, ...b.a } : { n, state: 'empty' as const, hasStem: false, optCount: 0, contributors: 0 };
    });
  }, [questions, targetCount]);

  const counts = useMemo(() => {
    const c = { full: 0, part: 0, empty: 0 };
    for (const x of cells) c[x.state]++;
    return c;
  }, [cells]);
  const filled = counts.full + counts.part;
  const pct = (v: number) => (targetCount ? (v / targetCount) * 100 : 0);

  const cell = selected != null ? cells[selected - 1] : undefined;

  const subLine = [
    committee ? committeeShortLabel(committee) : null,
    committee?.academicYear ? `${committee.academicYear} sınavı` : committee?.year ? `${committee.year} sınavı` : null,
    `${targetCount} soru`,
  ].filter(Boolean).join(' · ');

  const stateLabel: Record<CellState, string> = { full: 'tam', part: 'eksik', empty: 'boş' };

  const detail = cell ? (
    <MatrixDetail
      cell={cell}
      onOpen={(q) => onSelectQuestion(q)}
      onAdd={(n) => onAddContributionForNumber(n)}
    />
  ) : null;

  return (
    <div className="qm o12-page o12-qm">
      <PageToolbar title="Soru haritası" count={`${filled} / ${targetCount} dolu`}>
        <p className="qm-sub">{subLine}</p>
      </PageToolbar>

      <div className={`qm-body ${!phone ? 'has-detail' : ''}`}>
        <div className="qm-main">
          <div
            className="qm-bar"
            role="img"
            aria-label={`${counts.full} tam, ${counts.part} eksik, ${counts.empty} boş`}
          >
            <span className="is-full" style={{ width: `${pct(counts.full)}%` }} />
            <span className="is-part" style={{ width: `${pct(counts.part)}%` }} />
          </div>

          <div className="qm-grid" role="group" aria-label={`Soru numaraları 1–${targetCount}`}>
            {cells.map((c) => (
              <button
                key={c.n}
                type="button"
                className={`qm-cell is-${c.state} ${selected === c.n ? 'is-sel' : ''}`}
                aria-pressed={selected === c.n}
                aria-controls={phone ? undefined : detailId}
                aria-haspopup={phone ? 'dialog' : undefined}
                aria-label={`Soru ${c.n} ${stateLabel[c.state]}`}
                title={c.q ? `Soru ${c.n} · ${c.q.discipline || ''}${c.q.topic ? ` · ${c.q.topic}` : ''}` : `Soru ${c.n}: henüz kimse girmedi`}
                onClick={() => setSelected((s) => (s === c.n && !phone ? null : c.n))}
              >
                {c.n}
              </button>
            ))}
          </div>

          <ul className="qm-legend" aria-label="Renk açıklaması">
            <li><i className="is-full" aria-hidden />Tam (kök + 5 şık) <b>{counts.full}</b></li>
            <li><i className="is-part" aria-hidden />Eksik <b>{counts.part}</b></li>
            <li><i className="is-empty" aria-hidden />Boş <b>{counts.empty}</b></li>
          </ul>
        </div>

        {!phone && (
          <aside id={detailId} className="qm-side" aria-live="polite">
            {detail || (
              <div className="qm-hint">
                <strong>Bir numara seç</strong>
                <span>Kutuya basınca o sorunun kökünü, şık sayısını ve katkı verenleri burada görürsün. Boş kutulara hatırladığın parçayı ekleyebilirsin.</span>
              </div>
            )}
          </aside>
        )}
      </div>

      {phone && (
        <Sheet open={!!cell} onClose={() => setSelected(null)} title={cell ? `Soru ${cell.n}` : undefined} size="auto">
          {detail}
        </Sheet>
      )}
    </div>
  );
};

const MatrixDetail: React.FC<{ cell: Cell; onOpen: (q: QuestionItem) => void; onAdd: (n: number) => void }> = ({ cell, onOpen, onAdd }) => {
  const { q, n, state } = cell;
  if (!q || state === 'empty') {
    return (
      <div className="qm-detail">
        <span className="qm-meta">Soru {n}</span>
        <strong className="qm-stem is-empty">Bu soruyu henüz kimse girmedi.</strong>
        <span className="qm-note">Sınavdaki {n}. soruyu hatırlıyorsan kökünden ya da bir şıkkından başlayabilirsin.</span>
        <button type="button" className="ui-btn is-primary qm-act" onClick={() => onAdd(n)}>
          <Plus aria-hidden /> Bu soruyu ekle
        </button>
      </div>
    );
  }
  const stem = questionStemText(q);
  const missing = Math.max(0, 5 - cell.optCount);
  return (
    <div className="qm-detail">
      <span className="qm-meta">Soru {n}{q.discipline ? ` · ${q.discipline}` : ''}{q.topic ? ` · ${q.topic}` : ''}</span>
      <strong className={`qm-stem ${cell.hasStem ? '' : 'is-empty'}`}>{cell.hasStem && stem ? stem : 'Kök henüz yok'}</strong>
      <span className={`qm-pill ${cell.optCount >= 5 ? 'is-ok' : 'is-warn'}`}>{cell.optCount} / 5 şık</span>
      <span className="qm-note">
        {cell.contributors > 0 ? `${cell.contributors} kişi katkı verdi. ` : ''}
        {state === 'full' ? 'Soru tamamlandı; düzeltme ya da yorum için soruyu aç.' : !cell.hasStem ? 'Kökü hatırlıyorsan ekle.' : 'Eksik şıkları hatırlıyorsan ekle.'}
      </span>
      <div className="qm-acts">
        {state !== 'full' && (
          <button type="button" className="ui-btn is-primary qm-act" onClick={() => onAdd(n)}>
            <Plus aria-hidden /> {cell.hasStem && missing > 0 ? 'Şık ekle' : 'Parça ekle'}
          </button>
        )}
        <button type="button" className={`ui-btn ${state === 'full' ? 'is-primary' : 'is-tonal'} qm-act`} onClick={() => onOpen(q)}>
          Soruyu aç <ArrowRight aria-hidden />
        </button>
      </div>
    </div>
  );
};
