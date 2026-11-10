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
  /** yedili/takim/yuzbir: masadaki perleri yeniden kur (yer değiştir, taşları perler arasında yeniden diz). Masadaki taşların TAMAMI
   *  kullanılır, ele taş alınmaz; elden taş katılabilir (masadan alınan taşla yeni per). Her yeni per geçerli olmalıdır.
   *  Sıra sendeyken ve açmışken (takımda takım açmışken; yuzbir'de taş çektikten sonra, çiftlere dokunulmaz). */
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

export type UnoRenk = 'k' | 's' | 'y' | 'm'; // kırmızı, sarı, yeşil, mavi (Flip koyu yüz: pembe, turuncu, turkuaz, mor)
/**
 * Kart değerleri. Klasik: 0–9, pas, yon, +2, joker, +4 (joker +4).
 * Flip/Express: +1, flip, joker+2, +5, pasHerkes, jokerRenk · Hepsi Joker: jokerYon, jokerPas, jokerPas2, jokerHedef2, jokerTakas
 * No Mercy: hepsiAt, r+4 (renkli +4), jokerYon4, +6, +10, rulet · Extreme: vur1, vur2, jokerVur · Takım: jokerTakim, jokerTakim4
 * Flex: jokerCevir, fxHerkes, fxHedef2, fx+4 · Yalancı: jokerMeydan · Sevimli Dostlar: kitty, batman, kuromi, pony
 */
export type UnoDeger =
  | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'pas' | 'yon' | '+2' | 'joker' | '+4'
  | '+1' | 'flip' | 'joker+2' | '+5' | 'pasHerkes' | 'jokerRenk'
  | 'jokerYon' | 'jokerPas' | 'jokerPas2' | 'jokerHedef2' | 'jokerTakas'
  | 'hepsiAt' | 'r+4' | 'jokerYon4' | '+6' | '+10' | 'rulet'
  | 'vur1' | 'vur2' | 'jokerVur'
  | 'jokerTakim' | 'jokerTakim4'
  | 'jokerCevir' | 'fxHerkes' | 'fxHedef2' | 'fx+4'
  | 'jokerMeydan'
  | 'kitty' | 'batman' | 'kuromi' | 'pony';

/** Kartın bir yüzü */
export interface UnoYuz {
  renk: UnoRenk | null;
  deger: UnoDeger;
  /** Flip: koyu yüz */
  t?: 'k';
  /** Flex kartı: ikinci (flex) rengi; flex jokerlerde 'j' */
  fx?: UnoRenk | 'j';
  /** Flex: güç kartını çeviren sayı kartı */
  cv?: 1;
  /** Takım: paslaşma simgeli sayı kartı */
  ps?: 1;
  /** Yalancı: kapalı oynanan "yalancı" kartı */
  yl?: 1;
  /** Yalancı: kapalı oynandı; renk/deger söylenen (beyan) kimliktir, gerçek kart gizlidir */
  kp?: 1;
}
export interface UnoKart extends UnoYuz {
  id: number;
  /** Flip: kartın öbür yüzü (yalnız motor durumunda; kendi elinde gönderilmez) */
  arka?: UnoYuz;
}
export interface UnoBeyan { renk: UnoRenk; deger: UnoDeger }

export type UnoHamle =
  /**
   * renk: joker için zorunlu. uno: son ikinci kartı oynarken "UNO" dediğini bildirir. hedef: hedefli kartlar (7 takası, hedefli çekme, saldırı).
   * flex: Flex kartının flex yüzüyle oyna. kapali + beyan: Yalancı modunda kapalı oyna ve ne olduğunu söyle.
   */
  | { t: 'oyna'; kart: number; renk?: UnoRenk; uno?: boolean; hedef?: string; flex?: boolean; kapali?: boolean; beyan?: UnoBeyan }
  /** Desteden çek (Extreme: fırlatıcıya bas; birikmiş ceza varsa cezayı üstlen) */
  | { t: 'cek' }
  /** Çektikten sonra oynamadan geç */
  | { t: 'pas' }
  /** Tek kartı kalan ve UNO demeyi unutan oyuncu (Takım modunda ortağı da) yakalanmadan önce söyler */
  | { t: 'uno' }
  /** UNO demeyen oyuncuyu yakala */
  | { t: 'yakala'; hedef: string }
  /** Renk seçimi bekleniyorsa (ilk kart joker, Flip sonrası joker, Renk Ruleti) */
  | { t: 'renk'; renk: UnoRenk }
  /** Joker çekme kartı sana oynandı: kabul et ya da itiraz et */
  | { t: 'kabul' }
  | { t: 'itiraz' }
  /** Kart ver (Takım: ortağa; Sevimli Dostlar: hediye) */
  | { t: 'ver'; kart: number }
  /** Yalancı: kapalı karta inan / yalan de */
  | { t: 'inan' }
  | { t: 'yalan' }
  /** Yalancı Meydan Okuması: kapalı kart koy · koyanı sorgula · sorgulamayı bitir */
  | { t: 'koy'; kart: number }
  | { t: 'sorgula'; hedef: string }
  | { t: 'yeter' };

