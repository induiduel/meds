# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 28: Tümör Biyolojisi ve Terminolojisi
Bölüm 6: Diferansiyasyon, Anaplazi ve Hücresel Kriterler (Slayt 51 - 60)
Checkpoint: Slayt 59
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_6_slides():
    return [
        # Slayt 51
        {
            "slideNumber": 51,
            "title": "Diferansiyasyon Kavramı ve Fonksiyonel Kapasite",
            "content": (
                "Diferansiyasyon, neoplastik parankim hücrelerinin köken aldıkları normal hücrelere hem yapısal mimari "
                "hem de biyokimyasal ve fonksiyonel açıdan ne derecede benzediğini tanımlar. Benign tümörler kural olarak "
                "iyi diferansiyedir; örneğin bir tiroid adenomu tiroid folikülleri yapar ve kolloid depolar. Malign tümörler "
                "ise köken dokuya çok benzeyen 'iyi diferansiye' formlardan, orta ve az diferansiye formlara, oradan da "
                "orijinal dokuya hiçbir benzerliği kalmamış olan 'anaplastik' (undiferansiye) kitlelere kadar geniş bir "
                "spektrum sergiler. Diferansiyasyon azaldıkça hücreler normal fizyolojik yeteneklerini terk ederek yalnızca "
                "hızlı kontrolsüz bölünmeye odaklanırlar."
            ),
            "elements": [
                make_cloze(
                    "Tümör hücrelerinin köken aldıkları normal parankim hücrelerine yapısal ve fonksiyonel benzerlik derecesine diferansiyasyon denir.",
                    "diferansiyasyon",
                    "Farklılaşma ve olgunluk düzeyi"
                ),
                make_active_recall(
                    "İyi diferansiye bir skuamöz hücreli karsinom ile anaplastik bir karsinom arasındaki temel fonksiyonel fark nedir?",
                    "İyi diferansiye olanın keratin üretmeye devam etmesi, anaplastik olanın ise tüm özgül fonksiyonlarını tamamen kaybetmesidir.",
                    "Karakteristik uzmanlaşmış hücresel görev"
                )
            ]
        },
        # Slayt 52
        {
            "slideNumber": 52,
            "title": "Anaplazi: Malignitenin Güvenilir Histopatolojik Belirteci",
            "content": (
                "Anaplazi, kelime anlamı olarak 'geriye doğru biçimlenme' (diferansiyasyon kaybı) demektir ve mikroskop "
                "altında bir kitlenin tartışmasız olarak 'malign' olduğunu gösteren en güvenilir hücresel belirteçtir. "
                "Anaplastik bir tümör incelendiğinde, hücrelerin hangi dokudan (epitel mi, mezenkim mi, lenfoid mi) köken "
                "aldığını standart ışık mikroskopisi ile anlamak imkansızdır. Bu hücreler ilkel, kök hücre benzeri kaotik "
                "bir morfolojiye bürünürler. Anaplazinin varlığı daima agresif lokal invazyon, vasküler kanallara erken sızma "
                "ve yüksek oranda ölümcül uzak metastaz potansiyeli ile doğrudan birliktelik gösterir."
            ),
            "elements": [
                make_before_after(
                    "Diferansiye Karsinom vs Anaplastik Karsinom",
                    "İyi Diferansiye Karsinom",
                    "Bezler ve lümenler seçilebilir, hücreler düzenli sıralanmıştır, immünohistokimya olmadan da köken doku anlaşılır.",
                    "Anaplastik Karsinom",
                    "Tamamen sheets (tabakalar) halinde yığılmış kaotik hücreler, köken doku belirsizdir, tanıda pansitokeratin veya vimentin şarttır.",
                    "Anaplazi malignitenin patolojik kesinlik mührüdür."
                ),
                make_micro_quiz(
                    "Mikroskobik incelemede tümör hücrelerinin tüm diferansiyasyonunu kaybettiği ve ilkel hale geldiği duruma ne ad verilir?",
                    [
                        {
                            "text": "Anaplazi",
                            "isCorrect": True,
                            "explanation": "Doğrudur; anaplazi diferansiyasyonun tamamen kaybolmasıdır ve malignitenin belirtecidir."
                        },
                        {
                            "text": "Hiperplazi",
                            "isCorrect": False,
                            "explanation": "Hiperplazi hücre sayısının kontrollü artışıdır, diferansiyasyon kaybı değildir."
                        },
                        {
                            "text": "Metaplazi",
                            "isCorrect": False,
                            "explanation": "Metaplazi bir olgun hücre tipinin başka bir olgun hücre tipine dönüşmesidir."
                        },
                        {
                            "text": "Atrofi",
                            "isCorrect": False,
                            "explanation": "Atrofi hücre boyut ve sayısının küçülmesidir."
                        }
                    ],
                    "Anaplazi diferansiyasyon kaybını simgeler."
                )
            ]
        },
        # Slayt 53
        {
            "slideNumber": 53,
            "title": "Hücresel ve Nükleer Pleomorfizm",
            "content": (
                "Anaplazinin en çarpıcı morfolojik bulgularından biri 'pleomorfizm'dir (şekil ve boyut çeşitliliği). "
                "Normal bir dokuda tüm hücreler ve çekirdekleri standart bir geometriye ve homojen bir boyuta sahiptir. "
                "Anaplastik malign bir tümörde ise aynı mikroskop sahasında yan yana duran iki hücre arasında devasa farklar "
                "görülür: Bir yanda normal lenfosit boyutundan küçük büzüşmüş hücreler yer alırken, hemen yanında normal "
                "hücreden 5-10 kat daha büyük dev hücreler bulunur. Çekirdekler yuvarlak, oval, çentikli, lobüllü veya "
                "tamamen biçimsiz geometriler sergiler. Nükleer membranlar düzgün sınırını kaybederek girintili çıkıntılı bir hal alır."
            ),
            "elements": [
                make_cloze(
                    "Malign tümör hücrelerinin ve çekirdeklerinin boyut ve biçim açısından aşırı değişkenlik göstermesine pleomorfizm adı verilir.",
                    "pleomorfizm",
                    "Hücresel şekil ve büyüklük çeşitliliği"
                ),
                make_active_recall(
                    "Aynı doku kesitinde tümör hücre çekirdeklerinin birbirine hiç benzememesi ve şekil karmaşası göstermesi hangi patolojik terimle ifade edilir?",
                    "Nükleer pleomorfizm terimiyle ifade edilir.",
                    "Çekirdek şekil ve boyut anomalisi"
                )
            ]
        },
        # Slayt 54
        {
            "slideNumber": 54,
            "title": "Nükleer Atipi: Hiperkromazi ve N/S Oranı (1:1)",
            "content": (
                "Kanser hücrelerinin çekirdekleri, kontrolsüz genom duplikasyonları ve aşırı aneuploidi nedeniyle normalden "
                "çok daha fazla miktarda DNA içerir. Aşırı DNA yükü hematoksilen bazik boyasını koyu tutarak çekirdeklerin "
                "koyu mor/siyah renkte boyanmasına yol açar; bu duruma 'nükleer hiperkromazi' adı verilir. Kromatin homojen "
                "dağılımını kaybedip nükleer membran boyunca kaba kümeler halinde toplanır. Normal bir somatik hücrede nükleus-sitoplazma "
                "(N/S) hacim oranı 1:4 ile 1:6 arasında iken, anaplastik malign hücrelerde dev çekirdek neredeyse tüm sitoplazmayı "
                "doldurarak N/S oranını patolojik olarak '1:1' seviyesine tırmandırır."
            ),
            "elements": [
                make_table(
                    "Normal Hücre vs Anaplastik Malign Hücre Nükleer Karşılaştırması",
                    ["Parametre", "Normal Hücre", "Anaplastik Malign Hücre"],
                    [
                        {
                            "cells": ["Nükleus / Sitoplazma Oranı", "1:4 ile 1:6 arası", "1:1 seviyesine yaklaşır"],
                            "hiddenIndex": 2,
                            "hint": "Çekirdeğin hücreyi tamamen kaplaması"
                        },
                        {
                            "cells": ["Kromatin Boyanması", "Açık ve homojen (Ökromatin)", "Koyu mor/siyah (Hiperkromazi)"],
                            "hiddenIndex": 2,
                            "hint": "Yoğun bazofilik nükleer boyanma"
                        },
                        {
                            "cells": ["Nükleer Membran", "Düzgün, kesintisiz, pürüzsüz", "Girintili çıkıntılı, kalınlaşmış, düzensiz"],
                            "hiddenIndex": 2,
                            "hint": "Zarın çentikli bozuk yapısı"
                        }
                    ]
                ),
                make_cloze(
                    "Anaplastik malign tümör hücrelerinde nükleus aşırı büyüyerek nükleus sitoplazma oranını bire bir seviyesine kadar çıkarır.",
                    "bire bir",
                    "Eşit hacim nükleus sitoplazma oranı"
                )
            ]
        },
        # Slayt 55
        {
            "slideNumber": 55,
            "title": "Belirgin Nükleoller ve Nükleer Organizasyon",
            "content": (
                "Anaplastik kanser hücrelerinde çekirdek içi ribozomal RNA sentezi ve protein üretim fabrikaları aşırı "
                "derecede hızlanmıştır. Bu yoğun transkripsiyonel patlama, çekirdek içinde makronükleollerin (dev nükleollerin) "
                "ortaya çıkmasına neden olur. Nükleoller normalde silik veya küçüktür; oysa malign hücrelerde adeta birer "
                "kuş gözü (owl-eye) gibi parlayan, devasa, eozinofilik veya amfofilik yuvarlak cisimler şeklinde izlenir "
                "(örneğin Hodgkin lenfomadaki Reed-Sternberg hücresi nükleolü veya malign melanom nükleolü). Tek bir çekirdek "
                "içinde birden fazla prominent nükleol bulunması malignitenin en güvenilir sitolojik kriterleri arasındadır."
            ),
            "elements": [
                make_active_recall(
                    "Kanser hücresi çekirdeğinde devasa belirgin nükleollerin (makronükleol) ortaya çıkmasının primer biyokimyasal nedeni nedir?",
                    "Aşırı hızlanmış ribozomal RNA sentezi ve yoğun protein transkripsiyon faaliyetidir.",
                    "Ribozom fabrikası hiperaktivitesi"
                ),
                make_before_after(
                    "Normal Nükleol vs Malign Makronükleol",
                    "Normal İstirahat Hücresi",
                    "Nükleol siliktir, kromatin incedir, nükleus içi yapılar sakin ve dengelidir.",
                    "Malign Hücre (Melanom / Lenfoma)",
                    "Devasa kırmızı-mor makronükleol çekirdeğin merkezinde parlar; aşırı rRNA üretimini belgeler.",
                    "Belirgin nükleol varlığı sitopatolojik malignite tanısında en kritik ipuçlarındandır."
                )
            ]
        },
        # Slayt 56
        {
            "slideNumber": 56,
            "title": "Atipik ve Anormal Mitotik Figürler",
            "content": (
                "Hücre bölünmesini simgeleyen 'mitoz', hızlı prolifere olan normal dokularda da (kemik iliği, bağırsak kriptleri) "
                "sıkça görülebilir; bu nedenle yalnızca mitozun varlığı veya sayısı tek başına malignite kanıtı değildir. "
                "Malignitenin kesin kanıtı 'atipik ve anormal mitotik figürler'dir. Normal bir mitozda iğ iplikleri sentrozomlar "
                "aracılığıyla iki zıt kutba uzanır ve klasik simetrik 'bipolar' metafaz/anafaz tablosu oluşur. Kanser hücrelerinde "
                "ise sentrozom amplifikasyonu nedeniyle üç kutuplu (tripolar), dört kutuplu (kuadripolar) veya yıldız şeklinde "
                "anormal iğ iplikleri oluşur. Mikroskop altında tripolar veya 'Mercedes amblemi' şeklinde görülen bir mitoz, "
                "o dokunun istisnasız malign olduğunu kanıtlayan patognomonik bir bulgudur."
            ),
            "elements": [
                make_causal_chain(
                    "Sentrozom Defektinden Atipik Tripolar Mitoza Uzanan Kaskad",
                    [
                        "1. Sentrozom Aşırılığı: Genomik kararsızlık sonucu hücrede 2 yerine 3 veya daha fazla sentrozomun oluşması",
                        "2. Anormal İğ İplikleri: Kromozomları ayıran mikrotübül ipliklerinin 3 farklı kutba doğru fırlaması",
                        "3. Kaotik Ayrılma: Kromatidlerin düzensiz biçimde üçe bölünerek Mercedes amblemi geometrisi alması",
                        "4. Ağır Anöploidi: Her yavru hücreye eksik veya fazla kromozom dağılarak aşırı genomik kaos yaratılması"
                    ]
                ),
                make_micro_quiz(
                    "Bir doku kesitinde malignitenin tartışmasız kanıtı sayılan mitotik anormallik hangisidir?",
                    [
                        {
                            "text": "Tripolar veya kuadripolar anormal mitotik figürlerin varlığı",
                            "isCorrect": True,
                            "explanation": "Doğrudur; çok kutuplu mitozlar sentrozom defektini ve kesin maligniteyi simgeler."
                        },
                        {
                            "text": "Normal simetrik iki kutuplu bipolar mitozun görülmesi",
                            "isCorrect": False,
                            "explanation": "Bipolar mitoz normal bağırsak veya kemik iliğinde de bolca bulunur."
                        },
                        {
                            "text": "Tüm hücrelerin G0 fazında istirahatte beklemesi",
                            "isCorrect": False,
                            "explanation": "G0 bölünmeyen hücre durumudur, mitotik anormallik değildir."
                        },
                        {
                            "text": "Mitozun 24 saat sürmesi",
                            "isCorrect": False,
                            "explanation": "Süre tek başına atipik mitoz morfolojisini tanımlamaz."
                        }
                    ],
                    "Çok kutuplu (tripolar vb.) mitozlar malignitenin güvenilir mikroskobik kanıtıdır."
                )
            ]
        },
        # Slayt 57
        {
            "slideNumber": 57,
            "title": "Tümör Dev Hücreleri: Polikaryonlar ve Mononükleer Devler",
            "content": (
                "Anaplastik malign tümörlerin tipik bir diğer sitolojik özelliği 'tümör dev hücreleri'dir. Bu hücreler, "
                "komşu hücrelerin anormal füzyonuyla veya mitoz sırasında çekirdeğin bölünmesine rağmen sitoplazmanın "
                "bölünememesi (sitokinezin başarısızlığı) sonucu oluşur. Normal konak dev hücrelerinden 5-10 kat daha büyük "
                "olabilirler. İçlerinde ya tek bir devasa hiperkromatik nükleus (mononükleer tümör devi) ya da onlarca atipik "
                "pleomorfik nükleus yığını (polikaryon) barındırırlar. Bu tümör dev hücreleri, tüberkülozda görülen simetrik "
                "at nalı dizilimli Langhans dev hücreleriyle veya yabancı cisim dev hücreleriyle kesinlikle karıştırılmamalıdır; "
                "tümör dev hücrelerinin nükleusları son derece atipik, hiperkromatik ve biçimsizdir."
            ),
            "elements": [
                make_before_after(
                    "İnflamatuar Dev Hücre vs Tümör Dev Hücresi",
                    "İnflamatuar Dev Hücre (Langhans / Yabancı Cisim)",
                    "Monosit/makrofaj füzyonu, düzgün sınırlı düzenli nükleuslar, at nalı dizilimi, atipi ve hiperkromazi yoktur.",
                    "Tümör Dev Hücresi (Malign Pleomorfik)",
                    "Kanser hücresi füzyonu/sitokinaz defekti, biçimsiz dev çekirdekler, aşırı hiperkromazi, atipik nükleoller.",
                    "Dev hücrenin nükleer atipisi granülomatöz reaksiyonu anaplastik kanserden ayırır."
                ),
                make_cloze(
                    "Sitokinezin aksaması sonucu oluşan ve onlarca atipik nükleus içeren dev kitlelere tümör dev hücreleri adı verilir.",
                    "tümör dev hücreleri",
                    "Malign polikaryon dev hücresi"
                )
            ]
        },
        # Slayt 58
        {
            "slideNumber": 58,
            "title": "Fonksiyonel Bozulma ve Paraneoplastik Ektopik Hormonlar",
            "content": (
                "Tümör hücrelerinin diferansiyasyon derecesi ile sergiledikleri fonksiyonel yetenekler arasında sıkı bir bağ "
                "vardır. İyi diferansiye benign veya düşük dereceli malign tümörler köken aldıkları dokunun fizyolojik fonksiyonlarını "
                "sürdürebilirler: Örneğin iyi diferansiye bir skuamöz karsinom keratin üretir, iyi diferansiye hepatoselüler "
                "karsinom safra salgılar, endokrin tümörler ötopik hormon üretir. Ancak tümör anaplastik hale geldikçe normal "
                "fonksiyonlar çöker. Bunun yerine epigenetik susturmanın kalkması sonucu o dokuda normalde hiç üretilmeyen "
                "'ektopik hormonlar' üretilmeye başlar; örneğin akciğer küçük hücreli karsinomunun ACTH veya ADH salgılayarak "
                "Cushing sendromu veya uygunsuz ADH sendromu (SIADH) yapması gibi 'paraneoplastik sendromlar' doğar."
            ),
            "elements": [
                make_table(
                    "Tümör Diferansiyasyonuna Göre Fonksiyonel Salgılar",
                    ["Tümör Tipi", "Diferansiyasyon Düzeyi", "Salgılanan Tipik Ürün"],
                    [
                        {
                            "cells": ["Skuamöz Hücreli Karsinom", "İyi Diferansiye", "Keratin protein birikimi (Keratin incisi)"],
                            "hiddenIndex": 2,
                            "hint": "Yassı epitel koruyucu proteini"
                        },
                        {
                            "cells": ["Hepatoselüler Karsinom", "İyi Diferansiye", "Yeşil safra pigmenti sentezi"],
                            "hiddenIndex": 2,
                            "hint": "Karaciğer salgı sıvısı"
                        },
                        {
                            "cells": ["Akciğer Küçük Hücreli Karsinom", "Az Diferansiye / Nöroendokrin", "Ektopik ACTH ve ADH (Paraneoplastik)"],
                            "hiddenIndex": 2,
                            "hint": "Fizyolojik odağı dışı endokrin salınım"
                        }
                    ]
                ),
                make_active_recall(
                    "Akciğer küçük hücreli karsinomunun ektopik olarak ACTH salgılayarak Cushing sendromu yapması hangi klinik fenomenin örneğidir?",
                    "Paraneoplastik sendrom örneğidir.",
                    "Tümörün uzak ektopik hormonal etkisi"
                )
            ]
        },
        # Slayt 59 [CHECKPOINT 6]
        {
            "slideNumber": 59,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Diferansiyasyon ve Anaplazi",
            "content": (
                "Bu bölümde diferansiyasyon kavramını, anaplazinin morfolojik kriterlerini ve fonksiyonel yansımalarını inceledik. "
                "Diferansiyasyon, tümör hücrelerinin normal hücrelere benzerlik derecesidir; anaplazi ise diferansiyasyonun tamamen kaybolmasıdır. "
                "Anaplazi malignitenin tartışmasız en güvenilir histopatolojik kanıtıdır. "
                "Anaplazinin mikroskobik kriterleri: Hücresel/nükleer pleomorfizm, aşırı hiperkromazi, nükleus-sitoplazma (N/S) oranının 1:1'e çıkmasıdır. "
                "Kanser hücrelerinde ribozomal aşırı aktivite nedeniyle dev nükleoller (makronükleol) parlar. "
                "Malignitenin kesin mitotik ölçütü tripolar veya kuadripolar anormal mitotik figürlerdir. "
                "Tümör dev hücreleri atipik nükleuslarıyla inflamatuar Langhans hücrelerinden ayrılır. "
                "İyi diferansiye tümörler keratin veya safra üretirken, az diferansiye tümörler ektopik hormon salgılayarak paraneoplastik sendromlara yol açar."
            ),
            "flashcards": [
                {
                    "id": "k1-28-cp06-fc01",
                    "front": "Tümör parankim hücrelerinin köken aldıkları dokuya yapısal benzerliğini tamamen yitirmesini tanımlayan ve maligniteyi kanıtlayan terim nedir?",
                    "back": "Anaplazi terimidir.",
                    "hint": "Diferansiyasyonun bütünüyle yok olması"
                },
                {
                    "id": "k1-28-cp06-fc02",
                    "front": "Normal hücrede 1:4 ile 1:6 olan nükleus-sitoplazma (N/S) oranı anaplastik kanser hücresinde hangi patolojik seviyeye çıkar?",
                    "back": "Bire bir (1:1) seviyesine çıkar.",
                    "hint": "Çekirdeğin tüm sitoplazmayı kaplaması"
                },
                {
                    "id": "k1-28-cp06-fc03",
                    "front": "Doku kesitinde saptandığında malignitenin kesin patognomonik kanıtı sayılan çok kutuplu mitoz türü nedir?",
                    "back": "Tripolar veya kuadripolar atipik mitozdur.",
                    "hint": "Sentrozom defektine bağlı çoklu kutup"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 6 Özet Tablosu: Anaplazinin Sitopatolojik Kriterleri",
                    ["Kriter", "Patolojik Görünüm", "Biyolojik Anlamı"],
                    [
                        {
                            "cells": ["N/S Oranı", "1:1", "Dev çekirdek, yetersiz sitoplazma"],
                            "hiddenIndex": 1,
                            "hint": "Eşit hacimsel nükleer büyüme"
                        },
                        {
                            "cells": ["Atipik Mitoz", "Tripolar / Kuadripolar", "Genomik instabilite ve sentrozom fazlalığı"],
                            "hiddenIndex": 1,
                            "hint": "Çok kutuplu iğ iplikleri"
                        }
                    ]
                )
            ]
        },
        # Slayt 60
        {
            "slideNumber": 60,
            "title": "Klinik Karar: Histopatolojik Derecelendirme (Grading)",
            "content": (
                "Patoloji raporunda yer alan 'Grade' (derece), tümörün histolojik diferansiyasyon derecesini ve mitoz "
                "sayısını sayısal olarak ifade eden prognostik bir parametredir. Grade I (İyi diferansiye), Grade II (Orta "
                "diferansiye), Grade III (Az diferansiye) ve Grade IV (Anaplastik/undiferansiye) olarak derecelendirilir. "
                "Klinisyen unutmamalıdır ki 'Grade' ile 'Stage' (Evre) tamamen farklı kavramlardır. Grade mikroskop altındaki "
                "hücresel saldırganlığı ve atipiyi gösterirken, Stage (TNM evrelemesi) tümörün vücuttaki anatomik yayılım "
                "büyüklüğünü gösterir. Prognostik açıdan Stage daima Grade'den daha belirleyicidir; ancak cerrahi sonrası "
                "adjuvan kemoterapi kararı verilirken yüksek Grade varlığı en kritik endikasyonlardan birini teşkil eder."
            ),
            "elements": [
                make_branching_logic(
                    "Prostat biyopsisinde Gleason skoru 9 (4+5) yani Grade 5 az diferansiye adenokarsinom saptanan ancak tomografisinde uzak metastazı olmayan (T2N0M0 - Evre 2) bir hasta değerlendiriliyor.",
                    "Hastanın 'Grade' (derece) ve 'Stage' (evre) kavramları açısından onkolojik durumu nasıl yorumlanmalıdır?",
                    [
                        {
                            "text": "Tümör erken anatomik evrededir (Stage 2) ancak mikroskobik olarak son derece saldırgan ve yüksek derecelidir (Grade 5); agresif sistemik tedavi riski taşır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; Stage tümörün anatomik yayılımını, Grade ise mikroskobik saldırganlığını gösterir."
                        },
                        {
                            "text": "Grade ve Stage aynı şeydir, hasta son evre ölümcül metastatik kabul edilmelidir.",
                            "isCorrect": False,
                            "explanation": "Grade ile Stage farklıdır; metastaz olmadığı için son evre değildir."
                        },
                        {
                            "text": "Tümör iyi huylu kabul edilmeli ve tedavi verilmemelidir.",
                            "isCorrect": False,
                            "explanation": "Gleason 9 prostat kanseri son derece yüksek dereceli malign bir tümördür."
                        }
                    ]
                )
            ]
        }
    ]
