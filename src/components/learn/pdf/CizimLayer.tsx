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
  /** yerleşim (cizim_uret.yerlesim, içeriğin önü kapanmasın): ok kavisinin denetim noktası, asıl hedef, etiketin ve
   *  şema panelinin boş yerdeki konumu (sayfa oranı) */
  c?: number[];
  hedef?: number[];
  /** ok rotası (cizim_uret.ok_yerlesimi): düz / dirsek / kavis noktaları; hedef yazının kutusu */
  yol?: number[][];
  rota?: 'duz' | 'dirsek' | 'kavis';
  hedef_kutu?: number[];
  etiket_konum?: number[];
  etiket_genislik?: number;
  konum?: number[];
  genislik?: number;
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

/** Etiket yalnız betiğin boş bulduğu yerde (etiket_konum); yoksa gösterilmez — yazının üstüne binmesin */
function Etiket({ z }: { z: CizimKomut }) {
  if (!z.etiket || !z.etiket_konum) return null;
  return (
    <foreignObject x={z.etiket_konum[0] * V} y={z.etiket_konum[1] * V} width={(z.etiket_genislik || 0.3) * V} height={34}>
      <div className="pdv-cz-etiket">{z.etiket}</div>
    </foreignObject>
  );
}

/** Yol → SVG: dirsekte köşe yuvarlatılır (yarıçap kısa kenarın en çok yarısı) */
function yolD(y: number[][], rota?: string): string {
  if (rota === 'dirsek' && y.length === 3) {
    const [a, k, b] = y;
    const r = Math.min(0.018, Math.hypot(k[0] - a[0], k[1] - a[1]) / 2, Math.hypot(b[0] - k[0], b[1] - k[1]) / 2);
    const yon = (u: number[], v: number[]) => { const L = Math.hypot(v[0] - u[0], v[1] - u[1]) || 1; return [(v[0] - u[0]) / L, (v[1] - u[1]) / L]; };
    const d1 = yon(a, k), d2 = yon(k, b);
    return `M${P(a)} L${P([k[0] - d1[0] * r, k[1] - d1[1] * r])} Q${P(k)} ${P([k[0] + d2[0] * r, k[1] + d2[1] * r])} L${P(b)}`;
  }
  return `M${P(y[0])}` + y.slice(1).map((q) => ` L${P(q)}`).join('');
}

/** Yol boyunca u (0–1) oranındaki nokta (hareketli parçacık) */
function yolNokta(y: number[][], u: number): number[] {
  const seg = y.slice(1).map((q, i) => Math.hypot(q[0] - y[i][0], q[1] - y[i][1]));
  let kalan = u * seg.reduce((a, b) => a + b, 0);
  for (let i = 0; i < seg.length; i++) {
    if (kalan <= seg[i] || i === seg.length - 1) {
      const f = seg[i] ? Math.min(1, kalan / seg[i]) : 0;
      return [y[i][0] + (y[i + 1][0] - y[i][0]) * f, y[i][1] + (y[i + 1][1] - y[i][1]) * f];
    }
    kalan -= seg[i];
  }
  return y[y.length - 1];
}

function Komut({ z, t }: { z: CizimKomut; t: number }) {
  const ciz = { pathLength: 1, strokeDasharray: 1, strokeDashoffset: 1 - t } as const;
  if (z.tur === 'kontur' && z.nokta) {
    return (
      <g className="pdv-cz-kontur">
        <path d={egri(z.nokta, true)} {...ciz} vectorEffect="non-scaling-stroke" />
        {t >= 1 && <Etiket z={z} />}
      </g>
    );
  }
  if (z.tur === 'akis' && z.a && z.b) {
    const [a, b] = [z.a, z.b];
    const yol = z.yol?.length ? z.yol : z.c ? Array.from({ length: 17 }, (_, i) => {
      const u = i / 16, c = z.c!;
      return [(1 - u) ** 2 * a[0] + 2 * (1 - u) * u * c[0] + u * u * b[0], (1 - u) ** 2 * a[1] + 2 * (1 - u) * u * c[1] + u * u * b[1]];
    }) : [a, b];
    const m = yolNokta(yol, t);
    const ui = z.iliski === 'inhibe';
    const hk = z.hedef_kutu;
    return (
      <g className={`pdv-cz-akis is-${z.iliski || 'aktive'}`}>
        <path d={yolD(yol, z.rota)} {...ciz} markerEnd={t >= 1 ? `url(#pdv-cz-${ui ? 'dur' : 'ok'})` : undefined} vectorEffect="non-scaling-stroke" />
        {t > 0 && t < 1 && <circle cx={m[0] * V} cy={m[1] * V} r={4} className="pdv-cz-parca" />}
        {t >= 1 && hk && (
          <rect x={hk[0] * V} y={hk[1] * V} width={(hk[2] - hk[0]) * V} height={(hk[3] - hk[1]) * V} rx={6} className="pdv-cz-hedef" vectorEffect="non-scaling-stroke" />
        )}
        {t >= 1 && <Etiket z={z} />}
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
        <circle cx={z.nokta[ulasilan][0] * V} cy={z.nokta[ulasilan][1] * V} r={4} className="pdv-cz-parca" />
        {t >= 1 && <Etiket z={z} />}
      </g>
    );
  }
  return null;
}

