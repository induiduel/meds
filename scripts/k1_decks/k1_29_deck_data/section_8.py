# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 29: Karsinojenezin Moleküler Temeli
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 8: Radyasyon Karsinogenezi ve Tümör İnflamatuar Mikroçevresi (Slayt 71 - 80)
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
            "title": "İyonlaştırıcı Radyasyon Biyofiziği",
            "content": (
                "İyonlaştırıcı radyasyon (X-ışınları, gama ışınları, alfa ve beta parçacıkları, nötronlar), "
                "maddeden geçerken atomlardan elektron koparacak kadar yüksek enerji taşıyan elektromanyetik "
                "veya korpüsküler radyasyondur. Hücresel karsinogenez iki yolla tetiklenir: **Doğrudan etki**, "
                "radyasyon fotonunun doğrudan DNA omurgasına çarparak fosfodiester bağlarını koparmasıdır. "
                "**Dolaylı etki** ise (hasarların ~%70'inden sorumludur), hücre içi su moleküllerinin radyoliz "
                "edilerek yüksek reaktiviteye sahip serbest hidroksil radikallerinin (OH*) üretilmesidir. "
                "İyonlaştırıcı radyasyonun hücre genomunda oluşturduğu en karakteristik ve onarımı en zor lezyon "
                "**DNA çift iplik kırıklarıdır (DSB)**; bu kırıklar kromozomal delesyonlara, inversiyonlara ve "
                "onkojenik translokasyonlara yol açar."
            ),
            "elements": [
                make_cloze(
                    "İyonlaştırıcı radyasyonun hücredeki hasarının yaklaşık yüzde yetmişi suyun radyolizi sonucu serbest radikaller oluşumuyla gelişir.",
                    "radikaller",
                    "Yüksek reaktif oksijen türevleri"
                ),
                make_table(
                    "İyonlaştırıcı Radyasyonun DNA Hasar Mekanizmaları",
                    ["Etki Mekanizması", "Oluşum Yolu", "Birincil Genomik Lezyon"],
                    [
                        {
                            "cells": ["Doğrudan Etki", "Fotonun DNA fosfodiester zincirine direkt çarpması", "Tek ve çift iplik kırıkları"],
                            "hiddenIndex": 1,
                            "hint": "Hedef moleküle aracısız temas"
                        },
                        {
                            "cells": ["Dolaylı Etki (%70)", "Hücre içi suyun radyolizi ile OH* radikali üretimi", "Oksidatif baz hasarı ve çift iplik kopmaları"],
                            "hiddenIndex": 1,
                            "hint": "Su moleküllerinin parçalanması süreci"
                        }
                    ]
                )
            ]
        },

        # Slayt 72
        {
            "slideNumber": 72,
            "title": "İyonlaştırıcı Radyasyon Kanserleri: Lösemi ve Çernobil",
            "content": (
                "İyonlaştırıcı radyasyona maruziyet sonucu gelişen malignitelerin organ dağılımı ve ortaya çıkış "
                "zamanı (latent periyot) belirgin biyolojik kurallara uyar. Hiroşima ve Nagazaki atom bombası "
                "kurtulanlarında yapılan epidemiyolojik çalışmalarda, radyasyon sonrası en erken ortaya çıkan "
                "malignitenin **akut ve kronik miyeloid lösemi** olduğu gösterilmiştir; lösemi insidansı maruziyetten "
                "yaklaşık 5-7 yıl sonra zirve yapar. Katı solid karsinomların (tiroid, meme, akciğer, kolon ve "
                "tükürük bezi) ortaya çıkması için ise en az 10 ila 30 yıllık uzun bir latent dönem gerekir. "
                "1986 Çernobil nükleer reaktör kazasından sonra atmosfere yayılan radyoaktif iyot (I-131) izotopuna "
                "maruz kalan çocuklarda, tiroid follikül hücrelerinde karakteristik **RET/PTC füzyon translokasyonu** "
                "zemininde kitlesel bir **Papiller Tiroid Karsinomu** salgını patlak vermiştir."
            ),
            "elements": [
                make_before_after(
                    "Radyasyon Sonrası Lösemi vs Solid Tümör Latent Dönemleri",
                    "Radyasyona Bağlı Lösemiler",
                    "En erken gelişen malignitelerdir; maruziyetten yaklaşık 5-7 yıl sonra pik yapar ve 15 yıl sonra normale döner.",
                    "Radyasyona Bağlı Solid Karsinomlar",
                    "Uzun latent periyoda sahiptir (10-30 yıl sonra ortaya çıkar); tiroid, meme, akciğer karsinomları ömür boyu risk oluşturur.",
                    "Lösemi hematopoetik öncüllerin yüksek mitoz hızından dolayı erken, solid tümörler yavaş birikimle geç belirir."
                ),
                make_active_recall(
                    "Çernobil nükleer kazası sonrası radyoaktif iyot maruziyeti kalan çocuklarda papiller tiroid karsinomuna yol açan karakteristik füzyon lezyonu nedir?",
                    "RET/PTC kromozomal füzyon translokasyonudur.",
                    "Tirozin kinaz kimerik proteini"
                )
            ]
        },

        # Slayt 73
        {
            "slideNumber": 73,
            "title": "Ultraviyole (UV) Radyasyon ve Cilt Karsinogenezi",
            "content": (
                "Güneş ışığından kaynaklanan ultraviyole radyasyon, dalga boyuna göre üçe ayrılır: UVA (320-400 nm), "
                "UVB (290-320 nm) ve UVC (200-290 nm). Ozon tabakası UVC ışınlarını tamamen süzdüğü için biyolojik "
                "açıdan cilt kanserlerinin asıl sorumlusu **UVB radyasyonudur** (UVA ise serbest radikaller üretir). "
                "UVB fotonları epidermiste keratinosit ve melanosit DNA'sına çarparak pirimidin dimerleri oluşturur; "
                "bu hasarlar onarılamazsa **Malign Melanom**, **Skuamöz Hücreli Karsinom (SCC)** ve **Bazal Hücreli "
                "Karsinom (BCC)** gelişir. İlginç olarak maruziyet paterni kanser tipini belirler: Ömür boyu "
                "sürekli kümülatif güneş maruziyeti (örneğin çiftçiler, denizciler) cilt SCC ve BCC riskini "
                "artırırken; çocuklukta veya gençlikte yaşanan yoğun, aralıklı güneş yanıkları (tatil yanıkları) "
                "**Malign Melanom** için en tehlikeli tetikleyicidir."
            ),
            "elements": [
                make_table(
                    "Güneş Işığı Maruziyet Paternleri ve Cilt Kanseri Tipleri",
                    ["Maruziyet Tipi", "Tipik Popülasyon", "Primer Tetiklenen Malignite"],
                    [
                        {
                            "cells": ["Kümülatif Sürekli Güneş", "Açık hava işçileri, çiftçiler, balıkçılar", "Skuamöz Hücreli Karsinom (SCC) ve BCC"],
                            "hiddenIndex": 2,
                            "hint": "Yassı epitel kaynaklı cilt tümörü"
                        },
                        {
                            "cells": ["Aralıklı Yoğun Güneş Yanığı", "Hafta sonu güneşlenen açık tenliler", "Malign Melanom"],
                            "hiddenIndex": 2,
                            "hint": "Melanosit kökenli ölümcül neoplazm"
                        }
                    ]
                ),
                make_cloze(
                    "Çocukluk çağındaki şiddetli aralıklı büllöz güneş yanıkları erişkin dönemde malign melanom gelişimi için majör risk faktörüdür.",
                    "melanom",
                    "Pigment üreten melanosit neoplazmı"
                )
            ]
        },

        # Slayt 74
        {
            "slideNumber": 74,
            "title": "Tümörü Destekleyen Kronik İnflamasyon",
            "content": (
                "Ünlü patolog Rudolf Virchow 1863 yılında tümörlerin kronik inflamasyon alanlarında geliştiğini "
                "fark etmiş ve 'kanser iyileşmeyen bir yara gibidir' tezini ortaya koymuştur. Günümüzde tümörü "
                "destekleyen inflamasyon, kanserin temel bir **etkinleştirici zemini (enabling characteristic)** "
                "olarak kabul edilmektedir. Kronik inflamasyon mikroçevresinde toplanan reaktif hücreler (makrofajlar, "
                "nötrofiller), ortama bol miktarda **reaktif oksijen türleri (ROS)** ve azot radikalleri salarak "
                "komşu hücrelerin DNA'sında doğrudan mutasyonlar oluşturur. Aynı zamanda salınan inflamatuar sitokinler "
                "(TNF, IL-1, IL-6), doku tamirini tetikleme kisvesi altında tümör hücrelerinin proliferasyonunu "
                "uyarır, apoptoz direnci sağlar, matriksi yıkarak invazyonu kolaylaştırır ve neoanjiyogenezi besler."
            ),
            "elements": [
                make_causal_chain(
                    "Kronik İnflamasyondan Malign Transformasyona İlerleme Kaskadı",
                    [
                        "1. Kalıcı Doku Hasarı: Kronik enfeksiyon veya otoimmünite mukozada devamlı hücresel yıkım yaratır.",
                        "2. Oksidatif Nükleik Hasar: İnflamatuar fagositlerin ürettiği ROS epitel kök hücrelerinde sürücü mutasyonlar kurar.",
                        "3. Sitokin Bağımlı Çoğalma: Salınan IL-6 ve TNF, NF-kB ve STAT3 yollarını tetikleyerek bölünmeyi kamçılar.",
                        "4. Reaktif Yara Stroması: Fibroblastlar miyofibroblastlara dönüşerek tümör için koruyucu stroma örer.",
                        "5. İnvaziv Karsinom İlerlemesi: Metalloproteinazlar bazal membranı eritir ve kanser stromaya penetre olur."
                    ]
                ),
                make_active_recall(
                    "Kronik doku inflamasyonu sırasında makrofaj ve nötrofillerden salınarak çevre kök hücrelerde mutajenik DNA hasarı oluşturan serbest moleküller nelerdir?",
                    "Reaktif oksijen ve azot radikalleridir (ROS ve RNS).",
                    "Serbest oksijenli kimyasal türevler"
                )
            ]
        },

        # Slayt 75
        {
            "slideNumber": 75,
            "title": "Kanserle İlişkili Fibroblastlar (CAF)",
            "content": (
                "Malign bir tümör kitlesi yalnızca kanser hücrelerinden ibaret değildir; hacminin büyük kısmını "
                "**reaktif tümör stroması** oluşturur. Bu stromanın ana orkestra şefi **Kanserle İlişkili "
                "Fibroblastlardır (Cancer-Associated Fibroblasts - CAF)**. Kanser hücrelerinin salgıladığı **TGF-beta**, "
                "PDGF ve FGF sitokinleri, çevre normal bağ dokusu fibroblastlarını ve perisitleri uyararak onları "
                "alfa-düz kas aktini (alfa-SMA) eksprese eden kontraktil **miyofibroblastlara (CAF)** dönüştürür. "
                "CAF'lar yoğun Tip I kolajen ve fibronektin sentezleyerek tümörün etrafında taş sertliğinde "
                "bir bağ dokusu zırhı örerler; bu patolojik sürece **desmoplazi** denir (örneğin meme ve pankreas "
                "karsinomları). Ayrıca salgıladıkları CXCL12 (SDF-1) ile kemik iliğinden endotel öncüllerini "
                "çağırarak anjiyogenezi körüklerler."
            ),
            "elements": [
                make_before_after(
                    "Sakin Normal Fibroblast vs Kanserle İlişkili Fibroblast (CAF)",
                    "Normal Doku Fibroblastı",
                    "Sakin (quiescent) durumdadır; doku bütünlüğünü korur, minimal matriks üretir, alfa-SMA negatiftir.",
                    "Kanserle İlişkili Fibroblast (CAF)",
                    "Miyofibroblastik fenotip (alfa-SMA pozitif); yoğun kollajen (desmoplazi) üretir, kanser hücresine büyüme faktörü pompalar.",
                    "Desmoplastik fibröz stroma kemoterapötik ilaçların tümör merkezine difüzyonunu mekanik olarak engeller."
                ),
                make_cloze(
                    "Kanser hücrelerinin salgıladığı TGF-beta etkisiyle fibroblastların aşırı kolajen üreterek oluşturduğu sert fibröz stroma yanıtına desmoplazi denir.",
                    "desmoplazi",
                    "Taş sertliğinde bağ dokusu zırhı reaksiyonu"
                )
            ]
        },

        # Slayt 76
        {
            "slideNumber": 76,
            "title": "Tümör İlişkili Makrofajlar (TAM): M1 vs M2 Polarizasyonu",
            "content": (
                "Tümör stromasını en yoğun şekilde infiltre eden lökositler makrofajlardır; bu hücrelere **Tümör "
                "İlişkili Makrofajlar (Tumor-Associated Macrophages - TAM)** adı verilir. Makrofajlar mikroçevreden "
                "aldıkları sinyallere göre iki zıt fenotipe polarize olurlar: **M1 Makrofajlar (Klasik aktive)**, "
                "IFN-gama ve mikrobiyal ürünlerle uyarılır; bol IL-12 ve nitrik oksit (NO) üreterek tümör "
                "hücrelerini öldüren **antitümöral** savaşçılardır. Buna karşılık tümör hücrelerinin salgıladığı "
                "IL-4, IL-10, IL-13 ve TGF-beta ortamında olgunlaşan **M2 Makrofajlar (Alternatif aktive)** ise tam bir "
                "**protümöral hain** gibi davranır. M2 TAM'lar VEGF salgılayarak damarlanmayı artırır, MMP'ler ile "
                "matriksi parçalayarak metastazı kolaylaştırır ve arginaz-1 ile T lenfositleri baskılarlar. İleri "
                "evre kanserlerde TAM popülasyonu neredeyse tamamen M2 fenotipindedir."
            ),
            "elements": [
                make_table(
                    "M1 Antitümör Makrofaj ile M2 Protümör Makrofaj Karşılaştırması",
                    ["Özellik", "M1 Makrofaj (Klasik Aktive)", "M2 Makrofaj (TAM, Alternatif Aktive)"],
                    [
                        {
                            "cells": ["Uyaran Sitokinler", "IFN-gama, endotoksin (LPS)", "IL-4, IL-10, IL-13, TGF-beta"],
                            "hiddenIndex": 2,
                            "hint": "İnflamatuar Th2 kaynaklı sitokinler"
                        },
                        {
                            "cells": ["Kanser Üzerindeki Etkisi", "Antitümöral (Tümör hücresini öldürür)", "Protümöral (Büyüme, anjiyogenez ve metastaz desteği)"],
                            "hiddenIndex": 2,
                            "hint": "Kanser ilerlemesini besleyen rol"
                        },
                        {
                            "cells": ["Salgılanan Moleküller", "IL-12, TNF-alfa, Reaktif NO", "VEGF, EGF, MMP-9, Arginaz-1"],
                            "hiddenIndex": 2,
                            "hint": "Damar yapıcı ve matriks eritici faktörler"
                        }
                    ]
                ),
                make_active_recall(
                    "Tümör mikroçevresinde VEGF ve matriks metalloproteinazlar salgılayarak karsinogenezi ve metastazı besleyen alternatif makrofaj fenotipi hangisidir?",
                    "M2 fenotipindeki alternatif aktive makrofajlardır (TAM).",
                    "Protümöral polarize mononükleer hücre"
                )
            ]
        },

        # Slayt 77
        {
            "slideNumber": 77,
            "title": "İmmünosüpresif Hücresel Kalkan: MDSC ve Treg",
            "content": (
                "İlerleyen maligniteler konak immün sisteminin saldırılarından korunmak için stroma içinde "
                "özel bir immünosüpresif hücresel kalkan oluşturur. Bu kalkanın iki ana aktörü vardır: **Miyeloid "
                "Kaynaklı Baskılayıcı Hücreler (MDSC)** ve **Regülatuvar T Hücreleri (Treg)**. MDSC'ler kemik iliğinden "
                "tümör faktörleriyle (G-CSF, GM-CSF) çağrılan olgunlaşmamış granülositik ve monositik öncüllerdir. "
                "Ortama bol miktarda Arginaz-1 ve reaktif oksijen salarak sitotoksik T hücrelerinin proliferasyonunu "
                "durdururlar. **FoxP3+ CD4+ CD25+ Regülatuvar T hücreleri (Treg)** ise fizyolojik olarak otoimmüniteyi "
                "frenleyen hücrelerdir; tümör stromasında aşırı birikerek salgıladıkları **IL-10 ve TGF-beta** ile "
                "sitotoksik CD8+ T lenfositleri ve NK hücrelerini tamamen felç ederler. Tümörde yüksek Treg infiltrasyonu "
                "tedavi başarısızlığı ve kötü prognozla koreledir."
            ),
            "elements": [
                make_table(
                    "İmmünosüpresif Stroma Hücreleri Karşılaştırması",
                    ["Hücre Grubu", "Belirleyici İmmünofenotipik Belirteç", "Temel İmmünsüpresif Mekanizma"],
                    [
                        {
                            "cells": ["Regülatuvar T Hücresi (Treg)", "CD4+, CD25+, FoxP3+ nükleer pozitiflik", "IL-10 ve TGF-beta ile lenfosit baskılama"],
                            "hiddenIndex": 1,
                            "hint": "FoxP3 transkripsiyon faktörü taşıyan lenfosit"
                        },
                        {
                            "cells": ["Miyeloid Baskılayıcı Hücre (MDSC)", "CD11b+, CD33+, HLA-DR negatif", "Arginaz-1 ve ROS ile T hücre beslenmesini kesme"],
                            "hiddenIndex": 1,
                            "hint": "İmmatür miyeloid hücre belirteçleri"
                        }
                    ]
                ),
                make_cloze(
                    "Tümör mikroçevresinde sitotoksik lenfositleri baskılayan regülatuvar T hücrelerinin ana transkripsiyon faktörü FoxP3 molekülüdür.",
                    "FoxP3",
                    "Treg belirteci çatal başlı protein"
                )
            ]
        },

        # Slayt 78
        {
            "slideNumber": 78,
            "title": "Sitokinler ve Anjiyogenik Faktörler: TGF-beta Sinerjisi",
            "content": (
                "Tümör mikroçevresindeki hücresel diyalog çözünür sitokinler ve kemokinler aracılığıyla yürütülür. "
                "Bu sitokin ağının en paradoksal ve güçlü molekülü **TGF-beta'dır (Transforme Edici Büyüme Faktörü)**. "
                "TGF-beta normal epitel hücreleri için güçlü bir büyüme inhibitörüdür (CDK inhibitörlerini uyararak "
                "siklus durdurur). Ancak karsinogenez ilerledikçe kanser hücreleri TGF-beta'nın antiproliferatif "
                "etkisine direnç kazanırlar ve bizzat kendileri ortama masif TGF-beta pompalamaya başlarlar. "
                "Bu aşamada TGF-beta tam bir 'onkolojik canavara' dönüşür: Epitelyal-mezenkimal transdiferansiyasyonu "
                "(EMT) tetikler, CAF'ları uyararak desmoplazi yaptırır, Treg'leri çekerek immüniteyi baskılar "
                "ve **VEGF** üretimini artırarak damarlanmayı hızlandırır."
            ),
            "elements": [
                make_before_after(
                    "TGF-beta'nın Erken Evre vs İleri Evre Kanser Biyolojisindeki Rolü",
                    "Erken Evre (Tümör Baskılayıcı Rol)",
                    "Normal epitelde p15 ve p21'i uyarır, MYC'yi baskılar; hücre siklusunu G1 evresinde kilitler ve apoptozu destekler.",
                    "İleri Evre (Protümöral ve Metastatik Rol)",
                    "Baskılayıcı yol inaktifleşir; EMT'yi tetikler, E-kadherini yıkar, motiliteyi, desmoplaziyi ve immün kaçışı körükler.",
                    "TGF-beta tümör baskılayıcılıktan metastaz promotörlüğüne dönüşen prototipik bifazik sitokindir."
                ),
                make_active_recall(
                    "Normal epitelde büyümeyi durduran ancak ileri evre kanserde EMT, desmoplazi ve immünsüpresyonu yöneten majör bifazik sitokin hangisidir?",
                    "TGF-beta sitokinidir (Transforming Growth Factor-beta).",
                    "Transforme edici büyüme faktörü"
                )
            ]
        },

        # Slayt 79: CHECKPOINT 8
        {
            "slideNumber": 79,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Radyasyon ve Tümör İnflamatuar Mikroçevresi",
            "content": (
                "Sekizinci bölümün bu tekrar sayfasında, radyasyon karsinogenezi ve tümörü destekleyen stromal "
                "mikroçevre faktörleri özetlenmektedir. İyonlaştırıcı radyasyon suyun radyolizi ile OH* radikalleri "
                "ve çift iplik kırıkları üretir; lösemiler erken (5-7 yıl), solid tümörler geç (10-30 yıl) belirir "
                "(Çernobil sonrası tiroid RET/PTC). Güneş UVB'si timin dimerleri ile melanom, SCC ve BCC yapar; "
                "yoğun aralıklı güneş yanığı melanom riskidir. Tümör mikroçevresi kronik inflamasyonla mutasyon "
                "ve proliferasyonu besler; Kanserle İlişkili Fibroblastlar (CAF) desmoplazi örer. TAM makrofajları "
                "protümöral M2 fenotipindedir; FoxP3+ Treg ve MDSC hücreleri sitotoksik lenfositleri felç eder; "
                "TGF-beta ise EMT ve immün kaçışı koordine eder."
            ),
            "flashcards": [
                {
                    "id": "k1-29-cp08-fc01",
                    "front": "1986 Çernobil nükleer kazası sonrası radyoaktif iyot maruziyeti kalan çocuklarda salgın şeklinde artan kanser türü nedir?",
                    "back": "Papiller Tiroid Karsinomudur (RET/PTC füzyonu).",
                    "hint": "Boğaz ön bölgesi endokrin bezi malignitesi"
                },
                {
                    "id": "k1-29-cp08-fc02",
                    "front": "Tümör mikroçevresinde sitotoksik T hücrelerini baskılayan ve immün kaçış kalkanı kuran regülatuvar T hücrelerinin kilit transkripsiyon faktörü nedir?",
                    "back": "FoxP3 transkripsiyon faktörüdür.",
                    "hint": "Treg hücresinin nükleer belirteci"
                },
                {
                    "id": "k1-29-cp08-fc03",
                    "front": "Tümör stromasında kanser hücrelerinin salgılarıyla aktive olarak taş sertliğinde desmoplazi üreten fibroblastlara ne ad verilir?",
                    "back": "Kanserle İlişkili Fibroblastlar (CAF) adı verilir.",
                    "hint": "Miyofibroblastik stromayı oluşturan neoplastik bağ dokusu hücreleri"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 8 Özet Tablosu: Mikroçevre ve Radyasyon",
                    ["Hücre / Etken", "Temel Biyolojik Rol", "Klinik Onkolojik Sonuç"],
                    [
                        {
                            "cells": ["Kanser İlişkili Fibroblast (CAF)", "Alfa-SMA pozitif desmoplazi üretimi", "İlaç penetrasyonunun bozulması"],
                            "hiddenIndex": 0,
                            "hint": "Miyofibroblastik bağ dokusu hücresi"
                        },
                        {
                            "cells": ["M2 Polarize TAM", "VEGF ve MMP salınımı ile doku remodelingi", "Anjiyogenez ve uzak metastaz desteği"],
                            "hiddenIndex": 0,
                            "hint": "Protümöral mononükleer fagositer hücre"
                        }
                    ]
                )
            ]
        },

        # Slayt 80
        {
            "slideNumber": 80,
            "title": "Klinik Karar: Radyasyon Maruziyeti Öyküsünde Tiroid Nodülü Yönetimi",
            "content": (
                "Çocukluk veya gençlik çağında baş-boyun bölgesine radyoterapi almış (örneğin Hodgkin lenfoma, "
                "timus büyümesi veya tinea kapitis tedavisi) veya nükleer kaza bölgesinde bulunmuş bireyler, "
                "yaşam boyu tiroid maligniteleri açısından yüksek riskli kabul edilir. Radyasyon maruziyetinden "
                "10-25 yıl sonra tiroid bezinde palpe edilen soliter soğuk nodüllerde malignite olasılığı normal "
                "popülasyondan (%5) çok daha yüksektir (%30-50). Bu olgularda ultrasonografide mikrokalsifikasyon, "
                "düzensiz sınır ve hipoekoik yapı saptandığında derhal **İnce İğne Aspirasyon Biyopsisi (İİAB)** "
                "yapılmalı ve nükleer özellikler (buzlu cam nükleus, yarıklar, psödoinklüzyonlar) incelenerek "
                "papiller karsinom teyit edilmelidir."
            ),
            "elements": [
                make_branching_logic(
                    "34 yaşında kadın hasta boyun sağ tarafında ağrısız kitle ile başvuruyor. Öyküsünden 12 yaşındayken Hodgkin lenfoma nedeniyle mediastinal ve servikal manto alanı radyoterapisi aldığı öğreniliyor. Tiroid ultrasonografisinde sağ lobda 1.8 cm çapında, hipoekoik, mikrokalsifikasyonlar içeren solid nodül saptanıyor.",
                    "Bu hastanın öyküsü ve radyolojik bulguları karşısında onkoloji ve endokrin konseyinin izlemesi gereken en doğru tanısal ve cerrahi yaklaşım nedir?",
                    [
                        {
                            "text": "Radyasyon öyküsü tiroid malignitesi riskini ileri derecede artırdığından nodüle derhal USG eşliğinde İİAB yapılmalı; papiller karsinom saptanırsa total tiroidektomi planlanmalıdır.",
                            "isCorrect": True,
                            "explanation": "Radyasyon maruziyeti papiller tiroid karsinomunun (RET/PTC) en güçlü risk faktörüdür; şüpheli nodülde derhal biyopsi ve malignitede total cerrahi şarttır."
                        },
                        {
                            "text": "Radyasyon üzerinden 20 yıldan fazla zaman geçtiği için risk sıfırlanmıştır; nodül 6 ay sonra ultrasonla yeniden ölçülmelidir.",
                            "isCorrect": False,
                            "explanation": "Solid tümörlerde radyasyon riski 10-30 yıl sonra ortaya çıkar ve ömür boyu sürer."
                        },
                        {
                            "text": "Hastaya nodülü eritmek amacıyla yüksek doz radyoaktif iyot verilerek cerrahi dışlanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Biyopsi ve tanı konulmadan radyoaktif iyot ablasyonu yapılamaz; primer tedavi cerrahidir."
                        }
                    ]
                ),
                make_micro_quiz(
                    "Baş-boyun bölgesine iyonlaştırıcı radyasyon maruziyeti öyküsü olan bireylerde yıllar sonra en sık gelişen epitelyal tiroid bezi malignitesi hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "Papiller Tiroid Karsinomu",
                            "isCorrect": True,
                            "explanation": "İyonizan radyasyon RET/PTC translokasyonu üzerinden en sık papiller tiroid karsinomunu tetikler."
                        },
                        {
                            "key": "B",
                            "text": "Medüller Tiroid Karsinomu",
                            "isCorrect": False,
                            "explanation": "Medüller karsinom parafolliküler C hücrelerinden köken alır ve MEN2 sendromuyla ilişkilidir."
                        },
                        {
                            "key": "C",
                            "text": "Tiroid Folliküler Adenomu",
                            "isCorrect": False,
                            "explanation": "Adenoma selim bir neoplazmdır; radyasyonun majör malign tehdidi papiller karsinomdur."
                        },
                        {
                            "key": "D",
                            "text": "Tiroid Hürthle Hücreli Tümörü",
                            "isCorrect": False,
                            "explanation": "Onkositik folliküler neoplazmdır, radyasyonla spesifik ilişkisi papiller karsinom kadar belirgin değildir."
                        }
                    ],
                    "Radyasyon maruziyetinin prototipik endokrin malignitesi papiller tiroid karsinomudur."
                )
            ]
        }
    ]
