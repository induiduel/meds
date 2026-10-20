import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  BookOpenText, Check, ChevronDown, ChevronLeft, ChevronRight, Clock, Eraser, Eye, EyeOff,
  Headphones, History, Lightbulb, Maximize2, Minimize2, Minus, Pause, Play, Plus, RotateCcw,
  Settings2, SkipForward, Star, Strikethrough, Volume2, WandSparkles, X,
} from 'lucide-react';
import {
  HARFLER, altDersYukle, altDizinYukle, altSesDurumuHesapla, altSesYolu, dk,
  ilerlemeDersSifirla, ilerlemeOku, ilerlemeYaz, sureYazi, tercihOku, tercihYaz, useAltIlerleme,
  type AltDers, type AltDizin, type AltIlerleme, type AltSoru, type AltTercih, type Harf,
} from './altVeri';
import { KonuDugmeleri, KonuSureEtiketi } from '../takip/KonuTakip';
import { SpotsSureDiyalog } from '../spots/sure/SpotsSureDiyalog';
import type { SpotBransSureGrup } from '../spots/sure/spotsSureVeri';
import { ekleCozucuSure, fmtSureDk, kaydetCozucuZiyaret, useSpotCozucuStats } from '../../services/spotCozucuIstatistik';
import { tekrarTamamlandi, useKonuSayaci, useSoruSayaci } from '../../services/calismaTakip';
import { OgrenYeri } from '../spots/ogren/OgrenYeri';
import { ogrenEslemeVar } from '../spots/ogren/ogrenEsle';
import { Metin } from '../spots/onem/OnemMadde';
import { useYildizliSayisi, yildizToggle, yildizliMi } from '../../services/yildizliParagrafStore';
import { YildizliParagraflarModal } from '../study/YildizliParagraflarModal';
import { lockScroll, unlockScroll } from '../../utils/scrollLock';
import { isIosBrowserTab, shouldAvoidNativeFullscreen } from '../../utils/device';
import { openPwaInstallGuide } from '../../services/pwaService';
import { toast } from '../ui/Toast';
import { navigateTo, pathFor } from '../../router';
import '../../styles/soru-cozucu.css';
import { isAppFullscreen, releasePageFullscreen } from '../../utils/fullscreen';
import '../../styles/alternatif-cozucu.css';
import CihazdaIsaret from '../cevrimdisi/CihazdaIsaret';

/**
 * Patoloji alternatif sesli soru çözücü (/alternatif-cozucu).
 * Ana Soru Çözücü (.scs + .sc) ile birebir aynı tasarım ve etkileşim dilini kullanır;
 * ek olarak her sorunun tek parça kesintisiz EMA seslendirmesini (kök → şıklar → A..E analiz → doğru cevap → özet)
 * zaman damgalarıyla canlı vurgulayarak oynatır ve istenen şıkka/bölüme anında sarma imkânı sunar.
 */

const HIZLAR = [
  0.75, 0.875, 1, 1.125, 1.25, 1.375, 1.5, 1.625, 1.75, 1.875, 2, 2.25, 2.5, 2.75, 3,
];
const OLCEK_MIN = 85;
const OLCEK_MAX = 130;

const katla = (s: string) =>
  s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ı/g, 'i');

const urlOku = (k: string) => {
  try {
    return new URLSearchParams(location.search).get(k);
  } catch {
    return null;
  }
};

const urlYaz = (p: Record<string, string | null>) => {
  try {
    const u = new URL(location.href);
    Object.entries(p).forEach(([k, v]) => (v === null ? u.searchParams.delete(k) : u.searchParams.set(k, v)));
    history.replaceState(history.state, '', u.pathname + u.search + u.hash);
  } catch {
    /* yok */
  }
};

let pwaIpucuGosterildi = false;
function pwaIpucu() {
  if (pwaIpucuGosterildi || !isIosBrowserTab()) return;
  pwaIpucuGosterildi = true;
  toast.info(
    'Tam ekran modu açıldı',
    'Adres çubuğunu da tamamen gizlemek için uygulamayı Ana Ekrana ekleyebilirsin.',
    { label: 'Nasıl eklenir?', onClick: () => openPwaInstallGuide() },
  );
}

/** Bir dersin ilerleme özetini (ilk denemede doğru, yardımla doğru, dinlenen/incelenen) hesaplar */
function dersOzetHesapla(il: AltIlerleme | undefined, toplamSoru: number) {
  if (!il) return { d: 0, d2: 0, y: 0, cozulen: 0, tamam: false };
  const ilkSet = new Set(il.ilkDogru || []);
  const bittiSet = new Set(il.bitti || []);
  const incSet = new Set(il.incelenen || []);
  const secimNos = Object.keys(il.secim || {}).map(Number);
  const tumNos = new Set<number>([...bittiSet, ...incSet, ...ilkSet, ...secimNos]);

  let d = 0;
  let d2 = 0;
  let y = 0;
  tumNos.forEach((no) => {
    if (ilkSet.has(no)) d++;
    else if (il.secim && il.secim[no]) d2++;
    else y++;
  });
  const cozulen = Math.min(toplamSoru, d + d2 + y);
  return {
    d,
    d2,
    y,
    cozulen,
    tamam: toplamSoru > 0 && cozulen >= toplamSoru,
  };
}

interface OynaticiProps {
  kod: string;
  mod?: 'yanlis' | 'cikmis';
  dizin: AltDizin;
  onClose: () => void;
  onDersDegis: (kod: string) => void;
}

