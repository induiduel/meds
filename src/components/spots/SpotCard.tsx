import React, { useEffect, useState } from 'react';
import { AlertTriangle, BookMarked, Check, Eye, Share2 } from 'lucide-react';
import { toast } from '../ui/Toast';
import { KAT, Spot, Zengin } from './spotsShared';
import { kaydetSpotZiyaret } from '../../services/spotCozucuIstatistik';

/**
 * Tek spot kartı: kategori etiketi · önem çubukları · başlık · spot metni · maddeler · karşılaştırma tablosu ·
 * tuzak kutusu · alt eylemler (Öğrendim / Kaynak / Paylaş). Soru-cevap her modda kartın başında yazılıdır;
 * "Kendini sına" modunda yalnız soru görünür, gövde "Cevabı göster" ile açılır. Açılan içeriği görünür alana kaydırma işini utils/autoReveal.ts üstlenir
 * (aria-expanded + aria-controls taşıyan düğmeler); burada ayrıca scrollIntoView yazılmaz, çift kaydırma olmasın.
 */

const OnemCubuk: React.FC<{ n: number }> = ({ n }) => (
  <span className="xs-onem" role="img" aria-label={`Önem ${n}/3`} title={n === 3 ? 'Kesin sorulur' : n === 2 ? 'Sık sorulur' : 'Destekleyici'}>
    {[1, 2, 3].map((i) => <i key={i} className={i <= n ? 'is-on' : ''} />)}
  </span>
);

const paylas = async (s: Spot) => {
  const url = `${location.origin}/spotlar?id=${encodeURIComponent(s.id)}`;
  const nav = navigator as Navigator & { share?: (d: ShareData) => Promise<void> };
  if (nav.share) {
    try {
      await nav.share({ title: s.baslik, text: `Sınav spotu: ${s.baslik}`, url });
      return;
    } catch (e) {
      if ((e as Error)?.name === 'AbortError') return; // kullanıcı vazgeçti
    }
  }
  try {
    await navigator.clipboard.writeText(url);
    toast.show('success', 'Bağlantı kopyalandı', s.baslik);
  } catch {
    toast.show('error', 'Bağlantı kopyalanamadı', url);
  }
};

interface Props {
  s: Spot;
  sinav: boolean;
  ogrenildi: boolean;
  vurgulu: boolean;
  onOgren: (id: string) => void;
}

const SpotCardBase: React.FC<Props> = ({ s, sinav, ogrenildi, vurgulu, onOgren }) => {
  const [acik, setAcik] = useState(false);
  const [kaynakAcik, setKaynakAcik] = useState(false);

  // Mod değişince açılan cevaplar yeniden gizlenir
  useEffect(() => { setAcik(false); }, [sinav]);

  const gizli = sinav && !acik;
  const kat = KAT[s.kategori];
  const tablo = s.karsilastir && s.karsilastir.basliklar?.length > 0 ? s.karsilastir : null;
  const kaynakId = `xs-src-${s.id}`;
  const govdeId = `xs-body-${s.id}`;

  return (
    <article
      id={`xs-${s.id}`}
      className={`xs-card k-${s.kategori}${ogrenildi ? ' is-done' : ''}${vurgulu ? ' is-flash' : ''}`}
      aria-labelledby={`xs-t-${s.id}`}
      onClick={() => kaydetSpotZiyaret({ id: s.id, ders: s.ders, baslik: s.baslik, kategori: s.kategori })}
    >
      <div className="xs-card-top">
        <span className="xs-tag" title={kat?.aciklama}>{kat?.kisa}</span>
        <OnemCubuk n={s.onem} />
        {ogrenildi && <span className="xs-done-mark"><Check size={12} strokeWidth={3} aria-hidden /> Öğrenildi</span>}
      </div>

      <h3 className="xs-card-t" id={`xs-t-${s.id}`}>{s.baslik}</h3>

      {gizli ? (
        <div className="xs-quiz">
          <p className="xs-quiz-q">{s.soru || 'Bu spotu hatırlıyor musun?'}</p>
          <button type="button" className="xs-reveal" aria-expanded={false} aria-controls={govdeId} onClick={() => setAcik(true)}>
            <Eye size={15} aria-hidden /> Cevabı göster
          </button>
        </div>
      ) : (
        <div className="xs-card-b" id={govdeId}>
          {s.soru && s.cevap && (
            <div className="xs-qa">
              <p className="xs-qa-q"><span>Soru</span><Zengin metin={s.soru} /></p>
              <p className="xs-answer"><span>Cevap</span><Zengin metin={s.cevap} /></p>
            </div>
          )}
          <p className="xs-text"><Zengin metin={s.spot} /></p>
          {!!s.maddeler?.length && (
            <ul className="xs-list">{s.maddeler.map((m, i) => <li key={i}><Zengin metin={m} /></li>)}</ul>
          )}
          {tablo && (
            <div className="xs-table-wrap" tabIndex={0} role="region" aria-label={`${s.baslik} karşılaştırma tablosu`}>
              <table className="xs-table">
                <thead>
                  <tr><th scope="col"><span className="sr-only">Ölçüt</span></th>{tablo.basliklar.map((b, i) => <th key={i} scope="col">{b}</th>)}</tr>
                </thead>
                <tbody>
                  {tablo.satirlar.map((r, i) => (
                    <tr key={i}><th scope="row">{r[0]}</th>{r.slice(1).map((c, j) => <td key={j}><Zengin metin={c} /></td>)}</tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {s.tuzak && (
            <div className="xs-trap" role="note">
              <AlertTriangle size={15} aria-hidden />
              <p><b>Tuzak:</b> <Zengin metin={s.tuzak} /></p>
            </div>
          )}
        </div>
      )}

      {kaynakAcik && !!s.kaynak?.length && (
        <div className="xs-src" id={kaynakId}>
          <span className="xs-src-h">Ders notundan</span>
          {s.kaynak.map((k, i) => (
            <blockquote key={i}>“{k.alinti}”{k.satir ? <cite> · satır {k.satir}</cite> : null}</blockquote>
          ))}
        </div>
      )}

      <div className="xs-card-f">
        <button
          type="button"
          className={`xs-learn${ogrenildi ? ' is-on' : ''}`}
          aria-pressed={ogrenildi}
          onClick={(e) => {
            e.stopPropagation();
            kaydetSpotZiyaret({ id: s.id, ders: s.ders, baslik: s.baslik, kategori: s.kategori });
            onOgren(s.id);
          }}
        >
          <Check size={15} strokeWidth={ogrenildi ? 3 : 2} aria-hidden /> Öğrendim
        </button>
        {!!s.kaynak?.length && (
          <button type="button" className="xs-act" aria-expanded={kaynakAcik} aria-controls={kaynakId} onClick={() => setKaynakAcik((v) => !v)}>
            <BookMarked size={14} aria-hidden /> Kaynak
          </button>
        )}
        <button type="button" className="xs-act xs-share" aria-label={`Paylaş: ${s.baslik}`} title="Paylaş" onClick={() => void paylas(s)}>
          <Share2 size={15} aria-hidden />
        </button>
      </div>
    </article>
  );
};

export const SpotCard = React.memo(SpotCardBase);
