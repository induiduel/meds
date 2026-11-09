import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import { Lightbulb } from 'lucide-react';
import type { OdaGorunum, Olay } from '../../../services/masa/tipler';
import { masa, useMasa } from '../../../services/masa/istemci';
import { pistiOneri, type PistiGorunum, type PistiKart, type PistiOyuncuGorunum } from '../../../services/masa/motor/pisti';
import { azHareket, benOnde, oyuncuAdi, sesCal, titret } from '../ortak';
import { Kart, KartArka } from './Kart';
import '../../../styles/masa/pisti.css';

interface Ucus { key: number; x0: number; y0: number; x1: number; y1: number; kart?: PistiKart; adet?: number }
interface Balon { metin: string; n: number }

/** Pişti masası: kabın tamamını doldurur; el sonu / maç sonu katmanları kabuktadır. */
export default function PistiMasa({ oda }: { oda: OdaGorunum }) {
  const oyun = (oda.oyun as unknown as PistiGorunum | undefined)?.tur === 'pisti' ? (oda.oyun as unknown as PistiGorunum) : null;
  return <div className="pm-kok">{oyun && <Masa oda={oda} oyun={oyun} />}</div>;
}

function Masa({ oda, oyun }: { oda: OdaGorunum; oyun: PistiGorunum }) {
  const { hata } = useMasa();
  const ben = oda.ben;
  const benOyuncu = oyun.oyuncular.some((p) => p.id === ben);
  const etkin = oda.asama === 'oyun' && !oda.durdu && !oyun.bitti && benOyuncu;
  const siraBende = etkin && oyun.sira === ben;
  const asistan = oda.ayar.asistan !== false;

  const kokRef = useRef<HTMLDivElement>(null);
  const yerRef = useRef<HTMLDivElement>(null);
  const koltuk = useRef(new Map<string, HTMLElement>());
  const [secili, setSecili] = useState<number | null>(null);
  const [bekleyen, setBekleyen] = useState<number | null>(null);
  const [ucuslar, setUcuslar] = useState<Ucus[]>([]);
  const [pisti, setPisti] = useState<{ n: number; ad: string; puan: number } | null>(null);
  const [balon, setBalon] = useState<Balon | null>(null);
  const [oneriKart, setOneriKart] = useState<number | null>(null);
  const [surukle, setSurukle] = useState<{ id: number; dx: number; dy: number; ustunde: boolean } | null>(null);
  const no = useRef(1);

  // Oturma: ben altta; 2 kişide rakip üstte, 4 kişide sol–üst–sağ (saat yönü)
  const sira = benOnde(oyun.oyuncular, ben);
  const rakipler = benOyuncu ? sira.slice(1) : sira;
  const benim = benOyuncu ? sira[0] : null;
  const yerler = rakipler.length === 3 ? ['sol', 'ust', 'sag'] : rakipler.length === 1 ? ['ust'] : ['sol', 'ust', 'sag', 'alt'];

  /* ---- olay canlandırma ---- */
  const merkez = (el: Element | null | undefined) => {
    const k = kokRef.current?.getBoundingClientRect();
    const r = el?.getBoundingClientRect();
    return k && r ? { x: r.left - k.left + r.width / 2, y: r.top - k.top + r.height / 2 } : null;
  };
  const ucur = useCallback((u: Omit<Ucus, 'key'>) => setUcuslar((l) => [...l.slice(-6), { ...u, key: no.current++ }]), []);
  useEffect(() => masa.olayDinle((olaylar: Olay[], o: OdaGorunum) => {
    if (o.kod !== oda.kod) return;
    for (const ol of olaylar) {
      const kim = typeof ol.o === 'string' ? ol.o : '';
      if (ol.t === 'oynadi') {
        sesCal('birak');
        if (kim !== ben && !azHareket()) {
          const a = merkez(koltuk.current.get(kim)), b = merkez(yerRef.current);
          if (a && b) ucur({ x0: a.x, y0: a.y, x1: b.x, y1: b.y, kart: ol.kart as PistiKart });
        }
      } else if (ol.t === 'aldi') {
        sesCal('ac');
        if (!azHareket()) {
          const a = merkez(yerRef.current), b = merkez(koltuk.current.get(kim));
          if (a && b) ucur({ x0: a.x, y0: a.y, x1: b.x, y1: b.y, adet: Number(ol.adet) || 1 });
        }
      } else if (ol.t === 'pisti') {
        sesCal('kazan'); titret([30, 40, 60]);
        setPisti({ n: no.current++, ad: kim === ben ? 'Sen' : oyuncuAdi(o, kim), puan: Number(ol.puan) || 10 });
      } else if (ol.t === 'dagit') {
        sesCal('dagit');
      } else if (ol.t === 'sira' && kim === ben) {
        sesCal('sira');
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }), [oda.kod, ben, ucur]);
  useEffect(() => {
    if (!pisti) return;
    const t = window.setTimeout(() => setPisti((p) => (p && p.n === pisti.n ? null : p)), 1600);
    return () => clearTimeout(t);
  }, [pisti]);
  useEffect(() => {
    if (!balon) return;
    const t = window.setTimeout(() => setBalon((b) => (b && b.n === balon.n ? null : b)), 6000);
    return () => clearTimeout(t);
  }, [balon]);

  /* ---- sunucuyla uzlaşma ---- */
  const sonHata = useRef(hata?.at ?? 0);
  useEffect(() => { if (hata && hata.at !== sonHata.current) { sonHata.current = hata.at; setBekleyen(null); titret(30); } }, [hata]);
  useEffect(() => { if (bekleyen !== null && !oyun.elim.some((k) => k.id === bekleyen)) setBekleyen(null); }, [bekleyen, oyun.elim]);
  useEffect(() => { setOneriKart(null); setBalon(null); }, [oyun.sira, oyun.elim.length]);
  useEffect(() => { if (secili !== null && !oyun.elim.some((k) => k.id === secili)) setSecili(null); }, [secili, oyun.elim]);

  const oyna = (id: number) => {
    if (!siraBende || bekleyen !== null) { if (etkin && !siraBende) setBalon({ metin: 'Sıra sende değil.', n: no.current++ }); return; }
    masa.hamle({ t: 'oyna', kart: id } as any);
    setBekleyen(id); setSecili(null); titret(12);
  };
  const ipucu = () => {
    const o = pistiOneri(oyun.elim, oyun.ust, oyun.yerSayisi);
    if (!o) return;
    setOneriKart(o.kart); setBalon({ metin: o.neden, n: no.current++ });
  };

  /* ---- sürükle-bırak (pointer) ---- */
  const basla = useRef<{ id: number; x: number; y: number; tasindi: boolean } | null>(null);
  const yerUstunde = (x: number, y: number) => {
    const r = yerRef.current?.getBoundingClientRect();
    return !!r && x > r.left - 24 && x < r.right + 24 && y > r.top - 24 && y < r.bottom + 24;
  };
  const onDown = (e: React.PointerEvent, id: number) => {
    if (!etkin) return;
    basla.current = { id, x: e.clientX, y: e.clientY, tasindi: false };
    (e.currentTarget as HTMLElement).setPointerCapture?.(e.pointerId);
  };
  const onMove = (e: React.PointerEvent) => {
    const b = basla.current;
    if (!b) return;
    const dx = e.clientX - b.x, dy = e.clientY - b.y;
    if (!b.tasindi && Math.hypot(dx, dy) < 8) return;
    b.tasindi = true;
    setSurukle({ id: b.id, dx, dy, ustunde: yerUstunde(e.clientX, e.clientY) });
  };
  const onUp = (e: React.PointerEvent) => {
    const b = basla.current;
    basla.current = null;
    if (!b) return;
    if (b.tasindi) {
      setSurukle(null);
      if (yerUstunde(e.clientX, e.clientY)) oyna(b.id);
      return;
    }
    // dokun: seç; seçiliye yeniden dokun: oyna
    if (secili === b.id) oyna(b.id); else { setSecili(b.id); sesCal('tas'); }
  };

  const n = oyun.elim.length;
  return (
    <div ref={kokRef} className={`pm-masa pm-n${oyun.oyuncular.length}`}>
      {rakipler.map((p, i) => (
        <Koltuk key={p.id} p={p} ad={oyuncuAdi(oda, p.id)} yer={yerler[i]} sira={oyun.sira === p.id && !oyun.bitti}
          ortak={oyun.esli && benim ? p.takim === benim.takim : false} refAl={(el) => { if (el) koltuk.current.set(p.id, el); else koltuk.current.delete(p.id); }} />
      ))}

      <div className="pm-orta">
        <div className="pm-deste" aria-label={`Destede ${oyun.deste} kart`}>
          {oyun.deste > 0 ? <><KartArka className="pm-deste-k2" /><KartArka /></> : <div className="pk-kart pm-bos" />}
          <span className="pm-rozet">{oyun.deste}</span>
        </div>
        <div ref={yerRef} className={`pm-yer${surukle?.ustunde ? ' is-hedef' : ''}${secili !== null && siraBende ? ' is-hazir' : ''}`}
          onClick={() => { if (secili !== null) oyna(secili); }} aria-label={`Yerde ${oyun.yerSayisi} kart`}>
          {oyun.yerSayisi === 0 && <div className="pk-kart pm-bos"><span>Yer boş</span></div>}
          {Array.from({ length: Math.min(oyun.yerSayisi - (oyun.ust ? 1 : 0), 4) }, (_, i) => (
            <KartArka key={i} className="pm-yer-alt" style={{ transform: `translate(${(i - 1.5) * 3}px, ${-i * 2}px) rotate(${(i % 2 ? 1 : -1) * (4 + i * 2)}deg)` }} />
          ))}
          {oyun.ust && <Kart key={oyun.ust.id} kart={oyun.ust} className="pm-ust" />}
          {oyun.yerSayisi > 0 && <span className="pm-rozet">{oyun.yerSayisi}</span>}
        </div>
      </div>

      {benim && (
        <div className={`pm-ben${oyun.sira === ben && !oyun.bitti ? ' is-sira' : ''}`} ref={(el) => { if (el) koltuk.current.set(ben, el); }}>
          <span className="pm-ad">{siraBende ? 'Sıra sende' : 'Sen'}{oyun.esli ? ` · Takım ${benim.takim}` : ''}</span>
          <span className="pm-sayac">Topladığın {benim.aldigi} kart{benim.pisti ? ` · ${benim.pisti} pişti` : ''}</span>
          {asistan && siraBende && (
            <button type="button" className="pm-ipucu" onClick={ipucu} aria-label="İpucu"><Lightbulb size={16} aria-hidden="true" /><span>İpucu</span></button>
          )}
        </div>
      )}

      <div className="pm-el" style={{ ['--pm-n' as any]: Math.max(n, 1) }} onPointerMove={onMove} onPointerUp={onUp} onPointerCancel={() => { basla.current = null; setSurukle(null); }}>
        {oyun.elim.map((k, i) => {
          const s = surukle?.id === k.id;
          const aci = (i - (n - 1) / 2) * 5;
          return (
            <div key={k.id} className={`pm-el-yuva${secili === k.id ? ' is-secili' : ''}${oneriKart === k.id ? ' is-oneri' : ''}${s ? ' is-surukle' : ''}${bekleyen === k.id ? ' is-bekle' : ''}`}
              style={s ? { transform: `translate(${surukle!.dx}px, ${surukle!.dy}px) scale(1.06)` } : { transform: `rotate(${aci}deg) translateY(${Math.abs(aci) * 0.8}px)` }}
              onPointerDown={(e) => onDown(e, k.id)} role="button" tabIndex={etkin ? 0 : -1}
              onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); oyna(k.id); } }}>
              <Kart kart={k} />
            </div>
          );
        })}
      </div>

      {balon && <div className="pm-balon" role="status">{balon.metin}</div>}
      {pisti && (
        <div key={pisti.n} className="pm-pisti" role="status" aria-live="assertive">
          <b>PİŞTİ!</b><span>{pisti.ad} · +{pisti.puan}</span>
        </div>
      )}
      {ucuslar.map((u) => <UcusOge key={u.key} u={u} bitti={() => setUcuslar((l) => l.filter((x) => x.key !== u.key))} />)}
    </div>
  );
}

