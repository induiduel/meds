import React, { useEffect, useMemo, useRef, useState } from 'react';
import { ArrowDown, ArrowUp, Check, X } from 'lucide-react';
import { OyunUst, SonKart, useGecenSure } from './OyunKitV15';
import type { DiPaket, DiTerim } from './dersIcerik';

/**
 * v15 · Ders içerik paketlerinden tek kişilik oyunlar (Oyunlar sayfası). Veri yalnız yayındaki ders içerik paketleri
 * (src/data/ders_icerik/<key>.json; scripts/ders_icerik_uret.py): uydurma soru yok, LLM yok.
 *  - Kaydır (N07): terim + tanım önerme kartı; tanım ya o terimin kendi tanımı ya aynı dersten başka terimin tanımı.
 *    Sağa kaydır / "Doğru", sola / "Yanlış". 12 kart.
 *  - Sırala (F05): paketin sıralı listeleri (`listeler`, sira numara/azalan) ve ilk sütunu "Sıra" olan tablolar; karışık
 *    gelen adımları oklarla doğru sıraya diz. 5 tur.
 *  - Izgara (F07): 6 terim + 6 tanım karışık ızgarada; terimi ve tanımını art arda seç. 3 tur.
 * En iyi skor cihazda (medsoru_oyun_rekor_v1, `<oyun>:<ders|*>`).
 */
export type DersOyun = 'kaydir' | 'sirala' | 'izgara';

const PAKETLER = import.meta.glob('../../data/ders_icerik/*.json') as Record<string, () => Promise<{ default: DiPaket }>>;
const REKOR_KEY = 'medsoru_oyun_rekor_v1';
const karistir = <T,>(a: T[]) => { const r = [...a]; for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; } return r; };
const kacir = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const rekorOku = (k: string): number => { try { return JSON.parse(localStorage.getItem(REKOR_KEY) || '{}')[k] || 0; } catch { return 0; } };
const rekorYaz = (k: string, v: number) => { try { const o = JSON.parse(localStorage.getItem(REKOR_KEY) || '{}'); o[k] = v; localStorage.setItem(REKOR_KEY, JSON.stringify(o)); } catch { /* yok */ } };

/** Bütün ders içerik paketleri (oyun seçilince bir kez yüklenir) */
export function useDersPaketleri() {
  const [p, setP] = useState<DiPaket[] | null>(null);
  useEffect(() => {
    let vaz = false;
    void Promise.all(Object.values(PAKETLER).map((f) => f().then((m) => m.default, () => null)))
      .then((l) => { if (!vaz) setP((l.filter(Boolean) as DiPaket[]).sort((a, b) => a.key.localeCompare(b.key, 'tr', { numeric: true }))); });
    return () => { vaz = true; };
  }, []);
  return p;
}

/** Tanımın ilk cümlesi; terimin adı (ve ilk sözcüğü) tanımda geçiyorsa "…" ile gizlenir */
function tanim(t: DiTerim, sinir: number): string {
  let s = String(t.a || '').split(/(?<=[.!?])\s+/)[0] || '';
  const ad = String(t.t || '').replace(/\s*\(.*?\)\s*/g, ' ').trim();
  for (const x of [ad, ad.split(/\s+/)[0]].filter((y) => y.length > 3)) s = s.replace(new RegExp(`(?<!\\p{L})${kacir(x)}`, 'giu'), '…');
  return s.length > sinir ? `${s.slice(0, sinir - 1)}…` : s;
}
const uygunTerimler = (p: DiPaket[], sinir: number) => p.flatMap((k) => (k.terimler || [])
  .filter((t) => t.t && t.a && t.t.length <= 40)
  .map((t) => ({ id: `${k.key}:${t.t}`, ders: k.key, terim: t.t, tanim: tanim(t, sinir) }))
  .filter((x) => x.tanim.length >= 25 && !x.tanim.startsWith('…')));

/** Oyunun oynanabileceği yeterli veri var mı (ayar ekranında boş kip gösterilmez) */
export function oyunVeriVar(oyun: DersOyun, p: DiPaket[]): boolean {
  if (oyun === 'sirala') return siraTurlari(p).length >= 1;
  return uygunTerimler(p, 120).length >= (oyun === 'izgara' ? 6 : 8);
}


