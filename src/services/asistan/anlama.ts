/**
 * Tıp Asistanı — anlama katmanı (F2, 2026-10-29). LLM yok: kural + ağırlık; varlık/yazım düzeltme mevcut queryIntel'den gelir.
 *
 * anla("nistatinin yan etkileri neler") → { ana: 'yan_etki', varliklar: [nistatin], filtre: {...}, ... }
 * Yeni niyet eklemek: NIYET_KURALLARI'na satır + scripts/asistan/sinama/ içine örnek (kapı: scripts/asistan/anlama_sinama.mts).
 */
import { fold } from '../queryIntel/core';
import type { ConceptHit } from '../queryIntel/engine';
import { analyzeFor } from '../queryIntel/server';

export type Niyet =
  | 'tanim' | 'etiyoloji' | 'patogenez' | 'belirti' | 'tani' | 'laboratuvar' | 'goruntuleme' | 'ayirici_tani' | 'tedavi'
  | 'komplikasyon' | 'prognoz' | 'sayi' | 'ilac_mekanizma' | 'endikasyon' | 'kontrendikasyon' | 'yan_etki' | 'etkilesim' | 'doz'
  | 'karsilastir' | 'kisaltma' | 'cikmis_soru' | 'ornek_soru' | 'git' | 'ses_cal' | 'goster' | 'tablo'
  | 'site_yardim' | 'calisma_onerisi' | 'selam' | 'tesekkur' | 'veda' | 'bilinmiyor';

/** Sözcük başı eşleşmesi (ek alır): p('tedavi') → "tedavi", "tedavisi", "tedavide". */
const p = (s: string) => `(?:^| )${s}`;
/** Tam sözcük */
const k = (s: string) => `(?:^| )${s}(?: |$)`;

interface Kural { n: Niyet; re: RegExp; w: number }
const kural = (n: Niyet, w: number, ...kalip: string[]): Kural => ({ n, w, re: new RegExp(kalip.join('|')) });

