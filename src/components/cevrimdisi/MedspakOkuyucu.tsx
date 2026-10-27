import { useEffect, useMemo, useRef, useState } from 'react';
import { FileText, FileUp, PenLine, X } from 'lucide-react';
import type { MedspakDers } from '../../services/medspakOku';

/**
 * Çevrimdışı merkezi › Ders paketi (.medspak) aç (R7): dosya cihazda açılır (sunucuya gitmez); ekran maddeleri bölüm
 * bölüm, ses çalınca o anki paragraf zamanlamaya (ses_parca.zamanlama) göre vurgulanır. Opus'u çalamayan tarayıcıya not.
 */
const TUR: Record<string, string> = { terim: 'Terim', sayi: 'Sayı', tuzak: 'Tuzak', cikmis: 'Çıkmış', tanim: 'Tanım' };

export default function MedspakOkuyucu() {
  const [ders, setDers] = useState<MedspakDers | null>(null);
  const [hata, setHata] = useState('');
  const [yukleniyor, setYukleniyor] = useState(false);
  const [an, setAn] = useState(0);
  const girdi = useRef<HTMLInputElement>(null);
  const ses = useRef<HTMLAudioElement>(null);

  useEffect(() => () => {
    if (ders?.ses?.url) URL.revokeObjectURL(ders.ses.url);
    for (const p of ders?.pdfler || []) URL.revokeObjectURL(p.url);
  }, [ders]);

  const ac = async (f: File | undefined) => {
    if (!f) return;
    setHata(''); setYukleniyor(true);
    try {
      const { medspakAc } = await import('../../services/medspakOku');
      setDers(await medspakAc(f));
      setAn(0);
    } catch (e: any) {
      setHata(e?.message || 'Paket açılamadı.');
    } finally {
      setYukleniyor(false);
      if (girdi.current) girdi.current.value = '';
    }
  };

  // Telefondan gelen paket: Android "Paylaş → MeDSor" (sw.js önbelleğe koyar, ?paylasim=1) ya da masaüstü PWA
  // "Birlikte aç" (manifest file_handlers → launchQueue)
  useEffect(() => {
    const q = new URLSearchParams(location.search);
    if (q.get('paylasim') === '1') {
      q.delete('paylasim');
      history.replaceState(history.state, '', location.pathname + (q.toString() ? `?${q}` : '') + location.hash);
      void (async () => {
        try {
          const c = await caches.open('medsor-paylasim');
          const y = await c.match('/__paylasilan-paket');
          if (!y) { setHata('Paylaşılan paket alınamadı.'); return; }
          await c.delete('/__paylasilan-paket');
          const ad = decodeURIComponent(y.headers.get('X-Ad') || 'paket.medspak');
          await ac(new File([await y.blob()], ad));
          kok.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } catch (e: any) { setHata(e?.message || 'Paylaşılan paket açılamadı.'); }
      })();
    }
    const lq = (window as any).launchQueue;
    lq?.setConsumer?.(async (p: any) => {
      const h = p?.files?.[0];
      if (h?.getFile) await ac(await h.getFile());
    });
  }, []);

  // Ders listesindeki "Paketi aç": cihazdaki (çevrimdışı indirilmiş) .medspak, internetsiz açılır
  const kok = useRef<HTMLElement>(null);
  useEffect(() => {
    const dinle = (e: Event) => {
      const key = String((e as CustomEvent).detail || '');
      if (!key) return;
      setHata(''); setYukleniyor(true);
      void (async () => {
        try {
          const { medspakCihazdan } = await import('../../services/cevrimdisi/paketMotoru');
          const f = await medspakCihazdan(key);
          if (!f) throw new Error('Bu ders paketi cihazda yok.');
          const { medspakAc } = await import('../../services/medspakOku');
          setDers(await medspakAc(f));
          setAn(0);
          kok.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } catch (er: any) {
          setHata(er?.message || 'Paket açılamadı.');
        } finally { setYukleniyor(false); }
      })();
    };
    window.addEventListener('cv-medspak-ac', dinle);
    return () => window.removeEventListener('cv-medspak-ac', dinle);
  }, []);

  const etkin = useMemo(() => {
    const z = ders?.ses?.zamanlama || [];
    return z.findIndex((x) => an >= x[0] && an < x[1]);
  }, [an, ders]);
  const paragraflar = useMemo(() => {
    const m = new Map<number, MedspakDers['cumleler']>();
    for (const c of ders?.cumleler || []) m.set(c.paragraf, [...(m.get(c.paragraf) || []), c]);
    return [...m.entries()];
  }, [ders]);
  useEffect(() => {
    if (etkin >= 0) document.getElementById(`mp-p${etkin}`)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }, [etkin]);
  const opusYok = ders?.ses?.bicim === 'opus' && typeof document !== 'undefined'
    && !document.createElement('audio').canPlayType('audio/ogg; codecs=opus');

  return (
    <section className="cv-kart" aria-labelledby="cv-mp-b" ref={kok}>
      <div className="cv-kart-bas">
        <h2 id="cv-mp-b">Ders paketi aç (.medspak)</h2>
        {ders && (
          <button type="button" className="cv-btn" onClick={() => setDers(null)} aria-label="Paketi kapat"><X /></button>
        )}
      </div>
      {!ders ? (
        <>
          <p className="cv-aciklama">
            Tek dosyalık ders paketini bu cihazda aç: sesli anlatım, ekran maddeleri, vurgular ve ders PDF'i. Dosya sunucuya gönderilmez.
          </p>
          <button type="button" className="cv-btn is-birincil" disabled={yukleniyor} onClick={() => girdi.current?.click()}>
            <FileUp /> {yukleniyor ? 'Açılıyor…' : 'Dosya seç'}
          </button>
          <input ref={girdi} type="file" accept=".medspak" hidden onChange={(e) => ac(e.target.files?.[0])} />
          {hata && <p className="cv-hata" role="alert">{hata}</p>}
        </>
      ) : (
        <div className="mp-okuyucu">
          <p className="mp-ozet">
            <b>{ders.baslik}</b> · {ders.cumleler.length} cümle · {ders.paragrafSayisi} paragraf · {ders.slaytSayisi} slayt ·{' '}
            {ders.soruSayisi} soru{ders.ses ? ` · ${Math.round(ders.ses.sureSn / 60)} dk ses` : ''}
          </p>
          {ders.pdfler.map((p) => (
            <a key={p.url} className="cv-btn" href={p.url} target="_blank" rel="noreferrer" download={p.ad}>
              <FileText /> Ders PDF'ini aç
            </a>
          ))}
          {ders.ses && (
            <audio ref={ses} className="mp-ses" controls preload="metadata" src={ders.ses.url}
                   onTimeUpdate={(e) => setAn((e.target as HTMLAudioElement).currentTime)} />
          )}
          {opusYok && <p className="cv-hata">Bu tarayıcı paketteki Opus sesini çalamıyor; metin yine okunabilir.</p>}
          <ol className="mp-paragraflar">
            {paragraflar.map(([p, cs]) => (
              <li key={p} id={`mp-p${p}`} className={p === etkin ? 'is-etkin' : ''}
                  onClick={() => { const z = ders.ses?.zamanlama?.[p]; if (z && ses.current) { ses.current.currentTime = z[0]; void ses.current.play(); } }}>
                {cs.map((c) => (
                  <p key={c.id} className={`mp-cumle d${c.duzey}`}>
                    {c.ekran.replace(/\*\*/g, '')}
                    {c.vurgu.slice(0, 3).map((v, i) => <em key={i} className={`mp-vurgu is-${v.tur}`}>{TUR[v.tur] || v.tur}</em>)}
                    {c.cikmis.length > 0 && <em className="mp-vurgu is-cikmis">Çıkmış</em>}
                    {c.cizim > 0 && <PenLine className="mp-cizim" aria-label="Bu cümlede canlı çizim var" />}
                  </p>
                ))}
              </li>
            ))}
          </ol>
        </div>
      )}
    </section>
  );
}
