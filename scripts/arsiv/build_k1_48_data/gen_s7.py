import json

def get_s7_slides():
    slides = [
        # S61
        {
            "slideNumber": 61,
            "title": "Vulvanın Nadir Maligniteleri: Vulvar Malign Melanom",
            "subtitle": "Melanositik diferansiasyon, S100/Melan-A/HMB-45 ve Paget ayrımı",
            "clinicalFocus": "Nadir Vulvar Maligniteler",
            "content": "Vulvanın skuamöz karsinom dışındaki en önemli primer malignitesi **malign melanomdur**. Vulvar kanserlerin yaklaşık %3-5'ini oluşturur ve skuamöz karsinomdan sonra vulvanın ikinci en sık görülen malign tümörüdür.\n\n- **Klinik Görünüm:** Genellikle postmenopozal kadınlarda labia minora veya klitoris çevresinde asimetrik, sınırları düzensiz, alacalı pigmentli (siyah, kahverengi veya koyu mavi) hızla büyüyen pigmente nodül veya plaklar şeklinde belirir.\n- **Histopatoloji ve İmmünohistokimya:** Dermo-epidermal bileşkede ve dermiste pleomorfik, atipik nükleollü melanositler izlenir. Hücreler tek tek veya yuvalar halinde epidermise yayılabilir (pagetoid yayılım). Ayırıcı tanıda **S100, Melan-A, HMB-45 ve SOX10** pozitifliği tanıyı kesinleştirir.\n- **Paget Hastalığından Ayrım:** Ekstramammary Paget hastalığı müsin pozitif ve sitokeratin (CK7) pozitif iken; melanom müsin negatiftir ve S100/HMB-45/Melan-A pozitiftir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Vulvada pagetoid yayılım gösteren lezyonlarda ayırıcı tanı: Ekstramammary Paget (CK7+, Müsin+); Malign Melanom (S100+, HMB-45+, Melan-A+, Müsin-).",
            "synthesisNarrative": "Vulvanın skuamöz karsinom dışındaki en önemli primer malignitesi **malign melanomdur**. Vulvar kanserlerin yaklaşık %3-5'ini oluşturur ve skuamöz karsinomdan sonra vulvanın ikinci en sık görülen malign tümörüdür.\n\n- **Klinik Görünüm:** Genellikle postmenopozal kadınlarda labia minora veya klitoris çevresinde asimetrik, sınırları düzensiz, alacalı pigmentli (siyah, kahverengi veya koyu mavi) hızla büyüyen pigmente nodül veya plaklar şeklinde belirir.\n- **Histopatoloji ve İmmünohistokimya:** Dermo-epidermal bileşkede ve dermiste pleomorfik, atipik nükleollü melanositler izlenir. Hücreler tek tek veya yuvalar halinde epidermise yayılabilir (pagetoid yayılım). Ayırıcı tanıda **S100, Melan-A, HMB-45 ve SOX10** pozitifliği tanıyı kesinleştirir.\n- **Paget Hastalığından Ayrım:** Ekstramammary Paget hastalığı müsin pozitif ve sitokeratin (CK7) pozitif iken; melanom müsin negatiftir ve S100/HMB-45/Melan-A pozitiftir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Vulvada pagetoid yayılım gösteren lezyonlarda ayırıcı tanı: Ekstramammary Paget (CK7+, Müsin+); Malign Melanom (S100+, HMB-45+, Melan-A+, Müsin-).",
            "bulletPoints": [
                "Malign melanom vulvanın ikinci en sık primer malignitesidir.",
                "S100, HMB-45 ve Melan-A immünohistokimyasal belirteçleri pozitiftir.",
                "Ekstramammary Paget hastalığından müsin negatifliği ve melanositik belirteçlerle ayrılır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vulvar malign melanom tanısında melanositik diferansiasyonu kanıtlayan antikor paneli S100 ve HMB-45 belirteçlerini içerir.",
                    "maskedTerm": "HMB-45",
                    "hint": "Melanom ayırıcı tanısında kullanılan spesifik melanozom antijeni"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulvada Pagetoid Yayılım Gösteren Lezyonların Ayrımı",
                    "tableHeaders": ["Belirteç / Özellik", "Ekstramammary Paget", "Vulvar Malign Melanom"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Sitokeratin 7 (CK7)", "isMasked": False},
                                {"text": "Pozitif (+)", "isMasked": False},
                                {"text": "Negatif (-)", "isMasked": True, "hint": "karsinom dışı non-epitelyal yanıt"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "S100 / HMB-45 / Melan-A", "isMasked": False},
                                {"text": "Negatif (-)", "isMasked": False},
                                {"text": "Pozitif (+)", "isMasked": True, "hint": "melanositik diferansiasyon kanıtı"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Pigmente Vulvar Lezyondan Melanom Tanısına",
                    "steps": [
                        "1. Şüpheli Lezyon: Labium minus üzerinde asimetrik, koyu kahverengi-siyah pigmente lezyon saptanır.",
                        "2. Eksizyonel Biyopsi: Lezyon sağlam sınırlarla çıkarılarak patolojik incelemeye alınır.",
                        "3. Morfolojik Ayrım: Epidermise pagetoid dağılan atipik hücreler ve intraselüler melanin izlenir.",
                        "4. İmmünohistokimya: S100 ve HMB-45 diffüz pozitifliğiyle malign melanom doğrulanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulvada epidermise pagetoid yayılım gösteren hücrelerin Ekstramammary Paget mi yoksa Malign Melanom mu olduğunu kesin olarak ayıran immünohistokimyasal profil nedir?",
                    "answer": "Paget: CK7 (+), Müsin (+), S100/HMB-45 (-); Melanom: S100 (+), HMB-45 (+), Melan-A (+), CK7/Müsin (-)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vulvar Malign Melanom",
                    "items": [
                        {"text": "Malign melanom vulvanın ikinci en sık görülen primer malignitesidir.", "isLie": False, "explanation": "Doğru. Skuamöz karsinomdan sonra gelir."},
                        {"text": "Tanıda S100, Melan-A ve HMB-45 pozitifliği esastır.", "isLie": False, "explanation": "Doğru. Melanositik tümör belirteçleridir."},
                        {"text": "Ekstramammary Paget hastalığından müsin negatifliği ve S100 pozitifliğiyle ayrılır.", "isLie": False, "explanation": "Doğru. Klasik ayırıcı tanı algoritmasıdır."},
                        {"text": "Vulvar melanom tamamen zararsız bir su kabarcığı olup hiçbir zaman metastaz yapmaz.", "isLie": True, "explanation": "Tuzak! Malign melanom son derece agresif, metastaz potansiyeli yüksek öldürücü bir malignitedir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvada pigmente bir lezyondan alınan biyopside pagetoid dağılım gösteren atipik hücreler saptanıyor. Bu hücrelerin Ekstramammary Paget hastalığı değil de Malign Melanom olduğunu kanıtlayan bulgu hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "S100 ve HMB-45 pozitifliği saptanması ve intraselüler müsin bulunmaması",
                            "isCorrect": True,
                            "explanation": "Melanom S100/HMB-45 pozitiftir ve müsin içermez; Paget ise müsin ve CK7 pozitiftir."
                        },
                        {
                            "key": "B",
                            "text": "Hücrelerin yalnızca saf süt salgılaması",
                            "isCorrect": False,
                            "explanation": "Melanomla ilgisi yoktur."
                        },
                        {
                            "key": "C",
                            "text": "Tümör dokusunun kemik iliğinde kan hücresi üretmesi",
                            "isCorrect": False,
                            "explanation": "Hematopoez melanom bulgusu değildir."
                        },
                        {
                            "key": "D",
                            "text": "Lezyonun sadece saç taramakla tamamen kaybolması",
                            "isCorrect": False,
                            "explanation": "Malign neoplaziler mekanik taranmayla yok olmaz."
                        }
                    ]
                }
            ]
        },
        # S62
        {
            "slideNumber": 62,
            "title": "Vulvanın Bazal Hücreli Karsinomu ve Diğer Nadir Epitelyal Tümörleri",
            "subtitle": "Lokal agresif seyir, palizatlanma ve metastaz nadirliği",
            "clinicalFocus": "Nadir Epitelyal Tümörler",
            "content": "Ders notunda belirtildiği üzere vulvar malignitelerin yaklaşık %90'ı skuamöz hücreli karsinom olup, geri kalan grubu adenokarsinomlar ve **bazal hücreli karsinom (BCC)** gibi nadir antiteler oluşturur.\n\n- **Vulvar Bazal Hücreli Karsinom:** Güneşe maruz kalmayan bir deri bölgesi olmasına rağmen vulvada BCC gelişebilir. Genellikle ileri yaştaki kadınlarda labia majorada inci benzeri kabarık kenarlı, merkezinde kraterleşmiş ülser (rodent ülser) şeklinde belirir.\n- **Histopatoloji:** Epidermisle bağlantılı bazaloid atipik hücre adaları izlenir. Adaların en dışındaki hücreler karakteristik olarak **periferik palizatlanma (parmaklık dizilimi)** gösterir ve tümör yuvaları ile stroma arasında retraksiyon artefaktı (yarıklaşma) izlenir.\n- **Prognoz:** Skuamöz karsinom ve melanomun aksine, lenfatik veya uzak metastaz riski son derece düşüktür (%1'den az). Temel riski çevre dokulara lokal destrüktif büyüme ve yetersiz cerrahi sınırlarda nükstür.\n\n> [!NOTE]\n> Vulvar bazal hücreli karsinom lokal invazyon yapabilen ancak metastaz potansiyeli neredeyse olmayan mükemmel prognozlu bir deri tümörüdür.",
            "synthesisNarrative": "Ders notunda belirtildiği üzere vulvar malignitelerin yaklaşık %90'ı skuamöz hücreli karsinom olup, geri kalan grubu adenokarsinomlar ve **bazal hücreli karsinom (BCC)** gibi nadir antiteler oluşturur.\n\n- **Vulvar Bazal Hücreli Karsinom:** Güneşe maruz kalmayan bir deri bölgesi olmasına rağmen vulvada BCC gelişebilir. Genellikle ileri yaştaki kadınlarda labia majorada inci benzeri kabarık kenarlı, merkezinde kraterleşmiş ülser (rodent ülser) şeklinde belirir.\n- **Histopatoloji:** Epidermisle bağlantılı bazaloid atipik hücre adaları izlenir. Adaların en dışındaki hücreler karakteristik olarak **periferik palizatlanma (parmaklık dizilimi)** gösterir ve tümör yuvaları ile stroma arasında retraksiyon artefaktı (yarıklaşma) izlenir.\n- **Prognoz:** Skuamöz karsinom ve melanomun aksine, lenfatik veya uzak metastaz riski son derece düşüktür (%1'den az). Temel riski çevre dokulara lokal destrüktif büyüme ve yetersiz cerrahi sınırlarda nükstür.\n\n> [!NOTE]\n> Vulvar bazal hücreli karsinom lokal invazyon yapabilen ancak metastaz potansiyeli neredeyse olmayan mükemmel prognozlu bir deri tümörüdür.",
            "bulletPoints": [
                "Vulvada BCC nadir görülür ve labia majorada ülserli nodül yapar.",
                "Histolojisinde periferik palizatlanma ve retraksiyon yarıkları tipiktir.",
                "Metastaz yapmaz, lokal eksizyon ile tam kür sağlanır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Bazal hücreli karsinom histopatolojisinde tümör adalarının en dışındaki hücrelerin yan yana dizilmesine periferik palizatlanma adı verilir.",
                    "maskedTerm": "periferik palizatlanma",
                    "hint": "Parmaklık şeklinde nükleer dizilim paterni"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulva Karsinom Tiplerinin Karşılaştırması",
                    "tableHeaders": ["Özellik", "Skuamöz Hücreli Karsinom (SCC)", "Bazal Hücreli Karsinom (BCC)"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Görülme Sıklığı", "isMasked": False},
                                {"text": "%90 (en sık vulva kanseri)", "isMasked": False},
                                {"text": "Nadir (%1 - 2)", "isMasked": True, "hint": "nadir karsinom oranı"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Metastaz Potansiyeli", "isMasked": False},
                                {"text": "İnguinal lenf nodu ve sistemik metastaz", "isMasked": False},
                                {"text": "Neredeyse hiç metastaz yapmaz (lokal agresif)", "isMasked": True, "hint": "uzak yayılımı olmayan tümör"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Vulvar BCC'de Büyüme ve Tedavi Akışı",
                    "steps": [
                        "1. Bazaloid Proliferasyon: Labia majora kıl folikülü/epidermis bazalinden yuvalar ürer.",
                        "2. Ülserleşme: Merkezde kanamalı kraterleşme (rodent ülser) ve kenarlarda inci parlaklığı oluşur.",
                        "3. Stromal Ayrışma: Kesitlerde periferik palizatlanma ve peritümöral yarıklaşma saptanır.",
                        "4. Cerrahi Eksizyon: Temiz cerrahi sınırlarla çıkarıldığında tam şifa elde edilir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulvar bazal hücreli karsinomun histopatolojisinde tümör adalarının sınırlarında görülen patognomonik nükleer dizilim şekline ne ad verilir?",
                    "answer": "Periferik palizatlanma (parmaklık tarzı hücre dizilimi)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vulvar Bazal Hücreli Karsinom",
                    "items": [
                        {"text": "Vulvar BCC güneşe maruz kalmayan labia majora derisinde de gelişebilir.", "isLie": False, "explanation": "Doğru. Nadir de olsa izlenir."},
                        {"text": "Histolojisinde periferik palizatlanma gösteren bazaloid hücre adaları izlenir.", "isLie": False, "explanation": "Doğru. Karakteristik morfolojidir."},
                        {"text": "Metastaz yapma potansiyeli son derece düşüktür.", "isLie": False, "explanation": "Doğru. Lokal agresiftir, metastaz <%1'dir."},
                        {"text": "BCC tanısı konan hastalar 24 saat içinde masif beyin metastazından kaybedilir.", "isLie": True, "explanation": "Tuzak! BCC metastaz yapmaz, lokal cerrahi ile mükemmel prognoza sahiptir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvada labia majorada krater şeklinde ülserli bir nodülden alınan biyopside periferik palizatlanma gösteren bazaloid hücre yuvaları saptanıyor. En olası tanı ve prognoz nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Bazal hücreli karsinom; metastaz riski çok düşük, cerrahi eksizyonla prognozu mükemmeldir",
                            "isCorrect": True,
                            "explanation": "Periferik palizatlanma BCC'ye özgüdür; lokal agresiftir fakat neredeyse hiç metastaz yapmaz."
                        },
                        {
                            "key": "B",
                            "text": "Akut lösemi; kemik iliğinde blast artışı ile ölümcüldür",
                            "isCorrect": False,
                            "explanation": "Hematolojik malignitedir, cilt biyopsisini açıklamaz."
                        },
                        {
                            "key": "C",
                            "text": "Kondiloma akuminatum; düşük riskli HPV siğilidir",
                            "isCorrect": False,
                            "explanation": "Kondilomda koilositoz vardır, palizatlanma görülmez."
                        },
                        {
                            "key": "D",
                            "text": "Liken skleroz; epidermis incelmesi ve dermal fibrozistir",
                            "isCorrect": False,
                            "explanation": "Non-neoplastik inflamatuvar tablodur, bazaloid yuva yapmaz."
                        }
                    ]
                }
            ]
        },
        # S63
        {
            "slideNumber": 63,
            "title": "Vajinal Adenokarsinom ve İntrauterin DES Maruziyeti: Vajinal Adenozis",
            "subtitle": "Şeffaf hücreli adenokarsinom (Clear Cell Carcinoma) ve kalıcı glandüler adalar",
            "clinicalFocus": "DES ve Berrak Hücreli Karsinom",
            "content": "Vajinanın karsinomları neredeyse tamamen skuamöz hücreli karsinom tipinde olmakla birlikte, tarihte tıbbi bir trajedi olarak kaydedilen **Dietilstilbestrol (DES)** maruziyeti nadir bir karsinom tipinin patogenezini aydınlatmıştır.\n\n- **İntrauterin DES Maruziyeti:** 1940-1970 yılları arasında düşük tehdidi nedeniyle sentetik bir östrojen olan DES kullanan annelerin kız çocuklarında ergenlik ve genç erişkinlik döneminde genital sistem anomalileri ortaya çıkmıştır.\n- **Vajinal Adenozis:** Embriyolojik gelişim sırasında vajinanın normalde yassı epitele dönüşmesi gereken yüzeyinde endoservikal/müllerian benzeri glandüler epitel adacıklarının kalmasıdır. DES maruziyeti olan kadınların %90'ında saptanır.\n- **Şeffaf Hücreli Karsinom (Clear Cell Adenocarcinoma):** Vajinal adenozis zemininde, DES kızı olarak bilinen genç kadınlarda glikojenden zengin şeffaf sitoplazmalı, kabarık nükleuslu (çivi başı / hobnail hücreleri) son derece malign **berrak hücreli adenokarsinom** gelişebilmektedir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] İntrauterin dietilstilbestrol (DES) maruziyeti, vajinada önce vajinal adenozis gelişimine, ardından nadir ve agresif şeffaf hücreli (clear cell) adenokarsinoma yol açar.",
            "synthesisNarrative": "Vajinanın karsinomları neredeyse tamamen skuamöz hücreli karsinom tipinde olmakla birlikte, tarihte tıbbi bir trajedi olarak kaydedilen **Dietilstilbestrol (DES)** maruziyeti nadir bir karsinom tipinin patogenezini aydınlatmıştır.\n\n- **İntrauterin DES Maruziyeti:** 1940-1970 yılları arasında düşük tehdidi nedeniyle sentetik bir östrojen olan DES kullanan annelerin kız çocuklarında ergenlik ve genç erişkinlik döneminde genital sistem anomalileri ortaya çıkmıştır.\n- **Vajinal Adenozis:** Embriyolojik gelişim sırasında vajinanın normalde yassı epitele dönüşmesi gereken yüzeyinde endoservikal/müllerian benzeri glandüler epitel adacıklarının kalmasıdır. DES maruziyeti olan kadınların %90'ında saptanır.\n- **Şeffaf Hücreli Karsinom (Clear Cell Adenocarcinoma):** Vajinal adenozis zemininde, DES kızı olarak bilinen genç kadınlarda glikojenden zengin şeffaf sitoplazmalı, kabarık nükleuslu (çivi başı / hobnail hücreleri) son derece malign **berrak hücreli adenokarsinom** gelişebilmektedir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] İntrauterin dietilstilbestrol (DES) maruziyeti, vajinada önce vajinal adenozis gelişimine, ardından nadir ve agresif şeffaf hücreli (clear cell) adenokarsinoma yol açar.",
            "bulletPoints": [
                "Gebelikte DES kullanımı kız çocuklarında vajinal adenozise yol açar.",
                "Vajinal adenozis zemininde berrak hücreli adenokarsinom riski artar.",
                "Histolojisinde hobnail (çivi başı) hücreleri ve berrak sitoplazma izlenir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "İntrauterin DES maruziyeti kalan kız çocuklarında vajinada görülen glandüler epitel adacıklarına vajinal adenozis adı verilir.",
                    "maskedTerm": "vajinal adenozis",
                    "hint": "Yassı epitel yerine müllerian bez adacıklarının sebat etmesi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "DES İlişkili Vajinal Patolojiler",
                    "tableHeaders": ["Evre / Tablo", "Hücresel Özellik", "Klinik / Malignite Düzeyi"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Vajinal Adenozis", "isMasked": False},
                                {"text": "Vajina mukozasında sebat eden kolumnar bezler", "isMasked": True, "hint": "müllerian glandüler artıklar"},
                                {"text": "Premalign zemin hazırlayan selim anomali"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Berrak Hücreli Ca", "isMasked": False},
                                {"text": "Glikojen dolu şeffaf sitoplazma ve hobnail hücreler", "isMasked": True, "hint": "çivi başı hücre morfolojisi"},
                                {"text": "İnvaziv ve agresif glandüler malignite"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "DES Maruziyetinden Karsinoma Patolojik Yolak",
                    "steps": [
                        "1. Fetal İlaç Maruziyeti: Anne gebelikte düşük önleyici sentetik östrojen (DES) kullanır.",
                        "2. Müllerian Gelişim Bozukluğu: Vajinal skuamöz epitelizasyon tamamlanamaz ve glandüler bezler kalır.",
                        "3. Vajinal Adenozis: Vajina duvarında kadife kırmızısı kolumnar bez adacıkları oturur.",
                        "4. Malign Transformasyon: Genç kızlık döneminde şeffaf hücreli adenokarsinom gelişir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "İntrauterin dönemde annesi DES (dietilstilbestrol) kullanan genç kadınlarda vajinada gelişme riski artan iki temel patoloji nedir?",
                    "answer": "Vajinal adenozis (kalıntı glandüler adacıklar) ve berrak hücreli (clear cell) adenokarsinomdur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "DES Maruziyeti ve Vajinal Adenozis",
                    "items": [
                        {"text": "DES maruziyeti kız çocuklarında vajinal adenozise yol açabilir.", "isLie": False, "explanation": "Doğru. Klasik teratojenik etkidir."},
                        {"text": "Vajinal adenozis zemininde berrak hücreli karsinom gelişme riski artar.", "isLie": False, "explanation": "Doğru. Hobnail hücreli tümördür."},
                        {"text": "Vajinal adenozis vajina yüzeyinde glandüler epitel adacıklarının sebat etmesidir.", "isLie": False, "explanation": "Doğru. Müllerian sebat tablosudur."},
                        {"text": "DES tamamen su buharından ibaret olup insan hücrelerinde hiçbir etki yapmaz.", "isLie": True, "explanation": "Tuzak! DES güçlü bir sentetik östrojendir ve genital anomalilere ve kansere yol açmıştır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Annesi gebelikte düşük tehdidi nedeniyle dietilstilbestrol (DES) kullanan 19 yaşında bir kadında vajina üst kısmında kanamalı kitle saptanıyor. En olası histopatolojik tanı hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Berrak hücreli (clear cell) adenokarsinom (vajinal adenozis zemininde)",
                            "isCorrect": True,
                            "explanation": "İntrauterin DES maruziyeti tipik olarak vajinal adenozis ve berrak hücreli adenokarsinoma yol açar."
                        },
                        {
                            "key": "B",
                            "text": "Safra kesesi kolesterol polipi",
                            "isCorrect": False,
                            "explanation": "Safra kesesi patolojisidir."
                        },
                        {
                            "key": "C",
                            "text": "Kemik iliğinde kronik miyeloid lösemi",
                            "isCorrect": False,
                            "explanation": "Hematolojik malignitedir."
                        },
                        {
                            "key": "D",
                            "text": "Akciğer küçük hücreli nöroendokrin karsinom",
                            "isCorrect": False,
                            "explanation": "Akciğer kanseridir, DES ile vajinada oluşmaz."
                        }
                    ]
                }
            ]
        },
        # S64
        {
            "slideNumber": 64,
            "title": "Vajinal Benign Polipoid Lezyonlar: Fibroepitelyal Polip",
            "subtitle": "Stromal hücre atipisi, selim mezenkimal lezyon ve sarkomdan ayrım",
            "clinicalFocus": "Benign Polipoid Lezyon",
            "content": "Vajina lümeninde sarkan polipoid kitleler görüldüğünde, hastanın yaşına ve histolojisine göre son derece kritik bir ayırıcı tanı yapılması zorunludur. Erişkin kadınlarda en sık benign polipoid lezyon **fibroepitelyal poliptir** (vajinal skin tag / mezodermal polip).\n\n- **Makroskopi:** Vajina duvarından lümene doğru uzanan, yumuşak, mukozayla örtülü, tek veya birkaç adet saplı polipoid kabarıklık şeklinde izlenir.\n- **Mikroskopi ve Psödo-Malign Atipi:** Polip yüzeyi çok katlı yassı epitel ile örtülüdür. Stromasında gevşek bağ dokusu ve kan damarları yer alır. En kritik tuzak: Stromada ara sıra **büyük, çok çekirdekli veya nükleer pleomorfizm gösteren atipik stromal hücreler** bulunabilir. Bu atipi reaktiftir; mitoz ve kambiyum tabakası içermez.\n- **Klinik Ayrım:** Erişkinlerde görülen fibroepitelyal polipler selimdir; pediatrik yaştaki sarkoma botryoides lezyonları ile asla karıştırılmamalıdır.\n\n> [!NOTE]\n> Fibroepitelyal polipteki nükleer atipi dejeneratif/reaktiftir; malign sarkomlardaki gibi infiltrasyon, atipik mitoz veya malign rabdomiyoblastlar kesinlikle izlenmez.",
            "synthesisNarrative": "Vajina lümeninde sarkan polipoid kitleler görüldüğünde, hastanın yaşına ve histolojisine göre son derece kritik bir ayırıcı tanı yapılması zorunludur. Erişkin kadınlarda en sık benign polipoid lezyon **fibroepitelyal poliptir** (vajinal skin tag / mezodermal polip).\n\n- **Makroskopi:** Vajina duvarından lümene doğru uzanan, yumuşak, mukozayla örtülü, tek veya birkaç adet saplı polipoid kabarıklık şeklinde izlenir.\n- **Mikroskopi ve Psödo-Malign Atipi:** Polip yüzeyi çok katlı yassı epitel ile örtülüdür. Stromasında gevşek bağ dokusu ve kan damarları yer alır. En kritik tuzak: Stromada ara sıra **büyük, çok çekirdekli veya nükleer pleomorfizm gösteren atipik stromal hücreler** bulunabilir. Bu atipi reaktiftir; mitoz ve kambiyum tabakası içermez.\n- **Klinik Ayrım:** Erişkinlerde görülen fibroepitelyal polipler selimdir; pediatrik yaştaki sarkoma botryoides lezyonları ile asla karıştırılmamalıdır.\n\n> [!NOTE]\n> Fibroepitelyal polipteki nükleer atipi dejeneratif/reaktiftir; malign sarkomlardaki gibi infiltrasyon, atipik mitoz veya malign rabdomiyoblastlar kesinlikle izlenmez.",
            "bulletPoints": [
                "Erişkinlerde vajinanın en sık benign polipoid lezyonudur.",
                "Stromasında psödomalign dejeneratif nükleer atipi izlenebilir.",
                "Malign sarkomlardan infiltrasyon ve mitoz yokluğuyla ayrılır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Erişkin kadın vajinasında izlenen ve bazen dejeneratif atipik hücreler içeren selim kitleye fibroepitelyal polip adı verilir.",
                    "maskedTerm": "fibroepitelyal polip",
                    "hint": "Vajinanın mezenkimal kaynaklı en sık selim polipi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vajinada Polipoid Kitle Ayırıcı Tanısı",
                    "tableHeaders": ["Özellik", "Fibroepitelyal Polip", "Sarkoma Botryoides"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Tipik Yaş Grubu", "isMasked": False},
                                {"text": "Erişkin ve üreme çağındaki kadınlar", "isMasked": False},
                                {"text": "Bebekler ve 5 yaş altı çocuklar", "isMasked": True, "hint": "pediatrik yaş grubu"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Histopatolojik Karakter", "isMasked": False},
                                {"text": "Selim stroma, mitoz yok, psödoatipi", "isMasked": True, "hint": "malign olmayan dejeneratif tablo"},
                                {"text": "Kambiyum tabakası, desmin/miyogenin (+)"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Fibroepitelyal Polipin Tanı Güvenliği",
                    "steps": [
                        "1. Kitle Tespiti: Erişkin kadında vajinadan sarkan yumuşak, mukozal polip görülür.",
                        "2. Polipektomi: Kitle tabanından basit eksizyonla çıkarılır.",
                        "3. Mikroskopi Tuzağı: Stromada rastlanan pleomorfik nükleuslu büyük hücreler patoloğu uyarır.",
                        "4. Sarkomun Dışlanması: Kambiyum tabakası, rabdomiyoblast ve mitoz olmamasıyla selim tanı kesinleşir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Erişkin vajinasındaki fibroepitelyal polipin patoloğu yanıltabilecek en önemli histopatolojik tuzağı nedir ve sarkomdan nasıl ayırt edilir?",
                    "answer": "Stromada pleomorfik nükleer psödoatipi bulunabilmesidir; atipik mitozların bulunmaması ve subepitelyal yoğunlaşma (kambiyum tabakası) olmamasıyla sarkomdan ayrılır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajinal Fibroepitelyal Polip",
                    "items": [
                        {"text": "Fibroepitelyal polip erişkin vajinasında sık görülen selim bir lezyondur.", "isLie": False, "explanation": "Doğru. Benign polipoid tablodur."},
                        {"text": "Stromasında dejeneratif kaynaklı nükleer psödoatipi görülebilir.", "isLie": False, "explanation": "Doğru. Sarkomu taklit edebilir."},
                        {"text": "Mitoz içermez ve kambiyum tabakası yapmaz.", "isLie": False, "explanation": "Doğru. Malign sarkomdan bu bulgularla ayrılır."},
                        {"text": "Fibroepitelyal polip daima beyin sapından kaynaklanan bir gliomdur.", "isLie": True, "explanation": "Tuzak! Fibroepitelyal polip vajina mukozasından gelişen selim bir mezenkimal poliptir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "38 yaşında bir kadında vajinadan sarkan polipoid kitleden yapılan eksizyonda skuamöz epitel altında ödemli stroma ve seyrek pleomorfik nükleuslu atipik hücreler saptanıyor. Mitoz ve infiltrasyon izlenmiyor. En olası tanı nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Fibroepitelyal polip (reaktif / dejeneratif psödoatipi ile)",
                            "isCorrect": True,
                            "explanation": "Erişkin kadında mitozsuz, selim polipoid doku fibroepitelyal poliptir; atipik hücreler psödoatipidir."
                        },
                        {
                            "key": "B",
                            "text": "Yüksek dereceli rabdomiyosarkom",
                            "isCorrect": False,
                            "explanation": "Sarkom pediatrik gruptadır, bol mitoz ve kambiyum tabakası içerir."
                        },
                        {
                            "key": "C",
                            "text": "Akut miyokard infarktüsü",
                            "isCorrect": False,
                            "explanation": "Kalp kası iskemisidir."
                        },
                        {
                            "key": "D",
                            "text": "Karaciğer kist hidatiği",
                            "isCorrect": False,
                            "explanation": "Ekinokok parazit kistidir."
                        }
                    ]
                }
            ]
        },
        # S65
        {
            "slideNumber": 65,
            "title": "Embriyonel Rabdomiyosarkom Ayırıcı Tanısı: Sarkoma Botryoides",
            "subtitle": "Kambiyum tabakası, çizgili kas çizgilenmesi ve immün belirteçler (Desmin/Miyogenin)",
            "clinicalFocus": "Pediatrik Malign Tümör",
            "content": "Ders notunda belirtildiği üzere **Embriyonel rabdomiyosarkom (Sarkoma Botryoides)**, 5 yaşından küçük kız bebek ve çocuklarda vajinadan sarkan, üzüm salkımı benzeri kitlelerle karakterize son derece habis bir mezenkimal tümördür.\n\n- **Histopatolojik Ayrım Kriteri (Kambiyum Tabakası):** Tümör yüzeyindeki vajina epitelinin hemen altında hücrelerin aşırı yoğunlaştığı hiperselüler bir kuşak izlenir; bu yapıya **kambiyum tabakası (cambium layer)** adı verilir. Polipin derin kısımları ise hiposelüler ve miksoiddir.\n- **Sitomorfoloji:** Küçük, iğsi ve yuvarlak hücreler arasında patognomonik **strap hücreleri (kayış hücreleri)** ve sitoplazmasında çizgili kas diferansiasyonu (enine çizgilenme) gösteren rabdomiyoblastlar izlenir.\n- **İmmünohistokimya:** Tanı mezenkimal ve miyojenik belirteçlerle doğrulanır: **Desmin, Miyogenin (MyoD1) ve Aktin** güçlü pozitiflik verir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Sarkoma Botryoides'in histopatolojik tanısında subepitelyal kambiyum tabakası, rabdomiyoblastlar ve Desmin/Miyogenin immün pozitifliği patognomoniktir.",
            "synthesisNarrative": "Ders notunda belirtildiği üzere **Embriyonel rabdomiyosarkom (Sarkoma Botryoides)**, 5 yaşından küçük kız bebek ve çocuklarda vajinadan sarkan, üzüm salkımı benzeri kitlelerle karakterize son derece habis bir mezenkimal tümördür.\n\n- **Histopatolojik Ayrım Kriteri (Kambiyum Tabakası):** Tümör yüzeyindeki vajina epitelinin hemen altında hücrelerin aşırı yoğunlaştığı hiperselüler bir kuşak izlenir; bu yapıya **kambiyum tabakası (cambium layer)** adı verilir. Polipin derin kısımları ise hiposelüler ve miksoiddir.\n- **Sitomorfoloji:** Küçük, iğsi ve yuvarlak hücreler arasında patognomonik **strap hücreleri (kayış hücreleri)** ve sitoplazmasında çizgili kas diferansiasyonu (enine çizgilenme) gösteren rabdomiyoblastlar izlenir.\n- **İmmünohistokimya:** Tanı mezenkimal ve miyojenik belirteçlerle doğrulanır: **Desmin, Miyogenin (MyoD1) ve Aktin** güçlü pozitiflik verir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Sarkoma Botryoides'in histopatolojik tanısında subepitelyal kambiyum tabakası, rabdomiyoblastlar ve Desmin/Miyogenin immün pozitifliği patognomoniktir.",
            "bulletPoints": [
                "Sarkoma botryoides <5 yaş çocuklarda üzüm salkımı kitle yapar.",
                "Epitel altında hiperselüler kambiyum tabakası patognomoniktir.",
                "Desmin ve Miyogenin (MyoD1) immün belirteçleri pozitiftir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Sarkoma botryoides histopatolojisinde vajinal epitelin hemen altında tümör hücrelerinin yoğunlaştığı kuşağa kambiyum tabakası adı verilir.",
                    "maskedTerm": "kambiyum tabakası",
                    "hint": "Subepitelyal yoğun hücresel infiltrasyon kuşağı"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Sarkoma Botryoides İmmünohistokimyasal Profili",
                    "tableHeaders": ["Belirteç", "Hücresel Hedef", "Sonuç ve Yorum"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Desmin", "isMasked": False},
                                {"text": "İntermediate filaman (kas spesifik)", "isMasked": True, "hint": "kas diferansiasyon filamenti"},
                                {"text": "Pozitif (+), mezenkimal kas kökeni kanıtlar"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Miyogenin (MyoD1)", "isMasked": False},
                                {"text": "Çizgili kas transkripsiyon faktörü", "isMasked": True, "hint": "rabdomiyoblast nükleer proteini"},
                                {"text": "Pozitif (+), rabdomiyosarkom için en özgül kanıt"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Pediatrik Sarkomda Tanı Doğrulama Akışı",
                    "steps": [
                        "1. Klinik Başvuru: 2 yaşındaki kız çocuğunda vajinadan sarkan şeffaf polipoid kitle görülür.",
                        "2. Biyopsi: Kitle yüzeyinde sağlam skuamöz epitel altında yoğun hücreler (kambiyum kuşağı) izlenir.",
                        "3. Rabdomiyoblast Arayışı: Sitoplazmasında eozinofilik çizgilenme olan strap hücreleri saptanır.",
                        "4. İmmün Boyama: Miyogenin ve Desmin nükleer/sitoplazmik pozitifliğiyle sarkom teşhis edilir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Sarkoma Botryoides tanısını kesinleştiren en özgül iki kas belirteci ve epitel altındaki tipik hücresel kuşak nedir?",
                    "answer": "Desmin ve Miyogenin (MyoD1) belirteçleri pozitiftir; epitel altındaki yoğunlaşma kuşağına kambiyum tabakası (cambium layer) denir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Sarkoma Botryoides Histolojisi",
                    "items": [
                        {"text": "Sarkoma Botryoides 5 yaşından küçük çocukların malign tümörüdür.", "isLie": False, "explanation": "Doğru. Pediatrik grupta görülür."},
                        {"text": "Histolojisinde subepitelyal kambiyum tabakası karakteristik bir bulgudur.", "isLie": False, "explanation": "Doğru. Tanısal katmandır."},
                        {"text": "Desmin ve Miyogenin pozitifliği çizgili kas kökenini kanıtlar.", "isLie": False, "explanation": "Doğru. Spesifik miyojenik belirteçlerdir."},
                        {"text": "Sarkoma Botryoides tamamen selim bir yağ bezesi olup ameliyat dahi gerektirmez.", "isLie": True, "explanation": "Tuzak! Sarkoma Botryoides agresif, kemoterapi ve cerrahi gerektiren malign bir yumuşak doku sarkomudur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "2 yaşındaki bir kız çocuğunda vajinadan sarkan üzüm salkımı benzeri kitleden alınan biyopside skuamöz epitel altında yoğun kambiyum tabakası ve Desmin pozitifliği saptanıyor. En olası tanı nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Embriyonel rabdomiyosarkom (Sarkoma Botryoides)",
                            "isCorrect": True,
                            "explanation": "Kambiyum tabakası, pediatrik yaş ve Desmin/Miyogenin pozitifliği sarkoma botryoides'i kesinleştirir."
                        },
                        {
                            "key": "B",
                            "text": "Postmenopozal atrofik vajinit",
                            "isCorrect": False,
                            "explanation": "Yaşlı kadınlarda görülen hormon eksikliği tablosudur."
                        },
                        {
                            "key": "C",
                            "text": "Bartholin bezi kisti",
                            "isCorrect": False,
                            "explanation": "Vulva posterolateralinde yetişkin kistidir."
                        },
                        {
                            "key": "D",
                            "text": "Malign melanom",
                            "isCorrect": False,
                            "explanation": "Melanositik tümördür, kambiyum tabakası ve Desmin yapmaz."
                        }
                    ]
                }
            ]
        },
        # S66
        {
            "slideNumber": 66,
            "title": "Pediatrik Vajinal Kanamalara Patolojik Yaklaşım ve Ayırıcı Tanı",
            "subtitle": "Yabancı cisim, sarkoma botryoides, travma ve cinsel istismar bulguları",
            "clinicalFocus": "Klinik Patolojik Algoritma",
            "content": "Pediatrik yaş grubunda (özellikle prepubertal dönemde) vajinal kanama veya akıntı varlığı, hekim için acil ve multidisipliner bir patolojik araştırma gerektiren alarm bulgusudur.\n\n- **En Sık Benign Nedenler:** Küçük çocuklarda vajinal kanamanın en sık nedeni vajinaya yerleştirilen **yabancı cisimler** (tuvalet kağıdı, küçük oyuncaklar vb.) ve buna sekonder gelişen ülseratif süpüratif vajinittir. İkinci sık neden non-spesifik prepubertal vulvovajinittir.\n- **En Korkulan Malignite:** Aniden ortaya çıkan kanamalı polipoid doku sarkması durumunda derhal **sarkoma botryoides** ekarte edilmelidir. Erken dönemde basit bir vajinit veya yabancı cisim reaksiyonu sanılması ölümcül gecikmelere yol açabilir.\n- **Travma ve İstismar:** Laserasyonlar, hematomlar, hymen yırtıkları adli ve klinik patoloji açısından titizlikle dokümante edilmelidir.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Prepubertal bir çocukta vajinal kanama veya vajinadan dışarı sarkan et parçası görüldüğünde aksi kanıtlanana kadar sarkoma botryoides ve yabancı cisim düşünülerek genel anestezi altında vajinoskopi yapılmalıdır.",
            "synthesisNarrative": "Pediatrik yaş grubunda (özellikle prepubertal dönemde) vajinal kanama veya akıntı varlığı, hekim için acil ve multidisipliner bir patolojik araştırma gerektiren alarm bulgusudur.\n\n- **En Sık Benign Nedenler:** Küçük çocuklarda vajinal kanamanın en sık nedeni vajinaya yerleştirilen **yabancı cisimler** (tuvalet kağıdı, küçük oyuncaklar vb.) ve buna sekonder gelişen ülseratif süpüratif vajinittir. İkinci sık neden non-spesifik prepubertal vulvovajinittir.\n- **En Korkulan Malignite:** Aniden ortaya çıkan kanamalı polipoid doku sarkması durumunda derhal **sarkoma botryoides** ekarte edilmelidir. Erken dönemde basit bir vajinit veya yabancı cisim reaksiyonu sanılması ölümcül gecikmelere yol açabilir.\n- **Travma ve İstismar:** Laserasyonlar, hematomlar, hymen yırtıkları adli ve klinik patoloji açısından titizlikle dokümante edilmelidir.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Prepubertal bir çocukta vajinal kanama veya vajinadan dışarı sarkan et parçası görüldüğünde aksi kanıtlanana kadar sarkoma botryoides ve yabancı cisim düşünülerek genel anestezi altında vajinoskopi yapılmalıdır.",
            "bulletPoints": [
                "Pediatrik vajinal kanamada en sık benign neden yabancı cisimdir.",
                "En önemli malign etken sarkoma botryoides'tir ve acil araştırılmalıdır.",
                "Travma ve istismar bulguları patolojik olarak belgelenmelidir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Küçük kız çocuklarında vajinal kanamanın en sık selim nedeni vajina içine kaçan yabancı cisim varlığıdır.",
                    "maskedTerm": "yabancı cisim",
                    "hint": "Tuvalet kağıdı veya küçük parçaların vajinada yaptığı tahriş"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Pediatrik Vajinal Kanama Ayırıcı Tanı Kriterleri",
                    "tableHeaders": ["Etyoloji", "Tipik Morfoloji / Bulgu", "Yaklaşım"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Yabancı Cisim", "isMasked": False},
                                {"text": "Kokulu pürülan akıntı, yüzeyel erezyon", "isMasked": True, "hint": "iltihaplı vajinit ve tahriş"},
                                {"text": "Genel anestezi altında vajinoskopi ve çıkarma"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Sarkoma Botryoides", "isMasked": False},
                                {"text": "Vajinadan sarkan üzüm salkımı polipoid kitle", "isMasked": True, "hint": "botriyoid yumuşak doku tümörü"},
                                {"text": "Acil biyopsi, evreleme ve kemoterapi"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Pediatrik Kanamada Teşhis Basamakları",
                    "steps": [
                        "1. Alarm Bulgusu: 3 yaşındaki çocukta iç çamaşırında taze kan lekesi fark edilir.",
                        "2. Vajinoskopik Muayene: Çocuk uyutularak vajinal lümen endoskopik olarak görüntülenir.",
                        "3. Kitle veya Cisim: Lümeni dolduran üzüm tanesi benzeri polipoid lezyon saptanır.",
                        "4. Biyopsi: Alınan örnekte kambiyum tabakası ve rabdomiyoblastlar doğrulanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Prepubertal bir çocukta vajinal kanama ve polipoid doku sarkması izlendiğinde ekarte edilmesi gereken en ölümcül malign tümör nedir?",
                    "answer": "Embriyonel rabdomiyosarkom (Sarkoma Botryoides)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Pediatrik Vajinal Kanama",
                    "items": [
                        {"text": "Pediatrik vajinal kanamalarda yabancı cisim en sık benign nedendir.", "isLie": False, "explanation": "Doğru. Klinik pratikte en yaygın tablodur."},
                        {"text": "Vajinadan sarkan polipoid kitlelerde sarkoma botryoides hızla ekarte edilmelidir.", "isLie": False, "explanation": "Doğru. Hayati öneme sahip malignitedir."},
                        {"text": "Tanısal değerlendirme sıklıkla anestezi altında vajinoskopi gerektirir.", "isLie": False, "explanation": "Doğru. Çocuklarda travmayı önlemek için uygulanır."},
                        {"text": "2 yaşındaki kız çocuğunda vajinal kanama normal fizyolojik menstrüasyondur.", "isLie": True, "explanation": "Tuzak! 2 yaşındaki bebekte menstrüasyon olamaz; vajinal kanama daima patolojiktir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "3 yaşındaki bir kız çocuğunda vajinal kanama şikayeti ile başvuruda ayırıcı tanıda en sık görülen benign neden ile en kritik primer malign tümör hangi seçenekte doğru verilmiştir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Benign: Vajinal yabancı cisim; Malign: Sarkoma Botryoides (embriyonel rabdomiyosarkom)",
                            "isCorrect": True,
                            "explanation": "En sık selim neden yabancı cisim tahrişi; en kritik malignite ise sarkoma botryoides'tir."
                        },
                        {
                            "key": "B",
                            "text": "Benign: Safra kesesi taşı; Malign: Karaciğer hepatosellüler karsinom",
                            "isCorrect": False,
                            "explanation": "Karaciğer ve safra yolları patolojileridir."
                        },
                        {
                            "key": "C",
                            "text": "Benign: Diş çürüğü; Malign: Akciğer yassı hücreli kanseri",
                            "isCorrect": False,
                            "explanation": "Ağız ve göğüs hastalıklarıdır."
                        },
                        {
                            "key": "D",
                            "text": "Benign: Menopozal osteoporoz; Malign: Tiroid anaplastik kanseri",
                            "isCorrect": False,
                            "explanation": "Pediatrik jinekolojik patoloji ile ilgisi yoktur."
                        }
                    ]
                }
            ]
        },
        # S67
        {
            "slideNumber": 67,
            "title": "Vulvovajinal Travma ve Hematomlar: Vasküler Anatomi",
            "subtitle": "Pudendal arter dalları, labial hematom ve retroperitoneal yayılım riski",
            "clinicalFocus": "Travma ve Vasküler Aciller",
            "content": "Vulva ve vajina, zengin venöz pleksusları ve arteriyel dalları nedeniyle künt veya penetran travmalara karşı son derece duyarlıdır. Obstetrik travmalar veya kaza sonucu gelişen **vulvar hematomlar** hızla büyüyebilir.\n\n- **Vasküler Kaynak:** Temel kanama kaynağı **internal pudendal arterin dalları** (perineal arter, labial arterler ve klitoris arteri) ile genişlemiş labial venöz ağlardır.\n- **Anatomik Kompartmanlar:** Kanama perineal fasyanın (Colles fasyası) sınırlandırdığı yüzeyel perineal aralıkta kaldığında devasa, ağrılı, mavi-mor renkli bir **labial hematom** oluşturur. Fasyayı aşan derin kanamalar ise iskiyorektal fossaya ve retroperitona doğru sessizce yayılarak hastayı hipovolemik şoka sokabilir.\n- **Histopatoloji ve Onarım:** Dokuda masif eritrosit ekstravazasyonu, fibrin birikimi ve takip eden evrede hemosiderin yüklü makrofajlar ve granülasyon dokusu izlenir.\n\n> [!NOTE]\n> Hızla genişleyen vulvar hematomlarda kanama kontrol altına alınmazsa pelvik tabana ve retroperitona litrelerce gizli kan toplanabilir.",
            "synthesisNarrative": "Vulva ve vajina, zengin venöz pleksusları ve arteriyel dalları nedeniyle künt veya penetran travmalara karşı son derece duyarlıdır. Obstetrik travmalar veya kaza sonucu gelişen **vulvar hematomlar** hızla büyüyebilir.\n\n- **Vasküler Kaynak:** Temel kanama kaynağı **internal pudendal arterin dalları** (perineal arter, labial arterler ve klitoris arteri) ile genişlemiş labial venöz ağlardır.\n- **Anatomik Kompartmanlar:** Kanama perineal fasyanın (Colles fasyası) sınırlandırdığı yüzeyel perineal aralıkta kaldığında devasa, ağrılı, mavi-mor renkli bir **labial hematom** oluşturur. Fasyayı aşan derin kanamalar ise iskiyorektal fossaya ve retroperitona doğru sessizce yayılarak hastayı hipovolemik şoka sokabilir.\n- **Histopatoloji ve Onarım:** Dokuda masif eritrosit ekstravazasyonu, fibrin birikimi ve takip eden evrede hemosiderin yüklü makrofajlar ve granülasyon dokusu izlenir.\n\n> [!NOTE]\n> Hızla genişleyen vulvar hematomlarda kanama kontrol altına alınmazsa pelvik tabana ve retroperitona litrelerce gizli kan toplanabilir.",
            "bulletPoints": [
                "Vulva zengin damar ağı nedeniyle travmada masif hematom yapabilir.",
                "Kanama kaynağı internal pudendal arter dalları ve venöz pleksuslardır.",
                "Derin hematomlar retroperitona yayılarak gizli kan kaybına yol açar."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vulvar travmalarda labiumlarda hızla büyüyen kan birikimine vulvar hematom adı verilir.",
                    "maskedTerm": "vulvar hematom",
                    "hint": "Damar yırtılmasıyla doku içinde oluşan kitle benzeri kan göllenmesi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulvar Hematomun Klinik Özellikleri",
                    "tableHeaders": ["Anatomik Aralık", "Klinik Görünüm", "Hayati Risk"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Yüzeyel Perineal Aralık", "isMasked": False},
                                {"text": "Labiumda mor-siyah, aşırı gergin ve ağrılı kitle", "isMasked": True, "hint": "dışarıdan görülebilen labial şişlik"},
                                {"text": "Şiddetli lokal ağrı ve idrar retansiyonu"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "İskiyorektal Fossa / Derin", "isMasked": False},
                                {"text": "Pelvik taban ve retroperitona gizli kanama", "isMasked": True, "hint": "derin fasyal yayılım"},
                                {"text": "Belirgin şişlik olmadan hipovolemik şok"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Doğum Travmasından Hematoma Patogenez",
                    "steps": [
                        "1. Mekanik Travma: Doğum veya künt yaralanma labial damarları zedeler.",
                        "2. Damar Yırtılması: Pudendal arter dallarından doku aralıklarına kontrolsüz kan sızar.",
                        "3. Hematom Genişlemesi: Basınç yükselerek labiumu gerer ve mavi-mor hematom oluşturur.",
                        "4. Cerrahi Boşaltma: Hematom açılarak pıhtılar temizlenir ve kanayan damar bağlanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulvar hematomlarda kanamaya en sık kaynaklık eden arteriyel damar ağı hangisidir?",
                    "answer": "İnternal pudendal arterin dalları (perineal ve labial arterler)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vulvar Travma ve Hematomlar",
                    "items": [
                        {"text": "Vulva zengin damarlanması nedeniyle travmalarda büyük hematomlar geliştirebilir.", "isLie": False, "explanation": "Doğru. Pudendal dallar zengindir."},
                        {"text": "Derin fasyal yırtıklarda hematom retroperitona kadar ilerleyebilir.", "isLie": False, "explanation": "Doğru. Gizli masif kanama yapabilir."},
                        {"text": "Klinikte aşırı ağrılı, gergin, mor-siyah kitleler şeklinde belirir.", "isLie": False, "explanation": "Doğru. Tipik hematom görüntüsüdür."},
                        {"text": "Vulvar hematomlar doğrudan virüslerin mitoz bölünmesiyle çoğalan kanserlerdir.", "isLie": True, "explanation": "Tuzak! Hematom neoplazi değil, yırtılan damardan sızan pıhtılaşmış kandır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Doğum sonrasında labium majus bölgesinde hızla büyüyen, aşırı ağrılı ve mor-siyah renkli fluktuasyon veren kitle saptanan hastada en olası tanı nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Vulvar hematom (pudendal damar hasarına bağlı doku içi kan birikimi)",
                            "isCorrect": True,
                            "explanation": "Doğum travması sonrası hızla gelişen mor-siyah ağrılı kitle tipik vulvar hematomdur."
                        },
                        {
                            "key": "B",
                            "text": "Malign lenfoma",
                            "isCorrect": False,
                            "explanation": "Dakikalar içinde doğum travmasıyla akut hematom gibi ortaya çıkmaz."
                        },
                        {
                            "key": "C",
                            "text": "Böbrek taşı dökülmesi",
                            "isCorrect": False,
                            "explanation": "Üriner sistem patolojisidir, labial kitle yapmaz."
                        },
                        {
                            "key": "D",
                            "text": "Liken skleroz",
                            "isCorrect": False,
                            "explanation": "Kronik porselen beyazı atrofik dermatozdur, akut hematom değildir."
                        }
                    ]
                }
            ]
        },
        # S68
        {
            "slideNumber": 68,
            "title": "Postmenopozal Atrofik Vajinit Histopatolojisi ve Sitomorfolojisi",
            "subtitle": "Östrojen eksikliği, parabazal hücre hakimiyeti ve glikojen kaybı",
            "clinicalFocus": "Hormon Eksikliği ve Atrofi",
            "content": "Menopoz sonrası dönemde dolaşımdaki **östrojen düzeyinin dramatik düşmesi**, vajina ve serviks mukozasında derin histopatolojik değişikliklere yol açarak **atrofik vajinit** tablosunu ortaya çıkarır.\n\n- **Histopatoloji:** Normalde çok katlı, kalın ve glikojenden zengin olan skuamöz epitel belirgin biçimde incelir; yalnızca birkaç sıra hücre kalınlığına iner. Rete çıkıntıları silinir ve epitel altındaki stroma hyalinize olur.\n- **Sitolojik Matürasyon İndeksi:** Pap smear yaymasında normal üreme çağında görülen yüzeyel ve ara hücrelerin yerini, olgunlaşamamış **parabazal hücreler** alır. Parabazal hücre hakimiyeti atrofinin en net sitolojik kanıtıdır.\n- **Mikroçevre ve Enfeksiyon:** Glikojen yokluğunda laktobasiller yaşayamaz; vajinal pH 4.5'in üzerine fırlar. Koruyucu bariyer çöktüğünden mukozada peteşiyel kanamalar, yanma, disparoni (ağrılı ilişki) ve reaktif inflamasyon görülür.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Postmenopozal atrofik vajinitte smear sitolojisinde parabazal hücre hakimiyeti görülür; epitel incelmiştir ve glikojen eksikliğine bağlı laktobasiller kaybolarak pH alkaliye kayar.",
            "synthesisNarrative": "Menopoz sonrası dönemde dolaşımdaki **östrojen düzeyinin dramatik düşmesi**, vajina ve serviks mukozasında derin histopatolojik değişikliklere yol açarak **atrofik vajinit** tablosunu ortaya çıkarır.\n\n- **Histopatoloji:** Normalde çok katlı, kalın ve glikojenden zengin olan skuamöz epitel belirgin biçimde incelir; yalnızca birkaç sıra hücre kalınlığına iner. Rete çıkıntıları silinir ve epitel altındaki stroma hyalinize olur.\n- **Sitolojik Matürasyon İndeksi:** Pap smear yaymasında normal üreme çağında görülen yüzeyel ve ara hücrelerin yerini, olgunlaşamamış **parabazal hücreler** alır. Parabazal hücre hakimiyeti atrofinin en net sitolojik kanıtıdır.\n- **Mikroçevre ve Enfeksiyon:** Glikojen yokluğunda laktobasiller yaşayamaz; vajinal pH 4.5'in üzerine fırlar. Koruyucu bariyer çöktüğünden mukozada peteşiyel kanamalar, yanma, disparoni (ağrılı ilişki) ve reaktif inflamasyon görülür.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Postmenopozal atrofik vajinitte smear sitolojisinde parabazal hücre hakimiyeti görülür; epitel incelmiştir ve glikojen eksikliğine bağlı laktobasiller kaybolarak pH alkaliye kayar.",
            "bulletPoints": [
                "Östrojen eksikliği vajina skuamöz epitelinde belirgin incelmeye yol açar.",
                "Sitolojik yaymada parabazal hücre hakimiyeti izlenir.",
                "Glikojen kaybı nedeniyle laktobasiller azalır ve pH yükselir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Atrofik vajinit sitolojisinde östrojen eksikliğine bağlı olarak yaymada parabazal hücreler hakimiyeti görülür.",
                    "maskedTerm": "parabazal hücreler",
                    "hint": "Olgunlaşamamış, yuvarlak nükleuslu küçük epitel hücreleri"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Normal Reprodüktif Vajina vs Atrofik Vajina",
                    "tableHeaders": ["Özellik", "Reprodüktif Çağ (Östrojen Etkisi)", "Postmenopozal Atrofi"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Epitel Kalınlığı", "isMasked": False},
                                {"text": "Çok katlı, kalın, glikojenden zengin", "isMasked": False},
                                {"text": "Birkaç hücre sırasına inmiş ince epitel", "isMasked": True, "hint": "belirgin atrofik incelme"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Sitolojik Hakimiyet", "isMasked": False},
                                {"text": "Süperfisiyel ve intermediyer hücreler", "isMasked": False},
                                {"text": "Parabazal hücre hakimiyeti", "isMasked": True, "hint": "matürasyon kaybı göstergesi"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Östrojen Düşüşünden Atrofik Vajinite",
                    "steps": [
                        "1. Menopoz: Overlerde follikül tükenmesiyle sistemik östrojen seviyesi çöker.",
                        "2. Epitel İncilmesi: Vajina hücrelerinde proliferasyon ve glikojen sentezi durur.",
                        "3. Flora Bozulması: Laktobasiller besinsiz kalarak yok olur ve pH 6-7 düzeyine çıkar.",
                        "4. Atrofik Vajinit: Mukozal incelme nedeniyle peteşi, kuruluk ve parabazal hücreli akıntı başlar."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Postmenopozal atrofik vajinit tablosunda Pap smear yaymasında hangi hücre grubunun baskın hale gelmesi atrofinin en tipik sitolojik bulgusudur?",
                    "answer": "Parabazal hücrelerin hakimiyeti; epitel olgunlaşamadığı için yüzeyel hücrelerin yerini parabazal hücreler alır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Postmenopozal Atrofik Vajinit",
                    "items": [
                        {"text": "Atrofik vajinit temel olarak östrojen eksikliği sonucu gelişir.", "isLie": False, "explanation": "Doğru. Menopozal hormonal tablodur."},
                        {"text": "Smear sitolojisinde parabazal hücre hakimiyeti izlenir.", "isLie": False, "explanation": "Doğru. Atrofinin sitolojik kanıtıdır."},
                        {"text": "Glikojen kaybına bağlı olarak laktobasiller azalır ve pH bazikleşir.", "isLie": False, "explanation": "Doğru. Koruyucu bariyer bozulur."},
                        {"text": "Atrofik vajinitte skuamöz epitel 100 kat kalınlaşarak taş sertliğine ulaşır.", "isLie": True, "explanation": "Tuzak! Atrofide epitel kalınlaşmaz, tam tersine aşırı incelir ve kırılganlaşır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Menopozdaki bir kadında yapılan servikovajinal sitoloji yaymasında parabazal hücre hakimiyeti, glikojen eksikliği ve epitelde belirgin incelme saptanıyor. En olası klinik patolojik tanı nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Postmenopozal atrofik vajinit (östrojen eksikliğine bağlı mukozal atrofi)",
                            "isCorrect": True,
                            "explanation": "Östrojen eksikliği parabazal hücre hakimiyeti, glikojen kaybı ve mukozal atrofiye yol açar."
                        },
                        {
                            "key": "B",
                            "text": "Akut bakteriyel menenjit",
                            "isCorrect": False,
                            "explanation": "Santral sinir sistemi enfeksiyonudur."
                        },
                        {
                            "key": "C",
                            "text": "Yüksek dereceli rabdomiyosarkom",
                            "isCorrect": False,
                            "explanation": "Pediatrik malign tümördür."
                        },
                        {
                            "key": "D",
                            "text": "Hiperplastik skuamöz distrofi",
                            "isCorrect": False,
                            "explanation": "Hiperplastik tabloda epitel kalınlaşır (akantoz), atrofide ise incelir."
                        }
                    ]
                }
            ]
        },
        # S69
        {
            "slideNumber": 69,
            "title": "Atrofik Değişikliklerin Displaziden (HSIL) Ayrımı",
            "subtitle": "Kromatin düzeni, nükleer büyüme artefaktı ve östrojen testinin tanıdaki yeri",
            "clinicalFocus": "Sitolojik Ayırıcı Tanı",
            "content": "Postmenopozal kadınların servikovajinal sitolojilerinde en sık yapılan tanısal hata, atrofik epitel hücrelerindeki **psödo-displastik nükleer değişikliklerin yanlışlıkla HSIL (ağır displazi)** olarak yorumlanmasıdır.\n\n- **Nükleer Büyüme ve Artmış N/S Oranı:** Parabazal hücrelerin sitoplazması dar olduğundan nükleus/sitoplazma (N/S) oranı fizyolojik olarak yüksektir. Kuruma veya inflamasyon artefaktıyla nükleus hafifçe büyüyebilir.\n- **Kromatin Yapısı (Anahtar Kriter):** Gerçek displazide (HSIL) nükleer membran düzensiz, girintili çıkıntılı ve kromatin kaba topaklı (hiperkromatik) iken; atrofik hücrelerde **nükleer kontur tamamen pürüzsüz, yuvarlak ve kromatin homojen-düzgündür**.\n- **Östrojen Testi:** Şüpheli kalan olgularda hastaya 1-2 hafta lokal östrojen krem tedavisi verilir. Hormon etkisiyle atrofik hücreler hızla olgunlaşarak süperfisiyel hücrelere döner ve sitoloji normale döner; gerçek bir HSIL lezyonu ise östrojenle kaybolmaz.\n\n> [!NOTE]\n> [KLİNİK İPUCU] Atrofi ile HSIL arasında kalınan şüpheli postmenopozal yaymalarda lokal östrojen tedavisi sonrası smear tekrarı en güvenilir tanısal çözümdür.",
            "synthesisNarrative": "Postmenopozal kadınların servikovajinal sitolojilerinde en sık yapılan tanısal hata, atrofik epitel hücrelerindeki **psödo-displastik nükleer değişikliklerin yanlışlıkla HSIL (ağır displazi)** olarak yorumlanmasıdır.\n\n- **Nükleer Büyüme ve Artmış N/S Oranı:** Parabazal hücrelerin sitoplazması dar olduğundan nükleus/sitoplazma (N/S) oranı fizyolojik olarak yüksektir. Kuruma veya inflamasyon artefaktıyla nükleus hafifçe büyüyebilir.\n- **Kromatin Yapısı (Anahtar Kriter):** Gerçek displazide (HSIL) nükleer membran düzensiz, girintili çıkıntılı ve kromatin kaba topaklı (hiperkromatik) iken; atrofik hücrelerde **nükleer kontur tamamen pürüzsüz, yuvarlak ve kromatin homojen-düzgündür**.\n- **Östrojen Testi:** Şüpheli kalan olgularda hastaya 1-2 hafta lokal östrojen krem tedavisi verilir. Hormon etkisiyle atrofik hücreler hızla olgunlaşarak süperfisiyel hücrelere döner ve sitoloji normale döner; gerçek bir HSIL lezyonu ise östrojenle kaybolmaz.\n\n> [!NOTE]\n> [KLİNİK İPUCU] Atrofi ile HSIL arasında kalınan şüpheli postmenopozal yaymalarda lokal östrojen tedavisi sonrası smear tekrarı en güvenilir tanısal çözümdür.",
            "bulletPoints": [
                "Atrofik parabazal hücrelerin yüksek N/S oranı HSIL ile karışabilir.",
                "Düzgün nükleer membran ve homojen kromatin atrofiyi destekler.",
                "Lokal östrojen testi sonrası sitolojinin düzelmesi atrofiyi kanıtlar."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Atrofik hücrelerin HSIL'den ayrımında şüpheli olgulara kısa süreli lokal östrojen testi uygulanarak smear tekrarlanır.",
                    "maskedTerm": "östrojen testi",
                    "hint": "Epitelin olgunlaşmasını sağlayarak atrofiyi ortadan kaldıran tanısal hormon uygulaması"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Atrofik Parabazal Hücreler vs HSIL",
                    "tableHeaders": ["Hücresel Kriter", "Atrofik Parabazal Hücre", "Gerçek HSIL Hücresi"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Nükleer Membran", "isMasked": False},
                                {"text": "Düzgün, yuvarlak, pürüzsüz sınır", "isMasked": True, "hint": "girintisiz muntazam hat"},
                                {"text": "Düzensiz, girintili çıkıntılı, çentikli"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Kromatin Dağılımı", "isMasked": False},
                                {"text": "Homojen, ince granüler, düzgün", "isMasked": True, "hint": "kaba kümelenme göstermeyen nükleus"},
                                {"text": "Kaba granüler, koyu hiperkromatik"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Şüpheli Atrofik Yaymada Tanısal Doğrulama",
                    "steps": [
                        "1. Şüpheli Smear: Yaşlı hastada yüksek N/S oranlı hücreler görülür, HSIL şüphesi doğar.",
                        "2. Kromatin İncelemesi: Nükleer membranın düzgün ve kromatini homojen olduğu fark edilir.",
                        "3. Östrojen Uygulaması: Hastaya 10 gün lokal östrojen krem reçete edilir.",
                        "4. Kontrol Yayma: Epitel olgunlaşır, atipik görünüm kaybolarak atrofi doğrulanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Postmenopozal bir kadında atrofik parabazal hücrelerin HSIL (ağır displazi) ile karışmasını önleyen en temel nükleer mikroskobik özellik nedir?",
                    "answer": "Nükleer membranın tamamen pürüzsüz/düzgün olması ve kromatinin kaba topaklanma göstermeyip ince ve homojen dağılmasıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Atrofi vs HSIL Ayrımı",
                    "items": [
                        {"text": "Atrofik parabazal hücreler yüksek N/S oranı nedeniyle displaziyi taklit edebilir.", "isLie": False, "explanation": "Doğru. Yaygın bir sitolojik tuzaktır."},
                        {"text": "Atrofik hücrelerde nükleer kontur düzgün ve kromatin homojendir.", "isLie": False, "explanation": "Doğru. Malignite lehine bulgu yoktur."},
                        {"text": "Lokal östrojen testi şüpheli olgularda epitel maturasyonunu sağlayarak ayrım yaptırır.", "isLie": False, "explanation": "Doğru. Standart klinik yaklaşımdır."},
                        {"text": "HSIL lezyonları 1 damla östrojen kremle 10 saniye içinde tamamen yok olur.", "isLie": True, "explanation": "Tuzak! Gerçek neoplastik HSIL lezyonları östrojen tedavisiyle kaybolmaz, varlığını sürdürür."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Postmenopozal bir kadının Pap testinde yüksek nükleus/sitoplazma oranına sahip hücreler görülüyor ancak nükleer membran pürüzsüz ve kromatin homojen bulunuyor. Bu tablonun HSIL değil de atrofi olduğunu doğrulamak için en uygun yaklaşım nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Kısa süreli lokal östrojen tedavisi verip sitolojiyi tekrarlamak",
                            "isCorrect": True,
                            "explanation": "Östrojen testi atrofik hücreleri olgunlaştırarak psödo-displaziyi siler ve doğru tanıyı sağlar."
                        },
                        {
                            "key": "B",
                            "text": "Hastaya derhal kemik iliği nakli planlamak",
                            "isCorrect": False,
                            "explanation": "Gereksiz ve konu dışı ağır girişimdir."
                        },
                        {
                            "key": "C",
                            "text": "Hiçbir tetkik yapmadan radikal pelvik ekzanterasyon uygulamak",
                            "isCorrect": False,
                            "explanation": "Atrofi için aşırı ve hatalı cerrahidir."
                        },
                        {
                            "key": "D",
                            "text": "Sitolojiyi tamamen çöpe atıp hastanın takibini bırakmak",
                            "isCorrect": False,
                            "explanation": "Tıbbi takip prensiplerine aykırıdır."
                        }
                    ]
                }
            ]
        },
        # S70
        {
            "slideNumber": 70,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 7] Nadir Tümörler, DES Adenozisi ve Atrofik Süreçler",
            "subtitle": "Bölüm 7 kapsamındaki Malign Melanom, DES ve berrak hücreli karsinom, sarkoma botryoides ve atrofi sentezi",
            "clinicalFocus": "Kapsamlı Bölüm Tekrarı",
            "content": "Bölüm 7 boyunca vulva ve vajinanın nadir malignitelerini, konjenital/ilaç ilişkili anomalilerini ve postmenopozal fizyopatolojiyi konsolide ettik.\n\n- **Vulvar Melanom ve BCC:** Malign melanom vulvanın ikinci sık kanseri olup S100/HMB-45 pozitiftir; BCC ise periferik palizatlanma gösterir ve lokal agresif seyreder.\n- **DES ve Vajinal Adenozis:** İntrauterin DES maruziyeti kalıcı glandüler adacıklara (vajinal adenozis) ve berrak hücreli (clear cell) adenokarsinoma yol açar.\n- **Pediatrik Sarkom:** Sarkoma botryoides <5 yaş çocukta kambiyum tabakası ve Desmin/Miyogenin pozitifliğiyle karakterizedir.\n- **Postmenopozal Atrofi:** Östrojen eksikliği parabazal hücre hakimiyeti yapar; düzgün nükleer membran ile HSIL'den ayrılır.\n\n> [!IMPORTANT]\n> [CHECKPOINT SENTEZİ] S100/HMB-45 vulvar melanomu kanıtlar; intrauterin DES maruziyeti berrak hücreli karsinom yapar; kambiyum tabakası ve Desmin pozitifliği sarkoma botryoides'i belgeler.",
            "synthesisNarrative": "Bölüm 7 boyunca vulva ve vajinanın nadir malignitelerini, konjenital/ilaç ilişkili anomalilerini ve postmenopozal fizyopatolojiyi konsolide ettik.\n\n- **Vulvar Melanom ve BCC:** Malign melanom vulvanın ikinci sık kanseri olup S100/HMB-45 pozitiftir; BCC ise periferik palizatlanma gösterir ve lokal agresif seyreder.\n- **DES ve Vajinal Adenozis:** İntrauterin DES maruziyeti kalıcı glandüler adacıklara (vajinal adenozis) ve berrak hücreli (clear cell) adenokarsinoma yol açar.\n- **Pediatrik Sarkom:** Sarkoma botryoides <5 yaş çocukta kambiyum tabakası ve Desmin/Miyogenin pozitifliğiyle karakterizedir.\n- **Postmenopozal Atrofi:** Östrojen eksikliği parabazal hücre hakimiyeti yapar; düzgün nükleer membran ile HSIL'den ayrılır.\n\n> [!IMPORTANT]\n> [CHECKPOINT SENTEZİ] S100/HMB-45 vulvar melanomu kanıtlar; intrauterin DES maruziyeti berrak hücreli karsinom yapar; kambiyum tabakası ve Desmin pozitifliği sarkoma botryoides'i belgeler.",
            "bulletPoints": [
                "Vulvar melanom S100/HMB-45 (+), Paget ise CK7/Müsin (+) ile ayrılır.",
                "DES maruziyeti vajinal adenozis ve berrak hücreli adenokarsinom yapar.",
                "Sarkoma botryoides <5 yaş çocukta kambiyum tabakası ve Desmin/Miyogenin (+) içerir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "İntrauterin DES maruziyeti zemininde gelişen nadir ve agresif vajina tümörüne berrak hücreli karsinom adı verilir.",
                    "maskedTerm": "berrak hücreli karsinom",
                    "hint": "Glikojen dolu şeffaf sitoplazmalı hobnail hücreli tümör"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bölüm 7 Patoloji Karşılaştırma Tablosu",
                    "tableHeaders": ["Tümör / Lezyon", "Karakteristik Tanı Belirteci", "Klinik Özellik"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Vulvar Malign Melanom", "isMasked": False},
                                {"text": "S100, Melan-A, HMB-45 (+), Müsin (-)", "isMasked": True, "hint": "melanositik immün profil"},
                                {"text": "Vulvanın ikinci en sık malignitesi"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Sarkoma Botryoides", "isMasked": False},
                                {"text": "Kambiyum tabakası, Desmin ve Miyogenin (+)", "isMasked": True, "hint": "çizgili kas sarkomu belirteçleri"},
                                {"text": "<5 yaş çocukta üzüm salkımı kitle"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Bölüm 7 Patolojiler Entegrasyon Zinciri",
                    "steps": [
                        "1. Melanositik Tümör: Vulvada pigmente plak S100 ve HMB-45 ile melanom olarak tanınır.",
                        "2. Teratojenik Adenozis: Fetal DES maruziyeti gençlikte berrak hücreli adenokarsinoma yol açar.",
                        "3. Pediatrik Sarkom: Bebekte üzüm salkımı kitle kambiyum tabakası ve Desmin ile doğrulanır.",
                        "4. Menopozal Atrofi: Östrojen yokluğunda parabazal hücre hakimiyeti östrojen testiyle aydınlatılır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bölüm 7'de işlenen konulardan hareketle, fetal DES maruziyeti ile ilişkili vajina kanseri tipi ile <5 yaş çocuklarda saptanan embriyonel rabdomiyosarkomun patognomonik histolojik tabakası nedir?",
                    "answer": "DES ile ilişkili tümör berrak hücreli (clear cell) adenokarsinomdur; rabdomiyosarkomun tipik tabakası ise subepitelyal kambiyum tabakasıdır (cambium layer)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Bölüm 7 Genel Tekrar",
                    "items": [
                        {"text": "Vulvar melanomda S100 ve HMB-45 pozitifliği tanı koydurucudur.", "isLie": False, "explanation": "Doğru. Melanositik belirteçlerdir."},
                        {"text": "İntrauterin DES maruziyeti vajinal adenozis ve berrak hücreli karsinoma yol açar.", "isLie": False, "explanation": "Doğru. Kanıtlanmış ilaç ilişkisidir."},
                        {"text": "Sarkoma botryoides'te subepitelyal kambiyum tabakası izlenir.", "isLie": False, "explanation": "Doğru. Pediatrik sarkom bulgusudur."},
                        {"text": "Atrofik vajinitte epitel aşırı kalınlaşarak devasa boynuzsu kitleler üretir.", "isLie": True, "explanation": "Tuzak! Atrofik vajinitte epitel kalınlaşmaz, tam tersine aşırı incelir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Bölüm 7'de ele alınan tümörler ve klinik antiterle ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "DES maruziyeti berrak hücreli adenokarsinoma yol açar; sarkoma botryoides'te ise kambiyum tabakası ve Desmin pozitifliği tipiktir",
                            "isCorrect": True,
                            "explanation": "Bu sentez cümlesi bölümün iki kilit pediatrik/genç tümörünü eksiksiz özetler."
                        },
                        {
                            "key": "B",
                            "text": "Vulvar malign melanomda S100 daima negatif, saf kemik iliği hücreleri pozitiftir",
                            "isCorrect": False,
                            "explanation": "Melanomda S100 güçlü pozitiftir."
                        },
                        {
                            "key": "C",
                            "text": "Atrofik vajinit yalnızca yeni doğmuş erkek bebeklerde izlenir",
                            "isCorrect": False,
                            "explanation": "Postmenopozal kadınlarda östrojen eksikliği tablosudur."
                        },
                        {
                            "key": "D",
                            "text": "Fibroepitelyal polip daima 1 hafta içinde tüm vücuda yayılan ölümcül bir karsinomdur",
                            "isCorrect": False,
                            "explanation": "Erişkinlerde görülen tamamen selim bir poliptir."
                        }
                    ]
                }
            ]
        }
    ]
    return slides

if __name__ == '__main__':
    slides = get_s7_slides()
    print(f'Section 7 generated with {len(slides)} slides.')
