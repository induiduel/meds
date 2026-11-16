# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 30: İleri Tümör Genetiği ve Metabolizması
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 3: TP53: Genomun Koruyucusu ve Hücresel Karar Mekanizmaları (Slayt 21 - 30)
Checkpoint: Slayt 29
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_3_slides():
    return [
        # Slayt 21
        {
            "slideNumber": 21,
            "title": "TP53: Genomun Koruyucusu (Guardian of the Genome)",
            "content": (
                "Kromozom 17p13.1 lokusunda kodlanan TP53 geni, insan kanserlerinde açık ara en sık mutasyona "
                "uğrayan ve biyolojik önemi nedeniyle 'genomun koruyucusu' unvanını alan ana tümör baskılayıcı "
                "transkripsiyon faktörüdür. İnsan malign tümörlerinin yarısından fazlasında doğrudan TP53 geninde "
                "bialelik inaktivasyon saptanırken, geri kalan tümörlerin büyük çoğunluğunda p53'ün aktivasyon "
                "veya regülasyon yolları felç edilmiştir. p53'ün ana biyolojik misyonu, hücresel stres sinyallerini "
                "(DNA kırıkları, hipoksi, onkojenik sinyal taşması, telomer aşınması) algılayarak hücreyi ya geçici "
                "olarak durdurup onarmak ya da geri dönüşsüz ölüme (senesens veya apoptoz) yönlendirmektir."
            ),
            "elements": [
                make_table(
                    "TP53 Geninin Temel Genetik ve Biyolojik Çerçevesi",
                    ["Parametre", "Moleküler Özellik", "Biyolojik Fonksiyon"],
                    [
                        {
                            "cells": ["Kromozomal Lokus", "Kromozom 17p13.1 bandı", "Monozomi 17 veya delesyon 17p ile kayıp"],
                            "hiddenIndex": 1,
                            "hint": "On yedinci kromozomun kısa kolu lokasyonu"
                        },
                        {
                            "cells": ["Protein Yapısı", "Homotetramerik transkripsiyon faktörü", "Spesifik DNA yanıt elementlerine bağlanma"],
                            "hiddenIndex": 1,
                            "hint": "Dört özdeş polipeptit zincirinden oluşan kompleks"
                        },
                        {
                            "cells": ["Mutasyon Sıklığı", "Tüm insan kanserlerinin %50'sinden fazlası", "Malignitelerde en yaygın somatik sapma"],
                            "hiddenIndex": 1,
                            "hint": "Yarıdan fazla oranda gözlenme sıklığı"
                        }
                    ]
                )
            ]
        },

        # Slayt 22
        {
            "slideNumber": 22,
            "title": "MDM2 ve p53'ün Fizyolojik Dinamiği",
            "content": (
                "Sağlıklı ve dinlenme halindeki bir hücrede p53 proteininin varlığı toksik olabileceğinden "
                "düzeyi son derece düşük tutulur; p53'ün bazal yarı ömrü yalnızca 20 dakikadır. Bu sıkı "
                "denetimi sağlayan molekül **MDM2** adlı E3 ubiquitin ligaz enzimidir. MDM2 p53'ün transaktivasyon "
                "alanına bağlanır; hem p53'ün transkripsiyon yapmasını engeller hem de ona ubiquitin zincirleri "
                "ekleyerek 26S proteazomda sessizce parçalatır. p53 ise transkripsiyonel olarak MDM2 genini uyarır; "
                "böylece kusursuz bir otoregülatuvar negatif geri bildirim ilmeği kurulmuş olur."
            ),
            "elements": [
                make_cloze(
                    "Normal hücrelerde p53 proteinini ubikitinleyip proteazomda yıkan temel negatif regülatör MDM2 ligazıdır.",
                    "MDM2",
                    "p53'ün fizyolojik yarı ömrünü kısıtlayan ubiquitin enzimi"
                ),
                make_active_recall(
                    "Fizyolojik şartlarda dinlenme halindeki hücrelerde p53'ün yarı ömrünün 20 dakika gibi kısa bir sürede tutulmasının moleküler mekanizması nedir?",
                    "MDM2 ubiquitin ligazı tarafından sürekli ubikitinlenip 26S proteazomda parçalanmasıdır.",
                    "Hücrenin çöp öğütücü organelinde sindirilme mekanizması"
                )
            ]
        },

        # Slayt 23
        {
            "slideNumber": 23,
            "title": "Stres Sensörleri: ATM ve ATR Kinazları",
            "content": (
                "Hücre iyonize radyasyon, kemoterapötik ilaçlar veya serbest radikallerle karşılaştığında DNA "
                "hasar yanıtı (DDR) mekanizması devreye girer. Çift zincir kırıkları nükleer **ATM (Ataxia "
                "Telangiectasia Mutated)** kinazı tarafından; tek zincir kırıkları ve duraklamış replikasyon "
                "çatalları ise **ATR (ATM and Rad3-related)** kinazı tarafından algılanır. Bu apikal sensör kinazlar "
                "aracı kontrol kinazları olan Chk2 ve Chk1'i fosforilleyerek aktive eder. Aktif kinazlar p53'ün "
                "MDM2 bağlanma bölgesindeki serin aminoasitlerini hızla fosforiller."
            ),
            "elements": [
                make_causal_chain(
                    "DNA Hasarından p53 Kararlılığına Giden Moleküler Yolak",
                    [
                        "1. Lezyon Algısı: İyonize radyasyon DNA çift zincir kırığı yaratır ve ATM kinazı aktifleşir.",
                        "2. Sinyal İletimi: ATM kinazı doğrudan Chk2 kinazını fosforilleyerek aktive eder.",
                        "3. Konformasyonel Koruma: ATM ve Chk2 p53'ün amino-ucundaki serin kalıntılarını fosforiller.",
                        "4. MDM2 Ayrılması: Fosforillenen p53, MDM2 ubiquitin ligazına bağlanamaz ve yıkımdan kurtulur.",
                        "5. Nükleer Birikim: Kararlı hale gelen p53 tetramerleşerek DNA promotorlarına kenetlenir."
                    ]
                )
            ]
        },

        # Slayt 24
        {
            "slideNumber": 24,
            "title": "Hücresel Yanıt 1: Geçici G1 Fazı Durması (p21 İndüksiyonu)",
            "content": (
                "Kararlı hale gelen p53 nükleusta spesifik DNA dizilerine bağlanarak ilk savunma hattını kurar: "
                "geçici hücre döngüsü duraklaması (quiescence). p53 doğrudan **CDKN1A** genini transkribe ederek "
                "**p21** proteinini sentezletir. p21, Siklin D-CDK4 ve Siklin E-CDK2 komplekslerini güçlü şekilde "
                "bloke eder. Bu blokaj RB proteininin fosforillenmesini önler; RB hipofosforile kalarak E2F'yi "
                "hapseder ve hücre G1 evresinde kilitlenir. Hücre döngüsünün bu duraklaması DNA polimerazın "
                "hasarlı şablonu kopyalamasını engeller ve tamir enzimleri için değerli zaman kazandırır."
            ),
            "elements": [
                make_cloze(
                    "p53 tarafından indüklenen p21 proteini CDK komplekslerini inhibe ederek RB fosforilasyonunu önler ve G1 durması sağlar.",
                    "p21",
                    "CDKN1A geninin kodladığı yirmi bir kilodaltonluk inhibitör"
                ),
                make_active_recall(
                    "p53'ün hücreyi G1/S sınırında geçici olarak durdurmak için transkripsiyonunu doğrudan indüklediği temel CDK inhibitörü hangisidir?",
                    "p21 (CDKN1A geni ürünü) proteinidir.",
                    "Siklin E CDK2 kompleksinin geniş spektrumlu inhibitörü"
                )
            ]
        },

        # Slayt 25
        {
            "slideNumber": 25,
            "title": "Hücresel Yanıt 2: DNA Onarımı ve Döngüye Dönüş",
            "content": (
                "p53 yalnızca duraklama sağlamaz; aynı zamanda hasarlı genomu onaracak moleküler personeli de "
                "göreve çağırır. p53 doğrudan **GADD45 (Growth Arrest and DNA Damage)** genini ve nükleotid kesip "
                "çıkarma onarım proteinlerini kodlayan genleri transkribe eder. Eğer DNA hasarı başarıyla onarılırsa "
                "ATM/ATR sinyali kesilir. Bu aşamada p53'ün daha önceden uyardığı MDM2 proteinleri nükleusta "
                "birikmiştir; onarılmış p53'e bağlanarak onu hızla yıkar. p53 düzeyi normale döner, p21 freni "
                "kalkar, RB fosforillenir ve hücre sağlıklı şekilde bölünmesine devam eder."
            ),
            "elements": [
                make_before_after(
                    "Başarılı Onarım vs Başarısız Onarımda p53'ün Hücresel Kader Kararı",
                    "DNA Hasarı Başarıyla Onarıldığında",
                    "GADD45 ve onarım enzimleri hasarı düzeltir; p53 tarafından üretilen MDM2 p53'ü yıkar, döngü kaldığı yerden devam eder.",
                    "DNA Hasarı Onarılamaz Boyutta Olduğunda",
                    "Yüksek p53 düzeyi sebat eder; hücre ya kalıcı büyüme durması olan senesense girer ya da apoptoz programı ateşlenir.",
                    "p53'ün bu iki yönlü moleküler şalteri, genomik mutasyonların yavru hücrelere aktarılmasını önleyen en temel kalkandır."
                )
            ]
        },

        # Slayt 26
        {
            "slideNumber": 26,
            "title": "Hücresel Yanıt 3: Senesens (Kalıcı Hücre Döngüsü Durması)",
            "content": (
                "Eğer DNA hasarı onarılamayacak düzeydeyse ancak apoptoz eşiğine de ulaşmamışsa, p53 hücreyi "
                "**senesens (hücresel yaşlanma)** durumuna sokar. Senesens, hücrenin metabolik olarak canlı ve "
                "aktif kalmasına karşın mitojenik uyarılara karşı kalıcı ve geri dönüşümsüz olarak bölünme "
                "yeteneğini yitirmesidir. Bu süreçte heterokromatin adacıkları oluşur ve hücre döngüsü genleri "
                "epigenetik olarak kilitlenir. Senesent hücreler senesensle ilişkili sekretuvar fenotip (SASP) "
                "kazanarak sitokinler salgılar ve bağışıklık hücreleri tarafından çevre dokudan temizlenir."
            ),
            "elements": [
                make_cloze(
                    "Hücrenin metabolik olarak canlı kalıp bölünme yeteneğini geri dönüşümsüz kaybetmesine senesens adı verilir.",
                    "senesens",
                    "Kalıcı hücresel yaşlanma ve büyüme durması durumu"
                ),
                make_active_recall(
                    "Senesense giren bir hücrenin metabolik durumu ve bölünme yeteneği nasıldır?",
                    "Hücre metabolik olarak aktiftir ancak büyüme uyarısı olsa dahi geri dönüşümsüz olarak bölünemez.",
                    "Canlılığını korurken replikasyon kapasitesini ebediyen kaybetme hali"
                )
            ]
        },

        # Slayt 27
        {
            "slideNumber": 27,
            "title": "Hücresel Yanıt 4: p53 Aracılı İntrensek Apoptoz",
            "content": (
                "DNA hasarı şiddetli, çift zincir kırıkları yaygın veya onkojenik sinyal patlaması aşırı olduğunda "
                "p53 hücrenin intihar etmesine karar verir. p53 doğrudan pro-apoptotik BCL-2 ailesi üyeleri olan "
                "**BAX**, **PUMA** ve **NOXA** genlerinin transkripsiyonunu indüklerken; anti-apoptotik BCL-2 ve "
                "BCL-XL'i baskılar. PUMA ve NOXA, mitokondri dış zarındaki BAX ve BAK'ı doğrudan aktive eder. "
                "Oluşan dev gözeneklerden sitokrom c sitoplazmaya fışkırır, APAF-1 ile birleşerek apoptazomu "
                "kurar ve kaspaz-9/kaspaz-3 kaskadı ile hücre sessizce fagosite edilir."
            ),
            "elements": [
                make_causal_chain(
                    "p53 Aracılı Mitokondriyal Apoptoz Kaskadı",
                    [
                        "1. Şiddetli Hasar: Ağır DNA hasarı sonucu p53 düzeyi nükleusta eşik değeri aşar.",
                        "2. Gen İndüksiyonu: p53 doğrudan BAX, PUMA ve NOXA pro-apoptotik genlerini transkribe eder.",
                        "3. Gözenek Açılımı: BAX ve BAK mitokondri dış zarında oligomerleşerek MOMP kanallarını açar.",
                        "4. Sitokrom c Salınımı: İntermembran aralıktan sitoplazmaya sızan sitokrom c Apaf-1 ile birleşir.",
                        "5. Kaspaz Aktivasyonu: Apoptazom kaspaz-9'u ve ardından kaspaz-3'ü keserek hücreyi parçalar."
                    ]
                )
            ]
        },

        # Slayt 28
        {
            "slideNumber": 28,
            "title": "p53'ün Onkojenik Sinyal Algısı: p14/ARF Köprüsü",
            "content": (
                "p53 yalnızca DNA kırıklarına değil, aşırı onkojenik uyarılara karşı da koruma sağlar. Normal "
                "bir hücrede kontrolsüz RAS, MYC veya E2F aktivasyonu gerçekleştiğinde, CDKN2A lokusundan "
                "kodlanan **p14/ARF** proteini uyarılır. p14/ARF doğrudan MDM2'ye bağlanarak onu nükleolusta "
                "hapseder ve p53'ü serbest bırakır. Bu durum 'onkojen kaynaklı senesens veya apoptoz' olarak "
                "adlandırılır. Bir hücre onkogen kazandığında şayet p53'ü sağlamsa hemen intihar eder; kanser "
                "gelişebilmesi için hem onkogen aktivasyonu hem de p53/ARF kalkanının kırılması şarttır."
            ),
            "elements": [
                make_cloze(
                    "Onkojenik sinyal taşmasında MDM2'yi bağlayarak p53'ü aktive eden CDKN2A ürünü p14/ARF proteinidir.",
                    "p14/ARF",
                    "Alternatif okuma çerçevesinden kodlanan MDM2 inhibitörü"
                ),
                make_micro_quiz(
                    "Aşırı MYC veya RAS onkogenik aktivitesi varlığında normal bir hücrenin p53 aracılı apoptoza girmesini sağlayan aracı molekül hangisidir?",
                    [
                        {
                            "text": "p14/ARF proteini (MDM2'yi sekestre ederek p53'ü stabilize eder)",
                            "isCorrect": True,
                            "explanation": "p14/ARF onkojenik stresi algılar, MDM2'yi inhibe eder ve p53'ün hızla birikmesini sağlar."
                        },
                        {
                            "text": "Siklin D1 proteini (CDK4 ile birleşerek p53'ü fosforiller)",
                            "isCorrect": False,
                            "explanation": "Siklin D1 RB'yi fosforiller, p53 aktivatörü değildir."
                        },
                        {
                            "text": "Trombospondin-1 (anjiyogenezi durdurarak p53'ü uyarır)",
                            "isCorrect": False,
                            "explanation": "Trombospondin-1 p53'ün downstream hedefidir, upstream sensörü değildir."
                        },
                        {
                            "text": "Telomeraz enzimi (telomerleri uzatarak p53'ü tetikler)",
                            "isCorrect": False,
                            "explanation": "Telomeraz krizden kaçışı sağlar, apoptozu tetiklemez."
                        }
                    ],
                    "p14/ARF onkogen aktivasyonunu doğrudan p53 savunmasına bağlayan kritik köprüdür."
                )
            ]
        },

        # Slayt 29: CHECKPOINT 3
        {
            "slideNumber": 29,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 3] TP53 ve Genomik İstikrar Mekanizmaları",
            "content": (
                "Bu kontrol noktasında TP53 geninin regülasyonunu ve hücre kaderini belirleyen üç temel işlevini "
                "özetliyoruz:\n\n"
                "• **Lokus ve Yapı:** Kromozom 17p13.1'de kodlanan homotetramerik transkripsiyon faktörüdür.\n"
                "• **Fizyolojik Fren:** Dinlenmede MDM2 ubiquitin ligazı p53'ü proteazomda yıkar (yarı ömür ~20 dk).\n"
                "• **Aktivasyon:** DNA çift zincir kırıkları ATM-Chk2 yolağıyla p53'ü fosforiller; p53 MDM2'den ayrılıp birikir.\n"
                "• **Geçici G1 Durması:** p21 (CDKN1A) transkripsiyonu CDK'ları bloke eder, RB hipofosforile kalır.\n"
                "• **Onarım ve Yaşlanma:** GADD45 DNA onarımını sağlar; onarılamayan hasarda senesens tetiklenir.\n"
                "• **Apoptoz:** PUMA, NOXA ve BAX indüklenerek mitokondriyal sitokrom c salınımı ve kaspaz aktivasyonu yapılır.\n"
                "• **Onkogenik Stres:** p14/ARF MDM2'yi hapsederek p53'ü korur ve onkogen taşıyan hücreyi öldürür."
            ),
            "flashcards": [
                {
                    "id": "k1-30-fc07",
                    "front": "DNA çift zincir kırıklarını algılayarak Chk2 üzerinden p53'ü fosforilleyip MDM2 yıkımından kurtaran apikal kinaz hangisidir?",
                    "back": "ATM (Ataxia Telangiectasia Mutated) kinazıdır.",
                    "hint": "Ataksi telenjiektazi hastalığında mutant olan apikal DNA sensörü"
                },
                {
                    "id": "k1-30-fc08",
                    "front": "p53'ün hücreyi G1/S sınırında geçici olarak durdurmak amacıyla transkripsiyonunu doğrudan başlattığı CDK inhibitörü gen hangisidir?",
                    "back": "CDKN1A (p21) genidir.",
                    "hint": "Yirmi bir kilodaltonluk klasik siklin kinaz inhibitör proteini"
                },
                {
                    "id": "k1-30-fc09",
                    "front": "p53'ün şiddetli DNA hasarında mitokondri dış zarında gözenek açarak apoptozu başlatmak için uyardığı temel BH3-only pro-apoptotik proteinler hangileridir?",
                    "back": "PUMA ve NOXA proteinleridir.",
                    "hint": "Mitokondriyal intrensek ölüm yolağını ateşleyen iki kritik protein"
                }
            ],
            "elements": [
                make_active_recall(
                    "p53'ün hücre kaderini belirlemede kullandığı üç ana hücresel sonuç nedir?",
                    "Geçici hücre döngüsü durması (G1 arresti), kalıcı yaşlanma (senesens) ve programlı hücre ölümüdür (apoptoz).",
                    "Hücrenin durması, yaşlanması veya intihar etmesi üçlüsü"
                )
            ]
        },

        # Slayt 30
        {
            "slideNumber": 30,
            "title": "p53 Kaybının Moleküler Sonuçları ve Kanserleşme",
            "content": (
                "p53 geni inaktive olduğunda veya silindiğinde genomik polis devre dışı kalır. DNA hasarına "
                "uğrayan hücre artık G1 evresinde durdurulamaz, p21 sentezlenemez ve DNA onarımı için zaman "
                "tanınmaz. Hücre kırık, mutasyonlu veya translokasyonlu DNA'sını S fazında kopyalamaya devam eder. "
                "Daha da kötüsü, hasarlı hücre apoptoza yönlendirilemediği için bu genetik sapmalar klonal olarak "
                "tüm yavru hücrelere aktarılır. Bu durum mutasyon hızının katlanarak arttığı 'mutatör fenotip' "
                "ve 'genomik instabilite' evresini başlatır; karsinogenez için gerekli sürücü mutasyonlar hızla birikir."
            ),
            "elements": [
                make_table(
                    "p53 Sağlam Hücre vs p53 Mutant Hücre Davranışı",
                    ["Hücresel Durum", "Normal p53 (+/+)", "Mutant p53 (-/-)"],
                    [
                        {
                            "cells": ["DNA Hasarına Yanıt", "p21 ile G1 durması ve GADD45 ile onarım", "Duraklama olmaz, hasarlı DNA replike edilir"],
                            "hiddenIndex": 1,
                            "hint": "Döngüyü dondurarak tamire izin verme süreci"
                        },
                        {
                            "cells": ["Ağır Hasarda Sonuç", "BAX ve PUMA ile apoptoz (ölüm)", "Apoptozdan kaçış ve anormal sağkalım"],
                            "hiddenIndex": 1,
                            "hint": "Programlı intihar mekanizmasının çalışması"
                        },
                        {
                            "cells": ["Genomik Durum", "Genom bütünlüğü ve kromozom kararlılığı", "Aşırı mutasyon birikimi ve anöploidi"],
                            "hiddenIndex": 1,
                            "hint": "Genetik yapının korunması ve stabilitesi"
                        }
                    ]
                )
            ]
        }
    ]
