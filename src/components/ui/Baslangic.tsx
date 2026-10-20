/**
 * Sade başlangıç ekranı (Sınav çalışması · Soru çözücü · En önemliler). Tek sütun, ortalı:
 *   simge + başlık + tek cümle → (varsa) "Kaldığın yerden devam" birincil kartı → seçim listesi (branş/ders) → ikincil bağlantılar.
 * Kalabalık araçlar (arama, süzgeç, istatistik) seçimden sonra gelen ekrandadır; burada yalnız "nereden başlayayım" sorusu yanıtlanır.
 * Stil: styles/baslangic.css (.bs-*), yalnız palet tokenı.
 */
import React, { useId } from 'react';
import { ChevronRight, Play, type LucideIcon } from 'lucide-react';
import '../../styles/baslangic.css';

export interface BaslangicSatir {
  id: string;
  ad: string;
  alt: string;
  /** 0–1 ilerleme; 0 ya da yoksa çubuk çizilmez */
  pay?: number;
  /** sağdaki kısa durum (ör. "%40", "Bitti") */
  durum?: string;
  onSec: () => void;
}

export interface BaslangicDevam {
  etiket: string;
  ad: string;
  sag?: string;
  onClick: () => void;
}

export const Baslangic: React.FC<{
  ikon: LucideIcon;
  baslik: string;
  aciklama: string;
  /** başlığın altında küçük mono özet (toplamlar, genel ilerleme) */
  ozet?: React.ReactNode;
  devam?: BaslangicDevam | null;
  listeAd: string;
  /** null: yükleniyor */
  satirlar: BaslangicSatir[] | null;
  /** listenin altında ikincil bağlantılar / açıklama */
  alt?: React.ReactNode;
  /** listenin üstünde (ör. "Kurul 2 · tümünü göster" hapı) */
  ust?: React.ReactNode;
  /** liste boşsa gösterilen içerik */
  bos?: React.ReactNode;
}> = ({ ikon: Ikon, baslik, aciklama, ozet, devam, listeAd, satirlar, alt, ust, bos }) => {
  const capId = useId();
  return (
    <div className="bs">
      <header className="bs-head">
        <span className="bs-ic" aria-hidden><Ikon /></span>
        <h1 className="bs-h1">{baslik}</h1>
        <p className="bs-desc">{aciklama}</p>
        {ozet && <p className="bs-ozet">{ozet}</p>}
      </header>

      {ust}
      {devam && (
        <button type="button" className="bs-devam" onClick={devam.onClick}>
          <span className="bs-devam-ic" aria-hidden><Play /></span>
          <span className="bs-devam-t">
            <small>{devam.etiket}</small>
            <b>{devam.ad}</b>
          </span>
          {devam.sag && <span className="bs-devam-n">{devam.sag}</span>}
          <ChevronRight className="bs-chev" aria-hidden />
        </button>
      )}

      <section className="bs-sec" aria-labelledby={capId}>
        <h2 className="bs-cap" id={capId}>{listeAd}</h2>
        {satirlar === null ? (
          <div className="bs-skel" aria-busy="true" aria-label="Yükleniyor"><i /><i /><i /><i /></div>
        ) : !satirlar.length && bos ? (
          bos
        ) : (
          <ul className="bs-list">
            {satirlar.map((s) => {
              const pay = Math.max(0, Math.min(1, s.pay || 0));
              return (
                <li key={s.id}>
                  <button type="button" className="bs-row" onClick={s.onSec}>
                    <span className="bs-row-t">
                      <b>{s.ad}</b>
                      <small>{s.alt}</small>
                      {pay > 0 && <span className="bs-bar" aria-hidden><i style={{ width: `${pay * 100}%` }} /></span>}
                    </span>
                    {s.durum && <span className={`bs-durum${pay >= 1 ? ' is-ok' : ''}`}>{s.durum}</span>}
                    <ChevronRight className="bs-chev" aria-hidden />
                  </button>
                </li>
              );
            })}
          </ul>
        )}
      </section>

      {alt && <div className="bs-alt">{alt}</div>}
    </div>
  );
};

/** Başlangıçtan sonraki ekranın üstünde "← Tüm branşlar" gibi geri bağlantısı */
export const BaslangicGeri: React.FC<{ etiket: string; onClick: () => void }> = ({ etiket, onClick }) => (
  <button type="button" className="bs-geri" onClick={onClick}>
    <ChevronRight aria-hidden />
    {etiket}
  </button>
);

export default Baslangic;
