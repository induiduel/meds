import React, { useState } from 'react';
import { RotateCcw } from 'lucide-react';
import { FONT_LIST, OKUMA_VARSAYILAN, TEXT_PX_MAX, TEXT_PX_MIN, VURGU_RENKLERI, setAppearance, useAppearance } from '../../utils/appearance';
import { useOkuma } from '../canliDers/CdV15';
import '../../styles/v15/kronometre.css';
import '../../styles/v15/ogren.css';
import '../../styles/v15/ek15.css';

/**
 * v15 · Yazı ve okuma (tasarım K07 yaziAyar) — Profil › Ayarlar › Yazı ve okuma (/ayarlar#yazi).
 * Tek ekranda: canlı önizleme, okuma yazı tipi (FONT_LIST okuma tipleri), kalınlık, hizalama, satır ve harf aralığı,
 * vurgu (işaretleyici) rengi, arayüz ölçeği ve sesli ders okuma ayarları. Görünüm motoru (utils/appearance, cihazda —
 * DEVICE_PREFS) uygular; sesli ders ayarları kendi anahtarlarına yazılır (CdV15.useOkuma, medsoru_canli_ders_tam_yazi).
 */
const CD_YAZI_KEY = 'medsoru_canli_ders_tam_yazi';
const cdYaziOku = () => { try { return Number(localStorage.getItem(CD_YAZI_KEY)) || 20; } catch { return 20; } };

function Seg<T extends string | number>({ ad, deger, secenek, set }: { ad: string; deger: T; secenek: [T, string][]; set: (v: T) => void }) {
  return (
    <div className="ya15-sat">
      <span className="ya15-ad">{ad}</span>
      <div className="v15-seg" role="radiogroup" aria-label={ad}>
        {secenek.map(([v, t]) => <button key={String(v)} type="button" role="radio" aria-checked={deger === v} aria-current={deger === v ? 'page' : undefined} onClick={() => set(v)}>{t}</button>)}
      </div>
    </div>
  );
}
function Kaydir({ ad, deger, min, max, step, goster, set }: { ad: string; deger: number; min: number; max: number; step: number; goster: string; set: (v: number) => void }) {
  return (
    <label className="ya15-sat ya15-kay">
      <span className="ya15-ad">{ad}<small>{goster}</small></span>
      <input type="range" min={min} max={max} step={step} value={deger} onChange={(e) => set(Number(e.target.value))} aria-valuetext={goster} />
    </label>
  );
}

