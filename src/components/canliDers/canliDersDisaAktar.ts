/**
 * Sesli ders metnini dışa aktarma belgesine çevirir (motor: services/metinDisaAktar).
 * Metin birebir korunur, yalnız okunaklı dizilir: her bölüm başlık; kısa, noktasız paragraf alt başlık;
 * paragrafın ilk cümlesi ana madde, sonraki cümleler iç içe alt madde, "Yani/Örneğin…" açıklamaları bir düzey daha içte.
 * Konuşma üslubu dışa aktarımda ders notu üslubuna redakte edilir (services/konusmaRedakte); PDF'de başlık + maddeleri bölünmez.
 * Önemli cümleler ==…==, terimler **…**; okunuş için yazıya dökülmüş sayılar ("iki virgül bir") rakama döner.
 * İçerik seçenekleri (CdAktarSecenek): kapsam (tüm metin / yalnız önemli yerler), üslup (ders notu / konuşma metni), işaretler,
 * slayt başlıkları, resimler, bölüm seçimi ve ekler (terimler ve kısaltmalar, doğrulanmış çıkmış sorular). Seçimler cihazda hatırlanır.
 */
import { resimSatiri, type AktarBelge } from '../../services/metinDisaAktar';
import { araResimBitis, araResimleri, araResimYolu, type AraResim } from './araResimVeri';
import { ekranYazimi } from '../../services/ekranYazim';
import { cumleler, paragrafMd } from '../../services/maddeDuzen';
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

/** Dışa aktarılan belgenin içeriği (biçim ve sayfa görünümü ayrı: AktarBicim, PdfDuzen) */
export interface CdAktarSecenek {
  /** tam: bütün anlatım · onemli: yalnız önemli diye işaretlenmiş cümleler (kısa tekrar notu) */
  kapsam: 'tam' | 'onemli';
  /** not: ders notu üslubu, iç içe maddeler · konusma: seslendirilen metin olduğu gibi, paragraf paragraf */
  uslup: 'not' | 'konusma';
  /** önemli cümleler işaretli (==…==) */
  vurgu: boolean;
  /** anahtar terimler kalın */
  terim: boolean;
  /** slayt başlıkları alt başlık olur (PDF açılır; daha yavaş) */
  basliklar: boolean;
  /** ara resimler */
  resimler: boolean;
  /** ek: terimler ve kısaltmalar */
  sozluk: boolean;
  /** ek: bu dersten çıkmış sorular (yalnız doğrulanmış eşlemeler) */
  cikmis: boolean;
}
export const CD_AKTAR_VARSAYILAN: CdAktarSecenek = { kapsam: 'tam', uslup: 'not', vurgu: true, terim: true, basliklar: true, resimler: true, sozluk: false, cikmis: false };
const SECENEK_ANAHTAR = 'medsoru_cd_aktar_secenek_v1';
export function cdAktarSecenekOku(): CdAktarSecenek {
  try { return { ...CD_AKTAR_VARSAYILAN, ...JSON.parse(localStorage.getItem(SECENEK_ANAHTAR) || '{}') }; } catch { return { ...CD_AKTAR_VARSAYILAN }; }
}
export function cdAktarSecenekYaz(s: CdAktarSecenek) {
  try { localStorage.setItem(SECENEK_ANAHTAR, JSON.stringify(s)); } catch { /* yok */ }
}

/** Derste hangi seçeneklerin karşılığı var (olmayan seçenek pencerede kapalı görünür) */
export function cdAktarVar(detay: CdDetay) {
  return {
    vurgu: !!detay.vurgu && Object.values(detay.vurgu).some((v) => v.some((x) => x[2] === 'c')),
    terim: !!detay.vurgu && Object.values(detay.vurgu).some((v) => v.some((x) => x[2] === 't')),
    basliklar: !!detay.pdf,
    resimler: araResimleri(detay.key).length > 0,
    sozluk: sozlukMd(detay).length > 0,
    cikmis: (detay.cikmisKonum || []).some((c) => c.dogrulandi),
  };
}

const trSirala = (a: string, b: string) => a.localeCompare(b, 'tr');

/** Ek: slaytlardaki terimler ve kısaltmalar (PDF terim yardımcısının verisi), abc sırasıyla, yinelenenler tek */
function sozlukMd(detay: CdDetay): string {
  const terim = new Map<string, string>(), kis = new Map<string, string>();
  for (const katman of [detay.terim, detay.kisaltma]) {
    for (const dosya of Object.values(katman || {})) for (const sayfa of Object.values(dosya || {})) for (const t of sayfa?.t || []) {
      const ad = (t.t || '').trim(), a = (t.a || '').trim();
      if (!ad || !a) continue;
      const anahtar = ad.toLocaleLowerCase('tr');
      if (t.k === 'kisaltma') { if (!kis.has(anahtar)) kis.set(anahtar, `- **${ad}**${t.acilim ? ` (${t.acilim.trim()})` : ''}: ${a}`); }
      else if (!terim.has(anahtar)) terim.set(anahtar, `- **${ad}:** ${a}${t.k === 'karisan' && t.f ? ` *${t.f.trim()} ile karıştırılır.*` : ''}`);
    }
  }
  const sat = (m: Map<string, string>) => [...m.entries()].sort((x, y) => trSirala(x[0], y[0])).map((x) => x[1]);
  const out: string[] = [];
  if (terim.size) out.push('### Terimler', ...sat(terim));
  if (kis.size) out.push('### Kısaltmalar', ...sat(kis));
  return out.join('\n');
}

