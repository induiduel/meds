import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  Check, ChevronDown, ChevronLeft, ChevronRight, Eraser, Headphones, Lightbulb, Maximize2, Minimize2, Pause, Play, RotateCcw, Settings2, SkipForward, Volume2, X,
} from 'lucide-react';
import { getCustomApiUrl } from '../../../services/api';
import { lockScroll, unlockScroll } from '../../../utils/scrollLock';
import { Metin } from '../onem/OnemMadde';
import {
  HARFLER, TERCIH_KEY, cozucuDersYukle, cozucuDizinYukle, ilerlemeOku, ilerlemeYaz,
  type CDers, type CDizin, type CSoru, type Harf, type Sonuc,
} from './cozucuVeri';
import '../../../styles/soru-cozucu.css';

/**
 * Patoloji · Sesli soru çözücü (tam ekran). Anlatım yok, yalnız soru: asistan kökü ve şıkları okur, öğrenci şık seçer.
 *  - Yanlış seçim → "Yanlış." + o şıkkın neden yanlış olduğu (şık elenir), yeniden dener.
 *  - Doğru seçim → "Doğru!" + çözüm; otomatik geçiş açıksa sonraki soru.
 *  - Yardım: İpucu (cevabı söylemez) · Bir yanlışı ele (rastgele yanlış şık açıklanıp elenir) · Çözümü dinle (her şık sırayla
 *    vurgulanıp açıklanır, sonra "Doğru cevap …" + çözüm).
 * Çözülen soruda şıka dokunmak o şıkkın açıklamasını okur. Ses yoksa okuma süresiyle ilerler (metin yine görünür).
 */

/** mod: yanlis = yalnız yanlış/yardımlı çözülenler · cikmis = yalnız çıkmış sorular (ikisinde de konum kaydedilmez) */
interface Props { kod: string; onClose: () => void; onDersDegis?: (kod: string) => void; mod?: 'yanlis' | 'cikmis' }
type Durum = 'acik' | 'cozuluyor' | 'dogru' | 'gosterildi';
interface Adim { klasor: string; klip: string; metinler: string[]; onBasla?: () => void; onCumle?: (j: number) => void; kes?: number }
const HIZLAR = [0.85, 1, 1.15, 1.3, 1.5, 1.75, 2];
const HARF_SES: Record<Harf, string> = { A: 'A', B: 'Be', C: 'Ce', D: 'De', E: 'E' };
const kelimeSay = (s: string) => (s.match(/\S+/g) || []).length;
const azHareket = () => typeof window !== 'undefined' && !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
const tercihOku = () => {
  const v = { hiz: 1, siklariOku: true, otomatik: true };
  try { return { ...v, ...JSON.parse(localStorage.getItem(TERCIH_KEY) || '{}') }; } catch { return v; }
};

