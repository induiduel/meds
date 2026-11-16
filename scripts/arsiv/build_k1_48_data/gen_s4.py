import json

def get_s4_slides():
    slides = [
        # S31
        {
            "slideNumber": 31,
            "title": "Vajinanın Malign Neoplazmları ve Prekanseröz Lezyonlar: VAIN",
            "subtitle": "Vajinal intraepitelyal neoplazi, displazi derecelendirmesi ve HPV rolü",
            "clinicalFocus": "Preinvaziv Vajinal Neoplazi",
            "content": "Vajinanın primer malign neoplazmları son derece nadir görülmekle birlikte, invaziv karsinom gelişimi öncesinde genellikle iyi tanımlanmış bir prekanseröz evre olan **Vajinal İntraepitelyal Neoplazi (VAIN)** tablosu izlenir.\n\n- **Etyolojik Ajan:** Servikal neoplazilerde olduğu gibi VAIN gelişiminde de temel itici güç yüksek onkojenik riskli Human Papilloma Virus (özellikle **HPV tip 16 ve 18**) persistan enfeksiyonudur.\n- **Derecelendirme (VAIN 1, 2, 3):** Atipik hücrelerin epitel kalınlığı boyunca yayılımına göre üçe ayrılır. VAIN 1'de atipi epitelin alt 1/3'üne sınırlıyken; VAIN 3'te (karsinoma in situ) epitelin tamamını pleomorfik, yüksek nükleus/sitoplazma oranına sahip, mitoz içeren atipik hücreler kaplar.\n- **Klinik Yaklaşım:** Çoğunlukla asemptomatiktir; rutin servikovajinal Pap smear taramalarında veya kolposkopi sırasında lökoplakik/asetobeyaz alanlar şeklinde yakalanır.\n\n> [!NOTE]\n> VAIN lezyonları asemptomatik seyrettiğinden, serviks kanseri veya CIN öyküsü olan kadınlarda vajen fornikslerinin kolposkopik takibi kritiktir.",
            "synthesisNarrative": "Vajinanın primer malign neoplazmları son derece nadir görülmekle birlikte, invaziv karsinom gelişimi öncesinde genellikle iyi tanımlanmış bir prekanseröz evre olan **Vajinal İntraepitelyal Neoplazi (VAIN)** tablosu izlenir.\n\n- **Etyolojik Ajan:** Servikal neoplazilerde olduğu gibi VAIN gelişiminde de temel itici güç yüksek onkojenik riskli Human Papilloma Virus (özellikle **HPV tip 16 ve 18**) persistan enfeksiyonudur.\n- **Derecelendirme (VAIN 1, 2, 3):** Atipik hücrelerin epitel kalınlığı boyunca yayılımına göre üçe ayrılır. VAIN 1'de atipi epitelin alt 1/3'üne sınırlıyken; VAIN 3'te (karsinoma in situ) epitelin tamamını pleomorfik, yüksek nükleus/sitoplazma oranına sahip, mitoz içeren atipik hücreler kaplar.\n- **Klinik Yaklaşım:** Çoğunlukla asemptomatiktir; rutin servikovajinal Pap smear taramalarında veya kolposkopi sırasında lökoplakik/asetobeyaz alanlar şeklinde yakalanır.\n\n> [!NOTE]\n> VAIN lezyonları asemptomatik seyrettiğinden, serviks kanseri veya CIN öyküsü olan kadınlarda vajen fornikslerinin kolposkopik takibi kritiktir.",
            "bulletPoints": [
                "VAIN, vajinal skuamöz karsinomun öncü lezyonudur.",
                "Yüksek riskli HPV (tip 16 ve 18) enfeksiyonu ile ilişkilidir.",
                "Atipinin katman derinliğine göre VAIN 1, 2, 3 olarak sınıflanır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vajinal skuamöz hücreli karsinomun öncü prekanseröz lezyonuna Vajinal İntraepitelyal Neoplazi adı verilir.",
                    "maskedTerm": "Vajinal İntraepitelyal Neoplazi",
                    "hint": "VAIN kısaltmasıyla bilinen displastik epitel tablosu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vajinal İntraepitelyal Neoplazi (VAIN) Derecelendirmesi",
                    "tableHeaders": ["Evre", "Atipinin Epiteldeki Yayılımı", "Klinik Önlem"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "VAIN 1 (Hafif Displazi)", "isMasked": False},
                                {"text": "Epitelin alt 1/3 tabakasına sınırlı", "isMasked": True, "hint": "bazal katman displazisi"},
                                {"text": "Çoğu spontan geriler, takip edilir", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "VAIN 3 (Ağır Displazi / CIS)", "isMasked": False},
                                {"text": "Tüm epitel kalınlığını tutan atipi", "isMasked": False},
                                {"text": "Lokal eksizyon / ablasyon gerektirir", "isMasked": True, "hint": "invazyonu önleyici cerrahi müdahale"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "HPV Enfeksiyonundan VAIN'e",
                    "steps": [
                        "1. Viral İnokülasyon: Yüksek riskli HPV tip 16 vajina epitelinin bazal hücrelerine yerleşir.",
                        "2. Onkogen Ekspresyonu: Viral E6 ve E7 proteinleri p53 ve Rb tümör baskılayıcılarını inhibe eder.",
                        "3. Displazi: Epitel hücrelerinde atipi, mitoz ve tabakalaşma bozukluğu başlar (VAIN 1-2).",
                        "4. Karsinoma in Situ: Epitelin tamamı atipik hücrelerle dolarak VAIN 3 tablosu oturur."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "VAIN gelişiminde rol oynayan en önemli viral etken nedir ve histolojik derecelendirmesi neye göre yapılır?",
                    "answer": "Yüksek riskli HPV (özellikle tip 16 ve 18) temel etkendir; derecelendirme atipik hücrelerin epitel kalınlığının ne kadarlık kısmını (alt 1/3, 2/3 veya tamamı) tuttuğuna göre yapılır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajinal İntraepitelyal Neoplazi (VAIN)",
                    "items": [
                        {"text": "VAIN, vajinal skuamöz hücreli karsinomun kanıtlanmış öncü lezyonudur.", "isLie": False, "explanation": "Doğru. Servikal CIN gibi premalign karakterdedir."},
                        {"text": "Yüksek riskli HPV tipleri (HPV 16 ve 18) VAIN patogenezinde kritik rol oynar.", "isLie": False, "explanation": "Doğru. Onkojenik HPV tipleri temel tetikleyicidir."},
                        {"text": "VAIN 3 tablosunda atipi tüm epitel katmanlarını kaplar (karsinoma in situ).", "isLie": False, "explanation": "Doğru. Tam kat atipi mevcuttur."},
                        {"text": "VAIN yalnızca yenidoğan erkek çocuklarda görülen bir kemik displazisidir.", "isLie": True, "explanation": "Tuzak! VAIN kadın vajina skuamöz epitelinin prekanseröz neoplastik lezyonudur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vajinal İntraepitelyal Neoplazi (VAIN) ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Vajinal skuamöz karsinomun öncü lezyonudur ve yüksek riskli HPV enfeksiyonu ile ilişkilidir",
                            "isCorrect": True,
                            "explanation": "VAIN invaziv vajina SCC'sinin yüksek riskli HPV kaynaklı premalign öncülüdür."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca karaciğer hepatositlerinden köken alan selim bir hamartomdur",
                            "isCorrect": False,
                            "explanation": "Vajina skuamöz epitelinin intraepitelyal neoplazisidir."
                        },
                        {
                            "key": "C",
                            "text": "Tanı anında daima kemik iliğine doğrudan masif metastaz yapmış durumdadır",
                            "isCorrect": False,
                            "explanation": "İntraepitelyal bir lezyondur, bazal membranı aşmadığı için metastaz yapamaz."
                        },
                        {
                            "key": "D",
                            "text": "HPV enfeksiyonu ile hiçbir biyolojik ve epidemiyolojik bağlantısı yoktur",
                            "isCorrect": False,
                            "explanation": "Yüksek riskli HPV (tip 16) temel etyolojik faktördür."
                        }
                    ]
                }
            ]
        },
        # S32
        {
            "slideNumber": 32,
            "title": "Vajinal Skuamöz Hücreli Karsinom: Risk Faktörleri ve Lokalizasyon",
            "subtitle": "Geçirilmiş serviks karsinomu öyküsü ve üst vajina arka duvar tutulumu",
            "clinicalFocus": "Primer Vajina Kanseri",
            "content": "Primer vajinal karsinom, tüm kadın genital sistem kanserlerinin yalnızca %1'inden daha azını oluşturan son derece nadir bir malignitedir. Neredeyse tüm primer karsinomlar **skuamöz hücreli karsinom (SCC)** tipindedir.\n\n- **En Büyük Risk Faktörü:** Hastanın geçmişinde **serviks karsinomu veya vulva karsinomu öyküsü** bulunmasıdır. Aynı risk faktörlerini (özellikle yüksek riskli persistan HPV enfeksiyonunu) paylaşan kadın alt genital traktusunda 'alan kanserleşmesi' (field cancerization) fenomeni nedeniyle vajinal kanser riski katbekat artar.\n- **Lokalizasyon:** Primer vajinal skuamöz karsinom en sık **üst vajinada, özellikle ektoserviks ile birleşme noktasına komşu arka duvarda** yerleşim gösterir.\n- **Klinik Belirti:** En sık postkoital kanama, anormal vajinal kanama veya kokulu akıntı ile kendini gösterir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Vajinal skuamöz karsinom için en büyük risk faktörü geçirilmiş serviks veya vulva karsinomu öyküsüdür; tümör en sık üst vajina arka duvarına yerleşir.",
            "synthesisNarrative": "Primer vajinal karsinom, tüm kadın genital sistem kanserlerinin yalnızca %1'inden daha azını oluşturan son derece nadir bir malignitedir. Neredeyse tüm primer karsinomlar **skuamöz hücreli karsinom (SCC)** tipindedir.\n\n- **En Büyük Risk Faktörü:** Hastanın geçmişinde **serviks karsinomu veya vulva karsinomu öyküsü** bulunmasıdır. Aynı risk faktörlerini (özellikle yüksek riskli persistan HPV enfeksiyonunu) paylaşan kadın alt genital traktusunda 'alan kanserleşmesi' (field cancerization) fenomeni nedeniyle vajinal kanser riski katbekat artar.\n- **Lokalizasyon:** Primer vajinal skuamöz karsinom en sık **üst vajinada, özellikle ektoserviks ile birleşme noktasına komşu arka duvarda** yerleşim gösterir.\n- **Klinik Belirti:** En sık postkoital kanama, anormal vajinal kanama veya kokulu akıntı ile kendini gösterir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Vajinal skuamöz karsinom için en büyük risk faktörü geçirilmiş serviks veya vulva karsinomu öyküsüdür; tümör en sık üst vajina arka duvarına yerleşir.",
            "bulletPoints": [
                "Primer vajina kanserlerinin neredeyse tamamı skuamöz karsinomdur.",
                "En büyük risk faktörü önceki serviks veya vulva karsinomu öyküsüdür.",
                "En sık üst vajina arka duvarında lokalizedir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vajinal skuamöz hücreli karsinom için en büyük risk faktörü daha önce serviks veya vulva karsinomu öyküsü bulunmasıdır.",
                    "maskedTerm": "serviks veya vulva karsinomu",
                    "hint": "Alt genital sistemde alan kanserleşmesini gösteren önceki malignite öyküsü"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vajinal Skuamöz Karsinom Klinik Özellikleri",
                    "tableHeaders": ["Özellik", "Bulgu", "Klinik Yorum"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "En Sık Lokalizasyon", "isMasked": False},
                                {"text": "Üst vajina arka duvarı", "isMasked": True, "hint": "ektoservikse komşu posterior forniks"},
                                {"text": "Pelvik lenfatik drenaja yakınlık gösterir", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "En Önemli Risk Faktörü", "isMasked": False},
                                {"text": "Geçirilmiş serviks/vulva karsinomu", "isMasked": False},
                                {"text": "Alan kanserleşmesi ve persistan HPV zeminidir", "isMasked": True, "hint": "ortak onkojenik maruziyet"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Alan Kanserleşmesinden Vajina Kanserine",
                    "steps": [
                        "1. HPV Maruziyeti: Alt genital kanal çok katlı yassı epiteli persistan HPV-16 ile enfekte olur.",
                        "2. Servikal Karsinom: İlk olarak dönüşüm zonunda serviks karsinomu gelişir ve tedavi edilir.",
                        "3. Alan Kanserleşmesi: Vajina epitelindeki latent atipik klonlar yıllar sonra aktifleşir.",
                        "4. Vajinal Karsinom: Üst vajina arka duvarında primer invaziv skuamöz karsinom kitlesi ürer."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Primer vajinal skuamöz hücreli karsinom en sık vajinanın hangi anatomik bölgesine yerleşir ve en kritik risk faktörü nedir?",
                    "answer": "En sık üst vajina arka duvarında yerleşir; en önemli risk faktörü ise hastanın geçmişinde serviks veya vulva karsinomu öyküsü bulunmasıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajinal Skuamöz Hücreli Karsinom",
                    "items": [
                        {"text": "Primer vajinal karsinomların neredeyse tamamı skuamöz hücreli karsinomdur.", "isLie": False, "explanation": "Doğru. Histolojik tiplerin ezici çoğunluğu SCC'dir."},
                        {"text": "En büyük risk faktörü geçirilmiş serviks veya vulva karsinomu öyküsüdür.", "isLie": False, "explanation": "Doğru. Alan kanserleşmesi riski katlar."},
                        {"text": "Tümör çoğunlukla üst vajinanın arka duvarına yerleşim gösterir.", "isLie": False, "explanation": "Doğru. Ektoserviks bileşkesindeki arka duvar en sık lokalizasyondur."},
                        {"text": "Vajina kanseri kadınlarda meme kanserinden 50 kat daha sık izlenir.", "isLie": True, "explanation": "Tuzak! Vajina kanseri jinekolojik malignitelerin <%1'idir; son derece nadirdir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Primer vajinal skuamöz hücreli karsinom ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "En büyük risk faktörü önceki serviks veya vulva karsinomu öyküsüdür ve en sık üst vajina arka duvarında yerleşir",
                            "isCorrect": True,
                            "explanation": "Bu ifade vajinal SCC'nin Robbins ve ders notundaki en temel iki klinik özelliğini içerir."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca erkeklerde prostat bezinden köken alarak vajinaya sarkan bir adenomdur",
                            "isCorrect": False,
                            "explanation": "Vajina kadın genital organıdır."
                        },
                        {
                            "key": "C",
                            "text": "Tümör hücreleri daima bol kıkırdak ve kemik matriksi üreten bir kondromdur",
                            "isCorrect": False,
                            "explanation": "Tümör kıkırdak değil skuamöz epitel karsinomudur."
                        },
                        {
                            "key": "D",
                            "text": "Geçirilmiş serviks kanseri öyküsü olanlarda vajina kanseri riski tamamen sıfırlanır",
                            "isCorrect": False,
                            "explanation": "Tam tersine geçirilmiş serviks kanseri en büyük risk faktörüdür."
                        }
                    ]
                }
            ]
        },
        # S33
        {
            "slideNumber": 33,
            "title": "Vajinal Karsinomun Lenfatik Yayılım Paterni",
            "subtitle": "Üst vajina iliak drenajı vs alt vajina inguinal drenajı",
            "clinicalFocus": "Lenfatik Yayılım Anatomisi",
            "content": "Vajinal skuamöz hücreli karsinomun metastaz paterni ve cerrahi/radyoterapötik planlaması, lezyonun vajina boyunca yerleştiği kranyal-kaudal anatomik seviyeye sıkı sıkıya bağlıdır.\n\n- **Üst Vajina Yerleşimi:** Vajinanın üst 2/3'lük kısmından kaynaklanan tümörler, embriyolojik kökenlerine uygun olarak serviks karsinomu gibi drene olur. İlk metastaz durağı **bölgesel iliak lenf düğümleridir** (internal iliak, eksternal iliak ve obturatuar lenf nodları).\n- **Alt Vajina Yerleşimi:** Vajinanın alt 1/3'lük kısmında yerleşen tümörler ise vulva karsinomu gibi drene olur. İlk metastaz durağı **inguinofemoral (kasık) lenf düğümleridir**.\n- **Uzak Metastaz:** Akciğer, karaciğer ve kemik gibi uzak organ metastazları hastalığın daha ileri evrelerinde kan yoluyla (hematogen) gelişir.\n\n> [!NOTE]\n> Üst vajina tümörleri iliak lenf nodlarına, alt vajina tümörleri ise inguinal lenf nodlarına metastaz yapar; bu anatomik ikiye ayrım cerrahi lenf nodu diseksiyon sahasını belirler.",
            "synthesisNarrative": "Vajinal skuamöz hücreli karsinomun metastaz paterni ve cerrahi/radyoterapötik planlaması, lezyonun vajina boyunca yerleştiği kranyal-kaudal anatomik seviyeye sıkı sıkıya bağlıdır.\n\n- **Üst Vajina Yerleşimi:** Vajinanın üst 2/3'lük kısmından kaynaklanan tümörler, embriyolojik kökenlerine uygun olarak serviks karsinomu gibi drene olur. İlk metastaz durağı **bölgesel iliak lenf düğümleridir** (internal iliak, eksternal iliak ve obturatuar lenf nodları).\n- **Alt Vajina Yerleşimi:** Vajinanın alt 1/3'lük kısmında yerleşen tümörler ise vulva karsinomu gibi drene olur. İlk metastaz durağı **inguinofemoral (kasık) lenf düğümleridir**.\n- **Uzak Metastaz:** Akciğer, karaciğer ve kemik gibi uzak organ metastazları hastalığın daha ileri evrelerinde kan yoluyla (hematogen) gelişir.\n\n> [!NOTE]\n> Üst vajina tümörleri iliak lenf nodlarına, alt vajina tümörleri ise inguinal lenf nodlarına metastaz yapar; bu anatomik ikiye ayrım cerrahi lenf nodu diseksiyon sahasını belirler.",
            "bulletPoints": [
                "Üst vajina tümörleri bölgesel iliak lenf nodlarına drene olur.",
                "Alt vajina tümörleri inguinofemoral lenf nodlarına yayılır.",
                "Uzak organ metastazları geç dönemde hematogen gelişir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Üst vajinadan kaynaklanan skuamöz hücreli karsinom öncelikle bölgesel iliak lenf düğümlerine metastaz yapma eğilimindedir.",
                    "maskedTerm": "iliak lenf düğümlerine",
                    "hint": "Pelvis içinde ana damarlar etrafında yer alan lenf istasyonu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vajina Karsinomunda Seviyeye Göre Lenfatik Drenaj",
                    "tableHeaders": ["Tümör Lokalizasyonu", "Lenfatik Drenaj Yolu", "Örnek Aldığı Model"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Üst Vajina (2/3)", "isMasked": False},
                                {"text": "İliak lenf nodları (pelvik)", "isMasked": True, "hint": "pelvis içi derin lenf bezleri"},
                                {"text": "Serviks karsinomu gibi drene olur", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Alt Vajina (1/3)", "isMasked": False},
                                {"text": "İnguinofemoral lenf nodları (kasık)", "isMasked": False},
                                {"text": "Vulva karsinomu gibi drene olur", "isMasked": True, "hint": "dış genital kutanöz drenaj modeli"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Üst Vajina Lenfatik Metastaz Yolu",
                    "steps": [
                        "1. Üst Forniks Tümörü: Ektoserviks komşuluğunda invaziv SCC odağı paravajinal dokuya girer.",
                        "2. Pelvik Lenfatikler: Tümör hücreleri internal ve eksternal iliak lenf damarlarına penetre olur.",
                        "3. Bölgesel Tutulum: İliak lenf nodlarında metastatik kitleler gelişir.",
                        "4. Sistemik Evre: Paraaortik nodlar aşılarak torasik duktus yoluyla genel kan dolaşımına geçilir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Üst vajina ile alt vajina karsinomlarının primer lenfatik drenaj durakları arasındaki fark nedir?",
                    "answer": "Üst vajina tümörleri bölgesel iliak (pelvik) lenf düğümlerine; alt vajina tümörleri ise inguinofemoral (kasık) lenf düğümlerine drene olur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajinal Karsinomun Lenfatik Drenajı",
                    "items": [
                        {"text": "Üst vajina karsinomları bölgesel iliak lenf düğümlerine yayılma eğilimindedir.", "isLie": False, "explanation": "Doğru. Serviks gibi pelvik iliak nodlara gider."},
                        {"text": "Alt vajina tümörleri inguinofemoral lenf nodlarına metastaz yapabilir.", "isLie": False, "explanation": "Doğru. Vulva gibi kasık lenf nodlarına drene olur."},
                        {"text": "Uzak metastazlar ileri evrelerde kan yoluyla (akciğer vb.) ortaya çıkar.", "isLie": False, "explanation": "Doğru. Hematogen yayılım ileri evre bulgusudur."},
                        {"text": "Vajina tümörleri vücuttaki hiçbir lenf düğümüne asla ulaşamaz.", "isLie": True, "explanation": "Tuzak! Lenfatik metastaz vajinal karsinomun en temel yayılım yoludur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Üst vajinadan kaynaklanan primer bir skuamöz hücreli karsinomun İLK bölgesel lenfatik yayılım durağı hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Bölgesel iliak lenf düğümleri",
                            "isCorrect": True,
                            "explanation": "Üst vajina lenfatikleri serviks gibi bölgesel iliak lenf nodlarına dökülür."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca submandibular boyun lenf nodları",
                            "isCorrect": False,
                            "explanation": "Pelvik bir tümör boyun nodlarına doğrudan ilk durak olarak gitmez."
                        },
                        {
                            "key": "C",
                            "text": "Aksiller apeks lenf nodları",
                            "isCorrect": False,
                            "explanation": "Aksiller nodlar memenin drenaj durağıdır."
                        },
                        {
                            "key": "D",
                            "text": "Popliteal diz arkası lenf nodları",
                            "isCorrect": False,
                            "explanation": "Vajina drenajı popliteal bölgeye gitmez."
                        }
                    ]
                }
            ]
        },
        # S34
        {
            "slideNumber": 34,
            "title": "Embriyonel Rabdomiyosarkom (Sarkoma Botryoides): Çocukluk Çağı Malignitesi",
            "subtitle": "5 yaş altı kız çocukları, üzüm salkımı kitlesi ve rabdomiyoblastlar",
            "clinicalFocus": "Pediatrik Vajinal Kanser",
            "content": "Embriyonel rabdomiyosarkom (özel varyantıyla **Sarkoma Botryoides**), çocukluk çağının son derece nadir fakat hayatı tehdit edici malign yumuşak doku tümörüdür.\n\n- **Yaş Grubu ve İnsidans:** Neredeyse tamamen **bebeklerde ve 5 yaşından küçük kız çocuklarında** görülür; erişkinlerde pratik olarak izlenmez.\n- **Makroskopi (Sarkoma Botryoides):** Vajina lümeninden dışarı sarkan, jelatinöz, ödemli, polipoid, şeffaf **üzüm salkımı benzeri kitleler** şeklinde prezante olur ('botryoides' Yunanca üzüm salkımı demektir).\n- **Hücresel Köken:** Primitif mezenkimal kök hücrelerden ve malign embriyonel **rabdomiyoblastlardan** köken alır; çizgili kas diferansiasyonu gösterir.\n- **Diğer Organ Yerleşimleri:** Vajina dışında çocuklarda idrar kesesi (mesane) ve safra kanallarında da botriyoid rabdomiyosarkom gelişebilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] 5 yaşından küçük bir kız çocuğunda vajinadan dışarı sarkan üzüm salkımı benzeri kitle = Sarkoma Botryoides (Embriyonel Rabdomiyosarkom).",
            "synthesisNarrative": "Embriyonel rabdomiyosarkom (özel varyantıyla **Sarkoma Botryoides**), çocukluk çağının son derece nadir fakat hayatı tehdit edici malign yumuşak doku tümörüdür.\n\n- **Yaş Grubu ve İnsidans:** Neredeyse tamamen **bebeklerde ve 5 yaşından küçük kız çocuklarında** görülür; erişkinlerde pratik olarak izlenmez.\n- **Makroskopi (Sarkoma Botryoides):** Vajina lümeninden dışarı sarkan, jelatinöz, ödemli, polipoid, şeffaf **üzüm salkımı benzeri kitleler** şeklinde prezante olur ('botryoides' Yunanca üzüm salkımı demektir).\n- **Hücresel Köken:** Primitif mezenkimal kök hücrelerden ve malign embriyonel **rabdomiyoblastlardan** köken alır; çizgili kas diferansiasyonu gösterir.\n- **Diğer Organ Yerleşimleri:** Vajina dışında çocuklarda idrar kesesi (mesane) ve safra kanallarında da botriyoid rabdomiyosarkom gelişebilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] 5 yaşından küçük bir kız çocuğunda vajinadan dışarı sarkan üzüm salkımı benzeri kitle = Sarkoma Botryoides (Embriyonel Rabdomiyosarkom).",
            "bulletPoints": [
                "Bebeklerde ve 5 yaş altı kız çocuklarında izlenir.",
                "Vajinadan sarkan üzüm salkımı benzeri polipoid kitleler yapar.",
                "Malign embriyonel rabdomiyoblastlardan (çizgili kas) köken alır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Sarkoma botryoides tipik olarak beş yaşından küçük bebek ve çocuklarda izlenen embriyonel rabdomiyosarkom formudur.",
                    "maskedTerm": "beş yaşından küçük",
                    "hint": "Bu pediatrik sarkomun görüldüğü tipik yaş sınırı"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Sarkoma Botryoides Patolojik Karakteristikleri",
                    "tableHeaders": ["Özellik", "Bulgu", "Klinik Yansıma"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Hedef Yaş Grubu", "isMasked": False},
                                {"text": "Bebekler ve <5 yaş kız çocukları", "isMasked": True, "hint": "pediatrik erken çocukluk dönemi"},
                                {"text": "Erişkinlerde pratik olarak görülmez", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Makroskobik Form", "isMasked": False},
                                {"text": "Üzüm salkımı benzeri polipoid kitle", "isMasked": False},
                                {"text": "Vajina introitusundan dışarı sarkar", "isMasked": True, "hint": "dışarıdan fark edilen kitle"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Rabdomiyoblasttan Üzüm Salkımı Kitlesine",
                    "steps": [
                        "1. Onkojenik Transformasyon: Vajina submukozasındaki primitif embriyonel mezenkimal hücreler malignleşir.",
                        "2. Rabdomiyoblast Üremesi: Malign hücreler çizgili kas diferansiasyon belirteçleri (desmin, miyogenin) üretir.",
                        "3. Miksomatöz Stroma: Bol su tutan miksoid jelatinöz zemin içinde tümör lümene doğru polipoid büyür.",
                        "4. Botriyoid Kitle: Vajina açıklığından sarkan üzüm taneleri görünümünde kitleler belirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Sarkoma Botryoides hangi yaş grubunda görülür, histogenetik kökeni nedir ve klasik makroskopik görünümü nasıldır?",
                    "answer": "Bebekler ve 5 yaşından küçük çocuklarda görülür; malign embriyonel rabdomiyoblastlardan (çizgili kas) köken alır; makroskopik olarak vajinadan sarkan üzüm salkımı benzeri polipoid kitleler oluşturur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Embriyonel Rabdomiyosarkom (Sarkoma Botryoides)",
                    "items": [
                        {"text": "Sarkoma Botryoides tipik olarak 5 yaşından küçük bebek ve çocuklarda izlenir.", "isLie": False, "explanation": "Doğru. Pediatrik dönemin özgül tümörüdür."},
                        {"text": "Tümör malign embriyonel rabdomiyoblastlardan köken alır.", "isLie": False, "explanation": "Doğru. Çizgili kas kökenli embriyonel sarkomdur."},
                        {"text": "Makroskopik olarak üzüm salkımı benzeri jelatinöz kitleler oluşturur.", "isLie": False, "explanation": "Doğru. Botryoides terimi üzüm salkımı demektir."},
                        {"text": "Sarkoma Botryoides daima 80 yaş üstü kadınlarda gelişen iyi huylu bir kemik kistidir.", "isLie": True, "explanation": "Tuzak! <5 yaş kız çocuklarında gelişen son derece malign bir yumuşak doku sarkomudur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "3 yaşındaki bir kız çocuğunda vajinadan dışarı sarkan üzüm salkımı benzeri jelatinöz kitle ile başvuran olguda EN OLASI tanı hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Embriyonel rabdomiyosarkom (Sarkoma Botryoides)",
                            "isCorrect": True,
                            "explanation": "5 yaş altı kız çocukta üzüm salkımı vajinal kitle Sarkoma Botryoides için patognomoniktir."
                        },
                        {
                            "key": "B",
                            "text": "İleri evre primer skuamöz hücreli karsinom",
                            "isCorrect": False,
                            "explanation": "Skuamöz karsinom ileri yaştaki erişkin kadınların tümörüdür."
                        },
                        {
                            "key": "C",
                            "text": "Gartner kanal kisti",
                            "isCorrect": False,
                            "explanation": "Gartner kisti selim ve düzgün sınırlı kisttir, üzüm salkımı malignite yapmaz."
                        },
                        {
                            "key": "D",
                            "text": "Meme kaynaklı Paget hastalığı metastazı",
                            "isCorrect": False,
                            "explanation": "Bebeklik çağında meme Paget metastazı söz konusu değildir."
                        }
                    ]
                }
            ]
        },
        # S35
        {
            "slideNumber": 35,
            "title": "Embriyonel Rabdomiyosarkom Histolojisi: Kambiyum Katmanı ve Kas Belirteçleri",
            "subtitle": "Kambiyum zonu, tenis raketi hücreleri, desmin ve miyogenin pozitifliği",
            "clinicalFocus": "Sarkoma Botryoides Histopatolojisi",
            "content": "Sarkoma Botryoides'in histopatolojik incelemesi, lümene doğru büyüyen miksomatöz polipoid yapılar altında özgül bir hücresel dağılım gösterir.\n\n- **Kambiyum Katmanı (Cambium Layer):** İnce vajinal epitelin hemen altında, hücresel yoğunluğun belirgin biçimde arttığı hipertrofik bir neoplastik kondansasyon zonudur. Bu zonun altında ise hücreden fakir, ödemli ve miksomatöz bir stroma bulunur.\n- **Rabdomiyoblast Morfolojisi:** Malign hücreler primitif yuvarlak hücrelerden, sitoplazmasında çizgili kas flamentleri barındıran eozinofilik **'tenis raketi'** veya **'kayış'** biçimli olgunlaşmamış rabdomiyoblastlara kadar değişkenlik gösterir.\n- **İmmünohistokimya:** Tanıyı kesinleştirmek için çizgili kas belirteçleri uygulanır. Tümör hücreleri **Desmin**, **Miyogenin (Myogenin)** ve **MyoD1** ile kuvvetli nükleer/sitoplazmik pozitiflik verir.\n\n> [!NOTE]\n> Kambiyum katmanı, epitel altındaki sıkı hücre kuşağı olup botriyoid rabdomiyosarkomun en karakteristik mikroskobik belirtecidir.",
            "synthesisNarrative": "Sarkoma Botryoides'in histopatolojik incelemesi, lümene doğru büyüyen miksomatöz polipoid yapılar altında özgül bir hücresel dağılım gösterir.\n\n- **Kambiyum Katmanı (Cambium Layer):** İnce vajinal epitelin hemen altında, hücresel yoğunluğun belirgin biçimde arttığı hipertrofik bir neoplastik kondansasyon zonudur. Bu zonun altında ise hücreden fakir, ödemli ve miksomatöz bir stroma bulunur.\n- **Rabdomiyoblast Morfolojisi:** Malign hücreler primitif yuvarlak hücrelerden, sitoplazmasında çizgili kas flamentleri barındıran eozinofilik **'tenis raketi'** veya **'kayış'** biçimli olgunlaşmamış rabdomiyoblastlara kadar değişkenlik gösterir.\n- **İmmünohistokimya:** Tanıyı kesinleştirmek için çizgili kas belirteçleri uygulanır. Tümör hücreleri **Desmin**, **Miyogenin (Myogenin)** ve **MyoD1** ile kuvvetli nükleer/sitoplazmik pozitiflik verir.\n\n> [!NOTE]\n> Kambiyum katmanı, epitel altındaki sıkı hücre kuşağı olup botriyoid rabdomiyosarkomun en karakteristik mikroskobik belirtecidir.",
            "bulletPoints": [
                "Epitel altında hiperhücresel kambiyum katmanı (cambium layer) izlenir.",
                "Eozinofilik tenis raketi / kayış biçimli rabdomiyoblastlar bulunur.",
                "Desmin, miyogenin ve MyoD1 ile çizgili kas pozitifliği verir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Sarkoma Botryoides mikroskopisinde epitelin hemen altında izlenen dens neoplastik hücre kuşağına kambiyum katmanı adı verilir.",
                    "maskedTerm": "kambiyum katmanı",
                    "hint": "Cambium layer olarak adlandırılan patognomonik kondansasyon zonu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Sarkoma Botryoides İmmünohistokimyasal Profili",
                    "tableHeaders": ["Belirteç", "Sonuç", "Hedef Dokusal Farklılaşma"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Desmin", "isMasked": False},
                                {"text": "Kuvvetli sitoplazmik pozitif", "isMasked": True, "hint": "kas ara filamenti pozitifliği"},
                                {"text": "Tüm kas tiplerinde bulunan ara filament", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Miyogenin (Myogenin)", "isMasked": False},
                                {"text": "Kuvvetli nükleer pozitif", "isMasked": False},
                                {"text": "Çizgili kas diferansiasyonunun kesin kanıtı", "isMasked": True, "hint": "rabdomiyositer nükleer faktör"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Botriyoid Rabdomiyosarkom Tanı Zinciri",
                    "steps": [
                        "1. Mikroskopi: Vajinal polip kesitinde ödemli miksoid stroma ve yüzey epiteli görülür.",
                        "2. Kambiyum Zonu: Epitelin hemen altındaki hiperhücresel yoğunlaşma bandı fark edilir.",
                        "3. Rabdomiyoblastlar: Tenis raketi biçimli eozinofilik primitif kas hücreleri incelenir.",
                        "4. Miyogenin İmmün Pozitifliği: Nükleer miyogenin pozitifliği ile rabdomiyosarkom tanısı mühürlenir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Sarkoma botryoides'in histopatolojisinde mikroskopik olarak en karakteristik hücresel kondansasyon kuşağına ne ad verilir?",
                    "answer": "Epitelin hemen altında yer alan hiperhücresel 'kambiyum katmanı' (cambium layer) adı verilir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Sarkoma Botryoides Mikroskopisi",
                    "items": [
                        {"text": "Yüzey epitelinin hemen altında yoğun hücreli kambiyum katmanı izlenir.", "isLie": False, "explanation": "Doğru. Kambiyum katmanı patognomoniktir."},
                        {"text": "Tümör hücreleri desmin ve miyogenin ile çizgili kas pozitifliği gösterir.", "isLie": False, "explanation": "Doğru. Çizgili kas belirteçleri pozitiftir."},
                        {"text": "Tenis raketi veya kayış benzeri atipik rabdomiyoblastlar saptanabilir.", "isLie": False, "explanation": "Doğru. Karakteristik sitolojik formlardır."},
                        {"text": "Tümör tümüyle osteositlerden ve kalsifiye kemik lamellerinden ibarettir.", "isLie": True, "explanation": "Tuzak! Tümör kemik değil, embriyonel çizgili kas (rabdomiyosarkom) tümörüdür."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Embriyonel rabdomiyosarkomun (Sarkoma Botryoides) histopatolojik özellikleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Epitel altında dens kambiyum katmanı içerir ve desmin/miyogenin pozitif rabdomiyoblastlar izlenir",
                            "isCorrect": True,
                            "explanation": "Kambiyum katmanı ve çizgili kas belirteçleri botriyoid rabdomiyosarkomun altın standardıdır."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca matür adipositlerden oluşan ve hiçbir mitoz içermeyen selim bir yağ bezidir",
                            "isCorrect": False,
                            "explanation": "Yağ bezi değil, malign embriyonel sarkomdur."
                        },
                        {
                            "key": "C",
                            "text": "Miyogenin ve desmin belirteçleri tüm olgularda daima kesin olarak negatiftir",
                            "isCorrect": False,
                            "explanation": "Çizgili kas kökenli olduğu için desmin ve miyogenin kuvvetli pozitiftir."
                        },
                        {
                            "key": "D",
                            "text": "Kambiyum katmanı hiçbir zaman görülmez, hücreler kemik iliğinde yerleşiktir",
                            "isCorrect": False,
                            "explanation": "Kambiyum katmanı vajina epitelinin hemen altındaki klasik tümör zonudur."
                        }
                    ]
                }
            ]
        },
        # S36
        {
            "slideNumber": 36,
            "title": "Serviks Patolojisine Giriş: Anatomik Ziyaret ve Ektoserviks-Endoserviks",
            "subtitle": "Skuamokolumnar bileşke, glandüler yapılar ve mukozal bariyer",
            "clinicalFocus": "Servikal Anatomi ve Histoloji",
            "content": "Uterin serviks (rahim ağzı), uterus korpusunu vajinaya bağlayan silindirik anatomik yapıdır. İki temel histolojik kompartmandan meydana gelir:\n\n- **Ektoserviks (Portio Vaginalis):** Vajina lümenine bakan dış kısımdır. Vajina gibi glikojenden zengin, keratinize olmayan **çok katlı yassı epitelle** döşelidir.\n- **Endoserviks (Endoservikal Kanal):** İç kanaldır. Müsin salgılayan **tek katlı silyasız prizmatik (kolumnar) epitelle** döşelidir; lümene açılan derin endoservikal glandüler kriptalar içerir.\n- **Hastalık Spektrumu:** Serviks lezyonlarının çok büyük bir kısmını selim inflamatuvar süreçler (**servisit**) oluşturur. Ancak epitelyal neoplaziler ve servikal karsinomlar dünya genelinde kadın ölümlerinin en önemli onkolojik nedenlerinden biridir.\n\n> [!NOTE]\n> Ektoserviksin çok katlı yassı epiteli ile endoserviksin tek katlı prizmatik epitelinin karşılaştığı anatomik sınıra skuamokolumnar bileşke (SCJ) denir.",
            "synthesisNarrative": "Uterin serviks (rahim ağzı), uterus korpusunu vajinaya bağlayan silindirik anatomik yapıdır. İki temel histolojik kompartmandan meydana gelir:\n\n- **Ektoserviks (Portio Vaginalis):** Vajina lümenine bakan dış kısımdır. Vajina gibi glikojenden zengin, keratinize olmayan **çok katlı yassı epitelle** döşelidir.\n- **Endoserviks (Endoservikal Kanal):** İç kanaldır. Müsin salgılayan **tek katlı silyasız prizmatik (kolumnar) epitelle** döşelidir; lümene açılan derin endoservikal glandüler kriptalar içerir.\n- **Hastalık Spektrumu:** Serviks lezyonlarının çok büyük bir kısmını selim inflamatuvar süreçler (**servisit**) oluşturur. Ancak epitelyal neoplaziler ve servikal karsinomlar dünya genelinde kadın ölümlerinin en önemli onkolojik nedenlerinden biridir.\n\n> [!NOTE]\n> Ektoserviksin çok katlı yassı epiteli ile endoserviksin tek katlı prizmatik epitelinin karşılaştığı anatomik sınıra skuamokolumnar bileşke (SCJ) denir.",
            "bulletPoints": [
                "Ektoserviks çok katlı yassı, endoserviks tek katlı kolumnar epitelle döşelidir.",
                "En sık servikal patolojiler selim servisitlerdir.",
                "Servikal karsinom kadınlarda dünya çapında ölümcül bir malignitedir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Endoservikal kanal mukusu salgılayan tek katlı prizmatik epitelle döşelidir.",
                    "maskedTerm": "tek katlı prizmatik",
                    "hint": "Müsin üreten kolumnar epitel tipi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Serviksin Anatomik ve Epitelyal Katmanları",
                    "tableHeaders": ["Bölge", "Epitel Tipi", "Hücresel Fonksiyon"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Ektoserviks", "isMasked": False},
                                {"text": "Keratinize olmayan çok katlı yassı epitel", "isMasked": False},
                                {"text": "Mekanik sürtünmeye direnç ve glikojen depolama", "isMasked": True, "hint": "koruyucu yassı epitel görevi"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Endoserviks", "isMasked": False},
                                {"text": "Tek katlı kolumnar (prizmatik) epitel", "isMasked": True, "hint": "mukus üreten silindirik örtü"},
                                {"text": "Alkali ve koruyucu servikal mukus salgısı", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "İki Farklı Epitelden Ortak Fonksiyona",
                    "steps": [
                        "1. Anatomik Bölünme: Ektoserviks vajinal lümene, endoserviks uterus kavitesine bakar.",
                        "2. Mukus Salgısı: Endoservikal kriptalar mukus üreterek asendan bakterilere tıkaç oluşturur.",
                        "3. Mekanik Bariyer: Ektoserviksin çok katlı yassı epiteli cinsel ilişki sürtünmesini karşılar.",
                        "4. Patolojiye Yansıma: Enfeksiyonlar servisit yaparken, karsinomlar bu iki epitelin sınırında doğar."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Ektoserviks ile endoserviksin normal histolojik epitel örtüleri nelerdir?",
                    "answer": "Ektoserviks keratinize olmayan çok katlı yassı epitelle; endoserviks ise müsin salgılayan tek katlı prizmatik (kolumnar) epitelle döşelidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Serviksin Genel Histolojisi ve Patolojisi",
                    "items": [
                        {"text": "Ektoserviks keratinize olmayan çok katlı yassı epitel ile örtülüdür.", "isLie": False, "explanation": "Doğru. Vajina epiteli ile devamlılık gösterir."},
                        {"text": "Endoservikal kanal müsin salgılayan tek katlı kolumnar epitelle döşelidir.", "isLie": False, "explanation": "Doğru. Mukus salgılayan bez benzeri kriptalar içerir."},
                        {"text": "Servikal patolojilerin en sık formu selim inflamatuvar servisitlerdir.", "isLie": False, "explanation": "Doğru. İnflamasyon en yaygın servikal tablodur."},
                        {"text": "Endoserviks kalın kemik iliği trabeküllerinden oluşan mezenkimal bir kanaldır.", "isLie": True, "explanation": "Tuzak! Endoserviks epitel döşeli bir kanaldır; kemik iliği içermez."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Serviksin anatomik ve histolojik yapısı ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Ektoserviks çok katlı yassı epitelle, endoserviks ise tek katlı prizmatik (kolumnar) epitelle döşelidir",
                            "isCorrect": True,
                            "explanation": "Serviksin iki temel kompartmanının klasik ve doğru histolojik tanımı budur."
                        },
                        {
                            "key": "B",
                            "text": "Ektoserviks ve endoserviks tamamen çizgili iskelet kasından ibarettir",
                            "isCorrect": False,
                            "explanation": "Serviks fibromüsküler bağ dokusu ve epitelden oluşur."
                        },
                        {
                            "key": "C",
                            "text": "Servikste karsinom gelişimi tıp tarihinde hiçbir zaman bildirilmemiştir",
                            "isCorrect": False,
                            "explanation": "Serviks kanseri dünyada kadınlarda en sık kanserlerden biridir."
                        },
                        {
                            "key": "D",
                            "text": "Endoservikal kanalın içi hava dolu boş bir sinüs boşluğudur",
                            "isCorrect": False,
                            "explanation": "Endoserviks mukus üreten epitel döşeli silindirik bir kanaldır."
                        }
                    ]
                }
            ]
        },
        # S37
        {
            "slideNumber": 37,
            "title": "Dönüşüm Zonu (Transformasyon Zonu) ve Skuamöz Metaplazi",
            "subtitle": "Asidik vajina ortamına adaptasyon ve karsinogenezin beşiği",
            "clinicalFocus": "Transformasyon Zonu Biyolojisi",
            "content": "Serviksin onkolojik açıdan en kritik ve en dinamik anatomik bölgesi **Transformasyon Zonu (Dönüşüm Zonu)** olarak adlandırılır.\n\n- **Skuamokolumnar Bileşke (SCJ):** Çok katlı yassı epitel ile tek katlı kolumnar epitelin buluştuğu mikroskobik sınırdır. Pubertede hormonal etkiyle (östrojen) serviks eversiyona uğrar ve hassas endoservikal kolumnar epitel vajinanın asidik ortamına maruz kalır (ektropion).\n- **Fizyolojik Skuamöz Metaplazi:** Asidik pH ve vajinal mikrofloranın irritasyonuna karşı koyabilmek için, endoservikal kolumnar epitelin altındaki subkolumnar rezerv hücreleri çoğalarak çok katlı yassı epitele dönüşür (metaplazi).\n- **Karsinogenezin Beşiği:** Metaplastik skuamöz epitel henüz olgunlaşma aşamasındayken Human Papilloma Virus (HPV) enfeksiyonuna ve viral genom entegrasyonuna karşı son derece hassastır. Neredeyse tüm servikal karsinomlar ve prekanseröz lezyonlar (CIN) bu dönüşüm zonundan köken alır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Servikal kanserlerin ve displazilerin (CIN/SIL) neredeyse tamamı skuamöz metaplazinin gerçekleştiği transformasyon zonundan köken alır.",
            "synthesisNarrative": "Serviksin onkolojik açıdan en kritik ve en dinamik anatomik bölgesi **Transformasyon Zonu (Dönüşüm Zonu)** olarak adlandırılır.\n\n- **Skuamokolumnar Bileşke (SCJ):** Çok katlı yassı epitel ile tek katlı kolumnar epitelin buluştuğu mikroskobik sınırdır. Pubertede hormonal etkiyle (östrojen) serviks eversiyona uğrar ve hassas endoservikal kolumnar epitel vajinanın asidik ortamına maruz kalır (ektropion).\n- **Fizyolojik Skuamöz Metaplazi:** Asidik pH ve vajinal mikrofloranın irritasyonuna karşı koyabilmek için, endoservikal kolumnar epitelin altındaki subkolumnar rezerv hücreleri çoğalarak çok katlı yassı epitele dönüşür (metaplazi).\n- **Karsinogenezin Beşiği:** Metaplastik skuamöz epitel henüz olgunlaşma aşamasındayken Human Papilloma Virus (HPV) enfeksiyonuna ve viral genom entegrasyonuna karşı son derece hassastır. Neredeyse tüm servikal karsinomlar ve prekanseröz lezyonlar (CIN) bu dönüşüm zonundan köken alır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Servikal kanserlerin ve displazilerin (CIN/SIL) neredeyse tamamı skuamöz metaplazinin gerçekleştiği transformasyon zonundan köken alır.",
            "bulletPoints": [
                "SCJ, yassı epitel ile kolumnar epitelin buluştuğu yerdir.",
                "Asidik vajinal ortam kolumnar epitelde skuamöz metaplazi tetikler.",
                "Serviks kanserlerinin hemen tamamı transformasyon zonunda doğar."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Servikal karsinomların ve prekanseröz lezyonların neredeyse tamamı skuamöz metaplazinin geliştiği transformasyon zonu bölgesinden köken alır.",
                    "maskedTerm": "transformasyon zonu",
                    "hint": "Dönüşüm zonu olarak bilinen onkolojik kavşak bölgesi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Transformasyon Zonu ve Metaplazi Basamakları",
                    "tableHeaders": ["Aşama", "Histolojik Süreç", "Onkolojik Önem"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Fizyolojik Tetik", "isMasked": False},
                                {"text": "Asidik vajina ortamına maruziyet", "isMasked": False},
                                {"text": "Subkolumnar rezerv hücre uyarımı", "isMasked": True, "hint": "kök hücre proliferasyonu"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Skuamöz Metaplazi", "isMasked": False},
                                {"text": "Kolumnar epitelin çok katlı yassı epitele dönüşümü", "isMasked": True, "hint": "koruyucu adaptif epitel değişimi"},
                                {"text": "HPV enfeksiyonuna ve displaziye en duyarlı zon", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Asidik Ortamdan Karsinogenez Hassasiyetine",
                    "steps": [
                        "1. Eversiyon: Pubertede endoservikal kolumnar epitel vajina forniksine doğru dışarı kayar.",
                        "2. Asidik Hasar: Vajinanın düşük pH'sı tek katlı glandüler epitelde kimyasal stres yaratır.",
                        "3. Metaplazi: Rezerv hücreler aktive olarak epitel çok katlı yassı epitele dönüşür (metaplazi).",
                        "4. HPV Duyarlılığı: İmmatür metaplastik hücreler yüksek riskli HPV'nin entegrasyonu için ideal hedef olur."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Servikal intraepitelyal neoplazilerin ve serviks karsinomlarının transformasyon zonunda kümelenmesinin patofizyolojik nedeni nedir?",
                    "answer": "Bu alanda aktif skuamöz metaplazinin gerçekleşmesi ve immatür metaplastik skuamöz hücrelerin HPV enfeksiyonuna ve genetik mutasyonlara karşı son derece savunmasız olmasıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Transformasyon Zonu ve Skuamöz Metaplazi",
                    "items": [
                        {"text": "Transformasyon zonu ektoserviks ile endoserviks arasındaki geçiş bölgesidir.", "isLie": False, "explanation": "Doğru. İki epitelin buluştuğu sahadır."},
                        {"text": "Asidik vajinal ortama uyum için fizyolojik skuamöz metaplazi gelişir.", "isLie": False, "explanation": "Doğru. Kolumnar epitel yassı epitele dönüşür."},
                        {"text": "Servikal karsinomların hemen hemen tümü bu transformasyon zonunda başlar.", "isLie": False, "explanation": "Doğru. En duyarlı onkolojik odaktır."},
                        {"text": "Transformasyon zonu yalnızca postmenopozal dönemde kemik iliği hücresi üretir.", "isLie": True, "explanation": "Tuzak! Transformasyon zonu epitel örtüsüdür; hematopoez yapmaz."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Serviksin transformasyon zonu (dönüşüm zonu) ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Skuamöz metaplazinin gerçekleştiği ve servikal karsinomların neredeyse tamamının başladığı kritik bölgedir",
                            "isCorrect": True,
                            "explanation": "Transformasyon zonunun patolojideki en temel onkolojik tanımı budur."
                        },
                        {
                            "key": "B",
                            "text": "Hiçbir zaman HPV enfeksiyonundan etkilenmeyen korunaklı bir kıkırdak tabakasıdır",
                            "isCorrect": False,
                            "explanation": "HPV'ye en duyarlı epitel sahasıdır."
                        },
                        {
                            "key": "C",
                            "text": "Yalnızca erkeklerde mesane tabanında yer alan bir salgı bezidir",
                            "isCorrect": False,
                            "explanation": "Kadın serviksinde yer alır."
                        },
                        {
                            "key": "D",
                            "text": "Skuamokolumnar bileşke ile hiçbir anatomik ve hücresel ilgisi yoktur",
                            "isCorrect": False,
                            "explanation": "Skuamokolumnar bileşkenin metaplaziyle yer değiştirmesi sonucu oluşur."
                        }
                    ]
                }
            ]
        },
        # S38
        {
            "slideNumber": 38,
            "title": "Akut ve Kronik Servisit: Etiyoloji ve Naboth Kistleri",
            "subtitle": "Klamidya, mikoplazma, lökosit infiltrasyonu ve retansiyon kistleri",
            "clinicalFocus": "Servisit Patolojisi",
            "content": "Servisit, serviks mukozasının son derece sık karşılaşılan inflamatuvar hastalığıdır. Doğurganlık çağındaki kadınların neredeyse tamamında mikroskobik düzeyde hafif bir servisit tablosu mevcuttur.\n\n- **Etyolojik Ajanlar:** Cinsel yolla bulaşan mikroorganizmalar (özellikle **Chlamydia trachomatis**, **Neisseria gonorrhoeae**, Trichomonas, HSV ve HPV) ile normal vajinal floranın anaerob bakterileri başlıca nedenlerdir.\n- **Klinik Belirti:** Pürülan veya mukoid vajinal akıntı, pelvik ağrı ve spekulum muayenesinde servikste eritem, ödem ve temasla kolay kanama izlenir.\n- **Naboth Kistleri (Mukus Retansiyon Kistleri):** Skuamöz metaplazi sürecinde çoğalan yassı epitel, endoservikal bezlerin (kriptaların) ağzını tıkar. Kripta içinde mukus salgısı hapsolarak birkaç milimetreden birkaç santimetreye varan selim **Naboth kistlerini** oluşturur.\n\n> [!NOTE]\n> Naboth kistleri servikste rutin jinekolojik muayenede inci tanesi gibi görülen tamamen selim, fizyolojik retansiyon kistleridir; malignite potansiyeli taşımaz.",
            "synthesisNarrative": "Servisit, serviks mukozasının son derece sık karşılaşılan inflamatuvar hastalığıdır. Doğurganlık çağındaki kadınların neredeyse tamamında mikroskobik düzeyde hafif bir servisit tablosu mevcuttur.\n\n- **Etyolojik Ajanlar:** Cinsel yolla bulaşan mikroorganizmalar (özellikle **Chlamydia trachomatis**, **Neisseria gonorrhoeae**, Trichomonas, HSV ve HPV) ile normal vajinal floranın anaerob bakterileri başlıca nedenlerdir.\n- **Klinik Belirti:** Pürülan veya mukoid vajinal akıntı, pelvik ağrı ve spekulum muayenesinde servikste eritem, ödem ve temasla kolay kanama izlenir.\n- **Naboth Kistleri (Mukus Retansiyon Kistleri):** Skuamöz metaplazi sürecinde çoğalan yassı epitel, endoservikal bezlerin (kriptaların) ağzını tıkar. Kripta içinde mukus salgısı hapsolarak birkaç milimetreden birkaç santimetreye varan selim **Naboth kistlerini** oluşturur.\n\n> [!NOTE]\n> Naboth kistleri servikste rutin jinekolojik muayenede inci tanesi gibi görülen tamamen selim, fizyolojik retansiyon kistleridir; malignite potansiyeli taşımaz.",
            "bulletPoints": [
                "Klamidya ve gonore sık servisit etkenleridir.",
                "Eritem, ödem ve pürülan akıntı izlenir.",
                "Metaplazinin bez ağzını tıkamasıyla selim Naboth kistleri gelişir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Endoservikal bez kanallarının skuamöz epitel ile tıkanması sonucu mukus birikimiyle Naboth kistleri gelişir.",
                    "maskedTerm": "Naboth kistleri",
                    "hint": "Servikste sık görülen selim mukus retansiyon kistleri"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Servisit ve Naboth Kisti Özellikleri",
                    "tableHeaders": ["Antite", "Oluşum Mekanizması", "Klinik Anlam"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Enfeksiyöz Servisit", "isMasked": False},
                                {"text": "C. trachomatis ve N. gonorrhoeae invazyonu", "isMasked": True, "hint": "bakteriyel cinsel enfeksiyon"},
                                {"text": "Pürülan akıntı ve temasla kanama", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Naboth Kisti", "isMasked": False},
                                {"text": "Metaplastik skuamöz epitelin bez ağzını tıkaması", "isMasked": False},
                                {"text": "Tamamen selim retansiyon kisti", "isMasked": True, "hint": "malign potansiyeli olmayan kist"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Skuamöz Metaplaziden Naboth Kistine",
                    "steps": [
                        "1. Metaplazi Hareketi: Dönüşüm zonundaki yassı epitel endoservikal kolumnar epitelin üzerine doğru büyür.",
                        "2. Kripta Ağzı Tıkanması: Mukus üreten derin endoservikal glandın boşaltım deliği yassı epitelce örtülür.",
                        "3. Mukus Hapsolması: Salgılanan mukus dışarı akamaz ve gland lümeninde birikerek şişer.",
                        "4. Naboth Kisti: Serviks yüzeyinde inci beyazı kubbe şeklinde selim kistik yapı belirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Servikste sıkça karşılaşılan Naboth kistlerinin patolojik gelişim mekanizması nedir?",
                    "answer": "Skuamöz metaplazi sürecinde çoğalan yassı epitelin endoservikal bezlerin (kriptaların) ağzını tıkaması ve lümende mukusun hapsolarak kistik dilatasyon yapmasıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Servisit ve Naboth Kistleri",
                    "items": [
                        {"text": "Chlamydia trachomatis en sık karşılaşılan servisit patojenlerinden biridir.", "isLie": False, "explanation": "Doğru. Klamidya primer bakteriyel etkendir."},
                        {"text": "Naboth kistleri endoservikal bez ağızlarının tıkanmasıyla oluşan mukus kistleridir.", "isLie": False, "explanation": "Doğru. Selim retansiyon kistleridir."},
                        {"text": "Naboth kistleri klinik olarak tamamen selimdir ve kansere dönüşmez.", "isLie": False, "explanation": "Doğru. Malign potansiyelleri yoktur."},
                        {"text": "Naboth kistleri daima yüksek dereceli malign sarkomların lenfatik metastazıdır.", "isLie": True, "explanation": "Tuzak! Naboth kisti sarkom veya metastaz değil, fizyolojik/reaktif selim bir retansiyon kistidir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servikste izlenen Naboth kistleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Skuamöz metaplazinin endoservikal bez ağızlarını tıkaması sonucu gelişen tamamen selim mukus retansiyon kistleridir",
                            "isCorrect": True,
                            "explanation": "Naboth kistlerinin patolojideki kesin mekanizması ve klinik önemi budur."
                        },
                        {
                            "key": "B",
                            "text": "Acil cerrahi radikal histerektomi gerektiren ölümcül bir karsinomdur",
                            "isCorrect": False,
                            "explanation": "Naboth kistleri selimdir, cerrahi gerektirmez."
                        },
                        {
                            "key": "C",
                            "text": "Yalnızca intrauterin dönemde fetüste görülen bir nöral anomalidir",
                            "isCorrect": False,
                            "explanation": "Erişkin kadın serviksinde son derece sık izlenir."
                        },
                        {
                            "key": "D",
                            "text": "Kistler içinde daima yüksek hızda replike olan kuduza benzer virüsler bulunur",
                            "isCorrect": False,
                            "explanation": "İçeriği berrak steril mukustur."
                        }
                    ]
                }
            ]
        },
        # S39
        {
            "slideNumber": 39,
            "title": "Servikal Skuamöz Karsinogenez ve Yüksek Riskli HPV",
            "subtitle": "E6/E7 onkoproteinleri, p53 ve pRb inaktivasyonu, genomik instabilite",
            "clinicalFocus": "Moleküler Onkoloji",
            "content": "Servikal skuamöz hücreli karsinom, dünya genelinde kadınlarda en sık görülen ve gelişmekte olan ülkelerde yüksek mortaliteye sahip malignitelerden biridir. Patogenezinde yüksek onkojenik riskli HPV enfeksiyonu anahtar rol oynar.\n\n- **Yüksek Riskli HPV Tipleri:** Servikal kanserlerin %70'inden fazlasından **HPV tip 16 ve 18** sorumludur (diğer yüksek riskli tipler: 31, 33, 45, 52, 58).\n- **Viral Onkoproteinlerin Etkisi:**\n  * **E6 Onkoproteini:** p53 tümör baskılayıcı proteinine bağlanarak onu ubikuitin-proteazom yolağıyla yıkar; DNA hasar kontrolü ve apoptoz mekanizması çöker.\n  * **E7 Onkoproteini:** Retinoblastom (pRb) proteinine bağlanarak E2F transkripsiyon faktörünü serbest bırakır; hücre kontrolsüz biçimde G1/S fazına geçerek çoğalır.\n- **Genomik İnstabilite:** Viral DNA konakçı genomuna entegre olduğunda E2 gen repressörü kaybolur; kontrolsüz E6/E7 üretimi malign transformasyona yol açar.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] HPV E6 proteini p53'ü inhibe ederken; HPV E7 proteini pRb'yi inhibe eder. Bu çifte tümör baskılayıcı kaybı servikal karsinogenezin moleküler motorudur.",
            "synthesisNarrative": "Servikal skuamöz hücreli karsinom, dünya genelinde kadınlarda en sık görülen ve gelişmekte olan ülkelerde yüksek mortaliteye sahip malignitelerden biridir. Patogenezinde yüksek onkojenik riskli HPV enfeksiyonu anahtar rol oynar.\n\n- **Yüksek Riskli HPV Tipleri:** Servikal kanserlerin %70'inden fazlasından **HPV tip 16 ve 18** sorumludur (diğer yüksek riskli tipler: 31, 33, 45, 52, 58).\n- **Viral Onkoproteinlerin Etkisi:**\n  * **E6 Onkoproteini:** p53 tümör baskılayıcı proteinine bağlanarak onu ubikuitin-proteazom yolağıyla yıkar; DNA hasar kontrolü ve apoptoz mekanizması çöker.\n  * **E7 Onkoproteini:** Retinoblastom (pRb) proteinine bağlanarak E2F transkripsiyon faktörünü serbest bırakır; hücre kontrolsüz biçimde G1/S fazına geçerek çoğalır.\n- **Genomik İnstabilite:** Viral DNA konakçı genomuna entegre olduğunda E2 gen repressörü kaybolur; kontrolsüz E6/E7 üretimi malign transformasyona yol açar.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] HPV E6 proteini p53'ü inhibe ederken; HPV E7 proteini pRb'yi inhibe eder. Bu çifte tümör baskılayıcı kaybı servikal karsinogenezin moleküler motorudur.",
            "bulletPoints": [
                "HPV tip 16 ve 18 servikal kanserlerin temel nedenidir.",
                "E6 onkoproteini p53'ü yıkar; apoptozu engeller.",
                "E7 onkoproteini pRb'yi bağlar; hücre döngüsünü kontrolsüz hızlandırır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Human Papilloma Virus E6 onkoproteini p53 tümör baskılayıcı proteinini parçalayarak apoptozu engeller.",
                    "maskedTerm": "p53",
                    "hint": "Genomun koruyucusu olarak bilinen kilit tümör baskılayıcı protein"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "HPV Viral Onkoproteinleri ve Hücresel Hedefleri",
                    "tableHeaders": ["Onkoprotein", "Hücresel Hedef", "Biyolojik Sonuç"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Viral E6", "isMasked": False},
                                {"text": "p53 proteini", "isMasked": True, "hint": "apoptoz yöneticisi protein"},
                                {"text": "Proteazomal yıkım ve apoptoz kaybı", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Viral E7", "isMasked": False},
                                {"text": "pRb (Retinoblastom proteini)", "isMasked": False},
                                {"text": "E2F salınımı ve kontrolsüz S fazı geçişi", "isMasked": True, "hint": "hücre siklusu freninin kalkması"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Moleküler Karsinogenez Zinciri",
                    "steps": [
                        "1. Entegrasyon: Yüksek riskli HPV-16 DNA'sı konakçı serviks hücresi kromozomuna entegre olur.",
                        "2. Onkoprotein Artışı: E6 ve E7 viral genleri yüksek düzeyde sentezlenmeye başlar.",
                        "3. Çifte Baskılama: E6 p53'ü inaktive ederken E7 pRb'yi işlevsiz kılar.",
                        "4. Malign Proliferasyon: Mutasyonlar onarılamaz, genomik instabilite artar ve karsinom gelişir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Yüksek riskli HPV'nin E6 ve E7 onkoproteinleri insan hücre döngüsünü kontrol eden hangi iki temel proteini inaktive eder?",
                    "answer": "E6 onkoproteini p53 proteinini; E7 onkoproteini ise pRb (Retinoblastom) proteinini inaktive eder."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "HPV ve Servikal Moleküler Karsinogenez",
                    "items": [
                        {"text": "Yüksek riskli HPV tip 16 ve 18 servikal kanserlerin en sık etkenidir.", "isLie": False, "explanation": "Doğru. Olguların %70'inden fazlasından sorumludurlar."},
                        {"text": "Viral E6 proteini p53 yıkımına yol açarak apoptozu engeller.", "isLie": False, "explanation": "Doğru. E6 p53'ü hedefler."},
                        {"text": "Viral E7 proteini pRb'ye bağlanarak hücre döngüsünün frenini kaldırır.", "isLie": False, "explanation": "Doğru. E7 pRb-E2F eksenini bozar."},
                        {"text": "HPV virüsü hücrede p53 ve pRb proteinlerini 100 kat artırarak kanseri önler.", "isLie": True, "explanation": "Tuzak! Tam aksine bu koruyucu proteinleri yıkarak ve inaktive ederek kanser gelişimine yol açar."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Human Papilloma Virus'ün (HPV) servikal karsinogenezdeki moleküler mekanizması ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Viral E6 proteini p53'ü yıkar, viral E7 proteini ise pRb'yi bağlayarak hücre döngüsü kontrolünü bozar",
                            "isCorrect": True,
                            "explanation": "Bu iki mekanizma HPV onkogenezinin temel moleküler kuralıdır."
                        },
                        {
                            "key": "B",
                            "text": "E6 proteini yalnızca kalsiyum kanallarını bloke ederek kas krampı yapar",
                            "isCorrect": False,
                            "explanation": "E6 p53 tümör baskılayıcısını inaktive eder."
                        },
                        {
                            "key": "C",
                            "text": "HPV enfeksiyonu hücrenin DNA onarım mekanizmalarını 10 kat güçlendirir",
                            "isCorrect": False,
                            "explanation": "DNA onarımını bozar ve mutasyon birikimine yol açar."
                        },
                        {
                            "key": "D",
                            "text": "Servikal karsinomda virüsün hiçbir rolü yoktur, tek neden kalsiyum eksikliğidir",
                            "isCorrect": False,
                            "explanation": "Serviks kanserinin neredeyse %100'ünde yüksek riskli HPV gösterilir."
                        }
                    ]
                }
            ]
        },
        # S40
        {
            "slideNumber": 40,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 4] Vajinal ve Servikal Onkolojiye Geçiş",
            "subtitle": "31-39. adımların histopatolojik sentezi, prekanseröz evreler ve HPV karsinogenezi",
            "clinicalFocus": "Bölüm 4 Özeti ve Pekiştirme",
            "content": "Bu dördüncü kontrol noktasında vajinal karsinomları, pediatrik rabdomiyosarkomu ve servikal karsinogenezin temellerini sentezliyoruz:\n\n- **Vajinal Karsinom ve VAIN:** Vajinal kanserlerin %90'ı SCC'dir. En büyük risk faktörü önceki serviks veya vulva karsinomu öyküsüdür; tümör en sık üst vajina arka duvarına yerleşir. Üst vajina iliak lenf nodlarına, alt vajina inguinal nodlara drene olur.\n- **Sarkoma Botryoides:** 5 yaşından küçük çocuklarda vajinadan sarkan üzüm salkımı benzeri kitlelerdir; embriyonel rabdomiyoblastlardan köken alır, kambiyum katmanı ve desmin/miyogenin (+) çizgili kas diferansiasyonu gösterir.\n- **Serviks Histolojisi ve Transformasyon Zonu:** Ektoserviks çok katlı yassı, endoserviks tek katlı kolumnar epitellidir. İkisinin karşılaştığı ve skuamöz metaplazinin geliştiği transformasyon zonu karsinogenezin ana odağıdır. Endoservikal kripta tıkanması selim Naboth kistlerini doğurur.\n- **HPV Onkogenezi:** HPV E6 p53'ü yıkar; HPV E7 pRb'yi bağlar.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Vajina SCC = üst arka duvar + geçirilmiş serviks Ca riski. Sarkoma botryoides = <5 yaş + üzüm salkımı. HPV E6 = p53 yıkımı; E7 = pRb inaktivasyonu.",
            "synthesisNarrative": "Bu dördüncü kontrol noktasında vajinal karsinomları, pediatrik rabdomiyosarkomu ve servikal karsinogenezin temellerini sentezliyoruz:\n\n- **Vajinal Karsinom ve VAIN:** Vajinal kanserlerin %90'ı SCC'dir. En büyük risk faktörü önceki serviks veya vulva karsinomu öyküsüdür; tümör en sık üst vajina arka duvarına yerleşir. Üst vajina iliak lenf nodlarına, alt vajina inguinal nodlara drene olur.\n- **Sarkoma Botryoides:** 5 yaşından küçük çocuklarda vajinadan sarkan üzüm salkımı benzeri kitlelerdir; embriyonel rabdomiyoblastlardan köken alır, kambiyum katmanı ve desmin/miyogenin (+) çizgili kas diferansiasyonu gösterir.\n- **Serviks Histolojisi ve Transformasyon Zonu:** Ektoserviks çok katlı yassı, endoserviks tek katlı kolumnar epitellidir. İkisinin karşılaştığı ve skuamöz metaplazinin geliştiği transformasyon zonu karsinogenezin ana odağıdır. Endoservikal kripta tıkanması selim Naboth kistlerini doğurur.\n- **HPV Onkogenezi:** HPV E6 p53'ü yıkar; HPV E7 pRb'yi bağlar.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Vajina SCC = üst arka duvar + geçirilmiş serviks Ca riski. Sarkoma botryoides = <5 yaş + üzüm salkımı. HPV E6 = p53 yıkımı; E7 = pRb inaktivasyonu.",
            "bulletPoints": [
                "Vajina SCC: En sık üst arka duvar, önceki serviks Ca riski, iliak lenfatik tutulum.",
                "Sarkoma botryoides: <5 yaş kız çocuk, üzüm salkımı kitle, desmin/miyogenin(+).",
                "Transformasyon zonu: Skuamöz metaplazi sahası ve kanserin beşiğidir.",
                "HPV E6 p53'ü, E7 pRb'yi yıkarak karsinogenezi tetikler."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Sarkoma botryoides embriyonel rabdomiyoblastlardan köken alırken serviks kanserinde HPV E6 proteini p53 tümör baskılayıcısını inaktive eder.",
                    "maskedTerm": "rabdomiyoblastlardan",
                    "hint": "Çizgili kas diferansiasyonu gösteren embriyonel malign hücreler"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bölüm 4 Kilit Onkolojik Antiteler Sentezi",
                    "tableHeaders": ["Tümör / Yapı", "Yaş Grubu / Yerleşim", "Kritik Patolojik Özellik"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Vajinal Skuamöz Karsinom", "isMasked": False},
                                {"text": "İleri yaş / Üst vajina arka duvarı", "isMasked": True, "hint": "en sık anatomik yerleşim"},
                                {"text": "Geçirilmiş serviks Ca riski, iliak lenf nodu drenajı", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Sarkoma Botryoides", "isMasked": False},
                                {"text": "<5 yaş kız çocukları / Vajina lümeni", "isMasked": False},
                                {"text": "Üzüm salkımı kitle, kambiyum zonu, desmin(+)", "isMasked": True, "hint": "pediatrik kas sarkomu bulgusu"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Serviks Karsinomu", "isMasked": False},
                                {"text": "Transformasyon zonu (dönüşüm zonu)", "isMasked": False},
                                {"text": "Yüksek riskli HPV (E6 p53'ü, E7 pRb'yi yıkar)", "isMasked": True, "hint": "viral moleküler onkogenez"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Bölüm 4 Onkoloji Zinciri",
                    "steps": [
                        "1. Vajinal SCC: Önceki serviks Ca zemininde üst arka duvarda karsinom ve iliak tutulum gelişir.",
                        "2. Pediatrik Sarkom: <5 yaş çocukta mezenkimden sarkan üzüm salkımı botriyoid tümör ürer.",
                        "3. Servikal Epitel: Transformasyon zonunda metaplastik hücreler asidik ortamda şekillenir.",
                        "4. Moleküler Onkogenez: HPV E6 ve E7 p53/pRb'yi devre dışı bırakarak karsinomu başlatır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bölüm 4 kapsamında işlenen tümörlerden hangisi çizgili kas diferansiasyonu gösteren bir pediatrik yumuşak doku sarkomudur?",
                    "answer": "Embriyonel rabdomiyosarkom (Sarkoma Botryoides); 5 yaş altı çocuklarda vajinadan sarkan üzüm salkımı kitlelerle karakterizedir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Bölüm 4 Genel Tekrar",
                    "items": [
                        {"text": "Vajinal skuamöz hücreli karsinom en sık üst vajinanın arka duvarında yerleşir.", "isLie": False, "explanation": "Doğru. En sık anatomik lokalizasyondur."},
                        {"text": "Sarkoma botryoides 5 yaşından küçük çocuklarda üzüm salkımı kitleler yapar.", "isLie": False, "explanation": "Doğru. Klasik pediatrik tablodur."},
                        {"text": "HPV E6 proteini p53'ü, E7 proteini ise pRb'yi inaktive eder.", "isLie": False, "explanation": "Doğru. Onkogenezin moleküler motorudur."},
                        {"text": "Naboth kistleri yüksek dereceli metastatik anaplastik lenfomalardır.", "isLie": True, "explanation": "Tuzak! Naboth kistleri metaplaziye bağlı bez ağzı tıkanmasıyla oluşan tamamen selim retansiyon kistleridir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Bölüm 4'te özetlenen konularla ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Sarkoma botryoides <5 yaş çocukta üzüm salkımı kitle yapar; HPV E6 p53'ü, E7 ise pRb'yi inaktive eder",
                            "isCorrect": True,
                            "explanation": "Bu sentez cümlesi hem pediatrik sarkomun hem de HPV karsinogenezinin kilit spotlarını doğru özetler."
                        },
                        {
                            "key": "B",
                            "text": "Vajina kanseri en sık 1 yaşındaki erkek çocukların böbreğinde yerleşir",
                            "isCorrect": False,
                            "explanation": "Vajina kadın genital organıdır."
                        },
                        {
                            "key": "C",
                            "text": "Transformasyon zonu hiçbir zaman karsinogenez ile ilişkili değildir",
                            "isCorrect": False,
                            "explanation": "Serviks kanserlerinin neredeyse tamamı transformasyon zonunda başlar."
                        },
                        {
                            "key": "D",
                            "text": "HPV E6 ve E7 proteinleri hücrede DNA mutasyonlarını önleyen aşı maddeleridir",
                            "isCorrect": False,
                            "explanation": "Viral onkoproteinlerdir ve kansere yol açarlar."
                        }
                    ]
                }
            ]
        }
    ]
    return slides

if __name__ == '__main__':
    slides = get_s4_slides()
    print(f'Section 4 created with {len(slides)} slides.')
