/**
 * Taş Masası (Oyunlar › okey taşlı oyunlar + Uno) — ortak sözleşme. İstemci, sunucu, motorlar ve botlar YALNIZ bu türlerle konuşur.
 *
 * Katmanlar:
 *   motor/<oyun>.ts   saf kural motoru (yan etkisiz, JSON durum). Sunucu yetkilidir; istemci aynı saf işlevleri ipucu için kullanır.
 *   sunucu.ts         /api/masa/ws oda yöneticisi (motordan bağımsız), kalıcılık (meds-pg), istatistik, botlar.
 *   istemci.ts        tarayıcı soketi + useMasa() kancası.
 *
 * Oyunlar:
 *   yedili  Ana mod. 104 taş (1–13 × 4 renk × 2), joker yok, 7 taş dağıtılır, per aç / işle, eli bitiren kazanır.
 *   takim   Yedili'nin takımlı türü (A/B karşılıklı), takım açılışı ortak, "hediye taş" kuralı.
 *   yuzbir  101 Okey: 106 taş, gösterge + okey (joker), 21 taş, 101 ile ya da 5 çiftle açma, taş atma.
 *   uno     Uno: 108 kart.
 *   go      Go (ahşap tahta): 9/13/19, alan puanı + komi, ko, intihar yasak, iki pas → ölü taş işaretleme. 2 oyuncu.
 *   cizgi   Çizgi Yarışı: zarla kare kare ilerleyen çizgi rakip sahaya ulaşmaya çalışır (32/64/96/128 kare). 2 oyuncu.
 *   xox     XOX: 3×3, 4×4, 5×5, 6×6. 2 oyuncu.
 * Tahta oyunlarının kuralları ve arayüz planı: meds/docs/TAHTA_OYUNLARI.md
 */

import type { PistiGorunum, PistiHamle } from './motor/pisti';
import type { DominoGorunum, DominoHamle } from './motor/domino';

export type OyunTur = 'yedili' | 'takim' | 'yuzbir' | 'uno' | 'go' | 'cizgi' | 'xox' | 'remi' | 'kastet' | 'duz' | 'pisti' | 'domino';
/** Arayüzü hazır olmayan türler lobide gösterilmez, sunucu oda kurdurmaz (TURLER). Arayüz bitince sunucu TURLER'e eklenir. */
export const TAHTA_TURLER = ['go', 'cizgi', 'xox'] as const;
export type Takim = 'A' | 'B';
/** [0,1) düzgün rastgele sayı (sunucu kripto kaynaklı verir; sınamada tohumlu) */
export type Rng = () => number;

/* ------------------------------------------------------------------ okey taşları ------------------------------------------------------------------ */

/** Renk dizini 0–3; ekrandaki renk oda ayarındaki `renkler[r]` (kurucu değiştirebilir). */
export type Renk = 0 | 1 | 2 | 3;

export interface Tas {
  /** Destede tekil kimlik (yedili/takim: 0–103, yuzbir: 0–105) */
  id: number;
  /** 1–13; 0 = sahte okey (yalnız yuzbir) */
  s: number;
  r: Renk;
  /** Yalnız masadaki perde, taş joker (okey) olarak duruyorsa temsil ettiği taş */
  yerine?: { s: number; r: Renk };
}

/** seri: aynı renk ardışık (1 yalnız başta; 12-13-1 YOK) · grup: aynı sayı farklı renk (3–4) · cift: özdeş iki taş (yalnız yuzbir) */
export type PerTur = 'seri' | 'grup' | 'cift';

export interface Per {
  id: number;
  tur: PerTur;
  /** seri: küçükten büyüğe; grup: renk dizinine göre */
  taslar: Tas[];
  /** Peri açan oyuncu */
  sahip: string;
}

