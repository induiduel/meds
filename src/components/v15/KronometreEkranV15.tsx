import React, { useState } from 'react';
import { ChevronLeft } from 'lucide-react';
import { takipOku } from '../../services/calismaTakip';

/**
 * v15 · Kronometre ayarları ve geçmişi (tasarım T › kronoAyar, kronoGecmis). Kronometre panelinden açılan tam ekran
 * görünüm. Ayarlar cihazda (`medsoru_v15_kronometre_ayar`); geçmiş kronometre kayıtları ile sistemin ölçtüğü çalışma
 * süresini (calismaTakip günlük toplamları) yan yana gösterir — ikisi birbirine karışmaz.
 */
export type KrBicim = 'zar' | 'nokta' | 'hap' | 'kenar' | 'cip' | 'cizgi';
export interface KrAyar { bicim: KrBicim; goster: boolean; birles: boolean; devam: boolean; boyut: 'kucuk' | 'orta'; sag: boolean; molaDk: number; hedefDk: number }
export const KR_AYAR_KEY = 'medsoru_v15_kronometre_ayar';
export const AYAR_VARSAYILAN: KrAyar = { bicim: 'zar', goster: true, birles: true, devam: true, boyut: 'orta', sag: true, molaDk: 50, hedefDk: 120 };
export const ayarOku = (): KrAyar => { try { return { ...AYAR_VARSAYILAN, ...JSON.parse(localStorage.getItem(KR_AYAR_KEY) || '{}') }; } catch { return AYAR_VARSAYILAN; } };
export interface KrKayit { t: string; sn: number; tur: number; ad?: string }

const gunAnahtari = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const dkYaz = (sn: number) => { const dk = Math.round(sn / 60), sa = Math.floor(dk / 60); return sa ? `${sa} sa ${dk % 60} dk` : `${dk} dk`; };

function Anahtar({ acik, onDegis, etiket }: { acik: boolean; onDegis: (v: boolean) => void; etiket: string }) {
  return (
    <label className="kre-sat">
      <span>{etiket}</span>
      <button type="button" role="switch" aria-checked={acik} aria-label={etiket} className={`kre-tgl${acik ? ' is-on' : ''}`} onClick={() => onDegis(!acik)}><i /></button>
    </label>
  );
}
function Secim<T extends string | number>({ etiket, deger, secenek, onDegis }: { etiket: string; deger: T; secenek: [T, string][]; onDegis: (v: T) => void }) {
  return (
    <div className="kre-sat is-sec">
      <span>{etiket}</span>
      <div className="v15-seg kre-seg" role="group" aria-label={etiket}>
        {secenek.map(([v, ad]) => (
          <button key={String(v)} type="button" aria-pressed={deger === v} aria-current={deger === v ? 'page' : undefined} onClick={() => onDegis(v)}>{ad}</button>
        ))}
      </div>
    </div>
  );
}

/** Tasarım kronoFormlar: varsayılan zar + F1–F5 */
const BICIMLER: [KrBicim, string, string][] = [
  ['zar', 'Zar', 'Varsayılan yüzen baloncuk; süre ve ilerleme halkası.'],
  ['nokta', 'F1 · Nokta', '22 px halka; süre yalnız dokununca baloncukta görünür.'],
  ['hap', 'F2 · Hap', 'Süreli küçük hap; kenarı nefes alır.'],
  ['kenar', 'F3 · Kenar sekmesi', 'Ekran kenarına yapışık yarım kapsül; içeriği kapatmaz.'],
  ['cip', 'F4 · Başlık çipi', 'Üstte küçük çip; yüzmez, yer kaplamaz.'],
  ['cizgi', 'F5 · İnce çizgi', 'Ekran tepesinde 2 px ilerleme çizgisi + küçük süre.'],
];
function BicimSec({ deger, onDegis }: { deger: KrBicim; onDegis: (v: KrBicim) => void }) {
  return (
    <div className="kre-bicim" role="radiogroup" aria-label="Kronometre biçimi">
      <span className="kre-bicim-b">Biçim</span>
      <div className="kre-bicim-g">
        {BICIMLER.map(([v, ad, ac]) => (
          <button key={v} type="button" role="radio" aria-checked={deger === v} className={`kre-bk${deger === v ? ' is-on' : ''}`} onClick={() => onDegis(v)}>
            <span className={`kre-bk-o is-${v}`} aria-hidden>
              {v === 'zar' ? <i className="o-zar">12:48</i> : v === 'nokta' ? <i className="o-nokta" /> : v === 'hap' ? <i className="o-hap"><b />12:48</i>
                : v === 'kenar' ? <i className="o-kenar"><b />12<br />48</i> : v === 'cip' ? <i className="o-cip"><b />12:48</i> : <i className="o-cizgi"><b /><em>12:48</em></i>}
            </span>
            <b>{ad}</b><small>{ac}</small>
          </button>
        ))}
      </div>
    </div>
  );
}

