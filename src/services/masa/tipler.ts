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
 */

export type OyunTur = 'yedili' | 'takim' | 'yuzbir' | 'uno';
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
  tur: 'yedili' | 'takim' | 'yuzbir';
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
  | { t: 'yakala'; hedef: string };

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
}

export type OyunGorunum = OkeyGorunum | UnoGorunum;
export type Hamle = OkeyHamle | UnoHamle;

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
  elBaslat(g: { oyuncular: { id: string; takim?: Takim }[]; elNo: number; baslayan: number; rng: Rng }): unknown;
  uygula(durum: unknown, oyuncu: string, hamle: unknown, rng: Rng): { durum: unknown; olaylar: Olay[] } | { hata: string };
  /** bakan = null: izleyici (hiçbir el görünmez) */
  gorunum(durum: unknown, bakan: string | null): OyunGorunum;
  /** Bot şu an bir şey yapmalıysa hamlesi, değilse null. Her zaman kurala uygun, cezasız hamle döner. */
  botHamle(durum: unknown, bot: string, rng: Rng): unknown | null;
  /** El bittiyse sonuç */
  sonuc(durum: unknown): ElSonuc | null;
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
  /** Yardımcı asistan (ipucu, otomatik işle, en iyi plan) açık mı */
  asistan: boolean;
  /** okey: 'klasik' | 'kitty' · uno: 'klasik' | 'stitch' | 'buyucu' */
  tema: string;
  /** Okey taş renkleri (4 adet #rrggbb) */
  renkler: string[];
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
  | { t: 'hata'; mesaj: string; kod?: 'kimlik' | 'oda-yok' | 'dolu' | 'basladi' | 'hamle' | 'kapali' }
  | { t: 'pong'; z: number; s: number };

export const TEPKILER = ['👏', '😂', '😮', '😢', '🔥', '❤️', '😎', '🤔'] as const;
export const OYUN_ADI: Record<OyunTur, string> = { yedili: 'Yedili Okey', takim: 'Takım Yedili', yuzbir: '101 Okey', uno: 'Uno' };
export const OYUNCU_SINIR: Record<OyunTur, [number, number]> = { yedili: [2, 6], takim: [2, 6], yuzbir: [2, 4], uno: [2, 8] };

/* ------------------------------------------------------------------ istatistik (GET /api/masa/istatistik) ------------------------------------------------------------------ */

export interface TurIstatistik { tur: OyunTur; el: number; kazanma: number; puan: number; ceza: number; enIyi: number; enKotu: number }
export interface RakipIstatistik { kimlik: string; ad: string; el: number; benKazandim: number; oKazandi: number; benPuan: number; oPuan: number; turler: Partial<Record<OyunTur, number>> }
export interface SonEl { kod: string; tur: OyunTur; elNo: number; at: number; puan: number; kalan: number; ceza: number; kazandi: boolean; rakipler: string[] }
export interface Istatistik { genel: TurIstatistik[]; rakipler: RakipIstatistik[]; son: SonEl[] }
/** GET /api/masa/odalarim: yarım kalan (bitmemiş) odalarım */
export interface OdaOzet { kod: string; tur: OyunTur; asama: OdaAsama; durdu: boolean; oyuncular: string[]; elNo: number; guncel: number; kurucuBen: boolean }
