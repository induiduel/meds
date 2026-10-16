import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  Check, ChevronDown, ChevronLeft, ChevronRight, Maximize2, Minimize2, Pause, Play, RotateCcw, SkipForward, Star, Volume2, X,
} from 'lucide-react';
import { getCustomApiUrl } from '../../../services/api';
import { lockScroll, unlockScroll } from '../../../utils/scrollLock';
import { ogrenildiAyarla, tercihOku, tercihYaz } from '../onem/onemVeri';
import { Metin } from '../onem/OnemMadde';
import { asistanDosyasi } from './asistanVeri';
import '../../../styles/patoloji-asistan.css';

/**
 * Patoloji · Sesli sınav asistanı (tam ekran). Yalnız "Sınav için en önemliler" spotları için.
 * İçerik: src/data/patoloji_asistan/<kod>.json (scripts/patoloji_onem/asistan_birlestir.py) — her ders PDF'inden, sınava uygun ve
 * en önemli maddeler slayt sırasıyla; önemli adımlarda çıkmış/örnek soru, her yanlış şık için "neden yanlış · neyi karıştırdın ·
 * doğrusu" açıklaması. Ses: EMA Lightning klipleri (/api/patoloji-asistan/ses/<kod>/<klip>.mp3?v=…), cümle zamanlarıyla vurgu.
 *
 * Akış (sahneler): giriş → [anlatım → (soru)]* → kapanış → sonuç. Anlatım bitince otomatik sonraki sahne (kapatılabilir).
 * Soru: kök okunur, öğrenci şık seçer → doğruysa "Doğru" + pekiştirme, otomatik ilerler; yanlışsa o şıkkın açıklaması okunur,
 * şık elenir, tekrar dener ya da doğruyu görüp geçer. Sonuçta yanlışları tekrar etme. Ses yoksa okuma süresiyle ilerler.
 */

interface Klip { v: string; sure: number; zaman: [number, number][] }
interface Soru { tur: 'cikmis' | 'ornek'; sinav?: string; kok: string; secenekler: Record<string, string>; dogru: string; dogruMetin: string; yanlis: Record<string, string> }
interface Adim { id: string; puan: number; aday: number | null; kategori: string; baslik: string; bilgi: string; cumleler: string[]; soru?: Soru }
interface Ders { kod: string; no: number; baslik: string; soruSayisi: number; giris: string[]; kapanis: string[]; adimlar: Adim[]; klip: Record<string, Klip> }
interface DizinDers { kod: string; no: number; baslik: string; adim: number; soru: number; ses: boolean; sure: number }

const DIZIN = import.meta.glob('../../../data/patoloji_asistan/index.json') as Record<string, () => Promise<{ default: { dersler: DizinDers[] } }>>;
const dersYukle = (kod: string) => asistanDosyasi(kod)?.().then((m) => m.default as Ders);
const dizinYukle = () => (Object.values(DIZIN)[0]?.() ?? Promise.resolve({ default: { dersler: [] } })).then((m) => m.default.dersler);

type Sahne =
  | { tip: 'giris' }
  | { tip: 'anlatim'; a: Adim; n: number }
  | { tip: 'soru'; a: Adim; n: number }
  | { tip: 'kapanis' }
  | { tip: 'son' };
type Sonuc = 'd' | 'd2' | 'y'; // ilk denemede doğru · sonradan doğru · bilemedi
interface Kayit { i: number; sonuc: Record<string, Sonuc>; at: string }
const ILERLEME_KEY = 'medsoru_onem_asistan_v1';
const TERCIH_KEY = 'medsoru_onem_asistan_tercih_v1';
const HIZLAR = [0.85, 1, 1.15, 1.3, 1.5, 1.75, 2];
const kelimeSay = (s: string) => (s.match(/\S+/g) || []).length;
const azHareket = () => typeof window !== 'undefined' && !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
const sahneleriKur = (d: Ders, yalniz?: Set<string>): Sahne[] => {
  const ad = yalniz ? d.adimlar.filter((a) => yalniz.has(a.id)) : d.adimlar;
  const out: Sahne[] = yalniz ? [] : [{ tip: 'giris' }];
  ad.forEach((a, n) => { out.push({ tip: 'anlatim', a, n }); if (a.soru) out.push({ tip: 'soru', a, n }); });
  if (!yalniz) out.push({ tip: 'kapanis' });
  out.push({ tip: 'son' });
  return out;
};

