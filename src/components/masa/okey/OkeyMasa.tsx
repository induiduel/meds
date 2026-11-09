/** Okey masası (yedili / takım / 101): kompozisyon, seçim, hamle gönderimi, asistan akışları. Durumun tek kaynağı `oda`. */
import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { AlertTriangle, ArrowDownToLine, ArrowDownUp, ArrowUpFromLine, CopyPlus, CornerDownLeft, Gift, Layers, Lightbulb, LockOpen, PlusSquare, SkipForward, Sparkles, Undo2, Wand2 } from 'lucide-react';
import type { OdaGorunum, OkeyGorunum, OkeyHamle, Tas } from '../../../services/masa/tipler';
import { masa, useMasa } from '../../../services/masa/istemci';
import * as Y from '../../../services/masa/motor/yediliAsistan';
import * as Z from '../../../services/masa/motor/yuzbirAsistan';
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
  const okey = yuzbir ? g.okey : undefined;
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
      const sutun = Math.max(enAz, Math.ceil((n + 4) / kat));
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
  const yuvaKoy = (y: YuvaDurum) => { setDepo({ a: anahtar, y }); yuvaYaz(oda.kod, g.elNo, y); };

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
    if (!okey || !benO || benO.acti) return null;
    const perler: number[][] = [], ciftler: number[][] = [];
    let toplam = 0;
    for (const ids of gruplar(yuva)) {
      if (ids.length < 2) continue;
      const c = Z.perCoz(ids.map((id) => elMap.get(id)!), okey);
      if (!c) continue;
      if (c.tur === 'cift') ciftler.push(ids); else { perler.push(ids); toplam += c.deger; }
    }
    return { perler, ciftler, toplam };
  }, [okey, benO, yuva, elMap]);

  const onceki = useMemo(() => { const i = g.oyuncular.findIndex((o) => o.id === ben); return i < 0 ? undefined : g.oyuncular[(i - 1 + g.oyuncular.length) % g.oyuncular.length]; }, [g.oyuncular, ben]);
  const yanTas = onceki && onceki.id !== ben ? onceki.atiklar?.[onceki.atiklar.length - 1] : undefined;
  const cekebilir = siraBende && !g.tur_.cekti && (yuzbir || !g.tur_.hamleYapti);
  const zorunlu = !yuzbir && siraBende ? Y.zorunlu(g, ben) : { per: false, islek: false };

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
    const yap = () => { ipucuYuva.current = yuvaIpucu; gonder(yuzbir ? { t: 'cek', kaynak } : { t: 'cek' }); };
    if (yuzbir) yap(); else cezaOnay('çekersen', yap);
  }
  const devret = () => { if (!siraBende) return void siraYok([]); cezaOnay('devredersen', () => gonder({ t: 'devret' })); };
  function isle(ids: number[], perId: number, uc?: 'bas' | 'son' | 'bol' | null): boolean {
    if (!siraBende) return siraYok(ids);
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
  const ipuclari = useMemo(() => (asistan && siraBende ? (yuzbir ? Z.ipuclari(g, ben) : Y.ipuclari(g, ben)) : []), [asistan, siraBende, yuzbir, g, ben]);
  const ipucuGoster = () => {
    if (!ipuclari.length) return bildir(siraBende ? (cekebilir ? 'Açılacak per ya da işlenecek taş yok: taş çek.' : 'Yapılacak hamle kalmadı: eli devret.') : 'Sıra sana gelince ipucu verebilirim.', 'bilgi');
    const ip = ipuclari[ipucuSira.current++ % ipuclari.length];
    const h = ip.hamle;
    setIpucu({ taslar: new Set(ip.taslar), per: ip.per, yeni: h.t === 'ac' || h.t === 'ac101', kaynak: h.t === 'cek' ? h.kaynak ?? 'deste' : undefined });
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

  const sirala = () => {
    const sira: Kip[] = yuzbir ? ['per', 'seri', 'grup'] : ['seri', 'grup'];
    kip.current = sira[(sira.indexOf(kip.current) + 1) % sira.length];
    yuvaKoy(diz(yuva, siraGruplari(kip.current)));
    setSecili([]); sesCal('birak');
    bildir(kip.current === 'per' ? 'Perlere göre dizildi' : kip.current === 'seri' ? 'Renge göre dizildi' : 'Sayıya göre dizildi', 'bilgi');
  };

  /* ---------------- eylem çubuğu ---------------- */
  const ik = { size: 18, 'aria-hidden': true } as const;
  const eylemler: Eylem[] = [];
  if (!yuzbir) {
    const isleVar = ipuclari.some((x) => x.hamle.t === 'isle');
    eylemler.push(
      { ad: 'ac', etiket: 'Per aç', ikon: <PlusSquare {...ik} />, etkin: siraBende && secili.length >= 3 && perMi(secili), birincil: true, calis: () => perAc(secili) },
      { ad: 'cek', etiket: 'Taş çek', ikon: <ArrowDownToLine {...ik} />, etkin: cekebilir, birincil: !zorunlu.per && !zorunlu.islek, calis: () => cek('deste') },
      { ad: 'devret', etiket: 'Eli devret', ikon: <SkipForward {...ik} />, etkin: siraBende && (g.tur_.cekti || g.tur_.hamleYapti || zorunlu.per || zorunlu.islek), birincil: !cekebilir && !zorunlu.per && !zorunlu.islek, calis: devret },
      { ad: 'sirala', etiket: 'Sırala', ikon: <ArrowDownUp {...ik} />, etkin: !kilit && g.elim.length > 1, calis: sirala },
    );
    if (asistan) eylemler.push(
      { ad: 'oto', etiket: 'Otomatik işle', ikon: <Wand2 {...ik} />, etkin: siraBende && isleVar && !oto, asistan: true, calis: () => setOto('isle') },
      { ad: 'plan', etiket: 'En iyi hamle', ikon: <Sparkles {...ik} />, etkin: siraBende && ipuclari.length > 0 && !oto, asistan: true, calis: () => { plan.current = Y.enIyiPlan(g, ben); if (plan.current.length) setOto('plan'); } },
    );
  } else {
    if (!g.tur_.cekti || !siraBende) eylemler.push(
      { ad: 'cek', etiket: 'Desteden çek', ikon: <ArrowDownToLine {...ik} />, etkin: cekebilir, birincil: true, calis: () => cek('deste') },
      { ad: 'yan', etiket: 'Yandan al', ikon: <CornerDownLeft {...ik} />, etkin: cekebilir && !!yanTas, calis: () => cek('atik') },
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
    eylemler.push({ ad: 'sirala', etiket: 'Diz', ikon: <ArrowDownUp {...ik} />, etkin: !kilit && g.elim.length > 1, calis: sirala });
  }
  if (asistan && tercih.ipucu !== false) eylemler.push({ ad: 'ipucu', etiket: 'İpucu', ikon: <Lightbulb {...ik} />, etkin: !kilit, asistan: true, calis: ipucuGoster });

  const durumYazi = kilit ? (oda.durdu ? 'Oyun durdu' : g.bitti || oda.asama !== 'oyun' ? 'El bitti' : 'İzliyorsun')
    : !siraBende ? `Sıra: ${oyuncuAdi(oda, g.sira)}`
    : yuzbir ? (!g.tur_.cekti ? 'Sıra sende: taş çek' : g.yandanAlinan != null ? 'Yandan aldığın taşı kullan' : benO?.acti ? 'İşle, per aç ya da taş at' : 'Aç ya da taş at')
    : zorunlu.per ? 'Açabileceğin per var' : zorunlu.islek ? 'İşlenecek taşın var' : cekebilir ? 'Sıra sende: taş çek' : 'Eli devredebilirsin';

  /* ---------------- sürükleme / seçim hedefleri ---------------- */
  const aktifIds = sur.sur ? (sur.sur.src === 'el' ? sur.sur.ids : []) : secili;
  const uygun = useMemo(() => {
    const s = new Set<string>();
    if (aktifIds.length === 1 && siraBende && hak) { const t = elMap.get(aktifIds[0]); if (t) for (const y of yerler(t)) s.add(`${y.per}:${y.uc ?? ''}`); }
    return s;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [aktifIds.join(','), siraBende, hak, yerler, elMap]);
  const yeniUygun = siraBende && aktifIds.length >= 2 && (!yuzbir || (!!benO?.acti && g.tur_.cekti)) && perMi(aktifIds);
  const atikHedef = yuzbir && siraBende && g.tur_.cekti && aktifIds.length === 1 && g.yandanAlinan == null;

  /* ---------------- oturma düzeni ---------------- */
  const rakipler = benOnde(g.oyuncular, ben).filter((o) => o.id !== ben);
  const k = rakipler.length;
  const yan = duzen.genis && k >= 2;
  const sag = yan ? rakipler[0] : undefined, sol = yan ? rakipler[k - 1] : undefined;
  const ust = (yan ? rakipler.slice(1, k - 1) : rakipler).slice().reverse();
  const koltuk = (o: typeof rakipler[number], yon: 'ust' | 'sol' | 'sag') => (
    <Koltuk key={o.id} oda={oda} g={g} o={o} yon={yon} sarsil={can.sarsilan.has(o.id)} gizli={can.gizli} alinabilir={cekebilir && yuzbir && onceki?.id === o.id && !!yanTas} />
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
          <div className="om-masa">
            <PerAlani
              oda={oda} perler={g.perler} okey={okey} uygun={uygun} aktif={aktifIds.length > 0 && siraBende} yeniUygun={yeniUygun}
              gizli={can.gizli} hale={can.hale} ipucuPer={ipucu?.per} bolSayi={aktifIds.length === 1 ? elMap.get(aktifIds[0])?.s : undefined} bolunen={can.bolunen} ipucuYeni={!!ipucu?.yeni} enBuyuk={Math.max(26, Math.min(56, Math.round(duzen.b * 0.86)))}
              onUc={(per, uc) => hedefeDokun(() => { if (secili.length) isle(secili, per, uc); })}
              onPer={(per) => hedefeDokun(() => { if (secili.length) isle(secili, per); })}
              onYeni={() => hedefeDokun(() => { if (secili.length) perAc(secili); })}
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
              {yuzbir && g.gosterge && (
                <div className="om-gosterge" title="Gösterge taşı: okey bunun bir üstü">
                  <TasGorsel tas={g.gosterge} renkler={renkler} tema={tema} />
                  <span className="om-gosterge-yazi">Gösterge</span>
                  {okey && <span className="om-okeybilgi">Okey <b style={{ color: renkler[okey.r] }}>{okey.s}</b></span>}
                </div>
              )}
              {yuzbir && benO && (
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
          {acilis && (
            <span className={`om-balon${acilis.toplam >= Z.ACILIS_ESIK || acilis.ciftler.length >= Z.ACILIS_CIFT ? ' om-balon--tamam' : ''}`} title="Istakada boşlukla ayırdığın geçerli perlerin toplamı">
              <b>{acilis.toplam}</b><i>/ 101</i>{acilis.ciftler.length > 0 && <span>{acilis.ciftler.length} çift</span>}
            </span>
          )}
        </EylemCubugu>
        <Istaka
          yuva={yuva} taslar={elMap} b={duzen.b} renkler={renkler} tema={tema} okey={okey}
          secili={seciliKume} kaynak={sur.sur?.src === 'el' ? new Set(sur.sur.ids) : BOS_KUME} ipucu={ipucu?.taslar ?? BOS_KUME}
          gizli={can.gizli} yeni={can.yeni} sarsilan={can.sarsilan} yandan={g.yandanAlinan ?? undefined}
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
