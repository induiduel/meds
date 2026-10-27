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
import { yildizKonum } from '../../services/yildizliKonum';
import '../../styles/yildizli-paragraflar.css';

interface PanelProps {
  onClose?: () => void;
  onGecis?: (item: YildizliParagraf) => boolean;
  inline?: boolean;
  /** Sesli ders içinden açılınca yalnız o dersin paragrafları listelenir (kullanıcı "Tüm dersler"e geçebilir). */
  dersKey?: string;
}

interface ParagrafGrubu {
  anahtar: string;
  kaynak: ParagrafKaynak;
  kaynakAd: string;
  baslik: string;
  bolumBaslik?: string;
  sonTarih: number;
  ogeler: YildizliParagraf[];
}

function grupAnahtari(p: YildizliParagraf): string {
  if (p.kaynak === 'asistan' && p.meta?.dersKod && p.meta?.noktaId) {
    return `asistan|${p.meta.dersKod}|${p.meta.noktaId}`;
  }
  if (p.kaynak === 'canli_ders' && p.meta?.dersKey) {
    return `canli_ders|${p.meta.dersKey}|${p.altBaslik || ''}`;
  }
  if (p.kaynak === 'soru_cozucu' && p.meta?.dersKod) {
    const alt = p.meta.soruNo !== undefined ? `q${p.meta.soruNo}` : 'kisa';
    return `soru_cozucu|${p.meta.dersKod}|${alt}`;
  }
  return `${p.kaynak}|${p.baslik}`;
}

function ogeSiraDegeri(p: YildizliParagraf): number {
  if (p.id.endsWith('_hap')) return 999999;
  if (p.meta?.paragrafIndex !== undefined) return p.meta.paragrafIndex;
  return p.tarih;
}

