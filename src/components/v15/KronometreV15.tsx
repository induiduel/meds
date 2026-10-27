import React, { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { Flag, Pause, Play, Square, Timer, X } from 'lucide-react';
import '../../styles/v15/kronometre.css';

/**
 * v15 · Yüzen kronometre (tasarım sistemi v15 › T). İsteğe bağlı sayaç: kullanıcı başlatır/durdurur; sistemin ölçtüğü
 * çalışma süresine (calismaTakip) karışmaz. Menü › Araçlar › Kronometre ya da kenar menüsünden açılır
 * (`medsoru:kronometre` olayı). Küçük baloncuk; dokununca panel: başlat/duraklat, tur, bitir (geçmişe yazar), gizle.
 * Durum localStorage'da: sayfa değişse, yenilense de süre kaldığı yerden sürer.
 */
const KEY = 'medsoru_v15_kronometre';
interface Durum { acik: boolean; calisiyor: boolean; bas: number; birikmis: number; turlar: number[]; gecmis: { t: string; sn: number; tur: number }[] }
const BOS: Durum = { acik: false, calisiyor: false, bas: 0, birikmis: 0, turlar: [], gecmis: [] };
const oku = (): Durum => { try { return { ...BOS, ...JSON.parse(localStorage.getItem(KEY) || '{}') }; } catch { return BOS; } };
const yaz = (d: Durum) => { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch { /* özel pencere */ } };
const gecen = (d: Durum, simdi = Date.now()) => d.birikmis + (d.calisiyor ? simdi - d.bas : 0);
export const sureYaz = (ms: number) => {
  const s = Math.floor(ms / 1000), sa = Math.floor(s / 3600), dk = Math.floor((s % 3600) / 60), sn = s % 60;
  const p = (n: number) => String(n).padStart(2, '0');
  return sa ? `${sa}:${p(dk)}:${p(sn)}` : `${p(dk)}:${p(sn)}`;
};
/** Menü ve kenar menüsünden açmak için */
export const kronometreAc = () => window.dispatchEvent(new Event('medsoru:kronometre'));

export default function KronometreV15() {
  const [d, setD0] = useState<Durum>(oku);
  const [panel, setPanel] = useState(false);
  const [, tik] = useState(0);
  const setD = (f: (x: Durum) => Durum) => setD0((x) => { const n = f(x); yaz(n); return n; });

  useEffect(() => {
    const ac = () => { setD((x) => ({ ...x, acik: true })); setPanel(true); };
    const st = (e: StorageEvent) => { if (e.key === KEY) setD0(oku()); };
    window.addEventListener('medsoru:kronometre', ac);
    window.addEventListener('storage', st);
    return () => { window.removeEventListener('medsoru:kronometre', ac); window.removeEventListener('storage', st); };
  }, []);
  useEffect(() => {
    if (!d.calisiyor) return;
    const id = window.setInterval(() => tik((n) => n + 1), 1000);
    return () => window.clearInterval(id);
  }, [d.calisiyor]);
  if (!d.acik) return null;

  const ms = gecen(d);
  const baslat = () => setD((x) => (x.calisiyor ? { ...x, calisiyor: false, birikmis: gecen(x), bas: 0 } : { ...x, calisiyor: true, bas: Date.now() }));
  const tur = () => setD((x) => ({ ...x, turlar: [...x.turlar, gecen(x)].slice(-30) }));
  const bitir = () => setD((x) => {
    const sn = Math.round(gecen(x) / 1000);
    return { ...x, calisiyor: false, bas: 0, birikmis: 0, turlar: [], gecmis: sn ? [{ t: new Date().toISOString(), sn, tur: x.turlar.length }, ...x.gecmis].slice(0, 50) : x.gecmis };
  });
  const gizle = () => { setPanel(false); if (!d.calisiyor && !ms) setD((x) => ({ ...x, acik: false })); };
  const bugun = new Date().toDateString();
  const bugunSn = d.gecmis.filter((g) => new Date(g.t).toDateString() === bugun).reduce((a, g) => a + g.sn, 0);

  return createPortal(
    <div className={`kr15${panel ? ' is-acik' : ''}`} role="region" aria-label="Kronometre">
      {panel ? (
        <div className="kr15-panel v15-card">
          <div className="kr15-ust">
            <span className="v15-label">Kronometre</span>
            <button type="button" className="v15-ib" onClick={gizle} aria-label="Küçült"><X aria-hidden /></button>
          </div>
          <b className="kr15-sure" aria-live="off">{sureYaz(ms)}</b>
          <div className="kr15-dug">
            <button type="button" className="v15-btn" onClick={baslat}>{d.calisiyor ? <><Pause aria-hidden /> Duraklat</> : <><Play aria-hidden /> {ms ? 'Sürdür' : 'Başlat'}</>}</button>
            <button type="button" className="v15-btn is-soft" onClick={tur} disabled={!ms}><Flag aria-hidden /> Tur</button>
            <button type="button" className="v15-btn is-ghost" onClick={bitir} disabled={!ms}><Square aria-hidden /> Bitir</button>
          </div>
          {d.turlar.length > 0 && (
            <ol className="kr15-tur">
              {d.turlar.map((t, i) => <li key={i}><span>Tur {i + 1}</span><span>{sureYaz(t - (d.turlar[i - 1] || 0))}</span><span className="v15-cap">{sureYaz(t)}</span></li>).reverse()}
            </ol>
          )}
          <p className="v15-cap kr15-not">Bugün kronometreyle {sureYaz(bugunSn * 1000)} · sistemin ölçtüğü çalışma süresinden ayrıdır.</p>
        </div>
      ) : (
        <button type="button" className={`kr15-balon${d.calisiyor ? ' is-calisiyor' : ''}`} onClick={() => setPanel(true)} aria-label={`Kronometre ${sureYaz(ms)}, aç`}>
          <Timer aria-hidden />
          <span>{sureYaz(ms)}</span>
        </button>
      )}
    </div>,
    document.body,
  );
}
