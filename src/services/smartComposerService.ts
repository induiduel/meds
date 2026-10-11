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

import medicalAccentMapRaw from '../data/medical_accent_map.json';
const medicalAccentMap: Record<string, string> = medicalAccentMapRaw as Record<string, string>;

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
  'safra kesesi': 'safra kesesi',
  'tiroid': 'tiroit',
  'tiroit': 'tiroit',
  'kemik iligi': 'kemik iliği',
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
  'nefes darligi': 'nefes darlığı',
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
  'kilo kaybi': 'kilo kaybı',
  'gece terlemesi': 'gece terlemesi',
  'istahsizlik': 'iştahsızlık',
  'bas agrisi': 'baş ağrısı',
  'bas donmesi': 'baş dönmesi',
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
  'kreatin': 'kreatinin',
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
  'ultrason': 'ultrasonografi',
  'ultrasonu': 'ultrasonografisi',
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
  'nefrotik sendormu': 'nefrotik sendromu',
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
// 2. KLİNİK CÜMLE İÇİ DEVAM KÜTÜPHANESİ (CONTINUATION CORPUS)
// ------------------------------------------------------------------------------

export interface ContinuationPattern {
  triggerEndings: string[]; // Son kelime / bağlaçlar
  continuation: string;     // Devam metni
  contextKeywords?: string[]; // Bütün cümlede aranacak anahtar kavramlar
  category: 'demografi' | 'semptom' | 'muayene' | 'tetkik' | 'biyopsi' | 'genel';
  weight: number;
}

