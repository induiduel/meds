# -*- coding: utf-8 -*-
"""
Kurul 1 - Ders 27: Üriner Sistem Taş Hastalıkları Fizyopatolojisi
Bölüm 7: Kalkülüs Oluşum Teorileri ve Randall Plakları (Slayt 61 - 70)
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
            "title": "Kalkülüs Oluşum Teorilerine Genel Bakış",
            "content": (
                "Böbrek taşlarının oluşum mekanizmasını açıklamak üzere geliştirilen bilimsel teoriler, idrarın fizikokimyasal "
                "özellikleri ile renal anatomi ve hücresel biyolojiyi sentezlemeyi amaçlar. Taş hastalığı yalnızca tübül içi "
                "bir çökelme süreci olmayıp, renal medulladaki interstisyel dokudan başlayan karmaşık bir mineralizasyon "
                "kaskadıdır. Günümüzde kabul gören başlıca teoriler şunlardır: Alexander Randall tarafından 1937'de tanımlanan "
                "ve modern endoürolojik biyopsilerle doğrulanan 'Randall Plak Teorisi', toplayıcı tübüllerdeki tıkaçları "
                "açıklayan 'Randall Tıkaç Teorisi', hiperoksalürinin sitotoksik etkilerine dayanan 'Tübüler Hasar Teorisi', "
                "medüller vasküler bozuklukları öne süren 'Vasküler Hipotez' ve anatomik akım engellerine odaklanan 'Üriner Staz Teorisi'."
            ),
            "elements": [
                make_table(
                    "Kalkülüs Oluşum Teorilerinin Karşılaştırmalı Özeti",
                    ["Teori Adı", "Başlangıç Odak Noktası", "Primer Patolojik Olay", "Hedef Taş Türü"],
                    [
                        {
                            "cells": ["Randall Plak Teorisi", "Henle kulpu bazal membranı", "Subepitelyal kalsiyum apatit çökmesi", "İdiyopatik kalsiyum oksalat"],
                            "hiddenIndex": 1,
                            "hint": "İnterstisyel kalsiyum fosfat birikimi"
                        },
                        {
                            "cells": ["Randall Tıkaç Teorisi", "Bellini kanalı lümeni", "Tübül içi apatit tıkacı ve erozyon", "Bruşit, RTA, hiperparatiroidi"],
                            "hiddenIndex": 0,
                            "hint": "Toplayıcı kanal ağzı teorisi"
                        },
                        {
                            "cells": ["Vasküler Hipotez", "Vasa rekta mikrodolaşımı", "Endotel hasarı ve kalsifikasyon", "Papiller nekroz ve taş"],
                            "hiddenIndex": 2,
                            "hint": "Damarsal zedelenme ve kireçlenme"
                        }
                    ]
                ),
                make_cloze(
                    "İdiyopatik kalsiyum oksalat taşlarının en temel başlangıç lezyonunu açıklayan teori Randall plak teorisi olarak adlandırılır.",
                    "Randall plak teorisi",
                    "Papiller subepitelyal başlangıç modeli"
                )
            ]
        },
        # Slayt 62
        {
            "slideNumber": 62,
            "title": "Randall Plak Teorisi: Papiller Subepitelyal Apatit",
            "content": (
                "Alexander Randall 1937 yılında kadavra böbreklerinde yaptığı incelemelerde, renal papillaların ürotelyum "
                "altında krem-beyaz renkte kalsifiye lezyonlar gözlemlemiş ve bunların taş oluşumu için bir 'nidus' olduğunu "
                "ileri sürmüştür. Günümüzde fleksibl üreterorenoskopi (fURS) ile yapılan direkt görselleştirmeler, idiyopatik "
                "kalsiyum oksalat taşı oluşturan hastaların renal papillalarının %90'ından fazlasında Randall plaklarının "
                "bulunduğunu kanıtlamıştır. Bu plaklar idrar lümeninde değil, renal medullanın derin interstisyumunda, "
                "özellikle ince Henle kulpunun bazal membranında başlayan biyolojik bir kalsifikasyon sürecidir."
            ),
            "elements": [
                make_active_recall(
                    "Randall plaklarının böbrek piramidinde ilk olarak mikroskobik olarak başladığı özgül anatomik bölge neresidir?",
                    "İnce Henle kulpunun bazal membranıdır.",
                    "Medüller tübül bazal zarı"
                ),
                make_before_after(
                    "Sağlıklı Papilla vs Randall Plaklı Papilla",
                    "Normal Renal Papilla",
                    "Pürüzsüz pembe ürotelyum, intakt bazal membran, interstisyel kalsifikasyon yok, taş yapışma alanı sıfır.",
                    "Randall Plaklı Papilla",
                    "Subepitelyal beyaz-sarı kalsiyum apatit adacıkları, aşınmış ürotelyum, idrarla temas eden sert kalsifiye yatak.",
                    "Randall plaklarının yüzey alanı taş nüks sıklığı ile doğrusal korelasyon gösterir."
                )
            ]
        },
        # Slayt 63
        {
            "slideNumber": 63,
            "title": "İnce Henle Kulpu Bazal Membranı ve Apatit Çökmesi",
            "content": (
                "Randall plağının oluşumu, Henle kulpunun çıkan ince kolunun bazal membranında başlar. Bu bölgede medüller "
                "hipertonisite ve yüksek kalsiyum konsantrasyonu mevcuttur. Bazal membrandaki kollajen lifleri ve anyonik "
                "proteoglikanlar, ortamdaki kalsiyum ve fosfat iyonlarını bağlayarak ilk 'biyolojik apatit' (karbonatlanmış "
                "kalsiyum fosfat) sferüllerini oluşturur. Zamanla bu küçük apatit partikülleri interstisyel matriks boyunca "
                "yayılır ve birleşerek papilla ucundaki toplayıcı kanalların çevresini saran dev kalsifiye plaklara dönüşür. "
                "Burada dikkat edilmesi gereken en temel kural, plağın ana mineralinin oksalat değil kalsiyum fosfat (apatit) olmasıdır."
            ),
            "elements": [
                make_cloze(
                    "Randall plaklarının çekirdek yapısını oluşturan primer mineral kalsiyum fosfat yapısındaki apatit kristalidir.",
                    "apatit",
                    "Temel fosfat minerali"
                ),
                make_micro_quiz(
                    "Randall plağının kimyasal bileşimi ve başlangıç yeri ile ilgili doğru ifade hangisidir?",
                    [
                        {
                            "text": "İnce Henle kulpu bazal membranında başlayan karbonatlanmış kalsiyum fosfat (apatit) birikimidir.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; plak interstisyel apatitten doğar, üzerine kalsiyum oksalat büyür."
                        },
                        {
                            "text": "Toplayıcı kanallarda ürik asit kristallerinin saf çökmesiyle oluşur.",
                            "isCorrect": False,
                            "explanation": "Randall plağı ürik asit değil kalsiyum apatit yapısındadır."
                        },
                        {
                            "text": "Bakteriyel enfeksiyon sonucu oluşan saf strüvit kitlesidir.",
                            "isCorrect": False,
                            "explanation": "Strüvit enfeksiyon taşıdır; Randall plağı steril idiyopatik taşa yataklık eder."
                        },
                        {
                            "text": "Glomerül mezanjiyumunda biriken amiloid fibrilleridir.",
                            "isCorrect": False,
                            "explanation": "Randall plağı medüller kalsifikasyondur, amiloidoz ile ilgisi yoktur."
                        }
                    ],
                    "Randall plakları Henle kulpu bazal membranında apatit çökmesiyle başlayan interstisyel lezyonlardır."
                )
            ]
        },
        # Slayt 64
        {
            "slideNumber": 64,
            "title": "Ürotelyal Erozyon ve Kalsiyum Oksalatın Büyümesi",
            "content": (
                "Subepitelyal interstisyumda büyüyen apatit plağı zamanla papilla yüzeyine doğru ilerler ve üzerindeki "
                "ürotelyal örtüyü gererek iskemiye ve fokal ürotelyal nekroza yol açar. Ürotelyum yırtıldığında (erozyon), "
                "kalsifiye apatit plağı doğrudan pelvikaliseal sistemdeki idrara maruz kalır. İdrarda bulunan Tamm-Horsfall "
                "proteini ve osteopontin gibi organik moleküller açıkta kalan plağın üzerine hızla adsorbe olarak yapışkan "
                "bir ara katman oluşturur. Bu yapışkan ara katmanın üzerine idrardaki kalsiyum ve oksalat iyonları çökelir; "
                "böylece apatit plağı üzerinde büyüyen klasik kalsiyum oksalat monohidrat taşı meydana gelir."
            ),
            "elements": [
                make_causal_chain(
                    "Randall Plağından Kalsiyum Oksalat Taşına Uzanan Patofizyoloji",
                    [
                        "1. İnterstisyel Mineralizasyon: Henle kulpu bazal membranında apatit sferüllerinin birikmesi",
                        "2. Subepitelyal Yayılım: Plakların genişleyerek renal papillanın uç kısmına doğru ilerlemesi",
                        "3. Ürotelyal Erozyon: Apatit kitlesinin ürotelyumu aşındırıp doğrudan idrar boşluğuna açılması",
                        "4. Biyo-Matriks Örtüsü: Açıkta kalan plağın idrar proteinleri ve osteopontin ile kaplanması",
                        "5. CaOx Büyümesi: Kalsiyum oksalat kristallerinin bu organik ara yüzey üzerinde hızla taşlaşması"
                    ]
                ),
                make_active_recall(
                    "Renal papillada ürotelyumun erozyona uğraması sonucu açığa çıkan apatit plağının üzerine idrardan ilk çöken organik koruyucu/yapıştırıcı katman nedir?",
                    "Osteopontin ve Tamm-Horsfall gibi idrar makromoleküllerinden oluşan biyo-matriks tabakasıdır.",
                    "Protein ara tabakası"
                )
            ]
        },
        # Slayt 65
        {
            "slideNumber": 65,
            "title": "Randall Tıkaçları (Bellini Kanal Tıkaçları)",
            "content": (
                "Randall plağının yanı sıra literatürde 'Randall Tip 2 lezyonu' veya 'Bellini kanal tıkacı' olarak bilinen "
                "farklı bir taş başlangıç modeli mevcuttur. Bu mekanizma idiyopatik kalsiyum oksalat hastalarından ziyade; "
                "distal renal tübüler asidoz, primer hiperparatiroidi, primer hiperoksalüri ve bruşit taşı hastalarında görülür. "
                "Bu patolojilerde mineralizasyon interstisyumda değil, doğrudan toplayıcı tübüllerin ve Bellini kanallarının "
                "lümeni içinde başlar. Aşırı süpersatürasyon nedeniyle lümeni tıkayan dev kristal tıkaçları çevreleyen "
                "tübül epitelinde bası nekrozu, tübül yırtılması ve fokal interstisyel fibrozis yaratır; taş bu lüminal tıkaç "
                "üzerinden kaliks boşluğuna doğru uzanır."
            ),
            "elements": [
                make_table(
                    "Randall Plağı (Tip 1) ile Randall Tıkacı (Tip 2) Arasındaki Farklar",
                    ["Özellik", "Randall Plağı (Tip 1)", "Randall Tıkacı (Tip 2)"],
                    [
                        {
                            "cells": ["Başlangıç Yeri", "İnterstisyum (Henle bazal membranı)", "İntralüminal (Bellini kanalı içi)"],
                            "hiddenIndex": 2,
                            "hint": "Toplayıcı kanal içi yerleşim"
                        },
                        {
                            "cells": ["Tipik Hastalık Grubu", "İdiyopatik kalsiyum oksalat taşları", "Distal RTA, Bruşit, Primer Hiperparatiroidi"],
                            "hiddenIndex": 2,
                            "hint": "Asidoz ve fosfat taşı hastalıkları"
                        },
                        {
                            "cells": ["Renal Parankim Hasarı", "Çok sınırlı / minimal hasar", "Şiddetli tübüler nekroz ve interstisyel fibrozis"],
                            "hiddenIndex": 2,
                            "hint": "Ciddi tübül zedelenmesi ve nedbe"
                        }
                    ]
                ),
                make_cloze(
                    "Distal RTA ve bruşit taşlarında görülen toplayıcı tübül içi kristal kitlelerine Bellini kanal tıkacı adı verilir.",
                    "Bellini kanal tıkacı",
                    "İntralüminal tübüler tıkaç"
                )
            ]
        },
        # Slayt 66
        {
            "slideNumber": 66,
            "title": "Oksalat Toksisitesi ve Tübüler Hasar Teorisi",
            "content": (
                "Oksalat iyonu (C2O4^2-) renal tübüler epitel hücreleri için doğrudan ve güçlü bir sitotoksik moleküldür. "
                "Hiperoksalürik durumlarda yüksek konsantrasyonda serbest oksalata veya kalsiyum oksalat monohidrat kristallerine "
                "maruz kalan proksimal tübül hücrelerinde mitokondriyal disfonksiyon tetiklenir. Mitokondri membran potansiyeli "
                "kaybolur, sitokrom c salınır ve masif 'reaktif oksijen türleri' (ROS) üretimi başlar. Hücre içi serbest radikal "
                "patlaması lipid peroksidasyonuna, DNA hasarına ve apoptoza yol açar. Hasarlanan epitel hücreleri membranındaki "
                "glikokaliks korumasını kaybederek kristalleri kuvvetle bağlayan sabit birer nidus haline gelir."
            ),
            "elements": [
                make_before_after(
                    "Oksalatın Renal Hücresel Etkisi",
                    "Fizyolojik Oksalat Düzeyi",
                    "İntakt mitokondri, dengeli antioksidan savunma, pürüzsüz apikal membran, kristal tutulması yok.",
                    "Toksik Hiperoksalüri",
                    "Mitokondriyal çöküş, masif ROS üretimi, lipid peroksidasyonu, apoptoz ve kristallerin hasarlı zara yapışması.",
                    "Oksalat toksisitesi antioksidan kapasiteyi aşarak litogenezi hücresel düzeyde tetikler."
                ),
                make_active_recall(
                    "Hiperoksalürinin renal tübül epitel hücrelerinde hücresel hasar yaratmasında rol oynayan temel biyokimyasal aracı nedir?",
                    "Mitokondriyal kaynaklı reaktif oksijen türleri (ROS) ve oksidatif strestir.",
                    "Serbest oksijen radikalleri"
                )
            ]
        },
        # Slayt 67
        {
            "slideNumber": 67,
            "title": "Vasküler Hipotez: Mikrodolaşım Hasarı ve Kalsifikasyon",
            "content": (
                "Vasküler hipotez, taş hastalığının aslında renal meduller mikrodolaşımın vasküler bir patolojisi olduğunu "
                "savunur. Renal papillayı besleyen vasa rekta damarları, papilla ucunda U dönüşü yaparak son derece "
                "türbülanslı ve düşük akımlı bir mikrosirkülasyon oluşturur. Hipertansiyon, hiperlipidemi ve diyabet gibi "
                "aterosklerotik risk faktörleri vasa rekta endotelinde mikrovasküler hasara yol açar. Endotel hasarını takiben "
                "gelişen mikroenfarktüsler ve perivasküler inflamasyon, tıpkı aterosklerotik damar duvarında olduğu gibi "
                "distrofik kalsifikasyon başlatır. Bu perivasküler kalsifikasyon zamanla komşu Henle kulplarına ve interstisyuma "
                "ilerleyerek Randall plağına dönüşür."
            ),
            "elements": [
                make_cloze(
                    "Renal papillayı besleyen vasa rekta damarlarındaki mikrovasküler hasarı taş oluşumunun temeli sayan görüş vasküler hipotez olarak bilinir.",
                    "vasküler hipotez",
                    "Damarsal kökenli litogenez teorisi"
                ),
                make_active_recall(
                    "Vasküler hipoteze göre Randall plağı oluşumu hangi yaygın damar patolojisinin medüller bir benzeridir?",
                    "Ateroskleroz ve arteriyel distrofik kalsifikasyon sürecinin bir benzeridir.",
                    "Damar sertliği plak modeli"
                )
            ]
        },
        # Slayt 68
        {
            "slideNumber": 68,
            "title": "Üriner Staz ve Anatomik Anomaliler",
            "content": (
                "Üriner staz (idrar akımının yavaşlaması veya göllenmesi), litogenezin en güçlü fiziksel kolaylaştırıcısıdır. "
                "Normal idrar akımı mikrokristalleri henüz büyümeden yıkayıp atarken, staz durumunda nefron transit süresi "
                "uzar; kristallerin agregasyona uğraması ve birbiriyle birleşmesi için ideal bir zaman penceresi doğar. "
                "Üretero-pelvik bileşke (UPJ) darlığı, at nalı böbrek (isthmus basısı ve yüksek üreter çıkışı), kaliks "
                "divertikülü ve medüller sünger böbrek gibi konjenital anomaliler bölgesel idrar stazı yaratarak tekrarlayan "
                "taş oluşumuna zemin hazırlar. Ancak bu anatomik anomalili hastalarda bile altta yatan metabolik bir bozukluk "
                "(hiperkalsiüri vb.) çoğunlukla sürece eşlik eder."
            ),
            "elements": [
                make_table(
                    "Üriner Staz Yaratan Anatomik Anomaliler ve Litogenik Mekanizmaları",
                    ["Anatomik Anomali", "Staz Mekanizması", "Tipik Taş Lokalizasyonu"],
                    [
                        {
                            "cells": ["At Nalı Böbrek", "Yüksek üreter insersiyonu ve alt pol füzyonu", "Alt kaliksler ve renal pelvis"],
                            "hiddenIndex": 0,
                            "hint": "Füzyon anomalisi böbrek"
                        },
                        {
                            "cells": ["Kaliks Divertikülü", "Dar boyunlu kistik boşlukta idrar hapsi", "İzole divertikül lümeni içi"],
                            "hiddenIndex": 1,
                            "hint": "Genişlemiş kaliks cebi"
                        },
                        {
                            "cells": ["Medüller Sünger Böbrek", "Toplayıcı kanallarda kistik dilatasyon ve ektazi", "Renal papilla ve piramitler"],
                            "hiddenIndex": 2,
                            "hint": "Ektatik toplayıcı kanallar"
                        }
                    ]
                ),
                make_micro_quiz(
                    "İdrar akım stazının taş oluşumunu tetiklemesindeki temel fiziksel mekanizma hangisidir?",
                    [
                        {
                            "text": "Transit süresini uzatarak kristallerin agregasyon ve retansiyon için yeterli zaman bulmasını sağlaması",
                            "isCorrect": True,
                            "explanation": "Doğrudur; akım yavaşlayınca kristaller yıkanamaz ve hızla kümelenip çöker."
                        },
                        {
                            "text": "Böbrek sıcaklığını 45 dereceye kadar yükselterek suyu buharlaştırması",
                            "isCorrect": False,
                            "explanation": "Vücut ısısında buharlaşma gerçekleşmez."
                        },
                        {
                            "text": "Böbreğin eritropoietin salgısını sıfırlaması",
                            "isCorrect": False,
                            "explanation": "Eritropoietin anemiyle ilgilidir, litogenez mekanizması değildir."
                        },
                        {
                            "text": "Kalsiyum atomlarını parçalayarak potasyuma dönüştürmesi",
                            "isCorrect": False,
                            "explanation": "Nükleer transmutasyon biyolojik sistemlerde imkansızdır."
                        }
                    ],
                    "Staz, kristallere nefron içinde büyüme ve agregasyon için gerekli olan temas süresini sağlar."
                )
            ]
        },
        # Slayt 69 [CHECKPOINT 7]
        {
            "slideNumber": 69,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Taş Oluşum Teorileri",
            "content": (
                "Bu bölümde taş oluşumuna ilişkin Randall plakları, tübüler tıkaçlar, vasküler ve staz teorilerini özetledik. "
                "Randall plak teorisi, idiyopatik kalsiyum oksalat taşlarının en yaygın başlangıç zeminidir. "
                "Plak ilk olarak ince Henle kulpunun bazal membranında karbonatlanmış kalsiyum fosfat (apatit) olarak başlar. "
                "Apatit plağı subepitelyal olarak ilerleyip ürotelyumu aşındırır; idrarla temas eden çıplak plağın üzerine CaOx çöker. "
                "Randall tıkacı (Bellini kanal tıkacı), distal RTA ve bruşit taşlarında toplayıcı kanal lümenini dolduran kitlelerdir. "
                "Hiperoksalüri tübül hücrelerinde mitokondri hasarı ve ROS patlaması yaratarak epitelyal adezyonu tetikler. "
                "Vasküler hipotez vasa rekta mikrosirkülasyon hasarını ateroskleroz benzeri distrofik kalsifikasyonla açıklar. "
                "At nalı böbrek ve UPJ darlığı gibi staz durumları ise kristal transit süresini uzatarak litogenezi hızlandırır."
            ),
            "flashcards": [
                {
                    "id": "k1-27-cp07-fc01",
                    "front": "İdiyopatik kalsiyum oksalat taşlarının başlangıç yuvası olan Randall plağının kimyasal çekirdeğinde hangi inorganik bileşik yer alır?",
                    "back": "Kalsiyum fosfat türevi olan apatit bileşiğidir.",
                    "hint": "Kemikte de bulunan bazik tuz"
                },
                {
                    "id": "k1-27-cp07-fc02",
                    "front": "Distal RTA ve bruşit taşlarında toplayıcı kanal ağzını intralüminal olarak tıkayan lezyona ne ad verilir?",
                    "back": "Bellini kanal tıkacı lezyonudur.",
                    "hint": "Büyük toplayıcı lümende oluşan engel"
                },
                {
                    "id": "k1-27-cp07-fc03",
                    "front": "Oksalat sitotoksisitesinin renal tübül hücrelerinde membran hasarı ve apoptoz yaratmasında rol oynayan serbest moleküller nelerdir?",
                    "back": "Reaktif oksijen türleridir.",
                    "hint": "Hücre zedelenmesine yol açan serbest radikaller"
                }
            ],
            "elements": [
                make_table(
                    "Checkpoint 7 Özet Tablosu: Randall Plak vs Randall Tıkaç Modelleri",
                    ["Model", "Başlangıç Bölgesi", "Ana Mineral", "İlişkili Klinik Tablo"],
                    [
                        {
                            "cells": ["Randall Plağı", "Henle kulpu bazal membranı", "Apatit (Kalsiyum fosfat)", "İdiyopatik kalsiyum oksalat taşları"],
                            "hiddenIndex": 0,
                            "hint": "Subepitelyal papiller plak"
                        },
                        {
                            "cells": ["Randall Tıkacı", "Bellini kanalı içi (intralüminal)", "Bruşit / Apatit", "Distal RTA, hiperparatiroidi"],
                            "hiddenIndex": 0,
                            "hint": "Toplayıcı lümen içi tıkaç"
                        }
                    ]
                )
            ]
        },
        # Slayt 70
        {
            "slideNumber": 70,
            "title": "Klinik Karar: Endoskopide Randall Plağı Yönetimi",
            "content": (
                "Fleksibl üreterorenoskopi (RIRS) sırasında renal papillalarda yaygın Randall plakları gözlenen bir hastada, "
                "cerrahi işlem bittikten sonra bu plaklara lazer ablasyonu uygulanmamalıdır; çünkü plakları kazımak veya "
                "lazerle yakmak papiller skarlaşmaya ve tübüler fibrozise yol açar. Bunun yerine hastaya agresif medikal profilaksi "
                "planlanmalıdır. İdrar süpersatürasyonu düşürülmeli, kalsiyum oksalatın açıkta kalan plak yüzeyine epitaktik "
                "olarak tutunmasını engellemek için potasyum sitrat ve bol hidrasyon tedavisi verilmelidir."
            ),
            "elements": [
                make_branching_logic(
                    "34 yaşında tekrarlayan kalsiyum oksalat taşı nedeniyle fleksibl URS uygulanan hastanın papillalarında taşın oturduğu geniş subepitelyal Randall plakları görülüyor.",
                    "Bu hastada papiller plakların varlığında cerrahi ve postoperatif izlem için en doğru klinik yaklaşım ne olmalıdır?",
                    [
                        {
                            "text": "Plaklara mekanik/lazer müdahale yapılmamalı, doku travmasından kaçınılmalı ve ameliyat sonrası idrar süpersatürasyonunu düşürecek medikal koruma uygulanmalıdır.",
                            "isCorrect": True,
                            "explanation": "Doğrudur; plakları lazerle kazımak böbrek parankimine hasar verir, medikal profilaksi esastır."
                        },
                        {
                            "text": "Tüm plaklar holmium lazerle tamamen buharlaştırılarak böbrek papillası koterize edilmelidir.",
                            "isCorrect": False,
                            "explanation": "Papiller koterizasyon ciddi skar ve kaliks obstrüksiyonu yapar; kesinlikle kontrendikedir."
                        },
                        {
                            "text": "Hastaya acil nefrektomi planlanmalıdır.",
                            "isCorrect": False,
                            "explanation": "Randall plağı benign bir zemin hazırlayıcıdır, nefrektomi endikasyonu asla oluşturmaz."
                        }
                    ]
                )
            ]
        }
    ]
