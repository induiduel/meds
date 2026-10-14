import type React from 'react';
import {
  Baby, Building2, Bug, Factory, HeartPulse, LayoutDashboard, LineChart, MapPin, ScanSearch, Syringe, Users,
} from 'lucide-react';

/**
 * Sağlık Bakanlığı sekmesi (/saglik) — veri türleri, bölüm listesi ve yükleyiciler.
 * Veri: src/data/saglik/*.json (scripts/saglik/birlestir.py resmî kaynaklı araştırma çıktısından yazar,
 * scripts/saglik/baglantilari_kur.py ders bağlarını üretir). Her sayı bir `kaynak` kimliği taşır; kaynak yoksa gösterilmez.
 */

export type BolumId =
  | 'genel' | 'karabuk' | 'asi' | 'yenidogan' | 'anne_kadin' | 'tarama' | 'salgin' | 'cevre' | 'kurumlar' | 'istatistik' | 'halk_sagligi';

export interface BolumTanim {
  id: BolumId;
  slug: string;
  ad: string;
  kisa: string;
  aciklama: string;
  icon: React.ElementType;
}

export const BOLUMLER: BolumTanim[] = [
  { id: 'genel', slug: '', ad: 'Genel bakış', kisa: 'Genel', aciklama: 'Türkiye ve Karabük için kilit göstergeler, bölümler ve sınavda en çok sorulan konular.', icon: LayoutDashboard },
  { id: 'karabuk', slug: 'karabuk', ad: 'Karabük', kisa: 'Karabük', aciklama: 'İlin nüfusu, sağlık kurumları, aile hekimliği, il göstergeleri ve çevre sağlığı.', icon: MapPin },
  { id: 'asi', slug: 'asi', ad: 'Aşı', kisa: 'Aşı', aciklama: 'Genişletilmiş Bağışıklama Programı: aşı takvimi, aşılama hızları ve aşı ile önlenebilir hastalıklar.', icon: Syringe },
  { id: 'yenidogan', slug: 'yenidogan', ad: 'Yenidoğan', kisa: 'Yenidoğan', aciklama: 'Ulusal yenidoğan taramaları, bebek-çocuk izlemi, destek programları ve bebek ölüm göstergeleri.', icon: Baby },
  { id: 'anne_kadin', slug: 'anne-kadin', ad: 'Kadın / Anne Sağlığı', kisa: 'Anne-Kadın', aciklama: 'Doğum öncesi bakım, gebe ve lohusa izlemi, anne ölümü, doğurganlık ve üreme sağlığı.', icon: HeartPulse },
  { id: 'tarama', slug: 'tarama', ad: 'Erken teşhis', kisa: 'Tarama', aciklama: 'Kanser taramaları (KETEM), prenatal ve yenidoğan taramaları, tarama testinin geçerliliği.', icon: ScanSearch },
  { id: 'salgin', slug: 'salgin', ad: 'Salgın hastalıklar', kisa: 'Salgın', aciklama: 'Bildirimi zorunlu hastalıklar, sürveyans, salgın incelemesi ve güncel bulaşıcı hastalık verileri.', icon: Bug },
  { id: 'cevre', slug: 'cevre', ad: 'Çevre ve sağlık', kisa: 'Çevre', aciklama: 'İçme suyu ve hava kalitesi standartları, Karabük hava kalitesi, iş kazası ve meslek hastalıkları.', icon: Factory },
  { id: 'kurumlar', slug: 'kurumlar', ad: 'Sağlık kurumları', kisa: 'Kurumlar', aciklama: 'Basamaklar, kurum ve insan gücü sayıları, sevk zinciri ve Türkiye sağlık örgütlenmesinin tarihçesi.', icon: Building2 },
  { id: 'istatistik', slug: 'istatistik', ad: 'İstatistikler', kisa: 'İstatistik', aciklama: 'Sağlık göstergelerinin tanımı, formülü ve Türkiye seyri; gösterge hesaplayıcı ve ölüm nedenleri.', icon: LineChart },
  { id: 'halk_sagligi', slug: 'halk-sagligi', ad: 'Halk sağlığı', kisa: 'Halk sağlığı', aciklama: 'Halk sağlığı müfredat haritası, temel sağlık hizmetleri ve Türkiye halk sağlığı tarihçesi.', icon: Users },
];

export const bolumBySlug = (slug?: string): BolumTanim =>
  BOLUMLER.find((b) => b.slug === (slug || '')) || BOLUMLER[0];