export default function OyunDersV15({ oyun, paketler, baslik, onCik }: { oyun: DersOyun; paketler: DiPaket[]; baslik: string; onCik: () => void }) {
  const [tur, setTur] = useState(0); // yeniden başlatma anahtarı
  const anahtar = `${oyun}:${paketler.length === 1 ? paketler[0].key : '*'}`;
  const sure = useGecenSure();
  const [sonuc, setSonuc] = useState<{ puan: number; toplam: number; yanlis: number; sn: number; rekor: boolean; enIyi: number } | null>(null);
  const bitir = (puan: number, toplam: number, yanlis: number) => {
    const eski = rekorOku(anahtar);
    if (puan > eski) rekorYaz(anahtar, puan);
    setSonuc({ puan, toplam, yanlis, sn: sure.sn(), rekor: puan > eski, enIyi: Math.max(puan, eski) });
  };
  const ad = oyun === 'kaydir' ? 'Kaydır: doğru mu?' : oyun === 'sirala' ? 'Sırala' : 'Eşleştirme ızgarası';
  if (sonuc) {
    return (
      <SonKart
        baslik={`${sonuc.puan}/${sonuc.toplam}${oyun === 'sirala' ? ' adım yerinde' : ' doğru'}`}
        alt={`${ad} · ${baslik}`}
        dogru={sonuc.puan} yanlis={sonuc.yanlis} sureSn={sonuc.sn} enIyi={sonuc.enIyi} rekor={sonuc.rekor}
        oran={sonuc.toplam ? sonuc.puan / sonuc.toplam : 0}
        onCik={onCik} onYeniden={() => { setSonuc(null); sure.sifirla(); setTur((t) => t + 1); }}
      />
    );
  }
  const ortak = { paketler, onCik, bitir, rekor: rekorOku(anahtar) };
  return <div lang="tr" className="og15-oyun">{oyun === 'kaydir' ? <Kaydir key={tur} {...ortak} /> : oyun === 'sirala' ? <Sirala key={tur} {...ortak} /> : <Izgara key={tur} {...ortak} />}</div>;
}

interface OyunP { paketler: DiPaket[]; onCik: () => void; bitir: (puan: number, toplam: number, yanlis: number) => void; rekor: number }
const Bos = ({ metin, onCik }: { metin: string; onCik: () => void }) => <section className="v15-card oy15-kart"><p>{metin}</p><button type="button" className="oy15-cik" onClick={onCik}>Geri</button></section>;

