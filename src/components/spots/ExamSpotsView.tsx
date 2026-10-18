import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Search, X } from 'lucide-react';
import { useStorageRefresh } from '../../hooks/useStorageRefresh';
import { SpotCard } from './SpotCard';
import { QuickOptions, QuickPill, type QuickOption, type ToolbarQuick } from '../ui/PageToolbar';
import kurulIndex from '../../data/kazanimlar/index.json';
import { ANAHTAR, KATEGORILER, Kategori, Spot, Veri, azHareket, kucuk, okuOgrenilen, yazOgrenilen } from './spotsShared';
import { useAppearance } from '../../utils/appearance';
import { SpotsV12 } from '../v12/SpotsV12';
import { BRANSLAR, bransOku, type Brans } from './brans';
import { SpotCozucuDevamKart } from './stats/SpotCozucuDevamKart';
import { ekleSpotSure, type LastSpotInfo, type LastCozucuInfo } from '../../services/spotCozucuIstatistik';

export { KATEGORILER };

/**
 * Sınav spotları (Kurul 1). Veri: src/data/exam_spots_k1.json — scripts/sinav_spotlari/birlestir.py üretir;
 * her spotun ders notundan birebir alıntısı dogrula.py ile denetlenir. Sayfa yalnız gösterir.
 * Yerleşim (kapsayıcı genişliğine göre, styles/spots.css .xs-*):
 *  - telefon: başlık (ilerleme halkası) · Oku/Kendini sına · ders hapları · kategori çipleri · tek sütun kart
 *  - tablet: aynı şeritler, kartlar 2 sütun
 *  - masaüstü: ders rayı (260) | 2 sütun kart | süzgeç paneli (280: arama, kategori, önem)
 * Kartlar 30'ar 30'ar çizilir (IntersectionObserver). ?id=<spotId> ile gelen spota kaydırılır ve vurgulanır.
 * "Öğrendim" işareti tarayıcıda (medsoru_spot_ogrendim) tutulur; profil eşitlemesi useStorageRefresh ile gelir.
 */

const SAYFA = 30;
type OnemSuzgec = 'hepsi' | 'yuksek' | 'ogrenilmemis';
const ONEM_SECENEK: { id: OnemSuzgec; ad: string }[] = [
  { id: 'hepsi', ad: 'Hepsi' },
  { id: 'yuksek', ad: 'Yüksek' },
  { id: 'ogrenilmemis', ad: 'Öğrenilmemiş' },
];

/** Spot → kazanım eşlemesi (scripts/sinav_spotlari/kazanim_esle.py, bge-m3 ile en yakın kazanım) */
interface KazanimEsleme { dersler: Record<string, string[]>; spotlar: Record<string, number> }
const KURULLAR = (kurulIndex as { kurul: number; name: string }[]).map((k) => ({ no: k.kurul, ad: k.name }));

const tr = (n: number) => n.toLocaleString('tr-TR');

/** Öğrenilen yüzdesi halkası */
const Halka: React.FC<{ oran: number }> = ({ oran }) => {
  const r = 17;
  const c = 2 * Math.PI * r;
  const yuzde = Math.round(oran * 100);
  return (
    <span className="xs-ring" role="img" aria-label={`Yüzde ${yuzde} öğrenildi`}>
      <svg viewBox="0 0 40 40" aria-hidden>
        <circle cx="20" cy="20" r={r} className="xs-ring-bg" />
        <circle cx="20" cy="20" r={r} className="xs-ring-fg" strokeDasharray={c} strokeDashoffset={c * (1 - oran)} />
      </svg>
      <b aria-hidden>%{yuzde}</b>
    </span>
  );
};

/** Yüklenirken gerçek kart biçiminde iskelet */
const IskeletKart: React.FC<{ i: number }> = ({ i }) => (
  <div className="xs-card xs-card-skel" aria-hidden>
    <div className="xs-card-top"><span className="ui-skel" style={{ width: 64, height: 18 }} /><span className="ui-skel" style={{ width: 18, height: 12 }} /></div>
    <span className="ui-skel" style={{ width: `${55 + (i % 3) * 12}%`, height: 17 }} />
    <span className="ui-skel" style={{ width: '100%', height: 13 }} />
    <span className="ui-skel" style={{ width: `${70 + (i % 2) * 18}%`, height: 13 }} />
    {i % 2 === 0 && <span className="ui-skel" style={{ width: '100%', height: 36, borderRadius: 10 }} />}
    <div className="xs-card-f"><span className="ui-skel" style={{ width: 96, height: 30, borderRadius: 8 }} /><span className="ui-skel" style={{ width: 70, height: 30, borderRadius: 8 }} /></div>
  </div>
);