const AlternatifCozucuOynatici: React.FC<OynaticiProps> = ({
  kod: kod0,
  mod,
  dizin,
  onClose,
  onDersDegis,
}) => {
  const [kod, setKod] = useState(kod0);
  const [ders, setDers] = useState<AltDers | null>(null);
  const [hata, setHata] = useState(false);
  const [liste, setListe] = useState<number[] | null>(null);
  const [tekrar, setTekrar] = useState(false);
  const [i, setI] = useState(0);
  const [bitti, setBitti] = useState(false);
  const [devamSor, setDevamSor] = useState<number | null>(null);

  const [tercih, setTercihState] = useState<AltTercih>(() => tercihOku());
  const setTercih = useCallback((parca: Partial<AltTercih>) => {
    setTercihState((prev) => {
      const yeni = tercihYaz({ ...prev, ...parca });
      return yeni;
    });
  }, []);

  const olcek = Math.round(Math.min(OLCEK_MAX, Math.max(OLCEK_MIN, tercih.olcek || 100))) / 100;
  const olcekAdim = useCallback((yon: 1 | -1) => {
    setTercihState((prev) => {
      const yeniOlcek = Math.min(OLCEK_MAX, Math.max(OLCEK_MIN, (prev.olcek || 100) + yon * 10));
      return tercihYaz({ ...prev, olcek: yeniOlcek });
    });
  }, []);

  // Ses ve arayüz durumu
  const [caliyor, setCaliyor] = useState(false);
  const [anlik, setAnlik] = useState(0);
  const [sure, setSure] = useState(0);
  const [engel, setEngel] = useState(false);
  const [dersMenu, setDersMenu] = useState(false);
  const [ayarAcik, setAyarAcik] = useState(false);
  // Uygulama tam ekrandayken açılırsa (tam ekranda sayfa geçişi, Geri) doğrudan tam ekran kipinde başlar.
  const [tamEkran, setTamEkran] = useState(() => isAppFullscreen());
  const [ogrenAcik, setOgrenAcik] = useState(false);
  const [yildizModalAcik, setYildizModalAcik] = useState(false);
  const yildizSayisi = useYildizliSayisi();
  // Yıldız değişimlerinde yeniden çizim için
  useYildizliSayisi();

  // Soru içi etkileşim durumu
  const [secilen, setSecilen] = useState<Harf | null>(null);
  const [elenen, setElenen] = useState<Harf[]>([]);
  const [cizili, setCizili] = useState<Harf[]>([]);
  const [ipucuAcik, setIpucuAcik] = useState(false);
  const [cozumGosterildi, setCozumGosterildi] = useState(false);
  const [yardimKullanildi, setYardimKullanildi] = useState(false);

  const sesRef = useRef<HTMLAudioElement | null>(null);
  const kokRef = useRef<HTMLDivElement>(null);
  const otoRef = useRef(tercih.otoGec);
  otoRef.current = tercih.otoGec;
  const cozumdenBaslaRef = useRef(tercih.cozumdenBasla);
  cozumdenBaslaRef.current = tercih.cozumdenBasla;

  useEffect(() => {
    lockScroll();
    return () => unlockScroll();
  }, []);

  // Ders yükleme
  useEffect(() => {
    let canli = true;
    setDers(null);
    setHata(false);
    setListe(null);
    setTekrar(false);
    setI(0);
    setBitti(false);
    setDevamSor(null);

    altDersYukle(kod)
      .then((d) => {
        if (!canli) return;
        const kayit = ilerlemeOku()[kod];
        const urlSoruNo = Number(urlOku('s') || urlOku('q'));
        const urlIdx = urlSoruNo ? d.sorular.findIndex((x) => x.no === urlSoruNo) : -1;

        if (mod === 'yanlis' && kayit) {
          const ilkSet = new Set(kayit.ilkDogru || []);
          const yanlisNos = d.sorular
            .filter((x) => (kayit.bitti?.includes(x.no) || kayit.incelenen?.includes(x.no) || kayit.secim?.[x.no]) && !ilkSet.has(x.no))
            .map((x) => x.no);
          if (yanlisNos.length) {
            setListe(yanlisNos);
            setTekrar(true);
          }
        } else if (mod === 'cikmis') {
          const cikmisNos = d.sorular.filter((x) => x.tur === 'cikmis').map((x) => x.no);
          if (cikmisNos.length) {
            setListe(cikmisNos);
            setTekrar(true);
          }
        } else if (urlIdx >= 0) {
          setI(urlIdx);
        } else if (kayit && kayit.i > 0 && kayit.i < d.sorular.length && (kayit.bitti?.length || 0) < d.sorular.length) {
          setDevamSor(kayit.i);
        }
        setDers(d);
      })
      .catch(() => {
        if (canli) setHata(true);
      });

    return () => {
      canli = false;
    };
  }, [kod, mod]);

  const sorular = useMemo(() => {
    if (!ders) return [];
    return liste ? ders.sorular.filter((x) => liste.includes(x.no)) : ders.sorular;
  }, [ders, liste]);

  const q: AltSoru | undefined = sorular[i];

  // Çalışma süresi ve konu takibi
  useEffect(() => {
    let sonHareket = Date.now();
    const hareket = () => {
      sonHareket = Date.now();
    };
    window.addEventListener('pointerdown', hareket, { passive: true, capture: true });
    window.addEventListener('keydown', hareket, { passive: true, capture: true });
    const TICK = 5;
    const tid = window.setInterval(() => {
      if (document.visibilityState !== 'visible') return;
      if (caliyor || Date.now() - sonHareket <= 45_000) {
        ekleCozucuSure(TICK);
      }
    }, TICK * 1000);
    return () => {
      window.clearInterval(tid);
      window.removeEventListener('pointerdown', hareket, { capture: true });
      window.removeEventListener('keydown', hareket, { capture: true });
    };
  }, [caliyor]);

  const takipKonu = ders ? `patoloji/${ders.kod}` : null;
  useKonuSayaci('cozucu', takipKonu, caliyor);
  const soruSay = useSoruSayaci('cozucu', takipKonu);

  // Soru değiştiğinde soru içi durumu ve sesi hazırla
  useEffect(() => {
    if (!ders || !q || devamSor !== null || bitti) return;
    const kayit = ilerlemeOku()[ders.kod];
    const oncekiSecim = kayit?.secim?.[q.no] || null;
    setSecilen(oncekiSecim);
    setElenen([]);
    setCizili([]);
    setIpucuAcik(false);
    setCozumGosterildi(!tercih.cevabiGizle || oncekiSecim === q.dogru || !!kayit?.bitti?.includes(q.no));
    setYardimKullanildi(false);
    setAnlik(0);
    setSure(q.sure || 0);

    if (!tekrar) {
      ilerlemeYaz(ders.kod, {
        ...(kayit || { i: 0, bitti: [] }),
        i,
      });
    }
    kaydetCozucuZiyaret({
      brans: 'patoloji',
      kod: ders.kod,
      dersNo: ders.no,
      baslik: ders.baslik,
      soruNo: Math.min(i + 1, sorular.length),
      toplamSoru: sorular.length,
    });
    urlYaz({ s: String(q.no) });

    const a = sesRef.current;
    if (a) {
      a.src = altSesYolu(ders.kod, q);
      a.playbackRate = tercih.hiz;
      const baslangicSn = cozumdenBaslaRef.current && q.zaman && q.zaman.length >= 6 ? Math.max(0, q.zaman[5] - 0.1) : 0;
      const baslat = () => {
        if (baslangicSn > 0 && a.duration > baslangicSn) {
          try {
            a.currentTime = baslangicSn;
            setAnlik(baslangicSn);
          } catch {
            /* yok */
          }
        }
      };
      a.onloadedmetadata = () => {
        setSure(a.duration || q.sure || 0);
        baslat();
      };
      if (caliyor) {
        a.play()
          .then(() => {
            setCaliyor(true);
            setEngel(false);
          })
          .catch(() => {
            setCaliyor(false);
            setEngel(true);
          });
      }
    }
    kokRef.current?.scrollTo({ top: 0, behavior: 'smooth' });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ders?.kod, q?.no, devamSor, bitti]);

  useEffect(() => {
    if (sesRef.current) sesRef.current.playbackRate = tercih.hiz;
  }, [tercih.hiz]);

  // Tercih değiştiğinde açık anlatım modunu yansıt
  useEffect(() => {
    if (!tercih.cevabiGizle) {
      setCozumGosterildi(true);
    }
  }, [tercih.cevabiGizle]);

  // Canlı ses bölümü ve elenen şıklar
  const sesDurumu = useMemo(() => {
    if (!q) return { bolum: { asama: 'bekle' as const }, elenenler: new Set<Harf>(), cozumeUlasti: false };
    return altSesDurumuHesapla(q, anlik, caliyor);
  }, [q, anlik, caliyor]);

  const { bolum, elenenler, cozumeUlasti } = sesDurumu;
  const cozuldu = cozumGosterildi || secilen === q?.dogru || cozumeUlasti;

  // Ses çözüme ulaştığında inceleme kaydını işle
  useEffect(() => {
    if (!ders || !q || !cozumeUlasti) return;
    const kayit = ilerlemeOku()[ders.kod] || { i, bitti: [] };
    const inc = new Set(kayit.incelenen || []);
    if (!inc.has(q.no)) {
      inc.add(q.no);
      ilerlemeYaz(ders.kod, { ...kayit, incelenen: Array.from(inc) });
    }
  }, [cozumeUlasti, ders, q, i]);

  const saniyeyeGit = useCallback((sn: number, oynat = true) => {
    const a = sesRef.current;
    if (!a) return;
    const hedef = Math.max(0, Math.min(sn, a.duration || sure || sn));
    try {
      a.currentTime = hedef;
      setAnlik(hedef);
    } catch {
      /* henüz yüklenmediyse */
    }
    if (oynat) {
      a.play()
        .then(() => {
          setCaliyor(true);
          setEngel(false);
        })
        .catch(() => {
          setCaliyor(false);
          setEngel(true);
        });
    }
  }, [sure]);

  const sikkaSar = useCallback((h: Harf, oynat = true) => {
    if (!q) return;
    const idx = HARFLER.indexOf(h);
    const z = q.zaman;
    if (z && z.length >= 12 && idx >= 0) {
      // z[6] = giriş bitişi (A açıklamasının başlangıcı), z[6+idx] = ilgili şıkkın açıklamasının başlangıcı
      const baslangic = Math.max(0, z[6 + idx] - 0.15);
      saniyeyeGit(baslangic, oynat);
    } else {
      saniyeyeGit(0, oynat);
    }
  }, [q, saniyeyeGit]);

  const oynatDuraklat = useCallback(() => {
    const a = sesRef.current;
    if (!a) return;
    if (caliyor) {
      a.pause();
      setCaliyor(false);
    } else {
      a.play()
        .then(() => {
          setCaliyor(true);
          setEngel(false);
        })
        .catch(() => {
          setCaliyor(false);
          setEngel(true);
        });
    }
  }, [caliyor]);

  const bastanOku = useCallback(() => {
    saniyeyeGit(0, true);
  }, [saniyeyeGit]);

  const cozumdenDinle = useCallback(() => {
    if (!q) return;
    setCozumGosterildi(true);
    const z = q.zaman;
    const bas = z && z.length >= 6 ? Math.max(0, z[5] - 0.1) : 0;
    saniyeyeGit(bas, true);
  }, [q, saniyeyeGit]);

  const ileri = useCallback(() => {
    if (!ders) return;
    if (i >= sorular.length - 1) {
      const a = sesRef.current;
      if (a) a.pause();
      setCaliyor(false);
      setBitti(true);
      if (takipKonu && !tekrar) tekrarTamamlandi('cozucu', takipKonu);
      return;
    }
    setI((prev) => prev + 1);
  }, [ders, i, sorular.length, takipKonu, tekrar]);

  const geri = useCallback(() => {
    if (bitti) {
      setBitti(false);
      return;
    }
    if (i > 0) setI((prev) => prev - 1);
  }, [bitti, i]);

  // Şık seçimi / şık açıklaması dinleme
  const cevapla = useCallback((h: Harf) => {
    if (!ders || !q) return;
    // Çözüm zaten açıksa şıkka tıklamak doğrudan o şıkkın sesli analizine sarar
    if (cozuldu) {
      sikkaSar(h, true);
      return;
    }
    const kayit = ilerlemeOku()[ders.kod] || { i, bitti: [] };
    const yeniSecim = { ...(kayit.secim || {}), [q.no]: h };
    setSecilen(h);

    if (h === q.dogru) {
      const ilkDogruList = new Set(kayit.ilkDogru || []);
      const bittiList = new Set(kayit.bitti || []);
      bittiList.add(q.no);
      if (!yardimKullanildi && elenen.length === 0) {
        ilkDogruList.add(q.no);
      }
      ilerlemeYaz(ders.kod, {
        ...kayit,
        i,
        secim: yeniSecim,
        bitti: Array.from(bittiList),
        ilkDogru: Array.from(ilkDogruList),
      });
      soruSay(q.no);
      setCozumGosterildi(true);
      // Doğru şıkkın açıklamasına veya cevaba sar
      sikkaSar(h, true);
    } else {
      setYardimKullanildi(true);
      setElenen((prev) => (prev.includes(h) ? prev : [...prev, h]));
      ilerlemeYaz(ders.kod, {
        ...kayit,
        i,
        secim: yeniSecim,
      });
      // Yanlış şıkkın neden yanlış olduğunu anlatan bölüme sar
      sikkaSar(h, true);
    }
  }, [ders, q, cozuldu, sikkaSar, i, yardimKullanildi, elenen.length, soruSay]);

  const birYanlisEle = useCallback(() => {
    if (!q) return;
    const kalan = HARFLER.filter((h) => h !== q.dogru && !elenen.includes(h) && !elenenler.has(h));
    if (!kalan.length) return;
    const sec = kalan[Math.floor(Math.random() * kalan.length)];
    setYardimKullanildi(true);
    setElenen((prev) => [...prev, sec]);
    sikkaSar(sec, true);
  }, [q, elenen, elenenler, sikkaSar]);

  const ipucuGoster = useCallback(() => {
    setYardimKullanildi(true);
    setIpucuAcik((v) => !v);
  }, []);

  const ciz = useCallback((h: Harf) => {
    setCizili((prev) => (prev.includes(h) ? prev.filter((x) => x !== h) : [...prev, h]));
  }, []);

  const dersDegis = useCallback((yeniKod: string) => {
    const a = sesRef.current;
    if (a) a.pause();
    setCaliyor(false);
    setDersMenu(false);
    setKod(yeniKod);
    onDersDegis(yeniKod);
  }, [onDersDegis]);

  // Tam ekran yönetimi
  useEffect(() => {
    let hadNative = false;
    const f = () => {
      const nativeFs = !!(document.fullscreenElement || (document as any).webkitFullscreenElement);
      if (nativeFs) {
        hadNative = true;
        setTamEkran(true);
      } else if (hadNative) {
        hadNative = false;
        setTamEkran(false);
        document.documentElement.classList.remove('is-app-fullscreen');
      }
    };
    document.addEventListener('fullscreenchange', f);
    document.addEventListener('webkitfullscreenchange', f);
    return () => {
      document.removeEventListener('fullscreenchange', f);
      document.removeEventListener('webkitfullscreenchange', f);
      // Sayfa geçişinde tam ekran korunur (yeni sayfa tam ekranda açılır), aksi hâlde kapanır.
      releasePageFullscreen();
    };
  }, []);

  const tamEkranDegis = useCallback(() => {
    const d = document as any;
    if (tamEkran) {
      setTamEkran(false);
      document.documentElement.classList.remove('is-app-fullscreen');
      if (d.fullscreenElement || d.webkitFullscreenElement) {
        (d.exitFullscreen || d.webkitExitFullscreen || d.webkitCancelFullScreen)?.call(d)?.catch?.(() => {});
      }
      return;
    }
    setTamEkran(true);
    document.documentElement.classList.add('is-app-fullscreen');
    const el: any = document.documentElement;
    const req = el?.requestFullscreen || el?.webkitRequestFullscreen || el?.webkitRequestFullScreen;
    if (!req || shouldAvoidNativeFullscreen()) {
      pwaIpucu();
      return;
    }
    try {
      req.call(el, { navigationUI: 'hide' })?.catch?.(() => {});
    } catch {
      try {
        req.call(el)?.catch?.(() => {});
      } catch {
        pwaIpucu();
      }
    }
  }, [tamEkran]);

  // Klavye kısayolları
  useEffect(() => {
    const f = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'SELECT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
      if ((e.ctrlKey || e.metaKey) && (e.key === '+' || e.key === '=' || e.key === '-' || e.key === '_' || e.key === '0')) {
        e.preventDefault();
        if (e.key === '0') setTercih({ olcek: 100 });
        else olcekAdim(e.key === '-' || e.key === '_' ? -1 : 1);
        return;
      }
      if (e.key === 'Escape') {
        if (ogrenAcik) setOgrenAcik(false);
        else if (ayarAcik) setAyarAcik(false);
        else if (dersMenu) setDersMenu(false);
        else onClose();
        return;
      }
      if (devamSor !== null || bitti || !q) return;
      if (e.code === 'Space') {
        e.preventDefault();
        oynatDuraklat();
        return;
      }
      if (e.key === 'ArrowRight') {
        e.preventDefault();
        ileri();
        return;
      }
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        geri();
        return;
      }
      const k = e.key.toLocaleUpperCase('tr-TR');
      if ((k === 'Ö' || k === 'O') && ogrenEslemeVar('patoloji')) {
        e.preventDefault();
        setOgrenAcik((v) => !v);
        return;
      }
      const h = (/^[1-5]$/.test(e.key) ? HARFLER[Number(e.key) - 1] : HARFLER.find((x) => x === k)) as Harf | undefined;
      if (h) {
        e.preventDefault();
        cevapla(h);
        return;
      }
      if (k === 'İ' || k === 'I') {
        e.preventDefault();
        ipucuGoster();
        return;
      }
      if (k === 'L') {
        e.preventDefault();
        birYanlisEle();
        return;
      }
      if (k === 'Ç') {
        e.preventDefault();
        cozumdenDinle();
        return;
      }
      if (k === 'R') {
        e.preventDefault();
        bastanOku();
        return;
      }
    };
    window.addEventListener('keydown', f);
    return () => window.removeEventListener('keydown', f);
  }, [ogrenAcik, ayarAcik, dersMenu, onClose, devamSor, bitti, q, oynatDuraklat, ileri, geri, cevapla, ipucuGoster, birYanlisEle, cozumdenDinle, bastanOku, setTercih, olcekAdim]);

  const ogrenVar = ogrenEslemeVar('patoloji');
  const dersKayit = ders ? ilerlemeOku()[ders.kod] : undefined;
  const ozetBilgi = ders ? dersOzetHesapla(dersKayit, ders.sorular.length) : { d: 0, d2: 0, y: 0, cozulen: 0, tamam: false };
  const dizinIdx = dizin.dersler.findIndex((d) => d.kod === kod);
  const sonrakiDers = dizinIdx >= 0 ? dizin.dersler[dizinIdx + 1] : undefined;

  // Canlı durum metni
  const durumMetni = useMemo(() => {
    if (!q) return '';
    if (caliyor) {
      if (bolum.asama === 'kok') return 'Soru kökünü okuyor…';
      if (bolum.asama === 'sik') return `${bolum.harf} seçeneğini okuyor…`;
      if (bolum.asama === 'giris') return 'Seçenek analizine geçiyor…';
      if (bolum.asama === 'acik') return `${bolum.harf} seçeneğini değerlendiriyor…`;
      if (bolum.asama === 'cevap') return `Doğru cevabı (${q.dogru}) açıklıyor…`;
      if (bolum.asama === 'ozet') return 'Klinik ve patolojik özeti anlatıyor…';
      return 'Sesli anlatım oynatılıyor…';
    }
    if (secilen === q.dogru) return 'Doğru cevaplandı';
    if (cozuldu) return 'Açık anlatım · Şıklara dokunarak o şıkkın analizini dinleyebilirsin';
    return 'Cevabını bekliyor (veya Oynat ile dinle)';
  }, [q, caliyor, bolum, secilen, cozuldu]);

  // Gösterilecek açıklamalar listesi
  const gosterilenAciklamalar = useMemo(() => {
    if (!q) return [] as Harf[];
    if (cozuldu) return HARFLER;
    const set = new Set<Harf>([...elenen, ...Array.from(elenenler)]);
    if (bolum.asama === 'acik') set.add(bolum.harf);
    return HARFLER.filter((h) => set.has(h));
  }, [q, cozuldu, elenen, elenenler, bolum]);

  const kalanYanlis = useMemo(() => {
    if (!q) return [] as Harf[];
    return HARFLER.filter((h) => h !== q.dogru && !elenen.includes(h) && !elenenler.has(h));
  }, [q, elenen, elenenler]);

  const tekrarlikNos = useMemo(() => {
    if (!ders) return [] as number[];
    const ilkSet = new Set(dersKayit?.ilkDogru || []);
    return sorular.filter((x) => !ilkSet.has(x.no)).map((x) => x.no);
  }, [ders, dersKayit, sorular]);

  const icerik = (
    <div
      className={`sc${caliyor ? ' is-konusuyor' : ''}${olcek !== 1 ? ' is-olcekli' : ''}${ogrenAcik && ogrenVar ? ' is-ogren' : ''}${tamEkran ? ' is-tam' : ''}`}
      style={{ ['--sc-zoom' as string]: olcek }}
      role="dialog"
      aria-modal="true"
      aria-label="Patoloji alternatif sesli soru çözücü"
      onPointerDown={(e) => {
        const t = e.target as HTMLElement;
        if (ayarAcik && !t.closest('.sc-ayar')) setAyarAcik(false);
        if (dersMenu && !t.closest('.sc-ders')) setDersMenu(false);
      }}
    >
      <header className="sc-ust">
        <button type="button" className="sc-ikon" onClick={onClose} aria-label="Soru çözücüyü kapat">
          <X />
        </button>
        <div className="sc-ders">
          <button
            type="button"
            className="sc-ders-b"
            onClick={() => setDersMenu((v) => !v)}
            aria-expanded={dersMenu}
            aria-haspopup="listbox"
          >
            <span className="sc-ders-no">{ders?.no ?? '…'}</span>
            <span className="sc-ders-t">
              <small>
                Patoloji · alternatif çözücü
                {mod === 'cikmis' && tekrar ? ' · çıkmış sorular' : tekrar ? ' · tekrar listesi' : ''}
              </small>
              <b>{ders?.baslik ?? 'Yükleniyor…'}</b>
            </span>
            <ChevronDown aria-hidden />
          </button>
          {dersMenu && (
            <div className="sc-menu" role="listbox" aria-label="Ders seç">
              {dizin.dersler.map((d) => {
                const p = ilerlemeOku()[d.kod];
                const o = dersOzetHesapla(p, d.soru);
                return (
                  <button
                    key={d.kod}
                    type="button"
                    role="option"
                    aria-selected={d.kod === kod}
                    className={d.kod === kod ? 'is-on' : ''}
                    onClick={() => dersDegis(d.kod)}
                  >
                    <span className="sc-menu-no">{d.no}</span>
                    <span className="sc-menu-t">
                      <b>{d.baslik}</b>
                      <small>
                        {d.soru} soru · {d.cikmis} çıkmış · {dk(d.sure)}
                        {o.cozulen ? ` · ${o.cozulen} tamamlandı` : ''}
                      </small>
                    </span>
                  </button>
                );
              })}
            </div>
          )}
        </div>
        <div className="sc-ust-sag">
          <button
            type="button"
            className={`sc-ikon sc-btn-yildiz${yildizSayisi > 0 ? ' is-on' : ''}`}
            onClick={() => setYildizModalAcik(true)}
            title="Yıldızlı paragraflar (Tekrar listem)"
            aria-label="Yıldızlı paragraflar"
          >
            <Star
              className="sc-yildiz-ust-i"
              fill={yildizSayisi > 0 ? '#f59e0b' : 'none'}
              color={yildizSayisi > 0 ? '#f59e0b' : 'currentColor'}
              aria-hidden
            />
            {yildizSayisi > 0 && <span className="sc-yildiz-rozet">{yildizSayisi}</span>}
          </button>
          {ogrenVar && (
            <button
              type="button"
              className="oy-ac is-ust"
              onClick={() => setOgrenAcik((v) => !v)}
              aria-pressed={ogrenAcik}
              title="Bu sorunun Öğren'deki yeri (Ö)"
            >
              <BookOpenText aria-hidden />
              <span>Öğren</span>
            </button>
          )}
          <div className="sc-olcek" role="group" aria-label="Metin ve öge ölçeği">
            <button
              type="button"
              className="sc-olcek-b"
              onClick={() => olcekAdim(-1)}
              disabled={tercih.olcek <= OLCEK_MIN}
              aria-label="Ölçeği küçült"
              title="Küçült (Ctrl −)"
            >
              <Minus aria-hidden />
            </button>
            <button
              type="button"
              className="sc-olcek-v"
              onClick={() => setTercih({ olcek: 100 })}
              disabled={tercih.olcek === 100}
              aria-label={`Ölçek %${tercih.olcek}, sıfırlamak için dokun`}
              title="Varsayılan ölçeğe sıfırla (%100 · Ctrl 0)"
            >
              %{tercih.olcek}
            </button>
            <button
              type="button"
              className="sc-olcek-b"
              onClick={() => olcekAdim(1)}
              disabled={tercih.olcek >= OLCEK_MAX}
              aria-label="Ölçeği büyüt"
              title="Büyüt (Ctrl +)"
            >
              <Plus aria-hidden />
            </button>
          </div>
          <button
            type="button"
            className="sc-ikon sc-tam"
            onClick={tamEkranDegis}
            aria-label={tamEkran ? 'Tam ekrandan çık' : 'Tam ekran'}
          >
            {tamEkran ? <Minimize2 /> : <Maximize2 />}
          </button>
        </div>
      </header>

      {ders && devamSor === null && (
        <div className="sc-ilerleme" aria-label={`Soru ${Math.min(i + 1, sorular.length)} / ${sorular.length}`}>
          {sorular.map((x, n) => {
            const ilkD = dersKayit?.ilkDogru?.includes(x.no);
            const sec = dersKayit?.secim?.[x.no];
            const bit = dersKayit?.bitti?.includes(x.no) || dersKayit?.incelenen?.includes(x.no);
            const r = ilkD ? 'd' : sec ? 'd2' : bit ? 'y' : '';
            return (
              <button
                key={x.no}
                type="button"
                className={`sc-seg${n === i && !bitti ? ' is-simdi' : ''}${r === 'd' ? ' is-d' : r === 'd2' ? ' is-d2' : r === 'y' ? ' is-y' : ''}`}
                onClick={() => {
                  setBitti(false);
                  setI(n);
                }}
                aria-label={`${n + 1}. soru${r === 'd' ? ', ilk denemede doğru' : r === 'd2' ? ', çözüldü' : r === 'y' ? ', dinlendi' : ''}`}
              />
            );
          })}
        </div>
      )}

      <main className="sc-sahne" ref={kokRef}>
        {hata && (
          <div className="sc-bos">
            <p>Bu ders için alternatif soru çözücü yüklenemedi.</p>
            <button type="button" className="sc-btn" onClick={onClose}>
              Kapat
            </button>
          </div>
        )}
        {!hata && !ders && (
          <div className="sc-bos">
            <span className="sc-dalga is-yukle" aria-hidden>
              <i />
              <i />
              <i />
              <i />
              <i />
            </span>
            <p>Sorular hazırlanıyor…</p>
          </div>
        )}

        {ders && devamSor !== null && (
          <div className="sc-kart sc-devam">
            <h2>Kaldığın yerden devam edelim mi?</h2>
            <p>
              {ders.baslik} · {devamSor + 1}. sorudaydın, {ozetBilgi.cozulen} soru tamamlandı.
            </p>
            <div className="sc-btnler">
              <button
                type="button"
                className="sc-btn is-dolu"
                onClick={() => {
                  setI(devamSor);
                  setDevamSor(null);
                }}
              >
                <Play aria-hidden />
                Devam et
              </button>
              <button
                type="button"
                className="sc-btn"
                onClick={() => {
                  ilerlemeDersSifirla(ders.kod);
                  setI(0);
                  setDevamSor(null);
                }}
              >
                <RotateCcw aria-hidden />
                Baştan başla
              </button>
            </div>
          </div>
        )}

        {ders && q && devamSor === null && !bitti && (
          <div className="sc-icerik" key={`${tekrar ? 't' : ''}${q.no}`}>
            <div className="sc-asistan" aria-live="polite">
              <span className="sc-dalga" aria-hidden>
                <i />
                <i />
                <i />
                <i />
                <i />
              </span>
              <span className="sc-durum">{durumMetni}</span>
              <span className="sc-sayac">
                Soru {i + 1} / {sorular.length}
                {ozetBilgi.cozulen > 0 && (
                  <span style={{ marginLeft: 6, fontWeight: 700, color: '#16a34a' }}>
                    · {ozetBilgi.cozulen}/{ders.sorular.length} tamamlandı
                  </span>
                )}
              </span>
              {ogrenVar && (
                <button
                  type="button"
                  className="oy-ac is-satir"
                  onClick={() => setOgrenAcik((v) => !v)}
                  aria-pressed={ogrenAcik}
                  aria-label="Bu sorunun Öğren'deki yeri"
                >
                  <BookOpenText aria-hidden />
                  <span>Öğren</span>
                </button>
              )}
            </div>

            <section className="sc-kart sc-soru">
              <div className={`sc-tur t-${q.tur || 'ornek'}`}>
                {q.tur === 'cikmis' ? (
                  <>
                    <b>Çıkmış soru</b>
                    {q.sinav && <span>{q.sinav}</span>}
                  </>
                ) : q.zorluk ? (
                  <>
                    <b>Örnek soru</b>
                    <span>{q.zorluk === 'zor' ? 'Zor' : q.zorluk === 'kolay' ? 'Kolay' : 'Orta'}</span>
                  </>
                ) : (
                  <>
                    <b>Örnek soru</b>
                    <span>2026-27</span>
                  </>
                )}
              </div>

              <h2
                className={bolum.asama === 'kok' && caliyor ? 'is-aktif' : ''}
                onClick={() => saniyeyeGit(0, true)}
                style={{ cursor: 'pointer' }}
                title="Soru kökünü baştan dinlemek için dokun"
              >
                {q.soru}
              </h2>

              <div className="sc-siklar" role="group" aria-label="Seçenekler">
                {HARFLER.map((h, n) => {
                  const dogruMu = cozuldu && h === q.dogru;
                  const el = (elenen.includes(h) || elenenler.has(h)) && !dogruMu;
                  const okunuyor =
                    caliyor &&
                    ((bolum.asama === 'sik' && bolum.harf === h) ||
                      (bolum.asama === 'acik' && bolum.harf === h) ||
                      (bolum.asama === 'cevap' && h === q.dogru));
                  const cizik = !cozuldu && !el && cizili.includes(h);

                  return (
                    <div key={h} className="sik-sar">
                      <button
                        type="button"
                        className={`sc-sik${cizik ? ' is-cizili' : ''}${dogruMu ? ' is-dogru' : ''}${el ? ' is-yanlis' : ''}${cozuldu && !dogruMu ? ' is-sonuk' : ''}${okunuyor ? ' is-okunuyor' : ''}${secilen === h && el ? ' is-secili' : ''}`}
                        onClick={() => cevapla(h)}
                        aria-label={`${h}: ${q.secenekler[h]}${cozuldu ? ' — bu şıkkın açıklamasını dinle' : ''}`}
                      >
                        <b>{h}</b>
                        <span>{q.secenekler[h]}</span>
                        {!cozuldu && !el && <kbd aria-hidden>{n + 1}</kbd>}
                        {dogruMu && <Check className="sc-sik-i" aria-hidden />}
                        {el && <X className="sc-sik-i" aria-hidden />}
                        {cozuldu && <Volume2 className="sc-sik-dinle" aria-hidden />}
                      </button>
                      {!cozuldu && !el && (
                        <button
                          type="button"
                          className={`sik-ciz${cizik ? ' is-on' : ''}`}
                          onClick={() => ciz(h)}
                          aria-pressed={cizik}
                          aria-label={cizik ? `${h} şıkkının üstündeki çizgiyi kaldır` : `${h} şıkkını kendin ele (üstünü çiz)`}
                          title={cizik ? 'Çizgiyi kaldır' : 'Şıkkı ele'}
                        >
                          <Strikethrough aria-hidden />
                        </button>
                      )}
                    </div>
                  );
                })}
              </div>

              <div className="sc-yardim-cubuk" role="group" aria-label="Yardım ve anlatım araçları">
                <span className="sc-yardim-ad">{cozuldu ? 'Sesli anlatım' : 'Yardım al'}</span>
                {q.ipucu && (
                  <button
                    type="button"
                    className="sc-ybtn"
                    onClick={ipucuGoster}
                    title="İpucu (İ)"
                  >
                    <Lightbulb aria-hidden />
                    {ipucuAcik ? 'İpucunu gizle' : 'İpucu'}
                  </button>
                )}
                {!cozuldu && (
                  <button
                    type="button"
                    className="sc-ybtn"
                    onClick={birYanlisEle}
                    disabled={!kalanYanlis.length}
                    title="Bir yanlışı ele (L)"
                  >
                    <Eraser aria-hidden />
                    Bir yanlışı ele
                  </button>
                )}
                <button
                  type="button"
                  className="sc-ybtn"
                  onClick={() => {
                    if (cozuldu && tercih.cevabiGizle) {
                      setCozumGosterildi(false);
                    } else {
                      setCozumGosterildi(true);
                    }
                  }}
                  title={cozuldu ? 'Çözümü gizle / kendin dene' : 'Tüm şık açıklamalarını ve çözümü göster'}
                >
                  {cozuldu ? <EyeOff aria-hidden /> : <Eye aria-hidden />}
                  {cozuldu ? 'Cevabı gizle' : 'Çözümü göster'}
                </button>
                <button
                  type="button"
                  className="sc-ybtn is-coz"
                  onClick={cozumdenDinle}
                  title="Seçeneklerin analizini ve doğru cevabı dinle (Ç)"
                >
                  <Headphones aria-hidden />
                  Çözüm analizini dinle
                </button>
              </div>
            </section>

            {ipucuAcik && q.ipucu && (
              <div className="sc-not sc-ipucu">
                <b>
                  <Lightbulb aria-hidden />
                  İpucu
                </b>
                <p>
                  <Metin metin={q.ipucu} />
                </p>
              </div>
            )}

            {gosterilenAciklamalar.length > 0 && (
              <div className={`sc-not sc-aciklamalar${bolum.asama === 'giris' && caliyor ? ' is-aktif' : ''}`}>
                <b>{cozuldu ? 'Seçeneklerin ayrıntılı analizi (dinlemek için şıkka dokun)' : 'Değerlendirilen seçenekler'}</b>
                {q.giris && <p className="ac-giris-satir">{q.giris}</p>}
                <ul>
                  {gosterilenAciklamalar.map((h) => {
                    const aktifMi = caliyor && bolum.asama === 'acik' && bolum.harf === h;
                    const yId = `ac_${kod}_${q.no}_sik_${h}`;
                    const yildizli = yildizliMi(yId);
                    return (
                      <li
                        key={h}
                        className={`ac-tiklanir ${h === q.dogru ? 'is-dogru' : 'is-yanlis'}${aktifMi ? ' is-aktif' : ''}`}
                        onClick={() => sikkaSar(h, true)}
                        title={`${h} seçeneğinin açıklamasını sesli dinle`}
                      >
                        <span className="sc-h">{h}</span>
                        <div className="ac-acik-govde">
                          <span className="ac-sik-baslik">{q.secenekler[h]}</span>
                          <p>
                            <Metin metin={q.aciklamalar[h]} />
                          </p>
                        </div>
                        <div className="ac-acik-sag">
                          <span className="ac-acik-ses" aria-hidden>
                            <Volume2 />
                          </span>
                          <button
                            type="button"
                            className={`sc-p-yildiz${yildizli ? ' is-on' : ''}`}
                            onClick={(e) => {
                              e.stopPropagation();
                              yildizToggle({
                                id: yId,
                                kaynak: 'soru_cozucu',
                                kaynakAd: 'Alternatif çözücü',
                                baslik: `${ders.baslik} · Soru ${q.no} (${h})`,
                                altBaslik: q.secenekler[h],
                                metin: q.aciklamalar[h],
                                deeplink: `/alternatif-cozucu?ders=${kod}&s=${q.no}`,
                                meta: { dersKod: kod, brans: 'patoloji', soruNo: q.no },
                              });
                            }}
                            title={yildizli ? 'Listemden çıkar' : 'Bu şık açıklamasını yıldızla'}
                            aria-label={yildizli ? 'Listemden çıkar' : 'Bu şık açıklamasını yıldızla'}
                          >
                            <Star fill={yildizli ? '#f59e0b' : 'none'} color={yildizli ? '#f59e0b' : 'currentColor'} aria-hidden />
                          </button>
                        </div>
                      </li>
                    );
                  })}
                </ul>
                {!cozuldu && secilen && secilen !== q.dogru && (
                  <small className="sc-dene">Yanlış seçenek elendi — kalan seçeneklerden birini seçebilir veya çözüm analizini dinleyebilirsin.</small>
                )}
              </div>
            )}

            {cozuldu && (
              <div
                className={`sc-not sc-cozum${secilen === q.dogru ? ' is-dogru' : ''}${caliyor && (bolum.asama === 'cevap' || bolum.asama === 'ozet') ? ' is-aktif' : ''}`}
                onClick={() => {
                  if (q.zaman && q.zaman.length >= 12) saniyeyeGit(Math.max(0, q.zaman[11] - 0.1), true);
                }}
                style={{ cursor: 'pointer' }}
                title="Doğru cevap ve özet bölümünü dinlemek için dokun"
              >
                <div className="sc-cozum-ust">
                  <b>
                    {secilen === q.dogru
                      ? yardimKullanildi
                        ? 'Doğru! · yardımla'
                        : 'Doğru!'
                      : `Doğru cevap ${q.dogru}`}{' '}
                    <span>· {q.secenekler[q.dogru]}</span>
                  </b>
                  <button
                    type="button"
                    className={`sc-p-yildiz${yildizliMi(`ac_${kod}_${q.no}_ozet`) ? ' is-on' : ''}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      yildizToggle({
                        id: `ac_${kod}_${q.no}_ozet`,
                        kaynak: 'soru_cozucu',
                        kaynakAd: 'Alternatif çözücü',
                        baslik: `${ders.baslik} · Soru ${q.no}`,
                        altBaslik: `Doğru Cevap: ${q.dogru} — ${q.secenekler[q.dogru]}`,
                        metin: q.ozet,
                        deeplink: `/alternatif-cozucu?ders=${kod}&s=${q.no}`,
                        meta: { dersKod: kod, brans: 'patoloji', soruNo: q.no },
                      });
                    }}
                    title="Özeti yıldızla"
                    aria-label="Özeti yıldızla"
                  >
                    <Star
                      fill={yildizliMi(`ac_${kod}_${q.no}_ozet`) ? '#f59e0b' : 'none'}
                      color={yildizliMi(`ac_${kod}_${q.no}_ozet`) ? '#f59e0b' : 'currentColor'}
                      aria-hidden
                    />
                  </button>
                </div>
                <p>
                  <Metin metin={q.ozet} />
                </p>
                <small>
                  {q.sayfa && q.sayfa.length > 0 ? `Ders sunumu · s. ${q.sayfa.join(', ')} · ` : ''}
                  Herhangi bir seçeneğin açıklamasını dinlemek için o şıkkın üzerine dokunabilirsin.
                </small>
                {ogrenVar && !ogrenAcik && (
                  <button
                    type="button"
                    className="sc-ogren-b"
                    onClick={(e) => {
                      e.stopPropagation();
                      setOgrenAcik(true);
                    }}
                  >
                    <BookOpenText aria-hidden />
                    Bu bilgiyi Öğren'de gör
                  </button>
                )}
              </div>
            )}

            <div className="sc-btnler sc-alt-btn">
              <button type="button" className="sc-btn" onClick={bastanOku}>
                <RotateCcw aria-hidden />
                Soruyu baştan dinle
              </button>
              <button type="button" className="sc-btn" onClick={cozumdenDinle}>
                <Headphones aria-hidden />
                Çözüm analizini dinle
              </button>
              <button type="button" className="sc-btn is-dolu" onClick={ileri}>
                {i >= sorular.length - 1 ? 'Sonuçları gör' : 'Sonraki soru'}
                <ChevronRight aria-hidden />
              </button>
            </div>
          </div>
        )}

        {ders && devamSor === null && bitti && (
          <div className="sc-icerik">
            <section className="sc-kart sc-son">
              <small className="sc-etiket">
                {mod === 'cikmis' && tekrar ? 'Çıkmış sorular bitti' : tekrar ? 'Tekrar listesi bitti' : 'Ders tamamlandı'}
              </small>
              <h1>{ders.baslik}</h1>
              <div className="sc-skor">
                <div className="is-d">
                  <b>{ozetBilgi.d}</b>
                  <span>ilk denemede doğru</span>
                </div>
                <div className="is-d2">
                  <b>{ozetBilgi.d2}</b>
                  <span>yardımla / denemeyle</span>
                </div>
                <div className="is-y">
                  <b>{ozetBilgi.y}</b>
                  <span>sesli anlatımı dinlendi</span>
                </div>
              </div>
              {tekrarlikNos.length > 0 && (
                <div className="sc-yanlis-l">
                  <h3>Tekrar gözden geçirebileceklerin ({tekrarlikNos.length})</h3>
                  <ul>
                    {sorular
                      .filter((x) => tekrarlikNos.includes(x.no))
                      .slice(0, 20)
                      .map((x) => (
                        <li key={x.no}>
                          <button
                            type="button"
                            onClick={() => {
                              setBitti(false);
                              setI(sorular.indexOf(x));
                            }}
                          >
                            <b>{x.soru}</b>
                            <span>
                              {x.dogru}) {x.secenekler[x.dogru]}
                            </span>
                          </button>
                        </li>
                      ))}
                  </ul>
                </div>
              )}
              <div className="sc-btnler">
                {tekrarlikNos.length > 0 && (
                  <button
                    type="button"
                    className="sc-btn is-dolu"
                    onClick={() => {
                      setListe(tekrarlikNos);
                      setTekrar(true);
                      setI(0);
                      setBitti(false);
                    }}
                  >
                    <RotateCcw aria-hidden />
                    Kalanları tekrar çöz
                  </button>
                )}
                <button
                  type="button"
                  className="sc-btn"
                  onClick={() => {
                    setListe(null);
                    setTekrar(false);
                    setI(0);
                    setBitti(false);
                  }}
                >
                  <RotateCcw aria-hidden />
                  Baştan dön
                </button>
                {sonrakiDers && (
                  <button type="button" className="sc-btn" onClick={() => dersDegis(sonrakiDers.kod)}>
                    Sonraki ders: {sonrakiDers.no}) {sonrakiDers.baslik}
                    <ChevronRight aria-hidden />
                  </button>
                )}
              </div>
            </section>
          </div>
        )}
      </main>

      {ogrenAcik && ogrenVar && ders && devamSor === null && !bitti && (
        <OgrenYeri
          brans="patoloji"
          kod={kod}
          tur="s"
          id={q?.no}
          baglam={`Soru ${i + 1}`}
          onKapat={() => setOgrenAcik(false)}
        />
      )}

      {engel && ders && devamSor === null && !bitti && (
        <button
          type="button"
          className="sc-baslat"
          onClick={() => {
            setEngel(false);
            oynatDuraklat();
          }}
        >
          <span>
            <Play aria-hidden />
          </span>
          <b>Sesi başlat</b>
          <small>Tarayıcı sesi başlatmak için bir dokunuş istiyor</small>
        </button>
      )}

      {ders && devamSor === null && (
        <footer className="sc-alt ac-alt-bar">
          <div className="sc-oynat">
            <button
              type="button"
              className="sc-ikon"
              onClick={geri}
              disabled={i === 0 && !bitti}
              aria-label="Önceki soru"
            >
              <ChevronLeft />
            </button>
            <button
              type="button"
              className="sc-ikon"
              onClick={bastanOku}
              disabled={bitti}
              aria-label="Baştan dinle"
              title="Baştan dinle (R)"
            >
              <RotateCcw />
            </button>
            <button
              type="button"
              className="sc-buyuk"
              onClick={oynatDuraklat}
              disabled={bitti}
              aria-label={caliyor ? 'Duraklat' : 'Oynat'}
            >
              {caliyor ? <Pause /> : <Play />}
            </button>
            <button
              type="button"
              className="sc-ikon"
              onClick={ileri}
              disabled={bitti}
              aria-label={cozuldu ? 'Sonraki soru' : 'Soruyu atla'}
            >
              {cozuldu ? <ChevronRight /> : <SkipForward />}
            </button>
          </div>

          {q && !bitti && (
            <div className="ac-zaman-cubuk">
              <div className="ac-zaman-ust">
                <input
                  type="range"
                  min={0}
                  max={Math.max(1, sure || q.sure || 1)}
                  step={0.1}
                  value={Math.min(anlik, sure || q.sure || 1)}
                  onChange={(e) => saniyeyeGit(Number(e.target.value), caliyor)}
                  aria-label="Ses konumu"
                />
                <span className="ac-zaman-sure">
                  {sureYazi(anlik)} / {sureYazi(sure || q.sure)}
                </span>
              </div>
              {q.zaman && q.zaman.length >= 13 && (
                <div className="ac-bolum-cubuk" role="group" aria-label="Ses bölümlerine hızlı atla">
                  <button
                    type="button"
                    className={`ac-bolum-btn${bolum.asama === 'kok' || bolum.asama === 'sik' ? ' is-aktif' : ''}`}
                    onClick={() => saniyeyeGit(0, true)}
                    title="Soru kökünü ve seçenekleri dinle"
                  >
                    Soru
                  </button>
                  {HARFLER.map((h) => (
                    <button
                      key={h}
                      type="button"
                      className={`ac-bolum-btn${bolum.asama === 'acik' && bolum.harf === h ? ' is-aktif' : ''}${cozuldu && h === q.dogru ? ' is-dogru' : ''}`}
                      onClick={() => sikkaSar(h, true)}
                      title={`${h} seçeneğinin analizini dinle`}
                    >
                      {h} analiz
                    </button>
                  ))}
                  <button
                    type="button"
                    className={`ac-bolum-btn${bolum.asama === 'cevap' || bolum.asama === 'ozet' ? ' is-aktif' : ''}`}
                    onClick={() => saniyeyeGit(Math.max(0, q.zaman![11] - 0.1), true)}
                    title="Doğru cevabı ve özeti dinle"
                  >
                    Özet
                  </button>
                </div>
              )}
            </div>
          )}

          <div className="sc-ayar">
            <button
              type="button"
              className={`sc-otocoz${!tercih.cevabiGizle ? ' is-acik' : ''}`}
              onClick={() => {
                const yeniGizle = !tercih.cevabiGizle;
                setTercih({ cevabiGizle: yeniGizle });
                setCozumGosterildi(!yeniGizle);
              }}
              disabled={bitti}
              aria-pressed={!tercih.cevabiGizle}
              title="Açık anlatım modunda tüm şık açıklamaları ve doğru cevap baştan görünür; kapatırsan önce kendin çözersin"
            >
              <WandSparkles aria-hidden />
              <span>{!tercih.cevabiGizle ? 'Açık anlatım' : 'Kendim çözeyim'}</span>
            </button>
            <label className="sc-sec" title="Konuşma hızı">
              <Volume2 aria-hidden />
              <select
                value={tercih.hiz}
                onChange={(e) => setTercih({ hiz: Number(e.target.value) })}
                aria-label="Konuşma hızı"
              >
                {HIZLAR.map((h) => (
                  <option key={h} value={h}>
                    {h.toLocaleString('tr-TR')}×
                  </option>
                ))}
              </select>
            </label>
            <button
              type="button"
              className={`sc-ikon sc-ayar-b${ayarAcik ? ' is-acik' : ''}`}
              onClick={() => setAyarAcik((v) => !v)}
              aria-expanded={ayarAcik}
              aria-label="Okuma ayarları"
              title="Okuma ayarları"
            >
              <Settings2 />
            </button>
            <div className={`sc-ayar-p${ayarAcik ? ' is-acik' : ''}`}>
              <label className="sc-oto" title="Ses bittiğinde otomatik olarak sıradaki soruya geç">
                <input
                  type="checkbox"
                  checked={tercih.otoGec}
                  onChange={(e) => setTercih({ otoGec: e.target.checked })}
                />
                <span>Otomatik geç</span>
              </label>
              <label className="sc-oto" title="Soruyu açtığında doğru cevabı ve açıklamaları ben seçmeden gösterme">
                <input
                  type="checkbox"
                  checked={tercih.cevabiGizle}
                  onChange={(e) => {
                    const gizle = e.target.checked;
                    setTercih({ cevabiGizle: gizle });
                    setCozumGosterildi(!gizle);
                  }}
                />
                <span>Önce kendim çözeyim</span>
              </label>
              <label className="sc-oto" title="Soru kökünü kendin okuyorsan sesi doğrudan şık analizinden başlat">
                <input
                  type="checkbox"
                  checked={tercih.cozumdenBasla}
                  onChange={(e) => setTercih({ cozumdenBasla: e.target.checked })}
                />
                <span>Doğrudan analizden başlat</span>
              </label>
            </div>
          </div>
        </footer>
      )}

      <audio
        ref={sesRef}
        preload="auto"
        onTimeUpdate={(e) => setAnlik(e.currentTarget.currentTime)}
        onLoadedMetadata={(e) => setSure(e.currentTarget.duration || q?.sure || 0)}
        onEnded={() => {
          if (ders && q) {
            const kayit = ilerlemeOku()[ders.kod] || { i, bitti: [] };
            const b = new Set(kayit.bitti || []);
            b.add(q.no);
            ilerlemeYaz(ders.kod, { ...kayit, i, bitti: Array.from(b) });
            soruSay(q.no);
          }
          if (otoRef.current && i < sorular.length - 1) {
            setI((prev) => prev + 1);
          } else if (otoRef.current && i >= sorular.length - 1) {
            setCaliyor(false);
            setBitti(true);
          } else {
            setCaliyor(false);
          }
        }}
        onPause={() => setCaliyor(false)}
        onPlay={() => {
          setCaliyor(true);
          setEngel(false);
        }}
      />

      {yildizModalAcik && (
        <YildizliParagraflarModal
          onClose={() => setYildizModalAcik(false)}
          onGecis={(item) => {
            if (item.meta?.dersKod === kod && item.meta?.soruNo !== undefined) {
              const targetI = sorular.findIndex((x) => x.no === item.meta!.soruNo);
              if (targetI >= 0) {
                setI(targetI);
                setDevamSor(null);
                setBitti(false);
                return true;
              }
            }
            return false;
          }}
        />
      )}
    </div>
  );

  return createPortal(icerik, document.body);
};

const AlternatifCozucuView: React.FC = () => {
  const [dizin, setDizin] = useState<AltDizin | null>(null);
  const [hata, setHata] = useState(false);
  const [ara, setAra] = useState('');
  const [sureAcik, setSureAcik] = useState(() => location.hash === '#sureler');
  const [acik, setAcik] = useState<{ kod: string; mod?: 'yanlis' | 'cikmis' } | null>(() => {
    const k = urlOku('ders');
    const c = urlOku('coz');
    return k ? { kod: k, mod: c === 'yanlis' || c === 'cikmis' ? c : undefined } : null;
  });

  const ilerleme = useAltIlerleme();
  const stats = useSpotCozucuStats();

  useEffect(() => {
    altDizinYukle()
      .then((d) => {
        setDizin(d);
        const k = urlOku('ders');
        if (k && d.dersler.some((x) => x.kod === k)) {
          const c = urlOku('coz');
          setAcik({ kod: k, mod: c === 'yanlis' || c === 'cikmis' ? c : undefined });
        }
      })
      .catch(() => setHata(true));
  }, []);

  useEffect(() => {
    const onPop = () => {
      if (location.hash === '#sureler') setSureAcik(true);
      const k = urlOku('ders');
      const c = urlOku('coz');
      if (k) setAcik({ kod: k, mod: c === 'yanlis' || c === 'cikmis' ? c : undefined });
      else setAcik(null);
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, []);

  const ac = useCallback((kod: string, mod?: 'yanlis' | 'cikmis') => {
    setAcik({ kod, mod });
    urlYaz({ ders: kod, coz: mod || '1' });
  }, []);

  const kapat = useCallback(() => {
    setAcik(null);
    urlYaz({ ders: null, coz: null, s: null });
  }, []);

  const genel = useMemo(() => {
    const t = { d: 0, d2: 0, y: 0, toplam: 0, sure: 0 };
    dizin?.dersler.forEach((d) => {
      const o = dersOzetHesapla(ilerleme[d.kod], d.soru);
      t.d += o.d;
      t.d2 += o.d2;
      t.y += o.y;
      t.toplam += d.soru;
      t.sure += d.sure;
    });
    return t;
  }, [dizin, ilerleme]);

  const dersler = useMemo(() => {
    const q = katla(ara.trim());
    return (dizin?.dersler || []).filter((d) => !q || katla(`${d.no} ${d.baslik}`).includes(q));
  }, [dizin, ara]);

  const sureGruplari = useMemo<SpotBransSureGrup[]>(() => {
    if (!dizin) return [];
    let dinlenenSure = 0;
    const dList = dizin.dersler.map((d) => {
      const o = dersOzetHesapla(ilerleme[d.kod], d.soru);
      if (o.tamam) dinlenenSure += d.sure;
      else if (d.soru > 0 && o.cozulen > 0) dinlenenSure += Math.round((o.cozulen / d.soru) * d.sure);
      return {
        kod: d.kod,
        no: d.no,
        baslik: d.baslik,
        sure: d.sure,
        soru: d.soru,
        cikmis: d.cikmis,
        tamamlandi: o.tamam,
      };
    });
    return [
      {
        brans: 'patoloji',
        ad: 'Patoloji · Alternatif Çözücü',
        kisa: 'Patoloji',
        dersler: dList,
        toplamSure: genel.sure,
        toplamSoru: GenelSoruSayisi(dizin),
        toplamAdim: dList.length,
        dinlenenSure,
      },
    ];
  }, [dizin, genel.sure, ilerleme]);

  if (hata) return <p className="scs-bos">Alternatif soru çözücü yüklenemedi.</p>;
  if (!dizin) return <p className="scs-bos">Yükleniyor…</p>;
  if (!dizin.dersler.length) return <p className="scs-bos">Alternatif soru çözücü hazırlanıyor.</p>;

  const yuzde = (n: number) => `${genel.toplam ? (n / genel.toplam) * 100 : 0}%`;
  const cozulen = genel.d + genel.d2 + genel.y;
  const dersSay = new Set(dizin.dersler.map((d) => d.no)).size;

  // Kaldığın yer: en son çalışılan, bitmemiş ders
  const son = dizin.dersler
    .map((d) => ({ d, p: ilerleme[d.kod], o: dersOzetHesapla(ilerleme[d.kod], d.soru) }))
    .filter((x) => x.p && (x.o.cozulen > 0 || x.p.i > 0) && !x.o.tamam)
    .sort((a, b) => (Number(b.p!.son) || 0) - (Number(a.p!.son) || 0))[0];

  return (
    <div className="scs">
      <header className="scs-head">
        <div className="scs-head-t">
          <h2>
            <Headphones aria-hidden />
            Patoloji · Alternatif sesli soru çözücü
          </h2>
          <span className="scs-count">
            {dersSay} ders · {genel.toplam.toLocaleString('tr-TR')} soru · ~{Math.round(genel.sure / 3600)} saat ses
          </span>
        </div>
        <p className="scs-desc">
          <span className="scs-kaynak">
            Sorular: 2026-27 amfi ders sunumları ve çıkmış sorular — her soru baştan sona kesintisiz EMA seslendirmesiyle okunur, tüm seçenekler tek tek değerlendirilir ve doğru cevap klinik/patolojik gerekçesiyle özetlenir.
          </span>
        </p>
        <div className="scs-prog" aria-label={`${cozulen} / ${genel.toplam} soru tamamlandı`}>
          <div className="scs-cubuk" aria-hidden>
            <i className="is-d" style={{ width: yuzde(genel.d) }} />
            <i className="is-d2" style={{ width: yuzde(genel.d2) }} />
            <i className="is-y" style={{ width: yuzde(genel.y) }} />
          </div>
          <small>
            <b>{cozulen}</b> / {genel.toplam} tamamlandı
            {cozulen > 0 && (
              <>
                {' '}· <span className="is-d">{genel.d} ilk denemede doğru</span>
                {genel.d2 > 0 && <> · <span className="is-d2">{genel.d2} denemeyle</span></>}
                {' '}· <span className="is-y">{genel.y} sesli dinlendi</span>
                {stats.cozucuSureSn > 0 && <> · <b>⏱️ {fmtSureDk(stats.cozucuSureSn)} çalışıldı</b></>}
              </>
            )}
          </small>
        </div>
      </header>

      {son && (
        <button type="button" className="scs-devam" onClick={() => ac(son.d.kod)}>
          <span className="scs-devam-ic" aria-hidden>
            <Play />
          </span>
          <span className="scs-devam-t">
            <small>Kaldığın yerden devam</small>
            <b>
              {son.d.no}. {son.d.baslik}
            </b>
          </span>
          <span className="scs-devam-n">
            {son.o.cozulen}/{son.d.soru}
          </span>
        </button>
      )}

      <div className="scs-arac">
        <div className="scs-ara">
          <input
            type="search"
            value={ara}
            onChange={(e) => setAra(e.target.value)}
            placeholder="Ders ara (ör. nekroz, inflamasyon, tümör)"
            aria-label="Ders ara"
          />
        </div>
        <button
          type="button"
          className="scs-btn-sure"
          onClick={() => setSureAcik(true)}
          title="Tüm derslerin sesli soru çözümü süreleri"
        >
          <Clock aria-hidden />
          <span>Süreler</span>
        </button>
        <button
          type="button"
          className="scs-btn-sure"
          onClick={() => navigateTo(pathFor('soru_cozucu') + '?brans=patoloji')}
          title="Adım adım etkileşimli klasik soru çözücüye geç"
        >
          <Headphones aria-hidden />
          <span>Klasik soru çözücü</span>
        </button>
      </div>

      <ul className="scs-liste is-satir">
        {dersler.map((d) => {
          const p = ilerleme[d.kod];
          const o = dersOzetHesapla(p, d.soru);
          const y = o.d2 + o.y;
          const w = (n: number) => `${(n / d.soru) * 100}%`;
          const devam = !o.tamam && (o.cozulen > 0 || (p?.i || 0) > 0);
          return (
            <li key={d.kod} className={`scs-row${o.tamam ? ' is-tamam' : ''}`}>
              <button
                type="button"
                className="scs-row-b"
                onClick={() => ac(d.kod)}
                aria-label={`${d.no}. ${d.baslik}: ${o.tamam ? 'yeniden dinle/çöz' : devam ? `devam et, ${o.cozulen}/${d.soru}` : 'başla'}`}
              >
                <span className="scs-no">{d.no}</span>
                <span className="scs-ad">
                  <b>{d.baslik}</b>
                  <small>
                    {d.soru} soru · {d.cikmis} çıkmış · ~{dk(d.sure)}
                    {o.cozulen ? ` · ${o.cozulen}/${d.soru} tamamlandı` : ''}
                  </small>
                  {o.cozulen > 0 && (
                    <span className="scs-cubuk" aria-hidden>
                      <i className="is-d" style={{ width: w(o.d) }} />
                      <i className="is-d2" style={{ width: w(o.d2) }} />
                      <i className="is-y" style={{ width: w(o.y) }} />
                    </span>
                  )}
                </span>
                <span className={`scs-durum${devam ? ' is-devam' : ''}`}>
                  {o.tamam ? (
                    <>
                      <Check aria-hidden />
                      Bitti
                    </>
                  ) : devam ? (
                    <>Devam</>
                  ) : (
                    <>
                      <Play aria-hidden />
                      Başla
                    </>
                  )}
                </span>
              </button>
              <div className="scs-row-ek">
                {!!d.cikmis && (
                  <button type="button" onClick={() => ac(d.kod, 'cikmis')}>
                    <History aria-hidden />
                    Yalnız çıkmışlar · {d.cikmis}
                  </button>
                )}
                {y > 0 && (
                  <button type="button" onClick={() => ac(d.kod, 'yanlis')}>
                    <RotateCcw aria-hidden />
                    Tekrar · {y}
                  </button>
                )}
                <span className="scs-row-takip">
                  <CihazdaIsaret paket={`alt:${d.kod}`} />
                  <KonuSureEtiketi modul="cozucu" konu={`patoloji/${d.kod}`} />
                  <KonuDugmeleri
                    kucuk
                    modul="cozucu"
                    konu={`patoloji/${d.kod}`}
                    ad={`${d.no}. ${d.baslik}`}
                    turetilen={o.tamam}
                    onTekrar={() => {
                      ilerlemeDersSifirla(d.kod);
                      ac(d.kod);
                    }}
                  />
                </span>
              </div>
            </li>
          );
        })}
      </ul>

      {!dersler.length && <p className="scs-bos">“{ara}” ile eşleşen ders yok.</p>}

      {sureAcik && (
        <SpotsSureDiyalog
          takipModul="cozucu"
          baslik="Alternatif sesli soru çözücü süreleri"
          gruplar={sureGruplari}
          onKapat={() => {
            setSureAcik(false);
            if (location.hash === '#sureler') {
              history.replaceState(history.state, '', location.pathname + location.search);
            }
          }}
          onDersAc={(_b, k) => ac(k)}
          birimAd="ders"
          not="Süreler kesintisiz EMA seslendirmesine göredir. Soru kökü, seçenekler, her şıkkın ayrıntılı analizi, doğru cevap ve özet bölümlerini içerir."
        />
      )}

      {acik && (
        <AlternatifCozucuOynatici
          key={`${acik.kod}-${acik.mod || ''}`}
          kod={acik.kod}
          mod={acik.mod}
          dizin={dizin}
          onClose={kapat}
          onDersDegis={(yeniKod) => urlYaz({ ders: yeniKod, coz: '1', s: null })}
        />
      )}
    </div>
  );
};

function GenelSoruSayisi(dizin: AltDizin): number {
  return dizin.dersler.reduce((a, b) => a + b.soru, 0);
}

export default AlternatifCozucuView;
