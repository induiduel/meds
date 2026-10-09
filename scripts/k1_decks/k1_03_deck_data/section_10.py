#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Section 10: Adaptasyonun Sınırları, Geri Dönüşsüz Hücre Hasarına Geçiş ve Büyük Sentez (Adımlar 90 - 100)
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
        # Adım 90
        {
            "slideNumber": 90,
            "title": "Adaptasyon ile Hücre Hasarı Arasındaki Dinamik Sınır",
            "subtitle": "Stresin şiddeti veya süresi hücrenin adaptif kapasitesini aştığında süreç kaçınılmaz olarak hasara kayar.",
            "badge": "Patolojik Eşik",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hücresel adaptasyon sonsuz bir kapasiteye sahip değildir; her hücre tipinin genetik ve metabolik olarak belirlenmiş bir **adaptif sınırı** vardır.

Stresin şiddeti hafif ve tolere edilebilir düzeyde kaldığı sürece hücre yeni bir kararlı durumda (hipertrofi, atrofi, hiperplazi, metaplazi) canlılığını korur. Ancak uyaranın dozu aniden artarsa veya süre gereğinden fazla uzarsa bu koruyucu kalkan çöker. Hücre adaptasyon fazından çıkarak önce **geri dönüşümlü hücre hasarına**, ardından geri dönüşsüz ölüme sürüklenir.

> [TEMEL İLKE] Adaptasyon ile hasar arasındaki sınır durağan değildir; stresin şiddeti, süresi ve hücrenin beslenme rezerviyle belirlenir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Adaptif Kapasite", "desc": "Hücrenin yapısal protein ve enerji sentez sınırları adaptasyon tavanını belirler.", "isKey": True},
                    {"title": "Eşik Aşımı", "desc": "Stres sınırı aştığında hücre fonksiyonu bozulur ve hasar morfolojisi belirir.", "isKey": True},
                    {"title": "Spektrum Geçişi", "desc": "Adaptasyon -> Geri dönüşümlü hasar -> Nekroz/Apoptoz geçişi dinamiktir.", "isKey": False}
                ],
                "table": {
                    "title": "Hücresel Durumlar Arasındaki Geçiş Eşikleri",
                    "headers": ["Evre", "Morfolojik Durum", "Metabolik Karşılık"],
                    "rows": [
                        ["Adaptasyon", "Boyut, sayı veya fenotip değişimi", "Yeni dengede kararlı enerji üretimi"],
                        ["Geri Dönüşümlü Hasar", "Bulanık şişme, yağlanma, vakuolizasyon", "ATP pompalarında geçici aksama"],
                        ["Geri Dönüşsüz Ölüm", "Membran parçalanması, piknoz, lizis", "Tam ATP tükenmesi ve kalsiyum seli"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücresel stres adaptasyon sınırını aştığında süreç hücre hasarına ve ölüme ilerler.",
                "📌 [SINAV SPOTU] Stresin süresi ve dozu, adaptasyondan ölüme uzanan spektrumun temel belirleyicisidir."
            ],
            "medicalTerms": [
                {"term": "Adaptif Kapasite", "explanation": "Hücrenin hasar görmeden yeni bir denge kurabilme gücü ve sınırıdır."},
                {"term": "Hücresel Hasar", "explanation": "Hücrenin adaptasyon sınırını aşan stresler sonucu yapısal ve fonksiyonel bütünlüğünün bozulmasıdır."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "Adaptasyondan Hasara Geçiş Kaskadı",
                    [
                        "1. Tolere Edilebilir Stres: Hücrenin hipertrofi veya atrofi ile yeni denge kurması.",
                        "2. Stresin Artması: Kan akımının daha da azalması veya basınç yükünün tırmanması.",
                        "3. Rezerv Tükenmesi: Biyosentetik ve mitokondriyal kapasitenin doygunluğa ulaşması.",
                        "4. Geri Dönüşümlü Hasar: Membran pompalarının yavaşlaması ve hücresel şişme.",
                        "5. Terminal Hasar: Membran bütünlüğü kaybıyla geri dönüşsüz nekroz gelişimi."
                    ]
                ),
                make_cloze(
                    "Stresin şiddeti hücrenin [adaptif kapasitesini] aştığında hücre adaptasyon evresinden hasar evresine geçer.",
                    "adaptif kapasitesini",
                    "Hücrenin uyum sınırı tamlaması"
                )
            ]
        },

        # Adım 91
        {
            "slideNumber": 91,
            "title": "Doz-Süre İlişkisi: Aynı Uyaranın Adaptasyondan Ölüme Uzanan Spektrumu",
            "subtitle": "Aynı etiyolojik ajan doza ve süreye bağlı olarak adaptasyon, hasar veya ölüm oluşturur.",
            "badge": "Dinamik Spektrum",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Patolojide hiçbir lezyon tek başına etiyolojik ajanın adıyla tanımlanamaz; **maruziyetin dozu ve süresi** tablonun niteliğini baştan sona değiştirir.

Örneğin koroner iskemi ele alındığında: Yıllar süren yavaş ve kısmi kan akımı azalması kardiyomiyositlerde **iskemik atrofi** doğurur. Efor sırasında gelişen birkaç dakikalık geçici hipoksi **geri dönüşümlü anjina ve hücresel şişme** yapar. Arterin aniden tam tıkanması ise 20-30 dakika içinde **geri dönüşsüz nekroz (miyokard enfarktüsü)** ile sonuçlanır.

> [TEMEL İLKE] Aynı hastalık nedeni (iskemi, basınç, toksin); düşük dozda adaptasyon, yüksek dozda ölüm oluşturur.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Doz Etkisi", "desc": "Hafif uyaran adaptasyonu uyarırken, masif uyaran doğrudan hücreyi öldürür.", "isKey": True},
                    {"title": "Süre Etkisi", "desc": "Kısa süreli hasar geri dönerken, uzayan kalıcı hasar geri dönüşsüz ölüme gider.", "isKey": True},
                    {"title": "İskemi Modeli", "desc": "Yavaş darlık = Atrofi; geçici darlık = Şişme; tam tıkanma = Nekroz.", "isKey": False}
                ],
                "table": {
                    "title": "İskemi Doz ve Süresine Göre Hücresel Yanıt",
                    "headers": ["İskemik Maruziyet", "Hücresel Yanıt", "Morfolojik / Klinik Tablo"],
                    "rows": [
                        ["Kronik Kısmi İskemi", "Adaptasyon", "İskemik Atrofi (küçülmüş miyositler)"],
                        ["Akut Geçici İskemi (<20 dk)", "Geri Dönüşümlü Hasar", "Hücresel şişme, anjina pektoris"],
                        ["Akut Kalıcı İskemi (>20-30 dk)", "Geri Dönüşsüz Hücre Ölümü", "Akut Miyokard Enfarktüsü (Koagülasyon nekrozu)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Yavaş kronik iskemi atrofi (adaptasyon); akut tam iskemi nekroz (ölüm) yapar.",
                "📌 [SINAV SPOTU] Miyokard iskemisinde geri dönüşsüz hasar eşiği yaklaşık 20-30 dakikadır."
            ],
            "medicalTerms": [
                {"term": "Doz-Süre Bağımlılığı", "explanation": "Hücresel yanıtın zararlı etkenin konsantrasyonu ve temas süresiyle doğrudan belirlenmesidir."},
                {"term": "İskemi Eşiği", "explanation": "Bir dokunun geri dönüşsüz hasara uğramadan kansızlığa dayanabildiği maksimum süredir."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Kronik Kısmi İskemi ile Akut Tam İskemi Karşılaştırması",
                    "Kronik Kısmi İskemi (Ateroskleroz)",
                    "Akut Tam İskemi (Koroner Tromboz)",
                    [
                        "Yıllar içinde yavaş gelişir",
                        "Hücre küçülerek hayatta kalır (Atrofi)",
                        "Canlılık ve bazal metabolizma korunur"
                    ],
                    [
                        "Dakikalar içinde aniden gelişir",
                        "20-30 dakikada nekroz başlar (Enfarktüs)",
                        "Membran rüptürü ve hücre ölümü kaçınılmazdır"
                    ]
                ),
                make_cloze(
                    "Miyokard dokusunda akut tam iskemi durumunda geri dönüşsüz hücre ölümü yaklaşık [20-30] dakika içinde başlar.",
                    "20-30",
                    "Dakika aralığı rakamı"
                )
            ]
        },

        # Adım 92
        {
            "slideNumber": 92,
            "title": "Biyosentetik ve Vasküler Rezerv Sınırları Aşıldığında Ne Olur?",
            "subtitle": "Hücrenin protein sentez hızı ve kapiller beslenme kapasitesi tükendiğinde dekompansasyon başlar.",
            "badge": "Rezerv Tükenmesi",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Hipertrofiye uğrayan bir organın iflas etmesindeki temel kısıt **biyosentetik ve vasküler tavan sınırlarıdır**.

Hücre ne kadar büyürse büyüsün, tek bir çekirdeğin DNA transkripsiyon kapasitesi ve ribozomal translasyon hızı sonsuz değildir. Kas lifi kalınlaştıkça merkezdeki proteinlerin beslenmesi ve yenilenmesi gecikir. Eşzamanlı olarak koroner kılcal damar sayısı kas kütlesine yetişemez. Rezervler bittiğinde organ hipertrofiden **dekompansatuvar dilatasyona** kayar.

> [TEMEL İLKE] Bir hücrenin adaptif büyümesi, biyosentetik aparatının ve vasküler lojistiğinin sınırlarıyla kayıtlıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Çekirdek Kapasitesi", "desc": "Tek çekirdeğin kontrol edebileceği maksimum sitoplazma hacmi sınırlıdır.", "isKey": True},
                    {"title": "Vasküler Uçurum", "desc": "Kapiller difüzyon mesafesinin aşılması hücresel hipoksi yaratır.", "isKey": True},
                    {"title": "Dekompansasyon", "desc": "Artık yeni sarkomer üretilemez; var olanlar parçalanır ve yetmezlik başlar.", "isKey": False}
                ],
                "table": {
                    "title": "Kardiyak Hipertrofide Rezerv Tükenmesi Evreleri",
                    "headers": ["Evre", "Vasküler Durum", "Biyosentetik Durum"],
                    "rows": [
                        ["Fizyolojik / Erken", "Yeterli anjiyogenez ve difüzyon", "Dengeli ve aktif protein sentezi"],
                        ["İleri Konsantrik", "Rölatif mikrovasküler yetersizlik", "Mitokondri ve translasyon sınırında"],
                        ["Dekompanse Dilatasyon", "Ağır subendokardiyal iskemi", "Miyofibril lizisi ve protein yıkımı baskın"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hipertrofik kalpte yetmezliğe geçişin iki ana nedeni vasküler beslenme yetersizliği ve mitokondriyal ATP açığıdır.",
                "🚨 [KRİTİK UYARI] Biyosentetik sınır aşıldığında kasılma proteinleri üretilemez ve ventrikül duvarı incelip genişler."
            ],
            "medicalTerms": [
                {"term": "Nükleositoplazmik Oran", "explanation": "Hücre çekirdeğinin yönetebileceği sitoplazma hacmi arasındaki orandır."},
                {"term": "Vasküler Lojistik", "explanation": "Doku kütlesine oksijen ve glukoz taşıyan kapiller damar ağının yeterliliğidir."}
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kalp kası hücresinin hipertrofi sırasında sonsuza kadar büyüyememesini ve eninde sonunda yetmezliğe girmesini belirleyen iki temel biyolojik kısıt nedir?",
                    "1) Kapiller damar artışının kas hacmine yetişememesi sonucu oluşan mikrovasküler iskemi, 2) Mitokondriyal ATP üretiminin ve çekirdeğin protein sentez kapasitesinin tükenmesidir."
                ),
                make_cloze(
                    "Hipertrofik kas dokusunda kapiller damar yoğunluğunun devasa kas kütlesine yetersiz kalması sonucu dokuda [rölatif] iskemi gelişir.",
                    "rölatif",
                    "Oransal yetersizlik sıfatı"
                )
            ]
        },

        # Adım 93
        {
            "slideNumber": 93,
            "title": "Geri Dönüşümlü Hücre Hasarı: Hücresel Şişme (Hidropik Dejenerasyon) ve Yağlanma",
            "subtitle": "Adaptasyon sınırını aşan erken hasarın iki temel morfolojik kanıtı hücresel şişme ve yağ birikimidir.",
            "badge": "Erken Hasar",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Adaptasyon yetersiz kaldığında hücrenin girdiği ilk hasar safhası **geri dönüşümlü hücre hasarıdır**. Bu evrenin iki temel morfolojik görünümü vardır: **Hücresel Şişme (Bulanık Şişme / Hidropik Dejenerasyon)** ve **Yağlanma (Steatoz)**.

Hücresel şişme, ATP üretiminin düşmesi sonucu plazma membranındaki enerji bağımlı **Na+/K+ ATPaz pompasının** iflas etmesiyle başlar. Hücre dışarı sodyum atamaz; hücre içinde biriken sodyum ozmotik olarak suyu içeri çeker. Hücre şişer, endoplazmik retikulum genişler ve sitoplazmada berrak vakuoller belirir. Yağlanma ise özellikle karaciğer ve miyokardda lipid metabolizmasının bozulmasıyla gelişir.

> [TEMEL İLKE] Hücresel şişme hasarın en erken ve en sık görülen morfolojik bulgusudur; uyaran kalkarsa hücre tamamen normale döner.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Hücresel Şişme", "desc": "Na+/K+ pompası durunca sodyum ve suyun hücre içine hücum etmesidir.", "isKey": True},
                    {"title": "Hidropik Dejenerasyon", "desc": "Genişlemiş endoplazmik retikulum vakuollerinin sitoplazmayı doldurmasıdır.", "isKey": True},
                    {"title": "Yağlanma (Steatoz)", "desc": "Toksin veya hipoksiyle yağ metabolizmasının aksayıp trigiserid birikmesidir.", "isKey": False}
                ],
                "table": {
                    "title": "Geri Dönüşümlü Hasarın Temel Bulguları",
                    "headers": ["Bulgu", "Biyokimyasal Neden", "Mikroskobik Görünüm"],
                    "rows": [
                        ["Hücresel Şişme", "Na+/K+ ATPaz pompa yetersizliği", "Soluk, geniş sitoplazma, mikrovakuoller"],
                        ["Plazma Membran Kabarcıkları", "Hücre iskeletinin ayrışması", "Membranda dışa doğru tomurcuklar (blebs)"],
                        ["Yağlanma", "Trigliserit sentez ve atım kusuru", "Sitoplazmada lipid vakuolleri (steatoz)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hücre hasarının ilk ve en erken morfolojik bulgusu hücresel şişmedir (hidropik dejenerasyon).",
                "📌 [SINAV SPOTU] Hücresel şişmenin temel nedeni ATP düşüşüne bağlı Na+/K+ ATPaz pompasının bozulmasıdır."
            ],
            "medicalTerms": [
                {"term": "Hidropik Dejenerasyon", "explanation": "İyon pompalarının durmasıyla hücre içine su girip berrak vakuoller oluşturmasıdır."},
                {"term": "Steatoz", "explanation": "Parankim hücreleri (özellikle hepatositler) içinde anormal trigliserit birikimidir."}
            ],
            "interactiveElements": [
                make_causal_chain(
                    "İskemi Sonrası Hücresel Şişme Kaskadı",
                    [
                        "1. Hipoksi: Oksijen azlığıyla mitokondriyal oksidatif fosforilasyonun durması.",
                        "2. ATP Düşüşü: Hücresel enerji düzeyinin kritik seviyenin altına inmesi.",
                        "3. Pompa İflası: Membrandaki Na+/K+ ATPaz pompasının çalışamaz hale gelmesi.",
                        "4. İyon ve Su Girişi: Hücre içine kontrolsüz sodyum girişi ve suyu beraberinde çekmesi.",
                        "5. Hidropik Şişme: Endoplazmik retikulumun şişmesi ve sitoplazmada berrak vakuollerin oluşumu."
                    ]
                ),
                make_cloze(
                    "Hücre hasarının en erken morfolojik kanıtı membran pompalarının iflasıyla gelişen [hücresel şişme] (hidropik dejenerasyon) tablosudur.",
                    "hücresel şişme",
                    "Erken su birikimi lezyonu adı"
                )
            ]
        },

        # Adım 94
        {
            "slideNumber": 94,
            "title": "Geri Dönüşsüzlük Noktası (Point of No Return): Membran Hasarı ve Kalsiyum Girişi",
            "subtitle": "Ağır plazma membran hasarı ve mitokondriye aşırı kalsiyum girişi hücreyi geri dönüşsüz ölüme kilitler.",
            "badge": "Geri Dönüşsüz Eşik",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Geri dönüşümlü hasar ile geri dönüşsüz ölüm arasındaki sınır çizgisine patolojide **Geri Dönüşsüzlük Noktası (Point of No Return)** adı verilir. Bir hücrenin bu çizgiyi aşıp öldüğünü belirleyen iki kesin olay vardır:

1. **Ağır ve yaygın plazma membranı hasarı:** Membran seçici geçirgenliğini tamamen kaybeder; enzimler dışarı sızar (kanda troponin, AST/ALT yükselir).
2. **Mitokondriyal geçirgenlik geçişi (MPT) ve kalsiyum seli:** Hücre dışından kontrolsüzce giren kalsiyum mitokondriyi kilitler, ATP üretimini sıfırlar ve hücre içi parçalayıcı enzimleri (fosfolipaz, proteaz, endonükleaz) aktive ederek hücreyi içeriden sindirir.

> [TEMEL İLKE] Membran bütünlüğünün kalıcı kaybı ve dev kalsiyum girişi hücrenin ölüm fermanıdır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Membran Rüptürü", "desc": "Hücre zarı parçalanır; hücre içi enzimler kana sızarak laboratuvarda tespit edilir.", "isKey": True},
                    {"title": "Kalsiyum Toksisitesi", "desc": "Hücre içi kalsiyum artışı fosfolipaz ve endonükleazları aktive ederek DNA ve zarı yıkar.", "isKey": True},
                    {"title": "İki Kesin Kriter", "desc": "Düzeltilemeyen mitokondriyal disfonksiyon ve ağır membran geçirgenlik kaybı.", "isKey": False}
                ],
                "table": {
                    "title": "Geri Dönüşsüzlük Noktasının Kilit Kriterleri",
                    "headers": ["Kriter", "Biyolojik Mekanizma", "Tanısal / Klinik Gösterge"],
                    "rows": [
                        ["Plazma Membran Hasarı", "Fosfolipaz aktivasyonu ve lipid peroksidasyonu", "Kanda doku enzimlerinin (Troponin, CK-MB) fırlaması"],
                        ["Mitokondriyal Hasar", "MPT porlarının kalıcı açılması", "Mitokondride amorf kalsiyum yoğunlukları"],
                        ["Nükleer Yıkım", "Endonükleaz aktivasyonu", "Piknoz, karyoreksis ve karyolizis"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Geri dönüşsüz hücre hasarının iki temel belirteci: Ağır membran hasarı ve mitokondriyal disfonksiyondur.",
                "📌 [SINAV SPOTU] Enzimlerin (troponin, transaminaz) kana sızması plazma membran bütünlüğünün geri dönüşsüz kaybını gösterir."
            ],
            "medicalTerms": [
                {"term": "Point of No Return", "explanation": "Hücrenin artık iyileşemeyip kesin olarak ölüme mahkum olduğu biyokimyasal sınırdır."},
                {"term": "Kalsiyum İntoksikasyonu", "explanation": "Sitozolik kalsiyumun aşırı yükselerek hücreyi yıkan enzimleri aktive etmesidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "İskemiye maruz kalan bir miyositin artık geri dönüşümlü hasar safhasından çıkıp 'geri dönüşsüz hücre ölümü' safhasına geçtiğini kesin olarak kanıtlayan temel patolojik olay hangisidir?",
                    {
                        "A": "Plazma membran bütünlüğünün yaygın kaybı ve mitokondriyal disfonksiyon",
                        "B": "Hücre içinde geçici olarak laktik asit birikmesi",
                        "C": "Glikojen depolarının hafifçe azalması",
                        "D": "Endoplazmik retikulumun hafif genişlemesi",
                        "E": "Hücre zarındaki sodyum kanallarının yavaşlaması"
                    },
                    "A",
                    {
                        "A": "Doğru: Membran bütünlüğü kaybı ve kalıcı mitokondri hasarı geri dönüşsüzlüğün kesin kriteridir.",
                        "B": "Yanlış: Laktat birikimi erken geri dönüşümlü anaerobik evredir.",
                        "C": "Yanlış: Glikojen kaybı geri dönüşümlü erken evredir.",
                        "D": "Yanlış: ER şişmesi hidropik dejenerasyondur, geri döner.",
                        "E": "Yanlış: İyon pompası yavaşlaması geri dönüşümlü safhadır."
                    }
                ),
                make_cloze(
                    "Hücrenin geri dönüşsüz ölüme girdiğinin en kesin kanıtı plazma [membran bütünlüğünün] kalıcı olarak parçalanmasıdır.",
                    "membran bütünlüğünün",
                    "Hücre zarı sağlamlığı tamlaması"
                )
            ]
        },

        # Adım 95
        {
            "slideNumber": 95,
            "title": "Nekroz vs Apoptoz: Adaptasyon Başarısızlığının İki Farklı Ölüm Yolu",
            "subtitle": "Hücre ölümü kontrolsüz inflamatuvar parçalanma (nekroz) veya sessiz programlı intihar (apoptoz) şeklinde olur.",
            "badge": "Ölüm Biçimleri",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Adaptasyon sınırını aşan hücreler iki ana patolojik yolla ölür: **Nekroz** ve **Apoptoz**.

**Nekroz** daima patolojiktir. Membran parçalanır, hücre içi enzimler dışarı taşar ve çevre dokuda yoğun **akut inflamasyon** tetiklenir. Tipik örneği miyokard enfarktüsündeki koagülasyon nekrozudur. **Apoptoz** ise programlı bir hücre intiharıdır. Hücre büzüşür, nükleusu parçalanır ve membranla sarılı apoptoz cisimcikleri oluşturur. Hücre içeriği dışarı dökülmediği için çevre dokuda **asla inflamasyon oluşmaz**.

> [TEMEL İLKE] Nekroz çevre dokuyu yakan gürültülü ve inflamatuvar bir ölümdür; apoptoz ise iz bırakmadan temizlenen sessiz bir intihardır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Nekroz İnflamasyonu", "desc": "Membran patlar, hücre döküntüleri lökositleri çağırarak yangı başlatır.", "isKey": True},
                    {"title": "Apoptoz Sessizliği", "desc": "Apoptoz cisimcikleri makrofajlarca sessizce yutulur; inflamasyon gelişmez.", "isKey": True},
                    {"title": "Fizyolojik Ayrım", "desc": "Nekroz daima patolojiktir; apoptoz ise embriyogenez ve doku dengesinde fizyolojiktir.", "isKey": False}
                ],
                "table": {
                    "title": "Nekroz ve Apoptoz Karşılaştırma Matrisi",
                    "headers": ["Özellik", "Nekroz", "Apoptoz"],
                    "rows": [
                        ["Hücre Boyutu", "Şişmiş, büyümüş, lize olmuş", "Büzüşmüş, küçülmüş"],
                        ["Nükleus Durumu", "Piknoz -> Karyoreksis -> Karyolizis", "Nükleozom boyutunda düzenli fragmantasyon"],
                        ["Plazma Membranı", "Parçalanmış, rüptüre", "Sağlam kalır, apoptoz cisimciği yapar"],
                        ["İnflamasyon", "Daima var (şiddetli)", "Kesinlikle yoktur"],
                        ["Biyolojik Nitelik", "Daima patolojik", "Genellikle fizyolojik (patolojik de olabilir)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Nekrozda daima çevre dokuda inflamasyon oluşur; apoptozda ise kesinlikle inflamasyon görülmez.",
                "📌 [SINAV SPOTU] Nekroz daima patolojik bir tablodur; apoptoz ise fizyolojik doku yenilenmesinde de rol alır."
            ],
            "medicalTerms": [
                {"term": "Nekroz", "explanation": "Membran rüptürü ve inflamasyonla giden kontrolsüz patolojik hücre ölümüdür."},
                {"term": "Apoptoz Cisimciği", "explanation": "Apoptoza giden hücrenin membranla sarılı, makrofajlarca yutulan küçük parçalarıdır."}
            ],
            "interactiveElements": [
                make_before_after(
                    "Nekroz ile Apoptoz Hücre Ölümü Karşılaştırması",
                    "Nekroz (Patolojik Yıkım)",
                    "Apoptoz (Programlı İntihar)",
                    [
                        "Hücre şişer ve membranı yırtılır",
                        "Enzimler çevreye dökülür",
                        "Yoğun inflamatuvar lökosit reaksiyonu"
                    ],
                    [
                        "Hücre büzüşür ve yoğunlaşır",
                        "Membran sağlam apoptoz cisimcikleri",
                        "Hiçbir inflamatuvar yanıt gelişmez"
                    ]
                ),
                make_cloze(
                    "Apoptozda hücre içeriği membranla sarılı veziküller içinde kaldığı için çevre dokuda kesinlikle [inflamasyon] gelişmez.",
                    "inflamasyon",
                    "Yangısal doku reaksiyonu adı"
                )
            ]
        },

        # Adım 96
        {
            "slideNumber": 96,
            "title": "Karşılaştırmalı Ayırıcı Tanı: Hipertrofi, Hiperplazi, Atrofi ve Metaplazi",
            "subtitle": "Dört temel adaptasyonun hücresel mekanizma, doku kısıtı ve klinik örnek matrisi.",
            "badge": "Sentez Matrisi",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Dört temel hücresel adaptasyon mekanizmasını bir bütün olarak kavramak, patolojinin tüm organ sistemlerini anlamanın anahtarıdır:

1. **Hipertrofi:** Hücre boyutu artar; bölünemeyen dokularda tek yoldur (ör. kalp).
2. **Hiperplazi:** Hücre sayısı artar; bölünebilen dokularda görülür (ör. karaciğer, endometriyum).
3. **Atrofi:** Hücre boyutu ve kütlesi azalır; ubikuitin-proteazom ve otofajiyle enerji tasarrufu sağlar (ör. alçı bacak, senil beyin).
4. **Metaplazi:** Hücre fenotipi değişir; kök hücre reprogramlamasıyla daha dayanıklı epitel kurulur (ör. sigara bronşu, Barrett).

> [TEMEL İLKE] Doku tipi ve stresin niteliği, hücrenin hangi adaptif yolu seçeceğini belirleyen iki mutlak kuraldır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Boyut vs Sayı", "desc": "Hipertrofi boyut, hiperplazi sayı, atrofi küçülme, metaplazi dönüşümdür.", "isKey": True},
                    {"title": "Doku Bağımlılığı", "desc": "Bölünmeyen hücreler sadece hipertrofi/atrofi; kök hücre içerenler metaplazi yapabilir.", "isKey": True},
                    {"title": "Ortak Payda", "desc": "Dördü de uyaran kesildiğinde geri dönebilen (reversible) süreçlerdir.", "isKey": False}
                ],
                "table": {
                    "title": "Dört Temel Adaptasyon Tipinin Büyük Karşılaştırma Matrisi",
                    "headers": ["Adaptasyon", "Temel Mekanizma", "Doku Kısıtlılığı", "Klinik Prototip"],
                    "rows": [
                        ["Hipertrofi", "Protein ve organel sentezi", "Kalıcı bölünemeyen dokular", "Hipertansif sol ventrikül"],
                        ["Hiperplazi", "Mitoz bölünmeyle hücre artışı", "Labil ve stabil dokular", "Parsiyel hepatektomi, BPH"],
                        ["Atrofi", "Ubikuitin-proteazom ve otofaji", "Tüm dokularda geçerli", "Kırık alçısı, senil beyin"],
                        ["Metaplazi", "Kök hücre reprogramlaması", "Kök hücre içeren epiteller", "Sigarada bronş, Barrett özofagus"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Bölünemeyen kalıcı hücreler yalnızca hipertrofi yapabilir; hiperplazi yapamaz.",
                "📌 [SINAV SPOTU] Dört temel adaptasyonun dördü de etken ortadan kalktığında geri dönebilir (reversible)."
            ],
            "medicalTerms": [
                {"term": "Diferansiasyon", "explanation": "Hücrenin özelleşmiş fonksiyonel ve yapısal özellikler kazanmasıdır."},
                {"term": "Kombine Yanıt", "explanation": "Bir organda hipertrofi ve hiperplazinin eşzamanlı birlikte gelişmesidir."}
            ],
            "interactiveElements": [
                make_interactive_table(
                    "Dört Adaptasyon Tipinin Klinik Eşleştirmesi",
                    ["Klinik Senaryo", "Gelişen Temel Hücresel Süreç", "Doğru Adaptasyon Tipi"],
                    [
                        [
                            ("Aort darlığında sol ventrikül kalınlaşması", False),
                            ("Miyositlerde yeni sarkomer senteziyle büyüme", True, "Bölünemeyen dokuda hacim artışı"),
                            ("Hipertrofi", False)
                        ],
                        [
                            ("Karaciğer rezeksiyonunda kütle tamamlanması", False),
                            ("Hepatositlerin HGF ile mitoza girmesi", True, "Hücre sayısı artışı"),
                            ("Kompansatuvar hiperplazi", False)
                        ],
                        [
                            ("Alçıya alınan bacak kaslarının erimesi", False),
                            ("Ubikuitin-proteazom ile miyofilament yıkımı", True, "İş yükü kaybı küçülmesi"),
                            ("Kullanılmama atrofisi", False)
                        ],
                        [
                            ("Reflü hastasında özofagusta kolumnar epitel", False),
                            ("Kök hücrelerin aside dayanıklı epitele dönüşümü", True, "Hücre tipi yer değiştirmesi"),
                            ("Barrett metaplazisi", False)
                        ]
                    ]
                ),
                make_active_recall(
                    "Neden kalp miyokardında ve iskelet kasında adaptasyon olarak metaplazi veya hiperplazi değil yalnızca hipertrofi görülür?",
                    "Çünkü kardiyomiyositler ve iskelet kası lifleri bölünemeyen kalıcı hücrelerdir (hiperplazi yapamazlar) ve mezenkimal/epitelyal kök hücre havuzları bulunmadığından metaplaziye uğrayamazlar."
                )
            ]
        },

        # Adım 97
        {
            "slideNumber": 97,
            "title": "Klinik Vaka Analizi: Hipertansif Kalp Hastalığında Adaptif Evreleme",
            "subtitle": "Klinik vaka üzerinden konsantrik hipertrofiden kalp yetmezliğine gidişin analizi.",
            "badge": "Vaka Analizi",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """**Vaka:** 58 yaşında erkek hasta, 15 yıldır düzensiz tedavi aldığı hipertansiyon öyküsüyle başvuruyor. Ekokardiyografisinde sol ventrikül serbest duvar kalınlığı **2.2 cm**, lümeni daralmış ve ejeksiyon fraksiyonu %60 (korunmuş) bulunuyor. Hasta merdiven çıkarken hafif nefes darlığı tarifliyor.

Bu hasta **kompanse konsantrik hipertrofi** evresindedir. Art yükü karşılamak için miyositler kalınlaşmış ve duvar gerilimini düşürmüştür. Diyastolik doluş zorluğu nefes darlığını başlatmıştır. Eğer tansiyon regüle edilmezse sonraki evrede kapiller yetersizlik ve apoptozla duvar incelerek dilatasyon ve sistolik kalp yetmezliği gelişecektir.

> [KLİNİK İPUCU] Kompanse hipertrofi evresinde tansiyonun agresif tedavisi, dilatasyon ve geri dönüşsüz yetmezliğe gidişi durdurabilir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Mevcut Durum", "desc": "Sol ventrikül 2.2 cm (>2 cm) ile kompanse konsantrik hipertrofidedir.", "isKey": True},
                    {"title": "Diyastolik Sertlik", "desc": "Kalınlaşan duvar gevşeyemez; sol atriyum basıncı artarak efor dispnesi yapar.", "isKey": True},
                    {"title": "Gelecek Risk", "desc": "Tedavi edilmezse miyosit ölümü, fibrozis ve ventriküler dilatasyon kaçınılmazdır.", "isKey": False}
                ],
                "table": {
                    "title": "Vakanın Klinikopatolojik Evreleri",
                    "headers": ["Evre", "Patolojik Morfoloji", "Klinik Semptom"],
                    "rows": [
                        ["Şu Anki Evre (Kompanse)", "Konsantrik hipertrofi, duvar >2 cm, dar lümen", "Hafif efor dispnesi, korunmuş EF (%60)"],
                        ["Risk Altındaki Gelecek Evre", "İnterstisyel fibrozis, ventriküler dilatasyon", "Konjestif kalp yetmezliği, akciğer ödemi, düşük EF"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Hipertansif kalp hastalığında duvar kalınlığı >2 cm konsantrik hipertrofiyi kanıtlar.",
                "📌 [SINAV SPOTU] Erken evrede sistolik fonksiyon (EF) korunmuştur; sorun diyastolik gevşemedir."
            ],
            "medicalTerms": [
                {"term": "Konsantrik Evre", "explanation": "Basınç yüküne karşı ventrikül duvarının içe doğru kalınlaştığı kompanse dönemdir."},
                {"term": "Efor Dispnesi", "explanation": "Fiziksel aktivite sırasında akciğer konjesyonu nedeniyle nefes darlığı hissedilmesidir."}
            ],
            "interactiveElements": [
                make_branching_logic(
                    "Hipertansif konsantrik hipertrofisi (duvar 2.2 cm) olan 58 yaşındaki hastanın yönetim senaryosu.",
                    [
                        {
                            "text": "Ejeksiyon fraksiyonu %60 (normal) olduğuna göre kalpte hiçbir sorun yoktur, hasta takipsiz bırakılır.",
                            "isCorrect": False,
                            "feedback": "Hatalı! Konsantrik hipertrofi dekompansasyon ve ani ölüm riski taşır; mutlaka tedavi edilmelidir."
                        },
                        {
                            "text": "Kan basıncı antihipertansiflerle (ACEi/ARB) sıkı kontrole alınarak duvar gerilimi düşürülür ve hipertrofik gerileme hedeflenir.",
                            "isCorrect": True,
                            "feedback": "Kusursuz klinik yaklaşım! Art yükün düşürülmesi miyokardiyal hipertrofiyi gerileterek kalp yetmezliğini önler."
                        },
                        {
                            "text": "Doğrudan acil kalp nakli listesine alınır.",
                            "isCorrect": False,
                            "feedback": "Gereksiz ve aşırı! Hasta kompanse evrededir."
                        }
                    ]
                ),
                make_cloze(
                    "Hipertansif hastada sol ventrikül duvarının 2 cm üzerine çıkması [konsantrik] hipertrofi tablosunu gösterir.",
                    "konsantrik",
                    "İçe doğru kalınlaşma terimi"
                )
            ]
        },

        # Adım 98
        {
            "slideNumber": 98,
            "title": "Klinik Vaka Analizi: Reflü Hastasında Barrett Özofagusunun İzlemi",
            "subtitle": "Klinik vaka üzerinden intestinal metaplazi tanısı ve displazi tarama stratejisi.",
            "badge": "Vaka Analizi",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """**Vaka:** 48 yaşında erkek hasta, 8 yıldır devam eden retrosternal yanma (pirozis) ve asit regürjitasyonu şikayetleriyle endoskopiye alınıyor. Gastroözofageal bileşkeden yukarı doğru 3 cm tırmanan somon kırmızısı kadifemsi mukoza alanları izleniyor. Biyopside Alcian Blue pozitif **goblet hücreleri içeren kolumnar epitel** saptanıyor; nükleer atipi görülmüyor.

Bu hastanın tanısı **Atipisiz Barrett Özofagusudur (İntestinal Metaplazi)**. Asit hasarına karşı yassı epitel kolumnar epitele dönerek kendini korumuştur. Atipi olmadığı için acil cerrahi gerekmez; ancak hasta adenokarsinom riski nedeniyle 3-5 yılda bir biyopsili endoskopik takibe alınmalıdır.

> [KLİNİK İPUCU] Barrett özofagusunda displazi saptanmadığı sürece agresif ablasyon gerekmez; proton pompa inhibitörü ve periyodik takip yeterlidir.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Kesin Tanı", "desc": "Biyopside goblet hücreli intestinal metaplazinin gösterilmesiyle Barrett tanısı kesinleşmiştir.", "isKey": True},
                    {"title": "Atipi Yokluğu", "desc": "Displazi izlenmemesi hastayı yakın dönem karsinom tehdidinden uzak tutar.", "isKey": True},
                    {"title": "Tarama Protokolü", "desc": "Displazi gelişimini erken yakalamak için 3-5 yılda bir dört kadran biyopsi takibi önerilir.", "isKey": False}
                ],
                "table": {
                    "title": "Barrett Olgusunda İzlem Karar Matrisi",
                    "headers": ["Biyopsi Sonucu", "Kanser Riski", "Klinik İzlem Stratejisi"],
                    "rows": [
                        ["Displazi Yok (Mevcut Durum)", "Çok düşük (%0.2 - 0.5 / yıl)", "3 - 5 yılda bir endoskopi ve PPI tedavisi"],
                        ["Düşük Dereceli Displazi (LGD)", "Orta düzey", "Endoskopik ablasyon veya 6 ayda bir biyopsi"],
                        ["Yüksek Dereceli Displazi (HGD)", "Çok yüksek (%6-10 / yıl)", "Endoskopik mukozal rezeksiyon (EMR)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Barrett özofagusunda intestinal metaplazi (goblet hücresi) gösterilmesi şarttır.",
                "📌 [SINAV SPOTU] Displazisiz Barrett hastalarında takip aralığı kılavuzlara göre 3-5 yıldır."
            ],
            "medicalTerms": [
                {"term": "Pirozis", "explanation": "Mide asidinin özofagusa kaçmasıyla göğüs kemiği arkasında hissedilen yakıcı ağrıdır."},
                {"term": "EMR", "explanation": "Endoskopik mukozal rezeksiyon; mukozadaki displazik alanı cerrahisiz çıkarma işlemidir."}
            ],
            "interactiveElements": [
                make_active_recall(
                    "Barrett özofagusu tanısı alan bir hastada endoskopik biyopsilerin temel amacı nedir?",
                    "Kanser öncüsü olan epitelyal displazinin (düşük veya yüksek dereceli) erken evrede saptanarak invaziv adenokarsinom gelişmeden tedavi edilmesidir."
                ),
                make_cloze(
                    "Barrett özofagusu zemininde kanser gelişimini önlemek için biyopsilerde kilit olarak [displazi] varlığı araştırılır.",
                    "displazi",
                    "Kanser öncüsü atipik lezyon adı"
                )
            ]
        },

        # Adım 99
        {
            "slideNumber": 99,
            "title": "Kurul ve Klinik Patoloji Sınavları İçin Yüksek Verimli Özet Stratejisi",
            "subtitle": "Tıp fakültesi kurul ve TUS sınavlarında hücresel adaptasyonlardan en sık sorulan spot noktalar.",
            "badge": "Sınav Stratejisi",
            "badgeColor": "red",
            "discipline": "Tıbbi Patoloji",
            "synthesisNarrative": """Tıp fakültesi kurul sınavlarında ve uzmanlık (TUS) sınavlarında hücresel adaptasyonlar her dönem soru çıkan garantili konulardandır. Başarı için şu altın noktalar akılda tutulmalıdır:

1. **Kalıcı dokularda (kalp, iskelet kası)** yalnızca saf hipertrofi görülür, hiperplazi olamaz.
2. **Gebelik uterusunda** hem hipertrofi hem hiperplazi birlikte görülür.
3. **Karaciğer rejenerasyonu** parsiyel hepatektomi sonrası telafi edici hiperplazidir (HGF ve IL-6).
4. **Atrofinin moleküler motoru** ubikuitin-proteazom sistemi (MuRF1) ve otofajidir; kahverengi atrofide lipofuksin birikir.
5. **Barrett özofagusu** kolumnar metaplazidir ve goblet hücresi şarttır.

> [SINAV SPOTU] Adaptasyon sorularında hücre bölünme kapasitesini ve etiyolojik uyarının yönünü denetleyin.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "Mitoz Kuralı", "desc": "Kalıcı hücrelerde hiperplazi şıkkını doğrudan eleyin.", "isKey": True},
                    {"title": "Kombine Dokular", "desc": "Gebelik uterusu ve BPH hem hipertrofi hem hiperplazi içerir.", "isKey": True},
                    {"title": "Metaplazi İpuçları", "desc": "Sigarada kolumnar -> skuamöz; Barrett'te skuamöz -> kolumnar.", "isKey": False}
                ],
                "table": {
                    "title": "Sınavlarda En Çok Karıştırılan Tuzak Noktalar",
                    "headers": ["Soru İfadesi", "Tuzak Şık", "Doğru Patolojik Yanıt"],
                    "rows": [
                        ["Aort darlığında kalp miyokardı", "Hiperplazi", "Yalnızca Saf Hipertrofi"],
                        ["Gebelikte büyüyen miyometriyum", "Yalnızca hipertrofi", "Hipertrofi + Hiperplazi birlikte"],
                        ["Alçıya alınan kolda kas erimesi", "Nekroz veya hipoplazi", "Kullanılmama Atrofisi (Disuse)"],
                        ["Barrett özofagusu mikroskopisi", "Skuamöz metaplazi", "İntestinal kolumnar metaplazi (Goblet+)"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Kalıcı hücreler (kardiyomiyosit, nöron) hiperplazi yapamaz.",
                "📌 [SINAV SPOTU] Dört temel adaptasyonun tümü geri dönüşümlüdür (reversible)."
            ],
            "medicalTerms": [
                {"term": "TUS", "explanation": "Tıpta Uzmanlık Eğitimi Giriş Sınavı."},
                {"term": "Spot Bilgi", "explanation": "Sınavlarda doğrudan soru kökü veya doğru şık olan yüksek verimli klinik bilgidir."}
            ],
            "interactiveElements": [
                make_micro_quiz(
                    "Tıp fakültesi patoloji kurul sınavında 'Hücresel Adaptasyonlar' konusunda aşağıdaki ifadelerden hangisi sınav sorusu olarak karşınıza çıktığında KESİNLİKLE YANLIŞTIR?",
                    {
                        "A": "Miyokard hücreleri iş yükü artışına hiperplazi ile yanıt verir",
                        "B": "Gebelik uterusunda hipertrofi ve hiperplazi birlikte görülür",
                        "C": "Kullanılmama atrofisinde ubikuitin-proteazom yolağı aktive olur",
                        "D": "Barrett özofagusunda skuamöz epitel kolumnar epitele dönüşür",
                        "E": "Otofajinin moleküler göstergesi LC3-II proteinidir"
                    },
                    "A",
                    {
                        "A": "Doğru tuzak tespiti: Miyokard bölünemeyen kalıcı dokudur; hiperplazi yapamaz, yalnızca hipertrofi yapar.",
                        "B": "Yanlış: Doğru ifadedir; miyometriyumda ikisi birliktedir.",
                        "C": "Yanlış: Doğru ifadedir; MuRF1 kas proteinlerini yıkar.",
                        "D": "Yanlış: Doğru ifadedir; Barrett kolumnar metaplazidir.",
                        "E": "Yanlış: Doğru ifadedir; LC3-II altın standarttır."
                    }
                ),
                make_cloze(
                    "Kardiyomiyositler bölünme yeteneğinden yoksun oldukları için kurul sınavlarında miyokardda [hiperplazi] geliştiğini iddia eden şıklar daima yanlıştır.",
                    "hiperplazi",
                    "Hücre sayısı artışı süreci"
                )
            ]
        },

        # Adım 100 (CHECKPOINT 10 - BÜYÜK FİNAL)
        {
            "slideNumber": 100,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 10] BÜYÜK FİNAL: Hücresel Adaptasyonlar Sentez Matrisi",
            "subtitle": "100 adımlık maratonun büyük finali: Tüm hücresel adaptasyon modellerini, mekanizmalarını ve sınav spotlarını tek tabloda sentezleyin.",
            "badge": "Büyük Final",
            "badgeColor": "amber",
            "discipline": "Tıbbi Patoloji",
            "isCheckpoint": True,
            "checkpointNumber": 10,
            "synthesisNarrative": """Tebrikler! Kurul 1 Patoloji dersinin en temel ve kapsamlı konularından biri olan **Hücresel Adaptasyonlar** mikro-dersini 100 atomik adımda eksiksiz tamamladınız.

Homeostazın dinamik dengesinden başlayarak; saf hipertrofinin moleküler kaskadlarını (integrin, kalsinörin, NFAT), kardiyak hipertrofinin yetmezliğe uzanan trajik sınırlarını, labil ve stabil dokulardaki fizyolojik ve patolojik hiperplazileri (BPH, endometriyum, karaciğer rejenerasyonu), ubikuitin-proteazom ve otofaji odaklı kas atrofisini (MuRF1, lipofuksin, kahverengi atrofi), kök hücre reprogramlamasına dayanan epitelyal ve mezenkimal metaplazileri (Barrett, sigara bronşu, miyozitis ossifikans) ve geri dönüşsüz hücre ölümüne geçiş dinamiklerini tek tek inceledik.

> [BÜYÜK FİNAL İLKESİ] Adaptasyon hücrenin ölümle yaşam arasındaki köprüsüdür; onu doğru anlamak tüm klinik tıbbın patofizyolojisini kavramaktır.""",
            "coreContent": {
                "keyBullets": [
                    {"title": "100 Adım Tamamlandı", "desc": "Robbins 11. baskı ve fakülte amfi notlarıyla %100 uyumlu tam adaptasyon sentezi.", "isKey": True},
                    {"title": "Dört Temel Sütun", "desc": "Hipertrofi (boyut), Hiperplazi (sayı), Atrofi (küçülme), Metaplazi (dönüşüm).", "isKey": True},
                    {"title": "Klinik Hakimiyet", "desc": "Kardiyoloji, jinekoloji, üroloji ve gastroenteroloji adaptasyonlarına tam hakimiyet.", "isKey": False}
                ],
                "table": {
                    "title": "BÜYÜK FİNAL SENTEZ MATRİSİ",
                    "headers": ["Adaptasyon Türü", "Temel Hücresel Değişim", "Kilit Moleküler Faktör", "Klasik Klinik Prototip"],
                    "rows": [
                        ["Hipertrofi", "Hücre boyutunda artış", "Kalsinörin / NFAT, GATA4, IGF-1", "Hipertansif Sol Ventrikül"],
                        ["Hiperplazi", "Hücre sayısında artış", "MAPK, HGF, Östrojen, DHT", "Gebelikte Meme, Parsiyel Hepatektomi, BPH"],
                        ["Atrofi", "Hücre boyutu ve kütlesinde azalma", "Ubikuitin (MuRF1/Atrogin-1), Otofaji", "Alçıdaki Ekstremite Kası, Senil Beyin"],
                        ["Metaplazi", "Hücre fenotipinde yer değiştirme", "Kök hücre reprogramlaması, BMP", "Sigarada Bronş, Barrett Özofagusu"]
                    ]
                }
            },
            "spotPearls": [
                "📌 [SINAV SPOTU] Dört temel adaptasyonun tümü uyaran kesildiğinde GERİ DÖNÜŞÜMLÜDÜR.",
                "📌 [SINAV SPOTU] Bölünemeyen hücrelerde (kalp, iskelet kası) hiperplazi olmaz; saf hipertrofi olur.",
                "📌 [SINAV SPOTU] Barrett özofagusunda goblet hücreli kolumnar intestinal metaplazi görülür ve adenokarsinom öncülüdür."
            ],
            "medicalTerms": [
                {"term": "Hücresel Adaptasyon", "explanation": "Hücrenin stres karşısında canlı kalmak için geliştirdiği geri dönüşümlü morfolojik uyumdur."},
                {"term": "Homeostaz", "explanation": "İç ortamın dar fizyolojik sınırlar içinde kararlı tutulmasıdır."},
                {"term": "Otofaji", "explanation": "Hücrenin açlıkta kendi bileşenlerini lizozomda sindirerek enerji sağladığı süreçtir."}
            ],
            "flashcards": [
                make_flashcard(
                    "k1-03-fc28",
                    "Dört temel hücresel adaptasyon tipini (hipertrofi, hiperplazi, atrofi, metaplazi) tek birer cümleyle tanımlayınız.",
                    "Hipertrofi hücre boyutunun büyümesi, hiperplazi hücre sayısının artması, atrofi hücre maddesi kaybıyla küçülmesi, metaplazi ise bir olgun hücre tipinin daha dayanıklı başka bir olgun hücre tipine dönüşmesidir."
                ),
                make_flashcard(
                    "k1-03-fc29",
                    "Hücre hasarında 'Geri Dönüşsüzlük Noktası'nı (Point of No Return) belirleyen iki kesin patolojik olay nedir?",
                    "1) Plazma membran bütünlüğünün yaygın ve kalıcı kaybı (enzim sızıntısı), 2) Düzeltilemeyen mitokondriyal disfonksiyon ve aşırı kalsiyum girişidir."
                ),
                make_flashcard(
                    "k1-03-fc30",
                    "Nekroz ile apoptoz arasındaki en temel morfolojik ve inflamatuvar fark nedir?",
                    "Nekrozda hücre şişip membranı parçalanır ve çevre dokuda yoğun akut inflamasyon gelişir; apoptozda ise hücre membranla sarılı apoptoz cisimciklerine ayrılarak büzüşür ve çevre dokuda kesinlikle inflamasyon oluşmaz."
                )
            ],
            "interactiveElements": [
                make_active_recall(
                    "Kurul 1 Tıbbi Patoloji dersi kapsamında 'Hücresel Adaptasyonlar' konusunun klinik hekimlikteki en büyük önemi nedir?",
                    "Hastalıkların başlangıç evresinde gelişen hücresel adaptasyonların erken tanınması, etiyolojik etken (hipertansiyon, reflü, sigara) zamanında tedavi edildiğinde doku hasarının tamamen geri döndürülebilmesini (reversibilite) ve organ yetmezliğinin veya kanserleşmenin önlenebilmesini sağlar."
                )
            ]
        }
    ]
