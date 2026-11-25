/**
 * Ders özeti sesli oynatıcı çekirdeği — hem klasik ekran (DersOzetView) hem alternatif çalışma ekranı
 * (DersOzetYeni) aynı davranışı kullanır: klipler sırayla çalar, çalan öğe (madde) işaretlenir ve görünür tutulur,
 * maddeye dokununca oradan okur; hız ve kaldığı yer cihazda saklanır.
 */
import { useEffect, useMemo, useRef, useState } from 'react';
import { klipAdres, klipSirasi, ogeKlibi, ozIlerlemeYaz, type OzDers } from './dersOzetVeri';

export const OZET_HIZLAR = [1, 1.25, 1.5, 1.75];
const HIZ_KEY = 'medsoru_ders_ozet_hiz_v1';
const hizOku = () => { try { const v = Number(localStorage.getItem(HIZ_KEY)); return OZET_HIZLAR.includes(v) ? v : 1; } catch { return 1; } };

export function useOzetOynatici(d: OzDers | null, ders: string) {
  const ses = useRef<HTMLAudioElement | null>(null);
  const [klip, setKlip] = useState<string | null>(null);
  const [caliyor, setCaliyor] = useState(false);
  const [aktif, setAktif] = useState<string | null>(null);
  const [ilerleme, setIlerleme] = useState(0);
  const [hiz, setHiz] = useState(hizOku);
  const sira = useMemo(() => (d ? klipSirasi(d) : []), [d]);
  const toplam = d?.sure || 1;

  useEffect(() => () => { ses.current?.pause(); }, []);
  const yukle = (k: string, bas = 0) => {
    if (!d) return;
    let a = ses.current;
    if (!a) {
      a = new Audio();
      ses.current = a;
      a.addEventListener('play', () => setCaliyor(true));
      a.addEventListener('pause', () => setCaliyor(false));
    }
    a.onended = () => {
      const i = sira.indexOf(k);
      if (i >= 0 && i + 1 < sira.length) yukle(sira[i + 1]);
      else { setCaliyor(false); setAktif(null); ozIlerlemeYaz(ders, { klip: undefined, t: undefined, bitti: new Date().toISOString() }); }
    };
    let sonYaz = 0;
    a.ontimeupdate = () => {
      const t = a!.currentTime;
      const x = d.ses?.klipler[k];
      if (!x) return;
      const once = sira.slice(0, sira.indexOf(k)).reduce((s, q) => s + (d.ses?.klipler[q]?.sure || 0), 0);
      setIlerleme((once + t) / toplam);
      if (Date.now() - sonYaz > 5000) { sonYaz = Date.now(); ozIlerlemeYaz(ders, { klip: k, t: Math.max(0, t - 2) }); }
      const oge = Object.entries(x.oge).find(([, [b, s]]) => t >= b - 0.05 && t < s + 0.4)?.[0];
      const id = oge === 'baslik' ? null : oge;
      if (id) setAktif((o) => {
        if (o !== id) document.getElementById(`dz-${id}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return id;
      });
    };
    a.src = klipAdres(d, k);
    a.playbackRate = hiz;
    a.currentTime = bas;
    setKlip(k);
    a.play().catch(() => setCaliyor(false));
  };
  const calYaDur = () => {
    const a = ses.current;
    if (!klip || !a) {
      const il = (() => { try { return JSON.parse(localStorage.getItem('medsoru_ders_ozet_v1') || '{}')[ders]; } catch { return null; } })();
      return il?.klip && sira.includes(il.klip) ? yukle(il.klip, il.t || 0) : yukle(sira[0]);
    }
    if (a.paused) a.play().catch(() => undefined); else a.pause();
  };
  const atla = (y: number) => { const i = sira.indexOf(klip || ''); const j = Math.min(sira.length - 1, Math.max(0, i + y)); if (sira[j]) yukle(sira[j]); };
  const buradan = (oge: string) => {
    if (!d?.ses || !klip) return; // yalnız dinleme başladıysa dokununca atlar (okurken yanlışlıkla ses açılmasın)
    const k = ogeKlibi(d, oge);
    if (k) yukle(k, d.ses.klipler[k].oge[oge][0]);
  };
  const hizDegis = () => {
    const h = OZET_HIZLAR[(OZET_HIZLAR.indexOf(hiz) + 1) % OZET_HIZLAR.length];
    setHiz(h);
    try { localStorage.setItem(HIZ_KEY, String(h)); } catch { /* yoksay */ }
    if (ses.current) ses.current.playbackRate = h;
  };
  const klipAdi = !d || !klip ? '' : klip === 'g' ? 'Giriş' : klip === 'a' ? 'Akılda kalması gerekenler' : d.bolumler[Number(klip.slice(2)) - 1]?.baslik || '';
  const serbest = (k: string) => { if (sira.includes(k)) yukle(k); };
  return {
    caliyor, aktif, ilerleme, hiz, klipAdi, klip, basladi: !!klip,
    calYaDur, buradan, hizDegis, onceki: () => atla(-1), sonraki: () => atla(1), dur: () => ses.current?.pause(), serbest,
  };
}
