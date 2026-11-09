/** Çok katlı ahşap ıstaka: görünmez yuva ızgarası; taşlar yuvalarında durur, boşluklar oyuncunun kendi per gruplarını ayırır. */
import React, { useLayoutEffect, useRef } from 'react';
import type { Renk, Tas } from '../../../services/masa/tipler';
import type { Rect } from './surukle';
import { TasGorsel } from './Tas';
import type { YuvaDurum } from './yuva';

export interface IstakaProps {
  yuva: YuvaDurum;
  taslar: Map<number, Tas>;
  b: number;
  renkler: string[];
  tema: string;
  okey?: { s: number; r: Renk };
  secili: ReadonlySet<number>;
  kaynak: ReadonlySet<number>;
  ipucu: ReadonlySet<number>;
  gizli: ReadonlySet<number>;
  yeni: ReadonlySet<number>;
  sarsilan: ReadonlySet<string>;
  yandan?: number;
  siraBende: boolean;
  isilti: number;
  /** Taş seçiliyken yuvalar dokunma hedefi olur */
  hedefAcik: boolean;
  rectler: React.MutableRefObject<Map<number, Rect>>;
  sabit: React.MutableRefObject<Set<number>>;
  onYuva(i: number): void;
  onTus(id: number): void;
}

export default function Istaka(p: IstakaProps) {
  const ref = useRef<HTMLDivElement | null>(null);
  // Taşların son ekran konumu: elden çıkan taşın uçuşu buradan başlar
  useLayoutEffect(() => {
    const kok = ref.current;
    if (!kok) return;
    kok.querySelectorAll<HTMLElement>('[data-om-elt]').forEach((el) => {
      const id = +el.dataset.omElt!;
      if (p.sabit.current.has(id)) return;
      const r = el.getBoundingClientRect();
      p.rectler.current.set(id, { x: r.left, y: r.top, w: r.width, h: r.height });
    });
  });
  const katlar = Array.from({ length: p.yuva.kat }, (_, k) => k);
  return (
    <div ref={ref} className={`om-istaka${p.siraBende ? ' om-istaka--sira' : ''}${p.hedefAcik ? ' om-istaka--hedef' : ''}`} data-om-istaka="" data-om-hedef="istaka" style={{ '--om-b': `${p.b}px` } as React.CSSProperties}>
      {p.isilti > 0 && <span key={p.isilti} className="om-istaka-isilti" aria-hidden="true" />}
      <span className="om-istaka-baslik om-istaka-baslik--sol" aria-hidden="true" />
      <div className="om-istaka-govde">
        {katlar.map((k) => (
          <div className="om-istaka-kat" key={k}>
            {Array.from({ length: p.yuva.sutun }, (_, c) => {
              const i = k * p.yuva.sutun + c, id = p.yuva.d[i], tas = id === null ? undefined : p.taslar.get(id);
              return (
                <div className="om-yuva" key={c} data-om-hedef="yuva" data-i={i} onClick={() => p.onYuva(i)}>
                  {tas && (
                    <div
                      className={`om-elt${p.secili.has(tas.id) ? ' om-elt--secili' : ''}${p.kaynak.has(tas.id) ? ' om-elt--kaynak' : ''}${p.ipucu.has(tas.id) ? ' om-elt--ipucu' : ''}${p.gizli.has(tas.id) ? ' om-gizli' : ''}${p.yeni.has(tas.id) ? ' om-elt--yeni' : ''}${p.sarsilan.has(`t${tas.id}`) ? ' om-sars' : ''}${p.yandan === tas.id ? ' om-elt--yandan' : ''}`}
                      data-om-src="el" data-om-id={tas.id} data-om-elt={tas.id}
                      role="button" tabIndex={0} aria-pressed={p.secili.has(tas.id)}
                      onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); p.onTus(tas.id); } }}
                    >
                      <TasGorsel tas={tas} renkler={p.renkler} tema={p.tema} okey={p.okey} />
                      {p.yandan === tas.id && <span className="om-elt-not">kullanılmalı</span>}
                    </div>
                  )}
                </div>
              );
            })}
            <span className="om-istaka-pah" aria-hidden="true" />
          </div>
        ))}
      </div>
      <span className="om-istaka-baslik om-istaka-baslik--sag" aria-hidden="true" />
    </div>
  );
}
