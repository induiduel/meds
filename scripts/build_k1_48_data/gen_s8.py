import json

def get_s8_slides():
    slides = [
        # S71
        {
            "slideNumber": 71,
            "title": "HPV Aşıları ve Primer Profilaksi: İki Değerli, Dört Değerli ve Dokuz Değerli Kapsam",
            "subtitle": "HPV 16/18 onkojenik suşları, HPV 6/11 siğil suşları ve çapraz koruma",
            "clinicalFocus": "Primer Korunma ve Aşı Tipleri",
            "content": "Ders notunda vurgulandığı üzere, Human Papilloma Virus enfeksiyonuna ve ilişkili tümörlere karşı en etkili ve kesin korunma yöntemi **profilaktik rekombinant HPV aşılarıdır**.\n\n- **İki Değerli Aşı (Bivalan - Cervarix):** En yüksek karsinojenik potansiyele sahip iki majör onkojenik suş olan **HPV tip 16 ve 18**'e karşı koruma sağlar; temel hedefi servikal, vulvar ve vajinal karsinom insidansını düşürmektir.\n- **Dört Değerli Aşı (Kuadrivalan - Gardasil):** Kanser yapıcı **HPV 16 ve 18**'in yanında, anogenital siğillerin (kondiloma akuminatum) %90'ından sorumlu olan düşük riskli **HPV tip 6 ve 11**'i de kapsar. Hem kanserleri hem de siğilleri önler.\n- **Dokuz Değerli Aşı (Nonavalan - Gardasil 9):** Tip 6, 11, 16, 18'e ek olarak beş diğer yüksek riskli onkojenik suşu daha (HPV 31, 33, 45, 52, 58) içerir. Serviks kanserlerinden koruyuculuk oranını %90'ın üzerine taşır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Dört değerli ve dokuz değerli HPV aşıları, kondiloma akuminatum etkenleri olan HPV 6 ve 11 ile malign karsinom etkenleri olan HPV 16 ve 18'e karşı kombine koruma sağlar.",
            "synthesisNarrative": "Ders notunda vurgulandığı üzere, Human Papilloma Virus enfeksiyonuna ve ilişkili tümörlere karşı en etkili ve kesin korunma yöntemi **profilaktik rekombinant HPV aşılarıdır**.\n\n- **İki Değerli Aşı (Bivalan - Cervarix):** En yüksek karsinojenik potansiyele sahip iki majör onkojenik suş olan **HPV tip 16 ve 18**'e karşı koruma sağlar; temel hedefi servikal, vulvar ve vajinal karsinom insidansını düşürmektir.\n- **Dört Değerli Aşı (Kuadrivalan - Gardasil):** Kanser yapıcı **HPV 16 ve 18**'in yanında, anogenital siğillerin (kondiloma akuminatum) %90'ından sorumlu olan düşük riskli **HPV tip 6 ve 11**'i de kapsar. Hem kanserleri hem de siğilleri önler.\n- **Dokuz Değerli Aşı (Nonavalan - Gardasil 9):** Tip 6, 11, 16, 18'e ek olarak beş diğer yüksek riskli onkojenik suşu daha (HPV 31, 33, 45, 52, 58) içerir. Serviks kanserlerinden koruyuculuk oranını %90'ın üzerine taşır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Dört değerli ve dokuz değerli HPV aşıları, kondiloma akuminatum etkenleri olan HPV 6 ve 11 ile malign karsinom etkenleri olan HPV 16 ve 18'e karşı kombine koruma sağlar.",
            "bulletPoints": [
                "Bivalan aşı HPV 16 ve 18'e karşı korur.",
                "Kuadrivalan aşı HPV 6, 11, 16 ve 18'i hedefler (kanser + siğil).",
                "Nonavalan aşı beş ek onkojenik tipi daha kapsayarak korumayı %90+ yapar."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Dört değerli HPV aşısı genital siğil etkenleri olan HPV 6 ve 11 ile kanser etkenleri HPV 16 ve 18 tiplerini içerir.",
                    "maskedTerm": "HPV 6 ve 11",
                    "hint": "Kondiloma akuminatumdan sorumlu düşük riskli virüs tipleri"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "HPV Aşı Tipleri ve Kapsadıkları Viral Suşlar",
                    "tableHeaders": ["Aşı Türü", "İçerdiği HPV Tipleri", "Korumayı Hedeflediği Lezyonlar"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Bivalan (İki Değerli)", "isMasked": False},
                                {"text": "HPV 16 ve 18", "isMasked": True, "hint": "iki ana karsinojenik tip"},
                                {"text": "Serviks, vajina ve vulva kanserleri"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Kuadrivalan (Dört Değerli)", "isMasked": False},
                                {"text": "HPV 6, 11, 16, 18", "isMasked": True, "hint": "siğil ve kanser etkenleri dörtyüzlüsü"},
                                {"text": "Hem genital siğiller hem de karsinomlar"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Profilaktik Aşılamadan Kanser Önlemeye",
                    "steps": [
                        "1. Erken Aşılama: Cinsel temas öncesi adölesan dönemde aşı intramüsküler uygulanır.",
                        "2. Nötralizan Antikorlar: Plazma hücreleri kanda yüksek titrede anti-HPV antikorları üretir.",
                        "3. Maruziyet Anı: Virüs serviks veya vulvaya ulaştığında antikorlar kapside bağlanarak hücre girişini engeller.",
                        "4. Kanser ve Siğil Önleme: Displazi, CIN ve kondilom gelişimi engellenerek tam koruma sağlanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Dört değerli (kuadrivalan) HPV aşısının hedef aldığı 4 viral tip ve bunların yol açtığı temel patolojiler nelerdir?",
                    "answer": "HPV 6 ve 11 (genital siğiller / kondiloma akuminatum) ile HPV 16 ve 18'dir (servikal, vajinal ve vulvar displazi ve karsinomlar)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "HPV Aşıları ve Profilaksi",
                    "items": [
                        {"text": "Bivalan aşı HPV 16 ve 18'e karşı profilaksi sağlar.", "isLie": False, "explanation": "Doğru. İki majör onkojenik tipe yöneliktir."},
                        {"text": "Kuadrivalan aşı hem kanser yapıcı (16, 18) hem siğil yapıcı (6, 11) tipleri içerir.", "isLie": False, "explanation": "Doğru. Dört tipi birden kapsar."},
                        {"text": "Dokuz değerli aşı ek 5 onkojenik suşu daha ekleyerek korumayı artırır.", "isLie": False, "explanation": "Doğru. Genişletilmiş koruma sağlar."},
                        {"text": "HPV aşısı canlı kuduz virüsü içeren tehlikeli bir biyolojik silahtır.", "isLie": True, "explanation": "Tuzak! HPV aşıları canlı virüs içermez, rekombinant virüs benzeri partiküllerden oluşur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Dört değerli (kuadrivalan) rekombinant HPV aşısının içeriğinde yer alan viral suşlar hangi seçenekte eksiksiz ve doğru verilmiştir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "HPV tip 6, 11, 16 ve 18",
                            "isCorrect": True,
                            "explanation": "Kuadrivalan aşı kondilom etkenleri 6 ve 11 ile karsinoma yol açan 16 ve 18'i içerir."
                        },
                        {
                            "key": "B",
                            "text": "HPV tip 1, 2, 3 ve 4",
                            "isCorrect": False,
                            "explanation": "Cilt siğili etkenleridir."
                        },
                        {
                            "key": "C",
                            "text": "Yalnızca Hepatit B ve Hepatit C virüsleri",
                            "isCorrect": False,
                            "explanation": "Karaciğer virüsleridir."
                        },
                        {
                            "key": "D",
                            "text": "Sadece kuduz ve tetanoz toksinleri",
                            "isCorrect": False,
                            "explanation": "HPV ile ilgisi yoktur."
                        }
                    ]
                }
            ]
        },
        # S72
        {
            "slideNumber": 72,
            "title": "HPV Aşılarının Hedef Antijenleri: L1 Majör Kapsid Proteini ve VLP",
            "subtitle": "Virüs benzeri partiküller (VLP), viral DNA içermeme ve güvenlik profili",
            "clinicalFocus": "Moleküler Biyoloji ve Aşı Güvenliği",
            "content": "HPV aşılarının inanılmaz başarısı ve yüksek güvenlik profili, kullanılan ileri biyoteknolojik antijen tasarımına dayanır.\n\n- **L1 Majör Kapsid Proteini:** HPV viryonunun dış kapsidini oluşturan temel yapısal proteindir. Rekombinant DNA teknolojisi ile maya (Saccharomyces cerevisiae) veya böcek hücrelerinde sentezletilir.\n- **Virüs Benzeri Partiküller (VLP - Virus-Like Particles):** Üretilen rekombinant L1 proteinleri kendiliğinden bir araya gelerek (self-assembly) tıpkı gerçek HPV virüsünün dış kabuğuna birebir benzeyen içi boş kapsid küreleri oluşturur.\n- **Kusursuz Güvenlik:** VLP partikülleri **kesinlikle viral DNA, onkogen (E6/E7) veya canlı virüs genomu İÇERMEZ**. Bu sayede aşı uygulanan kişide hiçbir şekilde enfeksiyon, replikasyon veya malign transformasyon oluşamaz; ancak bağışıklık sistemi virüsün yüzeyini görerek devasa nötralizan antikor yanıtı geliştirir.\n\n> [!NOTE]\n> Aşıda kullanılan L1 VLP yapıları enfeksiyöz viral DNA taşımadığından aşıya bağlı enfeksiyon gelişmesi biyolojik olarak tamamen imkansızdır.",
            "synthesisNarrative": "HPV aşılarının inanılmaz başarısı ve yüksek güvenlik profili, kullanılan ileri biyoteknolojik antijen tasarımına dayanır.\n\n- **L1 Majör Kapsid Proteini:** HPV viryonunun dış kapsidini oluşturan temel yapısal proteindir. Rekombinant DNA teknolojisi ile maya (Saccharomyces cerevisiae) veya böcek hücrelerinde sentezletilir.\n- **Virüs Benzeri Partiküller (VLP - Virus-Like Particles):** Üretilen rekombinant L1 proteinleri kendiliğinden bir araya gelerek (self-assembly) tıpkı gerçek HPV virüsünün dış kabuğuna birebir benzeyen içi boş kapsid küreleri oluşturur.\n- **Kusursuz Güvenlik:** VLP partikülleri **kesinlikle viral DNA, onkogen (E6/E7) veya canlı virüs genomu İÇERMEZ**. Bu sayede aşı uygulanan kişide hiçbir şekilde enfeksiyon, replikasyon veya malign transformasyon oluşamaz; ancak bağışıklık sistemi virüsün yüzeyini görerek devasa nötralizan antikor yanıtı geliştirir.\n\n> [!NOTE]\n> Aşıda kullanılan L1 VLP yapıları enfeksiyöz viral DNA taşımadığından aşıya bağlı enfeksiyon gelişmesi biyolojik olarak tamamen imkansızdır.",
            "bulletPoints": [
                "HPV aşılarının ana antijeni rekombinant L1 majör kapsid proteinidir.",
                "L1 proteinleri virüs benzeri partiküller (VLP) şeklinde kümelenir.",
                "Viral DNA içermediğinden aşı kesinlikle enfeksiyon yapamaz."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "HPV aşılarında içi boş kapsid küreleri oluşturan ana yapısal antijen L1 majör kapsid proteini molekülüdür.",
                    "maskedTerm": "L1 majör kapsid proteini",
                    "hint": "Rekombinant teknolojiyle üretilen dış kapsid proteini"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "HPV Aşısının Moleküler Bileşenleri",
                    "tableHeaders": ["Bileşen", "Aşıdaki Durumu", "Fonksiyonel Sonuç"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "L1 Kapsid Proteini (VLP)", "isMasked": False},
                                {"text": "Mevcut (Rekombinant Partikül)", "isMasked": True, "hint": "antijenik hedef protein"},
                                {"text": "Yüksek titrede koruyucu nötralizan antikor uyarımı"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Viral Genomik DNA (E6/E7)", "isMasked": False},
                                {"text": "Kesinlikle Bulunmaz (Yok)", "isMasked": True, "hint": "genetik materyal içermez"},
                                {"text": "Sıfır enfeksiyon ve mutasyon riski, tam güvenlik"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "VLP Teknolojisinden Bağışıklığa",
                    "steps": [
                        "1. Rekombinant Üretim: L1 geni mayaya aktarılarak saf L1 kapsid proteini sentezlenir.",
                        "2. Self-Assembly: L1 monomerleri birleşerek içi boş virüs benzeri partikül (VLP) oluşturur.",
                        "3. Aşı Enjeksiyonu: İçi boş VLP konağa verilir; antijen sunan hücreler partikülü tanır.",
                        "4. Steril Korumalı İmmünite: Viral DNA olmadan kusursuz immün hafıza ve antikor üretilir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "HPV aşılarında antijen olarak kullanılan virüs benzeri partiküller (VLP) hangi viral proteinden üretilir ve neden enfeksiyon yapamaz?",
                    "answer": "L1 majör kapsid proteininden üretilir; viral DNA veya genetik materyal içermediği (içi boş olduğu) için replike olamaz ve enfeksiyon yapamaz."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "L1 Proteini ve VLP Teknolojisi",
                    "items": [
                        {"text": "HPV aşısının temel antijeni rekombinant L1 kapsid proteinidir.", "isLie": False, "explanation": "Doğru. Majör yapısal proteindir."},
                        {"text": "VLP'ler virüs benzeri içi boş partiküllerdir.", "isLie": False, "explanation": "Doğru. Virüs taklidi yapar."},
                        {"text": "Aşı kesinlikle viral DNA veya onkogen içermez.", "isLie": False, "explanation": "Doğru. Genetik materyali yoktur."},
                        {"text": "Aşı enjekte edilir edilmez hastanın hücrelerine canlı HPV DNA'sı entegre olur.", "isLie": True, "explanation": "Tuzak! Aşıda DNA bulunmaz, entegrasyon veya enfeksiyon imkansızdır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "HPV aşılarının içeriği ve antijenik yapısı ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Viral DNA içermeyen rekombinant L1 majör kapsid proteininden oluşan virüs benzeri partiküllerdir (VLP)",
                            "isCorrect": True,
                            "explanation": "L1 proteininden üretilen VLP'ler DNA içermez ve güvenle bağışıklık sağlar."
                        },
                        {
                            "key": "B",
                            "text": "Canlı ve çoğalan yüksek riskli HPV 16 virüslerinin doğrudan damara verilmesidir",
                            "isCorrect": False,
                            "explanation": "Aşıda canlı virüs bulunmaz."
                        },
                        {
                            "key": "C",
                            "text": "Yalnızca saf şeker şurubundan oluşur ve hiçbir protein içermez",
                            "isCorrect": False,
                            "explanation": "Rekombinant L1 proteini temel antijendir."
                        },
                        {
                            "key": "D",
                            "text": "Aşı enjeksiyonu anında hastada karsinoma in situ başlatır",
                            "isCorrect": False,
                            "explanation": "Aşı kanseri önler, başlatmaz."
                        }
                    ]
                }
            ]
        },
        # S73
        {
            "slideNumber": 73,
            "title": "Aşı Sonrası Tarama Gerekliliği ve Kanser İnsidansı Değişimi",
            "subtitle": "Aşılanmış bireylerde Pap smear / HPV taramasının devam zorunluluğu",
            "clinicalFocus": "Klinik Kılavuzlar ve Tarama",
            "content": "HPV aşılarının uygulanması toplum genelinde servikal displazi ve karsinom insidansını muazzam ölçüde düşürmüş olsa da, **aşılanmış kadınlarda servikal tarama programlarının (Pap smear / HPV testi) sonlandırılması KESİNLİKLE kabul edilemez**.\n\n- **Aşı Kapsamı Dışındaki Suşlar:** Mevcut aşılar en sık görülen onkojenik suşları (özellikle 16 ve 18) kapsasa da, servikal kanserlerin yaklaşık %10-30'u aşı içeriğinde bulunmayan diğer yüksek riskli HPV tiplerinden (örneğin tip 35, 39, 51, 56 vb.) kaynaklanabilir.\n- **Önceden Edinilmiş Enfeksiyonlar:** Aşı terapötik (tedavi edici) değildir; yalnızca profilaktiktir. Aşı yapılmadan önce edinilmiş mevcut bir HPV enfeksiyonunu veya var olan displaziyi geriletmez.\n- **Kılavuz Önerisi:** Aşı durumu ne olursa olsun, tüm kadınlar ulusal kılavuzların önerdiği yaş ve aralıklarla rutin Pap smear ve HPV tarama programlarına eksiksiz biçimde devam etmelidir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] HPV aşısı yapılmış kadınlarda da aşı kapsamı dışındaki diğer onkojenik suşlar ve önceden mevcut enfeksiyonlar nedeniyle rutin servikal taramaya (Pap smear/HPV testi) aynı şekilde devam edilmelidir.",
            "synthesisNarrative": "HPV aşılarının uygulanması toplum genelinde servikal displazi ve karsinom insidansını muazzam ölçüde düşürmüş olsa da, **aşılanmış kadınlarda servikal tarama programlarının (Pap smear / HPV testi) sonlandırılması KESİNLİKLE kabul edilemez**.\n\n- **Aşı Kapsamı Dışındaki Suşlar:** Mevcut aşılar en sık görülen onkojenik suşları (özellikle 16 ve 18) kapsasa da, servikal kanserlerin yaklaşık %10-30'u aşı içeriğinde bulunmayan diğer yüksek riskli HPV tiplerinden (örneğin tip 35, 39, 51, 56 vb.) kaynaklanabilir.\n- **Önceden Edinilmiş Enfeksiyonlar:** Aşı terapötik (tedavi edici) değildir; yalnızca profilaktiktir. Aşı yapılmadan önce edinilmiş mevcut bir HPV enfeksiyonunu veya var olan displaziyi geriletmez.\n- **Kılavuz Önerisi:** Aşı durumu ne olursa olsun, tüm kadınlar ulusal kılavuzların önerdiği yaş ve aralıklarla rutin Pap smear ve HPV tarama programlarına eksiksiz biçimde devam etmelidir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] HPV aşısı yapılmış kadınlarda da aşı kapsamı dışındaki diğer onkojenik suşlar ve önceden mevcut enfeksiyonlar nedeniyle rutin servikal taramaya (Pap smear/HPV testi) aynı şekilde devam edilmelidir.",
            "bulletPoints": [
                "HPV aşısı olan kadınlarda da rutin servikal tarama devam etmelidir.",
                "Aşılar tüm HPV tiplerini kapsamaz; aşı dışı onkojenik suşlar kanser yapabilir.",
                "Aşı profilaktiktir; önceden başlamış lezyonları tedavi etmez."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "HPV aşısı yapılmış bireylerde de aşı kapsamı dışındaki onkojenik tipler nedeniyle rutin servikal tarama programına devam edilir.",
                    "maskedTerm": "servikal tarama",
                    "hint": "Pap smear ve HPV DNA testleriyle yürütülen periyodik izlem"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "HPV Aşılama ve Tarama İlişkisi",
                    "tableHeaders": ["Parametre", "Aşının Sağladığı", "Aşının Sağlayamadığı / Devam Eden"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Hedef HPV Tipleri", "isMasked": False},
                                {"text": "Tip 16, 18 (ve aşısına göre diğerleri)", "isMasked": False},
                                {"text": "Nadir diğer yüksek riskli tipler (35, 39 vb.)", "isMasked": True, "hint": "aşı formülasyonu dışındaki suşlar"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Klinik Takip Gereksinimi", "isMasked": False},
                                {"text": "Karsinom riskinde dramatik azalma", "isMasked": False},
                                {"text": "Pap smear ve HPV taramasının aynen devamı", "isMasked": True, "hint": "bırakılmaması gereken koruyucu protokol"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Aşı Sonrası Tarama Mantığı",
                    "steps": [
                        "1. Aşılanma: Kişi kuadrivalan veya dokuz değerli aşı ile aşılanır.",
                        "2. Yüksek Koruma: Tip 16 ve 18 kaynaklı invaziv kanser riski ortadan kalkar.",
                        "3. Aşı Dışı Risk: Nadir bir onkojenik suş (örn. HPV-35) transformasyon zonunu enfekte edebilir.",
                        "4. Taramada Yakalama: Düzenli Pap smear bu nadir lezyonu erken yakalayarak invazyonu önler."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "HPV aşısı yaptıran bir kadında neden servikal Pap smear taraması sonlandırılmaz ve aynı şekilde devam ettirilir?",
                    "answer": "Aşı tüm onkojenik tipleri kapsamadığı (aşı dışı suşlar kanser yapabildiği) ve aşı öncesi edinilmiş mevcut enfeksiyonları tedavi etmediği için."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Aşı Sonrası Tarama İlkeleri",
                    "items": [
                        {"text": "HPV aşısı olan kadınlarda da rutin Pap smear taraması devam etmelidir.", "isLie": False, "explanation": "Doğru. Kılavuzların temel kuralıdır."},
                        {"text": "Aşı kapsamı dışındaki diğer onkojenik tipler displaziye yol açabilir.", "isLie": False, "explanation": "Doğru. Aşı tüm tipleri içermez."},
                        {"text": "Mevcut aşılar terapötik değil profilaktiktir.", "isLie": False, "explanation": "Doğru. Var olan lezyonu tedavi etmez."},
                        {"text": "HPV aşısı olan bir kişi ömrü boyunca hiçbir doktora gitmemeli ve hastaneden men edilmelidir.", "isLie": True, "explanation": "Tuzak! Aşılanmış bireyler normal tarama ve sağlık kontrollerine aynen devam eder."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Dokuz değerli HPV aşısı ile aşılanmış 25 yaşındaki asemptomatik bir kadın rutin jinekolojik kontrole başvuruyor. Bu hastanın servikal kanser taraması ile ilgili en doğru klinik yaklaşım nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Aşı yapılmış olsa dahi kılavuzlara uygun olarak rutin servikal taramaya (Pap smear/HPV) aynen devam edilmelidir",
                            "isCorrect": True,
                            "explanation": "Aşı tüm tipleri kapsamadığından rutin tarama protokolleri aşılanmış kadınlarda da aynen sürdürülür."
                        },
                        {
                            "key": "B",
                            "text": "Aşılandığı için ömür boyu hiçbir smear veya tarama yapılmasına gerek yoktur",
                            "isCorrect": False,
                            "explanation": "Hatalı ve tehlikeli bir yaklaşımdır."
                        },
                        {
                            "key": "C",
                            "text": "Hemen koruyucu amaçla total histerektomi ameliyatına alınmalıdır",
                            "isCorrect": False,
                            "explanation": "Endikasyonsuz ağır cerrahidir."
                        },
                        {
                            "key": "D",
                            "text": "Sadece her gün 10 litre maden suyu içmesi önerilmelidir",
                            "isCorrect": False,
                            "explanation": "Tıbbi tarama yöntemi değildir."
                        }
                    ]
                }
            ]
        },
        # S74
        {
            "slideNumber": 74,
            "title": "Liken Skleroz ve Skuamöz Hiperplazide Uzun Dönem Takip ve Biyopsi",
            "subtitle": "Kanser riski artışı, dVIN gelişimi ve periyodik vulvar muayene",
            "clinicalFocus": "Uzun Dönem Takip Protokolleri",
            "content": "Ders notunda belirtildiği üzere, vulvanın non-neoplastik epitel bozuklukları olan **liken skleroz ve skuamöz hücre hiperplazisi**, doğrudan premalign lezyonlar olmasalar da skuamöz hücreli karsinom riskini hafifçe artırırlar.\n\n- **Kanserleşme Riski:** Liken sklerozlu kadınların yaklaşık %1-5'inde uzun dönemde vulvar skuamöz karsinom gelişir. Bu tümörler HPV-negatif yoldan gelişen, yaşlı kadınlarda görülen keratinize karsinomlardır.\n- **Öncü Lezyon (dVIN):** Liken skleroz veya hiperplazi zemininde kronik irritasyon ve p53 mutasyonları sonucu **Diferansiye VIN (dVIN)** tablosu ortaya çıkar. dVIN çok hızla invaziv karsinoma ilerleyebilir.\n- **Klinik İzlem İlkeleri:** Hastalar ömür boyu 6-12 ayda bir dikkatli vulvar muayeneden geçirilmelidir. İnatçı kaşıntı, doku sertleşmesi, ülserleşme, yeni kabarıklık veya pigmente alan belirdiği anda **derhal punch biyopsi** alınmalıdır.\n\n> [!NOTE]\n> Liken skleroz hastalarında karsinom gelişimi dVIN üzerinden yürür; bu nedenle lezyon sahasındaki her yeni erozyon veya kalınlaşma biyopsi ile kontrol edilmelidir.",
            "synthesisNarrative": "Ders notunda belirtildiği üzere, vulvanın non-neoplastik epitel bozuklukları olan **liken skleroz ve skuamöz hücre hiperplazisi**, doğrudan premalign lezyonlar olmasalar da skuamöz hücreli karsinom riskini hafifçe artırırlar.\n\n- **Kanserleşme Riski:** Liken sklerozlu kadınların yaklaşık %1-5'inde uzun dönemde vulvar skuamöz karsinom gelişir. Bu tümörler HPV-negatif yoldan gelişen, yaşlı kadınlarda görülen keratinize karsinomlardır.\n- **Öncü Lezyon (dVIN):** Liken skleroz veya hiperplazi zemininde kronik irritasyon ve p53 mutasyonları sonucu **Diferansiye VIN (dVIN)** tablosu ortaya çıkar. dVIN çok hızla invaziv karsinoma ilerleyebilir.\n- **Klinik İzlem İlkeleri:** Hastalar ömür boyu 6-12 ayda bir dikkatli vulvar muayeneden geçirilmelidir. İnatçı kaşıntı, doku sertleşmesi, ülserleşme, yeni kabarıklık veya pigmente alan belirdiği anda **derhal punch biyopsi** alınmalıdır.\n\n> [!NOTE]\n> Liken skleroz hastalarında karsinom gelişimi dVIN üzerinden yürür; bu nedenle lezyon sahasındaki her yeni erozyon veya kalınlaşma biyopsi ile kontrol edilmelidir.",
            "bulletPoints": [
                "Liken sklerozda karsinom riski %1-5 civarında hafif artmıştır.",
                "Malignite dVIN öncü lezyonu üzerinden keratinize SCC'ye ilerler.",
                "Şüpheli sertleşme veya ülserlerde gecikmeksizin punch biyopsi yapılır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Liken skleroz zemininde HPV-negatif karsinoma ilerleyen öncü prekanseröz lezyona diferansiye VIN adı verilir.",
                    "maskedTerm": "diferansiye VIN",
                    "hint": "dVIN kısaltmasıyla bilinen ve p53 mutasyonu içeren öncü lezyon"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Non-Neoplastik Dermatozlarda Uzun Dönem Riskler",
                    "tableHeaders": ["Hastalık", "Histolojik Risk Mekanizması", "Önerilen Klinik Protokol"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Liken Skleroz", "isMasked": False},
                                {"text": "Kronik inflamasyon, skleroz ve dVIN gelişimi", "isMasked": True, "hint": "p53 ilişkili malign transformasyon"},
                                {"text": "Yıllık muayene, şüpheli alandan erken biyopsi"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Skuamöz Hiperplazi", "isMasked": False},
                                {"text": "Kronik kaşıma travması ve artmış mitoz", "isMasked": True, "hint": "ovmaya bağlı epidermal döngü artışı"},
                                {"text": "Kaşıntının kontrolü ve lökoplakide biyopsi"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Liken Sklerozdan Keratinize Karsinoma İzlem",
                    "steps": [
                        "1. Kronik Skleroz: Vulvada dermal fibrozis ve epidermis incelmesi yıllarca sürer.",
                        "2. Sürücü Mutasyon: Bazal hücrelerde p53 mutasyonu birikerek dVIN ortaya çıkar.",
                        "3. Klinik Değişiklik: Porselen beyazı plak üzerinde sert bir nodül veya inatçı ülser belirir.",
                        "4. Erken Biyopsi: Punch biyopside keratinize karsinom yakalanarak erken cerrahiye gidilir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Liken skleroz tanılı bir hastanın takibinde vulvada yeni gelişen bir sertlik veya ülser saptandığında izlenmesi gereken ilk ve zorunlu tanısal adım nedir?",
                    "answer": "Gecikmeksizin punch biyopsi alınarak dVIN veya invaziv skuamöz hücreli karsinomun araştırılmasıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Liken Sklerozda Takip Prensipleri",
                    "items": [
                        {"text": "Liken skleroz hastalarında vulvar skuamöz karsinom riski hafifçe artmıştır.", "isLie": False, "explanation": "Doğru. %1-5 oranında risk artışı vardır."},
                        {"text": "Karsinom öncüsü lezyon diferansiye VIN (dVIN)'dir.", "isLie": False, "explanation": "Doğru. HPV negatif yoldur."},
                        {"text": "Şüpheli alanlardan punch biyopsi ile doku tanısı alınmalıdır.", "isLie": False, "explanation": "Doğru. Kesin tanı biyopsiyle konur."},
                        {"text": "Liken sklerozlu hastalar asla muayene edilmemeli, kendi haline bırakılmalıdır.", "isLie": True, "explanation": "Tuzak! Malign transformasyon riski nedeniyle düzenli klinik izlem şarttır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Uzun süredir liken skleroz tanısıyla takip edilen 72 yaşındaki bir kadında labium majus üzerinde yeni gelişen sert bir ülseratif lezyon saptanıyor. En uygun yaklaşım nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Lezyondan punch biyopsi alarak diferansiye VIN ve invaziv karsinomu araştırmak",
                            "isCorrect": True,
                            "explanation": "Liken skleroz zemininde yeni ülser/nodül derhal biyopsi ile malignite açısından taranmalıdır."
                        },
                        {
                            "key": "B",
                            "text": "Hiçbir işlem yapmayıp hastaya sıcak su banyosu önermek",
                            "isCorrect": False,
                            "explanation": "Malignite riskini göz ardı eden hatalı yaklaşımdır."
                        },
                        {
                            "key": "C",
                            "text": "Yalnızca göz damlası reçete edip göndermek",
                            "isCorrect": False,
                            "explanation": "Alakasız bir yaklaşımdır."
                        },
                        {
                            "key": "D",
                            "text": "Hemen tüm iç organları kemoterapi ile yok etmek",
                            "isCorrect": False,
                            "explanation": "Biyopsi olmadan kemoterapi verilmez."
                        }
                    ]
                }
            ]
        },
        # S75
        {
            "slideNumber": 75,
            "title": "Vulva Lökoplakisinde Adım Adım Biyopsi Yönetimi",
            "subtitle": "Toluidin mavisi testi, punch biyopsi tekniği ve histopatolojik triyaj",
            "clinicalFocus": "Tanısal Algoritma",
            "content": "Ders notunda açıkça vurgulandığı üzere, **vulva lökoplakisi** yalnızca klinik bir tanımlama olup kazımakla çıkmayan beyaz plakları ifade eder; kesin patolojik tanı ancak **biyopsi** ile konabilir.\n\n- **Toluidin Mavisi (Collins Testi):** Nükleus yoğunluğu yüksek olan atipik veya invaziv alanları belirlemek için vulvaya sürülen bazik bir boyadır; asetik asitle yıkandığında nükleer zengin alanlar boyayı tutarak koyu mavi kalır ve biyopsi odağını gösterir.\n- **Punch Biyopsi Tekniği:** Şüpheli lökoplakik alanın en kalın, indüre veya ülserli sınırından lokal anestezi altında 3-4 mm'lik punch biyopsi aleti ile dermisi de içeren tam kat doku örneği alınır.\n- **Histopatolojik Triyaj:** Patolog kesitte akantoz/hiperkeratoz (skuamöz hiperplazi), dermal hyalinizasyon (liken skleroz), atipik nükleer tabakalaşma (VIN) veya stromal invazyon (karsinom) ayrımını yaparak tedaviyi yönlendirir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Her vulvar lökoplaki lezyonuna mutlaka biyopsi yapılmalıdır; çünkü lökoplakinin altında benign dermatozlar (liken skleroz, psöriyazis) yatabileceği gibi in situ veya invaziv karsinom da bulunabilir.",
            "synthesisNarrative": "Ders notunda açıkça vurgulandığı üzere, **vulva lökoplakisi** yalnızca klinik bir tanımlama olup kazımakla çıkmayan beyaz plakları ifade eder; kesin patolojik tanı ancak **biyopsi** ile konabilir.\n\n- **Toluidin Mavisi (Collins Testi):** Nükleus yoğunluğu yüksek olan atipik veya invaziv alanları belirlemek için vulvaya sürülen bazik bir boyadır; asetik asitle yıkandığında nükleer zengin alanlar boyayı tutarak koyu mavi kalır ve biyopsi odağını gösterir.\n- **Punch Biyopsi Tekniği:** Şüpheli lökoplakik alanın en kalın, indüre veya ülserli sınırından lokal anestezi altında 3-4 mm'lik punch biyopsi aleti ile dermisi de içeren tam kat doku örneği alınır.\n- **Histopatolojik Triyaj:** Patolog kesitte akantoz/hiperkeratoz (skuamöz hiperplazi), dermal hyalinizasyon (liken skleroz), atipik nükleer tabakalaşma (VIN) veya stromal invazyon (karsinom) ayrımını yaparak tedaviyi yönlendirir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Her vulvar lökoplaki lezyonuna mutlaka biyopsi yapılmalıdır; çünkü lökoplakinin altında benign dermatozlar (liken skleroz, psöriyazis) yatabileceği gibi in situ veya invaziv karsinom da bulunabilir.",
            "bulletPoints": [
                "Lökoplaki klinik bir tanıdır; kesin tanı için biyopsi şarttır.",
                "Toluidin mavisi ve punch biyopsi doğru örnekleme sağlar.",
                "Histopatoloji selim dermatoz ile karsinomu ayırt eder."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vulva lökoplakisinde kesin histopatolojik tanıyı koymak için lezyondan tam kat punch biyopsi alınması zorunludur.",
                    "maskedTerm": "punch biyopsi",
                    "hint": "Dermisi ve epidermisi içeren silindirik doku alma yöntemi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vulva Lökoplakisinin Histopatolojik Spektrumu",
                    "tableHeaders": ["Olası Histolojik Tanı", "Temel Mikroskobik Özellik", "Kanserleşme Riski"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Liken Skleroz", "isMasked": False},
                                {"text": "Epidermis incelmesi, homojen dermal skleroz", "isMasked": True, "hint": "atrofik ve sklerotik bant"},
                                {"text": "Hafif artmış (%1 - 5 risk)"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Skuamöz Karsinoma in Situ", "isMasked": False},
                                {"text": "Tam kat atipik hücreler, mitotik figürler", "isMasked": True, "hint": "bazal membranı aşmamış premalign lezyon"},
                                {"text": "Yüksek (tedavi edilmezse invazyon)"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Lökoplakide Klinik Yaklaşım Algoritması",
                    "steps": [
                        "1. Klinik İnceleme: Vulvada kazınamayan beyaz kalınlaşmış plak (lökoplaki) saptanır.",
                        "2. Alan Seçimi: Toluidin mavisi veya kolposkopik büyütmeyle en şüpheli odak belirlenir.",
                        "3. Punch Biyopsi: Dermisi de içeren tam kat doku örneği patolojiye sevk edilir.",
                        "4. Tedavi Planı: Histolojiye göre kortikosteroid veya cerrahi eksizyon kararlaştırılır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Vulva lökoplakisi görülen her hastada neden mutlaka biyopsi yapılmalıdır?",
                    "answer": "Lökoplaki spesifik bir hastalık değil yalnızca klinik bir tanımlamadır; altında selim bir dermatoz (liken skleroz vb.) yatabileceği gibi invaziv karsinom da bulunabileceğinden ayrım ancak biyopsi ile yapılabilir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vulva Lökoplakisi Yönetimi",
                    "items": [
                        {"text": "Lökoplaki kazımakla çıkmayan beyaz plakları tanımlayan klinik bir terimdir.", "isLie": False, "explanation": "Doğru. Histopatolojik değil klinik tanıdır."},
                        {"text": "Her lökoplaki lezyonunda kesin tanı için biyopsi zorunludur.", "isLie": False, "explanation": "Doğru. Amfi notunun temel vurgusudur."},
                        {"text": "Psoriasis, liken skleroz veya karsinom lökoplaki yapabilir.", "isLie": False, "explanation": "Doğru. Geniş ayırıcı tanısı vardır."},
                        {"text": "Lökoplaki lezyonları jiletle kazınarak evde hasta tarafından temizlenmelidir.", "isLie": True, "explanation": "Tuzak! Lökoplaki kazınamaz; doku travmatize edilmemeli ve cerrahi biyopsi alınmalıdır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvada kazımakla çıkmayan beyaz porselenimsi plaklar (lökoplaki) saptanan bir hastada doğru klinik patolojik yaklaşım nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Lökoplaki klinik bir tanı olduğundan kesin tanı için şüpheli odaktan punch biyopsi almak",
                            "isCorrect": True,
                            "explanation": "Lökoplaki altında karsinom veya liken skleroz yatabileceğinden mutlaka biyopsi yapılmalıdır."
                        },
                        {
                            "key": "B",
                            "text": "Hastaya lezyonu sert fırçayla kazımasını tavsiye etmek",
                            "isCorrect": False,
                            "explanation": "Dokuyu tahrip eder ve kanamaya yol açar."
                        },
                        {
                            "key": "C",
                            "text": "Beyaz lekeyi diş macunu ile silerek hastayı taburcu etmek",
                            "isCorrect": False,
                            "explanation": "Tıbbi değeri olmayan zararlı bir uygulamadır."
                        },
                        {
                            "key": "D",
                            "text": "Hiçbir tetkik yapmadan hastayı 30 yıl sonraya kontrole çağırmak",
                            "isCorrect": False,
                            "explanation": "Kanser atlanmasına yol açar."
                        }
                    ]
                }
            ]
        },
        # S76
        {
            "slideNumber": 76,
            "title": "Diferansiye VIN (dVIN) Yönetimi: Cerrahi Eksizyon Sınırları",
            "subtitle": "p53 pozitifliği, bazal atipi ve hızlı invazyon riski",
            "clinicalFocus": "Preinvaziv Cerrahi Yönetim",
            "content": "Ders notunda vurgulanan **diferansiye VIN (dVIN)**, klasik HPV ilişkili VIN'e göre çok daha sinsi, teşhisi zor ve agresif bir prekanseröz lezyondur.\n\n- **Histopatolojik Zorluk:** Atipik hücreler epitelin tamamına yayılmaz; yalnızca **bazal ve parabazal tabakalara sınırlıdır**. Yüzeyel hücreler ise aşırı keratinize ve matür görünümdedir. Bu nedenle patolog tarafından kolaylıkla 'benign hiperkeratoz' sanılarak atlanabilir.\n- **İmmünohistokimyasal Belirteç:** Vakaların neredeyse tamamında **p53 gen mutasyonu** bulunur. İmmünohistokimyada bazal hücrelerde ya aşırı kuvvetli p53 birikimi ya da genin tamamen sustuğu 'null fenotip' izlenir.\n- **Cerrahi Tedavi:** dVIN saptandığında hızla keratinize skuamöz karsinoma ilerleme riski taşıdığından lokal ablasyon (lazer vb.) yetersizdir; lezyon **geniş lokal eksizyon** ile negatif cerrahi sınırlarla tamamen çıkarılmalıdır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] dVIN bazal tabakaya sınırlı atipi ve p53 mutasyonu ile seyreder; invaziv karsinoma progresyon hızı klasik VIN'den çok daha yüksektir ve cerrahi eksizyon şarttır.",
            "synthesisNarrative": "Ders notunda vurgulanan **diferansiye VIN (dVIN)**, klasik HPV ilişkili VIN'e göre çok daha sinsi, teşhisi zor ve agresif bir prekanseröz lezyondur.\n\n- **Histopatolojik Zorluk:** Atipik hücreler epitelin tamamına yayılmaz; yalnızca **bazal ve parabazal tabakalara sınırlıdır**. Yüzeyel hücreler ise aşırı keratinize ve matür görünümdedir. Bu nedenle patolog tarafından kolaylıkla 'benign hiperkeratoz' sanılarak atlanabilir.\n- **İmmünohistokimyasal Belirteç:** Vakaların neredeyse tamamında **p53 gen mutasyonu** bulunur. İmmünohistokimyada bazal hücrelerde ya aşırı kuvvetli p53 birikimi ya da genin tamamen sustuğu 'null fenotip' izlenir.\n- **Cerrahi Tedavi:** dVIN saptandığında hızla keratinize skuamöz karsinoma ilerleme riski taşıdığından lokal ablasyon (lazer vb.) yetersizdir; lezyon **geniş lokal eksizyon** ile negatif cerrahi sınırlarla tamamen çıkarılmalıdır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] dVIN bazal tabakaya sınırlı atipi ve p53 mutasyonu ile seyreder; invaziv karsinoma progresyon hızı klasik VIN'den çok daha yüksektir ve cerrahi eksizyon şarttır.",
            "bulletPoints": [
                "dVIN bazal tabakada atipi ve p53 mutasyonu ile karakterizedir.",
                "Yüzey matür göründüğünden histopatolojik olarak kolayca atlanabilir.",
                "Hızla keratinize SCC'ye ilerlediğinden geniş cerrahi eksizyon gerekir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "HPV-negatif vulvar karsinomun öncüsü olan diferansiye VIN lezyonlarında p53 mutasyonu karakteristiktir.",
                    "maskedTerm": "p53 mutasyonu",
                    "hint": "Tümör baskılayıcı gende görülen onkojenik değişiklik"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "dVIN vs Klasik (Olağan) VIN",
                    "tableHeaders": ["Özellik", "Diferansiye VIN (dVIN)", "Klasik VIN (uVIN)"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Viral İlişki", "isMasked": False},
                                {"text": "HPV Negatif (-)", "isMasked": False},
                                {"text": "Yüksek riskli HPV Pozitif (+)", "isMasked": True, "hint": "viral etyoloji varlığı"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Histolojik Atipi Düzeyi", "isMasked": False},
                                {"text": "Bazal tabakaya sınırlı anormal atipi", "isMasked": True, "hint": "sadece alt katman tutulumu"},
                                {"text": "Tüm epitel katmanlarını kaplayan bazaloid atipi"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "dVIN Teşhis ve Eksizyon Süreci",
                    "steps": [
                        "1. Liken Zemininde Atipi: Liken sklerozlu alanda bazal hücrelerde p53 mutasyonu birikir.",
                        "2. Histopatolojik Şüphe: Patolog yüzeyel olgunlaşmaya rağmen bazaldeki atipik mitozları fark eder.",
                        "3. p53 İmmün Boyama: Bazal tabakada diffüz nükleer p53 pozitifliği ile dVIN doğrulanır.",
                        "4. Geniş Eksizyon: Doku sağlam cerrahi sınırlarla çıkarılarak invaziv karsinom engellenir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Diferansiye VIN (dVIN) lezyonunun histopatolojide atlanmasını kolaylaştıran morfolojik tuzak nedir?",
                    "answer": "Atipinin sadece bazal tabakada sınırlı olması, epitelin orta ve üst katmanlarının ise yanıltıcı biçimde son derece matür ve hiperkeratotik görünmesidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Diferansiye VIN (dVIN)",
                    "items": [
                        {"text": "dVIN HPV-negatif keratinize vulvar karsinomun öncüsüdür.", "isLie": False, "explanation": "Doğru. Liken skleroz zemininde gelişir."},
                        {"text": "Atipik hücreler bazal tabakaya sınırlıdır ve p53 mutasyonu taşır.", "isLie": False, "explanation": "Doğru. Tipik patolojik profilidir."},
                        {"text": "Tedavisinde negatif cerrahi sınırlarla geniş lokal eksizyon gerekir.", "isLie": False, "explanation": "Doğru. Hızlı progresyon gösterir."},
                        {"text": "dVIN sadece çocuklarda görülen ve yoğurt yemekle geçen bir alerjidir.", "isLie": True, "explanation": "Tuzak! dVIN yaşlı kadınlarda görülen ciddi bir premalign neoplazidir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Diferansiye VIN (dVIN) tanısı alan bir hasta ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "HPV-negatif yolun öncüsüdür, p53 mutasyonu içerir ve hızla keratinize skuamöz karsinoma ilerleyebilir",
                            "isCorrect": True,
                            "explanation": "dVIN p53 mutasyonlu, HPV negatif ve agresif seyirli premalign vulva lezyonudur."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca düşük riskli HPV tip 6 ile oluşan selim bir siğildir",
                            "isCorrect": False,
                            "explanation": "Kondilom ile dVIN farklıdır; dVIN HPV negatif ve premaligndir."
                        },
                        {
                            "key": "C",
                            "text": "Hiçbir zaman cerrahi müdahale gerektirmeyen selim bir su toplamasıdır",
                            "isCorrect": False,
                            "explanation": "Cerrahi eksizyon zorunludur."
                        },
                        {
                            "key": "D",
                            "text": "Sadece erkeklerin karaciğer dokusunda gelişir",
                            "isCorrect": False,
                            "explanation": "Kadın vulva neoplazisidir."
                        }
                    ]
                }
            ]
        },
        # S77
        {
            "slideNumber": 77,
            "title": "Klasik VIN (uVIN) Yönetiminde LEEP ve Lazer Ablasyon",
            "subtitle": "Multisentrik lezyonlar, genç hastalar, cerrahi sınırlar ve nüks riski",
            "clinicalFocus": "HPV İlişkili VIN Tedavisi",
            "content": "Yüksek riskli HPV (özellikle tip 16) ile ilişkili olarak genç ve sigara içen kadınlarda görülen **Klasik (Olağan) VIN (uVIN)**, dVIN'den oldukça farklı bir klinik seyir ve tedavi yaklaşımı gerektirir.\n\n- **Multisentrik Tutulum:** Klasik VIN lezyonları sıklıkla vulvanın birden fazla bölgesinde, perine ve perianal deride çok odaklı (multifokal) olarak yerleşir; servikal CIN ve vajinal VAIN ile eşzamanlı birliktelik gösterebilir.\n- **Tedavi Modaliteleri:** Genç hastalarda vulvanın anatomik yapısını ve fonksiyonunu korumak kritik olduğundan, invazyon şüphesi olmayan olgularda **karbondioksit (CO2) lazer ablasyonu** veya **LEEP eksizyonu** tercih edilir. Yaygın veya şüpheli lezyonlarda cerrahi eksizyon uygulanır.\n- **Nüks Potansiyeli:** HPV enfeksiyonu çevre normal görünen epitelde de latent olarak bulunabildiğinden ('alan kanserleşmesi'), lezyonlar cerrahi olarak tamamen çıkarılsa dahi **yüksek oranda lokal nüks** gösterebilir.\n\n> [!NOTE]\n> Klasik VIN çok odaklı olduğundan eksizyon sonrası uzun süreli ve periyodik kolposkopik/vulvoskopik takip zorunludur.",
            "synthesisNarrative": "Yüksek riskli HPV (özellikle tip 16) ile ilişkili olarak genç ve sigara içen kadınlarda görülen **Klasik (Olağan) VIN (uVIN)**, dVIN'den oldukça farklı bir klinik seyir ve tedavi yaklaşımı gerektirir.\n\n- **Multisentrik Tutulum:** Klasik VIN lezyonları sıklıkla vulvanın birden fazla bölgesinde, perine ve perianal deride çok odaklı (multifokal) olarak yerleşir; servikal CIN ve vajinal VAIN ile eşzamanlı birliktelik gösterebilir.\n- **Tedavi Modaliteleri:** Genç hastalarda vulvanın anatomik yapısını ve fonksiyonunu korumak kritik olduğundan, invazyon şüphesi olmayan olgularda **karbondioksit (CO2) lazer ablasyonu** veya **LEEP eksizyonu** tercih edilir. Yaygın veya şüpheli lezyonlarda cerrahi eksizyon uygulanır.\n- **Nüks Potansiyeli:** HPV enfeksiyonu çevre normal görünen epitelde de latent olarak bulunabildiğinden ('alan kanserleşmesi'), lezyonlar cerrahi olarak tamamen çıkarılsa dahi **yüksek oranda lokal nüks** gösterebilir.\n\n> [!NOTE]\n> Klasik VIN çok odaklı olduğundan eksizyon sonrası uzun süreli ve periyodik kolposkopik/vulvoskopik takip zorunludur.",
            "bulletPoints": [
                "Klasik VIN genç kadınlarda çok odaklı (multifokal) yerleşir.",
                "LEEP, lazer ablasyon ve cerrahi eksizyon tedavi seçenekleridir.",
                "Persistan HPV enfeksiyonu nedeniyle nüks riski yüksektir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Genç kadınlarda HPV ile ilişkili klasik VIN lezyonları vulvada sıklıkla multifokal olarak yerleşim gösterir.",
                    "maskedTerm": "multifokal",
                    "hint": "Birden çok odakta eşzamanlı ortaya çıkan dağılım"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Klasik VIN Tedavi Yaklaşımları",
                    "tableHeaders": ["Tedavi Yöntemi", "Uygulama Alanı", "Avantaj / Risk"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Lazer Ablasyon (CO2)", "isMasked": False},
                                {"text": "İnvazyon şüphesi olmayan multifokal lezyonlar", "isMasked": True, "hint": "yüzeyel buharlaştırma yöntemi"},
                                {"text": "Anatomi korunur, ancak histopatolojik sınır değerlendirilemez"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Cerrahi / LEEP Eksizyon", "isMasked": False},
                                {"text": "Şüpheli, ülsere veya soliter odaklar", "isMasked": False},
                                {"text": "Kesin patolojik sınır incelemesi sağlar", "isMasked": True, "hint": "invazyonu dışlama avantajı"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Multifokal VIN ve Nüks Yönetimi",
                    "steps": [
                        "1. HPV İnokülasyonu: Genç kadında yüksek riskli HPV labiumlar ve perinede yerleşir.",
                        "2. Multifokal Lezyonlar: Pigmente ve beyaz papüller birden fazla odakta belirir.",
                        "3. Eksizyon / Ablasyon: Gözle görülen lezyonlar LEEP veya lazerle temizlenir.",
                        "4. Alan Kanserleşmesi ve Nüks: Çevre dokudaki latent virüs aylar sonra yeni odak oluşturur; takip sürdürülür."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Genç kadınlarda yüksek riskli HPV ilişkili klasik VIN olgularında lezyonlar cerrahi olarak tamamen temizlense dahi nüksün sık görülmesinin nedeni nedir?",
                    "answer": "HPV'nin tüm alt genital traktus epitelinde latent olarak bulunabilmesi ve 'alan kanserleşmesi' fenomenidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Klasik VIN (uVIN) Yönetimi",
                    "items": [
                        {"text": "Klasik VIN genç kadınlarda sıklıkla çok odaklı yerleşim gösterir.", "isLie": False, "explanation": "Doğru. Multifokal tutulum sıktır."},
                        {"text": "İnvazyon şüphesi yoksa lazer ablasyon veya LEEP uygulanabilir.", "isLie": False, "explanation": "Doğru. Doku koruyucu yöntemlerdir."},
                        {"text": "Alan kanserleşmesi nedeniyle tedavi sonrası nüks riski mevcuttur.", "isLie": False, "explanation": "Doğru. Uzun takip gerektirir."},
                        {"text": "Klasik VIN hastalarına zorunlu olarak her iki bacağın ampütasyonu yapılır.", "isLie": True, "explanation": "Tuzak! VIN yüzeysel intraepitelyal lezyondur, bacak ampütasyonu kesinlikle yapılmaz."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "32 yaşında sigara içen bir kadında vulva ve perinede çok odaklı pigmente papüller saptanıyor; biyopside tam kat atipi gösteren klasik VIN (uVIN) doğrulanıyor. Bu hasta ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Yüksek riskli HPV ilişkili multifokal bir lezyondur; lokal tedaviler sonrası alan kanserleşmesi nedeniyle nüks riski taşır",
                            "isCorrect": True,
                            "explanation": "Klasik VIN yüksek riskli HPV kökenli, multifokal ve nüks eğilimli bir tablodur."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca menopoz sonrası 90 yaş üstü kadınlarda görülen bir kemik hastalığıdır",
                            "isCorrect": False,
                            "explanation": "Genç kadınların genital intraepitelyal neoplazisidir."
                        },
                        {
                            "key": "C",
                            "text": "Lezyonlar 1 saat içinde kendiliğinden diş minesine dönüşür",
                            "isCorrect": False,
                            "explanation": "Biyolojik gerçekliği yoktur."
                        },
                        {
                            "key": "D",
                            "text": "HPV enfeksiyonu ile hiçbir biyolojik ve epidemiyolojik bağlantısı yoktur",
                            "isCorrect": False,
                            "explanation": "HPV tip 16 temel etyolojik faktördür."
                        }
                    ]
                }
            ]
        },
        # S78
        {
            "slideNumber": 78,
            "title": "Vajinal Kanserlerde Radyoterapi İlkeleri ve Komplikasyonları",
            "subtitle": "Brakiterapi, eksternal ışınlama, mesane-rektum fistülleri ve vajinal stenoz",
            "clinicalFocus": "Radyasyon Onkolojisi ve Komplikasyonlar",
            "content": "Ders notunda belirtildiği üzere primer vajinal karsinom son derece nadirdir ve cerrahi olarak geniş rezeksiyon yapılması mesane, rektum ve üretra yakınlığı nedeniyle anatomik olarak çok güçtür. Bu nedenle çoğu vajinal karsinomda **primer tedavi radyoterapidir**.\n\n- **Radyoterapi Modaliteleri:** Eksternal pelvik radyoterapi (EBRT) ile bölgesel iliak lenf nodları ışınlanırken; vajina lümenine yerleştirilen radyoaktif kaynaklarla **brakiterapi (intrakaviter radyasyon)** uygulanarak tümör yatağına yüksek doz verilir.\n- **Geç Radyasyon Hasarları:** Radyasyon çevre normal dokularda mikrodamar hasarı (**obliteratif endarterit**) ve yaygın doku fibrozisi başlatır.\n- **Ağır Komplikasyonlar:** Vajina duvarında fibrotik daralma ve yapışıklık (**vajinal stenoz**), mukozal nekroz, rektovajinal veya vezikovajinal **fistül oluşumu** ile radyasyon sistiti/proktiti gelişebilir.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Vajinal karsinomların primer tedavisinde radyoterapi esastır; obliteratif endarterite bağlı doku nekrozu nedeniyle en korkulan geç komplikasyon rektovajinal ve vezikovajinal fistüllerdir.",
            "synthesisNarrative": "Ders notunda belirtildiği üzere primer vajinal karsinom son derece nadirdir ve cerrahi olarak geniş rezeksiyon yapılması mesane, rektum ve üretra yakınlığı nedeniyle anatomik olarak çok güçtür. Bu nedenle çoğu vajinal karsinomda **primer tedavi radyoterapidir**.\n\n- **Radyoterapi Modaliteleri:** Eksternal pelvik radyoterapi (EBRT) ile bölgesel iliak lenf nodları ışınlanırken; vajina lümenine yerleştirilen radyoaktif kaynaklarla **brakiterapi (intrakaviter radyasyon)** uygulanarak tümör yatağına yüksek doz verilir.\n- **Geç Radyasyon Hasarları:** Radyasyon çevre normal dokularda mikrodamar hasarı (**obliteratif endarterit**) ve yaygın doku fibrozisi başlatır.\n- **Ağır Komplikasyonlar:** Vajina duvarında fibrotik daralma ve yapışıklık (**vajinal stenoz**), mukozal nekroz, rektovajinal veya vezikovajinal **fistül oluşumu** ile radyasyon sistiti/proktiti gelişebilir.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Vajinal karsinomların primer tedavisinde radyoterapi esastır; obliteratif endarterite bağlı doku nekrozu nedeniyle en korkulan geç komplikasyon rektovajinal ve vezikovajinal fistüllerdir.",
            "bulletPoints": [
                "Vajinal karsinomun anatomik komşulukları nedeniyle primer tedavisi radyoterapidir.",
                "Eksternal ışınlama ve intrakaviter brakiterapi kombine edilir.",
                "Geç dönemde vajinal stenoz ve mesane/rektum fistülleri gelişebilir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Vajinal radyoterapinin doku iskemisi ve nekrozuna bağlı en ağır komplikasyonlarından biri fistül oluşumu tablosudur.",
                    "maskedTerm": "fistül oluşumu",
                    "hint": "Vajina ile mesane veya rektum arasında gelişen yapay delik/kanal"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Vajinal Radyoterapi Komplikasyonları",
                    "tableHeaders": ["Dönem", "Patolojik Mekanizma", "Klinik Tablo"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Erken Dönem", "isMasked": False},
                                {"text": "Mukozal inflamasyon, ödem ve dökülme", "isMasked": False},
                                {"text": "Radyasyon vajiniti, ağrı ve sulu akıntı", "isMasked": True, "hint": "akut ışın inflamasyonu"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Geç Dönem", "isMasked": False},
                                {"text": "Obliteratif endarterit, doku iskemisi ve fibrozis", "isMasked": True, "hint": "damar tıkanıklığı ve sertleşme"},
                                {"text": "Vajinal stenoz, rektovajinal/vezikovajinal fistül"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Radyasyon İskemisinden Fistül Oluşumuna",
                    "steps": [
                        "1. İntens Radyoterapi: Tümör yatağına brakiterapi ve eksternal ışınlama verilir.",
                        "2. Damar Hasarı: İnce kapillerlerde endotel şişer ve obliteratif endarterit başlar.",
                        "3. İskemik Nekroz: Vajina ve rektum/mesane ara duvarında doku beslenemeyerek çürür.",
                        "4. Fistül Gelişimi: Duvar delinecek rektovajinal veya vezikovajinal fistül açılır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Pelvik radyoterapi sonrasında dokularda fibrozis ve fistül gelişimine zemin hazırlayan temel mikrovasküler patolojik değişiklik nedir?",
                    "answer": "Obliteratif endarterit; küçük damarların iç yüzeyinin kalınlaşarak lümenin daralması ve dokuda kronik iskemi oluşturmasıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Vajinal Radyoterapi ve Komplikasyonları",
                    "items": [
                        {"text": "Vajinal karsinom tedavisinde radyoterapi primer modalitedir.", "isLie": False, "explanation": "Doğru. Anatomik güçlükler nedeniyle cerrahi sınırlıdır."},
                        {"text": "Brakiterapi vajina içine radyoaktif kaynak yerleştirilerek uygulanır.", "isLie": False, "explanation": "Doğru. İntrakaviter yöntemdir."},
                        {"text": "Geç dönemde vajinal stenoz ve fistül oluşumu riski vardır.", "isLie": False, "explanation": "Doğru. İskemiye bağlı ağır komplikasyonlardır."},
                        {"text": "Radyoterapi verilen bölgedeki tüm hücreler derhal saf elmasa dönüşür.", "isLie": True, "explanation": "Tuzak! Radyoterapi dokuda iskemi, nekroz ve fibrozis yapar."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Primer vajinal skuamöz karsinom nedeniyle brakiterapi ve pelvik radyoterapi uygulanan bir hastada radyasyonun neden olduğu obliteratif endarterite bağlı olarak en sık çekinilen geç dönem komplikasyon hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Doku iskemisi ve nekrozuna bağlı rektovajinal veya vezikovajinal fistül oluşumu",
                            "isCorrect": True,
                            "explanation": "Radyasyon endarteriti iskemik nekroza ve organlar arası fistüllere yol açabilir."
                        },
                        {
                            "key": "B",
                            "text": "Akut apandisit iltihaplanması",
                            "isCorrect": False,
                            "explanation": "Apandisit vajinal radyasyonun direkt komplikasyonu değildir."
                        },
                        {
                            "key": "C",
                            "text": "Hastanın boyunun aniden 20 cm uzaması",
                            "isCorrect": False,
                            "explanation": "Biyolojik olarak imkansızdır."
                        },
                        {
                            "key": "D",
                            "text": "Kemik iliğinde aşırı miktarda hemoglobin üretilmesi",
                            "isCorrect": False,
                            "explanation": "Radyasyon kemik iliğini baskılar, artırmaz."
                        }
                    ]
                }
            ]
        },
        # S79
        {
            "slideNumber": 79,
            "title": "Sarkoma Botryoides'te Multimodal Kemoterapi ve Cerrahi",
            "subtitle": "Organ koruyucu cerrahi, VAC kemoterapi protokolü ve prognoz devrimi",
            "clinicalFocus": "Modern Pediatrik Onkoloji",
            "content": "Geçmiş yıllarda 5 yaş altı kız çocuklarında saptanan **Sarkoma Botryoides (embriyonel rabdomiyosarkom)** vakalarında standart tedavi, radikal pelvik ekzanterasyon (mesane, vajen ve uterusun tamamen çıkarılması) idi; buna rağmen ölüm oranları çok yüksekti.\n\n- **Modern Tedavi Yaklaşımı:** Günümüzde sarkoma botryoides'in tedavisinde **multimodal kemoterapi** temel omurgayı oluşturur. Başta vinkristin, aktinomisin D ve siklofosfamid (**VAC protokolü**) olmak üzere yoğun sistemik kemoterapi uygulanır.\n- **Neoadjuvan Küçülme:** Kemoterapi üzüm salkımı benzeri kitleyi dramatik biçimde eriterek mikroskobik boyutlara geriletir.\n- **Organ Koruyucu Cerrahi:** Tümör küçüldükten sonra radikal cerrahi yerine çocuklarda mesane ve rektumu koruyan konservatif lokal rezeksiyon yapılır. Bu multimodal protokol sayesinde sağkalım oranları %80-90'ın üzerine çıkmıştır.\n\n> [!NOTE]\n> Pediatrik yumuşak doku sarkomlarında kemoterapiye son derece duyarlı bir histoloji söz konusudur; radikal sakatlayıcı cerrahilerin yerini organ koruyucu yaklaşımlar almıştır.",
            "synthesisNarrative": "Geçmiş yıllarda 5 yaş altı kız çocuklarında saptanan **Sarkoma Botryoides (embriyonel rabdomiyosarkom)** vakalarında standart tedavi, radikal pelvik ekzanterasyon (mesane, vajen ve uterusun tamamen çıkarılması) idi; buna rağmen ölüm oranları çok yüksekti.\n\n- **Modern Tedavi Yaklaşımı:** Günümüzde sarkoma botryoides'in tedavisinde **multimodal kemoterapi** temel omurgayı oluşturur. Başta vinkristin, aktinomisin D ve siklofosfamid (**VAC protokolü**) olmak üzere yoğun sistemik kemoterapi uygulanır.\n- **Neoadjuvan Küçülme:** Kemoterapi üzüm salkımı benzeri kitleyi dramatik biçimde eriterek mikroskobik boyutlara geriletir.\n- **Organ Koruyucu Cerrahi:** Tümör küçüldükten sonra radikal cerrahi yerine çocuklarda mesane ve rektumu koruyan konservatif lokal rezeksiyon yapılır. Bu multimodal protokol sayesinde sağkalım oranları %80-90'ın üzerine çıkmıştır.\n\n> [!NOTE]\n> Pediatrik yumuşak doku sarkomlarında kemoterapiye son derece duyarlı bir histoloji söz konusudur; radikal sakatlayıcı cerrahilerin yerini organ koruyucu yaklaşımlar almıştır.",
            "bulletPoints": [
                "Sarkoma botryoides tedavisinde temel yöntem multimodal kemoterapidir.",
                "VAC rejimi tümörü hızla küçülterek organ korumayı sağlar.",
                "Modern protokolle çocuklarda sağkalım oranı %80-90'a ulaşmıştır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Sarkoma botryoides tedavisinde tümörü hızla küçülterek organ koruyucu cerrahiye olanak tanıyan temel yaklaşım multimodal kemoterapi protokolüdür.",
                    "maskedTerm": "multimodal kemoterapi",
                    "hint": "VAC rejimi gibi kombine sitostatik ilaç tedavisi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Sarkoma Botryoides Tedavi Evrimi",
                    "tableHeaders": ["Tedavi Çağı", "Uygulanan Yaklaşım", "Klinik Çıktı / Sağkalım"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Tarihsel Yaklaşım", "isMasked": False},
                                {"text": "Radikal pelvik ekzanterasyon (tüm organların çıkarılması)", "isMasked": True, "hint": "sakatlayıcı aşırı cerrahi"},
                                {"text": "Ağır morbidite ve düşük sağkalım"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Modern Protokol", "isMasked": False},
                                {"text": "Neoadjuvan kemoterapi + organ koruyucu cerrahi", "isMasked": True, "hint": "ilaçla küçültme ve koruyucu rezeksiyon"},
                                {"text": "Yüksek sağkalım (%85+) ve organ fonksiyonu korunur"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Pediatrik Sarkomda Multimodal Başarı",
                    "steps": [
                        "1. Tanı: 2 yaşındaki kız çocuğunda üzüm salkımı botriyoid kitle doğrulanır.",
                        "2. Neoadjuvan Kemoterapi: VAC protokolü başlanarak rabdomiyoblastlar öldürülür.",
                        "3. Tümör Regresyonu: Lümeni dolduran dev kitle mikroskobik sınırlara kadar geriler.",
                        "4. Organ Koruyucu Cerrahi: Mesane ve rektum korunarak bakiye tümör odağı çıkarılır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Sarkoma botryoides tedavisinde tarihsel sakatlayıcı radikal ekzanterasyonların yerini alan ve %80-90 sağkalım sağlayan modern yaklaşım nedir?",
                    "answer": "Neoadjuvan multimodal kemoterapi (VAC protokolü) ve ardından uygulanan organ koruyucu konservatif cerrahidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Sarkoma Botryoides Tedavisi",
                    "items": [
                        {"text": "Sarkoma botryoides kemoterapiye duyarlı bir pediatrik yumuşak doku sarkomudur.", "isLie": False, "explanation": "Doğru. Kemoduyarlılığı yüksektir."},
                        {"text": "Modern yaklaşım neoadjuvan kemoterapi ve organ koruyucu cerrahidir.", "isLie": False, "explanation": "Doğru. Güncel standart protokoldür."},
                        {"text": "Tedavi başarısı ile 5 yıllık sağkalım %80-90 düzeyine çıkmıştır.", "isLie": False, "explanation": "Doğru. Prognozu dramatik iyileşmiştir."},
                        {"text": "Sarkoma botryoides'te hiçbir ilaç verilmez, sadece papatya çayı içirilir.", "isLie": True, "explanation": "Tuzak! Sarkoma botryoides yoğun onkolojik kemoterapi gerektiren malign bir sarkomdur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "2 yaşındaki bir kız çocuğunda saptanan embriyonel rabdomiyosarkom (Sarkoma Botryoides) olgusunda modern onkolojik tedavi protokolünün temel prensibi nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Neoadjuvan multimodal kemoterapi ile tümörü küçülterek organ koruyucu konservatif cerrahi uygulamak",
                            "isCorrect": True,
                            "explanation": "Modern tedavi kemoterapi ile kitleyi eritip mesane/rektumu koruyarak rezeksiyon yapmaktır."
                        },
                        {
                            "key": "B",
                            "text": "Doğrudan tüm pelvik organları körlemesine çıkarıp hastayı tedavisiz bırakmak",
                            "isCorrect": False,
                            "explanation": "Eski ve terk edilmiş yöntemdir."
                        },
                        {
                            "key": "C",
                            "text": "Hiçbir tedavi vermeden hastayı 18 yaşına kadar evde bekletmek",
                            "isCorrect": False,
                            "explanation": "Ölümcül sonuç doğurur."
                        },
                        {
                            "key": "D",
                            "text": "Sadece kulak damlası damlatarak tümörü yok etmeye çalışmak",
                            "isCorrect": False,
                            "explanation": "Tıbbi mantığı yoktur."
                        }
                    ]
                }
            ]
        },
        # S80
        {
            "slideNumber": 80,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 8] Profilaksi, Aşı Teknolojisi ve Tedavi Yönetimi",
            "subtitle": "Bölüm 8 kapsamındaki HPV aşıları, L1/VLP, lökoplaki biyopsisi, dVIN, uVIN ve sarkoma botryoides tedavisi sentezi",
            "clinicalFocus": "Kapsamlı Bölüm Tekrarı",
            "content": "Bölüm 8 boyunca jinekolojik patolojilerin önlenmesini, aşı teknolojilerini ve klinik yönetim basamaklarını sentezledik.\n\n- **Aşı Teknolojisi ve Kapsam:** Rekombinant L1 majör kapsid proteininden oluşan VLP partikülleri viral DNA içermez. Kuadrivalan aşı HPV 6, 11, 16 ve 18'e karşı korur; ancak aşı dışı tipler nedeniyle rutin servikal tarama sürdürülmelidir.\n- **Lökoplaki ve dVIN:** Lökoplakide kesin tanı için punch biyopsi zorunludur; dVIN p53 mutasyonlu bazal atipi gösterir ve cerrahi eksizyon gerektirir.\n- **Tedavi Modaliteleri:** Vajinal kanserde radyoterapi esastır (fistül riski); sarkoma botryoides'te ise neoadjuvan kemoterapi organ koruyucu cerrahiye olanak sağlar.\n\n> [!IMPORTANT]\n> [CHECKPOINT SENTEZİ] L1 VLP viral DNA içermez; kuadrivalan aşı 6, 11, 16, 18'i kapsar; aşılanmış bireylerde de rutin Pap taraması devam eder; dVIN p53 mutasyonludur ve cerrahi eksizyon şarttır.",
            "synthesisNarrative": "Bölüm 8 boyunca jinekolojik patolojilerin önlenmesini, aşı teknolojilerini ve klinik yönetim basamaklarını sentezledik.\n\n- **Aşı Teknolojisi ve Kapsam:** Rekombinant L1 majör kapsid proteininden oluşan VLP partikülleri viral DNA içermez. Kuadrivalan aşı HPV 6, 11, 16 ve 18'e karşı korur; ancak aşı dışı tipler nedeniyle rutin servikal tarama sürdürülmelidir.\n- **Lökoplaki ve dVIN:** Lökoplakide kesin tanı için punch biyopsi zorunludur; dVIN p53 mutasyonlu bazal atipi gösterir ve cerrahi eksizyon gerektirir.\n- **Tedavi Modaliteleri:** Vajinal kanserde radyoterapi esastır (fistül riski); sarkoma botryoides'te ise neoadjuvan kemoterapi organ koruyucu cerrahiye olanak sağlar.\n\n> [!IMPORTANT]\n> [CHECKPOINT SENTEZİ] L1 VLP viral DNA içermez; kuadrivalan aşı 6, 11, 16, 18'i kapsar; aşılanmış bireylerde de rutin Pap taraması devam eder; dVIN p53 mutasyonludur ve cerrahi eksizyon şarttır.",
            "bulletPoints": [
                "L1 VLP aşıları viral DNA içermez; kuadrivalan aşı HPV 6, 11, 16 ve 18'i hedefler.",
                "Aşı sonrası aşı dışı suşlar nedeniyle servikal tarama devam etmelidir.",
                "dVIN p53 mutasyonludur ve cerrahi eksizyon gerektirir; sarkomda kemoterapi organı korur."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Kuadrivalan HPV aşısı genital siğil etkeni HPV 6 ve 11 ile kanser etkeni HPV 16 ve 18 tiplerine karşı korur.",
                    "maskedTerm": "HPV 6 ve 11",
                    "hint": "Düşük riskli kondilom oluşturan viral suşlar"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bölüm 8 Yönetim ve Profilaksi Özeti",
                    "tableHeaders": ["Antite / Süreç", "Temel Mekanizma / Özellik", "Klinik Yaklaşım"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "L1 Rekombinant VLP", "isMasked": False},
                                {"text": "DNA içermeyen içi boş kapsid partikülü", "isMasked": True, "hint": "güvenli aşı antijeni"},
                                {"text": "Profilaktik aşılama (tarama yine de devam eder)"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Diferansiye VIN (dVIN)", "isMasked": False},
                                {"text": "Bazal atipi ve p53 gen mutasyonu", "isMasked": True, "hint": "HPV negatif premalign lezyon"},
                                {"text": "Negatif sınırlarla geniş lokal cerrahi eksizyon"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Bölüm 8 Yönetim Algoritması Zinciri",
                    "steps": [
                        "1. Birincil Koruma: Adölesan dönemde L1 VLP kuadrivalan/dokuzlu aşı yapılır.",
                        "2. Tarama Sürekliliği: Aşı dışı tipler için rutin Pap smear ve HPV testi sürdürülür.",
                        "3. Lökoplaki Triyajı: Şüpheli vulvar beyaz plaklardan punch biyopsi alınır.",
                        "4. Hedefe Yönelik Tedavi: dVIN cerrahiyle çıkarılır, pediatrik sarkom kemoterapiyle küçültülür."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bölüm 8 kapsamında incelenen konulardan kuadrivalan HPV aşısının içerdiği 4 viral suş ve aşılanmış kadınlarda taramanın neden devam etmesi gerektiği kuralı nedir?",
                    "answer": "Aşı HPV 6, 11, 16 ve 18'i içerir; aşı kapsamı dışındaki diğer onkojenik suşlar kanser yapabildiği için rutin tarama aynen sürdürülmelidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Bölüm 8 Genel Tekrar",
                    "items": [
                        {"text": "Kuadrivalan aşı HPV 6, 11, 16 ve 18'e karşı kombine koruma sağlar.", "isLie": False, "explanation": "Doğru. Dört tipi hedefler."},
                        {"text": "VLP partikülleri viral DNA içermediğinden enfeksiyon yapamaz.", "isLie": False, "explanation": "Doğru. İçi boş protein kapsiddir."},
                        {"text": "Aşılanmış bireylerde de rutin servikal taramaya devam edilmelidir.", "isLie": False, "explanation": "Doğru. Temel kılavuz kuralıdır."},
                        {"text": "dVIN saptandığında hiçbir cerrahi yapılmaz, lezyon sadece pudralanır.", "isLie": True, "explanation": "Tuzak! dVIN agresif premalign lezyondur, geniş cerrahi eksizyon şarttır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Bölüm 8'de incelenen profilaksi ve klinik yönetim konuları ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "L1 VLP aşısı viral DNA içermez; kuadrivalan aşı 6, 11, 16, 18'i kapsar ve aşılanmış kadınlarda da servikal tarama devam etmelidir",
                            "isCorrect": True,
                            "explanation": "Bu sentez cümlesi hem aşı biyolojisini hem de taramanın sürekliliği kuralını eksiksiz özetler."
                        },
                        {
                            "key": "B",
                            "text": "HPV aşısı yapılmış kadınların artık hiçbir zaman doktora gitmesine gerek kalmaz",
                            "isCorrect": False,
                            "explanation": "Tarama protokolleri aşılanmışlarda da devam eder."
                        },
                        {
                            "key": "C",
                            "text": "dVIN yalnızca safra kesesinde taş oluşumu ile seyreden selim bir durumdur",
                            "isCorrect": False,
                            "explanation": "Vulvanın premalign neoplastik tablosudur."
                        },
                        {
                            "key": "D",
                            "text": "Vajinal karsinomda radyoterapi yerine sadece aspirin tableti verilmesi yeterlidir",
                            "isCorrect": False,
                            "explanation": "Kanser tedavisinde yeri yoktur."
                        }
                    ]
                }
            ]
        }
    ]
    return slides

if __name__ == '__main__':
    slides = get_s8_slides()
    print(f'Section 8 generated with {len(slides)} slides.')