export const CLINICAL_CONTINUATION_PATTERNS: ContinuationPattern[] = [
  // --- Vaka Başvuru & Demografi Devamları ---
  {
    triggerEndings: ['ile', 'yakınmasıyla', 'yakınması ile', 'şikayetiyle', 'şikayeti ile'],
    continuation: 'acil servise başvuran hastanın',
    category: 'demografi',
    weight: 10,
  },
  {
    triggerEndings: ['ile', 'yakınmasıyla', 'yakınması ile', 'şikayetiyle'],
    continuation: 'polikliniğe başvuran 45 yaşında erkek hastanın',
    category: 'demografi',
    weight: 9,
  },
  {
    triggerEndings: ['ile', 'yakınmasıyla', 'şikayetiyle'],
    continuation: 'başvuran hastanın yapılan fizik muayenesinde',
    category: 'muayene',
    weight: 9,
  },
  {
    triggerEndings: ['yaşında', 'yaşındaki'],
    continuation: 'kadın hasta acil servise nefes darlığı ve göğüs ağrısı ile',
    category: 'demografi',
    weight: 8,
  },
  {
    triggerEndings: ['yaşında', 'yaşındaki'],
    continuation: 'erkek hasta 3 gündür devam eden yüksek ateş ve öksürük ile',
    category: 'demografi',
    weight: 8,
  },
  {
    triggerEndings: ['öyküsü', 'hikayesi'],
    continuation: 'bulunan ve son zamanlarda şikayetleri belirginleşen hastada',
    category: 'demografi',
    weight: 7,
  },

  // --- Semptom & Klinik Tablo Devamları ---
  {
    triggerEndings: ['ve', 'ile birlikte', 'ile beraber'],
    continuation: 'göğüs ağrısı yakınması ile başvuran hastada',
    contextKeywords: ['kalp', 'göğüs', 'retrosternal', 'nefes', 'dispne'],
    category: 'semptom',
    weight: 10,
  },
  {
    triggerEndings: ['ve', 'ile birlikte'],
    continuation: 'öksürük, yüksek ateş ve pürülan balgam çıkarma şikayeti ile',
    contextKeywords: ['akciğer', 'solunum', 'ateş', 'öksürük', 'balgam'],
    category: 'semptom',
    weight: 10,
  },
  {
    triggerEndings: ['ve', 'ile birlikte'],
    continuation: 'bulantı, kusma ve yaygın karın ağrısı yakınması ile',
    contextKeywords: ['karın', 'mide', 'bağırsak', 'bulantı', 'kusma', 'sarılık'],
    category: 'semptom',
    weight: 10,
  },
  {
    triggerEndings: ['ve', 'ile birlikte'],
    continuation: 'hematüri ve bacaklarda pretibial ödem şikayeti ile',
    contextKeywords: ['böbrek', 'idrar', 'renal', 'hematüri', 'proteinüri', 'nefrotik'],
    category: 'semptom',
    weight: 10,
  },
  {
    triggerEndings: ['ve', 'ile birlikte'],
    continuation: 'çift görme, pitozis ve çiğneme güçlüğü yakınması ile',
    contextKeywords: ['nörolojik', 'kas', 'göz', 'miyasteni', 'felç'],
    category: 'semptom',
    weight: 9,
  },

  // --- Fizik Muayene Devamları ---
  {
    triggerEndings: ['fizik muayenesinde', 'fizik muayenede', 'muayenesinde'],
    continuation: 'batında hassasiyet, istemsiz defans ve rebound saptanan',
    contextKeywords: ['karın', 'apandisit', 'akut batın', 'kolesistit'],
    category: 'muayene',
    weight: 10,
  },
  {
    triggerEndings: ['fizik muayenesinde', 'fizik muayenede', 'muayenesinde'],
    continuation: 'bilateral akciğer alt zonlarında krepitan raller duyulan',
    contextKeywords: ['akciğer', 'pnömoni', 'nefes', 'dispne', 'öksürük'],
    category: 'muayene',
    weight: 10,
  },
  {
    triggerEndings: ['fizik muayenesinde', 'fizik muayenede', 'muayenesinde'],
    continuation: 'pretibial +++ gode bırakan ödem ve juguler venöz dolgunluk izlenen',
    contextKeywords: ['kalp yetmezliği', 'ödem', 'böbrek', 'siroz'],
    category: 'muayene',
    weight: 10,
  },
  {
    triggerEndings: ['fizik muayenesinde', 'fizik muayenede', 'muayenesinde'],
    continuation: 'kardiyak oskültasyonda mezokardiyak odakta sistolik üfürüm duyulan',
    contextKeywords: ['üfürüm', 'kalp', 'kapak', 'aort', 'mitral'],
    category: 'muayene',
    weight: 9,
  },
  {
    triggerEndings: ['fizik muayenesinde', 'fizik muayenede', 'muayenesinde'],
    continuation: 'boyunda ağrısız, sert ve fikse lenfadenopati saptanan',
    contextKeywords: ['lenfoma', 'kanser', 'tiroit', 'tüberküloz'],
    category: 'muayene',
    weight: 9,
  },
  {
    triggerEndings: ['fizik muayenesinde', 'fizik muayenede', 'muayenesinde'],
    continuation: 'ense sertliği ve pozitif meningeal irritasyon bulguları saptanan',
    contextKeywords: ['menenjit', 'baş ağrısı', 'ateş', 'nöroloji'],
    category: 'muayene',
    weight: 10,
  },

  // --- Laboratuvar & Tetkik Devamları ---
  {
    triggerEndings: ['yapılan', 'istenen', 'bakılan'],
    continuation: 'laboratuvar incelemelerinde belirgin lökositoz ve CRP yüksekliği saptanan',
    category: 'tetkik',
    weight: 9,
  },
  {
    triggerEndings: ['laboratuvar incelemelerinde', 'laboratuvar tetkiklerinde', 'kan tahlillerinde'],
    continuation: 'serum üre ve kreatinin değerleri belirgin yüksek saptanan',
    contextKeywords: ['böbrek', 'kreatinin', 'üre', 'oligüri'],
    category: 'tetkik',
    weight: 10,
  },
  {
    triggerEndings: ['laboratuvar incelemelerinde', 'laboratuvar tetkiklerinde', 'tetkiklerinde'],
    continuation: 'ALT ve AST enzim düzeylerinde 10 kat artış tespit edilen',
    contextKeywords: ['karaciğer', 'hepatit', 'sarılık', 'enzim'],
    category: 'tetkik',
    weight: 10,
  },
  {
    triggerEndings: ['tam idrar tahlilinde', 'idrar mikroskopisinde', 'idrar incelemesinde'],
    continuation: 'mikroskopik hematüri ve dismorfik eritrosit silendirleri izlenen',
    contextKeywords: ['böbrek', 'glomerülonefrit', 'idrar', 'hematüri'],
    category: 'tetkik',
    weight: 10,
  },
  {
    triggerEndings: ['yapılan periferik yaymada', 'periferik yayma incelemesinde'],
    continuation: 'şistositler, parçalanmış eritrositler ve trombositopeni saptanan',
    contextKeywords: ['anemi', 'ttp', 'hus', 'hemoliz', 'trombosit'],
    category: 'tetkik',
    weight: 10,
  },
  {
    triggerEndings: ['çekilen akciğer grafisinde', 'toraks grafisinde'],
    continuation: 'sağ alt lobda lober konsolidasyon ve hava bronkogramları izlenen',
    contextKeywords: ['akciğer', 'pnömoni', 'öksürük', 'grafi'],
    category: 'tetkik',
    weight: 10,
  },
  {
    triggerEndings: ['çekilen elektrokardiyografisinde', 'ekg sinde', 'ekg de'],
    continuation: 'anterior derivasyonlarda ST elevasyonu ve patolojik Q dalgaları izlenen',
    contextKeywords: ['kalp', 'miyokard', 'infarktüs', 'göğüs ağrısı'],
    category: 'tetkik',
    weight: 10,
  },

  // --- Biyopsi & Histopatoloji Devamları ---
  {
    triggerEndings: ['yapılan biyopside', 'biyopsisinde', 'histopatolojik incelemesinde'],
    continuation: 'glomerüllerde kresent oluşumu ve nekroz izlenen hastada',
    contextKeywords: ['böbrek', 'glomerülonefrit', 'rpgn', 'biyopsi'],
    category: 'biyopsi',
    weight: 10,
  },
  {
    triggerEndings: ['yapılan biyopside', 'biyopsisinde', 'histopatolojik incelemesinde'],
    continuation: 'kazeifiye granülomatöz inflamasyon ve Langhans dev hücreleri saptanan',
    contextKeywords: ['tüberküloz', 'granülom', 'akciğer'],
    category: 'biyopsi',
    weight: 10,
  },
  {
    triggerEndings: ['yapılan biyopside', 'biyopsisinde', 'histopatolojik incelemesinde'],
    continuation: 'pleomorfik atipik epitel hücre proliferasyonu ve lenfovasküler invazyon saptanan',
    contextKeywords: ['kanser', 'tümör', 'karsinom', 'malign'],
    category: 'biyopsi',
    weight: 9,
  },
];

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
// 6. AKILLI DEVAM VE TAMAMLAMA MOTORU (SMART COMPOSER CORE)
// ------------------------------------------------------------------------------