export default function YaziAyarV15() {
  const a = useAppearance();
  const ok = a.okuma || OKUMA_VARSAYILAN;
  const [cd, setCd] = useOkuma();
  const [cdYazi, setCdYazi0] = useState(cdYaziOku);
  const setCdYazi = (n: number) => { const v = Math.min(40, Math.max(14, n)); setCdYazi0(v); try { localStorage.setItem(CD_YAZI_KEY, String(v)); } catch { /* yok */ } };
  const okumaFontlari = FONT_LIST.filter((f) => f.kind === 'read');
  const vr = VURGU_RENKLERI.find((r) => r[0] === ok.vurgu);
  return (
    <div className="ya15">
      <section className="v15-card ya15-on" aria-label="Önizleme">
        <span className="v15-cap">Önizleme</span>
        <p className="ya15-metin" style={{ fontWeight: ok.kalinlik, textAlign: ok.hizala === 'iki' ? 'justify' : 'start', lineHeight: ok.satir, letterSpacing: `${ok.harf}em`, fontFamily: 'var(--font-read)' }}>
          Hücre zedelenmesi geri dönüşlü evrede şişme ve yağlanma ile kendini gösterir. <mark className="ya15-mark" style={vr ? { background: a.mode === 'dark' ? vr[3] : vr[2] } : undefined}>Uyaran sürerse hücre ölümü gelişir</mark>; nekrozda zar bütünlüğü bozulur ve iltihap eşlik eder, apoptozda ise hücre iltihapsız biçimde ortadan kalkar.
        </p>
      </section>

      <section className="v15-card kre-kart ya15-k">
        <h2 className="v15-cap">Okuma yazısı</h2>
        <div className="ya15-sat ya15-font">
          <span className="ya15-ad">Yazı tipi</span>
          <div className="ya15-cipler" role="radiogroup" aria-label="Okuma yazı tipi">
            <button type="button" role="radio" aria-checked={!a.fontRead} className={`o15-cip${!a.fontRead ? ' is-on' : ''}`} onClick={() => setAppearance({ fontRead: undefined })}>Varsayılan</button>
            {okumaFontlari.map((f) => (
              <button key={f.id} type="button" role="radio" aria-checked={a.fontRead === f.id} className={`o15-cip${a.fontRead === f.id ? ' is-on' : ''}`} style={{ fontFamily: f.family }} title={f.hint} onClick={() => setAppearance({ fontRead: f.id })}>{f.name}</button>
            ))}
          </div>
        </div>
        <Seg ad="Kalınlık" deger={ok.kalinlik} secenek={[[400, 'Normal'], [500, 'Orta'], [600, 'Kalın']]} set={(v) => setAppearance({ okuma: { kalinlik: v } })} />
        <Seg ad="Hizalama" deger={ok.hizala} secenek={[['sol', 'Sola'], ['iki', 'İki yana']]} set={(v) => setAppearance({ okuma: { hizala: v } })} />
        <Kaydir ad="Satır aralığı" deger={ok.satir} min={1.3} max={2.2} step={0.05} goster={ok.satir.toFixed(2).replace('.', ',')} set={(v) => setAppearance({ okuma: { satir: v } })} />
        <Kaydir ad="Harf aralığı" deger={ok.harf} min={0} max={0.12} step={0.01} goster={ok.harf ? `+${Math.round(ok.harf * 100)}` : 'Normal'} set={(v) => setAppearance({ okuma: { harf: v } })} />
        <div className="ya15-sat">
          <span className="ya15-ad">Vurgu rengi</span>
          <div className="ya15-renk" role="radiogroup" aria-label="Vurgu (işaretleyici) rengi">
            <button type="button" role="radio" aria-checked={!ok.vurgu} className={`ya15-sw is-tema${!ok.vurgu ? ' is-on' : ''}`} onClick={() => setAppearance({ okuma: { vurgu: undefined } })} aria-label="Tema rengi" title="Tema rengi" />
            {VURGU_RENKLERI.map(([id, ad, acik, koyu]) => (
              <button key={id} type="button" role="radio" aria-checked={ok.vurgu === id} className={`ya15-sw${ok.vurgu === id ? ' is-on' : ''}`} style={{ background: a.mode === 'dark' ? koyu : acik }} onClick={() => setAppearance({ okuma: { vurgu: id } })} aria-label={ad} title={ad} />
            ))}
          </div>
        </div>
        {a.okuma && <button type="button" className="v15-btn is-ghost ya15-sifir" onClick={() => setAppearance({ okuma: null })}><RotateCcw aria-hidden /> Okuma ayarlarını sıfırla</button>}
      </section>

      <section className="v15-card kre-kart ya15-k">
        <h2 className="v15-cap">Arayüz</h2>
        <Kaydir ad="Yazı ve arayüz ölçeği" deger={a.textPx} min={TEXT_PX_MIN} max={TEXT_PX_MAX} step={1} goster={`${a.textPx} px`} set={(v) => setAppearance({ textPx: v })} />
      </section>

      <section className="v15-card kre-kart ya15-k">
        <h2 className="v15-cap">Sesli ders</h2>
        <Kaydir ad="Metin boyutu" deger={cdYazi} min={14} max={40} step={2} goster={`${cdYazi - 2} px`} set={setCdYazi} />
        <Seg ad="Satır aralığı" deger={cd.satir} secenek={[['siki', 'Sıkı'], ['normal', 'Normal'], ['genis', 'Geniş']]} set={(v) => setCd({ satir: v })} />
        <Seg ad="Zemin" deger={cd.zemin} secenek={[['varsayilan', 'Tema'], ['krem', 'Krem'], ['gri', 'Gri'], ['gece', 'Gece']]} set={(v) => setCd({ zemin: v })} />
        <p className="kre-not">Sesli ders ekranındaki Görünüm menüsünden de değiştirebilirsin; metin boyutu bir sonraki açılışta uygulanır.</p>
      </section>
      <p className="kre-not">Bu ayarlar bu cihazda saklanır.</p>
    </div>
  );
}
