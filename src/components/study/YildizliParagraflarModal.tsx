import React, { useMemo, useState } from 'react';
import { createPortal } from 'react-dom';
import {
  ExternalLink, Headphones, Layers, MessageCircleQuestion,
  Search, Star, Trash2, X,
} from 'lucide-react';
import {
  YildizliParagraf,
  ParagrafKaynak,
  useYildizliParagraflar,
  yildizCikar,
  yildizTemizle,
} from '../../services/yildizliParagrafStore';
import { navigateTo } from '../../router';
import '../../styles/yildizli-paragraflar.css';

interface PanelProps {
  onClose?: () => void;
  onGecis?: (item: YildizliParagraf) => boolean;
  inline?: boolean;
}

export const YildizliParagraflarPanel: React.FC<PanelProps> = ({ onClose, onGecis, inline = false }) => {
  const tumParagraflar = useYildizliParagraflar();
  const [arama, setArama] = useState('');
  const [kaynakFiltre, setKaynakFiltre] = useState<ParagrafKaynak | 'hepsi'>('hepsi');

  const filtrelenmis = useMemo(() => {
    let list = tumParagraflar;
    if (kaynakFiltre !== 'hepsi') {
      list = list.filter((p) => p.kaynak === kaynakFiltre);
    }
    if (arama.trim()) {
      const q = arama.toLocaleLowerCase('tr').trim();
      list = list.filter(
        (p) =>
          p.metin.toLocaleLowerCase('tr').includes(q) ||
          p.baslik.toLocaleLowerCase('tr').includes(q) ||
          (p.altBaslik && p.altBaslik.toLocaleLowerCase('tr').includes(q))
      );
    }
    return list;
  }, [tumParagraflar, kaynakFiltre, arama]);

  const sayilar = useMemo(() => {
    return {
      hepsi: tumParagraflar.length,
      canli_ders: tumParagraflar.filter((p) => p.kaynak === 'canli_ders').length,
      asistan: tumParagraflar.filter((p) => p.kaynak === 'asistan').length,
      soru_cozucu: tumParagraflar.filter((p) => p.kaynak === 'soru_cozucu').length,
    };
  }, [tumParagraflar]);

  const git = (item: YildizliParagraf) => {
    if (onGecis && onGecis(item)) {
      onClose?.();
      return;
    }
    onClose?.();
    navigateTo(item.deeplink);
  };

  const kaynakIkon = (kaynak: ParagrafKaynak) => {
    switch (kaynak) {
      case 'canli_ders':
        return <Headphones aria-hidden />;
      case 'asistan':
        return <Layers aria-hidden />;
      case 'soru_cozucu':
        return <MessageCircleQuestion aria-hidden />;
    }
  };

  const temizleOnay = () => {
    if (window.confirm('Tüm yıldızlı paragrafları listeden çıkarmak istediğine emin misin?')) {
      yildizTemizle();
    }
  };

  return (
    <div className={`yp-panel${inline ? ' is-inline' : ''}`}>
      <header className="yp-header">
        <div className="yp-header-sol">
          <span className="yp-header-ikon" aria-hidden>
            <Star fill="#f59e0b" color="#f59e0b" />
          </span>
          <div>
            <div className="yp-header-baslik-satir">
              <h2>Yıldızlı Paragraflar</h2>
              <span className="yp-rozet">{tumParagraflar.length}</span>
            </div>
            <p className="yp-header-alt">
              Sesli derslerden ve soru çözücüden kaydettiğin kritik noktalar
            </p>
          </div>
        </div>
        {onClose && (
          <button type="button" className="yp-kapat-btn" onClick={onClose} aria-label="Kapat">
            <X />
          </button>
        )}
      </header>

      {tumParagraflar.length > 0 && (
        <div className="yp-araclar">
          <div className="yp-filtreler" role="group" aria-label="Kaynağa göre süz">
            <button
              type="button"
              className={`yp-filtre-btn${kaynakFiltre === 'hepsi' ? ' is-aktif' : ''}`}
              onClick={() => setKaynakFiltre('hepsi')}
            >
              Tümü <span>{sayilar.hepsi}</span>
            </button>
            {sayilar.canli_ders > 0 && (
              <button
                type="button"
                className={`yp-filtre-btn${kaynakFiltre === 'canli_ders' ? ' is-aktif' : ''}`}
                onClick={() => setKaynakFiltre('canli_ders')}
              >
                <Headphones aria-hidden /> Sesli Dersler <span>{sayilar.canli_ders}</span>
              </button>
            )}
            {sayilar.asistan > 0 && (
              <button
                type="button"
                className={`yp-filtre-btn${kaynakFiltre === 'asistan' ? ' is-aktif' : ''}`}
                onClick={() => setKaynakFiltre('asistan')}
              >
                <Layers aria-hidden /> Sınav Asistanı <span>{sayilar.asistan}</span>
              </button>
            )}
            {sayilar.soru_cozucu > 0 && (
              <button
                type="button"
                className={`yp-filtre-btn${kaynakFiltre === 'soru_cozucu' ? ' is-aktif' : ''}`}
                onClick={() => setKaynakFiltre('soru_cozucu')}
              >
                <MessageCircleQuestion aria-hidden /> Soru Çözücü <span>{sayilar.soru_cozucu}</span>
              </button>
            )}
          </div>

          <div className="yp-arama-satir">
            <div className="yp-arama">
              <Search aria-hidden />
              <input
                type="search"
                value={arama}
                onChange={(e) => setArama(e.target.value)}
                placeholder="Paragraf veya konu içinde ara…"
                aria-label="Yıldızlı paragraflarda ara"
              />
              {arama && (
                <button type="button" onClick={() => setArama('')} aria-label="Aramayı temizle">
                  <X />
                </button>
              )}
            </div>
            <button
              type="button"
              className="yp-btn-temizle"
              onClick={temizleOnay}
              title="Tüm yıldızlıları temizle"
              aria-label="Tümünü temizle"
            >
              <Trash2 aria-hidden />
            </button>
          </div>
        </div>
      )}

      <div className="yp-liste">
        {tumParagraflar.length === 0 ? (
          <div className="yp-bos">
            <div className="yp-bos-ikon">
              <Star aria-hidden />
            </div>
            <h3>Henüz yıldızlı paragrafın yok</h3>
            <p>
              Sesli derslerde veya soru çözücü ekranında her paragrafın yanındaki{' '}
              <Star className="yp-mini-star" fill="#f59e0b" color="#f59e0b" /> yıldız işaretine
              dokunarak önemli yerleri bu listeye ekleyebilirsin.
            </p>
            <small>
              Eklediğin paragraflar doğrudan alıntılanan konuma derin bağlantı (deeplink) ile
              bağlanır.
            </small>
          </div>
        ) : filtrelenmis.length === 0 ? (
          <div className="yp-bos">
            <p>Arama kriterine uygun yıldızlı paragraf bulunamadı.</p>
          </div>
        ) : (
          filtrelenmis.map((item) => (
            <article key={item.id} className="yp-kart">
              <div className="yp-kart-ust">
                <div className="yp-kart-kaynak-blok">
                  <span className={`yp-tur t-${item.kaynak}`}>
                    {kaynakIkon(item.kaynak)}
                    {item.kaynakAd}
                  </span>
                  <span className="yp-kart-baslik">{item.baslik}</span>
                  {item.altBaslik && (
                    <span className="yp-kart-alt-baslik">· {item.altBaslik}</span>
                  )}
                </div>
                <button
                  type="button"
                  className="yp-kart-yildiz is-on"
                  onClick={(e) => {
                    e.stopPropagation();
                    yildizCikar(item.id);
                  }}
                  title="Listeden çıkar"
                  aria-label="Listeden çıkar"
                >
                  <Star fill="#f59e0b" color="#f59e0b" />
                </button>
              </div>

              <div
                className="yp-kart-metin"
                onClick={() => git(item)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') git(item);
                }}
              >
                <p>{item.metin.replace(/\*\*/g, '')}</p>
              </div>

              <div className="yp-kart-alt">
                <span className="yp-tarih">
                  {new Date(item.tarih).toLocaleDateString('tr-TR', {
                    day: 'numeric',
                    month: 'short',
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </span>
                <button
                  type="button"
                  className="yp-git-btn"
                  onClick={() => git(item)}
                >
                  <span>Doğrudan git</span>
                  <ExternalLink aria-hidden />
                </button>
              </div>
            </article>
          ))
        )}
      </div>
    </div>
  );
};

export const YildizliParagraflarModal: React.FC<Omit<PanelProps, 'inline'>> = ({
  onClose,
  onGecis,
}) => {
  return createPortal(
    <div
      className="yp-overlay"
      role="dialog"
      aria-modal="true"
      aria-label="Yıldızlı Paragraflar"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose?.();
      }}
    >
      <YildizliParagraflarPanel onClose={onClose} onGecis={onGecis} inline={false} />
    </div>,
    document.body
  );
};
