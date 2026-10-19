import React, { useCallback, useDeferredValue, useEffect, useMemo, useRef, useState } from 'react';
import {
  Check, ChevronDown, ChevronLeft, ChevronRight, ChevronsDownUp, ChevronsUpDown, Clock, Download, Eye, EyeOff, HelpCircle,
  Headphones, Info, Keyboard, ListFilter, Search, Star, X,
} from 'lucide-react';
import { Sheet } from '../ui/Sheet';
import { kucuk, azHareket } from './spotsShared';
import { OnemMadde, Metin, type Sekme } from './onem/OnemMadde';
import {
  ADAY, BANTLAR, HEPSI, ONEM_SON_KEY, TERCIH_KEY, TUR_AD, bantOf, dersAdi, dersVar, dersYukle, dizinYukle, ilkSayfa, ogrenildiAyarla,
  tercihOku, tercihYaz, useOgrenilen, type Aday, type Ders, type Dizin, type DizinDers, type Madde, type Tur,
} from './onem/onemVeri';
import type { EkranKapsami } from './onem/OnemPdfPenceresi';
import { asistanDersVar, asistanDersleri } from './asistan/asistanVeri';
import { cozucuDizinYukle } from './cozucu/cozucuVeri';
import { cozucuyaGit } from './spotsYol';
import { bransTanim, type Brans, type BransTanim } from './brans';
import { getAsistanSureGruplari, dk } from './sure/spotsSureVeri';
import { SpotsSureDiyalog } from './sure/SpotsSureDiyalog';
import { bittiMi, useKonuSayaci, useTakip } from '../../services/calismaTakip';
import { KonuDugmeleri, KonuSureEtiketi } from '../takip/KonuTakip';
import { onemAsistanBasaAl } from '../takip/basaAl';
import '../../styles/onem-listesi.css';
import CihazdaIsaret from '../cevrimdisi/CihazdaIsaret';

const OnemPdfPenceresi = React.lazy(() => import('./onem/OnemPdfPenceresi'));
const PatolojiAsistan = React.lazy(() => import('./asistan/PatolojiAsistan'));

/**
 * Sınav için en önemliler (100 puan, 10'ar puanlık partlar) — branş geneli (patoloji, enfeksiyon, üroloji). Kaynak: branşın Kurul 1
 * ders PDF'leri. Sınav adayları, sınav kuralı ve sesli asistan yalnız verisi olan branşta (patoloji) görünür.
 *
 * Yerleşim (kap genişliğine göre, @container):
 *  - Geniş: solda yapışkan ders gezgini (ilerleme + puan dağılımı), sağda içerik.
 *  - Dar: gezgin araç çubuğundaki ders düğmesinden alttan açılan sayfa.
 * İçerik: ders başlık kartı (önceki/sonraki ders, tıklanabilir puan çubuğu, öğrenilen ilerlemesi) → yapışkan araç çubuğu
 * (ara, süzgeç, tekrar modu, tümünü aç/kapat, part atlama çipleri) → "Sınavda çıkabilecek" kutusu → partlar.
 * Etkileşim: öğrendim işareti (profille eşitlenir), sekmeli ayrıntı, şık seçerek soru çözme, tekrar modunda kalın
 * terimleri gizleme, klavye (j/k gez · o aç · x öğrendim · t tekrar · / ara · [ ] ders).
 */

type OgrSuz = 'hepsi' | 'gizle' | 'yalniz';
interface Tercih { gizle: boolean; kuralAcik: boolean; siralama: 'puan' | 'slayt'; ogr: OgrSuz }
const TERCIH0: Tercih = { gizle: false, kuralAcik: true, siralama: 'puan', ogr: 'hepsi' };

const urlOku = (k: string) => { try { return new URLSearchParams(location.search).get(k); } catch { return null; } };
const urlYaz = (p: Record<string, string | null>) => {
  try {
    const u = new URL(location.href);
    for (const [k, v] of Object.entries(p)) { if (v) u.searchParams.set(k, v); else u.searchParams.delete(k); }
    history.replaceState(history.state, '', u.pathname + u.search + u.hash);
  } catch { /* yok */ }
};
const kodOfId = (id: string) => id.slice(0, id.lastIndexOf('-'));

/** Puan dağılımı çubuğu (dizin bant sayılarından); tıklanabilir sürümü süzgeç olarak çalışır */
const BantCubugu: React.FC<{ bant?: Record<string, number>; secili?: Set<number>; onSec?: (b: number) => void; ince?: boolean }> = ({ bant, secili, onSec, ince }) => {
  const top = Object.values(bant || {}).reduce((s, n) => s + n, 0) || 1;
  return (
    <div className={`on-bc${ince ? ' is-ince' : ''}`} role={onSec ? 'group' : undefined} aria-label={onSec ? 'Puan partına göre süz' : undefined} aria-hidden={onSec ? undefined : true}>
      {BANTLAR.map((B) => {
        const n = bant?.[String(B.b)] || 0;
        if (!n) return null;
        const st = { flexGrow: n, flexBasis: 0 } as React.CSSProperties;
        if (!onSec) return <i key={B.b} className={`b${B.b}`} style={st} />;
        const on = !!secili?.has(B.b);
        return (
          <button key={B.b} type="button" className={`b${B.b}${on ? ' is-on' : ''}${secili?.size && !on ? ' is-sonuk' : ''}`} style={st}
            onClick={() => onSec(B.b)} aria-pressed={on} title={`${B.ad} · ${B.not}: ${n} madde`}>
            <span>{n}</span>
          </button>
        );
      })}
      {!onSec && <span className="sr-only">{Math.round(top)}</span>}
    </div>
  );
};

