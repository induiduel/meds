import json

def get_s10_slides():
    slides = [
        # S91
        {
            "slideNumber": 91,
            "title": "Robbins ve Amfi Notu Sentezi: Vulva Hastalıkları Kilit Spotlar",
            "subtitle": "Labia majora kıllı derisi, labia minora mukozası, vulvit ve Bartholin kisti",
            "clinicalFocus": "Sınav Sentezi ve Spot Bilgiler",
            "content": "Kurul 1 Tıbbi Patoloji amfi ders notu ve Robbins referansları doğrultusunda vulva hastalıklarının temel spotlarını sentezliyoruz.\n\n- **Anatomik Ayrım:** Vulva dış kadın genital organıdır; **labia majora kıllı deri** yapısındayken, **labia minora kılsız mukoza** örtüsünden oluşur. Hastalık spektrumunda en sık inflamatuvar lezyonlar görülür; maligniteler nadir fakat hayatı tehdit edicidir.\n- **Vulvit Patolojisi:** Çok nedenli reaktif veya enfeksiyöz tablodur; yoğun kaşıntı ve kaşıma travması tabloyu ağırlaştırır. Yaşlı kadınlarda idrar teması irritan kontakt dermatitin sık bir nedenidir.\n- **Bartholin Komplikasyonu:** Vulva posterolateralindeki Bartholin bezi boşaltım kanalının enfeksiyon ve inflamasyonla tıkanması, aşırı ağrılı **Bartholin kisti ve apsesine** yol açar; cerrahi drenaj ve antibiyoterapi gerektirir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Vulvada en sık inflamatuvar lezyonlar görülür; Bartholin bezi kanal tıkanıklığı ağrılı kist ve apse ile sonuçlanan en önemli vulvit komplikasyonudur.",
            "synthesisNarrative": "Kurul 1 Tıbbi Patoloji amfi ders notu ve Robbins referansları doğrultusunda vulva hastalıklarının temel spotlarını sentezliyoruz.\n\n- **Anatomik Ayrım:** Vulva dış kadın genital organıdır; **labia majora kıllı deri** yapısındayken, **labia minora kılsız mukoza** örtüsünden oluşur. Hastalık spektrumunda en sık inflamatuvar lezyonlar görülür; maligniteler nadir fakat hayatı tehdit edicidir.\n- **Vulvit Patolojisi:** Çok nedenli reaktif veya enfeksiyöz tablodur; yoğun kaşıntı ve kaşıma travması tabloyu ağırlaştırır. Yaşlı kadınlarda idrar teması irritan kontakt dermatitin sık bir nedenidir.\n- **Bartholin Komplikasyonu:** Vulva posterolateralindeki Bartholin bezi boşaltım kanalının enfeksiyon ve inflamasyonla tıkanması, aşırı ağrılı **Bartholin kisti ve apsesine** yol açar; cerrahi drenaj ve antibiyoterapi gerektirir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Vulvada en sık inflamatuvar lezyonlar görülür; Bartholin bezi kanal tıkanıklığı ağrılı kist ve apse ile sonuçlanan en önemli vulvit komplikasyonudur.",
            "bulletPoints": [
                "Labia majora kıllı deri, labia minora ise kılsız mukozadır.",
                "Vulvada en sık inflamatuvar lezyonlar (vulvit) görülür.",
                "Bartholin kisti ve apsesi vulvitin en önemli anatomik komplikasyonudur."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vulva posterolateralindeki bez kanalının tıkanmasıyla oluşan ağrılı şişliğe Bartholin kisti adı verilir.",
                    "maskedTerm": "Bartholin kisti",
                    "hint": "Vulvit komplikasyonu olarak gelişen ve apseleşebilen glandüler kist"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulva Anatomisi ve Temel Lezyon Dağılımı",
                    "tableHeaders": ["Anatomik Bölge / Bez", "Doku Tipi", "En Sık Karşılaşılan Patoloji"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Labia Majora", "isMasked": False},
                                {"text": "Kıllı deri, sebase ve ter bezleri", "isMasked": True, "hint": "foliküllü deri örtüsü"},
                                {"text": "Kontakt dermatit, folikülit, skuamöz hiperplazi"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Bartholin Bezi", "isMasked": False},
                                {"text": "Müsin salgılayan posterolateral gland", "isMasked": False},
                                {"text": "Kanal obstrüksiyonu, kist ve akut apse", "isMasked": True, "hint": "ağrılı retansiyon lezyonu"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Kanal Tıkanıklığından Bartholin Apsesine",
                    "steps": [
                        "1. Duktal İnflamasyon: Enfeksiyon veya travma Bartholin bezi ana kanalını daraltır.",
                        "2. Mukus Retansiyonu: Salgı akamaz ve bez genişleyerek Bartholin kisti oluşturur.",
                        "3. Bakteriyel Süperenfeksiyon: Kist lümenine piyojenik bakteriler (stafilokok/gonokok) girer.",
                        "4. Akut Apse: Şiddetli zonklayıcı ağrı, kızarıklık ve fluktuasyon veren apse boşaltılır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulva hastalıkları spektrumunda klinik pratikte en sık görülen lezyon grubu ile Bartholin bezi kanal tıkanıklığı komplikasyonu nedir?",
                    "answer": "En sık inflamatuvar lezyonlar (vulvit) görülür; kanal tıkanıklığı ise ağrılı Bartholin kisti ve apsesine yol açar."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vulva Kilit Spotlar",
                    "items": [
                        {"text": "Labia majora kıllı deri, labia minora mukoza örtüsündedir.", "isLie": False, "explanation": "Doğru. Temel anatomi ayrımıdır."},
                        {"text": "Vulvada en sık inflamatuvar süreçler izlenir.", "isLie": False, "explanation": "Doğru. Amfi notunun kilit cümlesidir."},
                        {"text": "Bartholin kanal tıkanması apse ve kiste neden olabilir.", "isLie": False, "explanation": "Doğru. Sık komplikasyondur."},
                        {"text": "Bartholin bezi doğrudan beyin omurilik sıvısı salgılayan bir beyin ventrikülüdür.", "isLie": True, "explanation": "Tuzak! Bartholin bezi vulvada mukus salgılayan bir dış genital bezdir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvanın yapısı ve hastalıkları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Labia majora kıllı deri, labia minora mukozadır; en sık inflamatuvar lezyonlar görülür ve Bartholin kisti önemli bir komplikasyondur",
                            "isCorrect": True,
                            "explanation": "Bu sentez cümlesi amfi notundaki vulva anatomisi ve vulvit prensiplerini eksiksiz özetler."
                        },
                        {
                            "key": "B",
                            "text": "Vulvada hiçbir zaman yangısal lezyon görülemez, sadece kemik tümörleri oluşur",
                            "isCorrect": False,
                            "explanation": "En sık lezyonlar inflamatuvar süreçlerdir."
                        },
                        {
                            "key": "C",
                            "text": "Bartholin bezi yalnızca erkeklerde prostatın içinde yer alır",
                            "isCorrect": False,
                            "explanation": "Kadın dış genital sistemine aittir."
                        },
                        {
                            "key": "D",
                            "text": "Vulvit hastalarında kaşıma eylemi hastalığı derhal 1 saniyede iyileştirir",
                            "isCorrect": False,
                            "explanation": "Kaşıma travması tabloyu daha da ağırlaştırır."
                        }
                    ]
                }
            ]
        },
        # S92
        {
            "slideNumber": 92,
            "title": "Non-Neoplastik Bozukluklar ve Lökoplaki Kilit Spotlar",
            "subtitle": "Liken skleroz dermal fibrozisi vs skuamöz hiperplazi akantozu ve biyopsi zorunluluğu",
            "clinicalFocus": "Sınav Sentezi ve Ayırıcı Tanı",
            "content": "Vulvanın non-neoplastik epitel bozuklukları, klinikte kazımakla çıkmayan beyaz plaklar (**lökoplaki**) şeklinde karşımıza çıkar ve sınavların en sevilen ayırıcı tanı sahasıdır.\n\n- **Liken Skleroz Histopatolojisi:** Epidermiste **belirgin incelme**, rete çıkıntılarının kaybı, yüzeysel dermiste **homojen hücresiz asellüler fibrozis (kollajenleşme)** ve altında bant tarzında lenfositik infiltrat izlenir. Liken skleroz prekanseröz lezyon değildir ancak karsinom riski biraz artmıştır.\n- **Skuamöz Hücre Hiperplazisi:** Eski adıyla liken simpleks kronikus; kaşıma travmasına bağlı gelişir. Histolojisinde liken sklerozun tam tersine **epidermis kalınlaşması (akantoz)** ve hiperkeratoz izlenir; sitolojik atipi yoktur.\n- **Lökoplakide Biyopsi Zorunluluğu:** Psoriasis ve liken planus gibi selim dermatozlardan in situ veya invaziv karsinoma kadar çok geniş bir spektrum lökoplaki yapabildiğinden, **her lökoplakide biyopsi şarttır**.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Liken sklerozda epidermis incelmesi ve dermal fibrozis; skuamöz hiperplazide ise epidermis kalınlaşması (akantoz) ve hiperkeratoz görülür; her ikisinde de biyopsi zorunludur.",
            "synthesisNarrative": "Vulvanın non-neoplastik epitel bozuklukları, klinikte kazımakla çıkmayan beyaz plaklar (**lökoplaki**) şeklinde karşımıza çıkar ve sınavların en sevilen ayırıcı tanı sahasıdır.\n\n- **Liken Skleroz Histopatolojisi:** Epidermiste **belirgin incelme**, rete çıkıntılarının kaybı, yüzeysel dermiste **homojen hücresiz asellüler fibrozis (kollajenleşme)** ve altında bant tarzında lenfositik infiltrat izlenir. Liken skleroz prekanseröz lezyon değildir ancak karsinom riski biraz artmıştır.\n- **Skuamöz Hücre Hiperplazisi:** Eski adıyla liken simpleks kronikus; kaşıma travmasına bağlı gelişir. Histolojisinde liken sklerozun tam tersine **epidermis kalınlaşması (akantoz)** ve hiperkeratoz izlenir; sitolojik atipi yoktur.\n- **Lökoplakide Biyopsi Zorunluluğu:** Psoriasis ve liken planus gibi selim dermatozlardan in situ veya invaziv karsinoma kadar çok geniş bir spektrum lökoplaki yapabildiğinden, **her lökoplakide biyopsi şarttır**.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Liken sklerozda epidermis incelmesi ve dermal fibrozis; skuamöz hiperplazide ise epidermis kalınlaşması (akantoz) ve hiperkeratoz görülür; her ikisinde de biyopsi zorunludur.",
            "bulletPoints": [
                "Liken sklerozda epidermis incelir, dermiste homojen fibrozis oluşur.",
                "Skuamöz hücre hiperplazisinde epidermis kalınlaşır (akantoz) ve hiperkeratoz izlenir.",
                "Her lökoplaki lezyonunda ayırıcı tanı için biyopsi zorunludur."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Skuamöz hücre hiperplazisinde kaşıma travmasına bağlı olarak epidermis kalınlaşması yani akantoz tablosu izlenir.",
                    "maskedTerm": "akantoz",
                    "hint": "Stratum spinosum katmanının kalınlaşması histolojik terimi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Liken Skleroz vs Skuamöz Hücre Hiperplazisi",
                    "tableHeaders": ["Histolojik Parametre", "Liken Skleroz", "Skuamöz Hücre Hiperplazisi"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Epidermis Kalınlığı", "isMasked": False},
                                {"text": "Belirgin incelme ve atrofi", "isMasked": True, "hint": "tabakanın incelmesi"},
                                {"text": "Belirgin kalınlaşma (akantoz)"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Yüzeysel Dermis", "isMasked": False},
                                {"text": "Hücresiz homojen dermal fibrozis", "isMasked": True, "hint": "sklerotik hyalinize bant"},
                                {"text": "Normal bağ dokusu / hafif inflamasyon"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Beyaz Plaktan Kesin Histolojik Tanıya",
                    "steps": [
                        "1. Lökoplaki: Vulvada kazınamayan beyaz leke görülür.",
                        "2. Biyopsi Zorunluluğu: Klinik tanı yeterli olmadığından punch biyopsi yapılır.",
                        "3. Doku Analizi: Mikroskopta epidermis kalınlığı ve dermal kollajen incelenir.",
                        "4. Ayrım: İnce epidermis sklerozu, kalınlaşmış epidermis hiperplaziyi kesinleştirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Liken skleroz ile skuamöz hücre hiperplazisinin histopatolojik kesitlerdeki en temel epidermik ve dermal zıtlığı nedir?",
                    "answer": "Liken sklerozda epidermis incelmiş ve dermiste asellüler homojen fibrozis vardır; skuamöz hiperplazide ise epidermis kalınlaşmış (akantoz) ve hiperkeratoz mevcuttur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Liken Skleroz ve Lökoplaki",
                    "items": [
                        {"text": "Liken sklerozda epidermiste incelme ve rete kaybı izlenir.", "isLie": False, "explanation": "Doğru. Tipik atrofik histolojidir."},
                        {"text": "Skuamöz hiperplazide akantoz ve hiperkeratoz belirgindir.", "isLie": False, "explanation": "Doğru. Kaşıma yanıtıdır."},
                        {"text": "Lökoplakide karsinomu dışlamak için biyopsi zorunludur.", "isLie": False, "explanation": "Doğru. Temel klinik ilkedir."},
                        {"text": "Liken skleroz tanısı konduğu anda hastada yüksek dereceli invaziv sarkom başlamıştır.", "isLie": True, "explanation": "Tuzak! Liken skleroz prekanseröz dahi değildir; non-neoplastik inflamatuvar bir dermatozdur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulva lökoplakisi ve non-neoplastik epitel bozuklukları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Liken sklerozda epidermis incelmesi ve homojen dermal fibrozis varken, skuamöz hiperplazide akantoz izlenir ve her lökoplakide biyopsi şarttır",
                            "isCorrect": True,
                            "explanation": "Bu sentez amfi notundaki histolojik farkları ve lökoplaki biyopsi kuralını kusursuz özetler."
                        },
                        {
                            "key": "B",
                            "text": "Liken sklerozda epidermis 1 metre kalınlığa ulaşarak boynuz üretir",
                            "isCorrect": False,
                            "explanation": "Epidermis belirgin biçimde incelir."
                        },
                        {
                            "key": "C",
                            "text": "Skuamöz hiperplazi hastalarında biyopsi yapılması kanunen yasaklanmıştır",
                            "isCorrect": False,
                            "explanation": "Biyopsi ayırıcı tanı için zorunludur."
                        },
                        {
                            "key": "D",
                            "text": "Lökoplaki daima sadece akciğer bronşlarında gelişen bir hastalıktır",
                            "isCorrect": False,
                            "explanation": "Vulva ve mukozalarda görülen beyaz plaktır."
                        }
                    ]
                }
            ]
        },
        # S93
        {
            "slideNumber": 93,
            "title": "Kondilomlar ve Viral Lezyonlar Kilit Spotlar",
            "subtitle": "Kondiloma akuminatum (HPV 6/11) vs Kondiloma lata (T. pallidum) ve koilositoz",
            "clinicalFocus": "Sınav Sentezi ve Viral Morfoloji",
            "content": "Amfi ders notunun en sık soru çıkan başlıklarından biri genital siğil benzeri kabarık lezyonlar olan **kondilomların ayırıcı tanısıdır**.\n\n- **Kondiloma Akuminatum:** En yaygın kondilom tipidir. **Düşük riskli HPV tip 6 ve 11** enfeksiyonu ile gelişir. Papiller, ekzofitik, karnabahar benzeri lezyonlardır. Histolojisinde patognomonik **koilositik atipi** (büyümüş hiperkromatik buruşuk nükleus ve geniş perinükleer berrak halo) izlenir. Kondiloma akuminatum kansere dönüşmez.\n- **Kondiloma Lata:** Sekonder sifiliz tablosunda görülür; etkeni **Treponema pallidum**'dur. Akuminatum gibi papiller değil, **düz ve hafif kabarık plaklar** şeklindedir; sifiliz tedavisiyle hızla geriler.\n- **Aşı Koruması:** Kuadrivalan ve dokuz değerli HPV aşıları tip 6 ve 11'i içerdiğinden kondiloma akuminatum gelişimine karşı tam koruma sağlar.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Kondiloma akuminatum düşük riskli HPV 6 ve 11 kaynaklıdır, koilositoz içerir ve kansere dönüşmez; Kondiloma lata ise sekonder sifiliz (T. pallidum) lezyonudur ve düzdür.",
            "synthesisNarrative": "Amfi ders notunun en sık soru çıkan başlıklarından biri genital siğil benzeri kabarık lezyonlar olan **kondilomların ayırıcı tanısıdır**.\n\n- **Kondiloma Akuminatum:** En yaygın kondilom tipidir. **Düşük riskli HPV tip 6 ve 11** enfeksiyonu ile gelişir. Papiller, ekzofitik, karnabahar benzeri lezyonlardır. Histolojisinde patognomonik **koilositik atipi** (büyümüş hiperkromatik buruşuk nükleus ve geniş perinükleer berrak halo) izlenir. Kondiloma akuminatum kansere dönüşmez.\n- **Kondiloma Lata:** Sekonder sifiliz tablosunda görülür; etkeni **Treponema pallidum**'dur. Akuminatum gibi papiller değil, **düz ve hafif kabarık plaklar** şeklindedir; sifiliz tedavisiyle hızla geriler.\n- **Aşı Koruması:** Kuadrivalan ve dokuz değerli HPV aşıları tip 6 ve 11'i içerdiğinden kondiloma akuminatum gelişimine karşı tam koruma sağlar.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Kondiloma akuminatum düşük riskli HPV 6 ve 11 kaynaklıdır, koilositoz içerir ve kansere dönüşmez; Kondiloma lata ise sekonder sifiliz (T. pallidum) lezyonudur ve düzdür.",
            "bulletPoints": [
                "Kondiloma akuminatum HPV 6 ve 11 ile oluşur, koilositoz gösterir ve kanserleşmez.",
                "Kondiloma lata sekonder sifilizde (Treponema pallidum) görülen düz kabarıklıktır.",
                "HPV aşıları tip 6 ve 11'i kapsayarak siğilleri önler."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Kondiloma akuminatum histopatolojisinde HPV sitopatik etkisini gösteren perinükleer halolu hücrelere koilosit adı verilir.",
                    "maskedTerm": "koilosit",
                    "hint": "Buruşuk çekirdek ve etrafında şeffaf boşluk içeren epitel hücresi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Kondilomların Karşılaştırmalı Sınav Tablosu",
                    "tableHeaders": ["Özellik", "Kondiloma Akuminatum", "Kondiloma Lata"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Etyolojik Etken", "isMasked": False},
                                {"text": "Düşük riskli HPV tip 6 ve 11", "isMasked": True, "hint": "siğil virüsleri"},
                                {"text": "Treponema pallidum (Spiroket)"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Makroskopi ve Morfoloji", "isMasked": False},
                                {"text": "Papiller, ekzofitik, karnabahar benzeri", "isMasked": False},
                                {"text": "Geniş tabanlı, düz ve hafif kabarık", "isMasked": True, "hint": "sifilitik düz plak görünümü"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "HPV 6/11'den Kondiloma Akuminatuma",
                    "steps": [
                        "1. Viral İnokülasyon: HPV 6 veya 11 anogenital skuamöz epitele bulaşır.",
                        "2. Sitopatik Etki: Epitel hücrelerinde koilositik atipi ve akantoz başlar.",
                        "3. Papillomatozis: Damarlı fibrovasküler korlar üzerinde karnabahar benzeri büyüme oturur.",
                        "4. Biyolojik Karakter: Malign transformasyon göstermeden selim siğil olarak seyreder."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Kondiloma akuminatum ile kondiloma lata arasındaki etken mikroorganizma ve morfolojik lezyon farkı nedir?",
                    "answer": "Kondiloma akuminatum HPV 6 ve 11 kaynaklı papiller ekzofitik lezyondur; kondiloma lata ise Treponema pallidum (sekonder sifiliz) kaynaklı düz kabarık lezyondur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Kondilomlar",
                    "items": [
                        {"text": "Kondiloma akuminatum HPV 6 ve 11 enfeksiyonuna bağlıdır.", "isLie": False, "explanation": "Doğru. Düşük riskli tiplerdir."},
                        {"text": "Histolojisinde patognomonik koilositoz izlenir.", "isLie": False, "explanation": "Doğru. Tipik viral değişikliktir."},
                        {"text": "Kondiloma lata sekonder sifilizde görülen düz lezyondur.", "isLie": False, "explanation": "Doğru. T. pallidum etkenidir."},
                        {"text": "Kondiloma akuminatum olgularının %100'ü 1 ay içinde ölümcül kemik kanserine dönüşür.", "isLie": True, "explanation": "Tuzak! Kondiloma akuminatum selimdir, kansere dönüşmez."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Kondiloma akuminatum ve kondiloma lata ile ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Kondiloma akuminatum HPV 6/11 ilişkili papiller lezyondur; kondiloma lata ise Treponema pallidum ilişkili düz lezyondur",
                            "isCorrect": True,
                            "explanation": "Akuminatum HPV 6/11 kaynaklı ekzofitik siğildir; lata sekonder sifiliz spiroketi lezyonudur."
                        },
                        {
                            "key": "B",
                            "text": "Kondiloma akuminatum kuduz virüsüyle oluşan beyin apsesidir",
                            "isCorrect": False,
                            "explanation": "Genital siğildir."
                        },
                        {
                            "key": "C",
                            "text": "Kondiloma lata yalnızca gözün korneasında gelişir",
                            "isCorrect": False,
                            "explanation": "Anogenital bölge ve ciltte sekonder sifiliz bulgusudur."
                        },
                        {
                            "key": "D",
                            "text": "Her iki kondilom tipi de kesinlikle hiçbir mikroorganizma içermez",
                            "isCorrect": False,
                            "explanation": "Biri HPV virüsü, diğeri Treponema bakterisi içerir."
                        }
                    ]
                }
            ]
        },
        # S94
        {
            "slideNumber": 94,
            "title": "Vulvar Karsinom ve VIN İkili Yolu Kilit Spotlar",
            "subtitle": "HPV pozitif bazaloid yol (VIN) vs HPV negatif keratinize yol (dVIN/liken skleroz)",
            "clinicalFocus": "Sınav Sentezi ve İkili Karsinogenez",
            "content": "Vulvar karsinomlar kadın genital kanserlerinin ~%3'ünü oluşturur ve ~%90'ı skuamöz hücreli karsinomdur (SCC). Amfi ders notunun en kritik tablosu **iki farklı patogenetik yolun** karşılaştırılmasıdır.\n\n- **1. HPV Pozitif Yol (Bazaloid / Siğil Benzeri Karsinom):** Yüksek riskli **HPV tip 16** ile ilişkilidir. Hastalar daha gençtir (ortalama yaş ~60), sıklıkla sigara içerler. Öncesinde klasik **VIN (uVIN)** bulunur. Çoğunlukla **çok odaklıdır (multifokal)** ve mikroskopide kötü diferansiye bazaloid morfoloji izlenir.\n- **2. HPV Negatif Yol (Keratinize Skuamöz Karsinom):** HPV ile ilişkisizdir. İleri yaştaki kadınlarda görülür (**ortalama yaş ~75**). Uzun süreli **liken skleroz veya skuamöz hiperplazi** zemininde gelişir. Öncü lezyonu **diferansiye VIN (dVIN)** olup p53 mutasyonu içerir. Genellikle **tek odaklıdır (unifokal)** ve iyi diferansiye keratinize SCC yapar.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] HPV pozitif vulvar karsinom gençlerde, çok odaklı ve kötü diferansiyedir; HPV negatif karsinom ise yaşlılarda (~75 yaş), liken skleroz zemininde, tek odaklı ve iyi diferansiye keratinizedir.",
            "synthesisNarrative": "Vulvar karsinomlar kadın genital kanserlerinin ~%3'ünü oluşturur ve ~%90'ı skuamöz hücreli karsinomdur (SCC). Amfi ders notunun en kritik tablosu **iki farklı patogenetik yolun** karşılaştırılmasıdır.\n\n- **1. HPV Pozitif Yol (Bazaloid / Siğil Benzeri Karsinom):** Yüksek riskli **HPV tip 16** ile ilişkilidir. Hastalar daha gençtir (ortalama yaş ~60), sıklıkla sigara içerler. Öncesinde klasik **VIN (uVIN)** bulunur. Çoğunlukla **çok odaklıdır (multifokal)** ve mikroskopide kötü diferansiye bazaloid morfoloji izlenir.\n- **2. HPV Negatif Yol (Keratinize Skuamöz Karsinom):** HPV ile ilişkisizdir. İleri yaştaki kadınlarda görülür (**ortalama yaş ~75**). Uzun süreli **liken skleroz veya skuamöz hiperplazi** zemininde gelişir. Öncü lezyonu **diferansiye VIN (dVIN)** olup p53 mutasyonu içerir. Genellikle **tek odaklıdır (unifokal)** ve iyi diferansiye keratinize SCC yapar.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] HPV pozitif vulvar karsinom gençlerde, çok odaklı ve kötü diferansiyedir; HPV negatif karsinom ise yaşlılarda (~75 yaş), liken skleroz zemininde, tek odaklı ve iyi diferansiye keratinizedir.",
            "bulletPoints": [
                "HPV pozitif yol: ~60 yaş, HPV-16, çok odaklı, kötü diferansiye bazaloid SCC.",
                "HPV negatif yol: ~75 yaş, liken skleroz zemini, dVIN (p53), unifokal, keratinize SCC.",
                "Vulvar karsinomların %90'ı skuamöz karsinomdur."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "HPV-negatif vulvar karsinom olguları genellikle unifokal yerleşim gösterir ve ortalama 75 yaş civarındaki kadınlarda görülür.",
                    "maskedTerm": "unifokal",
                    "hint": "Tek bir odakta ortaya çıkan tümöral büyüme"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulvar Karsinogenezin İkili Modeli",
                    "tableHeaders": ["Özellik", "HPV Pozitif Karsinom", "HPV Negatif Karsinom"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Ortalama Hasta Yaşı", "isMasked": False},
                                {"text": "~60 yaş (daha genç)", "isMasked": False},
                                {"text": "~75 yaş (ileri yaş)", "isMasked": True, "hint": "yaşlı kadın popülasyonu"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Zemin / Öncü Lezyon", "isMasked": False},
                                {"text": "Klasik VIN (uVIN)", "isMasked": False},
                                {"text": "Liken skleroz / Diferansiye VIN (dVIN)", "isMasked": True, "hint": "non-neoplastik dermatoz ve p53 mutasyonu"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Odaklanma ve Diferansiasyon", "isMasked": False},
                                {"text": "Çok odaklı (multifokal), bazaloid/kötü", "isMasked": True, "hint": "yaygın ve az diferansiye"},
                                {"text": "Genellikle unifokal, iyi diferansiye keratinize"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "İkili Vulvar Karsinogenez Yolu",
                    "steps": [
                        "1. Yol Ayrımı: Onkojenik HPV maruziyeti VEYA kronik liken skleroz zemininde p53 mutasyonu gelişir.",
                        "2. Prekanseröz Evre: HPV yolunda klasik VIN; liken yolunda ise diferansiye VIN (dVIN) oturur.",
                        "3. Tümör Odaklanması: HPV grubu multifokal yayılırken; liken grubu unifokal kitle yapar.",
                        "4. Histolojik Sonuç: Gençte bazaloid SCC; 75 yaşındaki kadında keratin incili keratinize SCC belirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulvar skuamöz karsinomun iki ana yolundan HPV-negatif olan grubun ortalama yaşı, öncü lezyonu ve histolojik diferansiasyonu nedir?",
                    "answer": "Ortalama yaş ~75'tir; öncü lezyonu liken skleroz zemininde gelişen dVIN'dir; histolojisi genellikle unifokal, iyi diferansiye keratinize skuamöz hücreli karsinomdur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vulvar Karsinogenez İkili Modeli",
                    "items": [
                        {"text": "HPV pozitif karsinomlar çoğunlukla çok odaklı ve kötü diferansiyedir.", "isLie": False, "explanation": "Doğru. Tip 16 ilişkili gruptur."},
                        {"text": "HPV negatif karsinomlar ~75 yaş civarında liken skleroz zemininde görülür.", "isLie": False, "explanation": "Doğru. Klasik yaşlı grup tablosudur."},
                        {"text": "dVIN HPV-negatif keratinize karsinomun öncü lezyonudur.", "isLie": False, "explanation": "Doğru. p53 mutasyonludur."},
                        {"text": "Vulva karsinomlarının %90'ı iyi huylu kemik iliği naklidir.", "isLie": True, "explanation": "Tuzak! Vulva kanserlerinin %90'ı malign skuamöz hücreli karsinomdur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvar skuamöz hücreli karsinomun iki patogenetik yolu karşılaştırıldığında aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "HPV pozitif karsinom gençlerde çok odaklı bazaloid seyrederken; HPV negatif karsinom ~75 yaşta liken skleroz zemininde unifokal keratinize seyreder",
                            "isCorrect": True,
                            "explanation": "Bu sentez amfi ders notundaki vulvar karsinom ikili karşılaştırma tablosunu birebir özetler."
                        },
                        {
                            "key": "B",
                            "text": "HPV negatif karsinomlar daima 5 yaşındaki kız çocuklarında görülür",
                            "isCorrect": False,
                            "explanation": "Ortalama yaş 75'tir."
                        },
                        {
                            "key": "C",
                            "text": "HPV pozitif karsinomlarda virüsün rolü hiçbir zaman kanıtlanamamıştır",
                            "isCorrect": False,
                            "explanation": "HPV tip 16 kanıtlanmış birincil etyolojik ajandır."
                        },
                        {
                            "key": "D",
                            "text": "Keratinize skuamöz karsinom sadece süt dişlerinin dökülmesiyle oluşur",
                            "isCorrect": False,
                            "explanation": "Tıbbi patolojiyle ilgisi yoktur."
                        }
                    ]
                }
            ]
        },
        # S95
        {
            "slideNumber": 95,
            "title": "Ekstramammary Paget Hastalığı Kilit Spotlar",
            "subtitle": "İntraepidermal atipik glandüler hücreler, dermatit taklidi ve meme Paget'ten ayrım",
            "clinicalFocus": "Sınav Sentezi ve Paget Patolojisi",
            "content": "Amfi notunun ve Robbins'in en karakteristik dermatopatolojik lezyonu **Ekstramammary Paget hastalığıdır**.\n\n- **Tanım ve Histogenez:** Apokrin/ekrin ter bezleri yönünde diferansiasyon gösteren atipik neoplastik glandüler hücrelerin vulva epidermisi içinde tek tek veya adalar halinde çoğalmasıdır.\n- **Klinik Görünüm ve Tuzak:** Labia majorada kırmızı, pullu, kabuklu, kaşıntılı plak yapar; **kronik kontakt dermatiti veya egzamayı mükemmel taklit eder**. Bu nedenle tanıda sıklıkla aylar/yıllar süren gecikmeler yaşanır.\n- **Meme Paget'inden En Kritik Ayrım:** Meme ucu Paget hastalığında olguların **neredeyse %100'ünde altta yatan bir duktal meme karsinomu** bulunurken; vulva Ekstramammary Paget hastalığında olguların büyük çoğunluğunda altta yatan bir tümör yoktur (primer intraepidermal süreçtir).\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Ekstramammary Paget kronik dermatiti taklit eder; meme Paget'inin aksine vulva Paget olgularının çoğunda altta yatan invaziv bir karsinom bulunmaz.",
            "synthesisNarrative": "Amfi notunun ve Robbins'in en karakteristik dermatopatolojik lezyonu **Ekstramammary Paget hastalığıdır**.\n\n- **Tanım ve Histogenez:** Apokrin/ekrin ter bezleri yönünde diferansiasyon gösteren atipik neoplastik glandüler hücrelerin vulva epidermisi içinde tek tek veya adalar halinde çoğalmasıdır.\n- **Klinik Görünüm ve Tuzak:** Labia majorada kırmızı, pullu, kabuklu, kaşıntılı plak yapar; **kronik kontakt dermatiti veya egzamayı mükemmel taklit eder**. Bu nedenle tanıda sıklıkla aylar/yıllar süren gecikmeler yaşanır.\n- **Meme Paget'inden En Kritik Ayrım:** Meme ucu Paget hastalığında olguların **neredeyse %100'ünde altta yatan bir duktal meme karsinomu** bulunurken; vulva Ekstramammary Paget hastalığında olguların büyük çoğunluğunda altta yatan bir tümör yoktur (primer intraepidermal süreçtir).\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Ekstramammary Paget kronik dermatiti taklit eder; meme Paget'inin aksine vulva Paget olgularının çoğunda altta yatan invaziv bir karsinom bulunmaz.",
            "bulletPoints": [
                "Atipik glandüler hücrelerin intraepidermal neoplastik yayılımıdır.",
                "Kırmızı, pullu plak görünümüyle kronik dermatiti taklit eder.",
                "Meme Paget'inden farklı olarak genellikle altta yatan karsinom yoktur."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Ekstramammary Paget hastalığı meme Paget'inin aksine genellikle altta yatan karsinom olmaksızın seyreder.",
                    "maskedTerm": "altta yatan karsinom",
                    "hint": "Meme ucunda daima bulunan derin malign duktal tümör"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Meme Ucu Paget vs Vulva Ekstramammary Paget",
                    "tableHeaders": ["Özellik", "Meme Ucu Paget Hastalığı", "Vulva Ekstramammary Paget"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Altta Yatan Karsinom", "isMasked": False},
                                {"text": "Neredeyse daima mevcut (%100 duktal Ca)", "isMasked": False},
                                {"text": "Çoğunlukla yoktur (primer intraepidermal)", "isMasked": True, "hint": "derin tümör bulunmama özelliği"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Klinik Taklit", "isMasked": False},
                                {"text": "Meme ucu egzaması", "isMasked": False},
                                {"text": "Kronik kontakt dermatit / egzema", "isMasked": True, "hint": "vulvar kırmızı kaşıntılı plak taklidi"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Ekstramammary Paget Tanı Zinciri",
                    "steps": [
                        "1. Klinik Plak: Vulvada kaşıntılı, eritemli ve pullu kırmızı plak belirir.",
                        "2. Egzema Yanılgısı: Hasta aylarca kontakt dermatit zannedilerek topikal kremlerle tedavi edilir.",
                        "3. Tedavi Direnci: Lezyon gerilemeyince alınan biyopside müsinöz Paget hücreleri görülür.",
                        "4. İntraepidermal Tedavi: Geniş lokal eksizyon uygulanır; genellikle altta derin tümör aranmaz."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulva Ekstramammary Paget hastalığını meme ucu Paget hastalığından ayıran en temel patolojik ve onkolojik fark nedir?",
                    "answer": "Meme Paget'inde neredeyse daima altta yatan invaziv veya in situ duktal karsinom bulunurken; vulva Paget hastalığında olguların çoğunda altta yatan bir karsinom bulunmaz, primer intraepidermal neoplazidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Ekstramammary Paget Hastalığı",
                    "items": [
                        {"text": "Ekstramammary Paget atipik glandüler hücrelerin intraepidermal proliferasyonudur.", "isLie": False, "explanation": "Doğru. Tanısal histopatolojidir."},
                        {"text": "Kırmızı pullu plak görünümüyle kronik dermatiti taklit eder.", "isLie": False, "explanation": "Doğru. Amfi notunun anahtar klinik bulgusudur."},
                        {"text": "Meme Paget'inden farklı olarak çoğunlukla altta yatan karsinom yoktur.", "isLie": False, "explanation": "Doğru. En sık sorulan sınav spotudur."},
                        {"text": "Paget hücreleri sadece saf kurşun metali salgılayan mekanik robotlardır.", "isLie": True, "explanation": "Tuzak! Paget hücreleri müsin salgılayan atipik glandüler epitel hücreleridir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Ekstramammary Paget hastalığı ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Vulva derisinde intraepidermal atipik glandüler hücre proliferasyonudur; kronik dermatiti taklit eder ve meme Paget'inden farklı olarak genelde altta karsinom yoktur",
                            "isCorrect": True,
                            "explanation": "Bu sentez amfi ders notundaki Ekstramammary Paget tanımı ve klinik özelliklerini eksiksiz kapsar."
                        },
                        {
                            "key": "B",
                            "text": "Daima hastanın saçlarında dökülmeyle başlar ve ayak parmaklarını tutar",
                            "isCorrect": False,
                            "explanation": "Vulva labiumlarında yerleşir."
                        },
                        {
                            "key": "C",
                            "text": "Tümör hücrelerinde kesinlikle hiçbir zaman müsin boyanması izlenmez",
                            "isCorrect": False,
                            "explanation": "Paget hücreleri müsin pozitiftir (PAS/Alcian blue ile boyanır)."
                        },
                        {
                            "key": "D",
                            "text": "Meme Paget'i ile birebir aynı olup her ikisinde de %100 akciğer kanseri bulunur",
                            "isCorrect": False,
                            "explanation": "Akciğer kanseri ile ilişkisi yoktur."
                        }
                    ]
                }
            ]
        },
        # S96
        {
            "slideNumber": 96,
            "title": "Vajina Anomalileri ve Gartner Kisti Kilit Spotlar",
            "subtitle": "Kalıcı Wolffian kanal kalıntısı, lateral vajinal duvar ve asemptomatik seyir",
            "clinicalFocus": "Sınav Sentezi ve Embriyoloji",
            "content": "Amfi notunda vajinanın genel özellikleri özetlenirken erişkinlerde primer hastalıkların nadir olduğu, komşu organ karsinomlarının (serviks, rektum, mesane) sekonder invazyonunun daha sık görüldüğü vurgulanır.\n\n- **Gartner Kanal Kisti:** Vajinanın en sık karşılaşılan kistik lezyonudur. Embriyolojik gelişim sırasında körelmesi gereken **mezonefrik (Wolffian) kanal kalıntılarının** sebat etmesiyle oluşur.\n- **Lokalizasyon:** Karakteristik olarak **lateral vajinal duvarda** submukozal yerleşim gösterir.\n- **Morfoloji ve Seyir:** İçi berrak sıvı dolu, tek katlı küboid veya kolumnar epitel ile döşeli kistlerdir. Çoğu tamamen selim ve asemptomatiktir; rutin pelvik muayenede tesadüfen saptanır; ancak devasa boyutlara ulaştığında bası veya disparoni semptomu verebilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Gartner kanal kisti, lateral vajinal duvarda yerleşen ve kalıcı Wolffian (mezonefrik) kanal kalıntısından gelişen benign bir kisttir.",
            "synthesisNarrative": "Amfi notunda vajinanın genel özellikleri özetlenirken erişkinlerde primer hastalıkların nadir olduğu, komşu organ karsinomlarının (serviks, rektum, mesane) sekonder invazyonunun daha sık görüldüğü vurgulanır.\n\n- **Gartner Kanal Kisti:** Vajinanın en sık karşılaşılan kistik lezyonudur. Embriyolojik gelişim sırasında körelmesi gereken **mezonefrik (Wolffian) kanal kalıntılarının** sebat etmesiyle oluşur.\n- **Lokalizasyon:** Karakteristik olarak **lateral vajinal duvarda** submukozal yerleşim gösterir.\n- **Morfoloji ve Seyir:** İçi berrak sıvı dolu, tek katlı küboid veya kolumnar epitel ile döşeli kistlerdir. Çoğu tamamen selim ve asemptomatiktir; rutin pelvik muayenede tesadüfen saptanır; ancak devasa boyutlara ulaştığında bası veya disparoni semptomu verebilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Gartner kanal kisti, lateral vajinal duvarda yerleşen ve kalıcı Wolffian (mezonefrik) kanal kalıntısından gelişen benign bir kisttir.",
            "bulletPoints": [
                "Gartner kisti kalıcı Wolffian (mezonefrik) kanal kalıntısıdır.",
                "Karakteristik olarak lateral vajinal duvarda yerleşir.",
                "Çoğunlukla selim ve asemptomatiktir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Gartner kanal kisti embriyolojik mezonefrik kanal kalıntısından gelişir ve lateral duvarda yerleşir.",
                    "maskedTerm": "mezonefrik",
                    "hint": "Wolffian kanalının diğer bilimsel adı"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vajinal Kistlerin Embriyolojik Kökeni",
                    "tableHeaders": ["Kist Türü", "Embriyolojik Köken", "Anatomik Lokalizasyon"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Gartner Kanal Kisti", "isMasked": False},
                                {"text": "Wolffian (Mezonefrik) kanal artığı", "isMasked": True, "hint": "erkek taslağından kalan mezonefroz kanalı"},
                                {"text": "Lateral vajinal duvar submukozası"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Müllerian Kist", "isMasked": False},
                                {"text": "Paramezonefrik (Müllerian) kanal artığı", "isMasked": False},
                                {"text": "Üst vajina ve forniksler", "isMasked": True, "hint": "paramezonefrik kalıntı sahası"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Kalıntı Kanaldan Gartner Kistine",
                    "steps": [
                        "1. Embriyogenez: Dişi fetüste mezonefrik kanal körelirken lateral duvarda kalıntı tübüller kalır.",
                        "2. Sıvı Birikimi: Epitel lümen içine berrak seröz sekresyon salgılamaya devam eder.",
                        "3. Kist Şekillenmesi: Yavaşça genişleyerek lateral vajinal duvarda gergin kist oluşturur.",
                        "4. Klinik Tespit: Muayenede lateral duvarda submukozal fluktuasyon veren kist saptanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vajina lateral duvarında saptanan Gartner kanal kistinin embriyolojik kökeni nedir?",
                    "answer": "Kalıcı Wolffian (mezonefrik) kanal kalıntısıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Gartner Kanal Kisti",
                    "items": [
                        {"text": "Gartner kisti kalıcı Wolffian kanal kalıntısından köken alır.", "isLie": False, "explanation": "Doğru. Amfi notunun kilit bilgisidir."},
                        {"text": "Lateral vajinal duvarda submukozal yerleşir.", "isLie": False, "explanation": "Doğru. Karakteristik lokalizasyondur."},
                        {"text": "Çoğu lezyon benign ve asemptomatiktir.", "isLie": False, "explanation": "Doğru. Selim kistlerdir."},
                        {"text": "Gartner kisti doğrudan akciğerde hava kesesi oluşturan bir amfizem türüdür.", "isLie": True, "explanation": "Tuzak! Gartner kisti vajina lateral duvarında yerleşen jinekolojik bir embriyolojik kisttir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vajina muayenesinde lateral vajinal duvarda submukozal yerleşimli, asemptomatik kistik lezyon saptanan bir hastada en olası tanı ve bu lezyonun embriyolojik kökeni nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Gartner kanal kisti; kalıcı Wolffian (mezonefrik) kanal kalıntısı",
                            "isCorrect": True,
                            "explanation": "Gartner kisti lateral vajinal duvarda Wolffian kanal kalıntısından gelişir."
                        },
                        {
                            "key": "B",
                            "text": "Akut apandisit apsesi; çekum perforasyonu",
                            "isCorrect": False,
                            "explanation": "Batın cerrahisi patolojisidir."
                        },
                        {
                            "key": "C",
                            "text": "Embriyonel rabdomiyosarkom; çizgili kas diferansiasyonu",
                            "isCorrect": False,
                            "explanation": "Pediatrik malign tümördür, selim kist değildir."
                        },
                        {
                            "key": "D",
                            "text": "Göz kataraktı; lens bulanıklaşması",
                            "isCorrect": False,
                            "explanation": "Göz hastalığıdır."
                        }
                    ]
                }
            ]
        },
        # S97
        {
            "slideNumber": 97,
            "title": "Vajinit Tipleri ve Mikroskobik Bulguları Kilit Spotlar",
            "subtitle": "Candida (hif/Pap), Trichomonas (hareketli parazit/CYBH) ve Gardnerella (Clue cells/balık kokusu)",
            "clinicalFocus": "Sınav Sentezi ve Mikroskopi",
            "content": "Amfi ders notunun tablo ve metin olarak en detaylı işlediği, çıkmış açık uçlu sorularda doğrudan yer alan başlık **üç majör vajinit etkeninin ayırıcı tanısıdır**.\n\n- **1. Candida albicans:** Kadınların %20'sinde normal kommensal flora üyesidir. Diyabet, antibiyotik, gebelik ve immün yetmezlikte patojenleşir. **Cinsel yolla bulaşmaz**. Kalın, beyaz, **peynirimsi (süt kesiği)** akıntı, şiddetli kaşıntı ve yanma yapar. Tanısı **Pap testinde veya ıslak yaymada hif ve psödohiflerin** gösterilmesiyle konur.\n- **2. Trichomonas vaginalis:** **Dünya çapında en yaygın viral olmayan CYBH'dır**. Cinsel temasla bulaşır. Bol, sulu, köpüklü, **gri-yeşil akıntı** ve çilek serviks yapar. Tanısı direkt mikroskopide **kamçılı hareketli trofozoitin** gösterilmesidir.\n- **3. Gardnerella vaginalis:** Bakteriyel vajinozun ana etkenidir. İnce, homojen, gri-beyaz akıntı ve amin koku testiyle tipik **'balık kokusu'** verir. Tanıda patognomonik bulgu **Clue cells (ipucu hücreleri)** olup, yüzeyi basillerle kaplanmış sınırları silik skuamöz epitel hücreleridir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Candida cinsel yolla bulaşmaz (peynirimsi akıntı + hif); Trichomonas en yaygın non-viral CYBH'dır (gri-yeşil akıntı + hareketli parazit); Gardnerella ise balık kokusu ve Clue cells ile karakterizedir.",
            "synthesisNarrative": "Amfi ders notunun tablo ve metin olarak en detaylı işlediği, çıkmış açık uçlu sorularda doğrudan yer alan başlık **üç majör vajinit etkeninin ayırıcı tanısıdır**.\n\n- **1. Candida albicans:** Kadınların %20'sinde normal kommensal flora üyesidir. Diyabet, antibiyotik, gebelik ve immün yetmezlikte patojenleşir. **Cinsel yolla bulaşmaz**. Kalın, beyaz, **peynirimsi (süt kesiği)** akıntı, şiddetli kaşıntı ve yanma yapar. Tanısı **Pap testinde veya ıslak yaymada hif ve psödohiflerin** gösterilmesiyle konur.\n- **2. Trichomonas vaginalis:** **Dünya çapında en yaygın viral olmayan CYBH'dır**. Cinsel temasla bulaşır. Bol, sulu, köpüklü, **gri-yeşil akıntı** ve çilek serviks yapar. Tanısı direkt mikroskopide **kamçılı hareketli trofozoitin** gösterilmesidir.\n- **3. Gardnerella vaginalis:** Bakteriyel vajinozun ana etkenidir. İnce, homojen, gri-beyaz akıntı ve amin koku testiyle tipik **'balık kokusu'** verir. Tanıda patognomonik bulgu **Clue cells (ipucu hücreleri)** olup, yüzeyi basillerle kaplanmış sınırları silik skuamöz epitel hücreleridir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Candida cinsel yolla bulaşmaz (peynirimsi akıntı + hif); Trichomonas en yaygın non-viral CYBH'dır (gri-yeşil akıntı + hareketli parazit); Gardnerella ise balık kokusu ve Clue cells ile karakterizedir.",
            "bulletPoints": [
                "Candida cinsel yolla bulaşmaz; peynirimsi akıntı ve hif formları izlenir.",
                "Trichomonas en sık non-viral CYBH'dır; gri-yeşil akıntı ve hareketli parazit görülür.",
                "Gardnerella bakteriyel vajinoz yapar; balık kokusu ve clue cells patognomoniktir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Bakteriyel vajinozda yüzeyi kokobasillerle kaplanmış yassı epitel hücrelerine clue cells adı verilir.",
                    "maskedTerm": "clue cells",
                    "hint": "İpucu hücresi olarak da adlandırılan patognomonik sitoloji bulgusu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Üç Majör Vajinit Etkeninin Sınav Karşılaştırma Matrisi",
                    "tableHeaders": ["Etken", "Bulaş Yolu / CYBH?", "Klinik Akıntı Tipi", "Mikroskobik Tanı Kanıtı"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Candida albicans", "isMasked": False},
                                {"text": "Cinsel yolla bulaşmaz (flora üyesi)", "isMasked": True, "hint": "CYBH olmayan fırsatçı mantar"},
                                {"text": "Kalın, beyaz, peynirimsi / süt kesiği", "isMasked": False},
                                {"text": "Pap smear / ıslak yaymada hif ve sporlar"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Trichomonas vaginalis", "isMasked": False},
                                {"text": "Dünyada en sık viral olmayan CYBH", "isMasked": False},
                                {"text": "Bol, sulu, köpüklü, gri-yeşil akıntı", "isMasked": True, "hint": "yeşilimsi sulu lökore"},
                                {"text": "Direkt mikroskopide hareketli kamçılı parazit"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Gardnerella vaginalis", "isMasked": False},
                                {"text": "Flora dengesizliği (disbiyozis)", "isMasked": False},
                                {"text": "İnce gri-beyaz, tipik balık kokulu", "isMasked": False},
                                {"text": "Clue cells (kokobasille kaplı yassı epitel)", "isMasked": True, "hint": "sınırları belirsizleşmiş epitel hücresi"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Vajinal Akıntıdan Etken Teşhisine",
                    "steps": [
                        "1. Akıntı Muayenesi: Peynirimsi, yeşil veya balık kokulu lökore ayrımı yapılır.",
                        "2. Islak Yayma: Serum fizyolojik ile lam üzerinde mikroskopiye bakılır.",
                        "3. Karakteristik İşaret: Hareketli protozoon, fungal hif veya clue cell saptanır.",
                        "4. Spesifik Tedavi: Candida'ya antifungal, Trichomonas/Gardnerella'ya metronidazol başlanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Çıkmış kurul sorusunda da sorgulanan; dünyada cinsel yolla bulaşan hastalıklar arasında SAYILMAYAN ancak sık görülen vajinit/vulvit etkeni hangisidir ve mikroskopik tanı bulgusu nedir?",
                    "answer": "Candida türleridir (cinsel yolla bulaşmaz); mikroskopide hif ve psödohif yapılarının gösterilmesiyle tanı konur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajinit Tipleri",
                    "items": [
                        {"text": "Candida türleri vulvit ve vajinit yapar ancak cinsel yolla bulaşmaz.", "isLie": False, "explanation": "Doğru. Amfi notunun net çıkmış spotudur."},
                        {"text": "Trichomonas dünyada en yaygın viral olmayan CYBH'dır.", "isLie": False, "explanation": "Doğru. Hareketli parazittir."},
                        {"text": "Gardnerella bakteriyel vajinoz etkenidir ve clue cells yapar.", "isLie": False, "explanation": "Doğru. Patognomonik mikroskopidir."},
                        {"text": "Candida mantarları insan vücudunda yalnızca saf demir çivi üretir.", "isLie": True, "explanation": "Tuzak! Candida mantardır, demir çivi üretmez; tomurcuklanan maya ve hifler oluşturur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Kadın genital sisteminde gelişen vajinit etkenleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Candida cinsel yolla bulaşmaz ve hif gösterilmesiyle tanınır; Trichomonas en sık non-viral CYBH'dır; Gardnerella ise Clue cells yapar",
                            "isCorrect": True,
                            "explanation": "Bu sentez amfi notundaki üç majör vajinit tablosunun sınav spotlarını eksiksiz özetler."
                        },
                        {
                            "key": "B",
                            "text": "Trichomonas vaginalis bir bakteri olup hiçbir zaman hareket etmez",
                            "isCorrect": False,
                            "explanation": "Trichomonas kamçılı ve hareketli bir parazittir (protozoon)."
                        },
                        {
                            "key": "C",
                            "text": "Clue cells yalnızca menopoz sonrası erkeklerin böbreğinde görülür",
                            "isCorrect": False,
                            "explanation": "Bakteriyel vajinozda vajinal epitel hücresidir."
                        },
                        {
                            "key": "D",
                            "text": "Candida vajiniti dünyada cinsel yolla bulaşan en tehlikeli ölümcül virüstür",
                            "isCorrect": False,
                            "explanation": "Candida virüs değil mantardır ve cinsel yolla bulaşmaz."
                        }
                    ]
                }
            ]
        },
        # S98
        {
            "slideNumber": 98,
            "title": "Vajinal Maligniteler ve Sarkoma Botryoides Kilit Spotlar",
            "subtitle": "Vajinal SCC risk faktörleri (üst arka duvar) vs Sarkoma Botryoides (<5 yaş)",
            "clinicalFocus": "Sınav Sentezi ve Malign Vajinal Tümörler",
            "content": "Amfi ders notunun vajinal neoplaziler bölümünde vurgulanan iki temel tümörün sınav spotlarını bir arada konsolide ediyoruz.\n\n- **Vajinal Skuamöz Hücreli Karsinom:** Primer vajina kanseri kadın genital kanserlerinin %1'inden azını oluşturur. Neredeyse tamamı SCC'dir. **En büyük risk faktörü geçirilmiş serviks veya vulva karsinomu öyküsüdür**. Tümör en sık **üst vajinanın arka duvarında** yerleşir ve bölgesel **iliak lenf düğümlerine** metastaz yapar.\n- **Sarkoma Botryoides (Embriyonel Rabdomiyosarkom):** Vajinanın son derece nadir mezenkimal malignitesidir. Karakteristik olarak **5 yaşından küçük bebek ve çocuklarda** görülür; vajinadan dışarı sarkan şeffaf, polipoid, **üzüm salkımı benzeri kitleler** yapar. Histolojisinde malign rabdomiyoblastlar, epitel altında **kambiyum tabakası** ve Desmin/Miyogenin pozitifliği izlenir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Vajinal SCC için en büyük risk faktörü önceki serviks Ca öyküsüdür (üst arka duvar yerleşimi); Sarkoma Botryoides ise <5 yaş çocukta üzüm salkımı kitle ve kambiyum tabakası ile karakterizedir.",
            "synthesisNarrative": "Amfi ders notunun vajinal neoplaziler bölümünde vurgulanan iki temel tümörün sınav spotlarını bir arada konsolide ediyoruz.\n\n- **Vajinal Skuamöz Hücreli Karsinom:** Primer vajina kanseri kadın genital kanserlerinin %1'inden azını oluşturur. Neredeyse tamamı SCC'dir. **En büyük risk faktörü geçirilmiş serviks veya vulva karsinomu öyküsüdür**. Tümör en sık **üst vajinanın arka duvarında** yerleşir ve bölgesel **iliak lenf düğümlerine** metastaz yapar.\n- **Sarkoma Botryoides (Embriyonel Rabdomiyosarkom):** Vajinanın son derece nadir mezenkimal malignitesidir. Karakteristik olarak **5 yaşından küçük bebek ve çocuklarda** görülür; vajinadan dışarı sarkan şeffaf, polipoid, **üzüm salkımı benzeri kitleler** yapar. Histolojisinde malign rabdomiyoblastlar, epitel altında **kambiyum tabakası** ve Desmin/Miyogenin pozitifliği izlenir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Vajinal SCC için en büyük risk faktörü önceki serviks Ca öyküsüdür (üst arka duvar yerleşimi); Sarkoma Botryoides ise <5 yaş çocukta üzüm salkımı kitle ve kambiyum tabakası ile karakterizedir.",
            "bulletPoints": [
                "Vajinal SCC'nin en büyük risk faktörü önceki serviks/vulva kanseridir.",
                "Tümör en sık üst vajina arka duvarında yerleşir ve iliak nodlara yayılır.",
                "Sarkoma botryoides <5 yaş çocukta üzüm salkımı kitle ve kambiyum tabakası yapar."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Primer vajinal skuamöz hücreli karsinom en sık üst vajinanın arka duvarında yerleşim gösterir.",
                    "maskedTerm": "arka duvarında",
                    "hint": "Ektoserviks bileşkesine komşu anatomik lokalizasyon"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vajina Maligniteleri Sentezi",
                    "tableHeaders": ["Tümör", "Tipik Hasta Grubu", "En Önemli Klinik / Patolojik Özellik"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Vajinal Skuamöz Ca", "isMasked": False},
                                {"text": "İleri yaş kadınlar (>60 yaş)", "isMasked": False},
                                {"text": "Önceki serviks Ca öyküsü, üst arka duvar yerleşimi", "isMasked": True, "hint": "alan kanserleşmesi ve anatomik odak"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Sarkoma Botryoides", "isMasked": False},
                                {"text": "Bebekler ve 5 yaş altı çocuklar", "isMasked": True, "hint": "pediatrik yaş grubu"},
                                {"text": "Üzüm salkımı kitle, kambiyum tabakası, Desmin (+)"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Vajinal Malignite Diferansiasyonu",
                    "steps": [
                        "1. Yaş ve Semptom: Yaşlıda temas kanaması VEYA 2 yaşındaki bebekte vajinadan et sarkması izlenir.",
                        "2. Morfolojik Ayrım: Yaşlıda üst arka duvarda karsinom; bebekte lümende üzüm taneleri görülür.",
                        "3. Doku Karakteri: İlki keratinize epiteliyal SCC; ikincisi kambiyum tabakalı çizgili kas sarkomudur.",
                        "4. Yayılım Yolu: Karsinom iliak lenf bezlerine; sarkom ise pelvik lokal dokulara yayılır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Primer vajinal skuamöz karsinom için en büyük risk faktörü ve en sık yerleşim yeri nedir?",
                    "answer": "En büyük risk faktörü daha önce serviks veya vulva karsinomu öyküsü bulunmasıdır; en sık yerleşim yeri ise üst vajinanın arka duvarıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajinal Maligniteler",
                    "items": [
                        {"text": "Vajinal SCC için en büyük risk faktörü önceki serviks/vulva karsinomudur.", "isLie": False, "explanation": "Doğru. Amfi notunun net spotudur."},
                        {"text": "Vajinal karsinom en sık üst vajinanın arka duvarında yerleşir.", "isLie": False, "explanation": "Doğru. Anatomik odak noktasıdır."},
                        {"text": "Sarkoma botryoides 5 yaşından küçük çocukların malign tümörüdür.", "isLie": False, "explanation": "Doğru. Pediatrik rabdomiyosarkomdur."},
                        {"text": "Sarkoma botryoides sadece 90 yaşındaki erkeklerin sakallarında çıkan bir çıbandır.", "isLie": True, "explanation": "Tuzak! Sarkoma botryoides küçük kız çocuklarının vajinal mezenkimal sarkomudur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vajinanın malign neoplazmları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Vajinal SCC için en büyük risk faktörü önceki serviks karsinomu öyküsüdür; Sarkoma botryoides ise <5 yaş çocukta üzüm salkımı kitle yapar",
                            "isCorrect": True,
                            "explanation": "Bu sentez amfi notundaki vajinal malignite spotlarını eksiksiz özetler."
                        },
                        {
                            "key": "B",
                            "text": "Vajinal skuamöz karsinom en sık topuk kemiğine yapışık olarak gelişir",
                            "isCorrect": False,
                            "explanation": "Vajinada gelişen bir jinekolojik kanserdir."
                        },
                        {
                            "key": "C",
                            "text": "Sarkoma botryoides hiçbir zaman çocuklarda görülmeyen iyi huylu bir kemik kistidir",
                            "isCorrect": False,
                            "explanation": "Pediatrik malign çizgili kas sarkomudur."
                        },
                        {
                            "key": "D",
                            "text": "Vajina kanserlerinin %100'ü yalnızca güneş yanığı nedeniyle oluşur",
                            "isCorrect": False,
                            "explanation": "Güneş görmeyen iç genital organdır; HPV ve serviks kanseri öyküsü etkilidir."
                        }
                    ]
                }
            ]
        },
        # S99
        {
            "slideNumber": 99,
            "title": "Serviks Patolojisi ve Transformasyon Zonu Kilit Spotlar",
            "subtitle": "Karsinogenezin başladığı odak, Pap/HPV taraması ve üremiye bağlı ölüm",
            "clinicalFocus": "Sınav Sentezi ve Serviks Kanserleri",
            "content": "Kurul 1 ders notunun son kilit sentezinde serviks karsinogenezinin temel sınav spotlarını konsolide ediyoruz.\n\n- **Transformasyon Zonu:** Ektoserviksin çok katlı yassı epiteli ile endoserviksin tek katlı kolumnar bez epiteli arasındaki skuamokolumnar bileşkedir. Asidik vajina ortamında gelişen **skuamöz metaplazi** nedeniyle hücre döngüsü çok yüksektir; servikal karsinomların ve öncülü CIN lezyonlarının **neredeyse tamamı bu zonda başlar**.\n- **Tarama Programı:** Eksfoliyatif sitoloji (Papanicolaou testi) ve yüksek riskli HPV DNA testi ile taranır. Düzenli tarama mortaliteyi %70'ten fazla düşürmüştür.\n- **Mortalite Mekanizması:** İnvaziv karsinom komşu dokulara doğrudan yayılır; parametriyuma lateral yayılım **üreterleri tıkayarak bilateral hidronefroza ve üremiye (böbrek yetmezliği)** yol açar. İleri evre serviks kanserinde en sık ölüm nedeni üremidir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Servikal karsinomlar transformasyon zonunda başlar; Pap ve HPV testi ile taranır; ileri evrede parametrial yayılımla üreterleri tıkayarak en sık üremiden ölüme neden olur.",
            "synthesisNarrative": "Kurul 1 ders notunun son kilit sentezinde serviks karsinogenezinin temel sınav spotlarını konsolide ediyoruz.\n\n- **Transformasyon Zonu:** Ektoserviksin çok katlı yassı epiteli ile endoserviksin tek katlı kolumnar bez epiteli arasındaki skuamokolumnar bileşkedir. Asidik vajina ortamında gelişen **skuamöz metaplazi** nedeniyle hücre döngüsü çok yüksektir; servikal karsinomların ve öncülü CIN lezyonlarının **neredeyse tamamı bu zonda başlar**.\n- **Tarama Programı:** Eksfoliyatif sitoloji (Papanicolaou testi) ve yüksek riskli HPV DNA testi ile taranır. Düzenli tarama mortaliteyi %70'ten fazla düşürmüştür.\n- **Mortalite Mekanizması:** İnvaziv karsinom komşu dokulara doğrudan yayılır; parametriyuma lateral yayılım **üreterleri tıkayarak bilateral hidronefroza ve üremiye (böbrek yetmezliği)** yol açar. İleri evre serviks kanserinde en sık ölüm nedeni üremidir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Servikal karsinomlar transformasyon zonunda başlar; Pap ve HPV testi ile taranır; ileri evrede parametrial yayılımla üreterleri tıkayarak en sık üremiden ölüme neden olur.",
            "bulletPoints": [
                "Servikal karsinomların neredeyse tamamı transformasyon zonunda başlar.",
                "Düzenli Pap smear ve HPV DNA testi ile taranır.",
                "En sık ölüm nedeni parametrial yayılımla üreterlerin tıkanması ve üremidir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Servikal karsinomların ve displazilerin başladığı skuamokolumnar bileşke sahasına transformasyon zonu adı verilir.",
                    "maskedTerm": "transformasyon zonu",
                    "hint": "Metaplazinin gerçekleştiği karsinogenez başlangıç alanı"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Serviks Karsinomunun Kilit Patolojik Evreleri",
                    "tableHeaders": ["Evre / Süreç", "Yerleşim / Mekanizma", "Klinik Yansıması"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Başlangıç Odağı", "isMasked": False},
                                {"text": "Transformasyon Zonu (Metaplazi sahası)", "isMasked": True, "hint": "skuamokolumnar hat"},
                                {"text": "Pap smear ile sürüntü alınan kritik hedef alan"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Terminal Komplikasyon", "isMasked": False},
                                {"text": "Parametriyum yayılımı ve üreter basısı", "isMasked": True, "hint": "lateral doku infiltrasyonu"},
                                {"text": "Bilateral hidronefroz ve ölümcül üremi"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Transformasyon Zonundan Mortaliteye Karsinogenez",
                    "steps": [
                        "1. Metaplastik Enfeksiyon: HPV transformasyon zonundaki immatür metaplastik hücrelere girer.",
                        "2. CIN Spektrumu: Epitel kalınlığı boyunca CIN 1, 2 ve 3 displazisi gelişir.",
                        "3. İnvazyon: Hücreler bazal membranı yırtarak parametriyumu ve lenfatikleri tutar.",
                        "4. Üremi: İdrar kanalları tıkanarak böbrek yetmezliği sonucu hasta kaybedilir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Serviks karsinomlarının neredeyse tamamının başladığı anatomik bölge ve ileri evredeki en yaygın ölüm nedeni nedir?",
                    "answer": "Başladığı yer transformasyon zonudur (skuamokolumnar bileşke); en sık ölüm nedeni ise parametrial yayılımla üreterlerin tıkanmasına bağlı gelişen üremidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Serviks Patolojisi Kilit Spotlar",
                    "items": [
                        {"text": "Servikal neoplaziler transformasyon zonundan köken alır.", "isLie": False, "explanation": "Doğru. Metaplastik karsinogenez odağıdır."},
                        {"text": "Pap smear ve HPV testi ile düzenli tarama yapılır.", "isLie": False, "explanation": "Doğru. En başarılı tarama programıdır."},
                        {"text": "İleri evrede üreter basısı sonucu üremi en sık ölüm nedenidir.", "isLie": False, "explanation": "Doğru. Klasik ölüm mekanizmasıdır."},
                        {"text": "Serviks kanseri daima hastanın sol el parmaklarında kaşıntı ile başlar.", "isLie": True, "explanation": "Tuzak! Serviks kanseri uterus serviksinde başlar ve postkoital kanamayla belirir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servikal karsinomun patogenezi, taraması ve klinik seyri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Neredeyse tamamı transformasyon zonunda başlar, Pap/HPV testiyle taranır ve en sık ölüm nedeni parametrial yayılımla üreter tıkanmasına bağlı üremidir",
                            "isCorrect": True,
                            "explanation": "Bu sentez amfi notundaki serviks karsinogenezi, tarama ve mortalite spotlarını eksiksiz özetler."
                        },
                        {
                            "key": "B",
                            "text": "Serviks kanseri yalnızca safra kesesinden kaynaklanan selim bir taştır",
                            "isCorrect": False,
                            "explanation": "Malign epiteliyal jinekolojik kanserdir."
                        },
                        {
                            "key": "C",
                            "text": "Üreterler serviks kanseri tarafından hiçbir zaman sıkıştırılamaz",
                            "isCorrect": False,
                            "explanation": "Parametrial yayılım üreterleri sıkıştırarak üremiye yol açar."
                        },
                        {
                            "key": "D",
                            "text": "Transformasyon zonunun karsinogenez ile uzaktan yakından hiçbir ilgisi yoktur",
                            "isCorrect": False,
                            "explanation": "Serviks kanserlerinin neredeyse tamamı transformasyon zonunda başlar."
                        }
                    ]
                }
            ]
        },
        # S100
        {
            "slideNumber": 100,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 10] Vulva, Vajen ve Serviks Hastalıkları: Final Entegrasyon ve Sınav Sentezi",
            "subtitle": "Tüm amfi notu ve Robbins referanslarının 100 slaytlık tam klinik patolojik konsolidasyonu",
            "clinicalFocus": "Kapsamlı Müfredat Konsolidasyonu",
            "content": "Bu 100 slaytlık kapsamlı öğrenme modülünde Kurul 1 Dönem 3 Patoloji müfredatının tüm vulva, vajen ve serviks hastalıklarını eksiksiz olarak sentezledik.\n\n- **Vulva:** Bartholin kisti/apsesi, liken skleroz (ince epidermis + homojen dermal fibrozis), skuamöz hiperplazi (akantoz), lökoplaki biyopsi zorunluluğu, kondiloma akuminatum (HPV 6/11) vs lata (sifiliz), vulvar karsinom ikili yolu (HPV-16 bazaloid vs liken/dVIN keratinize), Ekstramammary Paget (dermatit taklidi, altta tümör genelde yok) ve melanom (S100+).\n- **Vajina:** Gartner kisti (Wolffian kalıntısı, lateral duvar), vajinitler (Candida cinsel yolla bulaşmaz; Trichomonas en sık non-viral CYBH; Gardnerella clue cells), vajinal SCC (önceki serviks Ca riski, üst arka duvar), sarkoma botryoides (<5 yaş, üzüm salkımı, kambiyum tabakası, Desmin+) ve DES berrak hücreli karsinomu.\n- **Serviks:** Transformasyon zonu karsinogenezi, HPV E6 (p53) ve E7 (Rb), Pap smear ve Bethesda (LSIL=CIN 1, HSIL=CIN 2/3), kolposkopi (asetobeyazlık) ve Schiller testi (glikojensiz hardal sarısı), AIS (HPV-18) ve ileri evrede en sık ölüm nedeni olan üremi.\n\n> [!IMPORTANT]\n> [FİNAL KONSOLİDASYON] Tıp Fakültesi Patoloji Kurul ve TUS sınavlarında bu dersten gelen tüm sorular; ayırıcı tanı kriterleri, histopatolojik belirteçler ve moleküler mekanizmalar temelinde bu 100 slaytlık akış ile eksiksiz yanıtlanabilir.",
            "synthesisNarrative": "Bu 100 slaytlık kapsamlı öğrenme modülünde Kurul 1 Dönem 3 Patoloji müfredatının tüm vulva, vajen ve serviks hastalıklarını eksiksiz olarak sentezledik.\n\n- **Vulva:** Bartholin kisti/apsesi, liken skleroz (ince epidermis + homojen dermal fibrozis), skuamöz hiperplazi (akantoz), lökoplaki biyopsi zorunluluğu, kondiloma akuminatum (HPV 6/11) vs lata (sifiliz), vulvar karsinom ikili yolu (HPV-16 bazaloid vs liken/dVIN keratinize), Ekstramammary Paget (dermatit taklidi, altta tümör genelde yok) ve melanom (S100+).\n- **Vajina:** Gartner kisti (Wolffian kalıntısı, lateral duvar), vajinitler (Candida cinsel yolla bulaşmaz; Trichomonas en sık non-viral CYBH; Gardnerella clue cells), vajinal SCC (önceki serviks Ca riski, üst arka duvar), sarkoma botryoides (<5 yaş, üzüm salkımı, kambiyum tabakası, Desmin+) ve DES berrak hücreli karsinomu.\n- **Serviks:** Transformasyon zonu karsinogenezi, HPV E6 (p53) ve E7 (Rb), Pap smear ve Bethesda (LSIL=CIN 1, HSIL=CIN 2/3), kolposkopi (asetobeyazlık) ve Schiller testi (glikojensiz hardal sarısı), AIS (HPV-18) ve ileri evrede en sık ölüm nedeni olan üremi.\n\n> [!IMPORTANT]\n> [FİNAL KONSOLİDASYON] Tıp Fakültesi Patoloji Kurul ve TUS sınavlarında bu dersten gelen tüm sorular; ayırıcı tanı kriterleri, histopatolojik belirteçler ve moleküler mekanizmalar temelinde bu 100 slaytlık akış ile eksiksiz yanıtlanabilir.",
            "bulletPoints": [
                "Vulva, vajina ve serviksin tüm neoplastik ve non-neoplastik süreçleri entegre edildi.",
                "HPV ile ilişkili ve ilişkisiz ikili yollar, aşı teknolojileri ve ayırıcı tanılar pekiştirildi.",
                "100 slayt boyunca katı kronoloji ve sıfır sızıntı ile tam sınav hazırliği sağlandı."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "İleri evre servikal karsinomda parametrial yayılımla üreterlerin tıkanması sonucu gelişen en yaygın ölüm nedeni üremi tablosudur.",
                    "maskedTerm": "üremi",
                    "hint": "Bilateral hidronefroza sekonder gelişen böbrek yetmezliği tablosu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulva, Vajen ve Serviks Hastalıkları Büyük Final Sentezi",
                    "tableHeaders": ["Organ / Bölge", "En Kritik Malignite / Öncü Lezyon", "Patognomonik / Anahtar Tanı Bulgusu"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Vulva", "isMasked": False},
                                {"text": "Keratinize SCC (HPV-) / Bazaloid SCC (HPV+)", "isMasked": True, "hint": "ikili patogenetik model"},
                                {"text": "dVIN (p53 mutasyonu) / Klasik VIN (koilosit)"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Vajina", "isMasked": False},
                                {"text": "Sarkoma Botryoides / Primer Vajinal SCC", "isMasked": True, "hint": "pediatrik sarkom ve erişkin karsinomu"},
                                {"text": "Kambiyum tabakası ve Desmin(+) / Önceki serviks Ca"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Serviks", "isMasked": False},
                                {"text": "Servikal Skuamöz Karsinom ve AIS", "isMasked": False},
                                {"text": "Transformasyon zonu, HPV E6/E7, ölümcül üremi", "isMasked": True, "hint": "karsinogenez başlangıcı ve terminal komplikasyon"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "100 Slaytlık Büyük Müfredat Entegrasyon Zinciri",
                    "steps": [
                        "1. Vulva: Bartholin apsesi, liken skleroz fibrozisi, ikili karsinogenez ve Paget hastalığı.",
                        "2. Vajina: Gartner kisti, Candida/Trichomonas/Gardnerella vajinitleri ve sarkoma botryoides.",
                        "3. Serviks: Skuamöz metaplazi, HPV E6/E7 onkogenezi, CIN 1-3 ve adenokarsinoma in situ.",
                        "4. Tanı ve Klinik: Pap smear, asetobeyaz epitel, Schiller hardal sarılığı ve üremi mortalitesi."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Ders 48 boyunca işlenen konulardan hareketle; vulvada dVIN'in ilişkili olduğu gen mutasyonu, vajinada <5 yaş çocukta saptanan sarkomun adı ve serviks kanserinde en sık ölüm nedeni nedir?",
                    "answer": "dVIN p53 gen mutasyonu içerir; vajinadaki pediatrik tümör Sarkoma Botryoides'tir (embriyonel rabdomiyosarkom); serviks kanserinde en sık ölüm nedeni ise üreter tıkanmasına bağlı üremidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Final Entegrasyon ve Sınav Sentezi",
                    "items": [
                        {"text": "Vulvar karsinogenezde HPV pozitif ve HPV negatif iki ana yolak bulunur.", "isLie": False, "explanation": "Doğru. Amfi notunun temel modelidir."},
                        {"text": "Candida türleri vajinit yapar fakat cinsel yolla bulaşmaz.", "isLie": False, "explanation": "Doğru. Çıkmış sınav sorusudur."},
                        {"text": "Sarkoma botryoides <5 yaş çocuklarda kambiyum tabakası ile karakterizedir.", "isLie": False, "explanation": "Doğru. Patognomonik sarkom bulgusudur."},
                        {"text": "Serviks kanseri daima hiçbir tedaviye gerek kalmadan 24 saatte kendiliğinden buharlaşır.", "isLie": True, "explanation": "Tuzak! İnvaziv serviks kanseri agresif, tedavi edilmezse üremiyle ölüme yol açan ciddi bir malignitedir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulva, Vajen ve Serviks Hastalıkları modülünün tüm kilit spotları dikkate alındığında aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Liken skleroz ince epidermis/homojen fibrozisle seyreder; Candida cinsel yolla bulaşmaz; sarkoma botryoides <5 yaşta kambiyum tabakası yapar; serviks Ca en sık üremiden ölüme neden olur",
                            "isCorrect": True,
                            "explanation": "Bu sentez cümlesi dersin tüm organlarındaki en yüksek verimli sınav spotlarını kusursuz biçimde bir araya getirir."
                        },
                        {
                            "key": "B",
                            "text": "Tüm bu hastalıklar yalnızca akciğer alveollerinde hava değişimi yapan selim durumlardır",
                            "isCorrect": False,
                            "explanation": "Kadın genital sistem hastalıklarıdır."
                        },
                        {
                            "key": "C",
                            "text": "Bartholin bezi ve Gartner kisti yalnızca erkeklerin göz çukurunda bulunur",
                            "isCorrect": False,
                            "explanation": "Kadın genital organlarına aittir."
                        },
                        {
                            "key": "D",
                            "text": "HPV virüsü ile alt genital kanserler arasında hiçbir bağlantı yoktur",
                            "isCorrect": False,
                            "explanation": "Yüksek riskli HPV temel onkojenik etkendir."
                        }
                    ]
                }
            ]
        }
    ]
    return slides

if __name__ == '__main__':
    slides = get_s10_slides()
    print(f'Section 10 generated with {len(slides)} slides.')
