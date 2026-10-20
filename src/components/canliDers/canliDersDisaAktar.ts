/**
 * Sesli ders metnini dışa aktarma belgesine çevirir (motor: services/metinDisaAktar).
 * Metin birebir korunur, yalnız okunaklı dizilir: her bölüm başlık; kısa, noktasız paragraf alt başlık;
 * paragrafın ilk cümlesi ana madde, sonraki cümleler iç içe alt madde, "Yani/Örneğin…" açıklamaları bir düzey daha içte.
 * Konuşma üslubu dışa aktarımda ders notu üslubuna redakte edilir (services/konusmaRedakte); PDF'de başlık + maddeleri bölünmez.
 * Önemli cümleler ==…==, terimler **…**; okunuş için yazıya dökülmüş sayılar ("iki virgül bir") rakama döner.
 */
import type { AktarBelge } from '../../services/metinDisaAktar';
import { sayilariYaz } from '../../services/sayiYazim';
import { paragrafMd } from '../../services/maddeDuzen';
import { konusmaRedakte } from '../../services/konusmaRedakte';
import type { CdDetay } from './canliDersStore';
import type { SlaytBasliklari } from './cdSlaytBasliklari';

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

/** Paragraf içindeki satır sonları tek boşluk olur: aksi hâlde her satır ayrı blok sayılır ve paragraf sayfa arasında bölünür. */
const tekSatir = (t: string) => t.replace(/[ \t]*\r?\n+[ \t]*/g, ' ').trim();

const katla = (t: string) => t.toLocaleLowerCase('tr').replace(/^\s*\d+[.)-]?\s*/, '').replace(/[^\p{L}\p{N}]+/gu, ' ').trim();

/** basliklar verilirse her paragrafın eşlendiği slaytın başlığı, değiştiği yerde alt başlık (###) olarak girer. */
export function cdAktarBelgesi(detay: CdDetay, etiket: string, vurguAcik = true, basliklar?: SlaytBasliklari): AktarBelge {
  return {
    baslik: detay.baslik,
    dersDuzeni: true,
    alt: `${etiket} · Sesli ders metni${vurguAcik && detay.vurgu ? ' · işaretli yerler çıkmış, örnek soru ve spotlarla eşleşen önemli bilgiler' : ''}`,
    bolumler: detay.bolumler.map((b) => {
      let onceki = katla(b.baslik);
      return {
        baslik: b.baslik.trim(),
        md: b.paragraflar.filter((p) => p.metin.trim())
          .map((p) => {
            const govde = konusmaRedakte(paragrafMd(sayilariYaz(tekSatir(vurgula(p.metin, vurguAcik ? detay.vurgu?.[p.i] : undefined)))));
            const e = basliklar && detay.pdf?.paragraflar?.[p.i];
            const sb = e ? basliklar!.get(`${e.dosya}:${e.sayfa}`) : undefined;
            if (!sb || katla(sb) === onceki) return govde;
            onceki = katla(sb);
            return `### ${sb}\n${govde}`;
          })
          .join('\n'),
      };
    }),
  };
}