export const NIYET_KURALLARI: Kural[] = [
  // — sohbet —
  kural('selam', 3, k('merhaba'), p('selam'), k('slm'), p('gunaydin'), p('iyi gunler'), p('iyi aksamlar'), k('naber'), p('nasilsin'), k('hey'), k('mrb')),
  kural('tesekkur', 3, p('tesekkur'), p('sag ?ol'), p('eyvallah'), k('saol'), p('cok iyi'), p('harika')),
  kural('veda', 3, p('gorusuruz'), p('hosca ?kal'), p('iyi geceler'), k('bay bay'), p('kolay gelsin')),
  // — site eylemleri —
  kural('git', 3.6, k('git'), p('gotur'), p('acar misin'), p('aciver'), p('acsana'), p('nerede'), p('nereden'), p('nasil giderim'), p('nasil ulas'), p('nasil bulur'), p('yonlendir'), p('sayfasi'), p('sayfasina'), p('ekrani'), p('ekranina'), p('menu'), p('kisayol'), p('gecis yap')),
  kural('git', 3.0, k('ac'), k('gec'), p('bolumune'), p('bolumu')),
  kural('ses_cal', 3.4, p('sesli'), p('sesini'), p('seslendir'), p('dinle'), p('oku bana'), p('anlat bana'), k('cal'), p('oynat'), p('calsana'), p('ses ac')),
  kural('goster', 3.2, p('resim'), p('gorsel'), p('sekil'), p('cizim'), p('diyagram'), p('foto'), k('mikroskop'), p('mikroskop goruntu'), p('animasyon'), p('resmini'), p('goster'), p('gostersene'), p('gorebilir')),
  kural('goster', 2.7, k('sema'), p('semasi')),  // tedavi/tanı şeması bilgi sorusu olabilir: bilgi niyetleri (2.8) önde
  kural('tablo', 3.3, p('tablo'), p('liste'), p('siralama')),
  kural('karsilastir', 3.1, p('fark'), p('karsilastir'), p('ayirt'), k('vs'), p('mi yoksa'), p('arasinda'), p('hangisi daha'), p('benzerlik')),
  kural('kisaltma', 3.2, p('kisaltma'), p('acilimi'), p('acilim'), p('uzun hali'), p('neyin kisaltma')),
  // — sorular —
  kural('cikmis_soru', 3.4, p('cikmis'), p('gecmis sinav'), p('onceki yillar'), p('cikti mi'), p('cikar mi'), p('sorulmus'), p('sorulur mu'), p('sorulmuslar'), p('kac kez cik'), p('sinavda cik'), p('kac yil'), p('hangi yil'), p('daha once sor')),
  kural('ornek_soru', 3.3, p('ornek soru'), `(?:^| )soru (?:sor|ver|getir|uret|olsun)`, `(?:^| )sorular?\\w* (?:getir|ver|sor|uret|olsun|coz|var mi)`, `(?:^| )sor\\w* (?:ver|getir)`, p('bana soru'), p('soru coz'), `(?:^| )test\\w* coz`, `(?:^| )soru\\w* coz`, p('mini sinav'), p('deneme'), p('quiz'), p('beni sina'), p('soru olsun'), p('soru var mi'), p('pratik'), p('sorular')),
  // — site yardımı —
  kural('site_yardim', 2.6, p('nasil kullan'), p('ne ise yar'), p('bu site'), p('uygulama'), p('kayit ol'), p('giris yap'), p('hesab'), p('hesap'), p('profil'), p('ayarlar'), p('sifre'), p('atp puan'), p('atp kazan'), p('basarim'), p('puan'), p('favori'), p('not al'), p('cevrimdisi'), p('karanlik'), p('tema'), p('bildirim'), p('hata bildir'), p('iletisim'), p('premium'), p('ucret')),
  kural('calisma_onerisi', 3.7, p('ne calis'), p('calisma plan'), p('tekrar et'), p('hangi konu'), p('nereden basla'), p('zayif konu'), p('eksik konu'), p('eksiklerim'), p('zayif yer'), p('bugun ne'), p('tavsiye'), p('oner'), p('program yap')),
  // — ilaç —
  kural('yan_etki', 3, p('yan etki'), p('advers'), p('toksisite'), p('toksik'), p('istenmeyen'), p('zarar')),
  kural('kontrendikasyon', 3, p('kontrendik'), p('kullanilmaz'), p('verilmez'), p('kimlere verilme'), p('kullanilamaz'), p('yasak')),
  kural('endikasyon', 3, p('endikasyon'), p('ne icin kullan'), p('ne zaman kullan'), p('kullanim alan')),
  kural('etkilesim', 3, p('etkiles'), p('birlikte kullan'), p('beraber'), p('birlikte verilir')),
  kural('doz', 3, p('doz'), k('mg'), p('kac mg'), p('kullanim sekli'), p('veriliş yolu'), p('verilis yolu'), p('ne kadar verilir'), p('kac gun kullan')),
  kural('ilac_mekanizma', 3.1, p('etki mekanizma'), p('nasil etki'), p('ne yapar'), p('ne yapiyor'), p('nasil etkili'), p('nasil calis'), p('hedefi'), p('inhibe')),
  // — bilgi —
  kural('sayi', 2.8, p('kac'), p('yuzde'), p('yuzdesi'), p('oran'), p('siklik'), p('siklig'), p('sik gorul'), p('insidans'), p('prevalans'), p('sayi'), p('kac yas'), p('%'), p('ortalama')),
  kural('tedavi', 2.8, p('tedavi'), p('ampirik'), p('ilk ne yap'), p('ne verilir'), p('uygulan'), p('yonetim'), p('yaklasim'), p('ilac tedavi'), p('cerrahi'), p('ilk basamak'), p('secim'), p('ilk tercih')),
  kural('tani', 2.8, `(?:^| )tani(?!m)`, p('nasil konur'), p('kriter'), p('altin standart'), p('gold standart'), p('biyopsi'), p('tetkik'), p('hangi test'), p('ne istenir'), p('teshis'), p('konfirm')),
  kural('belirti', 2.8, p('belirti'), p('bulgu'), p('semptom'), p('klinik'), p('yakinma'), p('nasil anlas'), p('seyreder'), p('gorulur'), p('kendini gosterir'), p('sikayet'), p('tablo ile')),
  kural('goruntuleme', 3.0, p('goruntuleme'), p('radyoloji'), k('bt'), k('mr'), k('mri'), k('usg'), p('ultrason'), p('rontgen'), k('ekg'), p('grafi'), p('tomografi'), p('sintigrafi'), p('ekokardiyo')),
  kural('laboratuvar', 3.0, p('laboratuvar'), k('lab'), p('kan deger'), p('referans'), p('normal deger'), p('duzey'), p('seviye'), p('yuksekligi'), p('dusuklugu'), p('kanda')),
  kural('etiyoloji', 2.8, p('etiyoloji'), p('neden olur'), p('nedeni'), p('nedenleri'), p('sebep'), p('sebeb'), p('risk faktor'), p('yol acar'), p('sorumlu'), p('etken'), p('niye'), p('neden')),
  kural('patogenez', 3.0, p('patogenez'), p('nasil gelisir'), p('nasil olusur'), p('fizyopatoloji'), p('patofizyoloji'), p('morfoloji'), p('histoloji'), p('histopatoloji'), p('makroskopik'), p('mikroskopik'), p('mekanizma'), p('patoloji'), p('gelisim'), p('nasil ol'), p('ortaya cik'), p('nasil ortaya'), p('nasil ciktig')),
  kural('ayirici_tani', 3.5, p('ayirici'), p('karisir'), p('benzer hastalik'), p('ayirt etmek'), p('ayirici tani')),
  kural('komplikasyon', 2.9, p('komplikasyon'), p('sonuc'), p('sorun'), p('yol acar mi'), p('ne olur')),
  kural('prognoz', 2.9, p('prognoz'), p('seyir'), p('seyri'), p('gidis'), p('sag ?kalim'), p('mortalite'), p('iyilesir mi'), p('ongor')),
  kural('tanim', 1.6, k('nedir'), p('ne demek'), p('tanim'), k('kimdir'), p('ne anlama'), p('acikla'), p('hakkinda'), p('ilgili'), p('soyle'), p('bilgi'), p('bilgi ver'), p('anlat'), p('bahset'), p('ozet'), p('kavram')),
];

