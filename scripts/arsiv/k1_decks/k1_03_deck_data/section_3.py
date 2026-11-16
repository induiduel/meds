#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 3: Patolojik Hipertrofi, Moleküler Sinyaller ve Kardiyak Dekompansasyon (Adımlar 20 - 29)
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
        # Adım 20
        {
            "slideNumber": 20,
            "title": "Patolojik Kardiyak Hipertrofi: Hipertansiyon ve Aort Stenozu",
            "subtitle": "Kronik hemodinamik aşırı yüklenme sol ventrikül miyositlerinde patolojik hipertrofiyi başlatır.",
            "badge": "Klinik Patoloji",
            "badgeColor": "rose",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patolojik kardiyak hipertrofinin en yaygın nedenleri **sistemik hipertansiyon** ve **aort kapak stenozudur**. Her iki patolojide de sol ventrikül kanı aortaya pompalayabilmek için sürekli yüksek bir çıkış direncine (art yük / afterload) karşı çalışmak zorundadır.

Laplace kanununa göre artan intraventriküler basınç miyokard duvar gerilimini yükseltir. Kalp bu gerilimi düşürmek ve duvar stresini normalize etmek amacıyla miyositlerini kalınlaştırır. Bu yanıt başlangıçta debiyi koruyan kompansatuvar bir adaptasyondur.

> [TEMEL İLKE] Patolojik hipertrofi, artan duvar stresini azaltmak için kalbin geliştirdiği zorunlu ancak uzun vadede tehlikeli bir adaptasyondur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Art Yük Artışı", "desc": "Hipertansiyon ve aort darlığı sol ventrikül önünde aşırı direnç oluşturur.", "isKey": True},
                    {"title": "Duvar Gerilimi", "desc": "Laplace yasasına göre duvar kalınlaşması (hipertrofi) tepe duvar stresini düşürür.", "isKey": True},
                    {"title": "Kompansasyon Sınırı", "desc": "Hipertrofi başlangıçta kalbin debisini korur ancak zamanla tüketir.", "isKey": False}
                ],
                "table": {
                    "title": "Sol Ventrikül Hipertrofisi Nedenleri",
                    "headers": ["Etiyoloji", "Hemodinamik Mekanizma", "Kardiyak Yük Tipi"],
                    "rows": [
                        ["Sistemik Hipertansiyon", "Periferik vasküler direnç artışı", "Kronik basınç aşırı yükü"],
                        ["Aort Kapak Stenozu", "Daralmış kapak deliğinden kan pompalama", "Ağır sistolik çıkış direnci"],
                        ["Mitral Yetersizliği", "Ventriküle aşırı kan geri dönüşü", "Hacim aşırı yükü (eksantrik)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Sol ventrikül patolojik hipertrofisinin en sık iki nedeni sistemik hipertansiyon ve aort stenozudur.",
                "📌 [SINAV SPOTU] Basınç aşırı yükü konsantrik hipertrofiye (duvar kalınlaşması) yol açar."
            ],
            "medicalTerms": [
                {"term": "Art Yük (Afterload)", "explanation": "Ventrikülün sistolde kanı fırlatabilmek için yenmek zorunda olduğu vasküler dirençtir."},
                {"term": "Aort Stenozu", "explanation": "Aort kapağının daralarak sol ventrikül çıkış yolunu tıkamasıdır."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Kronik sistemik hipertansiyonu olan 60 yaşındaki bir hastada sol ventrikül miyokardında gelişen konsantrik kalınlaşmanın temel hemodinamik tetikleyicisi nedir?",
                    {
                        "A": "Kronik basınç aşırı yükü (art yük artışı)",
                        "B": "Akut akciğer ödemi ve hipoksi",
                        "C": "Koroner arterlerdeki ani spazm",
                        "D": "Bakteriyel endokardite bağlı kapak yıkımı",
                        "E": "Perikard yaprakları arasında sıvı birikimi"
                    },
                    "A",
                    {
                        "A": "Doğru: Hipertansiyonda yüksek sistemik direnç basınç aşırı yükü oluşturarak hipertrofiyi tetikler.",
                        "B": "Yanlış: Akciğer ödemi hipertrofinin başlangıç nedeni değil yetmezlik sonucudur.",
                        "C": "Yanlış: Koroner spazm iskemi yapar, kronik konsantrik hipertrofi nedeni değildir.",
                        "D": "Yanlış: Endokardit enfeksiyondur, basınç hipertrofisi yapmaz.",
                        "E": "Yanlış: Perikard sıvısı tamponad yapabilir, miyokard hipertrofisi nedeni değildir."
                    }
                ),
                make_cloze(
                    "Hipertansiyon ve aort darlığında sol ventrikülün maruz kaldığı aşırı hemodinamik dirence [basınç] aşırı yükü adı verilir.",
                    "basınç",
                    "Hemodinamik direnç türü"
                )
            ]
        },

        # Adım 21
        {
            "slideNumber": 21,
            "title": "Sol Ventrikül Konsantrik Hipertrofisi: Duvar Kalınlığı (>2 cm)",
            "subtitle": "Basınç yüküne bağlı konsantrik hipertrofide ventrikül lümeni daralırken duvar kalınlığı 2 cm'yi aşar.",
            "badge": "Morfolojik Kriter",
            "badgeColor": "rose",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Normal bir erişkinde sol ventrikül serbest duvar kalınlığı **1.0 - 1.5 cm** arasındadır ve kalbin ağırlığı erkeklerde yaklaşık 300-350 gramdır.

Kronik hipertansiyona bağlı **konsantrik hipertrofide** ventrikül kavitesi genişlemez; tersine lümen daralırken serbest duvar ve interventriküler septum belirgin biçimde kalınlaşarak **2 cm'nin üzerine** çıkar. Kalbin toplam ağırlığı 500-800 grama (kor bovinum) kadar ulaşabilir.

> [KLİNİK İPUCU] Sol ventrikül serbest duvar kalınlığının 2 cm'yi aşması otopside ve ekokardiyografide patolojik hipertrofinin kesin kanıtıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Normal Duvar", "desc": "Sol ventrikül normal kalınlığı 1.0 - 1.5 cm aralığındadır.", "isKey": True},
                    {"title": "Konsantrik Kalınlaşma", "desc": "Patolojik hipertrofide duvar kalınlığı 2 cm'nin üzerine çıkar.", "isKey": True},
                    {"title": "Ağırlık Artışı", "desc": "Kalp ağırlığı 350 gramdan 600-800 gram seviyesine kadar yükselebilir.", "isKey": False}
                ],
                "table": {
                    "title": "Normal ve Hipertrofik Sol Ventrikül Ölçütleri",
                    "headers": ["Parametre", "Normal Sol Ventrikül", "Hipertrofik Sol Ventrikül"],
                    "rows": [
                        ["Duvar Kalınlığı", "1.0 - 1.5 cm", "> 2.0 cm (belirgin kalın)"],
                        ["Kalp Ağırlığı", "Erkekte 300-350 g, kadında 250-300 g", "500 - 800 gram (ağırlaşmış)"],
                        ["Lümen Geometrisi", "Normal elipsoid kavite", "Daralmış (konsantrik tip)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Normal sol ventrikül duvar kalınlığı 1-1.5 cm'dir; patolojik hipertrofide 2 cm'yi geçer.",
                "📌 [SINAV SPOTU] Basınç yükünde kavite genişlemeden duvar kalınlaşmasına konsantrik hipertrofi denir."
            ],
            "medicalTerms": [
                {"term": "Konsantrik Hipertrofi", "explanation": "Ventrikül lümeni genişlemeksizin duvar kalınlığının içe doğru artmasıdır."},
                {"term": "Kor Bovinum", "explanation": "Ağır patolojik hipertrofi nedeniyle öküz kalbi boyutuna (800 g üzeri) ulaşmış dev kalptir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Normal Sol Ventrikül ile Konsantrik Hipertrofi Morfolojisi",
                    "Normal Sol Ventrikül",
                    "Konsantrik Hipertrofik Sol Ventrikül",
                    [
                        "Duvar kalınlığı 1.0 - 1.5 cm",
                        "Kalp ağırlığı 300 - 350 gram",
                        "Lümen hacmi normal ve esnek"
                    ],
                    [
                        "Duvar kalınlığı > 2.0 cm",
                        "Kalp ağırlığı 500 - 800 gram",
                        "Lümen daralmış ve duvar sertleşmiş"
                    ]
                ),
                make_cloze(
                    "Patolojik kardiyak hipertrofide sol ventrikül serbest duvar kalınlığı normal sınır olan 1.5 cm'yi aşarak [2] santimetrenin üzerine çıkar.",
                    "2",
                    "Kritik santimetre sınırı rakamı"
                )
            ]
        },

        # Adım 22
        {
            "slideNumber": 22,
            "title": "Fetal Gen Programına Geri Dönüş: ANP ve BNP Salınımı",
            "subtitle": "Hipertrofiye uğrayan kardiyomiyositler fetal dönem genlerini yeniden aktive eder.",
            "badge": "Fetal Reprogramlama",
            "badgeColor": "rose",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patolojik hipertrofinin en çarpıcı moleküler özelliklerinden biri **fetal gen programının yeniden aktivasyonudur**. Normalde embriyonik dönemde aktif olan ancak doğumdan sonra susturulan bazı genler patolojik stresle tekrar açılır.

Bu genlerin başında **Atriyal Natriüretik Peptit (ANP)** ve **Beyin Natriüretik Peptit (BNP)** gelir. Normalde yalnız atriyumda üretilen ANP, hipertrofik ventrikül miyositlerinden yoğun şekilde kana salgılanır. Bu peptitler böbrekten sodyum ve su atarak kan hacmini düşürmeye çalışır.

> [KLİNİK İPUCU] Plazma BNP düzeyinin kanda yükselmesi, ventriküler duvar geriliminin ve patolojik hipertrofik dekompansasyonun en güvenilir biyobelirtecidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Fetal Gen İndüksiyonu", "desc": "Doğumdan sonra susturulan embriyonik genlerin yeniden eksprese edilmesidir.", "isKey": True},
                    {"title": "ANP ve BNP Salgısı", "desc": "Ventrikül miyositleri natriüretik peptitler üreterek kan basıncını düşürmeye çalışır.", "isKey": True},
                    {"title": "Tanısal Biyobelirteç", "desc": "BNP düzeyi kalp yetmezliği ve duvar geriliminin klinik izleminde kullanılır.", "isKey": False}
                ],
                "table": {
                    "title": "Fetal Gen Programı Değişiklikleri",
                    "headers": ["Gen / Peptit", "Normal Erişkin Durumu", "Hipertrofik Kalp Durumu"],
                    "rows": [
                        ["ANP", "Yalnızca atriyumda düşük ekspresyon", "Ventrikül miyositlerinde yüksek ekspresyon"],
                        ["BNP", "Düşük bazal salınım", "Ventrikül gerildikçe kanda katlanarak artış"],
                        ["İskeletsel Alfa-Aktin", "Embriyonik dönemde aktif", "Erişkin hipertrofik kalpte yeniden aktif"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patolojik hipertrofide embriyonik fetal gen programı (ANP, BNP, fetal aktin) yeniden aktive olur.",
                "📌 [SINAV SPOTU] Ventriküllerden salgılanan BNP, kalp yetmezliği tanısı ve takibinde kullanılan altın standart biyobelirteçtir."
            ],
            "medicalTerms": [
                {"term": "ANP", "explanation": "Damar genişletici ve böbrekten sodyum atıcı etki gösteren atriyal natriüretik peptittir."},
                {"term": "BNP", "explanation": "Ventrikül duvar gerilimi arttığında miyositlerce kana verilen natriüretik peptittir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Sol ventrikül patolojik hipertrofisinde fetal gen programının yeniden aktivasyonu bağlamında, ventrikül miyositlerinden salınarak kanda düzeyi yükselen ve klinik yetmezlik takibinde kullanılan peptid hangisidir?",
                    {
                        "A": "Beyin Natriüretik Peptid (BNP)",
                        "B": "Troponin T",
                        "C": "Kreatin Kinaz MB",
                        "D": "Miyoglobin",
                        "E": "Laktat Dehidrogenaz"
                    },
                    "A",
                    {
                        "A": "Doğru: BNP duvar gerilimiyle indüklenen ve fetal reprogramlamayla ventrikülden salınan peptittir.",
                        "B": "Yanlış: Troponin miyosit nekrozunda kanda yükselir, fetal gen peptiti değildir.",
                        "C": "Yanlış: CK-MB nekroz enzim belirtecidir.",
                        "D": "Yanlış: Miyoglobin erken kas yıkım belirtecidir.",
                        "E": "Yanlış: LDH doku hasarında yükselen genel enzimdir."
                    }
                ),
                make_cloze(
                    "Ventrikül duvar geriliminin artması sonucu fetal gen aktivasyonuyla miyositlerden kana salınan temel peptit [BNP] olarak adlandırılır.",
                    "BNP",
                    "Beyin natriüretik peptit kısaltması"
                )
            ]
        },

        # Adım 23
        {
            "slideNumber": 23,
            "title": "Ağır Zincir İzoform Değişimi: Alfa-MHC'den Beta-MHC'ye Geçiş",
            "subtitle": "Kalp kası enerji tüketimini azaltmak için hızlı kasılan alfa miyozinden yavaş ve ekonomik beta izoformuna geçer.",
            "badge": "Enerji Ekonomisi",
            "badgeColor": "rose",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Kardiyak hipertrofide gözlenen moleküler adaptasyonun önemli bir diğer ayağı **miyozin ağır zincir (MHC) izoform değişimidir**. Erişkin ventrikül miyokardında normalde hızlı kasılan ve yüksek ATPaz aktivitesine sahip **alfa-MHC** baskındır.

Patolojik hipertrofide gen ekspresyonu değişerek fetal tip olan **beta-MHC** üretimi artar. Beta-MHC daha yavaş kasılır ancak ATP'yi çok daha ekonomik kullanır. Bu değişim kasılma hızını düşürse de oksijen açığı çeken hipertrofik miyositin enerji tüketimini azaltır.

> [TEMEL İLKE] Alfa-MHC'den beta-MHC'ye geçiş, hızdan feragat ederek enerji tasarrufu sağlayan metabolik bir adaptasyondur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Alfa-MHC", "desc": "Normal erişkinde baskındır; hızlı kasılma ve yüksek ATP tüketimi sağlar.", "isKey": True},
                    {"title": "Beta-MHC", "desc": "Fetal ve hipertrofik kalpte baskındır; yavaş kasılma ve düşük ATP tüketimi sağlar.", "isKey": True},
                    {"title": "Fonksiyonel Sonuç", "desc": "Kasılma kinetiği yavaşlar ancak birim iş için tüketilen oksijen azalır.", "isKey": False}
                ],
                "table": {
                    "title": "Miyozin Ağır Zincir İzoformlarının Karşılaştırması",
                    "headers": ["Parametre", "Alfa-MHC (Erişkin Tip)", "Beta-MHC (Fetal/Hipertrofik Tip)"],
                    "rows": [
                        ["ATPaz Aktivitesi", "Yüksek (hızlı ATP hidrolizi)", "Düşük (yavaş ATP hidrolizi)"],
                        ["Kasılma Hızı", "Hızlı ve dinamik", "Yavaş ve sürekli"],
                        ["Enerji Verimliliği", "Düşük enerji tasarrufu", "Yüksek enerji tasarrufu (daha ekonomik)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kardiyak hipertrofide hızlı alfa-MHC izoformundan yavaş ve enerji tasarruflu beta-MHC izoformuna geçiş olur.",
                "📌 [SINAV SPOTU] Beta-MHC geçişi fetal gen programının yeniden aktivasyonunun bir parçasıdır."
            ],
            "medicalTerms": [
                {"term": "Alfa-MHC", "explanation": "Erişkin kalpte hızlı kasılma sağlayan miyozin ağır zincir izoformudur."},
                {"term": "Beta-MHC", "explanation": "Enerji tasarrufu sağlayan, fetal ve hipertrofik kalpte baskınlaşan miyozin izoformudur."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Miyozin Ağır Zincir İzoform Değişimi",
                    "Normal Erişkin Ventrikül (Alfa-MHC)",
                    "Hipertrofik Ventrikül (Beta-MHC)",
                    [
                        "Hızlı kasılma mekaniği",
                        "Yüksek ATPaz aktivitesi",
                        "Birim zamanda yüksek enerji tüketimi"
                    ],
                    [
                        "Yavaş ve temkinli kasılma",
                        "Düşük ATPaz aktivitesi",
                        "Enerji tasarruflu ekonomik çalışma"
                    ]
                ),
                make_active_recall(
                    "Hipertrofik kardiyomiyositlerin alfa-MHC yerine beta-MHC eksprese etmesinin metabolik avantajı nedir?",
                    "Beta-MHC'nin ATPaz aktivitesi daha düşüktür; bu sayede kasılma kuvveti üretilirken daha az ATP ve oksijen harcanarak enerji tasarrufu sağlanır."
                )
            ]
        },

        # Adım 24
        {
            "slideNumber": 24,
            "title": "Miyokardiyal İskemi Riski: Kapiller Yatak ile Kas Hacmi Uyuşmazlığı",
            "subtitle": "Kas kütlesi katlanarak büyürken kapiller damar ağı aynı oranda genişleyemez; rölatif iskemi başlar.",
            "badge": "Vasküler Kısıtlılık",
            "badgeColor": "rose",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hipertrofinin en zayıf karnı vasküler beslenmedir. Hipertrofi sırasında kardiyomiyositlerin hacmi %50-100 oranında büyürken, koroner mikrodolaşımdaki **kapiller damar sayısı aynı hızda çoğalamaz**.

Sonuç olarak kapillerler arası mesafe açılır ve oksijenin miyositin merkezine difüzyon yolu uzar. Kalp kası belirgin biçimde kalınlaşmış olmasına rağmen ==rölatif iskemi== tehlikesiyle karşı karşıya kalır. Özellikle subendokardiyal tabaka hipoksiye son derece duyarlı hale gelir.

> [TEMEL İLKE] Kapiller anjiyogenezin miyosit hipertrofisine ayak uyduramaması, hipertrofik kalbin iskemi ve infarktüse yatkınlığının ana nedenidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Anjiyogenez Yetersizliği", "desc": "Kapiller damar artışı miyositlerin hacimsel büyümesinin çok gerisinde kalır.", "isKey": True},
                    {"title": "Difüzyon Mesafesi", "desc": "Kılcal damardan kas lifinin merkezine oksijen ulaşması zorlaşır.", "isKey": True},
                    {"title": "Subendokardiyal İskemi", "desc": "En yüksek intramural basınca sahip iç tabakalar ilk hasarlanan alandır.", "isKey": False}
                ],
                "table": {
                    "title": "Hipertrofide Vasküler Uyuşmazlık Dinamiği",
                    "headers": ["Parametre", "Normal Miyokard", "Hipertrofik Miyokard"],
                    "rows": [
                        ["Kapiller / Miyosit Oranı", "Yaklaşık 1:1 dengeli", "1:1 ancak miyosit hacmi 2 kat büyük"],
                        ["Difüzyon Yolu", "Kısa ve hızlı oksijen iletimi", "Uzantılı ve yetersiz oksijen difüzyonu"],
                        ["İskemi Eşiği", "Yüksek tolerans", "Düşük eforla dahi tetiklenen anjina riski"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hipertrofik kalpte koroner arterler açık olsa dahi kapiller yetersizlik nedeniyle rölatif iskemi gelişebilir.",
                "🚨 [KRİTİK UYARI] Kalınlaşan miyokardda ilk ve en ağır iskemiye uğrayan bölge subendokardiyal tabakadır."
            ],
            "medicalTerms": [
                {"term": "Rölatif İskemi", "explanation": "Damar tıkanıklığı olmaksızın aşırı artmış doku kütlesinin oksijen ihtiyacının karşılanamamasıdır."},
                {"term": "Subendokardiyum", "explanation": "Ventrikül boşluğunun hemen altındaki, sistolik basınca ve iskemiye en duyarlı miyokard katıdır."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Hipertansif kalp hastalığı olan bir hastada koroner anjiyografide epikardiyal damarlar açık olmasına rağmen göğüs ağrısı (anjina) tanımlanması senaryosu.",
                    [
                        {
                            "text": "Koronerler açık olduğuna göre ağrı tamamen psikolojiktir, tedaviye gerek yoktur.",
                            "isCorrect": False,
                            "feedback": "Hatalı! Hipertrofik kalpte kapiller difüzyon yetersizliği epikardiyal darlık olmadan da gerçek iskemi yapar."
                        },
                        {
                            "text": "Kalınlaşmış miyokard kütlesi ile kapiller yatak arasındaki uyuşmazlığa bağlı mikrovasküler rölatif iskemi düşünülür; kan basıncı kontrolü ve oksijen tüketimini azaltıcı tedavi planlanır.",
                            "isCorrect": True,
                            "feedback": "Kusursuz klinik patoloji değerlendirmesi! Miyosit hacmi kapillerleri aştığında mikrovasküler iskemi kaçınılmazdır."
                        },
                        {
                            "text": "Derhal açık kalp cerrahisi ile bypass yapılır.",
                            "isCorrect": False,
                            "feedback": "Yanlış! Tıkalı damar olmadan bypass yapılamaz."
                        }
                    ]
                ),
                make_cloze(
                    "Hipertrofik kalpte kapiller damar yoğunluğunun büyüyen miyosit hacmine yetersiz kalması sonucu dokuda [rölatif iskemi] gelişir.",
                    "rölatif iskemi",
                    "Oransal oksijen azlığı terimi"
                )
            ]
        },

        # Adım 25
        {
            "slideNumber": 25,
            "title": "Mitokondriyal Oksidatif Kapasitenin Sınırları ve ATP Tükenmesi",
            "subtitle": "Büyüyen miyositin metabolik enerji ihtiyacı mitokondrilerin ATP üretim kapasitesini aşar.",
            "badge": "Metabolik Çöküş",
            "badgeColor": "rose",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Miyokard hücresinin yaşamı ve kesintisiz kasılması yüksek miktarda **ATP üretimine** bağımlıdır. Hipertrofinin erken evresinde mitokondri sayısı artırılarak enerji talebi karşılanır.

Ancak hipertrofi ilerledikçe mitokondriyal biyogenez kütle artışına yetişemez. Oksidatif fosforilasyon kapasitesi doygunluğa ulaşır ve hücre içi serbest kalsiyumun sarkoplazmik retikuluma geri pompalanması (SERCA2a pompası) için gereken ATP miktarı yetersiz kalır. Enerji açığı gevşeme kusuruna (diyastolik disfonksiyon) yol açar.

> [TEMEL İLKE] Enerji krizi hipertrofik kalbin kompanse fazdan dekompanse kalp yetmezliği fazına geçişindeki ana metabolik dönüm noktasıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "ATP Açığı", "desc": "Mitokondrilerin maksimum ATP üretim hızı dev kütlenin tüketimini karşılayamaz.", "isKey": True},
                    {"title": "Kalsiyum Pompa Yetmezliği", "desc": "SERCA pompasının ATP azlığı nedeniyle yavaşlaması gevşemeyi bozar.", "isKey": True},
                    {"title": "Diyastolik Disfonksiyon", "desc": "Sertleşen ve gevşeyemeyen ventrikül diyastolde yeterince kanla dolamaz.", "isKey": False}
                ],
                "table": {
                    "title": "Hipertrofide Enerji Metabolizması Aşamaları",
                    "headers": ["Evre", "Mitokondriyal Durum", "Metabolik Sonuç"],
                    "rows": [
                        ["Erken Kompanse", "Yeterli mitokondriyal çoğalma", "ATP ihtiyacı tam karşılanır"],
                        ["İleri Hipertrofik", "Mitokondri / Miyofibril dengesizliği", "Rölatif ATP düşüşü, laktat artışı"],
                        ["Dekompansasyon", "Mitokondriyal krista hasarı", "Ağır enerji tükenmesi ve kasılma yetmezliği"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hipertrofik kalpte ATP tükenmesinin ilk fonksiyonel sonucu diyastolik gevşeme bozukluğudur.",
                "📌 [SINAV SPOTU] SERCA2a kalsiyum pompasının aktivite kaybı miyosit içi serbest kalsiyumun temizlenmesini geciktirir."
            ],
            "medicalTerms": [
                {"term": "SERCA2a", "explanation": "Kas gevşemesi için kalsiyumu sitoplazmadan sarkoplazmik retikuluma geri pompalayan ATPazdır."},
                {"term": "Diyastolik Disfonksiyon", "explanation": "Miyokardın sertleşmesi ve gevşeyememesi sonucu ventrikül doluşunun bozulmasıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Metabolik Enerji Tükenmesi ve Fonksiyonel Çöküş",
                    [
                        "1. Kütle Büyümesi: Miyosit hacminin ve kasılma proteini sayısının aşırı artışı.",
                        "2. Mitokondri Sınırı: Oksidatif fosforilasyonun maksimum üretim kapasitesine ulaşması.",
                        "3. ATP Açığı: Hücre içi ATP/ADP oranının düşmesi ve enerji krizinin başlaması.",
                        "4. Pompa Yavaşlaması: SERCA2a pompasının kalsiyumu geri çekememesi ve gevşeme kusuru.",
                        "5. Dekompansasyon: Miyofibrillerin lizisi ve kasılma gücünün gerilemesi."
                    ]
                ),
                make_active_recall(
                    "Kardiyak hipertrofide ATP yetersizliği geliştiğinde ilk bozulan fonksiyon neden sistol (kasılma) değil diyastol (gevşeme) olur?",
                    "Çünkü kalsiyumun sitoplazmadan sarkoplazmik retikuluma geri pompalanması aktif ATP harcayan bir süreçtir; enerji azaldığında miyosit gevşeyemez ve diyastolik sertlik gelişir."
                )
            ]
        },

        # Adım 26
        {
            "slideNumber": 26,
            "title": "Miyosit Apoptozu ve Fokal Fibrozis Gelişimi",
            "subtitle": "Kalıcı stres altındaki miyositler ölmeye başlar; ölen hücrelerin yerini tamir dokusu (fibrozis) alır.",
            "badge": "Hücresel Kayıp",
            "badgeColor": "rose",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hipertrofinin sınırları aşıldığında ve kronik stres sürdüğünde, hücreler artık adaptasyonu koruyamaz. İskemi, enerji açığı ve oksidatif stres miyositlerde **apoptoz** ve **nekrozu** tetikler.

Kardiyomiyositler bölünemediğinden kaybedilen hücrelerin yerine yenisi üretilemez. Hasarlı alanlar fibroblastlar tarafından **interstisyel ve perivasküler fibrozis** (kollajen birikimi) ile doldurulur. Fibrozis miyokardı daha da sertleştirir ve elektriksel iletimi bozarak öldürücü aritmilere zemin hazırlar.

> [TEMEL İLKE] Hipertrofik miyokardda miyosit kaybı ve fibrozisin başlaması adaptasyonun çöktüğünün ve yetmezliğin başladığının göstergesidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Miyosit Ölümü", "desc": "Enerji krizine ve hipoksiye dayanamayan miyositler apoptozla yok olur.", "isKey": True},
                    {"title": "Onarıcı Fibrozis", "desc": "Ölen kas hücrelerinin yeri bölünemeyen dokuda bağ dokusu skarıyla doldurulur.", "isKey": True},
                    {"title": "Aritmi Zemini", "desc": "Miyokard arasına giren kollajen lifler re-entry aritmilerine neden olur.", "isKey": False}
                ],
                "table": {
                    "title": "Hipertrofide Miyosit Kaybı ve Sonuçları",
                    "headers": ["Aşama", "Histopatolojik Görünüm", "Klinik Yansıma"],
                    "rows": [
                        ["Hücre Ölümü", "Kromatin yoğunlaşması, apoptoz cisimcikleri", "Troponin sızıntısı"],
                        ["İnterstisyel Fibrozis", "Kardiyomiyositler arasında kollajen birikimi", "Ventrikül sertliği ve doluş bozukluğu"],
                        ["İleti Anomalisi", "Elektriksel homojenliğin bozulması", "Ventriküler taşikardi ve ani ölüm riski"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Patolojik hipertrofinin dekompansasyon evresinde kardiyomiyosit ölümü ve interstisyel fibrozis gelişir.",
                "🚨 [KRİTİK UYARI] Fibrotik doku elektriği iletmez; bu durum hipertrofik kalp hastalarında ani kardiyak ölümün temel nedenidir."
            ],
            "medicalTerms": [
                {"term": "İnterstisyel Fibrozis", "explanation": "Parankim hücreleri arasında aşırı fibröz bağ dokusu ve kollajen birikmesidir."},
                {"term": "Re-entry Aritmisi", "explanation": "Skar dokusu etrafında elektriksel uyarının kısır döngüye girerek taşikardi üretmesidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Hipertansif kalp hastalığının ilerleyen dönemlerinde sol ventrikül miyokardında miyosit kaybı sonrası gelişen ve ani kardiyak ölüm riskini artıran patolojik değişiklik hangisidir?",
                    {
                        "A": "İnterstisyel ve perivasküler fibrozis",
                        "B": "Akut lökositik infiltrasyon ve apse",
                        "C": "Kazeifiye granülom oluşumu",
                        "D": "Skuamöz metaplazi gelişimi",
                        "E": "Tümöral rabdomiyom infiltrasyonu"
                    },
                    "A",
                    {
                        "A": "Doğru: Kaybedilen miyositlerin yerini alan bağ dokusu skarı (fibrozis) iletiyi bozar ve aritmi yapar.",
                        "B": "Yanlış: Apse bakteriyel süpüratif enfeksiyonlarda görülür.",
                        "C": "Yanlış: Kazeifikasyon tüberküloza özgüdür.",
                        "D": "Yanlış: Kalp kasında metaplazi görülmez.",
                        "E": "Yanlış: Rabdomiyom benign neoplazidir, hipertansiyon sonucu değildir."
                    }
                ),
                make_cloze(
                    "Hipertrofik kalpte ölen kas liflerinin yerinin kollajen bağ dokusu ile doldurulmasına interstisyel [fibrozis] adı verilir.",
                    "fibrozis",
                    "Bağ dokusu artışı süreci"
                )
            ]
        },

        # Adım 27
        {
            "slideNumber": 27,
            "title": "Kompansatuvardan Dekompansatuvar Faz: Ventriküler Dilatasyon",
            "subtitle": "Kas liflerinin tükenmesiyle kalın ventrikül duvarı incelir, kalp boşluğu genişler ve kalp yetmezliği tablosu oturur.",
            "badge": "Yetmezlik Dönemi",
            "badgeColor": "rose",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patolojik hipertrofinin son trajik evresi **dekompansasyon ve ventriküler dilatasyondur**. Miyosit ölümü, miyofibril lizisi ve fibrozis birikimi kritik bir eşiğe ulaştığında ventrikül artık yüksek basınca direnemez.

Konsantrik olarak kalınlaşmış olan duvar gevşer, incelir ve ventrikül boşluğu dışa doğru balonlaşarak ==dilatasyona== uğrar. Kalbin kasılma gücü (ejeksiyon fraksiyonu) hızla düşer. Bu aşamada tablo geri dönüşsüz **konjestif kalp yetmezliğine** dönüşmüştür.

> [TEMEL İLKE] Konsantrik hipertrofinin dilatasyona dönmesi, kalbin mekanik adaptasyonunun çöktüğünü ve organ yetmezliğinin başladığını simgeler.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Miyofibril Kaybı", "desc": "Kas lifleri içindeki aktin ve miyozin proteinleri parçalanır.", "isKey": True},
                    {"title": "Kavite Dilatasyonu", "desc": "Daralmış olan ventrikül lümeni aşırı genişler ve duvar incelir.", "isKey": True},
                    {"title": "Pompa İflası", "desc": "Ejeksiyon fraksiyonu düşerek konjestif kalp yetmezliği gelişir.", "isKey": False}
                ],
                "table": {
                    "title": "Kompanse Hipertrofi vs Dekompanse Dilatasyon",
                    "headers": ["Parametre", "Kompanse Evre (Hipertrofi)", "Dekompanse Evre (Dilatasyon)"],
                    "rows": [
                        ["Ventrikül Duvarı", "Kalın (>2 cm, konsantrik)", "Göreceli incelmiş ve gevşek"],
                        ["Ventrikül Boşluğu", "Normal veya daralmış", "Genişlemiş ve balonlaşmış (dilatasyon)"],
                        ["Klinik Durum", "Asemptomatik veya hafif efor dispnesi", "Konjestif kalp yetmezliği, akciğer ödemi"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kalp hipertrofisinde dekompansasyonun en belirgin morfolojik bulgusu ventriküler dilatasyondur.",
                "🚨 [KRİTİK UYARI] Dilatasyon evresine geçen bir kalpte ejeksiyon fraksiyonu düşer ve geriye dönüş şansı son derece kısıtlıdır."
            ],
            "medicalTerms": [
                {"term": "Ventriküler Dilatasyon", "explanation": "Ventrikül boşluğunun kas zayıflığı nedeniyle anormal derecede genişlemesidir."},
                {"term": "Ejeksiyon Fraksiyonu", "explanation": "Sol ventrikülün her atımda içindeki kanın pompalayabildiği yüzdesidir (normal >%50-55)."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Kompanse Hipertrofi ile Dekompanse Dilatasyon Karşılaştırması",
                    "Kompanse Faz (Konsantrik Hipertrofi)",
                    "Dekompanse Faz (Kardiyak Dilatasyon)",
                    [
                        "Duvar kalınlığı 2 cm üzerinde",
                        "Ventrikül lümeni daralmış",
                        "Ejeksiyon fraksiyonu korunmuş"
                    ],
                    [
                        "Duvar incelmiş ve gevşemiş",
                        "Ventrikül lümeni aşırı genişlemiş",
                        "Ejeksiyon fraksiyonu ağır düşmüş"
                    ]
                ),
                make_cloze(
                    "Miyokard hipertrofisinin sınırları tükendiğinde ventrikül boşluğunun patolojik olarak genişlemesine ventriküler [dilatasyon] adı verilir.",
                    "dilatasyon",
                    "Lümen genişlemesi terimi"
                )
            ]
        },

        # Adım 28
        {
            "slideNumber": 28,
            "title": "İskemik Koagülatif Nekroz ve TTC (Trifeniltetrazolyum Klorür) Boyaması",
            "subtitle": "Aşırı hipertrofiye uğramış miyokardda kan akımının kesilmesi koagülasyon nekrozu (enfarktüs) ile sonuçlanır.",
            "badge": "Tanısal Histokimya",
            "badgeColor": "rose",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hipertrofik kalp kasında gelişen ağır iskemi geri dönüşsüz safhaya geçtiğinde miyositler ölür ve **koagülasyon nekrozu** (miyokard enfarktüsü) şekillenir.

Otopside erken enfarktüs alanlarını makroskopik olarak tespit etmek için **TTC (Trifeniltetrazolyum Klorür)** boyası kullanılır. TTC, canlı hücrelerdeki aktif laktat dehidrogenaz (LDH) enzimiyle reaksiyona girerek dokuyu **parlak tuğla kırmızısı (magenta)** renge boyar. Nekroze olmuş alanda enzimler hücre dışına sızıp kaybolduğundan nekrotik alan **soluk, boyanmamış** kalır.

> [KLİNİK İPUCU] TTC boyamasında boyanmayan soluk alanlar, enzim aktivitesini kaybetmiş taze nekrotik miyokardı kesin olarak gösterir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Koagülasyon Nekrozu", "desc": "İskemiye bağlı protein denatürasyonuyla şekillenen temel doku ölümüdür.", "isKey": True},
                    {"title": "TTC Reaksiyonu", "desc": "Canlı miyositlerdeki dehidrogenaz enzimleri TTC'yi kırmızı formazana çevirir.", "isKey": True},
                    {"title": "Nekrotik Alan", "desc": "Ölü hücrelerde enzim kaybı olduğu için TTC boyanması olmaz; soluk izlenir.", "isKey": False}
                ],
                "table": {
                    "title": "TTC Boyamasında Dokuların Görünümü",
                    "headers": ["Doku Durumu", "Enzim Durumu (LDH)", "TTC Makroskobik Rengi"],
                    "rows": [
                        ["Canlı Sağlam Miyokard", "İntakt dehidrogenaz enzimleri", "Canlı tuğla kırmızısı / magenta"],
                        ["İskemik Nekrotik Miyokard", "Hücre dışına sızmış, kayıp enzimler", "Soluk, grimsi-beyaz (boyanmaz)"],
                        ["Eski Fibröz Skar", "Bağ dokusu (enzim yok)", "Sedefsi beyaz kollajen alanı"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] TTC boyası taze miyokard enfarktüsünü makroskopik olarak saptamak için kullanılır.",
                "📌 [SINAV SPOTU] Canlı miyokard TTC ile kırmızıya (magenta) boyanırken; nekrotik enfarktüs alanı boyanmaz, soluk kalır."
            ],
            "medicalTerms": [
                {"term": "TTC Boyası", "explanation": "Hücresel dehidrogenaz enzim aktivitesine duyarlı makroskobik canlılık boyasıdır."},
                {"term": "Koagülasyon Nekrozu", "explanation": "İskemi sonucu hücre iskeletinin korunup proteinlerin pıhtılaşmasıyla oluşan nekrozdur."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Otopside taze miyokard enfarktüsü şüphesi olan bir kalbe uygulanan TTC (Trifeniltetrazolyum klorür) boyamasında nekrotik alanın boyanmayıp soluk kalmasının biyokimyasal temeli nedir?",
                    {
                        "A": "Ölü kardiyomiyositlerde membran hasarı sonucu dehidrogenaz enzimlerinin dışarı sızıp kaybolması",
                        "B": "Ölü alanda aşırı miktarda hemoglobin sentezlenmesi",
                        "C": "Nekrotik alanda glikojen depolarının aşırı artması",
                        "D": "Ölü hücrelerde nükleusun parçalanmadan devleşmesi",
                        "E": "TTC boyasının yalnızca yağ hücrelerine bağlanması"
                    },
                    "A",
                    {
                        "A": "Doğru: Canlı hücrede LDH enzimi TTC'yi kırmızıya boyar; nekrotik alanda enzim kaybı olduğundan soluk kalır.",
                        "B": "Yanlış: Miyokardda hemoglobin sentezlenmez.",
                        "C": "Yanlış: İskemide glikojen depoları tükenir.",
                        "D": "Yanlış: Nükleus piknoz ve lizise uğrar.",
                        "E": "Yanlış: TTC enzim aktivite boyasıdır, lipid boyası değildir."
                    }
                ),
                make_cloze(
                    "Taze miyokard enfarktüsü alanlarını saptamakta kullanılan TTC boyamasında canlı doku kırmızı boyanırken nekrotik alan [soluk] kalır.",
                    "soluk",
                    "Boyanmayan alan rengi"
                )
            ]
        },

        # Adım 29 (CHECKPOINT 3)
        {
            "slideNumber": 29,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Patolojik Hipertrofi ve Kalp Yetmezliği",
            "subtitle": "Kardiyak hipertrofinin hemodinamik tetikleyicilerini, moleküler izoform değişimlerini ve dilatasyon sürecini pekiştirin.",
            "badge": "Tekrar Sayfası",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 3,
            "synthesisNarrative": """Bu bölümde patolojik kardiyak hipertrofinin hemodinamik nedenlerini, moleküler mekanizmalarını ve kalp yetmezliğine gidiş basamaklarını inceledik.

Hipertansiyon ve aort darlığı sol ventrikülde konsantrik hipertrofiye (>2 cm duvar kalınlığı) neden olur. Fetal gen programı açılarak BNP salınır ve alfa-MHC'den beta-MHC'ye enerji tasarruflu geçiş yapılır. Ancak kapiller yetersizlik, ATP açığı ve miyosit apoptozu adaptasyonu aşar; dokuda fibrozis ve ventriküler dilatasyon gelişerek kalp yetmezliği oturur.

> [TEKRAR SPOTU] Konsantrik hipertrofi duvar stresini azaltmaya çalışır; ancak vasküler ve metabolik sınır aşıldığında dilatasyon ve iflas kaçınılmazdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Morfometrik Kriter", "desc": "Sol ventrikül duvar kalınlığının 2 cm'yi, kalp ağırlığının 500 gramı aşmasıdır.", "isKey": True},
                    {"title": "Moleküler İmzalar", "desc": "BNP salınımı, fetal reprogramlama ve beta-MHC izoformuna geçiştir.", "isKey": True},
                    {"title": "Terminal Evre", "desc": "İnterstisyel fibrozis, ventriküler dilatasyon ve ejeksiyon fraksiyonu çöküşüdür.", "isKey": False}
                ],
                "table": {
                    "title": "Bölüm 3 Sentez Tablosu",
                    "headers": ["Evre", "Morfoloji", "Moleküler / Klinik Belirteç"],
                    "rows": [
                        ["Erken Konsantrik", "Duvar > 2 cm, dar lümen", "BNP salınımı, beta-MHC aktivasyonu"],
                        ["Mikrovasküler İskemi", "Subendokardiyal hipoksi", "Kapiller/lif uyuşmazlığı, rölatif iskemi"],
                        ["Son Dönem İflas", "Ventriküler dilatasyon, fibrozis", "Konjestif kalp yetmezliği, aritmi riski"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Sol ventrikül duvar kalınlığı >2 cm konsantrik patolojik hipertrofinin tipik ölçütüdür.",
                "📌 [SINAV SPOTU] TTC boyamasında canlı miyokard kırmızıya boyanırken enfarktüslü nekrotik doku boyanmayıp soluk kalır."
            ],
            "medicalTerms": [
                {"term": "Konsantrik Hipertrofi", "explanation": "Basınç yüküne bağlı olarak ventrikül boşluğu genişlemeden duvarın kalınlaşmasıdır."},
                {"term": "Ventriküler Dilatasyon", "explanation": "Kas gücünün tükenmesiyle ventrikül boşluğunun anormal genişlemesidir."}
            ],
            "flashcards": [
                make_flashcard(
                    "k1-03-fc07",
                    "Hipertansiyonda gelişen konsantrik sol ventrikül hipertrofisinin makroskobik ölçütleri nelerdir?",
                    "Sol ventrikül serbest duvar kalınlığının 2 cm'nin üzerine çıkması ve kalp ağırlığının 500 gramı aşmasıdır."
                ),
                make_flashcard(
                    "k1-03-fc08",
                    "Hipertrofik kardiyomiyositlerde gözlenen 'fetal gen programına geri dönüş' ne anlama gelir?",
                    "Doğumdan sonra susturulan embriyonik genlerin (ANP, BNP, beta-MHC, fetal aktin) yeniden aktive olarak kana salınması ve enerji tasarrufu sağlamasıdır."
                ),
                make_flashcard(
                    "k1-03-fc09",
                    "TTC (Trifeniltetrazolyum klorür) boyaması otopside taze miyokard enfarktüsünü nasıl ayırt eder?",
                    "Canlı miyokarddaki dehidrogenaz enzimleri TTC'yi tuğla kırmızısına (magenta) boyar; nekrotik alanda enzim kaybı olduğundan doku boyanmaz ve soluk kalır."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Patolojik kardiyak hipertrofide koroner arterler açık olmasına rağmen neden anjina ve miyokardiyal iskemi gelişebilir?",
                    "Çünkü miyosit hacmi katlanarak büyürken kapiller damar sayısı aynı oranda artamaz; kılcal damarlar arası mesafe açılarak dokuda rölatif iskemi oluşur."
                )
            ]
        }
    ]
