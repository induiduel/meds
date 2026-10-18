import React, { useEffect } from 'react';
import { BarChart3, CheckCircle2, Clock, HelpCircle, Target, Trophy, X, Zap } from 'lucide-react';
import {
  fmtSureDk,
  useSpotCozucuStats,
  type BransCozucuIstatistik,
} from '../../../services/spotCozucuIstatistik';
import { lockScroll, unlockScroll } from '../../../utils/scrollLock';
import type { Brans } from '../brans';

interface Props {
  onClose: () => void;
  onBransSec?: (brans: Brans) => void;
}

export const SpotCozucuIstatistikModal: React.FC<Props> = ({ onClose, onBransSec }) => {
  const stats = useSpotCozucuStats();

  useEffect(() => {
    lockScroll();
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      unlockScroll();
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [onClose]);

  const yuzdeD = stats.cozulenSoru > 0 ? Math.round((stats.dogruIlk / stats.cozulenSoru) * 100) : 0;
  const yuzdeD2 = stats.cozulenSoru > 0 ? Math.round((stats.dogruYardimli / stats.cozulenSoru) * 100) : 0;
  const yuzdeY = stats.cozulenSoru > 0 ? Math.round((stats.yanlis / stats.cozulenSoru) * 100) : 0;

  return (
    <div
      className="scd-modal-arka"
      role="dialog"
      aria-modal="true"
      aria-labelledby="scd-modal-baslik"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="scd-modal">
        <header className="scd-modal-baslik">
          <h2 id="scd-modal-baslik">
            <BarChart3 className="text-accent" />
            Çalışma Karnesi & Doğruluk İstatistikleri
          </h2>
          <button
            type="button"
            className="scd-modal-kapat"
            onClick={onClose}
            aria-label="Kapat"
          >
            <X size={18} />
          </button>
        </header>

        <div className="scd-modal-govde">
          {/* Üst KPI Özeti */}
          <div className="scd-kpi-grid">
            <div className="scd-kpi-kart">
              <span className="scd-kpi-etiket">Toplam Çalışma</span>
              <span className="scd-kpi-deger">{fmtSureDk(stats.toplamSureSn)}</span>
              <span className="scd-kpi-alt">
                {fmtSureDk(stats.spotSureSn)} spot · {fmtSureDk(stats.cozucuSureSn)} çözücü
              </span>
            </div>

            <div className="scd-kpi-kart">
              <span className="scd-kpi-etiket">Doğruluk Oranı</span>
              <span className="scd-kpi-deger" style={{ color: stats.dogrulukOrani >= 70 ? '#16a34a' : stats.dogrulukOrani >= 50 ? '#d97706' : '#dc2626' }}>
                %{stats.dogrulukOrani}
              </span>
              <span className="scd-kpi-alt">
                {stats.dogruIlk} / {stats.cozulenSoru} ilk denemede
              </span>
            </div>

            <div className="scd-kpi-kart">
              <span className="scd-kpi-etiket">Soru İlerlemesi</span>
              <span className="scd-kpi-deger">{stats.cozulenSoru}</span>
              <span className="scd-kpi-alt">
                / {stats.toplamSoru.toLocaleString('tr-TR')} soru (%{stats.cozulmeOrani})
              </span>
            </div>

            <div className="scd-kpi-kart">
              <span className="scd-kpi-etiket">Öğrenilen Spot</span>
              <span className="scd-kpi-deger">{stats.ogrenilenSpot}</span>
              <span className="scd-kpi-alt">
                / {stats.toplamSpot.toLocaleString('tr-TR')} spot (%{stats.spotOgrenmeOrani})
              </span>
            </div>
          </div>

          {/* Doğruluk Dağılımı ve Hız */}
          <div className="scd-kart" style={{ background: 'var(--color-surface, #fff)' }}>
            <div className="scd-kart-bas">
              <span className="scd-kart-etiket">
                <Target size={16} />
                Soru Çözme Başarısı & Çözüm Hızı
              </span>
              {stats.ortalamaSoruSuresiSn > 0 && (
                <span className="scd-rozet is-sure">
                  <Zap size={12} />
                  Ortalama: ~{stats.ortalamaSoruSuresiSn} sn / soru
                </span>
              )}
            </div>

            {stats.cozulenSoru > 0 ? (
              <>
                <div className="scd-prog">
                  <div className="scd-prog-cubuk" style={{ height: 10 }}>
                    <i className="scd-seg-d" style={{ width: `${yuzdeD}%` }} title={`İlk denemede doğru: %${yuzdeD}`} />
                    <i className="scd-seg-d2" style={{ width: `${yuzdeD2}%` }} title={`Yardımla doğru: %${yuzdeD2}`} />
                    <i className="scd-seg-y" style={{ width: `${yuzdeY}%` }} title={`Çözümü dinlenen: %${yuzdeY}`} />
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 8, marginTop: 4 }}>
                  <div style={{ padding: '8px 10px', borderRadius: 8, background: '#f0fdf4', border: '1px solid #bbf7d0', fontSize: 12 }}>
                    <b style={{ color: '#16a34a', display: 'block' }}>İlk Denemede Doğru</b>
                    <span>{stats.dogruIlk} soru (%{yuzdeD})</span>
                  </div>

                  <div style={{ padding: '8px 10px', borderRadius: 8, background: '#eff6ff', border: '1px solid #bfdbfe', fontSize: 12 }}>
                    <b style={{ color: '#2563eb', display: 'block' }}>Yardımla / İkinci Denemede</b>
                    <span>{stats.dogruYardimli} soru (%{yuzdeD2})</span>
                  </div>

                  <div style={{ padding: '8px 10px', borderRadius: 8, background: '#fef2f2', border: '1px solid #fecaca', fontSize: 12 }}>
                    <b style={{ color: '#dc2626', display: 'block' }}>Çözümü Dinlenen / Yanlış</b>
                    <span>{stats.yanlis} soru (%{yuzdeY})</span>
                  </div>
                </div>
              </>
            ) : (
              <p style={{ margin: 0, fontSize: 12.5, color: 'var(--color-text-sub)' }}>
                Henüz soru çözücüde soru çözülmedi. Soru çözmeye başladıkça doğruluk ve çözüm hızı istatistikleriniz burada hesaplanacaktır.
              </p>
            )}
          </div>

          {/* 7 Branş Soru Çözücü Karnesi */}
          <div>
            <h3 style={{ margin: '0 0 8px', fontSize: 13.5, fontWeight: 700, color: 'var(--color-text)' }}>
              Branş Bazında Soru Çözücü Dağılımı (Kurul 1)
            </h3>
            <div className="scd-tablo-kapsayici">
              <table className="scd-tablo">
                <thead>
                  <tr>
                    <th>Branş</th>
                    <th>Çözülen / Toplam</th>
                    <th>Doğruluk</th>
                    <th>Tamamlanan</th>
                    <th>İşlem</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.branslar.map((b: BransCozucuIstatistik) => {
                    const oran = b.toplamSoru > 0 ? Math.round((b.cozulenSoru / b.toplamSoru) * 100) : 0;
                    return (
                      <tr key={b.brans}>
                        <td className="scd-brans-ad">
                          {b.tamAd}
                        </td>
                        <td>
                          <b>{b.cozulenSoru}</b> / {b.toplamSoru}
                          <span className="scd-brans-prog" aria-hidden>
                            <i style={{ width: `${oran}%` }} />
                          </span>
                        </td>
                        <td>
                          <span
                            className="scd-brans-dogruluk"
                            style={{
                              color: b.cozulenSoru === 0 ? 'var(--color-text-sub)' : b.dogrulukOrani >= 70 ? '#16a34a' : b.dogrulukOrani >= 50 ? '#d97706' : '#dc2626',
                            }}
                          >
                            {b.cozulenSoru > 0 ? `%{b.dogrulukOrani}` : '—'}
                          </span>
                        </td>
                        <td>
                          {b.tamamlananDers} / {b.toplamDers} ders
                        </td>
                        <td>
                          <button
                            type="button"
                            className="scd-btn-devam is-ikincil"
                            style={{ padding: '3px 8px', fontSize: 11, width: 'auto' }}
                            onClick={() => {
                              onBransSec?.(b.brans);
                              onClose();
                            }}
                          >
                            Çöz
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
