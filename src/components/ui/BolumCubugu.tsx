import React, { useRef, useState } from 'react';
import '../../styles/bolum-cubugu.css';

/**
 * YouTube tarzı bölümlü ilerleme çubuğu (ortak): her bölüm süresine oranlı ayrı parça, aralarında boşluk, parça parça
 * dolum; üstüne gelince parça kalınlaşır, ipucu imleci izler (bölüm adı + zaman). Tıklama/sürükleme o ana atlar,
 * ←/→ 5 sn, Shift+←/→ bölüm atlar. Sesli ders oynatıcısı aynı davranışın kendi sürümünü kullanır (CanliDersDock).
 */
export interface BolumParca {
  /** Başlangıç saniyesi */
  s: number;
  ad: string;
}

const fmt = (sn: number) => {
  const t = Math.max(0, Math.floor(sn || 0));
  const h = Math.floor(t / 3600), m = Math.floor((t % 3600) / 60), s = t % 60;
  return h ? `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}` : `${m}:${String(s).padStart(2, '0')}`;
};

export const BolumCubugu: React.FC<{
  t: number;
  dur: number;
  bolumler: BolumParca[];
  onSeek: (sn: number) => void;
  etiket?: string;
  className?: string;
}> = ({ t, dur, bolumler, onSeek, etiket = 'Ses konumu', className = '' }) => {
  const ref = useRef<HTMLDivElement>(null);
  const [surukle, setSurukle] = useState<number | null>(null);
  const [uzerinde, setUzerinde] = useState<number | null>(null);
  const sirali = bolumler.filter((b) => b.s < dur).sort((a, b) => a.s - b.s);
  const parcalar = sirali.length > 1
    ? sirali.map((b, k) => ({ ...b, e: k + 1 < sirali.length ? sirali[k + 1].s : dur, k }))
    : [{ s: 0, e: dur || 1, ad: '', k: -1 }];
  const indexOf = (x: number) => {
    for (let k = parcalar.length - 1; k >= 0; k--) if (x >= parcalar[k].s) return k;
    return 0;
  };
  const xden = (cx: number) => {
    const r = ref.current!.getBoundingClientRect();
    return Math.min(1, Math.max(0, (cx - r.left) / Math.max(1, r.width))) * dur;
  };
  const goster = surukle ?? t;
  const ip = surukle ?? uzerinde;
  const ipParca = ip != null ? parcalar[indexOf(ip)] : undefined;
  const etkin = indexOf(goster);

  return (
    <div
      ref={ref}
      className={`bc${surukle != null ? ' is-surukle' : ''}${parcalar.length > 1 ? ' is-bolumlu' : ''} ${className}`}
      role="slider"
      tabIndex={0}
      aria-label={parcalar.length > 1 ? `${etiket} (Shift + ok: bölüm atla)` : etiket}
      aria-valuemin={0}
      aria-valuemax={Math.round(dur)}
      aria-valuenow={Math.round(goster)}
      aria-valuetext={`${fmt(goster)} / ${fmt(dur)}${parcalar[etkin]?.ad ? `, ${parcalar[etkin].ad}` : ''}`}
      onPointerDown={(e) => {
        if (!dur || e.button !== 0) return;
        e.preventDefault();
        (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
        setSurukle(xden(e.clientX));
      }}
      onPointerMove={(e) => {
        if (!dur) return;
        const x = xden(e.clientX);
        if (surukle != null) setSurukle(x);
        if (e.pointerType !== 'touch') setUzerinde(x);
      }}
      onPointerLeave={() => setUzerinde(null)}
      onPointerUp={(e) => {
        if (surukle == null) return;
        onSeek(xden(e.clientX));
        setSurukle(null);
      }}
      onPointerCancel={() => { setSurukle(null); setUzerinde(null); }}
      onKeyDown={(e) => {
        if (e.shiftKey && (e.key === 'ArrowLeft' || e.key === 'ArrowRight') && parcalar.length > 1) {
          e.preventDefault(); e.stopPropagation();
          const k = indexOf(t);
          const h = e.key === 'ArrowRight' ? Math.min(parcalar.length - 1, k + 1) : (t - parcalar[k].s > 3 ? k : Math.max(0, k - 1));
          onSeek(parcalar[h].s);
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
          e.preventDefault(); e.stopPropagation();
          onSeek(Math.min(dur, Math.max(0, t + (e.key === 'ArrowRight' ? 5 : -5))));
        } else if (e.key === 'Home') { e.preventDefault(); onSeek(0); }
      }}
    >
      <div className="bc-parcalar">
        {parcalar.map((p) => {
          const gen = Math.max(0, p.e - p.s);
          const dolu = gen > 0 ? Math.min(1, Math.max(0, (goster - p.s) / gen)) : 0;
          return (
            <span key={p.k} className={`bc-parca${ipParca === p && parcalar.length > 1 ? ' is-ustunde' : ''}`} style={{ flexGrow: gen || 1 }}>
              <i style={{ transform: `scaleX(${dolu})` }} />
            </span>
          );
        })}
      </div>
      <span className="bc-tutamac" style={{ left: `${dur > 0 ? Math.min(1, goster / dur) * 100 : 0}%` }} />
      {ip != null && (
        <span className="bc-ipucu" style={{ ['--x' as string]: dur > 0 ? ip / dur : 0 }}>
          {ipParca?.ad && <b>{ipParca.ad}</b>}
          <span>{fmt(ip)}</span>
        </span>
      )}
    </div>
  );
};
