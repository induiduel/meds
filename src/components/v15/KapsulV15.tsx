import React, { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { Coffee, Pause, Play, Square, Target, X } from 'lucide-react';
import { sureYaz } from './KronometreV15';
import '../../styles/v15/kronometre.css';

/**
 * v15 · Çalışma kapsülü (tasarım sistemi v15 › U). Hedef süreli odak oturumu: süre (25/50/90 dk ya da serbest) ve konu
 * seçilir, geri sayım yüzen baloncukta sürer, bitince kısa mola önerilir. Geçmiş ve günlük toplam cihazda
 * (`medsoru_v15_kapsul_v1`, userKvSync ile hesaba eşitlenir); sistemin ölçtüğü çalışma süresine (calismaTakip) yazmaz.
 * Kronometre panelinden ve Menü › Araçlar › Odak'tan açılır (`medsoru:kapsul` olayı).
 */
const KEY = 'medsoru_v15_kapsul_v1';
interface Oturum { hedefDk: number; konu: string; bas: number; birikmis: number; calisiyor: boolean }
interface Kayit { t: string; konu: string; hedefDk: number; sn: number; tamam: boolean }
interface Durum { acik: boolean; oturum: Oturum | null; molaBitis: number; gecmis: Kayit[] }
const BOS: Durum = { acik: false, oturum: null, molaBitis: 0, gecmis: [] };
const oku = (): Durum => { try { return { ...BOS, ...JSON.parse(localStorage.getItem(KEY) || '{}') }; } catch { return BOS; } };
const yaz = (d: Durum) => { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch { /* özel pencere */ } };
const gecen = (o: Oturum, simdi = Date.now()) => o.birikmis + (o.calisiyor ? simdi - o.bas : 0);
const SURELER = [25, 50, 90];
const molaDk = (dk: number) => (dk >= 90 ? 15 : dk >= 50 ? 10 : 5);

/** Odak artık kronometre panelinin sekmesi: tek yüzen sayaç (tasarım T/U, çift sayaç yok) */
export const kapsulAc = () => window.dispatchEvent(new CustomEvent('medsoru:kronometre', { detail: 'odak' }));
/** Kronometre baloncuğunun okuduğu odak durumu */
export const kapsulOku = () => { const d = oku(); const o = d.oturum; return o ? { kalan: Math.max(0, o.hedefDk * 60000 - gecen(o)), oran: Math.min(1, gecen(o) / (o.hedefDk * 60000)), calisiyor: o.calisiyor } : null; };
export const KAPSUL_KEY = KEY;

export default function KapsulV15({ gomulu = false }: { gomulu?: boolean }) {
  const [d, setD0] = useState<Durum>(oku);
  const [panel, setPanel] = useState(false);
  const [hedef, setHedef] = useState(25);
  const [serbest, setSerbest] = useState('');
  const [konu, setKonu] = useState('');
  const [bitti, setBitti] = useState<Kayit | null>(null);
  const [, tik] = useState(0);
  const setD = (f: (x: Durum) => Durum) => setD0((x) => { const n = f(x); yaz(n); return n; });

  useEffect(() => {
    const st = (e: StorageEvent) => { if (e.key === KEY) setD0(oku()); };
    // kronometre başlayınca odak duraklar (aynı anda tek sayaç)
    const sayac = (e: Event) => { if ((e as CustomEvent).detail === 'kronometre') setD((x) => x.oturum?.calisiyor ? { ...x, oturum: { ...x.oturum, calisiyor: false, birikmis: gecen(x.oturum), bas: 0 } } : x); };
    window.addEventListener('medsoru:sayac', sayac);
    window.addEventListener('storage', st);
    return () => { window.removeEventListener('medsoru:sayac', sayac); window.removeEventListener('storage', st); };
  }, []);
  const sayiyor = !!d.oturum?.calisiyor || d.molaBitis > Date.now();
  useEffect(() => {
    if (!sayiyor) return;
    const id = window.setInterval(() => tik((n) => n + 1), 1000);
    return () => window.clearInterval(id);
  }, [sayiyor]);

  const bitir = (tamam: boolean) => setD((x) => {
    if (!x.oturum) return x;
    const sn = Math.round(Math.min(gecen(x.oturum), x.oturum.hedefDk * 60000) / 1000);
    const k: Kayit = { t: new Date().toISOString(), konu: x.oturum.konu, hedefDk: x.oturum.hedefDk, sn, tamam };
    setBitti(k); setPanel(true);
    return { ...x, oturum: null, gecmis: sn >= 30 ? [k, ...x.gecmis].slice(0, 100) : x.gecmis };
  });
  // Hedefe ulaşınca kendiliğinden biter
  const o = d.oturum;
  const ms = o ? gecen(o) : 0;
  const hedefMs = o ? o.hedefDk * 60000 : 0;
  useEffect(() => { if (o && hedefMs && ms >= hedefMs) bitir(true); });

  if (!gomulu) return null;

  const baslat = () => {
    const dk = serbest ? Math.max(1, Math.min(240, Math.round(Number(serbest) || 0))) : hedef;
    setBitti(null);
    window.dispatchEvent(new CustomEvent('medsoru:sayac', { detail: 'odak' }));
    setD((x) => ({ ...x, molaBitis: 0, oturum: { hedefDk: dk, konu: konu.trim() || 'Serbest çalışma', bas: Date.now(), birikmis: 0, calisiyor: true } }));
  };
  const duraklat = () => { if (!d.oturum?.calisiyor) window.dispatchEvent(new CustomEvent('medsoru:sayac', { detail: 'odak' })); setD((x) => x.oturum ? { ...x, oturum: x.oturum.calisiyor
    ? { ...x.oturum, calisiyor: false, birikmis: gecen(x.oturum), bas: 0 } : { ...x.oturum, calisiyor: true, bas: Date.now() } } : x); };
  const mola = (dk: number) => { setBitti(null); setD((x) => ({ ...x, molaBitis: Date.now() + dk * 60000 })); };
  const kapat = () => { setPanel(false); if (!d.oturum && d.molaBitis <= Date.now()) { setBitti(null); setD((x) => ({ ...x, acik: false, molaBitis: 0 })); } };

  const bugun = new Date().toDateString();
  const bugunKayit = d.gecmis.filter((g) => new Date(g.t).toDateString() === bugun);
  const bugunSn = bugunKayit.reduce((a, g) => a + g.sn, 0);
  const sonKonular = [...new Set(d.gecmis.map((g) => g.konu).filter((k) => k !== 'Serbest çalışma'))].slice(0, 4);
  const molaKalan = Math.max(0, d.molaBitis - Date.now());
  const kalan = Math.max(0, hedefMs - ms);
  const yuzde = hedefMs ? Math.min(100, (ms / hedefMs) * 100) : 0;

  return (
    <div className="kp15-ic">
          {o ? (
            <>
              <span className="kp15-konu">{o.konu}</span>
              <b className="kr15-sure">{sureYaz(kalan)}</b>
              <div className="kp15-bar" aria-hidden><i style={{ width: `${yuzde}%` }} /></div>
              <span className="v15-cap kp15-orta">{o.hedefDk} dk hedef · {sureYaz(ms)} geçti</span>
              <div className="kr15-dug">
                <button type="button" className="v15-btn" onClick={duraklat}>{o.calisiyor ? <><Pause aria-hidden /> Duraklat</> : <><Play aria-hidden /> Sürdür</>}</button>
                <button type="button" className="v15-btn is-ghost" onClick={() => bitir(false)}><Square aria-hidden /> Bitir</button>
              </div>
            </>
          ) : molaKalan > 0 ? (
            <>
              <span className="kp15-konu"><Coffee aria-hidden /> Mola</span>
              <b className="kr15-sure">{sureYaz(molaKalan)}</b>
              <span className="v15-cap kp15-orta">Kalk, su iç, gözlerini dinlendir.</span>
              <button type="button" className="v15-btn" onClick={() => setD((x) => ({ ...x, molaBitis: 0 }))}>Molayı bitir</button>
            </>
          ) : (
            <>
              {bitti && (
                <div className="kp15-bitti">
                  <b>{bitti.tamam ? 'Oturum tamamlandı' : 'Oturum bitti'}: {sureYaz(bitti.sn * 1000)}</b>
                  <span className="v15-cap">{bitti.konu} · kısa bir mola iyi gelir.</span>
                  <button type="button" className="v15-btn is-soft" onClick={() => mola(molaDk(bitti.hedefDk))}><Coffee aria-hidden /> {molaDk(bitti.hedefDk)} dk mola</button>
                </div>
              )}
              <span className="v15-cap">Hedef süre</span>
              <div className="kp15-secim" role="group" aria-label="Hedef süre">
                {SURELER.map((s) => (
                  <button key={s} type="button" className={`v15-btn is-soft${!serbest && hedef === s ? ' is-on' : ''}`} aria-pressed={!serbest && hedef === s}
                    onClick={() => { setHedef(s); setSerbest(''); }}>{s} dk</button>
                ))}
                <input className="kp15-girdi" inputMode="numeric" placeholder="Serbest" aria-label="Serbest süre (dakika)" value={serbest}
                  onChange={(e) => setSerbest(e.target.value.replace(/\D/g, '').slice(0, 3))} />
              </div>
              <input className="kp15-girdi kp15-konu-gir" placeholder="Ne çalışacaksın?" aria-label="Ne çalışacaksın" value={konu} maxLength={80}
                onChange={(e) => setKonu(e.target.value)} onKeyDown={(e) => { if (e.key === 'Enter') baslat(); }} />
              {sonKonular.length > 0 && (
                <div className="kp15-oneri">{sonKonular.map((k) => <button key={k} type="button" className="kp15-hap" onClick={() => setKonu(k)}>{k}</button>)}</div>
              )}
              <button type="button" className="v15-btn" onClick={baslat}><Play aria-hidden /> Odaklan</button>
            </>
          )}
          {bugunKayit.length > 0 && (
            <ol className="kr15-tur">
              {bugunKayit.slice(0, 8).map((g) => (
                <li key={g.t}><span>{g.konu}</span><span>{sureYaz(g.sn * 1000)}</span><span className="v15-cap">{new Date(g.t).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })}</span></li>
              ))}
            </ol>
          )}
          <p className="v15-cap kr15-not">Bugün {bugunKayit.length} oturum, toplam {sureYaz(bugunSn * 1000)} · sistemin ölçtüğü çalışma süresinden ayrıdır.</p>
    </div>
  );
}
