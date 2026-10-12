/**
 * ==============================================================================
 * MedSoru Akıllı Soru Yazma, Cümle Devamı ve Güvenli Yazım Düzeltme Motoru
 * (src/services/smartComposerService.ts)
 *
 * Özellikler:
 *  1. Anlık (0-10ms) Yerel Çalışma: Ana iş parçacığını kilitlemez, ağ gecikmesi yok.
 *  2. Cümle İçi Devam (isExpanding) vs. Soru Kökü Kapatma (isQuestionReady) Ayrımı:
 *     Kullanıcı vaka ayrıntısı yazarken zorla "hangisidir?" ile soruyu bitirmez;
 *     klinik devam önerir (fizik muayene, tetkik, semptom).
 *  3. Bütün Cümleyi Dikkate Alma (Whole-Sentence Context):
 *     Yalnız son 1-2 kelimeye değil, metindeki tüm tıbbi varlıklara (organ, hastalık,
 *     semptom, ilaç, demografi) göre en alakalı klinik önerileri sunar.
 *  4. Sıfır Hata / Güvenli Yazım Düzeltmesi:
 *     Geçerli tıp terimlerini asla bozmaz; yalnızca bariz harf hatalarını ve Türkçe
 *     karakter eksikliklerini ("bobrek" -> "böbrek", "akciger" -> "akciğer") düzeltir.
 * ==============================================================================
 */

export type AssistChipType = 'continue' | 'complete' | 'fix';

export interface AssistOption {
  type: AssistChipType;
  label: string; // e.g. "Devam", "Soruyu Tamamla"
  text: string;  // Continuation text to append
  preview: string; // User-facing display text
  isTop?: boolean;
  category?: string;
}

export interface AssistResult {
  ghost: string;
  ghostType: AssistChipType | null;
  options: AssistOption[];
  fix: { text: string; changes: string[] } | null;
  spell: { text: string; changes: { from: string; to: string }[] } | null;
  isExpanding: boolean;
  detectedEntities: string[];
}

// ------------------------------------------------------------------------------
// 1. TIBBİ SÖZLÜK & GÜVENLİ TÜRKÇE YAZIM DÜZELTME TABLOSU
// ------------------------------------------------------------------------------

/** Sık kullanılan Türkçe karakter eksiklikleri ve tıp terimi eşleşmeleri */
export const MEDICAL_ACCENT_RESTORES: Record<string, string> = {
  // Organlar & Anatomi
  'bobrek': 'böbrek',
  'bobrekler': 'böbrekler',
  'bobrekte': 'böbrekte',
  'bobreklerin': 'böbreklerin',
  'akciger': 'akciğer',
  'akcigerler': 'akciğerler',
  'akcigerde': 'akciğerde',
  'karaciger': 'karaciğer',
  'karacigerde': 'karaciğerde',
  'karacigerin': 'karaciğerin',
  'gogus': 'göğüs',
  'goguste': 'göğüste',
  'gogsun': 'göğsün',
  'bagirsak': 'bağırsak',
  'bagirsaklar': 'bağırsaklar',
  'tiroit': 'tiroit',
  'omurilik': 'omurilik',
  'dalak': 'dalak',
  'ureter': 'üreter',
  'uretra': 'üretra',
  'mesane': 'mesane',
  'ozofagus': 'özofagus',
  'ozefagus': 'özofagus',
  'göz': 'göz',
  'goz': 'göz',
  'kulak': 'kulak',

  // Semptom & Bulgular
  'agri': 'ağrı',
  'agrisi': 'ağrısı',
  'nefes': 'nefes',
  'darligi': 'darlığı',
  'ates': 'ateş',
  'atesi': 'ateşi',
  'atesli': 'ateşli',
  'oksuruk': 'öksürük',
  'balgam': 'balgam',
  'balgami': 'balgamı',
  'kanama': 'kanama',
  'kanamasi': 'kanaması',
  'morarma': 'morarma',
  'sarilik': 'sarılık',
  'sariligi': 'sarılığı',
  'kasinti': 'kaşıntı',
  'kasintisi': 'kaşıntısı',
  'sislik': 'şişlik',
  'sisligi': 'şişliği',
  'odem': 'ödem',
  'odemi': 'ödemi',
  'carpinti': 'çarpıntı',
  'carpintisi': 'çarpıntısı',
  'bulanti': 'bulantı',
  'kusma': 'kusma',
  'ishal': 'ishal',
  'kabizlik': 'kabızlık',
  'halsizlik': 'halsizlik',
  'yorgunluk': 'yorgunluk',
  'istahsizlik': 'iştahsızlık',
  'ufurum': 'üfürüm',
  'ufurumu': 'üfürümü',
  'ronkus': 'ronküs',
  'dokuntu': 'döküntü',
  'dokuntusu': 'döküntüsü',

  // Patoloji & Laboratuvar
  'tumuor': 'tümör',
  'tumor': 'tümör',
  'tumoru': 'tümörü',
  'tumorler': 'tümörler',
  'biyopsi': 'biyopsi',
  'biyopsisi': 'biyopsisi',
  'biyopsisinde': 'biyopsisinde',
  'kreatinin': 'kreatinin',
  'proteinuri': 'proteinüri',
  'proteinurisi': 'proteinürisi',
  'hematuri': 'hematüri',
  'hematurisi': 'hematürisi',
  'lokositoz': 'lökositoz',
  'lokosit': 'lökosit',
  'eritrosit': 'eritrosit',
  'trombosit': 'trombosit',
  'trombositopeni': 'trombositopeni',
  'anemi': 'anemi',
  'kansizlik': 'kansızlık',
  'iltihap': 'iltihap',
  'iltihabi': 'iltihabı',
  'inflamasyon': 'inflamasyon',
  'nekroz': 'nekroz',
  'kresent': 'kresent',
  'granulom': 'granülom',
  'granulomlar': 'granülomlar',
  'granulomatoz': 'granülomatöz',
  'kazeifikasyon': 'kazeifikasyon',

  // Hastalıklar
  'glomerulonefrit': 'glomerülonefrit',
  'glomerulonefriti': 'glomerülonefriti',
  'nefrotik': 'nefrotik',
  'nefritik': 'nefritik',
  'sendrom': 'sendrom',
  'sendromu': 'sendromu',
  'yetmezlik': 'yetmezlik',
  'yetmezligi': 'yetmezliği',
  'yetmezliginde': 'yetmezliğinde',
  'diyabet': 'diyabet',
  'diabet': 'diyabet',
  'hipertansiyon': 'hipertansiyon',
  'hipotansiyon': 'hipotansiyon',
  'tüberküloz': 'tüberküloz',
  'tuberkuloz': 'tüberküloz',
  'pnömoni': 'pnömoni',
  'pnomoni': 'pnömoni',
  'zatürre': 'zatürre',
  'zaturre': 'zatürre',
  'apandisit': 'apandisit',
  'kolesistit': 'kolesistit',
  'hepatit': 'hepatit',
  'siroz': 'siroz',
  'menenjit': 'menenjit',
  'romatoid': 'romatoid',
  'artrit': 'artrit',
  'artriti': 'artriti',
  'osteoartrit': 'osteoartrit',
  'osteoporoz': 'osteoporoz',
  'losemi': 'lösemi',
  'lenfoma': 'lenfoma',

  // Klinik Kavramlar & İlaçlar
  'ilac': 'ilaç',
  'ilaci': 'ilacı',
  'ilaclar': 'ilaçlar',
  'tedavi': 'tedavi',
  'tedavisi': 'tedavisi',
  'tedavisinde': 'tedavisinde',
  'tani': 'tanı',
  'tanisi': 'tanısı',
  'tanisinda': 'tanısında',
  'muayene': 'muayene',
  'muayenesi': 'muayenesi',
  'muayenesinde': 'muayenesinde',
  'tetkik': 'tetkik',
  'tetkiki': 'tetkiki',
  'tetkiklerinde': 'tetkiklerinde',
  'grafi': 'grafi',
  'grafisi': 'grafisi',
  'grafisinde': 'grafisinde',
  'tomografi': 'tomografi',
  'tomografisi': 'tomografisi',
  'tomografisinde': 'tomografisinde',
  'kontrendike': 'kontrendike',
  'endikasyon': 'endikasyon',
  'komplikasyon': 'komplikasyon',
  'komplikasyonu': 'komplikasyonu',
  'prognoz': 'prognoz',
  'prognozu': 'prognozu',
};

