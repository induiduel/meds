import React, { useMemo, useState } from 'react';
import { BarChart3, ChevronDown, Clock } from 'lucide-react';
import { fmtSaat, type SpotBransSureGrup } from './spotsSureVeri';
import { type Brans } from '../brans';
import '../../../styles/spots-sure.css';

interface Props {
  baslik: string;
  gruplar: SpotBransSureGrup[];
  seciliBrans?: Brans | 'tum';
  onSecBrans?: (b: Brans | 'tum') => void;
  onTamListe: () => void;
  birimAd?: 'ders' | 'set';
  tercihKey: string;
}

export const SpotsSureOzeti: React.FC<Props> = ({
  baslik,
  gruplar,
  seciliBrans = 'tum',
  onSecBrans,
  onTamListe,
  birimAd = 'ders',
  tercihKey,
}) => {
  const [acik, setAcik] = useState(() => {
    try {
      return localStorage.getItem(tercihKey) !== '0';
    } catch {
      return true;
    }
  });

  const degistir = () =>
    setAcik((x) => {
      try {
        localStorage.setItem(tercihKey, x ? '0' : '1');
      } catch {
        /* yok */
      }
      return !x;
    });

  const toplamSure = useMemo(() => gruplar.reduce((acc, g) => acc + g.toplamSure, 0), [gruplar]);
  const toplamBirim = useMemo(
    () => gruplar.reduce((acc, g) => acc + (birimAd === 'set' ? g.dersler.length : g.dersler.length), 0),
    [gruplar, birimAd]
  );
  const toplamSoru = useMemo(() => gruplar.reduce((acc, g) => acc + g.toplamSoru, 0), [gruplar]);
  const toplamDinlenen = useMemo(() => gruplar.reduce((acc, g) => acc + g.dinlenenSure, 0), [gruplar]);
  const enCokSure = useMemo(() => Math.max(1, ...gruplar.map((g) => g.toplamSure)), [gruplar]);
  const tamamlananYuzde = toplamSure ? Math.round((toplamDinlenen / toplamSure) * 100) : 0;
  const ortalamaSure = toplamBirim ? Math.round(toplamSure / toplamBirim) : 0;

  return (
    <section className={`sp-sure${acik ? '' : ' is-kapali'}`} aria-label={baslik}>
      <button type="button" className="sp-sure-bas" aria-expanded={acik} onClick={degistir}>
        <span className="sp-sure-ikon" aria-hidden>
          <Clock />
        </span>
        <span className="sp-sure-ana">
          <small>{baslik}</small>
          <b>{fmtSaat(toplamSure)}</b>
        </span>
        <span className="sp-sure-kutu">
          <b>{birimAd === 'set' ? toplamSoru : toplamBirim}</b>
          <small>{birimAd === 'set' ? 'soru' : 'ders'}</small>
        </span>
        <span className="sp-sure-kutu">
          <b>{fmtSaat(ortalamaSure)}</b>
          <small>ortalama</small>
        </span>
        <span className="sp-sure-kutu">
          <b>%{tamamlananYuzde}</b>
          <small>{birimAd === 'set' ? 'çözüldü' : 'dinledin'}</small>
        </span>
        <span className="sp-sure-ac">
          <BarChart3 aria-hidden />
          <span>{acik ? 'Gizle' : 'Branşlar'}</span>
          <ChevronDown aria-hidden className="sp-sure-ok" />
        </span>
      </button>

      {acik && (
        <ul className="sp-sure-liste">
          {gruplar.map((g) => {
            const oran = enCokSure ? (g.toplamSure / enCokSure) * 100 : 0;
            const doluluk = g.toplamSure ? (g.dinlenenSure / g.toplamSure) * 100 : 0;
            const ort = g.dersler.length ? Math.round(g.toplamSure / g.dersler.length) : 0;
            const secili = seciliBrans === g.brans;

            return (
              <li key={g.brans}>
                <button
                  type="button"
                  aria-pressed={secili}
                  className={secili ? 'is-on' : ''}
                  onClick={() => onSecBrans?.(secili ? 'tum' : g.brans)}
                  aria-label={`${g.ad}: ${g.dersler.length} ${birimAd}, ${fmtSaat(g.toplamSure)} anlatım. Bu branşı göster`}
                >
                  <span className="sp-sure-ad">
                    <b>{g.kisa}</b>
                    <small>
                      {g.dersler.length} {birimAd}
                      {birimAd === 'set' && g.toplamSoru ? ` · ${g.toplamSoru} soru` : ''}
                    </small>
                  </span>
                  <span className="sp-sure-cubuk" aria-hidden>
                    <i style={{ width: `${oran}%` }}>
                      <em style={{ width: `${doluluk}%` }} />
                    </i>
                  </span>
                  <span className="sp-sure-deger">
                    <b>{fmtSaat(g.toplamSure)}</b>
                    <small>ort. {fmtSaat(ort)}</small>
                  </span>
                </button>
              </li>
            );
          })}
          <li>
            <button type="button" className="sp-sure-tumu" onClick={onTamListe}>
              <Clock aria-hidden /> Her dersin süresi — tam liste
            </button>
          </li>
        </ul>
      )}
    </section>
  );
};

export default SpotsSureOzeti;
