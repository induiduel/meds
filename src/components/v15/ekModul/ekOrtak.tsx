import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Check, Pause, Play, RotateCcw, RotateCw, Settings2, SkipForward, X } from 'lucide-react';
import { klipUrl, type EkEtkinlik, type EkModul } from './ekVeri';

/** Ekran notu biçimi: paragraf, `- **Anahtar:** açıklama` maddeleri, `> [!IMPORTANT] …` vurgu kutusu, **kalın** */
const kalin = (s: string): React.ReactNode[] =>
  s.split(/(\*\*[^*]+\*\*)/g).filter(Boolean).map((p, i) => (p.startsWith('**') ? <b key={i}>{p.slice(2, -2)}</b> : <React.Fragment key={i}>{p}</React.Fragment>));

/** `okunan`: o an anlatılan satırın sırası (1 tabanlı, boş olmayan satırlar; pdf_esle.py::ekran_maddeleri ile aynı sayım) */
export const EkMd: React.FC<{ md: string; okunan?: number }> = ({ md, okunan }) => {
  const out: React.ReactNode[] = [];
  let liste: [string, number][] = [];
  const bosalt = () => {
    if (liste.length) out.push(<ul key={`l${out.length}`}>{liste.map(([x, n], i) => <li key={i} className={n === okunan ? 'is-okunan' : undefined}>{kalin(x)}</li>)}</ul>);
    liste = [];
  };
  md.split('\n').map((s) => s.trim()).filter(Boolean).forEach((s, i) => {
    const sinif = i + 1 === okunan ? ' is-okunan' : '';
    if (s.startsWith('- ')) { liste.push([s.slice(2), i + 1]); return; }
    bosalt();
    const v = /^>\s*\[!(IMPORTANT|NOTE)\]\s*(.*)$/.exec(s);
    if (v) out.push(<p key={`v${out.length}`} className={`ekm-vurgu is-${v[1].toLowerCase()}${sinif}`}>{kalin(v[2])}</p>);
    else out.push(<p key={`p${out.length}`} className={sinif.trim() || undefined}>{kalin(s.replace(/^>\s*/, ''))}</p>);
  });
  bosalt();
  return <div className="ekm-md">{out}</div>;
};

/* ——— sıralı klip oynatıcı: tek ortak Audio, klipler art arda; sayfada aynı anda tek ses ———
 * Ses öğesi modül düzeyinde tektir: konu değişince yeni öğe açılmaz, telefonun kilit ekranında / arka planda
 * çalarken bir sonraki konuya geçişte oynatma izni kaybolmaz. Kilit ekranı ve kulaklık tuşları Media Session ile. */
let ortak: HTMLAudioElement | null = null;
const sesOgesi = () => {
  if (!ortak) { ortak = new Audio(); ortak.preload = 'auto'; }
  return ortak;
};
let sahip = 0; // öğeyi şu an kullanan useSira örneği
let sahipSay = 0;
export const HIZLAR = [0.75, 0.85, 1, 1.15, 1.25, 1.5, 1.75, 2];
const HIZ_KEY = 'medsoru_ek_modul_hiz';
export const GECIS_KEY = 'medsoru_ek_modul_oto_gecis';
export const otoGecisAcik = () => { try { return localStorage.getItem(GECIS_KEY) !== '0'; } catch { return true; } };
const ms = (): MediaSession | null => ('mediaSession' in navigator ? navigator.mediaSession : null);
const msEylem = (a: MediaSessionAction, h: MediaSessionActionHandler | null) => { try { ms()?.setActionHandler(a, h); } catch { /* desteklenmiyor */ } };