/** Ders gezgini: özel görünümler + 33 ders (ilerleme, puan dağılımı); geniş ekranda raylı, dar ekranda sayfada */
const DersGezgini: React.FC<{ dizin: Dizin; kod: string; ogrSay: Record<string, number>; onSec: (k: string) => void; sayfada?: boolean; bt: BransTanim; aday: boolean; sureHaritasi?: Map<string, number> }> = ({ dizin, kod, ogrSay, onSec, sayfada, bt, aday, sureHaritasi }) => {
  const [q, setQ] = useState('');
  const t = kucuk(q.trim());
  const dersler = t ? dizin.dersler.filter((d) => kucuk(`${d.no} ${d.baslik}`).includes(t)) : dizin.dersler;
  const aktifRef = useRef<HTMLButtonElement>(null);
  // etkin ders görünsün: yalnız en yakın kayan kap kaydırılır (scrollIntoView pencereyi de kaydırırdı)
  useEffect(() => {
    const el = aktifRef.current; if (!el) return;
    let kap = el.parentElement;
    while (kap && !/(auto|scroll)/.test(getComputedStyle(kap).overflowY)) kap = kap.parentElement;
    if (!kap || kap === document.documentElement || kap === document.body) return;
    const r = el.getBoundingClientRect(), k = kap.getBoundingClientRect();
    if (r.top < k.top || r.bottom > k.bottom) kap.scrollTop += r.top - k.top - k.height / 2 + r.height / 2;
  }, []);
  const toplamOgr = dizin.dersler.reduce((s, d) => s + (ogrSay[d.kod] || 0), 0);
  const toplam = dizin.dersler.reduce((s, d) => s + d.madde, 0);
  const takip = useTakip();
  return (
    <nav className={`on-gez${sayfada ? ' is-sayfa' : ''}`} aria-label="Dersler">
      <div className="on-gez-ara">
        <Search aria-hidden />
        <input type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Ders ara" aria-label="Ders ara" />
      </div>
      <div className="on-gez-l">
        {!t && (
          <>
            {aday && (
              <button type="button" className={`on-gez-ozel is-aday${kod === ADAY ? ' is-on' : ''}`} onClick={() => onSec(ADAY)} aria-current={kod === ADAY ? 'page' : undefined}>
                <Star aria-hidden /><span><b>Sınav adayları</b><small>Her dersten çıkabilecek sorular</small></span>
              </button>
            )}
            <button type="button" className={`on-gez-ozel${kod === HEPSI ? ' is-on' : ''}`} onClick={() => onSec(HEPSI)} aria-current={kod === HEPSI ? 'page' : undefined}>
              <span className="on-gez-hepsi" aria-hidden>90+</span><span><b>{bt.hepsi}</b><small>{toplamOgr}/{toplam} öğrenildi</small></span>
            </button>
            <div className="on-gez-ayrac">{dizin.dersler.length} ders</div>
          </>
        )}
        {dersler.map((d) => {
          const o = ogrSay[d.kod] || 0;
          const on = kod === d.kod;
          const asistanSure = sureHaritasi?.get(d.kod);
          const tk = takip.k[`onem:${bt.id}/${d.kod}`];
          const bitti = bittiMi(tk, o >= d.madde);
          return (
            <button key={d.kod} ref={on ? aktifRef : undefined} type="button" className={`on-gez-d${on ? ' is-on' : ''}${bitti ? ' is-tam' : ''}`}
              onClick={() => onSec(d.kod)} aria-current={on ? 'page' : undefined}>
              <span className="on-gez-no">{bitti ? <Check aria-label="bitti" /> : d.no}</span>
              <span className="on-gez-t">
                <b>{d.baslik}</b>
                <span className="on-gez-m">
                  <BantCubugu bant={d.bant} ince />
                  <small>{o ? `${o}/${d.madde}` : `${d.madde} madde`}{asistanSure ? ` · ~${dk(asistanSure)} dk` : ''}</small>
                </span>
              </span>
            </button>
          );
        })}
        {t && !dersler.length && <p className="on-bos is-kucuk">“{q}” ile eşleşen ders yok.</p>}
      </div>
    </nav>
  );
};

/** "Sınavda çıkabilecek" kutusu: sıralı adaylar; dokununca maddeye gider */
const AdayKutusu: React.FC<{ d: Ders; baslikli?: boolean; ogr: Set<string>; onGit: (kod: string, id: string) => void; gizle: boolean }> = ({ d, baslikli, ogr, onGit, gizle }) => {
  const ns = d.soruSayisi || 1;
  const ad = (d.sinavAdaylari || []).map((a) => ({ a, m: d.maddeler.find((x) => x.id === a.id) })).filter((x): x is { a: Aday; m: Madde } => !!x.m).sort((x, y) => x.a.sira - y.a.sira);
  if (!ad.length) return null;
  return (
    <section className="on-adaylar" aria-label={`${dersAdi(d)} sınav adayları`}>
      <h3>
        <Star aria-hidden />
        {baslikli ? <button type="button" className="on-adaylar-ders" onClick={() => onGit(d.kod, '')}>{dersAdi(d)}</button> : <span>Sınavda çıkabilecek</span>}
        <em>bu slayttan {ns} soru</em>
      </h3>
      <ol>
        {ad.map(({ a, m }) => (
          <li key={a.id} className={`${a.sira <= ns ? 'is-en' : ''}${ogr.has(m.id) ? ' is-ogr' : ''}`}>
            <button type="button" onClick={() => onGit(d.kod, m.id)}>
              <span className="on-aday-no">{a.sira}</span>
              <span className="on-aday-t">
                <span className="on-aday-b"><Metin key={gizle ? 'g' : 'a'} metin={m.bilgi} gizle={gizle} /></span>
                <small>{a.sira <= ns ? <b>En olası soru · </b> : null}{a.gerekce}</small>
              </span>
              <span className="on-aday-p">{ogr.has(m.id) ? <Check aria-label="öğrenildi" /> : m.puan}</span>
            </button>
          </li>
        ))}
      </ol>
    </section>
  );
};

const KISAYOLLAR: [string, string][] = [['j / k', 'Sonraki / önceki madde'], ['o', 'Ayrıntıyı aç/kapat'], ['x', 'Öğrendim'], ['t', 'Tekrar modu'], ['/', 'Ara'], ['[ / ]', 'Önceki / sonraki ders'], ['Esc', 'Seçimi bırak']];

