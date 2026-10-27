import React, { useMemo } from 'react';
import dagilim from '../../data/sinav_dagilimi.json';
import branslar from '../../data/dersler/branslar.json';

/**
 * v15 · Sınav ağırlığı kabarcık haritası (tasarım Z04 "Sınav ağırlığı"). Veri: src/data/sinav_dagilimi.json (kurul başına
 * branş soru sayısı; "tahmini" ise etikette belirtilir). Kabarcık alanı soru sayısıyla orantılı; yerleşim açgözlü sarmal.
 */
type Kurullar = Record<string, { toplam: number; tahmini?: boolean; branslar: Record<string, number> }>;
const AD = new Map<string, string>((branslar as { branslar: { slug: string; kisa?: string; ad: string }[] }).branslar.map((b) => [b.slug, b.kisa || b.ad]));
const EK: Record<string, string> = { halksagligi: 'Halk Sağlığı', kadindogum: 'Kadın Doğum', aile: 'Aile Hekimliği', ftr: 'FTR', beyincerrahi: 'Beyin Cerrahi', uroloji: 'Üroloji' };
const ad = (k: string) => { const s = k.replace(/^k\d+/, ''); return AD.get(s) || EK[s] || s.charAt(0).toLocaleUpperCase('tr') + s.slice(1); };
const TON = ['var(--color-accent)', 'var(--color-clinic, var(--color-accent))', 'var(--color-warn)', 'var(--color-ai, var(--color-accent))', 'var(--color-ok)', 'var(--color-bad)'];

export function sinavAgirligiVar(kurul: number) { return !!(dagilim as { kurullar: Kurullar }).kurullar[String(kurul)]; }

export default function SinavAgirligiV15({ kurul }: { kurul: number }) {
  const k = (dagilim as { kurullar: Kurullar }).kurullar[String(kurul)];
  const yer = useMemo(() => {
    if (!k) return null;
    const ogeler = Object.entries(k.branslar).sort((a, b) => b[1] - a[1]).map(([id, n]) => ({ id, n, r: 9 + Math.sqrt(n) * 7.5 }));
    const konan: { id: string; n: number; r: number; x: number; y: number }[] = [];
    for (const o of ogeler) {
      let x = 0, y = 0;
      if (konan.length) {
        outer: for (let d = 0; d < 400; d += 2) for (let a = 0; a < 360; a += 12) {
          const tx = Math.cos((a * Math.PI) / 180) * d * 1.5, ty = Math.sin((a * Math.PI) / 180) * d;
          if (konan.every((c) => Math.hypot(c.x - tx, c.y - ty) >= c.r + o.r + 3)) { x = tx; y = ty; break outer; }
        }
      }
      konan.push({ ...o, x, y });
    }
    const minX = Math.min(...konan.map((c) => c.x - c.r)), maxX = Math.max(...konan.map((c) => c.x + c.r));
    const minY = Math.min(...konan.map((c) => c.y - c.r)), maxY = Math.max(...konan.map((c) => c.y + c.r));
    return { konan, vb: `${minX - 4} ${minY - 4} ${maxX - minX + 8} ${maxY - minY + 8}` };
  }, [k]);
  if (!k || !yer) return null;
  return (
    <figure className="sa15" aria-label={`Kurul ${kurul} sınav ağırlığı`}>
      <svg viewBox={yer.vb} role="img" aria-hidden="false">
        <title>{`Kurul ${kurul}: ${Object.entries(k.branslar).map(([b, n]) => `${ad(b)} ${n}`).join(', ')}`}</title>
        {yer.konan.map((c, i) => (
          <g key={c.id}>
            <circle cx={c.x} cy={c.y} r={c.r} fill={TON[i % TON.length]} fillOpacity={0.16} stroke={TON[i % TON.length]} strokeWidth={1.5} />
            {c.r >= 22 && <text x={c.x} y={c.y - 2} textAnchor="middle" className="sa15-ad" fontSize={Math.min(13, c.r / 3.2)}>{ad(c.id)}</text>}
            <text x={c.x} y={c.y + (c.r >= 22 ? 13 : 4)} textAnchor="middle" className="sa15-n" fontSize={Math.min(14, Math.max(9, c.r / 2.6))}>{c.n}</text>
          </g>
        ))}
      </svg>
      <figcaption className="v15-cap">
        {k.toplam} soru{k.tahmini ? ' · tahmini dağılım (resmî açıklanmadı)' : ''}
        <span className="sa15-leg">{Object.entries(k.branslar).sort((a, b) => b[1] - a[1]).map(([b, n]) => `${ad(b)} ${n}`).join(' · ')}</span>
      </figcaption>
    </figure>
  );
}