export type OkeyHamle =
  /** Elden yeni per aç (taş kimlikleri, sıra önemsiz; motor dizer). yuzbir'de yalnız açılıştan SONRA ek per için. */
  | { t: 'ac'; taslar: number[] }
  /** yuzbir ilk açılış: perlerin tamamı tek hamlede (seri/grup toplamı ≥ 101 ya da ≥ 5 çift) */
  | { t: 'ac101'; perler: number[][] }
  /** Masadaki pere taş işle. uc yalnız belirsizse gerekir (okeyle iki uca da uyan seri). */
  | { t: 'isle'; tas: number; per: number; uc?: 'bas' | 'son' }
  /** Taş çek. yuzbir'de kaynak: deste ya da bir önceki oyuncunun attığı taş. */
  | { t: 'cek'; kaynak?: 'deste' | 'atik' }
  /** yuzbir: yandan alınan ve kullanılamayan taşı geri bırakıp desteden çek (cezasız) */
  | { t: 'geriKoy' }
  /** yuzbir: taş at (turu bitirir) */
  | { t: 'at'; tas: number }
  /** yedili/takim: masadaki perleri yeniden kur (yer değiştir, taşları perler arasında yeniden diz). Masadaki taşların TAMAMI
   *  kullanılır, ele taş alınmaz, elden taş eklenmez; her yeni per geçerli olmalıdır. Sıra sendeyken ve açmışken (takımda takım açmışken). */
  | { t: 'duzenle'; perler: number[][]; ciftler?: number[][] }
  /** kastet/remi: sırayı geçir (Kastet'te el boşken el biter) */
  | { t: 'pas' }
  /** duz: son taşı atıp bitir; gruplar kalan 14 taş */
  | { t: 'bitir'; tas: number; gruplar: number[][] }
  /** duz: ilk turda göstergeyi göster */
  | { t: 'goster' }
  /** yedili/takim: eli devret (turu bitirir) */
  | { t: 'devret' };

export interface OkeyOyuncuGorunum {
  id: string;
  tasSayisi: number;
  /** Per açtı mı (takim: kendisi; işleme hakkı için `takimActi`) */
  acti: boolean;
  takim?: Takim;
  /** takim: takımdan biri açtıysa true (işleme hakkı) */
  takimActi?: boolean;
  /** yuzbir: çiftle açtı */
  ciftActi?: boolean;
  /** Bu elde yazılan cezalar */
  cezalar: Ceza[];
  /** yuzbir: attığı taşlar (son eleman en üstte) */
  atiklar?: Tas[];
}

export interface OkeyGorunum {
  tur: 'yedili' | 'takim' | 'yuzbir' | 'kastet' | 'remi' | 'duz';
  elNo: number;
  /** Sırası olan oyuncu */
  sira: string;
  /** Oturma sırasıyla */
  oyuncular: OkeyOyuncuGorunum[];
  /** Bakanın eli (izleyicide boş). Sıra motorun verdiği sıradır; ıstaka dizilişi istemcide tutulur. */
  elim: Tas[];
  perler: Per[];
  /** Destede kalan taş */
  deste: number;
  /** Sıradaki oyuncunun bu turdaki durumu */
  tur_: { cekti: boolean; hamleYapti: boolean };
  /** yuzbir */
  gosterge?: Tas;
  okey?: { s: number; r: Renk };
  /** yuzbir: bu turda yandan (atıktan) alınan ve kullanılması zorunlu taş */
  yandanAlinan?: number;
  bitti: boolean;
}

/* ------------------------------------------------------------------ uno ------------------------------------------------------------------ */

export type UnoRenk = 'k' | 's' | 'y' | 'm'; // kırmızı, sarı, yeşil, mavi
export type UnoDeger = '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'pas' | 'yon' | '+2' | 'joker' | '+4';
export interface UnoKart { id: number; renk: UnoRenk | null; deger: UnoDeger }

export type UnoHamle =
  /** renk: joker / +4 için zorunlu. uno: son ikinci kartı oynarken "UNO" dediğini bildirir. */
  | { t: 'oyna'; kart: number; renk?: UnoRenk; uno?: boolean }
  | { t: 'cek' }
  /** Çektikten sonra oynamadan geç */
  | { t: 'pas' }
  /** Tek kartı kalan ve UNO demeyi unutan oyuncu, yakalanmadan önce söyler */
  | { t: 'uno' }
  /** UNO demeyen oyuncuyu yakala (2 kart çeker) */
  | { t: 'yakala'; hedef: string }
  /** El ilk kartı joker açıldıysa ilk oyuncu rengi seçer */
  | { t: 'renk'; renk: UnoRenk }
  /** +4 sana oynandı: kabul et (4 çek, sıra geçer) ya da itiraz et (resmî kural) */
  | { t: 'kabul' }
  | { t: 'itiraz' };

