import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Check, Heart, Timer, X } from 'lucide-react';
import { OyunUst, SonKart, useGecenSure } from './OyunKitV15';
import { safeJsonFetch } from '../../services/api';

/**
 * v15 · Tek kişilik oyunlar (Oyunlar sayfası): Blitz (60 sn, olabildiğince çok doğru) ve Hayatta kal (3 can).
 * Sorular GET /api/oyun/sorular (sesli soru çözücü setleri, cevap + doğru şık açıklaması); puan istemcide.
 * Biten soruların yerine arka planda yenisi çekilir; aynı oyunda soru yinelenmez. En iyi skor cihazda tutulur.
 */
/** gorsel: görselli soru kipi (yalnız `gorsel` alanı olan sorular, 10 soru, açıklamalı) */
export type SoloMod = 'blitz' | 'hayatta' | 'gorsel';
const GORSEL_N = 10;
interface S { id: string; prompt: string; options: Record<string, string>; correct: string; aciklama: string; baslik: string; gorsel?: string }
const REKOR_KEY = 'medsoru_oyun_rekor_v1';
const SURE = 60_000;
const rekorOku = (k: string): number => { try { return JSON.parse(localStorage.getItem(REKOR_KEY) || '{}')[k] || 0; } catch { return 0; } };
const rekorYaz = (k: string, v: number) => { try { const o = JSON.parse(localStorage.getItem(REKOR_KEY) || '{}'); o[k] = v; localStorage.setItem(REKOR_KEY, JSON.stringify(o)); } catch { /* yok */ } };

