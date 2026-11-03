/**
 * Gezinen tilki: ara sıra ekranın alt kenarında (alt sekme çubuğunun üstünde, yan menünün sağında) bir tilki
 * koşarak geçer; yolun ortasında durup koklar, dokunulursa durur ve yukarı kalpler bırakır. Hareket azaltılmışsa çıkmaz.
 * `arzu:tilki` olayı ({ adet }) ile geçit başlatılır (klavyede "arzu" yazınca).
 */
import React, { useEffect, useRef, useState } from 'react';
import { TilkiYuruyen } from './cizimler';
import { kalpSuzul } from './kalpPatlamasi';

const azalt = () => !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
const rnd = (a: number, b: number) => a + Math.random() * (b - a);

type Kosu = { id: number; yon: 1 | -1; hiz: number; boy: number; gecikme: number; koklar: boolean };

function TilkiKosusu({ k, onBitti }: { k: Kosu; onBitti: (id: number) => void }) {
  const ref = useRef<HTMLDivElement>(null);
  const animRef = useRef<Animation | null>(null);
  const [durum, setDurum] = useState<'kosar' | 'koklar' | 'sevildi'>('kosar');
  const [balon, setBalon] = useState<string | null>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const kap = el.parentElement!;
    const w = kap.clientWidth;
    const gen = k.boy;
    const bas = k.yon === 1 ? -gen - 20 : w + 20;
    const son = k.yon === 1 ? w + 20 : -gen - 20;
    const mesafe = Math.abs(son - bas);
    const sure = (mesafe / k.hiz) * 1000;
    const anim = el.animate(
      [{ transform: `translateX(${bas}px)` }, { transform: `translateX(${son}px)` }],
      { duration: sure, delay: k.gecikme, easing: 'linear', fill: 'both' },
    );
    animRef.current = anim;
    const zamanlar: number[] = [];
    if (k.koklar) {
      // yolun %35–65'inde durup koklar
      const t = k.gecikme + sure * rnd(0.35, 0.65);
      zamanlar.push(window.setTimeout(() => {
        if (anim.playState !== 'running') return;
        anim.pause();
        setDurum('koklar');
        zamanlar.push(window.setTimeout(() => { setDurum('kosar'); anim.play(); }, rnd(1200, 2000)));
      }, t));
    }
    anim.onfinish = () => onBitti(k.id);
    return () => { zamanlar.forEach(clearTimeout); anim.cancel(); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const sev = (e: React.PointerEvent) => {
    const anim = animRef.current;
    if (!anim || durum === 'sevildi') return;
    anim.pause();
    setDurum('sevildi');
    const r = (e.currentTarget as HTMLElement).getBoundingClientRect();
    kalpSuzul(r.left + r.width * 0.62, r.top + 8, 6);
    const sozler = ['Seni seviyorum.', 'Biraz mola ver.', 'İyi gidiyorsun.', 'Su içmeyi unutma.', 'Seni özledim.'];
    setBalon(sozler[Math.floor(Math.random() * sozler.length)]);
    window.setTimeout(() => { setBalon(null); setDurum('kosar'); anim.play(); }, 1900);
  };

  return (
    <div ref={ref} className={`ar-tilki-kos is-${durum} ${k.yon === -1 ? 'is-sol' : ''}`} style={{ width: k.boy }} onPointerDown={sev}>
      {balon && <span className="ar-tilki-balon">{balon}</span>}
      <div className="ar-tilki-don"><TilkiYuruyen width={k.boy} /></div>
      <span className="ar-tilki-golge" />
    </div>
  );
}

export default function GezinenTilki({ ilkGecikmeMs = 75_000 }: { ilkGecikmeMs?: number }) {
  const [kosular, setKosular] = useState<Kosu[]>([]);
  const sayac = useRef(0);

  const baslat = (adet = 1) => {
    if (azalt()) return;
    const dar = window.innerWidth < 640;
    const yeni: Kosu[] = [];
    const yon: 1 | -1 = Math.random() < 0.5 ? 1 : -1;
    for (let i = 0; i < adet; i++) {
      yeni.push({
        id: ++sayac.current,
        yon: adet > 1 ? yon : (Math.random() < 0.5 ? 1 : -1),
        hiz: adet > 1 ? 150 : rnd(95, 160),
        boy: dar ? rnd(64, 80) : rnd(84, 118),
        gecikme: i * 420,
        koklar: adet === 1 && Math.random() < 0.7,
      });
    }
    setKosular((k) => [...k, ...yeni]);
  };

  useEffect(() => {
    let t = window.setTimeout(function dongu() {
      if (document.visibilityState === 'visible') baslat(1);
      t = window.setTimeout(dongu, rnd(100_000, 240_000));
    }, ilkGecikmeMs);
    const onGecit = (e: Event) => baslat(Math.max(1, Math.min(8, Number((e as CustomEvent).detail?.adet) || 1)));
    window.addEventListener('arzu:tilki', onGecit);
    return () => { window.clearTimeout(t); window.removeEventListener('arzu:tilki', onGecit); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!kosular.length) return null;
  return (
    <div className="ar-tilki-yol" aria-hidden="true">
      {kosular.map((k) => (
        <TilkiKosusu key={k.id} k={k} onBitti={(id) => setKosular((l) => l.filter((x) => x.id !== id))} />
      ))}
    </div>
  );
}
