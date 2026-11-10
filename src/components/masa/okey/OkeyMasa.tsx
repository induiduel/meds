/** Okey masası (yedili / takım / 101 / Kastet / Remi / Düz Okey): kompozisyon, seçim, hamle gönderimi, asistan akışları. Durumun tek kaynağı `oda`. */
import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { AlertTriangle, ArrowDownToLine, ArrowDownUp, Check, LayoutGrid, Pencil, RotateCcw, X, ArrowUpFromLine, CopyPlus, CornerDownLeft, Gift, Layers, Lightbulb, LockOpen, PlusSquare, SkipForward, Sparkles, Undo2, Wand2 } from 'lucide-react';
import type { OdaGorunum, OkeyGorunum, OkeyHamle, Per, Tas } from '../../../services/masa/tipler';
import { masa, useMasa } from '../../../services/masa/istemci';
import * as Y from '../../../services/masa/motor/yediliAsistan';
import * as Z from '../../../services/masa/motor/yuzbirAsistan';
import * as A from '../../../services/masa/motor/acikMasa';
import * as D from '../../../services/masa/motor/duzOkey';
import { benOnde, oyuncuAdi, sesCal, titret, useTercih } from '../ortak';
import { canSifirla, olaylariIsle, sarsTas, UcusKatmani, useCan } from './canlandir';
import EylemCubugu, { type Eylem } from './EylemCubugu';
import Istaka from './Istaka';
import PerAlani from './PerAlani';
import Koltuk, { AtikYigini, CEZA_BILGI, CezaRozetleri } from './Rakipler';
import { useSurukle, type Hedef, type Kaynak, type Rect } from './surukle';
import { TasGorsel } from './Tas';
import { diz, gruplar, komsuGrup, tasi, uzlas, yuvaOku, yuvaSirasi, yuvaYaz, type YuvaDurum } from './yuva';
import '../../../styles/masa/okey.css';
import '../../../styles/masa/okey-acik.css';

const BOS_KUME: ReadonlySet<number> = new Set();
type Kip = 'seri' | 'grup' | 'per';

export default function OkeyMasa({ oda }: { oda: OdaGorunum }) {
  const g = oda.oyun && oda.oyun.tur !== 'uno' ? (oda.oyun as OkeyGorunum) : null;
  if (!g) return <div className="om-kok om-kok--klasik" />;
  return <Masa oda={oda} g={g} />;
}

