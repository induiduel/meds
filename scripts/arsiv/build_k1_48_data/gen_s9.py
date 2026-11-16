import json

def get_s9_slides():
    slides = [
        # S81
        {
            "slideNumber": 81,
            "title": "Alt Genital Traktusta Alan Kanserleşmesi (Field Cancerization)",
            "subtitle": "Multisentrik HPV neoplazileri: CIN, VIN, VAIN ve AIN birlikteliği",
            "clinicalFocus": "Onkolojik Konsept",
            "content": "Kadın alt genital traktusu (serviks, vajina, vulva ve perianal bölge), embriyolojik ve anatomik süreklilik gösteren geniş bir skuamöz epitel sahasıdır. Bu bölgede gözlenen en kritik patolojik fenomenlerden biri **alan kanserleşmesidir (field cancerization)**.\n\n- **Fenomenin Biyolojisi:** Cinsel yolla bulaşan yüksek riskli HPV (özellikle tip 16), yalnızca serviksin transformasyon zonunu değil; aynı anda veya yıllar içinde vajina, vulva ve perianal anoderm epitelini de yaygın biçimde enfekte eder.\n- **Multisentrik Neoplaziler:** Bu durum alt genital traktusun birden fazla anatomik bölgesinde eşzamanlı (senkron) veya farklı zamanlarda (metakron) intraepitelyal neoplazilerin ortaya çıkmasına yol açar: **CIN (serviks), VAIN (vajen), VIN (vulva) ve AIN (anüs)** birlikteliği sıktır.\n- **Klinik Yansıma:** Bir kadında servikal CIN veya karsinom saptandığında, tüm alt genital traktus (vajen forniksleri ve vulva) kolposkopik olarak taranmalıdır; bir odağın tedavi edilmesi diğer alanlardaki riski sıfırlamaz.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Alan kanserleşmesi nedeniyle serviks karsinomu veya CIN öyküsü olan kadınlarda VAIN ve vulvar VIN gelişme riski katbekat artmıştır.",
            "synthesisNarrative": "Kadın alt genital traktusu (serviks, vajina, vulva ve perianal bölge), embriyolojik ve anatomik süreklilik gösteren geniş bir skuamöz epitel sahasıdır. Bu bölgede gözlenen en kritik patolojik fenomenlerden biri **alan kanserleşmesidir (field cancerization)**.\n\n- **Fenomenin Biyolojisi:** Cinsel yolla bulaşan yüksek riskli HPV (özellikle tip 16), yalnızca serviksin transformasyon zonunu değil; aynı anda veya yıllar içinde vajina, vulva ve perianal anoderm epitelini de yaygın biçimde enfekte eder.\n- **Multisentrik Neoplaziler:** Bu durum alt genital traktusun birden fazla anatomik bölgesinde eşzamanlı (senkron) veya farklı zamanlarda (metakron) intraepitelyal neoplazilerin ortaya çıkmasına yol açar: **CIN (serviks), VAIN (vajen), VIN (vulva) ve AIN (anüs)** birlikteliği sıktır.\n- **Klinik Yansıma:** Bir kadında servikal CIN veya karsinom saptandığında, tüm alt genital traktus (vajen forniksleri ve vulva) kolposkopik olarak taranmalıdır; bir odağın tedavi edilmesi diğer alanlardaki riski sıfırlamaz.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Alan kanserleşmesi nedeniyle serviks karsinomu veya CIN öyküsü olan kadınlarda VAIN ve vulvar VIN gelişme riski katbekat artmıştır.",
            "bulletPoints": [
                "Alan kanserleşmesi tüm alt genital traktusu etkileyen yaygın HPV maruziyetidir.",
                "CIN, VAIN, VIN ve AIN lezyonları multisentrik olarak bir arada görülebilir.",
                "Serviks karsinomu öyküsü olan kadınlarda vajina ve vulva titizlikle taranmalıdır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Tüm alt genital traktus epitelinin yaygın karsinojenik HPV maruziyeti sonucu çok odaklı neoplaziler geliştirmesine alan kanserleşmesi adı verilir.",
                    "maskedTerm": "alan kanserleşmesi",
                    "hint": "Field cancerization teriminin Türkçe karşılığı"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Alt Genital Traktusta Multisentrik Neoplaziler",
                    "tableHeaders": ["Anatomik Bölge", "Preinvaziv Neoplazi", "İnvaziv Karsinom"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Uterus Serviksi", "isMasked": False},
                                {"text": "CIN (Servikal İntraepitelyal Neoplazi)", "isMasked": False},
                                {"text": "Servikal Skuamöz Karsinom", "isMasked": True, "hint": "en sık kadın genital kanserlerinden biri"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Vajina Duvarı", "isMasked": False},
                                {"text": "VAIN (Vajinal İntraepitelyal Neoplazi)", "isMasked": True, "hint": "vajen öncü lezyonu"},
                                {"text": "Vajinal Skuamöz Hücreli Karsinom"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Alan Kanserleşmesinde Multisentrik Progresyon",
                    "steps": [
                        "1. Yaygın Enfeksiyon: HPV 16 serviks, vajina forniksleri ve vulva epitelini kaplar.",
                        "2. Servikal Lezyon: İlk olarak transformasyon zonunda CIN 3 gelişir ve tedavi edilir.",
                        "3. Vajinal Progresyon: Yıllar sonra aynı virüs maruziyeti zemininde üst vajinada VAIN belirir.",
                        "4. Bütüncül İzlem: Alan kanserleşmesi bilinciyle hastanın tüm genital traktusu izlenir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Serviks kanseri veya CIN öyküsü olan bir kadında vajina ve vulvada da karsinom gelişme riskinin yüksek olmasını açıklayan temel onkolojik kavram nedir?",
                    "answer": "Alan kanserleşmesi (Field Cancerization); tüm alt genital epitelin aynı onkojenik HPV karsinojenine yaygın olarak maruz kalması fenomenidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Alan Kanserleşmesi",
                    "items": [
                        {"text": "Alan kanserleşmesi alt genital epitelin yaygın HPV maruziyetini ifade eder.", "isLie": False, "explanation": "Doğru. Geniş epitel yüzeyi etkilenir."},
                        {"text": "CIN, VAIN ve VIN lezyonları aynı hastada farklı zamanlarda gelişebilir.", "isLie": False, "explanation": "Doğru. Multisentrik tutulum tipiktir."},
                        {"text": "Serviks karsinomu öyküsü olanlarda vajinal karsinom riski artmıştır.", "isLie": False, "explanation": "Doğru. En büyük risk faktörüdür."},
                        {"text": "Serviks kanseri geçiren bir kadının vulva ve vajinası tümörlere karşı %100 bağışık hale gelir.", "isLie": True, "explanation": "Tuzak! Bağışıklık gelişmez, tam tersine alan kanserleşmesi nedeniyle risk katbekat artar."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Daha önce servikal karsinoma in situ (CIN 3) nedeniyle konizasyon yapılmış bir kadında 5 yıl sonra üst vajina arka duvarında VAIN 3 saptanıyor. Bu durumu en iyi açıklayan onkopatolojik kavram hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Alan kanserleşmesi (Field Cancerization) ve multisentrik HPV maruziyeti",
                            "isCorrect": True,
                            "explanation": "Tüm alt genital traktusun aynı onkojenik etkene maruz kalmasıyla farklı odaklarda neoplazi gelişmesidir."
                        },
                        {
                            "key": "B",
                            "text": "Hastanın diyetinde aşırı miktarda C vitamini bulunması",
                            "isCorrect": False,
                            "explanation": "C vitamini displazi yapmaz."
                        },
                        {
                            "key": "C",
                            "text": "Böbrek taşı dökülmesinin vajinayı tahrip etmesi",
                            "isCorrect": False,
                            "explanation": "Üriner taş neoplazi nedeni değildir."
                        },
                        {
                            "key": "D",
                            "text": "Tamamen rastlantısal bir deri çillenmesi",
                            "isCorrect": False,
                            "explanation": "VAIN 3 yüksek dereceli premalign lezyondur, çil değildir."
                        }
                    ]
                }
            ]
        },
        # S82
        {
            "slideNumber": 82,
            "title": "İmmün Yetmezlikli Hastalarda HPV Agresyonu ve Hızlı Progresyon",
            "subtitle": "HIV enfeksiyonu, organ nakli ve sitotoksik T hücre yetersizliği",
            "clinicalFocus": "İmmünsüpresyon ve Karsinogenez",
            "content": "Ders notunda belirtildiği üzere, HPV ilişkili prekanseröz lezyonların (VIN, CIN, VAIN) ve invaziv karsinomların gelişiminde **immün sistemin baskılanması** en kritik hızlandırıcı faktördür.\n\n- **Hücresel Bağışıklığın Rolü:** Sağlıklı bireylerde CD4+ ve CD8+ sitotoksik T lenfositler HPV enfeksiyonunun %80-90'ını 1-2 yıl içinde kontrol altına alıp temizler. İmmün yetmezlikte ise viral klerens durur ve persistan enfeksiyon kalıcılaşır.\n- **HIV Pozitif Hastalar:** HIV enfeksiyonunda CD4+ T hücrelerinin tükenmesi, HPV E6 ve E7 onkoproteinlerinin kontrolsüz ekspresyonuna yol açar. Bu hastalarda CIN lezyonları olağanüstü yüksek sıklıkta görülür, tedaviye dirençlidir ve invaziv karsinoma progresyon süresi 10-15 yıldan birkaç yıla kadar kısalır.\n- **Organ Nakli Alıcıları:** Kronik immünsüpresif ilaç (siklosporin, takrolimus vb.) kullanan böbrek veya karaciğer nakilli hastalarda anogenital siğiller ve karsinom insidansı normal popülasyondan 10-30 kat daha yüksektir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] HIV pozitif ve immünsüpresif tedavi alan kadınlarda persistan HPV enfeksiyonu, yüksek dereceli displazi ve hızlı invaziv karsinom gelişimi dramatik olarak artar.",
            "synthesisNarrative": "Ders notunda belirtildiği üzere, HPV ilişkili prekanseröz lezyonların (VIN, CIN, VAIN) ve invaziv karsinomların gelişiminde **immün sistemin baskılanması** en kritik hızlandırıcı faktördür.\n\n- **Hücresel Bağışıklığın Rolü:** Sağlıklı bireylerde CD4+ ve CD8+ sitotoksik T lenfositler HPV enfeksiyonunun %80-90'ını 1-2 yıl içinde kontrol altına alıp temizler. İmmün yetmezlikte ise viral klerens durur ve persistan enfeksiyon kalıcılaşır.\n- **HIV Pozitif Hastalar:** HIV enfeksiyonunda CD4+ T hücrelerinin tükenmesi, HPV E6 ve E7 onkoproteinlerinin kontrolsüz ekspresyonuna yol açar. Bu hastalarda CIN lezyonları olağanüstü yüksek sıklıkta görülür, tedaviye dirençlidir ve invaziv karsinoma progresyon süresi 10-15 yıldan birkaç yıla kadar kısalır.\n- **Organ Nakli Alıcıları:** Kronik immünsüpresif ilaç (siklosporin, takrolimus vb.) kullanan böbrek veya karaciğer nakilli hastalarda anogenital siğiller ve karsinom insidansı normal popülasyondan 10-30 kat daha yüksektir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] HIV pozitif ve immünsüpresif tedavi alan kadınlarda persistan HPV enfeksiyonu, yüksek dereceli displazi ve hızlı invaziv karsinom gelişimi dramatik olarak artar.",
            "bulletPoints": [
                "Sitotoksik T hücreleri HPV viral klerensinde temel savunmadır.",
                "HIV pozitiflerde ve organ nakillilerde HPV persistan kalır.",
                "Displaziler hızla invaziv karsinoma ilerler ve nüks sıktır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Hücresel immün yetmezliği olan HIV pozitif hastalarda HPV viral klerensi bozulduğundan persistan enfeksiyon kalıcı hale gelir.",
                    "maskedTerm": "persistan enfeksiyon",
                    "hint": "Virüsün vücuttan atılamayıp dokuda sürekli çoğalması tablosu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "İmmün Durumun HPV Seyrine Etkisi",
                    "tableHeaders": ["İmmün Durum", "Viral Klerens Oranı", "Karsinoma Progresyon Hızı"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "İmmün Yetkin (Normal)", "isMasked": False},
                                {"text": "%80 - 90 temizlenir (1-2 yılda)", "isMasked": True, "hint": "yüksek spontan regresyon"},
                                {"text": "Yavaş (10-20 yıllık süreç)"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "İmmün Yetmezlik (HIV / Nakil)", "isMasked": False},
                                {"text": "Viral klerens neredeyse yok", "isMasked": False},
                                {"text": "Çok hızlı (birkaç yıl içinde invazyon)", "isMasked": True, "hint": "agresif ve hızlanmış malign transformasyon"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "İmmünsüpresyondan Hızlı Karsinoma Yolak",
                    "steps": [
                        "1. İmmün Baskılanma: CD4+ T hücreleri tükenir veya ilaçla bloke edilir.",
                        "2. Viral Klerens Kaybı: HPV enfeksiyonu epitel hücrelerinde kalıcılaşır.",
                        "3. Onkogen Aktivasyonu: E6 ve E7 p53/Rb'yi denetimsizce yıkarak mutasyonları artırır.",
                        "4. Hızlı İnvazyon: CIN lezyonları yıllar yerine aylar içinde invaziv karsinoma dönüşür."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "HIV enfeksiyonu veya organ nakli gibi hücresel immün yetmezlik durumlarında HPV ilişkili lezyonların klinik seyrini değiştiren temel mekanizma nedir?",
                    "answer": "Sitotoksik T hücre yetersizliği nedeniyle viral klerensin durması, HPV enfeksiyonunun persistan hale gelmesi ve displazinin çok hızlı invaziv karsinoma ilerlemesidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "İmmün Yetmezlik ve HPV",
                    "items": [
                        {"text": "İmmün yetmezlikte HPV enfeksiyonunun spontan gerilemesi belirgin azalır.", "isLie": False, "explanation": "Doğru. Viral klerens bozulur."},
                        {"text": "HIV pozitif kadınlarda CIN ve serviks kanseri riski dramatik artar.", "isLie": False, "explanation": "Doğru. AIDS tanımlayıcı malignitedir."},
                        {"text": "Organ nakli alıcılarında genital siğil ve kanser sıklığı yüksektir.", "isLie": False, "explanation": "Doğru. İlaçlara bağlı risk artar."},
                        {"text": "İmmün sistemi çöken bireylerde HPV virüsleri 5 saniyede kendiliğinden ölür.", "isLie": True, "explanation": "Tuzak! İmmünite çökerse virüs ölemez, tam tersine kontrolsüzce çoğalır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Böbrek nakli nedeniyle yüksek doz immünsüpresif tedavi alan 40 yaşındaki bir kadında genital lezyonlar açısından en olası patolojik risk hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Persistan HPV enfeksiyonu ve çok hızlı ilerleyen multifokal intraepitelyal neoplaziler",
                            "isCorrect": True,
                            "explanation": "İmmünsüpresyon HPV temizlenmesini engeller ve displazi progresyonunu hızlandırır."
                        },
                        {
                            "key": "B",
                            "text": "Tüm genital kanserlere karşı doğuştan tam bağışıklık kazanılması",
                            "isCorrect": False,
                            "explanation": "İmmünsüpresyon kanser riskini artırır."
                        },
                        {
                            "key": "C",
                            "text": "Serviksin aniden saf kemik dokusuna dönüşmesi",
                            "isCorrect": False,
                            "explanation": "Biyolojik olarak imkansızdır."
                        },
                        {
                            "key": "D",
                            "text": "Hiçbir enfeksiyon etkeninin vücuda girememesi",
                            "isCorrect": False,
                            "explanation": "Tam tersine enfeksiyonlara aşırı duyarlılık oluşur."
                        }
                    ]
                }
            ]
        },
        # S83
        {
            "slideNumber": 83,
            "title": "Gebelikte Servikal ve Vajinal Sitolojik Değişiklikler",
            "subtitle": "Arias-Stella reaksiyonu, desidual dönüşüm ve naviküler hücre hakimiyeti",
            "clinicalFocus": "Gebelik Fizyopatolojisi ve Sitoloji",
            "content": "Gebelik sırasında yükselen devasa **progesteron ve östrojen hormonları**, serviks ve vajina epitelinde dramatik fizyolojik değişiklikler yaratarak deneyimsiz gözler için sitopatolojik tuzaklara yol açar.\n\n- **Naviküler Hücre Hakimiyeti:** Progesteron etkisiyle ara (intermediyer) tabaka skuamöz hücreleri yoğun glikojen depolar. Hücreler kenarları kıvrık kayık benzeri bir şekil alır; bunlara **naviküler hücreler** adı verilir ve gebelik sitolojisinin en belirgin bulgusudur.\n- **Desidual Reaksiyon:** Servikal ve endometriyal stromada progesteron etkisiyle mezenkimal hücreler genişler; bol eozinofilik sitoplazmalı, yuvarlak nükleuslu desidua hücrelerine dönüşür. Biyopside veya smear zemininde karsinomla karıştırılmamalıdır.\n- **Arias-Stella Reaksiyonu:** Endoservikal bezlerde aşırı hormonal uyarım sonucu hücrelerde nükleer büyüme, hiperkromazi ve intrastromal vakuolizasyon gelişir; maligniteyi taklit edebilen selim bir gebelik reaksiyonudur.\n\n> [!NOTE]\n> Gebelik sitolojisinde izlenen naviküler hücreler ve desidual psödoatipi tamamen hormonal olup karsinom ile karıştırılmamalıdır.",
            "synthesisNarrative": "Gebelik sırasında yükselen devasa **progesteron ve östrojen hormonları**, serviks ve vajina epitelinde dramatik fizyolojik değişiklikler yaratarak deneyimsiz gözler için sitopatolojik tuzaklara yol açar.\n\n- **Naviküler Hücre Hakimiyeti:** Progesteron etkisiyle ara (intermediyer) tabaka skuamöz hücreleri yoğun glikojen depolar. Hücreler kenarları kıvrık kayık benzeri bir şekil alır; bunlara **naviküler hücreler** adı verilir ve gebelik sitolojisinin en belirgin bulgusudur.\n- **Desidual Reaksiyon:** Servikal ve endometriyal stromada progesteron etkisiyle mezenkimal hücreler genişler; bol eozinofilik sitoplazmalı, yuvarlak nükleuslu desidua hücrelerine dönüşür. Biyopside veya smear zemininde karsinomla karıştırılmamalıdır.\n- **Arias-Stella Reaksiyonu:** Endoservikal bezlerde aşırı hormonal uyarım sonucu hücrelerde nükleer büyüme, hiperkromazi ve intrastromal vakuolizasyon gelişir; maligniteyi taklit edebilen selim bir gebelik reaksiyonudur.\n\n> [!NOTE]\n> Gebelik sitolojisinde izlenen naviküler hücreler ve desidual psödoatipi tamamen hormonal olup karsinom ile karıştırılmamalıdır.",
            "bulletPoints": [
                "Progesteron etkisiyle glikojen yüklü naviküler hücreler baskınlaşır.",
                "Servikal stromada desidual dönüşüm karsinomu taklit edebilir.",
                "Arias-Stella reaksiyonu hormonal bir selim bez atipisidir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Gebelikte progesteron etkisiyle ara tabaka hücrelerinin glikojen depolayarak kayık şeklini almasına naviküler hücreler adı verilir.",
                    "maskedTerm": "naviküler hücreler",
                    "hint": "Gebelikte smear yaymasında baskın kayıksı epitel hücreleri"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Gebelik İlişkili Sitolojik Değişiklikler",
                    "tableHeaders": ["Hücresel Tablo", "Hormonal Tetikleyici", "Morfolojik Görünüm"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Naviküler Hücreler", "isMasked": False},
                                {"text": "Yüksek Progesteron", "isMasked": False},
                                {"text": "Kayık şeklinde, kenarları kıvrık, bol glikojenli", "isMasked": True, "hint": "sarımsı sitoplazmalı ara hücreler"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Arias-Stella Reaksiyonu", "isMasked": False},
                                {"text": "Gebelik hormonları (HCG / Progesteron)", "isMasked": True, "hint": "trofoblastik hormonal uyarı"},
                                {"text": "Bez epitelinde psödomalign nükleer büyüme"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Gebelikte Progesterondan Naviküler Hücreye",
                    "steps": [
                        "1. Korpus Luteum / Plasenta: Yüksek miktarda progesteron hormonu salgılanır.",
                        "2. Matürasyon Durgunluğu: Skuamöz epitel tam yüzeyel evreye geçmeden ara evrede durur.",
                        "3. Glikojen Yüklenmesi: Hücre sitoplazması glikojenle dolar ve kenarları katlanır.",
                        "4. Naviküler Yayma: Pap smear yaymasında kümeleşmiş naviküler hücreler sitoloğa gebeliği düşündürür."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Gebelik dönemindeki servikal sitolojide progesteron etkisiyle ortaya çıkan ve yoğun glikojen içeren kayık şeklindeki tipik hücrelere ne ad verilir?",
                    "answer": "Naviküler hücreler (navicular cells)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Gebelikte Sitolojik Değişiklikler",
                    "items": [
                        {"text": "Naviküler hücreler glikojenden zengin ara tabaka hücreleridir.", "isLie": False, "explanation": "Doğru. Progesteron etkisidir."},
                        {"text": "Servikal stromada desidual dönüşüm görülebilir.", "isLie": False, "explanation": "Doğru. Hormonal stroma yanıtıdır."},
                        {"text": "Arias-Stella reaksiyonu maligniteyi taklit edebilen selim bir durumdur.", "isLie": False, "explanation": "Doğru. Glandüler hormonal reaksiyondur."},
                        {"text": "Gebelikte tüm vajina epitel hücreleri derhal yok olarak kemik dokusuna döner.", "isLie": True, "explanation": "Tuzak! Gebelikte epitel hücreleri korunur ve glikojen depolar."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Gebe bir kadından alınan rutin servikal sitolojide bol glikojen içeren, kenarları katlanmış kayık şeklinde hücreler saptanıyor. Bu sitolojik bulgu aşağıdakilerden hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Naviküler hücreler (progesteron etkisine bağlı fizyolojik gebelik sitolojisi)",
                            "isCorrect": True,
                            "explanation": "Gebelikte progesteron etkisiyle glikojen dolu naviküler hücreler belirginleşir."
                        },
                        {
                            "key": "B",
                            "text": "Akut apandisit irin hücreleri",
                            "isCorrect": False,
                            "explanation": "Apandisit bulgusu değildir."
                        },
                        {
                            "key": "C",
                            "text": "Malign osteosarkom osteoblastları",
                            "isCorrect": False,
                            "explanation": "Kemik tümörü hücresi değildir."
                        },
                        {
                            "key": "D",
                            "text": "Karaciğer safra kristalleri",
                            "isCorrect": False,
                            "explanation": "Safra yolları bulgusudur."
                        }
                    ]
                }
            ]
        },
        # S84
        {
            "slideNumber": 84,
            "title": "Gebelikte Candida ve CYBH Yönetimi Güvenliği",
            "subtitle": "Glikojen artışının fungal yatkınlığı, topikal tedavi ve yenidoğan geçişi",
            "clinicalFocus": "Gebelik Enfeksiyonları",
            "content": "Ders notunda belirtildiği üzere, gebelik fizyolojisinde ortaya çıkan glikojen zenginliği ve hormonal durum, belirli mikroorganizmalar için mükemmel bir üreme ortamı oluşturur.\n\n- **Gebelikte Candida Patogenezi:** Yüksek östrojen ve progesteron vajinal epitelde yoğun glikojen birikimi sağlar; bu glikojen laktobasillerce laktik aside dönüştürülse de, Candida mantarları asidik ve glikojenli ortamı çok sever. Bu nedenle **semptomatik Candida vajiniti gebelikte en sık görülen enfeksiyondur**.\n- **Tedavi Güvenliği:** Gebelikte sistemik oral azoller teratojenik risk nedeniyle tercih edilmez; güvenli **topikal klotrimazol veya mikonazol** fitilleri kullanılır.\n- **Yenidoğan Geçiş Riski:** Doğum kanalından geçerken bebeğe bulaşabilen etkenler (**HSV, Gonokok ve Klamidya**) yenidoğanda körlük (oftalmiya neonatorum) veya dissemine neonatal herpes yapabileceğinden doğum öncesi kesin tanı ve tedavi şarttır.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Gebelerde aktif genital herpes (HSV) lezyonları varlığında neonatal herpes ve ölüm riskini önlemek için vajinal doğum yerine sezaryen doğum tercih edilir.",
            "synthesisNarrative": "Ders notunda belirtildiği üzere, gebelik fizyolojisinde ortaya çıkan glikojen zenginliği ve hormonal durum, belirli mikroorganizmalar için mükemmel bir üreme ortamı oluşturur.\n\n- **Gebelikte Candida Patogenezi:** Yüksek östrojen ve progesteron vajinal epitelde yoğun glikojen birikimi sağlar; bu glikojen laktobasillerce laktik aside dönüştürülse de, Candida mantarları asidik ve glikojenli ortamı çok sever. Bu nedenle **semptomatik Candida vajiniti gebelikte en sık görülen enfeksiyondur**.\n- **Tedavi Güvenliği:** Gebelikte sistemik oral azoller teratojenik risk nedeniyle tercih edilmez; güvenli **topikal klotrimazol veya mikonazol** fitilleri kullanılır.\n- **Yenidoğan Geçiş Riski:** Doğum kanalından geçerken bebeğe bulaşabilen etkenler (**HSV, Gonokok ve Klamidya**) yenidoğanda körlük (oftalmiya neonatorum) veya dissemine neonatal herpes yapabileceğinden doğum öncesi kesin tanı ve tedavi şarttır.\n\n> [!IMPORTANT]\n> [KLİNİK İPUCU] Gebelerde aktif genital herpes (HSV) lezyonları varlığında neonatal herpes ve ölüm riskini önlemek için vajinal doğum yerine sezaryen doğum tercih edilir.",
            "bulletPoints": [
                "Glikojen artışı gebelikte Candida vajiniti sıklığını belirgin artırır.",
                "Gebelikte sistemik yerine güvenli topikal tedaviler uygulanır.",
                "Aktif genital HSV varlığında yenidoğanı korumak için sezaryen uygulanır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Gebelikte epiteldeki yoğun glikojen birikimi Candida vajiniti gelişme sıklığını belirgin biçimde artırır.",
                    "maskedTerm": "Candida vajiniti",
                    "hint": "Kalın peynirimsi akıntı ve kaşıntıyla seyreden fungal enfeksiyon"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Gebelikte Enfeksiyon ve Yönetim İlkeleri",
                    "tableHeaders": ["Patojen", "Gebelikteki Klinik Önemi", "Güvenli Yaklaşım"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Candida albicans", "isMasked": False},
                                {"text": "Glikojen artışıyla şiddetli semptomatik alevlenme", "isMasked": True, "hint": "peynirimsi yoğun akıntı"},
                                {"text": "Topikal azol fitilleri (sistemik ilaçtan kaçınılır)"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Genital Herpes (HSV)", "isMasked": False},
                                {"text": "Yenidoğanda ölümcül dissemine enfeksiyon", "isMasked": True, "hint": "bebeğe geçiş riski"},
                                {"text": "Aktif lezyon varlığında sezaryen doğum"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Aktif Genital HSV ve Sezaryen Kararı",
                    "steps": [
                        "1. Term Gebe: Doğum eylemi başlayan kadının vulvasında ağrılı veziküller görülür.",
                        "2. Risk Analizi: Vajinal doğum sırasında bebeğin lezyonla teması ölümcül neonatal herpes riski taşır.",
                        "3. Doğum Kararı: Vajinal doğum iptal edilerek acil sezaryen operasyonuna geçilir.",
                        "4. Bebek Koruması: Bebek enfekte maternal dokuya temas etmeden steril doğurtulur."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Doğum anında annede aktif vulvovajinal Herpes Simplex (HSV) lezyonları saptandığında yenidoğanı korumak için hangi doğum yöntemi tercih edilir?",
                    "answer": "Sezaryen doğum; bebeğin doğum kanalındaki enfekte veziküllerle temasını engelleyerek ölümcül neonatal herpes gelişimini önler."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Gebelikte Enfeksiyon Yönetimi",
                    "items": [
                        {"text": "Candida vajiniti gebelikte yoğun glikojen nedeniyle sıklaşır.", "isLie": False, "explanation": "Doğru. Amfi notunun temel vurgusudur."},
                        {"text": "Gebelikte antifungal tedavide topikal fitiller tercih edilir.", "isLie": False, "explanation": "Doğru. Fetal güvenlik için esastır."},
                        {"text": "Aktif HSV lezyonları olan gebelerde sezaryen doğum endikedir.", "isLie": False, "explanation": "Doğru. Bebeği korumak için uygulanır."},
                        {"text": "Gebe kadınlara genital mantar tedavisi için yüksek doz radyoaktif kobalt verilir.", "isLie": True, "explanation": "Tuzak! Gebe kadına radyasyon veya kobalt verilemez; basit topikal ilaçlar kullanılır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "38 haftalık gebe bir kadında labiumlarda şiddetli ağrılı vezikülo-ülseratif lezyonlar saptanıyor ve Tzanck yaymasında HSV doğrulanıyor. Yenidoğan sağlığı açısından en doğru yaklaşım nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Doğum kanalından geçiş sırasında ölümcül neonatal herpes riskini önlemek için sezaryen doğum tercih etmek",
                            "isCorrect": True,
                            "explanation": "Aktif genital lezyon varlığında neonatal herpesi önlemenin yolu sezaryendir."
                        },
                        {
                            "key": "B",
                            "text": "Hiçbir önlem almadan evde kendi kendine doğum yapmasını beklemek",
                            "isCorrect": False,
                            "explanation": "Bebek için hayati tehlike yaratır."
                        },
                        {
                            "key": "C",
                            "text": "Lezyonların üzerine benzin döküp yakmak",
                            "isCorrect": False,
                            "explanation": "Tıbbi değeri olmayan zararlı bir eylemdir."
                        },
                        {
                            "key": "D",
                            "text": "Bebeği doğar doğmaz doğrudan kemik iliği nakline almak",
                            "isCorrect": False,
                            "explanation": "Yenidoğan herpes profilaksisi bu değildir."
                        }
                    ]
                }
            ]
        },
        # S85
        {
            "slideNumber": 85,
            "title": "Postpartum ve Postkoital Kanamalarda Patolojik Ayırıcı Tanı Ağacı",
            "subtitle": "Servikal karsinom, endoservikal polip, ektropiyon ve vajinal laserasyonlar",
            "clinicalFocus": "Semptom Temelli Ayırıcı Tanı",
            "content": "Jinekolojik pratikte **postkoital kanama (cinsel ilişki sonrası kanama)** ve **postpartum anormal kanama**, aksi kanıtlanana kadar malignite şüphesiyle yaklaşılması gereken temel semptomlardır.\n\n- **Servikal Karsinom:** Postkoital kanamanın ekarte edilmesi gereken en kritik malign nedenidir. Ekzofitik kırılgan kitleler veya ülseratif endofitik tümörler mekanik temasla kolayca kanar.\n- **Endoservikal Polip:** Kanal içinden sarkan, aşırı damarlı ve ödemli stroma içeren polipler koitus travmasıyla temas kanaması yapan en sık **benign neoplastik/polipoid** nedendir.\n- **Ektropiyon (Erozyon):** Endoservikal narin tek katlı epitelin dışa taştığı alanlar temasla hızla kapiller kanama sızdırır.\n- **Vajinal Laserasyonlar ve Enfeksiyonlar:** Şiddetli Trichomonas veya Candida vajinitinde mukozal erozyonlar kanayabilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Postkoital kanama ile başvuran bir kadında spekulum muayenesi ve servikal sitoloji/biyopsi ile ilk dışlanması gereken patoloji servikal skuamöz hücreli karsinomdur.",
            "synthesisNarrative": "Jinekolojik pratikte **postkoital kanama (cinsel ilişki sonrası kanama)** ve **postpartum anormal kanama**, aksi kanıtlanana kadar malignite şüphesiyle yaklaşılması gereken temel semptomlardır.\n\n- **Servikal Karsinom:** Postkoital kanamanın ekarte edilmesi gereken en kritik malign nedenidir. Ekzofitik kırılgan kitleler veya ülseratif endofitik tümörler mekanik temasla kolayca kanar.\n- **Endoservikal Polip:** Kanal içinden sarkan, aşırı damarlı ve ödemli stroma içeren polipler koitus travmasıyla temas kanaması yapan en sık **benign neoplastik/polipoid** nedendir.\n- **Ektropiyon (Erozyon):** Endoservikal narin tek katlı epitelin dışa taştığı alanlar temasla hızla kapiller kanama sızdırır.\n- **Vajinal Laserasyonlar ve Enfeksiyonlar:** Şiddetli Trichomonas veya Candida vajinitinde mukozal erozyonlar kanayabilir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Postkoital kanama ile başvuran bir kadında spekulum muayenesi ve servikal sitoloji/biyopsi ile ilk dışlanması gereken patoloji servikal skuamöz hücreli karsinomdur.",
            "bulletPoints": [
                "Postkoital kanamada ilk ekarte edilmesi gereken hastalık serviks kanseridir.",
                "En sık benign nedenler endoservikal polip ve ektropiyondur.",
                "Spekulum muayenesi ve hedefe yönelik biyopsi tanı koydurur."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Cinsel ilişki sonrasında görülen kanamalarda ilk dışlanması gereken malign patoloji servikal skuamöz karsinom lezyonudur.",
                    "maskedTerm": "servikal skuamöz karsinom",
                    "hint": "Serviksin en sık görülen temasla kanayan epiteliyal kanseri"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Postkoital Kanama Ayırıcı Tanı Ağacı",
                    "tableHeaders": ["Patoloji", "Biyolojik Doğası", "Morfolojik Mekanizma"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "İnvaziv Serviks Karsinomu", "isMasked": False},
                                {"text": "Malign epitelyal neoplazi", "isMasked": False},
                                {"text": "Kırılgan tümör damarları ve ekzofitik kitle nekrozu", "isMasked": True, "hint": "tümör dokusunun temasla dağılması"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Endoservikal Polip", "isMasked": False},
                                {"text": "Benign polipoid hiperplazi", "isMasked": True, "hint": "selim kitle"},
                                {"text": "Ödemli ve genişlemiş damarların travmatize olması"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Postkoital Kanamadan Kesin Tanıya",
                    "steps": [
                        "1. Şikayet: Hasta her cinsel ilişki sonrası taze parlak kırmızı kanama tarifler.",
                        "2. Spekulum Muayenesi: Serviks ektoserviksinde kanamalı ekzofitik kabarıklık izlenir.",
                        "3. Biyopsi: Kitle üzerinden punch biyopsi örneği alınarak fiksatif içine konur.",
                        "4. Histopatolojik Ayrım: Karsinom, polip veya ektropiyon tanısı netleştirilir."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Postkoital kanama şikayetiyle başvuran bir kadında jinekolojik ve patolojik olarak mutlaka ekarte edilmesi gereken en tehlikeli lezyon nedir?",
                    "answer": "Servikal karsinomdur (invaziv skuamöz hücreli karsinom veya adenokarsinom)."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Postkoital Kanama Ayırıcı Tanısı",
                    "items": [
                        {"text": "Postkoital kanamada serviks kanseri mutlaka ekarte edilmelidir.", "isLie": False, "explanation": "Doğru. En kritik malignitedir."},
                        {"text": "Endoservikal polipler sık görülen benign temas kanaması nedenidir.", "isLie": False, "explanation": "Doğru. Damardan zengin stroma kanar."},
                        {"text": "Ektropiyon narin bez epitelinin dışa taşmasıyla kanama yapabilir.", "isLie": False, "explanation": "Doğru. Mekanik temasla sızdırır."},
                        {"text": "Postkoital kanama daima burun kemiğindeki eğrilikten kaynaklanan bir üst solunum yolu kanamasıdır.", "isLie": True, "explanation": "Tuzak! Postkoital kanama alt genital traktus ve serviks kaynaklı jinekolojik kanamadır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "45 yaşında bir kadın son 3 aydır her cinsel ilişki sonrasında lekelenme tarzında vajinal kanama şikayetiyle başvuruyor. Bu hastada patolojik olarak ilk ekarte edilmesi gereken tanı nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "İnvaziv servikal karsinom",
                            "isCorrect": True,
                            "explanation": "Postkoital kanamanın ekarte edilmesi gereken birincil ve en ölümcül nedeni serviks karsinomudur."
                        },
                        {
                            "key": "B",
                            "text": "Akut glomerülonefrit",
                            "isCorrect": False,
                            "explanation": "Böbrek patolojisidir."
                        },
                        {
                            "key": "C",
                            "text": "Diş eti iltihabı",
                            "isCorrect": False,
                            "explanation": "Ağız boşluğu hastalığıdır."
                        },
                        {
                            "key": "D",
                            "text": "Bacakta venöz varis genişlemesi",
                            "isCorrect": False,
                            "explanation": "Vajinal temas kanaması yapmaz."
                        }
                    ]
                }
            ]
        },
        # S86
        {
            "slideNumber": 86,
            "title": "Sitopatolojide Artefaktlar ve Yanıltıcı Bulgular",
            "subtitle": "Hava kuruması, kan ve aşırı lökosit örtüsü, sitoliz ve tanısal tuzaklar",
            "clinicalFocus": "Tanısal Kalite ve Güvenlik",
            "content": "Servikovajinal Pap smear incelemelerinde patoloğun karşılaştığı en büyük engel, yayma ve fiksasyon hatalarına bağlı gelişen **artefaktlardır (teknik yanıltıcılar)**.\n\n- **Hava Kuruması Artefaktı (Air-Drying):** Yayma yapıldıktan sonra lam derhal alkol fiksatifine konmazsa hücreler saniyeler içinde kurur. Nükleuslar şişer, kromatin detayı silinir ve sahte bir nükleer büyüme/atipi görüntüsü ortaya çıkarak yanlış HSIL teşhisine yol açabilir.\n- **Aşırı Kan ve İnflamatuar Örtü:** Şiddetli akut vajinit veya aktif kanama sırasında alınan yaymalarda epitel hücreleri yoğun eritrosit ve parçalanmış nötrofil yığınları altında kalır; alttaki displastik hücreler maskelenerek yalancı negatiflik doğar.\n- **Döderlein Sitolizi:** Fazla laktobasiller intermediyer hücrelerin sitoplazmasını eriterek çıplak nükleus yığınları bırakır; bu çıplak nükleuslar atipik hücrelerle karıştırılmamalıdır.\n\n> [!NOTE]\n> Hatalı hazırlanmış veya aşırı kuruma artefaktı içeren yaymalar 'değerlendirme için yetersiz' kabul edilmeli ve zorlama yorum yapılmadan smear tekrarlanmalıdır.",
            "synthesisNarrative": "Servikovajinal Pap smear incelemelerinde patoloğun karşılaştığı en büyük engel, yayma ve fiksasyon hatalarına bağlı gelişen **artefaktlardır (teknik yanıltıcılar)**.\n\n- **Hava Kuruması Artefaktı (Air-Drying):** Yayma yapıldıktan sonra lam derhal alkol fiksatifine konmazsa hücreler saniyeler içinde kurur. Nükleuslar şişer, kromatin detayı silinir ve sahte bir nükleer büyüme/atipi görüntüsü ortaya çıkarak yanlış HSIL teşhisine yol açabilir.\n- **Aşırı Kan ve İnflamatuar Örtü:** Şiddetli akut vajinit veya aktif kanama sırasında alınan yaymalarda epitel hücreleri yoğun eritrosit ve parçalanmış nötrofil yığınları altında kalır; alttaki displastik hücreler maskelenerek yalancı negatiflik doğar.\n- **Döderlein Sitolizi:** Fazla laktobasiller intermediyer hücrelerin sitoplazmasını eriterek çıplak nükleus yığınları bırakır; bu çıplak nükleuslar atipik hücrelerle karıştırılmamalıdır.\n\n> [!NOTE]\n> Hatalı hazırlanmış veya aşırı kuruma artefaktı içeren yaymalar 'değerlendirme için yetersiz' kabul edilmeli ve zorlama yorum yapılmadan smear tekrarlanmalıdır.",
            "bulletPoints": [
                "Hava kuruması nükleusları yapay olarak büyüterek displaziyi taklit eder.",
                "Kan ve nötrofil örtüsü displastik hücreleri gizleyerek yalancı negatiflik yapar.",
                "Değerlendirilemeyen yaymalar yetersiz raporlanıp tekrarlanmalıdır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Pap smear yaymasının hemen alkole atılmayıp havada kuruması sonucu oluşan yalancı nükleer büyüme tablosuna hava kuruması artefaktı adı verilir.",
                    "maskedTerm": "hava kuruması",
                    "hint": "Fiksasyon gecikmesiyle hücrelerin şişmesi durumu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Sitopatolojik Artefaktlar ve Sonuçları",
                    "tableHeaders": ["Artefakt Nedeni", "Mikroskobik Görünüm", "Yol Açtığı Tanısal Hata"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Hava Kuruması (Fiksasyon Gecikmesi)", "isMasked": False},
                                {"text": "Şişmiş, soluk, detayını kaybetmiş nükleuslar", "isMasked": True, "hint": "şişkin çekirdek görüntüsü"},
                                {"text": "Yalancı pozitiflik (yanlışlıkla HSIL tanısı)"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Masif Kan / Pürülan Eksüda", "isMasked": False},
                                {"text": "Yoğun eritrosit ve nötrofil kümesi", "isMasked": False},
                                {"text": "Yalancı negatiflik (kanser hücrelerinin örtülmesi)", "isMasked": True, "hint": "malign hücrelerin gizlenmesi"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Hatalı Fiksasyondan Yanlış Teşhise",
                    "steps": [
                        "1. Sürüntü Alma: Spatül ile serviksten toplanan hücreler lama yayılır.",
                        "2. Fiksasyon Gecikmesi: Lam masada dakikalarca bekletilerek havayla kurur.",
                        "3. Nükleer Şişme: Su kaybı ve osmotik stres nükleusu yapay olarak büyütür.",
                        "4. Hatalı Yorum: Patolog şişmiş nükleusu gerçek displazi sanma riskiyle karşılaşır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Servikal Pap smear yaymasında fiksasyonun gecikmesi sonucu ortaya çıkan hava kuruması artefaktı mikroskopide hangi hücresel yanılgıya yol açabilir?",
                    "answer": "Hücre çekirdeklerinin şişmesine ve soluklaşmasına yol açarak benign hücrelerin yanlışlıkla displazik/neoplastik (HSIL) sanılmasına neden olabilir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Sitolojik Artefaktlar",
                    "items": [
                        {"text": "Hava kuruması nükleusları yapay olarak büyütebilir.", "isLie": False, "explanation": "Doğru. Tipik fiksasyon artefaktıdır."},
                        {"text": "Masif lökosit ve kan örtüsü displastik hücreleri gizleyebilir.", "isLie": False, "explanation": "Doğru. Yalancı negatifliğe yol açar."},
                        {"text": "Artefaktlı yetersiz yaymalarda smear testi tekrarlanmalıdır.", "isLie": False, "explanation": "Doğru. Kalite kontrol kuralıdır."},
                        {"text": "Hava kuruması artefaktı olan hücreler mikroskop altında şarkı söylemeye başlar.", "isLie": True, "explanation": "Tuzak! Hücreler ses çıkaramaz; yalnızca optik mikroskobik morfoloji bozulur."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Pap smear yayması hazırlandıktan sonra hemen fiksatif içine konmayıp havada kurumaya bırakılan bir preparatta hangi artefakt gelişir ve neye yol açar?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Hava kuruması artefaktı gelişir; nükleuslar şişerek yalancı displazi (atipi) şüphesine yol açabilir",
                            "isCorrect": True,
                            "explanation": "Hava kuruması nükleer şişmeye ve kromatin kaybına neden olarak sahte atipi oluşturur."
                        },
                        {
                            "key": "B",
                            "text": "Tüm hücreler derhal canlı balıklara dönüşür",
                            "isCorrect": False,
                            "explanation": "Biyolojik saçmalıktır."
                        },
                        {
                            "key": "C",
                            "text": "Preparat üzerinde hiçbir mikroskobik değişiklik olmaz",
                            "isCorrect": False,
                            "explanation": "Hava kuruması en ağır hücresel morfoloji bozukluklarından biridir."
                        },
                        {
                            "key": "D",
                            "text": "Lamın kendisi radyasyon yayarak patoloğu zehirler",
                            "isCorrect": False,
                            "explanation": "Radyoaktif bir durum yoktur."
                        }
                    ]
                }
            ]
        },
        # S87
        {
            "slideNumber": 87,
            "title": "Servikovajinal Smear Yeterlilik Kriterleri: Transformasyon Zonu Hücreleri",
            "subtitle": "Metaplastik hücreler, endoservikal hücre kümeleri ve Bethesda yeterlilik standardı",
            "clinicalFocus": "Sitolojik Kalite Standardı",
            "content": "Bir Pap smear raporunun güvenilir kabul edilebilmesi için en kritik koşul, preparatın **değerlendirme için yeterli (satisfactory for evaluation)** olmasıdır.\n\n- **Hücresel Sayı Kriteri:** Konvansiyonel yaymada en az 8.000 - 12.000, sıvı bazlı sitolojide ise en az 5.000 iyi korunmuş yassı epitel hücresinin mikroskop altında sayılabilmesi gerekir.\n- **Transformasyon Zonu Örnekleme Kriteri:** Yaymada en az **10 adet iyi korunmuş endoservikal hücre veya skuamöz metaplastik hücre** (tek tek veya kümeler halinde) bulunmalıdır. Bu hücrelerin varlığı, fırçanın karsinogenez odağı olan transformasyon zonuna ve skuamokolumnar bileşkeye ulaştığının kanıtıdır.\n- **Yetersiz Rapor:** Transformasyon zonu hücreleri içermeyen veya %75'inden fazlası kan/inflamasyonla örtülü yaymalar 'yetersiz' olarak raporlanır ve hekim tarafından tekrarlanması istenir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Yeterli bir servikal smear incelemesinde transformasyon zonunun örneklendiğini kanıtlayan en az 10 adet endoservikal veya skuamöz metaplastik hücre bulunması zorunludur.",
            "synthesisNarrative": "Bir Pap smear raporunun güvenilir kabul edilebilmesi için en kritik koşul, preparatın **değerlendirme için yeterli (satisfactory for evaluation)** olmasıdır.\n\n- **Hücresel Sayı Kriteri:** Konvansiyonel yaymada en az 8.000 - 12.000, sıvı bazlı sitolojide ise en az 5.000 iyi korunmuş yassı epitel hücresinin mikroskop altında sayılabilmesi gerekir.\n- **Transformasyon Zonu Örnekleme Kriteri:** Yaymada en az **10 adet iyi korunmuş endoservikal hücre veya skuamöz metaplastik hücre** (tek tek veya kümeler halinde) bulunmalıdır. Bu hücrelerin varlığı, fırçanın karsinogenez odağı olan transformasyon zonuna ve skuamokolumnar bileşkeye ulaştığının kanıtıdır.\n- **Yetersiz Rapor:** Transformasyon zonu hücreleri içermeyen veya %75'inden fazlası kan/inflamasyonla örtülü yaymalar 'yetersiz' olarak raporlanır ve hekim tarafından tekrarlanması istenir.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Yeterli bir servikal smear incelemesinde transformasyon zonunun örneklendiğini kanıtlayan en az 10 adet endoservikal veya skuamöz metaplastik hücre bulunması zorunludur.",
            "bulletPoints": [
                "Pap smearin yeterli sayılması için yeterli sayıda skuamöz hücre gerekir.",
                "En az 10 endoservikal veya skuamöz metaplastik hücre zorunludur.",
                "Transformasyon zonu örneklenmemiş yaymalar yetersiz kabul edilir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Smear preparatında transformasyon zonunun örneklendiğini kanıtlayan en az 10 adet endoservikal hücre veya metaplastik hücre bulunmalıdır.",
                    "maskedTerm": "endoservikal hücre",
                    "hint": "Müsin salgılayan kolumnar kanal hücresi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bethesda Smear Yeterlilik Standartları",
                    "tableHeaders": ["Kriter", "Gereken Minimum Eşik", "Karşılanmazsa Sonuç"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Yassı Epitel Sayısı", "isMasked": False},
                                {"text": "5.000 - 12.000 hücre", "isMasked": True, "hint": "yeterli skuamöz hücre yoğunluğu"},
                                {"text": "Yetersiz yayma, tekrar istenir"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Transformasyon Zonu Kanıtı", "isMasked": False},
                                {"text": "En az 10 endoservikal / metaplastik hücre", "isMasked": True, "hint": "kanal örnekleme kriteri"},
                                {"text": "Transformasyon zonu bileşeni yok olarak not edilir"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Doğru Örneklemeden Yeterli Sitolojiye",
                    "steps": [
                        "1. Servikal Fırçalama: Fırça endoservikal kanal ağzına sokularak 360 derece döndürülür.",
                        "2. Kanal Hücreleri Toplama: Kolumnar ve metaplastik hücreler fırça kıllarına tutunur.",
                        "3. Lam İncelemesi: Patolog yaymada petek benzeri endoservikal hücre kümelerini sayar.",
                        "4. Yeterlilik Onayı: En az 10 hücre görülerek rapor 'değerlendirme için yeterli' onayını alır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bethesda sistemine göre bir servikal smear yaymasında karsinogenez bölgesi olan transformasyon zonunun örneklendiğini kanıtlayan hücresel kriter nedir?",
                    "answer": "En az 10 adet iyi korunmuş endoservikal hücre veya skuamöz metaplastik hücrenin varlığıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Smear Yeterlilik Kriterleri",
                    "items": [
                        {"text": "Transformasyon zonunun örneklendiğini kanıtlamak için endoservikal hücreler aranır.", "isLie": False, "explanation": "Doğru. Standart yeterlilik ölçütüdür."},
                        {"text": "En az 10 adet endoservikal veya metaplastik hücre bulunması beklenir.", "isLie": False, "explanation": "Doğru. Sayısal yeterlilik eşiğidir."},
                        {"text": "Yeterli hücre içermeyen yaymalar tekrar edilmelidir.", "isLie": False, "explanation": "Doğru. Güvenilir tanı için şarttır."},
                        {"text": "Smear yaymasında sadece 1 adet eritrosit bulunması tüm rahim kanserlerini kesin teşhis eder.", "isLie": True, "explanation": "Tuzak! Eritrosit kanser teşhis ettirmez; binlerce korunmuş epitel hücresi aranır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Bethesda sitoloji sınıflamasına göre servikovajinal bir yaymanın 'değerlendirme için yeterli' kabul edilmesi ve transformasyon zonunun örneklendiğinin kanıtlanması için hangi hücre grubu bulunmalıdır?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "En az 10 adet endoservikal hücre veya skuamöz metaplastik hücre",
                            "isCorrect": True,
                            "explanation": "Bu hücrelerin varlığı transformasyon zonunun örneklendiğini kanıtlar."
                        },
                        {
                            "key": "B",
                            "text": "En az 500 adet çizgili kas miyoblastı",
                            "isCorrect": False,
                            "explanation": "Servikal smearde çizgili kas bulunmaz."
                        },
                        {
                            "key": "C",
                            "text": "Safra kesesi kolesterol kristalleri",
                            "isCorrect": False,
                            "explanation": "Sindirim sistemi bulgusudur."
                        },
                        {
                            "key": "D",
                            "text": "Yalnızca göz retina fotoreseptörleri",
                            "isCorrect": False,
                            "explanation": "Göz histolojisidir."
                        }
                    ]
                }
            ]
        },
        # S88
        {
            "slideNumber": 88,
            "title": "Kolposkopi ve Asetik Asit: Asetobeyaz Epitel Biyofiziksel Prensibi",
            "subtitle": "Nükleus-sitoplazma yoğunluğu, ışık kırılması ve punktuasyon / mozaizm",
            "clinicalFocus": "Tanısal Biyofizik",
            "content": "Kolposkopik incelemede displastik alanları saptamak için kullanılan **%3-5'lik asetik asit uygulamasının** altında yatan mekanizma tamamen biyofiziksel bir protein koagülasyonu olayıdır.\n\n- **Biyofiziksel Mekanizma:** Asetik asit hücre zarını geçerek intraselüler proteinleri ve özellikle nükleer proteinleri geçici olarak çöktürür (dehidrate eder/koagüle eder). Normal olgun skuamöz hücrelerde sitoplazma bol, nükleus küçüktür; ışık alttaki pembe damarlı stromaya ulaşıp geri yansır ve doku pembe görünür.\n- **Asetobeyaz Değişiklik:** Displastik hücrelerde (CIN) nükleus devasa, nükleus/sitoplazma oranı aşırı yüksek ve hücreler birbirine çok sıkışıktır. Asetik asit bu yoğun nükleer proteinleri çökelttiğinde ışık stromaya geçemez, yüzeyden opak olarak geri yansır ve doku gözümüze **parlak kireç beyazı (asetobeyaz epitel)** olarak görünür.\n- **Vasküler Bulgular:** Atipik neovaskülarizasyon sonucu kapillerlerin yüzeye dik veya paralel uzanmasıyla **punktuasyon (noktalanma)** ve **mozaik damarlanma** paternleri ortaya çıkar.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Asetik asit uygulandığında displastik hücrelerdeki yüksek nükleer protein yoğunluğunun ışığı geçirmeyip yansıtması asetobeyaz epitel görünümünü oluşturur.",
            "synthesisNarrative": "Kolposkopik incelemede displastik alanları saptamak için kullanılan **%3-5'lik asetik asit uygulamasının** altında yatan mekanizma tamamen biyofiziksel bir protein koagülasyonu olayıdır.\n\n- **Biyofiziksel Mekanizma:** Asetik asit hücre zarını geçerek intraselüler proteinleri ve özellikle nükleer proteinleri geçici olarak çöktürür (dehidrate eder/koagüle eder). Normal olgun skuamöz hücrelerde sitoplazma bol, nükleus küçüktür; ışık alttaki pembe damarlı stromaya ulaşıp geri yansır ve doku pembe görünür.\n- **Asetobeyaz Değişiklik:** Displastik hücrelerde (CIN) nükleus devasa, nükleus/sitoplazma oranı aşırı yüksek ve hücreler birbirine çok sıkışıktır. Asetik asit bu yoğun nükleer proteinleri çökelttiğinde ışık stromaya geçemez, yüzeyden opak olarak geri yansır ve doku gözümüze **parlak kireç beyazı (asetobeyaz epitel)** olarak görünür.\n- **Vasküler Bulgular:** Atipik neovaskülarizasyon sonucu kapillerlerin yüzeye dik veya paralel uzanmasıyla **punktuasyon (noktalanma)** ve **mozaik damarlanma** paternleri ortaya çıkar.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Asetik asit uygulandığında displastik hücrelerdeki yüksek nükleer protein yoğunluğunun ışığı geçirmeyip yansıtması asetobeyaz epitel görünümünü oluşturur.",
            "bulletPoints": [
                "Asetik asit yüksek nükleer proteinleri geçici çökelterek opaklaştırır.",
                "Yüksek N/S oranlı displastik epitel ışığı yansıtarak asetobeyaz görünür.",
                "Punktuasyon ve mozaizm displaziye eşlik eden atipik damarlanmalardır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Kolposkopide asetik asit uygulandığında nükleer protein yoğunluğuna bağlı olarak oluşan opak beyaz görünüme asetobeyaz epitel adı verilir.",
                    "maskedTerm": "asetobeyaz epitel",
                    "hint": "Displazik sahanın sirke ruhu ile beyazlaşması bulgusu"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Kolposkopik Bulguların Biyofiziksel Karşılığı",
                    "tableHeaders": ["Kolposkopik Bulgu", "Hücresel / Vasküler Mekanizma", "Patolojik Anlam"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Asetobeyaz Epitel", "isMasked": False},
                                {"text": "Yüksek N/S oranlı hücrelerde nükleer protein koagülasyonu", "isMasked": True, "hint": "opak protein çökelmesi"},
                                {"text": "Displazi / CIN lezyonu göstergesi"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Punktuasyon ve Mozaizm", "isMasked": False},
                                {"text": "Epitel içine dik uzanan veya ağımsı anormal kapillerler", "isMasked": True, "hint": "neovasküler damar anomalisi"},
                                {"text": "Yüksek dereceli intraepitelyal lezyon (HSIL)"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Asetik Asitten Asetobeyaz Görünüme",
                    "steps": [
                        "1. Solüsyon Teması: %3'lük asetik asit serviks mukozasına pamukla uygulanır.",
                        "2. Protein Çökmesi: Displastik hücrelerin dev çekirdeklerindeki nükleoproteinler koagüle olur.",
                        "3. Işık Refleksiyonu: Opaklaşan hücre katmanı ışığın alttaki damarlara geçişini engeller.",
                        "4. Asetobeyaz Vizüalizasyon: Kolposkop merceğinde kireç beyazı alan parlar ve biyopsi alınır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Kolposkopi sırasında asetik asit uygulanan displastik hücrelerin beyazlaşmasının (asetobeyaz epitel) biyofiziksel nedeni nedir?",
                    "answer": "Yüksek nükleus/sitoplazma oranına sahip hücrelerdeki nükleer proteinlerin asetik asitle geçici koagülasyona uğraması ve ışığı opak olarak geri yansıtmasıdır."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Asetobeyaz Epitel Biyofiziği",
                    "items": [
                        {"text": "Asetik asit nükleer proteinleri geçici olarak koagüle eder.", "isLie": False, "explanation": "Doğru. Biyofiziksel temeldir."},
                        {"text": "Yüksek nükleer yoğunluklu displastik epitel opak beyaz görünür.", "isLie": False, "explanation": "Doğru. Asetobeyaz oluşumudur."},
                        {"text": "Punktuasyon ve mozaizm anormal tümör damarlanmalarını yansıtır.", "isLie": False, "explanation": "Doğru. Tipik kolposkopi bulgularıdır."},
                        {"text": "Asetobeyaz alanlar servikse dökülen süt tozunun birikmesiyle oluşur.", "isLie": True, "explanation": "Tuzak! Dışarıdan süt tozu dökülmez; hücresel nükleer proteinlerin asitle opaklaşmasıdır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Kolposkopik incelemede serviks yüzeyine %3-5 asetik asit uygulandığında displastik epitelin beyaz görünmesinin (asetobeyaz değişiklik) temel nedeni nedir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Displastik hücrelerdeki yüksek nükleer protein içeriğinin asitle koagüle olarak ışığı opak geri yansıtması",
                            "isCorrect": True,
                            "explanation": "Asetobeyaz epitel yüksek N/S oranlı hücrelerin nükleer protein presipitasyonu ile oluşur."
                        },
                        {
                            "key": "B",
                            "text": "Bölgedeki tüm kanın aniden saf altına dönüşmesi",
                            "isCorrect": False,
                            "explanation": "Biyolojik olarak anlamsızdır."
                        },
                        {
                            "key": "C",
                            "text": "Serviks kemiklerinin kireç dökmesi",
                            "isCorrect": False,
                            "explanation": "Servikste kemik bulunmaz."
                        },
                        {
                            "key": "D",
                            "text": "Asetik asidin tümör hücrelerini anında buharlaştırması",
                            "isCorrect": False,
                            "explanation": "Asetik asit buharlaştırmaz, geçici protein koagülasyonu yapar."
                        }
                    ]
                }
            ]
        },
        # S89
        {
            "slideNumber": 89,
            "title": "Lugol İyot (Schiller Testi) ve Glikojen Kaybı Mekanizması",
            "subtitle": "İyot negatif (Schiller pozitif) soluk alanlar ve displazi haritalaması",
            "clinicalFocus": "Tanısal Biyokimya",
            "content": "Kolposkopide ve servikal muayenede lezyon sınırlarını belirlemek için kullanılan ikinci temel biyokimyasal yöntem **Lugol İyot solüsyonu (Schiller Testi)** uygulamasıdır.\n\n- **Biyokimyasal Dayanak:** Normal ektoservikal matür çok katlı yassı epitel hücreleri bol miktarda **glikojen** içerir. İyot molekülleri glikojen polimerleri ile reaksiyona girerek dokuyu **koyu maun kahverengisi / siyaha** boyar (Schiller Negatif - Normal epitel).\n- **Displastik Epitelde Glikojen Kaybı:** Neoplastik displastik hücreler (CIN) hızla çoğaldıkları ve diferansiye olamadıkları için glikojen sentezleyemezler ve glikojenden yoksundurlar. Lugol iyot sürüldüğünde bu atipik alanlar **iyot boyasını tutamaz ve parlak hardal sarısı / soluk sarı** renkte kalır.\n- **Schiller Pozitif Alan:** İyot tutmayan bu soluk hardal sarısı alanlara 'Schiller Pozitif' denir ve hekime biyopsi alacağı displastik lezyon sınırlarını kusursuz biçimde haritalandırır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Schiller testinde normal epitel glikojen içerdiğinden iyotla kahverengi boyanır; glikojenden yoksun displastik epitel ise iyot tutmayarak hardal sarısı/soluk kalır (Schiller pozitif).",
            "synthesisNarrative": "Kolposkopide ve servikal muayenede lezyon sınırlarını belirlemek için kullanılan ikinci temel biyokimyasal yöntem **Lugol İyot solüsyonu (Schiller Testi)** uygulamasıdır.\n\n- **Biyokimyasal Dayanak:** Normal ektoservikal matür çok katlı yassı epitel hücreleri bol miktarda **glikojen** içerir. İyot molekülleri glikojen polimerleri ile reaksiyona girerek dokuyu **koyu maun kahverengisi / siyaha** boyar (Schiller Negatif - Normal epitel).\n- **Displastik Epitelde Glikojen Kaybı:** Neoplastik displastik hücreler (CIN) hızla çoğaldıkları ve diferansiye olamadıkları için glikojen sentezleyemezler ve glikojenden yoksundurlar. Lugol iyot sürüldüğünde bu atipik alanlar **iyot boyasını tutamaz ve parlak hardal sarısı / soluk sarı** renkte kalır.\n- **Schiller Pozitif Alan:** İyot tutmayan bu soluk hardal sarısı alanlara 'Schiller Pozitif' denir ve hekime biyopsi alacağı displastik lezyon sınırlarını kusursuz biçimde haritalandırır.\n\n> [!IMPORTANT]\n> [SINAV SPOTU] Schiller testinde normal epitel glikojen içerdiğinden iyotla kahverengi boyanır; glikojenden yoksun displastik epitel ise iyot tutmayarak hardal sarısı/soluk kalır (Schiller pozitif).",
            "bulletPoints": [
                "Normal skuamöz epitel glikojen içerdiğinden Lugol iyot ile koyu kahverengi boyanır.",
                "Displastik epitel glikojen içermediğinden iyot tutmaz ve hardal sarısı kalır.",
                "İyot tutmayan sarı alanlar (Schiller pozitif) biyopsi için hedeflenir."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Schiller testinde normal skuamöz epitel glikojen içeriği sayesinde Lugol iyot ile koyu maun kahverengi renge boyanır.",
                    "maskedTerm": "glikojen",
                    "hint": "İyotla reaksiyona giren hücre içi depo polisakkariti"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Schiller Testinde Boyanma Dinamiği",
                    "tableHeaders": ["Doku Durumu", "Glikojen Varlığı", "Lugol İyot Boyanma Rengi", "Schiller Yorumu"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Normal Matür Skuamöz Epitel", "isMasked": False},
                                {"text": "Bol miktarda glikojen mevcut", "isMasked": False},
                                {"text": "Koyu maun kahverengisi / siyah", "isMasked": True, "hint": "iyotla koyulaşan renk"},
                                {"text": "Schiller Negatif (Sağlıklı doku)"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Displastik Epitel (CIN)", "isMasked": False},
                                {"text": "Glikojen sentezlenemez (yok)", "isMasked": True, "hint": "atipik hücrede glikojen kaybı"},
                                {"text": "İyot tutmaz, hardal sarısı / soluk kalır", "isMasked": False},
                                {"text": "Schiller Pozitif (Biyopsi hedefi)"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Glikojen Eksikliğinden Schiller Pozitifliğine",
                    "steps": [
                        "1. Solüsyon Uygulaması: Servikse Lugol iyot solüsyonu sürülür.",
                        "2. Normal Bölge: Glikojen içeren çevre normal hücreler iyotla birleşerek kararır.",
                        "3. Displastik Odak: CIN lezyonunda glikojen olmadığından iyot bağlanamaz.",
                        "4. Schiller Pozitif Harita: Siyah zemin üzerinde hardal sarısı kalan odaktan biyopsi alınır."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Schiller testinde displastik servikal epitelin Lugol iyot ile boyanmayıp hardal sarısı kalmasının (Schiller pozitifliği) biyokimyasal nedeni nedir?",
                    "answer": "Displastik hücrelerin olgunlaşamaması nedeniyle glikojen depolayamaması ve glikojensiz hücrelerin iyotla renk reaksiyonu verememesidir."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Schiller Testi ve Lugol İyot",
                    "items": [
                        {"text": "Normal matür skuamöz epitel glikojen içerdiğinden iyotla koyu kahverengi boyanır.", "isLie": False, "explanation": "Doğru. Fizyolojik boyanmadır."},
                        {"text": "Displastik epitel glikojen taşımadığı için iyot tutmaz ve hardal sarısı kalır.", "isLie": False, "explanation": "Doğru. Schiller pozitif alanıdır."},
                        {"text": "İyot tutmayan soluk alanlar biyopsi için rehberlik eder.", "isLie": False, "explanation": "Doğru. Hedeflenen sahadır."},
                        {"text": "Schiller testi hastanın göz bebeklerine limon suyu sıkılarak yapılan bir nöroloji testidir.", "isLie": True, "explanation": "Tuzak! Schiller testi servikse Lugol iyot sürülerek yapılan bir jinekolojik karsinom tarama yöntemidir."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Servikal kolposkopi sırasında uygulanan Schiller testinde (Lugol iyot) displastik alanların iyot tutmayarak hardal sarısı kalmasının biyokimyasal nedeni hangisidir?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Displastik epitel hücrelerinin glikojenden yoksun olması ve iyotla reaksiyona girememesi",
                            "isCorrect": True,
                            "explanation": "Displastik hücreler diferansiye olamadığı için glikojen sentezleyemez ve iyot tutmaz."
                        },
                        {
                            "key": "B",
                            "text": "Tümör hücrelerinin safra asitleri ile dolu olması",
                            "isCorrect": False,
                            "explanation": "Servikste safra asidi bulunmaz."
                        },
                        {
                            "key": "C",
                            "text": "İyot solüsyonunun yalnızca demir atomlarını eritmesi",
                            "isCorrect": False,
                            "explanation": "Schiller testinin prensibi demir değil glikojendir."
                        },
                        {
                            "key": "D",
                            "text": "Normal epitelin iyot ile beyaz, tümörün ise mor olması",
                            "isCorrect": False,
                            "explanation": "Normal epitel koyu maun kahverengi, tümör hardal sarısı kalır."
                        }
                    ]
                }
            ]
        },
        # S90
        {
            "slideNumber": 90,
            "title": "[TEKRAR SAYFASI - CHECKPOINT 9] Alan Kanserleşmesi, Gebelik ve Tanısal Biyofizik",
            "subtitle": "Bölüm 9 kapsamındaki Alan Kanserleşmesi, immünsüpresyon, gebelik sitolojisi, kolposkopi ve Schiller testi sentezi",
            "clinicalFocus": "Kapsamlı Bölüm Tekrarı",
            "content": "Bölüm 9 boyunca alt genital sistemin alan kanserleşmesi kavramını, immün yetmezlik dinamiklerini, gebelik sitopatolojisini ve tanısal biyofizik/biyokimyasal yöntemleri sentezledik.\n\n- **Alan Kanserleşmesi ve İmmünite:** Alt genital traktus geniş bir HPV sahasıdır; CIN, VIN ve VAIN multisentrik birliktelik gösterebilir. HIV ve nakil hastalarında hücresel immünite çöktüğünden karsinom progresyonu dramatik hızlanır.\n- **Gebelik Özellikleri:** Progesteron etkisiyle glikojen dolu naviküler hücreler belirir; Candida sıklığı artar. Aktif genital HSV varlığında sezaryen doğum hayat kurtarır.\n- **Biyofizik ve Biyokimya:** Asetik asit yüksek nükleer proteinleri çökelterek displaziyi asetobeyaz yapar; Lugol iyot (Schiller testi) ise glikojensiz displastik epitelin iyot tutmayarak hardal sarısı kalmasıyla lezyonu haritalar.\n\n> [!IMPORTANT]\n> [CHECKPOINT SENTEZİ] Alan kanserleşmesi multisentrik lezyonları (CIN+VIN+VAIN) açıklar; asetobeyazlık nükleer protein koagülasyonuyla, Schiller pozitifliği ise displastik hücrelerdeki glikojen kaybıyla oluşur.",
            "synthesisNarrative": "Bölüm 9 boyunca alt genital sistemin alan kanserleşmesi kavramını, immün yetmezlik dinamiklerini, gebelik sitopatolojisini ve tanısal biyofizik/biyokimyasal yöntemleri sentezledik.\n\n- **Alan Kanserleşmesi ve İmmünite:** Alt genital traktus geniş bir HPV sahasıdır; CIN, VIN ve VAIN multisentrik birliktelik gösterebilir. HIV ve nakil hastalarında hücresel immünite çöktüğünden karsinom progresyonu dramatik hızlanır.\n- **Gebelik Özellikleri:** Progesteron etkisiyle glikojen dolu naviküler hücreler belirir; Candida sıklığı artar. Aktif genital HSV varlığında sezaryen doğum hayat kurtarır.\n- **Biyofizik ve Biyokimya:** Asetik asit yüksek nükleer proteinleri çökelterek displaziyi asetobeyaz yapar; Lugol iyot (Schiller testi) ise glikojensiz displastik epitelin iyot tutmayarak hardal sarısı kalmasıyla lezyonu haritalar.\n\n> [!IMPORTANT]\n> [CHECKPOINT SENTEZİ] Alan kanserleşmesi multisentrik lezyonları (CIN+VIN+VAIN) açıklar; asetobeyazlık nükleer protein koagülasyonuyla, Schiller pozitifliği ise displastik hücrelerdeki glikojen kaybıyla oluşur.",
            "bulletPoints": [
                "Alan kanserleşmesi multisentrik CIN, VAIN ve VIN lezyonlarına yol açar.",
                "Gebelikte naviküler hücreler hakimdir; aktif HSV'de sezaryen endikedir.",
                "Asetobeyazlık nükleer protein koagülasyonu, Schiller pozitifliği ise glikojen kaybıdır."
            ],
            "relatedQuestions": [],
            "interactiveElements": [
                {
                    "type": "cloze_masking",
                    "sentence": "Schiller testinde displastik epitelin iyot tutmayıp sarı kalması hücrelerdeki glikojen kaybı sonucudur.",
                    "maskedTerm": "glikojen kaybı",
                    "hint": "İntraselüler depo karbonhidratının neoplazide sentezlenememesi"
                },
                {
                    "type": "interactive_table",
                    "tableTitle": "Bölüm 9 Tanısal Prensip Karşılaştırması",
                    "tableHeaders": ["Yöntem / Test", "Kullanılan Ajan", "Pozitiflik Mekanizması"],
                    "tableRows": [
                        {
                            "cells": [
                                {"text": "Asetobeyaz Testi", "isMasked": False},
                                {"text": "%3-5 Asetik Asit", "isMasked": False},
                                {"text": "Yüksek N/S nükleer protein koagülasyonu ve ışık yansıması", "isMasked": True, "hint": "nükleer presipitasyon"}
                            ]
                        },
                        {
                            "cells": [
                                {"text": "Schiller Testi", "isMasked": False},
                                {"text": "Lugol İyot Solüsyonu", "isMasked": False},
                                {"text": "Glikojen yokluğu nedeniyle boya tutamama (hardal sarısı)", "isMasked": True, "hint": "glikojensiz sahanın açık kalması"}
                            ]
                        }
                    ]
                },
                {
                    "type": "causal_chain",
                    "chainTitle": "Bölüm 9 Klinik Karar ve Haritalama Zinciri",
                    "steps": [
                        "1. Alan Şüphesi: Serviks CIN 3 öykülü hastada vajina ve vulva kolposkopla taranır.",
                        "2. Asetik Asit: Sirke ruhu yoğun nükleuslu displastik odakları asetobeyaz parlatır.",
                        "3. Schiller Testi: Lugol iyot sürülür; glikojensiz displastik alan sarı kalarak sınırları çizer.",
                        "4. Biyopsi Doğrulaması: Hardal sarısı asetobeyaz odaktan biyopsi alınarak VAIN/CIN tanısı konur."
                    ]
                },
                {
                    "type": "active_recall",
                    "question": "Bölüm 9'da incelenen kolposkopik iki temel boyama yöntemi olan asetik asit ve Lugol iyot (Schiller) testlerinin fizikokimyasal temel mekanizmaları nelerdir?",
                    "answer": "Asetik asit yüksek nükleer proteinleri koagüle ederek asetobeyaz görünüm oluşturur; Lugol iyot ise glikojensiz displastik epitelin boya tutmayıp hardal sarısı (Schiller pozitif) kalmasıyla lezyonu haritalar."
                },
                {
                    "type": "spot_the_lie",
                    "topic": "Bölüm 9 Genel Tekrar",
                    "items": [
                        {"text": "Alan kanserleşmesi multisentrik CIN, VAIN ve VIN birlikteliğini açıklar.", "isLie": False, "explanation": "Doğru. Yaygın HPV maruziyetidir."},
                        {"text": "Asetobeyazlık nükleer protein koagülasyonuyla ışığın geri yansımasıdır.", "isLie": False, "explanation": "Doğru. Biyofiziksel temeldir."},
                        {"text": "Schiller testinde displastik hücreler glikojen yokluğu nedeniyle boyanmaz.", "isLie": False, "explanation": "Doğru. Hardal sarısı kalır."},
                        {"text": "Gebelikte aktif HSV lezyonları olan tüm kadınlara zorla vajinal doğum yaptırılmalıdır.", "isLie": True, "explanation": "Tuzak! Aktif genital HSV'de bebeği korumak için vajinal doğum kesinlikle kontrendikedir, sezaryen uygulanır."}
                    ]
                },
                {
                    "type": "micro_quiz",
                    "question": "Bölüm 9'da incelenen konularla ilgili aşağıdaki ifadelerden hangisi DOĞRUDUR?",
                    "microQuizOptions": [
                        {
                            "key": "A",
                            "text": "Alan kanserleşmesi multisentrik neoplazilere yol açar; asetobeyazlık nükleer protein koagülasyonuyla, Schiller pozitifliği ise glikojen kaybıyla oluşur",
                            "isCorrect": True,
                            "explanation": "Bu sentez cümlesi hem onkopatolojik yayılımı hem de iki temel kolposkopik yöntemin mekanizmasını eksiksiz özetler."
                        },
                        {
                            "key": "B",
                            "text": "Schiller testinde tümör hücreleri glikojenle patlayarak masif köpük üretir",
                            "isCorrect": False,
                            "explanation": "Biyokimyasal gerçekliği yoktur."
                        },
                        {
                            "key": "C",
                            "text": "Gebelikte naviküler hücrelerin görülmesi derhal acil kemoterapi endikasyonudur",
                            "isCorrect": False,
                            "explanation": "Naviküler hücreler tamamen fizyolojik gebelik bulgusudur."
                        },
                        {
                            "key": "D",
                            "text": "HIV pozitif hastalarda HPV virüsleri hiçbir zaman çoğalamaz",
                            "isCorrect": False,
                            "explanation": "İmmün yetmezlikte HPV aşırı çoğalır ve hızla kansere ilerler."
                        }
                    ]
                }
            ]
        }
    ]
    return slides

if __name__ == '__main__':
    slides = get_s9_slides()
    print(f'Section 9 generated with {len(slides)} slides.')
