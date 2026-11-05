/**
 * KMB Hedefler filmi — KMB belgesindeki öğrenim hedeflerini (hedefCalisma) sırayla, tam ekranda, EMA sesiyle anlatan
 * ayrı animasyon. Lottie değil: sahne kitaplığı (sahneler.tsx) gerçek zamanlı sürülür; her cümle bir vuruştur
 * (`HedefKart.film[i]`: sahne değişimi, biriken eylem, odak ögesi + kamera yakınlaşması). Kamera odak ögesinin gerçek
 * kutusuna (getBBox) yumuşak geçişle yaklaşır, odak dışı alan loşlaşır (spot), etiketler yakınlaşmada aynı boyda kalır.
 * Her bölüm: başlık kartı (hedef no + belge metni) → Ne / Nasıl / Neden → Sık hata (kırmızı uyarı) → Hoca sorar (soru sesi
 * + düşünme payı) → sonraki hedef. Ses `h-<no>` ve `h-<no>-s` klipleri (ses_<kod>.json, cümle zamanlı); ses yoksa sessiz
 * kipte cümle uzunluğuna göre akar. Denetimler oynarken gizlenir; klavye: boşluk, ←/→ cümle, PgUp/PgDn ya da J/L hedef,
 * f tam ekran, Esc kapat. Veri kapısı: scripts/kmb/dogrula.py (film vuruşları, öge kimlikleri, zoom 1–2).
 */