/* ───────── N07 Kaydır: önerme kartları ───────── */
const KART = 12;
function Kaydir({ paketler, onCik, bitir, rekor }: OyunP) {
  const kartlar = useMemo(() => {
    const t = uygunTerimler(paketler, 160);
    return karistir(t).slice(0, KART).map((x) => {
      const ayni = t.filter((y) => y.ders === x.ders && y.id !== x.id);
      const yanlis = ayni.length && Math.random() < 0.5 ? ayni[Math.floor(Math.random() * ayni.length)] : null;
      return { id: x.id, terim: x.terim, tanim: yanlis ? yanlis.tanim : x.tanim, dogruMu: !yanlis, asil: x.tanim };
    });
  }, [paketler]);
  const [i, setI] = useState(0);
  const [dogru, setDogru] = useState(0);
  const [seri, setSeri] = useState(0);
  const [cevap, setCevap] = useState<boolean | null>(null);
  const [dx, setDx] = useState(0);
  const bas = useRef<number | null>(null);
  const k = kartlar[i];
  const cevapla = (c: boolean) => {
    if (!k || cevap !== null) return;
    setCevap(c); setDx(c ? 400 : -400);
    const ok = c === k.dogruMu;
    const yeni = dogru + (ok ? 1 : 0);
    if (ok) { setDogru(yeni); setSeri((s) => s + 1); } else setSeri(0);
    window.setTimeout(() => {
      if (i + 1 >= kartlar.length) { bitir(yeni, kartlar.length, i + 1 - yeni); return; }
      setI(i + 1); setCevap(null); setDx(0);
    }, ok ? 550 : 1900);
  };
  useEffect(() => {
    const t = (e: KeyboardEvent) => { if (e.key === 'ArrowRight') cevapla(true); else if (e.key === 'ArrowLeft') cevapla(false); };
    window.addEventListener('keydown', t);
    return () => window.removeEventListener('keydown', t);
  });
  if (!k) return <Bos metin="Bu derste yeterli terim yok." onCik={onCik} />;
  const ok = cevap !== null && cevap === k.dogruMu;
  // yanlışta kart geri gelir ve titrer, açıklama okunur; doğruda uçup gider
  const kx = cevap !== null && !ok ? 0 : dx;
  return (
    <section className="oy15-soru">
      <OyunUst ilerleme={(i + (cevap !== null ? 1 : 0)) / kartlar.length} sol={`Kart ${i + 1}/${kartlar.length}`} puan={dogru} puanEtiket="doğru" seri={seri}
        ek={<span className="og15-cip is-sonuk">En iyi {rekor}</span>} onCik={onCik} />
      <p className="v15-cap oy15-kd-ip">Tanım bu terime mi ait? Sağa kaydır: doğru · sola: yanlış</p>
      <div className="oy15-kd-alan">
        <div className="oy15-kd-yigin" aria-hidden />
        <div
          key={k.id}
          className={`oy15-kd-kart og15-gir${cevap === null ? '' : ok ? ' is-dogru og15-parla' : ' is-yanlis og15-titre'}`}
          style={{ transform: `translateX(${kx}px) rotate(${kx / 25}deg)`, transition: bas.current === null ? 'transform .3s ease' : 'none' }}
          onPointerDown={(e) => { if (cevap !== null) return; bas.current = e.clientX; (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId); }}
          onPointerMove={(e) => { if (bas.current !== null) setDx(e.clientX - bas.current); }}
          onPointerUp={() => { const d = dx; bas.current = null; if (Math.abs(d) > 80) cevapla(d > 0); else setDx(0); }}
          onPointerCancel={() => { bas.current = null; setDx(0); }}
        >
          <b className="oy15-kd-terim">{k.terim}</b>
          <p>{k.tanim}</p>
          {cevap !== null && !ok && <small>{k.dogruMu ? 'Bu tanım bu terime aitti.' : `Doğru tanım: ${k.asil}`}</small>}
          {cevap === null && Math.abs(dx) > 30 && <span className={`oy15-kd-etiket ${dx > 0 ? 'is-d' : 'is-y'}`}>{dx > 0 ? 'Doğru' : 'Yanlış'}</span>}
        </div>
      </div>
      <div className="oy15-dy-d">
        <button type="button" className="is-y" disabled={cevap !== null} onClick={() => cevapla(false)}><X aria-hidden /> Yanlış</button>
        <button type="button" className="is-d" disabled={cevap !== null} onClick={() => cevapla(true)}><Check aria-hidden /> Doğru</button>
      </div>
    </section>
  );
}

