/**
 * Sesli ders metnini dışa aktarma belgesine çevirir (motor: services/metinDisaAktar).
 * Ekranda yazan metin birebir: her bölüm başlık, her paragraf bir madde; önemli cümleler ==…==, terimleri **…**.
 */
import type { AktarBelge } from '../../services/metinDisaAktar';
import type { CdDetay } from './canliDersStore';

function vurgula(metin: string, v?: [number, number, 'c' | 't', number][]): string {
  if (!v?.length) return metin;
  // [konum, işaret, sıra]: aynı konumda eklenen sonra eklenen öne geçer; istenen dizilim "**==" kapanış, "==**" açılış
  const ek: [number, string, number][] = [];
  let son = 0;
  for (const [s, e, tur] of v) {
    if (tur === 'c' && s >= son) { ek.push([s, '==', 1], [e, '==', 2]); son = e; }
  }
  for (const [s, e, tur] of v) if (tur === 't') ek.push([s, '**', 0], [e, '**', 3]);
  ek.sort((x, y) => y[0] - x[0] || x[2] - y[2]);
  let t = metin;
  for (const [k, m] of ek) t = t.slice(0, k) + m + t.slice(k);
  return t;
}

export function cdAktarBelgesi(detay: CdDetay, etiket: string, vurguAcik = true): AktarBelge {
  return {
    baslik: detay.baslik,
    alt: `${etiket} · Sesli ders metni${vurguAcik && detay.vurgu ? ' · işaretli yerler çıkmış, örnek soru ve spotlarla eşleşen önemli bilgiler' : ''}`,
    bolumler: detay.bolumler.map((b) => ({
      baslik: b.baslik.trim(),
      md: b.paragraflar.filter((p) => p.metin.trim())
        .map((p) => `- ${vurgula(p.metin, vurguAcik ? detay.vurgu?.[p.i] : undefined)}`).join('\n'),
    })),
  };
}
