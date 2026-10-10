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
                        {"text": "Pap smear için mutlaka hastaya genel anestezi altında tam kat açık biyopsi yapılmalıdır.", "isLie": True, "explanation": "Tuzak! Pap smear invaziv cerrahi biyopsi değil, poliklinikte anestezi gerektirmeyen yüzeyel sürüntü (sitoloji) yöntemidir."}
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
        }
    ]
    return slides

if __name__ == '__main__':
    print("S5 draft initialized.")