/** Sık yapılan harf kayması / yazım hataları düzeltmesi */
export const COMMON_TYPOS: Record<string, string> = {
  'glamerülonefrit': 'glomerülonefrit',
  'glamerulonefrit': 'glomerülonefrit',
  'apandist': 'apandisit',
  'kolesistt': 'kolesistit',
  'enfeksyon': 'enfeksiyon',
  'enfeksiyonu': 'enfeksiyonu',
  'diyabetis': 'diyabet',
  'hipertansion': 'hipertansiyon',
  'kardiak': 'kardiyak',
  'myokard': 'miyokard',
  'asagidakilerden': 'aşağıdakilerden',
  'asagidaki': 'aşağıdaki',
  'hangisidirr': 'hangisidir',
  'hangisidr': 'hangisidir',
  'yanlistir': 'yanlıştır',
  'dogrudur': 'doğrudur',
  'degildir': 'değildir',
};

// ------------------------------------------------------------------------------
// 3. SORU KÖKÜ KAPATMA / YÖNELTME ŞABLONLARI (QUESTION STEM PATTERNS)
// ------------------------------------------------------------------------------

export interface QuestionStemPattern {
  initiators: string[];      // Kullanıcı bu kelimeleri yazdıysa veya soru aşamasındaysa
  stem: string;              // Tam soru yöneltmesi
  contextKeywords?: string[]; // Bütün metinde geçerse ağırlık kazanır
  category: 'tani' | 'tedavi' | 'mekanizma' | 'komplikasyon' | 'oncul' | 'genel';
  weight: number;
}

