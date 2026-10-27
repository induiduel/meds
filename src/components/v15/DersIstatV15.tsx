import React from 'react';
import { BarChart3, ChevronDown } from 'lucide-react';
import { bittiMi, sesliKonuId, sureYaz, useTakip, type KonuKaydi } from '../../services/calismaTakip';
import { ogrenTakipId } from '../takip/ogrenTakipId';

/**
 * v15 · Ders ayrıntısındaki açılır "Bu dersteki çalışman" kartı: süre (sesli ders, Öğren, soru çözücü), tekrar
 * (tur, durum, ilk/son çalışma) ve sorular (çıkmış, örnek, mini, Öğren, çözücü). Yalnız cihazda/profilde kayıtlı
 * gerçek veri; kaydı olmayan satır "—" gösterir. Kapalıyken başlıkta tek satır özet görünür.
 */
const tarih = (s?: string) => (s ? new Date(s).toLocaleDateString('tr-TR', { day: 'numeric', month: 'short' }) : '—');

export default function DersIstatV15(p: {
  dersKey: string;
  desteId?: string | null;
  cozucuUrl?: string | null;
  cikmisN: number;
  miniN: number;
  acik: boolean;
  onToggle: (acik: boolean) => void;
}) {
  const takip = useTakip();
  const sesli: KonuKaydi | undefined = takip.k[`sesli:${sesliKonuId(p.dersKey)}`];
  const ogren = p.desteId ? takip.k[`ogren:${ogrenTakipId(p.desteId)}`] : undefined;
  const cz = p.cozucuUrl ? new URLSearchParams(p.cozucuUrl.split('?')[1] || '') : null;
  const cozucu = cz?.get('brans') && cz.get('ders') ? takip.k[`cozucu:${cz.get('brans')}/${cz.get('ders')}`] : undefined;

  const snS = sesli?.sn || 0, snO = ogren?.sn || 0, snC = cozucu?.sn || 0;
  const toplamSn = snS + snO + snC;
  const cikmis = sesli?.cz?.cikmis?.length || 0;
  const ornek = sesli?.cz?.ornek?.length || 0;
  const mini = sesli?.cz?.mini?.length || 0;
  const soruO = ogren?.soru || 0, soruC = cozucu?.soru || 0;
  const toplamSoru = cikmis + ornek + mini + soruO + soruC;
  const bitti = bittiMi(sesli);
  const tur = sesli?.tur || 0;
  // tekrar sayısı: "Tekrar et" ile açılan turlar; bitti sonrası yeniden dinlemede tur kaydı yoksa en az bitirme sayılır
  const durum = sesli?.durum === 'tekrar' ? `${tur}. tekrarda` : bitti ? 'Bitirdin' : sesli?.sn ? 'Devam ediyor' : 'Başlamadın';
  const ilk = [sesli?.ilkAt, ogren?.ilkAt, cozucu?.ilkAt].filter(Boolean).sort()[0];
  const son = [sesli?.sonAt, ogren?.sonAt, cozucu?.sonAt].filter(Boolean).sort().pop();

  const gruplar: { ad: string; satir: [string, string, string?][] }[] = [
    {
      ad: 'Süre',
      satir: [
        ['Toplam', toplamSn ? sureYaz(toplamSn) : '—'],
        ['Sesli ders', snS ? sureYaz(snS) : '—'],
        ...(p.desteId ? [['Öğren destesi', snO ? sureYaz(snO) : '—'] as [string, string]] : []),
        ...(p.cozucuUrl ? [['Soru çözücü', snC ? sureYaz(snC) : '—'] as [string, string]] : []),
      ],
    },
    {
      ad: 'Tekrar',
      satir: [
        ['Tekrar sayısı', String(tur)],
        ['Durum', durum],
        ['İlk çalışma', tarih(ilk)],
        ['Son çalışma', tarih(son)],
      ],
    },
    {
      ad: 'Sorular',
      satir: [
        ...(p.cikmisN ? [['Çıkmış soru', String(cikmis), `/${p.cikmisN}`] as [string, string, string]] : []),
        ['Örnek soru', String(ornek)],
        ...(p.miniN ? [['Mini soru', String(mini), `/${p.miniN}`] as [string, string, string]] : []),
        ...(p.desteId ? [['Öğren soruları', String(soruO)] as [string, string]] : []),
        ...(p.cozucuUrl ? [['Çözücü soruları', String(soruC)] as [string, string]] : []),
      ],
    },
  ];
  const ozet = [toplamSn ? sureYaz(toplamSn) : null, `${tur} tekrar`, `${toplamSoru} soru`].filter(Boolean).join(' · ');

  return (
    <details className="dd15-grup dd15-istat v15-card" open={p.acik} onToggle={(e) => p.onToggle((e.currentTarget as HTMLDetailsElement).open)}>
      <summary>
        <span className="v15-tile is-c" aria-hidden><BarChart3 /></span>
        <b>Bu dersteki çalışman</b>
        <span className="v15-cap">{ozet}</span>
        <ChevronDown className="dd15-grup-ok" aria-hidden />
      </summary>
      <div className="dd15-istat-g">
        {gruplar.map((g) => (
          <section key={g.ad} aria-label={g.ad}>
            <h3>{g.ad}</h3>
            <dl>
              {g.satir.map(([a, d, alt]) => (
                <div key={a}>
                  <dt>{a}</dt>
                  <dd>{d}{alt && <small>{alt}</small>}</dd>
                </div>
              ))}
            </dl>
          </section>
        ))}
      </div>
    </details>
  );
}
