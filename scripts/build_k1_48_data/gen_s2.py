import json

def get_s2_slides():
    slides = [
        # S11
        {
            "slideNumber": 11,
            "title": "Skuamöz Hücre Hiperplazisi: Tanım ve Eski Terminoloji",
            "subtitle": "Hiperplastik distrofi, liken simpleks kronikus ve epitel kalınlaşması",
            "clinicalFocus": "Tanım ve Terminoloji",
            "content": "Skuamöz hücre hiperplazisi, vulva skuamöz epitelinin kronik mekanik sürtünme ve kaşımaya karşı geliştirdiği proliferatif ve hiperplastik bir yanıttır. Non-neoplastik epitel bozuklukları spektrumunun ikinci büyük grubunu oluşturur.\n\n- **Eski Terminoloji:** Geçmişte patoloji literatüründe 'hiperplastik distrofi' veya dermatolojide 'liken simpleks kronikus' olarak adlandırılmıştır; güncel uluslararası terminolojide skuamöz hücre hiperplazisi terimi tercih edilir.\n- **Tetikleyici Faktör:** Altta yatan temel mekanizma, başlangıçtaki hafif bir irritasyon veya kaşıntıyı gidermek amacıyla hastanın bölgeyi sürekli ovması ve kaşımasıdır.\n- **Klinik Görünüm:** Liken skleroza benzer şekilde vulvada beyaz renkli lezyonlar (lökoplaki) şeklinde karşımıza çıkar; ancak lezyonlar atrofik değil, kabarık ve kalındır.\n\n> [!NOTE]\n> Skuamöz hücre hiperplazisi liken skleroz gibi parşömen kağıdı şeklinde incelme yapmaz; tam tersine deride kalınlaşma ve kabalaşma ile karakterizedir.",
            "synthesisNarrative": "Skuamöz hücre hiperplazisi, vulva skuamöz epitelinin kronik mekanik sürtünme ve kaşımaya karşı geliştirdiği proliferatif ve hiperplastik bir yanıttır. Non-neoplastik epitel bozuklukları spektrumunun ikinci büyük grubunu oluşturur.\n\n- **Eski Terminoloji:** Geçmişte patoloji literatüründe 'hiperplastik distrofi' veya dermatolojide 'liken simpleks kronikus' olarak adlandırılmıştır; güncel uluslararası terminolojide skuamöz hücre hiperplazisi terimi tercih edilir.\n- **Tetikleyici Faktör:** Altta yatan temel mekanizma, başlangıçtaki hafif bir irritasyon veya kaşıntıyı gidermek amacıyla hastanın bölgeyi sürekli ovması ve kaşımasıdır.\n- **Klinik Görünüm:** Liken skleroza benzer şekilde vulvada beyaz renkli lezyonlar (lökoplaki) şeklinde karşımıza çıkar; ancak lezyonlar atrofik değil, kabarık ve kalındır.\n\n> [!NOTE]\n> Skuamöz hücre hiperplazisi liken skleroz gibi parşömen kağıdı şeklinde incelme yapmaz; tam tersine deride kalınlaşma ve kabalaşma ile karakterizedir.",
            "bulletPoints": [
                "Eski adı hiperplastik distrofi veya liken simpleks kronikustur.",
                "Kronik ovma ve kaşıma sonucu reaktif olarak gelişir.",
                "Lökoplaki görünümü verir ancak doku atrofik değil kalındır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Skuamöz hücre hiperplazisinin patolojideki eski adlandırması hiperplastik distrofi olarak bilinir.",
                    "maskedTerm": "hiperplastik distrofi",
                    "hint": "Eski sınıflamadaki distrofik adlandırma"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Skuamöz Hücre Hiperplazisi Terminolojisi",
                    "tableHeaders": ["Dönem / Disiplin", "Kullanılan Terim", "Biyolojik Anlam"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Güncel Patoloji", "isMasked": False},
                                {"text": "Skuamöz hücre hiperplazisi", "isMasked": False},
                                {"text": "reaktif epitel kalınlaşması", "isMasked": True, "hint": "hücresel hiperplazi yanıtı"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Dermatoloji / Eski", "isMasked": False},
                                {"text": "Liken simpleks kronikus", "isMasked": True, "hint": "kronik kaşıntı dermatozu"},
                                {"text": "Kaşımaya bağlı nörodermatit", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Kaşımadan Epitel Hiperplazisine",
                    "steps": [
                        "1. Kaşıntı: Vulvada hafif bir irritasyon veya alerjen kaşıntıyı tetikler.",
                        "2. Mekanik Sürtünme: Hasta lezyonu kronik olarak ovar ve şiddetle kaşır.",
                        "3. Proliferatif Yanıt: Sürekli sürtünme bazal tabakadaki keratinosit bölünmesini uyarır.",
                        "4. Hiperplazi: Epidermis tabakası kalınlaşarak lökoplakik plak formunu alır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Skuamöz hücre hiperplazisinin eski patolojik ve dermatolojik adları nelerdir?",
                    "answer": "Eski patolojik adı 'hiperplastik distrofi', dermatolojideki adı ise 'liken simpleks kronikus'tur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Skuamöz Hücre Hiperplazisi Temelleri",
                    "items": [
                        {"text": "Skuamöz hücre hiperplazisi kronik kaşıma ve ovmaya reaktif bir yanıttır.", "isLie": False, "explanation": "Doğru. Mekanik sürtünme temel tetikleyicidir."},
                        {"text": "Eski literatürde hiperplastik distrofi veya liken simpleks kronikus denilmiştir.", "isLie": False, "explanation": "Doğru. Terminolojik geçmişi bu şekildedir."},
                        {"text": "Klinikte lökoplaki (beyaz plak) şeklinde lezyonlar oluşturabilir.", "isLie": False, "explanation": "Doğru. Kalınlaşan keratin tabakası beyaz görünüm verir."},
                        {"text": "Skuamöz hücre hiperplazisi doğrudan embriyonel nöral krest tümörüdür.", "isLie": True, "explanation": "Tuzak! Skuamöz hücre hiperplazisi bir tümör değil, epitelin selim reaktif kalınlaşmasıdır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Skuamöz hücre hiperplazisinin etyopatogenezi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Şiddetli kaşıntıyı gidermek için yapılan kronik ovma ve kaşıma sonucu reaktif gelişir",
                            "isCorrect": True,
                            "explanation": "Mekanik kaşıma epitel proliferasyonunu uyararak hiperplaziye yol açar."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca Epstein-Barr virüsü taşıyan hastalarda gelişen genetik bir sarkomdur",
                            "isCorrect": False,
                            "explanation": "Virüsle veya sarkomla ilişkisi yoktur; reaktif selim bir tablodur."
                        },
                        {
                            "key": "C",
                            "text": "Epidermisin tamamen eriyerek yok olmasıyla seyreden atrofik bir lezyondur",
                            "isCorrect": False,
                            "explanation": "Epidermis incelmez, tam aksine belirgin biçimde kalınlaşır."
                        },
                        {
                            "key": "D",
                            "text": "Liken sklerozdan farklı olarak hiçbir zaman beyaz plak (lökoplaki) yapmaz",
                            "isCorrect": False,
                            "explanation": "Hiperkeratoz nedeniyle klinik olarak tipik lökoplaki görünümü oluşturur."
                        }
                    ]
                }
            ]
        },
        # S12
        {
            "slideNumber": 12,
            "title": "Skuamöz Hücre Hiperplazisi: Akantoz, Hiperkeratoz ve Atipi Yokluğu",
            "subtitle": "Histopatolojik mimari, artmış mitoz ve sitolojik selimlik",
            "clinicalFocus": "Histopatoloji ve Atipi Ayrımı",
            "content": "Skuamöz hücre hiperplazisinin kesin tanısı biyopside karakteristik histopatolojik bulguların gösterilmesi ve en önemlisi sitolojik atipinin bulunmadığının kanıtlanması ile konur.\n\n- **Epidermal Kalınlaşma (Akantoz):** Çok katlı yassı epitelin stratum spinosum tabakası belirgin biçimde genişlemiştir (akantoz); rete çıkıntıları uzamış ve genişlemiştir.\n- **Hiperkeratoz:** Epitel yüzeyinde kalınlaşmış bir keratin tabakası birikir; beyaz lökoplaki görünümünün asıl nedeni bu keratinize tabakadır.\n- **Mitoz ve Atipi:** Epitelin bazal ve parabazal katmanlarında artmış mitotik aktivite görülebilir; ancak mitozlar normal morfolojidedir ve ==KESİNLİKLE SİTOLOJİK ATİPİ YOKTUR==.\n- **Dermal İnfiltrat:** Dermiste değişken yoğunlukta lenfositik inflamatuvar infiltrasyon izlenebilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Skuamöz hücre hiperplazisinde akantoz ve hiperkeratoz vardır; mitotik aktivite artabilir ancak sitolojik atipi ASLA görülmez. Atipi saptanırsa tablo artık hiperplazi değil, vulvar intraepitelyal neoplazidir (VIN).",
            "synthesisNarrative": "Skuamöz hücre hiperplazisinin kesin tanısı biyopside karakteristik histopatolojik bulguların gösterilmesi ve en önemlisi sitolojik atipinin bulunmadığının kanıtlanması ile konur.\n\n- **Epidermal Kalınlaşma (Akantoz):** Çok katlı yassı epitelin stratum spinosum tabakası belirgin biçimde genişlemiştir (akantoz); rete çıkıntıları uzamış ve genişlemiştir.\n- **Hiperkeratoz:** Epitel yüzeyinde kalınlaşmış bir keratin tabakası birikir; beyaz lökoplaki görünümünün asıl nedeni bu keratinize tabakadır.\n- **Mitoz ve Atipi:** Epitelin bazal ve parabazal katmanlarında artmış mitotik aktivite görülebilir; ancak mitozlar normal morfolojidedir ve ==KESİNLİKLE SİTOLOJİK ATİPİ YOKTUR==.\n- **Dermal İnfiltrat:** Dermiste değişken yoğunlukta lenfositik inflamatuvar infiltrasyon izlenebilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Skuamöz hücre hiperplazisinde akantoz ve hiperkeratoz vardır; mitotik aktivite artabilir ancak sitolojik atipi ASLA görülmez. Atipi saptanırsa tablo artık hiperplazi değil, vulvar intraepitelyal neoplazidir (VIN).",
            "bulletPoints": [
                "Epidermiste akantoz ve hiperkeratoz belirgindir.",
                "Mitotik aktivite artabilir ancak sitolojik atipi kesinlikle yoktur.",
                "Atipi varlığı VIN veya malignite lehinedir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Skuamöz hücre hiperplazisinde mitotik aktivite artmış olabilir ancak epitelde sitolojik atipi yoktur.",
                    "maskedTerm": "sitolojik atipi",
                    "hint": "Neoplaziden ayıran nükleer polimorfizm ve anaplazinin bulunmaması durumu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Skuamöz Hiperplazi Histopatolojik Kriterleri",
                    "tableHeaders": ["Histolojik Parametre", "Bulgu", "Klinik Yorum"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Stratum spinosum", "isMasked": False},
                                {"text": "Belirgin akantoz (kalınlaşma)", "isMasked": True, "hint": "hücre katmanı artışı"},
                                {"text": "Genişlemiş ve uzamış rete çıkıntıları", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Nükleer Morfoloji", "isMasked": False},
                                {"text": "Düzenli nükleus, atipi yok", "isMasked": False},
                                {"text": "Selim reaktif sürecin kesin kanıtı", "isMasked": True, "hint": "maligniteden ayıran kilit nokta"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Histolojik Tabakalaşma Zinciri",
                    "steps": [
                        "1. Kaşıma Uyarısı: Keratinositler büyüme faktörleri salgılayarak bazal hücreleri uyarır.",
                        "2. Akantoz: Dikenli hücre tabakası kalınlaşır ve rete çıkıntıları derinleşir.",
                        "3. Hiperkeratoz: Yüzeyde aşırı keratin üretilerek beyaz koruyucu kabuk oluşturulur.",
                        "4. Histopatolojik Ayrım: Mikroskop altında sitolojik atipinin olmaması selim tanıyı kesinleştirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Skuamöz hücre hiperplazisini intraepitelyal neoplazilerden (VIN) ayıran en kritik mikroskobik özellik nedir?",
                    "answer": "Skuamöz hücre hiperplazisinde mitotik aktivite bulunabilse bile kesinlikle sitolojik atipi (nükleer pleomorfizm, hiperkromazi, polarite kaybı) izlenmez."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Skuamöz Hücre Hiperplazisi Histolojisi",
                    "items": [
                        {"text": "Epidermiste belirgin akantoz ve yüzeyde hiperkeratoz mevcuttur.", "isLie": False, "explanation": "Doğru. Doku kalınlaşması ve aşırı keratin karakteristiktir."},
                        {"text": "Epitel katmanlarında artmış mitotik aktivite görülebilir.", "isLie": False, "explanation": "Doğru. Reaktif proliferasyona bağlı mitoz artabilir."},
                        {"text": "Skuamöz hücre hiperplazisinde sitolojik atipi kesinlikle bulunmaz.", "isLie": False, "explanation": "Doğru. Sitolojik selimlik temel kuraldır."},
                        {"text": "Skuamöz hücre hiperplazisinde tüm katlarda yaygın pleomorfik atipik karsinom hücreleri izlenir.", "isLie": True, "explanation": "Tuzak! Atipik hücreler varsa lezyon hiperplazi değil, karsinoma in situdur (VIN)."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Skuamöz hücre hiperplazisinin mikroskobik incelemesinde aşağıdaki bulgulardan hangisi KESİNLİKLE BEKLENMEZ?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Belirgin sitolojik atipi ve anormal pleomorfik nükleuslar",
                            "isCorrect": True,
                            "explanation": "Skuamöz hücre hiperplazisinde sitolojik atipi yoktur; atipi varsa neoplazi düşünülür."
                        },
                        {
                            "key": "B",
                            "text": "Stratum spinosum tabakasında kalınlaşma (akantoz)",
                            "isCorrect": False,
                            "explanation": "Akantoz skuamöz hiperplazinin ana histopatolojik bulgusudur."
                        },
                        {
                            "key": "C",
                            "text": "Yüzeyde kalınlaşmış keratin tabakası (hiperkeratoz)",
                            "isCorrect": False,
                            "explanation": "Hiperkeratoz beyaz plak görünümünün morfolojik temelidir."
                        },
                        {
                            "key": "D",
                            "text": "Rete çıkıntılarında uzama ve genişleme",
                            "isCorrect": False,
                            "explanation": "Akantoza bağlı olarak rete çıkıntıları belirginleşir."
                        }
                    ]
                }
            ]
        },
        # S13
        {
            "slideNumber": 13,
            "title": "Liken Skleroz ve Skuamöz Hücre Hiperplazisi Karşılaştırması",
            "subtitle": "Epidermis kalınlığı, dermal kolajen yapısı ve klinik ayırıcı tanı",
            "clinicalFocus": "Ayırıcı Tanı",
            "content": "Vulvanın iki temel non-neoplastik epitel bozukluğu olan liken skleroz ve skuamöz hücre hiperplazisi, klinik olarak benzer lökoplaki plakları oluştursa da mikroskobik mimarileri birbirine tamamen zıttır.\n\n- **Epidermal Yanıt:** Liken sklerozda epidermis ileri derecede incelmiş ve atrofiktir; rete çıkıntıları silinmiştir. Skuamöz hücre hiperplazisinde ise epidermis kalınlaşmıştır (akantoz) ve rete çıkıntıları uzamıştır.\n- **Dermal Değişiklik:** Liken sklerozda yüzeyel dermiste hücresiz, homojen, soluk camsı bir skleroz/fibrozis bandı bulunur. Skuamöz hiperplazide ise homojen skleroz bandı yoktur, yalnızca değişken lenfositik infiltrat izlenir.\n- **Kanser Riski:** Liken skleroz zemininde vulvar karsinom riski hafifçe artmıştır; skuamöz hiperplazide ise atipi olmadığı sürece malignite riski artışı bildirilmemiştir.\n\n> [!IMPORTANT]\n> [KRİTİK UYARI] Tek başına klinik muayene ile bu iki antiteyi ayırt etmek imkansızdır; ayırıcı tanı mutlak surette biyopsi ile yapılır.",
            "synthesisNarrative": "Vulvanın iki temel non-neoplastik epitel bozukluğu olan liken skleroz ve skuamöz hücre hiperplazisi, klinik olarak benzer lökoplaki plakları oluştursa da mikroskobik mimarileri birbirine tamamen zıttır.\n\n- **Epidermal Yanıt:** Liken sklerozda epidermis ileri derecede incelmiş ve atrofiktir; rete çıkıntıları silinmiştir. Skuamöz hücre hiperplazisinde ise epidermis kalınlaşmıştır (akantoz) ve rete çıkıntıları uzamıştır.\n- **Dermal Değişiklik:** Liken sklerozda yüzeyel dermiste hücresiz, homojen, soluk camsı bir skleroz/fibrozis bandı bulunur. Skuamöz hiperplazide ise homojen skleroz bandı yoktur, yalnızca değişken lenfositik infiltrat izlenir.\n- **Kanser Riski:** Liken skleroz zemininde vulvar karsinom riski hafifçe artmıştır; skuamöz hiperplazide ise atipi olmadığı sürece malignite riski artışı bildirilmemiştir.\n\n> [!IMPORTANT]\n> [KRİTİK UYARI] Tek başına klinik muayene ile bu iki antiteyi ayırt etmek imkansızdır; ayırıcı tanı mutlak surette biyopsi ile yapılır.",
            "bulletPoints": [
                "Liken sklerozda epidermis incelir; skuamöz hiperplazide kalınlaşır.",
                "Liken sklerozda dermal homojen fibrozis bandı patognomoniktir.",
                "İkisinin kesin ayrımı için biyopsi şarttır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Liken sklerozda epidermis belirgin biçimde incelirken skuamöz hücre hiperplazisinde akantoz ile kalınlaşır.",
                    "maskedTerm": "incelirken",
                    "hint": "Liken sklerozdaki epitelyal atrofi yönü"
                },
                {
                    "type": "before_after_slider",
                    "leftTitle": "Liken Skleroz",
                    "rightTitle": "Skuamöz Hücre Hiperplazisi",
                    "leftPoints": [
                        "Epidermiste belirgin incelme ve atrofi izlenir.",
                        "Rete çıkıntıları tamamen kaybolmuş ve düzleşmiştir.",
                        "Yüzeyel dermiste hücresiz homojen skleroz bandı vardır.",
                        "Vulvar skuamöz karsinom riski hafifçe artmıştır."
                    ],
                    "rightPoints": [
                        "Epidermiste belirgin akantoz ve kalınlaşma izlenir.",
                        "Rete çıkıntıları derinleşmiş ve uzamıştır.",
                        "Dermiste homojen skleroz bandı bulunmaz.",
                        "Sitolojik atipi yoksa malignite riski artışı beklenmez."
                    ]
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Non-Neoplastik Epitel Bozuklukları Karşılaştırması",
                    "tableHeaders": ["Ölçüt", "Liken Skleroz", "Skuamöz Hücre Hiperplazisi"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Epidermis Kalınlığı", "isMasked": False},
                                {"text": "İncelmiş ve atrofik", "isMasked": True, "hint": "azalmış katman kalınlığı"},
                                {"text": "Kalınlaşmış (akantotik)", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Dermal Fibrozis Bandı", "isMasked": False},
                                {"text": "Var (homojen ve aselüler)", "isMasked": False},
                                {"text": "Yok (yalnızca lenfositik infiltrat)", "isMasked": True, "hint": "skleroz zonunun bulunmaması"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Ayırıcı Tanı Algoritması",
                    "steps": [
                        "1. Muayene: Vulvada kaşıntılı beyaz lökoplaki plakları tespit edilir.",
                        "2. Biyopsi: Kesin ayırıcı tanı için lezyondan punch/insizyonel biyopsi alınır.",
                        "3. Mikroskopi: Epitel kalınlığı ve dermal skleroz değerlendirilir.",
                        "4. Karar: Atrofi ve skleroz varsa liken skleroz, akantoz varsa skuamöz hiperplazi tanısı konur."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Liken skleroz ile skuamöz hücre hiperplazisinin epidermisteki en temel zıt morfolojik farkı nedir?",
                    "answer": "Liken sklerozda epidermis belirgin biçimde incelmiş (atrofik) ve rete çıkıntıları silinmişken; skuamöz hücre hiperplazisinde epidermis belirgin biçimde kalınlaşmış (akantotik) ve rete çıkıntıları uzamıştır."
                },
                {
                    "type": "micro_quiz",
                    "question": "Liken skleroz ile skuamöz hücre hiperplazisinin ayırıcı tanısında aşağıdakilerden hangisi LİKEN SKLEROZ lehinedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Epidermiste belirgin incelme, rete çıkıntılarının silinmesi ve yüzeyel dermal homojen skleroz bandı",
                            "isCorrect": True,
                            "explanation": "Bu bulgular liken sklerozun karakteristik histopatolojik özellikleridir."
                        },
                        {
                            "key": "B",
                            "text": "Stratum spinosum tabakasında aşırı genişleme ve akantoz",
                            "isCorrect": False,
                            "explanation": "Akantoz skuamöz hücre hiperplazisinin bulgusudur."
                        },
                        {
                            "key": "C",
                            "text": "Epitel kalınlığının 5 katına çıkması ve dev rete uzantıları",
                            "isCorrect": False,
                            "explanation": "Bu bulgu hiperplaziyi işaret eder; liken sklerozda epitel incelir."
                        },
                        {
                            "key": "D",
                            "text": "Dermiste hiçbir kolajen değişikliği olmaksızın yalnızca granülom görülmesi",
                            "isCorrect": False,
                            "explanation": "Liken sklerozda homojen kollajenöz skleroz temel bulgudur."
                        }
                    ]
                }
            ]
        },
        # S14
        {
            "slideNumber": 14,
            "title": "Vulvada Tümörler: Benign ve Malign Yelpazeye Genel Bakış",
            "subtitle": "Kondilomlar, karsinomlar ve nadir neoplazmlar",
            "clinicalFocus": "Genel Onkolojik Sınıflama",
            "content": "Vulva tümörleri, histogenetik kökenlerine ve biyolojik davranışlarına göre selim (benign) ve habis (malign) lezyonlar olarak iki temel grupta incelenir.\n\n- **Benign Tümörler:** En yaygın karşılaşılan selim vulva lezyonları siğil benzeri ekzofitik kitleler oluşturan **kondilomlardır** (özellikle kondiloma akuminatum). Bunun yanında hemanjiyomlar, lipomlar ve hidradenomlar da izlenebilir.\n- **Malign Tümörler:** Vulvanın primer malign neoplazmlarının yaklaşık **%90'ını skuamöz hücreli karsinom (SCC)** oluşturur. Geriye kalan nadir %10'luk dilimde adenokarsinomlar, bazal hücreli karsinomlar ve melanomlar yer alır.\n- **Prekanseröz Basamak:** İnvaziv karsinomların büyük kısmı aniden ortaya çıkmaz; öncesinde intraepitelyal neoplazi evrelerinden (VIN/dVIN) geçer.\n\n> [!NOTE]\n> Vulva maligniteleri tüm kadın genital kanserlerinin yalnızca %3'ünü oluştursa da ileri evrelerde lenfatik metastaz potansiyeli yüksektir.",
            "synthesisNarrative": "Vulva tümörleri, histogenetik kökenlerine ve biyolojik davranışlarına göre selim (benign) ve habis (malign) lezyonlar olarak iki temel grupta incelenir.\n\n- **Benign Tümörler:** En yaygın karşılaşılan selim vulva lezyonları siğil benzeri ekzofitik kitleler oluşturan **kondilomlardır** (özellikle kondiloma akuminatum). Bunun yanında hemanjiyomlar, lipomlar ve hidradenomlar da izlenebilir.\n- **Malign Tümörler:** Vulvanın primer malign neoplazmlarının yaklaşık **%90'ını skuamöz hücreli karsinom (SCC)** oluşturur. Geriye kalan nadir %10'luk dilimde adenokarsinomlar, bazal hücreli karsinomlar ve melanomlar yer alır.\n- **Prekanseröz Basamak:** İnvaziv karsinomların büyük kısmı aniden ortaya çıkmaz; öncesinde intraepitelyal neoplazi evrelerinden (VIN/dVIN) geçer.\n\n> [!NOTE]\n> Vulva maligniteleri tüm kadın genital kanserlerinin yalnızca %3'ünü oluştursa da ileri evrelerde lenfatik metastaz potansiyeli yüksektir.",
            "bulletPoints": [
                "En sık benign tümör kondilomlardır (kondiloma akuminatum).",
                "Malignitelerin yaklaşık %90'ı skuamöz hücreli karsinomdur (SCC).",
                "Malign lezyonlar öncesinde VIN aşamasından geçer."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vulvanın primer malign tümörlerinin yaklaşık yüzde doksanını skuamöz hücreli karsinom oluşturur.",
                    "maskedTerm": "yüzde doksanını",
                    "hint": "Skuamöz hücreli karsinomun tüm vulva kanserleri içindeki ezici oranı"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulva Tümörleri Sınıflandırması",
                    "tableHeaders": ["Biyolojik Davranış", "En Sık Lezyon", "Histogenetik Tip"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Benign (Selim)", "isMasked": False},
                                {"text": "Kondiloma akuminatum", "isMasked": True, "hint": "HPV ilişkili genital siğil"},
                                {"text": "Skuamöz papillomatöz proliferasyon", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Malign (Habis)", "isMasked": False},
                                {"text": "Skuamöz hücreli karsinom (%90)", "isMasked": False},
                                {"text": "İnvaziv skuamöz epitel karsinomu", "isMasked": True, "hint": "bazal membranı aşan malignite"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Selimden Habise Onkolojik Spektrum",
                    "steps": [
                        "1. Selim Proliferasyon: Düşük riskli HPV ile kondiloma akuminatum gibi selim siğiller oluşur.",
                        "2. Prekanseröz Faz: Yüksek riskli HPV veya kronik distrofi intraepitelyal neoplaziye yol açar.",
                        "3. İnvazyon: Atipik hücreler bazal membranı aşarak dermis ve stromaya invaze olur.",
                        "4. Skuamöz Karsinom: Vulvanın en sık malign tümörü olan invaziv SCC tablosu oturur."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulvanın primer malign neoplazmları arasında en sık görülen histolojik tip hangisidir ve oranı nedir?",
                    "answer": "Skuamöz hücreli karsinomdur (SCC) ve tüm vulva kanserlerinin yaklaşık %90'ını oluşturur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vulva Tümörlerinin Genel Özellikleri",
                    "items": [
                        {"text": "Vulvanın en yaygın selim lezyonları siğil benzeri kondilomlardır.", "isLie": False, "explanation": "Doğru. Kondiloma akuminatum en sık benign kitle lezyonudur."},
                        {"text": "Vulva kanserlerinin yaklaşık %90'ı skuamöz hücreli karsinomdur.", "isLie": False, "explanation": "Doğru. Skuamöz karsinom ezici çoğunluğu oluşturur."},
                        {"text": "Vulvada adenokarsinom ve bazal hücreli karsinom gibi diğer tipler de nadiren görülebilir.", "isLie": False, "explanation": "Doğru. Kalan %10'luk kısımda bu tümörler yer alır."},
                        {"text": "Vulvanın primer malign tümörlerinin %95'i kıkırdak kaynaklı kondrosarkomdur.", "isLie": True, "explanation": "Tuzak! Vulvada kondrosarkom pratik olarak görülmez; karsinomlar (%90 SCC) hakimdir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulva neoplazmlarının epidemiyolojisi ve histopatolojisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Malign tümörlerin yaklaşık %90'ı skuamöz hücreli karsinomdur ve en sık benign lezyon kondilomdur",
                            "isCorrect": True,
                            "explanation": "Vulva onkolojisinde selim grupta kondilomlar, habis grupta SCC baskındır."
                        },
                        {
                            "key": "B",
                            "text": "Vulvada karsinom gelişimi hiçbir zaman görülmez; yalnızca selim kistler oluşur",
                            "isCorrect": False,
                            "explanation": "Vulvada yaşamı tehdit edebilen invaziv karsinomlar görülür."
                        },
                        {
                            "key": "C",
                            "text": "Tüm kadın genital kanserlerinin %70'ini vulva skuamöz karsinomu oluşturur",
                            "isCorrect": False,
                            "explanation": "Vulva kanserleri tüm jinekolojik kanserlerin yalnızca yaklaşık %3'ünü oluşturur."
                        },
                        {
                            "key": "D",
                            "text": "Vulvanın en sık malign tümörü primer küçük hücreli nöroendokrin karsinomdur",
                            "isCorrect": False,
                            "explanation": "En sık malign tümör skuamöz hücreli karsinomdur."
                        }
                    ]
                }
            ]
        },
        # S15
        {
            "slideNumber": 15,
            "title": "Kondilomlar: Kondiloma Lata ve Kondiloma Akuminatum Ayrımı",
            "subtitle": "Treponema pallidum vs düşük riskli HPV tip 6 ve 11",
            "clinicalFocus": "Kondilom Tipleri ve Ayırıcı Tanı",
            "content": "Kondilomlar anogenital bölgenin cinsel temasla bulaşan siğil benzeri ekzofitik lezyonlarıdır. Tıbbi pratikte iki temel kondilom formu mutlaka birbirinden ayırt edilmelidir:\n\n- **Kondiloma Lata:** Sekonder sifiliz (frengi) evresinde ortaya çıkar. Etkeni spiroket olan **Treponema pallidum**'dur. Lezyonlar geniş tabanlı, düz, hafif kabarık ve oldukça bulaşıcıdır; uygun sifiliz antibiyoterapisi (penisilin) ile tamamen geriler.\n- **Kondiloma Akuminatum:** En yaygın kondilom formudur. Etkeni düşük onkojenik riskli **HPV tip 6 ve 11**'dir. Lezyonlar papiller, karnabahar benzeri ekzofitik, belirgin kabarık veya buruşuk plaklar şeklindedir.\n- **Lokalizasyon:** Anogenital bölgenin her yerinde, perinede ve erkekte peniste eşzamanlı izlenebilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Düz ve geniş tabanlı kondiloma lata sekonder sifiliz (T. pallidum) bulgusudur; papiller karnabahar benzeri kondiloma akuminatum ise düşük riskli HPV (tip 6 ve 11) kaynaklıdır.",
            "synthesisNarrative": "Kondilomlar anogenital bölgenin cinsel temasla bulaşan siğil benzeri ekzofitik lezyonlarıdır. Tıbbi pratikte iki temel kondilom formu mutlaka birbirinden ayırt edilmelidir:\n\n- **Kondiloma Lata:** Sekonder sifiliz (frengi) evresinde ortaya çıkar. Etkeni spiroket olan **Treponema pallidum**'dur. Lezyonlar geniş tabanlı, düz, hafif kabarık ve oldukça bulaşıcıdır; uygun sifiliz antibiyoterapisi (penisilin) ile tamamen geriler.\n- **Kondiloma Akuminatum:** En yaygın kondilom formudur. Etkeni düşük onkojenik riskli **HPV tip 6 ve 11**'dir. Lezyonlar papiller, karnabahar benzeri ekzofitik, belirgin kabarık veya buruşuk plaklar şeklindedir.\n- **Lokalizasyon:** Anogenital bölgenin her yerinde, perinede ve erkekte peniste eşzamanlı izlenebilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Düz ve geniş tabanlı kondiloma lata sekonder sifiliz (T. pallidum) bulgusudur; papiller karnabahar benzeri kondiloma akuminatum ise düşük riskli HPV (tip 6 ve 11) kaynaklıdır.",
            "bulletPoints": [
                "Kondiloma lata sekonder sifilize (T. pallidum) bağlıdır; düz lezyonlardır.",
                "Kondiloma akuminatum düşük riskli HPV tip 6 ve 11 ile oluşur; papillerdir.",
                "Her ikisi de anogenital bölgeye yerleşen cinsel bulaşlı tablolardır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "En yaygın genital siğil tipi olan kondiloma akuminatumun temel etkeni düşük riskli HPV tip 6 ve 11 enfeksiyonudur.",
                    "maskedTerm": "HPV tip 6 ve 11",
                    "hint": "Genital siğillerden sorumlu düşük onkojenik riskli virüs tipleri"
                },
                {
                    "type": "before_after_slider",
                    "leftTitle": "Kondiloma Lata",
                    "rightTitle": "Kondiloma Akuminatum",
                    "leftPoints": [
                        "Sekonder sifiliz evresinde ortaya çıkar.",
                        "Etken spiroket Treponema pallidum'dur.",
                        "Geniş tabanlı, düz ve hafif kabarık lezyonlardır.",
                        "Sifiliz tedavisi (penisilin) ile geriler."
                    ],
                    "rightPoints": [
                        "En yaygın anogenital siğil formudur.",
                        "Etken düşük riskli HPV tip 6 ve 11'dir.",
                        "Papiller, ekzofitik karnabahar benzeri lezyonlardır.",
                        "Lokal ablasyon veya kriyoterapi ile tedavi edilir."
                    ]
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Kondiloma Lata ve Kondiloma Akuminatum Ayırıcı Özellikleri",
                    "tableHeaders": ["Özellik", "Kondiloma Lata", "Kondiloma Akuminatum"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Mikrobiyal Etken", "isMasked": False},
                                {"text": "Treponema pallidum", "isMasked": True, "hint": "sifiliz spiroketi"},
                                {"text": "Düşük riskli HPV (6 ve 11)", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Morfolojik Yapı", "isMasked": False},
                                {"text": "Düz ve geniş tabanlı plak", "isMasked": False},
                                {"text": "Papiller karnabahar benzeri ekzofitik", "isMasked": True, "hint": "parmaksı çıkıntılar"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Kondiloma Akuminatum Gelişim Basamakları",
                    "steps": [
                        "1. Cinsel Bulaş: Düşük riskli HPV tip 6 veya 11 anogenital mikrotravmayla bazal epitele ulaşır.",
                        "2. Replikasyon: Virüs keratinositler içinde çoğalarak hücre siklusunu ve proliferasyonu tetikler.",
                        "3. Papillomatoz: Stromal damarlı korların üzerinde çok katlı yassı epitel kalınlaşır ve dallanır.",
                        "4. Kondilom: Makroskopik olarak karnabahar benzeri ekzofitik lezyonlar vulva yüzeyinde belirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Kondiloma lata ile kondiloma akuminatumun etkenleri ve morfolojik görünümleri arasındaki fark nedir?",
                    "answer": "Kondiloma lata sekonder sifilizin (T. pallidum) etken olduğu düz/geniş lezyonlarken; kondiloma akuminatum HPV tip 6 ve 11 kaynaklı papiller karnabahar benzeri ekzofitik lezyonlardır."
                },
                {
                    "type": "micro_quiz",
                    "question": "Kondilomlar ile ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Kondiloma lata — Sekonder sifiliz (Treponema pallidum) — Düz geniş lezyonlar",
                            "isCorrect": True,
                            "explanation": "Kondiloma lata sekonder sifilizin düz ve son derece bulaşıcı lezyonudur."
                        },
                        {
                            "key": "B",
                            "text": "Kondiloma akuminatum — Yüksek riskli HPV tip 16 — Masif kemik metastazı",
                            "isCorrect": False,
                            "explanation": "Kondiloma akuminatum düşük riskli HPV tip 6 ve 11 ile oluşur ve selimdir."
                        },
                        {
                            "key": "C",
                            "text": "Kondiloma lata — Candida albicans — Derin intraabdominal apse",
                            "isCorrect": False,
                            "explanation": "Kondiloma lata spiroket T. pallidum kaynaklıdır."
                        },
                        {
                            "key": "D",
                            "text": "Kondiloma akuminatum — Herpes Simplex Virus — Ağrısız kıkırdak lezyonu",
                            "isCorrect": False,
                            "explanation": "Kondiloma akuminatum HPV kaynaklı bir skuamöz epitel siğilidir."
                        }
                    ]
                }
            ]
        },
        # S16
        {
            "slideNumber": 16,
            "title": "Kondiloma Akuminatum Histolojisi: Koilositik Atipi",
            "subtitle": "Papiller korlar, perinükleer halo ve viral sitopatik etki",
            "clinicalFocus": "Koilositoz Histopatolojisi",
            "content": "Kondiloma akuminatumun mikroskobik tanısı, papillomatöz mimari ile birlikte HPV enfeksiyonunun karakteristik sitopatik etkisi olan **koilositik atipinin** gösterilmesine dayanır.\n\n- **Histolojik Mimari:** Fibrovasküler stromal bir çekirdek etrafında dallanan ekzofitik papiller parmaksı çıkıntılar ve üzerini örten belirgin akantotik skuamöz epitel izlenir.\n- **Koilositik Atipi (Koilositoz):** Epitelin üst ve orta katmanlarındaki keratinositlerde görülen patognomonik viral değişikliktir:\n  1. Nükleusta büyüme ve kontur düzensizliği (kuru üzüm tanesi görünümü),\n  2. Nükleer hiperkromazi (koyu boyanma),\n  3. Çekirdek etrafında berrak, optik olarak boş geniş bir sitoplazmik zon (**perinükleer halo**).\n- **Onkolojik Davranış:** Vulvar kondiloma akuminatum lezyonları ==KENDİLİĞİNDEN KANSERE DÖNÜŞMEZ==; ancak hastada eşzamanlı servikal veya vajinal displazi riski taranmalıdır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Kondiloma akuminatum histopatolojisinde aranan viral sitopatik anahtar bulgu koilositik atipidir (perinükleer halo + buruşuk hiperkromatik nükleus).",
            "synthesisNarrative": "Kondiloma akuminatumun mikroskobik tanısı, papillomatöz mimari ile birlikte HPV enfeksiyonunun karakteristik sitopatik etkisi olan **koilositik atipinin** gösterilmesine dayanır.\n\n- **Histolojik Mimari:** Fibrovasküler stromal bir çekirdek etrafında dallanan ekzofitik papiller parmaksı çıkıntılar ve üzerini örten belirgin akantotik skuamöz epitel izlenir.\n- **Koilositik Atipi (Koilositoz):** Epitelin üst ve orta katmanlarındaki keratinositlerde görülen patognomonik viral değişikliktir:\n  1. Nükleusta büyüme ve kontur düzensizliği (kuru üzüm tanesi görünümü),\n  2. Nükleer hiperkromazi (koyu boyanma),\n  3. Çekirdek etrafında berrak, optik olarak boş geniş bir sitoplazmik zon (**perinükleer halo**).\n- **Onkolojik Davranış:** Vulvar kondiloma akuminatum lezyonları ==KENDİLİĞİNDEN KANSERE DÖNÜŞMEZ==; ancak hastada eşzamanlı servikal veya vajinal displazi riski taranmalıdır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Kondiloma akuminatum histopatolojisinde aranan viral sitopatik anahtar bulgu koilositik atipidir (perinükleer halo + buruşuk hiperkromatik nükleus).",
            "bulletPoints": [
                "Papiller fibrovasküler korlar ve akantoz izlenir.",
                "Koilositoz: Büyümüş buruşuk nükleus ve perinükleer berrak halo.",
                "Vulvar kondilomlar selimdir; doğrudan kansere dönüşmez."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Kondiloma akuminatumda HPV enfeksiyonunun mikroskobik göstergesi olan hücre değişikliğine koilositik atipi denir.",
                    "maskedTerm": "koilositik atipi",
                    "hint": "Koilositoz olarak da bilinen patognomonik sitopatik etki"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Koilosit Hücresinin Mikroskobik Bileşenleri",
                    "tableHeaders": ["Hücresel Yapı", "Morfolojik Görünüm", "Tanısal İpucu"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Çekirdek (Nükleus)", "isMasked": False},
                                {"text": "Hiperkromatik ve buruşuk (kuru üzüm)", "isMasked": True, "hint": "kontur düzensizliği ve koyuluk"},
                                {"text": "Viral DNA replikasyonunun etkisi", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Sitoplazma", "isMasked": False},
                                {"text": "Geniş perinükleer berrak halo", "isMasked": False},
                                {"text": "Sitokeratin iskeletinin çökmesi", "isMasked": True, "hint": "çekirdek çevresinde boşluk"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "HPV Sitopatik Etkisinden Koilositoza",
                    "steps": [
                        "1. Viral Entegrasyon/Epizom: HPV E6 ve E7 proteinleri hücre döngüsünü bozar.",
                        "2. E4 Proteini Etkisi: Viral E4 proteini keratin filament ağını çözer ve kümeleştirir.",
                        "3. Halo Oluşumu: Çekirdek etrafındaki sitokeratinlerin çekilmesiyle optik berrak halo doğar.",
                        "4. Koilosit Görünümü: Nükleer büzüşme ve perinükleer halo ile koilosit mikroskopta tanınır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Koilositik atipinin (koilositoz) iki temel mikroskobik morfolojik özelliği nedir?",
                    "answer": "Büyümüş, hiperkromatik ve buruşuk (kuru üzüm benzeri) nükleus ile çekirdeğin etrafını saran belirgin berrak sitoplazmik halodur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Kondiloma Akuminatum Histopatolojisi",
                    "items": [
                        {"text": "Papiller ekzofitik uzantılar fibrovasküler stromal korlar içerir.", "isLie": False, "explanation": "Doğru. Papillomatöz yapının temel iskeletidir."},
                        {"text": "Koilositik atipide çekirdek çevresinde berrak perinükleer halo görülür.", "isLie": False, "explanation": "Doğru. Halo koilositozun en belirgin özelliğidir."},
                        {"text": "Vulvar kondiloma akuminatum lezyonları tek başına doğrudan kansere dönüşmez.", "isLie": False, "explanation": "Doğru. Düşük riskli HPV kaynaklıdır, selim seyreder."},
                        {"text": "Koilositler bol lipid damlacıkları içeren köpüksü multinükleer histiyositlerdir.", "isLie": True, "explanation": "Tuzak! Koilosit histiyosit değil, HPV sitopatik etkisi gösteren çok katlı yassı epitel keratinositidir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Kondiloma akuminatum biyopsisinde izlenen koilositik atipi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Büyümüş buruşuk hiperkromatik nükleus ve çekirdek etrafında berrak perinükleer halo içerir",
                            "isCorrect": True,
                            "explanation": "Koilositik atipinin klasik Robbins ve amfi notu histopatolojik tanımı budur."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca dermis derinliklerinde yer alan aselüler kollajen yumaklarıdır",
                            "isCorrect": False,
                            "explanation": "Koilosit epitelin yüzeyel/orta katındaki hücresel bir değişikliktir."
                        },
                        {
                            "key": "C",
                            "text": "Lezyonun doğrudan 4. evre anaplastik sarkoma dönüştüğünün kesin göstergesidir",
                            "isCorrect": False,
                            "explanation": "Koilositoz HPV sitopatik etkisidir, sarkom göstergesi değildir."
                        },
                        {
                            "key": "D",
                            "text": "Bakteriyel fagositoz yapan dev köpüksü makrofajlardan ibarettir",
                            "isCorrect": False,
                            "explanation": "Koilosit skuamöz epitel hücresidir, makrofaj değildir."
                        }
                    ]
                }
            ]
        },
        # S17
        {
            "slideNumber": 17,
            "title": "Vulvar Karsinom: Epidemiyoloji ve İki Ayrı Patojenetik Yol",
            "subtitle": "HPV pozitif bazaloid yol vs HPV negatif keratinize yol",
            "clinicalFocus": "Vulvar Karsinom İkili Modeli",
            "content": "Vulva kanseri tüm jinekolojik malignitelerin yaklaşık %3'ünü oluşturur ve vakaların %90'ı skuamöz hücreli karsinomdur (SCC). Patolojide vulvar SCC tamamen farklı iki biyolojik ve epidemiyolojik yol üzerinden gelişir:\n\n- **1. HPV Pozitif Yol (Bazaloid ve Verrüköz Karsinom):**\n  * Sıklıkla 45-60 yaş grubunda, cinsel aktif veya immün yetmezlikli kadınlarda görülür.\n  * En sık etken yüksek riskli **HPV tip 16** (ve tip 18)'dir; sıklıkla sigara kullanımı eşlik eder.\n  * Ön lezyonu klasik **Vulvar İntraepitelyal Neoplazi (klasik VIN)** tablosudur.\n  * Tümörler çoğunlukla **kötü diferansiye** ve **çok odaklıdır (multifokal)**.\n- **2. HPV Negatif Yol (Keratinize Skuamöz Karsinom):**\n  * İleri yaştaki kadınlarda (ortalama yaş ~75) izlenir; HPV enfeksiyonu ile ilişkisizdir.\n  * Zemininde uzun süreli **liken skleroz** veya skuamöz hücre hiperplazisi bulunur.\n  * Ön lezyonu **diferansiye VIN (dVIN)** olarak adlandırılır.\n  * Tümörler genellikle **iyi diferansiye**, belirgin keratin üreten ve **tek odaklıdır (unifokal)**.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Genç, sigara içen kadında çok odaklı kötü diferansiye tümör = HPV pozitif yol; yaşlı kadında liken skleroz zemininde tek odaklı iyi diferansiye keratinize tümör = HPV negatif yol.",
            "synthesisNarrative": "Vulva kanseri tüm jinekolojik malignitelerin yaklaşık %3'ünü oluşturur ve vakaların %90'ı skuamöz hücreli karsinomdur (SCC). Patolojide vulvar SCC tamamen farklı iki biyolojik ve epidemiyolojik yol üzerinden gelişir:\n\n- **1. HPV Pozitif Yol (Bazaloid ve Verrüköz Karsinom):**\n  * Sıklıkla 45-60 yaş grubunda, cinsel aktif veya immün yetmezlikli kadınlarda görülür.\n  * En sık etken yüksek riskli **HPV tip 16** (ve tip 18)'dir; sıklıkla sigara kullanımı eşlik eder.\n  * Ön lezyonu klasik **Vulvar İntraepitelyal Neoplazi (klasik VIN)** tablosudur.\n  * Tümörler çoğunlukla **kötü diferansiye** ve **çok odaklıdır (multifokal)**.\n- **2. HPV Negatif Yol (Keratinize Skuamöz Karsinom):**\n  * İleri yaştaki kadınlarda (ortalama yaş ~75) izlenir; HPV enfeksiyonu ile ilişkisizdir.\n  * Zemininde uzun süreli **liken skleroz** veya skuamöz hücre hiperplazisi bulunur.\n  * Ön lezyonu **diferansiye VIN (dVIN)** olarak adlandırılır.\n  * Tümörler genellikle **iyi diferansiye**, belirgin keratin üreten ve **tek odaklıdır (unifokal)**.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Genç, sigara içen kadında çok odaklı kötü diferansiye tümör = HPV pozitif yol; yaşlı kadında liken skleroz zemininde tek odaklı iyi diferansiye keratinize tümör = HPV negatif yol.",
            "bulletPoints": [
                "HPV pozitif: ~60 yaş, HPV-16, multifokal, kötü diferansiye.",
                "HPV negatif: ~75 yaş, liken skleroz zemini, unifokal, keratinize iyi diferansiye.",
                "İki yolun öncü lezyonları (klasik VIN vs dVIN) farklıdır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "HPV ile ilişkili olmayan vulvar karsinomlar genellikle ileri yaşta ve liken skleroz zemininde gelişir.",
                    "maskedTerm": "liken skleroz",
                    "hint": "HPV negatif keratinize karsinoma zemin hazırlayan atrofik dermatoz"
                },
                {
                    "type": "before_after_slider",
                    "leftTitle": "HPV Pozitif Vulvar SCC",
                    "rightTitle": "HPV Negatif Vulvar SCC",
                    "leftPoints": [
                        "Ortalama yaş ~60 civarındadır; sigara sık eşlik eder.",
                        "Yüksek riskli HPV tip 16 ile güçlü ilişkilidir.",
                        "Lezyonlar çoğunlukla çok odaklıdır (multifokal).",
                        "Histopatolojik olarak kötü diferansiye / bazaloid tiptedir."
                    ],
                    "rightPoints": [
                        "Ortalama yaş ~75 olup ileri yaş kadınlarda görülür.",
                        "HPV ile ilişkisizdir; liken skleroz zemininde gelişir.",
                        "Lezyonlar genellikle tek odaklıdır (unifokal).",
                        "Histopatolojik olarak iyi diferansiye ve keratinizedir."
                    ]
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulvar Karsinom İkili Model Karşılaştırması",
                    "tableHeaders": ["Özellik", "HPV Pozitif Karsinom", "HPV Negatif Karsinom"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Viral İlişki", "isMasked": False},
                                {"text": "Yüksek riskli HPV tip 16", "isMasked": True, "hint": "onkojenik karsinojenik virüs"},
                                {"text": "HPV ilişkisi yoktur", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Öncü Lezyon", "isMasked": False},
                                {"text": "Klasik VIN (uVIN)", "isMasked": False},
                                {"text": "Diferansiye VIN (dVIN)", "isMasked": True, "hint": "bazal katmanda atipi içeren ön lezyon"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "İki Ayrı Karsinogenez Yolu",
                    "steps": [
                        "1. Giriş: Bir kolda HPV enfeksiyonu, diğer kolda kronik liken skleroz başlar.",
                        "2. Mutasyon Birikimi: HPV E6/E7 onkoproteinleri p53/Rb yıkar; liken kolunda p53 mutasyonu birikir.",
                        "3. Prekanseröz Faz: HPV kolunda klasik VIN, liken kolunda diferansiye VIN oluşur.",
                        "4. İnvaziv Tümör: HPV kolunda kötü diferansiye bazaloid, liken kolunda iyi diferansiye keratinize SCC gelişir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulvar skuamöz karsinomun iki ana grubunun ortalama yaş, etken ve histolojik diferansiyasyon farkları nelerdir?",
                    "answer": "HPV pozitif grup: ~60 yaş, HPV-16 etken, multifokal ve kötü diferansiye bazaloid; HPV negatif grup: ~75 yaş, liken skleroz zeminli, unifokal ve iyi diferansiye keratinizedir."
                },
                {
                    "type": "micro_quiz",
                    "question": "Liken skleroz zemininde gelişen HPV-negatif vulvar karsinomlar için hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Genellikle ~75 yaşındaki kadınlarda, tek odaklı (unifokal) ve iyi diferansiye keratinize tümör olarak gelişir",
                            "isCorrect": True,
                            "explanation": "HPV negatif karsinomun klasik klinik ve histolojik profili unifokal, ileri yaş ve keratinize olmaktır."
                        },
                        {
                            "key": "B",
                            "text": "En sık 20 yaşındaki gençlerde çok odaklı bazaloid kitleler olarak izlenir",
                            "isCorrect": False,
                            "explanation": "Genç yaş ve multifokalite HPV pozitif grubun özelliğidir."
                        },
                        {
                            "key": "C",
                            "text": "Tümör dokusunda daima yüksek düzeyde HPV-16 DNA entegrasyonu saptanır",
                            "isCorrect": False,
                            "explanation": "Bu grup tanım gereği HPV'den tamamen bağımsızdır."
                        },
                        {
                            "key": "D",
                            "text": "Öncü lezyonu kondiloma akuminatumdur ve hiçbir zaman cerrahi gerekmez",
                            "isCorrect": False,
                            "explanation": "Öncü lezyonu dVIN'dir ve cerrahi tedavi gerektiren invaziv bir kanserdir."
                        }
                    ]
                }
            ]
        },
        # S18
        {
            "slideNumber": 18,
            "title": "Vulvar İntraepitelyal Neoplazi (VIN) ve dVIN Dinamikleri",
            "subtitle": "Klasik uVIN vs diferansiye VIN (dVIN) histopatolojisi ve p53 rolü",
            "clinicalFocus": "Preinvaziv Lezyonlar",
            "content": "Vulvar karsinomların iki patogenetik yolu, mikroskop altında tamamen farklı öncü lezyonlar üzerinden ilerler. Bu öncü lezyonların tanınması invaziv kanserin önlenmesinde hayatidir.\n\n- **Klasik (Olağan) VIN (uVIN):**\n  * Yüksek riskli HPV (özellikle tip 16) enfeksiyonuna sekonder gelişir.\n  * Epitelin tüm katmanlarında nükleer pleomorfizm, yüksek mitotik aktivite, polarite kaybı ve nükleus/sitoplazma oranında artış izlenir (karsinoma in situ).\n  * Genellikle çok odaklıdır ve genç kadınlarda görülür; p16 immünohistokimyası ile diffüz blok pozitiflik verir.\n- **Diferansiye VIN (dVIN):**\n  * HPV negatif yolun öncüsüdür; sıklıkla liken skleroz zemininde ortaya çıkar.\n  * Histolojik atipi epitelin tamamına yayılmaz; **yalnızca bazal ve parabazal katmanlara sınırlıdır**.\n  * Üst katmanlarda erken anormal keratinizasyon ve geniş eozinofilik sitoplazma izlenir.\n  * Çok sinsi bir lezyondur; p53 mutasyonu içerir ve hızla invaziv keratinize SCC'ye ilerleyebilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] dVIN'de atipi yalnızca bazal tabakada sınırlı olduğu için mikroskopta kolayca gözden kaçabilir; ancak invaziv kansere ilerleme hızı klasik VIN'den çok daha yüksektir.",
            "synthesisNarrative": "Vulvar karsinomların iki patogenetik yolu, mikroskop altında tamamen farklı öncü lezyonlar üzerinden ilerler. Bu öncü lezyonların tanınması invaziv kanserin önlenmesinde hayatidir.\n\n- **Klasik (Olağan) VIN (uVIN):**\n  * Yüksek riskli HPV (özellikle tip 16) enfeksiyonuna sekonder gelişir.\n  * Epitelin tüm katmanlarında nükleer pleomorfizm, yüksek mitotik aktivite, polarite kaybı ve nükleus/sitoplazma oranında artış izlenir (karsinoma in situ).\n  * Genellikle çok odaklıdır ve genç kadınlarda görülür; p16 immünohistokimyası ile diffüz blok pozitiflik verir.\n- **Diferansiye VIN (dVIN):**\n  * HPV negatif yolun öncüsüdür; sıklıkla liken skleroz zemininde ortaya çıkar.\n  * Histolojik atipi epitelin tamamına yayılmaz; **yalnızca bazal ve parabazal katmanlara sınırlıdır**.\n  * Üst katmanlarda erken anormal keratinizasyon ve geniş eozinofilik sitoplazma izlenir.\n  * Çok sinsi bir lezyondur; p53 mutasyonu içerir ve hızla invaziv keratinize SCC'ye ilerleyebilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] dVIN'de atipi yalnızca bazal tabakada sınırlı olduğu için mikroskopta kolayca gözden kaçabilir; ancak invaziv kansere ilerleme hızı klasik VIN'den çok daha yüksektir.",
            "bulletPoints": [
                "Klasik VIN: HPV ilişkili, tüm epitel katlarında atipi, p16(+).",
                "dVIN: HPV negatif, liken skleroz ilişkili, atipi bazal tabakada sınırlı, p53(+).",
                "dVIN hızla invaziv keratinize karsinoma ilerleyebilir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "HPV negatif vulvar karsinomun öncüsü olan diferansiye VIN lezyonunda sitolojik atipi bazal tabakaya sınırlıdır.",
                    "maskedTerm": "bazal tabakaya",
                    "hint": "dVIN'de atipik hücrelerin yerleştiği en alt epitel katmanı"
                },
                {
                    "type": "before_after_slider",
                    "leftTitle": "Klasik VIN (uVIN)",
                    "rightTitle": "Diferansiye VIN (dVIN)",
                    "leftPoints": [
                        "Yüksek riskli HPV tip 16 ile ilişkilidir.",
                        "Epitelin tüm katlarında yaygın atipi izlenir.",
                        "İmmünohistokimyada p16 diffüz pozitif boyanır.",
                        "İnvazyona ilerleme süreci yıllar alabilir."
                    ],
                    "rightPoints": [
                        "HPV ilişkisizdir; liken skleroz zemininde gelişir.",
                        "Atipi yalnızca bazal ve parabazal katmana sınırlıdır.",
                        "p53 gen mutasyonu ve anormal p53 boyanması tipiktir.",
                        "İnvaziv keratinize SCC'ye ilerleme potansiyeli çok hızlıdır."
                    ]
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Klasik VIN ve Diferansiye VIN Karşılaştırma Matrisi",
                    "tableHeaders": ["Özellik", "Klasik VIN (uVIN)", "Diferansiye VIN (dVIN)"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Atipinin Dağılımı", "isMasked": False},
                                {"text": "Tüm epitel kalınlığı boyunca", "isMasked": False},
                                {"text": "Yalnızca bazal tabakaya sınırlı", "isMasked": True, "hint": "en alt tabakada sınırlı atipi"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Biyolojik Zemin", "isMasked": False},
                                {"text": "HPV enfeksiyonu", "isMasked": True, "hint": "onkojenik viral zemin"},
                                {"text": "Liken skleroz / skuamöz hiperplazi", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "dVIN'den İnvaziv Keratinize Karsinoma",
                    "steps": [
                        "1. Zemin: Kronik liken sklerozda epitel hasarı ve kronik T hücre yangısı sürer.",
                        "2. p53 Mutasyonu: Bazal tabakadaki kök hücrelerde somatik TP53 mutasyonu gelişir.",
                        "3. dVIN Gelişimi: Bazal tabakada atipik hücreler ürerken üst katmanlar olgunlaşır (diferansiye VIN).",
                        "4. İnvazyon: Bazal atipik hücreler bazal membranı delerek dermise geçer ve keratinize SCC oluşturur."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Diferansiye VIN (dVIN) lezyonunun histopatolojik olarak mikroskopta gözden kaçmasını kolaylaştıran tuzak özellik nedir?",
                    "answer": "Atipinin tüm epitele yayılmayıp yalnızca bazal tabakada sınırlı kalması ve üst katmanların normal veya hiperkeratotik görünmesidir."
                },
                {
                    "type": "micro_quiz",
                    "question": "Diferansiye VIN (dVIN) lezyonu ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Liken skleroz zemininde gelişir, atipi bazal tabakayla sınırlıdır ve hızla keratinize karsinoma ilerleyebilir",
                            "isCorrect": True,
                            "explanation": "dVIN'in temel patolojik ve biyolojik tanımı tam olarak budur."
                        },
                        {
                            "key": "B",
                            "text": "Düşük riskli HPV tip 6 ve 11 enfeksiyonunun doğrudan selim sonucudur",
                            "isCorrect": False,
                            "explanation": "HPV 6 ve 11 kondilom yapar, dVIN ise HPV'den bağımsız premalign lezyondur."
                        },
                        {
                            "key": "C",
                            "text": "Epitelin tüm katmanlarında atipi vardır ve p16 proteini daima kuvvetli pozitiftir",
                            "isCorrect": False,
                            "explanation": "Tüm katlarda atipi ve p16 pozitifliği klasik uVIN'in özelliğidir."
                        },
                        {
                            "key": "D",
                            "text": "Yalnızca bebeklik çağında görülen benign vasküler bir anomalidir",
                            "isCorrect": False,
                            "explanation": "dVIN yaşlı kadınlarda görülen premalign bir epitelyal neoplazidir."
                        }
                    ]
                }
            ]
        },
        # S19
        {
            "slideNumber": 19,
            "title": "Vulvar Karsinom: Makroskopi, Yayılım Yolları ve Evreleme",
            "subtitle": "Bölgesel inguinal lenfatik tutulum ve hematogen metastaz",
            "clinicalFocus": "Yayılım Yolları ve Prognostik Faktörler",
            "content": "Vulvar skuamöz hücreli karsinomun klinik davranışı, tümörün lokal yayılımı ve lenfatik drenaj paterni ile doğrudan ilişkilidir.\n\n- **Makroskobik Görünüm:** Erken dönemde lökoplaki veya hiperpigmente düzensiz plaklar şeklindeyken; ilerleyen dönemde ekzofitik karnabahar benzeri kitleler veya ortası nekrotik, sert kenarlı endofitik ülserler oluşturur.\n- **Lokal Davranış:** Tümör uzun süre lokal kalma eğilimindedir; komşu vajina, üretra ve anüse doğrudan yayılım gösterebilir.\n- **Lenfatik Yayılım:** İlk ve en kritik metastaz yolu bölgesel lenf düğümleridir. Drenaj öncelikle **inguinofemoral lenf nodlarına** (yüzeyel ve derin inguinal nodlar), ardından pelvik lenf nodlarına ilerler.\n- **Uzak Metastaz ve Prognoz:** İleri evrede kan yoluyla (hematogen) akciğer, karaciğer ve kemik metastazları gelişir. Prognozu belirleyen en kritik parametreler **evre, tümör boyutu, invazyon derinliği ve lenf nodu metastazı varlığıdır**.\n\n> [!NOTE]\n> Vulva karsinomunda lenf nodu tutulumu prognozu dramatik şekilde kötüleştirir; bu nedenle cerrahi evrelemede sentinel lenf nodu biyopsisi veya inguinal diseksiyon esastır.",
            "synthesisNarrative": "Vulvar skuamöz hücreli karsinomun klinik davranışı, tümörün lokal yayılımı ve lenfatik drenaj paterni ile doğrudan ilişkilidir.\n\n- **Makroskobik Görünüm:** Erken dönemde lökoplaki veya hiperpigmente düzensiz plaklar şeklindeyken; ilerleyen dönemde ekzofitik karnabahar benzeri kitleler veya ortası nekrotik, sert kenarlı endofitik ülserler oluşturur.\n- **Lokal Davranış:** Tümör uzun süre lokal kalma eğilimindedir; komşu vajina, üretra ve anüse doğrudan yayılım gösterebilir.\n- **Lenfatik Yayılım:** İlk ve en kritik metastaz yolu bölgesel lenf düğümleridir. Drenaj öncelikle **inguinofemoral lenf nodlarına** (yüzeyel ve derin inguinal nodlar), ardından pelvik lenf nodlarına ilerler.\n- **Uzak Metastaz ve Prognoz:** İleri evrede kan yoluyla (hematogen) akciğer, karaciğer ve kemik metastazları gelişir. Prognozu belirleyen en kritik parametreler **evre, tümör boyutu, invazyon derinliği ve lenf nodu metastazı varlığıdır**.\n\n> [!NOTE]\n> Vulva karsinomunda lenf nodu tutulumu prognozu dramatik şekilde kötüleştirir; bu nedenle cerrahi evrelemede sentinel lenf nodu biyopsisi veya inguinal diseksiyon esastır.",
            "bulletPoints": [
                "Ekzofitik kitle veya ülsere lezyon şeklinde belirir.",
                "İlk metastaz yeri inguinofemoral lenf düğümleridir.",
                "Prognoz evre, derinlik ve lenf nodu tutulumuna bağlıdır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vulvar skuamöz hücreli karsinomun ilk bölgesel lenfatik metastaz durağı inguinofemoral lenf nodlarıdır.",
                    "maskedTerm": "inguinofemoral",
                    "hint": "Yüzeyel ve derin inguinal lenf bezlerini kapsayan bölgesel istasyon"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulvar Karsinomda Yayılım Aşamaları",
                    "tableHeaders": ["Yayılım Seviyesi", "Anatomik Hedef", "Prognostik Anlam"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Lokal İnvazyon", "isMasked": False},
                                {"text": "Vajina, üretra ve perine", "isMasked": False},
                                {"text": "Lokal cerrahi rezeksiyon sınırlarını zorlar", "isMasked": True, "hint": "organ koruyucu cerrahiyi kısıtlar"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Bölgesel Lenfatik", "isMasked": False},
                                {"text": "İnguinal ve pelvik lenf nodları", "isMasked": True, "hint": "ilk metastaz durağı"},
                                {"text": "Sağkalımı belirleyen en kritik faktördür", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Karsinom Yayılım Basamakları",
                    "steps": [
                        "1. Lokal Proliferasyon: Tümör hücreleri dermise doğru invazyon derinliğini artırır.",
                        "2. Lenfatik Giriş: Dermal lenfatik kanallara giren tümör embolileri akımla sürüklenir.",
                        "3. Bölgesel Tutulum: İnguinofemoral lenf düğümlerinde metastatik odaklar kurulur.",
                        "4. Uzak Yayılım: Sistemik dolaşıma katılarak akciğer ve karaciğer gibi uzak organlara metastaz yapar."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulvar skuamöz karsinomda prognozu belirleyen en kritik klinikopatolojik parametreler nelerdir?",
                    "answer": "Tümör evresi, invazyon derinliği, tümör çapı ve en önemlisi bölgesel (inguinofemoral) lenf nodu metastazının varlığıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vulva Karsinomunun Yayılımı ve Prognozu",
                    "items": [
                        {"text": "Vulvar karsinomlar ekzofitik kitle veya ülsere endofitik lezyon oluşturabilir.", "isLie": False, "explanation": "Doğru. Her iki makroskopik form da görülebilir."},
                        {"text": "İlk lenfatik yayılım durağı bölgesel inguinofemoral lenf düğümleridir.", "isLie": False, "explanation": "Doğru. Anatomik lenfatik drenaj öncelikle kasık nodlarına gider."},
                        {"text": "Prognoz doğrudan invazyon derinliği ve lenf nodu tutulumu ile ilişkilidir.", "isLie": False, "explanation": "Doğru. Lenf nodu pozitifliği sağkalımı belirgin düşürür."},
                        {"text": "Vulva karsinomu lenfatik yayılım yapmaz; daima ilk saniyede doğrudan beyne metastazla başlar.", "isLie": True, "explanation": "Tuzak! İlk yayılım lenfatiktir (inguinal nodlar); beyin metastazı son derece nadir ve terminaldir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvar skuamöz hücreli karsinomun metastaz paterni ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "İlk lenfatik metastazını bölgesel inguinofemoral lenf düğümlerine yapar",
                            "isCorrect": True,
                            "explanation": "Vulvanın primer lenfatik drenaj yolu inguinofemoral lenf nodlarıdır."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca retrograd yolla doğrudan böbrek glomerüllerine yayılır",
                            "isCorrect": False,
                            "explanation": "Böbrek glomerüllerine retrograd yayılım söz konusu değildir."
                        },
                        {
                            "key": "C",
                            "text": "Lenf nodlarını tamamen atlayarak daima yalnızca kemik iliğini tutar",
                            "isCorrect": False,
                            "explanation": "Lenfatik nod tutulumu en karakteristik yayılım basamağıdır."
                        },
                        {
                            "key": "D",
                            "text": "Hiçbir zaman lokal invazyon yapmaz ve komşu organlara asla sıçramaz",
                            "isCorrect": False,
                            "explanation": "Vajina, üretra ve perinede agresif lokal invazyon yapabilir."
                        }
                    ]
                }
            ]
        },
        # S20
        {
            "slideNumber": 20,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 2] Skuamöz Hiperplazi, Kondilomlar ve Karsinom Spektrumu",
            "subtitle": "11-19. adımların histopatolojik sentezi, ayırıcı tanı ve onkolojik modeller",
            "clinicalFocus": "Bölüm 2 Özeti ve Pekiştirme",
            "content": "Bu ikinci kontrol noktasında vulvanın hiperplastik, viral ve malign süreçlerini bir bütün halinde özetliyoruz:\n\n- **Skuamöz Hücre Hiperplazisi:** Kronik kaşımaya sekonder akantoz ve hiperkeratoz ile karakterizedir; mitoz artabilir ancak ==kesinlikle sitolojik atipi yoktur==.\n- **Kondilom Ayrımı:** Kondiloma lata sekonder sifiliz (T. pallidum) bulgusudur ve düz lezyonlardır; kondiloma akuminatum ise düşük riskli HPV tip 6 ve 11 ile oluşan, koilositik atipi barındıran ekzofitik papiller siğillerdir.\n- **Vulvar Karsinom İkili Modeli:**\n  * HPV Pozitif: ~60 yaş, sigara, HPV-16, klasik VIN öncüllü, multifokal ve kötü diferansiye.\n  * HPV Negatif: ~75 yaş, liken skleroz zeminli, dVIN öncüllü, unifokal ve keratinize iyi diferansiye.\n- **Yayılım ve Prognoz:** İlk metastaz durağı inguinofemoral lenf nodlarıdır; lenf nodu tutulumu ve invazyon derinliği prognozu belirler.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] dVIN'de atipi yalnızca bazal tabakada sınırlı kalır; kondilomlarda koilositik atipi (buruşuk nükleus + perinükleer halo) izlenir.",
            "synthesisNarrative": "Bu ikinci kontrol noktasında vulvanın hiperplastik, viral ve malign süreçlerini bir bütün halinde özetliyoruz:\n\n- **Skuamöz Hücre Hiperplazisi:** Kronik kaşımaya sekonder akantoz ve hiperkeratoz ile karakterizedir; mitoz artabilir ancak ==kesinlikle sitolojik atipi yoktur==.\n- **Kondilom Ayrımı:** Kondiloma lata sekonder sifiliz (T. pallidum) bulgusudur ve düz lezyonlardır; kondiloma akuminatum ise düşük riskli HPV tip 6 ve 11 ile oluşan, koilositik atipi barındıran ekzofitik papiller siğillerdir.\n- **Vulvar Karsinom İkili Modeli:**\n  * HPV Pozitif: ~60 yaş, sigara, HPV-16, klasik VIN öncüllü, multifokal ve kötü diferansiye.\n  * HPV Negatif: ~75 yaş, liken skleroz zeminli, dVIN öncüllü, unifokal ve keratinize iyi diferansiye.\n- **Yayılım ve Prognoz:** İlk metastaz durağı inguinofemoral lenf nodlarıdır; lenf nodu tutulumu ve invazyon derinliği prognozu belirler.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] dVIN'de atipi yalnızca bazal tabakada sınırlı kalır; kondilomlarda koilositik atipi (buruşuk nükleus + perinükleer halo) izlenir.",
            "bulletPoints": [
                "Skuamöz hiperplazide akantoz vardır, atipi yoktur.",
                "Kondiloma akuminatumda HPV 6/11 ve koilositik atipi izlenir.",
                "Vulvar karsinom HPV pozitif (VIN) ve negatif (dVIN) iki yoldan gelişir.",
                "İlk metastaz yeri inguinofemoral lenf nodlarıdır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Kondiloma akuminatum histolojisinde patognomonik viral etki olan koilositik atipi izlenir.",
                    "maskedTerm": "koilositik atipi",
                    "hint": "HPV sitopatik etkisiyle oluşan perinükleer halolu hücresel değişiklik"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bölüm 2 Onkolojik Spektrum Sentezi",
                    "tableHeaders": ["Lezyon / Tablo", "Etiyolojik Ajan / Zemin", "Histopatolojik Karakter"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Skuamöz Hiperplazi", "isMasked": False},
                                {"text": "Kronik kaşıma ve mekanik sürtünme", "isMasked": False},
                                {"text": "Akantoz ve hiperkeratoz; atipi yok", "isMasked": True, "hint": "sitolojik selimlik"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Kondiloma Akuminatum", "isMasked": False},
                                {"text": "Düşük riskli HPV tip 6 ve 11", "isMasked": True, "hint": "selim genital siğil virüsleri"},
                                {"text": "Papiller korlar ve koilositik atipi", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "HPV Negatif Karsinom", "isMasked": False},
                                {"text": "Liken skleroz / dVIN", "isMasked": False},
                                {"text": "İyi diferansiye keratinize SCC", "isMasked": True, "hint": "ileri yaş tek odaklı karsinom"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Bölüm 2 Patoloji Sentezi",
                    "steps": [
                        "1. Reaktif Faz: Kaşıntıyla başlayan ovma skuamöz hiperplaziyi (akantoz, atipisiz) doğurur.",
                        "2. Viral Siğil: Düşük riskli HPV kondiloma akuminatum (koilositoz) tablosunu yapar.",
                        "3. İki Karsinom Yolu: Yüksek riskli HPV klasik VIN'e, liken skleroz dVIN'e ilerler.",
                        "4. İnvazyon ve Metastaz: Bazal membran aşılır; karsinom inguinofemoral nodlara metastaz yapar."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bölüm 2'de işlenen skuamöz hiperplazi, kondiloma akuminatum ve dVIN lezyonlarının atipi açısından temel farkı nedir?",
                    "answer": "Skuamöz hiperplazide atipi yoktur; kondilomda viral koilositik atipi vardır; dVIN'de ise bazal tabakayla sınırlı malign sitolojik atipi mevcuttur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Bölüm 2 Genel Tekrar",
                    "items": [
                        {"text": "Skuamöz hücre hiperplazisinde akantoz ve hiperkeratoz görülürken sitolojik atipi yoktur.", "isLie": False, "explanation": "Doğru. Sitolojik selimlik temel kuraldır."},
                        {"text": "Kondiloma lata sekonder sifiliz etkeni Treponema pallidum ile oluşur.", "isLie": False, "explanation": "Doğru. Sifilizin düz geniş tabanlı lezyonudur."},
                        {"text": "Vulvar karsinomun ilk lenfatik metastaz durağı inguinofemoral lenf nodlarıdır.", "isLie": False, "explanation": "Doğru. Kasık lenf nodları ilk drenaj istasyonudur."},
                        {"text": "Kondiloma akuminatum hastaların tamamında doğrudan kemik metastazlı anaplastik osteosarkoma dönüşür.", "isLie": True, "explanation": "Tuzak! Kondiloma akuminatum düşük riskli HPV kaynaklıdır, osteosarkom yapmaz."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Bölüm 2'de özetlenen patolojilerle ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Kondiloma akuminatum HPV 6 ve 11 ile oluşan koilositik bir lezyondur; dVIN ise liken skleroz zeminli karsinom öncülüdür",
                            "isCorrect": True,
                            "explanation": "Bu ifade her iki antitenin de doğru etyolojik ve patolojik tanımını içerir."
                        },
                        {
                            "key": "B",
                            "text": "Skuamöz hiperplazide tüm katlarda dev karsinoma in situ hücreleri bulunur",
                            "isCorrect": False,
                            "explanation": "Skuamöz hiperplazide sitolojik atipi kesinlikle yoktur."
                        },
                        {
                            "key": "C",
                            "text": "Kondiloma lata yalnızca çocuklarda doğuştan görülen selim bir teratomdur",
                            "isCorrect": False,
                            "explanation": "Kondiloma lata sekonder sifilizin cinsel bulaşlı bulgusudur."
                        },
                        {
                            "key": "D",
                            "text": "Vulvar skuamöz karsinom hiçbir zaman lenf düğümlerine metastaz yapmaz",
                            "isCorrect": False,
                            "explanation": "İnguinofemoral lenf nodları en sık ve ilk metastaz durağıdır."
                        }
                    ]
                }
            ]
        }
    ]
    return slides

if __name__ == '__main__':
    slides = get_s2_slides()
    print(f'Section 2 created with {len(slides)} slides.')
