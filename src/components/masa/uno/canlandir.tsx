import React, { useCallback, useEffect, useLayoutEffect, useRef, useSyncExternalStore } from 'react';
import type { OdaGorunum, Olay, UnoGorunum, UnoKart, UnoRenk } from '../../../services/masa/tipler';
import { masa } from '../../../services/masa/istemci';
import { azHareket, sesCal, titret } from '../ortak';
import { KartGorsel } from './Kart';
import { damgaNokta, oyuncuNokta, type KartYer, type Nokta, type Yerlesim } from './yerlesim';

/* ---------------- sahne deposu: uçan kartlar + damgalar (masayı yeniden çizdirmeden) ---------------- */

export interface Ucus {
  key: number;
  kart?: UnoKart;
  /** Kapalı uçar; `cevir` ile birlikteyse kapalıdan açığa döner */
  kapali?: boolean;
  cevir?: boolean;
  w: number;
  x0: number; y0: number; a0: number; s0: number;
  x1: number; y1: number; a1: number; s1: number;
  sure: number;
  gecikme: number;
  bitince?: () => void;
}
export interface Damga {
  key: number;
  tur: 'arti' | 'atla' | 'uno' | 'yakala' | 'renk' | 'bilgi';
  metin?: string;
  alt?: string;
  x: number; y: number;
  renk?: UnoRenk;
}
const DAMGA_SURE: Record<Damga['tur'], number> = { arti: 1500, atla: 1300, uno: 1500, yakala: 1700, renk: 950, bilgi: 1100 };

export class SahneDeposu {
  private no = 1;
  private durum: { ucuslar: Ucus[]; damgalar: Damga[] } = { ucuslar: [], damgalar: [] };
  private aboneler = new Set<() => void>();
  private zamanlar = new Set<number>();
  abone = (f: () => void) => { this.aboneler.add(f); return () => { this.aboneler.delete(f); }; };
  oku = () => this.durum;
  private yaz(p: Partial<SahneDeposu['durum']>) { this.durum = { ...this.durum, ...p }; this.aboneler.forEach((f) => f()); }
  ucur(u: Omit<Ucus, 'key'>) { this.yaz({ ucuslar: [...this.durum.ucuslar, { ...u, key: this.no++ }] }); }
  ucusSil(key: number) { this.yaz({ ucuslar: this.durum.ucuslar.filter((u) => u.key !== key) }); }
  damga(d: Omit<Damga, 'key'>) {
    const key = this.no++;
    this.yaz({ damgalar: [...this.durum.damgalar, { ...d, key }] });
    const t = window.setTimeout(() => { this.zamanlar.delete(t); this.yaz({ damgalar: this.durum.damgalar.filter((x) => x.key !== key) }); }, DAMGA_SURE[d.tur]);
    this.zamanlar.add(t);
  }
  temizle() { this.zamanlar.forEach((t) => clearTimeout(t)); this.zamanlar.clear(); this.durum = { ucuslar: [], damgalar: [] }; }
}

const donusum = (x: number, y: number, a: number, s: number, w: number) =>
  `translate3d(${(x - w / 2).toFixed(1)}px, ${(y - w * 0.75).toFixed(1)}px, 0) rotate(${a.toFixed(1)}deg) scale(${s.toFixed(3)})`;

