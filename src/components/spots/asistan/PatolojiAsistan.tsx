import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  BookOpenText, Check, ChevronDown, ChevronLeft, ChevronRight, ChevronUp, Headphones, HelpCircle, LifeBuoy, ListChecks, MapPin, Maximize2, Minimize2, Minus, Pause, Play, Plus, RotateCcw, Settings2, SkipBack, SkipForward, Star, Target, Trash2, Volume2, X,
  Strikethrough,
} from 'lucide-react';
import { getCustomApiUrl } from '../../../services/api';
import { lockScroll, unlockScroll } from '../../../utils/scrollLock';
import { ogrenildiAyarla, tercihOku, tercihYaz } from '../onem/onemVeri';
import { Metin } from '../onem/OnemMadde';
import { asistanDosyasi, asistanDizinDosyasi, kodBrans } from './asistanVeri';
import { tekrarTamamlandi, useKonuSayaci, useSoruSayaci } from '../../../services/calismaTakip';
import { cozucuyaGit } from '../spotsYol';
import { cozucuDizinYukle } from '../cozucu/cozucuVeri';
import { bransTanim } from '../brans';
import { OgrenYeri } from '../ogren/OgrenYeri';
import { ogrenEslemeVar } from '../ogren/ogrenEsle';
import { useYildizliMi, useYildizliSayisi, yildizToggle, yildizliMi } from '../../../services/yildizliParagrafStore';
import { YildizliParagraflarModal } from '../../study/YildizliParagraflarModal';
import '../../../styles/patoloji-asistan.css';

/**
 * Sesli sınav asistanı v2 (tam ekran; Patoloji, Enfeksiyon, Üroloji — branş ders kodunun önekinden). Yalnız "Sınav için en önemliler" spotları için.
 * İçerik: src/data/patoloji_asistan/<kod>.json (scripts/patoloji_onem/asistan_birlestir.py) — ders PDF'ine dayalı; dersin slayt
 * akışıyla bölümler ("neden önemli" girişiyle), her bölümde noktalar (ne · neden/mekanizma · sınavda nasıl çıkar), her noktadan
 * sonra o noktanın soruları (tüm çıkmışlar + 2026-27 örnek soruları). Her soruda: yanlış şıkka özgü açıklama (neden yanlış ·
 * neyi karıştırdın · doğrusu), doğruda pekiştirme, "Yardım al" (her şık tek kısa cümle, sırayla sesli; okunan şık vurgulu).
 * Ses: EMA Lightning klipleri (/api/patoloji-asistan/ses/<kod>/<klip>.mp3?v=…) ve cümle zamanları. Ses yoksa okuma süresiyle.
 */

interface Klip { v: string; sure: number; zaman: [number, number][] }
interface Soru { k: string; tur: 'cikmis' | 'ornek26' | 'ornek'; sinav?: string; kok: string; secenekler: Record<string, string>; dogru: string; dogruMetin: string; yanlis: Record<string, string>; yardim: Record<string, string> }
interface Nokta { id: string; bolum: number; puan: number; aday: number | null; kategori: string; baslik: string; bilgi: string; cumleler: string[]; sorular: Soru[] }
interface Ders { kod: string; no: number; baslik: string; soruSayisi: number; giris: string[]; kapanis: string[]; bolumler: { baslik: string; neden: string }[]; noktalar: Nokta[]; klip: Record<string, Klip> }
interface DizinDers { kod: string; no: number; baslik: string; bolum?: number; adim: number; soru: number; cikmis?: number; ses: boolean; sure: number }

const dersYukle = (kod: string) => asistanDosyasi(kod)?.().then((m) => m.default as Ders);
const dizinYukle = (kod: string) =>
  (asistanDizinDosyasi(kodBrans(kod))?.() ?? Promise.resolve({ default: { dersler: [] } })).then((m) => m.default.dersler as DizinDers[]);

type Yogunluk = 'hepsi' | 'cikmis' | 'az' | 'yok';
const YOGUNLUK: [Yogunluk, string][] = [['hepsi', 'Tüm sorular'], ['cikmis', 'Yalnız çıkmışlar'], ['az', 'Nokta başına 1'], ['yok', 'Soru yok']];
type Sahne =
  | { tip: 'giris' }
  | { tip: 'bolum'; b: number }
  | { tip: 'anlatim'; n: number }
  | { tip: 'soru'; n: number; q: Soru; qi: number; qn: number }
  | { tip: 'kapanis' }
  | { tip: 'son' };
type Sonuc = 'd' | 'd2' | 'y'; // ilk denemede doğru · yardım/ikinci denemede doğru · bilemedi
type AdimFiltre = 'hepsi' | 'kalan' | 'tekrar' | 'tamam' | 'aday';
interface Kayit {
  nid: string;
  enIleriNid?: string;
  okunanlar?: string[];
  sonuc: Record<string, Sonuc>;
  at: string;
}
const ILERLEME_KEY = 'medsoru_onem_asistan_v1';
const TERCIH_KEY = 'medsoru_onem_asistan_tercih_v1';
const HIZLAR = [
  0.75, 0.875, 1, 1.125, 1.25, 1.375, 1.5, 1.625, 1.75, 1.875, 2, 2.125, 2.25, 2.375, 2.5, 2.625, 2.75, 2.875, 3,
];
const OLCEK_MIN = 0.7;
const OLCEK_MAX = 1.6;
const olcekSinirla = (v: number) => Math.round(Math.min(OLCEK_MAX, Math.max(OLCEK_MIN, Number(v) || 1)) * 100) / 100;
const TUR_AD: Record<Soru['tur'], string> = { cikmis: 'Çıkmış soru', ornek26: 'Örnek soru · 2026-27', ornek: 'Örnek soru' };
const TUR_KISA: Record<Soru['tur'], string> = { cikmis: 'Çıkmış', ornek26: 'Örnek', ornek: 'Örnek' };
const kelimeSay = (s: string) => (s.match(/\S+/g) || []).length;
const azHareket = () => typeof window !== 'undefined' && !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

const sorulariSec = (n: Nokta, y: Yogunluk) =>
  y === 'yok' ? [] : y === 'cikmis' ? n.sorular.filter((q) => q.tur === 'cikmis') : y === 'az' ? n.sorular.slice(0, 1) : n.sorular;

/** sahne dizisi; tekrar verilirse yalnız o soruların noktaları ve o sorular */
const sahneleriKur = (d: Ders, y: Yogunluk, tekrar?: Set<string>): Sahne[] => {
  const out: Sahne[] = tekrar ? [] : [{ tip: 'giris' }];
  let son = -1;
  d.noktalar.forEach((nk, n) => {
    const qs = tekrar ? nk.sorular.filter((q) => tekrar.has(q.k)) : sorulariSec(nk, y);
    if (tekrar && !qs.length) return;
    if (!tekrar && nk.bolum !== son) { out.push({ tip: 'bolum', b: nk.bolum }); son = nk.bolum; }
    out.push({ tip: 'anlatim', n });
    qs.forEach((q, qi) => out.push({ tip: 'soru', n, q, qi, qn: qs.length }));
  });
  if (!tekrar) out.push({ tip: 'kapanis' });
  out.push({ tip: 'son' });
  return out;
};

