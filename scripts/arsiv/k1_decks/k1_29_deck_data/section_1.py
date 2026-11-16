# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 29: Karsinojenezin Moleküler Temeli
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 1: Kanser Genlerinin Sınıflaması ve Moleküler Temelleri (Slayt 1 - 10)
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
            "title": "Karsinogenezin Moleküler Temeline Giriş",
            "content": (
                "Karsinogenez, normal bir hücrenin genetik ve epigenetik hasarların aşamalı birikimi sonucu otonom "
                "büyüme ve sınırsız çoğalma yeteneği kazanarak malign neoplazma dönüşmesi sürecidir. Tümörler "
                "klonal kökenlidir; yani karsinogenez tek bir transforme öncül kök hücrenin monoklonal genişlemesiyle "
                "başlar. Ancak tümör hücresi çoğaldıkça genomik istikrarsızlık devreye girer ve zamanla farklı genetik "
                "sapmalar taşıyan subklonlar türer; bu duruma tümörün subklonal heterojenitesi denir. Neoplastik "
                "dönüşümü yöneten hedef genler tesadüfi olmayıp, hücre proliferasyonunu, genomik bütünlüğü, programlı "
                "ölümü ve mikroçevre etkileşimini kontrol eden spesifik **kanser genleridir**."
            ),
            "elements": [
                make_cloze(
                    "Malign karsinogenez tek bir genetik sapmaya uğramış transforme hücrenin monoklonal çoğalmasıyla başlar.",
                    "monoklonal",
                    "Tek atasal hücreden türeme durumu"
                ),
                make_active_recall(
                    "Tümörlerin tek bir transformed hücreden köken almasına karşın geliştikçe farklı mutasyonlara sahip alt gruplar içermesine ne ad verilir?",
                    "Klonal heterojenite (subklonal çeşitlilik) adı verilir.",
                    "Farklılaşan alt grup çeşitliliği"
                )
            ]
        },

        # Slayt 2
        {
            "slideNumber": 2,
            "title": "Protoonkogenler ve Onkogenler",
            "content": (
                "Normal hücre bölünmesini, büyüme faktörü sinyal iletimini ve hücre sağkalımını uyaran fizyolojik "
                "genlere **protoonkogen** adı verilir. Protoonkogenler nokta mutasyonları, kromozomal translokasyonlar "
                "veya gen amplifikasyonları sonucunda kontrolsüz ve otonom aktifleşerek **onkogenlere** dönüşürler. "
                "Onkogenler tarafından üretilen mutant proteinlere **onkoprotein** denir. Onkoproteinlerin en kritik "
                "özelliği, normal fizyolojik geri bildirim (feedback) mekanizmalarına yanıt vermemeleri ve dışarıdan "
                "büyüme uyarısı gelmeksizin kesintisiz mitojenik sinyal pompalamalarıdır. Onkogen aktivasyonu "
                "**işlev kazanımı (gain-of-function)** türü bir mutasyondur ve kural olarak tek bir alelin "
                "mutasyona uğraması (**dominant etki**) neoplastik fenotipin ortaya çıkması için yeterlidir."
            ),
            "elements": [
                make_table(
                    "Protoonkogen ve Onkogen Temel Karşılaştırması",
                    ["Genetik Durum", "Mutasyonun Biyolojik Tipi", "Gereken Mutant Alel Sayısı", "Kalıtım Davranışı"],
                    [
                        {
                            "cells": ["Onkogenler", "İşlev kazanımı (Gain-of-function)", "Tek bir alel yeterlidir", "Dominant fenotip"],
                            "hiddenIndex": 1,
                            "hint": "Fazladan aktivite artışı tipi"
                        },
                        {
                            "cells": ["Tümör Baskılayıcılar", "İşlev kaybı (Loss-of-function)", "İki alelin inaktivasyonu gerekir", "Resesif hücresel fenotip"],
                            "hiddenIndex": 1,
                            "hint": "Aktivitenin ortadan kalkması durumu"
                        }
                    ]
                ),
                make_cloze(
                    "Protoonkogenlerin onkogene dönüşümünde tek bir alelin mutasyonu yeterli olup bu durum dominant kalıtım sergiler.",
                    "dominant",
                    "Tek kopya ile baskın karakter"
                )
            ]
        },

        # Slayt 3
        {
            "slideNumber": 3,
            "title": "Tümör Baskılayıcı Genler ve Knudson İki Vuruş Modeli",
            "content": (
                "Tümör baskılayıcı genler (TSG), hücre siklusunu yavaşlatan, hücre bölünmesini frenleyen ve DNA "
                "hasarı saptandığında apoptozu indükleyen koruyucu bekçilerdir. Bu genlerin neoplaziye yol açması "
                "için **işlev kaybı (loss-of-function)** mutasyonuna uğramaları gerekir. Alfred Knudson tarafından "
                "retinoblastom modeli üzerinden tanımlanan **'iki vuruş (two-hit) hipotezine'** göre, tümör "
                "baskılayıcı etkinin ortadan kalkması için her iki alelin de inaktive olması şarttır (hücresel düzeyde "
                "resesif davranış). Kalıtsal kanser sendromlarında birinci darbe germline olarak anne veya babadan "
                "kalıtılır ve bireyin vücudundaki tüm hücrelerde mevcuttur. Hedef dokuda ikinci alelin somatik "
                "mutasyon veya delesyonla yitirilmesi (**heterozigotluk kaybı - LOH**) neoplastik proliferasyonu tetikler."
            ),
            "elements": [
                make_before_after(
                    "Knudson İki Vuruş Hipotezi: Familyal vs Sporadik Model",
                    "Familyal (Kalıtsal) Model",
                    "Birinci vuruş germline taşınır (tüm hücrelerde 1 mutant alel). Tek bir somatik vuruş tümör başlatır; bilateral ve erken yaştadır.",
                    "Sporadik (Kalıtsal Olmayan) Model",
                    "Aynı hücrede bağımsız iki somatik mutasyonun ardışık gerçekleşmesi gerekir; tek taraflı ve ileri yaşta görülür.",
                    "Kalıtsal kanserlerde ikinci darbenin gerçekleşme olasılığı çok yüksek olduğundan kanser riski katbekat artar."
                ),
                make_active_recall(
                    "Kalıtsal kanser sendromlarında sağlam olan ikinci alelin somatik olarak kaybedilmesine ne ad verilir?",
                    "Heterozigotluk kaybı (Loss of Heterozygosity - LOH) adı verilir.",
                    "Alel çifti tekleşmesi terimi"
                )
            ]
        },

        # Slayt 4
        {
            "slideNumber": 4,
            "title": "Kapı Bekçileri (Gatekeepers) ve Bakımcılar (Caretakers)",
            "content": (
                "Tümör baskılayıcı genler hücresel işlevlerine göre iki ana sınıfa ayrılır: **Kapı bekçileri "
                "(Gatekeepers)** ve **Bakımcılar (Caretakers)**. Kapı bekçisi genler (örneğin RB1, TP53, APC), "
                "hücre büyümesini, siklus kontrol noktalarını ve apoptozu doğrudan denetleyen genlerdir. Bu genlerin "
                "çift alelik kaybı, hücrenin fren mekanizmalarını felç ederek doğrudan otonom proliferasyona yol açar. "
                "Buna karşılık bakımcı genler (örneğin MSH2, MLH1, BRCA1, BRCA2, XP genleri), doğrudan hücre siklusunu "
                "durdurmaz; DNA hasarını onararak genomun bütünlüğünü korur. Bakımcı genler inaktive olduğunda hücre "
                "bölünmesi anında hızlanmaz; ancak hücrede binlerce mutasyonun süratle biriktiği bir **mutatör fenotip** "
                "doğar; bu zemin kapı bekçisi genlerin de kaçınılmaz olarak mutasyona uğramasını hızlandırır."
            ),
            "elements": [
                make_table(
                    "Gatekeeper vs Caretaker Genlerin Ayrımı",
                    ["Kategori", "Temel Biyolojik Rol", "Prototipik Gen Örnekleri", "İnaktivasyon Sonucu"],
                    [
                        {
                            "cells": ["Kapı Bekçisi (Gatekeeper)", "Hücre siklusu ve apoptozun doğrudan kontrolü", "RB1, TP53, APC", "Hemen kontrolsüz hücre çoğalması"],
                            "hiddenIndex": 2,
                            "hint": "P53 ve retinoblastom genleri"
                        },
                        {
                            "cells": ["Bakımcı (Caretaker)", "DNA hasar tespiti ve genom tamiri", "MSH2, MLH1, BRCA1, XPA", "Genomik instabilite ve mutatör fenotip"],
                            "hiddenIndex": 2,
                            "hint": "Meme ve bağırsak onarım proteinleri"
                        }
                    ]
                ),
                make_micro_quiz(
                    "Doğrudan hücre döngüsünü durdurmayan ancak DNA tamirini yöneterek genomik istikrarı sağlayan ve mutasyon hızını kontrol altında tutan tümör baskılayıcı gen sınıfı hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "Protoonkogenler",
                            "isCorrect": False,
                            "explanation": "Protoonkogenler büyümeyi teşvik eden genlerdir."
                        },
                        {
                            "key": "B",
                            "text": "Bakımcı (Caretaker) genler",
                            "isCorrect": True,
                            "explanation": "Caretaker (bakımcı) genler DNA onarımını ve genomik stabiliteyi korur (ör. BRCA1, MSH2, MLH1)."
                        },
                        {
                            "key": "C",
                            "text": "Kapı bekçisi (Gatekeeper) genler",
                            "isCorrect": False,
                            "explanation": "Gatekeeper genler hücre döngüsünü doğrudan durduran frenlerdir (RB1, TP53, APC)."
                        },
                        {
                            "key": "D",
                            "text": "Anjiyogenik büyüme faktörleri",
                            "isCorrect": False,
                            "explanation": "Anjiyogenik faktörler damar yapımını uyarır."
                        }
                    ],
                    "Caretaker genler DNA tamiri yaparak genomun koruyucu bakımını üstlenir."
                )
            ]
        },

        # Slayt 5
        {
            "slideNumber": 5,
            "title": "Apoptozu Düzenleyen Genler: İçsel Mitokondriyal Yol",
            "content": (
                "Programlı hücre ölümü olan apoptoz, genomik hasara uğramış veya gereksiz hücrelerin doku bütünlüğüne "
                "zarar vermeden ortadan kaldırılmasını sağlar. Malign hücrelerin en belirleyici ayırt edici "
                "özelliklerinden biri apoptozdan kaçınarak ölümsüzlük kazanmalarıdır. Apoptozun ana regülasyon "
                "merkezi **içsel (mitokondriyal) apoptotik yoldur**. Bu yol mitokondri dış zar geçirgenliğini "
                "(MOMP) kontrol eden **BCL2 gen ailesi** tarafından yönetilir. Normalde DNA hasarı veya hücresel stres "
                "algılandığında mitokondri membranında gözenekler açılır ve sitoplazmaya **Sitokrom c** salınır. "
                "Sitokrom c, APAF-1 kofaktörü ile birleşerek apoptazom kompleksini kurar ve kaspaz-9 aktivasyonu "
                "üzerinden yürütücü kaspazları (kaspaz-3, kaspaz-7) tetikleyerek hücreyi parçalar."
            ),
            "elements": [
                make_causal_chain(
                    "İçsel Mitokondriyal Apoptoz Sinyal İletim Kaskadı",
                    [
                        "1. Genomik Hasar Algısı: Şiddetli DNA hasarı p53 aracılığıyla BH3-only proapoptotik proteinleri tetikler.",
                        "2. Mitokondriyal Delinme: BAX ve BAK oligomerize olarak mitokondri dış zarında geçirgenlik gözenekleri açar.",
                        "3. Sitokrom c Boşalımı: İntermembranöz aralıkta depolanan Sitokrom c molekülleri sitoplazmaya dökülür.",
                        "4. Apoptazom Montajı: Sitokrom c ve APAF-1 birleşerek tekerlek benzeri apoptazom oligomerini kurar.",
                        "5. Kaspaz Kaskadı İnfazı: Apoptazom prokaspaz-9'u kesip aktifleştirir, o da yürütücü kaspaz-3'ü devreye sokar."
                    ]
                ),
                make_cloze(
                    "Mitokondri membran geçirgenliğinin artması sonucu sitoplazmaya salınarak apoptazomu kuran elektron taşıma proteini Sitokrom c'dir.",
                    "Sitokrom",
                    "Hem içeren mitokondriyel solunum molekülü"
                )
            ]
        },

        # Slayt 6
        {
            "slideNumber": 6,
            "title": "BCL2 Ailesi Dengesi: Proapoptotik vs Antiapoptotik Gruplar",
            "content": (
                "İçsel mitokondriyal apoptoz yolu, BCL2 protein ailesine mensup üç fonksiyonel grup arasındaki "
                "hassas denge ile idare edilir. Birinci grup **antiapoptotik proteinlerdir (BCL2, BCL-XL, MCL1)**; "
                "bu moleküller mitokondri dış zarında oturarak zarı stabilize eder ve Sitokrom c sızıntısını önler. "
                "İkinci grup **proapoptotik efektörlerdir (BAX ve BAK)**; aktifleştiklerinde zarda por açarak "
                "ölümü gerçekleştirirler. Üçüncü grup ise hücresel stres sensörleri olan **BH3-only proteinleridir "
                "(BAD, BID, BIM, PUMA, NOXA)**. Kanser hücrelerinde bu denge dramatik şekilde antiapoptotik BCL2 "
                "lehine bozulur. Örneğin foliküler lenfomada t(14;18) translokasyonu sonucu BCL2 geni aşırı miktarda "
                "üretilir; BAX ve BAK nötralize edilir ve apoptoz engellendiği için B lenfositleri ölümsüzleşir."
            ),
            "elements": [
                make_table(
                    "BCL2 Ailesi Üçlü Fonksiyonel Sınıflaması",
                    ["Fonksiyonel Grup", "Kilit Protein Üyeleri", "Hücresel Görevi", "Kanser Hücresindeki Durumu"],
                    [
                        {
                            "cells": ["Antiapoptotik Grubu", "BCL2, BCL-XL, MCL1", "Mitokondri zarını stabilize ederek por açılmasını önler", "Aşırı ekspresyon (Ölüme direnç)"],
                            "hiddenIndex": 1,
                            "hint": "B lenfoma onkogeni ailesi"
                        },
                        {
                            "cells": ["Proapoptotik Efektörler", "BAX, BAK", "Mitokondri dış zarında porlar açarak Sitokrom c salar", "İnaktivasyon veya baskılanma"],
                            "hiddenIndex": 1,
                            "hint": "Ölümü doğrudan icra eden ikili"
                        },
                        {
                            "cells": ["BH3-Only Sensörleri", "BAD, BID, BIM, PUMA, NOXA", "Antiapoptotikleri nötralize edip BAX/BAK'ı tetikler", "Susturulma veya kaybı"],
                            "hiddenIndex": 1,
                            "hint": "Stres algılayıcı başlatıcı moleküller"
                        }
                    ]
                ),
                make_active_recall(
                    "Foliküler lenfomada t(14;18) translokasyonu sonucunda aşırı üretilerek apoptozu bloke eden antiapoptotik onkoprotein hangisidir?",
                    "BCL2 proteinidir (B-cell lymphoma 2).",
                    "Lenfoid apoptoz engelleyici faktör"
                )
            ]
        },

        # Slayt 7
        {
            "slideNumber": 7,
            "title": "Tümör-Konak Etkileşim Genleri: Anjiyogenez",
            "content": (
                "Tümör nodülleri 1-2 milimetre çapa ulaştıklarında oksijen ve besin difüzyon sınırına takılırlar. "
                "Bu aşamadan sonra büyümenin ve metastazın sürebilmesi için tümörün kendi yeni damar ağını kurması "
                "(neoanjiyogenez) zorunludur; bu kritik biyolojik eşiğe **anjiyogenik anahtarın açılması (angiogenic "
                "switch)** adı verilir. Tümör hipoksisi, prolil hidroksilaz enzimlerini inaktive ederek transkripsiyon "
                "faktörü **HIF-1alfa'yı (Hipoksi İle İndüklenen Faktör)** stabilize eder. HIF-1alfa nükleusa geçerek "
                "en güçlü damar yapıcı sitokin olan **VEGF (Vasküler Endotelyal Büyüme Faktörü)** ve bFGF genlerini "
                "aktive eder. Eş zamanlı olarak fizyolojik anjiyogenez inhibitörleri olan **trombospondin-1 (TSP-1)** "
                "ve anjiyostatin yapımı baskılanır. Tümör damarları normal damarlardan farklı olarak kıvrıntılı, "
                "düzensiz, perisitsiz ve son derece sızıntılıdır (hiperpermeabl)."
            ),
            "elements": [
                make_before_after(
                    "Normal Doku Damarlanması ile Tümör Neoanjiyogenezinin Farkı",
                    "Normal Doku Damar Ağı",
                    "Düzenli dallanma, sağlam bazal membran, perisit desteği ve kontrollü endotelyal geçirgenlik.",
                    "Tümörün Neoanjiyogenik Damarları",
                    "Düzensiz, kıvrıntılı, hiperpermeabl, kör uçlu ve perisit desteğinden yoksun kaotik kılcal ağ.",
                    "Sızıntılı damarlar intratümöral basıncı artırarak ilaç dağılımını zorlaştırır ve metastaza geçit verir."
                ),
                make_cloze(
                    "Hipoksi durumunda parçalanmaktan kurtulup VEGF transkripsiyonunu başlatan kilit transkripsiyon faktörü HIF-1alfa molekülüdür.",
                    "HIF-1alfa",
                    "Oksijen düşüklüğünde indüklenen transkripsiyon faktörü"
                )
            ]
        },

        # Slayt 8
        {
            "slideNumber": 8,
            "title": "Tümör-Konak Etkileşimi: İnvazyon ve İmmün Kontrol",
            "content": (
                "Kanser hücrelerinin çevre dokuya invaze olması ve metastaz yapması, stromal matriks ile girdikleri "
                "özel genetik ve biyokimyasal etkileşimlere bağlıdır. Epitelyal hücreleri birbirine sıkıca bağlayan "
                "**E-kadherin** molekülünün kaybı, kanser hücrelerinin birbirinden bağımsız hareket etmesini sağlar. "
                "Eş zamanlı salınan **Matriks Metalloproteinazlar (MMP-2, MMP-9)** bazal membranın Tip IV kolajenini "
                "eriterek stromal geçitler açar. İmmün gözetimden kaçış cephesinde ise, kanser hücreleri yüzeylerinde "
                "**PD-L1 (Programlanmış Ölüm Ligandı 1)** ekspresyonunu artırırlar. PD-L1, sitotoksik CD8+ T hücrelerinin "
                "yüzeyindeki **PD-1** reseptörüne kenetlenerek lenfositin sitotoksik aktivitesini felç eder (anerji). "
                "Ayrıca sitotoksik T hücrelerinin erken aktivasyonunu engelleyen **CTLA-4** yolu da tümör tarafından "
                "istismar edilen bir diğer immün kontrol noktası frenidir."
            ),
            "elements": [
                make_table(
                    "Tümör İnvazyonu ve İmmün Kaçışın Moleküler Araçları",
                    ["Biyolojik İşlem", "Kilit Gen / Molekül", "Normal Görevi", "Kanser Hücresindeki Rolü"],
                    [
                        {
                            "cells": ["Hücrelerarası Adezyon", "E-kadherin (CDH1)", "Epitel hücrelerini bir arada tutar", "İnaktivasyon ile hücrelerin birbirinden kopması"],
                            "hiddenIndex": 1,
                            "hint": "Kalsiyum bağımlı epitel yapıştırıcısı"
                        },
                        {
                            "cells": ["Matriks Yıkımı", "MMP-2 ve MMP-9 (Jelatinazlar)", "Doku remodelingi", "Tip IV kolajen ve bazal membran delinmesi"],
                            "hiddenIndex": 1,
                            "hint": "Metalo-proteaz enzim ailesi"
                        },
                        {
                            "cells": ["T Hücre Felci (Anerji)", "PD-L1 ve CTLA-4", "Otoimmüniteyi önleyen kontrol noktası", "Sitotoksik lenfositlerin susturulması"],
                            "hiddenIndex": 1,
                            "hint": "Programlı ölüm ligandı ekseni"
                        }
                    ]
                ),
                make_active_recall(
                    "Kanser hücrelerinin yüzeyinde eksprese ederek sitotoksik CD8+ T lenfositleri anerjiye soktuğu temel immün kontrol noktası ligandı nedir?",
                    "PD-L1 molekülüdür (Programmed Death-Ligand 1).",
                    "Lenfosit baskılayıcı tümöral yüzey ligandı"
                )
            ]
        },

        # Slayt 9: CHECKPOINT 1
        {
            "slideNumber": 9,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Kanser Genlerinin Moleküler Sınıflaması",
            "content": (
                "Birinci bölümün bu tekrar sayfasında, neoplastik transformasyonu yöneten dört temel kanser "
                "geni sınıfı özetlenmektedir. Protoonkogenler işlev kazanımı mutasyonlarıyla dominant karakterde "
                "onkogenlere dönüşür ve tek alel mutasyonu yeterlidir. Tümör baskılayıcı genler Knudson'ın iki "
                "vuruş kuralına uyarak çift alelik işlev kaybıyla inaktive olur; kapı bekçileri (gatekeepers) "
                "hücre döngüsünü doğrudan durdururken, bakımcılar (caretakers) DNA onarımını ve genomik stabiliteyi "
                "sağlar. Apoptoz cephesinde proapoptotik BAX/BAK por açarak Sitokrom c salarken, antiapoptotik BCL2 "
                "zarı stabilize eder. Tümör-konak etkileşiminde ise HIF-1alfa/VEGF aksı sızıntılı neoanjiyogenezi "
                "tetiklerken, E-kadherin kaybı ve MMP'ler invazyonu, PD-L1 ise lenfosit kaçışını yönetir."
            ),
            "flashcards": [
                {
                    "id": "k1-29-cp01-fc01",
                    "front": "Protoonkogenlerin kontrolsüz aktifleşerek onkogene dönüşmesinde rol oynayan mutasyonun biyolojik tipi ve kalıtım karakteri nedir?",
                    "back": "İşlev kazanımı (gain-of-function) ve dominant kalıtımdır.",
                    "hint": "Aktivite artışı ve baskın fenotip"
                },
                {
                    "id": "k1-29-cp01-fc02",
                    "front": "Tümör baskılayıcı genlerde Knudson'ın iki vuruş kuralına göre fenotipik etkinin kalkması için kaç alelin inaktive olması gerekir?",
                    "back": "Her iki alelin de inaktive olması gerekir (resesif davranış).",
                    "hint": "Çift kopya kaybı kuralı"
                },
                {
                    "id": "k1-29-cp01-fc03",
                    "front": "İçsel mitokondriyal apoptoz yolunda mitokondri dış zarında porlar açarak Sitokrom c salınımını icra eden proapoptotik efektör moleküller hangileridir?",
                    "back": "BAX ve BAK proteinleridir.",
                    "hint": "Mitokondriyi delen apoptotik ikili"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 1 Özet Tablosu: Kanser Genleri Sınıflaması",
                    ["Gen Grubu", "Temel Mekanizma", "Kritik Temsilci Genler"],
                    [
                        {
                            "cells": ["Onkogenler", "İşlev kazanımı (Dominant, tek alel)", "RAS, MYC, HER2/ERBB2"],
                            "hiddenIndex": 1,
                            "hint": "Aşırı büyüme sinyali üreten aktivasyon"
                        },
                        {
                            "cells": ["Tümör Baskılayıcılar", "İşlev kaybı (Resesif, iki alel)", "TP53, RB1, APC"],
                            "hiddenIndex": 1,
                            "hint": "Döngü frenlerinin çift taraflı düşmesi"
                        }
                    ]
                )
            ]
        },

        # Slayt 10
        {
            "slideNumber": 10,
            "title": "Klinik Karar: Germline ve Somatik Mutasyon Ayrımı",
            "content": (
                "Klinik onkolojide bir hastada saptanan sürücü mutasyonun germline (kalıtsal) mı yoksa somatik "
                "(edinsel) mi olduğunu ayırt etmek tedavi ve genetik danışma açısından hayati rol oynar. Germline "
                "mutasyonlar organizmanın sperm veya oosit hücresinde mevcuttur; bu nedenle bireyin vücudundaki "
                "tüm hücrelerde (lökositler, mukoza epiteli vb.) tek kopya olarak saptanır. Bu hastalar genç yaşta "
                "tümör geliştirme, bilateral organ tutulumu ve aile bireylerinde aynı kanser kümelenmesi riski "
                "taşırlar. Somatik mutasyonlar ise yalnızca hedef organdaki neoplastik hücre klonuna özgüdür; çevre "
                "normal dokuda veya kanda saptanmazlar. Yeni nesil dizileme (NGS) yapılırken tümör biyopsisi "
                "ile eş zamanlı hastanın periferik kan lenfosit DNA'sının birlikte analiz edilmesi bu ayrımı sağlar."
            ),
            "elements": [
                make_branching_logic(
                    "31 yaşında kadın hastaya sağ memede invaziv duktal karsinom tanısı konuyor. Aile öyküsünde annesinde 42 yaşında bilateral meme kanseri ve teyzesinde over kanseri olduğu öğreniliyor. Tümör dokusunun moleküler analizinde BRCA1 geninde mutasyon saptanıyor.",
                    "Bu hastada genetik yatkınlığı doğrulamak ve birinci derece yakınlarını korumak için patoloji ve tıbbi genetik konseyinin atması gereken en doğru adım nedir?",
                    [
                        {
                            "text": "Hastanın periferik kan lenfositlerinden DNA izole edilerek germline BRCA1 mutasyonu araştırılmalı; pozitif çıkarsa kontralateral meme ve over tarama/profilaksi protokolü başlatılmalıdır.",
                            "isCorrect": True,
                            "explanation": "Genç yaş ve güçlü aile öyküsü kalıtsal germline mutasyonu düşündürür. Periferik kanda mutasyonun gösterilmesi germline olduğunu kanıtlar ve sistemik korunma sağlar."
                        },
                        {
                            "text": "Mutasyon sadece tümör dokusunda görüldüğünden aile için hiçbir risk yoktur; genetik test yapılmasına gerek bulunmamaktadır.",
                            "isCorrect": False,
                            "explanation": "Genç yaş ve aile kümelenmesi germline mutasyon olasılığını son derece yükseltir; kan analizi şarttır."
                        },
                        {
                            "text": "Hastada Knudson'ın iki vuruş hipotezinin geçersiz olduğu kabul edilerek sadece lokal radyoterapi verilmelidir.",
                            "isCorrect": False,
                            "explanation": "BRCA kalıtsal meme kanserleri Knudson hipotezine tam olarak uyar; LOH ile tümör gelişir."
                        }
                    ]
                ),
                make_micro_quiz(
                    "Kalıtsal kanser sendromlarında hastanın tüm vücut somatik hücrelerinde bulunan ve bir sonraki kuşağa %50 olasılıkla aktarılan mutasyon türü hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "Somatik sürücü mutasyon",
                            "isCorrect": False,
                            "explanation": "Somatik mutasyonlar yalnızca hedef doku klonunda bulunur, kalıtılmaz."
                        },
                        {
                            "key": "B",
                            "text": "Germline (üreme hücresi kökenli) mutasyon",
                            "isCorrect": True,
                            "explanation": "Germline mutasyonlar gametlerden aktarılır, bireyin tüm hücrelerinde mevcuttur ve otozomal dominant kalıtılabilir."
                        },
                        {
                            "key": "C",
                            "text": "Yolcu (passenger) mutasyon",
                            "isCorrect": False,
                            "explanation": "Passenger mutasyonlar tümör gelişimi sırasında biriken nötr somatik sapmalardır."
                        },
                        {
                            "key": "D",
                            "text": "Epizomal viral entegrasyon",
                            "isCorrect": False,
                            "explanation": "Viral epizomlar enfeksiyon sonrası edinilir, mendelyen germline kalıtım göstermez."
                        }
                    ],
                    "Germline mutasyonlar döllenme anından itibaren tüm vücut hücrelerinde mevcuttur."
                )
            ]
        }
    ]
