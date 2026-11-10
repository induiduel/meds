import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Check, Pause, Play, RotateCcw, X } from 'lucide-react';
import { klipUrl, type EkEtkinlik, type EkModul } from './ekVeri';

/** Ekran notu biçimi: paragraf, `- **Anahtar:** açıklama` maddeleri, `> [!IMPORTANT] …` vurgu kutusu, **kalın** */
const kalin = (s: string): React.ReactNode[] =>
  s.split(/(\*\*[^*]+\*\*)/g).filter(Boolean).map((p, i) => (p.startsWith('**') ? <b key={i}>{p.slice(2, -2)}</b> : <React.Fragment key={i}>{p}</React.Fragment>));

export const EkMd: React.FC<{ md: string }> = ({ md }) => {
  const out: React.ReactNode[] = [];
  let liste: string[] = [];
  const bosalt = () => {
    if (liste.length) out.push(<ul key={`l${out.length}`}>{liste.map((x, i) => <li key={i}>{kalin(x)}</li>)}</ul>);
    liste = [];
  };
  md.split('\n').map((s) => s.trim()).filter(Boolean).forEach((s) => {
    if (s.startsWith('- ')) { liste.push(s.slice(2)); return; }
    bosalt();
    const v = /^>\s*\[!(IMPORTANT|NOTE)\]\s*(.*)$/.exec(s);
    if (v) out.push(<p key={`v${out.length}`} className={`ekm-vurgu is-${v[1].toLowerCase()}`}>{kalin(v[2])}</p>);
    else out.push(<p key={`p${out.length}`}>{kalin(s.replace(/^>\s*/, ''))}</p>);
  });
  bosalt();
  return <div className="ekm-md">{out}</div>;
};

/* ——— sıralı klip oynatıcı: tek Audio, klipler art arda; sayfada aynı anda tek ses ——— */
let etkin: HTMLAudioElement | null = null;
const HIZLAR = [1, 1.25, 1.5, 0.85];
const HIZ_KEY = 'medsoru_ek_modul_hiz';

export function useSira(m: EkModul, klipler: string[], bitti?: () => void) {
  const [i, setI] = useState(-1);
  const [caliyor, setCaliyor] = useState(false);
  const [hiz, setHiz] = useState(() => { try { return Number(localStorage.getItem(HIZ_KEY)) || 1; } catch { return 1; } });
  const ses = useRef<HTMLAudioElement | null>(null);
  const durum = useRef({ klipler, bitti, hiz, m });
  durum.current = { klipler, bitti, hiz, m };
  const imza = klipler.join('|');

  const durdur = useCallback(() => {
    ses.current?.pause();
    setCaliyor(false);
    setI(-1);
  }, []);
  const cal = useCallback((n: number) => {
    const d = durum.current;
    // klibi olmayan parça atlanır (ses henüz üretilmemiş olabilir)
    while (n < d.klipler.length && !klipUrl(d.m, d.klipler[n])) n++;
    if (n >= d.klipler.length) { durdur(); d.bitti?.(); return; }
    if (!ses.current) {
      ses.current = new Audio();
      ses.current.preload = 'auto';
    }
    const a = ses.current;
    if (etkin && etkin !== a) etkin.pause();
    etkin = a;
    a.onended = () => cal(n + 1);
    a.onpause = () => { if (etkin === a && !a.ended) setCaliyor(false); };
    a.onplay = () => setCaliyor(true);
    a.onerror = () => cal(n + 1);
    a.src = klipUrl(d.m, d.klipler[n]) as string;
    a.playbackRate = d.hiz;
    setI(n);
    a.play().catch(() => setCaliyor(false));
  }, [durdur]);
  const dugme = useCallback(() => {
    const a = ses.current;
    if (i >= 0 && a) { if (a.paused) a.play().catch(() => undefined); else a.pause(); } else cal(0);
  }, [i, cal]);
  const hizDegis = useCallback(() => {
    const y = HIZLAR[(HIZLAR.indexOf(durum.current.hiz) + 1) % HIZLAR.length];
    setHiz(y);
    try { localStorage.setItem(HIZ_KEY, String(y)); } catch { /* yok */ }
    if (ses.current) ses.current.playbackRate = y;
  }, []);
  // klip listesi değişince (başka konu/soru) ve sayfa kapanınca ses susar
  useEffect(() => () => { ses.current?.pause(); setCaliyor(false); setI(-1); }, [imza]);
  const sesVar = useMemo(() => klipler.some((k) => klipUrl(m, k)), [imza, m]); // eslint-disable-line react-hooks/exhaustive-deps
  const sure = useMemo(() => klipler.reduce((t, k) => t + (m.klip[k]?.sure || 0), 0), [imza, m]); // eslint-disable-line react-hooks/exhaustive-deps
  return { i, caliyor, hiz, sesVar, sure, cal, dugme, durdur, hizDegis };
}
export type Sira = ReturnType<typeof useSira>;

export const dk = (sn: number) => (sn >= 60 ? `${Math.round(sn / 60)} dk` : `${Math.max(1, Math.round(sn))} sn`);

/** Oynatma çubuğu: oynat/duraklat, parça sayacı, hız */
export const OynatCubugu: React.FC<{ sira: Sira; n: number; etiket: string; birim: string }> = ({ sira, n, etiket, birim }) => (
  <div className={`ekm-cubuk v15-card${sira.caliyor ? ' is-caliyor' : ''}`}>
    <button type="button" className="ekm-oynat" onClick={sira.dugme} disabled={!sira.sesVar} aria-label={sira.caliyor ? 'Duraklat' : etiket}>
      {sira.caliyor ? <Pause aria-hidden /> : <Play aria-hidden />}
    </button>
    <div className="ekm-cubuk-yazi">
      <b>{sira.sesVar ? (sira.i >= 0 ? `${birim} ${sira.i + 1} / ${n}` : etiket) : 'Ses hazırlanıyor'}</b>
      <span>{sira.sesVar ? `EMA sesi · ${dk(sira.sure)}` : 'Metinler hazır; sesli anlatım yakında eklenecek.'}</span>
    </div>
    <div className="ekm-ilerle" aria-hidden><i style={{ width: `${sira.i >= 0 ? ((sira.i + 1) / n) * 100 : 0}%` }} /></div>
    {sira.sesVar && (
      <>
        {sira.i >= 0 && <button type="button" className="ekm-kucuk" onClick={sira.durdur} aria-label="Başa dön"><RotateCcw aria-hidden /></button>}
        <button type="button" className="ekm-kucuk is-hiz" onClick={sira.hizDegis} aria-label="Okuma hızı">{String(sira.hiz).replace('.', ',')}×</button>
      </>
    )}
  </div>
);

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
