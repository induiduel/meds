import React from 'react';
import { ChevronDown } from 'lucide-react';
import { disciplineClass } from '../../utils/discipline';
import { OPTION_KEYS, POOL_STATUS_LABEL, PoolStatus, PoolSummary, DAY, fullTime, relTime, statusOf } from './poolModel';

const GENERIC_DISC = /^(belirtilmedi|genel|belirsiz|)$/i;

/** Ders etiketi: ders renginde küçük hap (genel/belirsiz derslerde gösterilmez) */
export const PoolTag: React.FC<{ discipline?: string | null }> = ({ discipline }) => {
  const d = (discipline || '').trim();
  if (GENERIC_DISC.test(d)) return null;
  return <span className={`pv-tag ${disciplineClass(d)}`}>{d}</span>;
};

/** Tek durum göstergesi: nokta + kısa ad */
export const PoolStatusMark: React.FC<{ status: PoolStatus }> = ({ status }) => (
  <span className={`pv-st is-${status}`}>
    <i aria-hidden />
    {POOL_STATUS_LABEL[status]}
  </span>
);

/** Beş küçük A–E kutusu: şık varsa dolu (yalnız ayrıntıda) */
export const PoolOptFill: React.FC<{ filled: Set<string> }> = ({ filled }) => (
  <span className="pv-of" role="img" aria-label={`${filled.size} / 5 şık var`}>
    {OPTION_KEYS.map((k) => (
      <span key={k} className={filled.has(k) ? 'is-on' : ''} aria-hidden>{k}</span>
    ))}
  </span>
);

interface PoolRowProps {
  sum: PoolSummary;
  now: number;
  /** Telefon/tablet: yerinde açılır (aria-expanded); bölmeli görünüm: sağ bölmede seçilir (aria-current) */
  mode: 'expand' | 'select';
  selected: boolean;
  onToggle: (id: string) => void;
}

/**
 * Havuz satırı (v12, sade): numara · 2 satır kök · ders etiketi · tek durum · zaman.
 * Seçili satır: vurgu rengi sol çizgi + renkli zemin + dolu numara rozeti.
 */
export const PoolRow = React.memo(function PoolRow({ sum, now, mode, selected, onToggle }: PoolRowProps) {
  const { q } = sum;
  const isNew = sum.lastAt > 0 && now - sum.lastAt < DAY;
  const status = statusOf(sum);
  const no = q.questionNumber || '—';
  const a11y = mode === 'expand'
    ? { 'aria-expanded': selected }
    : { 'aria-current': selected ? ('true' as const) : undefined };
  return (
    <button
      type="button"
      className={`pv-row ${selected ? 'is-selected' : ''}`}
      onClick={() => onToggle(q.id)}
      data-row={q.id}
      aria-label={`Soru ${q.questionNumber || 'numarasız'}, ${POOL_STATUS_LABEL[status]}${isNew ? ', yeni' : ''}: ${sum.stem.slice(0, 90) || 'kök yok'}`}
      {...a11y}
    >
      <span className="pv-no" aria-hidden>{no}</span>
      <span className="pv-row-main" aria-hidden>
        <span className={`pv-stem ${sum.hasStem ? '' : 'is-empty'}`}>{sum.stem || 'Kök henüz yok — hatırladığını ekle'}</span>
        <span className="pv-row-meta">
          <PoolTag discipline={q.discipline} />
          <PoolStatusMark status={status} />
          <span className="pv-sp" />
          {sum.lastAt > 0 && (
            <time className={`pv-when ${isNew ? 'is-new' : ''}`} dateTime={new Date(sum.lastAt).toISOString()} title={`Son etkinlik: ${fullTime(sum.lastAt)}`}>
              {relTime(sum.lastAt, now)}
            </time>
          )}
        </span>
      </span>
      {mode === 'expand' && <ChevronDown className="pv-chev" aria-hidden />}
    </button>
  );
});

/** Yüklenirken gerçek satır yüksekliğinde iskelet */
export const PoolRowSkeleton: React.FC = () => (
  <div className="pv-row is-skel" aria-hidden>
    <span className="ui-skel pv-no" />
    <span className="pv-row-main">
      <span className="ui-skel" style={{ height: 13 }} />
      <span className="ui-skel" style={{ width: '70%', height: 13 }} />
      <span className="ui-skel" style={{ width: 120, height: 12, marginTop: 4 }} />
    </span>
  </div>
);
