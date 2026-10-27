import React, { useMemo, useState } from 'react';
import { MODUL_AD, sureYaz, useTakip, type TakipModul } from '../../services/calismaTakip';
import '../../styles/v15/grafik.css';

/**
 * v15 · Çalışma grafikleri (tasarım sistemi v15 › X "İstatistik"). İstatistiklerim sayfasının tepesinde.
 * Veri yalnız çalışma takibinden (services/calismaTakip: modül → gün → saniye, konu kayıtları); uydurma sayı yok.
 * Tek ölçü (süre) tek eksen; tek renk (vurgu). Modül dağılımı yatay çubuk + doğrudan etiket, renkle kimlik yok.
 */
const GUN = 86_400_000;
const anahtar = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
const dk = (sn: number) => Math.round(sn / 60);

/** aralik: sayfanın dönem seçiminden (7 gün · 30 gün); ayrı seçici yok */
export default function CalismaGrafikleriV15({ aralik }: { aralik: 7 | 30 }) {
  const takip = useTakip();
  const [uzerinde, setUzerinde] = useState<number | null>(null);

  const v = useMemo(() => {
    const gunluk: Record<string, number> = {};
    const modul: Partial<Record<TakipModul, number>> = {};
    for (const [m, g] of Object.entries(takip.g) as [TakipModul, Record<string, number>][]) {
      for (const [d, sn] of Object.entries(g || {})) { gunluk[d] = (gunluk[d] || 0) + sn; }
    }
    const simdi = new Date();
    const gunler = Array.from({ length: aralik }, (_, i) => {
      const t = new Date(simdi.getTime() - (aralik - 1 - i) * GUN);
      const d = anahtar(t);
      return { d, t, sn: gunluk[d] || 0 };
    });
    const ilk = gunler[0].d;
    for (const [m, g] of Object.entries(takip.g) as [TakipModul, Record<string, number>][]) {
      for (const [d, sn] of Object.entries(g || {})) if (d >= ilk) modul[m] = (modul[m] || 0) + sn;
    }
    // seri: bugünden geriye en az 10 dk çalışılan ardışık günler (bugün henüz çalışılmadıysa dünden başlar)
    let seri = 0;
    for (let i = 0; i < 120; i++) {
      const sn = gunluk[anahtar(new Date(simdi.getTime() - i * GUN))] || 0;
      if (sn >= 600) seri++;
      else if (i > 0) break;
    }
    const toplam = gunler.reduce((a, g) => a + g.sn, 0);
    const aktif = gunler.filter((g) => g.sn >= 120).length;
    const konular = Object.values(takip.k);
    const biten = konular.filter((k) => k.durum === 'bitti' && k.bittiAt && k.bittiAt.slice(0, 10) >= ilk).length;
    const soru = konular.reduce((a, k) => a + (k.sonAt && k.sonAt.slice(0, 10) >= ilk ? k.soru || 0 : 0), 0);
    return { gunler, modul, seri, toplam, aktif, biten, soru, enCok: Math.max(1, ...gunler.map((g) => g.sn)) };
  }, [takip, aralik]);

  const modSira = (Object.entries(v.modul) as [TakipModul, number][]).filter(([, s]) => s >= 60).sort((a, b) => b[1] - a[1]);
  const modEnCok = Math.max(1, ...modSira.map(([, s]) => s));
  const bos = v.toplam < 60;
  // y ekseni: 30 dk'nın katlarına yuvarlanmış tavan
  const tavanDk = Math.max(30, Math.ceil(dk(v.enCok) / 30) * 30);
  const sec = uzerinde != null ? v.gunler[uzerinde] : null;

  return (
    <section className="gf15" aria-label="Çalışma grafikleri">
      <div className="gf15-ust">
        <h2>Çalışman</h2>
      </div>

      <div className="gf15-kpi">
        <div className="v15-card"><small>Toplam</small><b>{sureYaz(v.toplam) || '0 dk'}</b></div>
        <div className="v15-card"><small>Aktif gün ort.</small><b>{v.aktif ? sureYaz(v.toplam / v.aktif) : '—'}</b></div>
        <div className="v15-card"><small>Seri</small><b>{v.seri} gün</b></div>
        <div className="v15-card"><small>Biten konu</small><b>{v.biten}</b></div>
      </div>

      <div className="v15-card gf15-kart">
        <div className="gf15-kb">
          <b>Günlük çalışma süresi</b>
          <span className="v15-cap" aria-live="polite">
            {sec ? `${sec.t.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', weekday: 'short' })}: ${sec.sn ? sureYaz(sec.sn) : 'çalışma yok'}` : `Son ${aralik} gün · dakika`}
          </span>
        </div>
        {bos ? (
          <p className="gf15-bos">Bu aralıkta kayıtlı çalışma yok. Sesli ders, soru çözücü ya da etkileşimli derslerde geçen süre burada görünür.</p>
        ) : (
          <div className="gf15-grafik" onMouseLeave={() => setUzerinde(null)}>
            <div className="gf15-y" aria-hidden>
              <span>{tavanDk}</span><span>{tavanDk / 2}</span><span>0</span>
            </div>
            <div className="gf15-cubuklar" role="img" aria-label={`Son ${aralik} günde toplam ${sureYaz(v.toplam)} çalışma`}>
              <span className="gf15-cizgi" style={{ bottom: '50%' }} aria-hidden />
              {v.gunler.map((g, i) => {
                const h = (dk(g.sn) / tavanDk) * 100;
                const bugun = i === v.gunler.length - 1;
                return (
                  <button key={g.d} type="button" className={`gf15-c${uzerinde === i ? ' is-on' : ''}${bugun ? ' is-bugun' : ''}`}
                    onMouseEnter={() => setUzerinde(i)} onFocus={() => setUzerinde(i)} onClick={() => setUzerinde(uzerinde === i ? null : i)}
                    aria-label={`${g.t.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long' })}: ${g.sn ? sureYaz(g.sn) : 'çalışma yok'}`}>
                    <span style={{ height: g.sn ? `max(3px, ${h}%)` : 0 }} />
                  </button>
                );
              })}
            </div>
            <div className="gf15-x" aria-hidden>
              {v.gunler.map((g, i) => (
                <span key={g.d}>{(aralik === 7 || i % 5 === 4) || i === v.gunler.length - 1 ? g.t.getDate() : ''}</span>
              ))}
            </div>
          </div>
        )}
      </div>

      {!bos && (
        <div className="v15-card gf15-kart">
          <div className="gf15-kb"><b>Nerede çalıştın?</b><span className="v15-cap">Son {aralik} gün</span></div>
          <ul className="gf15-mod">
            {modSira.map(([m, s]) => (
              <li key={m}>
                <span className="gf15-mod-ad">{MODUL_AD[m]}</span>
                <span className="gf15-mod-bar" aria-hidden><span style={{ width: `${(s / modEnCok) * 100}%` }} /></span>
                <span className="gf15-mod-n">{sureYaz(s)} <small>%{Math.round((s / v.toplam) * 100)}</small></span>
              </li>
            ))}
          </ul>
          {v.soru > 0 && <p className="v15-cap gf15-not">Bu aralıkta çalıştığın konularda {v.soru} soru çözdün.</p>}
        </div>
      )}
    </section>
  );
}
