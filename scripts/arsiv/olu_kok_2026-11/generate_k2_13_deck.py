# -*- coding: utf-8 -*-
"""Generate deck.json for y25-k2-13-spinal-travmalar."""
import json
import os
import re

deck = {
    "id": "k2p-y25-k2-13-spinal-travmalar",
    "deckId": "k2p-y25-k2-13-spinal-travmalar",
    "title": "Medulla Spinalis Lezyonları ve Spinal Travmalar",
    "shortTitle": "Spinal Travmalar",
    "courseCode": "k2-13",
    "department": "Beyin ve Sinir Cerrahisi",
    "discipline": "Beyin ve Sinir Cerrahisi",
    "committee": "Kurul 2 (Sinir Sistemi ve Hareket)",
    "instructor": "Doç. Dr. Aydın Sinan Apaydın",
    "matchedNoteId": "y25-k2-13-spinal-travmalar",
    "overview": "Omurga biyomekaniği ve fonksiyonel kolon anatomisi, spinal stabilite kriterleri, üst servikal (C0-C2) ve alt servikal (C3-C7) travmaları, Denis üç kolon teorisi ve torakolomber kırıklar, cerrahi dekompresyon ve stabilizasyon endikasyonları ile spinal şok ve acil klinik hasta yönetimi.",
    "highYieldPearls": [
        "📌 [SINAV SPOTU] Jefferson (C1 atlas patlama) kırığında iki lateral kütlenin odontoid üzerinden yana taşma toplamı 7 mm'den fazla ise transvers ligaman kopmuş kabul edilir ve cerrahi stabilizasyon gerekir.",
        "📌 [SINAV SPOTU] Tip II odontoid kırığı dens kaidesindedir; avasküler bölge nedeniyle konservatif tedaviyle %80-90 kaynamaz (psödoartroz) ve ideal tedavisi anterior transodontoid vida fiksasyonudur.",
        "📌 [SINAV SPOTU] Hangman kırığı (aksisin travmatik spondilolistezisi) C2 pars interartikülarislerinin iki taraflı kırığıdır; C2 korpusu öne kayarken arka ark geride kaldığından spinal kanal genişler ve kord basısı nadirdir.",
        "📌 [SINAV SPOTU] Denis sınıflamasında orta kolon (PLL, arka 1/3 korpus ve arka 1/3 anulus) spinal kanal ön duvarını oluşturur; orta kolon tutuluşu omurganın mutlak instabil olduğunu gösterir.",
        "📌 [SINAV SPOTU] Kama kompresyon kırıklarında korpus ön yükseklik kaybı %50'nin altında ve orta kolon sağlamsa konservatif izlenir; %50'yi aşan çökme veya instabil patlama (burst) kırıkları cerrahi endikasyondur.",
        "📌 [SINAV SPOTU] Akut omurilik yaralanmasında spinal şokun bittiğinin en güvenilir klinik göstergesi bulbokavernöz refleksin (S3-S4) geri dönmesidir; bu refleks dönmeden tam kord hasarı teşhisi konulamaz."
    ],
    "kazanimlar": [
        "Omurganın anatomik bölümlerini, korpus ve arka elemanların biyomekanik yük taşıma işlevlerini açıklayabilme",
        "Spinal travma epidemiyolojisini, yaşa göre etyolojik nedenleri ve bölgesel kırık sıklıklarını sayabilme",
        "Spinal stabilite ilkelerini ve travmatik kuvvet vektörlerinin yarattığı hasar paternlerini tanımlayabilme",
        "Üst servikal bölgede oksipital kondil, atlas Jefferson kırığı ve transvers ligaman 7 mm kuralını açıklayabilme",
        "Aksis odontoid ve Hangman kırıklarının sınıflamasını, kaynamama risklerini ve tedavi yaklaşımlarını karşılaştırabilme",
        "Alt servikal omurgada fleksiyon, ekstansiyon, gözyaşı kırıkları ve faset dislokasyonlarının patolojisini ayırt edebilme",
        "Torakolomber bileşkede Denis üç kolon modelini, orta kolonun önemini ve kompresyon ile burst kırıklarını sınıflandırabilme",
        "Spinal travmalarda konservatif takip sınırlarını ve cerrahi dekompresyon ile enstrümantasyon endikasyonlarını belirleyebilme",
        "Akut omurilik hasarında spinal şok ile nörojenik şok arasındaki farkları ve acil yönetim basamaklarını uygulayabilme"
    ],
    "matchedPastQuestionsCount": 0,
    "sayfaHaritasi": "teyitli",
    "totalSlides": 16,
    "slides": []
}