/** v12 "Net" ayrı bileşendir (canvas Cards.dc.html › Spotlar); tasarım değişince kancalar karışmasın diye ayrı tür. */
const OnemListesi = React.lazy(() => import('./OnemListesi'));
const SoruCozucuSayfa = React.lazy(() => import('./cozucu/SoruCozucuSayfa'));
type Gorunum = 'spot' | 'onem' | 'cozucu';
const okuGorunum = (): Gorunum => {
  try { const g = new URLSearchParams(location.search).get('gorunum'); return g === 'onem' || g === 'cozucu' ? g : 'spot'; } catch { return 'spot'; }
};

const okuBrans = (): Brans => { try { return bransOku(new URLSearchParams(location.search).get('brans')); } catch { return 'patoloji'; } };

/** Üstte görünüm seçici: Sınav spotları (tüm dersler) | En önemliler (100 puan, ders PDF'ine dayalı) | Sesli soru çözücü;
 *  son ikisinde branş seçici (Patoloji · Enfeksiyon · Üroloji, ?brans=). */
export const ExamSpotsView: React.FC = () => {
  const v12 = useAppearance().design === 'v12';
  const [g, setG] = useState<Gorunum>(okuGorunum);
  const [brans, setBrans] = useState<Brans>(okuBrans);
  useEffect(() => {
    const f = () => { setG(okuGorunum()); setBrans(okuBrans()); };
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, []);
  const sec = (x: Gorunum) => {
    setG(x);
    try {
      const u = new URL(location.href);
      if (x !== 'spot') u.searchParams.set('gorunum', x); else u.searchParams.delete('gorunum');
      if (x !== 'cozucu') u.searchParams.delete('coz');
      history.replaceState(history.state, '', u.pathname + u.search + u.hash);
    } catch { /* yok */ }
  };
  const bransSec = (b: Brans) => {
    if (b === brans) return;
    setBrans(b);
    try {
      const u = new URL(location.href);
      if (b !== 'patoloji') u.searchParams.set('brans', b); else u.searchParams.delete('brans');
      ['ders', 'coz', 'asistan', 'madde'].forEach((k) => u.searchParams.delete(k)); // ders kodları branşa özgü
      history.replaceState(history.state, '', u.pathname + u.search + u.hash);
    } catch { /* yok */ }
  };
  // Spotlarda aktif çalışma süresi sayacı
  useEffect(() => {
    if (g !== 'spot' && g !== 'onem') return;
    let sonHareket = Date.now();
    const hareket = () => { sonHareket = Date.now(); };
    window.addEventListener('pointerdown', hareket, { passive: true, capture: true });
    window.addEventListener('keydown', hareket, { passive: true, capture: true });
    window.addEventListener('scroll', hareket, { passive: true, capture: true });
    const TICK = 10;
    const tid = window.setInterval(() => {
      if (document.visibilityState !== 'visible' || Date.now() - sonHareket > 60_000) return;
      ekleSpotSure(TICK);
    }, TICK * 1000);
    return () => {
      window.clearInterval(tid);
      window.removeEventListener('pointerdown', hareket, { capture: true });
      window.removeEventListener('keydown', hareket, { capture: true });
      window.removeEventListener('scroll', hareket, { capture: true });
    };
  }, [g]);

  const onDevamSpot = (s: LastSpotInfo) => {
    sec('spot');
    try {
      const u = new URL(location.href);
      u.searchParams.delete('gorunum');
      if (s.id) u.searchParams.set('id', s.id);
      history.replaceState(history.state, '', u.pathname + u.search + u.hash);
      window.dispatchEvent(new PopStateEvent('popstate'));
    } catch { /* yok */ }
  };

  const onDevamCozucu = (c: LastCozucuInfo) => {
    bransSec(c.brans);
    sec('cozucu');
    try {
      const u = new URL(location.href);
      u.searchParams.set('gorunum', 'cozucu');
      if (c.brans !== 'patoloji') u.searchParams.set('brans', c.brans);
      u.searchParams.set('ders', c.kod);
      u.searchParams.set('coz', '1');
      history.replaceState(history.state, '', u.pathname + u.search + u.hash);
      window.dispatchEvent(new PopStateEvent('popstate'));
    } catch { /* yok */ }
  };

  return (
    <>
      <h1 className="sr-only">Sınav spotları</h1>
      <div className="ol-gorunum" role="tablist" aria-label="Görünüm">
        <button type="button" role="tab" aria-selected={g === 'spot'} className={g === 'spot' ? 'is-on' : ''} onClick={() => sec('spot')}>Spotlar</button>
        <button type="button" role="tab" aria-selected={g === 'onem'} className={g === 'onem' ? 'is-on' : ''} onClick={() => sec('onem')}>En önemliler<span className="ol-g-ek">(100 puan)</span></button>
        <button type="button" role="tab" aria-selected={g === 'cozucu'} className={g === 'cozucu' ? 'is-on' : ''} onClick={() => sec('cozucu')}>Soru çözücü</button>
      </div>
      {g !== 'spot' && (
        <div className="ol-gorunum ol-brans" role="tablist" aria-label="Ders">
          {BRANSLAR.map((b) => (
            <button key={b.id} type="button" role="tab" aria-selected={brans === b.id} className={brans === b.id ? 'is-on' : ''} onClick={() => bransSec(b.id)}>{b.ad}</button>
          ))}
        </div>
      )}
      <SpotCozucuDevamKart
        onDevamSpot={onDevamSpot}
        onDevamCozucu={onDevamCozucu}
        onBransSec={(b) => {
          bransSec(b);
          sec('cozucu');
        }}
      />
      {g === 'onem' ? (
        <React.Suspense fallback={<p className="ol-bos">Yükleniyor…</p>}><OnemListesi key={brans} brans={brans} /></React.Suspense>
      ) : g === 'cozucu' ? (
        <React.Suspense fallback={<p className="ol-bos">Yükleniyor…</p>}><SoruCozucuSayfa key={brans} brans={brans} /></React.Suspense>
      ) : v12 ? <SpotsV12 /> : <ExamSpotsClassic />}
    </>
  );
};

const ExamSpotsClassic: React.FC = () => {
  const [veri, setVeri] = useState<Veri | null>(null);
  const [hata, setHata] = useState(false);
  const [q, setQ] = useState('');
  const [aramaAcik, setAramaAcik] = useState(false);
  const [ders, setDers] = useState(0); // 0 = tüm konular (tek ders notu = konu)
  const [disiplin, setDisiplin] = useState(''); // '' = tüm dersler (Tıbbi Patoloji, Üroloji…)
  const [kazanim, setKazanim] = useState(''); // '' | "<konu no>:<kazanım sırası>"
  const [kurulS, setKurulS] = useState(0); // 0 = tüm kurullar
  const [esleme, setEsleme] = useState<KazanimEsleme | null>(null);
  const [katlar, setKatlar] = useState<Set<Kategori>>(() => new Set()); // boş = hepsi
  const [onemS, setOnemS] = useState<OnemSuzgec>('hepsi');
  const [sinav, setSinav] = useState(false);
  const [ogrenilen, setOgrenilen] = useState<Set<string>>(okuOgrenilen);
  useStorageRefresh([ANAHTAR], () => setOgrenilen(okuOgrenilen()));
  const [limit, setLimit] = useState(SAYFA);
  const [odak, setOdak] = useState<string | null>(() => {
    try { return new URLSearchParams(window.location.search).get('id'); } catch { return null; }
  });
  const [vurgu, setVurgu] = useState<string | null>(null);

  const sayfaRef = useRef<HTMLDivElement>(null);
  const seritRef = useRef<HTMLDivElement>(null);
  const bekciRef = useRef<HTMLDivElement>(null);
  const aramaRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let iptal = false;
    import('../../data/exam_spots_k1.json')
      .then((m) => { if (!iptal) setVeri((m.default ?? m) as unknown as Veri); })
      .catch(() => { if (!iptal) setHata(true); });
    import('../../data/exam_spots_k1_kazanim.json')
      .then((m) => { if (!iptal) setEsleme((m.default ?? m) as unknown as KazanimEsleme); })
      .catch(() => { /* kazanım süzgeci boş kalır */ });
    return () => { iptal = true; };
  }, []);

  // Arama için her spotun küçük harfli metni bir kez hazırlanır
  const aramaMetni = useMemo(() => {
    const m = new Map<string, string>();
    for (const s of veri?.spotlar || []) {
      m.set(s.id, kucuk([s.baslik, s.spot, s.tuzak, s.cevap, s.soru, ...(s.maddeler || []), ...(s.etiketler || [])].filter(Boolean).join(' ')));
    }
    return m;
  }, [veri]);

  const dersMap = useMemo(() => new Map((veri?.dersler || []).map((d) => [d.no, d])), [veri]);

  // Ders başına toplam / öğrenilen (ray ilerleme çubukları)
  const dersToplam = useMemo(() => {
    const m = new Map<number, number>();
    for (const s of veri?.spotlar || []) m.set(s.ders, (m.get(s.ders) || 0) + 1);
    return m;
  }, [veri]);
  const dersOgrenilen = useMemo(() => {
    const m = new Map<number, number>();
    for (const s of veri?.spotlar || []) if (ogrenilen.has(s.id)) m.set(s.ders, (m.get(s.ders) || 0) + 1);
    return m;
  }, [veri, ogrenilen]);

  // Kategori dışındaki süzgeçler (kategori sayıları buradan)
  const temel = useMemo(() => {
    if (!veri) return [] as Spot[];
    const kelimeler = kucuk(q.trim()).split(/\s+/).filter(Boolean);
    return veri.spotlar.filter((s) => {
      if (kurulS && kurulS !== (veri.kurul ?? 1)) return false;
      if (ders && s.ders !== ders) return false;
      if (disiplin && dersMap.get(s.ders)?.disiplin !== disiplin) return false;
      if (kazanim && `${s.ders}:${esleme?.spotlar[s.id]}` !== kazanim) return false;
      if (onemS === 'yuksek' && s.onem < 3) return false;
      if (onemS === 'ogrenilmemis' && ogrenilen.has(s.id)) return false;
      if (kelimeler.length) {
        const t = aramaMetni.get(s.id) || '';
        if (!kelimeler.every((w) => t.includes(w))) return false;
      }
      return true;
    });
  }, [veri, ders, disiplin, kazanim, kurulS, esleme, dersMap, onemS, ogrenilen, q, aramaMetni]);

  const katSayi = useMemo(() => {
    const m: Partial<Record<Kategori, number>> = {};
    for (const s of temel) m[s.kategori] = (m[s.kategori] || 0) + 1;
    return m;
  }, [temel]);

  const liste = useMemo(
    () => (katlar.size ? temel.filter((s) => katlar.has(s.kategori)) : temel).slice().sort((a, b) => a.ders - b.ders),
    [temel, katlar],
  );

  // Süzgeç değişince çizim sınırı başa döner
  const katAnahtar = [...katlar].sort().join(',');
  useEffect(() => { setLimit(SAYFA); }, [ders, disiplin, kazanim, kurulS, katAnahtar, onemS, q]);

  // Sona yaklaşınca 30 kart daha
  useEffect(() => {
    const el = bekciRef.current;
    if (!el || liste.length <= limit) return;
    const io = new IntersectionObserver((e) => {
      if (e.some((x) => x.isIntersecting)) setLimit((l) => l + SAYFA);
    }, { rootMargin: '800px 0px' });
    io.observe(el);
    return () => io.disconnect();
  }, [limit, liste.length]);

  // Derin bağlantı: önce spotun dersine geç, süzgeçleri aç ...
  const odakHazir = useRef(false);
  useEffect(() => {
    if (!veri || !odak || odakHazir.current) return;
    odakHazir.current = true;
    const s = veri.spotlar.find((x) => x.id === odak);
    if (!s) { setOdak(null); return; }
    setDers(s.ders);
    setDisiplin(''); setKazanim(''); setKurulS(0);
    setKatlar(new Set());
    setOnemS('hepsi');
    setQ('');
  }, [veri, odak]);
  // ... sonra kart çizilene kadar sınırı büyüt, kaydır ve kısa süre vurgula
  useEffect(() => {
    if (!veri || !odak || !odakHazir.current) return;
    const i = liste.findIndex((x) => x.id === odak);
    if (i < 0) return;
    if (i >= limit) { setLimit(i + SAYFA); return; }
    const id = odak;
    const raf = requestAnimationFrame(() => {
      document.getElementById(`xs-${id}`)?.scrollIntoView({ block: 'center', behavior: azHareket() ? 'auto' : 'smooth' });
      setVurgu(id);
      setOdak(null);
    });
    return () => cancelAnimationFrame(raf);
  }, [veri, odak, liste, limit]);
  useEffect(() => {
    if (!vurgu) return;
    const t = window.setTimeout(() => setVurgu(null), 2400);
    return () => window.clearTimeout(t);
  }, [vurgu]);

  // Seçili ders hapı şeritte görünür kalsın (sayfa dikey kaymadan)
  useEffect(() => {
    const serit = seritRef.current;
    const hap = serit?.querySelector<HTMLElement>('[aria-selected="true"]');
    if (!serit || !hap || !serit.clientWidth) return;
    const sol = hap.offsetLeft - serit.offsetLeft;
    if (sol < serit.scrollLeft || sol + hap.offsetWidth > serit.scrollLeft + serit.clientWidth) {
      serit.scrollTo({ left: Math.max(0, sol - 16), behavior: azHareket() ? 'auto' : 'smooth' });
    }
  }, [ders, veri]);

  useEffect(() => { if (aramaAcik) aramaRef.current?.focus(); }, [aramaAcik]);

  const ogren = useCallback((id: string) => setOgrenilen((p) => {
    const n = new Set(p);
    if (n.has(id)) n.delete(id); else n.add(id);
    yazOgrenilen(n);
    return n;
  }), []);

  const dersSec = (no: number) => {
    setDers(no);
    if (!kazanim.startsWith(`${no}:`)) setKazanim('');
    const el = sayfaRef.current;
    if (el && el.getBoundingClientRect().top < 0) el.scrollIntoView({ block: 'start', behavior: azHareket() ? 'auto' : 'smooth' });
  };
  const katDegistir = (k: Kategori) => setKatlar((p) => {
    const n = new Set(p);
    if (n.has(k)) n.delete(k); else n.add(k);
    return n;
  });
  // Panel onay kutuları: boş küme "hepsi işaretli" görünür; birini kaldırmak = diğerlerini seç
  const katKutu = (k: Kategori) => setKatlar((p) => {
    if (p.size === 0) return new Set(KATEGORILER.map((x) => x.id).filter((x) => x !== k));
    const n = new Set(p);
    if (n.has(k)) n.delete(k); else n.add(k);
    return n.size === KATEGORILER.length ? new Set() : n;
  });
  const temizle = () => { setKatlar(new Set()); setOnemS('hepsi'); setQ(''); setDisiplin(''); setKazanim(''); setKurulS(0); setDers(0); };

  const toplam = veri?.spotlar.length || 0;
  const ogrenilenSayi = useMemo(() => [...dersOgrenilen.values()].reduce((a, b) => a + b, 0), [dersOgrenilen]);
  const seciliDers = ders ? dersMap.get(ders) : undefined;
  const suzgecVar = katlar.size > 0 || onemS !== 'hepsi' || !!q.trim() || !!disiplin || !!kazanim || !!kurulS;
  const gorunen = liste.slice(0, limit);
  const kapsamToplam = seciliDers ? dersToplam.get(seciliDers.no) || 0 : toplam;

  // ---------- Kurul · Ders · Konu · Kazanım hızlı süzgeçleri (sayfayla birlikte kayar, yapışkan değil) ----------
  const disiplinler = useMemo(() => {
    const m = new Map<string, number>();
    for (const d of veri?.dersler || []) m.set(d.disiplin, (m.get(d.disiplin) || 0) + (dersToplam.get(d.no) || 0));
    return [...m.entries()].sort((a, b) => b[1] - a[1]);
  }, [veri, dersToplam]);
  const konular = useMemo(() => (veri?.dersler || []).filter((d) => !disiplin || d.disiplin === disiplin), [veri, disiplin]);
  const kazanimSayi = useMemo(() => {
    const m = new Map<string, number>();
    if (esleme) for (const [id, i] of Object.entries(esleme.spotlar)) { const no = id.match(/^k\d+-(\d+)-/)?.[1]; if (no) { const k = `${+no}:${i}`; m.set(k, (m.get(k) || 0) + 1); } }
    return m;
  }, [esleme]);
  const kazanimSecenek: QuickOption[] = useMemo(() => {
    if (!esleme) return [];
    const kaynak = ders ? konular.filter((d) => d.no === ders) : konular;
    return kaynak.flatMap((d) => (esleme.dersler[String(d.no)] || []).map((m, i) => ({
      id: `${d.no}:${i}`, label: m, count: kazanimSayi.get(`${d.no}:${i}`) || 0, group: ders ? undefined : `${d.no} · ${d.baslik}`,
    })));
  }, [esleme, konular, ders, kazanimSayi]);
  const kazanimMetni = kazanim && esleme ? esleme.dersler[kazanim.split(':')[0]]?.[+kazanim.split(':')[1]] : undefined;
  const kisalt = (t: string, n = 26) => (t.length > n ? `${t.slice(0, n - 1)}…` : t);
  const quick: ToolbarQuick[] = [
    {
      id: 'kurul', label: 'Kurul', value: kurulS ? `Kurul ${kurulS}` : undefined, onClear: () => setKurulS(0),
      content: (close) => <QuickOptions close={close} value={String(kurulS)} onPick={(id) => setKurulS(+id)}
        options={[{ id: '0', label: 'Tüm kurullar', count: toplam }, ...KURULLAR.map((k) => ({ id: String(k.no), label: `Kurul ${k.no}`, hint: k.ad, count: k.no === (veri?.kurul ?? 1) ? toplam : 0 }))]} />,
    },
    {
      id: 'ders', label: 'Ders', value: disiplin ? kisalt(disiplin, 22) : undefined, onClear: () => setDisiplin(''),
      content: (close) => <QuickOptions close={close} value={disiplin} onPick={(id) => {
        setDisiplin(id);
        if (id && ders && dersMap.get(ders)?.disiplin !== id) { setDers(0); setKazanim(''); }
      }} options={[{ id: '', label: 'Tüm dersler', count: toplam }, ...disiplinler.map(([ad, n]) => ({ id: ad, label: ad, count: n }))]} />,
    },
    {
      id: 'konu', label: 'Konu', value: seciliDers ? kisalt(`${seciliDers.no} · ${seciliDers.baslik}`) : undefined, onClear: () => dersSec(0), wide: true,
      content: (close) => <QuickOptions close={close} searchable placeholder="Konu ara" value={String(ders)} onPick={(id) => dersSec(+id)}
        options={[{ id: '0', label: 'Tüm konular' }, ...konular.map((d) => ({ id: String(d.no), label: `${d.no} · ${d.baslik}`, hint: disiplin ? undefined : d.disiplin, count: dersToplam.get(d.no) || 0 }))]} />,
    },
    {
      id: 'kazanim', label: 'Kazanım', value: kazanimMetni ? kisalt(kazanimMetni, 30) : undefined, onClear: () => setKazanim(''), wide: true,
      content: (close) => kazanimSecenek.length
        ? <QuickOptions close={close} searchable placeholder="Kazanım ara" value={kazanim} onPick={(id) => {
            setKazanim(id);
            const no = +id.split(':')[0];
            if (no && no !== ders) setDers(no);
          }} options={kazanimSecenek} />
        : <p className="pt-qo-empty">{esleme ? 'Bu seçim için kazanım yok' : 'Kazanımlar yükleniyor…'}</p>,
    },
  ];

  const aramaKutusu = (cls: string, ref?: React.Ref<HTMLInputElement>) => (
    <label className={`xs-search ${cls}`}>
      <Search size={15} aria-hidden />
      <input ref={ref} type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Spot ara (ör. en sık, Turner)" aria-label="Spotlarda ara"
        onKeyDown={(e) => { if (e.key === 'Escape') { setQ(''); setAramaAcik(false); } }} />
      {q && <button type="button" onClick={() => setQ('')} aria-label="Aramayı temizle"><X size={14} /></button>}
    </label>
  );

  const onemGrubu = (cls: string) => (
    <div className={`xs-seg xs-onem-seg ${cls}`} role="group" aria-label="Önem süzgeci">
      {ONEM_SECENEK.map((o) => (
        <button key={o.id} type="button" aria-pressed={onemS === o.id} className={onemS === o.id ? 'is-on' : ''} onClick={() => setOnemS(o.id)}>{o.ad}</button>
      ))}
    </div>
  );

  return (
    <div className="xs-page" ref={sayfaRef}>
      <div className="xs-layout">
        {/* ---------- Ders rayı (masaüstü) ---------- */}
        <aside className="xs-rail" aria-label="Dersler">
          <span className="xs-cap">{disiplin || 'Konular'} · Kurul {veri?.kurul ?? 1}</span>
          <div className="xs-rail-list" role="tablist" aria-orientation="vertical" aria-label="Ders seç">
            {!veri && Array.from({ length: 8 }, (_, i) => <span key={i} className="ui-skel xs-rail-skel" />)}
            {veri && (
              <button type="button" role="tab" aria-selected={ders === 0} aria-controls="xs-grid" className={`xs-rail-i${ders === 0 ? ' is-on' : ''}`} onClick={() => dersSec(0)}>
                <span className="xs-rail-no" aria-hidden>∑</span>
                <span className="xs-rail-mid">
                  <span className="xs-rail-t">Tüm konular</span>
                  <span className="xs-bar" aria-hidden><span style={{ width: `${toplam ? (ogrenilenSayi / toplam) * 100 : 0}%` }} /></span>
                </span>
                <span className="xs-rail-n">{tr(toplam)}</span>
              </button>
            )}
            {konular.map((d) => {
              const n = dersToplam.get(d.no) || 0;
              const o = dersOgrenilen.get(d.no) || 0;
              return (
                <button key={d.no} type="button" role="tab" aria-selected={ders === d.no} aria-controls="xs-grid" title={`${d.baslik} · ${d.disiplin}`}
                  className={`xs-rail-i${ders === d.no ? ' is-on' : ''}`} onClick={() => dersSec(d.no)}>
                  <span className="xs-rail-no">{d.no}</span>
                  <span className="xs-rail-mid">
                    <span className="xs-rail-t">{d.baslik}</span>
                    <span className="xs-bar" aria-hidden><span style={{ width: `${n ? (o / n) * 100 : 0}%` }} /></span>
                  </span>
                  <span className="xs-rail-n"><span className="sr-only">{o} / </span>{n}<span className="sr-only"> öğrenildi</span></span>
                </button>
              );
            })}
          </div>
        </aside>

        {/* ---------- Orta sütun ---------- */}
        <div className="xs-main">
          <header className="xs-head">
            <div className="xs-head-row">
              <Halka oran={toplam ? ogrenilenSayi / toplam : 0} />
              <div className="xs-head-t">
                <h1>Sınav spotları</h1>
                <span>{veri ? `${tr(ogrenilenSayi)} / ${tr(toplam)} öğrenildi · Kurul ${veri.kurul ?? 1}` : 'Yükleniyor…'}</span>
              </div>
              <button type="button" className={`xs-icon-btn xs-search-toggle${aramaAcik || q ? ' is-on' : ''}`} aria-label="Ara" aria-expanded={aramaAcik || !!q}
                onClick={() => setAramaAcik((v) => !v)}>
                <Search size={17} aria-hidden />
              </button>
            </div>
            {(aramaAcik || !!q) && aramaKutusu('xs-search-top', aramaRef)}
            <div className="xs-seg xs-mode" role="tablist" aria-label="Mod">
              <button type="button" role="tab" aria-selected={!sinav} className={!sinav ? 'is-on' : ''} onClick={() => setSinav(false)}>Oku</button>
              <button type="button" role="tab" aria-selected={sinav} className={sinav ? 'is-on' : ''} onClick={() => setSinav(true)}>Kendini sına</button>
            </div>
          </header>

          {/* Kurul · Ders · Konu · Kazanım (akışta; kaydırınca yer kaplamaz) */}
          {veri && (
            <div className="pt-quick xs-quick" role="toolbar" aria-label="Kurul, ders, konu ve kazanım süzgeçleri">
              {quick.map((x) => <QuickPill key={x.id} q={x} />)}
            </div>
          )}

          {/* Konu hapları (telefon/tablet) */}
          <div className="xs-strip" ref={seritRef} role="tablist" aria-label="Ders seç">
            {!veri && Array.from({ length: 9 }, (_, i) => <span key={i} className="ui-skel xs-pill-skel" />)}
            {veri && (
              <button type="button" role="tab" aria-selected={ders === 0} aria-controls="xs-grid" className={`xs-pill${ders === 0 ? ' is-on' : ''}`} onClick={() => dersSec(0)}>Tümü</button>
            )}
            {konular.map((d) => {
              const tamam = (dersOgrenilen.get(d.no) || 0) >= (dersToplam.get(d.no) || 1);
              return (
                <button key={d.no} type="button" role="tab" aria-selected={ders === d.no} aria-controls="xs-grid" aria-label={`Ders ${d.no}: ${d.baslik}${tamam ? ' (tamamlandı)' : ''}`} title={d.baslik}
                  className={`xs-pill${ders === d.no ? ' is-on' : ''}${tamam ? ' is-full' : ''}`} onClick={() => dersSec(d.no)}>
                  {d.no}
                </button>
              );
            })}
          </div>

          {/* Kategori çipleri (telefon/tablet) */}
          {veri && (
            <div className="xs-chips" role="group" aria-label="Kategori süzgeci">
              <button type="button" aria-pressed={katlar.size === 0} className={`xs-chip${katlar.size === 0 ? ' is-on' : ''}`} onClick={() => setKatlar(new Set())}>
                Tümü <span>{temel.length}</span>
              </button>
              {KATEGORILER.map((k) => (
                <button key={k.id} type="button" aria-pressed={katlar.has(k.id)} title={k.aciklama} disabled={!katSayi[k.id] && !katlar.has(k.id)}
                  className={`xs-chip k-${k.id}${katlar.has(k.id) ? ' is-on' : ''}`} onClick={() => katDegistir(k.id)}>
                  <i className="xs-dot" aria-hidden />{k.kisa} <span>{katSayi[k.id] || 0}</span>
                </button>
              ))}
            </div>
          )}

          {/* Bağlam satırı: seçili ders + önem (önem grubu masaüstünde panelde) */}
          {veri && (
            <div className="xs-ctx">
              <div className="xs-ctx-t">
                <h2>{seciliDers ? <><span>Konu {seciliDers.no} ·</span> {seciliDers.baslik}</> : (disiplin || 'Tüm konular')}</h2>
                <span aria-live="polite">
                  {seciliDers ? `${seciliDers.disiplin} · ` : ''}
                  {liste.length === kapsamToplam ? `${tr(liste.length)} spot` : `${tr(liste.length)} / ${tr(kapsamToplam)} spot`}
                  {seciliDers ? ` · ${dersOgrenilen.get(seciliDers.no) || 0} öğrenildi` : ''}
                </span>
                {kazanimMetni && <span className="xs-ctx-kz">Kazanım: {kazanimMetni}</span>}
              </div>
              {onemGrubu('xs-onem-inline')}
            </div>
          )}

          {hata && (
            <div className="xs-empty" role="alert">
              <p>Spot verisi yüklenemedi.</p>
              <button type="button" className="xs-act" onClick={() => window.location.reload()}>Sayfayı yenile</button>
            </div>
          )}

          <div className="xs-grid bento is-duo is-rhythm is-list" id="xs-grid" aria-busy={!veri && !hata}>
            {!veri && !hata && Array.from({ length: 6 }, (_, i) => <IskeletKart key={i} i={i} />)}
            {gorunen.map((s, i) => {
              const yeniDers = !ders && (i === 0 || gorunen[i - 1].ders !== s.ders);
              const d = dersMap.get(s.ders);
              return (
                <React.Fragment key={s.id}>
                  {yeniDers && (
                    <h3 className="xs-sec bt-full"><b>{s.ders}</b><span>{d?.baslik || 'Ders'}</span>{d?.disiplin && <small>{d.disiplin}</small>}</h3>
                  )}
                  <SpotCard s={s} sinav={sinav} ogrenildi={ogrenilen.has(s.id)} vurgulu={vurgu === s.id} onOgren={ogren} />
                </React.Fragment>
              );
            })}
          </div>

          {veri && liste.length === 0 && (
            <div className="xs-empty">
              <p>Bu süzgeçle spot yok.</p>
              {suzgecVar && <button type="button" className="xs-act" onClick={temizle}>Süzgeçleri temizle</button>}
            </div>
          )}
          {liste.length > limit && (
            <div ref={bekciRef} className="xs-more" aria-hidden><span className="ui-skel" /></div>
          )}
          {veri && liste.length > SAYFA && liste.length <= limit && (
            <p className="xs-end">{tr(liste.length)} spotun hepsi gösterildi</p>
          )}
        </div>

        {/* ---------- Süzgeç paneli (masaüstü) ---------- */}
        <aside className="xs-panel" aria-label="Süzgeçler">
          {aramaKutusu('xs-search-panel')}
          <fieldset className="xs-panel-sec">
            <legend className="xs-cap">Kategori</legend>
            {KATEGORILER.map((k) => (
              <label key={k.id} className={`xs-check k-${k.id}`} title={k.aciklama}>
                <input type="checkbox" checked={katlar.size === 0 || katlar.has(k.id)} disabled={!veri} onChange={() => katKutu(k.id)} />
                <i className="xs-dot" aria-hidden />
                <span className="xs-check-t">{k.kisa}</span>
                <span className="xs-check-n">{katSayi[k.id] || 0}</span>
              </label>
            ))}
          </fieldset>
          <div className="xs-panel-sec">
            <span className="xs-cap" id="xs-onem-cap">Önem</span>
            {onemGrubu('xs-onem-panel')}
          </div>
          {suzgecVar && <button type="button" className="xs-link" onClick={temizle}>Süzgeçleri temizle</button>}
        </aside>
      </div>
    </div>
  );
};

export default ExamSpotsView;