export const PatolojiAsistan: React.FC<{ kod: string; onClose: () => void; onDersDegis?: (kod: string) => void }> = ({ kod: kod0, onClose, onDersDegis }) => {
  const [kod, setKod] = useState(kod0);
  const [dizin, setDizin] = useState<DizinDers[]>([]);
  const [ders, setDers] = useState<Ders | null>(null);
  const [hata, setHata] = useState(false);
  const [tekrar, setTekrar] = useState<Set<string> | null>(null); // yalnız yanlışları tekrar
  const [i, setI] = useState(0);
  const [sonuc, setSonuc] = useState<Record<string, Sonuc>>({});
  const [tercih, setTercih0] = useState(() => tercihOku(TERCIH_KEY, { hiz: 1, otomatik: true }));
  const setTercih = (p: Partial<typeof tercih>) => setTercih0((t) => { const n = { ...t, ...p }; tercihYaz(TERCIH_KEY, n); return n; });
  const [caliyor, setCaliyor] = useState(false);
  const [aktifCumle, setAktifCumle] = useState(-1);
  const [sesYok, setSesYok] = useState(false);
  const [devamSor, setDevamSor] = useState<Kayit | null>(null);
  const [dersMenu, setDersMenu] = useState(false);
  const [tamEkran, setTamEkran] = useState(false);
  const [engel, setEngel] = useState(false); // tarayıcı kendiliğinden çalmaya izin vermedi
  // soru durumu
  const [elenen, setElenen] = useState<string[]>([]);
  const [secim, setSecim] = useState<string | null>(null);
  const [cozuldu, setCozuldu] = useState<'dogru' | 'goster' | null>(null);
  const audio = useRef<HTMLAudioElement | null>(null);
  const zamanlayici = useRef<number | null>(null);
  const otoRef = useRef<number | null>(null); // bekleyen otomatik geçiş (elle gezinmede iptal)
  const bittiRef = useRef<(() => void) | null>(null);
  const kokRef = useRef<HTMLDivElement>(null);

  const sahneler = useMemo(() => (ders ? sahneleriKur(ders, tekrar || undefined) : []), [ders, tekrar]);
  const s = sahneler[i];
  const adimSayisi = ders ? (tekrar ? tekrar.size : ders.adimlar.length) : 0;

  useEffect(() => { lockScroll(); return () => unlockScroll(); }, []);
  useEffect(() => { dizinYukle().then(setDizin).catch(() => {}); }, []);
  useEffect(() => {
    let canli = true;
    setDers(null); setHata(false); setTekrar(null); setI(0); setSonuc({}); setDevamSor(null);
    const p = dersYukle(kod);
    if (!p) { setHata(true); return; }
    p.then((d) => {
      if (!canli) return;
      setDers(d);
      try {
        const k = (JSON.parse(localStorage.getItem(ILERLEME_KEY) || '{}') as Record<string, Kayit>)[kod];
        if (k && k.i > 1 && k.i < sahneleriKur(d).length - 1) setDevamSor(k);
      } catch { /* yok */ }
    }).catch(() => canli && setHata(true));
    return () => { canli = false; };
  }, [kod]);
  // ilerleme kaydı (yalnız tam akışta)
  useEffect(() => {
    if (!ders || tekrar || devamSor) return;
    try {
      const t = JSON.parse(localStorage.getItem(ILERLEME_KEY) || '{}');
      t[kod] = { i, sonuc, at: new Date().toISOString() } as Kayit;
      localStorage.setItem(ILERLEME_KEY, JSON.stringify(t));
    } catch { /* özel pencere */ }
  }, [i, sonuc, ders, tekrar, kod, devamSor]);

  // ---------- ses
  const durdur = useCallback(() => {
    const a = audio.current;
    if (a) { a.onended = null; a.ontimeupdate = null; a.onerror = null; a.pause(); }
    if (zamanlayici.current) { window.clearInterval(zamanlayici.current); zamanlayici.current = null; }
    bittiRef.current = null;
    setCaliyor(false);
  }, []);
  /** klibi çal; yoksa okuma süresiyle cümle cümle ilerle. bitince `bitti` */
  const cal = useCallback((klip: string, cumleler: string[], bitti?: () => void) => {
    durdur();
    setAktifCumle(cumleler.length ? 0 : -1);
    bittiRef.current = bitti || null;
    const k = ders?.klip[klip];
    const hiz = tercih.hiz;
    const yedek = () => {
      setSesYok(true);
      // okuma süresi: ~2,6 kelime/sn × hız
      const sureler = cumleler.map((c) => Math.max(1.4, kelimeSay(c) / 2.6) / hiz);
      let j = 0; let t = 0;
      setCaliyor(true);
      zamanlayici.current = window.setInterval(() => {
        t += 0.1;
        if (t >= sureler[j]) {
          t = 0; j++;
          if (j >= sureler.length) { durdur(); setAktifCumle(-1); bitti?.(); return; }
          setAktifCumle(j);
        }
      }, 100);
    };
    if (!k) { yedek(); return; }
    setSesYok(false);
    if (!audio.current) audio.current = new Audio();
    const a = audio.current;
    a.src = `${getCustomApiUrl() || ''}/api/patoloji-asistan/ses/${encodeURIComponent(kod)}/${encodeURIComponent(klip)}.mp3?v=${k.v}`;
    a.playbackRate = hiz;
    try { (a as HTMLAudioElement & { preservesPitch?: boolean }).preservesPitch = true; } catch { /* eski tarayıcı */ }
    a.ontimeupdate = () => {
      const t = a.currentTime;
      let j = k.zaman.findIndex(([b, e]) => t >= b - 0.05 && t < e + 0.4);
      if (j < 0) j = k.zaman.filter(([b]) => b <= t).length - 1;
      setAktifCumle(Math.max(0, Math.min(cumleler.length - 1, j)));
    };
    a.onended = () => { setCaliyor(false); setAktifCumle(-1); const f = bittiRef.current; bittiRef.current = null; f?.(); };
    a.onerror = () => { a.onerror = null; yedek(); };
    a.play().then(() => { setCaliyor(true); setEngel(false); }).catch((e) => { setCaliyor(false); if (e?.name === 'NotAllowedError') setEngel(true); });
  }, [ders, kod, tercih.hiz, durdur]);
  useEffect(() => () => { durdur(); if (otoRef.current) window.clearTimeout(otoRef.current); }, [durdur]);
  useEffect(() => { if (audio.current) audio.current.playbackRate = tercih.hiz; }, [tercih.hiz]);

  const ileri = useCallback(() => setI((x) => Math.min(sahneler.length - 1, x + 1)), [sahneler.length]);
  const geri = useCallback(() => setI((x) => Math.max(0, x - 1)), []);
  const otoIleri = useCallback(() => {
    if (!tercih.otomatik) return;
    if (otoRef.current) window.clearTimeout(otoRef.current);
    otoRef.current = window.setTimeout(() => { otoRef.current = null; ileri(); }, 650);
  }, [tercih.otomatik, ileri]);

  // sahne değişince: soru durumunu sıfırla, sesi başlat
  useEffect(() => {
    if (otoRef.current) { window.clearTimeout(otoRef.current); otoRef.current = null; }
    if (!ders || !s || devamSor) return;
    setElenen([]); setSecim(null); setCozuldu(null);
    kokRef.current?.scrollTo({ top: 0, behavior: azHareket() ? 'auto' : 'smooth' });
    if (s.tip === 'giris') cal('giris', ders.giris, otoIleri);
    else if (s.tip === 'kapanis') cal('kapanis', ders.kapanis, otoIleri);
    else if (s.tip === 'anlatim') cal(`a-${s.a.id}`, s.a.cumleler, otoIleri);
    else if (s.tip === 'soru') cal(`q-${s.a.id}`, [s.a.soru!.kok]);
    else durdur();
  }, [i, ders, sahneler, devamSor]); // eslint-disable-line react-hooks/exhaustive-deps

  const geriyeKaydir = () => requestAnimationFrame(() => requestAnimationFrame(() =>
    kokRef.current?.querySelector('.pa-geri')?.scrollIntoView({ block: 'nearest', behavior: azHareket() ? 'auto' : 'smooth' })));
  const cevapla = (h: string) => {
    if (!s || s.tip !== 'soru' || cozuldu || elenen.includes(h)) return;
    const q = s.a.soru!;
    setSecim(h);
    if (h === q.dogru) {
      setCozuldu('dogru');
      setSonuc((r) => ({ ...r, [s.a.id]: r[s.a.id] === 'y' || elenen.length ? (r[s.a.id] || 'd2') : 'd' }));
      cal(`d-${s.a.id}`, [q.dogruMetin], otoIleri);
      geriyeKaydir();
    } else {
      setElenen((e) => [...e, h]);
      setSonuc((r) => ({ ...r, [s.a.id]: 'y' }));
      cal(`y-${s.a.id}-${h}`, [q.yanlis[h]]);
      geriyeKaydir();
    }
  };
  const dogruyuGoster = () => {
    if (!s || s.tip !== 'soru') return;
    setCozuldu('goster'); setSecim(s.a.soru!.dogru);
    setSonuc((r) => ({ ...r, [s.a.id]: 'y' }));
    cal(`d-${s.a.id}`, [s.a.soru!.dogruMetin]);
    geriyeKaydir();
  };
  const oynatDuraklat = () => {
    const a = audio.current;
    if (caliyor) {
      if (zamanlayici.current) { window.clearInterval(zamanlayici.current); zamanlayici.current = null; setCaliyor(false); return; }
      a?.pause(); setCaliyor(false);
    } else if (a && a.src && !a.ended && a.currentTime > 0) { a.play().then(() => setCaliyor(true)).catch(() => {}); }
    else if (s && ders) {
      if (s.tip === 'giris') cal('giris', ders.giris, otoIleri);
      else if (s.tip === 'kapanis') cal('kapanis', ders.kapanis, otoIleri);
      else if (s.tip === 'anlatim') cal(`a-${s.a.id}`, s.a.cumleler, otoIleri);
      else if (s.tip === 'soru') cal(`q-${s.a.id}`, [s.a.soru!.kok]);
    }
  };

  // klavye
  useEffect(() => {
    const f = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey || e.altKey || (e.target as HTMLElement | null)?.closest?.('input,textarea,select')) return;
      if (e.key === 'Escape') { if (dersMenu) setDersMenu(false); else onClose(); return; }
      if (e.key === ' ') { e.preventDefault(); oynatDuraklat(); return; }
      if (e.key === 'ArrowRight') { e.preventDefault(); ileri(); return; }
      if (e.key === 'ArrowLeft') { e.preventDefault(); geri(); return; }
      if (s?.tip === 'soru') {
        const harfler = Object.keys(s.a.soru!.secenekler);
        const n = /^[1-9]$/.test(e.key) ? harfler[Number(e.key) - 1] : e.key.toUpperCase();
        if (!cozuldu && harfler.includes(n)) { e.preventDefault(); cevapla(n); return; }
        if (cozuldu && e.key === 'Enter') { e.preventDefault(); ileri(); }
      }
    };
    window.addEventListener('keydown', f);
    return () => window.removeEventListener('keydown', f);
  });
  // tarayıcı tam ekranı
  useEffect(() => {
    const f = () => setTamEkran(!!document.fullscreenElement);
    document.addEventListener('fullscreenchange', f);
    return () => { document.removeEventListener('fullscreenchange', f); if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {}); };
  }, []);
  const tamEkranDegis = () => {
    if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {});
    else (kokRef.current?.closest('.pa') as HTMLElement | null)?.requestFullscreen?.().catch(() => {});
  };
  // kilit ekranı / kulaklık düğmeleri
  useEffect(() => {
    const ms = (navigator as Navigator & { mediaSession?: MediaSession }).mediaSession;
    if (!ms || !ders) return;
    try {
      ms.metadata = new MediaMetadata({ title: s?.tip === 'anlatim' || s?.tip === 'soru' ? s.a.baslik : ders.baslik, artist: 'Patoloji · Sınav asistanı', album: `${ders.no}) ${ders.baslik}` });
      ms.setActionHandler('nexttrack', () => ileri());
      ms.setActionHandler('previoustrack', () => geri());
    } catch { /* desteklenmiyor */ }
  }, [ders, s, ileri, geri]);

  const dersDegis = (k: string) => { durdur(); setDersMenu(false); setKod(k); onDersDegis?.(k); };
  const dizinIdx = dizin.findIndex((d) => d.kod === kod);
  const sonrakiDers = dizinIdx >= 0 ? dizin[dizinIdx + 1] : undefined;

  const ilerlemeAdim = s && (s.tip === 'anlatim' || s.tip === 'soru') ? s.n + 1 : s?.tip === 'kapanis' || s?.tip === 'son' ? adimSayisi : 0;
  const adimListesi = ders ? (tekrar ? ders.adimlar.filter((a) => tekrar.has(a.id)) : ders.adimlar) : [];
  const sahneIdx = (n: number) => sahneler.findIndex((x) => (x.tip === 'anlatim') && x.n === n);
  const sorulu = ders?.adimlar.filter((a) => a.soru) || [];
  const ilkDogru = sorulu.filter((a) => sonuc[a.id] === 'd').length;
  // tekrar listesi: yanlış, ikinci denemede doğru ya da atlanan (cevaplanmadan geçilen) sorular
  const yanlislar = (tekrar ? sorulu.filter((a) => tekrar.has(a.id)) : sorulu).filter((a) => sonuc[a.id] !== 'd');
  const atlanan = yanlislar.filter((a) => !sonuc[a.id]).length;

  const icerik = (
    <div className={`pa${caliyor ? ' is-konusuyor' : ''}`} role="dialog" aria-modal="true" aria-label="Patoloji sesli sınav asistanı">
      <header className="pa-ust">
        <button type="button" className="pa-ikon" onClick={onClose} aria-label="Asistanı kapat"><X /></button>
        <div className="pa-ders">
          <button type="button" className="pa-ders-b" onClick={() => setDersMenu((v) => !v)} aria-expanded={dersMenu} aria-haspopup="listbox">
            <span className="pa-ders-no">{ders?.no ?? '…'}</span>
            <span className="pa-ders-t"><small>Sınav asistanı{tekrar ? ' · yanlışların tekrarı' : ''}</small><b>{ders?.baslik ?? 'Yükleniyor…'}</b></span>
            <ChevronDown aria-hidden />
          </button>
          {dersMenu && (
            <div className="pa-menu" role="listbox" aria-label="Ders seç">
              {dizin.map((d) => (
                <button key={d.kod} type="button" role="option" aria-selected={d.kod === kod} className={d.kod === kod ? 'is-on' : ''} onClick={() => dersDegis(d.kod)}>
                  <span className="pa-menu-no">{d.no}</span>
                  <span className="pa-menu-t"><b>{d.baslik}</b><small>{d.adim} nokta · {d.soru} soru{d.ses ? ` · ${Math.max(1, Math.round(d.sure / 60))} dk` : ' · ses hazırlanıyor'}</small></span>
                </button>
              ))}
            </div>
          )}
        </div>
        <button type="button" className="pa-ikon pa-tam" onClick={tamEkranDegis} aria-label={tamEkran ? 'Tam ekrandan çık' : 'Tam ekran'}>{tamEkran ? <Minimize2 /> : <Maximize2 />}</button>
      </header>

      {ders && (
        <div className="pa-ilerleme" aria-label={`Nokta ${ilerlemeAdim} / ${adimSayisi}`}>
          {adimListesi.map((a, n) => {
            const r = sonuc[a.id];
            const simdi = s && (s.tip === 'anlatim' || s.tip === 'soru') && s.n === n;
            return (
              <button key={a.id} type="button" className={`pa-seg${simdi ? ' is-simdi' : ''}${n < ilerlemeAdim - (simdi ? 1 : 0) ? ' is-gecti' : ''}${r === 'd' ? ' is-d' : r ? ' is-y' : ''}${a.aday ? ' is-aday' : ''}`}
                onClick={() => { const j = sahneIdx(n); if (j >= 0) setI(j); }} aria-label={`${n + 1}. nokta: ${a.baslik}`} title={a.baslik} />
            );
          })}
        </div>
      )}

      <main className="pa-sahne" ref={kokRef}>
        {hata && <div className="pa-bos"><p>Bu ders için asistan henüz hazır değil.</p><button type="button" className="pa-btn" onClick={onClose}>Kapat</button></div>}
        {!hata && !ders && <div className="pa-bos"><span className="pa-dalga is-yukle" aria-hidden><i /><i /><i /><i /><i /></span><p>Asistan hazırlanıyor…</p></div>}

        {ders && devamSor && (
          <div className="pa-kart pa-devam">
            <h2>Kaldığın yerden devam edelim mi?</h2>
            <p>{ders.baslik} dersinde {((sahneleriKur(ders)[devamSor.i] as { n?: number })?.n ?? 0) + 1}. noktadaydın.</p>
            <div className="pa-btnler">
              <button type="button" className="pa-btn is-dolu" onClick={() => { setSonuc(devamSor.sonuc || {}); setI(devamSor.i); setDevamSor(null); }}><Play aria-hidden />Devam et</button>
              <button type="button" className="pa-btn" onClick={() => { setSonuc({}); setI(0); setDevamSor(null); }}><RotateCcw aria-hidden />Baştan başla</button>
            </div>
          </div>
        )}

        {ders && s && !devamSor && (
          <div className="pa-icerik" key={`${tekrar ? 't' : ''}${i}`}>
            <div className="pa-asistan" aria-live="polite">
              <span className="pa-dalga" aria-hidden><i /><i /><i /><i /><i /></span>
              <span className="pa-durum">
                {s.tip === 'soru' && !cozuldu && !secim ? (caliyor ? 'Soruyu okuyor…' : 'Cevabını bekliyor') :
                  s.tip === 'soru' && secim && !cozuldu ? (caliyor ? 'Neden yanlış olduğunu anlatıyor…' : 'Bir daha dene') :
                  caliyor ? 'Anlatıyor…' : sesYok ? 'Metinle ilerliyor (ses hazırlanıyor)' : 'Duraklatıldı'}
              </span>
            </div>

            {s.tip === 'giris' && (
              <section className="pa-kart pa-giris">
                <small className="pa-etiket">{ders.no}. ders · {ders.adimlar.length} nokta · {sorulu.length} soru</small>
                <h1>{ders.baslik}</h1>
                <div className="pa-cumleler">{ders.giris.map((c, j) => <p key={j} className={j === aktifCumle ? 'is-aktif' : ''}><Metin metin={c} /></p>)}</div>
                <p className="pa-kural">Sınav kuralı: tablo, şekil ve klinik bulgu sorulmaz · her slayttan {ders.soruSayisi} soru.</p>
              </section>
            )}

            {s.tip === 'anlatim' && (
              <section className={`pa-kart pa-anlatim${s.a.aday ? ' is-aday' : ''}`}>
                <div className="pa-meta">
                  <span className="pa-puan">{s.a.puan}</span>
                  {s.a.aday && <span className={`pa-aday${s.a.aday <= ders.soruSayisi ? ' is-en' : ''}`}><Star aria-hidden />{s.a.aday <= ders.soruSayisi ? 'En olası soru' : `Sınav adayı ${s.a.aday}`}</span>}
                  {(s.a.kategori === 'prognoz' || s.a.kategori === 'tedavi') && <span className="pa-kat">{s.a.kategori === 'prognoz' ? 'Prognoz' : 'Tedavi'} · sorulabilir</span>}
                  <span className="pa-sayac">{s.n + 1} / {adimSayisi}</span>
                </div>
                <h2>{s.a.baslik}</h2>
                <div className="pa-cumleler">
                  {s.a.cumleler.map((c, j) => <p key={j} className={j === aktifCumle ? 'is-aktif' : j < aktifCumle ? 'is-gecti' : ''}><Metin metin={c} /></p>)}
                </div>
                <div className="pa-hap"><span>Akılda kalsın</span><p><Metin metin={s.a.bilgi} /></p></div>
              </section>
            )}

            {s.tip === 'soru' && (() => {
              const q = s.a.soru!;
              const aciklama = cozuldu ? q.dogruMetin : secim && secim !== q.dogru ? q.yanlis[secim] : null;
              return (
                <section className="pa-kart pa-soru">
                  <div className="pa-meta">
                    <span className="pa-soru-tur">{q.tur === 'cikmis' ? 'Çıkmış soru' : 'Örnek soru'}</span>
                    {q.sinav && <span className="pa-sinav">{q.sinav}</span>}
                    <span className="pa-sayac">{s.n + 1} / {adimSayisi}</span>
                  </div>
                  <h2 className={aktifCumle === 0 && caliyor && !secim ? 'is-aktif' : ''}>{q.kok}</h2>
                  <div className="pa-siklar" role="group" aria-label="Şıklar">
                    {Object.entries(q.secenekler).map(([h, v], n) => {
                      const durum = cozuldu && h === q.dogru ? ' is-dogru' : elenen.includes(h) ? ' is-yanlis' : cozuldu ? ' is-sonuk' : '';
                      return (
                        <button key={h} type="button" className={`pa-sik${durum}${secim === h ? ' is-secili' : ''}`} disabled={!!cozuldu || elenen.includes(h)} onClick={() => cevapla(h)}
                          aria-label={`${h} şıkkı: ${v}`}>
                          <b>{h}</b><span>{v}</span><kbd aria-hidden>{n + 1}</kbd>
                          {cozuldu && h === q.dogru && <Check className="pa-sik-i" aria-hidden />}
                          {elenen.includes(h) && <X className="pa-sik-i" aria-hidden />}
                        </button>
                      );
                    })}
                  </div>
                  {aciklama && (
                    <div className={`pa-geri${cozuldu === 'dogru' ? ' is-dogru' : cozuldu ? ' is-goster' : ' is-yanlis'}`} aria-live="polite">
                      <b>{cozuldu === 'dogru' ? (elenen.length ? 'Doğru, bu sefer oldu!' : 'Doğru!') : cozuldu ? `Doğru cevap ${q.dogru}` : `${secim} neden yanlış?`}</b>
                      <p className={aktifCumle === 0 && caliyor ? 'is-aktif' : ''}><Metin metin={aciklama.replace(/^Doğru!\s*/, '')} /></p>
                    </div>
                  )}
                  <div className="pa-btnler">
                    {!cozuldu && secim && <span className="pa-ipucu">Yanlış şık elendi — başka bir şık seç.</span>}
                    {!cozuldu && <button type="button" className="pa-btn" onClick={dogruyuGoster}>Doğruyu göster</button>}
                    {cozuldu && <button type="button" className="pa-btn is-dolu" onClick={ileri}>Devam<ChevronRight aria-hidden /></button>}
                  </div>
                </section>
              );
            })()}

            {s.tip === 'kapanis' && (
              <section className="pa-kart pa-giris">
                <small className="pa-etiket">Toparlayalım</small>
                <h1>Sınav için akılda kalsın</h1>
                <div className="pa-cumleler">{ders.kapanis.map((c, j) => <p key={j} className={j === aktifCumle ? 'is-aktif' : ''}><Metin metin={c} /></p>)}</div>
              </section>
            )}

            {s.tip === 'son' && (
              <section className="pa-kart pa-son">
                <small className="pa-etiket">{tekrar ? 'Yanlışların tekrarı bitti' : 'Ders bitti'}</small>
                <h1>{ders.baslik}</h1>
                <div className="pa-skor">
                  <div><b>{ilkDogru}</b><span>ilk denemede doğru</span></div>
                  <div><b>{yanlislar.length}</b><span>tekrar etmelisin{atlanan ? ` (${atlanan} atlanan)` : ''}</span></div>
                  <div><b>{sorulu.length}</b><span>soru</span></div>
                </div>
                {yanlislar.length > 0 && (
                  <div className="pa-yanlis-l">
                    <h3>Tekrar etmen gerekenler</h3>
                    <ul>{yanlislar.map((a) => <li key={a.id}><b>{a.baslik}</b><span><Metin metin={a.bilgi} /></span></li>)}</ul>
                  </div>
                )}
                <div className="pa-btnler">
                  {yanlislar.length > 0 && <button type="button" className="pa-btn is-dolu" onClick={() => { setTekrar(new Set(yanlislar.map((a) => a.id))); setI(0); }}><RotateCcw aria-hidden />Yanlışlarımı tekrar et</button>}
                  {ilkDogru > 0 && <button type="button" className="pa-btn" onClick={() => ogrenildiAyarla(sorulu.filter((a) => sonuc[a.id] === 'd').map((a) => a.id), true)}><Check aria-hidden />Doğru bildiklerimi öğrendim say</button>}
                  <button type="button" className="pa-btn" onClick={() => { setTekrar(null); setSonuc({}); setI(0); }}><RotateCcw aria-hidden />Baştan</button>
                  {sonrakiDers && <button type="button" className="pa-btn" onClick={() => dersDegis(sonrakiDers.kod)}>Sonraki ders: {sonrakiDers.no}) {sonrakiDers.baslik}<ChevronRight aria-hidden /></button>}
                </div>
              </section>
            )}
          </div>
        )}
      </main>

      {engel && ders && !devamSor && (
        <button type="button" className="pa-baslat" onClick={() => { setEngel(false); oynatDuraklat(); }}>
          <span><Play aria-hidden /></span><b>Asistanı başlat</b><small>Tarayıcı sesi başlatmak için bir dokunuş istiyor</small>
        </button>
      )}
      {ders && !devamSor && (
        <footer className="pa-alt">
          <div className="pa-oynat">
            <button type="button" className="pa-ikon" onClick={geri} disabled={i === 0} aria-label="Önceki"><ChevronLeft /></button>
            <button type="button" className="pa-buyuk" onClick={oynatDuraklat} aria-label={caliyor ? 'Duraklat' : 'Oynat'}>{caliyor ? <Pause /> : <Play />}</button>
            <button type="button" className="pa-ikon" onClick={ileri} disabled={i >= sahneler.length - 1} aria-label={s?.tip === 'soru' && !cozuldu ? 'Soruyu atla' : 'Sonraki'}>{s?.tip === 'soru' && !cozuldu ? <SkipForward /> : <ChevronRight />}</button>
          </div>
          <div className="pa-ayar">
            <label className="pa-sec" title="Konuşma hızı">
              <Volume2 aria-hidden />
              <select value={tercih.hiz} onChange={(e) => setTercih({ hiz: Number(e.target.value) })} aria-label="Konuşma hızı">
                {HIZLAR.map((h) => <option key={h} value={h}>{h.toLocaleString('tr-TR')}×</option>)}
              </select>
            </label>
            <label className="pa-oto">
              <input type="checkbox" checked={tercih.otomatik} onChange={(e) => setTercih({ otomatik: e.target.checked })} />
              <span>Otomatik geç</span>
            </label>
          </div>
        </footer>
      )}
    </div>
  );
  return createPortal(icerik, document.body);
};

export default PatolojiAsistan;
