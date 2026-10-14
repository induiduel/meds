import React, { startTransition, useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { AlertTriangle, Check, ChevronDown, CopyCheck, CopyPlus, Eye, Search, Share2, SlidersHorizontal, X } from 'lucide-react';
import { useStorageRefresh } from '../../hooks/useStorageRefresh';
import { getFavoriteCards, toggleFavoriteCard } from '../../services/studyStore';
import { toast } from '../ui/Toast';
import {
  ANAHTAR, KAT, KATEGORILER, type Ders, type Kategori, type Spot, type Veri, Zengin, azHareket, kucuk, okuOgrenilen, yazOgrenilen,
} from '../spots/spotsShared';
import { CardsSpotsNav } from './FlashcardsV12';
import '../../styles/v12/cards.css';

/**
 * Sınav spotları — v12 "Net" (canvas Cards.dc.html, "Spotlar" görünümü).
 * Kompakt liste, derse (disiplin) göre gruplu; her satır: tür rozeti (Sınav spotu / Kritik uyarı) · kısa spot ·
 * kaynak satırı · "Karta ekle" · "Öğrendim". Ayrıntı (soru-cevap, maddeler, tablo, tuzak, alıntı, paylaş) satırda açılır.
 * Veri ve "öğrendim" kaydı ExamSpotsView ile aynı (exam_spots_k1.json, medsoru_spot_ogrendim). "Karta ekle"
 * kartı favori ezber kartlarına koyar (studyStore.toggleFavoriteCard) — Kartlar › Göz at › Favoriler'de çalışılır.
 * "Kritik uyarı" = kategori "Tuzak & çeldirici"; diğer kategoriler "Sınav spotu".
 */

const SAYFA = 30;
const KART_ONEK = 'spot:';
type Tip = 'hepsi' | 'spot' | 'uyari';
type OnemSuzgec = 'hepsi' | 'yuksek' | 'ogrenilmemis';
const ONEM_SECENEK: { id: OnemSuzgec; ad: string }[] = [
  { id: 'hepsi', ad: 'Hepsi' },
  { id: 'yuksek', ad: 'Yüksek önem' },
  { id: 'ogrenilmemis', ad: 'Öğrenilmemiş' },
];
const ONEM_AD: Record<number, string> = { 3: 'Kesin sorulur', 2: 'Sık sorulur', 1: 'Destekleyici' };

interface KazanimEsleme { dersler: Record<string, string[]>; spotlar: Record<string, number> }

const tr = (n: number) => n.toLocaleString('tr-TR');
const duz = (s?: string) => String(s || '').replace(/\*\*/g, '');
const uyariMi = (s: Spot) => s.kategori === 'tuzak';

export const SpotsV12: React.FC = () => {
  const [veri, setVeri] = useState<Veri | null>(null);
  const [hata, setHata] = useState(false);
  const [esleme, setEsleme] = useState<KazanimEsleme | null>(null);
  const [aramaGirdi, setAramaGirdi] = useState('');
  const [q, setQ] = useState('');
  const [disiplin, setDisiplin] = useState('');
  const [ders, setDers] = useState(0);
  const [kazanim, setKazanim] = useState('');
  const [katlar, setKatlar] = useState<Set<Kategori>>(() => new Set());
  const [tip, setTip] = useState<Tip>('hepsi');
  const [onemS, setOnemS] = useState<OnemSuzgec>('hepsi');
  const [sinav, setSinav] = useState(false);
  const [suzgecAcik, setSuzgecAcik] = useState(false);
  const [ogrenilen, setOgrenilen] = useState<Set<string>>(okuOgrenilen);
  useStorageRefresh([ANAHTAR], () => setOgrenilen(okuOgrenilen()));
  const [kartta, setKartta] = useState<Set<string>>(() => new Set(getFavoriteCards().map((c) => c.id)));
  useStorageRefresh(['medsoru_flashcard_favorites_v1'], () => setKartta(new Set(getFavoriteCards().map((c) => c.id))));
  const [limit, setLimit] = useState(SAYFA);
  const [odak, setOdak] = useState<string | null>(() => {
    try { return new URLSearchParams(window.location.search).get('id'); } catch { return null; }
  });
  const [vurgu, setVurgu] = useState<string | null>(null);
  const bekciRef = useRef<HTMLDivElement>(null);

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

  const aramaMetni = useMemo(() => {
    const m = new Map<string, string>();
    for (const s of veri?.spotlar || []) {
      m.set(s.id, kucuk([s.baslik, s.spot, s.tuzak, s.cevap, s.soru, ...(s.maddeler || []), ...(s.etiketler || [])].filter(Boolean).join(' ')));
    }
    return m;
  }, [veri]);

  const dersMap = useMemo(() => new Map((veri?.dersler || []).map((d) => [d.no, d])), [veri]);
  const dersToplam = useMemo(() => {
    const m = new Map<number, number>();
    for (const s of veri?.spotlar || []) m.set(s.ders, (m.get(s.ders) || 0) + 1);
    return m;
  }, [veri]);
  // Disiplin sırası: en küçük konu numarasına göre (ders notu sırası korunur)
  const disiplinSira = useMemo(() => {
    const m = new Map<string, number>();
    for (const d of veri?.dersler || []) if (!m.has(d.disiplin) || d.no < (m.get(d.disiplin) as number)) m.set(d.disiplin, d.no);
    return m;
  }, [veri]);

  const temel = useMemo(() => {
    if (!veri) return [] as Spot[];
    const kelimeler = kucuk(q.trim()).split(/\s+/).filter(Boolean);
    return veri.spotlar.filter((s) => {
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
  }, [veri, ders, disiplin, kazanim, esleme, dersMap, onemS, ogrenilen, q, aramaMetni]);

  const katSayi = useMemo(() => {
    const m: Partial<Record<Kategori, number>> = {};
    for (const s of temel) m[s.kategori] = (m[s.kategori] || 0) + 1;
    return m;
  }, [temel]);
  const katli = useMemo(() => (katlar.size ? temel.filter((s) => katlar.has(s.kategori)) : temel), [temel, katlar]);
  const tipSayi = useMemo(() => {
    let uyari = 0;
    for (const s of katli) if (uyariMi(s)) uyari++;
    return { hepsi: katli.length, uyari, spot: katli.length - uyari };
  }, [katli]);

  const liste = useMemo(() => {
    const l = tip === 'hepsi' ? katli : katli.filter((s) => (tip === 'uyari') === uyariMi(s));
    const sira = (s: Spot) => disiplinSira.get(dersMap.get(s.ders)?.disiplin || '') ?? 999;
    return l.slice().sort((a, b) => sira(a) - sira(b) || a.ders - b.ders);
  }, [katli, tip, disiplinSira, dersMap]);

  const grupSayi = useMemo(() => {
    const m = new Map<string, { n: number; o: number }>();
    for (const s of liste) {
      const k = dersMap.get(s.ders)?.disiplin || 'Diğer';
      const v = m.get(k) || { n: 0, o: 0 };
      v.n++;
      if (ogrenilen.has(s.id)) v.o++;
      m.set(k, v);
    }
    return m;
  }, [liste, dersMap, ogrenilen]);

  const katAnahtar = [...katlar].sort().join(',');
  useEffect(() => { setLimit(SAYFA); }, [ders, disiplin, kazanim, katAnahtar, onemS, q, tip]);

  useEffect(() => {
    const el = bekciRef.current;
    if (!el || liste.length <= limit) return;
    const io = new IntersectionObserver((e) => {
      if (e.some((x) => x.isIntersecting)) setLimit((l) => l + SAYFA);
    }, { rootMargin: '800px 0px' });
    io.observe(el);
    return () => io.disconnect();
  }, [limit, liste.length]);

  // Derin bağlantı (?id=): süzgeçleri spota göre aç, çizilene kadar sınırı büyüt, kaydır ve kısa süre vurgula
  const odakHazir = useRef(false);
  useEffect(() => {
    if (!veri || !odak || odakHazir.current) return;
    odakHazir.current = true;
    const s = veri.spotlar.find((x) => x.id === odak);
    if (!s) { setOdak(null); return; }
    setDers(s.ders); setDisiplin(''); setKazanim(''); setKatlar(new Set()); setTip('hepsi'); setOnemS('hepsi');
    setQ(''); setAramaGirdi('');
  }, [veri, odak]);
  useEffect(() => {
    if (!veri || !odak || !odakHazir.current) return;
    const i = liste.findIndex((x) => x.id === odak);
    if (i < 0) return;
    if (i >= limit) { setLimit(i + SAYFA); return; }
    const id = odak;
    const raf = requestAnimationFrame(() => {
      document.getElementById(`f12-sp-${id}`)?.scrollIntoView({ block: 'center', behavior: azHareket() ? 'auto' : 'smooth' });
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

  const ogren = useCallback((id: string) => setOgrenilen((p) => {
    const n = new Set(p);
    if (n.has(id)) n.delete(id); else n.add(id);
    yazOgrenilen(n);
    return n;
  }), []);

  const kartaEkle = useCallback((s: Spot) => {
    const id = `${KART_ONEK}${s.id}`;
    const front = duz(s.soru || s.baslik);
    const back = duz(s.cevap ? `${s.cevap} — ${s.spot}` : s.spot);
    const next = toggleFavoriteCard({ id, front, back, group: 'Sınav spotları' });
    const ekli = next.some((c) => c.id === id);
    setKartta(new Set(next.map((c) => c.id)));
    toast.show('success', ekli ? 'Kartlara eklendi' : 'Kartlardan çıkarıldı', ekli ? 'Kartlar › Göz at › Favoriler' : s.baslik);
  }, []);

  const aramaDegis = (v: string) => {
    setAramaGirdi(v);
    startTransition(() => setQ(v));
  };
  const katDegistir = (k: Kategori) => setKatlar((p) => {
    const n = new Set(p);
    if (n.has(k)) n.delete(k); else n.add(k);
    return n;
  });
  const temizle = () => {
    setKatlar(new Set()); setOnemS('hepsi'); setQ(''); setAramaGirdi(''); setDisiplin(''); setKazanim(''); setDers(0); setTip('hepsi');
  };

  const disiplinler = useMemo(() => {
    const m = new Map<string, number>();
    for (const d of veri?.dersler || []) m.set(d.disiplin, (m.get(d.disiplin) || 0) + (dersToplam.get(d.no) || 0));
    return [...m.entries()].sort((a, b) => b[1] - a[1]);
  }, [veri, dersToplam]);
  const konular = useMemo(() => (veri?.dersler || []).filter((d) => !disiplin || d.disiplin === disiplin), [veri, disiplin]);
  const kazanimSecenek = useMemo(() => {
    if (!esleme) return [] as { id: string; label: string }[];
    const kaynak = ders ? konular.filter((d) => d.no === ders) : konular;
    return kaynak.flatMap((d) => (esleme.dersler[String(d.no)] || []).map((m, i) => ({ id: `${d.no}:${i}`, label: ders ? m : `${d.no} · ${m}` })));
  }, [esleme, konular, ders]);

  const toplam = veri?.spotlar.length || 0;
  const ogrenilenSayi = useMemo(() => {
    if (!veri) return 0;
    let n = 0;
    for (const s of veri.spotlar) if (ogrenilen.has(s.id)) n++;
    return n;
  }, [veri, ogrenilen]);
  const aktifSuzgec = (disiplin ? 1 : 0) + (ders ? 1 : 0) + (kazanim ? 1 : 0) + katlar.size + (onemS !== 'hepsi' ? 1 : 0);
  const suzgecVar = aktifSuzgec > 0 || !!q.trim() || tip !== 'hepsi';
  const gorunen = liste.slice(0, limit);

  // Görünen dilimi disipline göre grupla
  const gruplar = useMemo(() => {
    const out: { ad: string; spotlar: Spot[] }[] = [];
    for (const s of gorunen) {
      const ad = dersMap.get(s.ders)?.disiplin || 'Diğer';
      const son = out[out.length - 1];
      if (son && son.ad === ad) son.spotlar.push(s); else out.push({ ad, spotlar: [s] });
    }
    return out;
  }, [gorunen, dersMap]);

  return (
    <div className="f12-page">
      <div className="f12-sp-col">
        <div className="f12-head">
          <CardsSpotsNav active="spots" />
          <span className="f12-grow" />
          <span className="f12-meta">
            {veri ? <>Kurul {veri.kurul ?? 1} · <span className="f12-num">{tr(ogrenilenSayi)} / {tr(toplam)}</span> öğrenildi</> : 'Yükleniyor…'}
          </span>
          <div className="f12-seg" role="radiogroup" aria-label="Mod">
            <button type="button" role="radio" aria-checked={!sinav} className={!sinav ? 'on' : ''} onClick={() => setSinav(false)}>Oku</button>
            <button type="button" role="radio" aria-checked={sinav} className={sinav ? 'on' : ''} onClick={() => setSinav(true)}>Kendini sına</button>
          </div>
        </div>

        <div className="f12-tool">
          <label className="f12-field f12-search">
            <Search aria-hidden className="f12-ico" />
            <span className="f12-sr">Spotlarda ara</span>
            <input type="search" value={aramaGirdi} placeholder="Spotlarda ara" onChange={(e) => aramaDegis(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Escape') aramaDegis(''); }} />
            {aramaGirdi && (
              <button type="button" className="f12-x" aria-label="Aramayı temizle" onClick={() => aramaDegis('')}><X aria-hidden /></button>
            )}
          </label>
          <div className="f12-filters" role="radiogroup" aria-label="Spot türü">
            {(
              [
                ['hepsi', 'Tümü', tipSayi.hepsi],
                ['spot', 'Sınav spotu', tipSayi.spot],
                ['uyari', 'Kritik uyarı', tipSayi.uyari],
              ] as const
            ).map(([id, ad, n]) => (
              <button key={id} type="button" role="radio" aria-checked={tip === id} className={`f12-pill${tip === id ? ' on' : ''}`} onClick={() => setTip(id)}>
                <span>{ad}</span><b>{tr(n)}</b>
              </button>
            ))}
          </div>
          <span className="f12-grow" />
          <button type="button" className={`f12-btn sm${suzgecAcik || aktifSuzgec ? ' is-on' : ''}`} aria-expanded={suzgecAcik} aria-controls="f12-sp-suzgec"
            onClick={() => setSuzgecAcik((v) => !v)}>
            <SlidersHorizontal aria-hidden /> Süzgeç{aktifSuzgec ? <span className="f12-num"> · {aktifSuzgec}</span> : null}
          </button>
        </div>

        {suzgecAcik && (
          <div className="f12-panel f12-sp-filter" id="f12-sp-suzgec">
            <div className="f12-sp-fgrid">
              <label className="f12-flab">
                <span className="f12-label">Ders</span>
                <span className="f12-field">
                  <select value={disiplin} onChange={(e) => {
                    const id = e.target.value;
                    setDisiplin(id);
                    if (id && ders && dersMap.get(ders)?.disiplin !== id) { setDers(0); setKazanim(''); }
                  }}>
                    <option value="">Tüm dersler · {tr(toplam)}</option>
                    {disiplinler.map(([ad, n]) => <option key={ad} value={ad}>{ad} · {tr(n)}</option>)}
                  </select>
                  <ChevronDown aria-hidden className="f12-ico" />
                </span>
              </label>
              <label className="f12-flab">
                <span className="f12-label">Konu</span>
                <span className="f12-field">
                  <select value={String(ders)} onChange={(e) => {
                    const no = +e.target.value;
                    setDers(no);
                    if (!kazanim.startsWith(`${no}:`)) setKazanim('');
                  }}>
                    <option value="0">Tüm konular</option>
                    {konular.map((d) => <option key={d.no} value={d.no}>{d.no} · {d.baslik} · {tr(dersToplam.get(d.no) || 0)}</option>)}
                  </select>
                  <ChevronDown aria-hidden className="f12-ico" />
                </span>
              </label>
              <label className="f12-flab">
                <span className="f12-label">Kazanım</span>
                <span className="f12-field">
                  <select value={kazanim} disabled={!kazanimSecenek.length} onChange={(e) => {
                    const id = e.target.value;
                    setKazanim(id);
                    const no = +id.split(':')[0];
                    if (no && no !== ders) setDers(no);
                  }}>
                    <option value="">{esleme ? (kazanimSecenek.length ? 'Tüm kazanımlar' : 'Bu seçim için kazanım yok') : 'Kazanımlar yükleniyor…'}</option>
                    {kazanimSecenek.map((k) => <option key={k.id} value={k.id}>{k.label}</option>)}
                  </select>
                  <ChevronDown aria-hidden className="f12-ico" />
                </span>
              </label>
            </div>
            <div className="f12-flab">
              <span className="f12-label" id="f12-sp-kat">Kategori</span>
              <div className="f12-filters is-wrap" role="group" aria-labelledby="f12-sp-kat">
                {KATEGORILER.map((k) => (
                  <button key={k.id} type="button" aria-pressed={katlar.has(k.id)} title={k.aciklama} disabled={!katSayi[k.id] && !katlar.has(k.id)}
                    className={`f12-pill${katlar.has(k.id) ? ' on' : ''}`} onClick={() => katDegistir(k.id)}>
                    <span>{k.kisa}</span><b>{tr(katSayi[k.id] || 0)}</b>
                  </button>
                ))}
              </div>
            </div>
            <div className="f12-flab">
              <span className="f12-label" id="f12-sp-onem">Önem</span>
              <div className="f12-seg" role="radiogroup" aria-labelledby="f12-sp-onem">
                {ONEM_SECENEK.map((o) => (
                  <button key={o.id} type="button" role="radio" aria-checked={onemS === o.id} className={onemS === o.id ? 'on' : ''} onClick={() => setOnemS(o.id)}>{o.ad}</button>
                ))}
              </div>
            </div>
            {suzgecVar && (
              <div><button type="button" className="f12-btn sm ghost" onClick={temizle}>Süzgeçleri temizle</button></div>
            )}
          </div>
        )}

        {hata && (
          <div className="f12-panel f12-empty" role="alert">
            <b>Spot verisi yüklenemedi.</b>
            <button type="button" className="f12-btn sm" onClick={() => window.location.reload()}>Sayfayı yenile</button>
          </div>
        )}

        {!veri && !hata && (
          <div className="f12-panel f12-list" aria-busy="true" aria-label="Spotlar yükleniyor">
            {Array.from({ length: 6 }, (_, i) => (
              <div key={i} className="f12-sp-row" aria-hidden>
                <span className="f12-skel" style={{ width: 76, height: 20 }} />
                <span className="f12-sp-txt">
                  <span className="f12-skel" style={{ width: `${60 + (i % 3) * 12}%`, height: 14 }} />
                  <span className="f12-skel" style={{ width: '40%', height: 11 }} />
                </span>
              </div>
            ))}
          </div>
        )}

        <div aria-live="polite" className="f12-sr">{veri ? `${tr(liste.length)} spot` : ''}</div>

        {gruplar.map((g, gi) => {
          const sayi = grupSayi.get(g.ad);
          const hid = `f12-sp-g-${gi}`;
          return (
            <section key={`${g.ad}-${gi}`} aria-labelledby={hid} className="f12-sp-grp">
              <div className="f12-gh">
                <h2 className="f12-h2" id={hid}>{g.ad}</h2>
                {sayi && <span className="f12-meta"><span className="f12-num">{tr(sayi.n)}</span> spot · <span className="f12-num">{tr(sayi.o)}</span> öğrenildi</span>}
              </div>
              <div className="f12-panel f12-list">
                {g.spotlar.map((s) => (
                  <SpotRow key={s.id} s={s} d={dersMap.get(s.ders)} sinav={sinav} ogrenildi={ogrenilen.has(s.id)} kartta={kartta.has(`${KART_ONEK}${s.id}`)}
                    vurgulu={vurgu === s.id} onOgren={ogren} onKart={kartaEkle} />
                ))}
              </div>
            </section>
          );
        })}

        {veri && liste.length === 0 && (
          <div className="f12-panel f12-empty">
            <b>Bu süzgeçle spot yok.</b>
            {suzgecVar && <button type="button" className="f12-btn sm" onClick={temizle}>Süzgeçleri temizle</button>}
          </div>
        )}
        {liste.length > limit && <div ref={bekciRef} className="f12-sp-more" aria-hidden><span className="f12-skel" /></div>}
        {veri && liste.length > SAYFA && liste.length <= limit && (
          <p className="f12-meta f12-sp-end">{tr(liste.length)} spotun hepsi gösterildi</p>
        )}
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Tek satır
// ---------------------------------------------------------------------------
const paylas = async (s: Spot) => {
  const url = `${location.origin}/spotlar?id=${encodeURIComponent(s.id)}`;
  const nav = navigator as Navigator & { share?: (d: ShareData) => Promise<void> };
  if (nav.share) {
    try {
      await nav.share({ title: s.baslik, text: `Sınav spotu: ${s.baslik}`, url });
      return;
    } catch (e) {
      if ((e as Error)?.name === 'AbortError') return;
    }
  }
  try {
    await navigator.clipboard.writeText(url);
    toast.show('success', 'Bağlantı kopyalandı', s.baslik);
  } catch {
    toast.show('error', 'Bağlantı kopyalanamadı', url);
  }
};

interface RowProps {
  s: Spot;
  d?: Ders;
  sinav: boolean;
  ogrenildi: boolean;
  kartta: boolean;
  vurgulu: boolean;
  onOgren: (id: string) => void;
  onKart: (s: Spot) => void;
}

const SpotRowBase: React.FC<RowProps> = ({ s, d, sinav, ogrenildi, kartta, vurgulu, onOgren, onKart }) => {
  const [acik, setAcik] = useState(false);
  const [cevap, setCevap] = useState(false);
  useEffect(() => { setCevap(false); }, [sinav]);

  const uyari = uyariMi(s);
  const kat = KAT[s.kategori];
  const gizli = sinav && !cevap;
  const tablo = s.karsilastir && s.karsilastir.basliklar?.length > 0 ? s.karsilastir : null;
  const govdeId = `f12-sp-b-${s.id}`;
  const satir = s.kaynak?.find((k) => k.satir)?.satir;

  return (
    <article id={`f12-sp-${s.id}`} className={`f12-sp-row${ogrenildi ? ' is-done' : ''}${vurgulu ? ' is-flash' : ''}`} aria-labelledby={`f12-sp-t-${s.id}`}>
      <span className={`f12-badge ${uyari ? 'bad' : 'warn'}`}>{uyari ? 'Kritik uyarı' : 'Sınav spotu'}</span>
      <div className="f12-sp-txt">
        <h3 className="f12-sp-t" id={`f12-sp-t-${s.id}`}>{s.baslik}</h3>
        {gizli ? (
          <>
            <p>{s.soru ? <Zengin metin={s.soru} /> : 'Bu spotu hatırlıyor musun?'}</p>
            <div>
              <button type="button" className="f12-btn sm" aria-expanded={false} aria-controls={govdeId} onClick={() => setCevap(true)}>
                <Eye aria-hidden /> Cevabı göster
              </button>
            </div>
          </>
        ) : (
          <p id={govdeId}><Zengin metin={s.spot} /></p>
        )}
        <span className="f12-meta f12-sp-src">
          {kat?.kisa} · {ONEM_AD[s.onem]}
          {d ? <> · Konu {d.no} — {d.baslik}</> : null}
          {satir ? <> · satır <span className="f12-num">{satir}</span></> : null}
          {ogrenildi ? <> · <span className="f12-sp-ok">Öğrenildi</span></> : null}
        </span>
        {acik && !gizli && (
          <div className="f12-sp-more-b" id={`${govdeId}-x`}>
            {s.soru && s.cevap && (
              <dl className="f12-sp-qa">
                <dt>Soru</dt><dd><Zengin metin={s.soru} /></dd>
                <dt>Cevap</dt><dd><Zengin metin={s.cevap} /></dd>
              </dl>
            )}
            {!!s.maddeler?.length && <ul className="f12-sp-ul">{s.maddeler.map((m, i) => <li key={i}><Zengin metin={m} /></li>)}</ul>}
            {tablo && (
              <div className="f12-sp-tw" tabIndex={0} role="region" aria-label={`${s.baslik} karşılaştırma tablosu`}>
                <table className="f12-sp-table">
                  <thead>
                    <tr><th scope="col"><span className="f12-sr">Ölçüt</span></th>{tablo.basliklar.map((b, i) => <th key={i} scope="col">{b}</th>)}</tr>
                  </thead>
                  <tbody>
                    {tablo.satirlar.map((r, i) => (
                      <tr key={i}><th scope="row">{r[0]}</th>{r.slice(1).map((c, j) => <td key={j}><Zengin metin={c} /></td>)}</tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            {s.tuzak && (
              <p className="f12-sp-trap" role="note"><AlertTriangle aria-hidden className="f12-ico" /><span><b>Tuzak:</b> <Zengin metin={s.tuzak} /></span></p>
            )}
            {!!s.kaynak?.length && (
              <div className="f12-sp-quote">
                <span className="f12-label">Ders notundan</span>
                {s.kaynak.map((k, i) => (
                  <blockquote key={i}>“{k.alinti}”{k.satir ? <cite className="f12-meta"> · satır {k.satir}</cite> : null}</blockquote>
                ))}
              </div>
            )}
            <div>
              <button type="button" className="f12-btn sm ghost" onClick={() => void paylas(s)}><Share2 aria-hidden /> Paylaş</button>
            </div>
          </div>
        )}
      </div>
      <div className="f12-sp-act">
        <button type="button" className={`f12-btn icon sm ghost${kartta ? ' is-on' : ''}`} aria-pressed={kartta} onClick={() => onKart(s)}
          aria-label={kartta ? 'Kartlardan çıkar' : 'Karta ekle'} title={kartta ? 'Kartlardan çıkar' : 'Karta ekle'}>
          {kartta ? <CopyCheck aria-hidden /> : <CopyPlus aria-hidden />}
        </button>
        <button type="button" className={`f12-btn icon sm ghost f12-learn${ogrenildi ? ' is-on' : ''}`} aria-pressed={ogrenildi} onClick={() => onOgren(s.id)}
          aria-label="Öğrendim" title={ogrenildi ? 'Öğrenildi — geri al' : 'Öğrendim'}>
          <Check aria-hidden strokeWidth={ogrenildi ? 3 : 1.8} />
        </button>
        {!gizli && (
          <button type="button" className="f12-btn icon sm ghost" aria-expanded={acik} aria-controls={`${govdeId}-x`} onClick={() => setAcik((v) => !v)}
            aria-label={acik ? 'Ayrıntıyı gizle' : 'Ayrıntı'} title="Ayrıntı">
            <ChevronDown aria-hidden className={`f12-chev${acik ? ' is-open' : ''}`} />
          </button>
        )}
      </div>
    </article>
  );
};

const SpotRow = React.memo(SpotRowBase);
