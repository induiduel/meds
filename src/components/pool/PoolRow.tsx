import React from 'react';
import { Check, Combine, MessageCircle } from 'lucide-react';
import { OPTION_KEYS, PoolSummary, DAY, fullTime, initials, relTime, shortName, toneOf } from './poolModel';

/** Katkıcı simge yığını: en çok 3 baş harf + "+n" */
export const PoolAvatars: React.FC<{ people: PoolSummary['people']; max?: number; size?: 'sm' | 'md' }> = ({ people, max = 3, size = 'sm' }) => {
  if (!people.length) return null;
  const shown = people.slice(0, max);
  const rest = people.length - shown.length;
  return (
    <span className={`pv-avs is-${size}`} title={people.map((p) => p.name).join(', ')}>
      {shown.map((p) => (
        <span key={p.key} className={`pv-av t${toneOf(p.key)}`} aria-hidden>{initials(p.name)}</span>
      ))}
      {rest > 0 && <span className="pv-av is-more" aria-hidden>+{rest}</span>}
      <span className="sr-only">Katkıda bulunanlar: {people.map((p) => p.name).join(', ')}</span>
    </span>
  );
};

/** Beş küçük A–E kutusu: şık varsa dolu */
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
  /** Telefon/tablet: yerinde açılır (aria-expanded); masaüstü: sağ bölmede seçilir (aria-current) */
  mode: 'expand' | 'select';
  open: boolean;
  controls?: string;
  onToggle: (id: string) => void;
  /** Bu kayıtla aynı soruyu anlatan kayıt sayısı (birleştirme önerisi; kendisi dahil) */
  similar?: number;
}

export const PoolRow = React.memo(function PoolRow({ sum, now, mode, open, controls, onToggle, similar }: PoolRowProps) {
  const { q } = sum;
  const isNew = sum.lastAt > 0 && now - sum.lastAt < DAY;
  const ders = [q.discipline, q.topic && q.topic !== q.discipline ? q.topic : ''].filter(Boolean).join(' · ');
  const by = q.status === 'completed' ? null : sum.people.length > 0 ? `${sum.people.length} kişi` : 'boş';
  const who = sum.people[0] ? shortName(sum.people[0].name) : '';
  const a11y = mode === 'expand'
    ? { 'aria-expanded': open, 'aria-controls': controls }
    : { 'aria-current': open ? ('true' as const) : undefined, 'aria-controls': controls };
  return (
    <button type="button" className={`pv-row ${isNew ? 'is-new' : ''} ${open ? 'is-open' : ''}`} onClick={() => onToggle(q.id)} {...a11y}>
      <span className="pv-row-top">
        <span className="pv-no" aria-label={`Soru ${q.questionNumber || 'numarasız'}`}>{q.questionNumber || '—'}</span>
        {isNew && <span className="pv-new">YENİ</span>}
        <span className="pv-ders">{ders || 'Ders belirsiz'}</span>
        {sum.lastAt > 0 && (
          <time className="pv-when" dateTime={new Date(sum.lastAt).toISOString()} title={`Son etkinlik: ${fullTime(sum.lastAt)}${who ? ` · ${who}` : ''}`}>
            {relTime(sum.lastAt, now)}
          </time>
        )}
      </span>
      <span className={`pv-stem ${sum.hasStem ? '' : 'is-empty'}`}>{sum.stem || 'Kök henüz yok — hatırladığını ekle'}</span>
      <span className="pv-row-foot">
        <PoolOptFill filled={sum.filled} />
        {q.status === 'completed' && <span className="pv-ok"><Check aria-hidden strokeWidth={3} />onaylı</span>}
        {similar && similar > 1 ? (
          <span className="pv-sim" title={`${similar - 1} başka kayıt aynı soruyu anlatıyor olabilir (birleştirme önerisi)`}>
            <Combine aria-hidden />{similar - 1} benzer
          </span>
        ) : null}
        <span className="pv-sp" />
        <PoolAvatars people={sum.people} />
        {by && <span className="pv-meta">{by}</span>}
        <span className="pv-meta pv-cm" aria-label={`${sum.comments} yorum`}><MessageCircle aria-hidden />{sum.comments}</span>
      </span>
    </button>
  );
});

/** Yüklenirken gerçek satır yüksekliğinde iskelet */
export const PoolRowSkeleton: React.FC = () => (
  <div className="pv-row is-skel" aria-hidden>
    <span className="pv-row-top"><span className="ui-skel" style={{ width: 26, height: 18 }} /><span className="ui-skel" style={{ width: '40%', height: 10 }} /></span>
    <span className="ui-skel" style={{ height: 13 }} />
    <span className="ui-skel" style={{ width: '70%', height: 13 }} />
    <span className="pv-row-foot"><span className="ui-skel" style={{ width: 98, height: 16 }} /></span>
  </div>
);