/** Ek: doğrulanmış çıkmış sorular (anlatım sırasıyla), kökü ve cevabıyla */
function cikmisMd(detay: CdDetay): string {
  const gorulen = new Set<string>();
  return (detay.cikmisKonum || [])
    .filter((c) => c.dogrulandi && c.kok?.trim() && !gorulen.has(c.id) && gorulen.add(c.id))
    .sort((a, b) => a.p - b.p || a.c - b.c)
    .map((c, i) => `${i + 1}. ${tekSatir(c.kok)}${c.yil ? ` *(${c.yil})*` : ''}${c.cevap?.trim() ? `\n  - **Cevap:** ${tekSatir(c.cevap)}` : ''}`)
    .join('\n');
}

/** basliklar verilirse her paragrafın eşlendiği slaytın başlığı, değiştiği yerde alt başlık (###) olarak girer. */
/** Ara resimler (araResimVeri) bağlı oldukları paragraf aralığının sonuna (bitis paragrafından sonra) resim bloğu olarak girer;
 *  bitis paragrafı boşsa ya da yoksa aralıktan sonraki ilk paragraftan önce, en geç belge sonunda.
 *  secenek: eski çağrılar için boolean (önemli yer işaretleri açık/kapalı) da kabul edilir. bolumSecim: yalnız bu bölüm dizinleri. */
export function cdAktarBelgesi(detay: CdDetay, etiket: string, secenek: boolean | Partial<CdAktarSecenek> = true, basliklar?: SlaytBasliklari, bolumSecim?: ReadonlySet<number>): AktarBelge {
  const S: CdAktarSecenek = { ...CD_AKTAR_VARSAYILAN, ...(typeof secenek === 'boolean' ? { vurgu: secenek } : secenek) };
  const ozet = S.kapsam === 'onemli';
  const kalan: AraResim[] = S.resimler && !ozet ? [...araResimleri(detay.key)].sort((a, b) => araResimBitis(a) - araResimBitis(b)) : [];
  const resimMd = (r: AraResim) => resimSatiri(r.baslik, araResimYolu(r), r.aciklama || '');
  /** i'ye kadar (dahil) aralığı biten resimler */
  const al = (i: number) => {
    const out: string[] = [];
    while (kalan.length && araResimBitis(kalan[0]) <= i) out.push(resimMd(kalan.shift()!));
    return out;
  };
  /** Paragrafın işaretli hâli: özet için önemli cümle işareti her zaman konur (süzmek için), istenmiyorsa sonra silinir */
  const isaretli = (p: { i: number; metin: string }) => {
    const v = (detay.vurgu?.[p.i] || []).filter((x) => (x[2] === 'c' ? S.vurgu || ozet : S.terim));
    return ekranYazimi(tekSatir(vurgula(p.metin, v)));
  };
  const govdeYaz = (p: { i: number; metin: string }): string => {
    const t = isaretli(p);
    if (ozet) {
      const sec = cumleler(t).filter((c) => c.includes('=='));
      const sat = sec.map((c) => `- ${S.vurgu ? c : c.replace(/==/g, '')}`).join('\n');
      return S.uslup === 'not' ? konusmaRedakte(sat) : sat;
    }
    return S.uslup === 'not' ? konusmaRedakte(paragrafMd(t)) : t;
  };
  const secili = detay.bolumler.map((b, bi) => ({ b, bi })).filter(({ bi }) => !bolumSecim || bolumSecim.has(bi));
  const bolumler = secili.map(({ b }, sira) => {
    let onceki = katla(b.baslik);
    const satirlar = b.paragraflar.filter((p) => p.metin.trim())
      .map((p) => {
        const once = al(p.i - 1);
        const govde = govdeYaz(p);
        const e = basliklar && detay.pdf?.paragraflar?.[p.i];
        const sb = e ? basliklar!.get(`${e.dosya}:${e.sayfa}`) : undefined;
        const sonra = al(p.i);
        if (!govde.trim()) return [...once, ...sonra].join('\n');
        const ek = (g: string) => [...once, g, ...sonra].join('\n');
        if (!sb || katla(sb) === onceki) return ek(govde);
        onceki = katla(sb);
        return ek(`### ${sb}\n${govde}`);
      }).filter(Boolean);
    // bölüm seçimi yokken artan resimler belge sonuna; seçim varken seçilmeyen bölümlerin resimleri girmez
    if (!bolumSecim && sira === secili.length - 1) satirlar.push(...al(Infinity));
    return { baslik: b.baslik.trim(), md: satirlar.join(S.uslup === 'konusma' && !ozet ? '\n\n' : '\n') };
  }).filter((b) => b.md.trim());
  if (S.sozluk) { const m = sozlukMd(detay); if (m) bolumler.push({ baslik: 'Terimler ve kısaltmalar', md: m }); }
  if (S.cikmis) { const m = cikmisMd(detay); if (m) bolumler.push({ baslik: 'Bu dersten çıkmış sorular', md: m }); }
  const isaretNotu = S.vurgu && detay.vurgu ? ' · işaretli yerler çıkmış, örnek soru ve spotlarla eşleşen önemli bilgiler' : '';
  return {
    baslik: detay.baslik,
    dersDuzeni: true,
    alt: `${etiket} · ${ozet ? 'Sesli ders · önemli yerler özeti' : S.uslup === 'konusma' ? 'Sesli ders konuşma metni' : 'Sesli ders metni'}${isaretNotu}`,
    bolumler,
  };
}
