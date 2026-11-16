#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 5: Patolojik Hiperplazi, Hormonal Dengesizlik ve Kanser Riski (Adımlar 40 - 49)
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
        # Adım 40
        {
            "slideNumber": 40,
            "title": "Patolojik Hiperplazi Tanımı: Aşırı Hormon ve Büyüme Faktörü Uyarımı",
            "subtitle": "Aşırı veya uygunsuz hormon ve büyüme faktörü uyarımı hücrelerin anormal çoğalmasına yol açar.",
            "badge": "Patolojik Uyarım",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """**Patolojik hiperplazi**, dokuların aşırı, uygunsuz veya dengesiz hormonal uyarıya ya da kontrolsüz büyüme faktörü salgısına maruz kalması sonucu hücrelerin anormal biçimde çoğalmasıdır.

Fizyolojik hiperplaziden farkı, uyarının doğal bir biyolojik amaca hizmet etmemesi ve doku dengesini bozmasıdır. Ancak patolojik hiperplazide hücreler kanserleşmiş değildir; hücre çoğalması halen dış uyarana bağımlıdır. Hormonal veya kimyasal uyaran kesildiğinde hiperplazi gerileyebilme yeteneğini korur.

> [TEMEL İLKE] Patolojik hiperplazi uyarana bağımlı bir adaptasyondur; uyaran kesildiğinde geriler ancak neoplaziye zemin hazırlayabilir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Anormal Uyarım", "desc": "Aşırı hormon (östrojen, androjen) veya kronik büyüme faktörü fazlalığı.", "isKey": True},
                    {"title": "Uyarana Bağımlılık", "desc": "Neoplaziden farklı olarak uyaran kesildiğinde çoğalma durur ve geriler.", "isKey": True},
                    {"title": "Kanser Riski", "desc": "Uzamış ve kontrolsüz hiperplazi genetik mutasyon birikimine uygun zemin oluşturur.", "isKey": False}
                ],
                "table": {
                    "title": "Fizyolojik vs Patolojik Hiperplazi",
                    "headers": ["Özellik", "Fizyolojik Hiperplazi", "Patolojik Hiperplazi"],
                    "rows": [
                        ["Uyaran Niteliği", "Dengeli, siklik veya doğal hormon", "Aşırı, karşılanmamış, sürekli hormon"],
                        ["Dokusal Sonuç", "İşlevsel hazırlık (ör. laktasyon)", "Doku disfonksiyonu, anormal kanama, tıkanıklık"],
                        ["Kanserleşme Riski", "Yok veya bazal düzeyde", "Uzun vadede belirgin artış riski"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patolojik hiperplazilerin büyük çoğunluğu aşırı hormon veya büyüme faktörü uyarımına bağlıdır.",
                "🚨 [KRİTİK UYARI] Patolojik hiperplazi kanser değildir ancak bazı tipleri kanser gelişimine çok elverişli zemin hazırlar."
            ],
            "medicalTerms": [
                {"term": "Patolojik Hiperplazi", "explanation": "Aşırı hormon veya büyüme faktörüyle tetiklenen anormal hücre sayısı artışıdır."},
                {"term": "Karşılanmamış Östrojen", "explanation": "Progesteron dengesi olmaksızın endometriyumu tek başına uyaran sürekli östrojendir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Patolojik hiperplaziyi malign neoplaziden (kanserden) ayıran en temel biyolojik özellik hangisidir?",
                    {
                        "A": "Patolojik hiperplazide hücre çoğalmasının uyarana bağımlı olması ve uyaran kesilince durması",
                        "B": "Patolojik hiperplazide hücrelerin mitoz bölünme yapamaması",
                        "C": "Patolojik hiperplazinin yalnızca bölünemeyen kalıcı dokularda görülmesi",
                        "D": "Patolojik hiperplazide hücre zarının tamamen parçalanmış olması",
                        "E": "Patolojik hiperplazinin daima uzak metastaz yapması"
                    },
                    "A",
                    {
                        "A": "Doğru: Hiperplazi uyarana bağımlıdır ve uyaran kalkınca geriler; kanser ise otonomdur.",
                        "B": "Yanlış: Hiperplazi mitozla çoğalma sürecidir.",
                        "C": "Yanlış: Kalıcı dokularda hiperplazi görülmez.",
                        "D": "Yanlış: Membran sağlamdır, nekroz değildir.",
                        "E": "Yanlış: Hiperplazi benign bir süreçtir, asla metastaz yapmaz."
                    }
                ),
                make_cloze(
                    "Patolojik hiperplazide hücre çoğalması dış uyarana bağımlıdır; bu nedenle anormal uyaran kesildiğinde lezyon [geriler].",
                    "geriler",
                    "Eskiye dönme eylemi"
                )
            ]
        },

        # Adım 41
        {
            "slideNumber": 41,
            "title": "Endometriyal Hiperplazi: Östrojen / Progesteron Dengesizliği",
            "subtitle": "Progesteron ile dengelenmeyen aşırı östrojen uyarımı endometriyal bezlerin anormal çoğalmasını tetikler.",
            "badge": "Jinekolojik Patoloji",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patolojik hiperplazinin en tipik klinik örneği **endometriyal hiperplazidir**. Normal menstrüel döngüde östrojenin proliferatif etkisi ovülasyon sonrası progesteron ile dengelenir ve durdurulur.

Ancak anovülatuar sikluslarda, polikistik over sendromunda (PKOS), östrojen üreten over tümörlerinde veya dışarıdan karşılanmamış östrojen tedavisinde progesteron salgılanamaz. Sürekli östrojen bombardımanı altındaki endometriyal bezler aşırı çoğalarak kalınlaşır ve klinik olarak **anormal uterin kanamalara** yol açar.

> [KLİNİK İPUCU] Karşılanmamış (unomposed) östrojen uyarımı endometriyal hiperplazinin bir numaralı etiyolojik nedenidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hormon Dengesizliği", "desc": "Östrojenin proliferatif etkisi progesteron tarafından dengelenemez.", "isKey": True},
                    {"title": "Klinik Tablo", "desc": "Düzensiz, aşırı ve uzamış menstrüel veya postmenopozal kanamalar.", "isKey": True},
                    {"title": "Risk Faktörleri", "desc": "Anovülasyon, PKOS, obezite (periferik aromataz) ve hormon replasmanı.", "isKey": False}
                ],
                "table": {
                    "title": "Endometriyal Hiperplazi Etiyolojisi",
                    "headers": ["Klinik Durum", "Biyokimyasal Mekanizma", "Endometriyal Etki"],
                    "rows": [
                        ["Anovülatuar Siklus", "Korpus luteum oluşmaz, progesteron yok", "Sürekli tek başına östrojen uyarımı"],
                        ["Obezite", "Yağ dokusunda androstenedion -> estron dönüşümü", "Artmış periferik östrojen düzeyi"],
                        ["Granüloza Hücreli Tümör", "Over tümörünün aşırı östrojen salgılaması", "Şiddetli kistik ve atipili hiperplazi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Endometriyal hiperplazi karşılanmamış östrojen uyarımı sonucu gelişir.",
                "📌 [SINAV SPOTU] Obezite, yağ dokusundaki aromataz enzimiyle androjenleri östrojene çevirerek endometriyal hiperplazi riskini artırır."
            ],
            "medicalTerms": [
                {"term": "Anovülasyon", "explanation": "Yumurtlama olmaması nedeniyle korpus luteumun ve progesteronun oluşmadığı tablodur."},
                {"term": "Aromataz", "explanation": "Yağ dokusunda adrenal androjenleri östrojen hormonuna dönüştüren enzimdir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Obezite ve Karşılanmamış Östrojen Kaskadı",
                    [
                        "1. Adipoz Doku Artışı: Yağ dokusundaki aromataz enzim miktarının yükselmesi.",
                        "2. Periferik Dönüşüm: Androjenlerin aşırı miktarda estrona (östrojene) çevrilmesi.",
                        "3. Progesteron Eksikliği: Anovülasyon nedeniyle östrojenin dengelenememesi.",
                        "4. Endometriyal Uyarım: Bez epitel hücrelerinde sürekli ve aşırı mitoz indüksiyonu.",
                        "5. Hiperplazi ve Kanama: Düzensiz kalınlaşan endometriyumun dökülmesi ve kanama."
                    ]
                ),
                make_cloze(
                    "Endometriyal hiperplazide östrojenin mitojenik etkisini frenleyemeyen eksik hormon [progesteron] hormonudur.",
                    "progesteron",
                    "Luteal faz dengeleyici hormonu"
                )
            ]
        },

        # Adım 42
        {
            "slideNumber": 42,
            "title": "Endometriyal Hiperplazi Sınıflaması: Basit, Kompleks ve Atipili",
            "subtitle": "Histopatolojik sınıflama mimari karmaşıklık ve nükleer atipi varlığına dayanır.",
            "badge": "Histopatoloji",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Endometriyal hiperplazi tanısı küretaj veya biyopsi materyalinin mikroskobik incelemesiyle konulur. Klasik Dünya Sağlık Örgütü (WHO) sınıflamasında iki temel kriter değerlendirilir: **Mimari yapı** (basit vs kompleks) ve **sitoloijk atipi** (atipisiz vs atipili).

Basit hiperplazide bezler kistik olarak geniştir ancak aralarında bol stroma bulunur. Kompleks hiperplazide bezler sırt sırta vermiş (back-to-back), kıvrıntılıdır. Ancak prognoz ve tedavi yaklaşımını belirleyen en kritik parametre **hücre çekirdeğinde atipi (nükleer atipi)** bulunup bulunmadığıdır.

> [TEMEL İLKE] Endometriyal hiperplazide kanserleşme riskini belirleyen ana unsur mimari değil, nükleer atipinin varlığıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Basit Hiperplazi", "desc": "Kistik genişlemiş bezler ve bol stroma; kanser riski %1 civarındadır.", "isKey": True},
                    {"title": "Kompleks Hiperplazi", "desc": "Bezler sırt sırta vermiş, stroma azalmış; atipisiz ise kanser riski %3'tür.", "isKey": True},
                    {"title": "Atipili Hiperplazi", "desc": "Nükleer irileşme, pleomorfizm ve polarite kaybı; kanser riski %25-40'tır.", "isKey": False}
                ],
                "table": {
                    "title": "Endometriyal Hiperplazi Tipleri ve Kanser Riski",
                    "headers": ["Hiperplazi Tipi", "Histolojik Mimari", "Kanserleşme Oranı"],
                    "rows": [
                        ["Basit Atipisiz", "Kistik genişlemiş bezler, bol stroma", "~ %1 risk"],
                        ["Kompleks Atipisiz", "Sırt sırta bezler, daralmış stroma", "~ %3 risk"],
                        ["Basit Atipili", "Kistik bezler + nükleer atipi", "~ %8 risk"],
                        ["Kompleks Atipili (EIN)", "Sırt sırta bezler + belirgin nükleer atipi", "%25 - %40 yüksek risk"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Endometriyal hiperplazide malignite riskini belirleyen en önemli faktör nükleer atipidir.",
                "📌 [SINAV SPOTU] Kompleks atipili endometriyal hiperplazide endometrium kanseri riski yaklaşık %25-40'tır."
            ],
            "medicalTerms": [
                {"term": "Nükleer Atipi", "explanation": "Hücre çekirdeğinde büyüme, hiperkromazi ve polarite kaybı ile beliren yapısal anormalliktir."},
                {"term": "EIN", "explanation": "Endometriyal intraepitelyal neoplazi; atipili hiperplazinin modern prekanseröz adıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Atipisiz ve Atipili Endometriyal Hiperplazi Karşılaştırması",
                    "Atipisiz Endometriyal Hiperplazi",
                    "Atipili Endometriyal Hiperplazi",
                    [
                        "Nükleuslar düzenli ve polarize",
                        "Kromatin yapısı homojen",
                        "Malignite riski çok düşük (<%3)"
                    ],
                    [
                        "İri, hiperkromatik nükleuslar",
                        "Polarite kaybı ve nükleol belirginliği",
                        "Yüksek kanser riski (%25 - %40)"
                    ]
                ),
                make_cloze(
                    "Endometriyal hiperplazide malign transformasyon riskini belirleyen en kritik histopatolojik ölçüt [nükleer atipi] varlığıdır.",
                    "nükleer atipi",
                    "Çekirdek anormalliği terimi"
                )
            ]
        },

        # Adım 43
        {
            "slideNumber": 43,
            "title": "Atipili Endometriyal Hiperplazi ve Adenokarsinom Riski",
            "subtitle": "Atipili hiperplazi benign bir adaptasyon olmaktan çıkarak klonal neoplastik öncü lezyona dönüşür.",
            "badge": "Onkolojik Risk",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Atipili endometriyal hiperplazi, patolojide benign adaptasyon ile açık kanser arasındaki sınır çizgisidir. Bu lezyonda artık basit bir hormonal yanıt değil, **PTEN**, **PIK3CA** ve **KRAS** gibi onkogenik genetik mutasyonlar birikmeye başlamıştır.

Klinik çalışmalarda atipili kompleks hiperplazi tanısı alan kadınların **%25 - 40'ında** eşzamanlı veya sonraki yıllarda invaziv **endometrioid adenokarsinom** geliştiği gösterilmiştir. Hatta histerektomi yapılan hastaların üçte birinde operasyon sırasında odaksal karsinom saptanmaktadır.

> [KLİNİK İPUCU] Atipili endometriyal hiperplazi saptanan postmenopozal veya doğurganlığını tamamlamış kadınlarda standart tedavi histerektomidir (uterusun çıkarılması).""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Genetik Zemin", "desc": "PTEN tümör baskılayıcı gen mutasyonları atipili hiperplazide sıkça saptanır.", "isKey": True},
                    {"title": "Yüksek Kanser Riski", "desc": "Hastaların üçte birinden fazlasında invaziv adenokarsinom birlikteliği vardır.", "isKey": True},
                    {"title": "Cerrahi Karar", "desc": "Kanser öncüsü kabul edildiğinden histerektomi endikasyonu doğurur.", "isKey": False}
                ],
                "table": {
                    "title": "Hiperplazi - Kanser Geçiş Basamakları",
                    "headers": ["Evre", "Moleküler Değişim", "Klinik Yönetim"],
                    "rows": [
                        ["Atipisiz Hiperplazi", "Poliklonal çoğalma, östrojen fazlalığı", "Medikal progesteron tedavisi"],
                        ["Atipili Hiperplazi (EIN)", "PTEN mutasyonu, monoklonal başlangıç", "Histerektomi veya yüksek doz progestin"],
                        ["İnvaziv Karsinom", "Miyometriyal invazyon, p53/mikrosatellit", "Radikal cerrahi ve onkolojik evreleme"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Atipili endometriyal hiperplazi endometrioid adenokarsinomun doğrudan öncü lezyonudur.",
                "📌 [SINAV SPOTU] PTEN mutasyonu atipili hiperplazi ve endometrium kanserinde en sık saptanan genetik kusurdur."
            ],
            "medicalTerms": [
                {"term": "Adenokarsinom", "explanation": "Glandüler epitelden köken alan malign epitelyal tümördür."},
                {"term": "PTEN Geni", "explanation": "PI3K/Akt yolağını frenleyen, mutasyonunda kontrolsüz hücre çoğalması yaratan tümör baskılayıcı gendir."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "55 yaşında postmenopozal kanama şikayetiyle başvuran ve yapılan endometriyal biyopsisinde 'Kompleks Atipili Endometriyal Hiperplazi' raporlanan hastanın klinik yönetimi senaryosu.",
                    [
                        {
                            "text": "Hiperplazi benign bir süreç olduğundan hiçbir tedavi verilmez, hasta evine gönderilir.",
                            "isCorrect": False,
                            "feedback": "Kabul edilemez malpraktis! Atipili hiperplazide kanser riski %25-40'tır; tedavisiz bırakılamaz."
                        },
                        {
                            "text": "Lezyon adenokarsinom öncülü kabul edilir; postmenopozal hastada eşzamanlı invaziv kanser riski nedeniyle total histerektomi ve bilateral salpingo-ooferektomi planlanır.",
                            "isCorrect": True,
                            "feedback": "Mükemmel jinekolojik onkoloji kararı! Atipili hiperplazide definitif tedavi histerektomidir."
                        },
                        {
                            "text": "Hastaya sadece oral demir ilacı başlanır.",
                            "isCorrect": False,
                            "feedback": "Yetersiz! Anemi tedavisi altta yatan neoplastik riski çözmez."
                        }
                    ]
                ),
                make_cloze(
                    "Kompleks atipili endometriyal hiperplazide en sık inaktive olan tümör baskılayıcı gen [PTEN] genidir.",
                    "PTEN",
                    "PI3K yolağını baskılayan tümör baskılayıcı gen"
                )
            ]
        },

        # Adım 44
        {
            "slideNumber": 44,
            "title": "Benign Prostat Hiperplazisi (BPH): DHT ve Stroma-Epitel Etkileşimi",
            "subtitle": "Yaşlanan erkekte dihidrotestosteron (DHT) uyarımı prostatın periüretral bölgesinde nodüler hiperplazi yapar.",
            "badge": "Ürolojik Patoloji",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Erkeklerde yaşlanmayla en sık karşılaşılan patolojik hiperplazi modeli **Benign Prostat Hiperplazisidir (BPH)**. 50 yaşın üzerindeki erkeklerin yarısından fazlasında, 80 yaşında ise %90'ında görülür.

BPH'nin ana itici gücü testosterondan 5-alfa redüktaz enzimiyle sentezlenen **dihidrotestosterondur (DHT)**. DHT, testosterona göre androjen reseptörlerine çok daha güçlü bağlanır. Prostat stromal hücrelerinde FGF ve TGF-β salınımını uyararak hem glandüler epitelde hem de fibromusküler stromada hiperplazi başlatır.

> [TEMEL İLKE] BPH saf epitelyal bir hiperplazi değildir; stromal fibroblastlar ile glandüler epitelin el ele çoğaldığı bir stroma-epitel hiperplazisidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "DHT Bağımlılığı", "desc": "5-alfa redüktaz enzimiyle üretilen DHT prostatik büyümenin ana hormonudur.", "isKey": True},
                    {"title": "Stroma ve Epitel", "desc": "Hem salgı bezleri hem de aradaki düz kas/bağ dokusu birlikte çoğalır.", "isKey": True},
                    {"title": "Medikal Hedef", "desc": "5-alfa redüktaz inhibitörleri (finasterid) DHT'yi düşürerek BPH'yi geriletir.", "isKey": False}
                ],
                "table": {
                    "title": "BPH'de Hormonal ve Moleküler Mekanizmalar",
                    "headers": ["Faktör", "Biyolojik Kaynak", "Prostattaki Etkisi"],
                    "rows": [
                        ["Testosteron", "Testis Leydig hücreleri", "Öncül hormon, dokuda DHT'ye çevrilir"],
                        ["DHT", "Prostat stromal hücreleri (Tip 2 5-AR)", "Androjen reseptörünü uyararak hiperplazi yapar"],
                        ["FGF-7", "Stromal hücreler", "Epitel hücre mitozunu parakrin olarak uyarır"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Benign prostat hiperplazisinin gelişiminden primer sorumlu aktif androjen dihidrotestosterondur (DHT).",
                "📌 [SINAV SPOTU] Testosteronu DHT'ye dönüştüren enzim 5-alfa redüktazdır."
            ],
            "medicalTerms": [
                {"term": "BPH", "explanation": "Prostat bezinde stroma ve gland epitelinin nodüler çoğalmasıyla karakterize benign hastalıktır."},
                {"term": "5-Alfa Redüktaz", "explanation": "Testosteronu daha potent olan dihidrotestosterona (DHT) dönüştüren enzimdir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "BPH Patogenezinde Androjen Kaskadı",
                    [
                        "1. Testosteron Girişi: Dolaşımdaki testosteronun prostat stromal hücresine girmesi.",
                        "2. Enzimatik Dönüşüm: 5-alfa redüktaz Tip 2 ile dihidrotestosteron (DHT) üretimi.",
                        "3. Nükleer Bağlanma: DHT'nin androjen reseptörüne bağlanıp nükleusa geçmesi.",
                        "4. Parakrin Sinyal: Büyüme faktörlerinin (FGF-7, TGF-beta) sentezlenip epitele sunulması.",
                        "5. Nodüler Hiperplazi: Periüretral zonda glandüler ve stromal nodüllerin oluşması."
                    ]
                ),
                make_cloze(
                    "Benign prostat hiperplazisinde testosteronu daha güçlü olan DHT'ye çeviren anahtar enzim [5-alfa redüktaz] enzimidir.",
                    "5-alfa redüktaz",
                    "Androjen dönüştürücü enzim"
                )
            ]
        },

        # Adım 45
        {
            "slideNumber": 45,
            "title": "BPH'nin Histopatolojisi: Transizyonel Zonda Glandüler ve Fibröz Nodüller",
            "subtitle": "BPH anatomik olarak üretra etrafındaki transizyonel zonda nodüller oluşturarak idrar akımını tıkar.",
            "badge": "Anatomik Lokalizasyon",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """BPH'nin klinik tablosunu belirleyen en kritik özellik **anatomik lokalizasyonudur**. Prostat üç temel zondan oluşur: Periferik zon, santral zon ve transizyonel zon.

BPH neredeyse istisnasız olarak prostatik üretra etrafındaki **transizyonel (geçiş) zonda** ve periüretral bölgede gelişir. Büyüyen glandüler ve stromal nodüller üretrayı sıkıştırarak lümeni daraltır. Bu durum idrar yapmada zorlanma, çatallanma, noktüri ve idrar retansiyonu ile karakterize alt üriner sistem semptomlarına (LUTS) neden olur.

> [SINAV KURALI] BPH transizyonel zonda (üretra çevresi) gelişir ve erken obstrüksiyon yapar; prostat kanseri ise periferik zonda gelişir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Transizyonel Zon", "desc": "Üretrayı saran iç bölgedir; BPH nodülleri daima burada gelişir.", "isKey": True},
                    {"title": "Nodüler Mimari", "desc": "Papiller kıvrımlı bezler ile pembe düz kas stroması nodüller oluşturur.", "isKey": True},
                    {"title": "Obstrüksiyon", "desc": "Üretraya bası yaparak idrar çıkışını mekanik olarak engeller.", "isKey": False}
                ],
                "table": {
                    "title": "Prostat Zonları ve Patoloji Dağılımı",
                    "headers": ["Anatomik Zon", "Tipik Gelişen Patoloji", "Temel Klinik Bulgusu"],
                    "rows": [
                        ["Transizyonel Zon", "Benign Prostat Hiperplazisi (BPH)", "Erken üretra obstrüksiyonu, disüri, noktüri"],
                        ["Periferik Zon", "Prostat Adenokarsinomu", "Rektal muayenede sert nodül, geç obstrüksiyon"],
                        ["Santral Zon", "Nadir benign lezyonlar", "Genellikle asemptomatik"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] BPH prostatın transizyonel (periüretral) zonunda gelişir.",
                "📌 [SINAV SPOTU] Prostat kanseri periferik zonda, BPH ise transizyonel zonda gelişir."
            ],
            "medicalTerms": [
                {"term": "Transizyonel Zon", "explanation": "Prostatik üretrayı çevreleyen ve BPH'nin geliştiği iç prostat bölgesidir."},
                {"term": "Periferik Zon", "explanation": "Prostatın arka-dış kısmını oluşturan ve karsinomların en sık yerleştiği zondur."}
            ],
            "interactiveElements": [
                make_before_after(
                    "BPH ile Prostat Kanserinin Anatomik ve Klinik Karşılaştırması",
                    "Benign Prostat Hiperplazisi (BPH)",
                    "Prostat Adenokarsinomu",
                    [
                        "Transizyonel (periüretral) zonda gelişir",
                        "Erken dönemde üretra obstrüksiyonu yapar",
                        "Benign gland ve stroma nodülleri"
                    ],
                    [
                        "Periferik (arka-dış) zonda gelişir",
                        "Üretrayı geç sıkıştırır, geç semptom verir",
                        "Malign gland infiltrasyonu ve invazyon"
                    ]
                ),
                make_active_recall(
                    "BPH hastalarında idrar yapma güçlüğü (obstrüksiyon) erken dönemde belirirken, prostat kanserinde neden obstrüksiyon çok geç evrelerde ortaya çıkar?",
                    "Çünkü BPH doğrudan üretrayı saran transizyonel zonda gelişip üretrayı hemen daraltırken; prostat kanseri üretraya uzak periferik zonda başlar."
                )
            ]
        },

        # Adım 46
        {
            "slideNumber": 46,
            "title": "Siğiller (Verrü) ve Viral Kaynaklı Hiperplaziler: HPV E6 ve E7 Etkisi",
            "subtitle": "İnsan papilloma virüsü (HPV) epitel hücre döngüsünü bozarak epidermal hiperplazi oluşturur.",
            "badge": "Enfeksiyöz Hiperplazi",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hiperplazi yalnızca hormonlarla değil, bazı viral enfeksiyonlarla da tetiklenebilir. Bunun en bilinen örneği deride ve mukozalarda **siğillere (verrüka)** yol açan **İnsan Papilloma Virüsüdür (HPV)**.

HPV'nin kodladığı viral onkoproteinlerden **E7**, hücre döngüsünü frenleyen retinoblastom (Rb) proteinine bağlanarak onu inaktive eder. **E6** ise tümör baskılayıcı p53 proteinini ubikuitinleyip yıkar. Fren mekanizmaları çöken skuamöz epitel kontrolsüzce çoğalarak kalınlaşır (**akantoz** ve **hiperkeratoz**).

> [TEMEL İLKE] Viral proteinler konak hücrenin tümör baskılayıcı frenlerini yıkarak epidermal hiperplazi meydana getirir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Viral Onkoproteinler", "desc": "HPV E6 p53'ü parçalar; E7 ise Rb proteinini bağlayarak susturur.", "isKey": True},
                    {"title": "Akantoz", "desc": "Stratum spinosum tabakasındaki keratinosit sayısının belirgin artışıdır.", "isKey": True},
                    {"title": "Koilosite", "desc": "HPV enfeksiyonunun sitopatik etkisi olan perinükleer halolu atipik hücrelerdir.", "isKey": False}
                ],
                "table": {
                    "title": "HPV Onkoproteinleri ve Hücresel Etkileri",
                    "headers": ["Viral Protein", "Hedef Konak Molekülü", "Hücresel Sonuç"],
                    "rows": [
                        ["HPV E7", "Retinoblastom Proteini (pRb)", "E2F serbestleşir, hücre S fazına zorlanır (hiperplazi)"],
                        ["HPV E6", "p53 Tümör Baskılayıcı Protein", "Apoptoz engellenir, hasarlı hücre bölünmeye devam eder"],
                        ["Koilosite", "Sitokeratin iskeleti", "Perinükleer berrak vakuol ve nükleer büzüşme"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Deri siğilleri (verrü) HPV kaynaklı viral epidermal hiperplazidir.",
                "📌 [SINAV SPOTU] HPV E7 proteini Rb'yi inaktive ederken, E6 proteini p53'ü yıkarak hücre döngüsünü hızlandırır."
            ],
            "medicalTerms": [
                {"term": "Akantoz", "explanation": "Epidermisin stratum spinosum tabakasındaki hücre sayısının artmasıyla kalınlaşmasıdır."},
                {"term": "Koilosite", "explanation": "HPV enfeksiyonunda görülen iri, hiperkromatik ve çevresi berrak halolu skuamöz hücredir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "HPV Aracılı Siğil Gelişimi Kaskadı",
                    [
                        "1. Viral İnokülasyon: HPV'nin mikrotravma yoluyla bazal keratinositlere girişi.",
                        "2. Viral Protein Sentezi: Hücre içinde E6 ve E7 onkoproteinlerinin üretilmesi.",
                        "3. Frenlerin Yıkımı: E7'nin Rb'yi bağlaması, E6'nın p53'ü parçalaması.",
                        "4. Epitelyal Çoğalma: Keratinositlerin hızla mitoza girerek akantoz ve hiperkeratoz yapması.",
                        "5. Siğil Oluşumu: Deri yüzeyinde ekzofitik, papillomatöz lezyonun belirmesi."
                    ]
                ),
                make_cloze(
                    "HPV enfeksiyonunda hücre siklusunu frenleyen Rb proteinini bağlayarak epidermal hiperplaziyi başlatan viral protein [E7] proteinidir.",
                    "E7",
                    "Rb'yi inaktive eden viral onkoprotein"
                )
            ]
        },

        # Adım 47
        {
            "slideNumber": 47,
            "title": "Yara İyileşmesinde Aşırı Granülasyon Dokusu ve Skar Hiperplazisi",
            "subtitle": "Doku tamirinde fibroblast ve damarların aşırı çoğalması exuberant granülasyona ve keloide yol açar.",
            "badge": "Onarım Patolojisi",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Yara iyileşmesi fibroblastların, endotel hücrelerinin ve epitelin kontrollü proliferasyonuna dayanan fizyolojik bir süreçtir. Ancak büyüme faktörü uyarımı aşırı olursa patolojik hiperplaziler gelişir.

Eğer iyileşen yarada endotel ve fibroblast çoğalması kontrolsüz kalırsa cilt yüzeyinden taşan **exuberant granülasyon dokusu** (halk arasında gurur eti / proud flesh) oluşur ve epitelizasyonu engeller. Benzer şekilde skar dokusunda aşırı kollajen sentezlenmesi ve fibroblast proliferasyonu **keloid** ve **hipertrofik skarla** sonuçlanır.

> [TEMEL İLKE] Doku onarımında proliferasyonun zamanında durdurulamaması fibröz ve vasküler hiperplazilere yol açar.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Exuberant Granülasyon", "desc": "Yara sınırlarını aşan aşırı damar ve fibroblast proliferasyonudur.", "isKey": True},
                    {"title": "Keloid Gelişimi", "desc": "Yara sınırlarının ötesine taşan aşırı tip I ve III kollajen birikimidir.", "isKey": True},
                    {"title": "TGF-β Fazlalığı", "desc": "Aşırı büyüme faktörü uyarımı fibroblastları durmaksızın uyarır.", "isKey": False}
                ],
                "table": {
                    "title": "Yara İyileşmesinde Aşırı Proliferatif Durumlar",
                    "headers": ["Durum", "Baskın Çoğalan Hücre", "Morfolojik Karakteristik"],
                    "rows": [
                        ["Granülasyon Dokusu (Normal)", "Endotel + Fibroblast", "Yara tabanında kırmızı, granüllü vasküler doku"],
                        ["Exuberant Granülasyon", "Aşırı damar ve fibroblast", "Yara kenarlarından yukarı taşan et kitlesi"],
                        ["Keloid Skar", "Miyofibroblastlar", "Orijinal yara sınırlarını aşan kalın hyalinize kollajen"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Yara iyileşmesinde aşırı granülasyon dokusu oluşumuna exuberant granülasyon (gurur eti) denir.",
                "📌 [SINAV SPOTU] Keloid, yara sınırlarını aşarak çevre dokuya taşan patolojik skar ve kollajen hiperplazisidir."
            ],
            "medicalTerms": [
                {"term": "Granülasyon Dokusu", "explanation": "Yara tabanında yeni oluşan narin kılcal damarlar ve genç fibroblastlardan zengin tamir dokusudur."},
                {"term": "Keloid", "explanation": "Deri hasarı sonrası orijinal kesi sınırlarını aşarak büyüyen aşırı kollajenli skar dokusudur."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Normal Yara İyileşmesi ile Keloid Gelişimi",
                    "Normal Skarlaşma",
                    "Keloid Gelişimi",
                    [
                        "Proliferasyon zamanında durdurulur",
                        "Skar yara sınırları içinde kalır",
                        "Dengeli kollajen sentez ve yıkımı"
                    ],
                    [
                        "Fibroblast proliferasyonu durdurulamaz",
                        "Skar yara sınırlarını aşarak yayılır",
                        "Yoğun, hyalinize kaba kollajen yumakları"
                    ]
                ),
                make_active_recall(
                    "Cerrahi kesi sonrası oluşan bir skarın 'keloid' olarak adlandırılabilmesi için gereken en kritik morfolojik ölçüt nedir?",
                    "Skar dokusunun orijinal cerrahi yara sınırlarının ötesine taşarak çevre sağlam deriye doğru genişlemesidir."
                )
            ]
        },

        # Adım 48
        {
            "slideNumber": 48,
            "title": "Patolojik Hiperplazi ile Neoplazi Arasındaki Kritik Sınır: Geri Çekilme Yeteneği",
            "subtitle": "Hiperplazi uyarana bağımlıdır ve uyaran kesilince geriler; neoplazi ise uyarandan bağımsız otonomdur.",
            "badge": "Onkolojik Sınır",
            "badgeColor": "cyan",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patolojinin en temel felsefi ve pratik ayrımlarından biri **patolojik hiperplazi ile neoplazi (tümör)** arasındaki sınırdır.

Patolojik hiperplazide büyüme kontrol mekanizmaları halen kısmen sağlamdır; çoğalma dışsal bir hormonal veya trofik **uyarana bağımlıdır**. Bu uyaran ortadan kaldırıldığında hücre çoğalması durur ve doku geriler. Buna karşılık **neoplazide** somatik genetik mutasyonlar nedeniyle hücreler otonomlaşmıştır; dış uyaran kalksa dahi kontrolsüz çoğalma kesintisiz sürer.

> [TEMEL İLKE] Uyaran kalkınca gerileme adaptasyonun (hiperplazi) kanıtıdır; uyaran olmaksızın otonom çoğalma ise neoplazinin (kanser) tanımıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Uyarana Bağımlılık", "desc": "Hiperplazide hormon/büyüme faktörü kesilince lezyon küçülür ve geriler.", "isKey": True},
                    {"title": "Otonomi", "desc": "Neoplazide büyüme faktörü gerekmeksizin hücreler kendi kendine çoğalır.", "isKey": True},
                    {"title": "Klonallik", "desc": "Hiperplazi genellikle poliklonaldir; neoplazi ise monoklonal bir hücreden köken alır.", "isKey": False}
                ],
                "table": {
                    "title": "Patolojik Hiperplazi ve Neoplazi Ayırıcı Tanısı",
                    "headers": ["Parametre", "Patolojik Hiperplazi", "Neoplazi (Tümör)"],
                    "rows": [
                        ["Uyaran Bağımlılığı", "Tamamen bağımlı (uyaran bitince durur)", "Otonom (uyaran olmasa da sürer)"],
                        ["Hücresel Klonallik", "Poliklonal (tüm doku yanıt verir)", "Monoklonal (tek bir mutasyona uğramış klon)"],
                        ["Genetik Mutasyon", "Yok veya epigenetik/erken", "Sürekli ve ilerleyici somatik sürücü mutasyonlar"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patolojik hiperplazi uyarana bağımlıdır; uyaran ortadan kaldırılınca geriler.",
                "📌 [SINAV SPOTU] Neoplazinin temel özelliği uyaranlardan bağımsız otonom hücre çoğalmasıdır."
            ],
            "medicalTerms": [
                {"term": "Otonomi", "explanation": "Tümör hücrelerinin vücudun normal büyüme sinyallerine ihtiyaç duymadan çoğalabilmesidir."},
                {"term": "Poliklonal Çoğalma", "explanation": "Birden fazla farklı hücre klonunun aynı anda uyarana yanıt vererek bölünmesidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Patolojik bir lezyonun hiperplazi mi yoksa neoplazi mi olduğunu belirlemede patoloğun göz önüne aldığı en temel biyolojik ölçüt nedir?",
                    {
                        "A": "Büyümenin dışsal bir hormonal/kimyasal uyarana bağımlı olup olmadığı ve uyaran kesilince gerileyip gerilemediği",
                        "B": "Lezyonun yalnızca kadın hastalarda görülüp görülmediği",
                        "C": "Hücrelerin içinde mitokondri bulunup bulunmadığı",
                        "D": "Lezyonun mikroskop altında tamamen mavi renkte boyanması",
                        "E": "Doku hücrelerinde ribozom bulunmaması"
                    },
                    "A",
                    {
                        "A": "Doğru: Hiperplazi uyarana bağımlıdır ve geriler; neoplazi uyarandan bağımsız otonomdur.",
                        "B": "Yanlış: Cinsiyet ayrımı neoplazi/hiperplazi ölçütü değildir.",
                        "C": "Yanlış: Tüm canlı hücrelerde mitokondri bulunur.",
                        "D": "Yanlış: Boyanma rengi tanı ölçütü değildir.",
                        "E": "Yanlış: Her iki durumda da protein sentezi için ribozom şarttır."
                    }
                ),
                make_cloze(
                    "Neoplazi uyarandan bağımsız otonom seyrederken, patolojik hiperplazide büyüme kesinlikle dış [uyarana] bağımlıdır.",
                    "uyarana",
                    "Dışsal tetikleyici etken"
                )
            ]
        },

        # Adım 49 (CHECKPOINT 5)
        {
            "slideNumber": 49,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Patolojik Hiperplazi ve Neoplazi Riski",
            "subtitle": "Patolojik hiperplazi mekanizmalarını, BPH ve endometriyal hiperplazi modellerini ve neoplazi sınırını pekiştirin.",
            "badge": "Tekrar Sayfası",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 5,
            "synthesisNarrative": """Bu bölümde aşırı hormonal ve büyüme faktörü uyarımıyla gelişen patolojik hiperplazileri, BPH'yi, endometriyal hiperplaziyi ve neoplazi sınırını inceledik.

Patolojik hiperplazi uyarana bağımlı ve geri dönüşümlüdür. Endometriyumda karşılanmamış östrojen bez çoğalması yapar; nükleer atipi eklendiğinde adenokarsinom riski %25-40'a çıkar. Prostatta DHT etkisiyle transizyonel zonda BPH gelişerek üretra obstrüksiyonu oluşturur. HPV ise E6 ve E7 ile tümör baskılayıcıları yıkarak viral hiperplaziye yol açar.

> [TEKRAR SPOTU] Atipisiz hiperplaziler benign seyrederken; nükleer atipili hiperplaziler kanser öncüsü kabul edilir ve radikal tedavi gerektirir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hormon Fazlalığı", "desc": "Endometriumda östrojen, prostatta DHT patolojik hiperplazi tetikleyicisidir.", "isKey": True},
                    {"title": "Atipi Riski", "desc": "Endometriyal hiperplazide nükleer atipi varlığı malignite riskini belirler.", "isKey": True},
                    {"title": "Anatomik Kural", "desc": "BPH transizyonel zonda üriner tıkanıklık yapar; prostat kanseri periferik zonda gelişir.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 5 Sentez Tablosu",
                    "headers": ["Klinik Patoloji", "Tetikleyici Etken", "Kritik Onkolojik Boyut"],
                    "rows": [
                        ["Endometriyal Hiperplazi", "Karşılanmamış östrojen", "Atipili formda %25-40 adenokarsinom riski"],
                        ["Benign Prostat Hiperplazisi", "Dihidrotestosteron (DHT)", "Transizyonel zon obstrüksiyonu, kanserleşmez"],
                        ["Deri Siğilleri (Verrü)", "HPV E6 ve E7 onkoproteinleri", "Viral epidermal akantoz ve hiperkeratoz"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Endometriyal hiperplazide malignite riskini belirleyen en kritik ölçüt nükleer atipidir.",
                "📌 [SINAV SPOTU] BPH transizyonel zonda gelişip erken obstrüksiyon yaparken; prostat kanseri periferik zonda yerleşir."
            ],
            "medicalTerms": [
                {"term": "Patolojik Hiperplazi", "explanation": "Aşırı hormon uyarısıyla oluşan, uyarana bağımlı geri dönüşümlü hücre çoğalmasıdır."},
                {"term": "Dihidrotestosteron (DHT)", "explanation": "Prostatta 5-alfa redüktazla üretilen ve BPH gelişimini yöneten potent androjendir."}
            ],
            "flashcards": [
                make_flashcard(
                    "k1-03-fc13",
                    "Endometriyal hiperplazinin gelişimindeki temel hormonal dengesizlik nedir?",
                    "Östrojen hormonunun aşırı ve sürekli salgılanırken, ovülasyon olmaması nedeniyle progesteron ile dengelenememesidir (karşılanmamış östrojen)."
                ),
                make_flashcard(
                    "k1-03-fc14",
                    "BPH ile prostat karsinomu arasındaki anatomik yerleşim ve klinik semptom farkı nedir?",
                    "BPH üretrayı saran transizyonel zonda gelişip erken dönemde idrar obstrüksiyonu yapar; prostat kanseri ise periferik zonda yerleşip geç obstrüksiyon verir."
                ),
                make_flashcard(
                    "k1-03-fc15",
                    "Patolojik hiperplaziyi neoplaziden (tümörden) ayıran temel biyolojik özellik nedir?",
                    "Hiperplazide hücre çoğalması dış uyarana bağımlıdır ve uyaran kesilince geriler; neoplazide ise hücre çoğalması uyarandan bağımsız otonomdur."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Atipili endometriyal hiperplazi tanısı alan 55 yaşındaki bir hastada neden doğrudan medikal takip yerine histerektomi cerrahisi önerilir?",
                    "Çünkü atipili hiperplazide adenokarsinoma dönüşüm riski %25-40'tır ve histerektomi materyallerinin üçte birinde eşzamanlı gizli invaziv kanser saptanır."
                )
            ]
        }
    ]