export function useSira(m: EkModul, klipler: string[], bitti?: () => void, baslik?: (i: number) => string) {
  const kimlik = useMemo(() => ++sahipSay, []);
  const [i, setI] = useState(-1);
  const [caliyor, setCaliyor] = useState(false);
  const [hiz, setHiz] = useState(() => { try { return Number(localStorage.getItem(HIZ_KEY)) || 1; } catch { return 1; } });
  const [an2, setAn2] = useState({ t: 0, d: 0 });
  const durum = useRef({ klipler, bitti, hiz, m, baslik });
  durum.current = { klipler, bitti, hiz, m, baslik };
  const imza = klipler.join('|');
  const iRef = useRef(i);
  iRef.current = i;

  const durdur = useCallback(() => {
    if (sahip === kimlik) ortak?.pause();
    setCaliyor(false);
    setI(-1);
  }, [kimlik]);
  const cal = useCallback((n: number) => {
    const d = durum.current;
    // klibi olmayan parça atlanır (ses henüz üretilmemiş olabilir)
    while (n < d.klipler.length && !klipUrl(d.m, d.klipler[n])) n++;
    if (n < 0) n = 0;
    if (n >= d.klipler.length) { durdur(); d.bitti?.(); return; }
    const a = sesOgesi();
    sahip = kimlik;
    a.onended = () => cal(n + 1);
    a.onpause = () => { if (sahip === kimlik && !a.ended) setCaliyor(false); };
    a.onplay = () => setCaliyor(true);
    a.onerror = () => cal(n + 1);
    a.ontimeupdate = () => setAn2({ t: a.currentTime, d: a.duration || 0 });
    a.src = klipUrl(d.m, d.klipler[n]) as string;
    a.playbackRate = d.hiz;
    setI(n);
    const s = ms();
    if (s) {
      try { s.metadata = new MediaMetadata({ title: d.baslik?.(n) || `Bölüm ${n + 1}`, artist: d.m.ozet.ad, album: 'MeDSor · Ek modüller' }); } catch { /* yok */ }
    }
    a.play().catch(() => setCaliyor(false));
  }, [durdur, kimlik]);
  const dugme = useCallback(() => {
    const a = ortak;
    if (i >= 0 && a && sahip === kimlik) { if (a.paused) a.play().catch(() => undefined); else a.pause(); } else cal(Math.max(0, i));
  }, [i, cal, kimlik]);
  const hizAyarla = useCallback((y: number) => {
    setHiz(y);
    try { localStorage.setItem(HIZ_KEY, String(y)); } catch { /* yok */ }
    if (ortak && sahip === kimlik) ortak.playbackRate = y;
  }, [kimlik]);
  const hizDegis = useCallback(() => hizAyarla(HIZLAR[(HIZLAR.indexOf(durum.current.hiz) + 1) % HIZLAR.length] || 1), [hizAyarla]);
  const atla = useCallback((sn: number) => {
    const a = ortak;
    if (!a || sahip !== kimlik || iRef.current < 0) return;
    const t = a.currentTime + sn;
    if (t < 0 && iRef.current > 0 && sn < 0 && a.currentTime < 1.5) { cal(iRef.current - 1); return; }
    if (a.duration && t >= a.duration) { cal(iRef.current + 1); return; }
    a.currentTime = Math.max(0, t);
  }, [cal, kimlik]);
  const ileri = useCallback(() => { if (iRef.current >= 0) cal(iRef.current + 1); }, [cal]);
  const geri = useCallback(() => { if (iRef.current > 0) cal(iRef.current - 1); else atla(-999); }, [cal, atla]);

  // kilit ekranı / bildirim / kulaklık tuşları: yalnız bu örnek çalarken
  useEffect(() => {
    const s = ms();
    if (!s || i < 0) return;
    s.playbackState = caliyor ? 'playing' : 'paused';
    if (!caliyor) return;
    (window as any).__medsorMsSahip = 'ek-modul';
    window.dispatchEvent(new Event('medsor:canli-ders-oynuyor')); // müzik susar
    msEylem('play', () => ortak?.play().catch(() => undefined));
    msEylem('pause', () => ortak?.pause());
    msEylem('nexttrack', ileri);
    msEylem('previoustrack', geri);
    msEylem('seekforward', (e) => atla(e.seekOffset || 10));
    msEylem('seekbackward', (e) => atla(-(e.seekOffset || 10)));
  }, [i, caliyor, ileri, geri, atla]);

  // klip listesi değişince (başka konu/soru) ve sayfa kapanınca bu örnek susar
  useEffect(() => () => { if (sahip === kimlik) ortak?.pause(); setCaliyor(false); setI(-1); }, [imza, kimlik]);
  const sesVar = useMemo(() => klipler.some((k) => klipUrl(m, k)), [imza, m]); // eslint-disable-line react-hooks/exhaustive-deps
  const sure = useMemo(() => klipler.reduce((t, k) => t + (m.klip[k]?.sure || 0), 0), [imza, m]); // eslint-disable-line react-hooks/exhaustive-deps
  /** çalan klibin içindeki an (sn); cümle takibi bununla yapılır */
  const an = useCallback(() => (sahip === kimlik ? ortak?.currentTime || 0 : 0), [kimlik]);
  return { i, caliyor, hiz, sesVar, sure, cal, dugme, durdur, hizDegis, hizAyarla, an, atla, ileri, geri, klipAn: an2 };
}
export type Sira = ReturnType<typeof useSira>;

export const dk = (sn: number) => (sn >= 60 ? `${Math.round(sn / 60)} dk` : `${Math.max(1, Math.round(sn))} sn`);
const sa = (sn: number) => `${Math.floor(sn / 60)}:${String(Math.floor(sn % 60)).padStart(2, '0')}`;

/** Oynatma çubuğu: oynat/duraklat, parça sayacı, 10 sn atlama, ayarlar (hız, otomatik geçiş).
 *  ikili: her parça iki klip (soru + çözüm); sayaç ve ilerleme parçaya göre. */