export default function KronometreEkranV15({ gorunum, ayar, setAyar, gecmis, onKapat }: {
  gorunum: 'ayar' | 'gecmis'; ayar: KrAyar; setAyar: (a: KrAyar) => void; gecmis: KrKayit[]; onKapat: () => void;
}) {
  const [aralik, setAralik] = useState<7 | 30>(7);
  React.useEffect(() => { document.documentElement.classList.add('tam-katman'); return () => document.documentElement.classList.remove('tam-katman'); }, []);
  const ay = (k: Partial<KrAyar>) => setAyar({ ...ayar, ...k });

  let govde: React.ReactNode;
  if (gorunum === 'ayar') {
    govde = (
      <div className="kre-cols">
        <section className="v15-card kre-kart">
          <BicimSec deger={ayar.bicim} onDegis={(v) => ay({ bicim: v })} />
          <Anahtar etiket="Yüzen kronometreyi göster" acik={ayar.goster} onDegis={(v) => ay({ goster: v })} />
          <Anahtar etiket="Medya açıkken oynatıcıyla birleş" acik={ayar.birles} onDegis={(v) => ay({ birles: v })} />
          <Anahtar etiket="Sayfa değişince çalışmaya devam et" acik={ayar.devam} onDegis={(v) => ay({ devam: v })} />
          <Secim etiket="Boyut" deger={ayar.boyut} secenek={[['kucuk', 'Küçük'], ['orta', 'Orta']]} onDegis={(v) => ay({ boyut: v })} />
          <Secim etiket="Başlangıç konumu" deger={ayar.sag ? 1 : 0} secenek={[[0, 'Sol alt'], [1, 'Sağ alt']]} onDegis={(v) => ay({ sag: v === 1 })} />
        </section>
        <section className="v15-card kre-kart">
          <Secim etiket="Mola hatırlatması" deger={ayar.molaDk} secenek={[[0, 'Kapalı'], [25, '25 dk'], [50, '50 dk'], [90, '90 dk']]} onDegis={(v) => ay({ molaDk: v })} />
          <Secim etiket="Hedef süre (gün)" deger={ayar.hedefDk} secenek={[[60, '1 sa'], [120, '2 sa'], [180, '3 sa'], [240, '4 sa']]} onDegis={(v) => ay({ hedefDk: v })} />
          <p className="kre-not">Bu sayaç yalnız senin elinle açıp kapattığın süreyi tutar. Sistemin arka planda ölçtüğü çalışma süresine (sayfa görünür + etkileşim) karışmaz ve glukoz hesabına girmez.</p>
        </section>
      </div>
    );
  } else {
    const takip = takipOku();
    const gunler = Array.from({ length: aralik }, (_, i) => { const d = new Date(); d.setDate(d.getDate() - (aralik - 1 - i)); return d; });
    const kr: Record<string, number> = {};
    gecmis.forEach((g) => { const k = gunAnahtari(new Date(g.t)); kr[k] = (kr[k] || 0) + g.sn; });
    const sis = (k: string) => Object.values(takip.g || {}).reduce((a, m) => a + ((m as Record<string, number>)?.[k] || 0), 0);
    const veri = gunler.map((d) => { const k = gunAnahtari(d); return { d, kr: kr[k] || 0, sis: sis(k) }; });
    const krTop = veri.reduce((a, v) => a + v.kr, 0), sisTop = veri.reduce((a, v) => a + v.sis, 0);
    const tavan = Math.max(ayar.hedefDk * 60, ...veri.map((v) => Math.max(v.kr, v.sis)), 1);
    const sinir = gunler[0].getTime() - 86400_000;
    const oturumlar = gecmis.filter((g) => new Date(g.t).getTime() > sinir).slice(0, 30);
    const bugunK = gunAnahtari(new Date());
    govde = (
      <>
        <div className="v15-seg" role="tablist" aria-label="Aralık">
          <button type="button" role="tab" aria-selected={aralik === 7} aria-current={aralik === 7 ? 'page' : undefined} onClick={() => setAralik(7)}>Hafta</button>
          <button type="button" role="tab" aria-selected={aralik === 30} aria-current={aralik === 30 ? 'page' : undefined} onClick={() => setAralik(30)}>Ay</button>
        </div>
        <div className="kre-stat">
          <div className="v15-card"><b>{dkYaz(krTop)}</b><span>Kronometre</span></div>
          <div className="v15-card"><b>{dkYaz(sisTop)}</b><span>Sistem süresi</span></div>
          <div className="v15-card"><b>{sisTop ? `%${Math.min(100, Math.round((krTop / sisTop) * 100))}` : '—'}</b><span>Odak oranı</span></div>
        </div>
        <section className="v15-card kre-kart">
          <div className="kre-bas"><b>Gün gün</b><span className="kre-lej"><i className="is-kr" /> Kronometre <i className="is-sis" /> Sistem</span></div>
          <div className={`kre-bar${aralik === 30 ? ' is-ay' : ''}`} role="img" aria-label={`Son ${aralik} gün: kronometre ${dkYaz(krTop)}, sistem ${dkYaz(sisTop)}`}>
            <span className="kre-hedef" style={{ bottom: `${(ayar.hedefDk * 60 / tavan) * 100}%` }} title={`Hedef ${dkYaz(ayar.hedefDk * 60)}`} />
            {veri.map((v) => (
              <div key={v.d.toISOString()} className="kre-gun" title={`${v.d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' })}: ${dkYaz(v.kr)} / ${dkYaz(v.sis)}`}>
                <i className="is-kr" style={{ height: `${(v.kr / tavan) * 100}%` }} />
                <i className="is-sis" style={{ height: `${(v.sis / tavan) * 100}%` }} />
              </div>
            ))}
          </div>
          <div className={`kre-eks${aralik === 30 ? ' is-ay' : ''}`}>
            {veri.map((v, i) => <span key={i}>{aralik === 7 ? v.d.toLocaleDateString('tr-TR', { weekday: 'short' }) : i % 5 === 0 ? v.d.getDate() : ''}</span>)}
          </div>
          <p className="kre-not">Çizgi günlük hedefin ({dkYaz(ayar.hedefDk * 60)}). Bugün kronometre {dkYaz(kr[bugunK] || 0)}.</p>
        </section>
        <h2 className="v15-cap kre-h">Oturumlar</h2>
        {oturumlar.length ? (
          <ul className="v15-card kre-liste" role="list">
            {oturumlar.map((g) => {
              const d = new Date(g.t);
              const gun = gunAnahtari(d) === bugunK ? 'bugün' : d.toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' });
              return (
                <li key={g.t}>
                  <span className="kre-li-t"><b>{g.ad || 'Kronometre'}</b><span>{dkYaz(g.sn)}{g.tur ? ` · ${g.tur} tur` : ''}</span></span>
                  <span className="kre-li-z">{gun} {d.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })}</span>
                </li>
              );
            })}
          </ul>
        ) : <p className="v15-card kre-bos">Bu aralıkta kayıtlı kronometre oturumu yok. Kronometreyi sıfırladığında ya da kapattığında oturum buraya yazılır.</p>}
      </>
    );
  }

  return (
    <div className="kre" role="dialog" aria-modal="true" aria-label={gorunum === 'ayar' ? 'Kronometre ayarları' : 'Kronometre geçmişi'}>
      <header className="kre-ust">
        <button type="button" className="v15-ib" onClick={onKapat} aria-label="Geri"><ChevronLeft aria-hidden /></button>
        <div><b>{gorunum === 'ayar' ? 'Kronometre' : 'Kronometre geçmişi'}</b>{gorunum === 'ayar' && <span>Ayarlar</span>}</div>
      </header>
      <div className="kre-ic">{govde}</div>
    </div>
  );
}
