/** Sesli ders PDF terim yardımcısı (2026-10-26, scripts/sesli_anlatim/terim_sozlugu.py).
 *  - Yardımcı açık: slayttaki terimlerin 1–2 cümlelik açıklamaları slaytın altındaki boş alanda panel olarak durur;
 *    panel boşluğa sığmazsa sayfa yalnız gerektiği kadar uzatılır (onEk → PdfDocView ekAlt).
 *  - Yardımcı kapalı: terimlerin altı ince kesikli çizilir; dokununca açılır kartta açıklama gösterilir. */
import React, { useLayoutEffect, useRef, useSyncExternalStore } from 'react';
import { Info } from 'lucide-react';
import { Popover, PopoverContent, PopoverTrigger } from '../ui/radix';
import type { CdTerim, CdTerimSayfa } from './canliDersStore';

const ANAHTAR = 'cd-terim-yardimci';
const dinleyen = new Set<() => void>();
function okuAcik(): boolean {
  try { return localStorage.getItem(ANAHTAR) === '1'; } catch { return false; }
}
let acikDurum = okuAcik();
export function terimYardimciAyarla(v: boolean) {
  acikDurum = v;
  try { localStorage.setItem(ANAHTAR, v ? '1' : '0'); } catch { /* özel kip */ }
  dinleyen.forEach((f) => f());
}
export function useTerimYardimci(): boolean {
  return useSyncExternalStore((f) => { dinleyen.add(f); return () => { dinleyen.delete(f); }; }, () => acikDurum, () => false);
}

export const TERIM_TUR: Record<CdTerim['k'], string> = {
  terim: 'Tıbbi terim', latince: 'Latince / yabancı', karisan: 'Karıştırılabilir', kisaltma: 'Kısaltma',
};

/** PDF çubuğundaki ⓘ düğmesi */
export function TerimDugme() {
  const acik = useTerimYardimci();
  return (
    <button type="button" className={`cd-cik-btn cd-trm-btn${acik ? ' is-on' : ''}`} aria-pressed={acik}
      onClick={() => terimYardimciAyarla(!acik)}
      title={acik ? 'Terim yardımcısı açık: açıklamalar slayt altında. Kapatınca terimlere dokunarak okursun.' : 'Terim yardımcısı: slayttaki terimlerin kısa açıklamalarını slaytın altında göster'}
      aria-label="Terim yardımcısı">
      <Info aria-hidden /> <span className="cd-cik-ad">Terimler</span>
    </button>
  );
}

function Kart({ x }: { x: CdTerim }) {
  return (
    <>
      <div className="cd-trm-kart-bas">
        <b>{x.t}</b>
        <span className={`cd-trm-tur is-${x.k}`}>{TERIM_TUR[x.k]}</span>
      </div>
      <p>{x.a}</p>
      {x.f && <p className="cd-trm-f">Karıştırılan: <b>{x.f}</b></p>}
    </>
  );
}

/** Sayfa katmanı (pageOverlay içinde). bas: panelin başlayacağı ek ofset (çizim paneli ek alanı, sayfa oranı). */
export function CdTerimKatman({ sayfa, n, bas = 0, gizle, onEk }: {
  sayfa: CdTerimSayfa; n: number; bas?: number; gizle?: boolean; onEk: (n: number, h: number) => void;
}) {
  const acik = useTerimYardimci();
  const panelRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (!acik) { onEk(n, 0); return; }
    const el = panelRef.current;
    const kap = el?.parentElement?.parentElement; // .cd-trm-kat → .pdv-page
    if (!el || !kap) return;
    const olc = () => {
      const H = kap.offsetHeight;
      if (!H) return;
      const pay = 8;
      // boşluk: bas > 0 ise panel sayfanın (ve çizim ekinin) altından başlar; değilse alt boşluğa oturur
      const bosPx = bas > 0 ? 0 : sayfa.bos * H;
      const gerek = Math.max(0, el.offsetHeight + pay * 2 - bosPx) / H;
      onEk(n, gerek > 0.004 ? Math.ceil(gerek * 200) / 200 : 0);
    };
    olc();
    const ro = new ResizeObserver(olc);
    ro.observe(el); ro.observe(kap);
    return () => ro.disconnect();
  }, [acik, n, bas, sayfa, onEk]);

  if (!sayfa.t.length || gizle) return null;
  if (acik) {
    const ust = bas > 0 ? `calc(${(1 + bas) * 100}% + 8px)` : `calc(${(1 - sayfa.bos) * 100}% + 8px)`;
    return (
      <div className="cd-trm-kat">
        <div ref={panelRef} className="cd-trm-panel" style={{ top: ust }} role="note" aria-label={`Sayfa ${n} terimleri`}>
          {sayfa.t.map((x, i) => (
            <div key={i} className="cd-trm-oge">
              <span className="cd-trm-oge-t"><b>{x.t}</b><span className={`cd-trm-tur is-${x.k}`}>{TERIM_TUR[x.k]}</span></span>
              <span className="cd-trm-oge-a">{x.a}{x.f && <> <i>Karıştırılan: {x.f}.</i></>}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return (
    <div className="cd-trm-kat">
      {sayfa.t.flatMap((x, i) => x.b.map((b, j) => (
        <Popover key={`${i}-${j}`}>
          <PopoverTrigger asChild>
            <button type="button" className={`cd-trm is-${x.k}`} aria-label={`${x.t}: anlamını göster`}
              style={{ left: `${b[0] * 100}%`, top: `${b[1] * 100}%`, width: `${(b[2] - b[0]) * 100}%`, height: `${(b[3] - b[1]) * 100}%` }} />
          </PopoverTrigger>
          <PopoverContent className="cd-trm-kart" align="center" side="bottom" aria-label={x.t}>
            <Kart x={x} />
          </PopoverContent>
        </Popover>
      )))}
    </div>
  );
}

export default React.memo(CdTerimKatman);
