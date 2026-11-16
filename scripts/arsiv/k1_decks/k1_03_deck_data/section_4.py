#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 4: Hiperplazi: Tanım, Hücre Döngüsü ve Fizyolojik Tipler (Adımlar 30 - 39)
Ders: Tıbbi Patoloji - Hücresel Adaptasyonlar
Öğretim Üyesi: Prof. Dr. Hikmet Keleş
"""

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
        # Adım 30
        {
            "slideNumber": 30,
            "title": "Hiperplazi Tanımı: Hücre Sayısında Artış ve Organ Hacim Değişimi",
            "subtitle": "Hiperplazi, bölünebilen dokularda hücre sayısının artmasıyla organ kütlesinin büyümesidir.",
            "badge": "Temel Tanım",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """**Hiperplazi**, bir organ veya dokudaki parankim hücrelerinin mitoz bölünmeyle sayıca çoğalması sonucu ==doku kütlesinin büyümesidir==.

Hipertrofiden en temel farkı, büyümenin hücre boyutundan değil **hücre sayısından** kaynaklanmasıdır. Hiperplazi yalnızca mitoz yeteneğini koruyan dokularda gerçekleşebilir; bölünmeyen kalıcı dokularda hiperplazi oluşamaz. Genellikle iş yükü veya büyüme faktörü uyarımıyla tetiklenir ve sıklıkla hipertrofi ile eşzamanlı seyreder.

