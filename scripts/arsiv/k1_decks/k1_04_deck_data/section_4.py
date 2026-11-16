# -*- coding: utf-8 -*-
from .helpers import (
    make_micro_quiz,
    make_interactive_table,
    make_cloze,
    make_before_after,
    make_causal_chain,
    make_active_recall,
    make_branching_logic,
    make_flashcard
)

def get_steps():
    return [
        {
            "slideNumber": 30,
            "title": "Geri Dönüşümsüz Hasara Geçiş: Geri Dönüşü Olmayan Nokta",
            "subtitle": "The Point of No Return: Hücreyi ölüme mühürleyen biyokimyasal eşik",
            "badge": "Eşik Noktası",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre hasarında geri dönüşümlü evre ile geri dönüşümsüz ölüm arasındaki sınır çizgisi "
                "patolojide 'Geri Dönüşü Olmayan Nokta' (The Point of No Return) olarak adlandırılır. "
                "Stres uyarısı kalıcı veya aşırı şiddetli olduğunda hücre artık homeostazı yeniden "
                "kuramaz. Bu eşiğin aşılmasıyla birlikte hücresel enerji santralleri ve bariyerler çöker.\n\n"
                "> [TEMEL İLKE] İki temel fenomen geri dönüşümsüz hasarı kesin olarak karakterize eder: "
                "1) Mitokondriyal fonksiyonun geri döndürülemez kaybı, 2) Hücre ve organel zarlarında derin bozulma.\n\n"
                "Bu iki olay gerçekleştikten sonra dokuya kan akımı yeniden sağlansa (reperfüzyon) dahi hücre "
                "asla hayata dönemez; ölüm kaçınılmaz bir biyolojik zorunluluk haline gelir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Geri Dönüşsüz Eşik", "desc": "Zararlı etken kalksa dahi hücrenin yaşayamadığı kritik sınırdır.", "isKey": True},
                    {"title": "Mitokondriyal İflas", "desc": "ATP sentezinin geri döndürülemez biçimde durmasıdır.", "isKey": True},
                    {"title": "Membran Yıkımı", "desc": "Plazma zarında onarılamaz yırtıkların açılmasıdır.", "isKey": True}
                ],
                "table": {
                    "title": "Hasarın İki Evresinin Karşılaştırması",
                    "headers": ["Özellik", "Geri Dönüşümlü Evre", "Geri Dönüşümsüz Evre"],
                    "rows": [
                        ["ATP Üretimi", "Azalmış ancak geri kazanılabilir", "Kalıcı sıfırlanmış, geri dönüşsüz"],
                        ["Membran Hasarı", "Sadece blebler var, delik yok", "Geniş zar defektleri ve erime"],
                        ["Mitokondri Yapısı", "Hafif şişme", "Masif şişme, amorf kalsiyum yoğunlukları"],
                        ["Reperfüzyon Yanıtı", "Tam fonksiyonel düzelme", "Kurtarılamaz (aksine hasar artabilir)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Geri dönüşümsüz hasarın iki ana kriteri: 1) Mitokondri fonksiyonunun geri kazanılamaz kaybı, 2) Membran fonksiyonlarında derin ve kalıcı bozulmadır.",
                "🚨 [KRİTİK UYARI] 'Point of no return' aşıldıktan sonra kan akımının sağlanması ölü hücreyi diriltmez."
            ],
            "medicalTerms": [
                {"term": "Point of No Return", "explanation": "Hücre zedelenmesinde geri dönüşümlü fazdan kaçınılmaz hücre ölümüne geçilen kritik biyokimyasal eşiktir."},
                {"term": "Membran Defekti", "explanation": "Hücre zarındaki lipid çift tabakanın yırtılarak serbest geçirgen hale gelmesidir."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Hücre hasarında geri dönüşümlü fazdan kaçınılmaz ölüme geçişi tanımlayan eşik noktasına geri dönüşü olmayan nokta denir.",
                    "geri dönüşü olmayan nokta",
                    "Kritik Eşik"
                ),
                make_active_recall(
                    "Geri dönüşümsüz hücre hasarının evrensel kabul gören iki temel kriteri nedir?",
                    "1) Mitokondriyal fonksiyonun (oksidatif fosforilasyon ve ATP sentezi) geri kazanılamaz biçimde çökmesi, 2) Plazma ve organel zarlarında kalıcı, onarılamaz yapısal ve fonksiyonel hasar gelişmesidir."
                )
            ]
        },
        {
            "slideNumber": 31,
            "title": "Mitokondriyal Kriz: Geç Hasarda Amorf Kalsiyum Yoğunlukları",
            "subtitle": "Matriks şişmesi, krista lizisi ve elektron-yoğun çökeltiler",
            "badge": "Mitokondri",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Mitokondri hücrenin hem enerji üreten jeneratörü hem de apoptozu kontrol eden komuta merkezidir. "
                "Geri dönüşümlü evrede mitokondriler sadece hafifçe şişerken; geri dönüşümsüz evreye geçildiğinde "
                "masif matriks şişmesi, iç membran kristalarının parçalanması ve dış zarın yırtılması gerçekleşir.\n\n"
                "> [SINAV SPOTU] Geç veya geri dönüşümsüz hasara uğramış mitokondrilerin matriksinde elektron "
                "mikroskobunda izlenen büyük, elektron-yoğun, amorf kalsiyum birikintileri geri dönüşümsüzlüğün damgasıdır.\n\n"
                "Mitokondri iç zarında yüksek iletkenlikli 'mitokondriyal geçirgenlik geçiş gözeneği' (MPTP) "
                "açılır. Bu gözenek proton gradientini tamamen sıfırlayarak ATP üretimini imkansız kılar."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Amorf Yoğunluklar", "desc": "Mitokondri matriksinde çöken elektron-yoğun kalsiyum ve denatüre protein agregatlarıdır.", "isKey": True},
                    {"title": "MPTP Açılması", "desc": "İç zardaki kontrolsüz kanalın açılmasıyla zar potansiyelinin yok olmasıdır.", "isKey": True},
                    {"title": "Krista Kaybı", "desc": "Elektron taşıma zincirinin yerleştiği kıvrımların erimesidir.", "isKey": False}
                ],
                "table": {
                    "title": "Mitokondriyal Hasar Evreleri",
                    "headers": ["Evre", "Morfolojik Görünüm (EM)", "Biyokimyasal Durum"],
                    "rows": [
                        ["Normal", "Kompakt matriks, düzenli kristalar", "Yüksek membran potansiyeli, aktif ATP sentezi"],
                        ["Erken (Geri Dönüşümlü)", "Hafif şişme, kristalarda hafif aralanma", "ATP sentezi yavaşlamış fakat geri dönebilir"],
                        ["Geç (Geri Dönüşümsüz)", "Masif şişme, büyük amorf kalsiyum birikintileri", "MPTP açık, ATP sentezi sıfır, Sitokrom c kaçışı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Elektron mikroskobunda mitokondri matriksinde 'büyük amorf elektron-yoğun birikintilerin' görülmesi hasarın geri dönüşümsüz evreye geçtiğini kanıtlar.",
                "📌 [YÜKSEK VERİM] MPTP'nin açılması mitokondri membran potansiyelini sıfırlayarak hücresel enerji krizini kalıcı hale getirir."
            ],
            "medicalTerms": [
                {"term": "Amorf Yoğunluk", "explanation": "Elektron mikroskobunda mitokondri içinde izlenen şekilsiz, koyu renkli kalsiyum-protein çökeltisidir."},
                {"term": "Krista", "explanation": "Mitokondri iç zarının ATP sentaz ve elektron taşıma komplekslerini taşıyan içe doğru kıvrımlarıdır."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Elektron mikroskobunda mitokondri içinde büyük amorf elektron-yoğun kalsiyum birikintilerinin görülmesi geri dönüşümsüz hasar kriteridir.",
                    "geri dönüşümsüz hasar",
                    "Patolojik Evre"
                ),
                make_active_recall(
                    "Mitokondri iç membranında MPTP (mitokondriyal geçirgenlik geçiş kanalı) açıldığında ne olur?",
                    "Mitokondri iç zarı protonlara ve küçük moleküllere tamamen geçirgen hale gelir; membran potansiyeli çöker, ATP sentezi durur ve hücre sitoplazmasına sitokrom c sızarak ölümü kesinleştirir."
                )
            ]
        },
        {
            "slideNumber": 32,
            "title": "Membran Bütünlüğünün Kalıcı Olarak Bozulması",
            "subtitle": "Plazma zarı yırtıkları, fosfolipid kaybı ve hücre içeriğinin sızması",
            "badge": "Membran Hasarı",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Membran hasarı, hücre hasarının nekrozla sonuçlanmasındaki en doğrudan mekanik etkendir. "
                "Hücre zarı bütünlüğünü bozan 3 ana biyokimyasal olay eşzamanlı çalışır: 1) Mitokondriyal "
                "ATP eksikliği nedeniyle yeni fosfolipid sentezinin durması, 2) Kalsiyum aracılı fosfolipazların "
                "mevcut membran lipidlerini hızla yıkması, 3) Reaktif oksijen ürünlerinin (ROS) lipid peroksidasyonu.\n\n"
                "> [TEMEL İLKE] Yıkılan fosfolipidlerden açığa çıkan serbest yağ asitleri ve lizofosfolipidler, "
                "hücre zarında adeta bir deterjan gibi davranarak lipid çift tabakada geri dönüşsüz delikler açar.\n\n"
                "Ayrıca intraselüler proteazlar hücre iskeletini (aktin, spektrin) koparır; hücre zarı "
                "mekanik desteğini yitirerek patlar ve sitoplazma ekstraselüler alana dökülür."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Fosfolipid Kaybı", "desc": "Sentezin durması ve yıkımın artmasıyla membran incelmesi ve delinmesidir.", "isKey": True},
                    {"title": "Deterjan Etkisi", "desc": "Açığa çıkan lizofosfolipidlerin zarı kimyasal olarak eritmesidir.", "isKey": True},
                    {"title": "Sitoiskelet Kopması", "desc": "Proteazların tutunma proteinlerini keserek zarı yırtmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Membran Hasarını Oluşturan Mekanizmalar",
                    "headers": ["Mekanizma", "Biyokimyasal Etken", "Membrana Etkisi"],
                    "rows": [
                        ["Fosfolipid Azalması", "ATP yetersizliği", "Yeni zar sentezi ve onarımı durur"],
                        ["Fosfolipid Parçalanması", "Ca2+ ile aktive fosfolipazlar", "Zar lipidleri yıkılır, lizofosfolipid birikir"],
                        ["Sitoiskelet Hasarı", "Ca2+ ile aktive kalpain/proteazlar", "Membran gerilmeye dayanamaz, blebler yırtılır"],
                        ["Lipid Peroksidasyonu", "Reaktif Oksijen Radikalleri (ROS)", "Doymamış yağ asitleri okside olur, porlar açılır"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Membran hasarının oluşumunda: Fosfolipaz aktivasyonu, lipid peroksidasyonu ve sitoiskelet proteolizi rol oynar.",
                "📌 [YÜKSEK VERİM] Hücre zarının yırtılması nekrozun nihai morfolojik olayıdır; hücre içeriği kana dökülerek inflamasyonu başlatır."
            ],
            "medicalTerms": [
                {"term": "Lipid Çift Tabaka", "explanation": "Hücre zarını oluşturan, içe ve dışa bakan hidrofilik başlar ile ortadaki hidrofobik kuyruklardan oluşan yapıdır."},
                {"term": "Kalpain", "explanation": "Hücre içi kalsiyum yükselmesiyle aktive olan ve hücre iskeletini parçalayan nötral sistein proteazıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Membran Parçalanmasının Mekanizma Zinciri",
                    [
                        "1. Kalsiyum Yükselmesi: Sitozolik kalsiyum fosfolipaz ve proteazları uyarır.",
                        "2. Fosfolipid Yıkımı: Membran lipidleri hızla parçalanır, lizofosfolipidler birikir.",
                        "3. İskelet Bağlantısı Kopması: Proteazlar spektrin ve aktin ağını keser.",
                        "4. Deterjan Etkisi: Biriken serbest yağ asitleri kalan zarı kimyasal olarak çözer.",
                        "5. Kalıcı Membran Rüptürü: Hücre zarı patlar, enzimler kana karışır."
                    ]
                ),
                make_cloze(
                    "Membran fosfolipidlerinin yıkımı sonucu oluşan ve deterjan etkisiyle zarı çözen moleküllere lizofosfolipidler adı verilir.",
                    "lizofosfolipidler",
                    "Zar Yıkım Ürünü"
                )
            ]
        },
        {
            "slideNumber": 33,
            "title": "Lizozomal Enzimlerin Sitozole Boşalması ve Otoliz",
            "subtitle": "Asit hidrolazların aktivasyonu, organel erimesi ve nekroz",
            "badge": "Otoliz",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre içi intihar mekanizmasının bir diğer kritik bileşeni lizozom zarlarının parçalanmasıdır. "
                "Lizozomlar normalde pH 4.5-5.0 aralığında çalışan 40'tan fazla asit hidrolaz (ribonükleaz, "
                "deoksiribonükleaz, proteaz, fosfataz, glukozidaz) içerir. İskemi sırasında anaerobik "
                "glikoliz nedeniyle hücre içi pH asidik hale gelir.\n\n"
                "> [TEMEL İLKE] Lizozom zarı parçalandığında asit hidrolazlar hücre sitozolüne dökülür; "
                "hücre içi zaten asidik olduğu için bu enzimler tam aktiviteyle tüm organelleri eritmeye başlar.\n\n"
                "Ölü hücrenin kendi lizozomal enzimleriyle kendi kendini sindirmesi olayına 'otoliz' denir. "
                "Daha sonra çevreye gelen lökositlerin enzimleri de eklenerek (heteroliz) doku tamamen temizlenir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Asit Hidrolazlar", "desc": "Lizozom içinde hapsolmuş asidik ortamda çalışan yıkıcı enzimlerdir.", "isKey": True},
                    {"title": "Asidozun Rolü", "desc": "Düşük sitoplazmik pH lizozomal enzimlerin sitozolde tam güçle çalışmasını sağlar.", "isKey": True},
                    {"title": "Otoliz Kavramı", "desc": "Hücrenin kendi enzimleri tarafından içeriden eritilmesidir.", "isKey": True}
                ],
                "table": {
                    "title": "Lizozomal Sindirim Mekanizmaları",
                    "headers": ["Sindirim Tipi", "Enzim Kaynağı", "Patolojik Ortam"],
                    "rows": [
                        ["Otoliz", "Ölü hücrenin kendi lizozomları", "Nekroz ve postmortem doku erimesi"],
                        ["Heteroliz", "Gelen lökositlerin (nötrofil/makrofaj) lizozomları", "İnflamatuar eksuda, püy oluşumu"],
                        ["Otofaji", "Canlı hücrenin kendi lizozomuyla yaşlı organeli yemesi", "Besin yokluğu, hücresel adaptasyon"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Ölü hücrenin kendi lizozom enzimleri tarafından sindirilmesine Otoliz; lökositlerin enzimleri tarafından sindirilmesine Heteroliz denir.",
                "📌 [YÜKSEK VERİM] İskemik asidoz (düşük pH), lizozomal asit hidrolazların aktivasyonu için mükemmel bir biyokimyasal zemin hazırlar."
            ],
            "medicalTerms": [
                {"term": "Asit Hidrolaz", "explanation": "Lizozom içinde bulunan ve asidik pH'ta makromolekülleri parçalayan enzim sınıfıdır."},
                {"term": "Heteroliz", "explanation": "Nekrotik dokunun lökosit kaynaklı yabancı enzimler tarafından sindirilmesi sürecidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Doku Sindirim Tipleri",
                    "Otoliz",
                    "Heteroliz",
                    [
                        "Hücrenin kendi lizozom enzimleri çalışır",
                        "Enflamasyon başlamadan içeriden başlar",
                        "Ölü hücre kendi kendini eritir"
                    ],
                    [
                        "İnflamatuar lökositlerin enzimleri çalışır",
                        "Nötrofil ve makrofajlar dokuyu sindirir",
                        "Püy ve apseleşmede baskın sindirim tipidir"
                    ]
                ),
                make_cloze(
                    "Nekroza uğrayan bir hücrenin kendi lizozomal enzimleri tarafından sindirilmesi sürecine otoliz adı verilir.",
                    "otoliz",
                    "Enzimatik Erime"
                )
            ]
        },
        {
            "slideNumber": 34,
            "title": "Klinik Biyobelirteçler: Enzimlerin Kana Sızması",
            "subtitle": "Troponin, CK-MB, AST, ALT, amilaz ve LDH'nin tanısal gücü",
            "badge": "Laboratuvar",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre zarı parçalandığında sitoplazmada hapsolmuş olan organa özgü enzimler ve yapısal "
                "proteinler ekstraselüler aralığa ve lenfatik/venöz dolaşıma dökülür. Kanda bu proteinlerin "
                "saptanması, belirli bir organda geri dönüşümsüz hücre hasarının (nekrozun) gerçekleştiğini "
                "kanıtlayan altın standart klinik yöntemdir.\n\n"
                "> [KLİNİK İPUCU] Kalp kası nekrozunda kanda Troponin I/T ve CK-MB yükselir; hepatosit "
                "nekrozunda ALT ve AST fırlar; akut pankreatitte ise serum amilaz ve lipaz düzeyleri yükselir.\n\n"
                "Geri dönüşümlü hasarda membran delinmediği için bu enzimler kana sızmaz. Dolayısıyla "
                "enzim yüksekliği klinisyene 'hücreler öldü ve zarları parçalandı' mesajını kesin olarak verir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Biyobelirteç İlkesi", "desc": "Zar yırtılmasıyla hücre içi içeriğin dolaşıma geçmesidir.", "isKey": True},
                    {"title": "Doku Özgüllüğü", "desc": "Troponin kalbe, ALT karaciğere, lipaz pankreasa spesifiktir.", "isKey": True},
                    {"title": "Nekroz Kanıtı", "desc": "Enzim yüksekliği geri dönüşümsüz membran hasarının kesin kanıtıdır.", "isKey": True}
                ],
                "table": {
                    "title": "Nekrozun Klinik Biyobelirteçleri",
                    "headers": ["Hasara Uğrayan Doku", "Dolaşıma Sızan Enzim / Protein", "Klinik Tanı"],
                    "rows": [
                        ["Kalp Kası (Miyokard)", "Kardiyak Troponin I ve T, CK-MB", "Akut Miyokard Enfarktüsü (MI)"],
                        ["Karaciğer (Hepatosit)", "ALT (Alanin aminotransferaz), AST", "Akut Toksik veya Viral Hepatit"],
                        ["Pankreas Asinusları", "Amilaz, Lipaz", "Akut Nekrotizan Pankreatit"],
                        ["Çizgili Kas (İskelet)", "Kreatin Kinaz (CK-MM), Miyoglobin", "Rabdomiyoliz, Travma"],
                        ["Safra Yolu Epiteli", "Alkalen Fosfataz (ALP), GGT", "Biliyer Tıkanma, Kolestaz"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Miyokard enfarktüsünde en duyarlı ve spesifik nekroz belirteci Kardiyak Troponin I ve Troponin T'dir.",
                "📌 [YÜKSEK VERİM] Geri dönüşümlü hasarda plazma zarı bütünlüğü korunduğu için hücre içi enzimler kana sızmaz; enzim artışı nekrozun göstergesidir."
            ],
            "medicalTerms": [
                {"term": "Troponin", "explanation": "Çizgili ve kalp kasında aktin-miyozin etkileşimini düzenleyen, miyosit nekrozunda kana karışan proteindir."},
                {"term": "CK-MB", "explanation": "Kreatin kinaz enziminin miyokard dokusuna özgül olan izoenzim formudur."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Klinik Biyobelirteçler",
                    ["Organ", "Dökülen Belirteç", "Klinik Anlam"],
                    [
                        [("Miyokard", False), ("Troponin I / T", True, "Kardiyak Protein"), ("Enfarktüs tanısı", False)],
                        [("Hepatosit", False), ("ALT / AST", True, "Karaciğer Enzimi"), ("Hepatik nekroz", False)],
                        [("Pankreas", False), ("Amilaz / Lipaz", True, "Pankreatik Enzim"), ("Akut pankreatit", False)],
                        [("İskelet Kası", False), ("Miyoglobin / CK", True, "Kas Enzimi"), ("Rabdomiyoliz", False)]
                    ]
                ),
                make_micro_quiz(
                    "Şiddetli göğüs ağrısıyla acil servise başvuran bir hastada kalp kasında geri dönüşümsüz hücre hasarı (nekroz) geliştiğini kanıtlayan en duyarlı ve spesifik serum belirteci hangisidir?",
                    {
                        "A": "Alkalen fosfataz (ALP)",
                        "B": "Kardiyak Troponin I",
                        "C": "Alanin aminotransferaz (ALT)",
                        "D": "Serum amilaz düzeyi",
                        "E": "Asit fosfataz"
                    },
                    "B",
                    {
                        "A": "ALP safra yolları ve kemik patolojilerini gösterir.",
                        "B": "Doğru cevap B'dir: Kardiyak Troponin I ve T kalp kası nekrozunda en duyarlı ve spesifik altın standarttır.",
                        "C": "ALT karaciğer hasarında yükselir.",
                        "D": "Amilaz pankreas nekrozunda artar.",
                        "E": "Asit fosfataz prostat patolojilerinde incelenir."
                    }
                )
            ]
        },
        {
            "slideNumber": 35,
            "title": "İskemi-Reperfüzyon Hasarı: Oksijen Paradoksu",
            "subtitle": "Kan akımının yeniden sağlanmasıyla tetiklenen alevlenme",
            "badge": "Reperfüzyon",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "İskemiye uğramış bir dokuda kan akımının yeniden sağlanması (reperfüzyon), canlı kalmış "
                "hücrelerin kurtarılması için mutlak gerekliliktir. Ancak klinik pratikte bazen kan akımı "
                "sağlandığında doku hasarının düzelmek yerine paradoksal olarak daha da şiddetlendiği görülür; "
                "bu fenomene 'İskemi-Reperfüzyon Hasarı' adı verilir.\n\n"
                "> [TEMEL İLKE] İskemik hücrelere taze oksijenli kan ulaştığında, hasarlı mitokondriler ve "
                "oksidaz enzimleri moleküler oksijeni tam indirgeyemez; masif bir Reaktif Oksijen Radikali (ROS) patlaması yaşanır.\n\n"
                "Ayrıca reperfüzyonla dokuya hızla akan nötrofiller aktive olur, kompleman kaskadı tetiklenir "
                "ve hücre içine kontrolsüz kalsiyum dolarak hücre ölümünü hızlandırır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Oksijen Paradoksu", "desc": "Yeniden gelen oksijenin hasarlı mitokondride serbest radikallere dönüşmesidir.", "isKey": True},
                    {"title": "Nötrofil İstilası", "desc": "Taze kanla dokuya dolan lökositlerin sitokin ve enzimlerle yıkım yapmasıdır.", "isKey": True},
                    {"title": "Kalsiyum Aşırı Yükü", "desc": "Plazma kalsiyumunun hasarlı membranlardan içeri dolarak MPTP'yi açmasıdır.", "isKey": False}
                ],
                "table": {
                    "title": "Reperfüzyon Hasarının 4 Mekanizması",
                    "headers": ["Bileşen", "Biyokimyasal Olay", "Hücresel Sonuç"],
                    "rows": [
                        ["Oksidatif Stres", "Ksantin oksidaz ve mitokondri kaçağı", "Masif ROS üretimi, lipid peroksidasyonu"],
                        ["İntraselüler Kalsiyum", "Reperfüzyonla gelen plazma Ca2+ girişi", "Mitokondriyal MPTP açılması, hiperkontraksiyon"],
                        ["Enflamasyon", "Endotele lökosit adezyonu", "Nötrofil proteazları ve mikrovasküler tıkanma"],
                        ["Kompleman Aktivasyonu", "İskemik dokuda antikor birikimi", "Membran Atak Kompleksi (C5b-9) ile hücre delinmesi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İskemi-reperfüzyon hasarında en kritik rolü oynayan etkenler: Reaktif oksijen türleri (ROS), kalsiyum yüklenmesi ve nötrofil aktivasyonudur.",
                "📌 [KLİNİK İPUCU] Miyokard enfarktüsünde anjiyoplastiyle damar açıldığında reperfüzyon aritmileri ve miyokardiyal 'stunning' görülebilir."
            ],
            "medicalTerms": [
                {"term": "Oksijen Paradoksu", "explanation": "İskemik dokunun oksijensiz yaşayabilip oksijenle temas ettiğinde serbest radikallerle ölmesi fenomenidir."},
                {"term": "Membran Atak Kompleksi", "explanation": "Kompleman sisteminin C5b-9 proteinlerinin birleşerek hücre zarını deldiği komplekstir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "İskemi-Reperfüzyon Hasarı Basamakları",
                    [
                        "1. İskemi Evresi: Doku ATP kaybeder, membranlar zayıflar ve ksantin birikir.",
                        "2. Reperfüzyon Başlangıcı: Oksijenli kan aniden iskemik dokuya akar.",
                        "3. Serbest Radikal Patlaması: Ksantin oksidaz ve mitokondri hızla süperoksit (O2*-) üretir.",
                        "4. Lökosit Akını: Nötrofiller hasarlı endotele yapışarak mikrosirkülasyonu tıkar ve enzim salar.",
                        "5. İkincil Nekroz: Reperfüze edilen hücreler aşırı kalsiyum ve ROS etkisiyle ölür."
                    ]
                ),
                make_cloze(
                    "İskemik dokuya kan akımının yeniden sağlanması sırasında serbest radikal patlamasıyla hasarın artmasına iskemi-reperfüzyon hasarı denir.",
                    "iskemi-reperfüzyon hasarı",
                    "Klinik Fenomen"
                )
            ]
        },
        {
            "slideNumber": 36,
            "title": "DNA ve Kromatin Bütünlüğünün Bozulması",
            "subtitle": "Endonükleaz aktivasyonu, çift zincir kırıkları ve p53 sinyali",
            "badge": "Genetik Hasar",
            "badgeColor": "purple",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre hasarının nükleer boyutu, genomik DNA'nın ve kromatin yapısının parçalanmasıdır. "
                "İyonizan radyasyon, kemoterapötik ilaçlar ve serbest oksijen radikalleri doğrudan nükleer "
                "DNA'da tek ve çift zincir kırıklarına yol açar. Hücre içi kalsiyum yükselmesi ise kromatini "
                "içten kesen kalsiyum-magnezyum bağımlı endonükleazları aktive eder.\n\n"
                "> [TEMEL İLKE] DNA hasarı hafifse p53 proteini hücre döngüsünü G1 evresinde durdurarak onarım "
                "enzimlerine zaman tanır; hasar onarılamaz boyuttaysa p53 BAX/BAK üzerinden apoptozu tetikler.\n\n"
                "Nekrozda ise endonükleazlar DNA'yı gelişi güzel parçalara böler; ışık mikroskobunda "
                "kromatinin solmasına ve erimesine (karyolizis) yol açar."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Çift Zincir Kırıkları", "desc": "DNA sarmalının her iki kolunun kopmasıyla genom bütünlüğünün kaybolmasıdır.", "isKey": True},
                    {"title": "p53 Koruyuculuğu", "desc": "Genomun bekçisi olarak DNA hasarında tamir veya apoptoz kararı vermesidir.", "isKey": True},
                    {"title": "Rastgele Parçalanma", "desc": "Nekrozda nükleazların DNA'yı dağınık parçalayarak kromatini eritmesidir.", "isKey": False}
                ],
                "table": {
                    "title": "DNA Hasarı Yanıt Mekanizmaları",
                    "headers": ["Hasar Düzeyi", "Aktive Olan Yolak", "Hücresel Akıbet"],
                    "rows": [
                        ["Hafif DNA Hasarı", "ATM kinaz → p53 → p21", "G1 fazında duraklama, tamir mekanizmaları aktif"],
                        ["Ağır Hasar (Onarılamaz)", "p53 → PUMA/NOXA → BAX/BAK", "Mitokondriyal apoptoz (sessiz intihar)"],
                        ["İskemik Nekroz", "Ca2+ bağımlı endonükleazlar", "Gelişigüzel DNA parçalanması, karyolizis"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] p53 proteini DNA hasarında hücre döngüsünü durdurur; tamir edilemiyorsa apoptozu başlatır.",
                "📌 [YÜKSEK VERİM] Nekrozda DNA parçalanması rastgeledir (smear görünümü); apoptozda ise internükleozomal kesimle merdiven (ladder) deseni oluşur."
            ],
            "medicalTerms": [
                {"term": "p53 Proteini", "explanation": "Genomun koruyucusu olarak bilinen, DNA hasarında hücre döngüsünü durduran tümör baskılayıcıdır."},
                {"term": "DNA Merdiveni", "explanation": "Apoptozda endonükleazların DNA'yı 180-200 baz çiftlik düzenli parçalara kesmesiyle oluşan elektroforez desenidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "DNA Hasarında Ölüm Yolları",
                    "Düzenli Apoptoz (p53 Aracılı)",
                    "Düzensiz Nekroz (Kalsiyum Aracılı)",
                    [
                        "Internükleozomal düzenli kesim",
                        "Agaroz jelde merdiven (ladder) deseni",
                        "Zar intakt kalır, enflamasyon olmaz",
                        "Enerji (ATP) bağımlı programlı süreç"
                    ],
                    [
                        "Rastgele düzensiz nükleer erime",
                        "Agaroz jelde yayma (smear) görünümü",
                        "Zar yırtılır, masif enflamasyon başlar",
                        "Enerji çöküşüyle pasif parçalanma"
                    ]
                ),
                make_cloze(
                    "Ağır ve onarılamaz DNA hasarında hücreyi apoptoza yönlendiren temel tümör baskılayıcı protein p53 proteinidir.",
                    "p53 proteinidir",
                    "Genom Koruyucusu"
                )
            ]
        },
        {
            "slideNumber": 37,
            "title": "Geri Dönüşümsüz Hasarın Özeti: Üç Ölümcül Kriter",
            "subtitle": "Mitokondriyal çöküş, membran rüptürü ve nükleer erime üçgeni",
            "badge": "Sentez",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "Hücre biyolojisinde geri dönüşümsüz hasarı tanımlayan üç temel direk bir araya geldiğinde "
                "hücre için yaşam şansı tamamen sona erer. Bu üçlü sacayağı: 1) Mitokondriyal fonksiyonun "
                "kalıcı olarak yok olması (ATP üretiminin sıfırlanması ve MPTP açılması), 2) Plazma ve lizozom "
                "zarlarının yaygın parçalanması, 3) Nükleer kromatinin lizisi ve DNA'nın erimesidir.\n\n"
                "> [TEMEL İLKE] Bu üç olaydan herhangi birinin geri dönüşümsüz evreye ulaşması, diğer ikisini "
                "de kaçınılmaz olarak tamamlar ve hücreyi otolitik nekroza sürükler.\n\n"
                "Artık hücre canlı bir biyolojik varlık değil, çevredeki lökositler tarafından temizlenmeyi "
                "bekleyen bir doku enkazı (debris) haline gelmiştir."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "1. Mitokondriyal Kriz", "desc": "Geri kazanılamayan ATP yetersizliği ve amorf kalsiyum yoğunluklarıdır.", "isKey": True},
                    {"title": "2. Membran Rüptürü", "desc": "Plazma zarı delinmesi sonucu sitoplazmik enzimlerin kana dökülmesidir.", "isKey": True},
                    {"title": "3. Kromatin Dağılması", "desc": "Endonükleazlar tarafından nükleer DNA'nın eritilmesidir.", "isKey": True}
                ],
                "table": {
                    "title": "Geri Dönüşümsüz Hasarın 3 Kriteri",
                    "headers": ["Kriter", "Hücresel Gösterge", "Klinik / Morfolojik Kanıt"],
                    "rows": [
                        ["Mitokondriyal Çöküş", "Elektron-yoğun amorf kalsiyum birikimi", "ATP sentezinin geri döndürülemez kaybı"],
                        ["Membran Yıkımı", "Geniş plazma lezyonları, lizozom rüptürü", "Kanda Troponin, ALT, AST yüksekliği"],
                        ["Nükleer Hasar", "Piknoz, karyoreksis, karyolizis", "Işık mikroskobunda nükleer silinme"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Geri dönüşümsüz hasarın 3 vazgeçilmez kriteri: Mitokondri çöküşü, membran rüptürü ve nükleer kromatin hasarıdır.",
                "📌 [YÜKSEK VERİM] Membran rüptürü gerçekleşmeden enzimler kana sızmaz; enzim yüksekliği geri dönüşsüzlüğün kesin kanıtıdır."
            ],
            "medicalTerms": [
                {"term": "Hücresel Debris", "explanation": "Nekroza uğrayıp parçalanan hücrelerden geriye kalan amorf protein ve lipid kalıntılarıdır."},
                {"term": "Nükleer Silinme", "explanation": "Karyolizis sonucu çekirdeğin boyanma özelliğini tamamen kaybedip mikroskopta görünmez olmasıdır."}
            ],
            "interactiveElements": [
                make_cloze(
                    "Hücre hasarında geri dönüşümsüz evrenin en kritik iki özelliği mitokondriyal çöküş ve membran bütünlüğünün kaybıdır.",
                    "membran bütünlüğünün kaybıdır",
                    "Kritik Kriter"
                ),
                make_active_recall(
                    "Geri dönüşümlü hasar ile geri dönüşümsüz hasarı ayıran en temel biyokimyasal ve laboratuvar farkı nedir?",
                    "Geri dönüşümlü hasarda membran bütünlüğü korunduğu için hücre içi enzimler hücrede kalır; geri dönüşümsüz hasarda membran yırtıldığı için troponin, transaminaz gibi enzimler kana dökülür."
                )
            ]
        },
        {
            "slideNumber": 38,
            "title": "İskemik Hücre Hasarında Biyokimyasal Olaylar Dizisi",
            "subtitle": "Glikoliz, asidoz, kalsiyum girişi ve membran lizisinin tam akışı",
            "badge": "Mekanizma",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": (
                "İskemiye uğrayan bir hücrede gelişen patolojik basamaklar kusursuz bir biyokimyasal domino "
                "etkisi izler: 1) Oksijen kesilir, mitokondriyal oksidatif fosforilasyon durur ve ATP azalır. "
                "2) Hücre anaerobik glikolize geçer; glikojen tükenir, laktik asit birikir ve intraselüler pH düşer "
                "(nükleer kromatin kümeleşir).\n\n"
                "> [TEMEL İLKE] 3) ATP tükenmesi Na+/K+ pompasını durdurur; sodyum ve su içeri dolar, ER şişer "
                "ve ribozomlar ayrılır. 4) Ca2+ pompası durur, sitozolik kalsiyum fırlar ve fosfolipazlar zarları deler.\n\n"
                "Sonuçta lizozomlar yırtılır, asit ortamda aktive olan hidrolazlar hücreyi otolize uğratır "
                "ve hücre nekrozla tamamen parçalanır."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "1. ATP Düşüşü", "desc": "Oksidatif fosforilasyonun saniyeler içinde durmasıdır.", "isKey": True},
                    {"title": "2. Asidoz", "desc": "Anaerobik glikolizle laktat birikimi ve pH'ın asidikleşmesidir.", "isKey": True},
                    {"title": "3. İyon Pompaları", "desc": "Na+/K+ ve Ca2+ pompalarının durarak hücresel şişme ve enzim aktivasyonu yapmasıdır.", "isKey": True}
                ],
                "table": {
                    "title": "İskemik Hasarın Adım Adım Akışı",
                    "headers": ["Sıra", "Biyokimyasal Değişiklik", "Morfolojik / Fonksiyonel Yansıma"],
                    "rows": [
                        ["1. Adım", "Oksijen kesilmesi → ATP azalması", "Hücre kasılması durur, bazal metabolizma yavaşlar"],
                        ["2. Adım", "Anaerobik glikoliz artışı → pH düşüşü", "Kromatin topaklanması, glikojen depolarının tükenmesi"],
                        ["3. Adım", "Na+/K+ ATPaz durması → Na+ ve su girişi", "Hücresel şişme, ER dilatasyonu, blebler"],
                        ["4. Adım", "Ca2+ ATPaz durması → Ca2+ hücreye girişi", "Fosfolipaz, proteaz ve endonükleaz aktivasyonu"],
                        ["5. Adım", "Membran yırtılması → Enzim sızması", "Geri dönüşümsüz nekroz, inflamasyon"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] İskemik hücre hasarında erken evrede anaerobik glikoliz artar; laktik asit birikir ve hücre içi pH düşer.",
                "📌 [SINAV SPOTU] Düşük pH hücre içi nükleer kromatinin erken dönemde topaklanmasına (clumping) yol açar."
            ],
            "medicalTerms": [
                {"term": "Kromatin Topaklanması", "explanation": "Asidik hücre içi pH etkisiyle nükleer kromatini oluşturan nükleoproteinlerin kümeleşmesidir."},
                {"term": "Domino Etkisi", "explanation": "Bir biyokimyasal yetersizliğin zincirleme olarak diğer tüm hücresel sistemleri çökertmesidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "İskemik Hücre Hasarının Eksiksiz Biyokimyasal Akışı",
                    [
                        "1. Hipoksi: Oksijen kesilir, mitokondriyal ATP sentezi çöker.",
                        "2. Glikoliz ve Asidoz: Anaerobik glikoliz hızlanır, laktat birikir, pH düşer ve kromatin kümelenir.",
                        "3. Na+/K+ İflası: Na+ ve su içeri dolar, potasyum dışarı kaçar, ER şişer ve ribozomlar ayrılır.",
                        "4. Ca2+ Hücumu: Sitozolik kalsiyum fırlar, fosfolipazlar zarları deler, proteazlar iskeleti keser.",
                        "5. Otoliz ve Nekroz: Lizozomlar patlar, asit hidrolazlar hücreyi içeriden eritir ve enzimler kana sızar."
                    ]
                ),
                make_cloze(
                    "İskemik hücre hasarının erken döneminde anaerobik glikolize bağlı laktat birikimi hücre içi pH'ın düşmesine yol açar.",
                    "pH'ın düşmesine",
                    "Asit-Baz Değişimi"
                )
            ]
        },
        {
            "slideNumber": 39,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Geri Dönüşümsüzlük Kriterleri ve Enzim Salınımı",
            "subtitle": "Mitokondriyal amorf kalsiyum birikintileri, membran yırtığı, troponin ve reperfüzyon",
            "badge": "Checkpoint",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 4,
            "synthesisNarrative": (
                "Dördüncü kontrol noktasında, hücrenin geri dönüşü olmayan noktayı (point of no return) aşarak "
                "geri dönüşümsüz hasara girmesinin tüm biyokimyasal ve mikroskobik kanıtlarını özetliyoruz. "
                "Mitokondri matriksindeki elektron-yoğun amorf kalsiyum yoğunlukları ve membran yırtıkları "
                "hücrenin ölüm fermanıdır.\n\n"
                "> [ÖZET VURGU] Membran yırtıldığında hücre içi enzimler (Troponin, CK-MB, ALT, AST) kana "
                "sızar; reperfüzyon ise serbest radikal patlamasıyla hasarı paradoksal olarak artırabilir.\n\n"
                "Aşağıdaki 3 akıl kartını inceleyerek bu hayati kazanımları hafızanıza sabitleyin."
            ),
            "coreContent": {
                "keyBullets": [
                    {"title": "Amorf Yoğunluklar", "desc": "Mitokondride kalsiyum birikmesi geri dönüşsüzlüğün ultrastrüktürel kanıtıdır.", "isKey": True},
                    {"title": "Klinik Enzimler", "desc": "Troponin, ALT, lipaz yükselmesi membran bütünlüğünün parçalandığını kanıtlar.", "isKey": True},
                    {"title": "Reperfüzyon Hasarı", "desc": "Yeniden gelen oksijenin serbest radikal patlaması ve kalsiyum yükü yaratmasıdır.", "isKey": True}
                ],
                "table": {
                    "title": "Bölüm 4 Sentez Tablosu",
                    "headers": ["Kavram", "Biyokimyasal Gösterge", "Klinik Önem"],
                    "rows": [
                        ["Point of No Return", "Mitokondri ve membran çöküşü", "Hücrenin kurtarılamaz hale geldiği sınır"],
                        ["Amorf Kalsiyum Çökeltisi", "Mitokondri matriksinde EM yoğunluğu", "Geri dönüşümsüz hasarın histolojik damgası"],
                        ["Kardiyak Troponin", "Miyosit membran yırtılması", "Akut miyokard enfarktüsünün kesin tanısı"],
                        ["İskemi-Reperfüzyon", "Masif ROS üretimi, nötrofil infiltrasyonu", "Damar açıldıktan sonra gelişen paradoksal hasar"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Geri dönüşümsüz hasarın mikroskobik kriteri: Mitokondride amorf elektron-yoğun kalsiyum birikintileridir.",
                "📌 [SINAV SPOTU] Kanda Troponin yükselmesi kalp kası hücresinin geri dönüşümsüz membran hasarına uğradığını belgeler."
            ],
            "medicalTerms": [
                {"term": "Troponin T/I", "explanation": "Miyokard nekrozunda plazmaya sızan en duyarlı ve özgül kardiyak hasar belirtecidir."},
                {"term": "Oksidatif Stres", "explanation": "Hücrede serbest radikal üretiminin antioksidan savunma kapasitesini aşması durumudur."}
            ],
            "flashcards": [
                make_flashcard(
                    "fc-k1-04-010",
                    "Elektron mikroskobunda geri dönüşümlü hasar ile geri dönüşümsüz hasar gören mitokondriler nasıl ayırt edilir?",
                    "Geri dönüşümlü hasarda mitokondriler sadece hafifçe şişmiştir; geri dönüşümsüz hasarda ise masif şişme, krista lizisi ve matriks içinde büyük, elektron-yoğun amorf kalsiyum birikintileri görülür."
                ),
                make_flashcard(
                    "fc-k1-04-011",
                    "Geri dönüşümlü hasarda kanda troponin veya karaciğer enzimleri neden yükselmez?",
                    "Çünkü geri dönüşümlü hasarda hücre zarı (plazma membranı) gerilse ve blebler oluştursa dahi bütünlüğü KORUNMUŞTUR; makromoleküller ve enzimler hücre dışına sızamaz."
                ),
                make_flashcard(
                    "fc-k1-04-012",
                    "İskemi-reperfüzyon hasarında dokunun paradoksal olarak daha ağır hasar görmesine yol açan 3 ana mekanizma nedir?",
                    "1) Yeniden gelen oksijenin hasarlı mitokondrilerce reaktif oksijen radikallerine (ROS) dönüştürülmesi, 2) Dokuda masif kalsiyum yüklenmesi, 3) Nötrofillerin ve kompleman sisteminin aktive olması."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kontrol Noktası 4 Sentezi: Bir dokuda geri dönüşümsüz hasara geçildiğinde lizozomal enzimlerin sitozolde bu kadar yıkıcı olabilmesinin nedeni nedir?",
                    "Çünkü iskemik hücrede anaerobik glikolizle laktik asit birikmiş ve pH asidik hale gelmiştir; lizozomal enzimler asit hidrolazlar olduğu için bu düşük pH ortamında maksimum aktiviteyle çalışırlar."
                ),
                make_cloze(
                    "Mitokondri matriksinde elektron mikroskobunda izlenen elektron-yoğun amorf kalsiyum birikintileri geri dönüşümsüz hasarın kesin kanıtıdır.",
                    "amorf kalsiyum",
                    "Mitokondriyal Birikinti"
                )
            ]
        }
    ]