export const QUESTION_STEM_PATTERNS: QuestionStemPattern[] = [
  // --- Tanı / Ayırıcı Tanı ---
  {
    initiators: ['en olası', 'bu hastada en olası', 'tanı', 'bu hasta için en olası'],
    stem: 'en olası tanı aşağıdakilerden hangisidir?',
    category: 'tani',
    weight: 12,
  },
  {
    initiators: ['kesin tanı', 'kesin tanı için', 'ilk yapılması gereken'],
    stem: 'kesin tanı için yapılması gereken ilk tetkik aşağıdakilerden hangisidir?',
    category: 'tani',
    weight: 11,
  },
  {
    initiators: ['en uygun tanısal', 'tanıyı doğrulamak için'],
    stem: 'tanıyı doğrulamak için en uygun altın standart yöntem hangisidir?',
    category: 'tani',
    weight: 10,
  },
  {
    initiators: ['en olası etken', 'etken mikroorganizma'],
    stem: 'bu klinik tabloya yol açan en olası etken mikroorganizma hangisidir?',
    contextKeywords: ['ateş', 'enfeksiyon', 'kültür', 'bakteri', 'virüs', 'pnömoni', 'menenjit'],
    category: 'tani',
    weight: 11,
  },

  // --- Tedavi / Farmakoloji ---
  {
    initiators: ['tedavisinde ilk', 'tedavisinde ilk tercih', 'ilk tercih edilecek', 'en uygun tedavi'],
    stem: 'tedavisinde ilk basamakta tercih edilmesi gereken ilaç aşağıdakilerden hangisidir?',
    category: 'tedavi',
    weight: 12,
  },
  {
    initiators: ['en uygun ampirik', 'ampirik antibiyotik'],
    stem: 'en uygun ampirik antibiyotik tedavisi aşağıdakilerden hangisidir?',
    contextKeywords: ['enfeksiyon', 'ateş', 'lökositoz', 'antibiyotik'],
    category: 'tedavi',
    weight: 11,
  },
  {
    initiators: ['kontrendike', 'kullanılması kontrendike', 'verilmemesi gereken'],
    stem: 'bu hastanın tedavisinde verilmesi kontrendike olan ilaç hangisidir?',
    category: 'tedavi',
    weight: 10,
  },
  {
    initiators: ['en uygun acil', 'acil tedavi yaklaşımı'],
    stem: 'bu hastada uygulanması gereken en uygun acil tedavi yaklaşımı hangisidir?',
    category: 'tedavi',
    weight: 10,
  },

  // --- Patofizyoloji & Mekanizma ---
  {
    initiators: ['patofizyolojik', 'temel mekanizma', 'sorumlu mekanizma'],
    stem: 'bu klinik tablodan sorumlu olan temel patofizyolojik mekanizma hangisidir?',
    category: 'mekanizma',
    weight: 11,
  },
  {
    initiators: ['hangisinin eksikliği', 'hangisinin mutasyonu'],
    stem: 'aşağıdakilerden hangisinin eksikliği bu klinik tabloya yol açar?',
    category: 'mekanizma',
    weight: 10,
  },
  {
    initiators: ['histopatolojik bulgu', 'biyopside görülmesi'],
    stem: 'yapılacak doku biyopsisinde saptanması en olası histopatolojik bulgu hangisidir?',
    contextKeywords: ['biyopsi', 'patoloji', 'glomerül', 'doku'],
    category: 'mekanizma',
    weight: 10,
  },

  // --- Komplikasyon & Prognoz ---
  {
    initiators: ['en olası komplikasyon', 'gelişmesi en olası'],
    stem: 'bu hastada gelişmesi en olası komplikasyon aşağıdakilerden hangisidir?',
    category: 'komplikasyon',
    weight: 10,
  },
  {
    initiators: ['prognoz', 'prognozu belirleyen'],
    stem: 'hastanın klinik seyrini ve prognozunu belirleyen en önemli faktör hangisidir?',
    category: 'komplikasyon',
    weight: 9,
  },

  // --- Öncüller & Değerlendirmeler ---
  {
    initiators: ['aşağıdakilerden hangisi', 'ifadelerden hangisi yanlıştır'],
    stem: 'bu hastalık ile ilgili aşağıdaki ifadelerden hangisi yanlıştır?',
    category: 'genel',
    weight: 9,
  },
  {
    initiators: ['ifadelerden hangileri doğrudur', 'hangileri doğrudur'],
    stem: 'yukarıdaki ifadelerden hangileri doğrudur?',
    category: 'oncul',
    weight: 9,
  },
  {
    initiators: ['görülmesi beklenmez', 'en az beklenen'],
    stem: 'bu hastada saptanması en az beklenen bulgu aşağıdakilerden hangisidir?',
    category: 'genel',
    weight: 9,
  },
];

// ------------------------------------------------------------------------------
// 4. KELİME & CÜMLE EVRESİ ANALİZİ (PHASE & CONTEXT ENGINE)
// ------------------------------------------------------------------------------

