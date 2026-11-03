/**
 * Yoldaş tilki: sol altta oturan küçük tilki.
 * - Gece (23:00–05:00) oturumda bir kez kendiliğinden gelir ve uyur ("z" harfleri); dokununca uyanır, "Sen de uyu." der, gider.
 * - Koşan tilkiye ikinci kez dokununca (`arzu:yoldas` olayı) gelir, 5 dakika kalır; dokununca kısa bir söz, iki dokunuşta kalplerle gider.
 */
import React, { useEffect, useRef, useState } from 'react';
import { TilkiOturan } from './cizimler';
import { kalpSuzul } from './kalpPatlamasi';

type Durum = 'yok' | 'uyur' | 'oturur';
const SOZLER = ['Buradayım.', 'Devam et, ben bakıyorum.', 'Seninleyim.', 'Güzel gidiyor.'];
const geceMi = (d = new Date()) => d.getHours() >= 23 || d.getHours() < 5;

export default function Yoldas() {
  const [durum, setDurum] = useState<Durum>('yok');
  const [balon, setBalon] = useState<string | null>(null);
  const [gidiyor, setGidiyor] = useState(false);
  const sonDokunus = useRef(0);
  const gitT = useRef<number | undefined>(undefined);
  const geceGeldi = useRef(false);

  const git = (gecikme = 0) => {
    window.clearTimeout(gitT.current);
    gitT.current = window.setTimeout(() => {
      setGidiyor(true);
      window.setTimeout(() => { setDurum('yok'); setGidiyor(false); setBalon(null); }, 600);
    }, gecikme);
  };

  useEffect(() => {
    const onYoldas = () => {
      setGidiyor(false);
      setDurum('oturur');
      git(5 * 60_000);
    };
    window.addEventListener('arzu:yoldas', onYoldas);
    // Gece: ilk 2 dakika içinde bir kez uyuyan tilki
    const t = window.setTimeout(() => {
      if (!geceGeldi.current && geceMi() && document.visibilityState === 'visible') {
        geceGeldi.current = true;
        setDurum('uyur');
        git(100_000);
      }
    }, 95_000);
    return () => { window.removeEventListener('arzu:yoldas', onYoldas); window.clearTimeout(t); window.clearTimeout(gitT.current); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const dokun = (e: React.PointerEvent) => {
    const r = (e.currentTarget as HTMLElement).getBoundingClientRect();
    if (durum === 'uyur') {
      setDurum('oturur');
      setBalon('Sen de uyu.');
      kalpSuzul(r.left + r.width / 2, r.top + 10, 3);
      git(2800);
      return;
    }
    const now = Date.now();
    if (now - sonDokunus.current < 1800) {
      kalpSuzul(r.left + r.width / 2, r.top + 10, 6);
      setBalon('Görüşürüz.');
      git(900);
      return;
    }
    sonDokunus.current = now;
    setBalon(SOZLER[Math.floor(Math.random() * SOZLER.length)]);
    window.setTimeout(() => setBalon(null), 2200);
  };

  useEffect(() => {
    window.dispatchEvent(new CustomEvent('arzu:yoldas-durum', { detail: { acik: durum !== 'yok' } }));
  }, [durum]);

  if (durum === 'yok') return null;
  return (
    <button type="button" className={`ar-yoldas is-${durum} ${gidiyor ? 'is-gidiyor' : ''}`} onPointerDown={dokun} aria-label={durum === 'uyur' ? 'Uyuyan tilki' : 'Yoldaş tilki'}>
      {balon && <span className="ar-yoldas-balon">{balon}</span>}
      {durum === 'uyur' && (
        <span className="ar-zzz" aria-hidden="true"><i>z</i><i>z</i><i>z</i></span>
      )}
      <TilkiOturan width={104} />
    </button>
  );
}