export const OynatCubugu: React.FC<{ sira: Sira; n: number; etiket: string; birim: string; ikili?: boolean; gecis?: { acik: boolean; degis: (v: boolean) => void } }> = ({ sira, n, etiket, birim, ikili, gecis }) => {
  const [ayar, setAyar] = useState(false);
  const bol = ikili ? 2 : 1;
  const p = Math.floor(sira.i / bol);
  return (
    <div className={`ekm-cubuk v15-card${sira.caliyor ? ' is-caliyor' : ''}${ayar ? ' is-ayar' : ''}`}>
      <div className="ekm-cubuk-ana">
        {sira.sesVar && sira.i >= 0 && <button type="button" className="ekm-kucuk" onClick={() => sira.atla(-10)} aria-label="10 saniye geri"><RotateCcw aria-hidden /><small>10</small></button>}
        <button type="button" className="ekm-oynat" onClick={sira.dugme} disabled={!sira.sesVar} aria-label={sira.caliyor ? 'Duraklat' : etiket}>
          {sira.caliyor ? <Pause aria-hidden /> : <Play aria-hidden />}
        </button>
        {sira.sesVar && sira.i >= 0 && <button type="button" className="ekm-kucuk" onClick={() => sira.atla(10)} aria-label="10 saniye ileri"><RotateCw aria-hidden /><small>10</small></button>}
        <div className="ekm-cubuk-yazi">
          <b>{sira.sesVar ? (sira.i >= 0 ? `${birim} ${p + 1} / ${n}` : etiket) : 'Ses hazırlanıyor'}</b>
          <span>{sira.sesVar ? (sira.i >= 0 && sira.klipAn.d ? `${sa(sira.klipAn.t)} / ${sa(sira.klipAn.d)} · ${String(sira.hiz).replace('.', ',')}×` : `EMA sesi · ${dk(sira.sure)}`) : 'Metinler hazır; sesli anlatım yakında eklenecek.'}</span>
        </div>
        {sira.sesVar && (
          <>
            {sira.i >= 0 && <button type="button" className="ekm-kucuk" onClick={sira.ileri} aria-label="Sonraki bölüm"><SkipForward aria-hidden /></button>}
            <button type="button" className={`ekm-kucuk${ayar ? ' is-on' : ''}`} onClick={() => setAyar(!ayar)} aria-expanded={ayar} aria-label="Oynatıcı ayarları"><Settings2 aria-hidden /></button>
          </>
        )}
        <div className="ekm-ilerle" aria-hidden><i style={{ width: `${sira.i >= 0 ? ((sira.i + (sira.klipAn.d ? sira.klipAn.t / sira.klipAn.d : 0)) / (n * bol)) * 100 : 0}%` }} /></div>
      </div>
      {ayar && sira.sesVar && (
        <div className="ekm-ayar" role="group" aria-label="Oynatıcı ayarları">
          <div className="ekm-ayar-satir">
            <span>Okuma hızı</span>
            <div className="ekm-hizlar">
              {HIZLAR.map((h) => <button key={h} type="button" className={sira.hiz === h ? 'is-on' : ''} aria-pressed={sira.hiz === h} onClick={() => sira.hizAyarla(h)}>{String(h).replace('.', ',')}×</button>)}
            </div>
          </div>
          {gecis && (
            <label className="ekm-ayar-satir">
              <span>Konu bitince sonraki konuya otomatik geç<small>Ekran kilitliyken ya da başka sekmedeyken de sürer.</small></span>
              <input type="checkbox" checked={gecis.acik} onChange={(e) => gecis.degis(e.target.checked)} />
            </label>
          )}
          {sira.i >= 0 && (
            <div className="ekm-ayar-satir">
              <span>Dersi başa al</span>
              <button type="button" className="v15-btn is-ghost" onClick={() => { sira.durdur(); }}>Durdur ve başa dön</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

/* ——— etkinlikler ——— */
const karistir = <T,>(a: T[]): T[] => {
  const b = a.map((x, i) => [x, i] as const);
  for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; }
  // karıştırma özgün sırayla aynı çıkarsa bir kaydır (sıralama etkinliği çözülmüş gelmesin)
  if (b.length > 1 && b.every(([, k], i) => k === i)) b.push(b.shift() as (typeof b)[number]);
  return b.map(([x]) => x);
};

const DogruYanlis: React.FC<{ e: Extract<EkEtkinlik, { tur: 'dogru_yanlis' }> }> = ({ e }) => {
  const [c, setC] = useState<Record<number, boolean>>({});
  return (
    <ul className="ekm-dy">
      {e.ifadeler.map((f, i) => {
        const yanit = c[i];
        const bildi = yanit !== undefined && yanit === f.dogru;
        return (
          <li key={i} className={yanit === undefined ? '' : bildi ? 'is-ok' : 'is-bad'}>
            <p>{f.metin}</p>
            {yanit === undefined ? (
              <div className="ekm-dy-dugme">
                <button type="button" onClick={() => setC({ ...c, [i]: true })}><Check aria-hidden /> Doğru</button>
                <button type="button" onClick={() => setC({ ...c, [i]: false })}><X aria-hidden /> Yanlış</button>
              </div>
            ) : (
              <p className="ekm-dy-ack"><b>{bildi ? 'Bildin.' : 'Bilemedin.'} {f.dogru ? 'Bu doğru.' : 'Bu yanlış.'}</b> {f.aciklama}</p>
            )}
          </li>
        );
      })}
    </ul>
  );
};

const Sirala: React.FC<{ e: Extract<EkEtkinlik, { tur: 'sirala' }> }> = ({ e }) => {
  const [karisik, setKarisik] = useState(() => karistir(e.adimlar));
  const [secim, setSecim] = useState<string[]>([]);
  const bitti = secim.length === e.adimlar.length;
  const dogru = bitti && secim.every((s, i) => s === e.adimlar[i]);
  const sifirla = () => { setSecim([]); setKarisik(karistir(e.adimlar)); };
  return (
    <div className="ekm-sirala">
      <p className="ekm-et-soru">{e.soru} <span>Sırayla dokun.</span></p>
      <ol>
        {karisik.map((a) => {
          const n = secim.indexOf(a);
          const dogruYer = bitti && e.adimlar[n] === a;
          return (
            <li key={a}>
              <button type="button" disabled={n >= 0} className={n >= 0 ? (bitti ? (dogruYer ? 'is-ok' : 'is-bad') : 'is-sec') : ''} onClick={() => setSecim([...secim, a])}>
                <i>{n >= 0 ? n + 1 : ''}</i><span>{a}</span>
              </button>
            </li>
          );
        })}
      </ol>
      {bitti && (
        <div className={`ekm-sonuc ${dogru ? 'is-ok' : 'is-bad'}`}>
          <p><b>{dogru ? 'Sıra doğru.' : 'Sıra tam tutmadı.'}</b> {e.aciklama}</p>
          {!dogru && <p className="ekm-dogru-sira">Doğru sıra: {e.adimlar.join(' → ')}</p>}
        </div>
      )}
      {secim.length > 0 && <button type="button" className="v15-btn is-ghost ekm-yeniden" onClick={sifirla}><RotateCcw aria-hidden /> Baştan</button>}
    </div>
  );
};

const Esle: React.FC<{ e: Extract<EkEtkinlik, { tur: 'esle' }> }> = ({ e }) => {
  const sag = useMemo(() => karistir(e.ciftler.map((c) => c.sag)), [e]);
  const [sol, setSol] = useState<string | null>(null);
  const [tamam, setTamam] = useState<Record<string, string>>({});
  const [hata, setHata] = useState<string | null>(null);
  const sagSec = (s: string) => {
    if (!sol) return;
    if (e.ciftler.find((c) => c.sol === sol)?.sag === s) { setTamam({ ...tamam, [sol]: s }); setSol(null); } else {
      setHata(s);
      window.setTimeout(() => setHata(null), 500);
    }
  };
  const bitti = Object.keys(tamam).length === e.ciftler.length;
  return (
    <div className="ekm-esle">
      <p className="ekm-et-soru">Soldan birini seç, sağdaki eşine dokun.</p>
      <div className="ekm-esle-izgara">
        <div>
          {e.ciftler.map((c) => (
            <button key={c.sol} type="button" disabled={!!tamam[c.sol]} className={tamam[c.sol] ? 'is-ok' : sol === c.sol ? 'is-sec' : ''} onClick={() => setSol(c.sol)}>{c.sol}</button>
          ))}
        </div>
        <div>
          {sag.map((s) => {
            const bulundu = Object.values(tamam).includes(s);
            return <button key={s} type="button" disabled={bulundu || !sol} className={bulundu ? 'is-ok' : hata === s ? 'is-bad' : ''} onClick={() => sagSec(s)}>{s}</button>;
          })}
        </div>
      </div>
      {bitti && (
        <div className="ekm-sonuc is-ok">
          <p><b>Hepsi eşleşti.</b></p>
          <ul>{e.ciftler.map((c) => <li key={c.sol}><b>{c.sol}</b> → {c.sag}</li>)}</ul>
        </div>
      )}
    </div>
  );
};

export const Etkinlik: React.FC<{ e: EkEtkinlik }> = ({ e }) => (
  <section className="ekm-etkinlik v15-card">
    <h3>{e.baslik}</h3>
    {e.tur === 'dogru_yanlis' ? <DogruYanlis e={e} /> : e.tur === 'sirala' ? <Sirala e={e} /> : <Esle e={e} />}
  </section>
);