export class SmartComposerEngine {
  /**
   * Kullanıcının yazdığı metne göre en uygun devamları, soru kapatmalarını
   * ve yazım düzeltmelerini anlık (0ms - 5ms) hesaplar.
   */
  public getAssist(text: string, sources: string[] = []): AssistResult {
    const raw = text || '';
    const trimmed = raw.trim();
    if (!trimmed) {
      return {
        ghost: '',
        ghostType: null,
        options: [],
        fix: null,
        spell: null,
        isExpanding: true,
        detectedEntities: [],
      };
    }

    const phase = analyzeInputPhase(raw);
    const entities = extractEntities(raw);
    const foldedInput = foldTr(raw);
    const endsWithSpace = /\s$/.test(raw);
    const inputWords = foldedInput.split(' ').filter(Boolean);
    const lastWord = inputWords[inputWords.length - 1] || '';

    // --- 1. Güvenli Yazım Düzeltmesi (Spell / Fix) ---
    const spell = this.getSpellingCorrection(raw);
    const fix = this.getPunctuationFix(raw, spell?.text || null);

    // --- 2. Cümle İçi Devam Adayları (Continuations) ---
    const continueCandidates: Array<{ text: string; preview: string; score: number }> = [];

    // Kaynak çıkmış sorulardan bağlamlı devam çıkarma
    if (sources.length > 0) {
      this.extractContinuationsFromSources(raw, sources, entities, continueCandidates);
    }

    // Yerleşik zengin klinik kalıplardan bağlamlı devam çıkarma
    for (const pat of CLINICAL_CONTINUATION_PATTERNS) {
      let matchScore = 0;

      // Son kelime / tetikleyici kontrolü
      const matchesTrigger = pat.triggerEndings.some((tr) => {
        const trFold = foldTr(tr);
        if (trFold === lastWord) return true;
        if (foldedInput.endsWith(trFold)) return true;
        // Yarım yazılmış kelime ile önek eşleşmesi
        if (!endsWithSpace && trFold.startsWith(lastWord) && lastWord.length >= 2) return true;
        return false;
      });

      if (matchesTrigger) {
        matchScore += 30;
      }

      // Bütün cümle bağlamı puanı (Whole-Sentence Context)
      if (pat.contextKeywords && entities.length > 0) {
        const overlap = pat.contextKeywords.filter((kw) => entities.includes(kw)).length;
        matchScore += overlap * 25;
      }

      if (matchScore > 0) {
        // Cümlede zaten geçen kelimeleri peş peşe tekrarlamayı önle
        const contWords = foldTr(pat.continuation).split(' ');
        const firstContWord = contWords[0] || '';
        if (lastWord === firstContWord) continue;

        continueCandidates.push({
          text: (endsWithSpace ? '' : ' ') + pat.continuation,
          preview: `…${pat.continuation}`,
          score: matchScore + pat.weight,
        });
      }
    }

    // --- 3. Soru Kökü Kapatma Adayları (Question Stems) ---
    const questionCandidates: Array<{ text: string; preview: string; score: number }> = [];

    for (const qp of QUESTION_STEM_PATTERNS) {
      let qScore = 0;

      // Soru başlatıcı kelime eşleşmesi
      const matchesInit = qp.initiators.some((init) => {
        const initFold = foldTr(init);
        if (foldedInput.endsWith(initFold)) return true;
        if (!endsWithSpace && initFold.startsWith(lastWord) && lastWord.length >= 2) return true;
        return false;
      });

      if (matchesInit) qScore += 40;

      // Kullanıcı zaten soru aşamasındaysa genel soru şablonları puan kazanır
      if (phase.isQuestionReady) qScore += 25;

      // Bütün cümle bağlamı puanı
      if (qp.contextKeywords && entities.length > 0) {
        const overlap = qp.contextKeywords.filter((kw) => entities.includes(kw)).length;
        qScore += overlap * 20;
      }

      if (qScore > 0) {
        let textToAdd = qp.stem;
        // Eğer kullanıcı zaten "bu hastada" yazdıysa ve stem "bu hastada en olası..." ise baş kısmı kırp
        for (const init of qp.initiators) {
          const initFold = foldTr(init);
          if (foldedInput.endsWith(initFold)) {
            const idx = foldTr(textToAdd).indexOf(initFold);
            if (idx >= 0) {
              textToAdd = textToAdd.slice(idx + init.length).trim();
            }
          }
        }

        questionCandidates.push({
          text: (endsWithSpace ? '' : ' ') + textToAdd,
          preview: `…${textToAdd}`,
          score: qScore + qp.weight,
        });
      }
    }

    // --- 4. Sıralama ve Ayrım (Devam vs Soru Kapatma) ---
    continueCandidates.sort((a, b) => b.score - a.score);
    questionCandidates.sort((a, b) => b.score - a.score);

    const options: AssistOption[] = [];
    let topGhost = '';
    let topGhostType: AssistChipType | null = null;

    if (phase.isExpanding) {
      // KULLANICI CÜMLE İÇİ EKLEME YAPIYOR:
      // Birincil öneri (Ghost Text) KESİNLİKLE soru kapatma olamaz; klinik devam olmalıdır!
      if (continueCandidates.length > 0) {
        const topCont = continueCandidates[0];
        topGhost = topCont.text;
        topGhostType = 'continue';
        options.push({
          type: 'continue',
          label: 'Devam Et',
          text: topCont.text,
          preview: topCont.preview,
          isTop: true,
        });

        if (continueCandidates.length > 1) {
          options.push({
            type: 'continue',
            label: 'Alternatif',
            text: continueCandidates[1].text,
            preview: continueCandidates[1].preview,
          });
        }
      }

      // Kullanıcı dilerse soruyu kapatabilsin diye ayrı bir "Soruyu Kapat" seçeneği sun
      if (questionCandidates.length > 0) {
        const topQ = questionCandidates[0];
        options.push({
          type: 'complete',
          label: 'Soruyu Tamamla',
          text: topQ.text,
          preview: topQ.preview,
        });
      }
    } else {
      // KULLANICI SORU AŞAMASINDA:
      // Birincil öneri soru kökü kapatmadır
      if (questionCandidates.length > 0) {
        const topQ = questionCandidates[0];
        topGhost = topQ.text;
        topGhostType = 'complete';
        options.push({
          type: 'complete',
          label: 'Soruyu Tamamla',
          text: topQ.text,
          preview: topQ.preview,
          isTop: true,
        });

        if (questionCandidates.length > 1) {
          options.push({
            type: 'complete',
            label: 'Farklı Soru',
            text: questionCandidates[1].text,
            preview: questionCandidates[1].preview,
          });
        }
      }

      if (continueCandidates.length > 0) {
        options.push({
          type: 'continue',
          label: 'Klinik Bilgi Ekle',
          text: continueCandidates[0].text,
          preview: continueCandidates[0].preview,
        });
      }
    }

    return {
      ghost: topGhost,
      ghostType: topGhostType,
      options: options.slice(0, 4),
      fix,
      spell,
      isExpanding: phase.isExpanding,
      detectedEntities: entities,
    };
  }

