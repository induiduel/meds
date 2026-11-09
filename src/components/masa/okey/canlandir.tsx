/** Olay → canlandırma: uçuş kuyruğu, gizlenen/haleli taşlar, ceza kartı, hediye şeridi, son hamleler akışı. Durum kaynağı değildir. */
import React, { useLayoutEffect, useRef, useSyncExternalStore } from 'react';
import type { Ceza, OdaGorunum, OkeyGorunum, Olay, Per, Renk, Tas } from '../../../services/masa/tipler';
import { azHareket, oyuncuAdi, sesCal, titret } from '../ortak';
import type { Rect } from './surukle';
import { TasGorsel } from './Tas';

type Nokta = { sec: string } | { rect: Rect };
export interface Ucus { id: number; tas: Tas | null; kimden: Nokta; hedef: string; gecikme: number; gizle?: number; hale?: boolean; yeni?: boolean; kucuk?: boolean }
export interface CezaKart { anahtar: number; o: string; ceza: Ceza }
export interface CanDurum {
  ucuslar: Ucus[];
  gizli: ReadonlySet<number>;
  hale: ReadonlySet<number>;
  yeni: ReadonlySet<number>;
  ceza: CezaKart | null;
  serit: { anahtar: number; metin: string } | null;
  akis: { id: number; metin: string }[];
  sarsilan: ReadonlySet<string>;
  /** Az önce bölünen serinin iki parçası (per kimlikleri) */
  bolunen: ReadonlySet<number>;
  /** Sıra bana geldikçe artar (ıstaka ışıltısı) */
  isilti: number;
}
const BOS: CanDurum = { ucuslar: [], gizli: new Set(), hale: new Set(), yeni: new Set(), ceza: null, serit: null, akis: [], sarsilan: new Set(), bolunen: new Set(), isilti: 0 };
let durum = BOS;
const aboneler = new Set<() => void>();
const yaz = (p: Partial<CanDurum>) => { durum = { ...durum, ...p }; aboneler.forEach((f) => f()); };
export const canAbone = (f: () => void) => { aboneler.add(f); return () => { aboneler.delete(f); }; };
export const canOku = () => durum;
export const useCan = () => useSyncExternalStore(canAbone, canOku, canOku);

let sayac = 1;
let saat = 0;
const cezaKuyruk: CezaKart[] = [];
let cezaZaman: any = null;
const ekle = (s: ReadonlySet<any>, ...x: any[]) => { const n = new Set(s); x.forEach((v) => n.add(v)); return n; };
const cikar = (s: ReadonlySet<any>, ...x: any[]) => { const n = new Set(s); x.forEach((v) => n.delete(v)); return n; };

export function canSifirla() { cezaKuyruk.length = 0; clearTimeout(cezaZaman); cezaZaman = null; saat = 0; durum = BOS; aboneler.forEach((f) => f()); }

function cezaGoster() {
  const k = cezaKuyruk.shift();
  if (!k) { cezaZaman = null; yaz({ ceza: null }); return; }
  sesCal('ceza'); titret([30, 40, 30]);
  yaz({ ceza: k, sarsilan: ekle(durum.sarsilan, k.o) });
  setTimeout(() => yaz({ sarsilan: cikar(durum.sarsilan, k.o) }), 700);
  cezaZaman = setTimeout(cezaGoster, 2300);
}

export function sarsTas(ids: number[]) {
  const a = ids.map((i) => `t${i}`);
  yaz({ sarsilan: ekle(durum.sarsilan, ...a) });
  setTimeout(() => yaz({ sarsilan: cikar(durum.sarsilan, ...a) }), 450);
}

export function ucusBitti(u: Ucus) {
  const p: Partial<CanDurum> = { ucuslar: durum.ucuslar.filter((x) => x.id !== u.id) };
  if (u.gizle !== undefined) {
    const id = u.gizle;
    p.gizli = cikar(durum.gizli, id);
    if (u.hale) { p.hale = ekle(durum.hale, id); setTimeout(() => yaz({ hale: cikar(durum.hale, id) }), 2600); }
    if (u.yeni) { p.yeni = ekle(durum.yeni, id); setTimeout(() => yaz({ yeni: cikar(durum.yeni, id) }), 1300); }
  }
  yaz(p);
}

