/**
 * TBG Sınav Kampı › Sesli ders + slayt. Ders özeti (g07 anlatım cümleleri, maddeler halinde) EMA sesiyle kesintisiz okunur;
 * okunan cümlenin karşılığı olan ders PDF'i ve slaytı yanda açılır (eşleme: data/genetik_kamp/slayt.json, slayt_esle.py).
 * Kesintisizlik: sıradaki ses klibi önceden yüklenir; sıradaki farklı ders PDF'i gizli bir görüntüleyicide önceden açılır,
 * başlık o derse geçince yalnız görünürlük değişir.
 */
import React, { Suspense, lazy, useCallback, useEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react';
import { ArrowLeftRight, ChevronLeft, ChevronRight, Columns2, FileText, Maximize2, Minimize2, Minus, Pause, Play, Plus, ScrollText, SkipBack, SkipForward } from 'lucide-react';
import { createPortal } from 'react-dom';
import { shouldAvoidNativeFullscreen } from '../../utils/device';
import { getCustomApiUrl } from '../../services/api';
import slaytRaw from '../../data/genetik_kamp/slayt.json';
import kelimeRaw from '../../data/genetik_kamp/kelime.json';
import type { PdfMarks } from '../learn/pdf/PdfDocView';

const PdfDocView = lazy(() => import('../learn/pdf/PdfDocView'));

interface Klip { v: string; sure: number; zaman: [number, number][] }
interface Nokta { id: string; bolum: number; baslik: string; cumleler: string[] }
interface Ders { kod: string; bolumler: { baslik: string; neden: string }[]; noktalar: Nokta[]; klip: Record<string, Klip> }
type Yer = [string, number, number];
interface Isaret { s: number; t: PdfMarks['kind']; l: number[][]; w: number[][] }
const SLAYT = slaytRaw as unknown as { pdf: Record<string, { deck: string; sayfa: number }>; cumle: Record<string, Yer[]>; isaret?: Record<string, (Isaret | null)[]> };
const KELIME = kelimeRaw as unknown as Record<string, { v: string; c: number[][] }>;

/* ——— okunan kelime deposu: kelime değişince yalnız aktif cümle ve slayt işaret katmanı yeniden çizilir ——— */
const odak = { klip: '', c: -1, w: -1 };
const dinleyen = new Set<() => void>();
const odakAbone = (f: () => void) => { dinleyen.add(f); return () => { dinleyen.delete(f); }; };
function odakYaz(klip: string, c: number, w: number) {
  if (odak.klip === klip && odak.c === c && odak.w === w) return;
  odak.klip = klip; odak.c = c; odak.w = w;
  dinleyen.forEach((f) => f());
}
const useOdakKelime = (klip: string, c: number) => useSyncExternalStore(odakAbone, () => (odak.klip === klip && odak.c === c ? odak.w : -1));

/** Ekran metni (** silinmiş) karakterlerinin kalınlığı + /\S+/g kelimeleri (kelime zamanlarıyla birebir aynı bölme) */
function kelimeler(t: string) {
  let duz = ''; const kalin: boolean[] = []; let b = false;
  for (const p of t.split(/(\*\*)/)) { if (p === '**') { b = !b; continue; } for (const ch of p) { duz += ch; kalin.push(b); } }
  const K: { bas: number; son: number }[] = [];
  for (const m of duz.matchAll(/\S+/g)) K.push({ bas: m.index!, son: m.index! + m[0].length });
  return { duz, kalin, K };
}

/* ——— maddeleme: cümle metni aynen korunur, yalnız dizilir ———
 *  - "Örneğin / Buna karşın / Yani …" ile başlayan cümle bir öncekinin altına girer (düzey 1)
 *  - cümle içindeki "tanım; örnekler" / "giriş: ayrıntı" ayrımı alt madde olur (bir düzey içte)
 *  - "Sınavda en olası soru buradan: / Burası çok önemli:" cümleleri önemli not olarak işaretlenir */
const ALT_CUMLE = /^(Örneğin|Mesela|Buna karşın|Buna karşılık|Yani|Kısacası|Başka bir deyişle|Bu yüzden|Bu nedenle|Bu sayede|Dolayısıyla|Ayrıca|Özellikle|Sonuç olarak)(?!\p{L})/u;
const NOT = /^(Sınavda[^:]{0,40}|Burası (çok )?önemli|Dikkat( edin)?|Unutma(yın)?)\s*:\s*/u;
interface Parca { a: number; z: number; d: number }
interface Yapi { not: boolean; alt: boolean; parcalar: Parca[] }
function yapi(duz: string): Yapi {
  const notM = duz.match(NOT);
  const bas = notM ? notM[0].length : 0;
  const kes: number[] = [];
  const kelimeSay = (x: string) => (x.match(/\S+/g) || []).length;
  for (const m of duz.slice(bas).matchAll(/[;:]\s+/g)) {
    const k = bas + m.index! + m[0].length;
    const once = duz.slice(kes.length ? kes[kes.length - 1] : bas, bas + m.index!);
    if (kelimeSay(once) >= 3 && kelimeSay(duz.slice(k)) >= 3) kes.push(k);
  }
  const sinir = [0, ...kes, duz.length];
  return {
    not: !!notM, alt: ALT_CUMLE.test(duz),
    parcalar: sinir.slice(0, -1).map((a, i) => ({ a, z: sinir[i + 1], d: i === 0 ? 0 : 1 })),
  };
}

/** Bir cümleyi yapısıyla çizer; aktifse okunan kelime vurgulanır (yalnız aktif cümle kelime deposuna abone olur) */
function CumleGovde({ t, w, aktif = false }: { t: string; w: number; aktif?: boolean }) {
  const { duz, kalin, K } = useMemo(() => kelimeler(t), [t]);
  const y = useMemo(() => yapi(duz), [duz]);
  const parca = (a: number, z: number) => {
    const out: React.ReactNode[] = []; let i = a;
    while (i < z) { let j = i; while (j < z && kalin[j] === kalin[i]) j++; const s = duz.slice(i, j); out.push(kalin[i] ? <b key={i}>{s}</b> : s); i = j; }
    return out;
  };
  return (
    <>
      {y.parcalar.map((p, pi) => {
        const out: React.ReactNode[] = []; let son = p.a;
        K.forEach((k, i) => {
          if (k.bas < p.a || k.bas >= p.z) return;
          out.push(...parca(son, k.bas));
          out.push(<span key={`k${i}`} className={!aktif ? undefined : i === w ? 'gsd-k is-on' : i < w ? 'gsd-k is-gecti' : 'gsd-k'}>{parca(k.bas, Math.min(k.son, p.z))}</span>);
          son = Math.min(k.son, p.z);
        });
        out.push(...parca(son, p.z));
        return <span key={pi} className={`gsd-p gsd-d${p.d}`}>{out}</span>;
      })}
    </>
  );
}
function AktifCumle({ t, klip, c }: { t: string; klip: string; c: number }) {
  const w = useOdakKelime(klip, c);
  return <CumleGovde t={t} w={w} aktif />;
}
const cumleYapi = (t: string) => yapi(kelimeler(t).duz);

/* ——— düzen tercihleri (cihazda) ——— */
type Gorunum = 'metin' | 'ikisi' | 'pdf';
interface Duzen { gorunum: Gorunum; taraf: 'sag' | 'sol'; oran: number; yazi: number }
const DUZEN_KEY = 'medsoru_tbg_sesli_duzen';
const duzenOku = (): Duzen => {
  const v: Duzen = { gorunum: typeof window !== 'undefined' && window.innerWidth < 900 ? 'metin' : 'ikisi', taraf: 'sag', oran: 45, yazi: 1 };
  try { return { ...v, ...JSON.parse(localStorage.getItem(DUZEN_KEY) || '{}') }; } catch { return v; }
};
const YAZI = [0.9, 1, 1.15, 1.3, 1.5];

const PDF_AD: Record<string, string> = {
  g01: 'Dismorfolojide genetik terminoloji', g02: 'Kromozomal hastalıklar ve genetik danışma', g03: 'Doğumsal kadın-erkek gelişim anomalileri',
  g04: 'Ürogenital sistem tümörlerinde genetik belirteçler', g05: 'Prenatal tanı ve uygulama alanları', g06: 'Preimplantasyon genetik tanı',
};
const HIZLAR = [1, 1.15, 1.25, 1.5, 1.75, 2];

/** Okuma sırası: bölüm girişi (b-N) → bölümün adımları (a-id) */
interface Oge { klip: string; bolum: number; nokta?: Nokta }

const pdfAdresi = (k: string) => `${getCustomApiUrl() || ''}/api/lecture-pdf/deck/${encodeURIComponent(SLAYT.pdf[k].deck)}/0`;

function Zengin({ t }: { t: string }) {
  return <>{t.split(/(\*\*[^*]+\*\*)/g).map((p, i) => (p.startsWith('**') && p.endsWith('**') ? <b key={i}>{p.slice(2, -2)}</b> : <React.Fragment key={i}>{p}</React.Fragment>))}</>;
}

export default function GenetikSesliDers({ ders, adimlar }: { ders: Ders; adimlar: Nokta[] }) {
  const ogeler = useMemo(() => {
    const o: Oge[] = [];
    let son = -1;
    for (const n of adimlar) {
      if (n.bolum !== son) { if (ders.klip[`b-${n.bolum + 1}`]) o.push({ klip: `b-${n.bolum + 1}`, bolum: n.bolum }); son = n.bolum; }
      o.push({ klip: `a-${n.id}`, bolum: n.bolum, nokta: n });
    }
    return o;
  }, [adimlar, ders]);

  const [i, setI] = useState(0);
  const [cumle, setCumle] = useState(0);
  const [caliyor, setCaliyor] = useState(false);
  const [hiz, setHiz] = useState(1);
  const [pdfHata, setPdfHata] = useState<Record<string, boolean>>({});
  const [duzen, setDuzen0] = useState<Duzen>(duzenOku);
  const setDuzen = (p: Partial<Duzen>) => setDuzen0((d) => { const n = { ...d, ...p }; try { localStorage.setItem(DUZEN_KEY, JSON.stringify(n)); } catch { /* özel pencere */ } return n; });
  const kokRef = useRef<HTMLDivElement | null>(null);
  const [tam, setTam] = useState(false);
  const yerel = useRef(false); // gerçek (tarayıcı) tam ekranda mı
  const tamDegis = () => {
    const d = document as any;
    if (tam) {
      if (yerel.current && (d.fullscreenElement || d.webkitFullscreenElement)) void (d.exitFullscreen || d.webkitExitFullscreen)?.call(d)?.catch?.(() => {});
      yerel.current = false; setTam(false); return;
    }
    setTam(true);
    // sayfanın tamamı tam ekrana geçer; bileşen body'ye taşınıp (portal) her şeyin üstünü kaplar
    const el = document.documentElement as any;
    const req = el.requestFullscreen || el.webkitRequestFullscreen;
    if (el && req && !shouldAvoidNativeFullscreen()) {
      try { const r0 = req.call(el, { navigationUI: 'hide' }); yerel.current = true; r0?.catch?.(() => { yerel.current = false; }); } catch { yerel.current = false; }
    }
  };
  useEffect(() => {
    const d = document as any;
    const f = () => { if (yerel.current && !(d.fullscreenElement || d.webkitFullscreenElement)) { yerel.current = false; setTam(false); } };
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape' && tam && !yerel.current) setTam(false); };
    document.addEventListener('fullscreenchange', f); document.addEventListener('webkitfullscreenchange', f); window.addEventListener('keydown', esc);
    return () => { document.removeEventListener('fullscreenchange', f); document.removeEventListener('webkitfullscreenchange', f); window.removeEventListener('keydown', esc); };
  }, [tam]);
  useEffect(() => { // tam ekranda sayfa kaymasın
    if (!tam) return;
    const h = document.documentElement; const eski = h.style.overflow; h.style.overflow = 'hidden';
    return () => { h.style.overflow = eski; };
  }, [tam]);
  const ses = useRef<HTMLAudioElement | null>(null);
  const sonraki = useRef<{ klip: string; a: HTMLAudioElement } | null>(null);
  const metinRef = useRef<HTMLDivElement | null>(null);
  const durum = useRef({ i, caliyor, hiz });
  durum.current = { i, caliyor, hiz };

  useEffect(() => { setI(0); setCumle(0); }, [ogeler]);

  /** Bir öğenin cümle yeri (bölüm girişinde bölümün ilk adımının ilk slaytı) */
  const yer = useCallback((oi: number, ci: number): Yer | null => {
    const o = ogeler[oi];
    if (!o) return null;
    if (o.nokta) return SLAYT.cumle[o.nokta.id]?.[ci] || SLAYT.cumle[o.nokta.id]?.[0] || null;
    const n = ogeler.slice(oi + 1).find((x) => x.nokta)?.nokta;
    return n ? SLAYT.cumle[n.id]?.[0] || null : null;
  }, [ogeler]);

  const klipUrl = (id: string) => `${getCustomApiUrl() || ''}/api/patoloji-asistan/ses/${ders.kod}/${id}.mp3?v=${ders.klip[id]?.v || ''}`;

  /** Sıradaki klibi arka planda yükle */
  const onYukle = useCallback((oi: number) => {
    const o = ogeler[oi + 1];
    if (!o || !ders.klip[o.klip] || sonraki.current?.klip === o.klip) return;
    const a = new Audio(); a.preload = 'auto'; a.src = klipUrl(o.klip); a.load();
    sonraki.current = { klip: o.klip, a };
  }, [ogeler, ders]); // eslint-disable-line react-hooks/exhaustive-deps

  const oynat = useCallback((oi: number, ci = 0) => {
    const o = ogeler[oi];
    if (!o) { setCaliyor(false); return; }
    const k = ders.klip[o.klip];
    if (!k) { oynat(oi + 1); return; }
    const eski = ses.current;
    if (eski) { eski.onended = null; eski.ontimeupdate = null; eski.pause(); }
    const a = sonraki.current?.klip === o.klip ? sonraki.current.a : new Audio(klipUrl(o.klip));
    sonraki.current = null;
    ses.current = a;
    a.playbackRate = durum.current.hiz;
    if (ci > 0 && k.zaman[ci]) a.currentTime = Math.max(0, k.zaman[ci][0] - 0.05);
    setI(oi); setCumle(ci);
    const kz = KELIME[o.klip]?.v === k.v ? KELIME[o.klip].c : null;
    const izle = () => {
      const t = a.currentTime;
      let c = 0;
      for (let j = 0; j < k.zaman.length; j++) if (t >= k.zaman[j][0] - 0.1) c = j;
      const cc = o.nokta ? c : 0;
      setCumle((x) => (x === cc ? x : cc));
      let w = -1;
      const z = kz?.[cc];
      if (z) for (let j = 0; j < z.length; j++) if (t >= z[j] - 0.08) w = j;
      odakYaz(o.klip, cc, w);
    };
    a.ontimeupdate = izle;
    // timeupdate ~4 Hz; kelime için kare kare izle
    let kare = 0;
    const dongu = () => { if (ses.current !== a || a.paused) return; izle(); kare = requestAnimationFrame(dongu); };
    a.onplaying = () => { cancelAnimationFrame(kare); kare = requestAnimationFrame(dongu); };
    a.onended = () => oynat(oi + 1);
    a.play().then(() => setCaliyor(true)).catch(() => setCaliyor(false));
    onYukle(oi);
  }, [ogeler, ders, onYukle]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => () => { const a = ses.current; if (a) { a.onended = null; a.pause(); } }, []);
  useEffect(() => { if (ses.current) ses.current.playbackRate = hiz; }, [hiz]);

  const oynatDuraklat = () => {
    const a = ses.current;
    if (!a || a.ended || !a.src) { oynat(i, cumle); return; }
    if (caliyor) { a.pause(); setCaliyor(false); } else { a.play().then(() => setCaliyor(true)).catch(() => {}); }
  };
  const cumleGit = (d: number) => {
    const o = ogeler[i]; const n = o?.nokta ? o.nokta.cumleler.length : 1;
    if (cumle + d >= 0 && cumle + d < n) oynat(i, cumle + d);
    else if (d > 0) oynat(Math.min(ogeler.length - 1, i + 1));
    else if (i > 0) { const p = ogeler[i - 1]; oynat(i - 1, p.nokta ? p.nokta.cumleler.length - 1 : 0); }
  };
  const baslikGit = (d: number) => {
    let j = i + d;
    while (j > 0 && j < ogeler.length - 1 && !ogeler[j].nokta) j += d;
    oynat(Math.max(0, Math.min(ogeler.length - 1, j)));
  };

  // Okunan maddeyi metin panelinde görünür tut
  useEffect(() => {
    const el = metinRef.current?.querySelector('.gsd-c.is-on, .gsd-b.is-on');
    el?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }, [i, cumle]);

  const simdi = yer(i, cumle);
  const isr = ogeler[i]?.nokta ? SLAYT.isaret?.[ogeler[i].nokta!.id]?.[cumle] ?? null : null;
  const aktifKlip = ogeler[i]?.klip || '';
  const marks = useMemo<PdfMarks | null>(() => {
    if (!isr || !caliyor) return null;
    const ws = isr.w;
    const { K } = kelimeler(ogeler[i]?.nokta?.cumleler[cumle] || '');
    // o an konuşulan kelimenin slayttaki karşılığı (karakter aralığı eşleşmesi); karşılıksız kelimede işaret yok
    const useFocus = (): number => useSyncExternalStore(odakAbone, () => {
      if (odak.klip !== aktifKlip || odak.c !== cumle || odak.w < 0 || !K[odak.w]) return -1;
      const ch = K[odak.w].bas;
      return ws.findIndex((x) => ch >= x[0] && ch < x[1]);
    });
    return { page: isr.s, kind: isr.t, lines: isr.l, words: ws.map((x) => x.slice(2)), useFocus };
  }, [isr, caliyor, aktifKlip, cumle, i, ogeler]);
  const pdf = simdi?.[0] || 'g01';
  const sayfa = simdi?.[1] || 1;
  // Sıradaki (farklı) PDF ve onun ilk sayfası: gizli görüntüleyicide önceden açılır
  const sonrakiPdf = useMemo(() => {
    for (let j = i; j < ogeler.length; j++) {
      const n = ogeler[j].nokta;
      if (!n) continue;
      for (const y of SLAYT.cumle[n.id] || []) if (y[0] !== pdf) return { k: y[0], p: y[1] };
    }
    return null;
  }, [i, ogeler, pdf]);
  const oncekiPdf = useRef<string | null>(null);
  const [acik, setAcik] = useState<string[]>([]);
  useEffect(() => {
    // en çok 3 görüntüleyici: şimdiki, sıradaki, bir önceki (geri dönüş anında hazır)
    const L = [pdf, sonrakiPdf?.k, oncekiPdf.current].filter((x, j, a): x is string => !!x && a.indexOf(x) === j);
    setAcik(L);
    if (oncekiPdf.current !== pdf) oncekiPdf.current = pdf;
  }, [pdf, sonrakiPdf?.k]);
  const onSayfalar = useMemo(() => {
    const s = new Set<number>();
    for (let j = 1; j <= 3; j++) { const y = yer(i, cumle + j); if (y && y[0] === pdf) s.add(y[1]); }
    const o = ogeler[i + 1]?.nokta;
    if (o) for (const y of SLAYT.cumle[o.id] || []) if (y[0] === pdf) s.add(y[1]);
    return [...s];
  }, [i, cumle, pdf, ogeler, yer]);

  const toplamSn = useMemo(() => ogeler.reduce((t, o) => t + (ders.klip[o.klip]?.sure || 0), 0), [ogeler, ders]);
  const gecenSn = useMemo(() => ogeler.slice(0, i).reduce((t, o) => t + (ders.klip[o.klip]?.sure || 0), 0) + (ders.klip[ogeler[i]?.klip]?.zaman[cumle]?.[0] || 0), [ogeler, ders, i, cumle]);

  const icerik = (
    <div ref={kokRef} className={`gsd gsd-g-${duzen.gorunum} gsd-t-${duzen.taraf}${tam ? ' is-tam' : ''}`}
      style={{ ['--gsd-oran' as string]: `${duzen.oran}fr`, ['--gsd-pdf-oran' as string]: `${100 - duzen.oran}fr`, ['--gsd-yazi' as string]: String(duzen.yazi) }}>
      <div className="gsd-arac" role="toolbar" aria-label="Görünüm">
        <div className="gsd-sec" role="radiogroup" aria-label="Görünüm">
          {([['metin', 'Metin', ScrollText], ['ikisi', 'Metin + Slayt', Columns2], ['pdf', 'Slayt', FileText]] as const).map(([id, ad, Ic]) => (
            <button key={id} type="button" role="radio" aria-checked={duzen.gorunum === id} className={duzen.gorunum === id ? 'is-on' : ''} onClick={() => setDuzen({ gorunum: id })}>
              <Ic aria-hidden /><span>{ad}</span>
            </button>
          ))}
        </div>
        {duzen.gorunum === 'ikisi' && (
          <>
            <button type="button" className="tk-metin-btn gsd-taraf" onClick={() => setDuzen({ taraf: duzen.taraf === 'sag' ? 'sol' : 'sag' })} title="Slaytı diğer tarafa al"><ArrowLeftRight aria-hidden /></button>
            <label className="gsd-oran" title="Metin / slayt genişliği">
              <span className="sr-only">Metin genişliği</span>
              <input type="range" min={25} max={75} step={5} value={duzen.oran} onChange={(e) => setDuzen({ oran: Number(e.target.value) })} aria-label="Metin genişliği" />
            </label>
          </>
        )}
        {duzen.gorunum !== 'pdf' && (
          <span className="gsd-yazi" role="group" aria-label="Yazı boyutu">
            <button type="button" className="tk-metin-btn" onClick={() => setDuzen({ yazi: YAZI[Math.max(0, YAZI.indexOf(duzen.yazi) - 1)] ?? 1 })} disabled={duzen.yazi <= YAZI[0]} aria-label="Yazıyı küçült"><Minus aria-hidden /></button>
            <span className="tk-mono">{Math.round(duzen.yazi * 100)}%</span>
            <button type="button" className="tk-metin-btn" onClick={() => setDuzen({ yazi: YAZI[Math.min(YAZI.length - 1, YAZI.indexOf(duzen.yazi) + 1)] ?? 1 })} disabled={duzen.yazi >= YAZI[YAZI.length - 1]} aria-label="Yazıyı büyüt"><Plus aria-hidden /></button>
          </span>
        )}
        <button type="button" className="tk-btn gsd-tam-btn" onClick={tamDegis} aria-pressed={tam}>
          {tam ? <Minimize2 aria-hidden /> : <Maximize2 aria-hidden />}{tam ? 'Küçült' : 'Tam ekran'}
        </button>
      </div>
      <div className="gsd-govde">
        <div className="gsd-metin" ref={metinRef}>
          {ogeler.map((o, oi) => (o.nokta ? (
            <section key={o.klip} className={`gsd-n${oi === i ? ' is-on' : ''}`}>
              <h4>{o.nokta.baslik}</h4>
              <ul>
                {o.nokta.cumleler.map((c, ci) => {
                  const y = cumleYapi(c);
                  const on = oi === i && ci === cumle;
                  return (
                    <li key={ci} className={`gsd-c${on ? ' is-on' : ''}${y.alt ? ' is-alt' : ''}${y.not ? ' is-not' : ''}${oi === i && ci < cumle ? ' is-gecti' : ''}`}>
                      <button type="button" onClick={() => oynat(oi, ci)} title="Buradan dinle">{on ? <AktifCumle t={c} klip={o.klip} c={ci} /> : <CumleGovde t={c} w={-1} />}</button>
                    </li>
                  );
                })}
              </ul>
            </section>
          ) : (
            <button key={o.klip} type="button" className={`gsd-b${oi === i ? ' is-on' : ''}`} onClick={() => oynat(oi)}>
              <span>{o.bolum + 1}. bölüm</span>{ders.bolumler[o.bolum]?.baslik}
              <small>{oi === i ? <AktifCumle t={ders.bolumler[o.bolum]?.neden || ''} klip={o.klip} c={0} /> : ders.bolumler[o.bolum]?.neden}</small>
            </button>
          )))}
        </div>

        <div className="gsd-pdf">
          <div className="gsd-pdf-bas">
            <FileText aria-hidden />
            <span><b>{PDF_AD[pdf]}</b> · slayt <span className="tk-mono">{sayfa}</span></span>
            {sonrakiPdf && <small title="Önceden yüklendi">Sıradaki: {PDF_AD[sonrakiPdf.k]}</small>}
          </div>
          <div className="gsd-pdf-alan">
            <Suspense fallback={<div className="gsd-pdf-bos">PDF yükleniyor…</div>}>
              {acik.map((k) => (
                <div key={k} className={`gsd-pdf-k${k === pdf ? ' is-on' : ''}`} aria-hidden={k !== pdf}>
                  {pdfHata[k] ? <div className="gsd-pdf-bos">Bu dersin PDF'i açılamadı.</div> : (
                    <PdfDocView
                      src={pdfAdresi(k)}
                      page={k === pdf ? sayfa : sonrakiPdf?.k === k ? sonrakiPdf.p : 1}
                      highlight={k === pdf ? [sayfa, sayfa] : undefined}
                      highlightLabel="Okunan bilginin slaytı"
                      zoom={1}
                      fit="page"
                      preload={k === pdf ? onSayfalar : sonrakiPdf?.k === k ? [sonrakiPdf.p] : undefined}
                      marks={k === pdf && marks && marks.page === sayfa ? marks : null}
                      onError={() => setPdfHata((h) => ({ ...h, [k]: true }))}
                    />
                  )}
                </div>
              ))}
            </Suspense>
          </div>
        </div>
      </div>

      <div className="gsd-oynatici">
        <button type="button" className="tk-metin-btn" onClick={() => baslikGit(-1)} title="Önceki başlık"><SkipBack aria-hidden /></button>
        <button type="button" className="tk-metin-btn" onClick={() => cumleGit(-1)} title="Önceki cümle"><ChevronLeft aria-hidden /></button>
        <button type="button" className="tk-btn tk-btn-ana gsd-oyna" onClick={oynatDuraklat}>{caliyor ? <Pause aria-hidden /> : <Play aria-hidden />}{caliyor ? 'Duraklat' : 'Dinle'}</button>
        <button type="button" className="tk-metin-btn" onClick={() => cumleGit(1)} title="Sonraki cümle"><ChevronRight aria-hidden /></button>
        <button type="button" className="tk-metin-btn" onClick={() => baslikGit(1)} title="Sonraki başlık"><SkipForward aria-hidden /></button>
        <div className="gsd-ilerle" aria-label="İlerleme"><i style={{ ['--w' as string]: `${toplamSn ? (gecenSn / toplamSn) * 100 : 0}%` }} /></div>
        <span className="gsd-sure tk-mono">{Math.floor(gecenSn / 60)}:{String(Math.floor(gecenSn % 60)).padStart(2, '0')} / {Math.round(toplamSn / 60)} dk</span>
        <label className="tk-hiz">
          <select value={hiz} onChange={(e) => setHiz(Number(e.target.value))} aria-label="Hız">
            {HIZLAR.map((h) => <option key={h} value={h}>{h}×</option>)}
          </select>
        </label>
      </div>
    </div>
  );
  return tam ? createPortal(<div className="tk gsd-tam-kap">{icerik}</div>, document.body) : icerik;
}
