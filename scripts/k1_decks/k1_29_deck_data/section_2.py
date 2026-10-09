# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 29: Karsinojenezin Moleküler Temeli
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 2: Nokta Mutasyonları ve Kromozomal Translokasyonlar (Slayt 11 - 20)
Checkpoint: Slayt 19
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_2_slides():
    return [
        # Slayt 11
        {
            "slideNumber": 11,
            "title": "Kanser Genlerinde Nokta Mutasyonları",
            "content": (
                "Nokta mutasyonları, DNA zincirinde tek bir nükleotid bazının değişmesi (transisyon veya "
                "transversiyon) sonucu kodlanan amino asidin değişmesi (yanlış anlamlı/missense) veya erken bir dur "
                "kodonunun oluşması (anlamsız/nonsense) ile karakterizedir. İnsan solid tümörlerinde en sık "
                "saptanan genetik lezyon tipi nokta mutasyonlarıdır. Protoonkogenlerde nokta mutasyonu işlev kazanımına "
                "yol açar; prototipik örnek **RAS gen ailesidir (KRAS, NRAS, HRAS)**. KRAS'ın 12, 13 veya 61. "
                "kodonlarındaki tek baz değişimi, GTP hidrolizini engelleyerek proteini sürekli aktif tutar. Buna "
                "karşılık tümör baskılayıcı **TP53** geninde meydana gelen nokta mutasyonları, proteinin DNA'ya "
                "bağlanma bölgesini (core domain) bozarak işlev kaybına ve apoptoz tetiğinin düşmesine neden olur."
            ),
            "elements": [
                make_cloze(
                    "Solid tümörlerde en sık mutasyona uğrayan protoonkogen ailesi RAS gen ailesidir.",
                    "RAS",
                    "GTP bağlayan onkojenik sinyal proteini"
                ),
                make_table(
                    "Protoonkogen vs Tümör Baskılayıcıda Nokta Mutasyon Sonucu",
                    ["Gen Örneği", "Genin Sınıfı", "Mutasyonun Odak Bölgesi", "Fonksiyonel Moleküler Netice"],
                    [
                        {
                            "cells": ["KRAS Geni", "Protoonkogen", "Kodon 12, 13 veya 61", "GTPaz aktivitesi felci ve kesintisiz proliferasyon"],
                            "hiddenIndex": 3,
                            "hint": "GTP hidrolizinin durması sonucu bölünme"
                        },
                        {
                            "cells": ["TP53 Geni", "Tümör Baskılayıcı", "DNA bağlama bölgesi", "Hedef promotörlere bağlanamama ve apoptoz kaybı"],
                            "hiddenIndex": 3,
                            "hint": "Transkripsiyonel uyarının felç olması"
                        }
                    ]
                )
            ]
        },

        # Slayt 12
        {
            "slideNumber": 12,
            "title": "Kromozomal Yeniden Düzenlenmeler: Translokasyonlar",
            "content": (
                "Kromozomal translokasyonlar, iki homolog olmayan kromozom segmentinin kırılıp karşılıklı yer "
                "değiştirmesidir. Hematolojik malignitelerin (lösemi ve lenfomalar) ve yumuşak doku sarkomlarının "
                "başlıca patogenetik itici gücüdür. Translokasyonlar iki temel onkojenik mekanizma ile kanseri "
                "başlatır: Birincisi, bir protoonkogenin fizyolojik kontrol bölgesinden koparılarak antikor veya "
                "T hücre reseptörü gibi konstitütif olarak aktif bir **güçlü promotör veya enhancer altına "
                "taşınmasıdır**; bu durum onkoproteinin aşırı miktarda üretilmesine yol açar (Burkitt lenfoma, "
                "foliküler lenfoma). İkincisi ise, iki ayrı genin kırılma noktalarından birleşerek tamamen yeni ve "
                "anormal biyolojik aktiviteye sahip **hibrit (füzyon/kimerik) bir onkoprotein** kodlamasıdır (KML)."
            ),
            "elements": [
                make_before_after(
                    "Translokasyonların İki Temel Onkojenik Mekanizması",
                    "Promotör Altına Taşınma (Aşırı Ekspresyon)",
                    "Onkogenin yapısı değişmez; immünoglobulin promotörü altına girerek normal proteinini aşırı miktarda pompalar (Ör. Burkitt lenfoma).",
                    "Kimerik Füzyon Geni Oluşumu (Yeni Protein)",
                    "İki genin parçaları birleşerek doğada bulunmayan, sürekli aktif yeni bir hibrit kinaz üretir (Ör. KML'de BCR-ABL).",
                    "Füzyon kinazlar hedefe yönelik küçük moleküllü inhibitörlerle (akıllı ilaçlar) doğrudan bloke edilebilir."
                ),
                make_active_recall(
                    "Hematolojik malignitelerde protoonkogenlerin aşırı eksprese olmasına yol açan en yaygın promotör lokusu hangisidir?",
                    "İmmünoglobulin (Ig) ağır veya hafif zincir lokuslarıdır.",
                    "Antikor genlerinin aktif bölgesi"
                )
            ]
        },

        # Slayt 13
        {
            "slideNumber": 13,
            "title": "Güçlü Promotör Altına Taşınma: Burkitt Lenfoma t(8;14)",
            "content": (
                "**Burkitt lenfoma**, B lenfosit kökenli, son derece hızlı çoğalan yüksek dereceli bir "
                "non-Hodgkin lenfomadır. Olguların %90'ından fazlasında **t(8;14)(q24;q32)** resiprokal translokasyonu "
                "saptanır. 8. kromozomda yer alan **MYC protoonkogeni**, 14. kromozomdaki **immünoglobulin ağır zincir "
                "(IgH)** lokusunun hemen yanına transfer edilir. B lenfositlerinde antikor üretimi için IgH promotörü "
                "kesintisiz açık olduğundan, MYC geni kontrolsüz ve aşırı düzeyde transkribe edilir. MYC bir nükleer "
                "transkripsiyon faktörüdür; siklin bağımlı kinazları ve aerobik glikoliz (Warburg etkisi) enzimlerini "
                "tetikleyerek hücreyi sürekli S fazına iter. Mikroskopide proliferasyon fraksiyonu yaklaşık %100'dür "
                "ve apoptoza giden hücreleri yiyen makrofajlar klasik **'gökyüzünde yıldızlar (starry sky)'** "
                "görünümünü oluşturur."
            ),
            "elements": [
                make_causal_chain(
                    "Burkitt Lenfomada t(8;14) Translokasyonel Karsinogenez Zinciri",
                    [
                        "1. Kromozom Kırılması: B hücresinde 8q24 (MYC) ve 14q32 (IgH) bölgelerinde çift iplik DNA kırığı oluşur.",
                        "2. Hatalı Uç Birleşmesi: MYC geni 14. kromozomdaki yüksek aktiviteli IgH regülatuvar elemanlarının altına yerleşir.",
                        "3. Aşırı MYC Sentezi: B lenfositinde kontrol mekanizmalarından azade devasa miktarda MYC proteini üretilir.",
                        "4. Metabolik Patlama: MYC Siklin D ve glutaminaz enzimlerini uyararak glikolizi ve hücre siklusunu fırlatır.",
                        "5. Yıldızlı Gök Manzarası: Çok hızlı bölünen B lenfoblast tabakası içinde apoptotik kalıntıları yutan makrofajlar parlar."
                    ]
                ),
                make_cloze(
                    "Burkitt lenfomada 8. kromozomdan 14. kromozoma transfer edilerek aşırı eksprese edilen nükleer onkogen MYC genidir.",
                    "MYC",
                    "Nükleer transkripsiyon faktörü protoonkogeni"
                )
            ]
        },

        # Slayt 14
        {
            "slideNumber": 14,
            "title": "Apoptoz Blokajı: Foliküler Lenfoma ve t(14;18)",
            "content": (
                "**Foliküler lenfoma**, germinal merkez B hücrelerinden köken alan indolent seyirli bir diğer "
                "lenfomadır. Patogenezinde olguların %85-90'ında saptanan **t(14;18)(q32;q21)** translokasyonu yatar. "
                "Bu lezyonda 18. kromozomdaki antiapoptotik **BCL2 geni**, 14. kromozomdaki immünoglobulin ağır zincir "
                "(IgH) lokusunun güçlü regülasyonu altına taşınır. Bunun sonucunda B lenfositlerinde anormal derecede "
                "yüksek seviyelerde BCL2 proteini üretilir. BCL2 mitokondri dış zarında birikerek BAX ve BAK'ın "
                "oligomerizasyonunu engeller; mitokondri membran geçirgenliği bloke olur ve Sitokrom c salınamaz. "
                "Bu hücreler kontrolsüz çoğalmaktan ziyade, normalde apoptozla elenmesi gereken B hücrelerinin "
                "**ölümsüzleşmesi ve birikmesi** sayesinde tümör kitlesi meydana getirirler."
            ),
            "elements": [
                make_table(
                    "Burkitt Lenfoma ile Foliküler Lenfoma Karşılaştırması",
                    ["Parametre", "Burkitt Lenfoma", "Foliküler Lenfoma"],
                    [
                        {
                            "cells": ["Karakteristik Translokasyon", "t(8;14)(q24;q32)", "t(14;18)(q32;q21)"],
                            "hiddenIndex": 2,
                            "hint": "18. kromozom ile IgH yer değiştirmesi"
                        },
                        {
                            "cells": ["Translokasyona Uğrayan Gen", "MYC onkogeni", "BCL2 antiapoptotik geni"],
                            "hiddenIndex": 2,
                            "hint": "Mitokondriyal koruyucu protein"
                        },
                        {
                            "cells": ["Temel Kanser Mekanizması", "Patlayıcı proliferasyon ve bölünme", "Apoptozun önlenmesi ve hücre birikimi"],
                            "hiddenIndex": 2,
                            "hint": "Programlı ölümün durdurulması"
                        }
                    ]
                ),
                make_active_recall(
                    "Foliküler lenfomada t(14;18) translokasyonunun tümör oluşturmadaki temel hücresel mekanizması nedir?",
                    "Antiapoptotik BCL2 aşırı üretimi sayesinde mitokondriyal apoptozun engellenmesi ve hücrelerin ölümsüzleşmesidir.",
                    "Mitokondri zar stabilizasyonu ile sağkalım"
                )
            ]
        },

        # Slayt 15
        {
            "slideNumber": 15,
            "title": "Kimerik Füzyon Geni: KML ve Philadelphia Kromozomu",
            "content": (
                "Translokasyonların ikinci majör sınıfı, iki ayrı gen parçasının birleşerek hibrit bir onkoprotein "
                "oluşturmasıdır. Bunun tıptaki en parlak örneği **Kronik Miyeloid Lösemi'de (KML)** görülen "
                "**Philadelphia kromozomudur [t(9;22)(q34;q11)]**. 9. kromozomdaki **ABL1** tirozin kinaz geni, "
                "22. kromozomdaki **BCR (Breakpoint Cluster Region)** geni ile resiprokal yer değiştirir. Ortaya "
                "çıkan türev 22. kromozoma 'Philadelphia kromozomu' denir. Bu yeniden düzenleme sonucunda **BCR-ABL "
                "füzyon geni** ve buna bağlı **p210 BCR-ABL kimerik proteini** sentezlenir. Normal ABL sitoplazmik "
                "ve nükleer bir kinaz olup sıkı regülasyon altındadır; ancak BCR parçasının eklenmesi ABL'nin kendi "
                "kendini inhibe etme yeteneğini yok eder ve kinaz konstitütif (kesintisiz) otonom aktif hale gelir."
            ),
            "elements": [
                make_cloze(
                    "Kronik miyeloid lösemiye yol açan 9 ve 22. kromozomlar arası resiprokal translokasyon ürünü Philadelphia kromozomudur.",
                    "Philadelphia",
                    "Tarihi kentin adını taşıyan sitogenetik belirteç"
                ),
                make_causal_chain(
                    "KML'de Philadelphia Kromozomu ve BCR-ABL Füzyon Kaskadı",
                    [
                        "1. Resiprokal Kırılma: 9q34 (ABL1) ve 22q11 (BCR) lokuslarında DNA çift iplik kırıkları gerçekleşir.",
                        "2. Türev Kromozom Oluşumu: ABL kinaz bölgesi BCR geni ile birleşerek küçük Philadelphia (22q-) kromozomunu üretir.",
                        "3. Kimerik Transkripsiyon: Füzyon lokusundan hibrit BCR-ABL mRNA'sı transkribe edilir.",
                        "4. Otonom Kinaz Aktivasyonu: p210 onkoproteini otoligasyonla kontrolsüz tirozin kinaz aktivitesi kazanır.",
                        "5. Miyeloid Patlama: STAT5, AKT ve RAS yolları sürekli uyarılır; kemik iliğinde granülositik seri kontrolsüz taşar."
                    ]
                )
            ]
        },

        # Slayt 16
        {
            "slideNumber": 16,
            "title": "BCR-ABL Onkoproteini ve Hedefe Yönelik Tedavi",
            "content": (
                "BCR-ABL füzyon onkoproteini, modern hedefe yönelik moleküler tedavinin (akıllı ilaç çağı) doğuş "
                "noktasıdır. BCR-ABL'nin konstitütif tirozin kinaz aktivitesi hücreye sürekli 'çoğal' ve 'apoptoza "
                "gitme' sinyali gönderir. Bu biyolojik açığı hedefleyen **İmatinib (Gleevec)**, BCR-ABL kinaz "
                "enziminin ATP bağlama cebine rekabetçi şekilde oturarak fosfat transferini bloke eden küçük bir "
                "sentetik moleküldür. İmatinib sayesinde normal hücrelere zarar vermeksizin KML klonu seçici olarak "
                "apoptoza sürüklenir. Bu tedavi ile ölümcül olan KML, günde tek bir tabletle on yıllarca tam hematolojik "
                "ve moleküler remisyonda tutulabilen kronik yönetilebilir bir hastalığa dönüşmüştür. Ancak ilacın "
                "uzun süreli kullanımında ATP cebinde gelişen ikincil nokta mutasyonları (özellikle **T315I**) "
                "ilaç direncine yol açabilir ve yeni nesil tirozin kinaz inhibitörlerini (dasatinib, ponatinib) gerektirir."
            ),
            "elements": [
                make_before_after(
                    "KML Tedavisinde Kemoterapi vs Hedefe Yönelik İmatinib Devrimi",
                    "Geleneksel Sitotoksik Tedavi (Geçmiş)",
                    "İnterferon ve hidroksiüre; tüm kemik iliğini baskılar, ağır toksisite yapar, blastik krizi ve ölümü engelleyemez.",
                    "Hedefe Yönelik İmatinib (Tirozin Kinaz İnhibitörü)",
                    "Sadece mutant BCR-ABL'nin ATP cebini tıkar; normal hücrelere dokunmaz, blastik krizi önler ve yaşam süresini normale yaklaştırır.",
                    "Kanser tedavisinde moleküler hedefe yönelik onkolojinin prototipik ve en başarılı örneğidir."
                ),
                make_active_recall(
                    "Kronik miyeloid lösemide BCR-ABL kinazının ATP bağlanma cebini yarışmalı inhibe ederek devrim yaratan ilk hedefe yönelik tirozin kinaz inhibitörü nedir?",
                    "İmatinib (veya STI-571) etken maddesidir.",
                    "Lösemi akıllı ilaç öncüsü"
                )
            ]
        },

        # Slayt 17
        {
            "slideNumber": 17,
            "title": "Akut Promiyelositik Lösemi (APL) ve t(15;17)",
            "content": (
                "Akut miyeloid löseminin özel bir alt tipi olan **Akut Promiyelositik Lösemide (AML M3 / APL)** "
                "patognomonik lezyon **t(15;17)(q22;q21)** translokasyonudur. Bu mutasyonla 15. kromozomdaki **PML "
                "geni** ile 17. kromozomdaki **Retinoik Asit Reseptör Alfa (RARA)** geni birleşerek **PML-RARA füzyon "
                "proteinini** oluşturur. Normal RARA proteini fizyolojik dozda retinoik asit bağladığında miyeloid "
                "öncüllerin granülosite matürasyonunu sağlar. Ancak PML-RARA kimerik proteini fizyolojik retinoik "
                "asit seviyelerinde kromatini baskı altında tutarak hücrelerin promiyelosit evresinde takılıp kalmasına "
                "(matürasyon arresti) neden olur. Promiyelositlerin sitoplazmasındaki yoğun prokoagülan granüller "
                "kana döküldüğünde ölümcül Dissemine İntravasküler Koagülasyon (DİK) tetiklenir. Farmakolojik yüksek "
                "doz **Tüm-Trans Retinoik Asit (ATRA)** verildiğinde PML-RARA kompleksi çözülür ve hücreler matür "
                "nötrofillere diferansiye olarak lösemi iyileşir."
            ),
            "elements": [
                make_table(
                    "APL ve t(15;17) Patofizyolojik Özellikleri",
                    ["Bileşen / Parametre", "Patolojik Bulgu", "Klinik Yansıması"],
                    [
                        {
                            "cells": ["Kromozomal Lezyon", "t(15;17)(q22;q21) translokasyonu", "PML-RARA füzyon gen oluşumu"],
                            "hiddenIndex": 1,
                            "hint": "Kromozom on beş ve on yedi yer değişimi"
                        },
                        {
                            "cells": ["Hücresel Duraklama", "Promiyelosit evresinde matürasyon arresti", "Kemik iliğinde bol Auer çubuklu hücreler"],
                            "hiddenIndex": 1,
                            "hint": "Granülositik gelişim tıkanması"
                        },
                        {
                            "cells": ["Hedefe Yönelik Tedavi", "ATRA (Tüm-trans retinoik asit)", "Diferansiasyon indüksiyonu ile kür"],
                            "hiddenIndex": 1,
                            "hint": "A vitamini türevi diferansiyasyon ajanı"
                        }
                    ]
                ),
                make_cloze(
                    "PML-RARA füzyon proteini taşıyan APL hastalarında promiyelositlerin nötrofillere olgunlaşmasını tetikleyerek kür sağlayan ajan ATRA molekülüdür.",
                    "ATRA",
                    "Tüm trans retinoik asit kısaltması"
                )
            ]
        },

        # Slayt 18
        {
            "slideNumber": 18,
            "title": "Sarkomlarda Translokasyonlar: Ewing ve Diğerleri",
            "content": (
                "Translokasyonlar yalnızca hematolojik neoplazmlara özgü olmayıp mezenkimal kaynaklı pek çok sarkomda "
                "da patognomonik tanısal belirteçlerdir. Çocuk ve genç erişkinlerin kemik ve yumuşak doku tümörü olan "
                "**Ewing Sarkomunda**, vakaların %95'inde **t(11;22)(q24;q12)** translokasyonu izlenir. Bu lezyon "
                "22. kromozomdaki **EWSR1 geni** ile 11. kromozomdaki **FLI1 transkripsiyon faktörünü** birleştirerek "
                "güçlü bir kimerik onkoprotein (EWS-FLI1) oluşturur. Histopatolojide küçük yuvarlak mavi hücreli "
                "tümör tablosu görülür ve PAS pozitif glikojen içerir. Benzer biçimde **Sinovyal Sarkomda "
                "t(X;18)(p11;q11) SS18-SSX füzyonu**, **Miksosarkomda (Mikzoid Liposarkom) t(12;16) FUS-DDIT3 füzyonu** "
                "ve **Dermatofibrosarkoma Protuberans'ta t(17;22) COL1A1-PDGFB füzyonu** spesifik patolojik imzalardır."
            ),
            "elements": [
                make_table(
                    "Sarkomlarda Karakteristik Translokasyonlar",
                    ["Sarkom Tipi", "Karakteristik Translokasyon", "Oluşan Füzyon Geni", "Histopatolojik İpucu"],
                    [
                        {
                            "cells": ["Ewing Sarkomu", "t(11;22)(q24;q12)", "EWSR1-FLI1 füzyonu", "Küçük yuvarlak mavi hücreler"],
                            "hiddenIndex": 2,
                            "hint": "EWS ve FLI transkripsiyon kimerası"
                        },
                        {
                            "cells": ["Sinovyal Sarkom", "t(X;18)(p11;q11)", "SS18-SSX füzyonu", "Bifazik epitel/iğsi hücre paterni"],
                            "hiddenIndex": 2,
                            "hint": "X ve 18 kromozom füzyon proteini"
                        },
                        {
                            "cells": ["Mikzoid Liposarkom", "t(12;16)(q13;p11)", "FUS-DDIT3 füzyonu", "Tavuk ayağı kapiller damar ağı"],
                            "hiddenIndex": 2,
                            "hint": "Liposarkom mikzoid alt tipi hibriti"
                        }
                    ]
                ),
                make_active_recall(
                    "Küçük yuvarlak mavi hücreli kemik tümörü olan Ewing sarkomunun patogenezinde rol oynayan karakteristik translokasyon hangisidir?",
                    "t(11;22)(q24;q12) translokasyonudur (EWSR1-FLI1).",
                    "11 ve 22 kromozom transferi"
                )
            ]
        },

        # Slayt 19: CHECKPOINT 2
        {
            "slideNumber": 19,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Nokta Mutasyonları ve Kromozomal Translokasyonlar",
            "content": (
                "İkinci bölümün bu tekrar sayfasında, karsinogenezde kilit rol oynayan nokta mutasyonları ve "
                "kromozomal translokasyon mekanizmaları özetlenmektedir. Nokta mutasyonları solid tümörlerde "
                "en sık lezyondur; KRAS'ta işlev kazanımı, TP53'te işlev kaybı yapar. Translokasyonlar iki ana "
                "yolla etki gösterir: Onkogeni güçlü IgH promotörü altına taşıyıp aşırı eksprese ettirenler "
                "(Burkitt lenfomada t(8;14) MYC ve foliküler lenfomada t(14;18) BCL2) ile yeni kimerik protein "
                "üretenler (KML'de t(9;22) BCR-ABL Philadelphia ve APL'de t(15;17) PML-RARA). İmatinib BCR-ABL "
                "kinazını bloke ederek hedefe yönelik tedavinin prototipini oluştururken, ATRA PML-RARA'yı "
                "çözerek diferansiyasyonu uyarır. Ewing sarkomunda t(11;22) EWSR1-FLI1 mezenkimal translokasyonun "
                "klasik örneğidir."
            ),
            "flashcards": [
                {
                    "id": "k1-29-cp02-fc01",
                    "front": "Burkitt lenfomada t(8;14) translokasyonu sonucu immünoglobulin ağır zincir promotörü altına taşınarak aşırı üretilen onkogen hangisidir?",
                    "back": "MYC protoonkogenidir.",
                    "hint": "Bölünmeyi tetikleyen nükleer transkripsiyon faktörü"
                },
                {
                    "id": "k1-29-cp02-fc02",
                    "front": "Kronik miyeloid lösemide t(9;22) sonucu ortaya çıkan Philadelphia kromozomunun kodladığı kimerik protein nedir?",
                    "back": "BCR-ABL füzyon onkoproteinidir (p210).",
                    "hint": "Otonom aktif tirozin kinaz kompleksi"
                },
                {
                    "id": "k1-29-cp02-fc03",
                    "front": "Akut promiyelositik lösemide (APL) t(15;17) translokasyonuyla oluşan ve ATRA tedavisine yanıt veren kimerik gen hangisidir?",
                    "back": "PML-RARA füzyon genidir.",
                    "hint": "Retinoik asit reseptörü içeren hibrit yapı"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 2 Özet Tablosu: Majör Translokasyonlar",
                    ["Hastalık", "Translokasyon", "İlgili Genler / Füzyon"],
                    [
                        {
                            "cells": ["Burkitt Lenfoma", "t(8;14)", "MYC aşırı ekspresyonu (IgH regülasyonu)"],
                            "hiddenIndex": 2,
                            "hint": "MYC transkripsiyon faktörü aktivasyonu"
                        },
                        {
                            "cells": ["Foliküler Lenfoma", "t(14;18)", "BCL2 antiapoptotik aşırı ekspresyonu"],
                            "hiddenIndex": 2,
                            "hint": "Programlı hücre ölümünün kilitlenmesi"
                        }
                    ]
                )
            ]
        },

        # Slayt 20
        {
            "slideNumber": 20,
            "title": "Klinik Karar: Lösemi ve Lenfomalarda Moleküler Translokasyon Panelleri",
            "content": (
                "Hematolojik malignitelerin doğru sınıflandırılması, prognoz tayini ve hedefe yönelik ilaç "
                "seçimi mutlak surette sitogenetik ve moleküler testlere (FISH, RT-PCR, Karyotipleme) dayanır. "
                "Lökositoz ve splenomegali ile başvuran bir hastada kemik iliğinde Philadelphia kromozomu veya "
                "BCR-ABL transkripti saptanması KML tanısını kesinleştirir ve derhal birinci kuşak TKI (imatinib) "
                "başlanmasını gerektirir. Akut lösemi tablosunda ise t(15;17) PML-RARA saptanması, hastayı ölümcül "
                "DİK tablosundan kurtaracak olan ATRA tedavisinin gecikmeksizin verilmesi için acil bir hematopatolojik "
                "alarm işaretidir. Benzer şekilde lenf nodu biyopsisinde blastik hücrelerin t(8;14) MYC mi yoksa "
                "t(14;18) BCL2 mi taşıdığı, agresif kemoterapi mi yoksa indolent izlem mi yapılacağını belirler."
            ),
            "elements": [
                make_branching_logic(
                    "24 yaşında erkek hasta diş eti kanaması, peteşiler ve halsizlik ile acile başvuruyor. Hemogramda pansitopeni, periferik yaymada yoğun granüllü, multipl Auer çubukları içeren atipik promiyelositler saptanıyor. Koagülasyon testlerinde D-Dimer yüksek, fibrinojen ileri derecede düşük bulunuyor (DİK tablosu).",
                    "Bu hastada kesin tanı ve acil hedefe yönelik tedavi için yapılması gereken en kritik moleküler girişim hangisidir?",
                    [
                        {
                            "text": "Acil FISH veya RT-PCR ile t(15;17) PML-RARA füzyonu taranmalı ve sonuç beklenirken dahi DİK'i durdurmak için ATRA tedavisine başlanmalıdır.",
                            "isCorrect": True,
                            "explanation": "Auer çubukları ve DİK birlikteliği APL için patognomoniktir. t(15;17) doğrulaması ve erken ATRA hayat kurtarıcıdır."
                        },
                        {
                            "text": "Hastada KML blastik krizi düşünülerek derhal yüksek doz imatinib infüzyonu başlanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Auer çubuklu promiyelositler ve DİK APL özelliğidir, KML değildir."
                        },
                        {
                            "text": "Moleküler teste gerek yoktur; hastaya sadece trombosit süspansiyonu verilerek taburcu edilmelidir.",
                            "isCorrect": False,
                            "explanation": "APL tedavi edilmezse saatler içinde intrakraniyal kanama ile ölümcül seyreder."
                        }
                    ]
                ),
                make_micro_quiz(
                    "Sitogenetik incelemede t(9;22) Philadelphia kromozomu saptanan bir hastada uygulanacak en uygun hedefe yönelik birinci basamak farmakolojik ajan hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "İmatinib (Tirozin kinaz inhibitörü)",
                            "isCorrect": True,
                            "explanation": "İmatinib BCR-ABL kinaz cebini yarışmalı bloke eden birinci basamak spesifik akıllı ilaçtır."
                        },
                        {
                            "key": "B",
                            "text": "Tüm-trans retinoik asit (ATRA)",
                            "isCorrect": False,
                            "explanation": "ATRA t(15;17) PML-RARA taşıyan APL'de kullanılır."
                        },
                        {
                            "key": "C",
                            "text": "Anti-HER2 monoklonal antikoru (Trastuzumab)",
                            "isCorrect": False,
                            "explanation": "Trastuzumab HER2 amplifiye meme ve mide karsinomlarında kullanılır."
                        },
                        {
                            "key": "D",
                            "text": "PARP inhibitörü (Olaparib)",
                            "isCorrect": False,
                            "explanation": "PARP inhibitörleri BRCA mutant homolog rekombinasyon kusurlu kanserlerde kullanılır."
                        }
                    ],
                    "Philadelphia kromozomlu BCR-ABL lösemilerin ilacı imatinibdir."
                )
            ]
        }
    ]