import React, { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import { createPortal } from 'react-dom';
import { getCustomApiUrl } from '../../services/api';
import { type SahneDurum } from './sahneler';
import SahneGoster, { sahne3bVar, ucBoyutTercih } from './SahneGoster';
import { uygula } from './eylem';
import { KMB_DURDUR, sesOnYukle } from './LottieVideo';
import { ilAnahtar, ilOku, ilYaz } from './kmbVeri';
import type { Ders, HedefKart, SesKayit, FilmVurus } from './kmbVeri';

type Asama = 'anlatim' | 'soru' | 'dusun' | 'son';
type Kamera = { cx: number; cy: number; z: number; kutu: { x: number; y: number; w: number; h: number } | null };
const TAM: Kamera = { cx: 400, cy: 250, z: 1, kutu: null };
const DUSUN_SN = 5;
const GIZLE_MS = 3200;
const HIZLAR = [0.75, 1, 1.25, 1.5];
const TERCIH = 'medsoru_kmb_hedeffilm_v1';
type Tercih = { hiz: number; soru: boolean };
const tercihOku = (): Tercih => { try { return { hiz: 1, soru: true, ...JSON.parse(localStorage.getItem(TERCIH) || '{}') }; } catch { return { hiz: 1, soru: true }; } };
const tercihYaz = (p: Partial<Tercih>) => { try { localStorage.setItem(TERCIH, JSON.stringify({ ...tercihOku(), ...p })); } catch { /* özel pencere */ } };

const sesUrl = (kod: string, klip: string, h: string) => `${getCustomApiUrl() || ''}/api/cozucu-ses/kmb/ema/${kod}/${klip}.mp3?v=${h}`;

/** Bölümün cümleleri — Hedefler kartındaki sesle (h-<no>) aynı sıra */
export const filmCumleleri = (k: HedefKart) => [`Hedef ${k.no}. ${k.ne}`, ...k.nasil, k.neden, 'Sınavda sık yapılan bir hata var.', k.hata];
/** Cümlenin evresi: başlık kartı / nasıl / neden / sık hata */
const evre = (k: HedefKart, i: number): 'ne' | 'nasil' | 'neden' | 'hata' => (i === 0 ? 'ne' : i <= k.nasil.length ? 'nasil' : i === k.nasil.length + 1 ? 'neden' : 'hata');
const EVRE_AD = { ne: 'Ne yaparsın', nasil: 'Nasıl', neden: 'Neden', hata: 'Sık hata', soru: 'Hoca sorar' } as const;

/** Ses yoksa cümle uzunluğundan zaman çizelgesi (~14 karakter/sn, cümle arası 0,45 sn) */
function sessizZaman(cumleler: string[]): [number, number][] {
  let t = 0.2;
  return cumleler.map((c) => { const s: [number, number] = [t, t + Math.max(1.6, c.length / 14)]; t = s[1] + 0.45; return s; });
}

/** `i` cümlesine kadar biriken sahne + durum (sahne değişince durum sıfırlanır) */
function sahneDurumu(k: HedefKart, i: number): { sahne: string; durum: SahneDurum; odak: string | null; zoom: number; aci: [number, number] | null } {
  const film = k.film || [];
  let sahne = k.sahne, durum: SahneDurum = {}, odak: string | null = null, zoom = 1, aci: [number, number] | null = null;
  if (!film.length) return { sahne, durum: uygula({}, k.eylem), odak: null, zoom: 1, aci: null };
  for (let j = 0; j <= Math.min(i, film.length - 1); j++) {
    const v: FilmVurus = film[j];
    if (v.sahne && v.sahne !== sahne) { sahne = v.sahne; durum = {}; }
    durum = uygula(durum, v.eylem);
    if (j === Math.min(i, film.length - 1)) { odak = v.odak || null; zoom = v.zoom ?? (v.odak ? 1.2 : 1); aci = v.aci || null; }
  }
  return { sahne, durum, odak, zoom, aci };
}

const Ikon = ({ d }: { d: string }) => <svg viewBox="0 0 24 24" aria-hidden><path d={d} /></svg>;
const I = {
  oynat: 'M8 5v14l11-7z', dur: 'M7 5h3.5v14H7zM13.5 5H17v14h-3.5z',
  onceki: 'M6 5h2v14H6zM20 5v14L9 12z', sonraki: 'M16 5h2v14h-2zM4 5v14l11-7z',
  geri: 'M15 6l-6 6 6 6', ileri: 'M9 6l6 6-6 6',
  tam: 'M4 4h7v2H6v5H4zM13 4h7v7h-2V6h-5zM4 13h2v5h5v2H4zM18 13h2v7h-7v-2h5z',
  tamCik: 'M9 4v5H4v2h7V4zM15 4h-2v7h7V9h-5zM4 15h5v5h2v-7H4zM13 13v7h2v-5h5v-2z',
  kapat: 'M6.4 5 5 6.4 10.6 12 5 17.6 6.4 19l5.6-5.6 5.6 5.6 1.4-1.4-5.6-5.6L19 6.4 17.6 5 12 10.6z',
  soru: 'M11 18h2v-2h-2zm1-16a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 18a8 8 0 1 1 0-16 8 8 0 0 1 0 16zm0-14a4 4 0 0 0-4 4h2a2 2 0 1 1 4 0c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5a4 4 0 0 0-4-4z',
  uyari: 'M1 21h22L12 2zm12-3h-2v-2h2zm0-4h-2v-4h2z',
  onay: 'M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z',
};

export default function HedefFilmi({ ders, ses, bas = 0, onKapat, onSinav }: {
  ders: Ders; ses: SesKayit | null; bas?: number; onKapat: () => void; onSinav?: () => void;
}) {
  const K = ders.hedefCalisma || [];
  const kap = useRef<HTMLDivElement>(null);
  const sahneKap = useRef<HTMLDivElement>(null);
  const audio = useRef<HTMLAudioElement | null>(null);
  const saat = useRef({ bas: 0, t: 0 }); // sessiz kip / düşünme sayacı
  const tRef = useRef(0);
  const gizleZ = useRef(0);
  const [hi, setHi] = useState(Math.min(Math.max(0, bas), Math.max(0, K.length - 1)));
  const [asama, setAsama] = useState<Asama>('anlatim');
  const [t, setT] = useState(0);
  const [cal, setCal] = useState(true); // açılışta kendiliğinden oynar (öğrenci "izle"ye bastı)
  const [goster, setGoster] = useState(true);
  const [tam, setTam] = useState(false);
  const [tercih, setTercih] = useState(tercihOku);
  const [kam, setKam] = useState<Kamera>(TAM);
  const [sesHazir, setSesHazir] = useState(true);
  const [izlenen, setIzlenen] = useState<number[]>(() => ilOku<number[]>(ilAnahtar(ders.kod, 'hedeffilm'), []));
  const k = K[hi];
  const cumleler = useMemo(() => (k ? filmCumleleri(k) : []), [k]);
  const klip = k ? ses?.[`h-${k.no}`] : undefined;
  const soruKlip = k ? ses?.[`h-${k.no}-s`] : undefined;
  const zaman = useMemo<[number, number][]>(() => (klip?.zaman?.length === cumleler.length ? klip.zaman : sessizZaman(cumleler)), [klip, cumleler]);
  const sure = klip ? klip.sure : (zaman[zaman.length - 1]?.[1] ?? 1) + 0.3;
  // etkin cümle: zaman çizelgesinde t'nin düştüğü (cümle arası boşlukta önceki cümle kalır)
  const ci = useMemo(() => { let i = 0; zaman.forEach(([b], j) => { if (t >= b - 0.05) i = j; }); return i; }, [t, zaman]);
  const sd = useMemo(() => (k ? sahneDurumu(k, asama === 'anlatim' ? ci : cumleler.length - 1) : null), [k, ci, asama, cumleler.length]);
  const ev = k ? (asama === 'anlatim' ? evre(k, ci) : 'soru') : 'ne';
  const hataEvresi = asama === 'anlatim' && ev === 'hata' && ci === cumleler.length - 1;

  // ——— açılış: tam ekran, yönlendirme, kaydırma kilidi; kapanışta diğer oynatıcılara "durdur"
  useEffect(() => {
    kap.current?.requestFullscreen?.().then(() => setTam(true)).catch(() => { /* izin yoksa katman pencereyi kaplar */ });
    try { (screen.orientation as any)?.lock?.('landscape').catch(() => {}); } catch { /* yönlendirme kilidi yok */ }
    lockScroll();
    document.body.classList.add('kmb-film-acik'); // kabuğun alt sekme çubuğu (zoom'lu, sabit) filmin altından görünmesin
    window.dispatchEvent(new CustomEvent(KMB_DURDUR, { detail: 'hedef-film' }));
    const f = () => setTam(!!document.fullscreenElement);
    document.addEventListener('fullscreenchange', f);
    return () => { unlockScroll(); document.body.classList.remove('kmb-film-acik'); document.removeEventListener('fullscreenchange', f); audio.current?.pause(); };
  }, []);
  // sonraki hedefin sesini önceden indir (geçişte boşluk olmasın)
  useEffect(() => {
    const s = K[hi + 1];
    if (!s || !ses) return;
    for (const ad of [`h-${s.no}`, `h-${s.no}-s`]) { const z = ses[ad]; if (z) sesOnYukle(sesUrl(ders.kod, ad, z.h)).catch(() => {}); }
  }, [hi, K, ses, ders.kod]);

  const durdur = useCallback(() => { audio.current?.pause(); setCal(false); setGoster(true); }, []);
  const gizlemeKur = useCallback(() => {
    window.clearTimeout(gizleZ.current);
    gizleZ.current = window.setTimeout(() => setGoster(false), GIZLE_MS);
  }, []);
  const uyandir = useCallback(() => { setGoster(true); if (cal) gizlemeKur(); }, [cal, gizlemeKur]);
  useEffect(() => () => window.clearTimeout(gizleZ.current), []);

  /** Klibi yükleyip `s` saniyesinden oynat (ses yoksa sessiz saat) */
  const sesBaslat = useCallback(async (ad: string, h: string | undefined, s: number, hiz: number) => {
    audio.current?.pause();
    if (!h) { audio.current = null; return; }
    const a = new Audio();
    a.preload = 'auto';
    audio.current = a;
    setSesHazir(false);
    const u = await sesOnYukle(sesUrl(ders.kod, ad, h));
    if (audio.current !== a) return;
    a.src = u;
    a.playbackRate = hiz;
    a.currentTime = s;
    try { await a.play(); } catch (e) {
      // hızlı hedef geçişinde bir önceki klibin kesilen play() sözü AbortError ile düşer: o eski klibe aittir, oynatmayı durdurmaz.
      // Yalnız tarayıcının otomatik oynatma engeli (NotAllowedError) filmi duraklatır; kullanıcı ▶ basar.
      if (audio.current === a && (e as any)?.name === 'NotAllowedError') setCal(false);
    }
    if (audio.current === a) setSesHazir(true);
  }, [ders.kod]);

  const oynat = useCallback((s?: number) => {
    const b = s ?? (tRef.current >= sure - 0.1 ? 0 : tRef.current);
    saat.current = { bas: performance.now(), t: b };
    tRef.current = b; setT(b);
    setAsama('anlatim');
    setCal(true);
    gizlemeKur();
    sesBaslat(`h-${k?.no}`, klip?.h, b, tercih.hiz);
  }, [sure, k, klip, tercih.hiz, sesBaslat, gizlemeKur]);

  const hedefeGit = useCallback((i: number, otomatik = true) => {
    const j = Math.max(0, Math.min(K.length - 1, i));
    audio.current?.pause(); audio.current = null;
    setHi(j); setAsama('anlatim'); setKam(TAM);
    tRef.current = 0; setT(0);
    saat.current = { bas: performance.now(), t: 0 };
    ilYaz(ilAnahtar(ders.kod, 'hedeffilm-son'), j);
    setCal(otomatik);
    if (otomatik) gizlemeKur();
  }, [K.length, ders.kod, gizlemeKur]);
  // hedef değişince (açılış dahil) oynuyorsa o hedefin sesi baştan başlar
  useEffect(() => {
    if (!k || !cal) return;
    gizlemeKur();
    sesBaslat(`h-${k.no}`, klip?.h, 0, tercihOku().hiz);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hi]);
  useEffect(() => { if (!cal) audio.current?.pause(); else if (audio.current?.paused && asama !== 'dusun' && audio.current.src) audio.current.play().catch(() => {}); }, [cal, asama]);

  const bitir = useCallback(() => {
    if (!k) return;
    const y = izlenen.includes(k.no) ? izlenen : [...izlenen, k.no];
    setIzlenen(y); ilYaz(ilAnahtar(ders.kod, 'hedeffilm'), y);
    if (hi < K.length - 1) hedefeGit(hi + 1);
    else { setAsama('son'); setCal(false); setGoster(true); audio.current?.pause(); if (document.fullscreenElement) document.exitFullscreen().catch(() => {}); }
  }, [k, izlenen, ders.kod, hi, K.length, hedefeGit]);

  const soruyaGec = useCallback(() => {
    if (!k || !tercih.soru) { bitir(); return; }
    setAsama('soru');
    saat.current = { bas: performance.now(), t: 0 };
    tRef.current = 0; setT(0);
    sesBaslat(`h-${k.no}-s`, soruKlip?.h, 0, tercih.hiz);
  }, [k, tercih.soru, tercih.hiz, soruKlip, sesBaslat, bitir]);

  // ——— oynatma döngüsü (≈15 fps durum güncellemesi): ses varsa ses saati, yoksa iç saat
  useEffect(() => {
    if (!cal) return;
    let id = 0, son = 0;
    const adim = (now: number) => {
      id = requestAnimationFrame(adim);
      if (now - son < 66) return;
      son = now;
      const a = audio.current;
      if (asama === 'dusun') {
        const s = (now - saat.current.bas) / 1000;
        tRef.current = s; setT(s);
        if (s >= DUSUN_SN) { bitir(); }
        return;
      }
      const sonSn = asama === 'soru' ? (soruKlip?.zaman?.[0]?.[1] ?? (k ? k.hoca.length / 14 + 0.4 : 3)) : sure;
      let s: number;
      // klip gerçek süresi ses_<kod>.json'daki `sure`den birkaç ms kısa olabilir: biten ses bölümün sonu sayılır (ilerleme %98'de asılı kalmasın)
      if (a && a.src && a.ended) s = sonSn;
      else if (a && a.src && !a.paused) s = a.currentTime;
      else if (a && a.src) { s = tRef.current; } // ses tamponlanıyor / otomatik oynatma bekliyor
      else s = saat.current.t + ((now - saat.current.bas) / 1000) * tercih.hiz;
      tRef.current = s; setT(s);
      if (s >= sonSn - 0.02) {
        if (asama === 'anlatim') soruyaGec();
        else { a?.pause(); setAsama('dusun'); saat.current = { bas: now, t: 0 }; tRef.current = 0; setT(0); }
      }
    };
    id = requestAnimationFrame(adim);
    return () => cancelAnimationFrame(id);
  }, [cal, asama, sure, soruKlip, k, tercih.hiz, soruyaGec, bitir]);

  // ——— kamera: odak ögesinin gerçek kutusuna yaklaş (etiketler ve spot da ona göre)
  const [ucB, setUcB] = useState(ucBoyutTercih);
  useEffect(() => { const f = () => setUcB(ucBoyutTercih()); window.addEventListener('kmb-3b', f); return () => window.removeEventListener('kmb-3b', f); }, []);
  const ucBoyut = !!sd && ucB && sahne3bVar(sd.sahne);
  useLayoutEffect(() => {
    if (!sd) return;
    const kök = sahneKap.current;
    // 3B sahnede kamera motorun içindedir (odak → yumuşak yaklaşma); CSS yakınlaştırma ve spot kullanılmaz
    if (ucBoyut || !sd.odak || sd.zoom <= 1.02) { setKam(TAM); return; }
    const el = kök?.querySelector<SVGGraphicsElement>(`[data-id="${sd.odak}"]`);
    if (!el || typeof el.getBBox !== 'function') { setKam(TAM); return; }
    try {
      const b0 = el.getBBox();
      if (!b0.width && !b0.height) { setKam(TAM); return; }
      // getBBox ögenin kendi koordinatındadır; ata grupta transform varsa (ng-kesit translate(60 0)) kutu kayar → sahne köküne çevir
      const svg = el.ownerSVGElement, m = svg && el.getCTM() && svg.getCTM() ? svg.getCTM()!.inverse().multiply(el.getCTM()!) : null;
      const kose = m ? [[b0.x, b0.y], [b0.x + b0.width, b0.y], [b0.x, b0.y + b0.height], [b0.x + b0.width, b0.y + b0.height]].map(([x, y]) => new DOMPoint(x, y).matrixTransform(m)) : null;
      const b = kose ? { x: Math.min(...kose.map((q) => q.x)), y: Math.min(...kose.map((q) => q.y)), width: Math.max(...kose.map((q) => q.x)) - Math.min(...kose.map((q) => q.x)), height: Math.max(...kose.map((q) => q.y)) - Math.min(...kose.map((q) => q.y)) } : b0;
      // H462: yakınlaşma ılımlı (≤1,35) ve odak kutusu + etiket payı kadrajın en çok %70'ini kaplar; daha yakın çekim
      // komşu ayrıntıları ve etiketleri kesiyordu. Kutu zaten büyükse yakınlaşma yapılmaz (yalnız spot).
      const pay = 24;
      const kw = b.width + pay * 2, kh = b.height + pay * 2;
      const z = Math.max(1, Math.min(1.35, sd.zoom, (800 * 0.7) / kw, (500 * 0.7) / kh));
      if (z < 1.04) { setKam({ cx: 400, cy: 250, z: 1, kutu: { x: b.x - pay, y: b.y - pay, w: kw, h: kh } }); return; }
      const gw = 800 / z, gh = 500 / z;
      const cx = Math.min(800 - gw / 2, Math.max(gw / 2, b.x + b.width / 2));
      const cy = Math.min(500 - gh / 2, Math.max(gh / 2, b.y + b.height / 2));
      setKam({ cx, cy, z, kutu: { x: b.x - pay, y: b.y - pay, w: kw, h: kh } });
    } catch { setKam(TAM); }
  }, [sd?.odak, sd?.zoom, sd?.sahne, ucBoyut]); // eslint-disable-line react-hooks/exhaustive-deps

  // ——— denetimler
  const cumleyeGit = (i: number) => {
    const j = Math.max(0, Math.min(cumleler.length - 1, i));
    const b = Math.max(0, zaman[j][0] - 0.05);
    if (asama !== 'anlatim') { setAsama('anlatim'); }
    tRef.current = b; setT(b); saat.current = { bas: performance.now(), t: b };
    if (audio.current?.src && asama === 'anlatim') { audio.current.currentTime = b; if (cal) audio.current.play().catch(() => {}); }
    else if (cal) sesBaslat(`h-${k?.no}`, klip?.h, b, tercih.hiz);
    uyandir();
  };
  const degistir = () => { if (asama === 'son') return; if (cal) durdur(); else { setCal(true); gizlemeKur(); if (!audio.current?.src && asama === 'anlatim') oynat(tRef.current); else saat.current = { bas: performance.now(), t: tRef.current }; } };
  const hizSec = (h: number) => { setTercih((p) => ({ ...p, hiz: h })); tercihYaz({ hiz: h }); if (audio.current) audio.current.playbackRate = h; saat.current = { bas: performance.now(), t: tRef.current }; };
  const soruAc = () => { setTercih((p) => { tercihYaz({ soru: !p.soru }); return { ...p, soru: !p.soru }; }); };
  const tamDegistir = () => { if (document.fullscreenElement) document.exitFullscreen().catch(() => {}); else kap.current?.requestFullscreen?.().catch(() => {}); };
  const kapat = () => { if (document.fullscreenElement) document.exitFullscreen().catch(() => {}); audio.current?.pause(); onKapat(); };
  const tus = (e: React.KeyboardEvent) => {
    const m: Record<string, () => void> = {
      ' ': degistir, k: degistir, Escape: kapat, f: tamDegistir,
      ArrowLeft: () => cumleyeGit(ci - 1), ArrowRight: () => cumleyeGit(ci + 1),
      PageUp: () => hedefeGit(hi - 1), PageDown: () => hedefeGit(hi + 1), j: () => hedefeGit(hi - 1), l: () => hedefeGit(hi + 1),
    };
    const f = m[e.key];
    if (f) { e.preventDefault(); f(); uyandir(); }
  };

  if (!k) return null;
  const toplamIlerleme = ((hi + (asama === 'son' ? 1 : Math.min(1, t / sure))) / K.length) * 100;
  const belge = ders.hedefler.find((h) => h.no === k.no)?.metin || k.ne;
  // cümle içi kelime akışı: cümlenin geçen oranına göre kelimeler belirir (ses cümleyi okurken yazı da akar)
  const [cb, cs] = zaman[ci] || [0, 1];
  const oran = asama === 'anlatim' ? Math.min(1, Math.max(0, (t - cb) / Math.max(0.3, cs - cb))) : 1;
  const metin = asama === 'anlatim' ? cumleler[ci] : k.hoca;
  const kelimeler = metin.split(' ');
  const gorunen = asama === 'anlatim' ? Math.ceil(kelimeler.length * Math.min(1, oran * 1.25 + 0.08)) : kelimeler.length;
  const evreler: (keyof typeof EVRE_AD)[] = ['ne', 'nasil', 'neden', 'hata', 'soru'];
  const kamStil: React.CSSProperties = {
    transformOrigin: `${(kam.cx / 800) * 100}% ${(kam.cy / 500) * 100}%`,
    transform: `scale(${kam.z})`,
  };
  const spotStil: React.CSSProperties = kam.kutu ? {
    left: `${(kam.kutu.x / 800) * 100}%`, top: `${(kam.kutu.y / 500) * 100}%`,
    width: `${(kam.kutu.w / 800) * 100}%`, height: `${(kam.kutu.h / 500) * 100}%`, opacity: 1,
  } : { left: '-3%', top: '-3%', width: '106%', height: '106%', opacity: 0 };

  return createPortal(
    <div ref={kap} className={`kmb-hf kmb-kok${goster || !cal ? '' : ' uyku'}${hataEvresi ? ' hata' : ''}${tam ? ' tam' : ''}`} role="dialog" aria-label={`Hedefler filmi: ${ders.ad}`}
      tabIndex={-1} onKeyDown={tus} onPointerMove={uyandir} onClick={() => { if (!goster) uyandir(); }}>
      {/* üst: hedef şeridi + başlık + düğmeler */}
      <div className="kmb-hf-ust">
        <div className="kmb-hf-serit" role="tablist" aria-label="Hedefler">
          {K.map((x, j) => (
            <button key={x.no} role="tab" aria-selected={j === hi} title={`Hedef ${x.no}: ${ders.hedefler.find((h) => h.no === x.no)?.metin || ''}`}
              className={`${j === hi ? 'etkin' : ''}${j < hi || izlenen.includes(x.no) ? ' gecti' : ''}`} onClick={(e) => { e.stopPropagation(); hedefeGit(j); }}>
              {j === hi && asama !== 'son' && <i style={{ width: `${Math.min(100, (t / sure) * 100)}%` }} />}
            </button>
          ))}
        </div>
        <div className="kmb-hf-baslik"><span className="kmb-hf-no">Hedef {k.no} / {K.length}</span><b>{belge}</b></div>
        <div className="kmb-hf-dugmeler">
          <button onClick={(e) => { e.stopPropagation(); tamDegistir(); }} aria-label={tam ? 'Tam ekrandan çık' : 'Tam ekran'}><Ikon d={tam ? I.tamCik : I.tam} /></button>
          <button onClick={(e) => { e.stopPropagation(); kapat(); }} aria-label="Kapat"><Ikon d={I.kapat} /></button>
        </div>
      </div>

      {/* gövde: sahne (kamera + spot) ve sağda evre rayı */}
      <div className="kmb-hf-govde">
        <div className={`kmb-hf-sahne-kap ev-${ev}`} onClick={(e) => { e.stopPropagation(); if (goster) degistir(); else uyandir(); }}>
          <div className="kmb-hf-sahne" ref={sahneKap} style={kamStil}>
            {sd && <SahneGoster key={sd.sahne} sahne={sd.sahne} durum={sd.durum} odak={sd.odak} aci={sd.aci} olcek={kam.z} />}
            <div className="kmb-hf-spot" style={spotStil} aria-hidden />
          </div>
          {/* evre damgası (sol üst) */}
          <div className={`kmb-hf-damga ev-${ev}`} key={`${hi}-${ev}`}>
            {ev === 'hata' ? <Ikon d={I.uyari} /> : ev === 'soru' ? <Ikon d={I.soru} /> : null}
            <span>{EVRE_AD[ev]}</span>
          </div>
          {/* başlık kartı: bölüm başında, ilk cümle okunurken */}
          {asama === 'anlatim' && ci === 0 && (
            <div className="kmb-hf-kart" key={`kart-${hi}`}>
              <span className="kmb-hf-kart-no"><b>{k.no}</b><small>/ {K.length}</small></span>
              <span className="kmb-hf-kart-ust">KMB belgesi · Öğrenim hedefi</span>
              <h2>{belge}</h2>
            </div>
          )}
          {/* hoca sorusu + düşünme payı */}
          {(asama === 'soru' || asama === 'dusun') && (
            <div className="kmb-hf-soru" key={`soru-${hi}`} onClick={(e) => e.stopPropagation()}>
              <span className="kmb-hf-soru-ust"><Ikon d={I.soru} /> Hoca sorar</span>
              <p>{k.hoca}</p>
              {asama === 'dusun' ? (
                <div className="kmb-hf-dusun">
                  <svg viewBox="0 0 36 36" aria-hidden><circle cx="18" cy="18" r="15.5" /><circle cx="18" cy="18" r="15.5" className="dolum" style={{ strokeDashoffset: 97.4 * (1 - Math.min(1, t / DUSUN_SN)) }} /></svg>
                  <span>Kendi cevabını ver… <b>{Math.max(0, Math.ceil(DUSUN_SN - t))}</b></span>
                  <button className="ana" onClick={bitir}>{hi < K.length - 1 ? 'Sıradaki hedef ›' : 'Bitir ›'}</button>
                </div>
              ) : <span className="kmb-hf-soru-alt">Soru okunuyor…</span>}
              <details className="kmb-hf-cevap"><summary>Cevabı göster</summary><p><b>Ne:</b> {k.ne}</p>{k.nasil.map((c, i) => <p key={i}>{c}</p>)}<p><b>Neden:</b> {k.neden}</p></details>
            </div>
          )}
          {/* bitiş: tüm hedefler */}
          {asama === 'son' && (
            <div className="kmb-hf-son" onClick={(e) => e.stopPropagation()}>
              <h2>Tüm hedefleri izledin</h2>
              <p>KMB belgesindeki {K.length} öğrenim hedefi, her birinin nasıl yapıldığı, nedeni ve sınavda sık yapılan hatası.</p>
              <ol>{K.map((x, j) => <li key={x.no} style={{ animationDelay: `${j * 70}ms` }}><Ikon d={I.onay} /><span>{ders.hedefler.find((h) => h.no === x.no)?.metin}</span></li>)}</ol>
              <div className="kmb-denetim">
                <button className="ana" onClick={() => hedefeGit(0)}>↻ Baştan izle</button>
                {onSinav && <button onClick={() => { kapat(); onSinav(); }}>Sınava geç ›</button>}
                <button onClick={kapat}>Hedef kartlarına dön</button>
              </div>
            </div>
          )}
          {!sesHazir && cal && <span className="kmb-hf-yukleniyor">Ses yükleniyor…</span>}
          {!klip && asama === 'anlatim' && <span className="kmb-hf-sessiz">Sessiz kip: bu hedefin sesi henüz yok</span>}
        </div>
        <aside className="kmb-hf-ray" aria-label="Bölümün evreleri">
          {evreler.map((e) => (
            <button key={e} className={`ev-${e}${e === ev ? ' etkin' : ''}${(evreler.indexOf(e) < evreler.indexOf(ev)) ? ' gecti' : ''}${e === 'soru' && !tercih.soru ? ' kapali' : ''}`}
              onClick={(ev2) => { ev2.stopPropagation(); if (e === 'soru') { if (asama === 'anlatim') soruyaGec(); } else cumleyeGit(e === 'ne' ? 0 : e === 'nasil' ? 1 : e === 'neden' ? k.nasil.length + 1 : k.nasil.length + 2); }}>
              <i /><span>{EVRE_AD[e]}</span>
            </button>
          ))}
        </aside>
      </div>

      {/* alt: akan altyazı + denetimler */}
      <div className="kmb-hf-alt" onClick={(e) => e.stopPropagation()}>
        {asama !== 'son' && (
          <p className={`kmb-hf-altyazi ev-${ev}`} aria-live="polite">
            {kelimeler.map((w, i) => <span key={`${hi}-${ci}-${i}`} className={i < gorunen ? 'g' : ''}>{w} </span>)}
          </p>
        )}
        <div className="kmb-hf-denetim">
          <button onClick={() => hedefeGit(hi - 1)} disabled={hi === 0} aria-label="Önceki hedef"><Ikon d={I.onceki} /></button>
          <button onClick={() => cumleyeGit(ci - 1)} disabled={asama !== 'anlatim' || ci === 0} aria-label="Önceki cümle"><Ikon d={I.geri} /></button>
          <button className="ana" onClick={degistir} disabled={asama === 'son'} aria-label={cal ? 'Duraklat' : 'Oynat'}><Ikon d={cal ? I.dur : I.oynat} /></button>
          <button onClick={() => (asama === 'anlatim' && ci < cumleler.length - 1 ? cumleyeGit(ci + 1) : asama === 'anlatim' ? soruyaGec() : bitir())} disabled={asama === 'son'} aria-label="Sonraki cümle"><Ikon d={I.ileri} /></button>
          <button onClick={() => hedefeGit(hi + 1)} disabled={hi >= K.length - 1} aria-label="Sonraki hedef"><Ikon d={I.sonraki} /></button>
          <span className="kmb-hf-bosluk" />
          <span className="kmb-hf-ilerleme" aria-hidden><i style={{ width: `${toplamIlerleme}%` }} /></span>
          <button className={`kmb-hf-metin${tercih.soru ? ' etkin' : ''}`} onClick={soruAc} title="Her hedefin sonunda hocanın sorusu sorulsun" aria-pressed={tercih.soru}>Sorular</button>
          <select className="kmb-hf-hiz" value={tercih.hiz} onChange={(e) => hizSec(Number(e.target.value))} aria-label="Hız">
            {HIZLAR.map((h) => <option key={h} value={h}>{h}×</option>)}
          </select>
        </div>
      </div>
    </div>,
    document.body,
  );
}