/** Sorgudan çıkarılan süzgeçler (F3 aramada kullanır) */
export interface Filtre { kurul?: number; yil?: string; brans?: string }
const BRANS: Array<[string, RegExp]> = [
  ['patoloji', /(?:^| )patoloji/], ['farmakoloji', /(?:^| )farmakoloji/], ['enfeksiyon', /(?:^| )enfeksiyon/],
  ['uroloji', /(?:^| )uroloji/], ['genetik', /(?:^| )(?:genetik|tbg)/], ['halk-sagligi', /(?:^| )halk sagligi/],
  ['kadin-dogum', /(?:^| )(?:kadin dogum|jinekoloji|obstetrik)/], ['noroloji', /(?:^| )noroloji/],
];

export interface Anlama {
  soru: string;
  /** Yazım düzeltilmişse düzeltilmiş hali, değilse null */
  duzeltilmis: string | null;
  /** Niyet kararında kullanılan katlanmış metin */
  temiz: string;
  niyetler: Array<{ n: Niyet; p: number }>;
  ana: Niyet;
  /** Ana niyete yakın (≥%60) ikinci niyetler */
  ikincil: Niyet[];
  varliklar: ConceptHit[];
  odak: string[];
  filtre: Filtre;
  /** Varlık yok ve niyet zayıf: netleştirme sorusu gerekir */
  belirsiz: boolean;
}

