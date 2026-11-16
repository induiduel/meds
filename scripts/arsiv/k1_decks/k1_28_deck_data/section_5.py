# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi
Bölüm 5: Karma Tümörler, Teratom, Hamartom ve Koristom (Slayt 41 - 50)
Checkpoint: Slayt 49
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_5_slides():
    return [
        # Slayt 41
        {
            "slideNumber": 41,
            "title": "Özel Neoplazmlar ve Terminolojik Ayrım Mantığı",
            "content": (
                "Standart tümör terminolojisi, bir kitlede tek bir parankimal hücre tipinin (örneğin sadece fibroblast veya "
                "sadece duktus epiteli) çoğaldığı monomorfik neoplazmlar üzerine kuruludur. Ancak insan patolojisinde tek "
                "bir germ yaprağından köken alıp birden fazla hücre hattına farklılaşan veya birden fazla embriyonik germ "
                "yaprağını (ektoderm, mezoderm, endoderm) içeren çok yönlü doku kitleleri de bulunur. Bu özel tümör kümesi; "
                "tek klondan türeyen 'karma (mikst) tümörleri', totipotent germ hücrelerinden doğan 'teratomları', ait olduğu "
                "organda olgun dokuların düzensiz kümelenmesi olan 'hamartomları' ve ektopik olgun doku adacıklarını temsil eden "
                "'koristomları' kapsar. Bu lezyonların histogenetik sınırlarını bilmek sınav ve klinik tanı için vazgeçilmezdir."
            ),
            "elements": [
                make_table(
                    "Özel Tümör Kategorileri ve Histogenetik Temelleri",
                    ["Kategori", "Embriyolojik / Klonal Köken", "İçerdiği Doku Bileşenleri", "Tipik Örnek"],
                    [
                        {
                            "cells": ["Karma (Mikst) Tümör", "Tek bir multipotent klon", "Birden fazla diferansiyasyon hattı (epitel + miksoid/kıkırdak)", "Tükürük bezi pleomorfik adenomu"],
                            "hiddenIndex": 3,
                            "hint": "Parotisin en sık iyi huylu kitlesi"
                        },
                        {
                            "cells": ["Teratom", "Totipotent germ hücreleri", "Birden fazla germ yaprağı (ektoderm, mezoderm, endoderm)", "Over dermoid kisti / matür teratom"],
                            "hiddenIndex": 3,
                            "hint": "Yumurtalık kistik saçlı/dişli kitlesi"
                        },
                        {
                            "cells": ["Hamartom", "Organın kendi hücreleri", "Ait olduğu organ dokularının düzensiz kaotik kitlesi", "Akciğer kondroid hamartomu"],
                            "hiddenIndex": 0,
                            "hint": "Organın yerli doku anormalliği"
                        },
                        {
                            "cells": ["Koristom", "Ektopik normal hücreler", "Tamamen yabancı anatomik konumda olgun doku", "Mide duvarında ektopik pankreas"],
                            "hiddenIndex": 0,
                            "hint": "Heterotopik doku adacığı"
                        }
                    ]
                ),
                make_cloze(
                    "Tek bir neoplastik klondan köken alıp birden fazla hücre hattına diferansiye olan kitlelere karma veya mikst tümör denir.",
                    "karma veya mikst tümör",
                    "Çoklu diferansiyasyon gösteren neoplazm"
                )
            ]
        },
        # Slayt 42
        {
            "slideNumber": 42,
            "title": "Karma (Mikst) Tümörler: Tek Klon, Çift Hat",
            "content": (
                "Karma tümörler (mikst tümörler), sanılanın aksine iki farklı hücrenin aynı anda bağımsız olarak tümörleşmesi "
                "değildir. Moleküler sitogenetik çalışmalar, mikst tümörlerin 'tek bir monoklonal öncül hücreden' doğduğunu "
                "kesin olarak kanıtlamıştır. Bu öncül hücre, neoplastik transformasyon sırasında birden fazla yöne doğru "
                "diferansiye olma (diverjan diferansiyasyon) yeteneğine sahiptir. Örneğin meme fibroadenomunda epitelyal duktus "
                "elemanları ile stromal fibroblastik bağ dokusu eş zamanlı prolifere olur; parotisin pleomorfik adenomunda "
                "ise myoepitelyal hücreler hem glandüler epitel hem de kıkırdak ve kemik benzeri mezenkimal dokular üretir."
            ),
            "elements": [
                make_causal_chain(
                    "Tek Klondan Diverjan Mikst Diferansiyasyona Uzanan Yol",
                    [
                        "1. Monoklonal Başlangıç: Parotiste tek bir öncül myoepitelyal hücrede somatik mutasyon (PLAG1)",
                        "2. Diverjan Farklılaşma: Klonun hem glandüler epitelyal hem de stromal yöne dallanması",
                        "3. Matriks Sentezi: Neoplastik myoepitelyal hücrelerin kondroid ve miksoid ara madde salgılaması",
                        "4. Mikst Morfoloji: Epitelyal duktusların kıkırdaksı ve miksoid zemin içine gömüldüğü pleomorfik kitlenin oluşumu"
                    ]
                ),
                make_active_recall(
                    "Karma (mikst) tümörlerin klonal kökeni hakkında modern moleküler patolojinin kanıtladığı kural nedir?",
                    "Tek bir transforme öncül hücreden (monoklonal) köken aldıkları kuralıdır.",
                    "Tek atasal hücre prensibi"
                )
            ]
        },
        # Slayt 43
        {
            "slideNumber": 43,
            "title": "Pleomorfik Adenom: Tükürük Bezinin Mikst Prototipi",
            "content": (
                "Tükürük bezlerinin en sık görülen tümörü (%60-70) parotis bezinde yerleşen 'pleomorfik adenom'dur "
                "(benign mikst tümör). Histolojik olarak son derece alacalı ve zengin bir manzara sergiler: Bir yanda "
                "asiner ve duktal yapılar oluşturan neoplastik epitel adacıkları, diğer yanda bu yapıları çevreleyen "
                "açık mavi-gri miksoid stroma, hyalen kıkırdak (kondroid) adacıkları ve hatta nadiren lameller kemik trabekülleri "
                "bir arada izlenir. Bu tümör tamamen benign karakterdedir; ancak ince, düzensiz ve lobüllü bir yalancı "
                "kapsüle sahip olduğu için cerrahi olarak enükleasyon yapılırsa kapsül defektlerinden geride mikroskopik "
                "odaklar kalır ve %10-20 oranında lokal nüks gelişir. Yıllar içinde malignleşerek 'karsinoma ek-pleomorfik "
                "adenom' haline gelebilir."
            ),
            "elements": [
                make_before_after(
                    "Pleomorfik Adenomun Histolojik Komponentleri",
                    "Epitelyal Komponent",
                    "Duktal ve glandüler lümenler oluşturan, tabakalar yapan kübik ve myoepitelyal hücreler.",
                    "Mezenkimal Benzeri (Stromal) Komponent",
                    "Gevşek miksoid alanlar, lakünler içinde olgun kondrositler içeren kıkırdak dokusu ve hyalinize kolajen.",
                    "Epitel ve kıkırdağın bir arada bulunması pleomorfik adenomun patognomonik mikst görüntüsüdür."
                ),
                make_cloze(
                    "Tükürük bezinde hem glandüler epitel hem de kıkırdak benzeri miksoid stroma içeren benign mikst tümöre pleomorfik adenom denir.",
                    "pleomorfik adenom",
                    "Parotisin en sık benign karma uru"
                )
            ]
        },
        # Slayt 44
        {
            "slideNumber": 44,
            "title": "Teratomlar: Totipotent Germ Hücrelerinden Çoklu Germ Yaprakları",
            "content": (
                "Teratomlar (Grekçe 'teras' yani canavar/hilkat garibesi kelimesinden türetilmiştir), her üç embriyonik "
                "germ yaprağına da (ektoderm, mezoderm ve endoderm) diferansiye olma potansiyeline sahip 'totipotent germ "
                "hücrelerinden' köken alan olağanüstü neoplazmlardır. En sık primer lokalizasyonları gonadlardır (over ve testis); "
                "ayrıca embriyolojik orta hat göç yolları boyunca mediastende, retroperitonda ve sakrokoksigeal bölgede de "
                "saptanabilirler. Bir teratom kitlesi kesildiğinde içinde saç telleri, yağ bezleri, dişler, kıkırdak, "
                "kemik, bronş epiteli, tiroid dokusu (struma ovarii) ve gastrointestinal mukoza gibi birbiriyle tamamen "
                "alakasız çok sayıda olgun veya immatür doku parçası hayret verici bir kaos içinde bir arada bulunur."
            ),
            "elements": [
                make_table(
                    "Teratom İçeriğinde Temsil Edilen Germ Yaprakları ve Dokular",
                    ["Germ Yaprağı", "Teratomda Görülen Tipik Dokular"],
                    [
                        {
                            "cells": ["Ektoderm", "Çok katlı yassı epitel, saç folikülleri, yağ bezleri, nöronal beyin dokusu"],
                            "hiddenIndex": 1,
                            "hint": "Deri ekleri ve sinir sistemi dokuları"
                        },
                        {
                            "cells": ["Mezoderm", "Kemik, kıkırdak, düz ve çizgili kas, yağ dokusu"],
                            "hiddenIndex": 1,
                            "hint": "Mezenkimal matriks ve lifli yapılar"
                        },
                        {
                            "cells": ["Endoderm", "Gastrointestinal epitel, bronşiyal solunum epiteli, tiroid glandı"],
                            "hiddenIndex": 1,
                            "hint": "İç organ örtü epitelleri"
                        }
                    ]
                ),
                make_cloze(
                    "Birden fazla embriyonik germ tabakasından dokular içeren ve totipotent hücrelerden doğan neoplazmlara teratom adı verilir.",
                    "teratom",
                    "Diş ve kıl içeren çok yapraklı tümör"
                )
            ]
        },
        # Slayt 45
        {
            "slideNumber": 45,
            "title": "Matür Kistik Teratom (Dermoid Kist) vs İmmatür Teratom",
            "content": (
                "Teratomlar histopatolojik diferansiyasyon derecelerine göre iki hayati gruba ayrılır: 'Matür' ve 'İmmatür' "
                "teratomlar. Kadınlarda overin en sık görülen germ hücreli tümörü olan 'matür kistik teratom' (dermoid kist), "
                "içerdiği tüm dokuların tamamen olgun (matür) erişkin diferansiyasyonu gösterdiği benign bir kistik kitledir. "
                "Kist açıldığında sarı renkli peynirimsi yağlı sebum sıvısı, saç yumakları ve 'Rokitansky nodülü' üzerinde "
                "dişler izlenir. Buna karşılık 'immatür teratom'da, embriyonik veya fetal dokuları taklit eden, özellikle "
                "immatür nöroepitelyal rozetler ve indiferansiye mezenkimal alanlar bulunur. İmmatür nöroepitelyum varlığı "
                "kitlenin doğrudan malign olduğunu gösterir ve derecesine göre sistemik kemoterapi gerektirir."
            ),
            "elements": [
                make_before_after(
                    "Over Teratomunun Biyolojik Ayrımı",
                    "Matür Teratom (Dermoid Kist - Benign)",
                    "İçerideki tüm dokular (kıl, yağ bezi, kıkırdak) erişkin olgunluğundadır; cerrahi kistektomi tam kür sağlar.",
                    "İmmatür Teratom (Malign Potansiyel)",
                    "Fetal immatür nöroektodermal tübüller ve rozetler içerir; çevre dokulara yayılır ve metastaz riski yüksektir.",
                    "Bir teratomda immatür nöroepitelyum saptanması malignite tanısının kesin anahtarıdır."
                ),
                make_micro_quiz(
                    "Bir over teratomunda kitlenin malign (immatür teratom) kabul edilmesini sağlayan en kritik histopatolojik bileşen hangisidir?",
                    [
                        {
                            "text": "İmmatür fetal nöroepitelyal doku ve nöroblastik rozetlerin varlığı",
                            "isCorrect": True,
                            "explanation": "Doğrudur; immatür nöroepitelyum miktarı teratomun malignite derecesini (grade) belirler."
                        },
                        {
                            "text": "Olgun saç teli ve kıl foliküllerinin bulunması",
                            "isCorrect": False,
                            "explanation": "Olgun saç teli benign matür teratomun (dermoid kist) klasik bulgusudur."
                        },
                        {
                            "text": "Kitlenin içinde kemik ve diş yapılarının saptanması",
                            "isCorrect": False,
                            "explanation": "Olgun diş ve kemik matür teratomlarda da çok sık görülür."
                        },
                        {
                            "text": "Kistin içinde sarı sebum sıvısının akması",
                            "isCorrect": False,
                            "explanation": "Sebum matür yağ bezlerinin doğal salgısıdır, malignite göstergesi değildir."
                        }
                    ],
                    "İmmatür nöroepitelyal doku teratomlarda malignitenin histolojik kanıtıdır."
                )
            ]
        },
        # Slayt 46
        {
            "slideNumber": 46,
            "title": "Hamartom: Organın Yerli Dokularının Düzensiz Karışımı",
            "content": (
                "Hamartom, bulunduğu organa normalde ait olan yerli olgun doku elemanlarının, anormal bir mimari organizasyon "
                "ve düzensiz bir yığın halinde lokalize kitle oluşturmasıdır. Tarihsel olarak gelişimsel bir doku malformasyonu "
                "olarak kabul edilmişken, günümüzde birçok hamartomda klonal somatik kromozomal translokasyonlar (örneğin "
                "akciğer hamartomlarında 6p21 veya 12q14 translokasyonları) saptanmış olup benign neoplazm kategorisinde "
                "değerlendirilmektedir. Hamartomdaki kilit kavram şudur: Dokular tamamen olgundur ve kesinlikle o organın "
                "kendi yapıtaşlarıdır; ancak mimari bir düzen, polarite ve fonksiyonel organizasyon tamamen kaybolmuştur."
            ),
            "elements": [
                make_cloze(
                    "Bulunduğu anatomik organa ait olgun dokuların mimari düzenden yoksun kaotik kitlesine hamartom adı verilir.",
                    "hamartom",
                    "Yerli dokunun düzensiz neoplastik kitlesi"
                ),
                make_active_recall(
                    "Hamartom ile normal doku arasındaki temel histopatolojik fark nedir?",
                    "Dokuların olgun olmasına rağmen organın normal mimari diziliminden tamamen yoksun düzensiz bir kitle yapmasıdır.",
                    "Hücresel yerleşim karmaşası"
                )
            ]
        },
        # Slayt 47
        {
            "slideNumber": 47,
            "title": "Prototip Hamartom: Akciğer Pulmoner Hamartomu",
            "content": (
                "Hamartomun insan vücudundaki en klasik ve en sık örneği 'akciğer kondroid hamartomu'dur. Akciğer grafisinde "
                "veya toraks tomografisinde periferik yerleşimli, düzgün sınırlı, yuvarlak, 2-4 cm çapında ve karakteristik "
                "olarak patlamış mısır (popcorn) tarzı kalsifikasyonlar içeren bir 'soliter pulmoner nodül' (para lezyonu) "
                "şeklinde tesadüfen saptanır. Mikroskop altında incelendiğinde; akciğer bronş duvarına normalde ait olan "
                "olgun hyalen kıkırdak adacıkları, aralara serpiştirilmiş olgun yağ dokusu, fibröz bağ dokusu ve bunların "
                "arasında sıkışmış silyalı solunum epiteli ile döşeli yarıklar bir arada görülür; malign potansiyeli yoktur."
            ),
            "elements": [
                make_before_after(
                    "Akciğer Hamartomu vs Akciğer Karsinomu Ayrımı",
                    "Pulmoner Hamartom (Benign)",
                    "Düzgün keskin sınırlı, patlamış mısır kalsifikasyonu, kıkırdak ve yağ içerir; biyolojik olarak zararsızdır.",
                    "Akciğer Karsinomu (Malign)",
                    "Spiküle çentikli sınırlar, çevre parankime infiltrasyon, nekroz, hızla büyüyen lenfovasküler invazyonlu kitle.",
                    "Toraks tomografisindeki yağ ve patlamış mısır kalsifikasyonu hamartom için patognomoniktir."
                ),
                make_active_recall(
                    "Akciğer hamartomlarının radyolojik görüntülemesinde saptanan klasik kalsifikasyon paterni neye benzetilir?",
                    "Patlamış mısır (popcorn) kalsifikasyonuna benzetilir.",
                    "Atıştırmalık taneleri andıran radyoopasite"
                )
            ]
        },
        # Slayt 48
        {
            "slideNumber": 48,
            "title": "Koristom: Heterotopik (Ektopik) Olgun Doku Adacığı",
            "content": (
                "Koristom (heterotopi veya ektopi), normalde o organda kesinlikle bulunmaması gereken olgun bir dokunun, "
                "tamamen yabancı farklı bir anatomik bölgede küçük adacıklar veya nodüller halinde bulunmasıdır. Koristom "
                "gerçek bir neoplazm değil, embriyolojik organogenez sırasındaki göç kusurlarından kaynaklanan konjenital "
                "bir doku anomalisidir. En klasik ve en sık koristom örneği, mide submukozasında veya Meckel divertikülü "
                "duvarında saptanan 'ektopik pankreas' dokusu adacıklarıdır. Benzer şekilde overde adrenal korteks kalıntıları "
                "veya dilde tiroid dokusu (lingual tiroid) koristomun diğer iyi bilinen klinik örnekleridir."
            ),
            "elements": [
                make_table(
                    "Hamartom ve Koristom Arasındaki Temel Ayırıcı Tanı",
                    ["Kriter", "Hamartom", "Koristom (Heterotopi)"],
                    [
                        {
                            "cells": ["Doku Niteliği", "Organın kendi yerli dokuları", "O organda normalde bulunmayan yabancı ektopik doku"],
                            "hiddenIndex": 1,
                            "hint": "İlgili parankimin öz elemanları"
                        },
                        {
                            "cells": ["Klasik Klinik Örnek", "Akciğerde kıkırdak ve yağ kitlesi (Kondroid hamartom)", "Mide veya Meckel divertikülü duvarında pankreas adacığı"],
                            "hiddenIndex": 1,
                            "hint": "Gastrointestinal ektopik doku örneği"
                        },
                        {
                            "cells": ["Neoplazi Niteliği", "Genellikle benign klonal neoplazm", "Embriyolojik gelişimsel ektopi (gerçek neoplazm değil)"],
                            "hiddenIndex": 2,
                            "hint": "Fetal dönem hücresel göç sapması"
                        }
                    ]
                ),
                make_cloze(
                    "Mide submukozasında veya Meckel divertikülünde saptanan ektopik pankreas dokusu adacığı koristom için prototip örnektir.",
                    "koristom",
                    "Heterotopik olgun doku terimi"
                )
            ]
        },
        # Slayt 49 [CHECKPOINT 5]
        {
            "slideNumber": 49,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Karma Tümörler, Teratom, Hamartom ve Koristom",
            "content": (
                "Bu bölümde özel neoplastik ve gelişimsel lezyonların ayrımını ve morfolojisini inceledik. "
                "Karma (mikst) tümörler, tek bir monoklonal öncül hücreden köken alıp birden fazla hücre hattına diverjan farklılaşma gösterir; prototipi parotis pleomorfik adenomudur (epitel + kıkırdak). "
                "Teratomlar totipotent germ hücrelerinden doğar ve her üç germ yaprağına (ektoderm, mezoderm, endoderm) ait dokuları barındırır. "
                "Overin matür teratomu (dermoid kist) tamamen iyi huyludur; ancak immatür nöroepitelyum içermesi durumunda malign immatür teratom adını alır. "
                "Hamartom, organın kendi yerli dokularının mimari düzenden yoksun kitleleşmesidir; akciğer kondroid hamartomu (patlamış mısır kalsifikasyonu) klasiktir. "
                "Koristom ise tamamen yabancı bir organda olgun doku adacığının bulunmasıdır (midede ektopik pankreas)."
            ),
            "flashcards": [
                {
                    "id": "k1-28-cp05-fc01",
                    "front": "Tek bir monoklonal kökenden doğup tükürük bezinde hem epitel hem kıkırdak diferansiyasyonu sergileyen benign mikst tümör nedir?",
                    "back": "Pleomorfik adenomdur.",
                    "hint": "Parotisin en yaygın karma uru"
                },
                {
                    "id": "k1-28-cp05-fc02",
                    "front": "Overde saptanan bir teratomun iyi huylu dermoid kistten çıkıp malign kabul edilmesini sağlayan embriyonik doku tipi nedir?",
                    "back": "İmmatür nöroepitelyal dokudur.",
                    "hint": "Fetal primitif medüller tübül ve rozet yapıları"
                },
                {
                    "id": "k1-28-cp05-fc03",
                    "front": "Mide duvarında veya Meckel divertikülünde rastlanan normal pankreas adacıkları gibi ektopik doku lezyonuna ne ad verilir?",
                    "back": "Koristom adı verilir.",
                    "hint": "Heterotopik anatomik gelişim anomalisi"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 5 Özet Tablosu: Özel Kitlelerin Ayırıcı Özellikleri",
                    ["Terim", "Klonalite / Doğası", "Hücresel İçerik"],
                    [
                        {
                            "cells": ["Teratom", "Totipotent germ hücresi", "Ektoderm, mezoderm ve endoderm türevleri"],
                            "hiddenIndex": 0,
                            "hint": "Çoklu germ yaprağı uru"
                        },
                        {
                            "cells": ["Hamartom", "Organın kendi yerli hücresi", "Kaotik dizilimli yerli olgun dokular"],
                            "hiddenIndex": 0,
                            "hint": "Organın kaotik kendi dokusu"
                        }
                    ]
                )
            ]
        },
        # Slayt 50
        {
            "slideNumber": 50,
            "title": "Klinik Karar: Over Teratomunda Patolojik Örnekleme",
            "content": (
                "22 yaşında kadın hastada sol overde 10 cm'lik kistik kitle eksize ediliyor. Makroskobide kist lümeninde saç "
                "yumakları, sarı sebum sıvısı ve bir adet diş izleniyor. Patolog bu kitleyi incelerken yalnızca makroskobik "
                "olarak iyi huylu dermoid kist demekle yetinmemelidir. Malignite potansiyeli taşıyan 'immatür teratom' tanısını "
                "atlamamak için kist duvarından, özellikle solid ve yumuşak alanlardan kitlenin her 1 cm çapı için en az "
                "bir kaset (10 blok) mikroskobik örnekleme yapılmalıdır. Eğer mikroskopta immatür nöroepitelyal tübüller "
                "saptanırsa tümörün derecesi (Grade 1-3) belirlenmeli ve jinekolojik onkoloğa kemoterapi için bilgi verilmelidir."
            ),
            "elements": [
                make_branching_logic(
                    "24 yaşında kadından çıkarılan over kistinde makroskopik saç ve yağ görülmesine rağmen, mikroskobik incelemede geniş alanlarda hiperkromatik nükleuslu immatür nöroektodermal rozetler saptanıyor.",
                    "Bu patolojik bulgu karşısında tümörün tanısı ve klinik yaklaşımı ne olmalıdır?",
                    [
                        {
                            "text": "Tümör malign potansiyelli 'İmmatür Teratom' olarak rapor edilmeli, immatür doku alanlarına göre evrelenip adjuvan kemoterapi planlanmalıdır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; immatür nöroepitelyum varlığı teratomu benign dermoid kistten çıkarıp malign immatür teratom yapar."
                        },
                        {
                            "text": "İçinde saç olduğu için kesinlikle benign kabul edilmeli ve hasta takipten çıkarılmalıdır.",
                            "isCorrect": False,
                            "explanation": "İmmatür nöroepitelyum varlığı malignite kanıtıdır, takipten çıkarılamaz."
                        },
                        {
                            "text": "Hastaya tüberküloz tedavisi başlanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Nöroepitelyal rozetler tüberküloz granülomu değildir."
                        }
                    ]
                )
            ]
        }
    ]