export const PatolojiAsistan: React.FC<{ kod: string; onClose: () => void; onDersDegis?: (kod: string) => void }> = ({ kod: kod0, onClose, onDersDegis }) => {
  const [kod, setKod] = useState(kod0);
  const [ogrenAcik, setOgrenAcik] = useState(false);
  const [dizin, setDizin] = useState<DizinDers[]>([]);
  const [ders, setDers] = useState<Ders | null>(null);
  const [hata, setHata] = useState(false);
  const [tekrar, setTekrar] = useState<Set<string> | null>(null);
  const [i, setI] = useState(0);
  const [sonuc, setSonuc] = useState<Record<string, Sonuc>>({});
  const [sonKalinanNid, setSonKalinanNid] = useState<string | null>(null);
  const [okunanNoktalar, setOkunanNoktalar] = useState<Set<string>>(() => new Set());
  const [adimPanelAcik, setAdimPanelAcik] = useState(false);
  const [adimFiltre, setAdimFiltre] = useState<AdimFiltre>('hepsi');
  const [hoverNoktaIdx, setHoverNoktaIdx] = useState<number | null>(null);
  const [sifirlaOnay, setSifirlaOnay] = useState(false);
  const [tercih, setTercih0] = useState(() => tercihOku(TERCIH_KEY, { hiz: 1, otomatik: true, yogunluk: 'hepsi' as Yogunluk, olcek: 1 }));
  const olcek = olcekSinirla(tercih.olcek);
  const setTercih = (p: Partial<typeof tercih>) => setTercih0((t) => {
    const n = { ...t, ...p, olcek: olcekSinirla(p.olcek ?? t.olcek) };
    tercihYaz(TERCIH_KEY, n);
    return n;
  });
  const olcekAdim = useCallback((yon: 1 | -1) => {
    setTercih0((t) => {
      const n = { ...t, olcek: olcekSinirla(Math.round((olcekSinirla(t.olcek) + yon * 0.1) * 10) / 10) };
      tercihYaz(TERCIH_KEY, n);
      return n;
    });
  }, []);
  const [caliyor, setCaliyor] = useState(false);
  const [aktifCumle, setAktifCumle] = useState(-1);
  const [sesYok, setSesYok] = useState(false);
  const [devamSor, setDevamSor] = useState<Kayit | null>(null);
  const [dersMenu, setDersMenu] = useState(false);
  const [tamEkran, setTamEkran] = useState(false);
  const [ayarAcik, setAyarAcik] = useState(false); // dar ekranda oynatma ayarları açılır panelde
  const [engel, setEngel] = useState(false);
  const [yildizModalAcik, setYildizModalAcik] = useState(false);
  const yildizSayisi = useYildizliSayisi();
  // soru durumu
  const [elenen, setElenen] = useState<string[]>([]);
  const [cizili, setCizili] = useState<string[]>([]); // kullanıcının yalnız görsel olarak üstünü çizdiği şıklar
  const ciz = (h: string) => setCizili((c) => c.includes(h) ? c.filter((x) => x !== h) : [...c, h]);
  const [secim, setSecim] = useState<string | null>(null);
  const [cozuldu, setCozuldu] = useState<'dogru' | 'goster' | null>(null);
  const [yardim, setYardim] = useState(false);
  const [klipAdi, setKlipAdi] = useState('');
  const audio = useRef<HTMLAudioElement | null>(null);
  const zamanlayici = useRef<number | null>(null);
  const otoRef = useRef<number | null>(null);
  const bittiRef = useRef<(() => void) | null>(null);
  const kokRef = useRef<HTMLDivElement>(null);
  const sonCumleRef = useRef<number>(0);

  const sahneler = useMemo(() => (ders ? sahneleriKur(ders, tercih.yogunluk, tekrar || undefined) : []), [ders, tercih.yogunluk, tekrar]);
  const s = sahneler[i];
  // Konu takibi (Bitirdiklerim › En önemliler): etkin süre + yanıtlanan soru; tam akışta sona gelince tekrar turu biter
  const takipKonu = ders ? `${kodBrans(kod)}/${kod}` : null;
  useKonuSayaci('onem', takipKonu, caliyor);
  const soruSay = useSoruSayaci('onem', takipKonu);
  useEffect(() => { if (s?.tip === 'son' && !tekrar && takipKonu) tekrarTamamlandi('onem', takipKonu); }, [s?.tip]); // eslint-disable-line react-hooks/exhaustive-deps
  const nokta = s && (s.tip === 'anlatim' || s.tip === 'soru') ? ders!.noktalar[s.n] : null;

  // Deeplink desteği: URL'de ?nid=... ve ?p=... varsa o noktaya ve cümleye git
  const deeplinkUygula = useCallback((targetNid: string | null, targetP: string | null) => {
    if (!targetNid || !ders || !sahneler.length) return false;
    const targetI = sahneler.findIndex(
      (x) => (x.tip === 'anlatim' || x.tip === 'soru') && ders.noktalar[x.n]?.id === targetNid
    );
    if (targetI >= 0) {
      setI(targetI);
      setDevamSor(null);
      if (targetP !== null && targetP !== '') {
        if (targetP === 'hap') {
          setTimeout(() => {
            const el = document.querySelector('.pa-hap');
            if (el) {
              el.scrollIntoView({ behavior: 'smooth', block: 'center' });
              el.classList.remove('is-hedef');
              void (el as HTMLElement).offsetWidth;
              el.classList.add('is-hedef');
              setTimeout(() => el.classList.remove('is-hedef'), 3000);
            }
          }, 350);
        } else {
          const cIdx = parseInt(targetP, 10);
          if (!isNaN(cIdx)) {
            setAktifCumle(cIdx);
            setTimeout(() => {
              const el = document.querySelector(`.pa-cumleler [data-c="${cIdx}"]`);
              if (el) {
                el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                el.classList.remove('is-hedef');
                void (el as HTMLElement).offsetWidth;
                el.classList.add('is-hedef');
                setTimeout(() => el.classList.remove('is-hedef'), 3000);
              }
            }, 350);
          }
        }
      }
      return true;
    }
    return false;
  }, [ders, sahneler]);

  useEffect(() => {
    if (!ders || !sahneler.length) return;
    const sp = new URLSearchParams(window.location.search);
    deeplinkUygula(sp.get('nid'), sp.get('p'));
  }, [ders, sahneler, deeplinkUygula]);

  useEffect(() => {
    const onPop = () => {
      const sp = new URLSearchParams(window.location.search);
      const d = sp.get('ders');
      if (d && d !== kod) {
        setKod(d);
        return;
      }
      deeplinkUygula(sp.get('nid'), sp.get('p'));
    };
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
  }, [kod, deeplinkUygula]);

  useEffect(() => { lockScroll(); return () => unlockScroll(); }, []);
  useEffect(() => { dizinYukle(kod0).then(setDizin).catch(() => {}); }, [kod0]);
  useEffect(() => {
    let canli = true;
    setDers(null); setHata(false); setTekrar(null); setI(0); setSonuc({});
    setSonKalinanNid(null); setOkunanNoktalar(new Set()); setDevamSor(null);
    setAdimPanelAcik(false); setHoverNoktaIdx(null); setSifirlaOnay(false);
    const p = dersYukle(kod);
    if (!p) { setHata(true); return; }
    p.then((d) => {
      if (!canli) return;
      setDers(d);
      try {
        const k = (JSON.parse(localStorage.getItem(ILERLEME_KEY) || '{}') as Record<string, Kayit>)[kod];
        if (k) {
          if (k.sonuc && typeof k.sonuc === 'object') setSonuc(k.sonuc);
          const hedefId = k.enIleriNid || k.nid;
          const ni = hedefId ? d.noktalar.findIndex((n) => n.id === hedefId) : -1;
          if (ni >= 0) {
            setSonKalinanNid(d.noktalar[ni].id);
            const okunan = k.okunanlar?.length
              ? new Set(k.okunanlar)
              : new Set(d.noktalar.slice(0, ni + 1).map((n) => n.id));
            setOkunanNoktalar(okunan);
            const cozulenVar = Object.keys(k.sonuc || {}).length > 0;
            if (ni > 0 || cozulenVar) {
              setDevamSor({ ...k, nid: d.noktalar[ni].id, enIleriNid: d.noktalar[ni].id });
            }
          }
        }
      } catch { /* yok */ }
    }).catch(() => canli && setHata(true));
    return () => { canli = false; };
  }, [kod]);
  // ilerleme kaydı (yalnız tam akışta): bulunulan nokta + en ileri kalınan nokta + okunanlar + soru sonuçları
  useEffect(() => {
    if (!ders || tekrar || devamSor || !nokta) return;
    const mevcutIdx = ders.noktalar.indexOf(nokta);
    const oncekiSonIdx = sonKalinanNid ? ders.noktalar.findIndex((n) => n.id === sonKalinanNid) : -1;
    const yeniSonNid = mevcutIdx >= oncekiSonIdx ? nokta.id : (sonKalinanNid || nokta.id);
    if (yeniSonNid !== sonKalinanNid) setSonKalinanNid(yeniSonNid);

    let guncelOkunan = okunanNoktalar;
    if (!okunanNoktalar.has(nokta.id)) {
      guncelOkunan = new Set(okunanNoktalar);
      guncelOkunan.add(nokta.id);
      setOkunanNoktalar(guncelOkunan);
    }

    try {
      const t = JSON.parse(localStorage.getItem(ILERLEME_KEY) || '{}');
      t[kod] = {
        nid: yeniSonNid,
        enIleriNid: yeniSonNid,
        okunanlar: Array.from(guncelOkunan),
        sonuc,
        at: new Date().toISOString(),
      } as Kayit;
      localStorage.setItem(ILERLEME_KEY, JSON.stringify(t));
    } catch { /* özel pencere */ }
  }, [nokta, sonuc, ders, tekrar, kod, devamSor, sonKalinanNid, okunanNoktalar]);

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
    setKlipAdi(klip);
    setAktifCumle(cumleler.length ? 0 : -1);
    sonCumleRef.current = 0;
    bittiRef.current = bitti || null;
    const k = ders?.klip[klip];
    const hiz = tercih.hiz;
    const yedek = () => {
      setSesYok(true);
      const sureler = cumleler.map((c) => Math.max(1.4, kelimeSay(c) / 2.6) / hiz);
      let j = 0; let t = 0;
      setCaliyor(true);
      zamanlayici.current = window.setInterval(() => {
        t += 0.1;
        if (t >= sureler[j]) {
          t = 0; j++;
          if (j >= sureler.length) { durdur(); setAktifCumle(-1); bitti?.(); return; }
          setAktifCumle(j);
          sonCumleRef.current = j;
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
      const idx = Math.max(0, Math.min(cumleler.length - 1, j));
      setAktifCumle(idx);
      sonCumleRef.current = idx;
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
    otoRef.current = window.setTimeout(() => { otoRef.current = null; ileri(); }, 1200);
  }, [tercih.otomatik, ileri]);

  const sahneSesi = useCallback((x: Sahne | undefined) => {
    if (!x || !ders) return;
    if (x.tip === 'giris') cal('giris', ders.giris, otoIleri);
    else if (x.tip === 'kapanis') cal('kapanis', ders.kapanis, otoIleri);
    else if (x.tip === 'bolum') cal(`b-${x.b + 1}`, [ders.bolumler[x.b].neden], otoIleri);
    else if (x.tip === 'anlatim') cal(`a-${ders.noktalar[x.n].id}`, ders.noktalar[x.n].cumleler, otoIleri);
    else if (x.tip === 'soru') cal(`q-${x.q.k}`, [x.q.kok]);
    else durdur();
  }, [ders, cal, otoIleri, durdur]);

  // o anki sahnede geçerli cümle listesi (parça parça kontrol için)
  const aktifCumleler = useMemo(() => {
    if (!s || !ders) return [];
    if (s.tip === 'anlatim') return ders.noktalar[s.n]?.cumleler || [];
    if (s.tip === 'giris') return ders.giris;
    if (s.tip === 'kapanis') return ders.kapanis;
    if (s.tip === 'bolum') return [ders.bolumler[s.b]?.neden || ''];
    if (s.tip === 'soru') {
      if (yardim) return Object.values(s.q.yardim);
      if (cozuldu) return [s.q.dogruMetin];
      return [s.q.kok];
    }
    return [];
  }, [s, ders, yardim, cozuldu]);

  /** Belirtilen index'teki cümleye/parçaya sar ve çal */
  const cumleyeGit = useCallback((targetIdx: number) => {
    if (!s || !ders) return;
    if (otoRef.current) { window.clearTimeout(otoRef.current); otoRef.current = null; }

    const cumleler = aktifCumleler;
    if (!cumleler.length) return;
    const j = Math.max(0, Math.min(cumleler.length - 1, targetIdx));
    sonCumleRef.current = j;

    const beklenenKlip = s.tip === 'giris' ? 'giris'
      : s.tip === 'kapanis' ? 'kapanis'
      : s.tip === 'bolum' ? `b-${s.b + 1}`
      : s.tip === 'anlatim' ? `a-${ders.noktalar[s.n].id}`
      : s.tip === 'soru' ? (yardim ? `h-${s.q.k}` : cozuldu ? `d-${s.q.k}` : `q-${s.q.k}`)
      : null;

    if (!beklenenKlip) return;
    const k = ders.klip[beklenenKlip];
    const a = audio.current;

    if (a && klipAdi === beklenenKlip && k?.zaman?.[j]) {
      const baslangic = Math.max(0, k.zaman[j][0] - 0.04);
      a.currentTime = baslangic;
      setAktifCumle(j);
      if (!caliyor) {
        a.play().then(() => { setCaliyor(true); setEngel(false); }).catch(() => {});
      }
    } else {
      cal(beklenenKlip, cumleler, s.tip === 'soru' && !cozuldu ? undefined : otoIleri);
      if (k?.zaman?.[j] && audio.current) {
        const baslangic = Math.max(0, k.zaman[j][0] - 0.04);
        const aEl = audio.current;
        const sar = () => {
          try {
            aEl.currentTime = baslangic;
            setAktifCumle(j);
          } catch { /* yok */ }
        };
        aEl.addEventListener('loadedmetadata', sar, { once: true });
        aEl.addEventListener('canplay', sar, { once: true });
      }
    }
  }, [s, ders, aktifCumleler, klipAdi, caliyor, cal, otoIleri, yardim, cozuldu]);

  /** Aktif veya son biten cümleyi/parçayı tekrardan başlat */
  const cumleyiTekrarla = useCallback(() => {
    const hedef = aktifCumle >= 0 ? aktifCumle : sonCumleRef.current;
    cumleyeGit(hedef);
  }, [aktifCumle, cumleyeGit]);

  /** Önceki parçaya/cümleye geç */
  const oncekiCumle = useCallback(() => {
    const cumleler = aktifCumleler;
    if (!cumleler.length) return;
    const a = audio.current;
    const beklenenKlip = s?.tip === 'anlatim' ? `a-${ders?.noktalar[s.n].id}` : klipAdi;
    const k = beklenenKlip ? ders?.klip[beklenenKlip] : null;

    const suanki = aktifCumle >= 0 ? aktifCumle : sonCumleRef.current;
    if (a && k?.zaman?.[suanki]) {
      const baslangic = k.zaman[suanki][0];
      if (a.currentTime - baslangic > 1.8) {
        cumleyeGit(suanki);
        return;
      }
    }
    cumleyeGit(Math.max(0, suanki - 1));
  }, [aktifCumleler, s, ders, klipAdi, aktifCumle, cumleyeGit]);

  /** Sonraki parçaya/cümleye geç */
  const sonrakiCumle = useCallback(() => {
    const cumleler = aktifCumleler;
    if (!cumleler.length) return;
    const suanki = aktifCumle >= 0 ? aktifCumle : sonCumleRef.current;
    if (suanki < cumleler.length - 1) {
      cumleyeGit(suanki + 1);
    } else {
      ileri();
    }
  }, [aktifCumleler, aktifCumle, cumleyeGit, ileri]);

  /** Tüm anlatımı/sahneyi en baştan dinle */
  const tekrarDinle = useCallback(() => {
    cumleyeGit(0);
  }, [cumleyeGit]);

  // sahne değişince: bekleyen otomatik geçişi iptal et, soru durumunu sıfırla, sesi başlat
  useEffect(() => {
    if (otoRef.current) { window.clearTimeout(otoRef.current); otoRef.current = null; }
    if (!ders || !s || devamSor) return;
    setElenen([]); setCizili([]); setSecim(null); setCozuldu(null); setYardim(false);
    kokRef.current?.scrollTo({ top: 0, behavior: azHareket() ? 'auto' : 'smooth' });
    sahneSesi(s);
  }, [i, ders, sahneler, devamSor]); // eslint-disable-line react-hooks/exhaustive-deps

  const altaKaydir = (sec: string) => requestAnimationFrame(() => requestAnimationFrame(() =>
    kokRef.current?.querySelector(sec)?.scrollIntoView({ block: 'nearest', behavior: azHareket() ? 'auto' : 'smooth' })));
  const cevapla = (h: string) => {
    if (!s || s.tip !== 'soru' || cozuldu || elenen.includes(h)) return;
    const q = s.q;
    setSecim(h); setYardim(false);
    if (h === q.dogru) {
      setCozuldu('dogru');
      soruSay(q.k);
      setSonuc((r) => ({ ...r, [q.k]: r[q.k] === 'y' || elenen.length ? 'd2' : (r[q.k] || 'd') }));
      cal(`d-${q.k}`, [q.dogruMetin], otoIleri);
    } else {
      setElenen((e) => [...e, h]);
      soruSay(q.k);
      setSonuc((r) => ({ ...r, [q.k]: 'y' }));
      cal(`y-${q.k}-${h}`, [q.yanlis[h]]);
    }
    altaKaydir('.pa-geri');
  };
  const dogruyuGoster = () => {
    if (!s || s.tip !== 'soru') return;
    setCozuldu('goster'); setSecim(s.q.dogru); setYardim(false);
    soruSay(s.q.k);
    setSonuc((r) => ({ ...r, [s.q.k]: 'y' }));
    cal(`d-${s.q.k}`, [s.q.dogruMetin]);
    altaKaydir('.pa-geri');
  };
  /** Yardım al: her şık tek cümle, sırayla; okunan şık vurgulanır. Sonradan doğru cevap "ilk denemede" sayılmaz. */
  const yardimAl = () => {
    if (!s || s.tip !== 'soru') return;
    setYardim(true);
    if (!cozuldu) setSonuc((r) => ({ ...r, [s.q.k]: r[s.q.k] || 'y' }));
    cal(`h-${s.q.k}`, Object.keys(s.q.yardim).map((h) => s.q.yardim[h]));
    altaKaydir('.pa-yardim');
  };
  const oynatDuraklat = () => {
    if (otoRef.current) { window.clearTimeout(otoRef.current); otoRef.current = null; }
    const a = audio.current;
    if (caliyor) {
      if (zamanlayici.current) { window.clearInterval(zamanlayici.current); zamanlayici.current = null; setCaliyor(false); return; }
      a?.pause(); setCaliyor(false);
    } else if (a && a.src && !a.ended && a.currentTime > 0) {
      a.play().then(() => setCaliyor(true)).catch(() => {});
    } else if (a && a.ended) {
      tekrarDinle();
    } else {
      sahneSesi(s);
    }
  };
  const yogunlukDegis = (y: Yogunluk) => {
    // aynı noktada kal: yeni sahne dizisinde o noktanın anlatımına git
    const nid = nokta?.id;
    setTercih({ yogunluk: y });
    if (ders && nid) {
      const yeni = sahneleriKur(ders, y, tekrar || undefined);
      const j = yeni.findIndex((x) => x.tip === 'anlatim' && ders.noktalar[x.n].id === nid);
      setI(j >= 0 ? j : 0);
    }
  };

  // klavye + yakınlaştırma hareketleri
  useEffect(() => {
    const f = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && !e.altKey) {
        if (e.key === '=' || e.key === '+') { e.preventDefault(); olcekAdim(1); return; }
        if (e.key === '-' || e.key === '_') { e.preventDefault(); olcekAdim(-1); return; }
        if (e.key === '0') { e.preventDefault(); setTercih({ olcek: 1 }); return; }
        return;
      }
      if (e.altKey || (e.target as HTMLElement | null)?.closest?.('input,textarea,select,.oy')) return;
      if (e.key === 'Escape') {
        if (ogrenAcik) setOgrenAcik(false);
        else if (adimPanelAcik) setAdimPanelAcik(false);
        else if (dersMenu) setDersMenu(false);
        else if (ayarAcik) setAyarAcik(false);
        else if (tamEkran) setTamEkran(false);
        else onClose();
        return;
      }
      if ((e.key === 'ö' || e.key === 'Ö' || e.key === 'o' || e.key === 'O') && ogrenEslemeVar(kodBrans(kod))) { e.preventDefault(); setOgrenAcik((v) => !v); return; }
      if (e.key === ' ') { e.preventDefault(); oynatDuraklat(); return; }
      if (e.key === 'r' || e.key === 'R') { e.preventDefault(); cumleyiTekrarla(); return; }
      if (e.key === 't' || e.key === 'T') { e.preventDefault(); tekrarDinle(); return; }
      if (e.key === '[' || (e.shiftKey && e.key === 'ArrowLeft')) { e.preventDefault(); oncekiCumle(); return; }
      if (e.key === ']' || (e.shiftKey && e.key === 'ArrowRight')) { e.preventDefault(); sonrakiCumle(); return; }
      if (e.key === 'ArrowRight') { e.preventDefault(); ileri(); return; }
      if (e.key === 'ArrowLeft') { e.preventDefault(); geri(); return; }
      if (s?.tip === 'soru') {
        const harfler = Object.keys(s.q.secenekler);
        const n = /^[1-9]$/.test(e.key) ? harfler[Number(e.key) - 1] : e.key.toUpperCase();
        if (!cozuldu && harfler.includes(n)) { e.preventDefault(); cevapla(n); return; }
        if (e.key === 'y' || e.key === 'Y' || e.key === '?') { e.preventDefault(); yardimAl(); return; }
        if (cozuldu && e.key === 'Enter') { e.preventDefault(); ileri(); }
      }
    };
    window.addEventListener('keydown', f);
    return () => window.removeEventListener('keydown', f);
  });
  useEffect(() => {
    const el = kokRef.current;
    if (!el) return;
    let birikim = 0;
    const tekerlek = (e: WheelEvent) => {
      if (!e.ctrlKey && !e.metaKey) return;
      e.preventDefault();
      birikim += -e.deltaY;
      if (Math.abs(birikim) >= 40) {
        olcekAdim(birikim > 0 ? 1 : -1);
        birikim = 0;
      }
    };
    el.addEventListener('wheel', tekerlek, { passive: false });
    return () => el.removeEventListener('wheel', tekerlek);
  }, [olcekAdim]);
  useEffect(() => {
    const f = () => {
      const nativeFs = !!(document.fullscreenElement || (document as any).webkitFullscreenElement);
      setTamEkran(nativeFs);
    };
    document.addEventListener('fullscreenchange', f);
    document.addEventListener('webkitfullscreenchange', f);
    return () => {
      document.removeEventListener('fullscreenchange', f);
      document.removeEventListener('webkitfullscreenchange', f);
      const d = document as any;
      if (d.fullscreenElement || d.webkitFullscreenElement) {
        (d.exitFullscreen || d.webkitExitFullscreen)?.call(d)?.catch?.(() => {});
      }
    };
  }, []);
  const tamEkranDegis = () => {
    const d = document as any;
    if (tamEkran) {
      setTamEkran(false);
      if (d.fullscreenElement || d.webkitFullscreenElement) {
        (d.exitFullscreen || d.webkitExitFullscreen)?.call(d)?.catch?.(() => {});
      }
      return;
    }
    setTamEkran(true);
    const isIos = typeof CSS !== 'undefined' && typeof CSS.supports === 'function' && CSS.supports('-webkit-touch-callout', 'none');
    if (isIos) return;
    const el: any = kokRef.current?.closest('.pa') || document.documentElement;
    const req = el?.requestFullscreen || el?.webkitRequestFullscreen;
    if (req) {
      try {
        req.call(el, { navigationUI: 'hide' })?.catch?.(() => {});
      } catch {
        /* iOS/iPadOS'ta CSS tam ekran (is-tam) kullanılır */
      }
    }
  };
  useEffect(() => {
    const ms = (navigator as Navigator & { mediaSession?: MediaSession }).mediaSession;
    if (!ms || !ders) return;
    try {
      ms.metadata = new MediaMetadata({ title: nokta ? nokta.baslik : ders.baslik, artist: `${bransTanim(kodBrans(kod)).ad} · Sınav asistanı`, album: `${ders.no}) ${ders.baslik}` });
      ms.setActionHandler('nexttrack', () => ileri());
      ms.setActionHandler('previoustrack', () => geri());
    } catch { /* desteklenmiyor */ }
  }, [ders, nokta, ileri, geri]);

  const dersDegis = (k: string) => { durdur(); setDersMenu(false); setAdimPanelAcik(false); setKod(k); onDersDegis?.(k); };
  const cozucuyuAc = (hedefKod: string) => {
    durdur();
    const b = kodBrans(hedefKod);
    cozucuDizinYukle(b).then((c) => {
      const hedef = c.dersler.find((x) => x.kod === hedefKod) || c.dersler.find((x) => x.kod.startsWith(`${hedefKod}-`));
      cozucuyaGit({ brans: b, ders: hedef?.kod, coz: hedef ? '1' : null });
      onClose();
    }).catch(() => {});
  };
  const dizinIdx = dizin.findIndex((d) => d.kod === kod);
  const sonrakiDers = dizinIdx >= 0 ? dizin[dizinIdx + 1] : undefined;

  const gorunenNoktalar = useMemo(() => {
    const out: number[] = [];
    sahneler.forEach((x) => { if (x.tip === 'anlatim') out.push(x.n); });
    return out;
  }, [sahneler]);
  const noktaSirasi = nokta ? gorunenNoktalar.indexOf(ders!.noktalar.indexOf(nokta)) + 1 : s?.tip === 'kapanis' || s?.tip === 'son' ? gorunenNoktalar.length : 0;
  const tumSorular = useMemo(() => (ders ? ders.noktalar.flatMap((n) => n.sorular) : []), [ders]);
  const sorulanlar = useMemo(() => sahneler.filter((x): x is Extract<Sahne, { tip: 'soru' }> => x.tip === 'soru').map((x) => x.q), [sahneler]);
  const ilkDogru = sorulanlar.filter((q) => sonuc[q.k] === 'd').length;
  const yardimliDogru = sorulanlar.filter((q) => sonuc[q.k] === 'd2').length;
  const yanlisSayisi = sorulanlar.filter((q) => sonuc[q.k] === 'y').length;
  const cozulenSoruSayisi = ilkDogru + yardimliDogru + yanlisSayisi;
  const tekrarlar = sorulanlar.filter((q) => sonuc[q.k] !== 'd');
  const atlanan = tekrarlar.filter((q) => !sonuc[q.k]).length;
  const tekrarNoktalar = ders ? ders.noktalar.filter((n) => n.sorular.some((q) => tekrarlar.includes(q))) : [];

  // En son kalınan nokta bilgisi
  const sonKalinanGlobalIdx = useMemo(() => {
    if (!ders || !sonKalinanNid) return -1;
    return ders.noktalar.findIndex((n) => n.id === sonKalinanNid);
  }, [ders, sonKalinanNid]);
  const sonKalinanGorunenIdx = useMemo(() => {
    if (sonKalinanGlobalIdx < 0) return -1;
    return gorunenNoktalar.indexOf(sonKalinanGlobalIdx);
  }, [gorunenNoktalar, sonKalinanGlobalIdx]);
  const sonKalinanSira = sonKalinanGorunenIdx >= 0 ? sonKalinanGorunenIdx + 1 : 0;
  const sonKalinanNokta = sonKalinanGlobalIdx >= 0 && ders ? ders.noktalar[sonKalinanGlobalIdx] : null;

  // Aktif adımın soruları ve alt adım (aşama) bilgisi
  const aktifNoktaSorular = useMemo(() => (nokta ? (tekrar ? nokta.sorular.filter((q) => tekrar.has(q.k)) : sorulariSec(nokta, tercih.yogunluk)) : []), [nokta, tekrar, tercih.yogunluk]);
  const aktifToplamAsama = nokta ? 1 + aktifNoktaSorular.length : 0;
  const aktifAsamaNo = nokta && s ? (s.tip === 'anlatim' ? 1 : s.tip === 'soru' ? 2 + s.qi : 1) : 0;

  // Bir adımın durumunu hesapla
  const adimDurum = useCallback((nk: Nokta) => {
    const qs = tekrar ? nk.sorular.filter((q) => tekrar.has(q.k)) : sorulariSec(nk, tercih.yogunluk);
    const yanitlanan = qs.filter((q) => sonuc[q.k]);
    const okundu = okunanNoktalar.has(nk.id);
    if (qs.length > 0 && yanitlanan.length === qs.length) {
      if (qs.every((q) => sonuc[q.k] === 'd')) return 'tamam' as const;
      if (qs.some((q) => sonuc[q.k] === 'y')) return 'yanlis' as const;
      return 'yardimli' as const;
    }
    if (yanitlanan.length > 0) {
      if (yanitlanan.some((q) => sonuc[q.k] === 'y')) return 'yanlis' as const;
      return 'kismi' as const;
    }
    if (okundu) return qs.length === 0 ? ('tamam' as const) : ('okundu' as const);
    return 'bekliyor' as const;
  }, [tekrar, tercih.yogunluk, sonuc, okunanNoktalar]);

  const segSinif = (nk: Nokta) => {
    const qs = sorulariSec(nk, tercih.yogunluk).filter((q) => sonuc[q.k]);
    if (!qs.length) return '';
    return qs.every((q) => sonuc[q.k] === 'd') ? ' is-d' : qs.some((q) => sonuc[q.k] === 'y') ? ' is-y' : ' is-d2';
  };

  /** Belirli bir noktanın anlatımına veya belirli bir sorusuna git */
  const noktayaGit = useCallback((ni: number, soruIdx?: number) => {
    setDevamSor(null);
    setAdimPanelAcik(false);
    setHoverNoktaIdx(null);
    if (soruIdx !== undefined) {
      const x = sahneler.findIndex((y) => y.tip === 'soru' && y.n === ni && y.qi === soruIdx);
      if (x >= 0) { setI(x); return; }
    }
    const x = sahneler.findIndex((y) => y.tip === 'anlatim' && y.n === ni);
    if (x >= 0) setI(x);
  }, [sahneler]);

  /** En son kalınan ilerleme noktasına git (varsa çözülmemiş sorusuna, yoksa anlatımına) */
  const sonKalinanaGit = useCallback(() => {
    if (!ders) return;
    const hedefNi = sonKalinanGlobalIdx >= 0 ? sonKalinanGlobalIdx : gorunenNoktalar[0] ?? 0;
    const nk = ders.noktalar[hedefNi];
    if (!nk) return;
    const qs = tekrar ? nk.sorular.filter((q) => tekrar.has(q.k)) : sorulariSec(nk, tercih.yogunluk);
    const ilkCozulmemisQi = qs.findIndex((q) => !sonuc[q.k]);
    // Eğer anlatım zaten okunmuşsa ve çözülmemiş soru varsa ama bazı sorular çözülmüşse doğrudan o soruya git, aksi halde anlatımına git
    const baziCozulmus = qs.some((q) => !!sonuc[q.k]);
    if (baziCozulmus && ilkCozulmemisQi >= 0) {
      noktayaGit(hedefNi, ilkCozulmemisQi);
    } else {
      noktayaGit(hedefNi);
    }
  }, [ders, sonKalinanGlobalIdx, gorunenNoktalar, tekrar, tercih.yogunluk, sonuc, noktayaGit]);

  /** Sıradaki henüz tamamlanmamış / çözülmemiş ilk adıma git */
  const siradakiCozulmemiseGit = useCallback(() => {
    if (!ders) return;
    for (const ni of gorunenNoktalar) {
      const nk = ders.noktalar[ni];
      const d = adimDurum(nk);
      if (d === 'bekliyor' || d === 'okundu' || d === 'kismi') {
        const qs = tekrar ? nk.sorular.filter((q) => tekrar.has(q.k)) : sorulariSec(nk, tercih.yogunluk);
        const ilkBos = qs.findIndex((q) => !sonuc[q.k]);
        if ((d === 'okundu' || d === 'kismi') && ilkBos >= 0) {
          noktayaGit(ni, ilkBos);
        } else {
          noktayaGit(ni);
        }
        return;
      }
    }
    if (gorunenNoktalar.length > 0) noktayaGit(gorunenNoktalar[0]);
  }, [ders, gorunenNoktalar, adimDurum, tekrar, tercih.yogunluk, sonuc, noktayaGit]);

  /** Yanlış veya yardımlı çözülmüş ilk adıma git */
  const ilkTekraraGit = useCallback(() => {
    if (!ders) return;
    for (const ni of gorunenNoktalar) {
      const nk = ders.noktalar[ni];
      const qs = tekrar ? nk.sorular.filter((q) => tekrar.has(q.k)) : sorulariSec(nk, tercih.yogunluk);
      const hataliQi = qs.findIndex((q) => sonuc[q.k] === 'y' || sonuc[q.k] === 'd2');
      if (hataliQi >= 0) {
        noktayaGit(ni, hataliQi);
        return;
      }
    }
  }, [ders, gorunenNoktalar, tekrar, tercih.yogunluk, sonuc, noktayaGit]);

  /** Kullanıcının seçtiği adımı "en son kalınan yer" olarak sabitle */
  const kalinanYeriBurayaTasi = useCallback((hedefNid: string) => {
    if (!ders) return;
    setSonKalinanNid(hedefNid);
    try {
      const t = JSON.parse(localStorage.getItem(ILERLEME_KEY) || '{}');
      t[kod] = {
        nid: hedefNid,
        enIleriNid: hedefNid,
        okunanlar: Array.from(okunanNoktalar),
        sonuc,
        at: new Date().toISOString(),
      } as Kayit;
      localStorage.setItem(ILERLEME_KEY, JSON.stringify(t));
    } catch { /* özel pencere */ }
  }, [ders, kod, okunanNoktalar, sonuc]);

  /** Bu dersteki tüm ilerlemeyi sıfırla */
  const ilerlemeyiSifirla = useCallback(() => {
    setSonuc({});
    setSonKalinanNid(null);
    setOkunanNoktalar(new Set());
    setTekrar(null);
    setDevamSor(null);
    setAdimPanelAcik(false);
    setSifirlaOnay(false);
    setI(0);
    try {
      const t = JSON.parse(localStorage.getItem(ILERLEME_KEY) || '{}');
      delete t[kod];
      localStorage.setItem(ILERLEME_KEY, JSON.stringify(t));
    } catch { /* özel pencere */ }
  }, [kod]);

  // Adım istatistikleri (panel filtreleri ve özet için)
  const adimSayilari = useMemo(() => {
    if (!ders) return { tamam: 0, tekrar: 0, kalan: 0, aday: 0, toplamCumle: 0 };
    let tamam = 0; let tekrarSay = 0; let kalan = 0; let aday = 0; let toplamCumle = 0;
    gorunenNoktalar.forEach((ni) => {
      const nk = ders.noktalar[ni];
      toplamCumle += nk.cumleler.length;
      if (nk.aday) aday++;
      const d = adimDurum(nk);
      if (d === 'tamam') tamam++;
      else if (d === 'yanlis' || d === 'yardimli') tekrarSay++;
      else kalan++;
    });
    return { tamam, tekrar: tekrarSay, kalan, aday, toplamCumle };
  }, [ders, gorunenNoktalar, adimDurum]);

  const icerik = (
    <div
      className={`pa${caliyor ? ' is-konusuyor' : ''}${olcek !== 1 ? ' is-olcekli' : ''}${ogrenAcik ? ' is-ogren' : ''}${tamEkran ? ' is-tam' : ''}`}
      style={{ ['--pa-zoom' as string]: olcek }}
      role="dialog"
      aria-modal="true"
      aria-label={`${bransTanim(kodBrans(kod)).ad} sesli sınav asistanı`}
      onPointerDown={(e) => {
        const t = e.target as HTMLElement;
        if (dersMenu && !t.closest('.pa-ders')) setDersMenu(false);
        if (adimPanelAcik && !t.closest('.pa-ilerleme-kapsam')) setAdimPanelAcik(false);
        if (ayarAcik && !t.closest('.pa-ayar, .pa-ayar-ac')) setAyarAcik(false);
      }}
    >
      <header className="pa-ust">
        <button type="button" className="pa-ikon" onClick={onClose} aria-label="Asistanı kapat"><X /></button>
        <div className="pa-ders">
          <button type="button" className="pa-ders-b" onClick={() => setDersMenu((v) => !v)} aria-expanded={dersMenu} aria-haspopup="listbox">
            <span className="pa-ders-no">{ders?.no ?? '…'}</span>
            <span className="pa-ders-t"><small>Sınav asistanı{tekrar ? ' · tekrar' : nokta ? ` · ${ders!.bolumler[nokta.bolum]?.baslik || ''}` : ''}</small><b>{ders?.baslik ?? 'Yükleniyor…'}</b></span>
            <ChevronDown aria-hidden />
          </button>
          {dersMenu && (
            <div className="pa-menu" role="listbox" aria-label="Ders seç">
              {dizin.map((d) => (
                <button key={d.kod} type="button" role="option" aria-selected={d.kod === kod} className={d.kod === kod ? 'is-on' : ''} onClick={() => dersDegis(d.kod)}>
                  <span className="pa-menu-no">{d.no}</span>
                  <span className="pa-menu-t"><b>{d.baslik}</b><small>{d.adim} nokta · {d.soru} soru{d.ses ? ` · ${Math.max(1, Math.round(d.sure / 60))} dk anlatım` : ' · ses hazırlanıyor'}</small></span>
                </button>
              ))}
            </div>
          )}
        </div>
        <div className="pa-ust-sag">
          <button
            type="button"
            className={`pa-ikon pa-btn-yildiz${yildizSayisi > 0 ? ' is-on' : ''}`}
            onClick={() => setYildizModalAcik(true)}
            title="Yıldızlı paragraflar (Tekrar listem)"
            aria-label="Yıldızlı paragraflar"
          >
            <Star className="pa-yildiz-ust-i" fill={yildizSayisi > 0 ? '#f59e0b' : 'none'} color={yildizSayisi > 0 ? '#f59e0b' : 'currentColor'} aria-hidden />
            {yildizSayisi > 0 && <span className="pa-yildiz-rozet">{yildizSayisi}</span>}
          </button>
          {ogrenEslemeVar(kodBrans(kod)) && (
            <button type="button" className="oy-ac" onClick={() => setOgrenAcik((v) => !v)} aria-pressed={ogrenAcik} title="Bu bilginin Öğren'deki yeri (Ö)">
              <BookOpenText aria-hidden /><span>Öğren</span>
            </button>
          )}
          <div className="pa-olcek" role="group" aria-label="Metin ve öge ölçeği">
            <button type="button" className="pa-olcek-b" onClick={() => olcekAdim(-1)} disabled={olcek <= OLCEK_MIN} aria-label="Ölçeği küçült" title="Küçült (Ctrl −)"><Minus aria-hidden /></button>
            <button type="button" className="pa-olcek-v" onClick={() => setTercih({ olcek: 1 })} disabled={olcek === 1} aria-label={`Ölçek %${Math.round(olcek * 100)}, sıfırlamak için dokun`} title="Varsayılan ölçeğe sıfırla (%100 · Ctrl 0)">%{Math.round(olcek * 100)}</button>
            <button type="button" className="pa-olcek-b" onClick={() => olcekAdim(1)} disabled={olcek >= OLCEK_MAX} aria-label="Ölçeği büyüt" title="Büyüt (Ctrl +)"><Plus aria-hidden /></button>
          </div>
          <button type="button" className="pa-ikon pa-tam" onClick={tamEkranDegis} aria-label={tamEkran ? 'Tam ekrandan çık' : 'Tam ekran'}>{tamEkran ? <Minimize2 /> : <Maximize2 />}</button>
        </div>
      </header>

      {ders && (
        <div className="pa-ilerleme-kapsam">
          {/* 1. Satır: Kompakt Konum + Satır İçi Aşama Hapları + Son Kalınan & İstatistik */}
          <div className="pa-ilerleme-ust">
            <button
              type="button"
              className={`pa-konum-tetik${adimPanelAcik ? ' is-acik' : ''}`}
              onClick={() => setAdimPanelAcik((v) => !v)}
              aria-expanded={adimPanelAcik}
              title="Tüm adımları, soru sayılarını ve ilerleme durumunu görüntüle / yönet"
            >
              <span className="pa-konum-rozet">
                {nokta
                  ? `Adım ${noktaSirasi}/${gorunenNoktalar.length}`
                  : s?.tip === 'giris'
                    ? `Giriş`
                    : s?.tip === 'bolum'
                      ? `Bölüm ${s.b + 1}/${ders.bolumler.length}`
                      : `Özet`}
              </span>
              {!nokta && (
                <span className="pa-konum-detay">
                  {ders.bolumler.length} bölüm · <b>{gorunenNoktalar.length} adım</b> · <b>{sorulanlar.length} soru</b>
                </span>
              )}
              <span className="pa-konum-ac-etiket">
                <ListChecks aria-hidden />
                <span>Adımlar</span>
                {adimPanelAcik ? <ChevronUp aria-hidden /> : <ChevronDown aria-hidden />}
              </span>
            </button>

            {nokta && !devamSor && (
              <div className="pa-alt-adim-haplar" role="navigation" aria-label="Mevcut adımın aşamaları">
                <button
                  type="button"
                  className={`pa-asama-hap${s?.tip === 'anlatim' ? ' is-aktif' : ' is-gecti'}`}
                  onClick={() => noktayaGit(ders.noktalar.indexOf(nokta))}
                  title="Bu adımın konu anlatımına git"
                >
                  <BookOpenText aria-hidden />
                  <span>
                    Anlatım ({s?.tip === 'anlatim' && aktifCumle >= 0 ? `${aktifCumle + 1}/` : ''}{nokta.cumleler.length})
                  </span>
                </button>
                {aktifNoktaSorular.map((q, qi) => {
                  const r = sonuc[q.k];
                  const aktifSoruMu = s?.tip === 'soru' && s.qi === qi;
                  return (
                    <button
                      key={q.k}
                      type="button"
                      className={`pa-asama-hap${aktifSoruMu ? ' is-aktif' : ''}${r === 'd' ? ' is-d' : r === 'd2' ? ' is-d2' : r === 'y' ? ' is-y' : ''}`}
                      onClick={() => noktayaGit(ders.noktalar.indexOf(nokta), qi)}
                      title={`${qi + 1}. soruya git (${TUR_AD[q.tur]})`}
                    >
                      <HelpCircle aria-hidden />
                      <span>
                        S{qi + 1} <small>({TUR_KISA[q.tur]})</small>
                      </span>
                      {r === 'd' && <Check className="pa-asama-i" aria-hidden />}
                      {r === 'd2' && <span className="pa-asama-rozet">~</span>}
                      {r === 'y' && <X className="pa-asama-i" aria-hidden />}
                    </button>
                  );
                })}
              </div>
            )}

            <div className="pa-ilerleme-sag">
              {sonKalinanNokta && nokta?.id !== sonKalinanNokta.id && (
                <button
                  type="button"
                  className="pa-son-kalinan-btn"
                  onClick={sonKalinanaGit}
                  title={`En son kalınan ilerleme noktasına git: ${sonKalinanSira}. Adım — ${sonKalinanNokta.baslik}`}
                >
                  <Target aria-hidden />
                  <span>Kalınan: <b>{sonKalinanSira}. adım</b></span>
                </button>
              )}
              {sonKalinanNokta && nokta && nokta.id !== sonKalinanNokta.id && (
                <button
                  type="button"
                  className="pa-burayi-kaydet-btn"
                  onClick={() => kalinanYeriBurayaTasi(nokta.id)}
                  title={`Kalınan ilerleme noktasını şu anki adıma (${noktaSirasi}. adım) taşı`}
                  aria-label="Burayı kaldığım yer yap"
                >
                  <MapPin aria-hidden />
                  <span>Burayı sabitle</span>
                </button>
              )}
              {sonKalinanNokta && nokta?.id === sonKalinanNokta.id && (
                <span className="pa-son-kalinan-etiket" title="Şu an en son kaldığın ilerleme adımındasın">
                  <MapPin aria-hidden />
                  <span>Kalınan adım</span>
                </span>
              )}

              <div className="pa-ilerleme-istatistik" role="status" aria-label="Soru ve adım ilerleme özeti">
                <span className="pa-ist-soru" title={`Toplam ${sorulanlar.length} sorudan ${cozulenSoruSayisi} tanesi yanıtlandı`}>
                  {cozulenSoruSayisi}/{sorulanlar.length} soru
                </span>
                {ilkDogru > 0 && <span className="pa-ist-d" title="İlk denemede doğru">{ilkDogru}✓</span>}
                {yardimliDogru > 0 && <span className="pa-ist-d2" title="Yardımla veya 2. denemede doğru">{yardimliDogru}~</span>}
                {yanlisSayisi > 0 && <span className="pa-ist-y" title="Yanlış veya cevabı gösterildi">{yanlisSayisi}✗</span>}
              </div>
            </div>
          </div>

          {/* 2. Satır: İnce Görsel Segment Şeridi ve Yüzen Önizleme */}
          <div className="pa-ilerleme-serit-sar" onMouseLeave={() => setHoverNoktaIdx(null)}>
            <div className="pa-ilerleme" role="navigation" aria-label={`Adım ilerleme çubuğu: ${noktaSirasi} / ${gorunenNoktalar.length}`}>
              {gorunenNoktalar.map((ni, j) => {
                const nk = ders.noktalar[ni];
                const simdi = nokta === nk;
                const sonKalinanMi = sonKalinanNid === nk.id;
                const okunduMu = okunanNoktalar.has(nk.id) || j < noktaSirasi - (simdi ? 1 : 0);
                const yeniBolum = j > 0 && ders.noktalar[gorunenNoktalar[j - 1]].bolum !== nk.bolum;
                const qs = tekrar ? nk.sorular.filter((q) => tekrar.has(q.k)) : sorulariSec(nk, tercih.yogunluk);
                return (
                  <button
                    key={nk.id}
                    type="button"
                    className={`pa-seg${simdi ? ' is-simdi' : ''}${sonKalinanMi && !simdi ? ' is-son-kalinan' : ''}${okunduMu ? ' is-gecti' : ''}${segSinif(nk)}${nk.aday ? ' is-aday' : ''}${yeniBolum ? ' is-bolum' : ''}`}
                    onClick={() => noktayaGit(ni)}
                    onMouseEnter={() => setHoverNoktaIdx(j)}
                    onFocus={() => setHoverNoktaIdx(j)}
                    onBlur={() => setHoverNoktaIdx(null)}
                    aria-label={`${j + 1}. adım (${1 + qs.length} aşama, ${qs.length} soru): ${nk.baslik}${simdi ? ' — Şu an buradasın' : ''}${sonKalinanMi ? ' — En son kalınan adım' : ''}`}
                    aria-current={simdi ? 'step' : undefined}
                  />
                );
              })}
            </div>

            {hoverNoktaIdx !== null && gorunenNoktalar[hoverNoktaIdx] !== undefined && (() => {
              const hNi = gorunenNoktalar[hoverNoktaIdx];
              const hNk = ders.noktalar[hNi];
              if (!hNk) return null;
              const hQs = tekrar ? hNk.sorular.filter((q) => tekrar.has(q.k)) : sorulariSec(hNk, tercih.yogunluk);
              const hDogru = hQs.filter((q) => sonuc[q.k] === 'd').length;
              const hYardim = hQs.filter((q) => sonuc[q.k] === 'd2').length;
              const hYanlis = hQs.filter((q) => sonuc[q.k] === 'y').length;
              const hSimdi = nokta === hNk;
              const hSonKalinan = sonKalinanNid === hNk.id;
              return (
                <div className="pa-seg-onizleme" role="status">
                  <span className="pa-onizleme-no">{hoverNoktaIdx + 1}. Adım / {gorunenNoktalar.length}</span>
                  <span className="pa-onizleme-bolum">Bölüm {hNk.bolum + 1}: {ders.bolumler[hNk.bolum]?.baslik}</span>
                  <b className="pa-onizleme-baslik">{hNk.baslik}</b>
                  <span className="pa-onizleme-icerik">
                    {1 + hQs.length} aşama: 1 anlatım ({hNk.cumleler.length} cümle) + {hQs.length} soru
                  </span>
                  {hSimdi && <span className="pa-onizleme-etiket is-simdi">Şu an buradasın</span>}
                  {hSonKalinan && !hSimdi && <span className="pa-onizleme-etiket is-kalinan">Son kalınan yer</span>}
                  {(hDogru > 0 || hYardim > 0 || hYanlis > 0) && (
                    <span className="pa-onizleme-sonuc">
                      {hDogru > 0 ? `${hDogru} doğru ` : ''}
                      {hYardim > 0 ? `${hYardim} yardımlı ` : ''}
                      {hYanlis > 0 ? `${hYanlis} yanlış` : ''}
                    </span>
                  )}
                </div>
              );
            })()}
          </div>

          {/* Açılır Adım ve İlerleme Yöneticisi Paneli */}
          {adimPanelAcik && (
            <div className="pa-adim-panel" role="region" aria-label="Adım ve İlerleme Yöneticisi">
              <div className="pa-adim-panel-ust">
                <div className="pa-adim-panel-baslik">
                  <div>
                    <h3>Adım ve İlerleme Yöneticisi</h3>
                    <p>
                      Toplam <b>{ders.bolumler.length} bölüm</b>, <b>{gorunenNoktalar.length} adım</b> ({adimSayilari.toplamCumle} anlatım cümlesi) ve <b>{sorulanlar.length} soru</b>
                    </p>
                  </div>
                  <button type="button" className="pa-ikon" onClick={() => setAdimPanelAcik(false)} aria-label="Paneli kapat"><X /></button>
                </div>

                {/* Hızlı Durum Kartları */}
                <div className="pa-adim-ozet-izgara">
                  <div className="pa-adim-ozet-kart is-konum">
                    <small>Şu anki konumun</small>
                    <b>{nokta ? `${noktaSirasi} / ${gorunenNoktalar.length}. Adım` : s?.tip === 'giris' ? 'Ders Girişi' : s?.tip === 'bolum' ? `Bölüm ${s.b + 1} Girişi` : 'Ders Sonu'}</b>
                    <span>
                      {nokta
                        ? `${nokta.baslik} (Aşama ${aktifAsamaNo}/${aktifToplamAsama})`
                        : 'Adım seçerek doğrudan geçebilirsin'}
                    </span>
                  </div>
                  <div className="pa-adim-ozet-kart is-kalinan">
                    <small>En son kalınan ilerleme noktası</small>
                    <b>{sonKalinanNokta ? `${sonKalinanSira} / ${gorunenNoktalar.length}. Adım` : 'Henüz başlanmadı'}</b>
                    <span>{sonKalinanNokta ? sonKalinanNokta.baslik : 'İlerledikçe otomatik kaydedilir'}</span>
                  </div>
                  <div className="pa-adim-ozet-kart">
                    <small>Tamamlanan adım & soru</small>
                    <b>{adimSayilari.tamam}/{gorunenNoktalar.length} adım · {cozulenSoruSayisi}/{sorulanlar.length} soru</b>
                    <span>{ilkDogru} ilk denemede doğru · {yardimliDogru} yardımlı · {yanlisSayisi} yanlış</span>
                  </div>
                </div>

                {/* Hızlı Yönetim Aksiyonları */}
                <div className="pa-yonet-aksiyonlar">
                  {sonKalinanNokta && (
                    <button
                      type="button"
                      className="pa-yonet-btn is-vurgu"
                      onClick={sonKalinanaGit}
                      disabled={nokta?.id === sonKalinanNokta.id && !devamSor}
                    >
                      <Target aria-hidden />
                      <span>Son kalınan yere git ({sonKalinanSira}. adım)</span>
                    </button>
                  )}
                  {adimSayilari.kalan > 0 && (
                    <button type="button" className="pa-yonet-btn" onClick={siradakiCozulmemiseGit}>
                      <Play aria-hidden />
                      <span>Sıradaki çözülmemiş adıma git ({adimSayilari.kalan} kalan)</span>
                    </button>
                  )}
                  {adimSayilari.tekrar > 0 && (
                    <button type="button" className="pa-yonet-btn is-uyari" onClick={ilkTekraraGit}>
                      <RotateCcw aria-hidden />
                      <span>Yanlış / yardımlı ilk adıma git ({adimSayilari.tekrar} adım)</span>
                    </button>
                  )}
                  {nokta && nokta.id !== sonKalinanNid && (
                    <button type="button" className="pa-yonet-btn" onClick={() => kalinanYeriBurayaTasi(nokta.id)}>
                      <MapPin aria-hidden />
                      <span>Şu anki adımı ({noktaSirasi}. adım) kalınan yer yap</span>
                    </button>
                  )}
                  {!sifirlaOnay ? (
                    <button type="button" className="pa-yonet-btn is-tehlike" onClick={() => setSifirlaOnay(true)}>
                      <Trash2 aria-hidden />
                      <span>İlerlemeyi sıfırla</span>
                    </button>
                  ) : (
                    <div className="pa-sifirla-onay">
                      <span>Tüm ilerleme sıfırlansın mı?</span>
                      <button type="button" className="pa-yonet-btn is-tehlike-dolu" onClick={ilerlemeyiSifirla}>Evet, sıfırla</button>
                      <button type="button" className="pa-yonet-btn" onClick={() => setSifirlaOnay(false)}>Vazgeç</button>
                    </div>
                  )}
                </div>

                {/* Renk Rehberi (Lejant) ve Filtre Sekmeleri */}
                <div className="pa-adim-alt-cubuk">
                  <div className="pa-adim-filtreler" role="tablist" aria-label="Adım filtreleri">
                    <button type="button" role="tab" aria-selected={adimFiltre === 'hepsi'} className={adimFiltre === 'hepsi' ? 'is-on' : ''} onClick={() => setAdimFiltre('hepsi')}>
                      Tümü ({gorunenNoktalar.length})
                    </button>
                    <button type="button" role="tab" aria-selected={adimFiltre === 'kalan'} className={adimFiltre === 'kalan' ? 'is-on' : ''} onClick={() => setAdimFiltre('kalan')}>
                      Kalanlar ({adimSayilari.kalan})
                    </button>
                    <button type="button" role="tab" aria-selected={adimFiltre === 'tekrar'} className={adimFiltre === 'tekrar' ? 'is-on' : ''} onClick={() => setAdimFiltre('tekrar')}>
                      Tekrar Gereken ({adimSayilari.tekrar})
                    </button>
                    <button type="button" role="tab" aria-selected={adimFiltre === 'tamam'} className={adimFiltre === 'tamam' ? 'is-on' : ''} onClick={() => setAdimFiltre('tamam')}>
                      Tamamlanan ({adimSayilari.tamam})
                    </button>
                    {adimSayilari.aday > 0 && (
                      <button type="button" role="tab" aria-selected={adimFiltre === 'aday'} className={adimFiltre === 'aday' ? 'is-on' : ''} onClick={() => setAdimFiltre('aday')}>
                        Sınav Adayı ({adimSayilari.aday})
                      </button>
                    )}
                  </div>
                  <div className="pa-lejant" aria-label="Renk açıklamaları">
                    <span><i className="l-simdi" />Şu anki adım</span>
                    <span><i className="l-kalinan" />Son kalınan</span>
                    <span><i className="l-d" />İlk denemede doğru</span>
                    <span><i className="l-d2" />Yardımlı</span>
                    <span><i className="l-y" />Yanlış</span>
                    <span><i className="l-okundu" />Okundu</span>
                  </div>
                </div>
              </div>

              {/* Bölüm Bölüm Adım Listesi */}
              <div className="pa-adim-panel-liste">
                {ders.bolumler.map((b, bi) => {
                  const bolumAdimlari = gorunenNoktalar
                    .map((ni, j) => ({ ni, sira: j + 1, nk: ders.noktalar[ni] }))
                    .filter((x) => x.nk.bolum === bi)
                    .filter((x) => {
                      if (adimFiltre === 'hepsi') return true;
                      if (adimFiltre === 'aday') return !!x.nk.aday;
                      const d = adimDurum(x.nk);
                      if (adimFiltre === 'tamam') return d === 'tamam';
                      if (adimFiltre === 'tekrar') return d === 'yanlis' || d === 'yardimli';
                      return d === 'bekliyor' || d === 'okundu' || d === 'kismi';
                    });
                  if (!bolumAdimlari.length) return null;
                  const bolumToplamSoru = bolumAdimlari.reduce((acc, x) => acc + (tekrar ? x.nk.sorular.filter((q) => tekrar.has(q.k)) : sorulariSec(x.nk, tercih.yogunluk)).length, 0);
                  return (
                    <div key={bi} className="pa-adim-bolum-grup">
                      <div className="pa-adim-bolum-baslik">
                        <span>Bölüm {bi + 1}/{ders.bolumler.length}: <b>{b.baslik}</b></span>
                        <small>{bolumAdimlari.length} adım · {bolumToplamSoru} soru</small>
                      </div>
                      <div className="pa-adim-satirlar">
                        {bolumAdimlari.map(({ ni, sira, nk }) => {
                          const qs = tekrar ? nk.sorular.filter((q) => tekrar.has(q.k)) : sorulariSec(nk, tercih.yogunluk);
                          const durum = adimDurum(nk);
                          const simdiMi = nokta === nk;
                          const sonKalinanMi = sonKalinanNid === nk.id;
                          return (
                            <div key={nk.id} className={`pa-adim-satir d-${durum}${simdiMi ? ' is-simdi' : ''}${sonKalinanMi ? ' is-kalinan' : ''}`}>
                              <div className="pa-adim-satir-sol" onClick={() => noktayaGit(ni)} role="button" tabIndex={0} onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); noktayaGit(ni); } }}>
                                <span className={`pa-adim-no d-${durum}${simdiMi ? ' is-simdi' : ''}`}>{sira}</span>
                                <div className="pa-adim-metin">
                                  <div className="pa-adim-ust-satir">
                                    <b>{nk.baslik}</b>
                                    {simdiMi && <span className="pa-etiket-hap is-simdi">Şu an buradasın</span>}
                                    {sonKalinanMi && <span className="pa-etiket-hap is-kalinan">Son kalınan yer</span>}
                                    {nk.aday && <span className="pa-etiket-hap is-aday"><Star aria-hidden />Aday {nk.aday}</span>}
                                  </div>
                                  <div className="pa-adim-alt-bilgi">
                                    <span><b>{1 + qs.length} aşama:</b> 1 konu anlatımı ({nk.cumleler.length} cümle) + {qs.length} soru</span>
                                  </div>
                                </div>
                              </div>
                              <div className="pa-adim-satir-sag">
                                <button type="button" className={`pa-mini-gecis${simdiMi && s?.tip === 'anlatim' ? ' is-on' : ''}`} onClick={() => noktayaGit(ni)} title="Konu anlatımına git">
                                  <BookOpenText aria-hidden />
                                  <span>Anlatım ({nk.cumleler.length})</span>
                                </button>
                                {qs.map((q, qi) => {
                                  const r = sonuc[q.k];
                                  const aktifSoru = simdiMi && s?.tip === 'soru' && s.qi === qi;
                                  return (
                                    <button
                                      key={q.k}
                                      type="button"
                                      className={`pa-mini-gecis is-soru${aktifSoru ? ' is-on' : ''}${r === 'd' ? ' is-d' : r === 'd2' ? ' is-d2' : r === 'y' ? ' is-y' : ''}`}
                                      onClick={() => noktayaGit(ni, qi)}
                                      title={`${qi + 1}. soruya git (${TUR_AD[q.tur]})`}
                                    >
                                      <span>S{qi + 1}</span>
                                      {r === 'd' && <Check aria-hidden />}
                                      {r === 'd2' && <b>~</b>}
                                      {r === 'y' && <X aria-hidden />}
                                    </button>
                                  );
                                })}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      <main className="pa-sahne" ref={kokRef}>
        {hata && <div className="pa-bos"><p>Bu ders için asistan henüz hazır değil.</p><button type="button" className="pa-btn" onClick={onClose}>Kapat</button></div>}
        {!hata && !ders && <div className="pa-bos"><span className="pa-dalga is-yukle" aria-hidden><i /><i /><i /><i /><i /></span><p>Asistan hazırlanıyor…</p></div>}

        {ders && devamSor && (
          <div className="pa-kart pa-devam">
            <small className="pa-etiket">Kaldığın Yer Kayıtlı</small>
            <h2>Kaldığın yerden devam edelim mi?</h2>
            <p>
              <b>{ders.baslik}</b> dersinde toplam <b>{gorunenNoktalar.length} adım</b> içinden{' '}
              <b>{sonKalinanSira}. adımda</b> (“{sonKalinanNokta?.baslik || ders.noktalar.find((n) => n.id === devamSor.nid)?.baslik}”) kalmıştın.
              {cozulenSoruSayisi > 0 ? ` Şimdiye kadar ${sorulanlar.length} sorudan ${cozulenSoruSayisi} tanesini yanıtladın (${ilkDogru} doğru).` : ''}
            </p>
            <div className="pa-btnler">
              <button type="button" className="pa-btn is-dolu" onClick={() => {
                setDevamSor(null);
                sonKalinanaGit();
              }}><Play aria-hidden />Kaldığım yerden devam et ({sonKalinanSira}. adım)</button>
              <button type="button" className="pa-btn" onClick={() => {
                setDevamSor(null);
                setAdimPanelAcik(true);
              }}><ListChecks aria-hidden />Adımları gör ve seç</button>
              <button type="button" className="pa-btn" onClick={() => {
                setI(0); setDevamSor(null);
              }}><RotateCcw aria-hidden />Girişe git (İlerlemeyi koru)</button>
              <button type="button" className="pa-btn" onClick={ilerlemeyiSifirla}><Trash2 aria-hidden />Sıfırla ve baştan başla</button>
            </div>
          </div>
        )}

        {ders && s && !devamSor && (
          <div className="pa-icerik" key={`${tekrar ? 't' : ''}${i}`}>
            <div className="pa-asistan" aria-live="polite">
              <span className="pa-dalga" aria-hidden><i /><i /><i /><i /><i /></span>
              <span className="pa-durum">
                {s.tip === 'soru'
                  ? (yardim ? (caliyor ? 'Şıkları tek tek açıklıyor…' : cozuldu ? 'Devam edebilirsin' : 'Şimdi bir şık seç')
                    : !cozuldu && !secim ? (caliyor ? 'Soruyu okuyor…' : 'Cevabını bekliyor')
                    : secim && !cozuldu ? (caliyor ? 'Neden yanlış olduğunu anlatıyor…' : 'Bir daha dene ya da yardım al')
                    : caliyor ? 'Açıklıyor…' : 'Devam edebilirsin')
                  : caliyor ? 'Anlatıyor…' : sesYok ? 'Metinle ilerliyor (ses hazırlanıyor)' : 'Duraklatıldı'}
              </span>
            </div>

            {s.tip === 'giris' && (
              <section className="pa-kart pa-giris">
                <small className="pa-etiket">{ders.no}. ders · {ders.bolumler.length} bölüm · {ders.noktalar.length} nokta · {tumSorular.length} soru</small>
                <h1>{ders.baslik}</h1>
                <div className="pa-cumleler" role="region" aria-label="Giriş cümleleri">
                  {ders.giris.map((c, j) => {
                    const yId = `as_${kod}_giris_${j}`;
                    const yildizli = yildizliMi(yId);
                    return (
                      <div key={j} className="pa-cumle-sar">
                        <p
                          data-c={j}
                          className={`${j === aktifCumle ? 'is-aktif' : j < aktifCumle ? 'is-gecti' : ''} is-tiklanabilir`}
                          onClick={() => cumleyeGit(j)}
                          title="Bu cümleyi dinle"
                          role="button"
                          tabIndex={0}
                          onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); cumleyeGit(j); } }}
                        >
                          <Metin metin={c} />
                        </p>
                        <button
                          type="button"
                          className={`pa-p-yildiz${yildizli ? ' is-on' : ''}`}
                          onClick={(e) => {
                            e.stopPropagation();
                            yildizToggle({
                              id: yId,
                              kaynak: 'asistan',
                              kaynakAd: 'Sınav asistanı',
                              baslik: `${ders.baslik} · Giriş`,
                              metin: c,
                              deeplink: `/en-onemliler?brans=${kodBrans(kod)}&ders=${kod}&asistan=1&p=${j}`,
                              meta: { dersKod: kod, brans: kodBrans(kod), paragrafIndex: j },
                            });
                          }}
                          aria-label={yildizli ? 'Listemden çıkar' : 'Listeme ekle'}
                          title={yildizli ? 'Yıldızlı (tekrar listesinde)' : 'Yıldızla (tekrar listesine ekle)'}
                        >
                          <Star fill={yildizli ? '#f59e0b' : 'none'} color={yildizli ? '#f59e0b' : 'currentColor'} aria-hidden />
                        </button>
                      </div>
                    );
                  })}
                </div>
                <ol className="pa-plan">
                  {ders.bolumler.map((b, j) => {
                    const bAdimlar = gorunenNoktalar.filter((ni) => ders.noktalar[ni]?.bolum === j);
                    const bSorular = bAdimlar.reduce((acc, ni) => acc + sorulariSec(ders.noktalar[ni], tercih.yogunluk).length, 0);
                    return (
                      <li
                        key={j}
                        className="is-tiklanabilir"
                        onClick={() => {
                          const x = sahneler.findIndex((y) => y.tip === 'bolum' && y.b === j);
                          if (x >= 0) setI(x);
                          else if (bAdimlar.length > 0) noktayaGit(bAdimlar[0]);
                        }}
                        role="button"
                        tabIndex={0}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault();
                            const x = sahneler.findIndex((y) => y.tip === 'bolum' && y.b === j);
                            if (x >= 0) setI(x);
                            else if (bAdimlar.length > 0) noktayaGit(bAdimlar[0]);
                          }
                        }}
                        title={`${j + 1}. bölüme git`}
                      >
                        <span>{j + 1}</span>
                        <span className="pa-plan-baslik">{b.baslik}</span>
                        <small className="pa-plan-meta">{bAdimlar.length} adım · {bSorular} soru</small>
                      </li>
                    );
                  })}
                </ol>
                {bransTanim(kodBrans(kod)).sinavKurali && <p className="pa-kural">Sınav kuralı: tablo, şekil ve klinik bulgu sorulmaz · her slayttan {ders.soruSayisi} soru.</p>}
                <div className="pa-kart-aksiyonlar">
                  <button type="button" className="pa-btn-parca is-sade" onClick={tekrarDinle} title="Baştan dinle ( T )"><RotateCcw aria-hidden /><span>Baştan dinle</span></button>
                  <button type="button" className="pa-btn-akıs is-dolu" onClick={ileri}><span>Derse başla</span><ChevronRight aria-hidden /></button>
                </div>
              </section>
            )}

            {s.tip === 'bolum' && (
              <section className="pa-kart pa-bolum">
                <small className="pa-etiket">Bölüm {s.b + 1} / {ders.bolumler.length}</small>
                <h1>{ders.bolumler[s.b].baslik}</h1>
                <div className="pa-cumleler"><p className={`${aktifCumle === 0 ? 'is-aktif' : ''} is-tiklanabilir`} onClick={() => cumleyeGit(0)} role="button" tabIndex={0} title="Bu açıklamayı dinle"><Metin metin={ders.bolumler[s.b].neden} /></p></div>
                <ul className="pa-bolum-l">
                  {ders.noktalar.filter((n) => n.bolum === s.b && gorunenNoktalar.includes(ders.noktalar.indexOf(n))).map((n) => {
                    const ni = ders.noktalar.indexOf(n);
                    const gSira = gorunenNoktalar.indexOf(ni) + 1;
                    const qs = sorulariSec(n, tercih.yogunluk);
                    return (
                      <li
                        key={n.id}
                        className="is-tiklanabilir"
                        onClick={() => noktayaGit(ni)}
                        role="button"
                        tabIndex={0}
                        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); noktayaGit(ni); } }}
                        title={`${gSira}. adıma git: ${n.baslik}`}
                      >
                        {n.aday ? <Star aria-hidden className="is-aday" /> : <span className="pa-nokta" aria-hidden />}
                        <span><b>{gSira}.</b> {n.baslik}</span>
                        <small>{1 + qs.length} aşama · {n.cumleler.length} cümle{qs.length > 0 ? ` · ${qs.length} soru` : ''}</small>
                      </li>
                    );
                  })}
                </ul>
                <div className="pa-kart-aksiyonlar">
                  <button type="button" className="pa-btn-parca is-tek" onClick={tekrarDinle} title="Bölüm girişini tekrar dinle ( T )"><RotateCcw aria-hidden /><span>Tekrar dinle</span></button>
                  <button type="button" className="pa-btn-akıs is-dolu" onClick={ileri}><span>Bölüme başla</span><ChevronRight aria-hidden /></button>
                </div>
              </section>
            )}

            {s.tip === 'anlatim' && nokta && (
              <section className={`pa-kart pa-anlatim${nokta.aday ? ' is-aday' : ''}`}>
                <div className="pa-meta">
                  <span className="pa-puan">{nokta.puan}</span>
                  {nokta.aday && <span className={`pa-aday${nokta.aday <= ders.soruSayisi ? ' is-en' : ''}`}><Star aria-hidden />{nokta.aday <= ders.soruSayisi ? 'En olası soru' : `Sınav adayı ${nokta.aday}`}</span>}
                  {(nokta.kategori === 'prognoz' || nokta.kategori === 'tedavi') && <span className="pa-kat">{nokta.kategori === 'prognoz' ? 'Prognoz' : 'Tedavi'} · sorulabilir</span>}
                  <span className="pa-sayac">{noktaSirasi} / {gorunenNoktalar.length}</span>
                </div>
                <h2>{nokta.baslik}</h2>
                <div className="pa-cumleler" role="region" aria-label="Anlatım cümleleri">
                  {nokta.cumleler.map((c, j) => {
                    const yId = `as_${kod}_${nokta.id}_${j}`;
                    const yildizli = yildizliMi(yId);
                    return (
                      <div key={j} className="pa-cumle-sar">
                        <p
                          data-c={j}
                          className={`${j === aktifCumle ? 'is-aktif' : j < aktifCumle ? 'is-gecti' : ''} is-tiklanabilir`}
                          onClick={() => cumleyeGit(j)}
                          title="Bu cümleyi dinlemek için dokun"
                          role="button"
                          tabIndex={0}
                          onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); cumleyeGit(j); } }}
                        >
                          <Metin metin={c} />
                        </p>
                        <button
                          type="button"
                          className={`pa-p-yildiz${yildizli ? ' is-on' : ''}`}
                          onClick={(e) => {
                            e.stopPropagation();
                            yildizToggle({
                              id: yId,
                              kaynak: 'asistan',
                              kaynakAd: 'Sınav asistanı',
                              baslik: `${ders.baslik}: ${nokta.baslik}`,
                              altBaslik: ders.bolumler[nokta.bolum]?.baslik || `Nokta ${noktaSirasi}`,
                              metin: c,
                              deeplink: `/en-onemliler?brans=${kodBrans(kod)}&ders=${kod}&asistan=1&nid=${nokta.id}&p=${j}`,
                              meta: {
                                dersKod: kod,
                                brans: kodBrans(kod),
                                noktaId: nokta.id,
                                paragrafIndex: j,
                              },
                            });
                          }}
                          aria-label={yildizli ? 'Listemden çıkar' : 'Listeme ekle'}
                          title={yildizli ? 'Yıldızlı (tekrar listesinde)' : 'Yıldızla (tekrar listesine ekle)'}
                        >
                          <Star fill={yildizli ? '#f59e0b' : 'none'} color={yildizli ? '#f59e0b' : 'currentColor'} aria-hidden />
                        </button>
                      </div>
                    );
                  })}
                </div>
                {(() => {
                  const hapId = `as_${kod}_${nokta.id}_hap`;
                  const yildizliHap = yildizliMi(hapId);
                  return (
                    <div className="pa-hap pa-hap-sar">
                      <span>Akılda kalsın</span>
                      <p><Metin metin={nokta.bilgi} /></p>
                      <button
                        type="button"
                        className={`pa-p-yildiz${yildizliHap ? ' is-on' : ''}`}
                        onClick={(e) => {
                          e.stopPropagation();
                          yildizToggle({
                            id: hapId,
                            kaynak: 'asistan',
                            kaynakAd: 'Sınav asistanı',
                            baslik: `${ders.baslik}: ${nokta.baslik}`,
                            altBaslik: 'Akılda kalsın',
                            metin: nokta.bilgi,
                            deeplink: `/en-onemliler?brans=${kodBrans(kod)}&ders=${kod}&asistan=1&nid=${nokta.id}&p=hap`,
                            meta: {
                              dersKod: kod,
                              brans: kodBrans(kod),
                              noktaId: nokta.id,
                            },
                          });
                        }}
                        aria-label={yildizliHap ? 'Listemden çıkar' : 'Listeme ekle'}
                        title={yildizliHap ? 'Yıldızlı (tekrar listesinde)' : 'Yıldızla (tekrar listesine ekle)'}
                      >
                        <Star fill={yildizliHap ? '#f59e0b' : 'none'} color={yildizliHap ? '#f59e0b' : 'currentColor'} aria-hidden />
                      </button>
                    </div>
                  );
                })()}

                <div className="pa-kart-aksiyonlar">
                  <button type="button" className="pa-btn-parca is-sade" onClick={tekrarDinle} title="Baştan dinle ( T )"><RotateCcw aria-hidden /><span>Baştan dinle</span></button>

                  {sorulariSec(nokta, tercih.yogunluk).length > 0 ? (
                    <button
                      type="button"
                      className="pa-btn-akıs is-dolu"
                      onClick={ileri}
                      title="Bu noktanın sorularına geç"
                    >
                      <ListChecks aria-hidden />
                      <span>Soruları çöz ({sorulariSec(nokta, tercih.yogunluk).length})</span>
                      <ChevronRight aria-hidden />
                    </button>
                  ) : (
                    <button
                      type="button"
                      className="pa-btn-akıs is-dolu"
                      onClick={ileri}
                      title="Sonraki konuya geç"
                    >
                      <span>Sonraki konu</span>
                      <ChevronRight aria-hidden />
                    </button>
                  )}
                </div>
              </section>
            )}

            {s.tip === 'soru' && (() => {
              const q = s.q;
              const harfler = Object.keys(q.secenekler);
              const aciklama = cozuldu ? q.dogruMetin : secim && secim !== q.dogru ? q.yanlis[secim] : null;
              const yardimHarfler = Object.keys(q.yardim);
              const yardimAktif = yardim && klipAdi === `h-${q.k}` && caliyor ? yardimHarfler[aktifCumle] : null;
              return (
                <section className="pa-kart pa-soru">
                  <div className="pa-meta">
                    <span className={`pa-soru-tur t-${q.tur}`}>{TUR_AD[q.tur]}</span>
                    {q.sinav && <span className="pa-sinav">{q.sinav}</span>}
                    <span className="pa-sayac">{s.qn > 1 ? `Soru ${s.qi + 1}/${s.qn} · ` : ''}{noktaSirasi} / {gorunenNoktalar.length}</span>
                  </div>
                  <h2 className={klipAdi === `q-${q.k}` && caliyor ? 'is-aktif' : ''}>{q.kok}</h2>
                  <div className="pa-siklar" role="group" aria-label="Şıklar">
                    {Object.entries(q.secenekler).map(([h, v], n) => {
                      const durum = cozuldu && h === q.dogru ? ' is-dogru' : elenen.includes(h) ? ' is-yanlis' : cozuldu ? ' is-sonuk' : '';
                      const cizik = !cozuldu && !elenen.includes(h) && cizili.includes(h);
                      return (
                        <div key={h} className="sik-sar">
                        <button type="button" className={`pa-sik${durum}${cizik ? ' is-cizili' : ''}${secim === h ? ' is-secili' : ''}${yardimAktif === h ? ' is-yardim' : ''}`} disabled={!!cozuldu || elenen.includes(h)} onClick={() => cevapla(h)}
                          aria-label={`${h} şıkkı: ${v}`}>
                          <b>{h}</b><span>{v}</span><kbd aria-hidden>{n + 1}</kbd>
                          {cozuldu && h === q.dogru && <Check className="pa-sik-i" aria-hidden />}
                          {elenen.includes(h) && <X className="pa-sik-i" aria-hidden />}
                        </button>
                        {!cozuldu && !elenen.includes(h) && (
                          <button type="button" className={`sik-ciz${cizik ? ' is-on' : ''}`} onClick={() => ciz(h)} aria-pressed={cizik}
                            aria-label={cizik ? `${h} şıkkının üstündeki çizgiyi kaldır` : `${h} şıkkını kendin ele (üstünü çiz)`} title={cizik ? 'Çizgiyi kaldır' : 'Şıkkı ele'}><Strikethrough aria-hidden /></button>
                        )}
                        </div>
                      );
                    })}
                  </div>
                  {aciklama && !yardim && (
                    <div className={`pa-geri${cozuldu === 'dogru' ? ' is-dogru' : cozuldu ? ' is-goster' : ' is-yanlis'}`} aria-live="polite">
                      <b>{cozuldu === 'dogru' ? (sonuc[q.k] === 'd' ? 'Doğru!' : 'Doğru, bu sefer oldu!') : cozuldu ? `Doğru cevap ${q.dogru}` : `${secim} neden yanlış?`}</b>
                      <p className={aktifCumle === 0 && caliyor ? 'is-aktif' : ''}><Metin metin={aciklama.replace(/^Doğru!\s*/, '')} /></p>
                    </div>
                  )}
                  {yardim && (
                    <div className="pa-yardim" aria-live="polite">
                      <b><LifeBuoy aria-hidden />Şık şık kısa açıklama</b>
                      <ul>
                        {yardimHarfler.map((h) => (
                          <li key={h} className={`${yardimAktif === h ? 'is-aktif' : ''}${cozuldu && h === q.dogru ? ' is-dogru' : ''}${elenen.includes(h) ? ' is-elenen' : ''}`}>
                            <span className="pa-yardim-h">{h}</span><span><Metin metin={q.yardim[h] || ''} /></span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  <div className="pa-btnler">
                    {!cozuldu && secim && !yardim && <span className="pa-ipucu">Yanlış şık elendi — başka bir şık seç.</span>}
                    {!cozuldu && (
                      <button type="button" className="pa-btn" onClick={() => cal(`q-${q.k}`, [q.kok])} title="Soruyu tekrar dinle">
                        <RotateCcw aria-hidden />
                        Soruyu tekrar dinle
                      </button>
                    )}
                    {cozuldu && (
                      <button type="button" className="pa-btn" onClick={() => cal(`d-${q.k}`, [q.dogruMetin])} title="Açıklamayı tekrar dinle">
                        <RotateCcw aria-hidden />
                        Açıklamayı tekrar dinle
                      </button>
                    )}
                    {!yardim && <button type="button" className="pa-btn is-yardim" onClick={yardimAl}><LifeBuoy aria-hidden />{cozuldu ? 'Tüm şıkları açıkla' : 'Yardım al'}</button>}
                    {yardim && <button type="button" className="pa-btn" onClick={yardimAl}><RotateCcw aria-hidden />Tüm şıkları tekrar dinle</button>}
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
                <div className="pa-cumleler" role="region" aria-label="Özet cümleleri">
                  {ders.kapanis.map((c, j) => (
                    <p
                      key={j}
                      className={`${j === aktifCumle ? 'is-aktif' : j < aktifCumle ? 'is-gecti' : ''} is-tiklanabilir`}
                      onClick={() => cumleyeGit(j)}
                      title="Bu cümleyi dinle"
                      role="button"
                      tabIndex={0}
                      onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); cumleyeGit(j); } }}
                    >
                      <Metin metin={c} />
                    </p>
                  ))}
                </div>
                <div className="pa-kart-aksiyonlar">
                  <button type="button" className="pa-btn-parca is-sade" onClick={tekrarDinle} title="Baştan dinle ( T )"><RotateCcw aria-hidden /><span>Baştan dinle</span></button>
                  <button type="button" className="pa-btn-akıs is-dolu" onClick={ileri} title="Ders sonuçlarına geç">
                    <span>Sonuçları gör</span>
                    <ChevronRight aria-hidden />
                  </button>
                </div>
              </section>
            )}

            {s.tip === 'son' && (
              <section className="pa-kart pa-son">
                <small className="pa-etiket">{tekrar ? 'Tekrar bitti' : 'Ders bitti'}</small>
                <h1>{ders.baslik}</h1>
                <div className="pa-skor">
                  <div><b>{ilkDogru}</b><span>ilk denemede doğru</span></div>
                  <div><b>{tekrarlar.length}</b><span>tekrar etmelisin{atlanan ? ` (${atlanan} atlanan)` : ''}</span></div>
                  <div><b>{sorulanlar.length}</b><span>soru</span></div>
                </div>
                {tekrarNoktalar.length > 0 && (
                  <div className="pa-yanlis-l">
                    <h3>Tekrar etmen gereken noktalar</h3>
                    <ul>{tekrarNoktalar.map((n) => <li key={n.id}><b>{n.baslik}</b><span><Metin metin={n.bilgi} /></span></li>)}</ul>
                  </div>
                )}
                <div className="pa-son-oneri">
                  <button type="button" className="pa-hero-cozucu" onClick={() => cozucuyuAc(ders.kod)}>
                    <span className="pa-hero-cozucu-i"><Headphones aria-hidden /></span>
                    <span className="pa-hero-cozucu-t">
                      <b>Bu konunun soru çözücü asistanı</b>
                      <small>Çıkmış ve örnek sorularla sesli soru çözümü · şık analizleri ve ipuçları · tam ekran</small>
                    </span>
                    <ChevronRight aria-hidden />
                  </button>
                </div>
                <div className="pa-btnler">
                  {tekrarlar.length > 0 && <button type="button" className="pa-btn is-dolu" onClick={() => { setTekrar(new Set(tekrarlar.map((q) => q.k))); setI(0); }}><RotateCcw aria-hidden />Yanlışlarımı tekrar et</button>}
                  {ilkDogru > 0 && <button type="button" className="pa-btn" onClick={() => ogrenildiAyarla(ders.noktalar.filter((n) => n.sorular.length && n.sorular.every((q) => sonuc[q.k] === 'd')).map((n) => n.id), true)}><Check aria-hidden />Doğru bildiklerimi öğrendim say</button>}
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
      {ogrenAcik && ders && (
        <OgrenYeri brans={kodBrans(kod)} kod={kod} tur="n" id={nokta?.id} baglam={nokta?.baslik} onKapat={() => setOgrenAcik(false)} />
      )}
      {ders && !devamSor && (
        <footer className="pa-alt">
          <div className="pa-oynat">
            <button type="button" className="pa-ikon" onClick={geri} disabled={i === 0} aria-label="Önceki sayfa" title="Önceki sayfa (Sol ok)"><ChevronLeft /></button>
            <button type="button" className="pa-ikon pa-parca-btn" onClick={oncekiCumle} disabled={aktifCumleler.length <= 1} aria-label="Önceki cümle" title="Önceki cümle / parça ( [ )"><SkipBack /></button>
            <button type="button" className="pa-ikon pa-parca-btn" onClick={cumleyiTekrarla} aria-label="Bu cümleyi tekrarla" title="Bu cümleyi / parçayı tekrardan başlat ( R )"><RotateCcw /></button>
            <button type="button" className="pa-buyuk" onClick={oynatDuraklat} aria-label={caliyor ? 'Duraklat' : 'Oynat'} title={caliyor ? 'Duraklat (Boşluk)' : 'Oynat (Boşluk)'}>{caliyor ? <Pause /> : <Play />}</button>
            <button type="button" className="pa-ikon pa-parca-btn" onClick={sonrakiCumle} disabled={aktifCumleler.length <= 1} aria-label="Sonraki cümle" title="Sonraki cümle / parça ( ] )"><SkipForward /></button>
            <button type="button" className="pa-ikon" onClick={ileri} disabled={i >= sahneler.length - 1} aria-label={s?.tip === 'soru' && !cozuldu ? 'Soruyu atla' : 'Sonraki sayfa'} title={s?.tip === 'soru' && !cozuldu ? 'Soruyu atla' : 'Sonraki sayfa (Sağ ok)'}>{s?.tip === 'soru' && !cozuldu ? <SkipForward /> : <ChevronRight />}</button>
          </div>
          <div className="pa-alt-ayrac" aria-hidden />
          <button type="button" className={`pa-ikon pa-ayar-ac${ayarAcik ? ' is-on' : ''}`} onClick={() => setAyarAcik((v) => !v)} aria-expanded={ayarAcik} aria-controls="pa-ayar" aria-label="Oynatma ayarları" title="Soru yoğunluğu, hız, otomatik geçiş"><Settings2 /></button>
          <div className={`pa-ayar${ayarAcik ? ' is-acik' : ''}`} id="pa-ayar">
            <label className="pa-sec" title="Soru yoğunluğu">
              <ListChecks aria-hidden />
              <select value={tercih.yogunluk} onChange={(e) => yogunlukDegis(e.target.value as Yogunluk)} aria-label="Soru yoğunluğu">
                {YOGUNLUK.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
              </select>
            </label>
            <label className="pa-sec" title="Konuşma hızı">
              <Volume2 aria-hidden />
              <select value={tercih.hiz} onChange={(e) => setTercih({ hiz: Number(e.target.value) })} aria-label="Konuşma hızı">
                {HIZLAR.map((h) => <option key={h} value={h}>{h.toLocaleString('tr-TR')}×</option>)}
              </select>
            </label>
            <label className="pa-oto" title="Anlatım bitince sonraki noktaya otomatik geç">
              <input type="checkbox" checked={tercih.otomatik} onChange={(e) => setTercih({ otomatik: e.target.checked })} />
              <span>Otomatik geç</span>
            </label>
          </div>
        </footer>
      )}
      {yildizModalAcik && (
        <YildizliParagraflarModal
          onClose={() => setYildizModalAcik(false)}
          onGecis={(item) => {
            if (item.kaynak === 'asistan' && item.meta?.dersKod === kod) {
              if (item.meta.noktaId) {
                const targetI = sahneler.findIndex(
                  (x) => (x.tip === 'anlatim' || x.tip === 'soru') && ders?.noktalar[x.n]?.id === item.meta!.noktaId
                );
                if (targetI >= 0) {
                  setI(targetI);
                  setDevamSor(null);
                  const hapMi = item.altBaslik === 'Akılda kalsın' || item.id.endsWith('_hap');
                  if (hapMi) {
                    setTimeout(() => {
                      const el = document.querySelector('.pa-hap');
                      if (el) {
                        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        el.classList.remove('is-hedef');
                        void (el as HTMLElement).offsetWidth;
                        el.classList.add('is-hedef');
                        setTimeout(() => el.classList.remove('is-hedef'), 3000);
                      }
                    }, 300);
                  } else if (item.meta.paragrafIndex !== undefined) {
                    const pIdx = item.meta.paragrafIndex;
                    setAktifCumle(pIdx);
                    setTimeout(() => {
                      const el = document.querySelector(`.pa-cumleler [data-c="${pIdx}"]`);
                      if (el) {
                        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        el.classList.remove('is-hedef');
                        void (el as HTMLElement).offsetWidth;
                        el.classList.add('is-hedef');
                        setTimeout(() => el.classList.remove('is-hedef'), 3000);
                      }
                    }, 300);
                  }
                  return true;
                }
              } else if (item.meta.paragrafIndex !== undefined) {
                const targetI = sahneler.findIndex((x) => x.tip === 'giris');
                if (targetI >= 0) {
                  setI(targetI);
                  setDevamSor(null);
                  const pIdx = item.meta.paragrafIndex;
                  setAktifCumle(pIdx);
                  return true;
                }
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

export default PatolojiAsistan;