/* ───────── F05 Sırala ───────── */
interface SiraTur { id: string; baslik: string; adimlar: string[] }
function siraTurlari(paketler: DiPaket[]): SiraTur[] {
  const l: SiraTur[] = [];
  for (const p of paketler) {
    for (const x of p.listeler || []) {
      if ((x.sira === 'numara' || x.sira === 'azalan') && x.m.length >= 3 && x.m.length <= 7) {
        const adimlar = x.m.map((m) => String(m.m || '').trim()).filter(Boolean);
        if (adimlar.length === x.m.length && new Set(adimlar).size === adimlar.length) l.push({ id: `${p.key}:l:${x.t}`, baslik: x.t, adimlar });
      }
    }
    for (const t of p.tablolar || []) {
      if (!/^sıra/i.test(t.h?.[0] || '') || t.r.length < 3 || t.r.length > 7) continue;
      const satir = [...t.r].filter((r) => r[0] && !Number.isNaN(Number(r[0]))).sort((a, b) => Number(a[0]) - Number(b[0]));
      if (satir.length !== t.r.length) continue;
      const adimlar = satir.map((r) => r.slice(1).filter(Boolean).join(' — '));
      if (new Set(adimlar).size === adimlar.length) l.push({ id: `${p.key}:t:${t.t}`, baslik: t.t, adimlar });
    }
  }
  return l;
}
const TUR_N = 5;
function Sirala({ paketler, onCik, bitir, rekor }: OyunP) {
  const turlar = useMemo(() => karistir(siraTurlari(paketler)).slice(0, TUR_N), [paketler]);
  const [i, setI] = useState(0);
  const [toplam, setToplam] = useState(0);
  const [yerinde, setYerinde] = useState(0);
  const [seri, setSeri] = useState(0);
  const [kontrol, setKontrol] = useState(false);
  const [oynayan, setOynayan] = useState<number | null>(null);
  const t = turlar[i];
  const ilkDizi = (x: SiraTur) => {
    let d = karistir(x.adimlar.map((_, j) => j));
    for (let n = 0; n < 5 && d.every((v, j) => v === j); n++) d = karistir(d);
    return d;
  };
  const [dizi, setDizi] = useState<number[]>(() => (turlar[0] ? ilkDizi(turlar[0]) : []));
  if (!t) return <Bos metin="Bu derste sıralanacak adım listesi yok." onCik={onCik} />;
  const tasi = (j: number, y: number) => {
    const k = j + y;
    if (kontrol || k < 0 || k >= dizi.length) return;
    const d = [...dizi]; [d[j], d[k]] = [d[k], d[j]]; setDizi(d); setOynayan(d[k]);
  };
  const dogruSayi = dizi.filter((v, j) => v === j).length;
  const kontrolEt = () => {
    setKontrol(true); setYerinde((y) => y + dogruSayi); setToplam((x) => x + dizi.length);
    setSeri((s) => (dogruSayi === dizi.length ? s + 1 : 0));
  };
  const sonraki = () => {
    if (i + 1 >= turlar.length) { bitir(yerinde, toplam, toplam - yerinde); return; }
    setI(i + 1); setDizi(ilkDizi(turlar[i + 1])); setKontrol(false); setOynayan(null);
  };
  return (
    <section className="oy15-soru">
      <OyunUst ilerleme={(i + (kontrol ? 1 : 0)) / turlar.length} sol={`Tur ${i + 1}/${turlar.length}`} puan={yerinde} puanEtiket="yerinde" seri={seri}
        ek={<span className="og15-cip is-sonuk">En iyi {rekor}</span>} onCik={onCik} />
      <p className="oy15-kok">{t.baslik}</p>
      <p className="v15-cap">Adımları oklarla doğru sıraya diz.</p>
      <ol className="oy15-sr">
        {dizi.map((v, j) => (
          <li key={v} className={`${kontrol ? (v === j ? 'is-dogru og15-parla' : 'is-yanlis og15-titre') : ''}${!kontrol && oynayan === v ? ' og15-zipla' : ''}`} style={{ '--i': j } as React.CSSProperties}>
            <span className="oy15-sr-no" aria-hidden>{j + 1}</span>
            <span className="oy15-sr-t">{t.adimlar[v]}{kontrol && v !== j && <small>Doğru yeri: {v + 1}.</small>}</span>
            {!kontrol && (
              <span className="oy15-sr-d">
                <button type="button" onClick={() => tasi(j, -1)} disabled={j === 0} aria-label={`${j + 1}. adımı yukarı taşı`}><ArrowUp aria-hidden /></button>
                <button type="button" onClick={() => tasi(j, 1)} disabled={j === dizi.length - 1} aria-label={`${j + 1}. adımı aşağı taşı`}><ArrowDown aria-hidden /></button>
              </span>
            )}
          </li>
        ))}
      </ol>
      {kontrol ? (
        <div className={`v15-card oy15-aciklama og15-gir${dogruSayi === dizi.length ? ' is-tam' : ''}`}>
          <b>{dogruSayi === dizi.length ? 'Tam sıra! Hepsi yerinde.' : `${dogruSayi}/${dizi.length} adım yerinde.`}</b>
          <button type="button" className="v15-btn oy15-ana" onClick={sonraki}>{i + 1 >= turlar.length ? 'Sonucu gör' : 'Sonraki tur'}</button>
        </div>
      ) : <button type="button" className="v15-btn oy15-ana" onClick={kontrolEt}>Kontrol et</button>}
    </section>
  );
}

