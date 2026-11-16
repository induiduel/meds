#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 1: Homeostaz, Hücresel Stres ve Adaptasyon Kavramı (Adımlar 1 - 9)
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
        # Adım 1
        {
            "slideNumber": 1,
            "title": "Homeostaz: Tanım, Dinamik Denge ve Fizyolojik Sınırlar",
            "subtitle": "Hücreler iç ve dış çevre değişimlerine rağmen kararlı bir iç denge (homeostaz) sürdürmek zorundadır.",
            "badge": "Temel Kavram",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """**Homeostaz**, hücrelerin değişen mikroçevre koşullarına rağmen iç ortam parametrelerini (iyon dengesi, pH, ozmolarite, enerji düzeyi) dar ve kararlı fizyolojik sınırlar içinde tutabilme yeteneğidir.

Normal hücre fizyolojisinde hücre boyutu, sayısı ve metabolik fonksiyonu genetik program ve ekstrasellüler sinyaller tarafından sıkı kontrol altında tutulur. Hücreler fizyolojik sınırlar içindeki dalgalanmaları bazal metabolik düzenlemelerle yönetir; ancak bu sınırları aşan yüklenmeler hücresel stres yanıtını başlatır.

> [TEMEL İLKE] Hücresel homeostaz durağan bir durum değil; enerji tüketen, sürekli denetlenen dinamik bir iç dengedir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Dinamik Denge", "desc": "İyon, su, pH ve metabolitlerin dar fizyolojik aralıklarda tutulmasıdır.", "isKey": True},
                    {"title": "Fizyolojik Sınırlar", "desc": "Her hücre tipinin genetik olarak belirlenmiş fonksiyonel ve metabolik çalışma sınırları vardır.", "isKey": True},
                    {"title": "Stres Tetiklenmesi", "desc": "Fizyolojik kapasiteyi aşan mekanik veya kimyasal uyaranlar stres kaskadını başlatır.", "isKey": False}
                ],
                "table": {
                    "title": "Hücresel Durumlar ve Karakteristikleri",
                    "headers": ["Durum", "Metabolik Düzey", "Hücresel Karşılık"],
                    "rows": [
                        ["Bazal Homeostaz", "Dengeli ATP üretimi ve tüketimi", "Normal yapı ve fonksiyonun korunması"],
                        ["Fizyolojik Stres", "Artmış iş yükü veya hormonal uyarı", "Geri dönüşümlü hücresel adaptasyon"],
                        ["Zararlı Uyaran", "Hipoksi, toksin, termal hasar", "Geri dönüşümlü veya geri dönüşümsüz hasar"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Homeostaz, değişen çevre koşullarına rağmen hücrenin iç dengesini sabit tutabilme yeteneğidir.",
                "📌 [SINAV SPOTU] Fizyolojik sınırları aşan ancak hücreyi doğrudan öldürmeyen stresler adaptasyon mekanizmalarını uyarır."
            ],
            "medicalTerms": [
                {"term": "Homeostaz", "explanation": "Hücrenin iç ortamını dar ve kararlı fizyolojik sınırlar içinde tutma yeteneğidir."},
                {"term": "Hücresel Stres", "explanation": "Hücrenin fizyolojik kapasitesini aşarak yeni bir denge kurulmasını zorunlu kılan uyarandır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Hücrenin homeostatik dengesi fizyolojik sınırların üzerinde bir stresle karşılaştığında hücrenin vereceği ilk savunma yanıtı aşağıdakilerden hangisidir?",
                    {
                        "A": "Derhal koagülasyon nekrozuna gitmek",
                        "B": "Canlılığını sürdürmek için adaptasyon geliştirmek",
                        "C": "Hücre bölünmesini tamamen sonlandırmak",
                        "D": "DNA'sını tamamen parçalayarak apoptoz başlatmak",
                        "E": "Tüm protein sentezini geri dönüşsüz durdurmak"
                    },
                    "B",
                    {
                        "A": "Yanlış: Nekroz adaptasyonun yetersiz kaldığı ağır hasar durumunda görülür.",
                        "B": "Doğru: Hücre ilk olarak yeni bir kararlı durum kurmak için adaptif yanıt geliştirir.",
                        "C": "Yanlış: Hücre bölünmesi uyarana göre artabilir (hiperplazi) veya azalabilir.",
                        "D": "Yanlış: Apoptoz geri dönüşsüz hasar fazında devreye girer.",
                        "E": "Yanlış: Adaptasyonda protein sentezi amaca yönelik olarak artar veya özelleşir."
                    }
                ),
                make_cloze(
                    "Hücrelerin iç ve dış koşullardaki değişimlere rağmen iç ortam parametrelerini kararlı sınırlarda tutmasına [homeostaz] adı verilir.",
                    "homeostaz",
                    "Kararlı iç denge ilkesi"
                )
            ]
        },

        # Adım 2
        {
            "slideNumber": 2,
            "title": "Hücresel Stres Spektrumu: Uyaran Şiddeti ve Hücresel Karşılık",
            "subtitle": "Stresin şiddeti, türü ve etki süresi hücrenin adaptasyon mu yoksa hasar yoluna mı gireceğini belirler.",
            "badge": "Patolojik Spektrum",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hücrelerin maruz kaldığı stres tek tip değildir; **uyaranın şiddeti**, **maruziyet süresi** ve **hücrenin içsel direnci** yanıtın niteliğini doğrudan belirler.

Hafif veya orta dereceli kronik stresler (hafif basınç artışı, hormonal dalgalanma) hücrede ==adaptasyon== yanıtı doğurur. Şiddetli ve ani etkenler doğrudan ==hücre hasarı== oluşturur; hasar başlangıçta geri dönüşümlü olabilirken, uyaran devam ederse geri dönüşsüz hasar ve hücre ölümü kaçınılmaz hale gelir.

> [TEMEL İLKE] Hücresel yanıt bir spektrumdur; aynı etiyolojik ajan doza ve süreye bağlı olarak adaptasyondan nekroza kadar farklı tablolara yol açabilir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hafif/Orta Stres", "desc": "Hücrenin hayatta kalmasını sağlayan morfolojik ve metabolik adaptasyonu uyarır.", "isKey": True},
                    {"title": "Şiddetli Hasar", "desc": "Hücresel adaptasyon sınırını aşarak membran ve organel hasarına neden olur.", "isKey": True},
                    {"title": "Dinamik Geçiş", "desc": "Geri dönüşümlü hasar zamanında durdurulmazsa geri dönüşsüz ölüm kaskadı başlar.", "isKey": False}
                ],
                "table": {
                    "title": "Stres Şiddeti ve Hücresel Yanıt Spektrumu",
                    "headers": ["Stres Şiddeti", "Hücresel Yanıt", "Örnek Patoloji"],
                    "rows": [
                        ["Hafif / Orta", "Adaptasyon (hipertrofi, atrofi, hiperplazi)", "Hipertansiyonda kalp hipertrofisi"],
                        ["Şiddetli / Geçici", "Geri dönüşümlü hücre hasarı", "Kısa süreli iskemiye bağlı hidropik şişme"],
                        ["Şiddetli / Kalıcı", "Geri dönüşsüz hasar ve hücre ölümü", "Miyokard enfarktüsünde koagülasyon nekrozu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hafif ve orta dereceli kronik streslerin hücresel karşılığı adaptasyondur.",
                "🚨 [KRİTİK UYARI] Kalıcı veya aşırı şiddetli zararlı uyaranlar adaptasyon safhasını atlayarak doğrudan hücre ölümüne neden olabilir."
            ],
            "medicalTerms": [
                {"term": "Zararlı Uyaran", "explanation": "Hücrenin fizyolojik adaptasyon kapasitesini aşarak yapısal bozulma başlatan etkendir."},
                {"term": "Hücre Ölümü", "explanation": "Hücrenin metabolik ve yapısal bütünlüğünü geri dönüşsüz kaybederek yok olmasıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Hücresel Stres ve Yanıt Kaskadı",
                    [
                        "1. Bazal Durum: Hücrenin homeostatik dengede yaşamını sürdürmesi.",
                        "2. Stres Karşılaşması: Artmış iş yükü veya kimyasal uyaranın belirmesi.",
                        "3. Adaptif Faz: Boyut, sayı veya fenotip değiştirerek yeni denge kurulması.",
                        "4. Hasar Fazı: Stres sınırının aşılmasıyla organel ve membran hasarı oluşumu.",
                        "5. Terminal Faz: Nekroz veya apoptoz ile hücrenin geri dönüşsüz ölümü."
                    ]
                ),
                make_active_recall(
                    "Aynı etiyolojik etken (örneğin iskemi) nasıl hem adaptasyona hem de hücre ölümüne yol açabilir?",
                    "Etkenin süresi ve şiddeti belirleyicidir: Yavaş gelişen hafif iskemi dokuda atrofi (adaptasyon) yaparken; ani ve tam tıkanma dakikalar içinde nekroz (ölüm) oluşturur."
                )
            ]
        },

        # Adım 3
        {
            "slideNumber": 3,
            "title": "Hücrenin Üç Temel Yanıtı: Adaptasyon, Geri Dönüşümlü Hasar ve Ölüm",
            "subtitle": "Homeostaz tehdit edildiğinde hücre yalnızca üç temel yoldan birini seçebilir.",
            "badge": "Temel Triad",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Bir hücre patolojik veya fizyolojik stresle karşılaştığında verebileceği yanıtlar temelde üç ana kategoride toplanır: **Adaptasyon**, **Geri Dönüşümlü Hasar** ve **Geri Dönüşsüz Hasar (Ölüm)**.

Adaptasyonda hücre hayatta kalabilmek için yeni bir kararlı durum kurar. Uyaran adaptasyon sınırını aşarsa geri dönüşümlü hasar (hücresel şişme, yağlanma) gelişir; bu evrede etken çekilirse hücre normale döner. Stres devam ederse geri dönüşsüz nokta aşılır ve hücre ==nekroz== veya ==apoptoz== ile ölür.

> [TEMEL İLKE] Adaptasyon ve geri dönüşümlü hasar, etiyolojik etken ortadan kalktığında hücrenin başlangıç durumuna dönebildiği dinamik süreçlerdir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Adaptasyon", "desc": "Yeni bir kararlı denge kurularak hücre canlılığının ve fonksiyonunun sürdürülmesidir.", "isKey": True},
                    {"title": "Geri Dönüşümlü Hasar", "desc": "Membran ve organellerde geçici hasar oluşması; uyaran kesilince tam iyileşme mümkündür.", "isKey": True},
                    {"title": "Geri Dönüşsüz Ölüm", "desc": "ATP tükenmesi ve membran bütünlüğü kaybıyla sonuçlanan kaçınılmaz nekroz veya apoptozdur.", "isKey": False}
                ],
                "table": {
                    "title": "Hücrenin Üç Temel Yanıtının Karşılaştırması",
                    "headers": ["Özellik", "Adaptasyon", "Geri Dönüşümlü Hasar", "Geri Dönüşsüz Ölüm"],
                    "rows": [
                        ["Canlılık", "Canlı ve işlevsel", "Canlı, fonksiyon bozuk", "Canlılık tamamen kayıp"],
                        ["Geri Dönüş", "Tamamen geri döner", "Uyaran kalkınca geri döner", "Geri dönüş imkansız"],
                        ["Temel Morfoloji", "Boyut/sayı değişimi", "Bulanık şişme, yağlanma", "Nükleer piknoz, lizis, fragmantasyon"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücre stresine verilen üç temel yanıt: Adaptasyon, geri dönüşümlü hasar ve geri dönüşsüz hasardır.",
                "📌 [SINAV SPOTU] Adaptasyon ve erken hasar evresi geri dönüşümlüdür; nekroz ve apoptoz geri dönüşsüzdür."
            ],
            "medicalTerms": [
                {"term": "Geri Dönüşümlü Hasar", "explanation": "Zararlı etken kalktığında hücrenin morfolojik ve fonksiyonel olarak normale dönebildiği hasardır."},
                {"term": "Nekroz", "explanation": "Membran bütünlüğü kaybı ve enzim sindirimiyle karakterize patolojik hücre ölümüdür."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Geri Dönüşümlü Hasar ve Geri Dönüşsüz Hasar Ayrımı",
                    "Geri Dönüşümlü Hasar",
                    "Geri Dönüşsüz Hasar (Ölüm)",
                    [
                        "Hücresel şişme ve kabarcıklaşma",
                        "Plazma membranı sağlam kalır",
                        "Uyaran kesilince tam düzelme"
                    ],
                    [
                        "Plazma membranında yaygın rüptür",
                        "Yoğun kalsiyum girişi ve nükleer lizis",
                        "Enzim kaybı ve inflamatuvar yıkım"
                    ]
                ),
                make_cloze(
                    "Hücrenin zararlı etken ortadan kalktığında eski normal yapısına dönebildiği hasar türüne [geri dönüşümlü] hasar adı verilir.",
                    "geri dönüşümlü",
                    "Eski duruma gelebilme niteliği"
                )
            ]
        },

        # Adım 4
        {
            "slideNumber": 4,
            "title": "Adaptasyonun Tanımı: Geri Dönüşümlü Yapısal ve Fonksiyonel Uyum",
            "subtitle": "Adaptasyon, hücrenin stres karşısında canlılığını korumak amacıyla geliştirdiği morfolojik ve metabolik düzenlemelerdir.",
            "badge": "Tanısal İlke",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """**Hücresel adaptasyon**, hücrelerin sayı, boyut, fenotip, metabolik aktivite veya işlevlerini ==geri dönüşümlü biçimde== değiştirerek yeni bir kararlı duruma ulaşmasıdır.

Adaptasyonun nihai biyolojik hedefi, aşırı yük veya olumsuz çevre koşullarına rağmen hücrenin canlılığını ve temel görevlerini sürdürmesini sağlamaktır. Uyaran ortadan kalktığında doku yeniden orijinal mimari ve fizyolojik durumuna geri döner.

> [TEMEL İLKE] Adaptasyon kalıcı bir dönüşüm değil; uyaran varlığı boyunca sürdürülen dinamik ve geri dönüşümlü bir korunma kalkanıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Geri Dönüşümlülük", "desc": "Adaptasyon uyaran varlığında sürer, uyaran ortadan kalkınca doku normale döner.", "isKey": True},
                    {"title": "Canlılık Hedefi", "desc": "Hücrenin parçalanmasını önleyerek organizmanın fonksiyonel devamlılığını sağlar.", "isKey": True},
                    {"title": "Çok Boyutlu Uyum", "desc": "Yalnızca boyut değil; sayı, fenotip ve metabolik hız da adapte olur.", "isKey": False}
                ],
                "table": {
                    "title": "Adaptasyonun Temel Boyutları",
                    "headers": ["Uyum Düzlemi", "Biyolojik Mekanizma", "Adaptasyon Tipi"],
                    "rows": [
                        ["Hücre Boyutu", "Protein sentezi artışı veya yıkımı", "Hipertrofi veya Atrofi"],
                        ["Hücre Sayısı", "Kök hücre aktivasyonu ve mitoz", "Hiperplazi"],
                        ["Hücre Fenotipi", "Farklılaşma yolaklarının değişimi", "Metaplazi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Adaptasyonun en temel özelliği GERİ DÖNÜŞÜMLÜ (reversible) bir süreç olmasıdır.",
                "🚨 [KRİTİK UYARI] Adaptasyon sağlayan hücre hayatta kalır ancak bazı özelleşmiş normal fonksiyonlarında kısıtlanma yaşayabilir."
            ],
            "medicalTerms": [
                {"term": "Reversibilite", "explanation": "Patolojik veya adaptif bir sürecin uyaran sonlandığında kendiliğinden normale dönebilmesidir."},
                {"term": "Fenotip Değişimi", "explanation": "Hücrenin morfolojik ve fonksiyonel görünümünün stres koşullarına göre farklılaşmasıdır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Hücresel adaptasyon kavramı ile ilgili aşağıdaki ifadelerden hangisi biyolojik olarak doğrudur?",
                    {
                        "A": "Adaptasyon geliştiren hücreler bir daha asla normal boyutuna dönemez",
                        "B": "Adaptasyon, hücrenin stres altında canlılığını sürdürmesini sağlayan geri dönüşümlü bir yanıttır",
                        "C": "Adaptasyon süreci her zaman dokuda kontrolsüz malign neoplazi ile sonuçlanır",
                        "D": "Adaptasyon yalnızca hücrelerin kontrolsüz apoptoza gitmesiyle gerçekleşir",
                        "E": "Adaptasyonda gen ekspresyonu ve protein sentezi tamamen durur"
                    },
                    "B",
                    {
                        "A": "Yanlış: Uyaran kesildiğinde hücre eski normal durumuna geri döner.",
                        "B": "Doğru: Adaptasyon canlılığı koruyan geri dönüşümlü morfolojik ve fonksiyonel uyumdur.",
                        "C": "Yanlış: Çoğu adaptasyon fizyolojik veya benign sınırlarda seyreder.",
                        "D": "Yanlış: Apoptoz adaptasyon değil, programlı hücre ölümüdür.",
                        "E": "Yanlış: Adaptasyon aktif gen regülasyonu ve seçici protein sentezi gerektirir."
                    }
                ),
                make_cloze(
                    "Hücresel adaptasyonun en belirleyici biyolojik özelliği uyaran kesildiğinde sürecin [geri dönüşümlü] olmasıdır.",
                    "geri dönüşümlü",
                    "Tersine çevrilebilir olma durumu"
                )
            ]
        },

        # Adım 5
        {
            "slideNumber": 5,
            "title": "Yeni Bir Kararlı Durum (Steady State) Oluşturma Mantığı",
            "subtitle": "Hücre aşırı yüke karşı iç dengesini yeniden kalibre ederek fonksiyonel bir denge kurar.",
            "badge": "Fizyopatolojik Mantık",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Adaptasyonun merkezinde ==yeni bir kararlı durum (steady state)== inşa etme prensibi yatar. Normal bir hücre mevcut iş yükünü bazal kapasitesiyle karşılayamadığında, strese yenik düşüp ölmek yerine yapısını ve metabolizmasını yeniden organize eder.

Örneğin, artmış kan basıncına karşı kalp kası hücresi daha fazla kasılma proteini üreterek kalınlaşır; böylece artan duvar gerilimini karşılayacak yeni bir mekanik denge kurulur. Bu yeni dengede hücre hayattadır ve işini sürdürür; ancak rezerv kapasitesi daralmıştır.

> [TEMEL İLKE] Yeni kararlı durum hücreyi o anki tehlikeden kurtarır; fakat stresin sürekli artması bu kırılgan dengeyi bozarak dekompansasyona yol açar.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Denge Kalibrasyonu", "desc": "Hücre morfolojisini artan yüke göre yeniden şekillendirir.", "isKey": True},
                    {"title": "Fonksiyonel Devamlılık", "desc": "Yeni dengede hücre hasara uğramadan çalışmaya devam eder.", "isKey": True},
                    {"title": "Rezerv Daralması", "desc": "Adapte olmuş hücrenin ek stresleri tolere etme kapasitesi azalmıştır.", "isKey": False}
                ],
                "table": {
                    "title": "Normal Durum vs Yeni Kararlı Durum",
                    "headers": ["Ölçüt", "Normal Kararlı Durum", "Adapte Kararlı Durum"],
                    "rows": [
                        ["Enerji Tüketimi", "Bazal metabolik düzeyde", "Artmış veya koruyucu baskılanmış düzeyde"],
                        ["Hücre Kütlesi", "Standart fizyolojik boyut", "Artmış (hipertrofi) veya azalmış (atrofi)"],
                        ["Stres Toleransı", "Geniş güvenlik marjı", "Daralmış ek yük toleransı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Adaptasyonun amacı hücrenin stresli ortamda yeni bir kararlı durum (steady state) oluşturmasıdır.",
                "🚨 [KRİTİK UYARI] Yeni kararlı durum kurulamazsa hücre geri dönüşümlü veya geri dönüşsüz hasar evresine kayar."
            ],
            "medicalTerms": [
                {"term": "Kararlı Durum", "explanation": "Hücrenin metabolik girdi ve çıktılarını dengede tutarak canlılığını sürdürdüğü durumdur."},
                {"term": "Dekompansasyon", "explanation": "Adaptif kapasitenin yetersiz kalarak fonksiyonel çöküş ve hasarın başlamasıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Yeni Kararlı Durum Kurulumu Basamakları",
                    [
                        "1. Aşırı Yük: Hücrenin bazal kapasitesini aşan sürekli stres maruziyeti.",
                        "2. Sensör Aktivasyonu: Mekanik gerilim veya kimyasal reseptörlerin uyarılması.",
                        "3. Gen Programlaması: Yapısal protein sentezinin veya lizozom aktivitesinin modülasyonu.",
                        "4. Morfolojik Dönüşüm: Boyut veya fenotip değiştirerek yeni dengenin kurulması.",
                        "5. Sürdürülebilirlik: Stres sürdüğü müddetçe hücrenin canlılığını devam ettirmesi."
                    ]
                ),
                make_active_recall(
                    "Adapte olmuş bir hücre neden normal bir hücreye göre ek streslere karşı daha kırılgandır?",
                    "Çünkü adaptasyon sırasında hücre fonksiyonel ve metabolik rezervlerinin büyük kısmını tüketmiş, sınırlarına yaklaşmıştır."
                )
            ]
        },

        # Adım 6
        {
            "slideNumber": 6,
            "title": "Fizyolojik vs Patolojik Adaptasyon: Temel Ayırıcı Ölçütler",
            "subtitle": "Adaptasyon normal fizyolojik hormon ve iş yüküyle gelişebileceği gibi, hastalık süreçlerine ikincil olarak da ortaya çıkabilir.",
            "badge": "Ayırıcı Tanım",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Adaptasyon süreçleri tetikleyen uyarana ve amaca göre iki ana kategoriye ayrılır: **Fizyolojik Adaptasyon** ve **Patolojik Adaptasyon**.

==Fizyolojik adaptasyon==, normal hormonların veya endojen mediyatörlerin uyarısına verilen doğal yanıttır (örneğin gebelikte uterusun büyümesi veya laktasyonda meme bezlerinin gelişimi). ==Patolojik adaptasyon== ise hastalığı başlatan stres faktörlerine karşı hücrenin hayatta kalabilmek için verdiği yapısal yanıttır (örneğin hipertansiyonda kalp hipertrofisi veya sigara dumanına bağlı bronş metaplazisi).

> [TEMEL İLKE] Fizyolojik adaptasyon vücudun doğal biyolojik gereksinimlerini karşılarken; patolojik adaptasyon dokuyu hasardan korumaya çalışan savunma yanıtıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Fizyolojik Uyarım", "desc": "Normal büyüme faktörleri, hormonlar ve doğal iş yükü artışıyla tetiklenir.", "isKey": True},
                    {"title": "Patolojik Uyarım", "desc": "Hastalık süreçleri, kronik tahriş veya anormal vasküler yüklerle tetiklenir.", "isKey": True},
                    {"title": "Geri Dönüş Niteliği", "desc": "Her iki form da etken ortadan kalktığında geri dönebilme potansiyeli taşır.", "isKey": False}
                ],
                "table": {
                    "title": "Fizyolojik ve Patolojik Adaptasyon Karşılaştırması",
                    "headers": ["Özellik", "Fizyolojik Adaptasyon", "Patolojik Adaptasyon"],
                    "rows": [
                        ["Uyaran Niteliği", "Normal hormon veya iş yükü", "Hastalık yaratan aşırı stres"],
                        ["Biyolojik Amaç", "Doğal yaşam evresine uyum", "Hücreyi ölümden kurtarma"],
                        ["Klasik Örnek", "Gebelikte uterus hipertrofisi", "Aort stenozunda sol ventrikül hipertrofisi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Gebelik uterusu fizyolojik adaptasyona, hipertansif miyokard patolojik adaptasyona klasik örnektir.",
                "🚨 [KRİTİK UYARI] Patolojik adaptasyon hücreyi korur ancak uzun vadede altta yatan hastalık tedavi edilmezse organ yetmezliğine zemin hazırlar."
            ],
            "medicalTerms": [
                {"term": "Fizyolojik Adaptasyon", "explanation": "Doğal hormonal veya iş yükü uyaranlarına karşı gelişen normal hücresel yanıttır."},
                {"term": "Patolojik Adaptasyon", "explanation": "Hastalık yapıcı stres faktörlerine karşı hücrenin geliştirdiği savunma yanıtıdır."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Fizyolojik ve Patolojik Adaptasyon Eşleştirmesi",
                    ["Klinik Durum", "Adaptasyon Niteliği", "Doğru Sınıflama"],
                    [
                        [
                            ("Gebelikte miyometriyumun büyümesi", False),
                            ("Östrojen uyarımıyla doğal yanıt", True, "Doğal biyolojik süreç"),
                            ("Fizyolojik adaptasyon", False)
                        ],
                        [
                            ("Hipertansiyonda sol ventrikül kalınlaşması", False),
                            ("Aşırı basınca karşı patolojik yanıt", True, "Hastalığa ikincil yanıt"),
                            ("Patolojik adaptasyon", False)
                        ],
                        [
                            ("Ağırlık çalışan sporcuda pazı kası gelişimi", False),
                            ("İş yüküne fizyolojik uyum", True, "Egzersiz uyarımı"),
                            ("Fizyolojik adaptasyon", False)
                        ]
                    ]
                ),
                make_active_recall(
                    "Fizyolojik adaptasyon ile patolojik adaptasyon arasındaki temel ayrım noktası nedir?",
                    "Fizyolojik adaptasyon normal hormonal ve fiziksel uyaranlara verilen doğal yanıttır; patolojik adaptasyon ise hastalık oluşturan zararlı streslere karşı hayatta kalma yanıtıdır."
                )
            ]
        },

        # Adım 7
        {
            "slideNumber": 7,
            "title": "Dört Ana Adaptasyon Tipine Kuşbakışı: Boyut, Sayı, Fenotip ve Kütle",
            "subtitle": "Hücresel adaptasyon morfolojik olarak dört temel başlık altında incelenir.",
            "badge": "Sınıflama",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hücresel adaptasyonlar hücrenin verdiği morfolojik yanıt biçimine göre dört klasik tipe ayrılır: **Hipertrofi**, **Hiperplazi**, **Atrofi** ve **Metaplazi**.

==Hipertrofi== hücre boyutunda artıştır; bölünme yeteneği olmayan hücrelerde (kalp, iskelet kası) temel yanıttır. ==Hiperplazi== hücre sayısındaki artıştır ve bölünebilen dokularda görülür. ==Atrofi== hücre boyutu ve kütlesindeki azalmadır. ==Metaplazi== ise bir erişkin hücre tipinin strese daha dayanıklı başka bir hücre tipine dönüşmesidir.

> [TEMEL İLKE] Doku tipi adaptasyon şeklini belirler: Bölünemeyen hücreler yalnızca hipertrofi yapabilirken, bölünebilen hücreler hipertrofi ve hiperplaziyi birlikte kullanır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hipertrofi (Boyut)", "desc": "Hücre sayısı değişmeksizin hücre hacminin büyümesidir.", "isKey": True},
                    {"title": "Hiperplazi (Sayı)", "desc": "Mitoz yoluyla hücre sayısının çoğalmasıdır.", "isKey": True},
                    {"title": "Atrofi & Metaplazi", "desc": "Atrofi kütle kaybı, metaplazi ise hücre fenotipinin değişimidir.", "isKey": False}
                ],
                "table": {
                    "title": "Dört Temel Adaptasyon Tipinin Özeti",
                    "headers": ["Adaptasyon Tipi", "Hücresel Değişiklik", "Temel Dokusal Kısıt"],
                    "rows": [
                        ["Hipertrofi", "Hücre boyutunda artış", "Bölünemeyen kalıcı dokularda tek yoldur"],
                        ["Hiperplazi", "Hücre sayısında artış", "Hücrelerin mitoz yapabilmesi şarttır"],
                        ["Atrofi", "Hücre hacmi ve sayısında azalma", "Tüm dokularda enerji tasarrufu sağlar"],
                        ["Metaplazi", "Hücre tipinin değişmesi", "Kök hücrelerin yeniden programlanmasıdır"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hipertrofi hücre boyutu artışı, hiperplazi hücre sayısı artışıdır.",
                "📌 [SINAV SPOTU] Kalp ve iskelet kası bölünemez; bu nedenle iş yükü artışına yalnızca hipertrofi ile yanıt verir."
            ],
            "medicalTerms": [
                {"term": "Hipertrofi", "explanation": "Hücre içi yapısal protein ve organel artışıyla hücre boyutunun büyümesidir."},
                {"term": "Hiperplazi", "explanation": "Kök veya öncül hücrelerin bölünmesiyle dokudaki hücre sayısının artmasıdır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Bölünme yeteneği olmayan kalıcı hücrelerden oluşan miyokard dokusunun artmış basınca karşı verebileceği temel adaptasyon biçimi hangisidir?",
                    {
                        "A": "Hiperplazi",
                        "B": "Hipertrofi",
                        "C": "Skuamöz metaplazi",
                        "D": "Kazeifikasyon",
                        "E": "Displazi"
                    },
                    "B",
                    {
                        "A": "Yanlış: Kalp kası hücreleri bölünemediği için hiperplazi yapamaz.",
                        "B": "Doğru: Kalıcı hücreler iş yükü artışına sadece hücre boyutunu büyüterek (hipertrofi) yanıt verir.",
                        "C": "Yanlış: Metaplazi epitel ve mezenkimde görülür, kalp kasında görülmez.",
                        "D": "Yanlış: Kazeifikasyon tüberküloz nekrozudur, adaptasyon değildir.",
                        "E": "Yanlış: Displazi neoplastik öncülü atipik gelişimdir."
                    }
                ),
                make_cloze(
                    "Hücrelerin bölünme kapasitesinin olmadığı kalıcı dokularda organ büyümesi yalnızca hücre [boyutunda] artışla sağlanır.",
                    "boyutunda",
                    "Hacimsel büyüme parametresi"
                )
            ]
        },

        # Adım 8
        {
            "slideNumber": 8,
            "title": "Hücresel Rezerv ve Stres Yanıtında Organ Farklılıkları",
            "subtitle": "Her organın anatomik yapısı ve hücresel çoğalma kapasitesi adaptasyon biçimini belirler.",
            "badge": "Doku Farklılıkları",
            "badgeColor": "indigo",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Vücuttaki dokular proliferasyon kapasitelerine göre **labil** (sürekli bölünen), **stabil** (uyaranla bölünen) ve **kalıcı** (bölünmeyen) dokular olarak üç grupta incelenir. Bu özellik hangi adaptasyonun devreye gireceğini doğrudan tayin eder.

Kemik iliği ve gastrointestinal epitel gibi labil dokular stres altında hızla ==hiperplazi== geliştirir. Karaciğer gibi stabil dokular rezeksiyon sonrası kompansatuvar hiperplaziye gider. Buna karşılık kalp ve çizgili kas gibi kalıcı dokular hücrelerini çoğaltamadığından yalnızca ==hipertrofi== geliştirebilir.

> [TEMEL İLKE] Bir organın adaptasyon stratejisi, hücrelerinin hücre döngüsüne (mitoz) girip girememesine kesin olarak bağımlıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Labil Dokular", "desc": "Sürekli bölünen epitel hücreleri; temel yanıt hiperplazidir.", "isKey": True},
                    {"title": "Stabil Dokular", "desc": "Gerektiğinde G0 evresinden mitoza dönen karaciğer ve böbrek parankimidir.", "isKey": True},
                    {"title": "Kalıcı Dokular", "desc": "Mitoz yeteneğini kaybetmiş kalp kası ve nöronlar; hiperplazi yapamaz.", "isKey": False}
                ],
                "table": {
                    "title": "Doku Çoğalma Kapasitesi ve Adaptasyon Şekli",
                    "headers": ["Doku Grubu", "Hücre Döngüsü Durumu", "Olası Adaptasyon Yanıtı"],
                    "rows": [
                        ["Labil Doku", "Sürekli hücre döngüsünde (kripta, epidermis)", "Yoğun hiperplazi"],
                        ["Stabil Doku", "G0 fazında istirahatte (hepatosit)", "Hipertrofi ve hiperplazi birlikte"],
                        ["Kalıcı Doku", "Döngüyü kalıcı terk etmiş (kardiyomiyosit)", "Yalnızca hipertrofi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kalıcı hücreler (kalp kası, nöron) hiperplazi yapamaz, sadece hipertrofi geliştirir.",
                "📌 [SINAV SPOTU] Karaciğer stabil dokudur; parsiyel hepatektomi sonrası telafi edici hiperplazi ile kütlesini tamamlar."
            ],
            "medicalTerms": [
                {"term": "Labil Doku", "explanation": "Kök hücreler sayesinde yaşam boyu sürekli bölünen ve yenilenen dokudur."},
                {"term": "Kalıcı Doku", "explanation": "Doğum sonrası çoğalma yeteneğini tamamen kaybetmiş olan dokudur."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Miyokard enfarktüsü geçirmiş bir hastada kaybedilen kalp kası alanının yenilenmesi senaryosu.",
                    [
                        {
                            "text": "Kardiyomiyositler hızla bölünerek nekrotik alanı yeni kas hücreleriyle doldurur.",
                            "isCorrect": False,
                            "feedback": "Hatalı! Kardiyomiyositler kalıcı hücrelerdir, mitozla çoğalıp defekti kapatamazlar."
                        },
                        {
                            "text": "Ölen kas hücreleri bölünemez; defekt bağ dokusu (skar) ile onarılırken kalan sağlam miyositler hipertrofiye uğrar.",
                            "isCorrect": True,
                            "feedback": "Doğru patolojik mekanizma! Kalıcı doku hasarı skarlaşır, kalan parankim hipertrofi ile yükü karşılar."
                        },
                        {
                            "text": "Kalp kası metaplazi geliştirerek kıkırdağa dönüşür.",
                            "isCorrect": False,
                            "feedback": "Yanlış! İskemik hasar metaplazi değil fibröz skar ile sonuçlanır."
                        }
                    ]
                ),
                make_cloze(
                    "Kardiyak miyositler hücre döngüsünü kalıcı olarak terk ettiklerinden aşırı yüke karşı [hiperplazi] geliştiremezler.",
                    "hiperplazi",
                    "Hücre sayısı artışı süreci"
                )
            ]
        },

        # Adım 9 (CHECKPOINT 1)
        {
            "slideNumber": 9,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Homeostaz ve Adaptasyon İlkeleri",
            "subtitle": "Homeostazın dinamik dengesini, hücresel stres spektrumunu ve temel adaptasyon ilkelerini pekiştirin.",
            "badge": "Tekrar Sayfası",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 1,
            "synthesisNarrative": """Bu bölümde hücrenin homeostatik iç dengesini, stres karşısında verdiği üç temel yanıtı ve adaptasyonun biyolojik temellerini inceledik.

Adaptasyon, hücrelerin canlılığını korumak amacıyla geri dönüşümlü olarak boyut, sayı veya fenotip değiştirmesidir. Bölünemeyen kalıcı dokular hipertrofiye başvururken, bölünebilen dokular hiperplazi geliştirebilir. Adaptasyon başarılı olduğunda yeni bir kararlı durum kurulur; stres aşırı şiddetli veya kalıcı olursa hasar ve hücre ölümü kaçınılmaz hale gelir.

> [TEKRAR SPOTU] Geri dönüşümlülük adaptasyonun altın kuralıdır; uyaran ortadan kalktığında doku fizyolojik başlangıç durumuna geri döner.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Üç Temel Yanıt", "desc": "Adaptasyon, geri dönüşümlü hasar ve geri dönüşsüz hücre ölümü.", "isKey": True},
                    {"title": "Dört Adaptasyon", "desc": "Hipertrofi (boyut), hiperplazi (sayı), atrofi (küçülme), metaplazi (dönüşüm).", "isKey": True},
                    {"title": "Doku Kısıtı", "desc": "Kalıcı dokularda yalnızca hipertrofi, bölünebilen dokularda hiperplazi ve hipertrofi birlikte görülür.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 1 Sentez Tablosu",
                    "headers": ["Kavram", "Tanımlayıcı Mekanizma", "Kritik Klinik İlke"],
                    "rows": [
                        ["Homeostaz", "Dinamik iç denge", "Bozulması stres yanıtını başlatır"],
                        ["Adaptasyon", "Geri dönüşümlü yapısal uyum", "Canlılığı korumak için yeni kararlı durum kurar"],
                        ["Hasar/Ölüm", "Sınırın aşılmasıyla yıkım", "Kalıcı şiddetli stres nekroz veya apoptoz yapar"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Adaptasyon hücre canlılığını korumak için geliştirilen geri dönüşümlü yeni bir kararlı durumdur.",
                "📌 [SINAV SPOTU] Kalp kası bölünemeyen kalıcı hücrelerden oluştuğu için yük artışına yalnızca hipertrofi ile yanıt verir."
            ],
            "medicalTerms": [
                {"term": "Hücresel Adaptasyon", "explanation": "Hücrenin stres karşısında canlılığını korumak amacıyla geliştirdiği geri dönüşümlü yanıttır."},
                {"term": "Kararlı Durum", "explanation": "Hücrenin metabolik girdi ve çıktılarını yeni yük koşullarında dengede tutmasıdır."}
            ],
            "flashcards": [
                make_flashcard(
                    "k1-03-fc01",
                    "Hücrenin homeostatik dengesini tehdit eden bir strese verebileceği üç temel yanıt nedir?",
                    "Adaptasyon, geri dönüşümlü hasar ve geri dönüşsüz hasar (hücre ölümü)."
                ),
                make_flashcard(
                    "k1-03-fc02",
                    "Kalıcı dokular (kalp ve iskelet kası) neden iş yükü artışına hiperplazi ile yanıt veremez?",
                    "Çünkü kardiyomiyositler ve çizgili kas lifleri hücre döngüsünü kalıcı olarak terk etmiştir, mitoz bölünme yapamazlar."
                ),
                make_flashcard(
                    "k1-03-fc03",
                    "Fizyolojik adaptasyon ile patolojik adaptasyon arasındaki temel ayırıcı fark nedir?",
                    "Fizyolojik adaptasyon normal hormonal veya fiziksel uyaranlara verilen doğal yanıttır; patolojik adaptasyon ise hastalık yapıcı streslere karşı geliştirilen savunma yanıtıdır."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Adaptasyon sürecinin 'geri dönüşümlü' (reversible) olması klinik açıdan ne anlama gelir?",
                    "Hastalığı başlatan etiyolojik etken (örneğin hipertansiyon veya sigara) tedavi edilip ortadan kaldırıldığında dokunun eski normal yapısına ve boyutuna dönebilmesini ifade eder."
                )
            ]
        }
    ]
