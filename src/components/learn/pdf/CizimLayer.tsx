import { memo } from 'react';

/**
 * Canlı çizim katmanı (R6, ICERIK_MOTORU_V3.md §4): hoca konuşurken PDF üstünde kontur / akış oku / eğri fazı / şema.
 * Komutlar scripts/cizim/cizim_uret.py'den (kapı cizim_dogrula.py), sunucu cümle işaretine `z` olarak ekler. İlerleme
 * imleçle aynı sayaçtan: cümle içi konuşulan karakter `k[0]`→`k[1]` aralığında 0→1. Aralığa gelmeden çizim yok, geçince
 * tam kalır (cümle bitene dek). Koordinatlar sayfa oranı (0–1); SVG sayfayı kaplar, çizgi kalınlığı ölçekten bağımsız.
 */
export interface CizimKomut {
  tur: 'kontur' | 'akis' | 'egri_faz' | 'sema';
  s: number;
  k: [number, number];
  nokta?: number[][];
  a?: number[];
  b?: number[];
  iliski?: 'aktive' | 'inhibe' | 'donusur';
  fazlar?: { aralik: [number, number]; faz: 'yukselis' | 'inis' | 'plato' }[];
  dugum?: { id: string; metin: string }[];
  kenar?: { a: string; b: string; tur: string }[];
  etiket?: string;
}

const AZ_HAREKET = typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
const V = 1000;
const P = (n: number[]) => `${(n[0] * V).toFixed(1)} ${(n[1] * V).toFixed(1)}`;

/** Catmull-Rom → kübik Bezier (noktalardan geçen yumuşak eğri) */
function egri(nk: number[][], kapali = false): string {
  const p = nk.map((n) => [n[0] * V, n[1] * V]);
  if (p.length < 2) return '';
  const g = kapali ? [p[p.length - 1], ...p, p[0], p[1]] : [p[0], ...p, p[p.length - 1]];
  let d = `M${p[0][0].toFixed(1)} ${p[0][1].toFixed(1)}`;
  for (let i = 1; i < g.length - 2; i++) {
    const [p0, p1, p2, p3] = [g[i - 1], g[i], g[i + 1], g[i + 2]];
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += ` C${c1[0].toFixed(1)} ${c1[1].toFixed(1)}, ${c2[0].toFixed(1)} ${c2[1].toFixed(1)}, ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
  }
  return d;
}

const ilerleme = (z: CizimKomut, c: number) => (c < z.k[0] ? -1 : AZ_HAREKET ? 1 : Math.min(1, (c - z.k[0]) / Math.max(1, z.k[1] - z.k[0])));

function Etiket({ at, metin }: { at: number[]; metin?: string }) {
  if (!metin) return null;
  return (
    <foreignObject x={Math.min(at[0] * V, V - 260)} y={Math.max(0, at[1] * V - 44)} width={260} height={40}>
      <div className="pdv-cz-etiket">{metin}</div>
    </foreignObject>
  );
}

function Komut({ z, t }: { z: CizimKomut; t: number }) {
  const ciz = { pathLength: 1, strokeDasharray: 1, strokeDashoffset: 1 - t } as const;
  if (z.tur === 'kontur' && z.nokta) {
    return (
      <g className="pdv-cz-kontur">
        <path d={egri(z.nokta, true)} {...ciz} vectorEffect="non-scaling-stroke" />
        {t >= 1 && <Etiket at={z.nokta[0]} metin={z.etiket} />}
      </g>
    );
  }
  if (z.tur === 'akis' && z.a && z.b) {
    const [a, b] = [z.a, z.b];
    const m = [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
    const ui = z.iliski === 'inhibe';
    return (
      <g className={`pdv-cz-akis is-${z.iliski || 'aktive'}`}>
        <path d={`M${P(a)} L${P(b)}`} {...ciz} markerEnd={t >= 1 ? `url(#pdv-cz-${ui ? 'dur' : 'ok'})` : undefined} vectorEffect="non-scaling-stroke" />
        {t > 0 && t < 1 && <circle cx={m[0] * V} cy={m[1] * V} r={7} className="pdv-cz-parca" />}
        {t >= 1 && <Etiket at={[(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]} metin={z.etiket} />}
      </g>
    );
  }
  if (z.tur === 'egri_faz' && z.nokta) {
    const n = z.nokta.length;
    const ulasilan = Math.max(1, Math.round(t * (n - 1)));
    const fazOf = (i: number) => z.fazlar?.find((f) => i >= f.aralik[0] && i < f.aralik[1])?.faz || 'plato';
    return (
      <g className="pdv-cz-egri">
        {z.nokta.slice(0, ulasilan).map((p, i) => (
          <path key={i} className={`is-${fazOf(i)}`} d={`M${P(p)} L${P(z.nokta![i + 1])}`} vectorEffect="non-scaling-stroke" />
        ))}
        <circle cx={z.nokta[ulasilan][0] * V} cy={z.nokta[ulasilan][1] * V} r={8} className="pdv-cz-parca" />
        {t >= 1 && <Etiket at={z.nokta[0]} metin={z.etiket} />}
      </g>
    );
  }
  return null;
}

/** Şema: köşede yarı saydam panel, düğümler soldan sağa sırayla belirir (yerleşim istemcide; koordinat yok) */
function Sema({ z, t }: { z: CizimKomut; t: number }) {
  const dg = z.dugum || [];
  const gorunen = Math.max(1, Math.ceil(t * dg.length));
  const sira = new Map(dg.map((d, i) => [d.id, i]));
  return (
    <div className="pdv-cz-sema" role="img" aria-label={dg.map((d) => d.metin).join(', ')}>
      {dg.slice(0, gorunen).map((d, i) => {
        const gelen = (z.kenar || []).find((e) => sira.get(e.b) === i && (sira.get(e.a) ?? 99) < i);
        return (
          <span key={d.id} className="pdv-cz-dugum-kap">
            {gelen && <span className={`pdv-cz-sema-ok is-${gelen.tur}`}>{gelen.tur === 'inhibe' ? '⊣' : gelen.tur === 'donusur' ? '⇒' : '→'}</span>}
            <span className="pdv-cz-dugum">{d.metin}</span>
          </span>
        );
      })}
    </div>
  );
}

export const CizimLayer = memo(function CizimLayer({ z, useChar }: { z: CizimKomut[]; useChar: () => number }) {
  const c = useChar();
  const cizimler = z.filter((x) => x.tur !== 'sema');
  const sema = z.find((x) => x.tur === 'sema');
  return (
    <>
      {cizimler.length > 0 && (
        <svg className="pdv-cz" viewBox={`0 0 ${V} ${V}`} preserveAspectRatio="none" aria-hidden>
          <defs>
            <marker id="pdv-cz-ok" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
              <path d="M0 0 L10 5 L0 10 z" className="pdv-cz-uc" />
            </marker>
            <marker id="pdv-cz-dur" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto">
              <path d="M5 0 L5 10" className="pdv-cz-uc-dur" />
            </marker>
          </defs>
          {cizimler.map((x, i) => {
            const t = ilerleme(x, c);
            return t < 0 ? null : <Komut key={i} z={x} t={t} />;
          })}
        </svg>
      )}
      {sema && ilerleme(sema, c) >= 0 && <Sema z={sema} t={ilerleme(sema, c)} />}
    </>
  );
});