slides_data = [
    # SLIDE 1
    {
        "slideNumber": 1,
        "id": "k2p-y25-k2-13-spinal-travmalar-s01",
        "title": "Omurga Anatomisi: Kolonlar, Biyomekanik ve Kemik Yapı",
        "subtitle": "Omurganın anatomik bölümleri, korpus yapısı, diskler ve omurilik kanalını çevreleyen kemik elemanlar",
        "badge": "Temel Anatomi",
        "bolum": "1",
        "pdfSayfalari": [1, 7],
        "kaynakSayfa": "Slayt 1-7",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 1,
            "endPage": 7
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Omurga anatomisi üç ana bölgede incelenir; 7 servikal, 12 torakal ve 5 lomber omurdan oluşur. Lomber bölgenin hemen altında sakrum ve koksiks kemikleri yer alır.\n\n- **Vertebra Gövdesi:** Korpus, aksiyel mekanik yükün taşınmasında temel rol oynayan sağlam ön yapıdır.\n- **İntervertebral Diskler:** Korpuslar arasında sıralanan esnek diskler gelen darbeleri emen biyomekanik yastıklardır.\n- **Kanal ve Arka Elemanlar:** Gövdenin hemen arkasında omurilik kanalını çevreleyen pediküller ve laminalar uzanır. Faset eklemleri segmental hareketi yönlendirirken, spinöz ve transvers çıkıntılar derin sırt kaslarının tutunmasını sağlar.\n\n> [!NOTE]\n> Vertebra korpusu ana mekanik yük taşıyıcı parçadır; arkasındaki pedikül ve laminalar omurilik için koruyucu kemik kanal halkasını oluşturur.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Vertebra korpusu aksiyel mekanik yükün taşınmasında ana yapıdır; pedikül ve laminalar nöral kanalı çevreler."
        ],
        "medicalTerms": [
            {
                "term": "Vertebra Korpusu",
                "explanation": "Omur kemiğinin ön kısmında yer alan ve aksiyel vücut ağırlığını taşıyan silindirik gövde yapısıdır."
            },
            {
                "term": "Lamina",
                "explanation": "Omurilik kanalının posterior kemik çatısını oluşturan ve pediküllerle birleşen yassı kemik tabakadır."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s01-1",
                "front": "Omurgada aksiyel mekanik yükü taşıyan temel anatomik yapı hangisidir?",
                "back": "Vertebra gövdesi (korpus) yapısıdır.",
                "hint": "Ön sütunu oluşturan silindirik kemik gövde",
                "category": "Anatomi"
            },
            {
                "id": "fc-s01-2",
                "front": "Omurilik kanalının arka kemik çatısını oluşturan yapı nedir?",
                "back": "Lamina kemik yapısıdır.",
                "hint": "Pediküllerle birleşen posterior tabaka",
                "category": "Anatomi"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Omurga biyomekaniğinde aksiyel yükün taşınmasında ana görevi üstlenen ve intervertebral diskler üzerinde sıralanan kemik parça hangisidir?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Vertebra gövdesi (korpus)",
                        "isCorrect": True,
                        "explanation": "Doğru. Vertebra korpusu omurganın anteriorunda aksiyel mekanik yükün taşınmasından sorumlu ana taşıyıcı yapıdır. İntervertebral disklerin üzerine oturarak vücut ağırlığını alt seviyelere dengeli biçimde aktarır."
                    },
                    {
                        "key": "B",
                        "text": "Pedikül ve laminalar",
                        "isCorrect": False,
                        "explanation": "Pedikül ve laminalar omurilik kanalının yan ve arka duvarlarını oluşturan koruyucu kemik kemerlerdir. Bu yapılar nöral dokuyu çevreler ancak aksiyel ağırlığın ana taşıyıcısı değildir."
                    },
                    {
                        "key": "C",
                        "text": "Transvers prosesler",
                        "isCorrect": False,
                        "explanation": "Transvers prosesler omurların iki yanına uzanan ve derin sırt kasları ile bağların tutunduğu kaldıraç kollarıdır. Bu çıkıntılar kas biyomekaniğine katılır fakat doğrudan yük taşıyıcı korpus işlevi görmez."
                    },
                    {
                        "key": "D",
                        "text": "Spinöz çıkıntı",
                        "isCorrect": False,
                        "explanation": "Spinöz çıkıntı posterior hatta yer alan ve ligamentum supraspinale ile kasların yapıştığı arka çıkıntıdır. Bu eleman omurga ekstansiyonunda kaldıraç görevi yapar, ana aksiyel yük korpusta taşınır."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Bir omurga kemiğinde vertebra korpusu ana mekanik yükü taşıyan temel parçadır.",
                "maskedTerm": "korpusu",
                "hint": "Omurun gövde yapısı"
            },
            {
                "type": "interactive_table",
                "tableHeaders": ["Omurga Bölgesi", "Omur Sayısı", "Temel Yapısal Özellik"],
                "tableRows": [
                    {
                        "cells": [
                            {"value": "Servikal", "isMasked": False},
                            {"value": "7 adet", "isMasked": True, "hint": "Boyun segmentindeki kemik adedi"},
                            {"value": "Yüksek kraniyal hareketlilik ve foramen transversarium barındırma", "isMasked": False}
                        ]
                    },
                    {
                        "cells": [
                            {"value": "Torakal", "isMasked": False},
                            {"value": "12 adet", "isMasked": True, "hint": "Sırt segmentindeki kemik adedi"},
                            {"value": "Kostalar ile eklem yaparak rijit göğüs kafesini destekleme", "isMasked": False}
                        ]
                    },
                    {
                        "cells": [
                            {"value": "Lomber", "isMasked": False},
                            {"value": "5 adet", "isMasked": True, "hint": "Bel segmentindeki kemik adedi"},
                            {"value": "En geniş korpus çapı ve yüksek aksiyel yük taşıma", "isMasked": False}
                        ]
                    }
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Omurga Kemik Anatomisi ve Eklem Elemanları",
                "items": [
                    {
                        "text": "Vertebra korpusları arasında yer alan intervertebral diskler esnek yapılarıyla aksiyel mekanik darbeleri sönümler.",
                        "isLie": False,
                        "explanation": "İntervertebral diskler anulus fibrozus ve nukleus pulpozus yapılarıyla aksiyel darbeleri emerek omurları korur."
                    },
                    {
                        "text": "Omurilik kanalının posterior kemik çatısını oluşturan laminalar pediküller aracılığıyla korpusa bağlanır.",
                        "isLie": False,
                        "explanation": "Laminalar ve pediküller birleşerek spinal kanalı çevreleyen koruyucu nöral kemik halkayı tamamlar."
                    },
                    {
                        "text": "Spinal kolonda aksiyel mekanik yükün en büyük kısmını arka elemanlar olan spinöz proses ve laminalar taşır.",
                        "isLie": True,
                        "explanation": "Omurgada aksiyel mekanik yükün ana taşıyıcısı anterior yerleşimli vertebra korpusları ve disklerdir; spinöz prosesler kas tutunma çıkıntılarıdır."
                    }
                ]
            },
            {
                "type": "active_recall",
                "question": "Omurga anatomisinde gövdenin hemen arkasında yer alarak omurilik kanalını çevreleyen temel kemik yapılar nelerdir?",
                "answer": "Omurilik kanalını lateralden pediküller, posteriordan ise laminalar çevreler; bu yapılar nöral arkı ve faset eklemlerini oluşturur."
            }
        ]
    },

    # SLIDE 2
    {
        "slideNumber": 2,
        "id": "k2p-y25-k2-13-spinal-travmalar-s02",
        "title": "Spinal Travmalar: Epidemiyoloji, Etyoloji ve Kırık Dağılımı",
        "subtitle": "Trafik kazaları, düşmeler, spor yaralanmaları ve anatomik bölgelere göre kırık sıklığı",
        "badge": "Epidemiyoloji",
        "bolum": "1",
        "pdfSayfalari": [8, 10],
        "kaynakSayfa": "Slayt 8-10",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 8,
            "endPage": 10
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Spinal travmaların etyolojisi yaş gruplarına göre farklılık gösterir. Genel popülasyonda en sık neden yüzde kırk beş ila elli oranıyla trafik kazalarıdır; bu oran genç erişkinlerde yüzde altmış altıya kadar ulaşır.\n\n- **Düşmeler ve Spor:** Düşmeler yüzde yirmi ila yirmi beş sıklıkla ikinci sırada gelir. Sığ suya balıklama atlama gibi spor yaralanmaları yüzde on beş ila yirmi oranında servikal kırığa yol açar.\n- **Penetran Nedenler:** Ateşli ve delici silah yaralanmaları yüzde on dört civarındadır.\n- **Kırık Bölgeleri:** Kırıklar en sık torakolomber bileşkede (T11-L1) ve alt servikal bölgede (C5-C7) görülür. Üst torakal bölge göğüs kafesi sayesinde daha rijit ve korunaklıdır.\n\n> [!IMPORTANT]\n> Spinal kırıklar mekanik hareketliliğin en yüksek olduğu torakolomber ve alt servikal geçiş bölgelerinde en yüksek sıklıkta meydana gelir.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Spinal travmalarda genel olarak en sık neden trafik kazalarıdır; kırıklar en sık torakolomber ve alt servikalde görülür."
        ],
        "medicalTerms": [
            {
                "term": "Kamçı Yaralanması (Whiplash)",
                "explanation": "Trafik kazalarında ani hızlanma ve yavaşlama kuvvetleriyle boynun hızla fleksiyon ve ekstansiyona uğramasıdır."
            },
            {
                "term": "Torakolomber Bileşke",
                "explanation": "Rijit torakal kafes ile hareketli lomber omurganın birleştiği T11-L1 arasındaki mekanik geçiş bölgesidir."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s02-1",
                "front": "Spinal travmaların genel popülasyonda en sık görülen etyolojik nedeni nedir?",
                "back": "Yüzde kırk beş ila elli sıklıkla trafik kazalarıdır.",
                "hint": "Motorlu taşıt çarpışmaları",
                "category": "Epidemiyoloji"
            },
            {
                "id": "fc-s02-2",
                "front": "Spinal kırıkların anatomik olarak en sık yerleştiği iki omurga bölgesi hangileridir?",
                "back": "Torakolomber bileşke (T11-L1) ve alt servikal omurgadır (C5-C7).",
                "hint": "En hareketli biyomekanik geçiş alanları",
                "category": "Epidemiyoloji"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Spinal travma etyolojisinde genel popülasyonda en sık karşılaşılan birincil etken aşağıdakilerden hangisidir?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Trafik kazaları",
                        "isCorrect": True,
                        "explanation": "Doğru. Trafik kazaları genel popülasyonda omurga yaralanmalarının yüzde kırk beş ila ellisinden sorumludur. Genç grupta bu oran yüzde altmış altı seviyesine kadar çıkarak en sık spinal travma nedeni olur."
                    },
                    {
                        "key": "B",
                        "text": "Ateşli silah yaralanmaları",
                        "isCorrect": False,
                        "explanation": "Ateşli ve delici silah yaralanmaları penetran travmalar grubunda yer alır ve tüm vakaların yaklaşık yüzde on dördünü oluşturur. Önemli bir morbidite kaynağı olsa da en sık etken değildir."
                    },
                    {
                        "key": "C",
                        "text": "İleri yaş osteoporotik düşmeleri",
                        "isCorrect": False,
                        "explanation": "Düşmeler omurga travmalarında yüzde yirmi ila yirmi beş sıklıkla ikinci sırada yer alan önemli bir nedendir. Özellikle yaşlılarda sık görülmekle birlikte genel epidemiyolojide trafik kazalarının gerisindedir."
                    },
                    {
                        "key": "D",
                        "text": "Sığ suya balıklama atlama",
                        "isCorrect": False,
                        "explanation": "Balıklama atlama spor yaralanmaları kapsamında servikal omurga travmalarına yol açan ciddi bir mekanizmadır. Tüm spinal travmalar içindeki payı yüzde on beş ila yirmi arasındadır."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Spinal travma etyolojisinde sığ suya balıklama atlama gibi spor yaralanmaları servikal bölgede ciddi kırıklara yol açar.",
                "maskedTerm": "balıklama",
                "hint": "Sığ suya kafa üstü dalış eylemi"
            },
            {
                "type": "causal_chain",
                "title": "Sığ Suya Balıklama Atlama Travma Mekanizması",
                "steps": [
                    "1. Dalış: Sığ suya baş üstü hızla dalış yapılması",
                    "2. Çarpma: Verteks bölgesinin sert su tabanına yüksek hızla çarpması",
                    "3. Yüklenme: Baş ve boyun bileşkesine şiddetli aksiyel kompresyon kuvveti binmesi",
                    "4. Hasar: Servikal omurlarda kırık ve omurilik sıkışması tablosunun gelişmesi"
                ]
            },
            {
                "type": "swipe_matching",
                "leftCategory": "Yüksek Kırık Sıklığı",
                "rightCategory": "Düşük Kırık Sıklığı",
                "cards": [
                    {"text": "Torakolomber geçiş bölgesi (T11-L1)", "category": "left"},
                    {"text": "Alt servikal hareketli omurga (C5-C7)", "category": "left"},
                    {"text": "Üst torakal rijit kafes omurları (T4-T6)", "category": "right"},
                    {"text": "Sakral ve koksigeal kaynaşmış segmentler", "category": "right"}
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Spinal Travma Etyolojisi ve Bölgesel Kırık Dağılımı",
                "items": [
                    {
                        "text": "Trafik kazaları genç yaş grubundaki spinal travmaların yaklaşık üçte ikisinden sorumludur.",
                        "isLie": False,
                        "explanation": "Genç erişkinlerde trafik kazaları yüzde altmış altı oranıyla spinal travmaların açık ara en sık nedenidir."
                    },
                    {
                        "text": "Üst torakal omurga (T4-T6) kaburga kafesi desteğine rağmen spinal kırıkların en sık görüldüğü bölgedir.",
                        "isLie": True,
                        "explanation": "Torakal kafes stabilite sağladığından kırıklar en sık burada değil, hareketli torakolomber ve alt servikal bölgelerde görülür."
                    },
                    {
                        "text": "Spor yaralanmaları arasında sığ suya dalma aksiyel yüklenmeyle servikal omurga hasarı yaratır.",
                        "isLie": False,
                        "explanation": "Sığ suya kafa üstü atlama vertikal aksiyel kompresyonla servikal omurga kırıklarına ve kord hasarına neden olur."
                    }
                ]
            }
        ]
    },

    # SLIDE 3
    {
        "slideNumber": 3,
        "id": "k2p-y25-k2-13-spinal-travmalar-s03",
        "title": "Spinal Stabilite: Biyomekanik İlkeler ve Travma Kuvvetleri",
        "subtitle": "Stabilite tanımı, fizyolojik yük sınırları ve travmatik kuvvet vektörlerinin sınıflandırılması",
        "badge": "Biyomekanik",
        "bolum": "1",
        "pdfSayfalari": [11, 12],
        "kaynakSayfa": "Slayt 11-12",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 11,
            "endPage": 12
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Spinal stabilite, omurganın normal fizyolojik yükler ve hareketler altında nörolojik hasara veya ağrılı ilerleyici deformiteye yol açmadan bütünlüğünü koruyabilme kapasitesidir. Bu kapasiteyi bozan her türlü yaralanma instabil kabul edilir.\n\n- **Fleksiyon ve Rotasyon:** Öne bükülme fleksiyon, dönme kuvveti rotasyon hasarı doğurur; fleksiyon-rotasyon birlikteliği en yıkıcı instabilite nedenidir.\n- **Aksiyel Kompresyon:** Eksenel ezici kuvvetler korpusta kompresyon ve patlama kırıklarına yol açar.\n- **Ekstansiyon ve Distraksiyon:** Arkaya aşırı gerilme hiperekstansiyon, omurların boyuna birbirinden uzaklaşması ise distraksiyon hasarı yaratır. Penetran travmalar ise dokuları doğrudan parçalar.\n\n> [!NOTE]\n> Fizyolojik sınırlar altındaki normal hareketlerde dahi potansiyel nörolojik hasar riski taşıyan spinal lezyonlar cerrahi açıdan mutlak instabil kabul edilir.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Normal fizyolojik hareketler veya yükler altında nörolojik hasara yol açabilecek her türlü spinal yaralanma instabildir."
        ],
        "medicalTerms": [
            {
                "term": "Spinal İnstabilite",
                "explanation": "Omurganın fizyolojik yükler altında nöral yapıları koruyamayarak ilerleyici deformite veya nörolojik defisit yaratmasıdır."
            },
            {
                "term": "Distraksiyon Hasarı",
                "explanation": "Omurların boyuna eksende birbirinden çekilerek uzaklaşması sonucu ligaman ve disklerin kopmasıdır."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s03-1",
                "front": "Spinal instabilite kavramının temel klinik ve biyomekanik tanımı nedir?",
                "back": "Fizyolojik yük ve hareket altında potansiyel nörolojik hasar veya ilerleyici deformite oluşturabilen durumdur.",
                "hint": "Normal sınırlarda nöral dokuyu koruyamama",
                "category": "Biyomekanik"
            },
            {
                "id": "fc-s03-2",
                "front": "Spinal travmalarda en yıkıcı bağ ve eklem hasarını yaratan bileşik kuvvet vektörü nedir?",
                "back": "Fleksiyon ile rotasyon kuvvetlerinin bir arada bulunmasıdır.",
                "hint": "Bükülme ve dönme birlikteliği",
                "category": "Biyomekanik"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Biyomekanik açıdan fizyolojik sınırdaki yükler altında veya normal omurga hareketleri sırasında nörolojik hasar riski doğuran veya ilerleyici deformiteye neden olan lezyonlar nasıl tanımlanır?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "İnstabil spinal yaralanma",
                        "isCorrect": True,
                        "explanation": "Doğru. Normal fizyolojik hareketler veya yükler altında nörolojik dokuları koruyamayan, ilerleyici açısal deformite veya kayma riski taşıyan her türlü hasar instabil spinal yaralanma olarak tanımlanır."
                    },
                    {
                        "key": "B",
                        "text": "İzole stabil kama kırığı",
                        "isCorrect": False,
                        "explanation": "İzole stabil kama kırığında orta ve arka kolon sağlamdır, omurga fizyolojik yükleri güvenle taşımayı sürdürür. Bu lezyon nörolojik risk barındırmadığı için instabil kabul edilmez."
                    },
                    {
                        "key": "C",
                        "text": "Kronik dejeneratif spondiloz",
                        "isCorrect": False,
                        "explanation": "Kronik dejeneratif spondiloz yaşlanmayla ortaya çıkan disk ve faset eklem kireçlenmesidir. Travmatik akut mekanik instabilite kavramından bütünüyle farklı, yavaş ilerleyen bir süreçtir."
                    },
                    {
                        "key": "D",
                        "text": "Nondeplase faset eklem zorlanması",
                        "isCorrect": False,
                        "explanation": "Nondeplase faset eklem zorlanması yumuşak doku gerilmesidir ve kemik dizilimini bozmaz. Kolon bütünlüğü korunduğu için omurgada nörolojik risk taşıyan instabilite tablosu oluşturmaz."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Spinal travmalarda öne bükülme ve dönme kuvvetlerinin birleştiği fleksiyon-rotasyon birlikteliği en yıkıcı mekanik hasara yol açar.",
                "maskedTerm": "fleksiyon-rotasyon",
                "hint": "Bükülme ve dönme kuvvetlerinin birleşik vektörü"
            },
            {
                "type": "before_after_slider",
                "leftTitle": "Stabil Omurga Biyomekaniği",
                "rightTitle": "İnstabil Omurga Biyomekaniği",
                "leftPoints": [
                    "Normal fizyolojik yükleri ağrısız ve deformitesiz taşır",
                    "Hareket sırasında nörolojik hasar potansiyeli taşımaz",
                    "Ligaman ve kolon bütünlüğü yapısal olarak korunmuştur"
                ],
                "rightPoints": [
                    "Fizyolojik sınırlardaki yük altında dahi patolojik olarak çöker",
                    "Hareketle omurilik veya sinir kökü bası riski doğurur",
                    "Kolon elemanlarında yırtılma veya kemik devamlılığında kayıp vardır"
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Spinal Biyomekanik Kuvvetler ve Stabilite İlkeleri",
                "items": [
                    {
                        "text": "Fizyolojik yük altında omurilik basısı riski doğuran her türlü lezyon instabil kabul edilir.",
                        "isLie": False,
                        "explanation": "Spinal stabilite tanımı gereği nöral hasar veya ağrılı ilerleyici deformite riski taşıyan tüm hasarlar instabildir."
                    },
                    {
                        "text": "Eksenel çekilme ile omurların birbirinden boyuna uzaklaşması distraksiyon hasarı olarak adlandırılır.",
                        "isLie": False,
                        "explanation": "Distraksiyon kuvveti omurga ekseninde boyuna ayrılmaya yol açarak ligamanları ve diskleri yırtar."
                    },
                    {
                        "text": "Fleksiyon ve rotasyon kuvvetlerinin bir arada bulunması ligamanları koruduğundan omurgada en stabil kırık tipini oluşturur.",
                        "isLie": True,
                        "explanation": "Fleksiyon ile rotasyonun birleşmesi ligaman komplekslerini yırtıp fasetleri disloke ederek en yıkıcı ve instabil yaralanmayı doğurur."
                    }
                ]
            },
            {
                "type": "active_recall",
                "question": "Travma mekanizmasında eksenel ezici yüklenme sonucu korpus yüksekliğinde kayıp ve kemik parçalanması yaratan temel kuvvet vektörü nedir?",
                "answer": "Aksiyel kompresyon (aksiyel yüklenme) kuvvetidir; korpusu ezerek kama kompresyon veya patlama kırıklarına neden olur."
            }
        ]
    },

    # SLIDE 4
    {
        "slideNumber": 4,
        "id": "k2p-y25-k2-13-spinal-travmalar-s04",
        "title": "Üst Servikal Travmalar: Oksipital Kondil ve Kraniyoservikal Bileşke",
        "subtitle": "C0, C1 ve C2 bileşke anatomisi, kırık sınıflamaları ve ligamentöz hasar spektrumu",
        "badge": "Kraniyoservikal Bölge",
        "bolum": "2",
        "pdfSayfalari": [13, 18],
        "kaynakSayfa": "Slayt 13-18",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 13,
            "endPage": 18
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Üst servikal omurga C0 (oksipital kondil), C1 (atlas) ve C2 (aksis) anatomik yapılarını kapsar. Bu bölge kraniyoservikal bileşkeyi oluşturarak başın kafa tabanıyla bağlantısını ve geniş hareket açısını sağlar.\n\n- **I. Oksipital Kondil Hasarları:** Tip A izole kondil kırığıdır; Tip B nondeplase ligamentöz hasarı, Tip C ise deplase olan belirgin instabil kırıkları tanımlar.\n- **II. C1 Halka Hasarları:** Tip A izole kemik ark hasarıdır; Tip B transvers ligaman hasarını, Tip C ise atlantoaksiyel instabilite ve rotasyonel dislokasyonu gösterir.\n- **III. C2 ve C2-C3 Hasarları:** Tip A izole kemik kırığıdır; Tip B ligaman veya disk hasarını içerir, Tip C ise herhangi bir düzlemde vertebral kaymayla sonuçlanan instabil hasarları kapsar.\n\n> [!IMPORTANT]\n> Oksipital kondil ve atlas yaralanmalarında Tip C hasarlar deplasman ve rotasyonel instabilite barındırdığından cerrahi fiksasyon gerektirir.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Üst servikal sınıflamada Tip A izole kemik hasarını, Tip B bağ hasarını, Tip C ise deplasman ve instabiliteyi simgeler."
        ],
        "medicalTerms": [
            {
                "term": "Kraniyoservikal Bileşke",
                "explanation": "Oksiput kemiği (C0), atlas (C1) ve aksis (C2) omurlarını içeren kafa tabanı ve boyun geçiş bölgesidir."
            },
            {
                "term": "Transvers Atlantal Ligaman",
                "explanation": "Atlasın lateral kütleleri arasında uzanarak odontoid çıkıntıyı atlas ön arkına sabitleyen ana bağdır."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s04-1",
                "front": "C1 halka ve C1-C2 eklem travma sınıflamasında Tip B hasar neyi ifade eder?",
                "back": "Transvers ligaman hasarını ve ligamentöz yetersizliği ifade eder.",
                "hint": "Atlas stabilitesini sağlayan ana bağın hasarı",
                "category": "Üst Servikal"
            },
            {
                "id": "fc-s04-2",
                "front": "Oksipital kondil ve kraniyoservikal bileşke hasarlarında Tip C evresi ne anlama gelir?",
                "back": "Belirgin instabiliteye yol açan deplase kırık veya bağ hasarını simgeler.",
                "hint": "Yer değiştirmiş instabil hasar",
                "category": "Üst Servikal"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Üst servikal travma sınıflamasında C1 halka ve C1-C2 eklem hasarlarında transvers ligaman kopmasını veya ligamentöz yetersizliği tanımlayan evre hangisidir?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Tip B C1 hasarı",
                        "isCorrect": True,
                        "explanation": "Doğru. C1 halka ve C1-C2 eklem sınıflamasında Tip B doğrudan transvers ligaman hasarını temsil eder. Transvers ligamanın kopması odontoidin geriye kaymasına ve atlantoaksiyel instabiliteye yol açar."
                    },
                    {
                        "key": "B",
                        "text": "Tip A C1 hasarı",
                        "isCorrect": False,
                        "explanation": "Tip A hasar yalnızca izole kemik ark kırığını ifade eder; ligamentöz elemanlar sağlamdır. Transvers ligaman hasarı bu grupta bulunmadığından lezyon genellikle stabil seyreder."
                    },
                    {
                        "key": "C",
                        "text": "Tip C C1 hasarı",
                        "isCorrect": False,
                        "explanation": "Tip C hasar belirgin rotasyonel dislokasyon ve açık instabilite tablosunu tanımlar. Transvers ligaman hasarı Tip B evresinde başlar, Tip C'de ise eklem anatomisi bütünüyle kaymıştır."
                    },
                    {
                        "key": "D",
                        "text": "Tip A C0 kondil hasarı",
                        "isCorrect": False,
                        "explanation": "Tip A C0 hasarı oksipital kondilin izole kemik kırığıdır ve kafa tabanına aittir. C1 atlas halkası veya transvers ligaman anatomisiyle doğrudan ilişkili bir evreleme değildir."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Üst servikal omurgada C1 halka hasarlarında Tip B doğrudan transvers ligaman hasarını gösterir.",
                "maskedTerm": "transvers",
                "hint": "Atlasın iki lateral kütlesi arasında uzanan yatay bağ"
            },
            {
                "type": "interactive_table",
                "tableHeaders": ["Hasar Düzeyi", "Tip A Özelliği", "Tip B Özelliği", "Tip C Özelliği"],
                "tableRows": [
                    {
                        "cells": [
                            {"value": "C0 Oksipital Kondil", "isMasked": False},
                            {"value": "İzole kondil kırığı", "isMasked": False},
                            {"value": "Nondeplase ligamentöz hasar", "isMasked": True, "hint": "Ayrışma göstermeyen anatomik gerilme"},
                            {"value": "Deplase her türlü hasar", "isMasked": False}
                        ]
                    },
                    {
                        "cells": [
                            {"value": "C1 Halka", "isMasked": False},
                            {"value": "İzole kemik ark hasarı", "isMasked": False},
                            {"value": "Transvers ligaman hasarı", "isMasked": True, "hint": "Atlas stabilitesini sağlayan ana bağın kopması"},
                            {"value": "İnstabilite ve rotasyon", "isMasked": False}
                        ]
                    },
                    {
                        "cells": [
                            {"value": "C2 Halka", "isMasked": False},
                            {"value": "Yalnız kemik hasarı", "isMasked": False},
                            {"value": "Ligamentöz veya diskal yaralanma", "isMasked": True, "hint": "Yumuşak doku ve kıkırdak zedelenmesi"},
                            {"value": "Vertebral kaymaya yol açan hasar", "isMasked": False}
                        ]
                    }
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Üst Servikal Kırık ve Bağ Hasarı Sınıflaması",
                "items": [
                    {
                        "text": "Oksipital kondil Tip A kırıkları yer değiştirmemiş izole kemik parçalanmalarıdır.",
                        "isLie": False,
                        "explanation": "Tip A kondil kırığında ligamanlar sağlamdır ve kemik fragmanı ayrışmamış izole bir kırık olarak kalır."
                    },
                    {
                        "text": "C2 halka hasarlarında Tip A evresi disk ve ligaman hasarı içermeyen izole kemik kırığıdır.",
                        "isLie": False,
                        "explanation": "Tip A lezyonlarda tension band, disk veya ligaman hasarı bulunmaz; hasar yalnızca kemik dokuyla sınırlıdır."
                    },
                    {
                        "text": "C1 halka yaralanmalarında transvers ligaman kopması Tip A hasar olarak kabul edilir ve cerrahi risk taşımaz.",
                        "isLie": True,
                        "explanation": "Transvers ligaman hasarı Tip B olarak sınıflandırılır ve atlantoaksiyel instabilite yaratarak cerrahi risk oluşturur."
                    }
                ]
            },
            {
                "type": "active_recall",
                "question": "Üst servikal sınıflamada oksipital kondil ve kraniyoservikal bileşkede deplasman gösteren her türlü hasar hangi evreye girer?",
                "answer": "Tip C hasar evresine girer; belirgin instabiliteye işaret eder."
            }
        ]
    },

    # SLIDE 5 (CHECKPOINT 1)
    {
        "slideNumber": 5,
        "id": "k2p-y25-k2-13-spinal-travmalar-s05",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Omurga Anatomisi, Epidemiyoloji ve Üst Servikal Giriş",
        "subtitle": "İlk dört adımda işlenen omurga biyomekaniği, epidemiyolojik dağılım ve üst servikal sınıflamanın pekiştirilmesi",
        "badge": "Bölüm Tekrarı",
        "bolum": "2",
        "pdfSayfalari": [1, 18],
        "kaynakSayfa": "Slayt 1-18",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 1,
            "endPage": 18
        },
        "isCheckpoint": True,
        "checkpointNumber": 1,
        "isGameFinale": False,
        "synthesisNarrative": "Bu bölümde omurganın temel anatomik elemanlarını, epidemiyolojik sıklıklarını ve üst servikal sınıflama basamaklarını inceledik.\n\n- **Taşıyıcı Biyomekanik:** Aksiyel mekanik yük anterior yerleşimli vertebra korpusları ve intervertebral diskler tarafından taşınır; arkadaki pedikül ve laminalar omurilik kanalını korur.\n- **Epidemiyolojik Dağılım:** Spinal travmalarda trafik kazaları yüzde elli ile en sık etkendir; kırıklar en çok torakolomber ve alt servikal bölgelerde görülür.\n- **Stabilite ve Üst Servikal:** Fizyolojik yük altında nörolojik risk oluşturan her durum instabildir. C0, C1 ve C2 hasarlarında Tip A izole kemik, Tip B ligaman, Tip C ise deplasman ve instabiliteyi simgeler.\n\n> [!NOTE]\n> Omurganın normal fizyolojik sınırlarda nörolojik dokuyu koruyamaması instabilite tanımıdır; üst servikalde Tip C hasarlar bu tablonun en belirgin örneğidir.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Aksiyel yükü korpus taşır; kırıklar en sık T11-L1 ve C5-C7 seviyelerinde görülür.",
            "🚨 [KRİTİK UYARI] Üst servikalde Tip C hasarlar deplasman ve instabiliteyi simgeler."
        ],
        "medicalTerms": [
            {
                "term": "Biyomekanik Yük",
                "explanation": "Vücut ağırlığı ve hareket sırasında omurga üzerine binen mekanik kuvvet vektörlerinin toplamıdır."
            },
            {
                "term": "Atlas Ön Arkı",
                "explanation": "C1 omurunun anteriorunda yer alarak odontoid çıkıntı ile eklem yapan kemik halka parçasıdır."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s05-1",
                "front": "Genel popülasyonda spinal travmaların birinci sıradaki etyolojik nedeni nedir?",
                "back": "Yüzde kırk beş ila elli oranıyla trafik kazalarıdır.",
                "hint": "Motorlu taşıt kazaları",
                "category": "Epidemiyoloji"
            },
            {
                "id": "fc-s05-2",
                "front": "C1 halka hasarlarında Tip B doğrudan hangi anatomik yapının yetersizliğini gösterir?",
                "back": "Transvers ligaman hasarını gösterir.",
                "hint": "Atlas lateral kütlelerini bağlayan bağ",
                "category": "Üst Servikal"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Spinal travma epidemiyolojisi ve biyomekaniği değerlendirildiğinde aşağıdakilerden hangisi doğrudur?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Kırıklar hareketliliğin yüksek olduğu torakolomber ve alt servikal geçiş alanlarında en sıktır",
                        "isCorrect": True,
                        "explanation": "Doğru. Torakolomber (T11-L1) ve alt servikal (C5-C7) segmentler rijit ve mobil bölgelerin kesişiminde yer aldığından mekanik streslere en açık ve en sık kırılan bölgelerdir."
                    },
                    {
                        "key": "B",
                        "text": "Üst torakal omurga göğüs kafesi nedeniyle omurganın kırıklara en duyarlı bölgesidir",
                        "isCorrect": False,
                        "explanation": "Üst torakal omurga sternum ve kostalar tarafından desteklenen rijit bir kafes yapısına sahiptir. Bu koruyucu kemik kafes kırık sıklığını artırmaz, aksine bölgeyi travmalara karşı daha dayanıklı kılar."
                    },
                    {
                        "key": "C",
                        "text": "Genel popülasyonda spinal travmaların en sık nedeni spor yaralanmalarıdır",
                        "isCorrect": False,
                        "explanation": "Genel popülasyonda spinal travmaların birincil nedeni yaklaşık yüzde elli oranıyla trafik kazalarıdır. Spor yaralanmaları önemli olmakla birlikte üçüncü sırada yer alır."
                    },
                    {
                        "key": "D",
                        "text": "Vertebra korpusları aksiyel yük taşımayıp yalnızca kas tutunması için kaldıraç işlevi görür",
                        "isCorrect": False,
                        "explanation": "Vertebra korpusları vücut ağırlığını taşıyan primer aksiyel sütunlardır. Kas tutunması ve kaldıraç kolları korpuslar değil, transvers ve spinöz çıkıntılar tarafından sağlanır."
                    }
                ]
            },
            {
                "type": "feature_bidding",
                "optionA": "Tip A Üst Servikal Hasar",
                "optionB": "Tip C Üst Servikal Hasar",
                "rounds": [
                    {
                        "feature": "Kemik veya eklem elemanlarında herhangi bir yönde deplasman veya kayma varlığı",
                        "correct": "B",
                        "explanation": "Tip C hasarlar belirgin deplasman, rotasyonel kayma veya dislokasyon ile karakterizedir ve ağır instabilite taşır."
                    },
                    {
                        "feature": "Ligamentöz veya diskal yırtılma olmaksızın yalnızca izole kemik hasarı bulunması",
                        "correct": "A",
                        "explanation": "Tip A hasarlarda bağ dokusu, tension band veya disk sağlamdır; hasar izole kemik ark veya kondil çatlağıyla sınırlıdır."
                    }
                ]
            },
            {
                "type": "venn_grid",
                "labelA": "Vertebra Korpusu",
                "labelB": "Arka Elemanlar (Pedikül ve Lamina)",
                "items": [
                    {"criterion": "Aksiyel mekanik yükün taşınmasında ana görevi üstlenme", "correct": "A"},
                    {"criterion": "Omurilik kanalının kemik sınırlarını çevreleyip koruma", "correct": "B"},
                    {"criterion": "Omurga kemik anatomisinin temel bileşenleri arasında yer alma", "correct": "both"},
                    {"criterion": "Kafa tabanıyla eklem yapan C0 oksipital kondil yapısını oluşturma", "correct": "neither"}
                ]
            },
            {
                "type": "swipe_matching",
                "leftCategory": "Tip B Üst Servikal Hasar",
                "rightCategory": "Tip A Üst Servikal Hasar",
                "cards": [
                    {"text": "C1 halkasında transvers ligaman hasarı gelişmesi", "category": "left"},
                    {"text": "C0 oksipital kondilde nondeplase bağ hasarı", "category": "left"},
                    {"text": "C1 atlas arkında izole kemik kırığı oluşması", "category": "right"},
                    {"text": "Oksipital kondilde bağ hasarı içermeyen izole kondil kırığı", "category": "right"}
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Spinal Biyomekanik ve Epidemiyolojik Temeller",
                "items": [
                    {
                        "text": "Normal fizyolojik sınırdaki yükler altında nörolojik hasar yaratabilecek her durum instabildir.",
                        "isLie": False,
                        "explanation": "Spinal instabilite omurganın fizyolojik yükleri güvenle taşıyamayıp nöral yapılara bası riski doğurmasıdır."
                    },
                    {
                        "text": "Servikal bölge 7, torakal bölge 12 ve lomber bölge 5 hareketli omur segmentinden oluşur.",
                        "isLie": False,
                        "explanation": "İnsan omurgasında 7 boyun, 12 sırt ve 5 bel omuru anatomik kolonları oluşturur."
                    },
                    {
                        "text": "Genç yaş grubunda spinal travmaların ana nedeni yüzde altmış altı ile ateşli silah yaralanmalarıdır.",
                        "isLie": True,
                        "explanation": "Genç erişkinlerde omurga travmalarının üçte ikisine trafik kazaları yol açar; ateşli silahlar genel travmaların yaklaşık yüzde on dördüdür."
                    }
                ]
            }
        ]
    },

    # SLIDE 6
    {
        "slideNumber": 6,
        "id": "k2p-y25-k2-13-spinal-travmalar-s06",
        "title": "Atlas (C1) Kırıkları: Jefferson Kırığı ve Aksiyel Yüklenme",
        "subtitle": "Atlas halkasının anatomik yapısı, aksiyel kompresyon mekanizması ve transvers ligaman kuralı",
        "badge": "Üst Servikal Kırıklar",
        "bolum": "3",
        "pdfSayfalari": [19, 19],
        "kaynakSayfa": "Slayt 19",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 19,
            "endPage": 19
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Atlas (C1) omuru korpusa sahip olmayıp anterior ve posterior arklardan oluşan bir kemik halkadır. Başın tepesine gelen yüksek enerjili aksiyel yüklenme sonucunda oksipital kondiller atlasın lateral kütlelerini iki yana doğru iter.\n\n- **Jefferson Kırığı:** Atlas halkasının hem ön hem arka arklarında meydana gelen dört parçalı patlama kırığıdır.\n- **Transvers Ligaman Yetersizliği:** Yana açılan artiküler kütleler transvers ligamanı gerer; bu bağın yetersizliği atlantoaksiyel instabiliteye yol açar.\n- **Yedi Milimetre Kuralı:** Radyografide iki lateral kütlenin odontoid üzerinden yana taşma mesafelerinin toplamı 7 mm'den fazla ise transvers ligaman kopmuş kabul edilir ve cerrahi gündeme gelir.\n\n> [!IMPORTANT]\n> Lateral kütlelerin toplam yana taşma miktarı 7 mm ve üzerinde ise transvers ligaman rüptüre kabul edilir; 7 mm altında konservatif eksternal tespit tercih edilir.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Jefferson kırığında lateral kütlelerin yana taşma toplamı 7 mm'den fazla ise transvers ligaman kopmuş kabul edilir."
        ],
        "medicalTerms": [
            {
                "term": "Jefferson Kırığı",
                "explanation": "Baş tepesine gelen aksiyel kompresyonla C1 atlas halkasının ön ve arka arklardan patlamasıdır."
            },
            {
                "term": "Lateral Kütle Taşması",
                "explanation": "Atlas lateral eklem parçalarının aksisin odontoid çıkıntısına göre dışa doğru kayma mesafesidir."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s06-1",
                "front": "Jefferson kırığının ortaya çıkmasına yol açan primer biyomekanik kuvvet nedir?",
                "back": "Baş tepesine gelen yüksek enerjili aksiyel kompresyon (aksiyel yüklenme) kuvvetidir.",
                "hint": "Düşey eksenel sıkışma",
                "category": "Üst Servikal Kırıklar"
            },
            {
                "id": "fc-s06-2",
                "front": "Jefferson kırığında transvers ligamanın koptuğunu kanıtlayan radyolojik taşma eşiği nedir?",
                "back": "Lateral kütlelerin yana taşma mesafeleri toplamının 7 mm'den fazla olmasıdır.",
                "hint": "Yedi milimetre kuralı",
                "category": "Üst Servikal Kırıklar"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Jefferson (C1 atlas patlama) kırığında transvers ligamanın tamamen koptuğunu ve cerrahi stabilizasyon endikasyonu doğduğunu gösteren radyolojik kriter hangisidir?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "İki taraflı lateral kütlelerin odontoid üzerinden yana taşma toplamının 7 mm'den fazla olması",
                        "isCorrect": True,
                        "explanation": "Doğru. Açık ağız odontoid grafisinde veya tomografide atlas lateral kütlelerinin odontoid üzerinden iki yana taşma toplamı yedi milimetreyi aştığında transvers ligaman rüptüre kabul edilir ve cerrahi gerekir."
                    },
                    {
                        "key": "B",
                        "text": "C1 anterior ark kırık ayrışmasının 2 mm sınırını geçmesi",
                        "isCorrect": False,
                        "explanation": "Anterior ark ayrışması tek başına ligaman kopmasını belirlemez. İnstabilite ve transvers ligaman rüptürü lateral kütlelerin dışa taşma toplamının yedi milimetreyi aşmasıyla tanımlanır."
                    },
                    {
                        "key": "C",
                        "text": "Oksipital kondillerde izole Tip A kemik fissürü bulunması",
                        "isCorrect": False,
                        "explanation": "Oksipital kondildeki izole Tip A kırık kafa tabanı yaralanmasıdır. Bu lezyon atlas halkasının lateral kütle ayrışmasını veya transvers ligaman kopmasını göstermez."
                    },
                    {
                        "key": "D",
                        "text": "C2 korpusunda öne doğru 3 mm'den az translasyon görülmesi",
                        "isCorrect": False,
                        "explanation": "C2 korpusundaki 3 mm'den az translasyon Hangman Tip I kırığının kriteridir. Jefferson kırığı C1 halkasına aittir ve lateral kütle taşma toplamıyla değerlendirilir."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Atlas patlama kırığında lateral kütlelerin toplam yana taşma mesafesi yedi milimetreyi aştığında transvers ligaman kopmuş kabul edilir.",
                "maskedTerm": "milimetreyi",
                "hint": "Mesafe ölçümünde kullanılan metrik birim"
            },
            {
                "type": "branching_logic",
                "scenario": "Sığ havuza balıklama atlayan 24 yaşındaki hasta boyun ağrısıyla getiriliyor. Nörolojik muayenesi doğaldır. BT incelemesinde C1 halkasında dört parçalı Jefferson kırığı saptanıyor ve iki lateral kütlenin yana taşma toplamı 9 mm olarak ölçülüyor.",
                "options": [
                    {
                        "text": "Transvers ligaman kopmuş kabul edilerek cerrahi stabilizasyon planlanması",
                        "isCorrect": True,
                        "feedback": "Doğru karar. Lateral kütlelerin toplam taşması yedi milimetreyi aştığı için transvers ligaman rüptüre kabul edilir; instabilite nedeniyle cerrahi stabilizasyon endikasyonu vardır."
                    },
                    {
                        "text": "Nörolojik defisit bulunmadığı gerekçesiyle yalnızca basit yumuşak boyunlukla taburcu edilmesi",
                        "isCorrect": False,
                        "feedback": "Hatalı yaklaşım. Dokuz milimetrelik lateral kütle taşması ağır ligamentöz yetersizliğe işaret eder. Basit boyunluk instabiliteyi önleyemez ve ölümcül atlantoaksiyel dislokasyona zemin hazırlar."
                    }
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Atlas (C1) Anatomisi ve Jefferson Kırığı İlkeleri",
                "items": [
                    {
                        "text": "Atlas omurunun anatomisinde korpus bulunmaz; ön ve arka kemik arklardan oluşur.",
                        "isLie": False,
                        "explanation": "Atlas vertebra cismi barındırmaz, korpusa ait yapı aksisin odontoid çıkıntısı olarak gelişir."
                    },
                    {
                        "text": "Jefferson kırığı baş tepesine gelen yüksek enerjili aksiyel kompresyon kuvvetiyle meydana gelir.",
                        "isLie": False,
                        "explanation": "Aksiyel yüklenme oksipital kondilleri bir kama gibi atlas lateral kütlelerinin arasına sokarak halkayı patlatır."
                    },
                    {
                        "text": "Lateral kütle taşma toplamı 4 mm olan bir hastada transvers ligaman kesinlikle rüptüre kabul edilir ve acil cerrahi uygulanır.",
                        "isLie": True,
                        "explanation": "Transvers ligaman rüptürü için eşik değer 7 milimetredir; 7 mm altındaki taşmalarda bağ sağlam kabul edilir ve konservatif tedavi uygulanır."
                    }
                ]
            },
            {
                "type": "active_recall",
                "question": "Jefferson patlama kırığının temel biyomekanik oluşum mekanizması nedir?",
                "answer": "Baş tepesine gelen vertikal aksiyel kompresyon kuvvetinin oksipital kondiller aracılığıyla C1 lateral kütlelerini iki yana doğru itmesidir."
            }
        ]
    },

    # SLIDE 7
    {
        "slideNumber": 7,
        "id": "k2p-y25-k2-13-spinal-travmalar-s07",
        "title": "Aksis (C2) Kırıkları: Odontoid Fraktürleri ve Tedavi Yaklaşımı",
        "subtitle": "Anderson-D'Alonzo sınıflaması, Tip II psödoartroz riski ve anterior vida fiksasyonu",
        "badge": "Üst Servikal Kırıklar",
        "bolum": "3",
        "pdfSayfalari": [20, 22],
        "kaynakSayfa": "Slayt 20-22",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 20,
            "endPage": 22
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Aksis (C2) omurunun odontoid çıkıntısı (dens), C1 atlas halkası içinde dönme hareketinin eksenini oluşturur. Odontoid kırıkları Anderson-D'Alonzo sınıflamasıyla değerlendirilir.\n\n- **Tip I:** Odontoid apeksinde alar ligaman avulsiyon kırığıdır; stabildir ve konservatif iyileşir.\n- **Tip II:** Odontoid kaidesinde gelişen kırıktır. Kanlanması zayıf olduğundan yüzde seksen ila doksan oranında konservatif tedaviyle iyileşmez (psödoartroz riski). Hastaların çoğu nörolojik olarak normaldir; tedavisi transodontoid vida ile fiksasyondur.\n- **Tip III:** Kırık hattı kaideyi aşarak C2 vertebra cismine uzanır; spongiyöz kemik kanlanması iyi olduğundan konservatif takiple başarıyla kaynar.\n- **Tip III-A:** Kaidede parçalı kırık vardır; Tip II gibi yüksek instabilite taşır.\n\n> [!NOTE]\n> Tip II odontoid kırıklarında hastanın nörolojisi sıklıkla sağlamdır; ancak kanlanma yetersizliği nedeniyle kaynamama riski çok yüksek olduğundan cerrahi vida fiksasyonu mekanik ideal çözümdür.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Tip II odontoid kırığı dens kaidesindedir; %80-90 psödoartroz riski nedeniyle transodontoid vida fiksasyonu gerektirir."
        ],
        "medicalTerms": [
            {
                "term": "Psödoartroz",
                "explanation": "Kırık uçlarının kemikleşmeyerek fibröz bağ dokusuyla yalancı eklem oluşturması ve kaynamamasıdır."
            },
            {
                "term": "Transodontoid Vida",
                "explanation": "C2 korpusundan odontoid apeksine doğru anterior yaklaşımla yerleştirilen kemik fiksasyon vidasıdır."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s07-1",
                "front": "Odontoid kırıkları sınıflamasında konservatif tedaviyle %80-90 oranında kaynamayan tip hangisidir?",
                "back": "Tip II odontoid kırığıdır (kaide kırığı).",
                "hint": "Dens kaidesindeki avasküler kırık",
                "category": "Üst Servikal Kırıklar"
            },
            {
                "id": "fc-s07-2",
                "front": "Tip III odontoid kırığının konservatif tedaviyle başarıyla iyileşmesinin temel sebebi nedir?",
                "back": "Kırık hattının zengin kanlanan C2 spongiyöz korpus kemiğine uzanmasıdır.",
                "hint": "Geniş spongiyöz korpus kemik yüzeyi",
                "category": "Üst Servikal Kırıklar"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Anderson-D'Alonzo sınıflamasında odontoid kaidesinden geçen, avasküler yapısı nedeniyle konservatif tedaviyle yüzde seksen ila doksan kaynamayan ve ideal tedavisi transodontoid vida fiksasyonu olan kırık tipi hangisidir?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Tip II odontoid kırığı",
                        "isCorrect": True,
                        "explanation": "Doğru. Tip II odontoid kırığı dens kaidesinden geçer. Besleyici damar ağının zayıflığı nedeniyle konservatif izlemde yüzde seksen ila doksan psödoartroz gelişir; transodontoid vida ile fiksasyon ideal anatomik tedavidir."
                    },
                    {
                        "key": "B",
                        "text": "Tip I odontoid kırığı",
                        "isCorrect": False,
                        "explanation": "Tip I kırık odontoidin tepe noktasında alar bağın çekmesine bağlı avulsiyondur. Kemik tabanı sağlam kaldığından stabildir ve konservatif eksternal immobilizasyonla hızla iyileşir."
                    },
                    {
                        "key": "C",
                        "text": "Tip III odontoid kırığı",
                        "isCorrect": False,
                        "explanation": "Tip III kırık hattı geniş C2 korpusu kemik iliğine uzanır. Spongiyöz kemiğin kanlanması zengin olduğundan konservatif boyunluk veya halo tespitiyle yüksek oranda kaynama sağlanır."
                    },
                    {
                        "key": "D",
                        "text": "Jefferson atlas patlama kırığı",
                        "isCorrect": False,
                        "explanation": "Jefferson kırığı C1 atlas halkasının dört parçalı patlama kırığıdır. Aksis odontoid çıkıntısıyla ilgili bir patoloji olmayıp aksiyel yüklenmeyle C1 lateral kütlelerinde gelişir."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Tip II odontoid kırıklarında kaide kemiğinin kanlanması zayıf olduğundan transodontoid vida ile fiksasyon mekanik açıdan ideal çözümdür.",
                "maskedTerm": "transodontoid",
                "hint": "Dens kemiğinin içinden geçen vida yerleştirme tekniği"
            },
            {
                "type": "before_after_slider",
                "leftTitle": "Tip II Odontoid Kırığı",
                "rightTitle": "Tip III Odontoid Kırığı",
                "leftPoints": [
                    "Kırık hattı dar odontoid kaidesindedir",
                    "Bölgesel kanlanma zayıftır ve psödoartroz sıktır",
                    "Yüzde seksen ila doksan cerrahi vida fiksasyonu gerektirir"
                ],
                "rightPoints": [
                    "Kırık hattı geniş C2 vertebra cismi içine uzanır",
                    "Spongiyöz kemik kanlanması zengindir ve kaynama hızlıdır",
                    "Konservatif eksternal tespit ile başarıyla iyileşir"
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Aksis Odontoid Kırıkları ve Klinik Yaklaşım",
                "items": [
                    {
                        "text": "Tip I odontoid kırığı dens tepe noktasında gelişen stabil bir avulsiyon kırığıdır.",
                        "isLie": False,
                        "explanation": "Alar ligamanın çekmesine bağlı apeks avulsiyonudur ve konservatif immobilizasyonla sorunsuz kaynar."
                    },
                    {
                        "text": "Tip II odontoid kırığı olan hastaların büyük bir kısmı acil servise nörolojik muayenesi tamamen normal olarak başvurur.",
                        "isLie": False,
                        "explanation": "Spinal kanal bu seviyede geniş olduğundan hastaların çoğunda belirgin kord basısı ve nörolojik defisit görülmez."
                    },
                    {
                        "text": "Tip III odontoid kırıkları vertebra korpusuna uzandığı için kaynamaz ve mutlaka posterior füzyon ameliyatı gerektirir.",
                        "isLie": True,
                        "explanation": "Tip III kırıklar geniş ve iyi kanlanan spongiyöz C2 gövdesine uzandığı için konservatif eksternal tespit ile yüksek oranda kaynar."
                    }
                ]
            },
            {
                "type": "active_recall",
                "question": "Tip II odontoid kırıklarının konservatif tedavi ile yüzde 80-90 oranında iyileşmemesinin temel biyolojik nedeni nedir?",
                "answer": "Odontoid kaidesinin avasküler olması ve besleyici kan akımının yetersiz kalması sonucu psödoartroz (kaynamama) gelişmesidir."
            }
        ]
    },

    # SLIDE 8
    {
        "slideNumber": 8,
        "id": "k2p-y25-k2-13-spinal-travmalar-s08",
        "title": "Aksis (C2) Kırıkları: Hangman Kırığı ve Travmatik Spondilolistezis",
        "subtitle": "Pars interartikülaris kırığı, hiperekstansiyon mekanizması ve Effendi evrelemesi",
        "badge": "Üst Servikal Kırıklar",
        "bolum": "3",
        "pdfSayfalari": [23, 27],
        "kaynakSayfa": "Slayt 23-27",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 23,
            "endPage": 27
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Asılan adam kırığı (Hangman fraktürü), aksis omurunun travmatik spondilolistezisidir. Genellikle trafik kazasında çenenin çarpması veya ası travmasında olduğu gibi hiperekstansiyon ve aksiyel yüklenme kuvvetleriyle oluşur.\n\n- **Patolojik Anatomi:** C2 pars interartikülarisleri iki taraflı kırılır; C2 korpusu öne doğru kayarken arka ark elemanları geride kalır. Spinal kanal genişlediği için kord basısı seyrektir.\n- **Tip I:** Fragmanlar arasında 3 mm'den az ayrılma vardır, açılanma yoktur; stabildir.\n- **Tip II:** Kırık ayrışması 3 mm'den fazladır ve öne açılanma (dislokasyon) mevcuttur; instabildir.\n- **Tip III:** Pars kırığına iki taraflı faset eklem dislokasyonu eşlik eder; ileri derecede instabildir.\n\n> [!IMPORTANT]\n> Hangman kırığında pars kırığı nedeniyle nöral ark korpustan ayrıldığından spinal kanal genişler; bu durum nörolojik defisit tablosunu hafifletir.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Hangman kırığı C2 pars interartikülarislerinin iki taraflı kırığıdır; spinal kanal genişlediğinden nörolojik bası nadirdir."
        ],
        "medicalTerms": [
            {
                "term": "Travmatik Spondilolistezis",
                "explanation": "Akut travma sonucu C2 vertebra korpusunun pars kırığı zemininde C3 üzerinde öne doğru kaymasıdır."
            },
            {
                "term": "Pars İnterartikülaris",
                "explanation": "Üst ve alt faset eklemleri arasında yer alan dar kemik istmus anatomik köprüsüdür."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s08-1",
                "front": "Hangman kırığında kırılan temel anatomik kemik yapı hangisidir?",
                "back": "C2 aksis omurunun iki taraflı pars interartikülarisleridir.",
                "hint": "Fasetler arası kemik istmus",
                "category": "Üst Servikal Kırıklar"
            },
            {
                "id": "fc-s08-2",
                "front": "Hangman kırığı Tip II'yi Tip I'den ayıran radyolojik deplasman eşiği nedir?",
                "back": "Kırık uçları arasında 3 mm'den fazla ayrılma ve öne açılanma olmasıdır.",
                "hint": "Üç milimetreden fazla ayrışma",
                "category": "Üst Servikal Kırıklar"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Aksisin travmatik spondilolistezisinde (Hangman kırığı) C2 korpusunun öne doğru 3 mm'den fazla ayrıldığı ve belirgin açılanma gösterdiği kırık evresi hangisidir?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Tip II Hangman kırığı",
                        "isCorrect": True,
                        "explanation": "Doğru. Tip II Hangman kırığında kırık uçları arasında üç milimetreden fazla ayrışma ve C2 korpusunda öne açılanma mevcuttur. C2-C3 ligaman hasarı eşlik ettiğinden instabil kabul edilir."
                    },
                    {
                        "key": "B",
                        "text": "Tip I Hangman kırığı",
                        "isCorrect": False,
                        "explanation": "Tip I Hangman kırığında ayrışma üç milimetrenin altındadır ve öne açılanma bulunmaz. Kolon stabilitesi büyük oranda korunduğundan konservatif rijit boyunlukla takip edilir."
                    },
                    {
                        "key": "C",
                        "text": "Tip III Hangman kırığı",
                        "isCorrect": False,
                        "explanation": "Tip III Hangman kırığında pars kırığına ek olarak iki taraflı kilitli faset dislokasyonu bulunur. En ağır instabilite formudur ve redüksiyon cerrahisi gerektirir."
                    },
                    {
                        "key": "D",
                        "text": "Tip I Odontoid kırığı",
                        "isCorrect": False,
                        "explanation": "Tip I odontoid kırığı odontoid tepe noktasında alar bağın çekmesiyle oluşan stabil bir avulsiyondur. Bu patoloji C2 aksis korpusunun pars kırıklarından bütünüyle farklı bir anatomik bölgeye aittir."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Asılan adam kırığında C2 omurunun pars interartikülarisleri iki taraflı kırılarak korpusun öne kaymasına yol açar.",
                "maskedTerm": "interartikülarisleri",
                "hint": "Faset eklemleri arasındaki dar kemik istmus parçası"
            },
            {
                "type": "causal_chain",
                "title": "Hangman Kırığı ve Biyomekanik Ayrışma Mekanizması",
                "steps": [
                    "1. Darbe: Çene altına gelen ani hiperekstansiyon ve aksiyel kuvvet",
                    "2. Makaslama: C2 pars interartikülaris kemik istmuslarına aşırı gerilim binmesi",
                    "3. Kırılma: Pars interartikülarislerin iki taraflı olarak kemik bütünlüğünü kaybetmesi",
                    "4. Translasyon: C2 korpusunun öne doğru kayarken arka ark elemanlarının arkada kalması"
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Aksis Travmatik Spondilolistezisi (Hangman) Özellikleri",
                "items": [
                    {
                        "text": "Hangman kırığı iki taraflı C2 pars interartikülaris kırığı sonucu gelişir.",
                        "isLie": False,
                        "explanation": "Tanım gereği travmatik spondilolistezis aksis pars kemik yapısının iki taraflı kırılmasıdır."
                    },
                    {
                        "text": "Tip III Hangman kırığında pars kırığına iki taraflı faset dislokasyonu eşlik eder.",
                        "isLie": False,
                        "explanation": "Tip III en ağır evredir ve faset eklem kilitlenmesiyle birlikte tam mekanik instabilite yaratır."
                    },
                    {
                        "text": "Hangman kırığında C2 korpusunun öne kayması spinal kanalı hemen daraltarak hastaların tamamında ani kuadriplejiye yol açar.",
                        "isLie": True,
                        "explanation": "Arka elemanlar geride kaldığı için spinal kanal öne kaymada daralmaz, aksine genişler; kord basısı bu nedenle nadirdir."
                    }
                ]
            },
            {
                "type": "active_recall",
                "question": "Hangman kırığında Tip I ile Tip II evrelerini birbirinden ayıran temel radyolojik ölçüm kriteri nedir?",
                "answer": "Kırık kemik uçları arasındaki ayrılmanın 3 mm'den az (Tip I) veya 3 mm'den fazla olup açılanma göstermesi (Tip II) kriteridir."
            }
        ]
    },

    # SLIDE 9
    {
        "slideNumber": 9,
        "id": "k2p-y25-k2-13-spinal-travmalar-s09",
        "title": "Alt Servikal Spinal Travmalar: Fleksiyon, Ekstansiyon ve Teardrop Kırıkları",
        "subtitle": "C3-C7 biyomekaniği, bağ hasarları, faset subluksasyonu ve travmatik disk hernisi",
        "badge": "Alt Servikal Travmalar",
        "bolum": "4",
        "pdfSayfalari": [28, 34],
        "kaynakSayfa": "Slayt 28-34",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 28,
            "endPage": 34
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Alt servikal omurga (C3-C7), yüksek hareketliliği nedeniyle travmatik kuvvetlerden en fazla etkilenen bölgeler arasındadır. Hasar paterni travma mekanizmasına göre şekillenir.\n\n- **Fleksiyon Travmaları:** Vertebra korpusunda kama tipi kompresyon kırığı oluşturur. Posterior longitudinal ligaman (PLL) ve interspinöz bağlar yırtılır; posterior disk aralığı açılarak travmatik disk hernisi gelişebilir. Tek veya çift taraflı faset dislokasyonu kord miyelomalizisine yol açabilir.\n- **Ekstansiyon Travmaları:** Anterior longitudinal ligaman (ALL) yırtılır; korpusun ön-alt köşesinde gözyaşı (teardrop) kırığı meydana gelir ve posterior kemik elemanlar sıkışır.\n- **Aksiyel Yüklenme:** Korpusun patlamasına (burst kırığı) ve spinal kanala kemik fragman kaymasına neden olur.\n\n> [!IMPORTANT]\n> Hiperfleksiyon hasarında faset eklem dislokasyonu ve travmatik disk herniasyonu omurilik basısı yaratarak miyelomalizi ve nörolojik defisit doğurabilir.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Hiperfleksiyonda PLL ve interspinöz ligaman yırtılır, disk hernisi gelişir; hiperekstansiyonda ise ALL yırtılır ve teardrop kırığı oluşur."
        ],
        "medicalTerms": [
            {
                "term": "Gözyaşı (Teardrop) Kırığı",
                "explanation": "Vertebra korpusunun antero-inferior köşesinden üçgen biçimli kemik parçanın kopmasıdır."
            },
            {
                "term": "Miyelomalizi",
                "explanation": "Travmatik bası ve iskemi sonucu omurilik parankiminde gelişen nekrotik yumuşama ve doku hasarıdır."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s09-1",
                "front": "Alt servikal omurgada hiperekstansiyon yaralanmasında birincil olarak yırtılan ligaman hangisidir?",
                "back": "Anterior longitudinal ligamandir (ALL).",
                "hint": "Omurga ön yüzeyini boylu boyunca kaplayan bağ",
                "category": "Alt Servikal Travmalar"
            },
            {
                "id": "fc-s09-2",
                "front": "Alt servikal hiperfleksiyon travmasında posterior disk aralığının açılması hangi akut lezyona yol açabilir?",
                "back": "Travmatik disk herniasyonuna ve kord basısına yol açabilir.",
                "hint": "Omurilik kanalına disk fıtıklaşması",
                "category": "Alt Servikal Travmalar"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Alt servikal omurgada hiperfleksiyon travması geçiren bir hastada patofizyolojik olarak hangi anatomik lezyonun gelişmesi beklenir?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Posterior longitudinal ligaman yırtılması ve travmatik disk herniasyonu",
                        "isCorrect": True,
                        "explanation": "Doğru. Hiperfleksiyon omurganın arka elemanlarını gererek posterior longitudinal ligamanı ve interspinöz bağları yırtar. Arka disk mesafesi genişleyerek travmatik disk herniasyonuna ve faset subluksasyonuna yol açar."
                    },
                    {
                        "key": "B",
                        "text": "Anterior longitudinal ligaman rüptürü ve ekstansiyon teardrop kırığı",
                        "isCorrect": False,
                        "explanation": "Anterior longitudinal ligaman rüptürü ve ön köşe teardrop kırığı hiperekstansiyon yaralanmalarında gerilmeye bağlı gelişir. Bu lezyonlar omurganın arkaya zorlanmasıyla ortaya çıkar; hiperfleksiyon kuvvetlerinde ise posterior ligaman kompleksi hasar görür."
                    },
                    {
                        "key": "C",
                        "text": "Oksipital kondil Tip A izole kafa tabanı kırığı",
                        "isCorrect": False,
                        "explanation": "Oksipital kondil kırığı kafa tabanı ve C0 seviyesine ait bir üst servikal hasardır. C3-C7 alt servikal hiperfleksiyon lezyonları kapsamında yer almaz."
                    },
                    {
                        "key": "D",
                        "text": "Atlas lateral kütlelerinin dışa doğru 9 mm taşması",
                        "isCorrect": False,
                        "explanation": "Atlas lateral kütlelerinin dışa taşması C1 Jefferson kırığının aksiyel kompresyon bulgusudur. Alt servikal omurganın fleksiyon veya ekstansiyon hasarlarıyla ilişkili değildir."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Alt servikal omurgada şiddetli hiperekstansiyon travması anterior longitudinal ligamanın yırtılmasına yol açar.",
                "maskedTerm": "longitudinal",
                "hint": "Omurganın ön yüzü boyunca boylu boyunca uzanan bağın anatomik yönü"
            },
            {
                "type": "swipe_matching",
                "leftCategory": "Fleksiyon Mekanizması",
                "rightCategory": "Ekstansiyon Mekanizması",
                "cards": [
                    {"text": "Posterior longitudinal ligaman ve interspinöz bağ yırtılması", "category": "left"},
                    {"text": "Posterior disk mesafesinde genişleme ve travmatik disk hernisi", "category": "left"},
                    {"text": "Anterior longitudinal ligaman rüptürü ve gözyaşı (teardrop) kırığı", "category": "right"},
                    {"text": "Spinöz proses ve arka kemik elemanlarda ezilme kırıkları", "category": "right"}
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Alt Servikal Travma Mekanizmaları ve Radyoloji",
                "items": [
                    {
                        "text": "Fleksiyon travmalarında vertebra korpusunun ön kısmında kama tipi kompresyon gelişebilir.",
                        "isLie": False,
                        "explanation": "Öne bükülme aksiyel yükü korpusun ön kenarına bindirerek kama şeklinde çökme kırığı yaratır."
                    },
                    {
                        "text": "Hiperfleksiyona bağlı C5-C6 dislokasyonlarında omurilik ezilerek MRG'de miyelomalizi saptanabilir.",
                        "isLie": False,
                        "explanation": "Faset dislokasyonu spinal kanalı daraltarak kord basısına ve parankimde miyelomaliziye neden olur."
                    },
                    {
                        "text": "Hiperekstansiyon travmalarında gerilmeye maruz kalan ana yapı posterior longitudinal ligamandir ve bu bağ kopar.",
                        "isLie": True,
                        "explanation": "Hiperekstansiyonda ön taraf gerilir ve anterior longitudinal ligaman yırtılır; posterior ligamanlar ise fleksiyon kuvvetinde gerilip kopar."
                    }
                ]
            },
            {
                "type": "active_recall",
                "question": "Alt servikal omurgada hiperfleksiyon ve subluksasyon sonrasında omurilik dokusunda gelişen parankimal hasar MRG'de hangi terimle ifade edilir?",
                "answer": "Spinal kord miyelomalizisi (veya miyelopati/kord ödemi) olarak adlandırılır."
            }
        ]
    },

    # SLIDE 10 (CHECKPOINT 2)
    {
        "slideNumber": 10,
        "id": "k2p-y25-k2-13-spinal-travmalar-s10",
        "title": "[TEKRAR SAYFASI - CHECKPOINT 2] C1-C2 Özel Kırıkları ve Alt Servikal Travmalar",
        "subtitle": "Atlas, aksis ve alt servikal omurga kırıklarının patolojileri ve radyolojik ayrımı",
        "badge": "Bölüm Tekrarı",
        "bolum": "4",
        "pdfSayfalari": [19, 34],
        "kaynakSayfa": "Slayt 19-34",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 19,
            "endPage": 34
        },
        "isCheckpoint": True,
        "checkpointNumber": 2,
        "isGameFinale": False,
        "synthesisNarrative": "Bu bölümde servikal omurganın kendine özgü kırık tiplerini ve ligamentöz hasar mekanizmalarını inceledik.\n\n- **Atlas ve Aksis:** C1 Jefferson kırığında lateral kütle taşma toplamı 7 mm'yi aştığında transvers ligaman kopmuş kabul edilir. C2 odontoid Tip II kırıklarında avasküler kaide nedeniyle kaynamama riski yüksektir ve vida fiksasyonu uygulanır.\n- **Hangman ve Alt Servikal:** C2 Hangman kırığı hiperekstansiyonla pars interartikülarislerin kırılmasıdır; spinal kanal genişlediği için kord hasarı nadirdir. Alt servikalde fleksiyon PLL ve disk hasarı yaparken, ekstansiyon ALL yırtığı ve teardrop kırığı doğurur.\n\n> [!NOTE]\n> Odontoid Tip II kırıkları ile Jefferson kırığında 7 mm üzeri ayrışmalar ligamentöz ve vasküler yetersizlik nedeniyle cerrahi fiksasyon gerektiren yüksek riskli tablolardır.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Tip II odontoid kaide kırığı kaynamaz (%80-90 psödoartroz); Jefferson kırığında cerrahi sınır 7 mm'dir.",
            "🚨 [KRİTİK UYARI] Hangman kırığında pars kırığı nöral kanalı genişletir; kord basısı bu nedenle nadirdir."
        ],
        "medicalTerms": [
            {
                "term": "Hangman Fraktürü",
                "explanation": "Aksis omurunun pars interartikülarislerinin hiperekstansiyon sonucu iki taraflı kırılmasıdır."
            },
            {
                "term": "Faset Kilitlenmesi",
                "explanation": "Hiperfleksiyonla alt eklem çıkıntısının üst eklem çıkıntısının önüne kayarak takılmasıdır."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s10-1",
                "front": "Tip II odontoid kırığı ile Tip III odontoid kırığı arasındaki temel anatomik ve prognoz farkı nedir?",
                "back": "Tip II avasküler kaidededir ve kaynamaz; Tip III iyi kanlanan korpusa uzanır ve konservatif kaynar.",
                "hint": "Kaide vs korpus kemik iliği kanlanması",
                "category": "Üst Servikal Kırıklar"
            },
            {
                "id": "fc-s10-2",
                "front": "Alt servikal omurgada ekstansiyon teardrop kırığı hangi ana bağın avulsiyonu ile oluşur?",
                "back": "Anterior longitudinal ligamanın (ALL) korpus ön-alt köşesini koparmasıyla oluşur.",
                "hint": "Omurga ön yüzeyindeki ana boyuna bağ",
                "category": "Alt Servikal Travmalar"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Servikal omurga travmaları karşılaştırıldığında aşağıdakilerden hangisi doğrudur?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Tip II odontoid kırığı dens kaidesindeki yetersiz kanlanma nedeniyle yüksek psödoartroz riski taşır",
                        "isCorrect": True,
                        "explanation": "Doğru. Tip II odontoid kırığı dens kaidesinde yer alır ve kanlanması zayıf olduğundan konservatif takipte yüzde seksen ila doksan kaynamaz; transodontoid vida fiksasyonu gerekir."
                    },
                    {
                        "key": "B",
                        "text": "Jefferson kırığında transvers ligaman rüptürü tanısı için eşik değer lateral kütle taşmasının 2 mm olmasıdır",
                        "isCorrect": False,
                        "explanation": "Jefferson kırığında transvers ligaman rüptürü ve cerrahi endikasyon için lateral kütlelerin odontoid üzerinden yana taşma toplamının yedi milimetreyi aşması gerekir."
                    },
                    {
                        "key": "C",
                        "text": "Hangman kırığında pars interartikülaris kırığı spinal kanalı daraltarak hastaların tamamında tam kord basısı yapar",
                        "isCorrect": False,
                        "explanation": "Hangman kırığında C2 korpusu öne kayarken arka nöral ark arkada kalır. Bu durum spinal kanalı genişleterek kord basısı riskini azaltır."
                    },
                    {
                        "key": "D",
                        "text": "Alt servikal hiperekstansiyon travmalarında birincil olarak posterior longitudinal ligaman kopar",
                        "isCorrect": False,
                        "explanation": "Hiperekstansiyon travmasında omurganın ön sütunu gerildiğinden anterior longitudinal ligaman yırtılır. Posterior longitudinal ligaman ise hiperfleksiyon yaralanmalarında gerilip rüptüre olur."
                    }
                ]
            },
            {
                "type": "feature_bidding",
                "optionA": "Hangman Fraktürü (Travmatik Spondilolistezis)",
                "optionB": "Jefferson Fraktürü (C1 Patlama Kırığı)",
                "rounds": [
                    {
                        "feature": "C2 pars interartikülaris kemik istmuslarının iki taraflı olarak kırılması",
                        "correct": "A",
                        "explanation": "Hangman kırığı C2 omurunda iki taraflı pars interartikülaris kırığı sonucu korpusun öne kaymasıdır."
                    },
                    {
                        "feature": "Aksiyel yüklenme ile atlas halkasının ön ve arka arklarında çok parçalı kırık oluşması",
                        "correct": "B",
                        "explanation": "Jefferson kırığı baş tepesine gelen aksiyel kompresyonla C1 halkasının dört parçalı olarak patlamasıdır."
                    }
                ]
            },
            {
                "type": "venn_grid",
                "labelA": "Tip II Odontoid Kırığı",
                "labelB": "Tip III Odontoid Kırığı",
                "items": [
                    {"criterion": "Kırık hattının odontoid kaidesiyle sınırlı kalması", "correct": "A"},
                    {"criterion": "Kırık hattının geniş C2 vertebra gövdesi içine uzanması", "correct": "B"},
                    {"criterion": "Aksis omurunun odontoid çıkıntısını ilgilendiren travmatik kırık olma", "correct": "both"},
                    {"criterion": "C1 lateral kütlelerinin dışa 7 mm taşmasıyla tanımlanma", "correct": "neither"}
                ]
            },
            {
                "type": "swipe_matching",
                "leftCategory": "Konservatif Tedaviye Yüksek Yanıt",
                "rightCategory": "Cerrahi / İnstabilite Riski",
                "cards": [
                    {"text": "Tip I ve Tip III odontoid kırıkları", "category": "left"},
                    {"text": "Ayrışması 3 mm'den az olan açılanmasız Tip I Hangman kırığı", "category": "left"},
                    {"text": "Yüzde seksen ila doksan kaynamayan Tip II odontoid kırığı", "category": "right"},
                    {"text": "Lateral kütle taşma toplamı 7 mm'den fazla olan Jefferson kırığı", "category": "right"}
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Servikal Omurga Kırık Tipleri ve Karakteristikleri",
                "items": [
                    {
                        "text": "Tip III odontoid kırıkları C2 korpusu içine uzandığından kanlanması iyidir ve konservatif tedaviye yanıt verir.",
                        "isLie": False,
                        "explanation": "Spongiyöz kemik kanlanması zengin olduğundan Tip III kırıklar konservatif tespitle yüksek oranda iyileşir."
                    },
                    {
                        "text": "Alt servikal omurgada fleksiyon travması faset subluksasyonuna ve travmatik disk hernisine yol açabilir.",
                        "isLie": False,
                        "explanation": "Hiperfleksiyon arka kolon bağlarını yırtıp diski arkaya fıtıklaştırarak faset dislokasyonu yaratabilir."
                    },
                    {
                        "text": "Jefferson kırığında lateral kütlelerin odontoid üzerinden yana taşma toplamı 3 mm olduğunda transvers bağ kesinlikle kopmuştur.",
                        "isLie": True,
                        "explanation": "Transvers ligaman rüptürü için cerrahi sınır yedi milimetredir; üç milimetre taşmada bağ genellikle sağlamdır."
                    }
                ]
            }
        ]
    },

    # SLIDE 11
    {
        "slideNumber": 11,
        "id": "k2p-y25-k2-13-spinal-travmalar-s11",
        "title": "Torakolomber Travmalar: Denis Üç Kolon Teorisi ve Biyomekanik Stabilite",
        "subtitle": "Anterior, orta ve posterior kolon anatomisi ve Denis instabilite kriterleri",
        "badge": "Torakolomber Travmalar",
        "bolum": "5",
        "pdfSayfalari": [35, 37],
        "kaynakSayfa": "Slayt 35-37",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 35,
            "endPage": 37
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Torakolomber bileşke (T11-L1), rijit torakal kafes ile hareketli lomber omurga arasındaki anatomik geçiş zonu olup spinal kırıkların en sık görüldüğü yerdir. Denis, omurgayı üç biyomekanik kolona ayırmıştır.\n\n- **Anterior Kolon:** Anterior longitudinal ligaman (ALL), korpusun ön 2/3 kısmı ve anulus fibrozusun ön 2/3'ünü kapsar.\n- **Orta Kolon:** Posterior longitudinal ligaman (PLL), korpusun arka 1/3 kısmı ve anulus fibrozusun arka 1/3'ünden oluşur. Omurilik kanalı ön duvarını teşkil eder.\n- **Posterior Kolon:** Pediküller, fasetler, laminalar ve posterior ligaman kompleksini (supraspinöz, interspinöz, lig. flavum) içerir.\n\n> [!IMPORTANT]\n> Denis kriterlerine göre tek kolon tutuluşu stabildir; ancak üç kolon tutuluşu, iki komşu kolon tutuluşu veya ORTA KOLON tutuluşu mutlak instabilite göstergesidir.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Denis üç kolon modelinde orta kolon spinal kanal ön duvarıdır; orta kolon tutuluşu omurganın instabil olduğunu kanıtlar."
        ],
        "medicalTerms": [
            {
                "term": "Denis Orta Kolonu",
                "explanation": "PLL, vertebra korpusunun arka 1/3 kısmı ve anulus fibrozusun arka 1/3'ünden oluşan kritik biyomekanik kolondur."
            },
            {
                "term": "Posterior Ligamentöz Kompleks",
                "explanation": "Supraspinöz bağ, interspinöz bağ, ligamentum flavum ve faset eklem kapsüllerinden oluşan arka gerilme bandıdır."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s11-1",
                "front": "Denis üç kolon teorisinde orta kolon hangi anatomik yapıları içerir?",
                "back": "PLL, vertebra korpusunun arka 1/3'ü ve anulus fibrozusun arka 1/3'ünü içerir.",
                "hint": "Spinal kanalın ön duvarını oluşturan arka 1/3 korpus ve ligaman",
                "category": "Torakolomber Travmalar"
            },
            {
                "id": "fc-s11-2",
                "front": "Denis stabilite kriterlerine göre tek başına hangi kolonun tutulması omurgayı doğrudan instabil yapar?",
                "back": "Orta kolonun tutulması omurgayı kesinlikle instabil yapar.",
                "hint": "Spinal kanal ön duvarı kolonu",
                "category": "Torakolomber Travmalar"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Denis üç kolon modelinde posterior longitudinal ligaman (PLL), vertebra korpusunun arka 1/3 kısmı ve anulus fibrozusun arka 1/3'ünü içeren ve hasar gördüğünde mutlak instabiliteye işaret eden anatomik kolon hangisidir?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Orta kolon",
                        "isCorrect": True,
                        "explanation": "Doğru. Denis modelinde orta kolon korpusun arka üçte biri, anulus fibrozusun arka üçte biri ve posterior longitudinal ligamandan oluşur. Bu kolonun hasarı omurilik kanalı komşuluğu nedeniyle daima instabilite kriteridir."
                    },
                    {
                        "key": "B",
                        "text": "Anterior kolon",
                        "isCorrect": False,
                        "explanation": "Anterior kolon anterior longitudinal ligaman ile korpus ve anulusun ön üçte ikisini içerir. İzole anterior kolon hasarı omurga stabilitesini bozmaz ve kama kompresyon kırığı olarak seyreder."
                    },
                    {
                        "key": "C",
                        "text": "Posterior kemik kolon",
                        "isCorrect": False,
                        "explanation": "Posterior kolon pedikülleri, laminaları, faset eklemlerini ve posterior ligaman kompleksini kapsar. Tek başına tutulduğunda orta kolon kadar doğrudan omurilik kanalı ön duvarını temsil etmez."
                    },
                    {
                        "key": "D",
                        "text": "Lateral artiküler kolon",
                        "isCorrect": False,
                        "explanation": "Lateral artiküler kütleler servikal omurga anatomisinde faset eklemlerini ve segmental eklemleşmeyi oluşturan yapılardır. Denis sınıflaması torakolomber omurgayı anterior, orta ve posterior olmak üzere üç kolonda inceler; sınıflamada lateral kolon tanımı yer almaz."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Denis üç kolon teorisinde orta kolon omurilik kanalı ön duvarını oluşturur ve hasarı mutlak instabilite göstergesidir.",
                "maskedTerm": "kolon",
                "hint": "Denis sınıflamasındaki üç taşıyıcı sütundan her biri"
            },
            {
                "type": "interactive_table",
                "tableHeaders": ["Denis Kolonu", "Kemik Bileşenleri", "Ligamentöz ve Diskal Bileşenler", "Klinik Stabilite Anlamı"],
                "tableRows": [
                    {
                        "cells": [
                            {"value": "Anterior Kolon", "isMasked": False},
                            {"value": "Korpusun ön 2/3 kısmı", "isMasked": False},
                            {"value": "ALL ve anulusun ön 2/3'ü", "isMasked": False},
                            {"value": "Tek başına tutulursa omurga stabildir", "isMasked": False}
                        ]
                    },
                    {
                        "cells": [
                            {"value": "Orta Kolon", "isMasked": False},
                            {"value": "Korpusun arka 1/3 kısmı", "isMasked": True, "hint": "Gövdenin nöral kanala bakan derin parçası"},
                            {"value": "PLL ve anulusun arka 1/3'ü", "isMasked": False},
                            {"value": "Tutulumu daima instabilite göstergesidir", "isMasked": False}
                        ]
                    },
                    {
                        "cells": [
                            {"value": "Posterior Kolon", "isMasked": False},
                            {"value": "Pediküller, laminalar ve fasetler", "isMasked": False},
                            {"value": "Posterior ligaman kompleksi", "isMasked": True, "hint": "Supraspinöz, interspinöz ve flavum bağları"},
                            {"value": "Gerilme bandı görevi üstlenir", "isMasked": False}
                        ]
                    }
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Denis Üç Kolon Modeli ve Spinal Stabilite Kuralları",
                "items": [
                    {
                        "text": "Torakolomber bileşke (T11-L1) rijit ve mobil omurga geçişinde yer aldığından kırıkların en sık görüldüğü yerdir.",
                        "isLie": False,
                        "explanation": "Mekanik streslerin odaklandığı T11-L1 bileşkesi torakolomber travmaların açık ara en sık merkezidir."
                    },
                    {
                        "text": "Denis sınıflamasına göre orta kolon tutuluşu omurganın instabil olduğunu gösteren temel kriterdir.",
                        "isLie": False,
                        "explanation": "Orta kolon spinal kanal ön duvarını oluşturduğundan buradaki hasar potansiyel nöral bası ve instabilite demektir."
                    },
                    {
                        "text": "Denis modeline göre komşu iki kolonun birlikte tutulması omurganın mekanik olarak tam stabil kaldığını kanıtlar.",
                        "isLie": True,
                        "explanation": "Komşu iki kolonun veya üç kolonun birlikte tutulması omurganın yük taşıma kapasitesini yıkarak ağır instabilite oluşturur."
                    }
                ]
            },
            {
                "type": "active_recall",
                "question": "Denis biyomekanik sınıflamasına göre hangi kolon tutulumları omurgayı kesin olarak instabil kabul ettirir?",
                "answer": "Üç kolon tutuluşu, komşu iki kolon tutuluşu veya tek başına orta kolon tutuluşu omurgayı kesinlikle instabil yapar."
            }
        ]
    },

    # SLIDE 12
    {
        "slideNumber": 12,
        "id": "k2p-y25-k2-13-spinal-travmalar-s12",
        "title": "Torakolomber Kırık Tipleri: Kompresyon, Burst ve Fleksiyon-Distraksiyon",
        "subtitle": "Denis kırık sınıflaması, patlama mekanizması, Chance kırığı ve dislokasyonlar",
        "badge": "Torakolomber Travmalar",
        "bolum": "5",
        "pdfSayfalari": [38, 41],
        "kaynakSayfa": "Slayt 38-41",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 38,
            "endPage": 41
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Denis sınıflaması torakolomber kırıkları tutulan kolonlara ve hasar mekanizmasına göre dört ana tipe ayırır.\n\n- **1. Kompresyon Kırığı:** Yalnızca anterior kolon hasar görür; kama şeklinde yükseklik kaybı olur. Orta ve arka kolon sağlamdır, omurga stabildir ve nörolojik defisit beklenmez.\n- **2. Patlama (Burst) Kırığı:** Anterior ve orta kolon birlikte hasar görür. Aksiyel yükle korpus arka duvarı kırılarak spinal kanala kemik fragman taşar; nörolojik bası riski yüksektir ve instabildir.\n- **3. Emniyet Kemeri (Chance) Kırığı:** Fleksiyon-distraksiyon kuvvetiyle orta ve posterior kolon ayrışır.\n- **4. Kırıklı Çıkık (Fraktür-Dislokasyon):** Makaslama, fleksiyon-distraksiyon veya fleksiyon-rotasyon ile 3 kolonun tamamı veya 2-3 kolon parçalanır; ağır nörolojik defisit yaratır.\n\n> [!IMPORTANT]\n> Patlama (burst) kırığını basit kompresyon kırığından ayıran temel fark, orta kolonun kırılması ve kemik fragmanların spinal kanala retropulsiyonudur.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Burst kırığında anterior ve orta kolon birlikte kırılır; arka korpus fragmanı spinal kanala retropulse olur."
        ],
        "medicalTerms": [
            {
                "term": "Burst (Patlama) Kırığı",
                "explanation": "Aksiyel yüklenmeyle vertebra gövdesinin ezilerek anterior ve orta kolonlarının kanala doğru parçalanmasıdır."
            },
            {
                "term": "Chance Kırığı",
                "explanation": "Emniyet kemeri yaralanması olarak bilinen ve fleksiyon-distraksiyonla orta-arka kolonları ayıran kırıktır."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s12-1",
                "front": "Basit kama kompresyon kırığı ile patlama (burst) kırığı arasındaki en kritik ayrım nedir?",
                "back": "Burst kırığında orta kolonun hasar görmesi ve spinal kanala kemik taşmasıdır.",
                "hint": "Orta kolon sağlamlığı ve retropulsiyon",
                "category": "Torakolomber Travmalar"
            },
            {
                "id": "fc-s12-2",
                "front": "Fleksiyon-distraksiyon mekanizmasıyla posterior ve orta kolonun ayrışmasıyla karakterize kırık tipi nedir?",
                "back": "Emniyet kemeri tipi (Chance) kırığıdır.",
                "hint": "Seatbelt fraktürü",
                "category": "Torakolomber Travmalar"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Trafik kazası sonrası L1 omurunda aksiyel kompresyon sonucu hem anterior hem de orta kolonun kırıldığı ve arka korpus fragmanının spinal kanala taştığı (retropulsiyon) saptanan bir hastada Denis sınıflamasına göre tanı nedir?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Patlama (Burst) kırığı",
                        "isCorrect": True,
                        "explanation": "Doğru. Denis sınıflamasında aksiyel yüklenmeyle hem anterior hem de orta kolonun hasar görmesi ve korpus arka duvar fragmanlarının kanala taşması patlama (burst) kırığını tanımlar."
                    },
                    {
                        "key": "B",
                        "text": "Basit kama kompresyon kırığı",
                        "isCorrect": False,
                        "explanation": "Basit kama kompresyon kırığında hasar yalnızca anterior kolonla sınırlıdır. Orta kolon sağlam kaldığı için korpus arka duvarı bütünlüğünü korur ve kanala fragman taşması izlenmez."
                    },
                    {
                        "key": "C",
                        "text": "İzole transvers proses kırığı",
                        "isCorrect": False,
                        "explanation": "İzole transvers proses kırığı omurların yan çıkıntılarında gelişen minör kas avulsiyonudur. Korpusun anterior ve orta kolonlarını veya omurilik kanalını ilgilendiren majör bir kırık değildir."
                    },
                    {
                        "key": "D",
                        "text": "Tip I Odontoid avulsiyon kırığı",
                        "isCorrect": False,
                        "explanation": "Tip I odontoid kırığı C2 omurunun dens tepe noktasında gelişen üst servikal bir lezyondur. Torakolomber bileşke veya L1 patlama kırığıyla hiçbir anatomik ilişkisi yoktur."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Patlama kırığında aksiyel yüklenmeyle parçalanan korpus arka duvarı kemik fragmanlarının spinal kanala doğru kaymasına yol açar.",
                "maskedTerm": "kanala",
                "hint": "Omuriliğin içinden geçtiği kemik boşluğa yönelme"
            },
            {
                "type": "feature_bidding",
                "optionA": "Kama Kompresyon Kırığı",
                "optionB": "Patlama (Burst) Kırığı",
                "rounds": [
                    {
                        "feature": "Orta kolon sağlamdır ve kırık yalnızca anterior kolonda kama şeklinde çökmeye yol açar",
                        "correct": "A",
                        "explanation": "Kompresyon kırığında orta kolon sağlam kaldığından arka duvar bütünlüğü korunur ve nörolojik defisit beklenmez."
                    },
                    {
                        "feature": "Anterior ve orta kolon birlikte hasar görür; arka korpus fragmanı spinal kanala taşar",
                        "correct": "B",
                        "explanation": "Burst kırığında aksiyel yük orta kolonu da patlatarak spinal kanala kemik retropulsiyonu ve nörolojik risk doğurur."
                    }
                ]
            },
            {
                "type": "branching_logic",
                "scenario": "Yüksekten düşen 35 yaşındaki işçi acil servise getiriliyor. BT incelemesinde T12 omurunda izole anterior kolon kama kompresyon kırığı izleniyor; orta ve posterior kolonlar tamamen sağlamdır ve kanal basısı yoktur. Nörolojik muayenesi tam normaldir.",
                "options": [
                    {
                        "text": "Orta kolon sağlam ve omurga stabil olduğundan analjezik ve korse ile konservatif takip planlanması",
                        "isCorrect": True,
                        "feedback": "Doğru yaklaşım. İzole anterior kolon kama kırıklarında orta kolon sağlam ve kanal basısı yoksa omurga stabildir; konservatif izlem ve korse tedavisi yeterlidir."
                    },
                    {
                        "text": "Üç kolon instabilitesi geliştiği gerekçesiyle hastaya acil dekompresyon ve vida fiksasyonu yapılması",
                        "isCorrect": False,
                        "feedback": "Hatalı karar. İzole anterior kolon hasarı instabilite kriteri değildir. Orta ve arka kolon sağlamsa cerrahi stabilizasyon endikasyonu bulunmaz."
                    }
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Denis Torakolomber Kırık Tipleri ve Özellikleri",
                "items": [
                    {
                        "text": "Chance kırığı fleksiyon-distraksiyon mekanizmasıyla orta ve posterior kolonun ayrışmasıdır.",
                        "isLie": False,
                        "explanation": "Emniyet kemeri tipi Chance kırığında arka ve orta kolon transvers düzlemde distraksiyonla yırtılır."
                    },
                    {
                        "text": "Fraktür-dislokasyon yaralanmalarında üç kolonun tamamı veya iki komşu kolon ağır hasar görür.",
                        "isLie": False,
                        "explanation": "Fraktür-dislokasyon en yıkıcı tiptir; makaslama veya rotasyonla kolon bütünlüğü tamamen kaybolur."
                    },
                    {
                        "text": "Basit kompresyon kırıklarında orta kolon patlayarak spinal kanala kemik parçası fırlatır.",
                        "isLie": True,
                        "explanation": "Orta kolonun kırılıp kanala fragman retropulsiyonu yapması kompresyon değil, patlama (burst) kırığına özgüdür."
                    }
                ]
            }
        ]
    },

    # SLIDE 13
    {
        "slideNumber": 13,
        "id": "k2p-y25-k2-13-spinal-travmalar-s13",
        "title": "Spinal Travmalarda Tedavi: Konservatif İzlem ve Cerrahi Endikasyonlar",
        "subtitle": "Stabilite değerlendirmesi, korpus çökme oranı ve nörolojik tutuluma göre karar algoritması",
        "badge": "Klinik Yönetim",
        "bolum": "6",
        "pdfSayfalari": [42, 46],
        "kaynakSayfa": "Slayt 42-46",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 42,
            "endPage": 46
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Spinal travmalarda tedavi stratejisi omurganın biyomekanik stabilitesine ve nörolojik duruma göre belirlenir. Kararda fraktür şekli, omurilik basısı, nörolojik tutulumun derecesi ve eşlik eden sistemik yaralanmalar rol oynar.\n\n- **Konservatif Tedavi:** Omurga stabilse ve spinal kanalda bası yoksa konservatif izlem tercih edilir. Kama kompresyon kırıklarında vertebra korpus ön yükseklik kaybı yüzde ellinin altında ise korse ve istirahatle takip güvenlidir.\n- **Cerrahi Tedavi:** Korpus çökme oranı yüzde elliyi aşan kompresyon kırıkları, instabil patlama (burst) kırıkları ve fraktür-dislokasyonlar cerrahi endikasyondur. Ayrıca inkomplet kord basısı varlığında nöral dekompresyon şarttır.\n\n> [!IMPORTANT]\n> Vertebra korpusunda yüzde elliden fazla çökme veya ilerleyici nörolojik defisite yol açan kanal basısı varlığı cerrahi tedavinin temel göstergeleridir.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Kompresyon kırığında korpus çökmesi %50'nin altında ve kanalda bası yoksa konservatif takip edilir; %50 üzeri çökme cerrahi gerektirir."
        ],
        "medicalTerms": [
            {
                "term": "Konservatif Tedavi",
                "explanation": "Cerrahi müdahale olmaksızın yatak istirahati, rijit eksternal korse veya boyunluk ile yürütülen takip protokolüdür."
            },
            {
                "term": "Dekompresyon Cerrahisi",
                "explanation": "Spinal kord veya sinir köklerini sıkıştıran kemik, disk veya hematom dokusunun cerrahi olarak boşaltılmasıdır."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s13-1",
                "front": "Kama kompresyon kırıklarında konservatif tedavi sınırını belirleyen korpus çökme eşiği nedir?",
                "back": "Korpus ön yükseklik kaybının yüzde ellinin altında (% < 50) olmasıdır.",
                "hint": "Yüzde elli çökme sınırı",
                "category": "Klinik Yönetim"
            },
            {
                "id": "fc-s13-2",
                "front": "İnkomplet omurilik basısı olan bir hastada cerrahinin birincil acil hedefi nedir?",
                "back": "Kanaldaki basıyı kaldırarak nöral dokuları rahatlatmak (dekompresyon) ve stabilizasyon sağlamaktır.",
                "hint": "Nöral dekompresyon",
                "category": "Klinik Yönetim"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Torakolomber kama kompresyon kırığı olan nörolojik muayenesi normal bir hastada konservatif takip sınırını aşarak cerrahi stabilizasyon kararı verilmesini gerektiren korpus yükseklik kaybı (çökme) eşiği nedir?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Korpus yüksekliğinde yüzde elliden fazla çökme olması",
                        "isCorrect": True,
                        "explanation": "Doğru. Kama kompresyon kırıklarında vertebra korpus ön yüksekliğinde yüzde ellinin üzerinde çökme veya belirgin kifotik açılanma omurganın yük taşıma kapasitesini bozarak cerrahi stabilizasyon endikasyonu doğurur."
                    },
                    {
                        "key": "B",
                        "text": "Korpus yüksekliğinde yüzde on çökme olması",
                        "isCorrect": False,
                        "explanation": "Yüzde onluk korpus çökmesi biyomekanik dengeyi bozmaz. Bu hafif yükseklik kaybı omurga stabilitesini tehdit etmediğinden konservatif korse ve takip ile güvenle iyileşir."
                    },
                    {
                        "key": "C",
                        "text": "Korpus yüksekliğinde yüzde yirmi beş çökme olması",
                        "isCorrect": False,
                        "explanation": "Yüzde yirmi beşlik çökme yüzde elli eşik değerinin altındadır. Kanal basısı veya arka kolon hasarı eşlik etmedikçe konservatif tedavi sınırları içerisinde kabul edilir."
                    },
                    {
                        "key": "D",
                        "text": "Sadece tek taraflı transvers proses fissürü bulunması",
                        "isCorrect": False,
                        "explanation": "Transvers proses fissürü omur gövdesinin taşıyıcı kolonlarını etkilemeyen minör bir kemik çatlağıdır. Korpus yüksekliğiyle veya majör cerrahi endikasyonla ilişkisi bulunmaz."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Spinal travmalarda korpus ön yükseklik kaybı yüzde ellinin altında olan stabil kama kompresyon kırıkları konservatif izlemle takip edilebilir.",
                "maskedTerm": "konservatif",
                "hint": "Ameliyatsız tıbbi takip ve korse yaklaşımı"
            },
            {
                "type": "before_after_slider",
                "leftTitle": "Konservatif Tedavi Kriterleri",
                "rightTitle": "Cerrahi Tedavi Kriterleri",
                "leftPoints": [
                    "Biyomekanik olarak stabil omurga dizilimi",
                    "Kanal basısı ve nörolojik defisit olmaması",
                    "Korpus yüksekliğinde yüzde ellinin altında çökme"
                ],
                "rightPoints": [
                    "İnstabil patlama kırığı veya fraktür-dislokasyon",
                    "Kanalda nöral dokuya bası yapan disk veya kemik",
                    "Korpus yüksekliğinde yüzde elliden fazla çökme"
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Spinal Travmalarda Tedavi Kararı ve Endikasyonlar",
                "items": [
                    {
                        "text": "İnstabil patlama kırıkları ve fraktür-dislokasyonlar cerrahi endikasyon grubundadır.",
                        "isLie": False,
                        "explanation": "Mekanik stabilitesini kaybetmiş ve kolonları parçalanmış omurgaların cerrahi fiksasyonu zorunludur."
                    },
                    {
                        "text": "İnkomplet omurilik hasarı ve kanalda kemik basısı olan hastalarda cerrahi dekompresyon gerekir.",
                        "isLie": False,
                        "explanation": "Geri dönüş potansiyeli olan inkomplet lezyonlarda basının kaldırılması nörolojik iyileşmenin temel şartıdır."
                    },
                    {
                        "text": "Kama kompresyon kırıklarında korpus çökmesi yüzde seksen olsa dahi omurga her zaman konservatif izlenmelidir.",
                        "isLie": True,
                        "explanation": "Korpus çökmesi yüzde elliyi aştığında biyomekanik aks çöker ve kifoz gelişir; bu durum cerrahi endikasyondur."
                    }
                ]
            },
            {
                "type": "active_recall",
                "question": "Cerrahi tedavide nörolojik iyileşme şansını en üst düzeye çıkarmak için kanaldaki kemik veya disk basısının kaldırılması işlemine ne ad verilir?",
                "answer": "Cerrahi dekompresyon (nöral dekompresyon) adı verilir."
            }
        ]
    },

    # SLIDE 14
    {
        "slideNumber": 14,
        "id": "k2p-y25-k2-13-spinal-travmalar-s14",
        "title": "Cerrahi Teknikler: Dekompresyon, Redüksiyon ve Enstrümantasyonlu Stabilizasyon",
        "subtitle": "Transodontoid vida, anterior plaklama ve posterior transpediküler fiksasyon yöntemleri",
        "badge": "Klinik Yönetim",
        "bolum": "6",
        "pdfSayfalari": [47, 53],
        "kaynakSayfa": "Slayt 47-53",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 47,
            "endPage": 53
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Spinal cerrahide iki temel hedef vardır: bası altındaki nöral dokuları rahatlatmak (dekompresyon) ve omurganın yük taşıyıcı dengesini yeniden kurmak (enstrümantasyonla stabilizasyon).\n\n- **Dekompresyon:** İnkomplet kord hasarında spinal kanala taşan disk veya kemik parçaları anterior korpektomi veya posterior yaklaşımla temizlenir.\n- **Üst Servikal Stabilizasyon:** Tip II odontoid kırıklarında anterior yaklaşımla transodontoid vida yerleştirilir; anatomik redüksiyon sağlanarak boyun rotasyon hareketi korunur.\n- **Alt Servikal ve Torakolomber:** Alt servikal çıkıklarda anterior diskektomi ve plak fiksasyonu uygulanır. Torakolomber dislokasyon ve burst kırıklarında (ör. T12-L1 dislokasyonu) posterior transpediküler vida ve rod sistemleriyle güçlü stabilizasyon sağlanır.\n\n> [!NOTE]\n> Cerrahi enstrümantasyon omurga dizilimini düzelterek erken mobilizasyona olanak tanır ve geç dönem kifotik deformite gelişimini engeller.",
        "spotPearls": [
            "📌 [SINAV SPOTU] T12-L1 dislokasyon ve instabil kırıklarında en güçlü biyomekanik fiksasyon posterior transpediküler vida ve rod sistemleriyle sağlanır."
        ],
        "medicalTerms": [
            {
                "term": "Transpediküler Vida",
                "explanation": "Vertebra pedikülünün içinden korpusa ilerletilerek omurganın üç kolonunu aynı anda sabitleyen cerrahi vidadır."
            },
            {
                "term": "Anterior Korpektomi",
                "explanation": "Kırılan ve omuriliğe basan vertebra cisminin cerrahi olarak tamamen çıkarılması işlemidir."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s14-1",
                "front": "C2 Tip II odontoid kırığında fizyolojik boyun rotasyonunu koruyan ideal cerrahi teknik nedir?",
                "back": "Anterior yaklaşımla uygulanan transodontoid vida fiksasyonudur.",
                "hint": "Dens içinden geçen anterior tek/çift vida",
                "category": "Klinik Yönetim"
            },
            {
                "id": "fc-s14-2",
                "front": "Torakolomber instabil kırık ve dislokasyonlarda üç kolon rijit fiksasyonunu sağlayan temel cerrahi yöntem nedir?",
                "back": "Posterior transpediküler vida ve rod enstrümantasyonudur.",
                "hint": "Pediküllerden gönderilen vida-rod sistemi",
                "category": "Klinik Yönetim"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Torakolomber bileşkede (örneğin T12-L1 seviyesinde) instabil burst kırığı veya fraktür-dislokasyon gelişen bir hastada omurganın üç kolonunu mekanik olarak sabitlemek için en sık tercih edilen cerrahi yöntem hangisidir?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Posterior transpediküler vida ve rod enstrümantasyonu",
                        "isCorrect": True,
                        "explanation": "Doğru. Torakolomber bileşkede pediküllerden korpus içine gönderilen transpediküler vidalar ve rodlar güçlü üç kolon fiksasyonu sağlar; deformiteyi düzeltir ve erken mobilizasyona olanak tanır."
                    },
                    {
                        "key": "B",
                        "text": "İzole halo-vest eksternal immobilizasyonu",
                        "isCorrect": False,
                        "explanation": "Halo-vest fiksasyonu servikal omurga kırıklarında kullanılan eksternal bir cihazdır. Torakolomber bileşkedeki instabil dislokasyonları sabitlemede mekanik olarak yetersizdir."
                    },
                    {
                        "key": "C",
                        "text": "Anterior transodontoid tek vida fiksasyonu",
                        "isCorrect": False,
                        "explanation": "Transodontoid vida fiksasyonu C2 odontoid Tip II kırıklarına özgü bir tekniktir. T12-L1 torakolomber bileşke patolojilerinde kullanılabilecek bir cerrahi yöntem değildir."
                    },
                    {
                        "key": "D",
                        "text": "Basit yumuşak servikal boyunluk uygulaması",
                        "isCorrect": False,
                        "explanation": "Yumuşak boyunluk servikal kas spazmlarında semptomatik destek sağlar. Torakolomber bileşkede instabil kemik dislokasyonunu sabitleme yeteneği kesinlikle yoktur."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Torakolomber instabil kırıklarda omurga biyomekaniğini yeniden kurmak için enstrümantasyon ile stabilizasyon ameliyatı uygulanır.",
                "maskedTerm": "enstrümantasyon",
                "hint": "Metal vida ve rod gibi cerrahi implant sistemlerinin kullanımı"
            },
            {
                "type": "causal_chain",
                "title": "İnstabil Kırıkta Cerrahi Yönetim Basamakları",
                "steps": [
                    "1. Planlama: Radyolojik görüntüleme ile bası ve instabilite düzeyinin netleştirilmesi",
                    "2. Pozisyon: Hastanın nörolojik hasar yaratılmadan ameliyat masasına alınması",
                    "3. Dekompresyon: Spinal kanala bası yapan kemik ve disk fragmanlarının çıkarılması",
                    "4. Fiksasyon: Transpediküler vida ve rod sistemleriyle biyomekanik stabilizasyon sağlanması"
                ]
            },
            {
                "type": "venn_grid",
                "labelA": "Transodontoid Vida Fiksasyonu",
                "labelB": "Posterior Transpediküler Enstrümantasyon",
                "items": [
                    {"criterion": "Üst servikal bölgede C2 Tip II odontoid kırığına yönelik uygulanma", "correct": "A"},
                    {"criterion": "Torakolomber instabil burst ve dislokasyonlarda güçlü vida-rod fiksasyonu sağlama", "correct": "B"},
                    {"criterion": "Spinal travma cerrahisinde kemik stabilizasyonu amacıyla kullanılma", "correct": "both"},
                    {"criterion": "Ameliyatsız konservatif korse tedavisinin standart protokolü olma", "correct": "neither"}
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Spinal Cerrahi Dekompresyon ve Stabilizasyon İlkeleri",
                "items": [
                    {
                        "text": "Dekompresyon cerrahisinin amacı spinal kanaldaki basıyı kaldırarak nöral dokuları rahatlatmaktır.",
                        "isLie": False,
                        "explanation": "Kanala taşan disk veya kemik parçalarının çıkarılması kord perfüzyonunu ve nörolojik iyileşmeyi destekler."
                    },
                    {
                        "text": "Torakolomber fraktür-dislokasyonlarda transpediküler vidalar pedikül kemik köprülerinden korpusa gönderilir.",
                        "isLie": False,
                        "explanation": "Pedikül vidaları güçlü kemik tutunumuyla omurganın üç kolonunu aynı anda kontrol eden biyomekanik fiksasyon sağlar."
                    },
                    {
                        "text": "Tip II odontoid kırıklarında transodontoid vida ameliyatı boyun rotasyon hareketini tamamen yok eder.",
                        "isLie": True,
                        "explanation": "Transodontoid vida densi korpusa kaynatarak C1-C2 eklem anatomisini ve başın fizyolojik rotasyonunu korur."
                    }
                ]
            }
        ]
    },

    # SLIDE 15
    {
        "slideNumber": 15,
        "id": "k2p-y25-k2-13-spinal-travmalar-s15",
        "title": "Omurilik Hasarı: Klinik Seyir, Spinal Şok ve Acil Yönetim İlkeleri",
        "subtitle": "Spinal şok fizyopatolojisi, bulbokavernöz refleks, sakral koruma ve acil hasta bakımı",
        "badge": "Klinik Yönetim",
        "bolum": "6",
        "pdfSayfalari": [54, 57],
        "kaynakSayfa": "Slayt 54-57",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 54,
            "endPage": 57
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": False,
        "synthesisNarrative": "Akut omurilik yaralanması sonrasında lezyon seviyesi altında geçici olarak tüm motor, duyu ve refleks aktivitelerinin kaybolduğu tabloya spinal şok adı verilir.\n\n- **Spinal Şokun Sonu:** Spinal şokun sona erdiğinin en kritik klinik göstergesi bulbokavernöz refleksin geri dönmesidir (S3-S4 arkı). Bu refleks dönmeden lezyonun komplet olduğu kesinleştirilemez.\n- **Nörojenik Şok:** T6 seviyesi üzerindeki hasarlarda sempatik tonus kaybı sonucu vazodilatasyon, hipotansiyon ve bradikardi gelişir.\n- **Prognoz ve Sakral Koruma:** Perianal duyu ve anal sfinkter tonusunun korunduğu inkomplet lezyonlarda iyileşme şansı belirgin şekilde yüksektir.\n- **Acil Yönetim:** Sahada rijit boyunluk ve log-roll tekniğiyle omurga korunmalı; ortalama arteriyel basınç 85 mmHg üzerinde tutulmalıdır.\n\n> [!IMPORTANT]\n> Bulbokavernöz refleks dönmeden komplet spinal kord lezyonu tanısı konulamaz; bu refleksin dönüşü spinal şokun bittiğini kanıtlar.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Spinal şokun bittiğini gösteren en güvenilir bulgu bulbokavernöz refleksin geri dönmesidir.",
            "🚨 [KRİTİK UYARI] T6 üzeri omurilik yaralanmalarında nörojenik şok gelişir; hipotansiyona bradikardi eşlik eder."
        ],
        "medicalTerms": [
            {
                "term": "Spinal Şok",
                "explanation": "Akut kord hasarı sonrasında lezyon düzeyi altında geçici flask paralizi ve arefleksi gelişmesidir."
            },
            {
                "term": "Bulbokavernöz Refleks",
                "explanation": "Glans penis veya foley kateterin çekilmesiyle eksternal anal sfinkterin kasılmasını ölçen S3-S4 refleksidir."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s15-1",
                "front": "Spinal şok tablosunun sona erdiğini gösteren en önemli erken sakral refleks hangisidir?",
                "back": "Bulbokavernöz refleksin (S3-S4) geri dönmesidir.",
                "hint": "Anal sfinkter kasılmasını ölçen sakral ark",
                "category": "Klinik Yönetim"
            },
            {
                "id": "fc-s15-2",
                "front": "Akut kord hasarında nörojenik şok tablosunu hemorajik şoktan ayıran en temel kardiyovasküler bulgu nedir?",
                "back": "Hipotansiyona taşikardi yerine bradikardinin eşlik etmesidir.",
                "hint": "Sempatik tonus kaybına bağlı yavaş nabız",
                "category": "Klinik Yönetim"
            }
        ],
        "interactiveElements": [
            {
                "type": "micro_quiz",
                "question": "Akut omurilik yaralanması sonrası gelişen spinal şok tablosunun sona erdiğini ve nörolojik defisitin gerçek prognozunun değerlendirilebileceğini gösteren en güvenilir klinik refleks hangisidir?",
                "microQuizOptions": [
                    {
                        "key": "A",
                        "text": "Bulbokavernöz refleksin geri dönmesi",
                        "isCorrect": True,
                        "explanation": "Doğru. Bulbokavernöz refleks sakral S3-S4 segmentlerini değerlendirir. Bu refleksin geri dönmesi kordun arefleksi evresinden çıktığını ve spinal şok tablosunun bittiğini kanıtlar."
                    },
                    {
                        "key": "B",
                        "text": "Patella tendon refleksinin hiperaktifleşmesi",
                        "isCorrect": False,
                        "explanation": "Patella refleksi L2-L4 seviyesini test eder ve spinal şok sonrasında spastisiteye bağlı geç dönemde hiperaktifleşebilir. Spinal şokun bitişini belirleyen birincil erken sakral refleks değildir."
                    },
                    {
                        "key": "C",
                        "text": "Kornea refleksinin pozitifleşmesi",
                        "isCorrect": False,
                        "explanation": "Kornea refleksi trigeminal ve fasiyal kraniyal sinirler tarafından yönetilen bir beyin sapı refleksidir. Medulla spinalis yaralanması veya spinal şok evrelemesiyle ilişkisi yoktur."
                    },
                    {
                        "key": "D",
                        "text": "Babinski işaretinin kaybolması",
                        "isCorrect": False,
                        "explanation": "Babinski işareti kortikospinal traktus lezyonlarında ortaya çıkan patolojik bir yanıttır. Spinal şok sırasında arefleksi nedeniyle alınamaz; kaybolması spinal şokun bittiğini göstermez."
                    }
                ]
            },
            {
                "type": "cloze_masking",
                "sentence": "Akut omurilik hasarında spinal şok tablosunun bittiğinin en kritik klinik göstergesi bulbokavernöz refleksin geri dönmesidir.",
                "maskedTerm": "bulbokavernöz",
                "hint": "Glans penis veya klitoris uyarısıyla anal sfinkterin kasılmasını ölçen sakral refleks"
            },
            {
                "type": "branching_logic",
                "scenario": "T4 seviyesinde travmatik omurilik hasarı geçiren ve arefleksi tablosunda olan bir hastada akut dönemde kan basıncı 80/50 mmHg, nabız 48 atım/dakika olarak ölçülüyor. Cilt ılık ve kurudur.",
                "options": [
                    {
                        "text": "T6 üzeri sempatik tonus kaybına bağlı nörojenik şok düşünülerek sıvı ve vazopressör desteğiyle ortalama arteriyel basıncın 85 mmHg üzerine hedeflenmesi",
                        "isCorrect": True,
                        "feedback": "Doğru karar. T6 üzeri lezyonlarda sempatik tonus kaybı bradikardi ve vazodilatasyonla nörojenik şoka yol açar; kord perfüzyonunu korumak için OAB 85 mmHg üzerinde tutulmalıdır."
                    },
                    {
                        "text": "Klasik hemorajik şok düşünülerek yalnızca aşırı hacim yüklemesi yapılması ve bradikardinin önemsenmemesi",
                        "isCorrect": False,
                        "feedback": "Hatalı yaklaşım. Hipotansiyona eşlik eden bradikardi ve ılık cilt hemorajik şok değil nörojenik şok göstergesidir. Aşırı kontrolsüz sıvı akciğer ödemi riski yaratır."
                    }
                ]
            },
            {
                "type": "spot_the_lie",
                "topic": "Omurilik Hasarı, Spinal Şok ve Komplikasyon Yönetimi",
                "items": [
                    {
                        "text": "Nörojenik şokta sempatik kesi nedeniyle hipotansiyona paradoksal bradikardi eşlik eder.",
                        "isLie": False,
                        "explanation": "T6 üzeri kord kesilerinde vazomotor tonus kaybolur; vazodilatasyon ve bradikardi klinik tablosu oturur."
                    },
                    {
                        "text": "Sakral koruma mevcudiyeti inkomplet lezyonu gösterir ve daha iyi fonksiyonel prognoza işaret eder.",
                        "isLie": False,
                        "explanation": "Sakral liflerin korunması lezyonun tam olmadığını kanıtlar ve fonksiyonel iyileşme potansiyelinin yüksek olduğunu gösterir."
                    },
                    {
                        "text": "Spinal şok arefleksi tablosu sürerken hastaya kesin olarak kalıcı komplet paralizi teşhisi konulabilir.",
                        "isLie": True,
                        "explanation": "Spinal şok devam ederken refleksler geçici baskı altındadır; bulbokavernöz refleks dönmeden komplet hasar tanısı konulamaz."
                    }
                ]
            },
            {
                "type": "active_recall",
                "question": "Akut spinal kord yaralanmalı bir hastada omurilik perfüzyonunu korumak amacıyla hedeflenen minimum ortalama arteriyel basınç değeri nedir?",
                "answer": "Ortalama arteriyel basıncın en az 85 mmHg seviyesinde tutulması hedeflenir."
            }
        ]
    },

    # SLIDE 16 (GAME SLIDE)
    {
        "slideNumber": 16,
        "id": "k2p-y25-k2-13-spinal-travmalar-s16",
        "title": "[OYUN SAYFASI] Ders Sonu Oyunları: Medulla Spinalis Lezyonları ve Spinal Travmalar",
        "subtitle": "Spinal travma biyomekaniği, kırık sınıflamaları, cerrahi endikasyonlar ve hasta yönetimini oyunlarla pekiştirin",
        "badge": "Ders Sonu Değerlendirme",
        "bolum": "6",
        "pdfSayfalari": [1, 57],
        "kaynakSayfa": "Slayt 1-57",
        "sourcePdf": {
            "pdf": "meds_database_25_26/pdf/kurul2/y25-k2-13-spinal-travmalar.pdf",
            "startPage": 1,
            "endPage": 57
        },
        "isCheckpoint": False,
        "checkpointNumber": None,
        "isGameFinale": True,
        "synthesisNarrative": "Medulla spinalis lezyonları ve spinal travmalar dersinin tüm biyomekanik, anatomik ve klinik aşamalarını interaktif ders sonu oyunlarıyla pekiştirin.\n\n- **Sıralama Oyunu:** Torakolomber travma geçiren bir hastada kaza anından cerrahi fiksasyona uzanan patofizyolojik ve klinik basamakları doğru sıraya dizin.\n- **Tahmin Sürgüsü:** Jefferson kırığı cerrahi eşiği, odontoid kaynamama yüzdesi ve kompresyon kırığı cerrahi sınırını tahmin edin.\n- **Parametre Değişimi:** Akut nörojenik şok tablosunda kardiyovasküler ve nörolojik parametrelerin seyrini analiz edin.\n- **Metin Onarımı:** Odontoid ve Denis sınıflamasındaki hatalı ifadeleri saptayarak doğrularıyla değiştirin.\n\n> [!NOTE]\n> Dört farklı oyun türüyle teorik sınıflamaları klinik karar algoritmalarına dönüştürün.",
        "spotPearls": [
            "📌 [SINAV SPOTU] Dört oyunla Jefferson 7 mm eşiği, Tip II odontoid psödoartrozu ve Denis üç kolon modelini pekiştirin."
        ],
        "medicalTerms": [
            {
                "term": "Enstrümantasyon",
                "explanation": "Omurga stabilitesini sağlamak amacıyla metal vida, plak ve rod sistemlerinin cerrahi implantasyonudur."
            },
            {
                "term": "Nörojenik Şok",
                "explanation": "T6 üzeri kord lezyonlarında sempatik tonus kaybına bağlı gelişen hipotansiyon ve bradikardi tablosudur."
            }
        ],
        "flashcards": [
            {
                "id": "fc-s16-1",
                "front": "C1 patlama kırığında transvers ligaman rüptürü kabul edilen taşma eşik değeri nedir?",
                "back": "Lateral kütlelerin toplam 7 mm'den fazla yana taşmasıdır.",
                "hint": "Yedi milimetre kuralı",
                "category": "Ders Sonu Oyunu"
            },
            {
                "id": "fc-s16-2",
                "front": "Denis modeline göre orta kolon tutuluşu ne anlama gelir?",
                "back": "Omurganın mutlak biyomekanik instabilitesi anlamına gelir.",
                "hint": "Kanal ön duvarı hasarı",
                "category": "Ders Sonu Oyunu"
            }
        ],
        "interactiveElements": [
            {
                "type": "sequence_order",
                "prompt": "Yüksekten düşme sonucu T12 burst kırığı ve inkomplet omurilik hasarı gelişen hastanın acil servisten cerrahiye uzanan yönetim basamaklarını doğru sıraya dizin.",
                "steps": [
                    "1. Sahada omurganın rijit boyunluk ve omurga tahtasıyla log-roll tekniğiyle immobilize edilmesi",
                    "2. Acil serviste hemodinamik resüsitasyonla ortalama arteriyel basıncın 85 mmHg üzerinde tutulması",
                    "3. Bilgisayarlı tomografi ile T12 anterior ve orta kolon hasarının ve kanal basısının görüntülenmesi",
                    "4. Spinal şok tablosunda bulbokavernöz refleks değerlendirmesiyle inkomplet kord hasarının saptanması",
                    "5. Cerrahiye alınarak spinal kanaldaki kemik basısının dekompresyonu ve transpediküler vida stabilizasyonu"
                ],
                "explanation": "Spinal travmalı hastada önce sahada katı immobilizasyon sağlanır, ardından hemodinamik resüsitasyon yapılır. Radyoloji ile instabil burst kırığı saptanıp nörolojik muayene tamamlandıktan sonra basıyı gidermek için acil cerrahi dekompresyon ve stabilizasyon uygulanır."
            },
            {
                "type": "estimate_slider",
                "items": [
                    {
                        "prompt": "Jefferson (C1 patlama) kırığında transvers ligamanın koptuğunu ve cerrahi gerektiğini gösteren lateral kütle taşma toplamı eşik değeri kaç milimetredir?",
                        "unit": "mm",
                        "min": 1,
                        "max": 15,
                        "step": 1,
                        "answer": 7,
                        "tolerance": 1,
                        "explanation": "Atlas lateral kütlelerinin odontoid üzerinden yana taşma toplamı 7 milimetreyi aştığında transvers ligaman kopmuş kabul edilir."
                    },
                    {
                        "prompt": "Tip II odontoid kırıklarında kaidenin avasküler yapısı nedeniyle konservatif tedaviyle kaynamama (psödoartroz) oranı ortalama yüzde kaçtır?",
                        "unit": "%",
                        "min": 50,
                        "max": 100,
                        "step": 5,
                        "answer": 85,
                        "tolerance": 5,
                        "explanation": "Tip II odontoid kırıkları zayıf kanlanma nedeniyle yüzde seksen ila doksan oranında konservatif tedaviyle iyileşmez."
                    },
                    {
                        "prompt": "Torakolomber kama kompresyon kırıklarında konservatif sınırı aşarak cerrahi stabilizasyon gerektiren korpus yükseklik kaybı (çökme) oranı en az yüzde kaçtır?",
                        "unit": "%",
                        "min": 10,
                        "max": 90,
                        "step": 5,
                        "answer": 50,
                        "tolerance": 5,
                        "explanation": "Vertebra korpus ön yüksekliğinde yüzde elliden fazla çökme olması omurga yük taşıma kapasitesini bozduğundan cerrahi endikasyondur."
                    }
                ]
            },
            {
                "type": "perturbation",
                "scenario": "Yüksekten düşme sonrası T4 seviyesinde tam kord kesisi ve akut nörojenik şok gelişen bir hastada yoğun bakım izleminde parametreler değerlendirilmektedir.",
                "question": "Bu patolojik süreçte aşağıdaki hemodinamik ve nörolojik parametreler travma öncesine kıyasla nasıl değişir?",
                "parameters": [
                    {
                        "name": "Sistemik vasküler rezistans (vazomotor sempatik tonus kaybına bağlı damar direnci)",
                        "correct": "down",
                        "explanation": "T6 üzeri lezyonlarda vazomotor sempatik liflerin kesilmesi yaygın vazodilatasyona ve vasküler direnç düşüşüne yol açar."
                    },
                    {
                        "name": "Kalp tepe atımı (kardiyak sempatik akseleratör liflerin kesilmesine bağlı nabız)",
                        "correct": "down",
                        "explanation": "Sempatik kardiyak liflerin devre dışı kalması ve baskılanmamış vagal tonus bradikardiye neden olur."
                    },
                    {
                        "name": "Venöz göllenme miktarı (vasküler yataktaki kan birikimi)",
                        "correct": "up",
                        "explanation": "Vazodilatasyon periferik venöz göllenmeyi artırarak kalbe dönen kan miktarını yani önyükü azaltır."
                    },
                    {
                        "name": "Lezyon seviyesi altında spinal şok evresindeki derin tendon refleksleri",
                        "correct": "down",
                        "explanation": "Spinal şok sırasında lezyon altındaki tüm refleks aktiviteler geçici olarak bütünüyle kaybolur."
                    }
                ]
            },
            {
                "type": "fix_the_text",
                "text": "Tip II odontoid kırığı dens apeksinde alar bağ avulsiyonu ile oluşur ve konservatif tedaviye mükemmel yanıt verir. Denis sınıflamasına göre omurgada orta kolon sağlam kaldığında omurga kesinlikle instabildir. C1 Jefferson kırığında lateral kütlelerin taşma toplamı 7 milimetrenin altında olduğunda transvers ligaman kopmuş kabul edilir.",
                "errors": [
                    {
                        "wrong": "dens apeksinde alar bağ avulsiyonu ile oluşur",
                        "correct": "odontoid kaidesinden kırılır ve psödoartroz riski çok yüksektir",
                        "options": [
                            "C2 vertebra cismi içine doğru uzanır",
                            "spinöz çıkıntının kopmasıyla meydana gelir"
                        ],
                        "explanation": "Apeksteki avulsiyon Tip I kırığa aittir; Tip II kırık odontoid kaidesindedir ve kanlanması yetersiz olduğundan kaynamama riski çok yüksektir."
                    },
                    {
                        "wrong": "kesinlikle instabildir",
                        "correct": "biyomekanik olarak stabildir",
                        "options": [
                            "acil cerrahiye alınmalıdır",
                            "üç kolon kırığı sayılır"
                        ],
                        "explanation": "Denis modeline göre orta kolon sağlam kaldığında örneğin izole anterior kolon kama kırığında omurga biyomekanik olarak stabil kabul edilir."
                    },
                    {
                        "wrong": "altında olduğunda",
                        "correct": "üzerinde olduğunda",
                        "options": [
                            "hizasında kaldığında",
                            "gerisinde ölçüldüğünde"
                        ],
                        "explanation": "Jefferson kırığında transvers ligamanın koptuğunu gösteren patolojik sınır taşma toplamının yedi milimetrenin üzerinde olmasıdır."
                    }
                ]
            }
        ]
    }
]

deck["slides"] = slides_data
deck["totalSlides"] = len(slides_data)
deck["totalInteractiveElements"] = sum(len(s.get("interactiveElements", [])) for s in slides_data)
deck["interactiveRatio"] = round(deck["totalInteractiveElements"] / deck["totalSlides"], 2)

out_path = "meds_database_25_26/taslak/y25-k2-13-spinal-travmalar/deck.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(deck, f, ensure_ascii=False, indent=2)

print(f"Generated deck with {len(slides_data)} slides, {deck['totalInteractiveElements']} interactive elements.")