export default function OyunSoloV15({ mod, brans, ders, baslik, onCik }: { mod: SoloMod; brans: string; ders?: string; baslik: string; onCik: () => void }) {
  const [kuyruk, setKuyruk] = useState<S[]>([]);
  const goruldu = useRef(new Set<string>());
  const [soru, setSoru] = useState<S | null>(null);
  const [secim, setSecim] = useState<string | null>(null);
  const [dogru, setDogru] = useState(0);
  const [yanlis, setYanlis] = useState(0);
  const [can, setCan] = useState(3);
  const [seri, setSeri] = useState(0);
  const [bitis, setBitis] = useState(0);
  const [kalan, setKalan] = useState(SURE);
  const [bitti, setBitti] = useState(false);
  const [hata, setHata] = useState('');
  const rekorAnahtar = `${mod}:${brans}:${ders || '*'}`;
  const [rekor, setRekor] = useState(() => rekorOku(rekorAnahtar));
  const [yeniRekor, setYeniRekor] = useState(false);
  const getiriyor = useRef(false);
  // Blitz (tasarım F06): kök + tek bir şık önerme olarak gelir; "Doğru mu?" Doğru/Yanlış ile cevaplanır. Önerme yarı
  // olasılıkla doğru şık, değilse rastgele yanlış şık. Seri çarpanı: her 3 doğru seri puanı 1 artırır (×1, ×2, ×3…).
  const [puan, setPuan] = useState(0);
  const oneri = useMemo(() => {
    if (!soru || mod !== 'blitz') return null;
    const yanlislar = Object.keys(soru.options).filter((h) => h !== soru.correct);
    const h = Math.random() < 0.5 || !yanlislar.length ? soru.correct : yanlislar[Math.floor(Math.random() * yanlislar.length)];
    return { h, metin: soru.options[h], dogruMu: h === soru.correct };
  }, [soru, mod]);
  const [dySec, setDySec] = useState<boolean | null>(null);
  const carpan = 1 + Math.floor(seri / 3);
  const sure = useGecenSure();

  const getir = useCallback(async () => {
    if (getiriyor.current) return;
    getiriyor.current = true;
    const r = await safeJsonFetch<{ sorular: S[] }>(`/api/oyun/sorular?brans=${encodeURIComponent(brans)}${ders ? `&ders=${encodeURIComponent(ders)}` : ''}&n=20${mod === 'gorsel' ? '&gorsel=1' : ''}`);
    getiriyor.current = false;
    if (!r.ok || !r.data) { setHata('Sorular alınamadı.'); return; }
    const yeni = r.data.sorular.filter((x) => !goruldu.current.has(x.id));
    // havuz küçükse (tek ders) görülenleri sıfırla, oyun sürsün
    if (!yeni.length && r.data.sorular.length) { goruldu.current.clear(); setKuyruk((k) => [...k, ...r.data!.sorular]); return; }
    setKuyruk((k) => [...k, ...yeni]);
  }, [brans, ders, mod]);

  useEffect(() => { void getir(); }, [getir]);
  // ilk soru ve kuyruk azalınca yenisi
  useEffect(() => {
    if (!soru && kuyruk.length && !bitti) {
      const [ilk, ...geri] = kuyruk;
      goruldu.current.add(ilk.id);
      setSoru(ilk); setKuyruk(geri);
      if (mod === 'blitz' && !bitis) setBitis(Date.now() + SURE);
    }
    if (kuyruk.length < 4 && !bitti) void getir();
  }, [kuyruk, soru, bitti, getir, mod, bitis]);
  // Blitz saati
  useEffect(() => {
    if (mod !== 'blitz' || !bitis || bitti) return;
    const t = setInterval(() => { const k = Math.max(0, bitis - Date.now()); setKalan(k); if (!k) setBitti(true); }, 100);
    return () => clearInterval(t);
  }, [mod, bitis, bitti]);
  useEffect(() => {
    if (!bitti) return;
    const skor = mod === 'blitz' ? puan : dogru;
    if (skor > rekor) { rekorYaz(rekorAnahtar, skor); setRekor(skor); setYeniRekor(true); }
  }, [bitti]); // eslint-disable-line react-hooks/exhaustive-deps

  const cevapla = (h: string) => {
    if (!soru || secim || bitti) return;
    setSecim(h);
    const ok = h === soru.correct;
    if (ok) { setDogru((x) => x + 1); setSeri((x) => x + 1); } else { setYanlis((x) => x + 1); setSeri(0); if (mod === 'hayatta') setCan((c) => c - 1); }
    // Blitz akar (doğruda 0,5 sn, yanlışta 1,5 sn doğruyu gösterir); Hayatta kal açıklamayı okutur, "Sonraki"yle geçilir
    if (mod === 'blitz') setTimeout(sonraki, ok ? 500 : 1500);
  };
  const dyCevapla = (cevap: boolean) => {
    if (!oneri || dySec !== null || bitti) return;
    setDySec(cevap);
    const ok = cevap === oneri.dogruMu;
    if (ok) { setDogru((x) => x + 1); setPuan((p) => p + carpan); setSeri((x) => x + 1); } else { setYanlis((x) => x + 1); setSeri(0); }
    setTimeout(() => { setDySec(null); setSecim(null); setSoru(null); }, ok ? 450 : 1400);
  };
  const sonraki = () => {
    if (mod === 'hayatta' && can <= 0) { setBitti(true); return; }
    if (mod === 'gorsel' && dogru + yanlis >= GORSEL_N) { setBitti(true); return; }
    setSecim(null); setSoru(null);
  };
  const yeniden = () => {
    goruldu.current.clear(); setKuyruk([]); setSoru(null); setSecim(null); setDySec(null); setPuan(0); setDogru(0); setYanlis(0); setCan(3); setSeri(0);
    setBitis(0); setKalan(SURE); setBitti(false); setYeniRekor(false); void getir();
  };

  if (hata) return <section className="v15-card oy15-kart"><p className="oy15-hata">{hata}</p><button type="button" className="oy15-cik" onClick={onCik}>Geri</button></section>;

  if (bitti) {
    const skor = mod === 'blitz' ? puan : dogru;
    return (
      <SonKart
        baslik={mod === 'blitz' ? `${puan} puan` : `${dogru} doğru`}
        alt={`${baslik} · ${mod === 'blitz' ? '60 saniye' : mod === 'gorsel' ? 'Görselli soru' : 'Hayatta kal'}`}
        dogru={dogru} yanlis={yanlis} sureSn={sure.sn()} enIyi={Math.max(rekor, skor)} rekor={yeniRekor}
        oran={dogru + yanlis ? dogru / (dogru + yanlis) : 0} onCik={onCik} onYeniden={() => { sure.sifirla(); yeniden(); }}
      />
    );
  }

  return (
    <section className="oy15-soru" lang="tr">
      <OyunUst
        ilerleme={mod === 'blitz' ? kalan / SURE : mod === 'gorsel' ? (dogru + yanlis) / GORSEL_N : can / 3}
        sol={mod === 'blitz'
          ? <span className={`oy15-sayac${kalan < 10_000 ? ' is-az' : ''}`}><Timer aria-hidden /> {Math.ceil(kalan / 1000)} sn</span>
          : mod === 'gorsel' ? `Soru ${Math.min(GORSEL_N, dogru + yanlis + (secim ? 0 : 1))}/${GORSEL_N}`
          : <span className="oy15-canlar" aria-label={`${can} can`}>{[0, 1, 2].map((i) => <Heart key={i} aria-hidden className={i < can ? 'is-dolu' : ''} />)}</span>}
        puan={mod === 'blitz' ? puan : dogru} puanEtiket={mod === 'blitz' ? 'puan' : 'doğru'} seri={seri} carpan={mod === 'blitz' ? carpan : undefined}
        ek={<span className="og15-cip is-sonuk">En iyi {rekor}</span>} onCik={() => setBitti(true)} cikEtiket="Oyunu bitir" />
      {!soru ? <span className="v15-skel b15-skel" aria-hidden /> : (
        <>
          {mod === 'gorsel' && soru.gorsel && (
            <a className="oy15-gorsel" href={soru.gorsel} target="_blank" rel="noopener noreferrer" aria-label="Görseli büyük aç">
              <img src={soru.gorsel} alt="Soru görseli" loading="eager" />
            </a>
          )}
          <p className="oy15-kok">{soru.prompt}</p>
          {mod === 'blitz' && oneri ? (
            <div className="oy15-dy">
              <div key={oneri.metin} className={`oy15-oneri og15-gir${dySec === null ? '' : dySec === oneri.dogruMu ? ' is-dogru og15-parla' : ' is-yanlis og15-titre'}`}>
                <small>Önerme</small><b>{oneri.metin}</b>
                {dySec !== null && dySec !== oneri.dogruMu && <span>{oneri.dogruMu ? 'Bu şık doğruydu.' : `Doğru cevap: ${soru.options[soru.correct]}`}</span>}
              </div>
              <div className="oy15-dy-d">
                <button type="button" className="is-y" disabled={dySec !== null} onClick={() => dyCevapla(false)}><X aria-hidden /> Yanlış</button>
                <button type="button" className="is-d" disabled={dySec !== null} onClick={() => dyCevapla(true)}><Check aria-hidden /> Doğru</button>
              </div>
            </div>
          ) : (
          <ul className="oy15-siklar">
            {Object.entries(soru.options).map(([h, t]) => {
              const cls = secim ? (h === soru.correct ? ` is-dogru${h === secim ? ' og15-parla' : ''}` : h === secim ? ' is-yanlis og15-titre' : ' is-sonuk') : '';
              return (
                <li key={h}>
                  <button type="button" className={`oy15-sik${cls}`} disabled={!!secim} onClick={() => cevapla(h)}>
                    <b>{h}</b><span>{t}</span>{secim && h === soru.correct && <Check aria-hidden />}{secim === h && h !== soru.correct && <X aria-hidden />}
                  </button>
                </li>
              );
            })}
          </ul>
          )}
          {(mod === 'hayatta' || mod === 'gorsel') && secim && (
            <div className="v15-card oy15-aciklama">
              <b>{secim === soru.correct ? 'Doğru.' : `Doğru cevap ${soru.correct}.`}</b>
              {soru.aciklama && <p>{soru.aciklama}</p>}
              <button type="button" className="v15-btn oy15-ana" onClick={sonraki}>{(mod === 'hayatta' && can <= 0) || (mod === 'gorsel' && dogru + yanlis >= GORSEL_N) ? 'Sonucu gör' : 'Sonraki soru'}</button>
            </div>
          )}
        </>
      )}
    </section>
  );
}
