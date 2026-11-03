/**
 * Kalp avı: sayfa değişince ara sıra ekranda küçük, hafif nabız atan bir kalp belirir (rastgele yerde, kenarlardan
 * uzak). Dokununca toplanır; bulunan kalp sayısı cihazda tutulur (medsoru_arzu_kalpler). 5, 10, 25, 50, 100'de özel not.
 * Dokunma hedefi 48 px; fare olmayan cihazlarda da rahat yakalanır.
 */
import React, { useEffect, useRef, useState } from 'react';
import type { AppRoute } from '../../router';
import { Kalp } from './cizimler';
import { kalpPatlat } from './kalpPatlamasi';

const KEY = 'medsoru_arzu_kalpler';
const KILOMETRE: Record<number, string> = {
  1: 'İlk kalbi buldun. Sayfalarda başka kalpler de saklı.',
  5: 'Beş kalp oldu. Dikkatli bakıyorsun.',
  10: 'On kalp. Her biri senin için.',
  25: 'Yirmi beş kalp buldun. Çalışırken bile gözünden bir şey kaçmıyor.',
  50: 'Elli kalp. Bu kadarını bulacağını biliyordum.',
  100: 'Yüz kalp. Hepsi seninle ilgili tek bir şey söylüyor: seni seviyorum.',
};

const oku = (): number => { try { return Number(localStorage.getItem(KEY)) || 0; } catch { return 0; } };
const yaz = (n: number) => { try { localStorage.setItem(KEY, String(n)); } catch { /* depolama kapalı */ } };
const rnd = (a: number, b: number) => a + Math.random() * (b - a);

type Konum = { x: number; y: number; d: number };

export default function KalpAvi({ rota }: { rota: AppRoute }) {
  const [konum, setKonum] = useState<Konum | null>(null);
  const [bulundu, setBulundu] = useState<number | null>(null);
  const ilk = useRef(true);
  const zaman = useRef<number[]>([]);

  const yerlestir = (gecikme: number) => {
    zaman.current.forEach(clearTimeout);
    zaman.current = [window.setTimeout(() => {
      if (document.visibilityState !== 'visible') return;
      const w = window.innerWidth, h = window.innerHeight;
      const dar = w < 768;
      // Üst çubuk, alt sekme çubuğu ve yan menü dışında; kenarlardan 24 px içeride
      const solSinir = dar ? 24 : 260;
      setKonum({ x: rnd(solSinir, w - 60), y: rnd(90, h - (dar ? 150 : 90)), d: rnd(0.9, 1.15) });
      // 70 sn içinde bulunmazsa sessizce kaybolur
      zaman.current.push(window.setTimeout(() => setKonum(null), 70_000));
    }, gecikme)];
  };

  useEffect(() => {
    const t = ilk.current ? 50_000 : rnd(4000, 20_000);
    ilk.current = false;
    if (Math.random() < 0.55 || t === 50_000) yerlestir(t);
    const hemen = () => yerlestir(0);
    window.addEventListener('arzu:av', hemen);
    return () => { zaman.current.forEach(clearTimeout); window.removeEventListener('arzu:av', hemen); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [rota]);

  const topla = (e: React.PointerEvent) => {
    e.stopPropagation();
    const r = (e.currentTarget as HTMLElement).getBoundingClientRect();
    kalpPatlat(r.left + r.width / 2, r.top + r.height / 2, 14, 110);
    const n = oku() + 1;
    yaz(n);
    setKonum(null);
    setBulundu(n);
    window.setTimeout(() => setBulundu(null), 2600);
    const mesaj = KILOMETRE[n];
    if (mesaj) window.setTimeout(() => window.dispatchEvent(new CustomEvent('arzu:fisilti', { detail: { metin: mesaj } })), 900);
  };

  return (
    <>
      {konum && (
        <button
          type="button"
          className="ar-av"
          style={{ left: konum.x, top: konum.y, '--d': konum.d } as React.CSSProperties}
          onPointerDown={topla}
          aria-label="Saklı kalp"
        >
          <Kalp size={22} />
        </button>
      )}
      {bulundu !== null && (
        <span className="ar-av-sayac" role="status">
          <Kalp size={14} color="#fff" parlak={false} /> {bulundu}. kalp
        </span>
      )}
    </>
  );
}
