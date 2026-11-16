# -*- coding: utf-8 -*-
"""
Master Learning Deck Generator - Batch 4:
Akut Enflamasyon: Vasküler Değişiklikler ve Hücresel Olaylar
Prof. Dr. Hikmet Keleş - Tıbbi Patoloji (Dönem 3 Kurul 1)
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

decks_file = 'src/data/interactive_learning_decks.json'
meta_file = 'src/data/learning_decks_meta.json'
past_q_file = 'src/data/pastQuestions.json'

with open(decks_file, 'r', encoding='utf-8') as f:
    existing_decks = json.load(f)

with open(past_q_file, 'r', encoding='utf-8') as f:
    all_past_questions = json.load(f)

print(f"Mevcut {len(existing_decks)} deste ve {len(all_past_questions)} çıkmış soru yüklendi.")

# Gerçek kurul sorularının eşleştirilmesi
def find_q(target_id):
    for q in all_past_questions:
        if q.get('id') == target_id:
            return q
    return None

q_kardinal = find_q('d3-k1-pat-015') or {
    'id': 'd3-k1-pat-015',
    'examYear': '2021-2026',
    'committeeId': 'Kurul 1',
    'discipline': 'Tıbbi Patoloji',
    'topic': 'Enflamasyonun Kardinal Belirtileri',
    'stem': 'Aşağıdakilerden hangisi akut enflamasyonun klasik kardinal belirtilerinden biri DEĞİLDİR?',
    'options': [
        {'key': 'A', 'text': 'Rubor (Kızarıklık)'},
        {'key': 'B', 'text': 'Calor (Sıcaklık artışı)'},
        {'key': 'C', 'text': 'Tumor (Şişlik)'},
        {'key': 'D', 'text': 'Nekroz (Hücre ölümü)', 'isCorrect': True},
        {'key': 'E', 'text': 'Functio laesa (Fonksiyon kaybı)'}
    ],
    'correctAnswer': 'D',
    'explanation': 'Akut enflamasyonun klasik 5 kardinal bulgusu: Rubor (kızarıklık), Calor (sıcaklık artışı), Tumor (şişlik), Dolor (ağrı) ve Functio Laesa\'dır (fonksiyon kaybı - Virchow tarafından eklenmiştir). Nekroz ise enflamasyonun bir kardinal bulgusu değil, etkenin veya hasarın yol açtığı hücresel bir patolojidir.'
}

q_lokosit_hareket = find_q('d3-k1-pat-017') or {
    'id': 'd3-k1-pat-017',
    'examYear': '2021-2026',
    'committeeId': 'Kurul 1',
    'discipline': 'Tıbbi Patoloji',
    'topic': 'Lökosit Göç Aşamaları',
    'stem': 'İnflamasyon sırasında lökositlerin damar lümeninden hasarlı dokuya göçü sırasında izlediği doğru hareket sıralaması aşağıdakilerden hangisidir?',
    'options': [
        {'key': 'A', 'text': 'Marjinasyon -> Yuvarlanma (Rolling) -> Sıkı Adezyon -> Transmigrasyon (Diapedez) -> Kemotaksi', 'isCorrect': True},
        {'key': 'B', 'text': 'Yuvarlanma -> Marjinasyon -> Kemotaksi -> Sıkı Adezyon -> Fagositoz'},
        {'key': 'C', 'text': 'Sıkı Adezyon -> Marjinasyon -> Diapedez -> Yuvarlanma -> Kemotaksi'},
        {'key': 'D', 'text': 'Diapedez -> Yuvarlanma -> Marjinasyon -> Adezyon -> Kemotaksi'},
        {'key': 'E', 'text': 'Kemotaksi -> Marjinasyon -> Adezyon -> Diapedez -> Opsonizasyon'}
    ],
    'correctAnswer': 'A',
    'explanation': 'Lökosit ekstravazasyonu sırasıyla: 1) Marjinasyon (damar duvarına yaklaşma), 2) Yuvarlanma (Selektinler aracılığıyla gevşek bağlanma), 3) Sıkı Adezyon (İntegrinler ve ICAM-1/VCAM-1 etkileşimi), 4) Transmigrasyon / Diapedez (PECAM-1 / CD31 ile endotel arasından dokuya geçiş) ve 5) Kemotaksi (kemotaktik faktör gradyanına doğru yönelim).'
}

q_lokosit_toplanma = find_q('d3-k1-pat-027') or {
    'id': 'd3-k1-pat-027',
    'examYear': '2022-2026',
    'committeeId': 'Kurul 1',
    'discipline': 'Tıbbi Patoloji',
    'topic': 'Akut İnflamasyonda Lökosit Rekrutmanı',
    'stem': 'Akut inflamasyonda lökositlerin damar dışına çıkıp inflamasyon bölgesinde toplanma aşamaları hangi moleküler sırayla gerçekleşir?',
    'options': [
        {'key': 'A', 'text': 'İntegrin bağlanması -> Selektin bağlanması -> CD31 diapedez -> Fagositoz'},
        {'key': 'B', 'text': 'PECAM-1 geçişi -> Sialyl-Lewis X -> İntegrin yüksek afinitesi -> Kemotaksi'},
        {'key': 'C', 'text': 'Kemotaktik faktör bağlanması -> Bazal membran delinmesi -> Selektin bağlanması'},
        {'key': 'D', 'text': 'Selektin aracılı yuvarlanma -> Kemokinle integrin aktivasyonu ve sıkı adezyon -> PECAM-1 ile diapedez -> Kemotaksi', 'isCorrect': True},
        {'key': 'E', 'text': 'Opsonizasyon -> Diapedez -> Marjinasyon -> Fagositoz'}
    ],
    'correctAnswer': 'D',
    'explanation': 'Endotel ve lökosit adezyon molekülleri kronolojik ve hiyerarşik çalışır: Selektinler (E-, P-, L-selektin) ve Sialyl-Lewis X gevşek yuvarlanmayı sağlar; ardından endotelyal kemokinler lökosit integrinlerini (LFA-1, Mac-1, VLA-4) yüksek afiniteli konformasyona sokarak ICAM-1/VCAM-1\'e sıkı tutundurur; PECAM-1 (CD31) interendotelyal kavşaktan transmigrasyonu sağlar ve dokuda kemotaktik gradyanla odak noktasına ilerlenir.'
}

q_onkotik_basinc = find_q('d3-k1-pat-021') or {
    'id': 'd3-k1-pat-021',
    'examYear': '2021-2026',
    'committeeId': 'Kurul 1',
    'discipline': 'Tıbbi Patoloji',
    'topic': 'Hemodinamik Bozukluklar ve Ödem',
    'stem': 'Aşağıdakilerden hangisi plazma onkotik basıncını azaltarak transüda tipi ödeme yol açan durumlardan biri DEĞİLDİR?',
    'options': [
        {'key': 'A', 'text': 'Nefrotik Sendrom (İdrarla masif albümin kaybı)'},
        {'key': 'B', 'text': 'Karaciğer Sirozu (Albümin sentez yetersizliği)'},
        {'key': 'C', 'text': 'Protein Kaybettiren Enteropati (GİS yoluyla albümin kaybı)'},
        {'key': 'D', 'text': 'Akut Enflamasyonda Histamin Salınımı', 'isCorrect': True},
        {'key': 'E', 'text': 'Ağır Malnütrisyon (Kwashiorkor)'}
    ],
    'correctAnswer': 'D',
    'explanation': 'Plazma onkotik basıncını azaltan durumlar hipoalbüminemiye yol açan karaciğer yetmezliği, nefrotik sendrom, malnütrisyon ve protein kaybettiren enteropatidir (bu durumlarda transüda tipi protein-fakir ödem oluşur). Akut enflamasyonda histamin salınımı ise endotel aralıklarını açarak mikrovasküler geçirgenliği artırır ve damar dışına yüksek proteinli EKSÜDA çıkışına neden olur; bu primer bir onkotik basınç azalması değil, damar duvarı bariyer yıkımıdır.'
}

# 22 Slaytlık Eksiksiz Master Deste
deck_slides = [
    # Slayt 1
    {
        'slideNumber': 1,
        'title': 'Akut Enflamasyonun Tanımı ve Biyolojik Amacı',
        'subtitle': 'Damarlı dokuların enfeksiyon ve hasara karşı konak savunma reaksiyonu',
        'badge': 'Temel Patoloji',
        'badgeColor': 'emerald',
        'synthesisNarrative': '''### Enflamasyonun Temel Kavramsal Çerçevesi
#### Damarlı Dokuların Vazgeçilmez Savunma Yanıtı
Enflamasyon; damarlı canlı dokuların enfeksiyonlara, toksinlere, fiziksel travmalara veya doku nekrozuna karşı geliştirdiği son derece koordineli bir konak savunma cevabıdır. Canlı olmayan cansız dokuda enflamasyon gelişemez; damarsız dokularda (örneğin kornea veya avasküler kıkırdak) enflamatuvar yanıt gecikmeli ve çevre damarlı sınırlardan dolaylı olarak yürütülür.

💡 **Klinik ve Patolojik Amaç Zinciri:**
Enflamasyonun varoluşsal gayesi üç kritik aşamadan oluşur:
• **Zararlı Etkeni Ortadan Kaldırmak:** İnvaze olan mikroorganizmayı (bakteri, virüs, mantar, parazit) veya toksini etkisiz hale getirmek.
• **Nekrotik Hücre ve Kalıntıları Temizlemek:** İskemi, travma ya da toksin sonucu ölen konak hücrelerini fagositoz yoluyla sahadan süpürmek.
• **Doku Onarımını Başlatmak:** Rejenerasyon (parankim yenilenmesi) veya skar/fibrozis süreçlerine biyolojik zemin hazırlamak.

Enflamasyon reaksiyonu olmasaydı; en basit yüzeyel bakteriyel enfeksiyon dahi hızla fatal sepsise dönüşür, operasyon kesileri ve travmatik yaralar asla iyileşemez, nekrotik odaklar kalıcı lezyonlar olarak organ iflasına yol açardı.''',
        'professorAudioHighlight': {
            'quote': 'İnflamasyon yaşayan bir organizmada damarlı dokuların enfeksiyöz ya da non-enfeksiyöz etkenlere karşı vermiş olduğu hücresel, hümoral ve vasküler reaksiyonların bütünüdür. Canlıda görülen bir tablolama...',
            'note': 'Hoca amfide enflamasyonun damarlı dokularda geliştiğini, hücresel, hümoral ve vasküler üçlü sacayağı üzerinde yükseldiğini vurguladı.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-01-01',
                'category': 'Tanım',
                'front': 'Enflamasyon reaksiyonunun gerçekleşebilmesi için dokuda bulunması gereken temel biyolojik ön koşul nedir?',
                'hint': 'Kan dolaşımı ve lökosit transferi.',
                'back': '**Damarlı (Vaskülarize) Canlı Doku Olmasıdır**. Damarsız veya ölü dokularda enflamasyon meydana gelemez; avasküler dokularda (kornea gibi) periferik damarlı sınırlardan göç beklenir.'
            },
            {
                'id': 'inf-fc-01-02',
                'category': 'Amac',
                'front': 'Enflamatuvar yanıtın nihai hedefini oluşturan 3 ardışık basamak nedir?',
                'hint': 'Etken, nekroz temizliği ve tamir.',
                'back': '1) **Zararlı etkeni yok etmek**\n2) **Nekrotik hücre ve doku artıklarını temizlemek**\n3) **Doku onarımını (rejenerasyon/skar) başlatmak**.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Canlı Doku Şartı',
                    'desc': 'Enflamasyon yalnızca yaşayan ve mikrosirkülasyona sahip damarlı dokularda şekillenir.',
                    'isKey': True
                },
                {
                    'title': 'Koruyucu Nitelik',
                    'desc': 'Temelde konakçıyı mikroplardan ve nekrotik kitlelerden koruyan hayati bir adaptif yanıttır.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders notu Sayfa 4: Enflamasyon damarlı dokuların enfeksiyon ve doku hasarına verdiği konak savunma yanıtıdır.',
            'Enflamasyon olmasaydı enfeksiyonlar kontrolsüz yayılır, yaralar asla iyileşmez ve nekroz kalıcı hasar bırakırdı.'
        ],
        'relatedQuestions': [q_kardinal],
        'aiPromptSuggestions': [
            'Avasküler dokularda enflamasyon nasıl gerçekleşir?',
            'Enflamasyon ile enfeksiyon arasındaki fark nedir?'
        ]
    },

    # Slayt 2
    {
        'slideNumber': 2,
        'title': 'Enflamasyonun Temel Öğeleri ve İki Uçlu Kılıç Niteliği',
        'subtitle': 'Lökositler, antikorlar, kompleman ve kontrolsüz yanıtta gelişen patolojiler',
        'badge': 'İmmünopatoloji',
        'badgeColor': 'rose',
        'synthesisNarrative': '''### Enflamasyonun Silahları ve Potansiyel Zararları
#### Normalde Kanda Saklanan Savunma Araçları
Konak savunma araçları (fagositer nötrofiller ve monositler, antikorlar, kompleman gibi plazma proteinleri) normal koşullarda sistemik dolaşımda sessizce seyahat eder ve parankim dokulardan endotel bariyeri ile izole tutulur. Enflamatuvar sinyal alındığında bu savunma araçları süratle damar dışına çıkarak hasarlı alana rekrute edilir.

💡 **İki Uçlu Kılıç (Two-Edged Sword) İlkesi:**
Enflamasyon fizyolojik bir savunma silahıdır; ancak kontrolsüz, uygunsuz ya da aşırı gerçekleştiğinde bizzat kendisi ağır morbidite ve mortaliteye sebep olur:
• **Aşırı Duyarlılık Reaksiyonları ve Anafilaktik Şok:** Zararsız çevresel antijenlere veya ilaçlara karşı gelişen devasa vasküler kollaps ve laringeal ödem.
• **Otoimmün Hastalıklar:** Konak bağışıklık sisteminin kendi öz dokularına (örneğin Romatoid Artritte eklem kıkırdağına, SLE\'de glomerül bazal membranına) saldırarak kalıcı fibrozis ve destrüksiyon üretmesi.
• **Masum Seyirci (Bystander) Doku Hasarı:** Bakteriyi öldürmek üzere nötrofillerden ortama saçılan serbest oksijen radikalleri (ROS) ve proteolitik enzimlerin sağlam çevre dokuları nekroze etmesi.''',
        'professorAudioHighlight': {
            'quote': 'İnflamasyon normalde bir savunma silahıdır ama kontrolden çıktığı zaman hücreye ve organizmaya zarar verip hatta ölüme kadar götürür. Hangi örnekle? Aşırı duyarlılık reaksiyonu, şok, anaflaksi...',
            'note': 'Hoca enflamasyonun çift taraflı keskin bir kılıç olduğunu, kontrolden çıktığında anaflaktik şok ve otoimmünite gibi ölümcül tablolara yol açtığını özellikle belirtti.',
            'emphasisType': 'exam_trap'
        },
        'flashcards': [
            {
                'id': 'inf-fc-02-01',
                'category': 'Savunma Bileşenleri',
                'front': 'Enflamatuvar yanıtta rol alan başlıca 3 plazma ve hücresel savunma aracı nelerdir?',
                'hint': 'Hücre, hümoral immünite ve plazma proteini kaskadı.',
                'back': '1) **Fagositoz yapan lökositler** (Nötrofiller ve Makrofajlar)\n2) **Antikorlar (İmmünoglobulinler)**\n3) **Kompleman sistemi** plazma proteinleri.'
            },
            {
                'id': 'inf-fc-02-02',
                'category': 'Klinik Patoloji',
                'front': 'Enflamasyonun kontrolsüzce konak dokusuna ölümcül zarar verdiği 2 tipik klinik durum nedir?',
                'hint': 'Alerjik acil durum ve öz antijenlere saldırı.',
                'back': '1) **Anafilaktik Şok** (Tip I aşırı duyarlılık ve sistemik vasküler kollaps)\n2) **Otoimmün Hastalıklar** (SLE, Romatoid Artrit gibi immün tolerans kaybı).'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Dolaşım İzolasyonu',
                    'desc': 'Lökosit ve kompleman proteinleri normalde plazmada inaktif dolaşır, dokulardan uzaktır.',
                    'isKey': True
                },
                {
                    'title': 'Otoimmün Tehdit',
                    'desc': 'Yanıt kendi dokusuna yönelirse otoimmünite; aşırı olursa septik/anafilaktik şok doğar.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Enflamasyon savunma aracıdır fakat romatoid artrit, ateroskleroz ve anafilakside bizzat hastalığın kaynağıdır.',
            'Savunma proteinleri kanda inaktif halde tutularak sağlam dokuların zamansız lizisi engellenir.'
        ],
        'relatedQuestions': [q_kardinal],
        'aiPromptSuggestions': [
            'Otoimmün hastalıklarda enflamasyon neden durdurulamaz?',
            'Bystander doku hasarı hangi mekanizmayla oluşur?'
        ]
    },

    # Slayt 3
    {
        'slideNumber': 3,
        'title': 'Akut ve Kronik Enflamasyonun Karşılaştırmalı Dinamikleri',
        'subtitle': 'Başlangıç hızı, hücre tipi, doku hasarı şiddeti ve fibrozis farkları (Tablo 2.1)',
        'badge': 'Müfredat Tablosu',
        'badgeColor': 'blue',
        'synthesisNarrative': '''### Akut ve Kronik Enflamasyonun Kesin Ayrımı
#### Ders Notu Tablo 2.1 Analizi
Enflamatuvar süreç zamansal kinetiğine, mikrovasküler katılımına ve baskın lökosit profiline göre iki ana kategoriye ayrılır:

💡 **Akut Enflamasyon:**
• **Başlangıç:** Dakikalar veya saatler içinde çok hızlı tetiklenir.
• **Hücresel İnfiltrat:** Başlıca **Nötrofiller (Polimorfonükleer Lökositler - PMNL)** hakimdir.
• **Vasküler Bulgular:** Belirgin ödem (sıvı ve plazma protein eksüdasyonu) ve vazodilatasyon.
• **Doku Hasarı:** Genellikle hafif, lokalize ve kendini sınırlayan yapıdadır.
• **Fibrozis:** Akut evrede fibrozis (kollajen birikimi) **YOKTUR**.

💡 **Kronik Enflamasyon:**
• **Başlangıç:** Günler, haftalar veya aylar içinde yavaş ve sinsi gelişir.
• **Hücresel İnfiltrat:** **Monosit/Makrofajlar, Lenfositler ve Plazma Hücreleri** (mononükleer seri).
• **Doku Hasarı:** Belirgin, ilerleyici ve doku yıkımı (destrüksiyon) ile birliktedir.
• **Fibrozis:** **Şiddetli ve sıklıkla mevcuttur**; anjiyogenez ve fibroblast proliferasyonu eşlik eder.''',
        'professorAudioHighlight': {
            'quote': 'Akut enflamasyon dakikalar saatler içinde başlar, süresi saatler günlerdir, nötrofil ağırlıklıdır, ödemle gider. Kronik enflamasyonda ise mononükleer hücreler, doku yıkımı ve fibrozis vardır.',
            'note': 'Hoca sınavda akut ve kronik enflamasyon tablosundan hücre tipleri ve fibrozis varlığı üzerinden kesin soru geleceğini belirtti.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-03-01',
                'category': 'Hücresel Ayırım',
                'front': 'Akut enflamasyonda ilk dakikalardan itibaren sahaya koşan baskın hücre ile kronik enflamasyonda sahada kalan baskın hücreler nelerdir?',
                'hint': 'Çok parçalı çekirdekli lökosit vs mononükleer hücreler.',
                'back': 'Akut enflamasyonda: **Nötrofiller (PMNL)**.\nKronik enflamasyonda: **Monosit/Makrofajlar ve Lenfositler**.'
            },
            {
                'id': 'inf-fc-03-02',
                'category': 'Fibrozis Kriteri',
                'front': 'Akut enflamasyon ile kronik enflamasyon doku onarımı ve fibrozis (bağ dokusu birikimi) açısından nasıl ayrılır?',
                'hint': 'Sayfa 9 Tablo 2.1.',
                'back': 'Akut enflamasyonda **fibrozis YOKTUR** (yalnızca ödem ve nötrofil eksüdası vardır). Kronik enflamasyonda ise **şiddetli doku yıkımı ve fibrozis (skar)** karakteristik bulgudur.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Nötrofil Damgası',
                    'desc': 'Akut enflamasyonun histopatolojik imza hücresi nötrofildir.',
                    'isKey': True
                },
                {
                    'title': 'Skar ve Kronisite',
                    'desc': 'Fibrozis ve doku destrüksiyonu kronik enflamasyonun temel bileşenidir.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ders Notu Tablo 2.1: Akut ve Kronik İnflamasyonun Karşılaştırmalı Özellikleri',
                'headers': ['Özellik', 'Akut İnflamasyon', 'Kronik İnflamasyon'],
                'rows': [
                    ['Başlangıç (Onset)', 'Hızlı (Dakikalar - Saatler)', 'Yavaş (Günler - Haftalar)'],
                    ['Hücresel İnfiltrat', 'Başlıca Nötrofiller', 'Monosit/Makrofajlar ve Lenfositler'],
                    ['Doku Hasarı', 'Hafif ve kendini sınırlayan', 'Belirgin, ilerleyici ve destrüktif'],
                    ['Lokal ve Sistemik Belirtiler', 'Belirgin (Kardinal bulgular)', 'Daha az belirgin veya sinsi'],
                    ['Fibrozis (Skarlaşma)', 'YOK', 'Şiddetli ve sıklıkla mevcut']
                ]
            }
        },
        'spotPearls': [
            'Ders Notu Sayfa 9: Akut enflamasyonun temel özellikleri nötrofiller ve sıvı eksüdasyonudur; fibrozis bulunmaz.',
            'Sınav sorusu: Biyopside nötrofil infiltrasyonu ve ödem varsa tanı akut; mononükleer hücre ve fibrozis varsa kroniktir.'
        ],
        'relatedQuestions': [q_kardinal],
        'aiPromptSuggestions': [
            'Akut enflamasyon hangi durumlarda kronikleşir?',
            'Tablo 2.1\'deki hücre dağılımının zamansal sebebi nedir?'
        ]
    },

    # Slayt 4
    {
        'slideNumber': 4,
        'title': 'Enflamasyonun Beş Ana Kardinal Bulgusu',
        'subtitle': 'Celsus ve Virchow tanımları: Rubor, Calor, Tumor, Dolor ve Functio Laesa',
        'badge': 'Klinik Patoloji',
        'badgeColor': 'amber',
        'synthesisNarrative': '''### Enflamasyonun Tarihsel ve Klinik Belirtileri
#### Celsus'un 4 Maddesi ve Virchow'un 5. Ek Belirtisi
M.Ö. 1. yüzyılda Romalı yazar Aulus Cornelius Celsus akut enflamasyonun 4 klasik yerel bulgusunu formüle etmiştir. 19. yüzyılda modern hücresel patolojinin kurucusu Rudolf Virchow bu listeye beşinci bulguyu eklemiştir:

💡 **5 Kardinal Belirti ve Patofizyolojik Nedenleri:**
• **1. Kızarıklık (Rubor):** Arteriyoler vazodilatasyon ve mikrosirkülasyonda kan akımının artması (aktif hiperemi).
• **2. Sıcaklık Artışı (Calor):** Derin organlardaki sıcak kanın genişlemiş damarlar aracılığıyla periferik dokuya hücum etmesi.
• **3. Şişlik (Tumor):** Mikrovasküler geçirgenlik artışı sonucu damar dışı interstisyel alana protein-zengin sıvı (eksüda/ödem) birikmesi.
• **4. Ağrı (Dolor):** Doku gerilmesine ek olarak, enflamatuvar mediyatörlerin (özellikle **Bradikinin ve Prostaglandin E2 / PGE2**) duyu sinir uçlarını (nosiseptörleri) uyarması ve duyarlılaştırması.
• **5. Fonksiyon Kaybı (Functio Laesa):** Rudolf Virchow tarafından eklenmiştir; doku hasarı, ödem ve ağrının refleks inhibisyonu sonucu organ hareket veya işlevinin bozulmasıdır (örneğin artritli parmağın bükülememesi).''',
        'professorAudioHighlight': {
            'quote': 'Klasik belirtiler: Isı (calor), kızarıklık (rubor), şişlik (tumor), ağrı (dolor) ve fonksiyon kaybı (functio laesa). Celsus ve Virchow tanımları...',
            'note': 'Hoca sınavda 5 kardinal belirtiden fonksiyon kaybının (functio laesa) Rudolf Virchow tarafından sonradan eklendiğinin klasik bir soru olduğunu belirtti.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-04-01',
                'category': 'Tarihçe & Tanım',
                'front': 'Celsus\'un 4 kardinal belirtisine (Rubor, Calor, Tumor, Dolor) 5. olarak "Functio Laesa"yı (fonksiyon kaybı) ekleyen ünlü patolog kimdir?',
                'hint': 'Hücresel patolojinin babası.',
                'back': '**Rudolf Virchow** (19. yüzyıl). Fonksiyon kaybını (functio laesa) ekleyerek listeyi 5 ana bulguya tamamlamıştır.'
            },
            {
                'id': 'inf-fc-04-02',
                'category': 'Ağrı Mekanizması',
                'front': 'Akut enflamasyonda "Dolor" (ağrı) gelişimine doğrudan nosiseptif reseptör uyarısıyla yol açan 2 temel mediyatör nedir?',
                'hint': 'Plazma kinini ve araşidonik asit ürünü.',
                'back': '1) **Bradikinin**\n2) **Prostaglandinler (özellikle PGE2)**. Sinir uçlarını kimyasal olarak irrite eder ve ağrı eşiğini düşürürler.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Celsus Dörtlüsü',
                    'desc': 'Rubor (kızarıklık), Calor (sıcaklık), Tumor (şişlik), Dolor (ağrı).',
                    'isKey': True
                },
                {
                    'title': 'Virchow Katkısı',
                    'desc': 'Functio laesa (fonksiyon kaybı) 19. yüzyılda Rudolf Virchow tarafından eklenmiştir.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Sınav sorusu: Hangisi enflamasyonun kardinal bulgusu değildir? Yanıt: Nekroz (veya apoptoz).',
            'Kızarıklık ve sıcaklık vazodilatasyona; şişlik artmış geçirgenliğe; ağrı bradikinin/PGE2\'ye bağlıdır.'
        ],
        'relatedQuestions': [q_kardinal],
        'aiPromptSuggestions': [
            'Prostaglandin E2 ağrıyı nasıl şiddetlendirir?',
            'Functio laesa mekanizması nedir?'
        ]
    },

    # Slayt 5
    {
        'slideNumber': 5,
        'title': "Enflamatuvar Yanıtın '5R' Basamağı",
        'subtitle': 'Recognition, Recruitment, Removal, Regulation ve Repair basamakları',
        'badge': 'Mekanizma',
        'badgeColor': 'purple',
        'synthesisNarrative': '''### Enflamasyonun Kronolojik Yol Haritası
#### 5R Prensibi ile Sistematik İlerleme
Ders notu Sayfa 11 uyarınca enflamasyon reaksiyonu birbirini tetikleyen ve denetleyen 5 temel basamak (5R) halinde yürütülür:

💡 **5R Basamaklarının Analizi:**
• **1. Recognition (Tanıma):** Konak fagositleri ve dendritik hücreler yüzey ve sitozolik reseptörleriyle zararlı mikrobu veya hasarlı/nekrotik konak hücresini saptar.
• **2. Recruitment (Toplanma / Çağırma):** Vasküler değişiklikler ve kemokin salınımıyla lökositler ve plazma proteinleri damar lümeninden hasar bölgesine rekrute edilir.
• **3. Removal (Ortadan Kaldırma / Temizleme):** Alana ulaşan nötrofil ve makrofajlar fagositoz, reaktif oksijen radikalleri (ROS) ve enzimlerle mikroorganizmaları ve nekrotik dokuları yok eder.
• **4. Regulation (Kontrol ve Sonlanma):** Tehdit bertaraf edildiğinde anti-enflamatuvar sitokinler (TGF-β, IL-10) ve lipoksinler devreye girerek enflamasyonu durdurur. Nötrofiller apoptoza gider.
• **5. Repair (Onarım):** Makrofajlardan salınan büyüme faktörleri ile hasarlı doku ya kök hücrelerden rejenere edilir ya da granülasyon dokusu ve skar (fibrozis) ile onarılır.''',
        'professorAudioHighlight': {
            'quote': 'Enflamasyonun 5R basamağı: Recognition etkenin tanınması, Recruitment toplanma, Removal ortadan kaldırma, Regulation yanıtın kontrolü ve Repair doku onarımı.',
            'note': 'Hoca enflamasyonun kontrolsüz bir patlama olmadığını, 5R basamağı ile onarıma kadar uzanan düzenli bir biyolojik döngü olduğunu vurguladı.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-05-01',
                'category': '5R Kuralı',
                'front': 'Enflamasyon basamaklarından "Regulation" (Kontrol ve Sonlanma) evresinin temel biyolojik işlevi nedir?',
                'hint': 'Sürecin gereksiz uzamasını engellemek.',
                'back': 'Etken yok edildikten sonra **enflamatuvar yanıtın sonlandırılmasıdır**. Kısa ömürlü mediyatörler parçalanır, nötrofiller apoptoza uğrar ve anti-enflamatuvar sinyaller (TGF-β, IL-10) devreye girer.'
            },
            {
                'id': 'inf-fc-05-02',
                'category': 'Onarım',
                'front': 'Enflamasyonun 5R sürecindeki son basamak olan "Repair" (Onarım) hangi 2 temel yoldan biriyle tamamlanır?',
                'hint': 'Orijinal dokunun dönüşü veya bağ dokusu yaması.',
                'back': '1) **Rejenerasyon** (sağlam hücrelerin çoğalarak dokuyu orijinal mimarisine kavuşturması)\n2) **Skar / Fibrozis** (hasarlı bölgenin kolajenöz bağ dokusu ile doldurulması).'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Recognition İlk Adım',
                    'desc': 'PAMP ve DAMP paternlerinin konak reseptörlerince tanınması yanıtı başlatır.',
                    'isKey': True
                },
                {
                    'title': 'Regulation Şartı',
                    'desc': 'Enflamasyon kendi kendini sınırlamazsa doku harabiyeti (kronisite) doğar.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            '5R kuralı: Recognition (Tanıma) -> Recruitment (Çağırma) -> Removal (Yok etme) -> Regulation (Durdurma) -> Repair (Onarım).',
            'Enflamasyon yalnızca yıkım değil, aynı zamanda doku onarımını başlatan temel süreçtir.'
        ],
        'relatedQuestions': [q_kardinal],
        'aiPromptSuggestions': [
            'Anti-enflamatuvar sinyaller enflamasyonu nasıl sonlandırır?',
            'Regulation basamağı aksarsa hangi patolojiler doğar?'
        ]
    },

    # Slayt 6
    {
        'slideNumber': 6,
        'title': 'Mikropların ve Hasarlı Hücrelerin Tanınması',
        'subtitle': 'PAMPs, DAMPs, Toll-Like Reseptörler (TLR), İnflamazom ve Kaspaz-1',
        'badge': 'Moleküler İmmünoloji',
        'badgeColor': 'rose',
        'synthesisNarrative': '''### Tehdit Algılama Reseptör Sistemleri
#### Hücresel Sensörler ve İnflamazom Kompleksi
Konak hücreleri (makrofajlar, dendritik hücreler, endotel hücreleri) yabancı istilacıları ve hücresel stresi hücresel reseptörleri aracılığıyla anında algılar:

💡 **1. PAMPs ve DAMPs:**
• **PAMP (Patogen-Associated Molecular Patterns):** Mikroplara özgü, konak hücrelerinde bulunmayan yapılar (örneğin bakteriyel endotoksin/LPS, peptidoglikan, viral çift sarmallı RNA).
• **DAMP (Damage-Associated Molecular Patterns):** Hücre hasarı veya nekrozu sonucu açığa çıkan konak molekülleri (sitrik asit/ürik asit kristalleri, ATP, yüksek konsantrasyonda HMGB1 proteinleri).

💡 **2. Temel Patern Tanıma Reseptörleri (PRR):**
• **Toll-Like Reseptörler (TLR):** Hücre zarında ve endozomlarda yer alır. TLR aktivasyonu transkripsiyon faktörü **NF-κB**\'yi uyararak TNF, IL-1 ve sitokin üretimini tetikler.
• **İnflamazom Kompleksi:** Sitoplazmik NLR (NOD-like reseptör) sensörleri hücre içi tehlikeyi (ürik asit, ATP, kolesterol kristalleri) algılar. İnflamazom aktive olduğunda **Kaspaz-1** enzimini uyarır. Kaspaz-1 inaktif prokürsörleri parçalayarak aktif **İnterlökin-1β (IL-1β)** üretir. IL-1β lökositleri sahaya çağıran en güçlü pirojenik mediyatördür.''',
        'professorAudioHighlight': {
            'quote': 'Patojen ilişkili moleküler kalıplar PAMP ve hasar ilişkili DAMP... Toll-like reseptörler ve sitoplazmik inflamazom kompleksi devreye girerek kaspaz-1 üzerinden interlökin-1 salgısını başlatır.',
            'note': 'Hoca inflamazom kompleksinin kaspaz-1 enzimini aktive ettiğini ve bunun sonucunda IL-1 beta salındığını amfide soru adayı olarak vurguladı.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-06-01',
                'category': 'Moleküler Algılama',
                'front': 'Mikrobiyal kökenli "PAMP" ile steril doku nekrozunda açığa çıkan "DAMP" arasındaki temel fark nedir?',
                'hint': 'Mikrop bileşeni vs hasarlı konak bileşeni.',
                'back': '**PAMP**: Mikroorganizmalara özgü moleküler kalıplardır (LPS, flagellin, peptidoglikan).\n**DAMP**: Nekroze olan konak hücrelerinden salınan tehlike molekülleridir (ürik asit kristalleri, ATP, HMGB1).'
            },
            {
                'id': 'inf-fc-06-02',
                'category': 'İnflamazom',
                'front': 'Sitoplazmik İnflamazom kompleksinin tetiklediği temel enzim ve bu enzimin ürettiği ana pirojenik sitokin nedir?',
                'hint': 'Sayfa 14: Kaspaz ailesi ve interlökin.',
                'back': 'Enzim: **Kaspaz-1**.\nÜretilen Sitokin: **İnterlökin-1β (IL-1β)**. Lökosit toplanmasını ve ateşi tetikler.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'TLR ve NF-κB',
                    'desc': 'Toll-like reseptörler sinyali NF-κB yoluyla inflamatuvar sitokin genlerine iletir.',
                    'isKey': True
                },
                {
                    'title': 'İnflamazom ve Gut',
                    'desc': 'Gut hastalığında ürat kristalleri inflamazomu aktive ederek şiddetli IL-1β ve akut artrit üretir.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 14: İnflamazom aktivasyonu Kaspaz-1 aracılığıyla IL-1β salınımına yol açar.',
            'DAMP\'lar steril nekrozda (örneğin miyokard infarktüsünde) mikrop olmadan da enflamasyon başlatır.'
        ],
        'relatedQuestions': [q_kardinal],
        'aiPromptSuggestions': [
            'Gut hastalığında inflamazom nasıl bloke edilir (Kolşisin, Anakinra)?',
            'Toll-like reseptörlerin hücresel yerleşimleri nasıldır?'
        ]
    },

    # Slayt 7
    {
        'slideNumber': 7,
        'title': 'Akut Enflamasyonun 3 Ana Bileşeni',
        'subtitle': 'Vazodilatasyon, mikrovasküler geçirgenlik artışı ve postkapiller venül odağı',
        'badge': 'Vasküler Patoloji',
        'badgeColor': 'blue',
        'synthesisNarrative': '''### Akut Enflamasyonun Vasküler ve Hücresel Üçlüsü
#### Olayların Cereyan Ettiği Kritik Alan: Postkapiller Venüller
Ders notu Sayfa 16 uyarınca akut enflamasyonun tüm patolojik tezahürü 3 ana bileşenin eşzamanlı ve ardışık icrasıyla gerçekleşir:

💡 **3 Ana Bileşen:**
• **1. Küçük Damarların Vazodilatasyonu:** Kan akım hızını ve hacmini artırarak sahaya bol eritrosit, lökosit ve plazma getirir.
• **2. Mikrovasküler Geçirgenlik Artışı:** Normalde plazma proteinlerine kapalı olan endotel bariyerini açarak protein-zengin sıvının (eksüda) interstisyuma çıkmasına izin verir.
• **3. Lökositlerin Göçü ve Aktivasyonu:** Lökositlerin (başta nötrofiller) damar lümeninden ekstravaze olarak perivasküler dokuya geçmesi ve fagositoz için aktive olması.

💡 **Postkapiller Venüllerin Önemi:**
Akut enflamasyonda hem mikrovasküler geçirgenlik artışının (endotel hücre büzülmesi) hem de lökosit ekstravazasyonunun (adezyon ve transmigrasyon) gerçekleştiği **en birincil ve en duyarlı anatomik bölge POSTKAPİLLER VENÜLLERDİR**.''',
        'professorAudioHighlight': {
            'quote': 'Akut enflamasyonun 3 ana bileşeni: Küçük damarların vazodilatasyonu, mikrovasküler geçirgenlik artışı ve lökositlerin damardan dokuya göçü. Bu olaylar özellikle postkapiller venüllerde gerçekleşir.',
            'note': 'Hoca lökosit göçü ve histamin kaynaklı geçirgenlik artışının postkapiller venüllerde meydana geldiğini kurul sınavı için özellikle işaret etti.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-07-01',
                'category': 'Vasküler Odak',
                'front': 'Akut enflamasyonda endotelyal hücre büzülmesi ve lökosit ekstravazasyonunun en yoğun gerçekleştiği mikrovasküler segment hangisidir?',
                'hint': 'Kapillerlerden hemen sonraki damarcıklar.',
                'back': '**Postkapiller Venüller**. Histamin reseptörleri yoğunluğu ve endotel kavşak yapısı nedeniyle vasküler sızıntı ve lökosit çıkışı burada gerçekleşir.'
            },
            {
                'id': 'inf-fc-07-02',
                'category': 'Ana Bileşenler',
                'front': 'Akut enflamasyonun morfolojik ve fonksiyonel tablosunu oluşturan 3 ana bileşen nedir?',
                'hint': 'Çap, bariyer ve hücre göçü.',
                'back': '1) **Vazodilatasyon** (küçük damarların genişlemesi)\n2) **Mikrovasküler geçirgenlik artışı** (eksüda sızıntısı)\n3) **Lökositlerin lümenden dokuya göçü ve aktivasyonu**.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Postkapiller Venül Hedefi',
                    'desc': 'Enflamasyonun lökosit ve geçirgenlik olayları arteriyolde değil venülde cereyan eder.',
                    'isKey': True
                },
                {
                    'title': 'Üçlü Koordinasyon',
                    'desc': 'Vasküler çap artışı staza, geçirgenlik hemokonsantrasyona, bunlar da lökosit göçüne zemin hazırlar.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 16: Akut enflamasyon değişiklikleri özellikle postkapiller venüllerde gerçekleşir.',
            'Vazodilatasyon arteriyollerde başlar; geçirgenlik artışı ve lökosit göçü postkapiller venüllerde yoğunlaşır.'
        ],
        'relatedQuestions': [q_kardinal, q_lokosit_hareket],
        'aiPromptSuggestions': [
            'Neden arteriyollerde değil de postkapiller venüllerde lökosit göçü olur?',
            'Endotel hücrelerinin postkapiller venüllerdeki özgün farkı nedir?'
        ]
    },

    # Slayt 8
    {
        'slideNumber': 8,
        'title': 'Vasküler Değişiklikler: Vazodilatasyon ve Akım Dinamikleri',
        'subtitle': 'Prekapiller sfinkterler, arteriyoler dilatasyon, Nitrik Oksit (NO) ve Histamin',
        'badge': 'Hemodinami',
        'badgeColor': 'rose',
        'synthesisNarrative': '''### Vasküler Kalibre Değişiklikleri ve Akım Hızı
#### Geçici Vazokonstrüksiyon ve Ardından Gelişen Masif Hiperemi
Enflamatuvar hasar meydana geldiğinde mikrosirkülasyonda son derece hızlı hemodinamik değişimler yaşanır:

💡 **Kronolojik Akım Değişiklikleri:**
• **1. Geçici Vazokonstrüksiyon:** Hasardan hemen sonraki ilk birkaç saniye içinde arteriyollerde nörojenik refleksle geçici bir büzülme görülebilir; ancak bu klinik olarak önemsizdir ve saniyeler içinde kaybolur.
• **2. Vazodilatasyon:** Akut enflamasyonun **en erken vasküler belirtisidir**. Önce prekapiller arteriyollerde başlar, ardından kapiller yatakların ve venüllerin açılmasına yol açar.
• **3. Vasküler Mediyatörler:** Bu vazodilatasyonu vasküler düz kasları gevşeten **Histamin** ve endotel kaynaklı **Nitrik Oksit (NO)** yönetir.
• **4. Kan Akımında Artış (Aktif Hiperemi):** Kapiller yataklarda kan hacmi belirgin artar. Bu durum etkilenen dokuda sıcaklık artışı (calor) ve kızarıklığa (rubor) yol açar.
• **5. Staz Evresi:** İlerleyen dakikalarda damar geçirgenliği artıp sıvı dışarı kaçınca kan koyulaşır ve akım dramatik şekilde yavaşlar (Staz).''',
        'professorAudioHighlight': {
            'quote': 'Vasküler değişiklikler: Önce arteriyollerde vazodilatasyon gelişir. Nitrik oksit ve histamin damar düz kasını gevşetir, kan akımı artar, bölge kızarır ve ısınır. Ardından sıvı kaybıyla staz başlar.',
            'note': 'Hoca vazodilatasyonun en erken belirti olduğunu, histamin ve NO tarafından yönlendirildiğini belirtti.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-08-01',
                'category': 'Vasküler Yanıt',
                'front': 'Akut enflamasyonda arteriyoler düz kasları gevşeterek aktif vazodilatasyona ve hiperemiye yol açan 2 temel mediyatör nedir?',
                'hint': 'Mast hücresi amini ve endotel gazı.',
                'back': '1) **Histamin**\n2) **Nitrik Oksit (NO)**. Damar düz kasında cGMP artışı ile relaksasyon sağlar.'
            },
            {
                'id': 'inf-fc-08-02',
                'category': 'Kardinal Yansıma',
                'front': 'Arteriyoler vazodilatasyon ve kapiller yatağın kanla dolması (aktif hiperemi) Celsus\'un hangi 2 kardinal belirtisini oluşturur?',
                'hint': 'Renk ve sıcaklık.',
                'back': '**Rubor (Kızarıklık)** ve **Calor (Sıcaklık Artışı)**.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Erken Vazodilatasyon',
                    'desc': 'Arteriyollerin genişlemesi kapiller yataktaki perfüzyon basıncını ve hidrostatik basıncı artırır.',
                    'isKey': True
                },
                {
                    'title': 'NO ve Histamin Sinerjisi',
                    'desc': 'Hızlı histamin salınımı dakikalar içinde endotelyal NO sentazı uyararak tonusu düşürür.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 17: Akut enflamasyonun ilk ve en erken vasküler yanıtı vazodilatasyondur.',
            'Geçici vazokonstrüksiyon saniyeler sürer; esas klinik tablo kalıcı arteriyoler vazodilatasyon ile başlar.'
        ],
        'relatedQuestions': [q_kardinal, q_onkotik_basinc],
        'aiPromptSuggestions': [
            'Nitrik oksit vasküler düz kasta nasıl vazodilatasyon yapar?',
            'Aktif hiperemi ile pasif konjesyon arasındaki fark nedir?'
        ]
    },

    # Slayt 9
    {
        'slideNumber': 9,
        'title': 'Mikrovasküler Geçirgenlik: Eksüda, Transüda ve Ödem Ayrımı',
        'subtitle': 'Spesifik dansite, protein içeriği ve Starling kuvvetleri dengesi',
        'badge': 'Müfredat Tablosu',
        'badgeColor': 'amber',
        'synthesisNarrative': '''### Vasküler Kaçak ve Sıvı Dinamikleri
#### Starling Dengesi Bozulması: Eksüda vs Transüda
Mikrosirkülasyonda sıvı dengesi Starling kuvvetleri (damar içi hidrostatik basınç ile plazma kolloid onkotik basıncı) tarafından korunur. Akut enflamasyonda endotel bariyeri bozulduğunda sahneye **EKSÜDA** çıkar:

💡 **Eksüda (Enflamatuvar Sıvı):**
• **Mekanizma:** Mikrovasküler geçirgenlik artışı (endotel bariyerinin delinmesi / açılması).
• **Protein İçeriği:** **Yüksek** (albümin, globülin ve yüksek molekül ağırlıklı fibrinojen içerir).
• **Hücresel İçerik:** **Yoğun lökosit ve hücresel kalıntı** mevcuttur.
• **Spesifik Dansite:** **> 1.020** (yoğun ve bulanık).

💡 **Transüda (Non-enflamatuvar Sıvı):**
• **Mekanizma:** Damar geçirgenliği **NORMALDİR**. Artmış hidrostatik basınç (KKY, venöz obstrüksiyon) veya azalmış kolloid onkotik basınç (siroz, nefrotik sendrom, malnütrisyon) sonucu ultrafiltrasyon sıvısıdır.
• **Protein İçeriği:** **Düşük** (esas olarak eser miktarda albümin).
• **Hücresel İçerik:** Hücreden fakirdir (eser miktarda mezotel).
• **Spesifik Dansite:** **< 1.012** (berrak, şeffaf su kıvamında).''',
        'professorAudioHighlight': {
            'quote': 'Eksüda ve transüda ayrımı sınavların vazgeçilmezidir. Eksüda yüksek proteinli, yoğun hücreli, dansitesi 1.020\'den büyük enflamatuvar sıvıdır. Transüda ise damar geçirgenliği normal iken basınç farkıyla sızan proteinden fakir sıvıdır.',
            'note': 'Hoca eksüda ve transüdanın protein, dansite ve endotel geçirgenliği açısından kesinlikle karıştırılmaması gerektiğini belirtti.',
            'emphasisType': 'exam_trap'
        },
        'flashcards': [
            {
                'id': 'inf-fc-09-01',
                'category': 'Sıvı Ayrımı',
                'front': 'Enflamatuvar kökenli EKSÜDA sıvısını, basınç dengesizliğine bağlı TRANSÜDA sıvısından ayıran 3 temel laboratuvar kriteri nedir?',
                'hint': 'Protein, dansite ve hücre.',
                'back': '1) **Protein Konsantrasyonu**: Eksüdada YÜKSEK, Transüdada DÜŞÜK.\n2) **Spesifik Dansite**: Eksüdada > 1.020, Transüdada < 1.012.\n3) **Hücre İçeriği**: Eksüdada bol nötrofil/hücre artığı, Transüdada hücreden fakir.'
            },
            {
                'id': 'inf-fc-09-02',
                'category': 'Patofizyoloji',
                'front': 'Kalp yetmezliğinde gelişen ödem ile akut sellülitte gelişen ödemin vasküler mekanizma farkı nedir?',
                'hint': 'Bariyer sağlamlığı vs endotel açıklığı.',
                'back': 'Kalp yetmezliğinde endotel sağlamdır, hidrostatik basınç artışıyla **Transüda** sızar.\nSellülitte endotel geçirgenliği bozulmuştur, damar dışına proteinli **Eksüda** çıkar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Eksüda Enflamasyon Kanıtıdır',
                    'desc': 'Bir boşlukta protein-zengin eksüda varsa altta yatan olay mutlaka enflamasyondur.',
                    'isKey': True
                },
                {
                    'title': 'Dansite Eşiği',
                    'desc': '1.020 üzeri spesifik dansite yüksek protein ve hücresel debris varlığını kanıtlar.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 19: Eksüda ve Transüda Karşılaştırma Tablosu',
                'headers': ['Kriter', 'Eksüda (İnflamatuvar)', 'Transüda (Non-İnflamatuvar)'],
                'rows': [
                    ['Endotel Geçirgenliği', 'ARTMIŞ (Bariyer açık)', 'NORMAL (Bariyer sağlam)'],
                    ['Temel Neden', 'İnflamasyon, enfeksiyon, doku hasarı', 'Artmış hidrostatik P veya Azalmış onkotik P'],
                    ['Protein Konsantrasyonu', 'Yüksek (> 3.0 g/dL, Fibrinojen var)', 'Düşük (< 2.5 g/dL, Fibrinojen yok)'],
                    ['Spesifik Dansite', '> 1.020', '< 1.012'],
                    ['Hücresel İçerik', 'Bol (Nötrofiller, hücresel debris)', 'Çok az (Eser endotel/mezotel)'],
                    ['Pıhtılaşma Eğilimi', 'Var (Fibrinojen varlığı nedeniyle)', 'Yok']
                ]
            }
        },
        'spotPearls': [
            'Ders Notu Sayfa 19: Eksüda artmış damar geçirgenliğiyle oluşur; dansitesi >1.020\'dir.',
            'Nefrotik sendrom, siroz ve kalp yetmezliğinde transüda; bakteriyel peritonit ve pnömonide eksüda toplanır.'
        ],
        'relatedQuestions': [q_onkotik_basinc, q_kardinal],
        'aiPromptSuggestions': [
            'Light kriterleri ile plevral sıvıda eksüda-transüda nasıl ayrılır?',
            'Fibrinojenin eksüdaya çıkışı dokuda neye yol açar?'
        ]
    },

    # Slayt 10
    {
        'slideNumber': 10,
        'title': 'Artmış Vasküler Geçirgenliğin 4 Temel Mekanizması',
        'subtitle': 'Endotel hücre büzülmesi, doğrudan endotel hasarı, lökosit hasarı ve transsitoz',
        'badge': 'Mekanizma',
        'badgeColor': 'rose',
        'synthesisNarrative': '''### Damar Duvarının Geçirgenleşme Yolları
#### Endotel Büzülmesinden Nekrotik Vasküler Hasara Kadar 4 Model
Ders notu Sayfa 21 uyarınca proteinlerin ve sıvının damar dışına kaçmasına izin veren 4 temel patolojik mekanizma vardır:

💡 **1. Endotel Hücre Büzülmesi (Endothelial Cell Contraction):**
• **En sık görülen mekanizmadır.**
• **Etken Mediyatörler:** **Histamin, Bradikinin, Lökotrienler (LTC4, LTD4, LTE4), Substans P**.
• **Bölge:** **Yalnızca POSTKAPİLLER VENÜLLERDE** gerçekleşir.
• **Kinetik:** Hızlıdır (15-30 dakikada biter, \'hızlı geçici yanıt\'). Endotel hücreleri büzülerek aralarında interendotelyal yarıklar açar.

💡 **2. Doğrudan Endotel Hasarı (Direct Endothelial Injury):**
• Şiddetli travmalar, termal yanıklar, radyasyon veya nekrotizan mikrobiyal toksinler sonucu endotel hücreleri nekroze olur ve dökülür.
• **Bölge:** **Arteriyol, kapiller ve venüller dahil tüm mikrosirkülasyonu** tutar.
• **Kinetik:** Hızlı başlar ve saatlerce/günlerce sürer (tromboz veya tamir olana kadar kesintisiz kaçak).

💡 **3. Lökosit Aracılı Endotel Hasarı:**
• Lökositlerin endotel yüzeyine yapışması sırasında salgıladıkları toksik oksijen radikalleri ve lizozomal proteazlar komşu endoteli tahrip eder.

💡 **4. Transsitoz (Artmış Veziküler Taşıma):**
• **VEGF (Vasküler Endotelyal Büyüme Faktörü)** etkisiyle vezikülovakuoler organeller (VVO) aracılığıyla hücre içinden sıvı transportu artar.''',
        'professorAudioHighlight': {
            'quote': 'Artmış geçirgenliğin en sık mekanizması endotel hücre büzülmesidir; postkapiller venüllerde olur, histamin yapar ve hızlıdır. Ama yanıkta doğrudan endotel nekrozu vardır, tüm damarları tutar ve saatlerce sürer.',
            'note': 'Hoca endotel büzülmesinin postkapiller venüllerde histaminle olduğunu, doğrudan hasarın ise tüm mikrovasküler yatakta yanık/toksinle geliştiğini net biçimde ayırdı.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-10-01',
                'category': 'Geçirgenlik Mekanizması',
                'front': 'Akut enflamasyonda artmış damar geçirgenliğinin EN SIK görülen mekanizması nedir ve hangi damar segmentinde gerçekleşir?',
                'hint': 'Histamin etkisi ve venüller.',
                'back': '**Endotel Hücre Büzülmesi (Endothelial Contraction)**. Yalnızca **Postkapiller Venüllerde** gerçekleşir; histamin ve lökotrienler interendotelyal aralıkları açar.'
            },
            {
                'id': 'inf-fc-10-02',
                'category': 'Doğrudan Hasar',
                'front': 'Ağır bir yanık veya litik bakteriyel toksin varlığında gelişen endotel hasarının histaminik büzülmeden 2 temel yapısal farkı nedir?',
                'hint': 'Damar tipleri ve hücre canlılığı.',
                'back': '1) Yalnızca venülleri değil; **arteriyol, kapiller ve venüllerin tümünü** tutar.\n2) Hücreler büzülmez; **nekroza uğrayarak damar duvarından dökülür** ve saatlerce/günlerce sürer.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Histamin ve Venül',
                    'desc': 'Endotel hücre büzülmesi histamin reseptörleri taşıyan postkapiller venüllere özgüdür.',
                    'isKey': True
                },
                {
                    'title': 'VEGF ve Transsitoz',
                    'desc': 'VEGF sitoplazmik vezikülovakuoler kanalları açarak transsitozu tetikler.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 21: Endotel büzülmesi en sık geçirgenlik mekanizmasıdır ve postkapiller venüllerde olur.',
            'Doğrudan endotel hasarı (yanık, kostik) arteriyol ve kapillerleri de kapsayan masif ve uzun süreli sızıntı yapar.'
        ],
        'relatedQuestions': [q_onkotik_basinc, q_kardinal],
        'aiPromptSuggestions': [
            'Endotel hücre büzülmesinde sitoiskelet aktin-miyozin nasıl kasılır?',
            'VEGF aracılı transsitoz tümör anjiyogenezinde neden önemlidir?'
        ]
    },

    # Slayt 11
    {
        'slideNumber': 11,
        'title': 'Staz, Vasküler Konjesyon ve Lenfatik Yanıt',
        'subtitle': 'Hemokonsantrasyon, eritrosit yığılması, lenfanjit ve reaktif lenfadenit',
        'badge': 'Hemopatoloji',
        'badgeColor': 'blue',
        'synthesisNarrative': '''### Dolaşım Yavaşlaması ve Lenfatik Drenaj
#### Staz Evresi ve İkinci Savunma Hattı Olarak Lenf Düğümleri
Damar geçirgenliği artıp plazma sıvısı ve albümin masif şekilde dokuya sızdığında damar içi hemodinamik parametreler radikal şekilde değişir:

💡 **1. Hemokonsantrasyon ve Staz:**
• Plazma sıvısının kaybı damar içindeki kanın vizkozitesini (koyuluğunu) dramatik olarak artırır.
• Eritrositler damar lümeninde sıkışarak yavaşlar ve kümelenir.
• Bu duruma mikroskopik olarak genişlemiş, eritrositlerle tıka basa dolu damarlar tablosu olan **Vasküler Konjesyon ve STAZ** adı verilir.
• Staz gelişmesi, normalde damarın tam ortasında aksiyal (merkezi) akımla hızla akan lökositlerin damar çeperine doğru savrulmasına (Marjinasyon) zemin hazırlar.

💡 **2. Lenf Akımı ve Lenfadenit:**
• Enflamasyon sahasındaki aşırı ödem sıvısını, hücresel döküntüleri ve mikropları boşaltmak için lenfatik damarlar hızla genişler ve lenf akımı kat kat artar.
• **Lenfanjit:** Lenf damarlarının enfekte olması sonucu deride kırmızı çizgilenmeler oluşmasıdır.
• **Reaktif Lenfadenit:** Drenaj yapan lenf nodlarının mikrobu ve antijenleri süzerek büyüyüp ağrılı hale gelmesidir (ikinci savunma hattı).''',
        'professorAudioHighlight': {
            'quote': 'Sıvı damar dışına kaçınca damar içinde eritrositler konsantre olur, kan koyulaşır ve staz gelişir. Bu staz lökositlerin duvara itilmesi için şarttır. Drenajı yapan lenf damarları iltihaplanırsa lenfanjit, nodlar şişerse reaktif lenfadenit deriz.',
            'note': 'Hoca stazın bir arıza değil, lökositlerin duvara marjine olabilmesi için gereken hemodinamik yavaşlama olduğunu açıkladı.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-11-01',
                'category': 'Hemodinami',
                'front': 'Akut enflamasyonda kan akımının yavaşlayarak "Staz" gelişmesinin doğrudan nedeni nedir?',
                'hint': 'Sıvı kaybı ve kanın yoğunlaşması.',
                'back': 'Mikrovasküler geçirgenlik artışı sonucu sıvının interstisyuma kaçması ve damar lümeninde kalan kanın **aşırı yoğunlaşmasıdır (Hemokonsantrasyon)**.'
            },
            {
                'id': 'inf-fc-11-02',
                'category': 'Lenfatik Patoloji',
                'front': 'Deri enfeksiyonunda drenaj yolunda kırmızı çizgiler görülmesi ile drene olan lenf nodunun ağrılı büyümesi sırasıyla ne ad alır?',
                'hint': 'Damar iltihabı vs nod iltihabı.',
                'back': 'Lenf damarı iltihabı: **Lenfanjit**.\nLenf nodu büyümesi: **Reaktif Lenfadenit**.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Aksiyal Akımdan Kopuş',
                    'desc': 'Normalde kanın ortasından akan lökositler staz sayesinde endotel sınırına itilir.',
                    'isKey': True
                },
                {
                    'title': 'Lenfatik Filtre',
                    'desc': 'Lenf nodları bakterilerin sistemik kana karışmasını engelleyen ikincil savunma barajıdır.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 22-23: Staz, damar geçirgenliği nedeniyle sıvı kaybı ve eritrosit yığılmasıdır.',
            'Lenfanjit enfeksiyonun lenfatik yayılımını, reaktif lenfadenit ise lenf nodu immün cevabını gösterir.'
        ],
        'relatedQuestions': [q_kardinal],
        'aiPromptSuggestions': [
            'Staz evresinde tromboz riski neden artar?',
            'Reaktif lenfadenit ile lenfoma ayrımı nasıl yapılır?'
        ]
    },

    # Slayt 12
    {
        'slideNumber': 12,
        'title': 'Lökosit Rekrutmanı: Marjinasyon ve Yuvarlanma',
        'subtitle': 'Santral akımdan çepere kayma ve Selektinler aracılı gevşek bağlanma',
        'badge': 'Hücresel Olaylar',
        'badgeColor': 'emerald',
        'synthesisNarrative': '''### Lökositlerin Sahaya İniş Yolculuğu
#### Marjinasyon ve Yuvarlanma (Rolling) Dinamikleri
Lökositlerin damar lümeninden enflamasyon sahasına göç etmesi (ekstravazasyon) kusursuz moleküler adımlarla ilerler:

💡 **1. Marjinasyon:**
• Normalde laminer akımda eritrositler ve lökositler damarın merkez ekseninde hızla ilerler; endotel çeperine yakın bölgede ise hücresiz plazma akar.
• Enflamasyonda vazodilatasyon ve staz geliştikçe kan akımı yavaşlar; lökositler santral akımdan çevreye doğru savrularak **endotel yüzeyine çarpmaya ve temas etmeye başlar (Marjinasyon)**.

💡 **2. Yuvarlanma (Rolling):**
• Marjine olan lökositler endotel boyunca tekerlek gibi yuvarlanmaya başlar.
• Bu yuvarlanma **SELEKTİN AİLESİ** adezyon molekülleri aracılığıyla gerçekleştirilir.
• Selektinlerin ligandlarıyla yaptığı bağlar **düşük afinitelidir (zayıf ve gevşektir)**; kan akımının sürtünme kuvvetiyle bu bağlar hızla kurulur ve kopar. Lökosit bu sayede frenleme yaparak endotel üstünde yuvarlanır.''',
        'professorAudioHighlight': {
            'quote': 'Lökosit göçünün ilk adımı marjinasyondur; stazla kenara itilir. Sonra yuvarlanma başlar. Yuvarlanmayı selektinler sağlar. Bunlar zayıf bağlardır, kopar ve tekrar bağlanır, lökosit fren yapar.',
            'note': 'Hoca yuvarlanma basamağında rol alan moleküllerin Selektinler olduğunu, integrinlerin ise sıkı adezyonda devreye girdiğini açıkça belirtti.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-12-01',
                'category': 'Lökosit Göçü',
                'front': 'Lökositlerin damarın merkezi akım ekseninden ayrılarak endotel duvarına yakın konuma geçmesine ne ad verilir?',
                'hint': 'Sınır boyuna yerleşme.',
                'back': '**Marjinasyon**. Vazodilatasyon ve staz sonucu gelişen akım yavaşlaması bu süreci kolaylaştırır.'
            },
            {
                'id': 'inf-fc-12-02',
                'category': 'Moleküler Rol',
                'front': 'Lökositlerin endotel üzerinde "Yuvarlanma" (Rolling) hareketini yöneten temel adezyon molekülü ailesi hangisidir?',
                'hint': 'Gevşek bağlar kuran molekül grubu.',
                'back': '**Selektinler (E-selektin, P-selektin, L-selektin)**. Lökosit yüzeyindeki Sialyl-Lewis X karbohidratlarına zayıf bağlarla tutunup koparak yuvarlanmayı sağlar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Staz Şarttır',
                    'desc': 'Staz olmadan marjinasyon gerçekleşemez; lökositler merkezden akıp giderdi.',
                    'isKey': True
                },
                {
                    'title': 'Düşük Afinite',
                    'desc': 'Selektin bağları zayıftır; lökositi tamamen durdurmaz, sadece yuvarlar ve frenletir.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 26-27: Yuvarlanma selektinler; sıkı adezyon integrinler aracılığıyla gerçekleşir.',
            'Sınav sorusu: Yuvarlanmadan sorumlu molekül? Doğru yanıt: Selektinler.'
        ],
        'relatedQuestions': [q_lokosit_hareket, q_lokosit_toplanma],
        'aiPromptSuggestions': [
            'Selektinlerin yapısındaki lektin alanı ne işe yarar?',
            'Marjinasyon ile adezyon arasındaki moleküler geçiş nasıldır?'
        ]
    },

    # Slayt 13
    {
        'slideNumber': 13,
        'title': 'Selektin Ailesi ve Weibel-Palade Cisimcikleri',
        'subtitle': 'P-selektin, E-selektin, L-selektin ve Sialyl-Lewis X oligosakkarit ligandı',
        'badge': 'Moleküler Biyoloji',
        'badgeColor': 'purple',
        'synthesisNarrative': '''### Selektinlerin Biyokimyası ve Ekspresyon Kinetiği
#### P-, E- ve L-Selektinlerin Özgül Dağılımı (Tablo 2.3)
Selektinler hücre dışı lektin alanları içeren ve spesifik karbohidrat gruplarına (özellikle **Sialyl-Lewis X**) bağlanan adezyon proteinleridir:

💡 **Selektin Ailesinin 3 Üyesi:**
• **1. P-selektin (CD62P):** Endotel hücrelerinde ve trombositlerde bulunur.
  - Normalde endotel hücresi içinde **Weibel-Palade Cisimcikleri** adı verilen granüllerde depolanır.
  - **Histamin ve Trombin** uyarısı geldiğinde dakikalar içinde ekzositozla hücre yüzeyine fırlar. Sentez beklemez, hazır depodan gelir!
• **2. E-selektin (CD62E):** Yalnızca endotel hücrelerinde bulunur.
  - Deposu yoktur! Sitokinler (**TNF ve IL-1**) uyarısıyla transkripsiyonu tetiklenir ve yüzeyde belirmesi 1-2 saat sürer.
• **3. L-selektin (CD62L):** Lökositlerin (nötrofil, monosit, lenfosit) kendi yüzeyinde bulunur. Endotel üzerindeki sialillenmiş ligandlara bağlanır.

💡 **Temel Ligand:** Lökositlerin yüzeyindeki **Sialyl-Lewis X (s-Lex)** modifiyeli glikoproteinler hem P- hem E-selektin için birincil bağlanma ortağıdır.''',
        'professorAudioHighlight': {
            'quote': 'P-selektin endotelde Weibel-Palade cisimciklerindedir, histaminle dakikalar içinde hemen yüzeye çıkar. E-selektin ise sitokinlerle (TNF, IL-1) sentezlenir. Ligandları lökositteki Sialyl-Lewis X\'tir.',
            'note': 'Hoca P-selektinin Weibel-Palade cisimciklerinde depolandığını ve histaminle hızla yüzeye çıktığını TUS ve kurul için kritik bilgi olarak vurguladı.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-13-01',
                'category': 'Moleküler Depo',
                'front': 'P-selektin endotel hücresinde hangi sitoplazmik organelde depolanır ve hangi mediyatörlerle dakikalar içinde yüzeye çıkar?',
                'hint': 'Von Willebrand faktörün de depolandığı cisimcikler.',
                'back': '**Weibel-Palade Cisimcikleri**. **Histamin ve Trombin** uyarısıyla dakikalar içinde hücre zarına ekzositoz edilir.'
            },
            {
                'id': 'inf-fc-13-02',
                'category': 'Ligand',
                'front': 'Endoteldeki E- ve P-selektinlerin lökosit üzerinde tanıdığı temel karbohidrat/glikoprotein ligandı nedir?',
                'hint': 'Fukozillenmiş tetrasakkarit.',
                'back': '**Sialyl-Lewis X (s-Lex)** oligosakkaritidir. Eksikliğinde LAD-2 hastalığı doğar.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Hızlı P vs Yavaş E',
                    'desc': 'P-selektin hazır depodan dakikada çıkar; E-selektin gen transkripsiyonuyla 1-2 saatte belirir.',
                    'isKey': True
                },
                {
                    'title': 'Sialyl-Lewis X',
                    'desc': 'Lökosit yüzeyindeki fukozillenmiş sialik asit yapısı selektinlerin kancasıdır.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 27: Weibel-Palade cisimcikleri P-selektin ve von Willebrand Faktör (vWF) deposudur.',
            'TNF ve IL-1 endotelde E-selektin ve ICAM-1 ekspresyonunu gen düzeyinde artıran ana sitokinlerdir.'
        ],
        'relatedQuestions': [q_lokosit_hareket, q_lokosit_toplanma],
        'aiPromptSuggestions': [
            'Weibel-Palade cisimciklerinde vWF ve P-selektin nasıl paketlenir?',
            'L-selektin lökosit ekstravaze olduktan sonra neden zardan dökülür (shedding)?'
        ]
    },

    # Slayt 14
    {
        'slideNumber': 14,
        'title': 'Sıkı Adezyon ve İntegrinler: Yüksek Afiniteye Geçiş',
        'subtitle': 'LFA-1, Mac-1, VLA-4 ve endotelyal ligandlar (ICAM-1, VCAM-1)',
        'badge': 'Moleküler İmmünoloji',
        'badgeColor': 'emerald',
        'synthesisNarrative': '''### Lökositin Endotele Çakılması: Sıkı Adezyon
#### Kemokin Uyarısı ve İntegrin Konformasyonel Değişimi
Yuvarlanan lökositin kan akımına kapılıp sürüklenmemesi için endotel yüzeyine sıkıca tutunması (adezyon) şarttır. Bu basamağı **İNTEGRİNLER** yürütür:

💡 **İntegrinlerin Çalışma Mekanizması:**
• Lökosit yüzeyinde bulunan integrinler (heterodimerik glikoproteinler) normal dolaşımda **düşük afiniteli (bükük / katlanmış)** konformasyondadır; ligandlarına bağlanamazlar.
• Yuvarlanma sırasında endotel yüzeyinde proteoglikanlara bağlı duran **Kemokinler (örneğin CXCL8 / IL-8)** lökositteki reseptörlerine bağlanır.
• Bu bağlanma hücre içine **"İçten Dışa Sinyal" (Inside-Out Signaling)** gönderir.
• İntegrin proteinleri bükük formdan dikleşerek **yüksek afiniteli konformasyona** geçer.

💡 **Başlıca İntegrin - Ligand Eşleşmeleri (Tablo 2.3):**
• **LFA-1 (CD11a/CD18)** & **Mac-1 (CD11b/CD18):** Nötrofil ve monositlerde bulunur -> Endoteldeki **ICAM-1 (CD54)** molekülüne sıkıca bağlanır.
• **VLA-4 (α4β1 / CD49d/CD29):** Monosit ve lenfositlerde bulunur -> Endoteldeki **VCAM-1 (CD106)** molekülüne bağlanır.
• Sonuç: Lökosit yuvarlanmayı bırakır, endotel üzerinde yassılaşır ve sıkıca sabitlenir.''',
        'professorAudioHighlight': {
            'quote': 'Sıkı adezyonda integrinler devreye girer: LFA-1 ve Mac-1 endoteldeki ICAM-1\'e, VLA-4 ise VCAM-1\'e bağlanır. Kemokinler integrinleri düşük afiniteli bükük formdan yüksek afiniteli dik forma geçirir.',
            'note': 'Hoca integrinlerin beta zincirinin (CD18) ortak olduğunu ve ICAM-1\'e bağlandığını sınav için özel olarak hatırlattı.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-14-01',
                'category': 'Adezyon Molekülü',
                'front': 'Nötrofillerin endotel üzerindeki ICAM-1 molekülüne sıkıca tutunmasını sağlayan beta-2 integrin çifti nedir?',
                'hint': 'CD11a/CD18 ve CD11b/CD18.',
                'back': '**LFA-1 (CD11a/CD18)** ve **Mac-1 (CD11b/CD18)** heterodimerleridir.'
            },
            {
                'id': 'inf-fc-14-02',
                'category': 'Aktivasyon',
                'front': 'İntegrinleri düşük afiniteli bükük formdan yüksek afiniteli dik forma geçiren tetikleyici molekül nedir?',
                'hint': 'Endotel yüzeyinde sergilenen kemotaktik sitokinler.',
                'back': '**Kemokinlerdir**. Lökositteki GPCR reseptörlerine bağlanarak \'içten-dışa sinyal\' ile integrin konformasyonunu değiştirirler.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'İçten Dışa Sinyal',
                    'desc': 'Kemokin uyarısı olmadan integrinler ICAM-1\'e tutunamaz.',
                    'isKey': True
                },
                {
                    'title': 'TNF ve IL-1 Katkısı',
                    'desc': 'TNF ve IL-1 endotelde ICAM-1 ve VCAM-1 transkripsiyonunu artırarak adezyonu güçlendirir.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 28: Sıkı adezyonu integrinler (LFA-1, Mac-1, VLA-4) ve ligandları (ICAM-1, VCAM-1) sağlar.',
            'Sınav sorusu: Lökosit yuvarlanmasını selektin; sıkı durmasını integrin yönetir.'
        ],
        'relatedQuestions': [q_lokosit_hareket, q_lokosit_toplanma],
        'aiPromptSuggestions': [
            'Inside-out ve outside-in integrin sinyali arasındaki fark nedir?',
            'Anti-integrin ilaçlar (ör. Vedolizumab, Natalizumab) tıpta nerede kullanılır?'
        ]
    },

    # Slayt 15
    {
        'slideNumber': 15,
        'title': 'Lökosit Adezyon Eksiklikleri ve Klinik Tablolar',
        'subtitle': 'LAD-1 (CD18 eksikliği) ve LAD-2 (Sialyl-Lewis X sentez kusuru)',
        'badge': 'Genetik İmmünopatoloji',
        'badgeColor': 'rose',
        'synthesisNarrative': '''### Genetik Kusurların Patolojiye Yansıması
#### LAD-1 ve LAD-2: Apsesiz Enfeksiyon Paradoksu
Lökosit adezyon basamaklarındaki genetik mutasyonlar ölümcül immün yetmezliklere yol açar:

💡 **1. Lökosit Adezyon Eksikliği Tip 1 (LAD-1):**
• **Genetik Kusur:** İntegrinlerin ortak **β2 zincirini kodlayan CD18 geninde mutasyon** vardır.
• **Moleküler Sonuç:** LFA-1 ve Mac-1 (CD11/CD18) integrinleri üretilemez.
• **Patolojik Tablo:** Lökositler yuvarlanır ancak **SIKI ADEZYON YAPAMAZ**.
• **Klinik Bulgular:**
  1. **Göbek kordonunun geç düşmesi** (normalde kordon nötrofilik ayrışmayla düşer).
  2. Tekrarlayan bakteriyel ve mantar enfeksiyonları.
  3. **Yaralarda İRİN (PÜ) OLUŞAMAZ!** Çünkü nötrofiller dokuya çıkamaz.
  4. Kanda aşırı lökositoz (nötrofiller damarda hapsolduğu için kanda birikir).

💡 **2. Lökosit Adezyon Eksikliği Tip 2 (LAD-2):**
• **Genetik Kusur:** Fukoza metabolizmasında görevli fukoziltransferaz enzim defekti.
• **Moleküler Sonuç:** Selektin ligandı olan **Sialyl-Lewis X (s-Lex) sentezlenemez**.
• **Patolojik Tablo:** Lökositler **YUVARLANMA (ROLLING) YAPAMAZ**.
• **Klinik Bulgular:** LAD-1\'e benzer tekrarlayan enfeksiyonlar, ağır zeka geriliği ve kısa boy.''',
        'professorAudioHighlight': {
            'quote': 'LAD-1 çok meşhurdur, integrin beta-2 zinciri CD18 mutasyonudur. Nötrofil damardan çıkamaz. Hasta bebekte göbek kordonu geç düşer, enfeksiyon olur ama apsede İRİN OLUŞMAZ, kanda lökosit tavan yapar.',
            'note': 'Hoca LAD-1\'in CD18 mutasyonu olduğunu, göbek kordonunun geç düşmesi ve irin oluşamaması ile karakterize olduğunu kurul sorusu olarak vurguladı.',
            'emphasisType': 'exam_trap'
        },
        'flashcards': [
            {
                'id': 'inf-fc-15-01',
                'category': 'Genetik Defekt',
                'front': 'Lökosit Adezyon Eksikliği Tip 1 (LAD-1) patogenezinde hangi integrin alt biriminin genetik mutasyonu yatar?',
                'hint': 'Beta-2 integrin zinciri.',
                'back': '**CD18 (Beta-2 integrin zinciri)** mutasyonudur. LFA-1 ve Mac-1 üretilemez; sıkı adezyon imkansız hale gelir.'
            },
            {
                'id': 'inf-fc-15-02',
                'category': 'Klinik İpucu',
                'front': 'LAD-1 tanılı bir bebekte bakteriyel doku enfeksiyonu geliştiğinde biyopside veya klinik muayenede saptanan en paradoksal patolojik bulgu nedir?',
                'hint': 'Eksüdanın kıvamı.',
                'back': '**Dokuda İRİN (PÜ) ve Nötrofil Eksüdasının OLUŞAMAMASIDIR**. Nötrofiller damar dışına çıkamadığı için irin gelişemez; kanda masif lökositoz görülür.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'LAD-1: Göbek Kordonu',
                    'desc': 'Yenidoğanda göbek kordonunun haftalarca düşmemesi LAD-1 için tipik erken uyarıdır.',
                    'isKey': True
                },
                {
                    'title': 'LAD-2: Fukozil Kusuru',
                    'desc': 'LAD-2 Sialyl-Lewis X yokluğu nedeniyle yuvarlanma basamağının bozulmasıdır.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 29: LAD-1 CD18 integrin kusuru (adezyon yok); LAD-2 Sialyl-Lewis X kusurudur (yuvarlanma yok).',
            'Sınav sorusu: Göbek kordonu geç düşen ve irinsiz enfeksiyon geçiren çocukta defekt? Yanıt: CD18 / Beta-2 integrin.'
        ],
        'relatedQuestions': [q_lokosit_hareket, q_lokosit_toplanma],
        'aiPromptSuggestions': [
            'LAD-1 hastalarında kemik iliği naklinin yeri nedir?',
            'Göbek kordonu fizyolojik olarak nasıl ayrılır?'
        ]
    },

    # Slayt 16
    {
        'slideNumber': 16,
        'title': 'Transmigrasyon (Diapedez) ve Bazal Membran Geçişi',
        'subtitle': 'PECAM-1 (CD31) homofilik bağlanması ve Tip IV kollajenaz aktivitesi',
        'badge': 'Hücresel Olaylar',
        'badgeColor': 'emerald',
        'synthesisNarrative': '''### Endotel Arasından Dokuya Sızış: Diapedez
#### PECAM-1 (CD31) ve Bazal Membran Delinmesi
Endotele sıkıca yapışan lökositin bir sonraki görevi interendotelyal kavşaktan geçerek damar dışı bağ dokusuna adım atmaktır:

💡 **1. Transmigrasyon / Diapedez:**
• Lökositlerin endotel hücrelerinin arasındaki birleşme yerlerinden (interendotelyal kavşaklardan) sıkışarak geçmesine **Transmigrasyon (Diapedez)** denir.
• Bu süreç esas olarak **POSTKAPİLLER VENÜLLERDE** cereyan eder.
• Bu geçişi yöneten en kritik adezyon molekülü **PECAM-1 (Platelet Endothelial Cell Adhesion Molecule-1 / CD31)** dir.
• PECAM-1 hem lökosit üzerinde hem de endotel hücrelerinin temas noktalarında bulunur; **homofilik bağlanma** (CD31-CD31 kenetlenmesi) ile lökositi aralıktan aşağıya çeker.

💡 **2. Bazal Membranın Aşılması:**
• Endoteli geçen lökosit henüz doku parankimine ulaşmış sayılmaz; önünde kalın vasküler bazal membran vardır.
• Lökosit salgıladığı **Kollajenazlar (özellikle Tip IV kollajenaz / Matriks Metalloproteinazlar - MMP)** ile bazal membranı lokal olarak deler ve ekstravasküler interstisyuma çıkar.''',
        'professorAudioHighlight': {
            'quote': 'Diapedez yani transmigrasyon endotel kavşaklarından geçiştir. Burada en kritik molekül PECAM-1 diğer adıyla CD31\'dir. Endoteli geçtikten sonra bazal membranı delmek için kollajenaz salgılarlar.',
            'note': 'Hoca diapedez denince akla CD31 / PECAM-1 molekülünün gelmesi gerektiğini ve bazal membranın kollajenaz ile aşıldığını amfide vurguladı.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-16-01',
                'category': 'Diapedez Molekülü',
                'front': 'Lökositlerin interendotelyal kavşaklardan dokuya geçişinde (transmigrasyon/diapedez) rol oynayan anahtar adezyon molekülü ve CD numarası nedir?',
                'hint': 'Trombosit-endotel hücre adezyon molekülü.',
                'back': '**PECAM-1 (CD31)**. Hem lökosit hem endotel kavşağında eksprese edilir ve homofilik etkileşimle geçişi sağlar.'
            },
            {
                'id': 'inf-fc-16-02',
                'category': 'Enzimatik Bariyer',
                'front': 'Lökosit endoteli aştıktan sonra damar bazal membranını parçalayıp dokuya girebilmek için hangi enzimi salgılar?',
                'hint': 'Bazal membranın temel yapıtaşı Tip IV kollajendir.',
                'back': '**Tip IV Kollajenaz (Matriks Metalloproteinaz / MMP)**.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'CD31 / PECAM-1 İmzası',
                    'desc': 'Diapedez sorulduğunda işaretlenecek kesin seçenek PECAM-1\'dir.',
                    'isKey': True
                },
                {
                    'title': 'Postkapiller Venül Bölgesi',
                    'desc': 'Transmigrasyon mikrosirkülasyonda postkapiller venül endotel kavşaklarında tamamlanır.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 30: Diapedezde PECAM-1 (CD31) rol oynar; bazal membran kollajenaz ile delinir.',
            'Patolojide CD31 vasküler endotel diferansiyasyonunu gösteren en popüler immünhistokimya belirtecidir.'
        ],
        'relatedQuestions': [q_lokosit_hareket, q_lokosit_toplanma],
        'aiPromptSuggestions': [
            'Patolojide CD31 boyası anjiyosarkom tanısında nasıl kullanılır?',
            'Endotelyal sıkı bağlantılar (tight junction) diapedez sırasında nasıl açılır?'
        ]
    },

    # Slayt 17
    {
        'slideNumber': 17,
        'title': 'Kemotaksi ve Kemotaktik Faktörler',
        'subtitle': 'C5a, LTB4, CXCL8 (IL-8), N-formil peptitler ve GPCR / Aktin polimerizasyonu',
        'badge': 'Mekanizma',
        'badgeColor': 'blue',
        'synthesisNarrative': '''### Hedefe Yönelim: Kimyasal Koku İzi
#### Kemotaktik Gradyan Boyunca Aktin Polimerizasyonu
Damardan dışarı çıkan lökosit, hasarın tam merkezine ulaşmak için dokuda kimyasal bir konsantrasyon gradyanını takip eder. Bu hedefe yönelim hareketine **KEMOTAKSİ** denir:

💡 **Başlıca Kemotaktik Faktörler:**
• **Ekzojen Faktörler:** Bakteriyel ürünler (özellikle bakterilerin protein sentezinde kullandığı **N-formil metiyonil peptitler**).
• **Endojen Faktörler:**
  1. **Kompleman Sistemi:** **C5a** (en güçlü kemotaktik kompleman fragmanı).
  2. **Araşidonik Asit Lipoksijenaz Yolu:** **Lökotrien B4 (LTB4)**.
  3. **Kemokinler:** Özellikle nötrofiller için spesifik olan **CXCL8 (İnterlökin-8 / IL-8)**.

💡 **Hücresel Lokomosyon Mekanizması:**
Kemotaktik maddeler lökosit yüzeyindeki **G-proteini kenetli 7-transmembran reseptörlere (GPCR)** bağlanır. Hücre içinde kalsiyum artışı ve küçük GTPazlar (Rac/Rho/Cdc42) aktive olur. Lökositin ön ucunda **Aktin polimerizasyonu** gerçekleşir; lökosit filopod ve lamellipod adı verilen yalancı ayaklar uzatarak gradyanın yoğun olduğu yöne doğru amipsi hareketle ilerler.''',
        'professorAudioHighlight': {
            'quote': 'Kemotaksi kimyasal çekimdir. Lökositi hedefe çeken maddeler: Bakterilerin N-formil peptitleri, komplemandan C5a, lökotrienlerden LTB4 ve sitokinlerden IL-8\'dir. Aktin polimerizasyonuyla yalancı ayak uzatırlar.',
            'note': 'Hoca kemotaktik faktör listesini (C5a, LTB4, IL-8, bakteriyel peptitler) kurul sınavlarının klasik soru kalıbı olarak işaret etti.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-17-01',
                'category': 'Kemotaktik Ajanlar',
                'front': 'Akut enflamasyonda nötrofilleri hasar odağına çeken en güçlü 4 kemotaktik faktör (ekzojen ve endojen) nelerdir?',
                'hint': 'Bakteriyel peptit, kompleman, lökotrien ve sitokin.',
                'back': '1) **Bakteriyel N-formil metiyonil peptitler** (ekzojen)\n2) **Kompleman C5a**\n3) **Lökotrien B4 (LTB4)**\n4) **Kemokin CXCL8 (IL-8)**.'
            },
            {
                'id': 'inf-fc-17-02',
                'category': 'Hücresel Hareket',
                'front': 'Lökositin kemotaktik gradyan yönünde yalancı ayak (filopod/lamellipod) uzatmasını sağlayan hücre iskeleti mekanizması nedir?',
                'hint': 'Hücre ön ucunda mikrofilament oluşumu.',
                'back': 'GPCR sinyaliyle tetiklenen **Aktin Polimerizasyonudur**. Aktin filamentleri ön ucu iterken, miyozin arka ucu sıkarak lökositi ilerletir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Dörtlü Kemotaktik Kadro',
                    'desc': 'Bakteriyel ürünler, C5a, LTB4 ve IL-8 kemotaksinin dört büyük yöneticisidir.',
                    'isKey': True
                },
                {
                    'title': 'GPCR Sinyali',
                    'desc': 'Tüm kemotaktik ajanlar 7-transmembran GPCR reseptörleri üzerinden aktini yönetir.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 33: C5a, LTB4, IL-8 ve N-formil peptitler temel kemotaktik faktörlerdir.',
            'Sınav sorusu: Hangisi kemotaktik değildir? C3b opsonindir, kemotaktik olan C5a\'dır!'
        ],
        'relatedQuestions': [q_lokosit_toplanma, q_lokosit_hareket],
        'aiPromptSuggestions': [
            'C3b ile C5a arasındaki fonksiyonel fark nedir?',
            'Aktin polimerizasyonunu bozan ilaçlar (Sitokalazin B) kemotaksiyi nasıl etkiler?'
        ]
    },

    # Slayt 18
    {
        'slideNumber': 18,
        'title': 'Lökosit Zamanlaması ve Kinetiği: Nötrofil vs Makrofaj',
        'subtitle': 'İlk 6-24 saatte nötrofil üstünlüğü, 24-48 saatte monosit/makrofaj değişimi',
        'badge': 'Müfredat Tablosu',
        'badgeColor': 'amber',
        'synthesisNarrative': '''### Lökosit İnfiltrasyonunun Kronolojisi
#### İlk Müdahale Timi Nötrofiller ve Nöbeti Devralan Makrofajlar (Tablo 2.4)
Akut enflamasyon sahasına lökositlerin ulaşması rastgele değil, katı bir zamansal takvime tabidir:

💡 **Kronolojik Hücre Göçü:**
• **İlk 6 - 24 Saat:** Enflamasyon sahasına **NÖTROFİLLER (PMNL)** hakimdir.
  - *Neden ilk nötrofiller gelir?* Çünkü kanda sayıları çok fazladır (%60-70), endotel adezyon moleküllerine çok daha hızlı yanıt verirler ve kemokinlere süratle hareket ederler.
  - *Kaderleri:* Ömürleri kısadır (dokuda 24-48 saat). Fagositoz yaptıktan sonra hızla **apoptoza** giderler ve parçalanırlar.
• **24 - 48 Saat Sonra:** Sahayı **MONOSİT / MAKROFAJLAR** devralır.
  - Monositler dokuya geçtiklerinde makrofaja dönüşürler.
  - Daha uzun ömürlüdürler (haftalarca/aylarca yaşarlar), sadece mikropları değil apoptotik nötrofil enkazını da temizlerler, sitokin üretirler ve onarımı başlatırlar.

💡 **Özel ve İstisnai Durumlar (Sayfa 38):**
• **Pseudomonas aeruginosa enfeksiyonları:** Günlerce nötrofil infiltrasyonu devam eder!
• **Viral enfeksiyonlar:** İlk andan itibaren baskın hücre **Lenfositlerdir**.
• **Alerjik reaksiyonlar ve Paraziter enfeksiyonlar:** Başlıca hücre **Eozinofillerdir**.''',
        'professorAudioHighlight': {
            'quote': 'İlk 6-24 saatte daima nötrofiller gelir, kanda boldur ve hızlıdırlar ama çabuk ölürler. 24-48 saatte yerini monosit/makrofajlara bırakırlar. Ama dikkat: Pseudomonas enfeksiyonunda günlerce nötrofil kalır, viralde lenfosit, alerjide eozinofil baskındır.',
            'note': 'Hoca sınavda ilk gelen hücrenin nötrofil olduğunu, istisnalarda Pseudomonas\'ta nötrofilin günlerce sürdüğünü özellikle sordu/soracaktır.',
            'emphasisType': 'exam_trap'
        },
        'flashcards': [
            {
                'id': 'inf-fc-18-01',
                'category': 'Hücresel Kinetik',
                'front': 'Tipik bir akut bakteriyel enflamasyonda ilk 6-24 saatte sahaya hakim olan hücre ile 24-48 saat sonra yerini alan hücre hangisidir?',
                'hint': 'Çok parçalı çekirdekli lökosit devri ve mononükleer devir.',
                'back': 'İlk 6-24 saatte: **Nötrofiller (PMNL)**.\n24-48 saat sonra: **Monosit / Makrofajlar**.'
            },
            {
                'id': 'inf-fc-18-02',
                'category': 'İstisnai Durumlar',
                'front': 'Akut enflamasyonun standart hücresel kinetiğine uymayan 3 istisnai etken-hücre eşleşmesi nedir?',
                'hint': 'Ders Notu Sayfa 38.',
                'back': '1) **Pseudomonas enfeksiyonu**: Günlerce devam eden **Nötrofiller**.\n2) **Viral enfeksiyonlar**: İlk andan itibaren **Lenfositler**.\n3) **Alerji ve Parazitler**: **Eozinofiller**.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Nötrofil Ömrü Kısadır',
                    'desc': 'Nötrofil görevini yapıp 24-48 saatte apoptoz ile ölür, makrofajlarca yutulur.',
                    'isKey': True
                },
                {
                    'title': 'Pseudomonas İstisnası',
                    'desc': 'Pseudomonas aeruginosa dokuda günlerce nötrofilik yanıtı tetiklemeyi sürdürür.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ders Notu Tablo 2.4: Nötrofiller ve Makrofajların Karşılaştırmalı Özellikleri',
                'headers': ['Özellik', 'Nötrofiller', 'Makrofajlar'],
                'rows': [
                    ['Köken Aldığı Yer', 'Kemik iliği (kanda olgun)', 'Kemik iliği -> Monosit -> Dokuda Makrofaj'],
                    ['Dokudaki Yaşam Süresi', 'Kısa (1 - 2 gün)', 'Uzun (Aylar - Yıllar)'],
                    ['İnflamasyondaki Zamanı', 'Erken yanıt (İlk 6 - 24 saat)', 'Geç yanıt (24 - 48 saatten itibaren)'],
                    ['Reaktif Oksijen Türleri (ROS)', 'Çok hızlı ve yoğun (Respiratuvar patlama)', 'Daha az ve kademeli'],
                    ['Nitrik Oksit (NO) Üretimi', 'Düşük / Eser', 'Yüksek (iNOS aktivasyonu ile)'],
                    ['Fagositoz Kapasitesi', 'Hızlı tek kullanımlık', 'Büyük kapasiteli, tekrarlı yutma'],
                    ['Doku Onarımındaki Rolü', 'Yok (Yalnızca yıkım ve temizlik)', 'Temel aktör (Büyüme faktörleri salgılar)']
                ]
            }
        },
        'spotPearls': [
            'Ders Notu Sayfa 34-36: İlk 6-24 saatte nötrofiller; 24-48 saatte monosit/makrofajlar baskındır.',
            'Sınav sorusu: Pseudomonas enfeksiyonunda günlerce nötrofil; viralde lenfosit; alerjide eozinofil görülür.'
        ],
        'relatedQuestions': [q_lokosit_toplanma, q_kardinal],
        'aiPromptSuggestions': [
            'Pseudomonas neden günlerce nötrofil infiltrasyonuna yol açar?',
            'Eferositoz (makrofajın apoptotik nötrofili yutması) enflamasyonu nasıl yatıştırır?'
        ]
    },

    # Slayt 19
    {
        'slideNumber': 19,
        'title': 'Fagositoz Basamakları ve Opsonizasyon',
        'subtitle': 'Tanıma, yutma (fagozom), lizozom füzyonu ve opsoninler (IgG, C3b, MBL)',
        'badge': 'Mekanizma',
        'badgeColor': 'rose',
        'synthesisNarrative': '''### Mikropların Yutulması ve Opsonizasyon Sanatı
#### Fagozomdan Fagolizozoma Uzanan 3 Aşamalı Yolculuk
Dokuya ulaşan nötrofil ve makrofajların mikropları ortadan kaldırması 3 aşamalı **FAGOSİTOZ** süreciyle yürütülür:

💡 **Fagositozun 3 Aşaması:**
• **1. Tanıma ve Bağlanma:** Lökosit hedefi doğrudan kendi reseptörleriyle (Mannoz reseptörü, Scavenger reseptörleri) veya çok daha güçlü bir şekilde **Opsoninler** aracılığıyla tanır.
• **2. Hücre İçine Alma (Yutma):** Hedefe bağlanan lökosit psödopodlar (yalancı ayaklar) uzatarak mikrobu çepeçevre sarar. Zar kaynaşır ve mikrop bir kese içine hapsedilir. Bu yapıya **FAGOZOM** denir.
• **3. Sindirme ve Öldürme:** Fagozom lökosit içindeki lizozom granülleriyle birleşerek **FAGOLİZOZOM** oluşturur. İçeriye hidrolitik enzimler ve serbest radikaller boşaltılır.

💡 **Opsonizasyonun Hayati Rolü:**
Çıplak bakteriler fagositoza karşı direnç gösterebilir. Mikropların yüzeyinin konak proteinleriyle kaplanarak fagositoza son derece lezzetli ve kolay yutulabilir hale getirilmesine **OPSONİZASYON**, bu proteinlere **OPSONİN** denir.
• **En Güçlü Opsoninler:**
  1. **İmmünoglobulin G (IgG):** Bakteri antijenine bağlanır; lökosit **FcγR (Fc gama reseptörü)** ile IgG\'nin Fc kuyruğunu yakalar.
  2. **Kompleman C3b ve iC3b:** Bakteri duvarına kovalent bağlanır; lökositteki **CR1, CR3, CR4 (Kompleman Reseptörleri)** tarafından tutulur.
  3. **Mannoz Bağlayan Lektin (MBL)** ve Plazma Kollektinleri.''',
        'professorAudioHighlight': {
            'quote': 'Fagositozun 3 basamağı: Tanıma, yutma (fagozom oluşumu) ve öldürme. Bakteriyi lezzetli hale getiren opsoninlerdir. En önemli iki opsonin: IgG antikorunun Fc parçası ve komplemanın C3b fragmanıdır.',
            'note': 'Hoca en önemli opsoninlerin IgG ve C3b olduğunu, bunların lökosit reseptörleri (FcR ve CR1) ile tanındığını kesin soru olarak belirtti.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-19-01',
                'category': 'Opsoninler',
                'front': 'Mikroorganizmaların yüzeyini kaplayarak fagositozu yüzlerce kat hızlandıran EN GÜÇLÜ 2 opsonin molekülü hangisidir?',
                'hint': 'Antikor sınıfı ve kompleman fragmanı.',
                'back': '1) **İmmünoglobulin G (IgG)** (Fc parçası)\n2) **Kompleman C3b (ve inaktif formu iC3b)**.'
            },
            {
                'id': 'inf-fc-19-02',
                'category': 'Fagositoz Yapısı',
                'front': 'Yutulan mikrobun bulunduğu vakuolün (fagozom) lizozom granülü ile birleşmesiyle oluşan lizitik organel nedir?',
                'hint': 'İki yapının kaynaşmış adı.',
                'back': '**Fagolizozom (Fago-lizozom)**. Mikrop öldürme reaksiyonları bu kapalı vezikülün içinde gerçekleşir.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Opsoninsiz Fagositoz Zayıftır',
                    'desc': 'Kapsüllü bakteriler opsonize edilmeden fagosite edilemez (pnömokok, meningokok).',
                    'isKey': True
                },
                {
                    'title': 'Fc ve CR1 Reseptörleri',
                    'desc': 'Fagositler IgG için FcγRI, C3b için CR1 reseptörleriyle hedefe kilitlenir.',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 39-41: Fagositozun 3 basamağı: Tanıma/bağlanma, yutma ve öldürme/sindirmedir.',
            'Sınav sorusu: En güçlü opsoninler IgG ve C3b\'dir; en güçlü kemotaktik kompleman fragmanı C5a\'dır.'
        ],
        'relatedQuestions': [q_kardinal, q_lokosit_toplanma],
        'aiPromptSuggestions': [
            'Kapsüllü bakteriler neden opsonin olmadan fagositozdan kaçabilir?',
            'Splenektomili hastalarda opsonizasyon kusuru neden ölümcüldür?'
        ]
    },

    # Slayt 20
    {
        'slideNumber': 20,
        'title': 'Hücre İçi Öldürme: ROS, MPO Sistemi ve Genetik Hastalıklar',
        'subtitle': 'Respiratuvar patlama, NADPH oksidaz, Myeloperoksidaz, CGD ve Chédiak-Higashi',
        'badge': 'Biyokimyasal Patoloji',
        'badgeColor': 'rose',
        'synthesisNarrative': '''### Mikrobisidal Mekanizmaların Zirvesi
#### Oksijene Bağımlı Respiratuvar Patlama ve Klinik Defektler
Fagolizozom içine hapsedilen mikroorganizmanın öldürülmesinde en etkili sistem **Oksijene Bağımlı Reaktif Oksijen Türleri (ROS)** mekanizmasıdır:

💡 **1. Respiratuvar Patlama (Respiratory Burst) Biyokimyası:**
• **Adım 1:** Fagolizozom zarındaki **NADPH Oksidaz** enzimi aktive olur; moleküler oksijeni kullanarak **Süperoksit Radikali (O2•-)** üretir.
  $$\\text{NADPH} + 2\\text{O}_2 \\xrightarrow{\\text{NADPH Oksidaz}} \\text{NADP}^+ + \\text{H}^+ + 2\\text{O}_2^{\\bullet-}$$
• **Adım 2:** Süperoksit dismutaz (SOD) süperoksiti **Hidrojen Peroksit (H2O2)**\'e dönüştürür.
• **Adım 3 (En Güçlü Adım):** Nötrofil azurofilik granüllerindeki **Myeloperoksidaz (MPO)** enzimi, klor iyonları (Cl-) varlığında H2O2\'yi **HİPOKLORÖZ ASİTE (HOCl - Çamaşır Suyu!)** çevirir.
  $$\\text{H}_2\\text{O}_2 + \\text{Cl}^- \\xrightarrow{\\text{MPO}} \\text{HOCl} + \\text{OH}^-$$
  HOCl bilinen en güçlü bakterisidal ajandır; saniyeler içinde mikrobiyal protein ve lipidleri oksitleyerek parçalar.

💡 **2. Genetik Klinik Bozukluklar (Sayfa 42-44):**
• **Kronik Granülomatöz Hastalık (CGD):**
  - **NADPH oksidaz gen defekti** (çoğu X\'e bağlı).
  - Respiratuvar patlama gerçekleşemez, H2O2 üretilemez.
  - **Katalaz (+) bakteriler** (Staph. aureus, Serratia, Aspergillus) kendi ürettikleri H2O2\'yi yıktıkları için öldürülemez. Vücut bakteriyi hapsedebilmek için devasa granülomlar kurar. Tanı: **Nitroblue Tetrazolium (NBT) testi negatiftir**.
• **Chédiak-Higashi Sendromu:**
  - **LYST gen mutasyonu** (otozomal resesif).
  - Lizozom ile fagozom kaynaşamaz (**fagolizozom oluşum defekti**).
  - Lökositlerde mikroskopta karakteristik **DEV LİZOZOMAL GRANÜLLER** görülür; nötropeni, albinizm ve tekrarlayan enfeksiyonlar eşlik eder.''',
        'professorAudioHighlight': {
            'quote': 'Respiratuvar patlama: NADPH oksidaz süperoksit yapar, SOD peroksit yapar, Myeloperoksidaz (MPO) ise klorla birleştirip hipokloröz asit (çamaşır suyu) üretir. NADPH oksidaz yoksa hastalık Kronik Granülomatöz Hastalıktır (CGD). Chédiak-Higashi\'de ise fagolizozom füzyonu bozuktur, dev granüller vardır.',
            'note': 'Hoca CGD\'nin NADPH oksidaz eksikliği olduğunu, Chédiak-Higashi\'de fagozom-lizozom kaynaşma kusuru ve dev granüller görüldüğünü amfide defalarca vurguladı.',
            'emphasisType': 'exam_trap'
        },
        'flashcards': [
            {
                'id': 'inf-fc-20-01',
                'category': 'Biyokimyasal Reaksiyon',
                'front': 'Nötrofillerde Myeloperoksidaz (MPO) enziminin H2O2 ve klorid iyonlarını birleştirerek ürettiği en güçlü mikrobisidal bileşik nedir?',
                'hint': 'Çamaşır suyunun etken maddesi.',
                'back': '**Hipokloröz Asit (HOCl)**. Bakteriyel membran lipidlerini ve enzimlerini saniyeler içinde peroksidasyonla parçalar.'
            },
            {
                'id': 'inf-fc-20-02',
                'category': 'Genetik İmmünopatoloji',
                'front': 'NADPH oksidaz enzim kompleksi eksikliğine bağlı gelişen, katalaz-pozitif mikroplarla tekrarlayan granülomatöz enfeksiyonlara yol açan hastalık nedir?',
                'hint': 'NBT boyası negatiftir.',
                'back': '**Kronik Granülomatöz Hastalık (CGD)**. Respiratuvar patlama yapılamaz, süperoksit üretilemez.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'H2O2-MPO-Halid Sistemi',
                    'desc': 'Nötrofillerin hücre içi öldürmedeki en öldürücü biyokimyasal silahıdır.',
                    'isKey': True
                },
                {
                    'title': 'Chédiak-Higashi Triadı',
                    'desc': 'Fagolizozom füzyon defekti + Dev lizozomal granüller + Parsiyel okülokutanöz albinizm.',
                    'isKey': True
                }
            ],
            'formulaBox': {
                'title': 'Respiratuvar Patlama & HOCl Biyosentezi',
                'formula': 'O2 -> (NADPH Oksidaz) -> O2•- -> (SOD) -> H2O2 -> (MPO + Cl-) -> HOCl',
                'explanation': 'HOCl (Hipokloröz asit) bakterileri yok eden nihai kimyasal ajandır; CGD\'de ilk basamak (NADPH oksidaz) tıkalıdır.'
            }
        },
        'spotPearls': [
            'Ders Notu Sayfa 42: MPO sistemi H2O2\'yi hipoklorite (HOCl) çevirir; en etkili bakterisid ajandır.',
            'Sınav sorusu: Dev lizozomal granüller Chédiak-Higashi; NBT negatifliği ve katalaz (+) enfeksiyon CGD göstergesidir.'
        ],
        'relatedQuestions': [q_kardinal],
        'aiPromptSuggestions': [
            'Neden CGD hastaları katalaz-negatif bakterileri (ör. Streptokok) rahatça öldürebilir?',
            'MPO eksikliği olan bireyler neden genellikle asemptomatiktir?'
        ]
    },

    # Slayt 21
    {
        'slideNumber': 21,
        'title': "Nitrik Oksit, NET'ler ve Lökosit Aracılı Doku Hasarı",
        'subtitle': 'iNOS, Peroksinitrit, Netozis (Kromatin ağı), SLE ilişkisi ve Frustrated Fagositoz',
        'badge': 'İleri Patoloji',
        'badgeColor': 'purple',
        'synthesisNarrative': '''### Alternatif Öldürme Mekanizmaları ve Masum Doku Hasarı
#### NET'ler (Nötrofil Dışı Tuzaklar) ve Engellenmiş Fagositoz
Oksijene bağımlı MPO mekanizmasının yanı sıra lökositler ilave ölümcül stratejilere sahiptir:

💡 **1. Nitrik Oksit (NO) ve Peroksinitrit:**
• Makrofajlarda sitokinler (IFN-γ) ile indüklenebilir nitrik oksit sentaz (**iNOS**) uyarılır.
• Üretilen NO, süperoksit radikali (O2•-) ile birleşerek son derece toksik olan **Peroksinitrit (ONOO-)** serbest radikalini oluşturur.

💡 **2. NET'ler (Neutrophil Extracellular Traps / Nötrofil Dışı Tuzaklar):**
• Nötrofiller ölürken nükleer kromatini (DNA ve histonları) parçalayıp antimikrobiyal granül enzimleri (MPO, elastaz) ile birleştirerek hücre dışına fırlatırlar. Bu ağsı örgüye NET denir.
• Mikroplar bu yapışkan ağa takılarak tuzağa düşer ve öldürülür.
• **Otoimmünite Riski (SLE):** NET\'ler hücre dışına nükleer antijenleri ve histonları saçtığı için **Sistemik Lupus Eritematozus (SLE)** gibi hastalıklarda antinükleer antikor (ANA) oluşumunu ve otoimmüniteyi tetikler!

💡 **3. Lökosit Aracılı Doku Hasarı (Frustrated Fagositoz):**
• Lökositler fagosite edemeyecekleri kadar büyük düz yüzeylerle (örneğin glomerül bazal membranı, eklem kıkırdağı, immün kompleks birikintileri) karşılaştıklarında enzimleri hücre içine değil doğrudan **dokuya kusarlar (engellenmiş fagositoz)**. Bu durum Glomerülonefrit ve Romatoid Artritteki masif doku nekrozunun temelidir.''',
        'professorAudioHighlight': {
            'quote': 'NET\'ler nötrofilin intihar ederek kromatin ağını dışarı fırlatmasıdır; mikropları yakalar ama bu nükleer yapılar dışarı çıkınca SLE gibi otoimmün hastalıkları tetikler. Lökosit yutamadığı yere enzimlerini kusarsa buna frustrated fagositoz denir.',
            'note': 'Hoca NET\'lerin otoimmünite (özellikle SLE) patogenezindeki yerini ve doku hasarında frustrated fagositozu özellikle vurguladı.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-21-01',
                'category': 'Hücresel İntihar & Tuzak',
                'front': 'Nötrofillerin nükleer kromatin ağını granül proteinleriyle birleştirip hücre dışına fırlatarak oluşturduğu antimikrobiyal yapıya ne ad verilir ve hangi otoimmün hastalığı tetikler?',
                'hint': 'Netozis ve antinükleer antikorlar.',
                'back': '**NET (Neutrophil Extracellular Trap / Nötrofil Dışı Tuzak)**. Hücre dışına saçılan histon ve DNA, **Sistemik Lupus Eritematozus (SLE)** gelişimini tetikler.'
            },
            {
                'id': 'inf-fc-21-02',
                'category': 'Doku Yıkımı',
                'front': 'Fagositoz yapılamayacak kadar geniş immün birikintilerle (ör. Glomerül bazal membranı) karşılaşan lökositlerin lizozomal enzimleri doğrudan doku aralığına salarak hasar vermesine ne ad verilir?',
                'hint': 'Hayal kırıklığına uğramış / engellenmiş yutma.',
                'back': '**Engellenmiş (Frustrated) Fagositoz**. Glomerülonefrit ve artrit patogenezindeki temel doku yıkım mekanizmasıdır.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Peroksinitrit Toksisitesi',
                    'desc': 'Makrofaj kaynaklı NO ile süperoksitin birleşimi ONOO- oluşturur.',
                    'isKey': True
                },
                {
                    'title': 'NET ve Netozis',
                    'desc': 'Nötrofilin apoptoz ve nekrozdan farklı bir ölüm şeklidir (Netozis).',
                    'isKey': True
                }
            ]
        },
        'spotPearls': [
            'Ders Notu Sayfa 45: NET\'ler kromatin ve enzimlerden oluşur; SLE otoimmünitesine kaynaklık eder.',
            'Frustrated fagositoz glomerülonefritte bazal membranın nötrofil enzimleri tarafından eritilmesidir.'
        ],
        'relatedQuestions': [q_kardinal],
        'aiPromptSuggestions': [
            'Netozis mekanizması ile tromboz gelişimi arasında nasıl bir bağ vardır?',
            'Oksijenden bağımsız öldürme proteinleri (Defensin, Laktoferrin, Lizozim) nasıl çalışır?'
        ]
    },

    # Slayt 22
    {
        'slideNumber': 22,
        'title': 'Morfolojik Kalıplar ve Akut Enflamasyonun Sonuçları',
        'subtitle': 'Seröz, Fibrinöz, Pürülan (Apse), Ülseratif paternler ve 3 nihai sonuç',
        'badge': 'Histopatoloji & Prognoz',
        'badgeColor': 'emerald',
        'synthesisNarrative': '''### Makroskopik ve Mikroskopik Paternler
#### Enflamasyonun Morfolojik İmzaları ve 3 Olası Bitiş Senaryosu
Akut enflamatuvar eksüdanın niteliği ve dokunun anatomik yapısı morfolojik kalıbı belirler:

💡 **1. Morfolojik Kalıplar (Sayfa 48-56):**
• **Seröz Enflamasyon:** Hücreden fakir, berrak proteinli sıvı toplanmasıdır. Peritoneal/plevral efüzyonlar, yanık bülleri ve viral veziküller (Herpes suçiçeği) örnektir.
• **Fibrinöz Enflamasyon:** Şiddetli vasküler geçirgenlik artışı sonucu büyük fibrinojen molekülleri dokuya sızar ve fibrine dönüşür. Seroz membranlarda (perikard, plevra) görülür. Makroskopik olarak **"Ekmek-Tereyağı" (Bread and Butter)** görünümü verir; steteskopla **Friksiyon Sesi (Sürtünme Sesi)** duyulur. Fibrin temizlenemezse organize olarak fibröz yapışıklık (adezyon) bırakır.
• **Pürülan (Süpüratif) Enflamasyon ve Apse:** Piyojenik bakterilerin (Stafilokoklar) yol açtığı yoğun nötrofilik eksüda, likefaksiyon nekrozu ve ödemdir. **Apse:** Çevresi granülasyon dokusu ve fibröz kapsülle sınırlanmış lokalize cerahat (pü) koleksiyonudur.
• **Ülseratif Enflamasyon:** Bir organ veya doku yüzeyindeki enflamatuvar nekroz sonucu epitelin dökülerek krater oluşturmasıdır (Peptik ülser).

💡 **2. Akut Enflamasyonun 3 Olası Sonucu (Sayfa 57-59):**
• **1. Tam Rezolüsyon (Tam İyileşme):** Hasar hafifse, doku kendini yenileyebiliyorsa ve etken temizlenmişse doku orijinal anatomisine döner (Restitutio ad integrum).
• **2. Fibrozis ve Skar (Bağ Dokusu ile İyileşme):** Belirgin doku harabiyeti varsa veya bölünemeyen kalıcı dokularda (miyokard) hasarlı alan kolajenöz skar ile kapatılır.
• **3. Kronik Enflamasyona İlerleme:** Etken temizlenemezse akut faz yerini mononükleer infiltrasyona, anjiyogeneze ve kalıcı destrüksiyona bırakır.''',
        'professorAudioHighlight': {
            'quote': 'Morfolojik kalıplar: Seröz enflamasyonda berrak sıvı, bül vardır. Fibrinöz perikarditte ekmek-tereyağı görünümü ve sürtünme sesi duyulur. Pürülan enflamasyonda piyojenik bakteriler ve likefaksiyon nekrozu apse yapar. Akut enflamasyon ya rezolüsyonla iyileşir ya fibrozis skar bırakır ya da kronikleşir.',
            'note': 'Hoca fibrinöz perikarditin ekmek-tereyağı görünümü ve sürtünme sesi yaptığını, apse merkezinde likefaksiyon nekrozu olduğunu ve 3 olası sonucu dersin özeti olarak aktardı.',
            'emphasisType': 'pearl'
        },
        'flashcards': [
            {
                'id': 'inf-fc-22-01',
                'category': 'Morfolojik Kalıp',
                'front': 'Perikardiyal veya plevral boşlukta "Ekmek-Tereyağı" (Bread and butter) görünümü ve oskültasyonda sürtünme (friksiyon) sesi veren enflamasyon paterni hangisidir?',
                'hint': 'Fibrinojenin polimerize olduğu patern.',
                'back': '**Fibrinöz Enflamasyon**. Şiddetli vasküler kaçakla dışarı çıkan fibrinojenin fibrin ağlarına dönüşmesi sonucu oluşur.'
            },
            {
                'id': 'inf-fc-22-02',
                'category': 'Nihai Sonuçlar',
                'front': 'Akut enflamatuvar sürecin etken temizlendikten veya devam ettikten sonra varabileceği 3 nihai sonuç nedir?',
                'hint': 'Sayfa 57.',
                'back': '1) **Tam Rezolüsyon** (orijinal doku mimarisine tam dönüş)\n2) **Fibrozis / Skarlaşma** (bağ dokusu ile organizasyon)\n3) **Kronik Enflamasyona İlerleme**.'
            }
        ],
        'coreContent': {
            'keyBullets': [
                {
                    'title': 'Apse = Likefaksiyon Nekrozu',
                    'desc': 'Apsenin merkezinde nötrofillerin lizozomal enzimleri dokuyu eriterek sıvı pü havuzu yapar.',
                    'isKey': True
                },
                {
                    'title': 'Rezolüsyon Şartı',
                    'desc': 'Rezolüsyon için hasarlı hücrelerin bölünebilmesi ve bazal membranın korunmuş olması şarttır.',
                    'isKey': True
                }
            ],
            'table': {
                'title': 'Ders Notu Sayfa 48-56: Akut Enflamasyonun Morfolojik Kalıpları Özeti',
                'headers': ['Kalıp Adı', 'Eksüda Tipi', 'Karakteristik Özellik', 'Tipik Klinik Örnek'],
                'rows': [
                    ['Seröz', 'Proteinden zengin berrak sıvı', 'Hücreden fakir, sarımsı transparan sıvı', 'Deri yanık bülü, viral vezikül (Herpes)'],
                    ['Fibrinöz', 'Fibrinojen ve fibrin zengin', 'Pürtüklü ekmek-tereyağı görünümü, sürtünme sesi', 'Üremik veya romatizmal perikardit'],
                    ['Pürülan (Süpüratif)', 'Nötrofil ve nekrotik kalıntı', 'Likefaksiyon nekrozu, cerahat, apse kapsülü', 'Akut apandisit, Stafilokoksik apse'],
                    ['Ülseratif', 'Nekrotik döküntü ve granülasyon', 'Epitel yüzeyinin lokal ekskavasyonu / krateri', 'Mide peptik ülseri, diyabetik ayak ülseri']
                ]
            }
        },
        'spotPearls': [
            'Ders Notu Sayfa 51: Fibrinöz eksüda ekmek-tereyağı görünümü verir; organize olursa fibrozis bırakır.',
            'Pürülan enflamasyon likefaksiyon nekrozu ile karakterizedir; apse cerahat koleksiyonudur.'
        ],
        'relatedQuestions': [q_kardinal],
        'aiPromptSuggestions': [
            'Fibrinöz perikardit ile seröz perikarditin klinik ve EKG farkları nelerdir?',
            'Apse neden antibiyotiklerle tek başına iyileşmez de cerrahi drenaj gerektirir?'
        ]
    }
]

# Master Deste Nesnesi
new_deck = {
    'id': 'deck-acute-inflammation-pathology',
    'title': 'Akut Enflamasyon: Vasküler Değişiklikler ve Hücresel Olaylar',
    'subtitle': 'Karabük Üniversitesi Tıp Fakültesi Dönem 3 Kurul 1 Tıbbi Patoloji Müfredatı (Prof. Dr. Hikmet Keleş)',
    'subject': 'Tıbbi Patoloji',
    'discipline': 'Tıbbi Patoloji',
    'committee': 'Kurul 1',
    'department': 'Temel Tıp Bilimleri / Patoloji AD',
    'professor': 'Prof. Dr. Hikmet Keleş',
    'description': 'Damarlı canlı dokuların enfeksiyon ve doku hasarına karşı verdiği hızlı, lokal ve dinamik savunma yanıtı: Kardinal belirtiler, 5R basamağı, eksüda/transüda ayrımı, mikrovasküler geçirgenlik, lökosit alımı (marjinasyon, yuvarlanma, sıkı adezyon, diapedez, kemotaksi), selektinler, integrinler, fagositoz, ROS/MPO/NO mikrobisidal mekanizmaları, genetik eksiklikler (LAD-1, LAD-2, CGD, Chédiak-Higashi), NETler ve morfolojik kalıplar (seröz, fibrinöz, pürülan, ülser).',
    'estimatedMinutes': 45,
    'tags': [
        'Akut Enflamasyon',
        'Vasküler Geçirgenlik',
        'Lökosit Rekrutmanı',
        'Selektinler',
        'İntegrinler',
        'Fagositoz',
        'ROS ve MPO',
        'Tıbbi Patoloji',
        'Kurul 1'
    ],
    'highYieldPearls': [
        'Enflamasyonun 5 klasik kardinal belirtisi: Rubor (kızarıklık), Calor (sıcaklık), Tumor (şişlik), Dolor (ağrı) ve Functio Laesa\'dır (fonksiyon kaybı - Rudolf Virchow eklemiştir).',
        'Eksüda artmış mikrovasküler geçirgenlikle oluşan, proteini ve hücresi yüksek (dansite >1.020) enflamatuvar sıvıdır; transüda ise bariyer sağlamken hidrostatik/onkotik basınç dengesizliğiyle sızan proteinden fakir (dansite <1.012) sıvıdır.',
        'Artmış damar geçirgenliğinin en sık mekanizması histamin ve bradikinin kaynaklı endotel hücre büzülmesidir ve yalnızca postkapiller venüllerde gerçekleşir; yanık ve nekrozda ise tüm damar segmentlerini tutan doğrudan endotel nekrozu gelişir.',
        'Lökosit ekstravazasyonu sırasıyla: 1) Marjinasyon, 2) Yuvarlanma (Selektinler), 3) Sıkı Adezyon (İntegrinler: LFA-1, Mac-1, VLA-4 ve ligandları ICAM-1, VCAM-1), 4) Transmigrasyon / Diapedez (PECAM-1 / CD31), 5) Kemotaksi (C5a, LTB4, IL-8, N-formil peptitler).',
        'LAD-1 integrin beta-2 zinciri CD18 mutasyonudur (sıkı adezyon bozuk, göbek kordonu geç düşer, apsede İRİN OLUŞMAZ); LAD-2 ise Sialyl-Lewis X kusurudur (yuvarlanma bozuk).',
        'Akut enflamasyonda ilk 6-24 saatte sahaya hakim olan lökosit nötrofildir; 24-48 saat sonra yerini monosit/makrofajlara bırakır. İstisnalar: Pseudomonas\'ta günlerce nötrofil, virüslerde lenfosit, alerji/parazitte eozinofil baskındır.',
        'Hücre içi öldürmede en öldürücü silah respiratuvar patlama ile üretilen H2O2\'yi klorürle birleştirip hipokloröz asit (HOCl) yapan Myeloperoksidaz (MPO) sistemidir.',
        'Kronik Granülomatöz Hastalık (CGD) NADPH oksidaz gen kusurudur; süperoksit üretilemez, katalaz (+) mikroplarla (S. aureus, Aspergillus) granülomatöz enfeksiyonlar gelişir; NBT testi negatiftir.',
        'Chédiak-Higashi sendromunda LYST gen mutasyonu nedeniyle lizozom-fagozom füzyonu bozuktur; periferik yaymada dev lizozomal granüller ve albinizm görülür.',
        'Fibrinöz enflamasyonda ekmek-tereyağı görünümü ve sürtünme sesi duyulur; pürülan enflamasyon likefaksiyon nekrozu ve cerahat koleksiyonu olan apseyle seyreder.'
    ],
    'slides': deck_slides
}

# Listeye ekle / güncelle
updated_decks = [d for d in existing_decks if d['id'] != new_deck['id']]
updated_decks.append(new_deck)

with open(decks_file, 'w', encoding='utf-8') as f:
    json.dump(updated_decks, f, ensure_ascii=False, indent=2)

print(f"Başarıyla güncellendi! Toplam deste sayısı: {len(updated_decks)}")
print(f"Yeni eklenen deste: {new_deck['id']} ({len(new_deck['slides'])} slayt, {len(new_deck['slides']) * 2} akıl kartı)")