function Masa({ oda, g }: { oda: OdaGorunum; g: OkeyGorunum }) {
  const tercih = useTercih();
  const can = useCan();
  const { hata } = useMasa();
  const kokRef = useRef<HTMLDivElement | null>(null);
  const [kokEl, setKokEl] = useState<HTMLDivElement | null>(null);
  const [boyut, setBoyut] = useState({ w: 0, h: 0 });
  const ben = oda.ben;
  const yuzbir = g.tur === 'yuzbir';
  const turAd = g.tur as string;
  const duz = turAd === 'duz';
  const kastet = turAd === 'kastet', remi = turAd === 'remi';
  /** Kastet / Remi: taş atılmayan, masası ortak açık masa okeyleri */
  const acik = kastet || remi;
  const yedili = !yuzbir && !duz && !acik;
  /** Atık yığınlı, çek-at akışlı oyunlar */
  const atikli = yuzbir || duz;
  const okey = g.okey;
  const benO = g.oyuncular.find((o) => o.id === ben);
  const kilit = oda.asama !== 'oyun' || oda.durdu || g.bitti || !benO;
  const siraBende = !kilit && g.sira === ben;
  const tema = oda.ayar.tema === 'kitty' ? 'kitty' : 'klasik';
  const renkler = oda.ayar.renkler;
  const asistan = oda.ayar.asistan;

  useLayoutEffect(() => {
    const el = kokRef.current!;
    setKokEl(el);
    const olc = () => setBoyut((b) => (b.w === el.clientWidth && b.h === el.clientHeight ? b : { w: el.clientWidth, h: el.clientHeight }));
    olc();
    const ro = new ResizeObserver(olc);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  /* ---------------- düzen ---------------- */
  const duzen = useMemo(() => {
    const W = boyut.w || 1024, H = boyut.h || 700, n = g.elim.length;
    const kisa = H < 520 && W > H * 1.3;
    const genis = W >= 700;
    const kullan = W - 16 - (kisa ? 160 : 0) - 44;
    const hesap = (kat: number) => {
      const enAz = Math.ceil((yuzbir ? 30 : genis ? 20 : 16) / kat);
      // Gruplar arası boşluklar ve satır sonu artığı için pay: dar ıstakada gruplar birbirine yapışmasın (H529)
      const sutun = Math.max(enAz, Math.ceil((n + Math.max(4, Math.ceil(n * 0.35)) + kat) / kat));
      const yuk = (H * (kisa ? 0.41 : kat === 3 ? 0.4 : 0.34) - kat * 10 - 10) / kat / 1.38;
      return { kat, sutun, b: Math.max(18, Math.floor(Math.min((kullan - (sutun - 1) * 2) / sutun, yuk, 62))) };
    };
    let d = hesap(2);
    if (d.b < 31 && !kisa) { const u = hesap(3); if (u.b > d.b) d = u; }
    return { ...d, kisa, genis, yigin: W < 980 && !kisa };
  }, [boyut, g.elim.length, yuzbir]);

  /* ---------------- ıstaka yuvaları ---------------- */
  const anahtar = `${oda.kod}:${g.elNo}`;
  const [depo, setDepo] = useState<{ a: string; y: YuvaDurum | null }>(() => ({ a: anahtar, y: yuvaOku(oda.kod, g.elNo) }));
  const temel = depo.a === anahtar ? depo.y : null;
  const ilkDagitim = useRef(depo.y === null);
  const ipucuYuva = useRef<number | undefined>(undefined);
  const elMap = useMemo(() => new Map(g.elim.map((t) => [t.id, t])), [g.elim]);

  const siraGruplari = useCallback((kip: Kip): number[][] => {
    const deger = (t: Tas) => (okey ? Z.gercek(t, okey) : t);
    const bol = (ids: number[], ince: boolean): number[][] => {
      const out: number[][] = [];
      let onceki: { s: number; r: number } | null | undefined;
      for (const id of ids) {
        const d = deger(elMap.get(id)!);
        const ayni = out.length && d && onceki && (kip === 'grup' ? d.s === onceki.s : d.r === onceki.r && (!ince || d.s === onceki.s + 1));
        if (ayni) out[out.length - 1].push(id); else out.push([id]);
        onceki = d;
      }
      return out;
    };
    let on: number[][] = [], kalan = g.elim;
    if (kip === 'per' && okey) {
      on = Z.enIyiDizilim(g.elim, okey).perler.map((p) => p.map((t) => t.id));
      const kul = new Set(on.flat());
      kalan = g.elim.filter((t) => !kul.has(t.id));
    }
    const ids = okey ? Z.elSirala(kalan, okey, kip === 'grup' ? 'grup' : 'seri') : Y.elSirala(kalan, kip === 'grup' ? 'grup' : 'seri');
    return [...on, ...bol(ids, false)];
  }, [elMap, g.elim, okey, duzen.sutun, duzen.kat]);

  const yuva = useMemo(() => {
    const ids = g.elim.map((t) => t.id);
    const y = uzlas(temel, ids, duzen.sutun, duzen.kat, ipucuYuva.current);
    return temel || !ids.length ? y : diz(y, siraGruplari('seri'));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [temel, g.elim, duzen.sutun, duzen.kat]);
  useEffect(() => {
    ipucuYuva.current = undefined;
    if (yuva !== depo.y || depo.a !== anahtar) { setDepo({ a: anahtar, y: yuva }); yuvaYaz(oda.kod, g.elNo, yuva); }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [yuva, anahtar]);
  /** Istaka dizilişi geçmişi (geri al için; yalnız bu cihazda) */
  const yuvaGecmis = useRef<{ a: string; l: YuvaDurum[] }>({ a: anahtar, l: [] });
  if (yuvaGecmis.current.a !== anahtar) yuvaGecmis.current = { a: anahtar, l: [] };
  const [, setGecmisSay] = useState(0);
  const yuvaKoy = (y: YuvaDurum, kaydet = true) => {
    if (kaydet) { yuvaGecmis.current.l = [...yuvaGecmis.current.l.slice(-29), yuva]; setGecmisSay((n) => n + 1); }
    setDepo({ a: anahtar, y }); yuvaYaz(oda.kod, g.elNo, y);
  };

  /* ---------------- seçim, bildirim, bekleyen hamle ---------------- */
  const [seciliHam, setSecili] = useState<number[]>([]);
  const secili = useMemo(() => seciliHam.filter((id) => elMap.has(id)), [seciliHam, elMap]);
  const seciliKume = useMemo(() => new Set(secili), [secili]);
  const [bildirim, setBildirim] = useState<{ metin: string; tur: 'hata' | 'bilgi'; n: number } | null>(null);
  const bildir = useCallback((metin: string, tur: 'hata' | 'bilgi' = 'hata') => setBildirim({ metin, tur, n: Date.now() }), []);
  useEffect(() => { if (!bildirim) return; const t = setTimeout(() => setBildirim(null), bildirim.tur === 'bilgi' ? 4600 : 3200); return () => clearTimeout(t); }, [bildirim]);
  const [ipucu, setIpucu] = useState<{ taslar: ReadonlySet<number>; per?: number; yeni: boolean; kaynak?: 'deste' | 'atik' } | null>(null);
  const ipucuSira = useRef(0);
  const [onay, setOnay] = useState<{ metin: string; evet: string; calis(): void } | null>(null);
  const [oto, setOto] = useState<null | 'isle' | 'plan'>(null);
  const plan = useRef<OkeyHamle[]>([]);
  const bekleyen = useRef<number[]>([]);
  const rectler = useRef(new Map<number, Rect>());
  const sabit = useRef(new Set<number>());
  const kip = useRef<Kip>('grup');

  const olmadi = useCallback((ids: number[], metin: string) => { bildir(metin); sarsTas(ids); sesCal('hata'); titret(30); }, [bildir]);
  const gonder = useCallback((h: OkeyHamle, ids: number[] = []) => { bekleyen.current = ids; setIpucu(null); masa.hamle(h); }, []);

  /* ---------------- olaylar ---------------- */
  useEffect(() => {
    const birak = masa.olayDinle((olaylar, yeni) => { if (yeni.oyun && yeni.oyun.tur !== 'uno') olaylariIsle(olaylar, yeni, (id) => rectler.current.get(id)); });
    // Masa, dağıtım olayından sonra yüklendiyse (ilk el) dağıtımı yine de canlandır
    if (ilkDagitim.current && oda.asama === 'oyun' && !g.perler.length && !g.tur_.cekti && !g.tur_.hamleYapti) olaylariIsle([{ t: 'dagit' }], oda, () => undefined);
    return () => { birak(); canSifirla(); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const sur = useSurukle({
    kilit,
    idsAl: (src, id) => (src === 'el' ? (seciliKume.has(id) ? yuvaSirasi(yuva, secili) : [id]) : siraBende && !g.tur_.cekti ? [id] : null),
    dokun: (src, id) => {
      if (src === 'el') { sesCal('tas'); setSecili((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id])); }
      else if (src === 'deste') cek('deste');
      else cek('atik');
    },
    uzunBas: (src, id) => { if (src === 'el') setSecili((s) => [...new Set([...s, ...komsuGrup(yuva, id)])]); },
    birak: (hedef, s) => birak(hedef, s.src, s.ids, s.nokta),
  });

  useEffect(() => {
    if (sur.sur?.durum === 'asili') sur.bitir();
    bekleyen.current = [];
    const t = setTimeout(() => sabit.current.clear(), 0);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [oda.surum]);
  useEffect(() => {
    if (!hata || hata.kod !== 'hamle') return;
    setOto(null); plan.current = [];
    olmadi(bekleyen.current, hata.mesaj);
    bekleyen.current = []; sabit.current.clear();
    if (sur.sur?.durum === 'asili') sur.geriDon();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hata?.at]);
  useEffect(() => { if (kilit) { setOto(null); setOnay(null); setSecili([]); } }, [kilit]);

  /* ---------------- kural yardımcıları (motor işlevleri) ---------------- */
  const hak = yuzbir ? !!benO?.acti && g.tur_.cekti : !!benO && (benO.acti || !!benO.takimActi);
  const yerler = useCallback((t: Tas, perId?: number) => {
    const perler = perId === undefined ? g.perler : g.perler.filter((p) => p.id === perId);
    return okey ? Z.islemeYerleri(t, perler, okey) : Y.islemeYerleri(t, perler);
  }, [g.perler, okey]);
  const perMi = useCallback((ids: number[]): boolean => {
    const ts = ids.map((id) => elMap.get(id)).filter((t): t is Tas => !!t);
    if (ts.length !== ids.length) return false;
    if (!okey) return !!Y.perTuru(ts);
    const c = Z.perCoz(ts, okey);
    return !!c && (c.tur === 'cift') === !!benO?.ciftActi;
  }, [elMap, okey, benO?.ciftActi]);

  const acilis = useMemo(() => {
    if (!yuzbir || !okey || !benO || benO.acti) return null;
    const perler: number[][] = [], ciftler: number[][] = [];
    let toplam = 0;
    for (const ids of gruplar(yuva)) {
      if (ids.length < 2) continue;
      const c = Z.perCoz(ids.map((id) => elMap.get(id)!), okey);
      if (!c) continue;
      if (c.tur === 'cift') ciftler.push(ids); else { perler.push(ids); toplam += c.deger; }
    }
    return { perler, ciftler, toplam };
  }, [yuzbir, okey, benO, yuva, elMap]);
  /** Remi ilk açılış: ıstakada boşlukla ayrılmış geçerli perlerin toplamı */
  const remiAcilis = useMemo(() => {
    if (!remi || !benO || benO.acti) return null;
    const perler: number[][] = [];
    let toplam = 0;
    for (const ids of gruplar(yuva)) {
      if (ids.length < 3) continue;
      const c = A.acikPer(ids.map((id) => elMap.get(id)!), null);
      if (c) { perler.push(ids); toplam += c.deger; }
    }
    return { perler, toplam };
  }, [remi, benO, yuva, elMap]);
  /** Düz Okey bitişi: seçili (ya da ıstakada tek başına duran) taş atılır, kalan gruplar doğrulanır */
  const duzBitis = useMemo(() => {
    if (!duz || !okey || g.elim.length !== 15) return null;
    const gr = gruplar(yuva);
    const tekler = gr.filter((x) => x.length === 1).map((x) => x[0]);
    const tas = secili.length === 1 ? secili[0] : tekler.length === 1 ? tekler[0] : undefined;
    if (tas === undefined) return { tas: -1, gruplar: [] as number[][], gecerli: false };
    const kalan = gr.map((x) => x.filter((id) => id !== tas)).filter((x) => x.length);
    return { tas, gruplar: kalan, gecerli: !!D.bitisTuru(kalan.map((x) => x.map((id) => elMap.get(id)!)), okey) };
  }, [duz, okey, g.elim.length, yuva, secili, elMap]);

  const onceki = useMemo(() => { const i = g.oyuncular.findIndex((o) => o.id === ben); return i < 0 ? undefined : g.oyuncular[(i - 1 + g.oyuncular.length) % g.oyuncular.length]; }, [g.oyuncular, ben]);
  const yanTas = onceki && onceki.id !== ben ? onceki.atiklar?.[onceki.atiklar.length - 1] : undefined;
  const cekebilir = siraBende && (acik ? !g.tur_.hamleYapti && g.deste > 0 && !(kastet && g.elim.length >= A.KASTET_EL_TAVAN) : !g.tur_.cekti && (atikli || !g.tur_.hamleYapti));
  const pasVar = acik && siraBende && (g.tur_.hamleYapti || !cekebilir || (kastet && !g.elim.length));
  const zorunlu = yedili && siraBende ? Y.zorunlu(g, ben) : { per: false, islek: false };

  /* ---------------- hamleler ---------------- */
  const siraYok = (ids: number[]) => { olmadi(ids, kilit ? 'Şu an hamle yapılamaz.' : `Sıra sende değil. Sıra: ${oyuncuAdi(oda, g.sira)}`); return false; };
  const cezaOnay = (fiil: 'çekersen' | 'devredersen', calis: () => void) => {
    if (!asistan || (!zorunlu.per && !zorunlu.islek)) return calis();
    const ne = zorunlu.per && zorunlu.islek ? 'Açabileceğin per ve işleyebileceğin taş var' : zorunlu.per ? 'Açabileceğin per var' : 'İşleyebileceğin taş var';
    const adet = zorunlu.per && zorunlu.islek ? '−10' : '−5';
    setOnay({ metin: `${ne}. Yine de ${fiil} ${adet} ceza alır ve 1 ceza taşı çekersin.`, evet: fiil === 'çekersen' ? 'Yine de çek' : 'Yine de devret', calis });
  };
  function cek(kaynak: 'deste' | 'atik', yuvaIpucu?: number) {
    if (!siraBende) return void siraYok([]);
    if (g.tur_.cekti) return olmadi([], 'Bu turda zaten taş çektin.');
    if (kaynak === 'atik' && !yanTas) return olmadi([], 'Yanında alınacak taş yok; desteden çek.');
    if (acik && !cekebilir) return olmadi([], g.tur_.hamleYapti ? 'Bu turda yere taş açtın; taş çekemezsin. Pas ile sırayı geçir.' : !g.deste ? 'Deste bitti; pas geçmelisin.' : `Elinde ${A.KASTET_EL_TAVAN} taş var; daha fazla çekemezsin.`);
    const yap = () => { ipucuYuva.current = yuvaIpucu; gonder(atikli ? { t: 'cek', kaynak } : { t: 'cek' }); };
    if (yedili) cezaOnay('çekersen', yap); else yap();
  }
  const devret = () => { if (!siraBende) return void siraYok([]); cezaOnay('devredersen', () => gonder({ t: 'devret' })); };
  /* Kastet / Remi: her koyuş bir `duzenle` hamlesidir (masanın tamamı + elden taşlar) */
  const masaPerler = useMemo(() => (acik ? g.perler.filter((p) => p.tur !== 'cift') : g.perler), [acik, g.perler]);
  const ciftAlan = useMemo(() => (kastet ? g.perler.filter((p) => p.tur === 'cift') : []), [kastet, g.perler]);
  const masaIds = () => masaPerler.map((p) => p.taslar.map((t) => t.id));
  const acikGonder = (perler: number[][], ids: number[], ciftler?: number[][]): boolean => {
    const h: A.AcikHamle = ciftler?.length ? { t: 'duzenle', perler, ciftler } : { t: 'duzenle', perler };
    gonder(h as unknown as OkeyHamle, ids);
    setSecili([]);
    return true;
  };
  function acikIsle(ids: number[], perId: number): boolean {
    if (remi && !benO?.acti) { olmadi(ids, `Önce elinden en az ${A.REMI_ACILIS} sayı açmalısın; açılıştan önce masaya dokunulmaz.`); return false; }
    const k = masaPerler.findIndex((p) => p.id === perId);
    if (k < 0) { olmadi(ids, 'Çift alanındaki taşlara dokunulmaz.'); return false; }
    if (!A.acikPer([...masaPerler[k].taslar, ...ids.map((id) => elMap.get(id)!)], okey ?? null)) { olmadi(ids, 'Bu taşlar bu pere uymuyor. Peri bölmek ya da taş almak için “Masayı düzenle”yi kullan.'); return false; }
    return acikGonder(masaIds().map((x, i) => (i === k ? [...x, ...ids] : x)), ids);
  }
  /** Seçili el taşları tek başına yeni per (ya da Kastet çifti) olur mu */
  function acikYeniMi(ids: number[]): boolean {
    const ts = ids.map((id) => elMap.get(id)).filter((t): t is Tas => !!t);
    if (!acik || ts.length !== ids.length || ts.length < 2) return false;
    if (kastet && ts.length === 2) return A.ciftMi(ts[0], ts[1]) && masaPerler.length >= A.KASTET_ALAN;
    const c = A.acikPer(ts, okey ?? null);
    return !!c && (!remi || !!benO?.acti || c.deger >= A.REMI_ACILIS) && (!kastet || masaPerler.length < A.KASTET_ALAN);
  }
  function acikAc(ids: number[]): boolean {
    const ts = ids.map((id) => elMap.get(id)).filter((t): t is Tas => !!t);
    if (kastet && ts.length === 2 && A.ciftMi(ts[0], ts[1])) {
      if (masaPerler.length < A.KASTET_ALAN) { olmadi(ids, `Çift ancak ${A.KASTET_ALAN} seri alanı dolunca açılır (şu an ${masaPerler.length}).`); return false; }
      return acikGonder(masaIds(), ids, [ids]);
    }
    const c = A.acikPer(ts, okey ?? null);
    if (!c) { olmadi(ids, 'Bu taşlar per olmuyor: aynı renk ardışık ya da aynı sayı farklı renk, en az 3 taş.'); return false; }
    if (remi && !benO?.acti && c.deger < A.REMI_ACILIS) { olmadi(ids, `İlk açılış en az ${A.REMI_ACILIS} olmalı (bu per ${c.deger}). Perlerini ıstakada boşlukla ayırıp Aç’a bas.`); return false; }
    if (kastet && masaPerler.length >= A.KASTET_ALAN) { olmadi(ids, `${A.KASTET_ALAN} seri alanı dolu: yalnız işleyebilir ya da çift açabilirsin.`); return false; }
    return acikGonder([...masaIds(), ids], ids);
  }

  function isle(ids: number[], perId: number, uc?: 'bas' | 'son' | 'bol' | null): boolean {
    if (!siraBende) return siraYok(ids);
    if (acik) return acikIsle(ids, perId);
    if (duz) { olmadi(ids, 'Düz Okey’de masaya taş işlenmez.'); return false; }
    if (ids.length !== 1) { olmadi(ids, 'Pere taşlar tek tek işlenir.'); return false; }
    const t = elMap.get(ids[0]);
    if (!t) return false;
    if (yuzbir && !g.tur_.cekti) { olmadi(ids, 'Önce taş çekmelisin.'); return false; }
    if (!hak) { olmadi(ids, yuzbir ? 'Taş işlemek için önce açmalısın.' : 'Önce per açmalısın.'); return false; }
    const y: { per: number; uc: 'bas' | 'son' | 'bol' | null }[] = yerler(t, perId);
    const sec = uc ? y.find((x) => x.uc === uc) : y.find((x) => x.uc === 'son') ?? y[0];
    if (!sec) { olmadi(ids, 'Bu taş bu pere uymuyor.'); return false; }
    gonder({ t: 'isle', tas: t.id, per: perId, ...(sec.uc === 'bas' || sec.uc === 'son' ? { uc: sec.uc } : null) }, ids);
    setSecili([]);
    return true;
  }
  function perAc(ids: number[]): boolean {
    if (!siraBende) return siraYok(ids);
    if (acik) return acikAc(ids);
    if (duz) { olmadi(ids, 'Düz Okey’de per açılmaz: elin bitince taşı seçip Bitir’e bas.'); return false; }
    if (yuzbir && !g.tur_.cekti) { olmadi(ids, 'Önce taş çekmelisin.'); return false; }
    if (yuzbir && !benO?.acti) { olmadi(ids, 'Önce açmalısın: perlerini ıstakada boşlukla ayır, toplam 101 olunca Aç\'a bas.'); return false; }
    if (!perMi(ids)) { olmadi(ids, yuzbir && benO?.ciftActi ? 'Çiftle açtın: yalnız özdeş iki taş (çift) açabilirsin.' : 'Bu taşlar per olmuyor: aynı renk ardışık ya da aynı sayı farklı renk, en az 3 taş.'); return false; }
    gonder({ t: 'ac', taslar: ids }, ids);
    setSecili([]);
    return true;
  }
  function at(ids: number[]): boolean {
    if (!siraBende) return siraYok(ids);
    if (ids.length !== 1) { olmadi(ids, 'Atmak için tek taş seç.'); return false; }
    if (!g.tur_.cekti) { olmadi(ids, 'Önce taş çekmelisin.'); return false; }
    if (g.yandanAlinan != null) { olmadi(ids, 'Yandan aldığın taşı kullanmalı ya da geri koymalısın.'); return false; }
    gonder({ t: 'at', tas: ids[0] }, ids);
    setSecili([]);
    return true;
  }
  const duzBitir = () => {
    if (!siraBende) return void siraYok([]);
    if (!g.tur_.cekti) return olmadi([], 'Önce taş çekmelisin.');
    if (!duzBitis || duzBitis.tas < 0) return olmadi([], 'Atacağın son taşı seç (ya da ıstakada tek başına bırak), kalan 14 taşı boşlukla gruplara ayır.');
    if (!duzBitis.gecerli) return olmadi([duzBitis.tas], 'Elin bitmiyor: her grup seri ya da grup (en az 3 taş) olmalı, ya da tam 7 çift.');
    const h: D.DuzHamle = { t: 'bitir', tas: duzBitis.tas, gruplar: duzBitis.gruplar };
    gonder(h as unknown as OkeyHamle, [duzBitis.tas]);
    setSecili([]);
  };
  const benGosterdi = duz && !!benO?.acti;
  const gosterVar = duz && D.gosterebilir(g, ben, benGosterdi);
  const ac101 = (cift: boolean) => {
    if (!acilis) return;
    const perler = cift ? acilis.ciftler : acilis.perler;
    gonder({ t: 'ac101', perler }, perler.flat());
    setSecili([]);
  };

  function birak(hedef: Hedef | null, src: Kaynak, ids: number[], nokta: Rect): 'tamam' | 'bekle' | 'red' {
    if (src !== 'el') {
      if (!hedef || (hedef.tur !== 'yuva' && hedef.tur !== 'istaka')) return 'red';
      cek(src === 'atik' ? 'atik' : 'deste', hedef.tur === 'yuva' ? hedef.i : undefined);
      return 'tamam';
    }
    if (!hedef || hedef.tur === 'istaka') return 'red';
    if (hedef.tur === 'yuva') { yuvaKoy(tasi(yuva, ids, hedef.i!)); sesCal('birak'); setSecili([]); return 'tamam'; }
    const tamam = hedef.tur === 'yeni' ? perAc(ids) : hedef.tur === 'atik' ? at(ids) : isle(ids, hedef.per!, hedef.tur === 'uc' ? hedef.uc : undefined);
    if (!tamam) return 'red';
    // Uçuş bırakılan noktadan başlasın
    ids.forEach((id, k) => { sabit.current.add(id); rectler.current.set(id, { x: nokta.x + (ids.length > 1 ? (k * nokta.w) / ids.length : 0), y: nokta.y, w: ids.length > 1 ? nokta.w / ids.length : nokta.w, h: nokta.h }); });
    return 'bekle';
  }
  const hedefeDokun = (calis: () => void) => { if (!sur.azOnce() && !kilit) calis(); };

  /* ---------------- asistan ---------------- */
  const acikIp = useMemo(() => (acik && siraBende ? A.acikOneri(g, ben) : null), [acik, siraBende, g, ben]);
  const ipuclari = useMemo((): { hamle: OkeyHamle; taslar: number[]; per?: number; aciklama: string }[] => {
    if (!asistan || !siraBende) return [];
    if (yuzbir) return Z.ipuclari(g, ben);
    if (yedili) return Y.ipuclari(g, ben);
    const h = (x: unknown) => x as OkeyHamle;
    if (acik) {
      const out = acikIp ? [{ hamle: h(acikIp.hamle), taslar: acikIp.taslar, aciklama: acikIp.aciklama }] : [];
      if (!g.tur_.hamleYapti && cekebilir) out.push({ hamle: h({ t: 'cek' }), taslar: [], aciklama: 'Taş çek: sıra geçer.' });
      else if (!acikIp) out.push({ hamle: h({ t: 'pas' }), taslar: [], aciklama: kastet && !g.elim.length ? 'Elin boş: Pas’a bas, el biter.' : 'Koyacak taş kalmadı: pas geç.' });
      return out;
    }
    if (!okey) return [];
    if (!g.tur_.cekti) {
      return yanTas && D.yandanAl(g.elim, yanTas, okey)
        ? [{ hamle: h({ t: 'cek', kaynak: 'atik' }), taslar: [yanTas.id], aciklama: 'Yandaki taşı al: elini ilerletir.' }]
        : [{ hamle: h({ t: 'cek', kaynak: 'deste' }), taslar: [], aciklama: 'Desteden taş çek.' }];
    }
    const b = D.bitisBul(g.elim, okey);
    if (b) return [{ hamle: h({ t: 'bitir', ...b }), taslar: [b.tas], aciklama: 'Elin bitiyor: gruplar ıstakaya dizildi, işaretli taş seçili. Bitir’e bas.' }];
    const t = Z.atisSec(g.elim, [], okey, false, false);
    return [{ hamle: h({ t: 'at', tas: t }), taslar: [t], aciklama: 'Önerilen atış: perlerine en az yarayan taş.' }];
  }, [asistan, siraBende, yuzbir, yedili, acik, acikIp, kastet, cekebilir, okey, yanTas, g, ben]);
  const ipucuGoster = () => {
    if (!ipuclari.length) return bildir(siraBende ? (cekebilir ? 'Açılacak per ya da işlenecek taş yok: taş çek.' : 'Yapılacak hamle kalmadı: eli devret.') : 'Sıra sana gelince ipucu verebilirim.', 'bilgi');
    const ip = ipuclari[ipucuSira.current++ % ipuclari.length];
    const h = ip.hamle;
    setIpucu({ taslar: new Set(ip.taslar), per: ip.per, yeni: h.t === 'ac' || h.t === 'ac101', kaynak: h.t === 'cek' ? h.kaynak ?? 'deste' : undefined });
    const hb = h as unknown as { t: string; tas: number; gruplar: number[][] };
    if (hb.t === 'bitir') { yuvaKoy(diz(yuva, [...hb.gruplar, [hb.tas]])); setSecili([hb.tas]); }
    if (h.t === 'ac101') yuvaKoy(diz(yuva, [...h.perler, ...siraGruplari('seri').map((x) => x.filter((id) => !ip.taslar.includes(id))).filter((x) => x.length)]));
    bildir(ip.aciklama.charAt(0).toLocaleUpperCase('tr') + ip.aciklama.slice(1), 'bilgi');
  };
  useEffect(() => { if (!ipucu) return; const t = setTimeout(() => setIpucu(null), 4600); return () => clearTimeout(t); }, [ipucu]);
  useEffect(() => {
    if (!oto) return;
    if (!siraBende) { setOto(null); return; }
    const t = setTimeout(() => {
      const h = oto === 'isle' ? Y.ipuclari(g, ben).find((x) => x.hamle.t === 'isle')?.hamle : plan.current.shift();
      if (!h) { setOto(null); return; }
      const ids = h.t === 'ac' ? h.taslar : h.t === 'isle' ? [h.tas] : [];
      setIpucu({ taslar: new Set(ids), per: h.t === 'isle' ? h.per : undefined, yeni: h.t === 'ac' });
      setTimeout(() => gonder(h, ids), 260);
    }, 420);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [oto, oda.surum, siraBende]);

  // Otomatik sıralama: ele yeni taş girince (çekme, yandan alma) ıstaka son dizme biçimine göre yeniden dizilir.
  // Taş çıkınca (atma, açma) yerler korunur; oyuncunun elle kurduğu boşluklar ancak yeni taşta yenilenir.
  const oncekiEl = useRef<{ a: string; ids: Set<number> } | null>(null);
  useEffect(() => {
    const ids = new Set(g.elim.map((t) => t.id)), o = oncekiEl.current;
    oncekiEl.current = { a: anahtar, ids };
    if (!tercih.otoSira || !o || o.a !== anahtar || kilit) return;
    if (![...ids].some((id) => !o.ids.has(id))) return;
    yuvaKoy(diz(yuva, siraGruplari(kip.current)), false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [g.elim, anahtar]);

  const sirala = () => {
    const sira: Kip[] = yuzbir ? ['per', 'seri', 'grup'] : ['seri', 'grup'];
    kip.current = sira[(sira.indexOf(kip.current) + 1) % sira.length];
    yuvaKoy(diz(yuva, siraGruplari(kip.current)));
    setSecili([]); sesCal('birak');
    bildir(kip.current === 'per' ? 'Perlere göre dizildi' : kip.current === 'seri' ? 'Renge göre dizildi' : 'Sayıya göre dizildi', 'bilgi');
  };

  /* ---------------- masa: diz (görünüm) ve düzenle (hamle) ---------------- */
  const zorlu = !asistan;
  const perSirala = (l: Per[]) => l.slice().sort((a, b) => (a.tur === b.tur ? 0 : a.tur === 'seri' ? -1 : 1)
    || (a.tur === 'seri' ? a.taslar[0].r - b.taslar[0].r || a.taslar[0].s - b.taslar[0].s : a.taslar[0].s - b.taslar[0].s));
  // "Masayı diz" açılınca masa hep dizili görünür (iki modda da); zorlu modda el bitince de dizilir
  const [masaDizili, setMasaDizili] = useState(false);
  const elBitti = g.bitti || oda.asama !== 'oyun';
  const gorunenPerler = useMemo(() => ((masaDizili || (zorlu && elBitti)) ? perSirala(g.perler) : g.perler), [g.perler, zorlu, elBitti, masaDizili]);
  const [duzen2, setDuzen2] = useState<{ gruplar: number[][]; secili: number[] } | null>(null);
  const masaTas = useMemo(() => new Map(masaPerler.flatMap((p) => p.taslar.map((t) => [t.id, t] as const))), [masaPerler]);
  /** Açık masa: taslağa elden konan taşlar (ıstakada gizlenir) */
  const taslakEl = useMemo(() => new Set(duzen2 ? duzen2.gruplar.flat().filter((id) => elMap.has(id)) : []), [duzen2, elMap]);
  useEffect(() => { setDuzen2(null); }, [g.elNo, kilit, siraBende]);
  // Masa sunucuda değiştiyse (başkası işledi / geri alındı) taslak geçersiz kalır
  useEffect(() => { setDuzen2((d) => (d && d.gruplar.flat().filter((id) => masaTas.has(id)).length !== masaTas.size ? null : d)); }, [masaTas]);
  const taslakPerler: Per[] | null = useMemo(() => duzen2 && duzen2.gruplar.filter((x) => x.length).map((ids, i) => {
    const ts = ids.map((id) => masaTas.get(id) ?? elMap.get(id)!).filter(Boolean);
    if (acik) {
      const c = A.acikPer(ts, okey ?? null);
      const cift = !c && kastet && ts.length === 2 && A.ciftMi(ts[0], ts[1]) && ts.every((t) => elMap.has(t.id));
      return { id: 1000 + i, tur: c ? c.tur : cift ? 'cift' : 'seri', taslar: c ? c.taslar : ts, sahip: ben } as Per;
    }
    const pt = Y.perTuru(ts);
    return { id: 1000 + i, tur: pt ?? 'seri', taslar: pt ? Y.perDiz(ts) : ts, sahip: ben };
  }), [duzen2, masaTas, elMap, acik, kastet, okey, ben]);
  const taslakGecersiz = useMemo(() => new Set((taslakPerler || []).filter((p) => (acik ? p.tur !== 'cift' && !A.acikPer(p.taslar, okey ?? null) : !Y.perTuru(p.taslar))).map((p) => p.id)), [taslakPerler, acik, okey]);
  const duzenleBasla = () => {
    if (!siraBende) return void siraYok([]);
    if (acik ? remi && !benO?.acti : !hak) return olmadi([], acik ? `Masaya dokunmak için önce elinden en az ${A.REMI_ACILIS} sayı açmalısın.` : 'Masayı düzenlemek için önce per açmalısın.');
    if (!acik) setSecili([]);
    setDuzen2({ gruplar: perSirala(masaPerler).map((p) => p.taslar.map((t) => t.id)), secili: [] });
    bildir(acik
      ? 'Masadaki ve ıstakandaki taşlara dokunarak seç, sonra bir pere ya da “+ Ayrı per”e dokun. Elinden koyduğun taşa dokununca ıstakana döner; masadaki taşlar ele dönmez, Vazgeç her şeyi geri koyar.'
      : 'Masadaki taşlara dokunarak seç, sonra bir pere ya da “+ Ayrı per”e dokun. Hiçbir taş ele dönmez.', 'bilgi');
  };
  const duzenTasi = (hedef: number | 'yeni') => {
    const elSec = acik ? secili.filter((id) => !taslakEl.has(id)) : [];
    setDuzen2((d) => {
      const tum = d ? [...d.secili, ...elSec] : [];
      if (!d || !tum.length) return d;
      const sec = new Set(tum);
      const kalan = d.gruplar.map((x) => x.filter((id) => !sec.has(id)));
      const gr = hedef === 'yeni' ? [...kalan, tum] : kalan.map((x, i) => (i === hedef ? [...x, ...tum] : x));
      sesCal('birak');
      return { gruplar: gr.filter((x) => x.length), secili: [] };
    });
    if (elSec.length) setSecili([]);
  };
  const duzenOnayla = () => {
    if (!duzen2) return;
    if (taslakGecersiz.size) return olmadi([], 'Kırmızı çerçeveli perler geçersiz: her per aynı renk ardışık ya da aynı sayı farklı renk, en az 3 taş.');
    if (acik) {
      if (!taslakEl.size) return olmadi([], 'Elinden en az bir taş koymalısın: ıstakadan taş seçip bir pere dokun.');
      const l = taslakPerler || [];
      acikGonder(l.filter((p) => p.tur !== 'cift').map((p) => p.taslar.map((t) => t.id)), [...taslakEl], l.filter((p) => p.tur === 'cift').map((p) => p.taslar.map((t) => t.id)));
      setDuzen2(null);
      return;
    }
    gonder({ t: 'duzenle', perler: (taslakPerler || []).map((p) => p.taslar.map((t) => t.id)) });
    setDuzen2(null);
  };
  const geriAlVar = (oda.geriAl ?? 0) > 0 && siraBende;
  const geriAl = () => {
    if (duzen2) return setDuzen2(null);
    if (geriAlVar) { masa.geriAl(); return; }
    const l = yuvaGecmis.current.l;
    if (!l.length) return bildir('Geri alınacak bir şey yok. Taş çekme ve eli devretme geri alınmaz.', 'bilgi');
    const onceki = l[l.length - 1];
    yuvaGecmis.current.l = l.slice(0, -1); setGecmisSay((n) => n + 1);
    yuvaKoy(onceki, false); sesCal('birak');
  };

  /* ---------------- eylem çubuğu ---------------- */
  const ik = { size: 18, 'aria-hidden': true } as const;
  const eylemler: Eylem[] = [];
  if (acik) {
    if (remi && !benO?.acti) eylemler.push({ ad: 'ac', etiket: 'Aç', ikon: <LockOpen {...ik} />, etkin: siraBende && !!remiAcilis && remiAcilis.toplam >= A.REMI_ACILIS, birincil: true, ipucu: `Istakada boşlukla ayırdığın perlerin toplamı en az ${A.REMI_ACILIS}`, calis: () => { if (remiAcilis) acikGonder([...masaIds(), ...remiAcilis.perler], remiAcilis.perler.flat()); } });
    else eylemler.push({ ad: 'ac', etiket: 'Per aç', ikon: <PlusSquare {...ik} />, etkin: siraBende && !duzen2 && secili.length >= 2 && acikYeniMi(secili), birincil: true, calis: () => perAc(secili) });
    eylemler.push(
      { ad: 'cek', etiket: 'Taş çek', ikon: <ArrowDownToLine {...ik} />, etkin: cekebilir && !duzen2, birincil: !g.tur_.hamleYapti, calis: () => cek('deste') },
      { ad: 'pas', etiket: kastet && !g.elim.length ? 'Bitir' : 'Pas', ikon: <SkipForward {...ik} />, etkin: pasVar && !duzen2, birincil: g.tur_.hamleYapti || !cekebilir, calis: () => gonder({ t: 'pas' } as unknown as OkeyHamle) },
      { ad: 'duzenle', etiket: 'Masayı düzenle', ikon: <Pencil {...ik} />, etkin: siraBende && !duzen2 && masaPerler.length > 0 && (!remi || !!benO?.acti), calis: duzenleBasla },
    );
    eylemler.push({ ad: 'sirala', etiket: 'Diz', ikon: <ArrowDownUp {...ik} />, etkin: !kilit && g.elim.length > 1, calis: sirala });
    if (asistan) eylemler.push({ ad: 'plan', etiket: 'En iyi hamle', ikon: <Sparkles {...ik} />, etkin: siraBende && !!acikIp && !duzen2, asistan: true, calis: () => { if (acikIp) acikGonder((acikIp.hamle as { perler: number[][] }).perler, acikIp.taslar, (acikIp.hamle as { ciftler?: number[][] }).ciftler); } });
  } else if (yedili) {
    const isleVar = ipuclari.some((x) => x.hamle.t === 'isle');
    eylemler.push(
      { ad: 'ac', etiket: 'Per aç', ikon: <PlusSquare {...ik} />, etkin: siraBende && secili.length >= 3 && perMi(secili), birincil: true, calis: () => perAc(secili) },
      { ad: 'cek', etiket: 'Taş çek', ikon: <ArrowDownToLine {...ik} />, etkin: cekebilir, birincil: !zorunlu.per && !zorunlu.islek, calis: () => cek('deste') },
      { ad: 'devret', etiket: 'Eli devret', ikon: <SkipForward {...ik} />, etkin: siraBende && (g.tur_.cekti || g.tur_.hamleYapti || zorunlu.per || zorunlu.islek), birincil: !cekebilir && !zorunlu.per && !zorunlu.islek, calis: devret },
    );
    eylemler.push(
      { ad: 'sirala', etiket: 'Sırala', ikon: <ArrowDownUp {...ik} />, etkin: !kilit && g.elim.length > 1, calis: sirala },
      { ad: 'masadiz', etiket: masaDizili ? 'Açılış sırası' : 'Masayı diz', ikon: <LayoutGrid {...ik} />, etkin: g.perler.length > 1, calis: () => setMasaDizili((x) => !x) },
    );
    eylemler.push({ ad: 'duzenle', etiket: 'Masayı düzenle', ikon: <Pencil {...ik} />, etkin: siraBende && hak && g.perler.length > 0 && !duzen2, calis: duzenleBasla });
    if (asistan) eylemler.push(
      { ad: 'oto', etiket: 'Otomatik işle', ikon: <Wand2 {...ik} />, etkin: siraBende && isleVar && !oto, asistan: true, calis: () => setOto('isle') },
      { ad: 'plan', etiket: 'En iyi hamle', ikon: <Sparkles {...ik} />, etkin: siraBende && ipuclari.length > 0 && !oto, asistan: true, calis: () => { plan.current = Y.enIyiPlan(g, ben); if (plan.current.length) setOto('plan'); } },
    );
  } else {
    if (!g.tur_.cekti || !siraBende) eylemler.push(
      { ad: 'cek', etiket: 'Desteden çek', ikon: <ArrowDownToLine {...ik} />, etkin: cekebilir, birincil: true, calis: () => cek('deste') },
      { ad: 'yan', etiket: 'Yandan al', ikon: <CornerDownLeft {...ik} />, etkin: cekebilir && !!yanTas, calis: () => cek('atik') },
    );
    else if (duz) eylemler.push(
      { ad: 'bitir', etiket: 'Bitir', ikon: <Check {...ik} />, etkin: !!duzBitis?.gecerli, birincil: true, ipucu: 'Son taşı seç, kalan 14 taşı ıstakada boşlukla gruplara ayır', calis: duzBitir },
      { ad: 'at', etiket: 'Taş at', ikon: <ArrowUpFromLine {...ik} />, etkin: secili.length === 1, birincil: !duzBitis?.gecerli, calis: () => at(secili) },
    );
    else {
      if (!benO?.acti) eylemler.push(
        { ad: 'ac101', etiket: 'Aç', ikon: <LockOpen {...ik} />, etkin: !!acilis && acilis.toplam >= Z.ACILIS_ESIK, birincil: true, calis: () => ac101(false) },
        { ad: 'cift', etiket: 'Çift aç', ikon: <CopyPlus {...ik} />, etkin: !!acilis && acilis.ciftler.length >= Z.ACILIS_CIFT, birincil: true, calis: () => ac101(true) },
      );
      else eylemler.push({ ad: 'ac', etiket: 'Per aç', ikon: <PlusSquare {...ik} />, etkin: secili.length >= 2 && perMi(secili), birincil: true, calis: () => perAc(secili) });
      eylemler.push({ ad: 'at', etiket: 'Taş at', ikon: <ArrowUpFromLine {...ik} />, etkin: secili.length === 1 && g.yandanAlinan == null, birincil: true, calis: () => at(secili) });
      if (g.yandanAlinan != null) eylemler.push({ ad: 'geri', etiket: 'Geri koy', ikon: <Undo2 {...ik} />, etkin: true, calis: () => gonder({ t: 'geriKoy' }) });
    }
    if (gosterVar) eylemler.push({ ad: 'goster', etiket: 'Gösterge göster', ikon: <Sparkles {...ik} />, etkin: true, ipucu: 'İlk turunda göstergenin aynısını göster: rakiplere −1', calis: () => gonder({ t: 'goster' } as unknown as OkeyHamle) });
    eylemler.push({ ad: 'sirala', etiket: 'Diz', ikon: <ArrowDownUp {...ik} />, etkin: !kilit && g.elim.length > 1, calis: sirala });
  }
  eylemler.push({ ad: 'geriAl', etiket: 'Geri al', ikon: <RotateCcw {...ik} />, etkin: !kilit && (geriAlVar || !!duzen2 || yuvaGecmis.current.l.length > 0), calis: geriAl, ipucu: 'Son per açma / işleme ya da ıstaka hareketini geri al' });
  if (asistan && tercih.ipucu !== false) eylemler.push({ ad: 'ipucu', etiket: 'İpucu', ikon: <Lightbulb {...ik} />, etkin: !kilit, asistan: true, calis: ipucuGoster });

  const durumYazi = kilit ? (oda.durdu ? 'Oyun durdu' : g.bitti || oda.asama !== 'oyun' ? 'El bitti' : 'İzliyorsun')
    : !siraBende ? `Sıra: ${oyuncuAdi(oda, g.sira)}`
    : acik ? (remi && !benO?.acti ? (cekebilir ? `${A.REMI_ACILIS} ile aç ya da taş çek` : 'Açamıyorsan pas geç') : g.tur_.hamleYapti ? (kastet && !g.elim.length ? 'Elin boş: Bitir’e bas' : 'Koymaya devam et ya da pas geç') : cekebilir ? 'Taş koy ya da taş çek' : 'Taş koy ya da pas geç')
    : duz ? (!g.tur_.cekti ? 'Sıra sende: taş çek' : duzBitis?.gecerli ? 'Elin bitiyor: Bitir' : 'Taş at')
    : yuzbir ? (!g.tur_.cekti ? 'Sıra sende: taş çek' : g.yandanAlinan != null ? 'Yandan aldığın taşı kullan' : benO?.acti ? 'İşle, per aç ya da taş at' : 'Aç ya da taş at')
    : zorunlu.per ? 'Açabileceğin per var' : zorunlu.islek ? 'İşlenecek taşın var' : cekebilir ? 'Sıra sende: taş çek' : 'Eli devredebilirsin';

  /* ---------------- sürükleme / seçim hedefleri ---------------- */
  const aktifIds = sur.sur ? (sur.sur.src === 'el' ? sur.sur.ids : []) : secili;
  const uygun = useMemo(() => {
    const s = new Set<string>();
    if (acik) {
      if (!aktifIds.length || !siraBende || (remi && !benO?.acti) || duzen2) return s;
      const ts = aktifIds.map((id) => elMap.get(id)).filter((t): t is Tas => !!t);
      for (const p of masaPerler) if (A.acikPer([...p.taslar, ...ts], okey ?? null)) for (const u of ['bas', 'son', '']) s.add(`${p.id}:${u}`);
      return s;
    }
    if (aktifIds.length === 1 && siraBende && hak) { const t = elMap.get(aktifIds[0]); if (t) for (const y of yerler(t)) s.add(`${y.per}:${y.uc ?? ''}`); }
    return s;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [aktifIds.join(','), siraBende, hak, yerler, elMap, acik, masaPerler, okey, duzen2]);
  const yeniUygun = siraBende && aktifIds.length >= 2 && (acik ? acikYeniMi(aktifIds) : !duz && (!yuzbir || (!!benO?.acti && g.tur_.cekti)) && perMi(aktifIds));
  const atikHedef = atikli && siraBende && g.tur_.cekti && aktifIds.length === 1 && g.yandanAlinan == null;

  /* ---------------- oturma düzeni ---------------- */
  const rakipler = benOnde(g.oyuncular, ben).filter((o) => o.id !== ben);
  const k = rakipler.length;
  const yan = duzen.genis && k >= 2;
  const sag = yan ? rakipler[0] : undefined, sol = yan ? rakipler[k - 1] : undefined;
  const ust = (yan ? rakipler.slice(1, k - 1) : rakipler).slice().reverse();
  const koltuk = (o: typeof rakipler[number], yon: 'ust' | 'sol' | 'sag') => (
    <Koltuk key={o.id} oda={oda} g={g} o={o} yon={yon} sarsil={can.sarsilan.has(o.id)} gizli={can.gizli} alinabilir={cekebilir && atikli && onceki?.id === o.id && !!yanTas} />
  );
  const hayaletTaslar: (Tas | null)[] = sur.sur ? (sur.sur.src === 'el' ? sur.sur.ids.map((id) => elMap.get(id) ?? null).filter(Boolean) : [sur.sur.src === 'atik' ? yanTas ?? null : null]) : [];
  const cezaAd = can.ceza ? (can.ceza.o === ben ? 'Sen' : oyuncuAdi(oda, can.ceza.o)) : '';
  const cezaTur = can.ceza?.ceza.tur === 'per' ? 'per' : can.ceza?.ceza.tur === 'islek' || can.ceza?.ceza.tur === 'islekAtti' ? 'islek' : 'diger';

  return (
    <div
      ref={kokRef}
      className={`om-kok om-kok--${tema} ${tercih.boyut === '3b' ? 'om-3b' : 'om-2b'}${duzen.kisa ? ' om-kok--kisa' : ''}${duzen.genis ? '' : ' om-kok--dar'}${duzen.yigin ? ' om-kok--yigin' : ''}${kilit ? ' om-kok--kilit' : ''}${sur.sur ? ' om-kok--surukle' : ''}`}
      style={{ '--om-persp': `${Math.round(Math.max(1100, boyut.h * 2))}px` } as React.CSSProperties}
      onPointerDown={sur.onPointerDown}
      onContextMenu={(e) => e.preventDefault()}
    >
      <div className="om-ust">{ust.map((o) => koltuk(o, 'ust'))}</div>

      <div className="om-orta">
        {sol && <div className="om-yan om-yan--sol">{koltuk(sol, 'sol')}</div>}
        <div className="om-sahne">
          {duzen2 && (
            <div className="om-duzenserit" role="toolbar" aria-label="Masayı düzenle">
              <span>Masayı düzenliyorsun{duzen2.secili.length ? ` · ${duzen2.secili.length} taş seçili` : ''}</span>
              <button type="button" className="om-dugme" onClick={() => setDuzen2(null)}><X size={16} aria-hidden="true" /> Vazgeç</button>
              <button type="button" className="om-dugme om-dugme--birincil" disabled={taslakGecersiz.size > 0} onClick={duzenOnayla}><Check size={16} aria-hidden="true" /> Onayla</button>
            </div>
          )}
          {kastet && (
            <div className="om-ciftalan" aria-label="Çift alanı">
              <span className="om-ciftalan-baslik">Seri alanı <b>{masaPerler.length}</b>/{A.KASTET_ALAN}{masaPerler.length < A.KASTET_ALAN ? ' · çift alanı kapalı' : ' · Çift alanı'}</span>
              {ciftAlan.map((p) => (
                <span key={p.id} className="om-cift" data-per={p.id}>
                  {p.taslar.map((t) => <span key={t.id} className={`om-pertas${can.gizli.has(t.id) ? ' om-gizli' : ''}`} data-om-pertas={t.id}><TasGorsel tas={t} renkler={renkler} tema={tema} okey={okey} /></span>)}
                </span>
              ))}
            </div>
          )}
          <div className="om-masa">
            <PerAlani
              oda={oda} perler={taslakPerler ?? (acik ? gorunenPerler.filter((p) => p.tur !== 'cift') : gorunenPerler)} okey={okey} uygun={uygun} aktif={aktifIds.length > 0 && siraBende} yeniUygun={yeniUygun}
              gizli={can.gizli} hale={can.hale} ipucuPer={ipucu?.per} bolSayi={aktifIds.length === 1 ? elMap.get(aktifIds[0])?.s : undefined} bolunen={can.bolunen} ipucuYeni={!!ipucu?.yeni} enBuyuk={Math.max(26, Math.min(56, Math.round(duzen.b * 0.86)))}
              onUc={(per, uc) => hedefeDokun(() => { if (duzen2) duzenTasi(per - 1000); else if (secili.length) isle(secili, per, uc); })}
              onPer={(per) => hedefeDokun(() => { if (duzen2) duzenTasi(per - 1000); else if (secili.length) isle(secili, per); })}
              onYeni={() => hedefeDokun(() => { if (duzen2) duzenTasi('yeni'); else if (secili.length) perAc(secili); })}
              duzen={duzen2 ? { secili: new Set(duzen2.secili), gecersiz: taslakGecersiz, onTas: (id) => setDuzen2((d) => d && (elMap.has(id)
                // Taslağa elden konan taş: dokununca ıstakaya geri döner
                ? { gruplar: d.gruplar.map((x) => x.filter((y) => y !== id)), secili: d.secili.filter((x) => x !== id) }
                : { ...d, secili: d.secili.includes(id) ? d.secili.filter((x) => x !== id) : [...d.secili, id] })) } : undefined}
            />
            <div className="om-destekolon">
              <div
                className={`om-deste${cekebilir ? ' om-deste--cek' : ''}${ipucu?.kaynak === 'deste' ? ' om-deste--ipucu' : ''}${g.deste ? '' : ' om-deste--bos'}`}
                data-om-deste="" {...(cekebilir ? { 'data-om-src': 'deste', 'data-om-id': -1, role: 'button', tabIndex: 0, 'aria-label': `Desteden taş çek, kalan ${g.deste}` } : null)}
                onKeyDown={(e) => { if (cekebilir && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); cek('deste'); } }}
              >
                {g.deste > 0 && [2, 1, 0].slice(g.deste >= 3 ? 0 : 3 - g.deste).map((i) => <TasGorsel key={i} className={`om-deste-tas om-deste-tas--${i}`} tas={{ id: -1, s: 1, r: 0 }} kapali renkler={renkler} tema={tema} />)}
                <span className="om-deste-say">{g.deste}</span>
              </div>
              {g.gosterge && (
                <div className="om-gosterge" title="Gösterge taşı: okey bunun bir üstü">
                  <TasGorsel tas={g.gosterge} renkler={renkler} tema={tema} />
                  <span className="om-gosterge-yazi">Gösterge</span>
                  {okey && <span className="om-okeybilgi">Okey <b style={{ color: renkler[okey.r] }}>{okey.s}</b></span>}
                </div>
              )}
              {atikli && benO && (
                <div className="om-benatik" onClick={() => hedefeDokun(() => { if (secili.length) at(secili); })}>
                  <AtikYigini o={benO} oda={oda} okey={okey} gizli={can.gizli} ben hedef={atikHedef} />
                </div>
              )}
            </div>
          </div>
        </div>
        {sag && <div className="om-yan om-yan--sag">{koltuk(sag, 'sag')}</div>}
        {can.akis.length > 0 && (
          <ol key={can.akis[can.akis.length - 1].id} className="om-akis" aria-label="Son hamleler">
            {can.akis.slice(-4).map((a) => <li key={a.id}>{a.metin}</li>)}
          </ol>
        )}
      </div>

      <div className="om-alt">
        {bildirim && <div key={bildirim.n} className={`om-bildirim om-bildirim--${bildirim.tur}`} role="status">{bildirim.metin}</div>}
        <EylemCubugu eylemler={eylemler} durum={durumYazi} kisa={duzen.kisa}>
          {benO && (benO.cezalar.length > 0 || benO.takim) && <span className="om-benrozet">{benO.takim && <em className={`om-takim om-takim--${benO.takim}`}>Takım {benO.takim}</em>}<CezaRozetleri o={benO} /></span>}
          {remiAcilis && (
            <span className={`om-balon${remiAcilis.toplam >= A.REMI_ACILIS ? ' om-balon--tamam' : ''}`} title="Istakada boşlukla ayırdığın geçerli perlerin toplamı">
              <b>{remiAcilis.toplam}</b><i>/ {A.REMI_ACILIS}</i>
            </span>
          )}
          {acilis && (
            <span className={`om-balon${acilis.toplam >= Z.ACILIS_ESIK || acilis.ciftler.length >= Z.ACILIS_CIFT ? ' om-balon--tamam' : ''}`} title="Istakada boşlukla ayırdığın geçerli perlerin toplamı">
              <b>{acilis.toplam}</b><i>/ 101</i>{acilis.ciftler.length > 0 && <span>{acilis.ciftler.length} çift</span>}
            </span>
          )}
        </EylemCubugu>
        <Istaka
          yuva={yuva} taslar={elMap} b={duzen.b} renkler={renkler} tema={tema} okey={okey}
          secili={seciliKume} kaynak={sur.sur?.src === 'el' ? new Set(sur.sur.ids) : BOS_KUME} ipucu={ipucu?.taslar ?? BOS_KUME}
          gizli={taslakEl.size ? new Set([...can.gizli, ...taslakEl]) : can.gizli} yeni={can.yeni} sarsilan={can.sarsilan} yandan={g.yandanAlinan ?? undefined}
          siraBende={siraBende} isilti={can.isilti} hedefAcik={secili.length > 0 && !sur.sur} rectler={rectler} sabit={sabit}
          onYuva={(i) => hedefeDokun(() => { if (secili.length && yuva.d[i] === null) { yuvaKoy(tasi(yuva, yuvaSirasi(yuva, secili), i)); setSecili([]); sesCal('birak'); } })}
          onTus={(id) => setSecili((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]))}
        />
      </div>

      {can.serit && <div key={can.serit.anahtar} className="om-serit" role="status"><Gift size={20} aria-hidden="true" />{can.serit.metin}</div>}
      {can.ceza && (
        <div key={can.ceza.anahtar} className={`om-cezakart om-cezakart--${cezaTur}`} role="alert">
          <span className="om-cezakart-ikon">{cezaTur === 'per' ? <Layers size={26} /> : cezaTur === 'islek' ? <ArrowUpFromLine size={26} /> : <AlertTriangle size={26} />}</span>
          <span className="om-cezakart-yazi"><b>{can.ceza.o === ben ? 'Ceza aldın' : `${cezaAd} ceza aldı`}</b><span>{can.ceza.ceza.aciklama || CEZA_BILGI[can.ceza.ceza.tur]?.ad || 'Ceza'}</span></span>
          <span className="om-cezakart-puan">{String(can.ceza.ceza.puan).replace('-', '−')}</span>
        </div>
      )}
      <UcusKatmani kok={kokEl} renkler={renkler} tema={tema} okey={okey} />
      {sur.sur && (
        <div ref={sur.hayalet} className={`om-hayalet om-hayalet--${sur.sur.durum}`} style={{ '--om-b': `${duzen.b}px`, opacity: 0 } as React.CSSProperties} aria-hidden="true">
          {hayaletTaslar.map((t, i) => <TasGorsel key={t?.id ?? `k${i}`} tas={t ?? { id: -1, s: 1, r: 0 }} kapali={!t} renkler={renkler} tema={tema} okey={okey} />)}
        </div>
      )}
      {onay && (
        <div className="om-onay" role="dialog" aria-modal="true" aria-label="Ceza uyarısı">
          <div className="om-onay-kart">
            <AlertTriangle size={26} aria-hidden="true" />
            <p>{onay.metin}</p>
            <div className="om-onay-dugmeler">
              <button type="button" className="om-dugme om-dugme--birincil" onClick={() => setOnay(null)} autoFocus>Vazgeç</button>
              <button type="button" className="om-dugme om-dugme--tehlike" onClick={() => { const c = onay.calis; setOnay(null); c(); }}>{onay.evet}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