/** Bekleyen karar (sıra akışını durdurur) */
export type UnoBekle =
  | { tur: 'renk'; kim: string }
  /** Joker çekme kartına itiraz: kart = oynanan değer */
  | { tur: 'itiraz'; oynayan: string; hedef: string; kart: UnoDeger }
  /** Renk Ruleti: `kim` rengi seçer, o renk gelene dek çeker */
  | { tur: 'rulet'; kim: string }
  /** Kart verme: bekleyenler ve kime kaç kart verecekleri */
  | { tur: 'ver'; neden: 'takim' | 'sembol' | 'yari' | 'hediye'; kalan: { kim: string; kime: string; adet: number }[] }
  /** Yalancı: kapalı kart oynandı; `karar` (sıradaki) inanır ya da yalan der, öbürleri de yalan diyebilir */
  | { tur: 'yalan'; oynayan: string; beyan: UnoBeyan; karar: string }
  /** Yalancı Meydan Okuması */
  | { tur: 'meydan'; oynayan: string; renk: UnoRenk; asama: 'koy' | 'sorgu'; koymayan: string[]; konan: string[] };

export interface UnoOyuncuGorunum {
  id: string;
  kartSayisi: number;
  unoDedi: boolean;
  /** No Mercy: 25 karta ulaşıp elendi */
  elendi?: boolean;
  /** Takım: takım numarası (0…); cikti: elini bitirdi, ortağını bekliyor */
  takim?: number;
  cikti?: boolean;
  /** Flex: güç kartı yeşil (kullanılabilir) mi */
  guc?: boolean;
  /** Flip: elindeki kartların bana görünen öbür yüzleri */
  arka?: UnoYuz[];
}

export interface UnoGorunum {
  tur: 'uno';
  elNo: number;
  sira: string;
  yon: 1 | -1;
  oyuncular: UnoOyuncuGorunum[];
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
  /** Biriken çekme cezası (yığma, No Mercy, Sevimli Dostlar; Extreme'de biriken basış) (0 = yok) */
  yigin: number;
  /** +4 itirazı bekleniyor: hedef kabul ya da itiraz eder */
  dortBekle?: { oynayan: string; hedef: string };
  /** İlk açılan kart joker: sıradaki oyuncu renk seçer */
  renkSec?: boolean;
  /** Bekleyen karar (dortBekle / renkSec bunun eski kısa yollarıdır) */
  bekle?: UnoBekle;
  /** Bakanın şimdi vermesi gereken kart: kime, kaç tane */
  ver?: { kime: string; adet: number; neden: 'takim' | 'sembol' | 'yari' | 'hediye' };
  /** Flip: etkin yüz (a = açık, k = koyu); desteUst = çekme destesinin üstünde görünen öbür yüz */
  taraf?: 'a' | 'k';
  desteUst?: UnoYuz;
  /** Hepsi Joker: renk yok */
  renksiz?: boolean;
  /** Extreme: deste fırlatıcıda (çekmek = düğmeye basmak) */
  firlatici?: boolean;
  /** Flex: flex yüzüyle oynanabilecek kartlar; yalnizFlex = yalnız flex yüzüyle uyanlar */
  flex?: number[];
  yalnizFlex?: number[];
  /** Çekmek serbest mi (sıra bendeyken) */
  cekOlur?: boolean;
  /** Çekilen kart oynanmak zorunda (No Mercy) */
  zorunlu?: boolean;
  /** Takım Oyunu jokeri: ortak oynamak zorunda */
  takimOyun?: boolean;
  /** Maçın puan hedefi (0 = yok) */
  hedefPuan?: number;
}