// ---------------------------------------------------------------------------------------------------------------
// Veri türleri (alanlar araştırma şemasından; hepsi isteğe bağlı — eksik alan bileşende atlanır)
// ---------------------------------------------------------------------------------------------------------------

export interface Kaynak { id: string; kurum: string; belge: string; yil?: number | string; url: string; erisim?: string; not?: string }
export interface SeriNokta { yil: number | string; deger: number }
export interface Formul { pay?: string; payda?: string; katsayi?: number }
export interface Gosterge {
  kod?: string; ad: string; birim?: string; tanim?: string; formul?: Formul; seri?: SeriNokta[];
  deger?: number | string; yil?: number | string; turkiye?: number | string; kaynak?: string; ek_kaynaklar?: string[]; konum?: string;
}
export interface Madde { madde?: string; ad?: string; deger?: number | string; birim?: string; not?: string; yil?: number | string; kaynak?: string; konum?: string }

export interface AsiVeri {
  dogrulanamayan?: string[];
  takvim_zamanlari?: { id: string; etiket: string; ay: number; not?: string }[];
  takvim?: { id: string; ad: string; kisa: string; hastaliklar?: string[]; tur?: string; yol?: string; dozlar: { zaman: string; doz: string }[]; not?: string; kaynak?: string; ek_kaynaklar?: string[] }[];
  gebe_eriskin?: { baslik: string; maddeler: string[]; kaynak?: string }[];
  oranlar?: { birim?: string; tanim?: string; not?: string; kaynak?: string; konum?: string; seriler?: { asi: string; kisa?: string; not?: string; degerler: (SeriNokta & { kaynak?: string; konum?: string })[] }[] };
  hastaliklar?: { ad: string; etken?: string; asi?: string; bulas?: string; turkiye?: string; vaka?: { yil: number | string | null; donem?: string; sayi: number; kaynak?: string; konum?: string; not?: string }[]; kaynak?: string; ek_kaynaklar?: string[] }[];
  kilometre_taslari?: { yil: number | string; olay: string; kaynak?: string }[];
  soguk_zincir?: Madde[];
  genel_kurallar?: Madde[];
}

export interface AnneVeri {
  dogrulanamayan?: string[];
  dob_izlemleri?: { no: number; zaman: string; hafta_bas?: number; hafta_son?: number; icerik?: string[]; kaynak?: string }[];
  tehlike_isaretleri?: { maddeler: string[]; acil_sevk_kriterleri?: string[]; kaynak?: string; konum?: string };
  lohusa_izlemleri?: { no: number; zaman: string; icerik?: string[]; kaynak?: string }[];
  bebek_cocuk_izlemleri?: { zaman: string; ay?: number; icerik?: string[]; kaynak?: string }[];
  yenidogan_taramalari?: { id: string; ad: string; grup?: string; baslangic?: number | string; zaman?: string; yontem?: string; not?: string; kaynak?: string; ek_kaynaklar?: string[] }[];
  destek_programlari?: { ad: string; hedef?: string; doz?: string; baslangic?: string; bitis?: string; kaynak?: string }[];
  gostergeler?: Gosterge[];
  ureme_sagligi?: { ad: string; deger: number | string; yil?: number | string; kaynak?: string; konum?: string; ek_kaynaklar?: string[] }[];
  evlilik_oncesi?: { maddeler: string[]; kaynak?: string };
  programlar?: { ad: string; aciklama: string; kaynak?: string }[];
  kanser_taramalari?: { kanser: string; hedef: string; yontem: string; aralik: string; not?: string; kaynak?: string }[];
  ketem?: { sayi?: number; yil?: number | string; kaynak?: string; konum?: string; detay?: string; not?: string; seri?: SeriNokta[] };
}

export interface KarabukVeri {
  dogrulanamayan?: string[];
  nufus?: { toplam?: number; yil?: number | string; kaynak?: string; ilceler?: { ad: string; nufus: number }[]; yas_65_ustu_orani?: { deger: number; yil?: number | string; kaynak?: string } };
  gostergeler?: Gosterge[];
  kurum_sayilari?: { tur: string; sayi: number; yil?: number | string; yontem?: string; not?: string; adlar?: string[]; kaynak?: string; konum?: string }[];
  hastaneler?: { ad: string; ilce?: string; tur?: string; not?: string; url?: string; kaynak?: string }[];
  ilceler?: { ad: string; nufus?: number; asm?: number; asm_adlari?: string[]; aile_hekimi_birimi?: number; ahb_basina_nufus?: number; hastane?: string; kaynak?: string; ek_kaynaklar?: string[] }[];
  birimler?: { ad: string; adres_ilce?: string; aciklama?: string; kaynak?: string }[];
  cevre?: { baslik: string; deger?: number | string; birim?: string; yil?: number | string; istasyon?: string; aciklama?: string; kaynak?: string }[];
  is_sagligi?: { ad: string; deger: number | string; yil?: number | string; aciklama?: string; kaynak?: string; konum?: string }[];
  programlar?: { ad: string; aciklama: string; tarih?: string; kaynak?: string }[];
  universite?: { aciklama: string; kaynak?: string; ek_kaynaklar?: string[] };
}