function Koltuk({ p, ad, yer, sira, ortak, refAl }: { p: PistiOyuncuGorunum; ad: string; yer: string; sira: boolean; ortak: boolean; refAl: (el: HTMLDivElement | null) => void }) {
  return (
    <div ref={refAl} className={`pm-koltuk pm-k-${yer}${sira ? ' is-sira' : ''}${ortak ? ' is-ortak' : ''}`}>
      <div className="pm-koltuk-el" aria-hidden="true">
        {Array.from({ length: p.kartSayisi }, (_, i) => <KartArka key={i} style={{ transform: `rotate(${(i - (p.kartSayisi - 1) / 2) * 9}deg)` }} />)}
      </div>
      <span className="pm-ad">{ad.replace(/\s*\(bot\)$/i, '')}{/\(bot\)$/i.test(ad) ? ' · bot' : ''}{ortak ? ' · ortağın' : ''}</span>
      <span className="pm-sayac">Topladığı {p.aldigi} kart{p.pisti ? ` · ${p.pisti} pişti` : ''}</span>
    </div>
  );
}

/** Tek seferlik uçuş: Web Animations ile, yeniden çizim yok */
function UcusOge({ u, bitti }: { u: Ucus; bitti: () => void }) {
  const ref = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el || !el.animate) { bitti(); return; }
    const t = (x: number, y: number, s: number, a: number) => `translate(${x}px, ${y}px) translate(-50%, -50%) rotate(${a}deg) scale(${s})`;
    const an = el.animate(
      u.kart
        ? [{ transform: t(u.x0, u.y0, 0.6, -20) }, { transform: t(u.x1, u.y1, 1, 0) }]
        : [{ transform: t(u.x0, u.y0, 1, 0), opacity: 1 }, { transform: t(u.x1, u.y1, 0.45, 12), opacity: 0.2 }],
      { duration: u.kart ? 320 : 520, easing: 'cubic-bezier(.3,.7,.3,1)', fill: 'forwards' },
    );
    an.onfinish = bitti;
    return () => an.cancel();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return (
    <div ref={ref} className="pm-ucus" aria-hidden="true">
      {u.kart ? <Kart kart={u.kart} /> : <><KartArka /><KartArka className="pm-ucus-k2" />{(u.adet ?? 0) > 1 && <span className="pm-rozet">{u.adet}</span>}</>}
    </div>
  );
}
