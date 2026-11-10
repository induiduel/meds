import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { ArrowDownUp, Check, EyeOff, Gavel, Gift, Info, Lightbulb, Megaphone, Play, SkipForward, X } from 'lucide-react';
import type { OdaGorunum, UnoBeyan, UnoGorunum, UnoHamle, UnoKart, UnoRenk } from '../../../services/masa/tipler';
import { unoModTanim } from '../../../services/masa/tipler';
import { masa, useMasa } from '../../../services/masa/istemci';
import { UNO_DEGER_AD, elSirala, hedefGerek, oneri as oneriBul, renkGerek, sayiKartiMi } from '../../../services/masa/motor/unoAsistan';
import { benOnde, oyuncuAdi, sesCal, titret, useTercih } from '../ortak';
import El, { type ElKol } from './El';
import Orta, { type YiginKart } from './Orta';
import Rakipler from './Rakipler';
import RenkSecici from './RenkSecici';
import { BeyanSecici, FlexSecici, HedefSecici, Pencere } from './Secimler';
import { SahneDeposu, SahneKatmani, useOlayCanlandir, type Baglam } from './canlandir';
import { kartBilgi } from './kartRehber';
import { renkAl, temaKod } from './temalar';
import { elDiz, yerlesimHesapla, type Nokta } from './yerlesim';
import '../../../styles/masa/uno.css';
import '../../../styles/masa/uno-mod.css';

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
  const koyu = oyun?.taraf === 'k';
  return (
    <div ref={kokRef} className={`um-kok um-t-${tema}${tercih.boyut === '3b' ? ' um-3b' : ''}${koyu ? ' um-koyu' : ''}${oyun ? ` um-mod-${oyun.mod}` : ''}`}>
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

interface Balon { tur: 'ipucu' | 'uyari' | 'kart'; metin: string; baslik?: string; n: number }
/** Oynanacak kartın seçim taslağı: eksik seçimler sırayla sorulur */
interface Taslak { id: number; flex?: boolean; renk?: UnoRenk; hedef?: string; beyan?: UnoBeyan; adim: 'flex' | 'beyan' | 'renk' | 'hedef' }

function Masa({ oda, oyun, W, H, tema }: { oda: OdaGorunum; oyun: UnoGorunum; W: number; H: number; tema: string }) {
  const { hata } = useMasa();
  const tercih = useTercih();
  const ben = oda.ben;
  const mod = oyun.mod;
  const koyu = oyun.taraf === 'k';
  const palet = renkAl(tema, koyu);
  const benO = oyun.oyuncular.find((p) => p.id === ben);
  const benOyuncu = !!benO;
  const elendim = !!benO?.elendi;
  const etkin = oda.asama === 'oyun' && !oda.durdu && !oyun.bitti && benOyuncu && !elendim;
  const bekle = oyun.bekle;
  const asistan = oda.ayar.asistan !== false;
  const ad = (id: string) => oyuncuAdi(oda, id);

  /* ---- kiplerim ---- */
  const verKip = etkin && !!oyun.ver;
  const koyKip = etkin && bekle?.tur === 'meydan' && bekle.asama === 'koy' && bekle.koymayan.includes(ben);
  const kararBende = !!bekle && (bekle.tur === 'renk' || bekle.tur === 'rulet' ? bekle.kim === ben : bekle.tur === 'itiraz' ? bekle.hedef === ben : bekle.tur === 'yalan' ? bekle.karar === ben : bekle.tur === 'meydan' ? bekle.asama === 'sorgu' && bekle.oynayan === ben : false);
  const siraBende = etkin && oyun.sira === ben && !bekle;
  const ilgiBende = siraBende || verKip || koyKip || (etkin && kararBende);

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
  // Kart verme / kapalı kart koyma: eldeki her kart seçilebilir
  const oynanabilir = useMemo(() => new Set(verKip || koyKip ? oyun.elim.map((k) => k.id) : oyun.oynanabilir), [oyun.oynanabilir, oyun.elim, verKip, koyKip]);

  /* ---- görsel durum (olaylarla uzlaşan) ---- */
  const tazeDagitim = useRef(oda.asama === 'oyun' && oyun.atikSayisi === 1 && !oyun.cektiBuTur && !oyun.yigin && oyun.oyuncular.every((p) => p.kartSayisi === unoModTanim(mod).elKart));
  const [yigin, setYigin] = useState<YiginKart[]>(() => (tazeDagitim.current ? [] : [{ kart: oyun.ust, vurgu: false }]));
  const [halkaRenk, setHalkaRenk] = useState<UnoRenk>(oyun.aktifRenk);
  const [gizli, setGizli] = useState<Set<number>>(() => new Set());
  const [sarsilan, setSarsilan] = useState<{ id: string; n: number } | null>(null);
  const [yonVurus, setYonVurus] = useState(0);
  const [siraVurus, setSiraVurus] = useState(0);
  const [flipVurus, setFlipVurus] = useState(0);
  const [secili, setSecili] = useState<number | null>(null);
  const [bekleyen, setBekleyen] = useState<number | null>(null);
  const [taslak, setTaslak] = useState<Taslak | null>(null);
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
    setYigin((y) => {
      const son = y[y.length - 1];
      // Aynı kart yeniden gelirse (kapalı kart açıldı) yüzü yenilenir
      if (son && son.kart.id === kart.id) return son.kart.kp === kart.kp && son.kart.deger === kart.deger && son.kart.renk === kart.renk ? y : [...y.slice(0, -1), { kart, vurgu }];
      return [...y.filter((q) => q.kart.id !== kart.id).slice(-4), { kart, vurgu }];
    });
    setHalkaRenk(oyunRef.current.aktifRenk);
  }, []);
  const bRef = useRef<Baglam>(null as unknown as Baglam);
  const sabit = useMemo(() => ({
    kaynak: new Map<number, Nokta & { a?: number; s?: number }>(),
    atikBekle: (id: number) => { atikBekleyen.current.add(id); },
    yiginEkle,
    yiginSifirla: () => setYigin([]),
    yiginKirp: () => setYigin((y) => y.slice(-1)),
    yiginCikar: (id: number) => { atikBekleyen.current.delete(id); setYigin((y) => y.filter((q) => q.kart.id !== id)); },
    flipVur: () => setFlipVurus((n) => n + 1),
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
  const ustAnahtar = `${oyun.ust.id}|${oyun.ust.deger}|${oyun.ust.renk}|${oyun.ust.kp ?? 0}`;
  useEffect(() => {
    const ust = oyun.ust;
    if (!atikBekleyen.current.has(ust.id)) { yiginEkle(ust, false); return; }
    const t = window.setTimeout(() => yiginEkle(ust, false), 2600);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ustAnahtar]);
  useEffect(() => {
    if (!atikBekleyen.current.size) { setHalkaRenk(oyun.aktifRenk); return; }
    const t = window.setTimeout(() => setHalkaRenk(oyun.aktifRenk), 1200);
    return () => clearTimeout(t);
  }, [oyun.aktifRenk]);
  // Elde olmayan gizli kimlikleri temizle; gizli kalan kart takılmasın (olay kaçarsa)
  useEffect(() => {
    setGizli((g) => { if (!g.size) return g; const n = new Set([...g].filter((id) => oyun.elim.some((k) => k.id === id))); return n.size === g.size ? g : n; });
    const t = window.setTimeout(() => setGizli((g) => (g.size ? new Set() : g)), 3200);
    return () => clearTimeout(t);
  }, [oyun.elim]);

  /* ---- bildirim ---- */
  const balonNo = useRef(0);
  const bildir = useCallback((metin: string, tur: Balon['tur'] = 'uyari', baslik?: string) => setBalon({ tur, metin, baslik, n: ++balonNo.current }), []);
  useEffect(() => {
    if (!balon) return;
    const t = window.setTimeout(() => setBalon((b) => (b && b.n === balon.n ? null : b)), balon.tur === 'uyari' ? 3200 : 7000);
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
  // Oyun durdu / sıra geçti / el bitti: açık seçim kapanır
  const taslakRef = useRef<Taslak | null>(null);
  taslakRef.current = taslak;
  const taslakVazgec = useCallback(() => { const t = taslakRef.current; if (t) { geriAl(t.id); setTaslak(null); } }, [geriAl]);
  useEffect(() => { if (!siraBende) { taslakVazgec(); setUnoBasili(false); } }, [siraBende, taslakVazgec]);
  useEffect(() => { setOneriH(null); }, [oyun.sira, oyun.elim.length, oyun.cektiBuTur, oyun.yakalanabilir.length, bekle?.tur, oyun.ver?.adet]);
  useEffect(() => {
    if (!unoBasili) return;
    const t = window.setTimeout(() => setUnoBasili(false), 8000);
    return () => clearTimeout(t);
  }, [unoBasili]);

  /* ---- hamleler ---- */
  const rakipler = useMemo(() => oyun.oyuncular.filter((p) => p.id !== ben && !p.elendi && !p.cikti && (benO?.takim === undefined || p.takim !== benO.takim)).map((p) => p.id), [oyun.oyuncular, ben, benO?.takim]);
  const gonder = (t: Taslak) => {
    const h: Extract<UnoHamle, { t: 'oyna' }> = { t: 'oyna', kart: t.id };
    if (t.renk) h.renk = t.renk;
    if (t.hedef) h.hedef = t.hedef;
    if (t.flex) h.flex = true;
    if (t.beyan) { h.kapali = true; h.beyan = t.beyan; }
    if (oyun.elim.length === 2 && unoBasili) h.uno = true;
    masa.hamle(h);
    setBekleyen(t.id);
    setTaslak(null);
    setSecili(null);
    setUnoBasili(false);
    setBalon(null);
  };
  /** Taslağın eksik seçimini bul; hepsi tamamsa gönder */
  const ilerlet = (t: Taslak) => {
    const kart = oyun.elim.find((k) => k.id === t.id);
    if (!kart) { setTaslak(null); return; }
    const kapali = mod === 'yalanci' && !!kart.yl;
    if (kapali && !t.beyan) { setTaslak({ ...t, adim: 'beyan' }); return; }
    if (t.flex === undefined && !kapali) {
      if (oyun.yalnizFlex?.includes(kart.id)) t = { ...t, flex: true };
      else if (oyun.flex?.includes(kart.id) && !sayiKartiMi(kart)) { setTaslak({ ...t, adim: 'flex' }); return; }
      else t = { ...t, flex: false };
    }
    if (!kapali && renkGerek(mod, kart) && !t.renk) { setTaslak({ ...t, adim: 'renk' }); return; }
    const deger = kapali ? t.beyan!.deger : kart.deger;
    if (hedefGerek(mod, deger, !!t.flex) && !t.hedef) {
      if (rakipler.length === 1) t = { ...t, hedef: rakipler[0] };
      else if (rakipler.length > 1) { setTaslak({ ...t, adim: 'hedef' }); return; }
    }
    gonder(t);
  };
  const oyna = (id: number, nokta: (Nokta & { a: number; s: number }) | null): 'bekle' | 'geri' => {
    if (!etkin) return 'geri';
    const kart = oyun.elim.find((k) => k.id === id);
    if (!kart) return 'geri';
    const p = poz.get(id);
    const kaynak = nokta ?? { x: p?.x ?? W / 2, y: (p?.y ?? H) - yer.kw * 0.2, a: p?.a ?? 0, s: 1 };
    if (verKip || koyKip) {
      sabit.kaynak.set(id, kaynak);
      masa.hamle(verKip ? { t: 'ver', kart: id } : { t: 'koy', kart: id });
      setBekleyen(id); setSecili(null); setBalon(null);
      sesCal('birak');
      return 'bekle';
    }
    if (!oynanabilir.has(id)) {
      bildir(bekle || oyun.ver ? 'Önce bekleyen karar tamamlanmalı.'
        : oyun.sira !== ben ? `Sıra sende değil: ${ad(oyun.sira)} oynuyor.`
          : oyun.cektiBuTur ? 'Kart çektin: yalnız çektiğin kartı oynayabilir ya da geçebilirsin.'
            : oyun.yigin ? (oyun.firlatici ? 'Sana vuruş geldi: yalnız bir Vur kartı ekleyebilir ya da fırlatıcıya basabilirsin.' : 'Biriken cezaya yalnız uygun bir çekme kartıyla karşılık verebilirsin; yoksa çek.')
              : oyun.takimOyun ? 'Ortağın Takım Oyunu oynadı: uyan bir kartını oyna.'
                : kart.fx && benO?.guc === false ? 'Bu kart uymuyor; flex yüzü için güç kartın yeşil olmalı.'
                  : 'Bu kart uymuyor: rengi ya da değeri tutmalı.');
      sesCal('hata');
      titret(30);
      return 'geri';
    }
    sabit.kaynak.set(id, kaynak);
    setSecili(null); setBalon(null);
    ilerlet({ id, adim: 'renk' });
    return 'bekle';
  };
  const kartTanit = (kart: UnoKart) => {
    if (!asistan || tercih.ipucu === false || (sayiKartiMi(kart) && !kart.ps && !kart.cv && !kart.yl && !kart.fx && !((kart.deger === '7' || kart.deger === '0') && ['yediSifir', 'noMercy', 'yalanci'].includes(mod)))) return;
    const b = kartBilgi(mod, kart, !!oyun.yalnizFlex?.includes(kart.id));
    bildir(`${b.etki} · ${b.puan} puan`, 'kart', b.ad);
  };
  const dokun = (id: number) => {
    if (secili === id) { oyna(id, null); return; }
    setSecili(id);
    sesCal('tas');
    const kart = oyun.elim.find((k) => k.id === id);
    if (kart && !verKip && !koyKip) kartTanit(kart);
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
    bildir(bekle || oyun.ver ? 'Önce bekleyen karar tamamlanmalı.'
      : oyun.sira !== ben ? `Sıra sende değil: ${ad(oyun.sira)} oynuyor.`
        : oyun.takimOyun ? 'Ortağın Takım Oyunu oynadı: uyan bir kartını oynamalısın.'
          : mod === 'noMercy' && !oyun.cektiBuTur ? 'No Mercy: oynanabilir kartın varken çekemezsin.'
            : 'Bu turda zaten çektin: kartı oyna ya da geç.');
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
  const ortakId = benO?.takim !== undefined ? oyun.oyuncular.find((p) => p.id !== ben && p.takim === benO.takim)?.id : undefined;
  const ortakUno = etkin && !!ortakId && oyun.yakalanabilir.includes(ortakId);
  const unoDe = etkin && (oyun.yakalanabilir.includes(ben) || ortakUno);
  const unoHazir = siraBende && oyun.elim.length === 2 && taslak === null;
  const cekilenUygun = siraBende && oyun.cekilen !== undefined && oynanabilir.has(oyun.cekilen) ? oyun.cekilen : null;
  const oynaHedef = siraBende ? (secili ?? cekilenUygun) : (verKip || koyKip) ? secili : null;
  const gecGoster = siraBende && oyun.cektiBuTur && !oyun.zorunlu;
  const dar = W < 560;
  const oneriKart = oneriH && 'kart' in oneriH ? oneriH.kart : null;
  const sagAdet = Number(gecGoster) + Number(oynaHedef !== null) + Number(unoDe || unoHazir);
  // Çok dar ekranda üç düğme yan yana: simgesiz, sıkışık
  const sikisik = !yer.yatay && W < 400 && sagAdet >= 3;
  const elYuk = H - yer.elUst;
  const cekilebilir = siraBende && !!oyun.cekOlur && taslak === null;
  const taslakKart = taslak ? oyun.elim.find((k) => k.id === taslak.id) : undefined;
  const renkAd = (r: UnoRenk) => palet[r].ad;

  /* ---- görev bandı: şu an benden / masadan ne bekleniyor ---- */
  let gorev: { metin: React.ReactNode; vurgu?: boolean } | null = null;
  if (!oyun.bitti && !oda.durdu && benOyuncu) {
    if (elendim) gorev = { metin: <>25 karta ulaştın ve <b>elendin</b>. El bitene dek izliyorsun.</> };
    else if (verKip && oyun.ver) {
      gorev = { vurgu: true, metin: oyun.ver.neden === 'hediye'
        ? <><Gift size={16} aria-hidden="true" /> Hediye: <b>{ad(oyun.ver.kime)}</b> oyuncusuna <b>{oyun.ver.adet} kart</b> ver. Karta dokun, sonra Ver.</>
        : oyun.ver.neden === 'yari'
          ? <>Ortağın <b>{ad(oyun.ver.kime)}</b> elini bitirdi: ona <b>{oyun.ver.adet} kart</b> ver (kartlarının yarısı).</>
          : <>Ortağın <b>{ad(oyun.ver.kime)}</b> oyuncusuna <b>1 kart</b> ver{oyun.ver.neden === 'takim' ? ' (el başı paslaşması)' : ' (paslaşma simgesi)'}.</> };
    } else if (bekle?.tur === 'ver') gorev = { metin: <>Kart verilmesi bekleniyor: {bekle.kalan.map((x) => ad(x.kim)).join(', ')}</> };
    else if (koyKip && bekle?.tur === 'meydan') gorev = { vurgu: true, metin: <><EyeOff size={16} aria-hidden="true" /> Meydan okuma: <b>{renkAd(bekle.renk)}</b> bir kartını kapalı koy. Yoksa başka kart koyup blöf yap.</> };
    else if (bekle?.tur === 'meydan') gorev = { metin: bekle.asama === 'koy' ? <>Kapalı kartlar bekleniyor: {bekle.koymayan.map(ad).join(', ')}</> : bekle.oynayan === ben ? null : <>{ad(bekle.oynayan)} kimi sorgulayacağına karar veriyor…</> };
    else if (bekle?.tur === 'yalan' && bekle.oynayan === ben) gorev = { metin: <>Kapalı kartın için <b>{ad(bekle.karar)}</b> karar veriyor: inanacak mı, “Yalan!” mı diyecek?</> };
    else if (bekle?.tur === 'rulet' && bekle.kim !== ben) gorev = { metin: <>Renk Ruleti: {ad(bekle.kim)} renk seçiyor.</> };
    else if (bekle?.tur === 'itiraz' && bekle.hedef !== ben) gorev = { metin: <>{ad(bekle.hedef)} kabul mü edecek, itiraz mı? Karar bekleniyor.</> };
    else if (siraBende && oyun.takimOyun) gorev = { vurgu: true, metin: <>Ortağın <b>Takım Oyunu</b> oynadı: sıra sana atladı, uyan bir kartını oyna.</> };
    else if (siraBende && oyun.zorunlu) gorev = { vurgu: true, metin: <>No Mercy: çektiğin uyan kartı <b>oynamak zorundasın</b>.</> };
    if (gorev && gorev.metin === null) gorev = null;
  }
  const yalanDiyebilir = etkin && bekle?.tur === 'yalan' && bekle.oynayan !== ben && bekle.karar !== ben;
  const beyanAd = (b: UnoBeyan) => `${b.deger === '+4' ? '' : renkAd(b.renk) + ' '}${UNO_DEGER_AD[b.deger]}${b.deger === '+4' ? ` (renk: ${renkAd(b.renk)})` : ''}`;

  return (
    <div
      className={`um-masa${yer.yatay ? ' um-yatay' : ' um-dikey'}${etkin ? '' : ' um-etkisiz'}${dar ? ' um-dar' : ''}`}
      style={{ ['--um-b' as string]: `${(Math.min(W, H) / 100).toFixed(2)}px` }}
      onPointerDown={(e) => { if (secili !== null && !(e.target as HTMLElement).closest?.('.um-el-kart, .um-dugme')) setSecili(null); }}
    >
      {flipVurus > 0 && <div key={flipVurus} className="um-flip-dalga" aria-hidden="true" />}
      <Orta
        yer={yer} tema={tema} yigin={yigin} deste={oyun.deste} renk={halkaRenk} yon={oyun.yon} yonVurus={yonVurus}
        cekilebilir={cekilebilir} hedef={surukle} oneriCek={oneriH?.t === 'cek'}
        onCek={cek} onReddet={cekReddet}
        koyu={koyu} renksiz={oyun.renksiz} firlatici={oyun.firlatici} desteUst={oyun.desteUst}
      />
      <Rakipler oda={oda} oyun={oyun} yer={yer} tema={tema} etkin={etkin} sarsilan={sarsilan} oneriHedef={oneriH?.t === 'yakala' ? oneriH.hedef : null} onYakala={(id) => { masa.hamle({ t: 'yakala', hedef: id }); titret(15); }} />

      {benOyuncu && (
        <>
          <div className={`um-el-isik${ilgiBende ? ' um-acik' : ''}`} style={{ height: elYuk }} aria-hidden="true">
            {siraVurus > 0 && <div key={siraVurus} className="um-el-nabiz" />}
          </div>
          <El
            ref={elRef} kartlar={kartlar} poz={poz} yer={yer} tema={tema}
            oynanabilir={oynanabilir} fark={asistan && tercih.ipucu !== false && (siraBende || verKip || koyKip)}
            secili={secili} cekilen={siraBende ? oyun.cekilen ?? null : null} oneri={oneriKart} gizli={gizli} etkin={etkin && taslak === null}
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
            <span className={`um-durum${ilgiBende ? ' um-bende' : ''}${dar && !yer.yatay && sagAdet >= 2 ? ' um-durum-gizle' : ''}`} aria-live="polite">
              {oyun.bitti ? 'El bitti' : oda.durdu ? 'Oyun durdu' : elendim ? 'Elendin' : ilgiBende ? 'Sıra sende' : `Sıra: ${ad(oyun.sira)}`}
              {benO?.unoDedi && <b className="um-durum-uno">UNO!</b>}
              {mod === 'noMercy' && !elendim && oyun.elim.length >= 15 && <i className="um-mercy">{oyun.elim.length}/25</i>}
            </span>
            {benO?.guc !== undefined && <i className={`um-guc um-guc-ben${benO.guc ? ' um-acik' : ''}`} title={benO.guc ? 'Güç kartın yeşil: flex yüzünü kullanabilirsin' : 'Güç kartın kırmızı: flex yüzü kapalı'}>{benO.guc ? <Check size={12} strokeWidth={3.5} aria-hidden="true" /> : <X size={12} strokeWidth={3.5} aria-hidden="true" />} Güç</i>}
          </div>

          <div className={`um-eylem um-eylem-sag${sikisik ? ' um-sikisik' : ''}`} style={yer.yatay ? { right: yer.bosluk, bottom: yer.bosluk, width: yer.yanGen - yer.bosluk } : { right: yer.bosluk, bottom: 5 }}>
            {gecGoster && (
              <button type="button" className={`um-dugme um-dugme-gec${oneriH?.t === 'pas' ? ' um-oneri' : ''}`} onClick={() => { masa.hamle({ t: 'pas' }); setSecili(null); }} aria-label="Sırayı geç">
                {!sikisik && <SkipForward size={18} aria-hidden="true" />}<span className="um-dugme-yazi um-hep">Geç</span>
              </button>
            )}
            {oynaHedef !== null && (
              <button type="button" className="um-dugme um-dugme-oyna" onClick={() => oyna(oynaHedef, null)} aria-label={verKip ? 'Seçili kartı ver' : koyKip ? 'Seçili kartı kapalı koy' : 'Seçili kartı oyna'}>
                {!sikisik && (verKip ? <Gift size={18} aria-hidden="true" /> : koyKip ? <EyeOff size={18} aria-hidden="true" /> : <Play size={18} aria-hidden="true" />)}<span className="um-dugme-yazi um-hep">{verKip ? 'Ver' : koyKip ? 'Koy' : 'Oyna'}</span>
              </button>
            )}
            {(unoDe || unoHazir) && (
              <button
                type="button"
                className={`um-dugme um-dugme-uno${unoDe ? ' um-uno-de' : ''}${unoBasili ? ' um-basili' : ''}${oneriH?.t === 'uno' || (oneriH?.t === 'oyna' && oneriH.uno) ? ' um-oneri' : ''}`}
                onClick={() => { if (unoDe) masa.hamle({ t: 'uno' }); else { setUnoBasili((v) => !v); sesCal('uno'); } titret(20); }}
                aria-pressed={unoDe ? undefined : unoBasili}
                aria-label={unoDe ? (oyun.yakalanabilir.includes(ben) ? 'UNO de (yakalanmadan)' : 'Ortağın için UNO de') : unoBasili ? 'UNO denecek: kartını oyna' : 'Kartı oynarken UNO de'}
              >
                {!sikisik && <Megaphone size={18} aria-hidden="true" />}<span className="um-dugme-yazi um-hep">{unoDe ? (oyun.yakalanabilir.includes(ben) ? 'UNO de!' : 'Ortağa UNO!') : unoBasili ? 'UNO ✓' : 'UNO!'}</span>
              </button>
            )}
          </div>
        </>
      )}

      <div className="um-balon-yer" style={{ bottom: elYuk + 4 }}>
        {balon && (
          <div key={balon.n} className={`um-balon um-balon-${balon.tur}`} role="status">
            {balon.tur === 'ipucu' && <Lightbulb size={16} aria-hidden="true" />}
            {balon.tur === 'kart' && <Info size={16} aria-hidden="true" />}
            <span>{balon.baslik && <b>{balon.baslik}: </b>}{balon.metin}</span>
          </div>
        )}
        {gorev && <div className={`um-gorev${gorev.vurgu ? ' um-vurgu' : ''}`} role="status" aria-live="polite">{gorev.metin}</div>}
      </div>

      {oyun.yigin > 0 && !oyun.bitti && (
        <div className="um-yigin-rozet" role="status" style={{ left: yer.atik.x, top: Math.max(8, yer.atik.y - yer.kw * 1.1) }}>
          {oyun.firlatici ? <>Vuruş <b>×{oyun.yigin}</b>{siraBende ? ' · Vur ekle ya da bas' : ''}</> : <>Biriken <b>+{oyun.yigin}</b>{siraBende ? ' · ekle ya da çek' : ''}</>}
        </div>
      )}
      {yalanDiyebilir && bekle?.tur === 'yalan' && (
        <button type="button" className="um-yalan-dugme" style={{ left: yer.atik.x, top: Math.max(8, yer.atik.y - yer.kw * 1.25) }} onClick={() => { masa.hamle({ t: 'yalan' }); titret(25); }}>
          <Gavel size={16} aria-hidden="true" /> “{beyanAd(bekle.beyan)}” mi? <b>Yalan!</b>
        </button>
      )}

      {etkin && !oda.durdu && bekle?.tur === 'itiraz' && bekle.hedef === ben && (() => {
        const n = bekle.kart === 'joker+2' ? 2 : 4, renkCek = bekle.kart === 'jokerRenk';
        return (
          <Pencere baslik={`${ad(bekle.oynayan)} sana ${UNO_DEGER_AD[bekle.kart]} oynadı`} etiket="Joker çekme kartına itiraz"
            alt={renkCek
              ? <>Kabul edersen <b>{renkAd(oyun.aktifRenk)}</b> bir kart gelene dek çekersin, sıran geçer. İtiraz edersen eli kontrol edilir: elinde önceki renkten kart vardıysa kart kuralsızdır ve <b>o çeker</b>, sen oynarsın; yoksa <b>sen renk gelene dek çeker, 2 kart da fazladan alırsın</b>.</>
              : <>Kabul edersen {n} kart çekersin, sıran geçer. İtiraz edersen eli kontrol edilir: elinde önceki renkten kart vardıysa kart kuralsızdır ve <b>o {n} çeker</b>, sen oynarsın; yoksa <b>sen {n + 2} çekersin</b>.</>}
          >
            <div className="um-pencere-dugmeler">
              <button type="button" className="um-dugme" onClick={() => { masa.hamle({ t: 'kabul' }); titret(15); }}><Check size={18} aria-hidden="true" /> <span className="um-dugme-yazi um-hep">Kabul et</span></button>
              <button type="button" className="um-dugme um-dugme-uno" onClick={() => { masa.hamle({ t: 'itiraz' }); titret(25); }}><Gavel size={18} aria-hidden="true" /> <span className="um-dugme-yazi um-hep">İtiraz et</span></button>
            </div>
          </Pencere>
        );
      })()}
      {etkin && !oda.durdu && bekle?.tur === 'yalan' && bekle.karar === ben && (
        <Pencere baslik={`${ad(bekle.oynayan)} kapalı kart oynadı`} etiket="Kapalı karta inan ya da yalan de"
          alt={<>“<b>{beyanAd(bekle.beyan)}</b>” dedi. İnanırsan kart öyle sayılır ve oyun sürer. “Yalan!” dersen kart açılır: yalansa kartı geri alıp 1 kart çeker ve sırası geçer; doğruysa <b>sen 1 kart çekersin</b>.</>}
        >
          <div className="um-pencere-dugmeler">
            <button type="button" className="um-dugme" onClick={() => { masa.hamle({ t: 'inan' }); titret(15); }}><Check size={18} aria-hidden="true" /> <span className="um-dugme-yazi um-hep">İnan</span></button>
            <button type="button" className="um-dugme um-dugme-uno" onClick={() => { masa.hamle({ t: 'yalan' }); titret(25); }}><Gavel size={18} aria-hidden="true" /> <span className="um-dugme-yazi um-hep">Yalan!</span></button>
          </div>
        </Pencere>
      )}
      {etkin && !oda.durdu && bekle?.tur === 'meydan' && bekle.asama === 'sorgu' && bekle.oynayan === ben && (
        <Pencere baslik="Kimi sorgulayacaksın?" etiket="Meydan okuma sorgusu"
          alt={<>Herkes <b>{renkAd(bekle.renk)}</b> dediği bir kartı kapalı koydu. Sorguladığın oyuncu yalancıysa kartını geri alır ve 1 kart çeker; doğru renk çıkarsa sorgu biter, kalan herkes kartından kurtulur.</>}
        >
          <div className="um-liste">
            {bekle.konan.map((id) => (
              <button key={id} type="button" className="um-liste-oge" onClick={() => { masa.hamle({ t: 'sorgula', hedef: id }); titret(20); }}>
                <span className="um-avatar" aria-hidden="true">{ad(id).trim().charAt(0).toLocaleUpperCase('tr')}</span>
                <span className="um-liste-ad">{ad(id)}</span>
                <span className="um-liste-sayi">Sorgula</span>
              </button>
            ))}
          </div>
          <div className="um-pencere-dugmeler">
            <button type="button" className="um-dugme um-dugme-gec" onClick={() => masa.hamle({ t: 'yeter' })}><SkipForward size={18} aria-hidden="true" /> <span className="um-dugme-yazi um-hep">Yeter, devam et</span></button>
          </div>
        </Pencere>
      )}
      {etkin && !oda.durdu && (bekle?.tur === 'renk' || bekle?.tur === 'rulet') && bekle.kim === ben && (
        <RenkSecici
          yer={yer} tema={tema} koyu={koyu} zorunlu
          baslik={bekle.tur === 'rulet' ? 'Renk Ruleti: bir renk seç' : oyun.renkSec ? 'İlk kart joker: renk seç' : 'Üstte joker açıldı: renk seç'}
          onSec={(r) => masa.hamle({ t: 'renk', renk: r })}
          onVazgec={() => bildir(bekle.tur === 'rulet' ? 'Renk Ruleti: seçtiğin renk gelene dek kart açılır ve hepsini alırsın.' : 'Oyunun sürmesi için bir renk seçmelisin.')}
        />
      )}
      <SahneKatmani depo={depo} tema={tema} />
      {taslak?.adim === 'renk' && taslakKart && (
        <RenkSecici yer={yer} tema={tema} koyu={koyu} baslik={taslakKart.deger === 'pony' ? 'Hangi rengin hepsini atacaksın?' : 'Renk seç'} onSec={(r) => ilerlet({ ...taslak, renk: r })} onVazgec={taslakVazgec} />
      )}
      {taslak?.adim === 'hedef' && taslakKart && (
        <HedefSecici
          oda={oda} oyun={oyun} adaylar={rakipler} onVazgec={taslakVazgec} onSec={(id) => ilerlet({ ...taslak, hedef: id })}
          baslik={kartBilgi(mod, taslak.beyan ? { renk: taslak.beyan.renk, deger: taslak.beyan.deger } : taslakKart, !!taslak.flex).ad + ': kime?'}
          alt={kartBilgi(mod, taslak.beyan ? { renk: taslak.beyan.renk, deger: taslak.beyan.deger } : taslakKart, !!taslak.flex).etki}
        />
      )}
      {taslak?.adim === 'flex' && taslakKart && (
        <FlexSecici kart={taslakKart} tema={tema} duz={kartBilgi(mod, taslakKart, false).etki} flex={kartBilgi(mod, taslakKart, true).etki} onSec={(f) => ilerlet({ ...taslak, flex: f })} onVazgec={taslakVazgec} />
      )}
      {taslak?.adim === 'beyan' && taslakKart && (
        <BeyanSecici kart={taslakKart} oyun={oyun} tema={tema} onSec={(b) => ilerlet({ ...taslak, beyan: b })} onVazgec={taslakVazgec} />
      )}
    </div>
  );
}