export interface TurkiyeVeri {
  dogrulanamayan?: string[];
  gostergeler?: Gosterge[];
  olum_nedenleri?: {
    yil?: number | string; kaynak?: string; konum?: string;
    kalemler?: { ad: string; yuzde: number; onceki?: { yil: number | string; yuzde: number }; alt?: string }[];
    ilk_uc_seri?: { yil: number; dolasim?: number; tumor?: number; solunum?: number; kaynak?: string }[];
  };
  kurumlar?: { ad: string; seri?: SeriNokta[]; alt?: { ad: string; deger: number }[]; kaynak?: string; konum?: string }[];
  insan_gucu?: { ad: string; seri?: SeriNokta[]; kaynak?: string; konum?: string }[];
  basamaklar?: { basamak: string; kurumlar?: string[]; aciklama?: string; kaynak?: string }[];
  tarihce?: { yil: number | string; olay: string; kaynak?: string }[];
  bildirimi_zorunlu?: {
    yonetmelik?: string; kaynak?: string; not?: string; genel_kurallar?: string[];
    guncel_liste?: { aciklama?: string; sayi?: number; hastaliklar: string[] };
    gruplar?: { grup: string; kural?: string; hastaliklar: string[] }[]; gruplar_kaynak?: string; gruplar_konum?: string;
  };
  surveyans?: { tur: string; tanim: string; kaynak?: string }[];
  salgin_inceleme_basamaklari?: { no: number; adim: string; kaynak?: string }[];
  bulasici_veriler?: { hastalik: string; olcu?: string; seri?: SeriNokta[]; olum?: SeriNokta[]; insidans_100bin?: SeriNokta[]; ozet?: string; not?: string; kaynak?: string; konum?: string; ek_kaynaklar?: string[] }[];
  cevre?: { baslik: string; maddeler?: Madde[]; kaynak?: string }[];
  is_sagligi?: { ad: string; seri?: SeriNokta[]; kaynak?: string; konum?: string }[];
}

export interface BaglantiDeste { id: string; baslik: string; kisa: string; ders: string; kurul: string; hoca?: string; slayt: number; pdf: boolean; ozet?: string; ek?: boolean }
export interface BaglantiCapa { deste: string; kisa: string; slayt: number; baslik: string }
export interface BaglantiKazanim { kurul: number; ders: string; konu: string; anahtar: string; kazanimlar: { id: string; metin: string }[]; cikmis: number }
export interface BaglantiSpot { id: string; baslik: string; spot: string; onem: number; ders: string }
export interface BolumBaglanti {
  konular: string[];
  soru_sayisi: number;
  havuz: number;
  yillar: Record<string, number>;
  konu_dagilimi: Record<string, number>;
  kurul_dagilimi: Record<string, number>;
  kazanimlar: BaglantiKazanim[];
  desteler: BaglantiDeste[];
  capalar: Record<string, BaglantiCapa[]>;
  spotlar: BaglantiSpot[];
}
export interface MufredatKonu { kurul: number; ders: string; konu: string; anahtar: string; kazanim: number; cikmis: number; deste?: string }
export interface Baglantilar { uretildi: string; bolumler: Partial<Record<BolumId, BolumBaglanti>>; mufredat?: MufredatKonu[] }

export interface SinavSorusu {
  id: string; kok: string; secenekler: { k: string; t: string }[]; dogru: string; aciklama?: string;
  yil?: string; kurul?: number | null; ders?: string; konu?: string;
}

export interface SaglikVeri {
  kaynaklar: Record<string, Kaynak>;
  asi: AsiVeri;
  anne: AnneVeri;
  karabuk: KarabukVeri;
  turkiye: TurkiyeVeri;
  baglantilar: Baglantilar;
  guncelleme?: string;
}

const def = <T,>(m: { default?: T } | T): T => ((m as { default?: T }).default ?? m) as T;

