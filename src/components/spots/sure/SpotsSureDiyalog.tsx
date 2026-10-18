import React, { useEffect, useRef } from 'react';
import { Clock, X } from 'lucide-react';
import { dk, fmtSaat, fmtSure, type SpotBransSureGrup } from './spotsSureVeri';
import { type Brans } from '../brans';
import '../../../styles/spots-sure.css';

interface Props {
  baslik: string;
  gruplar: SpotBransSureGrup[];
  onKapat: () => void;
  onDersAc: (brans: Brans, kod: string) => void;
  birimAd?: 'ders' | 'set';
  not?: string;
}

export const SpotsSureDiyalog: React.FC<Props> = ({
  baslik,
  gruplar,
  onKapat,
  onDersAc,
  birimAd = 'ders',
  not,
}) => {
  const kapatRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    kapatRef.current?.focus();
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onKapat();
    };
    document.addEventListener('keydown', handleKey);
    const eskiOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', handleKey);
      document.body.style.overflow = eskiOverflow;
    };
  }, [onKapat]);

  const toplamSure = gruplar.reduce((acc, g) => acc + g.toplamSure, 0);
  const toplamBirim = gruplar.reduce((acc, g) => acc + g.dersler.length, 0);
  const toplamSoru = gruplar.reduce((acc, g) => acc + g.toplamSoru, 0);

  return (
    <div
      className="sp-dlg"
      role="presentation"
      onClick={(e) => {
        if (e.target === e.currentTarget) onKapat();
      }}
    >
      <div className="sp-dlg-kart" role="dialog" aria-modal="true" aria-labelledby="sp-dlg-baslik-id">
        <header className="sp-dlg-bas">
          <div id="sp-dlg-baslik-id" className="sp-dlg-baslik">
            <Clock aria-hidden />
            <span>{baslik}</span>
          </div>
          <button
            ref={kapatRef}
            type="button"
            className="sp-dlg-kapat"
            onClick={onKapat}
            aria-label="Kapat"
          >
            <X aria-hidden />
          </button>
        </header>

        <div className="sp-dlg-govde">
          <div className="sp-sl">
            <section className="sp-sl-toplam" aria-label="Tüm dersler toplamı">
              <div>
                <small>Tüm Branşlar Toplamı</small>
                <b>{dk(toplamSure).toLocaleString('tr-TR')} dk</b>
                <span>
                  {fmtSaat(toplamSure)} · {toplamBirim} {birimAd}
                  {birimAd === 'set' && ` · ${toplamSoru.toLocaleString('tr-TR')} soru`} · {gruplar.length} branş
                </span>
              </div>
              <ul>
                {gruplar.map((g) => (
                  <li key={g.brans}>
                    <a
                      href={`#sure-${g.brans}`}
                      onClick={(e) => {
                        e.preventDefault();
                        document.getElementById(`sure-${g.brans}`)?.scrollIntoView({
                          behavior: 'smooth',
                          block: 'start',
                        });
                      }}
                    >
                      <b>{g.kisa}</b>
                      <span>{dk(g.toplamSure)} dk</span>
                    </a>
                  </li>
                ))}
              </ul>
            </section>

            {gruplar.map((g) => (
              <section key={g.brans} id={`sure-${g.brans}`} className="sp-sl-grup" aria-label={`${g.ad} süreleri`}>
                <h2>
                  <span>
                    {g.ad}
                    {g.alt && <small> · {g.alt}</small>}
                  </span>
                  <span className="sp-sl-ara">
                    {g.dersler.length} {birimAd} · {dk(g.toplamSure)} dk · {fmtSaat(g.toplamSure)}
                  </span>
                </h2>
                <table className="sp-sl-tablo">
                  <thead>
                    <tr>
                      <th scope="col">No</th>
                      <th scope="col">{birimAd === 'set' ? 'Ders / Set Başlığı' : 'Ders Başlığı'}</th>
                      <th scope="col">{birimAd === 'set' ? 'Soru Sayısı' : 'Kapsam'}</th>
                      <th scope="col">Tahmini Süre</th>
                    </tr>
                  </thead>
                  <tbody>
                    {g.dersler.map((d) => (
                      <tr key={d.kod}>
                        <td className="sp-sl-no">{d.no}</td>
                        <td>
                          <button
                            type="button"
                            className="sp-sl-link"
                            onClick={() => {
                              onKapat();
                              onDersAc(g.brans, d.kod);
                            }}
                            title="Bu dersi aç"
                          >
                            {d.baslik}
                            {d.setSay && d.setSay > 1 ? ` (Set ${d.set}/${d.setSay})` : ''}
                          </button>
                        </td>
                        <td>
                          {birimAd === 'set' ? (
                            <span>
                              {d.soru} soru
                              {d.cikmis ? ` (${d.cikmis} çıkmış)` : ''}
                            </span>
                          ) : (
                            <span>
                              {d.adim ? `${d.adim} nokta` : ''}
                              {d.soru ? ` · ${d.soru} soru` : ''}
                            </span>
                          )}
                        </td>
                        <td className="sp-sl-sure">
                          <b>{dk(d.sure)} dk</b>
                          <small>{fmtSure(d.sure)}</small>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot>
                    <tr>
                      <td />
                      <th scope="row">{g.kisa} Toplamı</th>
                      <td>
                        {birimAd === 'set'
                          ? `${g.toplamSoru} soru`
                          : `${g.toplamAdim} nokta · ${g.toplamSoru} soru`}
                      </td>
                      <td className="sp-sl-sure">
                        <b>{dk(g.toplamSure)} dk</b>
                        <small>{fmtSaat(g.toplamSure)}</small>
                      </td>
                    </tr>
                  </tfoot>
                </table>
              </section>
            ))}

            <p className="sp-sl-not">
              {not ||
                'Süreler EMA seslendirme hızına göre hesaplanmıştır; soru çözücü süreleri soru, şıklar, ipuçları ve çözüm açıklamalarını içerir.'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SpotsSureDiyalog;