/** Uno modları: klasik = resmî kurallar (+4 itirazı, üst üste ekleme yok) */
export type UnoMod =
  | 'klasik' | 'yigma' | 'yediSifir' | 'cekCek' | 'atlama' | 'hizli'
  | 'deluxe' | 'express' | 'flip' | 'hepsiJoker' | 'noMercy' | 'extreme' | 'flex' | 'takim' | 'yalanci' | 'dostlar';
export type UnoModGrup = 'resmi' | 'ev' | 'ozel';
export interface UnoModTanim {
  id: UnoMod; ad: string; grup: UnoModGrup;
  /** Kart üstü kısa tanıtım */
  kisa: string;
  aciklama: string;
  /** Deste, dağıtılan kart, oyuncu sınırı (ciftOyuncu: yalnız 4, 6, 8) */
  deste: number; elKart: number; enAz: number; enCok: number; cift?: boolean;
  /** Resmî puan hedefi (0 = yok): maç bu puana ulaşılınca da biter */
  hedef: number;
  /** 1 kolay … 3 zor */
  zorluk: 1 | 2 | 3;
  /** Tanıtım rozetindeki örnek kartlar */
  ornek: [UnoRenk | null, UnoDeger][];
}
export const UNO_MOD_GRUPLAR: { id: UnoModGrup; ad: string; alt: string }[] = [
  { id: 'resmi', ad: 'Kutu oyunları', alt: 'Raflardaki Uno kutularının kendi desteleri ve kendi kuralları.' },
  { id: 'ev', ad: 'Ev kuralları', alt: 'Klasik 108 kartla, masada en çok oynanan ek kurallar.' },
  { id: 'ozel', ad: 'MeDSor özel', alt: 'Yalnız bu masada: karakter kartlı özel deste.' },
];
export const UNO_MODLAR: UnoModTanim[] = [
  { id: 'klasik', ad: 'Klasik', grup: 'resmi', kisa: 'Resmî kurallar', deste: 108, elKart: 7, enAz: 2, enCok: 8, hedef: 0, zorluk: 1, ornek: [['k', '7'], ['y', '+2'], [null, '+4']],
    aciklama: 'Resmî kurallar: +2 ve +4 üst üste eklenmez, +4’e itiraz edilebilir.' },
  { id: 'deluxe', ad: 'Deluxe', grup: 'resmi', kisa: '112 kart, 500 puan', deste: 112, elKart: 7, enAz: 2, enCok: 8, hedef: 500, zorluk: 1, ornek: [['m', '0'], ['s', 'yon'], [null, 'joker']],
    aciklama: 'Deluxe kutunun 112’lik destesi (8 Joker) ve puan defteri: klasik kurallar, maç 500 puana ulaşılınca da biter.' },
  { id: 'express', ad: 'Express', grup: 'resmi', kisa: '56 kart, 5’er kart', deste: 56, elKart: 5, enAz: 2, enCok: 6, hedef: 250, zorluk: 1, ornek: [['k', '4'], ['m', '+1'], [null, 'joker+2']],
    aciklama: 'Cep boyu Uno: 56 kart, herkese 5 kart. +2 yerine +1, +4 yerine Joker +2 vardır; hedef 250 puan.' },
  { id: 'flip', ad: 'Flip', grup: 'resmi', kisa: 'Çift yüzlü deste', deste: 112, elKart: 7, enAz: 2, enCok: 8, hedef: 500, zorluk: 2, ornek: [['y', 'flip'], ['k', '+5'], [null, 'jokerRenk']],
    aciklama: 'Her kartın açık ve koyu yüzü var. Flip kartı oynanınca deste, atık ve bütün eller ters döner; koyu yüzde +5, Herkesi Atlat ve Renk Gelene Dek Çek bekler.' },
  { id: 'hepsiJoker', ad: 'Hepsi Joker', grup: 'resmi', kisa: 'Renk yok, her kart oynanır', deste: 112, elKart: 7, enAz: 2, enCok: 8, hedef: 500, zorluk: 1, ornek: [[null, 'jokerPas2'], [null, 'jokerHedef2'], [null, 'jokerTakas']],
    aciklama: 'All Wild: destedeki her kart jokerdir, renk ve sayı tutturmak yoktur. Hedefli +2, Zorunlu Takas ve İkili Atlat ile sırayı sen yönetirsin.' },
  { id: 'noMercy', ad: 'No Mercy', grup: 'resmi', kisa: 'Acımasız: +10, 25 kartta elenme', deste: 168, elKart: 7, enAz: 2, enCok: 8, hedef: 1000, zorluk: 3, ornek: [[null, '+10'], ['k', 'hepsiAt'], [null, 'rulet']],
    aciklama: '168 kart: +6, +10, Renk Ruleti, Hepsini At. Çekme kartları birikir, uyan kart gelene dek çekilir, 7 takas 0 devir yapar; eli 25 karta ulaşan elenir.' },
  { id: 'extreme', ad: 'Extreme', grup: 'resmi', kisa: 'Kart fırlatıcı', deste: 112, elKart: 7, enAz: 2, enCok: 8, hedef: 500, zorluk: 2, ornek: [['m', 'vur2'], ['s', 'hepsiAt'], [null, 'jokerVur']],
    aciklama: 'Attack/Extreme: deste fırlatıcıdadır. Kart çekmek yerine düğmeye basarsın; bazen hiç, bazen bir avuç kart fırlar. Vur kartları üst üste eklenir.' },
  { id: 'flex', ad: 'Flex', grup: 'resmi', kisa: 'Güç kartıyla esnet', deste: 104, elKart: 7, enAz: 2, enCok: 8, hedef: 500, zorluk: 3, ornek: [['k', '5'], ['m', 'pas'], [null, 'fxHerkes']],
    aciklama: 'Flex kartlarının ikinci bir rengi ve güçlü bir ikinci etkisi var. Güç kartın yeşilken flex yüzünü kullanırsın; kullanınca kırmızıya döner.' },
  { id: 'takim', ad: 'Takım', grup: 'resmi', kisa: 'İkişerli takımlar', deste: 112, elKart: 7, enAz: 4, enCok: 8, cift: true, hedef: 500, zorluk: 2, ornek: [['y', '3'], [null, 'jokerTakim'], [null, 'jokerTakim4']],
    aciklama: 'Teams: karşındaki oyuncu ortağın. Kart paslaşır, Takım Oyunu jokeriyle sırayı ortağına atlatırsın; takım, iki ortak da elini bitirince kazanır. 4, 6 ya da 8 oyuncu.' },
  { id: 'yalanci', ad: 'Yalancı', grup: 'resmi', kisa: 'Kapalı oyna, blöf yap', deste: 112, elKart: 7, enAz: 2, enCok: 8, hedef: 500, zorluk: 3, ornek: [['k', '7'], ['m', '+2'], [null, 'jokerMeydan']],
    aciklama: 'Liar’s: yalancı kartları kapalı oynanır ve ne olduğu söylenir. İnanmayan “Yalan!” der: yalancı kartı geri alır, haksız çıkan 1 kart çeker. 7 takas, 0 devir yapar.' },
  { id: 'yigma', ad: 'Yığma', grup: 'ev', kisa: '+2 ve +4 birikir', deste: 108, elKart: 7, enAz: 2, enCok: 8, hedef: 0, zorluk: 2, ornek: [['k', '+2'], ['m', '+2'], [null, '+4']],
    aciklama: '+2 üstüne +2 ya da +4, +4 üstüne +4 eklenir; ceza birikir, ekleyemeyen hepsini çeker.' },
  { id: 'yediSifir', ad: '7-0', grup: 'ev', kisa: '7 ve 0 el değiştirir', deste: 108, elKart: 7, enAz: 2, enCok: 8, hedef: 0, zorluk: 2, ornek: [['s', '7'], ['y', '0']],
    aciklama: '7 oynayan seçtiği rakiple elini değiştirir; 0 oynanınca herkes elini yöndeki oyuncuya verir.' },
  { id: 'atlama', ad: 'Atlama', grup: 'ev', kisa: 'Tıpkısıyla araya gir', deste: 108, elKart: 7, enAz: 2, enCok: 8, hedef: 0, zorluk: 2, ornek: [['m', '5'], ['m', '5']],
    aciklama: 'Ortadaki kartın tıpkısı (aynı renk, aynı sayı ya da simge) elindeyse sıranı beklemeden atarsın; sıra senden devam eder.' },
  { id: 'hizli', ad: 'Hızlı', grup: 'ev', kisa: '5 kartla kısa el', deste: 108, elKart: 5, enAz: 2, enCok: 8, hedef: 0, zorluk: 1, ornek: [['y', '2'], ['k', 'pas']],
    aciklama: 'Herkese 5 kart dağıtılır; eller kısa sürer. Kurallar klasikle aynıdır.' },
  { id: 'cekCek', ad: 'Çek-çek', grup: 'ev', kisa: 'Uyan gelene dek çek', deste: 108, elKart: 7, enAz: 2, enCok: 8, hedef: 0, zorluk: 1, ornek: [['s', '9'], ['m', '1']],
    aciklama: 'Oynayacak kartın yoksa uyan kart gelene dek çekersin; gelen kartı oynayabilirsin.' },
  { id: 'dostlar', ad: 'Sevimli Dostlar', grup: 'ozel', kisa: 'Karakter kartları', deste: 116, elKart: 7, enAz: 2, enCok: 8, hedef: 0, zorluk: 2, ornek: [[null, 'kitty'], [null, 'batman'], [null, 'kuromi'], [null, 'pony']],
    aciklama: 'Klasik deste + 8 karakter kartı: Kedicik hediye verir, Yarasa cezayı siper eder, Yaramaz Tavşan herkese kart çektirir, Gökkuşağı Tayı bir rengin tamamını attırır. +2 ve +4 birikir.' },
];
export const unoModTanim = (mod: UnoMod | undefined): UnoModTanim => UNO_MODLAR.find((m) => m.id === mod) ?? UNO_MODLAR[0];
/** Oyuncu sayısı bu moda uyuyor mu; uymuyorsa Türkçe neden */
export function unoOyuncuUygun(mod: UnoMod | undefined, n: number): string | null {
  const m = unoModTanim(mod);
  if (m.cift && (n < 4 || n % 2)) return `${m.ad} modu 4, 6 ya da 8 oyuncuyla oynanır (ikişerli takımlar). Bot ekle ya da çıkar.`;
  if (n < m.enAz) return `${m.ad} modu için en az ${m.enAz} oyuncu gerekir.`;
  if (n > m.enCok) return `${m.ad} modu en çok ${m.enCok} oyuncuyla oynanır.`;
  return null;
}

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
  /** Düz yol açık oldukça kalan adımların hepsini tek hamlede harca */
  | { t: 'kos' }
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
 * Uno:   dagit · oynadi{o, kart, renk?, flex?} · cekti{o, adet, neden?: '+2'|'+4'|…|'yakalandi'|'cek'|'firlat'} · cektim{kime, kartlar}
 *        pas{o} · atlandi{o} · yon{yon} · uno{o} · yakalandi{o, yakalayan} · renk{renk} · karildi · sira{o} · elBitti
 *        flip{taraf} · elendi{o} · attiHepsi{o, adet} · firlat{o, adet} · verdi{o, hedef, adet} · aldim{kime, kartlar} · guc{o, acik} · gucHepsi
 *        yalan{o, hedef, hakli, kart?} · inandi{o} · geriAldi2{o} · meydan{o, renk} · koydu{o} · sorgu{o, hedef, dogru} · siper{o} · rulet{o, renk, adet}
 *        takimOyun{o, hedef} · cikti{o} · dondu{o}
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
export const UNO_TEMALAR = ['klasik', 'dostlar', 'stitch', 'buyucu'] as const;
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
  /** okey: 'klasik' | 'kitty' · uno: 'klasik' | 'dostlar' | 'stitch' | 'buyucu' */
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
  /** go/xox: bot gücü (varsayılan 'orta'; 'zor' eski kusursuz bot) */
  botZorluk?: BotZorluk;
}

export type BotZorluk = 'kolay' | 'orta' | 'zor';

export interface OyuncuBilgi {
  id: string;
  ad: string;
  bot?: boolean;
  takim?: Takim;
  bagli: boolean;
  foto?: string;
  /** Bağlantısı kopalı kaç saniye oldu (yalnız kopuk insan oyuncuda) */
  kopSn?: number;
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
  /** Bu istemci koltuksuz izleyici (oyun başladıktan sonra geldi) */
  izliyor?: boolean;
  /** İzleyiciler; istek: almak istediği bot koltuğu (kurucu onaylar) */
  izleyiciler?: { id: string; ad: string; istek?: string }[];
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
  | { t: 'koltukIste'; hedef: string }
  | { t: 'koltukVer'; kime: string; hedef?: string }
  | { t: 'koltukRed'; kime: string }
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
