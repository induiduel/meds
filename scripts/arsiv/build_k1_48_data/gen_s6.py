import json

def get_s6_slides():
    slides = [
        # S51
        {
            "slideNumber": 51,
            "title": "Servikal Glandüler Lezyonlar ve Adenokarsinoma in Situ (AIS)",
            "subtitle": "Endoservikal bez atipisi, HPV-18 ilişkisi ve atlamalı lezyonlar",
            "clinicalFocus": "Preinvaziv Glandüler Neoplazi",
            "content": "Servikal neoplaziler yalnızca yassı epitel ile sınırlı kalmayıp, endoservikal kanalı döşeyen müsin salgılayan kolumnar glandüler epitelden de köken alabilir. Bu sürecin premalign öncülü **Adenokarsinoma in Situ (AIS)** tablosudur.\n\n- **Etyoloji ve HPV İlişkisi:** Skuamöz karsinomlarda baskın tip HPV-16 iken, servikal glandüler neoplazilerde ve adenokarsinomalarda **HPV tip 18** belirgin biçimde daha yüksek oranda saptanır.\n- **Histopatoloji:** Endoservikal bezlerin yapısı korunmuş olmakla birlikte, bezleri döşeyen kolumnar hücrelerde nükleer psödostratifikasyon, hiperkromazi, sitoplazmik müsin kaybı ve artmış apikal mitozlar/apoptozis izlenir. Bazal membran kesinlikle intakttır.\n- **Klinik Zorluk (Atlamalı Tutulum):** AIS lezyonları sıklıkla endoservikal kanalın derinliklerinde yerleşir ve arada normal bezlerin bulunduğu multifokal 'atlamalı lezyonlar' (skip lesions) şeklinde dağılır. Bu nedenle kolposkopi ve biyopside yakalanması skuamöz lezyonlara göre çok daha zordur.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Servikal adenokarsinom ve öncülü AIS gelişiminde HPV-18 ön plandadır; lezyonlar endoservikal kanalda atlamalı (skip) odaklar oluşturduğundan cerrahi sınır değerlendirmesi zordur.",
            "synthesisNarrative": "Servikal neoplaziler yalnızca yassı epitel ile sınırlı kalmayıp, endoservikal kanalı döşeyen müsin salgılayan kolumnar glandüler epitelden de köken alabilir. Bu sürecin premalign öncülü **Adenokarsinoma in Situ (AIS)** tablosudur.\n\n- **Etyoloji ve HPV İlişkisi:** Skuamöz karsinomlarda baskın tip HPV-16 iken, servikal glandüler neoplazilerde ve adenokarsinomalarda **HPV tip 18** belirgin biçimde daha yüksek oranda saptanır.\n- **Histopatoloji:** Endoservikal bezlerin yapısı korunmuş olmakla birlikte, bezleri döşeyen kolumnar hücrelerde nükleer psödostratifikasyon, hiperkromazi, sitoplazmik müsin kaybı ve artmış apikal mitozlar/apoptozis izlenir. Bazal membran kesinlikle intakttır.\n- **Klinik Zorluk (Atlamalı Tutulum):** AIS lezyonları sıklıkla endoservikal kanalın derinliklerinde yerleşir ve arada normal bezlerin bulunduğu multifokal 'atlamalı lezyonlar' (skip lesions) şeklinde dağılır. Bu nedenle kolposkopi ve biyopside yakalanması skuamöz lezyonlara göre çok daha zordur.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Servikal adenokarsinom ve öncülü AIS gelişiminde HPV-18 ön plandadır; lezyonlar endoservikal kanalda atlamalı (skip) odaklar oluşturduğundan cerrahi sınır değerlendirmesi zordur.",
            "bulletPoints": [
                "AIS, servikal adenokarsinomun kanıtlanmış öncü glandüler lezyonudur.",
                "Özellikle HPV tip 18 enfeksiyonu ile güçlü ilişki gösterir.",
                "Endoservikal kanalda atlamalı (skip) odaklar yaparak tanıyı zorlaştırır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Servikal glandüler lezyonlar ve adenokarsinom gelişiminde en sık saptanan yüksek riskli viral tip HPV 18 suşudur.",
                    "maskedTerm": "HPV 18",
                    "hint": "Glandüler diferansiasyonda baskın yüksek onkojenik virüs tipi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Skuamöz Prekanser (CIN 3) vs Glandüler Prekanser (AIS)",
                    "tableHeaders": ["Özellik", "CIN 3 (Karsinoma in Situ)", "AIS (Adenokarsinoma in Situ)"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Epitel Kökeni", "isMasked": False},
                                {"text": "Çok katlı yassı epitel", "isMasked": False},
                                {"text": "Endoservikal tek katlı kolumnar bez epiteli", "isMasked": True, "hint": "müsin üreten glandüler yapı"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Baskın HPV Tipi", "isMasked": False},
                                {"text": "HPV tip 16 baskın", "isMasked": False},
                                {"text": "HPV tip 18 yüksek oranda ilişkili", "isMasked": True, "hint": "glandüler neoplazide öne çıkan tip"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "HPV-18'den Endoservikal AIS Gelişimi",
                    "steps": [
                        "1. Endoservikal Enfeksiyon: HPV tip 18 servikal kanalın kolumnar bez epitelini enfekte eder.",
                        "2. Nükleer Psödostratifikasyon: Bez hücrelerinde nükleer polarite kaybolur, çekirdekler lümene yığılır.",
                        "3. Müsin Kaybı ve Mitoz: Sitoplazmik müsin azalırken apikal mitoz ve apoptozlar artar.",
                        "4. Adenokarsinoma in Situ: Bez mimarisi korunmuş halde tam kat glandüler atipi oluşur (AIS)."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Servikal skuamöz karsinomlarda en sık HPV-16 görülürken, servikal glandüler neoplaziler ve adenokarsinomlarda hangi HPV tipi belirgin oranda öne çıkar?",
                    "answer": "HPV tip 18; endoservikal glandüler karsinogenezde baskın yüksek riskli tiptir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Adenokarsinoma in Situ (AIS)",
                    "items": [
                        {"text": "AIS, endoservikal kolumnar bez epitelinin premalign neoplastik tablosudur.", "isLie": False, "explanation": "Doğru. Glandüler karsinoma in situ lezyonudur."},
                        {"text": "Servikal glandüler neoplazilerde HPV-18 ilişkisi oldukça yüksektir.", "isLie": False, "explanation": "Doğru. Tipik viral ilişkidir."},
                        {"text": "AIS lezyonları endoservikal kanalda atlamalı (skip) odaklar oluşturabilir.", "isLie": False, "explanation": "Doğru. Multifokal yerleşim tanıyı zorlaştırır."},
                        {"text": "AIS tanısı konduğu anda kemik dokusuna doğrudan masif metastaz gelişmiştir.", "isLie": True, "explanation": "Tuzak! AIS in situ bir lezyondur, bazal membran aşılmadığı için metastaz yapamaz."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Endoservikal adenokarsinoma in situ (AIS) ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Endoservikal glandüler epitelin premalign lezyonudur ve sıklıkla HPV-18 enfeksiyonu ile ilişkilidir",
                            "isCorrect": True,
                            "explanation": "AIS müsinöz glandüler epitelin öncü lezyonudur ve HPV-18 ile belirgin birliktelik gösterir."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca safra kesesi taşlarının mekanik sürtünmesiyle oluşur",
                            "isCorrect": False,
                            "explanation": "Serviks glandüler epitelinin HPV kaynaklı neoplazisidir."
                        },
                        {
                            "key": "C",
                            "text": "Tümör hücreleri hiçbir zaman mitoz veya nükleer atipi göstermez",
                            "isCorrect": False,
                            "explanation": "AIS belirgin nükleer hiperkromazi, mitoz ve atipi ile tanımlanır."
                        },
                        {
                            "key": "D",
                            "text": "HPV enfeksiyonu ile hiçbir bilimsel ilişkisi bulunmamaktadır",
                            "isCorrect": False,
                            "explanation": "Yüksek riskli HPV (özellikle tip 18) temel etyolojik faktördür."
                        }
                    ]
                }
            ]
        },
        # S52
        {
            "slideNumber": 52,
            "title": "İnvaziv Servikal Adenokarsinom ve İleri Tipler",
            "subtitle": "Müsinöz diferansiasyon, papiller yapılar ve adenoid kistik patern",
            "clinicalFocus": "Malign Glandüler Tümörler",
            "content": "Servikal kanserlerin yaklaşık %15-20'sini oluşturan **servikal adenokarsinom**, tarama programlarının yaygınlaşmasıyla skuamöz karsinom insidansı düşerken oransal olarak daha sık karşımıza çıkmaktadır.\n\n- **Histopatolojik Görünüm:** En yaygın formu endoservikal tip müsinöz adenokarsinomdur. Düzensiz, dallanan, sırt sırta vermiş (back-to-back) kribriform glandüler yapılar stromayı infiltre eder. Hücreler bol nükleer atipi ve intrasitoplazmik müsin içerir.\n- **Klinik Seyir ve Prognoz:** Adenokarsinomlar endoservikal kanal içinde derin yerleşimli olduklarından Pap smear taramasında skuamöz karsinomlara göre daha kolay gözden kaçabilir. Genellikle daha ileri evrede yakalanır ve benzer evredeki skuamöz karsinomlara kıyasla lenf nodu metastazı ve nüks riski biraz daha yüksektir.\n- **Mikst Tümörler:** Bazı olgularda skuamöz ve glandüler diferansiasyon bir arada bulunur ve bu tümörler **adenoskuamöz karsinom** olarak adlandırılır; klinik seyirleri oldukça agresiftir.\n\n> [!NOTE]\n> Adenoskuamöz karsinomlar hem malign glandüler hem malign skuamöz komponentler içerir ve standart skuamöz karsinomdan daha kötü prognozludur.",
            "synthesisNarrative": "Servikal kanserlerin yaklaşık %15-20'sini oluşturan **servikal adenokarsinom**, tarama programlarının yaygınlaşmasıyla skuamöz karsinom insidansı düşerken oransal olarak daha sık karşımıza çıkmaktadır.\n\n- **Histopatolojik Görünüm:** En yaygın formu endoservikal tip müsinöz adenokarsinomdur. Düzensiz, dallanan, sırt sırta vermiş (back-to-back) kribriform glandüler yapılar stromayı infiltre eder. Hücreler bol nükleer atipi ve intrasitoplazmik müsin içerir.\n- **Klinik Seyir ve Prognoz:** Adenokarsinomlar endoservikal kanal içinde derin yerleşimli olduklarından Pap smear taramasında skuamöz karsinomlara göre daha kolay gözden kaçabilir. Genellikle daha ileri evrede yakalanır ve benzer evredeki skuamöz karsinomlara kıyasla lenf nodu metastazı ve nüks riski biraz daha yüksektir.\n- **Mikst Tümörler:** Bazı olgularda skuamöz ve glandüler diferansiasyon bir arada bulunur ve bu tümörler **adenoskuamöz karsinom** olarak adlandırılır; klinik seyirleri oldukça agresiftir.\n\n> [!NOTE]\n> Adenoskuamöz karsinomlar hem malign glandüler hem malign skuamöz komponentler içerir ve standart skuamöz karsinomdan daha kötü prognozludur.",
            "bulletPoints": [
                "Serviks karsinomlarının %15-20'si adenokarsinom tipindedir.",
                "Endoservikal kanalda sırt sırta vermiş atipik bez yapıları ile karakterizedir.",
                "Adenoskuamöz karsinom mikst diferansiasyon gösterir ve agresif seyreder."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Hem malign skuamöz hem de malign glandüler komponentleri bir arada içeren agresif serviks tümörüne adenoskuamöz karsinom adı verilir.",
                    "maskedTerm": "adenoskuamöz karsinom",
                    "hint": "Mikst diferansiasyon gösteren iki komponentli malign epitelyal tümör"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Servikal Epitelyal Karsinom Tipleri",
                    "tableHeaders": ["Tümör Tipi", "Oransal Sıklık", "Baskın Diferansiasyon"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Skuamöz Hücreli Karsinom", "isMasked": False},
                                {"text": "%80 - 85", "isMasked": False},
                                {"text": "Keratinizasyon, interselüler köprüler", "isMasked": True, "hint": "yassı epitel özellikleri"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Servikal Adenokarsinom", "isMasked": False},
                                {"text": "%15 - 20", "isMasked": True, "hint": "ikinci en sık epiteliyal malignite oranı"},
                                {"text": "Müsin salgılayan atipik glandüler yapılar"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Endoservikal Adenokarsinomun İnvazyon Zinciri",
                    "steps": [
                        "1. AIS Evresi: Endoservikal bezlerde atipik nükleer tabakalaşma ve müsin tükenmesi başlar.",
                        "2. Stromal Mikroinvazyon: Kribriform bez yapıları bez bazal membranını yırtarak serviks lifli dokusuna geçer.",
                        "3. Derin Kanal Tutulumu: Tümör endoservikal kanal boyunca derinlemesine genişler ve desmoplazi yapar.",
                        "4. Klinik Belirti: Derin yerleşim nedeniyle Pap smear negatif kalabilirken hasta postkoital kanamayla başvurur."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Serviks karsinomunda malign skuamöz ve malign glandüler bileşenlerin aynı tümörde bir arada bulunması hangi patolojik tanı ile ifade edilir?",
                    "answer": "Adenoskuamöz karsinom; saf skuamöz karsinoma göre daha agresif klinik seyir gösterir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Servikal Adenokarsinom",
                    "items": [
                        {"text": "Servikal karsinomların yaklaşık %15-20'sini adenokarsinomlar oluşturur.", "isLie": False, "explanation": "Doğru. Skuamöz karsinomdan sonraki en sık gruptur."},
                        {"text": "Endoservikal kanal derinliklerinde yerleştiği için Pap smear ile yakalanması daha güç olabilir.", "isLie": False, "explanation": "Doğru. Örnekleme zorluğu vardır."},
                        {"text": "Adenoskuamöz karsinom mikst diferansiasyonlu ve agresif bir tümördür.", "isLie": False, "explanation": "Doğru. İki malign komponent barındırır."},
                        {"text": "Adenokarsinom daima sadece saç diplerindeki yağ bezlerinden köken alır.", "isLie": True, "explanation": "Tuzak! Servikal adenokarsinom endoservikal kanalın kolumnar bez epitelinden gelişir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servikal adenokarsinomların histopatolojik ve klinik özellikleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Endoservikal kanal bezlerinden köken alır ve skuamöz karsinoma göre Pap smear ile yakalanması daha güçtür",
                            "isCorrect": True,
                            "explanation": "Kanal içi derin yerleşim ve atlamalı tutulum nedeniyle sitolojik taramada yakalanması daha zordur."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca göz kapağında arpacık şeklinde kendini gösterir",
                            "isCorrect": False,
                            "explanation": "Uterus serviksinde gelişen bir malignitedir."
                        },
                        {
                            "key": "C",
                            "text": "Tümör hücrelerinde kesinlikle hiçbir zaman müsin üretimi izlenmez",
                            "isCorrect": False,
                            "explanation": "En yaygın formu müsinöz diferansiasyon gösteren endoservikal tiptir."
                        },
                        {
                            "key": "D",
                            "text": "Tamamen selim bir kıkırdak büyümesi olup hiçbir zaman stromal invazyon yapmaz",
                            "isCorrect": False,
                            "explanation": "Malign epiteliyal bir neoplazmdır ve stromal invazyon gösterir."
                        }
                    ]
                }
            ]
        },
        # S53
        {
            "slideNumber": 53,
            "title": "Servikal Polipler: Endoservikal Polip Morfolojisi ve Selimliği",
            "subtitle": "Kanal içi polipoid kitleler, ödemli stroma ve nadir malignite riski",
            "clinicalFocus": "Benign Polipoid Lezyon",
            "content": "Servikal polipler, yetişkin kadınların yaklaşık %2-5'inde görülen, serviksin en sık karşılaşılan benign polipoid lezyonlarıdır. Büyük çoğunluğu endoservikal kanaldan köken alır (**endoservikal polip**).\n\n- **Makroskopi:** Endoservikal os'tan vajinaya doğru sarkan, birkaç milimetreden birkaç santimetreye kadar değişebilen, parlak kırmızı, yumuşak, mukoid ve saplı (pediküllü) kitlelerdir.\n- **Mikroskopi:** Yüzeyi tek katlı müsin salgılayan endoservikal kolumnar epitel ile döşelidir. Stroması oldukça ödemli, gevşek bağ dokusu, genişlemiş konjesyone kan damarları ve kronik inflamatuar hücre infiltrasyonu içerir. Sıklıkla yüzeyel skuamöz metaplazi ve erozyon izlenir.\n- **Klinik ve Malignite Potansiyeli:** Sıklıkla asemptomatiktir; semptom verdiğinde intermenstrüel veya postkoital lekelenme tarzı kanama yapar. Malign transformasyon riski son derece düşüktür (%1'den az).\n\n> [!NOTE]\n> Endoservikal polipler neoplastik bir karsinom değil; fokal kronik inflamasyon ve damarsal konjesyona bağlı reaktif polipoid hiperplazilerdir.",
            "synthesisNarrative": "Servikal polipler, yetişkin kadınların yaklaşık %2-5'inde görülen, serviksin en sık karşılaşılan benign polipoid lezyonlarıdır. Büyük çoğunluğu endoservikal kanaldan köken alır (**endoservikal polip**).\n\n- **Makroskopi:** Endoservikal os'tan vajinaya doğru sarkan, birkaç milimetreden birkaç santimetreye kadar değişebilen, parlak kırmızı, yumuşak, mukoid ve saplı (pediküllü) kitlelerdir.\n- **Mikroskopi:** Yüzeyi tek katlı müsin salgılayan endoservikal kolumnar epitel ile döşelidir. Stroması oldukça ödemli, gevşek bağ dokusu, genişlemiş konjesyone kan damarları ve kronik inflamatuar hücre infiltrasyonu içerir. Sıklıkla yüzeyel skuamöz metaplazi ve erozyon izlenir.\n- **Klinik ve Malignite Potansiyeli:** Sıklıkla asemptomatiktir; semptom verdiğinde intermenstrüel veya postkoital lekelenme tarzı kanama yapar. Malign transformasyon riski son derece düşüktür (%1'den az).\n\n> [!NOTE]\n> Endoservikal polipler neoplastik bir karsinom değil; fokal kronik inflamasyon ve damarsal konjesyona bağlı reaktif polipoid hiperplazilerdir.",
            "bulletPoints": [
                "Endoservikal polip serviksin en yaygın benign polipoid lezyonudur.",
                "Ödemli, damardan zengin stroma ve müsinöz epitel ile karakterizedir.",
                "Malign transformasyon riski son derece düşüktür (<%1)."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Endoservikal kanaldan vajinaya doğru sarkan damardan zengin ve ödemli benign kitlelere endoservikal polip adı verilir.",
                    "maskedTerm": "endoservikal polip",
                    "hint": "Serviksin en sık görülen saplı benign inflamatuvar kitlesi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Endoservikal Polip vs Malign Servikal Tümör",
                    "tableHeaders": ["Özellik", "Endoservikal Polip", "İnvaziv Serviks Karsinomu"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Biyolojik Doğası", "isMasked": False},
                                {"text": "Tamamen selim reaktif hiperplazi", "isMasked": True, "hint": "inflamatuvar benign süreç"},
                                {"text": "Malign epiteliyal neoplazi"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Histolojik Stroma", "isMasked": False},
                                {"text": "Ödemli, konjesyone ve inflamatuvar", "isMasked": False},
                                {"text": "Desmoplastik ve atipik hücre istilası", "isMasked": True, "hint": "karsinom hücre kordonları ile dolu stroma"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "İnflamasyondan Polip Oluşumuna Patogenez",
                    "steps": [
                        "1. Kronik İrritasyon: Endoservikal kanalda mukozal inflamasyon ve venöz konjesyon başlar.",
                        "2. Fokal Mukozal Ödem: Stromada sıvı birikimi ve damar proliferasyonu lokal kabarıklık yaratır.",
                        "3. Saplı Kitle Gelişimi: Gravite ve servikal kanal kontraksiyonları dokuyu lümene doğru uzatır.",
                        "4. Basit Eksizyon: Polip basitçe bükülerek (torsiyon) tabanından çıkartılır ve tam iyileşme sağlanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Endoservikal poliplerin mikroskobik incelemesinde stroma ve epitel örtüsünün temel özellikleri nelerdir?",
                    "answer": "Yüzeyi tek katlı endoservikal kolumnar epitel (bazen skuamöz metaplazili) ile örtülüdür; stroması belirgin ödemli, konjesyone kan damarları ve kronik inflamatuar hücreler içerir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Endoservikal Polipler",
                    "items": [
                        {"text": "Endoservikal polip serviksin en sık rastlanan benign polipoid lezyonudur.", "isLie": False, "explanation": "Doğru. Kadınların %2-5'inde görülür."},
                        {"text": "Stroması ödemli bağ dokusu ve konjesyone kan damarları içerir.", "isLie": False, "explanation": "Doğru. Kolayca kanayabilen yumuşak dokudur."},
                        {"text": "Malign dönüşüm riski son derece düşüktür (%1'den az).", "isLie": False, "explanation": "Doğru. Klinik olarak tamamen selimdir."},
                        {"text": "Endoservikal polipler doğrudan kemik iliği kök hücre kanseridir.", "isLie": True, "explanation": "Tuzak! Endoservikal polipler serviks mukozasının selim reaktif lezyonlarıdır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Endoservikal polip ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Serviksin en sık görülen benign polipoid lezyonudur; ödemli stroma ve müsinöz epitel içerir",
                            "isCorrect": True,
                            "explanation": "Endoservikal polipler yaygın, selim, damardan zengin ve ödemli stroma içeren lezyonlardır."
                        },
                        {
                            "key": "B",
                            "text": "Her zaman 1 hafta içinde tüm iç organlara metastaz yaparak ölüme yol açar",
                            "isCorrect": False,
                            "explanation": "Malignite potansiyeli <%1 olan tamamen selim bir tablodur."
                        },
                        {
                            "key": "C",
                            "text": "Sadece erkeklerin böbrek üstü bezinde ortaya çıkan bir tümördür",
                            "isCorrect": False,
                            "explanation": "Kadın serviksine ait bir lezyondur."
                        },
                        {
                            "key": "D",
                            "text": "Hiçbir zaman kan damarı veya ödem içermeyen taşlaşmış kemik kitlesidir",
                            "isCorrect": False,
                            "explanation": "Son derece damardan zengin ve ödemli yumuşak doku kıvamındadır."
                        }
                    ]
                }
            ]
        },
        # S54
        {
            "slideNumber": 54,
            "title": "Vulvar ve Servikal Enfeksiyonlarda Moleküler Tanı: PCR ve NAAT",
            "subtitle": "N. gonorrhoeae ve T. pallidum tanısında nükleik asit amplifikasyonu",
            "clinicalFocus": "Moleküler Mikrobiyoloji",
            "content": "Kadın alt genital traktusunda gelişen enfeksiyonların ayırıcı tanısında, geleneksel kültür yöntemlerinin yetersiz kaldığı durumlarda modern **Nükleik Asit Amplifikasyon Testleri (NAAT / PCR)** altın standart tanı aracı haline gelmiştir.\n\n- **Neisseria gonorrhoeae Tanısı:** Üretilmesi güç, hassas bir bakteri olduğundan sürüntü örneklerinde NAAT/PCR yöntemiyle spesifik DNA dizilimlerinin çoğaltılması duyarlılığı %98'in üzerine çıkarır. Kültür ise özellikle antibiyotik duyarlılık profili için saklanır.\n- **Treponema pallidum (Sifiliz) Tanısı:** Bakteri yapay besiyerlerinde üretilemez. Erken evre şankr lezyonlarında karanlık saha mikroskopisi yapılamıyorsa lezyon eksüdasından PCR ile treponemal DNA tespiti en kesin doğrudan tanı yöntemidir.\n- **Kombine Paneller:** Tek bir servikovajinal sürüntü örneğinden HPV, Gonokok, Klamidya ve Trichomonas gibi çoklu etkenlerin eşzamanlı taranması mümkündür.\n\n> [!NOTE]\n> Ders notunda vurgulandığı üzere N. gonorrhoeae ve T. pallidum için tanıda seroloji ve kültürün yanında NAAT/PCR yöntemleri vazgeçilmezdir.",
            "synthesisNarrative": "Kadın alt genital traktusunda gelişen enfeksiyonların ayırıcı tanısında, geleneksel kültür yöntemlerinin yetersiz kaldığı durumlarda modern **Nükleik Asit Amplifikasyon Testleri (NAAT / PCR)** altın standart tanı aracı haline gelmiştir.\n\n- **Neisseria gonorrhoeae Tanısı:** Üretilmesi güç, hassas bir bakteri olduğundan sürüntü örneklerinde NAAT/PCR yöntemiyle spesifik DNA dizilimlerinin çoğaltılması duyarlılığı %98'in üzerine çıkarır. Kültür ise özellikle antibiyotik duyarlılık profili için saklanır.\n- **Treponema pallidum (Sifiliz) Tanısı:** Bakteri yapay besiyerlerinde üretilemez. Erken evre şankr lezyonlarında karanlık saha mikroskopisi yapılamıyorsa lezyon eksüdasından PCR ile treponemal DNA tespiti en kesin doğrudan tanı yöntemidir.\n- **Kombine Paneller:** Tek bir servikovajinal sürüntü örneğinden HPV, Gonokok, Klamidya ve Trichomonas gibi çoklu etkenlerin eşzamanlı taranması mümkündür.\n\n> [!NOTE]\n> Ders notunda vurgulandığı üzere N. gonorrhoeae ve T. pallidum için tanıda seroloji ve kültürün yanında NAAT/PCR yöntemleri vazgeçilmezdir.",
            "bulletPoints": [
                "NAAT/PCR alt genital enfeksiyonlarda yüksek duyarlılık sağlar.",
                "N. gonorrhoeae tanısında kültürün yerini büyük oranda almıştır.",
                "T. pallidum yapay besiyerinde üretilemediğinden PCR doğrudan tanıda kritiktir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Genital enfeksiyonlarda mikroorganizma DNA'sını çoğaltarak yüksek duyarlılıkla tanı koyduran test grubu NAAT testleridir.",
                    "maskedTerm": "NAAT",
                    "hint": "Nükleik asit amplifikasyon testi kısaltması"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Genital Patojenlerde Tanı Yöntemleri",
                    "tableHeaders": ["Patojen Etken", "Birincil / Moleküler Yöntem", "Geleneksel / Tamamlayıcı Yöntem"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Neisseria gonorrhoeae", "isMasked": False},
                                {"text": "NAAT / PCR nükleik asit tespiti", "isMasked": True, "hint": "nükleik asit amplifikasyonu"},
                                {"text": "Çikolata agarda kültür ve antibiyogram"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Treponema pallidum", "isMasked": False},
                                {"text": "Lezyondan PCR veya Karanlık Saha", "isMasked": True, "hint": "direkt mikroskopi veya DNA testi"},
                                {"text": "VDRL, RPR serolojik antikor testleri"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "NAAT ile Hızlı ve Doğru Tanı Akışı",
                    "steps": [
                        "1. Sürüntü Alınması: Serviks veya vulvar lezyondan pamuklu eküvyonla sürüntü toplanır.",
                        "2. DNA Ekstraksiyonu: Örnekteki bakteriyel nükleik asitler lizis solüsyonu ile açığa çıkarılır.",
                        "3. Polimeraz Zincir Reaksiyonu: Hedef patojen geni milyonlarca kat amplifiye edilir.",
                        "4. Hızlı Sonuç: Saatler içinde etkenin DNA'sı tespit edilerek hedefe yönelik tedavi başlanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Treponema pallidum'un mikrobiyolojik kültürünün yapılamamasının nedeni nedir ve tanıda hangi doğrudan yöntemler kullanılır?",
                    "answer": "Bakteri yapay cansız besiyerlerinde üretilemez; doğrudan tanıda lezyon eksüdasından karanlık saha mikroskopisi veya NAAT/PCR DNA testi kullanılır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Genital Enfeksiyonlarda NAAT ve Moleküler Tanı",
                    "items": [
                        {"text": "NAAT nükleik asit amplifikasyonuyla çalışan yüksek duyarlıklı bir testtir.", "isLie": False, "explanation": "Doğru. PCR prensibine dayanır."},
                        {"text": "N. gonorrhoeae tanısında NAAT kültürden daha yüksek duyarlılık sunar.", "isLie": False, "explanation": "Doğru. Hızlı ve hassastır."},
                        {"text": "T. pallidum yapay besiyerinde üretilemediğinden moleküler testler değerlidir.", "isLie": False, "explanation": "Doğru. Rutin besiyerinde üremez."},
                        {"text": "NAAT testi sadece hastanın ayakkabı numarasını ölçen mekanik bir cetveldir.", "isLie": True, "explanation": "Tuzak! NAAT nükleik asit amplifikasyonu yapan moleküler biyolojik bir laboratuvar testidir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Alt genital sistem enfeksiyonlarında Nükleik Asit Amplifikasyon Testlerinin (NAAT) sağladığı en büyük klinik avantaj nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Üretilmesi güç veya imkansız mikroorganizmaların DNA'sını çoğaltarak son derece yüksek duyarlılıkla erken tanı sağlaması",
                            "isCorrect": True,
                            "explanation": "NAAT çok düşük sayıdaki patojen DNA'sını çoğaltarak yüksek özgüllük ve duyarlılıkla tanı koydurur."
                        },
                        {
                            "key": "B",
                            "text": "Hastanın kan grubunu göz rengine göre tahmin etmesi",
                            "isCorrect": False,
                            "explanation": "Biyolojik bir mantığı yoktur."
                        },
                        {
                            "key": "C",
                            "text": "Herhangi bir test yapmaksızın tüm hastaları sağlıklı kabul etmesi",
                            "isCorrect": False,
                            "explanation": "Laboratuvar doğrulama testidir."
                        },
                        {
                            "key": "D",
                            "text": "Sadece kemik kırıklarını alçıya almak için kullanılması",
                            "isCorrect": False,
                            "explanation": "Ortopedik alçı ile ilgisi yoktur."
                        }
                    ]
                }
            ]
        },
        # S55
        {
            "slideNumber": 55,
            "title": "Herpes Simplex Virüs (HSV): Tzanck Yayması ve Multinükleer Dev Hücreler",
            "subtitle": "Kromatin marjinasyonu, buzlu cam nükleus ve Cowdry A inklüzyonları",
            "clinicalFocus": "Viral Sitoloji ve Histoloji",
            "content": "Herpes Simplex Virus (özellikle **HSV-2** ve daha az sıklıkla HSV-1), vulva, vajen ve servikste son derece ağrılı vezikülo-ülseratif lezyonlara yol açan yaygın bir genital enfeksiyon etkenidir.\n\n- **Tzanck Yayması:** Vezikül tabanından kazınarak lam üzerine yayılan eksüdanın Giemsa veya Wright ile boyanmasıyla uygulanan klasik, hızlı bir sitolojik tanı yöntemidir.\n- **3M Viral Sitopatik Kriteri:** Mikroskopide multinükleasyon (Multinucleation), kromatinin kenara itilmesi (Margination) ve nükleusta homojen buzlu cam görünümü (Molding) izlenir.\n- **Histopatoloji:** Epidermal hücrelerin füzyonuyla oluşan **multinükleer dev hücreler** ve eozinofilik nükleer inklüzyon cisimcikleri (**Cowdry A inklüzyonları**) patognomoniktir. Hücreler intraepitelyal veziküller içinde akantolizise uğrayarak dökülür.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Tzanck yaymasında multinükleer dev hücreler, nükleer kromatin marjinasyonu ve Cowdry A tipi nükleer inklüzyonlar HSV enfeksiyonunun ayırt edici sitopatolojik bulgularıdır.",
            "synthesisNarrative": "Herpes Simplex Virus (özellikle **HSV-2** ve daha az sıklıkla HSV-1), vulva, vajen ve servikste son derece ağrılı vezikülo-ülseratif lezyonlara yol açan yaygın bir genital enfeksiyon etkenidir.\n\n- **Tzanck Yayması:** Vezikül tabanından kazınarak lam üzerine yayılan eksüdanın Giemsa veya Wright ile boyanmasıyla uygulanan klasik, hızlı bir sitolojik tanı yöntemidir.\n- **3M Viral Sitopatik Kriteri:** Mikroskopide multinükleasyon (Multinucleation), kromatinin kenara itilmesi (Margination) ve nükleusta homojen buzlu cam görünümü (Molding) izlenir.\n- **Histopatoloji:** Epidermal hücrelerin füzyonuyla oluşan **multinükleer dev hücreler** ve eozinofilik nükleer inklüzyon cisimcikleri (**Cowdry A inklüzyonları**) patognomoniktir. Hücreler intraepitelyal veziküller içinde akantolizise uğrayarak dökülür.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Tzanck yaymasında multinükleer dev hücreler, nükleer kromatin marjinasyonu ve Cowdry A tipi nükleer inklüzyonlar HSV enfeksiyonunun ayırt edici sitopatolojik bulgularıdır.",
            "bulletPoints": [
                "HSV vulvada son derece ağrılı vezikül ve ülserler yapar.",
                "Tzanck yaymasında multinükleer dev hücreler tanı koydurucudur.",
                "Cowdry A nükleer inklüzyonları ve kromatin marjinasyonu karakteristiktir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Genital herpes tanısında vezikül tabanından yapılan Tzanck yaymasında multinükleer dev hücreler saptanır.",
                    "maskedTerm": "multinükleer dev hücreler",
                    "hint": "Birbirine yapışmış çok sayıda çekirdek içeren büyük hücreler"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "HSV'nin Sitopatolojik Karakteristikleri",
                    "tableHeaders": ["Bulgu", "Hücresel Görünüm", "Tanısal Değer"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Multinükleasyon", "isMasked": False},
                                {"text": "Hücre füzyonuyla çok çekirdekli dev hücreler", "isMasked": True, "hint": "kaynaşmış birden fazla nükleus"},
                                {"text": "Tzanck yaymasında anahtar tanı kriteri"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Cowdry A İnklüzyonu", "isMasked": False},
                                {"text": "Eozinofilik nükleer viral inklüzyon", "isMasked": True, "hint": "çekirdek içi pembe cisimcik"},
                                {"text": "Herpesviridae ailesine özgül histolojik bulgu"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "HSV Enfeksiyonundan Tzanck Bulgusuna",
                    "steps": [
                        "1. İnokülasyon: HSV-2 vulva skuamöz epiteline penetre olarak replike olur.",
                        "2. Akantoliz ve Vezikül: İntraselüler ödem ve hücre ayrışması ağrılı intraepitelyal veziküller yapar.",
                        "3. Hücresel Füzyon: Enfekte hücre membranları birleşerek multinükleer dev hücreleri üretir.",
                        "4. Tzanck Yayması: Vezikül tabanından alınan sürüntüde çok çekirdekli hücreler mikroskopta teşhis edilir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Genital veziküler lezyonun tabanından yapılan Tzanck yaymasında HSV tanısını doğrulayan karakteristik mikroskobik bulgu nedir?",
                    "answer": "Multinükleer dev hücreler, nükleer kromatin marjinasyonu (buzlu cam nükleus) ve Cowdry A eozinofilik nükleer inklüzyon cisimcikleridir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "HSV ve Tzanck Yayması",
                    "items": [
                        {"text": "HSV ağrılı vezikülo-ülseratif lezyonlarla seyreder.", "isLie": False, "explanation": "Doğru. Tipik klinik tablodur."},
                        {"text": "Tzanck yaymasında multinükleer dev hücreler izlenir.", "isLie": False, "explanation": "Doğru. Patognomonik sitolojik bulgudur."},
                        {"text": "Cowdry A inklüzyon cisimcikleri HSV histopatolojisinde tipiktir.", "isLie": False, "explanation": "Doğru. Eozinofilik nükleer inklüzyondur."},
                        {"text": "Tzanck yayması kemik kırıklarının iyileşme hızını ölçen bir radyoloji cihazıdır.", "isLie": True, "explanation": "Tuzak! Tzanck yayması vezikül sıvısından yapılan bir sitolojik yayma testidir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvada ağrılı vezikülleri olan bir hastada vezikül tabanından hazırlanan Tzanck yaymasında aşağıdaki bulgulardan hangisinin görülmesi HSV enfeksiyonunu destekler?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Multinükleer dev hücreler ve buzlu cam görünümlü çekirdekler",
                            "isCorrect": True,
                            "explanation": "Tzanck yaymasında multinükleer dev hücreler ve viral sitopatik nükleer değişiklikler HSV'nin klasik bulgusudur."
                        },
                        {
                            "key": "B",
                            "text": "Konsantrik lameller oluşturan dev kalsiyum fosfat taşları",
                            "isCorrect": False,
                            "explanation": "Böbrek taşı veya psammom cismi bulgusudur."
                        },
                        {
                            "key": "C",
                            "text": "Sadece saf hyalin kıkırdak kondrositleri",
                            "isCorrect": False,
                            "explanation": "Kıkırdak dokusu histolojisidir."
                        },
                        {
                            "key": "D",
                            "text": "Hiçbir hücre içermeyen tamamen boş saf zeytinyağı damlacıkları",
                            "isCorrect": False,
                            "explanation": "Tıbbi sitoloji bulgusu değildir."
                        }
                    ]
                }
            ]
        },
        # S56
        {
            "slideNumber": 56,
            "title": "Sifiliz Serolojisi ve Vulvar Şankr Ayırıcı Tanısı",
            "subtitle": "Ağrısız sert şankr, Treponema pallidum ve VDRL / RPR testleri",
            "clinicalFocus": "Treponema pallidum ve Ayırıcı Tanı",
            "content": "Treponema pallidum enfeksiyonu (sifiliz), genital bölgede oluşturduğu lezyonlarla vulvit ve genital ülser ayırıcı tanısında kritik yer tutar.\n\n- **Primer Sifiliz (Sert Şankr):** Bakterinin inokülasyon yerinde (vulva labiumları veya serviks) ağrısız, tabanı temiz, kenarları belirgin ve sert (indüre) tek bir ülser şeklinde belirir. Ağrılı ve veziküler olan HSV lezyonlarından **ağrısız ve sert olmasıyla** kesin olarak ayrılır.\n- **Histopatoloji:** Şankr zemininde yoğun plazma hücresi infiltrasyonu ve endotelyal proliferasyonla karakterize **obliteratif endarterit** tablosu izlenir.\n- **Serolojik Tanı:** Non-treponemal testler (**VDRL, RPR**) tarama ve tedavi takibinde kullanılırken; treponemal testler (**TPHA, FTA-ABS**) tanıyı doğrulamak için başvurulan spesifik antikor yöntemleridir.\n\n> [!NOTE]\n> [SINAV SPOTU] Primer sifiliz ülseri (şankr) sert ve ağrısızdır; mikroskopisinde plazma hücrelerinden zengin infiltrat ve obliteratif endarterit patognomoniktir.",
            "synthesisNarrative": "Treponema pallidum enfeksiyonu (sifiliz), genital bölgede oluşturduğu lezyonlarla vulvit ve genital ülser ayırıcı tanısında kritik yer tutar.\n\n- **Primer Sifiliz (Sert Şankr):** Bakterinin inokülasyon yerinde (vulva labiumları veya serviks) ağrısız, tabanı temiz, kenarları belirgin ve sert (indüre) tek bir ülser şeklinde belirir. Ağrılı ve veziküler olan HSV lezyonlarından **ağrısız ve sert olmasıyla** kesin olarak ayrılır.\n- **Histopatoloji:** Şankr zemininde yoğun plazma hücresi infiltrasyonu ve endotelyal proliferasyonla karakterize **obliteratif endarterit** tablosu izlenir.\n- **Serolojik Tanı:** Non-treponemal testler (**VDRL, RPR**) tarama ve tedavi takibinde kullanılırken; treponemal testler (**TPHA, FTA-ABS**) tanıyı doğrulamak için başvurulan spesifik antikor yöntemleridir.\n\n> [!NOTE]\n> [SINAV SPOTU] Primer sifiliz ülseri (şankr) sert ve ağrısızdır; mikroskopisinde plazma hücrelerinden zengin infiltrat ve obliteratif endarterit patognomoniktir.",
            "bulletPoints": [
                "Primer sifiliz sert, tabanı temiz ve ağrısız şankr ile seyreder.",
                "Histolojisinde plazma hücreleri ve obliteratif endarterit tipiktir.",
                "Serolojide VDRL/RPR taramada, TPHA/FTA-ABS doğrulamada kullanılır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Primer sifilizin vulvadaki karakteristik lezyonu ağrısız ve sert tabanlı sert şankr lezyonudur.",
                    "maskedTerm": "sert şankr",
                    "hint": "Treponema pallidum inokülasyon yerindeki indüre primer ülser"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Genital Ülser Ayırıcı Tanısı: HSV vs Primer Sifiliz",
                    "tableHeaders": ["Özellik", "Genital Herpes (HSV)", "Primer Sifiliz (T. pallidum)"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Ağrı Durumu", "isMasked": False},
                                {"text": "Şiddetli derecede ağrılı", "isMasked": False},
                                {"text": "Karakteristik olarak ağrısız", "isMasked": True, "hint": "hastanın acı hissetmediği sert lezyon"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Lezyon Yapısı", "isMasked": False},
                                {"text": "Gruplaşmış veziküller ve yüzeyel ülserler", "isMasked": False},
                                {"text": "Tek, sert tabanlı, temiz kenarlı şankr", "isMasked": True, "hint": "indüre soliter ülser"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Treponema İnokülasyonundan Şankra Patogenez",
                    "steps": [
                        "1. Mukoza Girişi: Treponema pallidum mikroskobik çatlaklardan vulva dokusuna girer.",
                        "2. Obliteratif Endarterit: Küçük damarlarda endotel şişmesi ve perivasküler plazma hücresi toplanır.",
                        "3. Doku İskemisi: Damar tıkanıklığı odak noktasında doku nekrozuna ve sert şankr oluşumuna yol açar.",
                        "4. Serokonversiyon: Haftalar içinde kanda VDRL ve TPHA antikorları pozitifleşir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Primer sifiliz şankrını genital herpes (HSV) ülserlerinden ayıran en temel iki klinik özellik nedir?",
                    "answer": "Şankrın ağrısız olması ve tabanının sert (indüre) olmasıdır (HSV ise şiddetli ağrılı ve yumuşaktır)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Sifiliz ve Vulvar Şankr",
                    "items": [
                        {"text": "Primer sifiliz lezyonu olan sert şankr tipik olarak ağrısızdır.", "isLie": False, "explanation": "Doğru. Ağrısız olması ayırt edicidir."},
                        {"text": "Histopatolojide plazma hücresi infiltrasyonu ve obliteratif endarterit izlenir.", "isLie": False, "explanation": "Doğru. Tipik vasküler tablodur."},
                        {"text": "VDRL ve RPR non-treponemal serolojik testlerdir.", "isLie": False, "explanation": "Doğru. Taramada ve takipte kullanılır."},
                        {"text": "Sifiliz mikrobu yalnızca saf su içmekle bulaşan bir mantar sporudur.", "isLie": True, "explanation": "Tuzak! Sifiliz cinsel temasla bulaşan Treponema pallidum adlı spiroket bakterisidir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Vulvada tek, tabanı temiz, sert kenarlı ve tamamen ağrısız bir ülser saptanan hastada en olası tanı ve bu lezyonun histopatolojik bulgusu nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Primer sifiliz (sert şankr); plazma hücrelerinden zengin infiltrat ve obliteratif endarterit",
                            "isCorrect": True,
                            "explanation": "Ağrısız sert ülser primer sifiliz şankrıdır; histolojide plazma hücreleri ve endarterit karakteristiktir."
                        },
                        {
                            "key": "B",
                            "text": "Akut apandisit perforasyonu; nötrofilik cerahat",
                            "isCorrect": False,
                            "explanation": "Batın içi cerrahi tablodur, genital ülser yapmaz."
                        },
                        {
                            "key": "C",
                            "text": "Göz içi glokom krizi; optik sinir çukurlaşması",
                            "isCorrect": False,
                            "explanation": "Göz hastalığıdır."
                        },
                        {
                            "key": "D",
                            "text": "Deri melanomu; melanin yüklü nöronlar",
                            "isCorrect": False,
                            "explanation": "Sert ağrısız şankr tablosunu açıklamaz."
                        }
                    ]
                }
            ]
        },
        # S57
        {
            "slideNumber": 57,
            "title": "Pelvik İnflamatuar Hastalık (PİH) ile İlişki ve Asendan Yayılım",
            "subtitle": "Servisitten endometrit, salpenjit ve tuboovaryen apseye tırmanış",
            "clinicalFocus": "Asendan Enfeksiyon ve Komplikasyonlar",
            "content": "Servikal kanalda başlayan enfeksiyonlar yerinde sınırlı kalmayıp üst genital yollara doğru yayılarak **Pelvik İnflamatuar Hastalık (PİH)** tablosuna neden olabilir.\n\n- **Temel Etkenler:** Başta **Neisseria gonorrhoeae** ve Chlamydia trachomatis olmak üzere, alt genital sistemden asendan yolla yukarı tırmanan bakteriyel ajanlar sorumludur.\n- **Asendan Yayılım Basamakları:** Mikroorganizmalar endoservikal bariyeri aşarak sırasıyla endometriyumu (**endometrit**), fallop tüplerini (**salpenjit**) ve overleri tutarak **tuboovaryen apse** oluşturur. Peritona sızması pelviperitonit ile sonuçlanır.\n- **Geç Komplikasyonlar:** Akut inflamasyon iyileşirken fallop tüplerinde fibrozis ve lümen tıkanıklığı bırakır. Bu durum hastada **ektopik gebelik (dış gebelik)**, kronik pelvik ağrı ve **tubal infertilite (kısırlık)** riskini katbekat artırır.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Tedavi edilmemiş servikal gonokok ve klamidya enfeksiyonlarının en korkulan uzun vadeli sekeli, bilateral salpenjit ve tubal fibrozise bağlı infertilite ve dış gebeliktir.",
            "synthesisNarrative": "Servikal kanalda başlayan enfeksiyonlar yerinde sınırlı kalmayıp üst genital yollara doğru yayılarak **Pelvik İnflamatuar Hastalık (PİH)** tablosuna neden olabilir.\n\n- **Temel Etkenler:** Başta **Neisseria gonorrhoeae** ve Chlamydia trachomatis olmak üzere, alt genital sistemden asendan yolla yukarı tırmanan bakteriyel ajanlar sorumludur.\n- **Asendan Yayılım Basamakları:** Mikroorganizmalar endoservikal bariyeri aşarak sırasıyla endometriyumu (**endometrit**), fallop tüplerini (**salpenjit**) ve overleri tutarak **tuboovaryen apse** oluşturur. Peritona sızması pelviperitonit ile sonuçlanır.\n- **Geç Komplikasyonlar:** Akut inflamasyon iyileşirken fallop tüplerinde fibrozis ve lümen tıkanıklığı bırakır. Bu durum hastada **ektopik gebelik (dış gebelik)**, kronik pelvik ağrı ve **tubal infertilite (kısırlık)** riskini katbekat artırır.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Tedavi edilmemiş servikal gonokok ve klamidya enfeksiyonlarının en korkulan uzun vadeli sekeli, bilateral salpenjit ve tubal fibrozise bağlı infertilite ve dış gebeliktir.",
            "bulletPoints": [
                "N. gonorrhoeae serviksten üst genital yola asendan yayılır.",
                "Endometrit, salpenjit ve tuboovaryen apseye yol açabilir.",
                "Tubal tıkanıklık infertilite ve dış gebelik riskini artırır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "PİH tablosunda fallop tüplerinde gelişen inflamasyon ve lümen tıkanıklığı tüp kaynaklı infertilite komplikasyonuna yol açar.",
                    "maskedTerm": "infertilite",
                    "hint": "Tubal faktöre bağlı kısırlık tablosu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "PİH Asendan Yayılım Evreleri",
                    "tableHeaders": ["Anatomik Düzey", "İnflamatuar Tablo", "Olası Sekel / Risk"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Serviks Kanalı", "isMasked": False},
                                {"text": "Akut / Kronik Mukopürülan Servisit", "isMasked": False},
                                {"text": "Yukarı yayılım için odak oluşturma", "isMasked": True, "hint": "enfeksiyonun tırmanma başlangıcı"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Fallop Tüpleri", "isMasked": False},
                                {"text": "Akut Pürülan Salpenjit", "isMasked": True, "hint": "tüp iltihaplanması"},
                                {"text": "Lümen yapışıklığı, dış gebelik ve kısırlık"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Servisitten Tubal İnfertiliteye Asendan Zincir",
                    "steps": [
                        "1. Servisit: Gonokoklar endoservikal kolumnar epitele tutunarak pürülan akıntı yapar.",
                        "2. Asendan İlerleme: Bakteriler servikal bariyeri aşarak endometriyal kaviteden tüplere geçer.",
                        "3. Salpenjit: Fallop tüpü plikalarında masif süpürasyon ve püy birikimi (piyosalpenks) oluşur.",
                        "4. Fibröz Tıkanma: İyileşme sürecinde tüp lümeni yapışır; ovum geçişi engellenerek kısırlık gelişir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Servisitten kaynaklanan asendan pelvik enfeksiyonların (PİH) fallop tüplerinde yol açtığı en önemli iki uzun vadeli klinik sekel nedir?",
                    "answer": "Tubal infertilite (kısırlık) ve ektopik gebelik (dış gebelik) riskinde belirgin artıştır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Pelvik İnflamatuar Hastalık ve Asendan Yayılım",
                    "items": [
                        {"text": "PİH sıklıkla N. gonorrhoeae ve C. trachomatis'in asendan yayılımıyla gelişir.", "isLie": False, "explanation": "Doğru. En sık etkenlerdir."},
                        {"text": "Salpenjit fallop tüplerinde iltihaplanma ve püy birikimiyle seyreder.", "isLie": False, "explanation": "Doğru. Tüp tutulumu esastır."},
                        {"text": "PİH sonrası gelişen tubal skarlaşma infertilite ve dış gebeliğe zemin hazırlar.", "isLie": False, "explanation": "Doğru. Klasik uzun dönem sekellerdir."},
                        {"text": "PİH enfeksiyonu geçiren kadınlarda fallop tüpleri kendi kendine titanyum boruya dönüşür.", "isLie": True, "explanation": "Tuzak! Tüpler titanyum boru olmaz; fibröz yapışıklık ve skar dokusu ile tıkanır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Tedavi edilmeyen mukopürülan servisit olgularında mikroorganizmaların asendan yayılımı sonucu ortaya çıkan komplikasyonlarla ilgili hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Salpenjit ve tuboovaryen apse yaparak tüplerde skarlaşma, kısırlık ve dış gebeliğe neden olabilir",
                            "isCorrect": True,
                            "explanation": "Asendan pelvik yayılım tubal skarlaşmaya, kısırlığa ve ektopik gebeliğe zemin hazırlar."
                        },
                        {
                            "key": "B",
                            "text": "Sadece ayak başparmağında nasır oluşturarak sonlanır",
                            "isCorrect": False,
                            "explanation": "Üst genital traktus enfeksiyonudur."
                        },
                        {
                            "key": "C",
                            "text": "Over ve fallop tüplerini kansere karşı %100 bağışık hale getirir",
                            "isCorrect": False,
                            "explanation": "Kanser bağışıklığı sağlamaz, ağır inflamatuvar hasar bırakır."
                        },
                        {
                            "key": "D",
                            "text": "Hiçbir zaman uterus kavitesine veya tüplere ulaşamaz",
                            "isCorrect": False,
                            "explanation": "PİH'in temel patofizyolojisi asendan tırmanıştır."
                        }
                    ]
                }
            ]
        },
        # S58
        {
            "slideNumber": 58,
            "title": "Kronik Servisit Komplikasyonları: Doku Yenilenmesi ve Skar",
            "subtitle": "Mukozal erezyon, ektropiyon, granülasyon dokusu ve lökore",
            "clinicalFocus": "Kronik İnflamasyon ve Komplikasyonlar",
            "content": "Serviksin uzun süreli veya tekrarlayan enfeksiyonları **kronik servisit** tablosuna yol açar. Kronik servisit klinik pratikte son derece yaygın olup kadınların büyük kısmında bir dereceye kadar mevcuttur.\n\n- **Histolojik Bulgular:** Mukozada lenfositler, plazma hücreleri ve histiyositlerden oluşan mononükleer inflamatuar infiltrat görülür. Yüzey epitelinde tekrarlayan ülserasyon, soyulma (erozyon) ve granülasyon dokusu oluşumu eşlik eder.\n- **Ektropiyon (Servikal Erozyon):** Endoservikal narin kolumnar epitelin ektoservikse doğru taşması ve asidik vajinal ortama maruz kalarak kırmızı, kanamalı, granüler bir alan oluşturmasıdır. Sık sık postkoital kanama ve inatçı vajinal akıntıya (lökore) yol açar.\n- **Kanal Darlığı:** Kronik derin inflamasyonun iyileşme evresinde gelişen fibrozis, nadiren endoservikal kanal darlığına (servikal stenoz) ve mukus drenaj bozukluğuna sebep olabilir.\n\n> [!NOTE]\n> Kronik servisit zemininde gelişen skuamöz metaplazi, fizyolojik transformasyon zonunu genişleterek HPV enfeksiyonuna duyarlı hücre havuzunu artırabilir.",
            "synthesisNarrative": "Serviksin uzun süreli veya tekrarlayan enfeksiyonları **kronik servisit** tablosuna yol açar. Kronik servisit klinik pratikte son derece yaygın olup kadınların büyük kısmında bir dereceye kadar mevcuttur.\n\n- **Histolojik Bulgular:** Mukozada lenfositler, plazma hücreleri ve histiyositlerden oluşan mononükleer inflamatuar infiltrat görülür. Yüzey epitelinde tekrarlayan ülserasyon, soyulma (erozyon) ve granülasyon dokusu oluşumu eşlik eder.\n- **Ektropiyon (Servikal Erozyon):** Endoservikal narin kolumnar epitelin ektoservikse doğru taşması ve asidik vajinal ortama maruz kalarak kırmızı, kanamalı, granüler bir alan oluşturmasıdır. Sık sık postkoital kanama ve inatçı vajinal akıntıya (lökore) yol açar.\n- **Kanal Darlığı:** Kronik derin inflamasyonun iyileşme evresinde gelişen fibrozis, nadiren endoservikal kanal darlığına (servikal stenoz) ve mukus drenaj bozukluğuna sebep olabilir.\n\n> [!NOTE]\n> Kronik servisit zemininde gelişen skuamöz metaplazi, fizyolojik transformasyon zonunu genişleterek HPV enfeksiyonuna duyarlı hücre havuzunu artırabilir.",
            "bulletPoints": [
                "Kronik servisitte lenfosit ve plazma hücre infiltrasyonu izlenir.",
                "Ektropiyon kırmızı, granüler ve kolay kanayan erozyon görüntüsü verir.",
                "Fibrotik iyileşme nadiren servikal stenoza yol açabilir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Endoservikal kolumnar epitelin dışa taşmasıyla oluşan kırmızı granüler alana ektropiyon adı verilir.",
                    "maskedTerm": "ektropiyon",
                    "hint": "Servikal erozyon olarak da bilinen mukozal eversiyon"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Kronik Servisitin Morfolojik Özellikleri",
                    "tableHeaders": ["Bileşen", "Patolojik Bulgu", "Klinik Yansıma"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "İnflamatuar İnfiltrat", "isMasked": False},
                                {"text": "Lenfositler ve plazma hücreleri", "isMasked": True, "hint": "mononükleer yangı hücreleri"},
                                {"text": "Dokuda kronik yangısal hasar"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Mukozal Yüzey", "isMasked": False},
                                {"text": "Erozyon, ektropiyon ve skuamöz metaplazi", "isMasked": True, "hint": "kolumnar epitel eversiyonu ve onarım"},
                                {"text": "Postkoital kanama ve kronik akıntı (lökore)"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Kronik Servisitten Ektropiyona Morfolojik Süreç",
                    "steps": [
                        "1. Yangısal Uyarım: Servikal stroma sürekli mikroorganizma ve travmaya maruz kalır.",
                        "2. Vasküler Proliferasyon: Dokuda konjesyon ve granülasyon dokusu şekillenir.",
                        "3. Kolumnar Eversion: Endoservikal glandüler epitel ektoservikse doğru yer değiştirir (ektropiyon).",
                        "4. Metaplastik Yanıt: Vajina asiditesi nedeniyle kolumnar hücrelerin yerini metaplastik yassı epitel alır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Kronik servisitte narin endoservikal kolumnar epitelin dışa doğru taşarak asidik vajen ortamında kırmızı ve kanamalı görünmesine ne ad verilir?",
                    "answer": "Ektropiyon (servikal erozyon); sıklıkla postkoital temas kanaması ve lökoreye neden olur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Kronik Servisit Komplikasyonları",
                    "items": [
                        {"text": "Kronik servisitte stromada lenfosit ve plazma hücreleri hakimdir.", "isLie": False, "explanation": "Doğru. Mononükleer kronik yangı tablosudur."},
                        {"text": "Ektropiyon kırmızı, kolay kanayan granüler bir alan şeklinde izlenir.", "isLie": False, "explanation": "Doğru. Kolumnar epitelin dışa taşmasıdır."},
                        {"text": "Kronik inflamasyon skuamöz metaplazi gelişimini tetikleyebilir.", "isLie": False, "explanation": "Doğru. Asit ortam metaplaziyi başlatır."},
                        {"text": "Kronik servisit daima hastanın kalbinde aort diseksiyonuna yol açar.", "isLie": True, "explanation": "Tuzak! Kronik servisit servikse lokalize jinekolojik bir inflamasyondur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Kronik servisit ve ektropiyon ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Endoservikal kolumnar epitelin dışarı taşması (ektropiyon) kırmızı granüler görünüme ve postkoital kanamaya neden olabilir",
                            "isCorrect": True,
                            "explanation": "Ektropiyon mukozal eversiyon sonucu kanamalı ve granüler lezyon oluşturur."
                        },
                        {
                            "key": "B",
                            "text": "Kronik servisit yalnızca erkeklerde görülen bir karaciğer enfeksiyonudur",
                            "isCorrect": False,
                            "explanation": "Kadın serviksine ait bir durumdur."
                        },
                        {
                            "key": "C",
                            "text": "Stromada lenfosit veya plazma hücresi görülmesi kesinlikle imkansızdır",
                            "isCorrect": False,
                            "explanation": "Kronik yangının ana hücreleri lenfosit ve plazma hücreleridir."
                        },
                        {
                            "key": "D",
                            "text": "Ektropiyon görülen tüm kadınlarda acil kalp nakli yapılmalıdır",
                            "isCorrect": False,
                            "explanation": "Kalp patolojisi ile hiçbir ilgisi yoktur."
                        }
                    ]
                }
            ]
        },
        # S59
        {
            "slideNumber": 59,
            "title": "Naboth Kistlerinin Kolposkopik ve Ultrasonografik Bulguları",
            "subtitle": "Kanal tıkanıklığı, müsin retansiyonu ve selim papül morfolojisi",
            "clinicalFocus": "Benign Retansiyon Kistleri",
            "content": "Servikal muayenelerde ve ultrasonografide sıkça rastlanan **Naboth kistleri**, serviksin tamamen selim retansiyon kistleridir.\n\n- **Oluşum Mekanizması:** Transformasyon zonunda fizyolojik skuamöz metaplazi gelişirken, yüzeyi kaplayan yassı epitel altta kalan endoservikal bezlerin ağzını tıkar. Bezlerin lümeninde müsin salgısı birikmeye devam eder ve bez giderek kistik olarak genişler.\n- **Kolposkopik ve Makroskopik Görünüm:** Ektoserviks yüzeyinde birkaç milimetreden 1-2 cm'ye kadar ulaşabilen, düzgün yüzeyli, parlak, sarımsı-beyaz veya mavi-gri renkli, saydam kubbe şeklinde kistik kabarıklıklar şeklinde görülür. Üzerinden geçen ince damarlar normal seyreder.\n- **Ultrasonografik Özellik:** Pelvik ultrasonda serviks stroması içinde yuvarlak, anekoik (tamamen siyah), ince düzgün duvarlı ve arkasında akustik zenginleşme oluşturan tipik kistik yapılar olarak raporlanır.\n\n> [!NOTE]\n> Naboth kistleri neoplastik lezyonlar değildir; hiçbir malignite potansiyeli taşımazlar ve tedavi gerektirmezler.",
            "synthesisNarrative": "Servikal muayenelerde ve ultrasonografide sıkça rastlanan **Naboth kistleri**, serviksin tamamen selim retansiyon kistleridir.\n\n- **Oluşum Mekanizması:** Transformasyon zonunda fizyolojik skuamöz metaplazi gelişirken, yüzeyi kaplayan yassı epitel altta kalan endoservikal bezlerin ağzını tıkar. Bezlerin lümeninde müsin salgısı birikmeye devam eder ve bez giderek kistik olarak genişler.\n- **Kolposkopik ve Makroskopik Görünüm:** Ektoserviks yüzeyinde birkaç milimetreden 1-2 cm'ye kadar ulaşabilen, düzgün yüzeyli, parlak, sarımsı-beyaz veya mavi-gri renkli, saydam kubbe şeklinde kistik kabarıklıklar şeklinde görülür. Üzerinden geçen ince damarlar normal seyreder.\n- **Ultrasonografik Özellik:** Pelvik ultrasonda serviks stroması içinde yuvarlak, anekoik (tamamen siyah), ince düzgün duvarlı ve arkasında akustik zenginleşme oluşturan tipik kistik yapılar olarak raporlanır.\n\n> [!NOTE]\n> Naboth kistleri neoplastik lezyonlar değildir; hiçbir malignite potansiyeli taşımazlar ve tedavi gerektirmezler.",
            "bulletPoints": [
                "Naboth kistleri bez ağzının metaplastik epitelce tıkanmasıyla oluşur.",
                "Kolposkopide sarımsı-beyaz, parlak kubbe şeklinde kistlerdir.",
                "Pelvik ultrasonda ince duvarlı, anekoik selim retansiyon lezyonlarıdır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Endoservikal bez ağızlarının metaplastik yassı epitelce tıkanması sonucu müsin birikimiyle oluşan kistlere Naboth kistleri adı verilir.",
                    "maskedTerm": "Naboth kistleri",
                    "hint": "Serviksin tamamen selim müsinöz retansiyon kistleri"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Naboth Kistlerinin Tanısal Özellikleri",
                    "tableHeaders": ["Görüntüleme Yöntemi", "Morfolojik Görünüm", "Klinik Yorum"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Kolposkopi", "isMasked": False},
                                {"text": "Sarı-beyaz, düzgün yüzeyli kubbe şeklinde kistler", "isMasked": True, "hint": "parlak sarımsı kabarıklık"},
                                {"text": "Tamamen selim, müdahale gerektirmez"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Pelvik Ultrasonografi", "isMasked": False},
                                {"text": "Anekoik, arkasında akustik zenginleşme olan yuvarlak lezyon", "isMasked": True, "hint": "ultrasonda siyah sıvı dolu kist"},
                                {"text": "Karsinomla karıştırılmaması gereken benign bulgu"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Metaplaziden Naboth Kistine Gelişim Aşamaları",
                    "steps": [
                        "1. Skuamöz Metaplazi: Endoservikal gland açıklıkları üzerine doğru yassı epitel tabakası yayılır.",
                        "2. Kanal Orifisi Tıkanması: Metaplastik epitel bezin dışarıya açılan kanal ağzını tıkar.",
                        "3. Müsin Salgısının Hapsolması: Bez epitelinin ürettiği müsin kanaldan akamaz ve bez şişer.",
                        "4. Naboth Kisti: Stromada santimetrik boyutlara varabilen gergin müsinöz kist belirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Naboth kistlerinin temel oluşum mekanizması nedir ve kanserleşme riski taşır mı?",
                    "answer": "Skuamöz metaplazinin endoservikal bez ağızlarını tıkaması sonucu müsin retansiyonu ile oluşur; tamamen selimdir ve hiçbir kanserleşme riski taşımaz."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Naboth Kistleri",
                    "items": [
                        {"text": "Naboth kistleri metaplastik epitelin bez ağzını tıkamasıyla oluşur.", "isLie": False, "explanation": "Doğru. Klasik retansiyon mekanizmasıdır."},
                        {"text": "Ultrasonda anekoik, ince düzgün duvarlı kistler olarak izlenir.", "isLie": False, "explanation": "Doğru. Tipik kistik ekojenitedir."},
                        {"text": "Tamamen selim olup cerrahi tedavi gerektirmezler.", "isLie": False, "explanation": "Doğru. Malignite potansiyeli yoktur."},
                        {"text": "Naboth kistleri yüksek dereceli metastatik kemik tümörleridir.", "isLie": True, "explanation": "Tuzak! Naboth kistleri kemik tümörü değil, serviksin selim retansiyon kistleridir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servikal muayenede ve pelvik ultrasonda saptanan Naboth kistleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Endoservikal bez ağızlarının metaplaziyle tıkanması sonucu gelişen anekoik, selim müsinöz retansiyon kistleridir",
                            "isCorrect": True,
                            "explanation": "Naboth kistleri bez ağzı tıkanıklığına bağlı gelişen tamamen selim retansiyon kistleridir."
                        },
                        {
                            "key": "B",
                            "text": "Mutlaka radikal pelvik lenf nodu diseksiyonu ile temizlenmelidir",
                            "isCorrect": False,
                            "explanation": "Selim bir tablodur, cerrahi gerektirmez."
                        },
                        {
                            "key": "C",
                            "text": "Yalnızca menopoz sonrası erkeklerin testis dokusunda görülür",
                            "isCorrect": False,
                            "explanation": "Uterus serviksinde yer alır."
                        },
                        {
                            "key": "D",
                            "text": "İçinde daima canlı parazit kurtçukları barındıran enfeksiyöz kistlerdir",
                            "isCorrect": False,
                            "explanation": "İçeriği endoservikal hücrelerin salgıladığı steril müsindir."
                        }
                    ]
                }
            ]
        },
        # S60
        {
            "slideNumber": 60,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 6] Glandüler Servikal Lezyonlar, Polipler ve Enfeksiyon Tanısı",
            "subtitle": "Bölüm 6 kapsamındaki AIS, adenokarsinom, endoservikal polip, HSV, sifiliz ve Naboth kistleri konsolidasyonu",
            "clinicalFocus": "Kapsamlı Bölüm Tekrarı",
            "content": "Bölüm 6 boyunca serviksin glandüler neoplazilerini, selim polipoid kitlelerini ve alt genital enfeksiyonların ayırıcı tanı basamaklarını sentezledik.\n\n- **Glandüler Neoplaziler (AIS ve Adenokarsinom):** Kolumnar bez epitelinden köken alır; skuamöz tipten farklı olarak özellikle **HPV-18** ile güçlü birliktelik gösterir. Atlamalı lezyonlar nedeniyle cerrahi sınır değerlendirmesi zordur.\n- **Benign Lezyonlar:** Endoservikal polipler ödemli ve konjesyone damarlı benign kitlelerdir; Naboth kistleri ise metaplaziye bağlı müsin retansiyon kistleridir.\n- **Enfeksiyon Ayırıcı Tanısı:** HSV son derece ağrılı veziküller, Cowdry A inklüzyonları ve Tzanck'ta multinükleer dev hücreler yaparken; primer sifiliz ağrısız, sert şankr ve plazma hücreli endarterit ile seyreder.\n\n> [!IMPORTANT]\n> [CHECKPOINT SENTEZİ] Glandüler neoplazilerde (AIS/adenokarsinom) HPV-18 baskındır; Tzanck'ta multinükleer dev hücreler HSV'yi, ağrısız sert şankr ve plazma hücreli endarterit ise primer sifilizi gösterir.",
            "synthesisNarrative": "Bölüm 6 boyunca serviksin glandüler neoplazilerini, selim polipoid kitlelerini ve alt genital enfeksiyonların ayırıcı tanı basamaklarını sentezledik.\n\n- **Glandüler Neoplaziler (AIS ve Adenokarsinom):** Kolumnar bez epitelinden köken alır; skuamöz tipten farklı olarak özellikle **HPV-18** ile güçlü birliktelik gösterir. Atlamalı lezyonlar nedeniyle cerrahi sınır değerlendirmesi zordur.\n- **Benign Lezyonlar:** Endoservikal polipler ödemli ve konjesyone damarlı benign kitlelerdir; Naboth kistleri ise metaplaziye bağlı müsin retansiyon kistleridir.\n- **Enfeksiyon Ayırıcı Tanısı:** HSV son derece ağrılı veziküller, Cowdry A inklüzyonları ve Tzanck'ta multinükleer dev hücreler yaparken; primer sifiliz ağrısız, sert şankr ve plazma hücreli endarterit ile seyreder.\n\n> [!IMPORTANT]\n> [CHECKPOINT SENTEZİ] Glandüler neoplazilerde (AIS/adenokarsinom) HPV-18 baskındır; Tzanck'ta multinükleer dev hücreler HSV'yi, ağrısız sert şankr ve plazma hücreli endarterit ise primer sifilizi gösterir.",
            "bulletPoints": [
                "Servikal adenokarsinom ve AIS özellikle HPV-18 ile ilişkilidir.",
                "Endoservikal polip ve Naboth kistleri tamamen selim lezyonlardır.",
                "Ağrılı vezikülde Tzanck multinükleer hücreleri (HSV), ağrısız sert ülserde şankr (sifiliz) görülür."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Glandüler servikal neoplazi ve adenokarsinoma in situ gelişiminde baskın olan yüksek riskli suş HPV 18 virüsüdür.",
                    "maskedTerm": "HPV 18",
                    "hint": "Glandüler serviks karsinogenezinde öne çıkan tip"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bölüm 6 Karşılaştırmalı Tanı Matrisi",
                    "tableHeaders": ["Hastalık / Durum", "Anahtar Morfolojik Özellik", "Klinik Özellik / Biyolojik Risk"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Endoservikal AIS", "isMasked": False},
                                {"text": "Atipik bezler, psödostratifikasyon, apikal mitoz", "isMasked": True, "hint": "glandüler tam kat atipi"},
                                {"text": "HPV-18 ile ilişkili premalign glandüler lezyon"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Genital Herpes (HSV)", "isMasked": False},
                                {"text": "Multinükleer dev hücreler ve Cowdry A inklüzyonu", "isMasked": True, "hint": "Tzanck yayması bulgusu"},
                                {"text": "Şiddetli ağrılı vezikül ve ülserler"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Bölüm 6 Tanısal Akış Zinciri",
                    "steps": [
                        "1. Glandüler Neoplazi: HPV-18 kanalda AIS ve kribriform adenokarsinom başlatır.",
                        "2. Reaktif Polip/Kist: Yangı ve metaplazi endoservikal polip ve Naboth kisti doğurur.",
                        "3. Viral Sitopati: HSV veziküllerinde Tzanck multinükleer dev hücreleri yakalanır.",
                        "4. Bakteriyel Şankr: Treponema sert tabanlı ağrısız şankr ve plazma hücreli endarterit yapar."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bölüm 6 kapsamında incelenen patolojilerden servikal adenokarsinom ile güçlü ilişkili HPV tipi hangisidir ve primer sifiliz ülserinin HSV'den en temel farkı nedir?",
                    "answer": "HPV tip 18'dir; sifiliz ülseri sert ve karakteristiktir olarak ağrısızdır (HSV ise şiddetli ağrılı vezikülo-ülseratiftir)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Bölüm 6 Genel Tekrar",
                    "items": [
                        {"text": "Servikal glandüler neoplazilerde HPV-18 ilişkisi oldukça belirgindir.", "isLie": False, "explanation": "Doğru. Tipik viral ilişkidir."},
                        {"text": "Endoservikal polipler ve Naboth kistleri selim tablolardır.", "isLie": False, "explanation": "Doğru. Malignite potansiyeli taşımazlar."},
                        {"text": "Tzanck yaymasında multinükleer dev hücreler HSV için karakteristiktir.", "isLie": False, "explanation": "Doğru. Patognomonik sitolojidir."},
                        {"text": "Naboth kistleri tüm vücuda yayılan metastatik kötü huylu sarkomlardır.", "isLie": True, "explanation": "Tuzak! Naboth kistleri metaplaziye bağlı müsin birikimiyle oluşan tamamen selim retansiyon kistleridir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Bölüm 6'da incelenen konularla ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Servikal glandüler lezyonlarda HPV-18 ön plandadır; Tzanck yaymasında multinükleer dev hücreler HSV'yi düşündürür",
                            "isCorrect": True,
                            "explanation": "Bu sentez cümlesi glandüler neoplazi ve viral tanı özelliklerini eksiksiz özetler."
                        },
                        {
                            "key": "B",
                            "text": "Primer sifiliz ülseri daima şiddetli ağrılı ve su dolu yüzlerce vezikülden oluşur",
                            "isCorrect": False,
                            "explanation": "Sifiliz ülseri (şankr) karakteristiktir olarak ağrısızdır ve sert tabanlıdır."
                        },
                        {
                            "key": "C",
                            "text": "Endoservikal polipler tanı anında mutlaka tüm iç organları işgal eder",
                            "isCorrect": False,
                            "explanation": "Endoservikal polipler selim reaktif lezyonlardır."
                        },
                        {
                            "key": "D",
                            "text": "Naboth kistleri sadece kemik iliğinde kan hücresi üretmekle görevli bezlerdir",
                            "isCorrect": False,
                            "explanation": "Uterus serviksinde yer alan mukus retansiyon kistleridir."
                        }
                    ]
                }
            ]
        }
    ]
    return slides

if __name__ == '__main__':
    slides = get_s6_slides()
    print(f'Section 6 generated with {len(slides)} slides.')
