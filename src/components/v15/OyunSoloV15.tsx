import React, { useCallback, useEffect, useRef, useState } from 'react';
import { Check, Heart, RotateCcw, Timer, Trophy, X } from 'lucide-react';
import { safeJsonFetch } from '../../services/api';

/**
 * v15 · Tek kişilik oyunlar (Oyunlar sayfası): Blitz (60 sn, olabildiğince çok doğru) ve Hayatta kal (3 can).
 * Sorular GET /api/oyun/sorular (sesli soru çözücü setleri, cevap + doğru şık açıklaması); puan istemcide.
 * Biten soruların yerine arka planda yenisi çekilir; aynı oyunda soru yinelenmez. En iyi skor cihazda tutulur.
 */
export type SoloMod = 'blitz' | 'hayatta';
interface S { id: string; prompt: string; options: Record<string, string>; correct: string; aciklama: string; baslik: string }
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

  const getir = useCallback(async () => {
    if (getiriyor.current) return;
    getiriyor.current = true;
    const r = await safeJsonFetch<{ sorular: S[] }>(`/api/oyun/sorular?brans=${encodeURIComponent(brans)}${ders ? `&ders=${encodeURIComponent(ders)}` : ''}&n=20`);
    getiriyor.current = false;
    if (!r.ok || !r.data) { setHata('Sorular alınamadı.'); return; }
    const yeni = r.data.sorular.filter((x) => !goruldu.current.has(x.id));
    // havuz küçükse (tek ders) görülenleri sıfırla, oyun sürsün
    if (!yeni.length && r.data.sorular.length) { goruldu.current.clear(); setKuyruk((k) => [...k, ...r.data!.sorular]); return; }
    setKuyruk((k) => [...k, ...yeni]);
  }, [brans, ders]);

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
    const skor = dogru;
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
  const sonraki = () => {
    if (mod === 'hayatta' && can <= 0) { setBitti(true); return; }
    setSecim(null); setSoru(null);
  };
  const yeniden = () => {
    goruldu.current.clear(); setKuyruk([]); setSoru(null); setSecim(null); setDogru(0); setYanlis(0); setCan(3); setSeri(0);
    setBitis(0); setKalan(SURE); setBitti(false); setYeniRekor(false); void getir();
  };

  if (hata) return <section className="v15-card oy15-kart"><p className="oy15-hata">{hata}</p><button type="button" className="oy15-cik" onClick={onCik}>Geri</button></section>;

  if (bitti) {
    return (
      <section className="v15-card oy15-kart oy15-son">
        <Trophy aria-hidden className="oy15-tac" />
        <b className="oy15-kazanan">{dogru} doğru{yeniRekor ? ' · yeni rekor!' : ''}</b>
        <p className="v15-cap">{baslik} · {mod === 'blitz' ? '60 saniye' : 'Hayatta kal'} · {yanlis} yanlış · en iyi {rekor}</p>
        <div className="oy15-alt">
          <button type="button" className="oy15-cik" onClick={onCik}>Oyunlar</button>
          <button type="button" className="v15-btn oy15-ana" onClick={yeniden}><RotateCcw aria-hidden />Yeniden oyna</button>
        </div>
      </section>
    );
  }

  return (
    <section className="oy15-soru">
      <div className="oy15-ust">
        {mod === 'blitz'
          ? <span className="oy15-sayac"><Timer aria-hidden /> {Math.ceil(kalan / 1000)} sn</span>
          : <span className="oy15-canlar" aria-label={`${can} can`}>{[0, 1, 2].map((i) => <Heart key={i} aria-hidden className={i < can ? 'is-dolu' : ''} />)}</span>}
        <span className="v15-cap">{dogru} doğru{seri > 2 ? ` · ${seri} seri` : ''} · en iyi {rekor}</span>
        <button type="button" className="oy15-x" onClick={() => setBitti(true)} aria-label="Oyunu bitir"><X aria-hidden /></button>
      </div>
      {mod === 'blitz' && <div className="v15-bar oy15-sure" aria-hidden><span style={{ width: `${(kalan / SURE) * 100}%` }} /></div>}
      {!soru ? <span className="v15-skel b15-skel" aria-hidden /> : (
        <>
          <p className="oy15-kok">{soru.prompt}</p>
          <ul className="oy15-siklar">
            {Object.entries(soru.options).map(([h, t]) => {
              const cls = secim ? (h === soru.correct ? ' is-dogru' : h === secim ? ' is-yanlis' : ' is-sonuk') : '';
              return (
                <li key={h}>
                  <button type="button" className={`oy15-sik${cls}`} disabled={!!secim} onClick={() => cevapla(h)}>
                    <b>{h}</b><span>{t}</span>{secim && h === soru.correct && <Check aria-hidden />}{secim === h && h !== soru.correct && <X aria-hidden />}
                  </button>
                </li>
              );
            })}
          </ul>
          {mod === 'hayatta' && secim && (
            <div className="v15-card oy15-aciklama">
              <b>{secim === soru.correct ? 'Doğru.' : `Doğru cevap ${soru.correct}.`}</b>
              {soru.aciklama && <p>{soru.aciklama}</p>}
              <button type="button" className="v15-btn oy15-ana" onClick={sonraki}>{can <= 0 ? 'Sonucu gör' : 'Sonraki soru'}</button>
            </div>
          )}
        </>
      )}
    </section>
  );
}