export interface UnoGorunum {
  tur: 'uno';
  elNo: number;
  sira: string;
  yon: 1 | -1;
  oyuncular: { id: string; kartSayisi: number; unoDedi: boolean }[];
  elim: UnoKart[];
  /** Atık destesinin üstü */
  ust: UnoKart;
  /** Geçerli renk (joker sonrası seçilen) */
  aktifRenk: UnoRenk;
  deste: number;
  atikSayisi: number;
  /** Sıradaki oyuncu bu turda çekti mi; çektiyse yalnız `cekilen` oynanabilir ya da pas */
  cektiBuTur: boolean;
  cekilen?: number;
  /** Bakanın şu an oynayabileceği kart kimlikleri (sıra ondaysa) */
  oynanabilir: number[];
  /** UNO demediği için şu an yakalanabilecek oyuncular */
  yakalanabilir: string[];
  bitti: boolean;
  /** Oyun modu (UNO_MODLAR) */
  mod: UnoMod;
  /** Yığma modunda biriken çekme cezası (0 = yok) */
  yigin: number;
  /** +4 itirazı bekleniyor: hedef kabul ya da itiraz eder */
  dortBekle?: { oynayan: string; hedef: string };
  /** İlk açılan kart joker: sıradaki oyuncu renk seçer */
  renkSec?: boolean;
}

/** Uno modları: klasik = resmî kurallar (+4 itirazı, üst üste ekleme yok) */
export type UnoMod = 'klasik' | 'yigma' | 'yediSifir' | 'cekCek' | 'atlama' | 'hizli';
export const UNO_MODLAR: { id: UnoMod; ad: string; aciklama: string }[] = [
  { id: 'klasik', ad: 'Klasik', aciklama: 'Resmî kurallar: +2 ve +4 üst üste eklenmez, +4’e itiraz edilebilir.' },
  { id: 'yigma', ad: 'Yığma', aciklama: '+2 üstüne +2 ya da +4, +4 üstüne +4 eklenir; ceza birikir, ekleyemeyen hepsini çeker.' },
  { id: 'yediSifir', ad: '7-0', aciklama: '7 oynayan en az kartı olan rakiple elini değiştirir; 0 oynanınca herkes elini yöndeki oyuncuya verir.' },
  { id: 'atlama', ad: 'Atlama', aciklama: 'Ortadaki kartın tıpkısı (aynı renk, aynı sayı ya da simge) elindeyse sıranı beklemeden atarsın; sıra senden devam eder.' },
  { id: 'hizli', ad: 'Hızlı', aciklama: 'Herkese 5 kart dağıtılır; eller kısa sürer. Kurallar klasikle aynıdır.' },
  { id: 'cekCek', ad: 'Çek-çek', aciklama: 'Oynayacak kartın yoksa uyan kart gelene dek çekersin; gelen kartı oynayabilirsin.' },
];

/* ------------------------------------------------------------------ go ------------------------------------------------------------------ */

/** Kesişim dizini: i = y * boyut + x (x sütun, y satır; 0,0 sol üst) */
export type GoTas = 'S' | 'B'; // siyah, beyaz (siyah başlar)
export type GoBoyut = 9 | 13 | 19;
export type GoHamle =
  | { t: 'koy'; i: number }
  | { t: 'pas' }
  | { t: 'teslim' }
  /** Sayım aşaması: grubun ölü/diri işaretini değiştir (grubun herhangi bir taşı). Her değişiklik iki onayı da sıfırlar. */
  | { t: 'olu'; i: number }
  /** Sayım aşaması: işaretlemeyi onayla (iki taraf onaylayınca el biter) */
  | { t: 'onayla' }
  /** Sayım aşaması: anlaşmazlık, oyuna dön (pas sayacı sıfırlanır, sıra karşıdadır) */
  | { t: 'devam' }
  /** Sıradakinin süresi bitti (sunucu zamanlayıcısı yollar; motor saati doğrular) */
  | { t: 'sureBitti' };