let yukP: Promise<SaglikVeri> | null = null;
/** Tüm bölüm verisi (birlikte ~yüz KB'lar). Bir kez yüklenir. */
export function saglikVeriYukle(): Promise<SaglikVeri> {
  if (!yukP) {
    yukP = Promise.all([
      import('../../data/saglik/kaynaklar.json'),
      import('../../data/saglik/asi.json'),
      import('../../data/saglik/anne_yenidogan.json'),
      import('../../data/saglik/karabuk.json'),
      import('../../data/saglik/turkiye.json'),
      import('../../data/saglik/baglantilar.json'),
    ]).then(([k, a, an, kb, t, b]) => {
      const kaynakDosya = def(k) as unknown as { guncelleme?: string; kaynaklar: Kaynak[] };
      const kaynaklar: Record<string, Kaynak> = {};
      for (const x of kaynakDosya.kaynaklar || []) kaynaklar[x.id] = x;
      return {
        kaynaklar,
        guncelleme: kaynakDosya.guncelleme,
        asi: def(a) as unknown as AsiVeri,
        anne: def(an) as unknown as AnneVeri,
        karabuk: def(kb) as unknown as KarabukVeri,
        turkiye: def(t) as unknown as TurkiyeVeri,
        baglantilar: def(b) as unknown as Baglantilar,
      };
    }).catch((e) => { yukP = null; throw e; });
  }
  return yukP;
}

const soruP = new Map<BolumId, Promise<SinavSorusu[]>>();
/** "Kendini sına" soruları — bölüm açılınca tembel yüklenir */
export function bolumSorulari(b: BolumId): Promise<SinavSorusu[]> {
  let p = soruP.get(b);
  if (!p) {
    p = import(`../../data/saglik/sorular/${b}.json`)
      .then((m) => def(m) as unknown as SinavSorusu[])
      .catch(() => { soruP.delete(b); return [] as SinavSorusu[]; });
    soruP.set(b, p);
  }
  return p;
}

// ---------------------------------------------------------------------------------------------------------------
// Yardımcılar
// ---------------------------------------------------------------------------------------------------------------

export const sayi = (n: number | string | undefined | null, basamak?: number): string => {
  if (n == null || n === '') return '—';
  if (typeof n === 'string') return n;
  const b = basamak ?? (Math.abs(n) < 10 && !Number.isInteger(n) ? 1 : Number.isInteger(n) ? 0 : 1);
  return n.toLocaleString('tr-TR', { minimumFractionDigits: b, maximumFractionDigits: Math.max(b, 2) });
};

/** Bir veri ağacındaki tüm `kaynak` kimliklerini görülme sırasıyla toplar (bölüm kaynakçası için) */
export function kaynaklariTopla(...kokler: unknown[]): string[] {
  const out: string[] = [];
  const gor = new Set<string>();
  const yuru = (x: unknown) => {
    if (!x || typeof x !== 'object') return;
    if (Array.isArray(x)) { x.forEach(yuru); return; }
    const o = x as Record<string, unknown>;
    if (typeof o.kaynak === 'string' && !gor.has(o.kaynak)) { gor.add(o.kaynak); out.push(o.kaynak); }
    if (Array.isArray(o.ek_kaynaklar)) for (const e of o.ek_kaynaklar) if (typeof e === 'string' && !gor.has(e)) { gor.add(e); out.push(e); }
    for (const v of Object.values(o)) if (v && typeof v === 'object') yuru(v);
  };
  kokler.forEach(yuru);
  return out;
}

export const sonDeger = (g?: { seri?: SeriNokta[]; deger?: number | string; yil?: number | string }) => {
  if (!g) return null;
  if (g.seri?.length) {
    const s = [...g.seri].filter((x) => /^\d{4}$/.test(String(x.yil)) && typeof x.deger === 'number').sort((a, b) => Number(a.yil) - Number(b.yil));
    if (!s.length) return null;
    return { deger: s[s.length - 1].deger, yil: s[s.length - 1].yil, onceki: s.length > 1 ? s[s.length - 2] : undefined };
  }
  if (g.deger != null) return { deger: g.deger, yil: g.yil, onceki: undefined };
  return null;
};

/** Göstergeyi ada ya da koda göre bul (kaynaklar farklı adlandırabilir) */
export const gostergeBul = (liste: Gosterge[] | undefined, ...desenler: RegExp[]): Gosterge | undefined =>
  (liste || []).find((g) => desenler.some((d) => d.test(`${g.kod || ''} ${g.ad}`)));

export const kucukHarf = (s: string) => s.toLocaleLowerCase('tr-TR');