function UcusOge({ u, tema, depo }: { u: Ucus; tema: string; depo: SahneDeposu }) {
  const ref = useRef<HTMLDivElement>(null);
  const icRef = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    const el = ref.current;
    let bitti = false;
    const bitir = () => { if (bitti) return; bitti = true; try { u.bitince?.(); } finally { depo.ucusSil(u.key); } };
    const sade = azHareket();
    const sure = sade ? 80 : u.sure;
    const secenek: KeyframeAnimationOptions = { duration: sure, delay: u.gecikme, easing: 'cubic-bezier(.3,.7,.25,1)', fill: 'both' };
    const anlar: Animation[] = [];
    try {
      if (el) {
        const orta = donusum((u.x0 + u.x1) / 2, (u.y0 + u.y1) / 2 - (sade ? 0 : 14), (u.a0 + u.a1) / 2, Math.max(u.s0, u.s1) * (sade ? 1 : 1.08), u.w);
        anlar.push(el.animate([{ transform: donusum(u.x0, u.y0, u.a0, u.s0, u.w) }, { transform: orta }, { transform: donusum(u.x1, u.y1, u.a1, u.s1, u.w) }], secenek));
        anlar[0].onfinish = bitir;
      }
      if (u.cevir && icRef.current) anlar.push(icRef.current.animate([{ transform: 'rotateY(180deg)' }, { transform: 'rotateY(0deg)' }], { ...secenek, easing: 'ease-in-out' }));
    } catch { /* animasyon yoksa zamanlayıcı bitirir */ }
    const t = window.setTimeout(bitir, sure + u.gecikme + 300);
    return () => { clearTimeout(t); anlar.forEach((a) => { a.onfinish = null; a.cancel(); }); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return (
    <div ref={ref} className="um-ucus" style={{ width: u.w, height: u.w * 1.5, transform: donusum(u.x0, u.y0, u.a0, u.s0, u.w) }}>
      <div ref={icRef} className={`um-ucus-ic${u.cevir ? ' um-ucus-cevir' : ''}`}>
        {u.cevir
          ? (<><KartGorsel kart={u.kart} tema={tema} boy={u.w} className="um-ucus-on" /><KartGorsel tema={tema} boy={u.w} kapali className="um-ucus-arka" /></>)
          : <KartGorsel kart={u.kart} tema={tema} boy={u.w} kapali={u.kapali} />}
      </div>
    </div>
  );
}

export function SahneKatmani({ depo, tema }: { depo: SahneDeposu; tema: string }) {
  const { ucuslar, damgalar } = useSyncExternalStore(depo.abone, depo.oku, depo.oku);
  return (
    <div className="um-sahne" aria-hidden="true">
      {damgalar.map((d) => (
        <div key={d.key} className="um-damga-yer" style={{ transform: `translate3d(${d.x}px, ${d.y}px, 0)` }}>
          <div className={`um-damga um-damga-${d.tur}${d.renk ? ' um-r-' + d.renk : ''}`}>
            {d.metin && <span className="um-damga-metin">{d.metin}</span>}
            {d.alt && <span className="um-damga-alt">{d.alt}</span>}
          </div>
        </div>
      ))}
      {ucuslar.map((u) => <UcusOge key={u.key} u={u} tema={tema} depo={depo} />)}
    </div>
  );
}

/* ---------------- olay → canlandırma ---------------- */

/** Atıktaki kartın duruş açısı (kimlikten türetilir: uçuşun iniş açısıyla aynı) */
export const yiginAci = (id: number) => ((id * 37) % 41) - 20;

export interface Baglam {
  yer: Yerlesim | null;
  elPoz: Map<number, KartYer>;
  /** Oynanan kartın çıkış noktası (sürükleyip bırakılan yer ya da eldeki yeri) */
  kaynak: Map<number, Nokta & { a?: number; s?: number }>;
  /** Desteden sürüklenip bırakılan nokta */
  cekKaynak: (Nokta & { t: number }) | null;
  atikBekle: (id: number) => void;
  yiginEkle: (kart: UnoKart, vurgu: boolean) => void;
  yiginSifirla: () => void;
  yiginKirp: () => void;
  gizle: (idler: number[]) => void;
  goster: (idler: number[]) => void;
  sars: (id: string) => void;
  yonVur: () => void;
  siraVur: () => void;
}

/** Sunucu olaylarını sırayla canlandırır: her olay bir kez; olaylar art arda (zaman imleci) oynar. */
let sonDagit = '';

export function useOlayCanlandir(bRef: React.MutableRefObject<Baglam>, depo: SahneDeposu) {
  const z = useRef({ imlec: 0, zamanlar: new Set<number>() });
  const isle = useCallback((olaylar: Olay[], oda: OdaGorunum) => {
      const zamanlar = z.current.zamanlar;
      const sonra = (ms: number, fn: () => void) => {
        const t = window.setTimeout(() => { zamanlar.delete(t); try { fn(); } catch (e) { console.warn('[uno] canlandırma', e); } }, Math.max(0, ms));
        zamanlar.add(t);
      };
      if (!oda.oyun || oda.oyun.tur !== 'uno') return;
      const oyun = oda.oyun as UnoGorunum;
      const ben = oda.ben;
      const b0 = bRef.current;
      const simdi = performance.now();
      let t = Math.max(simdi, z.current.imlec);
      if (t - simdi > 1800) t = simdi + 150; // birikme: bekletme, öne al
      const at = (fn: (b: Baglam, yer: Yerlesim) => void, yoksa?: (b: Baglam) => void) =>
        sonra(t - simdi, () => { const b = bRef.current; if (b.yer) fn(b, b.yer); else yoksa?.(b); });
      const ad = (id: string) => oda.oyuncular.find((o) => o.id === id)?.ad || 'Oyuncu';

      olaylar.forEach((o, i) => {
        const kim = typeof o.o === 'string' ? o.o : '';
        const benMi = kim === ben;
        switch (o.t) {
          case 'dagit': {
            const anahtar = `${oda.kod}:${oda.elNo}`;
            if (sonDagit === anahtar) break;
            sonDagit = anahtar;
            const idler = oyun.elim.map((k) => k.id);
            b0.gizle(idler);
            b0.yiginSifirla();
            b0.atikBekle(oyun.ust.id);
            const sira = oyun.oyuncular.map((p) => p.id);
            const tur = Math.max(1, ...oyun.oyuncular.map((p) => p.kartSayisi));
            const toplam = sira.length * tur;
            const adim = Math.min(70, 1500 / toplam);
            at((b, yer) => {
              sesCal('dagit');
              let k = 0;
              for (let r = 0; r < tur; r++) for (const id of sira) {
                const gecikme = k++ * adim;
                if (id === ben) {
                  const kid = idler[r];
                  if (kid === undefined) continue;
                  const h = b.elPoz.get(kid) ?? { ...oyuncuNokta(yer, ben, ben), a: 0 };
                  depo.ucur({ kapali: true, w: yer.kw, x0: yer.deste.x, y0: yer.deste.y, a0: 0, s0: yer.pk / yer.kw, x1: h.x, y1: h.y, a1: h.a, s1: 1, sure: 330, gecikme, bitince: () => bRef.current.goster([kid]) });
                } else if (yer.koltuk[id]) {
                  const p = yer.koltuk[id];
                  depo.ucur({ kapali: true, w: yer.pk, x0: yer.deste.x, y0: yer.deste.y, a0: 0, s0: 1, x1: p.x, y1: p.y, a1: 40, s1: Math.max(14, yer.mk) / yer.pk, sure: 330, gecikme });
                }
              }
              depo.ucur({ kart: oyun.ust, cevir: true, w: yer.pk, x0: yer.deste.x, y0: yer.deste.y, a0: 0, s0: 1, x1: yer.atik.x, y1: yer.atik.y, a1: yiginAci(oyun.ust.id) * 0.3, s1: 1, sure: 460, gecikme: toplam * adim + 150, bitince: () => { bRef.current.yiginEkle(oyun.ust, false); sesCal('birak'); } });
            }, (b) => { b.goster(idler); b.yiginEkle(oyun.ust, false); });
            t += toplam * adim + 800;
            sonra(t - simdi + 600, () => bRef.current.goster(idler));
            if (oyun.sira === ben) sonra(t - simdi, () => { sesCal('sira'); bRef.current.siraVur(); });
            break;
          }
          case 'oynadi': {
            const kart = o.kart as UnoKart;
            if (!kart) break;
            b0.atikBekle(kart.id);
            at((b, yer) => {
              const k = b.kaynak.get(kart.id);
              b.kaynak.delete(kart.id);
              const p = benMi ? (k ?? oyuncuNokta(yer, ben, ben)) : oyuncuNokta(yer, kim, ben);
              depo.ucur({
                kart, cevir: !benMi, w: yer.pk,
                x0: p.x, y0: p.y, a0: benMi ? (k?.a ?? 0) : -30, s0: benMi ? (yer.kw / yer.pk) * (k?.s ?? 1) : Math.max(14, yer.mk) / yer.pk,
                x1: yer.atik.x, y1: yer.atik.y, a1: yiginAci(kart.id) * 0.3, s1: 1,
                sure: benMi ? 260 : 430, gecikme: 0,
                bitince: () => { bRef.current.yiginEkle(kart, !benMi); sesCal('birak'); if (benMi) titret(10); },
              });
            }, (b) => b.yiginEkle(kart, false));
            t += benMi ? 240 : 420;
            break;
          }
          case 'renk': {
            const renk = o.renk as UnoRenk;
            at((_b, yer) => depo.damga({ tur: 'renk', renk, x: yer.atik.x, y: yer.atik.y }));
            t += 160;
            break;
          }
          case 'cekti': {
            const adet = Number(o.adet) || 0;
            const neden = String(o.neden || 'cek');
            let kartlar: UnoKart[] = [];
            if (benMi) {
              const c = olaylar.slice(i + 1).find((e) => e.t === 'cektim');
              kartlar = Array.isArray(c?.kartlar) ? (c!.kartlar as UnoKart[]) : [];
              b0.gizle(kartlar.map((k) => k.id));
            }
            const idler = kartlar.map((k) => k.id);
            if (!adet) break;
            at((b, yer) => {
              if (neden === '+2' || neden === '+4') {
                const d = damgaNokta(yer, kim, ben);
                depo.damga({ tur: 'arti', metin: neden, x: d.x, y: d.y });
                if (benMi) titret([20, 40, 20]);
              }
              const ck = b.cekKaynak;
              b.cekKaynak = null;
              const bas = benMi && neden === 'cek' && ck && performance.now() - ck.t < 1500 ? ck : yer.deste;
              for (let j = 0; j < adet; j++) {
                const gecikme = j * 95;
                if (benMi) {
                  const kart = kartlar[j];
                  const h = (kart && b.elPoz.get(kart.id)) || { ...oyuncuNokta(yer, ben, ben), a: 0 };
                  depo.ucur({ kart, kapali: !kart, cevir: !!kart, w: yer.kw, x0: bas.x, y0: bas.y, a0: 0, s0: yer.pk / yer.kw, x1: h.x, y1: h.y, a1: h.a, s1: 1, sure: 380, gecikme, bitince: () => { if (kart) bRef.current.goster([kart.id]); sesCal('cek'); } });
                } else {
                  const p = oyuncuNokta(yer, kim, ben);
                  depo.ucur({ kapali: true, w: yer.pk, x0: yer.deste.x, y0: yer.deste.y, a0: 0, s0: 1, x1: p.x, y1: p.y, a1: 40, s1: Math.max(14, yer.mk) / yer.pk, sure: 360, gecikme, bitince: j === 0 ? () => sesCal('cek') : undefined });
                }
              }
            }, (b) => b.goster(idler));
            t += adet * 95 + 280;
            if (idler.length) sonra(t - simdi + 900, () => bRef.current.goster(idler));
            break;
          }
          case 'atlandi':
            at((_b, yer) => { const d = damgaNokta(yer, kim, ben); depo.damga({ tur: 'atla', metin: 'Atlandı', x: d.x, y: d.y }); sesCal('tas'); });
            t += 320;
            break;
          case 'yon':
            at((b) => { b.yonVur(); sesCal('isle'); });
            t += 180;
            break;
          case 'uno':
            at((_b, yer) => { depo.damga({ tur: 'uno', metin: 'UNO!', alt: benMi ? 'Tek kartın kaldı' : ad(kim), x: yer.W / 2, y: Math.min(yer.atik.y, yer.elUst * 0.5) }); sesCal('uno'); titret(25); });
            t += 380;
            break;
          case 'yakalandi':
            at((b, yer) => {
              const d = damgaNokta(yer, kim, ben);
              depo.damga({ tur: 'yakala', metin: 'Yakalandı! +2', alt: benMi ? 'UNO demeyi unuttun' : undefined, x: d.x, y: d.y });
              b.sars(kim);
              sesCal('ceza');
              if (benMi) titret([40, 50, 40]);
            });
            t += 480;
            break;
          case 'atladi':
            at((_b, yer) => { const d = damgaNokta(yer, kim, ben); depo.damga({ tur: 'bilgi', metin: 'Atladı!', alt: benMi ? 'Tıpkı kartla sıranı aldın' : ad(kim), x: d.x, y: d.y }); sesCal('uno'); });
            t += 300;
            break;
          case 'itiraz':
            at((b, yer) => {
              const hakli = !!o.hakli, ceken = hakli ? (o.hedef as string) : kim;
              const d = damgaNokta(yer, ceken, ben);
              depo.damga({ tur: 'yakala', metin: hakli ? 'İtiraz haklı! +4' : 'İtiraz boşa! +6', alt: hakli ? '+4 kuralsız oynanmıştı' : '+4 kurala uygundu', x: d.x, y: d.y });
              b.sars(ceken); sesCal('ceza');
            });
            t += 520;
            break;
          case 'yigin':
            at((_b, yer) => { depo.damga({ tur: 'arti', metin: `Biriken +${o.adet}`, x: yer.atik.x, y: yer.atik.y }); sesCal('isle'); });
            t += 300;
            break;
          case 'takas':
          case 'devir':
            at((_b, yer) => { depo.damga({ tur: 'bilgi', metin: o.t === 'takas' ? 'Eller takas edildi' : 'Eller döndü', alt: o.t === 'takas' ? `${ad(kim)} ↔ ${ad(o.hedef as string)}` : undefined, x: yer.W / 2, y: yer.atik.y }); sesCal('isle'); });
            t += 420;
            break;
          case 'karildi':
            at((b, yer) => {
              for (let j = 0; j < 6; j++) depo.ucur({ kapali: true, w: yer.pk, x0: yer.atik.x, y0: yer.atik.y, a0: yiginAci(j * 7), s0: 1, x1: yer.deste.x, y1: yer.deste.y, a1: 360, s1: 1, sure: 420, gecikme: j * 55 });
              b.yiginKirp();
              sesCal('dagit');
            }, (b) => b.yiginKirp());
            t += 520;
            break;
          case 'pas':
            if (!benMi) at((_b, yer) => { const d = damgaNokta(yer, kim, ben); depo.damga({ tur: 'bilgi', metin: 'Geçti', x: d.x, y: d.y }); });
            t += 120;
            break;
          case 'sira':
            if (benMi) sonra(t - simdi, () => { sesCal('sira'); titret(15); bRef.current.siraVur(); });
            break;
          default:
        }
      });
      z.current.imlec = t;
  }, [bRef, depo]);
  useEffect(() => {
    const zamanlar = z.current.zamanlar;
    const dur = masa.olayDinle(isle);
    return () => { dur(); zamanlar.forEach((x) => clearTimeout(x)); zamanlar.clear(); depo.temizle(); };
  }, [isle, depo]);
  return isle;
}
