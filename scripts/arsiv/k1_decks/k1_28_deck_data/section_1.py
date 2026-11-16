# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi
Bölüm 1: Neoplazi İlkeleri ve Kanser Hallmarks (Slayt 1 - 10)
Checkpoint: Slayt 9
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_1_slides():
    return [
        # Slayt 1
        {
            "slideNumber": 1,
            "title": "Neoplazi ve Kanser Kavramlarına Giriş",
            "content": (
                "Neoplazi, kelime anlamı olarak 'yeni büyüme' demektir ve Willis'in klasik tanımıyla; normal doku büyümesini "
                "aşan, bu büyüme ile koordine olmayan ve büyümeyi başlatan uyaran ortadan kalktıktan sonra dahi aşırı büyümesini "
                "özerk biçimde sürdüren anormal bir doku kitlesidir. 'Tümör' terimi tarihsel olarak enflamasyonun dört kardinal "
                "belirtisinden biri olan şişliği simgelerken, günümüzde neoplazm ile eş anlamlı olarak kullanılmaktadır. "
                "'Kanser' ise tüm malign neoplazmları kapsayan genel şemsiye terimdir. Kanser esasında genetik ve epigenetik "
                "değişikliklerin birikimiyle ortaya çıkan, hücrenin büyüme ve hayatta kalma mekanizmalarını bozan moleküler bir hastalıktır."
            ),
            "elements": [
                make_cloze(
                    "Normal doku büyümesini aşan ve uyaran ortadan kalktıktan sonra dahi otonom çoğalmasını sürdüren doku kitlesine neoplazi adı verilir.",
                    "neoplazi",
                    "Yeni büyüme anlamındaki tıp terimi"
                ),
                make_active_recall(
                    "Tüm malign neoplazmları tanımlamak için kullanılan genel ve evrensel terim nedir?",
                    "Kanser terimidir.",
                    "Malign kitlelerin genel adı"
                )
            ]
        },
        # Slayt 2
        {
            "slideNumber": 2,
            "title": "Parankim ve Stroma: İkili Yapısal Organizasyon",
            "content": (
                "Bütün neoplazmlar, benign ya da malign olsunlar, histolojik olarak iki temel bileşenden meydana gelir: "
                "'Parankim' ve 'Stroma'. Parankim, klonal olarak çoğalan transforme neoplastik hücreler kümesidir. "
                "Tümörün biyolojik davranışını (benign veya malign oluşunu), büyüme hızını, yayılma paternini belirleyen ve "
                "tümörün histopatolojik adlandırılmasını sağlayan yegane bileşen parankimdir. Stroma ise konakçı kökenli "
                "olup bağ dokusu, kan ve lenf damarları ile nötrofil, makrofaj ve lenfosit gibi inflamatuar hücrelerden oluşur. "
                "Stroma, tümörün oksijenlenmesini ve beslenmesini sağlarken aynı zamanda parankim ile parakrin sinyaller "
                "aracılığıyla dinamik ve iki yönlü bir metabolik etkileşim sürdürür."
            ),
            "elements": [
                make_table(
                    "Tümör Bileşenleri: Parankim vs Stroma Karşılaştırması",
                    ["Bileşen", "Hücresel Köken", "Temel Fonksiyon", "Sınıflamadaki Rolü"],
                    [
                        {
                            "cells": ["Parankim", "Transforme klonal neoplastik hücreler", "Biyolojik davranışı ve yayılımı belirleme", "Adlandırmanın temel dayanağı"],
                            "hiddenIndex": 3,
                            "hint": "Tümöre adını veren yapı"
                        },
                        {
                            "cells": ["Stroma", "Konakçı mezankimi ve inflamatuar hücreler", "Mekanik destek, anjiyogenez ve beslenme", "Adlandırmayı doğrudan belirlemez"],
                            "hiddenIndex": 1,
                            "hint": "Vücut kökenli destek elemanı"
                        }
                    ]
                ),
                make_before_after(
                    "Parankim ve Stroma Dengesi",
                    "Zengin Parankim, Az Stroma (Medüller Kitle)",
                    "Hücresel yoğunluk çok yüksektir, tümör yumuşak, etsi ve frajildir; nekroza yatkındır.",
                    "Yoğun Fibröz Stroma (Dezmoplazi / Skirröz Kitle)",
                    "Parankim hücreleri konak fibroblastlarını aşırı uyarır; taş gibi sert, çekintili ve fibrotik bir kitle oluşur.",
                    "Meme duktal karsinomundaki taş sertliği parankimden değil yoğun dezmoplastik stromadan kaynaklanır."
                )
            ]
        },
        # Slayt 3
        {
            "slideNumber": 3,
            "title": "Klonalite İlkesi ve Darwinci Klonal Seçilim",
            "content": (
                "Kanser gelişiminin en temel biyolojik postülatı 'monoklonalite'dir. Hemen hemen tüm insan tümörleri, "
                "genomunda kritik sürücü mutasyonlar biriktiren tek bir öncül hücrenin klonal proliferasyonundan doğar. "
                "Ancak tümör büyüdükçe genomik istikrarsızlık nedeniyle bu orijinal klondan türeyen hücreler yeni ikincil "
                "mutasyonlar kazanır. Büyüme, anjiyogenez veya kemoterapiden kaçış avantajı sağlayan mutant alt hücreler, "
                "tümör mikroçevresinde 'Darwinci doğal seçilim' yasalarına göre hayatta kalır ve baskın alt klonlar haline gelir. "
                "Bu sürece 'tümör progresyonu' ve 'klonal heterojenite' adı verilir; ileri evre bir kanserin tek bir kemoterapötik "
                "ilaca direnç geliştirmesinin temel biyolojik sebebi bu klonal çeşitliliktir."
            ),
            "elements": [
                make_causal_chain(
                    "Tek Hücreden Klonal Heterojeniteye Uzanan Progresyon Yolu",
                    [
                        "1. Monoklonal Başlangıç: Tek bir öncül somatik hücrede ilk sürücü mutasyonun oluşması",
                        "2. Klonal Genişleme: Transforme hücrenin kontrolsüz bölünerek primer tümör odağını kurması",
                        "3. Genomik İnstabilite: Hızlı bölünmeler sırasında DNA onarım kusurlarıyla yeni alt mutasyonların doğması",
                        "4. Darwinci Seçilim: Hipoksi ve immün saldırıya en dirençli alt klonların seçilerek baskınlaşması",
                        "5. Klonal Heterojenite: Farklı genetik ve fenotipik özelliklere sahip çoklu hücre popülasyonlarının oluşması"
                    ]
                ),
                make_cloze(
                    "Tümörlerin genetik olarak tek bir transforme hücre soyundan köken alması monoklonalite ilkesi ile tanımlanır.",
                    "monoklonalite",
                    "Tek atasal hücreden türeme durumu"
                )
            ]
        },
        # Slayt 4
        {
            "slideNumber": 4,
            "title": "Kanserin Ayırt Edici Özellikleri (Hanahan-Weinberg Hallmarks)",
            "content": (
                "Kanser hücrelerinin normal konakçı hücrelerinden ayrılmasını ve özerk malign davranış sergilemesini sağlayan "
                "temel biyolojik yetenekler, Hanahan ve Weinberg tarafından 'Kanserin Ayırt Edici Özellikleri' (Hallmarks of Cancer) "
                "olarak formüle edilmiştir. Bu sekiz temel kural şunlardır: Büyüme sinyallerinde kendine yeterlilik, büyüme "
                "baskılayıcı sinyallere duyarsızlık, değişmiş hücresel metabolizma (Warburg etkisi), apoptozdan kaçınma, "
                "sınırsız çoğalma potansiyeli (replikatif ölümsüzlük), sürekli ve kalıcı anjiyogenez indüksiyonu, doku invazyonu "
                "ve metastaz yeteneği ile konak bağışıklık gözetiminden kaçınma. Bu biyolojik yeteneklerin kazanılmasını kolaylaştıran "
                "iki temel zemin ise 'genomik istikrarsızlık' ve 'tümörü destekleyen kronik inflamasyon'dur."
            ),
            "elements": [
                make_table(
                    "Kanserin Ayırt Edici Özellikleri ve Moleküler Aracıları",
                    ["Hallmark Özelliği", "Kilit Gen veya Süreç", "Fizyopatolojik Sonuç"],
                    [
                        {
                            "cells": ["Büyüme Sinyalinde Kendine Yeterlilik", "RAS, EGFR, MYC onkogenleri", "Dış büyüme faktörü olmadan otonom bölünme"],
                            "hiddenIndex": 1,
                            "hint": "Onkogenik mutasyon örnekleri"
                        },
                        {
                            "cells": ["Büyüme Baskısına Duyarsızlık", "RB ve TP53 tümör baskılayıcıları", "Hücre döngüsü frenlerinin devre dışı kalması"],
                            "hiddenIndex": 1,
                            "hint": "Hücresel fren mekanizması genleri"
                        },
                        {
                            "cells": ["Replikatif Ölümsüzlük", "Telomeraz aktivasyonu (hTERT)", "Senesens bariyerinin aşılarak sınırsız bölünme"],
                            "hiddenIndex": 0,
                            "hint": "Hücrenin sonsuz bölünme yeteneği"
                        }
                    ]
                ),
                make_active_recall(
                    "Kanser hücrelerinin hallmarks yeteneklerini kazanmasını kolaylaştıran iki etkinleştirici faktör nedir?",
                    "Genomik istikrarsızlık ve tümörü destekleyen kronik inflamasyondur.",
                    "DNA onarım bozukluğu ve yangı"
                )
            ]
        },
        # Slayt 5
        {
            "slideNumber": 5,
            "title": "Onkogenik Sinyal Yolakları: RAS-RAF-MAPK Aksı",
            "content": (
                "Normal hücreler bölünmek için komşu hücrelerden veya mikroçevreden gelen parakrin büyüme faktörlerine muhtaçtır. "
                "Kanser hücreleri ise 'proto-onkogenlerin' mutasyonla 'onkogenlere' dönüşmesi sonucu büyüme sinyallerinde kendine "
                "yeterlilik kazanırlar. En sık mutasyona uğrayan proto-onkogen ailesi RAS'tır (KRAS, NRAS, HRAS). RAS, hücre zarının "
                "iç yüzeyinde yer alan bir G-proteindir. Dinlenme halinde GDP'ye bağlı inaktif formdadır; tirozin kinaz reseptörü "
                "uyarısıyla GTP bağlayarak aktif forma geçer. Aktif RAS, RAF/MAP-kinaz ve PI3K/AKT yollarını tetikleyerek nükleusta "
                "MYC ve siklin D transkripsiyonunu başlatır. GTPaz aktive edici proteinlerin (GAP) mutasyonla yok olması, RAS'ın sürekli "
                "GTP'li kalarak hücreye kapatılamayan kesintisiz bir 'bölün' sinyali pompalamasına yol açar."
            ),
            "elements": [
                make_causal_chain(
                    "Tirozin Kinaz Reseptöründen Nükleer Bölünmeye RAS Yolağı",
                    [
                        "1. Reseptör Aktivasyonu: Büyüme faktörünün zardaki tirozin kinaz reseptörüne bağlanması",
                        "2. Guanin Değişimi: RAS proteininin bağlı GDP'yi bırakıp GTP bağlayarak aktive olması",
                        "3. Kinaz Kaskadı: Aktif RAS-GTP kompleksinin sitoplazmada RAF ve MEK kinazları fosforilasyonu",
                        "4. MAPK Girişi: Aktif MAPK'ın çekirdeğe girerek transkripsiyon faktörlerini (MYC vb.) uyarması",
                        "5. Hücre Bölünmesi: Siklin D ekspresyonunun patlaması ve G1'den S fazına kontrolsüz geçiş"
                    ]
                ),
                make_cloze(
                    "İnsan kanserlerinde en sık mutasyona uğrayan zarlarla ilişkili G-protein proto-onkogeni RAS ailesidir.",
                    "RAS",
                    "GTPaz aktivitesi gösteren onkogen"
                )
            ]
        },
        # Slayt 6
        {
            "slideNumber": 6,
            "title": "Hücre Döngüsü Frenleri: Retinoblastom (RB) ve CDK'lar",
            "content": (
                "Hücre döngüsünün en kritik bekçisi G1-S kontrol noktasıdır ve bu geçiş 'retinoblastom' (RB) tümör baskılayıcı "
                "proteini tarafından kilit altında tutulur. İstirahat halindeki hücrelerde hipofosforile (aktif) RB proteini, "
                "E2F transkripsiyon faktörüne sıkıca bağlanarak onu hapseder ve S fazı genlerinin okunmasını engeller. Büyüme "
                "uyaranları geldiğinde siklin D - CDK4/6 ve siklin E - CDK2 kompleksleri aktive olarak RB proteinini hiperfosforile "
                "eder. Fosforillenen RB gevşer ve E2F serbest kalır; hücre geri dönüşsüz olarak DNA replikasyonuna (S fazı) girer. "
                "Bu döngüyü frenleyen p16 (CDKN2A) veya p21 tümör baskılayıcı inhibitörlerin mutasyonla kaybı ya da RB geninin "
                "doğrudan inaktivasyonu, hücre döngüsü frenlerinin kalıcı olarak bozulmasıyla sonuçlanır."
            ),
            "elements": [
                make_before_after(
                    "RB Proteininin Hücre Döngüsündeki Fosforilasyon Durumu",
                    "Hipofosforile RB (Fren Basılı)",
                    "RB aktif haldedir, E2F faktörünü sıkıca hapseder; hücre G1 fazında bekletilir, kontrolsüz bölünme engellenir.",
                    "Hiperfosforile veya Mutasyone RB (Fren Boşta)",
                    "CDK4/6 tarafından fosforillenen RB E2F'i serbest bırakır; S fazı enzimleri sentezlenir, hücre hızla DNA kopyalar.",
                    "Hemen hemen tüm insan kanserlerinde RB yolağındaki fren mekanizması bozulmuştur."
                ),
                make_active_recall(
                    "Hücre döngüsünde E2F faktörünü bağlayarak G1-S geçişini bloke eden kilit tümör baskılayıcı protein hangisidir?",
                    "Retinoblastom (RB) proteinidir.",
                    "Kromozom 13q'da kodlanan göz tümörü proteini"
                )
            ]
        },
        # Slayt 7
        {
            "slideNumber": 7,
            "title": "Değişmiş Metabolizma: Warburg Etkisi (Aerobik Glikoliz)",
            "content": (
                "Otto Warburg tarafından ilk kez keşfedilen 'Warburg etkisi' (aerobik glikoliz), kanser hücrelerinin bol oksijen "
                "bulunan ortamlarda dahi enerjilerini oksidatif fosforilasyon yerine glikoliz yoluyla glukozu laktata yıkarak "
                "üretmeleri fenomenidir. Normal hücrelerde 1 molekül glukoz mitokondride tam yakılarak 36 ATP üretirken, kanser "
                "hücresi glikolizle yalnızca 2 ATP üretir. İlk bakışta verimsiz görünen bu metabolik adaptasyon, hızla bölünen "
                "tümör hücresine devasa bir avantaj sağlar: Glukoz karbon iskeletleri mitokondride karbondioksite yakılmak yerine, "
                "hücre bölünmesi için mutlak gerekli olan nükleotid (riboz), lipit ve amino asit sentezi yolaklarına yönlendirilir. "
                "Bu aşırı glukoz açlığı, klinik onkolojide Florodeoksiglukoz PET (FDG-PET) görüntülemenin temel prensibini oluşturur."
            ),
            "elements": [
                make_cloze(
                    "Kanser hücrelerinin oksijen varlığında bile glukozu laktata yıkarak biyosentetik öncüller üretmesine Warburg etkisi denir.",
                    "Warburg etkisi",
                    "Aerobik glikoliz olgusu"
                ),
                make_micro_quiz(
                    "Kanser hücrelerinin verimsiz glikoliz yolunu tercih etmesindeki (Warburg etkisi) temel biyolojik amaç nedir?",
                    [
                        {
                            "text": "Glukoz ara ürünlerini nükleotid, amino asit ve lipid biyosentezi için yapıtaşı olarak kullanmak",
                            "isCorrect": True,
                            "explanation": "Doğrudur; hızlı bölünme için maksimum ATP değil maksimum biyosentetik yapıtaşı gerekir."
                        },
                        {
                            "text": "Mitokondrileri tamamen yok ederek vücut ısısını 30 dereceye düşürmek",
                            "isCorrect": False,
                            "explanation": "Vücut ısısını düşürmek amacıyla metabolizma değişmez."
                        },
                        {
                            "text": "Hücrenin içine giren tüm oksijeni helyum gazına dönüştürmek",
                            "isCorrect": False,
                            "explanation": "Biyokimyada nükleer element dönüşümü gerçekleşmez."
                        },
                        {
                            "text": "DNA zincirlerini tamamen eritip yok etmek",
                            "isCorrect": False,
                            "explanation": "Tümör hücresi çoğalmak için DNA'yı korumak ve kopyalamak zorundadır."
                        }
                    ],
                    "Warburg etkisi hücreye biyosentetik inşaat malzemeleri sağlar."
                )
            ]
        },
        # Slayt 8
        {
            "slideNumber": 8,
            "title": "Replikatif Ölümsüzlük ve Telomeraz Aktivasyonu",
            "content": (
                "Normal insan somatik hücreleri sınırsız bölünme kapasitesine sahip değildir; yaklaşık 50-70 bölünme sonrasında "
                "(Hayflick sınırı) replikatif yaşlanmaya (senesens) girer ve kalıcı olarak bölünmeyi durdurur. Bunun moleküler "
                "nedeni, her DNA replikasyonunda kromozom uçlarındaki koruyucu 'telomer' tekrarlarının (TTAGGG) kısalmasıdır. "
                "Kritik telomer kısalığı p53 ve RB tarafından çift zincir DNA kırığı olarak algılanır ve hücre döngüsü durdurulur. "
                "Kanser hücreleri ise ya p53/RB inaktivasyonuyla bu kontrolü aşar ya da vakaların %85-90'ında 'telomeraz' "
                "(hTERT) enzimini reaktive ederek telomer boyunu sürekli uzatır. Telomer boyunun korunması tümör hücresine "
                "'replikatif ölümsüzlük' (immortalite) kazandırarak nesiller boyu sınırsız çoğalma potansiyeli sunar."
            ),
            "elements": [
                make_before_after(
                    "Somatik Hücre vs Kanser Hücresinde Telomer Dinamikleri",
                    "Normal Somatik Hücre",
                    "Telomeraz aktivitesi yoktur; her mitozda telomer kısalır, 50-70 bölünmede Hayflick senesensine girer.",
                    "Kanser Hücresi (Ölümsüz)",
                    "hTERT telomeraz enzimi reaktive edilmiştir; telomerler sürekli onarılır ve sınırsız mitoz gerçekleşir.",
                    "Telomeraz aktivasyonu tümörlerin replikatif ölümsüzlük kazanmasının anahtarıdır."
                ),
                make_active_recall(
                    "Kanser hücrelerinin yaklaşık yüzde doksanında reaktive olarak sınırsız çoğalma (ölümsüzlük) sağlayan enzim nedir?",
                    "Telomeraz (hTERT) enzimidir.",
                    "Kromozom uçlarını uzatan revers transkriptaz"
                )
            ]
        },
        # Slayt 9 [CHECKPOINT 1]
        {
            "slideNumber": 9,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Neoplazi İlkeleri ve Kanser Hallmarks",
            "content": (
                "Bu bölümde neoplazinin temel prensiplerini, hücresel kompartmanlarını ve kanser hallmarks kavramını inceledik. "
                "Neoplazi, uyarandan bağımsız olarak otonom çoğalan anormal doku kitlesidir; kanser malign neoplazmları kapsar. "
                "Tümörler iki bileşenden oluşur: Biyolojik davranışı belirleyen ve adlandırmayı sağlayan parankim ile konak kökenli destekleyici stroma. "
                "Tümörler monoklonal olarak tek bir hücreden başlar, ancak zamanla genomik instabiliteyle klonal heterojenite kazanır. "
                "Kanserin hallmarks özellikleri arasında otonom büyüme sinyalleri, büyüme baskısına duyarsızlık ve metabolik yeniden programlama yer alır. "
                "RAS onkogeni sürekli GTP bağlı kalarak MAPK yolağını uyarır; RB proteini ise fosforillendiğinde E2F'i salarak G1-S geçişine izin verir. "
                "Warburg etkisi (aerobik glikoliz), tümörün biyosentez için glukozu laktata yıkmasıdır; telomeraz ise ölümsüzlük sağlar."
            ),
            "flashcards": [
                {
                    "id": "k1-28-cp01-fc01",
                    "front": "Neoplazmlarda tümörün biyolojik davranışını, büyüme karakterini ve adlandırılmasını belirleyen temel hücresel bileşen nedir?",
                    "back": "Parankim bileşenidir.",
                    "hint": "Transforme klonal hücrelerin oluşturduğu doku"
                },
                {
                    "id": "k1-28-cp01-fc02",
                    "front": "Kanser hücrelerinin bol oksijen varlığında dahi glukozu laktata yıkarak biyosentetik yapıtaşları üretmesi olayına ne ad verilir?",
                    "back": "Warburg etkisi adı verilir.",
                    "hint": "Aerobik glikoliz teriminin mucidi"
                },
                {
                    "id": "k1-28-cp01-fc03",
                    "front": "Hücre döngüsünün G1-S kontrol noktasında E2F transkripsiyon faktörünü hapsederek fren görevi gören kilit protein hangisidir?",
                    "back": "Retinoblastom etkenidir.",
                    "hint": "Çocukluk dönemi intraoküler kitle baskılayıcısı"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 1 Özet Tablosu: Moleküler Karsinogenez Temelleri",
                    ["Moleküler Kavram", "Kilit Oyuncu / Enzim", "Hücresel Anlamı"],
                    [
                        {
                            "cells": ["Aerobik Glikoliz", "Warburg Etkisi", "Hızlı biyosentez ve laktat üretimi"],
                            "hiddenIndex": 0,
                            "hint": "Metabolik yeniden programlama"
                        },
                        {
                            "cells": ["G1-S Döngü Freni", "Retinoblastom (RB)", "E2F faktörünün bağlanması ve baskılanması"],
                            "hiddenIndex": 1,
                            "hint": "Hipofosforile aktif kontrol proteini"
                        }
                    ]
                )
            ]
        },
        # Slayt 10
        {
            "slideNumber": 10,
            "title": "Klinik Karar: Tümör Stroma Oranı ve Agresiflik",
            "content": (
                "Patoloji raporlarında tümörün stromal yanıtı ve hücresel proliferasyon indeksi dikkatle analiz edilmelidir. "
                "Yoğun dezmoplastik stroma içeren meme ve pankreas adenokarsinomlarında parankim hücreleri yoğun kolajen "
                "lifleri arasına gömülüdür; bu yoğun fibrotik stroma intratümöral interstisyel sıvı basıncını aşırı yükselterek "
                "kemoterapötik ilaçların damardan parankim hücrelerine difüzyonunu fiziksel olarak engeller. Buna karşılık "
                "stroması zayıf ve hücreden zengin medüller karsinomlarda kanlanma yetersiz kalarak geniş harita tarzı "
                "nekrozlar gözlenir. Patolog, proliferasyon oranını Ki-67 immünohistokimyasal boyamasıyla belirleyerek onkoloğa "
                "kemoterapiye yanıt ve tümör agresifliği konusunda doğrudan rehberlik eder."
            ),
            "elements": [
                make_branching_logic(
                    "56 yaşında kadın hastanın meme kitle biyopsisinde yoğun fibröz kolajen lifleri arasına sıkışmış infiltratif tümör hücreleri (belirgin dezmoplazi) saptanıyor. Tümör klinik olarak taş gibi sert hissediliyor.",
                    "Bu dezmoplastik stromal tablonun hastanın kemoterapi yanıtı ve klinik özellikleri açısından anlamı nedir?",
                    [
                        {
                            "text": "Konak fibroblastlarının aşırı kolajen üretmesi (dezmoplazi) interstisyel basıncı artırarak intravenöz kemoterapi ilaçlarının tümör içine penetrasyonunu zorlaştırır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; dezmoplazi fiziksel bir ilaç bariyeri oluşturur ve kitleye taş sertliği verir."
                        },
                        {
                            "text": "Dezmoplazi kitlenin tamamen iyi huylu bir kist olduğunu kanıtlar.",
                            "isCorrect": False,
                            "explanation": "Dezmoplazi malign karsinomların tipik stromal yanıtıdır, kist değildir."
                        },
                        {
                            "text": "Tümör hücrelerinin tamamen öldüğünü ve cerrahiye gerek kalmadığını gösterir.",
                            "isCorrect": False,
                            "explanation": "Tümör hücreleri canlıdır ve stroma içinde çevre dokuya yayılmaktadır."
                        }
                    ]
                )
            ]
        }
    ]
