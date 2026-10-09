# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 29: Karsinojenezin Moleküler Temeli
(Prof. Dr. Hikmet Keleş - Tıbbi Patoloji ABD)
Bölüm 7: Kimyasal Karsinogenez İlkeleri ve Ajanlar (Slayt 61 - 70)
Checkpoint: Slayt 69
"""

from .helpers import (
    make_cloze, make_micro_quiz, make_table, make_before_after,
    make_causal_chain, make_active_recall, make_branching_logic
)

def get_section_7_slides():
    return [
        # Slayt 61
        {
            "slideNumber": 61,
            "title": "Kimyasal Karsinogenez İlkeleri",
            "content": (
                "Kimyasal karsinojenler, hücre genomunda doğrudan veya metabolik dönüşüm sonrası kalıcı DNA hasarı "
                "oluşturan doğal veya sentetik moleküllerdir. Kimyasal karsinogenezin temel biyofiziksel kuralı, "
                "nihai karsinojenik moleküllerin son derece reaktif **elektron seven (elektrofilik)** gruplar "
                "içermesidir. Hücrenin DNA, RNA ve protein molekülleri ise zengin **elektron verici (nükleofilik)** "
                "merkezlere sahiptir (özellikle guanin bazının N7 ve O6 pozisyonları). Elektrofilik karsinojenik "
                "metabolitler, DNA bazları ile kovalent bağlar kurarak **DNA adukları (DNA adducts)** oluştururlar. "
                "Bu aduklar DNA replikasyonundan önce tamir edilemezse, baz eşleşme hatalarına, transisyon ve "
                "transversiyon mutasyonlarına yol açarak onkogen veya tümör baskılayıcı genleri daimi olarak bozar."
            ),
            "elements": [
                make_cloze(
                    "Kimyasal karsinojenlerin DNA nükleofilik merkezleriyle kovalent bağ kurarak oluşturduğu hasarlı komplekslere DNA adukları denir.",
                    "adukları",
                    "Kovalent bağlanma kompleksi"
                ),
                make_active_recall(
                    "Nihai karsinojenik moleküllerin nükleik asit bazlarıyla kimyasal reaksiyona girmesini sağlayan temel kimyasal özelliği nedir?",
                    "Elektron çekici yüksek elektrofilik reaktiviteye sahip olmalarıdır.",
                    "Negatif yük arayan kimyasal afinite"
                )
            ]
        },

        # Slayt 62
        {
            "slideNumber": 62,
            "title": "Doğrudan Etkili Karsinojenler ve Sekonder AML",
            "content": (
                "Kimyasal karsinojenler metabolik aktivasyon gereksinimlerine göre iki sınıfa ayrılır: **Doğrudan "
                "etkili (direkt)** ve **Dolaylı etkili (indirekt)** karsinojenler. Doğrudan etkili karsinojenler, "
                "vücutta herhangi bir enzimatik veya kimyasal dönüşüme ihtiyaç duymaksızın doğrudan DNA ile "
                "reaksiyona giren güçlü elektrofillerdir. Genellikle zayıf karsinojenlerdir ancak tıpta büyük önem "
                "taşırlar çünkü **kanser kemoterapisinde kullanılan alkilleyici ajanlar (siklofosfamid, klorambusil, "
                "busulfan, melfalan, nitrozüreler)** bu gruptadır. Hodgkin lenfoma, meme kanseri veya over kanseri "
                "nedeniyle alkilleyici kemoterapi alan hastalarda tedaviden 5-8 yıl sonra kemik iliği kök hücrelerinde "
                "gelişen genetik hasarlar sonucu ölümcül **tedaviye bağlı sekonder Akut Miyeloid Lösemi (t-AML)** "
                "veya Miyelodisplastik Sendrom (t-MDS) riski ortaya çıkar."
            ),
            "elements": [
                make_table(
                    "Doğrudan vs Dolaylı Etkili Karsinojenler",
                    ["Kategori", "Metabolik Aktivasyon", "Klinik / Endüstriyel Örnek", "Tipik Malignite"],
                    [
                        {
                            "cells": ["Doğrudan Etkili", "Metabolik aktivasyon gerekmez", "Alkilleyici kemoterapötikler (Siklofosfamid)", "Tedaviye bağlı Akut Miyeloid Lösemi (t-AML)"],
                            "hiddenIndex": 1,
                            "hint": "Enzim dönüşümüne ihtiyaç duymama"
                        },
                        {
                            "cells": ["Dolaylı Etkili (Prokarsinojen)", "Hepatik P450 aktivasyonu şarttır", "Polisiklik aromatik hidrokarbonlar (PAH)", "Akciğer, mesane ve karaciğer karsinomları"],
                            "hiddenIndex": 1,
                            "hint": "Mikrozomal enzim aracılığı zorunluluğu"
                        }
                    ]
                ),
                make_active_recall(
                    "Hodgkin lenfoma veya solid tümör kemoterapisinde kullanılan alkilleyici ajanların yıllar sonra yol açabildiği en tehlikeli sekonder hematolojik malignite nedir?",
                    "Tedaviye bağlı Akut Miyeloid Lösemidir (t-AML).",
                    "Granülositik seri sekonder kemik iliği malignitesi"
                )
            ]
        },

        # Slayt 63
        {
            "slideNumber": 63,
            "title": "Dolaylı Karsinojenler ve Sitokrom P450 Enzimleri",
            "content": (
                "İnsanların çevresel ve mesleki olarak maruz kaldığı kimyasal karsinojenlerin ezici çoğunluğu "
                "**dolaylı etkili karsinojenlerdir (prokarsinojenler)**. Bu maddeler vücuda girdiklerinde biyolojik "
                "olarak inerttir; karsinojenik güçlerini konakçının endojen metabolik enzim sistemleri tarafından "
                "dönüştürüldükten sonra kazanırlar. Bu biyolojik dönüşümü (biyoaktivasyon) yürüten en kritik "
                "sistem karaciğer endoplazmik retikulumunda yerleşik **Sitokrom P450 bağımlı monooksijenaz "
                "(CYP) enzim ailesidir** (özellikle CYP1A1, CYP2E1, CYP3A4). Normalde vücuda giren yabancı "
                "hidrofobik toksinleri suda çözünür hale getirip safrayla veya idrarla atmayı hedefleyen bu "
                "detoksifikasyon reaksiyonları, ne yazık ki bazı kimyasalları reaktif elektrofilik epoksitlere "
                "ve radikallere çevirerek felakete yol açar. İnsanlar arasındaki CYP enzim polimorfizmleri, "
                "aynı miktarda sigara içen iki bireyden birinin neden kanser olup diğerinin olmadığını açıklar."
            ),
            "elements": [
                make_before_after(
                    "Detoksifikasyon Amacı vs Paradoksal Biyoaktivasyon",
                    "Fizyolojik Karaciğer Amacı",
                    "Lipofilik toksinleri hidroksilleyip polar hale getirmek ve idrar/safra ile güvenle vücuttan uzaklaştırmak.",
                    "Karsinojenik Biyoaktivasyon Felaketi",
                    "Sitokrom P450 oksidasyonu inert prokarsinojeni reaktif elektrofilik epoksite çevirerek doğrudan DNA mutasyonuna yol açar.",
                    "CYP1A1 geni aşırı indüklenebilir bireyler sigara dumanına maruz kaldıklarında akciğer kanserine çok daha yatkındır."
                ),
                make_cloze(
                    "İnert dolaylı prokarsinojenleri metabolik oksidasyonla aktif elektrofilik mutajenlere dönüştüren hepatik enzim sistemi Sitokrom P450 sistemidir.",
                    "Sitokrom",
                    "Mikrozomal hemoproteaz monooksijenaz kompleksi"
                )
            ]
        },

        # Slayt 64
        {
            "slideNumber": 64,
            "title": "Polisiklik Aromatik Hidrokarbonlar ve Benzo[a]piren",
            "content": (
                "**Polisiklik Aromatik Hidrokarbonlar (PAH)**, organik maddelerin (tütün, fosil yakıtlar, kömür "
                "katranı, mangalda kömürleşmiş etler) yüksek sıcaklıkta tam yanmaması sonucu oluşan en güçlü "
                "çevresel karsinojen grubudur. Bu ailenin prototipik temsilcisi **Benzo[a]piren**dir. Tarihsel olarak "
                "Sir Percivall Pott tarafından 1775 yılında baca temizleyicisi çocuklarda kurum maruziyetine bağlı "
                "skrotum kanserinin etiyolojisi olarak tanımlanmıştır (ilk mesleki kanser keşfi). Benzo[a]piren vücutta "
                "CYP1A1 ve epoksit hidrolaz enzimleri ile metabolize edilerek **benzo[a]piren diol epoksite (BPDE)** "
                "dönüşür. BPDE, DNA'daki guanin bazlarına kovalent kenetlenir ve replikasyon sırasında guanin yerine "
                "timin gelmesine neden olan karakteristik **G:C → T:A transversiyon mutasyonlarını** üretir; bu "
                "mutasyonel imza sigara içenlerin akciğer karsinomlarında TP53 ve KRAS genlerinde patognomoniktir."
            ),
            "elements": [
                make_causal_chain(
                    "Tütün Dumanından TP53 Transversiyon Mutasyonuna İlerleme Kaskadı",
                    [
                        "1. Benzo[a]piren İnhalasyonu: Tütün dumanındaki PAH partikülleri bronş epitel hücreleri içine difüze olur.",
                        "2. CYP1A1 Biyoaktivasyonu: Mikrozomal enzimler molekülü elektrofilik Benzo[a]piren Diol Epoksite (BPDE) çevirir.",
                        "3. Guanin Aduk Oluşumu: BPDE nükleusa geçerek TP53 geninin guanin bazlarına kovalent kollarla kenetlenir.",
                        "4. Transversiyon Mutasyonu: Replikasyon çatalı aduklu guanini timin olarak okur; G:C baz çifti T:A çiftine döner.",
                        "5. Epitelyal Karsinom: TP53 koruyucu fonksiyonunu yitirir ve bronş epitelinde skuamöz karsinom klonu türer."
                    ]
                ),
                make_active_recall(
                    "Tütün dumanındaki benzo[a]piren maruziyeti sonucu akciğer karsinomlarında TP53 geninde oluşan karakteristik transversiyon mutasyonu nedir?",
                    "G:C → T:A transversiyon mutasyonudur.",
                    "Guanin timin baz değişimi"
                )
            ]
        },

        # Slayt 65
        {
            "slideNumber": 65,
            "title": "Aromatik Aminler ve Mesane Karsinomu",
            "content": (
                "Boya, tekstil ve kauçuk endüstrisinde kullanılan **aromatik aminler ve azo boyaları "
                "(beta-naftilamin, benzidin)**, hedef organ spesifisitesi en çarpıcı mesleki karsinojenlerdir. "
                "Akciğerden veya ciltten emilen beta-naftilamin, karaciğere ulaşır ve sitokrom P450 ile hidroksilasyona "
                "uğrayıp glukuronik asit ile konjuge edilir. Bu konjuge metabolit karsinojenik değildir ve böbrekler "
                "yoluyla mesaneye atılır. Ancak idrarın asidik ortamında, mesane mukozasında bulunan **beta-glukuronidaz "
                "enzimi** glukuronit bağını parçalar ve karsinojenik elektrofilik metaboliti serbest bırakır. "
                "Yıllar boyu mesanede biriken idrarla temas eden ürotelyum hücreleri yoğun DNA hasarına maruz kalır; "
                "bu süreç maruziyetten 15-30 yıl sonra **mesane karsinomu (ürotelyal karsinom)** patlamasıyla sonlanır."
            ),
            "elements": [
                make_table(
                    "Aromatik Aminlerin Organ Spesifik Karsinogenez Mekanizması",
                    ["Anatomik İstasyon", "Biyokimyasal Süreç", "Karsinojenik Toksisite Durumu"],
                    [
                        {
                            "cells": ["Karaciğer Parankimi", "Glukuronik asit ile konjugasyon", "İnert ve zararsız metabolit formu"],
                            "hiddenIndex": 2,
                            "hint": "Toksik olmayan bağlı durum"
                        },
                        {
                            "cells": ["Mesane Lümeni (İdrar)", "Asidik idrarda beta-glukuronidaz ile serbestleşme", "Yüksek derecede mutajenik elektrofil salınımı"],
                            "hiddenIndex": 2,
                            "hint": "Mesane duvarında mutasyonel patlama"
                        }
                    ]
                ),
                make_cloze(
                    "Boya ve kauçuk sanayisinde beta-naftilamin maruziyeti sonucu karakteristik olarak gelişen malignite mesane karsinomudur.",
                    "mesane",
                    "İdrar torbası ürotelyal tümörü"
                )
            ]
        },

        # Slayt 66
        {
            "slideNumber": 66,
            "title": "Doğal Toksinler: Aflatoksin B1 ve TP53 Kodon 249",
            "content": (
                "Kimyasal karsinojenler yalnızca endüstriyel kaynaklı olmayıp doğada da üretilir. En ölümcül doğal "
                "karsinojen, nemli ve sıcak koşullarda uygunsuz depolanan tahıl, mısır ve yer fıstıklarında üreyen "
                "**Aspergillus flavus ve Aspergillus parasiticus** küf mantarlarının salgıladığı **Aflatoksin B1**dir. "
                "Özellikle Sahra Altı Afrika ve Güneydoğu Asya'da yaygındır. Aflatoksin B1 karaciğerde CYP3A4 "
                "tarafından son derece reaktif **aflatoksin-2,3-epoksite** çevrilir. Bu epoksit hepatosit genomunda "
                "**TP53 geninin 249. kodonundaki arginin bazını spesifik olarak serin ile değiştiren (R249S)** "
                "karakteristik transversiyon mutasyonunu (G:C → T:A) oluşturur. Eğer birey aynı zamanda kronik "
                "**Hepatit B Virüsü (HBV)** taşıyıcısı ise, aflatoksin ve viral hepatit sinerjik kooperasyon yaparak "
                "**Hepatosellüler Karsinom (HCC)** riskini yüzlerce katına fırlatır."
            ),
            "elements": [
                make_table(
                    "Aflatoksin B1 Karsinogenezinin Moleküler Parmak İzi",
                    ["Parametre", "Moleküler Detay", "Klinik Yansıması"],
                    [
                        {
                            "cells": ["Etiyolojik Ajan", "Aspergillus mantar toksini", "Küflü tahıl ve yer fıstığı tüketimi"],
                            "hiddenIndex": 1,
                            "hint": "Depolanmış tahılda üreyen küf salgısı"
                        },
                        {
                            "cells": ["Spesifik Mutasyonel Hedef", "TP53 geni kodon 249 transversiyonu (R249S)", "Hepatosellüler karsinomda moleküler imza"],
                            "hiddenIndex": 1,
                            "hint": "İki yüz kırk dokuzuncu nükleotid üçlüsü"
                        },
                        {
                            "cells": ["Sinerjik Viral Ortak", "Hepatit B Virüsü (HBV)", "Devasa HCC riski ve karaciğer yetmezliği"],
                            "hiddenIndex": 1,
                            "hint": "Karaciğeri tutan enfeksiyöz DNA etkeni"
                        }
                    ]
                ),
                make_active_recall(
                    "Aspergillus mantarlarının ürettiği aflatoksin B1'in hepatosellüler karsinom gelişiminde TP53 geninde oluşturduğu spesifik mutasyonel kodon hangisidir?",
                    "TP53 geninin 249. kodonundaki mutasyondur (R249S).",
                    "İki yüz kırk dokuzuncu amino asit bölgesi"
                )
            ]
        },

        # Slayt 67
        {
            "slideNumber": 67,
            "title": "Nitrozaminler, Diyet Faktörleri ve Mide Kanseri",
            "content": (
                "Diyet alışkanlıkları ve gıda koruyucuları kimyasal karsinojenlerin vücuda alınmasında majör bir "
                "kaynaktır. İşlenmiş et ürünlerine (salam, sosis, sucuk) botulizm bakterisini önlemek ve rengi "
                "korumak amacıyla eklenen **nitrit ve nitrat tuzları**, midenin asidik ortamında gıdalardaki sekonder "
                "aminlerle reaksiyona girerek **nitrozaminlere ve nitrozamidlere** dönüşür. Ayrıca tütsülenmiş, "
                "tuzlanmış balık ve turşu gibi gıdalar yüksek konsantrasyonda prekarsinojenik nitrozobileşikler "
                "içerir. Nitrozaminler gastrik foveoler kök hücre DNA'sında alkilasyon lezyonları (O6-metilguanin) "
                "oluşturur. Midede **Helicobacter pylori** enfeksiyonunun bulunması, mukozal pH'yı yükselterek "
                "nitrat indirgeyen bakterilerin çoğalmasına ve endojen nitrozamin sentezinin katlanmasına neden "
                "olarak **mide adenokarsinomu** riskini sinerjik olarak artırır."
            ),
            "elements": [
                make_before_after(
                    "Taze Akdeniz Diyeti vs İşlenmiş Nitratlı Diyet Mide Mukozası",
                    "Taze Sebze ve Meyve Ağırlıklı Diyet",
                    "C vitamini ve antioksidanlar nitrozamin oluşumunu midede kimyasal olarak bloke eder; mukozal epitel intakt kalır.",
                    "İşlenmiş Et ve Tütsülenmiş Tuzlu Gıdalar",
                    "Aşırı nitrozamin sentezi, O6-metilguanin adukları, kronik atrofik gastrit zemininde intestinal metaplazi ve adenokarsinom.",
                    "Antioksidan vitaminler (C ve E vitamini) intragastrik nitrozasyon reaksiyonunun güçlü inhibitörleridir."
                ),
                make_cloze(
                    "İşlenmiş etlerdeki koruyucu nitrit tuzlarının midede aminlerle birleşmesi sonucu oluşan karsinojenik bileşikler nitrozaminlerdir.",
                    "nitrozaminlerdir",
                    "Gıda katkısı türevi alkilleyici nitrozo bileşikleri"
                )
            ]
        },

        # Slayt 68
        {
            "slideNumber": 68,
            "title": "Çok Aşamalı Model: İnisiyasyon, Promosyon, Progresyon",
            "content": (
                "Deneysel kimyasal karsinogenez çalışmaları (klasik Berenblum fare derisi modeli), kanser gelişiminin "
                "üç net evreden oluştuğunu kanıtlamıştır: 1) **İnisiyasyon (Başlatma)**: Mutajenik bir başlatıcı "
                "ajanın (initiator) uygulanmasıdır. Hızlı, geri dönüşümsüz (irreversible) bir süreçtir; DNA'da "
                "kalıcı mutasyon oluşturur ancak inisiye hücre tek başına kitle oluşturamaz. 2) **Promosyon "
                "(Destekleme)**: İnisiyasyondan sonra uygulanan, tek başlarına mutajen veya karsinojen olmayan "
                "ancak hücre bölünmesini uyaran ajanların (promotörler: forbol esterleri/TPA, hormonlar, fenol, "
                "safra tuzları) etkisidir. **Geri dönüşümlüdür (reversible)**; inisiyatörden önce verilirse veya "
                "aralıklar çok uzatılırsa tümör gelişmez. 3) **Progresyon (İlerleme)**: Preneoplastik klonun "
                "otonom, anaplastik ve metastatik malignite kazanmasıdır."
            ),
            "elements": [
                make_table(
                    "İnisiyatör (Başlatıcı) ile Promotör (Destekleyici) Farkları",
                    ["Özellik", "İnisiyatör Ajan", "Promotör Ajan"],
                    [
                        {
                            "cells": ["Mutajenik Kapasite", "Doğrudan mutajeniktir (DNA hasarı yapar)", "Kesinlikle mutajen değildir (Mitotik uyarı yapar)"],
                            "hiddenIndex": 2,
                            "hint": "Hücre bölünmesini tetikleyen etki"
                        },
                        {
                            "cells": ["Geri Dönüşümlülük", "Geri dönüşümsüzdür (Kalıcı DNA hasarı)", "Geri dönüşümlüdür (Uygulama kesilince etki biter)"],
                            "hiddenIndex": 2,
                            "hint": "Destekleyicinin tersine çevrilebilir tabiatı"
                        },
                        {
                            "cells": ["Uygulama Sıralaması", "Önce uygulanmalıdır (Tek doz dahi yeter)", "İnisiyatörden sonra ve tekrarlayan dozda verilmelidir"],
                            "hiddenIndex": 2,
                            "hint": "Başlatıcı sonrası ardışık maruziyet"
                        }
                    ]
                ),
                make_micro_quiz(
                    "Kimyasal karsinogenezde mutajenik olmayan, tek başına tümör yapmayan ancak inisiye olmuş hücrelerin klonal proliferasyonunu tetikleyen ve etkisi geri dönüşümlü olan faktör hangisidir?",
                    [
                        {
                            "key": "A",
                            "text": "Promotör ajan",
                            "isCorrect": True,
                            "explanation": "Promotörler (TPA, hormonlar vb.) mutajen değildir, geri dönüşümlüdür ve inisiye hücrenin çoğalmasını uyarırlar."
                        },
                        {
                            "key": "B",
                            "text": "İnisiyatör ajan",
                            "isCorrect": False,
                            "explanation": "İnisiyatörler mutajendir ve geri dönüşsüz DNA hasarı yaparlar."
                        },
                        {
                            "key": "C",
                            "text": "DNA alkilleyicisi",
                            "isCorrect": False,
                            "explanation": "Alkilleyiciler başlatıcı mutajenlerdir."
                        },
                        {
                            "key": "D",
                            "text": "Onkojenik retrovirüs",
                            "isCorrect": False,
                            "explanation": "Retrovirüsler viral karsinojenlerdir."
                        }
                    ],
                    "Promotörler bölünmeyi tetikleyici geri dönüşümlü epigenetik ajanlardır."
                )
            ]
        },

        # Slayt 69: CHECKPOINT 7
        {
            "slideNumber": 69,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Kimyasal Karsinogenez ve Toksinler",
            "content": (
                "Yedinci bölümün bu tekrar sayfasında, kimyasal karsinojenlerin etki mekanizmaları ve karsinogenezin "
                "evresi özetlenmektedir. Nihai karsinojenler elektrofiliktir ve DNA'nın nükleofilik merkezleriyle "
                "kovalent aduklar kurar. Doğrudan etkili olan alkilleyiciler (kemoterapötikler) metabolik aktivasyon "
                "gerektirmez ve yıllar sonra sekonder AML'ye yol açar. Dolaylı karsinojenler karaciğer Sitokrom "
                "P450 monooksijenazları ile biyoaktive edilir; tütün dumanındaki benzo[a]piren TP53'te G:C>T:A "
                "transversiyonu yapar. Aromatik aminler (beta-naftilamin) mesane karsinomuna; Aspergillus toksini "
                "aflatoksin B1 ise TP53 kodon 249 mutasyonu ile HCC'ye yol açar. İnisiyasyon kalıcı mutasyondur; "
                "promosyon ise mutajen olmayan geri dönüşümlü klonal çoğalma evresidir."
            ),
            "flashcards": [
                {
                    "id": "k1-29-cp07-fc01",
                    "front": "Vücutta metabolik biyodönüşüme gerek duymadan doğrudan DNA ile kovalent bağ kurabilen kemoterapötik karsinojen grubu hangisidir?",
                    "back": "Alkilleyici kemoterapi ajanlarıdır.",
                    "hint": "Doğrudan etkili sitotoksik ilaç sınıfı"
                },
                {
                    "id": "k1-29-cp07-fc02",
                    "front": "Aspergillus mantarlarının ürettiği aflatoksin B1'in hepatosellüler karsinom gelişiminde TP53 geninde oluşturduğu spesifik mutasyon odağı neresidir?",
                    "back": "Kodon 249 transversiyonudur (R249S).",
                    "hint": "İki yüz kırk dokuzuncu amino asit bölgesi"
                },
                {
                    "id": "k1-29-cp07-fc03",
                    "front": "Boya ve kauçuk endüstrisinde çalışanlarda idrarda serbestleşerek mesane karsinomuna yol açan klasik aromatik amin karsinojeni nedir?",
                    "back": "Beta-naftilamindir (veya benzidin).",
                    "hint": "Mesane ürotelyal tümörü yapan endüstriyel kimyasal"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 7 Özet Tablosu: Kimyasal Karsinojenler",
                    ["Kimyasal Ajan", "Aktivasyon Tipi", "Hedef Organ / Malignite"],
                    [
                        {
                            "cells": ["Alkilleyici Ajanlar (Siklofosfamid)", "Doğrudan etkili", "Kemik iliği (Tedaviye bağlı sekonder AML)"],
                            "hiddenIndex": 2,
                            "hint": "Miyeloid lösemi yapan kemoterapi toksisitesi"
                        },
                        {
                            "cells": ["Aflatoksin B1 (Aspergillus)", "Dolaylı etkili (P450)", "Karaciğer (Hepatosellüler karsinom)"],
                            "hiddenIndex": 2,
                            "hint": "Primer hepatik malignite odağı"
                        }
                    ]
                )
            ]
        },

        # Slayt 70
        {
            "slideNumber": 70,
            "title": "Klinik Karar: Alkilleyici Kemoterapi Sonrası Pansitopeni Yönetimi",
            "content": (
                "Geçmişinde Hodgkin lenfoma veya meme karsinomu nedeniyle alkilleyici ajan (siklofosfamid, "
                "mekloretamin) içeren yoğun kemoterapi protokolleri almış hastaların uzun dönem onkolojik "
                "takibinde sekonder malignite şüphesi daima akılda tutulmalıdır. Tedaviden 4-8 yıl sonra gelişen "
                "ilerleyici halsizlik, anemi, trombositopeniye bağlı peteşiler ve lökopeni (pansitopeni) tablosunda, "
                "basit bir kemik iliği hipoplazisi düşünülmeden önce **tedaviye bağlı MDS / AML (t-AML)** mutlak "
                "surette ekarte edilmelidir. Bu hastalarda kemik iliği aspirasyon ve biyopsisinde promiyelositik veya "
                "miyeloblastik proliferasyon aranır ve sitogenetikte alkilleyici hasarının göstergesi olan **5. veya "
                "7. kromozom delesyonları (-5, del(5q), -7, del(7q))** araştırılır."
            ),
            "elements": [
                make_branching_logic(
                    "46 yaşında kadın hasta 6 yıl önce Evre 2 meme karsinomu nedeniyle antrasiklin ve siklofosfamid (alkilleyici) kemoterapisi almıştır ve remisyondadır. Son 2 aydır derinleşen halsizlik, burun kanamaları ve ateş ile başvuruyor. Tam kanda Hb: 7.2 g/dL, Trombosit: 28.000/uL, BK: 2.100/uL saptanıyor (pansitopeni). Periferik yaymada %25 miyeloblast izleniyor.",
                    "Bu hastada altta yatan patolojinin tanısı ve etiyolojik mekanizması için en doğru klinik-patolojik yaklaşım ne olmalıdır?",
                    [
                        {
                            "text": "Kemik iliği biyopsisi ve sitogenetik analiz yapılmalı; alkilleyici ajan maruziyetine bağlı gelişen sekonder t-AML (tedaviye bağlı AML) tanısı konmalıdır.",
                            "isCorrect": True,
                            "explanation": "Alkilleyici kemoterapiden 5-8 yıl sonra gelişen pansitopeni ve blast artışı klasik tedaviye bağlı AML (t-AML) tablosudur; sıklıkla 5 ve 7. kromozom anomalileri içerir."
                        },
                        {
                            "text": "Meme kanserinin kemik iliğine metastaz yaptığı düşünülerek sadece hormon tedavisi başlanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Miyeloblastlar hematolojik malignite göstergesidir; karsinom metastazında blast görülmez."
                        },
                        {
                            "text": "Hastada B12 vitamini eksikliği düşünülerek vitamin enjeksiyonu ile eve gönderilmelidir.",
                            "isCorrect": False,
                            "explanation": "Periferik kanda %25 miyeloblast varlığı doğrudan Akut Lösemi tanısı koydurur, B12 eksikliğiyle açıklanamaz."
                        }
                    ]
                ),
                make_micro_quiz(
                    "Alkilleyici kemoterapi ajanları maruziyeti sonucu yıllar sonra gelişen tedaviye bağlı sekonder akut miyeloid lösemi (t-AML) olgularında en sık rastlanan sitogenetik lezyonlar hangileridir?",
                    [
                        {
                            "key": "A",
                            "text": "5 ve 7. kromozom delesyonları veya monozomileri [-5/del(5q), -7/del(7q)]",
                            "isCorrect": True,
                            "explanation": "Alkilleyici ajan hasarına bağlı t-AML olgularında karakteristik olarak 5q ve 7q delesyonları veya monozomileri görülür ve prognozu çok kötüdür."
                        },
                        {
                            "key": "B",
                            "text": "t(9;22) Philadelphia translokasyonu",
                            "isCorrect": False,
                            "explanation": "t(9;22) primer KML belirtecidir."
                        },
                        {
                            "key": "C",
                            "text": "t(8;14) MYC translokasyonu",
                            "isCorrect": False,
                            "explanation": "t(8;14) Burkitt lenfoma lezyonudur."
                        },
                        {
                            "key": "D",
                            "text": "MYCN amplifikasyonu",
                            "isCorrect": False,
                            "explanation": "MYCN nöroblastom belirtecidir."
                        }
                    ],
                    "Alkilleyiciye bağlı sekonder AML tipik olarak 5 ve 7. kromozom kayıplarıyla seyreder."
                )
            ]
        }
    ]