const OK = (tur?: string) => (tur === 'inhibe' ? '⊣' : tur === 'donusur' ? '⇒' : '→');

/**
 * Şema: betiğin boş bulduğu yerde (konum) panel, düğümler sırayla belirir. Birden çok düğüm aynı hedefe gidiyorsa
 * (ör. dört neden → acil beyin görüntülemesi) tek okla değil, alt alta dizilip "}" ile toplanarak hedefe bağlanır
 * (kullanıcı 2026-10-24: tek ok grubun tamamını kapsadığını anlatmıyor). Kalan kenarlar soldan sağa zincir.
 */
function Sema({ z, t }: { z: CizimKomut; t: number }) {
  const dg = z.dugum || [];
  const kn = z.kenar || [];
  const gorunen = Math.max(1, Math.ceil(t * dg.length));
  const sira = new Map(dg.map((d, i) => [d.id, i]));
  const gelen = new Map<string, typeof kn>();
  for (const e of kn) gelen.set(e.b, [...(gelen.get(e.b) || []), e]);
  const grupHedef = [...gelen.entries()].filter(([, es]) => es.length >= 2).sort((x, y) => y[1].length - x[1].length)[0];
  const stil = z.konum ? { left: `${z.konum[0] * 100}%`, top: `${z.konum[1] * 100}%`, right: 'auto', bottom: 'auto', maxWidth: `${(z.genislik || 0.6) * 100}%` } : undefined;
  const aria = dg.map((d) => d.metin).join(', ');
  const gor = (id: string) => (sira.get(id) ?? 99) < gorunen;

  if (grupHedef) {
    const [hid, es] = grupHedef;
    const kaynak = es.map((e) => dg.find((d) => d.id === e.a)).filter(Boolean) as { id: string; metin: string }[];
    const hedef = dg.find((d) => d.id === hid);
    const tamam = kaynak.every((d) => gor(d.id));
    const diger = dg.filter((d) => d.id !== hid && !kaynak.includes(d));
    return (
      <div className="pdv-cz-sema is-grup" role="img" aria-label={aria} style={stil}>
        <div className="pdv-cz-grup">
          <div className="pdv-cz-grup-kaynak">
            {kaynak.filter((d) => gor(d.id)).map((d) => <span key={d.id} className="pdv-cz-dugum pdv-cz-dugum-kap">{d.metin}</span>)}
          </div>
          {tamam && <span className="pdv-cz-kume" aria-hidden />}
          {tamam && hedef && gor(hid) && (
            <span className="pdv-cz-dugum-kap">
              <span className={`pdv-cz-sema-ok is-${es[0].tur}`}>{OK(es[0].tur)}</span>
              <span className="pdv-cz-dugum is-hedef">{hedef.metin}</span>
            </span>
          )}
        </div>
        {diger.filter((d) => gor(d.id)).map((d) => {
          const g = kn.find((e) => e.b === d.id);
          return (
            <span key={d.id} className="pdv-cz-dugum-kap">
              {g && <span className={`pdv-cz-sema-ok is-${g.tur}`}>{OK(g.tur)}</span>}
              <span className="pdv-cz-dugum">{d.metin}</span>
            </span>
          );
        })}
      </div>
    );
  }
  return (
    <div className="pdv-cz-sema" role="img" aria-label={aria} style={stil}>
      {dg.slice(0, gorunen).map((d, i) => {
        const g = kn.find((e) => sira.get(e.b) === i && (sira.get(e.a) ?? 99) < i);
        return (
          <span key={d.id} className="pdv-cz-dugum-kap">
            {g && <span className={`pdv-cz-sema-ok is-${g.tur}`}>{OK(g.tur)}</span>}
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
  // şema yalnız betiğin boş bulduğu yerde (konum); boş yer yoksa (konum null) sayfanın önü kapanmasın diye gösterilmez
  const sema = z.find((x) => x.tur === 'sema' && (x.konum || x.konum === undefined));
  return (
    <>
      {cizimler.length > 0 && (
        <svg className="pdv-cz" viewBox={`0 0 ${V} ${V}`} preserveAspectRatio="none" aria-hidden>
          <defs>
            <marker id="pdv-cz-ok" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.5" markerHeight="4.5" orient="auto-start-reverse">
              <path d="M0 0 L10 5 L0 10 z" className="pdv-cz-uc" />
            </marker>
            <marker id="pdv-cz-dur" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto">
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
