# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi
Bölüm 8: Metastaz Mekanizmaları ve Organ Tropizmi (Slayt 71 - 80)
Checkpoint: Slayt 79
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_8_slides():
    return [
        # Slayt 71
        {
            "slideNumber": 71,
            "title": "Metastaz: Malignitenin Kesin Belirteci ve Mortalite Nedeni",
            "content": (
                "Metastaz, primer tümör odağı ile hiçbir fiziksel ve anatomik devamlılığı bulunmayan uzak doku veya organlarda "
                "sekonder neoplastik implantların (tümör kolonilerinin) kurulmasıdır. Patoloji biliminde metastaz, bir neoplazmın "
                "'tartışmasız olarak malign' olduğunu kanıtlayan tek ve en kesin ölçüttür; hiçbir benign tümör asla metastaz "
                "yapamaz. Kanser hastalarında görülen ölümlerin %90'ından fazlası primer kitleden değil, hayati organlara "
                "(beyin, karaciğer, akciğer, kemik iliği) yayılan metastazların organ yetmezliği yaratmasından kaynaklanır. "
                "İstisnai olarak deri bazal hücreli karsinomu ve beyin primer gliomları son derece lokal invaziv olmalarına "
                "rağmen uzak metastaz neredeyse hiç yapmazlar."
            ),
            "elements": [
                make_cloze(
                    "Primer tümör ile fiziksel devamlılığı olmayan uzak dokularda sekonder tümör kolonileri kurulmasına metastaz denir.",
                    "metastaz",
                    "Uzak organa yayılım süreci"
                ),
                make_active_recall(
                    "Lokal olarak son derece agresif ve kemirici büyümesine rağmen uzak metastaz yeteneği neredeyse sıfır olan deri kanseri nedir?",
                    "Bazal hücreli karsinomdur (BCC).",
                    "Metastaz yapmayan yaygın deri kanseri"
                )
            ]
        },
        # Slayt 72
        {
            "slideNumber": 72,
            "title": "Metastatik Kaskad: İntravazasyon, Dolaşım ve Kolonizasyon",
            "content": (
                "Metastaz son derece verimsiz, zorlu ve çok basamaklı bir biyolojik serüvendir (metastatik kaskad). Milyonlarca "
                "kanser hücresi primer kitleden dökülür; ancak bunların yalnızca %0.01'inden azı uzak organda başarılı bir "
                "metastaz odağı kurabilir. Kaskad şu basamaklardan oluşur: Ekstraselüler matriksi aşarak kapiller veya "
                "lenfatik damar lümenine girmek ('intravazasyon'), dolaşımda kan akımının hidrodinamik kesme kuvvetlerine "
                "ve immün gözetim hücrelerine (özellikle Natural Killer hücrelerine) karşı trombositlerle birleşerek 'tümör-trombosit "
                "embolisi' oluşturup hayatta kalmak, hedef organ kapiller endoteline yapışıp damar dışına çıkmak ('ekstravazasyon') "
                "ve yabancı mikroçevrede mikrometastazdan makrometastaza büyüyerek 'kolonize olmak'."
            ),
            "elements": [
                make_causal_chain(
                    "Metastatik Kaskadın Biyolojik Basamakları",
                    [
                        "1. İntravazasyon: Tümör hücresinin bazal membranı eriterek damar lümenine sızması",
                        "2. Dolaşımda Sağkalım: Hücrenin trombositlerle zırhlanarak NK hücrelerinden ve mekanik stresten kaçması",
                        "3. Endotelyal Tutunma: Hedef organ kapiller yatağında selektin ve integrinlerle lümene yapışma",
                        "4. Ekstravazasyon: Endotel aralıklarını aralayarak damardan hedef organ parankimine sızma",
                        "5. Kolonizasyon: Yabancı stromal ortamda anjiyogenezi tetikleyerek sekonder tümör kolonisi kurma"
                    ]
                ),
                make_cloze(
                    "Kanser hücrelerinin damar lümenine sızarak dolaşıma katılması sürecine intravazasyon adı verilir.",
                    "intravazasyon",
                    "Damar içine giriş evresi"
                )
            ]
        },
        # Slayt 73
        {
            "slideNumber": 73,
            "title": "Vücut Boşluklarına Tohumlanma: Transsölomik Yayılım",
            "content": (
                "Vücut boşluklarına tohumlanma (transsölomik yayılım), neoplazmın doğal bir seröz boşluğa (periton, plevra, "
                "perikard veya subaraknoid boşluk) penetre olmasıyla başlar. Kanser hücreleri seröz zarı deldikten sonra "
                "sıvı akımıyla serbestçe yüzerek boşluğun her yerine ekilir. En klasik örneği 'over karsinomu'dur; over kanseri "
                "hücreleri periton boşluğuna dökülerek tüm omentum, bağırsak serozası ve periton yüzeylerine milyarlarca küçük "
                "nodül halinde ekilir ve masif kanserli asit ile 'peritoneal karsinomatozis' oluşturur. Benzer şekilde beyin "
                "tümörleri (medulloblastom ve ependimom) beyin omurilik sıvısına (BOS) dökülerek omurilik boyunca tohumlanır."
            ),
            "elements": [
                make_before_after(
                    "Lokal Kitle vs Transsölomik Tohumlanma",
                    "Primer Over Karsinomu",
                    "Kitle pelviste over lojundadır, henüz seröz kapsülü delmemiştir; cerrahi çıkarım mümkündür.",
                    "Peritoneal Tohumlanma (Karsinomatozis)",
                    "Peritona açılan hücreler tüm karın içi organ zarlarına sıvanır, masif hemorajik asit ve omental kek oluşturur.",
                    "Over kanserinde tanı anında hastaların çoğunda transsölomik yayılım mevcuttur."
                ),
                make_active_recall(
                    "Over karsinomunun periton boşluğuna dökülerek tüm karın içi organ zarlarını neoplastik nodüllerle kaplamasına ne ad verilir?",
                    "Peritoneal karsinomatozis (transsölomik tohumlanma) adı verilir.",
                    "Karın zarına yaygın ekilme"
                )
            ]
        },
        # Slayt 74
        {
            "slideNumber": 74,
            "title": "Lenfatik Yayılım: Karsinomların Karakteristik Rotası",
            "content": (
                "Lenfatik damarlar boyunca yayılım, 'karsinomların' (epitelyal kanserlerin) en karakteristik ve en yaygın "
                "ilk metastaz yoludur. Lenfatik kılcallar ince duvarlıdır, bazal membranları kesintilidir ve kapakçıkları "
                "arasındaki aralıklar hücre geçişine çok uygundur. Tümör hücreleri doğal lenfatik drenaj yollarını takip "
                "ederek ilk olarak 'bölgesel lenf düğümlerine' (regional lymph nodes) ulaşırlar. Örneğin akciğer bronş karsinomu "
                "önce trakeobronşiyal ve hiler lenf düğümlerine; memenin üst dış kadran karsinomu ise primer olarak 'aksiller "
                "lenf düğümlerine' yayılır. Lenf düğümünde sinüsleri dolduran tümör hücreleri zamanla tüm düğümü tahrip ederek "
                "birbirine yapışık sert 'konglome' lenf nodu paketleri meydana getirir."
            ),
            "elements": [
                make_table(
                    "Tümörlerin Tipik İlk Bölgesel Lenfatik Drenaj İstasyonları",
                    ["Primer Tümör Odağı", "İlk Bölgesel Lenfatik İstasyon", "İkincil Lenfatik Durak"],
                    [
                        {
                            "cells": ["Meme Üst Dış Kadran Karsinomu", "Aksiller Lenf Düğümleri", "Supraklaviküler düğümler"],
                            "hiddenIndex": 1,
                            "hint": "Koltuk altı ganglion istasyonu"
                        },
                        {
                            "cells": ["Akciğer Bronş Karsinomu", "Hiler ve Trakeobronşiyal Düğümler", "Mediastinal lenf nodları"],
                            "hiddenIndex": 1,
                            "hint": "Akciğer kökü lenf bezleri"
                        },
                        {
                            "cells": ["Testis Tümörleri (Seminom vb.)", "Paraaortik Retroperitoneal Düğümler", "Mediastinal düğümler"],
                            "hiddenIndex": 1,
                            "hint": "Aort çevresi lenfatik zincir"
                        }
                    ]
                ),
                make_cloze(
                    "Epitelyal malignite olan karsinomların metastaz yaparken ilk tercih ettiği karakteristik yol lenfatik yayılım yoludur.",
                    "lenfatik yayılım",
                    "Lenf damarları aracılı metastaz"
                )
            ]
        },
        # Slayt 75
        {
            "slideNumber": 75,
            "title": "Sentinel (Bekçi) Lenf Düğümü Biyopsisi",
            "content": (
                "Sentinel lenf düğümü (bekçi lenf nodu), bir primer tümör odağından lenfatik drenaj sıvısını doğrudan "
                "alan 'ilk lenf düğümüdür'. Modern onkolojide (özellikle meme kanseri ve melanomda), tüm koltuk altı lenf "
                "düğümlerini körlemesine çıkarıp kolda ömür boyu lenfödem yaratmak yerine sentinel lenf nodu biyopsisi (SLNB) "
                "uygulanır. Tümör çevresine mavi boya (izosulfan mavisi) veya teknesyum-99 radyoaktif kolloid enjekte edilir. "
                "Gama probuyla ilk tutulan 'bekçi' lenf düğümü bulunup çıkarılır ve ameliyat sırasında 'frozen section' ile "
                "incelenir. Eğer sentinel düğüm tümörsüz (negatif) ise, arkasındaki lenf düğümleri %98-99 oranında temiz "
                "demektir ve aksiller diseksiyona gerek kalmaz; metastaz varsa aksiller temizlik yapılır."
            ),
            "elements": [
                make_before_after(
                    "Rutin Aksiller Diseksiyon vs Sentinel Lenf Nodu Biyopsisi",
                    "Geleneksel Tam Aksiller Diseksiyon",
                    "Tüm koltuk altı lenf nodları (I, II, III. seviye) kesilir; kolda ağır lenfödem, ağrı ve hareket kısıtlılığı gelişir.",
                    "Sentinel Lenf Nodu Biyopsisi (SLNB)",
                    "Yalnızca maviye boyanan ilk düğüm çıkarılır; negatifse lenf zinciri korunur, kolda lenfödem riski sıfırlanır.",
                    "SLNB modern cerrahi onkolojide gereksiz morbiditeyi önleyen en devrimsel yöntemdir."
                ),
                make_active_recall(
                    "Primer tümörden lenfatik akımı ilk karşılayan ve biyopsisi temiz çıktığında aksillanın korunmasını sağlayan düğüme ne ad verilir?",
                    "Sentinel (bekçi) lenf düğümü adı verilir.",
                    "İlk lenfatik durak bezi"
                )
            ]
        },
        # Slayt 76
        {
            "slideNumber": 76,
            "title": "Hematojen Yayılım: Sarkomların Tercih Ettiği Yol",
            "content": (
                "Hematojen yayılım (kan yoluyla yayılma), kural olarak 'sarkomların' (mezenkimal malignitelerin) primer "
                "metastaz yoludur; ancak karsinomlar da ileri evrelerde hematojen yola geçerler. Dolaşıma giren tümör hücreleri "
                "kalın ve elastik duvarlı arterleri kolay kolay delemeyip, ince duvarlı venöz kapillerleri ve postkapiller "
                "venülleri tercih ederler. Kan dolaşımına katılan hücreler venöz kan akımını takip eder. Renal hücreli karsinom "
                "(RCC) ve hepatoselüler karsinom (HCC) gibi bazı vasküler tümörler, doğrudan büyük ven lümenlerine (renal ven ve "
                "vena kava inferior) parmaksı tümör trombüsleri uzatarak sağ atriyuma kadar ilerleyebilir."
            ),
            "elements": [
                make_micro_quiz(
                    "Mezenkimal kaynaklı maligniteler olan sarkomların metastaz yaparken ilk ve karakteristik olarak kullandığı yol hangisidir?",
                    [
                        {
                            "text": "Hematojen yayılım yolu (özellikle ince duvarlı venler)",
                            "isCorrect": True,
                            "explanation": "Doğrudur; sarkomlar tipik olarak venöz kan yoluyla ilk olarak akciğere metastaz yaparlar."
                        },
                        {
                            "text": "Yalnızca gözyaşı kanalları yoluyla yayılım",
                            "isCorrect": False,
                            "explanation": "Gözyaşı kanalları metastaz yolu değildir."
                        },
                        {
                            "text": "Beyin omurilik sıvısı (BOS) yolu",
                            "isCorrect": False,
                            "explanation": "BOS yolu SSS tümörlerine özgüdür, periferik sarkomlar için geçerli değildir."
                        },
                        {
                            "text": "Sinir liflerinin içine girerek geri geri tırmanma",
                            "isCorrect": False,
                            "explanation": "Perinöral invazyon lokal bir yayılımdır, sistemik sarkom yolu değildir."
                        }
                    ],
                    "Sarkomlar kural olarak hematojen yolla yayılırlar."
                ),
                make_cloze(
                    "Böbreğin renal hücreli karsinomu doğrudan renal ven ve vena kava inferior lümenine tümör trombüsü uzatabilen klasik bir örnektir.",
                    "vena kava inferior",
                    "Gövdenin ana toplayıcı venası"
                )
            ]
        },
        # Slayt 77
        {
            "slideNumber": 77,
            "title": "Vasküler Drenaj Paternleri: Karaciğer ve Akciğer",
            "content": (
                "Hematojen metastazların yerleştiği hedef organlar, büyük ölçüde primer tümörün boşaldığı venöz vasküler "
                "drenaj haritası ile belirlenir. Gastrointestinal sistem organlarının (mide, kolon, rektum, pankreas) venöz "
                "drenajı portal ven aracılığıyla karaciğere akar; bu nedenle tüm gastrointestinal karsinomların hematojen "
                "metastaz için karşılaştığı ilk kapiller filtre 'karaciğer'dir. Karaciğer dışındaki tüm organların (böbrek, "
                "kemikler, tiroid, meme, ekstremite sarkomları) venöz kanı ise vena kava sistemine dökülerek ilk olarak "
                "'akciğer kapiller yatağına' ulaşır. Dolayısıyla akciğer ve karaciğer, vücutta hematojen metastazların "
                "en sık görüldüğü iki dev filtre organdır."
            ),
            "elements": [
                make_table(
                    "Venöz Drenaj Haritası ve İlk Hematojen Filtre Organları",
                    ["Primer Organ Grubu", "Venöz Drenaj Yolu", "İlk Karşılaşılan Metastatik Filtre Organ"],
                    [
                        {
                            "cells": ["Gastrointestinal Sistem (Kolon, Mide)", "Portal Ven Sistemi", "Karaciğer parankimi"],
                            "hiddenIndex": 2,
                            "hint": "Portal drenaj hedefi"
                        },
                        {
                            "cells": ["Sistemik Organlar (Böbrek, Kemik, Kas)", "Vena Kava İnferior / Superior", "Akciğer kapiller yatağı"],
                            "hiddenIndex": 2,
                            "hint": "Kaval drenaj hedefi"
                        },
                        {
                            "cells": ["Batson Paravertebral Venöz Pleksus", "Valfsiz vertebral venler", "Omurga vertebra kemikleri (Prostat kanseri)"],
                            "hiddenIndex": 2,
                            "hint": "Kemiğe valfsiz venöz yayılım"
                        }
                    ]
                ),
                make_active_recall(
                    "Gastrointestinal sistem karsinomlarının hematojen yolla en sık ilk metastaz yaptıkları organ neresidir?",
                    "Karaciğerdir (portal venöz dolaşım nedeniyle).",
                    "Mezenterik akımın ulaştığı primer organ"
                )
            ]
        },
        # Slayt 78
        {
            "slideNumber": 78,
            "title": "Organ Tropizmi ve 'Seed and Soil' (Tohum ve Toprak) Hipotezi",
            "content": (
                "Metastaz yalnızca kan akımının mekanik rotasıyla açıklanamaz; belirli tümör tiplerinin belirli organlara "
                "özgül bir çekim göstermesi olgusuna 'organ tropizmi' denir. Stephen Paget 1889'da bunu 'Tohum ve Toprak' "
                "(Seed and Soil) hipotezi ile açıklamıştır: Tümör hücresi bir 'tohum', metastaz yapılacak organ mikroçevresi "
                "ise 'toprak'tır; tohum ancak biyokimyasal olarak uygun olan toprakta yeşerebilir. Örneğin 'prostat karsinomu' "
                "kemik iliği stromasındaki büyüme faktörleri nedeniyle tercihen osteoblastik 'kemik metastazı' yapar. "
                "'Bronkojenik akciğer karsinomu' ise beyin ve adrenal bezlere tropizm gösterir. Buna karşılık iskelet kası "
                "ve dalak, son derece zengin kanlanmalarına rağmen metastazların neredeyse hiç yerleşmediği düşmanca topraklardır."
            ),
            "elements": [
                make_table(
                    "Kanser Tipleri ve Karakteristik Organ Tropizmi Eşleşmesi",
                    ["Primer Kanser", "Karakteristik Tercihli Metastaz Yeri", "Mekanizma / Uygun Toprak"],
                    [
                        {
                            "cells": ["Prostat Karsinomu", "Kemik (Özellikle vertebra, osteoblastik)", "Kemik iliği endotel adezyon molekülleri"],
                            "hiddenIndex": 1,
                            "hint": "Sklerotik iskelet lezyonu alanı"
                        },
                        {
                            "cells": ["Bronkojenik Akciğer Karsinomu", "Adrenal Bez ve Beyin", "Spesifik kemokin reseptör uyumu (CXCR4)"],
                            "hiddenIndex": 1,
                            "hint": "Sürrenal ve santral sinir sistemi"
                        },
                        {
                            "cells": ["Üveal Melanom", "Karaciğer", "Karaciğer sinusoidal IGF-1 tutunması"],
                            "hiddenIndex": 1,
                            "hint": "Göz tümörünün hedef organı"
                        }
                    ]
                ),
                make_cloze(
                    "Prostat kanserinin venöz akım dışındaki biyokimyasal affinite ile en sık metastaz yaptığı hedef doku kemik dokusudur.",
                    "kemik",
                    "Osteoblastik metastaz odağı"
                )
            ]
        },
        # Slayt 79 [CHECKPOINT 8]
        {
            "slideNumber": 79,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Metastaz Mekanizmaları ve Yolları",
            "content": (
                "Bu bölümde metastazın biyolojik doğasını, yayılım yollarını ve organ tropizmini özetledik. "
                "Metastaz, primer tümörle devamlılığı olmayan uzak kolonilerdir ve malignitenin kesin kanıtıdır. "
                "Metastatik kaskad: İntravazasyon, trombositlerle zırhlanarak dolaşımda sağkalım, ekstravazasyon ve kolonizasyondur. "
                "Üç ana metastaz yolu vardır: Transsölomik tohumlanma (over kanseri → periton karsinomatozisi), lenfatik yayılım (karsinomlar) ve hematojen yayılım (sarkomlar). "
                "Sentinel lenf nodu biyopsisi, ilk drenaj düğümünü bularak gereksiz aksiller diseksiyonu ve lenfödemi önler. "
                "Portal drenaj karaciğere, sistemik kaval drenaj akciğere ilk metastaz filtresi oluşturur. "
                "Paget'nin Seed and Soil hipotezine göre prostat kemiğe, akciğer kanseri adrenal ve beyine tropizm gösterirken; iskelet kası son derece nadir metastaz bölgesidir."
            ),
            "flashcards": [
                {
                    "id": "k1-28-cp08-fc01",
                    "front": "Epitelyal malignite olan karsinomların metastaz yaparken ilk ve karakteristik olarak kullandığı yayılım yolu nedir?",
                    "back": "Lenfatik damar yoludur.",
                    "hint": "Bölgesel düğümlere giden sıvı kanalları"
                },
                {
                    "id": "k1-28-cp08-fc02",
                    "front": "Prostat adenokarsinomunun metastaz yapmak için en yüksek biyokimyasal tropizm gösterdiği hedef organ neresidir?",
                    "back": "Kemik dokusudur.",
                    "hint": "Osteoblastik lezyonların oluştuğu iskelet sistemi"
                },
                {
                    "id": "k1-28-cp08-fc03",
                    "front": "Primer tümör yatağından lenfatik drenajı doğrudan ilk karşılayan lenf bezine ne ad verilir?",
                    "back": "Sentinel lenf düğümü adı verilir.",
                    "hint": "İlk durak bekçi istasyonu"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 8 Özet Tablosu: Metastaz Yolları ve Hedef Dokular",
                    ["Metastaz Yolu", "Tipik Tümör Grubu", "Klasik Hedef Bölge"],
                    [
                        {
                            "cells": ["Transsölomik Tohumlanma", "Over karsinomu", "Periton boşluğu (Karsinomatozis)"],
                            "hiddenIndex": 0,
                            "hint": "Seröz boşluğa ekilme"
                        },
                        {
                            "cells": ["Lenfatik Drenaj", "Karsinomlar", "Bölgesel sentinel ve derin lenf nodları"],
                            "hiddenIndex": 0,
                            "hint": "Epitel kanserlerinin ilk yolu"
                        },
                        {
                            "cells": ["Hematojen (Portal)", "Kolon karsinomu", "Karaciğer parankimi"],
                            "hiddenIndex": 2,
                            "hint": "GİS venöz drenaj hedefi"
                        }
                    ]
                )
            ]
        },
        # Slayt 80
        {
            "slideNumber": 80,
            "title": "Klinik Karar: Meme Kanserinde Sentinel Lenf Nodu Biyopsisi",
            "content": (
                "50 yaşında kadın hastada sol meme üst dış kadranda 1.8 cm çapında invaziv duktal karsinom saptanıyor; "
                "koltuk altında palpabl veya radyolojik şüpheli lenf nodu bulunmuyor (klinik N0). Cerrah lumpektomiye ek olarak "
                "sentinel lenf nodu biyopsisi (SLNB) uyguluyor; peritümöral radyoaktif madde ve mavi boya verildikten sonra "
                "yakalanan 2 adet sentinel lenf nodu frozen section'a gönderiliyor. Patolog frozen incelemesinde her iki "
                "düğümün de tamamen reaktif olduğunu ve tümör metastazı içermediğini bildiriyor. Cerrah tam aksiller diseksiyon "
                "yapmaktan kaçınarak ameliyatı sonlandırıyor; böylece hastanın kolu ömür boyu lenfödem sakatlığından korunmuş oluyor."
            ),
            "elements": [
                make_branching_logic(
                    "Meme karsinomu cerrahisinde çıkarılan 2 adet sentinel lenf düğümünün ameliyat içi dondurma (frozen) kesitlerinde metastaz saptanmıyor (negatif sentinel lenf nodu).",
                    "Bu patolojik sonuç karşısında cerrahi ekibin aksillaya yönelik en doğru klinik kararı ne olmalıdır?",
                    [
                        {
                            "text": "Sentinel lenf nodu negatif olduğunda aksillanın geri kalanı temiz kabul edilir; tam aksiller diseksiyon yapılmamalı, ameliyat sonlandırılmalıdır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; SLNB negatifliği aksiller diseksiyonu gereksiz kılar ve lenfödemi önler."
                        },
                        {
                            "text": "Negatif olsa dahi ne olur ne olmaz diye tüm aksiller lenf düğümleri radikal olarak çıkarılmalıdır.",
                            "isCorrect": False,
                            "explanation": "Bu yaklaşım terk edilmiştir; hastada kalıcı lenfödem sakatlığı yaratır."
                        },
                        {
                            "text": "Hastanın kolu omuzdan ampute edilmelidir.",
                            "isCorrect": False,
                            "explanation": "Meme kanseri cerrahisinde kol amputasyonu kesinlikle söz konusu değildir."
                        }
                    ]
                )
            ]
        }
    ]