export interface GoGorunum {
  tur: 'go';
  elNo: number;
  boyut: GoBoyut;
  /** boyut² uzunlukta: '' boş, 'S' / 'B' */
  tahta: ('' | GoTas)[];
  sira: string;
  /** Oyuncu → renk */
  renkler: Record<string, GoTas>;
  /** Esir (yakalanan rakip taşı) sayısı, renge göre */
  esir: Record<GoTas, number>;
  komi: number;
  /** Son hamle (i, pas için -1) — tahtada halka */
  son: { renk: GoTas; i: number } | null;
  /** Ko nedeniyle şu an konulamayan nokta */
  ko: number | null;
  /** Sıradakinin yasal noktaları (asistan / gölge taş için) */
  yasal: number[];
  /** Yıldız noktaları (hoshi) */
  yildiz: number[];
  asama: 'oyun' | 'sayim';
  /** Sayım: ölü işaretli taş dizinleri, onaylayanlar, anlık puan önizlemesi */
  olu: number[];
  onay: string[];
  alan?: { S: number[]; B: number[] };
  puan?: Record<GoTas, number>;
  hamleSayisi: number;
  bitti: boolean;
  /** Handikap taşı sayısı (0: yok) */
  handikap: number;
  /** Süre sınırı (ms): kalan ana süre + byo-yomi hakkı; gecen = sıradakinin bu görünüm gönderilirken harcadığı */
  saat: { ana: Record<GoTas, number>; periyot: Record<GoTas, number>; byo: number; gecen: number } | null;
}
/** Go süre seçenekleri: ana süre (sn) + byo-yomi (periyot × sn) */
export type GoSure = 'yok' | 'hizli' | 'normal' | 'uzun';
export const GO_SURELER: { id: GoSure; ad: string; ana: number; byo: number; periyot: number }[] = [
  { id: 'yok', ad: 'Süresiz', ana: 0, byo: 0, periyot: 0 },
  { id: 'hizli', ad: '5 dk + 3×30 sn', ana: 300, byo: 30, periyot: 3 },
  { id: 'normal', ad: '10 dk + 5×30 sn', ana: 600, byo: 30, periyot: 5 },
  { id: 'uzun', ad: '20 dk + 5×60 sn', ana: 1200, byo: 60, periyot: 5 },
];

/* ------------------------------------------------------------------ çizgi yarışı ------------------------------------------------------------------ */

/** Hücre: s sütun (0..genislik-1), r satır (0 = 1. oyuncunun kalesi, uzunluk-1 = 2. oyuncunun kalesi) */
export interface Hucre { s: number; r: number }
export type CizgiKare = 32 | 64 | 96 | 128;
export type CizgiHamle =
  /** Zar at (sunucu atar) */
  | { t: 'zar' }
  /** Zar atıldıktan sonra adımları harca. yan: önündeki hücre rakip çizgisiyle doluysa yandaki sütuna geç (1 adım, yan hakkı düşer). */
  | { t: 'ilerle'; yon: 'duz' | 'sol' | 'sag' }
  /** Kalan adımları yak (ilerleyemiyorsan ya da beklemek istiyorsan) */
  | { t: 'bekle' };

export interface CizgiAdim {
  /** el içi tur numarası */
  tur: number;
  o: string;
  zar: number;
  /** pozitif ilerleme, negatif gerileme (kapışmada mağlup) */
  fark: number;
  /** Bu turda eklenen / silinen hücreler (tasarımda son 3–4 tur vurgusu) */
  eklenen: Hucre[];
  silinen: Hucre[];
  kapisma?: { rakipZar: number; kazanan: string | null };
}

export interface CizgiGorunum {
  tur: 'cizgi';
  elNo: number;
  kare: CizgiKare;
  /** Satır sayısı (uzunluk) ve sütun sayısı */
  uzunluk: number;
  genislik: number;
  sira: string;
  /** Oyuncu → çizgi (baş son eleman); 1. oyuncu r artarak, 2. oyuncu r azalarak ilerler */
  cizgiler: Record<string, Hucre[]>;
  /** Oyuncu → kalan yan geçiş hakkı */
  yanHak: Record<string, number>;
  /** Sıradakinin atılmış zarı ve kalan adımı (null: zar atılmadı) */
  zar: number | null;
  kalan: number;
  /** Çizgiler baş başa ve iki baş da kendi yarısını geçmiş tarafta: zar düellosu (kazanan ilerler, kaybeden geriler) */
  kapisma: boolean;
  /** Son 4 tur (en yeni sonda) */
  gecmis: CizgiAdim[];
  /** Sıradakinin şu an yapabileceği ilerle yönleri */
  yonler: ('duz' | 'sol' | 'sag')[];
  bitti: boolean;
}

/* ------------------------------------------------------------------ xox ------------------------------------------------------------------ */

