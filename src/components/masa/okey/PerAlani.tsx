/** Masada açılan perler: satır satır otomatik yerleşim, uçlarda işleme yuvaları; per çoğaldıkça taş kademeli küçülür, taşmaz. */
import { Scissors } from 'lucide-react';
import React, { useLayoutEffect, useMemo, useRef, useState } from 'react';
import type { OdaGorunum, Per, Renk, Tas } from '../../../services/masa/tipler';
import { oyuncuAdi } from '../ortak';
import { TasGorsel, TAS_ORAN } from './Tas';

const UC = 0.62; // işleme yuvasının genişliği (taş genişliği oranı)
const etkinS = (t: Tas, okey?: { s: number; r: Renk }) => t.yerine?.s ?? (t.s === 0 && okey ? okey.s : t.s);

/** Perin açık uçları: seri baş/son (1'in altı, 13'ün üstü yok), 3'lü grup tek yuva */
function uclar(p: Per, okey?: { s: number; r: Renk }): { bas: boolean; son: boolean; grup: boolean } {
  if (p.tur === 'seri') return { bas: etkinS(p.taslar[0], okey) > 1, son: etkinS(p.taslar[p.taslar.length - 1], okey) < 13, grup: false };
  return { bas: false, son: false, grup: p.tur === 'grup' && p.taslar.length === 3 };
}

export interface PerAlaniProps {
  oda: OdaGorunum;
  perler: Per[];
  okey?: { s: number; r: Renk };
  /** Sürüklenen/seçili taşın uyduğu uçlar: `${per}:${uc ?? ''}` */
  uygun: ReadonlySet<string>;
  /** Bir taş sürükleniyor ya da seçili: yuvalar belirir */
  aktif: boolean;
  yeniUygun: boolean;
  gizli: ReadonlySet<number>;
  hale: ReadonlySet<number>;
  ipucuPer?: number;
  /** Seriyi bölerek işlenecek taşın sayısı (uygun kümesinde `${per}:bol` varsa o sayının üstünde makas hedefi çıkar) */
  bolSayi?: number;
  bolunen: ReadonlySet<number>;
  ipucuYeni: boolean;
  enBuyuk: number;
  onUc(per: number, uc: 'bas' | 'son' | 'bol' | null): void;
  onPer(per: number): void;
  onYeni(): void;
}

export default function PerAlani(p: PerAlaniProps) {
  const ref = useRef<HTMLDivElement | null>(null);
  const [kap, setKap] = useState({ w: 0, h: 0 });
  useLayoutEffect(() => {
    const el = ref.current!;
    const olc = () => setKap((k) => (k.w === el.clientWidth && k.h === el.clientHeight ? k : { w: el.clientWidth, h: el.clientHeight }));
    olc();
    const ro = new ResizeObserver(olc);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  const bilgi = useMemo(() => p.perler.map((per) => ({ per, uc: uclar(per, p.okey) })), [p.perler, p.okey]);
  // En büyük sığan taş boyu: satırlara açgözlü paketleme benzetimi
  const b = useMemo(() => {
    const W = kap.w - 16, H = kap.h - 12;
    if (W <= 0 || H <= 0) return 30;
    const sigar = (x: number) => {
      const ara = Math.round(x * 0.3), satirH = x * TAS_ORAN + 20;
      let satir = 1, dolu = 0;
      const koy = (w: number) => { if (dolu && dolu + ara + w > W) { satir++; dolu = w; } else dolu += (dolu ? ara : 0) + w; };
      for (const { per, uc } of bilgi) koy(per.taslar.length * (x + 1) + ((uc.bas ? 1 : 0) + (uc.son || uc.grup ? 1 : 0)) * (x * UC + 2) + 4);
      koy(x * 1.7);
      return satir * satirH <= H;
    };
    for (let x = p.enBuyuk; x >= 20; x -= 2) if (sigar(x)) return x;
    return 20;
  }, [bilgi, kap, p.enBuyuk]);

  return (
    <div ref={ref} className={`om-peralan${p.aktif ? ' om-peralan--aktif' : ''}${p.yeniUygun ? ' om-peralan--yeni' : ''}`} data-om-hedef="yeni" onClick={(e) => { if (e.target === e.currentTarget || (e.target as HTMLElement).classList.contains('om-peralan-ic')) p.onYeni(); }}>
      <div className="om-peralan-ic" style={{ '--om-b': `${b}px`, gap: `6px ${Math.round(b * 0.3)}px` } as React.CSSProperties}>
        {!p.perler.length && <p className="om-peralan-bos">Açılan perler burada dizilir</p>}
        {bilgi.map(({ per, uc }) => {
          const ucYuva = (u: 'bas' | 'son' | null) => (
            <button
              type="button" key={`u${u}`} className={`om-uc${p.uygun.has(`${per.id}:${u ?? ''}`) ? ' om-uc--uygun' : ''}`}
              data-om-hedef="uc" data-per={per.id} data-uc={u ?? ''} tabIndex={p.uygun.has(`${per.id}:${u ?? ''}`) ? 0 : -1}
              aria-label={u === 'bas' ? 'Serinin başına işle' : u === 'son' ? 'Serinin sonuna işle' : 'Gruba işle'}
              onClick={(e) => { e.stopPropagation(); p.onUc(per.id, u); }}
            />
          );
          const perUygun = [...p.uygun].some((k) => k.startsWith(`${per.id}:`));
          return (
            <div key={per.id} className={`om-per om-per--${per.tur}${perUygun ? ' om-per--uygun' : ''}${p.aktif && !perUygun ? ' om-per--sonuk' : ''}${p.ipucuPer === per.id ? ' om-per--ipucu' : ''}${p.bolunen.has(per.id) ? ' om-per--bolundu' : ''}`} data-om-hedef="per" data-per={per.id} onClick={(e) => { e.stopPropagation(); p.onPer(per.id); }}>
              <span className="om-per-sahip">{per.sahip === p.oda.ben ? 'Sen' : oyuncuAdi(p.oda, per.sahip)}</span>
              <div className="om-per-taslar">
                {uc.bas && ucYuva('bas')}
                {per.taslar.map((t) => (
                  <span key={t.id} className={`om-pertas${p.gizli.has(t.id) ? ' om-gizli' : ''}${p.hale.has(t.id) ? ' om-pertas--hale' : ''}`} data-om-pertas={t.id}>
                    <TasGorsel tas={t} renkler={p.oda.ayar.renkler} tema={p.oda.ayar.tema} okey={p.okey} />
                    {p.bolSayi === t.s && p.uygun.has(`${per.id}:bol`) && (
                      <button type="button" className="om-bol" data-om-hedef="uc" data-per={per.id} data-uc="bol" aria-label={`Seriyi ${t.s} taşından bölerek işle`} onClick={(e) => { e.stopPropagation(); p.onUc(per.id, 'bol'); }}>
                        <Scissors size={Math.max(12, Math.round(b * 0.42))} aria-hidden="true" />
                      </button>
                    )}
                  </span>
                ))}
                {uc.son && ucYuva('son')}
                {uc.grup && ucYuva(null)}
              </div>
            </div>
          );
        })}
        <button type="button" className={`om-yeniper${p.ipucuYeni ? ' om-yeniper--ipucu' : ''}`} tabIndex={p.yeniUygun ? 0 : -1} onClick={(e) => { e.stopPropagation(); p.onYeni(); }} aria-label="Seçili taşlarla yeni per aç">
          <span>+ Yeni per</span>
        </button>
      </div>
    </div>
  );
}