/** Metni Türkçe kurallarına göre küçük harfe katlar */
export function foldTr(s: string): string {
  return s
    .toLocaleLowerCase('tr-TR')
    .replace(/[.,;:!?()"'“”‘’«»\[\]]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/** Cümle içi devam bağlaçları ve ekleri */
const CONTINUATION_TRIGGERS = new Set([
  'ile', 've', 'veya', 'olan', 'olup', 'bulunan', 'gelişen', 'görülen', 'saptanan',
  'yapılan', 'çekilen', 'alınan', 'başvuran', 'gelen', 'nedeniyle', 'sonrasında',
  'esnasında', 'sırasında', 'öyküsü', 'hikayesi', 'yakınması', 'şikayeti',
  'yakınmasıyla', 'şikayetiyle', 'muayenede', 'muayenesinde', 'tetkiklerinde',
  'tahlillerinde', 'grafisinde', 'tomografisinde', 'biyopsisinde', 'düzeyi',
  'seviyesi', 'yüksekliği', 'düşüklüğü', 'hastada', 'olguda', 'hastaya', 'yaşında',
  'yaşındaki', 'bir', 'için', 'olarak', 'gibi', 'sonra', 'önce'
]);

/** Soru kapatma başlatıcıları */
const QUESTION_TRIGGER_STARTERS = [
  'en olası', 'kesin tanı', 'ilk yapılması', 'aşağıdakilerden', 'hangisidir',
  'hangisi', 'tedavisinde', 'tedavisi', 'hangileri', 'nedir', 'değildir',
  'yanlıştır', 'doğrudur', 'beklenmez', 'kontrendike', 'patofizyolojik',
  'bu hastada', 'bu hasta için', 'bu olguda', 'bu durumda'
];

/**
 * Kullanıcının yazdığı metnin şu anki evresini analiz eder:
 *  - isExpanding: Kullanıcı bir vaka, semptom ya da klinik bulgu yazmaya devam ediyor
 *  - isQuestionReady: Kullanıcı cümleyi bitirdi veya soru yöneltmeye geçti
 */
export function analyzeInputPhase(text: string): {
  isExpanding: boolean;
  isQuestionReady: boolean;
  tailWords: string[];
  fullWords: string[];
  lastWord: string;
  endsWithSpace: boolean;
} {
  const trimmed = text.trim();
  const endsWithSpace = /\s$/.test(text);
  const folded = foldTr(text);
  const words = folded.split(' ').filter(Boolean);
  const fullWords = words;
  const tailWords = words.slice(-4);
  const lastWord = words.length ? words[words.length - 1] : '';

  if (!trimmed || words.length === 0) {
    return { isExpanding: true, isQuestionReady: false, tailWords: [], fullWords: [], lastWord: '', endsWithSpace };
  }

  // 1. Kullanıcı açıkça bir soru kapatıcı kalıbı yazmaya başladıysa
  const lowerText = text.toLocaleLowerCase('tr-TR');
  const hasQuestionStarter = QUESTION_TRIGGER_STARTERS.some((qt) => lowerText.includes(qt));
  if (hasQuestionStarter) {
    return { isExpanding: false, isQuestionReady: true, tailWords, fullWords, lastWord, endsWithSpace };
  }

  // 2. Noktalama işareti ile bitmişse (". ", "\n") ve metin yeterince uzunsa
  const endsWithTerminalPunctuation = /[.!?](\s+)?$/.test(text);
  if (endsWithTerminalPunctuation && words.length >= 10) {
    return { isExpanding: false, isQuestionReady: true, tailWords, fullWords, lastWord, endsWithSpace };
  }

  // 3. Son kelime veya son iki kelime bir devam tetikleyicisi ise
  const lastTail = endsWithSpace ? lastWord : (words.length > 1 ? words[words.length - 2] : '');
  const isTailConnecting = CONTINUATION_TRIGGERS.has(lastWord) || CONTINUATION_TRIGGERS.has(lastTail);

  // 4. Kısa metinler (< 15 kelime) ve henüz nokta konmamış metinler varsayılan olarak "ekleme/devam" modundadır
  if (isTailConnecting || words.length < 15 || !endsWithTerminalPunctuation) {
    return { isExpanding: true, isQuestionReady: false, tailWords, fullWords, lastWord, endsWithSpace };
  }

  return { isExpanding: false, isQuestionReady: true, tailWords, fullWords, lastWord, endsWithSpace };
}

// ------------------------------------------------------------------------------
// 5. BÜTÜN CÜMLE BAĞLAMINI ÇIKARMA VE ÖNERİ PUANLAMA
// ------------------------------------------------------------------------------

/** Metinden anahtar tıbbi varlıkları çıkarır */
export function extractEntities(text: string): string[] {
  const folded = foldTr(text);
  const tokens = folded.split(' ').filter((w) => w.length >= 3);
  const entities: string[] = [];

  const KNOWN_MEDICAL_KEYWORDS = [
    'akciğer', 'böbrek', 'karaciğer', 'kalp', 'beyin', 'mide', 'bağırsak', 'tiroit',
    'idrar', 'kan', 'kemik', 'dalak', 'göz', 'deri', 'damar', 'kas',
    'glomerülonefrit', 'nefrotik', 'nefritik', 'diyabet', 'hipertansiyon', 'tüberküloz',
    'pnömoni', 'apandisit', 'kolesistit', 'siroz', 'hepatit', 'menenjit', 'romatoid',
    'artrit', 'lupus', 'sle', 'astım', 'koah', 'emboli', 'infarktüs', 'iskemi',
    'anemi', 'lösemi', 'lenfoma', 'tümör', 'karsinom', 'kanser', 'biyopsi',
    'proteinüri', 'hematüri', 'lökositoz', 'trombositopeni', 'kreatinin', 'üre',
    'sedimentasyon', 'crp', 'troponin', 'ekg', 'grafi', 'tomografi', 'ultrason',
    'ateş', 'öksürük', 'dispne', 'nefes', 'göğüs', 'karın', 'sarılık', 'ödem',
    'üfürüm', 'ral', 'ronküs', 'çarpıntı', 'senkop', 'baş ağrısı', 'döküntü',
    'çocuk', 'kadın', 'erkek', 'bebek', 'gebe', 'yaşında'
  ];

  for (const kw of KNOWN_MEDICAL_KEYWORDS) {
    if (folded.includes(kw) && !entities.includes(kw)) {
      entities.push(kw);
    }
  }

  return entities;
}

// ------------------------------------------------------------------------------
// 6. DERLEM MODELİ (src/data/composer_model.json — scripts/composer/build_composer_model.py)
// ------------------------------------------------------------------------------

export interface ComposerModel {
  v: number;
  /** katlanmış bağlam (1-3 kelime, cümle başı "^") → [[sonraki yüzey kelime, sayı]] */
  ng: Record<string, [string, number][]>;
  /** katlanmış kelime → sayı, ya da yüzey biçim farklıysa [yüzey biçim, sayı] */
  vocab: Record<string, number | [string, number]>;
  /** ASCII biçim → Türkçe karakterli biçim (belirsizliği olmayanlar) */
  acc: Record<string, string>;
}

let MODEL: ComposerModel | null = null;
let loading: Promise<void> | null = null;

/** Modeli tembel yükler (ayrı parça; ana paketi büyütmez). */
export function loadComposerModel(): Promise<void> {
  if (MODEL) return Promise.resolve();
  if (!loading) {
    loading = import('../data/composer_model.json')
      .then((m: any) => { MODEL = (m.default ?? m) as ComposerModel; })
      .catch(() => { loading = null; });
  }
  return loading;
}

const ASCII_TR: Record<string, string> = { ç: 'c', ğ: 'g', ı: 'i', ö: 'o', ş: 's', ü: 'u', â: 'a', î: 'i', û: 'u' };
const toAscii = (w: string) => w.replace(/[çğıöşüâîû]/g, (c) => ASCII_TR[c]);
/** Tek kelimeyi model anahtarına katlar (build_composer_model.py::fold ile aynı) */
const foldWord = (w: string) => w.toLocaleLowerCase('tr-TR').normalize('NFC').replace(/[^\p{L}\p{N}%/+-]/gu, '');
const TR_LETTERS = 'abcçdefgğhıijklmnoöprsştuüvyz';
/** Türkçe Q klavyede komşu tuşlar + aksan çiftleri (yanlış harf düzeltmesinde yalnız bunlar denenir) */
const NEAR: Record<string, string> = {
  a: 'sqz', b: 'vnh', c: 'çxv', ç: 'c.', d: 'sfe', e: 'wrd', f: 'dgr', g: 'ğfh', ğ: 'gpü', h: 'gjy',
  ı: 'iuo', i: 'ıuo', j: 'hku', k: 'jlı', l: 'kş', m: 'nö', n: 'bm', o: 'öıp', ö: 'om', p: 'oğ',
  r: 'et', s: 'şad', ş: 'sli', t: 'ry', u: 'üyı', ü: 'uğ', v: 'cb', y: 'tu', z: 'ax',
};
const CLOSER_RE = /\b(hangisi|hangileri|nedir|değildir|yanlıştır|doğrudur|aşağıdaki)/i;

type Cand = { text: string; score: number; conf: number; src: 'kaynak' | 'model' | 'kalıp' | 'kelime'; first?: string };

// ------------------------------------------------------------------------------
// 7. AKILLI DEVAM VE TAMAMLAMA MOTORU (SMART COMPOSER CORE)
// ------------------------------------------------------------------------------

export class SmartComposerEngine {
  /** Test/simülasyon için modeli doğrudan verir */
  public setModel(m: ComposerModel | null): void { MODEL = m; }
  public hasModel(): boolean { return !!MODEL; }
  /** Hayalet metnin gösterileceği en düşük güven (simülasyonla ayarlandı) */
  public ghostMin = 0.34;

  /**
   * Yazılan metne göre hayalet metin (ghost), seçenekler ve yazım düzeltmesi üretir.
   * İlke: emin olunmayan öneri gösterilmez (yanlış öneri, öneri yokluğundan kötüdür).
   * Sıra: 1) benzer çıkmış soru kökünden birebir devam, 2) derlem n-gram zinciri,
   *       3) açıkça başlatılmış soru kökü kalıbı, 4) yarım kelime tamamlama.
   */
  public getAssist(text: string, sources: string[] = []): AssistResult {
    const raw = text || '';
    if (!raw.trim()) {
      return { ghost: '', ghostType: null, options: [], fix: null, spell: null, isExpanding: true, detectedEntities: [] };
    }
    if (!MODEL) void loadComposerModel();

    const phase = analyzeInputPhase(raw);
    const entities = extractEntities(raw);
    const spell = this.getSpellingCorrection(raw);
    const punct = this.getPunctuationFix(raw, spell?.text || null);
    // Düzelt çipi hem yazım hem noktalama değişikliklerini listeler
    const spellChanges = spell ? spell.changes.map((c) => `${c.from} → ${c.to}`) : [];
    const fix = punct
      ? { text: punct.text, changes: [...spellChanges, ...punct.changes] }
      : spell ? { text: spell.text, changes: spellChanges } : null;

    // Cümle bittiyse (soru işareti) devam önerme
    if (/[?]\s*$/.test(raw)) {
      return { ghost: '', ghostType: null, options: [], fix, spell, isExpanding: false, detectedEntities: entities };
    }

    const endsWithSpace = /\s$/.test(raw);
    const words = raw.trim().split(/\s+/);
    const partial = endsWithSpace ? '' : words[words.length - 1];
    const done = (endsWithSpace ? words : words.slice(0, -1)).map(foldWord).filter(Boolean);
    const pf = foldWord(partial);
    const lead = endsWithSpace || !partial ? '' : ' ';

    const cands: Cand[] = [];
    this.fromSources(done, pf, partial, endsWithSpace, sources, cands);
    this.fromModel(done, pf, partial, endsWithSpace, cands);
    this.fromStemPatterns(raw, endsWithSpace, cands);
    if (!cands.length && pf.length >= 3) this.completeWord(done, pf, partial, cands);

    // Kaynak ile derlem modeli aynı kelimeyle başlıyorsa güven artar, ayrışıyorsa azalır
    const firstOf = (c: Cand) => foldWord((pf ? partial + c.text : c.text).trim().split(/\s+/)[0] || '');
    const modelC = cands.find((c) => c.src === 'model');
    if (modelC) {
      for (const c of cands) {
        if (c.src !== 'kaynak') continue;
        if (firstOf(c) === firstOf(modelC)) { c.conf = Math.min(1, c.conf + 0.25); modelC.conf = Math.min(1, modelC.conf + 0.25); }
        else if (c.conf < 0.7) c.conf *= 0.75;
      }
    }
    // Bozuk kaynak parçalarını (çift boşluk, sayfa artığı) eleme
    for (let i = cands.length - 1; i >= 0; i--) if (/\s{2,}|\.{3,}|_{3,}/.test(cands[i].text.trim())) cands.splice(i, 1);

    // Sırala; aynı metni tekille
    cands.sort((a, b) => b.score - a.score);
    const seen = new Set<string>();
    const uniq = cands.filter((c) => {
      const k = foldTr(c.text);
      if (!k || seen.has(k)) return false;
      seen.add(k);
      return true;
    });

    // Erken soru kapatma koruması: vaka anlatımı sürerken zayıf "hangisidir" önerisini bastır
    const ok = uniq.filter((c) => !(phase.isExpanding && CLOSER_RE.test(c.text) && c.conf < 0.5 && c.src !== 'kalıp'));
    const best = ok[0];
    const ghostOk = !!best && best.conf >= this.ghostMin;
    void lead;

    const options: AssistOption[] = ok.slice(0, 3).map((c, i) => {
      const closes = CLOSER_RE.test(c.text) || /\?\s*$/.test(c.text);
      return {
        type: closes ? 'complete' : 'continue',
        label: closes ? 'Soruyu Tamamla' : i === 0 ? 'Devam Et' : 'Alternatif',
        text: c.text,
        preview: `…${c.text.trim()}`,
        isTop: i === 0,
        category: c.src,
      } as AssistOption;
    });
    const ghost = ghostOk ? best.text : '';
    return {
      ghost,
      ghostType: ghost ? options[0].type : null,
      options,
      fix,
      spell,
      isExpanding: phase.isExpanding,
      detectedEntities: entities,
    };
  }

  /** Benzer çıkmış soru köklerinde yazılanın son kelimelerini bulup birebir devamını önerir */
  private fromSources(done: string[], pf: string, partial: string, endsWithSpace: boolean, sources: string[], out: Cand[]): void {
    if (!done.length && !pf) return;
    const firsts: string[] = [];
    for (const src of sources) {
      const sw = (src || '').trim().split(/\s+/).filter(Boolean);
      const sf = sw.map(foldWord);
      let bestK = 0, bestAt = -1;
      for (let i = 0; i < sw.length; i++) {
        // i: devam edecek kelimenin konumu; i'den önceki k kelime bağlamla eşleşmeli
        let k = 0;
        while (k < done.length && k < 6 && i - 1 - k >= 0 && sf[i - 1 - k] === done[done.length - 1 - k]) k++;
        if (pf) {
          if (!sf[i] || !sf[i].startsWith(pf) || sf[i] === pf && i === sw.length - 1) continue;
        }
        if (k > bestK) { bestK = k; bestAt = i; }
      }
      const minK = pf ? 1 : 2;
      if (bestAt < 0 || bestK < Math.min(minK, done.length) || (bestK === 0 && pf.length < 3)) continue;
      const rest = this.takeSentence(sw, bestAt, 10);
      if (!rest.length) continue;
      let text: string;
      if (pf) {
        const first = rest[0];
        const tail = first.slice(partial.length);
        text = tail + (rest.length > 1 ? ' ' + rest.slice(1).join(' ') : '');
        if (!tail) text = rest.length > 1 ? ' ' + rest.slice(1).join(' ') : '';
      } else {
        text = (endsWithSpace ? '' : ' ') + rest.join(' ');
      }
      if (text.trim().length < 2) continue;
      // Bağlam ne kadar genelse ("aşağıdakilerden hangisi") kaynağın devamı o kadar tahmindir
      let conf = bestK >= 4 ? 0.9 : bestK === 3 ? 0.7 : bestK === 2 ? 0.45 : 0.4;
      const gen = this.contextMass(done.slice(done.length - Math.min(bestK, 3)));
      if (gen > 30 && bestK < 4) conf *= 0.6;
      firsts.push(foldWord(rest[0]));
      out.push({ text, score: 100 + bestK * 20, conf, src: 'kaynak', first: foldWord(rest[0]) });
    }
    // Birden çok kaynak aynı kelimeyle devam ediyorsa güven artar
    for (const c of out) {
      if (c.src !== 'kaynak' || !c.first) continue;
      const agree = firsts.filter((f) => f === c.first).length;
      if (agree >= 2) c.conf = Math.min(1, c.conf + 0.2 * (agree - 1));
    }
  }

  /** Bağlamın derlemdeki toplam geçiş sayısı (genellik ölçüsü) */
  private contextMass(ctx: string[]): number {
    if (!MODEL || !ctx.length) return 0;
    const list = MODEL.ng[ctx.join(' ')];
    return list ? list.reduce((a, [, n]) => a + n, 0) : 0;
  }

  /** Derlem n-gram modeliyle (3→2→1 geri çekilme) güvenli kelime zinciri kurar */
  private fromModel(done: string[], pf: string, partial: string, endsWithSpace: boolean, out: Cand[]): void {
    if (!MODEL) return;
    const ctxWords = ['^', ...done];
    const next = (ctx: string[], prefix: string): { w: string; p: number; n: number; k: number } | null => {
      for (let k = Math.min(3, ctx.length); k >= 1; k--) {
        const key = ctx.slice(ctx.length - k).join(' ');
        let list = MODEL!.ng[key];
        if (!list) continue;
        if (prefix) list = list.filter(([w]) => { const f = foldWord(w); return f.startsWith(prefix) && f !== prefix; });
        if (!list.length) continue;
        const tot = list.reduce((a, [, n]) => a + n, 0);
        const [w, n] = list[0];
        // tek kelimelik bağlam zayıftır: daha sıkı eşik
        if (k === 1 && !prefix && ctx.length > 1 && n / tot < 0.6) return null;
        return { w, p: n / tot, n, k };
      }
      return null;
    };

    const first = next(ctxWords, pf);
    if (!first) return;
    const chain: string[] = [first.w];
    let conf = first.p * (first.k >= 2 ? 1 : 0.7);
    if (first.n < 2) return;
    const ctx = [...ctxWords, foldWord(first.w)];
    while (chain.length < 8 && !/[?.!]$/.test(chain[chain.length - 1])) {
      const nx = next(ctx, '');
      if (!nx || nx.p < 0.55 || nx.k < 2) break;
      chain.push(nx.w);
      ctx.push(foldWord(nx.w));
    }
    let text: string;
    if (pf) {
      const tail = chain[0].slice(partial.length);
      // yüzey biçimi yazılanla aynı harflerle başlamıyorsa (büyük/küçük) katlanmış kuyruğu kullan
      const okTail = foldWord(chain[0]).startsWith(pf) ? chain[0].slice(pf.length) : tail;
      text = okTail + (chain.length > 1 ? ' ' + chain.slice(1).join(' ') : '');
    } else {
      text = (endsWithSpace ? '' : ' ') + chain.join(' ');
    }
    if (!text.trim()) return;
    out.push({ text, score: 50 + conf * 40 + first.k * 5, conf, src: 'model' });
  }

  /** Kullanıcı açıkça bir soru kapatıcıya başladıysa ("en olası", "kesin tanı"…) kalıbı tamamlar */
  private fromStemPatterns(raw: string, endsWithSpace: boolean, out: Cand[]): void {
    const folded = foldTr(raw);
    for (const qp of QUESTION_STEM_PATTERNS) {
      for (const init of qp.initiators) {
        const f = foldTr(init);
        if (!folded.endsWith(' ' + f) && folded !== f) continue;
        const stemF = foldTr(qp.stem);
        if (!stemF.startsWith(f.split(' ').slice(-1)[0])) {
          // kalıp yazılanla örtüşmüyorsa olduğu gibi ekle
          out.push({ text: (endsWithSpace ? '' : ' ') + qp.stem, score: 40 + qp.weight, conf: 0.4, src: 'kalıp' });
        } else {
          const idx = stemF.indexOf(f);
          const rest = idx === 0 ? qp.stem.split(' ').slice(f.split(' ').length).join(' ') : qp.stem;
          if (rest) out.push({ text: (endsWithSpace ? '' : ' ') + rest, score: 40 + qp.weight, conf: 0.4, src: 'kalıp' });
        }
        break;
      }
    }
  }

  /** Yarım kelimeyi derlemdeki en sık kelimeyle tamamlar (yalnız baskın aday varsa) */
  private completeWord(done: string[], pf: string, partial: string, out: Cand[]): void {
    if (!MODEL) return;
    let best: [string, number] | null = null, second = 0;
    for (const [f, v] of Object.entries(MODEL.vocab)) {
      if (f.length <= pf.length || !f.startsWith(pf)) continue;
      const [w, n] = typeof v === 'number' ? [f, v] : v;
      if (!best || n > best[1]) { second = best ? best[1] : second; best = [w, n]; }
      else if (n > second) second = n;
    }
    if (!best || best[1] < 5 || best[1] < second * 2) return;
    void done; void partial;
    out.push({ text: best[0].slice(pf.length), score: 20, conf: 0.35, src: 'kelime' });
  }

  private takeSentence(sw: string[], from: number, max: number): string[] {
    const cut: string[] = [];
    for (let i = from; i < sw.length && cut.length < max; i++) {
      cut.push(sw[i]);
      if (/[?.!]$/.test(sw[i])) break;
    }
    return cut;
  }

  // --------------------------------------------------------------------------
  // YAZIM DÜZELTME
  // --------------------------------------------------------------------------

  /**
   * Güvenli Türkçe/tıbbi yazım düzeltmesi.
   *  - Derlemde geçen (bilinen) kelimeye asla dokunmaz.
   *  - Türkçe karakter eksikliği: yalnız ASCII biçimi derlemde kendi başına geçmiyorsa.
   *  - Harf hatası: 1 düzenleme uzaklığındaki (düşme, yer değiştirme, çiftleme, yanlış harf)
   *    tek baskın derlem kelimesine.
   *  - Henüz yazılmakta olan son kelimeye dokunmaz.
   */
  public getSpellingCorrection(
    text: string
  ): { text: string; changes: { from: string; to: string }[] } | null {
    if (!text || text.trim().length < 3) return null;
    const changes: Array<{ from: string; to: string }> = [];
    const asciiText = !/[çğıöşüÇĞİÖŞÜ]/.test(text);
    const typing = /[\p{L}]$/u.test(text);
    let lastIdx = -1;
    if (typing) { const m = text.match(/[\p{L}]+$/u); lastIdx = m ? text.length - m[0].length : -1; }

    const fixed = text.replace(/[\p{L}]{3,}/gu, (word, offset: number) => {
      if (offset === lastIdx) return word;
      const to = this.correctWord(word, asciiText);
      if (to && to !== word) { changes.push({ from: word, to }); return to; }
      return word;
    });
    return changes.length > 0 ? { text: fixed, changes } : null;
  }

  private known(f: string): number {
    const v = MODEL?.vocab[f];
    return v === undefined ? 0 : typeof v === 'number' ? v : v[1];
  }

  private correctWord(word: string, asciiText = false): string | null {
    let lower = word.toLocaleLowerCase('tr-TR');
    // Aksansız metinde baştaki "I" çoğunlukla "İ"dir ("Izleminde")
    if (asciiText && word[0] === 'I' && !this.known(lower) && !MODEL?.acc[lower]) lower = 'i' + lower.slice(1);
    // Kısaltma (CRP, EKG) ve sayılı ifadeler
    if (word.length <= 5 && word === word.toLocaleUpperCase('tr-TR')) return null;

    if (COMMON_TYPOS[lower]) return this.preserveCase(word, COMMON_TYPOS[lower]);

    const own = this.known(lower);
    // Türkçe karakter geri kazanımı
    const accTo = MODEL?.acc[lower] ?? (own ? undefined : MEDICAL_ACCENT_RESTORES[lower]);
    if (accTo && accTo !== lower) return this.preserveCase(word, accTo);
    if (own >= 1 || MEDICAL_ACCENT_RESTORES[lower] === lower) return null;
    if (!MODEL || lower.length < 5) return null;

    // Bilinen bir gövde + ek ise ("enfeksiyon|lu", "memede|n") geçerli çekim olabilir
    let stemmed = false;
    for (let k = lower.length - 1; k >= Math.max(5, lower.length - 4); k--) {
      if (this.known(lower.slice(0, k)) >= 2) { stemmed = true; break; }
    }
    // Türkçe karakterlerin hiç kullanılmadığı metinde ASCII kelime büyük olasılıkla aksansız
    // yazılmış geçerli bir çekimdir ("olmadi"); harf düzeltmesi yanlış kelimeye kayar.
    const cand = new Map<string, number>();
    const consider = (c: string, min: number) => {
      const n = this.known(c);
      if (n >= min) cand.set(c, Math.max(cand.get(c) ?? 0, n));
      const a = MODEL!.acc[c];
      if (a) { const m = this.known(a); if (m >= min) cand.set(a, Math.max(cand.get(a) ?? 0, m)); }
    };
    const L = lower.length;
    if (asciiText && toAscii(lower) === lower) {
      for (let i = 1; i < L; i++) if (lower[i] === lower[i - 1]) consider(lower.slice(0, i) + lower.slice(i + 1), 3);
      if (!cand.size) return null;
    } else {
      for (let i = 0; i < L - 1; i++) consider(lower.slice(0, i) + lower[i + 1] + lower[i] + lower.slice(i + 2), 3); // yer değiştirme
      for (let i = 1; i < L; i++) {                                                                                     // fazla harf
        if (lower[i] === lower[i - 1]) consider(lower.slice(0, i) + lower.slice(i + 1), 3);        // çiftlenmiş harf ("hangii")
        else if (!stemmed) consider(lower.slice(0, i) + lower.slice(i + 1), 8);
    }
    for (let i = 1; i <= L; i++) for (const ch of TR_LETTERS) consider(lower.slice(0, i) + ch + lower.slice(i), 8);   // eksik harf
    if (!stemmed) for (let i = 0; i < L; i++) for (const ch of NEAR[lower[i]] ?? '') consider(lower.slice(0, i) + ch + lower.slice(i + 1), 8); // komşu tuş / aksan
    }
    if (!cand.size) return null;
    const ranked = [...cand.entries()].sort((a, b) => b[1] - a[1]);
    const [bw, bn] = ranked[0];
    const second = ranked[1]?.[1] ?? 0;
    if (bn < 3 || bn < second * 3) return null;
    // Aday, yazılanın başı ise (yazılan = aday + ek) çekimdir
    if (lower.startsWith(bw) && lower[bw.length] !== lower[bw.length - 1]) return null;
    return this.preserveCase(word, bw);
  }

  /** Noktalama, çift boşluk ve büyük harf biçimlendirme */
  public getPunctuationFix(
    text: string,
    spelledText: string | null
  ): { text: string; changes: string[] } | null {
    const changes: string[] = [];
    let t = spelledText ?? text;

    if (/[ \t]{2,}/.test(t)) {
      t = t.replace(/[ \t]{2,}/g, ' ');
      changes.push('çift boşluk → tek boşluk');
    }

    const sp = t.match(/(\S+)\s+([?.!,;:])/);
    if (sp) {
      t = t.replace(/\s+([?.!,;:])/g, '$1');
      changes.push(`${sp[1]} ${sp[2]} → ${sp[1]}${sp[2]}`);
    }

    const first = t.match(/^(\s*)(\p{Ll}\S*)/u);
    if (first) {
      const w = first[2];
      const W = w.charAt(0).toLocaleUpperCase('tr-TR') + w.slice(1);
      t = first[1] + W + t.slice(first[0].length);
      changes.push(`${w} → ${W}`);
    }

    const q = t.trimEnd().match(/(\S+)$/);
    if (q && /^(hangisidir|hangisi|hangileridir|hangileri|nedir|değildir|yanlıştır|doğrudur)$/i.test(q[1])) {
      t = t.trimEnd() + '?';
      changes.push(`${q[1]} → ${q[1]}?`);
    }

    return changes.length > 0 ? { text: t, changes } : null;
  }

  private preserveCase(orig: string, target: string): string {
    if (orig.length > 1 && orig === orig.toLocaleUpperCase('tr-TR')) {
      return target.toLocaleUpperCase('tr-TR');
    }
    if (orig[0] === orig[0].toLocaleUpperCase('tr-TR')) {
      return target.charAt(0).toLocaleUpperCase('tr-TR') + target.slice(1);
    }
    return target;
  }
}

// Global Singleton
export const smartComposerService = new SmartComposerEngine();