export type XoxBoyut = 3 | 4 | 5 | 6;
export type XoxHamle = { t: 'koy'; i: number } | { t: 'teslim' };
export interface XoxGorunum {
  tur: 'xox';
  elNo: number;
  boyut: XoxBoyut;
  /** Kazanmak için yan yana gereken işaret */
  hedef: number;
  tahta: ('' | 'X' | 'O')[];
  sira: string;
  isaretler: Record<string, 'X' | 'O'>;
  son: number | null;
  /** Kazanan sıra (vurgu çizgisi) */
  cizgi: number[] | null;
  bitti: boolean;
}
/** Boyut → yan yana hedef (3×3 klasik; büyük tahtalarda berabereliği azaltmak için) */
export const XOX_HEDEF: Record<XoxBoyut, number> = { 3: 3, 4: 4, 5: 4, 6: 5 };

export type OyunGorunum = OkeyGorunum | UnoGorunum | GoGorunum | CizgiGorunum | XoxGorunum | PistiGorunum | DominoGorunum;
export type Hamle = OkeyHamle | UnoHamle | GoHamle | CizgiHamle | XoxHamle | PistiHamle | DominoHamle;

/* ------------------------------------------------------------------ olaylar ------------------------------------------------------------------ */

/**
 * Motorun her hamlede ürettiği olaylar: animasyon, ses ve kısa vurgu için. `kime` varsa yalnız o oyuncuya gider (gizli bilgi).
 * Durumun doğruluk kaynağı DEĞİLDİR; ekran her zaman son `OdaGorunum`'dan çizilir, olay yalnız "ne oldu"yu canlandırır.
 *
 * Okey:  dagit · acti{o, perler: Per[]} · isledi{o, per: Per.id, tas: Tas, uc: 'bas'|'son'|null|'bol', yeniPer?: Per.id} · geriKoydu{o, tas}
 *        (uc 'bol' = yedili/takim "seriyi bölerek işleme": kopya taş serinin ortasına işlenir, seri ikiye bölünür; alt parça eski kimliği
 *        korur ve işlenen taşla biter, üst parça `yeniPer` kimliğiyle eski taşla başlar) · cekti{o, kaynak?, tas? (yalnız açık kaynak: atık), cezaTasi?}
 *        cektim{kime, tas} · devretti{o} · atti{o, tas} · ceza{o, ceza: Ceza} · hediye{o, kimler: string[]} · sira{o} · elBitti
 * Uno:   dagit · oynadi{o, kart, renk?} · cekti{o, adet, neden?: '+2'|'+4'|'yakalandi'|'cek'} · cektim{kime, kartlar}
 *        pas{o} · atlandi{o} · yon{yon} · uno{o} · yakalandi{o, yakalayan} · renk{renk} · karildi · sira{o} · elBitti
 * Oda:   tepki{o, e} · katildi{o} · ayrildi{o} · botDevraldi{o} · durdu · devam
 */
export interface Olay {
  t: string;
  /** Olayı yapan oyuncu */
  o?: string;
  kime?: string;
  [k: string]: unknown;
}

/* ------------------------------------------------------------------ puan ------------------------------------------------------------------ */

export interface Ceza {
  /** islek: işlek taşı işlemedi · per: açabileceği peri bekletti · islekAtti / okeyAtti / acmadi (yuzbir) · uno (UNO demedi) */
  tur: string;
  /** Eksi değer (ör. -5) */
  puan: number;
  aciklama: string;
}

export interface ElSatir {
  id: string;
  /** Bu elin net puanı (yüksek iyi; kaybeden eksi alır). Cezalar dahildir. */
  puan: number;
  /** Elde kalan taş/kart sayısı */
  kalan: number;
  kazandi: boolean;
  cezalar: Ceza[];
  /** Kısa döküm: "5 taş (−5) · 1 ceza (−5)" */
  aciklama?: string;
}

export interface ElSonuc {
  /** bitti: biri elini bitirdi · berabere: yığın bitti ve kimse oynayamıyor · deste: deste bitti (yuzbir) */
  neden: 'bitti' | 'berabere' | 'deste';
  kazananlar: string[];
  kazananTakim?: Takim;
  satirlar: ElSatir[];
}

/* ------------------------------------------------------------------ motor ------------------------------------------------------------------ */

