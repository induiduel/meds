import React, { forwardRef, useEffect, useImperativeHandle, useRef } from 'react';
import type { UnoKart } from '../../../services/masa/tipler';
import { titret } from '../ortak';
import { KartGorsel, kartAdi } from './Kart';
import type { KartYer, Nokta, Yerlesim } from './yerlesim';

export interface ElKol {
  /** Bırakılıp bekleyen kartı yaylanarak ele döndürür */
  geriAl: (id: number) => void;
}

interface Props {
  kartlar: UnoKart[];
  poz: Map<number, KartYer>;
  yer: Yerlesim;
  tema: string;
  oynanabilir: Set<number>;
  /** Oynanabilir / sönük ayrımı gösterilsin mi (asistan) */
  fark: boolean;
  secili: number | null;
  cekilen: number | null;
  oneri: number | null;
  gizli: Set<number>;
  etkin: boolean;
  onDokun: (id: number) => void;
  onSurukle: (aktif: boolean) => void;
  /** Bırakma: 'bekle' = kart bırakıldığı yerde kalır (sunucu / renk seçimi beklenir), 'geri' = ele döner */
  onBirak: (id: number, kart: Nokta & { a: number; s: number }, isaretci: Nokta) => 'bekle' | 'geri';
}

interface Surukle { id: number; pid: number; el: HTMLElement; sx: number; sy: number; kx: number; ky: number; dx: number; dy: number; oynadi: boolean; raf: number; egim: number; sonX: number }

const HAVADA = 1.14;

