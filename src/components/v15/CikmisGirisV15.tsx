import React, { useState } from 'react';
import '../../styles/v15/cikmis.css';

/**
 * v15 · Çıkmışlar gruplaması (docs/tasarim/cikmis-alternatifler.html). Eski 12 büyük yıl kartı (C07 ızgarası) yerine:
 *  - YilSerit: tek satır yatay kayan yıl/konu çipleri (A · Liste, C · Tablo, D · Odak modlarında yapışkan çubukta).
 *  - YilPaneli: yıl/konu listesi + ilerleme çubukları (B · Panel modunda solda kalıcı, dar ekranda alt sayfa).
 * Veri çıkmış sayfasının kendi listesinden (PastExamsView prepared + çözüm kayıtları); seçim yıl/ders süzgecini kurar.
 */
export interface CikmisGrup { ad: string; toplam: number; cozulen: number; dogru: number; yeni: number }
export type GrupKip = 'yil' | 'ders';

interface Ortak {
  yillar: CikmisGrup[];
  dersler: CikmisGrup[];
  seciliYil: string;
  seciliDers: string;
  onYil: (y: string) => void;
  onDers: (d: string) => void;
}

const adGoster = (kip: GrupKip, ad: string) => (kip === 'yil' && ad === 'Kategorisiz' ? 'Yılı belirsiz' : ad.replace(/^Tıbbi\s+/, ''));
const tr = (v: number) => v.toLocaleString('tr-TR');

function useKip(): [GrupKip, (k: GrupKip) => void] {
  return useState<GrupKip>('yil');
}

const KipSecici: React.FC<{ kip: GrupKip; set: (k: GrupKip) => void; kisa?: boolean }> = ({ kip, set, kisa }) => (
  <div className="cg15-kip" role="tablist" aria-label="Gruplama">
    <button type="button" role="tab" aria-selected={kip === 'yil'} className={kip === 'yil' ? 'is-on' : ''} onClick={() => set('yil')}>{kisa ? 'Yıl' : 'Yıla göre'}</button>
    <button type="button" role="tab" aria-selected={kip === 'ders'} className={kip === 'ders' ? 'is-on' : ''} onClick={() => set('ders')}>{kisa ? 'Konu' : 'Konuya göre'}</button>
  </div>
);

/** A/C/D: yatay kayan çip şeridi (yıl · soru sayısı · yeni rozeti) */
export function YilSerit({ yillar, dersler, seciliYil, seciliDers, onYil, onDers }: Ortak) {
  const [kip, setKip] = useKip();
  const liste = kip === 'yil' ? yillar : dersler;
  if (!yillar.length && !dersler.length) return null;
  const secili = kip === 'yil' ? seciliYil : seciliDers;
  const sec = (ad: string) => (kip === 'yil' ? onYil(ad) : onDers(ad));
  const toplam = liste.reduce((s, g) => s + g.toplam, 0);
  return (
    <div className="cg15-serit" aria-label="Yıla ya da konuya göre süz">
      <KipSecici kip={kip} set={setKip} kisa />
      <div className="cg15-cipler" role="listbox" aria-label={kip === 'yil' ? 'Yıllar' : 'Konular'}>
        <button type="button" role="option" aria-selected={secili === 'all'} className={`cg15-cip ${secili === 'all' ? 'is-on' : ''}`} onClick={() => sec('all')}>
          Tümü <b>{tr(toplam)}</b>
        </button>
        {liste.map((g) => (
          <button key={g.ad} type="button" role="option" aria-selected={secili === g.ad} className={`cg15-cip ${secili === g.ad ? 'is-on' : ''}`}
            onClick={() => sec(secili === g.ad ? 'all' : g.ad)} title={`${adGoster(kip, g.ad)}: ${g.toplam} soru, ${g.cozulen} çözüldü`}>
            {adGoster(kip, g.ad)} <b>{tr(g.toplam)}</b>
            {g.yeni > 0 && <i className="cg15-yeni" aria-label={`${g.yeni} yeni`}>yeni</i>}
          </button>
        ))}
      </div>
    </div>
  );
}

/** B: yan panel (yıl/konu listesi + ilerleme çubuğu) */
export function YilPaneli({ yillar, dersler, seciliYil, seciliDers, onYil, onDers, onSecildi }: Ortak & { onSecildi?: () => void }) {
  const [kip, setKip] = useKip();
  const liste = kip === 'yil' ? yillar : dersler;
  const secili = kip === 'yil' ? seciliYil : seciliDers;
  const sec = (ad: string) => { (kip === 'yil' ? onYil : onDers)(ad); onSecildi?.(); };
  const toplam = liste.reduce((s, g) => s + g.toplam, 0);
  const cozulen = liste.reduce((s, g) => s + g.cozulen, 0);
  const Oge = ({ ad, ust, g }: { ad: string; ust: string; g: { toplam: number; cozulen: number; yeni?: number } }) => {
    const pct = g.toplam ? Math.round((g.cozulen / g.toplam) * 100) : 0;
    return (
      <button type="button" className={`cg15-po ${secili === ad ? 'is-on' : ''}`} aria-pressed={secili === ad} onClick={() => sec(ad)}>
        <span className="cg15-po-s">
          <span className="cg15-po-a">{ust}{g.yeni ? <i className="cg15-yeni">yeni</i> : null}</span>
          <small>{tr(g.cozulen)}/{tr(g.toplam)}</small>
        </span>
        <span className="cg15-po-bar" aria-hidden><span style={{ width: `${pct}%` }} /></span>
      </button>
    );
  };
  return (
    <nav className="cg15-panel" aria-label="Yıl ve konu">
      <KipSecici kip={kip} set={setKip} />
      <div className="cg15-po-liste">
        <Oge ad="all" ust="Tümü" g={{ toplam, cozulen }} />
        {liste.map((g) => <Oge key={g.ad} ad={g.ad} ust={adGoster(kip, g.ad)} g={g} />)}
      </div>
    </nav>
  );
}