/**
 * Kural motoru. Durum düz JSON'dur (meds-pg'ye yazılır, sunucu yeniden başlayınca geri yüklenir): Map/Set/Date/sınıf YOK.
 * `uygula` girdi durumunu DEĞİŞTİRMEZ; yeni durum döndürür. Kural dışı her hamle `{ hata }` döner (Türkçe, oyuncuya gösterilir).
 */
export interface Motor {
  tur: OyunTur;
  min: number;
  max: number;
  elBaslat(g: { oyuncular: { id: string; takim?: Takim }[]; elNo: number; baslayan: number; rng: Rng; ayar?: Partial<OdaAyar> }): unknown;
  uygula(durum: unknown, oyuncu: string, hamle: unknown, rng: Rng): { durum: unknown; olaylar: Olay[] } | { hata: string };
  /** bakan = null: izleyici (hiçbir el görünmez) */
  gorunum(durum: unknown, bakan: string | null): OyunGorunum;
  /** Bot şu an bir şey yapmalıysa hamlesi, değilse null. Her zaman kurala uygun, cezasız hamle döner. */
  botHamle(durum: unknown, bot: string, rng: Rng): unknown | null;
  /** El bittiyse sonuç */
  sonuc(durum: unknown): ElSonuc | null;
  /** Süreli oyunlar: sıradakinin süresinin biteceği an (ms). Sunucu bu anda `{ t: 'sureBitti' }` uygular; hamlelere `z` (sunucu saati) basar. */
  sureSonu?(durum: unknown): number | null;
  /** Oyun durdurulup sürdürülünce saati ms kadar ileri kaydır (durakta süre işlemez) */
  saatKaydir?(durum: unknown, ms: number): unknown;
}

/* ------------------------------------------------------------------ oda ------------------------------------------------------------------ */

export const OKEY_TEMALAR = ['klasik', 'kitty'] as const;
export const UNO_TEMALAR = ['klasik', 'stitch', 'buyucu'] as const;
export type OkeyTema = (typeof OKEY_TEMALAR)[number];
export type UnoTema = (typeof UNO_TEMALAR)[number];
/** Varsayılan taş renkleri: kırmızı, siyah, mavi, sarı */
export const VARSAYILAN_RENKLER = ['#d62839', '#1d1d1f', '#1f6feb', '#e8a400'] as const;
export const EL_SECENEK = [1, 3, 5, 7, 0] as const; // 0 = kurucu bitirene dek

export interface OdaAyar {
  /** Maç kaç el; 0 = sınırsız (kurucu "Oyunu bitir" diyene dek) */
  elSayisi: number;
  /** Normal mod (true): ipucu, otomatik işle/diz, en iyi plan açık. Zorlu mod (false): yardımcı yok, ıstaka/masa elle dizilemez; masa el bitince dizilir. */
  asistan: boolean;
  /** Uno modu (UNO_MODLAR) */
  unoMod?: UnoMod;
  /** Takım Yedili, 2–4 oyuncu: kişi başı 7 ya da 14 taş (kurucu seçer). 5–6 oyuncuda her zaman 4 taş. */
  tasSayisi: 7 | 14;
  /** okey: 'klasik' | 'kitty' · uno: 'klasik' | 'stitch' | 'buyucu' */
  tema: string;
  /** Okey taş renkleri (4 adet #rrggbb) */
  renkler: string[];
  /** go: tahta boyutu (varsayılan 9), komi (varsayılan 6.5) */
  goBoyut?: GoBoyut;
  komi?: number;
  /** go: handikap taşı 0–9 (≥1 iken komi 0,5; ≥2 iken taşlar yıldızlara, beyaz başlar), süre seçeneği */
  goHandikap?: number;
  goSure?: GoSure;
  /** cizgi: kare (yol uzunluğu, varsayılan 64) */
  cizgiKare?: CizgiKare;
  /** xox: tahta boyutu (varsayılan 3) */
  xoxBoyut?: XoxBoyut;
}

export interface OyuncuBilgi {
  id: string;
  ad: string;
  bot?: boolean;
  takim?: Takim;
  bagli: boolean;
  foto?: string;
}

export type OdaAsama = 'lobi' | 'oyun' | 'elSonu' | 'bitti';

export interface ElOzet { no: number; neden: ElSonuc['neden']; kazananlar: string[]; puanlar: Record<string, number> }

