import React from 'react';
import { Flag, Layers, Library, MessageSquare, Users } from 'lucide-react';

/**
 * Yönetim panosu metrik kartları (v8): değer, son 7 günün bir önceki 7 güne göre değişimi ve
 * son 14 günün eğilim çizgisi. Tarihi olmayan kayıtlar yalnız toplama girer.
 */
const DAY = 86400000;

function series(dates: (string | undefined)[], days = 14) {
  const end = new Date();
  end.setHours(23, 59, 59, 999);
  const out = new Array(days).fill(0);
  for (const d of dates) {
    if (!d) continue;
    const t = Date.parse(d);
    if (Number.isNaN(t)) continue;
    const i = days - 1 - Math.floor((end.getTime() - t) / DAY);
    if (i >= 0 && i < days) out[i] += 1;
  }
  return out;
}

const Spark: React.FC<{ data: number[] }> = ({ data }) => {
  const w = 88;
  const h = 28;
  const max = Math.max(1, ...data);
  const pts = data.map((v, i) => [(i / (data.length - 1)) * w, h - 3 - (v / max) * (h - 6)] as const);
  const line = pts.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' ');
  const [lx, ly] = pts[pts.length - 1];
  return (
    <svg className="mm-spark" viewBox={`0 0 ${w} ${h}`} width={w} height={h} aria-hidden="true">
      <path d={`${line} L${w} ${h} L0 ${h} Z`} className="mm-spark-area" />
      <path d={line} className="mm-spark-line" />
      <circle cx={lx} cy={ly} r="2.5" className="mm-spark-dot" />
    </svg>
  );
};

export interface MetricInput {
  id: string;
  label: string;
  value: number;
  dates?: (string | undefined)[];
  tone?: 'alert' | 'default';
  onClick?: () => void;
  /** Artış iyi mi (taslak/kullanıcı) yoksa kötü mü (bildirim) */
  upIsGood?: boolean;
}

const ICONS: Record<string, React.ElementType> = { reports: Flag, drafts: Layers, comments: MessageSquare, users: Users, pool: Library };

export const ManageMetrics: React.FC<{ items: MetricInput[]; loading?: boolean }> = ({ items, loading }) => (
  <section className="mm" aria-label="Pano">
    {items.map((m) => {
      const s = m.dates ? series(m.dates) : null;
      const last7 = s ? s.slice(7).reduce((a, b) => a + b, 0) : 0;
      const prev7 = s ? s.slice(0, 7).reduce((a, b) => a + b, 0) : 0;
      const delta = last7 - prev7;
      const good = m.upIsGood ? delta >= 0 : delta <= 0;
      const Icon = ICONS[m.id] || Library;
      const Tag = m.onClick ? 'button' : 'div';
      return (
        <Tag key={m.id} type={m.onClick ? 'button' : undefined} onClick={m.onClick} className={`mm-card ${m.tone === 'alert' && m.value > 0 ? 'is-alert' : ''}`}>
          <span className="mm-top">
            <span className="mm-ic" aria-hidden><Icon /></span>
            <span className="mm-l">{m.label}</span>
          </span>
          {loading ? (
            <span className="ui-skel" style={{ width: '45%', height: 22, marginTop: 4 }} />
          ) : (
            <span className="mm-row">
              <b className="mm-v hk-num">{m.value.toLocaleString('tr-TR')}</b>
              {s && <Spark data={s} />}
            </span>
          )}
          {s && !loading && (
            <span className={`mm-d ${delta === 0 ? '' : good ? 'is-good' : 'is-bad'}`}>
              {delta === 0 ? 'Geçen haftayla aynı' : `${delta > 0 ? '+' : ''}${delta} bu hafta`}
            </span>
          )}
        </Tag>
      );
    })}
  </section>
);