export const YildizliParagraflarPanel: React.FC<PanelProps> = ({ onClose, onGecis, inline = false, dersKey }) => {
  const hepsi = useYildizliParagraflar();
  const [yalnizDers, setYalnizDers] = useState(!!dersKey);
  const dersSayisi = useMemo(
    () => (dersKey ? hepsi.filter((p) => p.meta?.dersKey === dersKey).length : 0),
    [hepsi, dersKey]
  );
  const tumParagraflar = useMemo(
    () => (dersKey && yalnizDers ? hepsi.filter((p) => p.meta?.dersKey === dersKey) : hepsi),
    [hepsi, dersKey, yalnizDers]
  );
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

  const gruplar = useMemo(() => {
    const map = new Map<string, ParagrafGrubu>();
    for (const p of filtrelenmis) {
      const k = grupAnahtari(p);
      const mevcut = map.get(k);
      const ozelAlt = p.altBaslik === 'Akılda kalsın';
      if (!mevcut) {
        map.set(k, {
          anahtar: k,
          kaynak: p.kaynak,
          kaynakAd: p.kaynakAd,
          baslik: p.baslik,
          bolumBaslik: ozelAlt ? undefined : p.altBaslik,
          sonTarih: p.tarih,
          ogeler: [p],
        });
      } else {
        mevcut.ogeler.push(p);
        if (!mevcut.bolumBaslik && p.altBaslik && !ozelAlt) {
          mevcut.bolumBaslik = p.altBaslik;
        }
        if (p.tarih > mevcut.sonTarih) {
          mevcut.sonTarih = p.tarih;
        }
      }
    }
    const sonuc = [...map.values()];
    for (const g of sonuc) {
      g.ogeler.sort((a, b) => ogeSiraDegeri(a) - ogeSiraDegeri(b));
    }
    return sonuc;
  }, [filtrelenmis]);

  /** Kurul → ders (branş) → konu sırası; konu = grubun başlığı. */
  const agac = useMemo(() => {
    const kurullar = new Map<number, Map<string, ParagrafGrubu[]>>();
    for (const g of gruplar) {
      const { kurul, ders } = yildizKonum(g.ogeler[0]);
      const dm = kurullar.get(kurul) ?? new Map<string, ParagrafGrubu[]>();
      dm.set(ders, [...(dm.get(ders) ?? []), g]);
      kurullar.set(kurul, dm);
    }
    return [...kurullar].sort((a, b) => a[0] - b[0]).map(([k, dm]) => [
      k,
      new Map([...dm].sort((a, b) => a[0].localeCompare(b[0], 'tr'))),
    ] as [number, Map<string, ParagrafGrubu[]>]);
  }, [gruplar]);

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

  const grubuCikar = (g: ParagrafGrubu) => {
    for (const item of g.ogeler) {
      yildizCikar(item.id);
    }
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

      {dersKey && (
        <div className="yp-filtreler" role="group" aria-label="Kapsam" style={{ padding: '10px 20px 0' }}>
          <button type="button" className={`yp-filtre-btn${yalnizDers ? ' is-aktif' : ''}`} onClick={() => setYalnizDers(true)}>
            Bu ders <span>{dersSayisi}</span>
          </button>
          <button type="button" className={`yp-filtre-btn${!yalnizDers ? ' is-aktif' : ''}`} onClick={() => setYalnizDers(false)}>
            Tüm dersler <span>{hepsi.length}</span>
          </button>
        </div>
      )}

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
        ) : gruplar.length === 0 ? (
          <div className="yp-bos">
            <p>Arama kriterine uygun yıldızlı paragraf bulunamadı.</p>
          </div>
        ) : (
          agac.map(([kurul, dersler]) => (
            <details key={kurul} className="yp-kurul" open>
              <summary className="yp-kurul-baslik">
                Kurul {kurul} <span>{[...dersler.values()].reduce((n, gs) => n + gs.reduce((a, g) => a + g.ogeler.length, 0), 0)}</span>
              </summary>
              {[...dersler].map(([ders, gs]) => (
                <details key={ders} className="yp-ders" open>
                  <summary className="yp-ders-baslik">
                    {ders} <span>{gs.reduce((a, g) => a + g.ogeler.length, 0)}</span>
                  </summary>
                  {gs.map((grup) => {
            const ilkOge = grup.ogeler[0];
            const coklu = grup.ogeler.length > 1;
            return (
              <article key={grup.anahtar} className="yp-kart">
                <div className="yp-kart-ust">
                  <div className="yp-kart-kaynak-blok">
                    <span className={`yp-tur t-${grup.kaynak}`}>
                      {kaynakIkon(grup.kaynak)}
                      {grup.kaynakAd}
                    </span>
                    <span className="yp-kart-baslik">{grup.baslik}</span>
                    {grup.bolumBaslik && (
                      <span className="yp-kart-alt-baslik">· {grup.bolumBaslik}</span>
                    )}
                    {coklu && (
                      <span className="yp-grup-sayi">{grup.ogeler.length} paragraf</span>
                    )}
                  </div>
                  {!coklu && (
                    <button
                      type="button"
                      className="yp-kart-yildiz is-on"
                      onClick={(e) => {
                        e.stopPropagation();
                        yildizCikar(ilkOge.id);
                      }}
                      title="Listeden çıkar"
                      aria-label="Listeden çıkar"
                    >
                      <Star fill="#f59e0b" color="#f59e0b" />
                    </button>
                  )}
                </div>

                <div className="yp-grup-metinler">
                  {grup.ogeler.map((item) => {
                    const hapMi = item.altBaslik === 'Akılda kalsın' || item.id.endsWith('_hap');
                    return (
                      <div key={item.id} className={`yp-parca-satir${hapMi ? ' is-hap' : ''}`}>
                        <div
                          className="yp-kart-metin"
                          onClick={() => git(item)}
                          role="button"
                          tabIndex={0}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter') git(item);
                          }}
                        >
                          {hapMi && <span className="yp-hap-etiket">Akılda kalsın</span>}
                          <p>{item.metin.replace(/\*\*/g, '')}</p>
                        </div>
                        {coklu && (
                          <button
                            type="button"
                            className="yp-kart-yildiz is-on"
                            onClick={(e) => {
                              e.stopPropagation();
                              yildizCikar(item.id);
                            }}
                            title="Bu paragrafı listeden çıkar"
                            aria-label="Bu paragrafı listeden çıkar"
                          >
                            <Star fill="#f59e0b" color="#f59e0b" />
                          </button>
                        )}
                      </div>
                    );
                  })}
                </div>

                <div className="yp-kart-alt">
                  <span className="yp-tarih">
                    {new Date(grup.sonTarih).toLocaleDateString('tr-TR', {
                      day: 'numeric',
                      month: 'short',
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </span>
                  <div className="yp-kart-alt-sag">
                    {coklu && (
                      <button
                        type="button"
                        className="yp-grup-cikar-btn"
                        onClick={() => grubuCikar(grup)}
                        title="Bu başlıktaki tüm paragrafları çıkar"
                      >
                        Tümünü çıkar
                      </button>
                    )}
                    <button
                      type="button"
                      className="yp-git-btn"
                      onClick={() => git(ilkOge)}
                    >
                      <span>Doğrudan git</span>
                      <ExternalLink aria-hidden />
                    </button>
                  </div>
                </div>
              </article>
            );
                  })}
                </details>
              ))}
            </details>
          ))
        )}
      </div>
    </div>
  );
};

export const YildizliParagraflarModal: React.FC<Omit<PanelProps, 'inline'>> = ({
  onClose,
  onGecis,
  dersKey,
}) => {
  const portalHedef =
    (typeof document !== 'undefined' && (document.fullscreenElement as HTMLElement | null)) ||
    document.body;

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
      <YildizliParagraflarPanel onClose={onClose} onGecis={onGecis} inline={false} dersKey={dersKey} />
    </div>,
    portalHedef
  );
};

