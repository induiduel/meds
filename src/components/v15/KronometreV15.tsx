import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { BarChart3, Flag, Pause, Play, RotateCcw, Settings, Square, Timer, X } from 'lucide-react';
import KronometreEkranV15, { ayarOku, KR_AYAR_KEY, type KrAyar } from './KronometreEkranV15';
import KapsulV15, { kapsulOku, KAPSUL_KEY } from './KapsulV15';
import '../../styles/v15/kronometre.css';

/**
 * v15 · Yüzen kronometre (tasarım sistemi v15 › T "Yüzen kronometre" + U "Çalışma kapsülü").
 * - Tek örnek: uygulama kökünde (App) bir kez bağlanır, odak ekranları dahil her sayfada kalır; Odak (hedef süreli
 *   oturum) aynı panelin sekmesidir, ikinci baloncuk yoktur. Biri başlayınca öteki duraklar (`medsoru:sayac`).
 * - Zar baloncuğu: dakika:saniye, ilerleme halkası, nabız atan çekirdek; duraklatılınca soluk.
 * - Hareketler: dokun → panel · uzun bas → başlat/duraklat · iki kez dokun → tur · sürükle → kenara yapışır ·
 *   kenardan dışarı it → yarım baloncuk olarak gizlenir. Konum cihazda saklanır.
 * - Sesli ders oynatıcısı açıkken baloncuk oynatıcının sağ ucuna kaynaşır (zar boynu), kapanınca serbest konumuna döner.
 * Sistemin ölçtüğü çalışma süresine (calismaTakip) karışmaz. Durum localStorage'da; sekmeler arası eşitlenir.
 */
const KEY = 'medsoru_v15_kronometre';
const KONUM_KEY = 'medsoru_v15_kronometre_konum';
interface Durum { acik: boolean; calisiyor: boolean; bas: number; birikmis: number; turlar: number[]; gecmis: { t: string; sn: number; tur: number; ad?: string }[] }
interface Konum { sag: boolean; y: number; gizli: boolean }
const BOS: Durum = { acik: false, calisiyor: false, bas: 0, birikmis: 0, turlar: [], gecmis: [] };
const oku = (): Durum => { try { return { ...BOS, ...JSON.parse(localStorage.getItem(KEY) || '{}') }; } catch { return BOS; } };
const yaz = (d: Durum) => { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch { /* özel pencere */ } };
const konumOku = (): Konum => { try { return { sag: true, y: 0.72, gizli: false, ...JSON.parse(localStorage.getItem(KONUM_KEY) || '{}') }; } catch { return { sag: true, y: 0.72, gizli: false }; } };
const gecen = (d: Durum, simdi = Date.now()) => d.birikmis + (d.calisiyor ? simdi - d.bas : 0);
export const sureYaz = (ms: number) => {
  const s = Math.floor(ms / 1000), sa = Math.floor(s / 3600), dk = Math.floor((s % 3600) / 60), sn = s % 60;
  const p = (n: number) => String(n).padStart(2, '0');
  return sa ? `${sa}:${p(dk)}:${p(sn)}` : `${p(dk)}:${p(sn)}`;
};
/** Menü ve kenar menüsünden açmak için */
export const kronometreAc = () => window.dispatchEvent(new CustomEvent('medsoru:kronometre', { detail: 'kronometre' }));

const BOY_ORTA = 48, BOY_KUCUK = 38;
/** Oturuma ad: o an açık sayfanın başlığı ("Patoloji 3 · … · MeDSor" → ilk parça) */
const sayfaAdi = () => { const p = document.title.split(' · ').filter((x) => x && x !== 'MeDSor'); return p[0]?.slice(0, 60) || 'Kronometre'; };
/** Sesli ders oynatıcısı (mini ya da tam) — baloncuk ona kaynaşır */
const yuva = () => document.querySelector<HTMLElement>('.cd-dock');

