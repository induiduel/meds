import { createContext, useContext } from 'react';
import { sayi, type SeriNokta } from './saglikVeri';

/**
 * Sağlık Bakanlığı sekmesinin ortak bağlamları (bileşen içermez — döngüsel içe aktarma olmasın):
 *  - Görünüm: "kart" (görsel) ya da "madde" (her blok madde madde metin). Sayfa başındaki seçim; blok kendi düğmesiyle ezebilir.
 *  - Geçmiş yıllar: gösterge kutusu dokununca açılan pencere (SaglikMadde › GecmisPencere).
 */

/** Madde: düz metin ya da alt maddeli, kaynaklı öge */
export type MaddeOge = string | { metin: string; alt?: MaddeOge[]; kaynak?: string; ek?: string[]; konum?: string };

export type GorunumModu = 'kart' | 'madde';
export const GorunumCtx = createContext<{ mod: GorunumModu; setMod: (m: GorunumModu) => void }>({ mod: 'kart', setMod: () => {} });
export const useGorunum = () => useContext(GorunumCtx);

export type GecmisNokta = SeriNokta & { kaynak?: string; konum?: string; not?: string };
export interface GecmisIstek {
  baslik: string;
  birim?: string;
  /** İlk seri ana (vurgu), ikincisi karşılaştırma (nötr, ör. Türkiye) */
  seriler: { ad: string; seri: GecmisNokta[] }[];
  kaynak?: string;
  ek?: string[];
  konum?: string;
  tanim?: string;
  not?: string;
  ondalik?: number;
}
export const GecmisCtx = createContext<(g: GecmisIstek) => void>(() => {});
export const useGecmis = () => useContext(GecmisCtx);

/** Yıllık nokta mı? ("2002-2003" gibi dönemler grafikte yer almaz, listede kalır) */
export const yillikMi = (p: { yil: number | string | null | undefined }) => /^\d{4}$/.test(String(p.yil ?? ''));

/** Yılın yönelme eki: 2024'e, 2002'ye, 2010'a, 2006'ya, 2000'e (son okunan sözcüğün ünlüsüne göre) */
export function yilaEk(y: number | string): string {
  const n = parseInt(String(y), 10);
  if (isNaN(n)) return `${y}'e`;
  const birler = ['', 'e', 'ye', 'e', 'e', 'e', 'ya', 'ye', 'e', 'a'];
  const onlar = ['', 'a', 'ye', 'a', 'a', 'ye', 'a', 'e', 'e', 'a'];
  let ek: string;
  if (n % 10) ek = birler[n % 10];
  else if (n % 100) ek = onlar[(n % 100) / 10];
  else ek = 'e'; // yüz, bin
  return `${y}'${ek}`;
}

/** Değer + birim: yüzde Türkçe biçimde önde ("%94"), diğerleri arkada ("7,8 binde") */
export const degerBirim = (v: number | string, birim?: string, ondalik?: number) => {
  const d = typeof v === 'number' ? sayi(v, ondalik) : v;
  if (birim === '%') return /^%/.test(String(d)) ? String(d) : `%${d}`;
  return `${d}${birim ? ` ${birim}` : ''}`;
};

/** Seriyi yeniden eskiye madde listesine çevirir: "2025: 7,8 binde (2024'e göre −1,2)" */
export function seriMaddeleri(seri: GecmisNokta[], birim?: string, ondalik?: number): MaddeOge[] {
  const yillik = seri.filter((p) => typeof p.deger === 'number').slice().sort((a, b) => {
    const ya = parseInt(String(a.yil), 10), yb = parseInt(String(b.yil), 10);
    return (isNaN(yb) ? 0 : yb) - (isNaN(ya) ? 0 : ya);
  });
  return yillik.map((p, i) => {
    const onceki = yillik[i + 1];
    let fark = '';
    if (onceki && yillikMi(p) && yillikMi(onceki) && typeof onceki.deger === 'number' && onceki.deger !== 0) {
      const d = p.deger - onceki.deger;
      const yuzde = (d / Math.abs(onceki.deger)) * 100;
      const isaret = d > 0 ? '+' : d < 0 ? '−' : '±';
      const yz = Math.abs(yuzde).toLocaleString('tr-TR', { maximumFractionDigits: 1 });
      fark = ` (${yilaEk(onceki.yil)} göre ${isaret}${sayi(Math.abs(d), ondalik)}${birim === '%' ? ' puan' : ''}; ${isaret}%${yz})`;
    }
    return { metin: `**${p.yil}**: ${degerBirim(p.deger, birim, ondalik)}${fark}${p.not ? ` — ${p.not}` : ''}`, kaynak: p.kaynak, konum: p.konum };
  });
}

/** Madde ağacını düz metne çevirir (kopyalama). `num` kaynak numarasını verir. */
export function maddeMetni(ogeler: MaddeOge[], num: (id?: string) => number | undefined, girinti = ''): string {
  const duz = (x: string) => x.replace(/\*\*|==/g, '');
  return ogeler.map((o) => {
    if (typeof o === 'string') return `${girinti}- ${duz(o)}`;
    const n = num(o.kaynak);
    const ekler = (o.ek || []).map(num).filter(Boolean).map((x) => `[${x}]`).join('');
    const satir = `${girinti}- ${duz(o.metin)}${n ? ` [${n}]` : ''}${ekler}`;
    return o.alt?.length ? `${satir}\n${maddeMetni(o.alt, num, `${girinti}  `)}` : satir;
  }).join('\n');
}
