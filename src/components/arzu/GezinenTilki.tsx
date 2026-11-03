/**
 * Gezinenler: ekranın alt kenarında (alt sekme çubuğunun üstünde, yan menünün sağında) ara sıra bir yaratık geçer.
 * TEK YARATIK KURALI: aynı anda yalnız bir yaratık görünür; istekler sıraya girer (geçit = ardı ardına tek tek).
 * Yoldaş tilki ekrandayken (`arzu:yoldas-durum`) sıra bekler.
 *
 * Türler ve kipler:
 * - tilki / geçiş: koşar, yolun ortasında durup koklar; dokununca durur, kalp bırakır, bir söz söyler.
 *   Dokunulmuşken ikinci dokunuş → tilki yanında kalır (`arzu:yoldas`), koşu biter.
 * - tilki / selam: kenardan hızla girer, durup el sallar ("Selam!"), sonra kaçar.
 * - tavşan / geçiş: zıplayarak geçer, ara sıra durup burnunu oynatır; dokununca kalp + söz.
 * Olaylar: `arzu:tilki` {adet} (sırayla), `arzu:tavsan` {adet}. Hareket azaltılmışsa yaratık çıkmaz.
 */
import React, { useEffect, useRef, useState } from 'react';
import { TavsanZiplayan, TilkiYuruyen } from './cizimler';
import { kalpSuzul } from './kalpPatlamasi';

const azalt = () => !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
const rnd = (a: number, b: number) => a + Math.random() * (b - a);

type Tur = 'tilki' | 'tavsan';
type Kip = 'gecis' | 'selam';
type Kosu = { id: number; tur: Tur; kip: Kip; yon: 1 | -1; hiz: number; boy: number; durur: boolean };

/** Koşarken yere bırakılan pati izi: 1.4 sn'de solar */
function patiBirak(kap: HTMLElement, x: number, taban: number, sol: boolean, yon: 1 | -1) {
  const p = document.createElement('span');
  p.className = 'ar-pati';
  p.style.left = `${x}px`;
  p.style.bottom = `${taban + (sol ? 10 : 2)}px`;
  p.style.transform = `scaleX(${yon}) rotate(${yon * (sol ? -8 : 8)}deg)`;
  kap.appendChild(p);
  p.animate([{ opacity: .55 }, { opacity: .4, offset: .5 }, { opacity: 0 }], { duration: 1400, easing: 'ease-out', fill: 'forwards' }).onfinish = () => p.remove();
}

const TILKI_SOZ = ['Seni seviyorum.', 'Biraz mola ver.', 'İyi gidiyorsun.', 'Su içmeyi unutma.', 'Seni özledim.'];
const TAVSAN_SOZ = ['Selam.', 'Havuç yok mu?', 'Sen de biraz zıpla.', 'Merhaba Arzu.'];