export function niyetPuanla(temiz: string, ilacVar: boolean, varlikVar: boolean): Array<{ n: Niyet; p: number }> {
  const puan = new Map<Niyet, number>();
  for (const r of NIYET_KURALLARI) if (r.re.test(temiz)) puan.set(r.n, Math.max(puan.get(r.n) || 0, r.w));
  // bağlam düzeltmeleri
  if (puan.has('ilac_mekanizma') === false && ilacVar && puan.has('patogenez') && /mekanizma/.test(temiz)) puan.set('ilac_mekanizma', 3.3);
  if (ilacVar && puan.get('tedavi') && !puan.has('doz') && /(?:^| )ilac(?:lar)? (?:ne|nedir|hangi)/.test(temiz)) puan.delete('tedavi');
  if (puan.has('tanim') && puan.size > 1) puan.set('tanim', 0.8);
  // ilaç bağlamı: "X ne işe yarar / hangi hastalıkta" endikasyon; "gebelikte X verilir mi" kontrendikasyon
  if (ilacVar && /(?:^| )(?:ne ise yar|hangi hastalik)/.test(temiz)) puan.set('endikasyon', 3);
  if (ilacVar && /(?:^| )(?:verilir|kullanilir) mi/.test(temiz) && !puan.has('etkilesim')) puan.set('kontrendikasyon', 2.9);
  if (ilacVar && /hangi \w+ (?:kullanilir|verilir)/.test(temiz)) puan.set('endikasyon', 3);
  // tıbbi varlık yokken site sözcükleri ("puanlar nasıl çalışıyor") ilaç/bilgi kalıplarını bastırır
  if (!varlikVar && puan.has('site_yardim')) puan.set('site_yardim', 3.5);
  return [...puan].map(([n, pu]) => ({ n, p: pu })).sort((a, b) => b.p - a.p);
}

export function filtreCikar(temiz: string): Filtre {
  const f: Filtre = {};
  const km = /kurul ?([1-6])(?: |$)/.exec(temiz) || /(?:^| )([1-6]) ?\.? ?kurul/.exec(temiz);
  if (km) f.kurul = Number(km[1]);
  const ym = /(?:^| )(20\d\d)(?: ?[-/ ] ?(20\d\d|\d\d))?(?: |$)/.exec(temiz);
  if (ym) f.yil = ym[2] ? `${ym[1]}-${ym[2].length === 2 ? ym[1].slice(0, 2) + ym[2] : ym[2]}` : ym[1];
  for (const [b, re] of BRANS) if (re.test(temiz)) { f.brans = b; break; }
  return f;
}

export function anla(soru: string): Anlama {
  const q = (soru || '').slice(0, 500);
  const u = analyzeFor(q);
  const metin = u.corrected ?? q;
  const temiz = ' ' + fold(metin).replace(/[^a-z0-9%]+/g, ' ').trim() + ' ';
  const t = temiz.trim();
  const ilacVar = u.concepts.some(c => c.type === 'drug');
  // yazım düzeltme sohbet sözcüklerini bozabilir ("selam"→?): niyet iki metinden de aranır, kural başına en yüksek puan alınır
  const orijinal = fold(q).replace(/[^a-z0-9%]+/g, ' ').trim();
  const birlesik = new Map<Niyet, number>();
  for (const m of new Set([t, orijinal])) for (const x of niyetPuanla(m, ilacVar, u.concepts.length > 0)) birlesik.set(x.n, Math.max(birlesik.get(x.n) || 0, x.p));
  const niyetler = [...birlesik].map(([n, pu]) => ({ n, p: pu })).sort((a, b) => b.p - a.p);
  // yalın terim ("anosmi", "nistatin", "ACTH") bir arama isteğidir: niyet yoksa tanım/bilgi aranır
  const ana: Niyet = niyetler[0]?.n ?? (u.concepts.length || /[a-z0-9]{2,}/.test(t) ? 'tanim' : 'bilinmiyor');
  const ust = niyetler[0]?.p ?? 0;
  const ikincil = niyetler.slice(1).filter(x => x.p >= 0.6 * ust && x.n !== 'tanim').slice(0, 2).map(x => x.n);
  return {
    soru: q, duzeltilmis: u.corrected, temiz: t, niyetler, ana, ikincil, varliklar: u.concepts, odak: u.focus,
    filtre: filtreCikar(t), belirsiz: !u.concepts.length && ust < 2.6,
  };
}