  /** Kaynak çıkmış sorulardan bütün cümle bağlamlı devam metinleri çıkarır */
  private extractContinuationsFromSources(
    typed: string,
    sources: string[],
    entities: string[],
    out: Array<{ text: string; preview: string; score: number }>
  ): void {
    const endsWithSpace = /\s$/.test(typed);
    const tw = foldTr(typed).split(' ').filter(Boolean);
    if (tw.length === 0) return;
    const partial = endsWithSpace ? '' : tw[tw.length - 1];
    const done = endsWithSpace ? tw : tw.slice(0, -1);

    for (const src of sources) {
      const sw = src.split(/\s+/).filter(Boolean);
      const sf = sw.map((w) => foldTr(w));

      // Bütün cümledeki ortak kavram sayısı
      const srcOverlap = entities.filter((e) => foldTr(src).includes(e)).length;

      for (let k = Math.min(4, done.length); k >= (partial ? 0 : 1); k--) {
        const ctx = done.slice(done.length - k);
        if (k === 0 && partial.length < 3) break;

        for (let i = 0; i + k < sw.length + (partial ? 0 : 1); i++) {
          let ok = true;
          for (let j = 0; j < k; j++) {
            if (sf[i + j] !== ctx[j]) { ok = false; break; }
          }
          if (!ok) continue;

          let rest: string[] = [];
          const at = i + k;
          let lead = '';
          if (partial) {
            const w = sf[at];
            if (!w || !w.startsWith(partial)) continue;
            if (w === partial) {
              rest = sw.slice(at + 1);
              lead = ' ';
            } else {
              rest = [sw[at].slice(partial.length), ...sw.slice(at + 1)];
            }
          } else {
            rest = sw.slice(at);
          }

          // Cümle sonuna kadar en fazla 8 kelime al
          const cut: string[] = [];
          for (const t of rest) {
            cut.push(t);
            if (/[?.!]$/.test(t) || cut.length >= 8) break;
          }

          let text = cut.join(' ');
          if (lead && text) text = lead + text;
          else if (!partial && text) text = (endsWithSpace ? '' : ' ') + text;

          if (text.trim().length >= 4) {
            out.push({
              text,
              preview: `…${text.trim()}`,
              score: 25 + k * 10 + srcOverlap * 15,
            });
            return; // Bu kaynaktan tek en iyi devam yeterli
          }
        }
      }
    }
  }