> [TEMEL İLKE] Hiperplazi hücre çoğalmasıdır; bu nedenle yalnızca labil ve stabil hücre popülasyonlarında görülebilir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Sayısal Çoğalma", "desc": "Mitoz yoluyla dokudaki toplam parankim hücresi sayısı artar.", "isKey": True},
                    {"title": "Mitoz Zorunluluğu", "desc": "Hücrelerin hücre döngüsüne (G1, S, G2, M) girebilmesi şarttır.", "isKey": True},
                    {"title": "Kombine Büyüme", "desc": "Çoğu organda hipertrofi ile eşzamanlı olarak birlikte seyreder.", "isKey": False}
                ],
                "table": {
                    "title": "Hiperplazi ve Hipertrofi Karşılaştırması",
                    "headers": ["Parametre", "Hiperplazi", "Hipertrofi"],
                    "rows": [
                        ["Hücresel Temel", "Hücre sayısında artış (mitoz)", "Hücre hacminde artış (biyosentez)"],
                        ["Görüldüğü Dokular", "Yalnızca bölünebilen dokular", "Bölünen ve bölünmeyen tüm dokular"],
                        ["Klasik Örnek", "Parsiyel hepatektomide karaciğer", "Hipertansiyonda sol ventrikül miyokardı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hiperplazi hücre sayısında artıştır ve hücrelerin bölünebilir olmasını gerektirir.",
                "📌 [SINAV SPOTU] Kalp ve iskelet kası hücreleri bölünemediği için hiperplazi yapamaz."
            ],
            "medicalTerms": [
                {"term": "Hiperplazi", "explanation": "Mitoz bölünme yoluyla bir dokudaki hücre sayısının artmasıdır."},
                {"term": "Mitoz", "explanation": "Bir ökaryotik hücrenin genetik materyalini kopyalayarak iki yavru hücreye bölünmesidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Hiperplazi geliştirebilmek için bir dokunun sahip olması gereken en temel hücresel gereklilik nedir?",
                    {
                        "A": "Hücrelerin hücre döngüsüne girip mitozla bölünebilme yeteneğine sahip olması",
                        "B": "Hücrelerin mutlak olarak çizgili kas lifi morfolojisinde bulunması",
                        "C": "Hücre zarlarında kalsiyum kanallarının tamamen bloke olması",
                        "D": "Dokunun tümör baskılayıcı genlerden yoksun olması",
                        "E": "Doku hücrelerinin apoptoza asla gidememesi"
                    },
                    "A",
                    {
                        "A": "Doğru: Hiperplazi sayı artışı olduğundan hücrelerin mitoz yapabilmesi şarttır.",
                        "B": "Yanlış: Çizgili kas bölünemez, hiperplazi yapamaz.",
                        "C": "Yanlış: Kalsiyum kanalları hücre bölünmesi için gereklidir.",
                        "D": "Yanlış: Hiperplazi fizyolojik kontrol altındadır, tümör gen kusuru şart değildir.",
                        "E": "Yanlış: Hiperplastik hücreler normal apoptoz mekanizmalarını korur."
                    }
                ),
                make_cloze(
                    "Dokudaki hücrelerin mitoz yoluyla sayıca çoğalarak organı büyütmesi sürecine [hiperplazi] adı verilir.",
                    "hiperplazi",
                    "Hücre sayısı artışı terimi"
                )
            ]
        },

        # Adım 31
        {
            "slideNumber": 31,
            "title": "Hücre Çoğalması Ön Koşulu: Labil ve Stabil Hücre Popülasyonları",
            "subtitle": "Yalnızca labil (sürekli bölünen) ve stabil (dinlenme fazındaki) hücreler hiperplazi yapabilir.",
            "badge": "Hücre Döngüsü",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hiperplazinin sınırlarını dokunun proliferatif kapasitesi belirler. **Labil hücreler** (epidermis, kemik iliği, gastrointestinal sistem epiteli) yaşam boyu sürekli bölündüklerinden uyaranlara en hızlı ve en yoğun hiperplazi yanıtını verir.

**Stabil hücreler** (hepatositler, böbrek tübül epiteli, fibroblastlar, düz kas) normalde G0 istirahat fazındadır; ancak doku kaybı veya büyüme faktörü sinyali geldiğinde hızla G1 evresine geçerek mitoza başlar. Kalıcı hücreler ise döngüye dönemez.

> [TEMEL İLKE] Labil hücreler fizyolojik döngüde sürekli, stabil hücreler ise hasar veya uyaran anında hiperplazi geliştirir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Labil Hücreler", "desc": "Kök hücre kaynaklıdır; sürekli bölünüp deskuame olan hücreleri yeniler.", "isKey": True},
                    {"title": "Stabil Hücreler", "desc": "G0'da bekler; trofik sinyalle uyarıldığında proliferasyona geçer.", "isKey": True},
                    {"title": "G0/G1 Geçişi", "desc": "Büyüme faktörleri siklin-CDK komplekslerini aktive ederek mitozu başlatır.", "isKey": False}
                ],
                "table": {
                    "title": "Hücre Tipleri ve Proliferasyon Kapasiteleri",
                    "headers": ["Hücre Tipi", "Döngü Evresi", "Hiperplazi Potansiyeli"],
                    "rows": [
                        ["Labil (Epidermis, barsak epiteli)", "Sürekli G1 - S - G2 - M", "Maksimum ve kesintisiz"],
                        ["Stabil (Karaciğer, düz kas, böbrek)", "G0 fazında istirahat", "Uyaranla tetiklenen güçlü yanıt"],
                        ["Kalıcı (Kardiyomiyosit, nöron)", "Döngüyü kalıcı terk etmiş", "Sıfır (hiperplazi yapamaz)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Karaciğer ve böbrek tübül hücreleri stabil (fakültatif) hücrelerdir; uyarıldığında hiperplazi yaparlar.",
                "📌 [SINAV SPOTU] Labil hücreler kök hücre kompartmanından kesintisiz yenilenir."
            ],
            "medicalTerms": [
                {"term": "Labil Hücre", "explanation": "Hücre döngüsünde sürekli kalarak yaşam boyu çoğalan hücre grubudur."},
                {"term": "Stabil Hücre", "explanation": "Normalde G0 fazında dinlenen ancak uyarıldığında hızla mitoza giren hücre grubudur."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Labil ve Stabil Hücrelerin Çoğalma Dinamiği",
                    "Labil Hücre Grubu",
                    "Stabil Hücre Grubu",
                    [
                        "Sürekli hücre döngüsündedir",
                        "Fizyolojik olarak her gün bölünür",
                        "Kemik iliği ve barsak epiteli"
                    ],
                    [
                        "Normalde G0 fazında dinlenir",
                        "Yalnızca doku kaybında uyarılır",
                        "Karaciğer parankimi ve düz kas"
                    ]
                ),
                make_active_recall(
                    "Stabil bir hücre olan karaciğer hepatositinin normalde bölünmeyip yalnızca cerrahi rezeksiyon sonrası mitoza girmesini sağlayan döngü evresi nedir?",
                    "Hepatositler normalde G0 istirahat fazında bekler; rezeksiyon sonrası HGF ve sitokinlerle G1 fazına geçerek hücre döngüsüne girerler."
                )
            ]
        },

        # Adım 32
        {
            "slideNumber": 32,
            "title": "Kök Hücre Aktivasyonu ve Progenitör Hücre Proliferasyonu",
            "subtitle": "Hiperplazi olgun hücrelerin bölünmesiyle veya doku kök hücrelerinin çoğalmasıyla gerçekleşir.",
            "badge": "Kök Hücre Biyolojisi",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hiperplazide hücre sayısının artışı iki temel biyolojik kaynaktan beslenir: **Diferansiye olgun hücrelerin mitozu** ve **doku kök hücrelerinin aktivasyonu**.

Karaciğerde çoğalma esas olarak sağlam olgun hepatositlerin bölünmesiyle yürütülür. Buna karşılık hematopoetik sistem, cilt ve intestinal kriptalarda hiperplazi doğrudan dokuda yerleşik **erişkin kök hücrelerin** ve geçiş amplifiye edici progenitör hücrelerin uyarılmasıyla sağlanır.

> [TEMEL İLKE] Dokunun kök hücre nişi ve progenitör havuzu, hiperplazinin hızını ve kapasitesini belirleyen temel rezervdir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "İki Kaynak", "desc": "Olgun hücrelerin bölünmesi ve doku kök hücrelerinin çoğalması.", "isKey": True},
                    {"title": "Kök Hücre Nişi", "desc": "Kök hücreleri çevreleyen mikroçevre büyüme ve farklılaşma sinyallerini yönetir.", "isKey": True},
                    {"title": "Klonal Kontrol", "desc": "Kök hücre aktivasyonu fizyolojik denetim altındadır, kontrolsüz klonal neoplazi değildir.", "isKey": False}
                ],
                "table": {
                    "title": "Dokularda Hiperplazi Kaynakları",
                    "headers": ["Doku", "Baskın Çoğalma Kaynağı", "Regülasyon Mekanizması"],
                    "rows": [
                        ["Karaciğer", "Olgun hepatositlerin doğrudan bölünmesi", "HGF, TGF-alfa ve sitokinler"],
                        ["Epidermis", "Bazal tabaka kök hücreleri", "EGF ve keratinosit büyüme faktörü"],
                        ["Kemik İliği", "Hematopoetik kök hücreler (HSC)", "Eritropoietin, G-CSF ve trombopoietin"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Karaciğer rejenerasyonunda primer çoğalma kaynağı olgun hepatositlerin kendisidir.",
                "📌 [SINAV SPOTU] Epitel ve kemik iliğinde hiperplazi doku kök hücrelerinin aktivasyonuyla yürütülür."
            ],
            "medicalTerms": [
                {"term": "Kök Hücre Nişi", "explanation": "Kök hücrelerin canlılığını ve kendini yenilemesini sağlayan özelleşmiş mikroçevredir."},
                {"term": "Progenitör Hücre", "explanation": "Kök hücreden türeyen ve belirli bir yönde farklılaşma kapasitesi taşıyan öncül hücredir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Kök Hücre Aracılı Epitelyal Hiperplazi Kaskadı",
                    [
                        "1. Doku Hasarı/Uyaran: Yüzeyel epitelin dökülmesi veya mekanik aşınma.",
                        "2. Büyüme Faktörü Salınımı: Fibroblast ve lökositlerden EGF ve FGF salgısı.",
                        "3. Niş Sinyali: Bazal kök hücrelerin asimetrik bölünmeye yönlendirilmesi.",
                        "4. Progenitör Çoğalması: Hızla bölünen öncül hücre havuzunun genişlemesi.",
                        "5. Epitelyal Diferensiasyon: Yeni hücrelerin yüzeye göç ederek defekti kapatması."
                    ]
                ),
                make_cloze(
                    "Dokularda hiperplazi olgun hücrelerin bölünmesiyle veya dokuda yerleşik [kök hücre] havuzunun uyarılmasıyla sağlanır.",
                    "kök hücre",
                    "Yenilenme sağlayan temel öncül hücre"
                )
            ]
        },

        # Adım 33
        {
            "slideNumber": 33,
            "title": "Büyüme Faktörü Aracılı Sinyal İletimi: MAPK ve PI3K/Akt Yolakları",
            "subtitle": "Hiperplazi tetikleyicileri tirozin kinaz reseptörleri üzerinden mitojenik yolakları uyarır.",
            "badge": "Sinyal İletimi",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hiperplazinin moleküler itici gücü büyüme faktörlerinin hücre yüzeyindeki **reseptör tirozin kinazlara (RTK)** bağlanmasıdır. Bağlanma reseptör dimerizasyonunu ve otofosforilasyonu tetikler.

Bu sinyal iki ana kol üzerinden ilerler: **Ras/Raf/MEK/ERK (MAPK)** yolağı doğrudan hücre siklusuna giriş ve mitoz genlerini aktive ederken; **PI3K/Akt/mTOR** yolağı hücre büyümesini, besin alımını ve protein sentezini destekler. Birlikte çalıştıklarında hücreler hızla çoğalır.

> [TEMEL İLKE] MAPK yolağı mitojenik çoğalmayı (hiperplazi), PI3K/Akt yolağı ise hücresel anabolizmayı yönlendirir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "MAPK Yolağı", "desc": "Ras üzerinden siklin D sentezini uyararak G1/S kontrol noktasını aştırır.", "isKey": True},
                    {"title": "PI3K/Akt Yolağı", "desc": "Hücre sağkalımını ve ribozomal translasyonu aktive eder.", "isKey": True},
                    {"title": "Siklin Bağımlı Kinazlar", "desc": "CDK4/6 retinoblastom (Rb) proteinini fosforilleyerek E2F'yi serbest bırakır.", "isKey": False}
                ],
                "table": {
                    "title": "Mitojenik Sinyal Yolakları",
                    "headers": ["Yolak", "Temel İletici Moleküller", "Hücresel Sonuç"],
                    "rows": [
                        ["MAPK Kaskadı", "Ras -> Raf -> MEK -> ERK", "Mitoz bölünme ve hiperplazi"],
                        ["PI3K / Akt Kaskadı", "PI3K -> PIP3 -> Akt -> mTOR", "Hücre büyümesi, hayatta kalma"],
                        ["JAK / STAT Kaskadı", "Sitokin reseptörleri -> STAT dimerleri", "Enflamatuvar ve rejeneratif hiperplazi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Ras/MAPK yolağı büyüme faktörlerinin hücre bölünmesini (hiperplazi) uyaran ana yolağıdır.",
                "📌 [SINAV SPOTU] Siklin D / CDK4 kompleksi Rb proteinini fosforilleyerek hücreyi S fazına sokar."
            ],
            "medicalTerms": [
                {"term": "Tirozin Kinaz", "explanation": "Proteinlerdeki tirozin amino asitlerine fosfat ekleyerek sinyal ileten enzimdir."},
                {"term": "Siklin D", "explanation": "Hücre döngüsünün G1 fazından S fazına geçişini başlatan düzenleyici proteindir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Büyüme faktörlerinin hücre zarındaki reseptörlerine bağlanması sonucu hücre döngüsünü G1'den S fazına geçirerek hiperplaziyi başlatan temel hücre içi sinyal yolağı hangisidir?",
                    {
                        "A": "Ras / MAPK yolağı",
                        "B": "Apoptozom / Kaspaz-9 yolağı",
                        "C": "Kompleman membran atak kompleksi",
                        "D": "Ubikuitin-proteazom yolağı",
                        "E": "Anafilatoksin kaskadı"
                    },
                    "A",
                    {
                        "A": "Doğru: Ras/Raf/MEK/ERK (MAPK) kaskadı mitozu başlatan ana mitojenik yoldur.",
                        "B": "Yanlış: Kaspaz-9 apoptoz ölüm yolağıdır.",
                        "C": "Yanlış: Membran atak kompleksi kompleman aracılı hücre lizisidir.",
                        "D": "Yanlış: Ubikuitin proteazom protein yıkar, çoğaltmaz.",
                        "E": "Yanlış: Anafilatoksin inflamasyon mediyatörüdür."
                    }
                ),
                make_cloze(
                    "Büyüme faktörleri hücre döngüsünü başlatmak için [MAPK] sinyal iletim yolağını aktive eder.",
                    "MAPK",
                    "Mitojenle aktive olan protein kinaz kısaltması"
                )
            ]
        },

        # Adım 34
        {
            "slideNumber": 34,
            "title": "Hormonal Fizyolojik Hiperplazi: Ergenlik ve Gebelikte Meme Glandları",
            "subtitle": "Meme dokusu ergenlikte ve gebelikte hormonların etkisiyle fizyolojik glandüler hiperplaziye uğrar.",
            "badge": "Fizyolojik Örnek",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hormonal fizyolojik hiperplazinin en klasik modellerinden biri kadın **meme glandüler epitelinde** görülür. Pubertede östrojen uyarımıyla duktus sistemi dallanır ve meme dokusu genişler.

Gebelikte ise östrojen, progesteron ve prolaktin hormonlarının senkronize etkisiyle lobüllerdeki asinüs hücreleri yoğun biçimde çoğalarak ==glandüler hiperplazi== geliştirir. Lobül sayısı ve glandüler hücre miktarı katlanarak laktasyona (süt üretimine) hazır hale gelir. Emzirme bittiğinde ise apoptozla küçülür.

> [TEMEL İLKE] Meme glandüler hiperplazisi, hormon seviyesi normale döndüğünde apoptozla eski hacmine dönebilen kusursuz bir fizyolojik adaptasyondur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hormon Kokteyli", "desc": "Östrojen, progesteron ve prolaktin glandüler çoğalmayı senkronize uyarır.", "isKey": True},
                    {"title": "Lobüler Çoğalma", "desc": "Asinüs sayısı artar, stroma daralır, meme salgı yapacak mimariyi kazanır.", "isKey": True},
                    {"title": "Laktasyon Sonrası", "desc": "Süt kesilince hücreler programlı hücre ölümüyle (apoptoz) dökülür ve geriler.", "isKey": False}
                ],
                "table": {
                    "title": "Farklı Yaşam Evrelerinde Meme Gland Mimarisi",
                    "headers": ["Evre", "Baskın Hormonal Etki", "Histopatolojik Tablo"],
                    "rows": [
                        ["Puberte", "Östrojen baskın", "Duktusların uzaması ve stromal yağlanma"],
                        ["Gebelik", "Östrojen + Progesteron + Prolaktin", "Yaygın glandüler lobüler hiperplazi"],
                        ["Laktasyon Sonu", "Hormonların ani çekilmesi", "Apoptoz aracılı involüsyon ve gerileme"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Gebelikte meme bezlerinin büyümesi fizyolojik hormonal hiperplazinin tipik örneğidir.",
                "📌 [SINAV SPOTU] Emzirme bittikten sonra memenin küçülmesi apoptoz mekanizmasıyla gerçekleşir."
            ],
            "medicalTerms": [
                {"term": "Glandüler Hiperplazi", "explanation": "Salgı bezlerini oluşturan epitel hücrelerinin hormon etkisiyle sayıca çoğalmasıdır."},
                {"term": "Lobül İnvolüsyonu", "explanation": "Laktasyon bittiğinde artmış bez yapılarının apoptozla temizlenerek küçülmesidir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Gebe Olmayan ve Gebe Meme Dokusu Histolojisi",
                    "Gebe Olmayan Meme Dokusu",
                    "Gebe / Laktasyonel Meme Dokusu",
                    [
                        "Belirgin fibröz ve yağlı stroma",
                        "Küçük, seyrek asinüs lobülleri",
                        "İstirahat halinde salgısız lümen"
                    ],
                    [
                        "Yoğun biçimde çoğalmış asinüsler",
                        "Glandüler hiperplazi ile stromada daralma",
                        "Genişlemiş ve kolostrum/süt dolu lümenler"
                    ]
                ),
                make_cloze(
                    "Gebelikte meme dokusundaki asinüs hücrelerinin çoğalarak süt vermeye hazırlanması [fizyolojik] hormonal hiperplazidir.",
                    "fizyolojik",
                    "Doğal biyolojik süreç niteliği"
                )
            ]
        },

        # Adım 35
        {
            "slideNumber": 35,
            "title": "Hormonal Fizyolojik Hiperplazi: Siklik Endometriyal Proliferasyon",
            "subtitle": "Her menstrüel siklusta östrojen uyarısıyla endometrium bezleri ve stroması fizyolojik olarak çoğalır.",
            "badge": "Siklik Proliferasyon",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Her menstrüel siklusun ilk yarısında (foliküler / proliferatif faz) overden salgılanan östrojen hormonu, uterusun iç astarı olan **endometriyumda fizyolojik hiperplazi** başlatır.

Östrojen etkisiyle endometriyal bez epitel hücreleri ve stroma hücreleri hızla mitoza girer. Bezler uzar, kıvrımlanır ve endometriyal tabakanın kalınlığı 1-2 mm'den 5-7 mm'ye yükselir. Ovülasyon sonrası progesteron devreye girdiğinde proliferasyon durur ve bezler sekretuar faza geçer.

> [TEMEL İLKE] Proliferatif faz endometriyumu, hormonların kontrolünde her ay tekrarlanan düzenli fizyolojik bir hiperplazi modelidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Foliküler Faz", "desc": "Over foliküllerinden salgılanan östrojen mitojenik uyaran olarak görev yapar.", "isKey": True},
                    {"title": "Bez ve Stroma Mitozu", "desc": "Hem bez hücrelerinde hem de stromal fibroblastlarda belirgin mitoz izlenir.", "isKey": True},
                    {"title": "Progesteron Freni", "desc": "Ovülasyon sonrası progesteron mitotik aktiviteyi durdurur ve sekresyonu başlatır.", "isKey": False}
                ],
                "table": {
                    "title": "Siklik Endometrium Evreleri",
                    "headers": ["Evre", "Baskın Hormon", "Histopatolojik Özellik"],
                    "rows": [
                        ["Proliferatif Faz", "Östrojen", "Düzgün tübüler bezler, yoğun mitoz (Hiperplazi)"],
                        ["Sekretuar Faz", "Progesteron", "Kıvrıntılı testere dişi bezler, vakuoller, mitoz yok"],
                        ["Menstrüel Faz", "Hormon çekilmesi", "Damar spazmı, iskemik dökülme ve kanama"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Menstrüel siklusun proliferatif fazı fizyolojik hormonal hiperplazi örneğidir.",
                "📌 [SINAV SPOTU] Progesteron hormonu östrojenin başlattığı endometriyal hiperplaziyi durduran doğal dengeleyicidir."
            ],
            "medicalTerms": [
                {"term": "Proliferatif Faz", "explanation": "Östrojen etkisiyle endometriyal bez ve stromanın hızla bölündüğü siklus evresidir."},
                {"term": "Sekretuar Faz", "explanation": "Progesteron etkisiyle mitozun durup bezlerin salgı yaptığı siklus evresidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Menstrüel siklusun proliferatif fazında endometriyum tabakasının kalınlaşması ve bezlerin çoğalması hangi hücresel sürecin fizyolojik örneğidir?",
                    {
                        "A": "Fizyolojik hormonal hiperplazi",
                        "B": "Patolojik atipili hiperplazi",
                        "C": "Skuamöz metaplazi",
                        "D": "Kazeöz nekroz",
                        "E": "Disuse atrofisi"
                    },
                    "A",
                    {
                        "A": "Doğru: Östrojen uyarımıyla her ay tekrarlanan normal bez çoğalması fizyolojik hiperplazidir.",
                        "B": "Yanlış: Siklik süreç patolojik değildir, atipi içermez.",
                        "C": "Yanlış: Endometrium kolumnar kalır, yassılaşmaz.",
                        "D": "Yanlış: Fizyolojik evrede kazeöz nekroz görülmez.",
                        "E": "Yanlış: Atrofi değil belirgin kütle ve kalınlık artışıdır."
                    }
                ),
                make_cloze(
                    "Menstrüel siklusun ilk yarısında over kaynaklı [östrojen] hormonu endometriyal bezlerde fizyolojik hiperplazi başlatır.",
                    "östrojen",
                    "Proliferatif faz hormonu"
                )
            ]
        },

        # Adım 36
        {
            "slideNumber": 36,
            "title": "Kompansatuvar (Telafi Edici) Hiperplazi Prensibi",
            "subtitle": "Bir organın bir kısmı cerrahi veya hasarla kaybedildiğinde kalan parankim çoğalarak kütleyi tamamlar.",
            "badge": "Telafi Edici Yanıt",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hücresel adaptasyonun en mucizevi biçimlerinden biri **kompansatuvar (telafi edici) hiperplazidir**. Bir organın bir bölümü cerrahi olarak rezeke edildiğinde veya hasar gördüğünde, kalan sağlam parankim hücreleri hızla çoğalarak kaybedilen fonksiyonel kütleyi yerine koyar.

Burada temel amaç artan iş yükünü karşılamak ve organ kütlesini orijinal ağırlığına ulaştırmaktır. Kütle tamamlandığında büyüme durur; bu özellik kompansatuvar hiperplaziyi neoplaziden (kanserden) ayıran en temel biyolojik emniyet sübabıdır.

> [TEMEL İLKE] Kompansatuvar hiperplazi, organ orijinal kütlesine ulaştığında büyüme inhibitörleri (TGF-β) tarafından kesin olarak sonlandırılır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Doku Kaybı Tetikleyici", "desc": "Organın bir kısmının çıkarılması kalan hücrelerde mitozu ateşler.", "isKey": True},
                    {"title": "Fonksiyonel Tamamlanma", "desc": "Amaç organın metabolik ve fonksiyonel dengesini yeniden kurmaktır.", "isKey": True},
                    {"title": "Kontrollü Sonlanma", "desc": "Gereken kütleye ulaşıldığında büyüme kendiliğinden durur.", "isKey": False}
                ],
                "table": {
                    "title": "Kompansatuvar Hiperplazi Modelleri",
                    "headers": ["Organ", "Tetikleyici Neden", "Biyolojik Sonuç"],
                    "rows": [
                        ["Karaciğer", "Parsiyel hepatektomi (lobların çıkarılması)", "Kalan lobların büyüyerek eski kütleye dönmesi"],
                        ["Böbrek", "Tek taraflı nefrektomi (böbrek alınması)", "Kalan böbrekte kompansatuvar hipertrofi + hiperplazi"],
                        ["Kemik İliği", "Akut kanama veya hemoliz", "Eritroid seride yoğun kompanse hiperplazi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Parsiyel hepatektomi sonrası karaciğerin büyümesi kompansatuvar hiperplazinin altın standart örneğidir.",
                "📌 [SINAV SPOTU] Tek böbrek alındığında karşı böbrek büyür; nefron sayısı artmaz ancak tübüller hipertrofi ve hiperplaziye uğrar."
            ],
            "medicalTerms": [
                {"term": "Kompansatuvar Hiperplazi", "explanation": "Organ kaybı veya hasarı sonrası kalan parankim hücrelerinin çoğalarak kütleyi tamamlamasıdır."},
                {"term": "Nefrektomi", "explanation": "Böbreğin cerrahi olarak vücuttan çıkarılması ameliyatıdır."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Kompansatuvar Adaptasyon Örnekleri ve Mekanizmaları",
                    ["Klinik Durum", "Biyolojik Mekanizma", "Gelişen Adaptasyon"],
                    [
                        [
                            ("Karaciğerin 2/3'ünün rezeksiyonu", False),
                            ("Sağlam hepatositlerin mitozla çoğalması", True, "HGF aracılı mitoz"),
                            ("Kompansatuvar hiperplazi", False)
                        ],
                        [
                            ("Tek böbreğin cerrahi çıkarılması", False),
                            ("Karşı böbrek nefronlarının yük artışı", True, "Tübül hücresi büyümesi"),
                            ("Kompansatuvar hipertrofi ve hiperplazi", False)
                        ],
                        [
                            ("Ağır gastrointestinal kanama", False),
                            ("Eritropoietin uyarısıyla kök hücre artışı", True, "Hematopoetik çoğalma"),
                            ("Kemik iliği eritroid hiperplazisi", False)
                        ]
                    ]
                ),
                make_active_recall(
                    "Kompansatuvar karaciğer hiperplazisinde organ tam eski kütlesine ulaştığında mitozu durduran temel büyüme inhibitörü sitokin hangisidir?",
                    "Transforme edici büyüme faktörü-beta (TGF-β), karaciğer kütlesi tamamlandığında hepatosit proliferasyonunu durduran ana inhibitördür."
                )
            ]
        },

        # Adım 37
        {
            "slideNumber": 37,
            "title": "Parsiyel Hepatektomi Sonrası Karaciğer Rejenerasyonu",
            "subtitle": "Karaciğerin üçte ikisi cerrahi olarak çıkarıldığında kalan loblar günler içinde orijinal kütleyi yeniden oluşturur.",
            "badge": "Karaciğer Rejenerasyonu",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Karaciğerin telafi edici yeteneği tıp dünyasındaki en dramatik rejenerasyon örneğidir. Karaciğerin yaklaşık %60-70'i cerrahi olarak çıkarıldığında (parsiyel hepatektomi), çıkarılan loblar anatomik olarak yeniden büyümez; ancak **kalan loblardaki hepatositler hızla bölünerek** organı eski toplam kütlesine ulaştırır.

İnsanda rezeksiyondan sonraki ilk 24-48 saat içinde hepatositlerin neredeyse tamamı G0 fazından çıkarak DNA sentezine (S fazı) girer. Süreç öylesine hızlıdır ki, 1-2 hafta içinde karaciğer fonksiyonel hacmini tamamen tamamlar.

> [TEMEL İLKE] Karaciğer rejenerasyonu çıkarılan lobların yeniden oluşması değil; kalan loblardaki hücrelerin hiperplazisi ile kütlenin tamamlanmasıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Mitoz Patlaması", "desc": "İstirahat halindeki hepatositlerin %95'inden fazlası eşzamanlı döngüye girer.", "isKey": True},
                    {"title": "Anatomik Şekil", "desc": "Eski loblar yeniden çıkmaz; kalan loblar hacimsel olarak büyür.", "isKey": True},
                    {"title": "Süreç Hızı", "desc": "Kemirgenlerde 1 haftada, insanda birkaç haftada kütle tamamlanır.", "isKey": False}
                ],
                "table": {
                    "title": "Karaciğer Rejenerasyonu Aşamaları",
                    "headers": ["Aşama", "Zaman Aralığı", "Temel Hücresel Olay"],
                    "rows": [
                        ["Hazırlık (Priming)", "İlk 0 - 4 saat", "Kupffer hücrelerinden IL-6 ve TNF-alfa salınımı"],
                        ["Proliferasyon Fazı", "12 - 72 saat", "HGF ve EGF ile hepatosit mitozu"],
                        ["İnhibisyon Fazı", "Kütle tamamlanınca", "TGF-beta salınımı ve döngüden çıkış"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Parsiyel hepatektomi sonrası karaciğer kütlesi telafi edici (kompansatuvar) hiperplazi ile tamamlanır.",
                "📌 [SINAV SPOTU] Karaciğer rejenerasyonunu başlatan ön hazırlık sinyalleri IL-6 ve TNF-alfa sitokinleridir."
            ],
            "medicalTerms": [
                {"term": "Parsiyel Hepatektomi", "explanation": "Karaciğerin bir kısmının (örneğin tümör nedeniyle) cerrahi olarak kesilip çıkarılmasıdır."},
                {"term": "Priming (Hazırlık)", "explanation": "İstirahat halindeki hepatositlerin büyüme faktörlerine duyarlı hale getirilmesi evresidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Parsiyel Hepatektomi Rejenerasyon Döngüsü",
                    [
                        "1. Rezeksiyon: Karaciğer loblarının cerrahi olarak çıkarılması.",
                        "2. Priming Sinyali: Portal kanda artan endotoksinlerin Kupffer hücrelerini uyarması ve IL-6 salgısı.",
                        "3. Büyüme Uyarımı: Hepatosit Büyüme Faktörü (HGF) ile hepatositlerin G1 fazından S fazına geçişi.",
                        "4. Eşzamanlı Mitoz: Hepatositlerin, safra kanallarının ve sinüzoidal endotelin çoğalması.",
                        "5. Sonlanma (Frenleme): TGF-beta artışıyla kütle tamamlandığında hücrelerin tekrar G0 fazına dönmesi."
                    ]
                ),
                make_cloze(
                    "Karaciğer rezeksiyonu sonrası hepatositleri hücre döngüsüne sokarak kompansatuvar hiperplaziyi tetikleyen ana faktör [HGF] (Hepatosit Büyüme Faktörü)'dür.",
                    "HGF",
                    "Karaciğer büyüme faktörü kısaltması"
                )
            ]
        },

        # Adım 38
        {
            "slideNumber": 38,
            "title": "Hepatosit Büyüme Faktörü (HGF), IL-6 ve TNF-α'nın Hazırlayıcı Rolü",
            "subtitle": "Karaciğer rejenerasyonu sitokinlerin hazırlayıcı (priming) etkisi ve büyüme faktörlerinin mitojenik uyarısıyla yürütülür.",
            "badge": "Sitokin Regülasyonu",
            "badgeColor": "teal",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hepatositler normalde G0 fazında derin istirahat halindedir. Rezeksiyon sonrası mitoza girebilmeleri için önce uyarılmaya hazır hale gelmeleri (**priming**) gerekir.

Bu ön hazırlığı Kupffer hücrelerinden (karaciğer makrofajları) salgılanan **TNF-α** ve **IL-6** yürütür. Bu sitokinler NF-κB ve STAT3 transkripsiyon faktörlerini aktive ederek hepatositleri büyüme faktörlerine duyarlı kılar. Ardından mezenkimal hücrelerden salgılanan **HGF** ve **TGF-α** hepatositleri doğrudan mitoza sokar.

> [TEMEL İLKE] IL-6 ve TNF-α hücreyi kapıya (G1) getirir; HGF ve TGF-α ise kapıyı açarak hücreyi çoğalma döngüsüne (S fazı) iter.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Priming Fazı", "desc": "TNF-α ve IL-6 hepatositleri G0'dan çıkarıp büyüme faktörlerine hazır hale getirir.", "isKey": True},
                    {"title": "Mitojenik Uyarım", "desc": "HGF (c-Met reseptörü) ve TGF-α DNA replikasyonunu doğrudan başlatır.", "isKey": True},
                    {"title": "Kupffer Katkısı", "desc": "Karaciğer makrofajları rejenerasyonun vazgeçilmez orkestra şefleridir.", "isKey": False}
                ],
                "table": {
                    "title": "Karaciğer Rejenerasyonunda Temel Mediyatörler",
                    "headers": ["Mediyatör", "Üretildiği Hücre", "Temel İşlevi"],
                    "rows": [
                        ["TNF-alfa", "Kupffer hücreleri (makrofaj)", "NF-kB aktivasyonu ve hepatosit hazırlığı"],
                        ["IL-6", "Kupffer hücreleri", "STAT3 fosforilasyonu ve G1 giriş hazırlığı"],
                        ["HGF (Hepatosit Büyüme Faktörü)", "Stellat ve endotel hücreleri", "c-Met reseptör aktivasyonu ile güçlü mitoz indüksiyonu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Karaciğer rejenerasyonunda hazırlık (priming) fazını IL-6 ve TNF-alfa yönetir.",
                "📌 [SINAV SPOTU] HGF c-Met reseptörüne bağlanarak hepatositlerde DNA sentezini (mitozu) başlatan temel büyüme faktörüdür."
            ],
            "medicalTerms": [
                {"term": "HGF", "explanation": "Hepatositlerin çoğalmasını ve doku onarımını uyaran güçlü mitojenik büyüme faktörüdür."},
                {"term": "c-Met", "explanation": "HGF'nin bağlandığı ve hücre büyümesini tetikleyen reseptör tirozin kinazdır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Parsiyel hepatektomi sonrası hepatositlerin G0 fazından çıkarılarak büyüme faktörlerine duyarlı hale gelmesini (priming fazı) sağlayan temel sitokinler hangileridir?",
                    {
                        "A": "IL-6 ve TNF-alfa",
                        "B": "Histamin ve Serotonin",
                        "C": "Bradikinin ve Lökotrien D4",
                        "D": "Kalsitonin ve Parathormon",
                        "E": "Trombosit Faktör 4 ve Heparin"
                    },
                    "A",
                    {
                        "A": "Doğru: Kupffer hücrelerinden salgılanan IL-6 ve TNF-alfa priming fazının temel sitokinleridir.",
                        "B": "Yanlış: Histamin ve serotonin vazoaktif aminlerdir.",
                        "C": "Yanlış: Bradikinin ve lökotrienler vasküler permeabilite ve ağrı mediyatörleridir.",
                        "D": "Yanlış: Kalsitonin ve PTH kalsiyum regülatörleridir.",
                        "E": "Yanlış: TF4 ve heparin koagülasyon bileşenleridir."
                    }
                ),
                make_cloze(
                    "Hepatosit büyüme faktörü (HGF) hücre yüzeyindeki [c-Met] reseptörüne bağlanarak karaciğer hiperplazisini uyarır.",
                    "c-Met",
                    "HGF reseptör adı"
                )
            ]
        },

        # Adım 39 (CHECKPOINT 4)
        {
            "slideNumber": 39,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Hiperplazinin Biyolojisi ve Fizyolojik Tipleri",
            "subtitle": "Hiperplazi kavramını, hücre döngüsü bağımlılığını ve karaciğer/meme adaptasyon modellerini pekiştirin.",
            "badge": "Tekrar Sayfası",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 4,
            "synthesisNarrative": """Bu bölümde hiperplazinin tanımını, hücre bölünmesi ön koşulunu, hormon aracılı fizyolojik modelleri ve telafi edici karaciğer rejenerasyonunu inceledik.

Hiperplazi hücre sayısının mitozla artmasıdır; bölünemeyen kalıcı hücrelerde görülemez. Fizyolojik hormonal hiperplazi ergenlik/gebelikte meme bezlerinde ve proliferatif fazda endometriyumda gerçekleşir. Telafi edici hiperplazi ise parsiyel hepatektomide olduğu gibi TNF-α, IL-6 ve HGF kaskadıyla organ kütlesini tamamlar ve TGF-β ile sonlandırılır.

> [TEKRAR SPOTU] Hiperplazi fizyolojik kontrol altındadır; uyaran sonlandığında ya da organ kütlesi tamamlandığında büyüme kesin olarak durur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Mitoz Şartı", "desc": "Yalnızca labil ve stabil hücreler hiperplazi yapabilir.", "isKey": True},
                    {"title": "Hormonal Fizyolojik", "desc": "Gebelikte meme lobülleri, siklik proliferatif endometrium.", "isKey": True},
                    {"title": "Kompansatuvar Model", "desc": "Hepatektomi sonrası HGF aracılı karaciğer kütle tamamlanması.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 4 Sentez Tablosu",
                    "headers": ["Örnek", "Hiperplazi Alt Tipi", "Temel Uyaran"],
                    "rows": [
                        ["Gebelikte Meme", "Fizyolojik Hormonal", "Östrojen, Progesteron, Prolaktin"],
                        ["Siklik Endometrium", "Fizyolojik Hormonal", "Over kaynaklı östrojen"],
                        ["Parsiyel Hepatektomi", "Fizyolojik Kompansatuvar", "IL-6, TNF-alfa, HGF"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hiperplazi hücre sayısındaki artıştır; hücrelerin bölünebilir olmasını gerektirir.",
                "📌 [SINAV SPOTU] Karaciğer rejenerasyonu parsiyel hepatektomi sonrası kompansatuvar hiperplazinin kusursuz modelidir."
            ],
            "medicalTerms": [
                {"term": "Kompansatuvar Hiperplazi", "explanation": "Doku kaybı sonrası kalan hücrelerin çoğalarak organ kütlesini tamamlamasıdır."},
                {"term": "HGF", "explanation": "Hepatositlerin mitoz bölünmesini başlatan en güçlü büyüme faktörüdür."}
            ],
            "flashcards": [
                make_flashcard(
                    "k1-03-fc10",
                    "Hiperplazi ile hipertrofi arasındaki en temel hücresel fark nedir?",
                    "Hiperplazi mitoz bölünmeyle hücre sayısının artmasıdır; hipertrofi ise hücre sayısı değişmeden hücre boyutunun büyümesidir."
                ),
                make_flashcard(
                    "k1-03-fc11",
                    "Gebelikte meme dokusunda ve menstrüel siklusta endometriyumda görülen hiperplazi hangi kategoriye girer?",
                    "Hormonların uyarısıyla gerçekleşen fizyolojik hormonal hiperplazi kategorisine girer."
                ),
                make_flashcard(
                    "k1-03-fc12",
                    "Parsiyel hepatektomi sonrası karaciğer rejenerasyonunda priming (hazırlık) fazını ve mitoz fazını yöneten ana faktörler nelerdir?",
                    "Hazırlık fazını Kupffer hücrelerinden salınan TNF-alfa ve IL-6; doğrudan mitoz fazını ise HGF ve TGF-alfa yönetir."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kompansatuvar karaciğer hiperplazisi tamamlandığında hücre çoğalmasını frenleyen temel sitokin hangisidir?",
                    "Transforme edici büyüme faktörü-beta (TGF-β), organ orijinal kütlesine ulaştığında mitozu durduran ana inhibitör sitokindir."
                )
            ]
        }
    ]
