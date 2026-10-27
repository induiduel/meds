import React, { useEffect, useRef, useState } from 'react';
import { Check, Lightbulb, RotateCcw, Trophy, X } from 'lucide-react';
import type { GlossaryEntry } from '../../data/glossary';
import { ESLESTIR_KATEGORI } from './OyunEslestirV15';

/**
 * v15 · Terimi bul (Oyunlar, tek kişilik boşluk doldurma): sözlük tanımı gösterilir, terimi yazarsın.
 * Karşılaştırma Türkçe harf ve büyük/küçük farkı gözetmez; sözlükteki eşanlamlılar (aliases) ve parantez içi
 * kısaltma da doğru sayılır. İpucu her basışta bir harf daha açar (puan düşer). 10 soru; en iyi puan cihazda.
 */
const N = 10;
const REKOR_KEY = 'medsoru_oyun_rekor_v1';
const fold = (s: string) => s.toLocaleLowerCase('tr-TR').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ı/g, 'i').replace(/[^a-z0-9]+/g, ' ').trim();
const kacir = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
interface Soru { terim: string; kabul: string[]; tanim: string }

function soruYap(e: GlossaryEntry): Soru | null {
  const terim = String(e.term || '').trim();
  const ad = terim.replace(/\s*\(.*?\)\s*/g, ' ').trim();
  let t = String(e.definition || '').split(/(?<=[.!?])\s+/)[0] || '';
  for (const p of [ad, ...(e.aliases || []), ad.split(/\s+/)[0]].filter((x) => x && x.length > 3)) t = t.replace(new RegExp(`(?<!\\p{L})${kacir(String(p))}`, 'giu'), '…');
  if (t.length < 30 || ad.length > 32 || t.startsWith('…')) return null;
  const kisaltma = terim.match(/\(([^)]+)\)/)?.[1];
  return { terim: ad, kabul: [ad, terim, ...(e.aliases || []), ...(kisaltma ? [kisaltma] : [])].map(fold).filter(Boolean), tanim: t.length > 220 ? `${t.slice(0, 217)}…` : t };
}