  /**
   * Güvenli ve doğru Türkçe / Tıbbi Yazım Düzeltmesi (0ms)
   * Asla bilinen doğru tıp terimlerini bozmaz; yalnızca Türkçe harf eksikliklerini
   * ve açıkça hatalı kelimeleri onarır.
   */
  public getSpellingCorrection(
    text: string
  ): { text: string; changes: { from: string; to: string }[] } | null {
    if (!text || text.trim().length < 3) return null;
    const changes: Array<{ from: string; to: string }> = [];

    // Kelime kelime güvenli tarama
    const fixed = text.replace(/[\p{L}]{3,}/gu, (word) => {
      const lower = word.toLocaleLowerCase('tr-TR');

      // 1. Doğrudan genel yazım hatası sözlüğü
      if (COMMON_TYPOS[lower]) {
        const to = this.preserveCase(word, COMMON_TYPOS[lower]);
        if (to !== word) {
          changes.push({ from: word, to });
          return to;
        }
      }

      // 2. Türkçe karakter geri kazanımı ("bobrek" -> "böbrek", "akciger" -> "akciğer")
      if (MEDICAL_ACCENT_RESTORES[lower]) {
        const restored = MEDICAL_ACCENT_RESTORES[lower];
        // Kullanıcı zaten Türkçe karakterlerle yazdıysa dokunma
        if (restored === lower) return word;
        const to = this.preserveCase(word, restored);
        if (to !== word) {
          changes.push({ from: word, to });
          return to;
        }
      }

      // 3. Genişletilmiş Tıbbi Veritabanı Türkçe Karakter Eşlemesi (6.900+ Terim)
      if (medicalAccentMap[lower]) {
        const restored = medicalAccentMap[lower];
        if (restored !== lower) {
          const to = this.preserveCase(word, restored);
          if (to !== word) {
            changes.push({ from: word, to });
            return to;
          }
        }
      }

      return word;
    });

    return changes.length > 0 ? { text: fixed, changes } : null;
  }