const sayilar = (taslar: Tas[]) => taslar.map((t) => t.yerine?.s ?? (t.s || '★')).join('-');
const koltuk = (id: string): Nokta => ({ sec: `[data-om-koltuk="${id}"]` });
const DESTE: Nokta = { sec: '[data-om-deste]' };

/** Bir sunucu paketinin olaylarını sıraya koyar. `rectAl`: benim taşımın son bilinen (ya da bırakıldığı) ekran konumu. */
export function olaylariIsle(olaylar: Olay[], oda: OdaGorunum, rectAl: (id: number) => Rect | undefined) {
  const g = oda.oyun as OkeyGorunum | undefined;
  if (!g || g.tur === ('uno' as string)) return;
  const ben = oda.ben, sade = azHareket();
  const simdi = performance.now();
  let t = Math.max(simdi, saat);
  const ucus: Ucus[] = [], gizle: number[] = [], haleHemen: number[] = [], akis: string[] = [], bolunen: number[] = [];
  let isilti = durum.isilti, serit = durum.serit;
  const benimKaynak = (id: number): Nokta => { const r = rectAl(id); return r ? { rect: r } : { sec: '[data-om-istaka]' }; };
  const ekleUcus = (u: Omit<Ucus, 'id' | 'gecikme'>, adim = 70) => {
    if (sade) { if (u.hale && u.gizle !== undefined) haleHemen.push(u.gizle); return; }
    ucus.push({ ...u, id: sayac++, gecikme: t - simdi });
    if (u.gizle !== undefined) gizle.push(u.gizle);
    t += adim;
  };
  const ad = (id?: string) => (id === ben ? 'Sen' : oyuncuAdi(oda, id));
  /** Türkçe çekim: 'Defne açtı' / 'Sen açtın' */
  const f = (o: string | undefined, fiil: string) => (o === ben ? `${fiil}n` : fiil);
  const cekilenler = new Set<number>();
  for (const e of olaylar) {
    const o = e.o as string | undefined;
    switch (e.t) {
      case 'dagit':
        sesCal('dagit');
        g.elim.forEach((ts) => ekleUcus({ tas: ts, kimden: DESTE, hedef: `[data-om-elt="${ts.id}"]`, gizle: ts.id }, 38));
        akis.push('Taşlar dağıtıldı');
        break;
      case 'cekti': {
        const tas = e.tas as Tas | undefined, atik = e.kaynak === 'atik';
        const i = g.oyuncular.findIndex((x) => x.id === o);
        const onceki = g.oyuncular[(i - 1 + g.oyuncular.length) % g.oyuncular.length]?.id;
        const kimden: Nokta = atik ? { sec: `[data-om-atik="${onceki}"]` } : DESTE;
        if (o === ben) {
          if (tas && !e.bos) { cekilenler.add(tas.id); ekleUcus({ tas, kimden, hedef: `[data-om-elt="${tas.id}"]`, gizle: tas.id, yeni: true }); sesCal('cek'); }
        } else if (!e.bos) { ekleUcus({ tas: atik && tas ? tas : null, kimden, hedef: `[data-om-koltuk="${o}"]`, kucuk: true }); sesCal('cek'); }
        akis.push(e.cezaTasi ? `${ad(o)} ceza taşı ${f(o, 'çekti')}` : atik ? `${ad(o)} yandan taş ${f(o, 'aldı')}` : e.bos ? `${ad(o)} ${f(o, 'çekemedi')}: deste bitti` : `${ad(o)} taş ${f(o, 'çekti')}`);
        break;
      }
      case 'cektim': {
        const tas = e.tas as Tas;
        if (!tas || cekilenler.has(tas.id)) break;
        ekleUcus({ tas, kimden: DESTE, hedef: `[data-om-elt="${tas.id}"]`, gizle: tas.id, yeni: true });
        sesCal('cek');
        break;
      }
      case 'acti': {
        const perler = (e.perler as Per[]) || [];
        for (const p of perler) for (const ts of p.taslar) ekleUcus({ tas: ts, kimden: o === ben ? benimKaynak(ts.id) : koltuk(o!), hedef: `[data-om-pertas="${ts.id}"]`, gizle: ts.id, hale: o !== ben });
        sesCal('ac');
        akis.push(`${ad(o)} ${perler.map((p) => sayilar(p.taslar)).join(' · ')} ${f(o, 'açtı')}`);
        break;
      }
      case 'isledi': {
        const ts = e.tas as Tas;
        ekleUcus({ tas: ts, kimden: o === ben ? benimKaynak(ts.id) : koltuk(o!), hedef: `[data-om-pertas="${ts.id}"]`, gizle: ts.id, hale: o !== ben });
        sesCal('isle');
        if (e.uc === 'bol') {
          const ikisi = [e.per as number, e.yeniPer as number].filter((x) => typeof x === 'number');
          bolunen.push(...ikisi);
          setTimeout(() => yaz({ bolunen: cikar(durum.bolunen, ...ikisi) }), 900);
        }
        akis.push(e.uc === 'bol' ? `${ad(o)} ${ts.s} ile seriyi ${f(o, 'böldü')}` : `${ad(o)} ${ts.s || 'sahte okey'} ${f(o, 'işledi')}`);
        break;
      }
      case 'atti': {
        const ts = e.tas as Tas;
        ekleUcus({ tas: ts, kimden: o === ben ? benimKaynak(ts.id) : koltuk(o!), hedef: `[data-om-atiktas="${ts.id}"]`, gizle: ts.id });
        sesCal('birak');
        akis.push(`${ad(o)} ${ts.s || 'sahte okey'} ${f(o, 'attı')}`);
        break;
      }
      case 'geriKoydu': akis.push(`${ad(o)} yandan ${o === ben ? 'aldığını' : 'aldığını'} geri ${f(o, 'koydu')}`); break;
      case 'devretti': akis.push(`${ad(o)} eli ${f(o, 'devretti')}`); break;
      case 'ceza': {
        const ceza = e.ceza as Ceza;
        cezaKuyruk.push({ anahtar: sayac++, o: o!, ceza });
        akis.push(`${ad(o)} ceza ${f(o, 'aldı')} (${String(ceza.puan).replace('-', '−')})`);
        break;
      }
      case 'hediye': {
        const kimler = (e.kimler as string[]) || [];
        serit = { anahtar: sayac++, metin: `Hediye taş! ${ad(o)} grubu ${f(o, 'dörtledi')}` };
        const an = serit.anahtar;
        setTimeout(() => { if (durum.serit?.anahtar === an) yaz({ serit: null }); }, 2400);
        kimler.filter((k) => k !== ben).forEach((k) => ekleUcus({ tas: null, kimden: DESTE, hedef: `[data-om-koltuk="${k}"]`, kucuk: true }));
        akis.push(`${ad(o)} hediye taş ${f(o, 'verdirdi')}`);
        break;
      }
      case 'sira': if (o === ben && oda.asama === 'oyun') { isilti++; sesCal('sira'); titret(20); } break;
      case 'elBitti': akis.push('El bitti'); break;
      default: break;
    }
  }
  saat = t;
  if (gizle.length) setTimeout(() => { // güvenlik: uçuş bir nedenle bitmezse taş gizli kalmasın
    const kalan = gizle.filter((id) => durum.gizli.has(id) && !durum.ucuslar.some((u) => u.gizle === id));
    if (kalan.length) yaz({ gizli: cikar(durum.gizli, ...kalan) });
  }, t - simdi + 1600);
  if (haleHemen.length) setTimeout(() => yaz({ hale: cikar(durum.hale, ...haleHemen) }), 2600);
  yaz({
    ucuslar: ucus.length ? [...durum.ucuslar, ...ucus] : durum.ucuslar,
    gizli: gizle.length ? ekle(durum.gizli, ...gizle) : durum.gizli,
    hale: haleHemen.length ? ekle(durum.hale, ...haleHemen) : durum.hale,
    akis: akis.length ? [...durum.akis, ...akis.map((metin) => ({ id: sayac++, metin }))].slice(-5) : durum.akis,
    bolunen: bolunen.length ? ekle(durum.bolunen, ...bolunen) : durum.bolunen,
    isilti, serit,
  });
  if (cezaKuyruk.length && !cezaZaman) cezaZaman = setTimeout(cezaGoster, Math.min(900, t - simdi + 200));
}