/** Alttaki yelpaze el: sürükle-bırak (Pointer Events) + dokun-seç */
const El = forwardRef<ElKol, Props>(function El({ kartlar, poz, yer, tema, oynanabilir, fark, secili, cekilen, oneri, gizli, etkin, onDokun, onSurukle, onBirak }, ref) {
  const ogeler = useRef(new Map<number, HTMLElement>());
  const s = useRef<Surukle | null>(null);

  const serbest = (el: HTMLElement, yayli: boolean) => {
    el.classList.remove('um-havada', 'um-bekle');
    el.style.transform = '';
    if (yayli) { el.classList.add('um-donus'); window.setTimeout(() => el.classList.remove('um-donus'), 500); }
  };
  useImperativeHandle(ref, () => ({ geriAl: (id) => { const el = ogeler.current.get(id); if (el) serbest(el, true); } }), []);

  // Sürüklenen kart elden çıktıysa (oynandı, el bitti) sürüklemeyi kapat
  useEffect(() => {
    const d = s.current;
    if (d && (!etkin || !kartlar.some((k) => k.id === d.id))) { cancelAnimationFrame(d.raf); s.current = null; if (d.el.isConnected) serbest(d.el, false); onSurukle(false); }
  });
  useEffect(() => () => { if (s.current) cancelAnimationFrame(s.current.raf); }, []);

  const asagi = (e: React.PointerEvent<HTMLDivElement>, id: number) => {
    if (!etkin || s.current || (e.pointerType === 'mouse' && e.button !== 0)) return;
    const el = e.currentTarget;
    if (el.classList.contains('um-bekle')) return;
    const p = poz.get(id);
    if (!p) return;
    try { el.setPointerCapture(e.pointerId); } catch { /* yok */ }
    // Başlangıç: kartın o anki gerçek merkezi (kalkık / geçişte olabilir) → sıçrama olmaz
    const kok = el.closest('.um-kok')?.getBoundingClientRect();
    const r = el.getBoundingClientRect();
    const kx = kok ? r.left + r.width / 2 - kok.left : p.x;
    const ky = kok ? r.top + r.height / 2 - kok.top : p.y;
    s.current = { id, pid: e.pointerId, el, sx: e.clientX, sy: e.clientY, kx, ky, dx: 0, dy: 0, oynadi: false, raf: 0, egim: p.a, sonX: e.clientX };
  };
  const hareket = (e: React.PointerEvent<HTMLDivElement>) => {
    const d = s.current;
    if (!d || d.pid !== e.pointerId) return;
    d.dx = e.clientX - d.sx; d.dy = e.clientY - d.sy;
    if (!d.oynadi) {
      if (Math.hypot(d.dx, d.dy) < 8) return;
      d.oynadi = true;
      d.el.classList.remove('um-donus');
      d.el.classList.add('um-havada');
      titret(8);
      onSurukle(true);
    }
    // Eğim: yatay hıza göre, yumuşatılmış
    d.egim = d.egim * 0.7 + Math.max(-16, Math.min(16, (e.clientX - d.sonX) * 1.1)) * 0.3;
    d.sonX = e.clientX;
    if (!d.raf) d.raf = requestAnimationFrame(() => {
      d.raf = 0;
      if (s.current !== d) return;
      d.el.style.transform = `translate3d(${d.kx + d.dx}px, ${d.ky + d.dy}px, 0) rotate(${d.egim.toFixed(1)}deg) scale(${HAVADA})`;
    });
  };
  const bitir = (e: React.PointerEvent<HTMLDivElement>, iptal: boolean) => {
    const d = s.current;
    if (!d || d.pid !== e.pointerId) return;
    cancelAnimationFrame(d.raf);
    s.current = null;
    try { d.el.releasePointerCapture(d.pid); } catch { /* yok */ }
    if (!d.oynadi) { if (!iptal) onDokun(d.id); return; }
    onSurukle(false);
    if (iptal) { serbest(d.el, true); return; }
    const kok = d.el.closest('.um-kok')?.getBoundingClientRect();
    const isaretci = kok ? { x: e.clientX - kok.left, y: e.clientY - kok.top } : { x: d.kx + d.dx, y: d.ky + d.dy };
    const sonuc = onBirak(d.id, { x: d.kx + d.dx, y: d.ky + d.dy, a: d.egim, s: HAVADA }, isaretci);
    if (sonuc === 'bekle') {
      d.el.classList.remove('um-havada');
      d.el.classList.add('um-bekle');
      d.el.style.transform = `translate3d(${d.kx + d.dx}px, ${d.ky + d.dy}px, 0) rotate(${d.egim.toFixed(1)}deg) scale(${HAVADA})`;
    } else serbest(d.el, true);
  };

  return (
    <div className="um-el" role="group" aria-label={`Elin: ${kartlar.length} kart`} style={{ ['--um-kw' as string]: `${yer.kw}px` }}>
      {kartlar.map((k) => {
        const p = poz.get(k.id);
        if (!p) return null;
        const uygun = oynanabilir.has(k.id);
        const sinif = [
          'um-el-kart',
          fark && uygun ? 'um-uygun' : '',
          fark && !uygun ? 'um-sonuk' : '',
          secili === k.id ? 'um-secili' : '',
          cekilen === k.id ? 'um-cekilen' : '',
          oneri === k.id ? 'um-oneri' : '',
          gizli.has(k.id) ? 'um-gizli' : '',
        ].filter(Boolean).join(' ');
        return (
          <div
            key={k.id}
            ref={(el) => { if (el) ogeler.current.set(k.id, el); else ogeler.current.delete(k.id); }}
            className={sinif}
            data-kart={k.id}
            style={{ ['--x' as string]: `${p.x.toFixed(1)}px`, ['--y' as string]: `${p.y.toFixed(1)}px`, ['--a' as string]: `${p.a.toFixed(1)}deg`, zIndex: p.z, width: yer.kw, height: yer.kh, marginLeft: -yer.kw / 2, marginTop: -yer.kh / 2 }}
            role="button"
            tabIndex={etkin ? 0 : -1}
            aria-label={`${kartAdi(k, tema)}${fark && uygun ? ', oynanabilir' : ''}${secili === k.id ? ', seçili: oynamak için yeniden bas' : ''}`}
            aria-pressed={secili === k.id}
            onPointerDown={(e) => asagi(e, k.id)}
            onPointerMove={hareket}
            onPointerUp={(e) => bitir(e, false)}
            onPointerCancel={(e) => bitir(e, true)}
            onKeyDown={(e) => { if (etkin && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); onDokun(k.id); } }}
            onContextMenu={(e) => e.preventDefault()}
            onDragStart={(e) => e.preventDefault()}
          >
            <KartGorsel kart={k} tema={tema} boy={yer.kw} />
          </div>
        );
      })}
    </div>
  );
});

export default El;