export default function OyunBoslukV15({ kategori, onCik }: { kategori: string; onCik: () => void }) {
  const [sorular, setSorular] = useState<Soru[] | null>(null);
  const [i, setI] = useState(0);
  const [cevap, setCevap] = useState('');
  const [ipucu, setIpucu] = useState(0);
  const [sonuc, setSonuc] = useState<null | boolean>(null);
  const [puan, setPuan] = useState(0);
  const [dogru, setDogru] = useState(0);
  const anahtar = `bosluk:${kategori || '*'}`;
  const [rekor, setRekor] = useState<number>(() => { try { return JSON.parse(localStorage.getItem(REKOR_KEY) || '{}')[anahtar] || 0; } catch { return 0; } });
  const [yeniRekor, setYeniRekor] = useState(false);
  const girdi = useRef<HTMLInputElement>(null);
  const katAd = ESLESTIR_KATEGORI.find(([k]) => k === kategori)?.[1] || 'Karışık';

  const kur = () => import('../../data/glossary').then(({ GLOSSARY }) => {
    const aday = GLOSSARY.filter((e) => !kategori || e.category === kategori).map(soruYap).filter((x): x is Soru => !!x);
    for (let k = aday.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [aday[k], aday[j]] = [aday[j], aday[k]]; }
    setSorular(aday.slice(0, N)); setI(0); setCevap(''); setIpucu(0); setSonuc(null); setPuan(0); setDogru(0); setYeniRekor(false);
  });
  useEffect(() => { void kur(); }, [kategori]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { if (sonuc === null) girdi.current?.focus(); }, [i, sonuc]);

  const s = sorular?.[i];
  const bitti = !!sorular && i >= sorular.length;
  useEffect(() => {
    if (!bitti) return;
    if (puan > rekor) { setRekor(puan); setYeniRekor(true); try { const o = JSON.parse(localStorage.getItem(REKOR_KEY) || '{}'); o[anahtar] = puan; localStorage.setItem(REKOR_KEY, JSON.stringify(o)); } catch { /* yok */ } }
  }, [bitti]); // eslint-disable-line react-hooks/exhaustive-deps

  const kontrol = () => {
    if (!s || sonuc !== null || !cevap.trim()) return;
    const ok = s.kabul.includes(fold(cevap));
    setSonuc(ok);
    if (ok) { setDogru((d) => d + 1); setPuan((p) => p + Math.max(2, 10 - ipucu * 2)); }
  };
  const gec = () => { setSonuc(false); };
  const sonraki = () => { setI((x) => x + 1); setCevap(''); setIpucu(0); setSonuc(null); };
  const maske = s ? s.terim.split('').map((c, k) => (c === ' ' ? ' ' : k < ipucu ? c : '_')).join('') : '';

  if (!sorular) return <span className="v15-skel b15-skel" aria-hidden />;
  if (bitti) {
    return (
      <section className="v15-card oy15-kart oy15-son">
        <Trophy aria-hidden className="oy15-tac" />
        <b className="oy15-kazanan">{puan} puan{yeniRekor ? ' · yeni rekor!' : ''}</b>
        <p className="v15-cap">{katAd} · {dogru}/{sorular.length} doğru · en iyi {rekor}</p>
        <div className="oy15-alt">
          <button type="button" className="oy15-cik" onClick={onCik}>Oyunlar</button>
          <button type="button" className="v15-btn oy15-ana" onClick={() => void kur()}><RotateCcw aria-hidden />Yeniden oyna</button>
        </div>
      </section>
    );
  }
  if (!s) return null;

  return (
    <section className="oy15-soru">
      <div className="oy15-ust">
        <span className="v15-cap">Terimi bul · {katAd} · {i + 1}/{sorular.length}</span>
        <span className="v15-cap">{puan} puan</span>
        <button type="button" className="oy15-x" onClick={onCik} aria-label="Oyundan çık"><X aria-hidden /></button>
      </div>
      <p className="oy15-kok">{s.tanim}</p>
      <p className="bs15-maske" aria-label={`${s.terim.replace(/\s/g, '').length} harf`}>{sonuc === null ? maske : s.terim}</p>
      <form className="bs15-form" onSubmit={(e) => { e.preventDefault(); if (sonuc === null) kontrol(); else sonraki(); }}>
        <input ref={girdi} value={cevap} onChange={(e) => setCevap(e.target.value)} placeholder="Terimi yaz" aria-label="Cevap" disabled={sonuc !== null}
          className={sonuc === true ? 'is-dogru' : sonuc === false ? 'is-yanlis' : ''} autoComplete="off" autoCapitalize="off" spellCheck={false} />
        {sonuc === null ? (
          <>
            <button type="button" className="oy15-cik" onClick={() => setIpucu((x) => Math.min(x + 1, s.terim.length - 1))} title="Bir harf aç (puan düşer)"><Lightbulb aria-hidden />İpucu</button>
            <button type="submit" className="v15-btn" disabled={!cevap.trim()}>Kontrol</button>
          </>
        ) : <button type="submit" className="v15-btn">{i + 1 >= sorular.length ? 'Sonucu gör' : 'Sonraki'}</button>}
      </form>
      {sonuc === null && <button type="button" className="bs15-gec" onClick={gec}>Bilmiyorum, cevabı göster</button>}
      {sonuc !== null && <p className={`bs15-sonuc${sonuc ? ' is-dogru' : ''}`}>{sonuc ? <><Check aria-hidden /> Doğru: +{Math.max(2, 10 - ipucu * 2)} puan</> : <><X aria-hidden /> Doğrusu: <b>{s.terim}</b></>}</p>}
    </section>
  );
}
