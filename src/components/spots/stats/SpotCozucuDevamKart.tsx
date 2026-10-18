import React, { useState } from 'react';
import { ArrowRight, BarChart3, BookOpen, Clock, Headphones, History, Play, Sparkles, Target, Zap } from 'lucide-react';
import {
  fmtSureDk,
  relZamanTr,
  useSpotCozucuStats,
  type LastCozucuInfo,
  type LastSpotInfo,
} from '../../../services/spotCozucuIstatistik';
import { bransTanim, type Brans } from '../brans';
import { SpotCozucuIstatistikModal } from './SpotCozucuIstatistikModal';
import '../../../styles/spot-istatistik.css';

interface Props {
  onDevamSpot?: (spot: LastSpotInfo) => void;
  onDevamCozucu?: (cozucu: LastCozucuInfo) => void;
  onBransSec?: (brans: Brans) => void;
}

export const SpotCozucuDevamKart: React.FC<Props> = ({
  onDevamSpot,
  onDevamCozucu,
  onBransSec,
}) => {
  const [modalAcik, setModalAcik] = useState(false);
  const stats = useSpotCozucuStats();

  const yuzdeD = stats.cozulenSoru > 0 ? (stats.dogruIlk / stats.cozulenSoru) * 100 : 0;
  const yuzdeD2 = stats.cozulenSoru > 0 ? (stats.dogruYardimli / stats.cozulenSoru) * 100 : 0;
  const yuzdeY = stats.cozulenSoru > 0 ? (stats.yanlis / stats.cozulenSoru) * 100 : 0;

  return (
    <section className="scd-panel" aria-label="Spot ve Soru Çözücü Çalışma İstatistikleri">
      <div className="scd-ust-bilgi">
        <div className="scd-baslik-grup">
          <span className="scd-baslik-ikon" aria-hidden>
            <Sparkles size={18} />
          </span>
          <div className="scd-baslik-t">
            <b>Çalışma Durumu & Doğruluk Takibi</b>
            <span>
              Toplam {fmtSureDk(stats.toplamSureSn)} çalışma · {stats.cozulenSoru} soru çözüldü
              {stats.cozulenSoru > 0 && ` (%${stats.dogrulukOrani} doğruluk)`}
            </span>
          </div>
        </div>

        <div className="scd-ust-eylemler">
          <button
            type="button"
            className="scd-btn-rapor"
            onClick={() => setModalAcik(true)}
            title="Ayrıntılı doğruluk analizi, branş tablosu ve çalışma süreleri"
          >
            <BarChart3 size={15} aria-hidden />
            <span>Detaylı İstatistikler</span>
          </button>
        </div>
      </div>

      <div className="scd-grid">
        {/* 1. KART: Spot Bilgiler */}
        <div className="scd-kart">
          <div className="scd-kart-bas">
            <span className="scd-kart-etiket">
              <BookOpen size={16} />
              Spot Bilgiler
            </span>
            <div className="scd-kart-rozetler">
              <span className="scd-rozet is-sure" title="Spotlarda aktif çalışma süresi">
                <Clock size={11} />
                {fmtSureDk(stats.spotSureSn)}
              </span>
              <span className="scd-rozet" title="Öğrenilme yüzdesi">
                %{stats.spotOgrenmeOrani}
              </span>
            </div>
          </div>

          <div className="scd-prog">
            <div className="scd-prog-cubuk">
              <i
                className="scd-prog-dolu"
                style={{ width: `${Math.min(100, stats.spotOgrenmeOrani)}%` }}
                aria-hidden
              />
            </div>
            <div className="scd-prog-alt">
              <span>
                <b>{stats.ogrenilenSpot}</b> / {stats.toplamSpot.toLocaleString('tr-TR')} spot öğrenildi
              </span>
              <span>%{stats.spotOgrenmeOrani}</span>
            </div>
          </div>

          <div className="scd-kalinan-yer">
            <History size={14} aria-hidden />
            <div className="scd-ky-metin">
              {stats.lastSpot ? (
                <>
                  <span className="scd-ky-baslik" title={stats.lastSpot.baslik}>
                    Ders {stats.lastSpot.ders}: {stats.lastSpot.baslik}
                  </span>
                  <span className="scd-ky-alt">
                    <span>Son çalışma: {relZamanTr(stats.lastSpot.at)}</span>
                  </span>
                </>
              ) : (
                <span className="scd-ky-baslik" style={{ fontWeight: 500, color: 'var(--color-text-sub)' }}>
                  Henüz bir spot incelenmedi
                </span>
              )}
            </div>
          </div>

          {stats.lastSpot ? (
            <button
              type="button"
              className="scd-btn-devam"
              onClick={() => onDevamSpot?.(stats.lastSpot!)}
            >
              <Play size={13} fill="currentColor" aria-hidden />
              <span>Kaldığın Spottan Devam Et</span>
              <ArrowRight size={13} aria-hidden />
            </button>
          ) : (
            <button
              type="button"
              className="scd-btn-devam is-ikincil"
              onClick={() => onDevamSpot?.({ id: '', ders: 1, baslik: 'İlk ders', at: '' })}
            >
              <span>Spotları İncele</span>
              <ArrowRight size={13} aria-hidden />
            </button>
          )}
        </div>

        {/* 2. KART: Sesli Soru Çözücü */}
        <div className="scd-kart">
          <div className="scd-kart-bas">
            <span className="scd-kart-etiket">
              <Headphones size={16} />
              Sesli Soru Çözücü
            </span>
            <div className="scd-kart-rozetler">
              <span className="scd-rozet is-sure" title="Soru çözücüde aktif çalışma süresi">
                <Clock size={11} />
                {fmtSureDk(stats.cozucuSureSn)}
              </span>
              {stats.cozulenSoru > 0 && (
                <span
                  className={`scd-rozet ${stats.dogrulukOrani >= 70 ? 'is-dogru' : 'is-orta'}`}
                  title="İlk denemede doğru çözüm oranı"
                >
                  <Target size={11} />
                  %{stats.dogrulukOrani} Doğruluk
                </span>
              )}
            </div>
          </div>

          <div className="scd-prog">
            <div className="scd-prog-cubuk">
              <i className="scd-seg-d" style={{ width: `${yuzdeD}%` }} title={`İlk denemede doğru: ${stats.dogruIlk}`} />
              <i className="scd-seg-d2" style={{ width: `${yuzdeD2}%` }} title={`Yardımla doğru: ${stats.dogruYardimli}`} />
              <i className="scd-seg-y" style={{ width: `${yuzdeY}%` }} title={`Çözümü dinlenen: ${stats.yanlis}`} />
            </div>
            <div className="scd-prog-alt">
              <span>
                <b>{stats.cozulenSoru}</b> / {stats.toplamSoru.toLocaleString('tr-TR')} soru çözüldü
              </span>
              <span>
                {stats.dogruIlk} doğru{stats.dogruYardimli > 0 ? ` · ${stats.dogruYardimli} yardımlı` : ''}
              </span>
            </div>
          </div>

          <div className="scd-kalinan-yer">
            <History size={14} aria-hidden />
            <div className="scd-ky-metin">
              {stats.lastCozucu ? (
                <>
                  <span className="scd-ky-baslik" title={`${stats.lastCozucu.baslik} · Soru ${stats.lastCozucu.soruNo}`}>
                    {bransTanim(stats.lastCozucu.brans).ad} · {stats.lastCozucu.dersNo}. {stats.lastCozucu.baslik}
                  </span>
                  <span className="scd-ky-alt">
                    <span>Soru {stats.lastCozucu.soruNo} / {stats.lastCozucu.toplamSoru}</span>
                    <span>·</span>
                    <span>{relZamanTr(stats.lastCozucu.at)}</span>
                    {stats.ortalamaSoruSuresiSn > 0 && (
                      <>
                        <span>·</span>
                        <span>~{stats.ortalamaSoruSuresiSn} sn/soru</span>
                      </>
                    )}
                  </span>
                </>
              ) : (
                <span className="scd-ky-baslik" style={{ fontWeight: 500, color: 'var(--color-text-sub)' }}>
                  Henüz soru çözücüsü başlatılmadı
                </span>
              )}
            </div>
          </div>

          {stats.lastCozucu ? (
            <button
              type="button"
              className="scd-btn-devam"
              onClick={() => onDevamCozucu?.(stats.lastCozucu!)}
            >
              <Play size={13} fill="currentColor" aria-hidden />
              <span>Kaldığın Sorudan Devam Et</span>
              <ArrowRight size={13} aria-hidden />
            </button>
          ) : (
            <button
              type="button"
              className="scd-btn-devam is-ikincil"
              onClick={() =>
                onDevamCozucu?.({
                  brans: 'patoloji',
                  kod: 'p01',
                  dersNo: 1,
                  baslik: 'İlk Konu',
                  soruNo: 1,
                  toplamSoru: 10,
                  at: '',
                })
              }
            >
              <span>Soru Çözmeye Başla</span>
              <ArrowRight size={13} aria-hidden />
            </button>
          )}
        </div>
      </div>

      {modalAcik && (
        <SpotCozucuIstatistikModal
          onClose={() => setModalAcik(false)}
          onBransSec={onBransSec}
        />
      )}
    </section>
  );
};