export default function KronometreV15() {
  const [d, setD0] = useState<Durum>(oku);
  const [panel, setPanel] = useState(false);
  const [sekme, setSekme] = useState<'kronometre' | 'odak'>('kronometre');
  const [konum, setKonum0] = useState<Konum>(konumOku);
  const [surukle, setSurukle] = useState<{ x: number; y: number } | null>(null);
  const [kaynak, setKaynak] = useState<DOMRect | null>(null);
  const [, tik] = useState(0);
  const [ayar, setAyar0] = useState<KrAyar>(ayarOku);
  const [ekran, setEkran] = useState<'ayar' | 'gecmis' | null>(null);
  const setAyar = (a: KrAyar) => { if (a.sag !== ayar.sag) setKonum({ ...konum, sag: a.sag, y: 0.72, gizli: false }); setAyar0(a); try { localStorage.setItem(KR_AYAR_KEY, JSON.stringify(a)); } catch { /* yok */ } };
  const molaUyari = useRef(0);
  const BOY = ayar.boyut === 'kucuk' ? BOY_KUCUK : BOY_ORTA;
  const setD = (f: (x: Durum) => Durum) => setD0((x) => { const n = f(x); yaz(n); return n; });
  const setKonum = (k: Konum) => { setKonum0(k); try { localStorage.setItem(KONUM_KEY, JSON.stringify(k)); } catch { /* yok */ } };
  const bas = useRef<{ x: number; y: number; t: number; tasindi: boolean; uzun: number } | null>(null);
  const sonDokun = useRef(0);
  const tekTimer = useRef(0);

  useEffect(() => {
    const ac = (e: Event) => {
      setD((x) => ({ ...x, acik: true }));
      setSekme((e as CustomEvent).detail === 'odak' ? 'odak' : 'kronometre');
      setKonum0((k) => ({ ...k, gizli: false }));
      setPanel(true);
    };
    const st = (e: StorageEvent) => { if (e.key === KEY) setD0(oku()); if (e.key === KR_AYAR_KEY) setAyar0(ayarOku()); if (e.key === KAPSUL_KEY) tik((n) => n + 1); };
    // odak başlayınca kronometre duraklar (aynı anda tek sayaç)
    const sayac = (e: Event) => { if ((e as CustomEvent).detail === 'odak') setD((x) => ({ ...x, acik: true, ...(x.calisiyor ? { calisiyor: false, birikmis: gecen(x), bas: 0 } : {}) })); };
    window.addEventListener('medsoru:kronometre', ac);
    window.addEventListener('medsoru:sayac', sayac);
    window.addEventListener('storage', st);
    return () => { window.removeEventListener('medsoru:kronometre', ac); window.removeEventListener('medsoru:sayac', sayac); window.removeEventListener('storage', st); };
  }, []);

  const odak = kapsulOku();
  const sayiyor = d.calisiyor || !!odak?.calisiyor;
  useEffect(() => {
    if (!d.acik) return;
    const id = window.setInterval(() => tik((n) => n + 1), sayiyor ? 1000 : 4000);
    return () => window.clearInterval(id);
  }, [d.acik, sayiyor]);

  // Sesli ders oynatıcısını izle: varsa konumunu al (kaynaşma)
  useEffect(() => {
    if (!d.acik) return;
    let son = '';
    const bak = () => {
      const el = yuva();
      const r = el && el.offsetHeight ? el.getBoundingClientRect() : null;
      const imza = r ? `${Math.round(r.left)},${Math.round(r.top)},${Math.round(r.width)},${Math.round(r.height)}` : '';
      if (imza !== son) { son = imza; setKaynak(r); }
    };
    bak();
    const id = window.setInterval(bak, 400);
    window.addEventListener('resize', bak);
    return () => { window.clearInterval(id); window.removeEventListener('resize', bak); };
  }, [d.acik]);

  // kaynaşınca mini oynatıcı sağ ucunda baloncuğa yer açar
  const kaynasma = d.acik && ayar.birles && !!kaynak && kaynak.height < 110;
  useEffect(() => {
    document.documentElement.classList.toggle('kr-kaynasik', kaynasma);
    return () => document.documentElement.classList.remove('kr-kaynasik');
  }, [kaynasma]);

  // "Sayfa değişince çalışmaya devam et" kapalıysa adres değişiminde duraklar
  useEffect(() => {
    if (ayar.devam || !d.calisiyor) return;
    let yol = location.pathname;
    const id = window.setInterval(() => {
      if (location.pathname !== yol) { yol = location.pathname; setD((x) => (x.calisiyor ? { ...x, calisiyor: false, birikmis: gecen(x), bas: 0 } : x)); }
    }, 500);
    return () => window.clearInterval(id);
  }, [ayar.devam, d.calisiyor]);

  if (!d.acik) return null;

  const ms = gecen(d);
  // Mola hatırlatması: kesintisiz çalışma eşiği geçince baloncuk uyarı rengine döner, bir kez titrer
  const kesintisiz = d.calisiyor ? Date.now() - d.bas : 0;
  const molaZamani = ayar.molaDk > 0 && kesintisiz >= ayar.molaDk * 60000;
  if (molaZamani && molaUyari.current !== d.bas) { molaUyari.current = d.bas; navigator.vibrate?.([30, 60, 30]); }
  const baslat = () => {
    if (!d.calisiyor) window.dispatchEvent(new CustomEvent('medsoru:sayac', { detail: 'kronometre' }));
    setD((x) => (x.calisiyor ? { ...x, calisiyor: false, birikmis: gecen(x), bas: 0 } : { ...x, calisiyor: true, bas: Date.now() }));
  };
  const tur = () => setD((x) => (gecen(x) ? { ...x, turlar: [...x.turlar, gecen(x)].slice(-30) } : x));
  const sifirla = () => setD((x) => {
    const sn = Math.round(gecen(x) / 1000);
    return { ...x, calisiyor: false, bas: 0, birikmis: 0, turlar: [], gecmis: sn ? [{ t: new Date().toISOString(), sn, tur: x.turlar.length, ad: sayfaAdi() }, ...x.gecmis].slice(0, 200) : x.gecmis };
  });
  const kapat = () => { sifirla(); setPanel(false); setD((x) => ({ ...x, acik: false })); };
  const bugun = new Date().toDateString();
  const bugunSn = d.gecmis.filter((g) => new Date(g.t).toDateString() === bugun).reduce((a, g) => a + g.sn, 0) + Math.round(ms / 1000);

  // Baloncukta odak geri sayımı önceliklidir (çalışıyorsa); yoksa kronometre
  const odakGoster = !!odak && (odak.calisiyor || !d.calisiyor && !ms);
  const yazi = odakGoster ? sureYaz(odak!.kalan) : sureYaz(ms);
  const halka = odakGoster ? odak!.oran : ((ms / 1000) % 60) / 60;
  const calisiyorGor = odakGoster ? odak!.calisiyor : d.calisiyor;

  // ---- konum ----
  const vw = window.innerWidth, vh = window.innerHeight;
  const tasarim = kaynak && !surukle;
  let stil: React.CSSProperties;
  if (surukle) stil = { left: surukle.x - BOY / 2, top: surukle.y - BOY / 2 };
  else if (kaynak && ayar.birles) {
    const mini = kaynak.height < 110;
    stil = mini
      ? { left: Math.min(vw - BOY - 6, kaynak.right - BOY - 6), top: kaynak.top + kaynak.height / 2 - BOY / 2 }
      : { left: Math.min(vw - BOY - 8, kaynak.right - BOY - 8), top: kaynak.top - BOY - 10 };
  } else {
    const top = Math.max(70, Math.min(vh - BOY - 80, konum.y * vh));
    const kenar = konum.gizli ? -BOY / 2 : 12;
    stil = konum.sag ? { right: kenar, top } : { left: kenar, top };
  }
  const kaynasik = !!tasarim && ayar.birles && kaynak!.height < 110;

  const indir = (e: React.PointerEvent) => {
    if (e.button !== 0) return;
    (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
    bas.current = { x: e.clientX, y: e.clientY, t: Date.now(), tasindi: false, uzun: window.setTimeout(() => { if (bas.current && !bas.current.tasindi) { bas.current.tasindi = true; baslat(); navigator.vibrate?.(20); } }, 550) };
  };
  const hareket = (e: React.PointerEvent) => {
    const b = bas.current; if (!b) return;
    if (!b.tasindi && Math.hypot(e.clientX - b.x, e.clientY - b.y) > 8) { b.tasindi = true; window.clearTimeout(b.uzun); }
    if (b.tasindi && Date.now() - b.t > 0 && Math.hypot(e.clientX - b.x, e.clientY - b.y) > 8) setSurukle({ x: e.clientX, y: e.clientY });
  };
  const birak = (e: React.PointerEvent) => {
    const b = bas.current; bas.current = null; if (!b) return;
    window.clearTimeout(b.uzun);
    if (surukle) {
      const x = e.clientX;
      setSurukle(null);
      setKonum({ sag: x > vw / 2, y: Math.max(0.1, Math.min(0.9, e.clientY / vh)), gizli: x < 6 || x > vw - 6 });
      return;
    }
    if (b.tasindi) return;
    if (konum.gizli && !(kaynak && ayar.birles)) { setKonum({ ...konum, gizli: false }); return; }
    const simdi = Date.now();
    if (simdi - sonDokun.current < 300) { window.clearTimeout(tekTimer.current); sonDokun.current = 0; tur(); navigator.vibrate?.(10); return; }
    sonDokun.current = simdi;
    tekTimer.current = window.setTimeout(() => setPanel((p) => !p), 260);
  };

  // panel konumu: baloncuğun yanında, ekranda kalacak biçimde
  const balonSol = typeof stil.left === 'number' ? stil.left : vw - (stil.right as number) - BOY;
  const balonUst = stil.top as number;
  const panelGen = Math.min(300, vw - 24);
  const panelStil: React.CSSProperties = { left: Math.max(12, Math.min(vw - panelGen - 12, balonSol + BOY - panelGen)), width: panelGen };
  if (balonUst > vh / 2) panelStil.bottom = vh - balonUst + 10; else panelStil.top = balonUst + BOY + 10;

  const R = 66, CEVRE = 2 * Math.PI * R;
  return createPortal(
    <>
      {panel && <div className="krp15-perde" onClick={() => setPanel(false)} aria-hidden />}
      {panel && (
        <div className="krp15" style={panelStil} role="dialog" aria-label="Kronometre">
          <div className="krp15-ust">
            <div className="v15-seg krp15-seg" role="tablist" aria-label="Sayaç türü">
              <button type="button" role="tab" aria-selected={sekme === 'kronometre'} aria-current={sekme === 'kronometre' ? 'page' : undefined} onClick={() => setSekme('kronometre')}>Kronometre</button>
              <button type="button" role="tab" aria-selected={sekme === 'odak'} aria-current={sekme === 'odak' ? 'page' : undefined} onClick={() => setSekme('odak')}>Odak</button>
            </div>
            <button type="button" className="v15-ib" onClick={() => setPanel(false)} aria-label="Küçült"><X aria-hidden /></button>
          </div>
          {sekme === 'kronometre' ? (
            <>
              <div className="krp15-halka">
                <svg viewBox="0 0 150 150" aria-hidden>
                  <circle cx="75" cy="75" r={R} fill="none" className="krp15-iz" strokeWidth="6" />
                  <circle cx="75" cy="75" r={R} fill="none" className="krp15-dolu" strokeWidth="6" strokeLinecap="round"
                    strokeDasharray={CEVRE} strokeDashoffset={CEVRE * (1 - ((ms / 1000) % 60) / 60)} transform="rotate(-90 75 75)" />
                </svg>
                <b className="krp15-zaman" aria-live="off">{sureYaz(ms)}<small>.{Math.floor((ms % 1000) / 100)}</small></b>
              </div>
              <div className="krp15-dug">
                <button type="button" className="v15-ib" onClick={sifirla} disabled={!ms} aria-label="Sıfırla" title="Sıfırla"><RotateCcw aria-hidden /></button>
                <button type="button" className="v15-ib krp15-pl" onClick={baslat} aria-label={d.calisiyor ? 'Duraklat' : ms ? 'Sürdür' : 'Başlat'}>{d.calisiyor ? <Pause aria-hidden /> : <Play aria-hidden />}</button>
                <button type="button" className="v15-ib" onClick={tur} disabled={!ms} aria-label="Tur" title="Tur"><Flag aria-hidden /></button>
              </div>
              {d.turlar.length > 0 && (
                <ol className="krp15-tur">
                  {d.turlar.map((t, i) => <li key={i}><span>Tur {i + 1}</span><b>{sureYaz(t - (d.turlar[i - 1] || 0))}</b></li>).reverse()}
                </ol>
              )}
              <div className="krp15-alt">
                <span>Bugün kronometre: {sureYaz(bugunSn * 1000)}</span>
                <span className="krp15-alt-d">
                  <button type="button" onClick={() => setEkran('gecmis')} aria-label="Kronometre geçmişi" title="Geçmiş"><BarChart3 aria-hidden /></button>
                  <button type="button" onClick={() => setEkran('ayar')} aria-label="Kronometre ayarları" title="Ayarlar"><Settings aria-hidden /></button>
                  <button type="button" onClick={kapat}><Square aria-hidden /> Kapat</button>
                </span>
              </div>
            </>
          ) : (
            <KapsulV15 gomulu />
          )}
          <p className="v15-cap krp15-not">Dokun: aç · uzun bas: başlat/duraklat · iki kez dokun: tur · sürükle: kenara yapışır.</p>
        </div>
      )}
      {ekran && <KronometreEkranV15 gorunum={ekran} ayar={ayar} setAyar={setAyar} gecmis={d.gecmis} onKapat={() => setEkran(null)} />}
      {(ayar.goster || panel) && <div
        className={`kr15z${ayar.boyut === 'kucuk' ? ' is-kucuk' : ''}${molaZamani ? ' is-uyari' : ''}${calisiyorGor ? '' : ' is-dur'}${kaynasik ? ' is-kaynasik' : ''}${konum.gizli && !kaynak ? ' is-gizli' : ''}${surukle ? ' is-surukle' : ''}`}
        style={{ ...stil, ['--s' as string]: `${Math.round(halka * 100)}%` }}
        role="timer"
        aria-label={`${odakGoster ? 'Odak, kalan' : 'Kronometre'} ${yazi}. Dokun: aç, uzun bas: başlat veya duraklat`}
        tabIndex={0}
        onPointerDown={indir} onPointerMove={hareket} onPointerUp={birak}
        onPointerCancel={() => { if (bas.current) window.clearTimeout(bas.current.uzun); bas.current = null; setSurukle(null); }}
        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setPanel((p) => !p); } }}
      >
        {kaynasik && <span className="kr15z-boyun" aria-hidden />}
        <span className="kr15z-zar" aria-hidden />
        <span className="kr15z-cek" aria-hidden />
        {ms || odakGoster ? <span className="kr15z-zm">{yazi}</span> : <Timer className="kr15z-ik" aria-hidden />}
      </div>}
    </>,
    document.body,
  );
}