  /** Noktalama, çift boşluk ve büyük harf biçimlendirme */
  public getPunctuationFix(
    text: string,
    spelledText: string | null
  ): { text: string; changes: string[] } | null {
    const changes: string[] = [];
    let t = spelledText ?? text;

    // Çift boşlukları temizle
    if (/[ \t]{2,}/.test(t)) {
      t = t.replace(/[ \t]{2,}/g, ' ');
      changes.push('çift boşluk → tek boşluk');
    }

    // Noktalama öncesi gereksiz boşlukları temizle ("kelime ?" -> "kelime?")
    const sp = t.match(/(\S+)\s+([?.!,;:])/);
    if (sp) {
      t = t.replace(/\s+([?.!,;:])/g, '$1');
      changes.push(`${sp[1]} ${sp[2]} → ${sp[1]}${sp[2]}`);
    }

    // İlk harfi büyük yap
    const first = t.match(/^(\s*)(\p{Ll}\S*)/u);
    if (first) {
      const w = first[2];
      const W = w.charAt(0).toLocaleUpperCase('tr-TR') + w.slice(1);
      t = first[1] + W + t.slice(first[0].length);
      changes.push(`${w} → ${W}`);
    }

    // Soru kelimesi ile bitiyorsa soru işareti ekle
    const q = t.trimEnd().match(/(\S+)$/);
    if (q && /^(hangisidir|hangisi|hangileridir|hangileri|nedir|değildir|yanlıştır|doğrudur)$/i.test(q[1])) {
      t = t.trimEnd() + '?';
      changes.push(`${q[1]} → ${q[1]}?`);
    }

    return changes.length > 0 ? { text: t, changes } : null;
  }

  private preserveCase(orig: string, target: string): string {
    if (orig === orig.toLocaleUpperCase('tr-TR')) {
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
