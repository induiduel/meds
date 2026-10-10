import json

def get_s1_slides():
    return [
        {
            "slideNumber": 1,
            "title": "Kadın Alt Genital Sistemi: Vulvanın Anatomik ve Histolojik Çerçevesi",
            "subtitle": "Kıllı deri ve mukozal yüzeylerin histolojik organizasyonu",
            "clinicalFocus": "Anatomi ve Histoloji",
            "content": "Vulva, dış kadın genital organlarını tanımlayan ve hem keratinize çok katlı yassı epitel içeren kıl foliküllü deriyi hem de nemli mukozal yüzeyleri bir arada barındıran anatomik bölgedir. Bu iki farklı doku mimarisi, gelişebilecek patolojilerin karakterini ve klinik seyrini doğrudan belirler.\n\n- **Kıllı Deri Örtüsü:** Labia majora, tipik kıl folikülleri, yağ bezleri ve apokrin ter bezleri barındıran keratinize epidermis ile kaplıdır; dermatolojik lezyonlar sıklıkla bu alana yerleşir.\n- **Mukozal Yüzeyler:** Labia minora, klitoris ve vestibül nemli, keratinize olmayan veya hafif keratinize çok katlı yassı epitelle döşelidir; kıl folikülü içermez ve kimyasal irritanlara karşı oldukça geçirgendir.\n- **Hastalık Spektrumu:** En sık karşılaşılan tablolar hafif veya rahatsız edici inflamatuvar lezyonlardır; malign tümörler ise nadir görülmekle birlikte hayatı tehdit edici potansiyele sahiptir.\n\n> [!NOTE]\n> Vulva lezyonlarında lezyonun kıl folikülü içeren labia majorada mı yoksa mukozal labia minorada mı yerleştiği ayırıcı tanıda yol göstericidir.",
            "synthesisNarrative": "Vulva, dış kadın genital organlarını tanımlayan ve hem keratinize çok katlı yassı epitel içeren kıl foliküllü deriyi hem de nemli mukozal yüzeyleri bir arada barındıran anatomik bölgedir. Bu iki farklı doku mimarisi, gelişebilecek patolojilerin karakterini ve klinik seyrini doğrudan belirler.\n\n- **Kıllı Deri Örtüsü:** Labia majora, tipik kıl folikülleri, yağ bezleri ve apokrin ter bezleri barındıran keratinize epidermis ile kaplıdır; dermatolojik lezyonlar sıklıkla bu alana yerleşir.\n- **Mukozal Yüzeyler:** Labia minora, klitoris ve vestibül nemli, keratinize olmayan veya hafif keratinize çok katlı yassı epitelle döşelidir; kıl folikülü içermez ve kimyasal irritanlara karşı oldukça geçirgendir.\n- **Hastalık Spektrumu:** En sık karşılaşılan tablolar hafif veya rahatsız edici inflamatuvar lezyonlardır; malign tümörler ise nadir görülmekle birlikte hayatı tehdit edici potansiyele sahiptir.\n\n> [!NOTE]\n> Vulva lezyonlarında lezyonun kıl folikülü içeren labia majorada mı yoksa mukozal labia minorada mı yerleştiği ayırıcı tanıda yol göstericidir.",
            "bulletPoints": [
                "Vulva labia majora (kıllı deri) ve labia minora (mukoza) içerir.",
                "En sık inflamatuvar süreçler, nadiren maligniteler izlenir.",
                "Doku mimarisi patolojinin yerleşimini belirler."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vulvanın kıl folikülleri ve yağ bezleri içeren keratinize deri örtüsünü labia majora oluşturur.",
                    "maskedTerm": "labia majora",
                    "hint": "Vulvanın kıllı deri ile kaplı dış dudak anatomik yapısı"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulva Anatomik Bölgeleri ve Epitel Özellikleri",
                    "tableHeaders": ["Anatomik Bölge", "Doku Örtüsü", "Tipik Özellik"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Labia majora", "isMasked": False},
                                {"text": "Keratinize çok katlı yassı epitel", "isMasked": False},
                                {"text": "kıl folikülü ve apokrin ter bezleri", "isMasked": True, "hint": "deri ekleri"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Labia minora", "isMasked": False},
                                {"text": "Keratinize olmayan mukoza", "isMasked": True, "hint": "nemli mukoza katmanı"},
                                {"text": "Kıl folikülü bulunmaz", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Doku Bariyeri ve Lezyon Dağılımı",
                    "steps": [
                        "1. Doku Farkı: Labia majora kalın keratin ve kıl folikülü barındırırken, labia minora ince mukozal epitelle örtülüdür.",
                        "2. Ajan Teması: Sıvı irritanlar ve kimyasallar nemli mukozal bariyeri deriye kıyasla çok daha hızlı aşar.",
                        "3. Hücresel Yanıt: Epitel hasarı sonrasında dermiste lenfositik ve vasküler inflamatuvar yanıt tetiklenir.",
                        "4. Klinik Belirti: Hastada eritem, yanma ve belirgin kaşıntı bulguları gelişir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulva lezyonlarında labia majora ile labia minora arasındaki temel histolojik ayrım nedir?",
                    "answer": "Labia majora kıl folikülleri ve ter bezleri içeren keratinize deriyle kaplıyken; labia minora kıl folikülü içermeyen mukoza ile örtülüdür."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vulva Anatomisi ve Klinik Özellikleri",
                    "items": [
                        {"text": "Labia majora, kıl folikülü ve yağ bezleri içeren keratinize deri örtüsünden oluşur.", "isLie": False, "explanation": "Labia majora tipik dış kıl örtüsü ve apokrin/ekrin bezleri barındıran deri katmanıdır."},
                        {"text": "Labia minora mukozal yapıda olup kıl folikülü içermeyen çok katlı yassı epitelle döşelidir.", "isLie": False, "explanation": "Labia minora mukoza karakterindedir ve kıl folikülü barındırmaz."},
                        {"text": "Vulvada en sık karşılaşılan lezyonlar inflamatuvar süreçlerdir; maligniteler daha nadirdir.", "isLie": False, "explanation": "İnflamatuvar tablolar vulvanın en sık hastalığıdır, kanserler nadirdir."},
                        {"text": "Labia minora yoğun kıl folikülleriyle kaplı kalın keratinize deri yapısındadır.", "isLie": True, "explanation": "Tuzak! Kıl folikülleri labia minorada değil, labia majorada bulunur; labia minora mukozal yapıdadır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulva anatomisi ve doku katmanları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Labia majora kıl folikülü ve ek bezler içeren keratinize çok katlı yassı epitelle döşelidir",
                            "isCorrect": True,
                            "explanation": "Labia majora dış genital bölgenin kıllı deri örtüsünü oluşturur ve tipik deri eklerini barındırır."
                        },
                        {
                            "key": "B",
                            "text": "Labia minora yoğun kıl folikülü içeren kalın bir epidermis tabakasına sahiptir",
                            "isCorrect": False,
                            "explanation": "Labia minora mukozal karakterdedir ve kıl folikülü kesinlikle içermez."
                        },
                        {
                            "key": "C",
                            "text": "Vulvada malign tümörler inflamatuvar lezyonlardan çok daha sık izlenir",
                            "isCorrect": False,
                            "explanation": "Tam tersine en sık patolojiler inflamatuvar karakterdedir; maligniteler oldukça nadirdir."
                        },
                        {
                            "key": "D",
                            "text": "Vulvanın hiçbir bölgesinde keratinize çok katlı yassı epitel yer almaz",
                            "isCorrect": False,
                            "explanation": "Labia majora tam aksine keratinize çok katlı yassı deri epitelinden oluşur."
                        }
                    ]
                }
            ]
        },
        # S2
        {
            "slideNumber": 2,
            "title": "Vulvit: Tanım, Patogenez ve Klinik Spektrum",
            "subtitle": "Dış genital bölgenin yangısal süreçleri ve etyolojik karmaşıklık",
            "clinicalFocus": "Vulvit Etiyolojisi",
            "content": "Vulvit, vulva dokusunu oluşturan anatomik yapıların reaktif, alerjik veya enfeksiyöz nedenlerle gelişen yangısal durumudur. Tek bir hastalık antitesi olmayıp pek çok farklı etyolojik faktörün ortak klinik dışavurumudur.\n\n- **Klinik Tablo:** Hastalar en sık dayanılmaz, inatçı kaşıntı (pruritus), yanma hissi, lokal ödem ve eritem şikayetiyle başvurur.\n- **Kaşıntı-Hasar Döngüsü:** Yoğun kaşıntı refleks olarak ovma ve kaşımaya yol açar; bu mekanik travma yüzeysel epitel erozyonlarına ve sekonder bakteriyel enfeksiyonlara zemin hazırlar.\n- **Etyolojik İkiye Ayrım:** Vulvit olguları temel olarak reaktif/kontakt (irritan ve alerjik) nedenler ile mikrobiyal enfeksiyöz ajanlar olmak üzere iki büyük grupta incelenir.\n\n> [!IMPORTANT]\n> Vulvit tedavisinde yalnızca semptomatik rahatlama sağlamak yetersizdir; altta yatan irritan ajanın veya enfeksiyon etkeninin mikrobiyolojik ve patolojik olarak aydınlatılması gerekir.",
            "synthesisNarrative": "Vulvit, vulva dokusunu oluşturan anatomik yapıların reaktif, alerjik veya enfeksiyöz nedenlerle gelişen yangısal durumudur. Tek bir hastalık antitesi olmayıp pek çok farklı etyolojik faktörün ortak klinik dışavurumudur.\n\n- **Klinik Tablo:** Hastalar en sık dayanılmaz, inatçı kaşıntı (pruritus), yanma hissi, lokal ödem ve eritem şikayetiyle başvurur.\n- **Kaşıntı-Hasar Döngüsü:** Yoğun kaşıntı refleks olarak ovma ve kaşımaya yol açar; bu mekanik travma yüzeysel epitel erozyonlarına ve sekonder bakteriyel enfeksiyonlara zemin hazırlar.\n- **Etyolojik İkiye Ayrım:** Vulvit olguları temel olarak reaktif/kontakt (irritan ve alerjik) nedenler ile mikrobiyal enfeksiyöz ajanlar olmak üzere iki büyük grupta incelenir.\n\n> [!IMPORTANT]\n> Vulvit tedavisinde yalnızca semptomatik rahatlama sağlamak yetersizdir; altta yatan irritan ajanın veya enfeksiyon etkeninin mikrobiyolojik ve patolojik olarak aydınlatılması gerekir.",
            "bulletPoints": [
                "Vulvit çok nedenli bir inflamasyondur.",
                "En belirgin semptom inatçı kaşıntıdır (pruritus).",
                "Kaşıntı-ovma döngüsü doku hasarını ağırlaştırır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vulvit hastalarında en sık başvuru semptomu inatçı ve yoğun kaşıntı hissidir.",
                    "maskedTerm": "kaşıntı",
                    "hint": "Pruritus olarak da adlandırılan temel klinik yakınma"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulvit Patogenezinde Temel Basamaklar",
                    "tableHeaders": ["Aşama", "Patolojik Olay", "Klinik Yansıma"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Başlangıç", "isMasked": False},
                                {"text": "Kimyasal veya enfeksiyöz ajan teması", "isMasked": False},
                                {"text": "Lokal doku irritasyonu ve ödem", "isMasked": True, "hint": "erken vasküler yanıt"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "İlerleme", "isMasked": False},
                                {"text": "Mast hücrelerinden mediyatör salınımı", "isMasked": True, "hint": "alerjik ve yangısal degranülasyon"},
                                {"text": "İnatçı pruritus (kaşıntı)", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Kaşıntı-Kaşıma Kısır Döngüsü",
                    "steps": [
                        "1. İnflamasyon: Vulvar mukozada gelişen primer inflamasyon duyusal sinir uçlarını uyarır.",
                        "2. Pruritus: Hastada şiddetli ve durdurulamayan lokal kaşıntı hissi tetiklenir.",
                        "3. Mekanik Travma: Sürekli kaşıma ve ovma sonucu epitel tabakasında ekskoriasyon ve erozyon gelişir.",
                        "4. Süperenfeksiyon: Bariyeri bozulan dokuya bakteriyel flora eklenerek inflamatuvar tabloyu daha da derinleştirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulvit tablosunda kaşıntının klinik gidişatı ağırlaştırmasındaki temel mekanizma nedir?",
                    "answer": "Kaşımaya bağlı oluşan mekanik travma epitel bütünlüğünü bozar, ekskoriasyonlara yol açar ve sekonder bakteriyel enfeksiyon riskini artırır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vulvitin Genel Özellikleri",
                    "items": [
                        {"text": "Vulvit tek bir patojene bağlı spesifik bir hastalık olmayıp çok etkenli bir inflamasyondur.", "isLie": False, "explanation": "Doğru. Reaktif, alerjik veya enfeksiyöz pek çok sebep vulvite yol açabilir."},
                        {"text": "Vulvit kliniğinde en sık gözlenen rahatsız edici semptom yoğun kaşıntıdır.", "isLie": False, "explanation": "Doğru. Pruritus tablonun kardinal belirtisidir."},
                        {"text": "Mekanik kaşıma epitel bariyerini zedeleyerek lezyonun şiddetini artırır.", "isLie": False, "explanation": "Doğru. Kaşıntı-ovma döngüsü süperenfeksiyon riskini körükler."},
                        {"text": "Vulvit daima tek başına malign bir tümörün doğrudan başlangıç aşamasıdır.", "isLie": True, "explanation": "Tuzak! Vulvit selim bir inflamatuvar süreçtir; malignite ile zorunlu bir bağlantısı yoktur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvitin klinik seyri ve patofizyolojisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Sürekli kaşıma ve sürtünme epitel bütünlüğünü bozarak inflamasyonu ve sekonder enfeksiyonu ağırlaştırır",
                            "isCorrect": True,
                            "explanation": "Mekanik travma dokuda erozyon oluşturarak kısır döngüyü derinleştirir."
                        },
                        {
                            "key": "B",
                            "text": "Vulvit daima ağrısızdır ve hiçbir zaman kaşıntı semptomu oluşturmaz",
                            "isCorrect": False,
                            "explanation": "Kaşıntı (pruritus) vulvitin en belirgin ve kardinal klinik semptomudur."
                        },
                        {
                            "key": "C",
                            "text": "Vulvit etyolojisinde mikrobiyal enfeksiyonların hiçbir rolü bulunmaz",
                            "isCorrect": False,
                            "explanation": "HPV, HSV, bakteriler ve mantarlar gibi birçok mikrobiyal ajan enfeksiyöz vulvit yapar."
                        },
                        {
                            "key": "D",
                            "text": "Vulvit tanısı alan her hastada mutlaka primer invaziv karsinom gelişir",
                            "isCorrect": False,
                            "explanation": "Vulvit selim bir yangısal durumdur, doğrudan karsinom öncülü değildir."
                        }
                    ]
                }
            ]
        },
        # S3
        {
            "slideNumber": 3,
            "title": "Alerjik ve Kontakt İrritan Vulvit",
            "subtitle": "Kimyasal temas, hijyen ürünleri ve yaşlılarda idrar maruziyeti",
            "clinicalFocus": "Kontakt Dermatit",
            "content": "Alerjik ve kontakt irritan vulvit, dış genital bölgenin kimyasal, kozmetik veya biyolojik irritanlarla teması sonucu tetiklenen non-enfeksiyöz reaktif bir tablodur. İnce vulvar mukoza kimyasal maddelere karşı oldukça savunmasızdır.\n\n- **Kimyasal Nedenler:** Kokulu banyo sabunları, vücut losyonları, antiseptik solüsyonlar, parfümlü pedler ve sentetik çamaşırlardaki boyar maddeler en sık kontakt irritanlardır.\n- **Klinik Morfoloji:** Akut dönemde iyi sınırlı, eritemli papüller, ödem, sulanma (eksüdasyon) ve veziküller izlenirken; kronikleştikçe kabuklanma ve deskuamasyon tabloya eklenir.\n- **Yaşlı Populasyonda Özel Durum:** Postmenopozal dönemde üriner inkontinansı olan yaşlı kadınlarda cildin sürekli idrara maruz kalması ciddi kontakt irritan vulvite yol açar.\n\n> [!NOTE]\n> Yaşlı kadınlarda vulvada gözlenen inatçı eritem ve sulanmada idrar inkontinansına bağlı kimyasal irritan dermatit mutlaka akla getirilmelidir.",
            "synthesisNarrative": "Alerjik ve kontakt irritan vulvit, dış genital bölgenin kimyasal, kozmetik veya biyolojik irritanlarla teması sonucu tetiklenen non-enfeksiyöz reaktif bir tablodur. İnce vulvar mukoza kimyasal maddelere karşı oldukça savunmasızdır.\n\n- **Kimyasal Nedenler:** Kokulu banyo sabunları, vücut losyonları, antiseptik solüsyonlar, parfümlü pedler ve sentetik çamaşırlardaki boyar maddeler en sık kontakt irritanlardır.\n- **Klinik Morfoloji:** Akut dönemde iyi sınırlı, eritemli papüller, ödem, sulanma (eksüdasyon) ve veziküller izlenirken; kronikleştikçe kabuklanma ve deskuamasyon tabloya eklenir.\n- **Yaşlı Populasyonda Özel Durum:** Postmenopozal dönemde üriner inkontinansı olan yaşlı kadınlarda cildin sürekli idrara maruz kalması ciddi kontakt irritan vulvite yol açar.\n\n> [!NOTE]\n> Yaşlı kadınlarda vulvada gözlenen inatçı eritem ve sulanmada idrar inkontinansına bağlı kimyasal irritan dermatit mutlaka akla getirilmelidir.",
            "bulletPoints": [
                "Sabun, losyon ve antiseptikler kontakt dermatit tetikleyebilir.",
                "Eritemli papül, sulanma ve kabuklanma görülür.",
                "Yaşlılarda inkontinans ve idrar teması önemli irritan nedendir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "İnkontinansı olan yaşlı kadınlarda sürekli idrar teması şiddetli kontakt dermatit tablosuna neden olur.",
                    "maskedTerm": "idrar teması",
                    "hint": "Yaşlı hastalarda kimyasal maserasyona yol açan biyolojik sıvı teması"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Kontakt Vulvit: Akut ve Kronik Dönem Karşılaştırması",
                    "tableHeaders": ["Dönem", "Klinik Görünüm", "Baskın Histopatoloji"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Akut kontakt vulvit", "isMasked": False},
                                {"text": "Eritem, ödem ve sulanma", "isMasked": False},
                                {"text": "Spongiyoz ve vezikül oluşumu", "isMasked": True, "hint": "epidermal hücreler arası ödem"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Kronik kontakt vulvit", "isMasked": False},
                                {"text": "Kabuklanma ve doku kalınlaşması", "isMasked": True, "hint": "kuruma ve skuamasyon bulgusu"},
                                {"text": "Akantoz ve hiperkeratoz", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Kimyasal Temastan Egzematöz Lezyona",
                    "steps": [
                        "1. Kimyasal Temas: Antiseptik veya losyon katkı maddeleri vulva epidermisini irrite eder.",
                        "2. Keratinosit Hasarı: Epitel hücrelerinden sitokin ve kemokin salınımı tetiklenir.",
                        "3. Spongiyoz: Epidermal hücreler arasına sıvı birikerek mikroskopik veziküller oluşturur.",
                        "4. Eksüdasyon: Yüzeyde sulantılı eritemli plaklar ve kaşıntılı lezyonlar klinik olarak belirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Üriner inkontinansı olan yaşlı kadınlarda vulvada kontakt dermatit gelişiminin temel nedeni nedir?",
                    "answer": "Sürekli idrar teması sonucu cildin masere olması ve idrardaki üre/amonyak kaynaklı kimyasal doku irritasyonudur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Kontakt ve İrritan Vulvit Özellikleri",
                    "items": [
                        {"text": "Sabun, antiseptik ve losyon katkıları kontakt irritan dermatit gelişimini tetikleyebilir.", "isLie": False, "explanation": "Doğru. Kozmetik ve kimyasal temizleyiciler sık etyolojik ajanlardır."},
                        {"text": "Yaşlı hastalarda idrar sızıntısı ve inkontinans reaktif kontakt vulvite yol açabilir.", "isLie": False, "explanation": "Doğru. İdrar teması maserasyon ve kimyasal irritasyon doğurur."},
                        {"text": "Akut kontakt lezyonlar eritemli papüller ve sulantılı alanlarla karakterizedir.", "isLie": False, "explanation": "Doğru. Spongiyoz ve eksüdasyon akut evrenin tipik bulgusudur."},
                        {"text": "Alerjik kontakt vulvit yalnızca virüslerin doğrudan doku invazyonuyla ortaya çıkar.", "isLie": True, "explanation": "Tuzak! Kontakt dermatit mikrobiyal invazyonla değil kimyasal ve immünolojik irritan temasla oluşur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Alerjik ve kontakt irritan vulvit ile ilgili aşağıdaki ifadelerden hangisi YANLIŞTIR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Etyolojide daima cinsel yolla bulaşan zorunlu intraselüler bir virüs enfeksiyonu bulunur",
                            "isCorrect": True,
                            "explanation": "Kontakt vulvit enfeksiyöz değil kimyasal ve irritan kaynaklı reaktif bir cilt reaksiyonudur."
                        },
                        {
                            "key": "B",
                            "text": "Sabun ve antiseptiklerdeki katkı maddeleri alerjik reaksiyonu tetikleyebilir",
                            "isCorrect": False,
                            "explanation": "Bu maddeler bilinen ve sık karşılaşılan kimyasal tetikleyicilerdir."
                        },
                        {
                            "key": "C",
                            "text": "İnkontinansı bulunan yaşlı bireylerde idrar teması reaktif dermatite yol açar",
                            "isCorrect": False,
                            "explanation": "Sürekli idrar maruziyeti yaşlılarda önemli bir maserasyon ve vulvit nedenidir."
                        },
                        {
                            "key": "D",
                            "text": "Klinik lezyonlar iyi sınırlı eritemli papüller ve sulantılı alanlar şeklinde izlenebilir",
                            "isCorrect": False,
                            "explanation": "Bu bulgular akut kontakt dermatitin klasik dermatolojik belirtileridir."
                        }
                    ]
                }
            ]
        },
        # S4
        {
            "slideNumber": 4,
            "title": "Enfeksiyöz Vulvit: CYBH Patojenleri ve Cinsel Bulaş",
            "subtitle": "HPV, HSV, gonore ve sifiliz kaynaklı dış genital tutulumlar",
            "clinicalFocus": "CYBH ve Vulvit",
            "content": "Enfeksiyöz vulvit olgularının büyük bir çoğunluğu cinsel yolla bulaşan hastalıklar (CYBH) kapsamında gelişir. Farklı mikroorganizmalar vulvada kendilerine özgü histopatolojik ve klinik tablolar oluşturur.\n\n- **Human Papilloma Virus (HPV):** Düşük riskli tipleriyle ekzofitik siğiller (kondiloma akuminatum), yüksek riskli tipleriyle preinvaziv lezyonlar meydana getirir.\n- **Herpes Simplex Virus (HSV-1 ve HSV-2):** Ağrılı veziküller, yüzeyel ülserler ve tekrarlayıcı lezyonlarla seyreder; sinir ganglionlarında latent kalır.\n- **Neisseria gonorrhoeae:** Vulvovajinal bezlerin, özellikle de Bartholin bezlerinin akut süpüratif ve pürülan enfeksiyonlarına yol açar.\n- **Treponema pallidum:** İnkübasyon sonrası aşılama bölgesinde ağrısız, sert tabanlı primer şankr lezyonunu oluşturur.\n\n> [!IMPORTANT]\n> Enfeksiyöz vulvit etkenlerinin büyük kısmı cinsel yolla bulaşırken, Candida türleri cinsel yolla bulaşmayan kritik bir istisnadır.",
            "synthesisNarrative": "Enfeksiyöz vulvit olgularının büyük bir çoğunluğu cinsel yolla bulaşan hastalıklar (CYBH) kapsamında gelişir. Farklı mikroorganizmalar vulvada kendilerine özgü histopatolojik ve klinik tablolar oluşturur.\n\n- **Human Papilloma Virus (HPV):** Düşük riskli tipleriyle ekzofitik siğiller (kondiloma akuminatum), yüksek riskli tipleriyle preinvaziv lezyonlar meydana getirir.\n- **Herpes Simplex Virus (HSV-1 ve HSV-2):** Ağrılı veziküller, yüzeyel ülserler ve tekrarlayıcı lezyonlarla seyreder; sinir ganglionlarında latent kalır.\n- **Neisseria gonorrhoeae:** Vulvovajinal bezlerin, özellikle de Bartholin bezlerinin akut süpüratif ve pürülan enfeksiyonlarına yol açar.\n- **Treponema pallidum:** İnkübasyon sonrası aşılama bölgesinde ağrısız, sert tabanlı primer şankr lezyonunu oluşturur.\n\n> [!IMPORTANT]\n> Enfeksiyöz vulvit etkenlerinin büyük kısmı cinsel yolla bulaşırken, Candida türleri cinsel yolla bulaşmayan kritik bir istisnadır.",
            "bulletPoints": [
                "Çoğu enfeksiyöz vulvit cinsel yolla bulaşır.",
                "HPV siğil, HSV ağrılı vezikül ve ülser yapar.",
                "Gonore süpüratif bez enfeksiyonu, sifiliz şankr oluşturur."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Genital bölgede ağrılı vezikül ve ülserlerle seyreden tekrarlayıcı viral etken Herpes Simplex Virus enfeksiyonudur.",
                    "maskedTerm": "Herpes Simplex Virus",
                    "hint": "HSV-1 ve HSV-2 tipleriyle latent kalan viral ajan"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Cinsel Yolla Bulaşan Vulvit Etkenleri",
                    "tableHeaders": ["Patojen", "Bulaş Şekli", "Tipik Vulvar Lezyon"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Treponema pallidum", "isMasked": False},
                                {"text": "Cinsel temas", "isMasked": False},
                                {"text": "Primer sert şankr", "isMasked": True, "hint": "ağrısız endüre ülser"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Neisseria gonorrhoeae", "isMasked": False},
                                {"text": "Cinsel temas", "isMasked": False},
                                {"text": "Bezlerin süpüratif enfeksiyonu", "isMasked": True, "hint": "pürülan eksüda ve apse"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "HSV İnvazyonu ve Tekrarlayan Ülserler",
                    "steps": [
                        "1. İnokülasyon: HSV viryonları mukozal çatlaktan çok katlı yassı epitele giriş yapar.",
                        "2. İntraepitelyal Vezikül: İntraselüler çoğalma sonucu epitelde balonlaşma ve berrak veziküller gelişir.",
                        "3. Ülserasyon: Veziküller açılarak oldukça ağrılı, eritemli tabana sahip yüzeyel ülserlere dönüşür.",
                        "4. Latens: Virüs duyu sinirleri boyunca retrograd ilerleyerek sakral ganglionlarda sessiz faza geçer."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Enfeksiyöz vulvit etkenlerinden Neisseria gonorrhoeae vulvada en çok hangi anatomik yapıları hedef alır?",
                    "answer": "Bartholin bezleri başta olmak üzere vulvovajinal salgı bezlerini hedef alarak akut süpüratif enfeksiyona yol açar."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "CYBH Kaynaklı Vulvit Etkenleri",
                    "items": [
                        {"text": "Herpes Simplex Virus ağrılı veziküller ve yüzeyel ülserasyonlarla seyreder.", "isLie": False, "explanation": "Doğru. HSV lezyonları tipik olarak oldukça ağrılı vezikülo-ülseratif karakterdedir."},
                        {"text": "Treponema pallidum inokülasyon sahasında primer şankr lezyonunu oluşturur.", "isLie": False, "explanation": "Doğru. Primer sifilizin klasik bulgusu ağrısız şankrdır."},
                        {"text": "Neisseria gonorrhoeae vulvovajinal bezlerde süpüratif inflamasyona yol açabilir.", "isLie": False, "explanation": "Doğru. Gonore bez kanallarını tutarak süpürasyon ve apse yapar."},
                        {"text": "Treponema pallidum vulvada yalnızca kaşıntısız selim epidermoid kistler üretir.", "isLie": True, "explanation": "Tuzak! Sifiliz primer evrede tipik endüre tabanlı şankr ülseri oluşturur; kist yapmaz."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Enfeksiyöz vulvit etkenleri ve klinik özellikleri ile ilgili aşağıdaki eşleştirmelerden hangisi YANLIŞTIR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Treponema pallidum — Vulvar mukozada ağrılı döküntüsüz lipom oluşumu",
                            "isCorrect": True,
                            "explanation": "Treponema pallidum primer sifilizde sert tabanlı şankr ülseri yapar, lipom selim bir yağ dokusu tümörüdür."
                        },
                        {
                            "key": "B",
                            "text": "Herpes Simplex Virus — Ağrılı veziküller ve tekrarlayıcı yüzeyel ülserler",
                            "isCorrect": False,
                            "explanation": "Bu eşleştirme HSV-1 ve HSV-2 enfeksiyonunun kardinal klinik tablosudur."
                        },
                        {
                            "key": "C",
                            "text": "Neisseria gonorrhoeae — Vulvovajinal bezlerin akut pürülan süpürasyonu",
                            "isCorrect": False,
                            "explanation": "Gonokoklar bez kanallarında süpüratif yangı ve apse yapmaya yatkındır."
                        },
                        {
                            "key": "D",
                            "text": "Human Papilloma Virus — Ekzofitik genital siğiller (kondiloma akuminatum)",
                            "isCorrect": False,
                            "explanation": "Düşük riskli HPV tipleri (6 ve 11) tipik kondilom lezyonlarına yol açar."
                        }
                    ]
                }
            ]
        },
        # S5
        {
            "slideNumber": 5,
            "title": "Candida Vulviti: Cinsel Olmayan Fırsatçı Mikoz",
            "subtitle": "Risk faktörleri, psödohif oluşumu ve beyaz plak morfolojisi",
            "clinicalFocus": "Candida Vulviti",
            "content": "Candida türleri (en sık Candida albicans), kadın genital sisteminde normal mikrobiyal floranın kommensal bir üyesi olarak bulunabilen ancak uygun konak koşullarında aşırı çoğalarak vulvite yol açan bir mantardır.\n\n- **Bulaş Özelliği:** Candida vulviti cinsel yolla bulaşan bir enfeksiyon DEĞİLDİR; fırsatçı bir endojen alevlenmedir.\n- **Yatkınlaştırıcı Faktörler:** Kontrolsüz diyabet mellitus (glikozüri), geniş spektrumlu antibiyotik kullanımı (laktobasil florasının baskılanması), gebelik ve immün yetmezlik en önemli tetikleyicilerdir.\n- **Klinik ve Morfoloji:** Şiddetli vulvar kaşıntı, yoğun eritem, ödem ve mukoza üzerinde peynirimsi, süte benzer beyaz plak lezyonları ile karakterizedir; vajinit ile sıklıkla birliktedir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Kurul sınavlarında sıkça sorulur: Vulvit etkenleri arasında cinsel yolla bulaşmayan, fırsatçı proliferasyonla gelişen temel mikotik ajan Candida türleridir.",
            "synthesisNarrative": "Candida türleri (en sık Candida albicans), kadın genital sisteminde normal mikrobiyal floranın kommensal bir üyesi olarak bulunabilen ancak uygun konak koşullarında aşırı çoğalarak vulvite yol açan bir mantardır.\n\n- **Bulaş Özelliği:** Candida vulviti cinsel yolla bulaşan bir enfeksiyon DEĞİLDİR; fırsatçı bir endojen alevlenmedir.\n- **Yatkınlaştırıcı Faktörler:** Kontrolsüz diyabet mellitus (glikozüri), geniş spektrumlu antibiyotik kullanımı (laktobasil florasının baskılanması), gebelik ve immün yetmezlik en önemli tetikleyicilerdir.\n- **Klinik ve Morfoloji:** Şiddetli vulvar kaşıntı, yoğun eritem, ödem ve mukoza üzerinde peynirimsi, süte benzer beyaz plak lezyonları ile karakterizedir; vajinit ile sıklıkla birliktedir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Kurul sınavlarında sıkça sorulur: Vulvit etkenleri arasında cinsel yolla bulaşmayan, fırsatçı proliferasyonla gelişen temel mikotik ajan Candida türleridir.",
            "bulletPoints": [
                "Candida cinsel yolla bulaşmaz; fırsatçı çoğalır.",
                "Diyabet, antibiyotik ve gebelik yatkınlık yaratır.",
                "Şiddetli kaşıntı, eritem ve beyaz peynirimsi plaklar görülür."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vulvit etkenleri arasında yer alan Candida türleri cinsel yolla bulaşmaz ve fırsatçı karakterdedir.",
                    "maskedTerm": "cinsel yolla bulaşmaz",
                    "hint": "Diğer enfeksiyöz vulvit etkenlerinden ayrılan temel bulaş özelliği"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Candida Vulviti Yatkınlaştırıcı Faktörleri",
                    "tableHeaders": ["Risk Faktörü", "Patofizyolojik Mekanizma", "Klinik Etki"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Geniş spektrumlu antibiyotik", "isMasked": False},
                                {"text": "Koruyucu laktobasil florasının yok edilmesi", "isMasked": True, "hint": "yararlı bakterilerin ölümü"},
                                {"text": "Mantarların kontrolsüz çoğalması", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Diyabet mellitus", "isMasked": False},
                                {"text": "Dokuda ve idrarda glukoz artışı", "isMasked": False},
                                {"text": "Candida için zengin besiyeri ortamı", "isMasked": True, "hint": "mikotik üremeyi hızlandıran enerji kaynağı"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Antibiyotikten Candida Vulvitine",
                    "steps": [
                        "1. Antibiyotik Kullanımı: Sistemik antibiyotik vajinal floradaki koruyucu laktobasilleri öldürür.",
                        "2. pH ve Rekabet Kaybı: Asidik ortam zayıflar ve mikrobiyal denge mantarlar lehine bozulur.",
                        "3. Aşırı Proliferasyon: Kommensal Candida albicans blastosporlardan psödohif ve hif formuna geçer.",
                        "4. Dokusal Yangı: Yüzeyel mukozada beyaz peynirimsi plaklar ve şiddetli eritemli vulvit tablosu belirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Candida vulvitini diğer enfeksiyöz vulvitlerden (HPV, HSV, gonore, sifiliz) ayıran en temel epidemiyolojik fark nedir?",
                    "answer": "Candida cinsel yolla bulaşan bir enfeksiyon değildir; flora dengesinin bozulmasıyla gelişen endojen fırsatçı mikozdur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Candida Vulvitinin Özellikleri",
                    "items": [
                        {"text": "Candida vulviti cinsel yolla bulaşan klasik enfeksiyonlar grubunda yer almaz.", "isLie": False, "explanation": "Doğru. Candida endojen floranın fırsatçı çoğalmasıyla oluşur."},
                        {"text": "Geniş spektrumlu antibiyotik tedavisi laktobasilleri azaltarak Candida riskini artırır.", "isLie": False, "explanation": "Doğru. Koruyucu floranın çöküşü mantar üremesine kapı açar."},
                        {"text": "Klinikte yoğun kaşıntı, eritem ve beyaz peynirimsi plaklar tipiktir.", "isLie": False, "explanation": "Doğru. Bu tablo Candida enfeksiyonunun klasik klinik görünümüdür."},
                        {"text": "Candida kesinlikle insandan insana yalnızca zorunlu cinsel temasla bulaşır.", "isLie": True, "explanation": "Tuzak! Candida cinsel yolla bulaşmaz; flora dengesi bozulan hastada fırsatçı olarak alevlenir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvit etkenleri arasında hangisi cinsel yolla bulaşmayan, flora bozulmasıyla ortaya çıkan bir ajandır?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Candida türleri",
                            "isCorrect": True,
                            "explanation": "Candida normal florada bulunabilen ve cinsel yolla bulaşmayan fırsatçı bir mantardır."
                        },
                        {
                            "key": "B",
                            "text": "Neisseria gonorrhoeae",
                            "isCorrect": False,
                            "explanation": "Gonokok cinsel yolla bulaşan süpüratif bir bakteriyel patojendir."
                        },
                        {
                            "key": "C",
                            "text": "Treponema pallidum",
                            "isCorrect": False,
                            "explanation": "Treponema cinsel temasla bulaşıp primer şankr oluşturan spirokettir."
                        },
                        {
                            "key": "D",
                            "text": "Herpes Simplex Virus tip 2",
                            "isCorrect": False,
                            "explanation": "HSV-2 cinsel temasla bulaşan ve ağrılı veziküller yapan viral ajandır."
                        }
                    ]
                }
            ]
        },
        # S6
        {
            "slideNumber": 6,
            "title": "Bartholin Bezi Komplikasyonları: Kist ve Apse Patolojisi",
            "subtitle": "Kanal tıkanıklığı, müsinöz dilatasyon ve süpüratif enfeksiyon",
            "clinicalFocus": "Bartholin Kisti ve Apsesi",
            "content": "Bartholin bezleri (büyük vestibüler bezler), introitusun posterolateralinde yer alan ve vestibülü kayganlaştıran müsinöz salgı üreten bezlerdir. Kanallarının tıkanması vulvitin en önemli cerrahi komplikasyonlarındandır.\n\n- **Kanal Tıkanıklığı ve Kist Oluşumu:** Vulvitteki inflamasyon, epitel döküntüleri veya mekanik travma ana boşaltım kanalını tıkar. Salgılanmaya devam eden mukus bezi gerer ve ağrısız/hafif ağrılı **Bartholin kisti** gelişir.\n- **Sekonder Enfeksiyon ve Apse:** Tıkalı kist sıvısı stafilokoklar, streptokoklar veya Neisseria gonorrhoeae gibi bakterilerle enfekte olduğunda hızla **Bartholin apsesine** dönüşür.\n- **Klinik ve Tedavi:** Apse geliştiğinde hasta oturmakta ve yürümekte zorlanır; şiddetli zonklayıcı ağrı, eritem ve fluktuasyon veren kitle izlenir. Tedavide cerrahi drenaj (marsupiyalizasyon) ve antibiyotik gerekir.\n\n> [!NOTE]\n> Bartholin kisti selim bir duktal retansiyon kistidir; ancak süperenfeksiyonla apseleştiğinde vulvanın en ağrılı acil cerrahi durumlarından birini oluşturur.",
            "synthesisNarrative": "Bartholin bezleri (büyük vestibüler bezler), introitusun posterolateralinde yer alan ve vestibülü kayganlaştıran müsinöz salgı üreten bezlerdir. Kanallarının tıkanması vulvitin en önemli cerrahi komplikasyonlarındandır.\n\n- **Kanal Tıkanıklığı ve Kist Oluşumu:** Vulvitteki inflamasyon, epitel döküntüleri veya mekanik travma ana boşaltım kanalını tıkar. Salgılanmaya devam eden mukus bezi gerer ve ağrısız/hafif ağrılı **Bartholin kisti** gelişir.\n- **Sekonder Enfeksiyon ve Apse:** Tıkalı kist sıvısı stafilokoklar, streptokoklar veya Neisseria gonorrhoeae gibi bakterilerle enfekte olduğunda hızla **Bartholin apsesine** dönüşür.\n- **Klinik ve Tedavi:** Apse geliştiğinde hasta oturmakta ve yürümekte zorlanır; şiddetli zonklayıcı ağrı, eritem ve fluktuasyon veren kitle izlenir. Tedavide cerrahi drenaj (marsupiyalizasyon) ve antibiyotik gerekir.\n\n> [!NOTE]\n> Bartholin kisti selim bir duktal retansiyon kistidir; ancak süperenfeksiyonla apseleştiğinde vulvanın en ağrılı acil cerrahi durumlarından birini oluşturur.",
            "bulletPoints": [
                "Bartholin bezi kanalı tıkanırsa retansiyon kisti gelişir.",
                "Enfeksiyon eklenirse ağrılı ve fluktuan apse tablosu oluşur.",
                "Tedavide drenaj (marsupiyalizasyon) ve antibiyoterapi uygulanır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Bartholin bezi salgı kanalının inflamatuvar tıkanması sonucu gelişen ağrılı kistik genişlemeye Bartholin kisti denir.",
                    "maskedTerm": "Bartholin kisti",
                    "hint": "Vestibülün posterolateralinde oluşan retansiyon kisti"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bartholin Kisti ve Apsesi Ayrımı",
                    "tableHeaders": ["Özellik", "Bartholin Kisti", "Bartholin Apsesi"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Ağrı Şiddeti", "isMasked": False},
                                {"text": "Ağrısız veya hafif gerginlik hissi", "isMasked": False},
                                {"text": "Şiddetli, zonklayıcı dayanılmaz ağrı", "isMasked": True, "hint": "akut süpüratif gerilim"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "İçerik", "isMasked": False},
                                {"text": "Steril berrak müsinöz sıvı", "isMasked": True, "hint": "bez salgısının birikimi"},
                                {"text": "Pürülan eksüda ve bakteri infiltrasyonu", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Kanal Tıkanmasından Apseleşmeye",
                    "steps": [
                        "1. İnflamasyon: Vulvit veya lokal travma Bartholin bezi duktus lümeninde ödem ve daralma yapar.",
                        "2. Duktal Obstrüksiyon: Mukus boşalamaz ve retrograd basınçla bez lümeni kistik olarak dilate olur.",
                        "3. Bakteriyel Kolonizasyon: Stazdaki müsinöz içeriğe patojen bakteriler (gonokok, anaeroblar) yerleşir.",
                        "4. Apseleşme: Doku nekrozu ve nötrofil akınıyla zonklayıcı ağrılı, fluktuan apse kitlesi gelişir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bartholin kistinin primer oluşum mekanizması nedir ve apseden nasıl ayrılır?",
                    "answer": "Boşaltım kanalının tıkanmasıyla mukusun birikmesi sonucu oluşur; kist steril ve az ağrılıyken, apse bakteriyel süpürasyonla yoğun pürülan eksüda ve şiddetli zonklayıcı ağrı içerir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Bartholin Bezi Patolojileri",
                    "items": [
                        {"text": "Bartholin bezi introitusun posterolateralinde yer alan müsinöz salgı bezidir.", "isLie": False, "explanation": "Doğru. Anatomik konumu vestibülün arka yan kenarıdır."},
                        {"text": "Kanal obstrüksiyonu kistik dilatasyona ve Bartholin kistine yol açar.", "isLie": False, "explanation": "Doğru. Akım engeli gerilme kisti oluşturur."},
                        {"text": "Apse geliştiğinde zonklayıcı ağrı, eritem ve fluktuasyon izlenir.", "isLie": False, "explanation": "Doğru. Akut apse kliniği son derece gürültülüdür."},
                        {"text": "Bartholin kistleri embriyolojik Wolff kanalının kalıntısından gelişen mezonefrik yapılardır.", "isLie": True, "explanation": "Tuzak! Bartholin bezleri normal anatomik yapılardır; Wolff kanal kalıntısından gelişen kist vajinadaki Gartner kistidir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Bartholin bezi patolojileri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Kanal tıkanması sonucu mukus birikimiyle kist, bakteriyel süperenfeksiyonla apse gelişir",
                            "isCorrect": True,
                            "explanation": "Kanal obstrüksiyonu kisti oluşturur; enfeksiyon eklenmesi ise apseleşmeye yol açar."
                        },
                        {
                            "key": "B",
                            "text": "Bartholin apsesi her zaman ağrısızdır ve cerrahi drenaja asla ihtiyaç duymaz",
                            "isCorrect": False,
                            "explanation": "Apse son derece ağrılıdır ve cerrahi drenaj (marsupiyalizasyon) gerektirir."
                        },
                        {
                            "key": "C",
                            "text": "Bartholin bezleri klitoris tepesinde yerleşmiş yağ bezleridir",
                            "isCorrect": False,
                            "explanation": "Bartholin bezleri introitusun posterolateralinde yer alan müsinöz bezlerdir."
                        },
                        {
                            "key": "D",
                            "text": "Bartholin kistleri yalnızca menopoz sonrasında ortaya çıkan malign lezyonlardır",
                            "isCorrect": False,
                            "explanation": "Genellikle üreme çağında görülen tamamen benign retansiyon kistleridir."
                        }
                    ]
                }
            ]
        },
        # S7
        {
            "slideNumber": 7,
            "title": "Vulvada Non-Neoplastik Epitel Bozuklukları ve Lökoplaki Kavramı",
            "subtitle": "Klinik lökoplaki görünümü, biyopsi zorunluluğu ve patoloji ayrımı",
            "clinicalFocus": "Lökoplaki ve Epitel Bozuklukları",
            "content": "Non-neoplastik epitel bozuklukları, vulva cildinde neoplazi olmaksızın gelişen kronik morfolojik değişikliklerdir. Bu lezyonlar klinisyenin karşısına sıklıkla beyaz plak veya lekeler (**lökoplaki**) şeklinde çıkar.\n\n- **Lökoplaki Tanımı:** Kazımakla çıkmayan, beyaz renkli, plak benzeri mukozal veya kutanöz kalınlaşmadır. Lökoplaki patolojik bir tanı değil, klinik ve morfolojik bir tanımlamadır.\n- **İki Temel Tablo:** Non-neoplastik spektrumun iki ana prototipi **liken skleroz** ve **skuamöz hücre hiperplazisidir**.\n- **Malignite ve Ayırıcı Tanı:** Benign dermatozlar (psoriasis, liken planus) lökoplaki yapabileceği gibi, in situ karsinom ve invaziv skuamöz hücreli karsinom da birebir aynı beyaz plak görünümüyle başlayabilir.\n\n> [!IMPORTANT]\n> [KRİTİK UYARI] Her lökoplaki lezyonunda altta yatan malign veya premalign süreçleri dışlamak için biyopsi ve mikroskobik inceleme ZORUNLUDUR.",
            "synthesisNarrative": "Non-neoplastik epitel bozuklukları, vulva cildinde neoplazi olmaksızın gelişen kronik morfolojik değişikliklerdir. Bu lezyonlar klinisyenin karşısına sıklıkla beyaz plak veya lekeler (**lökoplaki**) şeklinde çıkar.\n\n- **Lökoplaki Tanımı:** Kazımakla çıkmayan, beyaz renkli, plak benzeri mukozal veya kutanöz kalınlaşmadır. Lökoplaki patolojik bir tanı değil, klinik ve morfolojik bir tanımlamadır.\n- **İki Temel Tablo:** Non-neoplastik spektrumun iki ana prototipi **liken skleroz** ve **skuamöz hücre hiperplazisidir**.\n- **Malignite ve Ayırıcı Tanı:** Benign dermatozlar (psoriasis, liken planus) lökoplaki yapabileceği gibi, in situ karsinom ve invaziv skuamöz hücreli karsinom da birebir aynı beyaz plak görünümüyle başlayabilir.\n\n> [!IMPORTANT]\n> [KRİTİK UYARI] Her lökoplaki lezyonunda altta yatan malign veya premalign süreçleri dışlamak için biyopsi ve mikroskobik inceleme ZORUNLUDUR.",
            "bulletPoints": [
                "Lökoplaki klinik bir tanımlamadır; patolojik tanı değildir.",
                "Liken skleroz ve skuamöz hiperplazi ana tablolardır.",
                "Maligniteyi dışlamak için mutlaka biyopsi alınmalıdır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vulvada kazımakla çıkmayan beyaz plak görünümü veren klinik lezyona lökoplaki adı verilir.",
                    "maskedTerm": "lökoplaki",
                    "hint": "Beyaz plak anlamına gelen tanımlayıcı klinik terim"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulva Lökoplakisinin Ayırıcı Tanı Yelpazesi",
                    "tableHeaders": ["Kategori", "Örnek Hastalıklar", "Klinik Anlam"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Non-neoplastik bozukluk", "isMasked": False},
                                {"text": "Liken skleroz ve skuamöz hücre hiperplazisi", "isMasked": False},
                                {"text": "kronik distrofik epitel yanıtı", "isMasked": True, "hint": "inflamatuvar ve sklerozan zemin"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Malign / Premalign", "isMasked": False},
                                {"text": "VIN ve invaziv skuamöz hücreli karsinom", "isMasked": True, "hint": "neoplastik epitelyal süreçler"},
                                {"text": "Biyopsi ile kesin dışlama zorunluluğu", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Lökoplakiden Biyopsi Kararına",
                    "steps": [
                        "1. Beyaz Plak: Vulva muayenesinde kazınamayan opak, beyaz porselenimsi lökoplaki alanı saptanır.",
                        "2. Klinik Sınır: Gözle muayene ile lezyonun selim liken mi yoksa invaziv karsinom mu olduğu anlaşılamaz.",
                        "3. Biyopsi İhtiyacı: Histopatolojik mimariyi ve olası sitolojik atipiyi görmek için doku örneği alınır.",
                        "4. Doğru Tedavi: Biyopsi sonucuna göre medikal kortikosteroid ya da onkolojik cerrahi planlanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulva lökoplakisi neden tek başına nihai bir patoloji tanısı olarak kabul edilemez?",
                    "answer": "Çünkü lökoplaki yalnızca beyaz plak görünümünü tanımlayan klinik bir terimdir; altında liken skleroz gibi benign lezyonlar da invaziv kanser de yatabilir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vulvada Lökoplaki ve Ayırıcı Tanı",
                    "items": [
                        {"text": "Lökoplaki klinik bir tanımlama olup kazımakla çıkmayan beyaz lezyonları ifade eder.", "isLie": False, "explanation": "Doğru. Klinik tanımlamadır ve histolojiyi yansıtmaz."},
                        {"text": "Psoriasis ve liken planus gibi benign dermatolojik tablolar lökoplaki yapabilir.", "isLie": False, "explanation": "Doğru. Bu selim inflamatuvar hastalıklar beyaz plak oluşturabilir."},
                        {"text": "Her vulva lökoplakisinde maligniteyi dışlamak amacıyla biyopsi yapılması şarttır.", "isLie": False, "explanation": "Doğru. Biyopsi kesin ayrım için altın standarttır."},
                        {"text": "Lökoplaki tanısı konulan her olgu doğrudan ileri evre metastatik sarkom kabul edilir.", "isLie": True, "explanation": "Tuzak! Lökoplaki bir sarkom değil, sıklıkla selim dermatozların oluşturduğu klinik bir beyaz plak görünümüdür."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvada lökoplaki saptanan bir hastada klinik yaklaşım ile ilgili hangisi KESİNLİKLE DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Kesin histopatolojik ayrım ve maligniteyi dışlamak için biyopsi ve mikroskobik inceleme zorunludur",
                            "isCorrect": True,
                            "explanation": "Lökoplakinin altında selim dermatoz da invaziv kanser de bulunabileceğinden biyopsi şarttır."
                        },
                        {
                            "key": "B",
                            "text": "Lökoplaki patolojik bir tanıdır ve biyopsi yapılmasına hiçbir koşulda gerek yoktur",
                            "isCorrect": False,
                            "explanation": "Lökoplaki patolojik değil klinik bir tanıdır, biyopsi zorunludur."
                        },
                        {
                            "key": "C",
                            "text": "Lökoplaki lezyonları kazındığında tabakalar halinde kolayca soyulup dökülür",
                            "isCorrect": False,
                            "explanation": "Lökoplaki kazımakla çıkmayan mukozal/kutanöz kalınlaşmadır."
                        },
                        {
                            "key": "D",
                            "text": "Tüm lökoplakiler istisnasız olarak yüksek riskli HPV enfeksiyonuna bağlıdır",
                            "isCorrect": False,
                            "explanation": "Liken skleroz, skuamöz hiperplazi ve psoriasis gibi HPV dışı birçok neden lökoplaki yapar."
                        }
                    ]
                }
            ]
        },
        # S8
        {
            "slideNumber": 8,
            "title": "Liken Skleroz: Klinik Özellikler ve Atrofik Dönüşüm",
            "subtitle": "Parşömen kağıdı derisi, introital daralma ve otoimmün zemin",
            "clinicalFocus": "Liken Skleroz Kliniği",
            "content": "Liken skleroz, vulvanın en sık görülen kronik sklerozan ve atrofik dermatozudur. Her yaşta ortaya çıkabilmekle birlikte en sık menopoz sonrası ileri yaştaki kadınlarda ve ergenlik öncesi kız çocuklarında görülür.\n\n- **Klinik Tablo:** Hastalar başlangıçta düz, fildişi beyazı plaklar veya papüllerle gelir. Zamanla lezyonlar birleşerek porselenimsi, buruşuk, incelmiş bir görünüm alır (parşömen kağıdı derisi).\n- **Anatomik Deformasyon:** Kronik süreç labia majora ve minorada atrofiye, labiumların birbirine yapışmasına ve vajinal açıklığın (introitus) daralmasına (stenoz) neden olur.\n- **Patogenez ve Birliktelik:** Kesin mekanizma bilinmemekle birlikte T hücre aracılı otoimmünite suçlanmaktadır; tiroidit ve vitiligo gibi diğer otoimmün hastalıklarla sık birliktelik gösterir.\n\n> [!NOTE]\n> Liken sklerozda labia minoranın silinmesi ve introital stenoz gelişmesi cinsel ilişkide şiddetli ağrıya (disparoni) yol açar.",
            "synthesisNarrative": "Liken skleroz, vulvanın en sık görülen kronik sklerozan ve atrofik dermatozudur. Her yaşta ortaya çıkabilmekle birlikte en sık menopoz sonrası ileri yaştaki kadınlarda ve ergenlik öncesi kız çocuklarında görülür.\n\n- **Klinik Tablo:** Hastalar başlangıçta düz, fildişi beyazı plaklar veya papüllerle gelir. Zamanla lezyonlar birleşerek porselenimsi, buruşuk, incelmiş bir görünüm alır (parşömen kağıdı derisi).\n- **Anatomik Deformasyon:** Kronik süreç labia majora ve minorada atrofiye, labiumların birbirine yapışmasına ve vajinal açıklığın (introitus) daralmasına (stenoz) neden olur.\n- **Patogenez ve Birliktelik:** Kesin mekanizma bilinmemekle birlikte T hücre aracılı otoimmünite suçlanmaktadır; tiroidit ve vitiligo gibi diğer otoimmün hastalıklarla sık birliktelik gösterir.\n\n> [!NOTE]\n> Liken sklerozda labia minoranın silinmesi ve introital stenoz gelişmesi cinsel ilişkide şiddetli ağrıya (disparoni) yol açar.",
            "bulletPoints": [
                "Menopoz sonrası kadınlarda ve ergenlik öncesinde sıktır.",
                "Parşömen kağıdı benzeri beyaz buruşuk plaklar yapar.",
                "Labial atrofiye ve vajinal açıklık daralmasına neden olur."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Liken skleroz zemininde labiumların atrofisi ve skarlaşması sonucu vajinal açıklık daralabilir.",
                    "maskedTerm": "vajinal açıklık",
                    "hint": "İntroitus olarak adlandırılan genital giriş anatomisi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Liken Sklerozun Klinik ve Demografik Profili",
                    "tableHeaders": ["Parametre", "Özellik", "Klinik Detay"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Yaş Dağılımı", "isMasked": False},
                                {"text": "Bimodal pik", "isMasked": False},
                                {"text": "postmenopozal kadınlar ve prepubertal kızlar", "isMasked": True, "hint": "en sık görülen iki yaş grubu"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Makroskopi", "isMasked": False},
                                {"text": "Parşömen kağıdı derisi", "isMasked": True, "hint": "buruşuk beyaz fildişi manzara"},
                                {"text": "Beyaz, atrofik ve sert plaklar", "isMasked": False}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Liken Sklerozda Atrofi ve Darlık Gelişimi",
                    "steps": [
                        "1. İmmün Saldırı: Subepitelyal dermise aktive T lenfositler infiltre olur.",
                        "2. Dermal Skleroz: Dermal bağ dokusunda aselüler kollajen birikimi ve fibrozis gelişir.",
                        "3. Epitelyal Atrofi: Üstteki epidermis incelir ve elastikiyetini kaybederek buruşur.",
                        "4. Skarlaşma: Labialar silinir, introitus daralır ve disparoni ortaya çıkar."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Liken sklerozun vulvada yol açtığı karakteristik anatomik deformiteler nelerdir?",
                    "answer": "Labia minoranın atrofiye uğrayarak silinmesi, labiumların birbirine yapışması ve vajinal introitusun daralmasıdır (stenoz)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Liken Skleroz Kliniği ve Epidemiyolojisi",
                    "items": [
                        {"text": "Liken skleroz en sık menopoz sonrası kadınlarda ve ergenlik öncesi kızlarda görülür.", "isLie": False, "explanation": "Doğru. Bimodal yaş dağılımı tipiktir."},
                        {"text": "Klinikte parşömen kağıdı benzeri buruşuk beyaz plaklar izlenir.", "isLie": False, "explanation": "Doğru. Doku incelir ve parşömen görünümü alır."},
                        {"text": "Kronik olgularda vajinal introitusta daralma ve labial silinme gelişebilir.", "isLie": False, "explanation": "Doğru. Skleroz anatomik mimariyi bozar."},
                        {"text": "Liken skleroz genç erkeklerde en sık görülen bulaşıcı bakteriyel üretrittir.", "isLie": True, "explanation": "Tuzak! Liken skleroz kadın vulvasının otoimmün sklerozan dermatozudur; bakteriyel üretrit değildir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Liken sklerozun klinik özellikleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Menopoz sonrası kadınlarda parşömen kağıdı benzeri beyaz atrofik plaklar ve introital darlık oluşturur",
                            "isCorrect": True,
                            "explanation": "Liken sklerozun klasik demografik ve klinik tablosu budur."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca gebelik döneminde görülen geçici ve akut süpüratif bir tablodur",
                            "isCorrect": False,
                            "explanation": "Liken skleroz kronik bir dermatozdur, en sık postmenopozal dönemde izlenir."
                        },
                        {
                            "key": "C",
                            "text": "Lezyonlar daima aşırı hipertrofik, kırmızı ve polipoid kitleler halindedir",
                            "isCorrect": False,
                            "explanation": "Lezyonlar polipoid değil, düz/buruşuk beyaz atrofik plaklardır."
                        },
                        {
                            "key": "D",
                            "text": "Anatomik yapılarda hiçbir zaman silinme veya introitus stenozu yapmaz",
                            "isCorrect": False,
                            "explanation": "İlerlemiş vakalarda labial silinme ve introital darlık en önemli komplikasyondur."
                        }
                    ]
                }
            ]
        },
        # S9
        {
            "slideNumber": 9,
            "title": "Liken Skleroz Histopatolojisi ve Kanser Riski",
            "subtitle": "Epidermis incelmesi, dermal homojen fibrozis ve skuamöz karsinom ilişkisi",
            "clinicalFocus": "Histopatoloji ve Onkolojik Risk",
            "content": "Liken skleroz tanısı, karakteristik mikroskobik mimarinin biyopside gösterilmesiyle kesinleşir. Bu histopatolojik bulgular hastalığın kronik atrofik doğasını yansıtır.\n\n- **Dört Kardinal Histolojik Bulgu:**\n  1. Epidermiste belirgin incelme (atrofi),\n  2. Rete çıkıntılarının düzleşmesi ve tamamen kaybı,\n  3. Yüzeyel dermiste hücresiz, homojen, camsı kollajenöz fibrozis bandı (skleroz),\n  4. Bu fibrotik zonun hemen altında bant tarzında mononükleer (T lenfositik) inflamatuvar infiltrat.\n- **Onkolojik Risk Değerlendirmesi:** Liken skleroz tek başına bir prekanseröz lezyon DEĞİLDİR. Ancak liken skleroz zemininde vulvar skuamöz hücreli karsinom gelişme riski hafif düzeyde (%1-5) artmıştır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Liken skleroz prekanseröz kabul edilmez; fakat uzun süreli kronik epitel irritasyonu ve doku hasarı nedeniyle HPV-negatif keratinize skuamöz hücreli karsinoma zemin hazırlayabilir. Bu nedenle hastalar uzun dönem takip edilmelidir.",
            "synthesisNarrative": "Liken skleroz tanısı, karakteristik mikroskobik mimarinin biyopside gösterilmesiyle kesinleşir. Bu histopatolojik bulgular hastalığın kronik atrofik doğasını yansıtır.\n\n- **Dört Kardinal Histolojik Bulgu:**\n  1. Epidermiste belirgin incelme (atrofi),\n  2. Rete çıkıntılarının düzleşmesi ve tamamen kaybı,\n  3. Yüzeyel dermiste hücresiz, homojen, camsı kollajenöz fibrozis bandı (skleroz),\n  4. Bu fibrotik zonun hemen altında bant tarzında mononükleer (T lenfositik) inflamatuvar infiltrat.\n- **Onkolojik Risk Değerlendirmesi:** Liken skleroz tek başına bir prekanseröz lezyon DEĞİLDİR. Ancak liken skleroz zemininde vulvar skuamöz hücreli karsinom gelişme riski hafif düzeyde (%1-5) artmıştır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Liken skleroz prekanseröz kabul edilmez; fakat uzun süreli kronik epitel irritasyonu ve doku hasarı nedeniyle HPV-negatif keratinize skuamöz hücreli karsinoma zemin hazırlayabilir. Bu nedenle hastalar uzun dönem takip edilmelidir.",
            "bulletPoints": [
                "Epidermis incelir, rete çıkıntıları silinir.",
                "Yüzeyel dermiste hücresiz homojen fibrozis ve altta bant infiltrat bulunur.",
                "Prekanseröz değildir; ancak vulvar SCC riski hafif artmıştır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Liken skleroz biyopsisinde yüzeyel dermiste hücresiz homojen fibrozis bandı karakteristiktir.",
                    "maskedTerm": "homojen fibrozis",
                    "hint": "Aselüler camsı kollajenöz skleroz tabakası"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Liken Skleroz Mikroskobik Katmanları",
                    "tableHeaders": ["Doku Katmanı", "Histopatolojik Değişiklik", "Ayırıcı Özellik"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Epidermis", "isMasked": False},
                                {"text": "Belirgin incelme ve atrofi", "isMasked": True, "hint": "katman sayısında azalma"},
                                {"text": "Rete çıkıntılarının kaybı", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Yüzeyel Dermis", "isMasked": False},
                                {"text": "Hücresiz sklerozan kollajen bandı", "isMasked": False},
                                {"text": "Derininde bant tarzı lenfosit infiltratı", "isMasked": True, "hint": "kronik mononükleer hücre kuşağı"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Liken Sklerozdan Karsinom Riskine",
                    "steps": [
                        "1. Kronik Skleroz: Liken skleroz zemininde epidermal atrofi ve dermal skleroz kalıcı hale gelir.",
                        "2. Kronik İrritasyon: İncelmiş epitel sürekli kaşıma ve mikrotravmalarla hasarlanır.",
                        "3. Artmış Hücre Döngüsü: Epitelyal onarım sürecinde sürücü genetik mutasyon birikimi tetiklenir.",
                        "4. Malign Transformasyon: Olguların küçük bir kısmında (%1-5) HPV-negatif keratinize SCC gelişebilir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Liken sklerozun histopatolojisindeki dört temel mikroskobik bulgu nedir?",
                    "answer": "1. Epidermis incelmesi (atrofi), 2. Rete çıkıntılarının kaybı, 3. Yüzeyel dermiste hücresiz homojen fibrozis bandı, 4. Fibrozisin altında bant tarzı mononükleer lenfositik infiltrat."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Liken Skleroz Histopatolojisi ve Onkolojik Risk",
                    "items": [
                        {"text": "Liken sklerozda epidermis incelir ve rete çıkıntıları silinir.", "isLie": False, "explanation": "Doğru. Epitelyal atrofi kardinal histolojik bulgudur."},
                        {"text": "Yüzeyel dermiste hücresiz homojen camsı fibrozis alanı izlenir.", "isLie": False, "explanation": "Doğru. Sklerotik bant liken skleroz için patognomoniktir."},
                        {"text": "Liken skleroz prekanseröz bir lezyon değildir ancak SCC riskini biraz artırır.", "isLie": False, "explanation": "Doğru. Doğrudan karsinoma in situ sayılmaz ama zemininde SCC gelişebilir."},
                        {"text": "Liken skleroz biyopsisinde dermis tümüyle nötrofilik süpüratif granülomlarla doludur.", "isLie": True, "explanation": "Tuzak! Liken sklerozda süpürasyon ve granülom yoktur; homojen skleroz ve lenfositik bant bulunur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Liken sklerozun onkolojik riski ve histopatolojisi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Prekanseröz lezyon değildir; ancak zemininde skuamöz hücreli karsinom riski hafifçe artmıştır",
                            "isCorrect": True,
                            "explanation": "Liken skleroz prekanseröz kabul edilmez ancak hastalar artmış SCC riski nedeniyle takip edilir."
                        },
                        {
                            "key": "B",
                            "text": "Epidermiste aşırı kalınlaşma ve dev pleomorfik tümör hücreleri görülür",
                            "isCorrect": False,
                            "explanation": "Epidermis tam aksine incelmiştir (atrofiktir) ve sitolojik atipi içermez."
                        },
                        {
                            "key": "C",
                            "text": "Tanı anında olguların %100'ünde invaziv karsinoma dönüşüm tamamlanmıştır",
                            "isCorrect": False,
                            "explanation": "SCC gelişimi nadir (%1-5) bir komplikasyondur."
                        },
                        {
                            "key": "D",
                            "text": "Rete çıkıntıları aşırı uzayarak dermisin derinliklerine doğru prolifere olur",
                            "isCorrect": False,
                            "explanation": "Rete çıkıntıları uzamaz, aksine tamamen silinip düzleşir."
                        }
                    ]
                }
            ]
        },
        # S10
        {
            "slideNumber": 10,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 1] Vulva Anatomisi, Vulvit ve Liken Skleroz",
            "subtitle": "İlk 9 adımın temel kavramları, doku ayrımları ve ayırıcı tanı sentezi",
            "clinicalFocus": "Bölüm 1 Özeti ve Pekiştirme",
            "content": "Bu ilk kontrol noktasında kadın alt genital sisteminin dış anatomisini, vulvit etyolojisini, Bartholin bezi patolojilerini ve liken sklerozun kritik histopatolojik dinamiklerini sentezliyoruz:\n\n- **Anatomik Ayrım:** Kıllı deri katmanı labia majorada kıl folikülleri ve ter bezleri bulunurken; labia minora keratinize olmayan mukozal yapıdadır.\n- **Vulvit Spektrumu:** En sık semptom inatçı kaşıntıdır. Alerjik/kontakt (losyon, sabun, inkontinans idrarı) ve enfeksiyöz (HPV, HSV, gonore, sifiliz, Candida) nedenlerle tetiklenir. Candida cinsel yolla bulaşmayan önemli bir istisnadır.\n- **Bartholin Bezi:** Kanal tıkanması kiste, enfeksiyon eklenmesi şiddetli ağrılı ve fluktuan apseye yol açar.\n- **Liken Skleroz:** Parşömen kağıdı derisi, epidermis incelmesi, rete kaybı ve dermal homojen skleroz ile karakterizedir; prekanseröz değildir ancak SCC riskini biraz artırır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Lökoplaki klinik bir bulgudur; liken sklerozda epidermis incelirken, skuamöz hiperplazide kalınlaşır. Her beyaz plakta biyopsi zorunludur.",
            "synthesisNarrative": "Bu ilk kontrol noktasında kadın alt genital sisteminin dış anatomisini, vulvit etyolojisini, Bartholin bezi patolojilerini ve liken sklerozun kritik histopatolojik dinamiklerini sentezliyoruz:\n\n- **Anatomik Ayrım:** Kıllı deri katmanı labia majorada kıl folikülleri ve ter bezleri bulunurken; labia minora keratinize olmayan mukozal yapıdadır.\n- **Vulvit Spektrumu:** En sık semptom inatçı kaşıntıdır. Alerjik/kontakt (losyon, sabun, inkontinans idrarı) ve enfeksiyöz (HPV, HSV, gonore, sifiliz, Candida) nedenlerle tetiklenir. Candida cinsel yolla bulaşmayan önemli bir istisnadır.\n- **Bartholin Bezi:** Kanal tıkanması kiste, enfeksiyon eklenmesi şiddetli ağrılı ve fluktuan apseye yol açar.\n- **Liken Skleroz:** Parşömen kağıdı derisi, epidermis incelmesi, rete kaybı ve dermal homojen skleroz ile karakterizedir; prekanseröz değildir ancak SCC riskini biraz artırır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Lökoplaki klinik bir bulgudur; liken sklerozda epidermis incelirken, skuamöz hiperplazide kalınlaşır. Her beyaz plakta biyopsi zorunludur.",
            "bulletPoints": [
                "Labia majora kıllı deri, labia minora mukozadır.",
                "Vulvit çok etkenlidir; kaşıntı tabloyu derinleştirir.",
                "Candida cinsel yolla bulaşmaz; flora bozulmasıyla gelişir.",
                "Liken skleroz epidermis incelmesi ve homojen sklerozla gider."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Liken skleroz zemininde vulvar skuamöz hücreli karsinom gelişme riski hafif düzeyde artmıştır.",
                    "maskedTerm": "skuamöz hücreli karsinom",
                    "hint": "Vulvanın en sık görülen primer malign epitel tümörü"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bölüm 1 Temel Patolojiler Sentez Tablosu",
                    "tableHeaders": ["Hastalık / Tablo", "Temel Mekanizma", "Kritik Klinik / Histolojik İpucu"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Kontakt Vulvit", "isMasked": False},
                                {"text": "Kimyasal irritan ve alerjen teması", "isMasked": False},
                                {"text": "Yaşlıda idrar maruziyeti, sulantılı eritem", "isMasked": True, "hint": "inkontinans maserasyonu"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Candida Vulviti", "isMasked": False},
                                {"text": "Flora baskılanması ve fırsatçı üreme", "isMasked": True, "hint": "cinsel olmayan endojen mikoz"},
                                {"text": "Beyaz peynirimsi plaklar ve yoğun kaşıntı", "isMasked": False}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Liken Skleroz", "isMasked": False},
                                {"text": "Otoimmün sklerozan dermatoz", "isMasked": False},
                                {"text": "Epidermis incelmesi ve homojen dermal fibrozis", "isMasked": True, "hint": "parşömen kağıdı dokusu"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Bölüm 1 Patoloji Zinciri",
                    "steps": [
                        "1. Doku Çatısı: Labia majora derisi ve labia minora mukozası dış genital organı kurar.",
                        "2. İnflamatuvar Saldırı: İrritan temas veya patojenler kaşıntılı vulvit tablosunu başlatır.",
                        "3. Komplikasyon: Kanal tıkanırsa Bartholin kisti, enfeksiyonla apse tablosu doğar.",
                        "4. Sklerozan Dönüşüm: Kronik otoimmün süreçte liken skleroz gelişerek atrofi ve darlık bırakır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bölüm 1 kapsamında işlenen vulvit etkenlerinden hangisi kesinlikle cinsel yolla bulaşmaz?",
                    "answer": "Candida türleri cinsel yolla bulaşmaz; flora bozulması, diyabet veya antibiyotik kullanımı sonucu fırsatçı prolifere olur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Bölüm 1 Genel Tekrar ve Kilit Noktalar",
                    "items": [
                        {"text": "Vulvada labia majora kıllı deri, labia minora kıl folikülsüz mukoza yapısındadır.", "isLie": False, "explanation": "Doğru. Doku mimarisi bu şekildedir."},
                        {"text": "Bartholin kisti kanal obstrüksiyonuyla oluşur ve enfeksiyonla apseleşebilir.", "isLie": False, "explanation": "Doğru. Kanal tıkanması kist, süperenfeksiyon apse yapar."},
                        {"text": "Liken sklerozda epidermis incelir ve yüzeyel dermiste homojen fibrozis izlenir.", "isLie": False, "explanation": "Doğru. Patognomonik mikroskopi bulgularıdır."},
                        {"text": "Liken skleroz doğrudan karsinoma in situ olup hastaların tamamında hızla sarkoma dönüşür.", "isLie": True, "explanation": "Tuzak! Liken skleroz prekanseröz değildir ve sarkom yapmaz; karsinom riski yalnızca hafifçe (%1-5) artmıştır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "İlk 10 slaytta incelenen vulva patolojileri ile ilgili aşağıdaki sentez ifadelerinden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Lökoplaki klinik bir tanımlamadır; liken skleroz atrofik incelme yaparken her beyaz plakta biyopsi şarttır",
                            "isCorrect": True,
                            "explanation": "Lökoplakide maligniteyi dışlamak için mikroskobik inceleme ve biyopsi altın kuraldır."
                        },
                        {
                            "key": "B",
                            "text": "Candida vulviti yalnızca cinsel temasla bulaşan yüksek riskli bir viral enfeksiyondur",
                            "isCorrect": False,
                            "explanation": "Candida mikotik ajandır ve cinsel yolla bulaşmaz."
                        },
                        {
                            "key": "C",
                            "text": "Bartholin bezi klitorisin hemen üzerinde yer alan hormonal salgı bezidir",
                            "isCorrect": False,
                            "explanation": "Bartholin bezleri introitusun posterolateralinde yer alır."
                        },
                        {
                            "key": "D",
                            "text": "Liken sklerozda rete çıkıntıları kalınlaşarak epidermisi devasa boyutlara ulaştırır",
                            "isCorrect": False,
                            "explanation": "Liken sklerozda rete çıkıntıları silinir ve epidermis incelir."
                        }
                    ]
                }
            ]
        }
    ]

if __name__ == '__main__':
    slides = get_s1_slides()
    print(f'Section 1 created with {len(slides)} slides.')