function Yaratik({ k, onBitti }: { k: Kosu; onBitti: (id: number) => void }) {
  const ref = useRef<HTMLDivElement>(null);
  const animRef = useRef<Animation | null>(null);
  const [durum, setDurum] = useState<'kosar' | 'durur' | 'sevildi' | 'selam'>('kosar');
  const [yon, setYon] = useState<1 | -1>(k.yon);
  const yonRef = useRef<1 | -1>(k.yon);
  const [balon, setBalon] = useState<string | null>(null);
  const bitti = useRef(false);
  const bitir = () => { if (!bitti.current) { bitti.current = true; onBitti(k.id); } };

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const kap = el.parentElement!;
    const w = kap.clientWidth;
    const gen = k.boy;
    const zamanlar: number[] = [];
    const disari = (y: 1 | -1) => (y === 1 ? w + 20 : -gen - 20);
    const kos = (bas: number, son: number, hiz: number, sonra: () => void) => {
      const a = el.animate([{ transform: `translateX(${bas}px)` }, { transform: `translateX(${son}px)` }], { duration: (Math.abs(son - bas) / hiz) * 1000, easing: 'linear', fill: 'both' });
      animRef.current = a;
      a.onfinish = sonra;
      return a;
    };

    if (k.kip === 'selam') {
      // kenardan girer, %14'te durur, el sallar, ters yöne hızla kaçar
      const bas = disari(k.yon === 1 ? -1 : 1);
      const dur = k.yon === 1 ? w * 0.14 : w * 0.86 - gen;
      kos(bas, dur, k.hiz * 1.6, () => {
        setDurum('selam');
        setBalon('Selam!');
        zamanlar.push(window.setTimeout(() => {
          setBalon(null);
          const geri: 1 | -1 = k.yon === 1 ? -1 : 1;
          yonRef.current = geri;
          setYon(geri);
          setDurum('kosar');
          kos(dur, disari(geri), k.hiz * 2.1, bitir);
        }, 1700));
      });
    } else {
      const bas = disari(k.yon === 1 ? -1 : 1);
      const anim = kos(bas, disari(k.yon), k.hiz, bitir);
      if (k.durur) {
        const t = anim.effect!.getComputedTiming().duration as number;
        zamanlar.push(window.setTimeout(() => {
          if (anim.playState !== 'running') return;
          anim.pause();
          setDurum('durur');
          zamanlar.push(window.setTimeout(() => { setDurum('kosar'); anim.play(); }, rnd(1200, 2000)));
        }, t * rnd(0.35, 0.65)));
      }
    }

    // tilki patileri (yalnız koşarken)
    let sol = false;
    const pati = k.tur === 'tilki' ? window.setInterval(() => {
      const a = animRef.current;
      if (!a || a.playState !== 'running') return;
      const r = el.getBoundingClientRect(), kr = kap.getBoundingClientRect();
      const y = yonRef.current;
      const x = r.left - kr.left + r.width * (y === 1 ? 0.42 : 0.58) + (Math.random() - 0.5) * 6;
      sol = !sol;
      patiBirak(kap, x, 2, sol, y);
    }, 230) : 0;

    return () => { zamanlar.forEach(clearTimeout); if (pati) window.clearInterval(pati); animRef.current?.cancel(); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const sev = (e: React.PointerEvent) => {
    const anim = animRef.current;
    if (!anim || durum === 'selam') return;
    if (durum === 'sevildi') {
      if (k.tur === 'tilki') {
        // ikinci okşama: tilki yanında kalır (Yoldas), koşu biter
        window.dispatchEvent(new CustomEvent('arzu:yoldas'));
        anim.cancel();
        bitir();
      }
      return;
    }
    anim.pause();
    setDurum('sevildi');
    const r = (e.currentTarget as HTMLElement).getBoundingClientRect();
    kalpSuzul(r.left + r.width * 0.62, r.top + 8, 6);
    const l = k.tur === 'tilki' ? TILKI_SOZ : TAVSAN_SOZ;
    setBalon(l[Math.floor(Math.random() * l.length)]);
    window.setTimeout(() => { setBalon(null); setDurum('kosar'); anim.play(); }, 1900);
  };

  return (
    <div ref={ref} className={`ar-yaratik ar-${k.tur} is-${durum} ${yon === -1 ? 'is-sol' : ''}`} style={{ width: k.boy }} onPointerDown={sev}>
      {balon && <span className="ar-tilki-balon">{balon}</span>}
      <div className="ar-tilki-don">{k.tur === 'tilki' ? <TilkiYuruyen width={k.boy} /> : <TavsanZiplayan width={k.boy} />}</div>
      <span className="ar-tilki-golge" />
    </div>
  );
}

export default function GezinenTilki({ ilkGecikmeMs = 75_000 }: { ilkGecikmeMs?: number }) {
  const [aktif, setAktif] = useState<Kosu | null>(null);
  const kuyruk = useRef<Kosu[]>([]);
  const aktifRef = useRef<Kosu | null>(null);
  const yoldasAcik = useRef(false);
  const sayac = useRef(0);

  const siradaki = () => {
    if (aktifRef.current || yoldasAcik.current) return;
    const k = kuyruk.current.shift();
    if (!k) return;
    aktifRef.current = k;
    setAktif(k);
  };
  const bitti = (id: number) => {
    if (aktifRef.current?.id !== id) return;
    aktifRef.current = null;
    setAktif(null);
    // sıradaki yaratık kısa bir aradan sonra
    window.setTimeout(siradaki, 700);
  };

  const ekle = (tur: Tur, kip: Kip, adet = 1) => {
    if (azalt()) return;
    const dar = window.innerWidth < 640;
    for (let i = 0; i < adet; i++) {
      kuyruk.current.push({
        id: ++sayac.current,
        tur, kip,
        yon: Math.random() < 0.5 ? 1 : -1,
        hiz: tur === 'tavsan' ? rnd(110, 150) : rnd(95, 160),
        boy: tur === 'tavsan' ? (dar ? rnd(58, 70) : rnd(76, 96)) : (dar ? rnd(64, 80) : rnd(84, 118)),
        durur: kip === 'gecis' && Math.random() < 0.7,
      });
    }
    siradaki();
  };

  useEffect(() => {
    let t = window.setTimeout(function dongu() {
      if (document.visibilityState === 'visible' && !kuyruk.current.length) {
        const r = Math.random();
        if (r < 0.5) ekle('tilki', 'gecis');
        else if (r < 0.72) ekle('tilki', 'selam');
        else ekle('tavsan', 'gecis');
      }
      t = window.setTimeout(dongu, rnd(100_000, 240_000));
    }, ilkGecikmeMs);
    const adet = (e: Event) => Math.max(1, Math.min(8, Number((e as CustomEvent).detail?.adet) || 1));
    const onTilki = (e: Event) => ekle('tilki', (e as CustomEvent).detail?.kip === 'selam' ? 'selam' : 'gecis', adet(e));
    const onTavsan = (e: Event) => ekle('tavsan', 'gecis', adet(e));
    const onYoldas = (e: Event) => {
      yoldasAcik.current = !!(e as CustomEvent).detail?.acik;
      if (!yoldasAcik.current) window.setTimeout(siradaki, 1200);
    };
    window.addEventListener('arzu:tilki', onTilki);
    window.addEventListener('arzu:tavsan', onTavsan);
    window.addEventListener('arzu:yoldas-durum', onYoldas);
    return () => {
      window.clearTimeout(t);
      window.removeEventListener('arzu:tilki', onTilki);
      window.removeEventListener('arzu:tavsan', onTavsan);
      window.removeEventListener('arzu:yoldas-durum', onYoldas);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!aktif) return null;
  return (
    <div className="ar-tilki-yol" aria-hidden="true">
      <Yaratik key={aktif.id} k={aktif} onBitti={bitti} />
    </div>
  );
}
