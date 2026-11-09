import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { ArrowDownUp, Lightbulb, Megaphone, Play, SkipForward } from 'lucide-react';
import type { OdaGorunum, UnoGorunum, UnoHamle, UnoKart, UnoRenk } from '../../../services/masa/tipler';
import { masa, useMasa } from '../../../services/masa/istemci';
import { elSirala, oneri as oneriBul } from '../../../services/masa/motor/unoAsistan';
import { benOnde, oyuncuAdi, sesCal, titret, useTercih } from '../ortak';
import El, { type ElKol } from './El';
import Orta, { type YiginKart } from './Orta';
import Rakipler from './Rakipler';
import RenkSecici from './RenkSecici';
import { SahneDeposu, SahneKatmani, useOlayCanlandir, type Baglam } from './canlandir';
import { temaKod } from './temalar';
import { elDiz, yerlesimHesapla, type Nokta } from './yerlesim';
import '../../../styles/masa/uno.css';

const SIRALA_KEY = 'medsoru_masa_uno_sirala';
const siralaOku = () => { try { return localStorage.getItem(SIRALA_KEY) !== '0'; } catch { return true; } };

/** Uno masası: kabın tamamını doldurur, yalnız oyunu çizer (el sonu / maç sonu katmanları kabuktadır). */
export default function UnoMasa({ oda }: { oda: OdaGorunum }) {
  const kokRef = useRef<HTMLDivElement>(null);
  const [boyut, setBoyut] = useState({ W: 0, H: 0 });
  useLayoutEffect(() => {
    const el = kokRef.current;
    if (!el) return;
    const olc = () => { const W = Math.round(el.clientWidth), H = Math.round(el.clientHeight); setBoyut((b) => (b.W === W && b.H === H ? b : { W, H })); };
    olc();
    const ro = new ResizeObserver(olc);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  const tercih = useTercih();
  const tema = temaKod(oda.ayar.tema);
  const oyun = oda.oyun && oda.oyun.tur === 'uno' ? (oda.oyun as UnoGorunum) : null;
  return (
    <div ref={kokRef} className={`um-kok um-t-${tema}${tercih.boyut === '3b' ? ' um-3b' : ''}`}>
      <div className="um-zemin" aria-hidden="true">
        <div className="um-zemin-doku" />
        <div className="um-zemin-sus um-zemin-sus-a" />
        <div className="um-zemin-sus um-zemin-sus-b" />
        <div className="um-zemin-oval" />
      </div>
      {oyun && boyut.W > 0 && boyut.H > 0 && <Masa oda={oda} oyun={oyun} W={boyut.W} H={boyut.H} tema={tema} />}
    </div>
  );
}

interface Balon { tur: 'ipucu' | 'uyari'; metin: string; n: number }

function Masa({ oda, oyun, W, H, tema }: { oda: OdaGorunum; oyun: UnoGorunum; W: number; H: number; tema: string }) {
  const { hata } = useMasa();
  const tercih = useTercih();
  const ben = oda.ben;
  const benOyuncu = oyun.oyuncular.some((p) => p.id === ben);
  const etkin = oda.asama === 'oyun' && !oda.durdu && !oyun.bitti && benOyuncu;
  const siraBende = etkin && oyun.sira === ben;
  const asistan = oda.ayar.asistan !== false;

  /* ---- el dizilişi ---- */
  const [otoSira, setOtoSira] = useState(siralaOku);
  const duzenRef = useRef<number[]>([]);
  const kartlar = useMemo(() => {
    const idler = oyun.elim.map((k) => k.id);
    let d: number[];
    if (otoSira) d = elSirala(oyun.elim);
    else { const eski = duzenRef.current.filter((id) => idler.includes(id)); d = [...eski, ...idler.filter((id) => !eski.includes(id))]; }
    duzenRef.current = d;
    const m = new Map(oyun.elim.map((k) => [k.id, k]));
    return d.map((id) => m.get(id)!).filter(Boolean);
  }, [oyun.elim, otoSira]);

  const rakipSira = useMemo(() => benOnde(oyun.oyuncular, ben).filter((p) => p.id !== ben).map((p) => p.id).join('|'), [oyun.oyuncular, ben]);
  const yer = useMemo(() => yerlesimHesapla(W, H, rakipSira ? rakipSira.split('|') : [], kartlar.length), [W, H, rakipSira, kartlar.length]);
  const poz = useMemo(() => elDiz(kartlar.map((k) => k.id), yer), [kartlar, yer]);
  const oynanabilir = useMemo(() => new Set(oyun.oynanabilir), [oyun.oynanabilir]);

  /* ---- görsel durum (olaylarla uzlaşan) ---- */
  const tazeDagitim = useRef(oda.asama === 'oyun' && oyun.atikSayisi === 1 && !oyun.cektiBuTur && oyun.oyuncular.every((p) => p.kartSayisi === 7));
  const [yigin, setYigin] = useState<YiginKart[]>(() => (tazeDagitim.current ? [] : [{ kart: oyun.ust, vurgu: false }]));
  const [halkaRenk, setHalkaRenk] = useState<UnoRenk>(oyun.aktifRenk);
  const [gizli, setGizli] = useState<Set<number>>(() => new Set());
  const [sarsilan, setSarsilan] = useState<{ id: string; n: number } | null>(null);
  const [yonVurus, setYonVurus] = useState(0);
  const [siraVurus, setSiraVurus] = useState(0);
  const [secili, setSecili] = useState<number | null>(null);
  const [bekleyen, setBekleyen] = useState<number | null>(null);
  const [renkIste, setRenkIste] = useState<number | null>(null);
  const [unoBasili, setUnoBasili] = useState(false);
  const [surukle, setSurukle] = useState(false);
  const [balon, setBalon] = useState<Balon | null>(null);
  const [oneriH, setOneriH] = useState<UnoHamle | null>(null);

  const elRef = useRef<ElKol>(null);
  const oyunRef = useRef(oyun);
  oyunRef.current = oyun;
  const atikBekleyen = useRef(new Set<number>());
  const depo = useMemo(() => new SahneDeposu(), []);

  const yiginEkle = useCallback((kart: UnoKart, vurgu: boolean) => {
    atikBekleyen.current.delete(kart.id);
    setYigin((y) => (y.length && y[y.length - 1].kart.id === kart.id ? y : [...y.filter((q) => q.kart.id !== kart.id).slice(-4), { kart, vurgu }]));
    setHalkaRenk(oyunRef.current.aktifRenk);
  }, []);
  const bRef = useRef<Baglam>(null as unknown as Baglam);
  const sabit = useMemo(() => ({
    kaynak: new Map<number, Nokta & { a?: number; s?: number }>(),
    atikBekle: (id: number) => { atikBekleyen.current.add(id); },
    yiginEkle,
    yiginSifirla: () => setYigin([]),
    yiginKirp: () => setYigin((y) => y.slice(-1)),
    gizle: (idler: number[]) => { if (idler.length) setGizli((g) => new Set([...g, ...idler])); },
    goster: (idler: number[]) => setGizli((g) => { if (!idler.some((i) => g.has(i))) return g; const n = new Set(g); idler.forEach((i) => n.delete(i)); return n; }),
    sars: (id: string) => setSarsilan((s) => ({ id, n: (s?.n ?? 0) + 1 })),
    yonVur: () => setYonVurus((n) => n + 1),
    siraVur: () => setSiraVurus((n) => n + 1),
  }), [yiginEkle]);
  bRef.current = { ...sabit, yer, elPoz: poz, cekKaynak: bRef.current?.cekKaynak ?? null };

  const isle = useOlayCanlandir(bRef, depo);
  // Masa, dağıtım olayıyla aynı anda kurulur (olay kaçar): taze dağıtımı kendimiz canlandırırız
  useEffect(() => {
    if (tazeDagitim.current) { tazeDagitim.current = false; isle([{ t: 'dagit' }], oda); }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Olaysız değişimde (yeniden bağlanma vb.) atık ve renk doğrudan görünüme uzlaşır
  useEffect(() => {
    const ust = oyun.ust;
    if (!atikBekleyen.current.has(ust.id)) { yiginEkle(ust, false); return; }
    const t = window.setTimeout(() => yiginEkle(ust, false), 2600);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [oyun.ust.id]);
  useEffect(() => {
    if (!atikBekleyen.current.size) { setHalkaRenk(oyun.aktifRenk); return; }
    const t = window.setTimeout(() => setHalkaRenk(oyun.aktifRenk), 1200);
    return () => clearTimeout(t);
  }, [oyun.aktifRenk]);
  // Elde olmayan gizli kimlikleri temizle
  useEffect(() => {
    setGizli((g) => { if (!g.size) return g; const n = new Set([...g].filter((id) => oyun.elim.some((k) => k.id === id))); return n.size === g.size ? g : n; });
  }, [oyun.elim]);

  /* ---- bildirim ---- */
  const balonNo = useRef(0);
  const bildir = useCallback((metin: string, tur: Balon['tur'] = 'uyari') => setBalon({ tur, metin, n: ++balonNo.current }), []);
  useEffect(() => {
    if (!balon) return;
    const t = window.setTimeout(() => setBalon((b) => (b && b.n === balon.n ? null : b)), balon.tur === 'ipucu' ? 7000 : 3200);
    return () => clearTimeout(t);
  }, [balon]);

  /* ---- sunucuyla uzlaşma ---- */
  const bekleyenRef = useRef<number | null>(null);
  bekleyenRef.current = bekleyen;
  const geriAl = useCallback((id: number) => { elRef.current?.geriAl(id); sabit.kaynak.delete(id); }, [sabit]);
  // Sunucu hamleyi reddetti: bekleyen kart yaylanarak ele döner (bildirimi kabuk gösterir)
  const sonHata = useRef(hata?.at ?? 0);
  useEffect(() => {
    if (!hata || hata.at === sonHata.current) return;
    sonHata.current = hata.at;
    if (bekleyenRef.current !== null) { geriAl(bekleyenRef.current); setBekleyen(null); }
    titret(30);
  }, [hata, geriAl]);
  useEffect(() => {
    if (bekleyen === null) return;
    if (!oyun.elim.some((k) => k.id === bekleyen)) { setBekleyen(null); return; }
    const t = window.setTimeout(() => { geriAl(bekleyen); setBekleyen(null); }, 4000);
    return () => clearTimeout(t);
  }, [bekleyen, oyun.elim, geriAl]);
  useEffect(() => {
    if (secili !== null && !oyun.elim.some((k) => k.id === secili)) setSecili(null);
  }, [secili, oyun.elim]);
  // Oyun durdu / el bitti: açık seçim kapanır
  const renkIsteRef = useRef<number | null>(null);
  renkIsteRef.current = renkIste;
  const renkVazgec = useCallback(() => { const id = renkIsteRef.current; if (id !== null) { geriAl(id); setRenkIste(null); } }, [geriAl]);
  useEffect(() => { if (!siraBende) { renkVazgec(); setUnoBasili(false); } }, [siraBende, renkVazgec]);
  useEffect(() => { setOneriH(null); }, [oyun.sira, oyun.elim.length, oyun.cektiBuTur, oyun.yakalanabilir.length]);
  useEffect(() => {
    if (!unoBasili) return;
    const t = window.setTimeout(() => setUnoBasili(false), 8000);
    return () => clearTimeout(t);
  }, [unoBasili]);

  /* ---- hamleler ---- */
  const gonder = (id: number, renk?: UnoRenk) => {
    const h: UnoHamle = { t: 'oyna', kart: id };
    if (renk) h.renk = renk;
    if (oyun.elim.length === 2 && unoBasili) h.uno = true;
    masa.hamle(h);
    setBekleyen(id);
    setSecili(null);
    setUnoBasili(false);
    setBalon(null);
  };
  const oyna = (id: number, nokta: (Nokta & { a: number; s: number }) | null): 'bekle' | 'geri' => {
    if (!etkin) return 'geri';
    const kart = oyun.elim.find((k) => k.id === id);
    if (!kart) return 'geri';
    if (!oynanabilir.has(id)) {
      bildir(oyun.sira !== ben ? `Sıra sende değil: ${oyuncuAdi(oda, oyun.sira)} oynuyor.` : oyun.cektiBuTur ? 'Kart çektin: yalnız çektiğin kartı oynayabilir ya da geçebilirsin.' : 'Bu kart uymuyor: rengi ya da değeri tutmalı.');
      sesCal('hata');
      titret(30);
      return 'geri';
    }
    const p = poz.get(id);
    sabit.kaynak.set(id, nokta ?? { x: p?.x ?? W / 2, y: (p?.y ?? H) - yer.kw * 0.2, a: p?.a ?? 0, s: 1 });
    if (kart.renk === null) { setRenkIste(id); setSecili(null); setBalon(null); return 'bekle'; }
    gonder(id);
    return 'bekle';
  };
  const dokun = (id: number) => {
    if (secili === id) { oyna(id, null); return; }
    setSecili(id);
    sesCal('tas');
  };
  const birak = (id: number, kart: Nokta & { a: number; s: number }, isaretci: Nokta): 'bekle' | 'geri' => {
    const uzak = (p: Nokta) => Math.hypot(p.x - yer.atik.x, p.y - yer.atik.y);
    if (uzak(isaretci) > yer.halka / 2 + 40 && uzak(kart) > yer.halka / 2 + 24) return 'geri';
    return oyna(id, kart);
  };
  const cek = (kaynak?: Nokta) => {
    if (kaynak) bRef.current.cekKaynak = { ...kaynak, t: performance.now() };
    sabit.kaynak.clear();
    masa.hamle({ t: 'cek' });
    sesCal('tas');
    setSecili(null);
  };
  const cekReddet = () => {
    if (!etkin) return;
    bildir(oyun.sira !== ben ? `Sıra sende değil: ${oyuncuAdi(oda, oyun.sira)} oynuyor.` : 'Bu turda zaten çektin: kartı oyna ya da geç.');
    sesCal('hata');
  };
  const ipucu = () => {
    const o = oneriBul(oyun, ben);
    if (!o) { bildir('Şimdilik yapacak bir şey yok: sıranı bekle.', 'ipucu'); return; }
    setOneriH(o.hamle);
    bildir(o.aciklama, 'ipucu');
  };
  const sirala = () => {
    const yeni = !otoSira;
    setOtoSira(yeni);
    try { localStorage.setItem(SIRALA_KEY, yeni ? '1' : '0'); } catch { /* yok */ }
    sesCal('tas');
  };

  /* ---- düğmeler ---- */
  const unoDe = etkin && oyun.yakalanabilir.includes(ben);
  const unoHazir = siraBende && oyun.elim.length === 2 && renkIste === null;
  const cekilenUygun = siraBende && oyun.cekilen !== undefined && oynanabilir.has(oyun.cekilen) ? oyun.cekilen : null;
  const oynaHedef = siraBende ? (secili ?? cekilenUygun) : null;
  const gecGoster = siraBende && oyun.cektiBuTur;
  const benUno = oyun.oyuncular.find((p) => p.id === ben)?.unoDedi;
  const dar = W < 560;
  const oneriKart = oneriH?.t === 'oyna' ? oneriH.kart : null;
  const sagAdet = Number(gecGoster) + Number(oynaHedef !== null) + Number(unoDe || unoHazir);
  // Çok dar ekranda üç düğme yan yana: simgesiz, sıkışık
  const sikisik = !yer.yatay && W < 400 && sagAdet >= 3;
  const elYuk = H - yer.elUst;

  return (
    <div
      className={`um-masa${yer.yatay ? ' um-yatay' : ' um-dikey'}${etkin ? '' : ' um-etkisiz'}${dar ? ' um-dar' : ''}`}
      style={{ ['--um-b' as string]: `${(Math.min(W, H) / 100).toFixed(2)}px` }}
      onPointerDown={(e) => { if (secili !== null && !(e.target as HTMLElement).closest?.('.um-el-kart, .um-dugme')) setSecili(null); }}
    >
      <Orta
        yer={yer} tema={tema} yigin={yigin} deste={oyun.deste} renk={halkaRenk} yon={oyun.yon} yonVurus={yonVurus}
        cekilebilir={siraBende && !oyun.cektiBuTur && renkIste === null} hedef={surukle} oneriCek={oneriH?.t === 'cek'}
        onCek={cek} onReddet={cekReddet}
      />
      <Rakipler oda={oda} oyun={oyun} yer={yer} tema={tema} etkin={etkin} sarsilan={sarsilan} oneriHedef={oneriH?.t === 'yakala' ? oneriH.hedef : null} onYakala={(id) => { masa.hamle({ t: 'yakala', hedef: id }); titret(15); }} />

      {benOyuncu && (
        <>
          <div className={`um-el-isik${siraBende ? ' um-acik' : ''}`} style={{ height: elYuk }} aria-hidden="true">
            {siraVurus > 0 && <div key={siraVurus} className="um-el-nabiz" />}
          </div>
          <El
            ref={elRef} kartlar={kartlar} poz={poz} yer={yer} tema={tema}
            oynanabilir={oynanabilir} fark={asistan && tercih.ipucu !== false && siraBende}
            secili={secili} cekilen={siraBende ? oyun.cekilen ?? null : null} oneri={oneriKart} gizli={gizli} etkin={etkin && renkIste === null}
            onDokun={dokun} onSurukle={setSurukle} onBirak={birak}
          />

          <div className="um-eylem um-eylem-sol" style={yer.yatay ? { left: yer.bosluk, bottom: yer.bosluk, width: yer.yanGen - yer.bosluk } : { left: yer.bosluk, bottom: 5 }}>
            <button type="button" className={`um-dugme${otoSira ? ' um-basili' : ''}`} onClick={sirala} aria-pressed={otoSira} aria-label="Eli otomatik sırala" title="Eli otomatik sırala">
              <ArrowDownUp size={18} aria-hidden="true" /><span className="um-dugme-yazi">Sırala</span>
            </button>
            {asistan && (
              <button type="button" className="um-dugme" onClick={ipucu} disabled={!etkin} aria-label="İpucu al" title="İpucu al">
                <Lightbulb size={18} aria-hidden="true" /><span className="um-dugme-yazi">İpucu</span>
              </button>
            )}
            <span className={`um-durum${siraBende ? ' um-bende' : ''}${dar && !yer.yatay && sagAdet >= 2 ? ' um-durum-gizle' : ''}`} aria-live="polite">
              {oyun.bitti ? 'El bitti' : oda.durdu ? 'Oyun durdu' : siraBende ? 'Sıra sende' : `Sıra: ${oyuncuAdi(oda, oyun.sira)}`}
              {benUno && <b className="um-durum-uno">UNO!</b>}
            </span>
          </div>

          <div className={`um-eylem um-eylem-sag${sikisik ? ' um-sikisik' : ''}`} style={yer.yatay ? { right: yer.bosluk, bottom: yer.bosluk, width: yer.yanGen - yer.bosluk } : { right: yer.bosluk, bottom: 5 }}>
            {gecGoster && (
              <button type="button" className={`um-dugme um-dugme-gec${oneriH?.t === 'pas' ? ' um-oneri' : ''}`} onClick={() => { masa.hamle({ t: 'pas' }); setSecili(null); }} aria-label="Sırayı geç">
                {!sikisik && <SkipForward size={18} aria-hidden="true" />}<span className="um-dugme-yazi um-hep">Geç</span>
              </button>
            )}
            {oynaHedef !== null && (
              <button type="button" className="um-dugme um-dugme-oyna" onClick={() => oyna(oynaHedef, null)} aria-label="Seçili kartı oyna">
                {!sikisik && <Play size={18} aria-hidden="true" />}<span className="um-dugme-yazi um-hep">Oyna</span>
              </button>
            )}
            {(unoDe || unoHazir) && (
              <button
                type="button"
                className={`um-dugme um-dugme-uno${unoDe ? ' um-uno-de' : ''}${unoBasili ? ' um-basili' : ''}${oneriH?.t === 'uno' || (oneriH?.t === 'oyna' && oneriH.uno) ? ' um-oneri' : ''}`}
                onClick={() => { if (unoDe) masa.hamle({ t: 'uno' }); else { setUnoBasili((v) => !v); sesCal('uno'); } titret(20); }}
                aria-pressed={unoDe ? undefined : unoBasili}
                aria-label={unoDe ? 'UNO de (yakalanmadan)' : unoBasili ? 'UNO denecek: kartını oyna' : 'Kartı oynarken UNO de'}
              >
                {!sikisik && <Megaphone size={18} aria-hidden="true" />}<span className="um-dugme-yazi um-hep">{unoDe ? 'UNO de!' : unoBasili ? 'UNO ✓' : 'UNO!'}</span>
              </button>
            )}
          </div>
        </>
      )}

      {balon && (
        <div className="um-balon-yer" style={{ bottom: elYuk + 4 }}>
          <div key={balon.n} className={`um-balon um-balon-${balon.tur}`} role="status">{balon.tur === 'ipucu' && <Lightbulb size={16} aria-hidden="true" />}<span>{balon.metin}</span></div>
        </div>
      )}

      <SahneKatmani depo={depo} tema={tema} />
      {renkIste !== null && <RenkSecici yer={yer} tema={tema} onSec={(r) => { const id = renkIste; setRenkIste(null); gonder(id, r); }} onVazgec={renkVazgec} />}
    </div>
  );
}