/* ───────── F07 Eşleştirme ızgarası: solda terim çipleri, sağda (dar ekranda altta) tanım kartları ───────── */
const IZ_TUR = 3;
const IZ_CIFT = 6;
function Izgara({ paketler, onCik, bitir, rekor }: OyunP) {
  const havuz = useMemo(() => karistir(uygunTerimler(paketler, 140)).slice(0, IZ_TUR * IZ_CIFT), [paketler]);
  const turSayi = Math.max(1, Math.floor(havuz.length / IZ_CIFT));
  const [tur, setTur] = useState(0);
  const [secili, setSecili] = useState<string | null>(null);
  const [tamam, setTamam] = useState<Set<string>>(new Set());
  const [yeni, setYeni] = useState<string | null>(null);
  const [hatali, setHatali] = useState<string[]>([]);
  const [yanlis, setYanlis] = useState(0);
  const [puan, setPuan] = useState(0);
  const [seri, setSeri] = useState(0);
  const ciftler = useMemo(() => havuz.slice(tur * IZ_CIFT, tur * IZ_CIFT + IZ_CIFT), [havuz, tur]);
  const terimler = useMemo(() => karistir(ciftler), [ciftler]);
  const tanimlar = useMemo(() => karistir(ciftler), [ciftler]);
  if (havuz.length < IZ_CIFT) return <Bos metin="Bu derste yeterli terim yok." onCik={onCik} />;
  const sec = (k: string, id: string) => {
    if (tamam.has(id) || hatali.length) return;
    if (!secili) { setSecili(k); return; }
    if (secili === k) { setSecili(null); return; }
    const [st, sid] = [secili.slice(0, 1), secili.slice(2)];
    if (st === k.slice(0, 1)) { setSecili(k); return; } // aynı türden ikinci seçim: seçimi değiştir
    if (sid === id) {
      const n = new Set(tamam).add(id);
      setTamam(n); setSecili(null); setYeni(id);
      const s = seri + 1; setSeri(s); setPuan((p) => p + 10 * Math.min(3, Math.ceil(s / 3)));
      if (ciftler.every((c) => n.has(c.id))) {
        const dogruToplam = (tur + 1) * IZ_CIFT;
        if (tur + 1 >= turSayi) window.setTimeout(() => bitir(Math.max(0, dogruToplam - yanlis), dogruToplam, yanlis), 650);
        else window.setTimeout(() => { setTur((x) => x + 1); setTamam(new Set()); setYeni(null); }, 750);
      }
    } else {
      setYanlis((y) => y + 1); setSeri(0); setHatali([secili, k]);
      window.setTimeout(() => { setHatali([]); setSecili(null); }, 600);
    }
  };
  const kutu = (k: string, id: string, metin: string, terim: boolean) => {
    const cls = tamam.has(id) ? ` is-tamam${yeni === id ? ' og15-onay' : ''}` : hatali.includes(k) ? ' is-hata og15-titre' : secili === k ? ' is-secili' : '';
    return (
      <li key={k}>
        <button type="button" className={`oy15-iz-k${terim ? ' is-terim' : ''}${cls}`} disabled={tamam.has(id)} aria-pressed={secili === k} onClick={() => sec(k, id)}>
          {tamam.has(id) && <Check aria-hidden className="oy15-iz-ok" />}<span>{metin}</span>
        </button>
      </li>
    );
  };
  const carpan = Math.min(3, Math.ceil(Math.max(1, seri) / 3));
  return (
    <section className="oy15-soru">
      <OyunUst ilerleme={(tur * IZ_CIFT + tamam.size) / (turSayi * IZ_CIFT)} sol={`Tur ${tur + 1}/${turSayi}`} puan={puan} seri={seri} carpan={seri >= 3 ? carpan : undefined}
        ek={<span className="og15-cip is-sonuk">{yanlis} yanlış · en iyi {rekor}</span>} onCik={onCik} />
      <p className="v15-cap">Bir terim seç, sonra onun tanımına dokun. Art arda doğrular çarpanı büyütür.</p>
      <div className="oy15-iz">
        <div className="oy15-iz-b">
          <h3 className="oy15-iz-h">Terimler</h3>
          <ul className="oy15-iz-terimler">{terimler.map((c) => kutu(`t|${c.id}`, c.id, c.terim, true))}</ul>
        </div>
        <div className="oy15-iz-b">
          <h3 className="oy15-iz-h">Tanımlar</h3>
          <ul className="oy15-iz-tanimlar">{tanimlar.map((c) => kutu(`d|${c.id}`, c.id, c.tanim, false))}</ul>
        </div>
      </div>
    </section>
  );
}
