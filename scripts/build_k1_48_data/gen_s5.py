import json

def get_s5_slides():
    slides = [
        # S41
        {
            "slideNumber": 41,
            "title": "Servikal Sitoloji ve Pap Smear Taramasının Temel İlkeleri",
            "subtitle": "Eksfoliyatif sitoloji, transformasyon zonu örneklemesi ve mortalite düşüşü",
            "clinicalFocus": "Preinvaziv Tarama",
            "content": "Papanicolaou (Pap) smear testi, servikal kanserin öncü lezyonlarını invaziv karsinoma dönüşmeden yıllar önce yakalamayı hedefleyen modern tıbbın en başarılı eksfoliyatif sitoloji tarama yöntemidir.\n\n- **Biyolojik Dayanak:** Serviks mukozasındaki displastik ve neoplastik hücreler, hücreler arası bağlantılarını (dezmozomları) kaybederek yüzeyden dökülmeye (eksfoliasyona) normal hücrelere göre çok daha meyillidir.\n- **Örnekleme Alanı:** Smear fırçası ve spatülü ile özellikle **transformasyon zonu ve skuamokolumnar bileşke** 360 derece taranmalıdır. Çünkü skuamöz intraepitelyal lezyonların neredeyse tamamı bu metaplastik hatta başlar.\n- **Klinik Başarı:** Yaygın ve düzenli Pap smear tarama programları uygulanan toplumlarda invaziv serviks karsinomu insidansı ve ilişkili mortalite oranları %70'ten fazla gerilemiştir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Pap smear bir eksfoliyatif sitoloji yöntemidir; yeterli bir yaymada transformasyon zonunu temsil eden metaplastik veya endoservikal hücrelerin bulunması zorunludur.",
            "synthesisNarrative": "Papanicolaou (Pap) smear testi, servikal kanserin öncü lezyonlarını invaziv karsinoma dönüşmeden yıllar önce yakalamayı hedefleyen modern tıbbın en başarılı eksfoliyatif sitoloji tarama yöntemidir.\n\n- **Biyolojik Dayanak:** Serviks mukozasındaki displastik ve neoplastik hücreler, hücreler arası bağlantılarını (dezmozomları) kaybederek yüzeyden dökülmeye (eksfoliasyona) normal hücrelere göre çok daha meyillidir.\n- **Örnekleme Alanı:** Smear fırçası ve spatülü ile özellikle **transformasyon zonu ve skuamokolumnar bileşke** 360 derece taranmalıdır. Çünkü skuamöz intraepitelyal lezyonların neredeyse tamamı bu metaplastik hatta başlar.\n- **Klinik Başarı:** Yaygın ve düzenli Pap smear tarama programları uygulanan toplumlarda invaziv serviks karsinomu insidansı ve ilişkili mortalite oranları %70'ten fazla gerilemiştir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Pap smear bir eksfoliyatif sitoloji yöntemidir; yeterli bir yaymada transformasyon zonunu temsil eden metaplastik veya endoservikal hücrelerin bulunması zorunludur.",
            "bulletPoints": [
                "Pap smear en başarılı eksfoliyatif sitoloji tarama testidir.",
                "Displastik epitel hücrelerinin kolay dökülme özelliğine dayanır.",
                "Transformasyon zonundan örnekleme yapılması zorunludur."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Pap smear tarama testinin başarısı transformasyon zonu bölgesinden eksfoliye olan hücrelerin incelenmesine dayanır.",
                    "maskedTerm": "transformasyon zonu",
                    "hint": "Ektoserviks ile endoserviks arasındaki metaplazi sahası"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Pap Smear Taramasının Temel Karakteristikleri",
                    "tableHeaders": ["Özellik", "Açıklama", "Klinik Önemi"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Yöntem Türü", "isMasked": False},
                                {"text": "Eksfoliyatif sitoloji", "isMasked": True, "hint": "dökülen hücrelerin incelenmesi"},
                                {"text": "Girişimsel olmayan, hızlı tarama sağlar"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Hedef Bölge", "isMasked": False},
                                {"text": "Skuamokolumnar bileşke / Transformasyon zonu", "isMasked": False},
                                {"text": "Karsinogenezin başladığı metaplastik odak", "isMasked": True, "hint": "neoplazilerin tetiklendiği sınır zonu"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Pap Smear ile Kanserden Korunma Zinciri",
                    "steps": [
                        "1. Örnekleme: Transformasyon zonundan spatül veya fırça yardımıyla hücreler toplanır.",
                        "2. Fiksasyon ve Boyama: Hücreler cama yayılıp Papanicolaou boyası ile sitolojik olarak renklendirilir.",
                        "3. Mikroskopi: Nükleus atipisi, koilositoz veya hiperkromazi gösteren dökülmüş hücreler taranır.",
                        "4. Erken Girişim: İnvazyon gelişmeden preinvaziv displazi evresinde lezyon tedavi edilerek kanser önlenir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Pap smear testinde dökülen hücrelerin incelenmesine dayanan hücresel prensibe ne ad verilir?",
                    "answer": "Eksfoliyatif sitoloji; kohezyonunu yitirmiş atipik hücrelerin yüzeyden kolayca dökülmesi prensibidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Pap Smear Taraması İlkeleri",
                    "items": [
                        {"text": "Pap smear eksfoliyatif sitoloji prensibiyle çalışan bir tarama testidir.", "isLie": False, "explanation": "Doğru. Dökülen epitel hücreleri taranır."},
                        {"text": "Örnekleme mutlaka skuamokolumnar bileşke ve transformasyon zonunu içermelidir.", "isLie": False, "explanation": "Doğru. Neoplaziler bu zondan köken alır."},
                        {"text": "Düzenli tarama programları serviks kanseri mortalitesini belirgin biçimde azaltmıştır.", "isLie": False, "explanation": "Doğru. Mortaliteyi %70'ten fazla düşürmüştür."},
                        {"text": "Pap smear için mutlaka hastaya genel anestezi altında tam kat açık biyopsi yapılmalıdır.", "isLie": True, "explanation": "Tuzak! Pap smear invaziv cerrahi biyopsi değil, poliklinikte anestezi gerektirmeyen yüzeyel sürüntü yöntemidir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servikal sitoloji (Pap smear) taraması ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Transformasyon zonundan dökülen hücrelerin incelendiği bir eksfoliyatif sitoloji testidir",
                            "isCorrect": True,
                            "explanation": "Pap smear transformasyon zonunu hedefleyen eksfoliyatif sitolojik taramadır."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca kemik iliği aspirasyon biyopsisi ile birlikte yapılabilen ağır bir cerrahidir",
                            "isCorrect": False,
                            "explanation": "Basit, poliklinik şartlarında uygulanan invaziv olmayan sürüntü yöntemidir."
                        },
                        {
                            "key": "C",
                            "text": "Servikal karsinom mortalitesi üzerinde hiçbir düşürücü etkisi gösterilememiştir",
                            "isCorrect": False,
                            "explanation": "Düzenli taramayla mortaliteyi %70'in üzerinde azaltmıştır."
                        },
                        {
                            "key": "D",
                            "text": "Örnekleme sadece mesane kubbesinden ve üretra lümeninden yapılmalıdır",
                            "isCorrect": False,
                            "explanation": "Serviks transformasyon zonundan sürüntü alınır."
                        }
                    ]
                }
            ]
        },
        # S42
        {
            "slideNumber": 42,
            "title": "Bethesda Sitolojik Sınıflaması: Terminoloji ve Kategoriler",
            "subtitle": "ASC-US, LSIL ve HSIL sitolojik tanımları ve klinik anlamları",
            "clinicalFocus": "Sitolojik Derecelendirme",
            "content": "Servikal sitoloji sonuçlarının uluslararası standardizasyonunu sağlamak amacıyla günümüzde **Bethesda Sistemi** kullanılmaktadır. Bu sınıflama sitolojik bulguları net risk kategorilerine ayırır.\n\n- **ASC-US (Önemi Belirsiz Atipik Skuamöz Hücreler):** Hücrelerde reaktif değişiklikleri aşan nükleer büyüme ve hafif hiperkromazi vardır ancak kesin bir displazi tanısı koyduracak kriterleri tam karşılamaz; HPV DNA testi ile triyaj gerektirir.\n- **LSIL (Düşük Dereceli Skuamöz İntraepitelyal Lezyon):** Yüksek oranda geçici HPV enfeksiyonunu ve koilositik değişiklikleri temsil eder. Histopatolojik olarak **CIN 1** tablosuna karşılık gelir.\n- **HSIL (Yüksek Dereceli Skuamöz İntraepitelyal Lezyon):** Yüksek karsinom progresyon potansiyeline sahip belirgin nükleer atipi, artmış nükleus/sitoplazma oranı ve pleomorfizmi ifade eder; histopatolojik olarak **CIN 2 ve CIN 3** ile örtüşür.\n\n> [!NOTE]\n> Bethesda sistemi sitolojik yaymalar içindir; doku biyopsilerinde ise histopatolojik CIN (Servikal İntraepitelyal Neoplazi) terminolojisi kullanılır.",
            "synthesisNarrative": "Servikal sitoloji sonuçlarının uluslararası standardizasyonunu sağlamak amacıyla günümüzde **Bethesda Sistemi** kullanılmaktadır. Bu sınıflama sitolojik bulguları net risk kategorilerine ayırır.\n\n- **ASC-US (Önemi Belirsiz Atipik Skuamöz Hücreler):** Hücrelerde reaktif değişiklikleri aşan nükleer büyüme ve hafif hiperkromazi vardır ancak kesin bir displazi tanısı koyduracak kriterleri tam karşılamaz; HPV DNA testi ile triyaj gerektirir.\n- **LSIL (Düşük Dereceli Skuamöz İntraepitelyal Lezyon):** Yüksek oranda geçici HPV enfeksiyonunu ve koilositik değişiklikleri temsil eder. Histopatolojik olarak **CIN 1** tablosuna karşılık gelir.\n- **HSIL (Yüksek Dereceli Skuamöz İntraepitelyal Lezyon):** Yüksek karsinom progresyon potansiyeline sahip belirgin nükleer atipi, artmış nükleus/sitoplazma oranı ve pleomorfizmi ifade eder; histopatolojik olarak **CIN 2 ve CIN 3** ile örtüşür.\n\n> [!NOTE]\n> Bethesda sistemi sitolojik yaymalar içindir; doku biyopsilerinde ise histopatolojik CIN (Servikal İntraepitelyal Neoplazi) terminolojisi kullanılır.",
            "bulletPoints": [
                "Bethesda sistemi sitolojik yaymaları standartlaştıran terminolojidir.",
                "LSIL geçici HPV etkisini ve histopatolojik CIN 1'i temsil eder.",
                "HSIL yüksek progresyon riskli CIN 2 ve CIN 3'e karşılık gelir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Bethesda sitoloji sınıflamasında LSIL kategorisi histopatolojik olarak CIN 1 lezyonuna karşılık gelir.",
                    "maskedTerm": "CIN 1",
                    "hint": "Hafif displazi ve koilositoz tablosu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bethesda Sitolojisi ile Histopatolojik CIN Karşılaştırması",
                    "tableHeaders": ["Bethesda Sitoloji", "Histolojik Karşılık", "Klinik Karakter"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "LSIL (Low-Grade SIL)", "isMasked": False},
                                {"text": "CIN 1 (Hafif Displazi)", "isMasked": True, "hint": "epitelin alt üçte birinde atipi"},
                                {"text": "Çoğu gençte spontan regrese olur"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "HSIL (High-Grade SIL)", "isMasked": False},
                                {"text": "CIN 2 ve CIN 3 (CIS)", "isMasked": True, "hint": "orta-ağır displazi ve karsinoma in situ"},
                                {"text": "Cerrahi tedavi ve eksizyon gerektirir"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Sitolojik Anormallikten Histolojik Doğrulamaya",
                    "steps": [
                        "1. Yayma Raporu: Pap smear sitolojisinde yüksek nükleus/sitoplazma oranlı hücrelerle HSIL saptanır.",
                        "2. Kolposkopi: Serviks büyütme altında asetik asit ve Lugol iyot ile incelenir.",
                        "3. Hedefe Yönelik Biyopsi: Şüpheli asetobeyaz alandan punch biyopsi örneği alınır.",
                        "4. Histopatolojik Tanı: Patolog doku kesitinde displazinin derinliğini ölçerek CIN 2/3 tanısını netleştirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bethesda sınıflamasındaki HSIL kategorisi histopatolojide hangi displazi derecelerine karşılık gelir?",
                    "answer": "CIN 2 (orta dereceli displazi) ve CIN 3 (ağır displazi / karsinoma in situ) tablolarına karşılık gelir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Bethesda Sitolojik Sınıflaması",
                    "items": [
                        {"text": "LSIL çoğunlukla geçici HPV enfeksiyonu ve koilositozu yansıtır.", "isLie": False, "explanation": "Doğru. Genç kadınlarda çoğu geriler."},
                        {"text": "HSIL sitolojisi histopatolojik olarak CIN 2 ve CIN 3 ile ilişkilidir.", "isLie": False, "explanation": "Doğru. Ciddi premalign potansiyel taşır."},
                        {"text": "ASC-US, reaktif değişiklikleri aşan ama kesin SIL kriteri taşımayan atipidir.", "isLie": False, "explanation": "Doğru. Triyaj gerektiren sınırda gruptur."},
                        {"text": "LSIL saptanan her hastaya vakit kaybetmeden radikal histerektomi yapılmalıdır.", "isLie": True, "explanation": "Tuzak! LSIL genç kadınlarda çok yüksek oranda spontan geriler, radikal histerektomi endikasyonu kesinlikle yoktur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Bethesda sınıflaması ve karşılık geldiği histopatolojik lezyonlarla ilgili aşağıdaki eşleştirmelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "LSIL sitolojisi temelde histopatolojik CIN 1'e, HSIL ise CIN 2 ve CIN 3'e karşılık gelir",
                            "isCorrect": True,
                            "explanation": "LSIL CIN 1'i temsil ederken HSIL CIN 2 ve CIN 3 lezyonlarını kapsar."
                        },
                        {
                            "key": "B",
                            "text": "LSIL her zaman metastatik kemik tümörünü temsil eden bir acil durumdur",
                            "isCorrect": False,
                            "explanation": "LSIL selim seyirli hafif servikal skuamöz displazidir."
                        },
                        {
                            "key": "C",
                            "text": "HSIL sitolojisi saptandığında hiçbir tedavi veya takip yapılmadan vaka kapatılır",
                            "isCorrect": False,
                            "explanation": "HSIL yüksek kanserleşme riski taşıdığı için kolposkopik biyopsi ve tedavi şarttır."
                        },
                        {
                            "key": "D",
                            "text": "ASC-US tanısı yalnızca böbrek glomerül epitelinin incelenmesiyle konur",
                            "isCorrect": False,
                            "explanation": "ASC-US servikal skuamöz epitel sitolojisine ait bir kategoridir."
                        }
                    ]
                }
            ]
        },
        # S43
        {
            "slideNumber": 43,
            "title": "Servikal İntraepitelyal Neoplazi (CIN 1, 2, 3) Histopatolojisi",
            "subtitle": "Epitel katmanlarının tutulum derinliği, atipi ve bazal membran bütünlüğü",
            "clinicalFocus": "Histopatolojik Displazi",
            "content": "Servikal İntraepitelyal Neoplazi (CIN), skuamöz epitel hücrelerinde maturasyon kaybı, nükleer hiperkromazi, pleomorfizm ve mitotik aktivitenin bazalden yüzeye doğru yayılım derinliğine göre üç dereceye ayrılır.\n\n- **CIN 1 (Hafif Displazi):** Atipik nükleer değişiklikler ve mitozlar yalnızca **epitelin alt 1/3 tabakasına** sınırlıdır. Yüzeyel katmanlarda tipik HPV koilositozu (perinükleer vakuolizasyon, buruşuk nükleus) eşlik eder. Olguların %60'tan fazlası kendiliğinden geriler.\n- **CIN 2 (Orta Dereceli Displazi):** Hücresel atipi ve polarite kaybı **epitelin alt 2/3'lük kısmına** kadar ilerlemiştir; yüzeyel tabakada hafif maturasyon korunmuştur.\n- **CIN 3 (Ağır Displazi / Karsinoma in Situ):** Atipik, bazaloid hücreler **epitel kalınlığının 2/3'ünden fazlasını veya tamamını** kaplar. Matürasyon tamamen kaybolmuştur ve atipik mitozlar üst katmanlarda izlenir.\n\n> [!IMPORTANT]\n> [KRİTİK UYARI] CIN 3 lezyonunda tüm epitel katmanları atipik hücrelerle dolmuş olsa dahi **bazal membran sağlamdır**; bazal membran aşıldığı anda lezyon artık invaziv karsinom adını alır.",
            "synthesisNarrative": "Servikal İntraepitelyal Neoplazi (CIN), skuamöz epitel hücrelerinde maturasyon kaybı, nükleer hiperkromazi, pleomorfizm ve mitotik aktivitenin bazalden yüzeye doğru yayılım derinliğine göre üç dereceye ayrılır.\n\n- **CIN 1 (Hafif Displazi):** Atipik nükleer değişiklikler ve mitozlar yalnızca **epitelin alt 1/3 tabakasına** sınırlıdır. Yüzeyel katmanlarda tipik HPV koilositozu (perinükleer vakuolizasyon, buruşuk nükleus) eşlik eder. Olguların %60'tan fazlası kendiliğinden geriler.\n- **CIN 2 (Orta Dereceli Displazi):** Hücresel atipi ve polarite kaybı **epitelin alt 2/3'lük kısmına** kadar ilerlemiştir; yüzeyel tabakada hafif maturasyon korunmuştur.\n- **CIN 3 (Ağır Displazi / Karsinoma in Situ):** Atipik, bazaloid hücreler **epitel kalınlığının 2/3'ünden fazlasını veya tamamını** kaplar. Matürasyon tamamen kaybolmuştur ve atipik mitozlar üst katmanlarda izlenir.\n\n> [!IMPORTANT]\n> [KRİTİK UYARI] CIN 3 lezyonunda tüm epitel katmanları atipik hücrelerle dolmuş olsa dahi **bazal membran sağlamdır**; bazal membran aşıldığı anda lezyon artık invaziv karsinom adını alır.",
            "bulletPoints": [
                "CIN 1'de atipi epitelin alt 1/3'üne sınırlıdır ve koilositoz eşlik eder.",
                "CIN 2'de atipi alt 2/3 tabakaya yayılır.",
                "CIN 3'te tam kat atipi vardır ancak bazal membran kesinlikle sağlamdır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "CIN 3 lezyonunda atipi epitelin tamamını kaplasa dahi bazal membran kesintisiz ve sağlam kalır.",
                    "maskedTerm": "bazal membran",
                    "hint": "Epiteli stromadan ayıran hücre dışı matriks bariyeri"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "CIN Derecelerinin Katman Derinliği Özeti",
                    "tableHeaders": ["Lezyon Derecesi", "Atipinin Katman Derinliği", "Bazal Membran Durumu"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "CIN 1", "isMasked": False},
                                {"text": "Epitelin alt 1/3 tabakası", "isMasked": True, "hint": "en yüzeyel olmayan bazal bölge"},
                                {"text": "Sağlam ve intakt"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "CIN 3 (CIS)", "isMasked": False},
                                {"text": "Epitelin 2/3'ünden fazlası veya tam kat", "isMasked": True, "hint": "tüm kalınlığı tutan atipi"},
                                {"text": "Sağlam (aşılırsa invaziv karsinom olur)"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "CIN Spektrumunda Morfolojik Progresyon",
                    "steps": [
                        "1. Bazal Tabaka Enfeksiyonu: HPV onkoproteinleri bazal hücre döngüsünü bozar.",
                        "2. CIN 1: Epitelin alt 1/3'ünde nükleer büyüme ve yüzeyde koilositik vakuoller belirir.",
                        "3. CIN 2: Atipik hücreler epitel kalınlığının 2/3'üne kadar tırmanır.",
                        "4. CIN 3: Tam kata yakın atipik hücre yığılması ve matürasyon kaybı oluşur, bazal membran henüz aşılmamıştır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "CIN 3 (karsinoma in situ) ile invaziv skuamöz hücreli karsinom arasındaki temel histopatolojik ayrım kriteri nedir?",
                    "answer": "Bazal membranın durumudur; CIN 3'te bazal membran tamamen intakttır, invaziv karsinomda ise atipik hücreler bazal membranı aşarak altındaki stroma içine girmiştir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "CIN Histopatolojik Derecelendirmesi",
                    "items": [
                        {"text": "CIN 1 lezyonunda atipi epitelin alt 1/3 tabakasına sınırlıdır.", "isLie": False, "explanation": "Doğru. Hafif displazi tanımıdır."},
                        {"text": "CIN 3 lezyonunda bazal membran kesintiye uğramamıştır, sağlamdır.", "isLie": False, "explanation": "Doğru. Aşılırsa invaziv karsinom olur."},
                        {"text": "CIN 1 olgularının önemli bir kısmı immün yanıtla spontan geriler.", "isLie": False, "explanation": "Doğru. Olguların %60'ından fazlası regrese olur."},
                        {"text": "CIN 1 tanısı konduğu anda stroma içinde masif vasküler invazyon başlamıştır.", "isLie": True, "explanation": "Tuzak! CIN lezyonları intraepitelyaldir; CIN 1'de stromal veya vasküler invazyon kesinlikle yoktur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servikal İntraepitelyal Neoplazi (CIN) derecelendirmesi ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "CIN 1'de atipi alt 1/3'e sınırlıyken, CIN 3'te tam kat atipi izlenir fakat bazal membran intakttır",
                            "isCorrect": True,
                            "explanation": "CIN sınıflaması atipinin epitel kalınlığı boyunca yayılımına dayanır; CIN 3'te bazal membran sağlamdır."
                        },
                        {
                            "key": "B",
                            "text": "CIN 1 lezyonunda atipik hücreler kemik iliği ve akciğer dokusuna yayılmıştır",
                            "isCorrect": False,
                            "explanation": "CIN 1 epitelin alt 1/3'üne sınırlı preinvaziv hafif displazidir."
                        },
                        {
                            "key": "C",
                            "text": "CIN 3 tanısı konabilmesi için mutlaka karaciğer metastazı görülmelidir",
                            "isCorrect": False,
                            "explanation": "CIN 3 intraepitelyal bir lezyondur, uzak metastaz yapamaz."
                        },
                        {
                            "key": "D",
                            "text": "CIN derecelendirmesi atipik hücrelerin sayısına değil yalnızca hastanın saç rengine göre yapılır",
                            "isCorrect": False,
                            "explanation": "Epitel katmanlarının tutulum derinliğine göre yapılır."
                        }
                    ]
                }
            ]
        },
        # S44
        {
            "slideNumber": 44,
            "title": "HPV DNA Testi ve Kolposkopik İncelemenin Rolü",
            "subtitle": "Moleküler tarama, asetik asit uygulaması ve biyopsi alanının belirlenmesi",
            "clinicalFocus": "Tanısal Algoritma",
            "content": "Servikal karsinogenez taramasında modern protokoller Pap smear ile birlikte yüksek riskli **HPV DNA testini** birleştirerek duyarlılığı en üst düzeye çıkarmaktadır.\n\n- **HPV DNA Taraması:** Özellikle HPV 16 ve 18 gibi yüksek riskli tiplerin saptanması, sitoloji normal olsa dahi hastanın artmış displazi riski taşıdığını gösterir ve yakın takibi zorunlu kılar.\n- **Kolposkopi Prensibi:** Çıplak gözle görülemeyen erken lezyonları büyütme altında inceleyen optik bir yöntemdir. Serviks yüzeyine %3-5'lik asetik asit (sirke ruhu) uygulandığında yüksek nükleuslu displastik epitel hücreleri proteini çökelterek **asetobeyaz alanlar** oluşturur.\n- **Doğrudan Biyopsi:** Kolposkopi körlemesine biyopsi yapılmasını engeller; kolposkopist asetobeyaz epitel, punktuasyon veya mozaik damarlanma gösteren en şüpheli alandan punch biyopsi alarak patoloğa gönderir.\n\n> [!NOTE]\n> Kolposkopi tek başına kesin doku tanısı koymaz; hedefe yönelik biyopsi alanını kusursuz biçimde belirleyerek histopatolojik incelemeye materyal sağlar.",
            "synthesisNarrative": "Servikal karsinogenez taramasında modern protokoller Pap smear ile birlikte yüksek riskli **HPV DNA testini** birleştirerek duyarlılığı en üst düzeye çıkarmaktadır.\n\n- **HPV DNA Taraması:** Özellikle HPV 16 ve 18 gibi yüksek riskli tiplerin saptanması, sitoloji normal olsa dahi hastanın artmış displazi riski taşıdığını gösterir ve yakın takibi zorunlu kılar.\n- **Kolposkopi Prensibi:** Çıplak gözle görülemeyen erken lezyonları büyütme altında inceleyen optik bir yöntemdir. Serviks yüzeyine %3-5'lik asetik asit (sirke ruhu) uygulandığında yüksek nükleuslu displastik epitel hücreleri proteini çökelterek **asetobeyaz alanlar** oluşturur.\n- **Doğrudan Biyopsi:** Kolposkopi körlemesine biyopsi yapılmasını engeller; kolposkopist asetobeyaz epitel, punktuasyon veya mozaik damarlanma gösteren en şüpheli alandan punch biyopsi alarak patoloğa gönderir.\n\n> [!NOTE]\n> Kolposkopi tek başına kesin doku tanısı koymaz; hedefe yönelik biyopsi alanını kusursuz biçimde belirleyerek histopatolojik incelemeye materyal sağlar.",
            "bulletPoints": [
                "HPV DNA testi yüksek riskli tiplerin moleküler taranmasını sağlar.",
                "Kolposkopi serviksi büyüterek asetobeyaz alanları ortaya çıkarır.",
                "Şüpheli odaktan doğrudan hedefe yönelik biyopsi alınmasını sağlar."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Kolposkopik incelemede serviks yüzeyine uygulanan asetik asit displastik epitelde asetobeyaz alanlar oluşturur.",
                    "maskedTerm": "asetobeyaz alanlar",
                    "hint": "Nükleer protein presipitasyonu sonucu beyazlaşan epitel görünümü"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Kolposkopi ve HPV Testinin Tanısal Görevleri",
                    "tableHeaders": ["Tanısal Araç", "Uygulama Prensibi", "Klinik Çıktı"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "HPV DNA Testi", "isMasked": False},
                                {"text": "Yüksek riskli virüs genomu amplifikasyonu", "isMasked": True, "hint": "moleküler viral DNA tespiti"},
                                {"text": "Yüksek onkojenik riski belirleme"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Kolposkopi", "isMasked": False},
                                {"text": "Optik büyütme ve asetik asitle boyama", "isMasked": False},
                                {"text": "Hedefe yönelik punch biyopsi yeri seçimi", "isMasked": True, "hint": "şüpheli sahadan doku alma rehberliği"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Pozitif Tarama Sonrası Tanı Algoritması",
                    "steps": [
                        "1. Tarama Pozitifliği: Hastada HPV 16 pozitifliği veya HSIL sitolojisi saptanır.",
                        "2. Kolposkopi: Serviks büyütülerek incelenir ve asetik asit solüsyonu sürülür.",
                        "3. Asetobeyaz Görünüm: Nükleer yoğunluğu yüksek displastik epitel beyazlaşarak belirginleşir.",
                        "4. Punch Biyopsi: Belirlenen en yoğun asetobeyaz odaktan biyopsi alınarak histolojik tanıya gidilir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Kolposkopi sırasında displastik alanları görünür kılmak için serviks epiteline hangi solüsyon uygulanır?",
                    "answer": "Asetik asit (%3-5 solüsyon); hücresel proteinleri koagüle ederek displastik epitelin asetobeyaz görünmesini sağlar."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "HPV Testi ve Kolposkopi",
                    "items": [
                        {"text": "Yüksek riskli HPV DNA testi servikal karsinom riskini moleküler olarak gösterir.", "isLie": False, "explanation": "Doğru. Özellikle tip 16 ve 18 varlığı kritiktir."},
                        {"text": "Kolposkopide asetik asit uygulaması displastik alanlarda asetobeyaz değişikliğe yol açar.", "isLie": False, "explanation": "Doğru. Artmış nükleer yoğunluk opak beyazlaşır."},
                        {"text": "Kolposkopi hedefe yönelik punch biyopsi alınmasına kılavuzluk eder.", "isLie": False, "explanation": "Doğru. Şüpheli odaklar doğrudan örneklenir."},
                        {"text": "Kolposkopi bir optik yöntem değil, radyoaktif uranyum enjekte edilen bir nükleer tıp taramasıdır.", "isLie": True, "explanation": "Tuzak! Kolposkopi ışık kaynağı ve merceklerden oluşan girişimsel olmayan bir optik büyütme aletidir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Serviks tarama ve tanı protokollerinde kolposkopi yönteminin temel görevi nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Serviksi büyüterek asetik asitle belirginleşen asetobeyaz alanlardan hedefe yönelik biyopsi alınmasını sağlamak",
                            "isCorrect": True,
                            "explanation": "Kolposkopi displastik alanları büyüterek doğru odaktan biyopsi alınmasına olanak tanır."
                        },
                        {
                            "key": "B",
                            "text": "Kemik iliği nakli öncesi tüm kemik iliğini radyasyonla yok etmek",
                            "isCorrect": False,
                            "explanation": "Kolposkopi serviksin jinekolojik optik muayenesidir."
                        },
                        {
                            "key": "C",
                            "text": "Akciğer tüberkülozunun balgam kültürünü hazırlamak",
                            "isCorrect": False,
                            "explanation": "Serviks hastalıkları tanı aracıdır."
                        },
                        {
                            "key": "D",
                            "text": "Herhangi bir görüntü oluşturmadan yalnızca genel anestezi derinliğini ölçmek",
                            "isCorrect": False,
                            "explanation": "Optik büyütme sağlayan bir muayene cihazıdır."
                        }
                    ]
                }
            ]
        },
        # S45
        {
            "slideNumber": 45,
            "title": "İnvaziv Servikal Karsinom: Makroskopik Tipler",
            "subtitle": "Ekzofitik polipoid kitleler, endofitik ülseratif lezyonlar ve fıçı serviks",
            "clinicalFocus": "Tümör Makroskopisi",
            "content": "Servikal intraepitelyal lezyonlar bazal membranı aşarak stromayı işgal ettiğinde **invaziv servikal karsinom** gelişir. Makroskopik olarak lezyonlar başlıca iki morfolojik büyüme paterni gösterir.\n\n- **Ekzofitik (Mantarsı / Polipoid) Büyüme:** Tümör serviks yüzeyinden vajen boşluğuna doğru karnabahar veya polip benzeri kitleler şeklinde lümene doğru büyür. Kolayca kanayan, kırılgan ve nekrotik alanlar içerir; jinekolojik spekulum muayenesinde hızla fark edilir.\n- **Endofitik (Ülseratif / İnfiltratif) Büyüme:** Tümör vajen lümenine belirgin bir çıkıntı yapmaksızın, servikal stromanın derinliklerine ve servikal kanala doğru içeriye infiltrasyon gösterir. Yüzeyde krater benzeri ülserleşme yaratır.\n- **Fıçı Serviks (Barrel-Shaped Cervix):** Endoservikal kanalda derinlemesine büyüyen endofitik karsinom tüm serviksi diffüz biçimde sertleştirip genişleterek fıçı şeklinde devasa bir kitleye dönüştürebilir.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Ekzofitik tümörler vajinaya sarkan polipoid kitlelerle postkoital kanama yaparken, endofitik tümörler serviks stromasını sessizce derinlemesine infiltre ederek çevre dokulara erken yayılabilir.",
            "synthesisNarrative": "Servikal intraepitelyal lezyonlar bazal membranı aşarak stromayı işgal ettiğinde **invaziv servikal karsinom** gelişir. Makroskopik olarak lezyonlar başlıca iki morfolojik büyüme paterni gösterir.\n\n- **Ekzofitik (Mantarsı / Polipoid) Büyüme:** Tümör serviks yüzeyinden vajen boşluğuna doğru karnabahar veya polip benzeri kitleler şeklinde lümene doğru büyür. Kolayca kanayan, kırılgan ve nekrotik alanlar içerir; jinekolojik spekulum muayenesinde hızla fark edilir.\n- **Endofitik (Ülseratif / İnfiltratif) Büyüme:** Tümör vajen lümenine belirgin bir çıkıntı yapmaksızın, servikal stromanın derinliklerine ve servikal kanala doğru içeriye infiltrasyon gösterir. Yüzeyde krater benzeri ülserleşme yaratır.\n- **Fıçı Serviks (Barrel-Shaped Cervix):** Endoservikal kanalda derinlemesine büyüyen endofitik karsinom tüm serviksi diffüz biçimde sertleştirip genişleterek fıçı şeklinde devasa bir kitleye dönüştürebilir.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Ekzofitik tümörler vajinaya sarkan polipoid kitlelerle postkoital kanama yaparken, endofitik tümörler serviks stromasını sessizce derinlemesine infiltre ederek çevre dokulara erken yayılabilir.",
            "bulletPoints": [
                "Ekzofitik karsinomlar vajinaya doğru karnabahar benzeri kitle oluşturur.",
                "Endofitik karsinomlar stromayı derinlemesine infiltre ederek ülserleşir.",
                "Endoservikal derin yayılım serviksi sertleştirerek fıçı serviks tablosuna yol açar."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "İnvaziv serviks karsinomunda vajen boşluğuna karnabahar gibi sarkan lümen içi kitlelere ekzofitik tümör adı verilir.",
                    "maskedTerm": "ekzofitik",
                    "hint": "Dışa doğru polipoid büyüyen lezyon tipi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Serviks Karsinomunun Makroskopik Büyüme Paternleri",
                    "tableHeaders": ["Büyüme Deseni", "Gelişim Yönü", "Morfolojik Görünüm"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Ekzofitik Tip", "isMasked": False},
                                {"text": "Vajina lümenine doğru dışa büyüme", "isMasked": True, "hint": "lümen içi polipoid proliferasyon"},
                                {"text": "Karnabahar benzeri, kırılgan ve kanamalı kitle"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Endofitik Tip", "isMasked": False},
                                {"text": "Serviks stromasına doğru derin infiltrasyon", "isMasked": True, "hint": "içe doğru invazyon"},
                                {"text": "Krater şeklinde ülser veya fıçı serviks"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Endofitik Karsinomun Fıçı Servikse İlerlemesi",
                    "steps": [
                        "1. Endoservikal Karsinogenez: Transformasyon zonu veya kanal bezlerinden invaziv karsinom başlar.",
                        "2. Derin Stromal İnvazyon: Tümör hücreleri vajina lümenine taşmak yerine stroma içine doğru ilerler.",
                        "3. Doku Sklerozu ve Genişleme: Serviks duvarı tümör adaları ve desmoplazi ile çepeçevre kalınlaşır.",
                        "4. Fıçı Serviks: Serviks simetrik biçimde sertleşerek genişlemiş fıçı morfolojisi kazanır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Serviks karsinomunun vajina lümenine doğru karnabahar şeklinde kitle yapması hangi makroskopik büyüme paterni olarak adlandırılır?",
                    "answer": "Ekzofitik (polipoid / mantarsı) büyüme paterni."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Servikal Karsinom Makroskopisi",
                    "items": [
                        {"text": "Ekzofitik karsinomlar vajinaya doğru karnabahar benzeri polipoid kitleler oluşturur.", "isLie": False, "explanation": "Doğru. Dışa doğru lümene büyürler."},
                        {"text": "Endofitik karsinomlar serviks stromasını derinlemesine infiltre eder.", "isLie": False, "explanation": "Doğru. Yüzeyde krater benzeri ülserleşme yapabilir."},
                        {"text": "Endoservikal derin infiltrasyon tüm serviksi sertleştirerek fıçı serviks tablosu yaratabilir.", "isLie": False, "explanation": "Doğru. Klasik makroskopik tablodur."},
                        {"text": "İnvaziv serviks karsinomu daima sadece sol ayak başparmağında tırnak batması şeklinde başlar.", "isLie": True, "explanation": "Tuzak! Serviks karsinomu uterus serviksinde gelişen bir genital sistem kanseridir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "İnvaziv servikal skuamöz hücreli karsinomun makroskopik görünümleri ile ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Vajina boşluğuna taşan karnabahar benzeri kitleler ekzofitik, stromayı derinden tutan lezyonlar endofitiktir",
                            "isCorrect": True,
                            "explanation": "Ekzofitik dışa lümene, endofitik ise stroma derinliğine doğru yayılımı ifade eder."
                        },
                        {
                            "key": "B",
                            "text": "Serviks kanseri daima kıkırdak ve kemik dokusundan oluşan iyi huylu bir kisttir",
                            "isCorrect": False,
                            "explanation": "Malign epiteliyal neoplazmdır."
                        },
                        {
                            "key": "C",
                            "text": "Endofitik tümörler hiçbir zaman servikal stromayı infiltre edemezler",
                            "isCorrect": False,
                            "explanation": "Endofitik tümörlerin temel özelliği derin stromal infiltrasyondur."
                        },
                        {
                            "key": "D",
                            "text": "Fıçı serviks tablosu yalnızca tiroid bezinin aşırı iyot almasıyla meydana gelir",
                            "isCorrect": False,
                            "explanation": "Serviksin derin tümöral tutulumu sonucu gelişen jinekolojik bulgudur."
                        }
                    ]
                }
            ]
        },
        # S46
        {
            "slideNumber": 46,
            "title": "Doğrudan Pelvik Yayılım ve Ölüm Nedeni: Üreter Obstrüksiyonu ve Üremi",
            "subtitle": "Parametriyum invazyonu, bilateral hidronefroz ve böbrek yetmezliği",
            "clinicalFocus": "Lokal Yayılım ve Mortalite",
            "content": "Servikal karsinomun en önemli klinik özelliği, uzak organ metastazlarından çok önce **komşu pelvik dokulara doğrudan lokal invazyon** gösterme eğilimidir.\n\n- **Doğrudan İnvazyon Yolları:** Tümör lateralde parametriyumlara, süperiyorda korpus uterusa, inferiyorda vajina duvarına, anteriyorda mesaneye ve posteriyorda rektuma doğrudan ilerler.\n- **Üreter Basısı ve Obstrüksiyon:** Parametriyum içine lateral invazyon sırasında serviksin hemen 1.5-2 cm lateralinden geçen **üreterleri sararak sıkıştırır veya lümenlerini tıkar**.\n- **En Sık Ölüm Nedeni:** Üreterlerin bilateral tümöral bası altında kalması sonucunda bilateral hidronefroz, postrenal böbrek yetmezliği ve **üremi** gelişir. İleri evre tedavi edilmemiş serviks kanserinde hastaların en sık ölüm nedeni üremidir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] İleri evre invaziv serviks karsinomunda en yaygın ölüm nedeni, parametrial yayılımla üreterlerin tıkanması sonucu gelişen bilateral hidronefroz ve üremidir (böbrek yetmezliği).",
            "synthesisNarrative": "Servikal karsinomun en önemli klinik özelliği, uzak organ metastazlarından çok önce **komşu pelvik dokulara doğrudan lokal invazyon** gösterme eğilimidir.\n\n- **Doğrudan İnvazyon Yolları:** Tümör lateralde parametriyumlara, süperiyorda korpus uterusa, inferiyorda vajina duvarına, anteriyorda mesaneye ve posteriyorda rektuma doğrudan ilerler.\n- **Üreter Basısı ve Obstrüksiyon:** Parametriyum içine lateral invazyon sırasında serviksin hemen 1.5-2 cm lateralinden geçen **üreterleri sararak sıkıştırır veya lümenlerini tıkar**.\n- **En Sık Ölüm Nedeni:** Üreterlerin bilateral tümöral bası altında kalması sonucunda bilateral hidronefroz, postrenal böbrek yetmezliği ve **üremi** gelişir. İleri evre tedavi edilmemiş serviks kanserinde hastaların en sık ölüm nedeni üremidir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] İleri evre invaziv serviks karsinomunda en yaygın ölüm nedeni, parametrial yayılımla üreterlerin tıkanması sonucu gelişen bilateral hidronefroz ve üremidir (böbrek yetmezliği).",
            "bulletPoints": [
                "Serviks karsinomu uzak metastazdan önce çevre pelvik dokulara doğrudan yayılır.",
                "Parametrial yayılım üreterleri sararak bilateral obstrüksiyona yol açar.",
                "En sık ölüm nedeni bilateral hidronefroz ve üremidir (böbrek yetmezliği)."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "İleri evre servikal karsinom hastalarında en sık ölüm nedeni üreter obstrüksiyonuna bağlı üremi tablosudur.",
                    "maskedTerm": "üremi",
                    "hint": "Postrenal böbrek yetmezliği sonucu kanda toksik azotlu atıkların birikmesi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Servikal Karsinomun Pelvik Yayılımı ve Sonuçları",
                    "tableHeaders": ["Yayılım Yönü", "Tutulan Anatomik Yapı", "Ortaya Çıkan Klinik Tablo"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Lateral Yayılım", "isMasked": False},
                                {"text": "Parametriyum ve Üreterler", "isMasked": True, "hint": "pelvik yan duvar damar ve idrar kanalları"},
                                {"text": "Bilateral hidronefroz, böbrek yetmezliği ve üremi"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Anterior / Posterior", "isMasked": False},
                                {"text": "Mesane ve Rektum", "isMasked": False},
                                {"text": "Hematüri, rektal kanama veya fistül gelişimi", "isMasked": True, "hint": "organlar arası yapay kanal açılması"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Parametrial İnvazyondan Üremiye Ölüm Mekanizması",
                    "steps": [
                        "1. Stromal İnvazyon: Tümör serviks sınırını aşarak lateral parametrial yağ dokusuna girer.",
                        "2. Üreter Çevrelenmesi: Tümör kitlesi parametriyumdan geçen bilateral üreterleri sarar ve daraltır.",
                        "3. İdrar Akımının Durması: İdrar böbrek pelvisinde birikerek bilateral hidronefroz oluşturur.",
                        "4. Postrenal Böbrek Yetmezliği: Fonksiyonel nefron kaybı üremiye ve ölüme yol açar."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "İleri evre serviks kanseri olgularında en sık karşılaşılan ölüm nedeni nedir ve hangi anatomik mekanizmayla oluşur?",
                    "answer": "En sık ölüm nedeni üremidir (böbrek yetmezliği); lateral parametrial invazyonla üreterlerin sıkışması ve bilateral hidronefroz gelişmesi sonucu oluşur."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Pelvik Yayılım ve Üremi",
                    "items": [
                        {"text": "Serviks karsinomu uzak metastazlardan önce lokal pelvik dokulara doğrudan yayılır.", "isLie": False, "explanation": "Doğru. Lokal invazyon ön plandadır."},
                        {"text": "Parametrial yayılım üreterleri sıkıştırarak bilateral hidronefroza neden olur.", "isLie": False, "explanation": "Doğru. Üreter basısı klasik bulgudur."},
                        {"text": "İleri evre serviks kanserinde en sık ölüm nedeni üremidir.", "isLie": False, "explanation": "Doğru. Böbrek yetmezliği temel mortalite nedenidir."},
                        {"text": "Serviks kanseri üreterleri hiçbir zaman etkilemez, yalnızca dalakta kanamaya yol açar.", "isLie": True, "explanation": "Tuzak! Serviks kanseri komşuluğu nedeniyle en çok parametriyum ve üreterleri tutar."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "İleri evre servikal skuamöz karsinom tanılı bir hastada en yaygın ölüm nedeni ve buna yol açan patolojik mekanizma aşağıdakilerden hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Parametrial invazyonla üreterlerin tıkanması sonucu gelişen bilateral hidronefroz ve üremi",
                            "isCorrect": True,
                            "explanation": "Tümörün lateral parametrial yayılımla üreterleri tıkaması ve üremi geliştirmesi en sık ölüm nedenidir."
                        },
                        {
                            "key": "B",
                            "text": "Beyin sapına ani masif kanama gelişmesi",
                            "isCorrect": False,
                            "explanation": "Serviks karsinomunun primer mortalite mekanizması beyin sapı kanaması değildir."
                        },
                        {
                            "key": "C",
                            "text": "Akut apandisit perforasyonuna bağlı sepsis",
                            "isCorrect": False,
                            "explanation": "Serviks kanseri mortalitesiyle doğrudan ilişkili temel neden değildir."
                        },
                        {
                            "key": "D",
                            "text": "Mide ülserinin kontrolsüz asit salgılaması",
                            "isCorrect": False,
                            "explanation": "Mide patolojisidir, serviks kanseri ölüm mekanizmasını açıklamaz."
                        }
                    ]
                }
            ]
        },
        # S47
        {
            "slideNumber": 47,
            "title": "Bölgesel Lenfatik Drenaj ve Evreleme Prensipleri",
            "subtitle": "Paraservikal, obturator, iliak lenf nodları ve paraaortik yayılım",
            "clinicalFocus": "Lenfatik Metastaz",
            "content": "Servikal karsinomun metastatik yayılımında lenfatik yol, doğrudan doku infiltrasyonuna paralel olarak en erken ve en kritik evreleme basamağını oluşturur.\n\n- **Birincil Lenfatik İstasyonlar:** Serviksin lenfatikleri öncelikle **paraservikal, parametriyal ve obturator** lenf nodlarına, ardından **internal ve eksternal iliak** lenf nodu zincirlerine drene olur.\n- **İkincil / İleri İstasyonlar:** İliak zincirlerden sonra metastaz **ortak (common) iliak ve paraaortik** lenf nodlarına ulaşır. Paraaortik nod tutulumu sistemik metastaz riskinin dramatik arttığını ve prognozun kötüleştiğini gösterir.\n- **Klinik Evreleme (FIGO):** Serviks kanseri geleneksel olarak FIGO evreleme sistemiyle değerlendirilir. Erken evrelerde cerrahi uygulanabilirken, lenf nodu pozitifliği ve parametrial tutulum varlığında radyoterapi ve kemoterapi kombine edilir.\n\n> [!NOTE]\n> Pelvik lenf nodu metastazı varlığı tek başına hastanın sağkalım oranını yarı yarıya düşüren en önemli bağımsız prognostik faktörlerden biridir.",
            "synthesisNarrative": "Servikal karsinomun metastatik yayılımında lenfatik yol, doğrudan doku infiltrasyonuna paralel olarak en erken ve en kritik evreleme basamağını oluşturur.\n\n- **Birincil Lenfatik İstasyonlar:** Serviksin lenfatikleri öncelikle **paraservikal, parametriyal ve obturator** lenf nodlarına, ardından **internal ve eksternal iliak** lenf nodu zincirlerine drene olur.\n- **İkincil / İleri İstasyonlar:** İliak zincirlerden sonra metastaz **ortak (common) iliak ve paraaortik** lenf nodlarına ulaşır. Paraaortik nod tutulumu sistemik metastaz riskinin dramatik arttığını ve prognozun kötüleştiğini gösterir.\n- **Klinik Evreleme (FIGO):** Serviks kanseri geleneksel olarak FIGO evreleme sistemiyle değerlendirilir. Erken evrelerde cerrahi uygulanabilirken, lenf nodu pozitifliği ve parametrial tutulum varlığında radyoterapi ve kemoterapi kombine edilir.\n\n> [!NOTE]\n> Pelvik lenf nodu metastazı varlığı tek başına hastanın sağkalım oranını yarı yarıya düşüren en önemli bağımsız prognostik faktörlerden biridir.",
            "bulletPoints": [
                "Serviksin lenfatikleri obturator, paraservikal ve iliak nodlara drene olur.",
                "İleri evrede common iliak ve paraaortik lenf nodlarına yayılım izlenir.",
                "Lenf nodu tutulumu en güçlü bağımsız prognostik faktördür."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Servikal karsinom metastazında iliak lenf nodlarından sonraki ileri lenfatik istasyon paraaortik lenf nodlarıdır.",
                    "maskedTerm": "paraaortik lenf nodları",
                    "hint": "Aort damarı çevresindeki retroperitoneal lenfatik istasyon"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Servikal Karsinom Lenfatik İstasyonları",
                    "tableHeaders": ["İstasyon Düzeyi", "Lenf Nodu Grupları", "Prognostik Anlam"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Bölgesel (Primer)", "isMasked": False},
                                {"text": "Obturator, paraservikal, internal/eksternal iliak", "isMasked": True, "hint": "pelvik taban lenf bezleri"},
                                {"text": "Pelvik radyoterapi/cerrahi alanına dahildir"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Uzak / İleri", "isMasked": False},
                                {"text": "Ortak iliak ve paraaortik nodlar", "isMasked": False},
                                {"text": "Sistemik yayılım riski ve kötü prognoz", "isMasked": True, "hint": "ileri evre göstergesi"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Karsinom Hücrelerinin Lenfatik Basamakları",
                    "steps": [
                        "1. Doku İstilası: Karsinom hücreleri serviks stromasındaki endotelyal lenfatik kanallara girer.",
                        "2. Bölgesel İstasyon: İlk olarak obturator ve internal iliak lenf düğümlerinde mikrometastazlar belirir.",
                        "3. Ortak İliak Yayılım: Metastatik yük artarak iliak damarlar boyunca retroperitona tırmanır.",
                        "4. Paraaortik Tutulum: Aort çevresi lenf bezleri tutularak duktus torasikus yoluyla sistemik dolaşıma açılır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Serviks karsinomunda bölgesel pelvik istasyonları aşarak retroperitonda tutulan ve kötü prognoza işaret eden ana lenf nodu grubu hangisidir?",
                    "answer": "Paraaortik lenf nodları; tutulumu ileri evreye ve yüksek sistemik yayılım riskine işaret eder."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Servikal Karsinom Lenfatik Yayılımı",
                    "items": [
                        {"text": "Serviks lenfatikleri öncelikle obturator ve iliak lenf nodlarına drene olur.", "isLie": False, "explanation": "Doğru. Primer drenaj sahasıdır."},
                        {"text": "Lenf nodu tutulumu serviks kanserinde en önemli prognostik faktörlerden biridir.", "isLie": False, "explanation": "Doğru. Sağkalımı doğrudan etkiler."},
                        {"text": "İleri evrede metastaz paraaortik lenf nodlarına kadar tırmanabilir.", "isLie": False, "explanation": "Doğru. Retroperitoneal basamaktır."},
                        {"text": "Serviks lenfi doğrudan sadece saç köklerindeki lenfatiklere drene olur.", "isLie": True, "explanation": "Tuzak! Serviks lenfatikleri pelvik obturator, iliak ve paraaortik nodlara drene olur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Serviks karsinomunun bölgesel lenfatik yayılımında en sık tutulan ilk lenf nodu grubu aşağıdakilerden hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Obturator, paraservikal ve internal/eksternal iliak lenf nodları",
                            "isCorrect": True,
                            "explanation": "Serviksin primer bölgesel lenf drenaj sahası obturator ve iliak istasyonlardır."
                        },
                        {
                            "key": "B",
                            "text": "Yalnızca submental ve submandibüler lenf bezleri",
                            "isCorrect": False,
                            "explanation": "Baş-boyun lenf düğümleridir."
                        },
                        {
                            "key": "C",
                            "text": "Aksiller apeks ve pektoral lenf nodları",
                            "isCorrect": False,
                            "explanation": "Meme ve üst ekstremite lenfatikleridir."
                        },
                        {
                            "key": "D",
                            "text": "Popliteal çukur derin lenf düğümleri",
                            "isCorrect": False,
                            "explanation": "Alt bacak lenf drenaj istasyonudur."
                        }
                    ]
                }
            ]
        },
        # S48
        {
            "slideNumber": 48,
            "title": "Mikroskobik Diferansiasyon: Keratinize ve Non-Keratinize Skuamöz Karsinom",
            "subtitle": "Keratin incileri, interselüler köprüler ve nükleer pleomorfizm",
            "clinicalFocus": "Histopatolojik Sınıflama",
            "content": "Servikal karsinomların yaklaşık %80-85'ini skuamöz hücreli karsinom (SCC) oluşturur. Histopatolojik incelemede skuamöz karsinom başlıca keratinize ve non-keratinize alt tiplere ayrılır.\n\n- **Keratinize Skuamöz Hücreli Karsinom:** Belirgin skuamöz diferansiasyon gösterir. Mikroskopide konsantrik lameller oluşturan pembe asidofilik **keratin incileri (keratin pearls)** ve hücreler arasında net **interselüler köprüler (dezmozomlar)** izlenir. Genellikle daha iyi diferansiye kabul edilir.\n- **Non-Keratinize Skuamöz Hücreli Karsinom:** Servikste en sık görülen tiptir. Hücreler geniş tabakalar veya kordonlar oluşturur ancak lameller keratin incisi yapımı izlenmez; tek tek hücrelerde diskeratoz görülebilir. Yüksek mitotik aktivite ve nükleer atipi belirgindir.\n- **Kötü Diferansiye Karsinom:** Küçük, bazaloid, sitoplazması dar ve aşırı pleomorfik hücrelerden oluşur; skuamöz diferansiasyon özellikleri güçlükle seçilir.\n\n> [!NOTE]\n> Keratin incisi varlığı tümörün skuamöz diferansiasyonunu kanıtlayan en karakteristik histopatolojik bulgudur.",
            "synthesisNarrative": "Servikal karsinomların yaklaşık %80-85'ini skuamöz hücreli karsinom (SCC) oluşturur. Histopatolojik incelemede skuamöz karsinom başlıca keratinize ve non-keratinize alt tiplere ayrılır.\n\n- **Keratinize Skuamöz Hücreli Karsinom:** Belirgin skuamöz diferansiasyon gösterir. Mikroskopide konsantrik lameller oluşturan pembe asidofilik **keratin incileri (keratin pearls)** ve hücreler arasında net **interselüler köprüler (dezmozomlar)** izlenir. Genellikle daha iyi diferansiye kabul edilir.\n- **Non-Keratinize Skuamöz Hücreli Karsinom:** Servikste en sık görülen tiptir. Hücreler geniş tabakalar veya kordonlar oluşturur ancak lameller keratin incisi yapımı izlenmez; tek tek hücrelerde diskeratoz görülebilir. Yüksek mitotik aktivite ve nükleer atipi belirgindir.\n- **Kötü Diferansiye Karsinom:** Küçük, bazaloid, sitoplazması dar ve aşırı pleomorfik hücrelerden oluşur; skuamöz diferansiasyon özellikleri güçlükle seçilir.\n\n> [!NOTE]\n> Keratin incisi varlığı tümörün skuamöz diferansiasyonunu kanıtlayan en karakteristik histopatolojik bulgudur.",
            "bulletPoints": [
                "Serviks karsinomlarının %80-85'i skuamöz hücreli karsinomdur.",
                "Keratinize SCC'de keratin incileri ve interselüler köprüler belirgindir.",
                "Non-keratinize SCC servikste en sık görülen histolojik tiptir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "İyi diferansiye skuamöz hücreli karsinom mikroskopisinde konsantrik keratin tabakalarından oluşan yapılara keratin incileri adı verilir.",
                    "maskedTerm": "keratin incileri",
                    "hint": "Skuamöz diferansiasyonun patognomonik lameller eozinofilik küresi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Skuamöz Karsinom Histolojik Tipleri",
                    "tableHeaders": ["Histolojik Tip", "Keratin İnci Varlığı", "Görülme Sıklığı"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Keratinize Skuamöz Ca", "isMasked": False},
                                {"text": "Belirgin ve bol miktarda mevcut", "isMasked": True, "hint": "lameller eozinofilik girdaplar"},
                                {"text": "Daha az yaygın, iyi diferansiye"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Non-Keratinize Skuamöz Ca", "isMasked": False},
                                {"text": "Lameller inci yok, tek hücre diskeratozu", "isMasked": True, "hint": "masif inci oluşturmayan tip"},
                                {"text": "Servikste en sık görülen tip"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Skuamöz Diferansiasyondan Karsinoma Histogenez",
                    "steps": [
                        "1. Neoplastik Transformasyon: Skuamöz hücreler kontrolsüz proliferasyon kazanır.",
                        "2. Matürasyon Derecesi: Tümör hücreleri keratin sentezleme yeteneğini kısmen korur.",
                        "3. Keratin İncisi Oluşumu: Konsantrik lameller halinde hücre içi keratin birikerek inci yapısı üretilir.",
                        "4. Histopatolojik Tanı: Patolog keratin incilerini görerek keratinize skuamöz karsinom tanısını kesinleştirir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Skuamöz hücreli karsinom mikroskopisinde skuamöz diferansiasyonu kanıtlayan konsantrik eozinofilik yapılara ne ad verilir?",
                    "answer": "Keratin incileri (keratin pearls); ayrıca hücreler arası interselüler köprüler (dezmozomlar) eşlik eder."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Skuamöz Karsinom Histopatolojisi",
                    "items": [
                        {"text": "Serviks karsinomlarının büyük çoğunluğu (%80-85) skuamöz hücreli karsinomdur.", "isLie": False, "explanation": "Doğru. En sık histolojik tiptir."},
                        {"text": "Keratinize SCC'de keratin incileri ve interselüler köprüler gözlenir.", "isLie": False, "explanation": "Doğru. Tipik diferansiasyon bulgularıdır."},
                        {"text": "Non-keratinize SCC servikste en yaygın karşılaşılan tiptir.", "isLie": False, "explanation": "Doğru. En sık görülen morfolojidir."},
                        {"text": "Skuamöz karsinom hücreleri daima sadece saf kemik osteoid matriksi üretir.", "isLie": True, "explanation": "Tuzak! Osteoid matriksi osteosarkom üretir; skuamöz karsinom hücreleri skuamöz epitel diferansiasyonu ve keratin üretir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servikal skuamöz hücreli karsinomun mikroskobik incelemesinde skuamöz diferansiasyonu en iyi gösteren histolojik bulgu hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Konsantrik tabakalanma gösteren keratin incileri ve interselüler köprüler",
                            "isCorrect": True,
                            "explanation": "Keratin incileri ve interselüler köprüler skuamöz diferansiasyonun temel histopatolojik kanıtıdır."
                        },
                        {
                            "key": "B",
                            "text": "Saf glikojen içeren nöronal akson yumakları",
                            "isCorrect": False,
                            "explanation": "Sinir dokusuna ait yapılardır."
                        },
                        {
                            "key": "C",
                            "text": "Karaciğer safra kanalikülleri ve hepatosit rozetleri",
                            "isCorrect": False,
                            "explanation": "Karaciğer dokusu bulgularıdır."
                        },
                        {
                            "key": "D",
                            "text": "Tiroid folikülleri içinde kolloid birikimi",
                            "isCorrect": False,
                            "explanation": "Tiroid bezi histolojisidir."
                        }
                    ]
                }
            ]
        },
        # S49
        {
            "slideNumber": 49,
            "title": "Tedavi Modaliteleri: Konizasyon, Histerektomi ve Radyoterapi",
            "subtitle": "Prekanseröz eksizyon sınırları, cerrahi evre ve radyokemoterapi endikasyonu",
            "clinicalFocus": "Klinik Yönetim",
            "content": "Servikal neoplazilerde tedavi seçimi, lezyonun preinvaziv (CIN) veya invaziv evrede olmasına, tümörün boyutuna ve yayılım derinliğine göre belirlenir.\n\n- **Konizasyon (LEEP / Soğuk Koni):** Yüksek dereceli intraepitelyal lezyonlarda (CIN 2/3) veya mikroinvaziv erken karsinomda transformasyon zonunun koni şeklinde cerrahi olarak çıkarılmasıdır. Hem kesin histopatolojik tanı sağlar hem de cerrahi sınır negatifse küratiftir.\n- **Radikal Histerektomi:** Erken evre invaziv karsinomda (FIGO Evre IA2 - IB1) uterus, serviks, parametriyumların bir kısmı ve üst vajen ile birlikte pelvik lenf nodu diseksiyonu yapılır.\n- **Kemoradyoterapi:** Parametrial yayılım gösteren (Evre IIB ve üzeri) veya cerrahiye uygun olmayan ileri evre tümörlerde primer tedavi radyoterapi ve eşzamanlı sisplatin bazlı kemoterapidir.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Parametrial tutulum saptanan serviks kanseri olgularında cerrahi primer tedavi seçeneği olmaktan çıkar; temel yaklaşım eşzamanlı kemoradyoterapidir.",
            "synthesisNarrative": "Servikal neoplazilerde tedavi seçimi, lezyonun preinvaziv (CIN) veya invaziv evrede olmasına, tümörün boyutuna ve yayılım derinliğine göre belirlenir.\n\n- **Konizasyon (LEEP / Soğuk Koni):** Yüksek dereceli intraepitelyal lezyonlarda (CIN 2/3) veya mikroinvaziv erken karsinomda transformasyon zonunun koni şeklinde cerrahi olarak çıkarılmasıdır. Hem kesin histopatolojik tanı sağlar hem de cerrahi sınır negatifse küratiftir.\n- **Radikal Histerektomi:** Erken evre invaziv karsinomda (FIGO Evre IA2 - IB1) uterus, serviks, parametriyumların bir kısmı ve üst vajen ile birlikte pelvik lenf nodu diseksiyonu yapılır.\n- **Kemoradyoterapi:** Parametrial yayılım gösteren (Evre IIB ve üzeri) veya cerrahiye uygun olmayan ileri evre tümörlerde primer tedavi radyoterapi ve eşzamanlı sisplatin bazlı kemoterapidir.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Parametrial tutulum saptanan serviks kanseri olgularında cerrahi primer tedavi seçeneği olmaktan çıkar; temel yaklaşım eşzamanlı kemoradyoterapidir.",
            "bulletPoints": [
                "CIN 2/3 ve mikroinvaziv lezyonlarda konizasyon tanı ve tedavi edicidir.",
                "Erken evre invaziv tümörlerde radikal histerektomi uygulanır.",
                "Parametrial yayılım varlığında primer tedavi kemoradyoterapidir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Parametriyum tutulumu gösteren ileri evre serviks karsinomunda temel tedavi yaklaşımı kemoradyoterapi yöntemidir.",
                    "maskedTerm": "kemoradyoterapi",
                    "hint": "Eşzamanlı radyasyon ve kemoterapötik ilaç kombinasyonu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Servikal Neoplazi Tedavi Seçenekleri",
                    "tableHeaders": ["Hastalık Düzeyi", "Standart Tedavi Yöntemi", "Tedavi Amacı"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "CIN 2 / CIN 3", "isMasked": False},
                                {"text": "Servikal konizasyon (LEEP / Soğuk Koni)", "isMasked": True, "hint": "transformasyon zonu eksizyonu"},
                                {"text": "İnvazyonu önleme ve sınır negatifliği sağlama"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Parametrial Tutulum (Evre IIB+)", "isMasked": False},
                                {"text": "Eşzamanlı kemoradyoterapi", "isMasked": True, "hint": "ışın ve ilaç kombinasyonu"},
                                {"text": "Lokal kontrol ve sistemik progresyonu önleme"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "CIN 3'ten Cerrahi Şifaya Tedavi Zinciri",
                    "steps": [
                        "1. Preinvaziv Tanı: Biyopside tam kat atipi gösteren CIN 3 doğrulanır.",
                        "2. Konizasyon Kararı: Hastaya transformasyon zonunu içeren koni şeklinde cerrahi eksizyon yapılır.",
                        "3. Patoloji Değerlendirmesi: Patolog konizasyon materyalinde cerrahi sınırların temiz olduğunu raporlar.",
                        "4. Tam Kür: İnvaziv karsinom gelişimi önlenerek hasta sağlığına kavuşturulur."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "CIN 2 ve CIN 3 olgularında hem kesin patolojik tanı sağlayan hem de temiz cerrahi sınırla tedavi edici olan eksizyonel cerrahi yönteme ne ad verilir?",
                    "answer": "Servikal konizasyon (LEEP veya soğuk koni biyopsi)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Servikal Neoplazilerde Tedavi Yaklaşımları",
                    "items": [
                        {"text": "Konizasyon CIN 2/3 olgularında hem tanısal hem tedavi edicidir.", "isLie": False, "explanation": "Doğru. Cerrahi sınır temizse küratiftir."},
                        {"text": "Erken evre serviks kanserinde radikal histerektomi uygulanabilir.", "isLie": False, "explanation": "Doğru. Seçilmiş erken olgularda standart cerrahidir."},
                        {"text": "Parametrial yayılımı olan ileri evre tümörlerde kemoradyoterapi tercih edilir.", "isLie": False, "explanation": "Doğru. Cerrahi yerine radyokemoterapi esastır."},
                        {"text": "CIN 3 tanısı alan tüm hastalara yalnızca antibiyotikli gargara verilerek tedavi sonlandırılır.", "isLie": True, "explanation": "Tuzak! CIN 3 ağır displazidir, antibiyotik gargarayla tedavi edilemez; cerrahi eksizyon (konizasyon) gerektirir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Parametriyum tutulumu bulunan (Evre IIB) invaziv serviks karsinomunda en uygun temel tedavi yaklaşımı aşağıdakilerden hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Eşzamanlı kemoradyoterapi (radyoterapi + kemoterapi kombinasyonu)",
                            "isCorrect": True,
                            "explanation": "Parametrial tutulumda primer cerrahi önerilmez; standart tedavi eşzamanlı kemoradyoterapidir."
                        },
                        {
                            "key": "B",
                            "text": "Sadece ayak tırnaklarına lokal masaj uygulanması",
                            "isCorrect": False,
                            "explanation": "Tıbbi tedavi değeri yoktur."
                        },
                        {
                            "key": "C",
                            "text": "Yalnızca oral kalsiyum tableti verilerek hastanın taburcu edilmesi",
                            "isCorrect": False,
                            "explanation": "Kanser tedavisinde yeri yoktur."
                        },
                        {
                            "key": "D",
                            "text": "Tedaviye gerek görülmeyip 50 yıl sonra kontrole çağrılması",
                            "isCorrect": False,
                            "explanation": "İleri evre kanserde acil onkolojik tedavi şarttır."
                        }
                    ]
                }
            ]
        },
        # S50
        {
            "slideNumber": 50,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 5] Servikal Displazi ve Karsinom Evrelemesi",
            "subtitle": "Bölüm 5 kapsamındaki Pap smear, CIN sınıflaması ve invaziv karsinom mekanizmaları konsolidasyonu",
            "clinicalFocus": "Kapsamlı Bölüm Tekrarı",
            "content": "Bölüm 5 boyunca servikal karsinogenezin tarama prensiplerinden başlayarak histopatolojik displazi basamaklarını ve invaziv karsinomun klinik yayılım paternlerini inceledik.\n\n- **Eksfoliyatif Tarama ve Bethesda:** Pap smear transformasyon zonundan dökülen hücreleri inceler; LSIL sitolojisi histopatolojik olarak CIN 1'e, HSIL ise CIN 2/3'e karşılık gelir.\n- **CIN Histopatolojisi:** CIN 1'de atipi alt 1/3'e sınırlıyken, CIN 3'te tam kat atipi izlenir; ancak bazal membran kesintisiz biçimde intakttır.\n- **Lokal Yayılım ve Mortalite:** İnvaziv karsinom ekzofitik veya endofitik büyüyebilir; parametriyuma lateral yayılım üreterleri tıkayarak bilateral hidronefroza ve en sık ölüm nedeni olan üremiye yol açar.\n\n> [!IMPORTANT]\n> [CHECKPOINT SENTEZİ] CIN 3'te bazal membran sağlamdır; bazal membranı aşan invaziv karsinomda en sık ölüm nedeni parametrial yayılımla üreterlerin tıkanması sonucu gelişen üremidir.",
            "synthesisNarrative": "Bölüm 5 boyunca servikal karsinogenezin tarama prensiplerinden başlayarak histopatolojik displazi basamaklarını ve invaziv karsinomun klinik yayılım paternlerini inceledik.\n\n- **Eksfoliyatif Tarama ve Bethesda:** Pap smear transformasyon zonundan dökülen hücreleri inceler; LSIL sitolojisi histopatolojik olarak CIN 1'e, HSIL ise CIN 2/3'e karşılık gelir.\n- **CIN Histopatolojisi:** CIN 1'de atipi alt 1/3'e sınırlıyken, CIN 3'te tam kat atipi izlenir; ancak bazal membran kesintisiz biçimde intakttır.\n- **Lokal Yayılım ve Mortalite:** İnvaziv karsinom ekzofitik veya endofitik büyüyebilir; parametriyuma lateral yayılım üreterleri tıkayarak bilateral hidronefroza ve en sık ölüm nedeni olan üremiye yol açar.\n\n> [!IMPORTANT]\n> [CHECKPOINT SENTEZİ] CIN 3'te bazal membran sağlamdır; bazal membranı aşan invaziv karsinomda en sık ölüm nedeni parametrial yayılımla üreterlerin tıkanması sonucu gelişen üremidir.",
            "bulletPoints": [
                "Pap smear eksfoliyatif tarama yöntemidir; LSIL CIN 1'e, HSIL CIN 2/3'e karşılık gelir.",
                "CIN 3 tam kat atipidir fakat bazal membran intakttır.",
                "İnvaziv karsinomda parametrial yayılıma bağlı üreter basısı ve üremi en sık ölüm nedenidir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "İnvaziv serviks karsinomunda parametrial yayılıma bağlı olarak en sık ölüm nedeni üremi tablosudur.",
                    "maskedTerm": "üremi",
                    "hint": "Üreter obstrüksiyonu sonucu gelişen postrenal böbrek yetmezliği"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bölüm 5: Serviks Prekanseröz ve Kanseröz Lezyonlar Özeti",
                    "tableHeaders": ["Evre / Tablo", "Temel Histopatolojik Özellik", "Klinik Seyir / Komplikasyon"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "CIN 1 (LSIL)", "isMasked": False},
                                {"text": "Epitelin alt 1/3'ünde atipi ve koilositoz", "isMasked": True, "hint": "hafif displazi katmanı"},
                                {"text": "Yüksek oranda spontan regresyon"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "İnvaziv Karsinom", "isMasked": False},
                                {"text": "Bazal membranın aşılması ve stromal invazyon", "isMasked": True, "hint": "prekanseröz sınırı aşan tümör"},
                                {"text": "Parametriyum tutulumu, üreter basısı ve üremi"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Taramadan Terminal Evreye Servikal Patoloji Zinciri",
                    "steps": [
                        "1. Tarama ve Sitoloji: Pap smear transformasyon zonundan atipik hücreleri yakalar.",
                        "2. Preinvaziv Displazi: Epitel içinde CIN 1-3 basamakları gelişir, bazal membran sağlam kalır.",
                        "3. İnvazyon: Hücreler bazal membranı delerek parametriyuma doğru yayılır.",
                        "4. Komplikasyon: Üreter obstrüksiyonu, bilateral hidronefroz ve ölümcül üremi gelişir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bölüm 5'te işlenen konular ışığında, CIN 3 ile invaziv karsinom arasındaki anatomik sınır ve ileri evre karsinomdaki en yaygın ölüm nedeni nedir?",
                    "answer": "Anatomik sınır bazal membrandır (CIN 3'te sağlam, invaziv karsinomda aşılmış); en sık ölüm nedeni ise üreter obstrüksiyonuna bağlı üremidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Bölüm 5 Genel Tekrar",
                    "items": [
                        {"text": "Pap smear eksfoliyatif sitoloji prensibiyle transformasyon zonunu tarar.", "isLie": False, "explanation": "Doğru. Karsinogenez odağı bu zondur."},
                        {"text": "CIN 3'te atipi tam kata ulaşsa da bazal membran henüz aşılmamıştır.", "isLie": False, "explanation": "Doğru. Aşılırsa invaziv karsinom olur."},
                        {"text": "İleri evre karsinomda en sık ölüm nedeni üreter basısına bağlı üremidir.", "isLie": False, "explanation": "Doğru. Bilateral hidronefroz ve böbrek yetmezliği gelişir."},
                        {"text": "CIN 1 saptanan hastaların %100'ü 24 saat içinde metastaz nedeniyle kaybedilir.", "isLie": True, "explanation": "Tuzak! CIN 1 hafif displazidir, metastaz yapmaz ve olguların çoğunluğu kendiliğinden geriler."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Bölüm 5'te ele alınan konularla ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "CIN 3'te bazal membran sağlamdır; invaziv karsinomda ise parametrial yayılım üreterleri tıkayarak üremiye yol açabilir",
                            "isCorrect": True,
                            "explanation": "Bu sentez cümlesi hem intraepitelyal lezyonun sınırını hem de invaziv karsinomun temel ölüm mekanizmasını doğru özetler."
                        },
                        {
                            "key": "B",
                            "text": "Pap smear sadece menopoz sonrası erkeklerin prostat bezinden alınır",
                            "isCorrect": False,
                            "explanation": "Pap smear kadın serviksinden alınan jinekolojik sitolojidir."
                        },
                        {
                            "key": "C",
                            "text": "Servikal karsinom hiçbir zaman parametriyuma veya lenf nodlarına yayılamaz",
                            "isCorrect": False,
                            "explanation": "En önemli yayılım yolları parametrial dokular ve bölgesel lenfatiklerdir."
                        },
                        {
                            "key": "D",
                            "text": "Keratin incileri yalnızca böbrek tübüllerinde oluşan idrar taşlarıdır",
                            "isCorrect": False,
                            "explanation": "Skuamöz diferansiasyon gösteren karsinomların histolojik bulgusudur."
                        }
                    ]
                }
            ]
        }
    ]
    return slides

if __name__ == '__main__':
    slides = get_s5_slides()
    print(f'Section 5 generated with {len(slides)} slides.')