function UcusTek({ u, kok, renkler, tema, okey }: { u: Ucus; kok: HTMLElement; renkler: string[]; tema: string; okey?: { s: number; r: Renk } }) {
  const ref = useRef<HTMLDivElement | null>(null);
  const [boy, setBoy] = React.useState(0);
  useLayoutEffect(() => {
    const hedefEl = kok.querySelector(u.hedef) as HTMLElement | null;
    const kaynakEl = 'sec' in u.kimden ? (kok.querySelector(u.kimden.sec) as HTMLElement | null) : null;
    const k = kok.getBoundingClientRect();
    const h = hedefEl?.getBoundingClientRect();
    const kr = 'rect' in u.kimden ? u.kimden.rect : kaynakEl ? (() => { const r = kaynakEl.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; })() : null;
    if (!h || !kr || !h.width) { ucusBitti(u); return; }
    const w = u.kucuk ? Math.max(22, Math.min(34, h.width)) : Math.max(18, Math.min(h.width, h.height / 1.38));
    setBoy(w);
    const el = ref.current!;
    const yk = w * 1.38;
    const ax = kr.x + kr.w / 2 - k.left - w / 2, ay = kr.y + kr.h / 2 - k.top - yk / 2;
    const bx = h.left + h.width / 2 - k.left - w / 2, by = h.top + h.height / 2 - k.top - yk / 2;
    const uzak = Math.hypot(bx - ax, by - ay);
    const kavis = Math.min(90, 24 + uzak * 0.22);
    const s0 = u.kucuk ? 1 : Math.max(0.5, Math.min(1.25, (kr.w || w) / w > 2 ? 0.7 : 1));
    const s1 = u.kucuk ? 0.5 : 1;
    const a = el.animate([
      { transform: `translate3d(${ax}px,${ay}px,0) scale(${s0})`, opacity: 0, offset: 0 },
      { transform: `translate3d(${ax}px,${ay}px,0) scale(${s0})`, opacity: 1, offset: 0.04 },
      { transform: `translate3d(${(ax + bx) / 2}px,${(ay + by) / 2 - kavis}px,0) scale(1.18) rotate(${bx > ax ? 6 : -6}deg)`, opacity: 1, offset: 0.55 },
      { transform: `translate3d(${bx}px,${by}px,0) scale(${s1})`, opacity: u.kucuk ? 0.2 : 1, offset: 1 },
    ], { duration: Math.min(620, 380 + uzak * 0.3), delay: u.gecikme, easing: 'cubic-bezier(.35,.05,.3,1)', fill: 'both' });
    let bitti = false;
    const son = () => { if (!bitti) { bitti = true; ucusBitti(u); } };
    a.onfinish = son; a.oncancel = son;
    return () => { a.cancel(); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return <div ref={ref} className="om-ucus"><TasGorsel tas={u.tas ?? { id: -1, s: 1, r: 0 }} kapali={!u.tas} renkler={renkler} tema={tema} okey={okey} boy={boy || 30} /></div>;
}

export function UcusKatmani({ kok, renkler, tema, okey }: { kok: HTMLElement | null; renkler: string[]; tema: string; okey?: { s: number; r: Renk } }) {
  const { ucuslar } = useCan();
  if (!kok || !ucuslar.length) return null;
  return <div className="om-ucus-katman" aria-hidden="true">{ucuslar.map((u) => <UcusTek key={u.id} u={u} kok={kok} renkler={renkler} tema={tema} okey={okey} />)}</div>;
}