export const OnemListesi: React.FC<{ brans?: Brans }> = ({ brans = 'patoloji' }) => {
  const bt = bransTanim(brans);
  const DERS_KEY = brans === 'patoloji' ? 'medsoru_onem_ders' : `medsoru_onem_ders_${brans}`;
  const [dizin, setDizin] = useState<Dizin | null>(null);
  const [yuklu, setYuklu] = useState<Record<string, Ders>>({});
  const [hata, setHata] = useState(false);
  const [kod, setKod] = useState<string>(() => urlOku('ders') || (() => { try { return localStorage.getItem(DERS_KEY) || ''; } catch { return ''; } })());
  const [q, setQ] = useState('');
  const dq = useDeferredValue(q);
  const [bantlar, setBantlar] = useState<Set<number>>(() => new Set());
  const [turlar, setTurlar] = useState<Set<Tur>>(() => new Set());
  const [yalnizSinav, setYalnizSinav] = useState(false);
  const [katS, setKatS] = useState<'' | 'prognoz' | 'tedavi'>('');
  const [yalnizCikmis, setYalnizCikmis] = useState(false);
  const [tercih, setTercih0] = useState<Tercih>(() => tercihOku(TERCIH_KEY, TERCIH0));
  const setTercih = (p: Partial<Tercih>) => setTercih0((t) => { const n = { ...t, ...p }; tercihYaz(TERCIH_KEY, n); return n; });
  const [acik, setAcik] = useState<Map<string, Sekme>>(() => new Map());
  const [odak, setOdak] = useState<string | null>(null);
  const [suzgecAcik, setSuzgecAcik] = useState(false);
  const [gezAcik, setGezAcik] = useState(false);
  const [pdfAcik, setPdfAcik] = useState(false);
  const [asistan, setAsistan] = useState<string | null>(() => (urlOku('asistan') ? urlOku('ders') || null : null));
  const [sureAcik, setSureAcik] = useState(() => location.hash === '#sureler');
  const [kisayolAcik, setKisayolAcik] = useState(false);
  const [aktifPart, setAktifPart] = useState<number | null>(null);
  const [ozetAcik, setOzetAcik] = useState(false);
  const aramaRef = useRef<HTMLInputElement>(null);
  const hedefRef = useRef<string | null>(urlOku('m'));
  const ogr = useOgrenilen();
  const cokDers = kod === HEPSI || kod === ADAY;
  const asistanSureGruplari = useMemo(() => getAsistanSureGruplari(), []);
  const asistanSureHaritasi = useMemo(() => {
    const m = new Map<string, number>();
    asistanSureGruplari.forEach((g) => g.dersler.forEach((d) => m.set(d.kod, d.sure)));
    return m;
  }, [asistanSureGruplari]);

  useEffect(() => {
    const f = () => {
      if (location.hash === '#sureler') setSureAcik(true);
      const asParam = urlOku('asistan');
      const dParam = urlOku('ders');
      if (asParam && dParam) {
        setKod(dParam);
        setAsistan(dParam);
      } else if (!asParam && asistan) {
        setAsistan(null);
      }
    };
    window.addEventListener('popstate', f);
    return () => window.removeEventListener('popstate', f);
  }, [asistan]);

  useEffect(() => {
    let canli = true;
    dizinYukle(brans).then((d) => canli && setDizin(d)).catch(() => canli && setHata(true));
    return () => { canli = false; };
  }, [brans]);
  useEffect(() => {
    if (!dizin) return;
    if (!kod || (!cokDers && !dizin.dersler.some((d) => d.kod === kod)) || (kod === ADAY && !bt.sinavKurali)) setKod(dizin.dersler[0]?.kod || HEPSI);
  }, [dizin, kod, cokDers, bt.sinavKurali]);
  useEffect(() => {
    if (!kod) return;
    try {
      localStorage.setItem(DERS_KEY, kod);
      const d = dizin?.dersler.find((x) => x.kod === kod);
      if (d) localStorage.setItem(ONEM_SON_KEY, JSON.stringify({ brans, kod, baslik: d.baslik, no: d.no }));
    } catch { /* özel pencere */ }
    urlYaz({ ders: kod });
  }, [kod, dizin]); // eslint-disable-line react-hooks/exhaustive-deps
  // seçilen ders(ler)in dosyası; çok dersli görünümler bütün dersleri paralel indirir
  useEffect(() => {
    if (!dizin || !kod) return;
    const gerek = (cokDers ? dizin.dersler.map((d) => d.kod) : [kod]).filter((k) => !yuklu[k] && dersVar(k, brans));
    if (!gerek.length) return;
    let canli = true;
    Promise.all(gerek.map((k) => dersYukle(k, brans).then((d) => [k, d] as const)))
      .then((r) => { if (canli) setYuklu((y) => ({ ...y, ...Object.fromEntries(r) })); })
      .catch(() => canli && setHata(true));
    return () => { canli = false; };
  }, [dizin, kod, cokDers, yuklu, brans]);

  const ders = !cokDers ? yuklu[kod] || null : null;
  const dizinDers: DizinDers | undefined = dizin?.dersler.find((d) => d.kod === kod);
  useKonuSayaci('onem', !asistan && dizinDers ? `${brans}/${dizinDers.kod}` : null);
  const dersSira = dizin ? dizin.dersler.findIndex((d) => d.kod === kod) : -1;
  const kaynak = useMemo(
    () => (!dizin ? [] : cokDers ? dizin.dersler.map((d) => yuklu[d.kod]).filter(Boolean) : ders ? [ders] : []) as Ders[],
    [dizin, cokDers, ders, yuklu],
  );
  const hazir = !!dizin && (cokDers ? kaynak.length === dizin.dersler.length : !!ders);
  const terimler = useMemo(() => kucuk(dq.trim()).split(/\s+/).filter((x) => x.length > 1), [dq]);
  const varsayilan90 = kod === HEPSI && !bantlar.size && !terimler.length;
  const liste = useMemo(() => {
    const out: { m: Madde; d: Ders }[] = [];
    for (const d of kaynak) for (const m of d.maddeler) {
      if (bantlar.size && !bantlar.has(bantOf(m.puan))) continue;
      if (varsayilan90 && m.puan < 90) continue;
      if (turlar.size && !turlar.has(m.tur)) continue;
      if (yalnizSinav && m.sinavUygun === false) continue;
      if (katS && m.kategori !== katS) continue;
      if (yalnizCikmis && !(m.cikmis || []).length) continue;
      if (tercih.ogr === 'gizle' && ogr.has(m.id)) continue;
      if (tercih.ogr === 'yalniz' && !ogr.has(m.id)) continue;
      if (terimler.length) {
        const h = kucuk(`${m.baslik} ${m.bilgi} ${(m.alt || []).join(' ')} ${m.detay}`);
        if (!terimler.every((x) => h.includes(x))) continue;
      }
      out.push({ m, d });
    }
    return tercih.siralama === 'slayt' && !cokDers
      ? out.sort((a, b) => ilkSayfa(a.m) - ilkSayfa(b.m) || b.m.puan - a.m.puan)
      : out.sort((a, b) => b.m.puan - a.m.puan);
  }, [kaynak, bantlar, varsayilan90, turlar, yalnizSinav, katS, yalnizCikmis, tercih.ogr, tercih.siralama, cokDers, ogr, terimler]);
  const gruplu = useMemo(() => {
    if (tercih.siralama === 'slayt' && !cokDers) return liste.length ? [{ b: 0, ad: 'Slayt sırası', kisa: 'Slayt', not: 'PDF sayfa sırasıyla', items: liste }] : [];
    return BANTLAR.map((B) => ({ ...B, b: B.b as number, items: liste.filter((x) => bantOf(x.m.puan) === B.b) })).filter((g) => g.items.length);
  }, [liste, tercih.siralama, cokDers]);
  const sirali = useMemo(() => gruplu.flatMap((g) => g.items.map((x) => x.m.id)), [gruplu]);

  const ogrSay = useMemo(() => {
    const r: Record<string, number> = {};
    for (const id of ogr) { const k = kodOfId(id); r[k] = (r[k] || 0) + 1; }
    return r;
  }, [ogr]);
  const suzgecSayisi = bantlar.size + turlar.size + (yalnizSinav ? 1 : 0) + (katS ? 1 : 0) + (yalnizCikmis ? 1 : 0) + (tercih.ogr !== 'hepsi' ? 1 : 0);
  const temizle = () => { setBantlar(new Set()); setTurlar(new Set()); setYalnizSinav(false); setKatS(''); setYalnizCikmis(false); setTercih({ ogr: 'hepsi' }); setQ(''); };

  // ders değişince açık kartlar, odak ve arama sıfırlanır; hedef madde (aday kutusu / adres) açılıp kaydırılır
  const dersSec = useCallback((k: string, hedef?: string) => {
    hedefRef.current = hedef || null;
    setKod(k); setAcik(new Map()); setOdak(null); setGezAcik(false);
    if (!hedef) window.scrollTo({ top: 0, behavior: azHareket() ? 'auto' : 'smooth' });
  }, []);
  useEffect(() => {
    const h = hedefRef.current;
    if (!h || !hazir) return;
    if (!sirali.includes(h)) {
      // süzgeç hedefi saklıyorsa süzgeçleri bırak
      if (kaynak.some((d) => d.maddeler.some((m) => m.id === h)) && (suzgecSayisi || q || varsayilan90)) { temizle(); if (varsayilan90) setBantlar(new Set([bantOf(kaynak.flatMap((d) => d.maddeler).find((m) => m.id === h)!.puan)])); return; }
      hedefRef.current = null; return;
    }
    hedefRef.current = null;
    setAcik((a) => new Map(a).set(h, a.get(h) || 'aciklama'));
    setOdak(h);
    requestAnimationFrame(() => document.getElementById(`on-m-${h}`)?.scrollIntoView({ block: 'center', behavior: azHareket() ? 'auto' : 'smooth' }));
    urlYaz({ m: null });
  }, [hazir, sirali]); // eslint-disable-line react-hooks/exhaustive-deps

  const asistanAc = (k: string) => { setAsistan(k); urlYaz({ asistan: '1' }); };
  const onAc = useCallback((id: string, s: Sekme | null) => {
    setAcik((a) => { const n = new Map(a); if (s) n.set(id, s); else n.delete(id); return n; });
    setOdak(id);
  }, []);
  const onOgren = useCallback((id: string, v: boolean) => ogrenildiAyarla([id], v), []);
  const tumAcik = sirali.length > 0 && sirali.every((id) => acik.has(id));
  const tumunu = () => setAcik(tumAcik ? new Map() : new Map(sirali.map((id) => [id, acik.get(id) || 'aciklama'] as const)));

  // part atlama: hangi part ekranda (üst çubuğun hemen altı)
  useEffect(() => {
    const els = [...document.querySelectorAll<HTMLElement>('.on-part')];
    if (!els.length) { setAktifPart(null); return; }
    const io = new IntersectionObserver((ents) => {
      const gor = ents.filter((e) => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0];
      if (gor) setAktifPart(Number((gor.target as HTMLElement).dataset.b));
    }, { rootMargin: '-35% 0px -60% 0px' });
    els.forEach((e) => io.observe(e));
    return () => io.disconnect();
  }, [gruplu]);
  const partaGit = (b: number) => document.getElementById(`on-part-${b}`)?.scrollIntoView({ block: 'start', behavior: azHareket() ? 'auto' : 'smooth' });

  // klavye
  const durum = useRef({ sirali, odak, acik, kod, dizin, ogr });
  durum.current = { sirali, odak, acik, kod, dizin, ogr };
  useEffect(() => {
    const f = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      const t = e.target as HTMLElement;
      if (t?.closest?.('input,textarea,select,[contenteditable="true"]') || document.querySelector('.sh-sheet-root, [role="dialog"][aria-modal="true"]')) return;
      const s = durum.current;
      const git = (yon: 1 | -1) => {
        if (!s.sirali.length) return;
        const i = s.odak ? s.sirali.indexOf(s.odak) : -1;
        const n = s.sirali[Math.max(0, Math.min(s.sirali.length - 1, i < 0 ? 0 : i + yon))];
        setOdak(n);
        document.getElementById(`on-m-${n}`)?.scrollIntoView({ block: 'center', behavior: azHareket() ? 'auto' : 'smooth' });
      };
      const dersKaydir = (yon: 1 | -1) => {
        if (!s.dizin) return;
        const i = s.dizin.dersler.findIndex((d) => d.kod === s.kod);
        const n = s.dizin.dersler[i + yon];
        if (n) dersSec(n.kod);
      };
      switch (e.key) {
        case 'j': git(1); break;
        case 'k': git(-1); break;
        case 'o': case 'Enter':
          if (!s.odak || (e.key === 'Enter' && t?.closest?.('button,a'))) return;
          onAc(s.odak, s.acik.has(s.odak) ? null : 'aciklama'); break;
        case 'x': if (s.odak) ogrenildiAyarla([s.odak], !s.ogr.has(s.odak)); else return; break;
        case 't': setTercih0((p) => { const n = { ...p, gizle: !p.gizle }; tercihYaz(TERCIH_KEY, n); return n; }); break;
        case '/': aramaRef.current?.focus(); break;
        case '[': dersKaydir(-1); break;
        case ']': dersKaydir(1); break;
        case '?': setKisayolAcik((v) => !v); break;
        case 'Escape': setOdak(null); setKisayolAcik(false); return;
        default: return;
      }
      e.preventDefault();
    };
    window.addEventListener('keydown', f);
    return () => window.removeEventListener('keydown', f);
  }, [dersSec, onAc]);

  const ekranKapsami: EkranKapsami | null = useMemo(() => {
    if (!dizin) return null;
    const ilgili = suzgecSayisi > 0 || terimler.length > 0 || varsayilan90 || kod === ADAY;
    if (!ilgili) return null;
    const ids = new Set(liste.map((x) => x.m.id));
    const adayIds = new Set(kaynak.flatMap((d) => (d.sinavAdaylari || []).map((a) => a.id)));
    const parca: string[] = [];
    if (kod === ADAY) parca.push('sınav adayları');
    if (varsayilan90) parca.push('90–100');
    if (bantlar.size) parca.push(BANTLAR.filter((B) => bantlar.has(B.b)).map((B) => B.ad).join(', '));
    if (turlar.size) parca.push([...turlar].map((t) => TUR_AD[t]).join(', '));
    if (yalnizSinav) parca.push('yalnız sınava uygun');
    if (katS) parca.push(katS === 'prognoz' ? 'prognoz' : 'tedavi');
    if (yalnizCikmis) parca.push('çıkmışlı');
    if (tercih.ogr === 'gizle') parca.push('öğrenilenler hariç');
    if (tercih.ogr === 'yalniz') parca.push('yalnız öğrenilenler');
    if (terimler.length) parca.push(`“${dq.trim()}”`);
    return {
      ad: `${cokDers ? (kod === ADAY ? 'Sınav adayları' : bt.hepsi) : dersAdi(dizinDers || { no: 0, baslik: '' })} · ${parca.join(' · ')}`,
      kodlar: [...new Set(kod === ADAY ? kaynak.map((d) => d.kod) : liste.map((x) => x.d.kod))],
      uyar: (_d, m) => (kod === ADAY ? adayIds.has(m.id) : ids.has(m.id)),
    };
  }, [dizin, suzgecSayisi, terimler, varsayilan90, kod, liste, kaynak, bantlar, turlar, yalnizSinav, katS, yalnizCikmis, tercih.ogr, dq, cokDers, dizinDers, bt.hepsi]);

  if (hata) return <div className="on-page"><p className="on-bos">Önem listesi yüklenemedi. Bağlantını kontrol edip sayfayı yenile.</p></div>;
  if (!dizin) return <div className="on-page"><div className="on-iskelet" aria-busy="true"><i /><i /><i /><i /></div></div>;
  if (!dizin.dersler.length) return <div className="on-page"><p className="on-bos">{bt.ad} önem listesi hazırlanıyor.</p></div>;

  const toplam = dizin.dersler.reduce((s, d) => s + d.madde, 0);
  const toplamOgr = dizin.dersler.reduce((s, d) => s + (ogrSay[d.kod] || 0), 0);
  const asistanVar = bt.asistan && asistanDersleri(brans).length > 0;
  const onceki = dersSira > 0 ? dizin.dersler[dersSira - 1] : null;
  const sonraki = dersSira >= 0 && dersSira < dizin.dersler.length - 1 ? dizin.dersler[dersSira + 1] : null;
  const dersOgr = dizinDers ? ogrSay[dizinDers.kod] || 0 : 0;
  const tglBant = (b: number) => setBantlar((s) => { const n = new Set(s); n.has(b) ? n.delete(b) : n.add(b); return n; });
  const dersCikmis = ders ? new Set(ders.maddeler.flatMap((m) => m.cikmis || []).filter((id) => ders.cikmis?.[id])).size : 0;
  const dersAday = ders?.sinavAdaylari?.length || 0;
  const gorunenOgr = liste.filter((x) => ogr.has(x.m.id)).length;
  const gorunurOgrenAyarla = (v: boolean) => ogrenildiAyarla(liste.map((x) => x.m.id), v);

  const aktifCipler: { ad: string; kaldir: () => void }[] = [
    ...[...bantlar].sort((a, b) => b - a).map((b) => ({ ad: BANTLAR.find((B) => B.b === b)!.ad, kaldir: () => tglBant(b) })),
    ...[...turlar].map((t) => ({ ad: TUR_AD[t], kaldir: () => setTurlar((s) => { const n = new Set(s); n.delete(t); return n; }) })),
    ...(yalnizSinav ? [{ ad: 'Sınava uygun', kaldir: () => setYalnizSinav(false) }] : []),
    ...(katS ? [{ ad: katS === 'prognoz' ? 'Prognoz' : 'Tedavi', kaldir: () => setKatS('') }] : []),
    ...(yalnizCikmis ? [{ ad: 'Çıkmışlı', kaldir: () => setYalnizCikmis(false) }] : []),
    ...(tercih.ogr !== 'hepsi' ? [{ ad: tercih.ogr === 'gizle' ? 'Öğrenilenler gizli' : 'Yalnız öğrenilenler', kaldir: () => setTercih({ ogr: 'hepsi' }) }] : []),
  ];

  const baslikAdi = kod === ADAY ? 'Sınav adayları' : kod === HEPSI ? bt.hepsi : dizinDers ? dizinDers.baslik : '';
  // bu dersin sesli soru çözücüsü (setlere bölünmüşse ilk set) → /soru-cozucu
  const cozucuyuAc = (k: string) => {
    cozucuDizinYukle(brans).then((c) => {
      const hedef = c.dersler.find((x) => x.kod === k) || c.dersler.find((x) => x.kod.startsWith(`${k}-`));
      cozucuyaGit({ brans, ders: hedef?.kod, coz: hedef ? '1' : null });
    }).catch(() => {});
  };

  return (
    <div className="on-page">
      <div className="on-sayfa-bas">
        <div className="on-sayfa-t">
          <h2>{bt.ad} · Sınav için en önemliler</h2>
          <p>{dizin.dersler.length} ders · {toplam} madde · 100 puan, 10'ar puanlık partlar · her madde ders PDF'inden alıntılı</p>
        </div>
        <div className="on-sayfa-ilerleme" title={`${toplamOgr} / ${toplam} madde öğrenildi`}>
          <span><b>{toplamOgr}</b>/{toplam} öğrenildi</span>
          <div className="on-bar"><i style={{ width: `${(toplamOgr / Math.max(1, toplam)) * 100}%` }} /></div>
        </div>
        <div className="on-sayfa-btn">
          {asistanVar && cokDers && (
            <button type="button" className="on-btn is-asistan" onClick={() => asistanAc(asistanDersleri(brans).sort()[0])}>
              <Headphones aria-hidden />Sesli asistan
            </button>
          )}
          {asistanVar && (
            <button type="button" className="on-btn" onClick={() => setSureAcik(true)} title="Sesli asistanın ders ders anlatım süreleri">
              <Clock aria-hidden />Süreler
            </button>
          )}
          <button type="button" className="on-btn" onClick={() => setPdfAcik(true)} title="Önem listesini PDF olarak indir"><Download aria-hidden />PDF</button>
        </div>
      </div>

      <div className="on-yerlesim">
        <aside className="on-rail">
          <DersGezgini dizin={dizin} kod={kod} ogrSay={ogrSay} onSec={(k) => dersSec(k)} bt={bt} aday={bt.sinavKurali} sureHaritasi={asistanSureHaritasi} />
        </aside>

        <div className="on-ana">
          {/* başlık kartı */}
          <header className="on-hero">
            <div className="on-hero-ust">
              {kod === ADAY ? <span className="on-hero-no is-aday"><Star aria-hidden /></span>
                : kod === HEPSI ? <span className="on-hero-no is-hepsi">90+</span>
                : <span className="on-hero-no">{dizinDers?.no}</span>}
              <div className="on-hero-t">
                <small>{kod === ADAY ? `${dizin.dersler.length} ders · sıralı adaylar` : kod === HEPSI ? 'Tüm dersler · varsayılan 90–100 çekirdek' : `Ders ${dersSira + 1}/${dizin.dersler.length}${ders ? ` · ${ders.pdf}` : ''}`}</small>
                <h2>{baslikAdi}</h2>
              </div>
              {!cokDers && (
                <div className="on-hero-nav">
                  <button type="button" className="on-ikon" disabled={!onceki} onClick={() => onceki && dersSec(onceki.kod)} aria-label={onceki ? `Önceki ders: ${dersAdi(onceki)}` : 'Önceki ders yok'} title="Önceki ders ([)"><ChevronLeft /></button>
                  <button type="button" className="on-ikon" disabled={!sonraki} onClick={() => sonraki && dersSec(sonraki.kod)} aria-label={sonraki ? `Sonraki ders: ${dersAdi(sonraki)}` : 'Sonraki ders yok'} title="Sonraki ders (])"><ChevronRight /></button>
                </div>
              )}
            </div>
            {!cokDers && dizinDers && (
              <>
                <div className={`on-hero-stat${bt.sinavKurali ? '' : ' is-3'}`}>
                  <div><b>{dizinDers.madde}</b><span>madde</span></div>
                  {bt.sinavKurali && <div><b>{dersAday || '–'}</b><span>sınav adayı</span></div>}
                  <div><b>{ders ? dersCikmis : '–'}</b><span>çıkmış soru</span></div>
                  <div className="on-hero-ogr">
                    <b>{dersOgr}<small>/{dizinDers.madde}</small></b><span>öğrenildi</span>
                    <div className="on-bar"><i style={{ width: `${(dersOgr / Math.max(1, dizinDers.madde)) * 100}%` }} /></div>
                  </div>
                </div>
                <div className="on-hero-takip">
                  <CihazdaIsaret paket={`onem:${brans}:${dizinDers.kod}`} />
                  <KonuSureEtiketi modul="onem" konu={`${brans}/${dizinDers.kod}`} />
                  <KonuDugmeleri modul="onem" konu={`${brans}/${dizinDers.kod}`} ad={dersAdi(dizinDers)} turetilen={dersOgr >= dizinDers.madde}
                    onTekrar={() => {
                      onemAsistanBasaAl(dizinDers.kod);
                      if (bt.asistan && asistanDersVar(dizinDers.kod)) asistanAc(dizinDers.kod);
                      else window.scrollTo({ top: 0, behavior: azHareket() ? 'auto' : 'smooth' });
                    }} />
                </div>
                <div className="on-hero-bant">
                  <span>Puan dağılımı <em>dokunarak süz</em></span>
                  <BantCubugu bant={dizinDers.bant} secili={bantlar} onSec={tglBant} />
                </div>
                {ders && (
                  <div className={`on-hero-ozet${ozetAcik ? ' is-acik' : ''}`}>
                    <p className="on-hero-ozet-p"><Metin metin={ders.ozet} /></p>
                    <p className="on-hero-neden"><HelpCircle aria-hidden /><span><b>Neden önemli:</b> <Metin metin={ders.neden_onemli} /></span></p>
                    <button type="button" className="on-link on-hero-devam" onClick={() => setOzetAcik((v) => !v)} aria-expanded={ozetAcik}>
                      {ozetAcik ? 'Daha az göster' : 'Devamını oku · neden önemli'}<ChevronDown aria-hidden />
                    </button>
                  </div>
                )}
              </>
            )}
            {!cokDers && (
              <div className="on-hero-eylem">
                {bt.asistan && asistanDersVar(kod) && (
                  <button type="button" className="on-eylem is-ana" onClick={() => asistanAc(kod)}
                    title="En önemli noktaları kısaca anlatır, soru sorar, yanlışını açıklar · tam ekran">
                    <Headphones aria-hidden />Sesli asistanla çalış{asistanSureHaritasi.get(kod) ? <small>~{dk(asistanSureHaritasi.get(kod)!)} dk</small> : null}
                  </button>
                )}
                <button type="button" className="on-eylem" onClick={() => cozucuyuAc(kod)}
                  title="Çıkmış ve örnek sorular karışık · ipucu, yanlışı ele, çözümü dinle · tam ekran">
                  <Headphones aria-hidden />Soruları sesli çöz
                </button>
              </div>
            )}
            {kod === HEPSI && <p className="on-hero-not">Süzgeç seçilmediğinde yalnız 90–100 partı görünür. Diğer partlar için süzgeçten puan seç.</p>}
          </header>

          {/* sınav kuralı (hocanın açıklaması; yalnız patoloji) */}
          {bt.sinavKurali && <div className={`on-kural${tercih.kuralAcik ? ' is-acik' : ''}`}>
            <button type="button" className="on-kural-b" onClick={() => setTercih({ kuralAcik: !tercih.kuralAcik })} aria-expanded={tercih.kuralAcik}>
              <Info aria-hidden /><b>Sınav kuralı</b>
              <span>Tablo, şekil ve klinik bulgu sorulmaz · her slayttan 1 soru</span>
              <ChevronDown className="on-kural-c" aria-hidden />
            </button>
            {tercih.kuralAcik && (
              <ul>
                <li>Resim ve tablolardan soru yok; bu maddeler <span className="on-dis">üstü çizili</span> ve soluk görünür.</li>
                <li>Klinik bulgu sorulmuyor; <span className="on-kat k-prognoz">Prognoz</span> ve <span className="on-kat k-tedavi">Tedavi</span> sorulabilir.</li>
                <li>Her ders slaytından <b>1 soru</b> (Genetik, Pediatrik ve Çevresel Patoloji'den <b>2 soru</b>). <span className="on-aday is-en"><Star aria-hidden />En olası soru</span> en güçlü aday.</li>
              </ul>
            )}
          </div>}

          {/* araç çubuğu */}
          <div className="on-arac">
            <div className="on-arac-1">
              <button type="button" className="on-dersbtn" onClick={() => setGezAcik(true)} aria-haspopup="dialog">
                <span className="on-dersbtn-no">{kod === ADAY ? <Star aria-hidden /> : kod === HEPSI ? '90+' : dizinDers?.no}</span>
                <span className="on-dersbtn-t">{baslikAdi}</span>
                <ChevronDown aria-hidden />
              </button>
              <label className="on-ara">
                <Search aria-hidden />
                <input ref={aramaRef} type="search" value={q} onChange={(e) => setQ(e.target.value)} placeholder={cokDers ? 'Tüm derslerde ara' : 'Bu derste ara'} aria-label="Önem listesinde ara" />
                {q ? <button type="button" onClick={() => setQ('')} aria-label="Aramayı temizle"><X /></button> : <kbd>/</kbd>}
              </label>
              {kod !== ADAY && (
                <>
                  <button type="button" className={`on-arac-b${suzgecAcik || suzgecSayisi ? ' is-on' : ''}`} onClick={() => setSuzgecAcik((v) => !v)} aria-expanded={suzgecAcik} aria-controls="on-suzgec">
                    <ListFilter aria-hidden /><span>Süzgeç</span>{suzgecSayisi > 0 && <small>{suzgecSayisi}</small>}
                  </button>
                  <button type="button" className={`on-arac-b${tercih.gizle ? ' is-on' : ''}`} onClick={() => setTercih({ gizle: !tercih.gizle })} aria-pressed={tercih.gizle} title="Tekrar modu: kalın terimleri gizle (t)">
                    {tercih.gizle ? <EyeOff aria-hidden /> : <Eye aria-hidden />}<span>Tekrar</span>
                  </button>
                  <button type="button" className="on-arac-b is-ikon" onClick={tumunu} title={tumAcik ? 'Tümünü kapat' : 'Tümünü aç'} aria-label={tumAcik ? 'Tümünü kapat' : 'Tümünü aç'}>
                    {tumAcik ? <ChevronsDownUp aria-hidden /> : <ChevronsUpDown aria-hidden />}
                  </button>
                  <div className="on-kisayol">
                    <button type="button" className={`on-arac-b is-ikon${kisayolAcik ? ' is-on' : ''}`} onClick={() => setKisayolAcik((v) => !v)} aria-expanded={kisayolAcik} aria-label="Klavye kısayolları" title="Klavye kısayolları (?)"><Keyboard aria-hidden /></button>
                    {kisayolAcik && (
                      <div className="on-kisayol-p" role="note">
                        {KISAYOLLAR.map(([k, a]) => <div key={k}><kbd>{k}</kbd><span>{a}</span></div>)}
                      </div>
                    )}
                  </div>
                </>
              )}
            </div>
            {kod !== ADAY && gruplu.length > 0 && (
              <div className="on-arac-2">
                <div className="on-partlar" role="navigation" aria-label="Partlara git">
                  {gruplu.map((g) => (
                    <button key={g.b} type="button" className={`on-partcip b${g.b}${aktifPart === g.b ? ' is-on' : ''}`} onClick={() => partaGit(g.b)}>
                      <span>{g.b ? g.ad : 'Slayt'}</span><small>{g.items.length}</small>
                    </button>
                  ))}
                </div>
                <span className="on-gorunen">{liste.length} madde{gorunenOgr ? ` · ${gorunenOgr} öğrenildi` : ''}</span>
              </div>
            )}
          </div>

          {suzgecAcik && kod !== ADAY && (
            <div className="on-suzgec" id="on-suzgec">
              <div className="on-suz-g">
                <span className="on-suz-ad">Puan partı</span>
                <div className="on-cipler">
                  {BANTLAR.map((B) => (
                    <button key={B.b} type="button" className={`on-cip is-bant b${B.b}${bantlar.has(B.b) ? ' is-on' : ''}`} onClick={() => tglBant(B.b)} aria-pressed={bantlar.has(B.b)}>
                      {bantlar.has(B.b) && <Check className="on-cip-i" aria-hidden />}{B.ad}<small>{B.not}</small>
                    </button>
                  ))}
                </div>
              </div>
              <div className="on-suz-g">
                <span className="on-suz-ad">Bilgi türü</span>
                <div className="on-cipler">
                  {(Object.keys(TUR_AD) as Tur[]).map((t) => (
                    <button key={t} type="button" className={`on-cip is-tur t-${t}${turlar.has(t) ? ' is-on' : ''}`} aria-pressed={turlar.has(t)}
                      onClick={() => setTurlar((s) => { const n = new Set(s); n.has(t) ? n.delete(t) : n.add(t); return n; })}>
                      {turlar.has(t) && <Check className="on-cip-i" aria-hidden />}{TUR_AD[t]}
                    </button>
                  ))}
                </div>
              </div>
              <div className="on-suz-g">
                <span className="on-suz-ad">Sınav</span>
                <div className="on-cipler">
                  {bt.sinavKurali && <>
                  <button type="button" className={`on-cip is-sinav${yalnizSinav ? ' is-on' : ''}`} onClick={() => setYalnizSinav((v) => !v)} aria-pressed={yalnizSinav}>{yalnizSinav && <Check className="on-cip-i" aria-hidden />}Yalnız sınava uygun</button>
                  <button type="button" className={`on-cip is-kat k-prognoz${katS === 'prognoz' ? ' is-on' : ''}`} onClick={() => setKatS((v) => (v === 'prognoz' ? '' : 'prognoz'))} aria-pressed={katS === 'prognoz'}>{katS === 'prognoz' && <Check className="on-cip-i" aria-hidden />}Prognoz</button>
                  <button type="button" className={`on-cip is-kat k-tedavi${katS === 'tedavi' ? ' is-on' : ''}`} onClick={() => setKatS((v) => (v === 'tedavi' ? '' : 'tedavi'))} aria-pressed={katS === 'tedavi'}>{katS === 'tedavi' && <Check className="on-cip-i" aria-hidden />}Tedavi</button>
                  </>}
                  <button type="button" className={`on-cip is-cik${yalnizCikmis ? ' is-on' : ''}`} onClick={() => setYalnizCikmis((v) => !v)} aria-pressed={yalnizCikmis}>{yalnizCikmis && <Check className="on-cip-i" aria-hidden />}Çıkmış sorusu olan</button>
                </div>
              </div>
              <div className="on-suz-satir">
                <div className="on-seg" role="radiogroup" aria-label="Öğrendiklerim">
                  <span>Öğrendiklerim</span>
                  {([['hepsi', 'Göster'], ['gizle', 'Gizle'], ['yalniz', 'Yalnız onlar']] as [OgrSuz, string][]).map(([v, l]) => (
                    <button key={v} type="button" role="radio" aria-checked={tercih.ogr === v} className={tercih.ogr === v ? 'is-on' : ''} onClick={() => setTercih({ ogr: v })}>{l}</button>
                  ))}
                </div>
                {!cokDers && (
                  <div className="on-seg" role="radiogroup" aria-label="Sıralama">
                    <span>Sıralama</span>
                    {([['puan', 'Puan partları'], ['slayt', 'Slayt sırası']] as ['puan' | 'slayt', string][]).map(([v, l]) => (
                      <button key={v} type="button" role="radio" aria-checked={tercih.siralama === v} className={tercih.siralama === v ? 'is-on' : ''} onClick={() => setTercih({ siralama: v })}>{l}</button>
                    ))}
                  </div>
                )}
              </div>
              <div className="on-suz-alt">
                <button type="button" className="on-link" disabled={!suzgecSayisi && !q} onClick={temizle}>Süzgeçleri temizle</button>
                {liste.length > 0 && (
                  <button type="button" className="on-link" onClick={() => gorunurOgrenAyarla(gorunenOgr < liste.length)}>
                    {gorunenOgr < liste.length ? `Görünen ${liste.length} maddeyi öğrendim say` : 'Görünenlerin işaretini kaldır'}
                  </button>
                )}
                <button type="button" className="on-btn" onClick={() => setSuzgecAcik(false)}>Tamam</button>
              </div>
            </div>
          )}
          {!suzgecAcik && aktifCipler.length > 0 && (
            <div className="on-aktif" aria-label="Etkin süzgeçler">
              {aktifCipler.map((c) => <button key={c.ad} type="button" className="on-aktif-c" onClick={c.kaldir} aria-label={`${c.ad} süzgecini kaldır`}>{c.ad}<X aria-hidden /></button>)}
              <button type="button" className="on-link" onClick={temizle}>Temizle</button>
            </div>
          )}

          {!hazir && <div className="on-iskelet" aria-busy="true"><i /><i /><i /></div>}

          {hazir && kod === ADAY && (
            <div className="on-aday-izgara">
              {kaynak.filter((d) => !terimler.length || d.maddeler.some((m) => (d.sinavAdaylari || []).some((a) => a.id === m.id) && terimler.every((x) => kucuk(`${m.baslik} ${m.bilgi}`).includes(x))))
                .map((d) => <AdayKutusu key={d.kod} d={d} baslikli ogr={ogr} gizle={tercih.gizle} onGit={(k, id) => dersSec(k, id || undefined)} />)}
            </div>
          )}

          {hazir && ders && !terimler.length && <AdayKutusu d={ders} ogr={ogr} gizle={tercih.gizle} onGit={(_k, id) => {
            if (sirali.includes(id)) { setAcik((a) => new Map(a).set(id, a.get(id) || 'aciklama')); setOdak(id); document.getElementById(`on-m-${id}`)?.scrollIntoView({ block: 'center', behavior: azHareket() ? 'auto' : 'smooth' }); }
            else { hedefRef.current = id; temizle(); }
          }} />}

          {hazir && kod !== ADAY && gruplu.length === 0 && (
            <div className="on-bos-k">
              <p>{tercih.ogr === 'gizle' && !terimler.length && !bantlar.size ? 'Bu görünümdeki her maddeyi öğrendin.' : 'Bu süzgeçle madde yok.'}</p>
              <button type="button" className="on-btn" onClick={temizle}>Süzgeçleri temizle</button>
            </div>
          )}

          {hazir && kod !== ADAY && gruplu.map((g, i) => (
            <section key={g.b} id={`on-part-${g.b}`} data-b={g.b} className={`on-part b${g.b}`}>
              <h3 className="on-part-h">
                <span className="on-part-no">{g.b ? `Part ${i + 1}` : 'Sıra'}</span>
                <span className="on-part-ad">{g.b ? `${g.ad} puan` : g.ad}</span>
                <span className="on-part-not">{g.not}</span>
                <span className="on-part-n">{g.items.filter((x) => ogr.has(x.m.id)).length}/{g.items.length}</span>
              </h3>
              <ul className="on-list">
                {g.items.map(({ m, d }) => (
                  <OnemMadde key={m.id} m={m} d={d} gosterDers={cokDers} acik={acik.has(m.id)} sekme={acik.get(m.id) || 'aciklama'} onAc={onAc}
                    ogrenildi={ogr.has(m.id)} onOgren={onOgren} gizle={tercih.gizle} terimler={terimler} odak={odak === m.id}
                    onDers={cokDers ? (k, id) => dersSec(k, id) : undefined} />
                ))}
              </ul>
            </section>
          ))}

          {hazir && !cokDers && (
            <div className="on-son-cozucu">
              <button type="button" className="on-hero-asistan is-cozucu" onClick={() => cozucuyuAc(kod)}>
                <span className="on-hero-asistan-i"><Headphones aria-hidden /></span>
                <span>
                  <b>Bu konunun soru çözücü asistanı</b>
                  <small>Çıkmış ve örnek sorularla sesli soru çözümü · şık analizleri ve ipuçları · tam ekran</small>
                </span>
                <ChevronRight aria-hidden />
              </button>
            </div>
          )}

          {hazir && !cokDers && (onceki || sonraki) && (
            <nav className="on-dersnav" aria-label="Ders gezintisi">
              {onceki ? (
                <button type="button" onClick={() => dersSec(onceki.kod)}><ChevronLeft aria-hidden /><span><small>Önceki ders</small><b>{dersAdi(onceki)}</b></span></button>
              ) : <span />}
              {sonraki ? (
                <button type="button" className="is-sonraki" onClick={() => dersSec(sonraki.kod)}><span><small>Sonraki ders</small><b>{dersAdi(sonraki)}</b></span><ChevronRight aria-hidden /></button>
              ) : <span />}
            </nav>
          )}
        </div>
      </div>


      <Sheet open={gezAcik} onClose={() => setGezAcik(false)} title="Ders seç" subtitle={`${toplamOgr}/${toplam} madde öğrenildi`} size="full" width={520}>
        <DersGezgini dizin={dizin} kod={kod} ogrSay={ogrSay} onSec={(k) => dersSec(k)} sayfada bt={bt} aday={bt.sinavKurali} sureHaritasi={asistanSureHaritasi} />
      </Sheet>
      {sureAcik && asistanVar && (
        <SpotsSureDiyalog
          takipModul="onem"
          baslik="Sesli sınav asistanı ders süreleri"
          gruplar={asistanSureGruplari}
          onKapat={() => {
            setSureAcik(false);
            if (location.hash === '#sureler') {
              history.replaceState(history.state, '', location.pathname + location.search);
            }
          }}
          onDersAc={(b, k) => {
            if (b !== brans) {
              const u = new URL(location.href);
              u.searchParams.set('brans', b);
              u.searchParams.set('asistan', '1');
              u.searchParams.set('ders', k);
              history.pushState(history.state, '', u.pathname + u.search + u.hash);
              window.dispatchEvent(new PopStateEvent('popstate'));
            } else {
              asistanAc(k);
            }
          }}
          birimAd="ders"
          not="Süreler EMA seslendirmesine göredir. Asistan anlatımı ve soru pekiştirmelerini içerir."
        />
      )}
      {asistan && bt.asistan && (
        <React.Suspense fallback={null}>
          <PatolojiAsistan kod={asistan} onClose={() => { setAsistan(null); urlYaz({ asistan: null }); }} onDersDegis={(k) => { if (!cokDers) setKod(k); }} />
        </React.Suspense>
      )}
      {pdfAcik && (
        <React.Suspense fallback={null}>
          <OnemPdfPenceresi brans={brans} dizin={dizin} secili={!cokDers ? kod : null} ekran={ekranKapsami} onClose={() => setPdfAcik(false)} />
        </React.Suspense>
      )}
    </div>
  );
};

export default OnemListesi;
