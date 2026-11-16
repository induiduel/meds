import json

def get_s3_slides():
    slides = [
        # S21
        {
            "slideNumber": 21,
            "title": "Ekstramammary Paget Hastalığı: Tanım ve Klinik Görünüm",
            "subtitle": "Vulva derisinde intraepidermal glandüler neoplazi ve dermatit benzeri lezyon",
            "clinicalFocus": "Tanım ve Klinik",
            "content": "Ekstramammary Paget hastalığı, apokrin ter bezleri yönünde diferansiasyon gösteren atipik müsinöz glandüler epitel hücrelerinin vulva epidermisi içinde çoğalarak yayılmasıyla karakterize nadir bir tablodur.\n\n- **Klinik Görünüm:** En sık postmenopozal kadınlarda labia majorada iyi sınırlı, eritemli, pullu, kabuklu, bazen masere ve kaşıntılı kırmızı plaklar şeklinde izlenir.\n- **Klinik Tuzak:** Görünümü kronik kontakt dermatiti, egzamayı veya fungal enfeksiyonları o kadar kusursuz taklit eder ki, hastalar sıklıkla yıllarca topikal kortikosteroid veya antifungal tedavilerle oyalanır.\n- **Tanısal İlke:** İnatçı, standart medikal tedaviye direnç gösteren vulvar eritematöz plaklarda gecikmeksizin biyopsi yapılmalıdır.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Vulvada tedaviye dirençli egzema benzeri kaşıntılı kırmızı-kabuklu plaklar görüldüğünde mutlaka Ekstramammary Paget hastalığı düşünülmeli ve biyopsi alınmalıdır.",
            "synthesisNarrative": "Ekstramammary Paget hastalığı, apokrin ter bezleri yönünde diferansiasyon gösteren atipik müsinöz glandüler epitel hücrelerinin vulva epidermisi içinde çoğalarak yayılmasıyla karakterize nadir bir tablodur.\n\n- **Klinik Görünüm:** En sık postmenopozal kadınlarda labia majorada iyi sınırlı, eritemli, pullu, kabuklu, bazen masere ve kaşıntılı kırmızı plaklar şeklinde izlenir.\n- **Klinik Tuzak:** Görünümü kronik kontakt dermatiti, egzamayı veya fungal enfeksiyonları o kadar kusursuz taklit eder ki, hastalar sıklıkla yıllarca topikal kortikosteroid veya antifungal tedavilerle oyalanır.\n- **Tanısal İlke:** İnatçı, standart medikal tedaviye direnç gösteren vulvar eritematöz plaklarda gecikmeksizin biyopsi yapılmalıdır.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Vulvada tedaviye dirençli egzema benzeri kaşıntılı kırmızı-kabuklu plaklar görüldüğünde mutlaka Ekstramammary Paget hastalığı düşünülmeli ve biyopsi alınmalıdır.",
            "bulletPoints": [
                "Atipik glandüler hücrelerin intraepidermal proliferasyonudur.",
                "Eritemli, pullu, kabuklu kırmızı plaklar yapar.",
                "Kronik dermatiti mükemmel taklit ederek tanı gecikmesine yol açar."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Ekstramammary Paget hastalığının klinik görünümü sıklıkla kronik dermatiti taklit eder.",
                    "maskedTerm": "kronik dermatiti",
                    "hint": "Egzematöz kaşıntılı inflamatuvar cilt hastalığı"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Ekstramammary Paget ve Kronik Dermatit Ayrımı",
                    "tableHeaders": ["Özellik", "Kronik Dermatit / Egzema", "Ekstramammary Paget"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Tedaviye Yanıt", "isMasked": False},
                                {"text": "Topikal kortikosteroide hızlı yanıt", "isMasked": False},
                                {"text": "Topikal tedaviye dirençli ve inatçı", "isMasked": True, "hint": "tedaviyle gerilemeyen süreç"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Histopatolojik Köken", "isMasked": False},
                                {"text": "Reaktif lenfositik inflamasyon", "isMasked": True, "hint": "selim yangısal zemin"},
                                {"text": "İntraepidermal atipik glandüler neoplazi", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Klinik Taklitten Doğru Tanıya",
                    "steps": [
                        "1. Lezyon Başlangıcı: Vulvada kaşıntılı, eritemli ve kabuklu kırmızı bir plak belirir.",
                        "2. Yanıltıcı Tedavi: Hasta egzema sanılarak aylarca topikal kortikosteroid merhemler kullanır.",
                        "3. Direnç: Lezyon gerilemez, sınırları yavaşça genişler ve kabuklanma devam eder.",
                        "4. Biyopsi: Şüphe üzerine alınan punch biyopside intraepidermal Paget hücreleri saptanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Ekstramammary Paget hastalığının tanısında sıklıkla aylarca hatta yıllarca gecikmeye yol açan klinik özellik nedir?",
                    "answer": "Kırmızı, pullu ve kabuklu plak görünümünün kronik kontakt dermatiti veya egzamayı çok andırması ve topikal tedavilerle zaman kaybedilmesidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Ekstramammary Paget Hastalığı Kliniği",
                    "items": [
                        {"text": "Ekstramammary Paget hastalığı vulva derisinde kırmızı, pullu ve kabuklu plaklar yapar.", "isLie": False, "explanation": "Doğru. Klasik klinik prezentasyon eritematöz skuamlı plaktır."},
                        {"text": "Lezyonlar sıklıkla kronik kontakt dermatiti veya egzamayı andırır.", "isLie": False, "explanation": "Doğru. Klinik taklit tanı gecikmelerinin en büyük sebebidir."},
                        {"text": "İnatçı ve tedaviye yanıtsız lezyonlarda biyopsi ile inceleme şarttır.", "isLie": False, "explanation": "Doğru. Mikroskopi kesin tanı koydurur."},
                        {"text": "Ekstramammary Paget daima doğum sırasında bebeklerde gelişen selim bir hematomdur.", "isLie": True, "explanation": "Tuzak! Ekstramammary Paget ileri yaştaki kadınlarda görülen intraepitelyal neoplastik bir hastalıktır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvanın Ekstramammary Paget hastalığı ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Klinik olarak kırmızı, pullu, kabuklu plaklar şeklinde olup sıklıkla kronik dermatiti taklit eder",
                            "isCorrect": True,
                            "explanation": "Bu klinik profil Ekstramammary Paget hastalığının amfi notlarındaki temel tanımıdır."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca çocukluk çağında izlenen ve hiçbir zaman kaşıntı yapmayan bir hemanjiyomdur",
                            "isCorrect": False,
                            "explanation": "Genellikle postmenopozal dönemde görülür ve kaşıntılıdır."
                        },
                        {
                            "key": "C",
                            "text": "Tek bir doz oral antibiyotik kullanımı ile 24 saat içinde tamamen kaybolur",
                            "isCorrect": False,
                            "explanation": "Neoplastik bir süreçtir, antibiyotiklerle gerilemez."
                        },
                        {
                            "key": "D",
                            "text": "Daima kemik iliğinden kaynaklanan malign bir lenfoma türüdür",
                            "isCorrect": False,
                            "explanation": "Ekstramammary Paget kutanöz/mukoza epitel içi glandüler bir neoplazidir."
                        }
                    ]
                }
            ]
        },
        # S22
        {
            "slideNumber": 22,
            "title": "Ekstramammary Paget Hastalığı vs Meme Paget Hastalığı Ayrımı",
            "subtitle": "Altta yatan duktal karsinom ilişkisi ve hücre kökeni farkları",
            "clinicalFocus": "Meme ve Vulva Paget Karşılaştırması",
            "content": "Paget hastalığı genel olarak skuamöz epitel katmanları arasına atipik glandüler hücrelerin infiltre olmasıdır. Ancak memenin Paget hastalığı ile vulvanın Ekstramammary Paget hastalığı arasında yaşamsal bir biyolojik fark bulunur:\n\n- **Memenin Paget Hastalığı:** Meme başı epidermisinde görülür ve vakaların ==NEREDEYSE %100'ÜNDE ALTA YATAN DUKTAL MEME KARSİNOMU== (in situ veya invaziv) mevcuttur. Atipik hücreler meme duktuslarından meme başına doğru göç etmiştir.\n- **Vulva Ekstramammary Paget Hastalığı:** Olguların büyük bir kısmında altta yatan bir iç organ veya glandüler malignite **YOKTUR**. Lezyon primer olarak vulva derisindeki duktusların multipotent kök hücrelerinden köken alan intraepidermal bir süreçtir.\n- **Altta Yatan Kanser Oranı:** Vulva Paget olgularının yalnızca yaklaşık %1-4'ünde altta yatan ek bir ter bezi veya komşu organ karsinomu eşlik eder.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Meme Paget hastalığı daima altta yatan duktal meme karsinomu ile ilişkilidir; oysa vulva Ekstramammary Paget hastalığı çoğunlukla altta yatan tümör olmaksızın primer intraepidermal bir neoplazidir.",
            "synthesisNarrative": "Paget hastalığı genel olarak skuamöz epitel katmanları arasına atipik glandüler hücrelerin infiltre olmasıdır. Ancak memenin Paget hastalığı ile vulvanın Ekstramammary Paget hastalığı arasında yaşamsal bir biyolojik fark bulunur:\n\n- **Memenin Paget Hastalığı:** Meme başı epidermisinde görülür ve vakaların ==NEREDEYSE %100'ÜNDE ALTA YATAN DUKTAL MEME KARSİNOMU== (in situ veya invaziv) mevcuttur. Atipik hücreler meme duktuslarından meme başına doğru göç etmiştir.\n- **Vulva Ekstramammary Paget Hastalığı:** Olguların büyük bir kısmında altta yatan bir iç organ veya glandüler malignite **YOKTUR**. Lezyon primer olarak vulva derisindeki duktusların multipotent kök hücrelerinden köken alan intraepidermal bir süreçtir.\n- **Altta Yatan Kanser Oranı:** Vulva Paget olgularının yalnızca yaklaşık %1-4'ünde altta yatan ek bir ter bezi veya komşu organ karsinomu eşlik eder.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Meme Paget hastalığı daima altta yatan duktal meme karsinomu ile ilişkilidir; oysa vulva Ekstramammary Paget hastalığı çoğunlukla altta yatan tümör olmaksızın primer intraepidermal bir neoplazidir.",
            "bulletPoints": [
                "Meme Paget'inde daima altta yatan duktal karsinom bulunur.",
                "Vulva Paget'inde çoğunlukla altta yatan karsinom yoktur.",
                "Vulva Paget'i primer multipotent kök hücrelerden doğar."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Meme ucu Paget hastalığı hemen her zaman altta yatan duktal meme karsinomu ile ilişkilidir.",
                    "maskedTerm": "duktal meme karsinomu",
                    "hint": "Meme parankiminde yer alan malign epitel tümörü"
                },
                {
                    "type": "before_after_slider",
                    "leftTitle": "Meme Paget Hastalığı",
                    "rightTitle": "Vulva Ekstramammary Paget",
                    "leftPoints": [
                        "Meme başı ve areola cildine yerleşir.",
                        "Hemen daima (%100'e yakın) altta invaziv/in situ duktal karsinom vardır.",
                        "Duktuslardan epidermise doğru yukarı göç söz konusudur.",
                        "Tedavi meme karsinomunun onkolojik tedavisine odaklanır."
                    ],
                    "rightPoints": [
                        "Vulvanın labia majora derisine yerleşir.",
                        "Olguların büyük çoğunluğunda altta yatan tümör bulunmaz.",
                        "Epidermis içi multipotent kök hücrelerden primer olarak gelişir.",
                        "Tedavide geniş cerrahi lokal eksizyon uygulanır."
                    ]
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Meme ve Vulva Paget Hastalığı Karşılaştırması",
                    "tableHeaders": ["Özellik", "Meme Paget Hastalığı", "Vulva Ekstramammary Paget"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Altta Yatan Karsinom", "isMasked": False},
                                {"text": "Her zaman vardır (duktal karsinom)", "isMasked": True, "hint": "zorunlu altta yatan malignite"},
                                {"text": "Çoğunlukla yoktur (%1-4 nadir)", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Hücresel Köken", "isMasked": False},
                                {"text": "Meme duktus epitel hücreleri", "isMasked": False},
                                {"text": "Kutanöz multipotent ter bezi öncüleri", "isMasked": True, "hint": "lokal deri eki kökeni"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "İki Paget Tipinin Biyolojik Ayrımı",
                    "steps": [
                        "1. Meme Patolojisi: Derindeki duktus karsinoma in situ hücreleri meme başına tırmanır.",
                        "2. Vulva Patolojisi: Vulva derisindeki multipotent öncül hücreler yerinde atipikleşir.",
                        "3. İntraepidermal Yayılım: Her iki formda da atipik Paget hücreleri skuamöz hücreler arasına dağılır.",
                        "4. Prognostik Fark: Memede prognozu alttaki duktal karsinom belirlerken, vulvada lokal yinelemeler ön plandadır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Meme Paget hastalığı ile vulva Ekstramammary Paget hastalığı arasındaki en kritik onkolojik fark nedir?",
                    "answer": "Meme Paget hastalığında neredeyse daima altta yatan bir duktal meme karsinomu bulunurken; vulva Ekstramammary Paget hastalığında vakaların çoğunda altta yatan bir karsinom yoktur, primer intraepidermal gelişir."
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvanın Ekstramammary Paget hastalığı ile memenin Paget hastalığı karşılaştırıldığında aşağıdakilerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Meme Paget'inde altta yatan duktal karsinom neredeyse daima bulunurken vulva Paget'inde çoğunlukla altta yatan tümör yoktur",
                            "isCorrect": True,
                            "explanation": "Bu fark iki hastalığın ayrımındaki en temel Robbins ve kurul sınav spotudur."
                        },
                        {
                            "key": "B",
                            "text": "Her iki hastalıkta da istisnasız %100 oranında metastatik osteosarkom saptanır",
                            "isCorrect": False,
                            "explanation": "Kemik sarkomu ile hiçbir ilgileri yoktur."
                        },
                        {
                            "key": "C",
                            "text": "Vulva Paget hastalığı daima akciğer karsinomunun doğrudan metastazı ile oluşur",
                            "isCorrect": False,
                            "explanation": "Vulva Paget'i primer kutanöz intraepidermal bir süreçtir."
                        },
                        {
                            "key": "D",
                            "text": "Meme Paget hastalığında hiçbir zaman altta yatan bir tümör görülmez",
                            "isCorrect": False,
                            "explanation": "Meme Paget'inde hemen daima altta yatan duktal karsinom vardır."
                        }
                    ]
                }
            ]
        },
        # S23
        {
            "slideNumber": 23,
            "title": "Ekstramammary Paget Histopatolojisi: Paget Hücreleri ve Boyanma",
            "subtitle": "Büyük soluk vakuollü hücreler, müsin pozitifliği ve ayırıcı tanı",
            "clinicalFocus": "Histopatoloji ve Özel Boyalar",
            "content": "Ekstramammary Paget hastalığının histopatolojisi, çok katlı yassı epitel katmanları arasına saçılmış büyük ve atipik hücrelerin tanınmasıyla karakterizedir.\n\n- **Paget Hücresi Morfolojisi:** Normal keratinositlerden belirgin biçimde daha büyük, bol miktarda soluk, ince granüllü veya vakuollü sitoplazmaya sahip hücrelerdir. Geniş ve pleomorfik nükleusları, belirgin nükleolleri bulunur.\n- **İntraepidermal Dağılım:** Hücreler bazal tabakada ve epitelin üst katmanlarında tek tek veya yuvalar (kümeler) halinde yerleşir.\n- **Müsin Boyaları:** Glandüler kökeni kanıtlamak amacıyla müsin boyaları kullanılır. Paget hücreleri **Müsikarmin (Mucicarmine)** ve **PAS (Alcian blue)** ile intraselüler müsin pozitifliği gösterir.\n- **İmmünohistokimya:** Skuamöz hücre karsinomundan ve malign melanomdan ayırt etmek için sitokeratin 7 (CK7 pozitif), CEA (pozitif) ve S100/HMB-45 (negatif) panelleri uygulanır.\n\n> [!NOTE]\n> Vulva Paget hücreleri müsin pozitifken; morfolojik olarak karışabildiği malign melanom hücreleri müsin negatiftir ve S100/Melan-A pozitiftir.",
            "synthesisNarrative": "Ekstramammary Paget hastalığının histopatolojisi, çok katlı yassı epitel katmanları arasına saçılmış büyük ve atipik hücrelerin tanınmasıyla karakterizedir.\n\n- **Paget Hücresi Morfolojisi:** Normal keratinositlerden belirgin biçimde daha büyük, bol miktarda soluk, ince granüllü veya vakuollü sitoplazmaya sahip hücrelerdir. Geniş ve pleomorfik nükleusları, belirgin nükleolleri bulunur.\n- **İntraepidermal Dağılım:** Hücreler bazal tabakada ve epitelin üst katmanlarında tek tek veya yuvalar (kümeler) halinde yerleşir.\n- **Müsin Boyaları:** Glandüler kökeni kanıtlamak amacıyla müsin boyaları kullanılır. Paget hücreleri **Müsikarmin (Mucicarmine)** ve **PAS (Alcian blue)** ile intraselüler müsin pozitifliği gösterir.\n- **İmmünohistokimya:** Skuamöz hücre karsinomundan ve malign melanomdan ayırt etmek için sitokeratin 7 (CK7 pozitif), CEA (pozitif) ve S100/HMB-45 (negatif) panelleri uygulanır.\n\n> [!NOTE]\n> Vulva Paget hücreleri müsin pozitifken; morfolojik olarak karışabildiği malign melanom hücreleri müsin negatiftir ve S100/Melan-A pozitiftir.",
            "bulletPoints": [
                "Büyük, bol soluk vakuollü sitoplazmalı hücreler izlenir.",
                "Hücreler tek tek veya kümeler halinde epidermiste yayılır.",
                "Müsikarmin ve PAS ile intraselüler müsin pozitif boyanır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Ekstramammary Paget hücreleri mikroskop altında bol soluk ince granüllü sitoplazma ve sitoplazmik vakuoller içerir.",
                    "maskedTerm": "soluk ince granüllü",
                    "hint": "Paget hücre sitoplazmasının tipik açık renkli görünümü"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Paget Hücresi ve Malign Melanom Histokimyasal Ayrımı",
                    "tableHeaders": ["Belirteç / Boya", "Ekstramammary Paget", "Malign Melanom"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Müsikarmin / PAS", "isMasked": False},
                                {"text": "Pozitif (müsin içerir)", "isMasked": True, "hint": "glandüler sekresyon boyanması"},
                                {"text": "Negatif (müsin içermez)", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Sitokeratin 7 (CK7)", "isMasked": False},
                                {"text": "Pozitif", "isMasked": False},
                                {"text": "Negatif", "isMasked": True, "hint": "epitelyal olmayan melanositik lezyon"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Biyopside Paget Tanı Zinciri",
                    "steps": [
                        "1. HE Kesit: Çok katlı yassı epitelde dağınık soluk sitoplazmalı atipik hücreler saptanır.",
                        "2. Müsin Boyası: Müsikarmin boyaması ile sitoplazmada pembe-kırmızı müsin damlacıkları gösterilir.",
                        "3. İmmün Boyama: CK7 pozitif ve S100 negatif bulunarak melanom dışlanır.",
                        "4. Tanı: Ekstramammary Paget hastalığı kesinleşir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Ekstramammary Paget hücrelerinin mikroskop altında sitoplazmik özellikleri nelerdir ve glandüler kökeni hangi boyalarla doğrulanır?",
                    "answer": "Bol, soluk, ince granüllü veya vakuollü sitoplazmaya sahiptirler; glandüler müsin içeriği Müsikarmin ve PAS boyaları ile pozitif olarak doğrulanır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Paget Hücrelerinin Histopatolojisi",
                    "items": [
                        {"text": "Paget hücreleri bol soluk sitoplazmalı ve pleomorfik nükleuslu büyük hücrelerdir.", "isLie": False, "explanation": "Doğru. Keratinositlerden çok daha iridirler."},
                        {"text": "Müsikarmin boyasıyla intraselüler müsin birikimi gösterilebilir.", "isLie": False, "explanation": "Doğru. Glandüler diferansiasyonu kanıtlar."},
                        {"text": "Hücreler epidermiste tek tek veya yuvalar halinde yayılır.", "isLie": False, "explanation": "Doğru. Pagetoid yayılım paterni budur."},
                        {"text": "Paget hücreleri kesinlikle çekirdeksiz saf keratin pullarından oluşur.", "isLie": True, "explanation": "Tuzak! Paget hücreleri iri nükleuslu atipik glandüler epitel hücreleridir; keratin pulu değildir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Ekstramammary Paget hastalığının histopatolojik tanısında kullanılan özel boyalar ve bulgularla ilgili hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Bol soluk sitoplazmalı Paget hücreleri Müsikarmin ve PAS boyaları ile müsin pozitifliği gösterir",
                            "isCorrect": True,
                            "explanation": "Paget hücreleri apokrin/glandüler kökenden geldiği için müsin boyalarıyla pozitif boyanır."
                        },
                        {
                            "key": "B",
                            "text": "Tümör hücrelerinde hiçbir zaman sitoplazma ve çekirdek izlenmez",
                            "isCorrect": False,
                            "explanation": "Hücreler belirgin çekirdeğe ve bol sitoplazmaya sahiptir."
                        },
                        {
                            "key": "C",
                            "text": "Yalnızca asidofilik kas fibrillerinden oluşan benign bir miyomdur",
                            "isCorrect": False,
                            "explanation": "Paget bir miyom değil, intraepidermal epitelyal glandüler bir süreçtir."
                        },
                        {
                            "key": "D",
                            "text": "Müsin boyaları her zaman negatiftir çünkü lezyon kıkırdak kökenlidir",
                            "isCorrect": False,
                            "explanation": "Glandüler diferansiasyon nedeniyle müsin pozitiftir."
                        }
                    ]
                }
            ]
        },
        # S24
        {
            "slideNumber": 24,
            "title": "Ekstramammary Paget: Klinik Seyir, İnvazyon ve Cerrahi Yönetim",
            "subtitle": "Yıllarca süren intraepidermal faz, nüks riski ve dermal invazyon prognozu",
            "clinicalFocus": "Tedavi ve Seyir",
            "content": "Ekstramammary Paget hastalığı, biyolojik olarak yavaş seyirli fakat cerrahi olarak sınır tayini oldukça güç bir neoplazmdır.\n\n- **İntraepidermal Faz:** Olguların büyük bir kısmında tümör hücreleri bazal membranı aşmadan, epidermiste yatay olarak yayılarak invazyon veya metastaz yapmaksızın yıllarca sürebilir.\n- **Tedavi:** Temel tedavi seçeneği **geniş lokal eksizyondur**. Ancak tümör hücreleri mikroskop altında klinik lezyon sınırlarının çok ötesine mikroskobik olarak yayılabildiğinden, cerrahi sınırlarda pozitiflik ve **lokal nüks oranı oldukça yüksektir**.\n- **Dermal İnvazyon ve Prognoz:** Vakaların az bir kısmında atipik Paget hücreleri bazal membranı delerek dermis ve derin dokulara invaze olur. Dermal invazyon geliştiğinde lenfatik yayılım riski katlanarak artar ve ==PROGNOZ ÇOK KÖTÜLEŞİR==.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Ekstramammary Paget intraepidermal kaldığı sürece prognoz iyidir; ancak dermal invazyon geliştiğinde prognoz dramatik biçimde kötüleşir.",
            "synthesisNarrative": "Ekstramammary Paget hastalığı, biyolojik olarak yavaş seyirli fakat cerrahi olarak sınır tayini oldukça güç bir neoplazmdır.\n\n- **İntraepidermal Faz:** Olguların büyük bir kısmında tümör hücreleri bazal membranı aşmadan, epidermiste yatay olarak yayılarak invazyon veya metastaz yapmaksızın yıllarca sürebilir.\n- **Tedavi:** Temel tedavi seçeneği **geniş lokal eksizyondur**. Ancak tümör hücreleri mikroskop altında klinik lezyon sınırlarının çok ötesine mikroskobik olarak yayılabildiğinden, cerrahi sınırlarda pozitiflik ve **lokal nüks oranı oldukça yüksektir**.\n- **Dermal İnvazyon ve Prognoz:** Vakaların az bir kısmında atipik Paget hücreleri bazal membranı delerek dermis ve derin dokulara invaze olur. Dermal invazyon geliştiğinde lenfatik yayılım riski katlanarak artar ve ==PROGNOZ ÇOK KÖTÜLEŞİR==.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Ekstramammary Paget intraepidermal kaldığı sürece prognoz iyidir; ancak dermal invazyon geliştiğinde prognoz dramatik biçimde kötüleşir.",
            "bulletPoints": [
                "İnvazyon olmaksızın yıllarca intraepidermal kalabilir.",
                "Geniş lokal eksizyon gerekir; nüks riski yüksektir.",
                "Dermal invazyon gelişirse prognoz oldukça kötüdür."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Ekstramammary Paget hastalığında nadir olgularda dermal invazyon gelişir ve bu durumda prognoz kötüdür.",
                    "maskedTerm": "dermal invazyon",
                    "hint": "Tümör hücrelerinin bazal membranı aşarak alt bağ dokuya geçmesi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Ekstramammary Paget Hastalığında Evre ve Prognoz",
                    "tableHeaders": ["Evre / Durum", "Biyolojik Davranış", "Klinik Prognoz"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Saf İntraepidermal", "isMasked": False},
                                {"text": "Bazal membranı aşmaz, yatay yayılır", "isMasked": False},
                                {"text": "Mükemmel sağkalım; nüks riski yüksek", "isMasked": True, "hint": "iyi seyirli fakat tekrarlayıcı"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Dermal İnvaziv", "isMasked": False},
                                {"text": "Dermise geçiş ve lenfovasküler invazyon", "isMasked": True, "hint": "bağ dokusu istilası"},
                                {"text": "Oldukça kötü prognoz ve metastaz riski", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "İntraepidermalden İnvazif Faza",
                    "steps": [
                        "1. İntraepidermal Faz: Paget hücreleri epidermis içinde sınır tanımadan yayılır.",
                        "2. Cerrahi Güçlük: Mikroskobik sınırların genişliği nedeniyle eksizyon sonrası sık nüks oluşur.",
                        "3. Bazal Membran Yıkımı: İleri evrede proteaz salınımıyla bazal membran delinir.",
                        "4. Dermal İnvazyon: Dermal lenfatiklere ulaşan tümör metastaz yapar ve prognoz kötüleşir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Ekstramammary Paget hastalığında geniş cerrahi eksizyona rağmen lokal nükslerin sık görülmesinin temel patolojik nedeni nedir?",
                    "answer": "Atipik Paget hücrelerinin makroskopik olarak görünen klinik eritem sınırlarının çok ötesinde, mikroskobik olarak normal görünen epidermise yayılmış olmasıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Ekstramammary Paget Seyri ve Prognozu",
                    "items": [
                        {"text": "İntraepidermal seyir invazyon olmaksızın yıllarca devam edebilir.", "isLie": False, "explanation": "Doğru. Yavaş ve indolent bir intraepitelyal süreçtir."},
                        {"text": "Temel tedavi cerrahi olarak geniş lokal eksizyon yapılmasıdır.", "isLie": False, "explanation": "Doğru. Cerrahi sınır güvenliği hedeflenir."},
                        {"text": "Dermal invazyon gelişen olgularda prognoz oldukça kötüdür.", "isLie": False, "explanation": "Doğru. Dermal invazyon metastaz riskini artırır."},
                        {"text": "Ekstramammary Paget olgularında ameliyattan sonra nüks olasılığı kesinlikle sıfırdır.", "isLie": True, "explanation": "Tuzak! Mikroskobik sınırların belirsizliği nedeniyle nüks oranı oldukça yüksektir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Ekstramammary Paget hastalığının klinik seyri ve prognozu ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "İntraepidermal sınırlı kaldıkça indolenttir; ancak dermal invazyon geliştiğinde prognoz dramatik biçimde kötüleşir",
                            "isCorrect": True,
                            "explanation": "Dermal invazyon lenfatik yayılım ve uzak metastaz riskini başlatarak prognozu bozar."
                        },
                        {
                            "key": "B",
                            "text": "İlk günden itibaren tüm olgularda doğrudan karaciğer yetmezliği ile ölüm gelişir",
                            "isCorrect": False,
                            "explanation": "Yıllarca sadece lokal intraepidermal kalabilir."
                        },
                        {
                            "key": "C",
                            "text": "Cerrahi rezeksiyondan sonra hiçbir zaman nüks etmez",
                            "isCorrect": False,
                            "explanation": "Sınırlar belirsiz olduğundan nüks oranı oldukça yüksektir."
                        },
                        {
                            "key": "D",
                            "text": "Dermal invazyon geliştiğinde hastanın sağkalımı tamamen normal popülasyonla aynıdır",
                            "isCorrect": False,
                            "explanation": "Dermal invazyon prognozu çok kötüleştirir."
                        }
                    ]
                }
            ]
        },
        # S25
        {
            "slideNumber": 25,
            "title": "Vajina Anatomisi ve İkincil Tutulum Eğilimi",
            "subtitle": "Kollapsöz fibromüsküler kanal ve primer hastalıkların nadirliği",
            "clinicalFocus": "Vajina Patolojisine Giriş",
            "content": "Vajina, serviksten vulvaya kadar uzanan, ön ve arka duvarları normalde birbirine temas eden (kollabe) fibromüsküler elastik bir kanaldır. İç yüzeyi keratinize olmayan çok katlı yassı epitelle döşelidir.\n\n- **Primer Hastalık Nadirliği:** Erişkin kadınlarda vajina, diğer genital organlara kıyasla ==NADİREN PRİMER BİR HASTALIK YERİDİR==. Primer maligniteleri kadın genital kanserlerinin %1'inden azını oluşturur.\n- **Sekonder Tutulum Baskınlığı:** Vajinada karşılaşılan patolojiler çoğunlukla komşu pelvik organlardan doğrudan uzanım ya da metastaz yoluyla gelişir:\n  * Serviks karsinomunun vajina fornikslerine doğrudan yayılımı,\n  * Rektum ve mesane karsinomlarının vajina duvarını infiltre etmesi,\n  * Komşu vulvar veya pelvik enfeksiyonların asendan/desendan bulaşı.\n- **Glandüler Yapı Eksikliği:** Vajina duvarında kendi özgül salgı bezleri bulunmaz; vajinal ıslaklık servikal mukus ve vasküler transüdasyonla sağlanır.\n\n> [!NOTE]\n> Vajinada bir kitle saptandığında primer vajinal tümörden önce mutlaka serviks, mesane ve rektum gibi komşu organ kanserlerinin sekonder yayılımı ekarte edilmelidir.",
            "synthesisNarrative": "Vajina, serviksten vulvaya kadar uzanan, ön ve arka duvarları normalde birbirine temas eden (kollabe) fibromüsküler elastik bir kanaldır. İç yüzeyi keratinize olmayan çok katlı yassı epitelle döşelidir.\n\n- **Primer Hastalık Nadirliği:** Erişkin kadınlarda vajina, diğer genital organlara kıyasla ==NADİREN PRİMER BİR HASTALIK YERİDİR==. Primer maligniteleri kadın genital kanserlerinin %1'inden azını oluşturur.\n- **Sekonder Tutulum Baskınlığı:** Vajinada karşılaşılan patolojiler çoğunlukla komşu pelvik organlardan doğrudan uzanım ya da metastaz yoluyla gelişir:\n  * Serviks karsinomunun vajina fornikslerine doğrudan yayılımı,\n  * Rektum ve mesane karsinomlarının vajina duvarını infiltre etmesi,\n  * Komşu vulvar veya pelvik enfeksiyonların asendan/desendan bulaşı.\n- **Glandüler Yapı Eksikliği:** Vajina duvarında kendi özgül salgı bezleri bulunmaz; vajinal ıslaklık servikal mukus ve vasküler transüdasyonla sağlanır.\n\n> [!NOTE]\n> Vajinada bir kitle saptandığında primer vajinal tümörden önce mutlaka serviks, mesane ve rektum gibi komşu organ kanserlerinin sekonder yayılımı ekarte edilmelidir.",
            "bulletPoints": [
                "Vajina nadiren primer hastalık merkezidir.",
                "En sık komşu organ (serviks, mesane, rektum) kanserleri yayılır.",
                "Primer vajina karsinomu kadın genital tümörlerinin <%1'idir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Erişkin kadınlarda vajina nadiren primer hastalık yeridir ve sıklıkla komşu organların sekonder tutulumu izlenir.",
                    "maskedTerm": "sekonder tutulumu",
                    "hint": "Tümörün komşuluk yoluyla ikincil olarak organı istila etmesi durumu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vajinada Primer ve Sekonder Hastalık Dağılımı",
                    "tableHeaders": ["Köken", "Sıklık", "Tipik Örnekler"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Primer Vajinal Hastalık", "isMasked": False},
                                {"text": "Son derece nadir (<%1 karsinom)", "isMasked": True, "hint": "oldukça düşük primer sıklık"},
                                {"text": "Vajinal intraepitelyal neoplazi (VAIN), Gartner kisti"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Sekonder Tutulum", "isMasked": False},
                                {"text": "Belirgin biçimde daha sık", "isMasked": False},
                                {"text": "Serviks, rektum ve mesane karsinomlarının invazyonu", "isMasked": True, "hint": "komşu pelvik kanserlerin yayılımı"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Vajinada Sekonder Yayılım Zinciri",
                    "steps": [
                        "1. Komşu Tümör: Ektoservikste veya rektumda invaziv karsinom kitlesi büyür.",
                        "2. Doğrudan Uzanım: Kanser hücreleri vajinanın üst fornikslerine veya arka duvarına sızar.",
                        "3. Duvar İnvazyonu: Vajina fibromüsküler katmanları tümörle infiltre olur.",
                        "4. Klinik Görünüm: Muayenede vajinada ülsere kitle görülür; araştırıldığında primer odağın serviks olduğu saptanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Erişkin kadında vajinada malign bir tümör kitlesi görüldüğünde öncelikle hangi olasılık ekarte edilmelidir?",
                    "answer": "Primer vajinal karsinom çok nadir olduğundan, öncelikle komşu organların (serviks, rektum, mesane) doğrudan sekonder tutulumu veya metastazı ekarte edilmelidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajina Patolojisinin Temel Özellikleri",
                    "items": [
                        {"text": "Vajina erişkinlerde nadiren primer hastalık merkezidir.", "isLie": False, "explanation": "Doğru. Primer patolojiler oldukça seyrektir."},
                        {"text": "Vajinada komşu organ kanserlerinin sekonder tutulumu daha sık izlenir.", "isLie": False, "explanation": "Doğru. Serviks ve mesane invazyonu sıktır."},
                        {"text": "Vajina iç yüzeyi keratinize olmayan çok katlı yassı epitelle kaplıdır.", "isLie": False, "explanation": "Doğru. Normal histolojisi bu şekildedir."},
                        {"text": "Vajina tüm kadın genital sistemi içerisinde primer karsinomun en sık geliştiği organdır.", "isLie": True, "explanation": "Tuzak! Tam aksine vajina primer karsinomun en az görüldüğü organlardan biridir (<%1)."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vajinanın genel hastalık özellikleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Erişkinlerde nadiren primer hastalık yeridir; komşu serviks veya mesane kanserlerinin sekonder yayılımı daha sıktır",
                            "isCorrect": True,
                            "explanation": "Vajinanın en önemli onkolojik kuralı primer lezyonların nadirliği ve sekonder tutulumun sıklığıdır."
                        },
                        {
                            "key": "B",
                            "text": "Tüm jinekolojik kanserlerin %95'i primer vajinal adenokarsinomdur",
                            "isCorrect": False,
                            "explanation": "Primer vajinal kanser tüm jinekolojik kanserlerin %1'inden azdır."
                        },
                        {
                            "key": "C",
                            "text": "Vajina hiçbir zaman komşu organların enfeksiyon ve tümörlerinden etkilenmez",
                            "isCorrect": False,
                            "explanation": "Komşu organ patolojileri vajinaya kolayca yayılır."
                        },
                        {
                            "key": "D",
                            "text": "Vajina epitelinde yalnızca tek katlı silyalı prizmatik epitel bulunur",
                            "isCorrect": False,
                            "explanation": "Vajina keratinize olmayan çok katlı yassı epitelle döşelidir."
                        }
                    ]
                }
            ]
        },
        # S26
        {
            "slideNumber": 26,
            "title": "Vajinanın Konjenital Anomalileri ve Gartner Kanal Kisti",
            "subtitle": "Müllerian füzyon defektleri ve kalıcı Wolffian kanal kalıntıları",
            "clinicalFocus": "Embriyoloji ve Konjenital Kistler",
            "content": "Vajinanın konjenital anomalileri nadir olmakla birlikte embriyolojik gelişim basamaklarındaki aksaklıkları yansıtır.\n\n- **Müllerian Gelişim Anomalileri:** Vajinanın tam yokluğu (agenezisi), transvers vajinal septum ve longitudinal çift vajina (vajina dupleks) gibi defektler Müllerian kanallarının füzyon veya rekanalizasyon yetersizliğinden doğar. Sıklıkla septalı serviks ve bikornis/septat uterusla birliktedir.\n- **Gartner Kanal Kisti (Mezonefrik Kist):**\n  * Kadın embriyogenezinde gerileyip kaybolması gereken **Wolffian (mezonefrik) kanal kalıntılarından** gelişir.\n  * En sık vajinanın **lateral (yan) duvarlarına** yerleşir.\n  * Çoğunlukla 1-2 cm çapında, asemptomatik, selim ve berrak sıvı içeren kistlerdir; nadiren büyük boyutlara ulaşarak disparoni yapabilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Vajinanın lateral duvarında yerleşen, kalıcı Wolffian (mezonefrik) kanal kalıntısından türeyen konjenital kistik yapı Gartner kanal kistidir.",
            "synthesisNarrative": "Vajinanın konjenital anomalileri nadir olmakla birlikte embriyolojik gelişim basamaklarındaki aksaklıkları yansıtır.\n\n- **Müllerian Gelişim Anomalileri:** Vajinanın tam yokluğu (agenezisi), transvers vajinal septum ve longitudinal çift vajina (vajina dupleks) gibi defektler Müllerian kanallarının füzyon veya rekanalizasyon yetersizliğinden doğar. Sıklıkla septalı serviks ve bikornis/septat uterusla birliktedir.\n- **Gartner Kanal Kisti (Mezonefrik Kist):**\n  * Kadın embriyogenezinde gerileyip kaybolması gereken **Wolffian (mezonefrik) kanal kalıntılarından** gelişir.\n  * En sık vajinanın **lateral (yan) duvarlarına** yerleşir.\n  * Çoğunlukla 1-2 cm çapında, asemptomatik, selim ve berrak sıvı içeren kistlerdir; nadiren büyük boyutlara ulaşarak disparoni yapabilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Vajinanın lateral duvarında yerleşen, kalıcı Wolffian (mezonefrik) kanal kalıntısından türeyen konjenital kistik yapı Gartner kanal kistidir.",
            "bulletPoints": [
                "Agenezi ve çift/septalı vajina Müllerian füzyon defektleridir.",
                "Gartner kanal kisti kalıcı Wolffian kanal kalıntısından gelişir.",
                "Gartner kisti lateral vajina duvarına yerleşir ve selimdir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Lateral vajinal duvarda yerleşen Gartner kanal kisti kalıcı Wolffian kanal kalıntısından gelişir.",
                    "maskedTerm": "Wolffian kanal",
                    "hint": "Mezonefrik kanal olarak da adlandırılan embriyolojik yapı"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vajinal Kistlerin Embriyolojik Köken Ayrımı",
                    "tableHeaders": ["Kist Tipi", "Embriyolojik Köken", "Tipik Lokalizasyon"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Gartner Kanal Kisti", "isMasked": False},
                                {"text": "Wolffian (mezonefrik) kanal kalıntısı", "isMasked": True, "hint": "erkek mezonefrik taslak kalıntısı"},
                                {"text": "Lateral vajinal duvar", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Müllerian / İnklüzyon Kisti", "isMasked": False},
                                {"text": "Paramezonefrik epitel veya doğum travması", "isMasked": False},
                                {"text": "Distal vajina veya arka duvar", "isMasked": True, "hint": "epitelyal inklüzyon sahası"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Wolffian Kalıntıdan Gartner Kistine",
                    "steps": [
                        "1. Embriyogenez: Dişi fetüste mezonefrik (Wolff) kanalları normalde geriler.",
                        "2. Kalıntı Dokusu: Kanalın lateral vajina duvarındaki parçaları dejenere olmadan kalır.",
                        "3. Salgı Birikimi: Mezonefrik epitel sıvı salgılayarak lümende biriktirir.",
                        "4. Gartner Kisti: Lateral vajina duvarında submukozal selim kistik kitle oluşur."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vajina lateral duvarında saptanan Gartner kanal kistinin embriyolojik kökeni nedir?",
                    "answer": "Dişi embriyogenezinde gerilemeyip kalıcı olan Wolffian (mezonefrik) kanal kalıntısıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajinanın Anomalileri ve Gartner Kisti",
                    "items": [
                        {"text": "Septalı veya çift vajina Müllerian füzyon bozukluklarına bağlı gelişebilir.", "isLie": False, "explanation": "Doğru. Paramezonefrik kanal defektidir."},
                        {"text": "Gartner kanal kisti lateral vajinal duvarda yerleşim gösterir.", "isLie": False, "explanation": "Doğru. Anatomik konumu lateral duvardır."},
                        {"text": "Gartner kisti kalıcı Wolffian kanal kalıntısından köken alır.", "isLie": False, "explanation": "Doğru. Mezonefrik duktus artığıdır."},
                        {"text": "Gartner kanal kisti doğrudan fetal nöral tüpün kapanma defektinden türer.", "isLie": True, "explanation": "Tuzak! Gartner kisti nöral tüple ilişkisizdir; mezonefrik ürogenital kanal kalıntısıdır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Gartner kanal kistinin lokalizasyonu ve embriyolojik kökeni ile ilgili doğru ifade hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Lateral vajinal duvarda yerleşir ve kalıcı Wolffian (mezonefrik) kanal kalıntısından gelişir",
                            "isCorrect": True,
                            "explanation": "Gartner kistinin klasik anatomik ve embriyolojik tanımı budur."
                        },
                        {
                            "key": "B",
                            "text": "Klitoris üzerinde yerleşir ve yüz kaslarının hipertrofisinden doğar",
                            "isCorrect": False,
                            "explanation": "Klitoriste değil, vajina lateral duvarında bulunur."
                        },
                        {
                            "key": "C",
                            "text": "Endometriumdan köken alan masif kemik metaplazisi kistidir",
                            "isCorrect": False,
                            "explanation": "Kemik metaplazisi değildir, selim sıvı dolu epitelyal kisttir."
                        },
                        {
                            "key": "D",
                            "text": "Bartholin bezi salgı kanalının aşırı genişlemesiyle oluşan apseleşmiş kisttir",
                            "isCorrect": False,
                            "explanation": "Bartholin kisti vulvadadır, Gartner kisti vajina lateral duvarındadır."
                        }
                    ]
                }
            ]
        },
        # S27
        {
            "slideNumber": 27,
            "title": "Vajinit Patolojisi: Tanım, Lökore ve Mikrobiyal Denge",
            "subtitle": "Normal floradan fırsatçı enflamasyona geçiş dinamikleri",
            "clinicalFocus": "Vajinit Fizyopatolojisi",
            "content": "Vajinit, vajina mukozasının genellikle enfeksiyöz ajanlara bağlı olarak gelişen, geçici ve son derece yaygın yangısal durumudur.\n\n- **Kardinal Belirti (Lökore):** Vajinitin en temel klinik bulgusu vajinal akıntıdır (**lökore**). Akıntının kıvamı, rengi, kokusu ve mikroskobik özellikleri etyolojik patojene göre dramatik farklılıklar gösterir.\n- **Kommensal Flora Dengesi:** Sağlıklı bir vajinada baskın mikroorganizma laktobasillerdir (Döderlein basilleri). Laktobasiller glikojenden laktik asit üreterek vajinal pH'yı asidik (pH 3.8 - 4.5) tutar ve patojenlerin kolonizasyonunu engeller.\n- **Alevlenmeyi Tetikleyen Durumlar:** Diyabet mellitus, sistemik antibiyotik kullanımı, gebelik, yakın zamanda düşük veya doğum ve immün yetmezlik flora dengesini bozarak kommensal mikroorganizmaların patojen hale gelmesine yol açar.\n\n> [!NOTE]\n> Vajinit etkenlerinin bir kısmı cinsel yolla bulaşırken, bir kısmı da normal floranın fırsatçı biçimde aşırı çoğalmasıyla klinik tablo oluşturur.",
            "synthesisNarrative": "Vajinit, vajina mukozasının genellikle enfeksiyöz ajanlara bağlı olarak gelişen, geçici ve son derece yaygın yangısal durumudur.\n\n- **Kardinal Belirti (Lökore):** Vajinitin en temel klinik bulgusu vajinal akıntıdır (**lökore**). Akıntının kıvamı, rengi, kokusu ve mikroskobik özellikleri etyolojik patojene göre dramatik farklılıklar gösterir.\n- **Kommensal Flora Dengesi:** Sağlıklı bir vajinada baskın mikroorganizma laktobasillerdir (Döderlein basilleri). Laktobasiller glikojenden laktik asit üreterek vajinal pH'yı asidik (pH 3.8 - 4.5) tutar ve patojenlerin kolonizasyonunu engeller.\n- **Alevlenmeyi Tetikleyen Durumlar:** Diyabet mellitus, sistemik antibiyotik kullanımı, gebelik, yakın zamanda düşük veya doğum ve immün yetmezlik flora dengesini bozarak kommensal mikroorganizmaların patojen hale gelmesine yol açar.\n\n> [!NOTE]\n> Vajinit etkenlerinin bir kısmı cinsel yolla bulaşırken, bir kısmı da normal floranın fırsatçı biçimde aşırı çoğalmasıyla klinik tablo oluşturur.",
            "bulletPoints": [
                "Temel bulgu vajinal akıntıdır (lökore).",
                "Laktobasiller asidik pH üreterek florayı korur.",
                "Diyabet, antibiyotik ve gebelik patojen alevlenmesini tetikler."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vajinitin en karakteristik klinik belirtisi vajinal akıntı yani tıbbi adıyla lökore tablosudur.",
                    "maskedTerm": "lökore",
                    "hint": "Vajinal akıntıyı tanımlayan klinik tıbbi terim"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vajinal Florada Denge ve Bozulma Faktörleri",
                    "tableHeaders": ["Faktör", "Fizyolojik Görev", "Bozulma Sonucu"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Laktobasiller (Döderlein)", "isMasked": False},
                                {"text": "Laktik asit üreterek pH'yı asidik tutmak", "isMasked": True, "hint": "asidik bariyer savunması"},
                                {"text": "Patojen bakterilerin ve mantarların baskılanması", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Geniş Spektrumlu Antibiyotik", "isMasked": False},
                                {"text": "Laktobasil popülasyonunu yok eder", "isMasked": False},
                                {"text": "pH yükselir; Candida ve anaeroblar çoğalır", "isMasked": True, "hint": "fırsatçı süperenfeksiyon alevlenmesi"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Floradan Semptomatik Vajinite",
                    "steps": [
                        "1. Denge Bozulması: Antibiyotik veya immün supresyon laktobasil sayısını düşürür.",
                        "2. Asidite Kaybı: Koruyucu laktik asit kalkanı zayıflar.",
                        "3. Patojen Artışı: Kommensal mantarlar veya anaerob bakteriler aşırı çoğalır.",
                        "4. Lökore: Epitelde gelişen yangı ve lökosit birikimiyle karakteristik vajinal akıntı belirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vajinal epitelin enfeksiyonlara karşı en önemli fizyolojik savunma kalkanı nedir?",
                    "answer": "Laktobasillerin (Döderlein basilleri) epitel glikojeninden laktik asit üreterek vajina pH'sını asidik düzeyde (pH 3.8 - 4.5) tutmasıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajinit Fizyopatolojisi ve Flora",
                    "items": [
                        {"text": "Vajinitin temel klinik bulgusu vajinal akıntıdır (lökore).", "isLie": False, "explanation": "Doğru. Lökore en sık başvuru semptomudur."},
                        {"text": "Normal vajinal floranın temel koruyucusu laktik asit üreten laktobasillerdir.", "isLie": False, "explanation": "Doğru. Asidik ortam enfeksiyonları engeller."},
                        {"text": "Antibiyotik kullanımı ve diyabet vajinit alevlenmesine zemin hazırlar.", "isLie": False, "explanation": "Doğru. Flora dengesini bozarak fırsatçı çoğalmayı tetikler."},
                        {"text": "Vajinit daima retrograd yolla doğrudan beyin omurilik sıvısına ilerler.", "isLie": True, "explanation": "Tuzak! Vajinit lokal bir mukozal inflamasyondur; BOS ile hiçbir anatomik bağlantısı yoktur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vajinit patofizyolojisi ve normal vajinal flora ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Laktobasiller asidik pH oluşturarak korur; antibiyotik veya diyabet florayı bozarak vajinite zemin hazırlar",
                            "isCorrect": True,
                            "explanation": "Vajinal ekolojinin ve vajinit patogenezinin temel mekanizması budur."
                        },
                        {
                            "key": "B",
                            "text": "Vajinit hiçbir zaman akıntı oluşturmaz, daima saf kemik ağrısı ile seyreder",
                            "isCorrect": False,
                            "explanation": "Vajinitin kardinal semptomu akıntıdır (lökore)."
                        },
                        {
                            "key": "C",
                            "text": "Sağlıklı vajinal floranın pH değeri daima 8.5'in üzerinde aşırı alkalidir",
                            "isCorrect": False,
                            "explanation": "Sağlıklı vajinal pH asidiktir (3.8 - 4.5)."
                        },
                        {
                            "key": "D",
                            "text": "Vajina florasında hiçbir mikroorganizma bulunmaz, tamamen sterildir",
                            "isCorrect": False,
                            "explanation": "Vajina zengin bir kommensal laktobasil florasına sahiptir."
                        }
                    ]
                }
            ]
        },
        # S28
        {
            "slideNumber": 28,
            "title": "Üç Temel Vajinit Etkeni ve Akıntı Paternleri",
            "subtitle": "Candida, Trichomonas ve Gardnerella klinik ayrımı",
            "clinicalFocus": "Klinik Etyoloji",
            "content": "Klinik pratikte vajinit olgularının büyük kısmı üç temel patojen tarafından oluşturulur. Bu üç etkenin oluşturduğu akıntı karakteri ayırıcı tanıda anahtar role sahiptir:\n\n- **1. Candida albicans (Mantar):** Kadınların yaklaşık %20'sinde normal florada bulunur. Yoğun kaşıntı, eritem ve **kalın, beyaz, kesilmiş süt / peynir benzeri akıntı** oluşturur.\n- **2. Trichomonas vaginalis (Parazit):** Kamçılı bir protozoondur; dünya genelinde en yaygın viral olmayan cinsel yolla bulaşan patojendir. Bol, sulu, **köpüklü, sarı-yeşil renkli akıntı** ve şiddetli vulvar tahriş yapar.\n- **3. Gardnerella vaginalis (Bakteri):** Bakteriyel vajinozun ana etkenidir. İnce, homojen, **gri-beyaz renkli, amin (balık) kokulu akıntı** ile karakterizedir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Peynirimsi beyaz akıntı = Candida; Köpüklü sarı-yeşil akıntı = Trichomonas; Balık kokulu gri-beyaz akıntı = Gardnerella vaginalis.",
            "synthesisNarrative": "Klinik pratikte vajinit olgularının büyük kısmı üç temel patojen tarafından oluşturulur. Bu üç etkenin oluşturduğu akıntı karakteri ayırıcı tanıda anahtar role sahiptir:\n\n- **1. Candida albicans (Mantar):** Kadınların yaklaşık %20'sinde normal florada bulunur. Yoğun kaşıntı, eritem ve **kalın, beyaz, kesilmiş süt / peynir benzeri akıntı** oluşturur.\n- **2. Trichomonas vaginalis (Parazit):** Kamçılı bir protozoondur; dünya genelinde en yaygın viral olmayan cinsel yolla bulaşan patojendir. Bol, sulu, **köpüklü, sarı-yeşil renkli akıntı** ve şiddetli vulvar tahriş yapar.\n- **3. Gardnerella vaginalis (Bakteri):** Bakteriyel vajinozun ana etkenidir. İnce, homojen, **gri-beyaz renkli, amin (balık) kokulu akıntı** ile karakterizedir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Peynirimsi beyaz akıntı = Candida; Köpüklü sarı-yeşil akıntı = Trichomonas; Balık kokulu gri-beyaz akıntı = Gardnerella vaginalis.",
            "bulletPoints": [
                "Candida: Kalın, beyaz, peynirimsi akıntı ve kaşıntı.",
                "Trichomonas: Bol, köpüklü, sarı-yeşil sulu akıntı.",
                "Gardnerella: İnce, gri-beyaz, tipik balık kokulu akıntı."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Trichomonas vaginalis enfeksiyonunda vajinal akıntı karakteristik olarak köpüklü sarı-yeşil renktedir.",
                    "maskedTerm": "köpüklü sarı-yeşil",
                    "hint": "Paraziter vajinite özgü gaz kabarcıklı renkli akıntı"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Üç Büyük Vajinit Etkeninin Klinik Karşılaştırması",
                    "tableHeaders": ["Etken", "Biyolojik Sınıf", "Akıntı Özelliği"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Candida albicans", "isMasked": False},
                                {"text": "Fırsatçı mantar", "isMasked": False},
                                {"text": "Beyaz peynirimsi / kesilmiş süt kıvamında", "isMasked": True, "hint": "floküle beyaz akıntı"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Trichomonas vaginalis", "isMasked": False},
                                {"text": "Kamçılı protozoon (CYBH)", "isMasked": True, "hint": "hareketli paraziter ajan"},
                                {"text": "Bol, sulu, köpüklü, sarı-yeşil", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Gardnerella vaginalis", "isMasked": False},
                                {"text": "Fakültatif anaerob bakteri", "isMasked": False},
                                {"text": "İnce, gri-beyaz, tipik balık kokulu", "isMasked": True, "hint": "amin kokulu homojen akıntı"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Akıntı Tipinden Etyolojik Tahmine",
                    "steps": [
                        "1. Spekulum Muayenesi: Vajina duvarında ve fornikste biriken akıntının vasfı incelenir.",
                        "2. Peynirimsi Beyaz: Akıntı kesilmiş süt gibiyse ve kaşıntı baskınsa Candida düşünülür.",
                        "3. Köpüklü Sarı-Yeşil: Akıntı bol köpüklü ve çilek serviks eşlik ediyorsa Trichomonas düşünülür.",
                        "4. Balık Kokusu: Homojen gri-beyaz akıntı ve KOH ile amin kokusu varsa Gardnerella düşünülür."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Candida albicans, Trichomonas vaginalis ve Gardnerella vaginalis akıntılarının tipik makroskopik ve koku özellikleri nelerdir?",
                    "answer": "Candida: Beyaz peynirimsi, kokusuz/hafif ekşi; Trichomonas: Bol, sulu, köpüklü sarı-yeşil; Gardnerella: İnce, homojen gri-beyaz ve tipik balık kokuludur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajinit Etkenleri ve Akıntı Nitelikleri",
                    "items": [
                        {"text": "Candida albicans kalın, beyaz ve peynirimsi akıntı oluşturur.", "isLie": False, "explanation": "Doğru. Kesilmiş süt görünümü tipiktir."},
                        {"text": "Trichomonas vaginalis bol, sulu ve köpüklü sarı-yeşil akıntı yapar.", "isLie": False, "explanation": "Doğru. Paraziter akıntı köpüklüdür."},
                        {"text": "Gardnerella vaginalis ince gri-beyaz ve balık kokulu akıntıyla seyreder.", "isLie": False, "explanation": "Doğru. Bakteriyel vajinoz kokusu amin kaynaklıdır."},
                        {"text": "Trichomonas vaginalis yalnızca kalın kuru siyah kabuklar üretir, asla sıvı akıntı yapmaz.", "isLie": True, "explanation": "Tuzak! Trichomonas bol, sulu ve köpüklü akıntı yapar; siyah kabuk oluşturmaz."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vajinal akıntı paternleri ve etken eşleştirmesi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Candida beyaz peynirimsi, Trichomonas köpüklü sarı-yeşil, Gardnerella ise balık kokulu gri-beyaz akıntı yapar",
                            "isCorrect": True,
                            "explanation": "Bu üçlü ayrım jinekolojik patolojinin en klasik tanı formülüdür."
                        },
                        {
                            "key": "B",
                            "text": "Gardnerella daima köpüklü koyu kırmızı kanlı kitle şeklinde izlenir",
                            "isCorrect": False,
                            "explanation": "Gardnerella ince gri-beyaz homojen akıntı yapar."
                        },
                        {
                            "key": "C",
                            "text": "Candida akıntısı yeşil renkli gaz kabarcıklarından ibarettir",
                            "isCorrect": False,
                            "explanation": "Candida akıntısı beyaz ve peynirimsidir."
                        },
                        {
                            "key": "D",
                            "text": "Trichomonas hiçbir zaman akıntı oluşturmaz, sadece saç dökülmesi yapar",
                            "isCorrect": False,
                            "explanation": "Trichomonas bol ve köpüklü sarı-yeşil lökorenin ana etkenidir."
                        }
                    ]
                }
            ]
        },
        # S29
        {
            "slideNumber": 29,
            "title": "Vajinitin Mikroskobik Tanısı: Hifler, Parazitler ve Clue Cells",
            "subtitle": "Pap smear, ıslak preparat ve Gram boyamada patognomonik bulgular",
            "clinicalFocus": "Mikroskobik Tanı Yöntemleri",
            "content": "Üç temel vajinit etkeninin kesin ayırıcı tanısı, basit mikroskobik incelemeler ve sitolojik preparatlarla hızla konulur:\n\n- **Candida Tanısı:** Sitolojik incelemede (Papanicolaou testi veya ıslak preparata %10 KOH damlatılması) mantarın tomurcuklanan maya hücreleri (**blastosporlar**) ve uzamış **psödohif / gerçek hif** formları net olarak gösterilir.\n- **Trichomonas Tanısı:** Taze vajinal salgının serum fizyolojikle incelendiği direkt mikroskopide (ıslak preparat), kamçılarıyla aktif olarak **hareket eden armut biçimli trofozoitler** patognomoniktir.\n- **Gardnerella Tanısı:** Rutin Pap yaymasında veya ıslak yaymada skuamöz epitel hücrelerinin yüzeyini adeta bir toz bulutu gibi tamamen kaplayan kokobasiller izlenir; bu hücrelere **ipucu hücreleri (clue cells)** adı verilir. Hücre sınırları kokobasil örtüsü nedeniyle silikleşmiştir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Pap testinde hif görülmesi = Candida; Islak preparatta hareketli trofozoit = Trichomonas; Skuamöz epitel yüzeyini örten kokobasiller (Clue cells) = Gardnerella vaginalis.",
            "synthesisNarrative": "Üç temel vajinit etkeninin kesin ayırıcı tanısı, basit mikroskobik incelemeler ve sitolojik preparatlarla hızla konulur:\n\n- **Candida Tanısı:** Sitolojik incelemede (Papanicolaou testi veya ıslak preparata %10 KOH damlatılması) mantarın tomurcuklanan maya hücreleri (**blastosporlar**) ve uzamış **psödohif / gerçek hif** formları net olarak gösterilir.\n- **Trichomonas Tanısı:** Taze vajinal salgının serum fizyolojikle incelendiği direkt mikroskopide (ıslak preparat), kamçılarıyla aktif olarak **hareket eden armut biçimli trofozoitler** patognomoniktir.\n- **Gardnerella Tanısı:** Rutin Pap yaymasında veya ıslak yaymada skuamöz epitel hücrelerinin yüzeyini adeta bir toz bulutu gibi tamamen kaplayan kokobasiller izlenir; bu hücrelere **ipucu hücreleri (clue cells)** adı verilir. Hücre sınırları kokobasil örtüsü nedeniyle silikleşmiştir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Pap testinde hif görülmesi = Candida; Islak preparatta hareketli trofozoit = Trichomonas; Skuamöz epitel yüzeyini örten kokobasiller (Clue cells) = Gardnerella vaginalis.",
            "bulletPoints": [
                "Candida: Pap smear veya KOH'ta hif ve psödohif yapıları.",
                "Trichomonas: Islak preparatta aktif hareketli trofozoitler.",
                "Gardnerella: Epiteli örten kokobasilli ipucu hücreleri (clue cells)."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Gardnerella vaginalis enfeksiyonunda yüzeyi kokobasillerle kaplanmış skuamöz epitel hücrelerine clue cells adı verilir.",
                    "maskedTerm": "clue cells",
                    "hint": "İpucu hücreleri anlamına gelen patognomonik histolojik terim"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vajinit Etkenlerinin Mikroskobik Tanı Kriterleri",
                    "tableHeaders": ["Patojen", "Tanı Yöntemi", "Patognomonik Mikroskobik Bulgu"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Candida albicans", "isMasked": False},
                                {"text": "Pap smear / KOH preparatı", "isMasked": False},
                                {"text": "Hif ve psödohif formları", "isMasked": True, "hint": "uzamış mikotik iplikçikler"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Trichomonas vaginalis", "isMasked": False},
                                {"text": "Taze direkt ıslak preparat", "isMasked": True, "hint": "serum fizyolojikle inceleme"},
                                {"text": "Aktif hareketli kamçılı parazitler", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Gardnerella vaginalis", "isMasked": False},
                                {"text": "Pap yayması / Gram boyama", "isMasked": False},
                                {"text": "İpucu hücreleri (Clue cells)", "isMasked": True, "hint": "kokobasille kaplı yassı hücreler"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Mikroskopik Tanı Doğrulama Zinciri",
                    "steps": [
                        "1. Örnek Alma: Vajinal forniksten sürüntü ve direkt yayma hazırlanır.",
                        "2. KOH Testi: Potasyum hidroksit ile hücresel artıklar eritilerek mantar hifleri açığa çıkarılır.",
                        "3. Islak Bakı: Taze damlada kamçılarıyla dönerek yüzen Trichomonas aranır.",
                        "4. Pap Yayması: Epitel sınırlarını silen kokobasilli Clue cells görülerek Gardnerella doğrulanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bakteriyel vajinoz tanısında patognomonik kabul edilen 'Clue cell' (ipucu hücresi) nedir?",
                    "answer": "Yüzeyi yoğun Gardnerella vaginalis kokobasilleri ile kaplanmış, bu nedenle hücre sınırları silikleşmiş ve buzlu cam görünümü almış çok katlı yassı epitel hücresidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajinitin Mikroskobik Tanı Yöntemleri",
                    "items": [
                        {"text": "Papanicolaou (Pap) testinde Candida hif ve psödohifleri net olarak seçilebilir.", "isLie": False, "explanation": "Doğru. Pap sitolojisinde mantar filamentleri izlenir."},
                        {"text": "Taze ıslak preparatta Trichomonas vaginalis kamçılı hareketiyle kolayca tanınır.", "isLie": False, "explanation": "Doğru. Canlı hareketli trofozoitler patognomoniktir."},
                        {"text": "Gardnerella enfeksiyonunda epitel yüzeyini kokobasiller örterek Clue cells oluşturur.", "isLie": False, "explanation": "Doğru. Clue hücresi bakteriyel vajinozun temelidir."},
                        {"text": "Clue cells yalnızca nükleer fisyon yapan dev nötrofilik granülositlerdir.", "isLie": True, "explanation": "Tuzak! Clue cells nötrofil değil, yüzeyi bakterilerle kaplanmış yassı epitel (keratinosit) hücresidir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vajinal yaymanın mikroskobik incelemesinde aşağıdaki bulgulardan hangisi TRICHOMONAS VAGINALIS tanısını kesinleştirir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Taze direkt mikroskopide kamçılarıyla aktif hareket eden parazit trofozoitlerinin izlenmesi",
                            "isCorrect": True,
                            "explanation": "Trichomonas tanısında taze preparatta kamçılı hareketli protozoonun görülmesi altın standarttır."
                        },
                        {
                            "key": "B",
                            "text": "Skuamöz epitel yüzeyini kaplayan kalın kokobasiller (clue cells)",
                            "isCorrect": False,
                            "explanation": "Clue cells Gardnerella vaginalis enfeksiyonunun (bakteriyel vajinoz) bulgusudur."
                        },
                        {
                            "key": "C",
                            "text": "Pap testinde tomurcuklanan mantar sporları ve psödohif yapıları",
                            "isCorrect": False,
                            "explanation": "Hif ve sporlar Candida albicans enfeksiyonunu gösterir."
                        },
                        {
                            "key": "D",
                            "text": "Yalnızca aselüler homojen amiloid kitlelerinin saptanması",
                            "isCorrect": False,
                            "explanation": "Trichomonas paraziter bir enfeksiyondur, amiloid ile ilişkisizdir."
                        }
                    ]
                }
            ]
        },
        # S30
        {
            "slideNumber": 30,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 3] Ekstramammary Paget, Vajina ve Vajinitler",
            "subtitle": "21-29. adımların histopatolojik sentezi, klinik ayırıcı tanı ve mikroskopi",
            "clinicalFocus": "Bölüm 3 Özeti ve Pekiştirme",
            "content": "Bu üçüncü kontrol noktasında vulvanın Paget hastalığını, vajina anatomisini ve sık görülen vajinit tablolarını pekiştiriyoruz:\n\n- **Ekstramammary Paget:** Kırmızı kabuklu plak şeklinde kronik dermatiti taklit eder. Memeden farkı: Meme Paget'inde altta daima duktal karsinom bulunurken, vulva Paget'inde çoğunlukla altta tümör yoktur (primerdir). Büyük, soluk sitoplazmalı hücreler Müsikarmin ve PAS ile müsin (+)'tir. Dermal invazyon yoksa indolenttir; dermal invazyon gelişirse prognoz çok kötüdür.\n- **Vajina Anatomisi ve Gartner Kisti:** Vajina nadiren primer hastalık yeridir; sekonder invazyonlar sıktır. Lateral vajinal duvardaki Gartner kanal kisti kalıcı Wolffian kanal kalıntısından gelişir.\n- **Üç Büyük Vajinit:**\n  * Candida: Beyaz peynirimsi akıntı; Pap/KOH'ta hif ve sporlar.\n  * Trichomonas: Cinsel yolla bulaşan hareketli kamçılı parazit; köpüklü sarı-yeşil akıntı.\n  * Gardnerella: Amin kokulu gri-beyaz akıntı; mikroskopide clue cells.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Meme Paget'i = altta daima karsinom var; Vulva Paget'i = altta çoğunlukla tümör yok. Gartner kisti = lateral duvar Wolffian kalıntısı. Clue cell = Gardnerella.",
            "synthesisNarrative": "Bu üçüncü kontrol noktasında vulvanın Paget hastalığını, vajina anatomisini ve sık görülen vajinit tablolarını pekiştiriyoruz:\n\n- **Ekstramammary Paget:** Kırmızı kabuklu plak şeklinde kronik dermatiti taklit eder. Memeden farkı: Meme Paget'inde altta daima duktal karsinom bulunurken, vulva Paget'inde çoğunlukla altta tümör yoktur (primerdir). Büyük, soluk sitoplazmalı hücreler Müsikarmin ve PAS ile müsin (+)'tir. Dermal invazyon yoksa indolenttir; dermal invazyon gelişirse prognoz çok kötüdür.\n- **Vajina Anatomisi ve Gartner Kisti:** Vajina nadiren primer hastalık yeridir; sekonder invazyonlar sıktır. Lateral vajinal duvardaki Gartner kanal kisti kalıcı Wolffian kanal kalıntısından gelişir.\n- **Üç Büyük Vajinit:**\n  * Candida: Beyaz peynirimsi akıntı; Pap/KOH'ta hif ve sporlar.\n  * Trichomonas: Cinsel yolla bulaşan hareketli kamçılı parazit; köpüklü sarı-yeşil akıntı.\n  * Gardnerella: Amin kokulu gri-beyaz akıntı; mikroskopide clue cells.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Meme Paget'i = altta daima karsinom var; Vulva Paget'i = altta çoğunlukla tümör yok. Gartner kisti = lateral duvar Wolffian kalıntısı. Clue cell = Gardnerella.",
            "bulletPoints": [
                "Vulva Paget'i primerdir; meme Paget'inde altta duktal karsinom vardır.",
                "Gartner kisti lateral vajina duvarındaki Wolffian kalıntısıdır.",
                "Vajinit üçlüsü: Candida (hif), Trichomonas (hareketli parazit), Gardnerella (clue cell)."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vajina lateral duvarındaki Gartner kisti kalıcı mezonefrik kalıntı olan Wolffian kanal kalıntısından gelişir.",
                    "maskedTerm": "Wolffian kanal",
                    "hint": "Gartner kistine köken veren embriyolojik duktus"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bölüm 3 Kilit Tanısal Eşleştirmeler",
                    "tableHeaders": ["Hastalık / Yapı", "Ayırıcı Özellik", "Tanısal İpucu"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Vulva Paget Hastalığı", "isMasked": False},
                                {"text": "Altta yatan tümör çoğunlukla yoktur", "isMasked": True, "hint": "meme Paget'inden ayrılan primer yön"},
                                {"text": "Müsikarmin (+) soluk vakuollü hücreler", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Gartner Kisti", "isMasked": False},
                                {"text": "Lateral vajinal duvar kisti", "isMasked": False},
                                {"text": "Wolffian kanal kalıntısı", "isMasked": True, "hint": "mezonefrik embriyolojik artık"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Bakteriyel Vajinoz", "isMasked": False},
                                {"text": "Gardnerella vaginalis etkeni", "isMasked": False},
                                {"text": "İpucu hücreleri (Clue cells)", "isMasked": True, "hint": "kokobasille kaplı skuamöz hücre"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Bölüm 3 Klinikopatolojik Sentez",
                    "steps": [
                        "1. Vulva Egzematöz Lezyon: İnatçı kırmızı plaktan alınan biyopside müsin(+) Paget saptanır.",
                        "2. Altta Tümör Taraması: Memeden farklı olarak vulva Paget'inde çoğunlukla altta karsinom çıkmaz.",
                        "3. Vajinal Kitle: Lateral duvarda saptanan kistin mezonefrik Gartner kalıntısı olduğu anlaşılır.",
                        "4. Vajinal Lökore: Akıntı tipine göre (peynirimsi, köpüklü, balık kokulu) mikroskopik tanı konur."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bölüm 3 kapsamında incelenen patolojilerden hangileri doğrudan glandüler müsin üretimi ile karakterizedir?",
                    "answer": "Ekstramammary Paget hastalığı (Paget hücreleri Müsikarmin ve PAS pozitiftir) ve Bartholin bezinin normal salgısı müsin karakterindedir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Bölüm 3 Genel Tekrar",
                    "items": [
                        {"text": "Vulva Ekstramammary Paget hastalığında çoğunlukla altta yatan tümör bulunmaz.", "isLie": False, "explanation": "Doğru. Meme Paget'inden en temel farkıdır."},
                        {"text": "Gartner kanal kisti lateral vajinal duvarda yerleşir ve Wolffian kalıntısıdır.", "isLie": False, "explanation": "Doğru. Embriyolojik mezonefrik kalıntıdır."},
                        {"text": "Gardnerella enfeksiyonunun mikroskobik göstergesi Clue cells varlığıdır.", "isLie": False, "explanation": "Doğru. Kokobasille kaplı yassı hücrelerdir."},
                        {"text": "Meme Paget hastalığı hiçbir zaman alttaki meme karsinomu ile ilişkili değildir.", "isLie": True, "explanation": "Tuzak! Meme Paget hastalığında neredeyse daima altta yatan bir duktal meme karsinomu bulunur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Bölüm 3'te özetlenen klinikopatolojik antitelerle ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Vulva Paget'i çoğunlukla altta karsinom olmaksızın primer gelişir; Gartner kisti ise lateral vajinadaki Wolffian kalıntısıdır",
                            "isCorrect": True,
                            "explanation": "Bu sentez ifadesi her iki patolojinin de temel ayırıcı özelliklerini eksiksiz özetler."
                        },
                        {
                            "key": "B",
                            "text": "Trichomonas vajiniti yalnızca kuru deskuamatif pullar yapar ve akıntı kesinlikle oluşturmaz",
                            "isCorrect": False,
                            "explanation": "Trichomonas bol ve köpüklü sarı-yeşil akıntı yapar."
                        },
                        {
                            "key": "C",
                            "text": "Clue cells yalnızca böbrek toplayıcı kanallarından dökülen tübüler silendirlerdir",
                            "isCorrect": False,
                            "explanation": "Clue cells bakteriyel vajinozda görülen kokobasilli yassı epitel hücreleridir."
                        },
                        {
                            "key": "D",
                            "text": "Vajina erişkin kadında primer invaziv kanserlerin en sık görüldüğü organdır",
                            "isCorrect": False,
                            "explanation": "Vajina nadiren primer kanser yeridir (<%1)."
                        }
                    ]
                }
            ]
        }
    ]
    return slides

if __name__ == '__main__':
    slides = get_s3_slides()
    print(f'Section 3 created with {len(slides)} slides.')