export const SoruCozucu: React.FC<Props> = ({ kod: kod0, onClose, onDersDegis, mod }) => {
  const [kod, setKod] = useState(kod0);
  const [dizin, setDizin] = useState<CDizin | null>(null);
  const [ders, setDers] = useState<CDers | null>(null);
  const [hata, setHata] = useState(false);
  const [liste, setListe] = useState<number[] | null>(null); // gösterilen soruların no'ları (tekrar modunda süzülü)
  const [tekrar, setTekrar] = useState(false);
  const [i, setI] = useState(0);
  const [bitti, setBitti] = useState(false);
  const [sonuc, setSonuc] = useState<Record<string, Sonuc>>({});
  const [devamSor, setDevamSor] = useState<number | null>(null);
  const [tercih, setTercih0] = useState(tercihOku);
  const setTercih = (p: Partial<ReturnType<typeof tercihOku>>) => setTercih0((t: ReturnType<typeof tercihOku>) => {
    const n = { ...t, ...p }; try { localStorage.setItem(TERCIH_KEY, JSON.stringify(n)); } catch { /* özel pencere */ } return n;
  });
  // ses
  const [caliyor, setCaliyor] = useState(false);
  const [sesYok, setSesYok] = useState(false);
  const [engel, setEngel] = useState(false);
  const [dersMenu, setDersMenu] = useState(false);
  const [ayarAcik, setAyarAcik] = useState(false);
  const [tamEkran, setTamEkran] = useState(false);
  // soru durumu
  const [durum, setDurum] = useState<Durum>('acik');
  const [elenen, setElenen] = useState<Harf[]>([]);
  const [aciklanan, setAciklanan] = useState<Harf[]>([]);
  const [ipucuAcik, setIpucuAcik] = useState(false);
  const [yardim, setYardim] = useState(false); // bu soruda yardım ya da yanlış deneme oldu
  const [sonSecim, setSonSecim] = useState<Harf | null>(null);
  const [yanlisSecti, setYanlisSecti] = useState(false);
  const [okunan, setOkunan] = useState<{ yer: 'kok' | 'sik' | 'ipucu' | 'aciklama' | 'cozum'; h?: Harf; j?: number } | null>(null);

  const audio = useRef<HTMLAudioElement | null>(null);
  const zamanlayici = useRef<number | null>(null);
  const siraRef = useRef(0); // her yeni sıra eskisini geçersiz kılar
  const otoRef = useRef<number | null>(null);
  const kokRef = useRef<HTMLDivElement>(null);
  const devamRef = useRef<(() => void) | null>(null); // duraklatılan sıranın kalanı

  const sorular = useMemo(() => {
    if (!ders) return [];
    return liste ? ders.sorular.filter((q) => liste.includes(q.no)) : ders.sorular;
  }, [ders, liste]);
  const q: CSoru | undefined = sorular[i];

  useEffect(() => { lockScroll(); return () => unlockScroll(); }, []);
  useEffect(() => { cozucuDizinYukle().then(setDizin).catch(() => {}); }, []);
  useEffect(() => {
    let canli = true;
    setDers(null); setHata(false); setListe(null); setTekrar(false); setI(0); setBitti(false); setDevamSor(null);
    cozucuDersYukle(kod).then((d) => {
      if (!canli) return;
      const k = ilerlemeOku()[kod];
      setSonuc(k?.s || {});
      const kalinan = k ? (k.q !== undefined ? d.sorular.findIndex((x) => x.no === k.q) : k.i) : -1;
      if (mod === 'yanlis' && k) {
        const y = d.sorular.filter((x) => k.s[x.no] && k.s[x.no] !== 'd').map((x) => x.no);
        if (y.length) { setListe(y); setTekrar(true); }
      } else if (mod === 'cikmis') {
        const c = d.sorular.filter((x) => x.tur === 'cikmis').map((x) => x.no);
        if (c.length) { setListe(c); setTekrar(true); }
      } else if (k && kalinan > 0 && kalinan < d.sorular.length && Object.keys(k.s).length < d.sorular.length) setDevamSor(kalinan);
      setDers(d);
    }).catch(() => canli && setHata(true));
    return () => { canli = false; };
  }, [kod, mod]);
  // ilerleme: tam akışta konum + sonuçlar; tekrar modunda yalnız sonuçlar
  useEffect(() => {
    if (!ders || devamSor !== null) return;
    // ders.kod: ders değişirken bu etki eski dersin durumuyla bir kez daha çalışır; kayıt yine eski derse gider
    ilerlemeYaz(ders.kod, tekrar ? { s: sonuc } : { s: sonuc, i: bitti ? 0 : i, q: bitti ? undefined : sorular[i]?.no });
  }, [sonuc, i, bitti, ders, tekrar, devamSor, sorular]);

  // ---------- ses motoru: adımlar sırayla; her adım bir klip (yoksa okuma süresi)
  const durdur = useCallback(() => {
    siraRef.current++;
    devamRef.current = null;
    const a = audio.current;
    if (a) { a.onended = null; a.ontimeupdate = null; a.onerror = null; a.pause(); }
    if (zamanlayici.current) { window.clearInterval(zamanlayici.current); zamanlayici.current = null; }
    setCaliyor(false);
  }, []);
  const klipBilgi = useCallback((klasor: string, klip: string) => {
    if (klasor === 'ortak') { const o = dizin?.ortak[klip]; return o ? { v: o.v, sure: o.sure, zaman: [] as [number, number][] } : undefined; }
    return ders?.klip[klip];
  }, [ders, dizin]);
  const calSira = useCallback((adimlar: Adim[], bitince?: () => void) => {
    durdur();
    const sira = siraRef.current;
    const hiz = tercih.hiz;
    const adim = (n: number) => {
      if (sira !== siraRef.current) return;
      if (n >= adimlar.length) { setCaliyor(false); setOkunan(null); bitince?.(); return; }
      const a = adimlar[n];
      a.onBasla?.();
      a.onCumle?.(0);
      const sonraki = () => { if (sira === siraRef.current) adim(n + 1); };
      const k = klipBilgi(a.klasor, a.klip);
      const yedek = () => {
        setSesYok(true);
        const sureler = a.metinler.slice(0, a.kes !== undefined ? a.kes + 1 : undefined).map((c) => Math.max(1.2, kelimeSay(c) / 2.6) / hiz);
        let j = 0; let t = 0;
        setCaliyor(true);
        if (zamanlayici.current) window.clearInterval(zamanlayici.current);
        zamanlayici.current = window.setInterval(() => {
          if (sira !== siraRef.current) return;
          t += 0.1;
          if (t >= sureler[j]) {
            t = 0; j++;
            if (j >= sureler.length) { window.clearInterval(zamanlayici.current!); zamanlayici.current = null; sonraki(); return; }
            a.onCumle?.(j);
          }
        }, 100);
      };
      if (!k) { yedek(); return; }
      setSesYok(false);
      if (!audio.current) audio.current = new Audio();
      const el = audio.current;
      el.src = `${getCustomApiUrl() || ''}/api/patoloji-cozucu/ses/${encodeURIComponent(a.klasor)}/${encodeURIComponent(a.klip)}.mp3?v=${k.v}`;
      el.playbackRate = hiz;
      try { (el as HTMLAudioElement & { preservesPitch?: boolean }).preservesPitch = true; } catch { /* eski tarayıcı */ }
      const kesSn = a.kes !== undefined && k.zaman[a.kes] ? k.zaman[a.kes][1] + 0.15 : Infinity;
      let son = 0;
      el.ontimeupdate = () => {
        const t = el.currentTime;
        if (t >= kesSn) { el.ontimeupdate = null; el.onended = null; el.pause(); sonraki(); return; }
        let j = k.zaman.findIndex(([b, e]) => t >= b - 0.05 && t < e + 0.4);
        if (j < 0) j = k.zaman.filter(([b]) => b <= t).length - 1;
        j = Math.max(0, j);
        if (j !== son) { son = j; a.onCumle?.(j); }
      };
      el.onended = () => { el.onended = null; sonraki(); };
      el.onerror = () => { el.onerror = null; yedek(); };
      el.play().then(() => { if (sira === siraRef.current) { setCaliyor(true); setEngel(false); } }).catch((e) => {
        if (sira !== siraRef.current) return;
        setCaliyor(false);
        if (e?.name === 'NotAllowedError') { setEngel(true); devamRef.current = () => adim(n); }
      });
    };
    adim(0);
  }, [durdur, klipBilgi, tercih.hiz]);
  useEffect(() => () => { durdur(); if (otoRef.current) window.clearTimeout(otoRef.current); }, [durdur]);
  useEffect(() => { if (audio.current) audio.current.playbackRate = tercih.hiz; }, [tercih.hiz]);

  // ---------- adım kurucular
  const kokAdimi = useCallback((s: CSoru, siklar: boolean): Adim => ({
    klasor: kod, klip: `q-${s.no}`, metinler: [s.soru, ...HARFLER.map((h) => `${HARF_SES[h]}, ${s.secenekler[h]}`)],
    kes: siklar ? undefined : 0,
    onCumle: (j) => setOkunan(j === 0 ? { yer: 'kok' } : { yer: 'sik', h: HARFLER[j - 1] }),
  }), [kod]);
  const sikAdimi = useCallback((s: CSoru, h: Harf, onBasla?: () => void): Adim => ({
    klasor: kod, klip: `s-${s.no}-${h}`, metinler: [s.siklar[h]],
    onBasla, onCumle: (j) => setOkunan({ yer: 'aciklama', h, j }),
  }), [kod]);

  const ileri = useCallback(() => {
    if (otoRef.current) { window.clearTimeout(otoRef.current); otoRef.current = null; }
    if (i >= sorular.length - 1) { durdur(); setBitti(true); } else setI(i + 1);
  }, [i, sorular.length, durdur]);
  const geri = useCallback(() => {
    if (otoRef.current) { window.clearTimeout(otoRef.current); otoRef.current = null; }
    if (bitti) setBitti(false); else setI((x) => Math.max(0, x - 1));
  }, [bitti]);

  // soru değişince: durumu sıfırla, soruyu oku
  useEffect(() => {
    if (otoRef.current) { window.clearTimeout(otoRef.current); otoRef.current = null; }
    if (!ders || !q || devamSor !== null || bitti) { if (bitti) durdur(); return; }
    setDurum('acik'); setElenen([]); setAciklanan([]); setIpucuAcik(false); setYardim(false); setSonSecim(null); setYanlisSecti(false); setOkunan(null);
    kokRef.current?.scrollTo({ top: 0, behavior: azHareket() ? 'auto' : 'smooth' });
    calSira([kokAdimi(q, tercih.siklariOku)]);
  }, [i, ders, sorular, devamSor, bitti]); // eslint-disable-line react-hooks/exhaustive-deps

  const kaydir = (sec: string) => requestAnimationFrame(() => requestAnimationFrame(() =>
    kokRef.current?.querySelector(sec)?.scrollIntoView({ block: 'nearest', behavior: azHareket() ? 'auto' : 'smooth' })));
  const sonucYaz = (no: number, r: Sonuc) => setSonuc((x) => ({ ...x, [no]: r }));
  const acikla = (h: Harf) => setAciklanan((a) => (a.includes(h) ? a : [...a, h]));
  const ele = (h: Harf) => setElenen((e) => (e.includes(h) ? e : [...e, h]));

  const cevapla = (h: Harf) => {
    if (!q) return;
    if (durum === 'dogru' || durum === 'gosterildi') { // çözülmüş soruda: şıkkın açıklamasını dinle
      acikla(h); calSira([sikAdimi(q, h)]); kaydir('.sc-aciklamalar'); return;
    }
    if (durum !== 'acik' || elenen.includes(h)) return;
    setSonSecim(h);
    if (h === q.dogru) {
      setDurum('dogru');
      sonucYaz(q.no, yardim || elenen.length ? 'd2' : 'd');
      calSira([{ klasor: kod, klip: `d-${q.no}`, metinler: ['Doğru!', q.cozum], onCumle: (j) => setOkunan(j > 0 ? { yer: 'cozum' } : null) }], () => {
        if (tercih.otomatik) otoRef.current = window.setTimeout(() => { otoRef.current = null; ileri(); }, 900);
      });
      kaydir('.sc-cozum');
    } else {
      setYardim(true); setYanlisSecti(true); ele(h); acikla(h);
      calSira([
        { klasor: 'ortak', klip: 'yanlis', metinler: ['Yanlış.'] },
        sikAdimi(q, h),
      ]);
      kaydir('.sc-aciklamalar');
    }
  };
  const ipucu = () => {
    if (!q || durum !== 'acik') return;
    setIpucuAcik(true); setYardim(true);
    calSira([{ klasor: kod, klip: `i-${q.no}`, metinler: [q.ipucu], onCumle: () => setOkunan({ yer: 'ipucu' }) }]);
    kaydir('.sc-ipucu');
  };
  const kalanYanlis = q ? HARFLER.filter((h) => h !== q.dogru && !elenen.includes(h)) : [];
  const birYanlisEle = () => {
    if (!q || durum !== 'acik' || !kalanYanlis.length) return;
    const h = kalanYanlis[Math.floor(Math.random() * kalanYanlis.length)];
    setYardim(true); ele(h); acikla(h);
    calSira([sikAdimi(q, h)]);
    kaydir('.sc-aciklamalar');
  };
  const cozumuDinle = () => {
    if (!q || durum === 'dogru' || durum === 'gosterildi') return;
    setDurum('cozuluyor'); setYardim(true);
    sonucYaz(q.no, 'y');
    const adimlar: Adim[] = HARFLER.filter((h) => !aciklanan.includes(h) || h === q.dogru).map((h) => sikAdimi(q, h, () => {
      acikla(h); if (h !== q.dogru) ele(h); kaydir('.sc-aciklamalar');
    }));
    adimlar.push({
      klasor: kod, klip: `c-${q.no}`, metinler: [`Doğru cevap ${q.dogru}, ${q.secenekler[q.dogru]}.`, q.cozum],
      onBasla: () => { setDurum('gosterildi'); setSonSecim(q.dogru); setElenen(HARFLER.filter((x) => x !== q.dogru)); kaydir('.sc-cozum'); },
      onCumle: (j) => setOkunan(j > 0 ? { yer: 'cozum' } : null),
    });
    // çözüm bitince (otomatik geçiş açıksa) sonraki soruya
    calSira(adimlar, () => {
      if (tercih.otomatik) otoRef.current = window.setTimeout(() => { otoRef.current = null; ileri(); }, 1400);
    });
  };
  const tekrarOku = () => { if (q) calSira([kokAdimi(q, true)]); };
  const oynatDuraklat = () => {
    const a = audio.current;
    if (caliyor) {
      if (zamanlayici.current) { durdur(); return; }
      a?.pause(); setCaliyor(false); return;
    }
    if (devamRef.current) { const f = devamRef.current; devamRef.current = null; setEngel(false); f(); return; }
    if (a && a.src && !a.ended && a.currentTime > 0 && a.onended) { a.play().then(() => setCaliyor(true)).catch(() => {}); return; }
    tekrarOku();
  };

  // klavye
  useEffect(() => {
    const f = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey || e.altKey || (e.target as HTMLElement | null)?.closest?.('input,textarea,select')) return;
      if (e.key === 'Escape') { if (dersMenu) setDersMenu(false); else if (ayarAcik) setAyarAcik(false); else onClose(); return; }
      if (!ders || devamSor !== null) return;
      if (e.key === ' ') { e.preventDefault(); oynatDuraklat(); return; }
      if (e.key === 'ArrowRight') { e.preventDefault(); ileri(); return; }
      if (e.key === 'ArrowLeft') { e.preventDefault(); geri(); return; }
      if (!q || bitti) return;
      const k = e.key.toLocaleUpperCase('tr-TR');
      const h = (/^[1-5]$/.test(e.key) ? HARFLER[Number(e.key) - 1] : HARFLER.find((x) => x === k)) as Harf | undefined;
      if (h) { e.preventDefault(); cevapla(h); return; }
      if (k === 'İ' || k === 'I') { e.preventDefault(); ipucu(); return; }
      if (k === 'L') { e.preventDefault(); birYanlisEle(); return; }
      if (k === 'Ç') { e.preventDefault(); cozumuDinle(); return; }
      if (k === 'R') { e.preventDefault(); tekrarOku(); return; }
      if (e.key === 'Enter' && (durum === 'dogru' || durum === 'gosterildi')) { e.preventDefault(); ileri(); }
    };
    window.addEventListener('keydown', f);
    return () => window.removeEventListener('keydown', f);
  });
  useEffect(() => {
    const f = () => setTamEkran(!!document.fullscreenElement);
    document.addEventListener('fullscreenchange', f);
    return () => { document.removeEventListener('fullscreenchange', f); if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {}); };
  }, []);
  const tamEkranDegis = () => {
    if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {});
    else (kokRef.current?.closest('.sc') as HTMLElement | null)?.requestFullscreen?.().catch(() => {});
  };
  useEffect(() => {
    const ms = (navigator as Navigator & { mediaSession?: MediaSession }).mediaSession;
    if (!ms || !ders) return;
    try {
      ms.metadata = new MediaMetadata({ title: q ? `Soru ${i + 1}` : ders.baslik, artist: 'Patoloji · Soru çözücü', album: `${ders.no}) ${ders.baslik}` });
      ms.setActionHandler('nexttrack', () => ileri());
      ms.setActionHandler('previoustrack', () => geri());
    } catch { /* desteklenmiyor */ }
  }, [ders, q, i, ileri, geri]);

  const dersDegis = (k: string) => { durdur(); setDersMenu(false); setKod(k); onDersDegis?.(k); };
  const dizinIdx = dizin ? dizin.dersler.findIndex((d) => d.kod === kod) : -1;
  const sonrakiDers = dizin && dizinIdx >= 0 ? dizin.dersler[dizinIdx + 1] : undefined;
  const cozuldu = durum === 'dogru' || durum === 'gosterildi';

  // sonuç ekranı sayıları (gösterilen liste üzerinden)
  const say = (r: Sonuc) => sorular.filter((x) => sonuc[x.no] === r).length;
  const atlanan = sorular.filter((x) => !sonuc[x.no]).length;
  const tekrarlik = sorular.filter((x) => sonuc[x.no] !== 'd').map((x) => x.no);

  const durumMetni = !q ? '' : caliyor
    ? okunan?.yer === 'kok' || okunan?.yer === 'sik' ? 'Soruyu okuyor…' : okunan?.yer === 'ipucu' ? 'İpucu veriyor…'
      : okunan?.yer === 'cozum' ? 'Çözümü anlatıyor…' : durum === 'cozuluyor' ? 'Seçenekleri tek tek açıklıyor…' : 'Açıklıyor…'
    : durum === 'dogru' ? 'Doğru cevap' : durum === 'gosterildi' ? 'Çözüldü' : sesYok ? 'Metinle ilerliyor (ses hazırlanıyor)' : 'Cevabını bekliyor';

  const icerik = (
    <div className={`sc${caliyor ? ' is-konusuyor' : ''}`} role="dialog" aria-modal="true" aria-label="Patoloji sesli soru çözücü"
      onPointerDown={(e) => {
        const t = e.target as HTMLElement;
        if (ayarAcik && !t.closest('.sc-ayar')) setAyarAcik(false);
        if (dersMenu && !t.closest('.sc-ders')) setDersMenu(false);
      }}>
      <header className="sc-ust">
        <button type="button" className="sc-ikon" onClick={onClose} aria-label="Soru çözücüyü kapat"><X /></button>
        <div className="sc-ders">
          <button type="button" className="sc-ders-b" onClick={() => setDersMenu((v) => !v)} aria-expanded={dersMenu} aria-haspopup="listbox">
            <span className="sc-ders-no">{ders?.no ?? '…'}</span>
            <span className="sc-ders-t"><small>Soru çözücü{mod === 'cikmis' && tekrar ? ' · çıkmış sorular' : tekrar ? ' · yanlışların tekrarı' : ''}</small><b>{ders?.baslik ?? 'Yükleniyor…'}</b></span>
            <ChevronDown aria-hidden />
          </button>
          {dersMenu && dizin && (
            <div className="sc-menu" role="listbox" aria-label="Ders seç">
              {dizin.dersler.map((d) => {
                const p = ilerlemeOku()[d.kod];
                const c = p ? Object.keys(p.s).length : 0;
                return (
                  <button key={d.kod} type="button" role="option" aria-selected={d.kod === kod} className={d.kod === kod ? 'is-on' : ''} onClick={() => dersDegis(d.kod)}>
                    <span className="sc-menu-no">{d.no}</span>
                    <span className="sc-menu-t"><b>{d.baslik}</b><small>{d.soru} soru{c ? ` · ${c} çözüldü` : ''}{d.ses ? '' : ' · ses hazırlanıyor'}</small></span>
                  </button>
                );
              })}
            </div>
          )}
        </div>
        <button type="button" className="sc-ikon sc-tam" onClick={tamEkranDegis} aria-label={tamEkran ? 'Tam ekrandan çık' : 'Tam ekran'}>{tamEkran ? <Minimize2 /> : <Maximize2 />}</button>
      </header>

      {ders && devamSor === null && (
        <div className="sc-ilerleme" aria-label={`Soru ${Math.min(i + 1, sorular.length)} / ${sorular.length}`}>
          {sorular.map((x, n) => {
            const r = sonuc[x.no];
            return (
              <button key={x.no} type="button" className={`sc-seg${n === i && !bitti ? ' is-simdi' : ''}${r === 'd' ? ' is-d' : r === 'd2' ? ' is-d2' : r === 'y' ? ' is-y' : ''}`}
                onClick={() => { setBitti(false); setI(n); }} aria-label={`${n + 1}. soru${r === 'd' ? ', doğru' : r === 'd2' ? ', yardımla doğru' : r === 'y' ? ', çözümü dinlendi' : ''}`} />
            );
          })}
        </div>
      )}

      <main className="sc-sahne" ref={kokRef}>
        {hata && <div className="sc-bos"><p>Bu ders için soru çözücü henüz hazır değil.</p><button type="button" className="sc-btn" onClick={onClose}>Kapat</button></div>}
        {!hata && !ders && <div className="sc-bos"><span className="sc-dalga is-yukle" aria-hidden><i /><i /><i /><i /><i /></span><p>Sorular hazırlanıyor…</p></div>}

        {ders && devamSor !== null && (
          <div className="sc-kart sc-devam">
            <h2>Kaldığın yerden devam edelim mi?</h2>
            <p>{ders.baslik} · {devamSor + 1}. sorudaydın, {Object.keys(sonuc).length} soru çözdün.</p>
            <div className="sc-btnler">
              <button type="button" className="sc-btn is-dolu" onClick={() => { setI(devamSor); setDevamSor(null); }}><Play aria-hidden />Devam et</button>
              <button type="button" className="sc-btn" onClick={() => { setSonuc({}); setI(0); setDevamSor(null); }}><RotateCcw aria-hidden />Baştan başla</button>
            </div>
          </div>
        )}

        {ders && q && devamSor === null && !bitti && (
          <div className="sc-icerik" key={`${tekrar ? 't' : ''}${q.no}`}>
            <div className="sc-asistan" aria-live="polite">
              <span className="sc-dalga" aria-hidden><i /><i /><i /><i /><i /></span>
              <span className="sc-durum">{durumMetni}</span>
              <span className="sc-sayac">Soru {i + 1} / {sorular.length}</span>
            </div>

            <section className="sc-kart sc-soru">
              <div className={`sc-tur t-${q.tur || 'ornek'}`}>
                {q.tur === 'cikmis' ? <><b>Çıkmış soru</b>{q.sinav && <span>{q.sinav}</span>}</>
                  : q.tur === 'benzer' ? <><b>Benzer soru</b>{q.zorluk && <span>{q.zorluk === 'zor' ? 'Zor' : 'Orta'}</span>}</>
                  : <><b>Örnek soru</b><span>2026-27</span></>}
              </div>
              <h2 className={okunan?.yer === 'kok' && caliyor ? 'is-aktif' : ''}>{q.soru}</h2>
              <div className="sc-siklar" role="group" aria-label="Seçenekler">
                {HARFLER.map((h, n) => {
                  const dogruMu = cozuldu && h === q.dogru;
                  const el = elenen.includes(h) && !dogruMu;
                  const okunuyor = caliyor && okunan?.h === h && (okunan.yer === 'sik' || okunan.yer === 'aciklama');
                  return (
                    <button key={h} type="button"
                      className={`sc-sik${dogruMu ? ' is-dogru' : ''}${el ? ' is-yanlis' : ''}${cozuldu && !dogruMu ? ' is-sonuk' : ''}${okunuyor ? ' is-okunuyor' : ''}${sonSecim === h && el ? ' is-secili' : ''}`}
                      disabled={durum === 'cozuluyor' || (durum === 'acik' && elenen.includes(h))}
                      onClick={() => cevapla(h)}
                      aria-label={`${h}: ${q.secenekler[h]}${cozuldu ? ' — açıklamayı dinle' : ''}`}>
                      <b>{h}</b><span>{q.secenekler[h]}</span>
                      {!cozuldu && !el && <kbd aria-hidden>{n + 1}</kbd>}
                      {dogruMu && <Check className="sc-sik-i" aria-hidden />}
                      {el && <X className="sc-sik-i" aria-hidden />}
                      {cozuldu && <Volume2 className="sc-sik-dinle" aria-hidden />}
                    </button>
                  );
                })}
              </div>

              {!cozuldu && (
                <div className="sc-yardim-cubuk" role="group" aria-label="Yardım al">
                  <span className="sc-yardim-ad">Yardım al</span>
                  <button type="button" className="sc-ybtn" onClick={ipucu} disabled={durum !== 'acik'} title="İpucu (İ)"><Lightbulb aria-hidden />İpucu</button>
                  <button type="button" className="sc-ybtn" onClick={birYanlisEle} disabled={durum !== 'acik' || !kalanYanlis.length} title="Bir yanlışı ele (L)"><Eraser aria-hidden />Bir yanlışı ele</button>
                  <button type="button" className="sc-ybtn is-coz" onClick={cozumuDinle} disabled={durum !== 'acik'} title="Çözümü dinle (Ç)"><Headphones aria-hidden />Çözümü dinle</button>
                </div>
              )}
            </section>

            {ipucuAcik && (
              <div className={`sc-not sc-ipucu${okunan?.yer === 'ipucu' && caliyor ? ' is-aktif' : ''}`}>
                <b><Lightbulb aria-hidden />İpucu</b>
                <p><Metin metin={q.ipucu} /></p>
              </div>
            )}

            {aciklanan.length > 0 && (
              <div className="sc-not sc-aciklamalar">
                <b>{cozuldu || durum === 'cozuluyor' ? 'Seçeneklerin açıklaması' : 'Elenen seçenekler'}</b>
                <ul>
                  {HARFLER.filter((h) => aciklanan.includes(h)).map((h) => (
                    <li key={h} className={`${h === q.dogru ? 'is-dogru' : 'is-yanlis'}${caliyor && okunan?.yer === 'aciklama' && okunan.h === h ? ' is-aktif' : ''}`}>
                      <span className="sc-h">{h}</span><p><Metin metin={q.siklar[h]} /></p>
                    </li>
                  ))}
                </ul>
                {!cozuldu && durum === 'acik' && sonSecim && sonSecim !== q.dogru && <small className="sc-dene">Yanlış seçenek elendi — bir daha dene.</small>}
              </div>
            )}

            {cozuldu && (
              <div className={`sc-not sc-cozum${durum === 'dogru' ? ' is-dogru' : ''}${okunan?.yer === 'cozum' && caliyor ? ' is-aktif' : ''}`}>
                <b>{durum === 'dogru' ? (yanlisSecti ? 'Doğru, bu sefer oldu!' : yardim ? 'Doğru! · yardımla' : 'Doğru!') : `Doğru cevap ${q.dogru}`} <span>· {q.secenekler[q.dogru]}</span></b>
                <p><Metin metin={q.cozum} /></p>
                <small>Ders sunumu · s. {q.sayfa.join(', ')}{aciklanan.length < 5 ? ' · Diğer seçeneklerin açıklamasını dinlemek için üzerine dokun.' : ''}</small>
              </div>
            )}

            <div className="sc-btnler sc-alt-btn">
              {cozuldu
                ? <button type="button" className="sc-btn is-dolu" onClick={ileri}>{i >= sorular.length - 1 ? 'Sonuçları gör' : 'Sonraki soru'}<ChevronRight aria-hidden /></button>
                : <button type="button" className="sc-btn" onClick={tekrarOku}><RotateCcw aria-hidden />Soruyu yeniden oku</button>}
            </div>
          </div>
        )}

        {ders && devamSor === null && bitti && (
          <div className="sc-icerik">
            <section className="sc-kart sc-son">
              <small className="sc-etiket">{mod === 'cikmis' && tekrar ? 'Çıkmış sorular bitti' : tekrar ? 'Yanlışların tekrarı bitti' : 'Ders bitti'}</small>
              <h1>{ders.baslik}</h1>
              <div className="sc-skor">
                <div className="is-d"><b>{say('d')}</b><span>ilk denemede doğru</span></div>
                <div className="is-d2"><b>{say('d2')}</b><span>yardımla doğru</span></div>
                <div className="is-y"><b>{say('y') + atlanan}</b><span>çözümü dinlendi{atlanan ? ` / ${atlanan} atlandı` : ''}</span></div>
              </div>
              {tekrarlik.length > 0 && (
                <div className="sc-yanlis-l">
                  <h3>Tekrar etmen gerekenler</h3>
                  <ul>{sorular.filter((x) => tekrarlik.includes(x.no)).map((x) => (
                    <li key={x.no}><button type="button" onClick={() => { setBitti(false); setI(sorular.indexOf(x)); }}>
                      <b>{x.soru}</b><span>{x.dogru}) {x.secenekler[x.dogru]}</span>
                    </button></li>
                  ))}</ul>
                </div>
              )}
              <div className="sc-btnler">
                {tekrarlik.length > 0 && <button type="button" className="sc-btn is-dolu" onClick={() => { setListe(tekrarlik); setTekrar(true); setI(0); setBitti(false); }}><RotateCcw aria-hidden />Yanlışlarımı tekrar çöz</button>}
                <button type="button" className="sc-btn" onClick={() => { setListe(null); setTekrar(false); setSonuc({}); setI(0); setBitti(false); }}><RotateCcw aria-hidden />Baştan</button>
                {sonrakiDers && <button type="button" className="sc-btn" onClick={() => dersDegis(sonrakiDers.kod)}>Sonraki ders: {sonrakiDers.no}) {sonrakiDers.baslik}<ChevronRight aria-hidden /></button>}
              </div>
            </section>
          </div>
        )}
      </main>

      {engel && ders && devamSor === null && !bitti && (
        <button type="button" className="sc-baslat" onClick={() => { setEngel(false); oynatDuraklat(); }}>
          <span><Play aria-hidden /></span><b>Sesi başlat</b><small>Tarayıcı sesi başlatmak için bir dokunuş istiyor</small>
        </button>
      )}
      {ders && devamSor === null && (
        <footer className="sc-alt">
          <div className="sc-oynat">
            <button type="button" className="sc-ikon" onClick={geri} disabled={i === 0 && !bitti} aria-label="Önceki soru"><ChevronLeft /></button>
            <button type="button" className="sc-buyuk" onClick={oynatDuraklat} disabled={bitti} aria-label={caliyor ? 'Duraklat' : 'Oynat'}>{caliyor ? <Pause /> : <Play />}</button>
            <button type="button" className="sc-ikon" onClick={ileri} disabled={bitti} aria-label={cozuldu ? 'Sonraki soru' : 'Soruyu atla'}>{cozuldu ? <ChevronRight /> : <SkipForward />}</button>
          </div>
          <div className="sc-ayar">
            <label className="sc-sec" title="Konuşma hızı">
              <Volume2 aria-hidden />
              <select value={tercih.hiz} onChange={(e) => setTercih({ hiz: Number(e.target.value) })} aria-label="Konuşma hızı">
                {HIZLAR.map((h) => <option key={h} value={h}>{h.toLocaleString('tr-TR')}×</option>)}
              </select>
            </label>
            <button type="button" className="sc-ikon sc-ayar-b" onClick={() => setAyarAcik((v) => !v)} aria-expanded={ayarAcik} aria-label="Okuma ayarları"><Settings2 /></button>
            <div className={`sc-ayar-p${ayarAcik ? ' is-acik' : ''}`}>
            <label className="sc-oto" title="Soruyu okurken seçenekleri de oku">
              <input type="checkbox" checked={tercih.siklariOku} onChange={(e) => setTercih({ siklariOku: e.target.checked })} />
              <span>Seçenekleri oku</span>
            </label>
            <label className="sc-oto" title="Doğru cevaptan sonra sonraki soruya geç">
              <input type="checkbox" checked={tercih.otomatik} onChange={(e) => setTercih({ otomatik: e.target.checked })} />
              <span>Otomatik geç</span>
            </label>
            </div>
          </div>
        </footer>
      )}
    </div>
  );
  return createPortal(icerik, document.body);
};

export default SoruCozucu;