export interface OdaGorunum {
  kod: string;
  tur: OyunTur;
  ayar: OdaAyar;
  asama: OdaAsama;
  /** Kurucu oyunu durdurdu: hamle kabul edilmez, "Devam ettir" bekler */
  durdu: boolean;
  kurucu: string;
  /** Bu istemcinin oyuncu kimliği */
  ben: string;
  /** Oturma sırasıyla */
  oyuncular: OyuncuBilgi[];
  elNo: number;
  oyun?: OyunGorunum;
  elSonuc?: ElSonuc;
  /** Maç toplam puanı */
  skor: Record<string, number>;
  eller: ElOzet[];
  /** Her değişiklikte artar */
  surum: number;
  /** Sırası olan bakanın bu turda geri alabileceği hamle sayısı (per açma / işleme) */
  geriAl?: number;
}

/** İstemci → sunucu */
export type IstemciMesaj =
  | { t: 'gir'; jeton: string; ad: string }
  | { t: 'kur'; tur: OyunTur; ayar?: Partial<OdaAyar> }
  | { t: 'katil'; kod: string }
  | { t: 'ayar'; ayar: Partial<OdaAyar> }
  | { t: 'takim'; takim: Takim; hedef?: string }
  | { t: 'botEkle' }
  | { t: 'cikar'; hedef: string }
  | { t: 'baslat' }
  | { t: 'hamle'; h: Hamle }
  | { t: 'geriAl' }
  | { t: 'sonrakiEl' }
  | { t: 'durdur' }
  | { t: 'devam' }
  | { t: 'bitir' }
  | { t: 'botDevral'; hedef: string }
  | { t: 'tepki'; e: string }
  | { t: 'cik' }
  | { t: 'ping'; z: number };

/** Sunucu → istemci */
export type SunucuMesaj =
  | { t: 'girdi'; ben: string; ad: string }
  | { t: 'durum'; oda: OdaGorunum; olaylar: Olay[] }
  | { t: 'cikti' }
  | { t: 'hata'; mesaj: string; kod?: 'kimlik' | 'kimlik-bekle' | 'oda-yok' | 'dolu' | 'basladi' | 'hamle' | 'kapali' }
  | { t: 'pong'; z: number; s: number };

export const TEPKILER = ['👏', '😂', '😮', '😢', '🔥', '❤️', '😎', '🤔'] as const;
export const OYUN_ADI: Record<OyunTur, string> = { yedili: 'Yedili Okey', takim: 'Takım Yedili', yuzbir: '101 Okey', uno: 'Uno', go: 'Go', cizgi: 'Çizgi Yarışı', xox: 'XOX', remi: 'Remi', kastet: 'Kastet', duz: 'Düz Okey', pisti: 'Pişti', domino: 'Taş Domino' };
/** Takım Yedili kişi başı taş: 5–6 oyuncuda 4, 2–4 oyuncuda kurucunun seçtiği 7 ya da 14 */
export const takimElTas = (n: number, secim?: number): number => (n >= 5 ? 4 : secim === 14 ? 14 : 7);
export const OYUNCU_SINIR: Record<OyunTur, [number, number]> = { yedili: [2, 6], takim: [2, 6], yuzbir: [2, 4], uno: [2, 8], go: [2, 2], cizgi: [2, 2], xox: [2, 2], remi: [2, 4], kastet: [2, 4], duz: [2, 4], pisti: [2, 4], domino: [2, 4] };

/* ------------------------------------------------------------------ istatistik (GET /api/masa/istatistik) ------------------------------------------------------------------ */

export interface TurIstatistik { tur: OyunTur; el: number; kazanma: number; puan: number; ceza: number; enIyi: number; enKotu: number }
export interface RakipIstatistik { kimlik: string; ad: string; el: number; benKazandim: number; oKazandi: number; benPuan: number; oPuan: number; turler: Partial<Record<OyunTur, number>> }
export interface SonEl { kod: string; tur: OyunTur; elNo: number; at: number; puan: number; kalan: number; ceza: number; kazandi: boolean; rakipler: string[] }
export interface Istatistik { genel: TurIstatistik[]; rakipler: RakipIstatistik[]; son: SonEl[] }
/** GET /api/masa/odalarim: yarım kalan (bitmemiş) odalarım */
export interface OdaOzet { kod: string; tur: OyunTur; asama: OdaAsama; durdu: boolean; oyuncular: string[]; elNo: number; guncel: number; kurucuBen: boolean }
