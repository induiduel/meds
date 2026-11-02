import React, { useEffect, useMemo, useState } from 'react';
import { Megaphone, Star, Headphones, Layers } from 'lucide-react';
import { linkClick, navigateTo, pathFor } from '../../router';
import { HV_KATEGORI, hocaVurguGetir, hvIsaretli, hvIsaretle, useHvIsaret, type HvDers, type HvKategori } from './hocaVurgu';
import '../../styles/v15/hocaVurgu.css';

/**
 * v15 · "Hocanın vurguladıkları" (ders sayfası ?b=vurgu). Hocanın ders kaydında "sınavda sorarım", "çıkmıştı", "önemli",
 * "bilin", "dikkat edin" dediği yerler AYRI kategori olarak (scripts/hoca_vurgu/yayinla.py → src/data/hoca_vurgu/<ders>.json).
 * Her madde: hocanın sözü (zaman damgalı), vurgulanan bilgi, slayt; öğrenci yıldızla işaretler (profil eşitlemeli),
 * "Sesli derste aç" o bilginin anlatıldığı paragrafa gider. Kayıt yalnız döküm anlaşılır ve slayta bağlanmışsa üretilir.
 */
export default function HocaVurguV15({ dersKey, desteId }: { dersKey: string; desteId?: string | null }) {
  const [veri, setVeri] = useState<HvDers | null | undefined>(undefined);
  const [suz, setSuz] = useState<HvKategori | 'isaret' | ''>('');
  const isaret = useHvIsaret();
  useEffect(() => {
    let canli = true;
    setVeri(undefined);
    hocaVurguGetir(dersKey).then((d) => canli && setVeri(d), () => canli && setVeri(null));
    return () => { canli = false; };
  }, [dersKey]);

  const say = useMemo(() => {
    const s: Record<string, number> = {};
    (veri?.vurgular || []).forEach((v) => { s[v.kategori] = (s[v.kategori] || 0) + 1; });
    return s;
  }, [veri]);
  if (veri === undefined) return <span className="v15-skel hv15-skel" aria-hidden />;
  if (!veri || !veri.vurgular.length) return <p className="hv15-bos v15-card">Bu derste hocanın açıkça vurguladığı bir yer kaydedilmedi.</p>;

  const isaretN = veri.vurgular.filter((v) => hvIsaretli(isaret, v.id)).length;
  const liste = veri.vurgular.filter((v) => (suz === 'isaret' ? hvIsaretli(isaret, v.id) : !suz || v.kategori === suz));
  const dinle = pathFor('canli_ders', dersKey);
  return (
    <div className="hv15">
      <p className="hv15-giris v15-card">
        <Megaphone aria-hidden />
        <span>Hocanın ders sırasında <b>sınavda sorulur, çıkmıştı, önemli, bilin, dikkat edin</b> dediği yerler. Her madde hocanın kendi sözüyle
          ve dersteki zamanıyla verilir; yıldızla işaretlediklerin ayrı listede toplanır.</span>
      </p>
      <nav className="hv15-cipler" aria-label="Vurgu türü">
        <button type="button" className={!suz ? 'is-on' : ''} onClick={() => setSuz('')}>Hepsi <span>{veri.vurgular.length}</span></button>
        {HV_KATEGORI.filter((k) => say[k.id]).map((k) => (
          <button key={k.id} type="button" className={`is-${k.id}${suz === k.id ? ' is-on' : ''}`} onClick={() => setSuz(k.id)}>{k.ad} <span>{say[k.id]}</span></button>
        ))}
        <button type="button" className={suz === 'isaret' ? 'is-on' : ''} onClick={() => setSuz('isaret')} disabled={!isaretN}>
          <Star aria-hidden /> İşaretlediklerim <span>{isaretN}</span></button>
      </nav>
      {!liste.length ? <p className="hv15-bos v15-card">Bu süzgeçte madde yok.</p> : (
        <ol className="hv15-liste" role="list">
          {liste.map((v) => {
            const k = HV_KATEGORI.find((x) => x.id === v.kategori);
            const on = hvIsaretli(isaret, v.id);
            const url = v.p != null ? `${dinle}?p=${v.p}` : dinle;
            const ogren = desteId && v.adim != null ? `/ogren/${encodeURIComponent(desteId)}?adim=${v.adim}` : null;
            return (
              <li key={v.id} className={`hv15-m v15-card is-${v.kategori}${on ? ' is-isaret' : ''}`}>
                <div className="hv15-ust">
                  <span className={`hv15-tur is-${v.kategori}`}>{k?.ad || v.kategori}</span>
                  {v.s != null && <span className="hv15-slayt">Slayt s.{v.s}</span>}
                  {v.dk && <span className="hv15-dk" title="Hocanın ders kaydındaki zamanı">{v.dk}</span>}
                  <button type="button" className="hv15-yildiz" aria-pressed={on} onClick={() => hvIsaretle(v.id, !on)}
                    aria-label={on ? 'İşareti kaldır' : 'İşaretle'} title={on ? 'İşareti kaldır' : 'İşaretle'}><Star aria-hidden /></button>
                </div>
                <p className="hv15-konu">{v.konu}</p>
                <blockquote className="hv15-soz">“{v.alinti}”</blockquote>
                <div className="hv15-git">
                  <a href={url} onClick={linkClick(() => navigateTo(url))}><Headphones aria-hidden /> Sesli derste aç</a>
                  {ogren && <a href={ogren} onClick={linkClick(() => navigateTo(ogren))}><Layers aria-hidden /> Öğren adımı {v.adim}</a>}
                </div>
              </li>
            );
          })}
        </ol>
      )}
    </div>
  );
}
